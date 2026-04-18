"""
pride_and_prejudice_dramatica_complete.py — *Pride and Prejudice*
encoded against the `dramatica-complete` Template.

Extends pride_and_prejudice_dramatic.py (the base Dramatic dialect
records — Argument, Throughlines, Characters, Scenes, Beats, Stakes)
with the Template-specific records: DomainAssignments, Dynamic Story
Points, Signposts, ThematicPicks, and CharacterElementAssignments.

Fourth encoding against dramatica-complete (after Oedipus, Macbeth,
Ackroyd) — **and the first non-tragedy in the corpus**. The three
previous encodings all land at Personal Tragedy (Success × Bad).
Pride and Prejudice lands at Triumph (Success × Good), exercising
for the first time:

- **Judgment = Good** — untested axis direction until now.
- **The `triumph` canonical ending** — the fourth of the four
  canonical endings (alongside personal-tragedy, tragedy,
  personal-triumph).
- **The Fixed Attitude domain as MC** — prior MCs were in Activity
  (Oedipus, Macbeth) or Manipulation (Sheppard). Elizabeth's
  prejudice IS her fixed attitude; the MC Throughline is about
  its dissolution.
- **The Manipulation domain as IC** — prior ICs were in Fixed
  Attitude (Jocasta, Lady Macbeth) or Situation (Poirot). Darcy's
  impact is manipulative — he separates Bingley from Jane, pays
  off Wickham; his effect on Elizabeth is shaped by what he does.

Every dramatica-complete encoding tests whether the Template handles
a structurally different storyform cleanly. Three-in-one-corner
(three personal-tragedies) was a suspicious dataset; a Triumph is
the negative control the framework needed.

Expected output from all three Template verifiers:

- verify_dramatica_complete: 0 observations (all structural rules
  pass — 4 Throughlines, 4 DomainAssignments, 6 DSPs, 16
  Signposts, Story Goal + Consequence)
- verify_character_elements: 0 observations (all 8 archetypes'
  Motivation Elements assigned canonically; no double-function
  divergences since function_labels are singular per character)
- verify_thematic_picks: 0 observations (all four pick-chains
  validate through shipped Issue Quads)
"""

from __future__ import annotations

