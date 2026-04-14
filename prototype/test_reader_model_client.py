"""
test_reader_model_client.py — tests for the reader-model LLM client.

These tests exercise the client's structural invariants — scope
enforcement (R5), the question-only rule for answers, dropped-output
auditability — without calling the API. They construct synthetic
ReaderOutput records (the Pydantic type the SDK would return from
parse()) and run them through the client's classify/translate
pipeline.

Run:
    .venv/bin/python3 test_reader_model_client.py
"""

from __future__ import annotations

import sys
import traceback

from substrate import (
    AnswerProposal,
    Attention,
    Description,
    DescStatus,
    anchor_event,
    anchor_desc,
)
from reader_model_client import (
    DroppedOutput,
    ReaderAnswer,
    ReaderOutput,
    ReaderReview,
    _classify_answer,
    _classify_review,
    _translate_answer,
    _translate_review,
    invoke_reader_model,
)


# ============================================================================
# Fixtures
# ============================================================================


def _make_descriptions() -> list:
    """Three descriptions: one normal, one that is a question, one anchored
    on another description."""
    return [
        Description(
            id="D_alpha",
            attached_to=anchor_event("E_main"),
            kind="texture",
            attention=Attention.INTERPRETIVE,
            text="alpha texture",
            authored_by="author",
            τ_a=10,
            is_question=False,
        ),
        Description(
            id="D_beta",
            attached_to=anchor_event("E_main"),
            kind="authorial-uncertainty",
            attention=Attention.STRUCTURAL,
            text="am I doing this right?",
            authored_by="author",
            τ_a=11,
            is_question=True,
        ),
        Description(
            id="D_gamma",
            attached_to=anchor_desc("D_beta"),
            kind="motivation",
            attention=Attention.INTERPRETIVE,
            text="beta-related motivation",
            authored_by="author",
            τ_a=12,
            is_question=False,
        ),
    ]


def _make_event_list() -> list:
    """Bare event used as an anchor."""
    from substrate import Event, CANONICAL_LABEL

    return [
        Event(
            id="E_main",
            type="test",
            τ_s=0,
            τ_a=5,
            participants={},
            effects=(),
            branches=frozenset({CANONICAL_LABEL}),
        ),
    ]


# ============================================================================
# R5 — scope enforcement on reviews
# ============================================================================


def test_review_in_reviews_for_is_accepted():
    """A review targeting a description in reviews_for AND present in
    the descriptions collection is accepted."""
    descriptions = _make_descriptions()
    raw = ReaderReview(
        description_id="D_alpha",
        verdict="approved",
        rationale="looks fine",
    )
    reason = _classify_review(raw, descriptions, reviews_for=["D_alpha"])
    assert reason is None, f"expected accepted; got drop reason: {reason}"


def test_review_outside_reviews_for_is_rejected():
    """R5: even if the description exists in the collection, reviewing it
    must have been requested. Out-of-scope reviews drop at ingest."""
    descriptions = _make_descriptions()
    raw = ReaderReview(
        description_id="D_gamma",
        verdict="approved",
        rationale="not in scope",
    )
    reason = _classify_review(raw, descriptions, reviews_for=["D_alpha"])
    assert reason is not None, (
        "R5 violation: review for D_gamma was accepted even though "
        "reviews_for=['D_alpha']"
    )
    assert "reviews_for" in reason, \
        f"reason should mention reviews_for; got {reason!r}"


def test_review_for_unknown_id_is_rejected():
    """If reviews_for lists an id that doesn't resolve, it still
    rejects — validation is both membership AND resolvability."""
    descriptions = _make_descriptions()
    raw = ReaderReview(
        description_id="D_nonexistent",
        verdict="approved",
        rationale="ghost",
    )
    reason = _classify_review(
        raw, descriptions, reviews_for=["D_nonexistent"]
    )
    assert reason is not None
    assert "does not resolve" in reason


# ============================================================================
# R5 + question-only: scope enforcement on answers
# ============================================================================


def test_answer_in_answers_for_and_is_question_is_accepted():
    """An answer targeting an is_question=True description in
    answers_for is accepted."""
    descriptions = _make_descriptions()
    raw = ReaderAnswer(
        question_description_id="D_beta",
        answer_kind="reader-frame",
        answer_text="here is an answer",
        rationale="because",
    )
    reason = _classify_answer(raw, descriptions, answers_for=["D_beta"])
    assert reason is None, f"expected accepted; got drop reason: {reason}"


