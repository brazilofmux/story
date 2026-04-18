# Scheduling-act utterance — sketch 01

**Status:** draft, active
**Date:** 2026-04-18
**Supersedes:** nothing
**Frames:** [architecture-sketch-02](architecture-sketch-02.md), [substrate-sketch-05](substrate-sketch-05.md), [pressure-shape-taxonomy-sketch-01](pressure-shape-taxonomy-sketch-01.md) / [-02](pressure-shape-taxonomy-sketch-02.md) / [-03](pressure-shape-taxonomy-sketch-03.md), [verification-sketch-01](verification-sketch-01.md), [reader-model-sketch-01](reader-model-sketch-01.md)
**Related:** `verifier_helpers.py` (LT8 in `classify_arc_limit_shape_strong`), `rocky.py`, `rashomon.py`, post-LT12 Rashomon probe output (`reader_model_rashomon_post_lt12_output.json`, committed 2026-04-18 at `25a56f4`)
**Superseded by:** nothing yet

## Purpose

Close two of the four probe qualifications from the post-LT12
Rashomon run by (1) codifying Rocky's existing scheduling-Prop
pattern as general authoring discipline and (2) extending LT8's
prefix-recognition to a second narrative force — utterance-carried
requests.

Minimal scope: one discipline commitment, one prefix addition, one
classifier-output field. Two adjacent probe findings (`provoked_*`
goading; non-utterance `situational_forcing`) stay open as OQs;
neither is closed here.

## Context

Rocky is the only encoding in the corpus asserting `scheduled_*`
Props (4 assertions — `scheduled_fight(apollo, mac)` at τ_s=-10,
retracted at τ_s=-5; `scheduled_fight(apollo, rocky)` at τ_s=-1,
observed at τ_s=5). LT8 recognizes the `scheduled_` prefix and fires
LT9 (strong Timelock) for Rocky; Rocky's DSP_limit landed APPROVED
1.00 under pressure-shape-taxonomy-sketch-02.

The other four encodings have zero scheduling Props.

Rashomon's four testimony branches each contain an utterance event
at τ_s=7 with **zero world effects** — all speech-act content lives
in descriptions per substrate-sketch-05's M1 routing rule
(interpretive → descriptions; structural → effects). Under LT12's
enabling/restricting distinction (sketch-03), the testimony
branches' middle-arc restricting retraction counts are zero; their
DSP_limit Timelock declarations land NOTED 0.5 (honest-but-
unaffirmed). The probe reads this correctly and then asks: could
the utterance events themselves carry scheduling force visible to
LT8, if the substrate surfaced them as typed Props?

## What the probe proposed

From `reader_model_rashomon_post_lt12_output.json` (commit
`25a56f4`), four utterance-scheduling commentary suggestions:

**Bandit testimony (vr_1).** Event `E_t_wife_requests_killing`
(τ_s=7, type=utterance, 0 effects). Probe-suggested predicate:
`requested_combat` or `scheduled_confrontation`. Rationale: "The
utterance's role as the trigger that makes the duel obligatory is
precisely the kind of temporal forcing that Timelock encodes."

**Samurai testimony (vr_3).** Event `E_h_wife_requests_killing`
(same shape, samurai branch, 0 effects). Probe-suggested predicate:
`scheduled_killing`. Rationale: "the wife's plea to the bandit is
the act that, in the samurai's account, sets the betrayal arc in
temporal motion."

**Woodcutter testimony (vr_4).** Event `E_wc_wife_goads` (τ_s=7,
type=utterance, 0 effects, dual-listener). Probe-suggested
predicate: `provoked_confrontation`. Rationale: "marking the
goading as the speech act that temporally forces the fight into
existence."

**Wife testimony (vr_2).** Event `E_w_tajomaru_leaves` (τ_s=7,
type=**action** — not utterance). Probe-suggested predicate:
`situational_forcing`. Rationale: "marking the departure as the
condition that temporally compels the next act."

Bandit + samurai are the same structural shape across branches —
wife → tajomaru → kill husband — and reduce to a single pattern:
utterance event where a speaker requests a listener perform a
targeted action. Sketch-01 closes this pair.

Woodcutter (`provoked_*`) is a dual-party goading — structurally
different from a one-way request. Out of scope as OQ1.

Wife (`situational_forcing`) attaches to a non-utterance action
event; outside "scheduling-act utterance" entirely. Out of scope as
OQ2.

## What this sketch commits to