from story_engine.encodings.pride_and_prejudice_dramatic import (
    STORY, THROUGHLINES, CHARACTERS, SCENES, BEATS, STAKES,
    ARGUMENTS,
    C_elizabeth, C_darcy, C_lady_catherine, C_jane, C_lydia,
    C_bingley, C_mr_bennet, C_wickham,
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
    ISSUE_QUAD_CONTEMPLATION,
    ISSUE_QUAD_THE_FUTURE,
    ISSUE_QUAD_CHANGING_ONES_NATURE,
    ISSUE_QUAD_DOING,
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
# - MC Elizabeth → Fixed Attitude (Mind). Her prejudice IS a fixed
#   attitude — formed in the first ballroom scene and sustained by
#   confirmation bias until Darcy's letter forces revision. Every
#   prior MC has been in Activity or Manipulation; Elizabeth is
#   the first MC whose problem is a mental stance rather than
#   something she does.
#
# - OS (Bennet family situation) → Situation (Universe). The
#   entailed estate, the five unmarried daughters, the Regency
#   marriage market — all external state the characters must
#   navigate. The Bennet family's situation IS what the overall
#   story is about.
#
# - IC Darcy → Manipulation (Psychology). Darcy's impact on
#   Elizabeth comes from what he manipulates — Bingley's removal
#   from Jane, Wickham's payoff, the servants' regard at
#   Pemberley. His Throughline is about changing natures through
#   deliberate action, both his own and others'.
#
# - RS (Elizabeth–Darcy courtship) → Activity (Physics). The
#   relationship is an *activity* — dances, visits, walks, letters.
#   Unlike Macbeth's marriage (also RS, but in Manipulation
#   because it was a conspiracy), the Elizabeth–Darcy relationship
#   is literally about doing things together (and badly, then
#   better). First RS in Activity in the corpus.

DOMAIN_ASSIGNMENTS = (
    DomainAssignment(
        id="DA_overall",
        throughline_id="T_overall_bennets",
        domain=Domain.SITUATION,
    ),
    DomainAssignment(
        id="DA_mc",
        throughline_id="T_mc_elizabeth",
        domain=Domain.FIXED_ATTITUDE,
    ),
    DomainAssignment(
        id="DA_ic",
        throughline_id="T_ic_darcy",
        domain=Domain.MANIPULATION,
    ),
    DomainAssignment(
        id="DA_rel",
        throughline_id="T_rel_elizabeth_darcy",
        domain=Domain.ACTIVITY,
    ),
)


# ============================================================================
# Dynamic Story Points (Q5)
# ============================================================================
#
# - Resolve: Change. Elizabeth changes. Her prejudice dissolves
#   under Darcy's letter and is inverted into advocacy by the
#   Lady Catherine confrontation. Darcy also changes (pride →
#   humility), but the MC's change is the load-bearing one.
#
# - Growth: Stop. Elizabeth needs to STOP judging on first
#   impression. The problem is the excess of inference from too
#   little evidence; the growth is its cessation. (Contrast
#   Ackroyd: Start — Sheppard needs to start confessing.)
#
# - Approach: Be-er. Elizabeth's approach is internal — she
#   revises her attitude through reading, re-reading, reflection.
#   She does not DO things to solve her problem; she BE-s
#   differently as evidence accumulates. (Same as Ackroyd's
#   Sheppard, who concealed by being the trusted narrator.)
#
# - Limit: Optionlock. Circumstances narrow one by one: refuses
#   Collins (no retreat into financial safety), refuses Darcy's
#   first proposal (no retreat into wealth without honor), Lydia
#   elopes (family options close), Lady Catherine demands refusal
#   (Elizabeth's options are either capitulation or commitment).
#   Each scene removes an alternative.
#
# - Outcome: Success. The OS goal — family security, advantageous
#   marriages, resolution of the entail's pressure — is achieved.
#   Three daughters well-married; Pemberley accessible to the
#   Gardiners; the family's future secured.
#
# - Judgment: Good. FIRST GOOD JUDGMENT IN THE CORPUS. Elizabeth
#   is happy. She has revised well; the marriage rewards the
#   revision. The MC's internal resolution is positive.
#
# Outcome × Judgment = Success × Good = "Triumph"
# The fourth canonical ending, untested until this encoding.

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
        choice=Judgment.GOOD.value, story_id=STORY.id,
    ),
)

CANONICAL_ENDING = canonical_ending(
    Outcome.SUCCESS.value, Judgment.GOOD.value,
)
assert CANONICAL_ENDING == "triumph", (
    f"expected 'triumph' canonical ending for Success × Good; "
    f"got {CANONICAL_ENDING!r}"
)


# ============================================================================
# Signposts (Q7) — 4 per Throughline = 16 total
# ============================================================================

# MC in Fixed Attitude:
# Contemplation → Memories → Innermost Desires → Impulsive Responses
# (order chosen to match Elizabeth's arc: contemplates first
# impression → remembers and re-reads Darcy's letter against her
# memories → confronts her desires under Lady Catherine's pressure →
# responds with acceptance when Darcy returns)
_mc_cq = CONCERN_FIXED_ATTITUDE_QUAD
MC_SIGNPOSTS = (
    Signpost(id="SP_mc_1", throughline_id="T_mc_elizabeth",
             signpost_position=1, signpost_element=_mc_cq.element_C),
             # contemplation — Elizabeth contemplates Darcy (badly,
             # at first); forms the fixed attitude
    Signpost(id="SP_mc_2", throughline_id="T_mc_elizabeth",
             signpost_position=2, signpost_element=_mc_cq.element_D),
             # memories — after the letter she re-reads every memory
             # of Darcy and Wickham; the prejudice dissolves against
             # her own remembered evidence
    Signpost(id="SP_mc_3", throughline_id="T_mc_elizabeth",
             signpost_position=3, signpost_element=_mc_cq.element_A),
             # innermost-desires — Pemberley; she confronts what she
             # now wants, and whether she has forfeited it through
             # her first-impression habit
    Signpost(id="SP_mc_4", throughline_id="T_mc_elizabeth",
             signpost_position=4, signpost_element=_mc_cq.element_B),
             # impulsive-responses — Lady Catherine's demand; her
             # refusal to promise is the attitude's inversion into
             # advocacy
)

