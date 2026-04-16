"""
rocky_dramatica_complete.py — *Rocky* (1976) encoded against the
`dramatica-complete` Template.

Extends rocky_dramatic.py (the base Dramatic dialect records —
Argument, Throughlines, Characters, Scenes, Beats, Stakes) with the
Template-specific records: DomainAssignments, Dynamic Story Points,
Signposts, ThematicPicks, and CharacterElementAssignments.

Fifth encoding against dramatica-complete (after Oedipus, Macbeth,
Ackroyd, Pride and Prejudice). Rocky is the first Personal Triumph
in the corpus (Failure × Good) and exercises two DSP axis states
untested by any prior encoding:

- **Limit = Timelock** (first in corpus). All four prior encodings
  used Optionlock (options narrow until one remains). Rocky's
  limit is a calendar date — the fight is scheduled; the clock
  counts down; whether or not Rocky is ready, the bell rings.

- **Outcome = Failure** (first in corpus). All prior encodings had
  Outcome = Success — even the tragedies' OS goals (identify the
  killer, end the tyranny, name the murderer) resolved. Rocky's
  OS goal (a clean bicentennial publicity-stunt win for Apollo)
  is not achieved; the stunt contaminates itself.

Together with Ackroyd (Steadfast, Be-er), Rocky's **Steadfast +
Do-er** combination completes the resolve × approach matrix across
the five encodings: every combination is represented at least once.

The storyform's remaining untested corner after this encoding is
**tragedy** (Failure × Bad) — the fourth canonical ending. A sixth
encoding picking that corner would complete the ending matrix.

Expected output from all three Template verifiers:

- verify_dramatica_complete: 0 observations.
- verify_character_elements: 0 observations (all 8 archetypes'
  canonical Motivation pairs assigned; no double-function
  divergences).
- verify_thematic_picks: 0 observations (all four pick-chains
  validate through shipped Issue Quads).
"""

from __future__ import annotations

from rocky_dramatic import (
    STORY, THROUGHLINES, CHARACTERS, SCENES, BEATS, STAKES,
    ARGUMENTS,
    C_rocky, C_apollo, C_mickey, C_paulie, C_adrian,
    C_duke, C_gazzo, C_jergens,
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
    ISSUE_QUAD_DOING,
    ISSUE_QUAD_THE_PRESENT,
    ISSUE_QUAD_IMPULSIVE_RESPONSES,
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
# - MC Rocky → Activity (Physics). Rocky is a Do-er; his Throughline
#   is the training, the running, the hitting meat, the fifteen
#   rounds. Same domain as Oedipus and Macbeth; different DSP
#   axis combination (Steadfast instead of Change).
#
# - OS (the fight) → Situation (Universe). The bicentennial title
#   defense is an external state — the fight exists on calendars
#   and posters whether anyone's heart is in it. The scripting,
#   the million-dollar gate, the George Washington costume are
#   all situational scaffolding the MC must cross.
#
# - IC Apollo → Fixed Attitude (Mind). Apollo's impact comes from
#   his dismissive attitude — the fixed stance that this is a
#   stunt, a marketing exercise, a club fighter who will fall
#   down on cue. That attitude is what Rocky's fifteen rounds
#   refute.
#
# - RS (Rocky + Adrian) → Manipulation (Psychology). The
#   relationship is about shaping and being shaped — Rocky draws
#   Adrian out, Adrian draws Rocky's emotional life into
#   visibility; both are changed by the other's presence.

DOMAIN_ASSIGNMENTS = (
    DomainAssignment(
        id="DA_overall",
        throughline_id="T_overall_fight",
        domain=Domain.SITUATION,
    ),
    DomainAssignment(
        id="DA_mc",
        throughline_id="T_mc_rocky",
        domain=Domain.ACTIVITY,
    ),
    DomainAssignment(
        id="DA_ic",
        throughline_id="T_ic_apollo",
        domain=Domain.FIXED_ATTITUDE,
    ),
    DomainAssignment(
        id="DA_rel",
        throughline_id="T_rel_rocky_adrian",
        domain=Domain.MANIPULATION,
    ),
)


# ============================================================================
# Dynamic Story Points (Q5)
# ============================================================================
#
# - Resolve: Steadfast. Rocky does not change. He enters the fight
#   the same man he was in the Spider Rico club fight — a palooka
#   who can take a punch and keep standing. What changes is the
#   scale of evidence, not the man. The final 'Adrian!' is the
#   same Rocky who flirted at the pet store, writ larger.
#
# - Growth: Start. He needs to START believing the goal he has
#   named ('I just want to go the distance'). The training is the
#   starting; Mickey and Adrian are the starters.
#
# - Approach: Do-er. Action-first MC. The film is training
#   montages and the fight itself — the MC's Throughline IS doing.
#   Same as Oedipus and Macbeth.
#
# - Limit: Timelock. FIRST IN CORPUS. The fight is scheduled. The
#   calendar is the antagonist the training is racing. Apollo's
#   camp is set, Rocky's camp is set, the card will go off at its
#   time — ready or not.
#
# - Outcome: Failure. FIRST IN CORPUS. The OS goal — a clean
#   bicentennial publicity-stunt win that extends Apollo's title
#   on script — is not achieved. Apollo wins the scorecard but
#   the stunt has been contaminated by what actually happened in
#   the ring; 'ain't gonna be no rematch' is the IC conceding
#   what the scorecards don't.
#
# - Judgment: Good. Rocky's internal resolution is positive — he
#   has gone the distance, he has Adrian, he has his self-respect.
#   The film closes on Good even as the belt goes to Apollo.
#
# Outcome × Judgment = Failure × Good = "Personal Triumph"
# Third of four canonical endings now exercised (personal-tragedy
# × 3 in Oedipus/Macbeth/Ackroyd, triumph × 1 in Pride and
# Prejudice, personal-triumph × 1 in Rocky). Tragedy (Failure × Bad)
# remains the unexercised corner.

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
        choice=Approach.DO_ER.value, story_id=STORY.id,
    ),
    DynamicStoryPoint(
        id="DSP_limit", axis=DSPAxis.LIMIT,
        choice=Limit.TIMELOCK.value, story_id=STORY.id,
    ),
    DynamicStoryPoint(
        id="DSP_outcome", axis=DSPAxis.OUTCOME,
        choice=Outcome.FAILURE.value, story_id=STORY.id,
    ),
    DynamicStoryPoint(
        id="DSP_judgment", axis=DSPAxis.JUDGMENT,
        choice=Judgment.GOOD.value, story_id=STORY.id,
    ),
)

