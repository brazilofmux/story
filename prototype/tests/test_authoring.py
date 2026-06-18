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


# ---- Save-the-Cat overlay compile (the second wired dialect) --------------

def _stc_doc(**over):
    """A minimal Save-the-Cat doc: theme, genre, a protagonist, and events on
    the load-bearing beats (Catalyst → Finale)."""
    beats = ["Catalyst", "Break Into Two", "Midpoint", "All Is Lost",
             "Break Into Three", "Finale"]
    doc = {
        "title": "The Heist",
        "logline": "a crew's loyalty is tested by greed",
        "telling": "chronological",
        "theme_statement": "loyalty outlasts greed",
        "genre": "golden-fleece",
        "characters": [
            {"id": "nick", "name": "Nick", "role": "protagonist"},
            {"id": "sal", "name": "Sal", "role": "antagonist"},
        ],
        "events": [
            {"id": f"e{i}", "when": i + 1,
             "who": ["nick"] if i % 2 else ["nick", "sal"],
             "summary": f"the {b} beat", "beat": b}
            for i, b in enumerate(beats)
        ],
        "phases": {"beginning": ["e0", "e1"], "middle": ["e2", "e3"],
                   "end": ["e4", "e5"]},
    }
    doc.update(over)
    return doc


def test_stc_compiles_substrate_and_overlay():
    s = compile_story(_stc_doc(), "save-the-cat")
    assert s.dialect == "save-the-cat"
    assert {e.id for e in s.entities} == {"nick", "sal"}   # shared substrate
    assert len(s.fabula) == 6 and len(s.sjuzhet) == 6
    ov = s.overlay
    assert ov.story.title == "The Heist"
    assert ov.story.theme_statement == "loyalty outlasts greed"
    assert ov.story.stc_genre_id == "golden-fleece"
    assert len(ov.beats) == 6
    # beats group onto the canonical slots (Catalyst=4 … Finale=14)
    assert {b.slot for b in ov.beats} == {4, 6, 9, 11, 13, 14}
    assert ov.beat_event_ids[4] == ("e0",)
    assert {st.kind.value for st in ov.strands} == {"a-story", "b-story"}
    nick = next(c for c in ov.characters if c.id == "nick")
    assert nick.role_labels == ("protagonist",)


def test_stc_verifies_without_rejecting():
    # the STC verifier never rejects — all findings are advisory (noted /
    # advises-review), never blocking. A complete doc still surfaces only those.
    obs = verify_compiled(compile_story(_stc_doc(), "save-the-cat"))
    assert all(o.severity in ("noted", "advises-review") for o in obs)


def test_stc_tolerates_unbeated_events():
    doc = _stc_doc()
    for ev in doc["events"]:
        ev.pop("beat", None)                 # author declined the beat homework
    s = compile_story(doc, "save-the-cat")   # still compiles
    assert s.overlay.beats == () and s.overlay.beat_event_ids == {}
    assert verify_compiled(s) is not None    # verifier runs, doesn't raise


# ---- Dramatic overlay compile (the third wired dialect) -------------------

def _dramatic_doc(**over):
    """A minimal Dramatic doc: an argument with a resolution, the four
    throughlines (owners drive the Hero/Obstacle function labels), stakes."""
    doc = {
        "title": "The Verdict",
        "logline": "a judge weighs mercy against the law",
        "telling": "chronological",
        "characters": [
            {"id": "dana", "name": "Dana", "role": "protagonist"},
            {"id": "cole", "name": "Cole", "role": "antagonist"},
            {"id": "rae", "name": "Rae", "role": "clerk"},
        ],
        "events": [
            {"id": "charge", "when": 1, "who": ["dana", "cole"],
             "summary": "the charge is read"},
            {"id": "trial", "when": 2, "who": ["dana", "cole", "rae"],
             "summary": "the trial unfolds"},
            {"id": "verdict", "when": 3, "who": ["dana"],
             "summary": "the verdict lands"},
        ],
        "arguments": [{"premise": "the law can be just",
                       "resolution": "complicate"}],
        "throughlines": [
            {"role": "overall-story", "owner": "situation",
             "stakes": {"at_risk": "the town's trust", "to_gain": "justice"}},
            {"role": "main-character", "owner": "dana",
             "stakes": {"at_risk": "her career", "to_gain": "her conscience"}},
            {"role": "impact-character", "owner": "cole",
             "stakes": {"at_risk": "his freedom", "to_gain": "acquittal"}},
            {"role": "relationship", "owner": "relationship", "stakes": {}},
        ],
        "phases": {"beginning": ["charge"], "middle": ["trial"],
                   "end": ["verdict"]},
    }
    doc.update(over)
    return doc


