"""
sworn.py — "Sworn", an ORIGINAL tragedy told in REVERSE.

The hard-telling experiment (state-of-play: the backward tragedy). The
fable is original and its STRUCTURE is sound Aristotelian — so it
verifies clean and the experiment isolates a single variable: the
SJUZHET runs in strict reverse chronological order. We open on the ruin
and walk backward, scene by scene, to the innocent beginning. If the
generated draft honours that staged order — opening on the aftermath,
building dread as the cause assembles backward, rendering the final
(earliest-in-time) scene drenched in everything the audience now knows —
then the substrate's STRUCTURE is driving the generation, not the
model's chronological instinct.

The fable. Tomas has built his whole name on a creed: he never lies, not
even by silence. His sworn friend from boyhood, Aleks, is present when a
man, Viktor, is killed in a brawl — present but innocent; he tried to
stop it. Tomas, passing, saw him there. Aleks begs Tomas only to stay
silent — not to lie, merely to omit that he saw him — because the bare
fact, stripped of its context, will hang him. Tomas cannot: his creed
forbids even a silence that deceives. At the trial he gives the plain
fact, truthfully and without the saving context, and it condemns Aleks.
**Peripeteia:** the honesty Tomas was proudest of is the instrument of
an innocent's death. Aleks, condemned, sees too late that his friend
loved being the honest man more than he loved him (an anti-recognition).
Aleks is executed — he is the pathos-centre, the one who pays. Alone
afterward, Tomas recognises that there was a truth deeper than the facts
— mercy, the friend before the creed — and that he betrayed it for his
name (the anagnorisis, too late). The man of plain words never speaks
again: his undoing is silence, the inversion of his creed.

Layers: this is the substrate; the Aristotelian overlay is
`sworn_aristotelian.py`. Story-time τ_s runs -50 … 20; the sjuzhet
stages it strictly backward (τ_d 0 → 9 maps to τ_s 20 → -50).
"""

from __future__ import annotations

from story_engine.core.substrate import (
    Entity, Prop, Event,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
    Description, Attention, anchor_event,
)


# ----------------------------------------------------------------------------
# Entities
# ----------------------------------------------------------------------------

tomas  = Entity(id="tomas",  name="Tomas",  kind="agent")
aleks  = Entity(id="aleks",  name="Aleks",  kind="agent")
viktor = Entity(id="viktor", name="Viktor", kind="agent")  # the man who dies

court  = Entity(id="court",  name="the assize court", kind="location")
tavern = Entity(id="tavern", name="the tavern yard",  kind="location")

ENTITIES = [tomas, aleks, viktor, court, tavern]
AGENT_IDS = [e.id for e in ENTITIES if e.kind == "agent"]


# ----------------------------------------------------------------------------
# Proposition constructors
# ----------------------------------------------------------------------------

def sworn_friends(a: str, b: str) -> Prop:    return Prop("sworn_friends", (a, b))
def never_lies(who: str) -> Prop:             return Prop("never_lies", (who,))
def dead(who: str) -> Prop:                   return Prop("dead", (who,))
def innocent(who: str) -> Prop:               return Prop("innocent", (who,))
def present_at_scene(who: str) -> Prop:       return Prop("present_at_scene", (who,))
def saw_at_scene(seer: str, seen: str) -> Prop:
    return Prop("saw_at_scene", (seer, seen))
def asked_silence(asker: str, of: str) -> Prop:
    return Prop("asked_for_silence", (asker, of))
def chose_plain_truth(who: str) -> Prop:      return Prop("chose_plain_truth", (who,))
def testified_plainly(who: str) -> Prop:      return Prop("testified_plainly", (who,))
def condemned(who: str) -> Prop:              return Prop("condemned", (who,))
def vanity_not_truth_killed(who: str, whom: str) -> Prop:
    return Prop("vanity_not_truth_killed", (who, whom))
def executed(who: str) -> Prop:               return Prop("executed", (who,))
def chose_name_over_friend(who: str) -> Prop:
    return Prop("chose_name_over_friend", (who,))
def silent_forever(who: str) -> Prop:         return Prop("silent_forever", (who,))


# ----------------------------------------------------------------------------
# Effect helpers
# ----------------------------------------------------------------------------

def world(p: Prop, asserts: bool = True) -> WorldEffect:
    return WorldEffect(prop=p, asserts=asserts)


def observe(agent_id: str, p: Prop, τ: int, slot: Slot = Slot.KNOWN,
            confidence: Confidence = Confidence.CERTAIN,
            note: str = "", via: str = None) -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(prop=p, slot=slot, confidence=confidence,
                  via=via or Diegetic.OBSERVATION.value,
                  provenance=(f"observed @ τ_s={τ}{(': ' + note) if note else ''}",)),
    )


def realize(agent_id: str, p: Prop, τ: int, note: str = "") -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(prop=p, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                  via=Diegetic.REALIZATION.value,
                  provenance=(f"realized @ τ_s={τ}{(': ' + note) if note else ''}",)),
    )


