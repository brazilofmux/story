# story

A self-correcting, multi-dialect **story engine**: it generates a draft to a
chosen structural theory, reads its own prose back **blind**, scores how
faithfully the draft carries the intended structure, and repairs the places
where it drifted — across four different theories of story, on one shared
substrate.

This is a research prototype and design notebook, not a product. But the core
loop works, end to end, and the repository is organized as an editorial
archive: design sketches accumulate, superseded work stays visible, and the
reasoning-over-time is preserved.

## What it does

The engine is a small compiler with a neutral middle and pluggable front/back:

1. **A neutral substrate.** Event-primary, tri-temporal (story-time, discourse-
   time, authored-time), branch-aware. It computes per-agent knowledge by fold
   (who knows what, when) and represents ambiguity as first-class branch
   structure rather than reader confusion. The substrate is the single source
   of truth; everything else is a lens over it.

2. **Plural dialect overlays.** Four theories of story sit above the substrate,
   each in its own vocabulary, none privileged:
   - **Aristotelian** — peripeteia, anagnorisis, the pathos-centre, recognition.
   - **Dramatica** — the full Grand Argument Story theory: four throughlines,
     the eight essential dynamics, and the complete Table of Story Elements
     (4 Classes → 16 Types → 64 Variations → the 256-cell / 64-element bottom).
   - **Save the Cat** — the fifteen-beat sheet, A/B strands.
   - **Dramatic** — the lean parent dialect: one argument, Hero/Obstacle/Helper,
     stakes.

3. **A self-correcting generation loop.** The generator imports *zero* dialect
   code — it defines only a neutral seam each dialect plugs into. The loop:
   - **generate** a verified substrate → first-draft prose, in the dialect's frame;
   - **evaluate** by decompiling the prose **blind** (the reader is given the
     genre, never the answer key) → a typed reading → a fidelity score;
   - **repair** each drift by re-rendering the scene that carries it;
   - **converge** by splicing repairs back and re-scoring the whole draft.

It also **verifies** an encoded story against its own substrate — surfacing
where a story's claimed structure isn't actually supported by its events. (That
check recently caught the project's own Dramatica encodings misciting their
bottom-level elements, and we corrected them against the real chart — the
system flagging where the corpus was lying to itself.)

## Coverage, honestly

Support is uniform at the core and uneven at the edges — by design ("widen,
don't perfect"):

| | Aristotelian | Dramatica | Save the Cat | Dramatic |
|---|---|---|---|---|
| generate · evaluate · repair | ✅ | ✅ | ✅ | ✅ |
| converge (iterate to a fidelity ceiling) | ✅ | ✅\* | ✅\* | ✅\* |
| author by interview (structural homework) | ✅ | ✅ | ✅ | ✅ |
| compile plain text → substrate | ✅ | – | – | – |

\* The convergence loop is dialect-agnostic; all four dialects' evaluate +
repair-planner compose into it (integration-tested offline). The *live*
recovery has been demonstrated on Aristotelian so far (Malfi, 89% → 100% after
an injected regression).

The interview front-end now elicits and gap-checks all four dialects' structural
homework (each overlay mirrors its dialect verifier's vocabulary — Save-the-Cat's
fifteen beats and genre, Dramatica's four throughlines and eight dynamics,
Dramatic's arguments and stakes). What still lands for Aristotelian only is the
plain-text *compiler* — turning that record into the verified substrate; the
other three are verified by their existing encodings, and the TOML→overlay
compiler for them is the remaining, named seam.

So the true claim: **four story theories, each able to generate a draft, read
it back blind, repair the drift, iterate to a fidelity ceiling, and be authored
by interview** — with the plain-text compiler proven on one so far.

## What to expect (and what not to)

- **It works on stories expressed in its terms** — authored into a substrate,
  or ones it generated. There is not yet a "paste an arbitrary screenplay and
  get an analysis" path.
- **Originals, not just classics.** Two original tragedies (*The Vantage Light*;
  *Sworn*, told in strict reverse chronology) were authored as substrates the
  model had never seen as finished works, then generated and scored at 100%
  blind structural fidelity. The reverse-told one is the sharpest result: the
  substrate's order overrode the model's forward-causality instinct, and a
  blind reader independently read the prose as reverse-told.
- **The self-grading caveat is named, not hidden.** Every fidelity number is
  graded by the same model family that generated the prose. A genuine
  cross-family check is future work; the score means "this model reads this
  draft as structurally faithful," no more.
- **Some texts are out of scope by design.** The engine commits to factual
  commitment, so deliberately ambiguity-load-bearing works (Borges, late James,
  *The Turn of the Screw*) are outside the supported forms on purpose.

## Status

Working prototype, closed-corpus encodings, large test surface:

- **Four dialects**, one dialect-agnostic generator + repair seam.
- **105 design sketches** across the substrate, the four dialects, identity,
  focalization, inference, lowering/verification, the generation and
  self-correction layer, and the ambiguity-honest substrate; status and open
  questions tracked per sketch. Current state: [`design/state-of-play-19.md`](design/state-of-play-19.md).
- **~1,248 tests** across 33 test files (standard-library core plus
  venv-backed tests for the LLM-in-the-loop reader/evaluator surfaces).
- **Generated draft artifacts** under `prototype/*_first_draft.md` — Oedipus,
  Malfi, Rocky (from two different dialects), Macbeth (Save the Cat), and the
  originals (Vantage, Sworn, Quarter) — the evidence the loop runs.
- **Survey** of prior narrative theories and computational story systems in
  `research/`.

## Quickstart

```sh
cd prototype
# Standard-library core (no dependencies):
PYTHONPATH=. python3 tests/test_substrate.py
PYTHONPATH=. python3 tests/test_dramatica_template.py
PYTHONPATH=. python3 tests/test_verification.py

# The generation / evaluation / repair layer needs the venv (anthropic, pydantic):
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
PYTHONPATH=. .venv/bin/python3 tests/test_save_the_cat_evaluator.py

# Live demos require an ANTHROPIC_API_KEY; --dry-run prints the prompt only:
PYTHONPATH=. .venv/bin/python3 -m demos.demo_generate_oedipus --dry-run
```

## Repository layout

- [`design/`](design/) — architectural sketches (`{topic}-sketch-NN.md`),
  self-contained per topic; superseded sketches kept as historical record.
  Start at [`design/README.md`](design/README.md) and the latest
  `state-of-play-NN`.
- [`prototype/`](prototype/) — Python 3.12 reference implementation, written as
  an executable specification (explicit dataclasses, no framework dependencies
  in the core). Module catalog in [`prototype/README.md`](prototype/README.md).
- [`research/`](research/) — surveys of narrative theories (`theories/`) and
  computational story systems (`systems/`).
- [`AGENTS.md`](AGENTS.md), [`GEMINI.md`](GEMINI.md) — agent-facing guidance.

## Conventions

- **Design first** — non-trivial change gets a sketch in `design/` before code.
- **Sketch immutability** — superseded sketches stay, marked and linked.
- **Python is a specification language** — clarity and portability over
  cleverness; the engine may be ported later.
- **Tests are plain `assert`** with a minimal runner; test names pin the sketch
  commitment they protect.
- **Report the honest number** — evaluate blind; when a score drops, say so;
  name limitations rather than papering over them.

## License

MIT — see [`LICENSE`](LICENSE). Copyright (c) 2026 Stephen Dennis.

On what this is and why it's released open: [`WARNING.md`](WARNING.md).

The author is [@brazilofmux](https://github.com/brazilofmux). The LLM
collaborator on most sessions is Claude (model and session noted in commit
co-authorship).
