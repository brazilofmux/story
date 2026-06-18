"""
test_dramatic_repair.py — general-Dramatic repair planning, offline.

plan_repairs is pure Python: a DramaticFidelityReport plus the authored
story and sjuzhet in, RepairDirectives out. Only the argument resolution
(sealed at the ending) localizes; the diffuse function / claim / stakes
drifts are reported, not forced onto a scene.

Pins dramatic_repair parity with the peer repairers.
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.dramatic_evaluator import (
    DramaticFidelityReport, DramaticFidelityFinding,
)
from story_engine.core.dramatic_repair import plan_repairs, _ending_event
from story_engine.core.dramatic_generation import DramaticStory
from story_engine.encodings import rocky_dramatic_three_actor as D
from story_engine.encodings.rocky import SJUZHET


def _story() -> DramaticStory:
    return DramaticStory(
        title="Rocky", action_summary="x",
        template_id=D.STORY.character_function_template_id,
        characters=D.CHARACTERS, arguments=(D.ARG_WORTH,),
        throughlines=D.THROUGHLINES, stakes=(D.STK_SELF_RESPECT,),
    )


def _finding(dim, verdict, authored="x"):
    return DramaticFidelityFinding(dimension=dim, authored=authored,
                                   decompiled="(none)", verdict=verdict)


def test_argument_drift_localizes_to_the_ending_beat():
    report = DramaticFidelityReport(title="Rocky", findings=[
        _finding("argument_resolution", "drifted", "affirm"),
    ])
    directives = plan_repairs(report, _story(), SJUZHET)
    assert len(directives) == 1
    d = directives[0]
    assert d.event_id == _ending_event(SJUZHET)        # the final staged beat
    assert d.dimension == "argument_resolution"
    # the directive rebuilds the authored AFFIRM resolution
    assert "AFFIRM" in d.instruction
    assert "enduring" in d.instruction.lower() or "worth" in d.instruction.lower()


def test_diffuse_dimensions_are_not_localized():
    report = DramaticFidelityReport(title="Rocky", findings=[
        _finding("hero", "lost"),
        _finding("obstacle", "lost"),
        _finding("helper", "lost"),
        _finding("argument_claim", "drifted"),
        _finding("stakes", "lost"),
    ])
    assert plan_repairs(report, _story(), SJUZHET) == []


def test_preserved_argument_produces_no_directive():
    report = DramaticFidelityReport(title="Rocky", findings=[
        _finding("argument_resolution", "preserved", "affirm"),
    ])
    assert plan_repairs(report, _story(), SJUZHET) == []


def test_no_sjuzhet_no_directive():
    report = DramaticFidelityReport(title="Rocky", findings=[
        _finding("argument_resolution", "drifted", "affirm"),
    ])
    assert plan_repairs(report, _story(), ()) == []


TESTS = [
    test_argument_drift_localizes_to_the_ending_beat,
    test_diffuse_dimensions_are_not_localized,
    test_preserved_argument_produces_no_directive,
    test_no_sjuzhet_no_directive,
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
