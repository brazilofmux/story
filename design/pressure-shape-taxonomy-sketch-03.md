# Pressure-shape taxonomy — sketch 03

**Status:** draft, active
**Date:** 2026-04-18
**Supersedes:** nothing (amendment to [pressure-shape-taxonomy-sketch-02](pressure-shape-taxonomy-sketch-02.md); extends LT1–LT11 without retouching them)
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [architecture-sketch-02.md](architecture-sketch-02.md), [substrate-sketch-05.md](substrate-sketch-05.md), [verification-sketch-01.md](verification-sketch-01.md), [reader-model-sketch-01.md](reader-model-sketch-01.md), [multi-story-sketch-01.md](multi-story-sketch-01.md)
**Related:** `verifier_helpers.py` (`classify_arc_limit_shape_strong`, `dsp_limit_characterization_check`), `rashomon.py`, `rashomon_dramatica_complete.py`, `rashomon_dramatica_complete_verification.py`, Rashomon cross-boundary probe output (`reader_model_rashomon_output.json`, committed 2026-04-18 at `6fa0d1d`)
**Superseded by:** nothing yet

## Purpose

Close the two LT2 findings the Rashomon probe returned — both
specific, both grounded, both about signals LT2 currently
mis-classifies. Sketch-02 landed LT7–LT11 in response to Rocky's
probe dissent; sketch-03 lands LT12–LT14 in response to Rashomon's
probe qualifications on DSP_bandit_limit and DSP_samurai_limit.

Amendment, not supersession. Sketch-01's LT1–LT6 and sketch-02's
LT7–LT11 stand unchanged. LT12–LT14 refine the LT2 signal
vocabulary itself — the predicate LT2 was originally written for
turns out to conflate two structurally distinct kinds of retraction,
and to miss a third signal that isn't a retraction at all.

## What the probe proposed

From `reader_model_rashomon_output.json`, two verifier_commentaries
on testimony DSP_limit verdicts (assessment: qualifies).

**DSP_bandit_limit (NEEDS_WORK 0.67), probe suggestion:**

> "Consider distinguishing enabling retractions (state removal that
> opens a new possibility for the immediately subsequent event, e.g.,
> 'unbound' enabling 'combat') from restricting retractions (state
> removal that forecloses a previously available path). Only
> restricting retractions should count as LT2 convergence evidence
> for optionlock."

**DSP_samurai_limit (NEEDS_WORK 0.67), probe suggestion:**

> "Consider checking whether events with effect_count=0 that
> structurally foreclose a narrative path (e.g., a refusal event
> that eliminates a previously offered action) should count as
> retractions for LT2 purposes, even when they carry no typed
> state-change effects in the substrate."

Two distinct refinements. The first (enabling vs restricting) is
the deeper of the two — it points at a conceptual conflation in
LT2's retraction detector. The second (effect_count=0 foreclosures)
is an honest gap: LT2 needs a prop to detect, and a refusal event
doesn't produce one.

Both land in this sketch. The first as a full commitment (LT12);
the second as a protocol for author opt-in (LT13) with automatic
detection deferred (OQ1).

## What this sketch commits to

- A constraint-predicate vocabulary (LT12a) that names the class of
  propositions whose retraction is presumed enabling. Initial list
  is verifier-local and small; authors can extend it per encoding.
- A positional-enabling rule (LT12b) that catches enabling
  retractions outside the lexical vocabulary: a retraction of
  `P(X, ...)` is enabling if `X` appears as a named participant in
  a subsequent event within a short arc window.
- LT2's middle-arc convergence count excludes enabling retractions.
  Restricting retractions continue to count as before.
- An affordance-retraction protocol (LT13) for effect_count=0
  foreclosure events — author-opt-in via synthetic `affordance_*`
  retractions rather than automatic detection. Verifier-local
  vocabulary, same shape as LT6's `scheduled_*`.
- A small extension to the LT10 disposition table (LT14) covering
  the new verdict shapes; no row is removed, only the "retraction
  kind" column is refined.

## What this sketch does NOT commit to

- **Automatic foreclosure detection.** LT13 asks the author to name
  the affordance being retracted; it does not detect foreclosure
  structurally from a zero-effect event. Automatic detection is
  deferred to OQ1 pending a larger refusal-event corpus.
- **A universal constraint-predicate registry.** The LT12a
  vocabulary is intentionally small (`bound_to`, `tied_to`,
  `imprisoned_in`, `trapped_in`, `locked_in`; explicitly NOT
  `scheduled_` — that's LT8's domain). Authors can add predicates
  to their encoding's verifier invocation; a cross-corpus registry
  is OQ2.
