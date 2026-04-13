# Prototype — substrate reference implementation

A small Python implementation of the substrate design in
`../design/substrate-sketch-04.md`, exercised on a slice of *Oedipus Rex*.
This is the first executable artifact of the project. It exists to pressure-
test the sketch by making the semantics run.

## Goals

- Make the design concrete enough to find problems that paper cannot.
- Produce a tangible dramatic-irony demonstration that pays off the sketch.
- Serve as a specification a future reader can port to another language
  without guessing intent. Python here is a specification language, not a
  target.

## Non-goals

- Performance. The fold is recomputed on every query; no memoization.
- Completeness. Large swaths of the sketch are deliberately deferred — see
  *What's deferred*, below.
- Authoring ergonomics. Events are constructed as Python objects; no DSL,
  no loader, no authoring UI.

## Run

```sh
cd prototype
python3 demo.py
```

No dependencies beyond the Python 3.12 standard library. No virtualenv needed.

## Files

- `substrate.py` — the engine. Event, Prop, Branch, Held, Effect types;
  the fold-scope rule; knowledge-projection and world-projection folds;
  reader-projection from a sjuzhet; dramatic-irony and Sternberg-curiosity
  queries.
- `oedipus.py` — the encoded story. Entities, proposition constructors,
  the pre-play and in-play fabula, the sjuzhet for the Messenger +
  Shepherd → anagnorisis slice. No substrate logic; this is content.
- `demo.py` — the driver. Prints a per-τ_d report showing reader and
  character states, live ironies, and anagnorisis deltas on a set of
  central propositions.

## What the demo demonstrates

For a sequence of discourse-time milestones in the play, the report
displays the state of four central propositions:

- `killed(Oedipus, Laius)`
- `child_of(Oedipus, Laius)`
- `child_of(Oedipus, Jocasta)`
- `married(Oedipus, Jocasta)`

For each milestone:

- **Reader state.** The reader enters at τ_d=0 with the myth's key
  facts already in hand (pre-play disclosures); the reader's knowledge
  does not decrease during the play.
- **Oedipus's state.** Starts with only `married()` as KNOWN. Through the
  scene the propositions migrate through SUSPECTED and are eventually
  KNOWN at the anagnorisis.
- **Jocasta's state.** Starts with the parentage facts as KNOWN (she
  bore Oedipus; she knows who his father was) but not the identity of
  Laius's killer. Realizes before Oedipus does.
- **Live ironies** on the central propositions.
- **Anagnorisis deltas** for Jocasta (τ_d=9) and Oedipus (τ_d=13),
  showing specifically which propositions were removed, migrated, or
  added by the realization event.

## The payoff

The demo makes three features of the substrate visible:

1. **Dramatic irony as a query, not a narrative feature.** The substrate
   does not know anything about tragedy or irony. It computes per-agent
   knowledge states by folding events and asks "who knows what the reader
   knows, and who doesn't?" The Oedipus Rex irony is the output of that
   query. Any other story with the same structure would yield the same
   query results.

2. **The anagnorisis as a typed event.** Aristotle's realization is here
   a `REALIZATION` update operator: propositions migrate from SUSPECTED
   to KNOWN, false beliefs are dislodged, a gap is closed. The event is
   authored explicitly (the prototype has no general inference model) but
   its mechanics are substrate-native.

3. **Reader as an agent.** The reader has the same epistemic-slot
   vocabulary (KNOWN, BELIEVED, SUSPECTED, GAP) as characters. The
   reader's state is updated by a different vocabulary — narrative
   operators, not diegetic ones. In this first prototype only
   DISCLOSURE is behaviorally active; FOCALIZATION is recorded as
   metadata but does not currently modify reader state (see
   *Focalization, honestly* below).

## Focalization, honestly

Sketch 04 K2 defines focalization as a **constraint** on reader access:
propositions the focalizer lacks become reader-gaps; propositions the
focalizer misconstrues become reader-believed rather than reader-known.

A first pass of this prototype implemented focalization as a **bulk
copy** of the focalizer's knowledge state into the reader's state (with
a "don't downgrade prior knowledge" guard). That was wrong in a specific
way: it collapses "the scene is routed through this character's
perspective" into "the narration dumps the contents of this character's
mind into the reader." Those are not the same operation. Focalization
tells the reader *whose blind spots are in view* — it does not grant
the reader access to the focalizer's entire epistemic history.

