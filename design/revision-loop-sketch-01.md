# Revision loop — sketch 01 (the writer's return trip)

**Status:** active; **landed** 2026-07-30 — all six commitments
implemented (`cmd_revise` + `record_diff` in
`story_engine/tools/story.py`; `generate` persists the structured
draft); 11 offline pins added to `tests/test_story_cli.py`; live
revision run pending an `ANTHROPIC_API_KEY` session.
**Date:** 2026-07-30
**Extends:** [authoring-cli-sketch-01](authoring-cli-sketch-01.md) (the
session), [authoring-interview-sketch-02](authoring-interview-sketch-02.md)
(the extractor), and the repair machinery
(`draft_repair.repair_scene`, `draft_generator.result_to_payload`,
`draft_convergence.assemble`).
**Frames:** architecture commitment A3 (structure in typed projections,
affect/tone in descriptions) — extended here from authoring to
*revision*.

## The gap this closes

A writer's real workflow is draft → notes → revise. The engine has
structural repair (evaluator-driven: fix what drifted from the record)
but no path for **writer-driven** revision: "make the sister colder,"
"the ending should be a failure after all," "less weather." Today
those notes have nowhere to land except hand-editing the record. This
sketch gives them a channel — and takes a position on what that channel
is.

## The thesis: notes patch the record, never the prose

The engine's one non-negotiable is that the substrate is the source of
truth and prose is derived from it. Revision keeps that: a writer's
note is **compiled into a record edit**, the record is re-verified, and
the affected prose is **re-derived** — the draft is never edited in
place. A tone note ("colder") lands as the event's authorial `note`
(the same texture channel the Winter Count briefs carried); a
structural note ("she should discover the rot, not him") lands as an
event/overlay edit. Both are record edits; they differ only in how much
prose they invalidate. This is A3 doing revision: if the note is about
what happens, it belongs in the typed record; if it is about how it
feels, it belongs in a description — either way it goes *through* the
record, so the record never lies about the draft.

## Commitments

**RL1 — one extractor, revision-framed.** The revision pass is the
interview extractor (`extract_story_draft`) with `prior=` the current
record and `answers=` the writer's notes wrapped in a revision frame
("The author has read the generated draft and wants these changes —
update the record to carry them; change nothing else."). No new LLM
surface; the one extraction machine serves brief → record, answers →
record, and now notes → record.

**RL2 — a pure diff decides the blast radius.** `record_diff(old,
new)` (offline, tested) classifies every difference:

- *scene-scoped* — an existing event's `summary`, `note`, `who`,
  `roles`, `focalizer`, `establishes`, `learns`: only that event's
  scene is re-rendered.
- *bible-scoped* — anything the story bible or scene briefs all see:
  title, logline, telling/staging, characters, phases,
  `anti_recognitions`, any overlay field (marks, dynamics,
  throughlines, arguments, beats, …), an event's `when` / `mark` /
  `recognizer`, or any event added or removed: the whole draft is
  regenerated. Reframing the story reframes every scene; pretending
  otherwise would splice stale context.

The policy is an explicit table in code, not a heuristic. A diff that
comes back empty is surfaced honestly ("your notes produced no record
change — say what should be different in the story, not the prose"),
not silently swallowed.

**RL3 — the structured draft is a session artifact.** `generate`
persists `result_to_payload` (per-scene `tau_d` / `event_id` / prose —
the same artifact the convergence loop already splices) as
`scenes.json`; `draft.md` is always *assembled from it*. Scene-scoped
revision re-renders the target scenes via the repair seam
(`repair_scene`, the writer's note as the corrective directive, the
fresh record compiled underneath), splices them back, reassembles. A
session whose draft predates `scenes.json` falls back to full
regeneration.

**RL4 — re-verify before re-render.** The revised record passes
`blocking_gaps` + `compile_story` + `verify_compiled` before any prose
is spent — a note that breaks the structure is a finding for the
writer, not a broken draft.

**RL5 — the cost surface shows the blast radius.** Before confirming:
"2 scene re-render(s)" vs "bible-scoped change (`dynamics`) — full
regeneration, 17 scenes." The writer sees what a structural note costs
before paying it. Any regeneration invalidates `evaluation.json`.

**RL6 — offline spine.** The diff, the scope policy, the splice, and
the session bookkeeping are pure and pinned; the extractor and the
renderer are injected. (Same AC6 discipline as the CLI.)

## Non-goals

- No automatic re-evaluation after revision — the writer decides when
  to spend the blind read (`evaluate` is one command away and the
  next-step hint says so).
- No prose-level patching, ever — a writer who wants to hand-polish
  prose exports the draft; the engine's revision channel is the record.
  (Round-tripping hand-edited prose back into the record is the
  compile-from-text problem — out of scope, named.)
- No note classification UI — the extractor decides where a note
  lands; the diff shows the writer what it decided before anything is
  spent.

## Open questions

- Scene-scoped re-renders splice into neighbors written against the
  *old* record; the story-so-far synopses come from the new record, but
  seam prose (a transition referencing a changed detail) can go stale.
  Accepted for now — the blind evaluate catches real drift; if seams
  prove noisy, widen scope to adjacent scenes.
- Should repeated scene-scoped revisions of the same scene accumulate
  the notes in the event's `note` field, or replace? Current answer:
  the extractor owns the record; whatever it writes is the record.
  Revisit against real sessions.
