# Production format — sketch 10

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (second per-record arc under Production C;
ships the first schemas into the `schema/verification/` namespace
committed by PFS8-N1)
**Frames:** [production-format-sketch-08](production-format-
sketch-08.md) PFS8-N1 (two new top-level namespaces), PFS8-V
(Verification-family catalog), PFS8 OQ2 (CrossDialectRef
inlining vs. cross-namespace `$ref`); [production-format-
sketch-09](production-format-sketch-09.md) PFS9-X1 (inline
`$defs` for CrossDialectRef inside `lowering.json`), PFS9-X4
(open dialect-token posture); [verification-sketch-01](
verification-sketch-01.md) V1–V8 (verification output
vocabulary); [production-format-sketch-01](production-format-
sketch-01.md) PFS1 (JSON Schema 2020-12), PFS2 (schemas-first);
[production-format-sketch-03](production-format-sketch-03.md)
PFS3-E1 (cross-file `$ref` via registry); [production-format-
sketch-06](production-format-sketch-06.md) PFS6-X1 (cross-file
`$ref` at dialect layer); [production-format-sketch-07](
production-format-sketch-07.md) PFS7-X2 (inline `$defs`
convention)
**Related:** [architecture-sketch-02](architecture-sketch-02.md)
A8 (verification as observational coupling); [lowering-sketch-
01](lowering-sketch-01.md) F1/F6 (Lowering and verification
architecturally distinct); [lowering-sketch-02](lowering-
sketch-02.md) F8 (Claim-moment + Claim-trajectory sub-kinds)
**Superseded by:** nothing yet

## Purpose

**Second per-record sketch under Production C.** Ships four JSON
Schema 2020-12 files for the Verification family — `VerificationReview`,
`StructuralAdvisory`, `VerificationAnswerProposal`,
`VerifierCommentary` — under the `schema/verification/` namespace
PFS8-N1 committed. Re-inlines `CrossDialectRef` as each schema's
own `$defs` per PFS8-V's guidance: lower cross-namespace coupling
even at the cost of one small duplicated shape. Cross-file `$ref`
from `verifier_commentary.json` to `verification_review.json`
extends the intra-namespace pattern PFS6-X1 established for the
Aristotelian dialect into the verification namespace.

The per-record design work is already done. Verification-sketch-
01 V1–V8 commit the output-record vocabulary + the three
primitive kinds (Characterization, Claim-moment, Claim-trajectory)
+ the probe/verifier coordination model. This sketch format-
renders the four records; V2's "observations route through the
proposal queue" contract and V3/V4's primitive-kind vocabulary
do not add new schema commitments beyond the field-level ones.

## Why now

- **PFS9 shipped CrossDialectRef.** PFS8-V deferred the
  CrossDialectRef inlining-vs-cross-namespace-$ref decision to
  PFS10 with guidance to prefer re-inlining. PFS9's lowering.json
  now carries the canonical shape (inline `$defs/cross_dialect_ref`);
  PFS10 has something concrete to re-inline from.
- **Verification is the load-bearing observation surface.**
  Every dramatica-complete → substrate verifier (Macbeth,
  Oedipus, Ackroyd, Rocky, Rashomon + two Save-the-Cat) emits
  VerificationReview records. Validating the shape at the
  schema layer is the strongest port-readiness claim Production
  C can produce for verifier output.
- **Verification-family records are the second `schema/<role>/`
  namespace.** PFS8-N1 committed two namespaces — PFS9 landed
  the first (`schema/lowering/`). PFS10 lands the second
  (`schema/verification/`) and validates that the tier
  generalizes across the two functional roles.
- **Corpus exists.** Eleven `*_verification.py` encoding modules
  export a `run()` function returning typed verification-family
  output. Running them gives ~90 VerificationReview records
  across the non-skeleton encodings plus ≥1 StructuralAdvisory
  from the `and_then_there_were_none` skeleton. Conformance
  validation is immediate.

## Scope — what the sketch covers

**In:**

- Four JSON Schema files under `schema/verification/`:
  - `schema/verification/verification_review.json`
    (`VerificationReview` per V2).
  - `schema/verification/structural_advisory.json`
    (`StructuralAdvisory` per V2).
  - `schema/verification/verification_answer_proposal.json`
    (`VerificationAnswerProposal` per V2).
  - `schema/verification/verifier_commentary.json`
    (`VerifierCommentary` per V7 — third-party read on a
    VerificationReview).
