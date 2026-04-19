# Production format — sketch 09

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (first per-record arc under Production C;
ships the first schemas into the `schema/lowering/` namespace
committed by PFS8-N1)
**Frames:** [production-format-sketch-08](production-format-
sketch-08.md) PFS8-N1 (two new top-level namespaces), PFS8-L
(Lowering-family catalog); [lowering-record-sketch-01](lowering-
record-sketch-01.md) L1–L10 (Lowering record shape);
[production-format-sketch-01](production-format-sketch-01.md)
PFS1 (JSON Schema 2020-12), PFS2 (schemas-first);
[production-format-sketch-03](production-format-sketch-03.md)
PFS3-E1 (cross-file `$ref` via registry); [production-format-
sketch-05](production-format-sketch-05.md) PFS5-B5 (allOf/
if-then-else pattern); [production-format-sketch-06](
production-format-sketch-06.md) PFS6-X1 (cross-file `$ref` at
dialect layer); [production-format-sketch-07](production-
format-sketch-07.md) PFS7-X2 (inline `$defs` for id-less sub-
records), PFS7-D1..D6 (dump + discovery + registry pattern)
**Related:** [architecture-sketch-02](architecture-sketch-02.md)
A7 (Lowering as structural coupling);
[lowering-sketch-01](lowering-sketch-01.md) F1–F8 (the four-
kinds finding that scopes Lowering to Realization only);
[lowering-sketch-02](lowering-sketch-02.md) F8 extension
**Superseded by:** nothing yet

## Purpose

**First per-record sketch under Production C.** Ships three JSON
Schema 2020-12 files for the Lowering family — `Lowering`,
`AnnotationReview`, `LoweringObservation` — under the
`schema/lowering/` namespace PFS8-N1 committed. Inline `$defs`
for the three id-less sub-records (`CrossDialectRef`,
`Annotation`, `PositionRange`) live inside `lowering.json` per
PFS7-X2. This is the load-bearing cross-boundary record family:
Lowering is the authored coupling between upper-dialect and
lower-dialect records, and every `*_lowerings.py` encoding
module emits records validated by this schema.

The per-record design work is already done. Lowering-record-
sketch-01 L1–L10 commit the Lowering shape; validate_lowerings
in `core/lowering.py` commits the LoweringObservation shape by
emitting exactly one record type from one code path. This
sketch is format-rendering — the sixth under PFS2's
"sketches-first, Python-as-conformance" discipline.

## Why now

- **PFS8-N1 committed the namespace.** `schema/lowering/` is
  decided; PFS9 can ship without a namespace-decision dependency.
- **Lowering is the most load-bearing cross-boundary record.**
  The substrate + dialect layers connect through Lowering; every
  dramatica-complete → substrate verifier reads Lowerings to
  resolve its CrossDialectRef targets; every `*_lowerings.py`
  encoding authors them. Validating the shape at the schema
  layer is the strongest port-readiness claim Production C can
  produce.
- **Corpus is dense.** Seven `*_lowerings.py` modules across
  six encodings (Oedipus, Macbeth, Ackroyd, Rocky, Rashomon
  substrate; Macbeth and Ackroyd save_the_cat); one empty-by-
  design (`and_then_there_were_none_lowerings.py` = scaffolded
  for future). Conservative estimate: 150+ Lowering records +
  zero authored AnnotationReviews + runtime-generated
  LoweringObservations (from validate_lowerings) in today's
  corpus.
- **PFS10 depends on PFS9's CrossDialectRef decision.** The
  Verification family records (VerificationReview,
  StructuralAdvisory, etc.) all carry CrossDialectRef. PFS8-V
  deferred the decision to PFS10 with "prefer re-inlining"
  guidance; PFS9 ships CrossDialectRef first so PFS10 has
  something to re-inline from.

## Scope — what the sketch covers

**In:**

