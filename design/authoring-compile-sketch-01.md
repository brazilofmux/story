# Authoring compile — sketch 01 (closing the loop: a second dialect compiles to substrate)

**Status:** active; landed (Save-the-Cat overlay compiler, 14 authoring tests, live end-to-end)
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

## What's next on this thread

- **Dramatic** then **Dramatica** overlay compilers — same shape, harder
  overlays (arguments/throughlines/stakes; storyform → element quads). Dramatica
  is the showcase and the largest mapping.
- The STC overlay does not yet capture **archetype assignments** or explicit
  **strands** from the interview (the verifier notes their absence as advisory).
  A deeper STC interview pass could elicit them; low priority.
