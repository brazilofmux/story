# Cross-dialect comparison — Ackroyd — sketch 01

**Status:** draft, active
**Date:** 2026-04-15
**Supersedes:** nothing (new comparison)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md), [dramatic-sketch-01.md](dramatic-sketch-01.md), [save-the-cat-sketch-01.md](save-the-cat-sketch-01.md), [cross-dialect-macbeth-sketch-01.md](cross-dialect-macbeth-sketch-01.md), [ackroyd-sketch-01.md](ackroyd-sketch-01.md)
**Superseded by:** nothing

## Purpose

Second empirical cross-dialect comparison. Where
cross-dialect-macbeth-sketch-01 made the multi-dialect architecture's
pluralism concrete on a pre-modern tragedy, this sketch repeats the
exercise on a 1926 English detective novel — the third encoded
story, deliberately chosen for structural dissimilarity per
REVIEW.md's next-term item #1.

Two new data points the Ackroyd comparison produces:

1. **Whydunit genre-fit on Save the Cat is clean.** Where Macbeth's
   Rites of Passage was the least-bad of ten genres, Ackroyd's
   Whydunit genre was what Snyder designed the genre for. The
   encoding fits without the strains Macbeth required the
   worked-example table to document. The cross-dialect comparison's
   finding: Save the Cat's advertised native-genre fit is real.

2. **Cross-dialect convergence at the finale.** Both dialects'
   verifier checks on the reveal moment exercise the *same four
   signatures* against the *same substrate moment*: Poirot + Caroline
   + Raglan + Flora all holding `killed(sheppard, ackroyd)` at KNOWN
   at τ_s=8. Two dialect vocabularies, one substrate reading — the
   architecture-sketch-02 claim that the substrate is the coordination
   layer becomes concretely visible.

Both self-verifiers run clean on their respective encodings. The
Dramatic dialect produces 0 observations; Save the Cat produces 1
NOTED observation (the informational `genre_archetypes_declared`
print). Both cross-boundary verifiers produce 3 + 4 REVIEWs, all
APPROVED at match_strength=1.0. The clean verifier output on a
narratively complex novel with a famously unreliable narrator is
itself informative — the substrate holds Ackroyd honestly.

## Method

Same as cross-dialect-macbeth-sketch-01. Both encodings of Ackroyd
(`ackroyd_dramatic.py` and `ackroyd_save_the_cat.py`) were authored
against their respective dialect sketches without trying to make the
two encodings parallel. Differences are dialect-driven, not
authorial-preference-driven.

## Record counts

### Dramatic on Ackroyd: 6 record types, 56 records

| Record type | Count | Change vs. Macbeth |
|---|---|---|
| Argument | 1 | same |
| Throughline | 4 | same |
| Character | 12 | +3 (more cast — 12 vs. 9) |
| Scene | 12 | -2 (12 vs. 14) |
| Beat | 23 | -2 (23 vs. 25) |
| Stakes | 4 | same |

### Save the Cat on Ackroyd: 2 authored record types, 17 records

| Record type | Count |
|---|---|
| Strand | 2 (A_case + B_flora_ralph) |
| Beat | 15 (canonical slots, all filled) |

Same 3:1 ratio on the same play that Macbeth's comparison showed.
Cross-encoding: Dramatic's schema demands more authored choices per
encoding; Save the Cat's prescriptive 15-beat skeleton means fewer
decisions are open.

## The central structural finding: Whydunit fits Ackroyd

### Genre archetypes map to authored characters without strain

Save the Cat's Whydunit genre ships three archetypes: *the
detective*, *the secret*, *the dark turn*. Against Ackroyd:

- **the detective** → Poirot. The encoding's genre archetype and
  the Dramatica Protagonist land on the same Character. No
  role-tension.
- **the secret** → Sheppard's blackmail of Mrs. Ferrars + his
  murder of Ackroyd. Two layered secrets; both are authored
  substrate facts the investigation recovers.
- **the dark turn** → the reveal itself, and Poirot's quiet
  ultimatum that ends in Sheppard's suicide. The genre's
  canonically-darkest beat is the novel's actual ending.

By contrast, Macbeth's Rites-of-Passage fit required the
comparison sketch to name the archetypes' fit as *imperfect*:
the-life-problem (ambition), the-wrong-way (murder),
the-acceptance (awareness at death). The mapping held, but strained
against a 17th-century tragedy rather than a 21st-century commercial
screenplay. Ackroyd's Whydunit mapping doesn't strain.

### Beat-slot content maps without compression on one end

The Macbeth comparison identified a compression pattern: Save the
Cat's slot 10 (Bad Guys Close In) collapsed four distinct Dramatic
Scenes into one beat — the dialect's prescriptive ceiling on late
rising action. For Ackroyd, the compression direction inverts:

**Substrate compresses, dialect expands.**

Ackroyd's substrate collapses the novel's long investigation middle
into a single event (`E_poirot_investigates`, τ_s=5). The Save the
Cat dialect reads *four distinct structural beats* within that
event:

| Save the Cat slot | Beat | Substrate event |
|---|---|---|
| 8 | Fun and Games | E_poirot_investigates |
| 9 | Midpoint | E_poirot_investigates (+ E_dictaphone_plays) |
| 10 | Bad Guys Close In | E_poirot_investigates |
| 11 | All Is Lost | E_poirot_investigates |

Four dialect beats bind to one substrate event. The substrate was
authored to compress the procedural middle (the novel itself has
many chapters of interviews; the substrate reads them as one
investigation); the dialect reads the same novel with Save the Cat's
5-point structural arc imposed. The compression direction is exactly
opposite to Macbeth's case.

This bidirectional compression is the *substrate's structural role
becoming empirically visible*: it is neither finer-grained nor
coarser-grained than any dialect a-priori; it is whatever the
authorial encoding chose to stage, and different dialects can read
the same substrate at their own granularity.

### The slot-6 cleanliness

cross-dialect-macbeth-sketch-01 flagged Save the Cat's slot 6
(Break Into Two) as PENDING for Macbeth's Lowering — the commit-to-
kill is an interior moment with no substrate event. Ackroyd's slot
6 is **the detective accepting Flora's commission**
(`E_flora_summons_poirot`), which IS a staged event with substrate
participants. Slot 6 lands ACTIVE for Ackroyd, PENDING for Macbeth.

This is the Whydunit's cleaner structural fit appearing at the
Lowering layer. Save the Cat's 15-beat skeleton implicitly assumes a
protagonist whose commit is visible — a detective's "I take the
case," a hero's quest-beginning, a love-interest's declaration.
Macbeth's protagonist commits inwardly (conscience-to-action);
Ackroyd's commits outwardly. The dialect fits the outward case.

Count of Save the Cat PENDING beats on each encoding:

- **Macbeth**: 4 PENDING (Opening Image, Theme Stated, Break Into
  Two, Dark Night)
- **Ackroyd**: 3 PENDING (Opening Image, Theme Stated, Dark Night)

The difference is slot 6 — which is the structural beat the genre
fit predicted would land cleanly. The count difference is small (1
fewer PENDING), but the *semantics* are the key finding: the PENDING
list tells you what the dialect asked for that the substrate didn't
stage. Fewer PENDINGs on the genre-native case means the dialect's
expectations were met.

## The MC-Antagonist alignment

ackroyd-sketch-01 flagged this as the Dramatic encoding's structural
thesis: C_sheppard carries the Antagonist function slot and owns
T_mc_sheppard (the main-character Throughline). Dramatica admits the
alignment; the encoding exercises it for the first time.

The Macbeth comparison sketch's open question was "should Save the
Cat acquire a Character record type?" — jarring because Macbeth's
Save the Cat encoding names zero Characters. Ackroyd's STC encoding
names zero Characters too. But the Dramatic encoding's MC-Antagonist
alignment gives us the clearest test of whether the gap matters:

- At Dramatic: Sheppard is C_sheppard; his function_labels=
  ("Antagonist",); he owns T_mc_sheppard; his Entity lowering is
  L_sheppard → substrate 'sheppard'. Everything is explicit.
- At Save the Cat: Sheppard is... a person referenced in beat
  descriptions. No StcCharacter. No function label. No verification
  check can reach him. The strands' verification checks pull
  substrate events' participant sets directly — the dialect does
  not expose Sheppard-as-role to the verifier.

This makes the Save the Cat Character gap more visible on Ackroyd
than on Macbeth: Ackroyd's entire novel pivots on *which character
is the killer*, and the Save the Cat dialect cannot express that at
all. The Dramatic encoding makes killed(sheppard, ackroyd)'s
structural claim visible through the Antagonist function slot on
C_sheppard. The Save the Cat encoding carries the same claim only
through the bound substrate events.

**Tentative conclusion**: the Save the Cat Character gap, flagged as
an open question after Macbeth, is pressed harder by Ackroyd.
Not-yet-a-sketch-amendment — the dialect may still be correctly
narrow and the role content may belong entirely substrate-side — but
the encoding experience suggests the gap is real. A future
save-the-cat-sketch-02 amendment admitting a minimal StcCharacter
record with role-labels (detective / suspect / victim / narrator)
would bring the dialect closer to how the framework is practically
used.

## Theme-statement convergence

Both dialects name Ackroyd's thematic claim:

- **Dramatic**: A_truth_recovers's `premise` = "the truth about a
  deed committed in concealment can be recovered by patient
  reasoning from what the concealer cannot hide"
- **Save the Cat**: Story's `theme_statement` = "The truth will
  out."

Same claim, two vernaculars. The Dramatic form is the thesis stated
analytically (with counter-premise); the Save the Cat form is the
canonical one-liner a screenwriter would put on a pitch page.
Macbeth's comparison flagged this pattern (Dramatic's Argument vs.
Save the Cat's Theme Stated as possibly-shared-underlying-type);
Ackroyd confirms the pattern holds.

The implication: a future dialect normalization could carry both
forms (literal line + underlying thesis) as one record with two
fields. Deferred until a third genre surfaces further pressure.

## Verifier-surface convergence at the finale

