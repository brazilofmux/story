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
    verify_claim_trajectory, run_claim_trajectory_checks,
    verify_claim_moment, run_claim_moment_checks,
    CheckRegistration, orchestrate_checks,
    COUPLING_REALIZATION, COUPLING_CHARACTERIZATION,
    COUPLING_CLAIM_MOMENT, COUPLING_CLAIM_TRAJECTORY, COUPLING_FLAVOR,
    ORCHESTRATABLE_COUPLING_KINDS,
    CoverageGap, coverage_report,
    group_gaps_by_record, group_gaps_by_kind, group_gaps_by_record_type,
    reviews_only, advisories_only, group_by_verdict,
)
from lowering import PositionRange


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
    # Find the T_mc_oedipus characterization review specifically
    # (run() now produces multiple reviews from different primitives).
    mc_reviews = [
        r for r in results
        if isinstance(r, VerificationReview)
        and r.target_record == cross_ref("dramatic", "T_mc_oedipus")
    ]
    assert len(mc_reviews) == 1
    r = mc_reviews[0]
    assert r.verdict == VERDICT_APPROVED
    assert r.match_strength == 1.0
    assert r.target_record == cross_ref("dramatic", "T_mc_oedipus")


def test_oedipus_verification_includes_owner_resolution_in_comment():
    """The comment should name the owner Character(s) and the
    resolved Entity(ies), so an author reading the verifier output
    can see which Lowering chain produced the verdict."""
    import oedipus_verification as ov
    results = ov.run()
    mc_reviews = [
        r for r in results
        if isinstance(r, VerificationReview)
        and r.target_record == cross_ref("dramatic", "T_mc_oedipus")
    ]
    r = mc_reviews[0]
    assert "C_oedipus" in r.comment
    assert "oedipus" in r.comment  # the resolved entity id
    # "13/13" after the F5 substrate extension added
    # E_tiresias_accusation + E_self_blinding + E_exile to the MC
    # Throughline's lower_records. Was "10/10" pre-extension.
    assert "13/13" in r.comment


# ----------------------------------------------------------------------------
# Claim-trajectory primitive
# ----------------------------------------------------------------------------


def test_claim_trajectory_runs_even_with_no_lowerings():
    """Unlike Characterization, Claim-trajectory always runs the
    check; the check supplies its own scope from its closure. This
    is the F1 / F6 distinction realized in primitive shape — Claim
    is verified against the substrate, not against Lowerings."""
    received = []
    def check(upper_ref, lower_refs, position_ranges):
        received.append((lower_refs, position_ranges))
        return (VERDICT_APPROVED, 1.0, "ran without Lowerings")

    review = verify_claim_trajectory(
        upper_record_id="A_some_argument",
        upper_dialect="dramatic",
        lowerings=(),  # no Lowerings at all
        check=check,
    )
    assert review is not None  # verifier returns review, not None
    assert review.verdict == VERDICT_APPROVED
    assert received == [((), ())]  # check was called with empty args


def test_claim_trajectory_passes_position_ranges_when_present():
    """When ACTIVE Lowerings carry position_range, the primitive
    collects them and passes to the check."""
    pr = PositionRange(coord="τ_s", min_value=0, max_value=13)
    lw = _lowering(upper_id="A1", position_range=pr)

    received = []
    def check(upper_ref, lower_refs, position_ranges):
        received.append(position_ranges)
        return (VERDICT_APPROVED, 1.0, "")

    verify_claim_trajectory(
        upper_record_id="A1",
        upper_dialect="dramatic",
        lowerings=(lw,),
        check=check,
    )
    assert received == [(pr,)]


def test_claim_trajectory_handles_partial_match():
    """Partial-match verdict + match_strength carried through."""
    def check(upper_ref, lower_refs, position_ranges):
        return (VERDICT_PARTIAL_MATCH, 0.66, "two of three signatures")

    review = verify_claim_trajectory(
        upper_record_id="A1",
        upper_dialect="dramatic",
        lowerings=(),
        check=check,
    )
    assert review.verdict == VERDICT_PARTIAL_MATCH
    assert review.match_strength == 0.66


def test_claim_trajectory_unknown_verdict_falls_back_to_noted():
    def check(upper_ref, lower_refs, position_ranges):
        return ("garbage", 0.5, "what")

    review = verify_claim_trajectory(
        upper_record_id="A1",
        upper_dialect="dramatic",
        lowerings=(),
        check=check,
    )
    assert review.verdict == VERDICT_NOTED
    assert "garbage" in review.comment


def test_claim_trajectory_orchestrator_returns_one_review_per_check():
    """run_claim_trajectory_checks always produces a Review per check
    (no Advisories — there's nothing to skip)."""
    def ok(upper_ref, lower_refs, prs):
        return (VERDICT_APPROVED, 1.0, "")
    def partial(upper_ref, lower_refs, prs):
        return (VERDICT_PARTIAL_MATCH, 0.5, "")

    results = run_claim_trajectory_checks(
        checks=(
            ("A1", "dramatic", ok),
            ("A2", "dramatic", partial),
        ),
        lowerings=(),
    )
    assert len(results) == 2
    assert all(isinstance(r, VerificationReview) for r in results)
    verdicts = {r.verdict for r in results}
    assert verdicts == {VERDICT_APPROVED, VERDICT_PARTIAL_MATCH}


