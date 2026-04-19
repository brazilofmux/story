# Substrate effect shape — sketch 01

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (new topic — record-shape detail for the
effect sub-records substrate-sketch-05 §Event internals names but
does not structurally specify)
**Frames:** [substrate-sketch-05](substrate-sketch-05.md) (§Event
internals; the five required elements, including `effects` as "a
tuple of KnowledgeEffect and/or WorldEffect records"), [substrate-
sketch-04](substrate-sketch-04.md) (§Update operators — the
closed vocabularies this sketch formalizes), [identity-and-
realization-sketch-01](identity-and-realization-sketch-01.md)
(§Realization and identity — the primary consumer of
KnowledgeEffect's via-operator machinery; the "Held" fold record)
**Related:** [architecture-sketch-01](architecture-sketch-01.md)
A3 (drift discipline), [substrate-entity-record-sketch-01](
substrate-entity-record-sketch-01.md) (precedent for record-shape
design sketches; holder references below resolve to Entity ids);
[production-format-sketch-01](production-format-sketch-01.md)
§PFS2 catches real drift (the finding that named this sketch as a
forcing function)
**Superseded by:** nothing yet

## Purpose

Structurally specify the two effect kinds — `WorldEffect` and
`KnowledgeEffect` — that substrate-sketch-05 §Event internals
names (as "a tuple of KnowledgeEffect and/or WorldEffect records
... fold-visible output of the event") but does not shape-specify.
This gap was surfaced by production-format-sketch-01 §PFS2 catches
real drift and is the primary blocker for a clean Event schema:
without effect shapes, Event's `effects: tuple` is an untyped
hole in the spec.

**What this sketch closes.** The design-sketch-level
specification of effect records. The production-layer schema
follows separately (candidate: `production-format-sketch-03`,
bundled or split depending on whether Prop lands first).

**Derivation discipline.** The sketch is written from first
principles **and** from the existing commitments sketches-04/05
and identity-and-realization-sketch-01 already made. The Python
prototype's `WorldEffect`, `KnowledgeEffect`, and `Held`
dataclasses are a conformance check, not a template. Where the
sketches and Python disagree, the sketch wins; where the sketches
underspecify, the sketch makes a first-principles call and names
its open questions.

## Why now

- Production-format-sketch-01 §PFS2 named this sketch as a
  forcing function for `schema/event.json`.
- Effect shapes are load-bearing across the substrate: the two
  folds (`project_world`, `project_knowledge`) are defined in
  terms of applying effects; every typed verifier check that
  reads effects (LT2's retraction detector; MN2's
  knowledge-asymmetry predicate; EK2's interpersonal+outward
  predicate) depends on effect shape. A clean spec unblocks
  schema work; it also anchors verifier documentation.
- The full 16-operator vocabulary (6 diegetic + 5 narrative for
  the reader + the WorldEffect polarity) is already implicit in
  sketches-04/05 and identity-and-realization-sketch-01. No new
  semantics are introduced — the sketch makes explicit what the
  prior sketches committed to in prose.

## Scope — what the sketch covers

**In:**

- The two effect kinds WorldEffect and KnowledgeEffect, why
  they are two and not one, and why no more.
- WorldEffect's field shape — Prop-reference + boolean
  assertion polarity.
- KnowledgeEffect's field shape — holder-reference + Prop-
  reference + via-operator. **No `asserts` bool**; the via
  encodes direction.
- The closed vocabulary of via-operators at v1: six diegetic
  (Observation, Utterance-heard, Inference, Deception,
  Forgetting, Realization) and five narrative (Disclosure,
  Focalization, Omission, Framing, Retroactive-reframing), per
  substrate-sketch-04 §Update operators.
- Effect ordering within an event (tuple-positional; identified
  by index, consistent with descriptions-sketch-01's
  EffectLocatorAnchor (event_id + effect_index) variant).

**Out:**

- **Prop's own shape.** Prop is referenced here as a named
  proposition record whose structural specification lives in
  `substrate-prop-literal-sketch-01` (still pending). This
  sketch treats Prop as a type-by-name, the same way
  production-format-sketch-01's `schema/description.json` uses
  its `PropPlaceholder` $def. When Prop's sketch lands, both
  the effect schema AND the description schema consume it.
- **Held's shape.** Held is the fold-state record
  (`project_knowledge`'s output: per-agent set of propositions
  with slot + via + provenance) mentioned by identity-and-
  realization-sketch-01 but not shape-specified anywhere. Held
  is an OUTPUT of folding effects, not an effect kind. A
  future sketch (candidate: `substrate-held-record-sketch-01`)
  specifies it; for this sketch, it is enough that Held
  exists and that KnowledgeEffect's via values are the
  operators the fold dispatches on to compute Held.
- **Slot vocabulary.** Slots (Known, Believed, Heard,
  Suspected, Gap, Blank) are Held-level, not Effect-level. The
  fold assigns a slot; the effect does not. This sketch
  commits: Slot is derived from via, not stored on the effect.
- **The reader's projection shape.** The reader is an
  epistemic subject whose knowledge state is projected by the
  narrative via-operators. How the reader's state is
  represented at fold-output time (separately from a
  character-agent Held set? shared shape with one?) is
  substrate-reader-projection-sketch-01's work, not this
  sketch. For effect-shape purposes, the reader's KnowledgeEffect
  has the same three-field shape as a character-agent's — the
  via values are disjoint per sketch-05 K2, but the record
  shape is unified.
- **Trans-agent effects.** An observation event with multiple
  witnesses produces knowledge effects on each witness. The
  sketch's commitment: one KnowledgeEffect *per witness*, not
  one effect with a list-valued holder. Rationale in ES5.
- **Dispatch mechanics.** How the fold dispatches on via-
  operator to update Held state is fold-implementation concern,
  not effect-shape concern. An effect is a data record; the
  fold is machinery.

## First-principles commitments

Labels **ES** (Effect Shape).

### ES1 — Two effect kinds, justified by fold structure

Substrate-sketch-05 commits to two effect kinds without naming
why. This sketch commits the reason: **the two kinds map to
the two folds over the event log.**

- `project_world(fabula, τ_s, branch) → { Prop: bool }` — a
  per-branch-per-τ_s boolean truth assignment over
  propositions. World state is shared (agent-independent);
  every agent who witnesses a world-state change agrees that
  it happened, though they may or may not individually know.
- `project_knowledge(fabula, agent, τ_s, branch) → Held-set` —
  per-agent-per-τ_s set of held propositions (with slot, via,
  provenance). Knowledge state is per-agent; two agents in the
  same room can hold different knowledge states.

A WorldEffect updates the first fold. A KnowledgeEffect updates
the second. Each kind's shape reflects what its target fold
needs:

- The world fold needs a proposition and a truth-polarity
  (asserts / retracts).
- The knowledge fold needs a holder (whose fold), a
  proposition, and a via-operator (how the fold updates).

A single effect kind would either have to merge the two folds
(not useful — they serve different queries) or carry optional
fields for both axes (worse — fields that only make sense for
one kind are noise when the effect is the other kind). Two
kinds, split at the fold boundary, is the clean shape.

**Why no third kind.** Substrate-sketch-05 F1-retirement
removed emotional-state and tension-state projections as
fold-visible. Any further projection (affect, suspense,
curiosity) lives on Descriptions or is computed as a query
(Sternberg queries per sketch-04 §Sternberg's interests as
queries), not produced by a third effect kind. If a future
design sketch reopens a third fold (unlikely given F1-
retirement), this sketch re-opens; until then, two.

### ES2 — WorldEffect shape

Three-field record:

- **`prop`** — a `Prop` record (defined by
  `substrate-prop-literal-sketch-01`, pending). The proposition
  whose truth this effect changes.
- **`asserts`** — a boolean. `True` means this effect asserts
  `prop` into world state (prop becomes true at the effect's
  event's τ_s on the effect's event's branches); `False` means
  this effect retracts `prop` (prop becomes false / is
  untrue-claimed). Default: True. An effect with `asserts=False`
  is the *retraction* instance LT2 detects when looking for
  convergence signals in pressure-shape-taxonomy-sketch-01+03.

No other fields. World state is a boolean-valued function over
Prop; a WorldEffect is a (Prop, polarity) pair. Everything else
(whose event, which branches, what τ_s) comes from the
containing Event record, not the effect.

**Why no explicit τ_s on the effect.** The containing Event
carries τ_s. An effect's timestamp is the event's timestamp. No
mechanism for effects-with-different-timestamps-within-one-
event — if the author needs two world-state changes at
different τ_s, that's two events. This keeps the fabula's
event-log ordering clean.

**Why no explicit branches on the effect.** The containing
Event carries a branch set. Effects inherit the event's branch
scope. An effect that applies on a different branch-set from
its own event is architecturally incoherent — the event is the
authoring unit.

### ES3 — KnowledgeEffect shape

Three-field record:

- **`holder`** — an Entity id (string) referencing the agent
  (kind="agent") whose knowledge state is updated. Per
  substrate-entity-record-sketch-01 SE3, only `kind="agent"`
  entities participate in K1; a KnowledgeEffect whose holder
  resolves to a non-agent Entity is an error surfaced by
  verifier machinery, not a well-formedness violation at the
  record level.
- **`prop`** — a `Prop` record. Same type as WorldEffect's
  prop field; Prop is the universal proposition type.
- **`via`** — a string from the closed via-operator
  vocabulary (ES4). The operator tells the fold *how* the
  holder gained (or, in the case of Forgetting, lost) this
  knowledge. The via encodes direction and provenance-kind
  simultaneously.

**No `asserts` field.** Knowledge is not a boolean-truth
projection; the via encodes the operator's effect on the
holder's Held-set. `Forgetting` is the sole retraction-like
operator in the diegetic vocabulary; it decays confidence / may
move a prop out of Held state, but the sketch does not commit
that Forgetting is literally a delete-from-set — that's fold-
implementation concern (see ES6 OQ).

**No explicit confidence-slot field.** Slots (Known, Believed,
Heard, Suspected, Gap, Blank) are fold-output state, not
effect-input. The fold determines a holder's slot for a prop
by accumulating effects by via; the effect does not declare
the slot.

### ES4 — Closed via-operator vocabulary at v1

Enumerated from substrate-sketch-04 §Update operators, verbatim:

**Diegetic via-operators** (apply to character-agents):

- `observation` — agent perceives an event in-world.
- `utterance-heard` — another agent tells this agent a
  proposition; the speaker is recoverable from the containing
  event's participants.
- `inference` — agent derives the proposition from current
  state via an inference model.
- `deception` — agent is told a proposition that is false on
  the relevant branch; the agent acquires it with normal
  provenance (unaware of the falsity). Distinct from
  `utterance-heard` because the authoring-time truth polarity
  differs.
- `forgetting` — the sole knowledge-decay operator; fold
  reduces confidence or moves the prop out of Held.
- `realization` — an existing proposition's substitutional
  consequences become newly accessible via an identity
  assertion (identity-and-realization-sketch-01 §Realization
  and identity). The *realized* prop is often an
  `identity(A, B)` proposition.

**Narrative via-operators** (apply to the reader):

- `disclosure` — the narration delivers a proposition to the
  reader directly.
- `focalization` — the narration routes reader access through
  a character-agent's perspective; the reader inherits that
  agent's Held state (modulo gaps where the focalizer is
  uncertain).
- `omission` — a proposition is withheld; creates a reader-
  blank or reader-gap.
- `framing` — a proposition is delivered with rhetorical
  coloring affecting reader confidence slot (a reliability
  discount, an intensifier).
- `retroactive-reframing` — a later narrative act causes the
  reader to re-interpret earlier material; propositions
  migrate between slots.

**The two vocabularies are disjoint.** A diegetic via-operator
applied to the reader is a category error; a narrative via-
operator applied to a character-agent is the same. The fold
dispatches on via AND on whether the holder is the reader or a
character-agent; invalid combinations are verifier-caught
(future work; not a record-level constraint).

**Closed, extensible by sketch amendment.** Adding a via value
requires:

1. Demonstrating that the new operator corresponds to a
   structural distinction neither fold (`project_world`,
   `project_knowledge`) currently handles — narratively rich
   operators that the fold doesn't need dispatch for belong
   in Descriptions, not in a new via.
2. Amending this sketch to add the value + its fold-dispatch
   semantics.
3. Amending the substrate-effect-shape production schema
   (future) to widen the enum.

Grid-snap in action: new via-operators require structural
justification, not narrative convenience.

### ES5 — One effect per holder

A single event with N witnesses produces N KnowledgeEffects, one
per witness — **not** one effect with a list-valued holder.

Why:

- **Per-witness divergence.** Different witnesses may acquire
  knowledge via different operators (one is the utterer,
  others are listeners; some are focalized-through, some are
  not). List-valued holder can't carry per-witness via.
- **Record simplicity.** A one-holder-one-prop-one-via shape
  is the minimal useful record; list-valued fields invite
  list-of-list complications (one holder for multiple props?
  multiple holders for multiple props with multiple vias?
  combinatorial explosion).
- **Fold simplicity.** `project_knowledge(agent, ...)` scans
  effects whose holder matches `agent`; the scan is a trivial
  filter. List-valued holders would need an `in` check per
  effect per agent per fold call — slower and more complex.

Corollary: an event asserting world-state changes that are
*also* visible to multiple agents carries one WorldEffect
(for the world-state assertion) plus one KnowledgeEffect per
witness (for their individual observations). The event's
effects tuple might contain 6 records: 1 WorldEffect +
5 observers' KnowledgeEffects. Per ES7, ordering in the tuple
is authored.

### ES6 — Effects are ordered within an event

An event's `effects: tuple` is positionally ordered. Within a
single event:

- Effects apply in tuple order when the fold processes them.
- An effect at index N applies after the effect at index N-1.
- The EffectLocatorAnchor variant of Description.attached_to
  (descriptions-sketch-01 §Required fields) uses
  (event_id, effect_index) to attach a description to a
  specific effect — presupposing index stability.

This means:

- Effect ordering within an event is author-authoritative.
- An event re-authored to reorder effects is an event edit;
  descriptions attached via EffectLocatorAnchor need index
  revalidation.
- A design pattern that asserts-then-retracts the same
  prop within one event is legal but unusual (why assert
  something just to retract it?); the sketch does not
  forbid but notes the oddity for authorial awareness.

### ES7 — Effect records are timeless at record level

Parallel to substrate-entity-record-sketch-01 SE5: an effect
record carries no τ_a, τ_s, or branch set. All temporal and
branch coordinates come from the containing event. Retract-ing
an effect means authoring a new event with `asserts=False`
(WorldEffect) or an appropriate via (KnowledgeEffect); editing
the original effect in place is not the mechanism.

This matches the append-only event-log architecture (E1 in
sketch-04/05): history is authored by additional events, never
by mutating prior ones.

## Worked examples

### WorldEffect — Woodcutter steals the dagger (Rashomon)

```
WorldEffect(
    prop=Prop(predicate="stole",
              args=("woodcutter", "dagger")),
    asserts=True,
)
```

Plus, on the same event:

```
WorldEffect(
    prop=Prop(predicate="at_location",
              args=("dagger", "woodcutter")),
    asserts=True,
)
```

The event `E_wc_theft` on branch `:b-woodcutter` emits these
two WorldEffects (and a KnowledgeEffect for the woodcutter
himself). The fold produces:
- `project_world(τ_s ≥ wc_theft_τ_s, :b-woodcutter)` includes
  `stole(woodcutter, dagger)` and `at_location(dagger,
  woodcutter)`.

### WorldEffect — Retraction (enabling)

Pressure-shape-taxonomy-sketch-03 LT12a names
`bound_to(husband, tree)` retraction as an example of an
enabling retraction (constraint-removal). The retracting event
carries:

```
WorldEffect(
    prop=Prop(predicate="bound_to",
              args=("husband", "tree")),
    asserts=False,
)
```

`asserts=False` is the polarity. LT12's enabling-vs-restricting
classification is a verifier pattern *over* retractions — the
classifier consumes the effect's (prop, asserts=False) pair and
the surrounding event context. Polarity is record-level; the
classification is verifier-level.

### KnowledgeEffect — Oedipus realizes his identity

Per identity-and-realization-sketch-01 §Worked example: the
event `E_oedipus_anagnorisis` carries:

```
KnowledgeEffect(
    holder="oedipus",
    prop=Prop(predicate="identity",
              args=("oedipus", "stranger_at_crossroads")),
    via="realization",
)
```

Plus a parallel effect for Jocasta (if she is also present; in
the Oedipus case Jocasta has a separate realization event
earlier). The fold projects Oedipus's Held-set at τ_s ≥
anagnorisis_τ_s to include `identity(oedipus,
stranger_at_crossroads)` at slot Known, via=realization.

### KnowledgeEffect — Alice hears about the locket (sketch-04 §E3)

Per sketch-04 §Fabula events E3: Bob tells Alice the locket
was his grandmother's.

```
KnowledgeEffect(
    holder="alice",
    prop=Prop(predicate="owner_of",
              args=("locket", "bobs_grandmother")),
    via="utterance-heard",
)
```

The speaker (Bob) is recoverable from the utterance event's
participants (`speaker="bob"`, `listener="alice"`); the
KnowledgeEffect does not duplicate it. The fold's downstream
machinery determines Alice's confidence slot for the prop
based on via="utterance-heard" (probably Believed rather
than Known absent further signals).

### KnowledgeEffect — Reader's disclosure-acquired fact

The narrator discloses E4 directly to the reader. The effect
structure:

```
KnowledgeEffect(
    holder="reader",
    prop=Prop(predicate="took_from",
              args=("bob", "locket", "charlies_drawer")),
    via="disclosure",
)
```

The holder "reader" is the distinguished reader-agent Entity
(substrate-sketch-05 §Entities: "the reader is an agent of a
distinct kind"). The via "disclosure" is from the narrative
vocabulary — invalid for character-agent holders, valid for
the reader.

## Not in scope

See §Scope "Out". Key re-emphases:

- **Prop's field shape.** Out. Prop is a named type reference
  whose shape lives in `substrate-prop-literal-sketch-01`.
- **Held's field shape.** Out. Held is fold-output, not
  effect-input; defer to a Held-specific sketch.
- **Slot vocabulary.** Out. Slot is derived by the fold from
  via; it is not an effect field.
- **Fold-implementation mechanics.** Out. How the fold processes
  via=observation vs. via=forgetting to update Held-state is
  the fold's concern; the effect record is input data.
- **Per-effect τ_s / τ_a / branch.** Out. Effects inherit from
  their containing event (ES7).
- **List-valued holder on KnowledgeEffect.** Out. One effect
  per holder (ES5).

## Open questions

1. **OQ1 — Is Forgetting literally a Held-set deletion, or a
   confidence-decay operation?** The sketch commits to `via="forgetting"`
   as a valid operator but does not specify the fold's response.
   Sketch-04 §Update operators says "confidence decays; a
   proposition moves toward or out of the state", which is
   deliberately non-committal. A future sketch pinning down the
   fold (candidate: `substrate-knowledge-fold-sketch-01`)
   decides. For now: via="forgetting" is legal; downstream
   fold behavior is deferred.
2. **OQ2 — Can a KnowledgeEffect be retracted?** ES3 commits
   there is no `asserts` bool on KnowledgeEffect. But suppose
   an author wants to re-author an event (retcon) and undo a
   KnowledgeEffect that was on it. Per ES7, effects are
   timeless; retcon re-authors the containing event under a
   new τ_a. The prior event is still in the append-only log;
   the new event replaces (via superseded-event machinery that
   sketch-05 alludes to but does not specify). So
   KnowledgeEffect retraction = event supersession, not effect-
   level polarity. Reopens if a forcing function surfaces (a
   encoding that needs intra-event knowledge retraction).
3. **OQ3 — How is the reader's holder id represented?** ES4
   names "reader" as a distinguished holder value for narrative
   via-operators. Is the reader an Entity record with
   `id="reader"` and `kind="agent"`? Or a distinguished
   off-Entity-list identifier? Sketch-05 says "the reader is an
   agent of a distinct kind" (sketch-05 K2); the cleanest
   interpretation is that the reader IS an Entity with
   `kind="agent"` and a reserved id like `"reader"` per
   encoding. This interacts with substrate-entity-record-
   sketch-01 SE3's kind enum (does "reader" deserve its own
   value?); the sketch defers the call. Banked.
4. **OQ4 — Per-prop retraction polarity on WorldEffect.** ES2's
   `asserts: bool` assumes every Prop is boolean-truth-valued.
   What about a fuzzy predicate (`believes_partially(X, p, 0.4)`)
   whose "retraction" would be decay? The sketch commits:
   fuzzy predicates live in Descriptions (grid-snap: structural
   predicates are atomic; shades of belief are interpretive).
   A future encoding forcing fuzzy world-state would re-open.
5. **OQ5 — Group effects.** ES5 commits one effect per holder.
   What about a world-scale event where 500 soldiers all
   observe the battle? 500 KnowledgeEffect records per event
   would bloat. Pragmatically: large-cast events don't appear
   in the current corpus; when they do, a sibling `GroupKnowledgeEffect`
   with a participant-role-filter would be a reasonable
   extension (e.g., "every participant with role=witness
   acquires this prop via=observation"). Banked; no forcing
   function today.
6. **OQ6 — Can one effect's prop reference another effect's
   effect?** (E.g., an inference effect whose prop cites the
   observation effect it follows from.) The sketch's shape
   says no: effects carry propositions (via Prop), not
   effect-references. If an author wants to model inference-
   chain provenance, that's a description concern or a future
   metadata extension. Banked.

## Discipline

- **Shape-before-schema.** This sketch is a design-level spec
  for a record; the production-format schema follows in
  `production-format-sketch-03` (or equivalent). Any attempt
  to write `schema/event.json`'s effect sub-schemas without
  grounding in this sketch re-introduces Python-as-spec drift.
- **Closed enum + extension protocol.** Via-operator values
  grow by sketch amendment, not per-encoding invention. Same
  grid-snap discipline substrate-entity-record-sketch-01 SE3
  established for kind.
- **The effect carries only what the fold needs.** Additional
  fields require a named fold-consumer. A field that "feels
  right" (an effect-level authored_by? an effect-level
  timestamp?) but has no fold-level consumer is drift.
- **Prop is a type reference.** This sketch names Prop; it does
  not define it. When substrate-prop-literal-sketch-01 lands,
  both this sketch's schemas AND descriptions-sketch-01's
  proposition-anchor schema consume it.

## Summary

Record-shape sketch for the two effect kinds
substrate-sketch-05 §Event internals names but does not
structurally specify. First-principles derivation keyed to the
two folds — `project_world` and `project_knowledge` — that
define the shape-need.

- **WorldEffect:** `(prop, asserts)`. Two fields. Polarity is
  a bool because world state is boolean-truth.
- **KnowledgeEffect:** `(holder, prop, via)`. Three fields.
  Polarity / direction are encoded in via; the via operator
  vocabulary is closed at 11 values (6 diegetic + 5 narrative)
  from substrate-sketch-04 §Update operators. No `asserts`
  bool.
- **Effects inherit the containing event's τ_s / τ_a /
  branches** (ES7). Timeless at record level; temporal
  coordinates come from events.
- **One effect per holder** (ES5). N witnesses = N
  KnowledgeEffects, not one list-valued effect.

Unblocks the effect sub-schema work that
`production-format-sketch-03` (candidate) will need. Does NOT
unblock the full Event schema — Prop shape
(`substrate-prop-literal-sketch-01`) is the remaining gate.

Six OQs banked with explicit forcing-function criteria. No
substrate or dialect record change forced by this sketch; the
existing corpus's effects validate every commitment ES1–ES7
(conformance surface belongs to the production-format sketch,
not here).

The sketch's load-bearing discipline: **the effect carries
exactly what the fold needs to consume it, no more.** Grid-
snap at the record level; fold-structure justification for every
field.
