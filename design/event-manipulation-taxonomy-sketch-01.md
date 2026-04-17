# Event-manipulation taxonomy — sketch 01

**Status:** draft, active
**Date:** 2026-04-17
**Supersedes:** nothing (new topic; parallel to [event-kind-taxonomy-sketch-01](event-kind-taxonomy-sketch-01.md), [event-agency-taxonomy-sketch-01](event-agency-taxonomy-sketch-01.md), and [pressure-shape-taxonomy-sketch-01](pressure-shape-taxonomy-sketch-01.md))
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [architecture-sketch-02.md](architecture-sketch-02.md), [substrate-sketch-05.md](substrate-sketch-05.md), [verification-sketch-01.md](verification-sketch-01.md), [reader-model-sketch-01.md](reader-model-sketch-01.md), [identity-and-realization-sketch-01.md](identity-and-realization-sketch-01.md)
**Related:** `ackroyd_dramatica_complete_verification.py` (DA_mc check); Ackroyd cross-boundary probe qualification on DA_mc (`reader_model_ackroyd_dramatica_complete_output.json`, committed 2026-04-17 at `faaebd8`)
**Superseded by:** nothing yet

## Purpose

Close the Ackroyd cross-boundary reader-model probe's DA_mc
qualification (PARTIAL 0.54 — the only PARTIAL in the four-encoding
DA_mc spread). The probe named a real gap: the current
Manipulation-domain check uses a frozen `MANIPULATION_KINDS` type-
string set; investigatory events where Sheppard is `also_present` or
`assistant` don't match those types and get counted as
non-manipulation — but from the MC Throughline's point of view, those
events ARE manipulation, because Sheppard is **performing innocence
while concealing `killed(sheppard, ackroyd)`**.

This sketch commits a structural **concealment-manipulation**
classifier: an event is manipulation-shaped (wrt MC) when the MC
holds a self-fact at KNOWN that at least one other participant does
not — the knowledge asymmetry IS the concealment. Parallel to EK2's
external-action classifier, AG3's pursuit predicate, and LT8's
scheduling detector. Lives in `verifier_helpers.py`; composes
cleanly with Ackroyd's existing `MANIPULATION_KINDS` set rather than
replacing it.

Fourth concrete probe → sketch → measurement-shift cycle in two days
(after LT9 scheduling, AG5 agency, IG2 identification-goal).

## What the probe proposed

From `reader_model_ackroyd_dramatica_complete_output.json`,
verifier_commentaries entry for `dramatica-complete:DA_mc`
(assessment: qualifies):

> "The 54% manipulation-kind ratio understates the case. Even
> events the check classifies as 'investigatory/discovery' (e.g.,
> E_body_discovered where Sheppard is 'also_present,'
> E_poirot_investigates where he is 'assistant') are
> manipulation-colored from the MC perspective — Sheppard is
> performing innocence at every one of these events. A structural
> event-type count cannot detect the concealment layer that makes
> each Sheppard-present event a manipulation event from the
> throughline's point of view."

And `suggested_signature`:

> "Consider weighting events where the MC's participant role is
> one of apparent collaboration (e.g., assistant, also_present)
> while the MC owns an active concealment motive — these are
> manipulation-shaped even when their event type is investigatory."

## What this sketch commits to

