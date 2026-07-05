"""
winter_count_dramatica_complete.py — the Dramatica storyform for THE
WINTER COUNT.

The deliberately unmarketable grid, stated once and held everywhere:

    Resolve  = STEADFAST   (no character arc — the note every editor
                            writes first, refused on purpose)
    Growth   = STOP        (the world waits for her to stop; she never does)
    Approach = DO-ER       (she acts on the world; the world loses)
    Style    = LINEAR      (a ledger mind — cause, effect, carry the one)
    Driver   = DECISION    (no storm causes anything after scene one;
                            people decide, and the deciding kills)
    Limit    = OPTIONLOCK  (ration → seed → the pass → the raid → nothing)
    Outcome  = FAILURE     (the goal is lost)
    Judgment = BAD         (and she is not redeemed by losing it)

canonical_ending(FAILURE, BAD) = "tragedy" — the cell commercial story
craft spends most of its rules preventing. The companion storyform
(The Price of Warmth, same town, same four-domain grid) lands
SUCCESS × GOOD from the identical structure: one town, one grid,
opposite polarity. That symmetry — not either story alone — is the
demonstration.

Every Dramatica appointment maps to authored events (ACT_EVENT_IDS), so
act boundaries are AUTHORED, not inferred, and drift against any of the
eight dynamics is checkable by the blind-reading evaluator.
"""

from __future__ import annotations

from story_engine.core.dramatica_template import (
    Domain, DomainAssignment, DynamicStoryPoint, Signpost,
    DSPAxis, Resolve, Growth, Approach, Limit, Outcome, Judgment,
    Driver, ProblemSolvingStyle, canonical_ending,
)

STORY_ID = "winter_count"


# ----------------------------------------------------------------------------
# Throughlines → Domains (all four domains, one each)
# ----------------------------------------------------------------------------
#
# OS  — Situation:      the sealed valley, the early winter, the short
#                       store: a circumstance everyone is trapped in.
# MC  — Fixed Attitude: Halla's creed — the count is sacred, the tally
#                       does not bend, arithmetic is mercy's only honest
#                       form. The trouble IS the settled mind.
# IC  — Manipulation:   Eirik works on her and around her — the plea,
#                       the forged chit, the extracted confession, the
#                       ultimatum, the telling. Pressure by scheme.
# RS  — Activity:       what brother and sister DO with and against each
#                       other: keeping, stealing, reconciling, telling.

DOMAIN_ASSIGNMENTS = (
    DomainAssignment(id="DA_os", throughline_id="T_os_sealed_winter",
                     domain=Domain.SITUATION),
    DomainAssignment(id="DA_mc", throughline_id="T_mc_halla",
                     domain=Domain.FIXED_ATTITUDE),
    DomainAssignment(id="DA_ic", throughline_id="T_ic_eirik",
                     domain=Domain.MANIPULATION),
    DomainAssignment(id="DA_rs", throughline_id="T_rel_siblings",
                     domain=Domain.ACTIVITY),
)


# ----------------------------------------------------------------------------
# Dynamics — all eight, single-pole (this story never wavers; the
# ambiguity machinery exists and is deliberately unused here)
# ----------------------------------------------------------------------------

DYNAMIC_STORY_POINTS = (
    DynamicStoryPoint(id="DSP_resolve", axis=DSPAxis.RESOLVE,
                      choice=Resolve.STEADFAST.value, story_id=STORY_ID),
    DynamicStoryPoint(id="DSP_growth", axis=DSPAxis.GROWTH,
                      choice=Growth.STOP.value, story_id=STORY_ID),
    DynamicStoryPoint(id="DSP_approach", axis=DSPAxis.APPROACH,
                      choice=Approach.DO_ER.value, story_id=STORY_ID),
    DynamicStoryPoint(id="DSP_pss", axis=DSPAxis.PROBLEM_SOLVING_STYLE,
                      choice=ProblemSolvingStyle.LINEAR.value,
                      story_id=STORY_ID),
    DynamicStoryPoint(id="DSP_driver", axis=DSPAxis.DRIVER,
                      choice=Driver.DECISION.value, story_id=STORY_ID),
    DynamicStoryPoint(id="DSP_limit", axis=DSPAxis.LIMIT,
                      choice=Limit.OPTIONLOCK.value, story_id=STORY_ID),
    DynamicStoryPoint(id="DSP_outcome", axis=DSPAxis.OUTCOME,
                      choice=Outcome.FAILURE.value, story_id=STORY_ID),
    DynamicStoryPoint(id="DSP_judgment", axis=DSPAxis.JUDGMENT,
                      choice=Judgment.BAD.value, story_id=STORY_ID),
)

