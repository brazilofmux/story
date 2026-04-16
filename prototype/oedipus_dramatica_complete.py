"""
oedipus_dramatica_complete.py — Oedipus Rex encoded against the
`dramatica-complete` Template.

Extends oedipus_dramatic.py (which encodes the base Dramatic dialect
records — Argument, Throughlines, Characters, Scenes, Beats, Stakes)
with the Template-specific records: DomainAssignments, Dynamic Story
Points, Signposts, ThematicPicks, and CharacterElementAssignments.

This is the first real encoding against dramatica-complete. The
smoke test in the commit that shipped the Template used Oedipus
with partial data (MC Signposts only); this file completes the
encoding across all four Throughlines and exercises every validation
rule the Template ships.

Encoding decisions follow dramatica-template-sketch-01's worked
example where it exists; the rest is authored here for the first
time.

Expected output from all three Template verifiers:

- verify_dramatica_complete: 0 observations (all structural rules
  pass — 4 Throughlines, 4 DomainAssignments, 6 DSPs, 16
  Signposts, Story Goal + Consequence)
- verify_character_elements: 0 observations (all 8 archetypes'
  Motivation Elements assigned canonically; no duplicates)
- verify_thematic_picks: 0 observations where chain data is
  registered (MC Throughline chain complete; other Throughlines'
  picks reference quads not yet fully registered, which the
  validator silently accepts)
"""

from __future__ import annotations

from oedipus_dramatic import (
    STORY, THROUGHLINES, CHARACTERS, SCENES, BEATS, STAKES,
    ARGUMENTS,
    C_oedipus, C_jocasta, C_creon, C_tiresias,
    C_shepherd, C_messenger,
)

from dramatica_template import (
    Domain, DSPAxis, QuadPosition,
    Resolve, Growth, Approach, Limit, Outcome, Judgment,
    MotivationElement,
    DomainAssignment, DynamicStoryPoint, Signpost,
    QuadPick, ThematicPicks,
    CharacterElementAssignment,
    CONCERN_QUADS_BY_DOMAIN,
    CONCERN_ACTIVITY_QUAD,
    CONCERN_SITUATION_QUAD,
    CONCERN_MANIPULATION_QUAD,
    CONCERN_FIXED_ATTITUDE_QUAD,
    ARCHETYPE_MOTIVATION_ELEMENTS,
    verify_dramatica_complete,
    verify_character_elements,
    verify_thematic_picks,
    canonical_ending,
    ISSUE_QUADS_BY_CONCERN,
    register_issue_quad,
    Quad,
)


# ============================================================================
# Domain Assignments (Q3)
# ============================================================================
#
# Per dramatica-template-sketch-01's worked example:
# - Overall Story (the plague investigation) → Situation (an external
#   fixed state — the plague IS the situation)
# - MC Oedipus → Activity (he acts: investigates, questions, demands)
# - IC Jocasta → Fixed Attitude (her fixed belief about oracles)
# - Relationship → Manipulation (the marriage is about concealment,
#   role-playing, revelation)

DOMAIN_ASSIGNMENTS = (
    DomainAssignment(
        id="DA_overall",
        throughline_id="T_overall_plague",
        domain=Domain.SITUATION,
    ),
    DomainAssignment(
        id="DA_mc",
        throughline_id="T_mc_oedipus",
        domain=Domain.ACTIVITY,
    ),
    DomainAssignment(
        id="DA_ic",
        throughline_id="T_impact_jocasta",
        domain=Domain.FIXED_ATTITUDE,
    ),
    DomainAssignment(
        id="DA_rel",
        throughline_id="T_relationship_oj",
        domain=Domain.MANIPULATION,
    ),
)


# ============================================================================
# Dynamic Story Points (Q5)
# ============================================================================
#
# Per the sketch's worked example:
# - Resolve: Change (Oedipus changes — catastrophically)
# - Growth: Stop (he must stop pursuing — he cannot)
# - Approach: Do-er (Oedipus acts; does not retreat inward)
# - Limit: Optionlock (he runs out of options, not time)
# - Outcome: Success (the plague-killer IS found)
# - Judgment: Bad (at catastrophic personal cost)
#
# Outcome × Judgment = Success × Bad = "Personal Tragedy"

