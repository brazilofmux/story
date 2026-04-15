"""
test_verification.py — permanent tests for verification.py and the
Oedipus characterization run.

Synthetic-fixture tests pin the verifier primitive's behavior:
- verify_characterization with check returning various verdicts
- match_strength carried through
- skipped checks (no ACTIVE Lowerings) return None
- run_characterization_checks orchestration produces both
  Reviews (when checks ran) and Advisories (when they were skipped)
- defensive verdict-validation falls back to 'noted'

Integration test against oedipus_verification.run() pins the
contract that the main-character check produces APPROVED with
strength=1.0 on this encoding.

Run:  python3 test_verification.py
"""

from __future__ import annotations

import sys
import traceback

from lowering import (
    cross_ref, Annotation, Lowering, LoweringStatus,
)
from verification import (
    VerificationReview, StructuralAdvisory, VerificationAnswerProposal,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH, VERDICT_NOTED,
    SEVERITY_NOTED,
    verify_characterization, run_characterization_checks,
    reviews_only, advisories_only, group_by_verdict,
)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


def _lowering(
    upper_id: str = "U1",
    upper_dialect: str = "dramatic",
    lower_id: str = "L1",
    lower_dialect: str = "substrate",
    **overrides,
) -> Lowering:
    base = dict(
        id=f"L_{upper_id}_to_{lower_id}",
        upper_record=cross_ref(upper_dialect, upper_id),
        lower_records=(cross_ref(lower_dialect, lower_id),),
        annotation=Annotation(text="binding"),
        τ_a=100,
        anchor_τ_a=10,
    )
    base.update(overrides)
    return Lowering(**base)


# ----------------------------------------------------------------------------
# verify_characterization basics
# ----------------------------------------------------------------------------


def test_check_with_approved_verdict_produces_review():
    lw = _lowering()

    def check(upper_ref, lower_refs):
        return (VERDICT_APPROVED, 1.0, "all matched")

    review = verify_characterization(
        upper_record_id="U1", upper_dialect="dramatic",
        lowerings=(lw,), check=check,
        reviewed_at_τ_a=200,
    )
    assert review is not None
    assert review.verdict == VERDICT_APPROVED
    assert review.match_strength == 1.0
    assert review.target_record == cross_ref("dramatic", "U1")
    assert review.comment == "all matched"
    assert review.anchor_τ_a == 10  # carried from the Lowering


def test_check_with_partial_match_carries_strength():
    lw = _lowering()

    def check(upper_ref, lower_refs):
        return (VERDICT_PARTIAL_MATCH, 0.7, "70% match")

    review = verify_characterization(
        upper_record_id="U1", upper_dialect="dramatic",
        lowerings=(lw,), check=check,
    )
    assert review.verdict == VERDICT_PARTIAL_MATCH
    assert review.match_strength == 0.7


def test_check_returning_unknown_verdict_falls_back_to_noted():
    """A defensive: if a check returns a non-standard verdict
    string, the verifier records it as 'noted' rather than dropping
    or crashing."""
    lw = _lowering()

    def check(upper_ref, lower_refs):
        return ("garbage-verdict", 0.5, "what?")

    review = verify_characterization(
        upper_record_id="U1", upper_dialect="dramatic",
        lowerings=(lw,), check=check,
    )
    assert review.verdict == VERDICT_NOTED
    assert "garbage-verdict" in review.comment


def test_no_active_lowerings_returns_none():
    """If the upper has no ACTIVE Lowerings, the verifier returns
    None (the orchestrator surfaces it as a StructuralAdvisory)."""
    pending = Lowering(
        id="L_pending",
        upper_record=cross_ref("dramatic", "U1"),
        lower_records=(),
        annotation=Annotation(text=""),
        τ_a=0,
        status=LoweringStatus.PENDING,
    )

    def check(upper_ref, lower_refs):
        # Should not be called.
        raise AssertionError("check should not run when no ACTIVE Lowerings")

    review = verify_characterization(
        upper_record_id="U1", upper_dialect="dramatic",
        lowerings=(pending,), check=check,
    )
    assert review is None


def test_check_receives_union_of_lower_records_across_lowerings():
    """If an upper has multiple ACTIVE Lowerings, the check
    receives the union of their lower_records."""
    lw1 = _lowering(upper_id="U1", lower_id="A")
    lw2 = Lowering(
        id="L_extra",
        upper_record=cross_ref("dramatic", "U1"),
        lower_records=(cross_ref("substrate", "B"), cross_ref("substrate", "C")),
        annotation=Annotation(text=""),
        τ_a=100,
    )

    received = []
    def check(upper_ref, lower_refs):
        received.append(lower_refs)
        return (VERDICT_APPROVED, 1.0, "")

    verify_characterization(
        upper_record_id="U1", upper_dialect="dramatic",
        lowerings=(lw1, lw2), check=check,
    )
    assert len(received) == 1
    assert len(received[0]) == 3  # A + B + C


