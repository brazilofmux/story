# Dramatica template — sketch 02 (completeness review; the canonical EIGHT dynamics; Driver + Problem-Solving Style)

**Status:** landed; the two missing essential dynamics added, authored across 7 encodings, 1239 tests green
**Date:** 2026-06-18
**Supersedes:** nothing (amendment)
**Extends:** [dramatica-template-sketch-01](dramatica-template-sketch-01.md) — its Q5 committed to *six* DynamicStoryPoints; this corrects that to the canonical eight. All other sketch-01 commitments unchanged.
**Frames:** memory `dramatica-precision-limit` (the dual-value machinery this leans on), [state-of-play-19](state-of-play-19.md).
**Related:** `dramatica_template.py` (the axes), the 7 `*_dramatica_complete.py` encodings (authored values), [ambiguity-honest-substrate-sketch-01](ambiguity-honest-substrate-sketch-01.md).

## Why this sketch exists

A completeness review of our Dramatica against the Grand Argument Story
theory. The verdict: **substantially complete on the hard structure, with one
real gap in the dynamics.** What we already have is the expensive part —

- 4 Throughlines × the Domain → Concern → Issue → Problem nested quad
  hierarchy, WITH the Problem → Solution / Symptom / Response derivation
  (dynamic / companion / dependent pairs). The thematic engine is real.
- All four character element quads (Motivation, Methodology, Evaluation,
  Purpose) + the 8 archetypal functions assigned to throughlines.
- Signposts (4 per throughline), Story Goal + Consequence, Outcome × Judgment
  → the four endings (now ambiguity-honest).

The gap: sketch-01's Q5 committed to **six** DynamicStoryPoints, but
Dramatica's canonical storyform is set by **eight** essential dynamics. Two
were silently absent:

- **Driver** (Action / Decision) — structurally load-bearing: it types every
  act / Signpost transition. Clearly necessary.
- **Problem-Solving Style** (Linear / Holistic; formerly "Mental Sex") — the
  eighth essential, and the single most-disputed appreciation in the theory.

## What was added

`Driver` and `ProblemSolvingStyle` enums + `DSPAxis.DRIVER` and
`DSPAxis.PROBLEM_SOLVING_STYLE`, wired into `DSP_VALID_CHOICES`, the coupling
map (both CHARACTERIZATION-kind — they classify from substrate structure), and
the generation glosses. `verify_dramatica_complete` now expects eight, not six.

The two new axes were authored across the **7 real** dramatica-complete
encodings (And Then There Were None is a skeleton stub — left alone):

| Encoding | Driver | Problem-Solving Style |
|---|---|---|
| Rocky | decision | holistic |
| Oedipus | action | linear |
| Macbeth | decision | linear |
| Chinatown | action | linear |
| Pride & Prejudice | decision | holistic |
| Ackroyd | action | **Dual{linear, holistic}** |
| Rashomon (frame) | **Dual{action, decision}** | **Dual{linear, holistic}** |

## The integrity move — Dual where the binary isn't honest

This is the payoff of pairing the completeness pass with the
[ambiguity-honest substrate](ambiguity-honest-substrate-sketch-01.md). Problem-
Solving Style is exactly the axis `dramatica-precision-limit` warns about — the
theory's own rename from "Mental Sex" signals it over-claims. So rather than
fabricate a confident binary for stories where the MC's solving manner is
genuinely unclear, those axes are authored `Dual`:

- **Ackroyd** — Sheppard is the concealing narrator-murderer; his
  problem-solving is a long con, neither cleanly linear nor holistic. PSS Dual.
- **Rashomon** — the irreconcilable-accounts story. BOTH its frame Driver and
  PSS are Dual; forcing either would betray the work's whole premise.

