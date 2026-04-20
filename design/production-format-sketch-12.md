# Production format — sketch 12

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (fourth per-record arc under Production C;
ships the Save-the-Cat self-verifier observation record under the
existing `schema/save_the_cat/` namespace committed by PFS7-N1, per
PFS8-N2's classification that dialect-internal cross-boundary
records live in the dialect's namespace)
**Frames:** [production-format-sketch-07](production-format-
sketch-07.md) PFS7-N1 (Save-the-Cat namespace), PFS7 §Deferred
(StcObservation deferred to a future production sketch);
[production-format-sketch-08](production-format-sketch-08.md)
PFS8-N2 (dialect-internal records stay under `schema/<dialect>/`),
PFS8 §Per-record arc plan item 4 (PFS12 brief);
[production-format-sketch-09](production-format-sketch-09.md)
PFS9-LO1..LO4 (LoweringObservation shape — direct template);
[production-format-sketch-11](production-format-sketch-11.md)
PFS11-AO1..AO4 (ArObservation shape — second instance of the same
template); [save-the-cat-sketch-01](save-the-cat-sketch-01.md) S6
(self-verifier scope — `verify` returns observation tuples);
[save-the-cat-sketch-02](save-the-cat-sketch-02.md) S13 (three
character-layer checks — adds eight new codes to the StcObservation
emission vocabulary); [production-format-sketch-01](production-
format-sketch-01.md) PFS1 (JSON Schema 2020-12), PFS2 (schemas-
first); [production-format-sketch-03](production-format-sketch-03.md)
PFS3-E1 (cross-file `$ref` via registry — registered for symmetry
even though the single record has no outbound refs)
**Related:** [architecture-sketch-02](architecture-sketch-02.md)
A7/A8 (dialect-internal observation vs. shared verification);
[referential-integrity-sketch-01](referential-integrity-sketch-01.md)
RI7 (record-id-resolution audit precedent — applies equally to
StcObservation.target_id resolution banked here as OQ2)
**Superseded by:** nothing yet

## Purpose

**Fourth per-record sketch under Production C.** Ships one JSON
Schema 2020-12 file for the Save-the-Cat self-verifier observation —
`StcObservation` — under the existing `schema/save_the_cat/`
namespace PFS7-N1 committed. Per PFS8-N2: dialect-internal records
(self-verifier observations) ship under the dialect's own
namespace, not under a top-level role-named namespace.

The smallest per-record arc under Production C. PFS9 shipped three
records, PFS10 four, PFS11 four; PFS12 ships one. The shape is
the third instance of the four-field structural-finding pattern
PFS9-LO and PFS11-AO already ship — same template, re-applied to
this dialect's verifier output.

The per-record design work is already done. Save-the-cat-sketch-01
S6 commits the `verify` self-verifier scope; sketch-02 S13 adds
three character-layer checks, expanding the emission vocabulary.
This sketch format-renders the single record; no new field-level
commitments.

## Why now

- **Smallest remaining per-record arc under Production C.** Once
  PFS12 lands, the Production-C tier completes for the substrate
  (PFS1–PFS5) and dialect-core (PFS6–PFS7) layers, plus all four
  cross-boundary arcs (PFS9 Lowering + PFS10 Verification + PFS11
  Aristotelian-cross-boundary + PFS12 Save-the-Cat-observation).
  Only the gated Dramatic / Dramatica-complete arcs (PFS13/PFS14)
  remain.
- **StcObservation is the load-bearing self-verifier output.**
  Every call to `save_the_cat.verify(story, ...)` returns a list
  of StcObservations. Validating the shape at the schema layer
  completes the dialect's output-shape contract (the input side —
  StcCharacter / StcStrand / StcBeat / StcStory — shipped under
  PFS7).
- **Corpus exists (non-zero).** The two Save-the-Cat encodings
  (macbeth, ackroyd) each emit one StcObservation today —
  `genre_archetypes_declared` (NOTED severity, informational
  pointer when the Story declares a genre per S5/S13 surface).
  Two records exercise the validator path; PFS12 is the first
  Production-C arc since PFS9-LO that lands with a non-zero
  observation corpus on first ship.

## Scope — what the sketch covers

**In:**

