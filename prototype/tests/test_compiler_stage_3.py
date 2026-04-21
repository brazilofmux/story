"""
test_compiler_stage_3.py — tests for the POCL planner spike per
compilation-stage-3-sketch-01.

The worked example (Oedipus crossroads) is the primary success pin.
Synthetic fixtures cover unification, operator-schema validation,
infeasibility detection, degenerate cases, and substrate event
emission.

Run:
    cd prototype
    python3 -m tests.test_compiler_stage_3
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.substrate import (
    CANONICAL_LABEL,
    Event,
    EventStatus,
    Prop,
    WorldEffect,
)
from story_engine.core.compiler_stage_3 import (
    OperatorSchema,
    PlanningError,
    PlanningGoal,
    plan_to_goal,
    reset_visited_guard_counter,
    visited_guard_fires,
)


# ----------------------------------------------------------------------------
# Type constants (sketch-02 S3P8)
# ----------------------------------------------------------------------------

AGENT_TYPE = "agent"
LOCATION_TYPE = "location"
OBJECT_TYPE = "object"
FACT_TYPE = "fact"          # sketch-03 S3P11


# ----------------------------------------------------------------------------
# Operator fixtures (migrated to sketch-02 typed form)
# ----------------------------------------------------------------------------


TRAVEL = OperatorSchema(
    name="travel",
    params=("AGENT", "FROM", "TO"),
    variable_types={
        "AGENT": AGENT_TYPE,
        "FROM": LOCATION_TYPE,
        "TO": LOCATION_TYPE,
    },
    preconditions=(
        Prop("at", ("AGENT", "FROM")),
        Prop("path", ("FROM", "TO")),
    ),
    add_effects=(Prop("at", ("AGENT", "TO")),),
    del_effects=(Prop("at", ("AGENT", "FROM")),),
)


KILLS = OperatorSchema(
    name="kills",
    params=("KILLER", "VICTIM"),
    variable_types={
        "KILLER": AGENT_TYPE,
        "VICTIM": AGENT_TYPE,
        "LOC": LOCATION_TYPE,
        "WEAPON": OBJECT_TYPE,
    },
    preconditions=(
        Prop("at", ("KILLER", "LOC")),
        Prop("at", ("VICTIM", "LOC")),
        Prop("has", ("KILLER", "WEAPON")),
        Prop("alive", ("KILLER",)),
        Prop("alive", ("VICTIM",)),
    ),
    add_effects=(Prop("dead", ("VICTIM",)),),
    del_effects=(Prop("alive", ("VICTIM",)),),
)


ACQUIRE = OperatorSchema(
    name="acquire",
    params=("AGENT", "ITEM", "LOCATION"),
    variable_types={
        "AGENT": AGENT_TYPE,
        "ITEM": OBJECT_TYPE,
        "LOCATION": LOCATION_TYPE,
    },
    preconditions=(
        Prop("at", ("AGENT", "LOCATION")),
        Prop("at", ("ITEM", "LOCATION")),
    ),
    add_effects=(Prop("has", ("AGENT", "ITEM")),),
    del_effects=(Prop("at", ("ITEM", "LOCATION")),),
)


# sketch-03 S3P12: knowledge-acquisition operator.
# S3P14 ordering: knows-of-teacher BEFORE at-preconds so the planner
# picks FACT + LOCATION that align with an existing teacher-knows
# relation, rather than spatial exploration followed by
# backtracking on FACT.
LEARN_FROM = OperatorSchema(
    name="learn_from",
    params=("STUDENT", "TEACHER", "FACT", "LOCATION"),
    variable_types={
        "STUDENT": AGENT_TYPE,
        "TEACHER": AGENT_TYPE,
        "FACT": FACT_TYPE,
        "LOCATION": LOCATION_TYPE,
    },
    preconditions=(
        Prop("knows", ("TEACHER", "FACT")),
        Prop("at", ("STUDENT", "LOCATION")),
        Prop("at", ("TEACHER", "LOCATION")),
    ),
    add_effects=(Prop("knows", ("STUDENT", "FACT")),),
    del_effects=(),
)


# sketch-03 S3P12 + S3P14: the Oedipus-vs-Sphinx event.
# `knows` precondition listed FIRST per S3P14 ordering discipline —
# otherwise the planner satisfies `at(agent, LOC)` first, then
# can't satisfy `knows(agent, fact)` without undoing location
# setup (the student must be with the teacher at DIFFERENT
# location).
DEFEAT_BY_RIDDLE = OperatorSchema(
    name="defeat_by_riddle",
    params=("AGENT", "OPPONENT"),
    variable_types={
        "AGENT": AGENT_TYPE,
        "OPPONENT": AGENT_TYPE,
        "FACT": FACT_TYPE,
        "LOC": LOCATION_TYPE,
    },
    preconditions=(
        Prop("knows", ("AGENT", "FACT")),
        Prop("at", ("AGENT", "LOC")),
        Prop("at", ("OPPONENT", "LOC")),
        Prop("alive", ("AGENT",)),
        Prop("alive", ("OPPONENT",)),
    ),
    add_effects=(Prop("dead", ("OPPONENT",)),),
    del_effects=(Prop("alive", ("OPPONENT",)),),
)


# ----------------------------------------------------------------------------
# State fixtures
# ----------------------------------------------------------------------------


def _type_assertions() -> frozenset:
    """Canonical type/2 assertions for the Oedipus spike universe.
    Migrations + new scenes compose these into their start state."""
    return frozenset({
        Prop("type", ("oedipus", AGENT_TYPE)),
        Prop("type", ("laius", AGENT_TYPE)),
        Prop("type", ("corinth", LOCATION_TYPE)),
        Prop("type", ("thebes", LOCATION_TYPE)),
        Prop("type", ("crossroads", LOCATION_TYPE)),
        Prop("type", ("sword", OBJECT_TYPE)),
    })


def _crossroads_start_state() -> frozenset:
    """Scene 1: Oedipus already has the sword. Kill gap is co-location."""
    return _type_assertions() | frozenset({
        Prop("at", ("oedipus", "corinth")),
        Prop("at", ("laius", "thebes")),
        Prop("has", ("oedipus", "sword")),
        Prop("path", ("corinth", "crossroads")),
        Prop("path", ("thebes", "crossroads")),
        Prop("alive", ("oedipus",)),
        Prop("alive", ("laius",)),
    })


def _acquire_en_route_start_state() -> frozenset:
    """Scene 2 (sketch-02 S3P10): Oedipus at Corinth unarmed; sword
    at crossroads; Laius at Thebes. Gap is both co-location AND
    weapon acquisition."""
    return _type_assertions() | frozenset({
        Prop("at", ("oedipus", "corinth")),
        Prop("at", ("laius", "thebes")),
        Prop("at", ("sword", "crossroads")),  # sword at location, not held
        Prop("path", ("corinth", "crossroads")),
        Prop("path", ("thebes", "crossroads")),
        Prop("alive", ("oedipus",)),
        Prop("alive", ("laius",)),
    })


def _type_assertions_scene_3() -> frozenset:
    """Scene 3's universe: Oedipus + Sphinx + Oracle (3 agents);
    Corinth + Delphi + thebes_gates (3 locations); riddle_answer
    (1 fact). No objects needed."""
    return frozenset({
        Prop("type", ("oedipus", AGENT_TYPE)),
        Prop("type", ("sphinx",  AGENT_TYPE)),
        Prop("type", ("oracle",  AGENT_TYPE)),
        Prop("type", ("corinth",      LOCATION_TYPE)),
        Prop("type", ("delphi",       LOCATION_TYPE)),
        Prop("type", ("thebes_gates", LOCATION_TYPE)),
        Prop("type", ("riddle_answer", FACT_TYPE)),
    })


def _sphinx_riddle_start_state() -> frozenset:
    """Scene 3 (sketch-03 S3P13): Oedipus at Corinth; Sphinx at
    thebes_gates; Oracle at Delphi knowing the riddle's answer.
    Paths route via Delphi (no direct Corinth → thebes_gates)."""
    return _type_assertions_scene_3() | frozenset({
        Prop("at", ("oedipus", "corinth")),
        Prop("alive", ("oedipus",)),
        Prop("at", ("sphinx", "thebes_gates")),
        Prop("alive", ("sphinx",)),
        Prop("at", ("oracle", "delphi")),
        Prop("alive", ("oracle",)),
        Prop("knows", ("oracle", "riddle_answer")),
        Prop("path", ("corinth", "delphi")),
        Prop("path", ("delphi", "thebes_gates")),
    })


def _sphinx_riddle_goal() -> PlanningGoal:
    """Goal for scene 3: defeat_by_riddle with AGENT/OPPONENT bound;
    FACT and LOC enumerated."""
    return PlanningGoal(
        operator=DEFEAT_BY_RIDDLE,
        bindings={"AGENT": "oedipus", "OPPONENT": "sphinx"},
    )


def _kills_oedipus_laius_goal() -> PlanningGoal:
    return PlanningGoal(
        operator=KILLS,
        bindings={"KILLER": "oedipus", "VICTIM": "laius"},
    )


# ----------------------------------------------------------------------------
# Worked example — the spike's primary success case
# ----------------------------------------------------------------------------


def test_worked_example_returns_three_event_plan():
    """Oedipus crossroads: start state has Oedipus@Corinth armed,
    Laius@Thebes; the planner must synthesize two travel events +
    the kill event. This is the spike's primary success pin — if
    this fails, the primitive mechanism doesn't work."""
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    assert isinstance(result, tuple), (
        f"expected tuple[Event, ...] on success; got "
        f"{type(result).__name__}: {result}"
    )
    assert len(result) == 3, (
        f"expected 3-event plan; got {len(result)}: "
        f"{[e.type for e in result]}"
    )