CANONICAL_ENDING = canonical_ending(
    Outcome.FAILURE.value, Judgment.GOOD.value,
)
assert CANONICAL_ENDING == "personal-triumph", (
    f"expected 'personal-triumph' canonical ending for "
    f"Failure × Good; got {CANONICAL_ENDING!r}"
)


# ============================================================================
# Signposts (Q7) — 4 per Throughline = 16 total
# ============================================================================

# MC in Activity:
# Learning → Understanding → Doing → Obtaining
_mc_cq = CONCERN_ACTIVITY_QUAD
MC_SIGNPOSTS = (
    Signpost(id="SP_mc_1", throughline_id="T_mc_rocky",
             signpost_position=1, signpost_element=_mc_cq.element_D),
             # learning — the opening; club fights, loan-sharking,
             # the pet store; Rocky is learning nothing new,
             # repeating his existence
    Signpost(id="SP_mc_2", throughline_id="T_mc_rocky",
             signpost_position=2, signpost_element=_mc_cq.element_A),
             # understanding — 'me, fight you?'; the phone call;
             # understanding what has been offered to him
    Signpost(id="SP_mc_3", throughline_id="T_mc_rocky",
             signpost_position=3, signpost_element=_mc_cq.element_B),
             # doing — the training montage; the meat, the stairs,
             # the dawn runs; the Do-er's Do-ing at full scale
    Signpost(id="SP_mc_4", throughline_id="T_mc_rocky",
             signpost_position=4, signpost_element=_mc_cq.element_C),
             # obtaining — Rocky obtains dignity through endurance;
             # he did not obtain the title, but he obtained the
             # private goal he named
)

