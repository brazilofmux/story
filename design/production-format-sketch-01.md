# Production format — sketch 01

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (new topic)
**Frames:** [architecture-sketch-02](architecture-sketch-02.md)
(the dialect stack this spec describes at the substrate layer),
[substrate-sketch-05](substrate-sketch-05.md) (Entity ontology,
Description peer-surface claim),
[descriptions-sketch-01](descriptions-sketch-01.md) (Description
record shape — the primary source for PFS3's Description schema)
**Related:** the project's `memory/project_longterm_roadmap.md`
goal #4 (port), goal #1 (markdown parser), goal #3 (prose
export); `memory/feedback_python_as_spec.md`
**Superseded by:** nothing yet

## Purpose

Open the production-direction work the roadmap has banked since
state-of-play-04. First production-layer sketch; first commit
where the artifact is *not* intended to be read by the Python
prototype.

**The problem this sketch addresses.** The current Python
dataclasses are the de facto spec. Every new field, helper, or
import chain deepens the coupling. A port to another language
(roadmap item 4) would be an archaeological dig through Python
code rather than a translation of a named spec. The research
arc has already produced drift by commission: when this sketch's
author tried to write a JSON Schema for `Event` purely from
design/substrate-sketch-05, the effect-shape fields
(`KnowledgeEffect`, `WorldEffect`) turned out to be named in the
sketch but not structurally defined there — the concrete shape
exists only in the Python. That is the Python-as-spec drift this
sketch opens a path out of.

**The methodological lever.** Write the schemas **as if the
Python prototype does not exist**. Source of truth: the design
sketches. The Python dataclasses are a conformance check,
not a template. When the sketches are under-specified (the
effect-shape gap above), the sketch surfaces the gap as a
forcing function for further design sketches — it does NOT paper
over the gap by reading the Python.

The long-term architecture:

1. **Schemas** (this sketch starts) — the canonical spec.
2. **On-disk format** (later sketch) — how schemas land as
   files a person can edit and git can diff.
3. **Author-input surface** (roadmap #1, later sketch) —
   markdown with fenced structured blocks.
4. **Engine** (current Python, eventual port) — reads files,
   runs verifiers, invokes probes.
5. **External glue** (probes, LLM API, UI) — already separately
   typed.

This sketch does layer 1 only, and only for two substrate
records. Layer 2 is a sibling sketch; layers 3–5 are downstream.

## Why now

- State-of-play-05 left the research-to-production question
  explicitly open. Two prior arcs were pure research. The
  shift-point signal is twice-confirmed (architectural via
  aristotelian-sketch-01; behavioral via aristotelian-probe-
  sketch-01). Production-direction work is overdue.
- `memory/feedback_python_as_spec.md` flagged Python-drift risk.
  The drift is real (see the effect-shape gap above); without
  a named spec external to Python, every research arc risks
  deepening it.
- This sketch's scope is small (two records, no format-layout
  commitments, no parser, no engine change) — a tractable first
  production commit. Matches the sketch-first-implementation-
  second discipline: this sketch is design only; conformance
  implementation is the second commit per PFA4.

## Scope — what the sketch covers

**In (after amendment — see §PFS2 catches real drift during
sketch-01 authoring):**

- JSON Schema 2020-12 as the schema language.
- **One** schema: **Description** — the only substrate record
  that is fully field-specified at the design-sketch level
  (descriptions-sketch-01 §Required fields + §Optional fields).
- Placement of the schema in a new top-level `schema/`
  directory, signaling language-independence.
- A conformance-check test (`prototype/tests/`) that validates
  every existing encoding's Description records against the
  schema. First-class conformance artifact; fails the build if
  an encoding drifts.
- The *derivation discipline* (PFS2) that makes this sketch's
  work replicable by a future sketch.

**Out:**

- **Entity.** *Moved to deferred during the sketch-01 authoring
  pass — see §PFS2 catches real drift.* Substrate-sketch-05
  §Entities describes Entity **ontologically** (Agent is a
  subtype of Entity) but does not enumerate the Entity record's
  fields; no `name`, no `kind` enumeration in the sketch. The
  Python prototype carries those fields. Writing an Entity
  schema from sketch content alone yields a near-empty record
  (id inferred, maybe kind inferred from the subtype axis,
  `name` and `kind` enumeration nowhere). Defer until a design
  sketch (candidate: `substrate-entity-record-sketch-01`)
  structurally specifies Entity's fields.
