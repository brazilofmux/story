# Prototype — reference implementation

Python 3.12 reference implementation for the story engine's current
research surface. The prototype is no longer just the first substrate
pressure-test: it now carries the substrate, two upper dialects,
cross-dialect lowering and verification, and optional reader-model
probe tooling.

The load-bearing design still lives in `../design/`. The prototype is
where those commitments are made runnable so they can fail honestly.

## Current scope

Active implementation tracks in this directory:

- **Substrate** — event-primary, branch-aware, tri-temporal core in
  `substrate.py`, with identity substitution and query-time rule
  derivation.
- **Upper dialects** — `dramatic.py`, `dramatica_template.py`, and
  `save_the_cat.py`.
- **Cross-boundary machinery** — `lowering.py`, `verification.py`,
  `verifier_helpers.py`, and `proposal_walker.py`.
- **Story encodings** — substrate and/or upper-dialect encodings for
  Oedipus, Rashomon, Macbeth, Ackroyd, Pride and Prejudice, Rocky,
  and Chinatown.
- **Optional reader-model tooling** — substrate-side client
  (`reader_model_client.py`) and cross-boundary client
  (`dramatic_reader_model_client.py`), both outside the standard-
  library-only core.

## Run

Core path: standard library only.

```sh
cd prototype
python3 -m demos.demo
python3 -m demos.demo_rashomon
python3 -m tests.test_substrate
python3 -m tests.test_identity
python3 -m tests.test_inference
python3 -m tests.test_dramatic
python3 -m tests.test_dramatica_template
python3 -m tests.test_lowering
python3 -m tests.test_verification
python3 -m tests.test_rashomon
python3 -m tests.test_proposal_walker
python3 -m tests.test_save_the_cat
```

Minimal bulk run for the standard-library core:

```sh
cd prototype
for t in \
  test_dramatic \
  test_dramatica_template \
  test_identity \
  test_inference \
  test_lowering \
  test_proposal_walker \
  test_rashomon \
  test_save_the_cat \
  test_skeleton \
  test_substrate \
  test_verification
  do python3 -m "tests.$t" | tail -1
 done
```

Optional reader-model path: requires local venv + `requirements.txt`
(`anthropic`, `pydantic`) and, for live API calls, `ANTHROPIC_API_KEY`.

```sh
cd prototype
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python3 -m tests.test_reader_model_client
.venv/bin/python3 -m tests.test_dramatic_reader_model_client
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
│   ├── core/          # framework — 10 modules (substrate, dialects,
│   │                  #   lowering, verification, verifier_helpers,
│   │                  #   proposal_walker, reader-model clients)
│   └── encodings/     # 39 modules across 8 works (oedipus, macbeth,
│                      #   ackroyd, rocky, rashomon, chinatown,
│                      #   pride_and_prejudice, turn_of_the_screw)
├── tests/             # 12 standalone test scripts
├── demos/             # 11 demo scripts
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

### Dialects and templates

- `dramatic.py` — base Dramatic dialect.
- `dramatica_template.py` — Dramatica theory data and Template-level
  verifier for the Dramatic dialect.
- `save_the_cat.py` — Save the Cat dialect and verifier.

### Story encodings

- Substrate encodings: `oedipus.py`, `rashomon.py`, `macbeth.py`,
  `ackroyd.py`, `turn_of_the_screw.py`.
- Dramatic encodings: `oedipus_dramatic.py`, `macbeth_dramatic.py`,
  `ackroyd_dramatic.py`, `rocky_dramatic.py`,
  `pride_and_prejudice_dramatic.py`, `chinatown_dramatic.py`.
- Dramatica-complete encodings: `oedipus_dramatica_complete.py`,
  `macbeth_dramatica_complete.py`, `ackroyd_dramatica_complete.py`,
  `rocky_dramatica_complete.py`,
  `pride_and_prejudice_dramatica_complete.py`,
  `chinatown_dramatica_complete.py`.
- Save the Cat encodings: `macbeth_save_the_cat.py`,
  `ackroyd_save_the_cat.py`.

### Cross-boundary bindings and verifiers

- Lowerings: `oedipus_lowerings.py`, `macbeth_lowerings.py`,
  `ackroyd_lowerings.py`, `macbeth_save_the_cat_lowerings.py`,
  `ackroyd_save_the_cat_lowerings.py`.
- Dramatic → substrate verifiers: `oedipus_verification.py`,
  `macbeth_verification.py`, `ackroyd_verification.py`.
- Dramatica-complete → substrate verifiers:
  `oedipus_dramatica_complete_verification.py`,
  `macbeth_dramatica_complete_verification.py`,
  `ackroyd_dramatica_complete_verification.py`.
- Save the Cat → substrate verifiers:
  `macbeth_save_the_cat_verification.py`,
  `ackroyd_save_the_cat_verification.py`.

### Reader-model tooling

- `reader_model_client.py` — substrate-side typed client.
- `dramatic_reader_model_client.py` — cross-boundary typed client.
- `demo_reader_model*.py` and `demo_dramatic_reader_model_*.py` —
  prompt inspection / live-probe drivers.

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

The prototype currently has **13 test files / 581 tests** (standard-library core).

- Standard-library core: `test_substrate.py`, `test_identity.py`,
  `test_inference.py`, `test_dramatic.py`,
  `test_dramatica_template.py`, `test_lowering.py`,
  `test_verification.py`, `test_rashomon.py`,
  `test_proposal_walker.py`, `test_save_the_cat.py`,
  `test_skeleton.py`.
- Venv-only client tests: `test_reader_model_client.py`,
  `test_dramatic_reader_model_client.py`.

## Non-goals

- Performance. The fold still recomputes on demand; memoization is not
  the point.
- Authoring ergonomics. Story authoring is still Python-record first;
  any author-document surface remains provisional in `design/`.
- False completeness. The repository is deliberately willing to leave
  partial verifier results and open design questions visible.