# ----------------------------------------------------------------------------
# Integration — Oedipus Argument trajectory check
# ----------------------------------------------------------------------------


def test_oedipus_argument_trajectory_check_passes():
    """A_knowledge_unmakes (resolution=AFFIRM) trajectory check
    should return APPROVED with match_strength=1.0: all three
    signatures (identity collapse, parricide derivable, incest
    derivable) present at τ_s ≤ 13."""
    import oedipus_verification as ov
    results = ov.run()
    # Find the Argument trajectory review.
    arg_reviews = [
        r for r in results
        if isinstance(r, VerificationReview)
        and r.target_record == cross_ref("dramatic", "A_knowledge_unmakes")
    ]
    assert len(arg_reviews) == 1
    r = arg_reviews[0]
    assert r.verdict == VERDICT_APPROVED
    assert r.match_strength == 1.0
    # The comment should name all three signatures.
    assert "identity collapse" in r.comment
    assert "parricide" in r.comment
    assert "incest" in r.comment
    assert "3/3" in r.comment


def test_oedipus_argument_trajectory_check_uses_inference_engine():
    """Per V6, the trajectory check composes with inference-01.
    parricide and incest are not literal world facts — they
    derive from PARRICIDE_RULE / INCEST_RULE on the substrate's
    authored premises. The check should return their derivability
    via world_holds_derived (not literal membership)."""
    # We verify this by inspecting the comment, which names whether
    # each derivation succeeded. If the inference engine were not
    # consulted, parricide_proof would be None (the predicates are
    # not authored as world facts since the inference-01 retirement).
    import oedipus_verification as ov
    results = ov.run()
    arg_review = next(
        r for r in results
        if isinstance(r, VerificationReview)
        and r.target_record == cross_ref("dramatic", "A_knowledge_unmakes")
    )
    assert "parricide(oedipus, laius) world-derivable: True" in arg_review.comment
    assert "incest(oedipus, jocasta) world-derivable: True" in arg_review.comment


def test_oedipus_run_produces_three_reviews():
    """The full Oedipus verifier run produces three
    VerificationReviews — one per V3 primitive: Characterization
    (T_mc_oedipus), Claim-trajectory (A_knowledge_unmakes),
    Claim-moment (S_anagnorisis). All APPROVED with strength=1.0
    in this encoding."""
    import oedipus_verification as ov
    results = ov.run()
    reviews = reviews_only(results)
    assert len(reviews) == 3
    assert all(r.verdict == VERDICT_APPROVED for r in reviews)
    assert all(r.match_strength == 1.0 for r in reviews)


# ----------------------------------------------------------------------------
# Claim-moment primitive
# ----------------------------------------------------------------------------


def test_claim_moment_runs_with_active_lowering():
    """Claim-moment requires ACTIVE Lowerings (the moment-pattern
    claim depends on knowing which lower records locate the moment).
    With at least one ACTIVE Lowering, the check runs."""
    lw = _lowering(upper_id="S1")
    received = []
    def check(upper_ref, lower_refs, position_ranges):
        received.append((lower_refs, position_ranges))
        return (VERDICT_APPROVED, 1.0, "ok")
    review = verify_claim_moment(
        upper_record_id="S1", upper_dialect="dramatic",
        lowerings=(lw,), check=check,
    )
    assert review is not None
    assert review.verdict == VERDICT_APPROVED
    assert len(received) == 1


def test_claim_moment_skips_with_no_active_lowerings():
    """Without ACTIVE Lowerings the moment check has no anchor and
    returns None. Same semantics as Characterization."""
    def check(upper_ref, lower_refs, position_ranges):
        raise AssertionError("should not be called")
    review = verify_claim_moment(
        upper_record_id="S1", upper_dialect="dramatic",
        lowerings=(), check=check,
    )
    assert review is None


def test_claim_moment_orchestrator_returns_advisory_for_skipped():
    """The orchestrator surfaces skipped checks as Advisories with
    code matching what the comment carries — same shape as
    Characterization."""
    def check(upper_ref, lower_refs, position_ranges):
        raise AssertionError("should not be called")
    results = run_claim_moment_checks(
        checks=(("S_no_lowering", "dramatic", check),),
        lowerings=(),
    )
    assert len(results) == 1
    assert isinstance(results[0], StructuralAdvisory)
    assert "no ACTIVE Lowerings" in results[0].comment


def test_claim_moment_passes_position_ranges_through():
    pr = PositionRange(coord="τ_s", min_value=10, max_value=13)
    lw = _lowering(upper_id="S1", position_range=pr)
    received = []
    def check(upper_ref, lower_refs, position_ranges):
        received.append(position_ranges)
        return (VERDICT_APPROVED, 1.0, "")
    verify_claim_moment(
        upper_record_id="S1", upper_dialect="dramatic",
        lowerings=(lw,), check=check,
    )
    assert received == [(pr,)]


def test_claim_moment_unknown_verdict_falls_back_to_noted():
    lw = _lowering(upper_id="S1")
    def check(upper_ref, lower_refs, position_ranges):
        return ("garbage", 0.5, "what")
    review = verify_claim_moment(
        upper_record_id="S1", upper_dialect="dramatic",
        lowerings=(lw,), check=check,
    )
    assert review.verdict == VERDICT_NOTED
    assert "garbage" in review.comment


