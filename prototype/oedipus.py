"""
Oedipus Rex — the encoded fabula and sjuzhet slice.

Story content only. No substrate logic. This file defines entities, events,
sjuzhet entries, and the predicates used in propositions, sufficient to
exercise the substrate on the Messenger + Shepherd → anagnorisis slice.

Under identity-and-realization-sketch-01, this encoding has been refactored:

- Realizations no longer rewrite derived truths via `realize_add` /
  `realize_remove` cascades. A realization asserts one or more
  `identity(A, B)` propositions into the realizing agent's state;
  query-time substitution produces the derived beliefs. The literal
  held set is not rewritten by the realization itself.

- Named entities stand in for "the person referred to as X from some
  agent's perspective, but not yet known to be the same as Y." Three
  such entities in this encoding:
    - `the-exposed-baby` — the infant Laius and Jocasta exposed on
      Mount Cithaeron. Canonically identical to Oedipus, but Jocasta
      does not hold that identity until her anagnorisis.
    - `the-crossroads-killer` — the unknown killer at the crossroads,
      from the perspective of Jocasta (and later Oedipus himself, as a
      suspicion). Canonically identical to Oedipus.
    - `the-crossroads-victim` — the unknown victim Oedipus killed at
      the crossroads, from his own perspective. Canonically identical
      to Laius. Oedipus does not hold that identity until his
      anagnorisis.

- The composite arity-1 predicate `killed_stranger_at_crossroads(oedipus)`
  is retired. In its place: `killed(oedipus, the-crossroads-victim)`.
  This is the ergonomic shift substrate-sketch-05 flagged — named
  entities plus identity substitution replace composite predicates as
  workarounds for existential gaps.

- Factual dislodgements (the messenger's reveal dislodging Oedipus's
  BELIEVED `child_of(oedipus, polybus)`, Jocasta's realization
  dislodging her BELIEVED `dead(the-exposed-baby)`, the anagnorisis
  closing Oedipus's GAP for his parentage) stay as `remove=True`
  knowledge effects. Those are legitimate factual updates triggered
  by specific evidence — distinct from the realization-driven rewrite
  pattern the sketch retires.

Fidelity choices (unchanged from prior iteration):

- Pre-play fabula (Laius's prophecy, infant exposure, Oedipus's
  Corinthian upbringing, the crossroads killing, the marriage) is
  represented as canonical events at negative τ_s. These are never
  *narrated* in the play — Sophocles opens in medias res. For the
  prototype, we disclose the key pre-play facts to the reader at
  τ_d = 0 on the premise that the original audience knew the myth.
  The disclosures include the identity propositions — the reader
  holds `identity(oedipus, the-exposed-baby)` and
  `identity(laius, the-crossroads-victim)` KNOWN from the opening,
  which is the substitution machinery that makes the whole play an
  exercise in dramatic irony.

- In-play events are a selected slice, not the full play. Minimum
  required to exercise the substrate's irony, reveal, and realization
  machinery: Jocasta's mention of the crossroads, the Messenger's
  two-step disclosure, Jocasta's own anagnorisis, the Shepherd's
  testimony, and Oedipus's anagnorisis.

- Tiresias, Creon, and the chorus are cut.
"""

from __future__ import annotations

