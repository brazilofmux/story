"""
chinatown_dramatica_complete.py — *Chinatown* (1974) encoded against
the `dramatica-complete` Template.

Extends chinatown_dramatic.py (the base Dramatic dialect records)
with the Template-specific records: DomainAssignments, Dynamic Story
Points, Signposts, ThematicPicks, and CharacterElementAssignments.

**Sixth encoding against dramatica-complete** (after Oedipus,
Macbeth, Ackroyd, Pride and Prejudice, Rocky). With this encoding
the canonical-ending matrix closes:

- **personal-tragedy** (Success × Bad) — Oedipus, Macbeth, Ackroyd
- **triumph** (Success × Good) — Pride and Prejudice
- **personal-triumph** (Failure × Good) — Rocky
- **tragedy** (Failure × Bad) — Chinatown ✓

All four canonical endings now exercised; the framework has been
pressure-tested across the entire Outcome × Judgment space.

Every DSP axis state is now exercised at least once across the
six-encoding corpus:

- Resolve: Change (5×), Steadfast (2× — Ackroyd, Rocky)
- Growth: Stop (4×), Start (2× — Ackroyd, Rocky)
- Approach: Do-er (4×), Be-er (2× — Ackroyd, P&P)
- Limit: Optionlock (5×), Timelock (1× — Rocky)
- Outcome: Success (5×), Failure (1× — Rocky... 2× with Chinatown)
- Judgment: Bad (4×), Good (2× — P&P, Rocky)

Expected output from all three Template verifiers:

- verify_dramatica_complete: 0 observations.
- verify_character_elements: 0 observations (all 8 archetypes'
  canonical Motivation pairs assigned; no double-function
  divergences).
- verify_thematic_picks: 0 observations (all four pick-chains
  validate through shipped Issue Quads).
"""

from __future__ import annotations

from chinatown_dramatic import (
    STORY, THROUGHLINES, CHARACTERS, SCENES, BEATS, STAKES,
    ARGUMENTS,
    C_jake, C_evelyn, C_cross, C_walsh, C_duffy,
    C_escobar, C_ida_sessions, C_mulvihill,
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
    # Shipped Issue Quads
    ISSUE_QUAD_UNDERSTANDING,
    ISSUE_QUAD_THE_PAST,
    ISSUE_QUAD_MEMORIES,
    ISSUE_QUAD_PLAYING_A_ROLE,
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
# - MC Jake → Activity (Physics). Jake is a PI; his Throughline
#   is the investigation — following, questioning, confronting,
#   photographing. Same domain as Oedipus, Macbeth, Rocky; the
#   Do-er MC's home.
#
# - OS (the water scheme) → Situation (Universe). The corrupt
#   state of Los Angeles's water apparatus is an external
#   situation — a condition of the city Jake investigates but
#   does not cause. Same domain as Oedipus, Macbeth, Rocky, P&P.
#
# - IC Evelyn → Fixed Attitude (Mind). Evelyn carries a fixed
#   interior attitude formed fifteen years before the story —
#   her father's abuse and her protective posture toward
#   Katherine are the fixed attitude the MC Throughline must
#   eventually open.
#
# - RS (Jake-Evelyn) → Manipulation (Psychology). The
#   relationship is mutual withholding and disclosure under
#   pressure — a psychological dance rather than the literal
#   activity of courtship (P&P's RS = Activity).

DOMAIN_ASSIGNMENTS = (
    DomainAssignment(
        id="DA_overall",
        throughline_id="T_overall_water",
        domain=Domain.SITUATION,
    ),
    DomainAssignment(
        id="DA_mc",
        throughline_id="T_mc_jake",
        domain=Domain.ACTIVITY,
    ),
    DomainAssignment(
        id="DA_ic",
        throughline_id="T_ic_evelyn",
        domain=Domain.FIXED_ATTITUDE,
    ),
    DomainAssignment(
        id="DA_rel",
        throughline_id="T_rel_jake_evelyn",
        domain=Domain.MANIPULATION,
    ),
)


# ============================================================================
# Dynamic Story Points (Q5)
# ============================================================================
#
# - Resolve: Change. Jake changes — from confident working PI
#   (pre-story Chinatown wound scarred but functional) to
#   shattered and withdrawn ('as little as possible'). Unlike
#   Oedipus and Macbeth (who change toward destruction through
#   action) or P&P (change toward happiness through revision),
#   Jake changes backward — toward withdrawal, toward the
#   Solution (Avoid) but from the wrong side of the Argument.
#
# - Growth: Stop. Jake needs to stop trying; the lesson
#   Chinatown forces on him is that trying produces what is
#   trying to be prevented. The 'forget it, Jake' is the
#   growth's articulation.
#
# - Approach: Do-er. Classic Do-er MC — investigation, physical
#   pursuit, photographing, confronting. Same as Oedipus,
#   Macbeth, Rocky.
#
# - Limit: Optionlock. Jake's options narrow through the
#   investigation — each discovery closes an alternative
#   (matrimonial case → murder → water scheme → the last
#   Chinatown scene). Not a calendar lock; an exhaustion lock.
#
# - Outcome: Failure. The OS goal — recover the truth, stop
#   Cross, protect the innocent — is not achieved. Cross gets
#   Katherine; the dam will be built; Evelyn is dead. Second
#   Failure in the corpus (after Rocky); first Failure with
#   Bad judgment.
#
# - Judgment: Bad. Jake is broken. No 'Adrian!' moment; no
#   compensation for the external loss. The film's final
#   images are Jake restrained by Escobar, walking away with
#   Walsh repeating the lesson.
#
# Outcome × Judgment = Failure × Bad = "Tragedy"
# FOURTH AND FINAL CANONICAL ENDING. The matrix closes.

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
        choice=Outcome.FAILURE.value, story_id=STORY.id,
    ),
    DynamicStoryPoint(
        id="DSP_judgment", axis=DSPAxis.JUDGMENT,
        choice=Judgment.BAD.value, story_id=STORY.id,
    ),
)

