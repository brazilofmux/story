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
from typing import Optional

# Substrate-side imports.
from story_engine.core.substrate import (
    Entity, Event, CANONICAL,
    project_world, project_knowledge, in_scope,
    world_holds_derived, holds_derived,
)
from story_engine.encodings.oedipus import (
    FABULA, ENTITIES, RULES, ALL_BRANCHES,
    parricide, incest, child_of, killed, exiled,
)

# Dramatic-side imports.
from story_engine.core.dramatic import Throughline, Character
from story_engine.encodings.oedipus_dramatic import THROUGHLINES, CHARACTERS, STORY

# Template-side imports.
from story_engine.core.dramatica_template import (
    DomainAssignment, DynamicStoryPoint, DSPAxis,
    Domain, Approach, Outcome, Judgment,
)
from story_engine.encodings.oedipus_dramatica_complete import (
    DOMAIN_ASSIGNMENTS, DYNAMIC_STORY_POINTS,
    STORY_GOAL, STORY_CONSEQUENCE,
)

# Lowering + verifier-primitive machinery.
from story_engine.core.lowering import (
    CrossDialectRef, cross_ref, LoweringStatus,
)
from story_engine.encodings.oedipus_lowerings import LOWERINGS
from story_engine.core.verification import (
    StructuralAdvisory,
    DirectCheckRegistration, run_direct_review_checks,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH,
    VERDICT_NOTED,
    SEVERITY_NOTED,
)
from story_engine.core.verifier_helpers import (
    classify_event_action_shape, agent_ids_from_entities,
    dsp_limit_characterization_check,
    classify_event_agency_shape,
    detect_preceding_ic_event,
    events_advancing_throughline,
    compute_pre_post_action_ratios,
    fabula_end_τ_s, events_lowered_from_throughline,
)


# ============================================================================
# Encoding-bound helpers
# ============================================================================


OEDIPUS_ENTITY_ID = "oedipus"
_AGENT_IDS = agent_ids_from_entities(ENTITIES)


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
    events = events_lowered_from_throughline("T_mc_oedipus", LOWERINGS, FABULA)
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
    τ_end = fabula_end_τ_s(FABULA)
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
    τ_end = fabula_end_τ_s(FABULA)
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
# Check 5 — Claim-trajectory: DSP_resolve = Change
# ============================================================================


