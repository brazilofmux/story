# Authoring propose mode — sketch 01 (directions, in plain language)

**Status:** active; **landed** 2026-07-30 — all five commitments
implemented (`cmd_propose` + `PROPOSE_AXES` in
`story_engine/tools/story.py`; seed consumption in the interview's
first extraction); 6 offline pins in `tests/test_story_cli.py`; live
proposal run pending an `ANTHROPIC_API_KEY` session.
**Date:** 2026-07-30
**Extends:** [authoring-cli-sketch-01](authoring-cli-sketch-01.md) (the
session), [authoring-interview-sketch-02](authoring-interview-sketch-02.md)
(the extractor and gap rules).
**Frames:** the July 2026 assessment: the step that makes "Dramatica,
accessible" true for someone who has never read the theory is an engine
that *proposes* — "this could end in failure she's at peace with, or
success that costs her everything; which is your story?" — rather than
only interrogating.

## The gap this closes

The interview asks the writer to fill the structural homework. That is
right once a direction exists — but at the blank page the load-bearing
choices (how it ends, who changes, what the argument is) are exactly
the ones a writer without the theory doesn't know they're making. Today
the engine's first move is a quiz; this sketch gives it a first move
that is an offer.

## The thesis: a proposal is pre-written author answers

No new record path, no per-dialect proposal compiler. A direction has
two faces:

- the **pitch** — 2–3 sentences in plain story language, no dialect
  jargon; this is all the writer must read to choose;
- the **structural seed** — the same direction written as concrete
  author answers in the dialect's terms (the ending axes, who changes,
  the argument's resolution, the genre/midpoint polarity — whatever
  that dialect's load-bearing axes are).

The writer picks a pitch; the seed is fed to the standard extraction as
`answers` on the interview's first round. From there the existing
machine takes over — the gap rules interrogate the seed exactly as they
would a writer's own words, and everything the seed under-specifies
becomes the interview's next questions. One extraction machine serves
brief → record, answers → record, notes → record (revision), and now
seed → record.

## Commitments

**P1 — propose is the blank-page move.** `story propose <dir>` is
allowed only before the interview has produced a record. After that,
direction changes are `revise`'s job (notes through the record), not a
re-roll. The next-step hint offers `propose` only when it is legal.

**P2 — one typed call, genuinely different directions.** A single
structured-output call returns 2–3 directions. The prompt requires them
to differ on the dialect's *load-bearing axes* — an explicit per-dialect
axis list (data, not vibes): Dramatica's Outcome × Judgment × Resolve;
Aristotelian's plot kind and who carries recognition vs suffering;
Save-the-Cat's genre and Midpoint/All-is-Lost polarity; Dramatic's
resolution direction. Three pitches that all end in triumph is a
failed proposal, not a choice.

**P3 — the pitch stays clean.** The pitch may not use dialect
vocabulary (no "throughline", "signpost", "beat sheet", "anagnorisis");
the seed carries all of it. The writer can ask to see the seeds
(`--show-structure`), but never has to.

**P4 — the choice is provenance.** The chosen direction (pitch + seed
+ when) is stored in the session and consumed by the first interview
extraction; it stays in the session record afterward, so a later reader
can see which offered direction the story grew from.

**P5 — offline spine.** Choice flow, seed storage, the blank-page
gate, and the interview's seed consumption are pinned with fakes; the
proposal call is the one injected edge.

## Non-goals

- No proposal-time compilation or scoring of the directions — the seed
  is interrogated by the gap rules like any answers; a seed that
  under-commits simply yields interview questions, which is the system
  working.
- No re-proposal after the record exists; no mixing of two directions
  ("the writer picks one"). A writer who wants a hybrid says so in the
  interview — plain language into the same extractor.

## Open questions

- Should the pitch-cleanliness rule (P3) be enforced by a check
  (reject a proposal whose pitch contains dialect vocabulary) or by
  prompt alone? Starting with prompt + a visible wordlist in the tests'
  fake data; add the check if live proposals leak jargon.
- Number of directions: fixed 3, or writer-configurable? Starting
  fixed at 3 (two feels like a coin flip, four like a menu).
