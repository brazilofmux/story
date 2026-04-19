# schema/

Canonical record-type schemas for the story engine. Specified by
[design/production-format-sketch-01.md](../design/production-format-sketch-01.md).

This directory is the **source of truth** for the shape of every
record type in the story engine. It is intentionally language-
independent: no Python, no Rust, no binary artifacts — only JSON
Schema 2020-12 files and this README.

## The commitment (PFS1)

JSON Schema 2020-12 is the schema language. Each record type
gets one `.json` file. The schema file is the source of truth
for that record's shape; any conforming JSON Schema validator
in any language can read these files and produce conformance
verdicts. This is the port-portability guarantee.

## The methodological lever (PFS2)

Schemas are authored as if the Python prototype does not exist.
The source of truth is the design sketches in
`../design/`. The Python dataclasses in
`../prototype/story_engine/core/` are a
**conformance check**, not a template.

Concretely, when authoring or amending a schema in this
directory:

- Read the design sketches first. For Entity:
  `../design/substrate-sketch-05.md` §Entities. For
  Description:
  `../design/descriptions-sketch-01.md` §The description
  record.
- Do not read `substrate.py`, `lowering.py`, or any other
  prototype source during schema authoring.
- When the sketches leave a question unanswered, the answer is
  "deferred" or "under-specified — sketch-XX forcing function"
  — not "look at the Python."
- When the Python has a field the schema doesn't, the Python
  may be over-specified (drop the field) or the schema may be
  incomplete (amend the design sketch first; then amend the
  schema; then reconcile Python).

The discipline inverts the default: **the schema does not
depend on the Python; the Python depends on the schema.**

## What's here at v1 (production-format-sketch-01)

- `description.json` — the `Description` record
  (descriptions-sketch-01 §The description record).

## What's deferred

- `Entity` — substrate-sketch-05 §Entities describes Entity
  ontologically (Agent is a subtype of Entity) but does not
  enumerate the Entity record's fields: no `name`, no `kind`
  value list. The Python prototype carries those fields; a
  design sketch structurally specifying Entity's record fields
  is the blocker. See production-format-sketch-01 §PFS2
  catches real drift for the detailed finding. Candidate
  sketch name: `substrate-entity-record-sketch-01`.
- `Event` — blocked on a design sketch pinning down
  `KnowledgeEffect` / `WorldEffect` shapes (substrate-sketch-05
  names both but does not structurally define them). Candidate
  sketch name: `substrate-effect-shape-sketch-01`.
- `Prop` — under-specified at the design-sketch level
  (substrate-sketch-05 names Props as "derived, not stored"
  but descriptions-sketch-01 admits proposition-shaped
  anchors). Candidate sketch name:
  `substrate-prop-literal-sketch-01`.
- Dialect records (Throughline, ArMythos, DSP, StcBeat, etc.),
  Lowering, VerificationReview, ArObservation, and other
  cross-boundary records. Substrate schemas first.

## Conformance

The prototype's conformance to these schemas is checked by
`../prototype/tests/test_production_format_sketch_01_conformance.py`.
Each conformance failure is a finding, resolved by amending a
design sketch (and then the schema) — not by quietly matching
the schema to the Python.

## Schema identity vs. fetch

Each schema's `$id` uses a project-stable URI. The URI is the
**identity** of the schema, not a fetch target; validators are
not required to resolve it over the network. If a validator
chooses to fetch, it may fail — this is not a conformance
issue. See sketch OQ5.
