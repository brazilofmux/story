# State of play — sketch 07

**Status:** active
**Date:** 2026-04-19
**Supersedes:** [state-of-play-06](state-of-play-06.md)

Cold-start orientation doc, rewritten (not amended) at the
close of a small rebalancing arc that landed the Held record
sketch + schema and retired two prior dispositions.

**Three commits since state-of-play-06** — all production-
track, closing the state-of-play-06 §What's next pairing of
research item #2 (KnowledgeEffect.remove refactor) + production
item B (Held record schema). The pairing landed together
because the two items turned out to be one arc, not two.

- `653c9f5` — substrate-held-record-sketch-01: design-first
  for Held; amends ES3 to (holder, held, remove); corrects
  state-of-play-06 item #2.
- `d66ea4e` — production-format-sketch-04: design-first for
  Held schema + event.json KnowledgeEffect amendment; retires
  sketch-03 dispositions 1+2.
- `43a3ab5` — production-format-sketch-04 implementation;
  schema/held.json + conformance; 706 tests passing.

**Headline.** The Held record is now canonically specified.
Entity + Description + Prop + Event + Held — five substrate
records with language-independent JSON Schema; six files under
`schema/`. The KnowledgeEffect shape amended at both the
design-sketch layer (ES3-amendment) and the schema layer
(event.json) to nest a full Held record and admit the `remove`
polarity the factual-dislodgement pattern has always used. The
Python prototype continues untouched — nine production-track
commits without a line of change under `prototype/story_engine/`.

**State-of-play-06 item #2 correction.** The research/production
pairing sketch-06 proposed framed item #2 as "rewrite the 7
remove=True realization events to drive the audit to 0". That
framing was wrong: the realization-removes-propositions
workaround identity-and-realization-sketch-01 §Prior encoding's
retirement targets had already been retired (the 7 remaining
cases are the `remove_held` factual-dislodgement pattern
§Sternberg-stays-literal endorsed as legitimate). Sketch-07's
arc closed the pairing differently: rather than refactor the
7 cases out, formalize the pattern they use as a first-class
KnowledgeEffect field. SH8 + PFS4-E-amend-2 do that; the audit
shifts from drift-to-zero to baseline-is-final.