CANONICAL_ENDING = canonical_ending(
    Outcome.FAILURE.value, Judgment.BAD.value,
)
assert CANONICAL_ENDING == "tragedy", (
    f"expected 'tragedy' canonical ending for Failure × Bad; "
    f"got {CANONICAL_ENDING!r}"
)


# ============================================================================
# Signposts (Q7) — 4 per Throughline = 16 total
# ============================================================================

# MC in Activity:
# Learning → Understanding → Doing → Obtaining
_mc_cq = CONCERN_ACTIVITY_QUAD
MC_SIGNPOSTS = (
    Signpost(id="SP_mc_1", throughline_id="T_mc_jake",
             signpost_position=1, signpost_element=_mc_cq.element_D),
             # learning — the fake-Evelyn hiring; Jake learning what
             # the new case is (or what it pretends to be)
    Signpost(id="SP_mc_2", throughline_id="T_mc_jake",
             signpost_position=2, signpost_element=_mc_cq.element_A),
             # understanding — the real Evelyn's arrival; Jake
             # understanding he has been used; piecing the water
             # scheme together
    Signpost(id="SP_mc_3", throughline_id="T_mc_jake",
             signpost_position=3, signpost_element=_mc_cq.element_B),
             # doing — active investigation; the orange grove, the
             # orchard-dumping, the obituary lead, the archives
    Signpost(id="SP_mc_4", throughline_id="T_mc_jake",
             signpost_position=4, signpost_element=_mc_cq.element_C),
             # obtaining — Jake obtains the truth (the sister/
             # daughter disclosure; Cross's scheme exposed); the
             # obtaining arrives too late to save anyone
)

# OS in Situation:
# The Present → How Things Are Changing → The Past → The Future
_os_cq = CONCERN_SITUATION_QUAD
OS_SIGNPOSTS = (
    Signpost(id="SP_os_1", throughline_id="T_overall_water",
             signpost_position=1, signpost_element=_os_cq.element_D),
             # the-present — the drought, the water department, the
             # appearance of normal public business
    Signpost(id="SP_os_2", throughline_id="T_overall_water",
             signpost_position=2, signpost_element=_os_cq.element_B),
             # how-things-are-changing — Hollis's murder, the
             # orchards being poisoned, the land changing hands
             # under dead people's names
    Signpost(id="SP_os_3", throughline_id="T_overall_water",
             signpost_position=3, signpost_element=_os_cq.element_A),
             # the-past — Cross's past surfaces (the abuse of
             # Evelyn fifteen years ago; Cross's earlier control
             # of the water department under his own name)
    Signpost(id="SP_os_4", throughline_id="T_overall_water",
             signpost_position=4, signpost_element=_os_cq.element_C),
             # the-future — the dam will be built; Katherine will
             # grow up in Cross's house; the future belongs to
             # Cross, not to the investigation
)

