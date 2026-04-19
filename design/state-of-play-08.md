# State of play — sketch 08

**Status:** active
**Date:** 2026-04-19
**Supersedes:** [state-of-play-07](state-of-play-07.md)

Cold-start orientation doc, rewritten (not amended) at the
milestone where the substrate schema layer reaches structural
completion.

**Four commits since state-of-play-07** — two small
rebalancing arcs, back-to-back, both landing inside the same
day. The first closed state-of-play-07's research-track item
#2 (descriptions-sketch-01 amendment clearing two active
Description conformance dispositions); the second closed
state-of-play-07's production-track item B (Branch record
schema). Neither arc required design derivation beyond what
prior sketches already committed — the first was an in-place
amendment recognizing patterns already in the corpus; the
second was pure format-rendering of a design spec already in
substrate-sketch-04.

- `b4a6307` — descriptions-sketch-01 amendment (design).
  Adds `authoring-note` kind + `superseded` status with
  structural justifications grounded in the rocky, macbeth,
  and substrate-edit-chain usage already in the codebase.
- `9941ce0` — descriptions-sketch-01 amendment
  (implementation). Schema enum extensions; dispositions 1+2
  retired in `production-format-sketch-01.md`; conformance
  test simplified (`_classify_failure` helper removed, meta-
  test retired).
- `082bb49` — production-format-sketch-05 (design).
  Slim production sketch for Branch; six record-shape
  commitments + two dump-layer commitments; no design
  derivation — substrate-sketch-04 §Branch representation
  had already committed the four-field shape.
- `220743d` — production-format-sketch-05 (implementation).
  `schema/branch.json` + conformance test extension + README
  sweep. Branch corpus 25/25 clean (17 canonical, 8
  contested; zero drafts / counterfactuals — enum admits).

**Headline.** The substrate schema layer is **structurally
complete**. Six records — Entity, Description, Prop, Event,
Held, Branch — each with a language-independent JSON Schema
under `schema/`. Every substrate record named in
substrate-sketch-04 or substrate-sketch-05 has a matching
schema file. The Description audit surface goes to zero
findings for the first time. The Python prototype continues
untouched — twelve consecutive production-track commits
without a line of change under `prototype/story_engine/`.

