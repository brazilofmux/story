# Pressure-shape taxonomy — sketch 02

**Status:** draft, active
**Date:** 2026-04-17
**Supersedes:** nothing (amendment to [pressure-shape-taxonomy-sketch-01](pressure-shape-taxonomy-sketch-01.md); extends LT1–LT6 without retouching them)
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [architecture-sketch-02.md](architecture-sketch-02.md), [substrate-sketch-05.md](substrate-sketch-05.md), [verification-sketch-01.md](verification-sketch-01.md), [reader-model-sketch-01.md](reader-model-sketch-01.md)
**Related:** `verifier_helpers.py` (`classify_arc_limit_shape`, `dsp_limit_characterization_check`), `rocky.py`, `rocky_dramatica_complete.py`, `rocky_dramatica_complete_verification.py`, Rocky cross-boundary probe output (`reader_model_rocky_dramatic_output.json`, committed 2026-04-17 at `a0f9bcf`)
**Superseded by:** nothing yet

## Purpose

Close LT3's asymmetry per the concrete signature proposal returned by
the cross-boundary reader-model probe's run against Rocky's
dramatica-complete verifier output. Sketch-01 committed LT3 as
explicitly weak (complement-only) with a stated asymmetry: the
Timelock predicate could not affirmatively detect scheduling because
substrate-05 lacked scheduling vocabulary. The probe run (2026-04-17)
dissented with Rocky's NEEDS_WORK 0.33 verdict on DSP_limit and
proposed a positive predicate the substrate can already evaluate —
turning LT3's deferred OQ1/OQ3 into a concrete implementation target.

This is that landing.

Amendment, not supersession. Sketch-01's LT1–LT6 stand. LT7–LT11
extend them with the new verifier vocabulary.

## What the probe proposed

From `reader_model_rocky_dramatic_output.json`, verifier_commentaries
entry for `dramatica-complete:DSP_limit` (assessment: dissents):

> "The Timelock assignment is well-supported by the narrative and
> substrate structure. The fight is scheduled at a fixed date
> (E_apollo_schedules_mac establishes the temporal frame); the entire
> training arc (τ_s=10–25) is explicitly deadline-driven preparation;
> the fight itself is fifteen rounds — a temporal limit. The
> 'convergence shape' the check detects (retraction:1 from Mac's
> injury removing him; rule-emergence:1 from WENT_THE_DISTANCE_RULE)
> are not Optionlock signatures — they are setup mechanics and
> consequence derivations, respectively. Mac's injury doesn't remove
> an option from Rocky; it creates the temporal setup. The
> rule-emergence is a post-limit evaluation, not a limit mechanism."

And `suggested_signature`:

> "Consider adding a signature for scheduled temporal endpoints: when
> a scheduling-type event establishes a future date and the story's
> τ_s progression converges toward that date with training/preparation
> events filling the interval, this is a positive Timelock indicator.
> Also consider that the fight's round structure (fought_rounds=15 in
> the derivation rule) is itself a temporal-limit mechanism embedded
> in the climax."

Two distinct proposals. The sketch commits the first (scheduling
endpoint + arc-position weighting) and defers the second (bounded-
iteration rule detection) — see the *Not committing* list.

## What this sketch commits to

- Arc-position classification for LT2 signals (pre-plot /
  middle-arc / terminal), so the classifier can distinguish
  **arc-converging** signals (the Optionlock evidence sketch-01
  LT2 was written for) from **arc-peripheral** signals (setup
  retractions and scheduled-event payoffs that happen to look
  like convergence).
- A scheduling-predicate recognition rule (LT8) that detects
  Timelock structurally via a verifier-local naming convention
  (predicates beginning `scheduled_`). Zero substrate changes; no
  new effect kind; no new descriptions kind.
- A positive Timelock predicate (LT9) composing LT8 with the
  arc-position breakdown: Timelock-strong requires both a
  scheduling predicate in vocabulary AND an empty middle-arc
  convergence count.
- A revised disposition table (LT10) that makes LT9's strong
  predicate first-class: Timelock declared + LT9 strong →
  APPROVED with strength tied to LT8's signal count. Preserves
  LT5 — author declaration never silently overridden.

## What this sketch does NOT commit to