def test_worked_example_event_types_are_two_travels_plus_kills():
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    types = [e.type for e in result]
    # Two travel events (one per agent) + one kill.
    assert types.count("travel") == 2, (
        f"expected exactly two 'travel' events; got types={types}"
    )
    assert types[-1] == "kills", (
        f"final event should be 'kills'; got {types[-1]}"
    )


def test_worked_example_travel_participants_cover_both_agents():
    """The two travels must move Oedipus and Laius (in some order)
    into the shared location."""
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    travel_agents = {
        e.participants["AGENT"] for e in result if e.type == "travel"
    }
    assert travel_agents == {"oedipus", "laius"}, (
        f"travel events should move both oedipus and laius; "
        f"got agents={travel_agents}"
    )


def test_worked_example_travels_converge_on_single_location():
    """Both travel TOs must be the same location — that's the
    co-location that satisfies the kill event's precondition."""
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    tos = {
        e.participants["TO"] for e in result if e.type == "travel"
    }
    assert len(tos) == 1, (
        f"both travels should target the same location; got {tos}"
    )
    # For this start state, the only reachable co-location is 'crossroads'.
    assert tos == {"crossroads"}


def test_worked_example_kill_participants_are_oedipus_and_laius():
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    kill_event = next(e for e in result if e.type == "kills")
    assert kill_event.participants["KILLER"] == "oedipus"
    assert kill_event.participants["VICTIM"] == "laius"


