"""
compiler_stage_3.py — POCL-in-Python planner spike per compilation-
stage-3-sketch-01 + sketch-02.

Scope (spike): Oedipus precondition-gap closures. Operator library
grown from sketch-01's (travel, kills) to sketch-02's (travel,
kills, acquire). Propositional + typed state per sketch-02 S3P8 —
every operator variable carries a type; ground terms assert their
types via state `type/2` propositions; enumeration is type-aware.

Public API:
    OperatorSchema — action schema with params, variable_types,
                     preconditions, add_effects, del_effects.
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
(empty operator name, non-variable params, missing variable_types
entries).

Per sketch-02 S3P8: visited-set guard in _achieve is demoted to
defensive belt-and-suspenders. Under typed enumeration the guard
should not fire; a module-level counter tracks firings to prove
(or disprove) that claim.
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
    against type-compatible ground terms from the state.

    Per sketch-02 S3P8, every variable (param or free) must have a
    type declared in `variable_types`. Types drive the planner's
    enumeration — a variable typed `location` binds only against
    terms asserted as `location` in the state's `type/2`
    propositions."""
    name: str
    params: Tuple[str, ...]
    variable_types: Dict[str, str]
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
        # S3P8 — every variable referenced anywhere in the schema
        # must have a declared type.
        vars_used: set = set()
        for p in self.preconditions + self.add_effects + self.del_effects:
            for arg in p.args:
                if _is_var(arg):
                    vars_used.add(arg)
        vars_used.update(self.params)
        for v in vars_used:
            if v not in self.variable_types:
                raise ValueError(
                    f"OperatorSchema {self.name!r}: variable {v!r} "
                    f"used in schema but missing from variable_types"
                )
            if not self.variable_types[v]:
                raise ValueError(
                    f"OperatorSchema {self.name!r}: variable_types["
                    f"{v!r}] must be a non-empty type name"
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

    type_registry = _build_type_registry(start_state)
    if not type_registry:
        return PlanningError(
            code="empty_universe",
            goal=_goal_repr(goal),
            unsatisfied_preconditions=(),
            message=(
                "start_state contains no type/2 propositions; typed "
                "enumeration has no terms to bind free variables "
                "against. Assert types via Prop('type', (term, "
                "type_name))."
            ),
        )

    # Enumerate bindings for free variables (typed; sketch-02 S3P8).
    for ext in _enumerate_variable_bindings(
        all_free_vars, goal.operator.variable_types, type_registry,
    ):
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
            f"exhausted typed enumeration across "
            f"{len(type_registry)} typed terms for free variables "
            f"{sorted(all_free_vars)}"
        ),
        relaxations=(
            "provide explicit bindings for free variables in goal",
            "add an operator whose add_effects include an "
            "unsatisfied precondition",
            "extend start_state to directly satisfy one or more "
            "preconditions",
            "verify that type/2 assertions exist in start_state "
            "for all ground terms the planner should consider",
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


def _build_type_registry(state: FrozenSet[Prop]) -> Dict[str, str]:
    """Map each ground term to its declared type per sketch-02 S3P8.

    Extracted from state `Prop('type', (term, type_name))` assertions.
    Terms without type assertions are absent from the registry;
    typed enumeration treats them as invisible (no binding is
    proposed against them). This is intentional — the spike's state
    is expected to assert types on every term it wants the planner
    to consider."""
    registry: Dict[str, str] = {}
    for p in state:
        if p.predicate == "type" and len(p.args) == 2:
            term, type_name = p.args
            if (isinstance(term, str) and not _is_var(term)
                    and isinstance(type_name, str)):
                registry[term] = type_name
    return registry


def _enumerate_variable_bindings(
    free_vars,
    variable_types: Dict[str, str],
    type_registry: Dict[str, str],
):
    """Typed Cartesian enumeration per sketch-02 S3P8.

    For each free variable V with declared type T, enumerate only
    over terms whose state-asserted type is T. If no term has the
    required type, the product is empty and no bindings yield.

    Deterministic: sorted order by variable name and by term."""
    terms_by_type: Dict[str, list] = {}
    for term, type_name in type_registry.items():
        terms_by_type.setdefault(type_name, []).append(term)
    for v in terms_by_type:
        terms_by_type[v].sort()

    vars_list = sorted(free_vars)
    lists_for_product: list = []
    for v in vars_list:
        required_type = variable_types.get(v)
        if required_type is None:
            # No type declared for this variable. Under sketch-02
            # this should not happen (validation requires types) —
            # but defensively, treat as zero-candidate to surface
            # the misconfiguration as infeasibility rather than
            # a crash.
            lists_for_product.append([])
        else:
            lists_for_product.append(terms_by_type.get(required_type, []))

    for values in product(*lists_for_product):
        yield dict(zip(vars_list, values))


# Visited-set-guard firing counter per sketch-02 S3P8. Under typed
# enumeration this should stay at 0; the counter provides evidence
# for the forcing function S3P-OQ9 "when is the guard removable?".
_VISITED_GUARD_FIRES: int = 0


def visited_guard_fires() -> int:
    """Observable counter for tests. Returns the number of times
    _achieve has short-circuited on its visited-set guard since the
    last reset."""
    return _VISITED_GUARD_FIRES


def reset_visited_guard_counter() -> None:
    """Tests call this before invoking the planner to isolate
    per-test firing counts."""
    global _VISITED_GUARD_FIRES
    _VISITED_GUARD_FIRES = 0


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
    type_registry = _build_type_registry(start_state)
    for p in grounded_preconds:
        if p in state:
            continue
        sub = _achieve(
            p, frozenset(state), operators, max_depth,
            frozenset(), type_registry,
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
    type_registry: Dict[str, str],
) -> Optional[list]:
    """Return a list of (operator, bindings) steps that achieve
    `target` from `state`, or None if no operator library + depth
    combination can. Caller is responsible for ensuring `target` is
    fully ground.

    Per sketch-02 S3P8, `visited` is defensive belt-and-suspenders —
    typed enumeration should prevent the nonsensical cascades that
    visited originally caught. Firings are counted via the
    module-level _VISITED_GUARD_FIRES counter for forcing-function
    S3P-OQ9 evidence."""
    global _VISITED_GUARD_FIRES
    if target in visited:
        _VISITED_GUARD_FIRES += 1
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
                        max_depth - 1, new_visited, type_registry,
                    )
                    if sub is None:
                        return None
                    subplan.extend(sub)
                    cur_state = set(_apply_plan_steps(
                        tuple(sub), frozenset(cur_state),
                    ))
                return subplan + [(op, full_b)]

            if free_vars_remaining:
                for ext in _enumerate_variable_bindings(
                    free_vars_remaining, op.variable_types,
                    type_registry,
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
