"""
macbeth_dramatica_complete_verification.py — first cross-boundary
verifier at the **dramatica-complete → substrate** coupling boundary.

Parallels macbeth_verification.py, which verifies the Dramatic dialect
against substrate. This module operates at a different layer: it
verifies the Template-specific records (DomainAssignment,
DynamicStoryPoint, ThematicPicks, ...) against substrate, using
verification-sketch-01's three primitives (Characterization,
Claim-moment, Claim-trajectory).

**Finding documented by this module's existence (and absence of a
sibling *_lowerings file):** the dramatica-complete Template
introduces no new Realization couplings. Every Template record either
classifies (Characterization) or claims (Claim-moment /
Claim-trajectory) substrate state — none binds "upper made true by
specific lower records" the way Character → Entity or Scene →
Event(s) does at the Dramatic layer. See TEMPLATE_COUPLING_DECLARATIONS
in dramatica_template.py for the per-record-type declarations. The
practical consequence: authoring Lowerings for a dramatica-complete
encoding reduces to authoring them for the underlying Dramatic
encoding (macbeth_lowerings.py). This verifier module is where all
the new coupling work lands.

Scope of this first pass — four representative checks, covering all
three primitives:

1. **Characterization** — DomainAssignment(T_mc_macbeth, ACTIVITY):
   the MC Throughline's lowered substrate events are predominantly
   external-action-kind (killed / ordered_killing / fought patterns)
   versus internal-state-kind (fixed attitudes, mental states). High
   ratio confirms Activity domain classification.

2. **Characterization** — DSP_approach (Do-er): Macbeth is a Do-er,
   not a Be-er. Check: of events where Macbeth is a participant, the
   fraction where he is the agent of an external action. High ratio
   confirms Do-er.

3. **Claim-moment** — DSP_outcome (Success): at τ_s = end of fabula,
   the OS goal ("ambition unmakes" → Scotland freed of Macbeth's
   tyranny) lands. Substrate check: `dead(macbeth)` holds at end_τ_s.

4. **Claim-trajectory** — DSP_judgment (Bad): Macbeth's moral state
   degrades across the arc. Substrate check: `tyrant(macbeth)` does
   NOT derive at τ_s=0, DOES derive by some intermediate τ_s, and
   continues to hold at end_τ_s. Emerges-and-persists shape.

Deferred (follow-on exercises, pressure the framework further):

- Signpost claim-moment checks (16 Signposts, 4 per Throughline —
  at each narrative position, the Throughline is "at" a declared
  Concern; substrate events in that position's range should exhibit
  the Concern's pattern).
- CharacterElementAssignment claim-trajectory checks across all four
  dimensions (Motivation, Methodology, Evaluation, Purpose) × 8
  function-carrying characters = up to 32 checks.
- ThematicPicks pick-chain claim-trajectory checks (problem →
  solution → symptom → response across each Throughline's arc).
- Story_goal and Story_consequence claims.
- Remaining DSP axes (Resolve, Growth, Limit).

Per V6, Claim-moment and Claim-trajectory checks compose with
inference-01's derivation surface — the `tyrant` and `dead` predicates
are derived from the rule engine, not authored at event sites.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

# Substrate-side imports.
from story_engine.core.substrate import (
    Entity, Event, CANONICAL,
    project_world, in_scope,
    world_holds_derived, world_holds_literal,
)
from story_engine.encodings.macbeth import (
    FABULA, ENTITIES, RULES, ALL_BRANCHES,
    tyrant, dead, killed, ordered_killing, king,
)

# Dramatic-side imports.
from story_engine.core.dramatic import Throughline, Character
from story_engine.encodings.macbeth_dramatic import THROUGHLINES, CHARACTERS, STORY, SCENES, BEATS

# Template-side imports.
from story_engine.core.dramatica_template import (
    DomainAssignment, DynamicStoryPoint, DSPAxis,
    Domain, Approach, Outcome, Judgment,
)
from story_engine.encodings.macbeth_dramatica_complete import (
    DOMAIN_ASSIGNMENTS, DYNAMIC_STORY_POINTS,
    STORY_GOAL, STORY_CONSEQUENCE,
)

# Lowering + verifier-primitive machinery.
from story_engine.core.lowering import (
    CrossDialectRef, cross_ref, LoweringStatus,
)
from story_engine.encodings.macbeth_lowerings import LOWERINGS
from story_engine.core.verification import (
    VerificationReview, StructuralAdvisory,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH,
    VERDICT_NOTED,
    SEVERITY_NOTED,
)
from story_engine.core.verifier_helpers import (
    classify_event_action_shape, agent_ids_from_entities,
    dsp_limit_characterization_check,
    beat_type_weight, event_to_beat_type,
    detect_preceding_ic_event,
    compute_pre_post_action_ratios,
)


# ============================================================================
# Encoding-bound helpers
# ============================================================================


MACBETH_ENTITY_ID = "macbeth"
_AGENT_IDS = agent_ids_from_entities(ENTITIES)


def _end_τ_s() -> int:
    """Highest τ_s in the Macbeth fabula."""
    return max(e.τ_s for e in FABULA if e.τ_s is not None)


def _events_lowered_from_throughline(throughline_id: str) -> tuple:
    """Return substrate Events reached via ACTIVE Lowerings whose
    upper_record is this Throughline. Uses macbeth_lowerings LOWERINGS
    as the source of truth for the MC Throughline's substrate scope."""
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


