"""
ackroyd_save_the_cat_verification.py — fourth cross-boundary
verifier. Save the Cat → substrate on the Ackroyd encoding.

Companion to macbeth_save_the_cat_verification.py. Same shape:
coupling declarations on the Save the Cat dialect admit
claim-trajectory on strands and theme + claim-moment on beats;
characterization is only available on StcGenre (which has no
Lowering, so no characterization check fires).

Four checks:

- **Claim-trajectory on Strand_A_case.description.** The case arc
  claims a trajectory from murder through investigation to
  identification. Substrate should exhibit four signatures at
  τ_s=8 (Poirot's reveal):
    1. killed(sheppard, ackroyd) world-literal — the case's
       central fact
    2. betrayer_of_trust(sheppard, ackroyd) world-derivable — the
       moral-derivation rule fires
    3. driver_of_suicide(sheppard, mrs_ferrars) world-derivable —
       the earlier moral fact, tying the case's pre-play rot to
       its reveal
    4. Poirot KNOWS killed(sheppard, ackroyd) — the
       investigation's epistemic output

- **Claim-trajectory on Strand_B_flora_ralph.description.** The
  love arc claims: engagement (pre-play) → secret marriage →
  disappearance-cum-accusation → vindication. Substrate should
  exhibit four signatures:
    1. secretly_married(ralph_paton, ursula_bourne) world-literal
       — the B arc's foundational fact
    2. accused_of_murder(ralph_paton, ackroyd) world-literal — the
       wrongful accusation that is the B story's external pressure
    3. flora_ackroyd in E_flora_summons_poirot.participants — her
       love drives the A engagement
    4. At τ_s=8, Poirot KNOWS secretly_married(ralph_paton,
       ursula_bourne) — the B story's clearing happens via Poirot's
       recovered knowledge of the secret

- **Claim-trajectory on StcStory.theme_statement.** "The truth will
  out." Four signatures of truth-recovered:
    1. betrayer_of_trust(sheppard, ackroyd) derivable — the moral
       truth
    2. driver_of_suicide(sheppard, mrs_ferrars) derivable — the
       second moral truth
    3. Poirot KNOWS killed(sheppard, ackroyd) — the investigator
       recovers the deed
    4. Caroline KNOWS killed(sheppard, ackroyd) — the family
       member, who started the novel not knowing her brother, ends
       it knowing. The Guardian function's bleak payoff

- **Claim-moment on B_14_finale.description_of_change.** At τ_s=8
  (E_poirot_reveals_solution), the cast's KNOWN sets update
  simultaneously. Four cast-knowledge signatures — exact parallel
  to the Dramatic dialect's S_poirot_reveal check. Two dialects
  exercising the same substrate moment with the same four
  signatures — the cross-dialect convergence noted in the Macbeth
  comparison, reaffirmed here.

Expected output: 4 REVIEWs, all APPROVED at match_strength=1.0.
"""

from __future__ import annotations

from story_engine.core.substrate import (
    Entity, Event, CANONICAL,
    project_knowledge, project_world, in_scope,
    world_holds_derived, world_holds_literal,
    Slot, Prop,
)
from story_engine.encodings.ackroyd import (
    FABULA, ENTITIES, ALL_BRANCHES, RULES,
    killed, dead, betrayer_of_trust, driver_of_suicide,
    secretly_married, accused_of_murder,
)

from story_engine.core.save_the_cat import (
    StcBeat, StcStrand, StcStory,
    COUPLING_DECLARATIONS as STC_COUPLING_DECLARATIONS,
)
from story_engine.encodings.ackroyd_save_the_cat import STORY, BEATS, STRANDS

from story_engine.core.lowering import (
    CrossDialectRef, cross_ref,
    Lowering, LoweringStatus, by_status,
)
from story_engine.encodings.ackroyd_save_the_cat_lowerings import LOWERINGS

from story_engine.core.verification import (
    VerificationReview, StructuralAdvisory,
    verify_characterization, verify_claim_trajectory,
    verify_claim_moment,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH,
    VERDICT_NOTED,
    CheckRegistration, orchestrate_checks,
    COUPLING_CHARACTERIZATION,
    COUPLING_CLAIM_TRAJECTORY,
    COUPLING_CLAIM_MOMENT,
    coverage_report, group_gaps_by_kind, group_gaps_by_record_type,
    reviews_only, group_by_verdict,
)

