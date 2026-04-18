"""
rashomon_dramatica_complete.py — Rashomon's Dramatica-Complete
Template layer across the five Stories in the encoding.

**Scope note.** Pragmatic-first-pass. The frame Story carries a
meaningful Template layer (DomainAssignments, DSPs, Story_goal,
Story_consequence). The four testimony Stories carry minimal
Template records — just enough (DomainAssignment + DSP_limit)
to trigger the LT9 classifier against each contested substrate
branch. Signposts, ThematicPicks, CharacterElementAssignments
are deferred per multi-story-sketch-01's explicit allowance that
testimony fragments may have incomplete Template records.

The Template declarations stake the Substack article's section-8
hypothesis concretely:

- **Frame DSP_limit = Optionlock.** The arguments at the gate
  narrow toward the decision about the abandoned baby; the
  priest's faith is tested alternative-by-alternative.
- **Each testimony DSP_limit = Timelock.** Each testimony is a
  scheduled climax within its own narrative arc — the duel, the
  violation, the suicide. The scheduling is internal to each
  account.

Running the LT9 classifier per Story against the appropriate
substrate scope will report each declaration against the available
structural signal. What actually measures is the next question.
"""

from __future__ import annotations

from story_engine.core.dramatica_template import (
    DomainAssignment, DynamicStoryPoint, DSPAxis,
    Domain, Resolve, Growth, Approach, Limit, Outcome, Judgment,
)
from story_engine.encodings.rashomon_dramatic import (
    RASHOMON_ENCODING,
    S_frame, S_bandit_ver, S_wife_ver, S_samurai_ver, S_woodcutter_ver,
)


# ============================================================================
# Frame Story — full Template layer
# ============================================================================

DOMAIN_ASSIGNMENTS_FRAME = (
    DomainAssignment(
        id="DA_frame_overall",
        throughline_id="T_frame_overall",
        domain=Domain.SITUATION,
    ),
    DomainAssignment(
        id="DA_frame_mc",
        throughline_id="T_frame_mc",
        domain=Domain.MANIPULATION,
    ),
    DomainAssignment(
        id="DA_frame_ic",
        throughline_id="T_frame_ic",
        domain=Domain.FIXED_ATTITUDE,
    ),
    DomainAssignment(
        id="DA_frame_rel",
        throughline_id="T_frame_rel",
        domain=Domain.ACTIVITY,
    ),
)

DYNAMIC_STORY_POINTS_FRAME = (
    DynamicStoryPoint(id="DSP_frame_resolve", axis=DSPAxis.RESOLVE,
                      choice=Resolve.CHANGE.value, story_id=S_frame.id),
    DynamicStoryPoint(id="DSP_frame_growth", axis=DSPAxis.GROWTH,
                      choice=Growth.START.value, story_id=S_frame.id),
    DynamicStoryPoint(id="DSP_frame_approach", axis=DSPAxis.APPROACH,
                      choice=Approach.BE_ER.value, story_id=S_frame.id),
    DynamicStoryPoint(id="DSP_frame_limit", axis=DSPAxis.LIMIT,
                      choice=Limit.OPTIONLOCK.value, story_id=S_frame.id),
    DynamicStoryPoint(id="DSP_frame_outcome", axis=DSPAxis.OUTCOME,
                      choice=Outcome.SUCCESS.value, story_id=S_frame.id),
    DynamicStoryPoint(id="DSP_frame_judgment", axis=DSPAxis.JUDGMENT,
                      choice=Judgment.GOOD.value, story_id=S_frame.id),
)

STORY_GOAL_FRAME = (
    "restore a defensible account of human nature — one that can "
    "survive four incompatible testimonies of a killing without "
    "collapsing into the counter-premise that everyone lies."
)

STORY_CONSEQUENCE_FRAME = (
    "the priest's faith collapses; the commoner's cynicism becomes "
    "the gate's accepted reading; human nature is what the commoner "
    "says it is."
)