- [**SC1**] Canonical authoring discipline for encoding utterance-
  carried scheduling force — Rocky's pattern codified, applicable
  to any encoding.
- [**SC2**] LT8's prefix-recognition set extends from `{"scheduled_"}`
  to `{"scheduled_", "requested_"}`. Both prefixes fire LT8/LT9;
  semantic distinction is author-facing and surfaces in classifier
  output, not in verdict strength.
- [**SC3**] `classify_arc_limit_shape_strong`'s output dict gains a
  `scheduling_prefixes` field mapping each matched prefix to its
  Props. Existing `scheduling_signals_tuple` / `scheduling_count`
  fields unchanged — back-compat.
- [**SC4**] Rashomon worked-case — add `requested_killing(tajomaru,
  husband)` effects to `E_t_wife_requests_killing` and
  `E_h_wife_requests_killing`. Both testimony DSP_limit verdicts
  shift NOTED 0.5 → APPROVED 0.5.
- [**SC5**] Named out-of-scope findings as OQ1 (`provoked_*`) and
  OQ2 (`situational_forcing`) so they remain visible without
  forcing premature commitment.

## What this sketch does NOT commit to

- **Structural inference of scheduling force from utterance event
  structure** (the "Path C" option from design discussion). Classify
  an event as a scheduler-by-construction without author opt-in.
  Rejected: too easy to over-fire; every command/request in a
  dialogue-heavy encoding would accidentally fire LT9. The author-
  opt-in discipline (SC1) keeps the encoding author accountable for
  which utterances carry structural force.
- **Multiple new prefixes beyond `requested_*`.** `commanded_*`,
  `prophesied_*`, `goaded_*`, `sworn_*` are all plausible
  extensions; none has a corpus forcing function yet. One encoding
  exercising the shape is the threshold for adding a prefix. OQ3
  captures the prophecy case; OQ1 captures goading.
- **Per-prefix LT9 strength weighting.** Narratively defensible
  argument: requests are contingent on target acceptance,
  schedules are unconditional; `requested_*` should contribute less
  than `scheduled_*`. Adds implementation complexity without a
  probe asking for it. Deferred as OQ4.
- **Banding of scheduling predicates.** LT8 currently counts
  globally — Rocky's peripheral-pre `scheduled_fight` at τ_s=-10
  still contributes. No change; the Rashomon utterance events sit
  at τ_s=7 (middle-arc), so banding wouldn't affect them anyway.
- **Back-application to Oedipus / Macbeth.** Oedipus's oracle
  prophecy and Macbeth's witches' prophecies are both plausible
  `prophesied_*` candidates. Neither encoding has a forcing
  function — their DSP_limit declarations are Optionlock, and the
  prophecies are already handled by identity-resolution / rule-
  emergence signals. OQ3.

## Commitments

### SC1 — Canonical discipline for scheduling utterances

When an utterance event narratively performs a scheduling act —
creating a pending commitment that structurally bears on future
events on the same arc — the author encodes that force as a
world-effect Prop with a scheduling-shape predicate prefix:

```python
E_t_wife_requests_killing = Event(
    id="E_t_wife_requests_killing",
    type="utterance",
    participants={
        "speaker": wife_id,
        "listener": tajomaru_id,
        "target": husband_id,
    },
    τ_s=7,
    effects=(
        world(Prop("requested_killing", (tajomaru_id, husband_id))),
    ),
    ...
)
```

Argument shape: `(agent, target)` — the party asked/scheduled to
perform the action and the party targeted by it. Authors may
extend with additional arguments per encoding context; LT8's
detection is prefix-based and argument-shape-agnostic.

The discipline applies regardless of whether LT8 will ultimately
fire on the event — the encoding authoring act is "surface the
speech-act force as typed fact." Whether the resulting Prop
contributes to an LT9-strong verdict is a downstream classifier
concern, not an authoring concern.

Rocky's encoding already follows this pattern with `scheduled_fight`
Props at the `E_apollo_schedules_mac` and `E_apollo_selects_rocky`
scheduling-type events. SC1 makes the pattern general.

### SC2 — LT8 prefix-recognition extension

The recognized scheduling-prefix set becomes:

```python
SCHEDULING_PREFIXES: frozenset = frozenset({
    "scheduled_",
    "requested_",
})
```

Any Prop whose predicate starts with any recognized prefix
contributes to LT8's count. Match is case-sensitive at string
position 0.

Narrative force per prefix:

- **`scheduled_*`** — objective/external schedule; unconditional
  until retracted. Rocky's model. The schedule exists as a fact in
  the story-world's shared knowledge.
- **`requested_*`** — subjective, one-party scheduling act;
  structurally force-carrying via the speech-act itself. Contingent
  on target acceptance but narratively sets the arc in motion.
  Rashomon's bandit/samurai model.

Both fire LT9. The distinction is preserved in classifier output
(SC3) for verifier-comment clarity; it does not differentiate
verdict strength in sketch-01 (deferred to OQ4).

### SC3 — Classifier output extension

`classify_arc_limit_shape_strong` gains one additive output field:

```python
{
    ...
    "scheduling_signals_tuple": (...),   # existing, unchanged
    "scheduling_count": int,             # existing, unchanged
    "scheduling_prefixes": {             # NEW (SC3)
        "scheduled_": (Prop, Prop, ...),
        "requested_": (Prop, ...),
    },
    ...
}
```

`scheduling_signals_tuple` and `scheduling_count` remain
unchanged — flat across prefixes, same contract as sketch-02.
`scheduling_prefixes` is additive; sketch-02-only callers ignore
it. The dict maps each matched prefix (exact string key) to the
tuple of Props carrying that prefix. Prefixes with zero matches in
this call are omitted (empty-tuple values discouraged).

The `dsp_limit_characterization_check` verifier-comment extends to
reference the prefix breakdown when more than one prefix has
matches — e.g., "LT8 signals: 1 scheduled_, 1 requested_". Single-
prefix cases retain the sketch-02 comment shape.

### SC4 — Rashomon worked case

The bandit and samurai testimony branches each contain the same
structural utterance event (τ_s=7, type=utterance, speaker=wife,
listener=tajomaru, target=husband, 0 effects). SC4 adds a single
world-effect to each event:

```python
# prototype/rashomon.py, bandit branch (B_TAJOMARU scope)
E_t_wife_requests_killing = Event(
    id="E_t_wife_requests_killing",
    type="utterance",
    τ_s=7,
    branch=B_TAJOMARU,
    participants={
        "speaker": wife_id,
        "listener": tajomaru_id,
        "target": husband_id,
    },
    effects=(
        world(Prop("requested_killing", (tajomaru_id, husband_id))),
    ),
    ...
)

# Samurai branch (B_HUSBAND scope)
E_h_wife_requests_killing = Event(  # structurally identical
    ...same effects structure...
)
```

Arguments `(tajomaru_id, husband_id)` — who is being asked to do
what to whom. Not `(wife_id, tajomaru_id)` — the first argument is
the action-performer, not the speech-act-agent. This keeps
consistency with Rocky's `scheduled_fight(a, b)` where `(a, b)` are
the fight's participants, not the scheduler.

Wife and woodcutter testimonies are NOT modified under SC4. Their
respective probe-flagged events fall outside scheduling-act-
utterance shape (wife: non-utterance action; woodcutter: goading
rather than request).

### SC5 — Named out-of-scope findings

OQ1 (`provoked_*`) and OQ2 (`situational_forcing`) are named below
rather than absorbed, to keep the sketch narrow without silently
dropping the findings. The post-LT12 probe's four observations
become: two closed here (bandit, samurai); two banked as named OQs
(woodcutter, wife).

## Worked cases — measurements prediction

### Rashomon bandit testimony

Before SC4:
- middle_arc_kinds (restricting): 0 (sketch-03 LT12a excludes
  `bound_to` retraction at τ_s=8 as enabling)
- scheduling_count: 0
- LT14 verdict: NOTED 0.5 (Timelock-declared, no LT8, no
  restricting middle-arc → LT3 weak fallback)

After SC4:
- middle_arc_kinds (restricting): 0 (unchanged)
- scheduling_count: **1** (`requested_killing(tajomaru, husband)`
  at τ_s=7)
- LT9 strong predicate: scheduling_count ≥ 1 AND middle_arc_kinds
  == 0 → fires
- LT14 verdict: **APPROVED, strength `min(1.0, 1/2.0) = 0.5`**

Verdict assessment shift: NOTED 0.5 → APPROVED 0.5. Same numerical
strength; different assertion polarity (substrate-confirms vs.
substrate-consistent-with).

### Rashomon samurai testimony

Same shape as bandit: 0 → 1 scheduling Prop; NOTED 0.5 → APPROVED
0.5.

### Rashomon wife testimony

