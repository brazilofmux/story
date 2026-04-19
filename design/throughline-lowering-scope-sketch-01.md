# Throughline-lowering scope — sketch 01

**Status:** draft, active
**Date:** 2026-04-18
**Supersedes:** nothing
**Frames:** [architecture-sketch-02](architecture-sketch-02.md) (the
dialect stack, grid-snap), [multi-story-sketch-01](multi-story-sketch-
01.md) (multi-Story Lowerings per MS5)
**Related:** [lowering-record-sketch-01](lowering-record-sketch-01.md);
[dramatic-sketch-01](dramatic-sketch-01.md) (Throughline.subject, M5);
`prototype/story_engine/encodings/rashomon_lowerings.py`
(`L_bandit_mc_throughline`, `L_wife_mc_throughline` — the two worked
cases); post-SC4 Rashomon probe JSON
(`prototype/reader_model_rashomon_post_sc4_output.json`, commit
`72dfdbe`)
**Superseded by:** nothing yet

## Purpose

Close two NEEDS_WORK annotation-review findings from the post-SC4
Rashomon probe (2026-04-18):

- `L_bandit_mc_throughline` — Throughline subject names
  "the seduction" (realized by canonical-floor events `E_lure`,
  `E_bind`, `E_bring_wife`, `E_intercourse` at τ_s=2..5) but the
  Lowering's `lower_records` scope to three B_TAJOMARU branch
  events (τ_s=7..9).
- `L_wife_mc_throughline` — Throughline subject names "violation"
  (realized by canonical-floor `E_intercourse` at τ_s=5) but the
  Lowering's `lower_records` scope to two B_WIFE branch events
  (τ_s=7..10).

Both findings expose the same structural gap: the scoping
principle the author applied (branch-scoped Throughline Lowerings,
with canonical-floor events carrying per-testimony reading via
Descriptions) exists as a Python comment in `rashomon_lowerings.py`
(lines 500-503), but is not visible to the verifier or the probe —
it's absent from the Lowering's `annotation.text`.

The probe's two-option recommendation ("include the canonical
events OR state the scoping principle") admits either a schema
change or an author-discipline commitment. This sketch picks the
second: codify the scoping principle as dialect-level architecture
and require it be stated explicitly in the annotation when a
Throughline subject names events outside the Lowering's
`lower_records`.

## Why now

- Post-SC4 Rashomon probe's two NEEDS_WORK annotation-review
  findings point at the same scoping gap. First probe-driven
  architectural finding on Throughline Lowering *shape* (prior
  Lowering findings were on substrate / DSP surface via LT / MN
  checks).
- The scoping principle is already in use (in Rashomon; the code
  comment at lines 500-503 names it), but not specified.
  Specification closes the discoverability gap.
- grid-snap discipline (memory: *schema grid-snaps structural
  facts; LLM/human carries the affective/interpretive load*)
  argues that the distinction between "Throughline.subject is
  interpretive" and "Lowering.lower_records is structural" is the
  architecture's existing commitment. Making it explicit for
  multi-Story Throughline Lowerings is a clarification, not a new
  commitment.
- Two worked cases exist concretely; any sketch that can't close
  them is under-specified.

## Context — what the probe saw and didn't see

Both NEEDS_WORK findings share one shape: Throughline subject text
**names content realized by events the Lowering excludes**. The
probe did not see the Python comment at `rashomon_lowerings.py`
lines 500-503:

> "The seduction/violation intercourse event is canonical floor;
> its per-branch reading lives in descriptions, not in the fabula,
> so the MC Throughline's arc-body is on the branch-scoped events
> where the testifier's account diverges."

This comment is correct. It expresses the scoping principle the
author applied to all four testimony Throughline Lowerings. But
it's a *code comment*, not a *record-level annotation*, so the
verifier and probe don't see it.

Two testimony Throughline Lowerings *don't have the gap* — the
probe approved both:

- `L_samurai_mc_throughline` — T_samurai_mc's subject names "his
  wife begging the bandit to kill him; his suicide with her
  dagger" — both realized by B_HUSBAND branch events
  (`E_h_wife_requests_killing` at τ_s=7, `E_h_suicide` at
  τ_s=11). No canonical-floor event named.
