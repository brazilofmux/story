# Evaluator shared core — sketch 01 (the four-dialect extraction)

**Status:** active; **landed** 2026-07-30 — all six commitments
implemented (`fidelity.py`, `decompile_blind`, template-side
`normalize_dynamics` / `throughline_perspective`); full suite green,
no pinned fixture flipped; the shared policy pinned by
`tests/test_fidelity.py`.
**Date:** 2026-07-30
**Extends:** `draft_evaluator.py`, `dramatica_evaluator.py`,
`save_the_cat_evaluator.py`, `dramatic_evaluator.py`;
`authoring.py` / `authoring_interview.py` (dynamics normalization);
`dramatica_generation.py` / `dramatica_evaluator.py` (throughline
perspective).
**Frames:** the repo rule "extract the shared piece once there are at
least two clients — no speculative generalization" (AGENTS.md), and the
2026-07-30 audit finding that the four dialects' evaluators have crossed
that threshold with **observed divergence**.

## The finding

When the second, third, and fourth dialects reached evaluate-parity, each
was written as a peer of `draft_evaluator.py` by copying its shape. That
was the right call at the time — parity first, extraction when earned.
Four clients later, the copies have diverged where they were supposed to
agree:

- `FidelityFinding` + `FidelityReport` (with identical `scored` /
  `preserved` / `score` properties) exist **four times**, verbatim.
- The `decompile_*` prompt-header assembly + `invoke_parse_helper` call
  is quadruplicated.
- **Name matching diverged by corpus.** The Aristotelian evaluator's
  stop-set carries Malfi vocabulary (`duke`, `duchess`, `cardinal`);
  Save-the-Cat's carries Macbeth vocabulary (`lord`, `lady`, `thane`);
  Dramatic has a generic content stop-set; Dramatica strips **nothing**
  (two names could match on a shared "the"). The same character-name
  pair can match under one dialect's evaluator and fail under another.
  A stop-word fix applied to one copy has demonstrably not propagated.
- `_split_dual_pole` + `_normalize_dynamics` are duplicated near-verbatim
  between `authoring.py` and `authoring_interview.py` (docstrings already
  drifted).
- `_perspective_of` is duplicated with different return vocabularies
  (`"mc"` vs `"main character"`), and `authoring.py` documents that its
  throughline-id minting must stay in lockstep with both — three sites
  encoding one convention.
- `_char_name` is identical in `draft_repair.py` and `draft_evaluator.py`.

## Commitments

**ESC1 — one fidelity record pair, stdlib home.** A new
`story_engine/core/fidelity.py` (standard library only — dataclasses and
string work, no pydantic) holds the single `FidelityFinding` /
`FidelityReport` definitions and the shared comparison helpers. The
evaluators stay venv-backed (their Stage 1 is pydantic); the *record
types and scoring* they share are pure Python and belong on the stdlib
side of the line.

**ESC2 — the dialect vocabulary is the API; the implementation is
shared.** Each dialect module keeps its public names
(`StcFidelityFinding`, `DramaticaFidelityReport`, …) as aliases of the
shared classes. Tests, demos, and repair planners are untouched. This is
not compatibility scaffolding — the per-dialect names are the dialect's
own vocabulary, which is the project's whole thesis; they simply stop
being four definitions.

**ESC3 — one name-matching policy.** `fidelity.name_matches(a, b)`:
tokenize alnum/lowercase; drop articles (`the a an of`); drop honorific
titles (one set: `cardinal count countess duchess duke king lady lord
prince princess queen sir thane`); match on core-token overlap; if the
cores are disjoint or empty, fall back to a **shared title token**
("the Duchess" ↔ "the Duchess of Amalfi" matches on the title;
"the Duchess" ↔ "the Duke" does not). The corpus-specific sets merge: a
title word is a title word in any corpus. Two deliberate behavior
changes, both in the honest direction:

- Dramatica's name matching stops accepting article-only overlap
  (a latent false-positive, never yet triggered by a fixture).
- The title fallback now applies uniformly, so e.g. an StC read of
  "King …" can title-match an authored "King …" the way the
  Aristotelian evaluator always allowed. The offline fixtures pin the
  observable results; any fixture flip is a finding, not a breakage.

`fidelity.content_overlap(read, *authored)` takes the Dramatic
evaluator's fuzzy content-token overlap (with its generic stop-set) as
the one shared fuzzy matcher; Dramatica's ending-phrase fallback uses it
too. `fidelity.char_name(ref_id, mythos)` replaces the
evaluator/repair twins (the generator's `name_map` variant has a
different contract and stays local).

**ESC4 — one blind-decompile assembly.** `reader_model_client_base.py`
(already the venv-side shared home) gains `decompile_blind(...)`: title
line, frame line, instruction line, `=== DRAFT PROSE ===`, then
`invoke_parse_helper`. The four `decompile_*` functions become thin
wrappers passing their system prompt, schema, and genre note. The
genre-only discipline (never pass the generation note) stays documented
at each dialect's wrapper — it is the dialect's contract with its
reader, not plumbing.

**ESC5 — dynamics normalization lives with the template.**
`split_dual_pole` and `normalize_dynamics` move to
`dramatica_template.py` (public, stdlib), which already owns the DSP
axis vocabulary; `authoring.py` and `authoring_interview.py` import
them. The dual-pole discipline ("honored, not flattened" —
`dramatica-precision-limit`) gets documented once, at the definition.

**ESC6 — one throughline-perspective classifier.**
`dramatica_template.throughline_perspective(tl_id)` returns the short
code (`"overall" | "mc" | "ic" | "rel"`). `dramatica_generation` uses it
directly; `dramatica_evaluator` maps codes to its reader-facing labels.
`authoring.py`'s stem-minting comment points at the classifier instead
of naming two modules that must stay in lockstep.

## Non-goals

- No change to any dialect's *scoring semantics* beyond the two named
  name-matching changes. Axis scoring (Dramatica), beat-slot mapping
  (StC), resolution normalization (Dramatic), and the Aristotelian
  dimension list stay in their dialects.
- No shared "evaluator base class". The dialects' Stage 2 comparison
  functions differ structurally because the theories differ; only the
  record types, the matching policy, and the prompt assembly are
  actually common. Extracting more would be the speculative
  generalization the repo forbids.
- Repair planners are untouched (they duck-type the reports).

## Open questions

- Should the title set grow honorifics as new corpora arrive (e.g.
  "doctor", "captain"), or is a per-storyform title hint the honest
  mechanism? Deferred until a corpus actually needs it.
