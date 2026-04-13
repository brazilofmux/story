"""
Oedipus Rex — the encoded fabula and sjuzhet slice.

Story content only. No substrate logic. This file defines entities, events,
sjuzhet entries, and the predicates used in propositions, sufficient to
exercise the substrate on the Messenger + Shepherd → anagnorisis slice.

Fidelity choices:

- Pre-play fabula (Laius's prophecy, infant exposure, Oedipus's Corinthian
  upbringing, the crossroads killing, the marriage) is represented as
  canonical events at negative τ_s. These are never *narrated* in the play
  — Sophocles opens in medias res. For the prototype, we disclose the key
  pre-play facts to the reader at τ_d = 0 on the premise that the original
  audience knew the myth and came in with the facts already loaded. This
  is what makes the whole play an exercise in dramatic irony.

- In-play events are a selected slice, not the full play. Minimum required
  to exercise the substrate's irony, reveal, and realization machinery:
  Jocasta's mention of the crossroads, the Messenger's two-step disclosure,
  Jocasta's own anagnorisis, the Shepherd's testimony, and Oedipus's
  anagnorisis.

- Some compressions for clarity. Tiresias is cut; Creon's dispatch is
  cut; the chorus is cut. None of these is substrate-relevant at the grain
  of this prototype, and including them would drown the irony signal in
  bookkeeping.
"""

from __future__ import annotations

from substrate import (
    Entity, Prop, Event, EventStatus, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
)


# ----------------------------------------------------------------------------
# Entities
# ----------------------------------------------------------------------------

oedipus  = Entity(id="oedipus",  name="Oedipus",  kind="agent")
jocasta  = Entity(id="jocasta",  name="Jocasta",  kind="agent")
laius    = Entity(id="laius",    name="Laius",    kind="agent")
polybus  = Entity(id="polybus",  name="Polybus",  kind="agent")
merope   = Entity(id="merope",   name="Merope",   kind="agent")
messenger = Entity(id="messenger", name="Corinthian Messenger", kind="agent")
shepherd = Entity(id="shepherd", name="Theban Shepherd", kind="agent")

thebes     = Entity(id="thebes",     name="Thebes",     kind="location")
corinth    = Entity(id="corinth",    name="Corinth",    kind="location")
crossroads = Entity(id="crossroads", name="the Crossroads", kind="location")
cithaeron  = Entity(id="cithaeron",  name="Mount Cithaeron", kind="location")

ENTITIES = [
    oedipus, jocasta, laius, polybus, merope, messenger, shepherd,
    thebes, corinth, crossroads, cithaeron,
]

AGENT_IDS = [e.id for e in ENTITIES if e.kind == "agent"]

# ----------------------------------------------------------------------------
# Proposition constructors
# ----------------------------------------------------------------------------

def child_of(child: str, parent: str) -> Prop:
    return Prop("child_of", (child, parent))

def killed(killer: str, victim: str) -> Prop:
    return Prop("killed", (killer, victim))

def dead(who: str) -> Prop:
    return Prop("dead", (who,))

def married(a: str, b: str) -> Prop:
    return Prop("married", (a, b))

def king(who: str, place: str) -> Prop:
    return Prop("king", (who, place))

def killed_stranger_at_crossroads(who: str) -> Prop:
    return Prop("killed_stranger_at_crossroads", (who,))

def prophecy_self() -> Prop:
    # Oedipus's personal prophecy: he will kill his father and marry his mother.
    return Prop("prophecy_will_kill_father_and_marry_mother", ("oedipus",))

def adopted_by(child: str, parent: str) -> Prop:
    return Prop("adopted_by", (child, parent))

def real_parents_of_oedipus_are(parent: str) -> Prop:
    # A proposition used as a GAP: Oedipus knows he doesn't know his real parents.
    # We still need a concrete proposition, so parametrize by candidate.
    return Prop("real_parent_of_oedipus", (parent,))

# A GAP placeholder: Oedipus wonders who his real parents are.
# This is a GAP, not a concrete proposition. For the prototype we model the
# gap as the proposition "Oedipus's real parents are identified" being
# held in the GAP slot on Oedipus's state, with the understanding that
# filling this gap happens at the anagnorisis.
gap_real_parents = Prop("real_parents_identified", ("oedipus",))


# ----------------------------------------------------------------------------
# Event helpers
# ----------------------------------------------------------------------------

def observe(agent_id: str, p: Prop, τ: int, confidence: Confidence = Confidence.CERTAIN,
            slot: Slot = Slot.KNOWN, note: str = "") -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(
            prop=p, slot=slot, confidence=confidence,
            via=Diegetic.OBSERVATION.value,
            provenance=(f"observed @ τ_s={τ}{(': ' + note) if note else ''}",),
        ),
    )

