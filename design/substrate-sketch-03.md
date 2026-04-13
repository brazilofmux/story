# Substrate — sketch 03 (consolidated)

**Status:** superseded
**Date:** 2026-04-13
**Supersedes:** [substrate-sketch-01.md](substrate-sketch-01.md), [substrate-sketch-02.md](substrate-sketch-02.md)
**Superseded by:** [substrate-sketch-04.md](substrate-sketch-04.md)

*Kept in place as historical record. [Sketch 04](substrate-sketch-04.md) is the current active substrate sketch. It fixes issues in sketch 03: distinguishes branch kinds (contested / draft / counterfactual) because they have different semantics for persistence and query inclusion; demotes the "post-contested canonical by construction" claim to an open question (13) about branch reconvergence; corrects a worked-example slip that used an undeclared slot name; simplifies event status to two values (committed / provisional) and recognizes contested-ness as a derived cross-branch property of propositions rather than an event attribute; makes Sternberg and dramatic-irony queries branch-aware.*

## Purpose

The consolidated, self-contained statement of the substrate design. Sketches 01 and 02 are kept as historical record of the reasoning; this sketch is the one to read. The prototype that follows is built against this sketch.

Three issues found in code review of sketches 01 and 02 are resolved here:

- **Fact/state semantics now include contested branches throughout.** Sketch 02 introduced contested regions but sketch 01 still defined fact and state as singular derivations; sketch 03 gives one consistent account of both.
- **Knowledge slots are source-agnostic.** Sketch 02 revised the reader's update operators but kept character-centric slot names (*witnessed*, *heard*). Sketch 03 separates slot identity (epistemic state) from provenance (update source), which disentangles the "same algebra, different operators" claim.
- **This sketch is self-contained.** The design/README distinguishes active vs. superseded sketches so the starting point is unambiguous.

## What this sketch is *not* committing to

- A storage engine (SQLite, Postgres, in-memory, custom — all open).
- A query language or external API.
- A particular wire or file representation.
- Any choice about LLM integration.
- Any scheduler, drama manager, beat system, or surface renderer. Those sit *above* the substrate.
- Authoring tooling, visualization, serialization.

If a question starts "what file format," "what API," or "which library," it is out of scope.

## What this sketch *is* committing to

1. **E1 — Event-primary substrate.** State is a fold over a typed event log, not a set of mutable rows.
2. **E2 — Typed, partially-ordered events.** Events have a declared type from an extensible vocabulary; they are partially ordered in story-time with optional absolute-time anchors.
3. **E3 — Tri-temporal.** Story-time (τ_s), discourse-time (τ_d), and authored-time (τ_a) are all represented and queryable.
4. **T1 — Fabula is authoritative where resolved; contested where not.** Events and fact-producing propositions carry a resolution status; contested regions are supported as a first-class substrate property, not as reader-side misunderstanding.
5. **K1 — Per-agent knowledge projection** computed by folding knowledge-affecting events.
6. **K2 — Same projection algebra, disjoint update operators.** The reader is an epistemic subject modeled with the same slot structure and algebra as characters, but updated by a distinct vocabulary of narrative operators.
7. **F1 — Emotion and tension as parallel projections** with the same discipline as knowledge.
8. **L1 — Library operates over fabula and sjuzhet both.** Prescriptive theories, genre templates, and author-goal structures are library-level operators; they may constrain both fabula content and sjuzhet selection/ordering. The substrate is neutral ontology.

## Ontology

### The three time axes

Everything in the substrate has coordinates on up to three axes:

- **Story-time (τ_s).** When in the fabula the event happens. Grain is story-dependent; the substrate does not enforce a single scale.
- **Discourse-time (τ_d).** Where in the narration the event is revealed to the reader. Monotonic by definition.
- **Authored-time (τ_a).** When the author made this commitment. Bitemporal "transaction time" — lets the substrate support retcon, draft diffing, and audited revision without losing history.

### Entities