- **Re-inlined `CrossDialectRef`** per PFS8-V guidance — three
  of the four schemas ship an inline `$defs/cross_dialect_ref`
  duplicating the shape committed by PFS9-X1. (VerifierCommentary
  doesn't reference CrossDialectRef directly; its `target_review`
  is a nested VerificationReview.)
- **Cross-file `$ref` from `verifier_commentary.json` to
  `verification_review.json`** for `target_review`. Extends
  PFS6-X1's intra-namespace cross-file pattern into the
  verification namespace.
- Dump-layer helpers: `_dump_verification_review`,
  `_dump_structural_advisory`,
  `_dump_verification_answer_proposal`, `_dump_verifier_commentary`.
- Discovery helper `_discover_encoding_verifier_output` —
  walks `*_verification.py` modules, calls `run()`, classifies
  output by type.
- Conformance-test extension: twelve new tests (4 metaschema +
  4 shape + 4 corpus).
- `schema/README.md` sweep: the "Cross-boundary layer" section
  gains a Verification subsection; "What's deferred" updated.

**Out:**

- Runtime / ephemeral records (CheckRegistration, CoverageGap,
  probe-result containers) — deferred per PFS8-X.
- Dialect-internal observation records (PFS11 / PFS12 concern).
- Validation of saved probe-result JSONs
  (`reader_model_*_output.json`). Those embed VerifierCommentary
  records in container structures. The `target_review` nested
  shape will validate against `verifier_commentary.json`, but
  the container wrapper isn't spec'd here — PFS8-X deferred the
  `DramaticReaderModelResult` / `AristotelianReaderModelResult`
  shape to future sketches.
- Any amendment to the V1–V8 vocabulary in Python.
- Closed-enum commitment on `VerificationAnswerProposal.status`.
  Per PFS10-AP3 below — today's Python hard-codes `"pending"` as
  the initial value but carries no enum; the schema leaves it
  as an open non-empty string until a forcing function argues
  otherwise (OQ3 banks the potential close-enum).

## Commitments

### PFS10-N1 — Verification family under `schema/verification/`

Inherits PFS8-N1 (`schema/<role>/<record>.json` subdirectory-per-
role at the top-level cross-boundary tier). The role token is
`verification`, matching the Python module name
(`core/verification.py`).

**`$id` URIs:**

- `https://brazilofmux.github.io/story/schema/verification/verification_review.json`
- `https://brazilofmux.github.io/story/schema/verification/structural_advisory.json`
- `https://brazilofmux.github.io/story/schema/verification/verification_answer_proposal.json`
- `https://brazilofmux.github.io/story/schema/verification/verifier_commentary.json`

**Precedent validation.** Second landing under the cross-
boundary top-level namespace tier (first was PFS9 Lowering
family). Confirms PFS8-N1 generalizes across the two committed
role namespaces.

### PFS10-VR1..VR5 — VerificationReview record shape

`schema/verification/verification_review.json` ships the
`VerificationReview` record per verification-sketch-01 V2.

- **PFS10-VR1.** Required fields: `reviewer_id`,
  `reviewed_at_τ_a`, `verdict`, `anchor_τ_a`, `target_record`.
  Five required fields — the Python dataclass has no defaults
  on these five; the two optional fields (`comment`,
  `match_strength`) are Python-optional-defaulted-None.
- **PFS10-VR2.** `reviewer_id` is a non-empty string;
  `reviewed_at_τ_a` and `anchor_τ_a` are integers.
- **PFS10-VR3.** `verdict` is a **closed enum** at four values:
  `{"approved", "needs-work", "partial-match", "noted"}`.
  Matches Python's `VERDICT_*` / `VALID_VERDICTS` (distinct
  from Lowering's AnnotationReview verdict vocabulary — the
  two record types have their own four-value sets. Lowering's
  AnnotationReview emits `"rejected"` as a fourth value where
  VerificationReview emits `"partial-match"`; the verdicts are
  not interchangeable).
- **PFS10-VR4.** `target_record` is a `CrossDialectRef` object
  per `#/$defs/cross_dialect_ref` (re-inlined per PFS10-X1).
  Points at the specific record (upper, Lowering, or Template)
  the review attaches to.
