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
# EK2 classifier (event-kind-taxonomy-sketch-01)
# ----------------------------------------------------------------------------
#
# Tests for `classify_event_action_shape` in verifier_helpers.py. The
# classifier reads fold-visible structure (participants + effects) and
# returns "external" or "internal". Synthetic fixtures exercise each
# shape that appears in the three dramatica-complete encodings.


def _classifier_fixtures():
    """Import deferred so this module doesn't force loading
    verifier_helpers at module import time (matches other
    encoding-bound integration tests below)."""
    from substrate import (
        Event, KnowledgeEffect, WorldEffect, Held, Prop, Slot,
        Confidence,
    )
    from verifier_helpers import classify_event_action_shape
    return (
        Event, KnowledgeEffect, WorldEffect, Held, Prop, Slot,
        Confidence, classify_event_action_shape,
    )


def _mk_ke(agent_id, predicate, *args):
    from substrate import KnowledgeEffect, Held, Prop, Slot, Confidence
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(
            prop=Prop(predicate=predicate, args=args),
            slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
            via="test",
        ),
    )


def _mk_we(predicate, *args):
    from substrate import WorldEffect, Prop
    return WorldEffect(prop=Prop(predicate=predicate, args=args))


def _mk_event(event_id, type_, participants, effects):
    from substrate import Event
    return Event(
        id=event_id, type=type_, τ_s=0, τ_a=0,
        participants=participants, effects=tuple(effects),
        branches=frozenset({":canonical"}),
    )


def test_ek2_soliloquy_shape_is_internal():
    """Single agent participant, self-directed KnowledgeEffect —
    internal per EK2 (fails interpersonal clause)."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_soliloquy", "utterance",
        {"speaker": "hamlet"},
        [_mk_ke("hamlet", "thinks", "aloud")],
    )
    assert classify(event, agent_ids=frozenset({"hamlet"})) == "internal"


def test_ek2_command_shape_is_external():
    """Speaker + hearer, KnowledgeEffect on non-actor — external."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_command", "utterance",
        {"speaker": "oedipus", "listener": "servant"},
        [_mk_ke("servant", "bring", "shepherd")],
    )
    agents = frozenset({"oedipus", "servant"})
    assert classify(event, agent_ids=agents) == "external"


def test_ek2_interrogation_shape_is_external():
    """Interrogation: bidirectional KnowledgeEffect — still external
    because at least one effect targets a non-actor."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_interrogation", "utterance",
        {"speaker": "oedipus", "listener": "shepherd"},
        [
            _mk_ke("shepherd", "queried", "by", "oedipus"),
            _mk_ke("oedipus", "heard", "shepherd", "say", "X"),
        ],
    )
    agents = frozenset({"oedipus", "shepherd"})
    assert classify(event, agent_ids=agents) == "external"


def test_ek2_killing_shape_is_external():
    """Two agent participants, WorldEffect (dead) — external."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_killing", "killing",
        {"killer": "oedipus", "victim": "laius"},
        [_mk_we("dead", "laius"), _mk_we("killed", "oedipus", "laius")],
    )
    agents = frozenset({"oedipus", "laius"})
    assert classify(event, agent_ids=agents) == "external"


def test_ek2_marriage_shape_is_external():
    """Two agent participants, WorldEffect — external."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_marriage", "marriage",
        {"husband": "oedipus", "wife": "jocasta"},
        [_mk_we("married", "oedipus", "jocasta")],
    )
    agents = frozenset({"oedipus", "jocasta"})
    assert classify(event, agent_ids=agents) == "external"


def test_ek2_realization_shape_is_internal():
    """Single agent, self-KnowledgeEffect only — internal."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_realization", "realization",
        {"agent": "oedipus"},
        [_mk_ke("oedipus", "realizes", "who", "he", "is")],
    )
    agents = frozenset({"oedipus"})
    assert classify(event, agent_ids=agents) == "internal"


def test_ek2_location_does_not_inflate_interpersonal_when_agent_ids_filters():
    """`E_oedipus_blinding`-shape: agent + location, WorldEffect. The
    location is not an agent; under the agent_ids filter, the event
    has only one agent-participant and classifies as internal.
    Pinned by the sketch's worked-case table."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_blinding", "blinding",
        {"agent": "oedipus", "location": "thebes"},
        [_mk_we("blind", "oedipus")],
    )
    agents = frozenset({"oedipus"})  # thebes is a location, not in agent_ids
    assert classify(event, agent_ids=agents) == "internal"


def test_ek2_without_agent_ids_counts_all_participants():
    """Without the agent_ids filter, every distinct participant id
    counts toward the interpersonal clause. The blinding event then
    classifies external because 'agent' and 'location' are distinct."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_blinding", "blinding",
        {"agent": "oedipus", "location": "thebes"},
        [_mk_we("blind", "oedipus")],
    )
    assert classify(event) == "external"  # no agent_ids filter


