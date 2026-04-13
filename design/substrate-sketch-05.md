# Substrate — sketch 05 (consolidated, A3-aligned)

**Status:** draft, active
**Date:** 2026-04-13
**Supersedes:** [substrate-sketch-04.md](substrate-sketch-04.md) (and its predecessors)
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md)
**Superseded by:** nothing yet

## Purpose

Consolidated statement of the substrate design, aligned with the
architectural commitments in [architecture-sketch-01.md](architecture-sketch-01.md).
Sketch 04 is kept as a historical record; this sketch is the one to read.

Corrections folded in over sketch 04:

- **F1 retired.** Sketch 04 committed to "emotion and tension as
  parallel projections with the same discipline as knowledge."
  Architecture-sketch-01 A3 (the inclusion test) rules out that
  commitment: affect and tension are interpretive content an LLM or
  author can reliably evaluate from prose, so they belong in the
  descriptions surface, not as a typed projection. Sketch 05 retires
  F1.
- **Event type is a categorical tag, not a dispatch key.** Sketch 04
  said events have "a declared type from an extensible vocabulary"
  but did not say what the substrate does with that type. Sketch 05
  states it explicitly: the substrate does not dispatch on event
  type. Type is for display, filtering, and library-level operators,
  and remains freely extensible per story.
- **Adverbial and modal content gets an explicit routing rule.**
  Rashomon's encoding under sketch 04 produced schema smells —
  `duel_character(A, B, "noble")`, `coerced` vs `yielded_willingly`
  as sibling predicates — because the substrate had no principled
  answer for where "how was this act qualified?" content goes.
  Sketch 05 gives the principled answer (the adverbial/modal rule
  below): modality with structural downstream consequences gets its
  own event; modality that is descriptive attaches as a description.
- **A3 is applied retroactively to every structural commitment**
  (below). No other sketch-04 commitment fails the test.

## What this sketch is *not* committing to

Same as sketch 04:

- A storage engine (SQLite, Postgres, in-memory, custom — all open).
- A query language or external API.
- A particular wire or file representation.
- Any choice about LLM integration at the substrate level (though
  architecture-sketch-01 A5 names LLM/human interpretation of
  descriptions as first-class at the system level).
- Any scheduler, drama manager, beat system, or surface renderer.
- Authoring tooling, visualization, serialization.

Additionally, as of sketch 05:

- **The descriptions surface's internal shape.** This sketch commits
  to descriptions as a peer to facts (per architecture-01 A2) and to
  the routing rule for modality, but does not specify the
  description record itself. That is the job of
  `descriptions-sketch-01`.
- **The full event-type vocabulary.** Sketch 05 gives guidance on
  how to pick event types and explicitly refuses to enumerate them
  all. Extension is per-story.

If a question starts "what file format," "what API," "what is the
exact set of allowed event types," or "what fields does a Description
have" — it is out of scope.

## What this sketch *is* committing to

1. **E1 — Event-primary substrate.** State is a fold over a typed
   event log, not a set of mutable rows.
2. **E2 — Typed, partially-ordered events.** Events have a declared
   type from an extensible per-story vocabulary; they are partially
   ordered in story-time with optional absolute-time anchors. Type is
   categorical metadata, not a dispatch key.
3. **E3 — Tri-temporal.** Story-time (τ_s), discourse-time (τ_d),
   and authored-time (τ_a) are all represented and queryable.
4. **T1 — Fabula is authoritative where resolved; contested where
   not.** Events and derived propositions support representation of
   ambiguity as a first-class substrate property, not as reader-side
   misunderstanding.
5. **K1 — Per-agent knowledge projection** computed by folding
   knowledge-affecting events.
6. **K2 — Same projection algebra, disjoint update operators.** The
   reader is an epistemic subject modeled with the same slot
   structure and algebra as characters, but updated by a distinct
   vocabulary of narrative operators.
7. **B1 — Branches have a declared kind.** Contested, draft, and
   counterfactual branches exist for different reasons, have
   different scopes of inclusion, and are treated differently by
   enforcement and queries. Event status and branch kind are
   orthogonal axes with enumerated legal combinations.
8. **L1 — Library operates over fabula and sjuzhet both.**
   Prescriptive theories, genre templates, and author-goal
   structures are library-level operators.
