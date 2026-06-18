"""
test_save_the_cat_repair.py — Save-the-Cat repair planning, offline.

plan_repairs is pure Python: an StcFidelityReport plus the authored sheet and
sjuzhet in, RepairDirectives out. A lost beat localizes to the substrate
event authored to carry it (sheet.beat_event_ids); diffuse dimensions
(beat_order, protagonist, b_story) and unmapped beats are NOT localized.

Pins save_the_cat_repair parity with draft_repair / dramatica_repair.
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.save_the_cat_evaluator import (
    StcFidelityReport, StcFidelityFinding,
)
from story_engine.core.save_the_cat_repair import plan_repairs
from story_engine.core.save_the_cat_generation import StcStorySheet
from story_engine.encodings import macbeth_save_the_cat as S
from story_engine.encodings.macbeth import SJUZHET


def _sheet() -> StcStorySheet:
    return StcStorySheet(
        title="Macbeth", action_summary="x",
        beats=S.BEATS, strands=S.STRANDS, characters=S.CHARACTERS,
        beat_event_ids=S.BEAT_EVENT_IDS,
    )


def _finding(dim, verdict, authored="x"):
    return StcFidelityFinding(dimension=dim, authored=authored,
                              decompiled="(none)", verdict=verdict)


def test_lost_beat_localizes_to_its_authored_event():
    """Catalyst (slot 4) is authored to E_prophecy_first — a lost Catalyst
    must produce a directive targeting exactly that event, naming the beat."""
    report = StcFidelityReport(title="Macbeth", findings=[
        _finding("beat[04]", "lost", "Catalyst"),
    ])
    directives = plan_repairs(report, _sheet(), SJUZHET)
    assert len(directives) == 1
    d = directives[0]
    assert d.event_id == "E_prophecy_first"
    assert d.authored == "Catalyst"
    assert "Catalyst" in d.instruction


def test_unmapped_beat_is_not_localized():
    """Opening Image (slot 1) has no beat_event_ids entry — a lost Opening
    Image cannot be localized and produces no directive."""
    report = StcFidelityReport(title="Macbeth", findings=[
        _finding("beat[01]", "lost", "Opening Image"),
    ])
    assert plan_repairs(report, _sheet(), SJUZHET) == []


def test_diffuse_dimensions_are_not_localized():
    report = StcFidelityReport(title="Macbeth", findings=[
        _finding("beat_order", "drifted"),
        _finding("protagonist", "lost"),
        _finding("b_story", "lost"),
    ])
    assert plan_repairs(report, _sheet(), SJUZHET) == []


def test_preserved_beats_produce_no_directives():
    report = StcFidelityReport(title="Macbeth", findings=[
        _finding("beat[04]", "preserved", "Catalyst"),
        _finding("beat[09]", "preserved", "Midpoint"),
    ])
    assert plan_repairs(report, _sheet(), SJUZHET) == []


def test_multiple_lost_beats_one_directive_each_deduped():
    report = StcFidelityReport(title="Macbeth", findings=[
        _finding("beat[04]", "lost", "Catalyst"),    # E_prophecy_first
        _finding("beat[09]", "lost", "Midpoint"),    # E_macbeth_crowned
        _finding("beat[04]", "lost", "Catalyst"),    # duplicate slot/event
    ])
    directives = plan_repairs(report, _sheet(), SJUZHET)
    events = sorted(d.event_id for d in directives)
    assert events == ["E_macbeth_crowned", "E_prophecy_first"]


TESTS = [
    test_lost_beat_localizes_to_its_authored_event,
    test_unmapped_beat_is_not_localized,
    test_diffuse_dimensions_are_not_localized,
    test_preserved_beats_produce_no_directives,
    test_multiple_lost_beats_one_directive_each_deduped,
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
