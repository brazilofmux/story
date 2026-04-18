"""
turn_of_the_screw.py — adversarial encoding probe of Henry James's
*The Turn of the Screw* (1898).

**This is an infeasibility probe, not a production encoding.** The
file is deliberately compact — enough to exercise the substrate's
load-bearing assumptions against a text designed to refuse them —
and is accompanied by findings in `design/turn-of-the-screw-
infeasibility-probe-sketch-01.md`. Read that sketch before using
this file as a model.

The test: can the substrate hold a novella whose *central effect*
is sustained ontological undecidability about whether the ghosts
are real? The substrate commits facts to either `world` (it's
true) or to an agent's `BELIEVED` set (someone holds it). The
novella's text refuses both commitments and leaves the question
open. We try three encoding approaches and document what each
loses.

The three approaches, tried in this file:

1. **Agent-belief-only.** Don't author ghost-existence as a world
   fact; encode only the governess's observations as her BELIEVED.
   The substrate carries her perspective; the world layer is silent
   on ghosts. Most faithful to James's surface; but loses the
   Mrs. Grose side of the question entirely (she cannot have a
   BELIEVED about a fact the substrate doesn't represent at all).

2. **Two-branch canonical.** Two sibling branches,
   `:b-supernatural` and `:b-psychological`. Ghost-existence is a
   world-fact on one branch, absent on the other. Mechanical fit
   is good. But the novella's effect is NOT two readings side-
   by-side (that's Rashomon's shape); it is the irreducible
   ambiguity between them. Two branches give us two encodings,
   not the one-encoding-that-holds-the-ambiguity.

3. **Canonical-with-observation.** Just don't commit either way
   in world facts; author only `observed` events. The substrate
   admits this (world-facts are not exhaustive), but loses the
   ability to say "the governess is right" or "the governess is
   wrong" anywhere. Every observation's meaning is left to
   descriptions.

This file encodes approach 1 (agent-belief-only) as the primary
attempt, with commentary on where approaches 2 and 3 would differ.
The comment density is higher than in production encodings — the
file is documentation as much as code.
"""

from __future__ import annotations

from story_engine.core.substrate import (
    Entity, Prop, Event, EventStatus,
    Branch, BranchKind, CANONICAL, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
    Rule,
)


# ----------------------------------------------------------------------------
# Entities
# ----------------------------------------------------------------------------

governess         = Entity(id="governess",       name="the Governess (unnamed)",  kind="agent")
mrs_grose         = Entity(id="mrs_grose",       name="Mrs. Grose",               kind="agent")
miles             = Entity(id="miles",           name="Miles",                    kind="agent")
flora             = Entity(id="flora",           name="Flora",                    kind="agent")
the_master        = Entity(id="the_master",      name="the Master (the uncle)",   kind="agent")

# The two "ghosts". Authored as agents so observe() helpers still
# work, following macbeth.py's Witches pattern. Whether they are
# metaphysical agents or projections of the governess's imagination
# is exactly the question the novella refuses to answer; in this
# encoding they are substrate entities the governess observes,
# without a commitment to their world-fact ontology.
peter_quint       = Entity(id="peter_quint",     name="Peter Quint (deceased)",   kind="agent")
miss_jessel       = Entity(id="miss_jessel",     name="Miss Jessel (deceased)",   kind="agent")

bly               = Entity(id="bly",             name="Bly (the country house)",  kind="location")
the_tower         = Entity(id="the_tower",       name="the tower",                kind="location")
the_window        = Entity(id="the_window",      name="the window",               kind="location")
the_lake          = Entity(id="the_lake",        name="the lake",                 kind="location")
the_staircase     = Entity(id="the_staircase",   name="the staircase",            kind="location")

ENTITIES = [
    governess, mrs_grose, miles, flora, the_master,
    peter_quint, miss_jessel,
    bly, the_tower, the_window, the_lake, the_staircase,
]

AGENT_IDS = [e.id for e in ENTITIES if e.kind == "agent"]


