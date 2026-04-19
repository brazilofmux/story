# State of play — sketch 09

**Status:** active
**Date:** 2026-04-19
**Supersedes:** [state-of-play-08](state-of-play-08.md)

Cold-start orientation doc, rewritten (not amended) at the
milestone where the **substrate layer reaches behavioral
completeness** and the **dialect schema layer begins**.

**Three commits since state-of-play-08** — two arcs, both
landing the same day (2026-04-19, continuing sketch-08's
one-day cadence). The first was a design-only consolidation
sketch closing five banked fold-mechanics open questions; the
second was the first dialect-layer production arc, shipping
three Aristotelian core-record schemas under a new
`schema/aristotelian/` namespace.

- `2206e10` — substrate-knowledge-fold-sketch-01 (design-only,
  single commit). KF1–KF5 close / sharpen / derive five
  banked OQs (held-sketch OQ5 / OQ6 / OQ7; substrate-04 OQ13;
  substrate-04 OQ14). Eight OQs banked forward with forcing
  functions. 676-line sketch; no schema deliverable; no
  Python change.
- `7a86b15` — production-format-sketch-06 (design). Slim
  production sketch for Aristotelian dialect core. PFS6-N1
  (schema namespace convention), PFS6-P1..P5 (ArPhase shape),
  PFS6-C1..C5 (ArCharacter shape), PFS6-M1..M11 (ArMythos
  shape + complex-plot conditional), PFS6-X1 (cross-file $ref
  extends to dialect layer), PFS6-X2 (no event-id $ref),
  PFS6-D1..D5 (dump-layer + registry registration). Five OQs
  banked. No design derivation (aristotelian-sketch-01 had
  already committed the field-level shapes).
- `2ab0355` — production-format-sketch-06 (implementation).
  Three JSON Schema files under `schema/aristotelian/`;
  conformance test +9 tests (3 metaschema + 3 shape +
  3 corpus); `schema/README.md` restructured into substrate +
  dialect subsections. Corpus validates 5 ArMythos +
  15 ArPhase + 6 ArCharacter records clean.

**Headline.** Two simultaneous completeness claims.

1. **The substrate layer reaches behavioral spec completeness.**
   State-of-play-08 declared substrate structural completeness
   — six JSON Schema files covering every substrate record
   type. Sketch-09's fold consolidation adds the *behavioral*
   layer: KF1–KF5 commit the fold's semantics (conflict
   resolution, `remove` scope, permanent-split reconvergence,
   event-level draft supersession) + sharpen the `via=
   "forgetting"` label. A port targeting substrate can now
   read the schemas + named sketches and have both *structural*
   and *behavioral* fidelity spec — no Python reads required.

2. **The dialect schema layer begins.** First production arc
   above the substrate shipped three Aristotelian core-record
   schemas. The `schema/<dialect>/` subdirectory convention
   is committed as PFS6-N1 — precedent for every future
   dialect-schema arc. Cross-file `$ref` pattern extended
   from substrate-layer usage (event→prop, held→prop,
   description→prop) to dialect-layer intra-dialect use
   (mythos→phase, mythos→character). The Python prototype
   remains unchanged across the two arcs — fourteen+
   consecutive production-track commits without a line of
   change under `prototype/story_engine/`.

