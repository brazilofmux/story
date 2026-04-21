"""
compiler_stage_3.py — POCL-in-Python planner spike per compilation-
stage-3-sketch-01.

Scope (spike): one Oedipus precondition-gap closure. Two operator
schemas (travel, kills). Propositional + typed state. Regression-
from-goal search with variable enumeration against the state's
ground-term universe. No epistemic / temporal / relational state;
OQ1 binds if a follow-on spike needs it.

Public API:
    OperatorSchema — action schema with params, preconditions,
                     add_effects, del_effects.
    PlanningGoal   — target operator + partial bindings.
    PlanningError  — structured failure per CS6 (mirrors stage 2's
                     InfeasibilityError pattern).
    plan_to_goal(...) — the planner entry function. Returns either
                        a Tuple[Event, ...] (success) or a
                        PlanningError (infeasibility).

Convention: variables are UPPERCASE-leading strings (AGENT, KILLER,
LOC). Ground terms are lowercase (oedipus, crossroads, sword).

Never raises on infeasibility — CS6's "loud" is structured, not
exceptional. ValueError is raised only on malformed inputs
(empty operator name, non-variable params).
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, FrozenSet, Optional, Tuple, Union

from story_engine.core.substrate import (
    CANONICAL_LABEL,
    Event,
    EventStatus,
    Prop,
    WorldEffect,
)


# ============================================================================
# Public types
# ============================================================================


@dataclass(frozen=True)
class OperatorSchema:
    """An action schema. Params are formal variables bound by caller
    or planner; preconditions must hold immediately before the action;
    add_effects are asserted and del_effects retracted by the action.

    Schema variables are UPPERCASE-leading strings. A precondition
    may reference the operator's params OR introduce additional free
    variables; the planner binds free variables via unification
    against the state's ground-term universe."""
    name: str
    params: Tuple[str, ...]
    preconditions: Tuple[Prop, ...]
    add_effects: Tuple[Prop, ...]
    del_effects: Tuple[Prop, ...]

    def __post_init__(self):
        if not self.name:
            raise ValueError("OperatorSchema.name must be non-empty")
        for param in self.params:
            if not _is_var(param):
                raise ValueError(
                    f"OperatorSchema {self.name!r}: param {param!r} "
                    f"must be a variable (UPPERCASE-leading string)"
                )


@dataclass(frozen=True)
class PlanningGoal:
    """A planning target: apply `operator` as the final action, with
    the provided `bindings` for its params and/or free variables.
    Unbound variables are resolved by the planner via enumeration
    against the start state's ground-term universe."""
    operator: OperatorSchema
    bindings: Dict[str, str]


@dataclass(frozen=True)
class PlanningError:
    """Structured failure from the planner per CS6. Mirrors stage
    2's InfeasibilityError in shape (code / constraints / message /
    relaxations). Compiler-layer, not verification-layer; distinct
    from ArObservation by architectural separation."""
    code: str
    goal: str
    unsatisfied_preconditions: Tuple[str, ...]
    message: str
    relaxations: Tuple[str, ...] = ()


# Depth bound on recursive goal regression. The spike's worked example
# needs depth 2 (goal → travel); 4 gives slack without blowing up the
# Cartesian enumeration when semantically-nonsensical variable bindings
# cascade (e.g., LOC=oedipus → the goal at(oedipus, oedipus) loops
# unless _achieve's visited-guard catches it — which it does, but
# with max_depth=8 and universe=6 the search still explores ~6^8 paths
# before all dead-end).
_MAX_PLAN_DEPTH = 4


# ============================================================================
# Public entry
# ============================================================================


def plan_to_goal(
    start_state: FrozenSet[Prop],
    goal: PlanningGoal,
    operators: Tuple[OperatorSchema, ...],
) -> Union[Tuple[Event, ...], PlanningError]:
    """Plan to achieve `goal.operator` with `goal.bindings` from
    `start_state` using the given operator library. Returns either
    a tuple of substrate `Event` records (success) or a
    `PlanningError` (failure).

    Deterministic: given identical inputs, produces identical
    outputs. The enumeration order over ground-term universes is
    sorted alphabetically; the first valid plan found is returned.
    """
    if not isinstance(start_state, (set, frozenset)):
        raise ValueError(
            "start_state must be a set or frozenset of Prop records"
        )
    start_state = frozenset(start_state)

    # Free variables in goal.operator's preconditions + unbound params.
    all_free_vars: set = set()
    for p in goal.operator.preconditions:
        for arg in p.args:
            if _is_var(arg) and arg not in goal.bindings:
                all_free_vars.add(arg)
    for param in goal.operator.params:
        if param not in goal.bindings:
            all_free_vars.add(param)

    universe = _extract_ground_terms(start_state)
    if not universe:
        return PlanningError(
            code="empty_universe",
            goal=_goal_repr(goal),
            unsatisfied_preconditions=(),
            message=(
                "start_state contains no ground terms; planner has "
                "nothing to bind free variables against"
            ),
        )

    # Enumerate bindings for free variables.
    for ext in _enumerate_variable_bindings(all_free_vars, universe):
        full_bindings = {**goal.bindings, **ext}
        plan_steps = _plan_with_bindings(
            full_bindings, goal.operator, start_state, operators,
            _MAX_PLAN_DEPTH,
        )
        if plan_steps is not None:
            return _plan_steps_to_events(plan_steps)

    # No binding succeeded. Summarize which preconditions couldn't be
    # satisfied under any binding.
    unsatisfied = tuple(
        _prop_repr(_ground_prop(p, goal.bindings))
        for p in goal.operator.preconditions
    )
    return PlanningError(
        code="no_plan_found",
        goal=_goal_repr(goal),
        unsatisfied_preconditions=unsatisfied,
        message=(
            f"no plan found for goal {_goal_repr(goal)}; search "
            f"exhausted {len(universe)} ground terms across free "
            f"variables {sorted(all_free_vars)}"
        ),
        relaxations=(
            "provide explicit bindings for free variables in goal",
            "add an operator whose add_effects include an "
            "unsatisfied precondition",
            "extend start_state to directly satisfy one or more "
            "preconditions",
        ),
    )


