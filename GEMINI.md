# story — computational storytelling engine

See [`README.md`](README.md) for the full project overview. This
file carries the Gemini-facing summary.

## Project goal

A long-horizon research project to build a story-telling engine.
The narrow goal is to **force humans or LLMs to do their homework
on the structural layer of a story** — who knows what when, what
claim the story argues, whether the dialect-chosen shape actually
fits the substrate's events.

Research + design notebook + working Python prototype. Not a
product. Not seeking contributors.

## Architectural stack

The engine is a stack of upper dialects over a single substrate:

1. **Substrate** ([`design/substrate-sketch-05.md`](design/substrate-sketch-05.md)).
   Event-primary; tri-temporal — **τ_s** (story time), **τ_d**
   (discourse time), **τ_a** (authored time). Branch-aware.
   Per-agent knowledge projections by fold. Ambiguity as
   first-class branch structure, not reader-side misunderstanding.
2. **Dialects.** Three exist:
   - **Dramatic** ([`design/dramatic-sketch-01.md`](design/dramatic-sketch-01.md))
     — role-driven, parameterized. Arguments, Throughlines,
     Characters, Scenes, Beats, Stakes.
   - **Save the Cat** ([`design/save-the-cat-sketch-01.md`](design/save-the-cat-sketch-01.md)
     + [`design/save-the-cat-sketch-02.md`](design/save-the-cat-sketch-02.md))
     — beat-driven, prescriptive. 15 canonical beats, 10 genres,
     StcCharacter with canonical role labels.
   - **dramatica-complete** ([`design/dramatica-template-sketch-01.md`](design/dramatica-template-sketch-01.md))
     — the full Dramatica Grand Argument Story theory as a
     Template atop Dramatic. 64 character elements across 4
     dimensions, 16 Issue Quads.
3. **Lowering + verification.** Four coupling kinds
   (Realization, Characterization, Claim-moment,
   Claim-trajectory, Flavor) identified by design; three verifier
   primitives implement the middle three. Observations flow
   through the proposal queue — partner, never gate.
4. **Inference model** ([`design/inference-model-sketch-01.md`](design/inference-model-sketch-01.md)).
   Horn-clause rules, bounded depth, proof-carrying derivation.
   Composes with identity-substitution
   ([`design/identity-and-realization-sketch-01.md`](design/identity-and-realization-sketch-01.md))
   to handle anagnorisis cleanly.
5. **Reader-model probe** ([`design/reader-model-sketch-01.md`](design/reader-model-sketch-01.md)).
   Optional LLM-in-the-loop component reading the description
   surface and proposing reviews, answer proposals, and edit
   proposals. Substrate-native record types on input and output.
   Built against Claude Opus 4.6 via the Anthropic SDK.

## Load-bearing design choices

- **Grid-snap architecture.** Substrate carries structural facts;
  authors (or LLMs) carry affective / interpretive / tonal load
  via descriptions. If an attentive reader could reliably catch
  drift in prose, that content belongs in descriptions — not a
  typed projection. (Architecture commitment A3.)
- **Ambiguity-load-bearing texts are scoped out by design.** The
  engine requires factual commitment; Borges / late James / Kafka
  are outside supported story forms. Not a limitation — a
  position.

## Repository layout

- [`design/`](design/) — architectural sketches (`{topic}-sketch-NN.md`).
  Self-contained per topic. Superseded sketches kept as record.
- [`prototype/`](prototype/) — Python 3.12 reference implementation.
  Executable specification; favor explicit records and plain
  functions over Python-specific cleverness (the engine may be
  ported later).
- [`research/`](research/) — two parallel tracks:
  `theories/` (narrative theory surveys) and `systems/`
  (computational narrative system surveys).
- [`REVIEW.md`](REVIEW.md) — April 2026 editorial review; several
  items have since landed.

## Status (April 2026)

- **12 active design sketches**; all have status / date / open
  questions tracked.
- **Seven encoded stories** closing the Outcome × Judgment matrix:
  Oedipus Rex, Macbeth, *The Murder of Roger Ackroyd*, Rashomon,
  *Pride and Prejudice*, Rocky, Chinatown.
- **Three cross-boundary verifiers** at the dramatica-complete →
  substrate coupling. Post-EK2 characterization spectrum: APPROVED
  0.77 (Oedipus) / PARTIAL 0.69 (Macbeth) / PARTIAL 0.54 (Ackroyd)
  — the three-point spread measures encoding/taxonomy match
  honestly.
- **~510 tests** across 12 test files; full suite runs in under a
  second. Standard-library only except the reader-model probe.

## Running the prototype

Core (standard library only):

```sh
cd prototype
python3 demo.py                  # Oedipus Rex — irony + anagnorisis report
python3 demo_rashomon.py         # Rashomon — contested-branch matrices
python3 test_substrate.py        # 45 tests — substrate invariants
python3 test_verification.py     # 79 tests — verifier primitives + EK2
python3 test_save_the_cat.py     # 60 tests — STC dialect S1–S13
```

Reader-model probe (requires venv + `ANTHROPIC_API_KEY`):

```sh
.venv/bin/pip install -r requirements.txt
.venv/bin/python3 demo_reader_model.py --dry-run   # print prompt
.venv/bin/python3 demo_reader_model.py --walk      # interactive walker
```

## Development conventions

- **Design first.** Non-trivial architectural change gets a
  Markdown sketch in `design/` before code lands.
- **Sketch immutability.** Superseded sketches stay in place with
  `Status: superseded` + successor link.
- **Python as specification.** Explicit `@dataclass(frozen=True)`,
  tagged unions via `Union[KnowledgeEffect, WorldEffect]`, plain
  functions. No metaclasses, no decorators-as-mechanism, no
  complex generics.
- **Tests are plain `assert`.** No framework. Each test's
  docstring notes which sketch commitment it pins.
- **Editorial review, not toolchain.** No CI, no linters, no
  formatters. Quality control is at commit time.

## Commit and PR style

Short imperative subjects; body bullets explain the *why*.
Implementation commits often pair with a follow-on `README:`
commit documenting the finding. Claude-co-authored commits use:

```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

(matched to the actual collaboration).
