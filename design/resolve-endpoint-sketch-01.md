# Resolve-endpoint — sketch 01

**Status:** draft, active
**Date:** 2026-04-17
**Supersedes:** nothing (additive, parallel to and composing with [resolve-relational-sketch-01](resolve-relational-sketch-01.md))
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [architecture-sketch-02.md](architecture-sketch-02.md), [verification-sketch-01.md](verification-sketch-01.md), [event-kind-taxonomy-sketch-01](event-kind-taxonomy-sketch-01.md), [event-agency-taxonomy-sketch-01](event-agency-taxonomy-sketch-01.md)
**Related:** four-encoding DSP_resolve checks; **v3** cross-boundary reader-model probe runs (2026-04-17, saved as `*_dramatica_complete_output_v3.json`)
**Superseded by:** nothing yet

## Purpose

Close the **second cross-corpus coherent finding** from the third
(v3) probe pass: three of four encodings' DSP_resolve checks
qualify along a new axis — **MC end-state behavior**, not just
mid-arc transition (Change) or mid-arc absence-of-transition
(Steadfast). The probe is surfacing that Dramatica's Resolve is
about the MC's *final position* vis-à-vis their drive, with the
transition itself being necessary but not sufficient evidence.

Three parallel v3 qualifications:

- **Rocky (Steadfast)**: `articulated_goal` entering at τ_s=45 IS
  a state change, just not a paradigm change. Probe wants IC-
  resistance (RR3) promoted to lead signal, with zero-identity-
  transition as supporting.
- **Macbeth (Change)**: "I will not yield" terminal beat could
  read as Steadfast commitment despite mid-arc tyrant-transition.
  Probe wants end-state yielding/doubling-down check.
- **Oedipus (Change)**: self-blinding could be read as embodied
  adoption of Jocasta's "don't look" IC counter-premise. Probe's
  suggestion crystallizes the OQ1 banked in IG2.

Seventh concrete probe → sketch cycle in two days. Adds a
second layer to the DSP_resolve check surface (first layer:
RR3 IC-relational; this layer: end-state behavioral-shift).

## What this sketch commits to

- An **end-state behavioral-shift signal** on Change DSP_resolve
  checks: compare the MC's EK2 action-shape distribution
  pre-transition vs. post-transition. Shift = structural
  evidence of behavioral change beyond the identity-transition
  itself.
- A **core-drive-persistence note** on Steadfast DSP_resolve
  checks: verify the MC's defining fact (betrayer_of_trust for
  Ackroyd; articulated_goal for Rocky) holds at τ_end. Report
  state-additions separately (Rocky's τ_s=45 goal entry is a
  state-addition, not a paradigm-reversal).
- All signals are **additive to comment** — no verdict polarity
  changes in the current corpus. Parallel to RR3's honesty-about-
  measurement framing.
- Zero substrate changes. Uses existing EK2 classifier
  (`classify_event_action_shape`) and existing knowledge /
  world projections.

## What this sketch does NOT commit to

- **Flipping Macbeth's Change verdict to Steadfast.** The probe
  noted Macbeth's terminal "I will not yield" reads like a
  doubling-down. The sketch reports this as a NOTED textual
  signal in the comment but does not flip the verdict — the
  mid-arc tyrant-transition is real, and Dramatica's Change is
  still the authorial declaration the substrate supports
  structurally. This is a v3 OQ1 banked for deeper sketch work
  if it becomes a forcing function.
- **An IC-counter-premise vocabulary.** Detecting "Oedipus's
  self-blinding embodies Jocasta's don't-look" requires a
  canonical IC-premise extraction that the Dramatic dialect
  doesn't currently support. We commit to the weaker but
  structurally tractable signal (behavioral-shift pre/post
  transition via EK2), and bank IC-premise-alignment as OQ2.
- **Generalizing to DSP_approach or DSP_growth.** Those axes
  have their own proxies and the v3 probe surfaced DSP_approach
  / DA_mc independence concerns, not end-state concerns.

## Commitments

### RE1 — Classifier reads fold-visible structure

Parallel to EK1 / LT1 / AG1 / IG1 / MN1 / BW1 / RR1. The
end-state signal is a function of the MC's participation events'
EK2 action-shape classification pre vs. post the transition τ_s.

### RE2 — End-state behavioral-shift predicate (Change)

For Change encodings with a detected transition τ_s:

1. Partition the MC's participation events into pre-transition
   (τ_s < transition_τ) and post-transition (τ_s ≥ transition_τ).
2. Compute `external_ratio_pre` = fraction of pre events classified
   as external-action under EK2.
3. Compute `external_ratio_post` = fraction of post events
   classified as external-action.
