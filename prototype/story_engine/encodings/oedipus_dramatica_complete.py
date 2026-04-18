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

from story_engine.encodings.oedipus_dramatic import (
    STORY, THROUGHLINES, CHARACTERS, SCENES, BEATS, STAKES,
    ARGUMENTS,
    C_oedipus, C_jocasta, C_creon, C_tiresias,
    C_shepherd, C_messenger,
)

from story_engine.core.dramatica_template import (
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
    # Shipped Issue Quads
    ISSUE_QUAD_UNDERSTANDING,
    ISSUE_QUAD_THE_PAST,
    ISSUE_QUAD_CONTEMPLATION,
    ISSUE_QUAD_PLAYING_A_ROLE,
    verify_dramatica_complete,
    verify_character_elements,
    verify_thematic_picks,
    canonical_ending,
    ISSUE_QUADS_BY_CONCERN,
    register_element_quad,
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
# ThematicPicks — all four Throughlines
# ============================================================================
#
# Each Throughline picks Concern → Issue → Problem through its
# Domain's hierarchy. Issue Quads are now shipped as canonical
# theory data in dramatica_template.py.

# -- MC Oedipus in Activity Domain --
#
# Concern: "understanding" (Activity Concern Quad, position A).
# Oedipus's activity-domain concern is about Understanding —
# specifically, understanding who he is and what he has done.

MC_CONCERN_PICK = QuadPick(
    id="CP_mc_oedipus",
    quad_id=CONCERN_ACTIVITY_QUAD.id,
    chosen_position=QuadPosition.A,  # "understanding"
    attached_to_kind="throughline",
    attached_to_id="T_mc_oedipus",
)

# Issue: "interpretation" from the Understanding Issue Quad.
# The play turns on how each piece of evidence is interpreted,
# and Oedipus's (mis)interpretation of his own identity.
MC_ISSUE_PICK = QuadPick(
    id="IP_mc_oedipus",
    quad_id=ISSUE_QUAD_UNDERSTANDING.id,
    chosen_position=QuadPosition.C,  # "interpretation"
    attached_to_kind="throughline",
    attached_to_id="T_mc_oedipus",
)

# Problem: Oedipus's Problem is Pursuit — he cannot stop pursuing.
# The Solution (Avoid) is the thing he cannot do.
#
# Note: Element Quad labels at this level need canonical Dramatica
# verification. The structural machinery works regardless.
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
    chosen_position=QuadPosition.A,  # "pursue"
    attached_to_kind="throughline",
    attached_to_id="T_mc_oedipus",
)

MC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_mc_oedipus",
    concern_pick=MC_CONCERN_PICK,
    issue_pick=MC_ISSUE_PICK,
    problem_pick=MC_PROBLEM_PICK,
    solution_override="avoid",  # dynamic pair of "pursue"
)

# -- OS (plague investigation) in Situation Domain --
#
# Concern: "the-past" (Situation Concern Quad, position A).
# The overall story is concerned with uncovering The Past — the
# murder of Laius, the oracle's history, the infant's exposure.

OS_CONCERN_PICK = QuadPick(
    id="CP_os_plague",
    quad_id=CONCERN_SITUATION_QUAD.id,
    chosen_position=QuadPosition.A,  # "the-past"
    attached_to_kind="throughline",
    attached_to_id="T_overall_plague",
)

# Issue: "fate" from The Past Issue Quad. The OS issue is Fate —
# the inescapable events that have already happened and now must
# be uncovered. Laius's death was fated; the oracle said so.
OS_ISSUE_PICK = QuadPick(
    id="IP_os_plague",
    quad_id=ISSUE_QUAD_THE_PAST.id,
    chosen_position=QuadPosition.A,  # "fate"
    attached_to_kind="throughline",
    attached_to_id="T_overall_plague",
)

# Problem: placeholder Element Quad — the OS Problem is not yet
# assigned a canonical Element Quad (would require one of the
# 256 Element Quads under "fate"). Use a structural placeholder
# that exercises the pick-chain machinery.
ELEMENT_QUAD_FATE = Quad(
    id="element_fate",
    kind="element-quad",
    element_A="faith",
    element_B="support",
    element_C="disbelief",
    element_D="oppose",
    authored_by="dramatica-theory",
)
register_element_quad("fate", ELEMENT_QUAD_FATE)

OS_PROBLEM_PICK = QuadPick(
    id="PP_os_plague",
    quad_id=ELEMENT_QUAD_FATE.id,
    chosen_position=QuadPosition.A,  # "faith"
    attached_to_kind="throughline",
    attached_to_id="T_overall_plague",
)