- **PFS10-VR5.** `comment` is an **optional string**;
  `match_strength` is an **optional number** in `[0, 1]`. Both
  Python-default-None → omitted from dump when None (PFS6-D3
  precedent). Per V7, `match_strength` is meaningful for
  `partial-match` verdicts (e.g., "the Characterization check
  holds 70% of the time"); other verdicts may set it for
  transparency or leave None.
- **`additionalProperties: false`.**

### PFS10-SA1..SA4 — StructuralAdvisory record shape

`schema/verification/structural_advisory.json` ships the
`StructuralAdvisory` record per verification-sketch-01 V2.

- **PFS10-SA1.** Required fields: `advisor_id`, `advised_at_τ_a`,
  `severity`, `comment`, `scope`. Five required — unlike
  VerificationReview, `comment` is required (a
  StructuralAdvisory names a cross-record pattern; a bare
  advisory without comment has no content).
- **PFS10-SA2.** `advisor_id` is a non-empty string;
  `advised_at_τ_a` is an integer; `comment` is a string (empty
  string admitted — an advisor could commit a placeholder and
  fill in the explanation later, same posture as Annotation.text
  in PFS9).
- **PFS10-SA3.** `severity` is a **closed enum** at three
  values: `{"noted", "suggest-review", "suggest-revise"}`.
  Matches Python's `SEVERITY_*` / `VALID_SEVERITIES` — distinct
  from Lowering-observation severities (LoweringObservation has
  only `noted` and `advises-review`; StructuralAdvisory adds a
  third tier for recommended revisions).
- **PFS10-SA4.** `scope` is an **array** of `CrossDialectRef`
  objects per `#/$defs/cross_dialect_ref` (re-inlined per
  PFS10-X1). The Python dataclass declares it as `tuple` but
  doesn't enforce min-length; the schema matches. Empty scope
  is legal (an advisor may flag a concern about the corpus as
  a whole that doesn't target specific records — though the
  corpus shows no such case today).
- `match_strength` is an **optional number** in `[0, 1]`
  (Python-default-None → omitted when None). Per V7, same
  semantics as VerificationReview's match_strength.
- **`additionalProperties: false`.**

### PFS10-AP1..AP3 — VerificationAnswerProposal record shape

`schema/verification/verification_answer_proposal.json` ships
the `VerificationAnswerProposal` record per verification-
sketch-01 V2 (a verifier-sourced proposal answering an upper-
dialect open question, parallel to `AnswerProposal` from the
reader-model surface).

- **PFS10-AP1.** Required fields: `proposer_id`, `question_id`,
  `proposed_text`, `rationale`, `proposed_at_τ_a`, `status`.
  Six required — `status` is required even though the Python
  has a default (`"pending"`) per the PFS7 convention: if the
  Python always carries it, the schema requires it.
- **PFS10-AP2.** `proposer_id`, `proposed_text`, `rationale`
  are strings. `question_id` is a `CrossDialectRef` object
  per `#/$defs/cross_dialect_ref` (re-inlined per PFS10-X1),
  pointing at the Description-with-is_question=true the
  proposal answers. `proposed_at_τ_a` is an integer.
- **PFS10-AP3.** `status` is an **open non-empty string**.
  Today's Python hard-codes initial value `"pending"`; the
  acceptance flow (see verification-sketch-01 V2's reference
  to "the existing proposal queue") would set further values
  (`"accepted"`, `"rejected"`, etc.). Per PFS9-X4's open-
  string discipline: leave extensible unless a forcing
  function argues for close-enum. Banked in PFS10 OQ3.
- **`additionalProperties: false`.**

### PFS10-VC1..VC4 — VerifierCommentary record shape

`schema/verification/verifier_commentary.json` ships the
`VerifierCommentary` record per verification-sketch-01 V7
(a third-party read on a VerificationReview).

- **PFS10-VC1.** Required fields: `commenter_id`,
  `commented_at_τ_a`, `assessment`, `target_review`,
  `comment`. Five required — `comment` is required (like
  StructuralAdvisory: a commentary without content has no
  content).
- **PFS10-VC2.** `commenter_id` is a non-empty string;
  `commented_at_τ_a` is an integer; `comment` is a string.
- **PFS10-VC3.** `assessment` is a **closed enum** at four
  values: `{"endorses", "qualifies", "dissents", "noted"}`.
  Matches Python's `ASSESSMENT_*` / `VALID_ASSESSMENTS`. A
  fifth distinct vocabulary from verdict / severity / verdict-
  on-AnnotationReview, each tuned to its distinct judgment
  surface.
- **PFS10-VC4.** `target_review` is a `VerificationReview`
  object via **cross-file `$ref`** to
  `verification_review.json` per PFS10-X2. The Python carries
  the VerificationReview by value (nested record); the schema
  expresses it via cross-file `$ref` (intra-namespace).
- `suggested_signature` is an **optional non-empty string**
  (Python-default-None → omitted from dump when None). Free-
  form prose the commentator thinks the check might add (e.g.,
  "also check told_by listener"); inspiration for the verifier-
  maintainer, not actionable code.
- **`additionalProperties: false`.**

### PFS10-X1 — Re-inlined CrossDialectRef per PFS8-V guidance

Three of the four Verification-family schemas carry a
`CrossDialectRef` shape: VerificationReview.target_record,
StructuralAdvisory.scope[*], VerificationAnswerProposal.question_id.
Each ships its own **inline `$defs/cross_dialect_ref`**
duplicating the shape PFS9-X1 inlined in `lowering/lowering.json`.

**Shape (identical across both namespaces):**

```json
"cross_dialect_ref": {
  "type": "object",
  "required": ["dialect", "record_id"],
  "properties": {
    "dialect": {"type": "string", "minLength": 1},
    "record_id": {"type": "string", "minLength": 1}
  },
  "additionalProperties": false
}
```

**Why re-inline rather than cross-namespace `$ref`.** PFS8-V's
guidance is to prefer re-inlining for three reasons: (1) lower
coupling between namespaces — the verification schemas don't
need lowering.json to resolve; (2) CrossDialectRef is small
(two non-empty strings) and structurally stable (no forcing
functions against it); (3) a port that wants only verification
records can read four files, not five. The cost is real but
bounded: a single shape definition lives in four locations
(once in lowering.json, three times across the verification
schemas), and any amendment to CrossDialectRef requires a
coordinated change across both namespaces. No forcing function
anticipated.

**Dialect token is open.** Same PFS9-X4 posture: `dialect` is a
non-empty string with no closed enum. Verifier-runtime catches
unknown-dialect tokens via CrossDialectRef resolution failures;
schema stays consistent with architecture-sketch-02 A6's
extensibility commitment.

### PFS10-X2 — Cross-file `$ref` from VerifierCommentary to VerificationReview

`verifier_commentary.json`'s `target_review` property uses
`$ref` to
`https://brazilofmux.github.io/story/schema/verification/verification_review.json`.
The registry pattern (PFS3-E1 → PFS4 P4A1 → PFS6-D5 → PFS9-D8)
resolves it.

**Why `$ref` here but re-inline for CrossDialectRef.** Two
factors:

1. **Size and stability.** VerificationReview is a larger,
   evolving record (seven fields; two enums; one nested
   CrossDialectRef). Duplicating its shape inside
   verifier_commentary.json would create a real maintenance
   burden — every VerificationReview amendment would require
   a coordinated verifier_commentary update. CrossDialectRef
   is two fields of stable shape; the duplication cost is an
   order of magnitude smaller.
2. **Same-namespace resolution.** VerifierCommentary's `$ref`
   stays within `schema/verification/`. PFS8-V's concern about
   cross-*namespace* coupling doesn't apply; the coupling is
   within the same top-level namespace, analogous to PFS6-X1's
   ArMythos → ArPhase reference inside `schema/aristotelian/`.

The general rule emerging across PFS6/PFS9/PFS10: prefer
`$ref` for larger/evolving records; prefer inline `$defs` (or
re-inlined copies) for small/stable sub-records; prefer `$ref`
for same-namespace references; prefer re-inline for cross-
namespace references.

### PFS10-X3 — No close-enum on `status` or ad-hoc string fields

Per PFS9-X4's posture: `VerificationAnswerProposal.status` is
an open non-empty string. Rationale identical to PFS9-X4 —
architecture-sketch-02 A6's extensibility commitment (proposal-
acceptance-flow states may grow; a close-enum at this layer
would obstruct).