Re-write this sketch (don't amend — write sketch-09) at the
next milestone.

---

## What is built — delta from sketch-07

### The schema layer (one new file, three extensions, README sweep)

- `schema/branch.json` (new, 46 lines) — Branch record per
  substrate-sketch-04 §Branch representation. Two required
  fields (`label`, `kind`); one conditional (`parent`,
  required except when `kind = canonical`; via allOf /
  if-then-else); one optional open object (`metadata`). No
  outbound cross-file references (event.json's `branches`
  field remains a plain array of label strings, not
  $ref-typed; cross-reference consistency between
  `event.branches` and the Branch registry is banked as
  PFS5 OQ3).
- `schema/description.json` — kind enum extended from six to
  seven values (`authoring-note` added); status enum extended
  from two to three values (`superseded` added); both field
  descriptions now reference descriptions-sketch-01
  §Amendments.
- `schema/README.md` — "What's here" section now lists all
  six substrate records with `branch.json` included; a new
  paragraph notes Branch has no outbound cross-file
  references; stale "What's deferred" Branch entry removed;
  the list reflects dialect / cross-boundary / KnowledgeState
  as the remaining schema-layer work.

### The design sketches (one amendment, one new production sketch)

- `design/descriptions-sketch-01.md` — first in-place
  amendment under the PFS2 discipline. `Amended: 2026-04-19`
  added to frontmatter; `authoring-note` entered as a
  seventh kind (distinguishing from `authorial-uncertainty`:
  the former describes encoding choices, the latter doubt
  about the story); `status` in §Optional fields extended
  from two values to three with the edit-chain mechanism
  named; §Record-level invariants clarified to distinguish
  content-immutability (strict, on semantic fields) from the
  two-field mutation surface (status + supersession
  metadata) the edit-chain requires; new §Amendments section
  documents both additions with structural justifications,
  grid-snap postures, and conformance implication.
- `design/production-format-sketch-05.md` (new, 320 lines) —
  Branch production sketch; six record-shape commitments
  (PFS5-B1..B6) + two dump-layer commitments (PFS5-D1..D2);
  five open questions banked (label format, metadata shape,
  cross-reference consistency, reconvergence semantics
  inherited from sketch-04 OQ13, draft supersession
  inherited from sketch-04 OQ14).
- `design/production-format-sketch-01.md` — §Dispositions 1
  and 2 rewritten to mark retirement under the 2026-04-19
  amendment, with original framings preserved for audit; the
  corpus-survey summary gains a post-retirement status note;
  the recognition-protocol paragraph rewritten (the test now
  recognizes no Description dispositions).

### The conformance test (four new tests, three helpers, one helper retired)

`prototype/tests/test_production_format_sketch_01_conformance.py`:

- `_load_branch_schema` added.
- `_discover_encoding_branches` added — iterates
  `ALL_BRANCHES.values()` across encoding modules (dict
  export, unlike FABULA / ENTITIES / DESCRIPTIONS which are
  list exports).
- `_dump_branch` added — field-for-field isomorphic to
  Python Branch; kind enum `.value` extraction; parent
  omitted when None (canonical); no metadata emission.
- `_classify_failure` removed (its two dispositions retired;
  no work remains).
- `DISPOSITION_KIND_AUTHORING_NOTE` and
  `DISPOSITION_STATUS_SUPERSEDED` constants + their comment
  blocks removed.
- `test_branch_schema_metaschema_valid` (new).
- `test_branch_schema_has_expected_shape` (new).
- `test_branch_corpus_conformance` (new) — 25 Branch
  records, 25 clean passes; by-kind breakdown printed.
- `test_corpus_conformance` (Description) simplified — no
  disposition-classification branching; docstring references
  the retirement.
- `test_description_schema_has_expected_shape` updated —
  kind enum assertion adds `authoring-note`; status enum
  assertion adds `superseded`; both carry pointers to
  §Amendments.
- `test_dispositions_resolution_paths` removed (vestigial
  after both dispositions retired).

### Corpus validation outcomes

- Description corpus: 33 records validate clean. **First
  clean Description corpus** — prior state was 29 clean + 4
  dispositioned (2 × `kind="authoring-note"` + 2 ×
  `status="superseded"`).
- Branch corpus: 25 records validate clean. 17 canonical, 8
  contested (Rashomon × 4 base + verification-module
  re-imports). Zero drafts, zero counterfactuals in the
  corpus; schema admits, corpus does not exercise — same
  shape as sketch-04's 5 unused narrative-via enum values.
- Held corpus: 199 clean (unchanged).
- Event corpus: 458 clean (unchanged).
- Entity corpus: 377 clean (unchanged).
- Remove audit: 7 (unchanged; baseline-is-final).
- Full test suite: **708 passing** (+2 from the 706 baseline;
  net: +3 new Branch tests − 1 retired meta-test on the
  Description side).

### Python unchanged

**Zero lines modified under `prototype/story_engine/` across
the four sketch-08 commits.** Continues the production-track
streak that started with production-format-sketch-01: every
substrate-layer schema file and its conformance test extension
has landed without asking the Python prototype to change.
State-of-play-07's phrasing ("nine consecutive production-
track commits" through sketch-07) extends; the streak's
current length depends on how state-of-play commits are
counted, but the structural claim is stable — the Python
prototype is a conformance check, not a template, and it has
stayed that way across every substrate schema's arrival.

The dump-layer does the work, as usual: the Python records
are fully conformant when run through `_dump_*` helpers.
Python-as-sneaky (sketch-06's phrase, retained through
sketches-07 and -08) held up twice more in this arc:

- `authoring-note` kind was used in the Python encodings
  (rocky.py × 2) before the sketch enumerated it; the
  amendment recognized the pattern rather than asking the
  encoding to change.
- `superseded` status was set by the Python edit-chain
  machinery (substrate.py `apply_description_edit`) before
  the sketch enumerated it; the amendment recognized the
  mechanism rather than asking the machinery to change.

Python Branch has no `metadata` field; schema admits
`metadata` as optional; the corpus validates clean under
omission. That is the *opposite* direction of
Python-as-sneaky — Python is under-specified relative to
the sketch, and the schema carries the over-spec that a
future Python refactor may populate. Both directions are
PFS2-kosher.

---

## Shift-point — substrate schema layer completes

Sketch-07 noted that spec-portability had sharpened with
Held: "a port would have had to invent via→slot dispatch
semantics the substrate didn't document … After sketch-07:
Held is a first-class record with its own schema; ports read
the schema + the Held sketch and have everything they need."

Sketch-08 closes the substrate-layer version of that claim
entirely: **every substrate record type a port would need to
emit or consume has a matching JSON Schema file**. The
design/schema gap at the substrate layer reaches zero. A
port that targets the substrate layer can read:

- `schema/*.json` (six files) for record shapes.
- `design/substrate-sketch-04.md` for branch semantics
  (fold-scope-across-branches, enforcement-per-branch,
  kind × status legal combinations).
- `design/substrate-sketch-05.md` for the substrate's
  overall architecture (K1 knowledge fold, W1 world
  projection, A3 invariant-testability).
- `design/substrate-effect-shape-sketch-01.md` (as amended
  by substrate-held-record-sketch-01) for effect semantics.
- `design/descriptions-sketch-01.md` (as amended 2026-04-19)
  for the interpretive-peer surface.
- `design/substrate-prop-literal-sketch-01.md` for the Prop
  atomic.
- `design/substrate-entity-record-sketch-01.md` for Entity.
- `design/substrate-held-record-sketch-01.md` for Held.

That's a complete specification *without reading any Python*.
Roadmap item #4 (port) is now unblocked at the substrate
layer in the strongest sense the repo can claim: no
structural-spec discovery work remains.

**What's still under-specified at the substrate layer.** The
*fold mechanics*. Substrate-sketch-04 §Update operators
deliberately leaves `via="forgetting"` non-committal (decay
vs. deletion). Substrate-sketch-04 open question 13
(reconvergence) and open question 14 (draft supersession)
are both unresolved. Substrate-held-record-sketch-01 OQ5
(conflicting same-prop effects, currently later-wins in
Python) is banked. These are fold-time behaviors, not
record-shape questions — they do not gate the port on
structural grounds, but they do gate it on *behavioral*
grounds. Candidate follow-on: `substrate-knowledge-fold-
sketch-01` (state-of-play-07's production item C).

**Dialect work is unblocked but unchanged in posture.** The
Aristotelian dialect (~7 records, first dialect candidate)
and the reader-model / probe surfaces both sit at the layer
above substrate; nothing in sketch-08's work changes their
readiness beyond the observation that the substrate layer is
now fully spec'd for them to build against.

---

## What the two sketch-08 arcs revealed

### Amendment cadence works

Sketch-08's first arc was the first in-place amendment to a
design sketch under the PFS2 discipline. The pattern that
emerged:

- Amend the original sketch in-place (update committed
  fields, clarify invariants, add to lists), marked by an
  `Amended:` frontmatter line.
- Add an `§Amendments` section at the sketch's end
  documenting what changed and why, with structural
  justifications grounded in corpus / machinery evidence.
- The amending commit can then be cited cleanly by the
  implementation commit, other sketches, and cold-start
  readers. Sketch-07's ES3-amendment (inside substrate-
  held-record-sketch-01) had shown the shape *between*
  sketches; sketch-08's descriptions-sketch-01 §Amendments
  shows it *within* one sketch.

A sketch amendment is different from a sketch supersession:
the original sketch remains the canonical doc; the
amendment is an audit-trail update, not a rewrite. The
methodology-level claim underneath — *sketches are
design-first; schemas and code follow* — is preserved under
both shapes.

### "Slim" production sketches when the design is already done

Production-format-sketch-05 was the first production sketch
to ship where no design derivation was needed — substrate-
sketch-04 §Branch representation had already committed the
shape, so the production sketch reduced to format-rendering
+ conformance plan. That constrained the sketch's size (320
lines vs. sketch-04's 552, sketch-03's 556, sketch-01's
~1100). The discipline: when the design sketch does the
structural work, the production sketch earns its brevity.

