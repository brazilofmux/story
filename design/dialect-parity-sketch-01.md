# Dialect parity — sketch 01 (Save-the-Cat AND Dramatic evaluate + repair; all four dialects reach gen·eval·repair)

**Status:** landed; StC + Dramatic evaluate + repair built; 18/18 (Macbeth StC) and 6/6 (Rocky Dramatic) blind; +23 offline tests (1239 green)
**Date:** 2026-06-18
**Supersedes:** nothing (new topic)
**Extends:** the evaluator/repair pattern set by `draft_evaluator.py`+`draft_repair.py` (Aristotelian) and `dramatica_evaluator.py`+`dramatica_repair.py` (Dramatica). No prior commitment retracted.
**Frames:** [state-of-play-18](state-of-play-18.md) "what's next" #2 (dialect parity); the coverage table there.
**Related:** `save_the_cat_evaluator.py`, `save_the_cat_repair.py`, `demos/demo_evaluate_macbeth_stc.py`, `story_engine/encodings/macbeth_save_the_cat.py` (the proving encoding), `macbeth_stc_first_draft.md` (the draft scored).
**Superseded by:** nothing yet

## Purpose

SoP-18's coverage table was honestly uneven by design ("widen, don't
perfect"): four dialects generate, but only Aristotelian and Dramatica could
*evaluate* and *repair*. This sketch closes that gap for **Save-the-Cat** —
bringing it to the same generate · evaluate · repair coverage Dramatica has.

StC is the cleanest dialect to evaluate. Where Dramatica's dynamics flicker
(the Outcome axis; see [ambiguity-honest-substrate-sketch-01](ambiguity-honest-substrate-sketch-01.md))
and the Aristotelian categories are interpretive, Save-the-Cat asserts every
story hits the SAME fifteen named beats in order. That is a crisp, nameable
fidelity target — beat coverage IS the structure.

## What was built

### `save_the_cat_evaluator.py` (decompile + compare)

Same two-stage shape as the peers:

1. `decompile_stc(prose) → StcReading` — BLIND. The reader is given the FORM
   (the fifteen canonical beat names) but never the answer key (which
   substrate event the author placed at each beat). Naming the form is fair —
   every StC story has those fifteen beats by definition; naming the fillings
   would lead the read. It reports the beats it can locate **in prose order**,
   the protagonist, the B story, the midpoint shape, the All-Is-Lost, and
   whether the Final Image mirrors the Opening.
2. `compare_to_sheet(reading, sheet) → StcFidelityReport` — pure Python,
   offline. Scores: **beat coverage** (one finding per authored slot —
   preserved/lost), **beat order** (did the located beats appear in
   non-decreasing canonical sequence?), **protagonist** identity, **B-story**
   presence. Beat-name resolution distinguishes look-alikes ("Break Into Two"
   vs "Break Into Three", "Opening Image" vs "Final Image") via a
   distinguishing-token guard, so a fuzzy match can't collapse them.

### `save_the_cat_repair.py` (plan_repairs)

A lost beat is the **most cleanly localizable drift in the corpus**: each beat
is authored to a substrate event (`sheet.beat_event_ids[slot]`), so a lost
beat re-renders exactly the scene meant to carry it, with a directive naming
the beat, its canonical purpose, and what fills it in this story. Re-rendering
reuses `draft_repair.repair_scene(adapter=StcFrame(...))` — the generator is
dialect-agnostic, so no new rendering code.

The same discipline the peers keep: **diffuse dimensions are not forced onto a
scene.** `beat_order` (a property of the whole sequence), `protagonist`, and
`b_story` are reported, not localized. And **honesty about the unmappable**:
four of Macbeth's fifteen slots (Opening Image, Theme Stated, B Story, Dark
Night) carry no `beat_event_ids` entry, so a loss there cannot be localized
and produces no directive — the repairer does not pretend to fix what it
cannot place.

## Evidence

