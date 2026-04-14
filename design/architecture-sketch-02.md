# Architecture — sketch 02

**Status:** draft, active
**Date:** 2026-04-14
**Supersedes:** nothing — extends [architecture-sketch-01.md](architecture-sketch-01.md)
**Frames:** all topic sketches; all future prescriptive/upper-layer sketches
**Superseded by:** nothing yet

## Purpose

Name the shape of the system *above* the substrate. Previous sketches
have treated the substrate as if it were the whole engine; the only
"above" mentioned is architecture-01's hint at L1 (library operators)
and the upcoming "prescriptive / upper-layer" line in the design
README. That hint is too thin to carry the work it must carry, and it
framed the upper layer as a library-of-queries *over* the substrate
rather than as a stack of distinct languages *compiled into* it.

This sketch commits to the compiler-like architecture the project's
mental model has been reaching for:

- The story-engine is a **stack of dialects**, each with its own
  schema and semantics, linked by **lowering relations**. The
  substrate is the lowest dialect the engine manages; prose
  (paragraphs, scenes, chapters) is the output, below.
- Lowering is **author-driven**, lossy, and non-deterministic. An
  upper-dialect record can be realized by many substrate
  encodings; the author picks the realization and annotates the
  binding. The system never synthesizes a binding.
- Verification — the **linter at each dialect boundary** — is
  automated. It reads the binding plus the records it points at
  and emits observations to the existing proposal queue.
  Observations, not errors; descriptions-01 and reader-model-01
  already specify the shape of that pipe.
- Dialects are **opt-in and plural**. A story may sit entirely in
  the substrate. A story that opts in may choose Dramatica, or
  Save-the-Cat beats, or Aristotelian unities, or a custom
  author-defined template, or a stack of several. The architecture
  commits to admitting them, not to any one.
- The **reader-model probe generalizes**: it is already a partner
  at the substrate/description boundary (A5 of architecture-01);
  the same partner pattern applies at every dialect boundary.

Why this shape, practically: **most writers already think in some
version of these dialects.** Acts, beats, inciting incidents,
climaxes, throughlines, central arguments, character functions —
these are craft vocabulary from Aristotle through Field through
McKee through Snyder through Dramatica. A system that meets writers
in the vocabulary they already use is a system that is *legible* to
them. The multi-dialect stack is not an engineering aesthetic; it is
a concession to how authoring actually happens.

This sketch specifies:

- The commitments (A6–A11) that define the multi-dialect shape.
- The relation to architecture-sketch-01's A1–A5 (which carry
  forward unchanged and extend to each dialect).
- The shape of a Lowering record (sketch-level; exact fields are
  left to a dialect-boundary or lowering-specific sketch).
- The shape of per-boundary verification and how it uses the
  proposal queue.
- How the reader-model probe generalizes to cross-boundary
  partnering.
- What is explicitly *not* committed to.
- A worked example using Oedipus + a minimal Dramatic dialect.
- Open questions and expected follow-on sketches.

## What this sketch is *not* committing to

- **Any specific upper dialect.** Not Dramatica, not Save-the-Cat,
  not Field's paradigm. This sketch commits to the *stack*; each
  dialect is its own sketch.
- **The exact shape of Lowering records.** The sketch names that
  lowerings are authored records with an upper side and a lower
  side; the exact fields (ids, multiplicities, annotation shape)
  are a dialect-boundary or lowering-specific sketch.
- **A canonical set of dialect boundaries.** Two boundaries may
  merge; a dialect may fan out to multiple lower dialects. The
  architecture admits arbitrary dialect graphs with the substrate
  as a single sink.
- **Automated lowering.** The system never synthesizes a lowering
  record. A reader-model partner may *propose* lowerings, which
  an author reviews; the proposal queue is the only way a
  lowering enters the store.
