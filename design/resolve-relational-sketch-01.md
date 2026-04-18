# Resolve-relational — sketch 01

**Status:** draft, active
**Date:** 2026-04-17
**Supersedes:** nothing (additive refinement; the existing DSP_resolve checks per encoding are preserved and enriched, not replaced)
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [architecture-sketch-02.md](architecture-sketch-02.md), [verification-sketch-01.md](verification-sketch-01.md), [dramatic-sketch-01.md](dramatic-sketch-01.md), [dramatica-template-sketch-01.md](dramatica-template-sketch-01.md)
**Related:** four-encoding DSP_resolve checks in the dramatica-complete verifiers; v2 cross-boundary reader-model probe runs (2026-04-17, all four encodings qualified DSP_resolve along the same axis — saved in `*_dramatica_complete_output_v2.json`)
**Superseded by:** nothing yet

## Purpose

Close the **cross-corpus coherent finding** from the second
(2026-04-17 v2) probe pass: all four encodings' DSP_resolve checks
drew qualifications along the same axis. The probe observed that
the current substrate-proxy checks (identity-transition for Oedipus
/ Macbeth / Rocky; world-state-stability for Ackroyd) measure MC
state in isolation, while **Dramatica's Resolve axis is
specifically about the MC's response to the Impact Character's
influence** — a relational property of the MC and IC throughlines,
not a property of MC state alone.

This sketch commits an **additive IC-relational signal** to each
DSP_resolve check. The existing MC-state proxies are preserved
(they're not wrong; they just don't cover the full Dramatica
definition). The new signal reads the IC throughline's lowered
events and reports whether they temporally correlate with the MC's
state behavior (for Change: transitions follow IC pressure; for
Steadfast: MC state holds through IC pressure).

**First sketch addressing a cross-corpus pattern.** The previous
five sketches each closed a single encoding's qualification; this
one closes four encodings' qualifications at once because the
probe's second pass revealed an architectural-level gap the per-
encoding view missed.

Sixth concrete probe → sketch cycle in two days.

## What the probe proposed (v2 synthesis)

Four independent qualifications at DSP_resolve, converging on the
same axis:

**Rocky (Steadfast)**: *"The signature is narrow. An identity-
transition check would also pass for characters who change their
approach or drive without a substrate-level identity change."*
Suggested: *"checking whether the MC's problem-element or drive-
element persists unchanged across the arc's key τ_s boundaries."*

**Macbeth (Change)**: *"Dramatica's Resolve axis specifically
measures whether the MC changes in response to the IC's influence.
The tyrant-transition is a behavioral/moral transformation that
correlates with the IC's influence (Lady Macbeth goaded the
initial murder)."* Suggested: *"checking whether the MC's
trajectory inflection points correlate temporally with IC-
throughline events."*

**Oedipus (Change)**: *"Dramatica's 'Change' resolve specifically
means the MC abandons their paradigm and adopts (or is forced
into) the IC's perspective. Oedipus doesn't adopt Jocasta's 'don't
look' stance."* Suggested: *"checking whether the MC's post-
transition behavior exhibits alignment with the IC's counter-
premise."*

**Ackroyd (Steadfast)**: *"betrayer_of_trust is a world-state fact
derived from his action, not a direct measure of psychological
resolve."* Suggested: *"supplementing the world-state stability
check with a negative-event check: confirm no event exists in the
MC throughline where the MC voluntarily initiates a change of
approach before external compulsion."*

Common thread: **Resolve is relational (MC↔IC), not monadic
(MC-only).** The existing checks need an IC-side signal.

## What this sketch commits to

- A **temporal IC-correlation check**: for each encoding, find
  the IC throughline's lowered events; compare their τ_s
  distribution to the MC's critical moments (transition τ_s for
  Change; pressure moments for Steadfast). Report whether the
  correlation is structurally present.
- **Additive, not replacing.** The existing MC-state checks
  (identity-transition, rule-emergence, world-state stability)
  remain as the primary signal. The IC-correlation signal is
  reported alongside, enriching the verdict's substrate
  grounding.
- **Per-encoding per-axis parameterization.** Each encoding's
  DSP_resolve check names its own IC throughline id (`T_impact_
  jocasta`, `T_impact_lady_macbeth`, `T_ic_poirot`, `T_ic_apollo`)
  and its own critical τ_s. The shared helper detects temporal
  correlation given those inputs.
