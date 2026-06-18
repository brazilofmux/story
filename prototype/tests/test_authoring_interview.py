"""
test_authoring_interview.py — the interview spine, offline.

`interview_gaps` is pure: given an authoring dict it enumerates the missing /
under-committed commitments as questions, with severity. These pin the spine
against the real `authoring.compile_story` contract — blocking gaps are exactly
the things the compiler refuses; structural gaps are the Aristotelian homework.
The extraction half needs the API; the demo exercises it.
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.authoring_interview import (
    interview_gaps, blocking_gaps, structural_gaps, is_compilable,
    next_questions, run_interview, DIALECTS,
)
from story_engine.core.authoring import compile_story, verify_compiled


def _codes(gaps):
    return {g.code for g in gaps}


def _complete_doc():
    return {
        "title": "The Vantage Light",
        "logline": "A keeper's pride wrecks the ship he meant to save.",
        "telling": "chronological",
        "characters": [
            {"id": "halvard", "name": "Halvard", "role": "tragic-hero",
             "hamartia": "pride in his instrument"},
            {"id": "mara", "name": "Mara", "role": "pathos-centre"},
        ],
        "events": [
            {"id": "calm", "when": 1, "who": ["halvard"],
             "summary": "Halvard tends the light, proud of its reach."},
            {"id": "storm", "when": 5, "who": ["halvard", "mara"],
             "summary": "The storm rises; the lens he over-trusts fails.",
             "mark": "peripeteia"},
            {"id": "wreck", "when": 9, "who": ["halvard"],
             "summary": "Halvard sees what his pride has cost.",
             "mark": "anagnorisis", "recognizer": "halvard"},
        ],
        "phases": {"beginning": ["calm"], "middle": ["storm"], "end": ["wreck"]},
    }


def test_empty_doc_blocks_on_the_basics():
    codes = _codes(blocking_gaps({}))
    assert {"no_title", "no_characters", "no_events"} <= codes


def test_event_without_when_blocks():
    doc = _complete_doc()
    doc["events"][1].pop("when")
    g = [x for x in blocking_gaps(doc) if x.code == "event_no_when"]
    assert len(g) == 1 and g[0].target == "storm"


def test_unphased_event_blocks():
    doc = _complete_doc()
    doc["phases"]["middle"] = []          # 'storm' now unphased
    g = [x for x in blocking_gaps(doc) if x.code == "unphased_events"]
    assert len(g) == 1 and "storm" in g[0].question


def test_unknown_participant_blocks():
    doc = _complete_doc()
    doc["events"][0]["who"] = ["ghost"]
    assert "event_unknown_who" in _codes(blocking_gaps(doc))


def test_explicit_telling_requires_staging():
    doc = _complete_doc()
    doc["telling"] = "explicit"
    assert "explicit_no_staging" in _codes(blocking_gaps(doc))


def test_unknown_recognizer_blocks():
    doc = _complete_doc()
    doc["events"][2]["recognizer"] = "nobody"
    assert "recognizer_unknown" in _codes(blocking_gaps(doc))


def test_structural_marks_surface_when_absent():
    doc = _complete_doc()
    for ev in doc["events"]:
        ev.pop("mark", None)
        ev.pop("recognizer", None)
    codes = _codes(structural_gaps(doc))
    assert {"no_peripeteia", "no_anagnorisis"} <= codes


def test_anagnorisis_without_recognizer_is_structural():
    doc = _complete_doc()
    doc["events"][2].pop("recognizer")
    g = [x for x in structural_gaps(doc) if x.code == "anag_no_recognizer"]
    assert len(g) == 1 and g[0].target == "wreck"


def test_tragic_hero_without_hamartia_is_structural():
    doc = _complete_doc()
    doc["characters"][0].pop("hamartia")
    assert "hero_no_hamartia" in _codes(structural_gaps(doc))


def test_missing_pathos_is_structural():
    doc = _complete_doc()
    doc["characters"][1]["role"] = "figure"   # no pathos-centre left
    assert "no_pathos" in _codes(structural_gaps(doc))


def test_complete_doc_has_no_gaps_and_compiles():
    doc = _complete_doc()
    assert interview_gaps(doc) == []          # blocking AND structural clear
    assert is_compilable(doc)
    compiled = compile_story(doc)             # the real compiler accepts it
    assert compiled.title == "The Vantage Light"
    assert len(compiled.fabula) == 3
    assert compiled.mythos.peripeteia_event_id == "storm"
    assert compiled.mythos.anagnorisis_event_id == "wreck"
    # and the dialect self-verifier runs on it without throwing
    verify_compiled(compiled)


def test_next_questions_puts_blocking_first():
    doc = _complete_doc()
    doc.pop("title")                          # 1 blocking
    doc["characters"][0].pop("hamartia")      # 1 structural
    qs = next_questions(doc, n=5)
    assert "title" in qs[0].lower()           # blocking gap leads


# ---- the dialect overlays: each dialect's structural homework -------------
#
# The skeleton (title/characters/events/when/who/phases) is dialect-agnostic;
# the structural gaps are per-dialect. These pin each overlay against its
# dialect verifier's vocabulary, the way the Aristotelian tests above do.


def _stc_complete_doc():
    """A well-formed Save-the-Cat draft: theme, genre, a protagonist, and an
    event on each load-bearing beat (Catalyst → Finale)."""
    beats = ["Catalyst", "Break Into Two", "Midpoint", "All Is Lost",
             "Break Into Three", "Finale"]
    events = [
        {"id": f"e{i}", "when": i + 1, "who": ["nick"],
         "summary": f"beat {b}", "beat": b}
        for i, b in enumerate(beats)
    ]
    return {
        "title": "The Heist",
        "telling": "chronological",
        "theme_statement": "loyalty outlasts greed",
        "genre": "golden-fleece",
        "characters": [{"id": "nick", "name": "Nick", "role": "protagonist"}],
        "events": events,
        "phases": {"beginning": ["e0", "e1"], "middle": ["e2", "e3"],
                   "end": ["e4", "e5"]},
    }


def test_stc_complete_doc_has_no_gaps():
    doc = _stc_complete_doc()
    assert interview_gaps(doc, "save-the-cat") == []
    assert is_compilable(doc, "save-the-cat")


def test_stc_missing_theme_genre_protagonist_surface():
    doc = _stc_complete_doc()
    doc.pop("theme_statement")
    doc.pop("genre")
    doc["characters"][0]["role"] = "ally"
    codes = _codes(structural_gaps(doc, "save-the-cat"))
    assert {"stc_no_theme", "stc_no_genre", "stc_no_protagonist"} <= codes


def test_stc_unfilled_load_bearing_beats_surface():
    doc = _stc_complete_doc()
    for ev in doc["events"]:               # strip every beat assignment
        ev.pop("beat", None)
    g = [x for x in structural_gaps(doc, "save-the-cat")
         if x.code == "stc_unfilled_beats"]
    assert len(g) == 1 and "Catalyst" in g[0].question and "Finale" in g[0].question


def test_stc_unknown_beat_and_genre_flagged():
    doc = _stc_complete_doc()
    doc["events"][0]["beat"] = "Plot Point One"   # not a Save-the-Cat beat
    doc["genre"] = "neo-noir"                      # not one of the ten
    codes = _codes(structural_gaps(doc, "save-the-cat"))
    assert {"stc_unknown_beat", "stc_unknown_genre"} <= codes


def _dramatica_complete_doc():
    """A well-formed Dramatica draft: four throughlines in four distinct
    domains, the eight dynamics, a goal and a consequence."""
    return {
        "title": "The Climb",
        "telling": "chronological",
        "story_goal": "reach the summit before the storm",
        "story_consequence": "the expedition is lost",
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
        "dynamics": [
            {"axis": "resolve", "choice": "change"},
            {"axis": "growth", "choice": "start"},
            {"axis": "approach", "choice": "do-er"},
            {"axis": "problem-solving-style", "choice": "linear"},
            {"axis": "driver", "choice": "action"},
            {"axis": "limit", "choice": "timelock"},
            {"axis": "outcome", "choice": "success"},
            {"axis": "judgment", "choice": "good"},
        ],
        "phases": {"beginning": ["base"], "middle": ["ridge"], "end": ["summit"]},
    }


def test_dramatica_complete_doc_has_no_gaps():
    doc = _dramatica_complete_doc()
    assert interview_gaps(doc, "dramatica") == []
    assert is_compilable(doc, "dramatica")


def test_dramatica_missing_throughlines_domains_dynamics_surface():
    doc = _dramatica_complete_doc()
    doc["throughlines"] = doc["throughlines"][:2]   # drop two roles + domains
    doc["dynamics"] = doc["dynamics"][:5]           # drop three axes
    doc.pop("story_goal")
    codes = _codes(structural_gaps(doc, "dramatica"))
    assert {"dram_missing_throughlines", "dram_missing_dynamics",
            "dram_no_goal"} <= codes


def test_dramatica_domain_collision_and_bad_pole():
    doc = _dramatica_complete_doc()
    doc["throughlines"][1]["domain"] = "activity"   # collides with overall-story
    doc["dynamics"][0]["choice"] = "transform"      # not change|steadfast
    codes = _codes(structural_gaps(doc, "dramatica"))
    assert {"dram_domain_collision", "dram_bad_dynamic"} <= codes


def test_dramatica_dual_dynamic_is_honored():
    # a genuinely-undecided axis given BOTH poles is well-formed, not an error
    # (the ambiguity-honest substrate — see dramatica-precision-limit).
    doc = _dramatica_complete_doc()
    doc["dynamics"][3]["choice"] = ["linear", "holistic"]
    assert "dram_bad_dynamic" not in _codes(structural_gaps(doc, "dramatica"))
    assert interview_gaps(doc, "dramatica") == []


def _dramatic_complete_doc():
    """A well-formed Dramatic draft: an argument with a resolution, a
    main-character throughline, and stakes on each throughline."""
    return {
        "title": "The Verdict",
        "telling": "chronological",
        "characters": [{"id": "dana", "name": "Dana"}],
        "events": [
            {"id": "charge", "when": 1, "who": ["dana"], "summary": "the charge"},
            {"id": "trial", "when": 2, "who": ["dana"], "summary": "the trial"},
            {"id": "verdict", "when": 3, "who": ["dana"], "summary": "the verdict"},
        ],
        "arguments": [
            {"premise": "the law can be just", "resolution": "complicate"},
        ],
        "throughlines": [
            {"role": "overall-story", "owner": "situation",
             "stakes": {"at_risk": "the town's trust", "to_gain": "justice"}},
            {"role": "main-character", "owner": "dana",
             "stakes": {"at_risk": "her career", "to_gain": "her conscience"}},
        ],
        "phases": {"beginning": ["charge"], "middle": ["trial"], "end": ["verdict"]},
    }


def test_dramatic_complete_doc_has_no_gaps():
    doc = _dramatic_complete_doc()
    assert interview_gaps(doc, "dramatic") == []
    assert is_compilable(doc, "dramatic")


def test_dramatic_missing_argument_mc_and_stakes_surface():
    doc = _dramatic_complete_doc()
    doc.pop("arguments")
    doc["throughlines"] = [{"role": "overall-story", "owner": "situation"}]
    codes = _codes(structural_gaps(doc, "dramatic"))
    assert {"dramatic_no_argument", "dramatic_no_main_character",
            "dramatic_throughline_no_stakes"} <= codes


def test_dramatic_bad_resolution_flagged():
    doc = _dramatic_complete_doc()
    doc["arguments"][0]["resolution"] = "maybe"
    assert "dramatic_bad_resolution" in _codes(structural_gaps(doc, "dramatic"))


# ---- cross-dialect invariants ----------------------------------------------

def test_skeleton_blocking_is_dialect_agnostic():
    # the same broken skeleton blocks identically in every dialect
    broken = {"events": [{"id": "x", "who": ["ghost"]}]}   # no title, no chars …
    base = _codes(blocking_gaps(broken, "aristotelian"))
    assert {"no_title", "no_characters", "event_no_when",
            "event_unknown_who", "no_phases"} <= base
    for d in DIALECTS:
        assert _codes(blocking_gaps(broken, d)) == base


def test_unknown_dialect_raises():
    try:
        interview_gaps(_complete_doc(), "freytag")
    except ValueError as e:
        assert "freytag" in str(e)
    else:
        raise AssertionError("expected ValueError for unknown dialect")


def test_aristotelian_is_the_default_dialect():
    doc = _complete_doc()
    assert interview_gaps(doc) == interview_gaps(doc, "aristotelian")


# ---- the multi-round loop controller (pure, injected extract/answer) ----

def _scripted_extract(docs):
    """extract_fn returning the next scripted draft each call (initial call +
    one per answered round)."""
    box = {"i": 0}

    def ex(_brief, _prior, _answers):
        d = docs[min(box["i"], len(docs) - 1)]
        box["i"] += 1
        return d
    return ex


def _always(answer):
    return lambda _questions, _doc: answer


def test_interview_converges_to_complete():
    # sparse -> partial -> complete over three drafts
    partial = _complete_doc()
    partial["events"][1].pop("when")          # one blocking gap left
    run = run_interview(
        brief="x",
        extract_fn=_scripted_extract([{}, partial, _complete_doc()]),
        answer_fn=_always("here are the answers"), max_rounds=6,
    )
    assert run.complete
    assert run.compilable
    assert len(run.rounds) == 3


def test_interview_stalls_when_answers_dont_help():
    stuck = _complete_doc()
    stuck["events"][1].pop("when")            # a gap the answers never fix
    run = run_interview(
        brief="x", extract_fn=_scripted_extract([stuck]),
        answer_fn=_always("unhelpful"), max_rounds=6,
    )
    assert run.rounds[-1].stopped.startswith("stalled")
    assert not run.compilable


def test_interview_stops_when_author_finishes():
    run = run_interview(
        brief="x", extract_fn=_scripted_extract([{}]),
        answer_fn=_always(""),                # author gives nothing
        max_rounds=6,
    )
    assert run.rounds[-1].stopped == "author finished"


def test_interview_respects_max_rounds():
    run = run_interview(
        brief="x", extract_fn=_scripted_extract([{}]),
        answer_fn=_always("more"), max_rounds=1,
    )
    assert run.rounds[-1].stopped == "max rounds reached"


TESTS = [
    test_empty_doc_blocks_on_the_basics,
    test_event_without_when_blocks,
    test_unphased_event_blocks,
    test_unknown_participant_blocks,
    test_explicit_telling_requires_staging,
    test_unknown_recognizer_blocks,
    test_structural_marks_surface_when_absent,
    test_anagnorisis_without_recognizer_is_structural,
    test_tragic_hero_without_hamartia_is_structural,
    test_missing_pathos_is_structural,
    test_complete_doc_has_no_gaps_and_compiles,
    test_next_questions_puts_blocking_first,
    test_stc_complete_doc_has_no_gaps,
    test_stc_missing_theme_genre_protagonist_surface,
    test_stc_unfilled_load_bearing_beats_surface,
    test_stc_unknown_beat_and_genre_flagged,
    test_dramatica_complete_doc_has_no_gaps,
    test_dramatica_missing_throughlines_domains_dynamics_surface,
    test_dramatica_domain_collision_and_bad_pole,
    test_dramatica_dual_dynamic_is_honored,
    test_dramatic_complete_doc_has_no_gaps,
    test_dramatic_missing_argument_mc_and_stakes_surface,
    test_dramatic_bad_resolution_flagged,
    test_skeleton_blocking_is_dialect_agnostic,
    test_unknown_dialect_raises,
    test_aristotelian_is_the_default_dialect,
    test_interview_converges_to_complete,
    test_interview_stalls_when_answers_dont_help,
    test_interview_stops_when_author_finishes,
    test_interview_respects_max_rounds,
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
