# State of play — sketch 06

**Status:** superseded by [state-of-play-07](state-of-play-07.md)
**Date:** 2026-04-19
**Supersedes:** [state-of-play-05](state-of-play-05.md)

Cold-start orientation doc, rewritten (not amended) at the close
of the production-arc that landed the substrate schema layer.
**Eight commits since state-of-play-05** — all production-track
work, opening and then closing the research-to-production
question sketch-05 left pending.

- `1e81b69` — production-format-sketch-01 design; PFS1 + PFS2
  methodology; schemas as canonical spec.
- `256b7a8` — production-format-sketch-01 implementation;
  `schema/description.json`; PFS2 caught real drift during
  sketch-01 authoring (Entity deferred).
- `a888844` — substrate-entity-record-sketch-01 +
  production-format-sketch-02 design.
- `fbda655` — production-format-sketch-02 implementation;
  `schema/entity.json`; 377/377 clean corpus conformance.
- `3930995` — substrate-effect-shape-sketch-01 design;
  WorldEffect + KnowledgeEffect; closed 11-operator via
  vocabulary.
- `4caf0eb` — substrate-prop-literal-sketch-01 design; Prop
  shape; args admit {str, int, float, bool}.
- `f03a605` — production-format-sketch-03 design; Prop + Event
  paired.
- `de3f899` — production-format-sketch-03 implementation;
  `schema/prop.json` + `schema/event.json`;
  `schema/description.json` updated (PropPlaceholder resolved);
  458/458 clean event conformance.

**Headline:** the substrate schema layer is complete. Every
substrate record named in substrate-sketch-05 has a canonical
JSON Schema. The Python prototype is now, in a precise sense,
disposable — the schemas are the spec; the Python is one
implementation of the spec. Any language with a JSON Schema
2020-12 validator can read the `schema/` tree and validate a
story's substrate against it.

**Research-to-production question, sketch-05's open thread:
resolved** — for this arc, in the production direction. The
balance shifted: two prior arcs were research; this arc was
pure production. The research track is still warm (new items
banked during production); a future arc will return to it.

