# Substrate entity record — sketch 01

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (new topic — record-shape detail for an
ontological commitment substrate-sketch-05 §Entities made at the
ontology level)
**Frames:** [substrate-sketch-05](substrate-sketch-05.md)
(§Entities, §The three time axes, K1 knowledge-projection fold),
[architecture-sketch-01](architecture-sketch-01.md) (A3 drift
discipline), [architecture-sketch-02](architecture-sketch-02.md)
(grid-snap discipline — schema grid-snaps structural facts)
**Related:** [descriptions-sketch-01](descriptions-sketch-01.md)
(the precedent for record-shape-specific sketches;
descriptions-sketch-01 does for Description what this sketch does
for Entity), [production-format-sketch-01](production-format-
sketch-01.md) §PFS2 catches real drift (the finding this sketch
is written to resolve); [identity-and-realization-sketch-01](
identity-and-realization-sketch-01.md) (consumer: identity
resolution uses Entity id equivalence classes)
**Superseded by:** nothing yet

## Purpose

Structurally specify the Entity record. Substrate-sketch-05
§Entities commits to Entity **ontologically** — "anything
referred to by the story. Agents are a subtype." — but does
not enumerate the Entity record's fields. That gap was caught by
production-format-sketch-01's PFS2 discipline during its
implementation pass: writing a schema for Entity from sketches
alone yielded near-emptiness, because the sketches simply do not
specify Entity structurally.

This sketch closes the gap. It is a companion-shape sketch to
descriptions-sketch-01 in the substrate layer: where sketch-05
made the ontological commitment, this sketch makes the
record-level commitment. A canonical schema
(`schema/entity.json`) follows under production-format-sketch-02.

**Derivation discipline.** The sketch is written from substrate
first-principles — what the substrate's machinery needs to know
about a referable thing — not from the Python prototype's
existing `Entity` dataclass. The prototype is a conformance
check, not a template. When the sketch disagrees with the
Python, the Python is the side that needs to change.

## Why now

- Production-format-sketch-01 §PFS2 catches real drift named
  this sketch as the forcing function for unblocking
  `schema/entity.json`.
- The dialect stack has three Entity-consuming layers actively
  in flight: the substrate's K1 knowledge fold (agents have
  knowledge-state), the at_location / unity-of-place checks
  (locations are a distinct substrate concern), and the
  identity-resolution machinery (identity-and-realization-
  sketch-01; abstract-kind entities function as identity
  handles). A record-level spec keeps these three consumers
  honest about what they depend on.
- The current corpus has 83 Entity records across 5 encodings
  exercising all four `kind` values — enough data to sanity-
  check any first-principles claim the sketch makes.

## Scope — what the sketch covers

**In:**

- The Entity record's required and optional fields.
- The `kind` vocabulary and the structural significance of
  each value.
- Identity scope (per-story; id stability semantics).
- Temporal coordinates (the sketch's explicit claim: Entity
  records are *timeless* at record level; presence in the
  fabula is time-coordinated by the events that reference the
  entity).
- Subtype-as-discriminator vs. subtype-as-inheritance (the
  sketch's explicit claim: Agent is not a subtype-record of
  Entity; Agent is "an Entity with `kind="agent"`").

**Out:**

- Cross-work identity semantics (is "oedipus" in Oedipus the
  same as a hypothetical "oedipus" in a sequel?). OQ1.