The single-pole calls (Oedipus/Macbeth/Chinatown linear; Rocky/P&P holistic)
are defensible authorial readings, each commented in its encoding — and open to
correction. The point is not that these are the "official" Dramatica values
(we don't claim to have those); it is that the axis is now *modeled*, and
honestly hedged where a confident call would be fabrication.

## Rashomon as the test of "complete"

Rashomon's four account-stories are **deliberately partial** — one DSP each
(Limit), one domain assignment. Incompleteness is the encoding's design: the
accounts contradict and none is a full storyform. So only its FRAME story was
brought to eight; the versions stay partial, and their `dsp_missing` advisory
is *correct*, not a defect. "Complete" is per-Story, and some stories rightly
refuse it.

## Level-4 elements: ship the canonical 64, verify by consistency

The quad hierarchy reaches level 4 (a throughline's Problem is a bottom-level
Element, with Solution/Symptom/Response derived), but until now the level-4
DATA was unshipped: encodings registered their own element quads via
`register_element_quad`, which silently overwrote — so a Variation could be
given two different quads by two encodings with nothing to catch it.

**What "256 elements" actually is.** The table's leaf level has 256 cells, but
they are filled by only **64 distinct element labels** — element quads recur
across the table in a pattern that is *not* Type-aligned (verified
empirically: `attempt`/`work` share a Type but differ; `attempt`/`fate`
differ in Type but share a quad). Those 64 are exactly the union of the four
character-element quad sets (Motivation/Methodology/Evaluation/Purpose),
already in the template and verified canonical. So the shippable canonical
*data* is the **64-element vocabulary** + the per-Variation placement map; the
geometry is 256, the vocabulary is 64 (the research doc's figure was right).

**What we shipped (no fabrication):**
- `CANONICAL_ELEMENTS` — the frozenset of 64, built from the four
  character-element enums. The authoritative bottom-level vocabulary.
- `register_element_quad` now HARD-validates the two unambiguous properties:
  every element ∈ the canonical 64, and a quad is four distinct elements.
  (All 15 existing element quads pass.)
- `verify_element_quads` — the consistency-based verifier: it surfaces
  `element_quad_conflict` (a Variation registered with >1 distinct quad),
  re-confirms vocabulary/well-formedness, and reports coverage (15/64
  Variations placed so far).

**What we did NOT ship:** the full 64-Variation → element-quad placement map.
That recurrence pattern is not derivable from the 64 vocabulary alone and needs
the Dramatica Table source. Per the chosen strategy, it fills in incrementally;
the verifier guards consistency in the meantime.

**The verifier earned its keep immediately** — it surfaced four REAL conflicts
in the existing corpus, where encodings disagree on a Variation's canonical
element quad (the 64 Variation labels are all distinct and each conflicted one
lives under a single Type, so these are genuine drift, not a keying artifact):

| Variation | conflicting registrations |
|---|---|
| `commitment` | `(conscience,help,temptation,hinder)` vs `(logic,control,feeling,uncontrolled)` |
| `desire` | `(avoid,reconsider,pursue,consider)` vs `(logic,control,feeling,uncontrolled)` |
| `doubt` | three variants (incl. a position-rotation of one) |
| `interpretation` | `(faith,support,disbelief,oppose)` vs `(pursue,consider,avoid,reconsider)` |

These are left FLAGGED, not resolved — which quad is canonical needs the
Dramatica Table source. (DP-OQ: resolve the four against the source when it is
available, then the verifier's conflict count should drop to zero.)

## What is still NOT modeled (correctly scoped, not flaws)

These are sketch-01's explicit deferrals, reaffirmed — the *mechanism* exists
or the pattern extends uniformly; fill when an encoding pressures them:

- The full 64 / 256 Issue / Problem quad **data** (some Issue quads now
  shipped; the rest on demand).
- **Journeys** / Plot-Sequence between the four Signposts (the PSR).
- The **six other OS plot appreciations** — Requirements, Forewarnings, Costs,
  Dividends, Prerequisites, Preconditions. Only Goal + Consequence are modeled
  as story points. These are the next real depth target if Dramatica plot-level
  fidelity is ever wanted.

## The discipline this pins

Our `dramatica-complete` now means the canonical **eight** essential dynamics,
the four-throughline domain/concern/issue/problem hierarchy with Problem
derivation, the character element quads, and Signposts + Goal/Consequence. When
authoring a dynamic you cannot confidently call — especially Problem-Solving
Style — declare it `Dual`, do not fabricate a binary. Completeness is per-Story;
an intentionally-partial encoding (Rashomon's accounts) is allowed to stay so.