- **Event.** The effect-shape sub-records (`KnowledgeEffect`,
  `WorldEffect`) are named but not shape-specified in
  substrate-sketch-05. Writing an Event schema either means
  reading the Python (which violates PFS2), or inventing shapes
  not anchored in any sketch. Neither is right. Event is
  production-format-sketch-02 work, blocked on an effect-shape
  design sketch (candidate: substrate-effect-shape-sketch-01).
- **Prop** — a minor record referenced by effects. Same
  deferral as Event: Prop's `args` field is typed "entity ids
  (strings) or primitive values" in the sketch, but "primitive
  values" is under-specified (ints? floats? bools? strings?
  heterogeneous arrays?). Defer.
- **Dialect records** (Throughline, ArMythos, DSP, StcBeat,
  etc.). Dialect-sketch work (dramatic-sketch-01, aristotelian-
  sketch-01, etc.) is further-out source material; schemas land
  after substrate schemas are stable.
- **Lowering, VerificationReview, ArObservation, etc.** —
  cross-boundary records. Out until substrate is done.
- **File format** (JSON vs JSONL vs sharded vs bundled). A
  schema is a specification of *shape*, not *layout*. Layout
  is production-layout-sketch-01.
- **The fenced-markdown parser**. Roadmap #1; separate sketch.
- **A DSL** (engine DSL, verifier DSL, query DSL). None are
  blocking; probably none are needed. Deferred.
- **SQL / SQLite / any database**. Files on disk suffice; a
  DB is optimization work not yet forced.
- **Cross-record referential integrity** (checking that a
  Description's `attached_to` resolves to an actual event).
  Schema says "string"; resolution is a validator-layer concern
  covered by production-layout-sketch-XX later.
- **Versioning / schema migration**. `$schema` / `$id` fields
  will carry URIs; no migration machinery yet.

## Commitments

Labels **PFS** (Production Format Sketch). Methodology first
(PFS1–PFS2); record spec second (PFS3, amended from original
two-record scope — see §PFS2 catches real drift); conformance
third (PFS4–PFS5).

### PFS1 — Schema as canonical spec

JSON Schema 2020-12 is the schema language. Each record type
gets one `.json` file in the top-level `schema/` directory of
the repository. The schema file is the source of truth for that
record's shape. Rules:

- The repo's `schema/` directory is language-independent. No
  Python, no Rust, no binary artifacts. Only `.json` schema
  files and a `README.md`.
- Every schema file is valid JSON Schema 2020-12, checkable by
  any conforming validator. This is the port-portability
  guarantee: any language's JSON Schema validator can read
  these files and produce conformance verdicts.
- Schema files are *never* generated from Python source.
  Tooling that auto-generates Pydantic-from-schema (or vice
  versa) is acceptable for consumer code but must not be the
  generating direction for the schema file itself. The schema
  file is authored by a human (or LLM working to this
  discipline) reading the design sketches, never by a
  code-introspection pass.

### PFS2 — Derivation discipline (the methodological lever)

Schemas are written **as if the Python prototype does not
exist**. Concretely:

- **Source of truth:** the design sketches in `design/`. For
  Entity: substrate-sketch-05 §Entities. For Description:
  descriptions-sketch-01 §The description record.
- **Reading order:** sketches first (in full), Python second
  (only for PFS5 conformance check, not for schema authoring).
- **Authoring prohibition:** the schema author does not read
  `substrate.py` / `lowering.py` / any prototype source during
  schema authoring. If the sketches leave a question
  unanswered, the answer is "deferred" or "under-specified —
  sketch-XX forcing function," not "look at the Python."
- **Conformance discrepancies:** when Python has a field the
  schema doesn't, the Python may be over-specified (drop the
  field) or the schema may be incomplete (add the field — but
  only after a design-sketch amendment adds it to a sketch).
  Discrepancies surface in §Conformance dispositions.