- Cross-dialect reference patterns (the Aristotelian dialect's
  ArCharacter uses `character_ref_id` to point at an Entity id;
  whether this pattern becomes a first-class part of every
  dialect's vocabulary). OQ4.
- Refinement of the `abstract` kind (the corpus exposes that
  `abstract` entities often function as identity-resolution
  handles, e.g., "the stranger who killed Laius" — a concept
  that later resolves to Oedipus). Whether this is its own kind
  or a sub-case of `abstract`. OQ3.
- Richer Agent-specific structure (would Agent records ever
  carry authored-at-record-level state?). The sketch's claim:
  no — agent knowledge is derived by the K1 fold, not stored on
  the Agent record. Reopens if a future encoding forces.
- Record-level τ_a for Entity. The sketch's claim:
  unnecessary — see SE5 below.

## First-principles commitments

Labels **SE** (Substrate Entity record).

### SE1 — Entity is a referable thing, nothing more at record level

An Entity is *any referable thing in a story*: a character, a
place, a physical object, an abstract concept. At the record
level, Entity is exactly what is needed to serve as the target
of a reference from events, descriptions, and upper-dialect
records: a stable handle, a display string, and a kind
discriminator that names what *sort* of referable thing this is
so the substrate's machinery can treat it appropriately.

The record does not carry:

- State (knowledge, location, possession) — state is derived
  from the event log via K1 and other folds (substrate-sketch-
  05).
- Affect (feelings toward other entities, reputation) — this
  is interpretive content living on Descriptions per
  architecture-sketch-01 A2.
- Narrative significance (protagonist / antagonist / foil) —
  dialect-layer concerns (Dramatic's Character record,
  Aristotelian's ArCharacter).

The record *only* carries what is structurally required for
references to resolve and for the substrate's kind-conditioned
machinery to dispatch correctly.

### SE2 — Three required fields

An Entity is exactly three required fields:

- **`id`** — a string. Stable identifier scoped per-story.
  Matches the shape sketch-05 §Entities assumes when describing
  agent ids, event-participant bindings ("dict from role-name
  to entity-id"), and similar.
- **`name`** — a string. The display handle the author and
  downstream tooling use when rendering this Entity in prose,
  review interfaces, or probe prompts. Required because every
  referable thing a story bothers to reference has *something*
  to be called, even if that something is "the crowd" or "the
  oracle" or "fate itself". Corpus survey confirms: 83/83
  entities across 5 encodings carry a non-empty name.
- **`kind`** — a string from the enumerated vocabulary at SE3.
  The kind discriminator is the substrate's dispatch hook: K1
  fold considers only `kind="agent"` entities; unity-of-place
  checks (aristotelian-sketch-01 A6) consider only
  `kind="location"` entities; identity resolution (identity-
  and-realization-sketch-01) operates heavily on
  `kind="abstract"` entities.

No optional fields. The three-field shape is complete for v1.

### SE3 — kind vocabulary (closed, extensible by sketch amendment)

The vocabulary at v1:

- **`"agent"`** — anything that holds knowledge and can
  witness or perform events. K1 knowledge-projection fold
  considers only agents. Characters, the reader, anyone whose
  knowledge-state matters for the fabula.
- **`"location"`** — a place. Can be the target of
  `at_location(entity, location)` propositions; subject to
  unity-of-place checks. Distinguishing locations from
  non-location entities is structurally necessary because the
  substrate's `at_location` predicate admits location-entities
  only as the second argument.
- **`"object"`** — a physical non-agent thing. No knowledge
  state; not a location; can be possessed, moved, broken,
  inscribed. The sword, the dagger, the letter.
- **`"abstract"`** — a referable entity that is not physically
  located or agent-like. Identity-referential concepts ("the
  stranger who killed Laius"); authorial-pointer handles ("the
  bicentennial title fight"); conceptual things events refer to
  but which have no physical location and no agency. The
  substrate admits abstract entities as reference targets but
  does not dispatch machinery on them the way it does for agent
  / location. They are the "everything else" bucket for
  referability.

**Why these four and no more.** Each of `agent`, `location`,
`object`, `abstract` corresponds to a structural distinction
the substrate already makes, not to a narrative concept:

- `agent` vs. everything else: K1 fold.
- `location` vs. everything else: `at_location` predicate
  + unity-of-place.
- `object` vs. `abstract`: the substrate does not dispatch on
  this distinction at present. The split is authorial — "the
  dagger" vs. "the prophecy" are both reference-targets with no
  kind-conditioned substrate machinery. They are kept distinct
  because downstream dialect-layer machinery (e.g., a future
  prose-export tool) might render objects and abstracts
  differently, and because collapsing them into one "non-agent-
  non-location" bucket would lose meaningful authorial
  distinction.

**Closed, extensible by sketch amendment.** The enum is fixed
at four values in this sketch. An encoding that wants a fifth
kind (`supernatural`? `collective`? `narrator`?) must:

1. Demonstrate that the new kind corresponds to a structural
   distinction the substrate (or a dialect) can dispatch on.
   A kind that merely narrates something ("this entity is
   mythological") is not structural — a description with
   `kind="texture"` serves that purpose. A kind that lets the
   substrate treat references differently ("supernatural
   entities are witnesses but cannot be `at_location`'d") is
   structural.
2. Amend this sketch to add the value + its structural rationale.
3. Update `schema/entity.json` (or its successor) to admit the
   value.

The discipline is parallel to descriptions-sketch-01 §Extension
rule. Grid-snap in action: new schema values require structural
justification, not narrative convenience.

### SE4 — Agent is a subtype-as-discriminator, not
subtype-as-inheritance

Substrate-sketch-05 §Entities says "Agents are a subtype" of
Entity. This sketch commits: "subtype" here means *discriminator
value*, not *record-shape specialization*. An Agent record is
an Entity record with `kind="agent"`. There are **no
Agent-specific fields** at the substrate record level.

Why this choice:

- **Agent state is derived, not stored.** Substrate-sketch-05
  K1 commits that an agent's knowledge is projected from the
  event log. The Agent record does not carry a knowledge field
  — if it did, the field would need authoring, validation, and
  staleness tracking, and the derived fold would still be the
  source of truth. The Agent record is a referable identity; the
  fold answers "what does this agent know?".
- **Cross-dialect reference stays simple.** Dialect-layer
  records (Aristotelian's ArCharacter, Dramatic's Character)
  point at Agent entities by id. A single Entity record shape
  (with kind discriminator) means cross-dialect references don't
  branch on "is this an Agent or just an Entity?".
- **Future Agent-specific state, if ever needed, lives in
  events.** A knowledge-revealing event emits effects that the
  fold integrates. A possession-establishing event emits
  world-state effects. None of these require new record-level
  Agent fields.

The claim is falsifiable: if a future encoding needs a field
that makes sense only for agents (some intrinsic property that
is not derivable from the event log and that only agents have),
this sketch needs amendment. As of the current 5-encoding
corpus, no such field is forced.

### SE5 — Entity records are timeless at record level

An Entity record has no `τ_a`. An entity's **presence in the
fabula** is a function of the first event that references it;
its **stability in the fabula** is a function of events that
continue to reference it. The record is a timeless referential
handle.

Why this choice:

- **Authoring an entity is cheap; referencing it is what
  matters.** Adding an entity to the story's ENTITIES list
  without referencing it in any event is vacuous. Conversely,
  the first time an event references the entity, the entity
  effectively exists at that event's `τ_s` — which is
  substrate-visible via the event's own coordinates.
- **Retcon is handled by branches, not record editing.**
  Substrate-sketch-04 §Branch representation handles retcon
  via branch branching and authored-time flagged events. If an
  author wants to retract an entity (say, Jocasta was
  originally a different person), the retraction is a branch-
  level operation on the events that reference Jocasta, not a
  record-level edit of the Jocasta Entity.
- **Simplicity.** Every field the substrate adds to Entity
  becomes a coordinate the fold must track. Timeless records
  are smaller.

The claim is falsifiable: if a future need for record-level
entity versioning appears (e.g., "this entity's name changed
between draft and final"), this sketch is amended. Current
corpus does not force.

### SE6 — Identity scope is per-story

An Entity's `id` is stable and unique **within one story**.
Across stories, an id collision carries no cross-story
semantics. Two stories both naming an Entity "oedipus" are
*not* claiming the same referent — the substrate offers no
machinery to equate them.

If cross-story identity becomes a real concern (a story
universe with shared characters; a sequel whose protagonist is
canonically the same person as the original's), a follow-on
sketch adds an explicit cross-story identity layer (candidate:
`cross-work-identity-sketch-01`). Until forced, identity is
per-story-local.

## Worked examples — Entity records under SE1–SE6

### Oedipus

```
Entity(id="oedipus", name="Oedipus", kind="agent")
Entity(id="jocasta", name="Jocasta", kind="agent")
Entity(id="the_stranger_oedipus_killed",
       name="the stranger Oedipus killed at the crossroads",
       kind="abstract")
Entity(id="thebes", name="Thebes", kind="location")
Entity(id="apollo", name="Apollo", kind="agent")
```

Notes:

- `oedipus` and `jocasta` are agents — their knowledge states
  matter (peripeteia at the messenger's reveal; anagnorisis at
  the shepherd's testimony).
- `the_stranger_oedipus_killed` is an `abstract` entity — a
  referential handle that *later* resolves, via identity-and-
  realization-sketch-01 machinery, to equal `laius`. This is
  the archetypal use of `abstract`: an identity-referential
  concept the work has, which resolves through events.
- `apollo` is `agent` because Apollo's knowledge is treated as
  authoritative in the prophecy-chain — he "knows" before
  anyone human does. A different encoding might choose
  `abstract` for Apollo-the-concept; the author's call.

### Rashomon

Four named humans (Tajomaru, Wife, Husband, Woodcutter) plus
the witness frame (Priest, Commoner) as agents. One location
dominates (the grove); the forest road and the gate each appear.
A few objects (sword, dagger). No abstract entities in the
current encoding — Rashomon's contested-knowledge structure
lives in branches, not identity-resolution handles.

### The abstract-kind pattern across the corpus

Across 5 encodings, `abstract` is used 5 times. Four of those
are identity-referential concepts ("the infant exposed on
Cithaeron" → later resolves to the adult Oedipus; "the
stranger who killed Laius" → later resolves to Oedipus). One
(Rocky's "the bicentennial title fight") is an authorial-
pointer handle — a referable event-concept the encoding can
bind to, distinct from any Event record for the fight itself.

**Both patterns are covered by the `abstract` kind at v1.** OQ3
revisits whether they should split into two kinds if the
distinction becomes structurally load-bearing.

## Not in scope

See §Scope "Out" above. Key re-emphases:

- **Agent's inheritance structure.** Agent is a discriminator
  value; no sub-record shape. SE4 commits explicitly.
- **Entity-level version history.** SE5 commits: Entity is
  timeless.
- **Cross-work identity.** SE6 commits: per-story-local.
- **Cross-dialect Entity-referencing patterns.** A dialect's
  choice to point at Entity (by id, as ArCharacter does) is
  the dialect's concern. Whether dialect-ref patterns should
  standardize is a future sketch.

## Open questions

1. **OQ1 — Cross-work identity.** Per SE6, identity is per-
   story. A project importing a second story (a Rocky sequel,
   a Macbeth stage adaptation alongside the substrate
   encoding) would want shared Entity references. Forcing
   function: a second story in the corpus that the author
   intends to share Entity references with an existing one.
   Candidate sketch: `cross-work-identity-sketch-01`.
2. **OQ2 — Richer Agent-specific state.** Per SE4, Agent has
   no intrinsic fields. Forcing function: an encoding that
   needs to carry agent-state not derivable from events (a
   persistent disposition, an intrinsic role). The current
   K1-fold-suffices claim holds; this OQ banks the alternative.
3. **OQ3 — `abstract` split.** The corpus exposes two sub-
   flavors: identity-referential handles ("the stranger who
   killed Laius") and authorial-pointer handles ("the
   bicentennial title fight"). Whether these need distinct
   kinds (`identity-handle` / `pointer-handle`?) depends on
   whether the substrate or a dialect ever dispatches on the
   distinction. Today: no. Banked.
4. **OQ4 — Cross-dialect reference patterns.** The Aristotelian
   dialect's ArCharacter points at an Entity via
   `character_ref_id`. Dramatic's Character does something
   similar via its own `owners` list. Whether this is a
   first-class pattern the substrate endorses (a standard
   `Entity_ref(entity_id, from_dialect, record_id)` record?)
   vs. per-dialect convention (what we have today) is open.
   Candidate sketch: `cross-dialect-entity-ref-sketch-01`.
5. **OQ5 — Name as structured.** Per SE2, name is a single
   string. A story with a character who has multiple names
   across the fabula (pre-reveal "the stranger" vs. post-
   reveal "Laius") handles this today by having two separate
   Entity records bridged by identity-resolution. An
   alternative: a single Entity with a list-of-names. The
   current single-string shape is simpler and matches how
   identity-and-realization-sketch-01 models reveals. Banked.
6. **OQ6 — Entity description attachment.** Descriptions-
   sketch-01 §The description record names five anchor kinds
   (event, effect, proposition, sjuzhet-entry, description).
   **Entity is not among them.** Can a Description attach to an
   Entity directly? Today: no, per descriptions-sketch-01's
   enumerated anchors. If the pattern becomes useful
   (descriptions on entities — "this character is flamboyant",
   as an Entity-level authorial note), descriptions-sketch-01
   gets an amendment to add an `entity` anchor variant. This
   sketch does not force it.

## Discipline

Process expectations for work against this sketch:

- **Record-level specification before schema.** This sketch's
  entire purpose is being the design-level specification the
  production-format-sketch-02 schema derives from. Any attempt
  to write `schema/entity.json` before (or without reference
  to) this sketch reintroduces the Python-as-spec drift
  production-format-sketch-01's PFS2 is meant to reverse.
- **Closed enum + extension protocol.** The `kind` vocabulary
  grows by sketch amendment, not by schema-widening or by
  per-encoding convention. Grid-snap enforced.
- **The record carries only what substrate machinery needs.**
  Additional fields require a named substrate consumer (a
  fold, a dialect-layer check, a production-format downstream)
  before they land. A field that "feels right" but has no
  substrate consumer is drift.

## Summary

A record-shape sketch for Entity. Fills the gap production-
format-sketch-01 §PFS2 caught. First-principles derivation:
Entity is a referable thing (id + name + kind), kind is a
closed four-value enum each value of which maps to a specific
substrate machinery dispatch, Agent is a discriminator value
not an inheriting subtype, the record is timeless at record
level (temporal presence is event-referenced), and identity is
per-story.

Unblocks `production-format-sketch-02` → `schema/entity.json`.
Six OQs banked, all with explicit forcing-function criteria.
No substrate or dialect record change forced by this sketch;
the existing 83-entity corpus validates every commitment SE1–
SE6 (conformance surface belongs to the production-format
sketch, not here).

The sketch's load-bearing discipline: **the substrate adds no
field without a named structural consumer.** Grid-snap at the
record level.