Proper constraint semantics — demote reader propositions the focalizer
lacks, for the scope of the focalized entry — requires τ_d-scoped
tracking of reader state that this prototype does not yet have. Demoting
globally would contradict prior disclosures and make reader state
unstable under replay.

The current implementation therefore records focalization as **metadata
only**. The focalizer_id is preserved on each sjuzhet entry for
inspection and for later use by a reader-model layer, but no automatic
state mutation occurs. Disclosures remain the only positive-update
operator on the reader.

This is weaker than sketch 04 asserts and is a deliberate deferred item.
A later sketch (and prototype iteration) should nail down:
- interaction between focalization-induced demotion and prior disclosure
- τ_d scope of focalization (one entry, a span, an arc)
- what "misconstrues" means operationally (confidence mismatch? belief
  content mismatch?)

## An honest note on the Jocasta delta

At τ_d=9 Jocasta's anagnorisis delta shows only two items — her prior
`BELIEVED dead(Oedipus)` is removed and `KNOWN killed(Oedipus, Laius)`
is added. The realization event also does `realize_add` for Oedipus's
parentage, but those propositions were *already* in Jocasta's state
since the E_birth event (she was there; she witnessed). She is not
learning new parentage facts; she is realizing that the man she married
*is* that son. The fold is honest about this: no-op re-additions are not
a state change and do not appear in the delta.

A more expressive encoding would add a composite proposition like
"the-man-I-married-is-the-son-I-bore" that Jocasta genuinely gains at
τ_s=9. The prototype does not yet do this. It surfaces a real modeling
question: some realizations are about new facts; others are about new
*connections between* facts already held. The substrate currently
privileges the first kind. See open question 2 in sketch 04 (inference
model) — a proper account of realization-as-integration likely requires
derived propositions or a composite-proposition mechanism.

## What's implemented

- **E1, E2, E3.** Event-primary substrate with typed events and tri-temporal
  fields. (Partial order is available structurally but not exercised; the
  total-order traversal suffices for the slice.)
- **K1.** Per-agent knowledge projection by fold.
- **K2.** Reader as epistemic subject with disjoint narrative update
  operators. Diegetic operators used: observation, utterance-heard,
  inference, realization. Narrative operators: DISCLOSURE is fully
  behavioral; FOCALIZATION is metadata-only for now (see
  *Focalization, honestly* above).
- **B1.** Branch labels, kinds, fold-scope rule. The scope logic runs on
  every query; the encoded story happens to place every event on
  `:canonical`, so scope degenerates cleanly. Adding a `:contested`
  branch would require no substrate changes.
- **Dramatic irony query.** Both Reader > Character and Character >
  Character ironies (with reader aware).
- **Sternberg curiosity gaps.** Reports propositions in the reader's GAP
  slot. None in the current slice because the reader is effectively
  omniscient.

## What's deferred

Pulled in later, as the prototype earns iterations:

- **F1** — emotional and tension projections.
- **Partial order** — structure is in place; no partial-order solver yet.
- **Contested branches** — supported by the fold-scope rule; no example
  uses one. Adding *Rashomon* or *Turn of the Screw* material would
  exercise this without substrate changes.
- **Draft / counterfactual branches** — as above. See open questions
  13 and 14 in sketch 04.
- **Proper focalization semantics** — currently metadata-only; see
  *Focalization, honestly*.
- **Narrative operators beyond disclosure and focalization** —
  omission, framing, retroactive reframing.
- **Causality warrants** (sketch 04 open question 10) — the prototype
  uses only preconditions (no examples trigger them yet).
- **BLANK slot** — collapsed to GAP. Adding a distinct BLANK requires
  a case that discriminates them.
- **Inference model** — realizations are authored events. A bounded
  forward-chaining inference layer is the natural next addition; see
  sketch 04 open question 2.
- **Performance.** Naive fold on every query. Memoization and snapshot
  anchors are sketch 04 open question 9.

## Porting notes

Python here is a specification language. A C#, Rust, or Go port should be
mostly mechanical:

- Prop is a hashable record with a predicate string and a tuple of
  arguments. Preserve value equality.
- Held is an immutable value.
- Effects are a tagged union (`KnowledgeEffect` or `WorldEffect`). Prefer
  explicit union types over subclass inheritance.
- The fold is a pure function from (events-in-scope, branch, τ) to state.
  Caller orchestrates when to recompute.
- The branch scope rule is deliberately simple and should port literally.

If the target language distinguishes agents from entities via a type
hierarchy, keep `Agent : Entity` as the natural relation. The Python
prototype collapses this into a `kind` field to keep porting trivial.
