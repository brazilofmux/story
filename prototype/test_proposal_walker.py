"""
test_proposal_walker.py — tests for the interactive proposal walker.

The walker is tooling (not substrate) but it orchestrates substrate
state transitions on the author's behalf. These tests drive it with
`io.StringIO` streams — no terminal required — and pin:

- Accept-review flow produces a new description with the review
  appended; original is untouched.
- Decline / skip leave state unchanged.
- Quit terminates the walk.
- Accept-answer flow commits a new description and flips the queue
  entry's status.
- Decline-answer flow flips status without touching descriptions.
- Unknown input re-prompts; EOF is treated as quit.
- Empty inputs produce empty outputs gracefully.

Run:
    .venv/bin/python3 test_proposal_walker.py
"""

from __future__ import annotations

import io
import sys
import traceback

from substrate import (
    AnswerProposal,
    Attention,
    Description,
    DescStatus,
    ReviewEntry,
    ReviewVerdict,
    anchor_event,
    ingest_question_answer,
)
from proposal_walker import (
    Decision,
    walk_answer_proposals,
    walk_reviews,
    summarize_decisions,
)


# ============================================================================
# Fixtures
# ============================================================================


def _make_description(id: str, text: str = "sample text",
                      is_question: bool = False) -> Description:
    return Description(
        id=id,
        attached_to=anchor_event("E_main"),
        kind="texture",
        attention=Attention.INTERPRETIVE,
        text=text,
        authored_by="author",
        τ_a=10,
        is_question=is_question,
    )


def _make_review(reviewer: str = "llm:test",
                 verdict: ReviewVerdict = ReviewVerdict.APPROVED) -> ReviewEntry:
    return ReviewEntry(
        reviewer_id=reviewer,
        reviewed_at_τ_a=100,
        verdict=verdict,
        anchor_τ_a=10,
        comment="test comment",
    )


def _make_answer_proposal(question_id: str, new_id: str) -> AnswerProposal:
    question = _make_description(question_id, is_question=True)
    proposed = Description(
        id=new_id,
        attached_to=question.attached_to,
        kind="reader-frame",
        attention=Attention.INTERPRETIVE,
        text="proposed answer body",
        authored_by="llm:test",
        τ_a=200,
        status=DescStatus.PROVISIONAL,
        metadata={"answers_question": question_id},
    )
    return AnswerProposal(
        question_description_id=question_id,
        proposed_description=proposed,
        proposer_id="llm:test",
        rationale="test rationale",
        proposed_at_τ_a=200,
    )


# ============================================================================
# walk_reviews
# ============================================================================


def test_walk_reviews_empty_is_noop():
    """No candidates → no decisions, descriptions unchanged, walker
    does not prompt."""
    descs = [_make_description("D_alpha")]
    stdin = io.StringIO("")  # should not be consumed
    stdout = io.StringIO()
    new_descs, decisions = walk_reviews(
        [], descs, stdin=stdin, stdout=stdout,
    )
    assert new_descs == descs, "descriptions mutated on empty walk"
    assert decisions == [], f"unexpected decisions: {decisions}"
    assert "no reviews" in stdout.getvalue()


def test_walk_reviews_accept_appends_review_to_description():
    """Typing 'a' at the prompt invokes ingest_review: the description's
    review_states grows by one; the original is preserved."""
    d = _make_description("D_alpha")
    review = _make_review()
    stdin = io.StringIO("a\n")
    stdout = io.StringIO()
    new_descs, decisions = walk_reviews(
        [("D_alpha", review)], [d], stdin=stdin, stdout=stdout,
    )
    assert len(new_descs) == 1
    updated = new_descs[0]
    assert updated.id == "D_alpha"
    assert len(updated.review_states) == 1
    assert updated.review_states[0] == review
    # Original untouched.
    assert len(d.review_states) == 0
    # Decision recorded.
    assert decisions == [Decision("review", "D_alpha", "accept")]


def test_walk_reviews_decline_leaves_description_unchanged():
    """Typing 'd' produces a decision but no ingest_review call; the
    description's review_states is still empty."""
    d = _make_description("D_alpha")
    review = _make_review()
    stdin = io.StringIO("d\n")
    stdout = io.StringIO()
    new_descs, decisions = walk_reviews(
        [("D_alpha", review)], [d], stdin=stdin, stdout=stdout,
    )
    assert len(new_descs[0].review_states) == 0, \
        "declined review should not land on description"
    assert decisions == [Decision("review", "D_alpha", "decline")]