- **When the Python has something *better-specified* than the
  sketches:** this is the Python-drift the sketch is written to
  reverse. The discrepancy is recorded; the resolution path is
  a design-sketch amendment, not a schema-Python-match-up.

This discipline inverts the default: the schema does not
depend on the Python; the Python depends on the schema.

### PFS3 — Schema for `Description`

Derived from descriptions-sketch-01 §The description record.
Required fields: `id`, `attached_to`, `kind`, `attention`,
`text`, `authored_by`, `τ_a`. Optional: `is_question`,
`branches`, `review_states`, `promoted_to`, `status`,
`metadata`.

Full schema inline here (authoritative for sketch-01;
authoritative file lives at `schema/description.json`):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://brazilofmux.github.io/story/schema/description.json",
  "title": "Description",
  "description": "An immutable interpretive record attached to a substrate anchor, per descriptions-sketch-01.",
  "type": "object",
  "required": ["id", "attached_to", "kind", "attention", "text", "authored_by", "τ_a"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Stable identifier, scoped per story."
    },
    "attached_to": {
      "description": "Anchor reference. One of: event id, effect-locator, proposition, sjuzhet-entry id, or another description id (D3 allows description-on-description).",
      "oneOf": [
        { "type": "object", "title": "EventAnchor", "required": ["kind", "event_id"], "properties": {
            "kind": { "const": "event" },
            "event_id": { "type": "string" }
        }},
        { "type": "object", "title": "EffectLocatorAnchor", "required": ["kind", "event_id", "effect_index"], "properties": {
            "kind": { "const": "effect" },
            "event_id": { "type": "string" },
            "effect_index": { "type": "integer", "minimum": 0 }
        }},
        { "type": "object", "title": "PropositionAnchor", "required": ["kind", "prop"], "properties": {
            "kind": { "const": "proposition" },
            "prop": { "$ref": "#/$defs/PropPlaceholder" }
        }},
        { "type": "object", "title": "SjuzhetEntryAnchor", "required": ["kind", "sjuzhet_entry_id"], "properties": {
            "kind": { "const": "sjuzhet-entry" },
            "sjuzhet_entry_id": { "type": "string" }
        }},
        { "type": "object", "title": "DescriptionAnchor", "required": ["kind", "description_id"], "properties": {
            "kind": { "const": "description" },
            "description_id": { "type": "string" }
        }}
      ]
    },
    "kind": {
      "type": "string",
      "description": "Starting vocabulary from descriptions-sketch-01; extensible per story with documentation (§Extension rule).",
      "enum": ["texture", "motivation", "reader-frame", "authorial-uncertainty", "trust-flag", "provenance"]
    },
    "attention": {
      "type": "string",
      "enum": ["structural", "interpretive", "flavor"]
    },
    "text": {
      "type": "string",
      "description": "Free-form UTF-8; substrate does not parse."
    },
    "authored_by": {
      "type": "string",
      "description": "Human id, LLM identifier (e.g., 'llm:claude-sonnet-4-6'), or 'unknown' for imported content."
    },
    "τ_a": {
      "type": "integer",
      "minimum": 0,
      "description": "Authored time; monotonic per story; shared sequence with events."
    },
    "is_question": {
      "type": "boolean",
      "description": "Description-as-question routes to an answer-me queue rather than being treated as an assertion. Orthogonal to kind."
    },
    "branches": {
      "type": "array",
      "items": { "type": "string" },
      "uniqueItems": true,
      "description": "Explicit branch scope, subset of the anchor's branches. Omitted = inherit anchor (D4)."
    },
    "review_states": {
      "type": "array",
      "items": { "$ref": "#/$defs/ReviewEntry" },
      "description": "Tuple of review entries. Omitted = no reviews yet."
    },
    "promoted_to": {
      "type": "string",
      "description": "Reference to an event id, if content was promoted from this description into a fact. Immutable audit link."
    },
    "status": {
      "type": "string",
      "enum": ["committed", "provisional"],
      "description": "Authorial commitment axis; same as events."
    },
    "metadata": {
      "type": "object",
      "description": "Open dict for tooling-specific extension; substrate does not read."
    }
  },
  "additionalProperties": false,
  "$defs": {
    "ReviewEntry": {
      "type": "object",
      "required": ["reviewer_id", "reviewed_at_τ_a", "verdict", "anchor_τ_a"],
      "properties": {
        "reviewer_id": { "type": "string" },
        "reviewed_at_τ_a": { "type": "integer", "minimum": 0 },
        "verdict": {
          "type": "string",
          "enum": ["approved", "needs-work", "rejected", "noted"]
        },
        "anchor_τ_a": { "type": "integer", "minimum": 0 },
        "comment": { "type": "string" }
      },
      "additionalProperties": false
    },
    "PropPlaceholder": {
      "description": "Prop shape is under-specified at the design-sketch level (substrate-sketch-05 §Ontology calls Props 'derived, not stored'; descriptions-sketch-01 §Required fields admits proposition-shaped anchors but does not define the shape). Schema-sketch-02 pins this down.",
      "type": "object"
    }
  }
}
```

Notes on the authoring choices:

- `additionalProperties: false` — strict; no undeclared fields
  pass conformance. Matches the substrate's typed discipline.
- `attached_to` as a tagged union (`oneOf`) — the sketch
  enumerates five anchor kinds; each gets a JSON Schema variant
  with a discriminator `kind` field. The Python reference
  encodes anchors as typed Python dataclasses (`AnchorEvent`,
  etc.); the schema expresses the same with a discriminator
  tag. Porting guidance: tag-based union.
- `kind` enum includes the descriptions-sketch-01 starting
  vocabulary. The sketch's "extension rule" (§Extension rule)
  says new kinds are introduced per story with documentation;
  this schema tracks the vocabulary at v1. An encoding that
  introduces a new kind must amend the schema (and this sketch)
  in the same commit.
- `τ_a` as `integer` — sketch says "monotonic per story, shared
  with the substrate's τ_a sequence". The Python uses `int`;
  schema does too.
- `review_states` items are `ReviewEntry`; defined inline under
  `$defs`. Matches descriptions-sketch-01 §Review state.
- `PropPlaceholder` under `$defs` is explicit: the Prop shape
  is under-specified at the sketch level, and this schema
  honestly flags that in the `description` text rather than
  smuggling in a Python-derived shape.

### PFS4 — Conformance is checked, not assumed

A test module `prototype/tests/test_production_format_
sketch_01_conformance.py` validates every existing encoding's
Description records against the schema. The test:

- Loads every encoding's Python records via the existing
  import path.
- Dumps each record to a JSON-compatible dict (a simple
  `dataclasses.asdict` suffices for frozen dataclasses; anchor
  dataclasses need explicit `kind` discriminators added).
- Validates each dict against the appropriate schema via the
  standard `jsonschema` library (added to
  `requirements.txt`).
- Fails loud on any validation error, with the specific record
  id and field named.

Conformance failures are **findings**, not engine errors.
Each failure resolves under PFS2's discipline: either the
Python is over-specified (drop the field) or the sketch is
incomplete (amend the sketch first, then the schema, then the
Python). Findings land in §Conformance dispositions below.

### PFS5 — Repository layout

- **`schema/` at the repo root** — `description.json`,
  `README.md`. New directory.
- `schema/README.md` names the discipline (PFS1, PFS2) and
  links back to this sketch.
- No other repo structure changes. `prototype/` stays where it
  is; `design/` stays where it is.

## PFS2 catches real drift during sketch-01 authoring

**This section is the most important amendment to this sketch.**
Added after the implementation pass discovered that the
original PFS3 (Entity schema) was itself PFS2-drifted.

### What happened

The original production-format-sketch-01 committed to two
record schemas: Entity and Description. When the implementation
pass began (creating `schema/entity.json`), PFS2 discipline
required reading substrate-sketch-05 §Entities first, without
reference to `substrate.py`.

Substrate-sketch-05 §Entities (lines 142–158) turned out to
describe Entity **ontologically only**:

> - **Agent.** Anything that holds knowledge, can witness or
>   perform events. Characters are agents.
> - **Entity.** Anything referred to by the story. Agents are a
>   subtype.

No field enumeration. No mention of `name`. No `kind` value
list. The Python prototype carries all three (`id: str`, `name:
str`, `kind: str  # "agent", "object", "location", "abstract"`)
— but every one of those commitments lives in Python, not in any
design sketch.

