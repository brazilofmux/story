# Authoring compile — sketch 01 (closing the loop: dialects compile to substrate)

**Status:** active; landed (Save-the-Cat + Dramatic overlay compilers, 17 authoring tests, both live end-to-end)
**Date:** 2026-06-18
**Extends:** `authoring.py` (the `.story.toml` → substrate compiler) and
[authoring-interview-sketch-02](authoring-interview-sketch-02.md) (the per-dialect interview).
**Frames:** memory `project-goal-generation-tool` (generation-first end goal).

## The seam this closes

The interview was generalized to all four dialects (sketch-02), but
`compile_story` still only emitted the Aristotelian overlay. So a Save-the-Cat
or Dramatica brief could be *interviewed* to a complete, 0-gap record that then
had nowhere to go — the interview→compile→generate chain was Aristotelian-only.
This pass wires the **second** dialect end to end, proving the chain isn't
special to Aristotelian. Save-the-Cat first because its overlay is the simplest
(fifteen fixed beats + A/B strands + genre + role labels).

## The split: shared substrate, per-dialect overlay

`compile_story(doc, dialect="aristotelian")` now factors into:

- **`_build_substrate(doc) -> _Substrate`** — dialect-neutral. Entities, fabula
  (with the focalizer knowledge anchor), sjuzhet (telling order), descriptions,
  preplay. This is exactly what every `*_save_the_cat` / `*_dramatic` encoding
  shares with its base encoding (e.g. `macbeth.py`'s ENTITIES/FABULA/SJUZHET are
  reused across dialects), so the compile side reuses it verbatim too.
- **`_build_aristotelian_overlay(doc, sub) -> ArMythos`** — the existing logic,
  lifted out unchanged (phases, marks, recognizer, binding, anti-recognition).
  Byte-for-byte: all 10 prior authoring tests still pass.
- **`_build_stc_overlay(doc, sub) -> CompiledStcOverlay`** — new. Maps the
  authoring dict's STC fields onto the canonical `StcStory` + the beat / strand
  / character records the generator needs:
  - each event's canonical `beat` name → its slot (1–15), grouping events into
    `StcBeat`s; `page_actual` = the slot's canonical page-target (monotonic);
    `beat_event_ids` is the slot→event-id map the renderer reads;
  - character `role` → `StcCharacter.role_labels`;
  - one synthesized A-story strand, plus a theme-carrying B-story strand when a
    `theme_statement` is stated;
  - `genre` → `stc_genre_id` when it names one of the ten.
  Beats are **tolerated-missing**: an un-beated story still compiles (the STC
  verifier merely *notes* the unfilled slots — it never rejects, per its S6
  commitment).

`CompiledStory` gains `dialect` and a generic `overlay` field;
`verify_compiled` dispatches on dialect (Aristotelian `verify` vs.
`save_the_cat.verify`). Generation takes the STC overlay via `adapter=StcFrame(
StcStorySheet(...), sjuzhet)` — the same call the `demo_generate_macbeth_stc`
path uses — rather than `mythos=`.

## Live, end to end

A sparse boxing brief ("a washed-up boxer gets one unlikely title shot;
golden-fleece; dignity is earned in how you fight") was **interviewed** (JSON
mode — see below), **compiled** to a `StcStory` (8 events, 3 entities, 11
advisory verifier notes, 0 rejections), and **generated** an Opening Image scene
that dramatizes the beat's structural job: the faded fight poster, the world
before the story disturbs it, the missing letter on the gym sign — the
mirror-the-Final-Image setup Snyder's Opening Image is *for*.

## A transport note (extraction)

The structured-output grammar compiler (`messages.parse`) has a low
schema-complexity ceiling — only the smallest schema (Aristotelian) compiles
under it reliably; Save-the-Cat, Dramatica, and Dramatic all return "Schema is
too complex" / "Grammar compilation timed out". So those three extract via plain
**JSON mode** (ask for a JSON object, validate with the same pydantic schema in
Python), gated by a `constrained` flag on the `Dialect` record. No schema-size
limit, and the spine's validation is unchanged.

## Dramatic — the third dialect (landed)

Same split, a different overlay. `_build_dramatic_overlay` maps the dict onto
the canonical `Story` + `Argument` / `Throughline` / `Character` / `Stakes`
records. The key discovery: the Dramatic generator is **character-function-
driven** — `DramaticFrame` labels each event's participants Hero / Obstacle /
Helper and, when the Hero and Obstacle share a beat, tells the renderer to make
it a *confrontation* where the argument's two sides collide. It never reads
Scenes or Beats. So the load-bearing synthesis is the **function assignment**,
not a scene layer:

- the owner of the **main-character** throughline becomes the **Hero**, the
  **impact-character** owner the **Obstacle**, everyone else a **Helper**
  (fallback: the character's `role` word), under the **three-actor** template;
- arguments carry their `resolution_direction` (affirm/negate/complicate/
  unresolved); each throughline's `{at_risk, to_gain}` becomes a `Stakes`
  record; owners map to the dialect's sentinels (`the-situation`,
  `the-relationship`, `none`) when not a declared character.

No scene/beat layer is built — the Dramatic dialect ties scenes to events in a
separate lowering pass, and the generator doesn't need it. `verify_compiled`
dispatches to `dramatic.verify` (advisory-only). *Live:* a whistleblower brief
("a safety engineer finds the bridge is flawed; argument *speaking the truth is
worth any cost*, resolved COMPLICATE") was interviewed → compiled to a `Story`
(5 events, 2 entities, 2 advisory notes) → generated a Hero-vs-Obstacle review-
room confrontation that puts the argument on trial through the mentor/protégé
collision.

## What's next on this thread

- **Dramatica** overlay compiler — the last dialect and the largest mapping
  (storyform → four throughlines × domains, the eight dynamics, element quads).
  The showcase close.
- Neither the STC overlay (archetype assignments, explicit strands) nor the
  Dramatic overlay (scene/beat layer, argument_contributions) captures every
  field its verifier notes as advisory; the interview elicits the load-bearing
  ones and the rest surface as advisory notes. Deeper per-dialect interview
  passes could elicit them; low priority.