# IC in Fixed Attitude:
# Memories → Innermost Desires → Contemplation → Impulsive Responses
# (order chosen to trace Evelyn's disclosure arc: memories that
# form the fixed attitude → desires that structure her daily life
# → contemplation as she considers disclosing to Jake → the
# impulsive flight that ends in her death)
_ic_cq = CONCERN_FIXED_ATTITUDE_QUAD
IC_SIGNPOSTS = (
    Signpost(id="SP_ic_1", throughline_id="T_ic_evelyn",
             signpost_position=1, signpost_element=_ic_cq.element_D),
             # memories — the fifteen-year-old abuse; the memory
             # that structured everything she has done since; the
             # fixed attitude's ground
    Signpost(id="SP_ic_2", throughline_id="T_ic_evelyn",
             signpost_position=2, signpost_element=_ic_cq.element_A),
             # innermost-desires — protect Katherine; keep the
             # secret; the unspoken desires that organize her
             # composed surface
    Signpost(id="SP_ic_3", throughline_id="T_ic_evelyn",
             signpost_position=3, signpost_element=_ic_cq.element_C),
             # contemplation — as Jake presses; she contemplates
             # telling him, contemplates escape, contemplates what
             # the disclosure will cost
    Signpost(id="SP_ic_4", throughline_id="T_ic_evelyn",
             signpost_position=4, signpost_element=_ic_cq.element_B),
             # impulsive-responses — the flight to Chinatown; the
             # gunshot at Cross; the attempted escape; her final
             # act is impulsive under impossible pressure
)

# RS in Manipulation:
# Playing a Role → Developing a Plan → Conceiving an Idea →
# Changing One's Nature
# (order chosen to trace the relationship's successive forms:
# detective-client role → plan to investigate together →
# conception of trust (and love) → failed nature-change at the
# disclosure scene)
_rs_cq = CONCERN_MANIPULATION_QUAD
RS_SIGNPOSTS = (
    Signpost(id="SP_rs_1", throughline_id="T_rel_jake_evelyn",
             signpost_position=1, signpost_element=_rs_cq.element_B),
             # playing-a-role — first meeting; Evelyn performs
             # aggrieved client, Jake performs professional PI;
             # each plays a role the other does not read correctly
    Signpost(id="SP_rs_2", throughline_id="T_rel_jake_evelyn",
             signpost_position=2, signpost_element=_rs_cq.element_A),
             # developing-a-plan — the real hiring; they develop
             # a collaboration; she evades, he presses; the plan
             # is mutual without being candid
    Signpost(id="SP_rs_3", throughline_id="T_rel_jake_evelyn",
             signpost_position=3, signpost_element=_rs_cq.element_D),
             # conceiving-an-idea — the affair night; an idea of
             # trust conceived without being realized; the
             # bandaging, the iris
    Signpost(id="SP_rs_4", throughline_id="T_rel_jake_evelyn",
             signpost_position=4, signpost_element=_rs_cq.element_C),
             # changing-one's-nature — the slap-confession; the
             # relationship attempts to change its nature through
             # disclosure; Chinatown takes the change away before
             # it can settle
)

ALL_SIGNPOSTS = MC_SIGNPOSTS + OS_SIGNPOSTS + IC_SIGNPOSTS + RS_SIGNPOSTS
assert len(ALL_SIGNPOSTS) == 16


# ============================================================================
# Story Goal and Story Consequence (Q4)
# ============================================================================

STORY_GOAL = ("recover the truth of Hollis Mulwray's murder and the "
              "water scheme behind it; protect the innocent "
              "(Evelyn, Katherine); stop Cross before the dam is "
              "approved")
STORY_CONSEQUENCE = ("the truth is recovered but cannot be acted on; "
                     "Cross wins the water and takes Katherine; "
                     "Evelyn is dead; Los Angeles will be watered "
                     "by Cross's dam on Cross's land; the "
                     "investigation has produced evidence nobody "
                     "will use")