def told_by(listener_id: str, speaker_id: str, p: Prop, τ: int,
            confidence: Confidence = Confidence.BELIEVED,
            slot: Slot = Slot.BELIEVED) -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=listener_id,
        held=Held(
            prop=p, slot=slot, confidence=confidence,
            via=Diegetic.UTTERANCE_HEARD.value,
            provenance=(f"told by {speaker_id} @ τ_s={τ}",),
        ),
    )

def realize_add(agent_id: str, p: Prop, τ: int, note: str = "") -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(
            prop=p, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
            via=Diegetic.REALIZATION.value,
            provenance=(f"realized @ τ_s={τ}{(': ' + note) if note else ''}",),
        ),
    )

def realize_remove(agent_id: str, p: Prop, τ: int) -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(
            prop=p, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
            via=Diegetic.REALIZATION.value,
            provenance=(f"realization removed @ τ_s={τ}",),
        ),
        remove=True,
    )

def world(p: Prop, asserts: bool = True) -> WorldEffect:
    return WorldEffect(prop=p, asserts=asserts)


# ----------------------------------------------------------------------------
# Fabula — all events on :canonical, status=committed
# ----------------------------------------------------------------------------

FABULA = [

    # --- Pre-play (τ_s < 0) ---

    Event(
        id="E_birth",
        type="birth",
        τ_s=-100, τ_a=1,
        participants={"child": "oedipus", "father": "laius", "mother": "jocasta"},
        effects=(
            world(child_of("oedipus", "laius")),
            world(child_of("oedipus", "jocasta")),
            observe("laius",   child_of("oedipus", "laius"),   -100, note="witnessed birth"),
            observe("laius",   child_of("oedipus", "jocasta"), -100, note="witnessed birth"),
            observe("jocasta", child_of("oedipus", "laius"),   -100, note="witnessed birth"),
            observe("jocasta", child_of("oedipus", "jocasta"), -100, note="witnessed birth"),
        ),
    ),

    Event(
        id="E_exposure_and_rescue",
        type="exposure",
        τ_s=-99, τ_a=2,
        participants={"infant": "oedipus", "rescuer": "shepherd", "courier": "messenger"},
        effects=(
            # Jocasta and Laius believe the infant died on Cithaeron.
            observe("jocasta", dead("oedipus"), -99, slot=Slot.BELIEVED,
                    confidence=Confidence.BELIEVED, note="thinks exposure succeeded"),
            observe("laius",   dead("oedipus"), -99, slot=Slot.BELIEVED,
                    confidence=Confidence.BELIEVED, note="thinks exposure succeeded"),
            # The shepherd knows: baby came from Laius's house, was not killed.
            observe("shepherd", child_of("oedipus", "laius"), -99,
                    note="served in Laius's house; knows the baby's parentage"),
            observe("shepherd", child_of("oedipus", "jocasta"), -99, note="same"),
            # The Corinthian messenger knows: he received the baby from the
            # Theban shepherd and delivered him to Polybus.
            observe("messenger", adopted_by("oedipus", "polybus"), -99,
                    note="delivered the child himself"),
        ),
    ),

    Event(
        id="E_upbringing_in_corinth",
        type="upbringing",
        τ_s=-50, τ_a=3,
        participants={"child": "oedipus", "father": "polybus", "mother": "merope"},
        effects=(
            # Oedipus grows up believing Polybus and Merope are his parents.
            observe("oedipus", child_of("oedipus", "polybus"), -50, slot=Slot.BELIEVED,
                    confidence=Confidence.BELIEVED, note="raised as their son"),
            observe("oedipus", child_of("oedipus", "merope"), -50, slot=Slot.BELIEVED,
                    confidence=Confidence.BELIEVED, note="raised as their son"),
        ),
    ),

    Event(
        id="E_oracle_to_oedipus",
        type="prophecy_received",
        τ_s=-49, τ_a=4,
        participants={"recipient": "oedipus"},
        effects=(
            observe("oedipus", prophecy_self(), -49, note="hears the oracle at Delphi"),
        ),
    ),

    Event(
        id="E_crossroads_killing",
        type="killing",
        τ_s=-48, τ_a=5,
        participants={"killer": "oedipus", "victim": "laius"},
        effects=(
            world(killed("oedipus", "laius")),
            world(dead("laius")),
            # Oedipus knows he killed *someone* at a crossroads, but does not
            # recognize the man. The identity of the victim is not in Oedipus's
            # knowledge state.
            observe("oedipus", killed_stranger_at_crossroads("oedipus"), -48,
                    note="a travel-quarrel, unidentified victim"),
            # Laius, before dying, knew his killer was a young stranger, but
            # Laius dies here — his knowledge is moot from this τ_s forward.
        ),
    ),

    Event(
        id="E_marriage_and_crown",
        type="marriage",
        τ_s=-46, τ_a=6,
        participants={"husband": "oedipus", "wife": "jocasta"},
        effects=(
            world(married("oedipus", "jocasta")),
            world(king("oedipus", "thebes")),
            observe("oedipus", married("oedipus", "jocasta"), -46),
            observe("jocasta", married("oedipus", "jocasta"), -46),
            observe("oedipus", king("oedipus", "thebes"), -46),
            observe("jocasta", king("oedipus", "thebes"), -46),
        ),
    ),

    # --- Play (τ_s ≥ 0) ---

    Event(
        id="E_jocasta_mentions_crossroads",
        type="utterance",
        τ_s=5, τ_a=7,
        participants={"speaker": "jocasta", "listener": "oedipus"},
        effects=(
            # Jocasta, reassuring Oedipus, mentions that Laius was killed at a
            # crossroads by strangers. This plants a suspicion in Oedipus.
            told_by("oedipus", "jocasta",
                    Prop("laius_killed_at_crossroads", ()), 5,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            # Oedipus now suspects he might be the one who killed Laius.
            # Modeled as Oedipus gaining a SUSPECTED proposition about his
            # own culpability for Laius's death.
            KnowledgeEffect(
                agent_id="oedipus",
                held=Held(
                    prop=killed("oedipus", "laius"),
                    slot=Slot.SUSPECTED,
                    confidence=Confidence.SUSPECTED,
                    via=Diegetic.INFERENCE.value,
                    provenance=("inferred from Jocasta's mention of the crossroads @ τ_s=5",),
                ),
            ),
        ),
    ),

    Event(
        id="E_messenger_polybus_dead",
        type="utterance",
        τ_s=7, τ_a=8,
        participants={"speaker": "messenger", "listener": "oedipus"},
        effects=(
            world(dead("polybus")),
            told_by("oedipus", "messenger", dead("polybus"), 7,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            told_by("jocasta", "messenger", dead("polybus"), 7,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
        ),
    ),

    Event(
        id="E_messenger_adoption_reveal",
        type="utterance",
        τ_s=8, τ_a=9,
        participants={"speaker": "messenger", "listener": "oedipus"},
        effects=(
            # The messenger, trying to reassure Oedipus that the
            # prophecy-about-Polybus cannot apply, lets slip that he
            # himself brought the baby Oedipus to Polybus.
            told_by("oedipus", "messenger", adopted_by("oedipus", "polybus"), 8,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            told_by("jocasta", "messenger", adopted_by("oedipus", "polybus"), 8,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            # Oedipus's prior beliefs about his parentage are dislodged.
            KnowledgeEffect(
                agent_id="oedipus",
                held=Held(prop=child_of("oedipus", "polybus"),
                          slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                          via=Diegetic.REALIZATION.value,
                          provenance=("dislodged by adoption revelation @ τ_s=8",)),
                remove=True,
            ),
            KnowledgeEffect(
                agent_id="oedipus",
                held=Held(prop=child_of("oedipus", "merope"),
                          slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                          via=Diegetic.REALIZATION.value,
                          provenance=("dislodged by adoption revelation @ τ_s=8",)),
                remove=True,
            ),
            # Oedipus now has a GAP about his real parents.
            KnowledgeEffect(
                agent_id="oedipus",
                held=Held(
                    prop=gap_real_parents,
                    slot=Slot.GAP, confidence=Confidence.OPEN,
                    via=Diegetic.INFERENCE.value,
                    provenance=("opened after adoption revelation @ τ_s=8",),
                ),
            ),
        ),
    ),

    Event(
        id="E_jocasta_realizes",
        type="realization",
        τ_s=9, τ_a=10,
        participants={"agent": "jocasta"},
        effects=(
            # Jocasta puts the pieces together: the baby her house exposed
            # grew up to be the man she married, who killed Laius.
            realize_add("jocasta", child_of("oedipus", "laius"), 9,
                        note="already knew she bore Laius a son; now knows that son is Oedipus"),
            realize_add("jocasta", child_of("oedipus", "jocasta"), 9),
            realize_add("jocasta", killed("oedipus", "laius"), 9),
            # Her earlier false belief (dead(oedipus)) is dislodged.
            KnowledgeEffect(
                agent_id="jocasta",
                held=Held(prop=dead("oedipus"),
                          slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                          via=Diegetic.REALIZATION.value,
                          provenance=("dislodged at τ_s=9",)),
                remove=True,
            ),
        ),
    ),

    Event(
        id="E_shepherd_testimony",
        type="utterance",
        τ_s=12, τ_a=11,
        participants={"speaker": "shepherd", "listener": "oedipus"},
        effects=(
            # The Shepherd, pressured, confirms: the baby came from Laius's house.
            # This is the final piece Oedipus needs.
            told_by("oedipus", "shepherd", child_of("oedipus", "laius"), 12,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            told_by("oedipus", "shepherd", child_of("oedipus", "jocasta"), 12,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
        ),
    ),

    Event(
        id="E_oedipus_anagnorisis",
        type="realization",
        τ_s=13, τ_a=12,
        participants={"agent": "oedipus"},
        effects=(
            # The canonical anagnorisis. Authored as an explicit realization
            # event (the prototype has no general inference model — realizations
            # of this scope are authored, per sketch 04 open question 2).
            # Old wrong beliefs dislodged:
            KnowledgeEffect(
                agent_id="oedipus",
                held=Held(prop=killed_stranger_at_crossroads("oedipus"),
                          slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                          via=Diegetic.REALIZATION.value, provenance=()),
                remove=True,
            ),
            # Suspected becomes known:
            KnowledgeEffect(
                agent_id="oedipus",
                held=Held(prop=killed("oedipus", "laius"),
                          slot=Slot.SUSPECTED, confidence=Confidence.SUSPECTED,
                          via=Diegetic.REALIZATION.value, provenance=()),
                remove=True,
            ),
            # Gap closed:
            KnowledgeEffect(
                agent_id="oedipus",
                held=Held(prop=gap_real_parents,
                          slot=Slot.GAP, confidence=Confidence.OPEN,
                          via=Diegetic.REALIZATION.value, provenance=()),
                remove=True,
            ),
            # New known truths:
            realize_add("oedipus", killed("oedipus", "laius"), 13,
                        note="the stranger at the crossroads was Laius, my father"),
            realize_add("oedipus", child_of("oedipus", "laius"), 13),
            realize_add("oedipus", child_of("oedipus", "jocasta"), 13,
                        note="my wife is my mother"),
            realize_add("oedipus", married("oedipus", "jocasta"), 13,
                        note="held before, now held as incest"),
        ),
    ),

]


# ----------------------------------------------------------------------------
# Sjuzhet — what the play narrates and in what τ_d order
# ----------------------------------------------------------------------------

# Pre-play disclosures at τ_d=0: the original audience knew the myth.
# We disclose the key pre-play world facts to the reader as KNOWN. The
# reader enters the play with the central irony already loaded.

PREPLAY_DISCLOSURES = (
    Disclosure(prop=child_of("oedipus", "laius"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=child_of("oedipus", "jocasta"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=killed("oedipus", "laius"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=dead("laius"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=married("oedipus", "jocasta"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=king("oedipus", "thebes"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=adopted_by("oedipus", "polybus"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
)


SJUZHET = [

    # τ_d=0 — the reader enters the play with the myth's facts in hand.
    # We attach the pre-play disclosures to the opening event nominally.
    SjuzhetEntry(
        event_id="E_marriage_and_crown",  # any pre-play event anchor works here
        τ_d=0,
        focalizer_id=None,  # omniscient framing
        disclosures=PREPLAY_DISCLOSURES,
    ),

    # τ_d=5 — Jocasta's reassurance, including the crossroads detail.
    SjuzhetEntry(
        event_id="E_jocasta_mentions_crossroads",
        τ_d=5,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=7 — the Corinthian messenger announces Polybus's death.
    SjuzhetEntry(
        event_id="E_messenger_polybus_dead",
        τ_d=7,
        focalizer_id=None,
        disclosures=(
            Disclosure(prop=dead("polybus"), slot=Slot.KNOWN,
                       confidence=Confidence.CERTAIN,
                       via=Narrative.DISCLOSURE.value),
        ),
    ),

    # τ_d=8 — the messenger's adoption reveal.
    SjuzhetEntry(
        event_id="E_messenger_adoption_reveal",
        τ_d=8,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=9 — Jocasta's anagnorisis. She realizes on stage; the audience
    # watches her realize.
    SjuzhetEntry(
        event_id="E_jocasta_realizes",
        τ_d=9,
        focalizer_id="jocasta",  # the scene is focalized through her here
        disclosures=(),
    ),

    # τ_d=12 — the Shepherd's testimony.
    SjuzhetEntry(
        event_id="E_shepherd_testimony",
        τ_d=12,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=13 — Oedipus's anagnorisis.
    SjuzhetEntry(
        event_id="E_oedipus_anagnorisis",
        τ_d=13,
        focalizer_id="oedipus",
        disclosures=(),
    ),

]