- **Bounded-iteration rule detection** (the probe's second
  proposal — treating `fought_rounds=15` as a temporal-limit
  signal baked into a derivation rule). Rejected at this pass.
  Rule-body inspection for numeric bounds is too fragile without
  substrate-06 structural scheduling primitives: a rule whose
  body contains an integer literal is not structurally different
  from one that does not, and the "temporal-limit mechanism"
  reading of `fought_rounds=15` is interpretive. The probe's
  dissent lands fully on LT9 alone; the bounded-iteration reading
  is banked as OQ4 below.
- **Substrate-06 scheduling-effect primitives.** LT8 detects
  scheduling via predicate-name convention (`scheduled_*`), not
  via a dedicated substrate effect kind. This stays verifier-local
  per LT6 — the pressure-shape frame is a property of the verifier
  surface, not of the substrate. If future pressure-shape work
  demands a substrate commitment, substrate-06 is the right venue.
- **Changes to LT1–LT6.** All sketch-01 commitments remain. LT2's
  three-signal disjunction is unchanged; LT3's complement-only
  fallback is still the right verdict when LT9 does not fire and
  no middle-arc signals are present (i.e., the weak Timelock case
  from sketch-01 is now the LT9-fails fallback).
- **Retroactive re-reading of sketch-01 verdicts.** The three
  Optionlock encodings (Oedipus / Macbeth / Ackroyd) stay
  APPROVED 0.67 — none of them contain `scheduled_*` predicates,
  and their middle-arc LT2 signal counts are nonzero. LT9 applies
  only where it fires; the existing spectrum is additive, not
  overwritten.

## Commitments

### LT7 — Arc-position bands for LT2 signals

Each LT2 convergence signal event is classified into one of three
arc-position bands by its τ_s:

- **peripheral-pre**: signal-event τ_s < 0. Substrate convention —
  negative τ_s marks backstory / pre-plot events (Rocky's
  `E_apollo_schedules_mac` at τ_s=−10, `E_mac_injured` at τ_s=−5,
  `E_apollo_selects_rocky` at τ_s=−1 all predate the arc proper).
  Encodings that don't use negative τ_s have no peripheral-pre
  signals — LT7 reduces to sketch-01's flat count in that case,
  preserving LT11 back-compat.
- **terminal**: signal-event τ_s ≥ max_τ_s − 3 (the climax + closing
  beats). The 3-tick window is chosen as a simple default —
  captures Rocky's `E_fight_ends` at τ_s=55 as terminal against
  max_τ_s=57, while Macbeth's mid-arc killings at their declared
  τ_s values remain middle-arc.
- **middle-arc**: τ_s ≥ 0 AND τ_s < max_τ_s − 3.

For rule-emergence signals, the emergence τ_s is the maximum τ_s
across events that assert any body premise of the rule whose head
emerges. Rocky's `went_the_distance` emerges at τ_s=55 (both
premises `fought_rounds(...)` and `standing_at_final_bell(...)`
asserted at `E_fight_ends`); Macbeth's `kinslayer(macbeth, duncan)`
emerges at the killing event's τ_s. This is a minor extension to
the existing sketch-01 LT2 rule-emergence detection, which counted
emergences without localizing them.

### LT8 — Scheduling-predicate recognition

A `WorldEffect` whose `prop.predicate` begins with the string
`"scheduled_"` (underscore-prefix convention) is a **scheduling
signal**. The classifier reports the signal whether the effect
asserts (`asserts=True`) or retracts (`asserts=False`) — the
appearance of the predicate in the canonical-scope vocabulary is
the load-bearing evidence that the story frames itself around a
schedule.

Per LT6, `scheduled_*` is verifier-local naming, not a substrate
commitment. Encodings that want their scheduling visible to LT9
name their scheduled-endpoint predicates with the prefix. Rocky's
`scheduled_fight(apollo, mac)` (asserted at `E_apollo_schedules_mac`,
retracted at `E_mac_injured`) fires LT8 twice — or once, depending
on whether the count of distinct predicate instances or the count
of effect events is used. The reference implementation counts
distinct `Prop` values.

Per LT1, the predicate name is a heuristic, not the sole classifier
input. A future refinement could require the scheduled predicate's
args to reference entities that also appear in the terminal event's
participants — strengthening the scheduling-to-terminal coupling.
Deferred as OQ1 here; not necessary for the current three-encoding
signal.