# OS in Situation:
# The Present → How Things Are Changing → The Past → The Future
_os_cq = CONCERN_SITUATION_QUAD
OS_SIGNPOSTS = (
    Signpost(id="SP_os_1", throughline_id="T_overall_fight",
             signpost_position=1, signpost_element=_os_cq.element_D),
             # the-present — Apollo is champion; Philadelphia in
             # 1976; the bicentennial card is the present state
    Signpost(id="SP_os_2", throughline_id="T_overall_fight",
             signpost_position=2, signpost_element=_os_cq.element_B),
             # how-things-are-changing — Green's injury; the
             # scheduled opponent drops out; the card's present
             # state shifts
    Signpost(id="SP_os_3", throughline_id="T_overall_fight",
             signpost_position=3, signpost_element=_os_cq.element_A),
             # the-past — the past of boxing invoked: Apollo's
             # record, the bicentennial frame, the 'give an unknown
             # a shot' rhetoric borrowed from American mythology
    Signpost(id="SP_os_4", throughline_id="T_overall_fight",
             signpost_position=4, signpost_element=_os_cq.element_C),
             # the-future — the fight itself is the situation's
             # future; the scorecards, the 'no rematch', the
             # shape of what the card actually was
)

# IC in Fixed Attitude:
# Innermost Desires → Impulsive Responses → Contemplation → Memories
_ic_cq = CONCERN_FIXED_ATTITUDE_QUAD
IC_SIGNPOSTS = (
    Signpost(id="SP_ic_1", throughline_id="T_ic_apollo",
             signpost_position=1, signpost_element=_ic_cq.element_A),
             # innermost-desires — Apollo's desire for legacy,
             # marketing, the championship extended; the showman's
             # interior
    Signpost(id="SP_ic_2", throughline_id="T_ic_apollo",
             signpost_position=2, signpost_element=_ic_cq.element_B),
             # impulsive-responses — 'give him a shot at the
             # title'; the improvised Rocky-stunt; the dismissive
             # press response; his attitude speaks through
             # impulsive moves
    Signpost(id="SP_ic_3", throughline_id="T_ic_apollo",
             signpost_position=3, signpost_element=_ic_cq.element_C),
             # contemplation — between rounds; the realization
             # Rocky is not falling down; the contemplative shift
             # from stunt to fight
    Signpost(id="SP_ic_4", throughline_id="T_ic_apollo",
             signpost_position=4, signpost_element=_ic_cq.element_D),
             # memories — after; what Apollo will remember versus
             # what he planned to remember; 'no rematch' as the
             # closing of a memory he does not want to revisit
)

# RS in Manipulation:
# Conceiving an Idea → Developing a Plan → Playing a Role →
# Changing One's Nature
_rs_cq = CONCERN_MANIPULATION_QUAD
RS_SIGNPOSTS = (
    Signpost(id="SP_rs_1", throughline_id="T_rel_rocky_adrian",
             signpost_position=1, signpost_element=_rs_cq.element_D),
             # conceiving-an-idea — Rocky conceives the idea of
             # connecting with Adrian; the pet-store jokes are
             # the idea's first draft
    Signpost(id="SP_rs_2", throughline_id="T_rel_rocky_adrian",
             signpost_position=2, signpost_element=_rs_cq.element_A),
             # developing-a-plan — Thanksgiving forced introduction;
             # ice rink; the plan is Rocky's slow patient
             # attention
    Signpost(id="SP_rs_3", throughline_id="T_rel_rocky_adrian",
             signpost_position=3, signpost_element=_rs_cq.element_B),
             # playing-a-role — couple roles begin; Adrian present
             # at training; Rocky protective; each performing the
             # partnership they are learning
    Signpost(id="SP_rs_4", throughline_id="T_rel_rocky_adrian",
             signpost_position=4, signpost_element=_rs_cq.element_C),
             # changing-one's-nature — Adrian's nature changes;
             # the glasses come off; Rocky's emotional life
             # changes; the 'Adrian!' is the reached-for-person
             # the unreached could not have called
)

ALL_SIGNPOSTS = MC_SIGNPOSTS + OS_SIGNPOSTS + IC_SIGNPOSTS + RS_SIGNPOSTS
assert len(ALL_SIGNPOSTS) == 16


# ============================================================================
# Story Goal and Story Consequence (Q4)
# ============================================================================

STORY_GOAL = ("stage Apollo Creed's bicentennial heavyweight title "
              "defense as a clean publicity event that confirms the "
              "scripted narrative (champion versus local unknown; "
              "one-sided spectacle)")
STORY_CONSEQUENCE = ("the card is staged but the scripted narrative "
                     "is contaminated; the unknown does not fall "
                     "down; Apollo takes the scorecard but refuses "
                     "the rematch — the 'clean publicity' outcome "
                     "has been displaced by what actually "
                     "happened in the ring")


