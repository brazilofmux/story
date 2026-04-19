# Production format — sketch 03

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing — extends
[production-format-sketch-01](production-format-sketch-01.md)'s
methodology (PFS1 + PFS2 unchanged) and
[production-format-sketch-02](production-format-sketch-02.md)'s
one-record-per-production-sketch pattern (relaxed here — sketch-03
covers two records because they are structurally entangled)
**Frames:** [production-format-sketch-01](production-format-
sketch-01.md) (PFS1 JSON Schema 2020-12, PFS2 derivation
discipline, PFS5 repository layout), [substrate-prop-literal-
sketch-01](substrate-prop-literal-sketch-01.md) (the design-
layer spec for Prop), [substrate-effect-shape-sketch-01](
substrate-effect-shape-sketch-01.md) (the design-layer spec for
WorldEffect + KnowledgeEffect), [substrate-sketch-05](
substrate-sketch-05.md) §Event internals (the design-layer spec
for Event — structurally field-enumerated at §The five required
elements)
**Related:** [substrate-entity-record-sketch-01](substrate-
entity-record-sketch-01.md) (Event.participants values resolve
to Entity ids); [descriptions-sketch-01](descriptions-sketch-
01.md) (updated here — PropPlaceholder $def replaced with $ref
to schema/prop.json)
**Superseded by:** nothing yet

## Purpose

Ship the remaining substrate-record schemas: `schema/prop.json`
and `schema/event.json`. Closes the substrate schema layer.

After this sketch's implementation, every substrate record
named by substrate-sketch-05 (Entity, Description, Prop, Event)
has a language-independent JSON Schema at `schema/*.json`. The
Python prototype can be thrown away; the schemas are the spec.

**Why two records in one sketch.** Prop is structurally trivial
(two fields); Event uses Prop via its effects' `prop` field.
Splitting would mean either (a) sketch-03 ships Prop with Event
waiting on sketch-04, or (b) both ship together but under
separate sketches. Both multiply overhead without benefit. The
one-record-per-sketch precedent sketch-02 established is a
default, not a rule; sketch-03 pairs the two records because
they land in the same commit either way.

**Extends sketch-01's methodology; no new PFS commitments.**
PFS1 (JSON Schema 2020-12) and PFS2 (derive-from-design-
sketches) hold unchanged. This sketch applies them to the
second-and-third substrate records, and adds one narrow
schema-layer decision (the effect-record `kind` discriminator
— see PFS3-E5 below) that deviates from the design sketch for
schema-validation convenience.

## Why now

- All three design-level forcing functions are satisfied:
  substrate-effect-shape-sketch-01 (2026-04-19) specifies
  effect shapes, substrate-prop-literal-sketch-01 (2026-04-19)
  specifies Prop shape, substrate-sketch-05 §Event internals
  already specified Event fields.
- description.json ships with a `PropPlaceholder` $def that
  needs replacement; this sketch provides the concrete Prop
  schema to reference.
- Event is the substrate's load-bearing record; without its
  schema, the production-layer story is incomplete — and
  downstream work (a markdown-fenced author parser, a prose
  exporter, a future port) all depend on knowing Event's
  shape.

## Scope — what the sketch covers

**In:**

- `schema/prop.json` — structural JSON Schema for Prop per
  substrate-prop-literal-sketch-01 PL1–PL7.
- `schema/event.json` — structural JSON Schema for Event per
  substrate-sketch-05 §Event internals + the two effect-kind
  sub-schemas inlined via `$defs`, each referencing
  `schema/prop.json` via `$ref`.
- Amendment to `schema/description.json` — the
  `PropositionAnchor` variant's `prop` field now `$ref`s
  `schema/prop.json` instead of the `PropPlaceholder`
  under-specification marker.
- Extension of `prototype/tests/test_production_format_
  sketch_01_conformance.py` to validate every encoding's
  Event records (FABULA / EVENTS_ALL) against the schemas.
  `jsonschema` Registry setup for cross-file `$ref`
  resolution.
- Conformance dispositions anticipated per sketch-01's
  precedent.

**Out:**

