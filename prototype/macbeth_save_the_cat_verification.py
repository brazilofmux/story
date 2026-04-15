"""
macbeth_save_the_cat_verification.py — third concrete cross-boundary
verifier. Save the Cat → substrate on the Macbeth encoding.

Companion to oedipus_verification.py and macbeth_verification.py. Same
V3 orchestrator pattern, different dialect above the line. Imports
substrate.py + macbeth.py + save_the_cat.py + macbeth_save_the_cat.py
+ lowering.py + macbeth_save_the_cat_lowerings.py + verification.py.

Where macbeth_verification.py exercises three coupling kinds
(characterization, claim-trajectory, claim-moment) against the
Dramatic dialect's record types, this file exercises what Save the
Cat's coupling declarations actually support. The declarations in
save_the_cat.py are weighted differently: characterization is only
available on StcGenre.archetypes (and the Macbeth encoding's
declared Genre has no Lowering — genres are dialect-shipped data,
not authored records). The remaining declarations admit three
claim-trajectory checks and one claim-moment check, which is what
this module authors.

- **Claim-trajectory on Strand_A_scotland.description.** The A strand
  claims a political arc: loyal-thane → prophecy → regicide →
  usurpation → tyranny → overthrow → restoration. The substrate
  should exhibit four trajectory signatures across two τ_s
  projections: regicide + tyrant + dead(macbeth) at τ_s=17 (peak of
  the tyranny phase); king(malcolm, scotland) at τ_s=18 (the
  restoration endpoint). Why two projections: E_malcolm_crowned at
  τ_s=18 explicitly revokes king(macbeth, scotland) via
  `world(..., asserts=False)`, which unwinds the TYRANT_RULE
  derivation — honest substrate semantics, tested honestly. All
  derivable signatures compose with inference-01 via
  `world_holds_derived`.

- **Claim-trajectory on StcStory.theme_statement.** The theme is the
  Witches' "Fair is foul, and foul is fair" — an inversion claim.
  The substrate should exhibit four inversion signatures at τ_s=17
  (the phase where all four derivations hold simultaneously):
  breach_of_hospitality (fair-thane → foul-traitor), kinslayer
  (fair-kinsman → foul-killer), regicide (fair-subject → foul-
  regicide), tyrant (fair-king-promotion → foul-tyranny). Each is a
  derived fact — the theme's "inversion" claim is the substrate's
  rule chain turning fair-facts into foul-derivations. Note: the
  Story record has no Lowering; claim-trajectory runs anyway (the
  primitive does not require a Lowering, per V6) and the check
  supplies its own τ_s.

- **Claim-trajectory on Strand_B_marriage.description.** The B
  strand claims a marriage arc: partnership → conspiracy → unified
  execution → isolation → sleepwalking → death. The substrate
  should exhibit four signatures across τ_s ∈ [2, 14]: lady_macbeth
  participates in E_letter_to_lady_macbeth (opening); in
  E_sleepwalking (psyche-break); NOT in E_banquo_killed (the
  rupture; Macbeth acts without telling her); and dead(lady_macbeth)
  world-holds at τ_s=14 (terminus). Mixed positive/negative
  signature set — the rupture is signaled by absence, which the
  strand description explicitly names.

- **Claim-moment on B_14_finale.description_of_change.** B_14_finale
  lowers to E_macduff_reveals_birth (τ_s=17) and E_macbeth_killed
  (τ_s=17). At that moment, four signatures should hold: Macbeth
  holds born_not_of_woman(macduff) at KNOWN (the reveal); Macbeth no
  longer holds the prophecy-of-protection (the dislodgement);
  dead(macbeth) world-literal; tyrant(macbeth) world-derivable.
  Direct parallel to macbeth_verification's S_macbeth_dies check —
  same substrate moment, different upper dialect. The cross-dialect
  comparison sketch predicted this convergence: two dialects reading
  the same substrate moment should produce checks of the same shape
  when both describe the same event-set.

Expected verifier output at τ_a=400: 4 REVIEWs, all APPROVED at
match_strength=1.0. Coverage: 14 gaps (all on StcBeat.
description_of_change — one beat covered, 14 others not; candidates
for burndown when prioritized).
"""

