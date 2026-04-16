"""
ackroyd_dramatica_complete.py — *The Murder of Roger Ackroyd* encoded
against the `dramatica-complete` Template.

Extends ackroyd_dramatic.py (which encodes the base Dramatic dialect
records — Argument, Throughlines, Characters, Scenes, Beats, Stakes)
with the Template-specific records: DomainAssignments, Dynamic Story
Points, Signposts, ThematicPicks, and CharacterElementAssignments.

Third real encoding against dramatica-complete (after Oedipus and
Macbeth). Ackroyd pressures the Template on:

- **Different domain mapping.** Unlike both tragedies (which share
  MC=Activity, OS=Situation, IC=Fixed Attitude, RS=Manipulation),
  Ackroyd maps MC=Manipulation, OS=Activity, IC=Situation,
  RS=Fixed Attitude. This is the first encoding that exercises all
  four domains in a different arrangement.

- **First Steadfast MC.** Sheppard never changes his approach — he
  conceals from start to finish. Both Oedipus and Macbeth are
  Change MCs. This tests Resolve=Steadfast code paths.

- **First Be-er MC.** Sheppard's approach is internal — he conceals
  by *being* the trusted narrator, not by *doing* things to cover
  up. Both prior MCs are Do-ers.

- **MC-Antagonist / IC-Protagonist alignment.** Sheppard (MC) is
  also the Antagonist; Poirot (IC) is also the Protagonist. This
  is the sharpest double-function test: the character the reader
  follows IS the force opposing the story goal.

- **No double-function element ambiguity.** Unlike Macbeth (where
  Macbeth carries Protagonist+Emotion elements), here each
  archetype slot maps 1:1 to characters. Sheppard carries
  Antagonist elements only (his MC role is Throughline ownership,
  not a function label). Poirot carries Protagonist elements only.

Expected output from all three Template verifiers:

- verify_dramatica_complete: 0 observations
- verify_character_elements: 0 observations (each archetype's
  canonical pair assigned, no double-function divergences since
  function_labels are singular per character)
- verify_thematic_picks: 0 observations where chain data is
  registered
"""

from __future__ import annotations

