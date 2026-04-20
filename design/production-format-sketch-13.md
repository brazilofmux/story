# Production format — sketch 13

**Status:** draft, active
**Date:** 2026-04-20
**Supersedes:** nothing (fifth per-record arc under Production C;
ships the three sketch-02 Aristotelian dialect-extensions —
`ArMythosRelation`, `ArAnagnorisisStep`, and three new optional
`ArMythos` fields — under the existing `schema/aristotelian/`
namespace committed by PFS6-N1, per PFS8-N2's classification that
dialect-internal records live in the dialect's namespace)
**Frames:** [production-format-sketch-06](production-format-
sketch-06.md) PFS6-N1 (Aristotelian namespace), PFS6-X1 (intra-
namespace cross-file `$ref` pattern), PFS6-M1..M11 (ArMythos
shape — PFS13 extends); [production-format-sketch-08](production-
format-sketch-08.md) PFS8-N2 (dialect-internal records stay under
`schema/<dialect>/`); [production-format-sketch-11](production-
format-sketch-11.md) PFS11-N1 (first arc to exercise PFS8-N2 under
`schema/aristotelian/`), PFS11-X2 (same-namespace `$ref` template);
[production-format-sketch-01](production-format-sketch-01.md) PFS1
(JSON Schema 2020-12), PFS2 (schemas-first); [production-format-
sketch-03](production-format-sketch-03.md) PFS3-E1 (cross-file
`$ref` via registry); [aristotelian-sketch-02](aristotelian-
sketch-02.md) A10 (`ArMythosRelation`), A11 (`ArAnagnorisisStep` +
`anagnorisis_chain`), A12 (`peripeteia_anagnorisis_binding` +
`peripeteia_anagnorisis_adjacency_bound`), AA11 (schema-layer
landing deferred to a follow-on PFS arc); [aristotelian-sketch-
02](aristotelian-sketch-02.md) §Open questions OQ6 (schema-layer
shape decision — own-file vs inline into `mythos.json`; settled
here as own-file).
**Related:** [architecture-sketch-02](architecture-sketch-02.md)
A7/A8 (dialect-internal records); [aristotelian-probe-sketch-
01](aristotelian-probe-sketch-01.md) (the probe runs that forced
A10–A12); [aristotelian-probe-sketch-02](aristotelian-probe-
sketch-02.md) (closure verification after sketch-02 landed);
[aristotelian-probe-sketch-03](aristotelian-probe-sketch-03.md)
(generalization test — Macbeth exercises A11 non-precipitating
step polarity + A12 BINDING_COINCIDENT cell; both verified
structurally load-bearing under probe reading)
**Superseded by:** nothing yet

## Purpose

**Fifth per-record sketch under Production C.** Ships two JSON
Schema 2020-12 files for the Aristotelian sketch-02 dialect
extensions — `ArMythosRelation` and `ArAnagnorisisStep` — under
the existing `schema/aristotelian/` namespace PFS6-N1 committed,
AND amends `schema/aristotelian/mythos.json` to admit the three
new optional fields A11 + A12 add to `ArMythos`
(`anagnorisis_chain`, `peripeteia_anagnorisis_binding`,
`peripeteia_anagnorisis_adjacency_bound`). Per PFS8-N2: dialect-
extensions that live on the dialect's own records ship under the
dialect's namespace.

The per-record design work is already done. Aristotelian-sketch-
02 commits both new records' shapes (A10, A11) and the three
new `ArMythos` fields (A11, A12), with invariants pinned by A7.6–
A7.9. The corpus carries the first instances today: Rashomon's
`AR_RASHOMON_CONTEST` (A10); Oedipus's `AR_STEP_JOCASTA` + Macbeth's
`AR_STEP_LADY_MACBETH_SLEEPWALKING` (A11); Oedipus declares
`peripeteia_anagnorisis_binding="separated"`, Macbeth declares
`"coincident"` (A12). This sketch format-renders the three
extensions at the schema layer; no new field-level commitments.

## Why now

- **Second per-record arc under Production C to ship under
  `schema/aristotelian/`.** PFS11 landed the four Aristotelian
  cross-boundary records (observation, annotation review,
  observation commentary, dialect reading). PFS13 is the first
  arc to *amend* an existing dialect-core schema (`mythos.json`)
  plus add sibling records that live on the same dialect. Same
  namespace, different shape-pressure: PFS11 extended the
  namespace outward (four new files); PFS13 both extends the
  namespace (two new files) and deepens the existing top-level
  record (three new fields on `ArMythos`).
- **AA11's deferral closes.** Aristotelian-sketch-02 AA11
  explicitly named "a follow-on production-format arc" as the
  home for A10–A12 schema landing. That arc is this one. OQ6's
  "own file vs inline" decision settles in favor of own-file —
  consistent with every prior aristotelian arc (`phase.json`,
  `character.json`, `observation.json` each ship as dedicated
  single-record schemas).
- **Corpus exists (non-zero on every axis).** Three Aristotelian
  encodings contribute sketch-02 records today:
  - `ArMythosRelation`: 1 record (Rashomon's
    `AR_RASHOMON_CONTEST`).
  - `ArAnagnorisisStep`: 2 records (Oedipus's `AR_STEP_JOCASTA`;
    Macbeth's `AR_STEP_LADY_MACBETH_SLEEPWALKING`). Two
    polarities: `precipitates_main=True` (Jocasta triggers
    Oedipus's main anagnorisis); `precipitates_main=False` (Lady
    Macbeth's sleepwalking recognition is non-causal vs. the
    main anagnorisis at `E_macduff_reveals_birth`).
  - `peripeteia_anagnorisis_binding`: 2 mythoi
    (`BINDING_SEPARATED` for Oedipus; `BINDING_COINCIDENT` for
    Macbeth). `"adjacent"` uncovered in the corpus — shape
    validated via the schema's enum at sketch time.
  Every new shape exercises the validator on first ship.
- **Probe-pressure closed, not growing.** Aristotelian-probe-
  sketch-03's generalization test confirmed A11 / A12 both work
  on Macbeth (new-to-corpus polarities cited structurally by
  probe); the closure ledger is stable. Schema landing rides
  that stability — nothing in A10–A12 is likely to churn before
  a sketch-03 amendment.

## Scope — what the sketch covers

**In:**

- Two new JSON Schema files under `schema/aristotelian/`:
  - `schema/aristotelian/mythos_relation.json`
    (`ArMythosRelation` per aristotelian-sketch-02 A10).
  - `schema/aristotelian/anagnorisis_step.json`
    (`ArAnagnorisisStep` per aristotelian-sketch-02 A11).
- **Amendment to `schema/aristotelian/mythos.json`**: three new
  optional properties — `anagnorisis_chain` (array of `$ref` to
  `anagnorisis_step.json`), `peripeteia_anagnorisis_binding`
  (closed enum), `peripeteia_anagnorisis_adjacency_bound`
  (integer).
- **Cross-file `$ref` from `mythos.json` to
  `anagnorisis_step.json`** for the `anagnorisis_chain` items.
  Extends PFS6-X1's intra-namespace cross-file pattern to a
  fourth reference inside `schema/aristotelian/` (mythos →
  phase; mythos → character; observation_commentary →
  observation; mythos → anagnorisis_step).
- Dump-layer helpers: `_dump_ar_mythos_relation`,
  `_dump_ar_anagnorisis_step`, and an extension to
  `_dump_armythos` to emit the three new fields.
- Discovery helper for `ArMythosRelation`:
  `_discover_encoding_aristotelian_relations()` — walks encoding
  modules for `AR_*_RELATIONS` tuples at module scope. Parallels
  the `AR_*_MYTHOI` discovery in `_discover_encoding_
  aristotelian_records()`. `ArAnagnorisisStep` records are
  reached *transitively* through each mythos's
  `anagnorisis_chain` tuple, parallel to how `ArPhase` and
  `ArCharacter` are reached through `mythos.phases` and
  `mythos.characters` — no new top-level discovery path needed.
- Registry registration: two new entries
  (`mythos_relation.json`, `anagnorisis_step.json`).
- Six new conformance tests:
  - 2 metaschema (one per new schema file).
  - 2 shape (one per new schema file).
  - 2 corpus (one per new record kind).
  Plus an extension to the existing
  `test_aristotelian_mythos_schema_has_expected_shape` test for
  the three new `mythos.json` properties.

**Out (banked with forcing functions):**

- **Close-enum on `ArMythosRelation.kind`.** A10's canonical
  kinds are `{"contests", "parallel", "contains"}` with open-
  string admittance at severity=noted (A7.6 check 1). Schema
  admits open non-empty string per A10's canonical-plus-open
  discipline; a close-enum commitment would contradict the
  authorial surface's "experiment without dialect update"
  posture. Parallel to PFS7 `role_labels` vocabulary and PFS11-
  AO3 observation code. Banked as **OQ1**.
- **Referential integrity audits on `ArMythosRelation.mythoi_ids`
  and `ArMythosRelation.over_event_ids`.** Both resolve at
  verification time (A7.6 check 2; A7.9). The schema admits any
  non-empty string tuple; existence is not checked. A later
  Tier-2 audit (per referential-integrity-sketch-NN) extends
  coverage. Parallel to PFS11 OQ3 / PFS12 OQ2. Banked as
  **OQ2**.
- **Referential integrity audit on
  `ArAnagnorisisStep.event_id` and `character_ref_id`.** Both
  resolve at verification time (A7.7 invariants 1 + 5). Same
  bank as OQ2. Banked as **OQ3**.
- **`peripeteia_anagnorisis_adjacency_bound` default at schema
  level.** Python carries the default `3`; schema declares the
  property as `"integer"` without a default, matching the
  `unity_of_time_bound` (default 24) and
  `unity_of_place_max_locations` (default 1) pattern already in
  `mythos.json`. A schema-level default would surface the
  authorial-unoverridden case at validator time rather than
  silent Python-defaulting. Deferred: the authoring experience
  favors field-presence explicitness in Python; a later arc
  with a cross-namespace default-handling convention would
  lift this uniformly (not just for this one field). Banked as
  **OQ4**.

**Not the topic:**

- **No Python change.** The `ArMythosRelation` dataclass,
  `ArAnagnorisisStep` dataclass, and the three new `ArMythos`
  fields all exist in `core/aristotelian.py` today (landed
  under AA6 from sketch-02). PFS2 discipline: schema shape is
  source of truth; Python conforms. No divergences anticipated
  — Python docstrings directly cite the sketch-02 shapes.
- **No sketch-02 semantics changes.** PFS13 format-renders the
  sketch-02 commitments; A7.6–A7.9 invariants remain enforced
  by the Python verifier. Schema catches shape violations
  (missing required field; wrong enum value); the verifier
  catches semantic violations (a step that precipitates without
  a main anagnorisis; a relation kind outside the canonical set).
- **No changes to `observation.json`.** A7.6–A7.9 added new
  observation codes under sketch-02's AA7; the schema's
  observation-code field admits any non-empty string per PFS11-
  AO3, so new codes don't require a schema amendment.
- **No `ArMythosRelation` at a higher scope.** Relations live
  within an encoding (per A10 placement discussion). No cross-
  encoding / cross-dialect relation shape ships here.

## Commitments

### PFS13-N1 — Namespace inherits PFS6-N1

The two new schemas live under `schema/aristotelian/` — the
dialect's existing namespace. No new top-level subdirectory.
Per PFS8-N2: dialect-internal records (the Aristotelian dialect's
own extension records, produced by authors in Aristotelian
encoding modules) share the namespace with the dialect's core
records (`mythos` / `phase` / `character` / `observation`).

This is the **third** arc under `schema/aristotelian/` (PFS6
shipped three core schemas; PFS11 shipped four cross-boundary
schemas; PFS13 ships two new-and-extension schemas — eight
namespaced schemas total after landing).

`$id` URIs:

- `https://brazilofmux.github.io/story/schema/aristotelian/mythos_relation.json`
- `https://brazilofmux.github.io/story/schema/aristotelian/anagnorisis_step.json`

### PFS13-MR1..MR4 — ArMythosRelation record shape

`schema/aristotelian/mythos_relation.json` ships the
`ArMythosRelation` record per aristotelian-sketch-02 A10. Encoding-
scope record (tupled as `AR_*_RELATIONS` at module level;
Rashomon is the first encoding to author one).

- **PFS13-MR1.** Required fields: `id`, `kind`, `mythoi_ids`.
  `over_event_ids` and `annotation` optional. Mirrors A10's
  dataclass: `id` / `kind` / `mythoi_ids` are required;
  `over_event_ids: Tuple[str, ...] = ()` and `annotation: str = ""`
  have Python defaults.
- **PFS13-MR2.** `kind` is an **open non-empty string**.
  Canonical vocabulary `{"contests", "parallel", "contains"}` is
  the authorial surface; A7.6 check 1 emits `severity=noted`
  for non-canonical values. Per A10's canonical-plus-open
  discipline (parallel to PFS7 `role_labels`), schema admits
  any non-empty string without close-enum. Close-enum deferred
  to OQ1.
- **PFS13-MR3.** `mythoi_ids` is an **array of non-empty strings
  with `minItems: 2`**. A10 requires at least two mythoi; A7.6
  check 2 separately enforces mythos-id resolution at
  verification time. The schema enforces cardinality at shape
  time.
- **PFS13-MR4.** `over_event_ids` is an **array of non-empty
  strings** (no `minItems` — empty tuple is the Python default
  and is valid per A10, though only non-empty arrays
  structurally support A7.6 check 3 for `kind="contests"`).
  `annotation` is an **open string** (no `minLength` — empty
  string is the Python default).
- **`additionalProperties: false`.**

### PFS13-AS1..AS4 — ArAnagnorisisStep record shape

`schema/aristotelian/anagnorisis_step.json` ships the
`ArAnagnorisisStep` record per aristotelian-sketch-02 A11. Sub-
record of `ArMythos` — reached via `anagnorisis_chain`; not
authored at encoding scope today (mirrors `ArPhase` and
`ArCharacter` living inside their enclosing mythos).

- **PFS13-AS1.** Required fields: `id`, `event_id`,
  `character_ref_id`. `precipitates_main` and `annotation`
  optional. Mirrors A11's dataclass: the first three are
  required (A11's "character_ref_id is required, not optional"
  is load-bearing — an anonymous step is audience-level, which
  sketch-02 rejects); `precipitates_main: bool = False` and
  `annotation: str = ""` have Python defaults.
- **PFS13-AS2.** `id`, `event_id`, `character_ref_id` are all
  **non-empty strings**. Plain-string references per PFS6-X2 —
  resolution (event_id in enclosing mythos's central_event_ids;
  character_ref_id in enclosing mythos's characters) is A7.7's
  job, not the schema's.
- **PFS13-AS3.** `precipitates_main` is **boolean**. No schema-
  level default (following the `asserts_unity_of_*` precedent
  in `mythos.json`: Python carries defaults; schema declares
  types without defaults). Python default is `False`.
- **PFS13-AS4.** `annotation` is an **open string**. No
  `minLength` — empty string is the Python default.
- **`additionalProperties: false`.**

### PFS13-M12..M14 — mythos.json amendment

Three new optional properties on `ArMythos`:

- **PFS13-M12.** `anagnorisis_chain` — an **array** of items
  each `$ref`-ing `anagnorisis_step.json`. No `minItems`: empty
  array is the Python default; pre-sketch-02 encodings carry
  no chain. Cross-file `$ref` per PFS13-X (below).
- **PFS13-M13.** `peripeteia_anagnorisis_binding` — a **closed
  enum** at three values: `{"coincident", "adjacent",
  "separated"}`. `None` is represented via field-absence
  (consistent with every other optional string field in
  `mythos.json` — `complication_event_id`,
  `denouement_event_id`, `peripeteia_event_id`,
  `anagnorisis_event_id`). A12 names these three canonical
  values; unknown values are rejected at shape time. (This
  contrasts with A7.8's runtime `peripeteia_anagnorisis_binding_
  invalid_value` observation, which catches Python-level
  misvalues that bypass the schema — the schema is now the
  first line of defense.)
- **PFS13-M14.** `peripeteia_anagnorisis_adjacency_bound` —
  an **integer**, no schema-level default (per OQ4). Python
  default is `3`; schema admits any integer.

All three fields are **optional** (not added to `required`).
Backward compatibility with pre-sketch-02 mythoi is preserved —
Oedipus and Macbeth are the only mythoi in the corpus that
declare any of the three today; Rashomon's four mythoi and
Oedipus's / Macbeth's pre-sketch-02 state validate identically.

### PFS13-X — Cross-file `$ref` to anagnorisis_step.json

`mythos.json`'s `anagnorisis_chain` property uses `$ref` to
`https://brazilofmux.github.io/story/schema/aristotelian/anagnorisis_step.json`.

**Same-namespace cross-file `$ref` reasoning** parallel to
PFS6-X1's `mythos → phase` and `mythos → character`:

1. **Size and stability.** `ArAnagnorisisStep` is a small record
   (five fields, no nested structure). Re-inlining would be
   feasible. But the namespace already holds three records
   cross-referencing each other (mythos → phase; mythos →
   character; observation_commentary → observation); adding
   mythos → anagnorisis_step is a one-liner under the established
   pattern. `$ref` scales without duplication pressure.
2. **Same-namespace resolution.** Reference stays within
   `schema/aristotelian/`; PFS8-V's cross-namespace-coupling
   concern doesn't apply. Same pattern PFS11-X2 used for
   observation_commentary → observation.

The registry pattern (PFS3-E1 → PFS4 P4A1 → PFS6-D5 → PFS9-D8
→ PFS10-D6 → PFS11-D6 → PFS12-D3) resolves it.

### PFS13-X2 — No CrossDialectRef

Neither new record carries a `CrossDialectRef`. Rationale:

- `ArMythosRelation.mythoi_ids` and `over_event_ids` resolve to
  intra-dialect ids (other mythoi in the encoding) and
  substrate event ids (plain-string per PFS6-X2). No dialect
  token needed at the schema layer.
- `ArAnagnorisisStep.event_id` and `character_ref_id` resolve
  to intra-dialect / substrate ids under A7.7's invariants —
  again, plain-string per PFS6-X2.

PFS13 is the third Production-C arc to ship without touching
CrossDialectRef, after PFS11 and PFS12. The same dialect-internal
routing rule applies: records produced by the dialect on behalf
of the dialect's own extensions don't need cross-dialect
identification.

## Dump-layer commitments

Parallel to PFS6-D1..D3 for Aristotelian core.

### PFS13-D1 — `_dump_ar_mythos_relation(rel) -> dict`

Field-for-field isomorphic. Required fields always emit
(`id`, `kind`, `mythoi_ids`). Tuple fields always emit as
arrays (empty tuple → empty array), matching PFS6-D2's
`_dump_armythos` convention for `characters` and `phases` —
`over_event_ids` emits even when empty. Optional string
`annotation` omits when empty, matching the `ArPhase.annotation`
/ `ArCharacter.hamartia_text` omit-when-empty discipline.

### PFS13-D2 — `_dump_ar_anagnorisis_step(step) -> dict`

Field-for-field isomorphic. Required fields always emit
(`id`, `event_id`, `character_ref_id`). `precipitates_main`
always emits (dataclass always carries a boolean, following
the `asserts_unity_of_*` precedent in `_dump_armythos`).
`annotation` omits when empty (matching `ArPhase.annotation`).

### PFS13-D3 — `_dump_armythos` extension

Three new conditional emissions:

- `anagnorisis_chain: [ _dump_ar_anagnorisis_step(s) for s in
  mythos.anagnorisis_chain ]` — always emitted (matching
  `phases` and `characters` which always emit as arrays).
- `peripeteia_anagnorisis_binding: mythos.peripeteia_anagnorisis_binding`
  — emitted when non-None, omitted when None (matching the
  four existing optional-string fields in `_dump_armythos`).
- `peripeteia_anagnorisis_adjacency_bound: mythos.peripeteia_
  anagnorisis_adjacency_bound` — always emitted (matching
  `unity_of_time_bound` and `unity_of_place_max_locations`
  which always emit regardless of default).

### PFS13-D4 — `_discover_encoding_aristotelian_relations()`

Walks encoding modules for module-level attributes named
`AR_*_RELATIONS` whose value is a tuple of `ArMythosRelation`.
Returns a list of `(encoding_name, relations)` tuples.
Parallels the `AR_*` mythoi walk in
`_discover_encoding_aristotelian_records()`.

Today: Rashomon is the only encoding with a relations tuple
(`AR_RASHOMON_RELATIONS`); Oedipus and Macbeth emit empty-list
skipped silently. If a future encoding authors multiple
relation tuples (e.g., `AR_RASHOMON_RELATIONS` +
`AR_RASHOMON_PARALLEL_RELATIONS`), all are concatenated —
matching the AR_MYTHOI / AR_*_MYTHOS dedup discipline (dedup
by id across module attrs).

### PFS13-D5 — ArAnagnorisisStep discovery

No new top-level discovery helper. `ArAnagnorisisStep` records
are reached transitively:

```python
for encoding_name, mythoi in mythoi_by_encoding:
    for mythos in mythoi:
        for step in mythos.anagnorisis_chain:
            ...
```

Same discipline as `ArPhase` and `ArCharacter` in
`_discover_encoding_aristotelian_records()`. Today: Oedipus's
`AR_OEDIPUS_MYTHOS` has one step (`AR_STEP_JOCASTA`); Macbeth's
`AR_MACBETH_MYTHOS` has one (`AR_STEP_LADY_MACBETH_SLEEPWALKING`);
Rashomon's four mythoi have zero steps each.

### PFS13-D6 — Registry registration

`_build_schema_registry` gains two new entries:
`mythos_relation.json` and `anagnorisis_step.json`. Both are
small; `anagnorisis_step.json` is referenced by `mythos.json`'s
amended `anagnorisis_chain` property, so its registry entry is
load-bearing for mythos shape conformance. `mythos_relation.json`
is self-contained (no outbound `$ref`) but registered for
symmetry — same posture PFS12-D3 takes for
`save_the_cat/observation.json`.

## Conformance dispositions (anticipated)

No active dispositions anticipated. Three **anticipated
findings** (all non-zero):

1. **One ArMythosRelation record in the corpus.** Rashomon's
   `AR_RASHOMON_CONTEST` — `kind="contests"` over the six
   canonical-floor events. Validates against
   `mythos_relation.json` with all optional fields populated
   (non-empty `over_event_ids`; non-empty `annotation`).
2. **Two ArAnagnorisisStep records in the corpus.** Oedipus's
   `AR_STEP_JOCASTA` (`precipitates_main=True`) and Macbeth's
   `AR_STEP_LADY_MACBETH_SLEEPWALKING`
   (`precipitates_main=False`). The two polarities exercise
   both boolean branches on first ship.
3. **Two mythoi with sketch-02 fields populated.** Oedipus's
   `AR_OEDIPUS_MYTHOS` declares `anagnorisis_chain=(AR_STEP_JOCASTA,)`
   and `peripeteia_anagnorisis_binding="separated"`; Macbeth's
   `AR_MACBETH_MYTHOS` declares `anagnorisis_chain=(AR_STEP_LADY_
   MACBETH_SLEEPWALKING,)` and `peripeteia_anagnorisis_binding=
   "coincident"`. Four pre-sketch-02 mythoi (Rashomon's four)
   validate identically to pre-PFS13 shape.

The corpus-conformance tests assert `total >= 1` (relation)
and `total >= 2` (step) rather than PFS11's zero-corpus pattern;
both are non-zero on first ship, distinguishing PFS13 from
PFS11's clean-corpus handling.

## Corpus expectations

Three Aristotelian-dialect encoding modules contribute to the
runtime-generated corpus:

- `oedipus_aristotelian.py` (1 mythos: `AR_OEDIPUS_MYTHOS`;
  1 anagnorisis step: `AR_STEP_JOCASTA`; 0 relations).
- `rashomon_aristotelian.py` (4 mythoi: `AR_RASHOMON_BANDIT`,
  `AR_RASHOMON_SAMURAI`, `AR_RASHOMON_WOODCUTTER`,
  `AR_RASHOMON_WIFE`; 0 steps across mythoi; 1 relation:
  `AR_RASHOMON_CONTEST` in `AR_RASHOMON_RELATIONS`).
- `macbeth_aristotelian.py` (1 mythos: `AR_MACBETH_MYTHOS`;
  1 step: `AR_STEP_LADY_MACBETH_SLEEPWALKING`; 0 relations).

**Expected corpus counts:**

- **ArMythosRelation**: 1 record — `kind="contests"`, 4 mythoi,
  6 over_event_ids, non-empty annotation. Shape validated via
  metaschema + shape + corpus tests.
- **ArAnagnorisisStep**: 2 records — one per polarity of
  `precipitates_main`. Shape validated via metaschema + shape
  + corpus tests.
- **ArMythos**: 6 records (4 Rashomon + 1 Oedipus + 1 Macbeth).
  Two carry non-empty `anagnorisis_chain`; two carry non-None
  `peripeteia_anagnorisis_binding`. All six validate against
  the amended `mythos.json`.

## Open questions

1. **OQ1 — `ArMythosRelation.kind` close-enum.** A10's three
   canonical kinds vs. open-string-at-noted-severity discipline
   argues against a close-enum today. Parallel to PFS9-LO3 /
   PFS11-AO3 / PFS12-O3 / PFS7 `role_labels`. Forcing function:
   kind vocabulary stabilizes AND no encoding has authored a
   non-canonical value in practice across a full year or two.
   Banked.
2. **OQ2 — Referential integrity on `ArMythosRelation.mythoi_ids`
   and `over_event_ids`.** Schema admits non-empty string arrays;
   A7.6 enforces at verification time. A later Tier-2 audit
   would lift mythos-id / event-id resolution to schema-walkable.
   Parallel to PFS11 OQ3 / PFS12 OQ2. Banked.
3. **OQ3 — Referential integrity on `ArAnagnorisisStep.event_id`
   and `character_ref_id`.** Same bank as OQ2. A7.7 enforces at
   verification time. Banked.
4. **OQ4 — Schema-level defaults for
   `peripeteia_anagnorisis_adjacency_bound`,
   `precipitates_main`, and other Python-defaulted fields.**
   Today's conformance discipline omits `"default"` keys at the
   schema layer, relying on Python to carry defaults (unity-of-*
   precedent). A later arc with a cross-namespace default-
   handling convention would lift this. Banked.
5. **OQ5 — Cross-encoding `ArMythosRelation`.** Today all
   relations live within one encoding. A cross-encoding
   structural relation (e.g., an Oedipus-vs-Ackroyd "narrator-
   is-the-killer" resonance) routes through the cross-dialect
   Lowering surface (architecture-sketch-02 A8), not the
   dialect-local relation record. Schema does not need to
   accommodate this today. Banked — same posture as
   aristotelian-sketch-02 OQ5.

## Discipline

Same-as-always under the PFS2 discipline:

- **Sketches before schema.** Aristotelian-sketch-02 committed
  A10–A12 field shapes. Probe-sketches-02 and -03 verified the
  shapes hold under encoding pressure (Rashomon relation;
  Oedipus / Macbeth steps + bindings). This arc format-renders;
  no new commitments.
- **Schemas before code.** No Python change. If a conformance
  issue surfaces, the posture is the same as all prior arcs
  (fix the design sketch first; then schema; then Python).
- **Fifth per-record arc under Production C.** PFS13's
  structure mirrors PFS9 / PFS10 / PFS11 / PFS12 (record
  commitment by record; dump-discovery-registry block; open
  questions banked). **First arc to amend an existing dialect-
  core schema** rather than purely extending the namespace with
  new files — the three-field `mythos.json` amendment is the
  novel shape-pressure. PFS13-D3's split between extending an
  existing dump helper (`_dump_armythos`) and adding new ones
  (`_dump_ar_mythos_relation`, `_dump_ar_anagnorisis_step`)
  reflects the same structure.
- **Slim within the per-record arc tier.** Two new records +
  three new fields on an existing record + one cross-file
  `$ref`. Target ~450 lines (PFS12 shipped one record at 440;
  PFS11 shipped four at ~720; PFS13's per-record-budget sits
  between them — two records is less than PFS11's four but the
  `mythos.json` amendment adds shape-pressure PFS12 didn't
  carry).

## Summary

Fifth per-record sketch under Production C. Two new JSON Schema
files plus an amendment to an existing schema, all under
`schema/aristotelian/` — the dialect's existing namespace,
per PFS8-N2's dialect-internal classification.

Commitments across four families:

- **PFS13-N1** — namespace inherits PFS6-N1
  (`schema/aristotelian/`).
- **PFS13-MR1..MR4** — ArMythosRelation shape (required id /
  kind / mythoi_ids; kind open string; mythoi_ids minItems 2;
  optional over_event_ids + annotation).
- **PFS13-AS1..AS4** — ArAnagnorisisStep shape (required id /
  event_id / character_ref_id; optional precipitates_main +
  annotation).
- **PFS13-M12..M14** — mythos.json amendment (three new optional
  properties: anagnorisis_chain array-of-ref;
  peripeteia_anagnorisis_binding closed enum;
  peripeteia_anagnorisis_adjacency_bound integer).
- **PFS13-X** — cross-file `$ref` from mythos.json to
  anagnorisis_step.json (fourth same-namespace reference in
  `schema/aristotelian/`).
- **PFS13-X2** — no CrossDialectRef (dialect-internal).
- **PFS13-D1..D6** — two new dump helpers + one extension to
  `_dump_armythos` + one new discovery helper for relations +
  registry registration.

Five open questions banked with forcing functions:
`ArMythosRelation.kind` close-enum (OQ1); Tier-2 referential-
integrity audits on relation refs (OQ2) and step refs (OQ3);
cross-namespace Python-defaults convention (OQ4); cross-encoding
relation routing (OQ5).

No design derivation needed. Aristotelian-sketch-02 A10–A12
committed the record shapes; probe-sketches-02 + -03 verified
the closures hold; this sketch format-renders and hands off to
implementation.

Python untouched at the sketch layer. Dump-layer + discovery +
test-suite extensions land in the implementation commit. First
arc under Production C that both *extends* a namespace (two new
files) AND *amends* an existing dialect-core record
(`mythos.json` gains three fields) in a single arc.
