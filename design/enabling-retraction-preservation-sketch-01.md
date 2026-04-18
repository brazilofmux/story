# Enabling-retraction preservation — sketch 01

**Status:** draft, active (deferral)
**Date:** 2026-04-18
**Supersedes:** nothing
**Frames:** [pressure-shape-taxonomy-sketch-03](pressure-shape-taxonomy-sketch-03.md) (LT12), [scheduling-act-utterance-sketch-01](scheduling-act-utterance-sketch-01.md), [verification-sketch-01](verification-sketch-01.md)
**Related:** `verifier_helpers.py` (`classify_arc_limit_shape_strong`, `dsp_limit_characterization_check`), post-LT12 Rashomon probe output (`reader_model_rashomon_post_lt12_output.json`, samurai commentary `vr_3`, committed 2026-04-18 at `25a56f4`)
**Superseded by:** nothing yet

## Purpose

Close the fourth post-LT12 Rashomon probe finding (samurai testimony) on
its own terms — not by adding mechanism, but by naming precisely what's
already preserved, what's missing, and the criteria under which a
sketch-02 should commit durable surface.

This is a **deferral sketch**. It commits to *not* writing code in
response to the probe finding, and documents why, so a later session
doesn't re-discover the choice point.

## The finding

From `reader_model_rashomon_post_lt12_output.json`, samurai testimony
commentary (verdict: qualifies):

> "the bound_to retraction at τ_s=10 might merit a secondary
> annotation as 'enabling_condition_removed' distinct from
> 'convergence_signal' to preserve the information LT12 currently
> discards."

The probe endorses LT12's exclusion of the bound_to retraction from the
LT2 convergence count. It then proposes preserving the enabling-
retraction as a *named signal kind* distinct from "convergence signal,"
so the information isn't silently dropped.

The probe does not propose a specific downstream use for the preserved
signal. The argument is structural — "don't discard" — rather than
functional — "here's what would consume it."

## What is already preserved (current state)

LT12's implementation in `verifier_helpers.py` (sketch-03 landing at
commit `ada7e97`) already preserves enabling retractions:

- **Classifier output field `enabling_retractions`** — tuple of
  `(predicate_name, τ_s, reason)` tuples. `reason` is a typed code:
  `"constraint-vocabulary"` (LT12a match) or `"subject-reactivation"`
  (LT12b match).
- **Classifier output field `enabling_retraction_count`** — int,
  `len(enabling_retractions)`.
- **Verifier-comment surfacing in
  `dsp_limit_characterization_check`** — when `enabling_retractions`
  is non-empty, the comment string gains a clause of the shape "LT12
  excluded N enabling retractions: pred@τ_s (reason), …". This is
  what the probe read to make the samurai finding.

The information is **preserved** in the classifier's output dict
and in the verifier comment. It is not lost.

## What is not preserved

Two gaps exist between "preserved in classifier output" and "first-
class narrative signal":

1. **No propagation to `VerificationReview` / `StructuralAdvisory`
   records.** `enabling_retractions` lives inside
   `classify_arc_limit_shape_strong`'s return dict, consumed only by
   `dsp_limit_characterization_check`. Other verifiers cannot observe
   enabling retractions without re-running the classifier.
2. **No typed record.** The tuple-of-tuples shape
   `(str, int, str)` is adequate for the comment-string consumer;
   a dataclass / NamedTuple would be more self-documenting and
   would enable type-aware downstream consumption.

## Candidate future consumers (surveyed; none yet pressing)

Future checks that could plausibly consume a first-class enabling-
retraction signal:

- **Scheduling-act composition with sketch-01's `requested_*`.** An
  enabling retraction immediately following a `requested_*` or
  `scheduled_*` Prop on the same arc is structurally a "scheduled-
  act completion" — the speech-act set up the commitment, the
  retraction cleared its blocker. Could strengthen LT9. Most
  plausible consumer; probe did not ask for it.
- **DSP_growth agency pivots.** Enabling retractions sometimes mark
  the moment the MC's agency shape shifts — e.g., `bound_to`
  retracted → MC moves from captive-shape to combatant-shape.
  Currently handled by AG1–AG6 on event-shape directly; enabling-
  retraction signal would be redundant unless AG's coverage turns
  out incomplete.
- **Scene or beat boundary detection.** Enabling retractions often
  coincide with scene transitions (the unbinding IS the scene
  start). No verifier currently targets scene boundaries at this
  granularity; beat-weight-taxonomy-sketch-01 operates on
  beat_type labels already, not on retraction shapes.
- **DA_mc domain-shift markers.** Enabling retractions can mark the
  moment an MC's Activity domain shifts. DA_mc checks in the
  dramatica-complete verifier surface currently count per-event
  domain-participation via MN / EK classifiers; a retraction-kind
  signal isn't obviously wanted.

None is currently pressing. The closest is the scheduling-act
composition, which shares commit-proximity with sketch-01 but wasn't
proposed by any probe.

## What this sketch commits to

