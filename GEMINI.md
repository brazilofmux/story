# story — computational storytelling engine

Gemini-facing entry point. This file deliberately carries no
project facts of its own: an earlier version duplicated the
overview and conventions and silently went stale against both.

Read, in order:

1. [`README.md`](README.md) — what the engine is, coverage,
   quickstart, repository layout.
2. [`AGENTS.md`](AGENTS.md) — agent-facing working guidelines:
   conventions per directory, how to run the tests, commit style,
   and the list of things to avoid (no CI/linters/frameworks, no
   dependencies in the core, no overwriting superseded sketches).
3. `design/state-of-play-NN.md` (highest NN) — the current state
   of the design.

Everything in AGENTS.md applies to Gemini sessions unchanged,
including the co-authorship trailer convention — use the actual
model name, e.g.:

```
Co-Authored-By: Gemini <model name> <noreply@google.com>
```