- **Re-banding of prior encodings.** Oedipus, Macbeth, Ackroyd, and
  Rocky pass through LT12–LT14 unchanged — their retractions are
  all restricting (Macbeth's `king(macbeth, scotland)`, Ackroyd's
  `accused_of_murder(ralph_paton, ackroyd)`) or already handled by
  LT7's peripheral-pre banding (Rocky's `scheduled_fight(apollo,
  mac)`). No existing verdict shifts.
- **Enabling-retraction semantics beyond the LT2 count.** LT12
  specifies that enabling retractions don't count as LT2
  convergence; it does not attempt to classify them as positive
  Timelock signals. An enabling retraction that preconditions a
  scheduled endpoint is simply silent — if that shape needs a
  Timelock-positive reading, it does so via LT8 (the scheduled
  predicate itself).

## Commitments

### LT12 — Enabling vs restricting retractions

A `WorldEffect` with `asserts=False` at event `e` retracting prop
`P(X, ...)` is classified as one of two kinds:

**LT12a — Lexical (constraint predicate).** The retraction is
**enabling** if `P.predicate` matches the verifier-local constraint-
predicate vocabulary. Initial vocabulary:

```
{"bound_to", "tied_to", "imprisoned_in", "trapped_in", "locked_in"}
```

Encodings can extend this set at their verifier invocation. The
`scheduled_` prefix is explicitly NOT in this set — it is LT8's
domain. Adding `scheduled_` to LT12a would double-handle it.

**LT12b — Positional (subject-reactivation).** If LT12a does not
fire, the retraction is **enabling** if the retracted prop's first
argument `X` appears as a named participant in any event `e'` with
`e'.τ_s ∈ (e.τ_s, e.τ_s + W]`, where the default window `W=2`.
"Named participant" means `X` is a value in `e'.participants`
(regardless of role — LT12b is lexically conservative rather than
role-aware; refining to role-aware detection is OQ3).

**LT12c — Default.** A retraction not matched by LT12a or LT12b is
**restricting**.

**LT2 integration:** only restricting retractions contribute to the
LT2 retraction count. Enabling retractions are reported in the
classifier output (under a new `enabling_retraction_count` field)
so the verifier comment can reference them, but they do not shift
the classification verdict.

The LT2 retraction-kind signal under LT12 reads: "N restricting
retractions, M enabling retractions" rather than sketch-01's flat
"retraction:N". Back-compat for sketch-01-only callers:
`classify_arc_limit_shape` (the narrow helper) continues to emit
the flat count with ALL retractions as before. Only
`classify_arc_limit_shape_strong` uses LT12's distinction.

### LT13 — Affordance retractions (author-opt-in)

Events that structurally foreclose a narrative possibility but
carry no typed world effect do not surface under LT2. The author
can expose the foreclosure to LT2 by adding a `WorldEffect`
retracting a synthetic affordance proposition:

```python
world(Prop("affordance_bandit_kills_husband", ()), asserts=False)
```

The predicate prefix `affordance_` is verifier-local naming (per
LT6). An `affordance_*` retraction counts as a **restricting**
retraction under LT12c by default — its first arg doesn't
correspond to a later-active participant (often the affordance is
an action label, not an agent), so LT12b does not fire.

The author-opt-in shape mirrors LT8's `scheduled_` prefix: both are
author-facing vocabularies the verifier recognizes without needing
substrate-level extensions. No new effect kind, no new record type.

For the Rashomon samurai testimony: `E_h_tajomaru_refuses` could
add `world(affordance_bandit_kills_husband(), asserts=False)` —
but because the affordance was never asserted in canonical scope
(no canonical event proclaims "the bandit may kill the husband"),
the retraction fires LT2's "prop was never asserted" guard and is
silently dropped. LT13's protocol therefore also requires the
author to assert the affordance BEFORE retracting it, typically at
the preceding utterance event:

```python
# E_h_wife_requests_killing (τ_s=7) asserts the affordance
world(Prop("affordance_bandit_kills_husband", ()), asserts=True)

# E_h_tajomaru_refuses (τ_s=8) retracts it
world(Prop("affordance_bandit_kills_husband", ()), asserts=False)
```

This ordering gives LT2 a clean assert-then-retract pair and
produces a valid restricting-retraction signal under LT12c. It
also makes the affordance visible to project_world / project_reader
as a proposition the reader holds for 1 τ_s tick — which may or
may not be the author's intent (OQ4).

