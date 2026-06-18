"""
test_dramatica_generation.py — the Dramatica dialect adapter + the seam.

Offline. Proves (a) the DramaticaFrame surfaces a storyform as bible
sections + per-scene act marks, and (b) the generator routes a non-
default adapter through `generate_draft(adapter=...)` in dry-run — i.e.
the dialect seam works end to end, with Dramatica vocabulary in the
bible and NONE of the Aristotelian (no peripeteia/pathos).
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.draft_generator import generate_draft, DialectFrame
from story_engine.core.dramatica_generation import (
    DramaticaStoryform, DramaticaFrame, _perspective_of,
)
from story_engine.encodings.rocky import FABULA, SJUZHET, ENTITIES, DESCRIPTIONS
from story_engine.encodings import rocky_dramatica_complete as RD


def _sf(authored_acts=True):
    return DramaticaStoryform(
        title="Rocky", action_summary="a club fighter goes the distance",
        domain_assignments=RD.DOMAIN_ASSIGNMENTS, signposts=RD.ALL_SIGNPOSTS,
        dynamics=RD.DYNAMIC_STORY_POINTS, story_goal=RD.STORY_GOAL,
        story_consequence=RD.STORY_CONSEQUENCE,
        canonical_ending=RD.CANONICAL_ENDING,
        act_event_ids=(RD.ACT_EVENT_IDS if authored_acts else {}),
    )


def test_perspective_detection():
    assert _perspective_of("T_overall_fight") == "overall"
    assert _perspective_of("T_mc_rocky") == "mc"
    assert _perspective_of("T_ic_apollo") == "ic"
    assert _perspective_of("T_rel_rocky_adrian") == "rel"


def test_bible_surfaces_storyform_not_tragedy():
    frame = DramaticaFrame(_sf(), SJUZHET)
    bible = "\n".join(frame.bible_sections(name_map={}))
    # Dramatica vocabulary present
    assert "personal-triumph" in bible
    assert "Outcome = FAILURE" in bible and "Judgment = GOOD" in bible
    assert "four throughlines" in bible
    assert "Main Character" in bible and "Influence Character" in bible
    assert "STEADFAST" in bible and "TIMELOCK" in bible
    assert "Signpost progression" in bible
    # NOT Aristotelian
    assert "PERIPETEIA" not in bible
    assert "pathos-centre" not in bible.lower()


def test_scene_marks_map_to_acts():
    frame = DramaticaFrame(_sf(), SJUZHET)
    ordered = sorted(SJUZHET, key=lambda s: s.τ_d)
    first = frame.scene_lines(entry=ordered[0], name_map={})
    last = frame.scene_lines(entry=ordered[-1], name_map={})
    assert "act: 1 of 4" in first[0]
    assert "act: 4 of 4" in last[0]
    # the per-throughline signpost concerns are named
    assert any("Main Character=" in s for s in first)


def test_acts_cover_one_to_four():
    frame = DramaticaFrame(_sf(), SJUZHET)
    acts = set()
    for e in SJUZHET:
        lines = frame.scene_lines(entry=e, name_map={})
        for tok in ("1 of 4", "2 of 4", "3 of 4", "4 of 4"):
            if any(tok in ln for ln in lines):
                acts.add(tok)
    assert acts == {"1 of 4", "2 of 4", "3 of 4", "4 of 4"}


def test_generator_routes_the_adapter_dry_run():
    """The seam: generate_draft(adapter=DramaticaFrame) produces a bible
    with Dramatica sections and Dramatica scene marks — no Aristotelian
    vocabulary — without any change to the generator."""
    frame = DramaticaFrame(_sf(), SJUZHET)
    result = generate_draft(
        title="Rocky", sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
        descriptions=DESCRIPTIONS, adapter=frame, dry_run=True,
    )
    assert "Dramatica storyform" in result.story_bible
    assert "PERIPETEIA" not in result.story_bible
    # every scene got Dramatica act marks
    assert all("Dramatica act:" in s.brief for s in result.scenes)
    assert len(result.scenes) == len(SJUZHET)


def test_authored_acts_beat_the_positional_heuristic():
    """The #1 integrity fix: when act boundaries are AUTHORED, boundary
    beats land in their true act — the bell opens act 4, Green's injury
    opens act 2 — where the positional quartile split misplaces them."""
    authored = DramaticaFrame(_sf(authored_acts=True), SJUZHET)
    heuristic = DramaticaFrame(_sf(authored_acts=False), SJUZHET)
    assert authored._acts_authored is True
    assert heuristic._acts_authored is False
    # the bell is the start of the climax — act 4, not act 3
    assert authored._act_of["E_fight_bell"] == 4
    assert heuristic._act_of["E_fight_bell"] == 3      # the heuristic's error
    # Green's injury opens the changing-situation act — act 2, not act 1
    assert authored._act_of["E_mac_injured"] == 2
    assert heuristic._act_of["E_mac_injured"] == 1     # the heuristic's error


def test_authored_acts_cover_every_staged_event_once():
    """No cheating: the authored act map must place every staged event,
    with nothing left to the positional fallback."""
    frame = DramaticaFrame(_sf(authored_acts=True), SJUZHET)
    staged = {s.event_id for s in SJUZHET}
    assert staged <= set(frame._act_of)
    assert frame._unplaced == []


def test_bible_is_honest_about_act_source():
    """Authored → the bible says so; inferred → the bible flags the acts
    as APPROXIMATE rather than passing a guess off as fact."""
    authored = "\n".join(
        DramaticaFrame(_sf(authored_acts=True), SJUZHET).bible_sections(
            name_map={}))
    inferred = "\n".join(
        DramaticaFrame(_sf(authored_acts=False), SJUZHET).bible_sections(
            name_map={}))
    assert "AUTHORED" in authored and "APPROXIMATE" not in authored
    assert "APPROXIMATE" in inferred


def test_base_frame_is_abstract_no_dialect_privileged():
    """Asymmetry #1 fix: the base DialectFrame holds NO dialect logic —
    both dialects are explicit peer frames, neither is the default."""
    base = DialectFrame(None)
    for call in (lambda: base.bible_sections(name_map={}),
                 lambda: base.scene_lines(entry=None, name_map={})):
        try:
            call()
        except NotImplementedError:
            pass
        else:
            raise AssertionError("base DialectFrame should be abstract")
    # the Aristotelian frame is a peer in its own module, not the base
    from story_engine.core.aristotelian_generation import AristotelianFrame
    assert issubclass(AristotelianFrame, DialectFrame)
    assert issubclass(DramaticaFrame, DialectFrame)


def test_default_frame_still_aristotelian():
    """Regression: the default frame (mythos=) still reads a tragic arc —
    the seam did not break the Aristotelian path."""
    from story_engine.encodings.vantage_light import (
        FABULA as VF, SJUZHET as VS, ENTITIES as VE,
    )
    from story_engine.encodings.vantage_light_aristotelian import (
        AR_VANTAGE_MYTHOS,
    )
    result = generate_draft(
        title="Vantage", sjuzhet=VS, fabula=VF, entities=VE,
        mythos=AR_VANTAGE_MYTHOS, dry_run=True,
    )
    assert "PERIPETEIA" in result.story_bible
    assert "Dramatica storyform" not in result.story_bible


TESTS = [
    test_perspective_detection,
    test_bible_surfaces_storyform_not_tragedy,
    test_scene_marks_map_to_acts,
    test_acts_cover_one_to_four,
    test_generator_routes_the_adapter_dry_run,
    test_authored_acts_beat_the_positional_heuristic,
    test_authored_acts_cover_every_staged_event_once,
    test_bible_is_honest_about_act_source,
    test_base_frame_is_abstract_no_dialect_privileged,
    test_default_frame_still_aristotelian,
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