# ----------------------------------------------------------------------------
# Integration — Oedipus S_anagnorisis moment check
# ----------------------------------------------------------------------------


def test_oedipus_anagnorisis_moment_check_passes():
    """S_anagnorisis result check should APPROVE at strength=1.0:
    all four moment signatures present at τ_s=13 — three identity
    propositions at KNOWN and the gap_real_parents GAP closed."""
    import oedipus_verification as ov
    results = ov.run()
    moment_reviews = [
        r for r in results
        if isinstance(r, VerificationReview)
        and r.target_record == cross_ref("dramatic", "S_anagnorisis")
    ]
    assert len(moment_reviews) == 1
    r = moment_reviews[0]
    assert r.verdict == VERDICT_APPROVED
    assert r.match_strength == 1.0


def test_oedipus_anagnorisis_moment_check_names_signatures():
    """The comment names all four signatures so an author reviewing
    the verifier output sees what was checked."""
    import oedipus_verification as ov
    results = ov.run()
    moment_review = next(
        r for r in results
        if isinstance(r, VerificationReview)
        and r.target_record == cross_ref("dramatic", "S_anagnorisis")
    )
    c = moment_review.comment
    assert "identity(oedipus, the-exposed-baby) KNOWN: True" in c
    assert "identity(oedipus, the-crossroads-killer) KNOWN: True" in c
    assert "identity(laius, the-crossroads-victim) KNOWN: True" in c
    assert "gap_real_parents closed" in c
    assert "4/4" in c
    # Moment is at τ_s=13 (E_oedipus_anagnorisis's τ_s).
    assert "τ_s=13" in c


# ============================================================================
# Per-record-type orchestrator (V5)
# ============================================================================
#
# A small fixture record type stands in for the dialect records the
# orchestrator iterates. Real Throughline / Argument / Scene records
# would work too, but a synthetic record keeps these tests off the
# dramatic-encoding test path so failures localize to the orchestrator.


from dataclasses import dataclass


@dataclass(frozen=True)
class _FakeUpper:
    id: str
    role_label: str = ""


def _always_approved_check(upper_ref, lower_refs):
    return (VERDICT_APPROVED, 1.0, "always-approved")


def _always_approved_trajectory(upper_ref, lower_refs, position_ranges):
    return (VERDICT_APPROVED, 1.0, "always-approved-trajectory")


def _always_approved_moment(upper_ref, lower_refs, position_ranges):
    return (VERDICT_APPROVED, 1.0, "always-approved-moment")


def test_check_registration_rejects_non_orchestratable_kind():
    """REALIZATION and FLAVOR are not orchestratable in this iteration
    (no primitive dispatch). Constructing a registration with one
    raises at __post_init__."""
    for bad_kind in (COUPLING_REALIZATION, COUPLING_FLAVOR, "made-up"):
        try:
            CheckRegistration(
                coupling_kind=bad_kind,
                record_type="X", field=None,
                applies_to=lambda r: True,
                check_fn=_always_approved_check,
            )
        except ValueError:
            continue
        raise AssertionError(
            f"CheckRegistration accepted non-orchestratable kind {bad_kind!r}"
        )


def test_check_registration_accepts_orchestratable_kinds():
    for kind in ORCHESTRATABLE_COUPLING_KINDS:
        # Should not raise.
        CheckRegistration(
            coupling_kind=kind, record_type="X", field=None,
            applies_to=lambda r: True, check_fn=_always_approved_check,
        )


def test_orchestrate_dispatches_characterization_with_active_lowering():
    record = _FakeUpper(id="U_one")
    lw = _lowering(upper_id="U_one")
    reg = CheckRegistration(
        coupling_kind=COUPLING_CHARACTERIZATION,
        record_type="Throughline", field=None,
        applies_to=lambda r: True,
        check_fn=_always_approved_check,
        description="test",
    )
    out = orchestrate_checks(
        records_by_type={"Throughline": (record,)},
        registry=(reg,), lowerings=(lw,),
        record_dialect="dramatic", reviewed_at_τ_a=500,
    )
    assert len(out) == 1
    review = out[0]
    assert isinstance(review, VerificationReview)
    assert review.verdict == VERDICT_APPROVED
    assert review.target_record.record_id == "U_one"
    assert "characterization" in review.reviewer_id


def test_orchestrate_emits_advisory_when_characterization_has_no_lowering():
    """A registered Characterization on a record with no ACTIVE
    Lowerings produces a StructuralAdvisory, not a silent skip — the
    gap surfaces."""
    record = _FakeUpper(id="U_orphan")
    reg = CheckRegistration(
        coupling_kind=COUPLING_CHARACTERIZATION,
        record_type="Throughline", field=None,
        applies_to=lambda r: True,
        check_fn=_always_approved_check,
        description="orphan-test",
    )
    out = orchestrate_checks(
        records_by_type={"Throughline": (record,)},
        registry=(reg,), lowerings=(),
        record_dialect="dramatic", reviewed_at_τ_a=500,
    )
    assert len(out) == 1
    adv = out[0]
    assert isinstance(adv, StructuralAdvisory)
    assert adv.severity == SEVERITY_NOTED
    assert "no ACTIVE Lowerings" in adv.comment
    assert "orphan-test" in adv.comment, (
        "advisory should name the registration's description so the "
        "author can find which check was skipped"
    )