OS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_overall_plague",
    concern_pick=OS_CONCERN_PICK,
    issue_pick=OS_ISSUE_PICK,
    problem_pick=OS_PROBLEM_PICK,
    solution_override="disbelief",  # dynamic pair of "faith"
)

# -- IC Jocasta in Fixed Attitude Domain --
#
# Concern: "contemplation" (Fixed Attitude Concern Quad, position C).
# Jocasta's impact stems from her contemplative stance toward the
# oracles — she contemplates (and dismisses) prophecy, and this
# fixed attitude drives her actions and her challenge to Oedipus.

IC_CONCERN_PICK = QuadPick(
    id="CP_ic_jocasta",
    quad_id=CONCERN_FIXED_ATTITUDE_QUAD.id,
    chosen_position=QuadPosition.C,  # "contemplation"
    attached_to_kind="throughline",
    attached_to_id="T_impact_jocasta",
)

# Issue: "doubt" from the Contemplation Issue Quad. Jocasta's
# contemplative stance IS doubt — doubt about the oracles, doubt
# about fate, doubt that becomes tragically ironic.
IC_ISSUE_PICK = QuadPick(
    id="IP_ic_jocasta",
    quad_id=ISSUE_QUAD_CONTEMPLATION.id,
    chosen_position=QuadPosition.D,  # "doubt"
    attached_to_kind="throughline",
    attached_to_id="T_impact_jocasta",
)

ELEMENT_QUAD_DOUBT = Quad(
    id="element_doubt",
    kind="element-quad",
    element_A="temptation",
    element_B="hinder",
    element_C="conscience",
    element_D="help",
    authored_by="dramatica-theory",
)
register_element_quad("doubt", ELEMENT_QUAD_DOUBT)

IC_PROBLEM_PICK = QuadPick(
    id="PP_ic_jocasta",
    quad_id=ELEMENT_QUAD_DOUBT.id,
    chosen_position=QuadPosition.A,  # "temptation"
    attached_to_kind="throughline",
    attached_to_id="T_impact_jocasta",
)

IC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_impact_jocasta",
    concern_pick=IC_CONCERN_PICK,
    issue_pick=IC_ISSUE_PICK,
    problem_pick=IC_PROBLEM_PICK,
    solution_override="conscience",  # dynamic pair of "temptation"
)

# -- RS (Oedipus-Jocasta marriage) in Manipulation Domain --
#
# Concern: "playing-a-role" (Manipulation Concern Quad, position B).
# The relationship IS about playing roles — husband/wife concealing
# the son/mother reality. The manipulation is structural, not
# deliberate.

RS_CONCERN_PICK = QuadPick(
    id="CP_rs_oj",
    quad_id=CONCERN_MANIPULATION_QUAD.id,
    chosen_position=QuadPosition.B,  # "playing-a-role"
    attached_to_kind="throughline",
    attached_to_id="T_relationship_oj",
)

# Issue: "desire" from the Playing A Role Issue Quad.
# The relationship's issue is Desire — Jocasta's desire to
# protect the marriage by stopping the investigation, Oedipus's
# desire to know the truth regardless.
RS_ISSUE_PICK = QuadPick(
    id="IP_rs_oj",
    quad_id=ISSUE_QUAD_PLAYING_A_ROLE.id,
    chosen_position=QuadPosition.C,  # "desire"
    attached_to_kind="throughline",
    attached_to_id="T_relationship_oj",
)

ELEMENT_QUAD_DESIRE = Quad(
    id="element_desire",
    kind="element-quad",
    element_A="logic",
    element_B="control",
    element_C="feeling",
    element_D="uncontrolled",
    authored_by="dramatica-theory",
)
register_element_quad("desire", ELEMENT_QUAD_DESIRE)

RS_PROBLEM_PICK = QuadPick(
    id="PP_rs_oj",
    quad_id=ELEMENT_QUAD_DESIRE.id,
    chosen_position=QuadPosition.C,  # "feeling"
    attached_to_kind="throughline",
    attached_to_id="T_relationship_oj",
)

RS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_relationship_oj",
    concern_pick=RS_CONCERN_PICK,
    issue_pick=RS_ISSUE_PICK,
    problem_pick=RS_PROBLEM_PICK,
    solution_override="logic",  # dynamic pair of "feeling"
)

ALL_THEMATIC_PICKS = (
    MC_THEMATIC_PICKS,
    OS_THEMATIC_PICKS,
    IC_THEMATIC_PICKS,
    RS_THEMATIC_PICKS,
)


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
