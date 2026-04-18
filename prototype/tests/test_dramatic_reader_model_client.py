"""
test_dramatic_reader_model_client.py — tests for the cross-boundary
LLM client.

Same shape as test_reader_model_client.py: synthetic Pydantic outputs
run through the classify/translate pipeline without hitting the API.
Covers scope enforcement on annotation reviews and verifier
commentaries, the synthetic-id map for verifier reviews, and the
pairing-on-drop invariant.

Run:
    .venv/bin/python3 -m tests.test_dramatic_reader_model_client
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.lowering import (
    Annotation, AnnotationReview, CrossDialectRef, Lowering, LoweringStatus,
    cross_ref,
)
from story_engine.core.verification import (
    StructuralAdvisory, VerificationReview, VerifierCommentary,
    SEVERITY_NOTED, VERDICT_APPROVED as V_APPROVED,
    VERDICT_PARTIAL_MATCH,
)
from story_engine.core.dramatic_reader_model_client import (
    DramaticReaderAnnotationReview,
    DramaticReaderOutput,
    DramaticReaderVerifierCommentary,
    DroppedOutput,
    _build_template_section,
    _build_verifier_section,
    _classify_annotation_review,
    _classify_verifier_commentary,
    _extract_review_ids,
    _translate_annotation_review,
    _translate_verifier_commentary,
    build_user_prompt,
)


# ============================================================================
# Fixtures
# ============================================================================


def _make_lowerings() -> tuple:
    """Three Lowerings: two ACTIVE, one PENDING."""
    return (
        Lowering(
            id="L_alpha",
            upper_record=cross_ref("dramatic", "C_alpha"),
            lower_records=(cross_ref("substrate", "alpha"),),
            annotation=Annotation(text="C_alpha → alpha entity"),
            τ_a=100,
            anchor_τ_a=10,
        ),
        Lowering(
            id="L_beta",
            upper_record=cross_ref("dramatic", "C_beta"),
            lower_records=(cross_ref("substrate", "beta"),),
            annotation=Annotation(text="C_beta → beta entity"),
            τ_a=101,
            anchor_τ_a=11,
        ),
        Lowering(
            id="L_pending",
            upper_record=cross_ref("dramatic", "C_pending"),
            lower_records=(),
            annotation=Annotation(text="not yet realized"),
            τ_a=102,
            status=LoweringStatus.PENDING,
        ),
    )


def _make_verifier_results() -> tuple:
    """Two VerificationReviews + one StructuralAdvisory, in that
    order. Used to exercise the synthetic-id assignment."""
    review_a = VerificationReview(
        reviewer_id="verifier:characterization",
        reviewed_at_τ_a=200,
        verdict=V_APPROVED,
        anchor_τ_a=10,
        target_record=cross_ref("dramatic", "T_one"),
        comment="solid",
        match_strength=1.0,
    )
    review_b = VerificationReview(
        reviewer_id="verifier:claim-trajectory",
        reviewed_at_τ_a=200,
        verdict=VERDICT_PARTIAL_MATCH,
        anchor_τ_a=12,
        target_record=cross_ref("dramatic", "A_two"),
        comment="2/3 signatures present",
        match_strength=0.67,
    )
    advisory = StructuralAdvisory(
        advisor_id="verifier:characterization",
        advised_at_τ_a=200,
        severity=SEVERITY_NOTED,
        comment="upper has no ACTIVE Lowerings; check skipped",
        scope=(cross_ref("dramatic", "T_three"),),
    )
    return (review_a, advisory, review_b)


# ============================================================================
# Annotation-review scope enforcement (R5)
# ============================================================================


def test_annotation_review_in_scope_is_accepted():
    """A review targeting a Lowering in lowerings_to_review and
    resolvable in the collection is accepted."""
    lowerings = _make_lowerings()
    raw = DramaticReaderAnnotationReview(
        lowering_id="L_alpha", verdict="approved",
        rationale="annotation matches the binding",
    )
    reason = _classify_annotation_review(
        raw, lowerings, lowerings_to_review=["L_alpha"],
    )
    assert reason is None, f"expected accepted; got drop: {reason}"


def test_annotation_review_outside_scope_is_rejected():
    """R5: in-collection but out-of-scope drops at ingest."""
    lowerings = _make_lowerings()
    raw = DramaticReaderAnnotationReview(
        lowering_id="L_beta", verdict="approved", rationale="ok",
    )
    reason = _classify_annotation_review(
        raw, lowerings, lowerings_to_review=["L_alpha"],
    )
    assert reason is not None
    assert "lowerings_to_review" in reason


def test_annotation_review_for_unknown_lowering_is_rejected():
    """If the id doesn't resolve, drop even when nominally in scope."""
    lowerings = _make_lowerings()
    raw = DramaticReaderAnnotationReview(
        lowering_id="L_ghost", verdict="approved", rationale="nope",
    )
    reason = _classify_annotation_review(
        raw, lowerings, lowerings_to_review=["L_ghost"],
    )
    assert reason is not None
    assert "does not resolve" in reason


