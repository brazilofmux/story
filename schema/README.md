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

### Dialect layer (Aristotelian + Save-the-Cat, seven core records)

Two dialects ship production-layer artifacts. The namespace
convention (`schema/<dialect>/<record>.json`) is committed by
production-format-sketch-06 PFS6-N1; production-format-
sketch-07 PFS7-N1 inherits it. Each dialect's reference
topology matches its Python shape — Aristotelian is tree-with-
inline-$ref (PFS6-X1), Save-the-Cat is flat-with-id-refs
(PFS7-X1). Both are admitted; future dialects choose the
pattern matching their Python.

#### Aristotelian (under `schema/aristotelian/`, three core records)

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

#### Save-the-Cat (under `schema/save_the_cat/`, four core records)

- `save_the_cat/character.json` — the `StcCharacter` record
  (save-the-cat-sketch-02 S9/S10: id, name, optional
  description, optional role_labels array with no closed enum
  per the canonical-plus-open S10 posture).
- `save_the_cat/strand.json` — the `StcStrand` record
  (save-the-cat-sketch-01 S3 + sketch-02 S11: id, kind closed
  enum {a-story, b-story}, optional description, optional
  focal_character_id).
- `save_the_cat/beat.json` — the `StcBeat` record (save-the-
  cat-sketch-01 S1/S2/S3 + sketch-02 S11: required id / slot /
  page_actual with slot bounded 1..15; `advances` array uses
  inline `$defs/strand_advancement` per PFS7-X2;
  `participant_ids` plain-string array per PFS7-X1).
- `save_the_cat/story.json` — the `StcStory` record (save-the-
  cat-sketch-01 S4/S5 + sketch-02 S11/S12: the dialect's root;
  required id / title; optional theme_statement / stc_genre_id /
  beat_ids / strand_ids / character_ids; `archetype_assignments`
  via inline `$defs/archetype_assignment` per PFS7-X2).

`StcObservation` (verifier output) and the dialect-catalog
records `StcCanonicalBeat` (15 shipped-as-data canonical beats)
and `StcGenre` (10 shipped-as-data Snyder genres) are deferred
— the former to Production C, the latter to PFS7 OQ2.

### Cross-boundary layer (Lowering, three records)

Top-level subdirectories for records that sit above the
substrate + dialect layers, connecting them or observing them.
The namespace convention is committed by production-format-
sketch-08 PFS8-N1; per-record arcs follow (PFS9 = Lowering,
PFS10 = Verification, etc.). Classification principle (PFS8-N2):
what a dialect produces OR what the dialect alone consumes
lives in the dialect's namespace; what is shared across
dialects lives in a top-level role-named namespace.

#### Lowering (under `schema/lowering/`, three records)

First namespace under the cross-boundary tier (production-format-
sketch-09 PFS9-N1). Lowering is the authored realization binding
between upper-dialect and lower-dialect records — the load-
bearing cross-boundary record.

- `lowering/lowering.json` — the `Lowering` record (lowering-
  record-sketch-01 L1–L10: required id / upper_record /
  lower_records / annotation / status; optional
  position_range / anchor_τ_a / metadata; status closed enum
  {active, pending} with L8 conditional via allOf/if-then-else
  per PFS9-X3 — active status requires non-empty
  lower_records). Inline `$defs` for three id-less sub-records
  per PFS7-X2: `cross_dialect_ref`, `annotation`,
  `position_range`.
- `lowering/annotation_review.json` — the `AnnotationReview`
  record (review act on a Lowering's annotation; verdict
  closed enum {approved, needs-work, rejected, noted}). Cross-
  file `$ref` target from `annotation.review_states` in
  lowering.json per PFS9-X2.
- `lowering/lowering_observation.json` — the
  `LoweringObservation` record (validate_lowerings output;
  severity closed enum {noted, advises-review}; code open
  string per PFS9-LO3).

### Cross-file references

Substrate-layer cross-file references resolve via canonical
`$id` URIs using a `jsonschema.referencing.Registry` in the
conformance test layer (pattern established by production-
format-sketch-03 PFS3-E1; extended by sketch-04 P4A1 for held;
extended by sketch-06 PFS6-D5 for the aristotelian dialect;
extended by sketch-07 PFS7-D6 for the save-the-cat dialect;
extended by sketch-09 PFS9-D8 for the lowering namespace).
Branch's `schema/branch.json` has no outbound cross-file
references; the Aristotelian mythos has two (phase.json and
character.json); the four Save-the-Cat schemas have none —
the dialect uses plain-string id references between sibling
records per PFS7-X1 (flat-with-id-refs topology). The lowering
namespace has one outbound cross-file `$ref` —
`lowering.json`'s inline `$defs/annotation.review_states`
references `annotation_review.json` per PFS9-X2, extending the
tree-with-$ref pattern into the cross-boundary tier.

Labels on `event.json`'s `branches` field, event-id strings on
ArMythos / ArPhase, id-string arrays on StcStory / StcBeat /
StcStrand, and `CrossDialectRef.dialect` tokens in the
lowering namespace are all plain strings, not $ref-typed — see
production-format-sketch-05 §Open questions OQ3, sketch-06 OQ3,
sketch-07 OQ4, and sketch-09 PFS9-X4 (dialect-token openness
per architecture-sketch-02 A6) for the cross-reference-
consistency audit surfaces.

## What's deferred

- Remaining dialect records (Dramatic, Dramatica-complete;
  `ArObservation` for Aristotelian; `StcObservation` +
  `StcCanonicalBeat` + `StcGenre` for Save-the-Cat). Each
  dialect or record group needs its own production-format
  sketch; Aristotelian-core (three records) shipped under PFS6
  as the first dialect-layer example; Save-the-Cat-core (four
  records) shipped under PFS7 as the second.
- Verification-family cross-boundary records
  (VerificationReview, StructuralAdvisory,
  VerificationAnswerProposal, VerifierCommentary). PFS10 ships
  these under `schema/verification/` after PFS9's
  CrossDialectRef decision (re-inlined per PFS8-V guidance).
- Dialect-internal observation / review / probe records
  (ArObservation, ArAnnotationReview, ArObservationCommentary,
  DialectReading, StcObservation, future DramaticaObservation).
  Ship under existing dialect namespaces per PFS8-N2
  (PFS11 Aristotelian batch, PFS12 Save-the-Cat observation,
  future Dramatic+Dramatica-complete).
- Runtime / ephemeral records (CheckRegistration, CoverageGap,
  DroppedOutput, three ReaderModelResult containers) — named
  in PFS8-X with forcing-function criteria. Not scheduled.
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