def test_walk_reviews_skip_leaves_description_unchanged():
    """Typing 's' produces a skip decision; no state changes."""
    d = _make_description("D_alpha")
    review = _make_review()
    stdin = io.StringIO("s\n")
    stdout = io.StringIO()
    new_descs, decisions = walk_reviews(
        [("D_alpha", review)], [d], stdin=stdin, stdout=stdout,
    )
    assert len(new_descs[0].review_states) == 0
    assert decisions == [Decision("review", "D_alpha", "skip")]


def test_walk_reviews_quit_stops_walk_mid_stream():
    """Typing 'q' on the second candidate stops the walk; the first
    decision is preserved, the remaining candidates are not shown."""
    d1, d2, d3 = [_make_description(f"D_{i}") for i in ("one", "two", "three")]
    r1, r2, r3 = _make_review(), _make_review(), _make_review()
    stdin = io.StringIO("a\nq\n")  # accept first, quit on second
    stdout = io.StringIO()
    new_descs, decisions = walk_reviews(
        [("D_one", r1), ("D_two", r2), ("D_three", r3)],
        [d1, d2, d3],
        stdin=stdin, stdout=stdout,
    )
    # First decision accepted; second is the quit sentinel; third never shown.
    kinds = [d.choice for d in decisions]
    assert kinds == ["accept", "quit"], f"unexpected decisions: {decisions}"
    # The first description has its review; the other two are untouched.
    by_id = {d.id: d for d in new_descs}
    assert len(by_id["D_one"].review_states) == 1
    assert len(by_id["D_two"].review_states) == 0
    assert len(by_id["D_three"].review_states) == 0


def test_walk_reviews_unknown_input_reprompts():
    """Junk input doesn't default — the walker re-prompts until a valid
    choice char arrives."""
    d = _make_description("D_alpha")
    review = _make_review()
    # Three lines: garbage, another garbage, then accept.
    stdin = io.StringIO("huh?\nnope\na\n")
    stdout = io.StringIO()
    new_descs, decisions = walk_reviews(
        [("D_alpha", review)], [d], stdin=stdin, stdout=stdout,
    )
    assert decisions == [Decision("review", "D_alpha", "accept")]
    out = stdout.getvalue()
    assert out.count("unrecognized input") == 2, (
        f"expected two unrecognized-input notices; got output:\n{out}"
    )


def test_walk_reviews_eof_treated_as_quit():
    """EOF on stdin before any input is a quit — the walker does not
    loop forever or mutate state."""
    d = _make_description("D_alpha")
    review = _make_review()
    stdin = io.StringIO("")  # immediate EOF
    stdout = io.StringIO()
    new_descs, decisions = walk_reviews(
        [("D_alpha", review)], [d], stdin=stdin, stdout=stdout,
    )
    assert len(new_descs[0].review_states) == 0
    assert decisions == [Decision("review", "D_alpha", "quit")]


def test_walk_reviews_missing_target_is_skipped():
    """If a review candidate names a target id not in descriptions,
    the walker records it as skipped rather than crashing."""
    d = _make_description("D_alpha")
    review = _make_review()
    stdin = io.StringIO("")  # should not be consumed
    stdout = io.StringIO()
    new_descs, decisions = walk_reviews(
        [("D_ghost", review)], [d], stdin=stdin, stdout=stdout,
    )
    assert decisions == [Decision("review", "D_ghost", "skip")]
    assert new_descs == [d], "descriptions list mutated on ghost target"


# ============================================================================
# walk_answer_proposals
# ============================================================================


def test_walk_answers_empty_queue_is_noop():
    descs = [_make_description("D_q", is_question=True)]
    stdin = io.StringIO("")
    stdout = io.StringIO()
    new_descs, new_queue, decisions = walk_answer_proposals(
        [], descs, stdin=stdin, stdout=stdout,
    )
    assert new_descs == descs
    assert new_queue == []
    assert decisions == []
    assert "no pending answer proposals" in stdout.getvalue()