def told_by(listener: str, speaker: str, p: Prop, τ: int) -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=listener,
        held=Held(prop=p, slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                  via=Diegetic.UTTERANCE_HEARD.value,
                  provenance=(f"told by {speaker} @ τ_s={τ}",)),
    )


# ----------------------------------------------------------------------------
# Fabula — chronological (τ_s = -50 … 20). All on :canonical, committed.
# ----------------------------------------------------------------------------

FABULA = [

    Event(
        id="E_friendship",
        type="bond",
        τ_s=-50, τ_a=1,
        participants={"a": "tomas", "b": "aleks"},
        effects=(
            world(sworn_friends("tomas", "aleks")),
            observe("tomas", sworn_friends("tomas", "aleks"), -50,
                    note="boyhood friends; they swore to stand for each other"),
            observe("aleks", sworn_friends("tomas", "aleks"), -50),
        ),
    ),

    Event(
        id="E_tomas_creed",
        type="establishing",
        τ_s=-30, τ_a=2,
        participants={"man": "tomas"},
        effects=(
            world(never_lies("tomas")),
            observe("tomas", never_lies("tomas"), -30,
                    note="he built his name on the plain truth; he will not lie, "
                         "not even by a silence that deceives — it is his honour"),
        ),
    ),

    Event(
        id="E_viktor_dies",
        type="killing",
        τ_s=-10, τ_a=3,
        participants={"victim": "viktor", "present": "aleks",
                      "witness": "tomas", "place": "tavern"},
        effects=(
            world(dead("viktor")),
            world(innocent("aleks")),
            world(present_at_scene("aleks")),
            observe("tomas", saw_at_scene("tomas", "aleks"), -10,
                    note="passing the tavern yard, Tomas saw Aleks there over the body — "
                         "Aleks had tried to stop the brawl, but the bare sight damns"),
        ),
    ),

    Event(
        id="E_aleks_asks",
        type="plea",
        τ_s=-9, τ_a=4,
        participants={"asker": "aleks", "of": "tomas"},
        effects=(
            world(asked_silence("aleks", "tomas")),
            observe("aleks", innocent("aleks"), -9,
                    note="he begs Tomas only to stay silent — not to lie, merely to omit "
                         "that he saw him — for the fact without the context will hang him"),
            told_by("tomas", "aleks", innocent("aleks"), -9),
        ),
    ),

    Event(
        id="E_tomas_chooses",
        type="choice",
        τ_s=-8, τ_a=5,
        participants={"man": "tomas"},
        effects=(
            world(chose_plain_truth("tomas")),
            observe("tomas", chose_plain_truth("tomas"), -8,
                    note="his creed forbids even a deceiving silence; he resolves to "
                         "give the plain fact and let the court weigh it — the hamartia"),
        ),
    ),

    Event(
        id="E_the_testimony",
        type="catastrophe",
        τ_s=0, τ_a=6,
        participants={"witness": "tomas", "accused": "aleks", "place": "court"},
        effects=(
            world(testified_plainly("tomas")),
            observe("tomas", testified_plainly("tomas"), 0,
                    note="he swears and gives the bare fact — he saw Aleks over the body — "
                         "truthfully, without the saving context, because plain truth is his creed"),
        ),
    ),

    Event(
        id="E_the_verdict",
        type="condemnation",
        τ_s=1, τ_a=7,
        participants={"accused": "aleks", "witness": "tomas", "place": "court"},
        effects=(
            world(condemned("aleks")),
            realize("aleks", vanity_not_truth_killed("tomas", "aleks"), 1,
                    note="condemned on the bare fact, Aleks looks at his friend and sees — "
                         "too late — that Tomas loved being the honest man more than he loved him"),
        ),
    ),

    Event(
        id="E_execution",
        type="death",
        τ_s=3, τ_a=8,
        participants={"condemned": "aleks"},
        effects=(
            world(executed("aleks")),
            world(dead("aleks")),
        ),
    ),

    Event(
        id="E_tomas_alone",
        type="recognition",
        τ_s=10, τ_a=9,
        participants={"man": "tomas"},
        effects=(
            realize("tomas", chose_name_over_friend("tomas"), 10,
                    note="alone with it, he recognises there was a truth deeper than the "
                         "facts — mercy, the friend before the creed — and he betrayed it for his name"),
        ),
    ),

    Event(
        id="E_tomas_silent",
        type="undoing",
        τ_s=20, τ_a=10,
        participants={"man": "tomas"},
        effects=(
            world(silent_forever("tomas")),
            observe("tomas", silent_forever("tomas"), 20,
                    note="the man of plain words never speaks again; his undoing is silence, "
                         "the inversion of the creed that ruled him"),
        ),
    ),
]


# ----------------------------------------------------------------------------
# Preplay disclosures — what the audience holds at the FIRST staged scene
# (which, in this reverse telling, is the end of the story): the outcome is
# known from the opening image; the backward staging assembles the CAUSE.
# ----------------------------------------------------------------------------