- One JSON Schema file under `schema/save_the_cat/`:
  - `schema/save_the_cat/observation.json` (`StcObservation` per
    save-the-cat-sketch-01 S6 + sketch-02 S13).
- Dump-layer helper: `_dump_stc_observation`.
- Discovery helper: walks each Save-the-Cat encoding's
  `(STORY, BEATS, STRANDS, CHARACTERS)` and calls `verify(...)`
  to produce observations. Parallels PFS11-D5
  (`_discover_encoding_aristotelian_observations`) which walks
  ArMythos records.
- Registry registration: one new entry. The schema is self-
  contained (no outbound `$ref`), but the registry stays
  symmetric across all dialect + cross-boundary namespaces (PFS7
  precedent: the four Save-the-Cat dialect-core schemas are
  registered though none cross-file-refs anything).
- Three new conformance tests (1 metaschema + 1 shape + 1 corpus),
  following the PFS9-LO / PFS11-AO template.

**Out (banked with forcing functions):**

- `StcCanonicalBeat` (15 shipped-as-data canonical beats from
  `core/save_the_cat.py`). PFS7 OQ2 banked the dialect-catalog
  question. Forcing function: a consumer (walker, markdown parser)
  needs to validate against the canonical sheet. Banked.
- `StcGenre` (10 shipped-as-data Snyder genres from
  `core/save_the_cat.py`). Same PFS7 OQ2 bank. Same forcing
  function shape. Banked.
- Probe-methodology records (no Save-the-Cat probe surface
  exists today). The dialect has no reader-model client; the
  parallels of PFS11's ArAnnotationReview /
  ArObservationCommentary / DialectReading do not exist.
  Forcing function: a Save-the-Cat reader-model probe lands.
  Deferred.
- StructuralAdvisory parallel for Save-the-Cat. The dialect's
  `verify` returns flat StcObservations (severity at the
  observation, no scope tuple). Forcing function: a
  cross-record advisory shape pressures the schema. Banked.
- Referential integrity audits on `StcObservation.target_id`
  (target_id resolves to a StcStory / StcBeat / StcStrand /
  StcCharacter id depending on the emitting check; the schema
  admits any non-empty string). Banked as OQ2; a later RI arc
  would add the audit per RI7's substrate event-ref precedent.
- Close-enum on `StcObservation.code`. Twenty-three stable
  codes as of save-the-cat-sketch-02; extensibility-friendly
  open string per PFS9-LO3 / PFS11-AO3. Banked as OQ1.

**Not the topic:**

- No Python change. The `StcObservation` dataclass already
  exists in `core/save_the_cat.py`; its field shape pre-committed
  by sketch-01 S6. PFS2 discipline: schema shape is source of
  truth; Python conforms to schema. No divergences anticipated
  (the four-field shape is identical to LoweringObservation and
  ArObservation by independent convergence).
- No new architecture claims. PFS8-N2 committed the dialect-
  internal classification; PFS11 was the first arc to exercise
  it. PFS12 is the second.
- No reader-model-client changes. The Save-the-Cat dialect has
  no reader-model client today; if one ships in a future
  sketch, a separate per-record arc would land its
  ArObservationCommentary / DialectReading parallels.

## Commitments

### PFS12-N1 — Namespace inherits PFS7-N1

The new schema lives under `schema/save_the_cat/` — the dialect's
existing namespace. No new top-level subdirectory. Per PFS8-N2:
dialect-internal cross-boundary records (self-verifier output)
share the namespace with the dialect's core records (story / beat
/ strand / character) because they're produced by the dialect
itself, not shared across dialects.

Same posture as PFS11-N1 for the Aristotelian
cross-boundary batch; this is the second arc to exercise PFS8-N2
classification.

This means the `$id` URI is:

- `https://brazilofmux.github.io/story/schema/save_the_cat/observation.json`

### PFS12-O1..O4 — StcObservation record shape

`schema/save_the_cat/observation.json` ships the `StcObservation`
record per save-the-cat-sketch-01 S6 (self-verifier finding).
Third instance of the four-field structural-finding shape PFS9-LO
and PFS11-AO already ship. The convergence is by independent
authorial decision in `core/lowering.py` /
`core/aristotelian.py` / `core/save_the_cat.py` — three modules
arrived at the same `(severity, code, target_id, message)` tuple
without sharing — and the schema lifts the convergence to
schema-level invariant (three records, one shape).