# OS in Situation:
# The Present → How Things Are Changing → The Past → The Future
_os_cq = CONCERN_SITUATION_QUAD
OS_SIGNPOSTS = (
    Signpost(id="SP_os_1", throughline_id="T_overall_bennets",
             signpost_position=1, signpost_element=_os_cq.element_D),
             # the-present — the Bennet family's present situation:
             # five unmarried daughters, entailed estate, Bingley
             # arriving at Netherfield
    Signpost(id="SP_os_2", throughline_id="T_overall_bennets",
             signpost_position=2, signpost_element=_os_cq.element_B),
             # how-things-are-changing — Collins's arrival, Charlotte's
             # marriage, the militia moving to Brighton; the situation
             # shifts piece by piece
    Signpost(id="SP_os_3", throughline_id="T_overall_bennets",
             signpost_position=3, signpost_element=_os_cq.element_A),
             # the-past — Lydia's elopement drags the past (Wickham's
             # history, the entail's shadow) into the present; the
             # family's past conduct determines its present jeopardy
    Signpost(id="SP_os_4", throughline_id="T_overall_bennets",
             signpost_position=4, signpost_element=_os_cq.element_C),
             # the-future — three daughters' marriages secure the
             # family's future; the entail no longer threatens the
             # surviving sisters
)

# IC in Manipulation:
# Conceiving an Idea → Developing a Plan → Playing a Role →
# Changing One's Nature
_ic_cq = CONCERN_MANIPULATION_QUAD
IC_SIGNPOSTS = (
    Signpost(id="SP_ic_1", throughline_id="T_ic_darcy",
             signpost_position=1, signpost_element=_ic_cq.element_D),
             # conceiving-an-idea — Darcy conceives the idea of
             # separating Bingley from Jane; the wrong manipulation,
             # conceived on the same prejudicial grounds Elizabeth
             # held
    Signpost(id="SP_ic_2", throughline_id="T_ic_darcy",
             signpost_position=2, signpost_element=_ic_cq.element_A),
             # developing-a-plan — the first proposal plan (bring
             # himself to offer despite the family); its rejection;
             # the letter as an unfinished plan for later action
    Signpost(id="SP_ic_3", throughline_id="T_ic_darcy",
             signpost_position=3, signpost_element=_ic_cq.element_B),
             # playing-a-role — the Wickham payoff; Darcy plays the
             # role of invisible benefactor, concealing his action
             # under the Gardiners' cover
    Signpost(id="SP_ic_4", throughline_id="T_ic_darcy",
             signpost_position=4, signpost_element=_ic_cq.element_C),
             # changing-one's-nature — the second proposal; Darcy's
             # nature is changed, and he presents the change to
             # Elizabeth for her judgment
)

# RS in Activity:
# Learning → Doing → Understanding → Obtaining
_rs_cq = CONCERN_ACTIVITY_QUAD
RS_SIGNPOSTS = (
    Signpost(id="SP_rs_1", throughline_id="T_rel_elizabeth_darcy",
             signpost_position=1, signpost_element=_rs_cq.element_D),
             # learning — first ball; each learns the other exists
             # (and dismisses)
    Signpost(id="SP_rs_2", throughline_id="T_rel_elizabeth_darcy",
             signpost_position=2, signpost_element=_rs_cq.element_B),
             # doing — Netherfield, Rosings; they do things together
             # (dancing, conversing, visiting) without understanding
             # what they are doing
    Signpost(id="SP_rs_3", throughline_id="T_rel_elizabeth_darcy",
             signpost_position=3, signpost_element=_rs_cq.element_A),
             # understanding — Pemberley and after; each now sees
             # the other truly; Darcy sees her moral quality under
             # scandal's pressure, Elizabeth sees his discretion
             # and care
    Signpost(id="SP_rs_4", throughline_id="T_rel_elizabeth_darcy",
             signpost_position=4, signpost_element=_rs_cq.element_C),
             # obtaining — second proposal walk; the relationship
             # obtains its settled form as marriage
)

ALL_SIGNPOSTS = MC_SIGNPOSTS + OS_SIGNPOSTS + IC_SIGNPOSTS + RS_SIGNPOSTS
assert len(ALL_SIGNPOSTS) == 16


