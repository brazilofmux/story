"""
rocky_dramatic_three_actor.py — Rocky under the general DRAMATIC dialect,
with the MINIMAL three-actor template.

A deliberate contrast. `rocky_dramatica_complete.py` encodes Rocky under
the heaviest Template (the full Dramatica storyform — four throughlines,
sixteen signposts, the six dynamics, the element hierarchy). This file
encodes the SAME substrate (`rocky.py`) under the leanest possible
structure the parent dialect offers: the three-actor template
(Hero / Obstacle / Helper), one thematic Argument, a couple of
Throughlines, and the Stakes. Nothing else.

It exists to drive the DramaticFrame — to show the dialect-agnostic
generator render a story from a MINIMAL structural vocabulary (whose
story it is, what it argues, what's at stake) rather than a maximalist
storyform or a 15-beat sheet.

The M8 self-verifier emits THREE advisory `noted` observations on this
encoding (no resolving Scene for the Argument; no Stakes on the Obstacle
and Relationship throughlines). That is correct and expected for the
minimal form — this encoding deliberately authors no Scenes and stakes
only the Hero. The verifier is a partner, not a gate; padding those
gaps away would contradict the point of a minimal template.
"""

from __future__ import annotations

from story_engine.core.dramatic import (
    Story, Argument, Throughline, Character, Stakes, StakesOwner,
    ArgumentContribution, ResolutionDirection, ArgumentSide, StakesOwnerKind,
    THROUGHLINE_OWNER_RELATIONSHIP,
)


# --- Characters: the three actors (function labels from `three-actor`) ----

CHARACTERS = (
    Character(id="rocky", name="Rocky Balboa", function_labels=("Hero",)),
    Character(id="apollo", name="Apollo Creed", function_labels=("Obstacle",)),
    Character(id="mickey", name="Mickey Goldmill", function_labels=("Helper",)),
    Character(id="adrian", name="Adrian Pennino", function_labels=("Helper",)),
)


# --- The thematic Argument (the claim the story interrogates) --------------

ARG_WORTH = Argument(
    id="arg_worth",
    premise=("A person earns their worth by ENDURING what would break them — "
             "by staying on their feet — not by winning."),
    counter_premise=("Worth is measured by victory: winners matter, and a man "
                     "who loses is just another bum from the neighborhood."),
    resolution_direction=ResolutionDirection.AFFIRM,
    domain="self-respect",
)


# --- Stakes ----------------------------------------------------------------

STK_SELF_RESPECT = Stakes(
    id="stk_self_respect",
    owner=StakesOwner(kind=StakesOwnerKind.STORY, id="story_rocky_3a"),
    at_risk=("Rocky's belief that he is not just another nobody — that his "
             "life has not already been decided by the neighborhood that "
             "wrote him off."),
    to_gain=("proof, to himself above all, that he can go the full fifteen "
             "rounds with the best in the world and still be standing."),
    external_manifestation="still on his feet at the final bell.",
)


# --- Throughlines: the structural roles within the Argument ----------------

TL_HERO = Throughline(
    id="tl_hero",
    role_label="Hero",
    owners=("rocky",),
    subject=("Rocky's private quest — not to win, but to go the distance and "
             "prove he is not a bum."),
    argument_contributions=(
        ArgumentContribution(argument_id="arg_worth", side=ArgumentSide.AFFIRMS),
    ),
    stakes_id="stk_self_respect",
)

TL_OBSTACLE = Throughline(
    id="tl_obstacle",
    role_label="Obstacle",
    owners=("apollo",),
    subject=("Apollo Creed and the spectacle around him — the bicentennial "
             "publicity machine that has cast Rocky as the body that falls "
             "down on schedule."),
    argument_contributions=(
        ArgumentContribution(argument_id="arg_worth", side=ArgumentSide.OPPOSES),
    ),
)

TL_RELATIONSHIP = Throughline(
    id="tl_relationship",
    role_label="the relationship",
    owners=(THROUGHLINE_OWNER_RELATIONSHIP,),
    subject=("Rocky and Adrian — two people the world overlooked, learning to "
             "be seen by each other; the love that gives the enduring its "
             "reason."),
    argument_contributions=(
        ArgumentContribution(argument_id="arg_worth",
                             side=ArgumentSide.COMPLICATES),
    ),
)

THROUGHLINES = (TL_HERO, TL_OBSTACLE, TL_RELATIONSHIP)


# --- The Story (root record, declaring the minimal template) ---------------

STORY = Story(
    id="story_rocky_3a",
    title="Rocky",
    character_function_template_id="three-actor",
    argument_ids=("arg_worth",),
    throughline_ids=("tl_hero", "tl_obstacle", "tl_relationship"),
    character_ids=("rocky", "apollo", "mickey", "adrian"),
    stakes_ids=("stk_self_respect",),
)