from story_engine.core.verifier_helpers import find_substrate_event, event_participants_flat


def _substrate_event(event_id: str) -> Event:
    return find_substrate_event(event_id, FABULA)


# ============================================================================
# Helpers shared across the four checks
# ============================================================================


def _agent_knows_at_known(
    agent_id: str, prop: Prop, up_to_τ_s: int,
) -> bool:
    """True iff agent_id holds prop at Slot.KNOWN at projection
    time up_to_τ_s. Used by both claim-trajectory and claim-moment
    checks that test epistemic-recovery signatures."""
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    state = project_knowledge(
        agent_id=agent_id,
        events_in_scope=events_in_scope,
        up_to_τ_s=up_to_τ_s,
    )
    held = state.holds_literal(prop)
    return held is not None and held.slot == Slot.KNOWN


# ============================================================================
# Claim-trajectory check: Strand_A_case
# ============================================================================


def strand_a_case_trajectory_check(
    upper_ref, lower_refs, position_ranges,
):
    """Trajectory check for Strand_A_case.description. Four signatures
    at τ_s=8 (Poirot's reveal)."""
    reveal_τ_s = 8

    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    world_facts = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=reveal_τ_s,
    )

    killed_world = world_holds_literal(
        killed("sheppard", "ackroyd"), world_facts,
    )
    betrayer_proof = world_holds_derived(
        world_facts, betrayer_of_trust("sheppard", "ackroyd"), RULES,
    )
    driver_proof = world_holds_derived(
        world_facts,
        driver_of_suicide("sheppard", "mrs_ferrars"),
        RULES,
    )
    poirot_knows = _agent_knows_at_known(
        "poirot", killed("sheppard", "ackroyd"), reveal_τ_s,
    )

    signatures = [
        killed_world,
        betrayer_proof is not None,
        driver_proof is not None,
        poirot_knows,
    ]
    matched = sum(signatures)
    strength = matched / len(signatures)

    if strength >= 0.99:
        verdict = VERDICT_APPROVED
    elif strength >= 0.5:
        verdict = VERDICT_PARTIAL_MATCH
    else:
        verdict = VERDICT_NEEDS_WORK

    comment = (
        f"Strand_A_case trajectory at τ_s={reveal_τ_s}: "
        f"killed(sheppard, ackroyd) world-literal: {killed_world}; "
        f"betrayer_of_trust derivable: "
        f"{betrayer_proof is not None}; "
        f"driver_of_suicide derivable: {driver_proof is not None}; "
        f"Poirot KNOWS killed: {poirot_knows}; "
        f"{matched}/4 case-arc signatures present"
    )
    return (verdict, strength, comment)


# ============================================================================
# Claim-trajectory check: Strand_B_flora_ralph
# ============================================================================


def strand_b_flora_ralph_trajectory_check(
    upper_ref, lower_refs, position_ranges,
):
    """Trajectory check for Strand_B_flora_ralph.description. Four
    signatures across the love arc; last is epistemic at τ_s=8.

    Note: the `accused_of_murder` signature is probed at τ_s=7 (the
    pre-reveal moment) because the reveal event at τ_s=8 now
    explicitly retracts the accusation (ackroyd.py substrate fix
    closing the Story_consequence partial finding). The trajectory
    semantics are preserved — "Ralph was accused during the
    investigation" — by querying at the latest τ_s before the
    reveal's retraction."""
    reveal_τ_s = 8
    pre_reveal_τ_s = 7

    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    world_facts_reveal = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=reveal_τ_s,
    )
    world_facts_pre_reveal = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=pre_reveal_τ_s,
    )

    married_fact = world_holds_literal(
        secretly_married("ralph_paton", "ursula_bourne"),
        world_facts_reveal,
    )
    accused_fact = world_holds_literal(
        accused_of_murder("ralph_paton", "ackroyd"),
        world_facts_pre_reveal,
    )

    summons_event = _substrate_event("E_flora_summons_poirot")
    flora_in_summons = (
        "flora_ackroyd" in event_participants_flat(summons_event)
    )

    poirot_knows_marriage = _agent_knows_at_known(
        "poirot",
        secretly_married("ralph_paton", "ursula_bourne"),
        reveal_τ_s,
    )

    signatures = [
        married_fact,
        accused_fact,
        flora_in_summons,
        poirot_knows_marriage,
    ]
    matched = sum(signatures)
    strength = matched / len(signatures)

    if strength >= 0.99:
        verdict = VERDICT_APPROVED
    elif strength >= 0.5:
        verdict = VERDICT_PARTIAL_MATCH
    else:
        verdict = VERDICT_NEEDS_WORK

    comment = (
        f"Strand_B_flora_ralph trajectory (τ_s=-10 through "
        f"τ_s={reveal_τ_s}): "
        f"secretly_married(ralph_paton, ursula_bourne) world-"
        f"literal: {married_fact}; "
        f"accused_of_murder(ralph_paton, ackroyd) at τ_s="
        f"{pre_reveal_τ_s}: {accused_fact}; "
        f"flora_ackroyd in E_flora_summons_poirot.participants: "
        f"{flora_in_summons}; "
        f"Poirot KNOWS secretly_married(ralph, ursula) at "
        f"τ_s={reveal_τ_s}: {poirot_knows_marriage}; "
        f"{matched}/4 love-arc signatures present"
    )
    return (verdict, strength, comment)


