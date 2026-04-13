"""
Rashomon — the encoded fabula and sjuzhet across four contested branches.

Story content only. No substrate logic. This file encodes the grove scene
and its four testimonies (Tajomaru, the wife, the husband via the medium,
and the woodcutter), following Akutagawa's *In a Grove* as filmed by
Kurosawa. Purpose: to exercise the substrate's `:contested` branch
machinery, which the *Oedipus Rex* slice does not.

Fidelity choices:

- **What is on :canonical.** Only the facts that no testimony disputes.
  The party enters the forest; Tajomaru sees them; he lures the husband
  off-road with a story about a buried sword; he ties the husband to a
  tree; he brings the wife to the grove; intercourse occurs (the bare
  fact of it — every account agrees this much); at the end of the scene,
  the husband is dead; a woodcutter discovers the body. Nothing about
  the modality of the intercourse, the manner of the killing, who held
  the weapon, or what the wife said or did after, is canonical.

- **What is contested.** The four mutually incompatible accounts live
  on four sibling `:contested` branches:
    `:b-tajomaru`  — Tajomaru's brag: a noble duel; the wife yielded.
    `:b-wife`      — the wife's testimony: she was violated; she killed
                     her husband in a half-conscious act after his gaze
                     of contempt.
    `:b-husband`   — the husband's testimony through the medium: the
                     wife went willingly with Tajomaru, begged him to
                     kill her husband; Tajomaru refused; the husband
                     took his own life with the wife's dagger.
    `:b-woodcutter`— the woodcutter's later confession: Tajomaru killed
                     the husband in a messy, cowardly fight after the
                     wife goaded both men; the woodcutter himself stole
                     the dagger from the scene.

- **The woodcutter's account has no privileged status in the substrate.**
  In the film, the woodcutter's testimony is offered last and is widely
  read as closer to the truth, but this is a property of the film's
  framing and of the woodcutter's self-incrimination, not a substrate-
  level distinction. The substrate treats all four branches as peers.
  Representing comparative credibility is a known soft spot; see the
  *Known soft spots* section at the bottom of this file.

- **Simplifications.** The framing characters (the priest, the
  policeman, the commoner at Rashomon gate) are omitted. The trial
  testimonies are not modeled as in-fabula canonical events — the
  reader experiences each account through a per-branch sjuzhet whose
  entries carry `focalizer_id = <testifier>`. This keeps the substrate
  stress test clean: what is being exercised is sibling-contested
  non-inheritance and per-branch reader projection, not the additional
  machinery of utterance-as-testimony.

- **Language.** The encoding treats sexual coercion and death
  clinically. The predicates used are `coerced`, `yielded_willingly`,
  `killed`, etc. The substrate is a substrate; the story is not told
  here.


Known soft spots (expected; flagged rather than hidden):

1. **No credibility weighting.** All four contested branches are peers.
   The substrate does not represent "branch X is more reliable than
   branch Y." Distinguishing credibility would need either branch-level
   metadata (trust weight, probability) or a meta-branch asserting
   relative reliability as a canonical claim about the contest.

2. **No "the reader heard a testimony" layer.** The reader's disclosures
   on each branch use slot=KNOWN as a first-order move, meaning "within
   the reality of this branch, the reader knows X." What the encoding
   does *not* capture is the reader's meta-knowledge that they have in
   fact heard four conflicting accounts and are uncertain which, if any,
   is true. That meta-uncertainty lives above the substrate's current
   per-branch regime. Proper treatment likely requires testimony-as-
   utterance events that lodge propositions of the form "X testified Y"
   on canonical rather than "Y" on a contested branch, with the reader
   then holding a separate branch-indexed belief about Y. This is an
   open-question item for a future sketch.

3. **No intercourse-as-event distinct from its modality.** We model the
   bare fact on canonical and the modality (`coerced` vs
   `yielded_willingly`) on branches. This is a pragmatic split but it
   leaves "modality of an event" as a stand-alone proposition rather
   than an adverbial modifier of the event itself. Event-modifier
   structure is part of open question 1 (event vocabulary).

4. **The husband's "I saw someone pull the dagger out after I died"
   detail is not represented.** In the film this is a notable feature
   of the husband's testimony (he narrates post-mortem events). The
   substrate has no mechanism for an agent's knowledge state to extend
   past their own death, and inventing one for this single case would
   distort the machinery. Left out.
"""

