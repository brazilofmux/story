# Event-agency taxonomy — sketch 01

**Status:** draft, active
**Date:** 2026-04-17
**Supersedes:** nothing (new topic; parallel to [event-kind-taxonomy-sketch-01](event-kind-taxonomy-sketch-01.md) and [pressure-shape-taxonomy-sketch-01](pressure-shape-taxonomy-sketch-01.md))
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [architecture-sketch-02.md](architecture-sketch-02.md), [substrate-sketch-05.md](substrate-sketch-05.md), [verification-sketch-01.md](verification-sketch-01.md), [reader-model-sketch-01.md](reader-model-sketch-01.md)
**Related:** `verifier_helpers.py` (the DSP_growth=Stop check family); Oedipus cross-boundary probe dissent on DSP_growth (`reader_model_oedipus_dramatica_complete_output.json`, committed 2026-04-17 at `faaebd8`)
**Superseded by:** nothing yet

## Purpose

Close the Oedipus cross-boundary reader-model probe's dissent on
DSP_growth PARTIAL 0.5. The current Oedipus DSP_growth=Stop check
uses raw participation-rate comparison pre/post anagnorisis; the
probe correctly named it too coarse: **Oedipus's participation rate
actually goes UP post-anagnorisis** (self-blinding at τ_s=15; exile
at τ_s=17) while his **pursuit activity** (investigating, questioning
witnesses) drops to zero. Growth=Stop's load-bearing signature is the
cessation of a problematic drive, not raw activity levels.

This sketch commits a structural event-agency classifier that
distinguishes **agentive-pursuit** from **reactive-consequential**
events, parallel to EK2's external-action / internal-state classifier
and LT7's arc-position banding — all three are verifier-layer tools
that read fold-visible structure rather than type-string tags.

Second concrete landing of the probe/verifier loop, parallel to
sketch-02's LT3-strong — probe dissent → sketch → measurement shift.

## What the probe proposed

From `reader_model_oedipus_dramatica_complete_output.json`,
verifier_commentaries entry for `dramatica-complete:DSP_growth`
(assessment: dissents):

> "The check measures Oedipus's participation rate pre/post
> anagnorisis (0.38 → 0.75) and interprets the absence of a 'sharp
> drop' as weak support for Growth=Stop. But Growth=Stop in Dramatica
> refers to the MC needing to stop a problematic drive or behavior —
> here, Oedipus's relentless pursuit of truth. The relevant signature
> isn't raw event participation but the *type* of participation: pre-
> anagnorisis Oedipus is actively investigating (pursuing, questioning,
> pressuring witnesses); post-anagnorisis he is acted upon or acting
> on himself (self-blinding, being exiled). The participation rate
> going UP post-anagnorisis is actually consistent with Stop growth
> — the consequences of the problem that needed stopping now cascade.
> Raw participation rate is too coarse a proxy for this dynamic."

And `suggested_signature`:

> "Consider distinguishing agentive-pursuit events (where the MC
> initiates investigation/confrontation) from reactive/consequential
> events (where the MC suffers or enacts consequences). A Growth=Stop
> signature would show the pursuit-type events ceasing after a
> critical point, even if total participation increases."

## What this sketch commits to

- A structural classifier at the event level: given an event and
  an MC entity id, classify as `"pursuit"` / `"consequential"` /
  `"neutral"` / `None` (MC not participant).
- A consequential-event predicate (AG2) based on world-effect
  target: an event is consequential iff it asserts at least one
  world-fact whose prop's first argument is the MC's entity id.
  This detects self-directed state changes (blinding, exile,
  punishment), revelations landing on the MC, and consequential
  effects that target the MC's state.
- A pursuit-event predicate (AG3) by complement-on-participation:
  an event is pursuit-shaped iff MC is a participant, the event
  is not consequential (AG2), and the event has at least one
  non-MC-targeting effect. Deliberately permissive —
  investigation-era events where MC summons / questions / pressures
  others fit even when MC's role is nominally passive (`listener`
  in utterance events where MC has summoned the speaker).
- A Growth=Stop refinement (AG5): the DSP_growth=Stop check
  measures pursuit-event rate across arc positions, not raw
  participation rate. Stop's load-bearing signature is pursuit
  activity ceasing — regardless of whether consequential activity
  rises.
- Zero substrate changes. The predicate reads existing
  WorldEffects and participants dictionaries.

## What this sketch does NOT commit to