No change. `E_w_tajomaru_leaves` is an action event, not an
utterance; sketch-01 does not author a scheduling-shape Prop
there. OQ2. Stays NOTED 0.5.

### Rashomon woodcutter testimony

No change. `E_wc_wife_goads` is an utterance but a goading, not a
request. OQ1. Stays NOTED 0.5.

### Post-SC4 testimony verdict spread

| Testimony | Pre-SC4 | Post-SC4 | Shift |
|---|---|---|---|
| Bandit | NOTED 0.5 | APPROVED 0.5 | ✓ |
| Samurai | NOTED 0.5 | APPROVED 0.5 | ✓ |
| Wife | NOTED 0.5 | NOTED 0.5 | — (OQ2) |
| Woodcutter | NOTED 0.5 | NOTED 0.5 | — (OQ1) |

Note the re-introduction of across-sibling verdict asymmetry —
sketch-03 closed the first asymmetry finding as an LT2-detector
artifact; sketch-01's asymmetry is **substantive** and tracks a
real narrative distinction. Two testimonies carry explicit speech-
act scheduling force (wife's verbal request to kill); two do not
(wife's situational entrapment; dual-party goading). The
asymmetric verdicts honestly report that the four testimonies make
the Timelock claim on structurally different grounds.

### Rocky / Oedipus / Macbeth / Ackroyd

All unchanged. Rocky's existing `scheduled_fight` Props use the
unchanged `scheduled_` prefix and land in `scheduling_prefixes
["scheduled_"]`; LT9-strong verdict preserved. The three
Optionlock encodings have zero Props matching either prefix;
sketch-01 is silent for them.

## Implementation brief

Concrete changes, in order of landing:

1. **Extend `SCHEDULING_PREFIXES` in `verifier_helpers.py`.**
   Replace the existing `"scheduled_".startswith(...)` call site
   with iteration over the frozenset. One location (sketch-02's
   line 516 per the research pass).

2. **Populate `scheduling_prefixes` output dict** in
   `classify_arc_limit_shape_strong`. Additive dict construction;
   no removals from existing output.

3. **Extend `dsp_limit_characterization_check` comment formatter**
   to reference the prefix breakdown when more than one prefix has
   matches. Single-prefix path retains sketch-02's comment.

4. **Update `rashomon.py`** — add `world(Prop("requested_killing",
   (tajomaru_id, husband_id)))` to `E_t_wife_requests_killing`
   and `E_h_wife_requests_killing` effects tuples. Two character
   bindings; verify arg construction matches encoding conventions
   for character ids.

5. **Update `rashomon_dramatica_complete_verification.py`
   docstring** to reference SC2/SC4 and the predicted bandit /
   samurai verdict shifts.

6. **Test updates.**
   - `test_verification.py`: add cases pinning `requested_*`
     prefix recognition; pin the `scheduling_prefixes` output
     shape.
   - `test_rashomon.py`: assert the new APPROVED 0.5 verdicts on
     bandit and samurai; assert wife and woodcutter stay NOTED
     0.5.
   - Rocky / Macbeth / Oedipus / Ackroyd: verify unchanged.

7. **Re-run the probe** against Rashomon post-implementation.
   Expectation: 5 endorses (all four testimony commentaries shift
   toward endorse; bandit and samurai around the now-adopted
   `requested_*` vocabulary; wife and woodcutter qualify
   bar-raising around the now-banked OQ1/OQ2). If the probe
   qualifies on sketch-01's shape itself (e.g., argues for
   per-prefix strength weighting), that's the next arc's starting
   point.

## Discipline

Sketch-01 is a narrow extension of sketch-02's LT8 signal
vocabulary, closing half of a four-point probe finding without
reaching for the other half. The two closed qualifications
(bandit, samurai) share one structural shape; the two open
qualifications (wife, woodcutter) share neither that shape nor
each other's. Forcing all four into one sketch would either
invent machinery (structural inference for action-shape forcings;
dual-party goading prefix) without an encoding pressing for it, or
broaden `requested_*` to cover cases it doesn't fit.

Author-opt-in via typed Prop keeps the authorial accountability
clear: the encoding author is naming each utterance that carries
structural scheduling force. The verifier does not guess. This
mirrors sketch-03's LT13 (`affordance_*` prefix for effect_count=0
foreclosures) — both are authorial vocabularies the verifier
recognizes, not structural inferences.

