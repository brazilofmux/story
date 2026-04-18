# Skeleton generator — sketch 01

**Status:** draft, active
**Date:** 2026-04-18
**Supersedes:** nothing
**Frames:** [architecture-sketch-02](architecture-sketch-02.md) (dialect stack), [dramatica-template-sketch-01](dramatica-template-sketch-01.md) (Dramatica as Template), [package-structure-sketch-01](package-structure-sketch-01.md) (target file layout)
**Related:** state-of-play-02 "What's next" item #3; expert-system 5-step author UX flow (start, **skeleton**, fill, walk/check, prose — per memory note)
**Superseded by:** nothing yet

## Purpose

Close state-of-play-02's skeleton-generator item. Ship a small CLI
tool that, given a work id, a title, and a character list, writes
the five canonical stub files for a new dramatica-complete encoding.
Codifies the mechanical shell of an encoding so the author faces a
shaped file instead of a blank page; does not codify story content.

This is **step 2 of the 5-step expert-system author flow**. Step 1
(start) is conversational — deciding what story to encode. Step 2
(skeleton) produces the files. Step 3 (fill) is manual or
LLM-assisted authoring inside those files. Step 4 (walk/check) runs
verifiers + the cross-boundary probe. Step 5 (prose) renders
author-facing documents.

## Why now

- The refactored `story_engine/encodings/` directory is stable
  (sketch-01 just landed). Adding more encodings is the natural
  next tension; a skeleton tool removes the blank-page friction.
- Current encodings share an enormously consistent five-file shape
  across Oedipus, Macbeth, Ackroyd, Rocky, Rashomon. The pattern
  is stable enough to templatize.
- Later encodings (the banked 6th encoding in state-of-play-02)
  benefit from the tool. Writing them without it means copy-paste
  from an existing encoding and string-replace — slower and more
  error-prone.

## Commitments

- [**SG1**] **Location.** Tool lives at
  `prototype/story_engine/tools/skeleton.py`, invokable as
  `python3 -m story_engine.tools.skeleton` from `prototype/`.
  `prototype/story_engine/tools/__init__.py` is an empty package
  marker, consistent with PS4.

- [**SG2**] **Input via CLI flags.**
  - `--work-id <id>` (required): file prefix and module name,
    e.g., `rashomon`, `and_then_there_were_none`.
    snake_case-validated.
  - `--title <string>` (required): human-readable title for
    docstrings, e.g., `"Rashomon"`.
  - `--characters "<id1:Name1,id2:Name2,...>"` (required, at least
    one character): comma-separated `id:Name` pairs.
    Character-id validated as snake_case; name is free-form.
  - `--out-dir <path>` (optional, default
    `prototype/story_engine/encodings`): output directory. Must
    exist.
  - `--force` (optional flag): overwrite existing files. Default
    is **refuse-to-overwrite** to protect in-progress authoring.

- [**SG3**] **Output.** Five stub files written to `--out-dir`:
  `{work-id}.py`, `{work-id}_dramatic.py`,
  `{work-id}_dramatica_complete.py`, `{work-id}_lowerings.py`,
  `{work-id}_dramatica_complete_verification.py`.

- [**SG4**] **Stub shape.** Each file imports the framework
  surfaces it needs, declares entity-id constants from the
  `--characters` list, and has empty data tuples (`EVENTS = ()`,
  `LOWERINGS = ()`, etc.) with `TODO` comments pointing to the
  fill-in contract. The stub imports cleanly (`python3 -c "import
  story_engine.encodings.{work-id}"` succeeds from `prototype/`);
  the verifier's `run()` entry point runs cleanly and emits a
  "skeletal encoding" advisory listing the missing data.

- [**SG5**] **Dramatica-complete only in v1.** The tool targets
  the dramatica-complete Template. Save-the-Cat,
  author-defined-template, and Dramatic-only stubs are named as
  OQ1 (Save-the-Cat) and OQ2 (Template-neutral) and deferred.