def test_orchestrate_dispatches_claim_trajectory_without_lowering():
    """Claim-trajectory always runs even without Lowerings (the
    trajectory claim has substrate-wide scope). orchestrate_checks
    must produce a VerificationReview, not an advisory."""
    record = _FakeUpper(id="A_one")
    reg = CheckRegistration(
        coupling_kind=COUPLING_CLAIM_TRAJECTORY,
        record_type="Argument", field=None,
        applies_to=lambda r: True,
        check_fn=_always_approved_trajectory,
    )
    out = orchestrate_checks(
        records_by_type={"Argument": (record,)},
        registry=(reg,), lowerings=(),
        record_dialect="dramatic", reviewed_at_τ_a=500,
    )
    assert len(out) == 1
    assert isinstance(out[0], VerificationReview)
    assert "claim-trajectory" in out[0].reviewer_id


def test_orchestrate_dispatches_claim_moment_with_active_lowering():
    record = _FakeUpper(id="S_one")
    lw = _lowering(upper_id="S_one")
    reg = CheckRegistration(
        coupling_kind=COUPLING_CLAIM_MOMENT,
        record_type="Scene", field=None,
        applies_to=lambda r: True,
        check_fn=_always_approved_moment,
    )
    out = orchestrate_checks(
        records_by_type={"Scene": (record,)},
        registry=(reg,), lowerings=(lw,),
        record_dialect="dramatic", reviewed_at_τ_a=500,
    )
    assert len(out) == 1
    assert isinstance(out[0], VerificationReview)
    assert "claim-moment" in out[0].reviewer_id


def test_orchestrate_emits_advisory_when_claim_moment_has_no_lowering():
    record = _FakeUpper(id="S_orphan")
    reg = CheckRegistration(
        coupling_kind=COUPLING_CLAIM_MOMENT,
        record_type="Scene", field=None,
        applies_to=lambda r: True,
        check_fn=_always_approved_moment,
        description="orphan-moment",
    )
    out = orchestrate_checks(
        records_by_type={"Scene": (record,)},
        registry=(reg,), lowerings=(),
        record_dialect="dramatic", reviewed_at_τ_a=500,
    )
    assert len(out) == 1
    assert isinstance(out[0], StructuralAdvisory)
    assert "orphan-moment" in out[0].comment


def test_orchestrate_skips_records_where_applies_to_returns_false():
    """A registration with a restrictive applies_to silently skips
    non-matching records — no advisory, no review for those. This
    is how "this check is for a specific record" is expressed."""
    matching = _FakeUpper(id="U_match", role_label="main-character")
    non_matching = _FakeUpper(id="U_other", role_label="impact-character")
    lw_match = _lowering(upper_id="U_match")
    lw_other = _lowering(upper_id="U_other")
    reg = CheckRegistration(
        coupling_kind=COUPLING_CHARACTERIZATION,
        record_type="Throughline", field="role_label",
        applies_to=lambda t: t.role_label == "main-character",
        check_fn=_always_approved_check,
    )
    out = orchestrate_checks(
        records_by_type={"Throughline": (matching, non_matching)},
        registry=(reg,), lowerings=(lw_match, lw_other),
        record_dialect="dramatic", reviewed_at_τ_a=500,
    )
    # Only one result: the matching record. The non-matching record
    # was silent-skipped (no review, no advisory).
    assert len(out) == 1
    assert out[0].target_record.record_id == "U_match"


def test_orchestrate_handles_record_type_missing_from_inventory():
    """If a registration's record_type isn't in records_by_type at all,
    the orchestrator silently produces no output for it (the encoding
    didn't supply records of that type — nothing to iterate)."""
    reg = CheckRegistration(
        coupling_kind=COUPLING_CHARACTERIZATION,
        record_type="UnseenType", field=None,
        applies_to=lambda r: True,
        check_fn=_always_approved_check,
    )
    out = orchestrate_checks(
        records_by_type={"Throughline": ()},  # no UnseenType key
        registry=(reg,), lowerings=(),
        record_dialect="dramatic", reviewed_at_τ_a=500,
    )
    assert out == ()


def test_orchestrate_dispatches_multiple_kinds_in_one_run():
    """A registry with all three orchestratable kinds produces one
    result per registration that matches a record. Order-of-results
    follows registry order then record order — predictable for
    walker / display consumers."""
    t = _FakeUpper(id="T_one", role_label="main-character")
    a = _FakeUpper(id="A_one")
    s = _FakeUpper(id="S_one")
    lw_t = _lowering(upper_id="T_one")
    lw_s = _lowering(upper_id="S_one")
    registry = (
        CheckRegistration(
            coupling_kind=COUPLING_CHARACTERIZATION,
            record_type="Throughline", field="role_label",
            applies_to=lambda r: True,
            check_fn=_always_approved_check,
        ),
        CheckRegistration(
            coupling_kind=COUPLING_CLAIM_TRAJECTORY,
            record_type="Argument", field=None,
            applies_to=lambda r: True,
            check_fn=_always_approved_trajectory,
        ),
        CheckRegistration(
            coupling_kind=COUPLING_CLAIM_MOMENT,
            record_type="Scene", field=None,
            applies_to=lambda r: True,
            check_fn=_always_approved_moment,
        ),
    )
    out = orchestrate_checks(
        records_by_type={
            "Throughline": (t,), "Argument": (a,), "Scene": (s,),
        },
        registry=registry, lowerings=(lw_t, lw_s),
        record_dialect="dramatic", reviewed_at_τ_a=500,
    )
    assert len(out) == 3
    # Order: registry order then record order. Throughline first,
    # Argument second, Scene third.
    assert out[0].target_record.record_id == "T_one"
    assert "characterization" in out[0].reviewer_id
    assert out[1].target_record.record_id == "A_one"
    assert "claim-trajectory" in out[1].reviewer_id
    assert out[2].target_record.record_id == "S_one"
    assert "claim-moment" in out[2].reviewer_id


