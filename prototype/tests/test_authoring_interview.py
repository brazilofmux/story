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
    next_questions, run_interview,
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