def test_walk_answers_accept_commits_new_description():
    """Accept on a pending AnswerProposal: descriptions grows by one
    committed Description, queue entry flips to accepted."""
    q = _make_description("D_q", is_question=True)
    ap = _make_answer_proposal("D_q", "D_q_answer_1")
    queue = ingest_question_answer(ap, [])
    stdin = io.StringIO("a\n")
    stdout = io.StringIO()
    new_descs, new_queue, decisions = walk_answer_proposals(
        queue, [q], stdin=stdin, stdout=stdout,
    )
    assert len(new_descs) == 2
    committed = new_descs[-1]
    assert committed.id == "D_q_answer_1"
    assert committed.status == DescStatus.COMMITTED
    assert new_queue[0].status == "accepted"
    assert decisions == [Decision("answer-proposal", "D_q", "accept")]


def test_walk_answers_decline_flips_queue_status():
    """Decline flips status to declined without touching descriptions."""
    q = _make_description("D_q", is_question=True)
    ap = _make_answer_proposal("D_q", "D_q_answer_2")
    queue = ingest_question_answer(ap, [])
    stdin = io.StringIO("d\n")
    stdout = io.StringIO()
    new_descs, new_queue, decisions = walk_answer_proposals(
        queue, [q], stdin=stdin, stdout=stdout,
    )
    assert len(new_descs) == 1, "declined answer should not commit"
    assert new_queue[0].status == "declined"
    assert decisions == [Decision("answer-proposal", "D_q", "decline")]


def test_walk_answers_skip_leaves_pending():
    """Skip does not change status; the queue entry stays pending
    and can be walked again later."""
    q = _make_description("D_q", is_question=True)
    ap = _make_answer_proposal("D_q", "D_q_answer_3")
    queue = ingest_question_answer(ap, [])
    stdin = io.StringIO("s\n")
    stdout = io.StringIO()
    new_descs, new_queue, decisions = walk_answer_proposals(
        queue, [q], stdin=stdin, stdout=stdout,
    )
    assert len(new_descs) == 1
    assert new_queue[0].status == "pending"
    assert decisions == [Decision("answer-proposal", "D_q", "skip")]


def test_walk_answers_only_shows_pending_entries():
    """Queue entries that are already accepted or declined are ignored
    on subsequent walks — the walker only prompts on `pending`."""
    q = _make_description("D_q", is_question=True)
    ap1 = _make_answer_proposal("D_q", "D_q_answer_first")
    ap2 = _make_answer_proposal("D_q", "D_q_answer_second")
    # First walk: decline ap1.
    queue = ingest_question_answer(ap1, [])
    queue = ingest_question_answer(ap2, queue)
    # Mark ap1 declined by walking with a decline.
    stdin = io.StringIO("d\ns\n")  # decline ap1, skip ap2
    stdout = io.StringIO()
    _, queue_after_first, _ = walk_answer_proposals(
        queue, [q], stdin=stdin, stdout=stdout,
    )
    assert queue_after_first[0].status == "declined"
    assert queue_after_first[1].status == "pending"

    # Second walk: ap1 is already declined and must NOT be shown again.
    # Only ap2 is pending and should receive a single prompt.
    stdin2 = io.StringIO("a\n")
    stdout2 = io.StringIO()
    new_descs, queue_after_second, decisions = walk_answer_proposals(
        queue_after_first, [q], stdin=stdin2, stdout=stdout2,
    )
    # Only one prompt was issued (ap2).
    assert decisions == [
        Decision("answer-proposal", "D_q", "accept"),
    ], f"unexpected decisions on second walk: {decisions}"
    # ap1 is still declined; ap2 is now accepted.
    assert queue_after_second[0].status == "declined"
    assert queue_after_second[1].status == "accepted"


def test_walk_answers_quit_stops_walk():
    """Quit mid-walk preserves earlier decisions; later proposals stay
    pending."""
    q = _make_description("D_q", is_question=True)
    ap1 = _make_answer_proposal("D_q", "D_q_answer_a")
    ap2 = _make_answer_proposal("D_q", "D_q_answer_b")
    queue = ingest_question_answer(ap1, [])
    queue = ingest_question_answer(ap2, queue)
    stdin = io.StringIO("a\nq\n")  # accept first, quit on second
    stdout = io.StringIO()
    new_descs, new_queue, decisions = walk_answer_proposals(
        queue, [q], stdin=stdin, stdout=stdout,
    )
    kinds = [d.choice for d in decisions]
    assert kinds == ["accept", "quit"]
    assert new_queue[0].status == "accepted"
    assert new_queue[1].status == "pending", \
        "quit should not mutate the un-walked proposal"


