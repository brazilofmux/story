"""
macbeth_dramatica_complete.py — *Macbeth* encoded against the
`dramatica-complete` Template.

Extends macbeth_dramatic.py (which encodes the base Dramatic dialect
records — Argument, Throughlines, Characters, Scenes, Beats, Stakes)
with the Template-specific records: DomainAssignments, Dynamic Story
Points, Signposts, ThematicPicks, and CharacterElementAssignments.

Second real encoding against dramatica-complete (parallel to
oedipus_dramatica_complete.py). Macbeth pressures the Template on:

- **Double-function Characters.** Macbeth is both Protagonist and
  Emotion; Macduff is both Antagonist and Skeptic. These produce
  archetype_element_divergence observations by design — the
  canonical pairs for two functions cannot both be assigned to
  one character without duplication.

- **Steadfast MC reading.** Unlike Oedipus (Change), Macbeth is
  read here as Change — he adopts Lady Macbeth's aggressive
  posture. This is a defensible but debatable interpretation;
  a Steadfast reading is equally valid. The encoding documents
  the choice.

- **Same domain mapping as Oedipus** (MC=Activity, OS=Situation,
  IC=Fixed Attitude, RS=Manipulation). This is not accidental:
  both are classical tragedies with action-first MCs and
  philosophical IC oppositions. A future encoding could test
  whether different domain assignments produce different
  observations.

Expected output from all three Template verifiers:

- verify_dramatica_complete: 0 observations (all structural rules
  pass — 4 Throughlines, 4 DomainAssignments, 6 DSPs, 16
  Signposts, Story Goal + Consequence)
- verify_character_elements: archetype_element_divergence
  observations for Macbeth (Protagonist+Emotion) and Macduff
  (Antagonist+Skeptic), since each carries only one function's
  canonical Motivation pair
- verify_thematic_picks: 0 observations where chain data is
  registered
"""

from __future__ import annotations

from story_engine.encodings.macbeth_dramatic import (
    STORY, THROUGHLINES, CHARACTERS, SCENES, BEATS, STAKES,
    ARGUMENTS,
    C_macbeth, C_lady_macbeth, C_macduff, C_banquo, C_malcolm,
    C_witches,
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
    ISSUE_QUAD_DOING,
    ISSUE_QUAD_HOW_THINGS_ARE_CHANGING,
    ISSUE_QUAD_INNERMOST_DESIRES,
    ISSUE_QUAD_CHANGING_ONES_NATURE,
    verify_dramatica_complete,
    verify_character_elements,
    verify_thematic_picks,
    canonical_ending,
    register_element_quad,
    Quad,
)


# ============================================================================
# Domain Assignments (Q3)
# ============================================================================
#
# - Overall Story (Scotland's crisis) → Situation (an external
#   state — the kingdom is usurped, the succession broken)
# - MC Macbeth → Activity (he acts: kills Duncan, orders Banquo
#   killed, orders the Macduff family killed, fights Macduff)
# - IC Lady Macbeth → Fixed Attitude (her fixed demand that he
#   kill, her inability to bear what she demanded; her mindset
#   is what impacts the MC)
# - Relationship (the marriage) → Manipulation (a conspiracy;
#   roles played; natures changed by what they've done together)

DOMAIN_ASSIGNMENTS = (
    DomainAssignment(
        id="DA_overall",
        throughline_id="T_overall_scotland",
        domain=Domain.SITUATION,
    ),
    DomainAssignment(
        id="DA_mc",
        throughline_id="T_mc_macbeth",
        domain=Domain.ACTIVITY,
    ),
    DomainAssignment(
        id="DA_ic",
        throughline_id="T_impact_lady_macbeth",
        domain=Domain.FIXED_ATTITUDE,
    ),
    DomainAssignment(
        id="DA_rel",
        throughline_id="T_relationship_macbeths",
        domain=Domain.MANIPULATION,
    ),
)