def test_orchestrate_oedipus_run_matches_three_results():
    """Integration: oedipus_verification.run() now goes through the
    orchestrator. It should still produce exactly three results (one
    per registration that fires on the encoding) — same shape as
    when the runner was hand-wired."""
    from oedipus_verification import run as run_oedipus
    out = run_oedipus()
    assert len(out) == 3
    reviews = reviews_only(out)
    assert len(reviews) == 3, (
        "all three Oedipus checks should land as reviews on this "
        "encoding (no missing-Lowering advisories)"
    )
    target_ids = {r.target_record.record_id for r in reviews}
    assert target_ids == {
        "T_mc_oedipus", "A_knowledge_unmakes", "S_anagnorisis",
    }


def test_orchestrate_macbeth_run_matches_three_results():
    """Same integration check on Macbeth."""
    from macbeth_verification import run as run_macbeth
    out = run_macbeth()
    assert len(out) == 3
    reviews = reviews_only(out)
    assert len(reviews) == 3
    target_ids = {r.target_record.record_id for r in reviews}
    assert target_ids == {
        "T_mc_macbeth", "A_ambition_unmakes", "S_macbeth_dies",
    }


def test_orchestrate_ackroyd_run_matches_three_results():
    """Third-encoding integration check: Ackroyd at Dramatic.
    Same V3 shape as Oedipus and Macbeth — one characterization,
    one claim-trajectory, one claim-moment. All three should land
    as reviews on this encoding (no missing-Lowering advisories)."""
    from ackroyd_verification import run as run_ackroyd
    out = run_ackroyd()
    assert len(out) == 3
    reviews = reviews_only(out)
    assert len(reviews) == 3
    target_ids = {r.target_record.record_id for r in reviews}
    assert target_ids == {
        "T_mc_sheppard", "A_truth_recovers", "S_poirot_reveal",
    }


def test_ackroyd_all_reviews_approved_at_full_strength():
    """Ackroyd encoding's contract: every check's signatures hold.
    All three reviews APPROVED at match_strength=1.0. Notably the
    MC-throughline check (characterization on Sheppard) requires the
    substrate to list Sheppard as an attending_physician participant
    on E_mrs_ferrars_suicide — the encoding's insistence that the
    doctor pronouncing death IS a substrate participant, not just
    narrative context."""
    from ackroyd_verification import run as run_ackroyd
    reviews = reviews_only(run_ackroyd())
    for r in reviews:
        assert r.verdict == VERDICT_APPROVED, (
            f"expected {r.target_record.record_id!r} verdict APPROVED; "
            f"got {r.verdict!r}: {r.comment}"
        )
        assert r.match_strength == 1.0, (
            f"expected {r.target_record.record_id!r} match_strength "
            f"1.0; got {r.match_strength}: {r.comment}"
        )


def test_orchestrate_macbeth_save_the_cat_run_matches_four_results():
    """Third encoding integration check: Macbeth at Save the Cat.
    Registers four checks (two strand trajectories, one theme
    trajectory, one finale-beat moment); all four should land as
    reviews against this encoding (no missing-Lowering advisories,
    because every check targets a record with either an ACTIVE
    Lowering or no Lowering dependence)."""
    from macbeth_save_the_cat_verification import run as run_mstc
    out = run_mstc()
    assert len(out) == 4
    reviews = reviews_only(out)
    assert len(reviews) == 4
    target_ids = {r.target_record.record_id for r in reviews}
    assert target_ids == {
        "Strand_A_scotland", "Strand_B_marriage",
        "S_macbeth_stc", "B_14_finale",
    }


def test_macbeth_save_the_cat_all_reviews_approved_at_full_strength():
    """Encoding's contract: every check's signatures hold against the
    substrate as authored. Each review lands APPROVED with
    match_strength=1.0. If this breaks, either the encoding or the
    substrate has drifted — the verifier is the pin."""
    from macbeth_save_the_cat_verification import run as run_mstc
    reviews = reviews_only(run_mstc())
    for r in reviews:
        assert r.verdict == VERDICT_APPROVED, (
            f"expected {r.target_record.record_id!r} verdict APPROVED; "
            f"got {r.verdict!r}: {r.comment}"
        )
        assert r.match_strength == 1.0, (
            f"expected {r.target_record.record_id!r} match_strength "
            f"1.0; got {r.match_strength}: {r.comment}"
        )


