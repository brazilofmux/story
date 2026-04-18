# story

A long-horizon research project to build a story-telling engine. The
narrow goal is to **force humans or LLMs to do their homework on the
structural layer of a story** — who knows what when, what claim the
story is arguing, whether the dialect-chosen shape (Dramatica's,
Save the Cat's, Aristotle's) actually fits the substrate's events.

This is a research and design notebook with a working Python
prototype. Not a product. Not seeking contributors. The repository is
organized as an editorial archive: sketches accumulate, old work
stays visible, and the design's reasoning-over-time is preserved.

## What the engine is, structurally

The engine is a stack of upper dialects over a single substrate, with
connective machinery between them.

- **Substrate.** Event-primary, tri-temporal (story-time τ_s,
  discourse-time τ_d, authored-time τ_a), branch-aware. Computes
  per-agent knowledge projections by fold. Represents ambiguity as
  first-class branch structure rather than reader-side
  misunderstanding. A small inference layer (Horn-clause rules,
  bounded depth, proof-carrying derivation) composes with
  identity-substitution to handle anagnorisis cleanly. Current
  statement: [`design/substrate-sketch-05.md`](design/substrate-sketch-05.md).
- **Dialects.** Author-facing vocabularies that sit above the
  substrate. Three exist today: **Dramatic** (role-driven,
  parameterized), **Save the Cat** (beat-driven, prescriptive), and
  the **dramatica-complete** Template atop Dramatic (the full
  Dramatica Grand Argument Story theory as theory data). Each has a
  self-verifier that speaks only that dialect's vocabulary.
- **Lowering and verification.** Cross-boundary machinery binding
  upper-dialect records to substrate facts. Four coupling kinds
  identified by design: **Realization** (upper made true by lower,
  carried by Lowering records), **Characterization** (upper
  classifies a substrate pattern), **Claim** (upper asserts
  substrate state at a moment or across a trajectory), **Flavor**
  (free-form metadata). Three verifier primitives implement the
  middle three. Observations flow through the proposal queue —
  partner, never gate.
- **Reader-model probe.** Optional LLM-in-the-loop component that
  reads the substrate's description surface and proposes reviews,
  answer proposals, and edit proposals. Substrate-native record
  types on both input and output; the substrate owns all state
  transitions. Built against Claude Opus 4.6 via the Anthropic SDK.

See [`design/README.md`](design/README.md) for the sketch list,
architectural frames, and open questions.

## Why this way

Two load-bearing design choices, named early so later decisions stay
coherent:

- **Grid-snap architecture.** The substrate grid-snaps structural
  facts (who kills whom, who knows what, what branches exist). The
  author (or an LLM) carries the affective / interpretive / tonal
  load via descriptions. If an attentive human or LLM reading the
  prose could reliably catch drift in some content, that content
  belongs in descriptions — not in a typed projection. This is
  commitment A3 in [`design/architecture-sketch-01.md`](design/architecture-sketch-01.md).
- **Ambiguity-load-bearing texts are a design decision, not a
  limitation.** The engine commits to factual commitment — Save the
  Cat and Dramatica both implicitly require it — so Borges, late
  James, and Kafka are outside the supported story forms *by
  design*. The system has an opinion about what constitutes
  well-formed story structure. See the Turn of the Screw
  infeasibility probe ([`design/turn-of-the-screw-infeasibility-probe-sketch-01.md`](design/turn-of-the-screw-infeasibility-probe-sketch-01.md)).

## Status

Working prototype, closed-corpus encodings, extensive test surface:

- **19 active design sketches** across substrate, dialects,
  identity, focalization, inference, lowering, verification,
  event-kind and pressure-shape taxonomies, and two cross-dialect
  comparisons. Status, supersession, and open questions tracked
  per sketch.
- **Seven encoded stories** exercising the substrate and dialects:
  *Oedipus Rex*, *Macbeth*, *The Murder of Roger Ackroyd*,
  *Rashomon*, *Pride and Prejudice*, *Rocky*, *Chinatown*. Together
  they close the canonical Outcome × Judgment matrix across all
  four corners (personal-tragedy ×3, triumph, personal-triumph,
  tragedy) and exercise every DSP axis direction at least once.
  Four have full substrate encodings (Oedipus, Macbeth, Ackroyd,
  Rocky); three are dialect-layer-only pending substrate
  authoring (P&P, Chinatown, Rashomon — Rashomon exercises its
  own branch-contested slice).
