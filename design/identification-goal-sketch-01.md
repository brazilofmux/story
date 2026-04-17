# Identification-goal trajectory — sketch 01

**Status:** draft, active
**Date:** 2026-04-17
**Supersedes:** nothing
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [architecture-sketch-02.md](architecture-sketch-02.md), [substrate-sketch-05.md](substrate-sketch-05.md), [verification-sketch-01.md](verification-sketch-01.md), [reader-model-sketch-01.md](reader-model-sketch-01.md), [identity-and-realization-sketch-01.md](identity-and-realization-sketch-01.md), [inference-model-sketch-01.md](inference-model-sketch-01.md)
**Related:** `oedipus_dramatica_complete_verification.py` (Story_goal trajectory check); Oedipus cross-boundary probe qualification on Story_goal (`reader_model_oedipus_dramatica_complete_output.json`, committed 2026-04-17 at `faaebd8`)
**Superseded by:** nothing yet

## Purpose

Close the Oedipus cross-boundary reader-model probe's qualification
on Story_goal (PARTIAL 0.7). The probe named a category error in the
verifier's trajectory check: it reads **world-state** order
(fabula-order) for a goal that is fundamentally **identification-
shaped** (the Story_goal is achieved when the investigator comes to
*know* something, not when a world-fact changes). For recognition/
mystery stories, the load-bearing trajectory is epistemic accretion,
not world-state accretion.

The fix makes the distinction explicit and refactors the Oedipus
check to use knowledge-projection instead of world-projection.
Ackroyd's existing Story_goal check already uses this pattern (it
tracks `killed(sheppard, ackroyd)` spreading through key witnesses'
KnowledgeStates over the arc) — so the sketch formalizes what
Ackroyd was doing right and corrects Oedipus's parallel mistake.

Third concrete probe → sketch → measurement-shift cycle in two days
(after LT9 scheduling and AG5 pursuit/consequential).

## What the probe proposed

From `reader_model_oedipus_dramatica_complete_output.json`,
verifier_commentaries entry for `dramatica-complete:Story_goal`
(assessment: qualifies):

> "The partial-match at 0.7 with the note about 'unusual premise
> order' deserves a clarification. The verifier flags that
> killed_τ=-48 comes after child_of_τ=-100 in fabula time as
> atypical, but in Oedipus Rex's recognition structure, the
> *revelation* order is reversed: the killing at the crossroads is
> known or suspected before the parentage is confirmed. The fabula
> order (birth before killing) is simply chronological and not
> unusual at all. If the check is evaluating sjuzhet-order
> derivation (the order in which the audience/characters learn the
> premises), then the order matters; if it's evaluating fabula-order
> causality, then birth-before-killing is trivially expected."

And `suggested_signature`:

> "Consider adding a flag for recognition/mystery story structures
> where the goal-derivation's premise-revelation order is expected
> to be reversed relative to fabula order, and adjusting the
> 'atypical buildup' penalty accordingly."

## What this sketch commits to

- A semantic distinction between **identification-shaped** goals
  (arrival condition: investigator gains knowledge of a specific
  derivation) and **achievement-shaped** goals (arrival condition:
  a world-state fact holds).
- Identification-goal trajectory checks read
  `project_knowledge(investigator_id, ...)` + `holds_derived(...)`
  rather than `project_world(...)` + `world_holds_derived(...)`.
  The investigator is the agent whose coming-to-know fulfills the
  goal.
- For identification goals, premise order is a knowledge-accrual
  question (sjuzhet/revelation order), not a world-assertion
  question (fabula order). The current Oedipus check's "unusual
  premise order" penalty is a category error when reading a
  fabula-predating substrate.
- Zero substrate changes. The fix reads existing
  `KnowledgeEffect` / `Held` records via existing
  `project_knowledge` / `holds_derived` APIs — both shipped in
  substrate.py.
- The goal-kind distinction is verifier-local, not a substrate
  commitment. Per encoding, each Story_goal check picks the
  appropriate shape based on the goal's semantic nature.

## What this sketch does NOT commit to

- **A new field on Story_goal records.** The goal-kind distinction
  lives in per-encoding verifier logic, not in the
  `dramatica_template.py` Story record. An encoding's author picks
  the check shape based on what the goal *means*. This avoids
  premature schema addition per A3.