Sketch-05's structural scaffolding (Purpose, Why now, Scope,
Commitments, Conformance dispositions, Open questions) is
unchanged from the sketch-02/-03/-04 template. Only the
internal Commitments section shrinks; the governance
sections stay as-is.

### Non-findings vs. dispositions

Sketch-05's §Conformance dispositions lists two *anticipated
non-findings* (metadata field unexercised; draft +
counterfactual kinds unexercised) rather than true
dispositions. The distinction, clarified in sketch-04's
§Not-a-disposition section and now generalized:

- A **disposition** is a known-failure-mode where a corpus
  record fails schema validation and the test tolerates it
  pending a design-sketch amendment.
- A **non-finding** is a known shape-spec decision where the
  schema admits something the corpus does not (yet)
  exercise, and the corpus validates clean because it never
  hits the admitted corner. No tolerance is needed; no
  amendment-path follows.

Both sketch-08's arcs produced non-findings only. No active
dispositions remain in the substrate corpus (the sole
remaining sketch-03 Disposition 3 — Event.metadata 0-of-102
populated — is technically active but marked harmless
artifact; it is the edge case between "disposition" and
"non-finding"). The Description corpus, post-retirement of
Dispositions 1 and 2, goes to zero dispositions for the
first time.

### The commit cadence is the rhythm