- **PFS12-O1.** Required fields: `severity`, `code`, `target_id`,
  `message`. All four from the Python dataclass. No optionals.
- **PFS12-O2.** `severity` is a **closed enum** at two values:
  `{"noted", "advises-review"}`. Matches
  `core/save_the_cat.py`'s `SEVERITY_NOTED` /
  `SEVERITY_ADVISES_REVIEW` constants. Identical to
  `LoweringObservation` (PFS9-LO2) and `ArObservation`
  (PFS11-AO2); third corpus instance of the same closed
  vocabulary.
- **PFS12-O3.** `code` is an **open non-empty string**. Today's
  S6 + S13 checks emit twenty-three stable codes —
  `beat_id_unresolved`, `strand_id_unresolved`, `genre_unknown`,
  `theme_statement_empty`, `beat_slot_unfilled`,
  `multiple_beats_per_slot`, `page_actual_non_monotonic`,
  `multiple_a_strands`, `multiple_b_strands`,
  `advancement_strand_unresolved`, `genre_archetypes_declared`,
  `character_id_unresolved`, `participant_id_unresolved`,
  `focal_character_id_unresolved`,
  `archetype_character_id_unresolved`, `character_unreferenced`,
  `multiple_protagonists`, `no_protagonist_declared`,
  `archetype_assignment_both_set`,
  `archetype_assignment_neither_set`,
  `archetype_assignments_without_genre`, `archetype_missing`,
  `archetype_duplicated`, `archetype_extraneous`. Open string
  per PFS9-LO3 / PFS11-AO3: new S-checks (or future amendment-
  sketches) don't require a schema amendment. Code vocabulary
  closure deferred to OQ1.
- **PFS12-O4.** `target_id` and `message` are **non-empty
  strings**. `target_id` names the record the observation
  attaches to (a StcStory / StcBeat / StcStrand / StcCharacter
  id depending on the emitting check); resolution banked as OQ2
  (referential-integrity audit). `message` is human-readable
  prose with no length bound.
- **`additionalProperties: false`.**

### PFS12-X — No cross-file `$ref`, no CrossDialectRef

Single-record arc. The schema has no outbound references — no
sub-records, no `$ref`s, no `$defs`. This is the first
Production-C arc since the substrate-tier minimal-shape arcs
(PFS1 Description, PFS2 Entity) to ship without an outbound
`$ref` — a property of the single-record arc's narrow scope, not
a deliberate divergence from PFS9/PFS10/PFS11's pattern.

PFS12 is also the second Production-C arc after PFS11 to ship
without touching CrossDialectRef. Rationale: `target_id` resolves
to an **intra-dialect** id (StcStory / StcBeat / StcStrand /
StcCharacter — the four core records authored under PFS7). No
dialect token needed. Same routing rule PFS11-X3 named: dialect-
internal cross-boundary records route differently than cross-
dialect ones; the namespace boundary is the routing signal.

## Dump-layer commitments

Parallel to PFS9-D6 for LoweringObservation, PFS11-D1 for
ArObservation.

### PFS12-D1 — `_dump_stc_observation(obs) -> dict`

Field-for-field isomorphic. All four fields always emit
(severity, code, target_id, message). No conditional emission —
no optional fields. Identical body to `_dump_lowering_observation`
and `_dump_ar_observation` (three independent functions that
return the same shape; sharing them would require a
cross-namespace import without forcing function — see PFS9
intentional-non-factoring discussion).

### PFS12-D2 — `_discover_encoding_save_the_cat_observations(stories, beats, strands, characters)`

Runs `save_the_cat.verify(story, beats=..., strands=...,
characters=...)` on each Story in each encoding to produce
StcObservation records. Parallels PFS11-D5
(`_discover_encoding_aristotelian_observations`) which walks
ArMythos records. The signature takes the four already-discovered
record kinds rather than re-walking encoding modules — same
discipline PFS11-D5 follows.