def _macbeth_is_participant(event: Event) -> bool:
    """True if the 'macbeth' entity appears among the event's
    participants. Substrate Event participants is a dict mapping
    role-label → entity_id; Macbeth's entity_id is 'macbeth'."""
    parts = event.participants or {}
    return MACBETH_ENTITY_ID in parts.values()


# ============================================================================
# Check 1 — Characterization: DomainAssignment(T_mc_macbeth, ACTIVITY)
# ============================================================================


def mc_throughline_activity_domain_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DA_mc — the MC Throughline (T_mc_macbeth) is in
    the Activity domain. Substrate check: of the events reached via
    L_mc_throughline's lowering, count external-action-shaped vs.
    internal-state-shaped per EK2, weighted by beat-type significance
    per beat-weight-taxonomy-sketch-01 (BW4).

    Beat-type weighting addresses the 2026-04-17 probe qualification:
    non-Activity events in Macbeth's arc (prophecies, ghost) are the
    MC Throughline's most dramatically significant moments
    (inciting, midpoint) — treating all events equally understates
    their narrative weight. The weighted ratio honestly reports the
    Activity-domain classification strength.

    Comment reports both the raw count and the weighted ratio so
    the refinement is inspectable."""
    events = _events_lowered_from_throughline("T_mc_macbeth")
    if not events:
        return (
            VERDICT_NOTED, None,
            "T_mc_macbeth has no ACTIVE substrate-event Lowerings; "
            "DomainAssignment check cannot evaluate",
        )
    total = len(events)
    action_count = sum(
        1 for e in events
        if classify_event_action_shape(e, agent_ids=_AGENT_IDS)
        == "external"
    )
    state_count = total - action_count
    raw_ratio = action_count / total

    # BW4: weighted ratio using beat_type significance.
    weighted_activity = 0.0
    weighted_total = 0.0
    for e in events:
        beat_type = event_to_beat_type(
            e.id, "T_mc_macbeth", LOWERINGS, SCENES, BEATS,
        )
        weight = beat_type_weight(beat_type)
        weighted_total += weight
        if (classify_event_action_shape(e, agent_ids=_AGENT_IDS)
                == "external"):
            weighted_activity += weight
    weighted_ratio = (
        weighted_activity / weighted_total if weighted_total > 0 else 0.0
    )
    breakdown = (
        f"raw {action_count}/{total} ({raw_ratio:.0%}); "
        f"BW4-weighted {weighted_activity:.1f}/{weighted_total:.1f} "
        f"({weighted_ratio:.0%}) — beat_type significance applied"
    )

    if weighted_ratio >= 0.7:
        return (
            VERDICT_APPROVED, weighted_ratio,
            f"{breakdown}. Consistent with Activity domain — "
            f"weighted signal confirms the Activity-flavored majority "
            f"carries enough narrative weight to support the "
            f"declaration.",
        )
    if weighted_ratio >= 0.4:
        return (
            VERDICT_PARTIAL_MATCH, weighted_ratio,
            f"{breakdown}. Activity-domain classification partially "
            f"supported; the non-Activity events ({state_count} raw) "
            f"include dramatically heavy beats (inciting prophecy, "
            f"midpoint ghost) whose weight shifts the honest signal "
            f"below the raw ratio.",
        )
    return (
        VERDICT_NEEDS_WORK, weighted_ratio,
        f"{breakdown}. Activity domain classification weakly "
        f"supported under beat-weighted reading; the non-Activity "
        f"events dominate when narrative weight is honored.",
    )


# ============================================================================
# Check 2 — Characterization: DSP_approach = Do-er
# ============================================================================


def macbeth_do_er_approach_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DSP_approach — Macbeth is a Do-er. Substrate
    check: of all fabula events in which Macbeth is a participant,
    the fraction that are external-action-shaped per EK2."""
    macbeth_events = [e for e in FABULA if _macbeth_is_participant(e)]
    if not macbeth_events:
        return (
            VERDICT_NOTED, None,
            "Macbeth entity has no recorded participations; check "
            "cannot evaluate",
        )
    total = len(macbeth_events)
    action_count = sum(
        1 for e in macbeth_events
        if classify_event_action_shape(e, agent_ids=_AGENT_IDS)
        == "external"
    )
    ratio = action_count / total
    if ratio >= 0.65:
        return (
            VERDICT_APPROVED, ratio,
            f"Macbeth participates in {total} events; {action_count} "
            f"({ratio:.0%}) are external-action-shaped (EK2). Do-er "
            f"approach confirmed.",
        )
    if ratio >= 0.35:
        return (
            VERDICT_PARTIAL_MATCH, ratio,
            f"Macbeth participates in {total} events; {action_count} "
            f"({ratio:.0%}) are external-action-shaped (EK2). Mixed "
            f"Do-er / Be-er signature.",
        )
    return (
        VERDICT_NEEDS_WORK, ratio,
        f"Macbeth participates in {total} events; only {action_count} "
        f"({ratio:.0%}) are external-action-shaped per EK2. Do-er "
        f"classification weakly supported.",
    )