def test_answer_outside_answers_for_is_rejected():
    """R5: out-of-scope answer is dropped even if its target exists and
    is a question."""
    descriptions = _make_descriptions()
    raw = ReaderAnswer(
        question_description_id="D_beta",
        answer_kind="reader-frame",
        answer_text="here",
        rationale="because",
    )
    reason = _classify_answer(raw, descriptions, answers_for=[])
    assert reason is not None, \
        "R5 violation: answer for D_beta accepted with answers_for=[]"
    assert "answers_for" in reason


def test_answer_to_non_question_description_is_rejected():
    """Contract bug the reviewer flagged: LLM emits an answer targeting
    an ordinary description (is_question=False). Must drop at ingest,
    even if the target is in answers_for."""
    descriptions = _make_descriptions()
    raw = ReaderAnswer(
        question_description_id="D_alpha",  # is_question=False
        answer_kind="texture",
        answer_text="trying to answer a non-question",
        rationale="shouldn't land",
    )
    reason = _classify_answer(raw, descriptions, answers_for=["D_alpha"])
    assert reason is not None, (
        "contract violation: answer for D_alpha accepted even though "
        "D_alpha.is_question=False"
    )
    assert "not a question" in reason, \
        f"reason should name the is_question violation; got {reason!r}"


def test_answer_for_unknown_id_is_rejected():
    """If answers_for lists an id that doesn't resolve, it rejects."""
    descriptions = _make_descriptions()
    raw = ReaderAnswer(
        question_description_id="D_nonexistent",
        answer_kind="reader-frame",
        answer_text="ghost answer",
        rationale="ghost",
    )
    reason = _classify_answer(
        raw, descriptions, answers_for=["D_nonexistent"]
    )
    assert reason is not None
    assert "does not resolve" in reason


# ============================================================================
# Translation: accepted records become substrate-native
# ============================================================================


def test_translate_review_produces_review_entry():
    """Once classify accepts, translate builds a ReviewEntry with the
    expected fields — reviewer_id, verdict, anchor_τ_a from the target's
    anchor, comment from the rationale."""
    from substrate import ReviewVerdict

    descriptions = _make_descriptions()
    events = _make_event_list()
    raw = ReaderReview(
        description_id="D_alpha",
        verdict="approved",
        rationale="grounded in view",
    )
    entry = _translate_review(
        raw, descriptions, events,
        reviewer_id="llm:test",
        current_τ_a=100,
    )
    assert entry.reviewer_id == "llm:test"
    assert entry.reviewed_at_τ_a == 100
    assert entry.verdict == ReviewVerdict.APPROVED
    assert entry.anchor_τ_a == 5, (
        f"anchor_τ_a should come from E_main (τ_a=5); got "
        f"{entry.anchor_τ_a}"
    )
    assert entry.comment == "grounded in view"


def test_translate_answer_produces_answer_proposal():
    """An accepted ReaderAnswer becomes an AnswerProposal carrying a
    constructed Description. The new description inherits the question's
    anchor (D3) and branches, but carries its own kind per the LLM's
    proposal, with status=provisional and a metadata link back. The
    proposal itself starts pending and carries proposer_id and
    proposed_at_τ_a so it can be queue-ingested directly."""
    descriptions = _make_descriptions()
    raw = ReaderAnswer(
        question_description_id="D_beta",
        answer_kind="reader-frame",
        answer_text="a reasoned answer",
        rationale="derived",
    )
    pa = _translate_answer(
        raw, descriptions,
        reviewer_id="llm:test",
        current_τ_a=100,
    )
    assert isinstance(pa, AnswerProposal)
    assert pa.question_description_id == "D_beta"
    assert pa.rationale == "derived"
    assert pa.proposer_id == "llm:test"
    assert pa.proposed_at_τ_a == 100
    assert pa.status == "pending"

    d = pa.proposed_description
    # Inherits anchor from the question (D_beta was anchored on E_main).
    assert d.attached_to.kind == "event"
    assert d.attached_to.target_id == "E_main"
    # Author's proposed kind, not the question's kind.
    assert d.kind == "reader-frame"
    # Attention defaults to interpretive for proposed answers.
    assert d.attention == Attention.INTERPRETIVE
    assert d.text == "a reasoned answer"
    assert d.authored_by == "llm:test"
    assert d.τ_a == 100
    assert d.status == DescStatus.PROVISIONAL
    # Provenance link back to the question (for author auditing).
    assert d.metadata.get("answers_question") == "D_beta"


# ============================================================================
# Dropped outputs are auditable
# ============================================================================


class _FakeMessages:
    def __init__(self, output):
        self._output = output

    def parse(self, **kwargs):
        class _R:
            pass
        r = _R()
        r.parsed_output = self._output
        return r


