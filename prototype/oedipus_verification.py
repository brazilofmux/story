"""
oedipus_verification.py — first concrete cross-boundary verifier
runs against the Oedipus encoding.

Imports from substrate.py + oedipus.py + dramatic.py +
oedipus_dramatic.py + lowering.py + oedipus_lowerings.py +
verification.py simultaneously. Like oedipus_lowerings.py, this
module is connective tissue — it brings dialects together to do
work neither dialect could do alone.

Scope of this first pass: one Characterization check on
T_mc_oedipus, the main-character Throughline. The check verifies
that the substrate events lowered from T_mc_oedipus actually have
Oedipus (the entity that C_oedipus lowers to) as a participant.
A "main-character" Throughline whose lowered events do not center
on the owner is mis-classified or has the wrong Lowering set;
either way the verifier should flag it. For Oedipus, all 10
events on the L_mc_throughline binding have Oedipus as a
participant, so we expect verdict=approved with match_strength=1.0.

Future verification work (other primitives, other checks, other
encodings) extends this pattern: each encoding pairs its dialect
records with check functions, and the verifier orchestrator runs
them and emits observations.
"""

from __future__ import annotations

# Substrate-side imports (for resolving Entity ids and Event
# participants).
from substrate import (
    Entity, Event, CANONICAL,
    project_knowledge, project_world, in_scope,
    world_holds_derived,
)
from oedipus import (
    FABULA, ENTITIES, ALL_BRANCHES, RULES,
    parricide, incest, identity_prop, gap_real_parents,
)
from substrate import Slot

# Dramatic-side imports (for resolving Throughline owners and
# Character ids).
from dramatic import Throughline, Character
from oedipus_dramatic import THROUGHLINES, CHARACTERS, STORY

# Lowering-side imports (for resolving owner Characters to
# substrate Entities).
from lowering import (
    CrossDialectRef, cross_ref,
    Lowering, LoweringStatus, by_status,
)
from oedipus_lowerings import LOWERINGS

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
from oedipus_dramatic import ARGUMENTS, SCENES, BEATS, STAKES
from dramatic import COUPLING_DECLARATIONS


# ============================================================================
# Helpers
# ============================================================================


def _throughline(throughline_id: str) -> Throughline:
    for t in THROUGHLINES:
        if t.id == throughline_id:
            return t
    raise KeyError(throughline_id)


def _substrate_event(event_id: str) -> Event:
    for e in FABULA:
        if e.id == event_id:
            return e
    raise KeyError(event_id)


def _is_abstract_owner(owner_id: str) -> bool:
    """Sentinel owner ids per dramatic.ABSTRACT_THROUGHLINE_OWNERS."""
    return owner_id in ("none", "the-situation", "the-relationship")


def _entity_id_for_character(character_id: str, lowerings: tuple) -> str:
    """Walk Lowerings to find the substrate Entity id that the given
    Dramatic Character lowers to. Returns the entity id string, or
    None if no ACTIVE Lowering exists or the lowering targets aren't
    substrate Entities."""
    char_ref = cross_ref("dramatic", character_id)
    for lw in lowerings:
        if lw.upper_record != char_ref:
            continue
        if lw.status != LoweringStatus.ACTIVE:
            continue
        for lr in lw.lower_records:
            if lr.dialect == "substrate":
                # Verify it's an Entity (vs. an Event); Entity ids
                # are lowercase agent names without an E_ prefix.
                if any(e.id == lr.record_id for e in ENTITIES):
                    return lr.record_id
    return None


def _event_participants_flat(event: Event) -> set:
    """Flatten an Event's participants dict into a set of entity ids.
    Substrate events sometimes use lists for participants like
    'targets'; this collapses those."""
    out = set()
    for v in event.participants.values():
        if isinstance(v, str):
            out.add(v)
        elif isinstance(v, (list, tuple)):
            for e in v:
                if isinstance(e, str):
                    out.add(e)
    return out


# ============================================================================
# Characterization check: main-character Throughline
# ============================================================================