# ============================================================================
# Claim-trajectory check: theme_statement "The truth will out"
# ============================================================================


def theme_statement_trajectory_check(
    upper_ref, lower_refs, position_ranges,
):
    """Trajectory check for StcStory.theme_statement. Four signatures
    of truth-recovered at τ_s=8."""
    reveal_τ_s = 8

    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    world_facts = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=reveal_τ_s,
    )

    betrayer_proof = world_holds_derived(
        world_facts, betrayer_of_trust("sheppard", "ackroyd"), RULES,
    )
    driver_proof = world_holds_derived(
        world_facts,
        driver_of_suicide("sheppard", "mrs_ferrars"),
        RULES,
    )
    poirot_knows = _agent_knows_at_known(
        "poirot", killed("sheppard", "ackroyd"), reveal_τ_s,
    )
    caroline_knows = _agent_knows_at_known(
        "caroline_sheppard", killed("sheppard", "ackroyd"), reveal_τ_s,
    )

    signatures = [
        betrayer_proof is not None,
        driver_proof is not None,
        poirot_knows,
        caroline_knows,
    ]
    matched = sum(signatures)
    strength = matched / len(signatures)

    if strength >= 0.99:
        verdict = VERDICT_APPROVED
    elif strength >= 0.5:
        verdict = VERDICT_PARTIAL_MATCH
    else:
        verdict = VERDICT_NEEDS_WORK

    comment = (
        f"theme_statement 'The truth will out' trajectory at "
        f"τ_s={reveal_τ_s}: "
        f"betrayer_of_trust derivable: "
        f"{betrayer_proof is not None}; "
        f"driver_of_suicide derivable: {driver_proof is not None}; "
        f"Poirot KNOWS killed(sheppard, ackroyd): {poirot_knows}; "
        f"Caroline KNOWS killed(sheppard, ackroyd): "
        f"{caroline_knows}; "
        f"{matched}/4 truth-recovered signatures present"
    )
    return (verdict, strength, comment)


# ============================================================================
# Claim-moment check: B_14_finale.description_of_change
# ============================================================================


def finale_beat_moment_check(
    upper_ref, lower_refs, position_ranges,
):
    """Claim-moment check for B_14_finale. Same four cast-KNOWN-set
    signatures as the Dramatic dialect's S_poirot_reveal check: two
    dialects, same substrate moment, same four signatures. The
    cross-dialect convergence."""
    max_τ_s = 0
    for lr in lower_refs:
        if lr.dialect != "substrate":
            continue
        for e in FABULA:
            if e.id == lr.record_id:
                if e.τ_s > max_τ_s:
                    max_τ_s = e.τ_s

    poirot_knows = _agent_knows_at_known(
        "poirot", killed("sheppard", "ackroyd"), max_τ_s,
    )
    caroline_knows = _agent_knows_at_known(
        "caroline_sheppard", killed("sheppard", "ackroyd"), max_τ_s,
    )
    raglan_knows = _agent_knows_at_known(
        "inspector_raglan", killed("sheppard", "ackroyd"), max_τ_s,
    )
    flora_knows = _agent_knows_at_known(
        "flora_ackroyd", killed("sheppard", "ackroyd"), max_τ_s,
    )

    signatures = [
        poirot_knows, caroline_knows, raglan_knows, flora_knows,
    ]
    matched = sum(signatures)
    strength = matched / len(signatures)

    if strength >= 0.99:
        verdict = VERDICT_APPROVED
    elif strength >= 0.5:
        verdict = VERDICT_PARTIAL_MATCH
    else:
        verdict = VERDICT_NEEDS_WORK

    comment = (
        f"B_14_finale at τ_s={max_τ_s}: "
        f"poirot KNOWS killed(sheppard, ackroyd): {poirot_knows}; "
        f"caroline KNOWS: {caroline_knows}; "
        f"raglan KNOWS: {raglan_knows}; "
        f"flora KNOWS: {flora_knows}; "
        f"{matched}/4 reveal-cast-KNOWN signatures present"
    )
    return (verdict, strength, comment)


