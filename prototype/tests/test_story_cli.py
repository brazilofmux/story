"""Pins for the turn-key writer CLI (`story_engine/tools/story.py`,
authoring-cli-sketch-01): session persistence and resume, the next-step
self-direction, per-round crash-safety in the interview, generate
gating + artifacts, and the evaluation payload. All offline — the paid
edges are injected fakes (AC6)."""

import json
import os
import sys
import tempfile
import traceback
from types import SimpleNamespace

from story_engine.tools.story import (
    Session, SessionError, new_session, load_session, save_session,
    next_step, cmd_status, cmd_interview, cmd_generate, cmd_evaluate,
    cmd_revise, record_diff, evaluation_payload,
    SESSION_FILE, DRAFT_FILE, EVAL_FILE, SCENES_FILE,
)
from story_engine.core.fidelity import FidelityFinding, FidelityReport


def _tmp() -> str:
    return os.path.join(tempfile.mkdtemp(prefix="story_cli_test_"), "s")


def _compilable_doc(**over):
    """A minimal Aristotelian record with no blocking gaps (mirrors
    test_authoring._min_doc)."""
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
        "phases": {
            "beginning": ["open"],
            "middle": ["turn"],
            "end": ["fall", "see"],
        },
    }
    doc.update(over)
    return doc


# ---- sessions --------------------------------------------------------------

def test_new_session_persists_and_reloads():
    path = _tmp()
    s = new_session(path, brief="A keeper's pride.", dialect="aristotelian")
    assert os.path.exists(os.path.join(path, SESSION_FILE))
    s2 = load_session(path)
    assert s2.brief == "A keeper's pride."
    assert s2.dialect == "aristotelian"
    assert s2.doc == {}


def test_new_session_rejects_bad_input():
    path = _tmp()
    try:
        new_session(path, brief="x", dialect="not-a-dialect")
    except SessionError:
        pass
    else:
        raise AssertionError("expected SessionError on unknown dialect")
    try:
        new_session(path, brief="   ", dialect="aristotelian")
    except SessionError:
        pass
    else:
        raise AssertionError("expected SessionError on empty brief")


def test_new_session_refuses_to_clobber():
    path = _tmp()
    new_session(path, brief="x", dialect="aristotelian")
    try:
        new_session(path, brief="y", dialect="aristotelian")
    except SessionError:
        pass
    else:
        raise AssertionError("expected SessionError on existing session")


def test_load_session_missing_is_a_friendly_error():
    try:
        load_session(_tmp())
    except SessionError:
        pass
    else:
        raise AssertionError("expected SessionError on missing session")


# ---- next-step self-direction ----------------------------------------------

def test_next_step_walks_the_pipeline():
    path = _tmp()
    s = new_session(path, brief="x", dialect="aristotelian")
    assert next_step(s)[0] == "interview"          # no record yet

    s.data["doc"] = {"title": "T"}                 # record with blocking gaps
    save_session(s)
    assert next_step(s)[0] == "interview"

    s.data["doc"] = _compilable_doc()              # compilable
    save_session(s)
    assert next_step(s)[0] == "generate"

    with open(s.draft_path, "w") as f:             # draft exists
        f.write("prose")
    assert next_step(s)[0] == "evaluate"

    with open(s.eval_path, "w") as f:              # evaluated
        json.dump({"score": 1.0}, f)
    assert next_step(s)[0] == "done"


# ---- interview: resume + per-round persistence ------------------------------

def test_interview_resume_does_not_reextract():
    """A session with a persisted record must NOT call the extractor for
    round one — resume is free."""
    path = _tmp()
    s = new_session(path, brief="x", dialect="aristotelian")
    s.data["doc"] = _compilable_doc()
    save_session(s)
    calls = []

    def extract(brief, prior, answers):
        calls.append((prior is not None, answers))
        return _compilable_doc()

    rc = cmd_interview(s, extract=extract, ask=lambda qs: "", max_rounds=3)
    assert rc == 0
    assert calls == [], f"resume re-extracted: {calls}"


