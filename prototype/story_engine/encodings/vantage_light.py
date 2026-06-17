"""
vantage_light.py — "The Vantage Light", an ORIGINAL tragedy substrate.

Not from any canon. Authored to test whether the story engine
(substrate → verified overlay → generated draft → fidelity evaluation)
is a story GENERATOR or merely a renderer of works the model already
knows. If a story the model has never read as a finished work still
compiles, verifies, generates faithfully, and moves — the pipeline
generalizes.

The fable. Halvard keeps the Vantage Light on a hard coast. Thirty
years, no ship lost on his watch — a record that is the scar over his
drowned wife, Maren, whom the sea took in a storm he could not beat. He
raised his daughter Inga at the light. A young harbourmaster, Tobias,
brings a storm-glass and a warning: a great storm is coming; signal the
inbound grain-ship to anchor offshore rather than make the harbour run.
Halvard's hamartia is pride in the record — to signal danger is to
confess the sea can best him — and he trusts his own eye over the glass
and refuses. Inga reads the falling glass, believes the warning, and
when her father will not signal she takes the dory and a hand-lantern
into the surf to warn the ship herself. The storm breaks; Captain Rost,
trusting the keeper's never-failing light, makes the run — and the
steady light guides his ship onto the skerry. **Peripeteia:** the thing
Halvard kept most perfectly is the instrument of the wreck; the record
breaks. **Pathos-centre:** Inga drowns in the attempt — she pays for
his pride. **Anagnorisis:** Halvard finds her body and recognises that
the sea did not best him; he bested himself. He lets the light go dark.

Layers (this file is the substrate; the Aristotelian overlay is
`vantage_light_aristotelian.py`):
- 6 entities (5 agents incl. the dead wife + the ship's captain; 2
  locations), 14 fabula events (τ_s = -40 … 13), preplay disclosures
  (the backstory the audience enters holding), a chronological sjuzhet
  (NOT in medias res — Oedipus already exercises that), and authorial
  descriptions carrying the tragic frame.
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

halvard = Entity(id="halvard", name="Halvard", kind="agent")
inga    = Entity(id="inga",    name="Inga",    kind="agent")
tobias  = Entity(id="tobias",  name="Tobias (the harbourmaster)", kind="agent")
captain = Entity(id="captain_rost", name="Captain Rost", kind="agent")
maren   = Entity(id="maren",   name="Maren", kind="agent")  # the drowned wife

vantage = Entity(id="vantage_light", name="the Vantage Light", kind="location")
skerry  = Entity(id="skerry", name="the Skerry", kind="location")

ENTITIES = [halvard, inga, tobias, captain, maren, vantage, skerry]
AGENT_IDS = [e.id for e in ENTITIES if e.kind == "agent"]


# ----------------------------------------------------------------------------
# Proposition constructors
# ----------------------------------------------------------------------------

def dead(who: str) -> Prop:                 return Prop("dead", (who,))
def lost_at_sea(who: str) -> Prop:          return Prop("lost_at_sea", (who,))
def record_unbroken(who: str) -> Prop:      return Prop("record_unbroken", (who,))
def keeps_light(who: str) -> Prop:          return Prop("keeps_light", (who,))
def learned_the_light(who: str) -> Prop:    return Prop("learned_the_light", (who,))
def storm_coming() -> Prop:                 return Prop("storm_coming", ())
def glass_falling() -> Prop:                return Prop("glass_falling", ())
def trusts_own_eye(who: str) -> Prop:       return Prop("trusts_own_eye", (who,))
def refused_to_signal(who: str) -> Prop:    return Prop("refused_to_signal", (who,))
def storm_active() -> Prop:                 return Prop("storm_active", ())
def ship_inbound(who: str) -> Prop:         return Prop("ship_inbound", (who,))
def trusts_light(who: str) -> Prop:         return Prop("trusts_light", (who,))
def at_sea_alone(who: str) -> Prop:         return Prop("at_sea_alone", (who,))
def ship_wrecked(who: str) -> Prop:         return Prop("ship_wrecked", (who,))
def record_broken(who: str) -> Prop:        return Prop("record_broken", (who,))
def light_betrayed_me(who: str) -> Prop:    return Prop("light_betrayed_me", (who,))
def drowned(who: str) -> Prop:              return Prop("drowned", (who,))
def pride_killed(who: str, whom: str) -> Prop:
    return Prop("pride_not_sea_killed", (who, whom))
def light_dark() -> Prop:                   return Prop("light_dark", ())
def undone(who: str) -> Prop:               return Prop("undone", (who,))


# ----------------------------------------------------------------------------
# Effect helpers
# ----------------------------------------------------------------------------

def world(p: Prop, asserts: bool = True) -> WorldEffect:
    return WorldEffect(prop=p, asserts=asserts)


def observe(agent_id: str, p: Prop, τ: int,
            slot: Slot = Slot.KNOWN,
            confidence: Confidence = Confidence.CERTAIN,
            note: str = "", via: str = None) -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(
            prop=p, slot=slot, confidence=confidence,
            via=via or Diegetic.OBSERVATION.value,
            provenance=(f"observed @ τ_s={τ}{(': ' + note) if note else ''}",),
        ),
    )


def realize(agent_id: str, p: Prop, τ: int, note: str = "") -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(
            prop=p, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
            via=Diegetic.REALIZATION.value,
            provenance=(f"realized @ τ_s={τ}{(': ' + note) if note else ''}",),
        ),
    )


def told_by(listener: str, speaker: str, p: Prop, τ: int,
            slot: Slot = Slot.BELIEVED,
            confidence: Confidence = Confidence.BELIEVED) -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=listener,
        held=Held(
            prop=p, slot=slot, confidence=confidence,
            via=Diegetic.UTTERANCE_HEARD.value,
            provenance=(f"told by {speaker} @ τ_s={τ}",),
        ),
    )


# ----------------------------------------------------------------------------
# Fabula — chronological, all on :canonical, status=committed
# ----------------------------------------------------------------------------

FABULA = [

    # --- Antecedent (τ_s < 0): the wound, the bond, the pride. ---

    Event(
        id="E_maren_lost",
        type="bereavement",
        τ_s=-40, τ_a=1,
        participants={"keeper": "halvard", "lost": "maren"},
        effects=(
            world(lost_at_sea("maren")),
            world(dead("maren")),
            observe("halvard", lost_at_sea("maren"), -40,
                    note="the storm he could not beat; the wound under the record"),
        ),
    ),

    Event(
        id="E_inga_raised",
        type="upbringing",
        τ_s=-30, τ_a=2,
        participants={"keeper": "halvard", "child": "inga"},
        effects=(
            world(learned_the_light("inga")),
            observe("inga", keeps_light("halvard"), -30,
                    note="learned the light at his side; reads the glass as he taught her"),
        ),
    ),

    Event(
        id="E_record_kept",
        type="establishing",
        τ_s=-1, τ_a=3,
        participants={"keeper": "halvard"},
        effects=(
            world(record_unbroken("halvard")),
            observe("halvard", record_unbroken("halvard"), -1,
                    note="thirty years, no ship lost on his watch — the record is his honour"),
        ),
    ),

    # --- Beginning's hinge: the warning arrives (complication). ---

    Event(
        id="E_tobias_brings_warning",
        type="warning",
        τ_s=0, τ_a=4,
        participants={"bringer": "tobias", "keeper": "halvard"},
        effects=(
            world(glass_falling()),
            observe("tobias", storm_coming(), 0,
                    note="the storm-glass is falling fast; a great blow is coming"),
            told_by("halvard", "tobias", storm_coming(), 0),
        ),
    ),

    # --- Middle: the refusal, the daughter's resolve, the storm. ---

    Event(
        id="E_halvard_dismisses",
        type="refusal",
        τ_s=2, τ_a=5,
        participants={"keeper": "halvard"},
        effects=(
            observe("halvard", trusts_own_eye("halvard"), 2,
                    note="he has read this coast longer than that glass has existed"),
        ),
    ),

    Event(
        id="E_inga_sees_glass",
        type="reading",
        τ_s=3, τ_a=6,
        participants={"reader": "inga"},
        effects=(
            observe("inga", storm_coming(), 3,
                    note="she reads the falling glass and believes it"),
        ),
    ),

    Event(
        id="E_halvard_refuses",
        type="choice",
        τ_s=4, τ_a=7,
        participants={"keeper": "halvard", "daughter": "inga"},
        effects=(
            world(refused_to_signal("halvard")),
            observe("halvard", refused_to_signal("halvard"), 4,
                    note="to raise the danger-signal is to confess the sea can best him"),
        ),
    ),

    Event(
        id="E_storm_breaks",
        type="storm",
        τ_s=6, τ_a=8,
        participants={"place": "vantage_light"},
        effects=(
            world(storm_active()),
        ),
    ),

    Event(
        id="E_ship_makes_run",
        type="approach",
        τ_s=7, τ_a=9,
        participants={"captain": "captain_rost", "toward": "vantage_light"},
        effects=(
            world(ship_inbound("captain_rost")),
            observe("captain_rost", trusts_light("halvard"), 7,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="the Vantage Light has never failed; he runs for the harbour on its word"),
        ),
    ),

    Event(
        id="E_inga_takes_dory",
        type="resolve",
        τ_s=8, τ_a=10,
        participants={"daughter": "inga", "toward": "skerry"},
        effects=(
            world(at_sea_alone("inga")),
            observe("inga", at_sea_alone("inga"), 8,
                    note="when her father will not signal, she takes the dory and a hand-lantern into the surf"),
        ),
    ),

    # --- End: the reversal, the death, the recognition, the dark. ---

    Event(
        id="E_ship_founders",
        type="catastrophe",
        τ_s=9, τ_a=11,
        participants={"captain": "captain_rost", "keeper": "halvard",
                      "place": "skerry"},
        effects=(
            world(ship_wrecked("captain_rost")),
            world(record_broken("halvard")),
            realize("captain_rost", light_betrayed_me("halvard"), 9,
                    note="too late — the steady light he trusted has led him onto the skerry"),
        ),
    ),

    Event(
        id="E_inga_drowns",
        type="death",
        τ_s=10, τ_a=12,
        participants={"daughter": "inga", "place": "skerry"},
        effects=(
            world(dead("inga")),
            world(drowned("inga")),
        ),
    ),

    Event(
        id="E_halvard_finds_inga",
        type="recognition",
        τ_s=11, τ_a=13,
        participants={"keeper": "halvard", "daughter": "inga"},
        effects=(
            realize("halvard", pride_killed("halvard", "inga"), 11,
                    note="not the sea — his pride; he finds her body and the spent hand-lantern"),
        ),
    ),

    Event(
        id="E_halvard_dark",
        type="undoing",
        τ_s=13, τ_a=14,
        participants={"keeper": "halvard", "place": "vantage_light"},
        effects=(
            world(light_dark()),
            observe("halvard", undone("halvard"), 13,
                    note="he lets the light go out; the record, the honour, and the man are gone"),
        ),
    ),
]


# ----------------------------------------------------------------------------
# Preplay disclosures — the backstory the audience enters holding.
# ----------------------------------------------------------------------------

PREPLAY_DISCLOSURES = (
    Disclosure(prop=dead("maren"), slot=Slot.KNOWN,
               confidence=Confidence.CERTAIN, via=Narrative.DISCLOSURE.value),
    Disclosure(prop=lost_at_sea("maren"), slot=Slot.KNOWN,
               confidence=Confidence.CERTAIN, via=Narrative.DISCLOSURE.value),
    Disclosure(prop=record_unbroken("halvard"), slot=Slot.KNOWN,
               confidence=Confidence.CERTAIN, via=Narrative.DISCLOSURE.value),
    Disclosure(prop=learned_the_light("inga"), slot=Slot.KNOWN,
               confidence=Confidence.CERTAIN, via=Narrative.DISCLOSURE.value),
)


# ----------------------------------------------------------------------------
# Sjuzhet — chronological staging, varied focalization. The pathos-centre
# (Inga) focalizes her three beats (reading the glass, taking the dory,
# drowning) so her suffering is rendered from within; Halvard focalizes
# the pride and the recognition; the captain focalizes the wreck.
# ----------------------------------------------------------------------------

SJUZHET = [
    SjuzhetEntry(event_id="E_maren_lost", τ_d=0, focalizer_id=None,
                 disclosures=PREPLAY_DISCLOSURES),
    SjuzhetEntry(event_id="E_inga_raised", τ_d=1, focalizer_id=None),
    SjuzhetEntry(event_id="E_record_kept", τ_d=2, focalizer_id="halvard"),
    SjuzhetEntry(event_id="E_tobias_brings_warning", τ_d=3, focalizer_id="tobias",
                 disclosures=(
                     Disclosure(prop=storm_coming(), slot=Slot.KNOWN,
                                confidence=Confidence.CERTAIN,
                                via=Narrative.DISCLOSURE.value),
                 )),
    SjuzhetEntry(event_id="E_halvard_dismisses", τ_d=4, focalizer_id="halvard"),
    SjuzhetEntry(event_id="E_inga_sees_glass", τ_d=5, focalizer_id="inga"),
    SjuzhetEntry(event_id="E_halvard_refuses", τ_d=6, focalizer_id="halvard"),
    SjuzhetEntry(event_id="E_storm_breaks", τ_d=7, focalizer_id=None),
    SjuzhetEntry(event_id="E_ship_makes_run", τ_d=8, focalizer_id="captain_rost"),
    SjuzhetEntry(event_id="E_inga_takes_dory", τ_d=9, focalizer_id="inga"),
    SjuzhetEntry(event_id="E_ship_founders", τ_d=10, focalizer_id="captain_rost"),
    SjuzhetEntry(event_id="E_inga_drowns", τ_d=11, focalizer_id="inga"),
    SjuzhetEntry(event_id="E_halvard_finds_inga", τ_d=12, focalizer_id="halvard"),
    SjuzhetEntry(event_id="E_halvard_dark", τ_d=13, focalizer_id="halvard"),
]


# ----------------------------------------------------------------------------
# Descriptions — the tragic frame, attached to the load-bearing beats.
# ----------------------------------------------------------------------------

DESCRIPTIONS = [
    Description(
        id="D_record_is_the_scar",
        attached_to=anchor_event("E_record_kept"),
        kind="reader-frame", attention=Attention.INTERPRETIVE,
        text=("The unbroken record is not vanity but a scar. Maren drowned "
              "in a storm Halvard could not beat; ever since, 'no ship lost "
              "on my watch' has been the wall he built against that night. "
              "Render the pride as grief that has hardened into law."),
        authored_by="author", τ_a=100,
    ),
    Description(
        id="D_the_hamartia",
        attached_to=anchor_event("E_halvard_refuses"),
        kind="reader-frame", attention=Attention.STRUCTURAL,
        text=("The hamartia, in action. Halvard's error is not cruelty but "
              "pride mistaken for fidelity: to raise the danger-signal would "
              "be to admit the sea can best his judgement, and that he cannot "
              "do. He chooses the record over the warning — and the warning "
              "is true."),
        authored_by="author", τ_a=101,
    ),
    Description(
        id="D_peripeteia_the_light_betrays",
        attached_to=anchor_event("E_ship_founders"),
        kind="reader-frame", attention=Attention.STRUCTURAL,
        text=("The peripeteia. The thing Halvard kept most perfectly — the "
              "steady, never-failing light — is the very instrument of the "
              "wreck: trusting it, the captain runs for a harbour that the "
              "storm has made a grave. His virtue becomes the mechanism of "
              "the catastrophe. The record breaks in the same instant."),
        authored_by="author", τ_a=102,
    ),
    Description(
        id="D_inga_is_the_pathos",
        attached_to=anchor_event("E_inga_drowns"),
        kind="reader-frame", attention=Attention.INTERPRETIVE,
        text=("Inga is the pathos-centre. The error is Halvard's; the "
              "suffering is hers. She believed the glass her father taught "
              "her to read, and when he would not act she acted, and the sea "
              "took her as it took her mother. Render her death as the play's "
              "centre of pity — not the agent of the recognition, but the one "
              "who pays for it."),
        authored_by="author", τ_a=103,
    ),
    Description(
        id="D_anagnorisis_too_late",
        attached_to=anchor_event("E_halvard_finds_inga"),
        kind="reader-frame", attention=Attention.STRUCTURAL,
        text=("The anagnorisis, and it is too late. Halvard finds Inga's body "
              "and the spent hand-lantern, and the recognition lands whole: "
              "the sea did not best him — he bested himself; his pride, not "
              "the storm, is what drowned his daughter and wrecked the ship. "
              "The knowledge changes nothing it could have saved."),
        authored_by="author", τ_a=104,
    ),
]
