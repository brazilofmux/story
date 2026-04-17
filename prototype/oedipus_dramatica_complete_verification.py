"""
oedipus_dramatica_complete_verification.py — second cross-boundary
verifier at the **dramatica-complete → substrate** coupling boundary.

Parallels macbeth_dramatica_complete_verification.py. Same four-check
shape; Oedipus's substrate pressures the checks differently:

- **Epistemic substrate.** Oedipus's fabula is 12 events; dominant
  event kinds are `utterance` (4), `realization` (2),
  `prophecy_received` (1), with only `killing` (1) and `marriage` (1)
  as external-action events. Macbeth's substrate is action-saturated
  (killings, battles, coronations); Oedipus's is speech-saturated
  (testimonies, realizations). Dramatica classifies both MCs as
  Activity domain / Do-er — correctly, since in upper-dialect terms
  investigation IS activity — but the substrate renders Oedipus's
  doing as speech acts. Expected result: the two Characterization
  checks surface this mismatch, pinpointing F5 (lowering-sketch-01's
  substrate-gap finding) concretely.

- **Different end-of-arc semantics.** For Macbeth, DSP_outcome=Success
  is confirmed by `dead(macbeth)`. For Oedipus, Outcome=Success is
  "the plague-killer is found" — a knowledge/derivation resolution.
  Substrate check: `parricide(oedipus, laius)` is world-derivable at
  τ_s=end (inference-01 rule chain from `killed` + `child_of`).

- **Epistemic Judgment trajectory.** Macbeth's Judgment=Bad tracks a
  moral-degradation shape (`tyrant(macbeth)` emerging). Oedipus's
  Judgment=Bad is epistemic-ruin — he discovers what he already was.
  Substrate check: Oedipus's own knowledge state (`project_knowledge`)
  does NOT contain the identity equivalence `oedipus ↔ laius-killer`
  at τ_s=0, DOES contain it at τ_s=end. Ruin-as-knowing trajectory.

Per V6, trajectory and moment checks compose with inference-01's
derivation surface — parricide is derived from the rule engine
(`killed(X,Y) ∧ child_of(X,Y) ⇒ parricide(X,Y)`), not authored at
event sites (inference-model-sketch-01 retired the authored
predicate).

This is the second verifier at the new boundary; together with
macbeth_dramatica_complete_verification it exercises two structurally
different encodings against the same three primitives, confirming the
boundary generalizes and surfacing where the Oedipus substrate gap
(F5) bites for the Activity / Do-er classifications.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

# Substrate-side imports.
from substrate import (
    Entity, Event, CANONICAL,
    project_world, project_knowledge, in_scope,
    world_holds_derived,
)
from oedipus import (
    FABULA, ENTITIES, RULES, ALL_BRANCHES,
    parricide, incest,
)

# Dramatic-side imports.
from dramatic import Throughline, Character
from oedipus_dramatic import THROUGHLINES, CHARACTERS, STORY

# Template-side imports.
from dramatica_template import (
    DomainAssignment, DynamicStoryPoint, DSPAxis,
    Domain, Approach, Outcome, Judgment,
)
from oedipus_dramatica_complete import (
    DOMAIN_ASSIGNMENTS, DYNAMIC_STORY_POINTS,
)

# Lowering + verifier-primitive machinery.
from lowering import (
    CrossDialectRef, cross_ref, LoweringStatus,
)
from oedipus_lowerings import LOWERINGS
from verification import (
    VerificationReview, StructuralAdvisory,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH,
    VERDICT_NOTED,
    SEVERITY_NOTED,
)
from verifier_helpers import (
    classify_event_action_shape, agent_ids_from_entities,
)


# ============================================================================
# Encoding-bound helpers
# ============================================================================


OEDIPUS_ENTITY_ID = "oedipus"
_AGENT_IDS = agent_ids_from_entities(ENTITIES)


def _end_τ_s() -> int:
    """Highest τ_s in Oedipus's fabula."""
    return max(e.τ_s for e in FABULA if e.τ_s is not None)


def _events_lowered_from_throughline(throughline_id: str) -> tuple:
    """Return substrate Events reached via ACTIVE Lowerings whose
    upper_record is this Throughline. Parallels the same-named helper
    in macbeth_dramatica_complete_verification.py; the logic is
    encoding-agnostic but the LOWERINGS source is Oedipus's."""
    upper = cross_ref("dramatic", throughline_id)
    event_ids: list = []
    for lw in LOWERINGS:
        if lw.upper_record != upper:
            continue
        if lw.status != LoweringStatus.ACTIVE:
            continue
        for lr in lw.lower_records:
            if lr.dialect == "substrate":
                event_ids.append(lr.record_id)
    events = []
    for eid in event_ids:
        for e in FABULA:
            if e.id == eid:
                events.append(e)
                break
    return tuple(events)


def _oedipus_is_participant(event: Event) -> bool:
    parts = event.participants or {}
    return OEDIPUS_ENTITY_ID in parts.values()


