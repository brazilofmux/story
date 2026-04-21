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
)


# ----------------------------------------------------------------------------
# Worked-example fixtures (Oedipus crossroads)
# ----------------------------------------------------------------------------


TRAVEL = OperatorSchema(
    name="travel",
    params=("AGENT", "FROM", "TO"),
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


def _crossroads_start_state() -> frozenset:
    return frozenset({
        Prop("at", ("oedipus", "corinth")),
        Prop("at", ("laius", "thebes")),
        Prop("has", ("oedipus", "sword")),
        Prop("path", ("corinth", "crossroads")),
        Prop("path", ("thebes", "crossroads")),
        Prop("alive", ("oedipus",)),
        Prop("alive", ("laius",)),
    })


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
    start = frozenset({
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
    start = frozenset({
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
    # Unification + binding
    test_goal_with_all_variables_bound_skips_enumeration,
    test_path_mismatch_prevents_plan,
    # OperatorSchema validation
    test_operator_schema_rejects_empty_name,
    test_operator_schema_rejects_lowercase_params,
    test_operator_schema_accepts_valid_shape,
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