from ackroyd_dramatic import (
    STORY, THROUGHLINES, CHARACTERS, SCENES, BEATS, STAKES,
    ARGUMENTS,
    C_poirot, C_sheppard, C_raymond, C_flora, C_raglan,
    C_blunt, C_caroline, C_ralph_paton,
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
    ISSUE_QUAD_THE_PRESENT,
    ISSUE_QUAD_PLAYING_A_ROLE,
    ISSUE_QUAD_CONTEMPLATION,
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
# Ackroyd maps to a DIFFERENT domain arrangement than the two
# tragedies. The structural reason:
#
# - MC Sheppard → Manipulation (Psychology). His personal problem
#   is psychological: he manipulates perception through the
#   manuscript, plays the role of innocent assistant, conceives
#   the plan to kill and conceal. His Throughline IS manipulation.
#
# - OS (the investigation) → Activity (Physics). The overall
#   story IS activity: investigating, interrogating, searching,
#   eliminating suspects. Detective fiction's OS is almost always
#   Activity — the case is DOING.
#
# - IC Poirot → Situation (Universe). Poirot's impact comes from
#   his situation: the retired detective who happens to settle
#   next door. His presence IS the inescapable situation Sheppard
#   cannot avoid. He doesn't change; he IS.
#
# - RS (the collaboration) → Fixed Attitude (Mind). The
#   relationship's shape is a fixed attitude held by both parties:
#   Sheppard's fixed determination to conceal, Poirot's fixed
#   suspicion once engaged. The relationship's tension is
#   attitudinal, not manipulative — Sheppard's manipulation is
#   his personal problem, not the relationship's.

DOMAIN_ASSIGNMENTS = (
    DomainAssignment(
        id="DA_overall",
        throughline_id="T_overall_case",
        domain=Domain.ACTIVITY,
    ),
    DomainAssignment(
        id="DA_mc",
        throughline_id="T_mc_sheppard",
        domain=Domain.MANIPULATION,
    ),
    DomainAssignment(
        id="DA_ic",
        throughline_id="T_ic_poirot",
        domain=Domain.SITUATION,
    ),
    DomainAssignment(
        id="DA_rel",
        throughline_id="T_rel_sheppard_poirot",
        domain=Domain.FIXED_ATTITUDE,
    ),
)


# ============================================================================
# Dynamic Story Points (Q5)
# ============================================================================
#
# - Resolve: Steadfast. Sheppard never changes his approach. He
#   conceals from start to finish, writes the manuscript as a
#   final act of concealment, and only "confesses" when Poirot
#   has already proven everything. Even the confession is a
#   performance — he writes it for the manuscript. FIRST
#   Steadfast MC in the dramatica-complete corpus.
#
# - Growth: Start. Sheppard needs to START confessing — his
#   problem is the absence of confession, not an excess of
#   action. The investigation's pressure tries to make him
#   start telling the truth.
#
# - Approach: Be-er. FIRST Be-er MC. Sheppard conceals not by
#   doing (he commits one act of violence; the rest is
#   concealment), but by being the trusted narrator-doctor. His
#   approach is internal: maintain the persona.
#
# - Limit: Optionlock. Poirot eliminates suspects one by one.
#   The investigation doesn't run out of time — it runs out of
#   alternatives. When everyone else has been eliminated, only
#   Sheppard remains.
#
# - Outcome: Success. The truth IS recovered. Poirot solves the
#   case. The OS goal is achieved.
#
# - Judgment: Bad. Catastrophic for the MC. Sheppard is exposed;
#   the novel implies he takes his own life (Poirot offers the
#   "alternative" of an overdose).
#
# Outcome × Judgment = Success × Bad = "Personal Tragedy"
# Same canonical ending as Oedipus and Macbeth — three
# structurally different stories, one ending archetype.

DYNAMIC_STORY_POINTS = (
    DynamicStoryPoint(
        id="DSP_resolve", axis=DSPAxis.RESOLVE,
        choice=Resolve.STEADFAST.value, story_id=STORY.id,
    ),
    DynamicStoryPoint(
        id="DSP_growth", axis=DSPAxis.GROWTH,
        choice=Growth.START.value, story_id=STORY.id,
    ),
    DynamicStoryPoint(
        id="DSP_approach", axis=DSPAxis.APPROACH,
        choice=Approach.BE_ER.value, story_id=STORY.id,
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

# MC in Manipulation:
# Conceiving an Idea → Playing a Role → Developing a Plan →
# Changing One's Nature
_mc_cq = CONCERN_MANIPULATION_QUAD
MC_SIGNPOSTS = (
    Signpost(id="SP_mc_1", throughline_id="T_mc_sheppard",
             signpost_position=1, signpost_element=_mc_cq.element_D),
             # conceiving-an-idea — Sheppard conceives the murder
             # plan; the blackmail drives the conception
    Signpost(id="SP_mc_2", throughline_id="T_mc_sheppard",
             signpost_position=2, signpost_element=_mc_cq.element_B),
             # playing-a-role — after the killing, he plays the
             # role of innocent narrator-assistant; the manuscript
             # IS the role
    Signpost(id="SP_mc_3", throughline_id="T_mc_sheppard",
             signpost_position=3, signpost_element=_mc_cq.element_A),
             # developing-a-plan — as Poirot closes in, Sheppard
             # develops his plan for the manuscript; each interview
             # is shaped to conceal
    Signpost(id="SP_mc_4", throughline_id="T_mc_sheppard",
             signpost_position=4, signpost_element=_mc_cq.element_C),
             # changing-one's-nature — the reveal; Sheppard's
             # nature as the killer is exposed; his performed
             # identity collapses
)

# OS in Activity:
# Learning → Understanding → Doing → Obtaining
_os_cq = CONCERN_ACTIVITY_QUAD
OS_SIGNPOSTS = (
    Signpost(id="SP_os_1", throughline_id="T_overall_case",
             signpost_position=1, signpost_element=_os_cq.element_D),
             # learning — the investigation begins; evidence
             # gathered; witnesses interviewed
    Signpost(id="SP_os_2", throughline_id="T_overall_case",
             signpost_position=2, signpost_element=_os_cq.element_A),
             # understanding — Poirot pieces together the clues;
             # the dictaphone, the moved chair, the timing
    Signpost(id="SP_os_3", throughline_id="T_overall_case",
             signpost_position=3, signpost_element=_os_cq.element_B),
             # doing — active investigation; Poirot confronts
             # suspects, Flora confesses her theft, Ursula's
             # marriage revealed
    Signpost(id="SP_os_4", throughline_id="T_overall_case",
             signpost_position=4, signpost_element=_os_cq.element_C),
             # obtaining — Poirot obtains the truth; the reveal
             # dinner; the killer named
)

# IC in Situation:
# The Present → How Things Are Changing → The Past → The Future
_ic_cq = CONCERN_SITUATION_QUAD
IC_SIGNPOSTS = (
    Signpost(id="SP_ic_1", throughline_id="T_ic_poirot",
             signpost_position=1, signpost_element=_ic_cq.element_D),
             # the-present — Poirot IS present; the retired
             # detective next door; his situation IS the impact
    Signpost(id="SP_ic_2", throughline_id="T_ic_poirot",
             signpost_position=2, signpost_element=_ic_cq.element_B),
             # how-things-are-changing — Poirot takes the case;
             # his situation changes from retired to active
    Signpost(id="SP_ic_3", throughline_id="T_ic_poirot",
             signpost_position=3, signpost_element=_ic_cq.element_A),
             # the-past — Poirot's past reputation as the world's
             # greatest detective; his past methods bear on the
             # present case
    Signpost(id="SP_ic_4", throughline_id="T_ic_poirot",
             signpost_position=4, signpost_element=_ic_cq.element_C),
             # the-future — Poirot shapes the future; the reveal
             # dinner determines what happens next for everyone
)

# RS in Fixed Attitude:
# Memories → Innermost Desires → Contemplation → Impulsive Responses
_rs_cq = CONCERN_FIXED_ATTITUDE_QUAD
RS_SIGNPOSTS = (
    Signpost(id="SP_rs_1", throughline_id="T_rel_sheppard_poirot",
             signpost_position=1, signpost_element=_rs_cq.element_D),
             # memories — the collaboration forms around shared
             # memory of the evening; what Sheppard "remembers"
             # is curated
    Signpost(id="SP_rs_2", throughline_id="T_rel_sheppard_poirot",
             signpost_position=2, signpost_element=_rs_cq.element_A),
             # innermost-desires — Sheppard desires concealment;
             # Poirot desires truth; the relationship is the
             # tension between these hidden desires
    Signpost(id="SP_rs_3", throughline_id="T_rel_sheppard_poirot",
             signpost_position=3, signpost_element=_rs_cq.element_C),
             # contemplation — the middle investigation period;
             # each contemplates the other; Sheppard wonders what
             # Poirot knows; Poirot contemplates the narrator's
             # role
    Signpost(id="SP_rs_4", throughline_id="T_rel_sheppard_poirot",
             signpost_position=4, signpost_element=_rs_cq.element_B),
             # impulsive-responses — the reveal; the
             # collaboration explodes; Poirot's confrontation
             # is the relationship's impulsive terminus
)

ALL_SIGNPOSTS = MC_SIGNPOSTS + OS_SIGNPOSTS + IC_SIGNPOSTS + RS_SIGNPOSTS
assert len(ALL_SIGNPOSTS) == 16


# ============================================================================
# Story Goal and Story Consequence (Q4)
# ============================================================================

STORY_GOAL = ("identify the killer of Roger Ackroyd and recover the "
              "truth about what happened on the night of the murder")
STORY_CONSEQUENCE = ("the killer goes undetected; Ralph Paton remains "
                     "the prime suspect; the innocent are condemned "
                     "and the guilty narrator's manuscript stands as "
                     "the accepted version")


# ============================================================================
# Character Element Assignments — Motivation Elements
# ============================================================================
#
# All 8 dramatica-8 function slots are filled by distinct characters
# (no double-function overlap at the function_label level — Sheppard's
# Antagonist label is his only function_label; his MC role is
# Throughline ownership, not a label). This means every archetype's
# canonical Motivation pair is assignable without conflict.

CHARACTER_ELEMENT_ASSIGNMENTS = (
    # Protagonist: Poirot — Pursue + Consider
    CharacterElementAssignment(
        id="CEA_poirot_pursue", character_id="C_poirot",
        element=MotivationElement.PURSUE,
    ),
    CharacterElementAssignment(
        id="CEA_poirot_consider", character_id="C_poirot",
        element=MotivationElement.CONSIDER,
    ),
    # Antagonist: Sheppard — Avoid + Reconsider
    CharacterElementAssignment(
        id="CEA_sheppard_avoid", character_id="C_sheppard",
        element=MotivationElement.AVOID,
    ),
    CharacterElementAssignment(
        id="CEA_sheppard_reconsider", character_id="C_sheppard",
        element=MotivationElement.RECONSIDER,
    ),
    # Reason: Raymond — Logic + Control
    CharacterElementAssignment(
        id="CEA_raymond_logic", character_id="C_raymond",
        element=MotivationElement.LOGIC,
    ),
    CharacterElementAssignment(
        id="CEA_raymond_control", character_id="C_raymond",
        element=MotivationElement.CONTROL,
    ),
    # Emotion: Flora — Feeling + Uncontrolled
    CharacterElementAssignment(
        id="CEA_flora_feeling", character_id="C_flora",
        element=MotivationElement.FEELING,
    ),
    CharacterElementAssignment(
        id="CEA_flora_uncontrolled", character_id="C_flora",
        element=MotivationElement.UNCONTROLLED,
    ),
    # Skeptic: Raglan — Disbelief + Oppose
    CharacterElementAssignment(
        id="CEA_raglan_disbelief", character_id="C_raglan",
        element=MotivationElement.DISBELIEF,
    ),
    CharacterElementAssignment(
        id="CEA_raglan_oppose", character_id="C_raglan",
        element=MotivationElement.OPPOSE,
    ),
    # Sidekick: Blunt — Faith + Support
    CharacterElementAssignment(
        id="CEA_blunt_faith", character_id="C_blunt",
        element=MotivationElement.FAITH,
    ),
    CharacterElementAssignment(
        id="CEA_blunt_support", character_id="C_blunt",
        element=MotivationElement.SUPPORT,
    ),
    # Guardian: Caroline — Conscience + Help
    CharacterElementAssignment(
        id="CEA_caroline_conscience", character_id="C_caroline",
        element=MotivationElement.CONSCIENCE,
    ),
    CharacterElementAssignment(
        id="CEA_caroline_help", character_id="C_caroline",
        element=MotivationElement.HELP,
    ),
    # Contagonist: Ralph Paton — Temptation + Hinder
    CharacterElementAssignment(
        id="CEA_ralph_temptation", character_id="C_ralph_paton",
        element=MotivationElement.TEMPTATION,
    ),
    CharacterElementAssignment(
        id="CEA_ralph_hinder", character_id="C_ralph_paton",
        element=MotivationElement.HINDER,
    ),
)


# ============================================================================
# ThematicPicks — all four Throughlines
# ============================================================================

# -- MC Sheppard in Manipulation Domain --
#
# Concern: "playing-a-role" (Manipulation Concern Quad, position B).
# Sheppard's concern IS playing a role — the innocent narrator,
# the helpful assistant, the concerned doctor. His entire personal
# problem is the role he maintains.

MC_CONCERN_PICK = QuadPick(
    id="CP_mc_sheppard",
    quad_id=CONCERN_MANIPULATION_QUAD.id,
    chosen_position=QuadPosition.B,  # "playing-a-role"
    attached_to_kind="throughline",
    attached_to_id="T_mc_sheppard",
)

# Issue: "desire" from Playing A Role Issue Quad. Sheppard's
# issue is Desire — desire to escape exposure, desire to maintain
# the performance, desire that drives the murder itself (he kills
# to end the blackmail that threatens his desired life).
MC_ISSUE_PICK = QuadPick(
    id="IP_mc_sheppard",
    quad_id=ISSUE_QUAD_PLAYING_A_ROLE.id,
    chosen_position=QuadPosition.C,  # "desire"
    attached_to_kind="throughline",
    attached_to_id="T_mc_sheppard",
)

ELEMENT_QUAD_DESIRE = Quad(
    id="element_desire",
    kind="element-quad",
    element_A="avoid",
    element_B="reconsider",
    element_C="pursue",
    element_D="consider",
    authored_by="dramatica-theory",
)
register_element_quad("desire", ELEMENT_QUAD_DESIRE)

MC_PROBLEM_PICK = QuadPick(
    id="PP_mc_sheppard",
    quad_id=ELEMENT_QUAD_DESIRE.id,
    chosen_position=QuadPosition.A,  # "avoid"
    attached_to_kind="throughline",
    attached_to_id="T_mc_sheppard",
)

MC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_mc_sheppard",
    concern_pick=MC_CONCERN_PICK,
    issue_pick=MC_ISSUE_PICK,
    problem_pick=MC_PROBLEM_PICK,
    solution_override="pursue",  # dynamic pair of "avoid"
)

# -- OS (the investigation) in Activity Domain --
#
# Concern: "understanding" (Activity Concern Quad, position A).
# The OS concern is Understanding — the investigation is about
# understanding what happened. Every interview, every clue, every
# deduction is in service of understanding.

OS_CONCERN_PICK = QuadPick(
    id="CP_os_case",
    quad_id=CONCERN_ACTIVITY_QUAD.id,
    chosen_position=QuadPosition.A,  # "understanding"
    attached_to_kind="throughline",
    attached_to_id="T_overall_case",
)

# Issue: "interpretation" from Understanding Issue Quad. The
# investigation's issue IS interpretation — every piece of
# evidence must be interpreted; Sheppard's narrative shapes
# how evidence is interpreted; Poirot re-interprets.
OS_ISSUE_PICK = QuadPick(
    id="IP_os_case",
    quad_id=ISSUE_QUAD_UNDERSTANDING.id,
    chosen_position=QuadPosition.C,  # "interpretation"
    attached_to_kind="throughline",
    attached_to_id="T_overall_case",
)

ELEMENT_QUAD_INTERPRETATION = Quad(
    id="element_interpretation_ackroyd",
    kind="element-quad",
    element_A="faith",
    element_B="support",
    element_C="disbelief",
    element_D="oppose",
    authored_by="dramatica-theory",
)
register_element_quad("interpretation", ELEMENT_QUAD_INTERPRETATION)

OS_PROBLEM_PICK = QuadPick(
    id="PP_os_case",
    quad_id=ELEMENT_QUAD_INTERPRETATION.id,
    chosen_position=QuadPosition.A,  # "faith"
    attached_to_kind="throughline",
    attached_to_id="T_overall_case",
)

OS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_overall_case",
    concern_pick=OS_CONCERN_PICK,
    issue_pick=OS_ISSUE_PICK,
    problem_pick=OS_PROBLEM_PICK,
    solution_override="disbelief",  # dynamic pair of "faith"
)

# -- IC Poirot in Situation Domain --
#
# Concern: "the-present" (Situation Concern Quad, position D).
# Poirot's impact is about the present — his present situation
# in King's Abbot, his present engagement with the case, his
# present attention to what others overlook.

IC_CONCERN_PICK = QuadPick(
    id="CP_ic_poirot",
    quad_id=CONCERN_SITUATION_QUAD.id,
    chosen_position=QuadPosition.D,  # "the-present"
    attached_to_kind="throughline",
    attached_to_id="T_ic_poirot",
)

# Issue: "work" from The Present Issue Quad. Poirot's impact
# IS his work — the patient investigative work he applies to
# the present situation. His grey cells are the work.
IC_ISSUE_PICK = QuadPick(
    id="IP_ic_poirot",
    quad_id=ISSUE_QUAD_THE_PRESENT.id,
    chosen_position=QuadPosition.A,  # "work"
    attached_to_kind="throughline",
    attached_to_id="T_ic_poirot",
)

ELEMENT_QUAD_WORK = Quad(
    id="element_work",
    kind="element-quad",
    element_A="logic",
    element_B="control",
    element_C="feeling",
    element_D="uncontrolled",
    authored_by="dramatica-theory",
)
register_element_quad("work", ELEMENT_QUAD_WORK)

IC_PROBLEM_PICK = QuadPick(
    id="PP_ic_poirot",
    quad_id=ELEMENT_QUAD_WORK.id,
    chosen_position=QuadPosition.A,  # "logic"
    attached_to_kind="throughline",
    attached_to_id="T_ic_poirot",
)

IC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_ic_poirot",
    concern_pick=IC_CONCERN_PICK,
    issue_pick=IC_ISSUE_PICK,
    problem_pick=IC_PROBLEM_PICK,
    solution_override="feeling",  # dynamic pair of "logic"
)