# ============================================================================
# Check 3 — Claim-moment: DSP_outcome = Success at τ_s = end
# ============================================================================


def outcome_success_claim_at_end_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-moment: at τ_s = end, the OS goal lands. For Macbeth
    under Outcome=Success, the OS goal is "Scotland freed of Macbeth's
    tyranny"; the load-bearing substrate fact is `dead(macbeth)` at
    end. A richer check would also verify a successor-king fact, but
    `dead(macbeth)` is the necessary condition this claim rests on."""
    τ_end = _end_τ_s()
    events_up_to_end = [
        e for e in FABULA
        if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    world_facts = project_world(
        events_in_scope=events_up_to_end, up_to_τ_s=τ_end,
    )
    holds = world_holds_literal(dead(MACBETH_ENTITY_ID), world_facts)
    if holds:
        return (
            VERDICT_APPROVED, 1.0,
            f"dead(macbeth) holds at τ_s={τ_end}; Outcome=Success "
            f"claim (OS goal — Scotland freed of Macbeth — lands) "
            f"is supported by substrate at end of fabula.",
        )
    return (
        VERDICT_NEEDS_WORK, 0.0,
        f"dead(macbeth) does NOT hold at τ_s={τ_end}; "
        f"Outcome=Success claim not supported by the substrate's "
        f"end-of-fabula state.",
    )


# ============================================================================
# Check 4 — Claim-trajectory: DSP_judgment = Bad (tyrant emerges, persists)
# ============================================================================


def judgment_bad_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: Judgment=Bad = Macbeth's moral state
    degrades and stays degraded through his arc's resolution.
    Substrate shape: tyrant(macbeth) does NOT derive at τ_s=0 (he
    isn't a tyrant yet — he's a loyal general), DOES derive by some
    intermediate τ_s (once regicide + king + kinslayer coincide),
    and continues to hold at τ_s = just-before-death. Judgment
    evaluates MC internal resolution at arc-resolution; for a
    character who dies that is the moment preceding death (the
    tyrant rule depends on king(macbeth), which collapses the moment
    Malcolm takes the throne — so checking at τ_end proper would
    under-report the MC's resolution state)."""
    τ_end = _end_τ_s()
    τ_judgment = τ_end - 1  # moment-before-death; MC's arc resolution
    events_in_scope_all = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    tyrant_query = tyrant(MACBETH_ENTITY_ID)

    def _tyrant_holds_at(τ: int) -> bool:
        wf = project_world(
            events_in_scope=events_in_scope_all, up_to_τ_s=τ,
        )
        return world_holds_derived(wf, tyrant_query, RULES) is not None

    at_start = _tyrant_holds_at(0)
    at_judgment = _tyrant_holds_at(τ_judgment)

    # Find the earliest τ_s at which tyrant(macbeth) derives.
    all_τ_s = sorted({e.τ_s for e in FABULA if e.τ_s is not None})
    first_holding = None
    for τ in all_τ_s:
        if _tyrant_holds_at(τ):
            first_holding = τ
            break

    if not at_start and at_judgment and first_holding is not None:
        return (
            VERDICT_APPROVED, 1.0,
            f"tyrant(macbeth) does not hold at τ_s=0; emerges at "
            f"τ_s={first_holding}; still holds at τ_s={τ_judgment} "
            f"(moment before death at τ_s={τ_end}). "
            f"Emerges-and-persists trajectory consistent with "
            f"Judgment=Bad.",
        )
    if at_judgment and not at_start:
        return (
            VERDICT_PARTIAL_MATCH, 0.7,
            f"tyrant(macbeth) holds at arc-resolution "
            f"(τ_s={τ_judgment}) but emergence τ_s could not be "
            f"pinpointed; trajectory shape consistent but the "
            f"emergence point is diffuse.",
        )
    return (
        VERDICT_NEEDS_WORK, 0.0,
        f"tyrant(macbeth) trajectory: at_start={at_start}, "
        f"at_judgment(τ_s={τ_judgment})={at_judgment}. Does not "
        f"match the emerges-and-persists shape Judgment=Bad predicts.",
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
    stance transitions mid-arc. For Macbeth the substrate signature
    is `tyrant(macbeth)` emerging: at τ_s=0 he is a loyal general
    (tyrant does NOT derive), at τ_s=6 (post-coronation + post-
    regicide) the rule chain fires and he becomes a tyrant world-
    side, holding through τ_s=17 (moment before death).

    Distinct from DSP_judgment=Bad (both check tyrant emergence, but
    asking different Dramatica questions): Judgment asks *was the
    resolution bad*; Resolve asks *did a transition occur at all*.
    For a Change/Bad MC both fire on the same substrate fact."""
    τ_end = _end_τ_s()
    events_in_scope_all = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    all_τ_s = sorted({e.τ_s for e in FABULA if e.τ_s is not None})

    def _tyrant_holds_at(τ: int) -> bool:
        wf = project_world(
            events_in_scope=events_in_scope_all, up_to_τ_s=τ,
        )
        return world_holds_derived(
            wf, tyrant(MACBETH_ENTITY_ID), RULES,
        ) is not None

    transition_τ = None
    for τ in all_τ_s:
        if _tyrant_holds_at(τ):
            transition_τ = τ
            break

    if transition_τ is None:
        return (
            VERDICT_NEEDS_WORK, 0.0,
            "tyrant(macbeth) never derives; Resolve=Change "
            "trajectory predicts a mid-arc transition that the "
            "substrate does not show.",
        )

    arc_start = min(t for t in all_τ_s if t >= 0)
    arc_span = τ_end - arc_start if τ_end > arc_start else 1
    position = (transition_τ - arc_start) / arc_span

    # RE2: end-state behavioral-shift signal per resolve-endpoint-
    # sketch-01. For Macbeth, both pre- and post-transition events
    # are action-dominated (kills before and after coronation); no
    # behavioral shift is expected. The RE2 "no shift" report
    # honestly surfaces v3's observation that Macbeth's terminal
    # "I will not yield" reads as Steadfast commitment at the
    # behavioral layer even though Change is confirmed at the
    # identity layer (tyrant emergence).
    re2 = compute_pre_post_action_ratios(
        MACBETH_ENTITY_ID, transition_τ,
        events_in_scope_all,
        _AGENT_IDS,
    )
    if re2["shift_detected"]:
        re_note = (
            f" [RE2 end-state: external-action ratio shifts from "
            f"{re2['pre_external_ratio']:.0%} (pre-transition, "
            f"n={re2['pre_count']}) to "
            f"{re2['post_external_ratio']:.0%} (post-transition, "
            f"n={re2['post_count']}) — behavioral shift reinforces "
            f"Change signal]"
        )
    else:
        re_note = (
            f" [RE2 end-state: external-action ratio "
            f"{re2['pre_external_ratio']:.0%} → "
            f"{re2['post_external_ratio']:.0%} (shift "
            f"{re2['shift']:.0%} below 30% threshold). Change is "
            f"structurally at the identity level (tyrant emergence), "
            f"not the behavioral-shape level. v3 probe observation: "
            f"Macbeth's terminal 'I will not yield' doubling-down "
            f"reads as Steadfast commitment at the behavioral layer]"
        )

    # RR3: IC-relational signal per resolve-relational-sketch-01.
    # Dramatica's Resolve=Change specifically means MC changes in
    # response to IC influence — check if Lady Macbeth's throughline
    # events temporally precede the tyrant-transition.
    ic_events = _events_lowered_from_throughline("T_impact_lady_macbeth")
    ic_τs = [e.τ_s for e in ic_events if e.τ_s is not None]
    ic_rel = detect_preceding_ic_event(transition_τ, ic_τs, window=5)
    if ic_rel["has_correlation"]:
        ic_note = (
            f" [RR3 IC-correlation: Lady Macbeth throughline event "
            f"at τ_s={ic_rel['nearest_preceding_ic_τ']} precedes "
            f"tyrant-transition by gap={ic_rel['gap']}; Dramatica's "
            f"IC-driven Change axis structurally supported]"
        )
    else:
        ic_note = (
            " [RR3 IC-correlation: no Lady Macbeth throughline event "
            "in the [τ-5, τ] window preceding the tyrant-transition; "
            "Change verdict rests on MC-state signal alone]"
        )

    if position >= 0.2:
        return (
            VERDICT_APPROVED, 1.0,
            f"Macbeth's tyrant-transition lands at τ_s="
            f"{transition_τ} ({position:.0%} through the "
            f"[{arc_start}, {τ_end}] arc) — a mid-arc transition "
            f"consistent with Resolve=Change. Distinct Dramatica "
            f"read from Judgment=Bad: the transition is the "
            f"resolve-signal; its badness is the judgment-signal."
            f"{re_note}{ic_note}",
        )
    return (
        VERDICT_PARTIAL_MATCH, position,
        f"tyrant-transition at τ_s={transition_τ} ({position:.0%} "
        f"through the arc) is very early; may read as a pre-existing "
        f"trait rather than a mid-arc shift.{re_note}{ic_note}",
    )


# ============================================================================
# Check 6 — Claim-trajectory: DSP_growth = Stop
# ============================================================================


def dsp_growth_stop_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: DSP_growth=Stop = the MC needs to stop
    doing something to resolve their arc. Macbeth's substrate
    signature is the monotonic accumulation of `killed(macbeth, X)`
    facts across the arc — he doesn't stop until he himself is
    killed. The growth=stop axis diagnoses the NEEDED cessation;
    the substrate shows the cessation never happens (until the
    external termination). This is the Change/Bad shape: the MC
    fails to grow, so the arc's resolution is catastrophic."""
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    all_τ_s = sorted({e.τ_s for e in FABULA if e.τ_s is not None})

    # Count macbeth-initiated kills at each τ_s. In Shakespeare's play
    # Macbeth personally kills Duncan; Banquo, Macduff's family are
    # killed by hired murderers under his orders. The substrate
    # encodes both as macbeth-driven via `killed(macbeth, X)` and
    # `ordered_killing(macbeth, X)` — count the union.
    kill_counts = []
    last_count = 0
    monotonic = True
    for τ in all_τ_s:
        if τ < 0:
            continue
        wf = project_world(events_in_scope=events_in_scope, up_to_τ_s=τ)
        count = sum(
            1 for p in wf
            if p.predicate in ("killed", "ordered_killing")
            and len(p.args) >= 1
            and p.args[0] == MACBETH_ENTITY_ID
        )
        if count < last_count:
            monotonic = False
        kill_counts.append((τ, count))
        last_count = count

    if not kill_counts:
        return (
            VERDICT_NEEDS_WORK, 0.0,
            "no kills found in fabula; Growth=Stop needs a "
            "cumulative activity to diagnose.",
        )

    final_count = kill_counts[-1][1]
    if monotonic and final_count >= 2:
        return (
            VERDICT_APPROVED, 1.0,
            f"killed(macbeth, X) count rises monotonically across "
            f"the arc to {final_count} by τ_s={kill_counts[-1][0]}. "
            f"Growth=Stop diagnoses the cessation the MC does not "
            f"enact; the substrate shows exactly that — the killing "
            f"never self-terminates.",
        )
    if final_count >= 2:
        return (
            VERDICT_PARTIAL_MATCH, 0.6,
            f"killed(macbeth, X) count is {final_count} but "
            f"trajectory is non-monotonic; Growth=Stop is supported "
            f"but the accumulation shape is atypical.",
        )
    return (
        VERDICT_PARTIAL_MATCH, 0.4,
        f"only {final_count} killed(macbeth, X) fact(s) at arc's "
        f"end; Growth=Stop predicts a more pronounced cumulative "
        f"shape.",
    )


# ============================================================================
# Check 7 — Claim-trajectory: Story_goal
# ============================================================================


def story_goal_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: Story_goal = 'restore Scotland's rightful
    succession and end the tyranny'. Substrate signature: the
    kingship trajectory has a three-phase shape — Duncan (rightful)
    at τ_s=0; Macbeth (usurper) for the middle; Malcolm (restored)
    at τ_s=end. The three-phase presence of `king(X, scotland)` is
    the trajectory's substrate realization."""
    τ_end = _end_τ_s()
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    all_τ_s = sorted({e.τ_s for e in FABULA if e.τ_s is not None})

    phases = {"duncan": None, "macbeth": None, "malcolm": None}
    for τ in all_τ_s:
        wf = project_world(events_in_scope=events_in_scope, up_to_τ_s=τ)
        if phases["duncan"] is None and king("duncan", "scotland") in wf:
            phases["duncan"] = τ
        if phases["macbeth"] is None and king("macbeth", "scotland") in wf:
            phases["macbeth"] = τ
        if phases["malcolm"] is None and king("malcolm", "scotland") in wf:
            phases["malcolm"] = τ

    final_world = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=τ_end,
    )
    malcolm_king_at_end = king("malcolm", "scotland") in final_world
    macbeth_king_at_end = king("macbeth", "scotland") in final_world

    all_phases_hit = all(v is not None for v in phases.values())
    phase_order = (
        phases["duncan"] is not None and phases["macbeth"] is not None
        and phases["malcolm"] is not None
        and phases["duncan"] < phases["macbeth"] < phases["malcolm"]
    )

    if (all_phases_hit and phase_order and malcolm_king_at_end
            and not macbeth_king_at_end):
        return (
            VERDICT_APPROVED, 1.0,
            f"kingship trajectory: Duncan at τ_s={phases['duncan']}, "
            f"Macbeth at τ_s={phases['macbeth']}, Malcolm at τ_s="
            f"{phases['malcolm']}; Malcolm king at τ_end={τ_end}, "
            f"Macbeth not king. Three-phase disrupt-restore shape "
            f"consistent with Story_goal (succession restored).",
        )
    if malcolm_king_at_end:
        return (
            VERDICT_PARTIAL_MATCH, 0.7,
            f"Malcolm is king at τ_end; goal lands at the moment "
            f"level, but the full three-phase trajectory "
            f"(Duncan→Macbeth→Malcolm) is incomplete: "
            f"phases={phases}.",
        )
    return (
        VERDICT_NEEDS_WORK, 0.0,
        f"Malcolm is not king at τ_end={τ_end}; Story_goal "
        f"(succession restored) not supported by substrate. "
        f"Phases reached: {phases}.",
    )


