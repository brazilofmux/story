# Substrate — sketch 02

**Status:** superseded
**Date:** 2026-04-13
**Supersedes:** [substrate-sketch-01.md](substrate-sketch-01.md)
**Superseded by:** [substrate-sketch-04.md](substrate-sketch-04.md) (via sketch 03, also superseded)

*Kept in place as historical record. [Sketch 04](substrate-sketch-04.md) is the current active substrate sketch. Sketch 03 was an intermediate consolidation that fixed sketch 02's fact/state inconsistency and slot-naming issues but conflated branch uses under one concept and claimed post-contested canonical consistency "by construction"; sketch 04 separates branch kinds and demotes the reconvergence claim to an open question.*


## Purpose

Revise three load-bearing commitments from sketch 01 and add three open questions that sketch missed. Everything sketch 01 said that isn't revised here still stands; refer back to it for context, the worked example, and the unrevised commitments.

This is a **delta sketch**, not a restatement. It exists so that the concrete prototype that follows is not built on sketch 01's errors.

## What's carried forward unchanged from sketch 01

- E1 — Event-primary substrate; state is a fold over the event log.
- E2 — Events are typed and partially ordered in story-time.
- E3 — Three time axes: story-time (τ_s), discourse-time (τ_d), authored-time (τ_a).
- K1 — Per-agent knowledge projection P_A(τ_s) computed by folding knowledge-affecting events.
- F1 — Emotional and tension state as parallel projections with the same shape as knowledge.
- Fabula / sjuzhet / discourse as three distinct representations.

## What changes

### T1 — revised from "single ground truth" to "authoritative where resolved, ambiguous where not"

**Old T1:** "The substrate represents story-time truth, not narrative truth. What a character believes lives in the knowledge layer; what happened lives in the event log. Unreliable narration is expressed as a disagreement between reader-projection and ground-truth event log, not as ambiguity in the event log itself."

**Problem:** This excluded a significant class of literary fiction — *The Turn of the Screw*, Rashomon-style contradictory testimony, *Mulholland Drive*-style dream/reality collapse, magical realism, and any story that deliberately refuses to settle what "really happened." Those are not unreliable-narrator-over-fixed-fabula structures. They are fabulas that are themselves under-resolved.

**New T1:**

The fabula is an **authoritative event layer** — the substrate's best account of what happens in the story world — but it is not required to be fully resolved. Events in the fabula carry a **resolution status**:

- **Canonical.** Settled; the substrate treats it as ground truth.
- **Contested.** Multiple mutually inconsistent candidate events exist with equal authorial endorsement; the fabula permanently holds all of them. Queries over contested regions return a set of interpretations, not a single fact.
- **Provisional.** An event is committed at authored-time N pending possible revision at N+k. The substrate allows this in draft; shipping drafts should resolve provisionals or convert them to contested.

For most events in most stories, *canonical* is the right and default status. The presence of a contested-events mechanism is the scope-widening commitment: it lets the substrate hold ambiguity as a first-class property of the fabula, not as a reader-side misunderstanding.

**Consequences:**

- Character beliefs still live in the knowledge layer; nothing changes there.
- Unreliable narrators still work as reader-projection disagreement with canonical fabula — this was not wrong, only incomplete.
- Ambiguous stories work as multiple contested branches in the fabula with no authorial tiebreaker.
- Enforcement queries ("does Alice's utterance respect what she knows") work over each candidate branch independently.
- **Cost:** downstream layers (inference, enforcement, reader-projection) must be branch-aware in contested regions. This is real complexity. Acknowledged up front.

### K2 — refined: same algebra, different update operators

**Old K2:** "The reader is an agent in the same knowledge system, with the same projection machinery."

**Problem:** "Same machinery" over-collapsed two genuinely different epistemic situations. A character *witnesses* events in-world — perception, physical presence, being-there. A reader *receives narrated disclosures* — mediated by who is telling, which facts are included or omitted, what is foregrounded, what rhetorical frame surrounds the report. Same projection *shape*; different update *operators*; different *inputs*.