CANONICAL_ENDING = canonical_ending(Outcome.FAILURE.value,
                                    Judgment.BAD.value)   # "tragedy"


# ----------------------------------------------------------------------------
# Signposts — four per throughline, the full sixteen
# ----------------------------------------------------------------------------

OS_SIGNPOSTS = (
    # Situation: present → future → progress → past. The act-2 position
    # is THE FUTURE on purpose: the pass vote is the town arguing about
    # its future on a number only Halla knows is false — the future is
    # debated and foreclosed in the same scene.
    Signpost(id="SP_os_1", throughline_id="T_os_sealed_winter",
             signpost_position=1, signpost_element="the-present"),
    Signpost(id="SP_os_2", throughline_id="T_os_sealed_winter",
             signpost_position=2, signpost_element="the-future"),
    Signpost(id="SP_os_3", throughline_id="T_os_sealed_winter",
             signpost_position=3, signpost_element="how-things-are-changing"),
    Signpost(id="SP_os_4", throughline_id="T_os_sealed_winter",
             signpost_position=4, signpost_element="the-past"),
)

MC_SIGNPOSTS = (
    # Fixed Attitude: memories → impulsive-responses → contemplation →
    # innermost-desires. Act 1 opens the creed's origin (Ketil on the
    # ice); act 2 is the reflex lie under a point-blank question; act 3
    # is the coldest arithmetic (truth buys nothing but panic); act 4
    # lays bare what she wanted all along — to be the trusted one — as
    # the thing her own steadfastness has made impossible.
    Signpost(id="SP_mc_1", throughline_id="T_mc_halla",
             signpost_position=1, signpost_element="memories"),
    Signpost(id="SP_mc_2", throughline_id="T_mc_halla",
             signpost_position=2, signpost_element="impulsive-responses"),
    Signpost(id="SP_mc_3", throughline_id="T_mc_halla",
             signpost_position=3, signpost_element="contemplation"),
    Signpost(id="SP_mc_4", throughline_id="T_mc_halla",
             signpost_position=4, signpost_element="innermost-desires"),
)

IC_SIGNPOSTS = (
    # Manipulation: conceiving → developing-a-plan → playing-a-role →
    # changing-one's-nature. Dramatica's bargain honored exactly: the MC
    # is steadfast, so the IC changes — and his change is not growth but
    # breakage: from cheating the count to abolishing it to walking onto
    # the ice his father was put out on.
    Signpost(id="SP_ic_1", throughline_id="T_ic_eirik",
             signpost_position=1, signpost_element="conceiving-an-idea"),
    Signpost(id="SP_ic_2", throughline_id="T_ic_eirik",
             signpost_position=2, signpost_element="developing-a-plan"),
    Signpost(id="SP_ic_3", throughline_id="T_ic_eirik",
             signpost_position=3, signpost_element="playing-a-role"),
    Signpost(id="SP_ic_4", throughline_id="T_ic_eirik",
             signpost_position=4, signpost_element="changing-one's-nature"),
)

RS_SIGNPOSTS = (
    # Activity: doing → obtaining → understanding → learning. The sibling
    # relationship moves from working the winter side by side, to each
    # obtaining a hold on the other's secret, to the confession where
    # each finally understands what the other is, to the last lesson:
    # some counts do not balance, and the ones that matter never did.
    Signpost(id="SP_rs_1", throughline_id="T_rel_siblings",
             signpost_position=1, signpost_element="doing"),
    Signpost(id="SP_rs_2", throughline_id="T_rel_siblings",
             signpost_position=2, signpost_element="obtaining"),
    Signpost(id="SP_rs_3", throughline_id="T_rel_siblings",
             signpost_position=3, signpost_element="understanding"),
    Signpost(id="SP_rs_4", throughline_id="T_rel_siblings",
             signpost_position=4, signpost_element="learning"),
)

ALL_SIGNPOSTS = OS_SIGNPOSTS + MC_SIGNPOSTS + IC_SIGNPOSTS + RS_SIGNPOSTS


# ----------------------------------------------------------------------------
# Authored act boundaries — TRUE boundaries, not positional guesses
# ----------------------------------------------------------------------------

ACT_EVENT_IDS = {
    1: (  # the-present / memories / conceiving-an-idea / doing
        "E_hard_freeze", "E_public_count", "E_rot_found", "E_the_lie",
        "E_ketil_fall", "E_eirik_asks",
    ),
    2: (  # the-future / impulsive-responses / developing-a-plan / obtaining
        "E_forged_chit", "E_shortfall", "E_sifa_dies", "E_pass_vote",
    ),
    3: (  # how-things-are-changing / contemplation / playing-a-role /
          # understanding
        "E_rations_cut", "E_confession", "E_ultimatum",
    ),
    4: (  # the-past / innermost-desires / changing-one's-nature / learning
        "E_eirik_tells", "E_the_breaking", "E_dying_weeks", "E_thaw",
    ),
}