def test_interview_persists_each_round():
    """The record must hit disk BEFORE the writer is asked — a killed
    session keeps the round's extraction."""
    path = _tmp()
    s = new_session(path, brief="x", dialect="aristotelian")
    partial = {"title": "T", "characters": [], "events": []}
    complete = _compilable_doc()
    docs = iter([partial] + [complete] * 4)
    seen_on_disk = []

    def ask(questions):
        on_disk = load_session(path).doc
        seen_on_disk.append(on_disk.get("title") is not None)
        return "answers"

    cmd_interview(s, extract=lambda b, p, a: next(docs), ask=ask,
                  max_rounds=4)
    assert seen_on_disk and all(seen_on_disk)
    assert load_session(path).doc == complete
    assert load_session(path).data["rounds"]


def test_interview_empty_answer_pauses():
    path = _tmp()
    s = new_session(path, brief="x", dialect="aristotelian")
    partial = {"title": "T", "characters": [], "events": []}
    rc = cmd_interview(s, extract=lambda b, p, a: dict(partial),
                       ask=lambda qs: "", max_rounds=4)
    assert rc == 0
    assert load_session(path).doc == partial       # persisted where it paused


# ---- generate: gating + artifacts ------------------------------------------

def test_generate_refuses_blocking_gaps():
    path = _tmp()
    s = new_session(path, brief="x", dialect="aristotelian")
    s.data["doc"] = {"title": "T", "characters": [], "events": []}
    save_session(s)
    rc = cmd_generate(s, generate=lambda **kw: None, assume_yes=True)
    assert rc == 1
    assert not s.has_draft()


def test_generate_writes_draft_and_invalidates_stale_evaluation():
    path = _tmp()
    s = new_session(path, brief="x", dialect="aristotelian")
    s.data["doc"] = _compilable_doc()
    save_session(s)
    with open(s.eval_path, "w") as f:              # stale evaluation
        json.dump({"score": 0.5}, f)
    captured = {}

    def fake_generate(**kw):
        captured.update(kw)
        return SimpleNamespace(title=kw["title"], draft="Scene prose here.")

    rc = cmd_generate(s, generate=fake_generate, assume_yes=True)
    assert rc == 0
    assert s.has_draft()
    with open(s.draft_path) as f:
        text = f.read()
    assert "Scene prose here." in text
    assert not s.has_evaluation(), "stale evaluation must be invalidated"
    assert load_session(path).data["generated"]["words"] == 3
    # The dialect frame was wired (Aristotelian → mythos=).
    assert captured.get("mythos") is not None
    assert "LEAN" in captured["dialect_note"]


def test_generate_declined_confirmation_is_a_clean_no():
    path = _tmp()
    s = new_session(path, brief="x", dialect="aristotelian")
    s.data["doc"] = _compilable_doc()
    save_session(s)
    rc = cmd_generate(s, generate=lambda **kw: None, assume_yes=False)
    # stdin is closed in tests → EOF → declined, not an error.
    assert rc == 0
    assert not s.has_draft()


# ---- revise: the diff policy (RL2) -----------------------------------------

def test_record_diff_scene_scoped_fields():
    old = _compilable_doc()
    new = _compilable_doc()
    new["events"] = [dict(e) for e in new["events"]]
    new["events"][0]["summary"] = "it opens, colder"
    new["events"][2]["note"] = "dwell on the silence"
    d = record_diff(old, new)
    assert not d.bible_changed
    assert d.changed_events == ["open", "fall"]
    assert not d.full_regeneration


def test_record_diff_bible_scoped_fields():
    old = _compilable_doc()
    for key, val in [("logline", "a different test"),
                     ("telling", "reverse"),
                     ("characters", [])]:
        new = _compilable_doc(**{key: val})
        d = record_diff(old, new)
        assert key in d.bible_changed, key
        assert d.full_regeneration


def test_record_diff_event_mark_or_when_is_bible_scoped():
    old = _compilable_doc()
    new = _compilable_doc()
    new["events"] = [dict(e) for e in new["events"]]
    new["events"][1]["when"] = 4
    d = record_diff(old, new)
    assert d.full_regeneration and not d.changed_events


def test_record_diff_added_or_removed_events_is_bible_scoped():
    old = _compilable_doc()
    new = _compilable_doc()
    new["events"] = list(new["events"]) + [
        {"id": "extra", "when": 10, "who": ["hero"], "summary": "more"}]
    d = record_diff(old, new)
    assert "events (added/removed)" in d.bible_changed