9. **M1 (new) — Adverbial/modal routing rule.** Modality is routed
   between events and descriptions by a principled test:
   modality-with-downstream-structural-consequence is its own event;
   purely descriptive modality is a description per architecture-01
   A2.

F1 (emotion and tension as parallel projections) is retired.

## Relation to architecture-sketch-01

Architecture-01 is the cross-topic frame; sketch 05 is the topic
sketch it constrains. Specifically:

- A1 (grid-snap scope): sketch 05 lives entirely within grid-snap
  territory. Structural facts only.
- A2 (two-surface semantics): sketch 05 recognizes descriptions as
  peers to facts and routes adverbial content to them per M1.
- A3 (inclusion test): applied to every commitment in sketch 05.
  The application is documented in the *A3 pass* section below.
- A4 (descriptions draft attention): sketch 05 defers to
  `descriptions-sketch-01` for the shape of descriptions, but
  affirms that they will draft attention — the routing rule M1 is
  where this first matters.
- A5 (interpretation as partner): sketch 05 commits to affect and
  tonal content being interpretive work done by LLMs or humans over
  descriptions, not by substrate query.

Reading sketch 05 alone gives you the substrate's current shape;
reading architecture-01 additionally gives you the frame sketch 05
sits inside.

## Ontology

### The three time axes

Everything in the substrate has coordinates on up to three axes:

- **Story-time (τ_s).** When in the fabula the event happens. Grain
  is story-dependent; the substrate does not enforce a single scale.
- **Discourse-time (τ_d).** Where in the narration the event is
  revealed to the reader. Monotonic by definition.
- **Authored-time (τ_a).** When the author made this commitment.
  Bitemporal "transaction time" — supports retcon, draft diffing,
  and audited revision without losing history.

### Entities

- **Agent.** Anything that holds knowledge, can witness or perform
  events. Characters are agents. The reader is an agent of a
  distinct kind (see K2).
- **Entity.** Anything referred to by the story. Agents are a
  subtype.
- **Event.** Something that happens at a specific story-time (or
  under a partial-order constraint), involving entities, of a
  declared type, with typed effects. See *Event internals* below
  for the full structure.
- **Proposition.** A fact-shaped claim about entities at a
  story-time. Propositions are not stored directly; they are derived
  from the event log.
- **Revelation.** A discourse-time event — the moment the narration
  communicates something to the reader. Revelations are the update
  operators for the reader's projection (see K2).

### Descriptions (peer to events, per architecture-01 A2)

Events, effects, propositions, and sjuzhet entries can carry
**descriptions** — fold-invisible, free-form annotations that
capture texture, motivation, affect, authorial uncertainty, or other
interpretive content. The full shape of a description is specified
by `descriptions-sketch-01`. This sketch commits only to the fact
that descriptions exist as peers to typed content, and to the
routing rule (M1) that determines what belongs on which surface.

## Event internals

This section specifies the structure of an event and the rules that
govern what goes inside it. It is the new material in sketch 05.

### The five required elements

Every event has:

- **id** — a stable identifier, scoped per story.
- **type** — a string from an extensible per-story vocabulary. The
  substrate does not dispatch on type. See *Event type is a tag,
  not a key* below.
- **story-time coordinates** — τ_s and τ_a. Partial-order relations
  may be used in addition to τ_s.
- **participants** — a dict from role-name (string) to entity-id
  (or list of entity-ids for plural roles). Role names are
  per-event-type; the substrate does not enumerate them.
- **effects** — a tuple of `KnowledgeEffect` and/or `WorldEffect`
  records. Effects are the fold-visible output of the event.

Additionally, every event may have:

- **preconditions** — a tuple of `Prop` records that must hold in
  the world state at τ_s for the event to be consistent. Failure is
  a consistency violation the substrate surfaces; it does not
  auto-enforce.
- **status** — `committed` or `provisional`. Unchanged from
  sketch 04.
- **branches** — a set of branch labels the event appears on. A
  canonical-only event carries `{":canonical"}`. Contested events
  carry their branch labels. Same event; same id; distinct branch
  memberships.
- **descriptions** — zero or more descriptions per architecture-01
  A2 / A4. Descriptions are fold-invisible.

### Event type is a tag, not a key

Type is a categorical label. The substrate does not branch on it
(no dispatch, no type-based query filtering beyond the obvious
"give me all events of type X" surface filter, no type-conditioned
fold semantics).

