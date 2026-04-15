"""
ackroyd_verification.py — third concrete cross-boundary verifier:
Ackroyd Dramatic → substrate.

Companion to oedipus_verification.py and macbeth_verification.py.
Same V3 trio (Characterization, Claim-trajectory, Claim-moment),
third story. Imports from substrate.py + ackroyd.py + dramatic.py +
ackroyd_dramatic.py + lowering.py + ackroyd_lowerings.py +
verification.py + verifier_helpers.py simultaneously.

Where Oedipus stresses identity collapse and Macbeth stresses moral
derivation + prophecy reinterpretation, Ackroyd stresses the
**MC-Antagonist alignment** on C_sheppard and the **epistemic
recovery** the Argument claims. The three checks exercise each:

- **Characterization on T_mc_sheppard.** Same main-character-
  Throughline shape as Oedipus and Macbeth. The non-trivial
  question: does Sheppard (owner C_sheppard, lowers to entity
  'sheppard') appear as participant in all of the lowered events?
  Answer: yes — Sheppard is in every lowered event on the MC
  Throughline (blackmail through suicide, 13 events). The
  MC-is-Antagonist alignment doesn't change this; it adds a
  function_label but leaves the owner-presence invariant intact.

- **Claim-trajectory on A_truth_recovers (AFFIRM).** The Argument
  claims the truth is recoverable. The substrate should exhibit
  four trajectory signatures by τ_s=8 (Poirot's reveal):
    1. killed(sheppard, ackroyd) world-literal. The authored fact
       the case is ultimately about; resolves anyway, but testing
       it confirms the substrate's world-layer is in order.
    2. betrayer_of_trust(sheppard, ackroyd) world-derivable. The
       moral derivation from killed + patient_of.
    3. driver_of_suicide(sheppard, mrs_ferrars) world-derivable.
       The moral derivation from blackmailed + dead +
       death_was_suicide.
    4. Poirot holds killed(sheppard, ackroyd) at KNOWN. The
       epistemic-recovery signature: the truth is NOT just
       world-visible but is present in the investigator's KNOWN
       set. This is the AFFIRM resolution's load-bearing proof.
  All four compose with inference-01 via `world_holds_derived` /
  `project_knowledge`. Signature (4) uses agent-knowledge, not
  world-facts — the substrate's epistemic machinery is what
  carries the "truth recovered" claim semantically.

- **Claim-moment on S_poirot_reveal.result.** At τ_s=8
  (E_poirot_reveals_solution), four signatures should hold on the
  cast's epistemic state:
    1. Poirot holds killed(sheppard, ackroyd) at KNOWN.
    2. Caroline holds killed(sheppard, ackroyd) at KNOWN — the
       private family-member-as-public-witness signature.
    3. Inspector Raglan holds killed(sheppard, ackroyd) at KNOWN —
       institutional knowledge, the legal consequence starts here.
    4. Flora holds killed(sheppard, ackroyd) at KNOWN — the
       Emotion function's engine resolves (Ralph is cleared;
       Flora now knows who actually did it).
  The signatures collectively demonstrate that the reveal moment
  updates the full cast's KNOWN sets simultaneously — which is
  the drawing-room-scene's structural purpose.

Per V6, the Claim-trajectory and Claim-moment checks compose with
inference-01: `world_holds_derived` drives the rule engine for the
moral-derivation signatures; `project_knowledge` drives the epistemic
projection for the Poirot / Caroline / Raglan / Flora signatures.
"""

from __future__ import annotations

# Substrate-side imports.
from substrate import (
    Entity, Event, CANONICAL,
    project_knowledge, project_world, in_scope,
    world_holds_derived, world_holds_literal,
    Slot,
)
from ackroyd import (
    FABULA, ENTITIES, ALL_BRANCHES, RULES,
    killed, dead, betrayer_of_trust, driver_of_suicide,
)

# Dramatic-side imports.
from dramatic import Throughline, Character
from ackroyd_dramatic import (
    THROUGHLINES, CHARACTERS, STORY,
    ARGUMENTS, SCENES, BEATS, STAKES,
)
from dramatic import COUPLING_DECLARATIONS

# Lowering-side imports.
from lowering import (
    CrossDialectRef, cross_ref,
    Lowering, LoweringStatus, by_status,
)
from ackroyd_lowerings import LOWERINGS

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

# Shared cross-boundary verifier helpers.
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
# Characterization check: main-character Throughline (T_mc_sheppard)
# ============================================================================


def main_character_throughline_check(
    upper_ref: CrossDialectRef,
    lower_refs: tuple,
) -> tuple:
    """Characterization check for a main-character Throughline.
    Returns (verdict, match_strength, comment).

    For Ackroyd: T_mc_sheppard's owner C_sheppard lowers to entity
    'sheppard'; the L_mc_throughline Lowering names 13 substrate
    events spanning [-18, 11]. Sheppard participates in all 13 —
    from deducing Mrs. Ferrars' poisoning (the arc's start) through
    his own death. Expected verdict APPROVED with match_strength=1.0.
    """
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
# Claim-trajectory check: A_truth_recovers
# ============================================================================