# ============================================================================
# Annotation-review translation
# ============================================================================


def test_translate_annotation_review_produces_annotation_review_record():
    """One accepted DramaticReaderAnnotationReview → one
    AnnotationReview with reviewer_id, anchor_τ_a from the
    Lowering's τ_a (snapshot of the binding at review time),
    verdict, and comment-from-rationale."""
    lowerings = _make_lowerings()
    raw = DramaticReaderAnnotationReview(
        lowering_id="L_alpha", verdict="needs-work",
        rationale="annotation overstates the lower side",
    )
    review = _translate_annotation_review(
        raw, lowerings, reviewer_id="llm:test", current_τ_a=500,
    )
    assert isinstance(review, AnnotationReview)
    assert review.reviewer_id == "llm:test"
    assert review.reviewed_at_τ_a == 500
    assert review.verdict == "needs-work"
    assert review.anchor_τ_a == 100, (
        f"anchor_τ_a should snapshot L_alpha.τ_a=100; got "
        f"{review.anchor_τ_a}"
    )
    assert review.comment == "annotation overstates the lower side"


def test_translate_annotation_review_works_on_pending_lowering():
    """Pending Lowerings are reviewable too — the LLM is asked to
    judge whether the annotation correctly identifies what would
    need to exist for the binding to flip ACTIVE."""
    lowerings = _make_lowerings()
    raw = DramaticReaderAnnotationReview(
        lowering_id="L_pending", verdict="approved",
        rationale="annotation correctly names the missing substrate",
    )
    review = _translate_annotation_review(
        raw, lowerings, reviewer_id="llm:test", current_τ_a=500,
    )
    assert review.anchor_τ_a == 102


# ============================================================================
# Verifier-commentary scope enforcement
# ============================================================================


def test_verifier_commentary_in_scope_is_accepted():
    """A commentary targeting a synthetic id in
    reviews_to_comment_on AND resolvable in the id_map is accepted."""
    results = _make_verifier_results()
    _, id_map = _build_verifier_section(results)
    raw = DramaticReaderVerifierCommentary(
        target_review_id="vr_0", assessment="endorses",
        rationale="check is well-grounded against the records",
    )
    reason = _classify_verifier_commentary(
        raw, id_map, reviews_to_comment_on=["vr_0"],
    )
    assert reason is None, f"expected accepted; got drop: {reason}"


def test_verifier_commentary_outside_scope_is_rejected():
    """R5: in-id-map but out-of-scope drops."""
    results = _make_verifier_results()
    _, id_map = _build_verifier_section(results)
    raw = DramaticReaderVerifierCommentary(
        target_review_id="vr_1", assessment="endorses",
        rationale="ok",
    )
    reason = _classify_verifier_commentary(
        raw, id_map, reviews_to_comment_on=["vr_0"],
    )
    assert reason is not None
    assert "reviews_to_comment_on" in reason