def test_orchestrate_ackroyd_save_the_cat_run_matches_four_results():
    """Fourth encoding-verifier integration: Ackroyd at Save the
    Cat. Four checks (two strand trajectories, one theme trajectory,
    one finale-beat moment); all four should land as APPROVED
    reviews."""
    from ackroyd_save_the_cat_verification import run as run_astc
    out = run_astc()
    assert len(out) == 4
    reviews = reviews_only(out)
    assert len(reviews) == 4
    target_ids = {r.target_record.record_id for r in reviews}
    assert target_ids == {
        "Strand_A_case", "Strand_B_flora_ralph",
        "S_ackroyd_stc", "B_14_finale",
    }


def test_ackroyd_save_the_cat_all_reviews_approved_at_full_strength():
    """Ackroyd STC encoding's contract: every check's signatures hold
    against the substrate. The cross-dialect convergence at the
    finale — same four cast-KNOWN signatures as the Dramatic
    dialect's S_poirot_reveal check — is part of the contract."""
    from ackroyd_save_the_cat_verification import run as run_astc
    reviews = reviews_only(run_astc())
    for r in reviews:
        assert r.verdict == VERDICT_APPROVED, (
            f"expected {r.target_record.record_id!r} verdict APPROVED; "
            f"got {r.verdict!r}: {r.comment}"
        )
        assert r.match_strength == 1.0, (
            f"expected {r.target_record.record_id!r} match_strength "
            f"1.0; got {r.match_strength}: {r.comment}"
        )


def test_coverage_report_macbeth_save_the_cat_surfaces_beat_gaps():
    """Integration: the Save the Cat encoding registers four checks
    against save_the_cat.COUPLING_DECLARATIONS. Coverage report
    should surface 14 claim-moment gaps — one per uncovered StcBeat's
    description_of_change declaration (15 beats total minus B_14 which
    has a registered check). No StcStrand or StcStory gaps, both
    strands and the theme are covered. Realization/Flavor
    declarations on StcStory / StcBeat.advances / etc. are
    non-orchestratable and skipped by coverage_report."""
    from macbeth_save_the_cat_verification import (
        CHECK_REGISTRY, RECORDS_BY_TYPE,
    )
    from save_the_cat import COUPLING_DECLARATIONS as STC_DECLS

    gaps = coverage_report(
        records_by_type=RECORDS_BY_TYPE,
        registry=CHECK_REGISTRY,
        coupling_declarations=STC_DECLS,
    )
    assert len(gaps) == 14, (
        f"expected 14 Save the Cat gaps (14 uncovered StcBeats × 1 "
        f"claim-moment declaration each); got {len(gaps)}"
    )
    by_kind = group_gaps_by_kind(gaps)
    assert len(by_kind[COUPLING_CLAIM_MOMENT]) == 14
    assert len(by_kind[COUPLING_CHARACTERIZATION]) == 0
    assert len(by_kind[COUPLING_CLAIM_TRAJECTORY]) == 0
    by_type = group_gaps_by_record_type(gaps)
    assert len(by_type["StcBeat"]) == 14
    assert "StcStrand" not in by_type or len(by_type["StcStrand"]) == 0
    assert "StcStory" not in by_type or len(by_type["StcStory"]) == 0


# ============================================================================
# Coverage report — gaps between registry and coupling declarations
# ============================================================================
#
# A small fixture declaration class stands in for dramatic.CouplingDeclaration
# so these tests stay off the dramatic-encoding test path. The real
# CouplingDeclaration would also work — coverage_report only reads
# `.record_type`, `.field`, `.kind` attributes.


@dataclass(frozen=True)
class _FakeDeclaration:
    record_type: str
    field: Optional[str]
    kind: str


def test_coverage_report_emits_gap_for_declared_uncovered_record():
    """An orchestratable declaration on a record that no registration
    fires on produces a CoverageGap. The basic homework-finder."""
    record = _FakeUpper(id="T_one", role_label="overall-story")
    decl = _FakeDeclaration(
        record_type="Throughline", field="role_label",
        kind=COUPLING_CHARACTERIZATION,
    )
    # Empty registry — no checks defined yet.
    gaps = coverage_report(
        records_by_type={"Throughline": (record,)},
        registry=(),
        coupling_declarations=(decl,),
    )
    assert len(gaps) == 1
    g = gaps[0]
    assert isinstance(g, CoverageGap)
    assert g.record_type == "Throughline"
    assert g.record_id == "T_one"
    assert g.field == "role_label"
    assert g.coupling_kind == COUPLING_CHARACTERIZATION
    assert "T_one" in g.message
    assert "role_label" in g.message


def test_coverage_report_omits_gap_when_registration_covers():
    """A registration matching (record_type, kind) and whose
    applies_to returns True for the record covers the declaration —
    no gap surfaced."""
    record = _FakeUpper(id="T_one", role_label="main-character")
    decl = _FakeDeclaration(
        record_type="Throughline", field="role_label",
        kind=COUPLING_CHARACTERIZATION,
    )
    reg = CheckRegistration(
        coupling_kind=COUPLING_CHARACTERIZATION,
        record_type="Throughline", field="role_label",
        applies_to=lambda t: t.role_label == "main-character",
        check_fn=_always_approved_check,
    )
    gaps = coverage_report(
        records_by_type={"Throughline": (record,)},
        registry=(reg,), coupling_declarations=(decl,),
    )
    assert gaps == ()


