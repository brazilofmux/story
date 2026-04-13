# Substrate — sketch 04 (consolidated)

**Status:** superseded
**Date:** 2026-04-13
**Supersedes:** [substrate-sketch-01.md](substrate-sketch-01.md), [substrate-sketch-02.md](substrate-sketch-02.md), [substrate-sketch-03.md](substrate-sketch-03.md)
**Superseded by:** [substrate-sketch-05.md](substrate-sketch-05.md)

## Purpose

The consolidated, self-contained statement of the substrate design. The three prior sketches are kept as historical record; this sketch is the one to read. The prototype that follows is built against this sketch.

Corrections folded in over sketch 03:

- **Branch-kind distinction (B1).** Sketch 03 conflated contested fabula, draft exploration, and counterfactual replay under one concept. Sketch 04 separates them; each has different semantics for persistence, query inclusion, and enforcement.
- **Branch reconvergence is an open question, not a solved property.** Sketch 03 claimed post-contested canonical facts return canonically "by construction." The sketch offered no mechanism to support that claim. Sketch 04 demotes it to a design question (open question 13) with three candidate resolutions and no silent default.
- **The worked example uses only declared epistemic slots.** Sketch 03's Scenario A slipped a line under *Held*, which is not one of the five slots. That line is now under *Known* with explicit provenance.
- **Event status simplified to a two-valued axis.** Sketch 03 had three statuses (canonical / contested / provisional); sketch 04 keeps only *committed* and *provisional*. Contested-ness is recognized as a derived cross-branch property of propositions rather than an event attribute, which removes the status × branch-kind ambiguity entirely and makes the status × branch-kind matrix small enough to enumerate.
- **Reader-interest queries are branch-aware.** Sketch 03's Sternberg and dramatic-irony formulations hard-coded canonical fabula. Sketch 04 parameterizes queries by branch, defaulting to canonical; in contested regions queries return branch-indexed results.
- **Fold scope across branches is explicitly defined.** Sketch 03's state-at-τ said "one fold per `:contested` branch" without saying what that fold included. Sketch 04 makes it a first-class rule: `:canonical` events are universal unless explicitly superseded on a child branch; a fold on branch b comprises b's own events plus its ancestors' events minus sibling `:contested` content.

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
4. **T1 — Fabula is authoritative where resolved; contested where not.** Events and derived propositions support a representation of ambiguity as a first-class substrate property, not as reader-side misunderstanding.
5. **K1 — Per-agent knowledge projection** computed by folding knowledge-affecting events.
6. **K2 — Same projection algebra, disjoint update operators.** The reader is an epistemic subject modeled with the same slot structure and algebra as characters, but updated by a distinct vocabulary of narrative operators.
7. **F1 — Emotion and tension as parallel projections** with the same discipline as knowledge.
8. **L1 — Library operates over fabula and sjuzhet both.** Prescriptive theories, genre templates, and author-goal structures are library-level operators; they may constrain both fabula content and sjuzhet selection/ordering. The substrate is neutral ontology.
9. **B1 — Branches have a declared *kind*.** Contested, draft, and counterfactual branches exist for different reasons, have different scopes of inclusion, and are treated differently by enforcement and queries. Event status and branch kind are orthogonal axes with enumerated legal combinations.

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
- **Branch label.** Events carry one or more branch labels identifying which branch (of which kind) they belong to. The distinguished `:canonical` label marks shipped canonical content.

### Events as the load-bearing primitive

Every event has, at minimum:

- `id` — stable identifier.
- `type` — member of a typed, extensible vocabulary.
- `τ_s` — story-time coordinate or partial-order constraint.
- `τ_a` — authored-time.
- `participants` — typed-role bindings to entities (`agent`, `patient`, `witness`, `location`, `instrument`, ...).
- `effects` — typed state changes (world-state mutations, knowledge-state mutations, emotional-state mutations, tension-state mutations).
- `preconditions` — typed propositions that must hold at τ_s for this event to be well-formed.
- `status` — one of { `committed`, `provisional` }. See *Event status and branch kinds* below.
- `branches` — one or more branch labels this event belongs to, each with its branch kind.
- `metadata` — genre tags, authorial notes, scene bindings, warrants (see open question 10).

State is not stored; state-at-τ is derived. (See *Facts and state*, below.)

### Partial order