from __future__ import annotations

# Substrate-side imports.
from substrate import (
    Entity, Event, CANONICAL,
    project_knowledge, project_world, in_scope,
    world_holds_derived, world_holds_literal,
    Slot,
)
from macbeth import (
    FABULA, ENTITIES, ALL_BRANCHES, RULES,
    tyrant, kinslayer, regicide, breach_of_hospitality,
    dead, born_not_of_woman, king,
    prophecy_none_of_woman_born_shall_harm,
)

# Save the Cat-side imports.
from save_the_cat import (
    StcBeat, StcStrand, StcStory,
    COUPLING_DECLARATIONS as STC_COUPLING_DECLARATIONS,
)
from macbeth_save_the_cat import (
    STORY, BEATS, STRANDS,
)

# Lowering-side imports.
from lowering import (
    CrossDialectRef, cross_ref,
    Lowering, LoweringStatus, by_status,
)
from macbeth_save_the_cat_lowerings import LOWERINGS

# Verifier primitive.
from verification import (
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


# ============================================================================
# Helpers
# ============================================================================


def _substrate_event(event_id: str) -> Event:
    for e in FABULA:
        if e.id == event_id:
            return e
    raise KeyError(event_id)


# ============================================================================
# Claim-trajectory check: Strand_A_scotland
# ============================================================================
#
# For the A strand ("loyal thane → prophecy → regicide → usurpation →
# tyranny → overthrow → restoration"), the substrate trajectory should
# exhibit four signatures, each at the τ_s where the phase lands:
#
#   1. regicide(macbeth, duncan) world-derivable at τ_s=17. The
#      depth-1 REGICIDE_RULE chains killed + king(duncan, _) from
#      τ_s=5 onward; the fact persists.
#   2. tyrant(macbeth) world-derivable at τ_s=17. The depth-2
#      TYRANT_RULE chains kinslayer + regicide + king(macbeth, _)
#      from τ_s=6 onward — and NOT at τ_s=18, because
#      E_malcolm_crowned explicitly revokes king(macbeth, scotland)
#      via `world(..., asserts=False)`, which unwinds the tyrant
#      derivation. Testing tyrant at the peak (τ_s=17) rather than at
#      the endpoint (τ_s=18) honors this: the A strand's arc INCLUDES
#      tyranny as a phase, not as a persistent endpoint property.
#   3. dead(macbeth) world-literal at τ_s=17. Authored by
#      E_macbeth_killed.
#   4. king(malcolm, scotland) world-literal at τ_s=18. Authored by
#      E_malcolm_crowned — the restoration the strand claims.
#
# Two substrate projections: one at τ_s=17 (peak tyranny) and one at
# τ_s=18 (restoration endpoint). Each signature drawn from the
# projection where its claim should hold.


def strand_a_scotland_trajectory_check(
    upper_ref, lower_refs, position_ranges,
):
    """Trajectory check for Strand_A_scotland.description. Returns
    (verdict, match_strength, comment).

    Four signatures across two substrate projections:
      at τ_s=17 (peak of tyranny phase):
        - regicide(macbeth, duncan) world-derivable
        - tyrant(macbeth) world-derivable
        - dead(macbeth) world-literal
      at τ_s=18 (restoration endpoint; position_range.max_value):
        - king(malcolm, scotland) world-literal
    """
    peak_τ_s = 17
    end_τ_s = 18
    if position_ranges:
        end_τ_s = max(pr.max_value for pr in position_ranges)

    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    world_facts_peak = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=peak_τ_s,
    )
    world_facts_end = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=end_τ_s,
    )

    regicide_proof = world_holds_derived(
        world_facts_peak, regicide("macbeth", "duncan"), RULES,
    )
    tyrant_proof = world_holds_derived(
        world_facts_peak, tyrant("macbeth"), RULES,
    )
    dead_macbeth = world_holds_literal(dead("macbeth"), world_facts_peak)
    king_malcolm = world_holds_literal(
        king("malcolm", "scotland"), world_facts_end,
    )

    signatures = [
        regicide_proof is not None,
        tyrant_proof is not None,
        dead_macbeth,
        king_malcolm,
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
        f"Strand_A_scotland trajectory (τ_s=17 peak, τ_s={end_τ_s} "
        f"endpoint): regicide(macbeth, duncan) world-derivable @17: "
        f"{regicide_proof is not None}; "
        f"tyrant(macbeth) world-derivable @17: "
        f"{tyrant_proof is not None}; "
        f"dead(macbeth) world-literal @17: {dead_macbeth}; "
        f"king(malcolm, scotland) world-literal @{end_τ_s}: "
        f"{king_malcolm}; "
        f"{matched}/4 political-arc signatures present"
    )
    return (verdict, strength, comment)


