# Prototype — substrate reference implementation

A small Python implementation of the substrate design in
`../design/substrate-sketch-04.md`, exercised on two encoded stories:
a slice of *Oedipus Rex* (dramatic irony on `:canonical`) and the grove
scene from *Rashomon* (four sibling `:contested` branches). This is the
first executable artifact of the project. It exists to pressure-test
the sketch by making the semantics run.

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
python3 demo.py                  # narrative report on the Oedipus slice
python3 demo_rashomon.py         # branch-indexed report on the Rashomon grove scene
python3 test_substrate.py        # permanent substrate tests (no framework)
python3 test_identity.py         # identity & realization tests
python3 test_inference.py        # rule-derivation tests (inference-01 N1-N10)
python3 test_dramatic.py         # Dramatic dialect M1-M10 + M8 verifier tests
python3 test_rashomon.py         # permanent contested-branch tests (no framework)
python3 test_proposal_walker.py  # walker tests (io.StringIO-driven, no terminal)

# Live reader-model probe — requires ANTHROPIC_API_KEY and the deps in
# requirements.txt. Use `--dry-run` to print the full prompt without calling
# the API, or `--walk` to drop into an interactive accept/decline/skip walker
# over the returned reviews and answer proposals.
.venv/bin/python3 demo_reader_model.py --dry-run            # Rashomon (:b-woodcutter)
.venv/bin/python3 demo_reader_model_oedipus.py --dry-run    # Oedipus (:canonical, through anagnorisis)
.venv/bin/python3 demo_reader_model_macbeth.py --dry-run    # Macbeth (:canonical, full play)
.venv/bin/python3 demo_reader_model.py --walk
.venv/bin/python3 test_reader_model_client.py  # client structural tests
```

The substrate, Oedipus, and Rashomon demos use only the Python 3.12 standard
library. The reader-model probe adds `anthropic` and `pydantic` (see
`requirements.txt`); install into a local venv.

## Files

- `substrate.py` — the engine. Event, Prop, Branch, Held, Effect types;
  the fold-scope rule; knowledge-projection and world-projection folds;
  reader-projection from a sjuzhet; dramatic-irony and Sternberg-curiosity
  queries; identity substitution machinery (identity-and-realization-01);
  Rule / Proof / holds_derived / derive_all / world_holds_derived
  (inference-model-sketch-01 N1–N10) — Horn-clause rules with conjunctive
  bodies, query-time derivation composed with identity substitution,
  per-fold scoping, weakest-premise slot propagation, bounded fixpoint
  with depth cap (default 3), proof-carrying derivation, authored-wins
  over derivation.
- `oedipus.py` — the encoded *Oedipus Rex* slice. Entities, proposition
  constructors, the pre-play and in-play fabula, the sjuzhet for the
  Messenger + Shepherd → anagnorisis slice. Exports a `RULES` tuple
  (PARRICIDE_RULE, INCEST_RULE) per inference-model-sketch-01; the
  compound predicates that were formerly author-asserted at canonical
  events now derive at query time. No substrate logic; content only.
  Used by `demo.py`.
- `rashomon.py` — the encoded *Rashomon* grove scene. Canonical floor
  (travel, lure, binding, bare fact of intercourse, body discovery)
  plus four sibling `:contested` branches — one per testimony, including
  the woodcutter's later confession. Per-branch sjuzhets share a
  canonical preamble and a canonical closing panel. No substrate logic;
  content only. Used by `demo_rashomon.py` and `test_rashomon.py`.
- `dramatic.py` — first-pass implementation of the Dramatic dialect
  (dramatic-sketch-01 M1-M10). Self-contained: no substrate imports.
  Eight record types (Story, Argument, Throughline, Character, Scene,
  Beat, Stakes, Template) plus helper records (FunctionSlot,
  ArgumentContribution, SceneAdvancement, StakesOwner) and four enums
  (FunctionMultiplicity, ResolutionDirection, ArgumentSide,
  StakesOwnerKind). Four shipped Templates: dramatica-8 (eight
  EXACTLY_ONE slots), three-actor (Hero+Obstacle+Helper), two-actor,
  ensemble. M8 self-verifier with eight checks emitting Observations
  (id resolution, beat sequencing, scene sequencing, template
  conformance with multiplicity, soft argument completeness, stakes
  coverage, scene purpose, orphans). Description surface deferred to
  a follow-on pass; cross-dialect Lowering integration lives in a
  separate module yet to be written.
- `oedipus_dramatic.py` — *Oedipus Rex* encoded in the Dramatic
  dialect. First encoding at this layer (parallel to `oedipus.py` at
  the substrate level). One Argument, four Throughlines under the
  dramatica-8 Template, six Characters (Antagonist deliberately
  unfilled), ten Scenes, two Stakes records, twenty Beats. Verifier
  produces exactly three observations on this encoding: the
  intentional Antagonist gap and two missing-Stakes observations
  (T_impact_jocasta and T_relationship_oj have no separate Stakes
  records — a real authoring choice). No id-resolution errors.
- `macbeth_dramatic.py` — *Macbeth* encoded in the Dramatic dialect.
  Second encoding at this layer (parallel to `macbeth.py` at the
  substrate level). One Argument, four Throughlines under the
  dramatica-8 Template, nine Characters (all dramatica-8 slots
  filled — Macduff = Antagonist + Skeptic, Macbeth = Protagonist +
  Emotion, etc.), fourteen Scenes spanning the full play, four
  Stakes records (one per Throughline; Macbeth's stakes are
  genuinely separable across Throughlines, unlike Oedipus's),
  twenty-five Beats. Verifier produces zero observations on this
  encoding. Multi-antagonist alternatives (Lady Macbeth, the
  Witches, Macbeth himself) documented but not encoded; a test
  fixture in `test_dramatic.py` exercises the verifier's overfilled-
  slot path by adding Antagonist to Lady Macbeth.
- `macbeth.py` — the encoded *Macbeth*. Canonical-only; 22 fabula events
  (full arc: pre-play heroism through Macbeth's defeat at Dunsinane and
  Malcolm's coronation); 19 sjuzhet entries in roughly linear order; 7
  descriptions including three authorial-uncertainty questions (the
  Witches' ontology, the banquet ghost's ontology, and the authored-
  compound-predicate derivation candidates). Parallel in shape to
  `oedipus.py` — no identity placeholders (Macbeth doesn't confuse who
  is who), Shakespeare-level encoding of moral trajectory rather than
  Oedipus's epistemic inversion. Exports a `RULES` tuple (KINSLAYER_RULE,
  REGICIDE_RULE, BREACH_OF_HOSPITALITY_RULE, TYRANT_RULE) per
  inference-model-sketch-01; the compound predicates that were formerly
  author-asserted at the killing events now derive at query time.
  TYRANT_RULE is the only depth-2 rule (consumes two depth-1 derivations
  plus an authored king fact). Pressure-tests the substrate on the
  structurally different story that `lowering-sketch-02` sketched.
- `demo.py` — the Oedipus driver. Prints a per-τ_d report showing
  reader and character states, live ironies, and anagnorisis deltas on
  a set of central propositions.
- `demo_rashomon.py` — the Rashomon driver. Prints branch-indexed
  matrices: per-branch world state, per-branch reader state, per-branch
  dramatic-irony counts, and sibling-non-inheritance side-by-side.
- `test_substrate.py` — permanent substrate tests pinning sketch-04
  invariants and current implementation behavior. Story-agnostic
  (though two oedipus integration tests live at the end).
- `test_inference.py` — permanent inference-engine tests per
  inference-model-sketch-01 N1–N10: rule shape and range-restriction;
  query-time derivation; identity-substitution composition; per-fold
  scoping; weakest-premise slot propagation and GAP-fails; bounded
  fixpoint with depth cap; proof-carrying derivation; authored-wins.
  Integration tests against the Oedipus and Macbeth retirements
  (authored compounds gone; derivations fire at the expected folds
  and moments).
- `test_dramatic.py` — Dramatic dialect tests per dramatic-sketch-01
  M1-M10. Synthetic-fixture tests pin each M8 check independently
  (id resolution, beat / scene sequencing, template conformance with
  multiplicity, soft argument completeness, stakes coverage, scene
  purpose, orphans). Integration tests against `oedipus_dramatic.py`
  pin the verifier's three-observation contract on that encoding.
- `test_rashomon.py` — permanent contested-branch tests pinning
  invariants that only become load-bearing with a non-trivial
  `:contested` example: sibling non-inheritance on a live encoding,
  canonical-is-universal propagation, per-branch reader projections,
  sjuzhet rejection for out-of-scope entries, branch-aware query
  differentiation. Also pins the reader-model probe surface:
  `reader_view` shape and scope, `ingest_review` / `ingest_proposal` /
  `ingest_question_answer` ingest invariants, `accept_answer_proposal`
  and `decline_proposal` transition rules.
- `reader_model_client.py` — live-LLM tooling for reader-model-sketch-01.
  Wraps Claude Opus 4.6 via the Anthropic SDK; produces substrate-native
  `ReviewEntry` and `AnswerProposal` records from a `ReaderView`.
- `demo_reader_model.py` — first LLM-in-the-loop demo. Builds a
  `:b-woodcutter` view, calls the reader-model, prints reviews and
  answer proposals. With `--walk`, hands them to the interactive walker.
- `proposal_walker.py` — terminal walker that turns LLM output into
  authorial acts: accept / decline / skip / quit over each review and
  each answer proposal, invoking `ingest_review` and
  `accept_answer_proposal` / `decline_proposal` on the author's
  decision. Stream-based (takes `stdin` / `stdout`) so tests can drive
  it without a terminal.
- `test_proposal_walker.py` — walker tests. `io.StringIO`-driven; pins
  accept/decline/skip/quit flow, EOF handling, and the "only-pending"
  invariant for repeated walks over the queue.
- `test_reader_model_client.py` — structural tests for the reader-model
  client: R5 scope enforcement on reviews and answers, the question-only
  rule, and translation into substrate-native records.

Both test files: no framework, no dependencies, plain assertions with a
minimal runner. Each test's docstring flags when it pins a convention
rather than a sketch commitment.

## What the Oedipus demo demonstrates

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

## What the Rashomon demo demonstrates

Where Oedipus exercises irony on a single canonical timeline, the
Rashomon demo exercises the `:contested` branch machinery: four
sibling branches, each internally consistent, mutually incompatible,
with the substrate computing per-branch answers for the same
propositions.

The demo prints four matrices:

- **Per-branch world state** on a dozen contested propositions
  (different killer per branch, different weapon, different modality
  of intercourse, and so on). Each row shows which branches assert
  the proposition and which do not.
- **Per-branch reader state** at τ_d=100 (after all testimonies). On
  each branch the reader holds that branch's disclosed facts as KNOWN;
  the facts of sibling branches are simply absent. What the substrate
  does *not* yet represent is the reader's meta-knowledge that they
  have heard four conflicting accounts — see `rashomon.py`'s *Known
  soft spots* #2.
- **Per-branch dramatic-irony counts.** A regression that collapsed
  branch-awareness back to canonical-only would make all four branches
  return identical counts. The woodcutter's branch has the largest
  total because it discloses one extra self-incriminating fact (the
  dagger theft) the other testimonies do not.
- **Who killed the husband?** — the same question resolved four
  different ways across the branches. Two branches agree Tajomaru did
  it; one says the wife; one says the husband himself. The substrate
  returns the multiplicity without arbitration, which is what sketch
  04 means by "represented ambiguity."

A final panel makes the fold-scope rule tangible: `stole(woodcutter,
dagger)` appears on `:b-woodcutter` and nowhere else (sibling non-
inheritance); `had_intercourse_with(Tajomaru, wife)` is on
`:canonical` and therefore appears on every branch (canonical-is-
universal).

## The payoff, Rashomon-flavored

Three features the Rashomon encoding makes visible:

1. **Represented ambiguity, not reader-side misunderstanding.** The
   substrate does not stage Rashomon as "the reader is confused."
   The fabula itself carries a contest; each branch is a complete,
   internally consistent reality; the substrate returns all four.
   This is sketch 04's commitment T1 in action.

2. **Sibling non-inheritance as a test.** The fold-scope rule reads
   as a line of prose in the sketch; in the prototype it is the
   reason `stole(woodcutter, dagger)` stays on one branch. A test
   (`test_stole_dagger_only_visible_on_woodcutter_branch`) pins this
   property against regression.

3. **Per-branch sjuzhets share a canonical spine.** The preamble
   disclosures — the entities travel, Tajomaru binds the husband,
   intercourse occurs — appear identically in every branch's
   sjuzhet because those events are labeled `:canonical`. The
   testimony-specific disclosures diverge. This is the narrator's
   "what everyone agrees on" framing, made mechanical.

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
- **B1.** Branch labels, kinds, fold-scope rule. Exercised end-to-end by
  the Rashomon encoding (four sibling `:contested` branches plus
  `:canonical`) as well as the Oedipus slice (canonical-only). The
  Rashomon demo makes per-branch divergence visible side-by-side.
- **Dramatic irony query.** Both Reader > Character and Character >
  Character ironies (with reader aware).
- **Sternberg curiosity gaps.** Reports propositions in the reader's GAP
  slot. None in the current slice because the reader is effectively
  omniscient.

## What's deferred

Pulled in later, as the prototype earns iterations:

- **F1** — emotional and tension projections.
- **Partial order** — structure is in place; no partial-order solver yet.
- **Draft / counterfactual branches** — supported by the fold-scope
  rule; no encoded story uses one. See open questions 13 and 14 in
  sketch 04.
- **Credibility weighting of contested branches** — Rashomon's four
  testimonies are represented as peer branches. The substrate has no
  notion of "branch X is more reliable than branch Y"; the woodcutter's
  account is not privileged. See `rashomon.py`'s *Known soft spots* #1.
- **Testimony-as-utterance** — Rashomon's reader disclosures land on
  each branch as KNOWN, which represents "within this branch's reality,
  the reader knows X" but not "the reader has heard four conflicting
  accounts and is uncertain." The latter meta-uncertainty needs a layer
  the substrate does not have yet. See `rashomon.py`'s *Known soft
  spots* #2.
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