# ============================================================================
# Each testimony Story — skeletal Template (DomainAssignment + DSP_limit)
# ============================================================================
#
# Each testimony's DSP_limit is declared Timelock: the testimony's
# climax is a scheduled event (duel / violation-and-killing /
# suicide). The LT9 classifier will be run against each testimony's
# contested substrate branch to see what it detects.

DOMAIN_ASSIGNMENTS_BANDIT = (
    DomainAssignment(
        id="DA_bandit_mc",
        throughline_id="T_bandit_mc",
        domain=Domain.ACTIVITY,
    ),
)
DSP_BANDIT_LIMIT = DynamicStoryPoint(
    id="DSP_bandit_limit", axis=DSPAxis.LIMIT,
    choice=Limit.TIMELOCK.value, story_id=S_bandit_ver.id,
)

DOMAIN_ASSIGNMENTS_WIFE = (
    DomainAssignment(
        id="DA_wife_mc",
        throughline_id="T_wife_mc",
        domain=Domain.FIXED_ATTITUDE,
    ),
)
DSP_WIFE_LIMIT = DynamicStoryPoint(
    id="DSP_wife_limit", axis=DSPAxis.LIMIT,
    choice=Limit.TIMELOCK.value, story_id=S_wife_ver.id,
)

DOMAIN_ASSIGNMENTS_SAMURAI = (
    DomainAssignment(
        id="DA_samurai_mc",
        throughline_id="T_samurai_mc",
        domain=Domain.FIXED_ATTITUDE,
    ),
)
DSP_SAMURAI_LIMIT = DynamicStoryPoint(
    id="DSP_samurai_limit", axis=DSPAxis.LIMIT,
    choice=Limit.TIMELOCK.value, story_id=S_samurai_ver.id,
)

DOMAIN_ASSIGNMENTS_WOODCUTTER = (
    DomainAssignment(
        id="DA_woodcutter_mc",
        throughline_id="T_woodcutter_mc",
        domain=Domain.ACTIVITY,
    ),
)
DSP_WOODCUTTER_LIMIT = DynamicStoryPoint(
    id="DSP_woodcutter_limit", axis=DSPAxis.LIMIT,
    choice=Limit.TIMELOCK.value, story_id=S_woodcutter_ver.id,
)


# ============================================================================
# Per-Story collections — indexed by Story id for the verifier
# ============================================================================

DOMAIN_ASSIGNMENTS_BY_STORY = {
    S_frame.id:           DOMAIN_ASSIGNMENTS_FRAME,
    S_bandit_ver.id:      DOMAIN_ASSIGNMENTS_BANDIT,
    S_wife_ver.id:        DOMAIN_ASSIGNMENTS_WIFE,
    S_samurai_ver.id:     DOMAIN_ASSIGNMENTS_SAMURAI,
    S_woodcutter_ver.id:  DOMAIN_ASSIGNMENTS_WOODCUTTER,
}

DYNAMIC_STORY_POINTS_BY_STORY = {
    S_frame.id:           DYNAMIC_STORY_POINTS_FRAME,
    S_bandit_ver.id:      (DSP_BANDIT_LIMIT,),
    S_wife_ver.id:        (DSP_WIFE_LIMIT,),
    S_samurai_ver.id:     (DSP_SAMURAI_LIMIT,),
    S_woodcutter_ver.id:  (DSP_WOODCUTTER_LIMIT,),
}

STORY_GOAL_BY_STORY = {
    S_frame.id: STORY_GOAL_FRAME,
    # Testimonies: no Story_goal declared (deliberately skeletal).
}

STORY_CONSEQUENCE_BY_STORY = {
    S_frame.id: STORY_CONSEQUENCE_FRAME,
}


# Flat aggregate (for callers that want a single tuple of records)
ALL_DOMAIN_ASSIGNMENTS = tuple(
    da for tup in DOMAIN_ASSIGNMENTS_BY_STORY.values() for da in tup
)
ALL_DYNAMIC_STORY_POINTS = tuple(
    d for tup in DYNAMIC_STORY_POINTS_BY_STORY.values() for d in tup
)