# ============================================================================
# Character Element Assignments — Motivation Elements
# ============================================================================
#
# All 8 dramatica-8 function slots are filled by distinct characters.
# Every archetype's canonical Motivation pair is assignable without
# conflict. Parallels Ackroyd and Pride and Prejudice in cleanness.

CHARACTER_ELEMENT_ASSIGNMENTS = (
    # Protagonist: Rocky — Pursue + Consider
    CharacterElementAssignment(
        id="CEA_rocky_pursue", character_id="C_rocky",
        element=MotivationElement.PURSUE,
    ),
    CharacterElementAssignment(
        id="CEA_rocky_consider", character_id="C_rocky",
        element=MotivationElement.CONSIDER,
    ),
    # Antagonist: Apollo — Avoid + Reconsider
    CharacterElementAssignment(
        id="CEA_apollo_avoid", character_id="C_apollo",
        element=MotivationElement.AVOID,
    ),
    CharacterElementAssignment(
        id="CEA_apollo_reconsider", character_id="C_apollo",
        element=MotivationElement.RECONSIDER,
    ),
    # Reason: Duke — Logic + Control
    CharacterElementAssignment(
        id="CEA_duke_logic", character_id="C_duke",
        element=MotivationElement.LOGIC,
    ),
    CharacterElementAssignment(
        id="CEA_duke_control", character_id="C_duke",
        element=MotivationElement.CONTROL,
    ),
    # Emotion: Adrian — Feeling + Uncontrolled
    CharacterElementAssignment(
        id="CEA_adrian_feeling", character_id="C_adrian",
        element=MotivationElement.FEELING,
    ),
    CharacterElementAssignment(
        id="CEA_adrian_uncontrolled", character_id="C_adrian",
        element=MotivationElement.UNCONTROLLED,
    ),
    # Sidekick: Gazzo — Faith + Support
    CharacterElementAssignment(
        id="CEA_gazzo_faith", character_id="C_gazzo",
        element=MotivationElement.FAITH,
    ),
    CharacterElementAssignment(
        id="CEA_gazzo_support", character_id="C_gazzo",
        element=MotivationElement.SUPPORT,
    ),
    # Skeptic: Jergens — Disbelief + Oppose
    CharacterElementAssignment(
        id="CEA_jergens_disbelief", character_id="C_jergens",
        element=MotivationElement.DISBELIEF,
    ),
    CharacterElementAssignment(
        id="CEA_jergens_oppose", character_id="C_jergens",
        element=MotivationElement.OPPOSE,
    ),
    # Guardian: Mickey — Conscience + Help
    CharacterElementAssignment(
        id="CEA_mickey_conscience", character_id="C_mickey",
        element=MotivationElement.CONSCIENCE,
    ),
    CharacterElementAssignment(
        id="CEA_mickey_help", character_id="C_mickey",
        element=MotivationElement.HELP,
    ),
    # Contagonist: Paulie — Temptation + Hinder
    CharacterElementAssignment(
        id="CEA_paulie_temptation", character_id="C_paulie",
        element=MotivationElement.TEMPTATION,
    ),
    CharacterElementAssignment(
        id="CEA_paulie_hinder", character_id="C_paulie",
        element=MotivationElement.HINDER,
    ),
)


# ============================================================================
# ThematicPicks — all four Throughlines
# ============================================================================

# -- MC Rocky in Activity Domain --
#
# Concern: "doing" (Activity Concern Quad, position B). Rocky's
# concern IS doing — the MC Throughline is training, action, the
# fifteen rounds. Same concern P&P's RS picked, different domain
# meaning.

MC_CONCERN_PICK = QuadPick(
    id="CP_mc_rocky",
    quad_id=CONCERN_ACTIVITY_QUAD.id,
    chosen_position=QuadPosition.B,  # "doing"
    attached_to_kind="throughline",
    attached_to_id="T_mc_rocky",
)

# Issue: "skill" from Doing Issue Quad. Rocky's issue is skill —
# the skill of fighting, the skill of enduring. His whole arc is
# the demonstration of a skill he was presumed not to have at the
# scale required.
MC_ISSUE_PICK = QuadPick(
    id="IP_mc_rocky",
    quad_id=ISSUE_QUAD_DOING.id,
    chosen_position=QuadPosition.B,  # "skill"
    attached_to_kind="throughline",
    attached_to_id="T_mc_rocky",
)