# ============================================================================
# Variable / unification / grounding helpers
# ============================================================================


def _is_var(arg) -> bool:
    """Variables are UPPERCASE-leading strings. 'KILLER', 'LOC' are
    variables; 'oedipus', 'crossroads' are ground."""
    return isinstance(arg, str) and len(arg) > 0 and arg[0].isupper()


def _unify_prop(
    p1: Prop, p2: Prop, bindings: Dict[str, str],
) -> Optional[Dict[str, str]]:
    """Attempt to unify two propositions under the given bindings.
    Returns extended bindings on success, None on failure."""
    if p1.predicate != p2.predicate:
        return None
    if len(p1.args) != len(p2.args):
        return None
    b = dict(bindings)
    for a1, a2 in zip(p1.args, p2.args):
        b = _unify_term(a1, a2, b)
        if b is None:
            return None
    return b


def _unify_term(t1, t2, bindings):
    """Unify two terms (arg positions in a Prop). Walks through
    existing bindings first."""
    # Walk through chain bindings.
    while _is_var(t1) and t1 in bindings:
        t1 = bindings[t1]
    while _is_var(t2) and t2 in bindings:
        t2 = bindings[t2]
    if t1 == t2:
        return bindings
    if _is_var(t1):
        return {**bindings, t1: t2}
    if _is_var(t2):
        return {**bindings, t2: t1}
    return None


def _ground_prop(p: Prop, bindings: Dict[str, str]) -> Prop:
    """Substitute variable args via bindings. Unbound vars remain."""
    args = tuple(
        bindings.get(a, a) if _is_var(a) else a
        for a in p.args
    )
    return Prop(predicate=p.predicate, args=args)


def _is_fully_ground(p: Prop) -> bool:
    return all(not _is_var(a) for a in p.args)


def _extract_ground_terms(state: FrozenSet[Prop]) -> FrozenSet[str]:
    """Every non-variable string appearing as an arg in any prop in
    `state`. The planner enumerates free variables over this set."""
    terms = set()
    for prop in state:
        for arg in prop.args:
            if isinstance(arg, str) and not _is_var(arg):
                terms.add(arg)
    return frozenset(terms)


def _enumerate_variable_bindings(free_vars, universe):
    """Yield each Cartesian-product assignment of free_vars against
    universe, in deterministic (sorted) order."""
    vars_list = sorted(free_vars)
    ground_list = sorted(universe)
    for values in product(ground_list, repeat=len(vars_list)):
        yield dict(zip(vars_list, values))


# ============================================================================
# Plan-step application
# ============================================================================


def _apply_plan_steps(
    steps: Tuple, state: FrozenSet[Prop],
) -> FrozenSet[Prop]:
    """Apply each (operator, bindings) step's effects to state in
    order. del_effects first, then add_effects (classical STRIPS
    convention)."""
    cur = set(state)
    for op, bindings in steps:
        for del_eff in op.del_effects:
            cur.discard(_ground_prop(del_eff, bindings))
        for add_eff in op.add_effects:
            cur.add(_ground_prop(add_eff, bindings))
    return frozenset(cur)


# ============================================================================
# Planner (regression from goal)
# ============================================================================


