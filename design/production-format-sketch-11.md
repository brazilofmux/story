# Production format — sketch 11

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (third per-record arc under Production C;
ships the Aristotelian cross-boundary batch — four records under
the existing `schema/aristotelian/` namespace committed by
PFS6-N1, per PFS8-N2's classification that dialect-internal
cross-boundary records live in the dialect's namespace)
**Frames:** [production-format-sketch-06](production-format-
sketch-06.md) PFS6-N1 (Aristotelian namespace), PFS6-X1
(intra-namespace cross-file `$ref`), PFS6 §Scope (deferred
Aristotelian cross-boundary records); [production-format-
sketch-08](production-format-sketch-08.md) PFS8-N2 (dialect-
internal records stay under `schema/<dialect>/`), PFS8 §Per-
record arc plan item 3 (PFS11 brief), PFS8 OQ4 (ArAnnotation-
Review optional-id decision); [production-format-sketch-09](
production-format-sketch-09.md) PFS9-LO1..LO4 (Lowering-
Observation shape as template for ArObservation); [production-
format-sketch-10](production-format-sketch-10.md) PFS10-VC1..
VC4 + PFS10-X2 (VerifierCommentary shape + cross-file `$ref`
as template for ArObservationCommentary); [aristotelian-
probe-sketch-01](aristotelian-probe-sketch-01.md) APA1 (four-
record additive surface — ArAnnotationReview /
ArObservationCommentary / DialectReading field-level shapes
pre-committed); [aristotelian-sketch-01](aristotelian-
sketch-01.md) A7 (self-verifier check catalog — ArObservation
emission sites); [production-format-sketch-01](production-
format-sketch-01.md) PFS1 (JSON Schema 2020-12), PFS2
(schemas-first); [production-format-sketch-03](production-
format-sketch-03.md) PFS3-E1 (cross-file `$ref` via registry);
[production-format-sketch-07](production-format-sketch-07.md)
PFS7-X2 (inline-$defs-for-sub-records convention)
**Related:** [architecture-sketch-02](architecture-sketch-02.md)
A7/A8 (dialect-internal observation vs. shared verification);
[reader-model-sketch-01](reader-model-sketch-01.md) R6
(reviewed_at_τ_a anchor semantics); [referential-integrity-
sketch-01](referential-integrity-sketch-01.md) RI7 (Aristotelian
event-ref audit precedent — applies equally to Ar* target_id
resolution banked here as OQ3)
**Superseded by:** nothing yet

## Purpose

**Third per-record sketch under Production C.** Ships four
JSON Schema 2020-12 files for the Aristotelian cross-boundary
batch — `ArObservation`, `ArAnnotationReview`,
`ArObservationCommentary`, `DialectReading` — under the
existing `schema/aristotelian/` namespace PFS6-N1 committed.
Per PFS8-N2: dialect-internal records (self-verifier
observations, probe-methodology review / commentary / reading)
ship under the dialect's namespace, not under a top-level
role-named namespace.

The per-record design work is already done. Aristotelian-
sketch-01 A7 commits the ArObservation emission vocabulary
(five checks as of aristotelian-sketch-02 A7.6–A7.9). The
three probe-surface records (ArAnnotationReview /
ArObservationCommentary / DialectReading) ship from
aristotelian-probe-sketch-01 APA1 (Python dataclasses
committed + Pydantic output schema aligned). This sketch
format-renders the four records; no new field-level
commitments.

## Why now

- **Largest remaining per-record arc under Production C.**
  PFS9 (three records), PFS10 (four records), PFS11 (four
  records) — PFS11 is the largest bundle under Production C;
  the four ship together because they share the same
  authorial surface (aristotelian-probe-sketch-01) and the
  same dialect namespace. Once PFS11 lands, only PFS12 (one-
  record Save-the-Cat observation) and the Dramatic / dramatica-
  complete gated arcs remain under Production C.
- **ArObservation is the load-bearing self-verifier output.**
  Every call to `aristotelian.verify(mythos)` returns a tuple
  of ArObservations. Validating the shape at the schema layer
  completes the dialect's output-shape contract (the input
  side — ArMythos / ArPhase / ArCharacter — shipped under
  PFS6).