def test_ek2_prophecy_received_is_internal_when_sender_unencoded():
    """E_prophecy_received-shape: the divine sender is not a
    participant. Only one agent in participants; KnowledgeEffect is
    on that agent (self). Internal per EK2."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_prophecy", "prophecy_received",
        {"recipient": "oedipus"},
        [_mk_ke("oedipus", "will_kill", "father")],
    )
    agents = frozenset({"oedipus"})
    assert classify(event, agent_ids=agents) == "internal"


def test_ek2_primary_actor_precedence_killer_over_speaker():
    """If both `killer` and `speaker` are present, `killer` wins
    per the _PRIMARY_ACTOR_ROLES precedence. KnowledgeEffect whose
    target is the speaker (not killer) counts as outward."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_mixed", "killing",
        {"killer": "a", "speaker": "b"},
        [_mk_ke("b", "is_killed", "by", "a")],
    )
    agents = frozenset({"a", "b"})
    assert classify(event, agent_ids=agents) == "external"


def test_ek2_list_valued_participants_flatten_correctly():
    """Some events use list-valued role slots (e.g., multiple killers
    or victims). Each id in the list counts toward the interpersonal
    clause."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_multi", "battle",
        {"killers": ["a", "b"], "victim": "c"},
        [_mk_we("dead", "c")],
    )
    agents = frozenset({"a", "b", "c"})
    assert classify(event, agent_ids=agents) == "external"


def test_ek2_no_outward_effect_is_internal():
    """Two participants but only self-directed KnowledgeEffect. Fails
    the outward-effect clause; internal."""
    (_, _, _, _, _, _, _, classify) = _classifier_fixtures()
    event = _mk_event(
        "E_self_only", "utterance",
        {"speaker": "a", "listener": "b"},
        [_mk_ke("a", "thinks", "x")],  # effect targets actor only
    )
    agents = frozenset({"a", "b"})
    assert classify(event, agent_ids=agents) == "internal"


# ----------------------------------------------------------------------------
# EK2 integration pins — three dramatica-complete verifiers' spectrum
# ----------------------------------------------------------------------------
#
# Pinned verdict bands rather than exact match_strength values per the
# sketch's implementation brief ("the test is not 'the verdict is
# exactly 0.69'; it is 'the verdict is in the expected band'"). Exact
# strengths are allowed to drift with encoding edits.


def test_ek2_oedipus_verifier_both_characterizations_approved():
    """Post-EK2 Oedipus: DA_mc and DSP_approach both APPROVED. Pre-EK2
    both were NEEDS_WORK 0.31 — the sketch's load-bearing claim that
    EK2 removes verifier-heuristic brittleness from the spectrum."""
    from oedipus_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    assert by_target["DA_mc"].verdict == VERDICT_APPROVED, (
        f"DA_mc expected APPROVED under EK2; got "
        f"{by_target['DA_mc'].verdict} "
        f"(strength={by_target['DA_mc'].match_strength})"
    )
    assert by_target["DSP_approach"].verdict == VERDICT_APPROVED
    assert by_target["DA_mc"].match_strength >= 0.7
    assert by_target["DSP_approach"].match_strength >= 0.65


def test_ek2_macbeth_verifier_no_regression():
    """Post-EK2 Macbeth: DA_mc stays PARTIAL, DSP_approach stays
    APPROVED. No regression from the pre-EK2 baseline (0.69 / 0.79).
    EK2 may move strengths slightly; the verdict bands hold."""
    from macbeth_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    assert by_target["DA_mc"].verdict == VERDICT_PARTIAL_MATCH
    assert by_target["DSP_approach"].verdict == VERDICT_APPROVED
    assert by_target["DA_mc"].match_strength >= 0.6
    assert by_target["DSP_approach"].match_strength >= 0.65


def test_ek2_ackroyd_verifier_be_er_inversion_preserved():
    """Post-EK2 Ackroyd: the Be-er check (DSP_approach) still lands
    PARTIAL — Sheppard's internal-ratio is modest because the
    cinematic murder and suicide pull the ratio toward Do-er. EK2's
    complement-of-external definition preserves the inversion
    semantics the original check had."""
    from ackroyd_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    assert by_target["DSP_approach"].verdict == VERDICT_PARTIAL_MATCH
    assert 0.3 <= by_target["DSP_approach"].match_strength < 0.6


# ----------------------------------------------------------------------------
# dramatica-complete → substrate verifier surface extension
# (item 2 from the design README's Upcoming list)
# ----------------------------------------------------------------------------
#
# Each of the three verifiers now ships 8 checks (was 4): adds DSP_resolve,
# DSP_growth, Story_goal, and Story_consequence. Integration pins confirm
# the extension lands and the new checks produce honest spectrum signal.


def test_verifier_surface_has_eight_checks_per_encoding():
    """Historical pin for the 8-check surface that landed before
    pressure-shape-taxonomy-sketch-01. Superseded by
    `test_lt_verifier_surface_has_nine_checks_per_encoding` once the
    LT2 DSP_limit check landed; kept so the sketch-by-sketch growth
    of the verifier surface is visible in the test suite. At 9
    checks today."""
    from oedipus_dramatica_complete_verification import run as o_run
    from macbeth_dramatica_complete_verification import run as m_run
    from ackroyd_dramatica_complete_verification import run as a_run
    assert len(o_run()) >= 8
    assert len(m_run()) >= 8
    assert len(a_run()) >= 8


def test_oedipus_story_consequence_averted_at_end():
    """Oedipus's Story_consequence = plague-continues. Under
    Outcome=Success the consequence is AVOIDED at τ_end —
    pollution is identified (parricide derives) and expelled
    (exile holds)."""
    from oedipus_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    assert by_target["Story_consequence"].verdict == VERDICT_APPROVED
    assert by_target["Story_consequence"].match_strength == 1.0


def test_macbeth_story_goal_three_phase_kingship():
    """Macbeth's Story_goal = restore succession. Three-phase
    trajectory: Duncan (rightful) → Macbeth (usurper) → Malcolm
    (restored), all three distinct τ_s values, Malcolm king at end."""
    from macbeth_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    assert by_target["Story_goal"].verdict == VERDICT_APPROVED
    assert by_target["Story_goal"].match_strength == 1.0


def test_macbeth_dsp_growth_monotonic_killing():
    """Macbeth's DSP_growth=Stop. Substrate signature: killed +
    ordered_killing count with macbeth as killer rises monotonically
    (he never self-terminates the killing)."""
    from macbeth_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    assert by_target["DSP_growth"].verdict == VERDICT_APPROVED


def test_ackroyd_resolve_steadfast_lands_before_investigation_arc():
    """Ackroyd's DSP_resolve=Steadfast. Sheppard's
    betrayer_of_trust role derives at τ_s=1 — before the
    investigation arc begins at τ_s=2. Classic steadfast signature:
    the MC's defining trait is a pre-arc property, not a mid-arc
    transition."""
    from ackroyd_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    assert by_target["DSP_resolve"].verdict == VERDICT_APPROVED


def test_ackroyd_growth_start_after_ultimatum():
    """Ackroyd's DSP_growth=Start. Substrate signature:
    confession_writing (τ_s=10) follows ultimatum (τ_s=9) —
    Sheppard 'starts' what he had been failing to start, but only
    under external compulsion. Classic Start/Bad shape."""
    from ackroyd_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    assert by_target["DSP_growth"].verdict == VERDICT_APPROVED


def test_ackroyd_story_consequence_approved_after_ralph_cleared_fix():
    """Ackroyd's Story_consequence is now APPROVED after the
    substrate gap was closed: E_poirot_reveals_solution now carries
    an explicit world-effect retracting accused_of_murder(
    ralph_paton, ackroyd), so Ralph is structurally cleared at the
    reveal rather than only socially inferred. The PARTIAL 0.5
    this test initially pinned was a real substrate-completeness
    finding the verifier surfaced; fix landed in ackroyd.py."""
    from ackroyd_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    assert by_target["Story_consequence"].verdict == VERDICT_APPROVED
    assert by_target["Story_consequence"].match_strength == 1.0


# ----------------------------------------------------------------------------
# LT2 / LT3 classifier (pressure-shape-taxonomy-sketch-01)
# ----------------------------------------------------------------------------
#
# Tests for `classify_arc_limit_shape` in verifier_helpers.py. The
# classifier reads fold-visible fabula structure (retractions,
# identity-prop effects, rule-derivable emergences) and returns
# `"optionlock"` when any convergence signal kind fires,
# `"timelock-consistent"` when none does. Synthetic fixtures exercise
# each signal kind in isolation plus the cross-products.


def _lt_fixtures():
    """Import deferred to keep import graph narrow; matches
    _classifier_fixtures pattern."""
    from substrate import (
        Event, KnowledgeEffect, WorldEffect, Held, Prop, Slot,
        Confidence, Rule, Branch, IDENTITY_PREDICATE,
    )
    from verifier_helpers import classify_arc_limit_shape
    return (
        Event, KnowledgeEffect, WorldEffect, Held, Prop, Slot,
        Confidence, Rule, Branch, IDENTITY_PREDICATE,
        classify_arc_limit_shape,
    )


def _lt_mk_event(event_id, τ_s, effects, participants=None):
    from substrate import Event
    return Event(
        id=event_id, type="generic", τ_s=τ_s, τ_a=τ_s,
        participants=participants or {"agent": "a"},
        effects=tuple(effects),
        branches=frozenset({":canonical"}),
    )


def _lt_branches():
    from substrate import Branch
    canonical = Branch(label=":canonical", kind="canonical", parent=None)
    return canonical, {":canonical": canonical}


def test_lt2_empty_fabula_is_timelock_consistent():
    """Zero events → zero convergence signals → timelock-consistent
    by LT3's complement rule. Not an error: trivially consistent."""
    (*_, classify) = _lt_fixtures()
    canonical, all_branches = _lt_branches()
    result = classify((), (), canonical, all_branches)
    assert result == ("timelock-consistent", 0.0, ())