def test_coverage_report_emits_gap_when_applies_to_excludes():
    """Same registration as above, but the record's role_label doesn't
    match — applies_to returns False, so coverage isn't claimed, gap
    surfaces. This is the predicate-restricted case the homework
    framing wants visible."""
    record = _FakeUpper(id="T_other", role_label="impact-character")
    decl = _FakeDeclaration(
        record_type="Throughline", field="role_label",
        kind=COUPLING_CHARACTERIZATION,
    )
    reg = CheckRegistration(
        coupling_kind=COUPLING_CHARACTERIZATION,
        record_type="Throughline", field="role_label",
        applies_to=lambda t: t.role_label == "main-character",
        check_fn=_always_approved_check,
    )
    gaps = coverage_report(
        records_by_type={"Throughline": (record,)},
        registry=(reg,), coupling_declarations=(decl,),
    )
    assert len(gaps) == 1
    assert gaps[0].record_id == "T_other"


def test_coverage_report_skips_realization_and_flavor():
    """Realization has no orchestrator dispatch yet; Flavor has no
    verifier by design. Neither produces gaps regardless of registry
    state — the gap report only surfaces orchestratable kinds."""
    record = _FakeUpper(id="C_one")
    decls = (
        _FakeDeclaration("Character", None, COUPLING_REALIZATION),
        _FakeDeclaration("Argument", "domain", COUPLING_FLAVOR),
    )
    gaps = coverage_report(
        records_by_type={"Character": (record,), "Argument": (record,)},
        registry=(), coupling_declarations=decls,
    )
    assert gaps == ()


def test_coverage_report_handles_record_type_not_in_inventory():
    """A declaration on a record_type the encoding didn't supply
    enumerates over zero records — no gaps from that declaration."""
    decl = _FakeDeclaration(
        record_type="UnseenType", field=None,
        kind=COUPLING_CHARACTERIZATION,
    )
    gaps = coverage_report(
        records_by_type={"OtherType": ()},
        registry=(), coupling_declarations=(decl,),
    )
    assert gaps == ()


def test_coverage_report_one_registration_covers_multiple_field_decls():
    """Two field-level declarations of the same (record_type, kind) are
    both covered by a single registration on (record_type, kind) —
    field is informational, not a dispatch key."""
    record = _FakeUpper(id="A_one")
    decls = (
        _FakeDeclaration("Argument", "premise", COUPLING_CLAIM_TRAJECTORY),
        _FakeDeclaration(
            "Argument", "resolution_direction", COUPLING_CLAIM_TRAJECTORY,
        ),
    )
    reg = CheckRegistration(
        coupling_kind=COUPLING_CLAIM_TRAJECTORY,
        record_type="Argument", field="premise",
        applies_to=lambda a: True,
        check_fn=_always_approved_trajectory,
    )
    gaps = coverage_report(
        records_by_type={"Argument": (record,)},
        registry=(reg,), coupling_declarations=decls,
    )
    assert gaps == ()


def test_coverage_report_predicate_exception_treated_as_uncovered():
    """If applies_to raises on a record (author bug in the predicate),
    coverage cannot be relied on — the gap surfaces. This is the
    safer default; an unhandled exception would otherwise read as
    'covered' which is a worse silent failure."""
    record = _FakeUpper(id="T_one", role_label="main-character")
    decl = _FakeDeclaration(
        "Throughline", "role_label", COUPLING_CHARACTERIZATION,
    )
    def _broken_predicate(record):
        raise RuntimeError("author bug")
    reg = CheckRegistration(
        coupling_kind=COUPLING_CHARACTERIZATION,
        record_type="Throughline", field="role_label",
        applies_to=_broken_predicate,
        check_fn=_always_approved_check,
    )
    gaps = coverage_report(
        records_by_type={"Throughline": (record,)},
        registry=(reg,), coupling_declarations=(decl,),
    )
    assert len(gaps) == 1


def test_group_gaps_by_record_buckets_correctly():
    g1 = CoverageGap(
        record_type="Throughline", record_id="T_one",
        record_dialect="dramatic", field="role_label",
        coupling_kind=COUPLING_CHARACTERIZATION, message="m1",
    )
    g2 = CoverageGap(
        record_type="Throughline", record_id="T_one",
        record_dialect="dramatic", field="subject",
        coupling_kind=COUPLING_CHARACTERIZATION, message="m2",
    )
    g3 = CoverageGap(
        record_type="Scene", record_id="S_one",
        record_dialect="dramatic", field="result",
        coupling_kind=COUPLING_CLAIM_MOMENT, message="m3",
    )
    by_record = group_gaps_by_record((g1, g2, g3))
    assert len(by_record["T_one"]) == 2
    assert len(by_record["S_one"]) == 1


def test_group_gaps_by_kind_initializes_orchestratable_keys():
    """The kind-grouped dict starts with all orchestratable kinds as
    empty lists, so a 'no gaps of kind X' read is unambiguous (the
    key is present with empty list, not missing)."""
    by_kind = group_gaps_by_kind(())
    for kind in ORCHESTRATABLE_COUPLING_KINDS:
        assert kind in by_kind
        assert by_kind[kind] == []