4. **Behavioral-shift detected** if `abs(pre - post) ≥ 0.3`
   (30-point absolute gap in external-action ratio).
5. Report both ratios and the shift decision.

For Oedipus: pre-anagnorisis includes interrogation utterances
(listener role — AG3-pursuit under existing predicate, external
under some participant rubrics). Post-anagnorisis includes self-
blinding (agent on self — AG2-consequential) and exile (passive).
EK2 shape ratio will shift meaningfully.

For Macbeth: both pre-transition (killing Duncan) and post-
transition (killing Banquo, fighting Macduff) are external-action
events. Shift will NOT meet threshold. The check reports "no
behavioral shift" — honest signal that Macbeth's Change is
structurally located at the identity level, not the behavioral
level.

### RE3 — Core-drive-persistence signal (Steadfast)

For Steadfast encodings:

1. Identify the MC's defining fact (per the existing check:
   betrayer_of_trust for Ackroyd; articulated_goal-entry-τ for
   Rocky).
2. Verify the fact persists through τ_end in world state or
   knowledge state.
3. Report state-additions separately (Rocky's articulated_goal
   entering at τ_s=45 is a state-addition around an already-
   stable core drive; this is noted distinctly from paradigm-
   reversal).
4. For Ackroyd: no state-additions expected; clean persistence.

### RE4 — Per-encoding DSP_resolve enrichment

Each DSP_resolve check appends an RE signal block to its verdict
comment:

- Oedipus (Change): add RE2 behavioral-shift signal.
- Macbeth (Change): add RE2 behavioral-shift signal; honest report
  if shift does not fire.
- Rocky (Steadfast): add RE3 core-drive-persistence note,
  including the τ_s=45 state-addition (articulated_goal entry)
  explicitly flagged.
- Ackroyd (Steadfast): add RE3 core-drive-persistence note.

All four verdicts stay APPROVED 1.0 under current substrate.

### RE5 — Shared helper in `verifier_helpers.py`

`compute_pre_post_action_ratios(mc_id, transition_τ, events_in_
scope, agent_ids)` returns:

```python
{
    "pre_count": int,
    "post_count": int,
    "pre_external_ratio": float,
    "post_external_ratio": float,
    "shift": float,           # abs(pre - post)
    "shift_detected": bool,   # shift >= 0.3
}
```

Parallel in shape to `detect_preceding_ic_event`. Verifier-local.

## Worked case — Oedipus (Change)

Pre-anagnorisis events (τ_s ∈ [0, 13)):
- E_tiresias_accusation, E_jocasta_mentions_crossroads,
  E_messenger_polybus_dead, E_messenger_adoption_reveal,
  E_shepherd_testimony — 5 events; all utterances. Under EK2
  with Oedipus as listener but present participant: mostly
  classified external-action (the speaker acting externally,
  participants including Oedipus).

Post-anagnorisis events (τ_s ≥ 13):
- E_oedipus_anagnorisis (realization, internal), E_self_blinding
  (agent on self — AG2-consequential, EK2 mixed),
  E_exile (passive, external via Creon).

Expected ratio shift: moderate — pre is higher-external-ratio
(witnesses acting on Oedipus); post is lower-external-ratio (MC
self-directed / passive). If threshold 0.3 is met, behavioral-
shift detected.

**Predicted: shift may or may not fire at 0.3 threshold depending
on EK2's exact classification.** If it fires, RE2 reports
strengthened Change signal; if not, RE2 reports honestly.

## Worked case — Macbeth (Change)

Pre-transition events (τ_s < 6):
- E_prophecy_first, E_prophecy_received, E_thane_of_cawdor_
  awarded, E_letter_to_lady_macbeth, E_plot_duncan's_visit,
  E_duncan_killed. Most are external-action.

Post-transition events (τ_s ≥ 6):
- E_macbeth_crowned, E_banquo_killed, E_banquet_ghost,
  E_prophecy_second, E_macduff_family_killed, E_birnam_moves,
  E_macduff_reveals_birth, E_macbeth_killed. Most are external-
  action (plus apparition events which EK2 may classify
  mixed).

**Predicted: shift does NOT fire at 0.3 threshold.** Both halves
are action-dominated. RE2 reports "no behavioral shift — the
Change is structurally at the identity level (tyrant emergence),
not the action-shape level. Macbeth's terminal 'I will not yield'
doubling-down reads as Steadfast commitment at the behavioral
layer even under Change at the identity layer."

This is honest: the v3 probe's observation that Macbeth's final
beat looks Steadfast-shaped is surfaced structurally.

## Worked case — Rocky (Steadfast)

Core drive: `articulated_goal(rocky, went_the_distance)` entering
at τ_s=45, persisting through τ_s=57.