from substrate import (
    Entity, Prop, Event, EventStatus, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
    IDENTITY_PREDICATE,
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

# Identity-placeholder entities. Canonically identical to named characters,
# but distinct references in the agent states that have not yet realized the
# identity. Substitution is what wires them together at query time once the
# realizing agent holds the `identity(…)` proposition at KNOWN.
the_exposed_baby       = Entity(id="the-exposed-baby",
                                name="the infant exposed on Cithaeron",
                                kind="abstract")
the_crossroads_killer  = Entity(id="the-crossroads-killer",
                                name="the stranger who killed Laius at the crossroads",
                                kind="abstract")
the_crossroads_victim  = Entity(id="the-crossroads-victim",
                                name="the stranger Oedipus killed at the crossroads",
                                kind="abstract")

thebes     = Entity(id="thebes",     name="Thebes",     kind="location")
corinth    = Entity(id="corinth",    name="Corinth",    kind="location")
crossroads = Entity(id="crossroads", name="the Crossroads", kind="location")
cithaeron  = Entity(id="cithaeron",  name="Mount Cithaeron", kind="location")

ENTITIES = [
    oedipus, jocasta, laius, polybus, merope, messenger, shepherd,
    the_exposed_baby, the_crossroads_killer, the_crossroads_victim,
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

def adopted_by(child: str, parent: str) -> Prop:
    return Prop("adopted_by", (child, parent))

def prophecy_self() -> Prop:
    # Oedipus's personal prophecy: he will kill his father and marry his mother.
    return Prop("prophecy_will_kill_father_and_marry_mother", ("oedipus",))

def identity_prop(a: str, b: str) -> Prop:
    """Construct an identity proposition. Thin wrapper over Prop so story
    code does not inline the reserved predicate name."""
    return Prop(IDENTITY_PREDICATE, (a, b))

# A GAP placeholder: Oedipus wonders who his real parents are.
# The gap is a proposition held in the GAP slot on Oedipus's state. The
# anagnorisis closes the gap via an explicit remove=True effect (a
# factual update, distinct from realization-driven substitution).
gap_real_parents = Prop("real_parents_identified", ("oedipus",))


# ----------------------------------------------------------------------------
# Event helpers
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
            slot: Slot = Slot.BELIEVED) -> KnowledgeEffect:
    return KnowledgeEffect(
        agent_id=listener_id,
        held=Held(
            prop=p, slot=slot, confidence=confidence,
            via=Diegetic.UTTERANCE_HEARD.value,
            provenance=(f"told by {speaker_id} @ τ_s={τ}",),
        ),
    )

def assert_identity(agent_id: str, a: str, b: str, τ: int,
                    note: str = "",
                    via: str = None) -> KnowledgeEffect:
    """Place an identity proposition into an agent's state at slot=KNOWN.
    This is the realization pattern under identity-and-realization-sketch-01:
    the realization event's payload is an identity assertion. Substitution
    produces the derived beliefs at query time.
    """
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(
            prop=identity_prop(a, b),
            slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
            via=via or Diegetic.REALIZATION.value,
            provenance=(f"identity asserted @ τ_s={τ}"
                        f"{(': ' + note) if note else ''}",),
        ),
    )