# ============================================================================
# Dynamic Story Points (Q5)
# ============================================================================
#
# - Resolve: Change (Macbeth changes — adopts Lady Macbeth's
#   aggressive posture; starts hesitant, becomes ruthless.
#   A Steadfast reading is defensible: he never abandons
#   ambition. This encoding reads the Act 1 hesitation as
#   his initial position and the escalating killings as the
#   Change from that position.)
# - Growth: Stop (he must stop pursuing power — he cannot)
# - Approach: Do-er (he kills with his own hands, orders
#   killings, fights to the death)
# - Limit: Optionlock (his protections collapse one by one:
#   Banquo dead but Fleance escapes, the prophecy's terms
#   met literally, his army deserts)
# - Outcome: Success (the OS problem IS resolved — Scotland's
#   rightful king is crowned; the plague of tyranny ends)
# - Judgment: Bad (catastrophic for the MC personally)
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

# MC in Activity:
# Learning → Doing → Understanding → Obtaining
_mc_cq = CONCERN_ACTIVITY_QUAD
MC_SIGNPOSTS = (
    Signpost(id="SP_mc_1", throughline_id="T_mc_macbeth",
             signpost_position=1, signpost_element=_mc_cq.element_D),
             # learning — hears the prophecy; gathers information
             # about what he might become
    Signpost(id="SP_mc_2", throughline_id="T_mc_macbeth",
             signpost_position=2, signpost_element=_mc_cq.element_B),
             # doing — kills Duncan; kills Banquo; the doing phase
             # where he acts on ambition
    Signpost(id="SP_mc_3", throughline_id="T_mc_macbeth",
             signpost_position=3, signpost_element=_mc_cq.element_A),
             # understanding — banquet ghost; the second prophecy;
             # he begins to understand what he has become
    Signpost(id="SP_mc_4", throughline_id="T_mc_macbeth",
             signpost_position=4, signpost_element=_mc_cq.element_C),
             # obtaining — obtains the prophecy's true meaning
             # (Birnam Wood, Caesarean birth) and obtains death
)

# OS in Situation:
# The Present → How Things Are Changing → The Past → The Future
_os_cq = CONCERN_SITUATION_QUAD
OS_SIGNPOSTS = (
    Signpost(id="SP_os_1", throughline_id="T_overall_scotland",
             signpost_position=1, signpost_element=_os_cq.element_D),
             # the-present — Scotland IS in a present state of
             # order under Duncan; the play opens here
    Signpost(id="SP_os_2", throughline_id="T_overall_scotland",
             signpost_position=2, signpost_element=_os_cq.element_B),
             # how-things-are-changing — the regicide; the crown
             # usurped; Scotland changes from order to tyranny
    Signpost(id="SP_os_3", throughline_id="T_overall_scotland",
             signpost_position=3, signpost_element=_os_cq.element_A),
             # the-past — the past catches up; Banquo's ghost;
             # the murdered king's legacy; the past crimes
             # compound into present instability
    Signpost(id="SP_os_4", throughline_id="T_overall_scotland",
             signpost_position=4, signpost_element=_os_cq.element_C),
             # the-future — Malcolm's army; the future of
             # Scotland being fought for; restoration
)

# IC in Fixed Attitude:
# Innermost Desires → Impulsive Responses → Contemplation → Memories
_ic_cq = CONCERN_FIXED_ATTITUDE_QUAD
IC_SIGNPOSTS = (
    Signpost(id="SP_ic_1", throughline_id="T_impact_lady_macbeth",
             signpost_position=1, signpost_element=_ic_cq.element_A),
             # innermost-desires — her desire for the crown;
             # "unsex me here"; the fixed desire that drives the MC
    Signpost(id="SP_ic_2", throughline_id="T_impact_lady_macbeth",
             signpost_position=2, signpost_element=_ic_cq.element_B),
             # impulsive-responses — she chides Macbeth's
             # hesitation; handles the daggers; smears the grooms;
             # her impulsive force carries the regicide
    Signpost(id="SP_ic_3", throughline_id="T_impact_lady_macbeth",
             signpost_position=3, signpost_element=_ic_cq.element_C),
             # contemplation — the banquet cover; she contemplates
             # what they have done; she can no longer reach him
    Signpost(id="SP_ic_4", throughline_id="T_impact_lady_macbeth",
             signpost_position=4, signpost_element=_ic_cq.element_D),
             # memories — the sleepwalking; she cannot escape the
             # memory of the blood; "all the perfumes of Arabia"
)

