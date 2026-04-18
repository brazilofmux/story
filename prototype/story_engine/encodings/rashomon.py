"""
Rashomon — the encoded fabula, sjuzhet, and descriptions across four
contested branches.

Story content only. No substrate logic. This file encodes the grove scene
and its four testimonies (Tajomaru, the wife, the husband via the medium,
and the woodcutter), following Akutagawa's *In a Grove* as filmed by
Kurosawa. Purpose: to exercise the substrate's `:contested` branch
machinery — which the *Oedipus Rex* slice does not — and the
description surface specified by descriptions-sketch-01.

This is the second iteration of the encoding. The first (superseded by
git) tried to schematize the *character* of the testimonies —
`duel_character(A, B, "noble")`, `coerced` vs `yielded_willingly` as
sibling predicates, `begged_to_kill` as a structured utterance content.
Those predicates all failed architecture-sketch-01's A3 test (an
attentive LLM or author would catch drift in that content from prose
as reliably as any schema could). Substrate-sketch-05 routed them to
the description surface per the M1 adverbial/modal rule. This
encoding applies the routing.

Fidelity choices:

- **What is on :canonical.** Only the facts that no testimony disputes.
  The party enters the forest; Tajomaru sees them; he lures the husband
  off-road with a story about a buried sword; he ties the husband to a
  tree; he brings the wife to the grove; intercourse occurs (the bare
  fact of it — every account agrees this much); at the end of the
  scene, the husband is dead; a woodcutter discovers the body. Nothing
  about the modality of the intercourse, the manner of the killing,
  who held the weapon, or what the wife said or did after, is
  canonical.

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

- **Facts and descriptions split per A3 / M1.** Structural facts
  (locations, bindings, intercourse-happened, killer-of-husband,
  weapon, body discovery, theft) are event effects on the branch
  where they hold. Interpretive content (the modality of the
  intercourse, the character of the duel, the content of utterances
  beyond "an utterance occurred") is a description attached to the
  relevant anchor event, branch-scoped where branch-specific.

- **The woodcutter's account has no privileged status in the substrate.**
  In the film, the woodcutter's testimony is offered last and is widely
  read as closer to the truth, but this is a property of the film's
  framing and of the woodcutter's self-incrimination, not a substrate-
  level distinction. The substrate treats all four branches as peers.
  Comparative credibility surfaces as a trust-flag description, not
  as a schema distinction.

- **Simplifications.** The framing characters (the priest, the
  policeman, the commoner at Rashomon gate) are omitted. The trial
  testimonies are not modeled as in-fabula canonical events — the
  reader experiences each account through a per-branch sjuzhet whose
  entries carry `focalizer_id = <testifier>`. This keeps the substrate
  stress test clean: what is being exercised is sibling-contested
  non-inheritance, per-branch reader projection, and per-branch
  description scoping, not the additional machinery of
  utterance-as-testimony.


Event-type vocabulary used in this encoding (per substrate-sketch-05
discipline — types are categorical tags, not dispatch keys):

    travel, observation, deception, action, combat, killing,
    utterance, outcome, discovery, theft


Known soft spots (expected; flagged rather than hidden):

1. **No credibility weighting.** All four contested branches are peers.
   The substrate does not represent "branch X is more reliable than
   branch Y." Distinguishing credibility would need either branch-level
   metadata (trust weight, probability) or a meta-branch asserting
   relative reliability as a canonical claim about the contest. The
   woodcutter trust-flag description names the tension without
   resolving it.

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

3. **The husband's "I saw someone pull the dagger out after I died"
   detail is not represented.** In the film this is a notable feature
   of the husband's testimony (he narrates post-mortem events). The
   substrate has no mechanism for an agent's knowledge state to extend
   past their own death, and inventing one for this single case would
   distort the machinery. Left out.

4. **Coercion-as-event is deferred.** Per substrate-sketch-05's M1
   worked example, coercion would promote from description to event if
   the encoding added trauma-state propositions downstream
   (`traumatized(wife)` grounding later preconditions). The current
   encoding does not model trauma-state, so coercion is descriptive.
   When a later sketch adds trauma-state, the D_intercourse_*
   descriptions on `:b-wife` and `:b-woodcutter` promote to `coercion`
   events with world effects.
"""