# ============================================================================
# Check 1 — Characterization: DomainAssignment(T_mc_oedipus, ACTIVITY)
# ============================================================================


def mc_throughline_activity_domain_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DA_mc — T_mc_oedipus in Activity domain. Substrate
    check: of the events reached via L_mc_throughline, count
    external-action-shaped vs. internal-state-shaped per EK2
    (event-kind-taxonomy-sketch-01) — a structural predicate over
    participants and effects, not a type-string set."""
    events = _events_lowered_from_throughline("T_mc_oedipus")
    if not events:
        return (
            VERDICT_NOTED, None,
            "T_mc_oedipus has no ACTIVE substrate-event Lowerings; "
            "DomainAssignment check cannot evaluate",
        )
    total = len(events)
    action_count = sum(
        1 for e in events
        if classify_event_action_shape(e, agent_ids=_AGENT_IDS)
        == "external"
    )
    state_count = total - action_count
    ratio = action_count / total
    if ratio >= 0.7:
        return (
            VERDICT_APPROVED, ratio,
            f"{action_count}/{total} ({ratio:.0%}) MC-Throughline "
            f"events are external-action-shaped (EK2); {state_count} "
            f"are internal-state-shaped. Consistent with Activity "
            f"domain.",
        )
    if ratio >= 0.4:
        return (
            VERDICT_PARTIAL_MATCH, ratio,
            f"{action_count}/{total} ({ratio:.0%}) MC-Throughline "
            f"events are external-action-shaped (EK2); the mix leans "
            f"toward internal-state.",
        )
    return (
        VERDICT_NEEDS_WORK, ratio,
        f"only {action_count}/{total} ({ratio:.0%}) MC-Throughline "
        f"events are external-action-shaped per EK2 "
        f"({state_count} are internal-state-shaped). If this "
        f"persists after substrate extension, the substrate is "
        f"genuinely at a different grain than Dramatica-Sophocles — "
        f"F5 (lowering-sketch-01 substrate-gap finding) points at "
        f"which beats the encoding is still missing.",
    )


# ============================================================================
# Check 2 — Characterization: DSP_approach = Do-er
# ============================================================================


def oedipus_do_er_approach_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DSP_approach — Oedipus is a Do-er. Substrate
    check: of events where Oedipus is a participant, the fraction
    that are external-action-shaped per EK2 (structural predicate
    over participants and effects)."""
    oed_events = [e for e in FABULA if _oedipus_is_participant(e)]
    if not oed_events:
        return (
            VERDICT_NOTED, None,
            "Oedipus entity has no recorded participations; check "
            "cannot evaluate",
        )
    total = len(oed_events)
    action_count = sum(
        1 for e in oed_events
        if classify_event_action_shape(e, agent_ids=_AGENT_IDS)
        == "external"
    )
    ratio = action_count / total
    if ratio >= 0.65:
        return (
            VERDICT_APPROVED, ratio,
            f"Oedipus participates in {total} events; {action_count} "
            f"({ratio:.0%}) are external-action-shaped (EK2). Do-er "
            f"approach confirmed.",
        )
    if ratio >= 0.35:
        return (
            VERDICT_PARTIAL_MATCH, ratio,
            f"Oedipus participates in {total} events; {action_count} "
            f"({ratio:.0%}) are external-action-shaped (EK2). Mixed "
            f"Do-er / Be-er signature in substrate.",
        )
    return (
        VERDICT_NEEDS_WORK, ratio,
        f"Oedipus participates in {total} events; only {action_count} "
        f"({ratio:.0%}) are external-action-shaped per EK2. Do-er "
        f"classification at the upper dialect is not invalidated — "
        f"Oedipus's investigation is active — but the substrate "
        f"does not yet encode enough of it as interpersonal outward-"
        f"effect events for EK2 to classify it external.",
    )


# ============================================================================
# Check 3 — Claim-moment: DSP_outcome = Success at τ_s = end
# ============================================================================