# ----------------------------------------------------------------------------
# Branches — canonical only (approach 1).
# ----------------------------------------------------------------------------
#
# For approach 2 (two-branch supernatural/psychological), we would
# introduce:
#
#   SUPERNATURAL = Branch(label=":b-supernatural", kind=BranchKind.CONTESTED, parent=CANONICAL)
#   PSYCHOLOGICAL = Branch(label=":b-psychological", kind=BranchKind.CONTESTED, parent=CANONICAL)
#
# plus world-fact events `apparitions_exist` and `apparitions_do_not_
# exist` on each branch respectively. The substrate mechanics allow
# this; the loss (documented in the sketch) is that the two-branch
# encoding produces two readings, not the one-encoding-that-holds-
# the-ambiguity the novella IS.

ALL_BRANCHES = {
    CANONICAL_LABEL: CANONICAL,
}


# ----------------------------------------------------------------------------
# Predicates
# ----------------------------------------------------------------------------

def dead(who: str) -> Prop:
    return Prop("dead", (who,))

def alive(who: str) -> Prop:
    return Prop("alive", (who,))

def at_location(who: str, where: str) -> Prop:
    return Prop("at_location", (who, where))

def governess_of(g: str, ward: str) -> Prop:
    return Prop("governess_of", (g, ward))

def housekeeper_of(h: str, household: str) -> Prop:
    return Prop("housekeeper_of", (h, household))

def child_of(child: str, adult: str) -> Prop:
    return Prop("child_of", (child, adult))

def employed_by(employee: str, employer: str) -> Prop:
    return Prop("employed_by", (employee, employer))

def former_servant(who: str, household: str) -> Prop:
    return Prop("former_servant", (who, household))

# The load-bearing predicate: what does the governess see? The substrate
# records the observation without committing to the observed thing's
# world-existence.
def apparition_of(entity: str, at: str) -> Prop:
    # Same pattern as macbeth.apparition_of — observation-level fact.
    # An observe() effect puts this in the governess's KNOWN set; no
    # corresponding world() effect says the apparition objectively
    # occurred. The substrate is silent at world-level.
    return Prop("apparition_of", (entity, at))

def expelled_from_school(who: str) -> Prop:
    return Prop("expelled_from_school", (who,))

def sent_away(who: str, from_: str) -> Prop:
    return Prop("sent_away", (who, from_))


# ----------------------------------------------------------------------------
# Event helpers (same as in oedipus.py / macbeth.py)
# ----------------------------------------------------------------------------

def observe(agent_id: str, p: Prop, τ: int,
            confidence: Confidence = Confidence.CERTAIN,
            slot: Slot = Slot.KNOWN, note: str = "",
            via: str = None) -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(
            prop=p, slot=slot, confidence=confidence,
            via=via or Diegetic.OBSERVATION.value,
            provenance=(f"observed @ τ_s={τ}{(': ' + note) if note else ''}",),
        ),
    )

def told_by(listener_id: str, speaker_id: str, p: Prop, τ: int,
            confidence: Confidence = Confidence.BELIEVED,
            slot: Slot = Slot.BELIEVED, note: str = "") -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=listener_id,
        held=Held(
            prop=p, slot=slot, confidence=confidence,
            via=Diegetic.UTTERANCE_HEARD.value,
            provenance=(f"told by {speaker_id} @ τ_s={τ}"
                        f"{(': ' + note) if note else ''}",),
        ),
    )

def world(p: Prop, asserts: bool = True) -> WorldEffect:
    return WorldEffect(prop=p, asserts=asserts)


# ----------------------------------------------------------------------------
# Fabula — compact. Hits the structurally-interesting moments only.
# ----------------------------------------------------------------------------