Events are partially ordered in story-time. Ordering is expressed as a graph of relative constraints (*A before B*, *B concurrent with C*), with optional absolute anchors. Total order is a degenerate case. This matters because:

- Authors often know event relationships without knowing timestamps.
- Enforcement works cleanly over constraints; exact times are often a fiction.
- Branches may disagree about relative order, which the graph handles naturally.

## Event status and branch kinds (B1)

Two orthogonal axes:

### Event status — authorial commitment

- **`committed`.** The author has committed to this event's content. The event participates in work-level queries on every branch it appears on.
- **`provisional`.** The event is placed but not fully settled. Acceptable during authoring; should be resolved to `committed` (or removed) before the branch containing it ships.

That is all. There is no `contested` status. Whether a proposition is *contested* is a question about the fabula: if folding different `:contested` branches yields different answers for P, P is contested. Event status stays local to the event's own authorial state.

### Branch kind — what role the branch plays

- **`:canonical`.** Shipped canonical content. One per work by default.
- **`:contested`.** Represented ambiguity. Permanent. Each contested branch carries one candidate interpretation the work does not adjudicate. *Rashomon* has one `:contested` branch per testimony.
- **`:draft`.** Authoring sandbox. Not part of the work's content. Transient until promoted or discarded.
- **`:counterfactual`.** Analytical sandbox. Created by queries; per-query lifetime; never part of the work.

### Legal status × branch-kind combinations

| Branch kind | `committed` | `provisional` |
|---|---|---|
| `:canonical` | ✓ shipped canonical event | ✓ authoring in-progress, settle before ship |
| `:contested` | ✓ settled within this branch | ✓ authoring in-progress on this branch |
| `:draft` | ✓ draft has settled on this event | ✓ normal drafting state |
| `:counterfactual` | ✓ inherited from source branch, or posited by the query | ✗ counterfactuals are analytical posits, not authorial commitments — no provisional state |

Additional invariants:

- **Default branch is `:canonical`.** An event with no explicit branch label is on `:canonical`. Authoring most events without labels is the common case.
- **`:canonical` is universal unless superseded.** `:canonical` events are in scope on every branch that traces back to `:canonical` through its parent chain, unless a child branch explicitly supersedes them. This is what makes pre-divergence event sharing work without duplication.
- **Branch membership is a set.** An event may appear on multiple branches (trans-branch canonical declarations; events that apply on several contested interpretations; etc.). When an event appears on multiple branches, its status is invariant — the same event has the same status everywhere it appears.
- **Status is local to the event. Contested-ness is local to the proposition across branches.** An event is never both committed and contested; it is committed (or provisional), and the propositions it produces may or may not be contested depending on what other branches say.
- **`:counterfactual` branches inherit event content and status from their source branch** for unmodified events, and introduce their own `committed` events for the query's "what-if" posits. Counterfactual branches never contain `provisional` events.
- **`:draft` and `:counterfactual` branches are excluded from work-level queries by default.** Queries must explicitly opt in. Sjuzhet selection draws only from `:canonical` and `:contested` branches.

### Branch representation

Each branch label carries:

- **Label.** A stable identifier (`:canonical`, `:b-theft`, `:draft-alt-ending-3`, `:cf-remove-E4`).
- **Kind.** One of `:canonical`, `:contested`, `:draft`, `:counterfactual`.
- **Parent.** The label of the branch this one diverged from. Defaults:
  - `:canonical` has no parent (it is root).
  - `:contested` branches default to `:canonical` as parent (unless explicitly nested under another branch).
  - `:draft` and `:counterfactual` branches must name a parent (or source).
- **Metadata.** Authorial notes, creation τ_a, disposition history (for drafts and counterfactuals).

Events without an explicit branch label are implicitly labeled `:canonical`. Events and propositions refer to branches by label; queries filter by branch kind.

## Facts and state (with branching)

### A fact is a proposition produced by folding events

For a proposition P about entities at story-time τ_s:

- **In canonical regions (no `:contested` branches bear on P):** folding the canonical event log up to τ_s either makes P true, makes P false, or leaves P undetermined. The substrate returns a single result.
- **In contested regions (multiple `:contested` branches bear on P):** folding each `:contested` branch may produce different results for P. The substrate returns a **branch-indexed mapping** — `{ :b-a: true, :b-b: false, :b-c: undetermined }`.

Propositions that do not touch any contested region of the log are unambiguously single-valued even when contested regions exist elsewhere in the fabula. Branching is local to the events it involves; it does not globally taint unrelated propositions.

