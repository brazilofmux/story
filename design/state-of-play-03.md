# State of play — sketch 03

**Status:** active
**Date:** 2026-04-18
**Supersedes:** [state-of-play-02](state-of-play-02.md)

A cold-start orientation doc, rewritten (per the sketch-02 / sketch-
01 discipline — "don't amend, write sketch-03 at the next milestone")
at the close of the scheduling-act-utterance arc. Five commits since
sketch-02 was written, consuming all five items in sketch-02's "What's
next" list:

- `d64a2ba` package-structure-sketch-01 + refactor (item 2).
- `42e67e4` skeleton-generator-sketch-01 + CLI tool (item 3).
- `dacefb5` *And Then There Were None* bootstrapped via generator
  (item 5 maybe-next).
- `86b4b03` scheduling-act-utterance-sketch-01 design (item 1).
- `c68d3ad` enabling-retraction-preservation-sketch-01 deferral
  (item 4).
- `5d81e02` scheduling-act-utterance-sketch-01 implementation
  (SC1–SC4; Rashomon bandit + samurai shift NOTED 0.5 → APPROVED
  0.5 end-to-end as sketch predicted).

Re-write this sketch (don't amend — write sketch-04) at the next
milestone. Stale state-of-play is worse than none.

---

## What is built

### The dialect stack (core machinery)

Now lives under `prototype/story_engine/core/` after the package
refactor (package-structure-sketch-01, `d64a2ba`). Modules:

- **substrate** (`core/substrate.py`) — typed facts, events,
  branches, descriptions. The "sink" dialect. Specified by
  substrate-sketch-05, descriptions-sketch-01, focalization-sketch-
  01, identity-and-realization-sketch-01, inference-model-sketch-01.
- **dramatic** (`core/dramatic.py`) — Throughlines, Characters,
  Scenes, Beats, Arguments, Stakes. Dialect-neutral upper surface;
  `StoryEncoding` + `StoryRelation` for multi-Story per multi-
  story-sketch-01.
- **dramatica-complete** (`core/dramatica_template.py`) —
  Dramatica's specific extension: DomainAssignments, DSPs on 6
  axes, Signposts, ThematicPicks, CharacterElementAssignments,
  Story_goal, Story_consequence. Specified by dramatica-template-
  sketch-01.
- **lowering** (`core/lowering.py`) — the cross-dialect binding
  record. Specified by lowering-record-sketch-01.
- **verification** (`core/verification.py`) — VerificationReview
  and StructuralAdvisory records. Orchestrated through encoding-
  specific `*_verification.py` files.
- **verifier_helpers** (`core/verifier_helpers.py`) — EK2 (action
  shape), AG1–AG6 (event agency), LT1–LT14 (DSP-limit pressure
  shape — sketches 01/02/03 of pressure-shape-taxonomy),
  **SC2** (LT8 scans `SCHEDULING_PREFIXES = frozenset({"scheduled_",
  "requested_"})` rather than hard-coding `"scheduled_"`), **SC3**
  (additive `scheduling_prefixes` output field on
  `classify_arc_limit_shape_strong`: dict mapping each matched
  prefix to the tuple of Props carrying it; existing
  `scheduling_signals` / `scheduling_count` flat-totals unchanged
  for sketch-02-era callers).

Package-refactor adjuncts also in `core/`: **proposal_walker**,
**reader_model_client**, **dramatic_reader_model_client**,
**save_the_cat** (the latter is dialect-layer machinery shared
across the Macbeth and Ackroyd Save-the-Cat wirings).

### The encodings

No new fully-verified encoding since sketch-02. Still the same
five works. The Rashomon verification module's two-testimony
verdict shift is the only measurement change:

1. **Oedipus** — DSP_limit=Optionlock. Unchanged.
2. **Macbeth** — DSP_limit=Optionlock. Unchanged.
3. **Ackroyd** — DSP_limit=Optionlock. Unchanged.
4. **Rocky** — DSP_limit=Timelock, APPROVED 1.00. Unchanged.
5. **Rashomon** — DSP_limit=Optionlock (frame) / Timelock (×4
   testimonies). **Bandit and samurai shifted NOTED 0.5 → APPROVED
   0.5 post-SC4** (the `requested_killing("tajomaru", "husband")`
   Prop on `E_t_wife_requests_killing` / `E_h_wife_requests_
   killing` now fires LT9 via the extended `SCHEDULING_PREFIXES`
   set). Wife and woodcutter unchanged at NOTED 0.5 — sketch-01
   explicitly scoped both out (OQ1 dual-party goading for
   woodcutter; OQ2 non-utterance action for wife).

**Sixth encoding bootstrapped (not yet in the verification corpus):**
**And Then There Were None** — 5-file skeleton authored
2026-04-18 via `story_engine.tools.skeleton` (`dacefb5`), the
first real use of the generator. Ten characters, no content
beyond Entity / Character binding. The substrate file's docstring
carries the rationale (first canonical multi-suspect whodunit;
ensemble cast stresses Dramatica-8 function assignment; discrete-
elimination Timelock — candidate probe target for a potential
`counted_*` / `enumerated_*` scheduling vocabulary extension),
anticipated DSP axis settings, MC/IC open-choice (conventional
Vera vs. subversive Wargrave), and probe expectations. The
verifier currently emits only a single
`skeleton:and_then_there_were_none` StructuralAdvisory — the
generator's SG4 contract.

**Non-corpus encodings at other dialect layers** (cold-start
pointer; these pre-date sketch-01 and are not counted as corpus
members):

- **Chinatown** — Dramatic-dialect-only (`chinatown_dramatic.py`,
  `chinatown_dramatica_complete.py`). First tragedy (Failure × Bad)
  in the dialect-level matrix. No substrate, no Lowerings, not in
  the verification-test corpus.
- **Pride and Prejudice** — Dramatic-dialect-only. Triumph
  (Success × Good) matrix slot at the dialect layer.
- **Turn of the Screw** — substrate-only stub from turn-of-the-
  screw-infeasibility-probe-sketch-01.

177 → **182 verification tests** (the +5 are SC2/SC3/SC4 pinning
tests; no LT12 test was removed — the two LT12-NOTED Rashomon
tests were reshaped in place to LT9-APPROVED). **586 standard
prototype tests pass** across 11 test modules; **40 venv-gated
tests pass** across the two Anthropic-SDK client modules. Skeleton-
generator's `test_skeleton.py` (8 tests) is part of the 586.

### The probe (cross-boundary reader-model)

`core/dramatic_reader_model_client.py` — no code change since
sketch-02. Four behavioral modes observed so far remain:

- **architectural-finding** (Rocky LT9 dissent; original Rashomon
  LT2 qualifications)
- **implementation-refinement** (probe qualifies a verdict's
  detail)
- **bar-raising** (probe endorses but proposes stricter check)
- **bar-raising-through-endorsement** (probe endorses a landed
  sketch AND proposes a sibling refinement — the post-LT12
  Rashomon pattern)

Rashomon probe JSON chain (durable artifacts; all at `prototype/`
root):

- `reader_model_rashomon_output.json` — original, pre-LT12; two
  architectural-finding qualifications that drove sketch-03's LT12.
- `reader_model_rashomon_post_lt12_output.json` — post-sketch-03
  (`25a56f4`); 5 commentaries endorse + 4 plant sibling
  refinements → four probe seeds. Three closed by scheduling-act-
  utterance-sketch-01 (bandit / wife / woodcutter); one closed by
  enabling-retraction-preservation-sketch-01 (samurai, deferral).
- **`reader_model_rashomon_post_sc4_output.json` (expected, not yet
  run)** — the third link in the chain, the scheduling-act arc's
  closing artifact. The implementation commit (`5d81e02`) names
  re-running the probe as the natural next step.

V5 = V6 distribution-identical on the four single-Story runs;
plateau confirmed empirically before the Substack piece
(unchanged).

### The article

`articles/2026-04-18-timelock-or-optionlock.md`, published 2026-
04-18 at https://unlikelyemphasis.substack.com/p/timelock-or-
optionlock-real-stories — unchanged since sketch-01. Section 8's
Rashomon hypothesis has now cycled probe → sketch-03 → probe →
sketch-01 (scheduling-act) → implementation → probe-pending.

### Infrastructure (new since sketch-02)

Two infrastructure sketches landed. Both were sketch-02 items; both
shipped same-day as their sketches.

- **Package structure** — `prototype/story_engine/{core,
  encodings,tools}/` plus sibling `prototype/tests/`,
  `prototype/demos/`. 72 flat `.py` files → 49 packaged modules +
  13 tests + 11 demos. Absolute imports only; no relative imports;
  no `sys.path` tricks. Run commands: `cd prototype && python3 -m
  tests.test_X` / `python3 -m demos.demo_X`. CWD-discoverable; no
  `pyproject.toml` yet. Probe JSON outputs stay at `prototype/`
  root. Specified by package-structure-sketch-01.
- **Skeleton generator** — `story_engine/tools/skeleton.py` +
  `skeleton_templates.py`. Invoked as `python3 -m
  story_engine.tools.skeleton --work-id W --title T --characters
  "id:Name,..."`. Writes the canonical 5-file dramatica-complete
  encoding stub. **Step 2 of the 5-step expert-system author
  flow** (start, *skeleton*, fill, walk/check, prose). Specified
  by skeleton-generator-sketch-01.

---

## What the probe has revealed (closed since sketch-02)

Both new-since-sketch-02 findings closed. Both closed same-day as
they were flagged.

- **Scheduling-act utterances (three post-LT12 testimonies)** →
  closed by scheduling-act-utterance-sketch-01 (design `86b4b03` →
  implementation `5d81e02`). SC2 extends `SCHEDULING_PREFIXES` to
  `{"scheduled_", "requested_"}`. SC3 adds the typed
  `scheduling_prefixes` output field. SC4 authors the Rashomon
  worked case (`requested_killing(tajomaru, husband)` Prop on
  `E_t_wife_requests_killing` + `E_h_wife_requests_killing`).
  Measured shifts: bandit and samurai NOTED 0.5 → APPROVED 0.5,
  matching sketch predictions end-to-end. Rocky / Macbeth /
  Oedipus / Ackroyd all confirmed unchanged. **Re-introduces
  substantive cross-testimony asymmetry** — distinct from the
  LT2-detector artifact that sketch-03's LT12 absorbed; the new
  asymmetry tracks which testimonies surface speech-act scheduling
  force as typed fact. OQ1 (`provoked_*`), OQ2
  (`situational_forcing`), OQ3 (`prophesied_*` bank for Oedipus
  oracle / Macbeth witches), OQ4 (per-prefix LT9 strength
  weighting) all remain open; scheduling-act-utterance-sketch-02
  writes when a probe or concrete use-case forces one of them.
- **Enabling-retraction preservation (samurai)** → closed by
  explicit deferral — enabling-retraction-preservation-sketch-01
  (`c68d3ad`). First deferral-as-sketch in the corpus. Four
  revisit criteria enumerated; none holds today. Baseline
  preservation already exists per sketch-03: `classify_arc_limit_
  shape_strong`'s `enabling_retractions` / `enabling_retraction_
  count` output fields, surfaced in the verifier comment. No
  code / test / substrate changes per EP1–EP4.

## What the probe has revealed (open, new since sketch-02)

**Nothing yet.** The post-SC4 Rashomon probe has not been run. Two
outcomes are structurally possible:

- **Endorsement across the board** — bandit / samurai endorsed at
  their new APPROVED 0.5 verdict; wife / woodcutter's continued
  NOTED 0.5 accepted under sketch-01's explicit scoping. The
  scheduling-act arc closes cleanly. No new sketch-forcing
  finding.
- **Qualification on the scoped-out testimonies** — the probe
  takes a position on OQ1 (`provoked_*`) or OQ2
  (`situational_forcing`) that the sketch deferred. This would be
  the first real bar-raising finding on the SC4-shifted surface
  and would motivate sketch-01's sketch-02.

Either outcome is informative. Running the probe is the cheapest
open task in the corpus.

---

## What's next (research)

In the order I'd work them:

1. **Post-SC4 Rashomon probe.** Closing artifact for the scheduling-
   act arc. Re-runs `demos/demo_dramatic_reader_model_rashomon.py`
   and commits `reader_model_rashomon_post_sc4_output.json`.
   Mechanical; cheap; completes the Rashomon JSON chain's third
   link.
2. **Decide:** close the scheduling-act arc, or act on probe
   qualification. If the probe endorses across the board, the arc
   closes and attention shifts to #3 or #4. If the probe dissents
   on OQ1/OQ2, scheduling-act-utterance-sketch-02 writes.
3. **And Then There Were None content.** Skeleton exists
   (`dacefb5`). First substantive fill would stress Dramatica-8
   function assignment against a 10-character cast, validate the
   `counted_*` / `enumerated_*` scheduling-vocabulary hypothesis
   from the bootstrap docstring, and exercise the full 5-step
   author flow end-to-end. Large task (~30–50 substrate events, 4
   throughlines, 10 character functions, ~15 scenes, Template
   records, Lowerings, verification replacement on the oedipus
   pattern). First forcing function for generator OQ3/OQ4/OQ5
   (function labels, MC/IC designation, Beat scaffolding).
4. **Chinatown / Pride and Prejudice substrate authoring.** Both
   exist at the Dramatic dialect layer only. Lifting either to
   substrate adds a Failure×Bad or Success×Good to the full-
   verification corpus. Structural question first: does the
   verification corpus aim for canonical-ending matrix coverage,
   or stay focused on LT/MN pressure-shape stress? Defer to user
   judgment before committing to the lift.
5. **Scheduling-act OQ1–OQ4.** Smaller sibling sketches for the
   open questions. Most natural after the post-SC4 probe lands, in
   case probe commentary steers which OQ to address first.
6. **Maybe-next (no commitment):**
   - The fourth Dramatica quad layer (Elements per Variation).
     Storage-cheap; probe-context expensive; not urgent.
   - Non-Dramatica Templates (Save-the-Cat is partly-done for
     Macbeth + Ackroyd; Freytag / Aristotelian / author-defined
     all admitted by architecture-sketch-02).
   - Turn of the Screw infeasibility follow-up — substrate file
     exists from the infeasibility probe; no active arc.
   - `pyproject.toml` / PyPI discoverability — package-structure-
     sketch-02 if CWD-discoverable stops being enough.

---

## Context-economy discipline (for cold-start continuity)

Rules unchanged from sketch-02. Recently validated:

- **Sketches before implementation.** scheduling-act-utterance-
  sketch-01 landed design-first (`86b4b03`), implementation-second
  (`5d81e02`), with sketch-predicted verdict shifts confirmed end-
  to-end. Discipline works.
- **Deferral as a sketch.** enabling-retraction-preservation-
  sketch-01 is the corpus's first deferral-as-sketch. Pattern: a
  finding is banked with explicit revisit criteria, not dropped,
  not built. Use when the finding is a separable topic with its
  own potential consumers.
- **State-of-play at milestone boundaries.** This doc. Re-write
  (not amend) sketch-04 at the next natural pause.
- **Probe output JSON files are durable artifacts.** The two-JSON
  Rashomon template holds: `reader_model_rashomon_output.json`
  pre-LT12, `reader_model_rashomon_post_lt12_output.json` post-
  sketch-03. The scheduling-act arc's closing `..._post_sc4_...`
  JSON is pending.
- **Commit messages are cross-session artifacts.** `d64a2ba`,
  `42e67e4`, `dacefb5`, `86b4b03`, `c68d3ad`, `5d81e02` all carry
  substantive dense records of their landings. Keep writing them.
- **Prefer Grep / Read-slice over full Read** when the target is
  known. Reserve full Read for unfamiliar files.
- **Spawn Explore agents aggressively** for research that will
  take 3+ queries. Agent context is separate; results come back
  compact.

### What a cold-start Claude should read first

If you're picking up this project without conversation memory:

1. `design/README.md` — active sketches per topic.
2. This doc (`design/state-of-play-03.md`) — current corpus +
   open findings.
3. `articles/2026-04-18-timelock-or-optionlock.md` — the paper,
   which contextualizes what the corpus is for.
4. `git log --oneline -30` — recent commits.
5. The most recently touched encoding's `*_verification.py` file
   (currently `rashomon_dramatica_complete_verification.py`).
6. The latest Rashomon probe JSON
   (`reader_model_rashomon_post_lt12_output.json` until the post-
   SC4 probe runs, at which point the `..._post_sc4_...` file
   becomes the latest).