- `L_woodcutter_mc_throughline` — T_woodcutter_mc's subject names
  "a messy, cowardly fight; the wife goading both men; the
  woodcutter stealing the dagger" — all B_WOODCUTTER branch
  events. No canonical-floor event named.

All four testimony Throughline Lowerings share the same author-
intended scoping principle. Only the two whose subject-text names
canonical-floor content trip the finding. The probe isolated the
real issue cleanly.

## Commitments

- [**TL1**] **Throughline subject is interpretive; Lowering
  lower_records is structural.** The `Throughline.subject` field
  (dramatic-sketch-01 M5) is the testifier's (or narrator's)
  reading of what the arc is about — it may name any content
  within the testifier's account. The `Lowering.lower_records`
  (lowering-record-sketch-01 L2) names the substrate events the
  arc's dialectic *binds to*. They may legitimately diverge;
  divergence is not a gap.

- [**TL2**] **Branch-scoped Throughline Lowerings are admitted by
  multi-Story.** In a StoryEncoding with branch-contested
  substrate (multi-story-sketch-01 MS5), a testimony Story's
  Throughline Lowering MAY scope its `lower_records` to that
  Story's own branch events, excluding canonical-floor events
  that realize Throughline-subject content via Descriptions rather
  than via substrate-binding. The Throughline still *holds* the
  subject-named content structurally (the canonical-floor event
  exists in the substrate; each testimony's Descriptions on that
  event express the per-branch reading), but the *binding* lives
  at a different scope.

- [**TL3**] **Annotation-explicit scoping.** When a Throughline
  Lowering's subject names content outside its `lower_records`,
  the Lowering's `annotation.text` MUST state the scoping
  principle explicitly: (a) name the subject-named-but-excluded
  content, (b) name the canonical-floor substrate event(s) that
  realize it, (c) name where the per-branch reading lives (the
  specific Description record ids on the excluded substrate
  event), and (d) name the scoping discipline ("branch-scoped per
  TL2"). Author-opt-in; no automated detection in v1 (OQ1).

- [**TL4**] **No schema change.** The existing Lowering record
  shape (lowering-record-sketch-01 L1-L10) is sufficient. No
  typed `scope_mode` field; no `subject_events_outside_scope`
  field. Per enabling-retraction-preservation-sketch-01's
  discipline ("add durable surface when a forcing function argues
  for it"), the probe has not argued for a typed field; annotation-
  prose is sufficient to close the finding.

## Worked cases

### L_bandit_mc_throughline (post-TL3)

Current annotation:

> "T_bandit_mc (Tajōmaru's self-account of prowess and noble
> contest) realizes across the three B_TAJOMARU branch events — the
> wife's requested killing that motivates the duel, the unbinding
> that makes a fair fight possible, and the twenty-three-stroke
> duel itself. Arc runs τ_s=7..9."

Post-TL3 annotation (addition in **bold**):

> "T_bandit_mc (Tajōmaru's self-account of prowess and noble
> contest) realizes across the three B_TAJOMARU branch events — the
> wife's requested killing that motivates the duel, the unbinding
> that makes a fair fight possible, and the twenty-three-stroke
> duel itself. Arc runs τ_s=7..9. **Branch-scoped per TL2: the
> subject-named seduction (canonical-floor events `E_lure`,
> `E_bind`, `E_bring_wife`, `E_intercourse` at τ_s=2..5) is shared
> substrate; Tajōmaru's reading of those events as a noble
> seduction lives in `D_intercourse_tajomaru_texture` (Description
> on `E_intercourse`), not in this Lowering's lower_records.**"

### L_wife_mc_throughline (post-TL3)

Current annotation:

> "T_wife_mc (the wife's self-account of violation and a half-
> conscious killing) realizes across the two B_WIFE branch events.
> Arc runs τ_s=7..10."

Post-TL3 annotation (addition in **bold**):

> "T_wife_mc (the wife's self-account of violation and a half-
> conscious killing) realizes across the two B_WIFE branch events.
> Arc runs τ_s=7..10. **Branch-scoped per TL2: the subject-named
> violation is realized by canonical-floor `E_intercourse` at
> τ_s=5; the wife's reading of that event as violation lives in
> `D_intercourse_wife_texture` (Description on `E_intercourse`),
> not in this Lowering's lower_records.**"

### Controls (already-approved Lowerings, no change)

