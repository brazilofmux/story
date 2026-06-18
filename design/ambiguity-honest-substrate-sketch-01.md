# Ambiguity-honest substrate — sketch 01 (dual DSP values; either pole is faithful)

**Status:** landed; offline-proven (1216 tests green) AND live-confirmed (OQ-AMB-1, 11 blind reads)
**Date:** 2026-06-18
**Supersedes:** nothing (new topic)
**Extends:** the Dramatica Template — adds `AmbiguousChoice` to the DSP value space; no prior commitment retracted.
**Frames:** [state-of-play-18](state-of-play-18.md) "what's next" #4 (the dramatica-precision-limit later-pass); memory `dramatica-precision-limit`, `project-goal-generation-tool`.
**Related:** commit `7165324` (blind evaluation — the observed run-to-run Outcome flip this sketch reframes); `prototype/story_engine/encodings/rocky_dramatica_complete.py` (the proving encoding); `dramatica_evaluator.py` (the honest-scoring change).
**Superseded by:** nothing yet

## Purpose

Let the substrate represent a Dynamic Story Point that **genuinely spans both
poles** instead of forcing the binary the formalism demands. This is the
later-pass SoP-18 deferred and the memory `dramatica-precision-limit`
prescribed: *pretend less, not more.*

The forcing case is Rocky's **Outcome**. The author's own encoding note
already conceded the contest is contested — "Apollo wins the scorecard but the
stunt has been contaminated… 'ain't gonna be no rematch.'" The blind Dramatica
evaluator flips `failure`↔`success` run-to-run (`7165324`) because the prose
renders the loss triumphantly, like the film, and **a reader genuinely
experiences Rocky as both a loss and a win at once.** The old schema scored
that flicker as *drift*. It was reading real ambiguity faithfully and being
punished for it. The binary was an artifact of the formalism, not a fact about
the story.

## What changed

### 1. The value space — `AmbiguousChoice` (`dramatica_template.py`)

A `DynamicStoryPoint.choice` is normally a single pole string (unchanged). It
may now also be an `AmbiguousChoice(poles, leans)`:

- `poles` — the ≥2 axis poles the value spans (each validated against the
  axis's pole set; a 1-pole "ambiguous" is a contradiction and raises).
- `leans` — an OPTIONAL single representative pole, for the rare consumer that
  must pick one (display, generation framing). `''` = genuinely balanced.

`Dual({Outcome.FAILURE, Outcome.SUCCESS}, leans="failure")` is the ergonomic
constructor. Three new DSP accessors keep every consumer simple:
`dsp.is_dual`, `dsp.poles` (a single-pole DSP → a 1-set), `dsp.leans` (a single
pole always, for code that needs one string).

### 2. Honest scoring (`dramatica_evaluator.py`) — the load-bearing rule

`compare_to_storyform` now scores Outcome / Judgment / Resolve by **pole-set
membership**, not string equality:

> A **single-pole** axis is **strict** (the binary case, byte-identical to
> before). A **dual** axis reads `preserved` if the blind read lands **any
> spanned pole** — because for a genuinely dual story either pole is faithful.

The integrity guard, stated plainly: **ambiguity is declared per-axis by the
author; it never loosens a binary axis.** Making Outcome dual does NOT make
Judgment forgiving — a tragic `good→bad` Judgment flip is still drift, still
caught (the test `test_binary_judgment_stays_strict_under_dual_outcome` pins
exactly this). This is the difference between *reading ambiguity* and *hiding
drift*, and it is the whole reason the move is honest rather than a fudge.

The fidelity finding **discloses** the duality (`authored="failure|success"`,
note "authored DUAL; either pole is faithful") rather than burying it behind
the lean. A reader of the report sees that the axis was authored ambiguous.

### 3. `canonical_ending` — contested endings

Computed over the cartesian product of the spanned poles. Rocky's
`{Failure, Success} × Good` collapses to **"personal-triumph / triumph"** — a
triumph whichever way Rocky is read; only the scoreboard is contested. When a
dual product lands a single cell it stays single; the binary path is unchanged.

### 4. Generation framing (`dramatica_generation.py`)

The bible now frames a dual axis as *genuinely contested* — "Outcome =
genuinely BOTH FAILURE and SUCCESS — this axis is CONTESTED, not resolved to
one pole… Render the ambiguity; do not collapse it" — so the prose can carry
the both-ness rather than being pushed to a pole. (Reader-model serialization
and repair directives are dual-aware too; both fall back to the lean as a
representative string, so no string-consumer broke.)

## Evidence

- `test_dual_outcome_either_pole_is_faithful` — a `success` read AND a
  `failure` read of Rocky both score `preserved`. The documented run-to-run
  flip is now read as the real ambiguity it is, not a fidelity loss.
- `test_binary_judgment_stays_strict_under_dual_outcome` — the control: the
  binary axis still catches a real collapse. Dual ≠ blanket forgiveness.
- Template: dual validation, `poles`/`leans`/`is_dual`, contested
  `canonical_ending`, and the binary path proven byte-identical.
- Full sweep **1216 tests green** (was 1207 at SoP-18; +7 template, +2
  evaluator, 2 existing assertions updated to the dual truth). Rocky's
  substrate verification re-ran APPROVED — the Outcome=Failure trajectory the
  substrate supports is still confirmed; `failure` is simply no longer the
  *whole* truth.
- `demos/demo_evaluate_rocky.py` — live OQ-AMB-1 confirmation (see below): 11
  blind reads, both poles surfaced, all preserved, binary control held.

## Live confirmation — OQ-AMB-1 (CLOSED, 2026-06-18)

`demos/demo_evaluate_rocky.py` decompiles `rocky_first_draft.md` BLIND
(genre-only note) and scores each read against the dual storyform.
**11 reads, claude-opus-4-6, effort=high**, across two independent batches:

| Outcome read | count | verdict | Judgment (control) |
|---|---|---|---|
| `success` | 9 | preserved (success ∈ span) | `good` — preserved, all 11 |
| `failure` | 2 | preserved (failure ∈ span) | `good` — preserved, all 11 |

Both poles surfaced; **every read scored `preserved`**; the binary Judgment
axis stayed stably good/preserved every run (the dual on Outcome did not
loosen it — the integrity guard held live, not just in tests). The run-to-run
flip the old schema scored as drift is now read as the real ambiguity it is.

**The honest asymmetry worth noting:** the blind reader leans `success` (9:2),
not `failure` — the *opposite* of the authored literal pole. The draft, as
written, lands Rocky's "go the distance" as an objective WIN; a blind reader
identifies *that* as the story goal and reads success, where the authored
storyform names Apollo's publicity stunt as the OS goal (which fails). So the
ambiguity has a deeper root: it is partly an ambiguity about **whose goal is
the story goal.** Under the OLD strict schema (authored single pole =
`failure`) this faithful triumphant reading would have scored the Outcome axis
as DRIFT on 9 of 11 runs — the dual is load-bearing in *both* directions, not
only when the reader flips.

## Open questions (first-class)
- **OQ-AMB-2 — dual Limit (TimeLock ∧ OptionLock).** The memory's *other*
  canonical example. The substrate now admits it (`Dual({TIMELOCK,
  OPTIONLOCK})` validates), but the **Limit verifier**
  (`verifier_helpers.classify_arc_limit_shape*`) still classifies against a
  single declared pole. A genuinely-dual Limit (a clock AND dwindling options)
  would need the verifier to accept either shape as consistent. No corpus
  encoding forces it yet — bank it until one does (probe-surfaced findings
  re-confirm; author-predicted ones often don't).
- **OQ-AMB-3 — should ambiguity live deeper than the dialect?** Outcome /
  Limit / Judgment are *Dramatica* concepts; this sketch makes the Dramatica
  overlay honest. The substrate event/coupling the DSP *reads from* could carry
  the ambiguity natively, with every dialect collapsing it per its own lens.
  That is a larger architecture move; only worth it if a second dialect needs
  the same ambiguity over the same substrate fact.

## The discipline this pins

The substrate may hold a **more general state than any one dialect's binary**;
forcing the binary is the error. Collapse to a pole only when the story
actually does — and when an axis is dual, **say so in the report**. The honest
8–9/9 of SoP-18 was the symptom; this is the cure that keeps the cure honest:
the binary axes stay strict, so the score still means something.