**New K2:**

The reader is an **epistemic subject** modeled with the same projection algebra as characters (a running knowledge state, with witnessed / inferred / heard / believed / blanks / gaps slots) but with a distinct and richer set of **update operators**:

- **Diegetic updates (characters):** observation, utterance heard directly, inference from current knowledge, deception by another agent, forgetting, realization. These are in-world epistemic events.
- **Narrative updates (reader):** a disjoint vocabulary.
  - **Disclosure.** The narration reveals a fact to the reader. May or may not be revealed to any character.
  - **Focalization.** The narration routes the reader's access to the world through a specific agent's perspective (or none, for omniscient narration). Facts the focalizer lacks become reader-gaps; facts the focalizer misinterprets become reader-beliefs.
  - **Omission.** A fact is withheld. Creates a reader-blank (reader doesn't know they don't know) or a reader-gap (if the omission is hinted).
  - **Framing / rhetoric.** Facts are colored — trustworthy, suspicious, ironic, pathetic. Affects the *confidence* with which the reader holds a belief, not just its content.
  - **Retroactive reframing.** A later narrative act causes the reader to re-interpret earlier material. Surprise-via-revelation is the canonical instance; unreliable-narrator reveals (Gone Girl, The Murder of Roger Ackroyd) are the extreme.

Characters never "focalize" or "retroactively reframe." Those are not in-world operations; they are authorial operations on the reader. Collapsing them into observation/utterance would lose the distinction between what happens and how it is told — which is the fabula/sjuzhet/discourse split, at the reader-model layer.

**Consequences:**

- The reader's projection is still a fold, still returns a knowledge state, still supports the Sternberg queries from sketch 01.
- The fold function for the reader reads the **sjuzhet** (and its framing metadata), not the fabula directly. This is the correct formalization: the reader knows only what the narration has delivered, in the form the narration has delivered it.
- **Focalization is now a first-class concept,** which it was not in sketch 01. See open question 12.

### Library claim — broadened: prescriptive structures are operators over fabula + sjuzhet, not sjuzhet alone

**Old claim:** "Prescriptive story structures (Freytag, three-act, monomyth) belong in a template library at the sjuzhet-selection layer, not in the substrate."

**Problem:** Correct that they stay out of the substrate; too narrow in locating them only at sjuzhet selection. Some prescriptive-structure elements are fabula-level claims:

- *Peripeteia* is a reversal of the protagonist's fortune — a fabula-level causal claim, not a sjuzhet placement.
- Campbell's *threshold crossing* is a fabula-level causal event that changes the protagonist's world-access, not just a narrative beat.
- Three-act's *plot point 1* requires the protagonist to be locked into the main problem — a fabula-level commitment about causal agency.
- *Character transformation arcs* (change vs. steadfast, in Dramatica's vocabulary) are fabula-level sequences of events on the protagonist's belief/value state.

**New claim:**

Prescriptive theories are **library-level operators over fabula and sjuzhet both**, not substrate ontology and not sjuzhet-only. They constrain:

- Which **fabula-level event types** must occur (reversal, realization, threshold, sacrifice, return).
- Which **causal roles** must be filled (protagonist, antagonist, mentor, threshold guardian — Propp's spheres generalized).
- What **character-state trajectories** are well-formed (transformation from state A to state B via a specific sequence of belief/value changes).
- What **sjuzhet selections and orderings** are well-formed for a given template (act proportions, beat placements, revelation timing).

The substrate supports all of this by remaining typed, partially-ordered, and neutral. It is the template-library's job to encode what e.g. "a three-act screenplay" asserts about the fabula and the sjuzhet. **The substrate does not know what a three-act screenplay is; the template library does.**

## New open questions

Numbered continuing from sketch 01.

### 10. Causality is undernamed

Sketch 01 treated story-time order (and partial-order constraints) as if they were equivalent to causation. They are not. *A happens before B* is a temporal claim; *A causes B* is a causal claim. Stories depend on both.

**Proposed commitment (to be validated in the prototype):** Events carry explicit **causal warrants** — typed links from an event to the prior events it causally depends on. Warrants are authorial annotations, not inferences. They are used by the enforcement layer ("if E caused F, removing E invalidates F") and by the reader-inference approximation ("the reader can plausibly connect F to its warrants if disclosed").

Candidate warrant types: *necessitates*, *enables*, *motivates*, *precipitates*, *forecloses*, *reveals*. The vocabulary is another library question. A minimal starter set (*enables*, *motivates*) is probably enough for the prototype.

**Implication:** Aristotle's "probability or necessity" becomes a property of the warrant graph — are the events in the fabula connected by well-typed warrants, or are they merely contiguous in time?

### 11. Event identity and granularity

Is "Alice enters the kitchen" one event, or three (approaching the door, opening it, crossing the threshold), or a bundle within a larger "Alice confronts Bob" event? The substrate has been silent; this is a first-class design question.

**Tentative position:** Events are **authored at the grain the story cares about**, and can be **hierarchical** — coarse events contain fine events, and queries operate at whatever level the caller asks for. Alice-enters-kitchen is one event for continuity-check purposes and three events if a scene turns on what she noticed between opening the door and crossing the threshold. Both views are valid; they are views over the same log.

**Implication:** The prototype must decide on a grain-flexible representation. Likely: events carry an optional *parent* link, and queries are parameterized by the granularity level.

### 12. Focalization and the narrator layer

K2 now treats focalization as a first-class narrative-update operator, but sketch 01 had no model of *who is telling* or *from whose perspective the reader is seeing*. A story engine without a narrator layer can produce the facts of a scene but not its point of view, tone, irony, or trust.

**Components the narrator layer must supply:**

- **Narrator identity** — omniscient, first-person-limited-to-agent-A, unreliable-first-person, free-indirect-via-A, dramatic-present. The narrator is itself an authored entity with properties.
- **Focalizer per scene (or per sentence)** — whose access to the world is being routed through. Focalizer and narrator may be different (omniscient narrator focalizing through Alice).
- **Reliability.** How much the reader should trust the narrator's framing and omissions. Unreliability is a narrator property, not a fabula property.
- **Rhetorical stance.** The narrator's relation to the events — sympathetic, critical, ironic, neutral. Affects framing-metadata attached to sjuzhet events.

**Implication:** This is probably its own sketch (narrator-sketch-NN), but the prototype needs at least a minimal narrator representation to exercise the K2 revision. A placeholder of *{ narrator_id, focalizer_id, reliability_scalar }* per scene is enough for the first prototype.

## Status of the commitments after this sketch

Seven commitments from sketch 01, now corrected:

1. E1 (event-primary). **Unchanged.**
2. E2 (typed, partially-ordered events). **Unchanged.**
3. E3 (tri-temporal). **Unchanged.**
4. K1 (per-agent knowledge projection). **Unchanged.**
5. K2 (reader as epistemic subject). **Refined** — same algebra, different update operators.
6. F1 (emotion/tension as parallel projections). **Unchanged.**
7. T1 (fabula as authoritative, potentially unresolved). **Revised** — no longer requires full resolution.

Plus one new commitment:

8. **L1 — Library operates over fabula and sjuzhet both.** Prescriptive theories, genre templates, and author-goal structures are library-level operators that can impose constraints at both the fabula and sjuzhet layers. The substrate is neutral ontology.

And three new open questions joining sketch 01's nine:

10. Causality requires explicit warrants, not just temporal order.
11. Event identity and granularity — hierarchy with per-grain queries, tentatively.
12. Focalization and narrator layer — first-class, likely its own sketch, minimal placeholder in the prototype.

## Path to the next sketch

Sketch 03 will be the **concrete prototype plan**: smallest implementation of this substrate on one worked story, to see where the design breaks before it is expanded. Candidate stories, tech stack, and scope for the prototype will be proposed there and selected with the user.

The prototype is the point. This sketch exists so that the prototype tests corrected commitments, not the ones sketch 01 got wrong.