# RS in Manipulation:
# Conceiving an Idea → Playing a Role → Developing a Plan →
# Changing One's Nature
_rs_cq = CONCERN_MANIPULATION_QUAD
RS_SIGNPOSTS = (
    Signpost(id="SP_rs_1", throughline_id="T_relationship_macbeths",
             signpost_position=1, signpost_element=_rs_cq.element_D),
             # conceiving-an-idea — the letter; the marriage
             # conceives the shared project of regicide
    Signpost(id="SP_rs_2", throughline_id="T_relationship_macbeths",
             signpost_position=2, signpost_element=_rs_cq.element_B),
             # playing-a-role — the host and hostess playing their
             # roles while plotting murder in their house
    Signpost(id="SP_rs_3", throughline_id="T_relationship_macbeths",
             signpost_position=3, signpost_element=_rs_cq.element_A),
             # developing-a-plan — after Duncan, the marriage
             # develops further plans; but Macbeth starts planning
             # alone (Banquo's killing)
    Signpost(id="SP_rs_4", throughline_id="T_relationship_macbeths",
             signpost_position=4, signpost_element=_rs_cq.element_C),
             # changing-one's-nature — the marriage changes its
             # nature from conspiracy to isolation; both are
             # changed by what they have done
)

ALL_SIGNPOSTS = MC_SIGNPOSTS + OS_SIGNPOSTS + IC_SIGNPOSTS + RS_SIGNPOSTS
assert len(ALL_SIGNPOSTS) == 16


# ============================================================================
# Story Goal and Story Consequence (Q4)
# ============================================================================

STORY_GOAL = ("restore Scotland's rightful succession and end the "
              "tyranny of the usurper")
STORY_CONSEQUENCE = ("Scotland remains under Macbeth's tyranny; the "
                     "natural order stays broken; the unnatural omens "
                     "continue")


# ============================================================================
# Character Element Assignments — Motivation Elements
# ============================================================================
#
# Macbeth uses the 8 archetypes from macbeth_dramatic.py's
# character_function_template="dramatica-8". Two characters carry
# double functions:
#   - Macbeth: Protagonist + Emotion
#   - Macduff: Antagonist + Skeptic
#
# Each character gets its PRIMARY function's canonical Motivation
# pair. The verifier will produce archetype_element_divergence
# observations for the SECONDARY functions, which is correct:
# these are complex characters whose element assignments reflect
# their dominant narrative function.

CHARACTER_ELEMENT_ASSIGNMENTS = (
    # Protagonist: Macbeth — Pursue + Consider
    # (also Emotion, but assigned Protagonist's canonical pair;
    # divergence from Emotion will be noted)
    CharacterElementAssignment(
        id="CEA_macbeth_pursue", character_id="C_macbeth",
        element=MotivationElement.PURSUE,
    ),
    CharacterElementAssignment(
        id="CEA_macbeth_consider", character_id="C_macbeth",
        element=MotivationElement.CONSIDER,
    ),
    # Antagonist: Macduff — Avoid + Reconsider
    # (also Skeptic; divergence from Skeptic will be noted)
    CharacterElementAssignment(
        id="CEA_macduff_avoid", character_id="C_macduff",
        element=MotivationElement.AVOID,
    ),
    CharacterElementAssignment(
        id="CEA_macduff_reconsider", character_id="C_macduff",
        element=MotivationElement.RECONSIDER,
    ),
    # Contagonist: Lady Macbeth — Temptation + Hinder
    CharacterElementAssignment(
        id="CEA_ladymacbeth_temptation", character_id="C_lady_macbeth",
        element=MotivationElement.TEMPTATION,
    ),
    CharacterElementAssignment(
        id="CEA_ladymacbeth_hinder", character_id="C_lady_macbeth",
        element=MotivationElement.HINDER,
    ),
    # Sidekick: Banquo — Faith + Support
    CharacterElementAssignment(
        id="CEA_banquo_faith", character_id="C_banquo",
        element=MotivationElement.FAITH,
    ),
    CharacterElementAssignment(
        id="CEA_banquo_support", character_id="C_banquo",
        element=MotivationElement.SUPPORT,
    ),
    # Reason: Malcolm — Logic + Control
    CharacterElementAssignment(
        id="CEA_malcolm_logic", character_id="C_malcolm",
        element=MotivationElement.LOGIC,
    ),
    CharacterElementAssignment(
        id="CEA_malcolm_control", character_id="C_malcolm",
        element=MotivationElement.CONTROL,
    ),
    # Guardian: the Witches — Conscience + Help
    CharacterElementAssignment(
        id="CEA_witches_conscience", character_id="C_witches",
        element=MotivationElement.CONSCIENCE,
    ),
    CharacterElementAssignment(
        id="CEA_witches_help", character_id="C_witches",
        element=MotivationElement.HELP,
    ),
)