### State-at-τ

For a story-time τ_s and branch b:

- **If b is `:canonical`:** state is one fold — the union of all `committed` effects from `:canonical` events with τ_s' ≤ τ_s.
- **If b is `:contested`:** state is a fold over *the combined scope defined below*, tagged with b. Queries that cross multiple contested branches return a branch-indexed mapping of such folds.

### Fold scope across branches

The rule for which events are "in scope" when folding state for a given branch b:

- **`:canonical`.** Fold all events labeled `:canonical` at τ_s' ≤ τ_s.
- **`:contested` branch b.** Fold all events labeled `:canonical`, plus all events labeled b, at τ_s' ≤ τ_s. Do not fold events labeled on any other `:contested` branch unless they are also explicitly labeled b or `:canonical`.
- **`:draft` branch d with parent p.** Fold the scope of p, plus events labeled d, minus events explicitly superseded by d. Full draft-supersession semantics are covered under open question 14.
- **`:counterfactual` branch c rooted at source s.** Fold the scope of s, plus events posited by the query on c, minus events removed by the query on c.

Consequences that matter for the worked example:

- Pre-divergence events (E1–E3 in Scenario C) may be left on `:canonical` rather than duplicated on every sibling `:contested` branch. A query on `:b-theft` picks them up automatically via the canonical-is-universal rule; a query on `:b-inheritance` picks them up the same way; neither sees the other's contested events.
- A trans-branch-canonical declaration (open question 13) is still representable — label the event with `:canonical` rather than any one `:contested` branch.
- Sibling `:contested` branches do not inherit from each other. Divergent content stays divergent unless explicitly resolved.

**Downstream of contested regions:** the relationship between a contested region and later events authored on `:canonical` is *not* automatic. See open question 13. An event authored on `:canonical` whose preconditions depend on a proposition contested upstream requires explicit authorial resolution — either the event is branch-indexed across the upstream `:contested` branches, the upstream contest is merged, or the event is declared trans-branch-canonical and its effects specified in a way that is well-formed under every branch.

### Enforcement per branch

Every enforcement check runs **per branch**:

- Precondition checks: does E's precondition hold on branch b at E's τ_s?
- Knowledge consistency: does A's utterance at τ_s respect what A knows on branch b?
- Continuity: are the events on branch b mutually coherent?

A well-formed contested region is one in which each branch is internally consistent, even if the branches disagree with each other. Enforcement on `:draft` branches is advisory; enforcement on `:counterfactual` branches is analytical.

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
- **Believed.** Held with meaningful confidence but genuinely fallible; may be wrong relative to the relevant branch.
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

### Sternberg's interests as queries (branch-aware)

All Sternberg queries are parameterized by a branch `b`. For canonical-only stories the default is `b = :canonical`. In contested regions, queries either specify a branch or return branch-indexed results.

- **Suspense(τ_d, b).** Reader holds a proposition-shaped gap about a τ_s-future outcome (on branch `b`) whose alternatives are known. Reader-side only; but what counts as "the outcome" depends on which branch's fabula the reader is tracking.
- **Curiosity(τ_d, b).** Reader holds a proposition-shaped gap about a τ_s-past event (on branch `b`) whose existence is known but whose content or cause is not. In permanently split contested regions, curiosity on `b` may be permanently unresolvable — *the story does not answer the question*, which is a deliberate feature of ambiguous fiction.
- **Surprise(τ_d, b).** A new narrative update contradicts prior reader belief relative to branch `b`. In contested regions, an update that is a surprise on one branch may be consistency on another; both are reported.

These are queries, not stored fields. Inputs: the reader's projection, a branch label, the fabula filtered to that branch.

### Dramatic irony as a query (branch-aware)

At story-time τ_s between characters A and B, on branch `b`:

    P_A(τ_s, b).knows(F) ∧ ¬P_B(τ_s, b).knows(F) ∧ P_Reader(τ_d).knows_about(asymmetry_on_b)

In contested regions, irony is branch-indexed. There may be live irony on `:b-theft` and no irony on `:b-inheritance`. The enforcement layer runs irony queries per branch and reports a mapping; the dramatic value of the irony depends on which branch(es) the reader is tracking and with what confidence.

This reduces every Sophoclean-style irony, and its ambiguous-narration generalizations, to a lookup over the same structure.

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