- **Four cross-boundary verifiers** at the dramatica-complete →
  substrate coupling: Macbeth, Oedipus, Ackroyd, Rocky. Nine
  checks per encoding. DA_mc spectrum: APPROVED 0.77 (Oedipus) /
  PARTIAL 0.69 (Macbeth) / PARTIAL 0.54 (Ackroyd) / APPROVED 0.72
  (Rocky) — a real four-point spread measuring encoding/taxonomy
  match honestly. DSP_limit four-point spectrum post-LT9:
  **all APPROVED** — 0.67 ×3 (Oedipus / Macbeth / Ackroyd, all
  Optionlock, three different signal compositions) + **1.00**
  (Rocky, Timelock-strong via LT9 — two distinct scheduling
  predicates + zero middle-arc LT2 signals; pressure-shape-
  taxonomy-sketch-02 adopts the probe's concrete signature proposal
  and closes the prior sketch-01 NEEDS_WORK 0.33 verdict).
- **Cross-boundary reader-model probe at the dramatica-complete
  surface** — four live probe runs against Rocky / Macbeth /
  Oedipus / Ackroyd. Each reads the Template records, the Lowerings,
  the substrate context, and the verifier's 9-check output, then
  emits annotation reviews on the Lowerings and commentaries on the
  verifier's verdicts. Full spectrum: 96 annotations (90 approved +
  6 needs-work) + 36 commentaries (27 endorses + 7 qualifies + 2
  dissents) across the four encodings; zero dropped. Rocky's dissent
  on DSP_limit NEEDS_WORK 0.33 drove pressure-shape-taxonomy-sketch-02
  (LT7–LT11) — adopted the probe's scheduling-endpoint signature;
  DSP_limit shifted to APPROVED 1.00 same day. Oedipus's DSP_growth
  dissent and three other qualification-level signature proposals
  (agentive-pursuit vs. reactive/consequential events; manipulation
  via participant-role; beat_type-weighted domain signals;
  recognition-structure premise-order inversion) — the first
  all four landed same day as sketches — Oedipus DSP_growth
  (AG5), Oedipus Story_goal (IG2), Ackroyd DA_mc (MN4), Macbeth
  DA_mc (BW4). Verdict shifts: Oedipus DSP_growth PARTIAL 0.5 →
  APPROVED 1.0; Oedipus Story_goal PARTIAL 0.7 → APPROVED 1.0;
  Ackroyd DA_mc PARTIAL 0.54 → APPROVED 0.85; Macbeth DA_mc
  PARTIAL 0.69 → PARTIAL 0.65 (first landed proposal where verdict
  polarity does not change — strength honestly calibrated below
  the unweighted raw ratio per the probe's prediction). The probe
  acts as a steady signature-proposal engine — not a verdict-
  opposition machine — with consistent ~7 endorse + 2 qualify +
  0-1 dissent baseline per 9-check run. **All five probe-proposed
  signatures have now landed as sketches** (LT9 scheduling,
  AG5 agency, IG2 identification-goal, MN4 concealment-
  manipulation, BW4 beat-type-weighting) — the probe/verifier
  loop replicates reliably, five cycles in two days, every banked
  proposal closed. **Second probe pass (v2)** against the refactored
  verifiers: **zero dissents across all 4 encodings** (was 2 in v1)
  — the loop converges on previously-dissented dimensions without
  over-correcting. New coherent finding in v2: all four DSP_resolve
  checks draw qualifications along the same axis (current substrate
  proxies don't measure Dramatica's IC-relational shape) — banked
  as the next forcing function — **landed same day as
  resolve-relational-sketch-01 (RR1–RR6)**, the first cross-corpus
  probe-driven sketch: all four encodings' DSP_resolve checks now
  carry an additive IC-throughline temporal-correlation signal.
  Sixth probe → sketch cycle; second landing where verdict
  polarity doesn't change (honesty about MC↔IC relational signal
  is the deliverable).
- **Two Save the Cat encodings** (Macbeth, Ackroyd) with
  StcCharacter amendment landed. Sheppard carries
  `role_labels=("protagonist", "antagonist", "narrator")` — the
  novel's structural overlap now expressible at the dialect layer.
- **596 tests** across 12 test files. Full suite runs in under a
  second. Standard-library only except for the reader-model probe
  (which needs `anthropic` and `pydantic` from
  `prototype/requirements.txt`).
