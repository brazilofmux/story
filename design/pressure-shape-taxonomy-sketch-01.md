# Pressure-shape taxonomy — sketch 01

**Status:** draft, active
**Date:** 2026-04-16
**Supersedes:** nothing (new topic; parallel to event-kind-taxonomy-sketch-01)
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [architecture-sketch-02.md](architecture-sketch-02.md), [substrate-sketch-05.md](substrate-sketch-05.md), [verification-sketch-01.md](verification-sketch-01.md)
**Related:** [event-kind-taxonomy-sketch-01.md](event-kind-taxonomy-sketch-01.md), [inference-model-sketch-01.md](inference-model-sketch-01.md), [identity-and-realization-sketch-01.md](identity-and-realization-sketch-01.md), `oedipus_dramatica_complete_verification.py`, `macbeth_dramatica_complete_verification.py`, `ackroyd_dramatica_complete_verification.py`
**Superseded by:** nothing yet

## Purpose

Close the remaining Characterization gap at the dramatica-complete →
substrate verifier boundary: **DSP_limit** (Optionlock vs Timelock).
Currently declared on every dramatica-complete encoding (six total;
five Optionlock, one Timelock) but unchecked by any verifier. Listed
in the README verifier-surface-extension finding as "needs a
pressure-shape classifier, same design problem EK2 solved for
Activity — deferred to its own sketch pass."

This is that sketch pass.

EK2 solved the Activity / Do-er boundary by reading fold-visible
structure (participants, effects) instead of type strings. DSP_limit
sits at an analogous slot in the Characterization primitive: it asks
what **kind of pressure** drives the arc to its climax — alternatives
running out, or a clock reaching zero. The answer is a structural
property of the fabula, not a string tag on the Story record.

## What this sketch is *not* committing to

- A new attribute on the event record. No `scheduled_τ_s` field, no
  `is_deadline_event` tag. A3 rejects speculative schema.
- A new substrate-05 vocabulary for scheduling. Substrate-05 stays
  as-is; if Timelock pressure eventually demands substrate support
  for scheduling, that is a substrate-05/06 question, not a verifier
  question.
- A universal pressure taxonomy across dialects. This sketch
  specifies Optionlock and Timelock (the dramatica-complete pair).
  Other dialects may ask different pressure-shape questions
  (Save-the-Cat's "All Is Lost" beat pressure, genre templates'
  convention pressures) — those get their own classifiers per EK5.
- Changing the `characterization` primitive itself. V3 /
  `verify_characterization` / `run_characterization_checks` are
  unchanged. Only a new *check function* and a new *classifier* are
  added.
- A claim that the Timelock predicate is as strong as the Optionlock
  predicate. It is not. See LT3 and the Open Questions.

## The tension in one frame

DSP_limit's two choices are semantically distinct:

- **Optionlock** — the arc ends because *alternatives run out*. The
  pressure is convergent: suspects eliminated, options foreclosed,
  candidate identities collapsed, knowledge accreted until a
  load-bearing claim becomes derivable. The story *could* run longer
  by authorial fiat but would not be Optionlock if it did, because
  the climax is no longer forced by elimination.

- **Timelock** — the arc ends because *a clock reaches zero*. The
  pressure is scheduled: a fight on a marked calendar, a deadline
  announced in advance, a ticking bomb. The climactic event's τ_s is
  fixed early in the arc regardless of whether anything has
  converged. The story *could not* run longer without breaking its
  own frame.

Both are author-level characterizations of the arc's shape. The
verifier's question: does the substrate *exhibit* the pressure shape
the DSP declares?

Substrate-05's discipline (per EK2) is to read fold-visible
participants and effects, not type strings. The pressure question
has the same shape as EK2 at a different granularity — EK2
classifies individual events; LT classifies the arc as a whole.

## Candidates considered

### Candidate A — Per-story enumeration of "Optionlock events" and "Timelock events"

Tag individual events as contributing to one pressure shape or the
other; the verifier counts the tags.

- **For.** Simple. Author declares intent.
- **Against.** **A3 fail** — the tag exists for the verifier's
  convenience; an attentive reader can classify the arc's pressure
  from the prose. Worse, it shifts classification work to the
  author, inverting the verifier's value proposition (the verifier
  is supposed to check the declared DSP against substrate, not have
  the author re-state the declaration at event granularity).
- **Verdict.** Rejected.

### Candidate B — Structural predicate over fold-visible fabula shape (Optionlock side)

Classify the arc's pressure by structural features the substrate
already carries: retractions (`asserts=False` effects), identity-
proposition effects (equivalence-class collapses), rule-derivable
compound facts emerging mid-arc. Convergence-shape is the disjunction
of the three.