def test_worked_example_cumulative_state_satisfies_preconditions_before_each_step():
    """Validates plan correctness: apply each event's effects in
    sequence; verify the next event's preconditions hold in that
    cumulative state. This is what 'valid plan' means."""
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    state = set(_crossroads_start_state())
    for event in result:
        for p in event.preconditions:
            assert p in state, (
                f"precondition {p} of {event.type} not in state "
                f"at τ_s={event.τ_s}"
            )
        # Apply this event's effects.
        for eff in event.effects:
            if eff.asserts:
                state.add(eff.prop)
            else:
                state.discard(eff.prop)


def test_worked_example_final_state_has_dead_laius():
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    state = set(_crossroads_start_state())
    for event in result:
        for eff in event.effects:
            if eff.asserts:
                state.add(eff.prop)
            else:
                state.discard(eff.prop)
    assert Prop("dead", ("laius",)) in state
    assert Prop("alive", ("laius",)) not in state


# ----------------------------------------------------------------------------
# Substrate event emission shape (CS7 — existing verifiers as type-check)
# ----------------------------------------------------------------------------


def test_emitted_events_are_substrate_event_records():
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    for e in result:
        assert isinstance(e, Event)


def test_emitted_events_are_provisional():
    """Planner output is provisional until a separate step promotes
    it. The spike does not promote."""
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    for e in result:
        assert e.status == EventStatus.PROVISIONAL


def test_emitted_events_are_on_canonical_branch():
    """Single-branch (canonical) only in the spike per S3P5."""
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    for e in result:
        assert e.branches == frozenset({CANONICAL_LABEL})


def test_emitted_events_have_monotonic_tau_s():
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    tau_s_seq = [e.τ_s for e in result]
    assert tau_s_seq == sorted(tau_s_seq), (
        f"τ_s values not monotonic: {tau_s_seq}"
    )


def test_emitted_events_have_sequential_tau_a():
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    tau_a_seq = [e.τ_a for e in result]
    assert tau_a_seq == [1, 2, 3]


def test_emitted_events_carry_world_effects():
    """WorldEffect is the substrate's world-state-update record.
    The planner emits effects in that shape."""
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    for e in result:
        assert len(e.effects) > 0
        for eff in e.effects:
            assert isinstance(eff, WorldEffect)


# ----------------------------------------------------------------------------
# Infeasibility — structured PlanningError per CS6 / S3P6
# ----------------------------------------------------------------------------


def test_weapon_removed_produces_planning_error():
    """Start state without the sword: no operator library adds 'has'
    — planner dead-ends; structured error surfaces."""
    start = frozenset(
        p for p in _crossroads_start_state()
        if not (p.predicate == "has")
    )
    result = plan_to_goal(
        start, _kills_oedipus_laius_goal(), (TRAVEL, KILLS),
    )
    assert isinstance(result, PlanningError), (
        f"expected PlanningError when weapon removed; got "
        f"{type(result).__name__}"
    )
    assert result.code == "no_plan_found"


def test_planning_error_names_unsatisfied_preconditions():
    """The error's unsatisfied_preconditions tuple lists the
    preconditions in their partially-ground form (after goal
    bindings applied, before free vars resolved)."""
    start = frozenset(
        p for p in _crossroads_start_state()
        if not (p.predicate == "has")
    )
    result = plan_to_goal(
        start, _kills_oedipus_laius_goal(), (TRAVEL, KILLS),
    )
    # Find the has(KILLER=oedipus, WEAPON) precondition — WEAPON
    # stays as a var because the enumeration couldn't bind it.
    assert any(
        "has" in p and "oedipus" in p and "WEAPON" in p
        for p in result.unsatisfied_preconditions
    ), (
        f"expected has/oedipus/WEAPON in unsatisfied_preconditions; "
        f"got {result.unsatisfied_preconditions}"
    )


def test_planning_error_offers_relaxations():
    start = frozenset(
        p for p in _crossroads_start_state()
        if not (p.predicate == "has")
    )
    result = plan_to_goal(
        start, _kills_oedipus_laius_goal(), (TRAVEL, KILLS),
    )
    assert len(result.relaxations) >= 1


def test_empty_start_state_produces_empty_universe_error():
    result = plan_to_goal(
        frozenset(), _kills_oedipus_laius_goal(), (TRAVEL, KILLS),
    )
    assert isinstance(result, PlanningError)
    assert result.code == "empty_universe"


def test_planning_error_is_frozen():
    from dataclasses import FrozenInstanceError
    err = PlanningError(
        code="x", goal="g", unsatisfied_preconditions=(),
        message="m",
    )
    try:
        err.code = "y"  # type: ignore[misc]
    except FrozenInstanceError:
        return
    raise AssertionError("PlanningError must be frozen")