def test_walk_answers_acts_on_correct_entry_with_duplicate_pending_proposals():
    """Regression for the equality-vs-identity bug in _match_queue_entry.
    If two pending AnswerProposal entries are structurally equal (same
    question, same proposed text, same τ_a), the walker must mutate
    the queue slot the author is currently reviewing — not the first
    equal entry it finds. Snapshot-index iteration + identity matching
    in the substrate API together pin this.
    """
    q = _make_description("D_q", is_question=True)
    # Two structurally-identical proposals. Frozen-dataclass equality
    # would collapse them; identity keeps them distinct queue slots.
    ap1 = _make_answer_proposal("D_q", "D_q_answer_dup")
    ap2 = _make_answer_proposal("D_q", "D_q_answer_dup")
    assert ap1 == ap2, "fixture precondition: proposals are equal"
    assert ap1 is not ap2, "fixture precondition: proposals are distinct"
    queue = ingest_question_answer(ap1, [])
    queue = ingest_question_answer(ap2, queue)

    # Skip the first, accept the second.
    stdin = io.StringIO("s\na\n")
    stdout = io.StringIO()
    new_descs, new_queue, decisions = walk_answer_proposals(
        queue, [q], stdin=stdin, stdout=stdout,
    )
    # The walker prompted twice (one skip, one accept).
    assert [d.choice for d in decisions] == ["skip", "accept"], decisions
    # The ACCEPT must have landed on index 1, not index 0. A buggy
    # equality-based _match_queue_entry would have mutated queue[0]
    # (the first structurally-equal entry) and left queue[1] pending.
    assert new_queue[0].status == "pending", (
        f"identity-match regression: expected queue[0] to remain "
        f"pending (skipped) but got {new_queue[0].status}"
    )
    assert new_queue[1].status == "accepted", (
        f"identity-match regression: expected queue[1] to be "
        f"accepted but got {new_queue[1].status}"
    )
    # Exactly one new committed description landed.
    assert len(new_descs) == 2


def test_walk_answers_ignores_non_answer_proposal_entries():
    """The queue may carry PromotionProposal entries too. The answer-
    walker must pass over them without prompting; they are out of
    scope for this walker."""
    from substrate import PromotionProposal

    q = _make_description("D_q", is_question=True)
    pp = PromotionProposal(
        description_id="D_other",
        proposed_fact=None,
        proposer_id="llm:test",
        rationale="something",
        proposed_at_τ_a=50,
    )
    ap = _make_answer_proposal("D_q", "D_q_answer_mixed")
    queue = [pp, ap]  # PromotionProposal first
    stdin = io.StringIO("a\n")  # one prompt expected, for ap
    stdout = io.StringIO()
    _, new_queue, decisions = walk_answer_proposals(
        queue, [q], stdin=stdin, stdout=stdout,
    )
    assert decisions == [Decision("answer-proposal", "D_q", "accept")]
    # PromotionProposal pass-through: unchanged.
    assert new_queue[0] == pp
    assert new_queue[1].status == "accepted"


# ============================================================================
# Summary helper
# ============================================================================


def test_summarize_decisions_groups_by_kind_and_choice():
    decisions = [
        Decision("review", "D_a", "accept"),
        Decision("review", "D_b", "accept"),
        Decision("review", "D_c", "decline"),
        Decision("answer-proposal", "D_q", "skip"),
    ]
    counts = summarize_decisions(decisions)
    assert counts[("review", "accept")] == 2
    assert counts[("review", "decline")] == 1
    assert counts[("answer-proposal", "skip")] == 1


# ============================================================================
# Runner
# ============================================================================


TESTS = [
    test_walk_reviews_empty_is_noop,
    test_walk_reviews_accept_appends_review_to_description,
    test_walk_reviews_decline_leaves_description_unchanged,
    test_walk_reviews_skip_leaves_description_unchanged,
    test_walk_reviews_quit_stops_walk_mid_stream,
    test_walk_reviews_unknown_input_reprompts,
    test_walk_reviews_eof_treated_as_quit,
    test_walk_reviews_missing_target_is_skipped,
    test_walk_answers_empty_queue_is_noop,
    test_walk_answers_accept_commits_new_description,
    test_walk_answers_decline_flips_queue_status,
    test_walk_answers_skip_leaves_pending,
    test_walk_answers_only_shows_pending_entries,
    test_walk_answers_quit_stops_walk,
    test_walk_answers_acts_on_correct_entry_with_duplicate_pending_proposals,
    test_walk_answers_ignores_non_answer_proposal_entries,
    test_summarize_decisions_groups_by_kind_and_choice,
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
