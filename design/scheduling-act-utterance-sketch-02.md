# Scheduling-act utterance — sketch 02

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (amendment to sketch-01; SC1–SC5 unchanged)
**Frames:** [scheduling-act-utterance-sketch-01](scheduling-act-utterance-sketch-01.md), [pressure-shape-taxonomy-sketch-01](pressure-shape-taxonomy-sketch-01.md) / [-02](pressure-shape-taxonomy-sketch-02.md) / [-03](pressure-shape-taxonomy-sketch-03.md)
**Related:** `prototype/reader_model_rashomon_post_sc4_output.json` (probe seed source), `rashomon_lowerings.py` (`L_wife_violated`), `rocky_lowerings.py` (`S_ice_skating`)
**Superseded by:** nothing yet

## Purpose

Close the **OQ2-reshaped** scheduling-act-family seed carried
forward since state-of-play-04 — *flag Timelock-declared stories
where the narrative's temporal driver is identified in a Lowering
annotation as "prose-carried" but absent from the event model*.

Sketch-01 closed two of the post-LT12 probe's four findings (bandit
+ samurai) via the `requested_*` prefix extension. Three findings
banked forward. The post-SC4 probe re-emerged with finer-grained
reshapings of the three, of which **OQ2-reshaped** supplied the
concrete actionable signal: the word "prose-carried" appearing in
a Lowering's annotation text.

Sketch-02 is a narrow commentary-layer extension. No verdict shift;
no strength shift; no new record. The NOTED-consistent-with-weak-
fallback verdict stays NOTED 0.5 (per sketch-01's LT3 honest
asymmetry); the comment gains a suffix specializing the diagnostic
when a prose-carried driver is present in the scope's lowerings.

## Context

