"""
test_save_the_cat_generation.py — the THIRD dialect through the generator.

Offline. Proves the StcFrame surfaces a Save-the-Cat beat sheet as bible
sections + per-scene beat marks, that the authored beat→event mapping
covers every staged scene (no positional guessing), and that the
generator routes this third adapter exactly like the others — with
Save-the-Cat vocabulary in the bible and NONE of the Aristotelian or
Dramatica vocabularies. Widening the seam from two dialects to three.
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.draft_generator import generate_draft, DialectFrame
from story_engine.core.save_the_cat_generation import StcStorySheet, StcFrame
from story_engine.encodings import macbeth_save_the_cat as S
from story_engine.encodings.macbeth import FABULA, SJUZHET, ENTITIES, DESCRIPTIONS


def _sheet(authored=True):
    return StcStorySheet(
        title="Macbeth", action_summary="a thane murders his king for a crown",
        beats=S.BEATS, strands=S.STRANDS, characters=S.CHARACTERS,
        beat_event_ids=(S.BEAT_EVENT_IDS if authored else {}),
    )


def test_authored_beats_cover_every_scene_once():
    frame = StcFrame(_sheet(authored=True), SJUZHET)
    assert frame._beats_authored is True
    staged = {s.event_id for s in SJUZHET}
    assert staged <= set(frame._beat_of)
    assert frame._unplaced == []


def test_bible_surfaces_beat_sheet_not_other_dialects():
    bible = "\n".join(StcFrame(_sheet(), SJUZHET).bible_sections(name_map={}))
    assert "Save-the-Cat beat sheet" in bible
    for beat in ("Opening Image", "Catalyst", "Midpoint", "All Is Lost",
                 "Finale", "Final Image"):
        assert beat in bible
    assert "Strands" in bible and "a-story" in bible
    # not the other dialects
    assert "PERIPETEIA" not in bible
    assert "pathos-centre" not in bible.lower()
    assert "Dramatica storyform" not in bible
    assert "throughline" not in bible.lower()


def test_scene_marks_identify_the_right_beat():
    frame = StcFrame(_sheet(), SJUZHET)
    by_id = {s.event_id: s for s in SJUZHET}

    def beat_of(eid):
        return "\n".join(frame.scene_lines(entry=by_id[eid], name_map={}))
    assert "Catalyst" in beat_of("E_prophecy_first")
    assert "Fun and Games" in beat_of("E_duncan_killed")
    assert "Midpoint" in beat_of("E_macbeth_crowned")
    assert "All Is Lost" in beat_of("E_lady_macbeth_dies")
    assert "Finale" in beat_of("E_macbeth_killed")
    assert "Final Image" in beat_of("E_malcolm_crowned")


def test_generator_routes_the_third_adapter_dry_run():
    frame = StcFrame(_sheet(), SJUZHET)
    result = generate_draft(
        title="Macbeth", sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
        descriptions=DESCRIPTIONS, adapter=frame, dry_run=True,
    )
    assert "Save-the-Cat beat sheet" in result.story_bible
    assert "PERIPETEIA" not in result.story_bible
    # every staged scene got a beat mark
    assert all("BEAT" in s.brief for s in result.scenes)
    assert len(result.scenes) == len(SJUZHET)
    assert issubclass(StcFrame, DialectFrame)


def test_bible_honest_about_beat_source():
    authored = "\n".join(
        StcFrame(_sheet(authored=True), SJUZHET).bible_sections(name_map={}))
    inferred = "\n".join(
        StcFrame(_sheet(authored=False), SJUZHET).bible_sections(name_map={}))
    assert "AUTHORED" in authored and "APPROXIMATE" not in authored
    assert "APPROXIMATE" in inferred


def test_aristotelian_path_unaffected():
    """Adding a third dialect did not disturb the default tragic-arc path."""
    from story_engine.encodings.vantage_light import (
        FABULA as VF, SJUZHET as VS, ENTITIES as VE)
    from story_engine.encodings.vantage_light_aristotelian import (
        AR_VANTAGE_MYTHOS)
    result = generate_draft(
        title="Vantage", sjuzhet=VS, fabula=VF, entities=VE,
        mythos=AR_VANTAGE_MYTHOS, dry_run=True)
    assert "PERIPETEIA" in result.story_bible
    assert "Save-the-Cat" not in result.story_bible


TESTS = [
    test_authored_beats_cover_every_scene_once,
    test_bible_surfaces_beat_sheet_not_other_dialects,
    test_scene_marks_identify_the_right_beat,
    test_generator_routes_the_third_adapter_dry_run,
    test_bible_honest_about_beat_source,
    test_aristotelian_path_unaffected,
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