def dsp_resolve_change_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: DSP_resolve=Change = the MC's fundamental
    stance transitions mid-arc rather than holding steady. For
    Oedipus this renders as the self-identity transition: Oedipus's
    equivalence class gains `the-exposed-baby` mid-story, crossing a
    discrete line.

    Distinct from DSP_judgment=Bad (same substrate fact, different
    Dramatica axis): Judgment asks about the *quality* of the MC's
    resolution (catastrophic); Resolve asks whether a *transition*
    occurred at all. Both land on the same identity emergence for
    Oedipus because epistemic tragedy couples the two — a good
    Change/Good MC would show a transition to flourishing, a
    Change/Bad MC a transition to ruin."""
    τ_end = fabula_end_τ_s(FABULA)
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

    all_τ_s = sorted({e.τ_s for e in FABULA if e.τ_s is not None})
    transition_τ = None
    for τ in all_τ_s:
        if _self_identified_at(τ):
            transition_τ = τ
            break

    # Classify where the transition lands in the arc.
    if transition_τ is None:
        return (
            VERDICT_NEEDS_WORK, 0.0,
            "no self-identity transition found; Resolve=Change "
            "predicts a mid-arc transition in the MC's stance. The "
            "substrate shows no such transition.",
        )
    arc_start = min(t for t in all_τ_s if t >= 0)
    arc_span = τ_end - arc_start if τ_end > arc_start else 1
    position = (transition_τ - arc_start) / arc_span
    # RE2: end-state behavioral-shift signal per resolve-endpoint-
    # sketch-01. Compare MC's EK2 action-shape ratio pre vs post
    # the anagnorisis. For Change, a behavioral shift strengthens
    # the Change verdict beyond the identity-transition alone.
    re2 = compute_pre_post_action_ratios(
        OEDIPUS_ENTITY_ID, transition_τ,
        [e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)],
        _AGENT_IDS,
    )
    if re2["shift_detected"]:
        re_note = (
            f" [RE2 end-state: external-action ratio shifts from "
            f"{re2['pre_external_ratio']:.0%} (pre-anagnorisis, "
            f"n={re2['pre_count']}) to "
            f"{re2['post_external_ratio']:.0%} (post-anagnorisis, "
            f"n={re2['post_count']}) — behavioral shift detected; "
            f"Change signal strengthened at the end-state layer]"
        )
    else:
        re_note = (
            f" [RE2 end-state: external-action ratio "
            f"{re2['pre_external_ratio']:.0%} → "
            f"{re2['post_external_ratio']:.0%} (shift "
            f"{re2['shift']:.0%} below 30% threshold); Change is "
            f"structurally at the identity level, not the "
            f"behavioral-shape level]"
        )

    # RR3: IC-relational signal per resolve-relational-sketch-01.
    # Dramatica's Resolve=Change means MC transitions in response to
    # IC influence — check if Jocasta's throughline events temporally
    # precede the anagnorisis. Oedipus has no direct T_impact_jocasta
    # Lowering, so fall back to Scene.advances to recover IC events.
    ic_events = events_lowered_from_throughline("T_impact_jocasta", LOWERINGS, FABULA)
    if not ic_events:
        from story_engine.encodings.oedipus_dramatic import SCENES
        ic_events = events_advancing_throughline(
            "T_impact_jocasta", LOWERINGS, SCENES, FABULA,
        )
    ic_τs = [e.τ_s for e in ic_events if e.τ_s is not None]
    ic_rel = detect_preceding_ic_event(transition_τ, ic_τs, window=5)
    if ic_rel["has_correlation"]:
        ic_note = (
            f" [RR3 IC-correlation: Jocasta throughline event at "
            f"τ_s={ic_rel['nearest_preceding_ic_τ']} precedes "
            f"anagnorisis by gap={ic_rel['gap']}; IC-driven Change "
            f"signal present. OQ1: Oedipus's post-transition "
            f"behavior (self-blinding) does not unambiguously adopt "
            f"Jocasta's 'don't look' counter-premise — the strict "
            f"IC-paradigm-adoption test is banked]"
        )
    else:
        ic_note = (
            " [RR3 IC-correlation: no Jocasta throughline event in "
            "the [τ-5, τ] window preceding the anagnorisis]"
        )

    if position >= 0.4:
        return (
            VERDICT_APPROVED, 1.0,
            f"Oedipus's self-identity transition lands at τ_s="
            f"{transition_τ} ({position:.0%} through the [{arc_start}, "
            f"{τ_end}] arc) — a mid-arc transition consistent with "
            f"Resolve=Change. Distinct from Judgment=Bad: Judgment "
            f"evaluates final state; Resolve evaluates whether a "
            f"transition occurred.{re_note}{ic_note}",
        )
    return (
        VERDICT_PARTIAL_MATCH, position,
        f"self-identity transition at τ_s={transition_τ} "
        f"({position:.0%} through the arc) is earlier than Change's "
        f"typical mid-arc placement; may indicate the transition is "
        f"a pre-existing trait rather than a story-arc shift.{re_note}{ic_note}",
    )


# ============================================================================
# Check 6 — Claim-trajectory: DSP_growth = Stop
# ============================================================================


def dsp_growth_stop_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: DSP_growth=Stop = the MC needs to stop a
    problematic drive or behavior. For Oedipus the drive is his
    relentless pursuit of truth — the investigation through witness-
    interrogation. Growth=Stop's load-bearing substrate signature is
    **pursuit-event count dropping to zero post-anagnorisis**, not
    raw participation rate (per event-agency-taxonomy-sketch-01).

    Post-anagnorisis, Oedipus's participation RISES (self-blinding at
    τ_s=15, exile at τ_s=17) because consequences cascade — but those
    events are consequential-shaped under AG2 (world-effects targeting
    oedipus's state: `blinded(oedipus)`, `exiled(oedipus, thebes)`),
    not pursuit-shaped. The Stop signature is preserved cleanly once
    agency shape is the measurement, not event count.

    Under Judgment=Bad, the MC's 'stopping' doesn't heal them —
    Oedipus stops pursuing because the search has ended with him as
    its target. The substrate shape still carries the cessation, just
    at the pursuit-vs-consequential layer rather than the
    participation-count layer."""
    τ_end = fabula_end_τ_s(FABULA)
    anagnorisis_τ = None
    for e in FABULA:
        if (e.type == "realization"
                and (e.participants or {}).get("agent") == OEDIPUS_ENTITY_ID):
            anagnorisis_τ = e.τ_s
            break
    if anagnorisis_τ is None:
        return (
            VERDICT_NEEDS_WORK, 0.0,
            "no Oedipus realization event found; Growth=Stop "
            "trajectory needs a cessation pivot the substrate does "
            "not encode.",
        )

    # Per AG5: count pursuit vs consequential events pre/post
    # anagnorisis. The anagnorisis itself is the pivot event, excluded
    # from both sides.
    pre_pursuit = 0
    pre_consequential = 0
    post_pursuit = 0
    post_consequential = 0
    for e in FABULA:
        if e.τ_s is None or e.τ_s < 0:
            continue
        if e.τ_s == anagnorisis_τ:
            continue
        shape = classify_event_agency_shape(e, OEDIPUS_ENTITY_ID)
        if shape is None:
            continue  # Oedipus not participant
        if e.τ_s < anagnorisis_τ:
            if shape == "pursuit":
                pre_pursuit += 1
            elif shape == "consequential":
                pre_consequential += 1
        else:  # τ_s > anagnorisis_τ
            if shape == "pursuit":
                post_pursuit += 1
            elif shape == "consequential":
                post_consequential += 1

    summary = (
        f"pursuit/consequential counts — pre-anagnorisis (τ_s<"
        f"{anagnorisis_τ}): {pre_pursuit}/{pre_consequential}; "
        f"post-anagnorisis: {post_pursuit}/{post_consequential}"
    )

    if pre_pursuit == 0:
        return (
            VERDICT_NEEDS_WORK, 0.0,
            f"no pursuit-shaped Oedipus events before anagnorisis "
            f"at τ_s={anagnorisis_τ}; Growth=Stop needs a pursuit "
            f"drive to diagnose cessation of. {summary}.",
        )

    drop_ratio = 1.0 - (post_pursuit / pre_pursuit)
    if post_pursuit == 0:
        return (
            VERDICT_APPROVED, 1.0,
            f"Oedipus's pursuit-event count drops {pre_pursuit}→0 "
            f"across the anagnorisis pivot (τ_s={anagnorisis_τ}); "
            f"post-anagnorisis events are all consequential-shaped "
            f"(self-blinding + exile). Clean Growth=Stop signature "
            f"per AG5. {summary}.",
        )
    if drop_ratio >= 0.5:
        return (
            VERDICT_APPROVED, min(drop_ratio, 1.0),
            f"Oedipus's pursuit-event count drops {pre_pursuit}→"
            f"{post_pursuit} ({drop_ratio:.0%}) across the "
            f"anagnorisis pivot. Growth=Stop trajectory supported "
            f"per AG5. {summary}.",
        )
    return (
        VERDICT_PARTIAL_MATCH, max(drop_ratio, 0.0),
        f"Oedipus's pursuit-event count: {pre_pursuit}→{post_pursuit} "
        f"— not the sharp drop Growth=Stop predicts. {summary}.",
    )


