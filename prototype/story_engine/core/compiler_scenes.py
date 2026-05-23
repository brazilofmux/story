"""
compiler_scenes.py — operator schemas and scene definitions for the
stage-3 POCL planner spike.

Per compilation-stage-3-sketch-01 (primitive mechanism),
sketch-02 (typed variables + library growth + scene 2),
sketch-03 (epistemic preconditions + scene 3 with learn_from).

This module is the current home for the five OperatorSchema
instances and the three start-state / goal builders actually
exercised by test_compiler_stage_3.py. It fulfills the
"test-file fixtures" role left open by S3P9.

No public "stable surface" or convenience tuples are provided
yet; any such surface will be added only when a second concrete
client (stage-1 extraction, a new worked scene that needs them,
etc.) appears and a forcing function justifies the extraction.
"""

from __future__ import annotations

from story_engine.core.compiler_stage_3 import OperatorSchema, PlanningGoal
from story_engine.core.substrate import Prop


# ----------------------------------------------------------------------------
# Type constants (sketch-02 S3P8 + sketch-03 S3P11)
# ----------------------------------------------------------------------------

AGENT_TYPE = "agent"
LOCATION_TYPE = "location"
OBJECT_TYPE = "object"
FACT_TYPE = "fact"          # sketch-03 S3P11


# ----------------------------------------------------------------------------
# Operator library (migrated to sketch-02/03 typed form)
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
# State builders (private helpers composed into public scene accessors)
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


# ----------------------------------------------------------------------------
# Goal builders
# ----------------------------------------------------------------------------


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


