"""
compiler.py — story-engine compiler module per compilation-sketch-01.

Current scope: stage 2 only (feasibility gate), per compilation-
stage-2-sketch-01. This module houses the compiler's public entry
points and grows as additional stages (1 / 3 / 4) land.

Architectural posture per compilation-sketch-01 CS1: the compiler is
a function, not an interactive process. Given identical inputs, it
produces identical outputs. No I/O, no randomness, no LLM.

Per CS6: infeasibility is loud but *structured*, not exceptional.
Callers receive a FeasibilityResult and dispatch on `is_feasible`.
Exceptions are reserved for malformed inputs.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple

from story_engine.core.aristotelian import ArMythos


# Default per-event word-count floor. compilation-sketch-01 CS4 quotes
# this as "empirically ~200 words; probably OQ-able." See
# compilation-stage-2-sketch-01 S2F-OQ1 for the forcing function that
# will decide the real value.
DEFAULT_W_MIN_PER_EVENT = 200


@dataclass(frozen=True)
class InfeasibilityError:
    """One structured error from a compiler-stage feasibility check,
    per compilation-sketch-01 CS6. Named fields match CS6's
    commitments: which constraints participate in the conflict and
    minimally-sufficient relaxations when computable.

    Distinct from verification-layer ArObservation by deliberate
    architectural separation (compiler-layer vs verification-layer).
    See compilation-stage-2-sketch-01 S2F4 for the rationale."""
    code: str
    conflicting_constraints: Tuple[str, ...]
    message: str
    relaxations: Tuple[str, ...] = ()


@dataclass(frozen=True)
class FeasibilityResult:
    """Outcome of stage-2 feasibility for one (mythos, word_budget)
    pair per compilation-stage-2-sketch-01 S2F4. Echo fields
    (word_budget, W_min_per_event) preserve the full arithmetic
    picture for callers without recomputation.

    `aggregate_max_events == 0` is the sentinel for "unbounded" — at
    least one phase has `max_event_count == 0`, so the aggregate
    ceiling is effectively infinite. Matches the Aristotelian
    field convention (0 = unbounded)."""
    is_feasible: bool
    aggregate_min_events: int
    aggregate_max_events: int
    min_word_floor: int
    word_budget: int
    W_min_per_event: int
    errors: Tuple[InfeasibilityError, ...] = ()


def stage_2_feasibility(
    mythos: ArMythos,
    *,
    word_budget: int,
    W_min_per_event: int = DEFAULT_W_MIN_PER_EVENT,
) -> FeasibilityResult:
    """Stage-2 feasibility gate for one Aristotelian mythos against
    a word budget. Per compilation-sketch-01 CS4 and compilation-
    stage-2-sketch-01 (S2F1-S2F6).

    Pre-planner arithmetic gate. Returns a FeasibilityResult without
    raising for infeasibility. CS6's "loud" is structured-error, not
    exceptional. Exceptions are reserved for malformed inputs —
    `word_budget < 0` or `W_min_per_event <= 0`.

    Aristotelian-only (S2F6). Extensions to Save-the-Cat and
    Dramatica deferred per S2F-OQ3, S2F-OQ4.

    The per-phase floor per S2F2:
        contribution = phase.min_event_count if set else len(scope_event_ids)
    The aggregate floor is Σ contributions; min_word_floor is
    aggregate × W_min_per_event. The budget is feasible iff
    word_budget ≥ min_word_floor AND every phase's current authoring
    is consistent with its bounds (S2F3).
    """
    if word_budget < 0:
        raise ValueError(
            f"word_budget must be non-negative; got {word_budget}"
        )
    if W_min_per_event <= 0:
        raise ValueError(
            f"W_min_per_event must be positive; got {W_min_per_event}"
        )

    errors: list = []

    # S2F3 — per-phase current-authoring vs bounds. Orthogonal to the
    # budget check. Delegates to A7.12 semantics; emits stage-2-phrased
    # errors so compiler callers receive a compiler-shaped diagnostic.
    for phase in mythos.phases:
        authored = len(phase.scope_event_ids)
        if phase.min_event_count < 0:
            errors.append(InfeasibilityError(
                code="phase_min_negative",
                conflicting_constraints=(
                    f"phases[{phase.id!r}].min_event_count="
                    f"{phase.min_event_count}",
                ),
                message=(
                    f"Phase {phase.id!r}: "
                    f"min_event_count={phase.min_event_count} "
                    f"must be non-negative"
                ),
                relaxations=(
                    f"raise phases[{phase.id!r}].min_event_count to >= 0",
                ),
            ))
        if phase.max_event_count < 0:
            errors.append(InfeasibilityError(
                code="phase_max_negative",
                conflicting_constraints=(
                    f"phases[{phase.id!r}].max_event_count="
                    f"{phase.max_event_count}",
                ),
                message=(
                    f"Phase {phase.id!r}: "
                    f"max_event_count={phase.max_event_count} "
                    f"must be non-negative"
                ),
                relaxations=(
                    f"raise phases[{phase.id!r}].max_event_count to >= 0",
                ),
            ))
        if (phase.min_event_count > 0
                and phase.max_event_count > 0
                and phase.min_event_count > phase.max_event_count):
            errors.append(InfeasibilityError(
                code="phase_bounds_inverted",
                conflicting_constraints=(
                    f"phases[{phase.id!r}].min_event_count="
                    f"{phase.min_event_count}",
                    f"phases[{phase.id!r}].max_event_count="
                    f"{phase.max_event_count}",
                ),
                message=(
                    f"Phase {phase.id!r}: "
                    f"min_event_count={phase.min_event_count} > "
                    f"max_event_count={phase.max_event_count}"
                ),
                relaxations=(
                    f"raise phases[{phase.id!r}].max_event_count to "
                    f">= {phase.min_event_count}",
                    f"lower phases[{phase.id!r}].min_event_count to "
                    f"<= {phase.max_event_count}",
                ),
            ))
        if (phase.min_event_count > 0
                and authored < phase.min_event_count):
            errors.append(InfeasibilityError(
                code="phase_authoring_below_min",
                conflicting_constraints=(
                    f"phases[{phase.id!r}].min_event_count="
                    f"{phase.min_event_count}",
                    f"len(phases[{phase.id!r}].scope_event_ids)="
                    f"{authored}",
                ),
                message=(
                    f"Phase {phase.id!r}: authored {authored} events "
                    f"but min_event_count={phase.min_event_count}"
                ),
                relaxations=(
                    f"author >= "
                    f"{phase.min_event_count - authored} additional "
                    f"events in phase {phase.id!r}",
                    f"lower phases[{phase.id!r}].min_event_count to "
                    f"<= {authored}",
                ),
            ))
        if (phase.max_event_count > 0
                and authored > phase.max_event_count):
            errors.append(InfeasibilityError(
                code="phase_authoring_above_max",
                conflicting_constraints=(
                    f"phases[{phase.id!r}].max_event_count="
                    f"{phase.max_event_count}",
                    f"len(phases[{phase.id!r}].scope_event_ids)="
                    f"{authored}",
                ),
                message=(
                    f"Phase {phase.id!r}: authored {authored} events "
                    f"but max_event_count={phase.max_event_count}"
                ),
                relaxations=(
                    f"remove >= "
                    f"{authored - phase.max_event_count} events from "
                    f"phase {phase.id!r}",
                    f"raise phases[{phase.id!r}].max_event_count to "
                    f">= {authored}",
                ),
            ))

    # S2F2 — aggregate min / max event counts (fallback-aware).
    aggregate_min_events = 0
    aggregate_max_events_if_bounded = 0
    has_unbounded_max = False
    for phase in mythos.phases:
        authored = len(phase.scope_event_ids)
        if phase.min_event_count > 0:
            aggregate_min_events += phase.min_event_count
        else:
            aggregate_min_events += authored  # S2F2 fallback
        if phase.max_event_count > 0:
            aggregate_max_events_if_bounded += phase.max_event_count
        else:
            has_unbounded_max = True
    aggregate_max_events = (
        0 if has_unbounded_max else aggregate_max_events_if_bounded
    )

    min_word_floor = aggregate_min_events * W_min_per_event

    # CS4 budget-floor check.
    if word_budget < min_word_floor:
        deficit = min_word_floor - word_budget
        event_deficit = math.ceil(deficit / W_min_per_event)
        errors.append(InfeasibilityError(
            code="budget_below_floor",
            conflicting_constraints=(
                f"word_budget={word_budget}",
                f"aggregate_min_events={aggregate_min_events}",
                f"W_min_per_event={W_min_per_event}",
            ),
            message=(
                f"word_budget={word_budget} is below min_word_floor="
                f"{min_word_floor} (= aggregate_min_events="
                f"{aggregate_min_events} x W_min_per_event="
                f"{W_min_per_event}); deficit {deficit} words"
            ),
            relaxations=(
                f"increase word_budget by >= {deficit} words",
                f"reduce aggregate phase.min_event_count by >= "
                f"{event_deficit} events across all phases",
            ),
        ))

    return FeasibilityResult(
        is_feasible=not errors,
        aggregate_min_events=aggregate_min_events,
        aggregate_max_events=aggregate_max_events,
        min_word_floor=min_word_floor,
        word_budget=word_budget,
        W_min_per_event=W_min_per_event,
        errors=tuple(errors),
    )