## Dump-layer commitments

Parallel to PFS5-D1/D2 for Branch, PFS6-D1..D3 for Aristotelian
core, PFS7-D1..D4 for Save-the-Cat core, and PFS9-D1..D6 for
Lowering family.

### PFS10-D1 — `_dump_verification_review(review) -> dict`

Field-for-field isomorphic. Required fields always emit
(reviewer_id / reviewed_at_τ_a / verdict / anchor_τ_a /
target_record). `target_record` rendered via
`_dump_cross_dialect_ref` (shared helper from PFS9-D2).
`comment` omitted when None. `match_strength` omitted when
None.

### PFS10-D2 — `_dump_structural_advisory(advisory) -> dict`

Field-for-field. Required fields always emit
(advisor_id / advised_at_τ_a / severity / comment / scope).
`scope` rendered as array of `_dump_cross_dialect_ref` outputs.
`match_strength` omitted when None.

### PFS10-D3 — `_dump_verification_answer_proposal(proposal) -> dict`

Field-for-field. All six fields (including `status` with
Python default `"pending"`) always emit. `question_id` rendered
via `_dump_cross_dialect_ref`.

### PFS10-D4 — `_dump_verifier_commentary(commentary) -> dict`

Field-for-field. Required fields always emit
(commenter_id / commented_at_τ_a / assessment / target_review /
comment). `target_review` rendered via
`_dump_verification_review` (full nested shape — matches the
Python's by-value carrying). `suggested_signature` omitted
when None.

### PFS10-D5 — `_discover_encoding_verifier_output(modules)`

Walks encoding modules matching `*_verification.py` and calls
each module's `run()` function. The four record types are
classified by `isinstance` check. Returns a quadruple
`(reviews, advisories, proposals, commentaries)` — four lists
of `(encoding_name, records)` tuples.

**`run()` signature variance.** Most verifier modules ship
`def run() -> tuple`; the skeleton
`and_then_there_were_none_dramatica_complete_verification.py`
ships `def run(advised_at_τ_a: int = 0)` — the default makes
a no-args call work across all modules.

**Output classification.** Each element of the returned tuple
is checked against the four record types (VerificationReview,
StructuralAdvisory, VerificationAnswerProposal,
VerifierCommentary) and routed to the matching output list.
Unknown-type elements are ignored (defensive; current corpus
exports only the four record types).

### PFS10-D6 — Registry registration

The conformance test's `_build_schema_registry` gains four
new entries. The registry is load-bearing for
`verifier_commentary.json` (cross-file `$ref` to
`verification_review.json` per PFS10-X2). The other three
schemas are self-contained (inline `$defs/cross_dialect_ref`)
and could validate without registry binding, but registration
gives symmetric $id lookup and keeps the registry consistent.

## Conformance dispositions (anticipated)

No active dispositions anticipated. Four **anticipated non-
findings**:

1. **`match_strength=None` omitted on most VerificationReviews.**
   Per the Python docstring: "Other verdicts may set it for
   transparency or leave it None." Most corpus reviews omit
   (when None); partial-match verdicts typically set it.
   Schema admits absence; dump omits. No disposition.

2. **`comment=None` omitted on most VerificationReviews.** Same
   pattern as match_strength. Schema admits absence; dump
   omits. No disposition.

3. **`status="pending"` always emits on
   VerificationAnswerProposal.** Per PFS10-AP1 the field is
   required (Python default-emitted). No current encoding
   mutates the status, so the corpus may show uniform
   `"pending"`; schema admits any non-empty string. No
   disposition.

4. **Zero `VerifierCommentary` records in the runtime corpus.**
   Verifier modules' `run()` emit only VerificationReview (or
   StructuralAdvisory for the skeleton case). VerifierCommentary
   records live in probe-output JSONs (not covered here) and
   in walker / test fixtures (not part of the conformance
   corpus). Shape validated via metaschema + shape tests; the
   corpus-conformance test reports zero records with a
   descriptive note, parallel to PFS9's AnnotationReview
   handling.