# ============================================================================
# Story Goal and Story Consequence (Q4)
# ============================================================================

STORY_GOAL = ("secure the Bennet daughters' futures through "
              "advantageous marriages that rest on accurate "
              "judgment of character rather than on first "
              "impressions or financial necessity")
STORY_CONSEQUENCE = ("the Bennet daughters marry unhappily or "
                     "not at all; the family's future is "
                     "jeopardized by the entail; Elizabeth in "
                     "particular carries her prejudice forward "
                     "into an unmarried middle age")


# ============================================================================
# Character Element Assignments — Motivation Elements
# ============================================================================
#
# All 8 dramatica-8 function slots are filled by distinct characters.
# Darcy's IC role is Throughline ownership (not a second function
# label), so he carries only Guardian's canonical pair — parallel
# to Ackroyd's Poirot (Protagonist + IC) carrying only Protagonist's
# pair.

CHARACTER_ELEMENT_ASSIGNMENTS = (
    # Protagonist: Elizabeth — Pursue + Consider
    CharacterElementAssignment(
        id="CEA_elizabeth_pursue", character_id="C_elizabeth",
        element=MotivationElement.PURSUE,
    ),
    CharacterElementAssignment(
        id="CEA_elizabeth_consider", character_id="C_elizabeth",
        element=MotivationElement.CONSIDER,
    ),
    # Antagonist: Lady Catherine — Avoid + Reconsider
    CharacterElementAssignment(
        id="CEA_lady_catherine_avoid", character_id="C_lady_catherine",
        element=MotivationElement.AVOID,
    ),
    CharacterElementAssignment(
        id="CEA_lady_catherine_reconsider",
        character_id="C_lady_catherine",
        element=MotivationElement.RECONSIDER,
    ),
    # Reason: Jane — Logic + Control
    CharacterElementAssignment(
        id="CEA_jane_logic", character_id="C_jane",
        element=MotivationElement.LOGIC,
    ),
    CharacterElementAssignment(
        id="CEA_jane_control", character_id="C_jane",
        element=MotivationElement.CONTROL,
    ),
    # Emotion: Lydia — Feeling + Uncontrolled
    CharacterElementAssignment(
        id="CEA_lydia_feeling", character_id="C_lydia",
        element=MotivationElement.FEELING,
    ),
    CharacterElementAssignment(
        id="CEA_lydia_uncontrolled", character_id="C_lydia",
        element=MotivationElement.UNCONTROLLED,
    ),
    # Sidekick: Bingley — Faith + Support
    CharacterElementAssignment(
        id="CEA_bingley_faith", character_id="C_bingley",
        element=MotivationElement.FAITH,
    ),
    CharacterElementAssignment(
        id="CEA_bingley_support", character_id="C_bingley",
        element=MotivationElement.SUPPORT,
    ),
    # Skeptic: Mr. Bennet — Disbelief + Oppose
    CharacterElementAssignment(
        id="CEA_mr_bennet_disbelief", character_id="C_mr_bennet",
        element=MotivationElement.DISBELIEF,
    ),
    CharacterElementAssignment(
        id="CEA_mr_bennet_oppose", character_id="C_mr_bennet",
        element=MotivationElement.OPPOSE,
    ),
    # Guardian: Darcy — Conscience + Help
    CharacterElementAssignment(
        id="CEA_darcy_conscience", character_id="C_darcy",
        element=MotivationElement.CONSCIENCE,
    ),
    CharacterElementAssignment(
        id="CEA_darcy_help", character_id="C_darcy",
        element=MotivationElement.HELP,
    ),
    # Contagonist: Wickham — Temptation + Hinder
    CharacterElementAssignment(
        id="CEA_wickham_temptation", character_id="C_wickham",
        element=MotivationElement.TEMPTATION,
    ),
    CharacterElementAssignment(
        id="CEA_wickham_hinder", character_id="C_wickham",
        element=MotivationElement.HINDER,
    ),
)


# ============================================================================
# ThematicPicks — all four Throughlines
# ============================================================================

# -- MC Elizabeth in Fixed Attitude Domain --
#
# Concern: "contemplation" (Fixed Attitude Concern Quad, position C).
# Elizabeth's problem is how she contemplates — the mental habit of
# fixing on first impression and defending it against evidence. The
# MC Throughline IS her contemplative method.