# -- RS (Sheppard-Poirot collaboration) in Fixed Attitude Domain --
#
# Concern: "contemplation" (Fixed Attitude Concern Quad, position C).
# The relationship's concern IS contemplation — each contemplates
# the other throughout the novel. Sheppard contemplates what Poirot
# knows; Poirot contemplates the narrator's reliability.

RS_CONCERN_PICK = QuadPick(
    id="CP_rs_sp",
    quad_id=CONCERN_FIXED_ATTITUDE_QUAD.id,
    chosen_position=QuadPosition.C,  # "contemplation"
    attached_to_kind="throughline",
    attached_to_id="T_rel_sheppard_poirot",
)

# Issue: "doubt" from Contemplation Issue Quad. The relationship's
# issue IS doubt — Poirot doubts the narrator (correct); Sheppard
# doubts whether his concealment will hold (also correct).
RS_ISSUE_PICK = QuadPick(
    id="IP_rs_sp",
    quad_id=ISSUE_QUAD_CONTEMPLATION.id,
    chosen_position=QuadPosition.D,  # "doubt"
    attached_to_kind="throughline",
    attached_to_id="T_rel_sheppard_poirot",
)

ELEMENT_QUAD_DOUBT = Quad(
    id="element_doubt_ackroyd",
    kind="element-quad",
    element_A="conscience",
    element_B="help",
    element_C="temptation",
    element_D="hinder",
    authored_by="dramatica-theory",
)
register_element_quad("doubt", ELEMENT_QUAD_DOUBT)

RS_PROBLEM_PICK = QuadPick(
    id="PP_rs_sp",
    quad_id=ELEMENT_QUAD_DOUBT.id,
    chosen_position=QuadPosition.C,  # "temptation"
    attached_to_kind="throughline",
    attached_to_id="T_rel_sheppard_poirot",
)

RS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_rel_sheppard_poirot",
    concern_pick=RS_CONCERN_PICK,
    issue_pick=RS_ISSUE_PICK,
    problem_pick=RS_PROBLEM_PICK,
    solution_override="conscience",  # dynamic pair of "temptation"
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
