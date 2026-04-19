# Production format — sketch 08

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (opens a new top-level namespace tier —
cross-boundary records, above the substrate layer and the dialect
layer)
**Frames:** [production-format-sketch-06](production-format-
sketch-06.md) PFS6-N1 (dialect namespace convention);
[production-format-sketch-07](production-format-sketch-07.md)
PFS7-X1 (flat-with-id-refs topology) + PFS7-X2 (inline `$defs`
for id-less sub-records); [lowering-record-sketch-01](lowering-
record-sketch-01.md) L1–L10 (Lowering record shape);
[verification-sketch-01](verification-sketch-01.md) V1–V8
(verification output vocabulary); [aristotelian-probe-sketch-01](
aristotelian-probe-sketch-01.md) APS1–APS6 (dialect-flavored
probe records); [reader-model-sketch-01](reader-model-sketch-01.md)
R1–R6 (probe I/O contract)
**Related:** [architecture-sketch-02](architecture-sketch-02.md)
A7 (Lowering as structural coupling) + A8 (verification as
observational coupling); [lowering-sketch-01](lowering-sketch-01.md)
F1/F6 (Lowering and verification are architecturally distinct)
**Superseded by:** nothing yet

## Purpose

**Production C opener.** Decides the namespace for all cross-
boundary records — records that sit above the substrate + dialect
layers, connecting them (Lowering), reviewing them
(AnnotationReview), or observing them (VerificationReview,
StructuralAdvisory, VerifierCommentary, and the dialect-flavored
observation/commentary/reading records). Commits two new top-
level subdirectories (`schema/verification/`, `schema/lowering/`)
for dialect-agnostic cross-boundary records; extends PFS6-N1 to
cover dialect-internal / dialect-flavored records (which stay
under `schema/<dialect>/`); briefs the per-record sketches that
will ship the actual schemas.

**No schemas ship in this arc.** This is a **namespace +
classification** sketch, parallel to PFS6-N1's namespace decision
but at the top-level map rather than the per-dialect level.
The per-record sketches (PFS9 onward) ship the schema files.

## Why now