ELEMENT_QUAD_SKILL_ROCKY = Quad(
    id="element_skill_rocky",
    kind="element-quad",
    element_A="pursue",
    element_B="consider",
    element_C="avoid",
    element_D="reconsider",
    authored_by="dramatica-theory",
)
register_element_quad("skill", ELEMENT_QUAD_SKILL_ROCKY)

MC_PROBLEM_PICK = QuadPick(
    id="PP_mc_rocky",
    quad_id=ELEMENT_QUAD_SKILL_ROCKY.id,
    chosen_position=QuadPosition.B,  # "consider"
    # Rocky's Problem is Consider — specifically his habitual
    # self-consideration as a bum, a palooka, a club fighter.
    # This consideration persists even at the end ('I just want
    # to go the distance' is the articulated form of the
    # Problem). For Steadfast MCs, the Problem is held, not
    # resolved — the Solution (Reconsider) manifests through the
    # world rather than the MC's change: Adrian, the crowd,
    # Apollo's 'no rematch' all reconsider Rocky even as Rocky
    # does not quite reconsider himself.
    attached_to_kind="throughline",
    attached_to_id="T_mc_rocky",
)

MC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_mc_rocky",
    concern_pick=MC_CONCERN_PICK,
    issue_pick=MC_ISSUE_PICK,
    problem_pick=MC_PROBLEM_PICK,
    solution_override="reconsider",  # dynamic pair of "consider"
)

# -- OS (the title fight) in Situation Domain --
#
# Concern: "the-present" (Situation Concern Quad, position D). The
# overall story's concern is the present situation — Apollo's
# champion present, the scheduled fight's present, the Spectrum
# on fight night.

OS_CONCERN_PICK = QuadPick(
    id="CP_os_fight",
    quad_id=CONCERN_SITUATION_QUAD.id,
    chosen_position=QuadPosition.D,  # "the-present"
    attached_to_kind="throughline",
    attached_to_id="T_overall_fight",
)

# Issue: "attempt" from The Present Issue Quad. The OS's issue is
# Attempt — the attempt to stage the bicentennial card, the
# attempt to make the stunt hold, the attempt to extract a clean
# narrative from a live fight.
OS_ISSUE_PICK = QuadPick(
    id="IP_os_fight",
    quad_id=ISSUE_QUAD_THE_PRESENT.id,
    chosen_position=QuadPosition.D,  # "attempt"
    attached_to_kind="throughline",
    attached_to_id="T_overall_fight",
)

ELEMENT_QUAD_ATTEMPT = Quad(
    id="element_attempt",
    kind="element-quad",
    element_A="faith",
    element_B="support",
    element_C="disbelief",
    element_D="oppose",
    authored_by="dramatica-theory",
)
register_element_quad("attempt", ELEMENT_QUAD_ATTEMPT)

OS_PROBLEM_PICK = QuadPick(
    id="PP_os_fight",
    quad_id=ELEMENT_QUAD_ATTEMPT.id,
    chosen_position=QuadPosition.C,  # "disbelief"
    # The OS's Problem is Disbelief — nobody in the machinery of
    # the fight (Apollo, Jergens, the press, even Rocky at the
    # start) actually believes the card is a real contest. That
    # disbelief IS the problem; its dissolution (Faith, the
    # dynamic pair) would solve the OS — and partially does, by
    # the final round's evidence.
    attached_to_kind="throughline",
    attached_to_id="T_overall_fight",
)

OS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_overall_fight",
    concern_pick=OS_CONCERN_PICK,
    issue_pick=OS_ISSUE_PICK,
    problem_pick=OS_PROBLEM_PICK,
    solution_override="faith",  # dynamic pair of "disbelief"
)

# -- IC Apollo in Fixed Attitude Domain --
#
# Concern: "impulsive-responses" (Fixed Attitude Concern Quad,
# position B). Apollo's impact comes through his impulsive
# responses — the dismissive press answers, the improvised stunt,
# the costume choice, the confident entry.

IC_CONCERN_PICK = QuadPick(
    id="CP_ic_apollo",
    quad_id=CONCERN_FIXED_ATTITUDE_QUAD.id,
    chosen_position=QuadPosition.B,  # "impulsive-responses"
    attached_to_kind="throughline",
    attached_to_id="T_ic_apollo",
)

