# Beat-weight taxonomy — sketch 01

**Status:** draft, active
**Date:** 2026-04-17
**Supersedes:** nothing (new topic; parallel to [event-kind-taxonomy-sketch-01](event-kind-taxonomy-sketch-01.md), [event-agency-taxonomy-sketch-01](event-agency-taxonomy-sketch-01.md), [event-manipulation-taxonomy-sketch-01](event-manipulation-taxonomy-sketch-01.md), [identification-goal-sketch-01](identification-goal-sketch-01.md), [pressure-shape-taxonomy-sketch-01](pressure-shape-taxonomy-sketch-01.md))
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [architecture-sketch-02.md](architecture-sketch-02.md), [verification-sketch-01.md](verification-sketch-01.md), [dramatic-sketch-01.md](dramatic-sketch-01.md), [reader-model-sketch-01.md](reader-model-sketch-01.md)
**Related:** `macbeth_dramatica_complete_verification.py` (DA_mc check); Macbeth cross-boundary probe qualification on DA_mc (`reader_model_macbeth_dramatica_complete_output.json`, committed 2026-04-17 at `faaebd8`)
**Superseded by:** nothing yet

## Purpose

Close the Macbeth cross-boundary reader-model probe's DA_mc
qualification (PARTIAL 0.69). The probe named a subtle but
important calibration gap: the existing DA_mc check treats all MC-
Throughline events as equally weighted, but **the non-Activity
events in Macbeth's arc are its most dramatically significant
moments** (the inciting prophecy, the doubling-down prophecy, the
midpoint banquet ghost) — structural weight and narrative weight
diverge. The probe observed: *"The 31% non-Activity signal carries
disproportionate narrative weight relative to its event count. The
partial-match verdict is correct; the 0.69 strength may even be
generous."*

Important framing: **this is the first probe proposal in the
four-cycle sequence (LT9 / AG5 / IG2 / MN4) that does NOT flip a
verdict.** It refines the measurement toward honesty. Macbeth's
DA_mc likely stays PARTIAL under BW-weighting; the strength may
*drop*. The sketch commits to that honest calibration.

Fifth concrete probe → sketch → measurement-shift cycle in two
days (though the shift here is strength-refinement, not a verdict
lift). Closes the last banked probe proposal from the four-encoding
Template-surface spectrum.

## What the probe proposed

From `reader_model_macbeth_dramatica_complete_output.json`,
verifier_commentaries entry for `dramatica-complete:DA_mc`
(assessment: qualifies):

> "The partial-match at 0.69 correctly flags that the Activity
> domain is not clean. However, the non-Activity MC events
> (E_prophecy_first, E_prophecy_second as prophecy_received;
> E_banquet_ghost as apparition) are not incidental — they are
> among the MC throughline's most dramatically significant moments
> (the inciting prophecy, the doubling-down prophecy, the midpoint
> ghost). The 31% non-Activity signal carries disproportionate
> narrative weight relative to its event count. The partial-match
> verdict is correct; the 0.69 strength may even be generous."

And `suggested_signature`:

> "Consider weighting events by beat_type significance (inciting,
> midpoint, climax carry more signal than rising-action beats)
> when computing domain-flavor percentages, rather than treating
> all throughline events equally."

## What this sketch commits to

- A **beat-type weight vocabulary** with five canonical levels
  matching Macbeth's Dramatic-dialect beat_type values:
  `inciting`, `rising`, `midpoint`, `climax`, `denouement`.
  Structural-narrative weight differs: inciting / midpoint /
  climax carry ~2× the signal of rising-action beats; denouement
  sits between.
- A **weighted DA_mc Activity check** for Macbeth: instead of
  counting `activity_events / total_events`, compute
  `sum(weight(beat_type(e)) for e in activity_events) /
  sum(weight(beat_type(e)) for e in all_events)`. The ratio is
  the weighted Activity fraction.
- An **event → beat_type resolver** that chains substrate event →
  realizing Scene (via Lowerings) → Scene.advances for the MC
  Throughline → Beat → beat_type. Handles events with no
  resolving beat_type by defaulting to baseline weight (1.0 —
  treated as rising-action).
