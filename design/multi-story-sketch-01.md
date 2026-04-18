# Multi-story encoding — sketch 01

**Status:** draft, active
**Date:** 2026-04-18
**Supersedes:** nothing (new topic; composes with but does not amend [dramatic-sketch-01](dramatic-sketch-01.md) and [dramatica-template-sketch-01](dramatica-template-sketch-01.md))
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [architecture-sketch-02.md](architecture-sketch-02.md), [substrate-sketch-05.md](substrate-sketch-05.md), [verification-sketch-01.md](verification-sketch-01.md), [dramatic-sketch-01.md](dramatic-sketch-01.md), [dramatica-template-sketch-01.md](dramatica-template-sketch-01.md)
**Related:** `rashomon.py` (substrate encoding with four contested branches, landed pre-sketch); the 2026-04-18 Substack article "Timelock or Optionlock? Real Stories Don't Pick One" (section 8 promises this as the next stress test)
**Superseded by:** nothing yet

## Purpose

Close the representational gap the Rashomon encoding immediately
hits at the Dramatic / Dramatica-Complete dialect layer: the
current dialect commits to **one Story per encoding**, and Rashomon
is not one story. It's a frame story at the gate (the woodcutter,
the priest, the commoner, trapped by the rainstorm, arguing about
what to trust in human nature) nesting four inner stories (the
four testimonies of the killing), each on its own contested
substrate branch.

The sketch commits the minimum required to proceed: a
**StoryEncoding** record that declares multiple Stories and their
nesting / parallel relations. No substrate changes. No changes to
the per-Story commitments in dramatic-sketch-01 or dramatica-
template-sketch-01. Verification runs per-Story; cross-Story
verification is a deliberately-scoped-out future primitive.

The goal is not to solve the general "recursive stories" question.
The goal is to let Rashomon be encoded today, so the probe/
verifier partnership can surface what it surfaces. Rashomon is the
forcing function; the sketch commits only what Rashomon requires.

## What this sketch commits to

- A new **StoryEncoding** record at the dialect layer, carrying a
  tuple of Stories, a tuple of typed StoryRelations between them,
  and a declared entry-Story id (the encoding's "root" — typically
  the outermost frame).
- Two relation kinds: **contains** (one Story nests another; the
  frame contains its inner stories) and **parallel-to** (two
  Stories are siblings under the same parent; the four Rashomon
  testimonies are parallel to each other under the frame). These
  two cover Rashomon. Others (mutually-exclusive, sequential,
  embedded-as-metaphor) are OQs.
- Per-Story verification. The existing `verify_dramatica_complete`
  (and related self-verifiers) run per-Story without modification.
  An encoding with N Stories produces a per-Story verdict vector;
  there is no forced "combined verdict."
- Lowerings remain unchanged in shape. Because record ids are
  globally unique within an encoding by existing discipline
  (`T_mc_frame`, `T_mc_testimony_a`, etc.), a Lowering's
  `upper_record` already disambiguates which Story it's for
  without needing a new `story_id` field.
- Zero substrate changes. Rashomon's substrate already represents
  the four contested branches; the dialect layer just needs to
  match.

## What this sketch does NOT commit to

- **Cross-Story verification primitives.** Whether a frame Story's
  Story_goal "aligns" with its inner Stories' payoffs, whether
  parallel Stories are "genuinely incompatible" in the Dramatica
  sense, whether a contains-relation implies specific structural
  constraints on the inner Stories — these are real and
  interesting questions, but the sketch does not commit to
  specific predicates. Banked as OQ1. What we learn from running
  Rashomon through per-Story verification will suggest what cross-
  Story predicates are worth committing to.
- **A general "recursive stories" framework.** The sketch supports
  two levels of nesting (frame contains testimonies) because
  that's what Rashomon is. Deeper nesting (frame contains frames
  containing testimonies) or arbitrary graphs (mutually-
  containing stories) are OQ2. A future encoding will pressure
  those questions if they matter.
- **Changes to single-Story encodings.** The four existing
  dramatica-complete encodings (Oedipus, Macbeth, Ackroyd, Rocky)
  continue to work. They are, in the new frame, StoryEncodings of
  exactly one Story with no relations. The sketch commits to
  back-compat: every existing encoding becomes a trivial
  StoryEncoding wrapper with no change to its per-Story records.