- **Lifting.** The sketch does not commit to inferring upper
  records from lower ones. (It does not forbid it either — a
  partner LLM might reasonably propose "the substrate slice at
  τ_d=40–50 reads as an Act 2 midpoint beat, do you want to
  lower this?" — but the formalism is one-way: the author writes
  upper records, lowerings bind them to lower records, and
  verification checks the binding.)
- **Cross-dialect query semantics.** A query written in one
  dialect's vocabulary against another dialect's records is not
  specified. Queries are dialect-local; cross-boundary reasoning
  happens through lowering + verification, not through a
  universal query surface.
- **Persistence of verification results.** Verification emits
  records to the proposal queue, which descriptions-01 OQ3 still
  has as deferred. Architecture-02 does not re-open OQ3.
- **Output-layer (prose) dialect.** The sketch names prose as
  "below the substrate" in the stack picture but does not
  formalize it. Prose is the target, not an intermediate
  representation the engine manages.

## What this sketch *is* committing to

1. **A6 — The story-engine is a stack of dialects.** Each dialect
   has its own schema (record types), its own semantics (queries,
   invariants, description surface), and its own grid-snap
   discipline (per A1/A3). The substrate is the lowest dialect the
   engine manages. Higher dialects name higher-level concepts
   (acts, throughlines, arguments); prose (paragraphs, scenes as
   written, chapters) is the output below the substrate and is
   not an engine-managed dialect.
2. **A7 — Lowering is author-driven.** The binding from an
   upper-dialect record to the lower-dialect records that realize
   it is an authored annotation, captured in a `Lowering` record.
   The system never synthesizes a lowering. A reader-model
   partner may propose one; acceptance is an authorial act via
   the existing proposal queue.
3. **A8 — Verification is automated linting at each dialect
   boundary.** For each pair of adjacent dialects (upper, lower)
   with one or more authored `Lowering` records between them, a
   verification layer reads the lowering, the upper records it
   names, and the lower records it points at, and checks whether
   the realization satisfies the upper intent. Verification emits
   observations — reviews, proposals — to the existing proposal
   queue. No new output pipe; no errors, only observations.
4. **A9 — Each verifier is implemented in the upper dialect's
   vocabulary, evaluated against the lower dialect's queries plus
   the lowering.** The Structural↔Substrate verifier reads in
   terms of "beats" and "acts" (upper), queries against substrate
   folds and descriptions (lower), and is parameterized by the
   lowerings that bind one to the other. This keeps the substrate
   clean — it does not acquire structural-dialect concepts — and
   keeps each verifier intelligible within its own level.
5. **A10 — Dialects are opt-in; multiple templates coexist.** A
   story may sit entirely in the substrate with no upper
   annotations (silent verification, no linter activity). A story
   that opts in may use any template (Dramatica, Save-the-Cat,
   Freytag, Aristotelian, author-defined) or several. Each
   template is its own dialect; dialects compose, they do not
   compete. Verification against Dramatica never precludes
   verification against Freytag on the same story.
6. **A11 — The reader-model probe generalizes as cross-boundary
   partner.** Architecture-01 A5 (interpretation is a partner,
   not a fallback) extends to every dialect boundary. A reader-
   model invocation at the substrate/description boundary reads
   substrate + descriptions and emits observations; the same
   mechanism at the Structural/Substrate boundary reads
   structural records + lowering + substrate and emits
   observations. The partner pattern is boundary-agnostic; the
   invocation is dialect-parameterized.

A6 through A11 pass architecture-01 A3 (schema inclusion test):
each describes drift the schema catches, not content an attentive
reviewer could self-police. Without A6, the substrate accretes
structural-dialect concepts that belong elsewhere. Without A7, the
system tries to infer authorial intent and fails silently on
mis-inference. Without A8, dialect boundaries are decorative, not
load-bearing. A9 is the discipline that lets each dialect stay
small. A10 is what keeps the architecture from becoming a
commitment to any one craft tradition. A11 is what keeps the
partner relationship from fragmenting across levels.

## Relation to architecture-01

