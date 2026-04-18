# Package structure — sketch 01

**Status:** draft, active
**Date:** 2026-04-18
**Supersedes:** nothing
**Frames:** [architecture-sketch-02](architecture-sketch-02.md) (the dialect stack)
**Related:** `prototype/` top-level reorganization; state-of-play-02 "What's next" item #2
**Superseded by:** nothing yet

## Purpose

Close state-of-play-02's package-split item. Move the 72 flat `.py` files in `prototype/` into a Python package that separates framework ("story_engine.core") from per-work encodings ("story_engine.encodings"), with tests and demos in sibling directories. This is a mechanical refactor; the sketch commits to structural shape and conventions before the move so the discipline is durable.

## Why now

- 72 flat files; `ls prototype/` is no longer scannable.
- The framework/encoding distinction is currently a naming convention only. Packaging makes it structural.
- Memory discipline "Python is a spec language — favor explicit/translatable Python over Python-specific cleverness" argues for proper module identity over flat-import conventions.
- Upcoming work (skeleton generator, sixth encoding) would add more encoding files to an already-cluttered flat layout.

## Commitments

- [**PS1**] **Directory shape.**
  - `prototype/story_engine/core/` — framework (substrate, dialects, lowering, verification, verifier_helpers, proposal_walker, reader-model clients).
  - `prototype/story_engine/encodings/` — per-work encodings (flat; no per-work subdirs — `oedipus.py`, `oedipus_dramatic.py`, …, all siblings).
  - `prototype/tests/` — standalone test scripts.
  - `prototype/demos/` — demo scripts.
  - `prototype/` — `README.md`, `requirements.txt`, `reader_model_*.json` probe outputs.

- [**PS2**] **Absolute imports only.** Every import uses the fully-qualified module path (`from story_engine.core.substrate import Event`, `from story_engine.encodings.oedipus import ...`). No relative imports (`from .substrate ...`); no `sys.path` manipulation. Translatable module identity is the discipline.

- [**PS3**] **Run commands.** `cd prototype && python3 -m tests.test_X` / `python3 -m demos.demo_X`. The prior pattern (`python3 test_X.py` with the test file at prototype/ root) no longer works because the test file's own imports are absolute-qualified.

- [**PS4**] **Empty `__init__.py` files** in `story_engine/`, `story_engine/core/`, `story_engine/encodings/`, `tests/`, `demos/`. Docstring only, no re-exports. Re-exports violate PS2's "module identity is explicit."

- [**PS5**] **Module membership.** A module belongs in `core/` iff either (a) it's part of the framework (substrate, dramatic, dramatica_template, save_the_cat, lowering, verification, verifier_helpers, proposal_walker, reader_model_client, dramatic_reader_model_client) or (b) it's referenced by modules from two or more distinct encodings. Everything else is an encoding. Current inventory: 10 core modules; 39 encoding modules across 8 works.

## Not in scope

- **PyPI packaging / `pyproject.toml`.** The package is discoverable via CWD. PyPI publication is a sketch-02 concern if it becomes relevant.
- **Relative imports anywhere.** Explicitly rejected — see PS2.
- **Test-framework migration.** Tests remain standalone scripts with `if __name__ == "__main__"` at the bottom. Migration to pytest is a separate decision with its own tradeoffs.
- **Probe output relocation.** `reader_model_*.json` files stay at `prototype/` root. They're referenced by exact path in design sketches (state-of-play-02, pressure-shape-taxonomy-sketch-03, etc.) and in commit messages; moving them invalidates those references for no proportionate benefit.
- **Docstring prose overhaul.** Run-command lines in docstrings get updated to the `python3 -m` form; other prose stays unchanged.

## Import rewrite rule

Deterministic table-driven rewrite. For each file in the repo:

- `from <core> import X` → `from story_engine.core.<core> import X`
  where `<core>` is one of the 10 core module names.
- `from <enc> import X` → `from story_engine.encodings.<enc> import X`
  where `<enc>` is any other module name in the original flat layout.
- `import <module>` patterns handled analogously (rewrite target is `import story_engine.core.<module> as <module>` / `import story_engine.encodings.<module> as <module>` to preserve the bare-name reference).

No ambiguity; the core and encoding module names are disjoint (encoding names always begin with a canonical work name: `oedipus`, `macbeth`, `ackroyd`, `rocky`, `rashomon`, `chinatown`, `pride_and_prejudice`, `turn_of_the_screw`; save-the-cat wirings carry the work prefix like `ackroyd_save_the_cat`).

## Verification

Post-refactor all 12 test scripts pass under the new run form:

```sh
cd prototype
python3 -m tests.test_substrate
python3 -m tests.test_identity
python3 -m tests.test_inference
python3 -m tests.test_dramatic
python3 -m tests.test_lowering
python3 -m tests.test_verification
python3 -m tests.test_rashomon
python3 -m tests.test_proposal_walker
python3 -m tests.test_save_the_cat
python3 -m tests.test_dramatica_template
.venv/bin/python3 -m tests.test_reader_model_client
.venv/bin/python3 -m tests.test_dramatic_reader_model_client
```

All 11 demos import cleanly as modules (full runs skipped — some hit the Anthropic API):

```sh
cd prototype
python3 -c "import demos.demo"
python3 -c "import demos.demo_rashomon"
...
```

## Summary

Flat `prototype/` → packaged `prototype/{story_engine{core,encodings}, tests, demos}/`. Absolute imports, no relative / sys.path tricks. Run via `python3 -m`. Probe outputs stay put. 12 tests and 11 demo-imports are the acceptance criteria.