- **Survey** of prior narrative theories (3-act, 5-act, Propp,
  Campbell, Dramatica, Story Grid, Truby, McKee, Save the Cat,
  Freytag) and computational systems (TALE-SPIN, MINSTREL, Mexica,
  Scheherazade, Façade, Brutus, LLM-era work) in `research/`.

## Where to start

- **New human reader:** [`design/README.md`](design/README.md) first
  (sketch list + active frames), then
  [`prototype/README.md`](prototype/README.md) (module catalog,
  runnable demos), then the Oedipus demo.
- **AI assistant:** [`AGENTS.md`](AGENTS.md) (Codex),
  [`GEMINI.md`](GEMINI.md) (Gemini). Both point back here.

Minimal test subset to confirm the prototype builds and runs:

```sh
cd prototype
python3 test_substrate.py        # 45 tests — core substrate invariants
python3 test_inference.py        # 28 tests — Horn-clause rules + proof-carrying derivation
python3 test_dramatic.py         # 36 tests — Dramatic dialect and M8 verifier
python3 test_verification.py     # 79 tests — verifier primitives + EK2 classifier
python3 test_save_the_cat.py     # 60 tests — Save the Cat dialect S1–S13
```

The demos are narrative — they print per-turn reports rather than
assertions:

```sh
python3 demo.py           # Oedipus Rex: reader / character / Jocasta states through anagnorisis
python3 demo_rashomon.py  # Rashomon: four contested branches side-by-side
```

## Repository layout

- [`design/`](design/) — architectural sketches (`{topic}-sketch-NN.md`).
  Self-contained within a topic. Old sketches kept as historical
  record of the design's evolution.
- [`prototype/`](prototype/) — Python 3.12 reference implementation.
  Written as an executable specification for portability — explicit
  dataclasses, avoided metaclasses and decorators, no framework
  dependencies in the core.
- [`research/`](research/) — two parallel tracks: `theories/` (narrative
  theories of story structure) and `systems/` (computational
  narrative systems, past and present). Long-form survey notes
  deepened over time.
- [`REVIEW.md`](REVIEW.md) — April 2026 editorial review of the
  repository's state, with findings and a plan. Several items have
  since landed; the file remains as a historical reference.
- [`AGENTS.md`](AGENTS.md), [`GEMINI.md`](GEMINI.md) — agent-facing
  guidance for Codex and Gemini respectively. Both are short and
  point here for the overview.

## Development conventions

- **Design first.** Non-trivial architectural change gets a
  Markdown sketch in `design/` before code lands. See
  [`design/README.md`](design/README.md) for the sketch template
  and numbering convention.
- **Sketch immutability.** Superseded sketches stay in place with
  `Status: superseded` and a link to the successor. The design's
  reasoning-over-time is part of the record.
- **Python is a specification language.** The prototype favors
  clarity and portability (dataclasses, tagged unions, plain
  functions) over Python-specific cleverness. The engine may be
  ported later — don't write code a C#/Rust/Go reader would have
  to guess at.
- **Tests are plain `assert`.** No framework. Each test file is a
  list of test functions with a minimal runner. The test surface
  pins sketch commitments — test names reference the sketch they
  protect (e.g., `test_ek2_command_shape_is_external`).
- **Minimal untyped abstractions.** When a refactor becomes
  pressing (e.g., duplicated verifier helpers across three
  encodings), extract the shared piece once there are at least
  two clients. No speculative generalization.
- **Editorial review over toolchain.** No CI, no linters, no
  formatters. Quality control is editorial and visible at commit
  time.

## Commit and PR style

Recent history uses short imperative subjects, with body bullets
explaining the why. Implementation commits often pair with a
follow-on `README:` commit that documents the finding. See
[`git log`](https://github.com/brazilofmux/story/commits/main).

## Context

This project began 2026-04-13 from an empty repository. It is
expected to be a ~20-year personal effort. Early decisions are
valued for their durability; the repository is deliberately
organized as an archive rather than a moving target. Incidents
in the design's history — a finding that flipped a commitment, a
probe that closed an infeasibility question, a refactor that
earned an abstraction — are first-class and preserved.

The author is [@brazilofmux](https://github.com/brazilofmux). The
LLM collaborator on most sessions is Claude (model and session
noted in commit co-authorship).