### LT9 — Strong Timelock predicate

An arc is **Timelock-shape-strongly-detected** if and only if:

1. At least one LT8 signal fires (scheduling-predicate present in
   canonical-scope fabula), AND
2. The middle-arc LT2 signal count (per LT7 banding) is **zero**
   (the arc's body is convergence-free).

Both conditions are required. A scheduling predicate without a
clean middle (e.g., a story that announces a fight on the calendar
AND retracts several world-facts mid-arc) is not LT9-strong —
that mixed signature is Dramatica-authorial territory (is this
Timelock with a subplot, or genuine Optionlock with a false-lead
scheduling reference?) and the check reports it honestly as
PARTIAL rather than APPROVED.

Sketch-01's LT3 (complement-only Timelock-consistent) remains the
fallback when LT8 does not fire and no middle-arc signals are
present. LT9 and LT3 are distinct verdicts:

- LT9 strong → APPROVED (affirmative detection).
- LT3 weak → NOTED (consistent but unaffirmed; sketch-01's honest
  asymmetry, preserved).

### LT10 — Revised disposition table

Extends LT5 with the LT7/LT9 distinctions. The authoritative table:

| DSP_limit declared | Substrate shape | Verdict | Strength |
|---|---|---|---|
| Optionlock | middle-arc LT2 signals present | APPROVED | `min(1.0, middle_kinds / 3.0)` |
| Optionlock | only peripheral/terminal LT2 signals | PARTIAL_MATCH | `0.5 × (peripheral+terminal_kinds / 3.0)` |
| Optionlock | no LT2 signals at all | NEEDS_WORK | 0.0 |
| Timelock | LT9 strong (LT8 ≥ 1 + middle-arc LT2 = 0) | APPROVED | `min(1.0, lt8_count / 2.0)` |
| Timelock | LT8 signal + middle-arc LT2 signals present | PARTIAL_MATCH | `0.5 × (1.0 − min(1.0, middle_kinds/3.0))` |
| Timelock | no LT8 signal, no middle-arc LT2 signals (LT3 weak) | NOTED | 0.5 |
| Timelock | middle-arc LT2 signals, no LT8 signal | NEEDS_WORK | `1.0 − min(1.0, middle_kinds/3.0)` |
| Unknown choice | any | NOTED | — |

LT5 is preserved: the author's declaration is never silently
overridden. Every row is a verifier verdict on whether the
substrate's shape agrees with the declaration — the resolution
(edit DSP, edit substrate, accept partial) stays with the author.

### LT11 — Backward compatibility

Sketch-01's `classify_arc_limit_shape` return shape is preserved
verbatim — the 3-tuple `(classification, strength, signals)` with
`signals` carrying `"<kind>:<count>"` strings continues to work for
any caller that only wants sketch-01's semantics. Sketch-02 adds a
parallel helper (name: `classify_arc_limit_shape_strong`, or an
extended-return flag — implementation pass decides) that returns
the richer arc-position-banded structure. The shared
`dsp_limit_characterization_check` upgrades in place to use the
strong predicate; its four callers (one per dramatica-complete
verifier) pick up LT7–LT10 verdicts automatically.

Existing tests pinning sketch-01's flat signal format
(`signals == ("retraction:1",)`) still pass — they reference the
narrower helper, not the new one. The sketch-01 worked-case
measurements (Oedipus APPROVED 0.67, Macbeth APPROVED 0.67, Ackroyd
APPROVED 0.67) stay APPROVED because their middle-arc LT2 signal
counts are ≥ 1.

## Worked case — Rocky under LT9 (the load-bearing prediction)

Rocky's canonical-scope fabula, re-read under LT7–LT9:

### LT7 banding on Rocky's LT2 signals

- **Retraction (1)**: `scheduled_fight(apollo, mac)` retracted at
  `E_mac_injured`, τ_s=−5. Position: **peripheral-pre** (τ_s < 0).
- **Identity-resolution (0)**: no equivalence-class collapses —
  Rocky is Steadfast.
- **Rule-emergence (1)**: `went_the_distance(rocky, apollo)` derives
  at τ_s=55 (body premises `fought_rounds(rocky, apollo, 15)` and
  `standing_at_final_bell(rocky, fight)` both assert at
  `E_fight_ends`, max_τ_s=57, so 55 ≥ 57−3 = 54). Position:
  **terminal**.

Middle-arc LT2 signals: **0** (both signals land outside the
middle-arc band).

### LT8 on Rocky's substrate

Canonical-scope world-effects scanned for predicates beginning
`scheduled_`:

- `scheduled_fight(apollo, mac)` at `E_apollo_schedules_mac`
  (asserts=True, τ_s=−10).
- `scheduled_fight(apollo, mac)` at `E_mac_injured` (asserts=False,
  τ_s=−5).

LT8 signal count (by distinct Prop): **1** (`scheduled_fight(apollo, mac)`).
LT8 signal count (by event): **2**.

### LT9 evaluation

- LT8 ≥ 1: **yes**.
- middle-arc LT2 count = 0: **yes**.

→ **Timelock-shape-strongly-detected.**

### LT10 verdict on Rocky

- Declared: Timelock.
- Classification: Timelock-strong.
- Verdict: **APPROVED** with strength `min(1.0, 1 / 2.0) = 0.5`.
  (Using distinct-Prop count for LT8; strength floors at 0.5 for
  single scheduling predicate.)

**Net shift:** NEEDS_WORK 0.33 → **APPROVED 0.50**. Rocky's
declaration/substrate tension resolves into affirmative agreement;
the LT9 predicate captures exactly what the sketch-01 worked case
argued the substrate already encoded (the retraction being pre-plot
setup; the rule-emergence being terminal payoff). The probe's
reading is vindicated.

## Worked case — Oedipus / Macbeth / Ackroyd under LT7–LT9

Prediction: no change. The three Optionlock-declared encodings
continue to land APPROVED 0.67 because their middle-arc LT2 signal
counts are ≥ 1 (Macbeth's four rule-emergences span the arc;
Oedipus's identity-resolutions cluster around the anagnorisis, all
mid-arc; Ackroyd's retraction at the reveal is terminal-band but
the rule-emergences are mid-arc). None contain `scheduled_*`
predicates — LT8 doesn't fire. Sketch-01's verdicts stay intact.

Measured confirmation lands in the implementation pass, not at sketch
time. If any of the three encodings surprises (e.g., Ackroyd's sole
retraction being terminal AND no middle-arc signals reducing to LT3
weak instead of LT2 strong), the sketch needs a correction — noted
as OQ2 below.

## Worked case — Prospective Timelock encodings

Two Dramatica Timelock archetypes the sketch predicts would land
LT9-strong once their substrates are written:

- **Heist-under-deadline**: `scheduled_bank_opening(downtown_bank, τ_s=...)`
  or similar at the arc's start; the crew's prep operations fill
  the middle-arc without world-fact retractions. LT9 fires.
- **Ticking-bomb thriller**: `scheduled_detonation(device_a, τ_s=100)`
  at τ_s=0; defusal attempts may retract `armed(device_a)` but that
  retraction is terminal-band (the defusal is the climax). LT9 fires
  if the detonation-to-terminal coupling holds and the middle has no
  world-fact retractions outside the device's state.

A future Save-the-Cat verifier asking a pressure-shape question in
its own dialect vocabulary could compose LT8's scheduling-predicate
check without re-implementing it — LT4/LT6's verifier-local-helper
pattern applies.

## Implementation brief

Concrete change, in order of landing:

1. **Extend `verifier_helpers.py` with `classify_arc_limit_shape_strong`.**
   Signature roughly:
   ```python
   def classify_arc_limit_shape_strong(
       fabula, rules, canonical_branch, all_branches: dict,
   ) -> dict:
   ```
   Returns a dict with keys:
   - `classification`: `"optionlock"` / `"timelock-strong"` /
     `"timelock-consistent"` / `"undetermined"`.
   - `strength`: float [0.0, 1.0] per LT10.
   - `signals`: tuple of `"<kind>:<count>"` strings (back-compat
     with sketch-01).
   - `middle_arc_kinds`: count of LT2 signal kinds with at least
     one middle-arc event.
   - `peripheral_pre_count`: integer count of peripheral-pre events.
   - `terminal_count`: integer count of terminal-band events.
   - `middle_arc_count`: integer count of middle-arc events.
   - `scheduling_signals`: tuple of `"scheduled_<name>:<event_count>"`
     strings (one entry per distinct Prop).
   - `scheduling_count`: distinct-Prop count.
   - `arc_range`: `(min_τ_s, max_τ_s)` reported for diagnostics.

   The existing `classify_arc_limit_shape` stays, unchanged, per LT11.

2. **Update `dsp_limit_characterization_check`** to call the strong
   variant and apply LT10's disposition table. Messages embed the
   arc-position breakdown so the author can see *why* a verdict
   landed (e.g., "peripheral-pre retractions don't support
   Optionlock").

3. **New unit tests** in `test_verification.py`:
   - Arc-position banding: synthetic fabulae with signals at
     τ_s=−5, τ_s=5, τ_s=max − 1, τ_s=max.
   - LT8 predicate-name matching: fabulae with and without
     `scheduled_*` props.
   - LT9 composition: scheduling + clean middle → Timelock-strong;
     scheduling + middle signals → PARTIAL.
   - Integration pins for Rocky (APPROVED 0.5), Oedipus / Macbeth
     / Ackroyd (APPROVED 0.67).

4. **Update Rocky's verifier header docstring** to reflect the
   APPROVED verdict post-LT9 (removes the stale "first non-APPROVED
   DSP_limit in the corpus" claim; that claim held at sketch-01
   and stays in sketch-01's record but is now superseded as a
   measurement).

5. **Update `design/README.md`** to register sketch-02, update the
   pressure-shape-taxonomy-sketch-01 bullet with a link forward,
   update item 2 / item 4 findings with the new spectrum.

6. **Update root `README.md`** status bullet with the updated
   DSP_limit spectrum.

No substrate changes. No new event types. No dialect changes. The
change is localized to `verifier_helpers.py` and propagates through
the shared check helper to all four verifier modules.

## Measurements prediction

Post-LT9 DSP_limit spectrum (predicted):

| Encoding | DSP_limit declared | LT8 signal | Middle-arc LT2 | Classification | Verdict | Strength |
|---|---|---|---|---|---|---|
| Oedipus | Optionlock | 0 | ≥ 1 | optionlock | APPROVED | 0.67 |
| Macbeth | Optionlock | 0 | ≥ 1 | optionlock | APPROVED | 0.67 |
| Ackroyd | Optionlock | 0 | ≥ 1 | optionlock | APPROVED | 0.67 |
| **Rocky** | **Timelock** | **1** | **0** | **timelock-strong** | **APPROVED** | **0.50** |

**Net shift:** 3 APPROVED + 1 NEEDS_WORK → **4 APPROVED**, with
strength reflecting the three Optionlock encodings' uniformity
(0.67 each, two of three signal kinds) vs. Rocky's Timelock-strong
signature (0.50, one scheduling predicate). The four-point spectrum
of sketch-01 Phase 2 becomes a different four-point spectrum —
post-LT9 every declaration is affirmatively supported.

The sketch's **honest failure mode**, if the implementation pass
measures something else: Ackroyd's Optionlock verdict may weaken
if its retraction lands terminal and its rule-emergences are fewer
than expected. OQ2 tracks that case.

## Discipline

- **LT11 back-compat is load-bearing.** The existing
  `classify_arc_limit_shape` signature is what sketch-01's 25 tests
  pin. LT7–LT9 live in a parallel helper so the narrower function
  remains a well-formed sketch-01 reading. Future refinements
  (LT12+) may consolidate if a consolidation earns its keep.
- **LT8's naming convention is owned, not hidden.** The sketch
  commits to `scheduled_*` as verifier-local vocabulary. Encodings
  wanting Timelock detection name their scheduled predicates
  accordingly; this is a discipline statement, not an enforcement
  mechanism. Other conventions could be added (OQ3) without
  superseding LT8.
- **Arc-position bands are structural, not stylistic.** The
  `τ_s < 0 = pre-plot` rule is a substrate convention; the
  `τ_s ≥ max − 3 = terminal` rule is a classifier choice. A future
  encoding that encodes its entire backstory at positive τ_s would
  need LT7's pre-plot detector to look elsewhere (e.g., at the
  first MC-participation event). Deferred until pressured.
- **Composition with the reader-model probe is the loop.** The
  probe proposed LT9; the implementation tests whether the
  proposal holds. If it does (Rocky APPROVED), the probe has
  closed one of its dissents concretely — validating
  architecture-02 A11's "cross-boundary partner" framing. If it
  doesn't, the sketch gets revisited and the probe's signal
  remains a partial. Either outcome is information.

## Open questions

1. **Tightening LT8 via args-matching.** A scheduling predicate
   whose args reference only non-terminal entities is weaker
   evidence than one whose args match the terminal event's
   participants. Rocky's `scheduled_fight(apollo, mac)` references
   the original scheduled fighter (Mac), not the terminal-event's
   actual participants (Rocky / Apollo) — but the predicate is
   still the scheduling signal. Whether to require a stronger
   args-to-terminal coupling is banked for a future sketch pass.

2. **Ackroyd LT10 row sensitivity.** If Ackroyd's retraction is
   classified as terminal-band (the reveal is the climax) AND
   Ackroyd's rule-emergences are all computed at the reveal's τ_s
   (rather than at the earlier murder event's τ_s), Ackroyd's
   middle-arc signal count could be zero or one. The sketch
   predicts APPROVED 0.67 but the strength may shift to PARTIAL
   if the implementation pass measures otherwise. The correction,
   if it bites, is either (a) widen the middle-arc band, or
   (b) refine rule-emergence τ_s to use the earliest complete-body
   τ_s rather than the max. Not blocking landing.

3. **Alternate scheduling-signal conventions.** LT8's `scheduled_*`
   prefix works for Rocky because the encoding author chose that
   convention. Other encodings might use `deadline_*`, `clock_*`,
   `countdown_*`, or free-form. A canonical vocabulary list (v.
   regex) is deferred — the prefix is load-bearing for the first
   encoding, not for all encodings. If the prefix convention
   itself turns out too narrow after two or three Timelock
   encodings land, the fix is a small list of accepted prefixes,
   not a new sketch.

4. **Bounded-iteration rule detection** (the probe's second
   proposal, banked from the current sketch). A rule whose body
   contains a numeric-literal premise (`fought_rounds(rocky,
   apollo, 15)`) encodes a discrete temporal/iteration limit.
   Detecting this structurally would require substrate-06 or
   some rule-body metadata convention. Whether it is worth adding
   depends on whether a future Timelock encoding lacks a
   `scheduled_*` predicate but has a bounded-iteration rule — a
   case not yet in the corpus.

5. **Save-the-Cat pressure check composition.** A future
   Save-the-Cat verifier wanting a pressure-shape check could
   compose LT8's scheduling-predicate scan without re-implementing
   it. Whether the dialect-specific framing (e.g., "All Is Lost"
   beat pressure) maps onto LT9's clean-middle-arc requirement is
   unknown. Left open per LT6.

## Summary

- The Rocky cross-boundary probe's dissent on DSP_limit
  NEEDS_WORK 0.33 named a concrete positive Timelock signature.
  This sketch commits it.
- LT7 bands LT2 signals by arc position (peripheral-pre /
  middle-arc / terminal) to distinguish arc-converging from
  arc-peripheral convergence signals.
- LT8 detects scheduling via a verifier-local predicate-name
  convention (`scheduled_*`). Zero substrate changes.
- LT9 is the positive Timelock predicate: scheduling present +
  middle-arc empty. Fires on Rocky; does not fire on the three
  Optionlock encodings (they lack `scheduled_*` predicates).
- LT10 extends the disposition table with APPROVED for
  Timelock-strong detection. LT5 preserved — author declaration
  never silently overridden.
- LT11 keeps sketch-01's API intact; LT7–LT9 live in a parallel
  helper.
- Predicted measurement shift: Rocky NEEDS_WORK 0.33 → APPROVED
  0.50; three Optionlock encodings unchanged. Four-point spectrum
  becomes all-APPROVED with Rocky at a distinct strength point
  documenting its Timelock-strong signature composition.
- The probe / verifier partnership (architecture-02 A11,
  verification-01 OQ4) closes its first concrete loop: probe
  dissent proposes a signature; verifier adopts it; Rocky moves
  from disagreement to affirmative agreement. Whether the loop
  holds across encodings is the next observation.