Twelve production-track commits across ten weeks (from
sketch-01 through sketch-08) with zero lines changed under
`prototype/story_engine/`. The average arc is 2-3 commits;
design-first is non-negotiable; implementation follows with
mechanical fidelity; the test suite grows +2-3 tests per
arc. Sketch-08's two arcs fit the pattern cleanly. A ~20-year
horizon is built one small arc at a time.

---

## What's next (research AND production)

### Research track

Re-ordered by sketch-08's completions (item #2 from sketch-07
closed):

1. **Probe-surfaced encoding cleanups** (sketch-05 → 06 → 07
   → 08 holdover, still unopened). 2 Oedipus prose fixes + 5
   Rashomon phase-annotation cleanups from the Aristotelian
   probe arc. No dialect change needed; smallest concrete
   research item.
2. **Aristotelian-sketch-02 candidate.** 5 relation-extension
   proposals (ArMythosRelation + ArFrameMythos +
   ArAnagnorisisLevel + ArAnagnorisisChain +
   ArPeripeteiaAnagnorisisBinding) banked from the probe arc.
   Evaluate under EP-style forcing-function criteria.
3. **A seventh Aristotelian encoding** (Macbeth or Ackroyd) —
   provides the second-encoding pressure several banked
   relation proposals need.
4. ***And Then There Were None* content fill.** Large task.
   Would pressure several banked items (quantified
   propositions via OQ4 of prop-sketch; ArMythosRelation if
   ten deaths are linked mythoi; MN2 concealment-asymmetry).
5. **Close a banked scheduling-act-family seed** (OQ2-reshaped
   wife prose-carried drivers; OQ1-reshaped woodcutter
   cross-branch signature; bandit-refinement).

Note: state-of-play-07's research item #2 (descriptions-
sketch-01 amendment) is **done** (sketch-08 arc 1).

### Production track

The substrate schema layer is now structurally complete.
Natural next production-track surfaces:

A. **Dialect schemas.** Each dialect (Dramatic, Dramatica-
   complete, Save-the-Cat, Aristotelian) has ~5–15 record
   types. Candidate first: Aristotelian (smallest dialect;
   aristotelian-sketch-01 is field-level-detailed; ~7
   records to ship). Unchanged from sketch-07.
B. **Substrate-knowledge-fold-sketch-01** (was sketch-07's
   production item C). The remaining substrate-layer
   under-specification is fold mechanics: how K1 resolves
   conflicting same-prop effects (current Python: later-wins);
   what the fold does with `via="forgetting"` (substrate-
   sketch-04 §Update operators: deliberately non-committal
   between decay and deletion); how `remove` interacts with
   branch scope; plus substrate-sketch-04 OQ13 (reconvergence)
   and OQ14 (draft supersession) — all banked. This is design-
   sketch work; no schema deliverable yet. Would consolidate
   at least four banked OQs into a single design-level close.
   **Design-heavy; promoted one slot because the substrate
   schema layer completing makes fold mechanics the obvious
   next surface.**