### LT14 — Disposition table clarification

Extends LT10 with the LT12 restricting/enabling distinction. No
row is added or removed; two rows are clarified to make explicit
that LT2 counts are *restricting-only* under LT12:

| DSP_limit declared | Substrate shape | Verdict | Strength |
|---|---|---|---|
| Optionlock | middle-arc **restricting** LT2 signals present | APPROVED | `min(1.0, middle_kinds / 3.0)` |
| Optionlock | only peripheral/terminal **restricting** LT2 signals | PARTIAL_MATCH | `0.5 × (peripheral+terminal_kinds / 3.0)` |
| Optionlock | no restricting LT2 signals (enabling-only, or none) | NEEDS_WORK | 0.0 |
| Timelock | LT9 strong (LT8 ≥ 1 + middle-arc restricting LT2 = 0) | APPROVED | `min(1.0, lt8_count / 2.0)` |
| Timelock | LT8 signal + middle-arc **restricting** LT2 signals present | PARTIAL_MATCH | `0.5 × (1.0 − min(1.0, middle_kinds/3.0))` |
| Timelock | no LT8 signal, no middle-arc restricting LT2 signals (LT3 weak) | NOTED | 0.5 |
| Timelock | middle-arc **restricting** LT2 signals, no LT8 signal | NEEDS_WORK | `1.0 − min(1.0, middle_kinds/3.0)` |
| Unknown choice | any | NOTED | — |

Enabling retractions are reported in the check's comment (per LT12)
but do not shift the verdict. Rocky's peripheral-pre
`scheduled_fight` retraction continues to be classified as
peripheral-pre under LT7 — LT12 does not touch it (LT7 handles
arc-position first, LT12 handles kind among those that passed LT7's
middle-arc band).

## Worked case — Rashomon testimonies under LT12 (the load-bearing prediction)

All four testimony Stories declared Timelock. Under sketch-02 the
verifier returned NEEDS_WORK 0.67 for bandit and samurai (middle-arc
bound_to retraction); NOTED for wife and woodcutter.

### Bandit testimony (B_TAJOMARU scope)

LT2 signal scan:

- `E_t_frees_husband` (τ_s=8) retracts `bound_to(husband, tree)`.
- LT12a: `bound_to` is in the constraint vocabulary → **enabling**.
- LT12 exclusion: restricting retraction count = 0.

Middle-arc restricting LT2 count: **0**. LT8 count: 0 (no
`scheduled_*` predicates on bandit branch).

LT14 verdict: Timelock declared + no LT8 + no middle-arc restricting
→ **NOTED (LT3 weak) 0.5**. Comment cites the enabling retraction.

**Net shift:** NEEDS_WORK 0.67 → **NOTED 0.5**.

### Samurai testimony (B_HUSBAND scope)

LT2 signal scan:

- `E_h_frees_husband` (τ_s=10) retracts `bound_to(husband, tree)`.
- LT12a: enabling.
- LT12 exclusion: restricting retraction count = 0.

Middle-arc restricting LT2 count: **0**. LT8 count: 0.

LT14 verdict: **NOTED (LT3 weak) 0.5**. Same net shift as bandit.

### Wife testimony (B_WIFE scope)

No retractions reach LT2 under sketch-02 (the `at_location(tajomaru,
forest_road)` retraction at `E_w_tajomaru_leaves` targets a prop
that was never asserted in canonical scope). LT12 is silent. **No
change** — remains NOTED 0.5.

### Woodcutter testimony (B_WOODCUTTER scope)

No retractions on this branch at all. LT12 is silent. **No change**
— remains NOTED 0.5.

### Substrate-asymmetry finding (state-of-play-01 #3) absorbed

All four testimonies now reach uniform NOTED 0.5 under LT14 —
consistent with the uniform authorial Timelock claim, and
consistent-but-not-affirmed per LT3's weak-fallback asymmetry. The
sibling-asymmetry finding recorded in state-of-play-01 was an
artifact of LT2's enabling/restricting conflation, not a substantive
narrative signal. LT12 absorbs it cleanly; no sibling-comparison
verifier pass is needed.

Per LT5, the author's declaration still stands. NOTED says "the
substrate is consistent with Timelock but cannot affirmatively
detect it" — if the author wants APPROVED, the path is to add a
`scheduled_*` predicate naming the testimony's temporal endpoint
(LT8 opt-in). None of the four Rashomon testimonies have an
obvious scheduled endpoint — testimonies are events-as-remembered,
not events-against-a-calendar — so NOTED is likely the honest
terminal verdict. That's fine; NOTED is a valid verdict.