# ----------------------------------------------------------------------------
# Degenerate case
# ----------------------------------------------------------------------------


def test_start_state_already_satisfies_goal_returns_one_step_plan():
    """If Oedipus and Laius are already at the crossroads in start
    state, planner should return just the kills event."""
    start = _type_assertions() | frozenset({
        Prop("at", ("oedipus", "crossroads")),
        Prop("at", ("laius", "crossroads")),
        Prop("has", ("oedipus", "sword")),
        Prop("alive", ("oedipus",)),
        Prop("alive", ("laius",)),
    })
    result = plan_to_goal(
        start, _kills_oedipus_laius_goal(), (TRAVEL, KILLS),
    )
    assert isinstance(result, tuple), (
        f"expected tuple on success; got {type(result).__name__}"
    )
    assert len(result) == 1
    assert result[0].type == "kills"


def test_fully_bound_goal_without_type_assertions_still_plans():
    """Typed enumeration is only needed when free variables remain.
    A fully bound goal should still succeed without any type/2 facts."""
    start = frozenset({
        Prop("at", ("oedipus", "corinth")),
        Prop("path", ("corinth", "thebes")),
    })
    goal = PlanningGoal(
        operator=TRAVEL,
        bindings={
            "AGENT": "oedipus",
            "FROM": "corinth",
            "TO": "thebes",
        },
    )
    result = plan_to_goal(start, goal, (TRAVEL,))
    assert isinstance(result, tuple), (
        f"expected tuple on fully-bound success; got "
        f"{type(result).__name__}: {result}"
    )
    assert len(result) == 1
    assert result[0].type == "travel"


# ----------------------------------------------------------------------------
# Unification + variable-binding
# ----------------------------------------------------------------------------


def test_goal_with_all_variables_bound_skips_enumeration():
    """If the caller binds LOC and WEAPON explicitly in the goal
    bindings, the planner doesn't need to enumerate them. Still
    produces the same 3-event plan when preconditions aren't met."""
    goal = PlanningGoal(
        operator=KILLS,
        bindings={
            "KILLER": "oedipus", "VICTIM": "laius",
            "LOC": "crossroads", "WEAPON": "sword",
        },
    )
    result = plan_to_goal(
        _crossroads_start_state(), goal, (TRAVEL, KILLS),
    )
    assert isinstance(result, tuple)
    assert len(result) == 3


def test_path_mismatch_prevents_plan():
    """Start state with no path to any shared location: infeasible."""
    start = _type_assertions() | frozenset({
        Prop("at", ("oedipus", "corinth")),
        Prop("at", ("laius", "thebes")),
        Prop("has", ("oedipus", "sword")),
        Prop("alive", ("oedipus",)),
        Prop("alive", ("laius",)),
        # No path propositions — agents can't travel anywhere.
    })
    result = plan_to_goal(
        start, _kills_oedipus_laius_goal(), (TRAVEL, KILLS),
    )
    assert isinstance(result, PlanningError)
    assert result.code == "no_plan_found"


# ----------------------------------------------------------------------------
# OperatorSchema validation (ValueError on malformed input per S3P6)
# ----------------------------------------------------------------------------


def test_operator_schema_rejects_empty_name():
    try:
        OperatorSchema(
            name="", params=("AGENT",),
            variable_types={"AGENT": AGENT_TYPE},
            preconditions=(), add_effects=(), del_effects=(),
        )
    except ValueError as e:
        assert "non-empty" in str(e).lower()
        return
    raise AssertionError("expected ValueError on empty operator name")


def test_operator_schema_rejects_lowercase_params():
    """Params must be variables (uppercase-leading)."""
    try:
        OperatorSchema(
            name="bad", params=("agent",),  # lowercase — not a var
            variable_types={"agent": AGENT_TYPE},
            preconditions=(), add_effects=(), del_effects=(),
        )
    except ValueError as e:
        assert "variable" in str(e).lower()
        return
    raise AssertionError(
        "expected ValueError on lowercase (non-variable) param"
    )


def test_operator_schema_accepts_valid_shape():
    """Smoke — the TRAVEL / KILLS schemas used throughout this test
    module construct without error."""
    assert TRAVEL.name == "travel"
    assert KILLS.name == "kills"


# ----------------------------------------------------------------------------
# Sketch-02 — typed variables (S3P8)
# ----------------------------------------------------------------------------


def test_operator_schema_rejects_missing_variable_type():
    """S3P8: every variable used in the schema must have a type
    declared in variable_types."""
    try:
        OperatorSchema(
            name="bad",
            params=("AGENT",),
            variable_types={},  # missing AGENT entry
            preconditions=(Prop("at", ("AGENT", "LOC")),),
            add_effects=(),
            del_effects=(),
        )
    except ValueError as e:
        assert "variable_types" in str(e)
        return
    raise AssertionError(
        "expected ValueError when a schema variable has no type"
    )


def test_operator_schema_rejects_empty_type_name():
    try:
        OperatorSchema(
            name="bad",
            params=("AGENT",),
            variable_types={"AGENT": ""},  # empty type name
            preconditions=(),
            add_effects=(),
            del_effects=(),
        )
    except ValueError as e:
        assert "non-empty" in str(e)
        return
    raise AssertionError(
        "expected ValueError on empty type name"
    )