def test_dramatic_compiles_substrate_and_overlay():
    s = compile_story(_dramatic_doc(), "dramatic")
    assert s.dialect == "dramatic"
    assert {e.id for e in s.entities} == {"dana", "cole", "rae"}
    assert len(s.fabula) == 3 and len(s.sjuzhet) == 3
    ov = s.overlay
    assert ov.template_id == "three-actor"
    # ownership drives the function labels the generator renders from
    funcs = {c.id: c.function_labels for c in ov.characters}
    assert funcs["dana"] == ("Hero",)        # owns main-character throughline
    assert funcs["cole"] == ("Obstacle",)    # owns impact-character throughline
    assert funcs["rae"] == ("Helper",)
    assert ov.arguments[0].resolution_direction.value == "complicate"
    roles = {t.role_label: t.owners for t in ov.throughlines}
    assert roles["main-character"] == ("dana",)
    assert roles["overall-story"] == ("the-situation",)
    assert roles["relationship"] == ("the-relationship",)
    # three throughlines carry stakes; the relationship one (empty) does not
    assert len(ov.stakes) == 3


def test_dramatic_verifies_without_rejecting():
    obs = verify_compiled(compile_story(_dramatic_doc(), "dramatic"))
    assert all(o.severity in ("noted", "advises-review") for o in obs)


def test_dramatic_tolerates_sparse_overlay():
    doc = _dramatic_doc()
    doc.pop("arguments")                     # author declined the argument
    doc.pop("throughlines")                  # … and the throughlines
    s = compile_story(doc, "dramatic")       # still compiles
    assert s.overlay.arguments == () and s.overlay.throughlines == ()
    # with no throughline owners, function labels fall back to the role field
    funcs = {c.id: c.function_labels for c in s.overlay.characters}
    assert funcs["dana"] == ("Hero",)        # role "protagonist" → Hero
    assert funcs["cole"] == ("Obstacle",)    # role "antagonist" → Obstacle
    assert verify_compiled(s) is not None


# ---- Dramatica overlay compile (the fourth wired dialect — full grid) -----

def _dramatica_doc(**over):
    """A minimal Dramatica doc: four throughlines in four distinct domains,
    the eight dynamics, a goal and a consequence."""
    doc = {
        "title": "The Climb",
        "logline": "a closed man learns to trust the rope",
        "telling": "chronological",
        "story_goal": "reach the summit before the storm",
        "story_consequence": "the expedition is lost on the mountain",
        "characters": [{"id": "ava", "name": "Ava"},
                       {"id": "rao", "name": "Rao"}],
        "events": [
            {"id": "base", "when": 1, "who": ["ava"], "summary": "they set out"},
            {"id": "ridge", "when": 2, "who": ["ava", "rao"],
             "summary": "the ridge nearly kills them"},
            {"id": "summit", "when": 3, "who": ["ava"], "summary": "the choice"},
        ],
        "throughlines": [
            {"role": "overall-story", "domain": "activity"},
            {"role": "main-character", "domain": "fixed-attitude", "owner": "ava"},
            {"role": "impact-character", "domain": "manipulation", "owner": "rao"},
            {"role": "relationship", "domain": "situation"},
        ],
        "dynamics": {"resolve": "change", "growth": "start", "approach": "do-er",
                     "problem_solving_style": "linear", "driver": "action",
                     "limit": "timelock", "outcome": "success",
                     "judgment": "good"},
        "phases": {"beginning": ["base"], "middle": ["ridge"], "end": ["summit"]},
    }
    doc.update(over)
    return doc