from __future__ import annotations

from substrate import (
    Entity, Prop, Event,
    Branch, BranchKind, CANONICAL, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
)


# ----------------------------------------------------------------------------
# Entities
# ----------------------------------------------------------------------------

tajomaru  = Entity(id="tajomaru",  name="Tajomaru",       kind="agent")
wife      = Entity(id="wife",      name="the Wife",       kind="agent")
husband   = Entity(id="husband",   name="the Husband",    kind="agent")
woodcutter = Entity(id="woodcutter", name="the Woodcutter", kind="agent")

forest_road = Entity(id="forest_road", name="the forest road", kind="location")
grove       = Entity(id="grove",       name="the grove",       kind="location")
tree        = Entity(id="tree",        name="the tree",        kind="object")
sword       = Entity(id="sword",       name="the sword",       kind="object")
dagger      = Entity(id="dagger",      name="the dagger",      kind="object")

ENTITIES = [
    tajomaru, wife, husband, woodcutter,
    forest_road, grove, tree, sword, dagger,
]

AGENT_IDS = [e.id for e in ENTITIES if e.kind == "agent"]


# ----------------------------------------------------------------------------
# Proposition constructors
# ----------------------------------------------------------------------------

def at_location(who: str, where: str) -> Prop:
    return Prop("at_location", (who, where))

def saw(observer: str, target: str) -> Prop:
    return Prop("saw", (observer, target))

def bound_to(who: str, what: str) -> Prop:
    return Prop("bound_to", (who, what))

def had_intercourse_with(a: str, b: str) -> Prop:
    return Prop("had_intercourse_with", (a, b))

def coerced(agent: str, patient: str) -> Prop:
    return Prop("coerced", (agent, patient))

def yielded_willingly(who: str, toward: str) -> Prop:
    return Prop("yielded_willingly", (who, toward))

def killed(killer: str, victim: str) -> Prop:
    return Prop("killed", (killer, victim))

def killed_with(killer: str, victim: str, weapon: str) -> Prop:
    return Prop("killed_with", (killer, victim, weapon))

def dead(who: str) -> Prop:
    return Prop("dead", (who,))

def duel_character(a: str, b: str, quality: str) -> Prop:
    # quality in {"noble", "cowardly"}
    return Prop("duel_character", (a, b, quality))

def begged_to_kill(pleader: str, target: str, victim: str) -> Prop:
    return Prop("begged_to_kill", (pleader, target, victim))

def stole(who: str, what: str) -> Prop:
    return Prop("stole", (who, what))

def fled(who: str) -> Prop:
    return Prop("fled", (who,))

def body_found_by(finder: str, victim: str) -> Prop:
    return Prop("body_found_by", (finder, victim))


# ----------------------------------------------------------------------------
# Branches (four sibling :contested, plus the root :canonical)
# ----------------------------------------------------------------------------

B_TAJOMARU   = Branch(label=":b-tajomaru",   kind=BranchKind.CONTESTED)
B_WIFE       = Branch(label=":b-wife",       kind=BranchKind.CONTESTED)
B_HUSBAND    = Branch(label=":b-husband",    kind=BranchKind.CONTESTED)
B_WOODCUTTER = Branch(label=":b-woodcutter", kind=BranchKind.CONTESTED)

CONTESTED_BRANCHES = [B_TAJOMARU, B_WIFE, B_HUSBAND, B_WOODCUTTER]

ALL_BRANCHES = {
    CANONICAL_LABEL:      CANONICAL,
    B_TAJOMARU.label:     B_TAJOMARU,
    B_WIFE.label:         B_WIFE,
    B_HUSBAND.label:      B_HUSBAND,
    B_WOODCUTTER.label:   B_WOODCUTTER,
}


# ----------------------------------------------------------------------------
# Event helpers (match oedipus.py's convention)
# ----------------------------------------------------------------------------

def observe(agent_id: str, p: Prop, τ: int,
            slot: Slot = Slot.KNOWN,
            confidence: Confidence = Confidence.CERTAIN,
            note: str = "") -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(
            prop=p, slot=slot, confidence=confidence,
            via=Diegetic.OBSERVATION.value,
            provenance=(f"observed @ τ_s={τ}{(': ' + note) if note else ''}",),
        ),
    )