def test_lt2_retraction_signal_alone():
    """One event asserts P; a later event retracts with asserts=False.
    Retraction kind fires; other signal kinds don't. Strength 1/3."""
    from substrate import WorldEffect, Prop
    (*_, classify) = _lt_fixtures()
    canonical, all_branches = _lt_branches()
    P = Prop("at_location", ("a", "forest"))
    fabula = (
        _lt_mk_event("E1", 1, [WorldEffect(prop=P, asserts=True)]),
        _lt_mk_event("E2", 2, [WorldEffect(prop=P, asserts=False)]),
    )
    classification, strength, signals = classify(
        fabula, (), canonical, all_branches,
    )
    assert classification == "optionlock"
    assert signals == ("retraction:1",)
    assert abs(strength - 1/3) < 1e-9


def test_lt2_retraction_without_prior_assertion_does_not_fire():
    """asserts=False on a proposition never previously asserted in
    this fabula is NOT a retraction. LT2's first-clause literal
    wording: 'where P was previously world-asserted'."""
    from substrate import WorldEffect, Prop
    (*_, classify) = _lt_fixtures()
    canonical, all_branches = _lt_branches()
    P = Prop("at_location", ("a", "forest"))
    fabula = (
        _lt_mk_event("E1", 1, [WorldEffect(prop=P, asserts=False)]),
    )
    classification, _strength, signals = classify(
        fabula, (), canonical, all_branches,
    )
    assert classification == "timelock-consistent"
    assert signals == ()