# ============================================================================
# Driver — run the checks
# ============================================================================


CHECK_REGISTRY = (
    CheckRegistration(
        coupling_kind=COUPLING_CLAIM_TRAJECTORY,
        record_type="StcStrand",
        field="description",
        applies_to=lambda s: s.id == "Strand_A_case",
        check_fn=strand_a_case_trajectory_check,
        description=(
            "Strand_A_case: killed + betrayer + driver + "
            "Poirot-KNOWS-killed at τ_s=8"
        ),
    ),
    CheckRegistration(
        coupling_kind=COUPLING_CLAIM_TRAJECTORY,
        record_type="StcStrand",
        field="description",
        applies_to=lambda s: s.id == "Strand_B_flora_ralph",
        check_fn=strand_b_flora_ralph_trajectory_check,
        description=(
            "Strand_B_flora_ralph: secret-marriage + accusation + "
            "flora-commissions + Poirot-KNOWS-marriage at τ_s=8"
        ),
    ),
    CheckRegistration(
        coupling_kind=COUPLING_CLAIM_TRAJECTORY,
        record_type="StcStory",
        field="theme_statement",
        applies_to=lambda s: s.id == "S_ackroyd_stc",
        check_fn=theme_statement_trajectory_check,
        description=(
            "theme_statement 'The truth will out': four truth-"
            "recovered signatures at τ_s=8"
        ),
    ),
    CheckRegistration(
        coupling_kind=COUPLING_CLAIM_MOMENT,
        record_type="StcBeat",
        field="description_of_change",
        applies_to=lambda b: b.id == "B_14_finale",
        check_fn=finale_beat_moment_check,
        description=(
            "B_14_finale: cast KNOWN sets all updated with "
            "killed(sheppard, ackroyd) at τ_s=8"
        ),
    ),
)


RECORDS_BY_TYPE = {
    "StcStory": (STORY,),
    "StcBeat": BEATS,
    "StcStrand": STRANDS,
}


def run() -> tuple:
    """Run all Save the Cat verifier checks for the Ackroyd
    encoding."""
    return orchestrate_checks(
        records_by_type=RECORDS_BY_TYPE,
        registry=CHECK_REGISTRY,
        lowerings=LOWERINGS,
        record_dialect="save-the-cat",
        reviewed_at_τ_a=600,
    )


if __name__ == "__main__":
    results = run()
    print(f"Verifier: {len(results)} results")
    print()
    for r in results:
        if isinstance(r, VerificationReview):
            print(f"  REVIEW [{r.verdict}] target={r.target_record}")
            print(f"    reviewer: {r.reviewer_id}")
            if r.match_strength is not None:
                print(f"    match_strength: {r.match_strength:.2f}")
            print(f"    anchor_τ_a: {r.anchor_τ_a}")
            print(f"    comment: {r.comment}")
        elif isinstance(r, StructuralAdvisory):
            print(f"  ADVISORY [{r.severity}] scope={r.scope}")
            print(f"    {r.comment}")
        print()

    gaps = coverage_report(
        records_by_type=RECORDS_BY_TYPE,
        registry=CHECK_REGISTRY,
        coupling_declarations=STC_COUPLING_DECLARATIONS,
    )
    print(f"Coverage: {len(gaps)} gaps "
          f"(declarations with no registered check)")
    if gaps:
        print("  by kind:")
        for kind, group in group_gaps_by_kind(gaps).items():
            if group:
                print(f"    {kind:<22} {len(group)}")
        print("  by record_type:")
        for rt, group in group_gaps_by_record_type(gaps).items():
            print(f"    {rt:<22} {len(group)}")
