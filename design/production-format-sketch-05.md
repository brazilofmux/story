# Production format — sketch 05

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing — extends
[production-format-sketch-01](production-format-sketch-01.md)'s
methodology (PFS1 + PFS2 + PFS5 unchanged) and continues the
one-record-per-sketch cadence (sketch-02's default).
**Frames:** [production-format-sketch-01](production-format-sketch-01.md)
(PFS1 JSON Schema 2020-12, PFS2 derivation discipline, PFS5
repository layout), [substrate-sketch-04](substrate-sketch-04.md)
§Branch representation (the design-layer field-level spec this
sketch renders at the schema layer).
**Related:** [production-format-sketch-03](production-format-sketch-03.md)
(PFS3-E1 cross-file `$ref` pattern, not invoked here — Branch
has no cross-file references), [substrate-sketch-04](substrate-sketch-04.md)
§Branch kind — what role the branch plays, §Facts and state
(with branching) — the surrounding fold semantics the Branch
record supports but does not itself encode.
**Superseded by:** nothing yet

## Purpose

Ship `schema/branch.json` — the canonical schema for the
Branch record specified by substrate-sketch-04 §Branch
representation. Extends the substrate schema layer from five
records (Entity, Description, Prop, Event, Held) to six.

**No design derivation.** Substrate-sketch-04 §Branch
representation already commits the field set — `label`,
`kind`, `parent`, `metadata` — with kind closed at four values
and parent conditional on kind. This sketch is a pure
format-rendering exercise: take the design-layer spec and
render it as JSON Schema 2020-12.

**Extends sketch-01's methodology; no new PFS commitments.**
PFS1 + PFS2 + PFS5 unchanged. This is the sixth substrate
record under the PFS2 discipline, the first since the layer
completed at Held (sketch-04), and the first one that does not
need a design-sketch amendment to land cleanly — substrate-
sketch-04 was written design-first, and the Branch field spec
there is already complete.

## Why now

- Design-layer forcing function is already satisfied:
  substrate-sketch-04 §Branch representation commits the
  four-field shape with no open questions about field identity,
  kind vocabulary, or parent conditionality.
- Closes the last substrate record the design sketches name but
  the schema layer does not yet carry. After this arc,
  **every substrate record named in any active design sketch
  has a matching schema file** — no design/schema gap remains
  at the substrate layer.
- Corpus validation is ready: seven encodings ship
  `ALL_BRANCHES` dicts — six are canonical-only (1 Branch each);
  Rashomon ships 5 (CANONICAL + 4 CONTESTED). Eleven Branch
  records total across the corpus, seven unique labels.
- No DRAFT and no COUNTERFACTUAL records in the current corpus
  — those two kinds are exercised by schema coverage (enum
  admission) but not by record-validation. Same non-issue as
  sketch-04's 5 narrative-via enum values.

## Scope — what the sketch covers

**In:**

- `schema/branch.json` — structural JSON Schema for Branch
  per substrate-sketch-04 §Branch representation.
- Extension of `prototype/tests/test_production_format_sketch_
  01_conformance.py`:
  - new `_load_branch_schema` + registry extension;
  - new `_dump_branch` helper (field-for-field isomorphic to
    Python Branch, with kind-enum `.value` extraction and
    conditional parent handling);
  - new `_discover_encoding_branches` helper that iterates
    `ALL_BRANCHES.values()` across encoding modules;
  - new Branch metaschema validity + shape-spot-check tests;
  - new Branch corpus conformance test: every Branch across
    every encoding's `ALL_BRANCHES` validates against
    `schema/branch.json`.
- `schema/README.md` sweep: Branch moves from the "What's
  deferred" list into the "What's here" list; the ordering
  reflects the substrate-layer completion.

**Out:**

- **Python prototype refactor.** The Python `Branch`
  dataclass has three fields (`label`, `kind`, `parent`) and
  no `metadata`. The schema admits `metadata` as optional
  (substrate-sketch-04 §Branch representation commits to it;
  the design sketch wins per PFS2); the Python corpus omits
  the field uniformly and validates clean under an optional
  field. A future Python refactor may add `metadata` and
  populate it for authored drafts / counterfactuals; the
  schema is ready.
- **Kind-dependent fold semantics.** The schema encodes which
  `kind` values are legal and the parent-presence conditional.
  It does not encode fold-scope rules (substrate-sketch-04
  §Fold scope across branches), enforcement-per-branch rules
  (§Enforcement per branch), or the branch × event-status
  legal-combination table (§Branch kind — what role the
  branch plays). Those are runtime semantics the Branch
  record participates in; they are not record-shape
  commitments.
- **Branch-label format.** Substrate-sketch-04 uses
  `:canonical`, `:b-*`, `:draft-*`, `:cf-*` conventions but
  does not normatively commit to the prefix scheme. The
  schema admits any non-empty string. Tightening to a
  prefix-by-kind convention is a future sketch concern (see
  §Open questions OQ1).
- **Event-to-Branch cross-reference validation.** Events
  carry `branches` as an array of label strings (per
  `schema/event.json`). Whether every such label resolves to
  a Branch record in some encoding's `ALL_BRANCHES` is a
  consistency check across records — not a per-record schema
  commitment. Bank as OQ3.
- **KnowledgeState schema.** Per-agent-per-τ_s state (a
  collection of Helds plus an agent_id) is trivially derivable
  but has no current consumer. Deferred (unchanged from sketch-04
  §Out).

## Commitments

Labels **PFS5**. Sub-namespaced by surface (B for Branch
record, D for dump-layer changes).

### Branch

#### PFS5-B1 — schema derives from substrate-sketch-04 §Branch representation

`schema/branch.json` renders substrate-sketch-04's
four-field spec as JSON Schema 2020-12. Two required fields
unconditionally (`label`, `kind`); one conditionally required
(`parent`, under all kinds except `canonical`); one optional
(`metadata`).

#### PFS5-B2 — `additionalProperties: false`

Strict shape per the PFS1 discipline already applied to
Entity, Description, Prop, Event, and Held. Undeclared fields
fail validation.

#### PFS5-B3 — `label` is a non-empty string

`label` is `{type: "string", minLength: 1}`. No prefix
constraint — substrate-sketch-04's `:foo` convention is
descriptive, not normative. A future sketch may tighten
(see OQ1).

#### PFS5-B4 — `kind` closed enum (four values)

`kind` is `{type: "string", enum: ["canonical", "contested",
"draft", "counterfactual"]}`. Matches substrate-sketch-04 B1's
closed vocabulary. The Python `BranchKind` str-subclass enum
produces exactly these four string values; dump extracts via
`.value`.

#### PFS5-B5 — `parent` conditional by kind

`parent` is `{type: "string", minLength: 1}` when present,
referring to another branch's `label` (a logical, not
schema-enforced, cross-reference — see §Out and OQ3).
Conditionality per substrate-sketch-04 §Branch representation:

- `kind = canonical` — `parent` MUST NOT be present.
- `kind = contested` — `parent` MUST be present (Python's
  `__post_init__` normalizes `None` to `":canonical"`;
  dumped records carry the normalized value).
- `kind = draft` — `parent` MUST be present.
- `kind = counterfactual` — `parent` MUST be present.

Expressed in JSON Schema as an `allOf` with an `if/then/else`:
if `kind === "canonical"`, then `not {required: ["parent"]}`;
else `required: ["parent"]`.

#### PFS5-B6 — `metadata` optional open object

`metadata` is `{type: "object"}` when present; no inner-shape
constraint. Matches the `Description.metadata` convention —
the substrate does not interpret the contents; tooling-
specific extension is admitted. Substrate-sketch-04 §Branch
representation names "authorial notes, creation τ_a,
disposition history (for drafts and counterfactuals)" as
the kinds of content this field carries; none of that is
structurally committed at the schema layer.

### Dump + discovery

#### PFS5-D1 — `_dump_branch` helper

Field-for-field isomorphic to Python `Branch(label, kind,
parent)`. Implementation:

- `label` → `label` (string pass-through).
- `kind.value` → `kind` (enum string extraction).
- `parent` → `parent` when not `None` (canonical branches
  have `parent=None` → field omitted).