- [**EP1**] Name the finding. Defer mechanism.
- [**EP2**] Document the current preservation surface (above) so a
  future sketch-02 knows the baseline and doesn't re-derive it.
- [**EP3**] Enumerate concrete criteria for "earning its keep"
  (below) so revisit isn't speculative.
- [**EP4**] No code changes. No test changes. No substrate changes.
  No new record types. No new output fields.

## Criteria for revisit (sketch-02 forcing functions)

Write a sketch-02 that commits mechanism when at least one of the
following holds:

1. **Probe observation points at a specific check** that would
   benefit from a first-class enabling-retraction signal. "Preserve
   the information" is the current finding; "feed it to X check so
   X's verdict improves" would be a sketch-02 forcing function.
2. **A concrete verifier change is drafted** that consumes enabling
   retractions as verdict input. E.g., scheduling-act-utterance
   sketch-02 commits to "enabling retraction immediately following
   a scheduling Prop contributes +0.25 to LT9 strength." Shape
   follows the concrete use.
3. **A second encoding exhibits enabling retractions** in a
   structurally-different shape than Rashomon's. All current
   examples are Rashomon bandit/samurai `bound_to` retractions
   under LT12a. A second shape — LT12b subject-reactivation in a
   non-Rashomon encoding, or a retraction whose "enabling" nature
   reads differently per narrative context — would pressure the
   reason-code vocabulary to grow, at which point a typed record
   earns its keep.
4. **Downstream-consumer inconvenience.** If the tuple-of-tuples
   shape causes a concrete implementation friction when a second
   consumer is written (e.g., filtering by reason code becomes
   awkward, or downstream code duplicates tuple-unpacking), the
   cost-of-upgrade justification becomes load-bearing.

None of these holds today. State-of-play-02 lists this finding
among open probe seeds; a reader tracking it should check against
these criteria at the next milestone boundary.

## Why defer (rationale)

- **The information is preserved.** It reaches the probe today via
  the verifier comment string — which is how the post-LT12 probe
  saw the bound_to retraction at τ_s=10 and made the finding in
  the first place. Absent a downstream check other than the probe,
  the comment-string surface is sufficient.
- **No verifier needs typed surface today.** Adding one creates a
  record-shape maintenance burden and test coverage cost without a
  verdict change. The project's discipline favors adding mechanism
  when a forcing function argues for it; not preemptively.
- **The most plausible consumer — scheduling-act composition —
  is itself fresh.** Sketch-01 just landed (2026-04-18, commit
  `86b4b03`); it has not yet gone through a probe cycle. Any
  composition mechanism should wait for sketch-01's first probe
  feedback, which may reshape the combination target.
- **Premature typed-record design risks getting the shape wrong.**
  A consumer-driven record shape is a stronger design than a
  preservation-driven one. Wait for the consumer to appear, then
  shape the record to fit its need.

## Alternatives considered

- **Mild preservation.** Upgrade `enabling_retractions` to a typed
  dataclass/NamedTuple; propagate via `StructuralAdvisory` records
  so other verifiers can observe enabling retractions without
  re-running the classifier. Cost: ~50 lines of code + propagation
  tests. Benefit: zero measured verdict change. **Rejected** —
  premature without a consumer.
- **Composition-with-SC.** Commit to "enabling retraction
  immediately following a `requested_*` / `scheduled_*` Prop
  strengthens LT9." Concrete and measurable; ties naturally to
  sketch-01. **Rejected** — the post-LT12 probe didn't propose it;
  speculative design. If sketch-01's next probe cycle points at
  this composition, it becomes a real sketch-02.
- **Name-only preservation in a new enum.** Add an
  `EnablingRetractionKind` enum with `CONSTRAINT_VOCABULARY` and
  `SUBJECT_REACTIVATION` members (replacing the string reason
  codes). Cost: small. Benefit: type-checkable reason codes.
  **Rejected** — the strings already function as an enum in
  practice, and changing them invalidates every existing test that
  asserts against the string values (about 6 assertions). Cost
  exceeds benefit without a consumer.

## Summary

The samurai probe finding is banked as a named deferral rather than
absorbed as mechanism. The classifier already preserves enabling
retractions with typed reason codes and surfaces them via the
verifier comment string the probe reads — the information is not
lost. First-class propagation to VerificationReview / typed record
shape are the gaps, but no verifier currently needs them. Sketch-02
of this topic should be written when a concrete forcing function
arrives; four criteria enumerated. Committing code without a
forcing function would invent maintenance cost without narrative
payoff.

This is the first **explicit deferral sketch** in the design
corpus. Prior sketches have banked OQs within commitment sketches
(sketch-03's OQ1–OQ4; sketch-01's OQ1–OQ4). An OQ is an internal
loose-end within a sketch; a deferral sketch is a standalone
no-commitment record. Both are first-class; the deferral-sketch
form is right when the finding is a separable topic (its own
concern, its own potential consumers) rather than a loose-end
attached to an adjacent commitment.