def world(p: Prop, asserts: bool = True) -> WorldEffect:
    return WorldEffect(prop=p, asserts=asserts)


# ----------------------------------------------------------------------------
# Canonical events — pre-scene + the undisputed floor
# ----------------------------------------------------------------------------
#
# These events appear on every branch's fold via the canonical-is-universal
# rule. They are the facts no testimony disputes.

CANONICAL_FABULA = [

    Event(
        id="E_travel",
        type="travel",
        τ_s=0, τ_a=1,
        participants={"husband": "husband", "wife": "wife"},
        effects=(
            world(at_location("husband", "forest_road")),
            world(at_location("wife",    "forest_road")),
            observe("husband", at_location("husband", "forest_road"), 0),
            observe("wife",    at_location("wife",    "forest_road"), 0),
        ),
    ),

    Event(
        id="E_tajomaru_sees_them",
        type="observation",
        τ_s=1, τ_a=2,
        participants={"observer": "tajomaru", "targets": ["husband", "wife"]},
        effects=(
            observe("tajomaru", at_location("husband", "forest_road"), 1),
            observe("tajomaru", at_location("wife",    "forest_road"), 1),
            observe("tajomaru", saw("tajomaru", "wife"), 1,
                    note="catches sight of her through the trees"),
        ),
    ),

    Event(
        id="E_lure",
        type="deception",
        τ_s=2, τ_a=3,
        participants={"deceiver": "tajomaru", "target": "husband"},
        effects=(
            # Tajomaru tells the husband of a buried sword in the grove.
            # The husband, persuaded, leaves the road.
            world(at_location("husband", "grove")),
            observe("tajomaru", at_location("husband", "grove"), 2),
            observe("husband",  at_location("husband", "grove"), 2,
                    note="lured off the road by story of buried sword"),
        ),
    ),

    Event(
        id="E_bind",
        type="action",
        τ_s=3, τ_a=4,
        participants={"binder": "tajomaru", "bound": "husband"},
        effects=(
            world(bound_to("husband", "tree")),
            observe("tajomaru", bound_to("husband", "tree"), 3),
            observe("husband",  bound_to("husband", "tree"), 3),
        ),
    ),

    Event(
        id="E_bring_wife",
        type="action",
        τ_s=4, τ_a=5,
        participants={"bringer": "tajomaru", "brought": "wife"},
        effects=(
            world(at_location("wife", "grove")),
            observe("tajomaru", at_location("wife", "grove"), 4),
            observe("wife",     at_location("wife", "grove"), 4),
            observe("husband",  at_location("wife", "grove"), 4,
                    note="bound to tree, sees wife arrive"),
        ),
    ),

    # The bare fact of intercourse. Every account agrees that this
    # happened; every account disagrees about its modality. Modality
    # lives on the per-branch events below.
    Event(
        id="E_intercourse_bare",
        type="action",
        τ_s=5, τ_a=6,
        participants={"a": "tajomaru", "b": "wife"},
        effects=(
            world(had_intercourse_with("tajomaru", "wife")),
            observe("tajomaru", had_intercourse_with("tajomaru", "wife"), 5),
            observe("wife",     had_intercourse_with("tajomaru", "wife"), 5),
            observe("husband",  had_intercourse_with("tajomaru", "wife"), 5,
                    note="forced to watch from the tree"),
        ),
    ),

    # The husband ends up dead. All accounts agree on the outcome; they
    # differ on the cause. The `killed(*, husband)` propositions are NOT
    # asserted canonically — they are branch-specific.
    Event(
        id="E_husband_dead",
        type="outcome",
        τ_s=20, τ_a=7,
        participants={"victim": "husband"},
        effects=(
            world(dead("husband")),
        ),
    ),

    # The woodcutter finds the body. This is the frame event that opens
    # the film and triggers the trial. Canonical: the body was found,
    # and the woodcutter found it.
    Event(
        id="E_body_found",
        type="discovery",
        τ_s=30, τ_a=8,
        participants={"finder": "woodcutter", "victim": "husband"},
        effects=(
            world(body_found_by("woodcutter", "husband")),
            observe("woodcutter", dead("husband"), 30),
            observe("woodcutter", body_found_by("woodcutter", "husband"), 30),
        ),
    ),

]