**The central empirical result of this comparison**: the Dramatic
and Save the Cat cross-boundary verifiers test the *same four
signatures* against the *same substrate moment* (τ_s=8,
E_poirot_reveals_solution):

1. Poirot holds killed(sheppard, ackroyd) at KNOWN
2. Caroline holds killed(sheppard, ackroyd) at KNOWN
3. Inspector Raglan holds killed(sheppard, ackroyd) at KNOWN
4. Flora holds killed(sheppard, ackroyd) at KNOWN

Dramatic's `poirot_reveal_scene_result_check` and Save the Cat's
`finale_beat_moment_check` execute the identical four probes at
the same τ_s. Both produce APPROVED at match_strength=1.0.

The prediction from cross-dialect-macbeth-sketch-01 was:

> two dialects reading the same substrate moment should produce
> checks of the same shape when both describe the same event-set.

Ackroyd confirms this. When two dialects name the same substrate
event as their claim-moment, their verifier checks converge to the
same substrate probes — because the substrate is what the claims
are ultimately *about*. The dialects supply the vocabulary of
naming; the substrate supplies the ground truth.

## Epistemic-recovery as an Argument signature

Both dialects' trajectory checks on their respective thematic claims
include an *epistemic-recovery* signature:

- Dramatic's A_truth_recovers: "Poirot KNOWS killed(sheppard,
  ackroyd)"
- Save the Cat's Strand_A_case: "Poirot KNOWS killed(sheppard,
  ackroyd)"
- Save the Cat's theme_statement: "Poirot KNOWS ...; Caroline KNOWS
  ..."

The AFFIRM resolution of "the truth will out" is checked in the
*agent-knowledge* layer, not just the world-facts layer. The
investigator's KNOWN set is where the claim lives. This is a new
verifier pattern relative to Oedipus and Macbeth's trajectory checks
(which tested world-derived compound predicates like tyrant or
kinslayer). Ackroyd's Whydunit structure pushed the verifier toward
epistemic signatures — because what the Whydunit argues IS about
epistemic recovery.

## What remains open

- ~~**StcCharacter amendment**: the Save the Cat Character gap is now
  pressed by two encodings. Not yet a sketch amendment; worth a
  third story encoded against the dialect before deciding.~~
  **Landed 2026-04-16** as [save-the-cat-sketch-02](save-the-cat-sketch-02.md):
  StcCharacter with `role_labels` as a canonical-plus-open vocabulary,
  reference wiring on beats/strands/story, and archetype assignments
  binding genre archetypes to characters or prose notes. Sheppard
  now carries `role_labels=("protagonist", "antagonist", "narrator")` —
  the structural claim this sketch named as unexpressible under
  sketch-01.

- **Substrate non-monotonicity pattern**: no substrate revocation
  events in Ackroyd's encoding (unlike Macbeth's E_malcolm_crowned
  revoking king(macbeth, scotland)). Both Dramatic and Save the Cat
  trajectory checks project to the same τ_s for all signatures,
  which simplifies the check code. Informative: the substrate's
  monotonicity-violation case is Macbeth-specific, not general.

- **Unreliable narration at the verifier**: the Dramatic and Save
  the Cat cross-boundary verifiers both test Ackroyd's substrate
  honestly — but neither exercises the sjuzhet layer. The
  τ_s-vs-τ_d divergence the substrate uses to hold the narrator's
  withholding is not probed. A future sjuzhet-aware verifier
  primitive could ask "at τ_d = 2, what does the reader know?" and
  compare against "at τ_s = 2, what is true?". This is the verifier
  gap ackroyd-sketch-01's OQ1 anticipated. Deferred to a future
  substrate + verifier extension.

- **Three encodings at two dialects = six verifier files.** The
  shared helpers extraction (verifier_helpers.py) has served well;
  six files using it is now the established pattern. No further
  refactor surface visible without more encodings.

## What's next

The Ackroyd encoding session concludes the third-story arc. Natural
follow-ons:

1. **StcCharacter amendment exercise.** If save-the-cat-sketch-02
   were to add a minimal StcCharacter record, this encoding is the
   natural test case (the MC-Antagonist Sheppard character is the
   gap's clearest example).

2. **Fourth encoding at both dialects, different again.** Serial /
   long-form or non-Western traditions were named as REVIEW.md's
   research-survey gaps. Ackroyd's Whydunit cleanness says the
   architecture handles genre-native material well; whether it
   handles form-native material (not a novel; not a play; something
   episodic) is the next open question.

3. **Sjuzhet-layer verifier extension.** The substrate's τ_s-vs-τ_d
   divergence carries Ackroyd's unreliable narration; no verifier
   probes it today. A single-file addition to verifier primitives
   for disclosure-layer checks would close one of
   ackroyd-sketch-01's stated gaps.

4. **The cross-dialect comparison pattern itself is now a genre.**
   Two of these sketches exist (Macbeth's, Ackroyd's). The next
   story encoded will want its own comparison sketch if the
   pattern keeps paying out. If it stops paying out, the
   convergences/divergences are stabilized and don't need per-story
   restatement.