def test_coverage_report_macbeth_surfaces_gaps_against_real_encoding():
    """Integration: against the real Macbeth encoding (3 registered
    checks against the full COUPLING_DECLARATIONS surface), the gap
    report surfaces dozens of uncovered (record, field) pairs. The
    exact count is not the point — the contract is that gaps
    surface, broken down by kind across all four orchestratable
    declaration types on the encoding."""
    from macbeth_verification import CHECK_REGISTRY, RECORDS_BY_TYPE
    from macbeth_dramatic import BEATS, STAKES
    from dramatic import COUPLING_DECLARATIONS

    records = dict(RECORDS_BY_TYPE)
    records["Beat"] = BEATS
    records["Stakes"] = STAKES

    gaps = coverage_report(
        records_by_type=records,
        registry=CHECK_REGISTRY,
        coupling_declarations=COUPLING_DECLARATIONS,
    )
    # Macbeth has many uncovered records; loose lower bound.
    assert len(gaps) >= 50, (
        f"expected the registry-vs-declaration gap to surface many "
        f"uncovered records on Macbeth; got only {len(gaps)}"
    )
    by_kind = group_gaps_by_kind(gaps)
    # All three orchestratable kinds should have at least one gap on
    # Macbeth (the encoding only registers one check per kind).
    assert len(by_kind[COUPLING_CHARACTERIZATION]) > 0
    assert len(by_kind[COUPLING_CLAIM_TRAJECTORY]) > 0
    assert len(by_kind[COUPLING_CLAIM_MOMENT]) > 0
    by_type = group_gaps_by_record_type(gaps)
    # Beats are completely uncovered (no Beat registrations on Macbeth).
    assert len(by_type["Beat"]) == len(BEATS)
    # Stakes are completely uncovered (no Stakes registrations).
    assert len(by_type["Stakes"]) == 12, (
        f"4 Stakes × 3 declarations each = 12 expected; got "
        f"{len(by_type['Stakes'])}"
    )


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
    # Integration — Oedipus Characterization
    test_oedipus_verification_main_character_check_passes,
    test_oedipus_verification_includes_owner_resolution_in_comment,
    # Claim-trajectory primitive
    test_claim_trajectory_runs_even_with_no_lowerings,
    test_claim_trajectory_passes_position_ranges_when_present,
    test_claim_trajectory_handles_partial_match,
    test_claim_trajectory_unknown_verdict_falls_back_to_noted,
    test_claim_trajectory_orchestrator_returns_one_review_per_check,
    # Integration — Oedipus Argument trajectory
    test_oedipus_argument_trajectory_check_passes,
    test_oedipus_argument_trajectory_check_uses_inference_engine,
    test_oedipus_run_produces_three_reviews,
    # Claim-moment primitive
    test_claim_moment_runs_with_active_lowering,
    test_claim_moment_skips_with_no_active_lowerings,
    test_claim_moment_orchestrator_returns_advisory_for_skipped,
    test_claim_moment_passes_position_ranges_through,
    test_claim_moment_unknown_verdict_falls_back_to_noted,
    # Integration — Oedipus S_anagnorisis moment check
    test_oedipus_anagnorisis_moment_check_passes,
    test_oedipus_anagnorisis_moment_check_names_signatures,
    # Per-record-type orchestrator (V5)
    test_check_registration_rejects_non_orchestratable_kind,
    test_check_registration_accepts_orchestratable_kinds,
    test_orchestrate_dispatches_characterization_with_active_lowering,
    test_orchestrate_emits_advisory_when_characterization_has_no_lowering,
    test_orchestrate_dispatches_claim_trajectory_without_lowering,
    test_orchestrate_dispatches_claim_moment_with_active_lowering,
    test_orchestrate_emits_advisory_when_claim_moment_has_no_lowering,
    test_orchestrate_skips_records_where_applies_to_returns_false,
    test_orchestrate_handles_record_type_missing_from_inventory,
    test_orchestrate_dispatches_multiple_kinds_in_one_run,
    test_orchestrate_oedipus_run_matches_three_results,
    test_orchestrate_macbeth_run_matches_three_results,
    test_orchestrate_ackroyd_run_matches_three_results,
    test_ackroyd_all_reviews_approved_at_full_strength,
    test_orchestrate_macbeth_save_the_cat_run_matches_four_results,
    test_macbeth_save_the_cat_all_reviews_approved_at_full_strength,
    test_coverage_report_macbeth_save_the_cat_surfaces_beat_gaps,
    test_orchestrate_ackroyd_save_the_cat_run_matches_four_results,
    test_ackroyd_save_the_cat_all_reviews_approved_at_full_strength,
    # Coverage report
    test_coverage_report_emits_gap_for_declared_uncovered_record,
    test_coverage_report_omits_gap_when_registration_covers,
    test_coverage_report_emits_gap_when_applies_to_excludes,
    test_coverage_report_skips_realization_and_flavor,
    test_coverage_report_handles_record_type_not_in_inventory,
    test_coverage_report_one_registration_covers_multiple_field_decls,
    test_coverage_report_predicate_exception_treated_as_uncovered,
    test_group_gaps_by_record_buckets_correctly,
    test_group_gaps_by_kind_initializes_orchestratable_keys,
    test_coverage_report_macbeth_surfaces_gaps_against_real_encoding,
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