def test_verifier_commentary_for_unknown_id_is_rejected():
    """An id that doesn't resolve in id_map drops even when in
    scope. Distinct from out-of-scope: a future id_map mismatch
    (caller invents an id, etc.) lands here."""
    results = _make_verifier_results()
    _, id_map = _build_verifier_section(results)
    raw = DramaticReaderVerifierCommentary(
        target_review_id="vr_99", assessment="endorses",
        rationale="ghost",
    )
    reason = _classify_verifier_commentary(
        raw, id_map, reviews_to_comment_on=["vr_99"],
    )
    assert reason is not None
    assert "does not resolve" in reason


# ============================================================================
# Verifier-commentary translation
# ============================================================================


def test_translate_verifier_commentary_resolves_target_review():
    """An accepted commentary → VerifierCommentary carrying the
    *resolved* VerificationReview object as `target_review`."""
    results = _make_verifier_results()
    _, id_map = _build_verifier_section(results)
    raw = DramaticReaderVerifierCommentary(
        target_review_id="vr_1",  # the second VerificationReview
        assessment="dissents",
        rationale="the partial-match here is actually approval-worthy "
                  "because the missing signature is structurally absent",
        suggested_signature="check whether the missing signature is "
                            "even authorable on this encoding",
    )
    commentary = _translate_verifier_commentary(
        raw, id_map, commenter_id="llm:test", current_τ_a=500,
    )
    assert isinstance(commentary, VerifierCommentary)
    assert commentary.commenter_id == "llm:test"
    assert commentary.commented_at_τ_a == 500
    assert commentary.assessment == "dissents"
    # target_review should be the actual VerificationReview object,
    # not a copy and not just the id.
    assert isinstance(commentary.target_review, VerificationReview)
    assert commentary.target_review.target_record.record_id == "A_two"
    assert commentary.target_review.match_strength == 0.67
    assert commentary.suggested_signature is not None
    assert "structurally absent" in commentary.comment


def test_translate_verifier_commentary_omits_suggested_signature():
    """suggested_signature is optional; an omitted field stays None
    on the VerifierCommentary."""
    results = _make_verifier_results()
    _, id_map = _build_verifier_section(results)
    raw = DramaticReaderVerifierCommentary(
        target_review_id="vr_0", assessment="endorses",
        rationale="solid",
    )
    commentary = _translate_verifier_commentary(
        raw, id_map, commenter_id="llm:test", current_τ_a=500,
    )
    assert commentary.suggested_signature is None


# ============================================================================
# Synthetic-id map invariants
# ============================================================================


def test_extract_review_ids_skips_advisories():
    """Only VerificationReviews get synthetic ids; advisories are
    context-only in this iteration."""
    results = _make_verifier_results()
    ids = _extract_review_ids(results)
    assert ids == ["vr_0", "vr_1"], (
        f"expected two ids skipping the advisory; got {ids!r}"
    )


def test_id_map_assignment_order_matches_input_order():
    """vr_0 is the first VerificationReview encountered in input
    order (regardless of intervening StructuralAdvisories)."""
    results = _make_verifier_results()
    _, id_map = _build_verifier_section(results)
    # results[0] is the first VR; results[1] is an advisory; results[2]
    # is the second VR. So vr_0 → results[0], vr_1 → results[2].
    assert id_map["vr_0"] is results[0]
    assert id_map["vr_1"] is results[2]


def test_id_map_is_empty_when_no_verification_reviews_present():
    """All-advisories input produces no ids."""
    advisory = StructuralAdvisory(
        advisor_id="verifier:claim-moment",
        advised_at_τ_a=200,
        severity=SEVERITY_NOTED,
        comment="no ACTIVE Lowerings; skipped",
        scope=(cross_ref("dramatic", "S_one"),),
    )
    _, id_map = _build_verifier_section((advisory,))
    assert id_map == {}