def test_pending_lowerings_not_passed_to_check():
    """ACTIVE-only filter: PENDING Lowerings should be ignored even
    if the upper record is the same."""
    active = _lowering(upper_id="U1", lower_id="A")
    pending = Lowering(
        id="L_pending",
        upper_record=cross_ref("dramatic", "U1"),
        lower_records=(),
        annotation=Annotation(text=""),
        τ_a=100,
        status=LoweringStatus.PENDING,
    )

    received = []
    def check(upper_ref, lower_refs):
        received.append(lower_refs)
        return (VERDICT_APPROVED, 1.0, "")

    verify_characterization(
        upper_record_id="U1", upper_dialect="dramatic",
        lowerings=(active, pending), check=check,
    )
    # Only the ACTIVE Lowering's lower_records should be visible.
    assert received == [(cross_ref("substrate", "A"),)]


# ----------------------------------------------------------------------------
# run_characterization_checks orchestration
# ----------------------------------------------------------------------------


def test_orchestrator_returns_reviews_for_checks_that_ran():
    lw = _lowering(upper_id="U1")

    def check(upper_ref, lower_refs):
        return (VERDICT_APPROVED, 1.0, "ok")

    results = run_characterization_checks(
        checks=(("U1", "dramatic", check),),
        lowerings=(lw,),
    )
    assert len(results) == 1
    assert isinstance(results[0], VerificationReview)


def test_orchestrator_returns_advisories_for_skipped_checks():
    """When the upper has no ACTIVE Lowerings, the orchestrator
    produces a StructuralAdvisory naming the gap rather than
    silently returning nothing."""
    def check(upper_ref, lower_refs):
        raise AssertionError("should not run")

    results = run_characterization_checks(
        checks=(("U_no_lowering", "dramatic", check),),
        lowerings=(),
    )
    assert len(results) == 1
    assert isinstance(results[0], StructuralAdvisory)
    assert "no ACTIVE Lowerings" in results[0].comment


def test_orchestrator_runs_multiple_checks():
    lw1 = _lowering(upper_id="U1")
    lw2 = _lowering(upper_id="U2", lower_id="X")

    def check_a(upper_ref, lower_refs):
        return (VERDICT_APPROVED, 1.0, "ok")
    def check_b(upper_ref, lower_refs):
        return (VERDICT_PARTIAL_MATCH, 0.6, "partial")

    results = run_characterization_checks(
        checks=(
            ("U1", "dramatic", check_a),
            ("U2", "dramatic", check_b),
        ),
        lowerings=(lw1, lw2),
    )
    assert len(results) == 2
    reviews = reviews_only(results)
    assert len(reviews) == 2
    verdicts = {r.verdict for r in reviews}
    assert verdicts == {VERDICT_APPROVED, VERDICT_PARTIAL_MATCH}


# ----------------------------------------------------------------------------
# Filtering helpers
# ----------------------------------------------------------------------------


def test_reviews_only_filters_correctly():
    review = VerificationReview(
        reviewer_id="x", reviewed_at_τ_a=0, verdict=VERDICT_APPROVED,
        anchor_τ_a=0, target_record=cross_ref("dramatic", "U1"),
    )
    advisory = StructuralAdvisory(
        advisor_id="x", advised_at_τ_a=0, severity=SEVERITY_NOTED,
        comment="x", scope=(),
    )
    out = reviews_only((review, advisory))
    assert out == (review,)


def test_advisories_only_filters_correctly():
    review = VerificationReview(
        reviewer_id="x", reviewed_at_τ_a=0, verdict=VERDICT_APPROVED,
        anchor_τ_a=0, target_record=cross_ref("dramatic", "U1"),
    )
    advisory = StructuralAdvisory(
        advisor_id="x", advised_at_τ_a=0, severity=SEVERITY_NOTED,
        comment="x", scope=(),
    )
    out = advisories_only((review, advisory))
    assert out == (advisory,)


def test_group_by_verdict_buckets_correctly():
    a = VerificationReview(
        reviewer_id="x", reviewed_at_τ_a=0, verdict=VERDICT_APPROVED,
        anchor_τ_a=0, target_record=cross_ref("dramatic", "U1"),
    )
    b = VerificationReview(
        reviewer_id="x", reviewed_at_τ_a=0, verdict=VERDICT_NEEDS_WORK,
        anchor_τ_a=0, target_record=cross_ref("dramatic", "U2"),
    )
    g = group_by_verdict((a, b))
    assert len(g[VERDICT_APPROVED]) == 1
    assert len(g[VERDICT_NEEDS_WORK]) == 1