## Worked case — Oedipus / Macbeth / Ackroyd / Rocky under LT12

Prediction: **no change**. Each encoding's retractions are either
restricting (so LT12 leaves them counted) or handled by sketch-02's
LT7 before LT12 applies:

- **Macbeth**: `king(macbeth, scotland)` retracted at Macbeth's
  death. Not a constraint predicate (LT12a miss); the retractee
  (`macbeth`) does not reappear as a later-active participant (he's
  dead) — LT12b miss. LT12c: **restricting**. Counted as before.
- **Ackroyd**: `accused_of_murder(ralph_paton, ackroyd)` retracted
  at the reveal. Not a constraint predicate; `ralph_paton` does
  reappear in subsequent participant lists, so LT12b MIGHT classify
  this as enabling. *Case to verify in implementation.* If LT12b
  fires spuriously, the implementation pass narrows the rule
  (e.g., require the retractee to appear in an agentive role, not
  just as a mentioned party). Noted as OQ3.
- **Oedipus**: no `asserts=False` world effects — no retraction
  signals at all. LT12 is silent. Identity-resolutions (LT2's other
  signal kind) are untouched by LT12.
- **Rocky**: `scheduled_fight(apollo, mac)` retracted at
  `E_mac_injured` — LT7 classifies it peripheral-pre; LT12 does
  not apply (it operates within the middle-arc band). Status:
  unchanged.

Expected measurements post-implementation:

- Oedipus APPROVED 0.67 → **unchanged**
- Macbeth APPROVED 0.67 → **unchanged**
- Ackroyd APPROVED 0.67 → **unchanged if LT12b does not misfire;
  lower verdict shift if it does** (OQ3)
- Rocky APPROVED 1.00 → **unchanged** (two `scheduled_fight`
  Props in Rocky's substrate: apollo-mac AND apollo-rocky; LT9
  strength `min(1.0, 2/2.0) = 1.00`)

## Implementation brief

Concrete change, in order of landing:

1. **Extend `classify_arc_limit_shape_strong`** with LT12 output
   fields:
   - `restricting_retraction_bands`: dict of band → count, same
     shape as current `retraction_bands` but filtered through
     LT12.
   - `enabling_retraction_count`: total count (all bands).
   - `enabling_retractions`: tuple of `(prop, τ_s, reason)` where
     `reason` is `"constraint-vocabulary"` or `"subject-
     reactivation"`.
   The existing `retraction_bands` field stays for sketch-01
   back-compat (flat count, no kind distinction).

2. **Add `classify_retraction_kind`** helper per LT12:
   ```python
   def classify_retraction_kind(
       retracted_prop, event_τ_s, fabula,
       canonical_branch, all_branches,
       constraint_vocab: frozenset = DEFAULT_CONSTRAINT_VOCAB,
       window: int = 2,
   ) -> tuple:  # ("enabling", reason) or ("restricting", None)
   ```
   Encodings that want custom constraint vocabulary pass it in;
   default is the LT12a list.

3. **Update `dsp_limit_characterization_check`** to route
   restricting-only LT2 counts through LT14's disposition table.
   The comment string gains an "enabling retractions: N" clause
   when any fire, so the verdict rationale surfaces the distinction.

4. **No substrate changes.** No new `Prop` kinds, no new
   `WorldEffect` fields, no new effect types. The `affordance_*`
   prefix (LT13) is author-facing vocabulary only; the substrate
   treats `affordance_*` props identically to any other prop.

5. **Test updates.**
   - `test_verification.py` (or the pressure-shape-taxonomy
     dedicated tests — verify location): add a case per LT12a,
     LT12b, LT12c on a minimal fixture.
   - `test_rashomon.py`: assert the new NOTED 0.5 verdicts on all
     four testimonies.
   - Rocky / Macbeth / Oedipus / Ackroyd verdict-pinning tests:
     verify unchanged.

6. **Update `rashomon_dramatica_complete_verification.py`
   docstring** to reference LT12–LT14 and the expected uniform-NOTED
   outcome.

7. **Re-run the probe** against Rashomon post-implementation. The
   expectation: 5 endorses (no qualifications remaining). If the
   probe qualifies or dissents on LT12's shape, that's the next
   arc's starting point.

## Measurements prediction