def remove_held(agent_id: str, p: Prop, slot: Slot,
                confidence: Confidence, τ: int,
                via: str = None,
                note: str = "") -> KnowledgeEffect:
    """Factual dislodgement — remove a specific Held record that has been
    superseded by evidence. Distinct from realization-driven rewriting
    (which identity-and-realization-sketch-01 retires); this pattern is
    still legitimate for *specific* literal beliefs the story has
    authored evidence against."""
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(prop=p, slot=slot, confidence=confidence,
                  via=via or Diegetic.INFERENCE.value,
                  provenance=(f"dislodged @ τ_s={τ}"
                              f"{(': ' + note) if note else ''}",)),
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
            # World facts: canonical biological truths PLUS the world-level
            # identity that makes oedipus and the-exposed-baby co-referential.
            world(child_of("oedipus", "laius")),
            world(child_of("oedipus", "jocasta")),
            world(identity_prop("oedipus", "the-exposed-baby")),
            # Laius and Jocasta witness the birth of *their baby* — whom
            # they refer to as the-exposed-baby in their states until (and
            # if) they realize the identity. They do NOT hold
            # child_of(oedipus, …) literally at this τ_s.
            observe("laius",   child_of("the-exposed-baby", "laius"),   -100,
                    note="witnessed birth"),
            observe("laius",   child_of("the-exposed-baby", "jocasta"), -100,
                    note="witnessed birth"),
            observe("jocasta", child_of("the-exposed-baby", "laius"),   -100,
                    note="witnessed birth"),
            observe("jocasta", child_of("the-exposed-baby", "jocasta"), -100,
                    note="witnessed birth"),
        ),
    ),

    Event(
        id="E_exposure_and_rescue",
        type="exposure",
        τ_s=-99, τ_a=2,
        participants={"infant": "the-exposed-baby",
                      "rescuer": "shepherd", "courier": "messenger"},
        effects=(
            # Jocasta and Laius believe the infant (the-exposed-baby) died
            # on Cithaeron. The belief is authored as BELIEVED — it is in
            # fact false, but they hold it sincerely.
            observe("jocasta", dead("the-exposed-baby"), -99,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="thinks exposure succeeded"),
            observe("laius",   dead("the-exposed-baby"), -99,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="thinks exposure succeeded"),
            # The shepherd knows the baby came from Laius's house and did
            # not die — he gave it to the Corinthian messenger. He also
            # knows (through the later chain: messenger → Polybus raises
            # as Oedipus) the identity, and he can name it under pressure.
            observe("shepherd", child_of("the-exposed-baby", "laius"), -99,
                    note="served in Laius's house; knows the baby's parentage"),
            observe("shepherd", child_of("the-exposed-baby", "jocasta"), -99,
                    note="same"),
            observe("shepherd", identity_prop("oedipus", "the-exposed-baby"), -99,
                    note="knows the chain: Laius's house → Cithaeron → "
                         "messenger → Polybus's household as Oedipus"),
            # The Corinthian messenger knows he received the baby from the
            # Theban shepherd and delivered him to Polybus, where the
            # child was raised as Oedipus. He holds the identity.
            observe("messenger", adopted_by("oedipus", "polybus"), -99,
                    note="delivered the child himself"),
            observe("messenger", identity_prop("oedipus", "the-exposed-baby"), -99,
                    note="direct knowledge from delivering the child"),
        ),
    ),

    Event(
        id="E_upbringing_in_corinth",
        type="upbringing",
        τ_s=-50, τ_a=3,
        participants={"child": "oedipus", "father": "polybus", "mother": "merope"},
        effects=(
            # Oedipus grows up believing Polybus and Merope are his parents.
            observe("oedipus", child_of("oedipus", "polybus"), -50,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="raised as their son"),
            observe("oedipus", child_of("oedipus", "merope"), -50,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="raised as their son"),
        ),
    ),

    Event(
        id="E_oracle_to_oedipus",
        type="prophecy_received",
        τ_s=-49, τ_a=4,
        participants={"recipient": "oedipus"},
        effects=(
            observe("oedipus", prophecy_self(), -49,
                    note="hears the oracle at Delphi"),
        ),
    ),

    Event(
        id="E_crossroads_killing",
        type="killing",
        τ_s=-48, τ_a=5,
        participants={"killer": "oedipus", "victim": "laius"},
        effects=(
            # World facts: canonical truth about who did what, plus the
            # world-level identity that makes laius and the-crossroads-
            # victim co-referential.
            world(killed("oedipus", "laius")),
            world(dead("laius")),
            world(identity_prop("laius", "the-crossroads-victim")),
            world(identity_prop("oedipus", "the-crossroads-killer")),
            # Oedipus knows he killed *someone* at the crossroads. The
            # victim's identity is not yet in his state — he held
            # killed(oedipus, the-crossroads-victim), not
            # killed(oedipus, laius).
            observe("oedipus", killed("oedipus", "the-crossroads-victim"), -48,
                    note="a travel-quarrel, unidentified victim"),
            # Jocasta learns (off-stage, via survivor/messenger) that Laius
            # was killed by a stranger at the crossroads. She does not
            # know the stranger's identity — literal record:
            # killed(the-crossroads-killer, laius).
            observe("jocasta", killed("the-crossroads-killer", "laius"), -47,
                    via=Diegetic.UTTERANCE_HEARD.value,
                    note="reported to her; killer's identity unknown"),
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
            # Jocasta tells Oedipus what she knows: Laius was killed by
            # a stranger at the crossroads. This is the literal fact she
            # holds; Oedipus gains it under the same name.
            told_by("oedipus", "jocasta",
                    killed("the-crossroads-killer", "laius"), 5,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            # Oedipus now suspects he might be the crossroads-killer. Under
            # the identity-and-realization model, the suspicion lives at
            # the identity level (per I7, SUSPECTED identity does not fire
            # substitution — this is precisely the "partial realization"
            # state). When the identity later promotes to KNOWN at the
            # anagnorisis, substitution yields killed(oedipus, laius).
            KnowledgeEffect(
                agent_id="oedipus",
                held=Held(
                    prop=identity_prop("oedipus", "the-crossroads-killer"),
                    slot=Slot.SUSPECTED,
                    confidence=Confidence.SUSPECTED,
                    via=Diegetic.INFERENCE.value,
                    provenance=("suspected after Jocasta mentions the "
                                "crossroads @ τ_s=5",),
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
            # The messenger, trying to reassure Oedipus that the prophecy-
            # about-Polybus cannot apply, lets slip that he himself brought
            # the baby Oedipus to Polybus.
            told_by("oedipus", "messenger", adopted_by("oedipus", "polybus"), 8,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            told_by("jocasta", "messenger", adopted_by("oedipus", "polybus"), 8,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            # Oedipus's prior BELIEVED beliefs about his parentage are
            # dislodged — this is a factual update (the messenger gave
            # direct evidence that Polybus is not his biological parent),
            # not a realization-driven rewrite.
            remove_held("oedipus", child_of("oedipus", "polybus"),
                        Slot.BELIEVED, Confidence.BELIEVED, 8,
                        note="dislodged by adoption revelation"),
            remove_held("oedipus", child_of("oedipus", "merope"),
                        Slot.BELIEVED, Confidence.BELIEVED, 8,
                        note="dislodged by adoption revelation"),
            # Oedipus now has a GAP about his real parents. The gap is an
            # authorial marker of an acknowledged open question —
            # substitution does not auto-close acknowledged gaps per the
            # sketch's Sternberg-stays-literal commitment.
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
            # Jocasta's anagnorisis. She combines the messenger's adoption
            # reveal with her own memory of exposing her child on
            # Cithaeron and realizes:
            #   1. The exposed baby did not die — he was brought to
            #      Polybus and raised as Oedipus.
            #   2. Oedipus, whom she married, IS her exposed child.
            # Under identity-and-realization, the realization payload is
            # two identity assertions plus one factual dislodgement
            # (the prior false belief that the baby died).
            assert_identity("jocasta", "oedipus", "the-exposed-baby", 9,
                            note="the exposed baby grew up to be Oedipus"),
            assert_identity("jocasta", "oedipus", "the-crossroads-killer", 9,
                            note="Oedipus is the stranger who killed Laius"),
            # Her earlier false belief that the exposed baby died is
            # dislodged — the exposure did not succeed.
            remove_held("jocasta", dead("the-exposed-baby"),
                        Slot.BELIEVED, Confidence.BELIEVED, 9,
                        via=Diegetic.REALIZATION.value,
                        note="the exposure did not succeed after all"),
            # Note what is NOT authored here: no realize_add of
            # child_of(oedipus, jocasta), killed(oedipus, laius), etc.
            # Those derive at query time from Jocasta's literal held set
            # plus the two identity assertions above. This is the
            # identity-and-realization-sketch-01 refactor in practice.
        ),
    ),

    Event(
        id="E_shepherd_testimony",
        type="utterance",
        τ_s=12, τ_a=11,
        participants={"speaker": "shepherd", "listener": "oedipus"},
        effects=(
            # The Shepherd, pressured, confirms: the baby came from Laius's
            # house, and he handed it to the Corinthian messenger. The
            # shepherd names the identity directly — he has held it since
            # the exposure (he rescued the baby; the messenger brought it
            # to Polybus; Oedipus is that child).
            told_by("oedipus", "shepherd",
                    child_of("the-exposed-baby", "laius"), 12,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            told_by("oedipus", "shepherd",
                    child_of("the-exposed-baby", "jocasta"), 12,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            told_by("oedipus", "shepherd",
                    identity_prop("oedipus", "the-exposed-baby"), 12,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
        ),
    ),

    Event(
        id="E_oedipus_anagnorisis",
        type="realization",
        τ_s=13, τ_a=12,
        participants={"agent": "oedipus"},
        effects=(
            # Oedipus's anagnorisis. The shepherd's testimony already
            # supplied identity(oedipus, the-exposed-baby) KNOWN. What
            # this event adds:
            #   1. Promote identity(oedipus, the-crossroads-killer) from
            #      SUSPECTED to KNOWN — he now fully owns the identity
            #      with the crossroads-killer (himself).
            #   2. Assert identity(laius, the-crossroads-victim) KNOWN —
            #      he realizes the stranger he killed was Laius, his
            #      father.
            #   3. Close the GAP on his real parents (an acknowledged
            #      open question is now resolved; remove the GAP record).
            assert_identity("oedipus", "oedipus", "the-crossroads-killer", 13,
                            note="promotes prior SUSPECTED to KNOWN; by_prop "
                                 "dict overwrites the SUSPECTED entry"),
            assert_identity("oedipus", "laius", "the-crossroads-victim", 13,
                            note="the stranger at the crossroads was Laius"),
            remove_held("oedipus", gap_real_parents,
                        Slot.GAP, Confidence.OPEN, 13,
                        via=Diegetic.REALIZATION.value,
                        note="gap closed — parentage now known via identity"),
            # Note what is NOT authored here: no realize_add of
            # killed(oedipus, laius), child_of(oedipus, laius),
            # child_of(oedipus, jocasta), married(oedipus, jocasta). All
            # derive at query time from Oedipus's literal held set plus
            # the identity assertions.
        ),
    ),

]


# ----------------------------------------------------------------------------
# Sjuzhet — what the play narrates and in what τ_d order
# ----------------------------------------------------------------------------

# Pre-play disclosures at τ_d=0: the original audience knew the myth.
# The reader enters the play with the central irony loaded — including
# the identity propositions that make substitution fire on the reader's
# state from τ_d=0. This is the substitution-driven reader-outruns-
# character pattern identity-and-realization-sketch-01 names.

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
    # Identity disclosures — the reader knows the myth, so the reader
    # holds the identities that Jocasta and Oedipus will realize later.
    # These power substitution-driven irony from τ_d=0.
    Disclosure(prop=identity_prop("oedipus", "the-exposed-baby"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=identity_prop("laius", "the-crossroads-victim"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=identity_prop("oedipus", "the-crossroads-killer"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
)


SJUZHET = [

    # τ_d=0 — the reader enters the play with the myth's facts in hand.
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
