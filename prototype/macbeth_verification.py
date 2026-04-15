"""
macbeth_verification.py — second concrete cross-boundary verifier
runs against the Macbeth encoding.

Companion to oedipus_verification.py. Same V3 trio (Characterization,
Claim-trajectory, Claim-moment), different play. Imports from
substrate.py + macbeth.py + dramatic.py + macbeth_dramatic.py +
lowering.py + macbeth_lowerings.py + verification.py simultaneously.

Where Oedipus stresses identity collapse (the substrate's identity
equivalence-class machinery, the gap_real_parents GAP), Macbeth
stresses moral derivation (the four-rule chain that turns
killed/kinsman/king/guest into kinslayer/regicide/breach/tyrant) and
prophecy reinterpretation (the dislodgement of a previously-KNOWN
prophecy when its protective reading collapses). The three checks
exercise both registers:

- Characterization on T_mc_macbeth — the same shape as the Oedipus
  check, but verifying a more action-saturated MC (Macbeth participates
  in even more of his lowered events than Oedipus does in his).
- Claim-trajectory on A_ambition_unmakes (resolution=AFFIRM) — three
  trajectory signatures the substrate must exhibit by τ_s=17 for the
  "ambition unmakes" premise to land: the moral collapse (tyrant),
  the literal unmaking (dead), the inflection point (breach of
  hospitality on the first ambitious act). All three lean on the
  inference engine: the compound predicates are no longer authored
  facts under inference-02, they derive via RULES.
- Claim-moment on S_macbeth_dies — four moment signatures at the
  battlefield: the prophecy's last protection collapses, the killing
  lands, the tyrant predicate still derives (he was overthrown *as*
  tyrant). Mirrors the oedipus_verification anagnorisis check in
  shape; differs in content (no identity-collapse signatures because
  Macbeth's anagnorisis is moral/strategic, not epistemic-of-self).

Per V6, the Claim-trajectory and Claim-moment checks compose with
inference-01: they call `world_holds_derived` against the substrate's
RULES tuple so the depth-1 and depth-2 rule chains participate in the
verification.
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
    dead, born_not_of_woman,
    prophecy_none_of_woman_born_shall_harm,
)

# Dramatic-side imports.
from dramatic import Throughline, Character
from macbeth_dramatic import THROUGHLINES, CHARACTERS, STORY

# Lowering-side imports.
from lowering import (
    CrossDialectRef, cross_ref,
    Lowering, LoweringStatus, by_status,
)
from macbeth_lowerings import LOWERINGS

# Verifier primitive.
from verification import (
    VerificationReview, StructuralAdvisory,
    verify_characterization, run_characterization_checks,
    verify_claim_trajectory, run_claim_trajectory_checks,
    verify_claim_moment, run_claim_moment_checks,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH,
    VERDICT_NOTED,
    CheckRegistration, orchestrate_checks,
    COUPLING_CHARACTERIZATION,
    COUPLING_CLAIM_TRAJECTORY,
    COUPLING_CLAIM_MOMENT,
    coverage_report, group_gaps_by_kind, group_gaps_by_record_type,
    reviews_only, group_by_verdict,
)
from macbeth_dramatic import ARGUMENTS, SCENES, BEATS, STAKES
from dramatic import COUPLING_DECLARATIONS

# Shared cross-boundary verifier helpers (extracted per REVIEW.md
# Finding 3 once the third encoding's verifier landed).
from verifier_helpers import (
    find_substrate_event,
    find_throughline,
    is_abstract_throughline_owner,
    event_participants_flat,
    entity_id_for_character,
)


# ============================================================================
# Encoding-bound helper closures
# ============================================================================


def _throughline(throughline_id: str) -> Throughline:
    return find_throughline(throughline_id, THROUGHLINES)


def _substrate_event(event_id: str) -> Event:
    return find_substrate_event(event_id, FABULA)


def _is_abstract_owner(owner_id: str) -> bool:
    return is_abstract_throughline_owner(owner_id)


def _entity_id_for_character(character_id: str, lowerings: tuple) -> str:
    return entity_id_for_character(character_id, lowerings, ENTITIES)


def _event_participants_flat(event: Event) -> set:
    return event_participants_flat(event)


# ============================================================================
# Characterization check: main-character Throughline
# ============================================================================
#
# Same shape as oedipus_verification.main_character_throughline_check
# — for a Throughline whose role_label is 'main-character', verify
# the owner Character's lowered Entity appears as participant in
# most/all of the lowered substrate events.
#
# Macbeth-side note: T_mc_macbeth's owner is C_macbeth, which lowers
# to entity 'macbeth'. The L_mc_throughline binding lists 13 events;
# Macbeth participates in nearly all of them (he's absent only from
# events that center other agents, but in the L_mc_throughline list
# every entry is one he's directly in). Expected verdict: APPROVED
# with match_strength=1.0.


def main_character_throughline_check(
    upper_ref: CrossDialectRef,
    lower_refs: tuple,
) -> tuple:
    """Characterization check for a main-character Throughline.
    Returns (verdict, match_strength, comment)."""
    throughline = _throughline(upper_ref.record_id)

    if throughline.role_label != "main-character":
        return (
            VERDICT_NOTED,
            None,
            (f"check applies to main-character Throughlines; "
             f"this one is {throughline.role_label!r}"),
        )

    owner_chars = [
        o for o in throughline.owners if not _is_abstract_owner(o)
    ]
    if not owner_chars:
        return (
            VERDICT_NOTED,
            None,
            "no concrete owner Characters; check skipped",
        )

    owner_entity_ids = []
    for char_id in owner_chars:
        entity_id = _entity_id_for_character(char_id, LOWERINGS)
        if entity_id is not None:
            owner_entity_ids.append(entity_id)

    if not owner_entity_ids:
        return (
            VERDICT_NOTED,
            None,
            (f"owner Characters {owner_chars} have no ACTIVE "
             f"Character→Entity Lowerings; check cannot evaluate"),
        )

    event_lower_refs = [
        lr for lr in lower_refs
        if lr.dialect == "substrate"
        and any(e.id == lr.record_id for e in FABULA)
    ]
    if not event_lower_refs:
        return (
            VERDICT_NOTED,
            None,
            "no substrate events in lower side",
        )

    matched = 0
    for lr in event_lower_refs:
        event = _substrate_event(lr.record_id)
        participants = _event_participants_flat(event)
        if any(eid in participants for eid in owner_entity_ids):
            matched += 1

    strength = matched / len(event_lower_refs)
    if strength >= 0.95:
        verdict = VERDICT_APPROVED
    elif strength >= 0.5:
        verdict = VERDICT_PARTIAL_MATCH
    else:
        verdict = VERDICT_NEEDS_WORK

    comment = (
        f"main-character Throughline {throughline.id!r}: owner "
        f"Character(s) {owner_chars} lower to substrate "
        f"Entity(ies) {owner_entity_ids}; "
        f"{matched}/{len(event_lower_refs)} of the "
        f"Lowered substrate events have at least one owner Entity "
        f"as a participant"
    )
    return (verdict, strength, comment)


# ============================================================================
# Claim-trajectory check: A_ambition_unmakes
# ============================================================================
#
# For Macbeth's Argument A_ambition_unmakes (premise: 'unchecked
# ambition unmakes the one who indulges it', resolution_direction=
# AFFIRM), the substrate trajectory should exhibit, by τ_s=17 (the
# overthrow):
#
#   1. tyrant(macbeth) is world-derivable. The depth-2 TYRANT_RULE
#      chains kinslayer + regicide + king(macbeth, _); all three
#      premises become available between τ_s=5 (the killing) and
#      τ_s=6 (the coronation). This signature carries the moral
#      register of "ambition unmakes" — Macbeth's ambition turned him
#      into the moral category his own actions made unavoidable.
#   2. dead(macbeth) holds in the substrate world. This is the
#      literal unmaking — authored at τ_s=17 by E_macbeth_killed.
#      The Argument's premise resolves AFFIRM not just morally but
#      materially.
#   3. breach_of_hospitality(macbeth, duncan) is world-derivable.
#      This is the inflection-point signature — the first ambitious
#      act broke the deepest available bond (king + kinsman + guest
#      under his roof). The depth-1 BREACH_OF_HOSPITALITY_RULE fires
#      from killed(macbeth, duncan) + guest_of(duncan, macbeth) at
#      τ_s=5.
#
# All three signatures lean on the inference engine — none of these
# compound predicates are authored facts under inference-02; they all
# derive via RULES. The check uses `world_holds_derived` so the rule
# engine participates.
#
# As with the Oedipus Argument check, A_ambition_unmakes has NO
# Lowering — Argument is a Claim coupling per L1, and Lowering is
# reserved for Realization. The Claim-trajectory primitive runs
# anyway; the check supplies its own substrate scope (τ_s ≤ 17).


def ambition_unmakes_argument_check(
    upper_ref, lower_refs, position_ranges,
):
    """Trajectory check for A_ambition_unmakes (resolution=AFFIRM).
    Returns (verdict, match_strength, comment).

    Three trajectory signatures verified at τ_s ≤ 17 (Macbeth's
    death):
      - tyrant(macbeth) world-derivable
      - dead(macbeth) world-true
      - breach_of_hospitality(macbeth, duncan) world-derivable

    Match strength = signatures-passing / 3.
    Verdict: approved if all three; partial-match if 2; needs-work if
    fewer.
    """
    # The trajectory scope. Default to τ_s=17 (Macbeth's death) but
    # use the position_range if one was authored on a Lowering (no
    # Lowering exists for the Argument in this encoding, so this
    # falls through to the default).
    max_τ_s = 17
    if position_ranges:
        max_τ_s = max(pr.max_value for pr in position_ranges)

    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    world_facts = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=max_τ_s,
    )

    tyrant_proof = world_holds_derived(
        world_facts, tyrant("macbeth"), RULES,
    )
    dead_macbeth = world_holds_literal(dead("macbeth"), world_facts)
    breach_proof = world_holds_derived(
        world_facts, breach_of_hospitality("macbeth", "duncan"), RULES,
    )

    signatures = [
        tyrant_proof is not None,
        dead_macbeth,
        breach_proof is not None,
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
        f"Argument 'unchecked ambition unmakes the one who indulges "
        f"it' (resolution=AFFIRM): trajectory check at τ_s ≤ "
        f"{max_τ_s} — "
        f"tyrant(macbeth) world-derivable: "
        f"{tyrant_proof is not None}; "
        f"dead(macbeth) world-true: {dead_macbeth}; "
        f"breach_of_hospitality(macbeth, duncan) world-derivable: "
        f"{breach_proof is not None}; "
        f"{matched}/3 trajectory signatures present"
    )
    return (verdict, strength, comment)


# ============================================================================
# Claim-moment check: S_macbeth_dies result
# ============================================================================
#
# S_macbeth_dies (narrative_position=13) claims at its `result` field:
# "Macbeth killed; the tyrant overthrown; the play's central conflict
# resolved." The Scene Lowers to two substrate events at τ_s=17:
# E_macduff_reveals_birth (the Caesarean reveal) and E_macbeth_killed
# (the killing). At that moment, the substrate should exhibit four
# signatures the realization performs:
#
#   1. Macbeth holds born_not_of_woman(macduff) at KNOWN. The reveal
#      is told_by Macduff to Macbeth at τ_s=17, slot=KNOWN; this is
#      the moment-defining epistemic update.
#   2. Macbeth no longer holds prophecy_none_of_woman_born_shall_harm
#      (the previously-KNOWN protection has been dislodged). At
#      τ_s=10 this prophecy was told_by Witches at KNOWN; at τ_s=17
#      E_macduff_reveals_birth issues a remove_held that takes it out
#      of his KNOWN set — the substrate's encoding of his realization
#      that his protective reading collapses.
#   3. dead(macbeth) holds in world. Authored at τ_s=17 by
#      E_macbeth_killed.
#   4. tyrant(macbeth) is world-derivable. The Scene's wording
#      ("the tyrant overthrown") presupposes he was a tyrant at the
#      moment of overthrow; the depth-2 TYRANT_RULE has been
#      derivable since τ_s=6, so this should hold.
#
# Signatures 1-2 are agent-knowledge facts on Macbeth; signatures 3-4
# are world facts (one literal, one derived). The check composes
# both registers.


def macbeth_dies_scene_result_check(
    upper_ref, lower_refs, position_ranges,
):
    """Claim-moment check for S_macbeth_dies.result. Returns
    (verdict, match_strength, comment).

    Four moment signatures verified at the max τ_s of the Lowered
    substrate events (τ_s=17 for both E_macduff_reveals_birth and
    E_macbeth_killed):
      - Macbeth holds born_not_of_woman(macduff) at KNOWN
      - Macbeth no longer holds prophecy_none_of_woman_born_shall_harm
      - dead(macbeth) holds in world
      - tyrant(macbeth) is world-derivable

    Match strength = signatures-passing / 4. Verdict: approved if all
    four; partial-match if 2-3; needs-work if fewer.
    """
    # Determine the moment from the lower records' max τ_s. For
    # S_macbeth_dies lowered to E_macduff_reveals_birth +
    # E_macbeth_killed, this is τ_s=17.
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

    # Signature 1: Macbeth holds born_not_of_woman(macduff) at KNOWN.
    born_held = state.holds_literal(born_not_of_woman("macduff"))
    has_born_known = (
        born_held is not None and born_held.slot == Slot.KNOWN
    )

    # Signature 2: Macbeth no longer holds the prophecy of protection.
    prophecy_dislodged = (
        state.holds_literal(
            prophecy_none_of_woman_born_shall_harm("macbeth"),
        ) is None
    )

    # Signature 3: dead(macbeth) world-true.
    dead_macbeth = world_holds_literal(dead("macbeth"), world_facts)

    # Signature 4: tyrant(macbeth) world-derivable.
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
        f"S_macbeth_dies result check at τ_s={max_τ_s}: "
        f"macbeth holds born_not_of_woman(macduff) at KNOWN: "
        f"{has_born_known}; "
        f"prophecy_none_of_woman_born_shall_harm(macbeth) "
        f"dislodged from macbeth's held set: {prophecy_dislodged}; "
        f"dead(macbeth) world-true: {dead_macbeth}; "
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
        coupling_kind=COUPLING_CHARACTERIZATION,
        record_type="Throughline",
        field="role_label",
        applies_to=lambda t: t.role_label == "main-character",
        check_fn=main_character_throughline_check,
        description=(
            "main-character Throughline: owner Character's substrate "
            "Entity must appear as participant in lowered events"
        ),
    ),
    CheckRegistration(
        coupling_kind=COUPLING_CLAIM_TRAJECTORY,
        record_type="Argument",
        field="resolution_direction",
        applies_to=lambda a: a.id == "A_ambition_unmakes",
        check_fn=ambition_unmakes_argument_check,
        description=(
            "A_ambition_unmakes (AFFIRM): tyrant + dead + breach "
            "derivable at τ_s ≤ 17"
        ),
    ),
    CheckRegistration(
        coupling_kind=COUPLING_CLAIM_MOMENT,
        record_type="Scene",
        field="result",
        applies_to=lambda s: s.id == "S_macbeth_dies",
        check_fn=macbeth_dies_scene_result_check,
        description=(
            "S_macbeth_dies result: born_not_of_woman KNOWN, prophecy "
            "dislodged, dead + tyrant world-true at τ_s=17"
        ),
    ),
)


RECORDS_BY_TYPE = {
    "Throughline": THROUGHLINES,
    "Argument": ARGUMENTS,
    "Scene": SCENES,
    # Beat and Stakes are included so coverage_report sees them. The
    # orchestrator silently skips record_types with no matching
    # registration; the inclusion only affects the gap audit.
    "Beat": BEATS,
    "Stakes": STAKES,
}


def run() -> tuple:
    """Run all verifier checks for the Macbeth encoding via the
    per-record-type orchestrator. Returns the verifier output tuple
    (mix of VerificationReview and StructuralAdvisory)."""
    return orchestrate_checks(
        records_by_type=RECORDS_BY_TYPE,
        registry=CHECK_REGISTRY,
        lowerings=LOWERINGS,
        record_dialect="dramatic",
        reviewed_at_τ_a=300,
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
        coupling_declarations=COUPLING_DECLARATIONS,
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
