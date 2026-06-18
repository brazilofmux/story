# State of play — sketch 18

**Status:** active
**Date:** 2026-06-18
**Supersedes:** [state-of-play-17](state-of-play-17.md)

The big swing. SoP-17 closed the last research loop (sketch-07 / OQ-MALFI-3)
and recommended pivoting to **generation**. This refresh marks what that
pivot became: the project crossed from "a research engine that analyses
masterpieces" to a **working, self-correcting, multi-dialect story
generator** — and the founding "substrate IR + plural dialect overlays"
thesis is now *demonstrated*, not asserted. Sixteen commits since SoP-17
(`845bf8d`→`f4bda0a`), all on `main`.

## Headline — four load-bearing claims

### 1. The generation pipeline exists end to end — and self-corrects

The compiler back-end is no longer a single Oedipus draft. It is a loop:

- **generate** (`draft_generator.py`) — a verified substrate → first-draft
  prose, scene by scene in sjuzhet order, framed by the dialect overlay.
- **evaluate** (`draft_evaluator.py`, terminus #2) — decompile the prose
  **blind** (the reader is given the genre, never the structure) → a typed
  reading → a name/qualifier-level fidelity score against the substrate.
- **repair** (`draft_repair.py`) — localize each drift to the substrate
  beat that carries it → re-render that scene with a corrective directive.
- **converge** (`draft_convergence.py`) — splice the repair back, re-score
  the WHOLE draft, iterate to a fidelity ceiling (dependency-injected, so
  dialect-agnostic).

Proven: Malfi convergence recovered an injected regression 89%→100%
(`7644d84`); the Aristotelian originals scored 100% blind.

### 2. It GENERATES originals — it is not a Shakespeare-renderer

Two original tragedies (authored as verified substrates, never seen by the
model as finished works) went through the full pipeline:

- **The Vantage Light** (`37b3aee`) — a lighthouse keeper whose pride is
  the instrument of the wreck; pathos-split (the daughter) from recognizer
  (the father). 100% blind structural fidelity.
- **Sworn** (`46a7844`) — told in **strict reverse** chronological order.
  The decisive experiment: the model's deepest instinct is forward
  causality, and the substrate's reverse sjuzhet **overrode it** — a blind
  reader independently read the prose as `telling='reverse'`. Structure
  beat priors. (The Aristotelian fidelity held 100% blind here too.)

### 3. A human can drive it — the front-end exists

`authoring.py` + `demos/author_story.py`: a writer authors a story in a
plain-text `.story.toml` (no Python) — characters with roles, events with
a `when` and a `summary`, structural marks, phases, telling order — and it
compiles to the exact verified substrate + Aristotelian overlay the engine
consumes, runs the self-verifier for feedback, and generates. Proven with
**Quarter** (`stories/quarter.story.toml`), a new original authored in the
format: verified clean, 6/6 fidelity. The gap from "engine" to "tool
someone other than a programmer can use" is closed (Aristotelian only).

### 4. The generator is DIALECT-AGNOSTIC — four dialects, one engine

The founding thesis, demonstrated. `draft_generator.py` imports **zero**
dialect code; it defines only an abstract `DialectFrame` seam. Each dialect
ships a peer frame in its own module; **none is privileged** (the base
class holds no dialect logic). Four frames now generate:

| Frame | Module | Vocabulary | Density |
|---|---|---|---|
| `AristotelianFrame` | `aristotelian_generation.py` | peripeteia, anagnorisis, pathos-split | medium |
| `DramaticaFrame` | `dramatica_generation.py` | 4 throughlines, 16 signposts, 6 dynamics | **heaviest** |
| `StcFrame` | `save_the_cat_generation.py` | 15-beat sheet, A/B strands | medium |
| `DramaticFrame` | `dramatic_generation.py` | one argument, Hero/Obstacle/Helper, stakes | **leanest** |

The cleanest proof: the **same `rocky.py` substrate** renders from two
dialects — the maximalist Dramatica storyform (`1c78eb1`) and the minimal
three-actor Dramatic template (`f4bda0a`) — and they are genuinely
different drafts because the *frame* is the only thing that changed. The
substrate holds the facts; the overlay is the lens. The Aristotelian
generation path stayed **byte-identical** across all three adapter
additions — the seam is real, not coincidence.

(Dialect note: **Dramatic** is the general parent dialect — Story,
Argument, Throughline, Scene, Beat, Stakes, + a pluggable Template;
**Dramatica** is its heaviest Template, extending it with the full Grand
Argument Story theory. The four frames span that whole density range.)

## The integrity thread (this is the important part)

The session held to a "no cheating" discipline, and it earned its keep —
each fix below made the claims *weaker and truer*:

- **The "blind" evaluator was being led** (`7165324`). The demos passed the
  *generation* note (which names the specific structure) to the
  *evaluator*. Fixed: blind-by-default genre-only `GENRE_NOTE`; warned in
  the docstrings; 8 call sites stripped. Re-ran honest: Aristotelian held
  100% blind (Vantage, Sworn — the claims were sound); **Dramatica dropped
  to an unstable 8–9/9** — the Outcome axis (lose-the-contest-but-triumph)
  flips run-to-run, because the draft frames the loss triumphantly like the
  film. Reported, not buried.
- **Positional heuristics killed** (`14b749b`, and again for Save-the-Cat).
  Dramatica acts and StC beats are now AUTHORED event mappings, not guessed
  from scene position; the fallback DISCLOSES itself in the bible ("act
  boundaries are APPROXIMATE") rather than passing a guess off as fact.
- **Dramatica over-claims precision** — accepted, not chased (see
  `memory: dramatica-precision-limit`). Some axes (TimeLock vs OptionLock,
  even Outcome×Judgment) are legitimately ambiguous; the substrate IR can
  hold a more general state than any one dialect's binary, and forcing the
  binary is the error. The Aristotelian categories proved more
  readable/stable than Dramatica's dynamics.
- **Breadth found bugs depth couldn't**: pushing structurally-different
  substrates through the generator surfaced two latent bugs — int-valued
  Prop args (Rocky) and list-valued participant roles (Macbeth) — both
  fixed. The "widen, don't perfect" strategy paid for itself.

## What is built — delta from sketch-17

### New core modules (the generation + plural-dialect layer)

- `draft_generator.py` — generator + the abstract `DialectFrame` seam +
  `render_scene_prose` (single-scene re-render, used by repair) +
  `result_to_payload` (structured-draft JSON for convergence).
- `draft_evaluator.py` — blind decompile (`DecompiledStructure`, incl.
  `telling_order`) + `compare_to_mythos` (pure-Python fidelity).
- `draft_repair.py` — `plan_repairs` + `repair_scene` (adapter-aware).
- `draft_convergence.py` — `converge` (injected evaluate/plan/repair fns).
- `authoring.py` — the `.story.toml` compiler + `verify_compiled`.
- The four dialect frames: `aristotelian_generation.py`,
  `dramatica_generation.py`, `save_the_cat_generation.py`,
  `dramatic_generation.py` (+ `dramatica_evaluator.py`,
  `dramatica_repair.py` for the Dramatica stack).

### Coverage by dialect (honestly uneven — by design)

- **Aristotelian** — generate · evaluate · repair · converge · **front-end**.
- **Dramatica** — generate · evaluate · repair (no front-end / convergence demo).
- **Save-the-Cat** — generate only.
- **Dramatic** — generate only.

That is the "widen, don't perfect" shape: breadth at the generation layer,
depth concentrated where it was earned first.

### New encodings / artifacts

- Originals: `vantage_light(.py/_aristotelian.py)`, `sworn(.py/_aristotelian.py)`.
- Front-end sample: `stories/quarter.story.toml`.
- Generation overlays: `rocky_dramatica_complete.ACT_EVENT_IDS`,
  `macbeth_save_the_cat.BEAT_EVENT_IDS`, `rocky_dramatic_three_actor.py`.
- Drafts (the evidence): `oedipus_first_draft.md`, `malfi_first_draft.md`,
  `malfi_converged.md` / `malfi_recovery.md`, `vantage_first_draft.md`,
  `sworn_first_draft.md`, `quarter_first_draft.md`, `rocky_first_draft.md`,
  `macbeth_stc_first_draft.md`, `rocky_dramatic_first_draft.md`.

### Test surface

Full core sweep **1207 tests green** (was ~1069 at SoP-15). The generation
+ plural-dialect layer added offline tests for the evaluator, repair,
convergence, authoring, and all four dialect frames; the Aristotelian
research suite (test_aristotelian 232) is unchanged.

## What's next (all DEPTH moves — deferred, none urgent)

The thesis is demonstrated; what remains is hardening and breadth, in
rough order of value:

1. **Kill the self-grading circularity.** Every fidelity number is graded
   by the same model family that generated. The honest fix: evaluate with a
   DIFFERENT model, run each read a few times to characterise instability.
   Stephen's call (2026-06-18): fine to defer — models improve; a 2–3 model
   vote is a clean future drop-in, not a now-problem.
2. **Evaluators / repair for the three newer dialects** (StC, Dramatic, and
   convergence/front-end for Dramatica) — bring them toward Aristotelian's
   full-stack parity, when a reason arises.
3. **More originals / story types** through the front-end; a Dramatica or
   StC authoring surface.
4. **The ambiguity-honest substrate** (the dramatica-precision-limit
   later-pass): let a dialect represent "both / unresolved" rather than
   forcing a binary the story refuses.

Research track (banked, unchanged from SoP-16/17): S6P-OQ1 (main-level
anagnorisis_qualifier), OQ-MALFI-1B, OQ-MALFI-4, OQ-AP7 — all await
forcing sites; the dialect ledger is A1–A23, untouched this session.

## Context-economy discipline (cold-start continuity)

- **The substrate is the neutral source of truth; the frame is only the
  lens.** Four dialects, one generator that imports no dialect. When adding
  a fifth, write a `DialectFrame` peer in its own module; do not touch the
  generator. Keep the Aristotelian dry-run byte-identical (the regression
  guard).
- **Author mappings, don't guess them; disclose fallbacks.** Scene→act /
  scene→beat mappings are authored in the encoding; a positional fallback
  must say so in the bible.
- **Evaluate blind.** The decompile note is GENRE-ONLY, never the structure
  (it defaults to `GENRE_NOTE`). Report the honest number even when it
  drops; prefer a true 8/9 to a led 9/9.
- **Probe-surfaced findings re-confirm; author-predicted ones often don't**
  (unchanged from SoP-16).

### What a cold-start Claude should read first

1. `design/README.md` — active sketches (stale past probe-sketch-03; read
   files).
2. This doc (`design/state-of-play-18.md`) — current state.
3. `design/state-of-play-17.md` — supersedes-link; the last research loop +
   the generation pivot recommendation.
4. `prototype/story_engine/core/draft_generator.py` — the generator + the
   `DialectFrame` seam (the architectural heart of the new layer).
5. The four frames (`*_generation.py`) — how each dialect surfaces itself;
   `dramatica_generation.py` is the richest worked example.
6. `prototype/story_engine/core/draft_evaluator.py` + `draft_repair.py` +
   `draft_convergence.py` — the self-correcting loop.
7. `prototype/story_engine/core/authoring.py` + `stories/quarter.story.toml`
   — the human front-end.
8. `prototype/sworn_first_draft.md` — the reverse-told original (the
   structure-beats-priors proof); `rocky_first_draft.md` +
   `rocky_dramatic_first_draft.md` — the same substrate from two dialects.
9. Memory: `project-goal-generation-tool`, `dramatica-precision-limit`,
   `commit-directly-to-main`.
10. `git log --oneline 4ab2b62..HEAD` — the sixteen commits of this arc.