def test_lt2_identity_resolution_via_world_effect():
    """An event with a world-level identity/2 proposition is an
    identity-resolution signal — equivalence-class collapse visible
    at fold time."""
    from substrate import WorldEffect, Prop, IDENTITY_PREDICATE
    (*_, classify) = _lt_fixtures()
    canonical, all_branches = _lt_branches()
    identity = Prop(IDENTITY_PREDICATE, ("oedipus", "the-exposed-baby"))
    fabula = (
        _lt_mk_event("E_reveal", 5, [WorldEffect(prop=identity)]),
    )
    classification, strength, signals = classify(
        fabula, (), canonical, all_branches,
    )
    assert classification == "optionlock"
    assert signals == ("identity-resolution:1",)
    assert abs(strength - 1/3) < 1e-9


def test_lt2_identity_resolution_via_knowledge_effect():
    """An identity/2 prop carried in a KnowledgeEffect's held.prop
    also counts as an identity-resolution signal."""
    from substrate import (
        KnowledgeEffect, Held, Prop, Slot, Confidence, IDENTITY_PREDICATE,
    )
    (*_, classify) = _lt_fixtures()
    canonical, all_branches = _lt_branches()
    identity = Prop(IDENTITY_PREDICATE, ("oedipus", "the-exposed-baby"))
    ke = KnowledgeEffect(
        agent_id="oedipus",
        held=Held(prop=identity, slot=Slot.KNOWN,
                  confidence=Confidence.CERTAIN, via="realization"),
    )
    fabula = (_lt_mk_event("E_realize", 5, [ke]),)
    classification, _strength, signals = classify(
        fabula, (), canonical, all_branches,
    )
    assert classification == "optionlock"
    assert signals == ("identity-resolution:1",)


def test_lt2_rule_emergence_signal_alone():
    """Premises accrete across the fabula; a rule-head compound
    becomes derivable at end. Rule-emergence signal fires even when
    the compound is also authored — the strip-authored-heads refinement
    keeps this robust against N10 (authored wins)."""
    from substrate import WorldEffect, Prop, Rule
    (*_, classify) = _lt_fixtures()
    canonical, all_branches = _lt_branches()
    killed = Prop("killed", ("X", "Y"))
    child_of = Prop("child_of", ("X", "Y"))
    parricide = Prop("parricide", ("X", "Y"))
    rule = Rule(id="parricide", head=parricide, body=(killed, child_of))
    fabula = (
        _lt_mk_event("E1", 1, [
            WorldEffect(prop=Prop("killed", ("o", "l"))),
        ]),
        _lt_mk_event("E2", 2, [
            WorldEffect(prop=Prop("child_of", ("o", "l"))),
        ]),
    )
    classification, strength, signals = classify(
        fabula, (rule,), canonical, all_branches,
    )
    assert classification == "optionlock"
    assert signals == ("rule-emergence:1",)
    assert abs(strength - 1/3) < 1e-9


def test_lt2_rule_emergence_fires_when_compound_also_authored():
    """N10 says authored beats derived; the classifier's strip-and-
    rederive step must still detect the rule firing even when the
    encoding directly authors the compound at an event."""
    from substrate import WorldEffect, Prop, Rule
    (*_, classify) = _lt_fixtures()
    canonical, all_branches = _lt_branches()
    killed = Prop("killed", ("X", "Y"))
    child_of = Prop("child_of", ("X", "Y"))
    parricide_head = Prop("parricide", ("X", "Y"))
    rule = Rule(
        id="parricide", head=parricide_head,
        body=(killed, child_of),
    )
    fabula = (
        _lt_mk_event("E1", 1, [
            WorldEffect(prop=Prop("killed", ("o", "l"))),
            WorldEffect(prop=Prop("child_of", ("o", "l"))),
            WorldEffect(prop=Prop("parricide", ("o", "l"))),
        ]),
    )
    classification, _strength, signals = classify(
        fabula, (rule,), canonical, all_branches,
    )
    assert classification == "optionlock"
    assert signals == ("rule-emergence:1",)