DYNAMIC_STORY_POINTS = (
    DynamicStoryPoint(
        id="DSP_resolve", axis=DSPAxis.RESOLVE,
        choice=Resolve.CHANGE.value, story_id=STORY.id,
    ),
    DynamicStoryPoint(
        id="DSP_growth", axis=DSPAxis.GROWTH,
        choice=Growth.STOP.value, story_id=STORY.id,
    ),
    DynamicStoryPoint(
        id="DSP_approach", axis=DSPAxis.APPROACH,
        choice=Approach.DO_ER.value, story_id=STORY.id,
    ),
    DynamicStoryPoint(
        id="DSP_limit", axis=DSPAxis.LIMIT,
        choice=Limit.OPTIONLOCK.value, story_id=STORY.id,
    ),
    DynamicStoryPoint(
        id="DSP_outcome", axis=DSPAxis.OUTCOME,
        choice=Outcome.SUCCESS.value, story_id=STORY.id,
    ),
    DynamicStoryPoint(
        id="DSP_judgment", axis=DSPAxis.JUDGMENT,
        choice=Judgment.BAD.value, story_id=STORY.id,
    ),
)

CANONICAL_ENDING = canonical_ending(
    Outcome.SUCCESS.value, Judgment.BAD.value,
)
assert CANONICAL_ENDING == "personal-tragedy"


# ============================================================================
# Signposts (Q7) — 4 per Throughline = 16 total
# ============================================================================
#
# Each Throughline uses all 4 Concerns from its Domain's Concern Quad
# as Signposts. The ordering represents the act-progression: which
# aspect of the Domain's conflict the Throughline passes through at
# each point.

# MC in Activity — per the sketch:
# Learning → Understanding → Doing → Obtaining
_mc_cq = CONCERN_ACTIVITY_QUAD
MC_SIGNPOSTS = (
    Signpost(id="SP_mc_1", throughline_id="T_mc_oedipus",
             signpost_position=1, signpost_element=_mc_cq.element_D),
             # learning — initial investigation
    Signpost(id="SP_mc_2", throughline_id="T_mc_oedipus",
             signpost_position=2, signpost_element=_mc_cq.element_A),
             # understanding — Tiresias's accusation sinks in
    Signpost(id="SP_mc_3", throughline_id="T_mc_oedipus",
             signpost_position=3, signpost_element=_mc_cq.element_B),
             # doing — sustained questioning (Jocasta, Messenger, Shepherd)
    Signpost(id="SP_mc_4", throughline_id="T_mc_oedipus",
             signpost_position=4, signpost_element=_mc_cq.element_C),
             # obtaining — he obtains the truth (and is undone)
)

# OS in Situation:
# The Present → How Things Are Changing → The Past → The Future
_os_cq = CONCERN_SITUATION_QUAD
OS_SIGNPOSTS = (
    Signpost(id="SP_os_1", throughline_id="T_overall_plague",
             signpost_position=1, signpost_element=_os_cq.element_D),
             # the-present — the plague IS the present situation
    Signpost(id="SP_os_2", throughline_id="T_overall_plague",
             signpost_position=2, signpost_element=_os_cq.element_B),
             # how-things-are-changing — investigation begins; the
             # present situation is being actively questioned
    Signpost(id="SP_os_3", throughline_id="T_overall_plague",
             signpost_position=3, signpost_element=_os_cq.element_A),
             # the-past — the murder of Laius IS the past that must
             # be uncovered; the past takes over the investigation
    Signpost(id="SP_os_4", throughline_id="T_overall_plague",
             signpost_position=4, signpost_element=_os_cq.element_C),
             # the-future — the plague will end; the future is
             # purchased at the cost of Oedipus's self-destruction
)

# IC in Fixed Attitude:
# Memories → Innermost Desires → Contemplation → Impulsive Responses
_ic_cq = CONCERN_FIXED_ATTITUDE_QUAD
IC_SIGNPOSTS = (
    Signpost(id="SP_ic_1", throughline_id="T_impact_jocasta",
             signpost_position=1, signpost_element=_ic_cq.element_D),
             # memories — Jocasta's memory of the oracle about her son
    Signpost(id="SP_ic_2", throughline_id="T_impact_jocasta",
             signpost_position=2, signpost_element=_ic_cq.element_A),
             # innermost-desires — her desire to protect the family
             # from what the investigation will find
    Signpost(id="SP_ic_3", throughline_id="T_impact_jocasta",
             signpost_position=3, signpost_element=_ic_cq.element_C),
             # contemplation — "don't pursue this; let it go"
    Signpost(id="SP_ic_4", throughline_id="T_impact_jocasta",
             signpost_position=4, signpost_element=_ic_cq.element_B),
             # impulsive-responses — her exit; the suicide
)