Architecture-01's A1–A5 carry forward unchanged and extend to each
dialect independently:

- **A1 (grid-snap scope).** Each dialect has its own grid-snap
  discipline. The substrate grid-snaps structural facts about
  events and props; a Dramatic dialect grid-snaps structural
  facts about arguments and throughlines. LLM/human carries the
  affective/interpretive load *within each dialect*.
- **A2 (two-surface semantics).** Each dialect has its own facts
  and descriptions. Lowering binds upper *facts* to lower *facts
  + descriptions*; upper descriptions are about upper-dialect
  records, not about the substrate directly. (An upper
  description *may* reference a substrate record via the
  lowering, but it stays attached to its own dialect's anchor
  kinds.)
- **A3 (schema inclusion test).** Apply per dialect. A new field
  in the Dramatic dialect earns its place by passing A3 within
  the Dramatic dialect — not by comparison to substrate fields.
- **A4 (descriptions draft attention).** Each dialect's
  description surface carries attention per descriptions-01's
  commitments, re-specified per dialect. An "authorial-
  uncertainty" description on a Dramatic record uses the same
  attention machinery descriptions-01 specifies.
- **A5 (interpretation is a partner).** A11 is the
  generalization.

New commitments (A6–A11) compose with the old, they do not
override.

## Relation to topic sketches

- **Substrate-05.** The substrate is the lowest engine-managed
  dialect. Its commitments (E1, K1, K2, B1, M1, A3-retroactive,
  etc.) stand as the substrate dialect's commitments. Upper
  dialects do not alter them; they consume substrate queries
  through the lowering + verification pattern.