- **Changes to participant role vocabularies.** Encodings author
  roles per their narrative needs (`listener`, `speaker`,
  `subject`, `killer`, `fighter_a`, etc.). The classifier
  deliberately avoids role-name dispatch per AG1 / EK1 / LT1.
- **Replacing existing Growth=Stop checks that already work.**
  Macbeth's `dsp_growth_stop_trajectory_check` uses monotonic
  kill-accumulation (counting the `killed(macbeth, X)` predicate's
  growth). That check is already pursuit-oriented — it measures
  the cumulative behavior needing to stop. AG5 does not force a
  refactor of Macbeth's check; it provides a second pattern for
  encodings where the problematic drive doesn't show up as a
  monotonically-accumulating compound.
- **Changes to Ackroyd's or Rocky's DSP_growth=Start checks.**
  Start is a different axis from Stop; this sketch addresses Stop
  only. Start checks remain unchanged.
- **A general pursuit/consequential distinction at the substrate
  layer.** The classifier is verifier-local (AG6). Substrate
  events carry effects; the agency distinction is a
  verifier-layer reading of those effects relative to a specified
  MC.
- **Multi-MC scenarios.** The classifier takes a single `mc_id`.
  Ensemble stories with multiple MCs would need multiple
  classifications. Deferred as OQ2.

## Commitments

### AG1 — Verifier classification reads fold-visible structure, not type strings

Parallel to EK1 and LT1. The pursuit / consequential predicate is
a function of the event's WorldEffects, KnowledgeEffects, and
participants dict — the same fold-visible surface EK2 and LT7 read.
Event type strings may inform priors but are not the sole
classifier input. Encodings extending the substrate with new event
types do not need to update the agency classifier.

### AG2 — Consequential-event predicate (strong)

An event is **consequential-shaped with respect to MC** if the
event's effects include **at least one `WorldEffect` whose `prop`
asserts a fact whose first argument equals `mc_id`**.

Examples from Oedipus:
- `E_self_blinding` asserts `blinded(oedipus)` — consequential.
- `E_exile` asserts `exiled(oedipus, thebes)` — consequential
  (first arg is `oedipus`).
- `E_tiresias_accusation` asserts no world-facts about oedipus-
  state; the accusation is a knowledge transfer, not a world-fact
  change — NOT consequential.

The first-argument convention is structural: world-facts about X's
state conventionally have X as their first argument (`blinded(X)`,
`exiled(X, place)`, `killed(killer, X)` — the last case is handled
by AG2's signal being **at least one** first-arg-matching effect,
so it still fires when MC is a victim of another agent's action).

Edge case: `killed(macbeth, duncan)` asserts a fact whose first arg
is macbeth. If we run AG2 against Duncan as MC, the predicate does
NOT fire for this event (Duncan's first arg in `killed` is the
second position). This is intentional — the classifier sees what
the substrate encodes and classifies from MC's structural position.
When Duncan is the MC (hypothetical), the same event would be
classified via MC-as-second-arg detection — which would require a
broader predicate. AG2's first-arg-only rule is the simple case.
See OQ1 for the strengthening question.

Per LT1 / EK1 discipline, AG2 does not inspect event type strings
or participant role names — only the WorldEffect prop structure.

### AG3 — Pursuit-event predicate (by complement on participation)

An event is **pursuit-shaped with respect to MC** if:

1. MC is a participant in the event, AND
2. The event is not consequential-shaped per AG2, AND
3. The event has at least one effect (WorldEffect or
   KnowledgeEffect) not exclusively targeting MC's state.

Condition (3) is a weak sanity check that excludes events that do
nothing (null-effect events, if any exist).

This predicate is deliberately permissive — a "listener" utterance
event where Oedipus has summoned the speaker fires pursuit because
the knowledge-effect targets Oedipus's state (Oedipus-gains-
knowledge) but does NOT assert a world-fact about the oedipus
entity. The AG2 predicate is reserved for world-state changes
targeting the MC; knowledge transfer TO the MC is pursuit-shaped
(MC is acquiring information), even if the MC's structural role is
nominally passive.

### AG4 — Classifier lives in `verifier_helpers.py`

Parallel to EK3 and LT4. Signature:

```python
def classify_event_agency_shape(
    event: Event,
    mc_id: str,
) -> Optional[str]:
    """Returns 'pursuit' / 'consequential' / 'neutral' / None.
    None if MC is not a participant. 'neutral' if MC participates
    but neither predicate fires (rare edge case; e.g., an event
    with only knowledge-effects not involving MC)."""
```