FABULA = [

    # --- Pre-play standing facts ---

    Event(
        id="E_standing_facts",
        type="standing",
        τ_s=-100, τ_a=1,
        participants={"household_head": "the_master"},
        effects=(
            world(child_of("miles", "the_master")),
            world(child_of("flora", "the_master")),
            world(housekeeper_of("mrs_grose", "bly")),
            world(governess_of("governess", "miles")),
            world(governess_of("governess", "flora")),
            world(employed_by("governess", "the_master")),
            world(employed_by("mrs_grose", "the_master")),
            world(former_servant("peter_quint", "bly")),
            world(former_servant("miss_jessel", "bly")),
            # The two deaths — uncontested at world layer. Both died
            # before the governess arrives. The ambiguity is not about
            # whether they died; it is about whether they appear.
            world(dead("peter_quint")),
            world(dead("miss_jessel")),
        ),
    ),

    # --- The first sighting: Quint on the tower ---
    #
    # THIS is the encoding's central adversarial test. The governess
    # climbs up the battlements at twilight, thinks about the Master
    # (not yet consciously desiring him to appear), and sees a man on
    # the tower who is not the Master and who is not anyone living at
    # Bly. James's prose refuses to name him as a ghost at this point;
    # Mrs. Grose's later identification of the description as "Peter
    # Quint's ghost" is when the word "ghost" enters the text. Before
    # Mrs. Grose names him, he is "a man on the tower."
    #
    # Encoding: we record the observation in the governess's KNOWN.
    # We do NOT record world(apparition_of("peter_quint", ...)). The
    # substrate is silent on whether the apparition objectively
    # occurred. Mrs. Grose's later identification is a separate event
    # where she adds her own BELIEVED.

    Event(
        id="E_first_sighting_tower",
        type="observation",
        τ_s=4, τ_a=10,
        participants={"observer": "governess",
                      "perceived_entity": "peter_quint",
                      "at": "the_tower"},
        effects=(
            # The observation itself. The governess is certain she
            # saw someone; that certainty is in her KNOWN set.
            observe("governess",
                    apparition_of("peter_quint", "the_tower"), 4,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="twilight; a man she does not know; he "
                         "seems to see her and withdraws"),
            # Crucially: no world() effect. The substrate does not
            # commit. This is approach 1's central move.
        ),
    ),

    # --- Mrs. Grose's identification ---
    #
    # The governess describes the man to Mrs. Grose. Mrs. Grose
    # identifies the description as Peter Quint — who is dead. This
    # is where "ghost" enters the text. Mrs. Grose adds
    # apparition_of(peter_quint, ...) to her own BELIEVED via
    # told_by — but BELIEVED, not KNOWN, because she is believing a
    # description, not witnessing.

    Event(
        id="E_grose_identifies",
        type="discussion",
        τ_s=5, τ_a=11,
        participants={"governess": "governess", "grose": "mrs_grose"},
        effects=(
            # The governess tells Mrs. Grose what she saw.
            told_by("mrs_grose", "governess",
                    apparition_of("peter_quint", "the_tower"), 5,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Mrs. Grose hears the governess's account "
                         "and identifies the described man as Peter "
                         "Quint, who is dead"),
            # The text is clear that Mrs. Grose believes the
            # governess — at least in this moment. Her BELIEVED is
            # what the substrate can carry. What the substrate
            # cannot carry: whether her belief is *correct*, because
            # that depends on a world-fact the substrate has not
            # authored.
        ),
    ),

    # --- Second sighting: Quint through the dining-room window ---

    Event(
        id="E_second_sighting_window",
        type="observation",
        τ_s=6, τ_a=12,
        participants={"observer": "governess",
                      "perceived_entity": "peter_quint",
                      "at": "the_window"},
        effects=(
            observe("governess",
                    apparition_of("peter_quint", "the_window"), 6,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Sunday afternoon; face at the dining-room "
                         "window; she runs out to confront and he "
                         "is gone"),
        ),
    ),

    # --- Miss Jessel at the lake ---
    #
    # Flora is playing by the lake. The governess sees a woman on
    # the far side; Flora, she becomes convinced, sees the woman
    # too but pretends not to. This is one of the novella's most
    # contested moments: later critics ask whether Flora was
    # communing or whether the governess projected.

    Event(
        id="E_jessel_at_lake",
        type="observation",
        τ_s=8, τ_a=13,
        participants={"observer": "governess",
                      "perceived_entity": "miss_jessel",
                      "at": "the_lake",
                      "also_present": "flora"},
        effects=(
            observe("governess",
                    apparition_of("miss_jessel", "the_lake"), 8,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="across the lake; Flora does not look up"),
            # The governess's BELIEVED (not KNOWN — she cannot
            # directly observe Flora's mind) that Flora is aware of
            # the apparition. This is already an interpretive
            # elaboration by the governess; the substrate can carry
            # it as her BELIEVED, but not as a world fact.
            observe("governess",
                    Prop("in_communion_with", ("flora", "miss_jessel")), 8,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="governess's interpretation; not directly "
                         "observed"),
        ),
    ),

    # --- Flora sent away ---

    Event(
        id="E_flora_sent_away",
        type="departure",
        τ_s=12, τ_a=14,
        participants={"subject": "flora", "sender": "mrs_grose"},
        effects=(
            world(sent_away("flora", "bly")),
            # Mrs. Grose takes Flora away after a confrontation in
            # which Flora denies seeing anything and becomes
            # hysterical. What this denial *means* is unsettled: did
            # the governess terrify a child with an imaginary threat,
            # or did Flora retreat into denial because the ghost she
            # was communing with had been named to her face?
        ),
    ),

    # --- The final scene: Miles, the letter, the death ---
    #
    # THE novella's terminal event. The governess confronts Miles
    # about his expulsion from school and about what he has been
    # communing with. She insists that Quint is there, at the
    # window; Miles cries out; she clasps him; he dies in her arms.
    #
    # The cause of death is structurally undetermined:
    #   - If the supernatural reading: Miles is seized from his
    #     "possession" by her protective act, and dies from the
    #     severance.
    #   - If the psychological reading: Miles is smothered or
    #     frightened to death by an hysteric who has spent weeks
    #     terrorizing him.
    #
    # The substrate can hold dead(miles); it cannot hold
    # killed(governess, miles) or died_of_fright(miles) or
    # released_from_possession(miles) without committing to one
    # reading. Approach 1: we author only dead(miles) and note the
    # undetermined cause in annotation. That's all the substrate
    # will hold honestly.

    Event(
        id="E_miles_dies",
        type="death",
        τ_s=20, τ_a=20,
        participants={"who": "miles",
                      "also_present": "governess",
                      "at": "bly"},
        effects=(
            world(dead("miles")),
            # NO cause authored. No killed(_, miles). No
            # died_of_fright(miles). The substrate cannot resolve
            # the cause without choosing a reading. Approach 1
            # accepts this silence.
            observe("governess", dead("miles"), 20,
                    note="he dies in her arms; she holds him and "
                         "knows he is gone"),
        ),
    ),
]