- **Refactoring Macbeth or Rocky's Story_goal checks.** Both goals
  are achievement-shaped: Macbeth's "restore Scotland's rightful
  succession" resolves when a legitimate king holds the throne;
  Rocky's "clean publicity stunt" resolves when the stunt runs as
  scripted. World-state trajectory applies; no refactor needed.
- **Refactoring Ackroyd's check.** Ackroyd's check is already
  knowledge-aware (tracks `killed(sheppard, ackroyd)` through
  `project_knowledge` + `holds_as(Slot.KNOWN)` across a witness
  set). The sketch formalizes what Ackroyd's check was doing right;
  no code change to Ackroyd.
- **A universal "all goals should be knowledge-aware" rule.**
  Achievement goals are perfectly well-measured by world-state.
  The knowledge/world distinction is per-goal, not system-wide.
- **Handling the "investigator" concept at the substrate layer.**
  The investigator is a verifier-local identification — typically
  the MC, sometimes a Detective or Reader as appropriate. Per-
  encoding, the check declares who the investigator is.

## Commitments

### IG1 — Identification-vs-Achievement goal distinction

A Story_goal is **identification-shaped** if its arrival condition
is an epistemic claim about a specific agent (typically the MC):
"the investigator comes to know X" where X is a derived proposition
assembled from the substrate's premise structure.

A Story_goal is **achievement-shaped** if its arrival condition is
a world-state claim: "the world proposition Y holds (or stops
holding) at τ_end".

Both are valid Story_goal shapes. Both are claim-trajectory-
primitive-compatible. The distinction determines which projection
the trajectory check reads.