def test_operator_schema_rejects_missing_free_var_type():
    """Free variables in preconditions (not in params) also need types."""
    try:
        OperatorSchema(
            name="bad",
            params=("AGENT",),
            variable_types={"AGENT": AGENT_TYPE},  # missing LOC
            preconditions=(Prop("at", ("AGENT", "LOC")),),
            add_effects=(),
            del_effects=(),
        )
    except ValueError as e:
        assert "LOC" in str(e)
        return
    raise AssertionError(
        "expected ValueError when a free variable has no type"
    )


def test_scene_1_visited_guard_firings_are_bounded():
    """Sketch-02 S3P8 characterization: typed enumeration eliminates
    nonsensical-binding cascades (e.g., LOC=oedipus producing
    at(oedipus, oedipus) goals). It does NOT eliminate visited-guard
    firings entirely — the guard still prunes sub-problem repetition
    during dead-end exploration (e.g., the planner tries LOC=corinth
    before finding LOC=crossroads; the corinth branch hits visited
    loops while backtracking). Both failure modes are load-bearing.

    This test pins: firings on scene 1 success are BOUNDED (finite),
    not that they are zero. A regression where firings explode to
    thousands would signal that typed enumeration is miscounting OR
    that a new failure mode the guard is catching has emerged."""
    reset_visited_guard_counter()
    result = plan_to_goal(
        _crossroads_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS),
    )
    assert isinstance(result, tuple)  # sanity — plan found
    fires = visited_guard_fires()
    # Loose upper bound — current implementation fires ~6. Any
    # number under ~50 is "bounded exploration"; thousands would be
    # a regression.
    assert fires < 50, (
        f"scene-1 visited-guard fires {fires} times (expected < 50); "
        f"regression in enumeration or a new failure mode"
    )


def test_start_state_without_type_assertions_produces_empty_universe():
    """S3P8: typed enumeration needs type/2 propositions in the
    start state. A state with no type assertions returns
    empty_universe even if it has other propositions."""
    start = frozenset({
        Prop("at", ("oedipus", "corinth")),
        Prop("at", ("laius", "thebes")),
        Prop("has", ("oedipus", "sword")),
        Prop("alive", ("oedipus",)),
        Prop("alive", ("laius",)),
        # No type/2 assertions.
    })
    result = plan_to_goal(
        start, _kills_oedipus_laius_goal(), (TRAVEL, KILLS),
    )
    assert isinstance(result, PlanningError)
    assert result.code == "empty_universe"


def test_typed_enumeration_ignores_wrongly_typed_terms():
    """S3P8: a KILLS goal with LOC: location should never try
    LOC=oedipus (agent-typed) during enumeration. Proof: a start
    state where the ONLY location-typed term has no path
    out should produce a 'no_plan_found' error with at-preconditions
    named — NOT hit an enumeration-driven cascade on a non-location
    LOC."""
    reset_visited_guard_counter()
    # State where the only location is 'corinth' — both agents start
    # there; no path anywhere; weapon in hand. Can LOC only be
    # corinth? Yes. But at(laius, corinth) is not in state → need
    # travel, but no path anywhere → fail.
    start = _type_assertions() | frozenset({
        Prop("at", ("oedipus", "corinth")),
        Prop("at", ("laius", "thebes")),
        Prop("has", ("oedipus", "sword")),
        Prop("alive", ("oedipus",)),
        Prop("alive", ("laius",)),
        # No path propositions.
    })
    result = plan_to_goal(
        start, _kills_oedipus_laius_goal(), (TRAVEL, KILLS),
    )
    assert isinstance(result, PlanningError)
    # The visited-guard MAY fire here (cascades like
    # achieve(at(oedipus, thebes)) → travel needing at(oedipus, ?)
    # → at(oedipus, thebes) again) — but not because of nonsensical
    # LOC=oedipus bindings. That's the point.


# ----------------------------------------------------------------------------
# Sketch-02 — acquire operator (S3P9)
# ----------------------------------------------------------------------------


def test_acquire_operator_schema_valid():
    assert ACQUIRE.name == "acquire"
    assert ACQUIRE.variable_types["AGENT"] == AGENT_TYPE
    assert ACQUIRE.variable_types["ITEM"] == OBJECT_TYPE
    assert ACQUIRE.variable_types["LOCATION"] == LOCATION_TYPE


def test_acquire_only_needs_co_location():
    """Small test: agent + item co-located, plan is just acquire."""
    start = _type_assertions() | frozenset({
        Prop("at", ("oedipus", "crossroads")),
        Prop("at", ("sword", "crossroads")),
    })
    goal = PlanningGoal(
        operator=ACQUIRE,
        bindings={
            "AGENT": "oedipus",
            "ITEM": "sword",
            "LOCATION": "crossroads",
        },
    )
    result = plan_to_goal(start, goal, (TRAVEL, ACQUIRE))
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert result[0].type == "acquire"


def test_acquire_item_not_at_location_infeasible():
    """If the item isn't where we're acquiring from, infeasible."""
    start = _type_assertions() | frozenset({
        Prop("at", ("oedipus", "corinth")),
        Prop("at", ("sword", "crossroads")),  # sword elsewhere
        Prop("path", ("corinth", "crossroads")),
    })
    goal = PlanningGoal(
        operator=ACQUIRE,
        bindings={
            "AGENT": "oedipus",
            "ITEM": "sword",
            "LOCATION": "corinth",  # wrong location
        },
    )
    result = plan_to_goal(start, goal, (TRAVEL, ACQUIRE))
    assert isinstance(result, PlanningError)
    assert result.code == "no_plan_found"