## Corpus expectations

Eleven `*_verification.py` modules contribute to the runtime-
generated corpus by calling their `run()` functions:

- Dramatic-layer verifiers (3): `oedipus_verification.py`,
  `macbeth_verification.py`, `ackroyd_verification.py`.
- Dramatica-complete verifiers (6): `oedipus_dramatica_complete_`,
  `macbeth_dramatica_complete_`, `ackroyd_dramatica_complete_`,
  `rocky_dramatica_complete_`, `rashomon_dramatica_complete_`,
  `and_then_there_were_none_dramatica_complete_` (skeleton).
- Save-the-Cat verifiers (2): `macbeth_save_the_cat_verification.py`,
  `ackroyd_save_the_cat_verification.py`.

**Expected corpus counts** (approximate; conformance test will
report exact numbers on landing):

- **VerificationReview**: ~90 records, emitted by the nine
  non-skeleton verifiers (conservative: 9 checks per
  dramatica-complete verifier × 5 + fewer per Dramatic /
  Save-the-Cat). Breakdown by verdict expected to match the
  state-of-play-09 documented cross-corpus spectrum (mostly
  APPROVED, some PARTIAL, occasional NEEDS_WORK / NOTED).
- **StructuralAdvisory**: ≥1 record, emitted by the skeleton
  `and_then_there_were_none` verifier's run() (the skeleton
  emits a `skeleton:{work-id}` advisory naming what's still
  missing per skeleton-generator-sketch-01 SG5).