- Zero substrate changes. IC throughlines, their Lowerings, and
  event τ_s are all already substrate-visible. The check reads
  fold-visible structure.
- Verdict polarity unlikely to change across corpus. All four
  encodings' current DSP_resolve verdicts are APPROVED; adding
  IC-correlation is expected to **preserve** APPROVED for all
  four (IC events are temporally correlated in all four) while
  **enriching the verdict comments** with the relational signal.

## What this sketch does NOT commit to

- **A strict "IC-paradigm-adoption" check for Change
  encodings.** The probe's Oedipus qualification raised the
  paradigm-adoption question (does the MC adopt the IC's
  counter-premise?); adopting that test strictly would weaken
  Oedipus's Change verdict (Oedipus doesn't adopt Jocasta's
  "don't look"). The sketch deliberately stops at temporal
  correlation and banks paradigm-adoption as OQ1.
- **A generalization to DSP_growth or other axes.** The
  relational pattern could plausibly apply to DSP_growth as
  well, but the v2 probe didn't surface that as a coherent
  pattern. Scope stays at DSP_resolve.
- **Changing existing checks' verdict logic.** The four
  DSP_resolve checks' verdict thresholds and proxy-signal
  computations are preserved; the IC-correlation signal is
  reported as additional information in the verdict comment.
- **Probability-weighting or confidence scoring.** The
  correlation signal is binary (correlation present / absent
  within window) with an optional numeric gap. More
  sophisticated models (Bayesian, correlation coefficient) are
  not needed for the current corpus.

## Commitments

### RR1 — Classifier reads fold-visible structure

Parallel to EK1 / LT1 / AG1 / IG1 / MN1 / BW1. The IC-correlation
predicate is a function of the IC throughline's lowered events
(via existing `_events_lowered_from_throughline` helpers) and
their τ_s values. No new fields, no role-name dispatch.

### RR2 — Temporal correlation window predicate

Given a target τ_s (MC critical moment) and a list of IC event
τ_s values, the predicate asks: does any IC event's τ_s fall
within `[target_τ_s − window, target_τ_s]`? The default window is
5 τ_s ticks — tunable per encoding if the story's time-base
warrants.

Returns `(has_correlation: bool, nearest_preceding_ic_τ:
Optional[int], gap: Optional[int])`. The gap is `target_τ − nearest
IC τ` when correlation fires; the absolute gap supports downstream
strength calibration.

### RR3 — Per-encoding DSP_resolve check enrichment

Each encoding's `dsp_resolve_*_trajectory_check` is extended to:

1. Compute its existing MC-state signal (unchanged).
2. Fetch IC throughline events via existing `_events_lowered_
   from_throughline` helper.
3. Apply RR2's correlation predicate:
   - For **Change** encodings (Oedipus, Macbeth): correlation
     target is the MC's identity-transition / rule-emergence τ_s
     (the inflection). Fires when an IC event precedes within
     window.
   - For **Steadfast** encodings (Ackroyd, Rocky): correlation
     target is EACH IC event's τ_s. For each IC event, check
     that MC's state (equivalence class, derived compounds)
     doesn't change in a following window. Report the
     "resistance count" — N of M IC pressure events the MC held
     through.
4. Enrich the verdict comment with the IC-correlation summary.
5. Strength: bumped to 1.0 when full correlation is present;
   unchanged otherwise.

### RR4 — Shared helper in `verifier_helpers.py`

`detect_preceding_ic_event(target_τ, ic_event_τs, window=5) ->
dict` returns:

- `has_correlation: bool`
- `nearest_preceding_ic_τ: Optional[int]` — latest IC τ_s in the
  window
- `gap: Optional[int]` — positive integer τ_s distance if
  correlated
- `ic_events_in_window: list[int]` — all IC τ_s values within the
  window

Parallel to `classify_event_manipulation_shape` and
`classify_event_agency_shape`. Verifier-local.

### RR5 — Per-encoding IC throughline identification

Each encoding hard-codes its IC throughline id:
- Oedipus: `T_impact_jocasta`
- Macbeth: `T_impact_lady_macbeth`
- Ackroyd: `T_ic_poirot`
- Rocky: `T_ic_apollo`

The per-encoding check reads this id and passes it to
`_events_lowered_from_throughline`. No central registry needed;
encoding-local declaration matches the existing pattern for MC
throughline ids.

### RR6 — The resolve-relational frame is verifier-local