# ----------------------------------------------------------------------------
# Sketch-02 — Scene 2: "Oedipus acquires sword en route" (S3P10)
# ----------------------------------------------------------------------------


def test_scene_2_returns_four_event_plan():
    """The spike's primary sketch-02 success pin. Start state has
    Oedipus at Corinth UNARMED, sword at crossroads, Laius at Thebes.
    Planner must synthesize: two travels + one acquire + the kill."""
    result = plan_to_goal(
        _acquire_en_route_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS, ACQUIRE),
    )
    assert isinstance(result, tuple), (
        f"expected success; got {type(result).__name__}: {result}"
    )
    assert len(result) == 4, (
        f"expected 4-step plan; got {len(result)}: "
        f"{[e.type for e in result]}"
    )


def test_scene_2_plan_includes_acquire():
    """S3P10: the plan must compose the new ACQUIRE operator —
    without it, there's no way to satisfy has(oedipus, sword)
    because start state has the sword at a location, not held."""
    result = plan_to_goal(
        _acquire_en_route_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS, ACQUIRE),
    )
    types = [e.type for e in result]
    assert "acquire" in types


def test_scene_2_plan_type_sequence():
    """Valid orderings: two travels + acquire + kill. Travels can
    swap; acquire must come after oedipus's travel (to be
    co-located with sword) but before the kill (needs has)."""
    result = plan_to_goal(
        _acquire_en_route_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS, ACQUIRE),
    )
    types = [e.type for e in result]
    assert types.count("travel") == 2
    assert types.count("acquire") == 1
    assert types.count("kills") == 1
    assert types[-1] == "kills"
    # Acquire cannot be the final action, nor first (needs
    # oedipus co-located with sword first).
    acquire_idx = types.index("acquire")
    assert 0 < acquire_idx < 3


def test_scene_2_preconditions_satisfied_at_each_step():
    """Cumulative-state validity invariant: each step's
    preconditions hold in the state reached by applying all prior
    events' effects."""
    result = plan_to_goal(
        _acquire_en_route_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS, ACQUIRE),
    )
    state = set(_acquire_en_route_start_state())
    for event in result:
        for p in event.preconditions:
            assert p in state, (
                f"precondition {p} of {event.type} (τ_a={event.τ_a}) "
                f"not in state"
            )
        for eff in event.effects:
            if eff.asserts:
                state.add(eff.prop)
            else:
                state.discard(eff.prop)


def test_scene_2_final_state_has_dead_laius_and_oedipus_has_sword():
    result = plan_to_goal(
        _acquire_en_route_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS, ACQUIRE),
    )
    state = set(_acquire_en_route_start_state())
    for event in result:
        for eff in event.effects:
            if eff.asserts:
                state.add(eff.prop)
            else:
                state.discard(eff.prop)
    assert Prop("dead", ("laius",)) in state
    assert Prop("has", ("oedipus", "sword")) in state
    # And the sword is no longer at crossroads — acquire deled it.
    assert Prop("at", ("sword", "crossroads")) not in state


def test_scene_2_acquire_comes_after_oedipus_travel():
    """S3P9 interaction pin: the plan must order acquire AFTER
    oedipus's travel (since acquire needs oedipus and sword
    co-located, and sword starts at crossroads). Not strictly
    before the kill — we just require logical ordering."""
    result = plan_to_goal(
        _acquire_en_route_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS, ACQUIRE),
    )
    # Find oedipus's travel event (AGENT=oedipus) and the acquire.
    oedipus_travel_idx = next(
        i for i, e in enumerate(result)
        if e.type == "travel" and e.participants.get("AGENT") == "oedipus"
    )
    acquire_idx = next(
        i for i, e in enumerate(result) if e.type == "acquire"
    )
    assert acquire_idx > oedipus_travel_idx


def test_scene_2_visited_guard_firings_are_bounded():
    """Same characterization as scene 1 but for the 3-operator,
    4-step plan. More operators + longer plan = more dead-end
    exploration = more (but still bounded) firings."""
    reset_visited_guard_counter()
    result = plan_to_goal(
        _acquire_en_route_start_state(),
        _kills_oedipus_laius_goal(),
        (TRAVEL, KILLS, ACQUIRE),
    )
    assert isinstance(result, tuple)  # sanity
    fires = visited_guard_fires()
    # Scene 2's dead-end exploration fires the guard more than
    # scene 1's (observed ~9 vs ~6). Bound at 100 for headroom.
    assert fires < 100, (
        f"scene-2 visited-guard fires {fires} times (expected < 100); "
        f"regression in enumeration or a new failure mode"
    )


# ----------------------------------------------------------------------------
# Sketch-03 — Scene 3: Oedipus defeats the Sphinx (S3P11-S3P14)
# ----------------------------------------------------------------------------


def test_scene_3_returns_four_event_plan():
    """Primary pin: the planner synthesizes a 4-step plan for the
    Sphinx encounter — travel to Delphi, learn from Oracle, travel
    to thebes_gates, defeat Sphinx. Tests epistemic preconds via
    flat propositional knows/2 (OQ1 epistemic sub-question)."""
    result = plan_to_goal(
        _sphinx_riddle_start_state(),
        _sphinx_riddle_goal(),
        (TRAVEL, LEARN_FROM, DEFEAT_BY_RIDDLE),
    )
    assert isinstance(result, tuple), (
        f"expected tuple on success; got {type(result).__name__}: "
        f"{result}"
    )
    assert len(result) == 4, (
        f"expected 4-step plan; got {len(result)}: "
        f"{[e.type for e in result]}"
    )


