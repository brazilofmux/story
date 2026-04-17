# Repository guidelines

Start with [`README.md`](README.md) for the project overview. This
file carries the agent-specific guidelines on top of what's there.

## What this repo is

A research and design notebook plus working Python prototype for a
story-telling engine. Three tracks live here:

- `design/` — architectural sketches; self-contained per topic.
- `prototype/` — Python 3.12 reference implementation with ~510
  tests across 12 test files. Executable specification.
- `research/` — long-form surveys of narrative theories and
  computational narrative systems.

Treat the design sketches as the load-bearing content. Prototype
code is the sketches made runnable; research is the evidence base
the sketches argue against.

## Working in `design/`

- Files are named `{topic}-sketch-NN.md`. Each sketch has a
  **Status** (*draft*, *active*, *superseded*, *abandoned*) and a
  **Date** at the top.
- Active sketches are self-contained within their topic. A reader
  should be able to understand the current state of that topic
  from the active sketch alone.
- Never overwrite a superseded sketch — mark `Status: superseded`
  and link to the successor.
- Sketches are design thinking in progress. Open questions are
  first-class. Tentative claims get labeled.
- Tone is analytical, direct, skeptical — not promotional.

## Working in `prototype/`

- Python 3.12, standard library only for the core. The
  reader-model probe adds `anthropic` and `pydantic` via
  `requirements.txt`; install into a local `.venv`.
- Tests are plain `assert` with a minimal runner at the bottom of
  each file. No framework. Each test's docstring should note
  which sketch commitment it pins.
- Run the standard-library core tests before claiming a change works:

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
  do
    python3 "$t" | tail -1
  done
  ```

- The reader-model probe and client tests require the venv; live
  demos also require an API key:

  ```sh
  cd prototype
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
  .venv/bin/python3 test_reader_model_client.py
  .venv/bin/python3 test_dramatic_reader_model_client.py
  .venv/bin/python3 demo_reader_model.py --dry-run
  ```

- Python is a specification language. Favor explicit records
  (`@dataclass(frozen=True)`, tagged unions, plain functions)
  over Python-specific cleverness (metaclasses, descriptors,
  complex generics). The engine may be ported later.
- When a refactor becomes pressing, extract the shared piece
  once there are at least two clients — no speculative
  generalization.

## Working in `research/`

- One Markdown file per theory or system. Long-form, permanent,
  deepened over time.
- Start from `theories/_template.md` or `systems/_template.md`
  when adding a new entry.
- Index tables in `research/theories/README.md` and
  `research/systems/README.md` must be updated when entries are
  added.
- Honest surveys, not cheerleading. Record where each theory /
  system is coherent and where it falls apart. Formalizability
  is a first-class question: *what would it take to encode this
  as data + rules an engine could operate on?*
- Cite primary sources. When an entry leans on secondhand
  summaries, label the tentative claims.

## Tool preferences

- File search: use glob patterns (`prototype/test_*.py`,
  `design/*-sketch-01.md`) rather than `find`.
- Content search: ripgrep / search tools work well; the
  repository is small enough that naive search is fine.
- Editing: prefer targeted edits to full-file rewrites.

## Commit and PR style

- Short imperative commit subjects, under ~80 chars. Many recent
  commits follow a pattern like `{topic}: {landing finding}` or
  `README: {finding update}`.
- Implementation commits often pair with a follow-on `README:`
  commit documenting the finding in `design/README.md`.
- Body uses bullet points explaining the *why* — especially when
  a finding flipped a commitment or closed an open question.
- Commits carrying Claude co-authorship use:

  ```
  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  ```

  (with the model + session matching the actual collaboration).

## What to avoid

- Do not add CI, linters, formatters, or test frameworks. Quality
  control is editorial.
- Do not add dependencies to the prototype core. The reader-model
  probe is the only exception and is scoped to its own files.
- Do not overwrite superseded design sketches or mangle historical
  records. The design's reasoning-over-time is part of the record.
- Do not simplify away hard problems. The project was picked
  because it is hard; shortcuts that paper over the difficulty
  are counterproductive.
- Do not add speculative generalization or future-proofing
  scaffolding. If the forcing function isn't concrete, the
  abstraction isn't earned.

## Key files to reference

- [`design/README.md`](design/README.md) — sketch list + upcoming
  work + recently landed.
- [`design/architecture-sketch-01.md`](design/architecture-sketch-01.md) —
  grid-snap scope, two-surface semantics, A3 inclusion test.
- [`design/architecture-sketch-02.md`](design/architecture-sketch-02.md) —
  multi-dialect stack with substrate as sink.
- [`design/substrate-sketch-05.md`](design/substrate-sketch-05.md) —
  current substrate statement.
- [`prototype/README.md`](prototype/README.md) — module catalog.
- [`REVIEW.md`](REVIEW.md) — April 2026 editorial review; several
  items have since landed but the document is still useful as a
  shape-of-the-project reference.
