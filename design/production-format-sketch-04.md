# Production format — sketch 04

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing — extends
[production-format-sketch-01](production-format-sketch-01.md)'s
methodology (PFS1 + PFS2 unchanged) and continues the
one-record-per-sketch cadence (sketch-02's default) with a
scoped schema amendment riding along because they are
inseparably coupled
**Frames:** [production-format-sketch-01](production-format-
sketch-01.md) (PFS1 JSON Schema 2020-12, PFS2 derivation
discipline, PFS5 repository layout), [production-format-
sketch-03](production-format-sketch-03.md) (PFS3-E5 effect
kind discriminator, cross-file `$ref` registry pattern,
KnowledgeEffect sub-schema this sketch amends), [substrate-
held-record-sketch-01](substrate-held-record-sketch-01.md)
(the design-layer spec for Held; SH1–SH8, including the SH8
`remove` polarity and the ES3-amendment this sketch
materializes at the schema layer)
**Related:** [substrate-effect-shape-sketch-01](substrate-
effect-shape-sketch-01.md) (ES3 — the text this sketch's
amendment revises; sketch-04 codifies the revision at the
schema layer); [substrate-sketch-05](substrate-sketch-05.md)
§K1 (the fold whose output Held is)
**Superseded by:** nothing yet

## Purpose

Ship `schema/held.json` — the canonical schema for the Held
fold-output / effect-input record specified by substrate-
held-record-sketch-01. Amend `schema/event.json`'s
KnowledgeEffect sub-schema to consume Held by `$ref` and to
admit the `remove` polarity the Held sketch's SH8 + ES3-
amendment commit.

**Why one record plus a scoped amendment in one sketch.** The
Held sketch's ES3-amendment changes the KnowledgeEffect shape
from `(holder, prop, via)` to `(holder, held, remove)`.
Shipping `schema/held.json` without the corresponding
`schema/event.json` amendment would leave the Event schema
out-of-sync with the design sketches. Shipping the amendment
without Held would leave `held` referencing a non-existent
schema. They land together.

**Extends sketch-01's methodology; no new PFS commitments.**
PFS1 + PFS2 + PFS5 unchanged. This sketch is the fifth
record under the substrate-schema layer (after Description,
Entity, Prop, Event) and the first schema *amendment* the
production track ships. The amendment pattern — revise a
prior schema in response to a design-sketch amendment — is
itself a PFS2 consequence: when a design sketch amends, the
schemas derived from it follow.

## Why now

- The design-layer forcing function is satisfied: substrate-
  held-record-sketch-01 (2026-04-19) specifies SH1–SH8,
  including the ES3-amendment that drives the Event schema
  change.
- Production-format-sketch-03's §Conformance dispositions
  §Disposition 1 (KnowledgeEffect shape translation) and
  §Disposition 2 (KnowledgeEffect.remove) are both retired
  by this sketch — Disposition 1 becomes a trivial field
  rename, and Disposition 2 closes (the remove polarity is
  now a first-class field, not Python-over-specification).
  The audit test's baseline interpretation shifts from
  "drift-to-zero" to "baseline-is-final".
- Corpus validation is ready: 102 unique events across 5
  encodings, 458 with re-export inflation; every Held nested
  inside a KnowledgeEffect (and transitively every Held the
  fold would produce) must conform to `schema/held.json`.

## Scope — what the sketch covers

**In:**

- `schema/held.json` — structural JSON Schema for Held per
  substrate-held-record-sketch-01 SH1–SH7.
- Amendment to `schema/event.json`'s KnowledgeEffect
  sub-schema — swaps the flat `(kind, holder, prop, via)`
  shape for `(kind, holder, held, remove?)` where `held` is
  `$ref`'d to `schema/held.json` and `remove` is an optional
  boolean defaulting to False.
- Extension of `prototype/tests/test_production_format_
  sketch_01_conformance.py`:
  - new Held metaschema validity + shape-spot-check tests;
  - new corpus conformance test: every Held nested inside a
    corpus KnowledgeEffect validates against `schema/held.json`;
  - re-validation of existing event conformance under the
    amended KnowledgeEffect sub-schema;
  - rewritten `_dump_knowledge_effect` helper emitting the
    nested Held and propagating `remove`;
  - new `_dump_held` helper;
  - revised audit docstring for `test_knowledge_effect_remove_
    audit` (baseline-is-final, not drift-to-zero).
- Conformance dispositions anticipated (§Conformance
  dispositions populated during implementation).

**Out:**

- **Python prototype refactor.** The Python's current
  KnowledgeEffect `(agent_id, held, remove)` shape already
  matches the amended schema at the field level; only the
  dump-layer translation (agent_id → holder, emit nested
  held, propagate remove) needs updating. A broader Python
  refactor (renaming `agent_id` to `holder` across all
  encodings) is out of this sketch's scope — a future arc
  may do it, but the conformance test routes around today.
- **Dialect records' Held consumption.** If an upper-dialect
  record ever references Held directly (e.g., a Throughline
  summarizing the agent's Held-set at a signpost), the Held
  schema is ready — but dialect-layer schemas are later work.
- **KnowledgeState schema.** The full per-agent-per-τ_s state
  is a collection of Helds plus an agent_id; its schema is
  trivially derivable but serves no current consumer (the
  fold produces KnowledgeState in memory and nothing serializes
  it yet). Deferred until a consumer appears.
- **Held inside WorldEffect.** WorldEffect does not carry a
  Held (world state is a set of Props; no slot/confidence/via).
  The amendment is to KnowledgeEffect only.

## Commitments

Labels **PFS4**. Sub-namespaced by record (H for Held,
E-amendment for Event update, D for dump-layer change).

### Held

#### PFS4-H1 — schema derives from held-record sketch

`schema/held.json` renders SH1–SH7 as JSON Schema 2020-12.
Five required fields (SH2): `prop`, `slot`, `confidence`,
`via`, `provenance`. Each field maps to a JSON-native type
with closed enums where the design sketch commits closed.

#### PFS4-H2 — `additionalProperties: false`

Strict shape per the PFS1 discipline already applied to
Entity, Description, Prop, and Event. Undeclared fields fail
validation.

#### PFS4-H3 — Prop via cross-file `$ref`

The `prop` field references `schema/prop.json` the same way
`schema/event.json` does (PFS3-E1). Cross-file `$ref` via the
canonical URI resolves through the `referencing.Registry`
already set up by the test module.

#### PFS4-H4 — Slot closed enum (four values)

`slot` is a string with `enum: ["known", "believed",
"suspected", "gap"]`. Matches SH3's closed-at-v1 vocabulary.
BLANK is not admitted (SH3: collapsed to GAP per Python's
existing convention).

#### PFS4-H5 — Confidence closed enum (four values)

`confidence` is a string with `enum: ["certain", "believed",
"suspected", "open"]`. Matches SH4's closed-at-v1 vocabulary.

#### PFS4-H6 — Via closed enum (shared with KnowledgeEffect)

`via` is a string with the same 11-value enum the Event
schema's KnowledgeEffect sub-schema currently uses (6
diegetic + 5 narrative per substrate-effect-shape-sketch-01
ES4). The enum is inlined in `schema/held.json`; the Event
schema's KnowledgeEffect no longer needs the enum directly
(the via moves inside the nested Held).

**Why inlined, not a shared `$defs`.** JSON Schema 2020-12
supports cross-file `$defs` references, but the duplication
cost is low (11 short strings) and the coupling cost is
higher (a shared $defs would require a third schema file
just for the enum). Inlining once, in the record that
authoritatively owns via per SH2 and ES3-amendment, is
cleaner. If a third consumer appears, consolidation is easy.

#### PFS4-H7 — Provenance as array of strings

`provenance` is an array; `items` is a plain `{type:
"string"}`. No structural commitment on the string content
(SH6 commits provenance is display-layer, not machinery-
visible). Empty array is admissible (SH2 does not mandate
non-empty provenance — a default-constructed Held with empty
provenance is legal).

### Event update

#### PFS4-E-amend-1 — KnowledgeEffect sub-schema rewrite

`schema/event.json`'s `$defs.KnowledgeEffect` changes shape:

- **Before** (per PFS3-E5 + sketch-03's inline spec):
  ```json
  "required": ["kind", "holder", "prop", "via"],
  "properties": {
    "kind": {"const": "knowledge"},
    "holder": {"type": "string", "..."},
    "prop": {"$ref": ".../prop.json"},
    "via": {"type": "string", "enum": [11 values], "..."}
  }
  ```
- **After:**
  ```json
  "required": ["kind", "holder", "held"],
  "properties": {
    "kind": {"const": "knowledge"},
    "holder": {"type": "string", "..."},
    "held": {"$ref": ".../held.json"},
    "remove": {"type": "boolean", "default": false, "..."}
  }
  ```

The `prop` and `via` fields move inside the nested Held
(SH5 + ES3-amendment). The `remove` polarity is added as an
optional boolean (SH8). `additionalProperties: false` stays.

#### PFS4-E-amend-2 — remove is optional; default False

`remove` is not in `required`. Absent = False = write-effect.
Present-and-True = dislodge-effect. The schema's
`default: false` is descriptive; validators do not synthesize
the default into the validated object, but tooling consuming
the schema can read the default to know the implicit value.

#### PFS4-E-amend-3 — held is required

`held` IS in `required`. A KnowledgeEffect always carries a
Held — even `remove=True` effects (per SH8 §The nested Held
is a tooling convenience: the author names what is being
dislodged). Requiring the field matches Python practice (the
corpus has no `remove=True` effect without a populated Held)
and keeps the schema honest about what the record shape is.

#### PFS4-E-amend-4 — WorldEffect unchanged

WorldEffect's sub-schema `(kind, prop, asserts)` is untouched.
The sketch's amendment scope is KnowledgeEffect only.

### Dump-layer changes

#### PFS4-D1 — _dump_knowledge_effect rewritten

The test module's `_dump_knowledge_effect` helper changes:

- **Before** (sketch-03 line 302–307): emits
  `{kind, holder, prop, via}`; drops slot/confidence/
  provenance/remove.
- **After:** emits `{kind, holder, held}` (with `held` via
  `_dump_held`); also emits `{remove: True}` when the effect's
  remove is True (and omits the field when False, relying on
  the schema default).

#### PFS4-D2 — _dump_held (new)

A new helper emits a Held as:

```python
{
    "prop": _dump_prop(held.prop),
    "slot": held.slot.value,          # Slot enum → string
    "confidence": held.confidence.value,  # Confidence enum → string
    "via": held.via,                  # already a string
    "provenance": list(held.provenance),  # tuple → array
}
```

No field dropping. Python's Held and the schema's Held are
field-for-field isomorphic under this sketch.

#### PFS4-D3 — remove audit docstring revision

`test_knowledge_effect_remove_audit` keeps its behavior
(count remove=True instances, print, no assertion) but the
docstring changes to reflect the new interpretation:

- **Before** (sketch-03's disposition framing): "A future
  encoding-side refactor per identity-and-realization-sketch-
  01 §Prior encoding's workaround, and its retirement drives
  the count to 0."
- **After:** "Per substrate-held-record-sketch-01 SH8, the
  remove polarity is a legitimate KnowledgeEffect field
  supporting factual dislodgement. The current count (7 as of
  2026-04-19) is the intended baseline, not a drift target.
  Drift below 0 is not possible; significant drift above is a
  finding (a new encoding authored a remove=True pattern that
  should perhaps use a write-effect instead, or the
  dislodgement idiom is spreading in ways worth tracking)."

The audit's informational character stays; only the reading
of the baseline changes.

## Inline schema for Held

Authoritative for sketch-04; file lives at `schema/held.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://brazilofmux.github.io/story/schema/held.json",
  "title": "Held",
  "description": "An agent's per-proposition held record per design/substrate-held-record-sketch-01 SH1–SH7. Five required fields; the K1 fold's output cell AND (under the ES3-amendment) the authored shape nested inside a KnowledgeEffect.",
  "type": "object",
  "required": ["prop", "slot", "confidence", "via", "provenance"],
  "properties": {
    "prop": {
      "$ref": "https://brazilofmux.github.io/story/schema/prop.json",
      "description": "The proposition this Held record asserts the agent holds (SH2)."
    },
    "slot": {
      "type": "string",
      "enum": ["known", "believed", "suspected", "gap"],
      "description": "Epistemic classification (SH3). BLANK is collapsed to GAP per Python's existing convention. Identity substitution (identity-and-realization-sketch-01 I7) fires only on slot=known for identity/2 propositions."
    },
    "confidence": {
      "type": "string",
      "enum": ["certain", "believed", "suspected", "open"],
      "description": "Ordinal confidence level (SH4). Orthogonal-in-principle to slot; typically co-varies. OQ1 banks a potential future collapse to a single epistemic-strength field."
    },
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
      "description": "The via-operator that most recently placed this Held into the agent's set (SH2). 6 diegetic values for character-agent holders; 5 narrative values for reader holders. Closed vocabulary from substrate-sketch-04 §Update operators + substrate-effect-shape-sketch-01 ES4."
    },
    "provenance": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Free-form authoring trail (SH6). Not substrate-machinery-visible; display-layer content only. Empty array is admissible."
    }
  },
  "additionalProperties": false
}
```

## Inline schema — KnowledgeEffect amendment to schema/event.json

The full schema/event.json file is unchanged except for the
`$defs.KnowledgeEffect` block. That block, after the
amendment:

```json
"KnowledgeEffect": {
  "type": "object",
  "description": "An update to a specific agent's knowledge state per substrate-effect-shape-sketch-01 ES3 (as amended by substrate-held-record-sketch-01 SH5 + SH8). The effect carries a holder reference, a full Held record (prop/slot/confidence/via/provenance all live on the Held), and an optional remove polarity.",
  "required": ["kind", "holder", "held"],
  "properties": {
    "kind": {"const": "knowledge"},
    "holder": {
      "type": "string",
      "description": "Entity-id of the agent whose knowledge updates (substrate-entity-record-sketch-01 SE3 kind='agent' expected; substrate does not enforce at record level per ES3)."
    },
    "held": {
      "$ref": "https://brazilofmux.github.io/story/schema/held.json",
      "description": "The authored Held record (SH5). On a write-effect (remove omitted or false) the fold writes this Held into the agent's KnowledgeState at the event's (branch, τ_s). On a dislodge-effect (remove: true) the fold drops the prior Held at (holder, prop); the nested Held here documents what is being dislodged but is not written (SH8)."
    },
    "remove": {
      "type": "boolean",
      "default": false,
      "description": "Polarity flag (SH8). Absent or false = write the Held into the state. True = dislodge the prior Held at (holder, prop); the nested `held` documents the dislodgement but is not written."
    }
  },
  "additionalProperties": false
}
```

Notes on design choices:

- **`held` is required even for remove=True effects** (PFS4-
  E-amend-3). Authorial clarity + current corpus practice.
- **`remove` is optional with default false** (PFS4-E-amend-
  2). The write-effect is the common case; requiring every
  effect to carry `"remove": false` would be noise.
- **Cross-file `$ref`.** Same pattern as Event's Prop refs;
  the test-layer registry resolves the URI.

## Conformance dispositions

Populated during the implementation pass. Two anticipated
dispositions (both resolved by this sketch):

### Disposition 1 (formerly sketch-03 Disposition 1): KnowledgeEffect shape — retired

The translation layer simplifies. Python's `KnowledgeEffect.
held` is a full Held record; the schema's `KnowledgeEffect.
held` is a full Held record. The dump-layer translation
becomes a field rename (`agent_id` → `holder`) plus a
mechanical recursive dump of `held`. No fields discarded.

This disposition is therefore **not a disposition anymore**
under the amended schema. The prior "Python over-specified"
reading was an artifact of ES3's under-specification; the
ES3-amendment aligns the two.

### Disposition 2 (formerly sketch-03 Disposition 2): KnowledgeEffect.remove — retired

The `remove: bool` field is now admitted by the schema per
PFS4-E-amend-1 + PFS4-E-amend-2. The dump emits it; the
schema validates it. No audit-surface needed to count drift;
the count is baseline-is-final.

The audit test remains (PFS4-D3) for operational visibility —
a jump from 7 to 40 is worth noticing — but its framing
changes.

### Disposition 3 (anticipated): Held.provenance tuple-vs-array

Python's Held stores `provenance` as a tuple; JSON has no
tuple type (arrays only). Mechanical conversion at dump time
(`list(held.provenance)`). Parallel to Prop.args' tuple→array
conversion in sketch-03. Not a PFS2 finding; mechanical.

### Disposition 4 (anticipated): Python Slot / Confidence enum string values

Python's `Slot` and `Confidence` enums are `str` subclasses
with lowercase values (`"known"`, `"believed"`, etc.) that
match the schema's enum values exactly. Dump-time
`.value` access yields the enum string. No translation
needed beyond the attribute access; mechanical.

### Non-dispositions: clean validations expected

- **All 4 slot values exercised.** KNOWN appears in (most)
  observation and realization contexts; BELIEVED in utterance-
  heard contexts; SUSPECTED in partial-inference contexts
  (Rashomon testimony); GAP in Oedipus's real_parents_
  identified placeholder. Schema admits all four.
- **All 4 confidence values exercised.** CERTAIN, BELIEVED,
  SUSPECTED paired with same-name slots; OPEN with GAP.
- **11 via values.** 6 diegetic exercised across the corpus;
  the 5 narrative values not yet exercised (no reader-state
  events in the substrate corpus today — the Aristotelian
  probe operates at the dialect layer, which is not in this
  sketch's corpus-conformance scope).
- **Empty provenance.** Corpus has no empty-provenance Held
  today; if a test encoding produces one, schema admits.
- **Re-export inflation.** Same as sketch-02 / sketch-03;
  458 raw validations, 102 distinct events; duplicates
  harmless.

## Open questions

1. **OQ1 — held required even on remove=True.** PFS4-E-amend-
   3 commits required. If a future encoding writes a
   dislodge-only effect with no authored nested Held (bare
   "drop whatever is there for (holder, prop)"), the sketch
   amends to make `held` conditionally optional (`required:
   ["kind", "holder"]` plus `if remove=false then held
   required`). Not forced today — every corpus remove=True
   carries an authored Held.
2. **OQ2 — Duplicating the via enum between held.json and
   event.json.** Today the enum lives only in held.json
   (event.json's KnowledgeEffect sub-schema no longer carries
   it directly). If a future schema needs the via enum
   independently (a Description.kind="reader-update" reference?
   a verifier rule input schema?), a shared `$defs` file or
   an in-held.json re-export becomes worth it. For now, the
   single location is clean.
3. **OQ3 — KnowledgeState schema.** A per-agent-per-τ_s
   state is a natural follow-on schema — `{agent_id,
   by_prop: [Held, ...]}`. No current consumer; deferred.
4. **OQ4 — Python agent_id → holder rename.** The Python
   prototype still uses `agent_id` on KnowledgeEffect. The
   dump translates; the schema uses `holder`. A future Python
   refactor aligns the names; this sketch does not force it.

## Acceptance criteria

Labels **P4A** (Production Sketch-4 Acceptance).

- **[P4A1]** `schema/held.json` per the inline spec.
  Metaschema-valid under Draft202012Validator. Cross-file
  `$ref` to `schema/prop.json` resolved by the test-layer
  registry.
- **[P4A2]** `schema/event.json` amended per the inline
  KnowledgeEffect spec. Metaschema-valid. Cross-file `$ref`
  to `schema/held.json` resolved.
- **[P4A3]** Conformance test extended:
  - new metaschema test for held.json;
  - new corpus conformance test for every Held nested
    inside corpus KnowledgeEffects;
  - re-validation of corpus Events under the amended
    KnowledgeEffect shape.
- **[P4A4]** `_dump_knowledge_effect` rewritten to emit
  `{kind, holder, held, remove?}`; `_dump_held` added
  emitting the five-field shape.
- **[P4A5]** `test_knowledge_effect_remove_audit` docstring
  updated per PFS4-D3. Test behavior (count + print,
  no assertion) unchanged.
- **[P4A6]** All conformance checks pass, OR each failure
  has a §Conformance dispositions entry with explicit
  resolution path.
- **[P4A7]** No change to any Python source outside
  `prototype/tests/`. In particular, `story_engine/core/
  substrate.py`, `story_engine/encodings/*.py` unchanged.
- **[P4A8]** Existing test suite continues to pass (703
  tests post-sketch-03; +~4–6 new tests expected —
  metaschema + shape spot-check + corpus conformance +
  re-export-aware Held count validation).

## Summary

Fourth production sketch; ships `schema/held.json` and amends
`schema/event.json`'s KnowledgeEffect sub-schema to consume
Held by `$ref` and admit `remove`.

- Held is five fields (prop, slot, confidence, via,
  provenance); slot + confidence + via are closed-enum
  strings; prop is `$ref`'d; provenance is a free-form
  string array.
- Event's KnowledgeEffect shape becomes `(kind, holder,
  held, remove?)` — materializing the ES3-amendment
  substrate-held-record-sketch-01 committed.
- Sketch-03's two KnowledgeEffect-related dispositions
  retire (shape translation becomes a field rename;
  remove is no longer Python-over-specification).
- Dump-layer gains `_dump_held`; `_dump_knowledge_effect`
  rewritten to match.
- Corpus validation expected clean; 4 anticipated
  mechanical-conversion dispositions are each trivial.

After this sketch's implementation, the substrate schema
layer is **complete plus Held**: Entity + Description + Prop
+ Event + Held + the effect sub-schemas. Five records; six
files. The fold-output cell has a language-independent spec;
any language's JSON-Schema-2020-12 validator can check both
effect-input-as-authored and (eventually) fold-output-as-
projected conformance against the substrate's authoritative
shapes.

Next arcs (user-choice):

- Continue building out substrate records — Branch record
  is already design-specified in sketch-04 §Branch
  representation; a slim production sketch would land it.
- Start dialect schemas (Aristotelian is smallest —
  ArMythos + ArPhase + ArCharacter + ArObservation + the
  three probe-surface records).
- Cross-boundary records (Lowering, VerificationReview, etc.).
- State-of-play-07 closing the arc.