- **Changes to the Dramatic dialect's M1–M10 or the Dramatica
  Template's Q1–Q10.** Those commitments are per-Story and stay
  intact. The StoryEncoding sits above them.
- **A claim about what Rashomon's verifier output will show.**
  Section 8 of the Substack article stakes a specific hypothesis
  (the four testimonies fail Grand Argument Story form; the frame
  satisfies it). That hypothesis is the *reason* to do this work,
  but the sketch does not commit to its truth — verification may
  reveal something else.

## Commitments

### MS1 — Multi-Story is additive, not a replacement

An encoding under the Dramatic dialect (with or without a
Dramatica-Complete template) may declare one Story (the current
case) or more than one (the new case). The existing per-Story
commitments — dramatic-sketch-01 M1–M10 and dramatica-template-
sketch-01 Q1–Q10 — apply to each Story independently. No existing
commitment is amended.

An encoding of exactly one Story requires no StoryEncoding record.
The existing single-Story modules (`oedipus_dramatica_complete.py`
et al.) continue to work verbatim.

### MS2 — StoryEncoding record

A new dialect-layer record:

```python
@dataclass(frozen=True)
class StoryEncoding:
    """A dialect-layer record that declares a set of Dramatica
    Stories composing one encoded work, plus the structural
    relations between them."""
    id: str
    title: str
    stories: tuple           # tuple[Story]
    relations: tuple         # tuple[StoryRelation]
    entry_story_id: str      # which Story is the root / outermost
    authored_by: str = "author"
```

`stories` is a tuple of the Story records in the encoding.
`entry_story_id` names the top-level Story — the frame, in
Rashomon's case. `relations` is the relationship graph.

### MS3 — StoryRelation kinds

Two relation kinds commit at this sketch:

- **`contains`** — `parent_story_id` nests `child_story_id`. The
  parent's narrative surrounds the child's; the child's events
  happen as retellings, flashbacks, or enclosed sub-narratives
  within the parent's frame.
- **`parallel-to`** — two Stories are siblings under the same
  containing parent. They represent incompatible or alternative
  accounts of the same events, or parallel-world narratives that
  share context. In Rashomon, the four testimonies are
  parallel-to each other under the frame.

```python
@dataclass(frozen=True)
class StoryRelation:
    kind: str                      # "contains" or "parallel-to"
    a_story_id: str                # parent or first sibling
    b_story_id: str                # child or second sibling
    notes: str = ""                # optional prose justification
```

Other relation kinds (mutually-exclusive, sequential,
embedded-as-metaphor) are deliberately deferred. Rashomon doesn't
need them; future encodings will pressure them if they matter.

### MS4 — Per-Story verification runs unchanged

The existing Dramatica self-verifier
(`verify_dramatica_complete`) and cross-boundary verifier
(`*_dramatica_complete_verification.py`) both run against a
single Story's records. Under MS1–MS3 they continue to do so —
they are invoked once per Story in a StoryEncoding, producing a
per-Story verdict-vector. No single "combined verdict" is
synthesized at this sketch.

This means a StoryEncoding of five Stories produces 5 × 9 = 45
VerificationReview records on the cross-boundary surface. The
cross-boundary reader-model probe receives them all; the author
walks them per-Story or in aggregate.

### MS5 — Lowerings carry per-Story semantics via record-id uniqueness

The existing Lowering record shape (lowering-record-sketch-01 L1–
L10) does not change. A Lowering binds a cross-dialect upper
record id to substrate lower records. Because each Story in a
StoryEncoding uses globally-unique record ids within the encoding
(`T_mc_frame`, `T_mc_testimony_a`, `T_mc_testimony_b`, …), the
Lowering's `upper_record.record_id` already disambiguates which
Story the binding belongs to.

A substrate event may be referenced by Lowerings from multiple
Stories. The Rashomon killing event is lowered from each of the
four testimonies' Throughline bindings independently. Nothing new
required; the Lowering surface supports this today.

### MS6 — No substrate changes