Re-write this sketch (don't amend — write sketch-08) at the
next milestone.

---

## What is built — delta from sketch-06

### The schema layer (one new file, one amendment, README sweep)

- `schema/held.json` (new, 44 lines) — Held per
  substrate-held-record-sketch-01 SH1–SH7. Five required
  fields; three closed enums (slot, confidence, via); `prop`
  via cross-file `$ref` to `schema/prop.json`.
- `schema/event.json` — KnowledgeEffect sub-schema rewrite.
  `(kind, holder, prop, via)` → `(kind, holder, held,
  remove?)`. `held` `$ref`s `held.json`; `remove` optional
  with `default: false`. WorldEffect untouched.
- `schema/README.md` — substantial sweep. "What's here" now
  lists all five shipped substrate records; stale
  Entity / Event / Prop deferral entries removed; deferred
  list focuses on dialect / cross-boundary / Branch /
  KnowledgeState work.

### The design sketches (two new)

Both shipped design-first per PFS2:

- `design/substrate-held-record-sketch-01.md` — Held's
  field-level spec (SH1–SH8). Eight commitments; two explicit
  amendments (ES3 shape revision; §Sternberg-stays-literal
  formalization). Seven OQs banked.
- `design/production-format-sketch-04.md` — Held schema +
  event.json amendment production design (PFS4-H1–H7 + PFS4-
  E-amend-1..4 + PFS4-D1..3). Four anticipated mechanical
  dispositions; four OQs banked.

### The conformance test (three new tests, one dump-helper, one rewrite)

`prototype/tests/test_production_format_sketch_01_conformance.py`:

- `_load_held_schema` added; `_build_schema_registry` extended
  to cover held.json.
- `_dump_held` (new) — field-for-field isomorphic to Python
  Held.
- `_dump_knowledge_effect` rewritten — emits `(kind, holder,
  held, remove?)`.
- `test_held_schema_metaschema_valid` (new).
- `test_held_schema_has_expected_shape` (new).
- `test_held_corpus_conformance` (new) — **199 Held records
  validated, 199 clean passes**. First time Helds are checked
  against a canonical spec.
- `test_event_schema_has_expected_shape` rewritten for the
  amended KnowledgeEffect shape.
- `test_knowledge_effect_remove_audit` docstring rewritten to
  the baseline-is-final framing.

### Corpus validation outcomes

- Event corpus still 458/458 clean. The amended KnowledgeEffect
  shape validates the same corpus — because the Python shape
  was always (agent_id, held, remove) and the schema now
  matches it field-for-field.
- Held corpus 199/199 clean. No findings. Three closed enums
  all exercised (slot × 4, confidence × 4, via × 6 diegetic;
  5 narrative-via values remain unexercised as expected — the
  substrate-layer corpus has no reader-state events).
- Remove audit: 7 (unchanged; baseline-is-final).
- Full test suite: 706 passing (+3 from the 703 baseline).

### Python unchanged

**Nine consecutive production-track commits (sketch-01 through
sketch-04, design + impl each, +04-implementation) without a
line of change under `prototype/story_engine/`.** Sketch-07's
three commits continue that streak. Python Held, Python
KnowledgeEffect, Python Slot + Confidence enums — all exactly
as they were at state-of-play-06.

The dump-layer does the work: the Python records are fully
conformant when run through `_dump_*` helpers. Python-as-sneaky
(state-of-play-06's phrase) — where the Python shape looks like
a vestige but the distinctions it carries are real — held up
again. The 7 `remove=True` cases are not vestigial workarounds;
the slot/confidence two-field shape is not vestigial either
(OQ1 bank for collapse if the orthogonality stays unused).

---

## Shift-point — further clarification

State-of-play-06 introduced three axes: architectural-stability,
behavioral-stability, and spec-portability. All three were
GREEN for the substrate at sketch-06.

Sketch-07 doesn't add a new axis; it **strengthens
spec-portability** for the substrate layer. Before sketch-07:
the Held record was fold-output-only at the spec level (ES3
committed KnowledgeEffect carried no Held fields; slot and
confidence were "fold-derived"). That reading of the spec was
not actually portable — a port would have had to invent
via→slot dispatch semantics the substrate didn't document.
After sketch-07: Held is a first-class record with its own
schema; authorship is explicit; ports read the schema + the
Held sketch and have everything they need.

**What this unlocks further.** Roadmap item #4 (port) was
un-gated on substrate spec after sketch-06. After sketch-07,
the unblock is sharper: the fold semantics (what happens when
two effects on the same (holder, prop) land at different
τ_s; how `remove` interacts with branch scope; what the fold
does with via="forgetting") are the remaining substrate-layer
under-specifications. None are record-shape questions; all
are fold-mechanics questions, which is the natural next design
arc surface (`substrate-knowledge-fold-sketch-01` candidate).

---

## What the sketch-07 arc revealed

### Plan revision catches the real problem

State-of-play-06 proposed the pair "research #2 (remove=True
refactor) + production B (Held schema)" as a rebalancing arc.
The proposal assumed they were two tasks that happened to
pressure each other. Orientation during Phase 1 surfaced that
the 7 remove=True cases were already the endorsed pattern,
not drift — state-of-play-06 item #2 was miscalibrated on the
audit's baseline interpretation. The arc's shape revised: one
task, not two. The design sketch formalized the pattern rather
than refactoring it out.

**This is what PFS2 orientation-before-action is for.** Had
the arc proceeded on state-of-play-06's framing, it would have
rewritten working code to fit an imagined clean-form target.
Catching the miscalibration in design-first mode saved the
rewrite from happening.

### The design / implementation split keeps tightening

Three commits this arc: design-sketch → production-sketch →
implementation. Each commit is self-contained; the design
commits don't touch code at all, the production-sketch commit
doesn't either, and the implementation commit is schema +
conformance test + README sweep. The rhythm is familiar from
the sketch-06 arc but the granularity is smaller (one record +
one amendment this time, vs. multi-record sketches-01/02/03).

Small arcs fit the ~20-year horizon pattern: a day's work
earns a day's worth of commits, not a week's.

### Dispositions retire as cleanly as they land

Two of sketch-03's three conformance dispositions (Disposition
1 KnowledgeEffect shape translation; Disposition 2
KnowledgeEffect.remove) retire under sketch-07. Disposition 3
(Event.metadata — 0/102 events populate the field; harmless
artifact) stays. The pattern — dispositions enter with one
sketch's implementation and exit with a later sketch's
amendment — is a healthy sign: dispositions are not
permanent tape-over; they are markers for the next design arc.

---

## What's next (research AND production)

### Research track

Re-ordered by this arc's completion:

1. **Probe-surfaced encoding cleanups** (sketch-05 → 06
   holdover, still unopened). 2 Oedipus prose fixes + 5
   Rashomon phase-annotation cleanups from the Aristotelian
   probe arc. No dialect change needed; smallest concrete
   research item.
2. **Descriptions-sketch-01 amendment** — add `authoring-
   note` to §Kinds and `superseded` to §Optional fields,
   clearing sketch-01's two dispositions (currently
   dispositioned in the Description conformance test).
3. **Aristotelian-sketch-02 candidate.** 5 relation-extension
   proposals (ArMythosRelation + ArFrameMythos +
   ArAnagnorisisLevel + ArAnagnorisisChain +
   ArPeripeteiaAnagnorisisBinding) banked from the probe arc.
   Evaluate under EP-style forcing-function criteria.
4. **A seventh Aristotelian encoding** (Macbeth or Ackroyd) —
   provides the second-encoding pressure several banked
   relation proposals need.
5. ***And Then There Were None* content fill.** Large task.
   Would pressure several banked items (quantified
   propositions via OQ4 of prop-sketch; ArMythosRelation if
   ten deaths are linked mythoi; MN2 concealment-asymmetry).