- **Fabula.** The event log with story-time coordinates, including `:canonical`, `:contested`, `:draft`, and `:counterfactual` branches as they exist at a given τ_a. Partially ordered. The authoritative (where resolved) account of what happens in the story world.
- **Sjuzhet.** A selected and ordered sequence of fabula events, annotated with narrative-update metadata (focalizer, framing, disclosure acts), intended for narration. Not every fabula event appears in the sjuzhet. Sjuzhet selects from `:canonical` and `:contested` branches only; `:draft` and `:counterfactual` branches are not eligible.
- **Discourse.** The rendered prose / script / scene / interactive turn produced from the sjuzhet.

Authorial operations map cleanly:

- Writing a chapter = selecting sjuzhet events from the fabula, attaching narrative-update metadata, and rendering.
- A flashback = a sjuzhet event with τ_s in the past, τ_d now.
- Withholding = a fabula event not selected (yet).
- Reveal = a sjuzhet event whose narrative update migrates reader-state.
- Retcon = an authored-time edit to the fabula; sjuzhet and discourse re-derive.
- Unreliable-narrator arrangement = narrative-update operators (framing, omission, focalization) that systematically place into the reader's state propositions that differ from the canonical fabula.
- Draft exploration = `:draft` branches, promoted / merged / discarded.
- "What if" analysis = `:counterfactual` branches, created and discarded per query.

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
- **Dramatic irony inventory.** Which reader-knows-but-character-doesn't asymmetries are currently live, on which branches?
- **Sternberg inventory.** At τ_d on branch b, how many open gaps, blanks, and unresolved suspense threads does the reader hold?
- **Character integrity.** Do actions contradict established emotional or value states?
- **Pacing.** Event density, scene-length distribution, tension curve shape over τ_d.
- **Theme coherence.** (Likely requires a layer above the substrate.) Do selected events bear on the authorial argument?

All enforcement queries are branch-kind-aware (B1): `:contested` branches contribute to work-level answers; `:draft` branches produce advisory output; `:counterfactual` branches produce analytical output only.

## How the theories map onto the substrate

| Theory | Substrate mapping |
|--------|-------------------|
| Aristotle — peripeteia | A typed event whose effects reverse previously-fixed propositions about the protagonist's trajectory, on a specified branch. |
| Aristotle — anagnorisis | A *realization* update operator on the protagonist's projection — a proposition migrates from gap/suspected to known. |
| Aristotle — hamartia | A past event in the protagonist's action history, later revealed (or not) to be causally linked to the peripeteia. |
| Propp — functions | The typed event vocabulary. 31 functions are types with partial-order constraints. |
| Propp — spheres of action | Typed roles in participant bindings. |
| Sternberg — interests | Branch-aware queries over the reader's projection at τ_d against the fabula on a specified branch (canonical by default; branch-indexed in contested regions). |
| Dramatic irony | Cross-agent projection comparison, parameterized by branch. |
| MEXICA — engagement/reflection | Engagement operates on fabula + emotional projection; reflection operates on the full substrate to find impasses and violations. |
| MINSTREL — author goals | Library-layer operators above the substrate. |
| Façade — beats | Units of the sjuzhet grouping events for scheduling. |
| Three-act / Campbell / Freytag | Library-level operators constraining fabula and sjuzhet both. |
| Rashomon / *Turn of the Screw* | Parallel `:contested` branches, no reconvergence. |
| Unreliable narration | Narrative update operators on reader state that systematically deviate from the canonical fabula. |
| Authorial "what if" exploration | `:draft` and `:counterfactual` branches. |

## Worked example

### Fabula events, canonical region (τ_s, type, participants, effects)

All events below are on branch `:canonical` with status `committed`.