from __future__ import annotations

from story_engine.core.substrate import (
    Entity, Prop, Event,
    Branch, BranchKind, CANONICAL, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
    Description, AnchorRef, Attention, anchor_event, anchor_desc,
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
# Proposition constructors — structural only.
# ----------------------------------------------------------------------------
#
# Predicates retired in this iteration per substrate-sketch-05 M1 + A3:
#   coerced, yielded_willingly   — descriptive modality of intercourse
#   duel_character               — reader's tonal read of a fight
#   begged_to_kill               — speech-act content of an utterance
#
# The utterance *events* that carried begged_to_kill as a world effect
# remain — an utterance occurring is structural (it changes the
# listener's knowledge via UTTERANCE_HEARD, even if we do not populate
# that effect here). What is gone is the predicate attempting to pin
# down what the utterance said; that is description territory.

def at_location(who: str, where: str) -> Prop:
    return Prop("at_location", (who, where))

def saw(observer: str, target: str) -> Prop:
    return Prop("saw", (observer, target))

def bound_to(who: str, what: str) -> Prop:
    return Prop("bound_to", (who, what))

def had_intercourse_with(a: str, b: str) -> Prop:
    return Prop("had_intercourse_with", (a, b))

def killed(killer: str, victim: str) -> Prop:
    return Prop("killed", (killer, victim))

def killed_with(killer: str, victim: str, weapon: str) -> Prop:
    return Prop("killed_with", (killer, victim, weapon))

def dead(who: str) -> Prop:
    return Prop("dead", (who,))

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
#
# The intercourse event is on :canonical too — every account agrees it
# happened. The per-branch descriptions below carry the branch-specific
# reading of what kind of act it was.

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

    # The intercourse event on canonical. Every account agrees it
    # happened; every account disagrees about its modality. The
    # modality lives in per-branch descriptions attached to this
    # event, not in sibling predicates.
    Event(
        id="E_intercourse",
        type="intercourse",
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
#
# Structural on this branch: Tajomaru unbinds the husband, they fight,
# Tajomaru kills him with the sword. Interpretive (the "noble" quality
# of the duel, the wife's "yielding," her "begging" for the killing):
# descriptions below, not events.

TAJOMARU_FABULA = [

    Event(
        id="E_t_wife_requests_killing",
        type="utterance",
        τ_s=7, τ_a=21,
        participants={"speaker": "wife", "listener": "tajomaru", "target": "husband"},
        branches=frozenset({B_TAJOMARU.label}),
        effects=(
            # Structural: an utterance occurred from wife to tajomaru about
            # the husband. Content — "kill him so only one man alive will
            # know my shame" — is a description.
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
            # The killer observes their own act. Required for
            # focalization-sketch-01 F1: without this, the sjuzhet
            # entry focalized through Tajomaru demotes its own
            # killing-disclosure to GAP (the focalizer wouldn't
            # literally hold the fact). Also correct on its own —
            # a killer ought to know they killed.
            observe("tajomaru", killed("tajomaru", "husband"), 9),
            observe("tajomaru", killed_with("tajomaru", "husband", "sword"), 9),
        ),
    ),

]


# ----------------------------------------------------------------------------
# :b-wife — the wife's account
# ----------------------------------------------------------------------------
#
# She is violated. Tajomaru leaves. She goes to her husband, seeking
# comfort, and meets a gaze of cold contempt. In anguish she begs him
# to kill her; he only stares. Half-conscious, she strikes him with
# her dagger. (In the film, she "faints holding the dagger" and wakes
# to find it in his chest — the testimony is vague by design. We
# encode the branch as asserting she killed him, since that is the
# claim her testimony makes.)
#
# Structural on this branch: Tajomaru flees; the wife kills the
# husband with the dagger. Interpretive (the violation, the
# contemptuous gaze, her half-conscious state): descriptions.

WIFE_FABULA = [

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
            # The killer observes their own act (see E_t_duel note).
            # The wife's testimony is vague about whether the act
            # was conscious — she "faints holding the dagger" —
            # but the branch asserts the killing, so she holds it
            # as her own knowledge within this branch's reality.
            observe("wife", killed("wife", "husband"), 10),
            observe("wife", killed_with("wife", "husband", "dagger"), 10),
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
#
# Structural on this branch: an utterance from wife to tajomaru;
# tajomaru refuses to act (a null event, structurally — kept as a
# narrative beat the sjuzhet references); the wife flees; the husband
# is unbound; the husband kills himself with the dagger.
# Interpretive (her willingness, the flattery in "even Tajomaru was
# disgusted," the humiliation): descriptions.

HUSBAND_FABULA = [

    Event(
        id="E_h_wife_requests_killing",
        type="utterance",
        τ_s=7, τ_a=61,
        participants={"speaker": "wife", "listener": "tajomaru", "target": "husband"},
        branches=frozenset({B_HUSBAND.label}),
        effects=(
            # Utterance occurred; content is a description.
        ),
    ),

    Event(
        id="E_h_tajomaru_refuses",
        type="action",
        τ_s=8, τ_a=62,
        participants={"agent": "tajomaru"},
        branches=frozenset({B_HUSBAND.label}),
        effects=(
            # Refusal is a non-event structurally — Tajomaru does not
            # do the requested thing. Kept as a sjuzhet beat; the
            # "disgust" framing is a description.
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
            # The husband observes his own act at τ_s=11 — the dying
            # moment captures the knowledge. The testimony is
            # delivered via medium, so "the husband knows he killed
            # himself" is exactly what the :b-husband branch asserts.
            observe("husband", killed("husband", "husband"), 11),
            observe("husband", killed_with("husband", "husband", "dagger"), 11),
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
#
# Structural on this branch: an utterance from wife to the two men;
# a fight in which tajomaru kills the husband with the sword; the
# wife flees; the woodcutter steals the dagger. Interpretive (the
# goading, the cowardliness of the fight, the coercion of the
# intercourse): descriptions.

WOODCUTTER_FABULA = [

    Event(
        id="E_wc_wife_goads",
        type="utterance",
        τ_s=7, τ_a=81,
        participants={"speaker": "wife", "listeners": ["tajomaru", "husband"]},
        branches=frozenset({B_WOODCUTTER.label}),
        effects=(
            # Utterance occurred; the goading content is a description.
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
            # The killer observes their own act.
            observe("tajomaru", killed("tajomaru", "husband"), 9),
            observe("tajomaru", killed_with("tajomaru", "husband", "sword"), 9),
            # The woodcutter observes the fight — he's the witness
            # narrating this branch's reality, and the sjuzhet entry
            # for this event is focalized through him. Without this
            # observation, F1 would demote his testimony's
            # killing-disclosure to GAP.
            observe("woodcutter", killed("tajomaru", "husband"), 9),
            observe("woodcutter", killed_with("tajomaru", "husband", "sword"), 9),
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
# Descriptions — the fold-invisible interpretive surface
# ----------------------------------------------------------------------------
#
# Attached to events; branch-scoped where the interpretation is branch-
# specific. Kinds in use: texture, reader-frame, trust-flag,
# authorial-uncertainty. Attention levels per descriptions-sketch-01
# defaults (texture → interpretive/structural; reader-frame →
# structural; trust-flag → interpretive; authorial-uncertainty →
# structural).
#
# τ_a values are chosen to place each description after its anchor in
# the shared authored-time sequence — this matters for staleness
# computations if an anchor is later edited (not exercised in this
# encoding, but the ordering is legible).

DESCRIPTIONS = [

    # --- Intercourse — four per-branch texture descriptions, one
    # trans-branch reader-frame on canonical.
    #
    # Each branch's texture sits on the canonical E_intercourse event
    # with explicit branches=:b-X. The reader-frame is scoped to
    # :canonical and is visible on every branch via
    # canonical-is-universal.

    Description(
        id="D_intercourse_tajomaru_texture",
        attached_to=anchor_event("E_intercourse"),
        kind="texture",
        attention=Attention.STRUCTURAL,
        text=("she yielded; what began as coercion became consent. "
              "Her resistance was a show, and it passed."),
        branches=frozenset({B_TAJOMARU.label}),
        authored_by="tajomaru-testimony",
        τ_a=100,
    ),

    Description(
        id="D_intercourse_wife_texture",
        attached_to=anchor_event("E_intercourse"),
        kind="texture",
        attention=Attention.STRUCTURAL,
        text=("violation — she fights, loses, goes silent. "
              "There was no yielding; there was only the end of fighting."),
        branches=frozenset({B_WIFE.label}),
        authored_by="wife-testimony",
        τ_a=101,
    ),

    Description(
        id="D_intercourse_husband_texture",
        attached_to=anchor_event("E_intercourse"),
        kind="texture",
        attention=Attention.STRUCTURAL,
        text=("she went to him with her eyes open. Worse — she watched the "
              "husband while it happened, and her gaze was the cut."),
        branches=frozenset({B_HUSBAND.label}),
        authored_by="husband-testimony",
        τ_a=102,
    ),

    Description(
        id="D_intercourse_woodcutter_texture",
        attached_to=anchor_event("E_intercourse"),
        kind="texture",
        attention=Attention.STRUCTURAL,
        text=("coercion, unambiguously, though Tajomaru grew gentler after — "
              "pleading with her as much as taking from her."),
        branches=frozenset({B_WOODCUTTER.label}),
        authored_by="woodcutter-testimony",
        τ_a=103,
    ),

    Description(
        id="D_intercourse_frame",
        attached_to=anchor_event("E_intercourse"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("across all four testimonies the intercourse is the pivot; "
              "what differs is whose agency the testifier centers. Each "
              "account's texture description is the testifier's self-"
              "portrait as much as a claim about the wife."),
        branches=frozenset({CANONICAL_LABEL}),
        authored_by="author",
        τ_a=104,
    ),

    # --- Wife's request / goading — the speech-act content of
    # each branch's utterance event. Each testimony reports a
    # different utterance; the events themselves are structural, the
    # content is description.

    Description(
        id="D_t_wife_requests_killing",
        attached_to=anchor_event("E_t_wife_requests_killing"),
        kind="motivation",
        attention=Attention.INTERPRETIVE,
        text=("she said: one of you must die; I cannot belong to two men. "
              "In Tajomaru's telling she asks it of him — kill the husband "
              "and take me."),
        authored_by="tajomaru-testimony",
        τ_a=121,
    ),

    Description(
        id="D_h_wife_requests_killing",
        attached_to=anchor_event("E_h_wife_requests_killing"),
        kind="motivation",
        attention=Attention.INTERPRETIVE,
        text=("in the husband's telling she asked Tajomaru to kill him so "
              "she could be free to follow the bandit. The husband hears "
              "this and loses faith in everything."),
        authored_by="husband-testimony",
        τ_a=161,
    ),

    Description(
        id="D_wc_wife_goads",
        attached_to=anchor_event("E_wc_wife_goads"),
        kind="motivation",
        attention=Attention.INTERPRETIVE,
        text=("she said: you are both less than men if you will not fight "
              "for me. In the woodcutter's telling she shames both into a "
              "fight neither wanted."),
        authored_by="woodcutter-testimony",
        τ_a=181,
    ),

    # --- Duel / fight character — the "noble" vs "cowardly" framing.
    # Attaches to the two combat events (E_t_duel, E_wc_fight). The
    # fight itself is structural; its character is read from prose.

    Description(
        id="D_t_duel_character",
        attached_to=anchor_event("E_t_duel"),
        kind="texture",
        attention=Attention.INTERPRETIVE,
        text=("twenty-three strokes; Tajomaru fought as to an equal, "
              "respecting the husband's skill. A noble duel, in his telling."),
        authored_by="tajomaru-testimony",
        τ_a=123,
    ),

    Description(
        id="D_wc_fight_character",
        attached_to=anchor_event("E_wc_fight"),
        kind="texture",
        attention=Attention.INTERPRETIVE,
        text=("a cowardly, clumsy skirmish. Both men flinched and missed. "
              "The woodcutter's version denies either man their dignity."),
        authored_by="woodcutter-testimony",
        τ_a=182,
    ),

    # --- Husband's suicide — the humiliated framing is description.

    Description(
        id="D_h_suicide_texture",
        attached_to=anchor_event("E_h_suicide"),
        kind="motivation",
        attention=Attention.INTERPRETIVE,
        text=("humiliated and alone, he chose the only dignity left to him. "
              "Or so his ghost claims."),
        authored_by="husband-testimony",
        τ_a=165,
    ),

    # --- Trust-flag on the woodcutter's confession, plus an
    # authorial-uncertainty description attached to that trust-flag
    # (description-on-description, per D3).

    Description(
        id="D_woodcutter_trust",
        attached_to=anchor_event("E_wc_theft"),
        kind="trust-flag",
        attention=Attention.INTERPRETIVE,
        text=("the woodcutter's self-incrimination (the stolen dagger) "
              "reads as candor, but he is also the last witness and the "
              "only one without an alibi. The film declines to adjudicate; "
              "this encoding does the same."),
        branches=frozenset({B_WOODCUTTER.label}),
        authored_by="author",
        τ_a=184,
    ),

    Description(
        id="D_wc_authorial_doubt",
        attached_to=anchor_desc("D_woodcutter_trust"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("am I representing this right? the film's stance on the "
              "woodcutter's reliability is famously contested. If a later "
              "encoding pass decides the film is closer to endorsing his "
              "account, this description is the place to surface that."),
        is_question=True,
        authored_by="author",
        τ_a=185,
    ),

]


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
# All disclosures are slot=KNOWN. The reader hears each testimony as if
# it were the reality of that branch. Cross-testimony meta-uncertainty
# is soft spot #2 above.
#
# Disclosures of the now-retired interpretive predicates are gone. The
# sjuzhet entries that narrated the dropped modality events (E_t_yields,
# E_w_coerced, E_h_willing, E_wc_coerced) are gone with them. Utterance
# events whose content was a begged_to_kill world effect keep their
# sjuzhet entries (the utterance happened, the narration points at it)
# but no longer disclose a speech-act proposition — the speech's content
# is a description the reader reads alongside.


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
    SjuzhetEntry(event_id="E_intercourse",        τ_d=5, focalizer_id=None),
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
        event_id="E_t_wife_requests_killing",
        τ_d=11, focalizer_id="tajomaru",
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
        ),
    ),
)

# :b-wife sjuzhet — testimony at τ_d 20..29.
WIFE_ENTRIES = (
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
        event_id="E_h_wife_requests_killing",
        τ_d=31, focalizer_id="husband",
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
        event_id="E_wc_wife_goads",
        τ_d=41, focalizer_id="woodcutter",
    ),
    SjuzhetEntry(
        event_id="E_wc_fight",
        τ_d=42, focalizer_id="woodcutter",
        disclosures=(
            _disc(killed("tajomaru", "husband")),
            _disc(killed_with("tajomaru", "husband", "sword")),
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