The asymmetry that sketch-01 introduces across Rashomon testimonies
is a feature, not a bug. State-of-play-01's substrate-asymmetry
finding was an LT2-detector artifact (sketch-03 absorbed it). The
sketch-01 asymmetry is substantive — the four testimonies
structurally differ in whether they surface speech-act scheduling
force, and the verdict spread tracks that difference honestly.

## Open questions

**OQ1 — `provoked_*` prefix for goading events.** Rashomon's
woodcutter branch features `E_wc_wife_goads` (τ_s=7, type=
utterance, dual-listener — wife goads both tajomaru AND husband
into fighting). Structurally this is not a one-way request; it's
closer to a challenge or provocation that puts pressure on both
parties at once. Probe-suggested predicate: `provoked_*`. Not
committed in sketch-01 because:
- One encoding exercising the shape isn't enough to ratify a new
  prefix (same threshold as SC2's `requested_*`, which DOES have
  two independent branches exercising it across bandit and samurai
  testimonies).
- A `provoked_*` Prop would likely carry three arguments (goader,
  provoked_party_a, provoked_party_b) rather than two, widening
  the argument-shape convention.
- The goading could alternatively be encoded as two `requested_*`
  Props (one per listener); whether that honestly captures the
  semantics is an authoring question, not a verifier question.

Revisit when a second encoding surfaces a goading-shaped
scheduling act.

**OQ2 — `situational_forcing` for non-utterance events.** The
Rashomon wife branch's `E_w_tajomaru_leaves` is an **action**
event (not an utterance) whose structural effect is to force the
next scene — the wife alone with her husband, leading to the
killing. Probe-suggested predicate: `situational_forcing`.

This is outside utterance-scheduling territory. Resolving it
requires either (a) broadening SCHEDULING_PREFIXES to cover
action-shape forcings — which widens the sketch's frame
considerably — or (b) a separate sketch on situational-forcing
detection. Deferred.

Interim note: authors of any encoding can author a `scheduled_*`
or `requested_*` Prop on a non-utterance event today — the prefix
recognition is event-type-agnostic. SC1's discipline is
"utterance-carried scheduling force"; the broader "action-carried
structural forcing" isn't discipline-committed here but also
isn't forbidden. An encoding that wants to surface the wife
branch's τ_s=7 shift as a `scheduled_*` Prop can do so under
existing LT8 without waiting for OQ2 resolution.

**OQ3 — `prophesied_*` prefix for Oedipus / Macbeth.** Both
encodings carry prophecy events at or before the positive arc
start — Oedipus's oracle at τ_s=-49, Macbeth's witches at τ_s=0
and τ_s=10. Under SC1's discipline, these are plausible
`prophesied_*` schedulings. Neither encoding has a forcing
function: their DSP_limit declarations are Optionlock (not
Timelock), their current DSP_limit verdicts are APPROVED 0.67
under sketch-02's LT10 disposition, and the prophecies are
already handled by identity-resolution (Oedipus's anagnorisis) /
rule-emergence signals. No pressure to add `prophesied_*` now.
Banked for future encoding work — the first encoding whose
Timelock declaration rests on prophecy-as-schedule is where this
prefix earns its keep.

**OQ4 — Per-prefix LT9 strength weighting.** Should `requested_*`
contribute less to LT9 strength than `scheduled_*`? Narratively
defensible: requests are contingent on target acceptance;
schedules are unconditional. A weighted model would compute
`weighted_count = 1.0 × scheduled_count + w_req × requested_count`
with `w_req < 1.0`. Adds implementation complexity; changes
Rocky's APPROVED 1.00 proportionally if Rocky ever adopts a
`requested_*` Prop (which it doesn't today). Deferred pending
either a probe observation or a corpus with a single encoding
exercising both prefixes at once.

## Summary

Sketch-01 codifies Rocky's existing scheduling-Prop pattern as
general discipline (SC1) and extends LT8's prefix-recognition
(SC2) and classifier output (SC3) to cover one additional
vocabulary, `requested_*` — enough to close the bandit and samurai
probe qualifications from the post-LT12 Rashomon run. The two
testimony DSP_limit verdicts are predicted to shift NOTED 0.5 →
APPROVED 0.5 after adding two `requested_killing` Props to the
existing Rashomon encoding. Rocky / Macbeth / Oedipus / Ackroyd
verdicts all predicted unchanged.

Verifier-local vocabulary extension only. No substrate changes, no
new record types. Two separate probe findings (`provoked_*`
goading; non-utterance `situational_forcing`) and two banked
prefix extensions (`prophesied_*`; per-prefix strength weighting)
stay open as OQs.