C. **Cross-boundary record schemas.** Lowering,
   VerificationReview, StructuralAdvisory, VerifierCommentary,
   ArAnnotationReview, ArObservationCommentary, DialectReading.
   Multiple sketches; substantial arc.
D. **Markdown-fenced author parser** (roadmap item 1).
   Unblocked by substrate schema layer; first consumer of the
   schemas outside the conformance test. Unchanged
   candidate.
E. **Prose export round-trip starter** (roadmap item 3).
F. **Goodreads import prototype** (roadmap item 2).
G. **Port work** (roadmap item 4). Substrate-layer-unblocked
   as of this arc (§Shift-point); fold-mechanics-gated if
   behavioral fidelity is wanted (item B above).

Note: state-of-play-07's production item B (Branch schema)
is **done** (sketch-08 arc 2).

### Recommendation

Sketch-08's arcs were small (2 commits each) and rebalancing;
a similar small next arc keeps the cadence. Three candidates
fit the small-arc shape:

- **Research track #1** (probe-surfaced encoding cleanups).
  Quick clarifying arc; no dialect change; the smallest
  concrete research item. Long-time holdover.
- **Production track B** (fold-sketch) — design-only arc,
  one commit. Consolidates banked OQs; closes the last
  substrate-layer under-specification. Design-heavy but no
  schema deliverable.

Alternative: **Production track A** (Aristotelian dialect
schemas). Larger arc (~7 records) but the natural
"up-the-layer-stack" next step after the substrate layer
completes. Fits the "moving to dialect layer" narrative the
sketch-08 milestone suggests.

Or **production track D** (markdown parser) — still the
newly-compelling consumer-of-schemas direction. The
substrate-layer completion makes it doubly timely: every
record the parser would need to emit is now spec'd.

---

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketches-04/05/06/07. Validated again
across the 4 commits:

- **Orientation before commitment.** Phase 1 on each arc
  began with a survey read: descriptions-sketch-01's
  current shape + the disposition comments + the corpus
  usage for arc 1; substrate-sketch-04 §Branch
  representation + the Python Branch dataclass + the corpus
  Branch records for arc 2. Both arcs discovered the work
  was smaller than the sketch-07 §What's next framing
  suggested (disposition comment misnamed the encodings;
  Branch shape was fully already design-spec'd).
- **Sketches before implementation.** Same rhythm as prior
  arcs.
- **First-principles vs. retroactive recognition.**
  Sketch-08 added a wrinkle: amendments that *recognize
  existing patterns* rather than *deriving new ones*. Both
  `authoring-note` and `superseded` were already in use;
  the amendment made them canonical. Similarly, `metadata`
  on Branch was already spec'd in substrate-sketch-04 but
  the Python under-implemented — the schema made the gap
  visible.
- **Amendment surfaces, not schema stretching.** The two
  additions to descriptions-sketch-01 are cited
  transparently under §Amendments with structural
  justifications; production-format-sketch-01 §Dispositions
  1 and 2 are rewritten with retirement markers, original
  framings preserved for audit.
- **State-of-play at milestone boundaries.** This doc.
  Milestone: substrate schema layer structurally complete.
- **Commit messages as cross-session artifacts.** The four
  production commits average ~80-line bodies; a cold-start
  Claude reading `git log --oneline -6` can reconstruct
  sketch-08's arcs fully.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic.
2. This doc (`design/state-of-play-08.md`) — current corpus,
   shift-point state, research + production tracks.
3. `schema/README.md` — the production layer's discipline +
   the six substrate records shipped.
4. `git log --oneline -20` — recent commits; the sketch-07
   and sketch-08 arc commits carry dense readable bodies.
5. `design/descriptions-sketch-01.md` §Amendments — the
   first in-place sketch amendment under the PFS2
   discipline; sets the shape for future amendments.
6. `design/production-format-sketch-05.md` §Conformance
   dispositions — the "slim production sketch" pattern
   when the design sketch has already done the structural
   work.
7. The two most-recent probe JSONs (still
   `reader_model_oedipus_aristotelian_output.json`,
   `reader_model_rashomon_aristotelian_output.json`) —
   unchanged through the sketch-08 arcs; probe work unlocks
   again at the next research-track arc.