def test_lt2_all_three_kinds_firing_gives_strength_one():
    """Retraction + identity-resolution + rule-emergence — strength
    1.0 because 3/3 signal kinds fire."""
    from substrate import (
        WorldEffect, Prop, Rule, IDENTITY_PREDICATE,
    )
    (*_, classify) = _lt_fixtures()
    canonical, all_branches = _lt_branches()
    P = Prop("at_location", ("a", "forest"))
    identity = Prop(IDENTITY_PREDICATE, ("a", "b"))
    killed = Prop("killed", ("X", "Y"))
    child_of = Prop("child_of", ("X", "Y"))
    parricide = Prop("parricide", ("X", "Y"))
    rule = Rule(id="parricide", head=parricide, body=(killed, child_of))
    fabula = (
        _lt_mk_event("E1", 1, [
            WorldEffect(prop=P, asserts=True),
            WorldEffect(prop=Prop("killed", ("x", "y"))),
            WorldEffect(prop=Prop("child_of", ("x", "y"))),
        ]),
        _lt_mk_event("E2", 2, [
            WorldEffect(prop=P, asserts=False),
            WorldEffect(prop=identity),
        ]),
    )
    classification, strength, signals = classify(
        fabula, (rule,), canonical, all_branches,
    )
    assert classification == "optionlock"
    assert strength == 1.0
    assert set(signals) == {
        "retraction:1", "identity-resolution:1", "rule-emergence:1",
    }


def test_lt2_oedipus_fabula_classifies_optionlock():
    """Integration pin: the real Oedipus encoding lands Optionlock
    with identity-resolution + rule-emergence signals (matching the
    sketch's LT2 worked-case prediction)."""
    from substrate import CANONICAL
    from verifier_helpers import classify_arc_limit_shape
    from oedipus import FABULA, RULES, ALL_BRANCHES
    classification, strength, signals = classify_arc_limit_shape(
        FABULA, RULES, CANONICAL, ALL_BRANCHES,
    )
    assert classification == "optionlock"
    assert any(s.startswith("identity-resolution:") for s in signals)
    assert any(s.startswith("rule-emergence:") for s in signals)
    assert strength >= 2 / 3


def test_lt2_macbeth_fabula_classifies_optionlock():
    """Integration pin: Macbeth lands Optionlock via retraction +
    rule-emergence (the retraction is king=False at death; the
    emergences are the inference-01-retired compounds)."""
    from substrate import CANONICAL
    from verifier_helpers import classify_arc_limit_shape
    from macbeth import FABULA, RULES, ALL_BRANCHES
    classification, _strength, signals = classify_arc_limit_shape(
        FABULA, RULES, CANONICAL, ALL_BRANCHES,
    )
    assert classification == "optionlock"
    assert any(s.startswith("retraction:") for s in signals)
    assert any(s.startswith("rule-emergence:") for s in signals)


def test_lt2_ackroyd_fabula_classifies_optionlock():
    """Integration pin: Ackroyd lands Optionlock via retraction
    (post-F5 Ralph-cleared fix) + rule-emergence (betrayer_of_trust
    and driver_of_suicide)."""
    from substrate import CANONICAL
    from verifier_helpers import classify_arc_limit_shape
    from ackroyd import FABULA, RULES, ALL_BRANCHES
    classification, _strength, signals = classify_arc_limit_shape(
        FABULA, RULES, CANONICAL, ALL_BRANCHES,
    )
    assert classification == "optionlock"
    assert any(s.startswith("retraction:") for s in signals)
    assert any(s.startswith("rule-emergence:") for s in signals)


def test_lt2_rocky_substrate_shows_mild_convergence_not_clean_timelock():
    """Phase 1 Rocky substrate authoring finding: Rocky's fabula shows
    mild convergence signals — one retraction (Mac's scheduled fight
    retracted when Mac breaks his hand) and one rule-emergence
    (went_the_distance derivable at τ_s=55) — and classifies as
    Optionlock 0.67 under LT2, despite the dramatic encoding declaring
    DSP_limit=Timelock. This is the LT2-OQ3 'subplot-only convergence'
    case the sketch anticipated, and it sharpens the forcing function
    for LT3-strong (scheduling-vocabulary detection). No identity
    resolutions (Rocky is Steadfast — no equivalence classes collapse).
    """
    from substrate import CANONICAL
    from verifier_helpers import classify_arc_limit_shape
    from rocky import FABULA, RULES, ALL_BRANCHES
    classification, strength, signals = classify_arc_limit_shape(
        FABULA, RULES, CANONICAL, ALL_BRANCHES,
    )
    assert classification == "optionlock"
    assert abs(strength - 2/3) < 1e-9
    assert any(s.startswith("retraction:") for s in signals)
    assert any(s.startswith("rule-emergence:") for s in signals)
    assert not any(s.startswith("identity-resolution:") for s in signals)