PREPLAY_DISCLOSURES = (
    Disclosure(prop=dead("aleks"), slot=Slot.KNOWN,
               confidence=Confidence.CERTAIN, via=Narrative.DISCLOSURE.value),
    Disclosure(prop=executed("aleks"), slot=Slot.KNOWN,
               confidence=Confidence.CERTAIN, via=Narrative.DISCLOSURE.value),
    Disclosure(prop=silent_forever("tomas"), slot=Slot.KNOWN,
               confidence=Confidence.CERTAIN, via=Narrative.DISCLOSURE.value),
    Disclosure(prop=sworn_friends("tomas", "aleks"), slot=Slot.KNOWN,
               confidence=Confidence.CERTAIN, via=Narrative.DISCLOSURE.value),
)


# ----------------------------------------------------------------------------
# Sjuzhet — STRICT REVERSE: τ_d 0→9 stages τ_s 20→-50. The audience meets
# the ruin first and the innocent beginning last.
# ----------------------------------------------------------------------------

SJUZHET = [
    SjuzhetEntry(event_id="E_tomas_silent", τ_d=0, focalizer_id="tomas",
                 disclosures=PREPLAY_DISCLOSURES),
    SjuzhetEntry(event_id="E_tomas_alone", τ_d=1, focalizer_id="tomas"),
    SjuzhetEntry(event_id="E_execution", τ_d=2, focalizer_id=None),
    SjuzhetEntry(event_id="E_the_verdict", τ_d=3, focalizer_id="aleks"),
    SjuzhetEntry(event_id="E_the_testimony", τ_d=4, focalizer_id="tomas"),
    SjuzhetEntry(event_id="E_tomas_chooses", τ_d=5, focalizer_id="tomas"),
    SjuzhetEntry(event_id="E_aleks_asks", τ_d=6, focalizer_id="aleks"),
    SjuzhetEntry(event_id="E_viktor_dies", τ_d=7, focalizer_id=None),
    SjuzhetEntry(event_id="E_tomas_creed", τ_d=8, focalizer_id="tomas"),
    SjuzhetEntry(event_id="E_friendship", τ_d=9, focalizer_id=None),
]


# ----------------------------------------------------------------------------
# Descriptions — the tragic frame, and (crucially) the reverse-telling frame.
# ----------------------------------------------------------------------------

DESCRIPTIONS = [
    Description(
        id="D_we_begin_at_the_end",
        attached_to=anchor_event("E_tomas_silent"),
        kind="reader-frame", attention=Attention.STRUCTURAL,
        text=("We begin at the end. This is the first scene the audience "
              "sees and the LAST in the story's time: years on, Tomas, the "
              "man who never lied, has stopped speaking altogether. The "
              "story now walks backward to find the small, plain word that "
              "did this. Render the silence as a finished thing whose cause "
              "we do not yet know — the question the backward telling will "
              "answer."),
        authored_by="author", τ_a=100,
    ),
    Description(
        id="D_peripeteia_plain_truth",
        attached_to=anchor_event("E_the_testimony"),
        kind="reader-frame", attention=Attention.STRUCTURAL,
        text=("The peripeteia, and by now the audience already knows it kills "
              "Aleks — it has watched the execution and the verdict in the "
              "scenes before. The horror is not surprise but inevitability: "
              "Tomas's plain truth, the thing he is proudest of, is the "
              "murder weapon, because the bare fact without mercy is a lie of "
              "the worst kind. Render his honesty as the blade."),
        authored_by="author", τ_a=101,
    ),
    Description(
        id="D_aleks_anti_recognition",
        attached_to=anchor_event("E_the_verdict"),
        kind="reader-frame", attention=Attention.INTERPRETIVE,
        text=("Aleks is the pathos-centre, and here he comes to an anti-"
              "recognition: condemned on his friend's bare fact, he sees too "
              "late that Tomas loved being the honest man more than he loved "
              "him. The recognition is complete and powerless. He is the one "
              "who pays for the creed; the error is Tomas's, the death is his."),
        authored_by="author", τ_a=102,
    ),
    Description(
        id="D_anagnorisis_deeper_truth",
        attached_to=anchor_event("E_tomas_alone"),
        kind="reader-frame", attention=Attention.STRUCTURAL,
        text=("The anagnorisis. Tomas recognises that there was a truth "
              "deeper than the facts — mercy, the friend before the creed — "
              "and that he betrayed it for his name. Staged near the "
              "opening (it is late in the story), so the audience meets his "
              "ruin before it understands the choice that caused it."),
        authored_by="author", τ_a=103,
    ),
    Description(
        id="D_the_last_scene_is_the_first",
        attached_to=anchor_event("E_friendship"),
        kind="reader-frame", attention=Attention.STRUCTURAL,
        text=("The last scene staged is the first in time: the two of them "
              "as boys, swearing to stand for each other, before any of it. "
              "By now the audience knows everything — the testimony, the "
              "rope, the silence. Render the warmth as unbearable precisely "
              "because we know where it goes; every easy word between them "
              "is shadowed by the plain word that will undo it. End the play "
              "on the vow, and let the vow indict the creed that broke it."),
        authored_by="author", τ_a=104,
    ),
]
