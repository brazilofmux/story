# Authoring front-end — sketch 02 (generalizing the interview past Aristotelian)

**Status:** active; landed (spine + extraction, four dialects, 30 tests)
**Date:** 2026-06-18
**Supersedes:** nothing — **extends** [authoring-interview-sketch-01](authoring-interview-sketch-01.md)
**Frames:** [state-of-play-20](state-of-play-20.md) "what's next" #2; memory `dramatica-precision-limit`.

## The idea

sketch-01 landed the interview Aristotelian-first: the deterministic gap-spine
phrased the substrate's demands and the Aristotelian overlay's homework
(peripeteia, anagnorisis, hamartia, pathos) as questions. This pass widens it
**the way the rest of the stack widened** — each dialect's overlay gets its own
gap rules and its own extraction schema, while the load-bearing skeleton stays
one shared, dialect-agnostic thing.

## The split that makes it clean

The interview's gaps fall into two kinds, and only one was ever Aristotelian:

- **The skeleton** (`_skeleton_gaps`, dialect-agnostic) — what `compile_story`
  needs to build entities · fabula · sjuzhet · phases *at all*: a title,
  characters with ids, events with a story-time `when`, participants that
  resolve, a valid telling order, every beat in exactly one phase. This is the
  same for every dialect — it is the **substrate's** demand, not any overlay's.
- **The homework** (a per-dialect overlay) — the commitments a dialect's
  *self-verifier* wants but tolerates missing. This is what was hard-wired to
  Aristotelian and is now pluggable.

A `Dialect` record carries the overlay's `overlay_gaps(doc) -> [Gap]` (the
deterministic spine half) plus its `system_prompt` and `build_schema` (the LLM
extraction half). A `DIALECTS` registry maps the four names; `interview_gaps`,
`blocking_gaps`, `structural_gaps`, `is_compilable`, `next_questions`,
`run_interview`, and `extract_story_draft` all take `dialect="aristotelian"`
(unchanged default — every sketch-01 test still passes byte-for-byte).

```
interview_gaps(doc, dialect)  =  _skeleton_gaps(doc)  +  DIALECTS[dialect].overlay_gaps(doc)
                                  └─ shared, blocking  └─ per-dialect, structural
```

## The four overlays (each mirrors its dialect verifier)

- **Aristotelian** — `recognizer_unknown` (blocking: the compiler refuses it);
  then structural: `no_peripeteia`, `no_anagnorisis`, `anag_no_recognizer`,
  `no_hero`, `no_pathos`, `hero_no_hamartia`. (Unchanged behavior, lifted out.)
- **Save-the-Cat** — `stc_no_theme`, `stc_no_genre` / `stc_unknown_genre` (the
  ten genres), `stc_no_protagonist` (the role labels), and beat coverage against
  the canonical fifteen: `stc_unknown_beat` and `stc_unfilled_beats` for the
  six load-bearing beats (Catalyst → Finale; the atmospheric beats are polish).
- **Dramatica** — `dram_missing_throughlines` (the four), `dram_*_domain` (the
  four distinct domains, with collision + completeness checks),
  `dram_missing_dynamics` / `dram_bad_dynamic` (the eight axes and their poles),
  `dram_no_goal`, `dram_no_consequence`. A dynamic given **both** poles is a
  genuinely-dual axis and is honored, not flagged — the ambiguity-honest
  substrate (`dramatica-precision-limit`): forcing a binary the story doesn't
  commit is exactly the over-claim we refuse.
- **Dramatic** — `dramatic_no_argument` / `dramatic_arg_no_premise` /
  `dramatic_bad_resolution` (affirm | negate | complicate | unresolved),
  `dramatic_no_main_character`, `dramatic_throughline_no_stakes`.

Each dialect's `extract_story_draft` builds a pydantic schema with the shared
skeleton fields plus the overlay's fields (STC's `theme_statement` / `genre` /
per-event `beat`; Dramatica's `throughlines` / `dynamics` / goal+consequence;
Dramatic's `arguments` / `throughlines`-with-`stakes`), and a system prompt that
names that dialect's vocabulary.

## Scope / honesty (what landed vs. what is named)

- **The deterministic spine is the load-bearing, tested part** — 30 offline
  tests (up from 16): a complete doc in each dialect has zero gaps; each
  overlay's omissions surface with the right codes; the **skeleton blocking gaps
  are proven identical across all four dialects**; an unknown dialect raises.
- **`compile_story` still lands the substrate skeleton + the Aristotelian
  overlay only.** The other three dialects' homework is now elicited and
  gap-checked, and their records are verified by the existing encodings; a
  TOML→non-Aristotelian-overlay compiler is the remaining seam (README coverage
  grid: "compile plain text → substrate" is the Aristotelian-only row now;
  "author by interview" is ✅ across all four).
- **The extraction is LLM-shaped and self-graded**, the same named caveat. The
  spine is where the correctness lives, and it is model-free.

## Why this is the right shape

The substrate was always the neutral source of truth and every dialect a lens.
The interview now reflects that: one shared set of questions the *substrate*
demands, and four interchangeable sets the *dialects* demand — the same
"widen, don't perfect" seam as the generator/evaluator/repair/convergence
stack, turned around to face the author.