def test_dramatica_compiles_full_storyform():
    s = compile_story(_dramatica_doc(), "dramatica")
    assert s.dialect == "dramatica"
    assert {e.id for e in s.entities} == {"ava", "rao"}
    ov = s.overlay
    assert len(ov.throughlines) == 4
    # four distinct domains, all four covered
    assert {d.domain.value for d in ov.domain_assignments} == {
        "activity", "situation", "manipulation", "fixed-attitude"}
    assert len(ov.dynamics) == 8
    # 16 signposts: 4 per throughline, from the domain's Concern quad
    assert len(ov.signposts) == 16
    mc = sorted((sp.signpost_position, sp.signpost_element)
                for sp in ov.signposts if sp.throughline_id == "T_main_character")
    assert mc[0] == (1, "innermost-desires") and mc[3] == (4, "memories")
    assert ov.story_goal and ov.story_consequence


def test_dramatica_complete_storyform_verifies_clean():
    # all four structural pillars present → the verifier passes with no notes
    assert verify_compiled(compile_story(_dramatica_doc(), "dramatica")) == []


def test_dramatica_dual_dynamic_honored():
    doc = _dramatica_doc()
    doc["dynamics"]["problem_solving_style"] = ["linear", "holistic"]
    ov = compile_story(doc, "dramatica").overlay
    pss = next(x for x in ov.dynamics if x.axis.value == "problem-solving-style")
    assert pss.is_dual and pss.poles == frozenset({"linear", "holistic"})


def test_dramatica_drops_invalid_pole_not_raises():
    doc = _dramatica_doc()
    doc["dynamics"]["resolve"] = "transform"   # not change|steadfast
    ov = compile_story(doc, "dramatica").overlay   # must not raise
    axes = {x.axis.value for x in ov.dynamics}
    assert "resolve" not in axes and len(ov.dynamics) == 7


# ---- knowledge discipline: authored `learns` → KnowledgeEffects -----------

def test_learns_compile_to_knowledge_effects():
    from story_engine.core.substrate import KnowledgeEffect, Slot
    doc = _min_doc()
    # at the recognition, the hero comes to KNOW (observation); a figure is
    # deceived into a false BELIEF.
    doc["events"][3]["learns"] = [
        {"who": "hero", "fact": "truth_seen(hero)", "via": "realization"}]
    doc["events"][1]["learns"] = [
        {"who": "victim", "fact": "rescue_coming(victim)", "via": "deception"}]
    s = compile_story(doc)   # dialect-agnostic — runs in the substrate build
    held = {}
    for ev in s.fabula:
        for e in ev.effects:
            if isinstance(e, KnowledgeEffect):
                held[(ev.id, e.agent_id)] = e.held
    see = held[("see", "hero")]
    assert see.slot == Slot.KNOWN and see.via == "realization"
    assert see.prop.predicate == "truth_seen"
    # a deception is held as a false BELIEF, not knowledge (dramatic-irony seed)
    turn = held[("turn", "victim")]
    assert turn.slot == Slot.BELIEVED and turn.via == "deception"


def test_unknown_dialect_compile_raises():
    _expect_error_dialect(_stc_doc(), "freytag", "no overlay compiler")


def _expect_error_dialect(doc, dialect, fragment):
    try:
        compile_story(doc, dialect)
    except StoryFormatError as e:
        assert fragment in str(e), f"{fragment!r} not in {e!r}"
    else:
        raise AssertionError(f"expected StoryFormatError for dialect {dialect}")


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
    test_stc_compiles_substrate_and_overlay,
    test_stc_verifies_without_rejecting,
    test_stc_tolerates_unbeated_events,
    test_dramatic_compiles_substrate_and_overlay,
    test_dramatic_verifies_without_rejecting,
    test_dramatic_tolerates_sparse_overlay,
    test_dramatica_compiles_full_storyform,
    test_dramatica_complete_storyform_verifies_clean,
    test_dramatica_dual_dynamic_honored,
    test_dramatica_drops_invalid_pole_not_raises,
    test_learns_compile_to_knowledge_effects,
    test_unknown_dialect_compile_raises,
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