# Note: Feeling, Uncontrolled (Emotion's canonical pair) and
# Disbelief, Oppose (Skeptic's canonical pair) are unassigned
# because Macbeth and Macduff carry their primary function's
# elements instead. This is honest: a complex character can't
# hold both functions' full element sets without duplication
# pressure on the rest of the cast.


# ============================================================================
# ThematicPicks — all four Throughlines
# ============================================================================

# -- MC Macbeth in Activity Domain --
#
# Concern: "doing" (Activity Concern Quad, position B).
# Macbeth's concern is Doing — he IS the action-first MC,
# killing his way to and through the crown.

MC_CONCERN_PICK = QuadPick(
    id="CP_mc_macbeth",
    quad_id=CONCERN_ACTIVITY_QUAD.id,
    chosen_position=QuadPosition.B,  # "doing"
    attached_to_kind="throughline",
    attached_to_id="T_mc_macbeth",
)

# Issue: "skill" from the Doing Issue Quad. Macbeth's skill as a
# warrior is what makes the regicide possible; his issue is whether
# his capability justifies its exercise.
MC_ISSUE_PICK = QuadPick(
    id="IP_mc_macbeth",
    quad_id=ISSUE_QUAD_DOING.id,
    chosen_position=QuadPosition.B,  # "skill"
    attached_to_kind="throughline",
    attached_to_id="T_mc_macbeth",
)

ELEMENT_QUAD_SKILL = Quad(
    id="element_skill",
    kind="element-quad",
    element_A="pursue",
    element_B="consider",
    element_C="avoid",
    element_D="reconsider",
    authored_by="dramatica-theory",
)
register_element_quad("skill", ELEMENT_QUAD_SKILL)

MC_PROBLEM_PICK = QuadPick(
    id="PP_mc_macbeth",
    quad_id=ELEMENT_QUAD_SKILL.id,
    chosen_position=QuadPosition.A,  # "pursue"
    attached_to_kind="throughline",
    attached_to_id="T_mc_macbeth",
)

MC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_mc_macbeth",
    concern_pick=MC_CONCERN_PICK,
    issue_pick=MC_ISSUE_PICK,
    problem_pick=MC_PROBLEM_PICK,
    solution_override="avoid",  # dynamic pair of "pursue"
)

# -- OS (Scotland's crisis) in Situation Domain --
#
# Concern: "how-things-are-changing" (Situation Concern Quad,
# position B). Scotland is changing — from order to tyranny and
# back again. The OS concern IS the change.

OS_CONCERN_PICK = QuadPick(
    id="CP_os_scotland",
    quad_id=CONCERN_SITUATION_QUAD.id,
    chosen_position=QuadPosition.B,  # "how-things-are-changing"
    attached_to_kind="throughline",
    attached_to_id="T_overall_scotland",
)

# Issue: "threat" from How Things Are Changing Issue Quad.
# Scotland is under threat — of tyranny, of unnatural succession,
# of the moral order collapsing.
OS_ISSUE_PICK = QuadPick(
    id="IP_os_scotland",
    quad_id=ISSUE_QUAD_HOW_THINGS_ARE_CHANGING.id,
    chosen_position=QuadPosition.C,  # "threat"
    attached_to_kind="throughline",
    attached_to_id="T_overall_scotland",
)

ELEMENT_QUAD_THREAT = Quad(
    id="element_threat",
    kind="element-quad",
    element_A="faith",
    element_B="support",
    element_C="disbelief",
    element_D="oppose",
    authored_by="dramatica-theory",
)
register_element_quad("threat", ELEMENT_QUAD_THREAT)

OS_PROBLEM_PICK = QuadPick(
    id="PP_os_scotland",
    quad_id=ELEMENT_QUAD_THREAT.id,
    chosen_position=QuadPosition.C,  # "disbelief"
    attached_to_kind="throughline",
    attached_to_id="T_overall_scotland",
)