- **For.** Honors substrate-05's "examine effects" discipline.
  Generalizes across encodings automatically — the same classifier
  works on Macbeth (retraction-dominant), Ackroyd (retraction +
  suspect elimination), and Oedipus (identity-resolution +
  rule-derivation) without per-story tuning. The three signals
  correspond to three different mechanisms Dramatica authors use to
  make "alternatives run out" visible.
- **Against.** More verifier complexity. The three-signal disjunction
  may over-trigger on stories that are genuinely Timelock but happen
  to contain a retraction in a subplot.
- **Verdict.** Primary fix for Optionlock. See LT2.

### Candidate C — Structural predicate for Timelock

Detect Timelock symmetrically: a structural signal for scheduling.
The natural candidates:
1. **Terminal-event τ_s referenced by an earlier event's effect
   payload** — e.g., an early event whose `WorldEffect` asserts
   `scheduled_at(fight, τ_s=15)` and a terminal event at τ_s=15.
2. **Description-carried schedule hints** — a description whose kind
   indicates scheduling ("the fight is on the calendar"; "the
   countdown begins").
3. **Complement of LT2** — no convergence-shape features visible.

- **For (1).** Structural, fold-visible.
- **Against (1).** Substrate-05 has no scheduling vocabulary; this
  would require a new effect kind or a conventional predicate name.
  Not ready to commit without a real Timelock substrate to pressure
  it (Rocky's is unwritten).
- **For (2).** Honors A3 — schedules live in prose naturally. The
  verifier reads description kind/anchor, not event type.
- **Against (2).** Requires a canonical "schedule" description kind
  the project has not defined. May turn into probe-driven
  classification (Candidate D territory).
- **For (3).** Cheapest.
- **Against (3).** Unreliable — Timelock stories sometimes contain
  retractions and identity-resolutions (Rocky's stunt-goal gets
  retracted when the fight becomes real; Adrian's identity-
  characterization shifts as Rocky draws her out). Complement-only
  classification risks Timelock stories being misclassified as
  Optionlock just because they contain any convergence signal.
- **Verdict.** (1) deferred pending Rocky substrate. (2) deferred
  pending a schedule-description convention. (3) taken as the
  weak-signal fallback per LT3. **Honest statement: the Timelock
  predicate is weaker than the Optionlock predicate by design; the
  sketch commits to this asymmetry rather than papering over it.**

### Candidate D — Description-driven classification via reader-model probe

Attach probe-derived descriptions that characterize each arc's
pressure shape. The verifier reads the descriptions.

- **For.** A3-compliant. Composes with architecture-02 A11.
- **Against.** Loses the verifier's mechanical determinism. The
  convergence-shape question is structural ("does the fabula contain
  a retraction?"), not interpretive ("is this *really* Optionlock?"),
  for Optionlock side. Probe is appropriate where the question is
  genuinely interpretive.
- **Verdict.** Rejected for Optionlock. May be reconsidered for
  Timelock if structural signal stays weak through future encodings.

### Candidate E — Accept DSP_limit as an unverifiable declaration

Do not check DSP_limit at all. The author says Optionlock or
Timelock; the verifier trusts.

- **For.** Zero cost. Matches the Dramatica-theory stance that
  Limit is an authorial choice.
- **Against.** Leaves the verifier surface with a hole exactly at
  the place substrate-lowering honesty can be measured. Five
  Optionlock encodings have substrate convergence signals visible
  *right now*; not reporting on them is leaving signal on the
  floor.
- **Verdict.** Rejected. The asymmetric position (strong Optionlock
  check, weak Timelock check) is strictly more informative than no
  check.

## Commitments

### LT1 — Verifier classification reads fold-visible structure, not type strings

The pressure-shape predicate is a function of the fabula's events,
effects, and rule-derivable world/knowledge state — the same
fold-visible surface EK1 commits to at the event level. Type strings
may inform priors (e.g., event types `realization` and `anagnorisis`
bias toward identity-resolution signal) but may not be the sole
classifier input. EK1's discipline extends to LT1 unchanged.

### LT2 — Optionlock-shape predicate

An arc is **Optionlock-shaped** if at least one of the following
convergence signals appears in its canonical-scope fabula:

- **Retraction.** There exists an event with an effect asserting a
  world proposition `P` with `asserts=False`, where `P` was
  previously world-asserted (`asserts=True`) in the fabula, OR
- **Identity resolution.** There exists an event whose effects
  include an identity proposition that causes at least two
  previously-distinct entities to join an equivalence class under
  identity-and-realization-sketch-01's substitution rule, OR
- **Rule-derivable emergence.** There exists a rule-derivable
  compound world proposition (per inference-model-sketch-01) that
  is **not** derivable at the arc's start but **is** derivable at
  the arc's end.

The three are disjunctive. Any one signal is sufficient evidence of
convergence shape; the count is reported as strength (higher count
≈ stronger convergence).

These three signals correspond to the three mechanisms by which
Dramatica authors make "alternatives run out" concrete: explicit
retraction of prior claims, collapse of candidate identities, and
gradual buildup to a load-bearing derivation.

### LT3 — Timelock-shape predicate (weak, complement-based)

An arc is **Timelock-shape-consistent** if it is *not*
Optionlock-shaped under LT2: zero retractions, zero identity
resolutions, zero mid-arc rule emergences. This is complement-only
signal and is explicitly weak: it confirms the absence of
convergence but does not affirmatively detect scheduling.

**Timelock-shape-strongly-detected** remains unavailable in this
sketch. Detection requires one of:

- a scheduling vocabulary in substrate-05 (future sketch —
  `scheduled_at` or equivalent effect payload), or
- a canonical schedule-description kind (future descriptions sketch),
  or
- sequence-aware analysis of terminal-event anticipation in early
  events' knowledge-effects (future refinement).

Until then, a Timelock-declared story whose substrate exhibits no
convergence signals is reported as `NOTED` with a message stating
that the absence of Optionlock structural features is consistent
with the Timelock declaration but is not affirmative evidence. A
Timelock-declared story whose substrate *does* exhibit convergence
signals is reported as `PARTIAL_MATCH` or `NEEDS_WORK` with a
message flagging the declaration/substrate tension.

This asymmetry is the sketch's honest position. Sharpening LT3 is
on the sketch's Open Questions; it does not block landing LT2.

### LT4 — The classifier lives in `verifier_helpers.py`

Per EK3 and the cross-boundary verifier-helper extraction pattern
(commit `bf5bfa0`), a new function `classify_arc_limit_shape` (or
similar) ships in `verifier_helpers.py`. It takes a fabula, rules,
and canonical-scope indicator and returns a classification record:
`("optionlock", strength, signals)` or `("timelock-consistent",
strength, signals)` or `("undetermined", 0.0, ())`. Each of the
three verifier modules imports and calls it.

### LT5 — Author declaration is fallback, not override

The DSP_limit declaration is the Story author's claim about the
arc's pressure shape. The verifier reports whether the substrate
*agrees*:

- Optionlock declared + Optionlock-shaped substrate → `APPROVED`.
- Timelock declared + no convergence signals in substrate →
  `NOTED` (consistent-but-not-affirmed).
- Optionlock declared + no convergence signals → `NEEDS_WORK`
  (substrate does not render the declared shape).
- Timelock declared + convergence signals present → `PARTIAL_MATCH`
  or `NEEDS_WORK` (substrate convergence shape contradicts the
  Timelock declaration).

LT5 is the coupling discipline: the author's declaration is never
silently overridden by substrate signal; the verifier reports the
disagreement and leaves resolution to the author (edit the DSP, edit
the substrate, or accept the mismatch as a known partial).

### LT6 — The pressure-shape frame is verifier-local

Like EK5, the Optionlock / Timelock frame is a property of the
dramatica-complete → substrate verifier, not a substrate
commitment. Save-the-Cat's corresponding pressure question (its
"catalyst → debate → break into 2 → all is lost" pressure shape)
is a different structural question and gets its own classifier.
Other dialects are likewise independent.

## Worked case — Oedipus under LT2 (identity-resolution dominant)

`oedipus.py` at the current commit. Canonical-scope events reviewed
for LT2 convergence signals:

- **Retractions.** Zero. No `asserts=False` effects in Oedipus's
  fabula.
- **Identity resolutions.** The load-bearing one: Oedipus's
  `project_knowledge` equivalence class gains `the-exposed-baby`
  after E_shepherd_testimony + E_oedipus_anagnorisis. At τ_s=0,
  `oedipus` and `the-exposed-baby` are distinct; at τ_s=13+, they
  are in the same equivalence class. This is per identity-and-
  realization-sketch-01 I3/I6 (realization as identity-assertion
  trigger). Count: at least 1 (the oedipus-baby collapse, possibly
  also oedipus-laius-killer depending on the encoding's identity
  effects).
- **Rule-derivable emergences.** `parricide(oedipus, laius)` does
  not derive at τ_s=0 (premises missing); derives at τ_s=end (both
  `killed` and `child_of` world-asserted). Same for `incest`. Count:
  2.

Total LT2 signals: 3 (0 retractions + 1 identity resolution + 2
rule emergences). **Classification: Optionlock-shaped.**

DSP_limit declaration: Optionlock. **Expected verdict: APPROVED.**
Strength signal: strong (three convergence signals).

This result vindicates the identity-resolution clause of LT2 —
Oedipus's convergence is not a retraction story; it is a
discovery-of-what-already-was story, and the substrate encodes that
shape as equivalence-class collapse plus rule-chain premise
accretion.

## Worked case — Macbeth under LT2 (retraction-assisted)

`macbeth.py` at the current commit.

- **Retractions.** One: `king("macbeth", "scotland")` retracted via
  `asserts=False` at the death scene (per macbeth_lowerings.py
  narration, this unwinds the `tyrant` derivation).
- **Identity resolutions.** No new equivalence classes form across
  the arc; Macbeth's identity (kinslayer, regicide, tyrant) is
  rule-derived from authored premises, not identity-collapsed.
- **Rule-derivable emergences.** `kinslayer`, `regicide`,
  `breach_of_hospitality`, `tyrant` — four rule-derivable compounds
  that emerge over the arc (per inference-model-sketch-01's
  retirement of the authored predicates). Count: 4.

Total LT2 signals: 5 (1 + 0 + 4). **Classification:
Optionlock-shaped.**

DSP_limit declaration: Optionlock. **Expected verdict: APPROVED.**
Strength signal: strong.

Macbeth's "protections collapse one by one" shape is the
rule-emergence signal: each killing premise turns an increasingly
severe compound derivable. The retraction at death closes the arc
symmetrically.

## Worked case — Ackroyd under LT2 (retraction-dominant)

`ackroyd.py` at the current commit.

- **Retractions.** One (post-F5 fix):
  `accused_of_murder(ralph_paton, ackroyd)` retracted via
  `asserts=False` at Poirot's reveal. This is the substrate trace of
  "Ralph cleared"; prior to the same-day fix, the retraction was
  implicit in social inference rather than encoded, and
  Story_consequence sat at PARTIAL 0.5.
- **Identity resolutions.** None at the substrate-identity level
  (the killer's identity resolves as world-fact, not as entity-
  identity collapse — Sheppard and `the-killer` are not modeled as
  candidate-identical entities; `killer(sheppard)` is a world
  predicate).
- **Rule-derivable emergences.** Depends on the encoding's rule
  set. At minimum, the killer identification chain (witness
  testimony → Sheppard's absence/motive → Poirot's derivation) is
  visible through `world_holds_derived` at end.

Total LT2 signals: at least 2 (1 retraction + at least 1 emergence).
**Classification: Optionlock-shaped.**

DSP_limit declaration: Optionlock. **Expected verdict: APPROVED.**
Strength signal: moderate to strong.

Ackroyd's "Poirot eliminates suspects one by one" shape is the
retraction signal: the explicit `asserts=False` on Ralph's
accusation at the reveal is the suspect-list pruning operation
Dramatica-theory Optionlock predicts, made fold-visible after F5.

## Worked case — Rocky under LT3 (measured, Phase 2 landing)

Rocky's substrate (`rocky.py`), lowerings (`rocky_lowerings.py`),
and cross-boundary verifier
(`rocky_dramatica_complete_verification.py`) all landed in the
three-phase Rocky encoding following this sketch. Rocky's DSP_limit
declaration is Timelock (first in the corpus). The sketch's original
prediction was that Rocky's substrate would be timelock-consistent
(zero convergence signals) under LT3. **Measured: that prediction
was partially wrong.**

Measured LT2 classifier output on `rocky.py`:

- retraction: **1** (not 0 — `scheduled_fight(apollo, mac)` retracts
  at E_mac_injured when Mac breaks his hand; this forces the arc
  into existence).
- identity-resolution: **0** (prediction confirmed — Rocky is
  Steadfast; no entity-identity collapses).
- rule-emergence: **1** (not 0 — `went_the_distance(rocky, apollo)`
  derives at E_fight_ends from `fought_rounds=15` +
  `standing_at_final_bell`, via the single `WENT_THE_DISTANCE_RULE`).

LT2 classification: `("optionlock", 0.67, ("retraction:1",
"rule-emergence:1"))`.

Under LT5's disposition table, DSP_limit=Timelock declared +
substrate-shows-convergence → **NEEDS_WORK 0.33**. This is the first
non-APPROVED DSP_limit verdict in the corpus and the direct
validation that LT5's asymmetric disposition works as designed.

**Why the prediction was partially wrong.** The two signals Rocky
does exhibit are structurally different from arc-converging
signals:

- The retraction is a **pre-plot premise retraction**, not a
  convergence of the main arc. Mac's fight gets retracted so that
  Rocky's fight can exist. The main arc (τ_s=0-57) never retracts
  any world fact; the retraction at τ_s=-5 is the *precondition* of
  the arc, not its payoff. LT2 cannot tell these apart from the
  classifier's perspective — both are `asserts=False` effects
  unwinding prior assertions.
- The rule emergence lands **at the scheduled τ_s** (τ_s=55,
  E_fight_ends), not before. `went_the_distance` derives because
  the two premises happen simultaneously at the fight's end.
  Convergence *coincides* with schedule rather than *replacing*
  schedule as the arc's forcing mechanism. A Dramatica Timelock
  arc can still produce a compound at the scheduled moment — the
  rule's firing is not evidence against Timelock; it is a property
  of how Rocky's achievement is encoded.

This is LT3's OQ3 ("subplot-only convergence") case made concrete,
though the name is slightly misleading: the signals are in the
main arc, not a subplot. A better framing for OQ3 after Rocky:
**arc-peripheral vs. arc-converging convergence signals**. Both
exist, both fire LT2, and LT2 cannot distinguish them today.

**Implication for LT3-strong.** The Rocky finding sharpens the
case for LT3-strong detection rather than weakening the broader
framework. Two refinement paths, both deferred to a future sketch:

1. **Arc-position weighting.** Weight signals by proximity to the
   terminal event. A retraction at τ_s=-5 (far from the τ_s=57
   terminal) contributes less than a retraction at τ_s=55. The
   ratio of arc-position-weighted signals to total signals would
   distinguish arc-converging from arc-peripheral shapes.
2. **Scheduling vocabulary.** Add a `schedule(event_id, at_τ_s)`
   world effect or a canonical `schedule` description kind. The
   classifier then asks: does a terminal event's τ_s match an
   earlier scheduling reference? If yes, the arc is
   Timelock-shape-strong even in the presence of other signals.

Path 2 is more principled (schedules are a genuine substrate
concern, not an inference over sparse signals). The Rocky
encoding's descriptions already flag this explicitly
(`D_timelock_not_natively_detectable`) — the substrate encoding
anticipates the future sketch.

**DSP_limit's role in the verifier surface remains correct.** A
NEEDS_WORK verdict on Rocky is strictly more informative than no
check. The disagreement is reported honestly; the author can
choose to edit the DSP declaration, the substrate, or accept the
mismatch as a known partial. LT5's neutrality preserves authorial
authority, per the commitment.

## Worked case — Rocky's full 9-check verifier surface (Phase 2 measurements)

Beyond the DSP_limit finding above, Rocky's full verifier run
(`rocky_dramatica_complete_verification.run()`) produces 8 APPROVED
+ 1 NEEDS_WORK, with three verifier patterns new to the
dramatica-complete → substrate boundary:

- **First Outcome=Failure check in the corpus.** DSP_outcome=Failure
  declared on Rocky; the check asks "does the substrate show the
  goal NOT landing?" The load-bearing fact for "clean publicity-
  stunt win" is the **opposite** of the goal's own predicate —
  `went_the_distance(rocky, apollo)` deriving IS the evidence that
  supports the Failure declaration. APPROVED 1.00. Pattern:
  **goal-opposite-is-evidence** inversion.

- **First Judgment=Good check for the MC in the corpus.** All prior
  encodings had Judgment=Bad (epistemic ruin, moral degradation,
  betrayer self-erasure). Rocky's Good is the positive-closure
  cluster at τ_s=end: `went_the_distance` (achievement),
  `called_out(rocky, adrian)` (relationship payoff),
  `refused_rematch(rocky)` (acceptance). All three hold → APPROVED
  1.00.

- **Steadfast via structural invariance** (new predicate shape).
  Ackroyd's Steadfast check uses a pre-existing rule-derived trait
  (`betrayer_of_trust` holds from the arc's start). Rocky has no
  comparable pre-existing trait — his Steadfast rests on
  *absence* of transition. The substrate predicate: Rocky's
  equivalence-class structure at τ_s=0 matches τ_s=end (both
  empty). Same DSP value (Steadfast) + different verifier
  evidence pattern. APPROVED 1.00.

The remaining checks (DA_mc APPROVED 0.72, DSP_approach APPROVED
0.74, DSP_growth APPROVED 1.00, Story_goal APPROVED 1.00,
Story_consequence APPROVED 1.00) match the sketch's expected
measurements. DSP_growth's "privately-chosen start" at τ_s=45 is
semantically distinct from Ackroyd's "ultimatum-compelled start"
but uses the same verifier predicate (acquisition of a specific
proposition mid-arc).

## Worked case — P&P and Chinatown (prediction, pending substrate)

Both also declared Optionlock at the Template layer. `pride_and_prejudice.py`
and `chinatown.py` **do not exist** — substrate not authored. LT2
predicts Optionlock signals in both:

- **P&P**: prejudice retractions (Elizabeth's reassessment of
  Darcy after the Pemberley letter; Darcy's reassessment of
  Elizabeth), plus rule-derivable emergences around marriage-
  eligibility chains.
- **Chinatown**: identity resolution (Evelyn's daughter / sister
  revelation), plus a retraction around the orchard murder's
  perpetrator.

These predictions are banked; they do not run until substrate is
written. Consistent with item 2 in the README's upcoming-sketches
list — P&P/Rocky/Chinatown remain gated by substrate authoring.

## Relation to the eight-check verifier surface

Post-LT2 landing, each dramatica-complete → substrate verifier
ships **nine checks** (up from eight). The new DSP_limit check slots
alongside DA_mc and DSP_approach in the Characterization-primitive
group:

- Characterization (3): DA_mc, DSP_approach, **DSP_limit** (new).
- Claim-moment (2): DSP_outcome, Story_consequence.
- Claim-trajectory (4): DSP_judgment, DSP_resolve, DSP_growth,
  Story_goal.

Measured post-LT2 spectrum at the DSP_limit check (four encodings;
updated after Rocky Phase 2):

| Encoding | DSP_limit declared | Signals fired | DSP_limit verdict |
|---|---|---|---|
| Oedipus | Optionlock | identity-resolution:7 + rule-emergence:9 | APPROVED 0.67 |
| Macbeth | Optionlock | retraction:1 + rule-emergence:3 | APPROVED 0.67 |
| Ackroyd | Optionlock | retraction:1 + rule-emergence:2 | APPROVED 0.67 |
| **Rocky** | **Timelock** | retraction:1 + rule-emergence:1 | **NEEDS_WORK 0.33** |

The three Optionlock encodings all land APPROVED 0.67 (two of
three signal kinds firing) — uniformity is a property of the
corpus, not a weakness of the predicate. The Rocky case is the
verifier surface's first DSP_limit disagreement and the honest
signal LT5 was written to produce.

## Implementation brief

Concrete change, in order of landing:

1. **Add `classify_arc_limit_shape` to `verifier_helpers.py`.**
   Signature roughly:
   ```python
   def classify_arc_limit_shape(
       fabula: Iterable[Event],
       rules: Iterable[Rule],
       canonical: Branch,
       all_branches: Sequence[Branch],
       *,
       identity_collapse_sample: Optional[Callable[...]] = None,
   ) -> tuple[str, float, tuple[str, ...]]:
   ```
   Returns `("optionlock", strength, signal_tags)` or
   `("timelock-consistent", strength, signal_tags)` or
   `("undetermined", 0.0, ())`. The three LT2 signals are computed
   independently; `signal_tags` records which fired. Strength is a
   normalized count (e.g., `min(1.0, signal_count / 3.0)`).
2. **Add a unit test suite in `test_verification.py`.** Classifier
   unit tests against small fixture fabulae: one retraction-only,
   one identity-resolution-only, one rule-emergence-only, one with
   all three, one with none. Six or seven fixtures total.
3. **Add `limit_optionlock_characterization_check` to
   `oedipus_dramatica_complete_verification.py`.** Calls
   `classify_arc_limit_shape` on Oedipus's fabula, compares to
   `DSP_limit.choice`, returns `(verdict, strength, comment)` per
   LT5's disposition table.
4. **Parallel rewrite for
   `macbeth_dramatica_complete_verification.py`** and
   **`ackroyd_dramatica_complete_verification.py`**. The check
   function is encoding-agnostic; each module plugs its own fabula
   and `DSP_limit` into the shared check helper.
5. **Update `run()` in each verifier** to include the new check
   (now returning nine `VerificationReview` records).
6. **Integration tests** in `test_verification.py` pin the expected
   verdict bands for Oedipus / Macbeth / Ackroyd at APPROVED.
7. **Update README.md's upcoming-sketches item 2 finding** to
   record the LT2 spectrum (all three APPROVED; Rocky pending
   substrate for Timelock-side testing) and retire the "DSP_limit
   — deferred to its own sketch pass" bullet.

No substrate changes. No new event types. No schema changes in any
dialect. Strictly parallel to EK2's implementation shape.

## Discipline

- **Future pressure-shape checks use the same pattern.** If a
  Save-the-Cat or other-dialect verifier needs a pressure classifier
  (e.g., the "all is lost" / "break into 2" pressure curve), the
  classifier lives in `verifier_helpers.py` and reads fold-visible
  structure. LT1 is the rule; each dialect gets its own classifier.
- **The Optionlock / Timelock asymmetry is owned, not hidden.** The
  sketch commits to reporting Timelock-declared stories as `NOTED`
  (consistent but not affirmed) rather than `APPROVED`. This is the
  honest position given substrate-05's scheduling gap. Any future
  sketch strengthening LT3 must preserve LT5 (declaration never
  silently overridden).
- **Substrate convergence signals are load-bearing.** Identity
  resolutions and rule-derivable emergences are the two mechanisms
  by which inference-model-sketch-01 and identity-and-realization-
  sketch-01 make substrate pressure visible. LT2 is the first
  verifier check to read them at the arc level rather than at the
  fact level. A future Claim-trajectory check that asks a similar
  question ("does this arc converge on X?") should compose with LT2
  rather than reinvent the signal-detection.
- **Composition with EK2.** EK2 classifies individual events; LT2
  classifies the arc. An event that is internal-state-shaped under
  EK2 may still contribute an LT2 signal (a soliloquy-style
  realization that collapses an equivalence class is EK2-internal
  but LT2-identity-resolution). The two classifiers answer different
  questions and do not conflict.

## Open questions

1. **Timelock strong-predicate via substrate extension.** A
   substrate-sketch-06 could add `schedule(event_id, at_τ_s)` as a
   first-class world effect. Or it could add a descriptive kind
   (`schedule`) in descriptions-sketch-02. Either unlocks LT3-strong.
   Which path is more principled is an open design question; the
   A3 test suggests descriptions first (schedules are prose content
   an attentive reader catches) and substrate extension only if the
   verifier needs mechanical access. Deferred until Rocky substrate
   pressures it.

2. **Identity-resolution counting.** LT2's identity-resolution clause
   counts distinct equivalence-class collapses across the arc. But
   a single realization event (e.g., Oedipus's anagnorisis) may
   cause multiple collapses simultaneously (oedipus ↔ the-exposed-
   baby; oedipus ↔ laius-killer-subject-of-oracle). Is the count
   "events with identity effects" or "equivalence-class join
   operations"? The difference matters only for strength scoring,
   not for Optionlock/Timelock classification. The current
   implementation proposal uses the event count for simplicity;
   the alternative is banked.

3. **Subplot-only convergence signals.** A Timelock main arc may
   contain a subplot with a retraction or identity resolution (e.g.,
   a minor character's identity reveal inside an otherwise
   schedule-driven arc). LT2 currently counts all convergence
   signals in the canonical fabula; this risks a Timelock story
   being flagged Optionlock-shaped on subplot signals alone. If this
   bites when Rocky lands, the refinement is to weight signals by
   their participation in the MC throughline's Lowered event set.
   Deferred pending concrete case.

4. **Retraction shape heterogeneity.** Not all retractions carry the
   same semantic weight. Macbeth's `king → asserts=False` retraction
   at death is a mechanical unwinding of a world-fact by an event
   that happens to end the story. Ackroyd's accused-of-murder
   retraction at the reveal is the load-bearing beat. LT2 counts
   both as one signal each. Strength weighting by retraction
   position (early, mid, terminal) is deferred.

5. **Dialect-agnostic classifier library.** LT4 places the
   classifier in `verifier_helpers.py` for the dramatica-complete
   boundary. When Save-the-Cat grows its own pressure-shape check,
   do the two classifiers share structure? Likely yes — both read
   the same fold-visible substrate — but the upper-dialect semantic
   framing differs. A shared helper module may eventually factor
   out the signal-detection primitives from the dialect-specific
   classification logic. Premature to extract now.

## Summary

- DSP_limit is the last DSP-axis Characterization gap at the
  dramatica-complete → substrate boundary. The verifier ships
  nine checks per encoding (was eight); DSP_limit is the ninth.
- The Optionlock side of the predicate is strong: three disjunctive
  fold-visible signals (retraction, identity resolution, rule
  emergence) cover all three Optionlock-declared encodings and
  produce a uniform APPROVED 0.67.
- The Timelock side is weak by design — substrate-05 does not
  encode schedules. The sketch commits to this asymmetry (LT3
  reports `NOTED` for Timelock-consistent-but-unaffirmed, or
  `NEEDS_WORK`/`PARTIAL_MATCH` when the substrate shows
  convergence) rather than faking a strong predicate.
- No substrate changes; no new dialect commitments; the classifier
  is a `verifier_helpers.py` addition parallel to EK2's
  `classify_event_action_shape`.
- Rocky's substrate (Phase 2 landing) produced **NEEDS_WORK 0.33**
  on DSP_limit — the first non-APPROVED DSP_limit in the corpus.
  LT5's asymmetric disposition is validated concretely. The
  finding sharpens the case for LT3-strong (scheduling vocabulary)
  and refines LT3's OQ3 from "subplot-only convergence" to
  "arc-peripheral vs. arc-converging signals".

## Implementation landed

This sketch has been implemented in two phases.

**Phase 1 (2026-04-16, commit `24e1408`):** LT2 / LT3 / LT4 / LT5 /
LT6 commitments landed for the three existing substrates.

- `classify_arc_limit_shape` and `dsp_limit_characterization_check`
  shipped in `verifier_helpers.py`. Three-signal disjunction
  (retraction + identity-resolution + rule-emergence) with the
  strip-and-rederive refinement that detects rule firings even when
  the compound is also authored (N10's "authored wins" would
  otherwise hide Ackroyd's `betrayer_of_trust` / `driver_of_suicide`
  emergences).
- DSP_limit check added to
  `oedipus_dramatica_complete_verification.py`,
  `macbeth_dramatica_complete_verification.py`,
  `ackroyd_dramatica_complete_verification.py`. Each verifier now
  runs 9 checks (was 8).
- 18 new tests in `test_verification.py` (classifier unit tests
  with synthetic fixtures, LT5 disposition tests, per-encoding
  integration pins).

**Phase 2 (2026-04-16, commit `9813d18`):** Rocky encoding —
`rocky.py` (21 events, 11 agents, 1 rule, 2 descriptions),
`rocky_lowerings.py` (23 Lowerings), and
`rocky_dramatica_complete_verification.py` (9 checks). Phase 2
produced the first non-APPROVED DSP_limit verdict in the corpus
and two new verifier patterns (Steadfast via structural
invariance; Failure via goal-opposite-is-evidence).

**Post-Phase-2 spectrum, measured:**

| Encoding | DSP_limit declared | Verdict | Strength | Signals |
|---|---|---|---|---|
| Oedipus | Optionlock | APPROVED | 0.67 | identity-resolution:7 + rule-emergence:9 |
| Macbeth | Optionlock | APPROVED | 0.67 | retraction:1 + rule-emergence:3 |
| Ackroyd | Optionlock | APPROVED | 0.67 | retraction:1 + rule-emergence:2 |
| Rocky   | Timelock   | NEEDS_WORK | 0.33 | retraction:1 + rule-emergence:1 |

Three Optionlock encodings APPROVED with three different signal
compositions; one Timelock encoding NEEDS_WORK via LT5's disagreement
disposition. The finding is not that Rocky was "misclassified" —
LT2's reading of Rocky is honest; both signals are present in the
substrate. The finding is that LT2's current predicate does not
distinguish arc-converging signals (which support Optionlock) from
arc-peripheral signals (which may coexist with Timelock). LT3-strong
is the natural next sketch when a fifth encoding or an explicit
scheduling vocabulary provides the forcing function.

Tests: 25 new tests total across both phases (18 Phase 1 + 7
Phase 2). Full suite: 490 → 515 passed (standard-library suite).

**Findings surfaced by Phase 2 that the sketch did not anticipate:**

1. **Steadfast-via-structural-invariance** is a distinct verifier
   pattern from Steadfast-via-pre-existing-trait (Ackroyd's shape).
   Rocky has no stable-trait predicate; its Steadfast rests on the
   absence of equivalence-class collapses involving the MC. Two
   different verifier evidence shapes for the same DSP axis value.
2. **Failure-as-goal-opposite-evidence.** The Outcome check
   inverts cleanly: under Failure, the compound-derivation fact
   that contradicts the goal IS the evidence supporting the
   declaration. This generalizes to any DSP where the declaration
   is the negative form of a predicate the substrate can derive.
3. **Positive-closure clusters for Judgment=Good.** Unlike the
   Bad-judgment trajectory shapes (tyrant emerging, self-identity
   collapsing, betrayer landing), Judgment=Good is best checked as
   a confluence of multiple positive facts at τ_s=end, not as a
   trajectory emergence. Different verifier shape; same primitive
   (claim-trajectory).

These findings are banked as inputs to a future verifier-patterns
consolidation sketch, not as amendments to this one.