# ----------------------------------------------------------------------------
# :b-tajomaru — Tajomaru's account
# ----------------------------------------------------------------------------
#
# A boast. After the intercourse (which he frames as eventual consent),
# the wife, overcome, asks Tajomaru to kill her husband so only one man
# alive will know her shame. Tajomaru, respecting the husband as a
# worthy opponent, unties him and fights him in a long, skilled duel —
# twenty-three strokes — and kills him with the sword.

TAJOMARU_FABULA = [

    Event(
        id="E_t_yields",
        type="internal",
        τ_s=6, τ_a=20,
        participants={"who": "wife", "toward": "tajomaru"},
        branches=frozenset({B_TAJOMARU.label}),
        effects=(
            world(yielded_willingly("wife", "tajomaru")),
        ),
    ),

    Event(
        id="E_t_wife_begs",
        type="utterance",
        τ_s=7, τ_a=21,
        participants={"speaker": "wife", "listener": "tajomaru", "target": "husband"},
        branches=frozenset({B_TAJOMARU.label}),
        effects=(
            world(begged_to_kill("wife", "tajomaru", "husband")),
        ),
    ),

    Event(
        id="E_t_frees_husband",
        type="action",
        τ_s=8, τ_a=22,
        participants={"agent": "tajomaru", "patient": "husband"},
        branches=frozenset({B_TAJOMARU.label}),
        effects=(
            world(bound_to("husband", "tree"), asserts=False),
        ),
    ),

    Event(
        id="E_t_duel",
        type="combat",
        τ_s=9, τ_a=23,
        participants={"a": "tajomaru", "b": "husband"},
        branches=frozenset({B_TAJOMARU.label}),
        effects=(
            world(killed("tajomaru", "husband")),
            world(killed_with("tajomaru", "husband", "sword")),
            world(duel_character("tajomaru", "husband", "noble")),
        ),
    ),

]


# ----------------------------------------------------------------------------
# :b-wife — the wife's account
# ----------------------------------------------------------------------------
#
# She is violated (coerced, not willing). Tajomaru leaves. She goes to
# her husband, seeking comfort, and meets a gaze of cold contempt. In
# anguish she begs him to kill her; he only stares. Half-conscious, she
# strikes him with her dagger. (In the film, she "faints holding the
# dagger" and wakes to find it in his chest — the testimony is vague by
# design. We encode the branch as asserting she killed him, since that
# is the claim her testimony makes.)

WIFE_FABULA = [

    Event(
        id="E_w_coerced",
        type="internal",
        τ_s=6, τ_a=40,
        participants={"agent": "tajomaru", "patient": "wife"},
        branches=frozenset({B_WIFE.label}),
        effects=(
            world(coerced("tajomaru", "wife")),
        ),
    ),

    Event(
        id="E_w_tajomaru_leaves",
        type="action",
        τ_s=7, τ_a=41,
        participants={"agent": "tajomaru"},
        branches=frozenset({B_WIFE.label}),
        effects=(
            world(at_location("tajomaru", "forest_road"), asserts=False),
            world(fled("tajomaru")),
        ),
    ),

    Event(
        id="E_w_killing",
        type="killing",
        τ_s=10, τ_a=42,
        participants={"killer": "wife", "victim": "husband"},
        branches=frozenset({B_WIFE.label}),
        effects=(
            world(killed("wife", "husband")),
            world(killed_with("wife", "husband", "dagger")),
        ),
    ),

]


# ----------------------------------------------------------------------------
# :b-husband — the husband's account through the medium
# ----------------------------------------------------------------------------
#
# The wife goes willingly with Tajomaru. So smitten is she that she
# begs him to kill her husband so she can be free to follow him.
# Tajomaru, repulsed, offers the husband a choice — kill this woman
# or let her live — and the wife flees. Tajomaru unties the husband
# and leaves. Alone, humiliated, the husband takes up his wife's
# dagger (left behind in the struggle) and ends his own life.