- [**SG6**] **No content invention.** The tool never invents
  events, beats, arguments, lowerings, or signposts. A Character
  stub carries only id + name; role assignments (Protagonist,
  Antagonist, etc.) and Throughline ownership are author-filled.
  This mirrors architecture-sketch-02's commitment that authorial
  intent is authored, not derived.

## Not in scope

- **Interactive prompts.** v1 is non-interactive — all inputs via
  flags, all outputs to files. An interactive wrapper is a
  sketch-02 concern if a forcing function argues for it.
- **Re-generation / merge.** `--force` overwrites; it doesn't
  diff-merge. A skeleton re-run against an in-progress encoding
  is destructive. v2 can add merge logic when the pattern emerges.
- **File count variants.** Always-five-files, always in the same
  shape. An encoding that wants fewer files (e.g., Chinatown's
  2-file stub — upper-dialect only) writes them by hand or waits
  for a sketch-02 commitment.
- **Lowering / Verifier content.** The lowerings file has an empty
  `LOWERINGS = ()` tuple; the verification file registers the
  canonical 9 Template checks but emits skipped advisories until
  the author adds ACTIVE Lowerings. The tool does not pre-wire
  any specific lowerings.
- **Substrate detail.** The substrate stub has empty events,
  branches (canonical only), rules, and descriptions. No entity
  inference from character names, no event skeleton, no rule
  scaffolding.
- **Probe integration.** No reader-model probe wiring. The
  generated encoding is stone-silent until the author adds
  content.
- **Save-the-Cat wiring.** The STC trio (stc.py, stc_lowerings.py,
  stc_verification.py) is not generated. OQ1.

## Generated file shapes

Each shape is sketched below in outline; the tool's template
strings render these with work-id, title, and character
interpolation.

### `{work-id}.py` (substrate stub)

```python
"""
{work-id}.py — {title} substrate encoding (skeleton).

Skeletal stub generated by story_engine.tools.skeleton on {date}.
Author responsibility: fill in EVENTS, BRANCHES, RULES,
DESCRIPTIONS per substrate-sketch-05, identity-and-realization-
sketch-01, inference-model-sketch-01.
"""

from __future__ import annotations

from story_engine.core.substrate import (
    Event, Prop, WorldEffect, KnowledgeEffect,
    BranchLabel, BranchKind, Fabula, Rule,
    Description, DescKind, Attention, DescStatus,
    world, holds, KNOWN, BELIEVED, SUSPECTED, GAP,
)

# ---------------------------------------------------------------
# Entities
# ---------------------------------------------------------------

{character_id_constants}

# ---------------------------------------------------------------
# Events (fabula) — TODO: author here
# ---------------------------------------------------------------

EVENTS: tuple[Event, ...] = ()

# ---------------------------------------------------------------
# Branches — TODO: add contested / counterfactual branches if any
# ---------------------------------------------------------------

B_CANONICAL = BranchLabel(":canonical", BranchKind.CANONICAL)

BRANCHES: tuple[BranchLabel, ...] = (B_CANONICAL,)

# ---------------------------------------------------------------
# Rules (inference-model-sketch-01) — TODO: author if needed
# ---------------------------------------------------------------

RULES: tuple[Rule, ...] = ()

# ---------------------------------------------------------------
# Descriptions (descriptions-sketch-01) — TODO: author as needed
# ---------------------------------------------------------------

DESCRIPTIONS: tuple[Description, ...] = ()

# ---------------------------------------------------------------
# Fabula assembly
# ---------------------------------------------------------------

fabula = Fabula(
    events=EVENTS,
    branches=BRANCHES,
    rules=RULES,
    descriptions=DESCRIPTIONS,
)
```

### `{work-id}_dramatic.py` (Dramatic dialect stub)

Stub imports, one placeholder Argument, four Throughlines stubbed
with standard ids (`T_os`, `T_mc`, `T_ic`, `T_rs`), Characters from
input, empty Scenes / Beats / Stakes, Story wrapping.

### `{work-id}_dramatica_complete.py` (Template stub)