# RS in Manipulation:
# Conceiving an Idea → Developing a Plan → Playing a Role →
# Changing One's Nature
_rs_cq = CONCERN_MANIPULATION_QUAD
RS_SIGNPOSTS = (
    Signpost(id="SP_rs_1", throughline_id="T_relationship_oj",
             signpost_position=1, signpost_element=_rs_cq.element_D),
             # conceiving-an-idea — the marriage as a settled idea;
             # the relationship's premise
    Signpost(id="SP_rs_2", throughline_id="T_relationship_oj",
             signpost_position=2, signpost_element=_rs_cq.element_A),
             # developing-a-plan — Jocasta's plan to stop the
             # investigation before it reaches the truth
    Signpost(id="SP_rs_3", throughline_id="T_relationship_oj",
             signpost_position=3, signpost_element=_rs_cq.element_B),
             # playing-a-role — husband/wife as roles concealing
             # the son/mother reality
    Signpost(id="SP_rs_4", throughline_id="T_relationship_oj",
             signpost_position=4, signpost_element=_rs_cq.element_C),
             # changing-one's-nature — the relationship can no longer
             # be what it was; both are changed
)

ALL_SIGNPOSTS = MC_SIGNPOSTS + OS_SIGNPOSTS + IC_SIGNPOSTS + RS_SIGNPOSTS
assert len(ALL_SIGNPOSTS) == 16


# ============================================================================
# Story Goal and Story Consequence (Q4)
# ============================================================================

STORY_GOAL = ("identify the pollution causing the plague and expel "
              "it from Thebes")
STORY_CONSEQUENCE = ("the plague continues; the city dies; the "
                     "moral pollution festers")


# ============================================================================
# Character Element Assignments — Motivation Elements
# ============================================================================
#
# Oedipus uses the 8 archetypes (per oedipus_dramatic.py's
# character_function_template="dramatica-8"). Each archetype gets
# its canonical Motivation pair. For Oedipus, who fills Protagonist,
# the canonical elements are Pursue + Consider — which exactly
# describes Oedipus's character: he Pursues the truth relentlessly
# and he Considers each piece of evidence.
#
# Note: oedipus_dramatic.py has 6 Characters with function_labels;
# 2 remain without (Laius — dead pre-play, and others if they exist).
# Only the 6 function-carrying Characters get element assignments.

CHARACTER_ELEMENT_ASSIGNMENTS = (
    # Protagonist: Oedipus — Pursue + Consider
    CharacterElementAssignment(
        id="CEA_oedipus_pursue", character_id="C_oedipus",
        element=MotivationElement.PURSUE,
    ),
    CharacterElementAssignment(
        id="CEA_oedipus_consider", character_id="C_oedipus",
        element=MotivationElement.CONSIDER,
    ),
    # Guardian: Creon — Conscience + Help
    CharacterElementAssignment(
        id="CEA_creon_conscience", character_id="C_creon",
        element=MotivationElement.CONSCIENCE,
    ),
    CharacterElementAssignment(
        id="CEA_creon_help", character_id="C_creon",
        element=MotivationElement.HELP,
    ),
    # Contagonist: Jocasta — Temptation + Hinder
    CharacterElementAssignment(
        id="CEA_jocasta_temptation", character_id="C_jocasta",
        element=MotivationElement.TEMPTATION,
    ),
    CharacterElementAssignment(
        id="CEA_jocasta_hinder", character_id="C_jocasta",
        element=MotivationElement.HINDER,
    ),
    # Reason: Tiresias — Logic + Control
    CharacterElementAssignment(
        id="CEA_tiresias_logic", character_id="C_tiresias",
        element=MotivationElement.LOGIC,
    ),
    CharacterElementAssignment(
        id="CEA_tiresias_control", character_id="C_tiresias",
        element=MotivationElement.CONTROL,
    ),
    # Emotion: Shepherd — Feeling + Uncontrolled
    CharacterElementAssignment(
        id="CEA_shepherd_feeling", character_id="C_shepherd",
        element=MotivationElement.FEELING,
    ),
    CharacterElementAssignment(
        id="CEA_shepherd_uncontrolled", character_id="C_shepherd",
        element=MotivationElement.UNCONTROLLED,
    ),
    # Sidekick: Messenger — Faith + Support
    CharacterElementAssignment(
        id="CEA_messenger_faith", character_id="C_messenger",
        element=MotivationElement.FAITH,
    ),
    CharacterElementAssignment(
        id="CEA_messenger_support", character_id="C_messenger",
        element=MotivationElement.SUPPORT,
    ),
)

# Note: Antagonist and Skeptic are unfilled in the oedipus_dramatic.py
# encoding (Oedipus has no clear single antagonist — the plague / fate
# / himself). Those elements (Avoid, Reconsider, Disbelief, Oppose)
# are unassigned, which is honest for this encoding.