# ============================================================================
# Pairing-on-drop (the issue the substrate-side client also handles)
# ============================================================================


def test_review_candidates_paired_correctly_when_some_drop():
    """If three raw reviews come in and the middle one is out of
    scope, the surviving pairs must still carry the right
    (lowering_id, AnnotationReview) — no off-by-one from filtering."""
    lowerings = _make_lowerings()
    raws = [
        DramaticReaderAnnotationReview(
            lowering_id="L_alpha", verdict="approved",
            rationale="alpha rationale",
        ),
        DramaticReaderAnnotationReview(
            lowering_id="L_beta", verdict="approved",
            rationale="beta rationale (will drop: out of scope)",
        ),
        DramaticReaderAnnotationReview(
            lowering_id="L_pending", verdict="noted",
            rationale="pending rationale",
        ),
    ]
    in_scope = ["L_alpha", "L_pending"]
    candidates: list = []
    dropped: list = []
    for raw in raws:
        reason = _classify_annotation_review(raw, lowerings, in_scope)
        if reason is not None:
            dropped.append(DroppedOutput(reason=reason, raw=raw))
            continue
        review = _translate_annotation_review(
            raw, lowerings, reviewer_id="llm:test", current_τ_a=500,
        )
        candidates.append((raw.lowering_id, review))

    assert len(candidates) == 2
    assert len(dropped) == 1
    # Verify each surviving pair has the right id-to-rationale alignment.
    by_id = dict(candidates)
    assert by_id["L_alpha"].comment == "alpha rationale"
    assert by_id["L_pending"].comment == "pending rationale"
    # And the dropped raw is the L_beta one.
    assert dropped[0].raw.lowering_id == "L_beta"


# ============================================================================
# DroppedOutput shape
# ============================================================================


def test_dropped_output_carries_reason_and_raw_record():
    """An audit consumer should be able to read both the drop reason
    and the original raw object — the prompt told the LLM what was
    in scope, and a dropped record is exactly the trail to find
    where the LLM went off-script."""
    raw = DramaticReaderAnnotationReview(
        lowering_id="L_ghost", verdict="approved", rationale="ghost",
    )
    drop = DroppedOutput(reason="ghost id", raw=raw)
    assert drop.reason == "ghost id"
    assert drop.raw is raw
    assert hasattr(drop.raw, "model_dump")


# ============================================================================
# Template-section rendering (dramatica-complete extension)
# ============================================================================


def test_template_section_is_none_when_all_empty():
    """All-empty Template inputs produce no Template section. Preserves
    the Dramatic-only prompt shape — callers who don't pass Template
    records see no extra section rendered."""
    result = _build_template_section(
        domain_assignments=(),
        dynamic_story_points=(),
        signposts=(),
        thematic_picks=(),
        character_element_assignments=(),
        methodology_element_assignments=(),
        evaluation_element_assignments=(),
        purpose_element_assignments=(),
        story_goal=None,
        story_consequence=None,
    )
    assert result is None


def test_template_section_renders_story_level_keys():
    """Story_goal / Story_consequence render under the keys the
    verifier uses — record_ids `Story_goal` / `Story_consequence` —
    so a reader comparing a VerificationReview's target_record to
    the Template surface can find the matching entry."""
    result = _build_template_section(
        domain_assignments=(),
        dynamic_story_points=(),
        signposts=(),
        thematic_picks=(),
        character_element_assignments=(),
        methodology_element_assignments=(),
        evaluation_element_assignments=(),
        purpose_element_assignments=(),
        story_goal="stage a clean stunt",
        story_consequence="stunt contaminated",
    )
    assert result is not None
    import json as _json
    parsed = _json.loads(result)
    assert "story_level_fields" in parsed
    assert parsed["story_level_fields"]["Story_goal"] == "stage a clean stunt"
    assert (
        parsed["story_level_fields"]["Story_consequence"]
        == "stunt contaminated"
    )