# ============================================================================
# Claim-trajectory check: theme_statement "Fair is foul, and foul is fair"
# ============================================================================
#
# The theme is an inversion claim. The substrate's depth-1 and depth-2
# rule chains turn loyal-thane / kinsman / subject / crowned-king
# facts into traitor / killer / regicide / tyrant derivations. That
# fact-to-derivation transit IS the inversion the theme claims.
#
# Four inversion signatures at τ_s ≤ 18:
#
#   1. breach_of_hospitality(macbeth, duncan) derivable — fair-thane
#      (host under whose roof the king slept) became foul-traitor
#      (the one who broke hospitality).
#   2. kinslayer(macbeth) derivable — fair-kinsman (macbeth
#      kinsman_of duncan) became foul-killer (the one who killed his
#      kin).
#   3. regicide(macbeth, duncan) derivable — fair-subject became foul-
#      regicide. (Same signature as Strand_A; different framing — here
#      it's an instance of the fair-to-foul transit.)
#   4. tyrant(macbeth) derivable — fair-king-promotion (the
#      prophecy's literal promise come true) became foul-tyranny (the
#      moral predicate Macbeth's cumulative actions earned).
#
# The theme_statement record has no Lowering — the Story record
# doesn't lower to the substrate directly in this encoding — so the
# check supplies its own max τ_s = 18.


def theme_statement_trajectory_check(
    upper_ref, lower_refs, position_ranges,
):
    """Trajectory check for StcStory.theme_statement ('Fair is foul,
    and foul is fair.'). Returns (verdict, match_strength, comment).

    Four inversion signatures verified at τ_s=17 (the phase where
    all four fair-to-foul derivations hold simultaneously; at τ_s=18
    the restoration revokes king(macbeth, scotland) and tyrant stops
    deriving):
      - breach_of_hospitality(macbeth, duncan) derivable
      - kinslayer(macbeth, duncan) derivable
      - regicide(macbeth, duncan) derivable
      - tyrant(macbeth) derivable
    """
    peak_τ_s = 17

    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    world_facts = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=peak_τ_s,
    )

    breach_proof = world_holds_derived(
        world_facts, breach_of_hospitality("macbeth", "duncan"), RULES,
    )
    kinslayer_proof = world_holds_derived(
        world_facts, kinslayer("macbeth", "duncan"), RULES,
    )
    regicide_proof = world_holds_derived(
        world_facts, regicide("macbeth", "duncan"), RULES,
    )
    tyrant_proof = world_holds_derived(
        world_facts, tyrant("macbeth"), RULES,
    )

    signatures = [
        breach_proof is not None,
        kinslayer_proof is not None,
        regicide_proof is not None,
        tyrant_proof is not None,
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
        f"theme_statement 'Fair is foul, and foul is fair' "
        f"trajectory at τ_s={peak_τ_s} (fair-to-foul inversion "
        f"signatures): "
        f"breach_of_hospitality(macbeth, duncan) derivable: "
        f"{breach_proof is not None}; "
        f"kinslayer(macbeth, duncan) derivable: "
        f"{kinslayer_proof is not None}; "
        f"regicide(macbeth, duncan) derivable: "
        f"{regicide_proof is not None}; "
        f"tyrant(macbeth) derivable: {tyrant_proof is not None}; "
        f"{matched}/4 inversion signatures present"
    )
    return (verdict, strength, comment)