def test_rocky_went_the_distance_rule_derives_at_fight_end():
    """Rocky's single rule fires at τ_s=55: fought_rounds(rocky, apollo, 15)
    + standing_at_final_bell(rocky, fight) ⇒ went_the_distance(rocky,
    apollo). This is the substrate-visible form of the MC's articulated
    goal from the night-before-fight scene."""
    from substrate import (
        CANONICAL, in_scope, project_world, world_holds_derived,
    )
    from rocky import FABULA, RULES, ALL_BRANCHES, went_the_distance
    events = [e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)]
    τ_end = max(e.τ_s for e in events if e.τ_s is not None)
    world = project_world(events, up_to_τ_s=τ_end)
    proof = world_holds_derived(
        world, went_the_distance("rocky", "apollo"), RULES,
    )
    assert proof is not None
    assert proof.kind == "derived"


def test_rocky_has_no_identity_propositions():
    """Rocky is Steadfast — no identity placeholder entities, no
    equivalence-class collapses across the arc. This is the
    structural signature that LT2 correctly detects (zero identity-
    resolution signal count)."""
    from substrate import IDENTITY_PREDICATE, WorldEffect, KnowledgeEffect
    from rocky import FABULA, ENTITIES
    # No 'abstract' entities intended as identity placeholders other
    # than `fight`/`mac_fight` (which are referenceable entities, not
    # identity stand-ins).
    for e in FABULA:
        for ef in e.effects:
            if isinstance(ef, WorldEffect):
                assert ef.prop.predicate != IDENTITY_PREDICATE, (
                    f"unexpected identity prop in {e.id}"
                )
            elif isinstance(ef, KnowledgeEffect):
                assert ef.held.prop.predicate != IDENTITY_PREDICATE, (
                    f"unexpected identity prop in {e.id}"
                )


def test_lt5_timelock_declared_on_timelock_consistent_substrate_is_noted():
    """LT5's disposition: Timelock declared + no convergence signals
    → NOTED (consistent-but-not-affirmed). The honest asymmetry
    stated in LT3."""
    from verifier_helpers import dsp_limit_characterization_check
    from substrate import CANONICAL, Branch
    canonical = Branch(label=":canonical", kind="canonical", parent=None)
    all_branches = {":canonical": canonical}
    verdict, strength, comment = dsp_limit_characterization_check(
        (), (), canonical, all_branches, "timelock",
    )
    assert verdict == VERDICT_NOTED
    assert strength is None
    assert "timelock" in comment.lower()
    assert "complement-only" in comment.lower()


def test_lt5_optionlock_declared_on_optionlock_substrate_is_approved():
    """LT5's primary case: Optionlock declared + convergence signals
    present → APPROVED."""
    from verifier_helpers import dsp_limit_characterization_check
    from substrate import CANONICAL, WorldEffect, Prop, Branch, Event
    canonical = Branch(label=":canonical", kind="canonical", parent=None)
    all_branches = {":canonical": canonical}
    P = Prop("x", ("a",))
    e1 = Event(
        id="E1", type="g", τ_s=1, τ_a=1, participants={"agent": "a"},
        effects=(WorldEffect(prop=P, asserts=True),),
        branches=frozenset({":canonical"}),
    )
    e2 = Event(
        id="E2", type="g", τ_s=2, τ_a=2, participants={"agent": "a"},
        effects=(WorldEffect(prop=P, asserts=False),),
        branches=frozenset({":canonical"}),
    )
    verdict, strength, _comment = dsp_limit_characterization_check(
        (e1, e2), (), canonical, all_branches, "optionlock",
    )
    assert verdict == VERDICT_APPROVED
    assert strength > 0


def test_lt5_optionlock_declared_on_timelock_consistent_substrate_is_needs_work():
    """LT5 disagreement case: Optionlock declared but no convergence
    → NEEDS_WORK. The substrate contradicts the declaration."""
    from verifier_helpers import dsp_limit_characterization_check
    from substrate import Branch
    canonical = Branch(label=":canonical", kind="canonical", parent=None)
    all_branches = {":canonical": canonical}
    verdict, strength, _comment = dsp_limit_characterization_check(
        (), (), canonical, all_branches, "optionlock",
    )
    assert verdict == VERDICT_NEEDS_WORK
    assert strength == 0.0


def test_lt_verifier_surface_has_nine_checks_per_encoding():
    """Post-LT2 landing: each of the three dramatica-complete
    verifiers runs 9 checks (was 8). The ninth is DSP_limit,
    adding a Characterization-primitive check for pressure shape."""
    from oedipus_dramatica_complete_verification import run as o_run
    from macbeth_dramatica_complete_verification import run as m_run
    from ackroyd_dramatica_complete_verification import run as a_run
    assert len(o_run()) == 9
    assert len(m_run()) == 9
    assert len(a_run()) == 9


def test_lt_oedipus_dsp_limit_approved_with_two_signal_kinds():
    """Post-LT2: Oedipus DSP_limit APPROVED at strength 0.67 (two of
    three signal kinds fire — identity-resolution + rule-emergence;
    no retractions in the Oedipus substrate)."""
    from oedipus_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    r = by_target["DSP_limit"]
    assert r.verdict == VERDICT_APPROVED
    assert abs(r.match_strength - 2/3) < 1e-9
    assert "identity-resolution" in r.comment
    assert "rule-emergence" in r.comment


