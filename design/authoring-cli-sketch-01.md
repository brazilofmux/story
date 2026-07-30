# Authoring CLI — sketch 01 (the turn-key writer front-end)

**Status:** active; **landed** 2026-07-30 — all six commitments
implemented (`story_engine/tools/story.py`; `dialect_story_object` /
`frame_kwargs_for` in `authoring.py`; demo rewired to the shared
switch); 14 offline pins in `tests/test_story_cli.py`; live interview
run pending an `ANTHROPIC_API_KEY` session.
**Date:** 2026-07-30
**Extends:** [authoring-interview-sketch-02](authoring-interview-sketch-02.md)
(the multi-round loop), [authoring-compile-sketch-01](authoring-compile-sketch-01.md)
(per-dialect compile), and the demo pair `demos/author_by_interview.py` /
`demos/author_story.py`.
**Frames:** memory `project-goal-generation-tool` (generation-first end
goal); the July 2026 assessment that the interview is the writer-facing
seam and the missing piece between "provable" and "usable" is packaging,
not research.

## The gap this closes

Every stage a writer needs exists and is proven live — interview →
compile → verify → generate → blind evaluate, for all four dialects.
What does NOT exist is a way to run that chain without assembling it by
hand: the interview demo takes `--answers` as a command-line string and
forgets everything between invocations; the `.story.toml` demo skips the
interview and is Aristotelian-only past compile; nothing persists a
session, shows a writer where they are, or says what the next step is.
The chain is a proof, not a tool. This sketch commits to the tool.

## Commitments

**AC1 — one entry point, resumable, self-directing.**
`python3 -m story_engine.tools.story <command> <session-dir>` with five
commands: `new`, `status`, `interview`, `generate`, `evaluate`. Bare
`story <session-dir>` = `status`. Every command ends by naming the next
step ("next: … interview" / "… generate" / "draft is evaluated — read
it"), so a writer never needs to know the pipeline to walk it.

**AC2 — a story session is a directory.** `story.json` (the evolving
authoring dict + meta: dialect, brief, round history, timestamps),
`draft.md` (the generated draft), `evaluation.json` (the blind read +
fidelity findings). Persisted after **every** interview round — a
killed session resumes where it stopped. JSON, not TOML: the stdlib
reads TOML but cannot write it, and the persisted doc is exactly the
dict `compile_story` consumes; a `.story.toml` export is deferred until
someone actually wants to hand-edit outside the interview.

**AC3 — one interview loop, two kinds of author.** The CLI adds an
interactive `answer_fn` (questions printed, multi-line answers on
stdin, blank line ends the answer, empty answer ends the session) and
an `extract_fn` that returns the persisted doc on the first round
(resume is free — no re-extraction) and calls `extract_story_draft`
with the writer's answers thereafter. `run_interview` itself is
untouched: the same loop serves the AI-simulated author (the demo) and
the human (the CLI).

**AC4 — honest cost surface, counts not dollars.** Before any paid
step the CLI states the shape of the spend — "generation: N scene
calls, up to M tokens each, effort E; evaluation: 1 call at 8k" — and
asks (or `--yes`). Dollar figures are deliberately absent: prices rot,
call shapes don't. Defaults encode the Winter Count run lessons:
effort `high` with `max_tokens` 12000 (adaptive thinking shares the
budget; the fail-loud seam aborts underfunded calls), and the dialect
note carries "scenes are LEAN: 700–1200 words" against scene
ballooning.

**AC5 — the per-dialect object/frame switch is extracted, once.**
`authoring.py` gains `dialect_story_object(compiled)` (the compiled
overlay → the dialect's canonical story object: `ArMythos` /
`StcStorySheet` / `DramaticStory` / `DramaticaStoryform`) and
`frame_kwargs_for(compiled)` (→ the `generate_draft` kwargs, `mythos=`
or `adapter=`). Earned, not speculative: `demos/author_by_interview.py`
already builds this switch inline and the CLI is the second client; the
demo is rewired to the shared helper. The evaluate-side switch
(decompile + compare per dialect) lives in the CLI module — it has one
client today and moves out when it earns two.

**AC6 — offline-testable spine, injected edges.** Session load/save,
gap gating, next-step logic, the interview driver, and the cost
summary are pure and tested with fakes (the `run_interview` pattern).
Everything that costs money is behind an injected function or an
explicit command with an API-key check; `status` and `new` never touch
the network.

## Non-goals

- No revision loop (writer notes → substrate edits → regenerate). That
  is the return trip — its own sketch, next.
- No storyform-proposal mode ("here are three ways your story could
  end"). After the return trip.
- No convergence in the CLI yet — `generate` + `evaluate` shows the
  writer the fidelity table; wiring `converge` behind a flag is cheap
  later, but a first draft plus an honest score is the product today.
- No TOML export, no packaging (`pip install`), no TUI. Directory +
  stdlib + the venv the repo already requires.

## Open questions

- Should `evaluate` offer the cross-family check (`--model grok-…`)
  when `XAI_API_KEY` is present? Probably yes and cheap, but the
  cross-family number's meaning (agreement, not self-grade) deserves
  its own presentation — deferred to keep this sketch small.
- Interview stall handling for humans: `run_interview` stops when a
  round's answers don't reduce the gap count. For a human that can be
  one terse answer away from unfair; the CLI surfaces the stall and
  invites `interview` again (the resume is free), rather than looping
  forever. Revisit if real sessions stall often.