- **VerificationAnswerProposal**: zero expected — no encoding
  authors one today. Shape validated via metaschema + shape
  tests.
- **VerifierCommentary**: zero expected — run() emits
  VerificationReview (or StructuralAdvisory for the skeleton);
  VerifierCommentary records live in probe-output JSONs. Shape
  validated via metaschema + shape tests.

Every corpus record expected to validate clean under the
implementation. If a non-finding materializes as a true
conformance issue, this sketch gains a §Dispositions section
(none anticipated).

## Open questions

1. **OQ1 — Cross-record referential integrity for
   `CrossDialectRef` targets.** VerificationReview.target_record,
   StructuralAdvisory.scope[*], VerificationAnswerProposal.question_id
   all point at records that should resolve in the encoding's
   record set. Schema admits any `(dialect, record_id)` pair;
   the verifier's orchestrator carries resolution at runtime.
   A conformance-test-layer audit would extend validation
   beyond shape to existence. Forcing function: a verifier
   that emits a review against a non-existent record id (e.g.,
   a typo in a Python literal). Banked; parallel to PFS5 OQ3 /
   PFS6 OQ3 / PFS9 OQ2's referential-integrity banking.

2. **OQ2 — `match_strength` partial-match correlation audit.**
   Per V7: `match_strength` is meaningful for `partial-match`
   verdicts, optional otherwise. The schema admits any `[0,1]`
   value on any verdict; no cross-field conditional. A future
   amendment could add an `allOf/if-then-else` requiring
   `match_strength` when `verdict=partial-match`, parallel to
   PFS5-B5 / PFS6-M6 / PFS9-X3. Not committed today because
   the Python is permissive (partial-match without
   match_strength is admitted; the advisory is just a
   docstring-level recommendation). Forcing function: a corpus
   partial-match that forgets the strength, detected in review.

3. **OQ3 — `VerificationAnswerProposal.status` close-enum.**
   Today's Python hard-codes `"pending"` as the initial
   value. The proposal-queue walker would mutate it to
   `"accepted"` or `"rejected"`; `"deferred"` is plausible
   too. A future sketch closes the enum when the walker
   integration lands (verification-sketch-01 §Deferred names
   this as the `VerificationAnswerProposal` acceptance flow).
   Banked.

4. **OQ4 — VerifierCommentary's `target_review` shape — nested
   record vs. reference by id.** The Python carries
   VerificationReview by value (full nested record). An
   alternative would be a reference-by-id-string, forcing a
   lookup through an accompanying review collection. The
   nested-by-value shape has no id-generation cost but
   increases commentary record size; the reference shape is
   smaller but requires the commentary consumer to carry a
   review index. PFS10 commits the nested-by-value shape to
   match Python; reversal would require amending the Python
   first. Forcing function: large-scale commentary storage
   where nested duplication hurts.

5. **OQ5 — StructuralAdvisory empty `scope`.** The schema
   admits an empty scope array (the Python tuple can be
   empty); a zero-scope advisory effectively names a corpus-
   level concern with no specific record target. No current
   corpus case. If a future verifier emits such advisories,
   the question of whether they should route through a
   different record type (e.g., a `CorpusAdvisory` parallel)
   becomes live. Banked.