- **Identity-and-realization-01.** Identity and substitution are
  substrate-dialect primitives. Upper dialects may *reference*
  them via queries (e.g., a Dramatic verifier asking "at τ_s=13,
  does Oedipus's identity equivalence class collapse?"). Upper
  dialects do not introduce their own identity machinery.
- **Inference-model-01.** Rules and derivation are substrate-
  dialect. Upper dialects consume derived facts as query results;
  they do not author rules into their own dialect. (A future
  Dramatic-dialect sketch may need its own *dialect-local*
  inference — "this structural configuration entails that
  beat" — and if so, it uses the inference-01 machinery as a
  template, instantiated in the Dramatic dialect's vocabulary.)
- **Descriptions-01.** Each dialect has a description surface
  following descriptions-01's pattern. The substrate's
  description surface is the one descriptions-01 specifies; a
  Dramatic dialect's description surface is analogous — new
  kinds (`argument-note`, `throughline-rationale`), new anchor
  kinds (`argument`, `throughline`), but the same
  fold-invisibility, attention, review, and provenance
  machinery.
- **Reader-model-01.** The reader-model probe generalizes under
  A11. Reader-model-01's commitments (R1 typed I/O, R2 label
  descriptions in the view, R3 partner-not-fallback, R4 shared
  review-entry type across humans and LLMs, R5 declared-scope
  invocations, R6 anchor-τ_a staleness) all apply at every
  dialect boundary. A cross-boundary probe invocation declares
  which dialect's view it reads; everything else follows.
- **Focalization-01.** Focalization is substrate-dialect. Upper
  dialects consume the reader-state projection through queries.
  A Dramatic verifier may ask "at the midpoint, is the
  focalizer's state aligned with the Argument's protagonist?" —
  a query over the substrate's focalization-shaped reader
  projection.

## The dialect stack

The architecture admits an open graph of dialects with a single
sink (the substrate). A sketch-01 enumeration is illustrative,
not prescriptive:

```
    (prose — output, not managed)
          ↑ lowering to words
    ┌─────────────────┐
    │    Substrate    │  events, props, folds, descriptions,
    │                 │  identities, rules
    └─────────────────┘
          ↑ lowering
    ┌─────────────────┐
    │   Structural    │  acts, beats, plot points, pacing
    └─────────────────┘
          ↑ lowering
    ┌─────────────────┐
    │    Dramatic     │  argument, throughlines, character
    │                 │  functions, Story Mind
    └─────────────────┘
          ↑ (possibly more)
```

This enumeration — substrate / structural / dramatic — is one
plausible stack. Others are equally admissible:

- A single "craft" dialect above the substrate, collapsing
  structural and dramatic.
- A Save-the-Cat-specific "beat-sheet" dialect parallel to the
  Structural dialect, binding directly to the substrate.
- A Dramatica-full dialect bypassing a generic Dramatic layer
  entirely, with its own schema for throughlines, quads, and
  dynamic/static story points.
- An author-defined dialect specific to a project's conventions.

The architecture does not legislate. Each dialect is its own
sketch with its own A3 justification and its own grid-snap
discipline. Architecture-02's commitment is that the *shape* is a
stack (strictly: a DAG) of distinct dialects with the substrate
as the sink.

### What "dialect" means, precisely

A dialect is:

1. A set of **record types** (analogous to `Event`, `Prop`,
   `Description` in the substrate).
2. A **description surface** for those records, following
   descriptions-01's pattern.
3. A **query surface** — functions that answer questions about
   the dialect's records.
4. A **grid-snap discipline** — which facts are structural
   (record fields, predicate vocabulary) and which are
   interpretive (descriptions). Per A1 / A3.
5. A **lowering relation** to at least one other dialect in the
   stack (except the substrate, which is the sink; the substrate
   is lowered into prose by craft, not by the engine).
6. A **verification layer** at each outgoing boundary, implemented
   in the dialect's own vocabulary, evaluated against the lower
   dialect's queries + lowerings.

What a dialect is *not*:

- A schema extension to the substrate. Dialects are
  independent; their records do not subclass or reference
  substrate record types directly. Lowerings carry the binding.
- A rendering layer. Rendering to prose is below the substrate
  and not part of the dialect stack.
- A theory. Dialects do not make claims about what good
  stories are. They are vocabularies; templates within a dialect
  (e.g., "the three-act structure" as a Structural template)
  are separate from the dialect itself.

## Lowering records

A `Lowering` is an authored record that binds an upper-dialect
record to the lower-dialect records that realize it. The sketch
commits to the *existence* and *role* of lowerings; exact fields
are a dialect-boundary or dedicated lowering-sketch concern.

### Sketch-level shape

```
Lowering {
    id
    upper_record            { dialect, id }
    lower_records           [ { dialect, id }, ... ]
    authored_by
    τ_a
    annotation              (human-readable binding rationale)
    metadata                (per-boundary; dialect-specific)
}
```

Notes:

- `lower_records` is a tuple, not a singleton. One upper record
  may realize in many lower records (an Argument spans many
  events); the multiplicity is intrinsic to the binding.
- A single lower record may be the target of several lowerings
  from different upper records. An event that realizes both an
  inciting incident (Structural) and a character-introduction
  beat (Dramatic) is named twice — once per binding. The engine
  keeps each binding separate.
- Annotation is human-readable prose explaining *why* the
  binding is claimed. The verifier reads the structural side;
  the annotation is for the author and for reader-model
  partnering.

### What a Lowering is *not*

- A compilation target. The lower records exist independently;
  lowering does not produce them. Lowering is an *annotation*
  that says "these lower records realize this upper record."
- Strict. A single lowering is one author's claim; others may
  disagree. Disagreement lives in review entries on the
  lowering, not in the lowering itself.
- Lossless. The upper record carries information the lower
  records do not (the Argument's premise may have no substrate
  realization beyond an emergent pattern); conversely, the
  lower records carry information the upper record ignores.
  Lowering is a partial map.

### Lowering staleness

If either side of a lowering is edited — a new Act record
replaces an old one, or the substrate events it binds to are
revised — the lowering may become stale. Staleness follows the
descriptions-01 model: the lowering's `anchor_τ_a` (the max τ_a
of its bound records at the time of authoring) is compared to
their current τ_a; divergence surfaces as a staleness signal
via the verifier. No automatic re-binding.