Imports Template surfaces + Dramatic Story reference. Empty
DomainAssignments, DSPs, Signposts, ThematicPicks,
CharacterElementAssignments tuples. Empty Story_goal,
Story_consequence.

### `{work-id}_lowerings.py` (Lowerings stub)

Empty `LOWERINGS: tuple[Lowering, ...] = ()`.

### `{work-id}_dramatica_complete_verification.py` (Verifier stub)

Registers the canonical 9 Template checks (DA_mc, DSP_approach,
DSP_outcome, DSP_judgment, DSP_resolve, DSP_growth, Story_goal,
Story_consequence, DSP_limit). Each check skips because no ACTIVE
Lowerings exist. `run()` entry point emits a single "skeletal
encoding — no data to verify" advisory.

The exact stub template strings live in
`prototype/story_engine/tools/skeleton_templates.py` alongside
`skeleton.py` (separating templates from CLI logic — testable
independently).

## Verification

The skeleton tool ships with `prototype/tests/test_skeleton.py`,
which:

1. Runs the CLI against a temp directory with a minimal invocation
   (one character).
2. Asserts all 5 files are written.
3. Importing each generated file as a module succeeds.
4. Running the generated verifier's `run()` function succeeds and
   emits the expected "skeletal" advisory.
5. Re-running the CLI against the same directory without `--force`
   fails with a "files exist" error.
6. Re-running with `--force` overwrites cleanly.

These are acceptance criteria; the tool is not considered shipped
until the six checks pass.

## Open questions

**OQ1 — Save-the-Cat stubs.** Should the tool accept
`--template=dramatica-complete,save-the-cat` and generate the STC
trio alongside the dramatica stack? Pattern across Macbeth and
Ackroyd suggests the STC shape is stable enough to template.
Deferred until a second encoding has both Templates (current: two
encodings both have STC, but pressure for a third isn't active).

**OQ2 — Template-neutral skeleton.** Author-defined templates
per architecture-sketch-02 are admitted but unimplemented. A
Template-neutral skeleton (generates just Dramatic + substrate +
lowerings) could serve authors who are template-shopping. Would
require the tool to inspect a Template descriptor rather than
bake-in dramatica-complete. Deferred.

**OQ3 — Character functions.** Dramatica-8 assigns 8 function
roles (Protagonist, Antagonist, Sidekick, Contagonist, Reason,
Emotion, Guardian, Skeptic) across characters. The skeleton could
accept `--characters "sherlock:Sherlock[protagonist],watson:Watson
[sidekick]"` and populate function assignments. v1 omits this —
author edits the stub — because the 8-function assignment is
substantial design work that doesn't fit a one-line CLI flag
cleanly. OQ3 resolves when a clean input syntax emerges.

**OQ4 — MC/IC designation.** Similar to OQ3 — which character is
the Main Character, Influence Character? v1 requires the author
to wire `THROUGHLINE_OWNER_CHARACTER` and character-id references
in the stub. A future flag `--mc <char-id> --ic <char-id>` could
populate them directly.

**OQ5 — Beat scaffolding.** The Dramatic dialect's canonical beat
types (inciting, rising, midpoint, climax, denouement — per
beat-weight-taxonomy-sketch-01's BW2) could be pre-stubbed at
standard narrative positions (0%, 25%, 50%, 75%, 100%) with empty
content. Useful for authors who want page-number scaffolding
(Save-the-Cat style); not obviously wanted for Dramatica-first
authors. Deferred.

## Summary

Small CLI tool that writes the canonical 5-file encoding shell
given a work-id, title, and character list. Dramatica-complete
only. No content invention — shape without substance. Imports
cleanly; `run()` on the verifier produces a "skeletal encoding"
advisory until content is added. Test suite (6 checks) is the
acceptance criterion. Five OQs named: STC variant, Template-neutral
variant, character-function assignment, MC/IC designation, beat
scaffolding. v1 ships the narrow happy path; extensions earn their
keep one at a time.