Type exists for:

- Display and reporting (the demo knows "realization" events
  render differently from "utterance" events).
- Library-level operators (a genre template may want to count
  "combat" events, or assert "at least one realization per act").
- Author communication (a sketch or review can talk about "the
  utterance at τ_s=5" without needing to point at specific
  effects).

Type does *not* exist for substrate branching. Two events with the
same effects and the same participants but different types produce
the same fold result. If that feels wrong for a given case, the
right move is to examine the effects, not to reach for type
dispatch.

**Extension rule.** Event types are added per story as needed. A
sketch that proposes a new event type should say what the type is
for (categorization, library use, display convention) and
demonstrate that nothing substrate-level depends on the new type.

**Why this matters.** Sketch 04 left type's role ambiguous, which
invited a drift where specific types started carrying semantics
("deception" events are handled specially; "realization" events get
custom fold behavior; ...). That drift is exactly what A3 says
should not happen without an explicit structural reason. Sketch 05
closes the ambiguity: type is tag, effects are structure.

### M1 — the adverbial/modal routing rule

This is the rule that keeps the schema from drifting into
story-specific predicate proliferation.

**The rule.**

> Modality — the *how, in what spirit, under what qualification* of
> an act — is routed between events and descriptions as follows:
>
> - **Event, if the modality has downstream structural
>   consequences.** If the modality changes what subsequent events
>   can happen, what agent-state carries forward, or what
>   preconditions are satisfied downstream, then it earns its own
>   typed event or a participant role, because the fold needs to
>   see it.
> - **Description, if the modality is descriptive.** If the modality
>   is tonal, interpretive, or carries no fold-visible consequence,
>   it is a description attached to the base event.

**The A3 test under this rule.** Before introducing a modal
predicate or a quality-tagged tuple, answer architecture-01 A3:
*would an attentive LLM or human author reliably catch drift in
this content without the schema?* For a modal qualifier with no
downstream fold consequence, yes — the LLM/author reading the
prose would catch a tonal inconsistency as readily as the schema
would. So the modality belongs in a description. If the modality
*does* have downstream fold consequence — it grounds a later
precondition, it creates an epistemic-state change, it alters
world state — then the fold needs to see it, and it earns an event
or a participant role.

**Worked examples from Rashomon.**

- `duel_character(A, B, "noble")` vs `duel_character(A, B, "cowardly")`
  → **description.** No downstream fold consequence. No subsequent
  event depends on duel-nobility as a precondition; no agent-state
  carries "fought nobly" as a proposition the fold uses. The
  "noble" quality is read from prose by a reader or LLM. Attach as
  a description to the combat event.

- `stole(woodcutter, dagger)` → **event.** Changes world state
  (`world(stole(woodcutter, dagger))`); potentially changes the
  dagger's location/ownership in subsequent folds. Downstream
  structural consequence present. Stays as an event (as encoded).

- `coerced(tajomaru, wife)` vs `yielded_willingly(wife, tajomaru)`
  → **context-dependent.** This is the interesting case and worth
  making explicit:
  - If the story uses trauma-state propositions downstream (e.g.,
    `traumatized(wife)` propagates, constrains wife's subsequent
    agency, grounds later preconditions), then coercion has
    downstream structural consequence and should be its own event
    (type `coercion`) on the relevant branch, with effects that
    create those downstream states.
  - If the story does not use such downstream state — the
    coercion is context for the scene but nothing in the fold
    depends on it — then it is a description attached to the base
    `intercourse` event. The branch still differs (via
    `:b-tajomaru` saying "willing" in its description vs `:b-wife`
    saying "coerced" in its description); the substrate's
    contested-branch machinery still distinguishes them.
  - The current prototype does not track trauma-state. Under
    sketch 05, coercion is therefore a description in the current
    encoding, with a note that if trauma-state is added later,
    coercion is promoted to an event.

**The principle the rule protects.** The schema does not pre-commit
to which modalities are structural. A given modality might be
descriptive in one story and structural in another. The encoding
makes the call per story, justified against A3 in the encoding's
documentation. Sketch 05's job is to name the rule; the stories
apply it.

## A3 pass over sketch-04's commitments

Architecture-01 A3 is applied retroactively to every sketch-04
commitment carried forward into sketch 05. Each passes or is noted:

- **E1 (event-primary).** Events are structural; their log is
  append-only; the fold is deterministic. A3 pass — without the
  event log, author and LLM cannot self-police state consistency
  across a long fabula.
- **E2 (typed, partially-ordered events).** Type is a tag (see
  above); partial order is structural. A3 pass for both.
- **E3 (tri-temporal).** Temporal coordinates are structural. A3
  pass.
- **T1 (contested fabula as first-class).** Branch structure is
  exactly the kind of drift the schema catches that prose doesn't —
  an LLM cannot reliably maintain four mutually incompatible
  accounts without structural book-keeping. A3 pass.
- **K1 (per-agent knowledge projection).** Who knows what at when
  is the canonical case of drift the schema catches. A3 pass.
- **K2 (reader projection with disjoint operators).** Same
  argument. A3 pass.
- **B1 (branch kinds).** Kind distinctions (contested / draft /
  counterfactual) each have different fold-scope semantics;
  without explicit kind the fold rule would drift. A3 pass.
- **L1 (library over fabula and sjuzhet).** Library operators are
  extension points, not substrate features. Neutral under A3.
  Kept.
- **F1 (emotion and tension as parallel projections).** **A3
  fail.** Affect and tonal content are interpretive — an attentive
  LLM or author reading prose can evaluate them as reliably as any
  schema could. The schema should not try. F1 retired; affect
  surfaces as descriptions.

The retroactive pass is clean except for F1.

## F1 retirement (expanded)

F1's intent was real: stories have tonal and emotional structure
that readers track, and a substrate that ignores this is missing
something narrative-theoretical. Sketch 05 does not deny the
phenomenon; it denies that the substrate's typed fold is where the
phenomenon lives.

What F1 attempted, reframed under sketch 05:

- **Affect** — how a character feels at τ_s — is a description
  attached to the character's state or to the event that caused
  the shift. An LLM or human reads the description; no substrate
  query dispatches on affect.
- **Tonal registration** — how a scene is colored for the reader —
  is a description attached to sjuzhet entries. Same argument.
- **Tension as narrative structure** — "the reader has a gap that
  has been open too long" — is a structural query, but it is a
  query *over existing fold state* (reader's GAP slot, τ_d elapsed
  since gap opened), not over a separate projection. Any
  tension-management tool lives above the substrate and consults
  the reader projection plus descriptions.
- **Pacing** — "how many events per story-time unit, how much
  elapsed τ_d per τ_s" — is a simple query over event and sjuzhet
  counts. No affect projection needed.

The pattern: if a question about tension or pacing is structural
(countable, truth-evaluable), it is a query over existing fold
state. If it is about feel (does this climax land, is this beat
earned), it is interpretive — description + LLM/human.

**Prototype impact.** None. Neither the Oedipus nor the Rashomon
encoding used F1; there is no prototype code to remove. When the
prototype iterates against sketch 05, nothing needs to be undone.

## Rashomon encoding refactor (worked)

This section shows what changes in the Rashomon encoding under
sketch 05's rules. The changes are not yet reflected in the
prototype code; applying them is prototype work for a subsequent
iteration.

### Changes

1. **Remove `duel_character(A, B, "quality")`.** Not a schema
   predicate. The "noble" vs "cowardly" character of the duel is a
   description attached to the combat event on each branch.