The original PFS3 said:

> - `name` (string, required) — the sketch does not specify
>   constraints beyond "name". Schema admits any non-empty UTF-8
>   string.

But the sketch does not mention "name" at all. The claim
"derived from the sketch" was itself Python-drifted. The
implementation pass caught this before any schema file was
written.

### The resolution

Entity joins Event and Prop in the deferred column. A future
design sketch (candidate: `substrate-entity-record-sketch-01`)
structurally specifies Entity's fields; then production-format-
sketch-02 (or this sketch's §amendments) can ship
`schema/entity.json`. Until then, the honest answer is: the
design-sketch record for Entity is under-specified.

### Why this is the sketch working, not failing

The discipline is designed to surface exactly this class of
drift. The sketch before amendment was a draft; the implementation
pass refined the draft by running it; the amendment records
what the implementation learned. Authoring the schema revealed
the sketch's own derivation-claim was PFS2-invalid — so the
sketch is corrected, and the scope narrows to what is truly
supported.

An alternative response — "amend substrate-sketch-05 quickly to
add `name` and the kind enum" — would have been faster but
would have skipped the PFS2 friction that makes the spec real.
The resolution here preserves the friction: spec changes
propagate through a design sketch first, never through
production-format-sketch-01 reading Python and calling it
sketch-derived.

### Lessons for sketch-02 and beyond

1. **Sketch authoring itself is subject to PFS2.** An author
   writing a production-format sketch cannot assert "field X is
   derived from sketch Y" without pointing to the specific
   sketch passage that names field X. Vague ontology-level
   descriptions (Entity is a subtype of Agent) are insufficient
   to ground a record schema.
2. **Record-level specification is design-sketch work.**
   Substrate-sketch-05 is a *concept* sketch; it establishes
   the ontology. A *record-shape* sketch per type is
   complementary, not redundant.
3. **Scope narrowing during implementation is legitimate.**
   This sketch began with two records and finished with one.
   The scope narrowed by surfacing under-specification; that is
   the correct direction of narrowing, and the sketch records
   why rather than silently dropping.

## Conformance dispositions

Populated during the implementation pass (PFA4). The
discipline: every discrepancy between current Python records
and the sketch-derived schema produces one disposition entry,
named and resolved.

### Corpus survey (n=33 Description records across 4 encodings)

Scan of DESCRIPTIONS in `rashomon.py`, `oedipus.py`,
`macbeth.py`, `rocky.py`. `and_then_there_were_none.py` has an
empty list. Results:

- **29 of 33 records validate clean** against the v1 schema.
- **2 records fail on `kind="authoring-note"`** — not in
  descriptions-sketch-01 §Kinds enumeration. *Retired
  2026-04-19 — see Disposition 1 below and descriptions-
  sketch-01 §Amendments Addition 1.*
- **2 records fail on `status="superseded"`** — not in
  descriptions-sketch-01 §Optional fields enumeration.
  *Retired 2026-04-19 — see Disposition 2 below and
  descriptions-sketch-01 §Amendments Addition 2.*

No other discrepancies. Anchor dump transformation
(tagged-union mapping) is mechanical and covers every anchor
in the corpus (only `event` and `description` kinds exercised).

Post-retirement status (2026-04-19): Description corpus is
clean on both axes; all 33+ records validate against the
amended schema.

### Disposition 1: `kind = "authoring-note"`

**Status:** retired 2026-04-19 under descriptions-sketch-01
§Amendments Addition 1. `"authoring-note"` is now enumerated in
§Kinds with typical attention, distinguishing semantics, and an
example (rocky.py `D_timelock_not_natively_detectable`);
`schema/description.json`'s `kind` enum includes it; the
conformance test's `DISPOSITION_KIND_AUTHORING_NOTE` constant
and classification branch are removed.

**Original framing (preserved for audit):** sketch-incompleteness.
The kind was used in `rocky.py` encodings (two descriptions)
but not in descriptions-sketch-01 §Kinds. Resolution required
a design-sketch amendment before schema widening, per PFS2.
The 2026-04-19 amendment supplied that justification.

### Disposition 2: `status = "superseded"`

**Status:** retired 2026-04-19 under descriptions-sketch-01
§Amendments Addition 2. `"superseded"` is now enumerated in
§Optional fields as a third status value, with the edit-chain
mechanism it marks named in §Record-level invariants;
`schema/description.json`'s `status` enum includes it; the
conformance test's `DISPOSITION_STATUS_SUPERSEDED` constant
and classification branch are removed.

**Original framing (preserved for audit):** sketch-incompleteness.
The status was set by the substrate's edit-chain machinery
(`substrate.py apply_description_edit`) and shipped directly
in the macbeth corpus, but was not enumerated in descriptions-
sketch-01 §Optional fields. The amendment rejected the
alternative "model supersession as an explicit edit-replacement
relation" variant — the existing `status` + `metadata.{
supersedes, superseded_by}` mechanism was already load-bearing
and the sketch's own append-on-edit commitment required a
marker; the amendment made the existing shape canonical rather
than redesigning it.

### Not a disposition: anchor shape

**Status:** mechanical dump transformation.
Python's flat `AnchorRef(kind, target_id)` maps cleanly to the
schema's tagged-union at dump time (see `_dump_anchor` in the
conformance test). Not a conformance failure; the Python shape
is a compact affordance for the current corpus's two anchor
kinds (event, description); the schema preserves the full
five-variant vocabulary for when future encodings use other
kinds. Both shapes are specification-consistent.

### Recognition protocol

Post-retirement (2026-04-19), the conformance test
(`prototype/tests/
test_production_format_sketch_01_conformance.py`) recognizes
no Description dispositions — Dispositions 1 and 2 both
retired under the descriptions-sketch-01 amendment, and the
test has been simplified accordingly (no `_classify_failure`
helper; every schema-validation failure is a new finding).
Adding a new disposition requires amending this section first;
the test is not the right place to silently accept new drift.

## Not in scope

See §Scope "Out" above. Key items to re-emphasize:

- **Event.** Defers pending an effect-shape design sketch.
  Anticipated sketch name: `substrate-effect-shape-sketch-01`.
  Without it, an Event schema either violates PFS2 (reads
  Python) or ships under-specified. The deferral is principled.
- **Prop.** Same deferral reason.
- **Dialect records, Lowerings, verification records.**
  Substrate first. Dialect work in later sketches.
- **On-disk layout.** Schemas describe shape. Layout is a
  sibling sketch.
- **Markdown-fenced author-input parser.** Roadmap #1; separate
  sketch; consumes the schemas this sketch produces.

## Open questions

1. **OQ1 — Prop shape.** The most urgent open question this
   sketch surfaces. `Description.attached_to` (variant
   `proposition`) references a Prop, and events' `effects`
   reference Props. Substrate-sketch-05 §Ontology names Props
   as "derived, not stored" — but the Description schema must
   admit a proposition-shaped literal somewhere, because an
   anchor-by-proposition means the proposition is stored on the
   Description. The split between "propositions are derived"
   (state) and "a proposition literal can be an anchor"
   (reference) needs explicit design-sketch treatment. Sketch:
   `substrate-prop-literal-sketch-01` candidate.
2. **OQ2 — Effect shapes.** The larger blocker for Event.
   KnowledgeEffect and WorldEffect are named in the sketch but
   not structurally defined. Sketch candidate:
   `substrate-effect-shape-sketch-01`.
3. **OQ3 — kind-vocabulary extension mechanism.** Descriptions-
   sketch-01 §Extension rule says new kinds are introduced per
   story with documentation. Does a new kind mean: (a) schema
   amendment + PFS2 author reads sketch for justification, or
   (b) schema allows any string and the engine carries the
   vocabulary list? The former is tight (schema breaks when
   vocabulary drifts uncritically); the latter is flexible
   (new kinds need no schema change). Sketch-01 chooses the
   former (schema breaks on new kinds); a future encoding's
   forcing function could revisit.
4. **OQ4 — τ_a scope boundary.** Sketch says τ_a is "monotonic
   per story". If the production format supports multiple
   stories in one repo (or one directory), is τ_a global or
   per-story? Schema models it as a simple integer with no
   namespacing. The "one work per directory" layout sketch
   (sibling sketch, out of scope here) determines this.
5. **OQ5 — `$id` base URI.** The schema's `$id` uses
   `https://brazilofmux.github.io/story/schema/...`. That URI
   may not resolve (no GitHub Pages today). Schema validators
   do not require the URI to resolve — `$id` is the *identity*
   of the schema, not a fetch target — but some tooling
   chooses to fetch. If fetch-failure bites, the URI becomes
   `https://example.com/story/schema/...` or similar and the
   sketch notes the change. No action today.