HUSBAND_FABULA = [

    Event(
        id="E_h_willing",
        type="internal",
        τ_s=6, τ_a=60,
        participants={"who": "wife", "toward": "tajomaru"},
        branches=frozenset({B_HUSBAND.label}),
        effects=(
            world(yielded_willingly("wife", "tajomaru")),
        ),
    ),

    Event(
        id="E_h_wife_begs",
        type="utterance",
        τ_s=7, τ_a=61,
        participants={"speaker": "wife", "listener": "tajomaru", "target": "husband"},
        branches=frozenset({B_HUSBAND.label}),
        effects=(
            world(begged_to_kill("wife", "tajomaru", "husband")),
        ),
    ),

    Event(
        id="E_h_tajomaru_refuses",
        type="action",
        τ_s=8, τ_a=62,
        participants={"agent": "tajomaru"},
        branches=frozenset({B_HUSBAND.label}),
        effects=(
            # Tajomaru refuses to kill the husband; this is the husband's
            # flattering framing, in which even the bandit is disgusted
            # by the wife.
        ),
    ),

    Event(
        id="E_h_wife_flees",
        type="action",
        τ_s=9, τ_a=63,
        participants={"agent": "wife"},
        branches=frozenset({B_HUSBAND.label}),
        effects=(
            world(fled("wife")),
        ),
    ),

    Event(
        id="E_h_frees_husband",
        type="action",
        τ_s=10, τ_a=64,
        participants={"agent": "tajomaru", "patient": "husband"},
        branches=frozenset({B_HUSBAND.label}),
        effects=(
            world(bound_to("husband", "tree"), asserts=False),
        ),
    ),

    Event(
        id="E_h_suicide",
        type="killing",
        τ_s=11, τ_a=65,
        participants={"agent": "husband", "victim": "husband"},
        branches=frozenset({B_HUSBAND.label}),
        effects=(
            world(killed("husband", "husband")),
            world(killed_with("husband", "husband", "dagger")),
        ),
    ),

]


# ----------------------------------------------------------------------------
# :b-woodcutter — the woodcutter's later confession
# ----------------------------------------------------------------------------
#
# The woodcutter claims (after first lying that he only found the body)
# to have witnessed the whole scene. In his version: Tajomaru pleaded
# with the wife to marry him; the wife, enraged at both men's passivity,
# goaded them into a fight; both fought clumsily, not nobly; Tajomaru
# eventually killed the husband in the messy skirmish. The woodcutter's
# own self-incriminating disclosure: after the scene he crept out and
# took the wife's dagger, which is why it was missing from the body.

WOODCUTTER_FABULA = [

    Event(
        id="E_wc_coerced",
        type="internal",
        τ_s=6, τ_a=80,
        participants={"agent": "tajomaru", "patient": "wife"},
        branches=frozenset({B_WOODCUTTER.label}),
        effects=(
            world(coerced("tajomaru", "wife")),
        ),
    ),

    Event(
        id="E_wc_wife_goads",
        type="utterance",
        τ_s=7, τ_a=81,
        participants={"speaker": "wife", "listeners": ["tajomaru", "husband"]},
        branches=frozenset({B_WOODCUTTER.label}),
        effects=(
            # The wife, in the woodcutter's account, is the one who
            # forces the killing by shaming both men into a fight.
            # Represented as her asking for the killing the way
            # Tajomaru's account claims.
            world(begged_to_kill("wife", "tajomaru", "husband")),
        ),
    ),

    Event(
        id="E_wc_fight",
        type="combat",
        τ_s=9, τ_a=82,
        participants={"a": "tajomaru", "b": "husband"},
        branches=frozenset({B_WOODCUTTER.label}),
        effects=(
            world(killed("tajomaru", "husband")),
            world(killed_with("tajomaru", "husband", "sword")),
            world(duel_character("tajomaru", "husband", "cowardly")),
        ),
    ),

    Event(
        id="E_wc_wife_flees",
        type="action",
        τ_s=10, τ_a=83,
        participants={"agent": "wife"},
        branches=frozenset({B_WOODCUTTER.label}),
        effects=(
            world(fled("wife")),
        ),
    ),

    Event(
        id="E_wc_theft",
        type="theft",
        τ_s=11, τ_a=84,
        participants={"thief": "woodcutter", "object": "dagger"},
        branches=frozenset({B_WOODCUTTER.label}),
        effects=(
            # Self-incriminating. The woodcutter's credibility within the
            # film rests partly on volunteering this detail. Substrate
            # does not model that credibility effect.
            world(stole("woodcutter", "dagger")),
            observe("woodcutter", stole("woodcutter", "dagger"), 11),
        ),
    ),

]


