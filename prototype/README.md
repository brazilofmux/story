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
python3 demo.py
python3 demo_rashomon.py
python3 test_substrate.py
python3 test_identity.py
python3 test_inference.py
python3 test_dramatic.py
python3 test_dramatica_template.py
python3 test_lowering.py
python3 test_verification.py
python3 test_rashomon.py
python3 test_proposal_walker.py
python3 test_save_the_cat.py
```

Minimal bulk run for the standard-library core:

```sh
cd prototype
for t in \
  test_dramatic.py \
  test_dramatica_template.py \
  test_identity.py \
  test_inference.py \
  test_lowering.py \
  test_proposal_walker.py \
  test_rashomon.py \
  test_save_the_cat.py \
  test_substrate.py \
  test_verification.py
  do python3 "$t" | tail -1
 done
```

Optional reader-model path: requires local venv + `requirements.txt`
(`anthropic`, `pydantic`) and, for live API calls, `ANTHROPIC_API_KEY`.

```sh
cd prototype
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python3 test_reader_model_client.py
.venv/bin/python3 test_dramatic_reader_model_client.py
.venv/bin/python3 demo_reader_model.py --dry-run
.venv/bin/python3 demo_reader_model_oedipus.py --dry-run
.venv/bin/python3 demo_reader_model_macbeth.py --dry-run
.venv/bin/python3 demo_reader_model.py --walk
```

Cross-boundary verifier demos:

```sh
cd prototype
python3 oedipus_dramatica_complete_verification.py
python3 macbeth_dramatica_complete_verification.py
python3 ackroyd_dramatica_complete_verification.py
python3 macbeth_save_the_cat_verification.py
python3 ackroyd_save_the_cat_verification.py
```

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

### Tests

The prototype currently has **12 test files / 514 tests**.

- Standard-library core: `test_substrate.py`, `test_identity.py`,
  `test_inference.py`, `test_dramatic.py`,
  `test_dramatica_template.py`, `test_lowering.py`,
  `test_verification.py`, `test_rashomon.py`,
  `test_proposal_walker.py`, `test_save_the_cat.py`.
- Venv-only client tests: `test_reader_model_client.py`,
  `test_dramatic_reader_model_client.py`.

## Non-goals

- Performance. The fold still recomputes on demand; memoization is not
  the point.
- Authoring ergonomics. Story authoring is still Python-record first;
  any author-document surface remains provisional in `design/`.
- False completeness. The repository is deliberately willing to leave
  partial verifier results and open design questions visible.
