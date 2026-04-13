# Substrate — sketch 01

**Status:** superseded
**Date:** 2026-04-13
**Supersedes:** nothing
**Superseded by:** [substrate-sketch-02.md](substrate-sketch-02.md)

*Kept in place as the record of initial thinking. Sketch 02 revises T1 (was too strong — excluded ambiguous-narration stories), K2 (same algebra but different update operators for characters vs. reader), and the library claim (prescriptive structures operate over fabula + sjuzhet, not sjuzhet alone). Sketch 02 also adds three open questions (causality-vs-temporal-order, event granularity, focalization/narrator layer) missing here.*


## Purpose

Sketch the data substrate at the bottom of the story engine — the thing every other component reads from and writes to. This is the layer that holds *what is true in the story world, when it became true, who knows it, and in what order the narration has revealed it*.

This is a **design sketch**, not a schema, not an implementation, not a database choice. The output of this sketch is a working vocabulary and a short list of load-bearing commitments, suitable for pressure-testing against the research survey and for guiding the next sketch (which may be a concrete schema, a prototype, or a different substrate entirely if this one fails under examination).

## What this sketch is *not* committing to

- A storage engine. SQLite, Postgres, a custom log store, in-memory — all remain open.
- A query language or external API.
- A particular representation for events (structured records? CD primitives? typed propositions? JSON?).
- Any choice about LLM integration.
- Any scheduler, drama manager, or surface renderer. Those sit *above* the substrate.
- Anything about authoring tooling, visualization, or serialization format.

If a question starts "what file format," "what API," or "which library," it is out of scope for this sketch.

## What this sketch *is* committing to, tentatively

1. The substrate is **event-primary**: state is a fold over an event log, not a set of mutable rows. *(Principle E1.)*
2. Events are **typed** and **partially ordered in story-time**, not merely linearly ordered. *(Principle E2.)*
3. The substrate is **tri-temporal**: story-time, discourse-time, and authored-time are all represented, and all three are queryable. *(Principle E3.)*
4. **Knowledge is per-agent** and is itself a fold over the events that agent has witnessed, inferred, been told, or been deceived into believing. *(Principle K1.)*
5. **The reader is an agent** in the same knowledge system, with the same projection machinery. Sternberg's narrative interests are queries over the reader's projection. *(Principle K2.)*
6. Emotional and tension state are **parallel projections** over the event log, per-agent and global, with the same architectural shape as knowledge projections. *(Principle F1.)*
7. The substrate represents **story-time truth**, not narrative truth. What a character *believes* lives in the knowledge layer; what *happened* lives in the event log. Unreliable narration is expressed as a disagreement between reader-projection and ground-truth event log, not as ambiguity in the event log itself. *(Principle T1.)*

These are the seven commitments the rest of the sketch elaborates.

## Ontology

### The three time axes

Everything in the substrate has coordinates on up to three axes:

- **Story-time (τ_s).** When in the fabula the event happens. Years, days, seconds — whatever grain the story needs, sometimes mixed. A duel plays out in seconds; a dynasty spans centuries.
- **Discourse-time (τ_d).** Where in the narration the event is revealed to the reader. Chapter 3, page 47, minute 12. Monotonic by definition (the reader reads forward).
- **Authored-time (τ_a).** When the author made this commitment. The substrate is revised over time as the author changes their mind; τ_a is the bitemporal "transaction time" axis that lets us replay authorial decisions, diff drafts, and retcon without losing history.

Story-time and discourse-time are the **Russian Formalist fabula/sjuzhet distinction** with explicit coordinates. Authored-time is the **bitemporal database insight** applied to authorship.

### Entities

- **Agent.** Anything that holds knowledge, has emotional state, can witness or perform events. Characters are agents. The reader is an agent. The author may or may not be an agent (undecided — see Open Questions).
- **Entity.** Anything that is *referred to* but does not necessarily know anything: objects, locations, organizations, abstract things the story names (a prophecy, a reputation). Agents are a subtype of entity.
- **Event.** Something that happens at a specific story-time, involving one or more entities, of a declared type, with typed effects on world state and on agent knowledge/emotion.
- **Fact.** A proposition true at some story-time about entities — "Alice is in the kitchen at τ=10," "The locket contains a photograph." Facts are not stored directly; they are *derived* from the event log by replaying effects up to a chosen story-time.
- **Belief.** A fact-shaped object labeled with an agent and a confidence — "Bob believes Alice is in the garden" — which may or may not correspond to ground-truth facts. Beliefs are not stored directly either; they are *derived* from the agent's knowledge projection.
- **Revelation.** A discourse-time event: the moment at which the narration communicates a fact or belief to the reader. Revelations are the operations that update the reader's projection.