- **Dialect records** (Throughline, ArMythos, DSP, Signpost,
  ThematicPicks, CharacterElementAssignment, StcBeat,
  StcStrand, Argument, Scene, Beat, Character, Stakes, etc.).
  Dialect-layer schemas need their own production-format
  sketches; substrate-first.
- **Cross-boundary records** (Lowering, VerificationReview,
  StructuralAdvisory, VerifierCommentary, ArAnnotationReview,
  ArObservationCommentary, DialectReading). Same reason —
  substrate schemas first.
- **Held records.** The fold's output state. Mentioned but
  not specified in any sketch; a candidate
  `substrate-held-record-sketch-01` unblocks later.
- **Branch records.** The Branch record (sketch-04 §Branch
  representation: label + kind + parent + metadata) is
  distinct from the `branches: [string]` set on Event.
  Branch-record schema is `production-format-sketch-04` or
  later work.
- **Partial-order relations** between events. Sketch-05 says
  "partial-order relations may be used in addition to τ_s"
  but does not structurally specify the relation shape. Under
  PFS2, the schema cannot include partial-order fields until
  a design sketch specifies them. Deferred.
- **Event.descriptions inline-field.** Sketch-05 says "every
  event may have ... zero or more descriptions". This reads
  as a relationship ("descriptions may be attached to the
  event") not a record-level field ("event object has a
  descriptions array"). The attach-via-Description.
  attached_to mechanism is sufficient. If the Python
  prototype has a `descriptions` field on Event, that's a
  PFS2 conformance finding (Python over-specified) — not a
  schema inclusion.
- **Event.metadata.** Sketch-04 mentioned metadata; sketch-05
  did not carry it forward into §The five required elements
  list. The schema omits; Python conformance may find it and
  disposition accordingly.

## Commitments

Labels **PFS3**. Sub-namespaced by record (P for Prop, E for
Event, D for Description update).

### Prop

#### PFS3-P1 — schema derives from prop-literal sketch

`schema/prop.json` renders PL1–PL7 as JSON Schema 2020-12.
Two fields (PL1): `predicate` required string; `args` required
array of atomic primitives. PL4's admissible primitives map to
JSON types: string, integer, number (for float), boolean.

#### PFS3-P2 — `additionalProperties: false`

Strict shape. Consistent with Description and Entity schemas.
Undeclared fields fail validation; the Prop is exactly two
fields.

#### PFS3-P3 — args items are `oneOf` atomic types

No nested structures (PL5) encoded as schema restriction:
`items` uses `oneOf: [{type:string},{type:integer},{type:
number},{type:boolean}]`. `null` is not admitted; arrays /
objects / sub-Props are not admitted.

### Event

#### PFS3-E1 — schema derives from sketch-05 §Event internals + sub-sketches

`schema/event.json` renders substrate-sketch-05 §The five
required elements + §Additionally ... fields. Effects use
`$defs` inline (WorldEffect + KnowledgeEffect sub-schemas per
substrate-effect-shape-sketch-01 ES2 / ES3) to avoid
schema-file proliferation.

Each Prop reference (in effects' prop fields and in
preconditions) uses `$ref` to `schema/prop.json` rather than
duplicating the Prop schema inline. Cross-file $ref is standard
JSON Schema 2020-12 practice; test-layer registry resolves the
URIs to local files.

#### PFS3-E2 — required fields

From sketch-05 §The five required elements:
- `id` (string)
- `type` (string; open vocabulary; no enum restriction — see
  sketch-05 §Event type is a tag, not a key)
- `τ_s` (integer; grain is story-dependent per sketch-05)
- `τ_a` (integer)
- `participants` (object; see PFS3-E3)
- `effects` (array; see PFS3-E4)

All six required. `additionalProperties: false`.

#### PFS3-E3 — participants shape

Per sketch-05: "a dict from role-name (string) to entity-id
(or list of entity-ids for plural roles)". Schema shape:

```json
"participants": {
  "type": "object",
  "additionalProperties": {
    "oneOf": [
      {"type": "string"},
      {"type": "array", "items": {"type": "string"}, "minItems": 1}
    ]
  }
}
```

Role names are per-event-type and open-vocabulary
(sketch-05 §M1 contrast with closed enums). String value =
single Entity id; array value = multiple Entity ids (plural
roles like `witnesses`, `listeners`).

#### PFS3-E4 — effects shape (tagged-union array)

Per sketch-05: "a tuple of KnowledgeEffect and/or WorldEffect
records". Schema shape:

```json
"effects": {
  "type": "array",
  "items": {
    "oneOf": [
      {"$ref": "#/$defs/WorldEffect"},
      {"$ref": "#/$defs/KnowledgeEffect"}
    ]
  }
}
```

Tuple-vs-array is serialization detail (PFS2 discipline: JSON
has arrays, not tuples; mechanical conversion). Array order is
authored per substrate-effect-shape-sketch-01 ES6.

#### PFS3-E5 — schema-layer `kind` discriminator on effects

**Schema-layer commitment not present in substrate-effect-
shape-sketch-01.** The design sketch specifies
WorldEffect (prop + asserts) and KnowledgeEffect (holder + prop
+ via) without a discriminator field — disambiguation happens
by field presence. The schema adds an explicit `kind` field
(`"world"` or `"knowledge"`) to make records self-describing
and to simplify validation dispatch (a validator can reject a
malformed effect faster with an explicit tag than by trying
each `oneOf` variant).

This is a **schema-authoring choice beyond what the design
sketch committed to**, documented transparently per PFS2. The
Python prototype's `WorldEffect` and `KnowledgeEffect`
dataclasses distinguish by Python class identity; the schema
dump-layer (in the conformance test) adds the `kind`
discriminator during dumping, parallel to how the AnchorRef
dump adds `kind` during Description dumping.

If a future amendment to substrate-effect-shape-sketch-01
codifies the `kind` discriminator at the design-sketch level,
this schema stays unchanged. If a future amendment removes
effect discrimination entirely (single unified effect shape),
the schema and the design both change together.

#### PFS3-E6 — optional fields

Per sketch-05 §Additionally:
- `preconditions` (array of Prop; each Prop is `$ref`'d)
- `status` (enum: "committed" | "provisional")
- `branches` (array of string; branch-label strings; sketch-04
  §Branch representation per-label shape is a separate
  record whose schema this sketch does not ship — Event's
  reference is by label only)

All three optional; their omission carries sensible defaults
(no preconditions declared = none required; no status = the
sketch does not define a default; no branches = the event is on
`:canonical` per sketch-04 "Default branch is `:canonical`").

#### PFS3-E7 — deliberately NOT in schema

Explicit omissions with rationale (each is a candidate PFS2
conformance disposition if Python has the field):

- **`metadata`** — sketch-04 mentioned as Event field; sketch-
  05 did not carry forward. Absent from the schema; if Python
  has it, disposition per §Conformance dispositions.
- **`descriptions`** — sketch-05 says "zero or more descriptions"
  but this reads as a relationship (Description.attached_to
  points at Event), not a record field. Absent from the schema.
- **Partial-order relations between events** — sketch-05 says
  these "may be used in addition to τ_s" but does not specify
  the shape. PFS2 deferral.

### Description update

#### PFS3-D1 — PropositionAnchor uses `$ref` to prop.json

`schema/description.json`'s `PropositionAnchor` variant
currently carries a `prop` field of type `$ref:
#/$defs/PropPlaceholder`. This sketch replaces that reference
with `$ref: "schema/prop.json"` (or canonical URI) pointing at
the now-defined Prop schema. The `$defs/PropPlaceholder` entry
is removed.

Functionally equivalent to keeping PropPlaceholder as a
permissive object, but structurally right: the Prop shape is
now specified; the placeholder was a promissory gap-marker
whose promise is fulfilled.

## Inline schema for Prop

Authoritative for sketch-03; file lives at `schema/prop.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://brazilofmux.github.io/story/schema/prop.json",
  "title": "Prop",
  "description": "A proposition literal — a fact-shaped claim per design/substrate-prop-literal-sketch-01. Two fields; atomic primitive args only; structurally hashable (PL6); timeless at record level (PL7).",
  "type": "object",
  "required": ["predicate", "args"],
  "properties": {
    "predicate": {
      "type": "string",
      "minLength": 1,
      "description": "Relation name from an open per-story vocabulary (PL2). Two substrate-reserved names at v1: 'identity' (identity-and-realization-sketch-01) and 'at_location' (unity-of-place checks)."
    },
    "args": {
      "type": "array",
      "description": "Ordered tuple of atomic primitive values (PL3, PL4). Strings are Entity-id references; int/number/boolean are literal values with structural fold-consequence. PL5 prohibits nested/composite/null values; this is enforced by items' oneOf.",
      "items": {
        "oneOf": [
          {"type": "string"},
          {"type": "integer"},
          {"type": "number"},
          {"type": "boolean"}
        ]
      }
    }
  },
  "additionalProperties": false
}
```

## Inline schema for Event

Authoritative for sketch-03; file lives at `schema/event.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://brazilofmux.github.io/story/schema/event.json",
  "title": "Event",
  "description": "A structural event in the fabula per design/substrate-sketch-05 §Event internals. Six required fields + three optional; effects are a tagged-union array of WorldEffect / KnowledgeEffect sub-records; Props are $ref'd to schema/prop.json.",
  "type": "object",
  "required": ["id", "type", "τ_s", "τ_a", "participants", "effects"],
  "properties": {
    "id": {
      "type": "string",
      "minLength": 1,
      "description": "Stable identifier, scoped per story."
    },
    "type": {
      "type": "string",
      "minLength": 1,
      "description": "Event-type tag from an open per-story vocabulary (sketch-05 §Event type is a tag, not a key). No closed enum; substrate does not dispatch on type."
    },
    "τ_s": {
      "type": "integer",
      "description": "Story-time coordinate. Grain is story-dependent; the substrate does not enforce a single scale."
    },
    "τ_a": {
      "type": "integer",
      "minimum": 0,
      "description": "Authored time; monotonic per story; shared sequence with descriptions."
    },
    "participants": {
      "type": "object",
      "description": "Dict from role-name (string) to entity-id (string) or list of entity-ids (array). Role names are per-event-type, open vocabulary (sketch-05 §The five required elements).",
      "additionalProperties": {
        "oneOf": [
          {"type": "string"},
          {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
          }
        ]
      }
    },
    "effects": {
      "type": "array",
      "description": "Tuple of WorldEffect and/or KnowledgeEffect records (substrate-effect-shape-sketch-01 ES1–ES7). Order is authored (ES6); the 'kind' discriminator on each record disambiguates the two shapes (schema-layer decision PFS3-E5).",
      "items": {
        "oneOf": [
          {"$ref": "#/$defs/WorldEffect"},
          {"$ref": "#/$defs/KnowledgeEffect"}
        ]
      }
    },
    "preconditions": {
      "type": "array",
      "description": "Optional. Tuple of Prop records that must hold in world state at τ_s for the event to be consistent (sketch-05 §The five required elements, §Additionally).",
      "items": {"$ref": "https://brazilofmux.github.io/story/schema/prop.json"}
    },
    "status": {
      "type": "string",
      "enum": ["committed", "provisional"],
      "description": "Authorial commitment axis (sketch-04 §Event status and branch kinds)."
    },
    "branches": {
      "type": "array",
      "items": {"type": "string"},
      "uniqueItems": true,
      "description": "Set of branch labels the event appears on (sketch-04 §Branch representation). Omitted = default to {':canonical'}."
    }
  },
  "additionalProperties": false,
  "$defs": {
    "WorldEffect": {
      "type": "object",
      "description": "A fact-assertion or fact-retraction on world state per substrate-effect-shape-sketch-01 ES2. The 'kind' field is a schema-layer discriminator (PFS3-E5), not present in the design-sketch shape but added for validation-dispatch convenience.",
      "required": ["kind", "prop", "asserts"],
      "properties": {
        "kind": {"const": "world"},
        "prop": {"$ref": "https://brazilofmux.github.io/story/schema/prop.json"},
        "asserts": {"type": "boolean"}
      },
      "additionalProperties": false
    },
    "KnowledgeEffect": {
      "type": "object",
      "description": "An update to a specific agent's knowledge state per substrate-effect-shape-sketch-01 ES3–ES4. 'holder' is an Entity-id reference (agent-kind); 'via' encodes direction and provenance-kind from a closed 11-value vocabulary (6 diegetic + 5 narrative).",
      "required": ["kind", "holder", "prop", "via"],
      "properties": {
        "kind": {"const": "knowledge"},
        "holder": {
          "type": "string",
          "description": "Entity-id of the agent whose knowledge updates (substrate-entity-record-sketch-01 SE3 kind='agent' expected; substrate does not enforce at record level per ES3)."
        },
        "prop": {"$ref": "https://brazilofmux.github.io/story/schema/prop.json"},
        "via": {
          "type": "string",
          "enum": [
            "observation",
            "utterance-heard",
            "inference",
            "deception",
            "forgetting",
            "realization",
            "disclosure",
            "focalization",
            "omission",
            "framing",
            "retroactive-reframing"
          ],
          "description": "Update-operator vocabulary from substrate-sketch-04 §Update operators + substrate-effect-shape-sketch-01 ES4. Diegetic vocabulary for character-agent holders; narrative vocabulary for the reader."
        }
      },
      "additionalProperties": false
    }
  }
}
```

Notes on design choices:

- **Cross-file `$ref` via full URIs.** Each `$ref` to prop
  uses the canonical URI `https://brazilofmux.github.io/story/schema/prop.json`.
  Validators resolve the URI via a registry; the URI does not
  need to fetch (PFS1 same as sketch-01 — identity, not fetch
  target).
- **`additionalProperties: false` throughout.** Consistent
  with Description and Entity schemas. Every undeclared field
  is a finding.
- **`τ_s` has no `minimum`.** Sketch-05 admits negative τ_s
  for pre-play antecedent action (Oedipus Tyrannus uses τ_s
  from E_birth onwards; pre-play events are negative). `τ_a`
  has `minimum: 0` because authored-time monotonicity starts
  at zero.
- **No `metadata` or `descriptions` field.** Per PFS3-E7. If
  conformance surfaces one in Python, it's a PFS2 finding.

## Conformance dispositions

Anticipated from the corpus survey run during this sketch's
authoring. The scan: look for attributes on Python `Event`
instances not covered by the schema's properties.

**Anticipated dispositions** (pre-implementation guesses;
validated or corrected during the implementation pass):

- **`Event.metadata`.** Sketch-04 named it; sketch-05 did not
  carry it forward. If Python has it, disposition: sketch-05
  was implicit about preservation; amendment to
  sketch-05 (or this sketch) decides whether metadata is a
  keeper. Most likely outcome: Python over-specified; field
  absent from corpus; no schema amendment.
- **`Event.descriptions`.** Same question. Anticipated: Python
  may have the field from sketch-04's era; the field may or
  may not be populated across the corpus. If unpopulated,
  trivially absorbed; if populated, real decision needed
  (attach-via-Description vs. inline-on-Event).
- **Partial-order relations** (sketch-05 mentions but does
  not shape-specify). If Python has a `partial_order` or
  similar field, schema cannot admit it (PFS2 says design
  sketch must specify first); disposition defers to a future
  sketch.
- **`Event.effect_count` / computed fields.** Verifier
  helpers compute these; they are not stored fields. If
  Python exposes any as attributes on Event, the dump logic
  excludes them.
- **Empty ENTITIES-like re-export inflation.** As with
  sketch-02, lowering + verification modules may re-export
  FABULA / EVENTS_ALL. The conformance test discovers by
  naming convention; duplicate validation is harmless.

**Anticipated-findings-not-dispositions** (schema should pass
these cleanly):

- Positive and negative `τ_s` values (Oedipus's antecedent
  action is negative).
- Various `via` values across the 11-value vocabulary.
- Events with and without `preconditions`.
- Events on `:canonical` alone, on a single `:contested`
  branch, or trans-branch.

Findings land here verbatim during implementation. Absence of
findings in a category = the field is admitted cleanly.

## Open questions

1. **OQ1 — Cross-file `$ref` test infrastructure.** The test
   module needs a `jsonschema.referencing.Registry` that maps
   the canonical URIs to local files. First time this pattern
   appears in the test; pattern land under PEA implementation.
2. **OQ2 — Event.descriptions as relationship-not-field.**
   PFS3-E7 commits to not having a field; if the corpus
   exercises the field, this sketch amends to add it as an
   optional array of strings (description ids). Forcing
   function: corpus population > 0 for `descriptions` field.
3. **OQ3 — τ_s scale declaration.** Sketch-05 says "grain is
   story-dependent". An encoding using hours-since-play-start
   for one story and calendar-years for another has the same
   `integer` type but different semantics. No per-story scale
   declaration is a schema field today. Future sketch may add
   a `Story` (or `Work`) record containing metadata like
   `τ_s_scale: "hours" | "years" | ...`. Out of scope here.
4. **OQ4 — Reserved predicate names in the corpus.** PL2
   names `identity` and `at_location` as substrate-reserved.
   A conformance pass could flag use of reserved predicate
   names with non-canonical arg shape. Not this sketch;
   future verifier.
5. **OQ5 — Event.type open vocabulary vs. an emerging
   registry.** The corpus has tens of distinct event types.
   No schema enum — open per sketch-05. A future sketch may
   consolidate a registry if cross-encoding type-name
   collisions become a problem.

## Acceptance criteria

Labels **P3A** (Production Sketch-3 Acceptance).

- **[P3A1]** `schema/prop.json` per the inline spec.
  Metaschema-valid under Draft202012Validator.
- **[P3A2]** `schema/event.json` per the inline spec.
  Metaschema-valid. Cross-file `$ref` to prop.json resolved
  by test-layer registry.
- **[P3A3]** `schema/description.json` updated — the
  `PropositionAnchor` variant's `prop` field changes from
  `$ref: "#/$defs/PropPlaceholder"` to `$ref:
  "https://brazilofmux.github.io/story/schema/prop.json"`.
  The `$defs/PropPlaceholder` entry is removed.
- **[P3A4]** Conformance test extended to validate FABULA /
  EVENTS_ALL / equivalent tuples across encodings. Registry
  setup resolves cross-file `$ref`s. Effects dump-logic adds
  the `kind` discriminator per PFS3-E5.
- **[P3A5]** All conformance checks pass, OR each failure
  has a §Conformance dispositions entry (this sketch's
  amendment) with explicit resolution path.
- **[P3A6]** No change to any Python source outside
  `prototype/tests/` and `prototype/requirements.txt`
  (which needs no change — `jsonschema` + `referencing`
  already in requirements from sketch-01's implementation).
- **[P3A7]** The existing test suite continues to pass (695
  tests post-sketch-02; + whatever conformance tests this
  sketch adds — Event surface is larger than Entity's, so
  5–10 new tests is expected).

## Summary

Third production sketch; closes the substrate schema layer.
Ships `schema/prop.json` + `schema/event.json`; updates
`schema/description.json` to consume Prop by `$ref`.

- Prop is two fields (predicate + args); args admit
  {string, integer, number, boolean} per PL4.
- Event is six required + three optional fields per
  sketch-05 §Event internals. Effects are a tagged-union
  array with inline `$defs` for WorldEffect and
  KnowledgeEffect; each references Prop by `$ref`.
- Schema-layer adds a `kind` discriminator to the effect
  records (PFS3-E5) — a self-description convenience not
  present in the design sketch. Documented transparently.
- Three fields deliberately NOT in the Event schema:
  `metadata`, `descriptions`, and partial-order relations.
  Each absence is per PFS2: sketch-05 does not structurally
  commit, so the schema does not admit.

Expected conformance outcome: larger than Entity (smaller
than Description), with 1–3 dispositions for Python
over-specified fields the sketches retired. Each disposition
lands in §Conformance dispositions verbatim.

After this sketch's implementation, the substrate schema
layer is complete: Entity + Description + Prop + Event + the
effect sub-schemas. Four records; five files
(entity/description/prop/event/README);
one conformance test module. Any language with a JSON Schema
2020-12 validator can read the `schema/` tree and validate a
story's substrate against it. The Python prototype is
disposable.

Next arcs (user-choice):

- Dialect schemas (Throughline, ArMythos, etc. — each dialect
  its own production sketch).
- Held record (the fold output state — a new design sketch
  then production sketch).
- Branch record (sketch-04 §Branch representation — already
  design-specified; a slim production sketch suffices).
- Cross-boundary records (Lowering, VerificationReview,
  ArAnnotationReview, etc. — multiple production sketches).

Substrate is done.