The four record-kind tuples come from
`_discover_encoding_save_the_cat_records()` (PFS7-D5), which
walks `*_save_the_cat.py` encoding modules and returns the
quadruple `(stories, beats, strands, characters)`. The
discovery helper threads each per-encoding bundle through
`verify` and accumulates the resulting observations under the
encoding name.

Returns a list of `(encoding_name, observations)` tuples across
all stories in the encoding (singleton today — Save-the-Cat
encodings export exactly one `STORY` per module per PFS7-D5).
Empty lists skip silently per the per-encoding discovery
convention.

### PFS12-D3 — Registry registration

The conformance test's `_build_schema_registry` gains one new
entry: `_load_save_the_cat_observation_schema()`. The schema is
self-contained — no outbound cross-file `$ref` — and could
validate without registry binding, but registration keeps the
registry symmetric across all dialect + cross-boundary namespaces
(PFS7 already registers the four self-contained Save-the-Cat
core schemas for the same reason). Pattern introduced by PFS3-E1
and extended through every subsequent per-record arc.

## Conformance dispositions (anticipated)

No active dispositions anticipated. One **anticipated finding**:

1. **Two StcObservation records in the corpus.** The two
   Save-the-Cat encodings (macbeth, ackroyd) each declare
   `stc_genre_id` per S5; the S5 verifier check
   (`_check_genre_archetypes`) emits a NOTED
   `genre_archetypes_declared` observation as an informational
   pointer for the author. The two records exercise the
   validator path on first ship — distinguishes PFS12 from
   PFS11's clean-corpus zero (where all three Aristotelian
   encodings verify clean and the validator runs only the
   metaschema + shape tests).

The corpus-conformance test asserts `total >= 2` rather than
the PFS11 zero-corpus pattern. If a future encoding suppresses
the genre declaration (or the S5 check changes), the assertion
amends.

## Corpus expectations

Two Save-the-Cat encoding modules contribute to the runtime-
generated corpus:

- `macbeth_save_the_cat.py` (1 STORY: S_macbeth_stc, declares
  `stc_genre_id` — emits 1 NOTED observation).
- `ackroyd_save_the_cat.py` (1 STORY: S_ackroyd_stc, declares
  `stc_genre_id` — emits 1 NOTED observation).

Running `save_the_cat.verify` over the 2 stories with their
respective beats / strands / characters produces **two
StcObservations** — both NOTED severity, both
`genre_archetypes_declared` code, one targeting each story's id.

**Expected corpus counts:**

- **StcObservation**: 2 records — both NOTED `genre_archetypes_
  declared`. Shape validated via metaschema + shape + corpus
  tests; codes counted; severities counted.