# ============================================================================
# Claim-trajectory check: Strand_B_marriage
# ============================================================================
#
# For the B strand ("partnership → conspiracy → unified execution →
# isolation → sleepwalking → death"), the substrate trajectory should
# exhibit four signatures spanning the marriage's in-play lifespan
# (τ_s ∈ [2, 14], matching position_range). Each signature tests a
# different arc phase using participant-set and world-fact signals:
#
#   1. lady_macbeth is a participant in E_letter_to_lady_macbeth
#      (τ_s=2) — the arc's opening; she receives the prophecy and
#      chooses for both.
#   2. lady_macbeth is a participant in E_sleepwalking (τ_s=13) — the
#      psyche-break phase; conscience surfaces as compulsive speech.
#   3. lady_macbeth is NOT a participant in E_banquo_killed (τ_s=8) —
#      the rupture indicator; Macbeth acts without telling her. This
#      is the negative signature the strand description names
#      explicitly ("Macbeth acts without his wife").
#   4. dead(lady_macbeth) world-holds at τ_s=14 — the arc's terminus;
#      E_lady_macbeth_dies authors the fact.


def strand_b_marriage_trajectory_check(
    upper_ref, lower_refs, position_ranges,
):
    """Trajectory check for Strand_B_marriage.description. Returns
    (verdict, match_strength, comment).

    Four signatures across the marriage arc:
      - lady_macbeth in E_letter_to_lady_macbeth.participants (open)
      - lady_macbeth in E_sleepwalking.participants (psyche-break)
      - lady_macbeth NOT in E_banquo_killed.participants (rupture)
      - dead(lady_macbeth) world-literal at τ_s=14 (terminus)
    """
    end_τ_s = 14
    if position_ranges:
        end_τ_s = max(pr.max_value for pr in position_ranges)

    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    world_facts_end = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=end_τ_s,
    )

    def _participants(event_id: str) -> set:
        e = _substrate_event(event_id)
        out = set()
        for v in e.participants.values():
            if isinstance(v, str):
                out.add(v)
            elif isinstance(v, (list, tuple)):
                for item in v:
                    if isinstance(item, str):
                        out.add(item)
        return out

    letter_participants = _participants("E_letter_to_lady_macbeth")
    sleepwalk_participants = _participants("E_sleepwalking")
    banquo_participants = _participants("E_banquo_killed")

    opens_with_lm = "lady_macbeth" in letter_participants
    sleepwalk_focal = "lady_macbeth" in sleepwalk_participants
    rupture_excludes_lm = "lady_macbeth" not in banquo_participants
    lm_dead = world_holds_literal(dead("lady_macbeth"), world_facts_end)

    signatures = [
        opens_with_lm,
        sleepwalk_focal,
        rupture_excludes_lm,
        lm_dead,
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
        f"Strand_B_marriage trajectory (τ_s ∈ [2, {end_τ_s}]): "
        f"lady_macbeth in E_letter_to_lady_macbeth.participants "
        f"(opens): {opens_with_lm}; "
        f"lady_macbeth in E_sleepwalking.participants "
        f"(psyche-break): {sleepwalk_focal}; "
        f"lady_macbeth NOT in E_banquo_killed.participants "
        f"(rupture): {rupture_excludes_lm}; "
        f"dead(lady_macbeth) world-literal @{end_τ_s} "
        f"(terminus): {lm_dead}; "
        f"{matched}/4 marriage-arc signatures present"
    )
    return (verdict, strength, comment)


# ============================================================================
# Claim-moment check: B_14_finale.description_of_change
# ============================================================================
#
# B_14_finale lowers to E_macduff_reveals_birth (τ_s=17) and
# E_macbeth_killed (τ_s=17). At that moment, the substrate should
# exhibit four signatures — the same four the Dramatic encoding's
# S_macbeth_dies check exercises, because both dialects name the same
# substrate event-pair as the play's central-conflict-resolution
# moment. The cross-dialect comparison's convergence prediction made
# concrete.