The substrate's branch-contested machinery (substrate-sketch-05)
already represents Rashomon's four incompatible fabulae as sibling
branches. The dialect-layer StoryEncoding lets the Dramatic /
Dramatica-Complete surfaces match that shape at their own layer.
No new effect kinds, no new Event types, no new Branch kinds.

## Worked case — Rashomon under MS1–MS6

Proposed shape:

```
StoryEncoding(
    id="rashomon_encoding",
    title="Rashomon",
    entry_story_id="S_frame",
    stories=(
        S_frame,         # the gate / rainstorm / three listeners
        S_bandit_ver,    # Tajōmaru's testimony
        S_wife_ver,      # the wife's testimony
        S_samurai_ver,   # the dead samurai's testimony (via medium)
        S_woodcutter_ver,  # the woodcutter's belated testimony
    ),
    relations=(
        StoryRelation(kind="contains",
                      a_story_id="S_frame",
                      b_story_id="S_bandit_ver"),
        StoryRelation(kind="contains",
                      a_story_id="S_frame",
                      b_story_id="S_wife_ver"),
        StoryRelation(kind="contains",
                      a_story_id="S_frame",
                      b_story_id="S_samurai_ver"),
        StoryRelation(kind="contains",
                      a_story_id="S_frame",
                      b_story_id="S_woodcutter_ver"),
        # Six pairwise parallel-to relations among the four inner
        # stories (bandit↔wife, bandit↔samurai, bandit↔woodcutter,
        # wife↔samurai, wife↔woodcutter, samurai↔woodcutter).
        # Elided for brevity; the encoding declares all six.
    ),
)
```

Each inner Story has its own Throughlines, Characters, Scenes,
Beats, plus a Dramatica-Complete Template layer declaring its
DomainAssignments, DynamicStoryPoints, Signposts, etc. Each inner
Story's Throughlines lower onto its own substrate branch.

The substrate event `E_killing` is referenced by Lowerings from
all four inner Stories — each binding interprets the killing
differently. In one testimony the bandit is the killer; in another
the wife is; in another the samurai killed himself; in the
woodcutter's: a mix. Same substrate event, four narrative
interpretations.

Under MS4, the cross-boundary verifier runs five times (once per
Story) producing a 45-review vector. The Substack article's
hypothesis predicts the four inner verdicts fail multiple Dramatica
checks (Story_goal, Story_consequence, DSP_outcome) because
testimony-fragments don't sustain full storyform, while the frame's
nine verdicts all APPROVE.

Whether that prediction holds is the empirical question this
sketch's implementation surfaces.

## Implementation brief

1. **Extend `dramatic.py`** with the `StoryEncoding` and
   `StoryRelation` records per MS2 and MS3. Small addition; no
   existing record changes.
2. **Create `rashomon_dramatic.py`** with five Stories, their
   Throughlines/Characters/Scenes/Beats/Stakes, plus the
   StoryEncoding wrapper.
3. **Create `rashomon_dramatica_complete.py`** with the Template
   layer for each Story — DomainAssignments, DSPs, Signposts,
   ThematicPicks, CharacterElementAssignments, STORY_GOAL,
   STORY_CONSEQUENCE. Testimony fragments may have incomplete
   Template records; that's fine — the verifier will report the
   gaps.
4. **Create `rashomon_lowerings.py`** with per-Story Lowerings.
   Shared substrate events (the killing, the grove, the sword)
   appear in multiple Stories' Lowerings with different narrative
   readings per testimony.
5. **Create `rashomon_dramatica_complete_verification.py`** per
   the existing verifier pattern, but iterating over
   `StoryEncoding.stories` and producing a per-Story verdict
   vector.
6. **Add tests** in the existing test files, pinning that
   Rashomon produces 45 reviews, that the four inner Stories
   exhibit the predicted pattern (or whatever the measurement
   actually shows), that the frame Story's verdicts satisfy
   per-Story expectations.
7. **Run the cross-boundary reader-model probe** on Rashomon.
   The probe's commentary on 45 reviews will surface whatever it
   surfaces. The 2026-04-18 Substack article's hypothesis is
   testable here.

## Measurements prediction

The article's section 8 stakes:

- Frame Story verdicts: all APPROVED (Timelock at the rainstorm,
  Optionlock at the gate-leaving decision, Story_goal shaped like
  "can we trust human nature").