- **Probe-methodology records close the reader-model output
  surface.** The three probe-surface records are produced by
  `aristotelian_reader_model_client.py` on every invocation;
  their Pydantic output schema sits at the LLM boundary.
  Schema-level shape completes the parallel to PFS10's
  VerificationReview (verifier boundary) + PFS9's
  AnnotationReview (reader-model boundary).
- **Corpus exists (partial).** ArObservations emit from
  running each encoding's mythoi through `verify()`; three
  Aristotelian encodings (oedipus, rashomon, macbeth) each
  contribute. The clean corpus emits zero observations (every
  encoding verifies clean per sketch-11 baseline 807 passing);
  shape validated via metaschema + shape tests. The three
  probe records have no encoding-level corpus (probe output
  lives in JSON files outside the conformance corpus; parallels
  PFS10's VerifierCommentary handling).

## Scope — what the sketch covers

**In:**

- Four JSON Schema files under `schema/aristotelian/`:
  - `schema/aristotelian/observation.json` (`ArObservation`
    per A7).
  - `schema/aristotelian/annotation_review.json`
    (`ArAnnotationReview` per APA1).
  - `schema/aristotelian/observation_commentary.json`
    (`ArObservationCommentary` per APA1).
  - `schema/aristotelian/dialect_reading.json`
    (`DialectReading` per APA1).
- **Cross-file `$ref` from `observation_commentary.json` to
  `observation.json`** for `target_observation`. Extends
  PFS6-X1's intra-namespace cross-file pattern to a fourth
  reference inside `schema/aristotelian/` (mythos.json →
  phase.json; mythos.json → character.json;
  observation_commentary.json → observation.json).
- **Pair-consistency conditional on `ArAnnotationReview`**:
  `field` values constrained by `target_kind` via
  `allOf/if-then-else` (three branches — ArMythos →
  action_summary; ArPhase → annotation; ArCharacter →
  hamartia_text). Mirrors the
  `FIELDS_BY_TARGET_KIND` invariant in `core/aristotelian.py`
  at schema level.
- Dump-layer helpers: `_dump_ar_observation`,
  `_dump_ar_annotation_review`,
  `_dump_ar_observation_commentary`, `_dump_dialect_reading`.
- Discovery helper for ArObservation: walks each encoding's
  Aristotelian mythoi and calls `verify(mythos)` to produce
  observations.
- Registry registration: four new entries.
- Twelve new conformance tests (4 metaschema + 4 shape + 4
  corpus), following the PFS10 template.

**Out (banked with forcing functions):**

- StcObservation (PFS12 — shipped under `schema/save_the_cat/`).
- DramaticaObservation family (Dramatic / Dramatica-complete
  dialects — gated on PFS13 / PFS14).
- Probe-result *container* records (ReaderModelResult,
  DramaticReaderModelResult, AristotelianReaderModelResult)
  — deferred per PFS8-X as runtime/ephemeral containers whose
  contents are the load-bearing types spec'd here.
- Referential integrity audits on Ar* target_id fields
  (ArObservation.target_id → mythos/phase/character id;
  ArAnnotationReview.target_id → mythos/phase/character id).
  Banked as OQ3 under this sketch; a later RI arc would add
  the audit per RI7's Aristotelian event-ref precedent.
- Close-enum on ArObservation.code. Five stable codes as of
  aristotelian-sketch-02; extensibility-friendly open string
  per PFS9-LO3.
- Probe-output corpus ingestion (loading
  `reader_model_*_aristotelian_output*.json` as conformance
  corpus). The JSONs are research artifacts per sketch-10's
  context-economy discipline; their contents are validated
  implicitly by the aristotelian-probe-sketch-02 probe-
  closure loop. Banked as OQ4.

**Not the topic:**

- No Python change. The four dataclasses already exist in
  `core/aristotelian.py`; their field shapes pre-committed by
  APA1 / A7. PFS2 discipline: schema shape is source of
  truth; Python conforms to schema. No divergences
  anticipated (the Python docstrings directly cite the
  sketch-01 shapes).
- No new architecture claims. PFS8-N2 committed the dialect-
  internal classification; this is the first arc to exercise
  it.
- No reader-model-client changes. Output Pydantic schema in
  `aristotelian_reader_model_client.py` stays as-is; the
  translate-to-records path produces the four dataclasses
  already.

## Commitments

### PFS11-N1 — Namespace inherits PFS6-N1

The four new schemas live under `schema/aristotelian/` — the
dialect's existing namespace. No new top-level subdirectory.
Per PFS8-N2: dialect-internal cross-boundary records (self-
verifier observation, probe-methodology review / commentary /
reading) share the namespace with the dialect's core records
(mythos / phase / character) because they're produced by or
about the dialect itself, not shared across dialects.

This means the `$id` URIs are:

- `https://brazilofmux.github.io/story/schema/aristotelian/observation.json`
- `https://brazilofmux.github.io/story/schema/aristotelian/annotation_review.json`
- `https://brazilofmux.github.io/story/schema/aristotelian/observation_commentary.json`
- `https://brazilofmux.github.io/story/schema/aristotelian/dialect_reading.json`

### PFS11-AO1..AO4 — ArObservation record shape

`schema/aristotelian/observation.json` ships the
`ArObservation` record per aristotelian-sketch-01 A7 (self-
verifier finding). Parallels `LoweringObservation` (PFS9-LO)
and the anticipated `StcObservation` (PFS12): four-field
structural-finding shape.

- **PFS11-AO1.** Required fields: `severity`, `code`,
  `target_id`, `message`. All four from the Python
  dataclass. No optionals.
- **PFS11-AO2.** `severity` is a **closed enum** at two
  values: `{"noted", "advises-review"}`. Matches
  `core/aristotelian.py`'s `SEVERITY_NOTED` /
  `SEVERITY_ADVISES_REVIEW` constants. Distinct from
  `LoweringObservation` (same two values; happens to align)
  and `StructuralAdvisory` (three-tier — adds `suggest-revise`).
- **PFS11-AO3.** `code` is an **open non-empty string**.
  Today's A7 checks emit five stable codes:
  `plot_kind_invalid`, `phase_roles_not_beginning_middle_end`,
  `peripeteia_not_in_central_events`,
  `anagnorisis_not_in_central_events`, and the sketch-02
  additions A7.6–A7.9 (`mythos_relation_dialect_internal`,
  `anagnorisis_step_precipitates_coincident`, etc.). Open
  string per PFS9-LO3: new A7 checks don't require a schema
  amendment. Code vocabulary closure deferred to OQ1 if the
  code set stabilizes.
- **PFS11-AO4.** `target_id` and `message` are **non-empty
  strings**. `target_id` names the record the observation
  attaches to (an ArMythos / ArPhase / ArCharacter id);
  resolution banked as OQ3 (referential-integrity audit).
  `message` is human-readable prose with no length bound.
- **`additionalProperties: false`.**

### PFS11-AR1..AR6 — ArAnnotationReview record shape

`schema/aristotelian/annotation_review.json` ships the
`ArAnnotationReview` record per aristotelian-probe-sketch-01
APA1 (reviewer verdict on a prose field of an Aristotelian
record). Parallels `lowering/annotation_review.json` in shape
but targets Aristotelian records' prose fields instead of a
Lowering's annotation field.

- **PFS11-AR1.** Required fields: `reviewer_id`,
  `reviewed_at_τ_a`, `target_kind`, `target_id`, `field`,
  `verdict`, `anchor_τ_a`. Seven required. `anchor_τ_a` is
  required per PFS7 convention (Python always carries the
  default-0 value; schema requires it).
- **PFS11-AR2.** `reviewer_id` non-empty string;
  `reviewed_at_τ_a` and `anchor_τ_a` integers; `target_id`
  non-empty string.
- **PFS11-AR3.** `target_kind` is a **closed enum** at
  three values: `{"ArMythos", "ArPhase", "ArCharacter"}`.
  Matches Python's `VALID_REVIEW_TARGET_KINDS`. The closed
  set matches APA1's commitment: each reviewable record
  kind appears here; future dialect-record kinds (A10–A12)
  have no reviewable prose field of their own today
  (ArMythosRelation / ArAnagnorisisStep author-notes live on
  their parent records per aristotelian-sketch-02 §A10–A12
  scope discussion). If a future sketch adds prose fields to
  those records, PFS11 amends target_kind — a schema-amend-
  only change.
- **PFS11-AR4.** `field` is a **closed enum** at three values:
  `{"action_summary", "annotation", "hamartia_text"}`.
  Matches Python's `VALID_REVIEW_FIELDS`. Each token names the
  one reviewable prose field on its target kind — no
  polymorphism across target_kinds (per APA1's one-field-per-
  target rule).
- **PFS11-AR5.** `verdict` is a **closed enum** at four values:
  `{"approved", "needs-work", "rejected", "noted"}`. Matches
  Python's `VERDICT_*` (duplicated locally in `aristotelian.py`
  to keep the module free of `lowering.py` imports, parallel
  to `verification.py`'s duplicate). Same four-value shape as
  `lowering/annotation_review.json` — the two AnnotationReview
  records share vocabulary (both are review acts emitting
  verdicts on authored prose).
- **PFS11-AR6.** `comment` is an **optional string** (Python-
  default-None → omitted from dump when None). `id` is an
  **optional non-empty string** (PFS8 OQ4 closure — Python's
  `id: Optional[str] = None` maps to schema-optional, emitted
  only when set; default elides). Differs from lowering
  AnnotationReview (no id field); decision per PFS8 OQ4 is
  keep optional to match Python, bank close-enum / convergence
  question to OQ5.
- **`additionalProperties: false`.**

### PFS11-AC1..AC5 — ArObservationCommentary record shape

`schema/aristotelian/observation_commentary.json` ships the
`ArObservationCommentary` record per APA1 (reader-model
commentary on an ArObservation). Parallels
`verification/verifier_commentary.json` (PFS10-VC) in shape
but targets this dialect's observation rather than a
VerificationReview.

- **PFS11-AC1.** Required fields: `commenter_id`,
  `commented_at_τ_a`, `assessment`, `target_observation`.
  Four required. `comment` not required — Python has it
  optional; an endorsement-with-no-comment is structurally
  valid (parallel to StcObservation's optional-comment
  posture, different from VerifierCommentary where
  `comment` is required per PFS10-VC1 because the commentary's
  entire purpose is to carry content).
- **PFS11-AC2.** `commenter_id` non-empty string;
  `commented_at_τ_a` integer.
- **PFS11-AC3.** `assessment` is a **closed enum** at four
  values: `{"endorses", "qualifies", "dissents", "noted"}`.
  Matches Python's `ASSESSMENT_*` (duplicated locally for the
  same no-`verification.py`-import discipline). Same four-
  value shape as `verification/verifier_commentary.json`.
