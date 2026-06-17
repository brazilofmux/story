"""
test_authoring.py — the human front-end compiler (story format → verified
substrate + overlay), offline.

Pins that a plain-text story doc compiles to the right objects, verifies
clean, honors the telling order, derives the Aristotelian marks, and
raises friendly errors on malformed input.
"""

from __future__ import annotations

import os
import sys
import traceback

from story_engine.core.authoring import (
    compile_story, load_story_file, verify_compiled, StoryFormatError,
    _parse_prop,
)
from story_engine.core.substrate import Prop


def _min_doc(**over):
    """A minimal valid story doc (dict, as tomllib would produce)."""
    doc = {
        "title": "Test",
        "logline": "a test",
        "telling": "chronological",
        "characters": [
            {"id": "hero", "name": "Hero", "role": "tragic-hero",
             "hamartia": "the flaw"},
            {"id": "victim", "name": "Victim", "role": "pathos-centre"},
        ],
        "events": [
            {"id": "open", "when": 0, "who": ["hero"], "summary": "it opens"},
            {"id": "turn", "when": 5, "who": ["hero", "victim"],
             "mark": "peripeteia", "summary": "the reversal"},
            {"id": "fall", "when": 6, "who": ["victim"], "summary": "death"},
            {"id": "see", "when": 9, "who": ["hero"], "mark": "anagnorisis",
             "recognizer": "hero", "summary": "he sees"},
        ],
        "anti_recognitions": [{"at": "fall", "who": "victim"}],
        "phases": {
            "beginning": ["open"],
            "middle": ["turn"],
            "end": ["fall", "see"],
        },
    }
    doc.update(over)
    return doc


def test_compiles_to_objects():
    s = compile_story(_min_doc())
    assert {e.id for e in s.entities} == {"hero", "victim"}
    assert len(s.fabula) == 4
    assert len(s.sjuzhet) == 4
    m = s.mythos
    assert m.plot_kind == "complex"
    assert m.peripeteia_event_id == "turn"
    assert m.anagnorisis_event_id == "see"
    assert m.anagnorisis_character_ref_id == "ar_hero"
    assert m.pathos_character_ref_ids == ("ar_victim",)


def test_compiled_story_verifies_clean():
    assert verify_compiled(compile_story(_min_doc())) == []


def test_roles_map_to_flags():
    s = compile_story(_min_doc())
    hero = next(c for c in s.mythos.characters if c.id == "ar_hero")
    victim = next(c for c in s.mythos.characters if c.id == "ar_victim")
    assert hero.is_tragic_hero and not hero.pathos_carrier
    assert victim.pathos_carrier and not victim.is_tragic_hero
    assert hero.hamartia_text == "the flaw"


def test_anti_recognition_compiled():
    s = compile_story(_min_doc())
    assert len(s.mythos.anagnorisis_chain) == 1
    step = s.mythos.anagnorisis_chain[0]
    assert step.anagnorisis_qualifier == "anti"
    assert step.character_ref_id == "ar_victim"
    assert step.event_id == "fall"


def test_chronological_vs_reverse_staging():
    chron = compile_story(_min_doc(telling="chronological"))
    assert [s.event_id for s in chron.sjuzhet] == ["open", "turn", "fall", "see"]
    rev = compile_story(_min_doc(telling="reverse"))
    assert [s.event_id for s in rev.sjuzhet] == ["see", "fall", "turn", "open"]


def test_explicit_staging():
    doc = _min_doc(telling="explicit", staging=["see", "open", "fall", "turn"])
    s = compile_story(doc)
    assert [e.event_id for e in s.sjuzhet] == ["see", "open", "fall", "turn"]


def test_binding_computed_from_distance():
    # peripeteia τ_s=5, anagnorisis τ_s=9 → distance 4 → separated.
    s = compile_story(_min_doc())
    assert s.mythos.peripeteia_anagnorisis_binding == "separated"


def test_parse_prop():
    assert _parse_prop("dead(maren)") == Prop("dead", ("maren",))
    assert _parse_prop("storm_active()") == Prop("storm_active", ())
    assert _parse_prop("killed(a, b)") == Prop("killed", ("a", "b"))


def _expect_error(doc, needle):
    try:
        compile_story(doc)
    except StoryFormatError as e:
        assert needle in str(e), f"got {e!r}, expected {needle!r}"
        return
    raise AssertionError(f"expected StoryFormatError containing {needle!r}")


def test_friendly_errors():
    _expect_error(_min_doc(phases={"beginning": ["open"], "middle": [],
                                   "end": ["see"]}),
                  "in no phase")                       # fall + turn unphased
    doc = _min_doc()
    doc["events"][0]["who"] = ["nobody"]
    _expect_error(doc, "not a declared")               # unknown participant
    _expect_error(_min_doc(telling="explicit"),
                  "requires a staging")                # explicit w/o staging
    doc2 = _min_doc()
    doc2["phases"]["middle"] = ["open"]                # open in 2 phases
    _expect_error(doc2, "two phases")


def test_loads_real_sample_file():
    path = os.path.join(os.path.dirname(__file__), "..", "stories",
                        "quarter.story.toml")
    if not os.path.exists(path):
        return
    s = load_story_file(path)
    assert s.title == "Quarter"
    assert verify_compiled(s) == []


TESTS = [
    test_compiles_to_objects,
    test_compiled_story_verifies_clean,
    test_roles_map_to_flags,
    test_anti_recognition_compiled,
    test_chronological_vs_reverse_staging,
    test_explicit_staging,
    test_binding_computed_from_distance,
    test_parse_prop,
    test_friendly_errors,
    test_loads_real_sample_file,
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
