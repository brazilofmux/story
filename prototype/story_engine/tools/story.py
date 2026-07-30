"""
story.py — the turn-key writer front-end (`authoring-cli-sketch-01`).

One entry point that walks a writer through the whole chain — interview
→ compile → verify → generate → blind evaluate — with the session
persisted in a directory, resumable at every step, and each command
naming the next one. The writer never needs to know the pipeline to
walk it.

Usage:
    cd prototype

    # Start a story session (offline — no API):
    PYTHONPATH=. python3 -m story_engine.tools.story new mystory \\
        --dialect dramatica --brief "A lighthouse keeper's pride ..."

    # Where am I? What's next? (offline):
    PYTHONPATH=. python3 -m story_engine.tools.story status mystory

    # The interview: the engine asks its structural homework, you
    # answer in plain language (needs ANTHROPIC_API_KEY + venv):
    PYTHONPATH=. .venv/bin/python3 -m story_engine.tools.story interview mystory

    # Generate the draft (shows the call shape and asks first):
    PYTHONPATH=. .venv/bin/python3 -m story_engine.tools.story generate mystory

    # Score it blind against your own structure:
    PYTHONPATH=. .venv/bin/python3 -m story_engine.tools.story evaluate mystory

The session directory holds `story.json` (the evolving authoring record
+ history), `draft.md`, and `evaluation.json`. Every interview round is
persisted, so a killed session resumes where it stopped.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys

from story_engine.core.authoring_interview import (
    DIALECTS, interview_gaps, blocking_gaps, run_interview,
)
from story_engine.core.authoring import (
    compile_story, verify_compiled, dialect_story_object, frame_kwargs_for,
    StoryFormatError,
)

SESSION_FILE = "story.json"
DRAFT_FILE = "draft.md"
EVAL_FILE = "evaluation.json"

# Run lessons from the Winter Count generation (winter-count-sketch-01):
# high effort shares the token budget with adaptive thinking — underfund
# it and the fail-loud seam aborts; and without a leanness directive
# scenes balloon.
DEFAULT_EFFORT = "high"
DEFAULT_MAX_TOKENS = 12000
LEAN_NOTE = "Scenes are LEAN: 700-1200 words."


class SessionError(Exception):
    """A human-facing session problem — phrased for the writer."""


def _now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


class Session:
    """A story session directory: `story.json` + the artifacts beside it."""

    def __init__(self, path: str, data: dict):
        self.path = path
        self.data = data

    # -- fields ------------------------------------------------------------
    @property
    def brief(self) -> str:
        return self.data.get("brief", "")

    @property
    def dialect(self) -> str:
        return self.data.get("dialect", "aristotelian")

    @property
    def doc(self) -> dict:
        return self.data.get("doc") or {}

    @property
    def draft_path(self) -> str:
        return os.path.join(self.path, DRAFT_FILE)

    @property
    def eval_path(self) -> str:
        return os.path.join(self.path, EVAL_FILE)

    def has_draft(self) -> bool:
        return os.path.exists(self.draft_path)

    def has_evaluation(self) -> bool:
        return os.path.exists(self.eval_path)


def new_session(path: str, *, brief: str, dialect: str) -> Session:
    if dialect not in DIALECTS:
        raise SessionError(
            f"unknown dialect {dialect!r} — choose one of: "
            f"{', '.join(sorted(DIALECTS))}")
    if not brief.strip():
        raise SessionError("the brief is empty — a session starts from a "
                           "few sentences about the story you want")
    session_file = os.path.join(path, SESSION_FILE)
    if os.path.exists(session_file):
        raise SessionError(f"{path} already holds a story session — "
                           f"run `status` on it instead")
    os.makedirs(path, exist_ok=True)
    s = Session(path, {
        "version": 1,
        "created": _now(),
        "updated": _now(),
        "brief": brief.strip(),
        "dialect": dialect,
        "doc": None,
        "rounds": [],
    })
    save_session(s)
    return s


def load_session(path: str) -> Session:
    session_file = os.path.join(path, SESSION_FILE)
    if not os.path.exists(session_file):
        raise SessionError(
            f"no story session at {path} — start one with "
            f"`new {path} --brief \"...\"`")
    with open(session_file) as f:
        return Session(path, json.load(f))


def save_session(s: Session) -> None:
    s.data["updated"] = _now()
    tmp = os.path.join(s.path, SESSION_FILE + ".tmp")
    with open(tmp, "w") as f:
        json.dump(s.data, f, indent=1)
    os.replace(tmp, os.path.join(s.path, SESSION_FILE))


# ============================================================================
# The next-step logic — the CLI's self-direction (AC1)
# ============================================================================


def next_step(s: Session) -> tuple:
    """(command, human hint) — the next thing this session needs."""
    if not s.doc:
        return ("interview",
                "extract the first record from your brief and answer the "
                "engine's questions")
    blocking = blocking_gaps(s.doc, s.dialect)
    if blocking:
        return ("interview",
                f"{len(blocking)} blocking question(s) remain — the record "
                f"cannot compile yet")
    if not s.has_draft():
        structural = [g for g in interview_gaps(s.doc, s.dialect)
                      if g.severity == "structural"]
        extra = (f" ({len(structural)} structural question(s) are open — "
                 f"more interview sharpens the structure, or generate now)"
                 if structural else "")
        return ("generate", "the record compiles — generate the draft" + extra)
    if not s.has_evaluation():
        return ("evaluate",
                "score the draft blind against your authored structure")
    return ("done",
            f"draft + evaluation complete — read {DRAFT_FILE}, or keep "
            f"interviewing and regenerate")


def _print_next(s: Session) -> None:
    cmd, hint = next_step(s)
    if cmd == "done":
        print(f"\nnext: {hint}")
    else:
        print(f"\nnext: `... {cmd} {s.path}` — {hint}")


# ============================================================================
# status (offline)
# ============================================================================


def cmd_status(s: Session) -> int:
    doc = s.doc
    print(f"STORY SESSION — {s.path}")
    print(f"  dialect: {s.dialect} | created {s.data.get('created')} | "
          f"updated {s.data.get('updated')}")
    print(f"  brief: {s.brief[:140]}{'…' if len(s.brief) > 140 else ''}")
    if not doc:
        print("  record: (not yet extracted — the interview starts it)")
    else:
        print(f"  record: '{doc.get('title', '(untitled)')}' — "
              f"{len(doc.get('characters') or [])} character(s), "
              f"{len(doc.get('events') or [])} event(s); "
              f"{len(s.data.get('rounds') or [])} interview round(s) so far")
        gaps = interview_gaps(doc, s.dialect)
        blk = [g for g in gaps if g.severity == "blocking"]
        stc = [g for g in gaps if g.severity == "structural"]
        print(f"  open questions: {len(blk)} blocking, {len(stc)} structural")
        for g in blk[:5]:
            print(f"    ● {g.question}")
        for g in stc[:3]:
            print(f"    ○ {g.question}")
    if s.has_draft():
        with open(s.draft_path) as f:
            words = len(f.read().split())
        print(f"  draft: {DRAFT_FILE} ({words} words)")
    if s.has_evaluation():
        with open(s.eval_path) as f:
            ev = json.load(f)
        print(f"  fidelity: {ev.get('preserved')}/{ev.get('total')} "
              f"preserved ({round(100 * ev.get('score', 0))}%)")
    _print_next(s)
    return 0


# ============================================================================
# interview (needs API unless resuming a finished record)
# ============================================================================


def _stdin_author(questions: list) -> str:
    """The interactive answer_fn: print the round's questions, read the
    writer's answers (multi-line; blank line finishes). An empty answer
    ends the interview — the session persists and resumes any time."""
    print("\nThe engine asks:")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")
    print("\nAnswer in plain language (blank line to finish; just a blank "
          "line to pause the interview here):")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines)


def cmd_interview(s: Session, *, extract=None, ask=None,
                  max_rounds: int = 8, effort: str = DEFAULT_EFFORT,
                  ask_structural: bool = True) -> int:
    """Run (or resume) the interview. `extract` and `ask` are injectable
    for tests; the defaults are the live extractor and stdin."""
    if extract is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("ERROR: ANTHROPIC_API_KEY is not set — the interview's "
                  "extraction step needs it. (`status` works offline.)",
                  file=sys.stderr)
            return 1
        from story_engine.core.authoring_interview import extract_story_draft

        def extract(brief, prior, answers):
            return extract_story_draft(
                brief, dialect=s.dialect, prior=prior, answers=answers,
                effort=effort)
    ask = ask or _stdin_author

    resumed = {"pending": bool(s.doc)}

    def extract_fn(brief, prior, answers):
        # Resume is free: the first round reuses the persisted record
        # instead of re-extracting from the brief.
        if resumed["pending"]:
            resumed["pending"] = False
            return s.doc
        doc = extract(brief, prior, answers) or {}
        return doc

    def answer_fn(questions, doc):
        # Persist BEFORE asking — a killed session keeps this round's
        # extraction (AC2).
        s.data["doc"] = doc
        save_session(s)
        return ask(questions)

    def on_round(rec, blocking, structural):
        s.data["rounds"].append({
            "at": _now(), "round": rec.round,
            "blocking": rec.n_blocking, "structural": rec.n_structural,
        })
        print(f"\n[round {len(s.data['rounds'])}] {rec.n_blocking} blocking, "
              f"{rec.n_structural} structural question(s) open"
              + (f" — {rec.stopped}" if rec.stopped else ""))

    run = run_interview(
        brief=s.brief, dialect=s.dialect,
        extract_fn=extract_fn, answer_fn=answer_fn,
        max_rounds=max_rounds, ask_structural=ask_structural,
        on_round=on_round,
    )
    s.data["doc"] = run.final_doc
    save_session(s)

    last = run.rounds[-1] if run.rounds else None
    if run.complete:
        print("\nThe record is well-formed — every structural question is "
              "answered.")
    elif last is not None and last.stopped:
        print(f"\nInterview paused: {last.stopped}. The session is saved — "
              f"`interview` again to continue.")
    if run.compilable:
        print("It compiles: the story can be generated.")
    _print_next(s)
    return 0


# ============================================================================
# generate (needs API)
# ============================================================================


def _confirm(prompt: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    try:
        return input(f"{prompt} [y/N] ").strip().lower() in ("y", "yes")
    except EOFError:
        return False


def cmd_generate(s: Session, *, generate=None, force: bool = False,
                 assume_yes: bool = False, effort: str = DEFAULT_EFFORT,
                 max_tokens: int = DEFAULT_MAX_TOKENS) -> int:
    """Compile, verify, state the call shape, confirm, generate, save."""
    doc = s.doc
    if not doc:
        print("Nothing to generate yet — the interview hasn't produced a "
              "record.", file=sys.stderr)
        _print_next(s)
        return 1
    blocking = blocking_gaps(doc, s.dialect)
    if blocking:
        print(f"Cannot compile: {len(blocking)} blocking question(s) remain:",
              file=sys.stderr)
        for g in blocking[:5]:
            print(f"  ● {g.question}", file=sys.stderr)
        _print_next(s)
        return 1

    try:
        compiled = compile_story(doc, s.dialect)
    except StoryFormatError as e:
        print(f"AUTHORING ERROR: {e}", file=sys.stderr)
        return 1
    print(f"Compiled '{compiled.title}' ({s.dialect}): "
          f"{len(compiled.entities)} entities, {len(compiled.fabula)} events, "
          f"{len(compiled.sjuzhet)} staged scenes.")

    obs = verify_compiled(compiled)
    if obs:
        print(f"⚠ the {s.dialect} self-verifier reports "
              f"{len(obs)} finding(s):")
        for o in obs:
            print(f"  [{getattr(o, 'severity', '?')}] "
                  f"{getattr(o, 'code', '')}: {getattr(o, 'message', o)}")
        if not force:
            print("Not generating — fix the findings (more interview), or "
                  "pass --force.", file=sys.stderr)
            return 1
    else:
        print("✓ verifies clean.")

    # The honest cost surface (AC4): call shape, not dollars.
    n = len(compiled.sjuzhet)
    print(f"\nGeneration will make {n} scene call(s), each up to "
          f"{max_tokens} tokens at effort '{effort}', plus the story bible "
          f"context each call carries.")
    if not _confirm("Generate the draft?", assume_yes):
        print("Not generating.")
        return 0

    if generate is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("ERROR: ANTHROPIC_API_KEY is not set — needed to generate.",
                  file=sys.stderr)
            return 1
        from story_engine.core.draft_generator import generate_draft
        generate = generate_draft

    def on_scene(sc):
        print(f"  [scene {sc.τ_d}] {sc.event_id:24s} "
              f"→ {len(sc.prose.split())} words")

    note = (f"A {s.dialect} story authored by interview. "
            + (compiled.logline or "") + " " + LEAN_NOTE).strip()
    result = generate(
        title=compiled.title, sjuzhet=compiled.sjuzhet,
        fabula=compiled.fabula, entities=compiled.entities,
        descriptions=compiled.descriptions,
        preplay_disclosures=compiled.preplay_disclosures,
        dialect_note=note, effort=effort, max_tokens=max_tokens,
        on_scene=on_scene, **frame_kwargs_for(compiled),
    )

    with open(s.draft_path, "w") as f:
        f.write(f"# {result.title} — first draft\n\n")
        if compiled.logline:
            f.write(f"_{compiled.logline}_\n\n")
        f.write(f"_A {s.dialect} story, authored by interview and generated "
                f"from the verified substrate._\n\n")
        f.write(result.draft)
    words = len(result.draft.split())
    s.data["generated"] = {"at": _now(), "words": words,
                           "effort": effort, "max_tokens": max_tokens}
    # A regenerated draft invalidates the old evaluation.
    if s.has_evaluation():
        os.remove(s.eval_path)
    save_session(s)
    print(f"\nDraft saved: {s.draft_path} ({words} words)")
    _print_next(s)
    return 0


# ============================================================================
# evaluate (needs API)
# ============================================================================


def _build_evaluator(dialect: str):
    """(decompile_fn, compare_fn) for the dialect — the blind read and
    the offline comparison. Imported lazily (pydantic surfaces)."""
    if dialect == "aristotelian":
        from story_engine.core.draft_evaluator import (
            decompile_draft, compare_to_mythos)
        return decompile_draft, compare_to_mythos
    if dialect == "save-the-cat":
        from story_engine.core.save_the_cat_evaluator import (
            decompile_stc, compare_to_sheet)
        return decompile_stc, compare_to_sheet
    if dialect == "dramatic":
        from story_engine.core.dramatic_evaluator import (
            decompile_dramatic, compare_to_story)
        return decompile_dramatic, compare_to_story
    from story_engine.core.dramatica_evaluator import (
        decompile_dramatica, compare_to_storyform)
    return decompile_dramatica, compare_to_storyform


def evaluation_payload(report) -> dict:
    """A FidelityReport → the JSON persisted beside the draft."""
    return {
        "at": _now(),
        "score": report.score,
        "preserved": report.preserved,
        "total": len(report.scored),
        "findings": [
            {"dimension": f.dimension, "authored": f.authored,
             "decompiled": f.decompiled, "verdict": f.verdict,
             "note": f.note}
            for f in report.findings
        ],
    }


_MARK = {"preserved": "✓", "drifted": "~", "lost": "✗", "added": "+"}


def cmd_evaluate(s: Session, *, evaluate=None, assume_yes: bool = False,
                 effort: str = "high") -> int:
    """Decompile the draft blind in the session's dialect and score it
    against the compiled structure. `evaluate(compiled, draft_text)` →
    FidelityReport is injectable for tests."""
    if not s.has_draft():
        print("No draft to evaluate — generate first.", file=sys.stderr)
        _print_next(s)
        return 1
    with open(s.draft_path) as f:
        draft_text = f.read()
    try:
        compiled = compile_story(s.doc, s.dialect)
    except StoryFormatError as e:
        print(f"AUTHORING ERROR: {e}", file=sys.stderr)
        return 1

    print("Evaluation is a blind read: 1 call over the whole draft "
          f"({len(draft_text.split())} words) at effort '{effort}'. The "
          "reader is given the genre, never your structure.")
    if not _confirm("Evaluate?", assume_yes):
        print("Not evaluating.")
        return 0

    if evaluate is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("ERROR: ANTHROPIC_API_KEY is not set — needed for the "
                  "blind read.", file=sys.stderr)
            return 1
        decompile_fn, compare_fn = _build_evaluator(s.dialect)
        target = dialect_story_object(compiled)

        def evaluate(compiled_, draft_text_):
            reading = decompile_fn(draft_text_, title=compiled_.title,
                                   effort=effort)
            return compare_fn(reading, target)

    report = evaluate(compiled, draft_text)
    for fnd in report.findings:
        print(f"  {_MARK.get(fnd.verdict, '?')} {fnd.dimension:22s} "
              f"authored={fnd.authored!r:30s} read={fnd.decompiled!r}")
    print(f"\n  FIDELITY: {report.preserved}/{len(report.scored)} preserved "
          f"({round(100 * report.score)}%)")

    with open(s.eval_path, "w") as f:
        json.dump(evaluation_payload(report), f, indent=1)
    save_session(s)
    print(f"Saved: {s.eval_path}")
    _print_next(s)
    return 0


# ============================================================================
# CLI
# ============================================================================


def _cli(argv=None):
    p = argparse.ArgumentParser(
        prog="story", description=__doc__.split("\n\n", 1)[0])
    sub = p.add_subparsers(dest="command")

    p_new = sub.add_parser("new", help="start a story session")
    p_new.add_argument("session")
    p_new.add_argument("--brief", default="",
                       help="a few sentences about the story (prompted for "
                            "if omitted)")
    p_new.add_argument("--dialect", default="aristotelian",
                       choices=sorted(DIALECTS))

    p_st = sub.add_parser("status", help="where the session is; what's next")
    p_st.add_argument("session")

    p_iv = sub.add_parser("interview", help="answer the engine's questions")
    p_iv.add_argument("session")
    p_iv.add_argument("--max-rounds", type=int, default=8)
    p_iv.add_argument("--skeleton-only", action="store_true",
                      help="ask only blocking questions (skip the dialect's "
                           "structural polish)")
    p_iv.add_argument("--effort", default=DEFAULT_EFFORT,
                      choices=["low", "medium", "high", "max"])

    p_gen = sub.add_parser("generate", help="compile, verify, generate")
    p_gen.add_argument("session")
    p_gen.add_argument("--force", action="store_true",
                       help="generate even with verifier findings")
    p_gen.add_argument("--yes", action="store_true",
                       help="skip the confirmation prompt")
    p_gen.add_argument("--effort", default=DEFAULT_EFFORT,
                       choices=["low", "medium", "high", "max"])
    p_gen.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)

    p_ev = sub.add_parser("evaluate", help="blind-read the draft and score it")
    p_ev.add_argument("session")
    p_ev.add_argument("--yes", action="store_true")

    # bare `story <dir>` = status
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in ("new", "status", "interview", "generate",
                                "evaluate", "-h", "--help"):
        argv = ["status"] + argv
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _cli(argv)
    if not getattr(args, "command", None):
        print("usage: story {new,status,interview,generate,evaluate} "
              "<session-dir>", file=sys.stderr)
        return 2
    try:
        if args.command == "new":
            brief = args.brief
            if not brief.strip():
                print("A few sentences about the story (end with a blank "
                      "line):")
                lines = []
                while True:
                    try:
                        line = input()
                    except EOFError:
                        break
                    if not line.strip():
                        break
                    lines.append(line)
                brief = "\n".join(lines)
            s = new_session(args.session, brief=brief, dialect=args.dialect)
            print(f"Started '{args.session}' ({args.dialect}).")
            _print_next(s)
            return 0

        s = load_session(args.session)
        if args.command == "status":
            return cmd_status(s)
        if args.command == "interview":
            return cmd_interview(s, max_rounds=args.max_rounds,
                                 effort=args.effort,
                                 ask_structural=not args.skeleton_only)
        if args.command == "generate":
            return cmd_generate(s, force=args.force, assume_yes=args.yes,
                                effort=args.effort,
                                max_tokens=args.max_tokens)
        if args.command == "evaluate":
            return cmd_evaluate(s, assume_yes=args.yes)
    except SessionError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