# ============================================================================
# Character Element Assignments — Motivation Elements
# ============================================================================
#
# All 8 dramatica-8 function slots are filled by distinct
# characters. Every archetype's canonical Motivation pair is
# assignable without conflict. Parallels Ackroyd, Pride and
# Prejudice, and Rocky in cleanness.

CHARACTER_ELEMENT_ASSIGNMENTS = (
    # Protagonist: Jake — Pursue + Consider
    CharacterElementAssignment(
        id="CEA_jake_pursue", character_id="C_jake",
        element=MotivationElement.PURSUE,
    ),
    CharacterElementAssignment(
        id="CEA_jake_consider", character_id="C_jake",
        element=MotivationElement.CONSIDER,
    ),
    # Antagonist: Cross — Avoid + Reconsider
    CharacterElementAssignment(
        id="CEA_cross_avoid", character_id="C_cross",
        element=MotivationElement.AVOID,
    ),
    CharacterElementAssignment(
        id="CEA_cross_reconsider", character_id="C_cross",
        element=MotivationElement.RECONSIDER,
    ),
    # Reason: Walsh — Logic + Control
    CharacterElementAssignment(
        id="CEA_walsh_logic", character_id="C_walsh",
        element=MotivationElement.LOGIC,
    ),
    CharacterElementAssignment(
        id="CEA_walsh_control", character_id="C_walsh",
        element=MotivationElement.CONTROL,
    ),
    # Emotion: Evelyn — Feeling + Uncontrolled
    CharacterElementAssignment(
        id="CEA_evelyn_feeling", character_id="C_evelyn",
        element=MotivationElement.FEELING,
    ),
    CharacterElementAssignment(
        id="CEA_evelyn_uncontrolled", character_id="C_evelyn",
        element=MotivationElement.UNCONTROLLED,
    ),
    # Sidekick: Duffy — Faith + Support
    CharacterElementAssignment(
        id="CEA_duffy_faith", character_id="C_duffy",
        element=MotivationElement.FAITH,
    ),
    CharacterElementAssignment(
        id="CEA_duffy_support", character_id="C_duffy",
        element=MotivationElement.SUPPORT,
    ),
    # Skeptic: Escobar — Disbelief + Oppose
    CharacterElementAssignment(
        id="CEA_escobar_disbelief", character_id="C_escobar",
        element=MotivationElement.DISBELIEF,
    ),
    CharacterElementAssignment(
        id="CEA_escobar_oppose", character_id="C_escobar",
        element=MotivationElement.OPPOSE,
    ),
    # Guardian: Ida Sessions — Conscience + Help
    CharacterElementAssignment(
        id="CEA_ida_conscience", character_id="C_ida_sessions",
        element=MotivationElement.CONSCIENCE,
    ),
    CharacterElementAssignment(
        id="CEA_ida_help", character_id="C_ida_sessions",
        element=MotivationElement.HELP,
    ),
    # Contagonist: Mulvihill — Temptation + Hinder
    CharacterElementAssignment(
        id="CEA_mulvihill_temptation", character_id="C_mulvihill",
        element=MotivationElement.TEMPTATION,
    ),
    CharacterElementAssignment(
        id="CEA_mulvihill_hinder", character_id="C_mulvihill",
        element=MotivationElement.HINDER,
    ),
)


# ============================================================================
# ThematicPicks — all four Throughlines
# ============================================================================

# -- MC Jake in Activity Domain --
#
# Concern: "understanding" (Activity Concern Quad, position A).
# Jake's concern is understanding — what happened, who did it, who
# Evelyn is, what Chinatown really was. His MC Throughline IS the
# understanding that arrives too late.

MC_CONCERN_PICK = QuadPick(
    id="CP_mc_jake",
    quad_id=CONCERN_ACTIVITY_QUAD.id,
    chosen_position=QuadPosition.A,  # "understanding"
    attached_to_kind="throughline",
    attached_to_id="T_mc_jake",
)

# Issue: "interpretation" from Understanding Issue Quad. Jake's
# issue is interpretation — every piece of evidence means one
# thing to his first reading and another thing to the story's
# actual shape. Same Issue as Oedipus's MC pick; different
# story, different interpretation failure.
MC_ISSUE_PICK = QuadPick(
    id="IP_mc_jake",
    quad_id=ISSUE_QUAD_UNDERSTANDING.id,
    chosen_position=QuadPosition.C,  # "interpretation"
    attached_to_kind="throughline",
    attached_to_id="T_mc_jake",
)