### AG5 — DSP_growth=Stop refinement

Growth=Stop's load-bearing signature under AG3 is: **pursuit-event
count (wrt MC) drops to zero after a critical arc point**. The
critical point is encoded per-story (anagnorisis for Oedipus;
realization / reveal / pivot for other encodings).

Oedipus's DSP_growth=Stop check gets refactored:

- **Before (current):** participation-rate drop pre/post anagnorisis.
  Measured: 0.38 → 0.75 (participation rose), verdict
  PARTIAL_MATCH 0.5.
- **After (under AG5):** pursuit-event count drop pre/post
  anagnorisis. Expected: 5 (all mid-arc utterance events) → 0 (zero
  post-anagnorisis pursuit events — only consequential). Predicted
  verdict: **APPROVED** with strength `min(1.0, 1.0 - (post_pursuit /
  pre_pursuit))` = 1.0 for clean drop-to-zero.

Macbeth's existing check (monotonic kill-accumulation) stays
unchanged — the kill count IS the pursuit signal for Macbeth; AG5's
pursuit-event-count approach would also work, but the existing
check is a legitimate alternative pattern. Both count cumulative
problematic behavior.

### AG6 — The agency frame is verifier-local

Parallel to EK5 and LT6. The pursuit / consequential distinction is
a property of the dramatica-complete → substrate verifier (DSP_growth
reading), not a substrate commitment. Save-the-Cat's analogous
question (MC growth at beat positions) could reuse the classifier
if useful, or could define its own.

## Worked case — Oedipus under AG5

Oedipus's canonical-scope events with `oedipus` as participant
(τ_s ≥ 0), classified under AG2/AG3:

| τ_s | event | MC role | world-effects on oedipus? | classification |
|---|---|---|---|---|
| 3 | E_tiresias_accusation | listener | no | pursuit |
| 5 | E_jocasta_mentions_crossroads | listener | no | pursuit |
| 7 | E_messenger_polybus_dead | listener | no | pursuit |
| 8 | E_messenger_adoption_reveal | listener | no | pursuit |
| 12 | E_shepherd_testimony | listener | no | pursuit |
| 13 | E_oedipus_anagnorisis | agent | knowledge-effects (identity) | neutral-or-pursuit |
| 15 | E_self_blinding | agent | `blinded(oedipus)` | **consequential** |
| 17 | E_exile | subject | `exiled(oedipus, thebes)` | **consequential** |

Pre-anagnorisis (τ_s in [0, 13)): **5 pursuit events, 0 consequential.**
Post-anagnorisis (τ_s ≥ 13): **0 pursuit events, 2 consequential**
(not counting the anagnorisis itself, which is the pivot).

Pursuit drop: 5 → 0 — the signature the probe named, made
structurally detectable.

Expected DSP_growth=Stop verdict under AG5: **APPROVED 1.0** —
perfect drop-to-zero.

## Worked case — Macbeth, Ackroyd, Rocky (no-regression)

- **Macbeth** DSP_growth=Stop — existing kill-accumulation check
  unchanged. Measured APPROVED 1.0, stays APPROVED 1.0.
- **Ackroyd** DSP_growth=Start — different axis, different check
  (ultimatum-compelled start at the interrogation). Unchanged.
- **Rocky** DSP_growth=Start — different axis, different check
  (articulated_goal acquisition at τ_s=45). Unchanged.

Only Oedipus's DSP_growth verdict shifts under AG5. The other three
encodings' checks are untouched.

## Implementation brief

1. **Add `classify_event_agency_shape` to `verifier_helpers.py`.**
   Reads event.effects and event.participants. Returns
   `"pursuit"` / `"consequential"` / `"neutral"` / `None`.
2. **Refactor `dsp_growth_stop_trajectory_check` in
   `oedipus_dramatica_complete_verification.py`.** Replace the
   participation-rate comparison with pursuit-event-count comparison
   pre/post anagnorisis. Message explains the pursuit/consequential
   breakdown.
3. **Add unit tests in `test_verification.py`:**
   - `classify_event_agency_shape` on synthetic events — MC-as-target
     world-effect → consequential; MC-as-participant-with-external-
     knowledge → pursuit; MC-absent → None.
   - Integration pin: Oedipus DSP_growth APPROVED post-AG5.
   - No-regression: Macbeth / Ackroyd / Rocky DSP_growth unchanged.