- **Agent.** Anything that holds knowledge, has emotional state, can witness or perform events. Characters are agents. The reader is an agent (of a distinct kind — see K2).
- **Entity.** Anything referred to by the story. Agents are a subtype.
- **Event.** Something that happens at a specific story-time (or under a partial-order constraint), involving entities, of a declared type, with typed effects.
- **Proposition.** A fact-shaped claim about entities at a story-time — "Alice is in the kitchen at τ=10," "The locket contains a photograph." Propositions are not stored directly; they are *derived* from the event log.
- **Revelation.** A discourse-time event: the moment the narration communicates something to the reader. Revelations are the update operators for the reader's projection.
- **Branch label.** When the fabula contains contested regions, branches carry labels identifying which interpretation they embody. Canonical regions have a distinguished `:canonical` branch.

### Events as the load-bearing primitive

Every event has, at minimum:

- `id` — stable identifier.
- `type` — member of a typed, extensible vocabulary.
- `τ_s` — story-time coordinate or partial-order constraint.
- `τ_a` — authored-time.
- `participants` — typed-role bindings to entities (`agent`, `patient`, `witness`, `location`, `instrument`, ...).
- `effects` — typed state changes (world-state mutations, knowledge-state mutations, emotional-state mutations, tension-state mutations).
- `preconditions` — typed propositions that must hold at τ_s for this event to be well-formed.
- `status` — resolution status (see Fabula resolution below).
- `branch` — one or more branch labels this event belongs to.
- `metadata` — genre tags, authorial notes, scene bindings, warrants (see open question 10).

State is not stored; state-at-τ is derived. (See Facts and state, below.)

### Partial order

Events are partially ordered in story-time. Ordering is expressed as a graph of relative constraints (*A before B*, *B concurrent with C*), with optional absolute anchors. Total order is a degenerate case. This matters because:

- Authors often know event relationships without knowing timestamps.
- Enforcement works cleanly over constraints; exact times are often a fiction.
- Branches (see below) may disagree about relative order, which the graph handles naturally.

## Fabula resolution and branching

Every event and every derived proposition carries a **resolution status**:

- **Canonical.** Settled; the substrate treats it as ground truth.
- **Contested.** Multiple mutually inconsistent candidates exist with equal authorial endorsement. The fabula permanently holds all candidates, each tagged with a distinguishing branch label.
- **Provisional.** Committed at some τ_a pending possible later revision; acceptable in drafts, should be resolved or converted to contested before the work is considered complete.

For most events in most stories, canonical is the right and default status. The substrate *permits* contested fabula; it does not require it.

### Branches, formally

A **branch** is a subset of events (and their associated propositions) sharing a label. Branches exist for:

- Contested regions in T1 — e.g., in *Rashomon*, four branches for the four testimonies.
- Authorial draft exploration — not shipped but useful during writing.
- Counterfactual replay — "what if E did not happen" creates a temporary branch for enforcement and dramatic-value queries.

The `:canonical` branch is the default; events not tagged with a branch are implicitly on it. Canonical regions are queries without branch-ambiguity. Contested regions return **branch-indexed results**.

## Facts and state (with branching)

### A fact is a proposition produced by folding events

For a proposition P about entities at story-time τ_s:

- **In canonical regions:** folding the canonical event log up to τ_s either makes P true, makes P false, or leaves P undetermined. The substrate returns a single result.
- **In contested regions:** folding each candidate branch may produce different results for P. The substrate returns a **branch-indexed mapping** — `{ :branch_a: true, :branch_b: false, :branch_c: undetermined }`.

Propositions that do not touch any contested region of the log are unambiguously single-valued even when contested regions exist elsewhere in the fabula. Branching is local, not global.

### State-at-τ

For a story-time τ_s:

- **In canonical regions:** state is one fold — the union of all canonical effects with τ_s' ≤ τ_s.
- **In contested regions:** state is **branch-indexed** — one fold per candidate branch, tagged.

