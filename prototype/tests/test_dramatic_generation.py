"""
test_dramatic_generation.py — the FOURTH dialect (the general Dramatic
dialect, minimal three-actor template) through the generator.

Offline. Proves the DramaticFrame surfaces the LEAN parent-dialect
vocabulary — the thematic argument, the character functions, the stakes,
the throughlines — as bible sections, and per-scene the FUNCTIONS
present (Hero+Obstacle = confrontation; Hero+Helper = aid), and that the
generator routes this fourth adapter with NONE of the other three
dialects' vocabulary. Also pins the minimal encoding's expected advisory
verifier notes.
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.draft_generator import generate_draft, DialectFrame
from story_engine.core.dramatic_generation import DramaticStory, DramaticFrame
from story_engine.core.dramatic import verify
from story_engine.encodings import rocky_dramatic_three_actor as D
from story_engine.encodings.rocky import FABULA, SJUZHET, ENTITIES, DESCRIPTIONS


def _story():
    return DramaticStory(
        title="Rocky", action_summary="a club fighter goes the distance",
        template_id=D.STORY.character_function_template_id,
        characters=D.CHARACTERS, arguments=(D.ARG_WORTH,),
        throughlines=D.THROUGHLINES, stakes=(D.STK_SELF_RESPECT,),
    )


def test_minimal_encoding_verifies_with_expected_advisories():
    obs = verify(D.STORY, arguments=(D.ARG_WORTH,), throughlines=D.THROUGHLINES,
                 characters=D.CHARACTERS, stakes=(D.STK_SELF_RESPECT,))
    # all advisory 'noted', none an error; expected for the minimal form
    assert all(getattr(o, "severity", "") == "noted" for o in obs)
    assert D.STORY.character_function_template_id == "three-actor"


def test_bible_surfaces_argument_functions_stakes_not_other_dialects():
    bible = "\n".join(DramaticFrame(_story(), FABULA).bible_sections(name_map={}))
    assert "three-actor" in bible
    assert "argument" in bible.lower() and "AFFIRMS this claim" in bible
    assert "Hero: Rocky Balboa" in bible
    assert "Obstacle: Apollo Creed" in bible
    assert "Helper: Mickey Goldmill, Adrian Pennino" in bible
    assert "Stakes" in bible and "AT RISK" in bible
    # not any of the other three dialects
    assert "PERIPETEIA" not in bible
    assert "Dramatica storyform" not in bible
    assert "signpost" not in bible.lower()
    assert "Save-the-Cat" not in bible


def test_scene_marks_show_function_presence_and_confrontation():
    frame = DramaticFrame(_story(), FABULA)
    by_id = {s.event_id: s for s in SJUZHET}

    def lines(eid):
        return "\n".join(frame.scene_lines(entry=by_id[eid], name_map={}))
    # Apollo picks Rocky — Hero and Obstacle share the beat → confrontation
    conf = lines("E_apollo_selects_rocky")
    assert "Obstacle (Apollo" in conf and "Hero (Rocky" in conf
    assert "CONFRONTATION" in conf
    # training with Mickey — Helper with the Hero → aid
    aid = lines("E_training_begins")
    assert "Helper (Mickey" in aid
    assert "Helper is with the Hero" in aid


def test_generator_routes_the_fourth_adapter_dry_run():
    frame = DramaticFrame(_story(), FABULA)
    result = generate_draft(
        title="Rocky", sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
        descriptions=DESCRIPTIONS, adapter=frame, dry_run=True,
    )
    assert "Dramatic structure" in result.story_bible
    assert "PERIPETEIA" not in result.story_bible
    # the confrontation/aid beats carry function marks
    briefs = "\n".join(s.brief for s in result.scenes)
    assert "Functions present in this beat" in briefs
    assert issubclass(DramaticFrame, DialectFrame)
    assert len(result.scenes) == len(SJUZHET)


def test_aristotelian_path_unaffected():
    from story_engine.encodings.vantage_light import (
        FABULA as VF, SJUZHET as VS, ENTITIES as VE)
    from story_engine.encodings.vantage_light_aristotelian import (
        AR_VANTAGE_MYTHOS)
    result = generate_draft(
        title="Vantage", sjuzhet=VS, fabula=VF, entities=VE,
        mythos=AR_VANTAGE_MYTHOS, dry_run=True)
    assert "PERIPETEIA" in result.story_bible
    assert "Dramatic structure" not in result.story_bible


TESTS = [
    test_minimal_encoding_verifies_with_expected_advisories,
    test_bible_surfaces_argument_functions_stakes_not_other_dialects,
    test_scene_marks_show_function_presence_and_confrontation,
    test_generator_routes_the_fourth_adapter_dry_run,
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
