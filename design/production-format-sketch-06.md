# Production format — sketch 06

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (new topic: dialect-layer schema arc,
first under the dialect-stack portion of architecture-sketch-02
to ship production-layer artifacts)
**Frames:** [aristotelian-sketch-01](aristotelian-sketch-01.md)
A1 (ArMythos primary record), A2 (ArPhase logical divisions), A3
(simple/complex plot kind), A5 (ArCharacter + cross-dialect hook),
A6 (three unities), A7 (self-verifier); [production-format-sketch-
01](production-format-sketch-01.md) PFS1 (JSON Schema 2020-12 as
substrate spec language), PFS2 (schemas-first / Python-as-
conformance); [production-format-sketch-03](production-format-
sketch-03.md) PFS3-E1 (cross-file `$ref` via
`jsonschema.referencing.Registry`); [production-format-sketch-
05](production-format-sketch-05.md) §Open questions OQ3 (plain-
string event-id references); [architecture-sketch-02](
architecture-sketch-02.md) A6–A11 (dialect stack)
**Related:** [substrate-sketch-05](substrate-sketch-05.md) (the
substrate layer Mythos / Phase event-ids reference); [save-the-
cat-sketch-01](save-the-cat-sketch-01.md) + [sketch-02](save-the-
cat-sketch-02.md) (parallel non-Dramatica dialect; not yet
schema-ified but the precedent the next dialect-schema arc would
follow); [dramatic-sketch-01](dramatic-sketch-01.md) (third
dialect; also not yet schema-ified)
**Superseded by:** nothing yet

## Purpose

**First dialect production sketch.** Ships JSON Schema 2020-12
files for three Aristotelian core records — `ArMythos`,
`ArPhase`, `ArCharacter` — and commits the **dialect schema
namespace convention** that all future dialect-layer schemas
will follow.