RE3 report: "Rocky's core drive entered at τ_s=45 (state-addition
around the arc's midpoint), persists through τ_end=57. State-
addition is not a paradigm-reversal; Steadfast reading preserved.
Distinct from Ackroyd's Steadfast (pre-arc trait) — Rocky's is
mid-arc-articulated but stable post-articulation."

Verdict unchanged (APPROVED 1.0). Comment enriched.

## Worked case — Ackroyd (Steadfast)

Core drive: `betrayer_of_trust(sheppard, ackroyd)` derives at
τ_s=1 and holds through τ_s=11.

RE3 report: "Ackroyd's defining fact `betrayer_of_trust` derives
at τ_s=1 and holds through τ_end=11. No state-additions around
it; clean pre-arc trait persistence. Steadfast fully confirmed
at both identity and end-state levels."

Verdict unchanged (APPROVED 1.0). Comment enriched.

## Implementation brief

1. Add `compute_pre_post_action_ratios` to `verifier_helpers.py`
   per RE5.
2. Enrich four DSP_resolve checks with RE2/RE3 signals per RE4.
3. Add unit tests for the helper (synthetic pre/post fixtures).
4. Integration pins: each DSP_resolve comment carries RE
   signal; verdict polarity unchanged across all four.
5. Update `design/README.md` to register sketch-01 and the v3
   cross-corpus landing.
6. Update root `README.md` with seventh-cycle note.

## Measurements prediction

- All four DSP_resolve: APPROVED 1.0 → APPROVED 1.0 (no polarity
  change). Comments enriched with RE signals.
- Oedipus: RE2 fires OR reports "no shift" honestly.
- Macbeth: RE2 reports "no shift" (honest signal matching v3
  probe observation about terminal doubling-down).
- Rocky: RE3 reports state-addition + persistence.
- Ackroyd: RE3 reports clean pre-arc-trait persistence.

**Third landing where verdict polarity doesn't change** (after
BW4 and RR3). Honesty-about-measurement accumulates:
seven cycles, three of them measurement-refinements rather than
verdict-flips.

## Discipline

- **Additive, like RR3.** Existing checks untouched; RE signal
  is new textual content, not a new verdict source.
- **Honesty over hero-shot.** If Macbeth's behavioral shift
  doesn't fire, the check says so; it doesn't squeeze the
  substrate to produce a Change-strengthening reading. The
  probe's v3 observation about terminal doubling-down is
  preserved as structural signal.
- **Weak predicate is the intentional choice.** A stronger
  predicate (IC-premise-alignment, for instance) would require
  new vocabulary; the 30-point external-action-ratio gap is
  the honest minimum that closes the v3 finding without
  over-reaching.

## Open questions

1. **IC-counter-premise alignment check for Change.** The v3
   Oedipus probe explicitly suggested this (self-blinding as
   embodied adoption of Jocasta's "don't look"). Implementing
   it would require IC-premise vocabulary on the Dramatic
   dialect — a schema addition. Banked.
2. **Macbeth's "I will not yield" as Steadfast behavioral
   commitment.** V3's observation is valid: Macbeth's terminal
   beat reads as commitment-to-drive-at-death, which is a
   Steadfast shape behaviorally even though his identity
   transitioned at τ_s=6. This is a real Dramatica question
   (Change at what level — identity, behavior, paradigm?)
   that the current sketch doesn't resolve.
3. **Threshold tuning.** The 30-point external-action-ratio
   gap is a starting-point threshold. If future encodings show
   the threshold is too loose or too tight, tune.
4. **Rocky's state-addition framing.** Is `articulated_goal`
   entering mid-arc a Steadfast state-addition, a Growth=Start
   signal (DSP_growth), or both? The two axes may be reading
   the same substrate fact from different angles. Not a
   forcing function here.

## Summary

- All four DSP_resolve checks enriched with end-state signals
  (RE2 for Change, RE3 for Steadfast).
- Closes v3's second cross-corpus coherent finding — three of
  four encodings qualified on DSP_resolve end-state axis.
- Verdict polarity unchanged across corpus (all four stay
  APPROVED 1.0); comments carry new structural signal.
- Seventh probe → sketch cycle in two days. Second
  end-state-layer landing on the DSP_resolve axis (after RR3's
  IC-relational layer).
- Pattern: the DSP_resolve axis has produced three successive
  layers of probe findings — per-encoding proxies (v1 →
  AG5), cross-corpus IC-relational (v2 → RR3), cross-corpus
  end-state (v3 → RE). Each landing produces the NEXT-sharper
  observation. The probe/verifier loop has practically
  open-ended depth.
