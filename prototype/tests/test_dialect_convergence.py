"""
test_dialect_convergence.py — convergence parity across dialects, offline.

The convergence controller (draft_convergence.converge) is dialect-agnostic
and tested generically in test_draft_convergence with fakes. This file proves
the missing half: that each dialect's REAL evaluator (compare_*) and REAL
repair planner (plan_repairs) COMPOSE into that loop — the integration the
Aristotelian path gets from demo_converge_malfi, here pinned offline for
Save-the-Cat, Dramatic, and Dramatica.

Pattern per dialect: build the authored structure + sjuzhet, scenes from the
sjuzhet, and a scripted evaluate_fn that returns the dialect's real fidelity
report for a DRIFTED reading then a FAITHFUL one. The dialect's real
plan_repairs (wrapped to the controller's 2-arg plan_fn) localizes the drift;
a marker repair_fn splices. We assert the loop reaches the fidelity ceiling and
repaired the right substrate event — i.e. the dialect is wired end to end.
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.draft_convergence import converge

# Save-the-Cat
from story_engine.core.save_the_cat_evaluator import (
    StcReading, StcBeatRead, compare_to_sheet,
)
from story_engine.core.save_the_cat_repair import plan_repairs as stc_plan
from story_engine.core.save_the_cat_generation import StcStorySheet
from story_engine.core.save_the_cat import CANONICAL_BEAT_BY_SLOT
from story_engine.encodings import macbeth_save_the_cat as STC
from story_engine.encodings.macbeth import SJUZHET as MACBETH_SJUZHET

# Dramatic
from story_engine.core.dramatic_evaluator import (
    DramaticReading, compare_to_story,
)
from story_engine.core.dramatic_repair import plan_repairs as dramatic_plan, _ending_event
from story_engine.core.dramatic_generation import DramaticStory
from story_engine.encodings import rocky_dramatic_three_actor as DRM
from story_engine.encodings.rocky import SJUZHET as ROCKY_SJUZHET

# Dramatica
from story_engine.core.dramatica_evaluator import (
    DramaticaReading, compare_to_storyform,
)
from story_engine.core.dramatica_repair import plan_repairs as dramatica_plan
from story_engine.core.dramatica_generation import DramaticaStoryform
from story_engine.encodings import rocky_dramatica_complete as RD


def _scenes_from(sjuzhet):
    return [{"tau_d": e.τ_d, "event_id": e.event_id, "prose": "placeholder"}
            for e in sjuzhet]


def _scripted(readings, compare, structure):
    """evaluate_fn: return the dialect's real report for the next scripted
    reading (last reading repeats once exhausted)."""
    box = {"i": 0}

    def ev(_text):
        r = readings[min(box["i"], len(readings) - 1)]
        box["i"] += 1
        return compare(r, structure)
    return ev


def _marker(d):
    return f"FIXED::{d.event_id}"


# ============================================================================
# Save-the-Cat
# ============================================================================

def _stc_sheet():
    return StcStorySheet(
        title="Macbeth", action_summary="x",
        beats=STC.BEATS, strands=STC.STRANDS, characters=STC.CHARACTERS,
        beat_event_ids=STC.BEAT_EVENT_IDS,
    )


def _stc_reading(drop=None):
    beats = [StcBeatRead(beat=CANONICAL_BEAT_BY_SLOT[s].name, what_happens="x")
             for s in range(1, 16) if CANONICAL_BEAT_BY_SLOT[s].name != drop]
    return StcReading(
        protagonist="Macbeth", beats_identified=beats,
        b_story="the Macbeth marriage", midpoint="false victory",
        all_is_lost="Lady Macbeth dies", final_mirrors_opening="yes",
        overall_read="x")


def test_save_the_cat_converges():
    sheet = _stc_sheet()
    scenes = _scenes_from(MACBETH_SJUZHET)
    # round 0: Catalyst (slot 4 → E_prophecy_first) missing; round 1: faithful
    ev = _scripted([_stc_reading(drop="Catalyst"), _stc_reading()],
                   compare_to_sheet, sheet)
    run = converge(
        scenes=scenes, mythos=sheet, evaluate_fn=ev, repair_fn=_marker,
        plan_fn=lambda rep, s: stc_plan(rep, s, MACBETH_SJUZHET),
        max_iters=4, target=1.0,
    )
    assert run.final_score == 1.0
    assert run.history[-1].stopped == "target reached"
    repaired = [e for rec in run.history for e in rec.repaired_events]
    assert "E_prophecy_first" in repaired


# ============================================================================
# Dramatic
# ============================================================================

def _dramatic_story():
    return DramaticStory(
        title="Rocky", action_summary="x",
        template_id=DRM.STORY.character_function_template_id,
        characters=DRM.CHARACTERS, arguments=(DRM.ARG_WORTH,),
        throughlines=DRM.THROUGHLINES, stakes=(DRM.STK_SELF_RESPECT,),
    )


def _dramatic_reading(resolution):
    return DramaticReading(
        hero="Rocky Balboa", obstacle="Apollo Creed", helper="Mickey",
        argument_claim="worth is earned by enduring, not winning",
        argument_resolution=resolution,
        stakes="proof he can go the full fifteen rounds",
        overall_read="x")


def test_dramatic_converges():
    story = _dramatic_story()
    scenes = _scenes_from(ROCKY_SJUZHET)
    # round 0: argument NEGATED (authored affirm) — drift sealed at the ending;
    # round 1: affirm — faithful.
    ev = _scripted([_dramatic_reading("negate"), _dramatic_reading("affirm")],
                   compare_to_story, story)
    run = converge(
        scenes=scenes, mythos=story, evaluate_fn=ev, repair_fn=_marker,
        plan_fn=lambda rep, s: dramatic_plan(rep, s, ROCKY_SJUZHET),
        max_iters=4, target=1.0,
    )
    assert run.final_score == 1.0
    assert run.history[-1].stopped == "target reached"
    repaired = [e for rec in run.history for e in rec.repaired_events]
    assert _ending_event(ROCKY_SJUZHET) in repaired


# ============================================================================
# Dramatica
# ============================================================================

def _dramatica_storyform():
    return DramaticaStoryform(
        title="Rocky", action_summary="x",
        domain_assignments=RD.DOMAIN_ASSIGNMENTS, signposts=RD.ALL_SIGNPOSTS,
        dynamics=RD.DYNAMIC_STORY_POINTS, story_goal=RD.STORY_GOAL,
        story_consequence=RD.STORY_CONSEQUENCE,
        canonical_ending=RD.CANONICAL_ENDING, act_event_ids=RD.ACT_EVENT_IDS,
    )


def _dramatica_reading(judgment):
    return DramaticaReading(
        story_goal="a clean publicity title defense for Apollo",
        outcome="failure", judgment=judgment,
        ending_shape="personal triumph" if judgment == "good" else "tragedy",
        main_character="Rocky", mc_resolve="steadfast",
        influence_character="Apollo", relationship="Rocky and Adrian",
        throughlines_present=["overall", "main character",
                              "influence character", "relationship"],
        overall_read="x")


def test_dramatica_converges():
    storyform = _dramatica_storyform()
    scenes = _scenes_from(ROCKY_SJUZHET)
    # round 0: judgment BAD (tragic collapse — authored Good); round 1: good.
    ev = _scripted([_dramatica_reading("bad"), _dramatica_reading("good")],
                   compare_to_storyform, storyform)
    run = converge(
        scenes=scenes, mythos=storyform, evaluate_fn=ev, repair_fn=_marker,
        plan_fn=lambda rep, s: dramatica_plan(rep, s, ROCKY_SJUZHET),
        max_iters=4, target=1.0,
    )
    assert run.final_score == 1.0
    assert run.history[-1].stopped == "target reached"
    # the Dramatica ending-shape drift localizes to a final-act beat
    assert any(rec.repaired_events for rec in run.history)


TESTS = [
    test_save_the_cat_converges,
    test_dramatic_converges,
    test_dramatica_converges,
]


def main() -> int:
    passed = failed = 0
    for fn in TESTS:
        try:
            fn()
        except Exception:
            failed += 1
            print(f"FAIL  {fn.__name__}")
            traceback.print_exc()
        else:
            passed += 1
            print(f"ok    {fn.__name__}")
    print(f"\n{passed} passed, {failed} failed, {passed + failed} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