4. **Update Oedipus verifier's expected-measurements block** if one
   exists.
5. **Update `design/README.md`** to register sketch-01 under a new
   topic bullet; update item 4's (d.1) finding from "banked" to
   "landed".
6. **Update root `README.md`** if the DSP_growth shift changes
   headline numbers enough to warrant mention (probably not — the
   shift is Oedipus-specific).

## Measurements prediction

- Oedipus DSP_growth: PARTIAL 0.5 → **APPROVED 1.0**.
- Macbeth DSP_growth: APPROVED 1.0 (unchanged).
- Ackroyd DSP_growth: APPROVED (unchanged).
- Rocky DSP_growth: APPROVED 1.0 (unchanged).

Net shift: one encoding's verdict upgrade. Parallel to sketch-02's
Rocky DSP_limit shift — a single measurement change driven by a
probe proposal, adopted cleanly at the verifier layer.

## Discipline

- **AG2's first-arg-only rule is honest simplification.** A more
  sophisticated predicate could match ANY argument position for
  the MC id (catching `killed(X, mc_id)` as consequential-for-MC).
  That extension is OQ1; the current rule covers the Oedipus case
  cleanly without overreach.
- **The pursuit predicate is a complement, not a positive
  detector.** AG3 fires broadly — investigation-era participation
  is captured without needing a dedicated "investigation event"
  type. This is the opposite trade from EK2 (which uses a positive
  structural predicate for external-action). Different design
  choice, owned honestly.
- **Checks that already work don't need to adopt AG5.** Macbeth's
  kill-accumulation check is a legitimate alternative pattern for
  Growth=Stop; the sketch does not force it to refactor.
- **The agency frame supports future checks beyond DSP_growth.**
  A future DSP_approach refinement (Do-er vs. Be-er, where the
  dispute hinges on MC's agentive shape) could use the same
  classifier. Not pursued here — EK2's Do-er check works fine
  today.

## Open questions

1. **Multi-argument MC detection.** AG2's first-arg-only rule
   misses cases like `killed(murderer, mc_id)` where the MC is a
   victim in a non-first position. For the current corpus this
   doesn't matter — Oedipus's consequential events encode self-
   directed state via first-arg MC (blinded, exiled). A future
   encoding where the MC is victim of an external agent's action
   with MC in non-first position would need the rule extended.
   The extension is straightforward (match any arg position) but
   risks over-triggering on incidental mentions. Deferred.

2. **Ensemble stories (multiple MCs).** The classifier takes a
   single mc_id. For stories with multiple MCs (e.g., Crash,
   Love Actually), classification would need to be run per-MC.
   This is a loop-pattern at the call site, not a classifier
   issue. Deferred.

3. **The anagnorisis-as-critical-point convention.** The Oedipus
   check uses the realization event as the arc's critical point.
   Encodings without a clean anagnorisis would need a different
   pivot (the confrontation, the reveal, the decision). A general
   "find the critical point" helper could factor out this concern,
   but the current per-encoding pivot-finding is honest.

4. **Growth=Start and Change axes.** AG5 addresses Stop only. Start
   has its own structural signature (acquisition of a new
   proposition, ultimatum-compelled transition) already landed in
   Ackroyd and Rocky. Change (not exercised in the corpus yet) would
   need its own verifier pattern. Not a current forcing function.

5. **Cross-dialect generality.** Save-the-Cat could use an
   analogous pursuit/consequential classification for its Dark
   Night of the Soul vs. Finale beat distinction — the dramatic
   shape is similar (the MC's active drive ceases at a pivot).
   Whether the classifier transplants cleanly is open.

## Summary

- Oedipus DSP_growth PARTIAL 0.5 → APPROVED 1.0 predicted, driven
  by the Oedipus cross-boundary probe's dissent (2026-04-17).
- New verifier-helper classifier `classify_event_agency_shape`
  parallel to EK2 and LT9's scheduling-predicate detection.
- Consequential-event predicate: world-effect asserts fact whose
  first arg is MC_id. Pursuit predicate: complement on
  participating events.
- Oedipus DSP_growth=Stop check refactored to use pursuit-event-
  count drop rather than participation-rate comparison. Other
  encodings' DSP_growth checks unchanged.
- Zero substrate changes. Second concrete probe → sketch →
  measurement-shift cycle in two days. The probe/verifier loop
  replicates.