def _plan_with_bindings(
    bindings, goal_op, start_state, operators, max_depth,
):
    """Try to build a plan under the given (fully-free-variable-
    assigned) bindings. Returns list of (operator, bindings) steps or
    None if the binding is inconsistent with state + operator
    library."""
    grounded_preconds = [
        _ground_prop(p, bindings) for p in goal_op.preconditions
    ]
    # Every precondition must be fully grounded by this binding for the
    # goal action to be applicable. If not, this binding is inconsistent.
    for p in grounded_preconds:
        if not _is_fully_ground(p):
            return None

    plan: list = []
    state = set(start_state)
    for p in grounded_preconds:
        if p in state:
            continue
        sub = _achieve(
            p, frozenset(state), operators, max_depth, frozenset(),
        )
        if sub is None:
            return None
        plan.extend(sub)
        state = set(_apply_plan_steps(tuple(sub), frozenset(state)))

    # Sanity: every precondition now satisfied.
    for p in grounded_preconds:
        if p not in state:
            return None

    return plan + [(goal_op, dict(bindings))]


def _achieve(
    target: Prop,
    state: FrozenSet[Prop],
    operators: Tuple[OperatorSchema, ...],
    max_depth: int,
    visited: FrozenSet[Prop],
) -> Optional[list]:
    """Return a list of (operator, bindings) steps that achieve
    `target` from `state`, or None if no operator library + depth
    combination can. Caller is responsible for ensuring `target` is
    fully ground.

    `visited` is the set of targets currently on the recursion stack;
    re-entering a target short-circuits to None (cycle detection).
    Without this guard, free-variable enumeration producing
    semantically-nonsensical subgoals (e.g., at(oedipus, oedipus))
    recurses indefinitely until max_depth."""
    if target in visited:
        return None
    if max_depth <= 0:
        return None
    if target in state:
        return []

    new_visited = visited | {target}

    # Find operators whose add_effects can unify with target.
    for op in operators:
        for add_eff in op.add_effects:
            bindings = _unify_prop(add_eff, target, {})
            if bindings is None:
                continue
            # Free variables remaining in the operator's preconditions
            # after partial binding from the unification.
            grounded_preconds = [
                _ground_prop(p, bindings) for p in op.preconditions
            ]
            free_vars_remaining: set = set()
            for gp in grounded_preconds:
                for arg in gp.args:
                    if _is_var(arg):
                        free_vars_remaining.add(arg)

            def _try(full_b: dict):
                full_grounded = [
                    _ground_prop(p, full_b) for p in op.preconditions
                ]
                if not all(_is_fully_ground(p) for p in full_grounded):
                    return None
                subplan: list = []
                cur_state = set(state)
                for p in full_grounded:
                    if p in cur_state:
                        continue
                    sub = _achieve(
                        p, frozenset(cur_state), operators,
                        max_depth - 1, new_visited,
                    )
                    if sub is None:
                        return None
                    subplan.extend(sub)
                    cur_state = set(_apply_plan_steps(
                        tuple(sub), frozenset(cur_state),
                    ))
                return subplan + [(op, full_b)]

            if free_vars_remaining:
                universe = _extract_ground_terms(state)
                for ext in _enumerate_variable_bindings(
                    free_vars_remaining, universe,
                ):
                    full_b = {**bindings, **ext}
                    result = _try(full_b)
                    if result is not None:
                        return result
            else:
                result = _try(bindings)
                if result is not None:
                    return result
    return None


# ============================================================================
# Plan steps -> substrate Event records
# ============================================================================


def _plan_steps_to_events(plan_steps) -> Tuple[Event, ...]:
    """Each (operator, bindings) becomes a substrate.Event record.
    participants dict is built from the operator's params. effects
    tuple mirrors the operator's add/del effects as WorldEffect
    records. τ_s is monotonic negative (pre-play); τ_a is the plan-
    step ordinal. status=PROVISIONAL; branches=canonical only."""
    events: list = []
    for i, (op, bindings) in enumerate(plan_steps):
        participants = {
            param: bindings[param]
            for param in op.params
            if param in bindings
        }
        effects = []
        for add in op.add_effects:
            effects.append(WorldEffect(
                prop=_ground_prop(add, bindings), asserts=True,
            ))
        for d in op.del_effects:
            effects.append(WorldEffect(
                prop=_ground_prop(d, bindings), asserts=False,
            ))
        preconditions = tuple(
            _ground_prop(p, bindings) for p in op.preconditions
        )
        event = Event(
            id=f"planned_{op.name}_{i + 1:02d}",
            type=op.name,
            τ_s=-100 + i,
            τ_a=i + 1,
            participants=participants,
            effects=tuple(effects),
            preconditions=preconditions,
            status=EventStatus.PROVISIONAL,
            branches=frozenset({CANONICAL_LABEL}),
        )
        events.append(event)
    return tuple(events)


# ============================================================================
# String rendering helpers (for error messages)
# ============================================================================


def _prop_repr(p: Prop) -> str:
    return f"{p.predicate}({', '.join(repr(a) for a in p.args)})"


def _goal_repr(goal: PlanningGoal) -> str:
    param_strs = []
    for param in goal.operator.params:
        if param in goal.bindings:
            param_strs.append(f"{param}={goal.bindings[param]}")
        else:
            param_strs.append(f"{param}=?")
    return f"{goal.operator.name}({', '.join(param_strs)})"