class _FakeClient:
    """Minimal stand-in for anthropic.Anthropic — exposes .messages.parse()
    returning the canned ReaderOutput. Everything else is ignored."""
    def __init__(self, output):
        self.messages = _FakeMessages(output)


def test_review_candidates_paired_correctly_when_raw_reviews_are_dropped():
    """Regression for the zip-misalignment bug. When the LLM returns
    reviews where at least one raw record fails scope validation, the
    dropped record must not shift later records' target_ids. Each
    translated ReviewEntry is authoritatively paired with its raw
    description_id at translation time — not by parallel-indexing the
    full raw.reviews list.
    """
    from substrate import ReaderView

    descriptions = _make_descriptions()
    events = _make_event_list()
    view = ReaderView(
        branch_label=":canonical",
        up_to_τ_s=10,
        up_to_τ_a=100,
        attention_filter=None,
        anchor_scope=None,
        events=(),
        descriptions=(),
        open_questions=(),
    )
    # LLM returns three raw reviews, in this order:
    #   1) valid (D_alpha)
    #   2) out-of-scope (D_gamma NOT in reviews_for)
    #   3) valid (D_beta)
    raw_output = ReaderOutput(
        reviews=[
            ReaderReview(description_id="D_alpha", verdict="approved",
                         rationale="ok"),
            ReaderReview(description_id="D_gamma", verdict="needs-work",
                         rationale="should be dropped — not in scope"),
            ReaderReview(description_id="D_beta",  verdict="rejected",
                         rationale="nope"),
        ],
        answers=[],
    )
    client = _FakeClient(raw_output)
    # D_beta is a question in the test fixtures, but reviewing a question
    # description is legal — reviews_for controls scope, not is_question.
    result = invoke_reader_model(
        view=view,
        events=events,
        descriptions=descriptions,
        current_τ_a=100,
        reviews_for=["D_alpha", "D_beta"],
        answers_for=[],
        client=client,
    )
    # Two survived, one dropped.
    assert len(result.review_candidates) == 2, (
        f"expected 2 surviving review candidates; got "
        f"{len(result.review_candidates)}"
    )
    assert len(result.dropped) == 1
    # The pairings are 1:1 with the accepted raw records, preserving
    # order of arrival. The dropped middle record must NOT cause D_beta
    # to be paired with D_gamma (the bug this pins).
    assert result.review_candidates[0][0] == "D_alpha"
    assert result.review_candidates[0][1].verdict.value == "approved"
    assert result.review_candidates[0][1].comment == "ok"
    assert result.review_candidates[1][0] == "D_beta", (
        f"zip-misalignment bug: expected D_beta paired with the 'rejected' "
        f"review, got {result.review_candidates[1][0]!r}"
    )
    assert result.review_candidates[1][1].verdict.value == "rejected"
    assert result.review_candidates[1][1].comment == "nope"


def test_dropped_output_carries_reason_and_raw_record():
    """DroppedOutput preserves both the reason and the original LLM
    record, so an author can inspect what was rejected."""
    raw = ReaderReview(
        description_id="D_gamma",
        verdict="approved",
        rationale="out of scope",
    )
    d = DroppedOutput(reason="example reason", raw=raw)
    assert d.reason == "example reason"
    assert d.raw is raw
    # The raw record is still a Pydantic object; callers can dump it.
    assert hasattr(d.raw, "model_dump")


# ============================================================================
# Runner
# ============================================================================


TESTS = [
    # R5 — review scope
    test_review_in_reviews_for_is_accepted,
    test_review_outside_reviews_for_is_rejected,
    test_review_for_unknown_id_is_rejected,
    # R5 + question-only — answer scope
    test_answer_in_answers_for_and_is_question_is_accepted,
    test_answer_outside_answers_for_is_rejected,
    test_answer_to_non_question_description_is_rejected,
    test_answer_for_unknown_id_is_rejected,
    # Translation
    test_translate_review_produces_review_entry,
    test_translate_answer_produces_answer_proposal,
    # Zip-misalignment regression
    test_review_candidates_paired_correctly_when_raw_reviews_are_dropped,
    # Auditability
    test_dropped_output_carries_reason_and_raw_record,
]


def main() -> int:
    passed = 0
    failed = 0
    for test in TESTS:
        try:
            test()
        except AssertionError as e:
            print(f"FAIL  {test.__name__}")
            print(f"      {e}")
            failed += 1
            continue
        except Exception:
            print(f"ERROR {test.__name__}")
            traceback.print_exc()
            failed += 1
            continue
        print(f"ok    {test.__name__}")
        passed += 1

    print()
    print(f"{passed} passed, {failed} failed, {len(TESTS)} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