### Events as the load-bearing primitive

Every event has, at minimum:

- `id`: a stable identifier.
- `type`: a member of a typed vocabulary (e.g. *movement*, *utterance*, *observation*, *decision*, *death*, *revelation*, *peripeteia*, *anagnorisis*, ...). The vocabulary is extensible and is one of the engine's main authoring-time design decisions.
- `τ_s`: story-time coordinate (or range, or partial-order constraint).
- `τ_a`: authored-time coordinate (when this event was committed).
- `participants`: typed-role bindings to entities (`agent`, `patient`, `witness`, `location`, `instrument`, ...).
- `effects`: a list of typed state changes (world-state mutations, knowledge-state mutations, emotional-state mutations).
- `preconditions`: a list of typed facts that must hold at τ_s for this event to be well-formed. Violated preconditions are a first-class error surfaced by the enforcement layer.
- `metadata`: whatever else — genre tags, authorial notes, scene bindings.

State is not stored. State at τ_s = *fold(effects of all events with τ_s' ≤ τ_s)*.

This is the same discipline as event sourcing in distributed systems, applied to fiction. Its virtues for our setting:

- **Timeline queries are free.** "What was true at τ_s = 1340 Midsummer?" is fold-through-timestamp.
- **Retcons are cheap and auditable.** Adding, removing, or revising an event re-runs the fold and highlights what downstream facts changed. Authored-time preserves the prior history.
- **Counterfactuals are cheap.** "Replay without event E" yields an alternative state; the engine can ask "would event E' still be well-formed?"
- **Knowledge and emotion projections are the same operation with a different fold function.** See K1/F1 below.

### Partial order, not total order

Events are partially ordered in story-time. Some events are strictly ordered (Alice enters *before* she speaks), many are not (what Alice is doing in the kitchen at τ=10 and what Bob is doing in the garden at τ=10 have no ordering constraint unless the story imposes one).

Partial order matters because:

- Authors often know event relationships without knowing absolute timestamps. "After Alice learns the truth, before the wedding" is a constraint, not a timestamp.
- Many stories are internally partially-ordered and are only made total by the discourse.
- Enforcement is easier over constraints than over exact values: "this event violates the after-wedding constraint" is a clearer error than "this event has timestamp 1340-06-24 12:30 but should be 1340-06-25 09:00."

Representation: a **partial-order constraint graph** over events, with optional absolute-time anchors. Total ordering is a degenerate case (all events anchored).

## Knowledge

### K1. Per-agent knowledge projection

Each agent has a **knowledge projection function** P_A(τ_s) that yields the agent's epistemic state at story-time τ_s:

- **Witnessed facts.** Facts for which A has direct perceptual evidence via an event where A was a `witness` (or `agent` or `patient`).
- **Inferred facts.** Facts A deduces from witnessed or heard facts + A's background model.
- **Heard facts.** Facts A has been told by another agent, with a provenance chain (who told A, when, under what circumstances). Provenance supports evaluating reliability.
- **Beliefs.** Held propositions with confidence, possibly contradicting ground truth (deception, mistake, delusion).
- **Blanks.** Propositions A does not know and does not know they don't know. Explicit representation of blanks enables Sternberg-surprise.
- **Gaps.** Propositions A knows they don't know (open questions the agent is aware of). Enables Sternberg-curiosity from the character side.

The projection is computed by folding *knowledge-affecting events* up to τ_s. Knowledge-affecting events include:

- **Observation** — A perceives event E; facts about E enter A's witnessed set.
- **Utterance** — A is told fact F by B; F enters A's heard set with provenance [B, τ_s, any accompanying context].
- **Inference** — A performs inference from their current knowledge state; derived facts enter A's inferred set.
- **Deception** — A is told fact F by B but F is false in the event log; A's belief set acquires F, in contradiction to ground truth.
- **Forgetting** — rare but real; facts drop from A's active knowledge. Useful for long time passages.
- **Realization** — a specific kind of inference that moves a fact from *blank* or *gap* to *known*, often dramatically. Aristotle's anagnorisis is a realization event.

### K2. The reader is an agent

The reader has a projection P_Reader(τ_d) — note the discourse-time axis, not story-time. The reader's projection is updated by **revelation events** (discourse-time events that communicate facts or beliefs from the narration to the reader).

Consequence: the same mechanism that handles dramatic irony between characters (Alice's projection vs. Bob's projection at τ_s) handles **reader interest** (Reader's projection vs. ground-truth event log at τ_d). Sternberg becomes:

- **Suspense(τ_d):** Reader knows a τ_s-future event is coming (an outcome-shaped gap) but does not know which outcome.
- **Curiosity(τ_d):** Reader knows a τ_s-past event happened (a provenance-shaped gap) but does not know its content or cause.
- **Surprise(τ_d):** Reader had a belief that ground-truth-in-the-event-log contradicts; a revelation moves the belief.

All three reduce to queries over the reader's projection at a given discourse-time, against the event log. This is the direct payoff of the reader-as-agent commitment.

### Dramatic irony as a trivial query

Dramatic irony at τ_s between agents A and B is:

    P_A(τ_s).knows(F) ∧ ¬P_B(τ_s).knows(F) ∧ Reader.knows_about(A_and_B_relationship)

In English: A knows F, B doesn't, and the reader can see the asymmetry. Every Greek tragedy reduces to this pattern applied to *Oedipus*, *Othello*, *Macbeth*. The substrate makes it a lookup.

## Emotional and tension projections

### F1. Emotional state is a per-agent fold

Parallel to knowledge projection. Each agent has an **emotional projection** E_A(τ_s) yielding:

- A vector of emotional dimensions (valence, arousal, specific emotions — model TBD), per-target where applicable (Alice's feelings *toward Bob* vs. *toward herself*).
- Relationship dynamics (affinity, trust, rivalry, dependence) between pairs of agents.

Updated by **emotion-affecting events**: interactions, revelations, losses, successes, perceived slights, time passing. The effect function is authored per event type (the engine's emotion model is itself a design decision, probably worth its own sketch).

Global **tension** is a projection over the event log at the story level — roughly the aggregate of unresolved stakes, pending threats, outstanding gaps in the reader's projection, and emotional volatility. MEXICA-style.

Both projections have the same discipline as knowledge: state is a fold; events are the primitives; the projection can be replayed with modified events for counterfactual work.

## Fabula, sjuzhet, discourse

Three representations, explicitly separated:

- **Fabula.** The event log with story-time coordinates. Ground truth. Partially ordered.
- **Sjuzhet.** A **selected and ordered sequence** of events from the fabula, intended for narration. Not every fabula event appears in the sjuzhet. Order in the sjuzhet is discourse-time order, not story-time order.
- **Discourse.** The rendered text (or stage directions, or screenplay lines, or game scenes) produced from the sjuzhet.

Authorial operations map to this separation cleanly:

- Writing a chapter = selecting sjuzhet events from the fabula and rendering them to discourse.
- A flashback = a sjuzhet event with τ_s in the past but τ_d now.
- Withholding = a fabula event *not* selected into the sjuzhet (yet); it will later be revealed.
- A reveal = a sjuzhet event whose revelation to the reader collapses a blank or gap.
- A retcon = an authored-time edit to the fabula; sjuzhet and discourse re-derive.

## Enforcement: the expert-system layer's target

The expert system (front three in the original plan) reasons over the substrate. Examples of the kinds of checks and queries it must support:

- **Continuity.** Does every event's preconditions hold at its τ_s in the current fabula? Where are the violations?
- **Knowledge consistency.** Does character A say something at τ_s that A shouldn't know? Does A fail to say something they would have to, given what they know?
- **Dramatic irony health.** Are known-to-reader-but-not-to-character asymmetries being used or wasted?
- **Suspense/curiosity/surprise inventory.** At the current τ_d, how many open gaps does the reader have? What's the last surprise? How long has tension gone without variation?
- **Theme coherence.** (Harder; may require layer above substrate.) Do the events selected into the sjuzhet bear on the authorial argument?
- **Character integrity.** Does A's action at τ_s contradict their established emotional or value state?
- **Pacing/rhythm.** At discourse level, what's the event density, scene-length distribution, tension curve?

None of these require LLMs. They are deterministic queries over a structured substrate. This is the "expert system running at warp speed" front made concrete.

## How the theories map onto the substrate

| Theory | Substrate mapping |
|--------|-------------------|
| Aristotle — peripeteia | A typed event whose effects reverse a previously-fixed fact about the protagonist's trajectory. |
| Aristotle — anagnorisis | A *realization* event in the protagonist's knowledge projection — a fact moves from gap/blank to known. |
| Aristotle — hamartia | A past event in the protagonist's action history, later revealed (or never) to be causally linked to the peripeteia. |
| Propp — function | A typed event vocabulary. The 31 functions are just types in our taxonomy, with partial-order constraints. |
| Propp — sphere of action | A typed role in participant bindings. |
| Freytag / three-act / monomyth | Templates at the sjuzhet-selection layer. They specify which event types occur at which discourse-time positions. **Not substrate; library.** |
| Dramatica — four throughlines | Four threads of events in the fabula, each with its own protagonist/entity focus. Operationalizable but stops short of Dramatica's full lattice — which, by design, we don't yet commit to. |
| Sternberg — suspense, curiosity, surprise | Queries over the reader's knowledge projection at τ_d, as spelled out in K2 above. |
| MEXICA — engagement/reflection | Engagement operates on fabula + emotional projection; reflection operates on the full substrate to find impasses and violations. The substrate supports both phases without privileging either. |
| MINSTREL — author goals | Sit above the substrate as targets the drama/sjuzhet layer optimizes for. |
| Façade — beats | Units of the sjuzhet, one layer above events. Beats group events for scheduling. |

The theories are not directly encoded in the substrate. The substrate is **what they can all be expressed over**.

## Worked example

A short, deliberately mundane scene to make the machinery concrete.

### Fabula events (τ_s, type, participants, effects)

1. `E1 @ τ=T0`: *arrival*. Alice enters the kitchen. Precondition: Alice not in kitchen. Effects: world{Alice.location = kitchen}. Witness: Bob (also in kitchen).
2. `E2 @ τ=T0+1`: *observation*. Alice observes Bob is holding a locket. Effects: knowledge{Alice.witnessed(Bob.holding(locket))}.
3. `E3 @ τ=T0+2`: *utterance*. Bob tells Alice, "This is my grandmother's." Effects: knowledge{Alice.heard(locket.owner = Bob.grandmother, from: Bob)}.
4. `E4 @ τ=T0-hours`: *observation*. Earlier, unseen by Alice, Bob picked the locket up from Charlie's drawer. Effects: world{locket.location = Bob}. Witness: none.

### Knowledge projections at τ=T0+2

- **P_Alice(T0+2):** knows locket is in Bob's hand, knows Bob has asserted "grandmother's." Holds belief locket is Bob's grandmother's. Does not know E4. Blank: that the locket has any other history.
- **P_Bob(T0+2):** knows E4 (took from Charlie's drawer). Knows E1–E3. Holds belief Alice does not know E4.
- **P_Charlie(T0+2):** does not know E1–E3 (wasn't there). Probably has a gap re: locket location (depending on when they last looked).

### Ground truth at T0+2

- Locket is in Bob's hand.
- Locket was in Charlie's drawer at T0-hours.
- E4 is in the fabula.

### Reader projection, scenario A (reader saw E4)

- P_Reader(current τ_d) knows E4, knows E1–E3, knows Alice believes Bob's assertion.
- **Dramatic irony:** Reader.knows(E4) ∧ ¬P_Alice.knows(E4). This is a suspense/curiosity seed: the reader is now waiting to see whether, when, and how Alice will learn.
- Sternberg: a prospective gap has opened. Suspense value is real. Any subsequent Bob-Alice interaction carries weight it would not otherwise carry.

### Reader projection, scenario B (reader did *not* see E4)

- P_Reader(current τ_d) knows E1–E3 and Alice's belief. Does not know E4.
- **Blank:** The reader does not know the locket has a prior history.
- Sternberg: no suspense or curiosity yet. If E4 is later revealed to the reader (a sjuzhet choice), a *surprise* is possible.

**The authorial decision** — select E4 into the sjuzhet early, late, or never — is operationalized as a choice among three reader-projection trajectories, each with different tension/surprise/curiosity profiles. The substrate makes this decision visible as a query.

This is the payoff. A trivial scene, three agents, four events, and the substrate has already made irony, suspense, curiosity, and surprise into first-class things the engine can see, count, and reason about.

## Open questions

These are the commitments this sketch *did not* make, and must be resolved in later sketches or prototypes before any implementation begins.

1. **What is the event-type vocabulary?** How many types, at what grain, extensible by whom? Too few types → under-expressive; too many → fragmented and unqueryable. This is the single largest open design question.
2. **What is the logic for inference?** Alice sees Bob holding the locket and hears Bob claim it — what inferences does she make, under what model? A full theory of character reasoning is out of scope for the substrate; a **minimum** inference capability is not. Candidate: a bounded forward-chaining rule layer, per-agent. Possibly LLM-augmented for plausibility judgments. Probably should be its own sketch.
3. **What is the emotional model?** PAD (pleasure/arousal/dominance)? OCC (Ortony/Clore/Collins appraisal theory)? A custom genre-specific vocabulary? The field has many candidates; none is obviously right. Needs its own sketch.
4. **How is the reader model updated?** Sjuzhet revelations update P_Reader, but the reader also *infers* — anticipates, retroactively revises, commits to expectations. Do we simulate reader inference? Approximate it? Use human feedback?
5. **Is the author an agent?** If yes, the substrate has an explicit model of the author's intent; if no, intent lives in a separate layer. Dramatica would say yes; Façade's drama manager says the author is a layer, not an agent.
6. **How are long-running entities represented when the grain of events varies by orders of magnitude?** A dynasty over 300 years plus a sword-fight of 30 seconds in the same fabula. The partial-order graph handles this in principle; in practice, emotional and tension projections will need time-aware decay functions that respect the grain.
7. **What happens when the fabula is inconsistent?** Authors contradict themselves; events added in authored-time N may violate preconditions set by events in authored-time N-1. The substrate must surface contradictions without silently preferring one over the other. This is an enforcement-layer question but the substrate must support it.
8. **How does this interact with the LLM as generator?** The LLM cannot be the source of truth — it will happily contradict the event log. Candidate discipline: the LLM proposes events and prose; the substrate validates; rejected proposals are retried or escalated. But this is a higher-layer concern, and its architecture is a separate sketch.
9. **Scale.** A novel might have thousands of events and tens of agents. A multi-novel saga, an order of magnitude more. Projections computed by full fold will not scale naively. Incremental projections, memoization, snapshots at anchors — all implementation concerns, but the substrate must be designed to make them possible.

## What this sketch changed

- Moved "event log" from vague to a specific bitemporal, partially-ordered, typed-event store.
- Established **per-agent knowledge projection, with the reader as an agent**, as the central commitment.
- Spelled out how Sternberg's three interests and dramatic irony reduce to queries over this substrate.
- Separated *fabula*, *sjuzhet*, and *discourse* as three distinct representations that the engine operates on at different layers.
- Made the case that prescriptive story structures (Freytag, three-act, monomyth) belong in a **template library** at the sjuzhet-selection layer, **not** in the substrate.

## What this sketch does not yet give us

- A schema.
- A way to ingest authored events.
- A generator.
- A drama manager.
- A surface renderer.
- A test corpus.
- Any running code.

The next sketch should probably be either:

- **(a)** An event-type vocabulary sketch — what events exist, at what grain, with what effects. Without this, the substrate is an empty vessel.
- **(b)** An inference-model sketch — what characters can reason, how much, with what fidelity.
- **(c)** A concrete data-model prototype — the smallest possible implementation of the substrate as it stands, on a single worked story, so we can see where the sketch breaks before expanding it.

The case for (c) is strong: an implementation forces decisions the sketch can defer, and surfaces problems no amount of design-talk will find.