6. **OQ6 — Versioning policy.** When a schema changes, how do
   documents declare which version they conform to? No
   commitment today; candidate conventions include
   `"$schemaVersion": "1.0"` at the record level or
   `$id` URIs with a version segment. Revisit when the first
   breaking change is on the table.

## Acceptance criteria

Labels **PFA**. Implementation lands after this sketch's
amendment for the Entity deferral (PFS2-driven scope narrowing).

- **[PFA1]** New top-level `schema/` directory with
  `README.md` + `description.json`. Each schema validates
  under JSON Schema 2020-12 (metaschema validation passes).
- **[PFA2]** `schema/README.md` names PFS1 + PFS2 + links to
  this sketch.
- **[PFA3]** `schema/description.json` matches the inline
  spec in PFS3, including the tagged-union `attached_to`,
  the `kind` enum, `review_states`, and the `PropPlaceholder`
  honest-under-specification marker.
- **[PFA4]** `prototype/tests/test_production_format_
  sketch_01_conformance.py` validates every existing
  encoding's Description records (where present) against the
  schema. Uses `jsonschema` (added to
  `prototype/requirements.txt`). Test iterates all encodings
  under `prototype/story_engine/encodings/` discovering
  `DESCRIPTIONS` / similar tuples by naming convention.
- **[PFA5]** All conformance checks pass, OR each failure has
  a §Conformance dispositions entry in this sketch (amending
  if needed) naming the discrepancy and its resolution path.