Current corpus (post-sketch-01):
- **Oedipus**: identification ("identify the pollution causing the
  plague"). Investigator: Oedipus. Target derivation:
  `parricide(oedipus, laius)`.
- **Ackroyd**: identification ("identify the killer of Roger
  Ackroyd"). Investigator: the witness-set (Poirot + Caroline +
  Raglan + Flora). Target proposition: `killed(sheppard, ackroyd)`
  at Slot.KNOWN.
- **Macbeth**: achievement ("restore Scotland's rightful
  succession"). World-state resolution at τ_end.
- **Rocky**: achievement ("stage Apollo's bicentennial heavyweight
  title defense as a clean publicity event"). World-state
  resolution at τ_end (Failure: stunt contamination holds instead).

### IG2 — Identification-goal trajectory check reads knowledge-projection

For identification goals, the trajectory check uses the substrate's
agent-knowledge API:

- `project_knowledge(investigator_id, events_in_scope, up_to_τ_s)`
  returns the KnowledgeState at that τ_s.
- `holds_derived(state, target_prop, rules)` returns `(Slot, Proof)`
  if the investigator's knowledge — with identity substitution and
  rule derivation — supports the target prop; `None` otherwise.

The trajectory check walks τ_s in order, asking: at which τ_s does
the target derivation first become supportable by the investigator's
knowledge? That's the **recognition τ_s** — the point at which the
goal is achieved (for the investigator).

For Oedipus the recognition τ_s is **13** (anagnorisis). Before
τ_s=13, Oedipus's knowledge does not support `parricide(oedipus,
laius)` — the identity substitutions that collapse
`the-crossroads-victim` with `laius` and `oedipus's-father` with
`laius` haven't landed yet. At τ_s=13 the equivalence class
collapses via the anagnorisis's identity-assertion, and the
derivation becomes supportable.

### IG3 — Fabula-order vs. revelation-order

For identification goals, premise order is a **knowledge-accrual**
question. The verifier asks: did the investigator's knowledge of
the target's premises accrue *in the arc proper* (τ_s ≥ 0)? Not:
did the world-facts get asserted in fabula order?

The current Oedipus check penalized `killed_τ=-48 ≥ child_of_τ=-100`
as "unusual premise order". Under IG3 this check is a category
error: both premises are world-true pre-plot (κilled at the
crossroads; child_of from birth), and the order of their
pre-plot assertion is narratively irrelevant. What matters
dramatically is when Oedipus's knowledge catches up — and that
happens at a single τ_s (the anagnorisis), not as an ordered
accrual.

### IG4 — Back-compat for achievement goals

Achievement-shaped goals (Macbeth's succession; Rocky's stunt)
continue to use world-projection + `world_holds_derived`. The
verifier's trajectory check for those goals is unchanged by this
sketch. IG1's distinction is a per-goal property, not a
system-wide flag.

### IG5 — Goal-kind distinction is verifier-local

Per EK5 / LT6 / AG6, the identification/achievement distinction is
a property of the verifier surface, not the substrate. Each
encoding's `story_goal_trajectory_check` picks the appropriate
shape; the substrate exposes both `project_world` and
`project_knowledge` uniformly.

Future Template work could add a `goal_kind` field to the Story
record or to a `StoryGoal` record, making the choice declarative
rather than embedded in the check function. Deferred — the
per-encoding check is honest for the current corpus. See OQ2.

## Worked case — Oedipus under IG2

The refactored Oedipus Story_goal trajectory check:

1. Walk τ_s in increasing order.
2. At each τ_s, project Oedipus's knowledge
   (`project_knowledge("oedipus", events_in_scope, up_to_τ_s)`).
3. Ask: does `holds_derived(state, parricide(oedipus, laius),
   RULES)` return a non-None result?
4. The first τ_s where this is True is the **recognition τ_s**.
5. Verdict:
   - **APPROVED 1.0** if recognition τ_s is in the arc proper
     (τ_s ≥ 0) and Oedipus is the MC (parity with the author's
     intent).
   - **PARTIAL** if recognition happens but in an odd place (τ_s
     < 0, suggesting pre-plot knowledge; or at τ_end only,
     suggesting the buildup was absent).
   - **NEEDS_WORK** if the derivation is never supportable from
     Oedipus's knowledge.

Measured under this predicate:

- Oedipus's knowledge does not support `parricide(oedipus, laius)`
  at any τ_s < 13 (no substitution available; equivalence class
  not yet collapsed).
- At τ_s=13 (the anagnorisis event), the identity-assertion
  `identity(oedipus, the-exposed-baby)` collapses the equivalence
  class linking `oedipus`, `the-crossroads-victim`, and `laius`'s
  killer; substitution over his held beliefs makes
  `killed(oedipus, laius)` and `child_of(oedipus, laius)` supportable
  via the substitution chain; `parricide` derives via
  `PARRICIDE_RULE`.
- **Recognition τ_s = 13. Mid-arc (0 ≤ 13 ≤ 17). APPROVED 1.0.**

Net shift: PARTIAL 0.7 → **APPROVED 1.0**. The "unusual premise
order" language is removed; the trajectory is cleanly reported as
an epistemic pivot at the anagnorisis.

## Worked case — Ackroyd as precedent (no-regression)

Ackroyd's existing Story_goal check tracks how many of the four
key witnesses (Poirot, Caroline, Raglan, Flora) hold
`killed(sheppard, ackroyd)` at `Slot.KNOWN` between τ_s=2
(investigation start) and τ_end. The signature is "knowledge
expansion from 0/4 to 4/4 across the arc." This is identification-
shaped per IG1 — the goal resolves when the witness-set comes to
know the killer — and the check already uses `project_knowledge`
per IG2 .

No refactor needed. Ackroyd's check is the precedent the Oedipus
refactor aligns to. The sketch formalizes what Ackroyd's author was
doing by instinct into a verifier commitment.

## Worked case — Macbeth and Rocky (achievement, no-regression)

Macbeth's `story_goal_trajectory_check` asks whether the
`succession` world-predicate returns to a legitimate line by
τ_end. Rocky's asks whether the `clean_stunt` preconditions hold
at τ_end (and finds them contaminated by `went_the_distance`). Both
are world-state trajectory checks; both stay. IG1's distinction is
declarative-by-semantics, not a forced refactor.

## Implementation brief

1. **Refactor `story_goal_trajectory_check` in
   `oedipus_dramatica_complete_verification.py`:**
   - Import `project_knowledge`, `holds_derived` from substrate.
   - Replace world-projection loop with knowledge-projection loop
     over Oedipus's state.
   - Target derivation: `parricide(oedipus, laius)` via
     `holds_derived(state, parricide_prop, RULES)`.
   - Verdict: APPROVED 1.0 on mid-arc recognition; PARTIAL or
     NEEDS_WORK on edge cases.
2. **Rewrite stale Oedipus Story_goal test** pinning the PARTIAL
   0.7 verdict to instead pin APPROVED 1.0 under IG2.
3. **Add new unit-level tests** exercising the knowledge-vs-world
   distinction on synthetic fixtures (a simple recognition
   fixture where world-asserts happen pre-plot but knowledge
   accrues mid-arc; a simple achievement fixture where world-state
   changes mid-arc).
4. **Update `design/README.md`** to register sketch-01 under a new
   bullet; promote the probe's Oedipus Story_goal qualification
   from "banked" to "landed".
5. **Update root `README.md`** with the Story_goal shift note and
   the "three probe proposals landed" count.

No substrate changes. No new event types. No dialect changes.

## Measurements prediction

- Oedipus Story_goal: PARTIAL 0.7 → **APPROVED 1.0**.
- Macbeth Story_goal: unchanged (achievement, world-state check).
- Ackroyd Story_goal: unchanged (already knowledge-aware).
- Rocky Story_goal: unchanged (achievement, world-state check).

Net shift: one encoding's verdict upgrade. Parallel to LT9's Rocky
shift and AG5's Oedipus DSP_growth shift — a single measurement
change driven by a probe proposal, adopted cleanly at the verifier
layer.

## Discipline

- **The knowledge/world distinction is not a generalization.** It
  applies to Story_goal trajectory checks for identification-
  shaped goals specifically. Other claim-trajectory checks (e.g.,
  DSP_judgment=Good's positive-closure cluster) don't need to
  pivot on this distinction — those are world-state claims.
- **IG2 composes with the identity-and-realization substrate.**
  `holds_derived` is the substitution-aware query; it already
  handles equivalence-class collapse at the anagnorisis event per
  identity-and-realization-sketch-01's I3/I7. The sketch commits
  to using the existing machinery, not building new.
- **The "investigator" is identification, not prescription.** For
  Oedipus, it's the MC. For Ackroyd, it's a witness-set (per the
  existing check). For a future encoding, it might be a Detective
  character distinct from the MC, or a Reader-role agent. The
  check declares; the sketch doesn't enforce one pattern.

## Open questions

1. **Achievement-shaped identifier predicates.** Ackroyd's goal is
   "identify the killer AND recover the moral order". The first
   half is identification; the second is achievement. The current
   check tracks only the first half. A future Story_goal could
   split into a two-part trajectory (identification phase +
   achievement phase). Deferred.

2. **Declarative goal-kind on the Story record.** Adding a
   `goal_kind: "identification" | "achievement"` field to the
   `Story` or a new `StoryGoal` record would make the distinction
   declarative at the dialect layer, not embedded in the check
   function. Worth considering when the corpus grows past four
   encodings, or when a multi-goal structure (like OQ1) forces it.

3. **Non-MC investigators.** Ackroyd uses a witness-set rather
   than a single investigator. A future identification-goal check
   that tracks knowledge across MULTIPLE investigators (an
   ensemble mystery) would need the trajectory to be
   per-investigator-then-aggregated. Current Ackroyd check does
   this via the `knowers` tuple; could generalize. Not forced now.

4. **View vs. sjuzhet visibility (item 8 in design-README).** The
   identification-goal check uses `project_knowledge` — which is
   τ_s-indexed, not τ_d-indexed. Descriptions making claims about
   reader-disclosure-schedule ("the reader has held both premises
   since τ_d=0") still can't be verified by this check. The OQ
   remains open; IG2 doesn't close it but is compatible with
   whatever τ_d-aware machinery eventually lands.

5. **Story_consequence parallel.** Story_consequence is a
   claim-moment check at τ_end. If a consequence is identification-
   shaped ("the killer goes undetected" as a failure consequence,
   which is a *knowledge* claim — no one comes to know), it should
   read knowledge-projection too. Not a current forcing function
   (Ackroyd's Story_consequence happens to land via world-fact
   anyway), but banked.

## Summary

- Oedipus Story_goal PARTIAL 0.7 → APPROVED 1.0 predicted, driven
  by the 2026-04-17 cross-boundary probe's qualification.
- Two goal shapes recognized: **identification** (epistemic
  arrival) and **achievement** (world-state arrival). Per-encoding
  check picks the appropriate projection.
- Oedipus Story_goal check refactored to use `project_knowledge` +
  `holds_derived` — the recognition τ_s at the anagnorisis (τ_s=13)
  IS the trajectory's landing point, not an "atypical buildup".
- Ackroyd's check is already knowledge-aware; the sketch formalizes
  what it was doing. Macbeth and Rocky are achievement-shaped;
  their world-state checks remain.
- Zero substrate changes. Third concrete probe → sketch →
  measurement-shift cycle in two days. Three probe-proposed
  signatures now landed (LT9 scheduling, AG5 agency, IG2
  identification-goal); two banked (Ackroyd DA_mc manipulation,
  Macbeth DA_mc beat-weighting).
