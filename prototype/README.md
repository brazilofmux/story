# Prototype — reference implementation

Python 3.12+ reference implementation for the story engine's current
research surface (developed and run on 3.14). The prototype is no
longer just the first substrate pressure-test: it now carries the
substrate, four upper dialects (Dramatic, Dramatica, Save the Cat,
Aristotelian), cross-dialect lowering and verification, the authoring
and compilation front-ends, the generate → evaluate → repair →
convergence loop, and optional reader-model probe tooling.

The load-bearing design still lives in `../design/`. The prototype is
where those commitments are made runnable so they can fail honestly.

## Current scope

Active implementation tracks in this directory:

- **Substrate** — event-primary, branch-aware, tri-temporal core in
  `substrate.py`, with identity substitution and query-time rule
  derivation.
- **Upper dialects** — `dramatic.py`, `dramatica_template.py`,
  `save_the_cat.py`, and `aristotelian.py`.
- **Cross-boundary machinery** — `lowering.py`, `verification.py`,
  `verifier_helpers.py`, `proposal_walker.py`, and `conformance.py`.
- **Authoring and compilation** — the `.story.toml` front-end
  (`authoring.py`, `authoring_interview.py`) and the compiler spikes
  (`compiler.py`, `compiler_scenes.py`, `compiler_stage_3.py`).
- **Generation / evaluation / repair / convergence** — the substrate →
  prose back-end (`draft_generator.py` plus one frame, one blind
  evaluator, and one repairer per dialect, converged by
  `draft_convergence.py`, all routed through the `llm.py` provider
  seam).
- **Story encodings** — substrate and/or upper-dialect encodings for
  sixteen works: Oedipus, Rashomon, Macbeth, Hamlet, Lear, The Duchess
  of Malfi, The Revenger's Tragedy, Ackroyd, And Then There Were None,
  Pride and Prejudice, Rocky, Chinatown, the Turn of the Screw
  infeasibility probe, and three originals (Sworn, The Vantage Light,
  Winter Count).
- **Optional reader-model tooling** — substrate-side client
  (`reader_model_client.py`) and cross-boundary clients
  (`dramatic_reader_model_client.py`,
  `aristotelian_reader_model_client.py`), all outside the
  standard-library-only core.

## Run

Core path: standard library only.

```sh
cd prototype
python3 -m demos.demo
python3 -m demos.demo_rashomon
python3 -m tests.test_substrate      # any stdlib test runs this way
python3 -m tests.test_dramatica_template
```

Bulk run for the standard-library core (all 24 stdlib-only test files):

```sh
cd prototype
for t in \
  test_aristotelian \
  test_authoring \
  test_authoring_interview \
  test_compiler_stage_2 \
  test_compiler_stage_3 \
  test_draft_convergence \
  test_dramatic \
  test_dramatic_generation \
  test_dramatica_generation \
  test_dramatica_template \
  test_fidelity \
  test_identity \
  test_inference \
  test_lowering \
  test_proposal_walker \
  test_rashomon \
  test_save_the_cat \
  test_save_the_cat_generation \
  test_skeleton \
  test_substrate \
  test_sworn \
  test_vantage_light \
  test_verification \
  test_winter_count
  do python3 -m "tests.$t" | tail -1
 done
```

Venv-backed path: requires local venv + `requirements.txt`
(`anthropic`, `openai`, `pydantic`, `jsonschema`) and, for live API
calls, `ANTHROPIC_API_KEY`.