- Three JSON Schema files under `schema/lowering/`:
  - `schema/lowering/lowering.json` (`Lowering` per L1–L10 +
    inline `$defs/cross_dialect_ref` + `$defs/annotation` +
    `$defs/position_range`).
  - `schema/lowering/annotation_review.json` (`AnnotationReview`;
    same shape as substrate ReviewEntry plus no anchor-to-field
    requirement).
  - `schema/lowering/lowering_observation.json`
    (`LoweringObservation`; severity + code + target_id +
    message).
- The **conditional `status=active` ⇒ non-empty lower_records**
  clause via `allOf/if-then-else` (PFS9-X3; parallels PFS5-B5's
  shape).
- Cross-file `$ref` from Annotation's `review_states` array to
  `annotation_review.json` (PFS9-X2; parallels PFS6-X1's tree-
  with-inline-$ref pattern, extended across the lowering-
  namespace boundary rather than the dialect-namespace boundary).
- Dump-layer helpers: `_dump_lowering`, `_dump_annotation_review`,
  `_dump_lowering_observation` + inline sub-record helpers
  (`_dump_cross_dialect_ref`, `_dump_annotation`,
  `_dump_position_range`). Discovery helper
  `_discover_encoding_lowerings`. Registry registration for
  three new schemas.
- Conformance-test extension: nine new tests (3 metaschema + 3
  shape + 3 corpus).
- `schema/README.md` sweep: new top-level subsection for
  `schema/lowering/` under a new "Cross-boundary layer"
  supersection; "What's deferred" list updated.

**Out:**

- Verification-family records (PFS10 concern).
- Dialect-internal observation records (PFS11 / PFS12 concern).
- Validation of probe-result JSONs (`reader_model_*_output.json`)
  — those embed AnnotationReview + VerifierCommentary records in
  mixed structures; PFS10 will decide whether those JSONs get a
  dedicated container-schema or stay as informal debug artifacts.
- Any amendment to Lowering's shape in Python. Lowering's design
  is committed under lowering-record-sketch-01.