def main_character_throughline_check(
    upper_ref: CrossDialectRef,
    lower_refs: tuple,
) -> tuple:
    """Characterization check for a Throughline whose role_label is
    'main-character'. The check verifies that the owner Character's
    lowered substrate Entity appears as a participant in most/all of
    the lowered substrate events.

    Returns (verdict, match_strength, comment). Verdicts:
      - 'approved' if ≥95% of events have the owner as participant
      - 'partial-match' if 50%-94%
      - 'needs-work' if <50%
      - 'noted' if the check can't be evaluated (no owner, no
        Entity Lowerings, no event lower records)
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
# Claim-trajectory check: the Argument's affirmation
# ============================================================================
#
# For Oedipus's Argument A_knowledge_unmakes (premise: 'knowledge of
# self is the unmaking of the self', resolution_direction=AFFIRM), the
# substrate trajectory should exhibit, by τ_s=13 (the anagnorisis):
#
#   1. Oedipus's identity equivalence class has expanded to include
#      the-exposed-baby (knowledge-of-self gained — he holds the
#      identity propositions linking himself to his exposed-infant
#      and crossroads-killer past).
#   2. parricide(oedipus, laius) is derivable in world (the moral
#      consequence of his action, derived via inference-01's
#      PARRICIDE_RULE from killed + child_of premises both world-
#      true since the canonical events).
#   3. incest(oedipus, jocasta) is derivable in world (the moral
#      consequence of his marriage, derived via INCEST_RULE).
#
# All three signatures are concrete, structurally-checkable facts
# the substrate carries (under inference-01, after the parricide /
# incest authored-compounds were retired). A trajectory-check
# verdict that affirms the premise requires all three. The check
# composes with inference-01 (V6) — it uses
# `world_holds_derived` rather than literal world membership so
# the rule engine's derivations participate.
#
# Note this check has NO Lowerings in oedipus_lowerings.py — Argument
# is a Claim coupling per the four-coupling-kinds framework
# (lowering-sketch-01 F1) and Lowering-record-sketch-01 L1 reserves
# Lowering for Realization. The Claim-trajectory primitive runs even
# without Lowerings; the check supplies its own substrate scope.


def knowledge_unmakes_argument_check(
    upper_ref, lower_refs, position_ranges,
):
    """Trajectory check for A_knowledge_unmakes (resolution=AFFIRM).
    Returns (verdict, match_strength, comment).

    Three trajectory signatures are checked at τ_s ≤ 13 (the
    anagnorisis):
      - Oedipus's identity equivalence class includes the-exposed-baby
      - parricide(oedipus, laius) is world-derivable
      - incest(oedipus, jocasta) is world-derivable

    Match strength = (signatures-passing) / 3.
    Verdict: approved if all three; partial-match if 2; needs-work if
    fewer.
    """
    # The trajectory scope. Default to τ_s=13 (anagnorisis) but use
    # the position_range if one was authored on a Lowering (no
    # Lowering exists for the Argument in this encoding, so this
    # falls through to the default).
    max_τ_s = 13
    if position_ranges:
        max_τ_s = max(pr.max_value for pr in position_ranges)

    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]

    # Signature 1: knowledge of self via identity equivalence class.
    state = project_knowledge(
        agent_id="oedipus",
        events_in_scope=events_in_scope,
        up_to_τ_s=max_τ_s,
    )
    classes = state.equivalence_classes()
    has_self_identity = any(
        "oedipus" in cls and "the-exposed-baby" in cls
        for cls in classes
    )

    # Signature 2 + 3: compound moral consequences derivable in world.
    world_facts = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=max_τ_s,
    )
    parricide_proof = world_holds_derived(
        world_facts, parricide("oedipus", "laius"), RULES,
    )
    incest_proof = world_holds_derived(
        world_facts, incest("oedipus", "jocasta"), RULES,
    )

    signatures = [
        has_self_identity,
        parricide_proof is not None,
        incest_proof is not None,
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
        f"Argument 'knowledge of self is the unmaking of the self' "
        f"(resolution=AFFIRM): trajectory check at τ_s ≤ {max_τ_s} — "
        f"identity collapse (oedipus + the-exposed-baby in same "
        f"equivalence class): {has_self_identity}; "
        f"parricide(oedipus, laius) world-derivable: "
        f"{parricide_proof is not None}; "
        f"incest(oedipus, jocasta) world-derivable: "
        f"{incest_proof is not None}; "
        f"{matched}/3 trajectory signatures present"
    )
    return (verdict, strength, comment)


# ============================================================================
# Claim-moment check: the anagnorisis Scene's result
# ============================================================================
#
# S_anagnorisis (narrative_position=7 in the Dramatic encoding)
# claims at its `result` field: "the Argument's premise lands in
# the MC's own perception; knowledge of self has unmade him." The
# Scene Lowers to E_oedipus_anagnorisis (τ_s=13). At that moment,
# the substrate should exhibit the specific epistemic effects the
# realization performs:
#
#   1. Oedipus holds identity(oedipus, the-exposed-baby) at KNOWN —
#      the anagnorisis's first identity assertion.
#   2. Oedipus holds identity(oedipus, the-crossroads-killer) at
#      KNOWN — the anagnorisis promotes the SUSPECTED identity to
#      KNOWN (the realization composes prior suspicion with the
#      newly-arriving evidence).
#   3. Oedipus holds identity(laius, the-crossroads-victim) at KNOWN —
#      the realization's third identity assertion.
#   4. Oedipus's gap_real_parents GAP has been removed — the
#      anagnorisis closes his acknowledged gap about parentage.
#
# All four signatures are literal substrate facts the realization
# event authors. A moment check at τ_s=13 verifies they all hold
# at the right slots; if so, the Scene's claim about its result is
# vindicated by the substrate.
#
# This check uses literal `holds_literal` / absence checks rather
# than rule-derived facts — the signatures are about the
# substrate's own authoring, not derivation chains. (Compare with
# the Argument's trajectory check, which uses `world_holds_derived`
# for the compound consequences.)


def anagnorisis_scene_result_check(
    upper_ref, lower_refs, position_ranges,
):
    """Claim-moment check for S_anagnorisis.result. Returns
    (verdict, match_strength, comment).

    Four moment signatures verified at the max τ_s of the Lowered
    substrate events (τ_s=13 for E_oedipus_anagnorisis):
      - Oedipus holds identity(oedipus, the-exposed-baby) at KNOWN
      - Oedipus holds identity(oedipus, the-crossroads-killer) at KNOWN
      - Oedipus holds identity(laius, the-crossroads-victim) at KNOWN
      - Oedipus no longer holds gap_real_parents (the GAP closed)

    Match strength = signatures-passing / 4. Verdict: approved if all
    four; partial-match if 2-3; needs-work if fewer.
    """
    # Determine the moment from the lower records' max τ_s. For
    # S_anagnorisis lowered to E_oedipus_anagnorisis, this is τ_s=13.
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
        agent_id="oedipus",
        events_in_scope=events_in_scope,
        up_to_τ_s=max_τ_s,
    )

    identity_signatures = [
        identity_prop("oedipus", "the-exposed-baby"),
        identity_prop("oedipus", "the-crossroads-killer"),
        identity_prop("laius", "the-crossroads-victim"),
    ]
    identity_results = []
    for p in identity_signatures:
        held = state.holds_literal(p)
        identity_results.append(held is not None and held.slot == Slot.KNOWN)

    gap_closed = state.holds_literal(gap_real_parents) is None

    signatures = identity_results + [gap_closed]
    matched = sum(signatures)
    strength = matched / len(signatures)

    if strength >= 0.99:
        verdict = VERDICT_APPROVED
    elif strength >= 0.5:
        verdict = VERDICT_PARTIAL_MATCH
    else:
        verdict = VERDICT_NEEDS_WORK

    comment = (
        f"S_anagnorisis result check at τ_s={max_τ_s}: "
        f"identity(oedipus, the-exposed-baby) KNOWN: "
        f"{identity_results[0]}; "
        f"identity(oedipus, the-crossroads-killer) KNOWN: "
        f"{identity_results[1]}; "
        f"identity(laius, the-crossroads-victim) KNOWN: "
        f"{identity_results[2]}; "
        f"gap_real_parents closed (absent from held set): "
        f"{gap_closed}; "
        f"{matched}/{len(signatures)} moment signatures present"
    )
    return (verdict, strength, comment)


# ============================================================================
# Driver — orchestrated check registry
# ============================================================================
#
# Single CHECK_REGISTRY replaces the three hand-wired tuples
# (CHARACTERIZATION_CHECKS / CLAIM_TRAJECTORY_CHECKS /
# CLAIM_MOMENT_CHECKS) and the three parallel run_X_checks calls in
# run(). The orchestrator dispatches by coupling kind, enumerates
# records per type, and applies each registered check function where
# its `applies_to` predicate matches.


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
        applies_to=lambda a: a.id == "A_knowledge_unmakes",
        check_fn=knowledge_unmakes_argument_check,
        description=(
            "A_knowledge_unmakes (AFFIRM): identity collapse + "
            "parricide + incest derivable at τ_s ≤ 13"
        ),
    ),
    CheckRegistration(
        coupling_kind=COUPLING_CLAIM_MOMENT,
        record_type="Scene",
        field="result",
        applies_to=lambda s: s.id == "S_anagnorisis",
        check_fn=anagnorisis_scene_result_check,
        description=(
            "S_anagnorisis result: identity propositions KNOWN + "
            "gap_real_parents closed at τ_s=13"
        ),
    ),
)


# Per-record-type record collections the orchestrator iterates. The
# encoding builds this; the orchestrator stays dialect-agnostic.

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
    """Run all verifier checks for the Oedipus encoding via the
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