def test_scene_3_plan_type_sequence():
    """Valid sequence: travel, learn_from, travel, defeat_by_riddle.
    Ordering is forced by state graph — no direct Corinth →
    thebes_gates path and no alternative knowledge source."""
    result = plan_to_goal(
        _sphinx_riddle_start_state(),
        _sphinx_riddle_goal(),
        (TRAVEL, LEARN_FROM, DEFEAT_BY_RIDDLE),
    )
    types = [e.type for e in result]
    assert types[0] == "travel"
    assert types[1] == "learn_from"
    assert types[2] == "travel"
    assert types[3] == "defeat_by_riddle"


def test_scene_3_learn_from_happens_at_delphi():
    """The Oracle is at Delphi; knowledge acquisition must happen
    there, not at any other location."""
    result = plan_to_goal(
        _sphinx_riddle_start_state(),
        _sphinx_riddle_goal(),
        (TRAVEL, LEARN_FROM, DEFEAT_BY_RIDDLE),
    )
    learn_event = next(e for e in result if e.type == "learn_from")
    assert learn_event.participants["LOCATION"] == "delphi"
    assert learn_event.participants["TEACHER"] == "oracle"


def test_scene_3_defeat_happens_at_thebes_gates():
    result = plan_to_goal(
        _sphinx_riddle_start_state(),
        _sphinx_riddle_goal(),
        (TRAVEL, LEARN_FROM, DEFEAT_BY_RIDDLE),
    )
    defeat_event = next(e for e in result if e.type == "defeat_by_riddle")
    assert defeat_event.participants["AGENT"] == "oedipus"
    assert defeat_event.participants["OPPONENT"] == "sphinx"


def test_scene_3_preconditions_satisfied_at_each_step():
    """Cumulative-state validity across the full 4-step plan,
    including the epistemic-precondition satisfaction at the
    defeat step."""
    result = plan_to_goal(
        _sphinx_riddle_start_state(),
        _sphinx_riddle_goal(),
        (TRAVEL, LEARN_FROM, DEFEAT_BY_RIDDLE),
    )
    state = set(_sphinx_riddle_start_state())
    for event in result:
        for p in event.preconditions:
            assert p in state, (
                f"precondition {p} of {event.type} "
                f"(τ_a={event.τ_a}) not in state"
            )
        for eff in event.effects:
            if eff.asserts:
                state.add(eff.prop)
            else:
                state.discard(eff.prop)


def test_scene_3_final_state_has_dead_sphinx_and_oedipus_knows():
    """Terminal invariant: Sphinx dead; Oedipus knows the riddle
    answer; Oedipus at thebes_gates."""
    result = plan_to_goal(
        _sphinx_riddle_start_state(),
        _sphinx_riddle_goal(),
        (TRAVEL, LEARN_FROM, DEFEAT_BY_RIDDLE),
    )
    state = set(_sphinx_riddle_start_state())
    for event in result:
        for eff in event.effects:
            if eff.asserts:
                state.add(eff.prop)
            else:
                state.discard(eff.prop)
    assert Prop("dead", ("sphinx",)) in state
    assert Prop("alive", ("sphinx",)) not in state
    assert Prop("knows", ("oedipus", "riddle_answer")) in state
    assert Prop("at", ("oedipus", "thebes_gates")) in state


def test_scene_3_defeat_by_riddle_schema_has_knows_first():
    """S3P14 pragmatic ordering pin: knows/2 precondition is the
    first entry in DEFEAT_BY_RIDDLE.preconditions. If this gets
    reordered, the planner loses the ability to plan this scene
    (until threat-resolution replaces sequential regression per
    S3P-OQ10)."""
    assert DEFEAT_BY_RIDDLE.preconditions[0].predicate == "knows"


def test_scene_3_infeasible_without_teacher_knowledge():
    """Remove the Oracle's knowledge; no other fact-typed term
    exists. Goal becomes infeasible because learn_from can't
    satisfy its knows(TEACHER, FACT) precondition anywhere."""
    start = frozenset(
        p for p in _sphinx_riddle_start_state()
        if not (p.predicate == "knows")
    )
    result = plan_to_goal(
        start,
        _sphinx_riddle_goal(),
        (TRAVEL, LEARN_FROM, DEFEAT_BY_RIDDLE),
    )
    assert isinstance(result, PlanningError)
    assert result.code == "no_plan_found"


def test_scene_3_visited_guard_firings_are_bounded():
    """S3P8 invariant carries into scene 3 — typed enumeration
    prevents unbounded cascades on the larger 5-operator state
    space. A regression where firings explode to thousands would
    signal enumeration blowup."""
    reset_visited_guard_counter()
    result = plan_to_goal(
        _sphinx_riddle_start_state(),
        _sphinx_riddle_goal(),
        (TRAVEL, LEARN_FROM, DEFEAT_BY_RIDDLE),
    )
    assert isinstance(result, tuple)  # sanity
    fires = visited_guard_fires()
    assert fires < 200, (
        f"scene-3 visited-guard fires {fires} times (expected < 200); "
        f"regression in enumeration or state-graph size"
    )