A query about a fact that is canonical but happens to be set by an event after a contested region still returns canonically, because canonical events at τ_s' > contested-region-end are downstream and consistent across branches by construction (or the author has extended the contest, which the substrate allows).

### Enforcement in contested regions

Every enforcement check runs **per branch**:

- Precondition checks: does E's precondition hold on branch b at E's τ_s?
- Knowledge consistency: does A's utterance at τ_s respect what A knows on branch b?
- Continuity: are the events on branch b mutually coherent?

A well-formed contested region is one in which each branch is internally consistent, even if the branches disagree with each other. *Rashomon* is well-formed in this sense: within each testimony the events cohere; across testimonies they contradict; the substrate holds all of them.

## Knowledge

### Projection shape (shared across agent types)

Every agent — characters and the reader — has a knowledge state modeled as a set of **propositions**, each carrying:

- **Content.** The proposition itself (a fact-shaped claim about entities at a story-time).
- **Confidence.** A scalar or categorical — how firmly held (certain / believed / suspected / dismissed).
- **Provenance.** The chain of update operators that placed this proposition into the agent's state: who told/showed the agent, through what operation, at what τ.
- **Status in the agent's model.** Held-as-true, held-as-false, held-as-open-question.
- **Branch awareness.** If the agent's knowledge touches a contested region, the agent may hold different content per branch, know about the contest, or be unaware of it — all representable.

From these primitives the following **epistemic slots** partition any agent's knowledge state. Slots are **source-agnostic**:

- **Known.** Propositions held with high confidence, taken as true for the agent's reasoning.
- **Believed.** Held with meaningful confidence but genuinely fallible; may be wrong relative to canonical fabula.
- **Suspected.** Held tentatively; the agent entertains the proposition without committing.
- **Gap.** A proposition-shaped question the agent is aware is open. Explicit known-unknowns.
- **Blank.** A proposition whose absence the agent is not aware of. The hardest to represent; approximated operationally as "not in the agent's state and not reachable by the agent's current inferences." Present for Sternberg-surprise mechanics.

These slot names **do not imply a source**. Provenance is separate metadata. A character's "known" arrived by observation, utterance, or inference; a reader's "known" arrived by disclosure, focalization, or framed report. The slots are what the agent holds; the update operators are how it got there.

### Update operators (disjoint vocabularies)

Update operators are the verbs that move propositions into and among slots. The vocabularies are different for the two subject types:

**Diegetic update operators (characters):**

- *Observation* — agent perceives an event in-world.
- *Utterance-heard* — another agent tells this agent a proposition; provenance records the speaker.
- *Inference* — agent derives a proposition from current state via an inference model.
- *Deception* — agent is told a proposition that is false on the relevant branch; the agent acquires it with normal provenance (unaware of the falsity).
- *Forgetting* — confidence decays; a proposition moves toward or out of the state.
- *Realization* — an existing proposition is upgraded from gap/suspected to known, often via newly-available inference. Aristotle's anagnorisis is the canonical instance.

**Narrative update operators (reader):**

- *Disclosure* — the narration delivers a proposition to the reader. Provenance records the narrative act.
- *Focalization* — the narration routes the reader's access through an agent's perspective. Propositions the focalizer lacks become reader-gaps; propositions the focalizer misconstrues become reader-believed rather than reader-known.
- *Omission* — a proposition is withheld. Creates a reader-blank, or a reader-gap if the narration hints at the omission.
- *Framing* — a proposition is delivered with rhetorical coloring that affects the confidence or the held-as-true/false status. "Bob said he loved her, though his hands were shaking" frames the report with a reliability discount.
- *Retroactive reframing* — a later narrative act causes the reader to re-interpret earlier material; propositions migrate between slots or have their confidence revised. Unreliable-narrator reveals are the extreme case; any foreshadowing-pays-off moment is a mild case.

Characters never undergo focalization, omission, framing, or retroactive reframing. Those are operations on the reader's access to the story, not in-world epistemic events. Readers never undergo diegetic observation in the character sense; their access to the world is always mediated.