Aristotelian is the natural first dialect: it is field-level-
specified by aristotelian-sketch-01 (A1–A9), its scope is
bounded (~3 authored record types at the core), the corpus
exists (Oedipus + Rashomon encodings, 5 ArMythos + 15 ArPhase +
6 ArCharacter records), and the dialect is architecturally
stable — no dialect-sketch-02 amendments have landed since
aristotelian-sketch-01 (contrast Save-the-Cat, which amended
once, and Dramatic, which has multiple pending forcing
functions named in dramatica-template-sketch-01's "Where the
dialect resists" section).

This sketch stays deliberately slim for the same reason
production-format-sketch-05 did: **the design sketch has
already done the structural work**. A1 ships ArMythos's field
list; A2 ships ArPhase's; A5 ships ArCharacter's. The work
here is format-rendering — re-expressing the three record
shapes in JSON Schema — plus a small number of architectural
commitments (schema namespace; cross-file `$ref` pattern; what
the `plot_kind="complex"` → peripeteia/anagnorisis conditional
looks like as an `allOf/if-then-else`).

## Why now

- **Substrate schema layer is structurally complete** (state-
  of-play-08's headline). Every substrate record named in
  substrate-sketch-04 / substrate-sketch-05 has a matching
  schema file; `production-format-sketch-06` lifts the PFS
  discipline to the first layer *above* the substrate.
- **Dialect layer is the next-up-the-stack tier.** Three
  dialects exist with authored records (Dramatic, Save-the-
  Cat, Aristotelian); Aristotelian is smallest.
- **`production-format-sketch-06`'s precedents close cleanly
  over the needed primitives.** Cross-file `$ref` was
  established for the substrate layer (PFS3-E1 via
  `jsonschema.referencing.Registry`, extended by PFS4). The
  conditional-field pattern (`allOf/if-then-else`) was
  established by PFS5 for Branch's kind-conditional parent.
  Plain-string cross-record refs (no $ref-typing of event-id
  strings) was established by PFS5-B3 / PFS5 OQ3.
- **No conformance dispositions on the substrate side.**
  Description corpus reaches zero findings (sketch-08 arc 1).
  The dialect arc does not inherit a backlog.

## Scope — what the sketch covers

**In:**

- Three JSON Schema files for Aristotelian core records:
  - `schema/aristotelian/mythos.json` (ArMythos per A1).
  - `schema/aristotelian/phase.json` (ArPhase per A2).
  - `schema/aristotelian/character.json` (ArCharacter per A5).
- The **dialect schema namespace convention**:
  `schema/<dialect>/<record>.json` subdirectory-per-dialect
  (PFS6-N1).
- Cross-file `$ref` structure for ArMythos's `phases` (refs
  phase.json) and `characters` (refs character.json) fields
  (PFS6-M8, PFS6-X1).
- The `plot_kind="complex"` → peripeteia-or-anagnorisis
  conditional via `allOf/if-then-else` (PFS6-M6).
- Dump-layer helpers: `_dump_armythos`, `_dump_arphase`,
  `_dump_archaracter` (PFS6-D1..D3) + an encoding-discovery
  helper (PFS6-D4).
- Conformance-test extension: three new schema-shape tests,
  three new corpus conformance tests.
- `schema/README.md` sweep: the "What's here" section gains a
  dialect-layer subsection; "What's deferred" updated.

**Out:**

- `ArObservation`. Parallel to the cross-boundary verifier-
  output records (VerifierCommentary, StructuralAdvisory,
  etc.) that state-of-play-08 grouped under "Production C —
  Cross-boundary record schemas." Ships as part of that arc,
  not here. Rationale: ephemeral verifier output; no authored
  corpus; natural batch-partner with the dialect-agnostic
  verifier-output surface.
- `ArAnnotationReview`, `ArObservationCommentary`,
  `DialectReading`. Cross-boundary probe/review records;
  Production C territory.
- Cross-dialect Lowering (Aristotelian ↔ Dramatic ↔ substrate)
  per aristotelian-sketch-01 A9. Lowering record schema is a
  Production C concern anyway.
- Save-the-Cat / Dramatic dialect schemas. Separate per-
  dialect production sketches; each earns its shape by its
  own corpus and design sketch.
- `ArMythosRelation` or other aristotelian-sketch-02 candidate
  extensions. Banked until forced.

## Commitments

### PFS6-N1 — Dialect schemas live under `schema/<dialect>/`

Every schema under this sketch ships under a dialect-specific
subdirectory: `schema/aristotelian/mythos.json`,
`schema/aristotelian/phase.json`,
`schema/aristotelian/character.json`.

**Precedent set.** Future dialect-schema arcs (Save-the-Cat,
Dramatic, Dramatica-complete) will land their records under
`schema/save_the_cat/`, `schema/dramatic/`,
`schema/dramatica_complete/` respectively.

**Rationale.**

- **Namespacing.** Each dialect has its own record type
  vocabulary; flat layout at `schema/` would collide on common
  names (Character / Phase / Observation are plausible
  multi-dialect names).
- **Visual separation.** `schema/` + `schema/aristotelian/`
  side-by-side makes the substrate/dialect layering obvious
  in a directory listing.
- **`$id` URI structure.** The `$id` URI follows the file
  path — `https://brazilofmux.github.io/story/schema/
  aristotelian/mythos.json` — so the path encodes the dialect
  name. Ports and external tools can route by URL prefix.
- **Conformance loader cost.** Negligible: the conformance
  test loads each schema by explicit relative path, not via
  directory walk. Subdirs add one pathjoin call per schema.

**Dialect name tokens.** Use the underscore-free dialect name
(`aristotelian`, not `Aristotelian` or `ar`), matching the
Python module naming. Multi-word dialects (`save_the_cat`) use
underscores, matching the Python module naming.

### PFS6-P1..P5 — Phase record shape

`schema/aristotelian/phase.json` ships the ArPhase record per
aristotelian-sketch-01 A2.

- **PFS6-P1.** Required fields: `id`, `role`,
  `scope_event_ids`.
- **PFS6-P2.** `id` is a non-empty string. No prefix
  convention enforced (sketch-convention uses `ph_*` but this
  is descriptive, not normative — same posture as PFS5-B3 on
  Branch labels).
- **PFS6-P3.** `role` is a **closed enum** at three values:
  `{"beginning", "middle", "end"}`. Per A2 — these are the
  three logical divisions of the mythos; additional role
  names would be a dialect amendment, not a record-shape
  authoring choice.
- **PFS6-P4.** `scope_event_ids` is an array of non-empty
  strings. Empty array is legal (a phase may exist as
  scaffolding before events are authored; the self-verifier
  will surface it); the schema admits it. **Plain-string
  references** per PFS5 OQ3 — `scope_event_ids` items are
  not `$ref`-typed to event.json.
- **PFS6-P5.** `annotation` is an optional string (default
  `""` in the Python record; schema admits absence as well
  as empty string, consistent with PFS1's treatment of
  string-defaults).
- **`additionalProperties: false`.** Per PFS1 strict-shape
  convention.

### PFS6-C1..C5 — Character record shape

`schema/aristotelian/character.json` ships the ArCharacter
record per aristotelian-sketch-01 A5.

- **PFS6-C1.** Required fields: `id`, `name`.
- **PFS6-C2.** `id` is a non-empty string. `name` is a non-
  empty string.
- **PFS6-C3.** `character_ref_id` is an **optional non-empty
  string** — the cross-dialect identity hook per A5. Admits
  substrate Entity ids (e.g., `"oedipus"`) and Dramatic
  Character ids (e.g., `"c_macbeth"`). **Plain-string
  reference, not `$ref`-typed.** The cross-dialect-consistency
  audit surface is OQ3 below (parallel to PFS5 OQ3).
- **PFS6-C4.** `hamartia_text` is an optional string — author
  prose per A5. No length constraint.
- **PFS6-C5.** `is_tragic_hero` is an optional boolean,
  default `false` per the Python record. Schema admits
  absence; defaulting to false is a Python-side concern, not
  a schema concern (PFS1 + PFS3 established this).
- **`additionalProperties: false`.**

### PFS6-M1..M8 — Mythos record shape

`schema/aristotelian/mythos.json` ships the ArMythos record
per aristotelian-sketch-01 A1. The primary record of the
dialect; the largest of the three schemas.

- **PFS6-M1.** Required fields: `id`, `title`,
  `action_summary`, `central_event_ids`, `plot_kind`,
  `phases`.
- **PFS6-M2.** `id`, `title`, `action_summary` are non-empty
  strings.
- **PFS6-M3.** `central_event_ids` is a non-empty array of
  non-empty strings. **Plain-string references** per PFS5
  OQ3. Must be non-empty: a mythos with zero events violates
  A1's "arrangement of incidents" — there must be at least
  one incident.
- **PFS6-M4.** `plot_kind` is a **closed enum** at two values:
  `{"simple", "complex"}`. Per A3.
- **PFS6-M5.** `phases` is a non-empty array of Phase records
  via `$ref` to `schema/aristotelian/phase.json`. Minimum one
  phase; the self-verifier (A7 unity of action) checks
  phase-coverage; the schema enforces the minimum but leaves
  coverage to the verifier.
- **PFS6-M6.** **`plot_kind="complex"` conditional** via
  `allOf/if-then-else`: if `plot_kind == "complex"`, at
  least one of `peripeteia_event_id` / `anagnorisis_event_id`
  is required (per A3 + A7 check 1). Expressed as:

  ```json
  "allOf": [{
    "if": { "properties": { "plot_kind": { "const": "complex" } },
             "required": ["plot_kind"] },
    "then": {
      "anyOf": [
        { "required": ["peripeteia_event_id"] },
        { "required": ["anagnorisis_event_id"] }
      ]
    }
  }]
  ```

  **Precedent.** PFS5-B5 established the `allOf/if-then-else`
  pattern for Branch's kind-conditional parent; this sketch
  extends it to an `anyOf`-in-then shape. Same structural
  commitment; different semantics.

- **PFS6-M7.** Four optional event-id pointer fields —
  `complication_event_id`, `denouement_event_id`,
  `peripeteia_event_id`, `anagnorisis_event_id` — are
  optional non-empty strings. Plain-string references (PFS5
  OQ3 posture).
- **PFS6-M8.** Three boolean unity-assertion fields —
  `asserts_unity_of_action`, `asserts_unity_of_time`,
  `asserts_unity_of_place` — are optional booleans. Python
  defaults are `(True, False, False)` per A6; schema admits
  presence or absence.
- **PFS6-M9.** Two bound fields — `unity_of_time_bound`
  (integer, Python default 24) and `unity_of_place_max_
  locations` (integer, Python default 1) — are optional
  integers. Only load-bearing when the corresponding
  `asserts_*` is true; schema does not enforce the
  conditional (the self-verifier reads them when asserted).
- **PFS6-M10.** `aims_at_catharsis` is an optional boolean,
  Python default `True`. Per A8, this is an authorial claim
  with no verifier check; the schema admits the field but
  assigns no special semantics.
- **PFS6-M11.** `characters` is an optional array of
  Character records via `$ref` to
  `schema/aristotelian/character.json`. Empty array is legal
  (a mythos without Aristotelian-dialect characters is
  valid — characters may live on the Dramatic side only, or
  be elided for short-form probes); defaults to empty tuple
  in Python.
- **`additionalProperties: false`.**

### PFS6-X1 — Cross-file `$ref` extends to the dialect layer

The substrate schema layer established cross-file `$ref` via
`jsonschema.referencing.Registry` (PFS3-E1; extended by PFS4
for Held). This sketch extends the pattern across the
substrate/dialect boundary (if needed) and within the dialect
(for Phase and Character):

- `schema/aristotelian/mythos.json` references
  `schema/aristotelian/phase.json` via `$ref` at
  `properties.phases.items`.
- `schema/aristotelian/mythos.json` references
  `schema/aristotelian/character.json` via `$ref` at
  `properties.characters.items`.
- **No outbound cross-file `$ref` from the dialect layer
  into substrate schemas today.** Event-id references are
  plain strings; cross-layer consistency is PFS5 OQ3's audit
  surface (OQ3 below lifts it to the dialect layer). A future
  sketch may `$ref`-type event-id cross-references if a
  forcing function argues for it; today none does.

The conformance test's `_build_schema_registry` is extended
(PFS6-D5 below) to register phase.json and character.json so
mythos.json's `$ref`s resolve.

### PFS6-X2 — No event-id `$ref` at the dialect layer

Event-id strings on ArMythos (central, complication, denouement,
peripeteia, anagnorisis) and on ArPhase (scope_event_ids) are
**not** `$ref`-typed to event.json. They are plain non-empty
strings.

**Consistency with PFS5.** PFS5-B3 took the same posture for
Branch labels vs. event.branches string arrays, banking the
cross-reference consistency audit as PFS5 OQ3. This sketch
applies the same posture to dialect-layer event-id references;
the audit surface lifts to OQ3 below.

**Why not `$ref`-typed today.** JSON Schema's `$ref` describes
*shape* conformance, not *referential integrity*. A typed
`"$ref": "event.json"` on `central_event_ids[*]` would admit
any string the event.json's top-level shape accepts — which is
an object, not an id string. Typed cross-references require
either an `$id` anchor of the form `#/event-id-string` or a
separate schema-extension mechanism (e.g., JSON Schema's
unevaluated feature plus a custom vocabulary). Neither today.

**Non-finding.** Every event-id string in the corpus resolves
to a real substrate event at conformance-test time (the A7
self-verifier's check 4 — event-ref integrity — does the
resolution). Schema + verifier together carry the guarantee;
schema alone does not.

## Dump-layer commitments

Parallel to PFS5-D1/D2 for Branch.

### PFS6-D1 — `_dump_armythos(mythos: ArMythos) -> dict`

Field-for-field isomorphic to Python ArMythos. Empty-tuple
`characters` emits as empty array; optional None-valued
pointer fields (`complication_event_id` etc.) are **omitted**,
not emitted as `null`. Omission matches the schema's "optional
means may-be-absent" posture.

### PFS6-D2 — `_dump_arphase(phase: ArPhase) -> dict`

Field-for-field. `annotation=""` default emits as an empty
string (not omitted) because the Python record's default is a
string literal, not None — the presence-vs-absence distinction
is not semantically meaningful for annotation.

### PFS6-D3 — `_dump_archaracter(character: ArCharacter) -> dict`

Field-for-field. Optional `character_ref_id` and
`hamartia_text` omitted when None.

### PFS6-D4 — `_discover_encoding_aristotelian(modules: list)`

Returns a triple `(mythoi, phases, characters)` — three lists —
by walking encoding modules. Aristotelian encodings export
either `AR_*_MYTHOS` singletons (Oedipus) or `AR_*_MYTHOI`
tuples (Rashomon). The discovery helper handles both:

- Pull any module-level attribute starting with `AR_` that is
  an `ArMythos` or a tuple of `ArMythos`.
- Collect all phases reached through each mythos's `phases`
  tuple (deduplicate by id; Oedipus's three phases might
  appear via `AR_OEDIPUS_MYTHOS.phases` only).
- Collect all characters reached through each mythos's
  `characters` tuple (deduplicate by id).

Dedup is by id (as an equality heuristic). Same-id records
across encodings are a corpus-authoring concern, not a
discovery concern.

### PFS6-D5 — Registry registration

The conformance test's `_build_schema_registry` gains three
new entries: phase.json, character.json, mythos.json — in
registration order so each schema can resolve `$ref`s
outbound.

## Conformance dispositions (anticipated)

No active dispositions anticipated. Three **anticipated non-
findings**:

1. **`annotation` field default is `""` in Python; schema
   admits empty string cleanly.** Empty string validates
   against `type: string`; no special handling needed.
2. **`unity_of_time_bound` / `unity_of_place_max_locations`
   present when their corresponding `asserts_*` is false.**
   The Python record always carries the default values (24
   and 1), so the dump emits them regardless of assertion
   state. Schema admits the integers unconditionally; verifier
   reads them only when the matching assertion is true. Non-
   finding: schema admits, verifier semantics handle the
   conditional.
3. **Rashomon's mythoi share characters across mythoi via
   `character_ref_id` to substrate entities, but the
   ArCharacter records are local to each mythos.**
   Specifically: `AR_RASHOMON_BANDIT.characters[0]`'s id may
   be `"ar_bandit"`, same as `AR_RASHOMON_WIFE.characters[1]`.
   The dump emits them independently; schema validates each
   independently. Duplicate-id deduplication is a corpus-
   authoring concern (not necessarily a bug — different
   mythoi authored different angles on the same dialogue-
   actor), not a schema conformance concern.

## Corpus expectations

- **ArMythos**: 5 records (1 Oedipus + 4 Rashomon).
- **ArPhase**: 15 records (3 Oedipus + 12 Rashomon; 4 mythoi
  × 3 phases each).
- **ArCharacter**: 6 records (2 Oedipus — Oedipus + Jocasta,
  both with substrate `character_ref_id`; 4 Rashomon — one
  per mythos).

Every corpus record expected to validate clean under the
implementation. If a non-finding materializes as a true
conformance issue, this sketch gains a §Dispositions section
(none anticipated).

## Open questions

1. **OQ1 — ArObservation schema + corpus-validation shape.**
   ArObservation is ephemeral verifier output; no authored
   corpus exists. A future Production C sketch — covering
   ArObservation, StcObservation, VerifierCommentary,
   StructuralAdvisory, VerificationReview, and the cross-
   boundary record shapes the probe-surface emits — is the
   natural home. OQ1 deferred until that arc opens.

2. **OQ2 — Save-the-Cat and Dramatic dialect schemas.**
   Parallel arcs. Save-the-Cat (sketch-01 + sketch-02) is
   field-level-detailed enough that a slim production sketch
   like this one would ship cleanly. Dramatic has open
   forcing functions (dramatica-template-sketch-01's "Where
   the dialect resists" lists six) that may argue for a
   dramatic-sketch-02 design-first arc before a production
   sketch lands. Timing decision.

3. **OQ3 — Dialect-layer event-id cross-reference consistency
   audit.** Parallel to PFS5 OQ3. Every event-id string on
   an ArMythos or ArPhase should resolve to a real substrate
   event in the same encoding. The A7 self-verifier's check
   4 does this at verify-time; a conformance-test-layer
   audit would extend it to validate-time. Forcing function:
   an encoding whose ArMythos references an event id absent
   from its substrate. No corpus case today; OQ lifted to
   this sketch from PFS5's surface to align the two.

4. **OQ4 — Cross-dialect `character_ref_id` audit.**
   ArCharacter's `character_ref_id` should resolve to either
   a substrate Entity id or a Dramatic Character id in the
   same encoding. Today the field is a plain string; the
   audit would be a second-layer check. Forcing function: an
   encoding where character_ref_id points at nothing.
   Oedipus's `"oedipus"` / `"jocasta"` both resolve to
   substrate entities; Rashomon's resolve the same way.
   Banked.

5. **OQ5 — `ArMythosRelation` or other aristotelian-sketch-02
   extensions.** If a dialect amendment lands (e.g., mythos-
   relation records for the Rashomon four-testimony case
   that aristotelian-sketch-01's stress case flagged), a
   production sketch at that point would amend PFS6's shape
   commitments or add new records. No forcing function today;
   sketch-01 §Stress case itself banked `ArMythosRelation` as
   sketch-02 territory.

## Discipline

Same-as-always under the PFS2 discipline:

- **Sketches before schema.** aristotelian-sketch-01 A1–A9
  did the design-layer work for the three records shipped
  here. PFS6 is pure format-rendering plus small number of
  schema-layer commitments (namespace; cross-file $ref
  pattern; conditional encoding of A3).
- **Schemas before code.** No Python change is anticipated
  (the Aristotelian dataclasses already match the shape A1/
  A2/A5 committed). If a conformance issue surfaces, the
  posture is the same as the substrate arcs: amend the
  design sketch first; then schema; then Python.
- **First-dialect sketch sets precedent for next-dialect
  sketch.** PFS6-N1 (namespace), PFS6-X1 (intra-dialect
  cross-file $ref), PFS6-X2 (no event-id $ref), PFS6-D1..D5
  (dump-layer pattern) carry forward. Save-the-Cat's
  production sketch (future OQ2) would cite PFS6 as its
  precedent, the way PFS5 cited PFS3.
- **Slim when the design is done.** Same discipline as
  PFS5. This sketch aims for ~500 lines; the Commitments
  section is longer than PFS5's because three records are
  shipped rather than one, not because more design
  derivation was needed.

## Summary

First dialect production sketch. Three JSON Schema files for
Aristotelian core records (ArMythos, ArPhase, ArCharacter)
shipped under a new `schema/aristotelian/` subdirectory.
Eleven commitments:

- **PFS6-N1** — dialect schema namespace (`schema/<dialect>/`
  subdir).
- **PFS6-P1..P5** — Phase shape (required id/role/scope_
  event_ids; role enum; scope is plain-string array;
  annotation optional default-empty).
- **PFS6-C1..C5** — Character shape (required id/name;
  optional ref-id / hamartia / tragic-hero; ref-id is plain
  string).
- **PFS6-M1..M11** — Mythos shape (primary record; `allOf/
  if-then-else` for complex-plot peripeteia-or-anagnorisis;
  `$ref` for phases and characters arrays).
- **PFS6-X1** — cross-file `$ref` extends to dialect layer.
- **PFS6-X2** — no event-id `$ref`; plain-string references
  consistent with PFS5 OQ3.

Four open questions banked with forcing functions: ArObservation
+ cross-boundary record shapes (OQ1, Production C); next-dialect
schemas (OQ2); event-id audit surface (OQ3); character-ref-id
audit (OQ4); sketch-02 extensions (OQ5).

No design derivation needed. Aristotelian-sketch-01 already
committed the record shapes; this sketch renders them as JSON
Schema 2020-12, commits the namespace convention, and hands
off to implementation.

Python untouched at the sketch layer. Dump-layer + discovery
+ test-suite extensions land in the implementation commit.
Substrate schema layer remains structurally complete; dialect
schema layer begins.