# ----------------------------------------------------------------------------
# Coupling-kind declarations (V5 amendment to dramatic.py)
# ----------------------------------------------------------------------------


def test_coupling_kind_for_field_lookup():
    from dramatic import coupling_kind_for
    assert coupling_kind_for("Argument", "resolution_direction") == "claim-trajectory"
    assert coupling_kind_for("Argument", "domain") == "flavor"
    assert coupling_kind_for("Throughline", "role_label") == "characterization"
    assert coupling_kind_for("Throughline", "owners") == "realization"
    assert coupling_kind_for("Scene", "result") == "claim-moment"


def test_coupling_kind_for_whole_record_lookup():
    from dramatic import coupling_kind_for
    assert coupling_kind_for("Character") == "realization"
    assert coupling_kind_for("Story") == "realization"


def test_coupling_kind_for_unknown_field_returns_record_level():
    """If a record has a record-level (field=None) declaration but
    no specific-field declaration for the queried field, the lookup
    falls back to the record-level kind."""
    from dramatic import coupling_kind_for
    # Character has only a record-level declaration; asking about a
    # specific field should return the record-level kind.
    assert coupling_kind_for("Character", "name") == "realization"


def test_coupling_kind_for_unknown_record_returns_none():
    from dramatic import coupling_kind_for
    assert coupling_kind_for("NotARecord", "field") is None
    assert coupling_kind_for("NotARecord") is None


def test_declarations_for_kind_returns_only_matching():
    from dramatic import declarations_for_kind
    char_decls = declarations_for_kind("characterization")
    assert all(d.kind == "characterization" for d in char_decls)
    # Throughline.role_label and .subject are the two
    # characterization declarations.
    fields = {d.field for d in char_decls}
    assert "role_label" in fields
    assert "subject" in fields


def test_fields_with_coupling_for_argument():
    from dramatic import fields_with_coupling
    flavor_fields = fields_with_coupling("Argument", "flavor")
    assert "domain" in flavor_fields
    assert "counter_premise" in flavor_fields


# ----------------------------------------------------------------------------
# Integration — Oedipus characterization
# ----------------------------------------------------------------------------


def test_oedipus_verification_main_character_check_passes():
    """The main-character Throughline check on T_mc_oedipus should
    return APPROVED with match_strength=1.0: all 10 events on the
    L_mc_throughline binding have Oedipus as a participant."""
    import oedipus_verification as ov
    results = ov.run()
    assert len(results) == 1
    r = results[0]
    assert isinstance(r, VerificationReview)
    assert r.verdict == VERDICT_APPROVED
    assert r.match_strength == 1.0
    assert r.target_record == cross_ref("dramatic", "T_mc_oedipus")


def test_oedipus_verification_includes_owner_resolution_in_comment():
    """The comment should name the owner Character(s) and the
    resolved Entity(ies), so an author reading the verifier output
    can see which Lowering chain produced the verdict."""
    import oedipus_verification as ov
    results = ov.run()
    r = results[0]
    assert "C_oedipus" in r.comment
    assert "oedipus" in r.comment  # the resolved entity id
    assert "10/10" in r.comment  # the structural result


# ----------------------------------------------------------------------------
# Test runner
# ----------------------------------------------------------------------------


TESTS = [
    # verify_characterization basics
    test_check_with_approved_verdict_produces_review,
    test_check_with_partial_match_carries_strength,
    test_check_returning_unknown_verdict_falls_back_to_noted,
    test_no_active_lowerings_returns_none,
    test_check_receives_union_of_lower_records_across_lowerings,
    test_pending_lowerings_not_passed_to_check,
    # Orchestrator
    test_orchestrator_returns_reviews_for_checks_that_ran,
    test_orchestrator_returns_advisories_for_skipped_checks,
    test_orchestrator_runs_multiple_checks,
    # Filtering helpers
    test_reviews_only_filters_correctly,
    test_advisories_only_filters_correctly,
    test_group_by_verdict_buckets_correctly,
    # Coupling-kind declarations
    test_coupling_kind_for_field_lookup,
    test_coupling_kind_for_whole_record_lookup,
    test_coupling_kind_for_unknown_field_returns_record_level,
    test_coupling_kind_for_unknown_record_returns_none,
    test_declarations_for_kind_returns_only_matching,
    test_fields_with_coupling_for_argument,
    # Integration — Oedipus
    test_oedipus_verification_main_character_check_passes,
    test_oedipus_verification_includes_owner_resolution_in_comment,
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
