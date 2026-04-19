# Production format — sketch 02

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (extension of
[production-format-sketch-01](production-format-sketch-01.md),
not a replacement — sketch-01's PFS1 + PFS2 remain in force;
sketch-02 runs them for a second record)
**Frames:** [production-format-sketch-01](production-format-
sketch-01.md) (PFS1 JSON Schema 2020-12; PFS2 derivation
discipline; PFS5 repository layout), [substrate-entity-record-
sketch-01](substrate-entity-record-sketch-01.md) (the design-
level record specification this production sketch derives from)
**Related:** [descriptions-sketch-01](descriptions-sketch-01.md)
(the design-level record for Description that sketch-01
derived from — Entity's parallel is now
substrate-entity-record-sketch-01)
**Superseded by:** nothing yet

## Purpose

Ship `schema/entity.json`. Second record schema under the
methodology production-format-sketch-01 established (PFS1:
JSON Schema 2020-12; PFS2: derive from design sketches, never
from Python). Entity was deferred in sketch-01 because
substrate-sketch-05 §Entities was ontological-only; the gap is
now filled by substrate-entity-record-sketch-01 (SE1–SE6),
which unblocks the schema.

This sketch is narrow: it is the production-layer spec for one
record whose design-layer spec lands separately. Mostly
references sketch-01 and the design sketch; makes a few
record-specific commitments (conformance dispositions scoped to
Entity; acceptance criteria for the schema file + test
extension).

## Why now

- Substrate-entity-record-sketch-01 (2026-04-19) structurally
  specified Entity per the "design-before-schema" discipline.
- Production-format-sketch-01 §PFS2 caught real drift explicitly
  named this sketch (in effect) as the follow-up once the
  design sketch landed. The forcing function is satisfied; the
  work is unblocked.
- Corpus survey (83 Entity records across 5 encodings) confirms
  the design sketch's commitments cover every entity in the
  corpus — no surprise findings blocking the schema.

## Scope — what the sketch covers

**In:**

- Commitment that `schema/entity.json` derives from
  substrate-entity-record-sketch-01 under production-format-
  sketch-01 PFS1 + PFS2.
- The record-specific schema design choices (kind enum,
  required-fields list, `additionalProperties: false`
  strictness) that follow from SE1–SE6.
- Extension of the existing conformance test
  (`prototype/tests/test_production_format_sketch_01_conformance.py`)
  to cover ENTITIES from every encoding. The test module keeps
  its existing name (the sketch-01 + sketch-02 surfaces are one
  test surface; no reason to split).
- Anticipated conformance dispositions for Entity specifically.

**Out:**

- Any revisit of PFS1 / PFS2 — those commitments carry forward
  from sketch-01 unchanged.
- `Event` and `Prop` — still deferred pending their own design-
  level record sketches (`substrate-effect-shape-sketch-01`,
  `substrate-prop-literal-sketch-01`). Either could be
  unblocked by a production-format-sketch-03.
- Repository layout changes. `schema/` already exists at repo
  root per PFS5.
- Changes to `schema/description.json` — sketch-01 ships what
  it ships.

## Commitments

Labels **PFE** (Production Format — Entity).

### PFE1 — Schema derives from substrate-entity-record-sketch-01

`schema/entity.json` renders SE1–SE6 as JSON Schema 2020-12.
Authoring discipline follows production-format-sketch-01 PFS2:
source of truth is the design sketch; the Python prototype's
`Entity` dataclass is a conformance check only.

### PFE2 — Required-fields + `additionalProperties: false`

Per SE2: the three required fields are `id`, `name`, `kind`.
The schema enforces `required: ["id", "name", "kind"]` and
`additionalProperties: false`. Matches sketch-01's discipline
for Description — strict shape, no silent-passing undeclared
fields.

### PFE3 — kind is a closed enum at v1

Per SE3: the schema's `kind` property is a string enum with
exactly four values: `"agent"`, `"object"`, `"location"`,
`"abstract"`. Extensions go through SE3's protocol: amend
substrate-entity-record-sketch-01 first; then amend this sketch
(or its successor); then widen the schema enum.

### PFE4 — No τ_a; no optional fields

Per SE5: the record is timeless. The schema declares no
`τ_a`-equivalent. Per SE2: no optional fields. The entire Entity
schema is three required string fields, one of which is an enum.
This is deliberately minimal.

