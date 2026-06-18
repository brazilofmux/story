# State of play — sketch 19

**Status:** superseded by [state-of-play-20](state-of-play-20.md)
**Date:** 2026-06-18
**Supersedes:** [state-of-play-18](state-of-play-18.md)

SoP-18 marked the four-dialect *generation* milestone and listed four
deferred depth-moves. This refresh marks what the next session built: two of
those moves landed, and the headline is no longer "four dialects generate" but
**four dialects generate, evaluate, AND repair — on one dialect-agnostic
engine — and the substrate now represents ambiguity honestly instead of
forcing a binary the story refuses.** Four commits since SoP-18
(`9614bfb`→`1bf354a`), all on `main`.

## Headline — two load-bearing additions

### 1. The ambiguity-honest substrate (the dramatica-precision-limit pass)

SoP-18's deferred move #4 is done. A Dramatica Dynamic Story Point can now
hold a **dual value** — `AmbiguousChoice` / `Dual({failure, success},
leans=…)` — when the story genuinely spans both poles and refuses the binary
the formalism demands. The integrity rule is the whole point:

- A **dual** axis scores `preserved` if the blind read lands **any** spanned
  pole (for a genuinely-dual story, either pole is faithful).
- A **single-pole** axis stays **strict**, byte-identical to before.

Ambiguity is **author-declared per axis** — it never loosens a binary axis. A
tragic `good→bad` Judgment flip is still caught. Rocky's Outcome was rewritten
`Dual({failure, success}, leans=failure)`; `canonical_ending` collapses over
the pole product to the contested "personal-triumph / triumph".

**Live-confirmed (OQ-AMB-1):** 11 blind reads of the Rocky draft scattered
9× `success` / 2× `failure` — both poles in-span — and **every read scored
preserved** while the binary Judgment control held all 11. The run-to-run flip
SoP-18 reported as instability is now read as the real ambiguity it is. The
honest twist: the reader *leans the opposite pole from the authored literal*
(success, not failure), because it reads Rocky's "go the distance" as the
goal — so under the old strict schema this faithful reading would have scored
DRIFT on 9 of 11 runs. The dual is load-bearing in both directions.
(Design: [ambiguity-honest-substrate-sketch-01](ambiguity-honest-substrate-sketch-01.md).)

### 2. Full evaluate + repair parity — all four dialects

SoP-18's deferred move #2. The coverage table was ragged; it is now uniform:

| Dialect | gen | eval | repair | conv | front |
|---|---|---|---|---|---|
| Aristotelian | ✅ | ✅ | ✅ | ✅ | ✅ |
| Dramatica | ✅ | ✅ | ✅ | · | · |
| Save-the-Cat | ✅ | ✅ | ✅ | · | · |
| Dramatic | ✅ | ✅ | ✅ | · | · |

Every dialect now generates, evaluates, AND repairs. Each new evaluator is a
`decompile_X`/`compare_to_Y` peer that reads **blind** (given the dialect's
FORM, never the answer key) plus a `plan_repairs` that localizes only what maps
cleanly to a substrate event and reports the rest. **Zero new generator or
rendering code** — the dialect-agnostic seam held; repair reuses
`draft_repair.repair_scene(adapter=...)`.

- **Save-the-Cat** (`save_the_cat_evaluator.py` + `_repair.py`): the crispest
  target — the fifteen named beats. Live **18/18 (100%) blind** on Macbeth;
  all beats located in canonical order, protagonist + B-story preserved. A
  lost beat localizes to the substrate event authored to carry it
  (`beat_event_ids`); the four unmapped slots honestly produce no directive.
- **Dramatic** (`dramatic_evaluator.py` + `_repair.py`): the lean parent —
  softer by nature (no beat sheet). Two honest tiers: CRISP name-level
  (Hero / Obstacle / Helper), the argument's resolution on the dialect's own
  four-value axis (affirm/negate/complicate/unresolved — already admits a
  middle, no forcing), and FUZZY token-overlap for the claim and stakes,
  **labelled `FUZZY` in the finding**. Live **6/6 (100%) blind** on Rocky.
  Only the argument resolution (sealed at the ending) is localizable.

(Design: [dialect-parity-sketch-01](dialect-parity-sketch-01.md).)

## The integrity thread (still the important part)

Each decision this session made the claims weaker and truer:

- **Cross-model evaluation was reconsidered and DROPPED as a near-term move**
  (memory `cross-model-eval-deferred`). SoP-18 called it "the single biggest
  credibility upgrade." Stephen's correction: a same-family Haiku+Opus vote is
  *manufactured* — averaging a weaker reader into a stronger one is noise, not
  rigor; a real cross-family check (Codex/Gemini/Opus) needs multi-API wiring
  not yet on the table. So the self-grading circularity is now a **named,
  honest limitation**, not something fake-fixed. Every fidelity number this
  session (18/18, 6/6, the 11 ambiguity reads) is opus reading opus-generated
  prose — and says so.
- **Fuzzy matches are labelled fuzzy.** The Dramatic claim/stakes dimensions
  are token-overlap, not name-level; the finding's note says `FUZZY` so a soft
  match cannot masquerade as a crisp one.