- **[PFA6]** No change to any Python file outside
  `prototype/tests/` + `prototype/requirements.txt`. The
  prototype's Description dataclasses are unchanged;
  conformance is achieved by schema + dump logic in the test
  module, not by Python modification.
- **[PFA7]** The existing test suite continues to pass
  (684 tests post-aristotelian-probe-sketch-01; + however many
  conformance tests this adds).

If implementation surfaces a Python record that cannot be
reconciled with the sketch-derived schema without modifying
Python, halt and re-open: either (a) amend a design sketch
first (PFS2 discipline), or (b) record a "Python over-specified"
disposition and address separately.

## Summary

First production-layer sketch. Opens the path out of
Python-as-de-facto-spec drift by committing to JSON Schema as
the canonical specification language, with a strict derivation
discipline (PFS2: write schemas from design sketches, never
from Python source).

Scope narrowed during the implementation pass from two schemas
to one: **Description** lands; **Entity** defers because
substrate-sketch-05's §Entities describes Entity ontologically
only (no field enumeration, no `name`, no `kind` value list —
all three come from the Python). That is exactly the drift
PFS2 is designed to catch; see §PFS2 catches real drift for
the full finding. Event and Prop were always deferred pending
effect-shape and prop-literal design sketches. One schema; one
deferral list of three records; honest scope.

Conformance is a first-class check, not an assumption.
Implementation lands as a second commit under the acceptance
criteria PFA1–PFA8. The Python prototype is unchanged in both
commits — the schemas live outside the prototype, as signals
of language-independence, not generated from it.

The sketch's load-bearing claim: **once the spec is outside
Python, the prototype becomes one implementation of the spec
rather than the spec itself.** Further research arcs can
consume the schemas (e.g., an author-input-markdown parser
validates output against `description.json`; a future Rust port
reads the same schemas); each consumer deepens the spec's
external-ness rather than Python's centrality. This is the
first production commit that is intentionally disposable: the
Python engine could be thrown away tomorrow and the `schema/`
directory would still be the right source of truth.
