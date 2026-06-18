# State of play — sketch 20

**Status:** active
**Date:** 2026-06-18
**Supersedes:** [state-of-play-19](state-of-play-19.md)

SoP-19 marked full-stack four-dialect parity + the ambiguity-honest substrate.
This refresh marks the arc that followed: **Dramatica was made genuinely
complete (and the corpus drift that exposed was fixed), convergence reached
parity, a conversational front-end landed, and the project went public** —
MIT-licensed, README rewritten, and the dark-choice WARNING answered in the
open. Eighteen commits since SoP-19 (`a06e0e8`→`993febb`), all on `main`.

## Headline — four load-bearing additions

### 1. Dramatica is now actually complete — and the corpus it exposed got fixed

Two real gaps closed, with the project's discipline intact:

- **The canonical EIGHT dynamics.** sketch-01's Q5 modeled *six* DSP axes;
  Dramatica's storyform needs eight. Added **Driver** (action/decision) and
  **Problem-Solving Style** (linear/holistic), authored across the 7 real
  encodings — with PSS held `Dual` where the binary isn't honest (Ackroyd,
  Rashomon), tying the completeness work to the ambiguity-honest substrate.
- **The full Table of Story Elements, level 4.** The 256-cell bottom level is
  64 distinct elements (the "chess set") recurring across the table. Stephen
  read the entire chart off the structure-chart PDF (the copy/paste scrambles;
  decoded via the fixed 2-line quad layout and cross-checked — typed and pasted
  Situation agreed exactly). `CANONICAL_ELEMENT_QUADS` now holds all 64
  Variation → element-quad placements; invariants pinned (256 cells, each of 64
  elements ×4, each Type = one character-element category).
- **The verifier earned its keep, twice.** Shipping the canonical placements
  surfaced that **every one of the 15 corpus-used element quads was
  non-canonical** — the prior session had authored level-4 without the chart,
  defaulting Problem quads to Motivation elements. The drift was fixed **story
  by story**: all 24 throughline Problem picks across the six encodings
  re-authored as genuine thematic re-reads within the correct canonical quad
  (Stephen approving each), e.g. Lady Macbeth's IC Problem Control→Uncontrolled,
  Elizabeth's MC Evaluation→Re-evaluation. All six now co-load with **0
  deviations, 0 conflicts**. (Design: [dramatica-template-sketch-02](dramatica-template-sketch-02.md).)

### 2. Convergence parity — all four dialects compose into the loop

`draft_convergence.converge` was dialect-agnostic but only the Aristotelian
path had its real evaluate+plan+repair wired through it. `test_dialect_convergence`
now proves Save-the-Cat, Dramatic, and Dramatica each compose end to end (real
`compare_*` report + real `plan_repairs` via a sjuzhet-closure `plan_fn`),
driving the loop to its fidelity ceiling and repairing the right substrate
event. So generate · evaluate · repair · **converge** is uniform across the
four. (Live recovery still demonstrated on Aristotelian only — Malfi 89%→100%.)

### 3. The conversational front-end — the substrate's homework as the interview

`authoring.py` compiles a `.story.toml`; the new front-end makes producing that
dict a **conversation**. The architecture keeps the load-bearing part
model-free:

- **`interview_gaps(doc)` — the spine** (pure, deterministic, standard-library,
  16 tests): the authoring dict's gaps, phrased as questions, with severity —
  *blocking* (what `compile_story` refuses: no `when`, an unphased beat, an
  undeclared participant) and *structural* (the Aristotelian homework: no
  peripeteia, an anagnorisis with no recognizer, a hero with no hamartia). The
  verifier turned to face the author.
- **`extract_story_draft` — the LLM half** (pydantic, lazily imported): natural
  brief + answers → the authoring dict.
- **`run_interview` — the multi-round loop** (pure controller, injected
  extract/answer fns, mirrors `converge`): extract → ask the gaps → answer →
  re-extract until 'complete' / 'stalled' / author-finished / max-rounds.
- **Live, end to end:** a lighthouse paragraph became a complete authoring
  record (0 gaps), compiled clean (0 verifier observations), and generated an
  opening scene that *dramatizes its own hamartia* — no `.story.toml`, no hand-
  authoring. Aristotelian-first. (Design: [authoring-interview-sketch-01](authoring-interview-sketch-01.md).)

### 4. The project went public

- **MIT `LICENSE`** (the repo had none) + a **rewritten README** — the prior
  one predated the entire generation era (said "three dialects", "822 tests",
  analysis-only). Now leads with generate→evaluate→repair→converge across four
  dialects, the honest coverage matrix, and the named caveats.