### Sternberg's interests as queries

At discourse-time τ_d, over the reader's projection:

- **Suspense.** Reader holds a proposition-shaped gap about a τ_s-future outcome whose alternatives are known.
- **Curiosity.** Reader holds a proposition-shaped gap about a τ_s-past event whose existence is known but whose content/cause is not.
- **Surprise.** New narrative update contradicts a prior reader belief; retroactive reframing migrates propositions between slots.

These are queries, not stored fields. They are computed from the reader's current projection plus the fabula (for "what is actually true that the reader does not know").

### Dramatic irony as a query

At story-time τ_s between characters A and B, on branch b:

    P_A(τ_s, b).knows(F) ∧ ¬P_B(τ_s, b).knows(F) ∧ P_Reader(τ_d).knows_about(the_asymmetry)

This reduces every Sophoclean-style irony to a lookup over the same structure.

## Emotional and tension projections (F1)

Parallel to knowledge projection. Each agent has an **emotional projection** E_A(τ_s) yielding:

- A vector of emotional dimensions (specific model TBD — an open question that deserves its own sketch).
- Per-target affect (Alice's feelings toward Bob).
- Relationship dynamics (affinity, trust, rivalry, dependence) between pairs.

Updated by emotion-affecting events. Effect functions are authored per event type.

Global **tension** is a projection at the story level — aggregate of unresolved stakes, pending threats, outstanding reader-gaps, emotional volatility. MEXICA-style.

Both projections branch the way knowledge does: in contested regions, per-branch emotional states are tracked and returned.

## Fabula, sjuzhet, discourse

Three representations:

- **Fabula.** The event log with story-time coordinates, including canonical, contested, and provisional regions. Partially ordered. The authoritative (where resolved) account of what happens in the story world.
- **Sjuzhet.** A selected and ordered sequence of fabula events, annotated with narrative-update metadata (focalizer, framing, disclosure acts), intended for narration. Not every fabula event appears in the sjuzhet.
- **Discourse.** The rendered prose / script / scene / interactive turn produced from the sjuzhet.

Authorial operations map cleanly:

- Writing a chapter = selecting sjuzhet events from the fabula, attaching narrative-update metadata, and rendering.
- A flashback = a sjuzhet event with τ_s in the past, τ_d now.
- Withholding = a fabula event not selected (yet).
- Reveal = a sjuzhet event whose narrative update migrates reader-state.
- Retcon = an authored-time edit to the fabula; sjuzhet and discourse re-derive.
- Unreliable-narrator arrangement = narrative-update operators (framing, omission, focalization) that systematically place into the reader's state propositions that differ from the canonical fabula.

## Library claim (L1)

Prescriptive theories are **library-level operators** that constrain content at both substrate layers:

- **Fabula-level constraints:** required event types (reversal, realization, threshold, sacrifice), required causal roles (protagonist, antagonist, mentor), required character-state trajectories (transformation arcs from state A to state B through specified intermediates).
- **Sjuzhet-level constraints:** event selection, ordering (act proportions, beat placements), revelation timing.

The substrate does not know what a three-act screenplay is. The library knows.

## Narrator and focalization (minimal placeholder for the prototype)

The full narrator layer deserves its own sketch. For this substrate and the first prototype, the minimum requirement is per-scene metadata:

- `narrator_id` — identifier of the narrator entity (omniscient, first-person-as-A, free-indirect-via-A, ...).
- `focalizer_id` — which agent (or `:none` for omniscient) routes the reader's access.
- `reliability` — scalar or categorical summarizing how trustworthy the reader should take the narration to be.
- `stance` — rhetorical color (sympathetic, critical, ironic, neutral).

Richer models of narrator identity, voice, and rhetorical range come later.

## Enforcement (the expert-system layer's target)

The expert-system layer operates on this substrate. The queries it must support, all deterministic and runnable without LLMs, include:

- **Continuity.** Do all preconditions hold at their events' τ_s? Which violations, on which branches?
- **Knowledge consistency.** Do characters' utterances and actions respect their knowledge states?
- **Dramatic irony inventory.** Which reader-knows-but-character-doesn't asymmetries are currently live?
- **Sternberg inventory.** At τ_d, how many open gaps, blanks, and unresolved suspense threads does the reader hold?
- **Character integrity.** Do actions contradict established emotional or value states?
- **Pacing.** Event density, scene-length distribution, tension curve shape over τ_d.
- **Theme coherence.** (Likely requires a layer above the substrate.) Do selected events bear on the authorial argument?

## How the theories map onto the substrate

| Theory | Substrate mapping |
|--------|-------------------|
| Aristotle — peripeteia | A typed event whose effects reverse previously-fixed propositions about the protagonist's trajectory. |
| Aristotle — anagnorisis | A *realization* update operator on the protagonist's projection — a proposition migrates from gap/suspected to known. |
| Aristotle — hamartia | A past event in the protagonist's action history, later revealed (or not) to be causally linked to the peripeteia. |
| Propp — functions | The typed event vocabulary. 31 functions are types with partial-order constraints. |
| Propp — spheres of action | Typed roles in participant bindings. |
| Sternberg — interests | Queries over the reader's projection at τ_d against canonical fabula. |
| Dramatic irony | Cross-agent projection comparison. |
| MEXICA — engagement/reflection | Engagement operates on fabula + emotional projection; reflection operates on the full substrate to find impasses and violations. |
| MINSTREL — author goals | Library-layer operators above the substrate. |
| Façade — beats | Units of the sjuzhet grouping events for scheduling. |
| Three-act / Campbell / Freytag | Library-level operators constraining fabula and sjuzhet both. |
| Rashomon / *Turn of the Screw* | Contested branches of the fabula. |
| Unreliable narration | Narrative update operators on reader state that systematically deviate from canonical fabula. |

## Worked example (extended from sketch 01)

### Fabula events, canonical region (τ_s, type, participants, effects)

1. `E1 @ τ=T0`: *arrival*. Alice enters the kitchen. Precondition: Alice not in kitchen. Effects: *{Alice.location = kitchen}*. Witness: Bob.
2. `E2 @ τ=T0+1`: *observation*. Alice observes Bob holding a locket. Knowledge effect: Alice's state gains the proposition *{Bob.holding(locket)}* via diegetic-observation.
3. `E3 @ τ=T0+2`: *utterance-heard* (from Alice's perspective). Bob says to Alice, "This is my grandmother's." Knowledge effect on Alice: gains proposition *{locket.owner = Bob.grandmother}* with confidence = believed and provenance = utterance-from-Bob.
4. `E4 @ τ=T0-hours`: *observation* (canonical, but with no Alice-witness). Bob took the locket from Charlie's drawer. Effects: *{locket.location = Bob}*. Witness: none.

### Knowledge projection at τ=T0+2

**Alice's state:**
- Known: *{Alice.location = kitchen}*, *{Bob.holding(locket)}* (both via observation).
- Believed: *{locket.owner = Bob.grandmother}* (via utterance-heard, provenance Bob).
- Blank: E4 and everything implied by it.

**Bob's state:**
- Known: E4 and its implications, E1–E3.
- Believed: *{Alice's state does not include E4}* (meta-proposition about Alice's knowledge).

**Canonical fabula:**
- E4 is canonical; the locket was in Charlie's drawer hours before T0.
- *{locket.owner = Bob.grandmother}* is false on the canonical branch (or at least unsupported).

### Scenario A — narration includes E4 (reader sees the theft)

Sjuzhet includes E4 with a narrative update: *disclosure* to reader at some τ_d before the kitchen scene.

**Reader's state at the kitchen-scene τ_d:**
- Known (via disclosure): E4 — locket's origin, Bob's action.
- Known (via focalization): E1–E3 and Alice's state at those events.
- Held: *{Alice.believes(locket.owner = Bob.grandmother) ∧ canonical.fabula.contradicts(it)}* — awareness of the asymmetry.

Dramatic irony query: P_Alice.believes(locket.owner = Bob.grandmother) ∧ ¬canonical.supports(it) ∧ Reader.known(E4). **True.** Irony is live.

Sternberg-suspense: reader holds a gap about whether/how/when Alice will learn. **Open.**

### Scenario B — narration withholds E4

Sjuzhet excludes E4 from disclosure to date. E4 exists in the fabula but has no revelation yet.

**Reader's state at the kitchen-scene τ_d:**
- Known (via disclosure): E1–E3.
- Believed (via framing, since narrator delivered Bob's line without undercutting): *{locket.owner = Bob.grandmother}*.
- Blank: E4.

No irony is live yet. Reader tracks with Alice.

If the narration later discloses E4, a **retroactive reframing** operator migrates *{locket.owner = Bob.grandmother}* from reader's believed to reader's (probably) disbelieved, and E4 enters known. That migration is the Sternberg-surprise.

### Scenario C — contested fabula

Suppose the work is structured so that E4 is never canonically resolved — perhaps a later character claims Bob did not take the locket and the work refuses to adjudicate.

The fabula now contains E4 on branch `:b-theft` and a counter-event E4' ("Bob inherited the locket") on branch `:b-inheritance`. Both branches pass internal consistency checks independently. Queries about locket.owner return branch-indexed results.

Reader state may be shaped so the reader holds *both* branches (deliberate ambiguity), or one branch as believed with the other as suspected (reader bias), or neither as determined. Sternberg-curiosity is permanent in this case — the gap never closes.

## Open questions

1. **Event-type vocabulary.** How many types, at what grain, extensible by whom. The single largest design question; probably its own sketch.
2. **Inference model for characters.** The substrate needs a minimum capability; the max is a research problem. Candidate: bounded forward-chaining with per-agent rule sets. Own sketch.
3. **Emotional model.** PAD, OCC, custom? Own sketch.
4. **Reader inference approximation.** Readers don't just receive disclosures; they anticipate, revise, commit. Do we model this, approximate it, or leave it external? Open.
5. **Is the author an agent?** Dramatica says yes; Façade treats the author as a layer. Probably a layer, but this shapes the drama-management architecture.
6. **Scale at multi-grain time spans.** A 30-second duel and a 300-year dynasty in the same fabula. The partial-order graph handles it in principle; emotional and tension projections will need grain-aware decay. Implementation concern.
7. **Inconsistent fabula handling.** Distinct from contested: unintentional author contradictions (same event with incompatible canonical effects on the same branch). The substrate must surface these without silently preferring one.
8. **LLM integration discipline.** The LLM cannot be the source of truth. Candidate: LLM proposes, substrate validates, rejected proposals are retried. Needs its own sketch.
9. **Performance at novel scale.** Projections as naive folds don't scale. Memoization, incremental projections, snapshot anchors — implementation concerns the substrate must *permit*.
10. **Causality is not temporal order.** Events need explicit **causal warrants** linking event to prior causes. Candidate warrant types: *necessitates*, *enables*, *motivates*, *precipitates*, *forecloses*, *reveals*. Aristotle's "probability or necessity" becomes a property of the warrant graph. Minimal starter set for prototype: *enables*, *motivates*.
11. **Event identity and granularity.** Events should probably be hierarchical — coarse events contain fine events; queries parameterize by granularity level. To be tested in prototype.
12. **Focalization and narrator layer.** Minimal placeholder here (*{narrator_id, focalizer_id, reliability, stance}* per scene); full model deserves its own sketch.

## What this sketch does not yet give us

- A schema.
- An event vocabulary.
- An inference model.
- A generator.
- Running code.

The next artifact is the **concrete prototype** — the smallest implementation of this substrate on one worked story, to see where the design breaks before expanding it. The prototype's selection (worked story, stack, scope, persistence) is a separate decision still pending user input.
