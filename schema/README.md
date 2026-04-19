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

## What's here

### Substrate layer (structurally complete, six records)

- `description.json` — the `Description` record
  (descriptions-sketch-01 §The description record as amended
  2026-04-19). Shipped by production-format-sketch-01.
- `entity.json` — the `Entity` record
  (substrate-entity-record-sketch-01 SE1–SE6). Shipped by
  production-format-sketch-02.
- `prop.json` — the `Prop` literal (substrate-prop-literal-
  sketch-01 PL1–PL7). Shipped by production-format-sketch-03.
- `event.json` — the `Event` record plus inline `WorldEffect`
  and `KnowledgeEffect` $defs (substrate-sketch-05 §Event
  internals + substrate-effect-shape-sketch-01 ES1–ES7 as
  amended by substrate-held-record-sketch-01 SH5+SH8).
  Shipped by production-format-sketch-03; KnowledgeEffect
  sub-schema amended by production-format-sketch-04.
- `held.json` — the `Held` record (substrate-held-record-
  sketch-01 SH1–SH7). Shipped by production-format-sketch-04.
- `branch.json` — the `Branch` record (substrate-sketch-04
  §Branch representation: label, kind, parent conditional
  on kind, optional metadata). Shipped by production-format-
  sketch-05.

### Dialect layer (Aristotelian, three core records)

Under `schema/aristotelian/` per production-format-sketch-06
PFS6-N1 — first dialect to ship production-layer artifacts;
establishes the `schema/<dialect>/` namespace convention for
future dialect-schema arcs.

- `aristotelian/phase.json` — the `ArPhase` record
  (aristotelian-sketch-01 A2: logical division with id, role
  enum {beginning, middle, end}, scope_event_ids, optional
  annotation).
- `aristotelian/character.json` — the `ArCharacter` record
  (aristotelian-sketch-01 A5: id, name, optional
  character_ref_id cross-dialect hook, optional hamartia_text,
  optional is_tragic_hero).
- `aristotelian/mythos.json` — the `ArMythos` record
  (aristotelian-sketch-01 A1: the dialect's primary record;
  required id / title / action_summary / central_event_ids /
  plot_kind / phases; optional peripeteia / anagnorisis /
  complication / denouement pointers; three unity assertions
  with configurable bounds per A6; authorial catharsis claim
  per A8). Cross-file $refs into `phase.json` and
  `character.json` via PFS6-X1.

`ArObservation` (verifier output) and the Aristotelian cross-
boundary records (`ArAnnotationReview`,
`ArObservationCommentary`, `DialectReading`) are deferred to
the Production C cross-boundary arc, per PFS6 §Scope.

### Cross-file references

Substrate-layer cross-file references resolve via canonical
`$id` URIs using a `jsonschema.referencing.Registry` in the
conformance test layer (pattern established by production-
format-sketch-03 PFS3-E1; extended by sketch-04 P4A1 for held;
extended by sketch-06 PFS6-D5 for the aristotelian dialect).
Branch's `schema/branch.json` has no outbound cross-file
references; the Aristotelian mythos has two (phase.json and
character.json). Labels on `event.json`'s `branches` field
and event-id strings on ArMythos / ArPhase are plain string
arrays / strings, not $ref-typed — see production-format-
sketch-05 §Open questions OQ3 and production-format-sketch-06
§Open questions OQ3 for the cross-reference-consistency audit
surface.

## What's deferred

- Remaining dialect records (Dramatic, Save-the-Cat, Dramatica-
  complete; `ArObservation` for Aristotelian). Each dialect or
  record group needs its own production-format sketch;
  Aristotelian-core (three records) shipped under PFS6 as the
  first dialect-layer example.
- Cross-boundary records (Lowering, VerificationReview,
  StructuralAdvisory, VerifierCommentary, ArAnnotationReview,
  ArObservationCommentary, DialectReading). Multiple production
  sketches.
- KnowledgeState record (per-agent-per-τ_s state — a
  collection of Helds plus agent_id). No current consumer.

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