Rashomon's wife testimony declares `DSP_limit=Timelock`. Under
sketch-01 after SC4, the bandit and samurai testimony branches
shifted NOTED 0.5 → APPROVED 0.5 via authored `requested_killing`
Props. The wife branch did not: her narrative's temporal driver —
"the husband's gaze of contempt" — is carried in the Lowering
annotation (`L_wife_violated.annotation.text`: *"the husband's
gaze of contempt is not modeled as a substrate event … it is
prose-carried"*) rather than as a substrate event with
scheduling-prefix predicates.

The post-SC4 probe flagged this precisely:

> "the wife's Timelock driver exists in the narrative but is
> representationally absent from the substrate. Consider flagging
> Timelock-declared stories where the narrative's temporal driver
> is identified in a Lowering annotation as 'prose-carried' but
> absent from the event model — this is a stronger signal than
> generic 'no scheduling predicate found' and points to a specific
> representational gap."

State-of-play-04 reshaped sketch-01's OQ2 into a concrete signal:
*flag-Timelock-declared-stories-whose-driver-is-Lowering-identified-
as-prose-carried*. Five state-of-play docs (04–08) carried the seed
forward; state-of-play-10 (2026-04-19) named it as a research-track
small-arc candidate for sketch-11 work.

## What the probe proposed (reminder)

Two probe observations in `reader_model_rashomon_post_sc4_output.
json` frame the OQ2-reshaped seed:

1. **vr_2 (wife testimony).** `"the wife's account has a clear
   temporal driver — the husband's gaze of contempt — that is
   acknowledged as prose-carried and not event-modeled (per
   L_wife_violated's annotation). If this gaze were modeled as an
   event (e.g., type 'provocation' with a target effect on the
   wife's state), it would function as a scheduling predicate
   analogous to the 'requested_killing' events."`
2. **Suggested signature.** *"Consider flagging Timelock-declared
   stories where the narrative's temporal driver is identified in
   a Lowering annotation as 'prose-carried' but absent from the
   event model — this is a stronger signal than generic 'no
   scheduling predicate found' and points to a specific
   representational gap."*

The probe framed the check as **comment-layer specialization**, not
verdict change. Sketch-02 honors the framing: the structural reading
is still "consistent-with-Timelock, not affirmatively detected" —
the verdict contract from sketch-01 LT3 stands. What changes is the
diagnostic's specificity.

## What this sketch commits to

- [**SC6**] Authorial vocabulary token. The substring
  `"prose-carried"` appearing anywhere in a Lowering's
  `annotation.text` declares: *"this Lowering names a narratively
  load-bearing driver not modeled in substrate."* The token is
  plain prose; exact-case substring match (`"prose-carried"` —
  with hyphen). Authors opt in by writing the token; the verifier
  recognizes.

- [**SC7**] `dsp_limit_characterization_check` signature extension.
  A new optional kwarg `lowerings: tuple = ()` is added. When the
  default empty-tuple is passed (pre-sketch-02 callers), behavior
  is identical to sketch-01. When a non-empty tuple is passed, the
  scan fires per SC8.

- [**SC8**] Comment specialization at `timelock-consistent`. When
  `declared_choice=timelock` AND `classification=timelock-
  consistent` (the NOTED weak-fallback path, strength None) AND
  any Lowering in the threaded `lowerings` tuple carries
  `"prose-carried"` in its `annotation.text`, the verdict comment
  gains a trailing sentence naming the Lowering id(s) and pointing
  at the representational gap. Verdict stays `VERDICT_NOTED`;
  strength stays `None`.

- [**SC9**] Rashomon worked-case threading.
  `rashomon_dramatica_complete_verification.py`'s
  `_run_testimony_dsp_limit_check` helper threads the
  `LOWERINGS_BY_STORY[story_id]` tuple through to the helper. All
  four testimonies pass their per-Story lowering subset; only
  `S_wife_ver` has a prose-carried annotation in its subset and
  surfaces the specialized comment.

- [**SC10**] Scope boundary: what sketch-02 does NOT commit to.
  - No verdict-strength lift. A prose-carried driver is a
    structural absence from the substrate; the declaration remains
    consistent-but-not-affirmed. Verdict stays NOTED None.
  - No extension to the Optionlock path. The prose-carried signal
    is a Timelock-specific diagnostic per the probe's framing
    (non-scheduling temporal drivers in Timelock-declared works).
  - No schema-layer addition. A typed `Annotation.is_prose_carried`
    boolean would be port-friendlier but is premature; the
    substring-token approach matches the authorial prose without
    a schema change. Banked (OQ7).
  - No cross-dialect scan. Only Lowering annotations are checked.
    Dramatic Scene annotations, Dramatica Story annotations, and
    Aristotelian phase annotations are out of scope.
  - No back-application to the **bandit-refinement** or
    **OQ1-reshaped (woodcutter)** seeds. Each has its own distinct
    forcing function per sketch-01's OQ1 and state-of-play-04's
    "bandit refinement" banking. Neither fits the prose-carried
    annotation signal.

## Worked cases — measurements prediction

### Rashomon — S_wife_ver (Timelock declared)

Before SC7/SC8:
- classification: `timelock-consistent` (no restricting middle-arc
  LT2 signals; no scheduling predicate)
- verdict: `NOTED`, strength `None`
- comment: *"DSP_limit=Timelock declared; substrate shows no
  restricting middle-arc LT2 convergence signals AND no scheduling
  predicate (LT8). Consistent with Timelock but not affirmatively
  detected — LT3's honest weak-fallback asymmetry (sketch-01).
  Consider naming the scheduled endpoint with a `scheduled_*`
  predicate to fire LT9."*

After SC7/SC8 (when `LOWERINGS_BY_STORY[S_wife_ver.id]` threaded):
- classification: `timelock-consistent` (unchanged)
- verdict: `NOTED`, strength `None` (unchanged)
- comment: prior text + new suffix naming the L_wife_violated
  annotation as the prose-carried driver signal and describing
  the representational gap.

Verdict polarity + strength unchanged. Comment newly names the
specific representational gap.

### Rashomon — S_bandit_ver / S_samurai_ver (Timelock declared)

LT9 affirmatively detects Timelock shape (classification=`timelock-
strong` via SC4's `requested_killing`). The new code path (at
`timelock-consistent`) is not entered. No comment change.

### Rashomon — S_woodcutter_ver (Timelock declared)

classification=`timelock-consistent` (same as wife's). The
woodcutter's in-scope lowerings (per LOWERINGS_BY_STORY) do NOT
contain "prose-carried" in their annotation text. The new suffix
is not appended. Comment unchanged from sketch-01.

### Rocky (Timelock declared)

Rocky's `L_ice_skating` annotation does contain "prose-carried"
text, but Rocky's DSP_limit check hits `classification=timelock-
strong` (`scheduled_fight` fires LT8/LT9). The new code path
(timelock-consistent) is not entered. Rocky's comment unchanged.

### Oedipus / Macbeth / Ackroyd (Optionlock declared)

Optionlock path unchanged per SC10. No new suffix.

### Post-SC7/SC8 verdict spread

| Encoding.Story | Pre-SC7 | Post-SC7 | Shift |
|---|---|---|---|
| Rashomon.S_wife_ver | NOTED None | NOTED None + prose-carried suffix | comment-only |
| Rashomon.S_bandit_ver | APPROVED 0.5 | APPROVED 0.5 | — |
| Rashomon.S_samurai_ver | APPROVED 0.5 | APPROVED 0.5 | — |
| Rashomon.S_woodcutter_ver | NOTED None | NOTED None | — |
| Rocky.S_rocky | APPROVED 1.00 | APPROVED 1.00 | — |
| Oedipus / Macbeth / Ackroyd | all paths | all paths | — |

No verdict-polarity or strength shift in any encoding. The
wife-branch test gains a specialized comment.

## Implementation brief

In order of landing:

1. **Add helper** in `verifier_helpers.py`:
   `_prose_carried_lowerings(lowerings: tuple) -> tuple[Lowering, ...]`
   Scans each Lowering's `annotation.text` for the substring
   `"prose-carried"`. Returns the subset with the substring
   present. Empty input → empty output. Non-string annotation
   field → skipped (defensive).

2. **Extend** `dsp_limit_characterization_check`:
   - New kwarg: `lowerings: tuple = ()`.
   - In the `timelock-consistent` branch of the `timelock`
     declared path, after constructing the base comment, call the
     new helper. If the helper returns non-empty, append the
     specializing suffix. Otherwise emit the base comment
     unchanged.
   - Suffix shape: *" Lowering annotation(s) {id_list}
     identify prose-carried temporal driver(s) not modeled in
     substrate — a specific representational gap per OQ2-reshaped."*
     Where `{id_list}` is the comma-separated Lowering ids with
     prose-carried annotations (typically one; the spec admits
     multiple).

3. **Thread** in
   `rashomon_dramatica_complete_verification.py`:
   `_run_testimony_dsp_limit_check(story_id, canonical_scope_branch)`
   passes `LOWERINGS_BY_STORY[story_id]` (already imported) to
   the helper via the new kwarg.
   (No other verifier modules use `dsp_limit_characterization_check`
   today with a path that would enter the new branch — defensively,
   leave them unchanged.)

4. **Tests** in `test_verification.py`:
   - Pin that `_prose_carried_lowerings(())` returns `()`.
   - Pin that `_prose_carried_lowerings((synthetic_prose_carried,))`
     returns the synthetic.
   - Pin that `_prose_carried_lowerings((synthetic_without_token,))`
     returns `()`.
   - Pin that the helper is substring-match (not whole-word): text
     `"prose-carried."` (with period) matches; text
     `"authorially-carried"` does not.
   - Pin that `dsp_limit_characterization_check` with `lowerings=()`
     produces the pre-sketch-02 comment exactly.
   - Pin that `dsp_limit_characterization_check` with
     `lowerings=(synthetic_prose_carried,)` on a Timelock-declared
     fabula producing `timelock-consistent` classification emits
     a comment ending with the SC8 suffix naming the synthetic id.
   - Pin that threading the same `lowerings` through a `timelock-
     strong` classification (scheduling-predicate present) does
     NOT add the suffix.
   - Pin that threading the same `lowerings` through an Optionlock
     declaration does NOT add the suffix.

5. **Tests** in `test_rashomon.py`:
   - Pin S_wife_ver's DSP_limit verdict is NOTED None (unchanged).
   - Pin S_wife_ver's DSP_limit comment contains the substring
     `"prose-carried"` after SC9 threading (or equivalent marker
     text from SC8's suffix).
   - Pin S_bandit_ver / S_samurai_ver's DSP_limit verdicts are
     APPROVED 0.5 (unchanged; the SC8 suffix must not appear).
   - Pin S_woodcutter_ver's verdict stays NOTED None with no SC8
     suffix (no prose-carried annotation in its scope).

6. **No schema change.** Annotations remain plain-text; the
   sketch-02 discipline is authorial vocabulary recognition, not
   a shape change. `schema/lowering/lowering.json`'s `annotation`
   sub-schema admits any string; this sketch does not touch it.

7. **No new design records.** No sketch-11 candidate landings.

## Discipline

Sketch-02 is a deliberately narrow closure — one new helper, one
optional kwarg, one worked-case threading, one specializing suffix.
The four out-of-scope items (OQ1/woodcutter; bandit-refinement;
Optionlock path; schema-layer typing) are banked with their own
forcing-function criteria, not merged in. Same scope-discipline as
sketch-01's SC5 reservations.

The substring-match is pragmatic. A typed boolean on `Annotation`
would be more robust to port-translation and to authors writing
stylistic variations ("prose only", "prose carried", "not modeled
in substrate"). But the probe's signal was *"prose-carried"*
specifically; authors already write this token; adding a schema
field preemptively would be speculative. When a second author
writes the token in a different encoding and the probe re-surfaces
a variant phrasing, OQ7 becomes forcing.

The no-verdict-shift stance preserves the sketch-01 LT3 contract:
"consistent but not affirmatively detected" is the honest verdict
for a Timelock with no substrate scheduling signal, whether or not
the Lowering names a prose-carried driver. The prose-carried signal
specializes the diagnostic; the verdict stays at the weak-fallback
strength. An alternative — lift NOTED to NOTED 0.5 with a
strength-carrying number — was considered and rejected: inventing
a numeric strength for a pure comment-layer signal would drift the
verdict-strength contract without earning it.

The **post-SC7/SC8 probe re-run is banked**, not committed in
sketch-02. If a future probe arc on the updated Rashomon output
finds the wife-branch specialized comment insufficient ("asks for
an 'annotation-read' / 'gaze' / 'provocation' substrate event
model"), that seed opens a new arc. Sketch-02 does not promise
probe-satisfaction; it promises a verifiable specialization of the
wife-branch diagnostic.

## Open questions

**OQ5 — Cross-branch scope handling.** Today the caller
(`_run_testimony_dsp_limit_check`) passes `LOWERINGS_BY_STORY
[story_id]`, which already contains the story's own scope-
relevant lowerings. The helper does not re-filter by branch. If a
lowering whose scope overlaps multiple testimony branches carries
"prose-carried", every testimony seeing it via LOWERINGS_BY_STORY
gets the suffix. In Rashomon today no shared lowering carries
"prose-carried" (L_wife_violated is wife-only); the asymmetry is
theoretical. Forcing: a future encoding where a prose-carried
annotation spans branches.

**OQ6 — Multiple prose-carried Lowerings in one story.** The
SC8 suffix names all matching Lowering ids. If an encoding
authors 5 prose-carried lowerings, the suffix names 5 ids. The
comment is verbose but faithful. Deferred as a future cosmetic
question if comments accumulate.

**OQ7 — Typed `Annotation.is_prose_carried` boolean.** Schema-
layer alternative to substring matching. Would be clean for port
work and for authors writing stylistic variations. Banked. Forcing:
a second encoding author writes a prose-carried-semantic
annotation with a different spelling OR the port work surfaces
substring-matching as fragile.

**OQ8 — Other annotation-carried diagnostics.** "Prose-carried"
is one of potentially many authorial vocabulary tokens that could
specialize verifier diagnostics. `"narratively-elided"`,
`"implicit-only"`, `"author-asserted"` are plausible. Banked as
an authorial-vocabulary extension point if sketch-03 or a future
sketch finds a second token worth recognizing.

**OQ9 — Post-sketch-02 probe re-run outcome.** Banked. If
re-running the post-SC4 probe against the sketch-02 Rashomon
verifier produces the expected "endorse" on the wife-branch and
the bandit-refinement / woodcutter-cross-branch seeds stay
qualified, sketch-02 has closed OQ2-reshaped cleanly. If the
probe asks for a `gaze_of_contempt`-shaped substrate event
(Path B from sketch-01's design discussion, now finer-grained),
that's a new arc's starting point.

## Summary

Sketch-02 closes the OQ2-reshaped scheduling-act-family seed by
codifying `"prose-carried"` as authorial vocabulary in Lowering
annotation text (SC6) and extending
`dsp_limit_characterization_check` (SC7) with a Timelock-
consistent-path specializing suffix (SC8). Rashomon's wife
testimony DSP_limit comment gains the specialized diagnostic;
all other verdicts and strengths across the corpus are
unchanged. No schema change, no record type addition, no LT9
strength re-tuning.

Two of three banked post-SC4 seeds remain (bandit-refinement;
OQ1-reshaped woodcutter cross-branch signature) with their own
forcing functions. Sketch-02 does not reach for them.

Verifier-local vocabulary extension only. Same pattern as
sketch-01's SC1/SC2 (author-opt-in via prose token) but applied
to comment-layer specialization rather than LT8 signal firing.