Re-write this sketch (don't amend — write sketch-10) at the
next milestone.

---

## What is built — delta from sketch-08

### The schema layer (one new subdirectory, three new schemas, README restructure)

- `schema/aristotelian/phase.json` (new, 34 lines) — ArPhase
  record per aristotelian-sketch-01 A2. Required id / role /
  scope_event_ids; role closed enum at {beginning, middle,
  end}; scope_event_ids plain-string array per PFS6-X2;
  annotation optional.
- `schema/aristotelian/character.json` (new, 37 lines) —
  ArCharacter record per aristotelian-sketch-01 A5. Required
  id / name; optional character_ref_id (plain-string cross-
  dialect hook); optional hamartia_text, is_tragic_hero.
- `schema/aristotelian/mythos.json` (new, 101 lines) — ArMythos
  primary record per aristotelian-sketch-01 A1. Six required
  fields; plot_kind closed enum at {simple, complex}; phases
  non-empty via `$ref` to phase.json; optional characters via
  `$ref` to character.json; four optional event-id pointer
  fields (complication / denouement / peripeteia /
  anagnorisis); three boolean unity assertions + bounds;
  aims_at_catharsis. Complex-plot conditional via allOf/
  if-then-else-anyOf — first occurrence of the anyOf-in-then
  pattern, extending PFS5-B5's if-then-else shape.
- `schema/README.md` — restructured into `Substrate layer
  (structurally complete, six records)` + `Dialect layer
  (Aristotelian, three core records)` subsections; cross-file
  reference narrative extended to cover mythos's two outbound
  $refs; deferred list updated to no longer name Aristotelian-
  core among the deferred (ArObservation + cross-boundary
  Aristotelian records explicitly deferred to Production C).

**No substrate schema file changes.** The six substrate
schemas are unchanged; substrate layer remains structurally
complete.

### The design sketches (two new)

- `design/substrate-knowledge-fold-sketch-01.md` (new,
  676 lines). Consolidation sketch closing five banked fold-
  mechanics OQs: held-sketch OQ5 (conflict resolution), OQ6
  (remove across branches), OQ7 (forgetting); substrate-04
  OQ13 (reconvergence), OQ14 (draft supersession). Five
  commitments (KF1–KF5) + eight banked OQs (OQ-KF1..OQ-KF8)
  with forcing-function criteria. First design-only
  consolidation sketch under the PFS2 discipline — no schema,
  no Python; lifts docstring claims (e.g., `scope` function's
  "τ_a tiebreaker is load-bearing" text) to design-level
  commitments.
- `design/production-format-sketch-06.md` (new, 540 lines).
  First dialect-layer production sketch. Slim format-rendering
  arc — aristotelian-sketch-01 A1/A2/A5 had already committed
  the three record shapes. Eleven record commitments
  (PFS6-P1..P5, C1..C5, M1..M11), two cross-commitments
  (PFS6-N1 namespace, PFS6-X1 cross-file $ref), two posture
  commitments (PFS6-X2 plain-string event refs), five
  dump/discovery commitments (PFS6-D1..D5). Five OQs banked:
  ArObservation + cross-boundary records (OQ1), next-dialect
  schemas (OQ2), event-id audit (OQ3), character-ref-id audit
  (OQ4), sketch-02 extensions (OQ5).
- `design/README.md` — new entry in Per-topic active-sketches
  section for substrate-knowledge-fold-sketch-01, adjacent to
  substrate-sketch-05. Entry summarizes KF1–KF5 commitments +
  the eight banked OQs.

### The conformance test (nine new tests, one registry extension)

`prototype/tests/test_production_format_sketch_01_conformance.py`:

- `_load_aristotelian_phase_schema`,
  `_load_aristotelian_character_schema`,
  `_load_aristotelian_mythos_schema` added — three loaders
  walking the new `schema/aristotelian/` subdir.
- `_build_schema_registry` extended to register the three
  new schemas per PFS6-D5 (mythos.json's `$refs` resolve
  against sibling phase.json + character.json).
- `_discover_encoding_aristotelian_records` added per PFS6-D4
  — walks `AR_*` module attributes matching `ArMythos`
  singletons or tuples; dedupes mythoi by id within each
  encoding (Rashomon exports both four mythos singletons AND
  a tuple containing them; id-dedup collapses the collision).
  Returns triple `(mythoi, phases, characters)` — phases and
  characters reached by traversal of each mythos's `.phases`
  / `.characters` tuples with id-dedup within an encoding.
- `_dump_armythos`, `_dump_arphase`, `_dump_archaracter` added
  per PFS6-D1..D3 — field-for-field isomorphic dumps; optional
  None-valued fields omitted; dataclass-default-True /
  dataclass-default-False booleans always emitted.
- `test_aristotelian_{phase,character,mythos}_schema_
  metaschema_valid` (new × 3).
- `test_aristotelian_{phase,character,mythos}_schema_has_
  expected_shape` (new × 3) — verifies $id, title, required
  set, `additionalProperties: false`, all declared properties,
  closed-enum values, the cross-file `$ref` URIs in
  mythos.json's phases/characters arrays, and the allOf/
  if-then-else-anyOf complex-plot clause.
- `test_aristotelian_{phase,character,mythos}_corpus_
  conformance` (new × 3). Mythos corpus test uses registry-
  bound validator; the other two use plain validators.

### Corpus validation outcomes

- **Aristotelian dialect corpus (new):**
  - ArMythos: 5 records (1 Oedipus + 4 Rashomon). Plot-kind
    breakdown: 5 complex, 0 simple (no simple-plot encoding
    today; simple-plot admitted by the schema but unexercised).
  - ArPhase: 15 records. Role breakdown: 5 beginning / 5
    middle / 5 end (3 phases × 5 mythoi per A2).
  - ArCharacter: 6 records. 5 tragic-hero-flagged (Oedipus,
    and each of the four Rashomon testifiers-as-protagonist);
    1 non-tragic-hero (Jocasta). All 6 carry a
    character_ref_id into substrate entities.
- **Substrate corpus (unchanged from sketch-08):**
  - Description: 33 clean.
  - Branch: 25 clean (17 canonical + 8 contested).
  - Held: 199 clean.
  - Event: 458 clean.
  - Entity: 377 clean.
  - Remove-audit: 7 (baseline unchanged).
- **Full test suite: 717 passing** (+9 from the 708 baseline:
  3 metaschema + 3 shape + 3 corpus, all Aristotelian).

Three anticipated non-findings materialized as predicted in
PFS6 §Conformance dispositions, none escalating to a true
disposition:

1. `annotation=""` Python default validates clean (string
   type accepts empty string).
2. `unity_of_time_bound` / `unity_of_place_max_locations` /
   `aims_at_catharsis` always present in the dump because the
   dataclass always carries defaults; schema admits
   unconditionally; verifier reads conditionally.
3. Rashomon's ArCharacter records are mythos-local; schema
   validates each independently. No shared-character dedup at
   the schema layer.

### Python unchanged

**Zero lines modified under `prototype/story_engine/` across
all three sketch-09 commits.** The Python ArMythos / ArPhase /
ArCharacter dataclasses were already PFS6-correct; only the
dump-layer + discovery + test code had to be written (all
under `prototype/tests/`). Similarly the fold-sketch commit
touched no code — the Python substrate.py's `scope` /
`project_knowledge` / `in_scope` already matched KF1 / KF3 /
KF4 at the docstring level; sketch-09 lifted the docstring
claims to design-level commitments without asking Python to
change.

**Python-as-sneaky** (sketch-06's phrase, retained through
-07 / -08 / -09) held in both arcs:

- The Python fold already implemented the (τ_s, τ_a) tie-
  breaker as "load-bearing" per the `scope` function's own
  docstring; the fold sketch recognized the pattern and named
  it as KF1.
- `in_scope`'s docstring already said "Draft supersession …
  not yet implemented. When the prototype gains those, this
  function gains an exclusion check against branch-specific
  supersession/removal metadata." The fold sketch specified
  the exclusion-check mechanism (KF5: read
  `Branch.metadata["supersedes"]`); a future Python change
  will wire it without changing the fold's semantic
  contract.
- ArMythos / ArPhase / ArCharacter already matched their
  respective A1 / A2 / A5 commitments in aristotelian-
  sketch-01; PFS6 format-rendered them with no design
  translation, no semantic gap.

The discipline extends: **the schema does not depend on the
Python; the Python depends on the schema.** Now applied across
two layers (substrate + first dialect) with the same
consistency.

---

## Shift-point — dialect schema layer begins + substrate behavioral spec complete

Sketch-08 declared substrate structural completeness ("every
substrate record a port would need to emit or consume has a
matching JSON Schema file"). Sketch-09 adds two independent
claims:

### Substrate behavioral spec is complete

Where sketch-08 declared "structural spec" complete, sketch-09
extends the completeness claim to **behavioral spec**. A port
that reads:

- `schema/*.json` (six substrate record schemas) — structural.
- `design/substrate-knowledge-fold-sketch-01.md` — fold
  mechanics (KF1 conflict resolution, KF2 `via="forgetting"`
  semantics, KF3 `remove` scope, KF4 reconvergence default,
  KF5 draft-supersession default).
- `design/substrate-sketch-04.md` — branch semantics, fold
  scope rule, enforcement per branch.
- `design/substrate-sketch-05.md` — K1 / W1 / A3 frames.
- `design/substrate-effect-shape-sketch-01.md` (as amended by
  held-sketch) — effect semantics.
- `design/descriptions-sketch-01.md` (as amended 2026-04-19)
  — the interpretive-peer surface.
- `design/substrate-prop-literal-sketch-01.md` — Prop atomic.
- `design/substrate-entity-record-sketch-01.md` — Entity.
- `design/substrate-held-record-sketch-01.md` — Held.

— has **complete structural AND behavioral spec** for the K1
substrate. That's the substrate-layer port-readiness claim at
its strongest form the repo can produce.

**What's still under-specified at the substrate layer.**
W1 (world-projection fold) and K2 (reader projection). W1 is
parallel to K1 but has its own analogous OQs (what does `remove`
mean for world facts? how do multi-assertion / retraction
compositions resolve?); K2 composes K1 + focalization + sjuzhet
order per focalization-sketch-01 F1–F6. Neither has an
equivalent consolidation sketch today; `substrate-world-fold-
sketch-01` and `substrate-reader-fold-sketch-01` would be the
candidates if forcing functions surface.

### Dialect schema layer has begun

Sketch-08's dialect-schema work was on the "next-up-the-stack"
list; sketch-09 moves it to the "partially shipped" list.
Concretely:

- **Three Aristotelian core records ship as schema files.**
  ArObservation (dialect-internal verifier output) and three
  Aristotelian cross-boundary records (ArAnnotationReview,
  ArObservationCommentary, DialectReading) still deferred to
  Production C.
- **Namespace convention is committed.** `schema/<dialect>/`
  subdir per PFS6-N1. Next dialect ships at
  `schema/save_the_cat/` or `schema/dramatic/` by the same
  precedent.
- **Cross-file `$ref` extends across dialect boundaries.**
  Mythos's `phases` and `characters` arrays reference
  sibling-dialect-schema files; same
  `jsonschema.referencing.Registry` pattern that has carried
  substrate-layer refs since PFS3-E1.
- **Complex-plot conditional is first allOf/if-then-else
  with anyOf-in-then.** Extends PFS5-B5's conditional
  pattern to conditions that require "at-least-one-of-N-fields"
  rather than "exactly-one-field-or-none." Future dialect or
  cross-boundary schemas with similar conditionals have
  precedent.

**Dialect layer roadmap.** Three remaining dialects:

- **Save-the-Cat** — two sketches (save-the-cat-sketch-01 +
  sketch-02). Field-level-detailed; no outstanding design
  forcing functions. Candidate for production-format-sketch-
  07 following the PFS6 pattern directly.
- **Dramatic** — one sketch (dramatic-sketch-01). Has open
  design forcing functions (dramatica-template-sketch-01's
  "Where the dialect resists" lists six). A dramatic-sketch-
  02 design-first arc may be needed before a production-
  format-sketch for Dramatic can ship cleanly.
- **Dramatica-complete** — one sketch (dramatica-template-
  sketch-01). Extends Dramatic as a Template; gated on
  Dramatic-schema readiness.

**Cross-boundary schema work stays in Production C.** Lowering,
VerificationReview, StructuralAdvisory, VerifierCommentary,
plus Aristotelian and future-dialect-specific cross-boundary
records (ArObservation, ArAnnotationReview, etc.; StcObservation
already extant). Multiple sketches; substantial arc.

---

## What the two sketch-09 arcs revealed

### Design-only consolidation sketches earn their shape

Substrate-knowledge-fold-sketch-01 was the first **pure design
consolidation** sketch in the design corpus — no schema, no
code, no new record shape, no amendment-to-prior-sketch. Purpose
was entirely "close banked OQs by naming the semantics the
Python already implements and the corpus hasn't contradicted."

The discipline that emerged:

- **Lift prototype docstring claims to design-level
  commitments.** `substrate.py`'s `scope` docstring already
  carried "the τ_a tiebreaker is load-bearing." Sketch-09
  made this a sketch commitment (KF1). The commit message
  explicitly named this path: "this sketch lifts that local
  docstring claim to a design-level commitment."
- **Commit / sharpen / derive as three separable postures.**
  KF1 commits (later-wins as the fold rule). KF2 sharpens
  (forgetting as authorial label, not fold operator; stays
  banked on mechanism). KF3 derives (remove-across-branches
  falls out of B1 + SH8). KF4 and KF5 commit prototype
  defaults (permanent-split; event-level supersession) while
  explicitly banking the alternatives.
- **Bank with forcing-function criteria, not "TBD."** Each
  banked OQ (OQ-KF1 through OQ-KF8) names a concrete forcing
  function — "encoding with genuinely-contested middle and
  genuinely-single-valued end," "very-long-fabula encoding,"
  etc. The sketch does not say "we'll figure this out
  later"; it says "this reopens when X surfaces."

Consolidation sketches now have a template for future use:
W1, K2, performance-engineering, event-vocabulary are all
candidates for similar treatment when their banked-OQ density
reaches fold-sketch levels.

### Slim production sketches when the design is truly done

PFS6 was the second slim production sketch (after PFS5) where
no design derivation was needed. PFS5 shipped one record in
320 lines; PFS6 shipped three records in 540 lines (roughly
linear scaling — the per-record work is small when the design
sketch is field-detailed). Contrast with PFS3 (two records at
~550 lines including design derivation for Event internals)
or PFS4 (held-record derivation + conformance + KnowledgeEffect
amendment at ~550 lines).

**Slim pattern test.** PFS6's structure (Purpose → Why now →
Scope → Commitments → Anticipated non-findings → Corpus
expectations → Open questions → Discipline → Summary)
duplicates PFS5's; the governance sections stay stable; the
Commitments section scales linearly with record count.
Save-the-Cat's PFS7 (OQ2) would test this pattern — two
sketches worth of design already done, slim production sketch
should ship cleanly.

### First schema-namespacing decision

PFS6-N1 committed `schema/<dialect>/` over flat-with-prefix
(e.g., `schema/ar_phase.json`) and over no-prefix (e.g.,
`schema/phase.json`). The tradeoff came down to:

- **Namespacing.** Dialect records collide on common names
  (Character / Phase / Observation are plausible multi-dialect
  names) — flat layout would force awkward prefixes.
- **Visual separation.** `schema/` + `schema/aristotelian/`
  side-by-side makes the substrate vs. dialect layering
  obvious.
- **`$id` URI structure.** Path-mirrors-filesystem means
  ports can route by URL prefix.
- **Loader cost.** Negligible — explicit relative paths, no
  directory walk.

The conversation decision ("sounds right") landed on subdir
before drafting began. Worth naming explicitly: schema-layer
design decisions like namespace choice are **one-shot** —
once the first dialect ships under `schema/aristotelian/`,
every subsequent dialect follows. The cost of revisiting would
be real (renames across schemas, tests, READMEs, external
references); the benefit would have to be proportional. None
is in view today.

### The anyOf-in-then conditional pattern is general

PFS5-B5 shipped the first allOf/if-then-else clause at the
substrate-layer schema (Branch's kind→parent conditional:
`kind=canonical` forbids parent, all others require it).
PFS6-M6 extended the pattern: `plot_kind=complex` requires
*at least one of two fields*, via anyOf in the then-clause.

General shape: structural conditional requirements that
cannot be expressed in a flat JSON Schema's `required` array
are expressible as allOf clauses whose if-guard matches a
discriminator value and whose then-branch carries whatever
JSON Schema fragment describes the requirement. Same
Draft202012 validator handles both PFS5-B5 and PFS6-M6 shapes;
the registry is not involved (these are intra-file clauses).

Future conditional-field needs — e.g., "an Event with
`is_inference=True` requires an `inference_source_id`" if
such a shape ever surfaces — follow the same template.

### The production-track streak extends

Sketch-08 named the streak as "twelve production-track
commits … zero lines changed under `prototype/story_engine/`."
Three sketch-09 commits extend it: one design-only (fold),
one production design (PFS6), one production implementation
(PFS6 impl). None modified the Python prototype. The
continued streak is not the point itself — the point is that
the PFS2 discipline (schemas-first, Python-as-conformance-
check) is holding up across both a design-only consolidation
(sketch-04 and held-sketch's docstring claims lifted cleanly)
and a production format-rendering arc (aristotelian-sketch-
01's A1/A2/A5 format-rendered cleanly). Two qualitatively
different arc shapes; same Python-untouched outcome.

---

## What's next (research AND production)

### Research track

Unchanged from sketch-08 in list order; item completions
noted:

1. **Probe-surfaced encoding cleanups** (sketch-05 → 06 → 07
   → 08 → 09 holdover, still unopened). 2 Oedipus prose fixes
   + 5 Rashomon phase-annotation cleanups from the
   Aristotelian probe arc. Smallest concrete research item.
2. **Aristotelian-sketch-02 candidate.** 5 relation-extension
   proposals (ArMythosRelation + ArFrameMythos +
   ArAnagnorisisLevel + ArAnagnorisisChain +
   ArPeripeteiaAnagnorisisBinding) banked from the probe arc.
   Evaluate under EP-style forcing-function criteria.
3. **A seventh Aristotelian encoding** (Macbeth or Ackroyd)
   — provides the second-encoding pressure several banked
   relation proposals need.
4. ***And Then There Were None* content fill.** Large task.
   Would pressure several banked items (quantified
   propositions via OQ4 of prop-sketch; ArMythosRelation if
   ten deaths are linked mythoi; MN2 concealment-asymmetry).
5. **Close a banked scheduling-act-family seed** (OQ2-reshaped
   wife prose-carried drivers; OQ1-reshaped woodcutter
   cross-branch signature; bandit-refinement).

### Production track

Re-ordered by sketch-09's completions (items A-substrate-fold
and A-Aristotelian-core closed):

A. **Next-dialect schemas.** Two remaining dialects:
   - **Save-the-Cat (PFS7 candidate).** Field-level-detailed
     across two sketches (sketch-01 + sketch-02); no
     outstanding design forcing functions. Slim production
     sketch expected, same shape as PFS6. Corpus: Macbeth +
     Ackroyd encodings.
   - **Dramatic (PFS8 candidate, gated).** Six design
     forcing functions banked in dramatica-template-sketch-
     01's "Where the dialect resists" — Template-level
     schema extension, derived-field semantics, Story-level
     Template extensions, per-Function Throughline-assignment
     constraints, heavy Template theory-data, quad-shape
     typed validators. A dramatic-sketch-02 design-first arc
     is the prerequisite if any of the six forces a schema-
     shape decision.
B. **Substrate-world-fold-sketch-01** (parallel to fold-
   sketch-01 but for W1). Only if a forcing function surfaces
   — current corpus has no contradictory world-fact patterns
   that the fold's later-wins default doesn't handle.
C. **Cross-boundary record schemas.** Lowering,
   VerificationReview, StructuralAdvisory, VerifierCommentary,
   ArAnnotationReview, ArObservationCommentary, DialectReading,
   plus ArObservation (deferred from PFS6 per its OQ1).
   Multiple sketches; substantial arc. A single opener
   sketch that lays out the cross-boundary schema namespace
   convention (`schema/verification/` or `schema/
   cross_boundary/`, or flat-at-schema-root?) would precede
   the per-record sketches.
D. **Markdown-fenced author parser** (roadmap item 1).
   First consumer of the schemas outside the conformance
   test. Unblocked further by sketch-09 — every substrate
   + dialect-core record the parser would need to emit is
   now spec'd.
E. **Prose export round-trip starter** (roadmap item 3).
F. **Goodreads import prototype** (roadmap item 2).
G. **Port work** (roadmap item 4). Substrate-layer fully
   unblocked (structural + behavioral). Dialect-layer
   partially unblocked (Aristotelian-core spec'd; others
   still per-dialect-Python).

### Recommendation

Sketch-09's two arcs (fold consolidation + PFS6) paired a
design-heavy + an implementation-light commit, landing three
commits total. A similar small next arc keeps the cadence.
Three candidates fit the small-arc shape:

- **Research track #1** (probe-surfaced encoding cleanups).
  Holdover since sketch-05. Quick clarifying arc; smallest
  concrete research item.
- **Production track A1** (Save-the-Cat dialect schemas,
  PFS7). Extends PFS6's precedent directly; validates the
  namespace and cross-file $ref pattern on a second dialect.
  Slim production sketch expected.
- **Production track C-opener** (cross-boundary schema
  namespace sketch). Single design decision — where do
  cross-boundary records live, and under what naming — that
  unblocks a later batch of per-record arcs. Could be a
  one-commit design-only sketch.

Alternative: **Production track D** (markdown parser) — still
the newly-compelling consumer-of-schemas direction. Now has
MORE consumable records than after sketch-08: substrate six
+ Aristotelian three = nine. Might benefit from waiting until
a second dialect ships so the parser consumes two namespaces
at once; or not, depending on scope.

---

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketches-04 through -08. Validated again
across the 3 commits:

- **Orientation before commitment.** Fold sketch began with
  a read of substrate-sketch-04 §Fold scope + held-sketch
  §Fold-implementation mechanics + the Python `scope` +
  `project_knowledge` + `in_scope` functions. PFS6 began
  with a read of aristotelian-sketch-01 A1–A9 + both
  Aristotelian encodings (oedipus / rashomon) + the existing
  `schema/branch.json` as template. Both arcs confirmed
  scope via conversation ("3 records vs 4 vs 7 — going with
  3," "schema/aristotelian/ subdir — sounds right") before
  drafting began.
- **Sketches before implementation.** Same rhythm as prior
  arcs. Fold sketch shipped alone (no implementation); PFS6
  shipped as design+impl pair.
- **First-principles vs. retroactive recognition.** Fold
  sketch was *entirely* retroactive — five OQs the prior
  sketches banked; KF1–KF5 recognize patterns the Python
  and prior sketches already established. PFS6 was primarily
  format-rendering (retroactive on A1/A2/A5) + small number
  of first-principles schema-layer choices (namespace,
  anyOf-in-then conditional, $ref pattern extension).
- **Banking with forcing-function criteria.** Both arcs
  produced banked OQs; each OQ carries a named forcing
  function (not "TBD"). Fold sketch: 8 OQs. PFS6: 5 OQs.
  The discipline now covers 40+ banked OQs across the
  design corpus.
- **State-of-play at milestone boundaries.** This doc.
  Milestone: substrate behavioral spec complete + dialect
  schema layer begins.
- **Commit messages as cross-session artifacts.** Three
  sketch-09 commits carry 60–110 line bodies; a cold-start
  Claude reading `git log --oneline -8` can reconstruct
  sketch-09's arcs fully from commit bodies.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic (now
   includes substrate-knowledge-fold-sketch-01).
2. This doc (`design/state-of-play-09.md`) — current corpus,
   shift-point state, research + production tracks.
3. `schema/README.md` — the production layer's discipline,
   now structured in substrate + dialect subsections;
   cross-file reference narrative.
4. `git log --oneline -20` — recent commits; the sketch-08
   and sketch-09 arc commits carry dense readable bodies.
5. `design/substrate-knowledge-fold-sketch-01.md` — the
   first design-only consolidation sketch under PFS2;
   commitments KF1–KF5 are load-bearing for any port work.
6. `design/production-format-sketch-06.md` — the first
   dialect-layer production sketch; sets precedent for
   PFS7 / PFS8 (next-dialect schemas) and for the
   Production C opener (cross-boundary namespace decision).
7. The two most-recent probe JSONs (still
   `reader_model_oedipus_aristotelian_output.json`,
   `reader_model_rashomon_aristotelian_output.json`) —
   unchanged through sketch-09; probe work unlocks again at
   the next research-track arc.