- Four inner Stories: each likely fails several Dramatica checks
  — Story_goal (testimony fragments don't carry goal-shaped
  argument), DSP_outcome (no clean outcome; the testimony ends at
  the witness's exit), Story_consequence (undefined).

But the sketch's honest position: the hypothesis is
article-author's bet, not verifier prediction. The implementation
pass will reveal what actually measures. The interesting case is
what the probe says when it sees 45 reviews for one encoding — it
may surface cross-Story observations the existing probe prompt
isn't shaped to produce, driving a future probe-prompt extension.

## Discipline

- **Rashomon-specific, not speculative.** MS1–MS6 commit to what
  Rashomon needs, not to a general multi-story theory. Future
  multi-story encodings (a novel with nested frames, a triptych
  narrative with three parallel stories, a choose-your-own-
  adventure with branching Stories) will pressure additional
  commitments. Commit them when they're needed.
- **Back-compat is non-negotiable.** Existing encodings work
  verbatim. The StoryEncoding wrapper is a new optional capability,
  not a forced restructuring.
- **Per-Story verification is the honest unit.** A StoryEncoding
  of five Stories means five Dramatica arguments are being made,
  one per Story. Each gets measured on its own terms. Combining
  verdicts into an aggregate is a future cross-Story primitive
  that this sketch deliberately doesn't commit to — because what
  that aggregate should mean is exactly the question Rashomon
  exists to make concrete.

## Open questions

1. **Cross-Story verification primitives.** What does it mean for
   a frame's Story_goal to "align with" its contained Stories'
   payoffs? What structural invariants should hold between
   parallel-to Stories (they must share a substrate branch set?
   they must disagree on specific world-facts? they must share
   entities?)? The sketch banks these pending Rashomon measurement.
2. **Deeper nesting / arbitrary graphs.** A novel like *Cloud
   Atlas* has six nested narratives; *Pale Fire* has a poem and a
   commentary that contain each other. Rashomon's two-level flat-
   nesting is the simple case. Multi-level nesting and cyclic
   containment are deferred until an encoding forces them.
3. **Entity aliasing across Stories.** In Rashomon, "the bandit"
   in the frame's woodcutter-testimony-relay is the same person as
   "Tajōmaru" in the bandit's own testimony. Do the Stories share
   Character records, alias them, or declare cross-Story
   identity via a new relation? The sketch defers — the
   implementation will pick a pragmatic choice and document it.
4. **Probe-prompt extension.** The cross-boundary probe's prompt
   is shaped for single-Story verifier output. Feeding it 45
   reviews from a 5-Story encoding may produce mis-calibrated
   commentary (the probe may try to synthesize a single verdict
   when there isn't one). A probe-prompt sketch extension may be
   needed — defer pending measurement.
5. **StoryEncoding vs. StoryBundle naming.** The sketch uses
   `StoryEncoding` because that's descriptive of its role — it
   encodes a set of Stories under a relation-graph. If future
   patterns argue for a richer or different name, rename.

## Summary

- New `StoryEncoding` + `StoryRelation` records at the dialect
  layer. Commit the minimum needed for Rashomon: contains + 
  parallel-to relations; per-Story verification; no cross-Story
  primitives; no substrate changes; full back-compat with single-
  Story encodings.
- The four existing dramatica-complete encodings (Oedipus,
  Macbeth, Ackroyd, Rocky) remain single-Story; they gain a
  trivial StoryEncoding wrapper only if needed for uniformity, or
  continue to skip the wrapper entirely.
- Rashomon's five Stories (frame + four testimonies) under
  contains + parallel-to relations produces 45 VerificationReviews
  when run through the existing cross-boundary verifier primitives.
- The implementation is a short sequence: extend `dramatic.py`;
  author `rashomon_dramatic.py`, `rashomon_dramatica_complete.py`,
  `rashomon_lowerings.py`, `rashomon_dramatica_complete_
  verification.py`; run probe; document what measures.
- The sketch's honest stake: the Substack article's section 8
  hypothesis is the *reason* for this work. The verifier + probe
  will say whether the hypothesis lands, breaks, or surfaces
  something else. Either outcome is information.