Parallel to EK5 / LT6 / AG6 / IG5 / MN5 / BW5. The IC-correlation
signal is a property of the DSP_resolve check, not a substrate
commitment. The substrate exposes throughline Lowerings and event
τ_s uniformly; reading them for Resolve-axis relational meaning is
the verifier's concern.

## Worked case — Macbeth (Change, expected APPROVED 1.0)

MC critical τ_s: tyrant-transition derives when `killed(macbeth,
duncan)` + `king(duncan)` + `king(macbeth)` premises all hold —
landing approximately τ_s=6 (E_macbeth_crowned), per the existing
check's reading.

IC throughline `T_impact_lady_macbeth`'s lowered events:
- E_letter_to_lady_macbeth (τ_s=-2): LM receives the letter
  declaring Macbeth's thane promotion
- E_plot_duncan's_visit (τ_s=3): LM and Macbeth plot Duncan's
  killing — LM is the primary goader
- Further LM events through the arc: banquet reprimand, sleepwalking,
  suicide

Window check against tyrant-transition τ_s=6:
- E_plot at τ_s=3 falls in [6-5, 6] = [1, 6]. **Correlation
  fires**; nearest_preceding_ic_τ=3, gap=3.

**Predicted verdict: APPROVED 1.0** (unchanged polarity and
strength), with enriched comment — the tyrant-transition follows
LM's goading within 3 τ_s, structural evidence that Macbeth's
Change response is IC-correlated per Dramatica's Resolve=Change
definition.

## Worked case — Oedipus (Change, expected APPROVED 1.0 with OQ)

MC critical τ_s: anagnorisis at τ_s=13.

IC throughline `T_impact_jocasta`'s lowered events:
- E_jocasta_mentions_crossroads (τ_s=5)
- E_jocasta_realizes (τ_s=9) — IC's own recognition
- E_jocasta_hangs (τ_s=~11) — IC's climactic act

Window check against anagnorisis τ_s=13 (window=5 → [8, 13]):
- E_jocasta_realizes (τ_s=9) in window ✓
- E_jocasta_hangs (τ_s=~11) in window ✓
- **Correlation fires**; gap=2-4.

**Predicted verdict: APPROVED 1.0**. OQ1 notes the separate
question of whether Oedipus adopts Jocasta's paradigm (he doesn't,
per the probe) — that's a stricter check left for a future
sketch.

## Worked case — Ackroyd (Steadfast, resistance-count)

Ackroyd's DSP_resolve=Steadfast. No MC critical τ_s (no transition
by definition). IC throughline `T_ic_poirot`'s lowered events
represent investigation pressure moments.

Poirot's events: E_poirot_arrives (τ_s=2), E_poirot_investigates
(τ_s=4), E_poirot_confronts (τ_s=6), E_poirot_reveals_solution
(τ_s=8), each a pressure moment.

For each pressure τ_s, the check asks: does the MC (Sheppard)
state change in a following window? `betrayer_of_trust` derives at
τ_s=1 and holds through — no change. Resistance count: 4/4.

**Predicted verdict: APPROVED 1.0** — Sheppard holds his
concealment through all four IC pressure moments until external
compulsion at the reveal.

## Worked case — Rocky (Steadfast, resistance-count)

Rocky's DSP_resolve=Steadfast. No MC identity transitions. IC
throughline `T_ic_apollo`'s events: E_apollo_schedules_mac,
E_apollo_selects_rocky, E_apollo_announces, E_round_one_knockdown,
E_no_rematch.

For each IC pressure τ_s, check if Rocky's articulated_goal
(`went_the_distance`) stability is preserved. It doesn't get
dislodged at any IC event. Resistance count: N/N.

**Predicted verdict: APPROVED 1.0** — Rocky's resolve holds
through Apollo's successive pressures (dismissal, knockdown,
refusal of rematch). Honest signal: Steadfast via sustained
resistance, not just absence of transition.

## Implementation brief

1. **Add `detect_preceding_ic_event` to `verifier_helpers.py`** per
   RR4.
2. **Refactor four DSP_resolve checks** (Oedipus / Macbeth /
   Ackroyd / Rocky) to call the helper with their IC throughline
   id and MC critical τ_s(s).
3. **Enrich verdict comments** with IC-correlation summary
   (correlated/not-correlated; for Steadfast, resistance count).