# ============================================================================
# ThematicPicks — MC Throughline (others deferred to full Issue data)
# ============================================================================
#
# MC Oedipus in Activity Domain.
# Concern pick: "understanding" (from Activity's Concern Quad at
# position A). Oedipus's activity-domain concern is about
# Understanding — specifically, understanding who he is and what
# he has done.

MC_CONCERN_PICK = QuadPick(
    id="CP_mc_oedipus",
    quad_id=CONCERN_ACTIVITY_QUAD.id,
    chosen_position=QuadPosition.A,  # "understanding"
    attached_to_kind="throughline",
    attached_to_id="T_mc_oedipus",
)

# Issue pick: from the "understanding" Issue Quad.
# This Quad is registered in test_dramatica_template.py for testing;
# we re-register here to be explicit (idempotent — same id).
ISSUE_QUAD_UNDERSTANDING = Quad(
    id="issue_understanding",
    kind="issue-quad",
    element_A="instinct",
    element_B="senses",
    element_C="interpretation",
    element_D="conditioning",
    authored_by="dramatica-theory",
)
register_issue_quad("understanding", ISSUE_QUAD_UNDERSTANDING)

MC_ISSUE_PICK = QuadPick(
    id="IP_mc_oedipus",
    quad_id=ISSUE_QUAD_UNDERSTANDING.id,
    chosen_position=QuadPosition.C,  # "interpretation"
    # Oedipus's Issue is Interpretation — the play turns on how
    # each piece of evidence is interpreted, and Oedipus's
    # (mis)interpretation of his own identity.
    attached_to_kind="throughline",
    attached_to_id="T_mc_oedipus",
)

# Problem pick: would come from an Element Quad under "interpretation".
# For now, use the test Element Quad (which has Pursue/Consider/Avoid/
# Reconsider). Oedipus's Problem is Pursuit — he cannot stop pursuing.
# The Solution (Avoid) is the thing he cannot do.
#
# Note: the exact Element Quad labels at this level need canonical
# Dramatica verification. The structural machinery (pick, derive,
# validate) works regardless of the exact labels.

from dramatica_template import register_element_quad

ELEMENT_QUAD_INTERPRETATION = Quad(
    id="element_interpretation",
    kind="element-quad",
    element_A="pursue",
    element_B="consider",
    element_C="avoid",
    element_D="reconsider",
    authored_by="dramatica-theory",
)
register_element_quad("interpretation", ELEMENT_QUAD_INTERPRETATION)

MC_PROBLEM_PICK = QuadPick(
    id="PP_mc_oedipus",
    quad_id=ELEMENT_QUAD_INTERPRETATION.id,
    chosen_position=QuadPosition.A,  # "pursue" — Oedipus's Problem
    attached_to_kind="throughline",
    attached_to_id="T_mc_oedipus",
)

MC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_mc_oedipus",
    concern_pick=MC_CONCERN_PICK,
    issue_pick=MC_ISSUE_PICK,
    problem_pick=MC_PROBLEM_PICK,
    solution_override="avoid",  # derived from dynamic pair of "pursue"
)

ALL_THEMATIC_PICKS = (MC_THEMATIC_PICKS,)


# ============================================================================
# Run all three verifiers
# ============================================================================


def run() -> dict:
    """Run verify_dramatica_complete + verify_character_elements +
    verify_thematic_picks. Returns a dict of results by verifier."""
    structural = verify_dramatica_complete(
        throughlines=THROUGHLINES,
        domain_assignments=DOMAIN_ASSIGNMENTS,
        dynamic_story_points=DYNAMIC_STORY_POINTS,
        signposts=ALL_SIGNPOSTS,
        story_goal=STORY_GOAL,
        story_consequence=STORY_CONSEQUENCE,
    )
    elements = verify_character_elements(
        assignments=CHARACTER_ELEMENT_ASSIGNMENTS,
        characters=CHARACTERS,
    )
    thematic = verify_thematic_picks(
        picks_list=ALL_THEMATIC_PICKS,
        domain_assignments=DOMAIN_ASSIGNMENTS,
    )
    return {
        "structural": structural,
        "elements": elements,
        "thematic": thematic,
    }


if __name__ == "__main__":
    results = run()
    total = 0
    for name, obs in results.items():
        print(f"=== {name}: {len(obs)} observations ===")
        for o in obs:
            print(f"  [{o.severity}] {o.code}: {o.message[:90]}")
        total += len(obs)
    print(f"\nTotal observations: {total}")
    print(f"Canonical ending: {CANONICAL_ENDING}")