# ============================================================================
# Check 8 — Characterization: DSP_limit (pressure-shape-taxonomy-sketch-01)
# ============================================================================


def dsp_limit_optionlock_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DSP_limit. Macbeth declares Optionlock (protections
    collapse one by one). LT2 predicts convergence signals in the
    substrate: a retraction (king=False at death unwinding tyrant) and
    rule-derivable emergences (kinslayer / regicide / breach_of_hospitality
    / tyrant accreting across the arc). Delegates to
    `dsp_limit_characterization_check` in verifier_helpers."""
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
    """Claim-moment: Story_consequence = 'Scotland remains under
    Macbeth's tyranny'. Under Outcome=Success, the consequence is
    AVOIDED at τ_end. Substrate check: at τ_end, neither
    king(macbeth, scotland) nor tyrant(macbeth) should hold, and
    Malcolm should be king. Three conditions must all hold for
    the consequence to be averted."""
    τ_end = _end_τ_s()
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    final_world = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=τ_end,
    )
    macbeth_king = king("macbeth", "scotland") in final_world
    macbeth_tyrant = world_holds_derived(
        final_world, tyrant(MACBETH_ENTITY_ID), RULES,
    ) is not None
    malcolm_king = king("malcolm", "scotland") in final_world

    if not macbeth_king and not macbeth_tyrant and malcolm_king:
        return (
            VERDICT_APPROVED, 1.0,
            f"at τ_s={τ_end}: king(macbeth)=False, tyrant(macbeth) "
            f"not derivable, king(malcolm)=True. Story_consequence "
            f"(tyranny continues) is fully averted; the substrate "
            f"supports Outcome=Success.",
        )
    matches = sum(
        1 for cond in
        (not macbeth_king, not macbeth_tyrant, malcolm_king)
        if cond
    )
    strength = matches / 3
    if matches >= 2:
        return (
            VERDICT_PARTIAL_MATCH, strength,
            f"at τ_s={τ_end}: king(macbeth)={macbeth_king}, "
            f"tyrant(macbeth)={macbeth_tyrant}, king(malcolm)="
            f"{malcolm_king}. {matches}/3 consequence-avoidance "
            f"conditions hold; partial averting.",
        )
    return (
        VERDICT_NEEDS_WORK, strength,
        f"at τ_s={τ_end}: {matches}/3 consequence-avoidance "
        f"conditions hold (king(macbeth)={macbeth_king}, "
        f"tyrant(macbeth)={macbeth_tyrant}, king(malcolm)="
        f"{malcolm_king}). Consequence not averted.",
    )


# ============================================================================
# Orchestration — run all four checks; build VerificationReviews directly
# ============================================================================
#
# The Template-layer upper records (DomainAssignment, DynamicStoryPoint)
# do not carry Lowerings binding them directly to substrate (per L1 /
# TEMPLATE_COUPLING_DECLARATIONS: none of these records has a
# Realization coupling). The three primitives in verification.py filter
# by `lw.upper_record == upper_ref` — so passing LOWERINGS would find
# no Template-record Lowerings and either short-circuit
# (verify_characterization returns None) or yield an empty context
# tuple (Claim-trajectory / Claim-moment). The checks above capture
# their substrate scope in their closures and do not depend on the
# primitive filtering out Lowerings for them. The orchestrator builds
# VerificationReview records directly, with reviewer_id tagged to the
# coupling kind being asserted.


def _wrap_check(
    upper_dialect: str,
    upper_record_id: str,
    check_fn: Callable,
    reviewer_id: str,
    *,
    reviewed_at_τ_a: int = 0,
) -> VerificationReview:
    """Run a check function and wrap its result in a VerificationReview.
    All Template-layer checks follow this shape."""
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
    """Run the Template-layer verifier checks for Macbeth. Returns a
    tuple of VerificationReview records.

    Check inventory (9 checks across all three primitives):
    - Characterization: DA_mc, DSP_approach, DSP_limit
    - Claim-moment: DSP_outcome, Story_consequence
    - Claim-trajectory: DSP_judgment, DSP_resolve, DSP_growth,
      Story_goal
    """
    return (
        _wrap_check(
            "dramatica-complete", "DA_mc",
            mc_throughline_activity_domain_check,
            reviewer_id="verifier:characterization:domain-assignment",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_approach",
            macbeth_do_er_approach_check,
            reviewer_id="verifier:characterization:dsp-approach",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_limit",
            dsp_limit_optionlock_check,
            reviewer_id="verifier:characterization:dsp-limit",
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
        _wrap_check(
            "dramatica-complete", "DSP_resolve",
            dsp_resolve_change_trajectory_check,
            reviewer_id="verifier:claim-trajectory:dsp-resolve",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_growth",
            dsp_growth_stop_trajectory_check,
            reviewer_id="verifier:claim-trajectory:dsp-growth",
        ),
        _wrap_check(
            "dramatica-complete", "Story_goal",
            story_goal_trajectory_check,
            reviewer_id="verifier:claim-trajectory:story-goal",
        ),
        _wrap_check(
            "dramatica-complete", "Story_consequence",
            story_consequence_moment_check,
            reviewer_id="verifier:claim-moment:story-consequence",
        ),
    )


if __name__ == "__main__":
    reviews = run()
    print(f"=== Macbeth dramatica-complete → substrate verifier ===")
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