- `Lowering.metadata` deep validation. Per PFS8 OQ1, metadata is
  an open object — the schema admits arbitrary keys (matches
  substrate-sketch-05's posture). Per-key schemas (e.g., a
  `supersedes` key's shape) are out of scope; the verifier's
  `validate_lowerings` already checks `supersedes` / `superseded_by`
  referential consistency.
- Dialect-token validation on `CrossDialectRef.dialect`. Per
  PFS8 OQ3 — close-enum vs. open string. This sketch commits the
  posture: **leave open** — any non-empty string accepted;
  typo-detection is a runtime concern (verifier-layer audit),
  not a schema concern. Rationale in PFS9-X4 below.

## Commitments

### PFS9-N1 — Lowering family under `schema/lowering/`

Inherits PFS8-N1 (`schema/<role>/<record>.json` subdirectory-per-
role at the top-level cross-boundary tier). The role token is
`lowering`, matching the Python module name (`core/lowering.py`).

**`$id` URIs:**

- `https://brazilofmux.github.io/story/schema/lowering/lowering.json`
- `https://brazilofmux.github.io/story/schema/lowering/annotation_review.json`
- `https://brazilofmux.github.io/story/schema/lowering/lowering_observation.json`

**Precedent validation.** First landing under the new cross-
boundary top-level namespace tier. PFS10 (Verification family)
will ship under `schema/verification/` by the same rule.

### PFS9-L1..L10 — Lowering record shape

`schema/lowering/lowering.json` ships the `Lowering` record per
lowering-record-sketch-01 L1–L10. Nine field commitments + one
conditional clause.

- **PFS9-L1.** Required fields: `id`, `upper_record`,
  `lower_records`, `annotation`, `status`. Five required fields
  — `status` is required even though the Python has a default
  (`LoweringStatus.ACTIVE`) because the PFS7 convention is
  isomorphic dump: if the Python always carries it, the schema
  requires it, and the dump emits it.
- **PFS9-L2.** `id` is a non-empty string (per L2).
- **PFS9-L3.** `upper_record` is a `CrossDialectRef` object per
  `#/$defs/cross_dialect_ref` (inline per PFS9-X1). Per L2 —
  the single upper record this Lowering realizes; many-to-many
  at the collection level (multiple Lowerings can share an
  upper_record), one-to-many at the record level (one Lowering
  points at one upper).
- **PFS9-L4.** `lower_records` is an array of `CrossDialectRef`
  objects per `#/$defs/cross_dialect_ref`. Per L3 + L8 —
  multiple lower records per Lowering are first-class; empty
  array admitted but only under PENDING status (the L8
  conditional below enforces this).
- **PFS9-L5.** `annotation` is an `Annotation` object per
  `#/$defs/annotation` (inline per PFS9-X1). Per L5 — the
  prose rationale carried on the Lowering.
- **PFS9-L6.** `authored_by` is an optional string (Python
  default `"author"`; dump emits unconditionally per PFS6-D2
  precedent).
- **PFS9-L7.** `τ_a` is an optional integer (Python default
  `0`; dump emits unconditionally). Per L6 — the Lowering's
  own authored τ_a, distinct from `anchor_τ_a` (which snapshots
  the lower side's τ_a at author time for staleness).
- **PFS9-L8.** `status` is a **closed enum** at two values:
  `{"active", "pending"}`. Matches Python's `LoweringStatus`
  enum per L8.
- **PFS9-L9.** `position_range` is an **optional**
  `PositionRange` object per `#/$defs/position_range` (inline
  per PFS9-X1). Per L7 — present only when the upper and lower
  dialects both use positional ordering and the Lowering covers
  a range.
- **PFS9-L10.** `anchor_τ_a` is an **optional integer** per L6.
  Python default `None`; dump omits when None (matches PFS6-D3
  `character_ref_id` precedent).
- **`metadata`** is an **optional object** with
  `additionalProperties: true` per PFS8 OQ1. Admits any keys.
  Dump emits only when the dict is non-empty (PFS6 precedent
  on empty-default omission). No per-key schema today; the
  validate_lowerings verifier carries referential-integrity
  checks for known keys (`supersedes`, `superseded_by`).
- **`additionalProperties: false`** at the top level of the
  Lowering schema — only declared properties admitted. The
  exception is `metadata` itself (the nested object admits
  open keys).

### PFS9-AR1..AR4 — AnnotationReview shape

`schema/lowering/annotation_review.json` ships the
`AnnotationReview` record.

- **PFS9-AR1.** Required fields: `reviewer_id`,
  `reviewed_at_τ_a`, `verdict`, `anchor_τ_a`.
- **PFS9-AR2.** `reviewer_id` is a non-empty string.
  `reviewed_at_τ_a` and `anchor_τ_a` are integers.
- **PFS9-AR3.** `verdict` is a **closed enum** at four values:
  `{"approved", "needs-work", "rejected", "noted"}`. Matches
  Python's `VERDICT_*` constants.
- **PFS9-AR4.** `comment` is an **optional string**. Python
  default `None`; dump omits when None (PFS6-D3 precedent).
- **`additionalProperties: false`.**

### PFS9-LO1..LO4 — LoweringObservation shape

`schema/lowering/lowering_observation.json` ships the
`LoweringObservation` record.

- **PFS9-LO1.** Required fields: `severity`, `code`,
  `target_id`, `message`. All four required — the Python
  dataclass has no defaults, so the schema matches.
- **PFS9-LO2.** `severity` is a **closed enum** at two values:
  `{"noted", "advises-review"}`. Matches Python's `validate_
  lowerings` implementation, which hard-codes these two
  severities across its four emission sites.
- **PFS9-LO3.** `code` is a non-empty string. No closed enum —
  `validate_lowerings` emits four codes today
  (`lowering_id_duplicate`, `pending_lowering_has_records`,
  `annotation_attention_unknown`, `supersedes_unresolved`,
  `supersession_back_reference_missing` — five actually) but
  future checks can add codes without a schema amendment. The
  schema admits any non-empty string per the extension-over-
  restriction discipline.
- **PFS9-LO4.** `target_id` and `message` are non-empty
  strings.
- **`additionalProperties: false`.**

### PFS9-X1 — Inline `$defs` for id-less sub-records

Three Lowering-family sub-records ship as inline `$defs` inside
`lowering.json` per the PFS7-X2 convention (sub-records without
authorial ids + single parent context):

- **`$defs/cross_dialect_ref`** — the `CrossDialectRef` shape.
  Required `dialect` (non-empty string) + `record_id` (non-empty
  string). `additionalProperties: false`.
- **`$defs/annotation`** — the `Annotation` shape. Required
  `text` (string, may be empty). Optional `attention` as closed
  enum `{"structural", "interpretive", "flavor"}` matching
  Python's `ATTENTION_*` constants. Optional `authored_by`
  string. Optional `review_states` as array of
  `AnnotationReview` objects via **cross-file `$ref`** to
  `annotation_review.json` (PFS9-X2 below).
  `additionalProperties: false`.
- **`$defs/position_range`** — the `PositionRange` shape.
  Required `coord` (non-empty string), `min_value` (integer),
  `max_value` (integer). `additionalProperties: false`.

**Why inline rather than sibling files.** CrossDialectRef,
Annotation, and PositionRange all lack authorial ids and
appear only within Lowering's tree (CrossDialectRef also
appears across the verification namespace — handled separately
in PFS10 per PFS8-V guidance: re-inline rather than $ref
across namespaces). Inline `$defs` matches PFS7-X2's rule and
keeps `schema/lowering/` to three files rather than six.

### PFS9-X2 — Cross-file `$ref` from Annotation to AnnotationReview

`$defs/annotation.review_states.items` uses a `$ref` to
`https://brazilofmux.github.io/story/schema/lowering/
annotation_review.json`. The registry pattern (PFS3-E1;
extended by PFS4, PFS6-X1) resolves the cross-file reference.

**Why `$ref`, not inline for AnnotationReview.** Unlike the
three sub-records PFS9-X1 inlines, `AnnotationReview` is used
in **two contexts**: (1) inside `Annotation.review_states` as
shown here; and (2) as a standalone probe output — the reader-
model probe emits AnnotationReview records directly via
`annotation_review_candidates` on its result container. The
two-context rule from PFS7-X2 promotes it to a sibling file.

**The pattern extends.** PFS6-X1 applied cross-file `$ref` at
the dialect-namespace boundary (ArMythos → ArPhase within
`schema/aristotelian/`). PFS9-X2 applies it within a single
cross-boundary namespace (Annotation → AnnotationReview within
`schema/lowering/`). Same registry-based resolution, same
isomorphic-to-Python shape rule.

### PFS9-X3 — `status="active"` requires non-empty `lower_records`

Per L8's Python `__post_init__`: an ACTIVE Lowering whose
`lower_records` is empty raises `ValueError` at construction.
The schema expresses this via `allOf/if-then-else` — same
structural pattern as PFS5-B5 (Branch's kind-conditional
parent) and PFS6-M6 (Mythos's plot-kind-conditional peripeteia/
anagnorisis).

```json
"allOf": [{
  "description": "L8: ACTIVE status requires at least one lower_record.",
  "if": {
    "properties": {"status": {"const": "active"}},
    "required": ["status"]
  },
  "then": {
    "properties": {
      "lower_records": {"minItems": 1}
    },
    "required": ["lower_records"]
  }
}]
```

**PENDING Lowerings admit empty `lower_records`** per L8
(promissory bindings authored against upper records whose lower
realization doesn't yet exist).

The verifier (validate_lowerings) emits
`pending_lowering_has_records` as a NOTED observation when a
PENDING has records; the schema does **not** enforce that
direction (it's a "did you mean to flip to ACTIVE?" nudge, not
a structural violation). Only the ACTIVE-empty case is a
structural violation the schema catches.

### PFS9-X4 — `CrossDialectRef.dialect` is an open string

Per PFS8 OQ3's deferral to PFS9: the `dialect` field on
`CrossDialectRef` is a non-empty string with **no closed enum**.
Today's corpus uses five dialect tokens (`substrate`,
`dramatic`, `dramatica_complete`, `aristotelian`,
`save_the_cat`), but architecture-sketch-02 A6 commits to
"dialects are plural, extensibility is first-class."

**Rationale for open.** A close-enum would catch typos at the
schema layer (useful) but would forbid author-defined dialects
at the architecture's commitment cost (not useful). The
verifier surface already provides runtime typo detection: any
unknown dialect token in a CrossDialectRef will fail to resolve
in the Lowering verifier's cross-dialect lookup. The schema
stays consistent with the extensibility commitment; the
verifier catches the typo case at a layer that already does.

**Banking for reversal.** If a dialect-token typo surfaces in
the corpus that the verifier missed (e.g., a Lowering whose
target records never get queried so the typo goes undetected),
PFS9-X4 may flip to a close-enum posture. Forcing function:
the first such typo.

## Dump-layer commitments

Parallel to PFS5-D1/D2 for Branch, PFS6-D1..D3 for Aristotelian
core, and PFS7-D1..D4 for Save-the-Cat core.

### PFS9-D1 — `_dump_lowering(lowering: Lowering) -> dict`

Field-for-field isomorphic. Required fields (id,
upper_record, lower_records, annotation, status) always emit.
`authored_by` and `τ_a` emit unconditionally (Python defaults,
PFS6-D2 precedent). `position_range` omitted when None.
`anchor_τ_a` omitted when None. `metadata` omitted when empty
dict (PFS-convention on empty-default omission). Nested
records (`upper_record`, each of `lower_records`, `annotation`,
`position_range`) rendered via sub-dump helpers below.

### PFS9-D2 — `_dump_cross_dialect_ref(ref) -> dict`

Field-for-field: `{dialect, record_id}`. Both required, both
non-empty strings per the Python dataclass.

### PFS9-D3 — `_dump_annotation(annotation) -> dict`

Field-for-field. `text` always emitted (Python no-default-but-
potentially-empty-string; schema requires). `attention` emits
unconditionally (default `"structural"`). `authored_by`
unconditional (default `"author"`). `review_states` emits as
array (empty tuple → empty array); each element rendered via
`_dump_annotation_review`.

### PFS9-D4 — `_dump_annotation_review(review) -> dict`

Field-for-field. `reviewer_id`, `reviewed_at_τ_a`, `verdict`,
`anchor_τ_a` always emitted. `comment` omitted when None.

### PFS9-D5 — `_dump_position_range(pr) -> dict`

Field-for-field: `{coord, min_value, max_value}`.

### PFS9-D6 — `_dump_lowering_observation(obs) -> dict`

Field-for-field: `{severity, code, target_id, message}`. All
four always emit.

### PFS9-D7 — `_discover_encoding_lowerings(modules)`

Walks encoding modules for `LOWERINGS` attribute. Returns a
list of `(encoding_name, lowerings_list)` tuples. Parallel to
PFS5's `_discover_encoding_branches` (which walks
`ALL_BRANCHES`) and PFS6-D4 / PFS7-D5 (which walk dialect-
specific module attrs).

**Filename filter.** Walks `prototype/story_engine/encodings/
*_lowerings.py` only — that's the canonical `*_lowerings.py`
module naming, following PFS7-D5's base-file pattern (no
sibling `_verification.py` pollution today, but the filter is
defensive).

**Empty-tuple handling.** `and_then_there_were_none_lowerings.py`
exports `LOWERINGS: tuple = ()`. Discovery skips empty tuples
(consistent with substrate-layer discovery helpers' behavior
per `_discover_encoding_records`).

### PFS9-D8 — Registry registration

The conformance test's `_build_schema_registry` gains three
new entries: `lowering.json`, `annotation_review.json`,
`lowering_observation.json`. The registry is load-bearing
here — `lowering.json`'s inline `$defs/annotation` refs
`annotation_review.json` cross-file.

## Conformance dispositions (anticipated)

No active dispositions anticipated. Three **anticipated non-
findings**:

1. **`annotation.review_states` empty tuple in every corpus
   Lowering.** The `*_lowerings.py` encodings don't author
   AnnotationReview records (those land from the reader-model
   probe output, which is a downstream concern). Schema admits
   empty arrays cleanly; no disposition.

2. **`metadata` empty dict default-omitted vs. set with
   `supersedes` / `superseded_by`.** Corpus Lowerings carry
   metadata only when supersession is authored; most carry
   empty dicts. Schema's open `additionalProperties: true`
   admits both cases; no disposition.

3. **`anchor_τ_a=None` on Character → Entity Lowerings.**
   Per oedipus_lowerings.py's docstring: "Entities have no τ_a
   ... Character → Entity Lowerings have anchor_τ_a=None —
   staleness is undefined for those." Dump omits when None;
   schema admits absence. Intentional by design. No
   disposition.

## Corpus expectations

Seven `*_lowerings.py` modules contribute to the authored
corpus:

- `oedipus_lowerings.py`
- `macbeth_lowerings.py`
- `ackroyd_lowerings.py`
- `rocky_lowerings.py`
- `rashomon_lowerings.py`
- `macbeth_save_the_cat_lowerings.py`
- `ackroyd_save_the_cat_lowerings.py`
- `and_then_there_were_none_lowerings.py` (empty-by-design;
  discovery skips empty tuples).

**Expected corpus counts** (approximate; conformance test
will report exact numbers on landing):

- **Lowering**: 150+ records across the seven populated
  `*_lowerings.py` modules.
- **AnnotationReview**: zero in today's corpus (no encoding
  authors review_states; future probe-walker-authored reviews
  will populate).
- **LoweringObservation**: runtime-generated by
  `validate_lowerings(lowerings)`. Corpus conformance runs
  `validate_lowerings` against each encoding's LOWERINGS tuple
  and validates each emitted LoweringObservation. Expected:
  zero observations on a clean corpus (otherwise the
  encoding has a self-consistency issue that pre-dates PFS9).

Every corpus record expected to validate clean under the
implementation. If a non-finding materializes as a true
conformance issue, this sketch gains a §Dispositions section
(none anticipated).

## Open questions

1. **OQ1 — `metadata` per-key schemas.** PFS8 OQ1 noted that
   `Lowering.metadata` is an open object. Known keys today:
   `supersedes` (Lowering id), `superseded_by` (Lowering id).
   A future amendment could enumerate these via a
   `patternProperties` or per-key validators if a forcing
   function argues. Forcing function: a third well-defined
   metadata key lands and starts looking like a vocabulary.

2. **OQ2 — AnnotationReview corpus-discovery strategy.**
   `AnnotationReview` records land inside `Annotation.
   review_states` (authored) AND as standalone probe output
   (saved in `reader_model_*_output.json` files, not
   authored). The corpus conformance test walks the former
   path (discovers AnnotationReview through Lowering →
   Annotation → review_states). The latter path is **not**
   walked today — probe JSONs are runtime artifacts, not
   corpus. If PFS10 or a future sketch decides to schemafy
   the probe-container shape, that sketch picks up
   probe-side AnnotationReview validation.

3. **OQ3 — `Lowering.τ_a` vs. `Lowering.anchor_τ_a` field-
   name audit.** The Python carries both: `τ_a` for the
   Lowering's own authored timestamp and `anchor_τ_a` for the
   lower-side snapshot. JSON field names use Greek τ in both.
   Field-name clarity is a Python-level concern; schema just
   mirrors. Banked in case a port prefers ASCII field names
   (`tau_a` / `anchor_tau_a`) at the JSON layer.

4. **OQ4 — Closed enum for `annotation.attention`.** The
   Python has exactly three canonical values: `"structural"`,
   `"interpretive"`, `"flavor"`. `validate_lowerings` emits
   `annotation_attention_unknown` on any other value. Schema
   ships with closed enum (PFS9-X1 above); this commits the
   three-value vocabulary at the schema layer, parallel to
   `verdict`'s closed enum. Reversal path: if a legitimate
   fourth attention value surfaces from a design forcing
   function, the schema enum grows.

5. **OQ5 — `LoweringObservation.code` vocabulary.** PFS9-LO3
   leaves code as an open string because `validate_lowerings`
   is extensible. A future sketch could enumerate the stable-
   today codes (`lowering_id_duplicate`,
   `pending_lowering_has_records`,
   `annotation_attention_unknown`, `supersedes_unresolved`,
   `supersession_back_reference_missing`) if a consumer wants
   to branch on them at validator time. Forcing function: a
   downstream walker that types its logic on observation
   codes.

## Discipline

Same-as-always under the PFS2 discipline:

- **Sketches before schema.** Lowering-record-sketch-01 L1–L10
  did the design-layer work for the primary record.
  LoweringObservation's shape is committed by its single Python
  emission site (`validate_lowerings`); the sketch lifts that
  to schema-level per the same discipline that lifted substrate
  docstring claims in substrate-knowledge-fold-sketch-01 KF1–KF5.
- **Schemas before code.** No Python change is anticipated.
  If a conformance issue surfaces, the posture is the same as
  all prior arcs: amend the design sketch first; then schema;
  then Python.
- **First per-record arc under Production C sets precedent for
  the next four.** PFS9-X1 (inline $defs), PFS9-X2 (cross-file
  $ref within a cross-boundary namespace), PFS9-X3 (conditional
  allOf/if-then-else), PFS9-X4 (open dialect-token string),
  and PFS9-D7 (lowerings-suffix discovery) all carry forward.
  PFS10 will cite PFS9 the way PFS5 cited PFS3, and PFS7 cited
  PFS6.
- **Slim when the design is done.** Same discipline as PFS5 /
  PFS6 / PFS7. Three records + inline sub-records is a moderate
  scope; expected to land at ~650 lines (similar to PFS7).

## Summary

First per-record sketch under Production C. Three JSON Schema
files for the Lowering family shipped under `schema/lowering/`
— the first records under the cross-boundary namespace tier
PFS8-N1 committed. Twenty-four commitments:

- **PFS9-N1** — namespace inherits PFS8-N1 (`schema/lowering/`).
- **PFS9-L1..L10** — Lowering shape (required
  id/upper_record/lower_records/annotation/status; status enum
  {active, pending}; optional position_range / anchor_τ_a /
  metadata; inline $defs for cross_dialect_ref / annotation /
  position_range).
- **PFS9-AR1..AR4** — AnnotationReview shape (required
  reviewer_id/reviewed_at_τ_a/verdict/anchor_τ_a; verdict enum
  {approved, needs-work, rejected, noted}; optional comment).
- **PFS9-LO1..LO4** — LoweringObservation shape (required
  severity/code/target_id/message; severity enum
  {noted, advises-review}; code open string).
- **PFS9-X1** — inline `$defs` for CrossDialectRef,
  Annotation, PositionRange.
- **PFS9-X2** — cross-file `$ref` from Annotation.review_states
  to annotation_review.json (extends PFS6-X1's pattern into the
  cross-boundary namespace).
- **PFS9-X3** — allOf/if-then-else: status=active requires
  non-empty lower_records (L8 conditional, parallel to PFS5-B5
  and PFS6-M6).
- **PFS9-X4** — CrossDialectRef.dialect is an open string
  (honors architecture-sketch-02 A6's extensibility
  commitment).
- **PFS9-D1..D8** — dump helpers (6) + discovery helper +
  registry registration.

Five open questions banked with forcing functions: metadata
per-key schemas (OQ1, future); AnnotationReview corpus-discovery
from probe JSONs (OQ2, PFS10 or future); τ_a / anchor_τ_a field-
name ASCII alternative (OQ3, port-driven); attention closed-enum
reversal path (OQ4, future); LoweringObservation.code vocabulary
(OQ5, consumer-driven).

No design derivation needed. lowering-record-sketch-01 already
committed the record shape; this sketch renders it as JSON
Schema 2020-12, lifts validate_lowerings's severity + code + target
emission pattern to schema-level commitments, and hands off to
implementation.

Python untouched at the sketch layer. Dump-layer + discovery +
test-suite extensions land in the implementation commit.
Cross-boundary namespace tier opens with the load-bearing record
first; PFS10 (Verification family) follows, gated on this
sketch's CrossDialectRef decision (re-inlined, per PFS8-V's
guidance).