ELEMENT_QUAD_INTERPRETATION_CT = Quad(
    id="element_interpretation_chinatown",
    kind="element-quad",
    element_A="pursue",
    element_B="consider",
    element_C="avoid",
    element_D="reconsider",
    authored_by="dramatica-theory",
)
register_element_quad("interpretation", ELEMENT_QUAD_INTERPRETATION_CT)

MC_PROBLEM_PICK = QuadPick(
    id="PP_mc_jake",
    quad_id=ELEMENT_QUAD_INTERPRETATION_CT.id,
    chosen_position=QuadPosition.A,  # "pursue"
    # Jake's Problem is Pursue — he pursues the case even when
    # the Chinatown wound is warning him. For a Change MC, the
    # Problem is held until the climactic change adopts the
    # Solution (Avoid). 'Forget it, Jake. It's Chinatown.' IS
    # the adoption of Avoid — but adopted too late, after the
    # losses the pursuit produced.
    attached_to_kind="throughline",
    attached_to_id="T_mc_jake",
)

MC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_mc_jake",
    concern_pick=MC_CONCERN_PICK,
    issue_pick=MC_ISSUE_PICK,
    problem_pick=MC_PROBLEM_PICK,
    solution_override="avoid",  # dynamic pair of "pursue"
)

# -- OS (the water scheme) in Situation Domain --
#
# Concern: "the-past" (Situation Concern Quad, position A). The
# overall story's concern is the past — Cross's past control,
# Hollis's past refusal, Evelyn's past trauma, Chinatown as the
# past that reasserts itself. Same Concern as Oedipus's OS.

OS_CONCERN_PICK = QuadPick(
    id="CP_os_water",
    quad_id=CONCERN_SITUATION_QUAD.id,
    chosen_position=QuadPosition.A,  # "the-past"
    attached_to_kind="throughline",
    attached_to_id="T_overall_water",
)

# Issue: "destiny" from The Past Issue Quad. The OS's issue is
# Destiny — the structural destiny of power like Cross's to
# continue operating, the past of Chinatown as Jake's destiny
# repeating, the city's destiny to be Cross's.
OS_ISSUE_PICK = QuadPick(
    id="IP_os_water",
    quad_id=ISSUE_QUAD_THE_PAST.id,
    chosen_position=QuadPosition.D,  # "destiny"
    attached_to_kind="throughline",
    attached_to_id="T_overall_water",
)

ELEMENT_QUAD_DESTINY = Quad(
    id="element_destiny",
    kind="element-quad",
    element_A="avoid",
    element_B="reconsider",
    element_C="pursue",
    element_D="consider",
    authored_by="dramatica-theory",
)
register_element_quad("destiny", ELEMENT_QUAD_DESTINY)

OS_PROBLEM_PICK = QuadPick(
    id="PP_os_water",
    quad_id=ELEMENT_QUAD_DESTINY.id,
    chosen_position=QuadPosition.A,  # "avoid"
    # The OS's Problem is Avoid — the city's apparatus (police,
    # press, water department) avoids confronting Cross's power.
    # The Solution is Pursue — a sustained public pursuit would
    # break the scheme. The story makes the Argument that the
    # Solution is unavailable to these institutions.
    attached_to_kind="throughline",
    attached_to_id="T_overall_water",
)

OS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_overall_water",
    concern_pick=OS_CONCERN_PICK,
    issue_pick=OS_ISSUE_PICK,
    problem_pick=OS_PROBLEM_PICK,
    solution_override="pursue",  # dynamic pair of "avoid"
)

# -- IC Evelyn in Fixed Attitude Domain --
#
# Concern: "memories" (Fixed Attitude Concern Quad, position D).
# Evelyn's impact is grounded in memory — the fifteen-year-old
# abuse, the memory of concealment she has lived inside. The IC
# Throughline is what that memory has made her.

IC_CONCERN_PICK = QuadPick(
    id="CP_ic_evelyn",
    quad_id=CONCERN_FIXED_ATTITUDE_QUAD.id,
    chosen_position=QuadPosition.D,  # "memories"
    attached_to_kind="throughline",
    attached_to_id="T_ic_evelyn",
)