# ============================================================================
# Check 7 — Claim-trajectory: Story_goal
# ============================================================================


def story_goal_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: Story_goal = 'identify the pollution causing
    the plague and expel it'. This is an **identification-shaped**
    goal per identification-goal-sketch-01 (IG1) — it resolves when
    the investigator (Oedipus himself) comes to know that he IS the
    pollution. The load-bearing claim is epistemic, not world-state.

    Under IG2 the check reads Oedipus's knowledge projection, not
    the world state. Target derivation: `parricide(oedipus, laius)`
    supportable from his KnowledgeState via identity-substitution +
    rule derivation (per identity-and-realization-sketch-01 I3/I7
    and inference-model-sketch-01). The **recognition τ_s** is the
    first τ_s at which this derivation is supportable; clean
    identification-goal trajectory lands at recognition τ_s ≥ 0
    (mid-arc epistemic arrival).

    Pre-sketch-01 this check read world-state and reported PARTIAL
    0.7 with a misleading 'unusual premise order' message — the
    world-facts `killed(oedipus, laius)` and `child_of(oedipus,
    laius)` both hold pre-plot (crossroads killing at τ_s=-48,
    birth at τ_s=-100), so their fabula-order was irrelevant to
    the dramatic trajectory. The probe's 2026-04-17 qualification
    named the category error; IG2 closes it."""
    τ_end = fabula_end_τ_s(FABULA)
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]

    target = parricide("oedipus", "laius")
    all_τ_s = sorted({e.τ_s for e in FABULA if e.τ_s is not None})

    # Walk τ_s in increasing order; find the first τ_s at which
    # Oedipus's knowledge supports the target derivation.
    recognition_τ = None
    for τ in all_τ_s:
        state = project_knowledge(
            agent_id=OEDIPUS_ENTITY_ID,
            events_in_scope=events_in_scope,
            up_to_τ_s=τ,
        )
        if holds_derived(state, target, RULES) is not None:
            recognition_τ = τ
            break

    if recognition_τ is None:
        return (
            VERDICT_NEEDS_WORK, 0.0,
            f"Story_goal (identification): Oedipus's knowledge "
            f"never supports parricide(oedipus, laius) at any "
            f"τ_s in arc. Trajectory does not land.",
        )

    if recognition_τ < 0:
        return (
            VERDICT_PARTIAL_MATCH, 0.5,
            f"Story_goal (identification): Oedipus's knowledge "
            f"already supports parricide(oedipus, laius) at pre-plot "
            f"τ_s={recognition_τ}. Goal lands before the arc begins; "
            f"the dramatic buildup is missing.",
        )

    if recognition_τ >= τ_end:
        return (
            VERDICT_PARTIAL_MATCH, 0.7,
            f"Story_goal (identification): Oedipus's knowledge "
            f"supports parricide only at τ_s={recognition_τ} (arc "
            f"end); the trajectory lands but without mid-arc "
            f"buildup.",
        )

    return (
        VERDICT_APPROVED, 1.0,
        f"Story_goal (identification): Oedipus's knowledge supports "
        f"parricide(oedipus, laius) from τ_s={recognition_τ} "
        f"(anagnorisis) onward via identity-substitution. Pre-"
        f"anagnorisis his knowledge does not support the derivation "
        f"— the equivalence class linking oedipus and laius hasn't "
        f"collapsed yet. The epistemic pivot at τ_s={recognition_τ} "
        f"IS the goal's trajectory landing (IG2).",
    )


# ============================================================================
# Check 8 — Characterization: DSP_limit (pressure-shape-taxonomy-sketch-01)
# ============================================================================


def dsp_limit_optionlock_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DSP_limit. Oedipus declares Optionlock (he runs
    out of options, not time). LT2 predicts convergence signals in
    the substrate: identity-resolution (oedipus ↔ the-exposed-baby)
    and rule-derivable emergences (parricide, incest) accreting
    across the arc. Delegates to `dsp_limit_characterization_check`
    in verifier_helpers; the classifier is encoding-agnostic."""
    declared = next(
        d.choice for d in DYNAMIC_STORY_POINTS if d.axis == DSPAxis.LIMIT
    )
    return dsp_limit_characterization_check(
        FABULA, RULES, CANONICAL, ALL_BRANCHES, declared,
    )