`L_samurai_mc_throughline` and `L_woodcutter_mc_throughline`
require no change — their subject text doesn't name canonical-
floor events, so TL3's "MUST" doesn't trigger. Their approval by
the post-SC4 probe confirms the sketch's trigger condition is
correctly scoped.

The Python comment at `rashomon_lowerings.py` lines 500-503 is
retained — it gives collective context for all four testimony
Throughline Lowerings. TL3 adds per-Lowering statements to the two
Lowerings where the principle is non-obvious; the collective
comment continues to orient the reader at the section level.

## Acceptance criteria

- [TLA1] The two Lowerings' `annotation.text` fields are extended
  as in the worked cases. No other Lowering changes.
- [TLA2] All existing tests continue to pass (no test touches the
  `annotation.text` content substantively; this sketch does not
  add a test because there is no new verifier behavior).
- [TLA3] Commit message references this sketch and cites both
  worked-case Lowerings for traceability.

Post-commit re-probe would close the two NEEDS_WORK findings. The
sketch does not commit to running the re-probe; that's a sketch-04
state-of-play call.

## Not in scope

- **Automated detection of the TL3 trigger condition.** A verifier
  pass that scans Throughline subject text for references to
  substrate-record names or description content overlapping with
  canonical-floor events. OQ1. Would need an NLP-ish match or a
  structured `subject_events` / `subject_references` field on
  Throughline. Defer until a second encoding presents the same
  pattern; `and_then_there_were_none` may be that encoding once
  authored.
- **Scope-mode typed field on Lowering / Annotation.** Rejected
  per TL4. Reopens if a forcing function surfaces — see OQ2.
- **Scene-lowering scope.** The post-SC4 probe approved all
  Rashomon Scene Lowerings (e.g., `L_bandit_seduction`,
  `L_wife_violated`) — they *do* include canonical-floor events
  within their scene window. TL1-TL4 are about Throughline
  Lowerings specifically. Scene Lowerings have a different
  scoping rule (coverage of the declared Scene's content),
  already tacit; promoting it to a commitment would widen the
  sketch beyond the probe-finding scope.
- **Beat-lowering scope.** The corpus has no multi-Story Beat
  Lowerings with this shape yet. Sibling sketch if and when.
- **Retroactive application to single-Story Throughline
  Lowerings** in Oedipus / Macbeth / Ackroyd / Rocky. Those
  encodings don't have canonical-floor-vs-branch-divergent
  structure; TL3's trigger doesn't fire. No action.

## Open questions

1. **Automated trigger detection.** Forcing function: a second
   encoding with the same shape whose author forgets the
   annotation update. Candidates: `and_then_there_were_none` once
   authored (if individual-suspect MC Throughlines are scoped to
   per-suspect events while the ten deaths are shared canonical-
   floor substrate). Until then, author-discipline + reviewer-
   probe is sufficient.
2. **Does the principle generalize to frame Throughlines?** Frame
   Throughline Lowerings in Rashomon are all PENDING (no substrate
   realization — grove-only scope, MS5). If a future encoding has
   an ACTIVE frame Throughline Lowering whose subject names events
   that live inside a testimony-branch, TL3 would need a
   direction-flip. Defer; no forcing case today.
3. **Sketch-02 forcing-function criteria** (mirroring enabling-
   retraction-preservation-sketch-01's discipline): (a) a second
   encoding exhibiting the shape with an author-mistake the probe
   catches; (b) a probe asking for automated detection; (c) a
   typed `scope_mode` consumer appears downstream (e.g., a
   verifier pass that distinguishes per-scope-mode). None holds
   today.

## Summary

Two post-SC4 probe NEEDS_WORK findings on Rashomon testimony
Throughline Lowerings share one cause: the scoping principle the
author applied (branch-divergent events; canonical-floor reading
via Descriptions) lives in a code comment, not in the record-level
annotation. TL1-TL4 codify the distinction between interpretive
subject and structural binding, admit branch-scoped Throughline
Lowerings explicitly, and require per-Lowering annotation text when
the distinction makes a Lowering's scope non-obvious to a cold-
start reader. No schema change, no verifier change, no test change —
two annotation edits close the probe findings. Author-opt-in
discipline consistent with the rest of the post-LT12 sketch arc
(scheduling-act-utterance SC1's Rocky-pattern codification,
enabling-retraction-preservation's explicit deferral).
