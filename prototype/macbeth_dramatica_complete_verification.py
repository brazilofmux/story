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
from substrate import (
    Entity, Event, CANONICAL,
    project_world, in_scope,
    world_holds_derived, world_holds_literal,
)
from macbeth import (
    FABULA, ENTITIES, RULES, ALL_BRANCHES,
    tyrant, dead, killed, ordered_killing,
)

# Dramatic-side imports.
from dramatic import Throughline, Character
from macbeth_dramatic import THROUGHLINES, CHARACTERS, STORY

# Template-side imports.
from dramatica_template import (
    DomainAssignment, DynamicStoryPoint, DSPAxis,
    Domain, Approach, Outcome, Judgment,
)
from macbeth_dramatica_complete import (
    DOMAIN_ASSIGNMENTS, DYNAMIC_STORY_POINTS,
)

# Lowering + verifier-primitive machinery.
from lowering import (
    CrossDialectRef, cross_ref, LoweringStatus,
)
from macbeth_lowerings import LOWERINGS
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
    internal-state-shaped per EK2 (structural predicate on
    participants and effects, not a type-string set)."""
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
            f"events are external-action-shaped (EK2); the mix is "
            f"not decisively Activity-flavored.",
        )
    return (
        VERDICT_NEEDS_WORK, ratio,
        f"only {action_count}/{total} ({ratio:.0%}) MC-Throughline "
        f"events are external-action-shaped per EK2; Activity domain "
        f"classification is weakly supported by substrate.",
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
    """Run the four Template-layer verifier checks. Returns a tuple
    of VerificationReview records."""
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