6. **Close a banked scheduling-act-family seed** (OQ2-reshaped
   wife prose-carried drivers; OQ1-reshaped woodcutter
   cross-branch signature; bandit-refinement).

Note: state-of-play-06's research item #2 (KnowledgeEffect.
remove refactor) is **struck** — it was based on a misread;
the pattern is canonical now.

### Production track

The substrate schema layer is complete-plus-Held. Natural next
production-track surfaces:

A. **Dialect schemas.** Each dialect (Dramatic, Dramatica-
   complete, Save-the-Cat, Aristotelian) has ~5–15 record
   types. Candidate first: Aristotelian (smallest dialect;
   aristotelian-sketch-01 is field-level-detailed; ~7 records
   to ship).
B. **Branch record schema.** Substrate-sketch-04 §Branch
   representation specifies the Branch record fields (label,
   kind, parent, metadata) at the design level. A slim
   production sketch suffices — most of the design work is
   done.
C. **Substrate-knowledge-fold-sketch-01.** The remaining
   substrate-layer under-specification is fold mechanics:
   how K1 resolves conflicting same-prop effects (current
   Python: later-wins); what the fold does with
   via="forgetting" (substrate-sketch-04 §Update operators:
   deliberately non-committal between decay and deletion);
   how `remove` interacts with branch scope (per B1, but the
   edge cases haven't been tested). This is design-sketch
   work; no schema deliverable yet. Would consolidate OQ5 /
   OQ6 / OQ7 of substrate-held-record-sketch-01 + ES3 OQ1
   into a single design-level close.
D. **Cross-boundary record schemas.** Lowering,
   VerificationReview, StructuralAdvisory, VerifierCommentary,
   ArAnnotationReview, ArObservationCommentary, DialectReading.
   Multiple sketches; substantial arc.
E. **Markdown-fenced author parser** (roadmap item 1).
   Unblocked by substrate schema layer; first consumer of the
   schemas outside the conformance test. Natural next-
   production-arc candidate.
F. **Prose export round-trip starter** (roadmap item 3).
G. **Goodreads import prototype** (roadmap item 2).
H. **Port work** (roadmap item 4). Dialect-schema-gated.

### Recommendation

Sketch-07's arc was small (3 commits) and rebalancing; a
similar small next arc keeps the cadence. Two candidates fit:

- **Research track #2** (descriptions-sketch-01 amendment —
  clearing the two active conformance dispositions). Quick
  clarifying arc; the amendment is small; the audit flips
  clean.
- **Production track B** (Branch record schema). Design is
  already done; production sketch would be slim; closes
  another substrate-layer record.

Alternative: **Production track C** (fold-sketch) is the
design-heavy surface that closes several banked OQs at once.
Design-only arc; no schema deliverable. Slightly larger than
the above two but natural follow-on to sketch-07.

Or **production track E** (markdown parser) — still the
newly-compelling consumer-of-schemas direction, unchanged
from sketch-06's recommendation.

---

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketches-04/05/06. Validated again across
the 3 commits:

- **Orientation before commitment.** Phase 1 began with a
  survey pass: read the sketches, count the corpus cases,
  read the encoding comments. That read surfaced the
  state-of-play-06 miscalibration before any design work
  went out. The orientation pass saved the arc from going
  the wrong direction.
- **Sketches before implementation.** Same rhythm as the
  sketch-06 arc.
- **First-principles design derivation.** Held's shape
  derived from what the K1 fold actually produces and what
  the authoring surface actually needs, not from the Python
  dataclass.
- **Amendment surfaces, not schema stretching.** SH5 +
  SH8 + ES3-amendment explicitly revise a prior sketch
  (substrate-effect-shape-sketch-01 ES3) rather than widening
  the Held schema silently to fit Python. The amendment is
  load-bearing and cited transparently.
- **State-of-play at milestone boundaries.** This doc.
- **Commit messages as cross-session artifacts.** The three
  production commits average ~70-line bodies; a cold-start
  Claude reading `git log --oneline -5` can reconstruct the
  arc fully.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic.
2. This doc (`design/state-of-play-07.md`) — current corpus,
   shift-point state, research + production tracks.
3. `schema/README.md` — the production layer's discipline +
   what's shipped.
4. `git log --oneline -15` — recent commits; the sketch-06
   and sketch-07 arc commits carry dense readable bodies.
5. `design/substrate-held-record-sketch-01.md` §Why now +
   §Amendments — the §Why now paragraph documents the
   state-of-play-06 miscalibration and how Phase 1's
   orientation caught it; the §Amendments section spells out
   the ES3 revision.
6. `design/production-format-sketch-04.md` §Conformance
   dispositions — the pattern of sketch-03's dispositions
   retiring under sketch-04's amendment.
7. The two most-recent probe JSONs (still
   `reader_model_oedipus_aristotelian_output.json`,
   `reader_model_rashomon_aristotelian_output.json`) — unchanged
   through this arc; probe work unlocks again at the next
   research-track arc.