Re-write this sketch (don't amend — write sketch-07) at the
next milestone.

---

## What is built — delta from sketch-05

### The schema layer (new top-level directory)

**New at repo root:** `schema/`. Language-independent canonical
specs. No Python, no binary artifacts.

- `schema/README.md` — names the PFS1 + PFS2 discipline.
- `schema/entity.json` — Entity (id, name, kind-enum).
- `schema/description.json` — Description (tagged-union
  attached_to; 6-kind enum; 3-attention enum; ReviewEntry
  sub-schema). Consumes `schema/prop.json` via `$ref` for
  PropositionAnchor variant.
- `schema/prop.json` — Prop (predicate, args of {str, int,
  number, bool} primitives).
- `schema/event.json` — Event (six required + three optional
  fields; WorldEffect + KnowledgeEffect as inline `$defs`
  with `kind` discriminator; Prop via cross-file `$ref`).

Four records; five files; cross-file `$ref` resolution via
`jsonschema.referencing.Registry`.

### The design sketches (four new, behind the schemas)

All design-sketch-first per the PFS2 derivation discipline:

- `design/substrate-entity-record-sketch-01.md` — Entity's
  field-level spec (SE1–SE6). Closes a gap substrate-sketch-05
  §Entities left: the sketch was ontological only ("Agent is
  a subtype of Entity"), never record-shape-specific.
- `design/substrate-effect-shape-sketch-01.md` — WorldEffect
  (prop + asserts) + KnowledgeEffect (holder + prop + via).
  11-value closed via-operator vocabulary from substrate-
  sketch-04 §Update operators: 6 diegetic + 5 narrative.
- `design/substrate-prop-literal-sketch-01.md` — Prop's
  field-level spec (PL1–PL7). Two fields; atomic primitives
  only; structurally hashable.
- `design/production-format-sketch-01.md` → `02.md` → `03.md`
  — the production layer's sketch sequence. Each shipped
  under PFS1 + PFS2 methodology.

### The conformance test (one module, extends across records)

`prototype/tests/test_production_format_sketch_01_conformance.py`
— the module name kept stable; sketch-02 + sketch-03 extended
rather than adding new modules. At sketch-06:

- **19 tests** covering metaschema validity, schema-shape
  spot-checks, corpus conformance (Entity + Description +
  Event), cross-file `$ref` registry setup, effect-kind
  discriminator dump logic, KnowledgeEffect.remove=True audit,
  dispositions-documented-in-sketch meta-checks.
- `referencing.Registry` pattern established; extends naturally
  to future cross-file refs (dialect → substrate, cross-
  boundary records → dialect).
- **First consumer** of the schemas outside Python — proves
  the schema/ tree is a real spec, not just documentation.

### The dialect + probe work (unchanged from sketch-05)

All four upper dialects unchanged. The Aristotelian probe
client (`core/aristotelian_reader_model_client.py`) unchanged;
the two Aristotelian probe JSONs unchanged. 703 standard tests
(was 695 pre-arc; +8 new conformance tests — metaschema Prop +
Event + cross-file registry + schema shape × 3 + corpus event
validation + KnowledgeEffect.remove audit).

### Substrate and dialect records are untouched

**The entire production arc — 8 commits — made zero
modifications to any file under `prototype/story_engine/`.**
The Python dataclasses for Entity, Description, Prop, Event,
WorldEffect, KnowledgeEffect, ArMythos, Throughline, Lowering,
VerificationReview, etc. are exactly as they were at
state-of-play-05. The production work is disjoint from the
Python — which is the whole point of the PFS2 discipline.

---

## Shift-point — further clarification

State-of-play-05 refined the shift-point reading into two
axes: architectural-stability (can the dialect stack be
written without substrate pressure?) and behavioral-stability
(does the dialect hold up when read?). Both were GREEN at
sketch-05.

State-of-play-06 adds a third axis: **spec-portability**. *Can
the Python be thrown away and the substrate still be usable?*

Before this arc: no. The Python dataclasses were the spec. A
port would have been an archaeological dig — read the Python,
infer the intended shape, reimplement in the target language,
pray nothing was lost.

After this arc, for the substrate layer: **yes**. A port reads
`schema/*.json` and the design sketches, implements conforming
record types in the target language, and validates against the
same tests. The Python is *one* conformant implementation; a
Rust or TypeScript port is another. Spec-portability is GREEN
for the substrate.

Dialect layer is still Python-only for spec; dialect records
do not yet have schemas. That work is ahead.

**What this unlocks.** The roadmap's item #4 (port) is no
longer gated on "figure out what the spec is." It is gated on
"write dialect schemas" and "translate the engine / verifier
machinery." The first is production-track work; the second
can proceed incrementally (port one dialect at a time). Neither
is an archaeological dig.

---

## What the production arc revealed

### PFS2 catches real drift — twice

The production-arc's methodological lever (PFS2: derive from
design sketches, never from Python) produced two real
sketch-amendment events during implementation:

- **sketch-01 Entity scope narrowing.** The sketch committed
  PFS3 Entity schema ("fields derived from the sketch") before
  implementation. Implementation-pass re-read caught that
  substrate-sketch-05 §Entities is ontological-only — no
  `name`, no `kind` enum at the design level. The sketch
  amended: Entity moved from "shipping in sketch-01" to
  "deferred pending substrate-entity-record-sketch-01". The
  discipline produced real scope-narrowing pressure.
- **sketch-03 oneOf-vs-anyOf.** The initial prop.json used
  `oneOf` over {string, integer, number, boolean}. Integer
  values validate against both `integer` AND `number` in JSON
  Schema; `oneOf` fails on exact-one matching; Rocky's
  `fought_rounds(rocky, apollo, 15)` was the forcing instance.
  Amended to `anyOf`. A schema-authoring discipline finding
  the implementation pass surfaced; both the sketch's inline
  schema and the schema file carry the fix.

Neither finding would have been caught without the discipline
of implementing-against-corpus. Both are informative.

### Conformance dispositions across three records

| Record | Dispositions surfaced |
|---|---|
| Description (33 records) | 2 sketch-incompletenesses: `authoring-note` kind + `superseded` status, both in use but absent from descriptions-sketch-01's vocabulary. Resolution path: amend descriptions-sketch-01. |
| Entity (105 unique; 377 with re-export inflation) | Zero. First-principles sketch SE1–SE6 landed exactly on the corpus. |
| Event (102 unique; 458 with re-export inflation) | Three: KnowledgeEffect shape translation (mechanical; dump-layer bridges), remove=True audit (7 cases of pre-identity-and-realization-sketch-01 pattern), metadata (sketch-04-era field; 0/102 populated). |

Entity's zero-disposition result is informative: small records
written first-principles land clean. Description's two
dispositions were incompletenesses in the source design
sketch; resolution is sketch-amendment, not schema-widening.
Event's three dispositions expose a richer history — the
Python's `KnowledgeEffect(agent_id, held, remove)` shape
predates substrate-effect-shape-sketch-01's committed shape
and identity-and-realization-sketch-01's realization-should-
not-remove-propositions discipline. Both are **research-track
items that production-track work surfaced**.

### The Python prototype has real drift from the sketches

Production-arc-surfaced Python over-specifications (each is a
cleanup target for a future research-track commit, or can
simply remain as-is since the conformance test routes around):

- `KnowledgeEffect.remove` — the pre-sketch retraction bool.
  7 instances in Oedipus. Refactor per identity-and-
  realization-sketch-01 recommended pattern.
- `KnowledgeEffect.held` carrying fold-output fields (slot,
  confidence, provenance) inline with the effect. Refactor
  splits Held (fold-output) from KnowledgeEffect (effect-input).
- `Event.metadata` — sketch-04-era field; 0/102 populated;
  harmless but cruft.
- `Description.status == "superseded"` — used in corpus but
  not in descriptions-sketch-01.
- `Description.kind == "authoring-note"` — used in corpus but
  not in descriptions-sketch-01's kind vocabulary.

Five Python-over-specification findings. None block further
work; each is a candidate focused cleanup arc.

---

## What's next (research AND production)

### Research track

Accumulated across arcs; re-ordered by this arc's impact:

1. **Probe-surfaced encoding cleanups** (sketch-04 → sketch-05
   holdover). 2 Oedipus prose fixes + 5 Rashomon phase-
   annotation cleanups from the Aristotelian probe arc. All
   grounded; no dialect change needed. Smallest concrete
   research item.
2. **KnowledgeEffect.remove refactor.** The 7 remove=True
   cases this arc's audit surfaced. Rewrite Oedipus's
   realization events per identity-and-realization-sketch-01
   §Prior encoding's workaround, and its retirement. Small
   scope; directly testable (the audit's baseline drops to 0).
3. **Descriptions-sketch-01 amendment** — add `authoring-note`
   to §Kinds and `superseded` to §Optional fields, clearing
   sketch-01's two conformance dispositions.
4. **Close one banked scheduling-act-family seed** (sketch-05
   holdover). OQ2-reshaped (wife prose-carried drivers) or
   OQ1-reshaped (woodcutter cross-branch signature) or
   bandit-refinement.
5. **Aristotelian-sketch-02 candidate.** 5 relation-extension
   proposals (ArMythosRelation + ArFrameMythos +
   ArAnagnorisisLevel + ArAnagnorisisChain +
   ArPeripeteiaAnagnorisisBinding) banked from the probe arc.
   Evaluate under EP-style forcing-function criteria; decide
   which earn inclusion.
6. **A seventh Aristotelian encoding** (Macbeth or Ackroyd) —
   provides the second-encoding pressure several banked
   dispositions + relation proposals need.
7. ***And Then There Were None* content fill.** Large task.
   Would pressure several banked items (quantified
   propositions via OQ4 of prop-sketch; ArMythosRelation if
   ten deaths are linked mythoi; MN2 concealment-asymmetry).

### Production track

The substrate schema layer just landed; the dialect schemas
are the next large surface.

A. **Dialect schemas.** Each dialect (Dramatic, Dramatica-
   complete, Save-the-Cat, Aristotelian) has ~5–15 record
   types. Each needs a production-format sketch of its own.
   Candidate first: Aristotelian — it is the smallest dialect
   (ArMythos, ArPhase, ArCharacter, ArObservation, + the three
   probe-surface records from aristotelian-probe-sketch-01;
   total 7 records) and is the dialect most recently-specified
   design-side (aristotelian-sketch-01 is field-level-detailed
   by construction).
B. **Held record schema.** The fold-output record mentioned in
   effect-shape-sketch-01 + identity-and-realization-sketch-
   01 but never shape-specified. Needs a design sketch first
   (candidate: `substrate-held-record-sketch-01`), then a
   production sketch. Would pressure the KnowledgeEffect
   refactor (item 2 above) to happen at the same time.
C. **Branch record schema.** Substrate-sketch-04 §Branch
   representation specifies the Branch record fields (label,
   kind, parent, metadata) at the design level. A slim
   production sketch suffices — most of the design-work is
   already done.
D. **Cross-boundary record schemas.** Lowering,
   VerificationReview, StructuralAdvisory, VerifierCommentary,
   ArAnnotationReview, ArObservationCommentary, DialectReading.
   Multiple sketches; substantial arc.
E. **Port work** (roadmap item 4). No longer gated on spec
   portability (substrate is done). Gated on dialect schemas
   (A) + engine-translation effort (TBD). A future state-of-
   play may revisit the gating.
F. **Markdown-fenced author parser** (roadmap item 1). Consumer
   of the schemas — parser produces JSON conforming to
   `schema/*.json`. Unblocked by the substrate schema layer;
   natural next-production-arc candidate.
G. **Prose export round-trip starter** (roadmap item 3). Less
   dependent on schemas; more dependent on reader-model probe
   infrastructure.
H. **Goodreads import prototype** (roadmap item 2). Same.

### Recommendation

This arc's scale was large (8 commits, 4 design sketches, 3
production sketches, 4 schema files). A shorter next arc
— closing research-track item #1 (probe findings) or item #2
(remove=True refactor) — would rebalance. Both are small,
grounded, and produce measurable effect (probe-findings close;
audit-baseline drops).

Alternatively: **production item (F)** — the markdown parser
— is newly compelling. Until the substrate schema layer
landed, the parser had no canonical target; now it does. Would
be the first consumer of the schemas *outside* the conformance
test.

sketch-05's standing "do one of each" recommendation survives:
research-track #1 or #2 plus production-track (F) would be the
pair that best demonstrates the schemas are a real spec.

---

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketch-04 + sketch-05. Validated again
across 8 commits:

- **Sketches before implementation.** Every sketch this arc
  landed design-first then implementation-second (same rhythm
  as the probe arc's `3f13af1` → `e6a89c7` → `6d70199`
  sequence). The rhythm:
  - production-format-sketch-01: design (`1e81b69`) → impl
    (`256b7a8`).
  - substrate-entity-record + production-format-sketch-02:
    design (`a888844`) → impl (`fbda655`).
  - substrate-effect-shape (design only): `3930995`.
  - substrate-prop-literal (design only): `4caf0eb`.
  - production-format-sketch-03: design (`f03a605`) → impl
    (`de3f899`).
- **First-principles design derivation.** The substrate-level
  design sketches (entity-record, effect-shape, prop-literal)
  derive from substrate-sketch-05 / sketch-04 / identity-and-
  realization-sketch-01 — never from the Python. Commits are
  explicit about this.
- **Conformance dispositions, not silent schema-widening.**
  Every sketch-amendment during implementation is recorded
  in the sketch's §Conformance dispositions section. PFS2
  says resolve discrepancies through sketch amendment, not
  schema stretching.
- **State-of-play at milestone boundaries.** This doc.
- **Commit messages are cross-session artifacts.** The 8
  production commits average ~45-line bodies (dense); a
  cold-start Claude reading `git log --oneline -15` can
  reconstruct the production arc fully.
- **Prefer Grep / Read-slice over full Read.** Large sketches
  now exist; random-access reading keeps context economical.
- **Spawn Explore agents aggressively** for 3+-query research.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic.
2. This doc (`design/state-of-play-06.md`) — current corpus,
   shift-point state, research + production tracks.
3. `schema/README.md` — the production layer's discipline.
4. `articles/2026-04-18-timelock-or-optionlock.md` — the paper.
5. `git log --oneline -30` — recent commits; the 8 production-
   arc commits carry dense, readable bodies.
6. `design/production-format-sketch-01.md` §PFS2 catches real
   drift during sketch-01 authoring — the methodological
   lever explained with its first catch.
7. `design/substrate-effect-shape-sketch-01.md` — the design
   sketch with the richest first-principles derivation
   (fold-structure-justified asymmetry between WorldEffect
   and KnowledgeEffect).
8. The two most-recent probe JSONs
   (`reader_model_oedipus_aristotelian_output.json`,
   `reader_model_rashomon_aristotelian_output.json`) — first
   Aristotelian probe output; relation-extension proposals
   live here verbatim.