# ----------------------------------------------------------------------------
# Combined event list
# ----------------------------------------------------------------------------

EVENTS_ALL = (
    CANONICAL_FABULA
    + TAJOMARU_FABULA
    + WIFE_FABULA
    + HUSBAND_FABULA
    + WOODCUTTER_FABULA
)


# ----------------------------------------------------------------------------
# Sjuzhet — per-branch narration
# ----------------------------------------------------------------------------
#
# The substrate requires the reader-projection to be computed per branch,
# and sjuzhet entries must only reference events in fold-scope for the
# target branch. We therefore build one sjuzhet per contested branch.
# Each consists of:
#
#   1. A shared canonical preamble — the undisputed setup narrated with
#      no focalizer (the film's opening panel, before any testimony is
#      offered). Disclosures give the reader the bare facts everyone
#      agrees on.
#
#   2. Branch-specific narration — the testimony's own account of what
#      happened in the grove, narrated with focalizer_id set to the
#      testifier.
#
#   3. A canonical closing panel — the body is found; the frame story
#      resumes; the testimonies have concluded.
#
# All disclosures are slot=KNOWN. See *Known soft spots* #2 above on
# why this is a first-order encoding.


def _disc(prop: Prop, via: str = Narrative.DISCLOSURE.value) -> Disclosure:
    return Disclosure(
        prop=prop,
        slot=Slot.KNOWN,
        confidence=Confidence.CERTAIN,
        via=via,
    )


PREAMBLE_DISCLOSURES = (
    _disc(at_location("husband", "forest_road")),
    _disc(at_location("wife",    "forest_road")),
    _disc(saw("tajomaru", "wife")),
    _disc(at_location("husband", "grove")),
    _disc(bound_to("husband", "tree")),
    _disc(at_location("wife", "grove")),
    _disc(had_intercourse_with("tajomaru", "wife")),
)

PREAMBLE_ENTRIES = (
    # τ_d=0 — setup, omniscient narration.
    SjuzhetEntry(
        event_id="E_travel",
        τ_d=0, focalizer_id=None,
        disclosures=PREAMBLE_DISCLOSURES,
    ),
    SjuzhetEntry(event_id="E_tajomaru_sees_them", τ_d=1, focalizer_id=None),
    SjuzhetEntry(event_id="E_lure",               τ_d=2, focalizer_id=None),
    SjuzhetEntry(event_id="E_bind",               τ_d=3, focalizer_id=None),
    SjuzhetEntry(event_id="E_bring_wife",         τ_d=4, focalizer_id=None),
    SjuzhetEntry(event_id="E_intercourse_bare",   τ_d=5, focalizer_id=None),
)

# Closing panel — body discovery, narrated omnisciently.
CLOSING_ENTRIES = (
    SjuzhetEntry(
        event_id="E_husband_dead",
        τ_d=90, focalizer_id=None,
        disclosures=(_disc(dead("husband")),),
    ),
    SjuzhetEntry(
        event_id="E_body_found",
        τ_d=91, focalizer_id=None,
        disclosures=(_disc(body_found_by("woodcutter", "husband")),),
    ),
)


# :b-tajomaru sjuzhet — testimony at τ_d 10..19.
TAJOMARU_ENTRIES = (
    SjuzhetEntry(
        event_id="E_t_yields",
        τ_d=10, focalizer_id="tajomaru",
        disclosures=(_disc(yielded_willingly("wife", "tajomaru")),),
    ),
    SjuzhetEntry(
        event_id="E_t_wife_begs",
        τ_d=11, focalizer_id="tajomaru",
        disclosures=(_disc(begged_to_kill("wife", "tajomaru", "husband")),),
    ),
    SjuzhetEntry(
        event_id="E_t_frees_husband",
        τ_d=12, focalizer_id="tajomaru",
    ),
    SjuzhetEntry(
        event_id="E_t_duel",
        τ_d=13, focalizer_id="tajomaru",
        disclosures=(
            _disc(killed("tajomaru", "husband")),
            _disc(killed_with("tajomaru", "husband", "sword")),
            _disc(duel_character("tajomaru", "husband", "noble")),
        ),
    ),
)