# ============================================================================
# Check 9 — Claim-moment: Story_consequence
# ============================================================================


def story_consequence_moment_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-moment: Story_consequence = 'the plague continues; the
    city dies; the pollution festers'. Under DSP_outcome=Success,
    the consequence is AVOIDED at τ_end — the pollution is expelled.
    Substrate check: at τ_end, (a) parricide derives (the pollution
    is identified) AND (b) `exiled(oedipus)` is world-asserted
    (the pollution is expelled). Both conditions must hold for
    the consequence to be successfully averted."""
    τ_end = fabula_end_τ_s(FABULA)
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    final_world = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=τ_end,
    )
    pollution_identified = world_holds_derived(
        final_world, parricide("oedipus", "laius"), RULES,
    ) is not None
    pollution_expelled = exiled("oedipus") in final_world

    if pollution_identified and pollution_expelled:
        return (
            VERDICT_APPROVED, 1.0,
            f"at τ_s={τ_end}: parricide(oedipus, laius) derives "
            f"(pollution identified) AND exiled(oedipus) holds "
            f"(pollution expelled). Story_consequence is averted — "
            f"the plague-cause has been found and removed, as "
            f"Success=Outcome predicts.",
        )
    if pollution_identified or pollution_expelled:
        return (
            VERDICT_PARTIAL_MATCH, 0.5,
            f"at τ_s={τ_end}: identified={pollution_identified}, "
            f"expelled={pollution_expelled}. One half of the "
            f"consequence-avoidance condition is missing; the "
            f"success is incomplete.",
        )
    return (
        VERDICT_NEEDS_WORK, 0.0,
        f"at τ_s={τ_end}: identified=False, expelled=False. The "
        f"consequence is not averted; substrate state does not "
        f"support Outcome=Success.",
    )


# ============================================================================
# Orchestration (parallel to other dramatica-complete verifiers)
# ============================================================================


CHECK_REGISTRY = (
    DirectCheckRegistration(
        "dramatica-complete", "DA_mc",
        mc_throughline_activity_domain_check,
        "verifier:characterization:domain-assignment",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_approach",
        oedipus_do_er_approach_check,
        "verifier:characterization:dsp-approach",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_limit",
        dsp_limit_optionlock_check,
        "verifier:characterization:dsp-limit",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_outcome",
        outcome_success_claim_at_end_check,
        "verifier:claim-moment:dsp-outcome",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_judgment",
        judgment_bad_trajectory_check,
        "verifier:claim-trajectory:dsp-judgment",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_resolve",
        dsp_resolve_change_trajectory_check,
        "verifier:claim-trajectory:dsp-resolve",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_growth",
        dsp_growth_stop_trajectory_check,
        "verifier:claim-trajectory:dsp-growth",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "Story_goal",
        story_goal_trajectory_check,
        "verifier:claim-trajectory:story-goal",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "Story_consequence",
        story_consequence_moment_check,
        "verifier:claim-moment:story-consequence",
    ),
)


def run() -> tuple:
    """Run the Template-layer verifier checks for Oedipus.
    Returns a tuple of VerificationReview records.

    Check inventory (9 checks across all three primitives):
    - Characterization: DA_mc, DSP_approach, DSP_limit
    - Claim-moment: DSP_outcome, Story_consequence
    - Claim-trajectory: DSP_judgment, DSP_resolve, DSP_growth,
      Story_goal
    """
    return run_direct_review_checks(CHECK_REGISTRY)


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