def test_record_diff_identical_is_empty():
    assert record_diff(_compilable_doc(), _compilable_doc()).empty


# ---- revise: the flows (RL1, RL3–RL5) --------------------------------------

def _revisable_session():
    """A session with a compilable record, a structured draft, a draft.md,
    and an evaluation."""
    path = _tmp()
    s = new_session(path, brief="x", dialect="aristotelian")
    s.data["doc"] = _compilable_doc()
    save_session(s)
    payload = {"title": "Test", "story_bible": "bible", "scenes": [
        {"tau_d": i, "event_id": eid, "focalizer": None,
         "prose": f"prose of {eid}."}
        for i, eid in enumerate(["open", "turn", "fall", "see"])]}
    with open(s.scenes_path, "w") as f:
        json.dump(payload, f)
    with open(s.draft_path, "w") as f:
        f.write("old draft")
    with open(s.eval_path, "w") as f:
        json.dump({"score": 1.0}, f)
    return path, s


def test_revise_scene_scoped_splices_only_the_target():
    path, s = _revisable_session()
    revised = _compilable_doc()
    revised["events"] = [dict(e) for e in revised["events"]]
    revised["events"][1]["note"] = "make the reversal colder"
    rendered = []

    def render(directive, compiled, before):
        rendered.append((directive.event_id, before))
        return "COLDER REVERSAL PROSE."

    rc = cmd_revise(s, notes="make the reversal colder",
                    extract=lambda n, prior: revised, render=render,
                    assume_yes=True)
    assert rc == 0
    assert [e for e, _ in rendered] == ["turn"]
    assert rendered[0][1] == "prose of turn."     # old prose passed as before
    with open(s.scenes_path) as f:
        scenes = json.load(f)["scenes"]
    assert scenes[1]["prose"] == "COLDER REVERSAL PROSE."
    assert scenes[0]["prose"] == "prose of open." # neighbors untouched
    with open(s.draft_path) as f:
        text = f.read()
    assert "COLDER REVERSAL PROSE." in text and "prose of open." in text
    assert not s.has_evaluation(), "revision must invalidate the blind read"
    assert load_session(path).doc == revised      # the record is the truth
    assert load_session(path).data["revisions"][0]["scope"] == ["turn"]


def test_revise_bible_scoped_regenerates_fully():
    path, s = _revisable_session()
    revised = _compilable_doc(logline="a colder test")
    calls = []

    def fake_generate(**kw):
        calls.append(kw)
        return SimpleNamespace(title=kw["title"], draft="WHOLE NEW DRAFT.")

    rc = cmd_revise(s, notes="colder throughout",
                    extract=lambda n, prior: revised,
                    generate=fake_generate, assume_yes=True)
    assert rc == 0
    assert len(calls) == 1                        # full regeneration ran
    with open(s.draft_path) as f:
        assert "WHOLE NEW DRAFT." in f.read()
    assert load_session(path).doc == revised


def test_revise_noop_diff_is_surfaced_and_keeps_the_record():
    path, s = _revisable_session()
    rc = cmd_revise(s, notes="something vague",
                    extract=lambda n, prior: _compilable_doc(),
                    render=lambda *a: "X", assume_yes=True)
    assert rc == 0
    assert load_session(path).doc == _compilable_doc()
    with open(s.draft_path) as f:
        assert f.read() == "old draft"            # nothing regenerated
    assert s.has_evaluation()                     # nothing invalidated


def test_revise_that_breaks_the_record_keeps_the_working_one():
    path, s = _revisable_session()
    broken = {"title": "T", "characters": [], "events": []}
    rc = cmd_revise(s, notes="delete everyone",
                    extract=lambda n, prior: broken,
                    render=lambda *a: "X", assume_yes=True)
    assert rc == 1
    assert load_session(path).doc == _compilable_doc()