- Zero substrate changes. Beat and Scene records already exist
  in `dramatic.py`; beat_type is already an author-declared
  string; Lowerings already bind Scenes to events. The
  weighting reads fold-visible structure per LT1 / EK1 / AG1 /
  IG1 / MN1.
- Macbeth-only wiring (parallel to MN4's Ackroyd-only wiring).
  Not forced across all four encodings' DA_mc checks — each
  encoding's check composes whichever classifiers / weightings
  earn their keep for that encoding's substrate.

## What this sketch does NOT commit to

- **A forced refactor of Oedipus / Ackroyd / Rocky DA_mc checks.**
  Oedipus uses EK2 cleanly (4-of-4 APPROVED under Activity-domain
  classification); Ackroyd now uses MN4 (knowledge-asymmetry);
  Rocky uses EK2. None of them surfaced the weight-disparity
  signal the Macbeth probe did — beat-weighting can be wired later
  if a probe run on one of those encodings flags the same
  calibration issue. BW is opt-in per encoding.
- **A guarantee that Macbeth's DA_mc will remain APPROVED or flip
  APPROVED.** The probe explicitly said "the 0.69 strength may even
  be generous" — the weighted ratio may drop below 0.69, possibly
  below 0.4. The sketch commits to adopting the calibration, not
  to any specific post-measurement verdict. **This is the first
  landed probe proposal where honesty-about-measurement is the
  primary goal; verdict change is incidental.**
- **A canonical weight table for all dialects.** The five
  beat_type weights (inciting=2.0, rising=1.0, midpoint=2.0,
  climax=2.0, denouement=1.5) are a starting-point vocabulary
  tuned to Macbeth's Dramatic-dialect beats. Save the Cat's 15
  beats would need a different table (BS1 "opening image" = 1.0;
  "all is lost" = 2.0; "finale" = 2.5; etc.) — deferred to a
  future sketch if Save the Cat's verifier grows beat-weighted
  checks.
- **Arbitrary-granularity weight precision.** The five canonical
  weights are coarse. A future refinement could tune per-story
  (e.g., Macbeth's specific inciting prophecy gets weight 2.5
  instead of 2.0 because it's *especially* load-bearing). Not
  pursued; author-supplied per-beat weights risk A3 violation
  (schema-for-the-verifier's-convenience).

## Commitments

### BW1 — Verifier classification reads fold-visible structure

Parallel to EK1 / LT1 / AG1 / IG1 / MN1. The weight applied to an
event is a function of the event's realizing Scene (via Lowerings)
and that Scene's MC-Throughline Beat's `beat_type` value. All data
reads from existing records; no new fields, no new substrate
commitments.

### BW2 — Canonical beat-type weight vocabulary

Five weights keyed by the canonical Dramatic-dialect beat_type
values:

| beat_type | weight | rationale |
|---|---|---|
| `inciting` | 2.0 | the arc's structural starting bell — where the story's problem is posed |
| `rising` | 1.0 | the baseline; rising-action beats provide texture between pivots |
| `midpoint` | 2.0 | the arc's structural pivot — often reversal or realization |
| `climax` | 2.0 | the arc's structural resolution point |
| `denouement` | 1.5 | consequence-unpacking after the climax; weight between rising and climax |

Unknown or missing beat_type values default to 1.0 (rising-action
baseline). Per-story authors may use alternative beat_type strings;
the weight table treats unknowns conservatively rather than
rejecting them.

The weights are **verifier-local** (parallel to EK5 / LT6 / AG6 /
IG5 / MN5). The values are not substrate commitments; they are
tuning parameters in the classifier. They can be adjusted without
touching any encoding.

### BW3 — Event → beat_type resolver

An event's beat_type (for a specified throughline) is resolved
via:

1. Find the Scene-level Lowering whose `lower_records` include
   this substrate event and whose `upper_record` is a Scene in
   the Dramatic dialect.
2. Look up the Scene's `advances` tuple; find the advance entry
   matching the target `throughline_id`.
3. Look up that advance's `beat_id` in the Dramatic dialect's
   Beats tuple; return its `beat_type`.
4. If any step returns no match, return `None` (caller uses
   baseline weight 1.0).

A helper `event_to_beat_type(event_id, throughline_id, lowerings,
scenes, beats) -> Optional[str]` implements this chain.

### BW4 — Macbeth DA_mc check uses weighted ratio

`mc_throughline_activity_domain_check` in
`macbeth_dramatica_complete_verification.py`:

- For each event in the MC-Throughline event set, compute its
  beat-type weight via BW3 (default 1.0 for unresolvable).
- Classify each event as Activity-shaped per EK2.
- Compute `weighted_activity = sum(weight × is_activity)` and
  `weighted_total = sum(weight)`.
- Ratio: `weighted_activity / weighted_total`.
- Apply existing thresholds (≥0.7 → APPROVED; ≥0.4 → PARTIAL;
  else NEEDS_WORK).
- Report both the raw count and the weighted ratio in the
  verdict comment so the refinement is inspectable.

Other encodings' DA_mc checks are **not** modified.

### BW5 — The beat-weighting frame is verifier-local

Parallel to EK5 / LT6 / AG6 / IG5 / MN5. BW2's weight table is a
property of the Macbeth DA_mc check. Other dialects / encodings
may define their own weight vocabularies, or may not weight at
all.

## Worked case — Macbeth under BW4

Macbeth's 13 MC-Throughline events, with realizing Scene and
beat_type for T_mc_macbeth:

Predicted decomposition (requires chase through Lowerings + Scene
advances; implementation pass produces measurement):

- Activity events at `rising` beat_type (weight 1.0): most of the
  killing sequence (Duncan's murder, Banquo's killing, Macduff's
  family, Macbeth's combat / death).
- Activity events at `climax` / `denouement` (weight 2.0 / 1.5):
  late-arc Macbeth actions — Macbeth killed, Malcolm crowned.
- Non-Activity events at `inciting` (weight 2.0): the first
  prophecy (`E_prophecy_first`) — the story's structural starting
  bell is a prophecy-received event, not an action.
- Non-Activity events at `midpoint` (weight 2.0): the banquet
  ghost (`E_banquet_ghost`) — the arc's pivot is an apparition,
  not an action.
- Non-Activity events at `rising` (weight 1.0): the second
  prophecy (`E_prophecy_second`) if classified as rising-action;
  may also be climax-ish.

Under weighted arithmetic, the three heavy non-Activity beats
(inciting + midpoint + possibly climax) contribute ~4.0–6.0 to
non-Activity weighted total, while the lighter non-Activity rising
events contribute ~1.0. Activity events at rising beats dominate
the Activity weighted total but not by the 9/13 ratio — probably
closer to 7.0/11.0 or similar.

**Predicted weighted ratio: 0.55–0.65**, below the unweighted 0.69
— validating the probe's "may even be generous" observation.
Verdict: stays PARTIAL (above the 0.4 threshold), but the strength
honestly reflects the non-Activity events' disproportionate weight.

If the measurement comes out lower than predicted (e.g., 0.45),
that's an honest downward shift; if it stays around 0.69, the
weighting was near-neutral for Macbeth's specific distribution.
Either outcome is informative.

## Worked case — Oedipus / Ackroyd / Rocky (no-regression)

Not modified by this sketch. Oedipus's EK2-based DA_mc stays
APPROVED 0.77; Ackroyd's MN4-based DA_mc stays APPROVED 0.85;
Rocky's EK2-based DA_mc stays APPROVED 0.72.

## Implementation brief

1. **Add `beat_type_weight` and `event_to_beat_type` to
   `verifier_helpers.py`.** The weight function is a small dict
   lookup; the resolver walks Lowerings + Scene.advances + Beats.
2. **Refactor
   `mc_throughline_activity_domain_check` in
   `macbeth_dramatica_complete_verification.py`** to use the
   weighted ratio per BW4. Message reports raw and weighted
   numbers.
3. **Add unit tests in `test_verification.py`:**
   - `beat_type_weight` table returns canonical values and
     defaults to 1.0 for unknown strings.
   - `event_to_beat_type` on a fixture where a Scene advances an
     MC beat — returns the right beat_type.
   - Integration pin: Macbeth DA_mc weighted ratio differs from
     unweighted 0.69 (direction: down, by the probe's prediction;
     exact value captured at measurement time).
   - No-regression: Oedipus / Ackroyd / Rocky DA_mc verdicts
     unchanged.
4. **Update `design/README.md`** to register sketch-01; promote
   the Macbeth DA_mc qualification from "banked" to "landed".
5. **Update root `README.md`** with the five-landing count — all
   four probe qualifications/dissents now adopted; the
   probe/verifier loop has closed every banked signature.

## Measurements prediction

- Macbeth DA_mc: PARTIAL 0.69 → **PARTIAL with weighted strength,
  expected ~0.55–0.65** (likely still PARTIAL, but honestly
  calibrated). Exact value at measurement time.
- Oedipus DA_mc: APPROVED 0.77 (unchanged; EK2).
- Ackroyd DA_mc: APPROVED 0.85 (unchanged; MN4).
- Rocky DA_mc: APPROVED 0.72 (unchanged; EK2).

**First landed probe proposal that does not flip a verdict.** The
value is in honesty-about-measurement — the probe said the
unweighted 0.69 was generous; the weighted measurement validates
that observation.

## Discipline

- **Honesty is a first-class landing.** Not every probe proposal
  should flip a verdict. Sometimes the probe is calibrating the
  measurement's relationship to narrative reality. BW-weighting
  is that kind of landing; the verdict may not change polarity
  but the strength carries more meaning.
- **Weight-tuning is verifier territory, not substrate
  territory.** Per EK5 / LT6 / AG6 / IG5 / MN5, the weight
  vocabulary is verifier-local. A future tuning pass could
  adjust the specific weights (inciting=2.5 instead of 2.0) based
  on accumulated signal across encodings — this is a calibration
  concern, not a commitment concern.
- **BW's weight table is not a narrative-theory claim.** The
  five weights are practical tuning values matching the Dramatic
  dialect's common beat_type vocabulary. They are not a
  rediscovered universal about which beats matter more; they are
  a weighting scheme that happens to help the verifier read
  Macbeth's signal more honestly.

## Open questions

1. **Save the Cat 15-beat weighting.** The Save the Cat dialect
   has a different beat taxonomy (opening image, debate, midpoint,
   all is lost, finale, final image, etc.). A parallel sketch for
   Save the Cat's DA_mc or equivalent checks would need its own
   weight table. Banking.

2. **Auto-derived weights from probe signal.** An LLM probe
   could be asked per-encoding which beats feel load-bearing and
   translate that into per-story weights. This would eliminate
   the hand-tuned vocabulary in favor of author-probed tuning.
   Interesting, probably premature.

3. **Cross-check weighted vs. unweighted.** The verifier could
   report both numbers systematically — "unweighted 0.69,
   weighted 0.58" — letting the author see the weighting's
   effect on every check. Consider adding as a comment convention.

4. **Generalization to non-DA checks.** DSP_approach, DSP_growth,
   Story_goal trajectories could all be weight-tunable. Not
   pursued here; wire case-by-case as probe signal argues.

5. **Per-story beat-type overrides.** An encoding author might
   declare `B_banquet_ghost.is_load_bearing=True` to promote it
   beyond its beat_type weight. Currently rejected as A3
   schema-for-verifier-convenience. Could revisit if multiple
   encodings surface edge cases.

## Summary

- Macbeth DA_mc qualification closed by adopting beat-type-
  weighted ratio computation. Weight vocabulary: inciting=2.0,
  rising=1.0, midpoint=2.0, climax=2.0, denouement=1.5.
- Macbeth-only wiring (parallel to MN4's Ackroyd-only wiring).
- Predicted measurement shift: ~0.69 → ~0.55–0.65 (down).
  **First landed probe proposal where verdict polarity does not
  change** — honesty-about-measurement is the deliverable.
- Zero substrate changes; Beat / Scene / Lowering records already
  provide everything the weight resolver needs.
- Fifth concrete probe → sketch cycle in two days. Closes the
  last banked probe proposal from the four-encoding Template-
  surface spectrum (LT9 + AG5 + IG2 + MN4 + BW).