Before sketch-03 (current):
- Rashomon bandit: NEEDS_WORK 0.67
- Rashomon samurai: NEEDS_WORK 0.67
- Rashomon wife: NOTED 0.5
- Rashomon woodcutter: NOTED 0.5
- Rocky: APPROVED 1.00
- Ackroyd: APPROVED 0.67
- Macbeth: APPROVED 0.67
- Oedipus: APPROVED 0.67

After sketch-03 (predicted):
- Rashomon bandit: **NOTED 0.5** ← shift
- Rashomon samurai: **NOTED 0.5** ← shift
- Rashomon wife: NOTED 0.5 (no change)
- Rashomon woodcutter: NOTED 0.5 (no change)
- Rocky: APPROVED 1.00 (no change)
- Ackroyd: APPROVED 0.67 (no change — OQ3 verifies)
- Macbeth: APPROVED 0.67 (no change)
- Oedipus: APPROVED 0.67 (no change)

Net effect: two false-positive NEEDS_WORK shifts to honest NOTED;
uniform verdict across the four Rashomon testimonies; no prior
encoding's verdict moves. The second probe-finding (affordance
foreclosure, LT13) becomes available to future encodings via the
`affordance_*` prefix protocol; no current encoding adopts it in
this pass.

## Discipline

Sketch-03 is a narrowing of sketch-01's LT2, not a widening. The
sketch adds no new signal kinds and no new classification outputs
beyond the LT12 breakdown. LT2's original intent — detect arc-body
convergence that signals Optionlock — is preserved; what sketch-03
fixes is the detector was counting signals that didn't fit that
intent (enabling retractions create affordances; they don't foreclose
them).

The probe's two qualifications came from the same run, against the
same multi-Story encoding, at the same boundary. Both got absorbed.
If subsequent probe runs surface additional refinements to the LT2
surface, the pattern is: amend (sketch-NN+1), not restart. LT2's
original articulation isn't wrong — just narrower than its
initial naming suggested.

## Open questions

**OQ1 — Automatic foreclosure detection.** LT13 requires author
opt-in via the `affordance_*` prefix. A future refinement could
detect foreclosure structurally — e.g., events with effect_count=0
following a preceding utterance event whose content describes an
offered action, where the current event's type is in a refusal
vocabulary (`"refusal"`, `"decline"`, `"abstain"`). Requires a
larger refusal-event corpus than the current five encodings
supply. Deferred.

**OQ2 — Cross-corpus constraint-predicate registry.** LT12a's
initial list is tight by design. A corpus-wide registry (like
Dramatica's own lexicon of beats) would make the vocabulary
author-facing rather than verifier-local. Requires consensus across
multiple encodings and probably a dedicated sketch. Deferred.

**OQ3 — LT12b role-awareness.** The lexically-conservative
"appears as any participant" rule risks false-enabling verdicts on
retractions whose first-arg-entity is merely mentioned in a later
event, not actually activated. The Ackroyd `ralph_paton` case may
be exposed here. If the implementation pass surfaces a false
positive, narrow LT12b to require the retractee to appear in an
agentive role (role-label set: `{"agent", "speaker", "killer",
"thief", "observer", "deceiver", "binder", "a", "b"}` per current
corpus usage). Deferring the decision to the implementation pass
rather than pre-committing in sketch.

**OQ4 — Affordance-as-proposition semantics.** LT13's protocol
asserts an affordance proposition for one τ_s tick before
retracting it. The reader's knowledge state will then briefly hold
an affordance — which might or might not be the author's intent.
If the reader's brief holding is narratively wrong ("the reader
shouldn't know the option existed"), the author can scope the
affordance to a testimony branch only, or mark its assertion with a
lower slot (BELIEVED rather than KNOWN). Noted here as a
consideration for encodings adopting LT13 rather than a commitment.

## Summary

Sketch-03 lands in response to the Rashomon probe's two
qualifications on testimony DSP_limit verdicts. LT12 distinguishes
enabling retractions (constraint-removal that opens a new action)
from restricting retractions (option-closing convergence); only the
latter count as LT2 signals. LT13 gives authors a way to expose
effect_count=0 foreclosures to LT2 via an `affordance_*` prefix
protocol. LT14 clarifies LT10's disposition table to reference
*restricting* LT2 counts.

No substrate changes. No schema extensions. The sketch closes two
measured false-positive NEEDS_WORK verdicts on Rashomon testimonies
and harmonizes the four testimonies' verdicts into uniform NOTED
— consistent with the uniform authorial Timelock claim, honest-but-
unaffirmed per LT3's weak-fallback.