# Issue: "confidence" from Impulsive Responses Issue Quad.
# Apollo's issue is confidence — specifically the kind of
# confidence that dismisses without looking. His confidence is
# his asset and his blindness.
IC_ISSUE_PICK = QuadPick(
    id="IP_ic_apollo",
    quad_id=ISSUE_QUAD_IMPULSIVE_RESPONSES.id,
    chosen_position=QuadPosition.B,  # "confidence"
    attached_to_kind="throughline",
    attached_to_id="T_ic_apollo",
)

ELEMENT_QUAD_CONFIDENCE = Quad(
    id="element_confidence",
    kind="element-quad",
    element_A="avoid",
    element_B="reconsider",
    element_C="pursue",
    element_D="consider",
    authored_by="dramatica-theory",
)
register_element_quad("confidence", ELEMENT_QUAD_CONFIDENCE)

IC_PROBLEM_PICK = QuadPick(
    id="PP_ic_apollo",
    quad_id=ELEMENT_QUAD_CONFIDENCE.id,
    chosen_position=QuadPosition.A,  # "avoid"
    # Apollo's Problem is Avoid — he avoids taking Rocky
    # seriously as a competitive question (picks him precisely
    # because he doesn't look like a competitive question). The
    # Solution is Pursue — if he'd pursued real preparation the
    # ribs would have held up; but his fixed attitude has him
    # avoiding the question until round five makes avoidance
    # impossible.
    attached_to_kind="throughline",
    attached_to_id="T_ic_apollo",
)

IC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_ic_apollo",
    concern_pick=IC_CONCERN_PICK,
    issue_pick=IC_ISSUE_PICK,
    problem_pick=IC_PROBLEM_PICK,
    solution_override="pursue",  # dynamic pair of "avoid"
)

# -- RS (Rocky + Adrian) in Manipulation Domain --
#
# Concern: "changing-one's-nature" (Manipulation Concern Quad,
# position C). The relationship's concern is nature-change —
# Adrian's shell opening, Rocky's emotional life becoming
# visible. The RS Throughline IS that change.

RS_CONCERN_PICK = QuadPick(
    id="CP_rs_ra",
    quad_id=CONCERN_MANIPULATION_QUAD.id,
    chosen_position=QuadPosition.C,  # "changing-one's-nature"
    attached_to_kind="throughline",
    attached_to_id="T_rel_rocky_adrian",
)

# Issue: "commitment" from Changing One's Nature Issue Quad.
# The relationship's issue is commitment — both are committing
# to each other against long-standing solitary habits; the
# commitment is what the changing natures enable.
RS_ISSUE_PICK = QuadPick(
    id="IP_rs_ra",
    quad_id=ISSUE_QUAD_CHANGING_ONES_NATURE.id,
    chosen_position=QuadPosition.C,  # "commitment"
    attached_to_kind="throughline",
    attached_to_id="T_rel_rocky_adrian",
)

ELEMENT_QUAD_COMMITMENT_ROCKY = Quad(
    id="element_commitment_rocky",
    kind="element-quad",
    element_A="conscience",
    element_B="help",
    element_C="temptation",
    element_D="hinder",
    authored_by="dramatica-theory",
)
register_element_quad("commitment", ELEMENT_QUAD_COMMITMENT_ROCKY)

RS_PROBLEM_PICK = QuadPick(
    id="PP_rs_ra",
    quad_id=ELEMENT_QUAD_COMMITMENT_ROCKY.id,
    chosen_position=QuadPosition.D,  # "hinder"
    # The RS's Problem is Hinder — concretely, Paulie's
    # Contagonist force hindering the relationship (his drunken
    # rage, his jealousy, his throwing Adrian at Rocky). The
    # Solution is Help (dynamic pair) — Rocky and Adrian each
    # help the other emerge from their long-standing solitude;
    # the helping IS the relationship.
    attached_to_kind="throughline",
    attached_to_id="T_rel_rocky_adrian",
)

RS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_rel_rocky_adrian",
    concern_pick=RS_CONCERN_PICK,
    issue_pick=RS_ISSUE_PICK,
    problem_pick=RS_PROBLEM_PICK,
    solution_override="help",  # dynamic pair of "hinder"
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