def test_scene_3_learn_from_alone_on_co_located_agents():
    """Minimal sanity for LEARN_FROM: student + teacher already
    co-located; teacher knows; one-step plan."""
    start = _type_assertions_scene_3() | frozenset({
        Prop("at", ("oedipus", "delphi")),
        Prop("at", ("oracle", "delphi")),
        Prop("knows", ("oracle", "riddle_answer")),
        Prop("alive", ("oedipus",)),
        Prop("alive", ("oracle",)),
    })
    goal = PlanningGoal(
        operator=LEARN_FROM,
        bindings={
            "STUDENT": "oedipus",
            "TEACHER": "oracle",
            "FACT": "riddle_answer",
            "LOCATION": "delphi",
        },
    )
    result = plan_to_goal(start, goal, (TRAVEL, LEARN_FROM))
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert result[0].type == "learn_from"


def test_scene_3_defeat_by_riddle_schema_valid():
    """Smoke — both new schemas construct without validation errors
    (sketch-02 S3P8 type-discipline check)."""
    assert LEARN_FROM.name == "learn_from"
    assert DEFEAT_BY_RIDDLE.name == "defeat_by_riddle"
    assert LEARN_FROM.variable_types["FACT"] == FACT_TYPE
    assert DEFEAT_BY_RIDDLE.variable_types["FACT"] == FACT_TYPE


# ----------------------------------------------------------------------------
# Test runner
# ----------------------------------------------------------------------------


TESTS = [
    # Worked example — primary success pin
    test_worked_example_returns_three_event_plan,
    test_worked_example_event_types_are_two_travels_plus_kills,
    test_worked_example_travel_participants_cover_both_agents,
    test_worked_example_travels_converge_on_single_location,
    test_worked_example_kill_participants_are_oedipus_and_laius,
    test_worked_example_cumulative_state_satisfies_preconditions_before_each_step,
    test_worked_example_final_state_has_dead_laius,
    # Substrate event emission
    test_emitted_events_are_substrate_event_records,
    test_emitted_events_are_provisional,
    test_emitted_events_are_on_canonical_branch,
    test_emitted_events_have_monotonic_tau_s,
    test_emitted_events_have_sequential_tau_a,
    test_emitted_events_carry_world_effects,
    # Infeasibility
    test_weapon_removed_produces_planning_error,
    test_planning_error_names_unsatisfied_preconditions,
    test_planning_error_offers_relaxations,
    test_empty_start_state_produces_empty_universe_error,
    test_planning_error_is_frozen,
    # Degenerate
    test_start_state_already_satisfies_goal_returns_one_step_plan,
    test_fully_bound_goal_without_type_assertions_still_plans,
    # Unification + binding
    test_goal_with_all_variables_bound_skips_enumeration,
    test_path_mismatch_prevents_plan,
    # OperatorSchema validation
    test_operator_schema_rejects_empty_name,
    test_operator_schema_rejects_lowercase_params,
    test_operator_schema_accepts_valid_shape,
    # Sketch-02 — typed variables
    test_operator_schema_rejects_missing_variable_type,
    test_operator_schema_rejects_empty_type_name,
    test_operator_schema_rejects_missing_free_var_type,
    test_scene_1_visited_guard_firings_are_bounded,
    test_start_state_without_type_assertions_produces_empty_universe,
    test_typed_enumeration_ignores_wrongly_typed_terms,
    # Sketch-02 — acquire operator
    test_acquire_operator_schema_valid,
    test_acquire_only_needs_co_location,
    test_acquire_item_not_at_location_infeasible,
    # Sketch-02 — Scene 2
    test_scene_2_returns_four_event_plan,
    test_scene_2_plan_includes_acquire,
    test_scene_2_plan_type_sequence,
    test_scene_2_preconditions_satisfied_at_each_step,
    test_scene_2_final_state_has_dead_laius_and_oedipus_has_sword,
    test_scene_2_acquire_comes_after_oedipus_travel,
    test_scene_2_visited_guard_firings_are_bounded,
    # Sketch-03 — Scene 3: Oedipus defeats the Sphinx
    test_scene_3_returns_four_event_plan,
    test_scene_3_plan_type_sequence,
    test_scene_3_learn_from_happens_at_delphi,
    test_scene_3_defeat_happens_at_thebes_gates,
    test_scene_3_preconditions_satisfied_at_each_step,
    test_scene_3_final_state_has_dead_sphinx_and_oedipus_knows,
    test_scene_3_defeat_by_riddle_schema_has_knows_first,
    test_scene_3_infeasible_without_teacher_knowledge,
    test_scene_3_visited_guard_firings_are_bounded,
    test_scene_3_learn_from_alone_on_co_located_agents,
    test_scene_3_defeat_by_riddle_schema_valid,
]


def main() -> int:
    passed = 0
    failed = 0
    for test in TESTS:
        try:
            test()
        except AssertionError as e:
            print(f"FAIL  {test.__name__}")
            print(f"      {e}")
            failed += 1
            continue
        except Exception:
            print(f"ERROR {test.__name__}")
            traceback.print_exc()
            failed += 1
            continue
        print(f"ok    {test.__name__}")
        passed += 1

    print()
    print(f"{passed} passed, {failed} failed, {len(TESTS)} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