# :b-wife sjuzhet — testimony at τ_d 20..29.
WIFE_ENTRIES = (
    SjuzhetEntry(
        event_id="E_w_coerced",
        τ_d=20, focalizer_id="wife",
        disclosures=(_disc(coerced("tajomaru", "wife")),),
    ),
    SjuzhetEntry(
        event_id="E_w_tajomaru_leaves",
        τ_d=21, focalizer_id="wife",
        disclosures=(_disc(fled("tajomaru")),),
    ),
    SjuzhetEntry(
        event_id="E_w_killing",
        τ_d=22, focalizer_id="wife",
        disclosures=(
            _disc(killed("wife", "husband")),
            _disc(killed_with("wife", "husband", "dagger")),
        ),
    ),
)

# :b-husband sjuzhet — testimony via medium at τ_d 30..39.
HUSBAND_ENTRIES = (
    SjuzhetEntry(
        event_id="E_h_willing",
        τ_d=30, focalizer_id="husband",
        disclosures=(_disc(yielded_willingly("wife", "tajomaru")),),
    ),
    SjuzhetEntry(
        event_id="E_h_wife_begs",
        τ_d=31, focalizer_id="husband",
        disclosures=(_disc(begged_to_kill("wife", "tajomaru", "husband")),),
    ),
    SjuzhetEntry(
        event_id="E_h_tajomaru_refuses",
        τ_d=32, focalizer_id="husband",
    ),
    SjuzhetEntry(
        event_id="E_h_wife_flees",
        τ_d=33, focalizer_id="husband",
        disclosures=(_disc(fled("wife")),),
    ),
    SjuzhetEntry(
        event_id="E_h_frees_husband",
        τ_d=34, focalizer_id="husband",
    ),
    SjuzhetEntry(
        event_id="E_h_suicide",
        τ_d=35, focalizer_id="husband",
        disclosures=(
            _disc(killed("husband", "husband")),
            _disc(killed_with("husband", "husband", "dagger")),
        ),
    ),
)

# :b-woodcutter sjuzhet — later confession at τ_d 40..49.
WOODCUTTER_ENTRIES = (
    SjuzhetEntry(
        event_id="E_wc_coerced",
        τ_d=40, focalizer_id="woodcutter",
        disclosures=(_disc(coerced("tajomaru", "wife")),),
    ),
    SjuzhetEntry(
        event_id="E_wc_wife_goads",
        τ_d=41, focalizer_id="woodcutter",
        disclosures=(_disc(begged_to_kill("wife", "tajomaru", "husband")),),
    ),
    SjuzhetEntry(
        event_id="E_wc_fight",
        τ_d=42, focalizer_id="woodcutter",
        disclosures=(
            _disc(killed("tajomaru", "husband")),
            _disc(killed_with("tajomaru", "husband", "sword")),
            _disc(duel_character("tajomaru", "husband", "cowardly")),
        ),
    ),
    SjuzhetEntry(
        event_id="E_wc_wife_flees",
        τ_d=43, focalizer_id="woodcutter",
        disclosures=(_disc(fled("wife")),),
    ),
    SjuzhetEntry(
        event_id="E_wc_theft",
        τ_d=44, focalizer_id="woodcutter",
        disclosures=(_disc(stole("woodcutter", "dagger")),),
    ),
)


SJUZHET_BY_BRANCH = {
    B_TAJOMARU.label:   list(PREAMBLE_ENTRIES) + list(TAJOMARU_ENTRIES)   + list(CLOSING_ENTRIES),
    B_WIFE.label:       list(PREAMBLE_ENTRIES) + list(WIFE_ENTRIES)       + list(CLOSING_ENTRIES),
    B_HUSBAND.label:    list(PREAMBLE_ENTRIES) + list(HUSBAND_ENTRIES)    + list(CLOSING_ENTRIES),
    B_WOODCUTTER.label: list(PREAMBLE_ENTRIES) + list(WOODCUTTER_ENTRIES) + list(CLOSING_ENTRIES),
}