MC_CONCERN_PICK = QuadPick(
    id="CP_mc_elizabeth",
    quad_id=CONCERN_FIXED_ATTITUDE_QUAD.id,
    chosen_position=QuadPosition.C,  # "contemplation"
    attached_to_kind="throughline",
    attached_to_id="T_mc_elizabeth",
)

# Issue: "doubt" from Contemplation Issue Quad. Elizabeth's Issue
# is Doubt — doubt of her own first impression, doubt invited by
# the letter, doubt that matures into revised certainty. The lack
# of doubt before the letter IS the problem; the arrival of doubt
# IS the solution.
MC_ISSUE_PICK = QuadPick(
    id="IP_mc_elizabeth",
    quad_id=ISSUE_QUAD_CONTEMPLATION.id,
    chosen_position=QuadPosition.D,  # "doubt"
    attached_to_kind="throughline",
    attached_to_id="T_mc_elizabeth",
)

ELEMENT_QUAD_DOUBT_PNP = Quad(
    id="element_doubt_pnp",
    kind="element-quad",
    element_A="disbelief",
    element_B="oppose",
    element_C="faith",
    element_D="support",
    authored_by="dramatica-theory",
)
register_element_quad("doubt", ELEMENT_QUAD_DOUBT_PNP)

MC_PROBLEM_PICK = QuadPick(
    id="PP_mc_elizabeth",
    quad_id=ELEMENT_QUAD_DOUBT_PNP.id,
    chosen_position=QuadPosition.A,  # "disbelief"
    attached_to_kind="throughline",
    attached_to_id="T_mc_elizabeth",
)

MC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_mc_elizabeth",
    concern_pick=MC_CONCERN_PICK,
    issue_pick=MC_ISSUE_PICK,
    problem_pick=MC_PROBLEM_PICK,
    solution_override="faith",  # dynamic pair of "disbelief"
)

# -- OS (Bennet family situation) in Situation Domain --
#
# Concern: "the-future" (Situation Concern Quad, position C). The
# overall story's concern is the Bennets' future — what happens
# after Mr. Bennet dies, who the daughters marry, whether the
# family survives the entail.

OS_CONCERN_PICK = QuadPick(
    id="CP_os_bennets",
    quad_id=CONCERN_SITUATION_QUAD.id,
    chosen_position=QuadPosition.C,  # "the-future"
    attached_to_kind="throughline",
    attached_to_id="T_overall_bennets",
)

# Issue: "preconception" from The Future Issue Quad. The
# overall story's issue is preconception — everyone's
# preconceptions about marriage, class, fortune, first
# impressions. The novel tests them all.
OS_ISSUE_PICK = QuadPick(
    id="IP_os_bennets",
    quad_id=ISSUE_QUAD_THE_FUTURE.id,
    chosen_position=QuadPosition.D,  # "preconception"
    attached_to_kind="throughline",
    attached_to_id="T_overall_bennets",
)

ELEMENT_QUAD_PRECONCEPTION = Quad(
    id="element_preconception",
    kind="element-quad",
    element_A="logic",
    element_B="control",
    element_C="feeling",
    element_D="uncontrolled",
    authored_by="dramatica-theory",
)
register_element_quad("preconception", ELEMENT_QUAD_PRECONCEPTION)

OS_PROBLEM_PICK = QuadPick(
    id="PP_os_bennets",
    quad_id=ELEMENT_QUAD_PRECONCEPTION.id,
    chosen_position=QuadPosition.A,  # "logic"
    # The overall story's Problem is Logic — specifically the
    # marriage-arithmetic logic (Mrs. Bennet's pragmatism,
    # Charlotte's calculus) that reduces daughters to incomes.
    # The Solution is Feeling — matches that rest on affection
    # between people who see each other truly.
    attached_to_kind="throughline",
    attached_to_id="T_overall_bennets",
)

OS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_overall_bennets",
    concern_pick=OS_CONCERN_PICK,
    issue_pick=OS_ISSUE_PICK,
    problem_pick=OS_PROBLEM_PICK,
    solution_override="feeling",  # dynamic pair of "logic"
)

# -- IC Darcy in Manipulation Domain --
#
# Concern: "changing-one's-nature" (Manipulation Concern Quad,
# position C). Darcy's impact on Elizabeth is driven by his own
# nature changing — and the evidence of that change is what
# Elizabeth eventually responds to.