- No `metadata` emission (Python has no such field today;
  omission validates under the schema's optional `metadata`).

#### PFS5-D2 — `_discover_encoding_branches` helper

Iterates over encoding modules that export `ALL_BRANCHES` (a
dict mapping label → Branch). Returns a list of
`(encoding_name, [Branch, ...])` tuples. Encodings without
`ALL_BRANCHES` skip silently (matches the existing
discovery-pattern for DESCRIPTIONS / ENTITIES / FABULA).

## Conformance dispositions

Anticipated findings during implementation (to be filled in
or lifted as the conformance test runs):

### Disposition 1 (anticipated): `metadata` field not exercised

**Status (anticipated):** not-a-finding, schema-over-provision
under PFS2.

The Python `Branch` dataclass does not carry `metadata`;
every corpus record validates clean under the schema's
optional `metadata`. Schema admitting a field the corpus
does not emit is the PFS2-correct posture (sketch wins; the
field exists for future encodings that want authorial notes
on drafts or counterfactuals).

### Disposition 2 (anticipated): `draft` and `counterfactual` kinds not exercised

**Status (anticipated):** not-a-finding, corpus-coverage gap.

The corpus has zero DRAFT and zero COUNTERFACTUAL records.
Schema admits both per PFS5-B4; corpus validation against
the schema does not exercise the enum's third and fourth
slots. Same shape as sketch-04's 5 unused narrative-via
enum values. A future encoding that authors a draft or
counterfactual exercises the schema; no sketch change needed.

### Recognition protocol

The conformance test recognizes no Branch dispositions as of
shipping (both anticipated dispositions above are
non-findings, not dispositions in the sketch-03 sense). Any
schema-validation failure on a Branch record is a new
finding and fails the test loudly; adding a disposition
requires amending this sketch's §Conformance dispositions
first.

## Open questions

1. **Label-format tightening.** Substrate-sketch-04 uses a
   prefix convention (`:canonical`, `:b-*`, `:draft-*`,
   `:cf-*`) but does not commit it. A future sketch may
   normatively enforce prefix-by-kind (e.g., `:b-*` for
   contested). This sketch admits any non-empty string;
   tightening breaks no existing encoding and can land as
   a schema amendment.
2. **Metadata shape.** If future encodings populate
   `metadata` with load-bearing structure (creation τ_a,
   disposition history), a later sketch may promote the
   field from open dict to a typed sub-schema. This sketch
   defers.
3. **Cross-reference consistency.** Events carry `branches`
   as an array of label strings, but `schema/event.json`
   does not verify those labels resolve to a Branch record
   in any `ALL_BRANCHES`. A separate consistency test could
   check this at the test layer. Bank as a non-schema,
   cross-record audit.
4. **Branch reconvergence semantics** (substrate-sketch-04
   open question 13) remains unresolved and is out of scope
   for this sketch. The Branch record's shape does not depend
   on which reconvergence candidate wins; the schema is
   stable across all three.
5. **Draft supersession semantics** (substrate-sketch-04
   open question 14) similarly does not affect the Branch
   record's shape. When drafts carry explicit supersession
   links (author-declared), the link will live in
   `metadata` (or a promoted typed field if OQ2 fires); no
   schema action needed now.

## Schema-layer milestone

After this sketch's implementation commit lands, the
substrate schema layer is **structurally complete**. Six
records:

- Entity (production-format-sketch-02)
- Description (production-format-sketch-01)
- Prop (production-format-sketch-03)
- Event (production-format-sketch-03, amended by sketch-04)
- Held (production-format-sketch-04)
- Branch (this sketch)

Every substrate record named in substrate-sketch-04 §The
substrate layer or substrate-sketch-05 has a matching schema
file. The design/schema gap at the substrate layer reaches
zero.

Remaining schema-layer work (unchanged from sketch-04 §Out):

- Dialect records — per-dialect production sketches;
  Aristotelian is the smallest candidate (~7 records).
- Cross-boundary records — Lowering, VerificationReview,
  StructuralAdvisory, VerifierCommentary, ArAnnotationReview,
  ArObservationCommentary, DialectReading. Multiple sketches.
- KnowledgeState record — deferred; no current consumer.

## Not in scope

Recap, cross-referenced to §Out:

- **Fold semantics.** Branch as a record, not as a fold rule.
  Fold-sketch (candidate `substrate-knowledge-fold-sketch-01`)
  territory.
- **Python refactor to add `metadata`.** Future arc; not gated
  on this sketch.
- **Label format prefix enforcement.** Future sketch; current
  conformance test uses substring checks for `:`-prefixed
  labels where appropriate.
- **Cross-reference validation** between Event.branches and
  ALL_BRANCHES. OQ3; a consistency test.