OS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_overall_scotland",
    concern_pick=OS_CONCERN_PICK,
    issue_pick=OS_ISSUE_PICK,
    problem_pick=OS_PROBLEM_PICK,
    solution_override="faith",  # dynamic pair of "disbelief"
)

# -- IC Lady Macbeth in Fixed Attitude Domain --
#
# Concern: "innermost-desires" (Fixed Attitude Concern Quad,
# position A). Lady Macbeth's fixed attitude IS her innermost
# desire for the crown and what it represents — power, arrival,
# the final form of ambition.

IC_CONCERN_PICK = QuadPick(
    id="CP_ic_ladymacbeth",
    quad_id=CONCERN_FIXED_ATTITUDE_QUAD.id,
    chosen_position=QuadPosition.A,  # "innermost-desires"
    attached_to_kind="throughline",
    attached_to_id="T_impact_lady_macbeth",
)

# Issue: "hope" from the Innermost Desires Issue Quad. Lady
# Macbeth's impact on the MC is driven by hope — hope for the
# crown, hope that the killing will be worth it, hope that
# collapses into the sleepwalking.
IC_ISSUE_PICK = QuadPick(
    id="IP_ic_ladymacbeth",
    quad_id=ISSUE_QUAD_INNERMOST_DESIRES.id,
    chosen_position=QuadPosition.B,  # "hope"
    attached_to_kind="throughline",
    attached_to_id="T_impact_lady_macbeth",
)

ELEMENT_QUAD_HOPE = Quad(
    id="element_hope",
    kind="element-quad",
    element_A="temptation",
    element_B="hinder",
    element_C="conscience",
    element_D="help",
    authored_by="dramatica-theory",
)
register_element_quad("hope", ELEMENT_QUAD_HOPE)

IC_PROBLEM_PICK = QuadPick(
    id="PP_ic_ladymacbeth",
    quad_id=ELEMENT_QUAD_HOPE.id,
    chosen_position=QuadPosition.A,  # "temptation"
    attached_to_kind="throughline",
    attached_to_id="T_impact_lady_macbeth",
)

IC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_impact_lady_macbeth",
    concern_pick=IC_CONCERN_PICK,
    issue_pick=IC_ISSUE_PICK,
    problem_pick=IC_PROBLEM_PICK,
    solution_override="conscience",  # dynamic pair of "temptation"
)

# -- RS (the Macbeths' marriage) in Manipulation Domain --
#
# Concern: "changing-one's-nature" (Manipulation Concern Quad,
# position C). The marriage IS about changing one's nature —
# from loyal subjects to regicides, from partners to isolates,
# from human to inhuman.

RS_CONCERN_PICK = QuadPick(
    id="CP_rs_macbeths",
    quad_id=CONCERN_MANIPULATION_QUAD.id,
    chosen_position=QuadPosition.C,  # "changing-one's-nature"
    attached_to_kind="throughline",
    attached_to_id="T_relationship_macbeths",
)

# Issue: "commitment" from Changing One's Nature Issue Quad.
# The marriage's issue IS commitment — their commitment to the
# conspiracy, the unraveling of that commitment as the cost
# becomes visible.
RS_ISSUE_PICK = QuadPick(
    id="IP_rs_macbeths",
    quad_id=ISSUE_QUAD_CHANGING_ONES_NATURE.id,
    chosen_position=QuadPosition.C,  # "commitment"
    attached_to_kind="throughline",
    attached_to_id="T_relationship_macbeths",
)

ELEMENT_QUAD_COMMITMENT = Quad(
    id="element_commitment",
    kind="element-quad",
    element_A="logic",
    element_B="control",
    element_C="feeling",
    element_D="uncontrolled",
    authored_by="dramatica-theory",
)
register_element_quad("commitment", ELEMENT_QUAD_COMMITMENT)

RS_PROBLEM_PICK = QuadPick(
    id="PP_rs_macbeths",
    quad_id=ELEMENT_QUAD_COMMITMENT.id,
    chosen_position=QuadPosition.C,  # "feeling"
    attached_to_kind="throughline",
    attached_to_id="T_relationship_macbeths",
)

RS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_relationship_macbeths",
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