def finale_beat_moment_check(
    upper_ref, lower_refs, position_ranges,
):
    """Claim-moment check for B_14_finale.description_of_change.
    Returns (verdict, match_strength, comment).

    Four moment signatures verified at the max τ_s of the Lowered
    substrate events (τ_s=17):
      - Macbeth holds born_not_of_woman(macduff) at KNOWN
      - Macbeth no longer holds prophecy_none_of_woman_born_shall_harm
      - dead(macbeth) world-literal
      - tyrant(macbeth) world-derivable
    """
    max_τ_s = 0
    for lr in lower_refs:
        if lr.dialect != "substrate":
            continue
        for e in FABULA:
            if e.id == lr.record_id:
                if e.τ_s > max_τ_s:
                    max_τ_s = e.τ_s

    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    state = project_knowledge(
        agent_id="macbeth",
        events_in_scope=events_in_scope,
        up_to_τ_s=max_τ_s,
    )
    world_facts = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=max_τ_s,
    )

    born_held = state.holds_literal(born_not_of_woman("macduff"))
    has_born_known = (
        born_held is not None and born_held.slot == Slot.KNOWN
    )
    prophecy_dislodged = (
        state.holds_literal(
            prophecy_none_of_woman_born_shall_harm("macbeth"),
        ) is None
    )
    dead_macbeth = world_holds_literal(dead("macbeth"), world_facts)
    tyrant_proof = world_holds_derived(
        world_facts, tyrant("macbeth"), RULES,
    )

    signatures = [
        has_born_known,
        prophecy_dislodged,
        dead_macbeth,
        tyrant_proof is not None,
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
        f"B_14_finale.description_of_change at τ_s={max_τ_s}: "
        f"macbeth holds born_not_of_woman(macduff) at KNOWN: "
        f"{has_born_known}; "
        f"prophecy_none_of_woman_born_shall_harm(macbeth) "
        f"dislodged from macbeth's held set: {prophecy_dislodged}; "
        f"dead(macbeth) world-literal: {dead_macbeth}; "
        f"tyrant(macbeth) world-derivable: "
        f"{tyrant_proof is not None}; "
        f"{matched}/{len(signatures)} moment signatures present"
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
        applies_to=lambda s: s.id == "Strand_A_scotland",
        check_fn=strand_a_scotland_trajectory_check,
        description=(
            "Strand_A_scotland: regicide + tyrant + dead(macbeth) + "
            "king(malcolm, scotland) derivable/holding at τ_s ≤ 18"
        ),
    ),
    CheckRegistration(
        coupling_kind=COUPLING_CLAIM_TRAJECTORY,
        record_type="StcStrand",
        field="description",
        applies_to=lambda s: s.id == "Strand_B_marriage",
        check_fn=strand_b_marriage_trajectory_check,
        description=(
            "Strand_B_marriage: lady_macbeth participant-set across "
            "letter/sleepwalking/banquo-killing + dead at τ_s=14"
        ),
    ),
    CheckRegistration(
        coupling_kind=COUPLING_CLAIM_TRAJECTORY,
        record_type="StcStory",
        field="theme_statement",
        applies_to=lambda s: s.id == "S_macbeth_stc",
        check_fn=theme_statement_trajectory_check,
        description=(
            "theme_statement 'Fair is foul, and foul is fair': four "
            "fair-to-foul inversion signatures derivable at τ_s ≤ 18"
        ),
    ),
    CheckRegistration(
        coupling_kind=COUPLING_CLAIM_MOMENT,
        record_type="StcBeat",
        field="description_of_change",
        applies_to=lambda b: b.id == "B_14_finale",
        check_fn=finale_beat_moment_check,
        description=(
            "B_14_finale: born_not_of_woman KNOWN + prophecy "
            "dislodged + dead + tyrant at τ_s=17"
        ),
    ),
)


RECORDS_BY_TYPE = {
    "StcStory": (STORY,),
    "StcBeat": BEATS,
    "StcStrand": STRANDS,
}


def run() -> tuple:
    """Run all verifier checks for the Macbeth-at-Save-the-Cat
    encoding via the per-record-type orchestrator. Returns the
    verifier output tuple (mix of VerificationReview and
    StructuralAdvisory)."""
    return orchestrate_checks(
        records_by_type=RECORDS_BY_TYPE,
        registry=CHECK_REGISTRY,
        lowerings=LOWERINGS,
        record_dialect="save-the-cat",
        reviewed_at_τ_a=400,
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