2. **Collapse `E_intercourse_bare` + per-branch modality events
   into one intercourse event per branch, with per-branch modality
   as a description.** Under sketch-04 the encoding needed a bare
   canonical `intercourse` event plus separate per-branch
   `coerced` / `willing` events to carry the modality. Under
   sketch 05, modality-without-downstream-consequence is a
   description, so:
   - On `:b-tajomaru`: `Event(type="intercourse", ...)` +
     description(kind=interpretive, text="she yielded; what began
     as coercion became consent").
   - On `:b-wife`: `Event(type="intercourse", ...)` +
     description(kind=structural, text="coercion throughout;
     violation").
   - On `:b-husband`: similar to `:b-tajomaru`.
   - On `:b-woodcutter`: similar to `:b-wife`.
   - The bare-fact event is gone; each branch has its own
     intercourse event. Canonical fact "intercourse happened" is
     still derivable because every branch carries one.

3. **Promote coercion to an event if trauma-state is added.** Not
   required for the current encoding. Flagged as a follow-on: if a
   subsequent sketch adds `traumatized(X)` propositions that fold
   into wife's subsequent state, `coercion(tajomaru, wife)` becomes
   an event on `:b-wife` and `:b-woodcutter` with a world effect
   that creates that state.

4. **Drop `begged_to_kill(wife, tajomaru, husband)` as a predicate.**
   Replace with an `utterance` event whose content is described,
   not schematized. Utterances are structural (they change
   listener knowledge via `UTTERANCE_HEARD`); the *content* of the
   utterance is a description attached to the event. The schema
   does not try to encode the speech-act type.

5. **Drop `duel_character` quality-tags for dead, killed, killed_with,
   coerced, yielded_willingly, begged_to_kill, fled,
   body_found_by.** Review each against M1:
   - `dead(X)`: structural (grounds "is this agent active?"
     queries). Keep as predicate.
   - `killed(X, Y)`: structural (world state change, triggers
     dead). Keep as predicate.
   - `killed_with(X, Y, weapon)`: structural if weapon matters for
     downstream state (e.g., "the dagger ends up somewhere");
     descriptive if not. In the Rashomon encoding, the dagger's
     fate does matter (woodcutter steals it), so keep as
     predicate on branches where it matters, and note as
     description elsewhere.
   - `coerced`, `yielded_willingly`: description (see above).
   - `begged_to_kill`: description content of an utterance event.
   - `fled`: structural (location change). Keep, though
     `world(at_location(X, away))` is cleaner.
   - `body_found_by`: structural (discovery triggers knowledge
     state change). Keep.

6. **`intercourse` modality in the encoded sjuzhet.** The sjuzhet
   entries that used to disclose `coerced(T, W)` or
   `yielded_willingly(W, T)` as facts instead attach descriptions
   to the intercourse event. The reader's knowledge on each branch
   includes the intercourse event (as KNOWN); the modality is
   available via the event's descriptions, not as a proposition in
   the reader's fold.

### What stays

- The four sibling `:contested` branches and their structure.
- Canonical preamble: travel, lure, binding, body discovery.
- All `killed`, `killed_with`, `stole` predicates (all pass M1).
- The per-branch sjuzhet structure.

### What the prototype does next

When the prototype iterates against sketch 05:

- `rashomon.py` drops the `duel_character`, `coerced`,
  `yielded_willingly`, and `begged_to_kill` predicate constructors.
- Events that previously asserted those via world-effects now carry
  descriptions instead (pending descriptions-sketch-01 for the
  precise record shape).
- `test_rashomon.py` loses the tests that key on those predicates
  and gains tests that pin description-attachment invariants (once
  descriptions-sketch-01 lands).
- The demo's per-branch world-state matrix has fewer rows; the
  narrative report gains a per-branch description column.

This refactor is not in this sketch — it is sequential prototype
work that happens after `descriptions-sketch-01` specifies the
description record.

## Oedipus spot-check

The Oedipus encoding's schema vocabulary is:

- `child_of(child, parent)` — relational, truth-evaluable, drives
  the anagnorisis fold. A3 pass.
- `killed(killer, victim)` — same. A3 pass.
- `dead(who)` — structural. A3 pass.
- `married(a, b)` — relational. A3 pass.
- `king(who, place)` — relational. A3 pass.
- `killed_stranger_at_crossroads(who)` — this is borderline. It is
  a placeholder for "killed an unidentified victim at a specific
  location," which is structural (the whole plot depends on
  identity-of-victim being unresolved). A3 pass with a note that a
  cleaner encoding might use `killed(oedipus, ?)` with ? being a
  gap; the current shape is a workaround for the substrate's
  lack of existential gap support. This is not urgent — flagged as
  a minor open question.
- `prophecy_will_kill_father_and_marry_mother(who)` — this is a
  compound proposition that would be cleaner as separate prophecy
  content, but the prototype treats it as atomic. A3 pass with a
  similar note.
- `adopted_by(child, parent)` — relational. A3 pass.
- `real_parents_identified(oedipus)` — a GAP placeholder. A3 pass.
- `laius_killed_at_crossroads()` — arity-zero predicate. A3 pass,
  though arity-zero predicates are a minor smell.

No Oedipus predicates fail A3. The encoding is clean.

## Open questions

Revised from sketch 04; closed items removed; new items added where
sketch 05 exposes them.

1. **Existential gaps.** `killed_stranger_at_crossroads` is a
   workaround for the substrate's lack of "A killed someone
   unidentified" representation. Add first-class existential
   propositions or handle in library? Not urgent.
2. **Inference model.** Sketch 04's open question 2 carries
   forward: realization-as-integration (Jocasta realizing the
   man-she-married is the son-she-bore) needs either an inference
   layer or a composite-proposition mechanism. Currently realizations
   are authored events. Unchanged under sketch 05.
3. **Proper focalization semantics.** The prototype records
   focalizer as metadata only. Proper constraint semantics (demoting
   reader propositions the focalizer lacks, scoped to the
   focalized entry) needs τ_d-scoped reader-state tracking.
   Unchanged.
4. **Branch reconvergence.** Sketch 04's open question 13. Whether
   a `:canonical` event downstream of a contest requires explicit
   per-branch resolution, merge, or trans-branch declaration is
   still open. Unchanged.
5. **Draft supersession.** Sketch 04's open question 14 — how a
   `:draft` branch overrides earlier events from its parent. Still
   open; not blocking.
6. **BLANK vs GAP.** Sketch 04 collapsed these; distinguishing them
   needs a case that discriminates (what would a BLANK allow that
   GAP doesn't?). Unchanged.
7. **Trauma-state as the operative example of M1's "depends on
   story" clause.** If a future sketch or encoding adds
   `traumatized(X)` or similar agent-state propositions, `coercion`
   promotes from description to event on the branches that care.
   Document this reversal explicitly when it happens so the
   refactor is legible.
8. **Memoization and snapshot anchors.** Sketch 04 open question 9
   (performance). Unchanged — the naive fold is still sufficient
   for prototype scale.
9. **Description branch semantics.** A description attached to a
   `:b-wife` event lives on `:b-wife`. A description that compares
   the four testimonies lives on `:canonical` as a trans-branch
   annotation. Deferred to `descriptions-sketch-01`.
10. **Event types as an explicit vocabulary per story.** Each
    encoded story (oedipus.py, rashomon.py, future encodings)
    declares its event types as a documented list. The substrate
    does not enforce this; the *discipline* section below asks for
    it.

## Scenarios

The substrate-sketch-04 scenarios (A, B, C) carry forward unchanged
structurally. C (contested fabula) is now also exercised by the
Rashomon encoding, not only by a hypothetical locket case. Refer
to sketch 04 sections for the original scenarios; sketch 05 does
not restate them.

## Discipline

Process expectations for work against sketch 05:

- **New schema fields pass A3 in the sketch or encoding where they
  are introduced.** Any predicate or event attribute is documented
  with a one-line A3 justification. If it fails the test, it is
  routed to a description instead.
- **Event types are named and documented per story.** An encoded
  story declares the event-type vocabulary it uses, with a short
  note on what each type is for.
- **M1 is applied per story, not globally.** The adverbial/modal
  decision is local to the encoding. A sketch or encoding that
  reverses a prior call (e.g., promoting `coercion` from
  description to event) documents the reversal and the reason.
- **F1 is not re-opened without an A3 argument.** Affect as a typed
  projection was A3-rejected in this sketch; a future sketch that
  wants to reintroduce it must give a structural argument that
  does not reduce to "we want affect queries." If such queries are
  structural they are queries over gap state and description
  metadata, not over a new projection.

## Summary of changes from sketch 04

| Commitment | Sketch 04 | Sketch 05 |
|---|---|---|
| E1 event-primary | ✓ | ✓ (A3 pass) |
| E2 typed events | ✓ | ✓ (type as tag, not key) |
| E3 tri-temporal | ✓ | ✓ (A3 pass) |
| T1 contested fabula | ✓ | ✓ (A3 pass) |
| K1 agent fold | ✓ | ✓ (A3 pass) |
| K2 reader-as-subject | ✓ | ✓ (A3 pass) |
| F1 emotion/tension projection | ✓ | ✗ retired |
| L1 library operators | ✓ | ✓ (A3 pass) |
| B1 branch kinds | ✓ | ✓ (A3 pass) |
| M1 adverbial/modal rule | — | ✓ new |
| Descriptions as peer surface | — | ✓ acknowledged; shape in descriptions-sketch-01 |
| Event type as dispatch key | ambiguous | ✗ explicitly not a dispatch key |