# ----------------------------------------------------------------------------
# Preplay disclosures
# ----------------------------------------------------------------------------
#
# Framing-device standing facts the reader knows from the Douglas-
# introduces-the-manuscript opening.

PREPLAY_DISCLOSURES = (
    Disclosure(prop=governess_of("governess", "miles"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=child_of("miles", "the_master"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=former_servant("peter_quint", "bly"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=dead("peter_quint"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
)


# ----------------------------------------------------------------------------
# Sjuzhet
# ----------------------------------------------------------------------------
#
# All entries focalized through the governess — like Ackroyd, but with
# the twist that the novella FRAMES her manuscript as read aloud by
# Douglas, so there's a nesting (Douglas's audience hears the frame-
# narrator hearing Douglas reading the governess's written account).
# We keep focalizer_id="governess" to match the substrate's available
# handle; the frame-narrator nesting is a descriptions-layer concern
# we do not model here.

SJUZHET = [
    SjuzhetEntry(
        event_id="E_standing_facts",
        τ_d=0,
        focalizer_id="governess",
        disclosures=PREPLAY_DISCLOSURES,
    ),
    SjuzhetEntry(
        event_id="E_first_sighting_tower",
        τ_d=1, focalizer_id="governess", disclosures=(),
    ),
    SjuzhetEntry(
        event_id="E_grose_identifies",
        τ_d=2, focalizer_id="governess", disclosures=(),
    ),
    SjuzhetEntry(
        event_id="E_second_sighting_window",
        τ_d=3, focalizer_id="governess", disclosures=(),
    ),
    SjuzhetEntry(
        event_id="E_jessel_at_lake",
        τ_d=4, focalizer_id="governess", disclosures=(),
    ),
    SjuzhetEntry(
        event_id="E_flora_sent_away",
        τ_d=5, focalizer_id="governess", disclosures=(),
    ),
    SjuzhetEntry(
        event_id="E_miles_dies",
        τ_d=6, focalizer_id="governess", disclosures=(),
    ),
]


# ----------------------------------------------------------------------------
# Rules — none.
# ----------------------------------------------------------------------------
#
# The novella's terminal facts (Miles dies) have no compound moral
# derivation that fires without taking a side. No equivalent of
# Macbeth's tyrant-rule is safely authorable. This is itself a finding:
# when the text refuses world-fact commitment, the substrate's Horn-
# clause rule machinery has no antecedents to fire from.

RULES = ()