def outcome_success_claim_at_end_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-moment: at τ_s = end, the OS goal lands. For Oedipus
    under Outcome=Success, the OS goal is "find the plague-killer"
    — the load-bearing substrate fact is `parricide(oedipus, laius)`
    being world-derivable at end, which is the public identification
    that ends the plague per Apollo's oracle. The rule chain
    `killed(X,Y) ∧ child_of(X,Y) ⇒ parricide(X,Y)` fires at τ_s=end
    because both premises are world-asserted by then
    (E_crossroads_killing gives killed(oedipus, laius);
    E_shepherd_testimony + E_oedipus_anagnorisis establish
    child_of(oedipus, laius))."""
    τ_end = _end_τ_s()
    events_up_to_end = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    world_facts = project_world(
        events_in_scope=events_up_to_end, up_to_τ_s=τ_end,
    )
    proof = world_holds_derived(
        world_facts, parricide(OEDIPUS_ENTITY_ID, "laius"), RULES,
    )
    if proof is not None:
        return (
            VERDICT_APPROVED, 1.0,
            f"parricide(oedipus, laius) is world-derivable at "
            f"τ_s={τ_end}; Outcome=Success claim (OS goal — plague-"
            f"killer identified) is supported by substrate via the "
            f"inference-01 rule chain at end of fabula.",
        )
    return (
        VERDICT_NEEDS_WORK, 0.0,
        f"parricide(oedipus, laius) does NOT derive at τ_s={τ_end}; "
        f"Outcome=Success claim not supported by substrate at end "
        f"of fabula.",
    )


# ============================================================================
# Check 4 — Claim-trajectory: DSP_judgment = Bad (epistemic ruin)
# ============================================================================


def judgment_bad_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: Judgment=Bad = Oedipus's internal resolution
    is catastrophic. For Oedipus this renders as epistemic ruin (not
    Macbeth's moral-degradation shape): he ends knowing what he
    already was. Substrate shape: project_knowledge(agent=oedipus)
    at τ_s=0 does NOT contain the self-identity equivalence class
    (oedipus ↔ the-exposed-baby / son-of-laius); at τ_s=end it DOES.
    Identity-and-realization sketch-01's machinery is the substrate
    surface this claim rests on."""
    τ_end = _end_τ_s()
    events_in_scope_all = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]

    def _self_identified_at(τ: int) -> bool:
        state = project_knowledge(
            agent_id=OEDIPUS_ENTITY_ID,
            events_in_scope=events_in_scope_all,
            up_to_τ_s=τ,
        )
        for cls in state.equivalence_classes():
            if (OEDIPUS_ENTITY_ID in cls
                    and "the-exposed-baby" in cls):
                return True
        return False

    at_start = _self_identified_at(0)
    at_end = _self_identified_at(τ_end)

    # Find the earliest τ_s at which self-identity lands — the
    # anagnorisis point, structurally.
    all_τ_s = sorted({e.τ_s for e in FABULA if e.τ_s is not None})
    first_holding = None
    for τ in all_τ_s:
        if _self_identified_at(τ):
            first_holding = τ
            break

    if not at_start and at_end and first_holding is not None:
        return (
            VERDICT_APPROVED, 1.0,
            f"Oedipus's self-identity (oedipus ↔ the-exposed-baby) "
            f"does not hold at τ_s=0; emerges at τ_s={first_holding} "
            f"(anagnorisis); still holds at τ_s={τ_end}. Epistemic-"
            f"ruin trajectory consistent with Judgment=Bad.",
        )
    if at_end and not at_start:
        return (
            VERDICT_PARTIAL_MATCH, 0.7,
            f"Oedipus's self-identity holds at end (τ_s={τ_end}) but "
            f"anagnorisis τ_s could not be pinpointed; trajectory "
            f"shape consistent.",
        )
    return (
        VERDICT_NEEDS_WORK, 0.0,
        f"Oedipus self-identity trajectory: at_start={at_start}, "
        f"at_end={at_end}. Does not match the ignorance-to-knowing "
        f"shape Judgment=Bad predicts for an epistemic-tragedy MC.",
    )


# ============================================================================
# Orchestration (parallel to macbeth_dramatica_complete_verification)
# ============================================================================


def _wrap_check(
    upper_dialect: str,
    upper_record_id: str,
    check_fn: Callable,
    reviewer_id: str,
    *,
    reviewed_at_τ_a: int = 0,
) -> VerificationReview:
    upper_ref = cross_ref(upper_dialect, upper_record_id)
    verdict, strength, comment = check_fn(upper_ref)
    return VerificationReview(
        reviewer_id=reviewer_id,
        reviewed_at_τ_a=reviewed_at_τ_a,
        verdict=verdict,
        anchor_τ_a=0,
        target_record=upper_ref,
        comment=comment,
        match_strength=strength,
    )


def run() -> tuple:
    """Run the four Template-layer verifier checks for Oedipus.
    Returns a tuple of VerificationReview records."""
    return (
        _wrap_check(
            "dramatica-complete", "DA_mc",
            mc_throughline_activity_domain_check,
            reviewer_id="verifier:characterization:domain-assignment",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_approach",
            oedipus_do_er_approach_check,
            reviewer_id="verifier:characterization:dsp-approach",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_outcome",
            outcome_success_claim_at_end_check,
            reviewer_id="verifier:claim-moment:dsp-outcome",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_judgment",
            judgment_bad_trajectory_check,
            reviewer_id="verifier:claim-trajectory:dsp-judgment",
        ),
    )


if __name__ == "__main__":
    reviews = run()
    print(f"=== Oedipus dramatica-complete → substrate verifier ===")
    print(f"{len(reviews)} checks run; "
          f"{sum(1 for r in reviews if r.verdict == VERDICT_APPROVED)} "
          f"approved.\n")
    for r in reviews:
        target = f"{r.target_record.dialect}:{r.target_record.record_id}"
        strength = (
            f" strength={r.match_strength:.2f}"
            if r.match_strength is not None else ""
        )
        print(f"[{r.verdict}]{strength} {target}")
        print(f"  via {r.reviewer_id}")
        print(f"  {r.comment}\n")