**Test assertion posture.** The corpus-conformance test asserts
`total >= 2` to match today's expected non-zero corpus and
`new_findings == []` to surface validator failures. Code and
severity dictionaries print for diagnostic visibility (parallel
to PFS9-LO's corpus-conformance output).

## Open questions

1. **OQ1 — StcObservation.code close-enum.** Today's S6 + S13
   checks emit a stable set of codes (eleven from sketch-01 S6
   + twelve from sketch-02 S13 = twenty-three total). Schema
   admits any non-empty string per PFS12-O3. A close-enum
   commitment could lift Python's emission vocabulary to schema
   level. Deferred: the check set is still growing (sketch-01
   shipped 11; sketch-02 added 12; future amendment-sketches
   would add more — Save-the-Cat is the dialect with the
   largest emission vocabulary today and the most likely to
   keep adding). Forcing function: S-check set stabilizes with
   a PFS-committed close-enum disposition. Parallel to PFS9-LO3
   / PFS11-AO3 / PFS9 OQ5 / PFS11 OQ1. Banked.

2. **OQ2 — Referential integrity on StcObservation.target_id.**
   target_id points at intra-dialect record ids (StcStory /
   StcBeat / StcStrand / StcCharacter depending on the emitting
   check — `_check_id_resolution` targets the Story; checks
   per-beat target the beat; checks per-strand target the
   strand; the character checks target either the character
   id or the story id). The schema admits any non-empty string;
   existence is not checked. A later Tier-2 audit (per
   referential-integrity-sketch-NN) extends coverage. Today:
   two StcObservations in the corpus, both targeting valid
   story ids; the audit surface doesn't forcing-function until
   either (a) a non-trivially-larger corpus exists, or (b) a
   probe emits records with a typo in target_id. Parallels
   PFS9 OQ2 / PFS10 OQ1 / PFS11 OQ3. Banked.

3. **OQ3 — Cross-namespace observation-record convergence.**
   Three Production-C arcs (PFS9-LO, PFS11-AO, PFS12)
   independently shipped the same four-field shape
   (`severity`, `code`, `target_id`, `message`) with the same
   two-value severity enum. Could the three converge on a
   single shared `schema/cross_boundary/observation.json` that
   each dialect re-uses? Decision today: **no**. The three
   records are produced by three different verifiers, target
   different namespaces' record ids, and emit different code
   vocabularies — sharing them at the schema layer would
   couple three independent emission surfaces without
   load-bearing benefit (close to the PFS8-V re-inline-rather-
   than-cross-namespace-couple posture for CrossDialectRef).
   Forcing function: a fourth observation record (e.g., a
   future Dramatic / Dramatica-complete observation under
   PFS13 / PFS14) makes four-of-a-kind too noisy to keep
   un-factored, AND a consumer (walker, CI tooling) needs to
   treat the four uniformly. Banked — both halves of the
   forcing function need to land before convergence is worth
   the coupling cost.

## Discipline

Same-as-always under the PFS2 discipline:

- **Sketches before schema.** Save-the-cat-sketch-01 S6
  committed the verifier-output shape and the
  noted/advises-review severity vocabulary; sketch-02 S13
  added the character-layer checks (and twelve new codes to
  the emission vocabulary). The `SEVERITY_*` constants lift
  to schema-level closed enum.
- **Schemas before code.** No Python change. If a conformance
  issue surfaces, the posture is the same as all prior arcs
  (fix the design sketch first; then schema; then Python).
- **Fourth per-record arc under Production C.** PFS12's
  structure mirrors PFS9 / PFS10 / PFS11 (record commitment
  by record; dump-discovery-registry block; open questions
  banked). The generalization tests that the per-record
  sketch template scales to a single-record arc — same slim
  shape, same commitments-by-record-family, smaller scope.
- **Slim when the design is done.** Target ~330 lines (PFS9
  shipped 600+ for three records; PFS10 shipped 700+ for four
  records; PFS11 shipped 720+ for four records). One record
  with four field-level decisions plus the three-way
  convergence note (PFS12-O / OQ3) shrinks to roughly half
  PFS9's per-record-budget.

## Summary

Fourth per-record sketch under Production C. One JSON Schema
file for the Save-the-Cat self-verifier observation shipped
under `schema/save_the_cat/` — the dialect's existing
namespace, per PFS8-N2's dialect-internal classification.

Six commitments across three families:

- **PFS12-N1** — namespace inherits PFS7-N1
  (`schema/save_the_cat/`).
- **PFS12-O1..O4** — StcObservation shape (required severity /
  code / target_id / message; severity enum {noted,
  advises-review}; code open string; target_id + message
  non-empty strings).
- **PFS12-X** — no cross-file `$ref`, no CrossDialectRef
  (intra-dialect single record).
- **PFS12-D1..D3** — dump helper + discovery helper (runs
  `verify()` on each encoding's story bundle) + registry
  registration.

Three open questions banked with forcing functions:
StcObservation.code close-enum (OQ1); Tier-2 referential-
integrity audit on intra-dialect target_id (OQ2); cross-
namespace observation-record convergence across LO/AO/StcO
(OQ3 — both-halves forcing function: a fourth record AND a
consumer that needs uniform treatment).

No design derivation needed. Save-the-cat-sketch-01 S6 +
sketch-02 S13 committed the record shape; this sketch
format-renders, lifts SEVERITY vocabulary to schema-level
closed enum, hands off to implementation.

Python untouched at the sketch layer. Dump-layer + discovery
+ test-suite extensions land in the implementation commit.
Cross-boundary namespace tier reaches five of five briefed
per-record arcs landed (PFS9 Lowering + PFS10 Verification +
PFS11 Aristotelian + PFS12 Save-the-Cat-observation; the
Dramatic arcs PFS13/PFS14 remain gated on dramatic-sketch-02).
Production C closes for all dialect-internal observation
records the corpus carries today.