IC_CONCERN_PICK = QuadPick(
    id="CP_ic_darcy",
    quad_id=CONCERN_MANIPULATION_QUAD.id,
    chosen_position=QuadPosition.C,  # "changing-one's-nature"
    attached_to_kind="throughline",
    attached_to_id="T_ic_darcy",
)

# Issue: "commitment" from Changing One's Nature Issue Quad.
# Darcy's issue is commitment — commitment to the change his
# letter promised, proved by the Wickham payoff and the second
# proposal.
IC_ISSUE_PICK = QuadPick(
    id="IP_ic_darcy",
    quad_id=ISSUE_QUAD_CHANGING_ONES_NATURE.id,
    chosen_position=QuadPosition.C,  # "commitment"
    attached_to_kind="throughline",
    attached_to_id="T_ic_darcy",
)

ELEMENT_QUAD_COMMITMENT_PNP = Quad(
    id="element_commitment_pnp",
    kind="element-quad",
    element_A="conscience",
    element_B="help",
    element_C="temptation",
    element_D="hinder",
    authored_by="dramatica-theory",
)
register_element_quad("commitment", ELEMENT_QUAD_COMMITMENT_PNP)

IC_PROBLEM_PICK = QuadPick(
    id="PP_ic_darcy",
    quad_id=ELEMENT_QUAD_COMMITMENT_PNP.id,
    chosen_position=QuadPosition.A,  # "conscience"
    attached_to_kind="throughline",
    attached_to_id="T_ic_darcy",
)

IC_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_ic_darcy",
    concern_pick=IC_CONCERN_PICK,
    issue_pick=IC_ISSUE_PICK,
    problem_pick=IC_PROBLEM_PICK,
    solution_override="temptation",  # dynamic pair of "conscience"
)

# -- RS (Elizabeth-Darcy courtship) in Activity Domain --
#
# Concern: "doing" (Activity Concern Quad, position B). The
# relationship IS doing — the literal activities of courtship
# in Regency England, dance by dance, letter by letter.

RS_CONCERN_PICK = QuadPick(
    id="CP_rs_ed",
    quad_id=CONCERN_ACTIVITY_QUAD.id,
    chosen_position=QuadPosition.B,  # "doing"
    attached_to_kind="throughline",
    attached_to_id="T_rel_elizabeth_darcy",
)

# Issue: "skill" from Doing Issue Quad. The relationship's
# issue is skill — the skill of reading another person under
# conditions (ballrooms, formal calls) designed to obscure
# rather than reveal. Each grows more skilled at reading the
# other as the story progresses.
RS_ISSUE_PICK = QuadPick(
    id="IP_rs_ed",
    quad_id=ISSUE_QUAD_DOING.id,
    chosen_position=QuadPosition.B,  # "skill"
    attached_to_kind="throughline",
    attached_to_id="T_rel_elizabeth_darcy",
)

ELEMENT_QUAD_SKILL_PNP = Quad(
    id="element_skill_pnp",
    kind="element-quad",
    element_A="pursue",
    element_B="consider",
    element_C="avoid",
    element_D="reconsider",
    authored_by="dramatica-theory",
)
register_element_quad("skill", ELEMENT_QUAD_SKILL_PNP)

RS_PROBLEM_PICK = QuadPick(
    id="PP_rs_ed",
    quad_id=ELEMENT_QUAD_SKILL_PNP.id,
    chosen_position=QuadPosition.D,  # "reconsider"
    # The RS's Problem is Reconsider — the relationship is stuck
    # in a mode of reconsideration (of first impressions, of the
    # other's remarks, of each other's letters) until Consider
    # (the genuine article — fresh, forward-looking attention)
    # replaces it.
    attached_to_kind="throughline",
    attached_to_id="T_rel_elizabeth_darcy",
)

RS_THEMATIC_PICKS = ThematicPicks(
    throughline_id="T_rel_elizabeth_darcy",
    concern_pick=RS_CONCERN_PICK,
    issue_pick=RS_ISSUE_PICK,
    problem_pick=RS_PROBLEM_PICK,
    solution_override="consider",  # dynamic pair of "reconsider"
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