def truth_recovers_argument_check(
    upper_ref, lower_refs, position_ranges,
):
    """Trajectory check for A_truth_recovers (resolution=AFFIRM).
    Returns (verdict, match_strength, comment).

    Four signatures at τ_s=8 (Poirot's reveal):
      - killed(sheppard, ackroyd) world-literal
      - betrayer_of_trust(sheppard, ackroyd) world-derivable
      - driver_of_suicide(sheppard, mrs_ferrars) world-derivable
      - Poirot KNOWS killed(sheppard, ackroyd) — the
        epistemic-recovery signature; the Argument's AFFIRM
        resolution lives in the investigator's KNOWN set, not just
        in the world facts
    """
    # A_truth_recovers has no Lowering (Argument is a Claim coupling
    # per L1); check supplies its own τ_s.
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

    # The epistemic-recovery signature — Poirot's KNOWN set.
    poirot_state = project_knowledge(
        agent_id="poirot",
        events_in_scope=events_in_scope,
        up_to_τ_s=reveal_τ_s,
    )
    poirot_held = poirot_state.holds_literal(
        killed("sheppard", "ackroyd"),
    )
    poirot_knows = (
        poirot_held is not None and poirot_held.slot == Slot.KNOWN
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
        f"Argument A_truth_recovers (AFFIRM) trajectory at "
        f"τ_s={reveal_τ_s} (Poirot's reveal): "
        f"killed(sheppard, ackroyd) world-literal: "
        f"{killed_world}; "
        f"betrayer_of_trust(sheppard, ackroyd) derivable: "
        f"{betrayer_proof is not None}; "
        f"driver_of_suicide(sheppard, mrs_ferrars) derivable: "
        f"{driver_proof is not None}; "
        f"Poirot KNOWS killed(sheppard, ackroyd): {poirot_knows}; "
        f"{matched}/4 truth-recovery signatures present"
    )
    return (verdict, strength, comment)


# ============================================================================
# Claim-moment check: S_poirot_reveal.result
# ============================================================================


def poirot_reveal_scene_result_check(
    upper_ref, lower_refs, position_ranges,
):
    """Claim-moment check for S_poirot_reveal.result. Returns
    (verdict, match_strength, comment).

    Four moment signatures at τ_s=8 (E_poirot_reveals_solution):
      - Poirot holds killed(sheppard, ackroyd) at KNOWN
      - Caroline holds killed(sheppard, ackroyd) at KNOWN (family)
      - Inspector Raglan holds killed(sheppard, ackroyd) at KNOWN
        (institutional)
      - Flora holds killed(sheppard, ackroyd) at KNOWN (Emotion
        function's engine resolves)
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

    def _agent_knows_killing(agent_id: str) -> bool:
        state = project_knowledge(
            agent_id=agent_id,
            events_in_scope=events_in_scope,
            up_to_τ_s=max_τ_s,
        )
        held = state.holds_literal(killed("sheppard", "ackroyd"))
        return held is not None and held.slot == Slot.KNOWN

    poirot_knows = _agent_knows_killing("poirot")
    caroline_knows = _agent_knows_killing("caroline_sheppard")
    raglan_knows = _agent_knows_killing("inspector_raglan")
    flora_knows = _agent_knows_killing("flora_ackroyd")

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
        f"S_poirot_reveal result at τ_s={max_τ_s}: "
        f"poirot KNOWS killed(sheppard, ackroyd): {poirot_knows}; "
        f"caroline KNOWS: {caroline_knows}; "
        f"raglan KNOWS: {raglan_knows}; "
        f"flora KNOWS: {flora_knows}; "
        f"{matched}/4 cast-KNOWN-set signatures present"
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
        applies_to=lambda a: a.id == "A_truth_recovers",
        check_fn=truth_recovers_argument_check,
        description=(
            "A_truth_recovers (AFFIRM): killed + betrayer_of_trust + "
            "driver_of_suicide + Poirot-KNOWS-killed at τ_s=8"
        ),
    ),
    CheckRegistration(
        coupling_kind=COUPLING_CLAIM_MOMENT,
        record_type="Scene",
        field="result",
        applies_to=lambda s: s.id == "S_poirot_reveal",
        check_fn=poirot_reveal_scene_result_check,
        description=(
            "S_poirot_reveal result: cast KNOWN sets all updated "
            "with killed(sheppard, ackroyd) at τ_s=8"
        ),
    ),
)


RECORDS_BY_TYPE = {
    "Throughline": THROUGHLINES,
    "Argument": ARGUMENTS,
    "Scene": SCENES,
    # Beat and Stakes included so coverage_report sees them. The
    # orchestrator silently skips record_types with no matching
    # registration; the inclusion only affects the gap audit.
    "Beat": BEATS,
    "Stakes": STAKES,
}


def run() -> tuple:
    """Run all verifier checks for the Ackroyd encoding via the
    per-record-type orchestrator. Returns the verifier output tuple
    (mix of VerificationReview and StructuralAdvisory)."""
    return orchestrate_checks(
        records_by_type=RECORDS_BY_TYPE,
        registry=CHECK_REGISTRY,
        lowerings=LOWERINGS,
        record_dialect="dramatic",
        reviewed_at_τ_a=500,
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