def test_lt_macbeth_dsp_limit_approved_with_two_signal_kinds():
    """Post-LT2: Macbeth DSP_limit APPROVED at strength 0.67 via
    retraction (king=False at death) + rule-emergence (kinslayer /
    regicide / breach_of_hospitality / tyrant)."""
    from macbeth_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    r = by_target["DSP_limit"]
    assert r.verdict == VERDICT_APPROVED
    assert abs(r.match_strength - 2/3) < 1e-9
    assert "retraction" in r.comment
    assert "rule-emergence" in r.comment


def test_lt_ackroyd_dsp_limit_approved_with_two_signal_kinds():
    """Post-LT2: Ackroyd DSP_limit APPROVED at strength 0.67 via
    retraction (Ralph cleared at reveal, landed same-day as F5
    substrate fix) + rule-emergence (betrayer_of_trust +
    driver_of_suicide)."""
    from ackroyd_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    r = by_target["DSP_limit"]
    assert r.verdict == VERDICT_APPROVED
    assert abs(r.match_strength - 2/3) < 1e-9
    assert "retraction" in r.comment
    assert "rule-emergence" in r.comment


# ----------------------------------------------------------------------------
# Rocky verifier — Phase 2 integration pins (pressure-shape-taxonomy-sketch-01)
# ----------------------------------------------------------------------------
#
# Rocky is the first Timelock + Failure + Judgment=Good encoding in the
# corpus. The verifier surface stresses LT5's asymmetric disposition
# table (DSP_limit NEEDS_WORK on a Timelock declaration + Optionlock-
# shaped substrate), inverted DSP_outcome semantics (Failure = goal
# fact does NOT land), and the Good-judgment positive-closure cluster.


def test_rocky_verifier_has_nine_checks():
    """Rocky's verifier surface matches the other three dramatica-
    complete verifiers at 9 checks across all three primitives."""
    from rocky_dramatica_complete_verification import run
    assert len(run()) == 9


def test_rocky_dsp_limit_needs_work_on_timelock_declaration():
    """First non-APPROVED DSP_limit in the corpus. Rocky declares
    Timelock; LT2 reads the substrate and counts retraction (Mac's
    scheduled fight) + rule-emergence (went_the_distance) → Optionlock
    0.67. LT5's disposition reports NEEDS_WORK for the declaration/
    substrate disagreement — the honest signal the sketch named as
    the forcing function for LT3-strong (OQ1 / OQ3)."""
    from rocky_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    r = by_target["DSP_limit"]
    assert r.verdict == VERDICT_NEEDS_WORK
    assert "timelock" in r.comment.lower()
    assert "optionlock" in r.comment.lower()


def test_rocky_dsp_outcome_failure_approved():
    """Rocky's Failure declaration is supported by substrate: went_the_
    distance(rocky, apollo) derives at τ_s=end, which contaminates
    the clean-publicity-stunt goal. Inverted from the Success checks
    in the other three encodings: for Failure, the goal's load-bearing
    fact being the OPPOSITE of what the goal predicts IS the evidence
    that supports the declaration."""
    from rocky_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    r = by_target["DSP_outcome"]
    assert r.verdict == VERDICT_APPROVED
    assert r.match_strength == 1.0
    assert "went_the_distance" in r.comment


def test_rocky_dsp_judgment_good_positive_closure_cluster():
    """First Judgment=Good for the MC in the corpus. Rocky's Good
    signature is the confluence of three positive-closure facts at
    τ_s=end: went_the_distance (achievement), called_out(rocky,
    adrian) (relationship payoff), refused_rematch(rocky)
    (acceptance). All three hold — APPROVED 1.0."""
    from rocky_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    r = by_target["DSP_judgment"]
    assert r.verdict == VERDICT_APPROVED
    assert r.match_strength == 1.0


def test_rocky_dsp_resolve_steadfast_via_structural_invariance():
    """Rocky's Steadfast rests on the structural absence of equivalence-
    class collapses involving the MC — unlike Ackroyd's Steadfast
    (which rests on a pre-existing rule-derived trait). Same DSP
    axis value, different verifier evidence."""
    from rocky_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    r = by_target["DSP_resolve"]
    assert r.verdict == VERDICT_APPROVED


def test_rocky_dsp_growth_start_via_articulated_goal_acquisition():
    """Rocky's Start is privately chosen at the night-before-fight
    empty-ring scene (τ_s=45), not externally compelled like Ackroyd's
    ultimatum-driven confession-writing. Substrate signature:
    articulated_goal enters Rocky's knowledge state at τ_s=45 and
    holds through τ_s=end."""
    from rocky_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    r = by_target["DSP_growth"]
    assert r.verdict == VERDICT_APPROVED