- A **knowledge-asymmetry** structural predicate: an event is
  concealment-manipulation-shaped iff the MC holds at Slot.KNOWN
  at least one self-fact (world-proposition whose first argument
  is MC's entity id) that at least one other participant in the
  same event does NOT hold at Slot.KNOWN at the event's τ_s.
- Compositional with Ackroyd's existing `MANIPULATION_KINDS`: an
  event counts as Manipulation-domain if its event-type is in
  `MANIPULATION_KINDS` OR the new classifier returns
  `"manipulation"`. The type-string set becomes an early-positive
  fast path, not the sole classifier input.
- Zero substrate changes. The predicate reads existing
  `project_knowledge` + `holds_as(Slot.KNOWN)` for each event
  participant; the MC's own knowledge-state provides the
  self-facts; the other participants' projections provide the
  asymmetry signal.
- The classifier is verifier-local, not a substrate commitment.
  Save-the-Cat or another dialect could reuse the predicate if
  useful; each dialect decides.

## What this sketch does NOT commit to

- **Replacing `MANIPULATION_KINDS`.** The existing frozen set
  captures the positive signals (killing, staged_disclosure,
  blackmail_begins) cleanly at the type-string level. MN4
  composes the two; it doesn't retire either.
- **Generalizing the predicate to all encodings.** Macbeth's MC
  (Macbeth) holds `killed(macbeth, duncan)` at KNOWN and
  participants at the banquet don't — under MN2, those events
  would classify as manipulation-shaped too. But Macbeth's DA_mc
  is Activity-domain, not Manipulation; the manipulation
  classifier's output is not wired into Macbeth's DA_mc check.
  Each encoding's DA_mc check picks which classifiers to compose.
- **A universal motive model.** Per A3 and EK1, the sketch does
  not add a `concealment_motive` field to events or to the MC
  character. Motive is read structurally from the knowledge-state
  asymmetry, not from author-declared tags.
- **Classifying MC-non-participant events.** If the MC is not in
  an event's participants, the classifier returns None — the
  event is not a Manipulation-domain signal either way.
- **Resolving what the "self-fact" subject-matter should be.**
  The predicate accepts any world-fact whose first arg is MC_id
  and is KNOWN to MC but not to at least one other participant.
  For Ackroyd this cleanly catches `killed(sheppard, ackroyd)`;
  for a future encoding where multiple self-facts concurrently
  hold, all contribute. OQ1 banks the question of whether finer
  subject-matter gating is needed.

## Commitments

### MN1 — Verifier classification reads fold-visible structure, not type strings

Parallel to EK1, LT1, AG1, IG1. The concealment-manipulation
predicate is a function of the event's participants, the substrate's
world-state at τ_s, and each participant's KnowledgeState at τ_s.
Event type strings may inform priors (Ackroyd's `MANIPULATION_KINDS`
set remains a valid positive signal) but are not the sole classifier
input.

### MN2 — Concealment-manipulation predicate (structural)

An event is **concealment-manipulation-shaped with respect to MC**
iff all of:

1. MC is a participant in the event (MC's entity id appears in the
   event's `participants` dict values).
2. At least one world-proposition `P` is asserted in the substrate
   at τ_s ≤ event.τ_s where `P.args[0] == mc_id` (MC is the
   subject of `P`).
3. MC holds `P` at `Slot.KNOWN` in their KnowledgeState at τ_s =
   event.τ_s.
4. At least one non-MC participant in this event does NOT hold `P`
   at `Slot.KNOWN` at τ_s = event.τ_s (weaker slot or absent).

The four conditions together detect **asymmetric knowledge about the
MC's own state** — the structural trace of performed innocence /
concealment. Sheppard holds `killed(sheppard, ackroyd)` at KNOWN from
the murder onward; until Poirot's reveal, co-participants in
investigation events (Caroline, Raglan, Flora) do not hold it at
KNOWN. The asymmetry fires MN2.

Per MN1, the predicate reads only fold-visible structure — no motive
tags, no author-declared concealment flags. The substrate's existing
KnowledgeEffect / project_knowledge machinery is sufficient.

### MN3 — Classifier lives in `verifier_helpers.py`

Parallel to EK3, LT4, AG4. Signature:

```python
def classify_event_manipulation_shape(
    event: Event,
    mc_id: str,
    events_in_scope: list,
) -> Optional[str]:
    """Returns 'manipulation' / 'non-manipulation' / None.
    None if MC is not a participant in this event. 'manipulation'
    if MN2's asymmetry predicate fires. 'non-manipulation'
    otherwise."""
```

The function projects knowledge states at event.τ_s for each non-MC
participant and compares against MC's own state on self-facts. The
comparison is O(self_facts × participants); both are small per
event.

### MN4 — Ackroyd DA_mc check composes MN3 with `MANIPULATION_KINDS`

`mc_throughline_manipulation_domain_check` counts an event as
manipulation-shaped if:

- `_event_kind(e) in MANIPULATION_KINDS` (existing positive
  signal), OR
- `classify_event_manipulation_shape(e, SHEPPARD_ENTITY_ID,
  events_in_scope) == "manipulation"` (new structural signal).

The two are OR-composed. Strength improves when the structural
signal fires on investigation events the type-set misses. The
existing `MANIPULATION_KINDS` set stays intact as the fast path for
events whose type directly names the manipulation shape (killing,
blackmail_begins, etc.).

### MN5 — Manipulation classification is verifier-local

Parallel to EK5, LT6, AG6, IG5. The concealment-manipulation frame
is a property of the verifier's DA_mc reading for Ackroyd, not a
substrate commitment. Other dialects' manipulation-adjacent checks
(e.g., Save-the-Cat genre-aware MC-concealment detection) could
reuse MN3 or define their own classifiers.

## Worked case — Ackroyd under MN4

Ackroyd's 13 MC-Throughline events (via `L_mc_throughline`):

- 7 match `MANIPULATION_KINDS` (E_sheppard_murders_ackroyd,
  E_blackmail_begins, etc.) — fire via the existing type-set
  signal.
- 6 are investigatory (E_body_discovered, E_poirot_investigates,
  E_alibi_examined, etc.) — these are where Sheppard is
  `also_present` or `assistant` and the event's type is discovery/
  investigation.

Under MN2 applied to the 6 investigatory events:
- Sheppard holds `killed(sheppard, ackroyd)` at `Slot.KNOWN` from
  τ_s=1 (the murder) onward.
- Pre-reveal (τ_s < 8), other participants (Caroline, Raglan,
  Flora, Hammond, Blunt) do not hold `killed(sheppard, ackroyd)`
  at KNOWN. MN2's asymmetry predicate fires.
- Post-reveal (τ_s ≥ 8), Poirot and at least one witness hold it
  at KNOWN. Events where ONLY knowers participate won't fire MN2
  (no asymmetry). Events where at least one non-knower is present
  still fire.

Measured prediction: **MN4 moves Ackroyd DA_mc from 7/13 (54%,
PARTIAL) to at least 12/13 or 13/13 (~92-100%, APPROVED)**. The
exact count depends on which investigation events have any
non-knower participant post-reveal.

Per the existing thresholds (≥70% → APPROVED; ≥40% → PARTIAL;
else NEEDS_WORK), the Ackroyd DA_mc verdict lifts PARTIAL 0.54 →
**APPROVED (≥0.90)**.

## Worked case — Macbeth / Oedipus / Rocky (no-regression)

The Manipulation classifier is only wired into Ackroyd's DA_mc
check. For Macbeth / Oedipus / Rocky, DA_mc is a different domain
(Activity or Fixed Attitude) checked via EK2's action-shape
classifier. MN3 is available but not called from those checks.

Note: Macbeth's MC (Macbeth) does have concealment structure —
holds `killed(macbeth, duncan)` at KNOWN post-murder while other
banquet participants don't. If a future encoding probes Macbeth's
DA_mc asking the Manipulation question, MN2 would fire there. The
sketch doesn't force that wiring; Macbeth's DA=Activity stays
correct under EK2.

## Implementation brief

1. **Add `classify_event_manipulation_shape` to
   `verifier_helpers.py`.** Uses `project_knowledge` +
   `holds_as(Slot.KNOWN)` on each participant's state at event.τ_s.
   MN2's asymmetry predicate is the core loop.
2. **Update
   `mc_throughline_manipulation_domain_check` in
   `ackroyd_dramatica_complete_verification.py`** to compose MN3
   with `MANIPULATION_KINDS` per MN4. The existing thresholds
   (≥70%, ≥40%) remain.
3. **Update check message** to report the two contributions
   separately ("k via type-set + n via concealment-asymmetry") so
   the verdict's breakdown is inspectable.
4. **Add unit tests in `test_verification.py`:**
   - `classify_event_manipulation_shape` on synthetic events
     with controlled participant knowledge states.
   - Integration pin: Ackroyd DA_mc lifted from PARTIAL to
     APPROVED under MN4.
   - No-regression: Macbeth / Oedipus / Rocky DA_mc verdicts
     unchanged.
5. **Update `design/README.md`** to register sketch-01 under a
   new bullet; promote the Ackroyd DA_mc qualification from
   "banked" to "landed".
6. **Update root `README.md`** with the four-landed count (LT9,
   AG5, IG2, MN4 — Macbeth DA_mc remains the last banked
   proposal).

## Measurements prediction

- Ackroyd DA_mc: PARTIAL 0.54 → **APPROVED ≥0.90** (exact
  strength depends on the concealment-asymmetry count on
  investigation events).
- Oedipus DA_mc: APPROVED 0.77 (unchanged; uses EK2, not MN3).
- Macbeth DA_mc: PARTIAL 0.69 (unchanged; MN3 not wired).
- Rocky DA_mc: APPROVED 0.72 (unchanged; EK2).

## Discipline

- **MN2 composes with identity-substitution per I3/I7.** A
  future encoding where MC's self-fact becomes KNOWN via
  identity collapse (not direct authoring) should still fire MN2
  at the right τ_s, because `holds_as` is substitution-aware.
- **The predicate is MC-centric.** For ensemble or multi-
  perspective stories, the classifier would need to be run
  per-investigator-role; the current Ackroyd case has a single
  MC. OQ3 in event-agency-sketch-01 has a parallel open
  question about multi-MC encodings.
- **The sketch does not generalize "manipulation" beyond
  knowledge-asymmetry-about-self.** Other manipulation forms
  (e.g., MC manipulating OTHERS' beliefs about a third party)
  are out of scope; a future sketch could add another predicate
  for that shape.

## Open questions

1. **Subject-matter gating of self-facts.** The predicate fires
   on any self-fact with the asymmetry pattern. For an encoding
   where the MC has many self-facts of varied relevance (some
   concealed, some trivially private), the predicate might
   over-trigger. Banking: add a "relevance to arc" filter if
   needed. Not an issue for current corpus.

2. **Dramatic irony vs. concealment.** MN2 detects character-to-
   character knowledge asymmetry. Dramatic irony is typically
   reader-to-character — that's a different structural surface
   (the view layer, per reader-model-sketch-01). Not addressed.

3. **Asymmetry direction.** MN2 fires when MC knows something
   others don't. The reverse (others know something MC doesn't)
   is a different shape — dramatic irony directed AT the MC
   (e.g., Oedipus pre-anagnorisis, where witnesses figure it out
   before he does). That's a different verifier question —
   relevant for DSP_growth=Stop trajectories potentially, but
   not for DA_mc.

4. **Post-reveal events.** Once the concealment breaks (τ_s=8
   in Ackroyd), the asymmetry may collapse — but investigation
   events still happen with Sheppard performing defeat / writing
   confession. Are those still manipulation-shaped? Probably
   yes (he's managing narrative), but MN2's current predicate
   fires based on unknown-self-facts, not narrative management.
   If a post-reveal event has Sheppard + Poirot (both know) +
   someone-else who doesn't know yet, MN2 still fires. Adequate
   for current corpus.

5. **Multi-self-fact weighting.** If an MC holds multiple
   concealed self-facts simultaneously (a common structural
   pattern for complex MCs), MN2 fires on any one of them. The
   strength isn't weighted by how many fire. A future refinement
   could count asymmetry-depth; not a current forcing function.

## Summary

- Ackroyd DA_mc PARTIAL 0.54 → APPROVED predicted, driven by the
  2026-04-17 cross-boundary probe's qualification.
- New verifier-helper classifier `classify_event_manipulation_shape`
  parallel to EK2 / AG classifier / IG knowledge-projection usage.
- Concealment-manipulation predicate: MC knows self-fact at
  KNOWN; at least one other participant in the event doesn't.
  Structural, participant-role-independent, no type-string
  dependence.
- Ackroyd DA_mc check composes MN3 with `MANIPULATION_KINDS` via
  OR; existing type-set signal preserved as fast path. Other
  encodings' DA_mc checks untouched.
- Zero substrate changes. Fourth concrete probe → sketch →
  measurement-shift cycle in two days. Four probe-proposed
  signatures now landed (LT9, AG5, IG2, MN4); one remains
  banked (Macbeth DA_mc beat-type weighting).