- **PFS11-AC4.** `target_observation` is an `ArObservation`
  object via **cross-file `$ref`** to
  `observation.json` per PFS11-X1. The Python carries the
  ArObservation by value (frozen, no id); the schema expresses
  it via cross-file `$ref` (same-namespace resolution,
  parallel to PFS10-X2's verifier_commentary → verification_
  review).
- **PFS11-AC5.** `comment` is an **optional string**; Python-
  default-None → omitted when None. `suggested_signature` is
  an **optional non-empty string** (free-form prose naming a
  concrete signature the commenter thinks the A7 check might
  add; inspiration for the maintainer, not executable code).
  Both emit only when set.
- **`additionalProperties: false`.**

### PFS11-DR1..DR5 — DialectReading record shape

`schema/aristotelian/dialect_reading.json` ships the
`DialectReading` record per APA1 (reader-model's methodology
self-report — "did I engage the Aristotelian surface on its
own terms or drift?"). **No analog in PFS9 / PFS10** —
DialectReading is the dialect-probe surface's distinctive
record type, not a parallel of existing cross-boundary shapes.

- **PFS11-DR1.** Required fields: `reader_id`, `read_at_τ_a`,
  `read_on_terms`, `rationale`, `drift_flagged`,
  `scope_limits_observed`, `relations_wanted`. Seven required.
  The three tuple fields (`drift_flagged`,
  `scope_limits_observed`, `relations_wanted`) default to
  empty tuples in Python; per the PFS7 convention (if the
  Python always carries them, the schema requires them), they
  emit always.
- **PFS11-DR2.** `reader_id` non-empty string; `read_at_τ_a`
  integer; `rationale` non-empty string (bounded free-form
  prose; the prompt caps length, the schema does not).
- **PFS11-DR3.** `read_on_terms` is a **closed enum** at
  three values: `{"yes", "partial", "no"}`. Matches
  Python's `READ_ON_TERMS_*`. Three-valued ordinal self-
  report per APA1: the probe's principal signal.
- **PFS11-DR4.** `drift_flagged`, `scope_limits_observed`,
  `relations_wanted` are **arrays of non-empty strings**.
  Each empty-allowable (empty = clean in-dialect read). Free-
  form token content (per APA1 docstrings). No per-element
  closed enum — these tokens are dialect-specific
  observations; aristotelian-probe-sketch-01/-02 carry worked
  examples (`"ArMythosRelation"`, `"meta-anagnorisis"`, etc.)
  but no exhaustive vocabulary.
- **PFS11-DR5.** `additionalProperties: false`.

### PFS11-X1 — Pair-consistency conditional on ArAnnotationReview

`ArAnnotationReview`'s `field` value must match `target_kind`
per the Python invariant `FIELDS_BY_TARGET_KIND`:

- `target_kind=ArMythos` ⇒ `field=action_summary`
- `target_kind=ArPhase` ⇒ `field=annotation`
- `target_kind=ArCharacter` ⇒ `field=hamartia_text`

The schema enforces this via `allOf/if-then-else` (three
branches; schema-level pair-consistency). Mirrors the PFS5-B5
/ PFS6-M6 / PFS9-X3 conditional-required pattern — a
Python-invariant lifted to schema at the shape tier rather
than deferred to a runtime check.

Shape:

```json
"allOf": [
  {"if": {"properties": {"target_kind": {"const": "ArMythos"}},
          "required": ["target_kind"]},
   "then": {"properties": {"field": {"const": "action_summary"}}}},
  {"if": {"properties": {"target_kind": {"const": "ArPhase"}},
          "required": ["target_kind"]},
   "then": {"properties": {"field": {"const": "annotation"}}}},
  {"if": {"properties": {"target_kind": {"const": "ArCharacter"}},
          "required": ["target_kind"]},
   "then": {"properties": {"field": {"const": "hamartia_text"}}}}
]
```

The close-enum on `target_kind` and `field` already blocks
invalid values individually; the conditional blocks a *valid-
individually-but-mismatched-pair*. A future `target_kind` with
an additional prose field would add a fourth branch.

### PFS11-X2 — Cross-file `$ref` from ArObservationCommentary to ArObservation

`observation_commentary.json`'s `target_observation` property
uses `$ref` to
`https://brazilofmux.github.io/story/schema/aristotelian/observation.json`.
The registry pattern (PFS3-E1 → PFS4 P4A1 → PFS6-D5 → PFS9-D8
→ PFS10-D6) resolves it.

**Same-namespace cross-file `$ref` reasoning** parallel to
PFS10-X2:

1. **Size and stability.** ArObservation is a small record
   (four fields, no nested structure) — re-inlining would be
   feasible. But the dialect namespace already holds four
   records cross-referencing each other (mythos → phase,
   mythos → character); adding observation_commentary →
   observation is a one-liner under the established pattern.
   `$ref` scales without duplication pressure.
2. **Same-namespace resolution.** Reference stays within
   `schema/aristotelian/`; PFS8-V's cross-namespace-coupling
   concern doesn't apply. The same pattern PFS10-X2 used for
   verifier_commentary → verification_review.

The general rule across PFS6/PFS9/PFS10/PFS11: prefer cross-
file `$ref` for same-namespace references; prefer inline
`$defs` (or re-inlined copies) for cross-namespace small-and-
stable sub-records.

### PFS11-X3 — No CrossDialectRef

Unlike PFS9/PFS10, no record in this batch carries a
`CrossDialectRef`. Rationale:

- `ArObservation.target_id` resolves to an **intra-dialect**
  id (ArMythos / ArPhase / ArCharacter). No dialect token
  needed.
- `ArAnnotationReview.target_id` + `target_kind` resolves to
  an intra-dialect record. The `target_kind` field carries
  the record-type discrimination that `CrossDialectRef.dialect`
  would carry in a cross-dialect case; since the set is
  intra-Aristotelian, a simple `(target_kind, target_id)`
  pair is simpler.
- `ArObservationCommentary.target_observation` is a nested
  ArObservation by value — no id indirection.
- `DialectReading` has no record references.

PFS11 is the first Production-C arc since PFS8 to ship
without touching CrossDialectRef. Dialect-internal cross-
boundary records route differently than cross-dialect
ones; the namespace boundary is the routing signal.

## Dump-layer commitments

Parallel to PFS6-D1..D3 for Aristotelian core, PFS9-D1..D6
for Lowering family, PFS10-D1..D4 for Verification family.

### PFS11-D1 — `_dump_ar_observation(obs) -> dict`

Field-for-field isomorphic. All four fields always emit
(severity, code, target_id, message). No conditional emission
— no optional fields.

### PFS11-D2 — `_dump_ar_annotation_review(review) -> dict`

Field-for-field. Required fields always emit (reviewer_id,
reviewed_at_τ_a, target_kind, target_id, field, verdict,
anchor_τ_a). `comment` omitted when None. `id` omitted when
None.

### PFS11-D3 — `_dump_ar_observation_commentary(commentary) -> dict`

Field-for-field. Required fields always emit (commenter_id,
commented_at_τ_a, assessment, target_observation).
`target_observation` rendered via `_dump_ar_observation` (full
nested shape — matches the Python's by-value carrying).
`comment` omitted when None. `suggested_signature` omitted
when None.

### PFS11-D4 — `_dump_dialect_reading(reading) -> dict`

Field-for-field. All seven fields always emit (including the
three tuple fields rendered as arrays; empty tuples → empty
arrays). `rationale` emits as-is.

### PFS11-D5 — `_discover_encoding_aristotelian_observations(mythoi_by_encoding)`

Runs `aristotelian.verify(mythos)` on each mythos in each
encoding to produce ArObservation records. Parallels
PFS10-D5 (which walks `*_verification.py` modules) — this
walks in-memory ArMythos records from
`_discover_encoding_aristotelian_records()` (PFS6-D4) and
invokes the dialect's self-verifier.

Returns a list of `(encoding_name, observations)` tuples
across all mythoi in the encoding. Clean corpus → empty lists
(all three Aristotelian encodings verify clean per sketch-11
baseline). The discovery helper does not need to re-walk
encoding modules — it takes the already-discovered mythoi
list as input.

**No encoding-level probe-record discovery.** The three probe-
surface records (ArAnnotationReview / ArObservationCommentary
/ DialectReading) are produced by `aristotelian_reader_model_
client.py` at runtime and serialized to probe JSONs; they're
not encoding-level attributes. The corpus-conformance tests
for these three records see zero records — shape validated
via metaschema + shape tests only (parallel to PFS10's
VerifierCommentary + VerificationAnswerProposal handling).

### PFS11-D6 — Registry registration

The conformance test's `_build_schema_registry` gains four
new entries. The registry is load-bearing for
`observation_commentary.json` (cross-file `$ref` to
`observation.json` per PFS11-X2). The other three schemas
(observation, annotation_review, dialect_reading) are self-
contained and could validate without registry binding, but
registration gives symmetric `$id` lookup and keeps the
registry consistent across dialect + cross-boundary namespaces.

## Conformance dispositions (anticipated)

No active dispositions anticipated. Four **anticipated non-
findings**:

1. **Zero ArObservation records in the corpus (clean).** All
   three Aristotelian encodings (oedipus, rashomon, macbeth)
   verify clean per sketch-11 baseline. The corpus-conformance
   test emits `0 ArObservation records` with a descriptive
   note, parallel to PFS10's VerificationAnswerProposal
   handling. Shape validated via metaschema + shape tests.
2. **Zero ArAnnotationReview records.** No encoding authors
   ArAnnotationReview records; they emit from probe runs.
   Shape validated; corpus-conformance note.
3. **Zero ArObservationCommentary records.** Same reasoning.
4. **Zero DialectReading records.** Same reasoning.

All four zero-corpus cases mirror PFS10's VerifierCommentary
handling — shape is validated fully; the corpus-conformance
test prints `zero records; expected per PFS11 §Corpus
expectations` rather than failing.

**If a future corpus change forces non-zero records** (e.g.,
an encoding deliberately authoring an ArObservation as
documented structural concern, or a verifier emitting
ArObservationCommentary), the dispositions section amends
then.

## Corpus expectations

Three Aristotelian-dialect encoding modules contribute to the
runtime-generated corpus:

- `oedipus_aristotelian.py` (1 mythos: AR_OEDIPUS_MYTHOS).
- `rashomon_aristotelian.py` (4 mythoi: AR_RASHOMON_BANDIT,
  AR_RASHOMON_SAMURAI, AR_RASHOMON_WOODCUTTER,
  AR_RASHOMON_WIFE; tupled as AR_RASHOMON_MYTHOI).
- `macbeth_aristotelian.py` (1 mythos: AR_MACBETH_MYTHOS).

Running `aristotelian.verify` over the 6 mythoi (accounting
for one per Oedipus + one per Macbeth + four Rashomon)
produces **zero ArObservations** — the three encodings all
pass clean under A7 checks (tests
`test_{oedipus,rashomon,macbeth}_aristotelian_verifies_clean`
pin this).

**Expected corpus counts:**

- **ArObservation**: zero records — clean corpus. Shape
  validated via metaschema + shape tests.
- **ArAnnotationReview**: zero records — probe output only.
- **ArObservationCommentary**: zero records — probe output
  only.
- **DialectReading**: zero records — probe output only.

**Test assertion posture.** Each corpus-conformance test
allows zero records (no `assert total > 0`, unlike
VerificationReview which expects ≥1). This matches PFS10's
zero-corpus pattern for probe records. The tests still
validate non-zero totals when they materialize (a later
sketch encoding an ArObservation as authored-fact would
exercise the validator path).

## Open questions

1. **OQ1 — ArObservation.code close-enum.** Today's A7 checks
   emit a stable set of codes (five before sketch-02 + new
   sketch-02 codes). Schema admits any non-empty string per
   PFS11-AO3. A close-enum commitment could lift Python's
   emission vocabulary to schema level. Deferred: the A7
   check set is still growing (sketch-01 had 5; sketch-02
   added 4; a future amendment-sketch would add more).
   Forcing function: A7 check set stabilizes with a PFS-
   committed close-enum disposition. Parallel to PFS9-LO3's
   open-code posture. Banked.

2. **OQ2 — DialectReading tuple-element close-enum.** The
   three tuple fields (`drift_flagged`, `scope_limits_observed`,
   `relations_wanted`) carry free-form tokens today. A probe
   reading many encodings over time would grow a natural
   vocabulary — e.g., drift_flagged converges on a small set
   of "off-dialect" terms the probe keeps noticing itself
   want to use. A close-enum at that point would surface a
   mismatch (token outside the set) as a finding worth
   investigating. Forcing function: two-plus probe runs with
   drift_flagged vocabulary stabilizing. Banked.

3. **OQ3 — Referential integrity on ArObservation.target_id
   and ArAnnotationReview.target_id.** Both point at intra-
   dialect record ids (ArMythos / ArPhase / ArCharacter).
   The schema admits any non-empty string; existence is not
   checked. A later Tier-2 audit (per referential-integrity-
   sketch-NN) extends coverage. Today: zero ArObservations
   + zero ArAnnotationReviews in the corpus; the audit
   surface doesn't forcing-function until either (a) a
   non-zero corpus exists, or (b) a probe emits records with
   a typo in target_id. Parallels PFS5 OQ3 / PFS6 OQ3 / PFS9
   OQ2 / PFS10 OQ1. Banked.

4. **OQ4 — Probe-output corpus ingestion.** The three probe
   records have no encoding-level corpus today; the research
   artifacts (`reader_model_*_aristotelian_output*.json`)
   carry them in JSON form. A future sketch could load these
   JSONs as conformance corpus (validate every record in
   every probe output file). Rejected as sketch-level scope
   today because probe JSONs are intended as disposable
   research artifacts per the context-economy discipline;
   loading them turns them into conformance input and creates
   a keep-or-delete pressure that isn't wanted. Forcing
   function: a probe finding a schema drift in its own
   output (self-inconsistent JSON). Banked.

5. **OQ5 — ArAnnotationReview id-field convergence.** Lowering's
   AnnotationReview has no id field; Aristotelian's has
   `Optional[str]` id (PFS8 OQ4 asked whether to converge).
   PFS11-AR6 keeps optional per Python. A convergence path
   (both id-less, or both required-id) would require an
   upstream decision — APA1's commitment pre-dated the PFS9
   annotation_review landing; without an external-cross-
   reference forcing function, the current asymmetry is
   tolerable. Forcing function: a consumer (walker / CI
   tooling) that needs to externally reference a specific
   AnnotationReview across both namespaces by id. Banked.

## Discipline

Same-as-always under the PFS2 discipline:

- **Sketches before schema.** Aristotelian-sketch-01 A7
  committed the ArObservation code vocabulary; aristotelian-
  probe-sketch-01 APA1 committed the three probe-surface
  records' field shapes. The `SEVERITY_*` / `VERDICT_*` /
  `ASSESSMENT_*` / `READ_ON_TERMS_*` constant vocabularies
  lift to schema-level closed enums.
- **Schemas before code.** No Python change. If a conformance
  issue surfaces, the posture is the same as all prior arcs
  (fix the design sketch first; then schema; then Python).
- **Third per-record arc under Production C.** PFS11's
  structure mirrors PFS9/PFS10 (record commitments by record;
  inline-vs-$ref decisions named explicitly; dump-discovery-
  registry block; open questions banked). The generalization
  from PFS9/PFS10 to PFS11 tests that the per-record sketch
  template works for the dialect-internal arc — same slim
  shape, same commitments-by-record-family.
- **Slim when the design is done.** Target ~650 lines similar
  to PFS9 / PFS10. Four records with a modest number of
  field-level decisions each plus the pair-consistency
  conditional (PFS11-X1) and the observation_commentary →
  observation cross-file `$ref` (PFS11-X2).

## Summary

Third per-record sketch under Production C. Four JSON Schema
files for the Aristotelian cross-boundary batch shipped
under `schema/aristotelian/` — the dialect's existing
namespace, per PFS8-N2's dialect-internal classification.

Twenty-four commitments across six families:

- **PFS11-N1** — namespace inherits PFS6-N1
  (`schema/aristotelian/`).
- **PFS11-AO1..AO4** — ArObservation shape (required severity /
  code / target_id / message; severity enum {noted, advises-
  review}; code open string; target_id + message non-empty
  strings).
- **PFS11-AR1..AR6** — ArAnnotationReview shape (required
  reviewer_id / reviewed_at_τ_a / target_kind / target_id /
  field / verdict / anchor_τ_a; target_kind enum {ArMythos,
  ArPhase, ArCharacter}; field enum {action_summary,
  annotation, hamartia_text}; verdict enum {approved, needs-
  work, rejected, noted}; optional comment / id).
- **PFS11-AC1..AC5** — ArObservationCommentary shape
  (required commenter_id / commented_at_τ_a / assessment /
  target_observation; assessment enum {endorses, qualifies,
  dissents, noted}; target_observation via cross-file `$ref`
  to observation.json per PFS11-X2; optional comment /
  suggested_signature).
- **PFS11-DR1..DR5** — DialectReading shape (required
  reader_id / read_at_τ_a / read_on_terms / rationale /
  drift_flagged / scope_limits_observed / relations_wanted;
  read_on_terms enum {yes, partial, no}; tuple fields as
  arrays of non-empty strings, empty-allowable).
- **PFS11-X1** — pair-consistency conditional on
  ArAnnotationReview (allOf/if-then-else — target_kind →
  field mapping).
- **PFS11-X2** — cross-file `$ref` from observation_
  commentary.json to observation.json (intra-namespace,
  extends PFS6-X1 / PFS10-X2 pattern).
- **PFS11-X3** — no CrossDialectRef; all references are
  intra-dialect.
- **PFS11-D1..D6** — dump helpers + discovery helper (runs
  `verify()` on each encoding's mythoi) + registry
  registration.

Five open questions banked with forcing functions:
ArObservation.code close-enum (OQ1); DialectReading tuple
close-enums (OQ2); Tier-2 referential-integrity audit on
intra-dialect target_id fields (OQ3); probe-output corpus
ingestion (OQ4); ArAnnotationReview id-field convergence
across namespaces (OQ5).

No design derivation needed. Aristotelian-sketch-01 A7 +
aristotelian-probe-sketch-01 APA1 committed the record
shapes; this sketch format-renders, lifts SEVERITY /
VERDICT / ASSESSMENT / READ_ON_TERMS vocabularies to schema-
level enums, encodes FIELDS_BY_TARGET_KIND pair-consistency
as PFS11-X1, extends PFS6-X1's cross-file `$ref` pattern to
observation_commentary → observation via PFS11-X2, and hands
off to implementation.

Python untouched at the sketch layer. Dump-layer + discovery
+ test-suite extensions land in the implementation commit.
Cross-boundary namespace tier reaches four of five briefed
per-record arcs landed (PFS9 Lowering + PFS10 Verification +
PFS11 Aristotelian + pending PFS12 Save-the-Cat-observation);
the Dramatic arcs (PFS13/PFS14) remain gated on dramatic-
sketch-02.