## Verification at dialect boundaries

For each pair of adjacent dialects with authored lowerings, a
verifier reads lowerings + upper records + lower records and
emits observations.

### Verifier shape (conceptual)

```
verify(
    upper_records,
    lower_records,
    lowerings,
    upper_query_surface,
    lower_query_surface,
) -> list[Observation]
```

Where `Observation` is:
- a `ReviewEntry` on the lowering itself, with verdict
  (`approved` / `needs-work` / `noted`) and a comment;
- an `EditProposal` on the lowering's annotation, if the
  verifier finds the annotation doesn't match the realization;
- an `AnswerProposal` if the upper record has an authorial-
  uncertainty question the verifier can speak to;
- a new kind of entry, `StructuralAdvisory`, for observations
  not attached to a specific description (e.g., "this Act has
  three lowerings; the middle one has no substrate realization
  that changes any fold state").

The first three absorb into the existing proposal queue
unchanged. The fourth is a new shape this sketch flags but does
not formalize; a dedicated sketch per dialect boundary can
specialize it.

### Verifier primitives

A verifier's checks are expressed in terms of:

1. **Upper-record structure.** Shape of the record (fields
   present, conforming to dialect schema).
2. **Lowering coverage.** Does every upper record have at least
   one lowering? Does the lowering point at lower records that
   exist?
3. **Realization signature.** For each upper record, a dialect-
   specific check that the lower records exhibit the structural
   signature the upper record claims. "Inciting incident" may
   require a detectable state-change-in-focalizer's-held-set
   event in the substrate; "midpoint reversal" may require a
   specific kind of epistemic inversion between protagonist and
   antagonist; "Argument: knowledge begets suffering" may
   require that the protagonist's GAP-close on their fatal flaw
   precedes a world-state change that instantiates the premise.

The realization-signature checks are the load-bearing ones and
are dialect-specific. Architecture-02 does not enumerate them;
each dialect sketch does.

### Verification is not enforcement

A verifier's output is observation, never error. An upper record
with no lowering produces an observation ("no substrate
realization bound to this Argument"); the author decides whether
that's a problem or a deliberate choice (some Arguments may be
emergent from the whole story with no single substrate slice
realizing them). An upper record whose realization fails the
signature check produces an observation; the author decides
whether to revise the realization, revise the upper record, or
accept the mismatch.

This is A5 / A11 reasserted: the partner reads, judges, emits;
the author decides.

## Cross-boundary reader-model partnering

The reader-model probe's existing pattern (reader-model-01)
generalizes:

- At the substrate/description boundary, the probe reads the
  `ReaderView` (substrate folds + descriptions) and emits
  reviews, answer proposals, edit proposals.
- At the Structural/Substrate boundary, a probe reads Structural
  records + lowerings + substrate view and emits:
  - Reviews on lowerings (does this inciting-incident binding
    read honestly?).
  - Proposals for lowering annotations when they're weak or
    missing.
  - Answer proposals for authorial-uncertainty descriptions on
    Structural records ("I'm not sure this counts as a
    midpoint").
  - Edit proposals for Structural record text (description text
    attached to an Act).

The invocation pattern is the same: declared scope, typed I/O,
partner-not-fallback, shared review-entry type, anchor-τ_a
staleness (R1–R6 generalized). Each boundary's probe is a
parameterization of the same machinery.

This is A11 in practice: reader-model is not substrate-specific;
it is boundary-agnostic.

## Worked example: Oedipus with a minimal Dramatic dialect

Concrete illustration, deliberately thin on the Dramatic-dialect
details (those are sketch-per-dialect).

### Dramatic records (illustrative)

```
Argument {
    id = "A_oedipus_argument"
    premise = "knowledge of self is the unmaking of self"
    resolution_direction = "tragic"
    authored_by = "author"
}

Throughline {
    id = "T_oedipus_protagonist"
    role = "protagonist"
    entity_id = "oedipus"    # points at substrate.Entity
    authored_by = "author"
}
```

### Lowering records

```
Lowering {
    id = "L_argument_to_substrate"
    upper_record = { dialect: "dramatic", id: "A_oedipus_argument" }
    lower_records = [
        { dialect: "substrate", id: "E_oedipus_anagnorisis" },
        { dialect: "substrate", id: "D_oedipus_anagnorisis_texture" },
        { dialect: "substrate", id: "D_anagnorisis_logical_payload" },
    ]
    annotation = "The Argument's premise is realized by Oedipus's
                  GAP→KNOWN transition on his own parentage and
                  prior actions, which closes at E_oedipus_
                  anagnorisis and whose payload is made legible by
                  the two descriptions."
    authored_by = "author"
    τ_a = 50000
}

Lowering {
    id = "L_protagonist_throughline_to_substrate"
    upper_record = { dialect: "dramatic", id: "T_oedipus_protagonist" }
    lower_records = [...]    # every substrate event and description
                             # focalized on or centered on oedipus
    annotation = "Oedipus is the protagonist; the throughline is
                  the fold over his held set across τ_d."
    authored_by = "author"
    τ_a = 50001
}
```

### Verification at the Dramatic/Substrate boundary

A Dramatic↔Substrate verifier reads these lowerings and asks,
for each:

- **Argument lowering.** The Argument's `resolution_direction =
  "tragic"` implies a signature: the protagonist's GAP closes,
  and the world state post-closure is worse (by some substrate-
  checkable criterion — e.g., a world-level `suffering`
  predicate derived from the inference-01 rule engine) than pre-
  closure. The verifier checks the signature against the lower
  records and the substrate fold at τ_s >= 13.
- **Throughline lowering.** The Throughline claims Oedipus is
  the protagonist. The verifier checks that (a) the lowering's
  lower records include a non-trivial fraction of events whose
  participants include oedipus, (b) oedipus's held set changes
  across more τ_d entries than any other entity, (c) the
  focalizer is oedipus (or omniscient) for a majority of the
  sjuzhet.

Observations:

- If the Argument's signature passes: `ReviewEntry(verdict=approved)`
  on the Lowering.
- If the Throughline's coverage criterion fails (say, the
  encoding actually centers on Jocasta): `ReviewEntry(verdict=
  needs-work)` with a comment explaining the coverage shortfall.
- If the verifier can't evaluate a signature because the
  required substrate predicate doesn't exist (`suffering` isn't
  defined): `StructuralAdvisory(noted)` flagging the missing
  vocabulary.

No errors. The author decides whether to revise the upper record,
revise the substrate, revise the binding, or accept the
observation.

### What this example does *not* commit to

- The exact fields of `Argument`, `Throughline`, `Lowering`.
  These are for the Dramatic-dialect sketch and the lowering-
  shape sketch.
- The Argument's signature criterion. "Protagonist's GAP
  closes, world state worsens" is one candidate; Dramatica's
  own vocabulary may prescribe a different signature; a
  Freytag-style arc prescribes another. Each is dialect-
  specific.
- Whether `resolution_direction = "tragic"` is in the record or
  in a description. A3 within the Dramatic dialect decides.

The worked example illustrates the *shape*; every detail is
pending its own sketch.

## Open questions

1. **OQ1 — Lowering-record shape.** The sketch-level shape above
   is a strawman. Outstanding: whether lowerings carry their own
   attention level (they're a kind of second-class
   description-meets-annotation); whether one lowering may bind
   multiple upper records to the same lower records (many-to-many);
   whether lowering deletion is distinct from lowering supersession.
   A dedicated `lowering-sketch-01` probably wants to own this.
2. **OQ2 — The dialect graph.** Architecture-02 admits a DAG of
   dialects above the substrate. Is that right, or should the
   graph be strictly linear (one chain from top to substrate)?
   DAGs admit Dramatica-plus-Structural concurrently; linear
   chains force authors to pick. The sketch favors DAG for
   optionality; a forcing function (author confusion, verifier
   cost) might narrow it later.
3. **OQ3 — Dialect-local inference.** A Dramatic-dialect record
   like `Throughline(role="protagonist")` may entail other
   Dramatic records (e.g., there must exist a corresponding
   `Throughline(role="antagonist")` for some Dramatica templates).
   Does the inference-01 machinery instantiate per-dialect, or
   does it remain substrate-only? The sketch defers to each
   dialect sketch; the general answer is likely "per-dialect
   instantiation, via the inference-01 Rule machinery in the
   dialect's vocabulary."
4. **OQ4 — Cross-dialect queries.** A verifier at the
   Dramatic/Substrate boundary phrases its checks in mixed
   language ("the Argument's premise holds at τ_s >= 13"). Is
   "at τ_s >= 13" a substrate-dialect query, or is the verifier
   a new dialect of its own? The sketch treats verifiers as
   *upper-dialect code that makes lower-dialect queries*; a
   future sketch may find that verifiers earn their own dialect.
5. **OQ5 — Template records within a dialect.** "Three-act
   structure" is a template in the Structural dialect;
   "Dramatica argument-with-four-throughlines" is a template in
   the Dramatic dialect. A template is a *constraint on how a
   story uses that dialect's records*. Is a template itself a
   record type within the dialect, or an external schema
   applied at verification time? The sketch defers.
6. **OQ6 — Lifting.** The sketch commits to one-way (author
   writes upper + lowering; verifier checks). A reader-model
   partner may *propose* upper records from lower ones ("this
   substrate slice reads as an inciting incident, add a
   Structural record and a lowering?"). The proposal flow
   exists (reader-model-01 + proposal queue); the question is
   whether any dialect wants to formalize lifting-beyond-
   proposals. The architecture leaves it open.
7. **OQ7 — Prose dialect.** Prose sits below the substrate. Is
   it worth naming prose as a dialect the engine doesn't
   manage, or leaving it entirely implicit? Naming it forces
   honest accounting of what the engine does *not* do.
8. **OQ8 — Verification cost and scheduling.** A full stack of
   dialects with rich lowerings could produce a verification
   pass that's expensive. When does verification run? On every
   commit, on demand, on a schedule? The sketch notes this as
   a tooling question, not a schema question.

## What happens next

1. **Pick the first dialect to sketch.** Candidates: a
   Structural dialect (acts, beats, plot points — McKee /
   Aristotelian-accessible), or a Dramatic dialect (argument,
   throughlines — Dramatica-influenced). My lean: start
   Structural, because (a) its vocabulary is more widely
   familiar to writers, (b) its verifier primitives are
   closer to substrate-queryable structural signatures, and
   (c) the Dramatic dialect will want to lower into Structural
   before lowering into substrate — so Structural comes first
   in the stack and probably in the sketch order.
2. **Sketch the lowering-record shape.** Either as
   `lowering-sketch-01` or as part of the first dialect sketch.
   Until it lands, any dialect sketch is working against a
   strawman.
3. **Sketch the verifier machinery, once or per-dialect.** The
   sketch commits to verifiers being dialect-specific in their
   checks; the *infrastructure* (how observations emit to the
   proposal queue, how verifier-partner invocations compose
   with reader-model-01) is cross-cutting and may earn its own
   sketch.
4. **Consider a `view/sjuzhet-visibility-sketch-01`** (banked
   earlier) before or alongside the first dialect sketch. That
   sketch's outcome — whether `ReaderView` exposes sjuzhet
   coordinates — affects which primitives verifiers can rely on
   at the Structural/Substrate boundary.
5. **Retire author-asserted `parricide` / `incest` in the
   Oedipus encoding** (inference-model-01's pending prototype
   work) before probing the first dialect sketch, so the
   verifier has the substrate's full rule surface to query
   against.