- **`WARNING.md` — the dark choice, answered.** Releasing a narrative-
  structure engine open is a dual-use decision; the document makes the case
  (commons over monopoly; literacy as the only durable defense) and was
  **calibrated to the repo's own restraint**: the *promise* claimed as the
  accountability loop (verifiable), the *threat* relocated from the prototype
  to the trajectory ("the first cheap, repeatable step toward it — I can see
  the road"). Scarier because checkable.

## The integrity thread (still the point)

- **The verifier caught the corpus lying to itself.** Level-4 drift was
  invisible and ad-hoc until the canonical table made it checkable; then it was
  fixed honestly (per-throughline re-authoring, not a mechanical relabel).
- **The front-end turns rigor into help.** A blank form demands the author
  already know the structure; the interview asks for exactly the commitments
  the substrate needs — the homework-forcing discipline becomes the UX.
- **The WARNING under-claims on purpose.** Every concrete claim is one a
  skeptic can confirm in the repo; the dread comes from the slope, not the
  snapshot. The license is the proof, not the prose.
- **The self-grading circularity is still named, not fixed** (memory
  `cross-model-eval-deferred`) — the extraction and every fidelity number are
  self-graded; a real cross-family check remains future work.

## Coverage grid

| | Aristotelian | Dramatica | Save-the-Cat | Dramatic |
|---|---|---|---|---|
| generate · evaluate · repair | ✅ | ✅ | ✅ | ✅ |
| converge | ✅ | ✅\* | ✅\* | ✅\* |
| interview (structural homework) | ✅ | ✅ | ✅ | ✅ |
| compile (TOML → substrate) | ✅ | – | – | – |

\* converge composed + integration-tested for all four; live recovery
demonstrated on Aristotelian.

## What is built — delta from sketch-19

- `dramatica_template.py`: `Driver` + `ProblemSolvingStyle` (the canonical 8);
  `CANONICAL_ELEMENTS` (the 64) + `CANONICAL_ELEMENT_QUADS` (all 64 placements);
  hardened `register_element_quad` + `verify_element_quads` (consistency +
  canonical-deviation).
- All 7 dramatica-complete encodings: 8 DSPs + canonical element quads + the 24
  re-authored Problem picks.
- `tests/test_dialect_convergence.py` (convergence parity, 3 tests).
- `story_engine/core/authoring_interview.py` + `tests/test_authoring_interview.py`
  (16) + `demos/author_by_interview.py`.
- `LICENSE`, rewritten `README.md`, `WARNING.md`.

### Test surface
**1267 tests green** across 35 files (was 1207 at SoP-18 / ~1216 at SoP-19's
baseline). No regressions through the Dramatica recompletion or the front-end.

## What's next (deferred, none urgent)

1. **Interview, deeper homework** — the who-knows-what-when knowledge
   discipline (the substrate's real teeth) is only lightly probed in v1; the
   next gap-rule pass checks that an asserted "X knows Y" has an establishing
   event.
2. ~~**Generalize the interview past Aristotelian**~~ — **LANDED.** Each dialect
   now has its own structural-gap overlay + extraction schema; the skeleton
   stays one shared, dialect-agnostic thing (proven identical across all four).
   30 offline tests (was 16); `compile_story` still Aristotelian-only (named
   seam). Design: [authoring-interview-sketch-02](authoring-interview-sketch-02.md).
3. **Live convergence demos per dialect** — the offline composition is proven;
   three `demo_converge_*` mirrors of the Malfi one would close the live
   symmetry (lower value than 1–2).
4. **Cross-model evaluation** — still deferred and still right to defer; the
   cheap same-family vote is manufactured (memory `cross-model-eval-deferred`).
5. **Dramatica depth, if pressured** — Journeys / Plot-Sequence and the six
   other OS plot appreciations (Requirements, Forewarnings, Costs, Dividends,
   Prerequisites, Preconditions) remain unmodeled by design.

Banked research OQs (unchanged): OQ-AMB-2 (dual Limit verifier), OQ-AMB-3
(ambiguity below the dialect), and the SoP-16/17 forcing-site queue.

## Context-economy discipline (cold-start continuity)

- **The substrate is the neutral source of truth; everything else is a lens.**
  Four dialects, one generator/repair seam, one convergence controller, one
  authoring dict — all dialect-agnostic at the core.
- **Author canonical data from the source, not memory.** The level-4 drift came
  from authoring without the chart; the fix came from transcribing it. When a
  dialect over-claims a binary, hold it `Dual` (`dramatica-precision-limit`).
- **Evaluate blind; report the honest number; name what you can't fix.** True of
  the loop, the front-end's extraction, and the WARNING alike.

### What a cold-start Claude should read first
1. `design/README.md` (stale; read files) → this doc.
2. `design/state-of-play-19.md` and `-18.md` — the parity + generation arcs.
3. `design/dramatica-template-sketch-02.md` — the canonical eight + the full
   element table + the drift fix.
4. `design/authoring-interview-sketch-01.md` + `authoring_interview.py` — the
   front-end (the spine is the worked example of "homework as questions").
5. `prototype/story_engine/core/draft_generator.py` + the four `*_evaluator.py`
   / `*_repair.py` peers + `draft_convergence.py` — the self-correcting loop.
6. `WARNING.md`, `README.md` — what shipped and why it shipped open.
7. Memory: `cross-model-eval-deferred`, `dramatica-precision-limit`,
   `project-goal-generation-tool`, `commit-directly-to-main`.
8. `git log --oneline a06e0e8..HEAD` — this arc's eighteen commits.