def test_rocky_all_characterization_and_claim_checks_except_dsp_limit_approved():
    """Summary pin: Rocky produces 8 APPROVED and 1 NEEDS_WORK
    (DSP_limit) across the 9-check surface. Ackroyd/Macbeth/Oedipus
    each produce 9/9 APPROVED on DSP_limit; Rocky is the first to
    exercise LT5's disagreement verdict — which is the core finding
    the Phase 2 landing reports."""
    from rocky_dramatica_complete_verification import run
    reviews = run()
    approved = sum(1 for r in reviews if r.verdict == VERDICT_APPROVED)
    needs_work = sum(1 for r in reviews if r.verdict == VERDICT_NEEDS_WORK)
    assert approved == 8
    assert needs_work == 1
    # The single NEEDS_WORK is on DSP_limit specifically.
    needs_work_targets = [
        r.target_record.record_id for r in reviews
        if r.verdict == VERDICT_NEEDS_WORK
    ]
    assert needs_work_targets == ["DSP_limit"]


def test_oedipus_dsp_growth_partial_rate_heuristic():
    """Oedipus's DSP_growth=Stop. Honest PARTIAL finding: the
    current rate-based heuristic (participation events per τ_s pre
    vs post anagnorisis) doesn't capture Oedipus's actual
    cessation pattern because post-anagnorisis events are densely
    clustered. A primary-actor-shift heuristic would be stronger;
    deferred as a follow-on refinement."""
    from oedipus_dramatica_complete_verification import run
    reviews = run()
    by_target = {r.target_record.record_id: r for r in reviews}
    assert by_target["DSP_growth"].verdict == VERDICT_PARTIAL_MATCH


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
    # EK2 classifier (event-kind-taxonomy-sketch-01)
    test_ek2_soliloquy_shape_is_internal,
    test_ek2_command_shape_is_external,
    test_ek2_interrogation_shape_is_external,
    test_ek2_killing_shape_is_external,
    test_ek2_marriage_shape_is_external,
    test_ek2_realization_shape_is_internal,
    test_ek2_location_does_not_inflate_interpersonal_when_agent_ids_filters,
    test_ek2_without_agent_ids_counts_all_participants,
    test_ek2_prophecy_received_is_internal_when_sender_unencoded,
    test_ek2_primary_actor_precedence_killer_over_speaker,
    test_ek2_list_valued_participants_flatten_correctly,
    test_ek2_no_outward_effect_is_internal,
    # EK2 integration pins on the three dramatica-complete verifiers
    test_ek2_oedipus_verifier_both_characterizations_approved,
    test_ek2_macbeth_verifier_no_regression,
    test_ek2_ackroyd_verifier_be_er_inversion_preserved,
    # dramatica-complete → substrate verifier surface extension
    test_verifier_surface_has_eight_checks_per_encoding,
    test_oedipus_story_consequence_averted_at_end,
    test_macbeth_story_goal_three_phase_kingship,
    test_macbeth_dsp_growth_monotonic_killing,
    test_ackroyd_resolve_steadfast_lands_before_investigation_arc,
    test_ackroyd_growth_start_after_ultimatum,
    test_ackroyd_story_consequence_approved_after_ralph_cleared_fix,
    # LT2 / LT3 classifier (pressure-shape-taxonomy-sketch-01)
    test_lt2_empty_fabula_is_timelock_consistent,
    test_lt2_retraction_signal_alone,
    test_lt2_retraction_without_prior_assertion_does_not_fire,
    test_lt2_identity_resolution_via_world_effect,
    test_lt2_identity_resolution_via_knowledge_effect,
    test_lt2_rule_emergence_signal_alone,
    test_lt2_rule_emergence_fires_when_compound_also_authored,
    test_lt2_all_three_kinds_firing_gives_strength_one,
    test_lt2_oedipus_fabula_classifies_optionlock,
    test_lt2_macbeth_fabula_classifies_optionlock,
    test_lt2_ackroyd_fabula_classifies_optionlock,
    test_lt2_rocky_substrate_shows_mild_convergence_not_clean_timelock,
    test_rocky_went_the_distance_rule_derives_at_fight_end,
    test_rocky_has_no_identity_propositions,
    test_lt5_timelock_declared_on_timelock_consistent_substrate_is_noted,
    test_lt5_optionlock_declared_on_optionlock_substrate_is_approved,
    test_lt5_optionlock_declared_on_timelock_consistent_substrate_is_needs_work,
    # LT2 integration pins on the three dramatica-complete verifiers
    test_lt_verifier_surface_has_nine_checks_per_encoding,
    test_lt_oedipus_dsp_limit_approved_with_two_signal_kinds,
    test_lt_macbeth_dsp_limit_approved_with_two_signal_kinds,
    test_lt_ackroyd_dsp_limit_approved_with_two_signal_kinds,
    # Rocky Phase 2 integration pins
    test_rocky_verifier_has_nine_checks,
    test_rocky_dsp_limit_needs_work_on_timelock_declaration,
    test_rocky_dsp_outcome_failure_approved,
    test_rocky_dsp_judgment_good_positive_closure_cluster,
    test_rocky_dsp_resolve_steadfast_via_structural_invariance,
    test_rocky_dsp_growth_start_via_articulated_goal_acquisition,
    test_rocky_all_characterization_and_claim_checks_except_dsp_limit_approved,
    test_oedipus_dsp_growth_partial_rate_heuristic,
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