## Inline schema (authoritative; file lives at `schema/entity.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://brazilofmux.github.io/story/schema/entity.json",
  "title": "Entity",
  "description": "A referable thing in a story — a character, place, physical object, or abstract concept — per design/substrate-entity-record-sketch-01.md. Exactly three fields; timeless at record level (SE5); identity per-story-local (SE6).",
  "type": "object",
  "required": ["id", "name", "kind"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Stable identifier, scoped per story (SE2, SE6)."
    },
    "name": {
      "type": "string",
      "description": "Display handle used by authoring tools, rendering, probe prompts (SE2). Non-empty in practice across the current corpus."
    },
    "kind": {
      "type": "string",
      "description": "Discriminator naming what sort of referable thing this is (SE3). Each value corresponds to a structural distinction the substrate or a dialect dispatches on.",
      "enum": ["agent", "object", "location", "abstract"]
    }
  },
  "additionalProperties": false
}
```

Notes on design choices:

- No `minLength` on `id` or `name`. SE2 says "non-empty name in
  the corpus" but does not mandate non-empty at the substrate
  level. Future encoding may want anonymous entities (a `kind:
  "abstract"` stand-in for "the truth itself" with no
  meaningful name). Empty strings are legal unless SE2 is
  amended to forbid.
- `additionalProperties: false`. Strict; undeclared fields
  fail validation. Matches Description's discipline. An
  encoding that adds an ad-hoc field to its Python Entity
  dataclass would break conformance, surfacing as a finding.
- No format constraint on `id` (no regex requirement for
  identifier-like strings). The design sketch says "stable
  identifier"; it does not enumerate syntax rules. Practically,
  the current corpus uses snake_case ids, but this is
  convention, not substrate requirement. If a substrate rule
  is added later, schema amends.

## Conformance dispositions

Anticipated from the corpus survey run during this sketch's
authoring (n=83 Entity records across rashomon, oedipus,
macbeth, rocky, ackroyd):

- **All four kind values exercised.** `agent`: 50. `location`:
  25. `abstract`: 5. `object`: 3. No out-of-enum kinds present.
- **All names non-empty.** 83/83.
- **All ids non-empty strings.** 83/83.
- **`additionalProperties: false` disposition.** The current
  Python `Entity` dataclass has exactly three fields; asdict
  produces a three-key dict. No anticipated disposition.

**Prediction:** 83 clean conformance passes, 0 failures,
0 known dispositions applied. If the implementation surfaces a
discrepancy this section didn't anticipate, it lands here as a
disposition per PFS2.

## Acceptance criteria

Labels **PEA** (Production Entity Acceptance). Slim — most of
the discipline is inherited from production-format-sketch-01's
PFA.

- **[PEA1]** `schema/entity.json` per the inline spec in this
  sketch. Metaschema-valid under Draft202012Validator.
- **[PEA2]** `prototype/tests/test_production_format_
  sketch_01_conformance.py` extended to validate ENTITIES from
  every discovered encoding. Test discovery uses the same
  "ENTITIES attribute on module" naming convention it already
  uses for DESCRIPTIONS.
- **[PEA3]** All conformance checks pass. If any fails, it
  lands in §Conformance dispositions above (this sketch's
  amendment) with an explicit resolution path, per sketch-01's
  PFS2 discipline.
- **[PEA4]** No change to any Python source outside
  `prototype/tests/` and `prototype/requirements.txt`.
  `prototype/story_engine/core/substrate.py`'s Entity
  dataclass remains untouched. Conformance is achieved by
  schema + dump logic in the test module, per the discipline
  sketch-01 established.

Implementation lands in a single commit after this design
commit; no separate "implementation sketch" since PEA is short.

## Summary

Narrow production sketch. Ships `schema/entity.json` under the
same discipline production-format-sketch-01 established, now
that substrate-entity-record-sketch-01 has filled the design-
level spec gap. Three required fields; closed kind enum at four
values; no optional fields; timeless record.

Expected conformance: 83/83 clean passes across the current
corpus, validated by the existing conformance test module
(extended by PEA2). No new dispositions anticipated; if any
surface, they land here per the established pattern.

Event and Prop remain deferred. `substrate-effect-shape-sketch-
01` and `substrate-prop-literal-sketch-01` are the next
design-level forcing functions, either of which unblocks a
production-format-sketch-03 or amendment.