**Model provider is chosen by the model name** (`story_engine/core/llm.py`).
Every call — interview extraction, authoring compile, draft generation,
repair, reader-model probes, and the blind evaluators — routes through one
seam and picks its backend from the `model=` argument: `claude-*` →
Anthropic, `grok-*` → xAI (needs `XAI_API_KEY`; `gpt-*`/`gemini-*` are
reserved). Pass `model="grok-4.3"` to any of them, or set
`STORY_LLM_MODEL=grok-4.3` to flip the whole engine's default in one place
(an explicit `model=` always wins). This is what lets a draft be
**cross-checked across model families** — Claude and Grok read the same
prose blind and their agreement (not a single model's self-grade) is the
fidelity signal:

```sh
.venv/bin/python3 -m demos.demo_crosscheck_malfi              # Claude vs Grok
.venv/bin/python3 -m demos.demo_crosscheck_malfi --models grok-4.3,claude-opus-4-6
```

```sh
cd prototype
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
for t in \
  test_aristotelian_reader_model_client \
  test_dialect_convergence \
  test_draft_evaluator \
  test_draft_repair \
  test_dramatic_evaluator \
  test_dramatic_reader_model_client \
  test_dramatic_repair \
  test_dramatica_evaluator \
  test_dramatica_repair \
  test_production_format_sketch_01_conformance \
  test_reader_model_client \
  test_save_the_cat_evaluator \
  test_save_the_cat_repair
  do .venv/bin/python3 -m "tests.$t" | tail -1
 done
.venv/bin/python3 -m demos.demo_reader_model --dry-run
.venv/bin/python3 -m demos.demo_reader_model_oedipus --dry-run
.venv/bin/python3 -m demos.demo_reader_model_macbeth --dry-run
.venv/bin/python3 -m demos.demo_reader_model --walk
```

Cross-boundary verifier demos:

```sh
cd prototype
python3 -m story_engine.encodings.oedipus_dramatica_complete_verification
python3 -m story_engine.encodings.macbeth_dramatica_complete_verification
python3 -m story_engine.encodings.ackroyd_dramatica_complete_verification
python3 -m story_engine.encodings.macbeth_save_the_cat_verification
python3 -m story_engine.encodings.ackroyd_save_the_cat_verification
```

## Package layout

```
prototype/
├── story_engine/
│   ├── core/          # framework — 35 modules (substrate, four dialects,
│   │                  #   lowering/verification, authoring + compiler,
│   │                  #   generation/evaluation/repair/convergence,
│   │                  #   llm provider seam, reader-model clients)
│   ├── encodings/     # 62 modules across 16 works
│   └── tools/         # skeleton generator CLI + templates
├── tests/             # 37 standalone test scripts (1,337 tests)
├── demos/             # 36 demo scripts
├── reader_model_*.json  # probe output artifacts
├── README.md
└── requirements.txt
```

See [`design/package-structure-sketch-01.md`](../design/package-structure-sketch-01.md)
for the structural commitments (PS1–PS5: directory shape, absolute
imports, run conventions, package markers, module-membership rule).

## Files

### Core engine

- `substrate.py` — fold semantics, reader/world projection,
  dramatic-irony queries, identity substitution, and query-time rule
  derivation.
- `lowering.py` — Lowering records plus annotation review and
  staleness machinery.
- `verification.py` — verifier output records, primitive helpers,
  orchestration support, and coverage-gap reporting.
- `verifier_helpers.py` — shared structural predicates used by
  encoding verifiers.
- `proposal_walker.py` — interactive walker for review entries,
  proposals, annotation reviews, and verifier commentary.
- `conformance.py` — corpus audits for encoding referential integrity;
  audit functions return structured `AuditReport`s shared by the
  conformance test and any future tooling.

### Dialects and templates

- `dramatic.py` — base Dramatic dialect.
- `dramatica_template.py` — Dramatica theory data and Template-level
  verifier for the Dramatic dialect.
- `save_the_cat.py` — Save the Cat dialect and verifier.
- `aristotelian.py` — Aristotelian dialect (per aristotelian-sketch-01):
  ArMythos/ArPhase records, complex-plot commitments, unity checks.

### Authoring and compilation

- `authoring.py` — the human front-end: compiles a plain-text
  `.story.toml` file to the same verified substrate + overlay objects
  the generator and evaluators consume.
- `authoring_interview.py` — AI-interview authoring: a pure,
  per-dialect gap reporter (`interview_gaps`) drives an interviewer
  that elicits the authoring dict conversationally.
- `compiler.py` — compiler entry points per compilation-sketch-01;
  currently stage 2 (feasibility gate). Pure function: no I/O, no
  randomness, no LLM.
- `compiler_stage_3.py` — POCL-in-Python planner spike for
  precondition-gap closures (typed variables, structured
  `PlanningError`).
- `compiler_scenes.py` — operator schemas and scene fixtures exercised
  by the stage-3 planner tests.

### Generation, evaluation, repair, convergence

The substrate → prose back-end. The generator is dialect-agnostic (it
defines only the neutral `DialectFrame` interface); each dialect ships
a frame, a blind evaluator, and a repairer as peers. All model calls
route through the `llm.py` provider seam described above.

- `llm.py` — the provider seam: `parse` (typed output) and `generate`
  (free text); backend chosen by model name.
- `fidelity.py` — the shared evaluator core (stdlib): the one
  `FidelityFinding`/`FidelityReport` pair, the name-matching policy
  (articles + one honorific set, title fallback), the fuzzy
  content-overlap matcher, and the authored-side name lookup. The four
  evaluators alias its records under their own vocabularies
  (`evaluator-shared-core-sketch-01`).
- `draft_generator.py` — walks the sjuzhet and renders first-draft
  prose from a verified substrate; the substrate is the source of
  truth, the LLM is the renderer.
- `draft_convergence.py` — iterates generate → evaluate → repair to a
  structural-fidelity ceiling; splices repaired scenes and re-scores
  the whole draft. Control loop is dependency-injected and
  offline-testable.
- Dialect frames (generation adapters):
  - `aristotelian_generation.py` — surfaces an ArMythos as bible
    sections + per-scene structural marks (peripeteia, anagnorisis,
    pathos-centre, recognition chain).
  - `dramatica_generation.py` — reads a full storyform (throughlines,
    signposts, dynamics, goal); unlocks shapes like Rocky's
    Failure × Good ending.
  - `save_the_cat_generation.py` — the 15-beat sheet and A/B strands;
    authored beat → event mapping with an honest page-proportion
    fallback.
  - `dramatic_generation.py` — the lean parent dialect with the
    minimal three-actor template (Hero / Obstacle / Helper) and the
    thematic Argument.
- Blind evaluators (prose → structure → fidelity diff; the reader
  never sees the answer key):
  - `draft_evaluator.py` — Aristotelian decompile-and-compare;
    name-level fidelity score for the substrate → prose round-trip.
  - `dramatica_evaluator.py` — Dramatica terms: throughlines, goal,
    Outcome × Judgment as independent axes, MC resolve.
  - `save_the_cat_evaluator.py` — which of the fifteen named beats
    read back from the prose, in order.
  - `dramatic_evaluator.py` — crisp function-casting checks plus
    labelled-fuzzy argument/stakes matching.
- Repairers (fidelity findings → targeted scene re-renders; diffuse
  losses are reported, never forced onto one scene):
  - `draft_repair.py` — maps localizable Aristotelian losses to their
    substrate events and re-renders those scenes with directives.
  - `dramatica_repair.py` — localizes ending-sealed shape drifts
    (outcome / judgment / resolve) to the climactic scene.
  - `save_the_cat_repair.py` — lost beats re-render exactly the
    authored carrier scene; the most cleanly localizable dialect.
  - `dramatic_repair.py` — localizes only the argument's resolution
    (to the final beat); everything else is diffuse by design.

### Story encodings (`story_engine/encodings/` — 62 modules, 16 works)

One row per work. Module names drop the shared `{work}_` prefix:
"substrate" is the bare `{work}.py` fabula encoding; overlay columns
name the dialect encodings; "cross-boundary" collects `_lowerings` and
`_verification` modules.

| Work | Substrate | Dialect overlays | Cross-boundary |
|---|---|---|---|
| Oedipus | `oedipus` | `_aristotelian`, `_dramatic`, `_dramatica_complete` | `_lowerings`, `_verification`, `_dramatica_complete_verification` |
| Rashomon | `rashomon` | `_aristotelian`, `_dramatic`, `_dramatica_complete` | `_lowerings`, `_dramatica_complete_verification` |
| Macbeth | `macbeth` | `_aristotelian`, `_dramatic`, `_dramatica_complete`, `_save_the_cat` | `_lowerings`, `_verification`, `_dramatica_complete_verification`, `_save_the_cat_lowerings`, `_save_the_cat_verification` |
| Ackroyd | `ackroyd` | `_dramatic`, `_dramatica_complete`, `_save_the_cat` | `_lowerings`, `_verification`, `_dramatica_complete_verification`, `_save_the_cat_lowerings`, `_save_the_cat_verification` |
| Rocky | `rocky` | `_dramatic`, `_dramatic_three_actor`, `_dramatica_complete` | `_lowerings`, `_dramatica_complete_verification` |
| And Then There Were None | `and_then_there_were_none` | `_dramatic`, `_dramatica_complete` | `_lowerings`, `_dramatica_complete_verification` |
| Hamlet | `hamlet` | `_aristotelian` | — |
| King Lear | `lear` | `_aristotelian` | — |
| The Duchess of Malfi | `malfi` | `_aristotelian` | — |
| The Revenger's Tragedy | `revengers_tragedy` | `_aristotelian` | — |
| Chinatown | — | `_dramatic`, `_dramatica_complete` | — |
| Pride and Prejudice | — | `_dramatic`, `_dramatica_complete` | — |
| Sworn (original) | `sworn` | `_aristotelian` | — |
| The Vantage Light (original) | `vantage_light` | `_aristotelian` | — |
| Winter Count (original) | `winter_count` | `_dramatica_complete` | — |
| The Turn of the Screw | `turn_of_the_screw` | — | — |

Notes:

- `rocky_dramatic_three_actor.py` is a deliberate contrast encoding:
  the same substrate under the minimal three-actor Dramatic template
  instead of the full storyform.
- `turn_of_the_screw.py` is an adversarial infeasibility probe, not a
  production encoding; findings live in `design/`.
- Sworn, The Vantage Light, and Winter Count are original stories
  authored to test whether the pipeline generates or merely re-renders
  works the model already knows (Sworn additionally runs its sjuzhet
  in strict reverse).
- The `*_dramatica_complete_verification.py` modules double as runnable
  demos (see the verifier-demo commands above).

### Reader-model tooling

- `reader_model_client.py` — substrate-side typed client.
- `dramatic_reader_model_client.py` — cross-boundary typed client for
  the Dramatic dialect.
- `aristotelian_reader_model_client.py` — cross-boundary typed client
  for the Aristotelian dialect.
- `reader_model_client_base.py` — shared infrastructure for the three
  clients (uniform drop-shape, shared system-prompt opener), factored
  out once the pattern was stable across three invocations.
- `demos/demo_reader_model*.py`, `demos/demo_dramatic_reader_model_*.py`,
  and `demos/demo_aristotelian_reader_model_*.py` — prompt inspection /
  live-probe drivers. The `demos/` directory (36 scripts) also carries
  the generation-track drivers: `demo_generate_*`, `demo_evaluate_*`,
  `demo_repair_*`, `demo_converge_malfi`, `demo_crosscheck_malfi`, and
  the authoring front-ends `author_story` / `author_by_interview`.

### Author tools

- `story_engine/tools/skeleton.py` — CLI tool that writes the
  canonical 5-file encoding stub given a work-id, title, and
  character list. See
  [`../design/skeleton-generator-sketch-01.md`](../design/skeleton-generator-sketch-01.md)
  for commitments SG1–SG6. Invoked as
  `python3 -m story_engine.tools.skeleton --work-id <id> --title
  "<Title>" --characters "id1:Name1,id2:Name2" [--out-dir <path>]
  [--force]`. Step 2 of the 5-step expert-system author flow
  (start, **skeleton**, fill, walk/check, prose).
- `story_engine/tools/skeleton_templates.py` — template strings
  for each of the 5 generated files. Separated from the CLI for
  independent testability.

### Tests

The prototype currently has **37 test files / 1,337 tests**, all under
`tests/`.

- Standard-library path (24 files): `test_aristotelian.py`,
  `test_authoring.py`, `test_authoring_interview.py`,
  `test_compiler_stage_2.py`, `test_compiler_stage_3.py`,
  `test_draft_convergence.py`, `test_dramatic.py`,
  `test_dramatic_generation.py`, `test_dramatica_generation.py`,
  `test_dramatica_template.py`, `test_fidelity.py`, `test_identity.py`,
  `test_inference.py`, `test_lowering.py`, `test_proposal_walker.py`,
  `test_rashomon.py`, `test_save_the_cat.py`,
  `test_save_the_cat_generation.py`, `test_skeleton.py`,
  `test_substrate.py`, `test_sworn.py`, `test_vantage_light.py`,
  `test_verification.py`, `test_winter_count.py`.
- Venv-backed path (13 files — need `pydantic` et al. from
  `requirements.txt`, no API key):
  `test_aristotelian_reader_model_client.py`,
  `test_dialect_convergence.py`, `test_draft_evaluator.py`,
  `test_draft_repair.py`, `test_dramatic_evaluator.py`,
  `test_dramatic_reader_model_client.py`, `test_dramatic_repair.py`,
  `test_dramatica_evaluator.py`, `test_dramatica_repair.py`,
  `test_production_format_sketch_01_conformance.py`,
  `test_reader_model_client.py`, `test_save_the_cat_evaluator.py`,
  `test_save_the_cat_repair.py`.

## Non-goals

- Performance. The fold still recomputes on demand; memoization is not
  the point.
- Authoring ergonomics. The `.story.toml` and interview front-ends
  exist to prove the compile path, not to be a polished authoring
  product; encodings in the corpus remain Python-record first.
- False completeness. The repository is deliberately willing to leave
  partial verifier results and open design questions visible.