- **Dialect-layer schema arc has closed two-of-four** (state-of-
  play-09's headline + PFS7's landing). The dialect namespace
  convention is load-bearing across two structurally different
  dialects (Aristotelian's tree-with-inline-$ref topology vs.
  Save-the-Cat's flat-with-id-refs topology); its twin at the
  cross-boundary tier can be committed without guesswork.
- **Cross-boundary records are the next-up-the-stack work.**
  Every per-record sketch would benefit from a committed
  namespace — if PFS9 ships Lowering first, PFS9 would have to
  decide the namespace at the same time as the record shape,
  repeating the PFS6-N1 decision.
- **Multiple deferred records are converging.** `ArObservation`
  (PFS6 OQ1), `StcObservation` (PFS7 OQ1), `Lowering`,
  `VerificationReview`, `StructuralAdvisory`, `VerifierCommentary`,
  and the Aristotelian probe records (`ArAnnotationReview`,
  `ArObservationCommentary`, `DialectReading`) all route through
  this tier. Sequencing them needs a shared namespace decision up
  front.
- **A one-commit opener is the right shape.** The namespace
  decision is small but load-bearing (same as PFS6-N1); per-
  record shape commitments do not belong in the same commit.

## Scope — what the sketch covers

**In:**

- Two new top-level schema subdirectories committed as convention
  (`schema/verification/` + `schema/lowering/`).
- Extension of PFS6-N1 to cover dialect-internal records
  (self-verifier observations, dialect-flavored reviews, probe
  methodology records).
- Classification of every known cross-boundary record type to its
  target namespace (or to deferred / out-of-scope).
- Per-record sketch briefs as follow-ons (PFS9, PFS10, PFS11,
  PFS12). Each follow-on's expected scope and dependencies.
- OQs for ephemeral / runtime records (verifier registry,
  probe-result containers) — deferred with forcing-function
  criteria.

**Out:**

- Record-shape commitments. The per-record sketches (PFS9+)
  ship those. This sketch only commits *where* records will
  live and *what categories* they fall into.
- Dump-layer helpers, discovery helpers, conformance tests —
  per-record sketch concerns.
- Any amendment to record shapes in the Python prototype — no
  code change accompanies this sketch.
- Dramatic / Dramatica-complete dialect-internal records.
  Dramatic observations ship with the Dramatic dialect schema
  (gated on dramatic-sketch-02 per PFS6 OQ2);
  Dramatica-complete observations similarly gated on the
  Template schemas.

## Commitments

### PFS8-N1 — Two new top-level namespaces for dialect-agnostic cross-boundary records

Cross-boundary records that apply across any dialect live under
two new top-level subdirectories:

- `schema/lowering/` — the **structural-coupling family**.
  Records that encode authored realization bindings between
  upper-dialect records and lower-dialect records.
- `schema/verification/` — the **observation-shaped family**.
  Records that encode verifier verdicts, advisories,
  commentaries, and verifier-sourced proposals — dialect-
  agnostic outputs of the verifier surface.

**`$id` URI pattern.** Same as PFS6-N1:
`https://brazilofmux.github.io/story/schema/<role>/<record>.json`.

**Why two, not one.** The alternative considered was a single
`schema/cross_boundary/` catch-all subdirectory. Rejected:

- **Different functional roles.** Lowering is *structural*
  (encodes a coupling that exists in the authored record set).
  Verifier output is *observation-shaped* (encodes a finding
  *about* the record set). These are architecturally different
  per architecture-sketch-02 A7 / A8; lowering-sketch-01's
  F1/F6 findings explicitly say Lowering and verification are
  not reducible to each other. The namespace reflects that
  distinction rather than flattening it.
- **Different consumer sets.** A port reading the Lowering
  family needs the coupling records to render or author
  realization bindings; a port reading the verification family
  needs the observation records to render verifier output.
  Keeping them side-by-side is fine — in-one-bucket would
  obscure that a new reader can absorb one side without the
  other.
- **Different evolution cadence.** Lowering's shape is
  committed (lowering-record-sketch-01 L1–L10, ten
  commitments). Verification output evolves with the
  probe/verifier coordination pattern (verification-sketch-01
  V1–V8; ongoing). Separate subdirs let each family's README
  narrative name its own evolution story.

**Why not more, either.** Finer-grained subdivision
(`schema/reviews/`, `schema/advisories/`, `schema/proposals/`)
would over-fragment a small number of tightly related records.
Four verification records share a close coupling (VerifierCommentary
refers to a VerificationReview's verdict); splitting them across
subdirectories would complicate `$ref` resolution without clarifying
anything.

### PFS8-N2 — Dialect-internal records live under `schema/<dialect>/` (extends PFS6-N1)

Records produced by OR authored for a single dialect — including
self-verifier observations, dialect-flavored prose reviews, and
probe-methodology records — live under the dialect's existing
namespace:

- `schema/aristotelian/observation.json` (`ArObservation`)
- `schema/aristotelian/annotation_review.json`
  (`ArAnnotationReview`)
- `schema/aristotelian/observation_commentary.json`
  (`ArObservationCommentary`)
- `schema/aristotelian/dialect_reading.json` (`DialectReading`)
- `schema/save_the_cat/observation.json` (`StcObservation`) —
  PFS7 OQ1.
- `schema/dramatica_complete/observation.json`
  (`DramaticaObservation`) — future; gated on Dramatic dialect
  schemas (PFS6 OQ2).

**Rationale — same discipline as PFS6-N1.** Dialect records vary
in shape across dialects (`ArObservation` carries Aristotelian-
flavored severity codes; `StcObservation` carries Save-the-Cat-
flavored codes; `ArAnnotationReview` targets prose fields
specific to Aristotelian records). Carrying them in their
dialect namespace keeps each dialect a self-contained schema
tree — a port reading the Aristotelian dialect gets both the
authored records AND the observation / review shapes in one
directory.

**Extension beyond PFS6-N1.** PFS6-N1 committed the convention
for *authored* dialect records (ArMythos, ArPhase, ArCharacter;
StcStory, StcBeat, StcStrand, StcCharacter). PFS8-N2 extends it
to dialect-*produced* records (verifier output, probe commentary,
dialect-methodology reading) — same namespace, same `$id`
pattern. The classification principle:

> **What a dialect produces OR what the dialect alone consumes
> lives in the dialect's namespace; what is shared across
> dialects lives in a top-level role-named namespace.**

### PFS8-L — Lowering-family namespace catalog

Under `schema/lowering/`:

- `lowering.json` — the `Lowering` record (lowering-record-
  sketch-01 L1–L10). Encodes a realization binding from one
  upper-dialect record to one or more lower-dialect records;
  carries `CrossDialectRef` pairs, authored annotation, status
  (active/pending), optional position range, optional
  anchor_τ_a for staleness, metadata dict.
- `annotation_review.json` — the `AnnotationReview` record
  (review act on a Lowering's annotation; mirrors substrate
  ReviewEntry shape with verdict ∈ {approved, needs-work,
  rejected, noted}).
- `lowering_observation.json` — the `LoweringObservation`
  record (self-consistency finding from
  `validate_lowerings`; severity ∈ {noted, advises-review}).

**Inline sub-records per PFS7-X2.** `CrossDialectRef`,
`Annotation`, and `PositionRange` do not carry authorial ids
and are used only within Lowering; they ship as inline `$defs`
inside `lowering.json` per the PFS7-X2 convention. The
`Annotation` record has nested `review_states:
tuple[AnnotationReview, ...]` — `AnnotationReview` is cross-
referenced via `$ref` to `annotation_review.json` since the
same record also flows through the proposal queue outside
Lowering context (the reader-model probe produces them as
typed output via `annotation_review_candidates`).

**Per-record sketch follow-on: PFS9 — Lowering family.**
Expected 3 files + inline sub-record `$defs`. Inherits PFS6-X1's
cross-file `$ref` pattern (Annotation's `review_states` →
`annotation_review.json`). Corpus: existing Lowerings under
`*_lowerings.py` and `*_save_the_cat_lowerings.py` encodings.

### PFS8-V — Verification-family namespace catalog

Under `schema/verification/`:

- `verification_review.json` — the `VerificationReview` record
  (verifier verdict on a specific CrossDialectRef target;
  carries `match_strength` ∈ [0,1] for partial-match verdicts).
- `structural_advisory.json` — the `StructuralAdvisory` record
  (pattern observation spanning multiple records; `scope` is
  a tuple of CrossDialectRef).
- `verification_answer_proposal.json` — the
  `VerificationAnswerProposal` record (verifier-sourced
  proposal answering an upper-dialect question-Description).
- `verifier_commentary.json` — the `VerifierCommentary` record
  (third-party read on a VerificationReview;
  `assessment` ∈ {endorses, qualifies, dissents, noted}).

**Cross-file `$ref` to Lowering's namespace.** Verification-
family records reference `CrossDialectRef` (shipped inline
inside `lowering/lowering.json`'s `$defs`). PFS10 chooses
between (a) `$ref`-ing across namespaces via the shared
registry, or (b) re-inlining `CrossDialectRef` as its own
`$defs` inside each verification-family schema. Guidance: prefer
re-inlining — lower coupling between namespaces, and
CrossDialectRef is small (two strings) and stable.

**Per-record sketch follow-on: PFS10 — Verification family.**
Expected 4 files. Inherits Lowering's inline-CrossDialectRef
decision from PFS9. Corpus: VerificationReview records produced
by the four existing dramatica-complete → substrate verifiers
(Macbeth / Oedipus / Ackroyd / Rocky).

### PFS8-D — Dialect-internal observation / review batch

Under existing dialect namespaces per PFS8-N2:

**Aristotelian (4 records):**

- `schema/aristotelian/observation.json` — `ArObservation`
  (self-verifier finding; severity ∈ {noted, advises-review};
  shape parallels StcObservation: `{severity, code, target_id,
  message}`).
- `schema/aristotelian/annotation_review.json` —
  `ArAnnotationReview` (review on a prose field of an
  Aristotelian record; `target_kind + target_id + field`
  triple identifies the prose — e.g., `("ArMythos",
  "ar_oedipus", "action_summary")`).
- `schema/aristotelian/observation_commentary.json` —
  `ArObservationCommentary` (reviewer read on an
  `ArObservation`; parallels `VerifierCommentary` for dialect-
  internal observations; assessment ∈ {endorses, qualifies,
  dissents, noted}; optional `suggested_signature` prose).
- `schema/aristotelian/dialect_reading.json` — `DialectReading`
  (probe's methodology self-report, one per probe invocation;
  `read_on_terms` ∈ {yes, partial, no}; `drift_flagged` +
  `scope_limits_observed` + `relations_wanted` tuples; the
  "did the LLM engage the dialect on its own terms?" signal
  aristotelian-probe-sketch-01 APS6 P4 exists to produce).

**Save-the-Cat (1 record):**

- `schema/save_the_cat/observation.json` — `StcObservation`
  (self-verifier finding; shape parallels ArObservation).

**Per-record sketch follow-ons:**

- **PFS11 — Aristotelian cross-boundary batch.** 4 files; the
  natural bundling since all four ship together from the
  Aristotelian probe surface. Corpus: the two Aristotelian
  probe JSONs (`reader_model_oedipus_aristotelian_output.json`,
  `reader_model_rashomon_aristotelian_output.json`) + any
  future re-probes.
- **PFS12 — Save-the-Cat observation.** 1 file; smallest arc.
  Corpus: synthetic / per-encoding verifier outputs (no
  authored probe JSONs for Save-the-Cat today — the probe
  surface is Dramatica-complete-focused).

**ArAnnotationReview vs. Lowering's `AnnotationReview` — genuinely
different records, different namespaces.** Both carry review-
verdict vocabulary, but:

- Lowering's `AnnotationReview` targets **a Lowering's
  Annotation field** (review act on prose-rationale attached
  to a Lowering record).
- Aristotelian's `ArAnnotationReview` targets **prose fields
  on Aristotelian records** (`action_summary`, `annotation`,
  `hamartia_text`), identified by a `target_kind + target_id +
  field` triple.

Different target semantics; no merge is warranted. The naming
collision is resolved by the namespace — `lowering/
annotation_review.json` vs. `aristotelian/annotation_review.json`.

**DramaticaObservation and any future Dramatic observation.**
Ship under `schema/dramatica_complete/observation.json` and
(if a Dramatic-specific variant exists) `schema/dramatic/
observation.json` — both gated on Dramatic-dialect schemas
(PFS6 OQ2's dramatic-sketch-02 forcing function).

### PFS8-X — Deferred / out-of-scope records

The following Python record types are **deferred** from
Production C — they are runtime state or ephemeral containers,
not authored records, and schema-ification is not load-bearing
until a consumer forces it.

- **`CheckRegistration`** (`core/verification.py`). Runtime
  binding of check functions to record types; reconstructed at
  orchestrator boot time from module imports + coupling
  declarations; not persisted. **Deferred.** Forcing function:
  a port that wants to ship check-registration state as
  authored data (would enable offline coverage-gap analysis
  from a dumped registry).
- **`CoverageGap`** (`core/verification.py`). Verifier registry
  gap report; transient output of a linting pass. **Deferred.**
  Forcing function: a port or CI pipeline that wants to
  serialize gap reports for trend tracking across runs.
- **`DroppedOutput`** (`core/reader_model_client.py`). Probe
  LLM output that failed scope/structural validation; audit
  artifact, not authored. **Deferred.** Forcing function:
  cross-run drift analysis that wants to index historical
  drops.
- **`ReaderModelResult`** (`core/reader_model_client.py`),
  **`DramaticReaderModelResult`** (`core/
  dramatic_reader_model_client.py`),
  **`AristotelianReaderModelResult`** (`core/
  aristotelian_reader_model_client.py`). Probe-result
  *container* records — each holds typed tuples of records
  already spec'd here (AnnotationReview, VerifierCommentary,
  ArObservationCommentary, DialectReading, etc.). The
  containers are runtime structures; their contents are the
  load-bearing types, each with its own per-record schema
  above. **Deferred.** Forcing function: a port that wants to
  render a full probe-result dump as a single JSON artifact
  with a top-level container schema. The existing
  `reader_model_*_output.json` files already do this informally;
  a schema would formalize the container shape.

Deferring these is cheap — zero cost today, tiny per-record-
sketch cost later when a forcing function argues for any of
them. Each is small (≤10 fields); none blocks downstream work.

## Per-record arc plan

Five per-record sketches follow C-opener, in this priority
order:

1. **PFS9 — Lowering family.** `schema/lowering/{lowering,
   annotation_review, lowering_observation}.json` + inline
   `$defs/cross_dialect_ref`, `$defs/annotation`, and
   `$defs/position_range` inside `lowering.json` (PFS7-X2
   convention). Annotation's `review_states` → cross-file
   `$ref` to `annotation_review.json` (PFS6-X1 pattern).
   Corpus: existing `*_lowerings.py` files across the six
   dramatica-complete encodings + save-the-cat encodings.
2. **PFS10 — Verification family.** `schema/verification/{
   verification_review, structural_advisory,
   verification_answer_proposal, verifier_commentary}.json`.
   Re-inlines `CrossDialectRef` as its own `$defs` per
   PFS8-V recommendation (lower cross-namespace coupling).
   Corpus: verifier outputs produced by the four existing
   dramatica-complete → substrate verifiers.
3. **PFS11 — Aristotelian cross-boundary batch.**
   `schema/aristotelian/{observation, annotation_review,
   observation_commentary, dialect_reading}.json`. Largest
   per-record arc (4 files); natural bundling since all four
   ship together from the Aristotelian probe surface.
4. **PFS12 — Save-the-Cat observation.** `schema/save_the_cat/
   observation.json`. One file; smallest arc.
5. **Dramatic + Dramatica-complete observations** (pending).
   Gated on Dramatic-dialect schema landing (PFS6 OQ2 →
   dramatic-sketch-02). Ships with or after the Dramatic
   production sketch.

**Sequencing.** PFS9 before PFS10 (so PFS10 can reference or
re-inline CrossDialectRef after seeing how PFS9 shipped it).
PFS11 / PFS12 are independent of the PFS9/PFS10 pair and can
interleave; PFS12 is a single-file arc and could ship
concurrently with the Aristotelian batch or as a breather
between larger arcs.

**Slim-sketch expectation.** Each per-record sketch stays slim
(~400–600 lines) under the same discipline PFS5/PFS6/PFS7
established: design sketches (lowering-record-sketch-01,
verification-sketch-01, aristotelian-probe-sketch-01) ship the
field-level shapes; production sketches format-render.

## Open questions

1. **OQ1 — Lowering's `metadata: dict` field.** `Lowering`
   carries `metadata: dict = field(default_factory=dict)` for
   supersession pointers and ad-hoc annotations. JSON Schema
   can admit `additionalProperties: true` on a nested object,
   but schema-level validation of the metadata's shape is
   impossible without enumerating every key the corpus uses.
   PFS9 decides whether to admit metadata openly, reject it at
   the schema layer, or enumerate known keys. Parallel to
   substrate-sketch-05's metadata-as-string-dict posture. No
   forcing function today; banked to PFS9.

2. **OQ2 — CrossDialectRef inlining vs. `$ref` across
   namespaces.** Named in PFS8-V above. Deferred to PFS10 with
   guidance: prefer re-inlining. The argument for `$ref`-ing
   across namespaces is deduplication (one schema definition);
   the argument against is coupling (verification-family
   records become dependent on the lowering namespace's layout).
   Forcing function: a third consumer of CrossDialectRef showing
   up (e.g., a cross-boundary reader-model container schema
   under PFS8-X's deferred set). Until then, the deduplication
   win is small and the coupling cost is real.

3. **OQ3 — Dialect-token registry.**
   `CrossDialectRef.dialect` is a plain string in Python
   (`"substrate"`, `"dramatic"`, `"dramatica_complete"`,
   `"aristotelian"`, `"save_the_cat"`). PFS9 decides whether
   to close-enum the dialect string at the schema layer
   (catches typos, forbids author-defined dialects) or leave it
   open (honors architecture-sketch-02 A6's "dialects are
   plural, extensibility is first-class"). Forcing function: a
   dialect-token typo detected at runtime. Banked.

4. **OQ4 — AnnotationReview optional `id` field.** Per
   `aristotelian.py`, `ArAnnotationReview` has `id:
   Optional[str] = None`. Lowering's `AnnotationReview` has no
   id field. PFS11 decides whether Aristotelian's optional-id
   is worth spec'ing or whether the two AnnotationReview
   shapes should converge on id-less. Forcing function: an
   external cross-reference to a specific review (external
   tooling that wants to cite a review by id).

5. **OQ5 — Dialect-catalog schemas (`StcCanonicalBeat`,
   `StcGenre`, and any future Aristotelian parallel).** Named
   in PFS7 OQ2. Not cross-boundary per se — dialect-catalog is
   a legitimate third kind of dialect-namespace record, neither
   authored per-encoding (like StcStory) nor produced per-
   encoding (like StcObservation). Per PFS8-N2's classification
   principle, dialect-catalog records clearly live under the
   dialect namespace (`save_the_cat/genre.json`,
   `save_the_cat/canonical_beat.json`). The remaining question
   is whether schemas earn their keep for records validated
   once at module load vs. per-encoding. Deferred to a future
   dialect-catalog sketch; outside Production C's scope.

## Discipline

Same-as-always under the PFS2 discipline:

- **Design sketches ship the record shapes.** lowering-record-
  sketch-01 (L1–L10), verification-sketch-01 (V1–V8),
  aristotelian-probe-sketch-01 (APS1–APS6), save-the-cat-
  sketch-02 (S9–S13 for the StcCharacter surface;
  StcObservation's shape is already in `save_the_cat.py`
  Python). Each per-record production sketch format-renders;
  no new design derivation should be required, and if it is,
  the sketch pauses to amend the design layer first.
- **Schemas before code.** No Python change is anticipated in
  any of the per-record sketches. If a conformance failure
  surfaces, the posture is the same as all prior arcs: amend
  the design sketch first; then schema; then Python.
- **Namespace is one-shot.** PFS8-N1 + PFS8-N2 commit the
  namespace; once PFS9 ships under `schema/lowering/`, every
  downstream port routes by that path. The namespace decision
  is load-bearing; the cost of revisiting would be real
  (renames across schemas, tests, READMEs, external
  references); the benefit would have to be proportional. None
  is in view today.
- **Slim when design is done.** Same discipline as PFS5 / PFS6
  / PFS7 for the per-record sketches. The opener sketch is
  larger (this one) because it covers a wider surface area;
  that's the one-time cost of committing the namespace.
- **PFS8 is the opener, not the Dramatic production sketch.**
  PFS7 OQ5 referenced Dramatic as "PFS8 candidate"; that
  expectation shifts — Dramatic becomes PFS13 candidate (after
  PFS8 opener + PFS9 Lowering + PFS10 Verification + PFS11
  Aristotelian batch + PFS12 Save-the-Cat observation). The
  re-numbering has no retroactive cost; PFS sketches are
  prefix-stable once shipped.

## Summary

Cross-boundary schema namespace committed. Two new top-level
subdirectories (`schema/lowering/` + `schema/verification/`)
for dialect-agnostic cross-boundary records; dialect-internal
records (observations, dialect-flavored reviews, probe
methodology) stay under `schema/<dialect>/` per extended PFS6-
N1.

Twelve commitments:

- **PFS8-N1** — two new top-level namespaces
  (`schema/lowering/`, `schema/verification/`).
- **PFS8-N2** — dialect-internal records under
  `schema/<dialect>/` (extends PFS6-N1).
- **PFS8-L** — Lowering-family namespace catalog (3 files +
  inline sub-records: CrossDialectRef, Annotation,
  PositionRange).
- **PFS8-V** — Verification-family namespace catalog (4 files;
  CrossDialectRef re-inlined or $ref-resolved per PFS10).
- **PFS8-D** — Dialect-internal observation/review batch
  (4 Aristotelian + 1 Save-the-Cat + future Dramatica).
- **PFS8-X** — Runtime / ephemeral records deferred
  (CheckRegistration, CoverageGap, DroppedOutput, three
  ReaderModelResult containers).

Twenty-two known cross-boundary Python record types
classified: eleven ship under the new top-level namespaces
(3 Lowering + 4 Verification + 4 Aristotelian-dialect-
boundary + future Dramatic-dialect-boundary); five under
existing dialect namespaces when they ship (Aristotelian: 4;
Save-the-Cat: 1); and six deferred as runtime / ephemeral
(CheckRegistration, CoverageGap, DroppedOutput,
ReaderModelResult, DramaticReaderModelResult,
AristotelianReaderModelResult).

Five per-record sketches briefed (PFS9 Lowering family, PFS10
Verification family, PFS11 Aristotelian cross-boundary batch,
PFS12 Save-the-Cat observation, + future Dramatic observations
gated on dramatic-sketch-02). Each stays slim under the
PFS5/6/7 discipline.

Five open questions banked with forcing functions: metadata
shape (OQ1, PFS9); CrossDialectRef inlining-vs-$ref across
namespaces (OQ2, PFS10); dialect-token registry (OQ3, PFS9);
AnnotationReview id field (OQ4, PFS11); dialect-catalog
records (OQ5, future).

No schema deliverable in this arc. No Python change. Sixteenth
consecutive production-track commit on track to avoid
`prototype/story_engine/` modifications. The PFS2 discipline
(schemas depend on design sketches; Python depends on schemas;
conformance verifies the chain) extends into Production C
without a new principle — the namespace map is the only new
commitment.