- **Repair declines what it cannot localize.** StC's four unmapped beats and
  every dialect's diffuse dimensions (order, function identity, throughline
  coverage, stakes) are reported, not forced onto a scene.
- **Score weighting disclosed.** StC's score is coverage-dominated (15 of 18
  dims) — a coverage measure, not a craft measure; the Dramatic score is a
  6-dim spine check with two fuzzy dims — a weaker instrument. Both stated.

## What is built — delta from sketch-18

### New core modules
- `dramatica_template.py` — `AmbiguousChoice` + `Dual()`; `DynamicStoryPoint`
  accepts a dual `choice` with `.poles`/`.leans`/`.is_dual`; `canonical_ending`
  collapses over the pole product.
- `dramatica_evaluator.py` — pole-set membership scoring (dual = either pole
  faithful; binary = strict).
- `save_the_cat_evaluator.py` + `save_the_cat_repair.py`.
- `dramatic_evaluator.py` + `dramatic_repair.py`.

### New demos / artifacts
- `demos/demo_evaluate_rocky.py` (OQ-AMB-1 live), `demo_evaluate_macbeth_stc.py`,
  `demo_evaluate_rocky_dramatic.py`. Rocky's encoding now declares the dual
  Outcome in place.

### Test surface
**1239 tests green** (was 1207 at SoP-18): +9 ambiguity (template/evaluator),
+12 Save-the-Cat (evaluator/repair), +11 Dramatic (evaluator/repair). No
regressions; Rocky substrate verification re-ran APPROVED under the dual.

## What's next (deferred, none urgent)

The remaining grid debt is now small and **uniform** across the three
non-Aristotelian dialects:

1. **Convergence demos.** `draft_convergence.converge` is dependency-injected
   and dialect-agnostic; StC / Dramatica / Dramatic wire in with no new core
   code — but none has a *demonstrated* live convergence (only Aristotelian /
   Malfi). Needs a draft that actually drops something to recover; a 100%
   first draft gives the loop nothing to do.
2. **Front-ends.** `.story.toml` authoring exists only for the Aristotelian
   path (`authoring.py`). StC / Dramatica / Dramatic surfaces are a larger,
   separate build.
3. **Dramatica completeness review** — DONE (2026-06-18,
   [dramatica-template-sketch-02](dramatica-template-sketch-02.md), commit
   `a06e0e8`). Verdict: complete on the hard structure; the gap was the
   dynamics — sketch-01 modeled SIX, the canonical storyform needs EIGHT.
   Added Driver (action/decision) + Problem-Solving Style (linear/holistic),
   authored across the 7 real encodings, with PSS held `Dual` where the binary
   isn't honest (Ackroyd, Rashomon). Still NOT modeled (correctly deferred):
   Journeys/PSR, and the six other OS plot appreciations (Requirements,
   Forewarnings, Costs, Dividends, Prerequisites, Preconditions) — the next
   Dramatica depth target if plot-level fidelity is ever wanted.
4. **The standing self-grading circularity** — named, not fixed (see above).
   Revisit only with multi-API wiring or a model-agnostic structural check.

Banked research track (unchanged from SoP-16/17): S6P-OQ1, OQ-MALFI-1B,
OQ-MALFI-4, OQ-AP7 — all await forcing sites. New ambiguity OQs: OQ-AMB-2
(dual Limit — the verifier still classifies one pole), OQ-AMB-3 (ambiguity
below the dialect).

## Context-economy discipline (cold-start continuity)

- **The substrate is the neutral source of truth; the frame is only the lens.**
  Four dialects, one generator that imports no dialect, one repair that reuses
  the dialect-agnostic re-render. Adding eval/repair to a dialect = a blind
  `decompile_X`/`compare_to_Y` peer + a `plan_repairs` that localizes only
  clean substrate-event maps. Never grade a dialect through another's lens.
- **The substrate may hold a more general state than any one dialect's binary.**
  Forcing the binary is the error; collapse to a pole only when the story does,
  and when an axis is dual, SAY SO in the report. Binary axes stay strict so
  the score still means something.
- **Evaluate blind; report the honest number; label the soft ones fuzzy.**
- **Name limitations you can't yet fix** (self-grading circularity) rather than
  fake-fixing them.

### What a cold-start Claude should read first
1. `design/README.md` — active sketches (stale; read files).
2. This doc (`design/state-of-play-19.md`).
3. `design/state-of-play-18.md` — the four-dialect generation milestone.
4. `design/ambiguity-honest-substrate-sketch-01.md` + `dialect-parity-sketch-01.md`
   — this session's two pieces.
5. `prototype/story_engine/core/draft_generator.py` — the generator + the
   `DialectFrame` seam.
6. The four `*_evaluator.py` + `*_repair.py` peers — the self-correcting loop
   per dialect; `save_the_cat_evaluator.py` is the cleanest worked example.
7. Memory: `cross-model-eval-deferred`, `dramatica-precision-limit`,
   `project-goal-generation-tool`, `commit-directly-to-main`.
8. `git log --oneline 1773a05..HEAD` — this session's four commits.