# ----------------------------------------------------------------------------
# Goal / Consequence
# ----------------------------------------------------------------------------

STORY_GOAL = (
    "Bring every soul in Vastisetr through the sealed winter on the "
    "common store — the count holding, the compact of equal shares "
    "intact."
)

STORY_CONSEQUENCE = (
    "The compact of the count dies: the store burns, the town breaks "
    "into locked doors and teeth, the hungry dead fill the ledger's "
    "back pages, and when the pass opens the traders find a town that "
    "is mostly graves — with the Measurer still at her table, keeping "
    "the only count left."
)


# ----------------------------------------------------------------------------
# Story-specific signpost territory — folded into the dialect note by the
# demo so the renderer knows exactly what ground each act must occupy.
# ----------------------------------------------------------------------------

SIGNPOST_DETAILS = {
    # Overall Story (Situation)
    "SP_os_1": "The-present: winter a month early, the pass sealed, the "
               "public count barely clearing the season. The trap closes "
               "in scene one and every scene after is inside it.",
    "SP_os_2": "The-future: the town argues its future on the published "
               "number — the crossing to Hestfell proposed, weighed, and "
               "voted down as a needless risk. The one exit closes here, "
               "rationally, on false arithmetic.",
    "SP_os_3": "How-things-are-changing: the ration cut, trust curdling "
               "into fear, the share-lines becoming teeth-lines. The "
               "compact is visibly decaying scene by scene.",
    "SP_os_4": "The-past: the reckoning. The lie's history is told at the "
               "Beehive, the granary burns, and the spring finds the "
               "town counting what its past decisions cost.",

    # Main Character (Fixed Attitude)
    "SP_mc_1": "Memories: Ketil weighed by his own ledger and put out on "
               "the ice, his daughter watching. The creed's origin — the "
               "count is sacred BECAUSE her father broke it.",
    "SP_mc_2": "Impulsive-responses: the point-blank question at the vote "
               "— 'Does the count hold, Measurer?' — and the reflex "
               "answer that damns the town. Not a plan; a reflex, from "
               "the deepest groove of who she is.",
    "SP_mc_3": "Contemplation: the coldest arithmetic. She reasons — "
               "correctly, by her lights — that the truth now purchases "
               "nothing but panic. The reader watches a good mind defend "
               "an indefensible position without a single false step.",
    "SP_mc_4": "Innermost-desires: what she wanted was to be the trusted "
               "one, the wall that holds. The final scenes lay the want "
               "bare and deny it: she ends trusted by no one, holding a "
               "perfect count of the dead.",

    # Influence Character (Manipulation)
    "SP_ic_1": "Conceiving-an-idea: the plea for the Ostergards, and — "
               "refused — the conceiving of the forgery. His schemes "
               "start as mercy wearing her mark.",
    "SP_ic_2": "Developing-a-plan: the chit scheme running; sacks moving "
               "in the dark; covering the draws while watching his "
               "sister swear a count he can hear the seam in.",
    "SP_ic_3": "Playing-a-role: the brother-as-conscience. He holds both "
               "secrets, extracts hers, and plays the last honest man in "
               "a town of one ledger — while being its only thief.",
    "SP_ic_4": "Changing-one's-nature: the steadfast MC forces the IC's "
               "change. He stops working around the count and kills it — "
               "tells the council, throws the granary open — then walks "
               "onto his father's ice to BE the help nobody sent for.",

    # Relationship (Activity)
    "SP_rs_1": "Doing: brother and sister running the winter side by side "
               "— she counts, he pours; the town's arithmetic and the "
               "town's warmth, one household, division of labor as love.",
    "SP_rs_2": "Obtaining: each obtains a hold on the other — his theft "
               "in her books, her lie shielding his theft. The knowledge-"
               "lock IS the relationship now: mutual hostage.",
    "SP_rs_3": "Understanding: the confession in the granary. Each "
               "finally sees what the other is — she, that his crime was "
               "her creed's mirror; he, that her lie was love of the "
               "town gone rigid. Understanding changes neither. That is "
               "the point.",
    "SP_rs_4": "Learning: severance as the last lesson. He walks onto "
               "the ice; she lets him; the ice gives him back in spring. "
               "What the relationship teaches is what it costs.",
}