1. `E1 @ τ=T0`: *arrival*. Alice enters the kitchen. Precondition: Alice not in kitchen. Effects: *{Alice.location = kitchen}*. Witness: Bob.
2. `E2 @ τ=T0+1`: *observation*. Alice observes Bob holding a locket. Knowledge effect: Alice's state gains the proposition *{Bob.holding(locket)}* via diegetic-observation.
3. `E3 @ τ=T0+2`: *utterance-heard* (from Alice's perspective). Bob says to Alice, "This is my grandmother's." Knowledge effect on Alice: gains proposition *{locket.owner = Bob.grandmother}* with confidence = believed and provenance = utterance-from-Bob.
4. `E4 @ τ=T0-hours`: *observation* (canonical, but with no Alice-witness). Bob took the locket from Charlie's drawer. Effects: *{locket.location = Bob}*. Witness: none.

### Knowledge projection at τ=T0+2, branch `:canonical`

**Alice's state:**
- Known: *{Alice.location = kitchen}*, *{Bob.holding(locket)}* (both via diegetic observation).
- Believed: *{locket.owner = Bob.grandmother}* (via utterance-heard, provenance Bob).
- Blank: E4 and everything implied by it.

**Bob's state:**
- Known: E4 and its implications, E1–E3.
- Believed: *{Alice's state does not include E4}* (meta-proposition about Alice's knowledge; via inference).

**Canonical fabula:**
- E4 is committed on `:canonical`; the locket was in Charlie's drawer hours before T0.
- *{locket.owner = Bob.grandmother}* is false on the canonical branch (or at least unsupported).

### Scenario A — narration includes E4 (reader sees the theft)

Sjuzhet includes E4 with a narrative update: *disclosure* to reader at some τ_d before the kitchen scene.

**Reader's state at the kitchen-scene τ_d:**
- Known (via disclosure): E4 — locket's origin, Bob's action.
- Known (via focalization): E1–E3 and Alice's state at those events.
- Known (via inference from the above): the meta-proposition *{Alice.believes(locket.owner = Bob.grandmother) ∧ canonical.fabula.does-not-support(it)}* — the asymmetry itself.

Dramatic irony query on `:canonical`: P_Alice.believes(locket.owner = Bob.grandmother) ∧ ¬canonical.supports(it) ∧ Reader.known(E4). **True.** Irony is live.

Suspense(τ_d, :canonical): reader holds a gap about whether/how/when Alice will learn. **Open.**

### Scenario B — narration withholds E4

Sjuzhet excludes E4 from disclosure to date. E4 exists in the fabula but has no revelation yet.

**Reader's state at the kitchen-scene τ_d:**
- Known (via disclosure): E1–E3.
- Believed (via framing, since narrator delivered Bob's line without undercutting): *{locket.owner = Bob.grandmother}*.
- Blank: E4.

No irony is live yet. Reader tracks with Alice.

If the narration later discloses E4, a **retroactive reframing** operator migrates *{locket.owner = Bob.grandmother}* from reader's believed to reader's (probably) disbelieved, and E4 enters known. That migration is the Sternberg-surprise on `:canonical`.

### Scenario C — contested fabula

Suppose the work is structured so that E4 is never canonically resolved — perhaps a later character claims Bob did not take the locket and the work refuses to adjudicate.

Two `:contested` branches are introduced: `:b-theft` and `:b-inheritance`, both with parent `:canonical`. E4 is committed on `:b-theft`. A counter-event E4' ("Bob inherited the locket") is committed on `:b-inheritance`. Both branches pass internal consistency checks independently.

E1–E3 remain labeled `:canonical`. Per the fold-scope rule, a query on `:b-theft` picks them up (because `:canonical` is universal upstream of the contest), and a query on `:b-inheritance` picks them up too; neither picks up the other's contested event. The contest is about the locket's history, not Alice's arrival in the kitchen, and the labeling reflects that exactly.

Queries about `locket.owner`:

- On `:b-theft`: locket.owner = Charlie (or Charlie's estate), Bob obtained it via theft.
- On `:b-inheritance`: locket.owner = Bob, acquired legitimately.

Reader state may be shaped so the reader holds *both* branches (deliberate ambiguity), or one branch as believed with the other as suspected (reader bias), or neither as determined. Curiosity(τ_d, :b-theft) and Curiosity(τ_d, :b-inheritance) are each open, and neither closes — the story does not answer the question.

**Note on downstream events:** any later event that depends on locket.owner must be explicitly resolved per open question 13. The author may publish the event on both contested branches (with differing effects), merge the branches before the event, or declare the event trans-branch-canonical. Nothing is automatic.

### Scenario D — counterfactual query

A tool query asks, "How much of the story's tension comes from E4?" The substrate creates a `:counterfactual` branch `:cf-no-E4` rooted at `:canonical` with E4 removed. Projections and tension are recomputed on that branch. The answer is the delta between canonical and counterfactual tension curves.

`:cf-no-E4` is discarded when the query completes. No event in the work references it; the reader never encounters it; enforcement treats it as analytical output only. All events on `:cf-no-E4` are status `committed` (inherited or posited); counterfactual branches never contain `provisional` events.

## Open questions

1. **Event-type vocabulary.** How many types, at what grain, extensible by whom. The single largest design question; probably its own sketch.
2. **Inference model for characters.** The substrate needs a minimum capability; the max is a research problem. Candidate: bounded forward-chaining with per-agent rule sets. Own sketch.
3. **Emotional model.** PAD, OCC, custom? Own sketch.
4. **Reader inference approximation.** Readers don't just receive disclosures; they anticipate, revise, commit. Do we model this, approximate it, or leave it external? Open.
5. **Is the author an agent?** Dramatica says yes; Façade treats the author as a layer. Probably a layer, but this shapes the drama-management architecture.
6. **Scale at multi-grain time spans.** A 30-second duel and a 300-year dynasty in the same fabula. The partial-order graph handles it in principle; emotional and tension projections will need grain-aware decay. Implementation concern.
7. **Inconsistent fabula handling.** Distinct from contested: unintentional author contradictions (same event with incompatible effects on the same branch). The substrate must surface these without silently preferring one.
8. **LLM integration discipline.** The LLM cannot be the source of truth. Candidate: LLM proposes, substrate validates, rejected proposals are retried. Needs its own sketch.
9. **Performance at novel scale.** Projections as naive folds don't scale. Memoization, incremental projections, snapshot anchors — implementation concerns the substrate must *permit*.
10. **Causality is not temporal order.** Events need explicit **causal warrants** linking event to prior causes. Candidate warrant types: *necessitates*, *enables*, *motivates*, *precipitates*, *forecloses*, *reveals*. Aristotle's "probability or necessity" becomes a property of the warrant graph. Minimal starter set for prototype: *enables*, *motivates*.
11. **Event identity and granularity.** Events should probably be hierarchical — coarse events contain fine events; queries parameterize by granularity level. To be tested in prototype.
12. **Focalization and narrator layer.** Minimal placeholder here (*{narrator_id, focalizer_id, reliability, stance}* per scene); full model deserves its own sketch.
13. **Branch reconvergence semantics.** When a contested region has canonical events downstream that depend on propositions the contest left unresolved, the substrate has three candidate resolutions, none of which is automatic:
    - **Permanent split.** Once branches diverge on a contested proposition, every downstream event that depends on it is also branch-indexed. The fabula effectively splits from the divergence point for any proposition reachable from it. *Rashomon* works this way.
    - **Explicit authorial merge.** The author declares at some τ_s that branches reconverge. A *merge event* specifies how post-merge state combines (e.g., "regardless of how Bob acquired the locket, it is in his hand at the wedding"). Pre-merge branches remain available for analysis.
    - **Trans-branch canonical declaration.** Individual events or propositions are declared canonical across all contested branches by authorial fiat — they happen or hold the same way on every branch even if the paths to them differ.

    These are not mutually exclusive; real stories combine them. The substrate must support all three, and must refuse to silently pick one when the author has not. The prototype can start with permanent-split as the default and add merge/declaration as needed.

14. **Draft supersession semantics.** `:draft` branches are meant to let authors explore alternatives to parent events, which requires a mechanism for a draft to override, modify, or remove events inherited from its parent. Several candidate mechanisms, none yet chosen:
    - **Event-level supersession.** A draft records explicit `supersedes(event_id)` links; folding a draft skips superseded events and applies the draft's replacements.
    - **Effect-level override.** A draft marks specific effects of a parent event as overridden without removing the event itself — useful for small changes (different dialogue, different witness set) that don't warrant a full replacement.
    - **Removal.** A draft records an explicit `removes(event_id)` marker, skipping the event entirely without replacement.

    Additional sub-questions: how supersessions compose when drafts are stacked (draft-of-draft); what happens to downstream events whose preconditions depended on a superseded event; and how a draft is *promoted* to canonical — does the promotion rewrite the canonical log in place (losing the supersession history), or append the draft's events with retained supersession metadata (preserving authored-time history at the cost of log clutter). The prototype can begin with event-level supersession and append-on-promote; richer mechanisms added if the simple model breaks.

## What this sketch does not yet give us

- A schema.
- An event vocabulary.
- An inference model.
- A generator.
- Running code.

The next artifact is the **concrete prototype** — the smallest implementation of this substrate on one worked story, to see where the design breaks before expanding it. The prototype's selection (worked story, stack, scope, persistence) is a separate decision still pending user input.