## Discipline

Same-as-always under the PFS2 discipline:

- **Sketches before schema.** Verification-sketch-01 V1–V8
  did the design-layer work for the four records shipped
  here. The VERDICT_* / SEVERITY_* / ASSESSMENT_* constant
  vocabularies in `core/verification.py` are lifted to schema-
  level closed enums — parallel to how substrate-knowledge-
  fold-sketch-01 KF1–KF5 lifted docstring claims to commitment
  level.
- **Schemas before code.** No Python change is anticipated.
  If a conformance issue surfaces, the posture is the same as
  all prior arcs.
- **Second per-record arc under Production C validates the
  first.** PFS10's structure mirrors PFS9 (record commitments
  by record; inline vs. $ref decisions named explicitly;
  dump-discovery-registry block). The generalization from
  PFS9 to PFS10 tests that the per-record sketch template
  works across both cross-boundary roles — structural (PFS9
  Lowering) and observational (PFS10 Verification).
- **Slim when the design is done.** Target ~650 lines similar
  to PFS7 / PFS9. Four records with a modest number of field-
  level decisions each plus the CrossDialectRef re-inline
  commitment and the verifier_commentary → verification_review
  cross-file ref.

## Summary

Second per-record sketch under Production C. Four JSON Schema
files for the Verification family shipped under
`schema/verification/` — the second namespace under the cross-
boundary tier PFS8-N1 committed. Twenty-one commitments:

- **PFS10-N1** — namespace inherits PFS8-N1
  (`schema/verification/`).
- **PFS10-VR1..VR5** — VerificationReview shape (required
  reviewer_id / reviewed_at_τ_a / verdict / anchor_τ_a /
  target_record; verdict enum {approved, needs-work, partial-
  match, noted}; optional comment / match_strength).
- **PFS10-SA1..SA4** — StructuralAdvisory shape (required
  advisor_id / advised_at_τ_a / severity / comment / scope;
  severity enum {noted, suggest-review, suggest-revise};
  scope as array of CrossDialectRef).
- **PFS10-AP1..AP3** — VerificationAnswerProposal shape
  (required proposer_id / question_id / proposed_text /
  rationale / proposed_at_τ_a / status; status open non-empty
  string).
- **PFS10-VC1..VC4** — VerifierCommentary shape (required
  commenter_id / commented_at_τ_a / assessment /
  target_review / comment; assessment enum {endorses,
  qualifies, dissents, noted}; target_review via cross-file
  `$ref` to verification_review.json per PFS10-X2).
- **PFS10-X1** — CrossDialectRef re-inlined in three schemas
  per PFS8-V guidance (lower cross-namespace coupling;
  duplication cost bounded by small + stable shape).
- **PFS10-X2** — cross-file `$ref` from verifier_commentary.json
  to verification_review.json (intra-namespace; extends PFS6-X1
  pattern into the verification namespace).
- **PFS10-X3** — open-string posture on `status` and ad-hoc
  string fields (honors PFS9-X4 discipline).
- **PFS10-D1..D6** — dump helpers + discovery helper (walks
  `*_verification.py` modules, calls run(), classifies by
  type) + registry registration.

Five open questions banked with forcing functions:
CrossDialectRef referential-integrity audit (OQ1);
match_strength partial-match correlation audit (OQ2);
VerificationAnswerProposal status close-enum when walker
acceptance flow lands (OQ3); target_review nested-vs-
reference shape (OQ4); StructuralAdvisory empty-scope corpus-
level advisory routing (OQ5).

No design derivation needed. Verification-sketch-01 committed
the record shapes; this sketch format-renders, lifts the
VERDICT / SEVERITY / ASSESSMENT string-constant vocabularies
to schema-level enums, re-inlines CrossDialectRef per PFS8-V's
deferred guidance, extends PFS6-X1's cross-file `$ref` pattern
to the verification namespace via PFS10-X2, and hands off to
implementation.

Python untouched at the sketch layer. Dump-layer + discovery +
test-suite extensions land in the implementation commit.
Cross-boundary namespace tier reaches two-of-two committed
namespaces landed (Lowering + Verification); PFS11 and PFS12
follow under existing dialect namespaces, independent of the
cross-boundary tier.