- **Live: 18/18 (100%) blind** on `macbeth_stc_first_draft.md` (opus-4-6,
  high). All fifteen beats located in canonical order (1→15), protagonist
  Macbeth, marriage B-story present. The decompiler independently caught the
  Midpoint false-victory and the Opening/Final-Image inversion — structure the
  prose genuinely carries. (One live read; the score is high enough that
  instability characterization wasn't the question — coverage was.)
- **Offline: +12 tests** (`test_save_the_cat_evaluator` 7, `test_save_the_cat_repair`
  5) pinning beat coverage, order-drift detection, look-alike name
  resolution, protagonist/B-story drift, and the repair localization +
  diffuse-skip + unmappable-skip + dedup rules. Full sweep **1228 green** (was
  1216).

## The honest caveats

- **The 18/18 is one model family grading itself** — the standing self-grading
  circularity (see memory `cross-model-eval-deferred`). Named, not fixed: a
  same-family multi-vote is manufactured, and a real cross-family check is not
  wired. The number means "opus reads opus-generated prose as a faithful beat
  sheet," no more.
- **Beat coverage dominates the score** (15 of 18 dimensions). That is
  defensible for a beat sheet — the beats ARE the structure — but it means a
  draft that hits every beat in order scores ~83% before protagonist/order/B
  are even considered. The score is a coverage measure, not a craft measure.
- **A 100% first-draft score gave the repair loop nothing to do here.** Repair
  is proven by its unit tests (localization, dedup, diffuse-skip), not by a
  live recovery the way Malfi's Aristotelian convergence was. A live StC
  repair/convergence demo awaits a draft that actually drops a beat.

## Dramatic — the lean parent (added same session)

`dramatic_evaluator.py` + `dramatic_repair.py` bring the FOURTH dialect to the
same coverage. As predicted, the Dramatic target is SOFTER — there is no beat
sheet to count, only an argument carried by functions. So the evaluator scores
in two honest tiers:

- **Crisp, name-level:** Hero, Obstacle, Helper(s) — who plays each function.
- **The argument's resolution:** does the prose AFFIRM / NEGATE / COMPLICATE /
  leave UNRESOLVED its premise? The dialect's own four-value axis already
  admits a middle, so nothing is forced (contrast the dual-value work the
  Dramatica Outcome needed).
- **Fuzzy, content-level:** the claim and the stakes, scored by token overlap
  and **labelled `FUZZY` in the finding** so a soft match is never mistaken
  for a crisp one.

Repair localizes ONLY the argument resolution (sealed at the ending, like a
Dramatica ending-shape drift) to the final staged beat; the diffuse function /
claim / stakes drifts are reported, not forced.

**Evidence:** live **6/6 (100%) blind** on `rocky_dramatic_first_draft.md` —
Hero (Rocky), Obstacle (Apollo), both Helpers (Mickey + Adrian), `affirm`
resolution, and the fuzzy claim/stakes overlaps all preserved. +11 offline
tests (`test_dramatic_evaluator` 7, `test_dramatic_repair` 4). Same caveats as
StC apply, plus: with only 6 dimensions and two of them fuzzy, this score is a
**weaker instrument** than StC's fifteen-beat coverage — it confirms the
spine, not the texture.

## Open questions / what's next (the rest of the parity grid)

| Dialect | gen | eval | repair | conv | front |
|---|---|---|---|---|---|
| Aristotelian | ✅ | ✅ | ✅ | ✅ | ✅ |
| Dramatica | ✅ | ✅ | ✅ | · | · |
| **Save-the-Cat** | ✅ | **✅** | **✅** | · | · |
| **Dramatic** | ✅ | **✅** | **✅** | · | · |

Every dialect now generates, evaluates, and repairs. The empty cells are
uniform: convergence (DI-ready, demonstrated only for Aristotelian) and
front-ends (a separate build).

- **DP-OQ2 — convergence demos.** `draft_convergence.converge` is
  dependency-injected and dialect-agnostic; StC and Dramatica can both be
  wired into it with no new core code. Neither has a *demonstrated* live
  convergence (Aristotelian/Malfi is the only one). Wire + prove when a
  beat-dropping draft exists to recover.
- **DP-OQ3 — front-ends.** A `.story.toml` authoring surface exists only for
  the Aristotelian path (`authoring.py`). StC / Dramatica front-ends are a
  separate, larger build.

## The discipline this pins

Adding evaluate/repair to a dialect = a `decompile_X`/`compare_to_Y` peer
that reads BLIND (form, never answer key) + a `plan_repairs` that localizes
only what maps cleanly to a substrate event and reports the rest. No new
generator or rendering code — the seam is real. Score in the dialect's OWN
terms; never borrow another dialect's lens to grade.