# Issue: "falsehood" from Memories Issue Quad. Evelyn's issue is
# falsehood — the constructed falsehood of Katherine's parentage
# that has organized her life since the abuse; the performed
# composure that conceals the memory.
IC_ISSUE_PICK = QuadPick(
    id="IP_ic_evelyn",
    quad_id=ISSUE_QUAD_MEMORIES.id,
    chosen_position=QuadPosition.D,  # "falsehood"
    attached_to_kind="throughline",
    attached_to_id="T_ic_evelyn",
)

ELEMENT_QUAD_FALSEHOOD = Quad(
    id="element_falsehood",
    kind="element-quad",
    element_A="temptation",
    element_B="hinder",
    element_C="conscience",
    element_D="help",
    authored_by="dramatica-theory",
)
register_element_quad("falsehood", ELEMENT_QUAD_FALSEHOOD)

IC_PROBLEM_PICK = QuadPick(
    id="PP_ic_evelyn",
    quad_id=ELEMENT_QUAD_FALSEHOOD.id,
    chosen_position=QuadPosition.B,  # "hinder"
    # Evelyn's Problem is Hinder — her falsehood hinders Jake's
    # investigation, hinders her own disclosure, hinders any
    # alternative future for Katherine. The Solution is Help
    # (dynamic pair) — but her fixed attitude is constructed
    # specifically to avoid 'helping' reveal what cannot be
    # revealed safely. The Solution is unavailable to her
    # character.
    attached_to_kind="throughline",
    attached_to_id="T_ic_evelyn",
)

IC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_ic_evelyn",
    concern_pick=IC_CONCERN_PICK,
    issue_pick=IC_ISSUE_PICK,
    problem_pick=IC_PROBLEM_PICK,
    solution_override="help",  # dynamic pair of "hinder"
)

# -- RS (Jake-Evelyn) in Manipulation Domain --
#
# Concern: "playing-a-role" (Manipulation Concern Quad, position B).
# The relationship's concern is role-playing — client and detective,
# lover and lover, each presenting a face to the other that hides
# what is beneath.

RS_CONCERN_PICK = QuadPick(
    id="CP_rs_je",
    quad_id=CONCERN_MANIPULATION_QUAD.id,
    chosen_position=QuadPosition.B,  # "playing-a-role"
    attached_to_kind="throughline",
    attached_to_id="T_rel_jake_evelyn",
)

# Issue: "knowledge" from Playing A Role Issue Quad. The
# relationship's issue is knowledge — specifically the
# asymmetry of knowledge between Evelyn (who knows the truth)
# and Jake (who is trying to know it). The role-playing is the
# management of that asymmetry.
RS_ISSUE_PICK = QuadPick(
    id="IP_rs_je",
    quad_id=ISSUE_QUAD_PLAYING_A_ROLE.id,
    chosen_position=QuadPosition.A,  # "knowledge"
    attached_to_kind="throughline",
    attached_to_id="T_rel_jake_evelyn",
)

ELEMENT_QUAD_KNOWLEDGE = Quad(
    id="element_knowledge",
    kind="element-quad",
    element_A="logic",
    element_B="control",
    element_C="feeling",
    element_D="uncontrolled",
    authored_by="dramatica-theory",
)
register_element_quad("knowledge", ELEMENT_QUAD_KNOWLEDGE)

RS_PROBLEM_PICK = QuadPick(
    id="PP_rs_je",
    quad_id=ELEMENT_QUAD_KNOWLEDGE.id,
    chosen_position=QuadPosition.B,  # "control"
    # The RS's Problem is Control — each party tries to control
    # what the other knows, when the other knows it, how it
    # enters the relationship. The Solution is Uncontrolled
    # (dynamic pair) — which arrives in the slap-confession
    # scene (Evelyn finally uncontrolled) and is immediately
    # followed by Chinatown.
    attached_to_kind="throughline",
    attached_to_id="T_rel_jake_evelyn",
)

RS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_rel_jake_evelyn",
    concern_pick=RS_CONCERN_PICK,
    issue_pick=RS_ISSUE_PICK,
    problem_pick=RS_PROBLEM_PICK,
    solution_override="uncontrolled",  # dynamic pair of "control"
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