4. **Add unit tests in `test_verification.py`:**
   - `detect_preceding_ic_event` correctness (synthetic
     fixtures).
   - Per-encoding integration pins: each DSP_resolve comment
     contains IC-correlation language; strength stays at 1.0.
5. **Update `design/README.md`** to register sketch-01 with
   cross-corpus-pattern framing; update item 4 with the v2
   follow-on.
6. **Update root `README.md`** with the sixth-cycle + cross-
   corpus-pattern note.

No substrate changes. No new dialect fields.

## Measurements prediction

- Oedipus DSP_resolve: APPROVED 1.0 → APPROVED 1.0 (IC-correlated
  via Jocasta's realize/hang preceding anagnorisis).
- Macbeth DSP_resolve: APPROVED 1.0 → APPROVED 1.0 (IC-correlated
  via LM's plot preceding tyrant-transition).
- Ackroyd DSP_resolve: APPROVED 1.0 → APPROVED 1.0 (resistance
  signal: Sheppard holds through all IC pressure moments).
- Rocky DSP_resolve: APPROVED 1.0 → APPROVED 1.0 (resistance
  signal: Rocky holds through Apollo's pressures).

**No verdict polarity change expected.** This is the second
sketch (after BW4) where honesty-about-measurement is the
deliverable. Difference from BW4: BW4 refined a single
encoding's strength downward; RR3 enriches four encodings'
comments with an IC-relational signal that was structurally
present but previously unreported.

## Discipline

- **The sketch is additive.** Existing checks still work; the
  IC signal is new context, not a replacement metric. This
  avoids destabilizing verified results while closing the
  probe's v2 observation.
- **Temporal correlation is a weak relational signal, by
  design.** Stronger relational checks (IC-premise-adoption,
  IC-trajectory-inflection-alignment, rule-derivability-at-IC-
  moment) are banked as OQs. RR2's window-based check is the
  honest minimum that closes the probe's v2 finding without
  over-reaching.
- **Cross-corpus patterns earn cross-corpus sketches.** The
  first five probe-driven sketches closed per-encoding signals;
  this one closes a pattern visible only across all four
  encodings. The meta-finding is as important as the sketch:
  **a re-probe after sketch-landings produced a sharper,
  architectural-level signal** than the first pass did.

## Open questions

1. **IC-paradigm-adoption check for Change.** The probe's
   Oedipus qualification explicitly raised this: does the MC
   actually adopt the IC's counter-premise, or merely undergo an
   IC-correlated transition? Adopting the strict test would
   sharpen the Change verdict; Oedipus might flip to PARTIAL
   under it (Oedipus doesn't adopt Jocasta's "don't look"). A
   future sketch could add an IC-premise-enactment predicate.
2. **Non-temporal correlation.** The IC-correlation window is
   purely τ_s-based. A future refinement could ask: is there a
   knowledge-flow from IC to MC (KnowledgeEffect whose agent is
   MC and whose held matches an IC-introduced prop)? That's a
   stronger relational predicate than mere τ_s adjacency.
3. **Drive-element / problem-element persistence.** The Rocky
   probe specifically asked for checking whether the MC's
   drive-element persists across arc boundaries, not just
   identity-classes. The Dramatic dialect has concepts of drive
   / problem / solution elements (dramatica-complete template's
   CharacterElementAssignments). Checking drive-element
   persistence requires machinery that reads those elements
   against the arc's event flow. Deferred.
4. **Steadfast under zero IC events.** An encoding with no IC
   throughline events would leave the resistance count
   undefined. Current corpus has IC events in all four
   encodings; not a forcing function.
5. **Generalization to DSP_growth relational.** DSP_growth might
   have an analogous relational dimension (MC growth correlated
   with OS pressure, say). V2 probe did not surface this
   coherently; not pursued now.

## Summary

- All four encodings' DSP_resolve checks enriched with an
  IC-relational temporal-correlation signal per RR1-RR6.
- Closes the cross-corpus coherent finding from the 2026-04-17
  v2 probe pass: Resolve-axis is MC↔IC relational, not MC-only.
- Verdict polarity unchanged across corpus (all four stay
  APPROVED 1.0); comment grounding enriched with the IC signal.
- Sixth concrete probe → sketch cycle in two days. First sketch
  to close a cross-corpus pattern (prior five closed per-
  encoding signals).
- Zero substrate changes. The helper is a small `verifier_
  helpers.py` addition; each DSP_resolve check picks up the
  enrichment via ~10 lines of per-encoding call.