def test_revise_without_structured_draft_falls_back_to_full():
    path, s = _revisable_session()
    os.remove(s.scenes_path)                      # draft predates scenes.json
    revised = _compilable_doc()
    revised["events"] = [dict(e) for e in revised["events"]]
    revised["events"][0]["summary"] = "changed"
    calls = []

    def fake_generate(**kw):
        calls.append(kw)
        return SimpleNamespace(title=kw["title"], draft="REGENERATED.")

    rc = cmd_revise(s, notes="change the opening",
                    extract=lambda n, prior: revised,
                    generate=fake_generate, assume_yes=True)
    assert rc == 0
    assert len(calls) == 1


def test_generate_persists_structured_draft():
    path = _tmp()
    s = new_session(path, brief="x", dialect="aristotelian")
    s.data["doc"] = _compilable_doc()
    save_session(s)

    def fake_generate(**kw):
        scenes = [SimpleNamespace(τ_d=i, event_id=e.event_id, focalizer=None,
                                  prose=f"p{i}")
                  for i, e in enumerate(kw["sjuzhet"])]
        return SimpleNamespace(title=kw["title"], story_bible="b",
                               scenes=scenes,
                               draft="\n\n".join(s.prose for s in scenes))

    rc = cmd_generate(s, generate=fake_generate, assume_yes=True)
    assert rc == 0
    with open(s.scenes_path) as f:
        payload = json.load(f)
    assert len(payload["scenes"]) == 4
    assert payload["scenes"][0]["event_id"] == "open"


# ---- evaluate: payload + persistence ---------------------------------------

def _report():
    r = FidelityReport(title="Test")
    r.findings.append(FidelityFinding("plot_kind", "complex", "complex",
                                      "preserved"))
    r.findings.append(FidelityFinding("pathos_centre", "Victim", "(none)",
                                      "lost", "did not survive"))
    return r


def test_evaluate_requires_a_draft():
    path = _tmp()
    s = new_session(path, brief="x", dialect="aristotelian")
    s.data["doc"] = _compilable_doc()
    save_session(s)
    rc = cmd_evaluate(s, evaluate=lambda c, t: _report(), assume_yes=True)
    assert rc == 1


def test_evaluate_saves_payload():
    path = _tmp()
    s = new_session(path, brief="x", dialect="aristotelian")
    s.data["doc"] = _compilable_doc()
    save_session(s)
    with open(s.draft_path, "w") as f:
        f.write("prose")
    rc = cmd_evaluate(s, evaluate=lambda c, t: _report(), assume_yes=True)
    assert rc == 0
    with open(s.eval_path) as f:
        ev = json.load(f)
    assert ev["preserved"] == 1 and ev["total"] == 2
    assert ev["score"] == 0.5
    assert {f["dimension"] for f in ev["findings"]} == {"plot_kind",
                                                        "pathos_centre"}
    assert next_step(s)[0] == "done"


def test_evaluation_payload_shape():
    p = evaluation_payload(_report())
    assert p["findings"][1]["verdict"] == "lost"
    assert p["findings"][1]["note"] == "did not survive"


TESTS = [
    test_record_diff_scene_scoped_fields,
    test_record_diff_bible_scoped_fields,
    test_record_diff_event_mark_or_when_is_bible_scoped,
    test_record_diff_added_or_removed_events_is_bible_scoped,
    test_record_diff_identical_is_empty,
    test_revise_scene_scoped_splices_only_the_target,
    test_revise_bible_scoped_regenerates_fully,
    test_revise_noop_diff_is_surfaced_and_keeps_the_record,
    test_revise_that_breaks_the_record_keeps_the_working_one,
    test_revise_without_structured_draft_falls_back_to_full,
    test_generate_persists_structured_draft,
    test_new_session_persists_and_reloads,
    test_new_session_rejects_bad_input,
    test_new_session_refuses_to_clobber,
    test_load_session_missing_is_a_friendly_error,
    test_next_step_walks_the_pipeline,
    test_interview_resume_does_not_reextract,
    test_interview_persists_each_round,
    test_interview_empty_answer_pauses,
    test_generate_refuses_blocking_gaps,
    test_generate_writes_draft_and_invalidates_stale_evaluation,
    test_generate_declined_confirmation_is_a_clean_no,
    test_evaluate_requires_a_draft,
    test_evaluate_saves_payload,
    test_evaluation_payload_shape,
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