def test_template_section_renders_domain_assignment_with_enum_value():
    """Enum fields serialize by value so the LLM sees the canonical
    label ('activity', 'situation') rather than a Python enum repr."""
    from story_engine.core.dramatica_template import DomainAssignment, Domain
    da = DomainAssignment(
        id="DA_mc", throughline_id="T_mc", domain=Domain.ACTIVITY,
    )
    result = _build_template_section(
        domain_assignments=(da,),
        dynamic_story_points=(),
        signposts=(),
        thematic_picks=(),
        character_element_assignments=(),
        methodology_element_assignments=(),
        evaluation_element_assignments=(),
        purpose_element_assignments=(),
        story_goal=None,
        story_consequence=None,
    )
    import json as _json
    parsed = _json.loads(result)
    assert parsed["domain_assignments"][0]["domain"] == "activity"
    assert parsed["domain_assignments"][0]["id"] == "DA_mc"


def test_build_user_prompt_omits_template_section_without_records():
    """A Dramatic-only invocation (no Template kwargs) produces a
    prompt with no Template records section. Back-compat guarantee
    for callers that haven't adopted the Template extension."""
    prompt, _ = build_user_prompt(
        arguments=(), throughlines=(), characters=(),
        scenes=(), beats=(), stakes=(),
        lowerings=_make_lowerings(),
        verifier_results=_make_verifier_results(),
        substrate_events=[], substrate_entities=[],
        lowerings_to_review=[], reviews_to_comment_on=[],
    )
    assert "## Template records" not in prompt


def test_build_user_prompt_includes_template_section_with_records():
    """When Template kwargs are populated, the Template-records
    section renders between the Dramatic section and the Lowerings
    section — so the LLM reads Template records alongside the
    underlying Dramatic records the verifier targets."""
    from story_engine.core.dramatica_template import DomainAssignment, Domain
    da = DomainAssignment(
        id="DA_mc", throughline_id="T_one", domain=Domain.ACTIVITY,
    )
    prompt, _ = build_user_prompt(
        arguments=(), throughlines=(), characters=(),
        scenes=(), beats=(), stakes=(),
        lowerings=_make_lowerings(),
        verifier_results=_make_verifier_results(),
        substrate_events=[], substrate_entities=[],
        lowerings_to_review=[], reviews_to_comment_on=[],
        domain_assignments=(da,),
    )
    assert "## Template records (dramatica-complete)" in prompt
    # Section ordering: Dramatic before Template before Lowerings.
    dramatic_pos = prompt.index("## Dramatic records")
    template_pos = prompt.index("## Template records")
    lowerings_pos = prompt.index("## Lowerings")
    assert dramatic_pos < template_pos < lowerings_pos


def test_template_section_with_only_story_goal_omits_empty_lists():
    """Empty Template collections don't produce empty-list keys in
    the rendered JSON — the payload only contains populated
    sub-sections. Keeps the prompt tight when the caller only has
    a partial Template surface to show."""
    result = _build_template_section(
        domain_assignments=(),
        dynamic_story_points=(),
        signposts=(),
        thematic_picks=(),
        character_element_assignments=(),
        methodology_element_assignments=(),
        evaluation_element_assignments=(),
        purpose_element_assignments=(),
        story_goal="the goal",
        story_consequence=None,
    )
    import json as _json
    parsed = _json.loads(result)
    assert "domain_assignments" not in parsed
    assert "dynamic_story_points" not in parsed
    assert "signposts" not in parsed
    assert "story_level_fields" in parsed
    assert "Story_goal" in parsed["story_level_fields"]
    assert "Story_consequence" not in parsed["story_level_fields"]


# ============================================================================
# Test runner
# ============================================================================


def main() -> int:
    tests = [
        (name, fn) for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    ]
    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
        except Exception:
            failed += 1
            print(f"FAIL  {name}")
            traceback.print_exc()
        else:
            passed += 1
            print(f"ok    {name}")
    print()
    print(f"{passed} passed, {failed} failed, {passed + failed} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
