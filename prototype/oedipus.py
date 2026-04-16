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
    Entity, Prop, Event, EventStatus,
    Branch, BranchKind, CANONICAL, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
    Description, AnchorRef, Attention, anchor_event, anchor_desc,
    IDENTITY_PREDICATE,
    Rule,
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

# Added 2026-04-16 per F5 follow-on: Tiresias (the blind seer of
# Apollo who confronts Oedipus in Act 1) and Creon (Jocasta's brother,
# who brings the Delphic oracle's answer at the play's open and takes
# authority at its close). The earlier substrate cut both for the
# identity-probe slice; the dramatica-complete verifier's DA_mc /
# DSP_approach NEEDS_WORK verdicts made the cost of the cut numeric.
tiresias = Entity(id="tiresias", name="Tiresias (the seer)",
                  kind="agent")
creon    = Entity(id="creon",    name="Creon", kind="agent")

ENTITIES = [
    oedipus, jocasta, laius, polybus, merope, messenger, shepherd,
    tiresias, creon,
    the_exposed_baby, the_crossroads_killer, the_crossroads_victim,
    thebes, corinth, crossroads, cithaeron,
]

AGENT_IDS = [e.id for e in ENTITIES if e.kind == "agent"]


# ----------------------------------------------------------------------------
# Branches — canonical-only. The encoding has no contested, draft, or
# counterfactual branches; every fact sits on :canonical.
# ----------------------------------------------------------------------------

ALL_BRANCHES = {
    CANONICAL_LABEL: CANONICAL,
}


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

# Post-anagnorisis predicates (added with the F5 substrate extension
# 2026-04-16). The world's resolution beats: Jocasta's hanging,
# Oedipus's self-blinding, Oedipus's banishment from Thebes.
def blinded(who: str) -> Prop:
    return Prop("blinded", (who,))

def exiled(who: str) -> Prop:
    return Prop("exiled", (who,))

# Currently *authored* as world facts at the canonical moments where the
# composite relation becomes true (parricide at the crossroads killing;
# incest at the marriage). Both are candidate derivations for a future
# inference-model sketch:
#     killed(X, Y)  ∧ child_of(X, Y) ⇒ parricide(X, Y)
#     married(X, Y) ∧ child_of(X, Y) ⇒ incest(X, Y)
# Authoring them explicitly makes the pinch visible: every agent that
# reaches the premises via identity substitution currently also needs
# an explicit observe(…) for the conclusion, because the substrate has
# no forward-chaining surface to derive it.

def parricide(killer: str, victim: str) -> Prop:
    return Prop("parricide", (killer, victim))

def incest(a: str, b: str) -> Prop:
    return Prop("incest", (a, b))

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
            # not die — he gave it to the Corinthian messenger. He does
            # NOT hold identity(oedipus, the-exposed-baby) at this τ_s:
            # Oedipus is not yet named. The shepherd's identity knowledge
            # comes later (if at all); in this encoding, the shepherd
            # never directly holds it — he provides parentage facts, and
            # Oedipus's anagnorisis is what combines them with the
            # messenger's chain to assert the identity.
            observe("shepherd", child_of("the-exposed-baby", "laius"), -99,
                    note="served in Laius's house; knows the baby's parentage"),
            observe("shepherd", child_of("the-exposed-baby", "jocasta"), -99,
                    note="same"),
            # The Corinthian messenger at this τ_s knows he delivered the
            # baby (the-exposed-baby) to Polybus. He does NOT yet hold
            # identity(oedipus, the-exposed-baby) — Oedipus is not named
            # until the upbringing event at τ_s=-50, where the messenger
            # learns the adopted name and forms the identity.
            observe("messenger", adopted_by("the-exposed-baby", "polybus"), -99,
                    note="delivered the child himself; name 'Oedipus' not "
                         "yet assigned at this τ_s"),
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
            # The messenger, at the Corinthian court, witnesses the baby
            # he delivered being named Oedipus and raised by Polybus. This
            # is when he forms identity(oedipus, the-exposed-baby) — not
            # at the exposure event, where Oedipus did not yet exist as a
            # named referent.
            observe("messenger", identity_prop("oedipus", "the-exposed-baby"), -50,
                    note="witnesses the baby grow up at Polybus's court and "
                         "be named Oedipus"),
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
            # parricide(oedipus, laius) is world-true from this τ_s
            # onward but is NOT authored here. Under inference-model-
            # sketch-01 (now implemented in substrate.py), it derives
            # from PARRICIDE_RULE at query time:
            #     killed(X, Y) ∧ child_of(X, Y) ⇒ parricide(X, Y)
            # The premises are both world-true here (killed above,
            # child_of at E_birth); derivation yields parricide at
            # query time without an authored world-effect.
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
            # incest(oedipus, jocasta) is world-true from this τ_s
            # onward but is NOT authored here. Under inference-model-
            # sketch-01, it derives from INCEST_RULE:
            #     married(X, Y) ∧ child_of(X, Y) ⇒ incest(X, Y)
            # Both premises are world-true (married here, child_of at
            # E_birth). Derivation yields incest at query time.
            observe("oedipus", married("oedipus", "jocasta"), -46),
            observe("jocasta", married("oedipus", "jocasta"), -46),
            observe("oedipus", king("oedipus", "thebes"), -46),
            observe("jocasta", king("oedipus", "thebes"), -46),
        ),
    ),

    # --- Play (τ_s ≥ 0) ---

    Event(
        id="E_tiresias_accusation",
        type="utterance",
        τ_s=3, τ_a=6,
        participants={"speaker": "tiresias", "listener": "oedipus"},
        effects=(
            # Tiresias, compelled, names Oedipus as the killer of Laius.
            # The riddling accusation lands in Oedipus's state at SUSPECTED
            # — he rejects it as a Creon-backed plot, but the suspicion is
            # seeded. Sophocles: "I say you are the murderer you hunt."
            # The identity assertion the prophet makes lands via told_by;
            # slot=SUSPECTED preserves the fact that Oedipus does not take
            # it as KNOWN.
            told_by("oedipus", "tiresias",
                    identity_prop("oedipus", "the-crossroads-killer"), 3,
                    slot=Slot.SUSPECTED, confidence=Confidence.BELIEVED),
            # Tiresias is the substrate's first source of the identity;
            # the shepherd's testimony + messenger's chain at τ_s=12 will
            # later promote it to KNOWN at τ_s=13. The world fact
            # identity(oedipus, the-crossroads-killer) was already asserted
            # at E_crossroads_killing; Tiresias's accusation is the first
            # time it enters Oedipus's literal state at any strength.
        ),
    ),

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
            #
            # Nor are parricide(oedipus, laius) and
            # incest(oedipus, jocasta) authored: now that inference-
            # model-sketch-01 is implemented, the rule engine derives
            # them at query time from the premises Jocasta now holds
            # (via substitution: killed(oedipus, laius) and
            # child_of(oedipus, jocasta); married at -46). The earlier
            # author-asserted workaround retired with this pass.
        ),
    ),

    Event(
        id="E_shepherd_testimony",
        type="utterance",
        τ_s=12, τ_a=11,
        participants={"speaker": "shepherd", "listener": "oedipus"},
        effects=(
            # The Shepherd, pressured, confirms: the baby came from Laius's
            # house, and he handed it to the Corinthian messenger. He does
            # NOT assert identity(oedipus, the-exposed-baby) — the shepherd
            # does not hold that identity in his own state, and the
            # combinatorial insight (the messenger's chain ended with this
            # baby becoming Oedipus) is Oedipus's realization, not the
            # shepherd's testimony.
            told_by("oedipus", "shepherd",
                    child_of("the-exposed-baby", "laius"), 12,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            told_by("oedipus", "shepherd",
                    child_of("the-exposed-baby", "jocasta"), 12,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
        ),
    ),

    Event(
        id="E_oedipus_anagnorisis",
        type="realization",
        τ_s=13, τ_a=12,
        participants={"agent": "oedipus"},
        effects=(
            # Oedipus's anagnorisis. This event combines the messenger's
            # prior reveal (the baby went to Polybus, was raised as me)
            # with the shepherd's testimony (the baby came from Laius's
            # house) to assert the central identity. Three identities
            # land at once — this is the combinatorial click:
            #   1. identity(oedipus, the-exposed-baby) — "I was the
            #      exposed child; my mother and father are Jocasta and
            #      Laius."
            #   2. identity(oedipus, the-crossroads-killer) — promoted
            #      from SUSPECTED (at τ_s=5) to KNOWN. by_prop dict
            #      semantics overwrites the SUSPECTED record under the
            #      same Prop key.
            #   3. identity(laius, the-crossroads-victim) — "the stranger
            #      at the crossroads was Laius, my father."
            # Plus one factual dislodgement: the gap_real_parents GAP
            # closes.
            assert_identity("oedipus", "oedipus", "the-exposed-baby", 13,
                            note="the baby the shepherd rescued, brought by "
                                 "the messenger to Polybus, raised as me — "
                                 "I am that child"),
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
            # the three identity assertions above.
            #
            # Nor are parricide(oedipus, laius) and
            # incest(oedipus, jocasta) authored. With inference-model-
            # sketch-01 implemented, PARRICIDE_RULE and INCEST_RULE
            # (see RULES export at the bottom of this module) derive
            # them at query time from Oedipus's post-anagnorisis held
            # set under identity substitution.
        ),
    ),

    # --- Post-anagnorisis (τ_s > 13) — the play's resolution beats.
    # Added 2026-04-16 as part of the F5 substrate extension. The
    # earlier encoding cut Jocasta's suicide, Oedipus's self-blinding,
    # and the exile; the dramatica-complete verifier's 0.20 NEEDS_WORK
    # verdicts for DA_mc / DSP_approach were the forcing function.

    Event(
        id="E_jocasta_suicide",
        type="death",
        τ_s=14, τ_a=13,
        participants={"agent": "jocasta", "location": "thebes"},
        effects=(
            world(dead("jocasta")),
            # Oedipus learns of her death when he finds her body (see
            # E_self_blinding at τ_s=15, where the discovery is folded
            # into his motivation for the blinding). No agent-side
            # held-record here: the death is the world fact; downstream
            # events thread the knowledge.
        ),
    ),

    Event(
        id="E_self_blinding",
        type="blinding",
        τ_s=15, τ_a=14,
        participants={"agent": "oedipus", "location": "thebes"},
        effects=(
            # Oedipus, finding Jocasta hanged, takes the brooches from
            # her robe and blinds himself. The world fact blinded(oedipus)
            # holds from this τ_s on; Oedipus's knowledge of his own
            # blinding is authored explicitly.
            world(blinded("oedipus")),
            observe("oedipus", blinded("oedipus"), 15,
                    note="self-inflicted with Jocasta's brooches"),
            # Oedipus also registers Jocasta's death as KNOWN here,
            # since finding her body is how he comes to know.
            observe("oedipus", dead("jocasta"), 15,
                    note="found hanged"),
        ),
    ),

    Event(
        id="E_exile",
        type="exile",
        τ_s=17, τ_a=15,
        participants={"agent": "creon", "subject": "oedipus",
                      "location": "thebes"},
        effects=(
            # Creon, now regent, enacts Oedipus's banishment — or rather,
            # Oedipus asks for it and Creon grants it. The world fact
            # exiled(oedipus) holds from this τ_s on; Oedipus's and
            # Creon's literal states register it.
            world(exiled("oedipus")),
            observe("oedipus", exiled("oedipus"), 17),
            observe("creon", exiled("oedipus"), 17),
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
    # Compound-conclusion disclosures (parricide, incest) are NOT
    # authored here. The reader still holds them from τ_d=0, but
    # under inference-model-sketch-01 they derive at query time from
    # the premises the reader does hold (child_of + killed + married)
    # plus the RULES below. The reader-outruns-character shape stands:
    # the audience has the compound conclusions from τ_d=0 via
    # derivation, not via authored disclosure.
)


SJUZHET = [

    # τ_d=0 — the reader enters the play with the myth's facts in hand.
    SjuzhetEntry(
        event_id="E_marriage_and_crown",  # any pre-play event anchor works here
        τ_d=0,
        focalizer_id=None,  # omniscient framing
        disclosures=PREPLAY_DISCLOSURES,
    ),

    # τ_d=3 — Tiresias's accusation. The first onstage confrontation;
    # the prophet names Oedipus as the killer. The play discloses the
    # identity at SUSPECTED strength for Oedipus (he rejects it); the
    # audience hears it as a loaded-hint from the prophet.
    SjuzhetEntry(
        event_id="E_tiresias_accusation",
        τ_d=3,
        focalizer_id=None,
        disclosures=(),
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

    # τ_d=14 — Messenger reports Jocasta's suicide. The play narrates
    # this offstage via the messenger's speech; the disclosure lands
    # in the reader's state at KNOWN strength.
    SjuzhetEntry(
        event_id="E_jocasta_suicide",
        τ_d=14,
        focalizer_id=None,
        disclosures=(
            Disclosure(prop=dead("jocasta"), slot=Slot.KNOWN,
                       confidence=Confidence.CERTAIN,
                       via=Narrative.DISCLOSURE.value),
        ),
    ),

    # τ_d=15 — Oedipus reappears onstage, blinded. The messenger has
    # already narrated the act; the onstage reveal makes it present.
    SjuzhetEntry(
        event_id="E_self_blinding",
        τ_d=15,
        focalizer_id=None,
        disclosures=(
            Disclosure(prop=blinded("oedipus"), slot=Slot.KNOWN,
                       confidence=Confidence.CERTAIN,
                       via=Narrative.DISCLOSURE.value),
        ),
    ),

    # τ_d=17 — Creon enacts the exile. The play's closing beat: Oedipus
    # asks to be cast out; Creon grants it.
    SjuzhetEntry(
        event_id="E_exile",
        τ_d=17,
        focalizer_id=None,
        disclosures=(
            Disclosure(prop=exiled("oedipus"), slot=Slot.KNOWN,
                       confidence=Confidence.CERTAIN,
                       via=Narrative.DISCLOSURE.value),
        ),
    ),

]


# ----------------------------------------------------------------------------
# Descriptions — the interpretive peer surface over the fabula.
# ----------------------------------------------------------------------------
#
# Minimal set aimed at exercising the "author-asserted vs. derived"
# pinch. The anagnorisis texture reads the realization scene as the
# play's emotional crest; the logical-payload reader-frame names the
# substrate-level shape (compound conclusions become epistemically
# reachable); the authorial-uncertainty question asks the probe
# whether parricide/incest belong as world facts or as derivations.
#
# τ_a values are placed after the last fabula τ_a (12) with gaps, so
# later passes can interleave without renumbering.
#
# Attention levels follow descriptions-sketch-01 defaults:
#   texture              → interpretive
#   reader-frame         → structural
#   authorial-uncertainty → structural

DESCRIPTIONS = [

    Description(
        id="D_oedipus_anagnorisis_texture",
        attached_to=anchor_event("E_oedipus_anagnorisis"),
        kind="texture",
        attention=Attention.INTERPRETIVE,
        text=("the realization does not import new facts from outside — "
              "every premise was already on stage. The shepherd's "
              "testimony collides with the messenger's chain, and the "
              "three identities click at once: I was the exposed child; "
              "I killed my father at the crossroads; I am married to my "
              "mother. The scene's horror is that the facts were all in "
              "his head already, waiting for the composition."),
        authored_by="author",
        τ_a=100,
    ),

    Description(
        id="D_anagnorisis_logical_payload",
        attached_to=anchor_event("E_oedipus_anagnorisis"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("the anagnorisis's logical payload is two compound "
              "conclusions — parricide(oedipus, laius) and "
              "incest(oedipus, jocasta) — that both derive from "
              "premises Oedipus already held plus the identities he "
              "asserts in this scene. They enter his state here; they "
              "were world-true from the crossroads killing and the "
              "marriage respectively. This is the reader-outruns-"
              "character gap closing: the reader has held both since "
              "τ_d=0."),
        authored_by="author",
        τ_a=101,
    ),

    Description(
        id="D_parricide_incest_authored_not_derived",
        attached_to=anchor_desc("D_anagnorisis_logical_payload"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("parricide(oedipus, laius) and incest(oedipus, jocasta) "
              "were originally authored as world facts at the "
              "canonical moments (crossroads killing, marriage) and "
              "observed into both agents' states at their realizations. "
              "They are the conclusions of domain rules the substrate "
              "could not yet express: killed(X,Y) ∧ child_of(X,Y) ⇒ "
              "parricide(X,Y), married(X,Y) ∧ child_of(X,Y) ⇒ "
              "incest(X,Y). "
              "RESOLVED (2026-04-14): the inference engine per "
              "inference-model-sketch-01 is now implemented in the "
              "substrate. Both predicates derive at query time via "
              "PARRICIDE_RULE and INCEST_RULE (see RULES export at "
              "end of this module). The authored assertions at "
              "E_crossroads_killing, E_marriage_and_crown, and both "
              "anagnoreses, and the compound disclosures at τ_d=0, "
              "all retired. Kept as a description because the answer "
              "record (the accepted LLM proposal below) remains "
              "load-bearing context for the boundary criterion."),
        is_question=True,
        authored_by="author",
        τ_a=102,
    ),

    # Probe-authored answer, accepted via the walker at τ_a=20000.
    # Provenance: reader-model probe, Claude Opus 4.6, effort=high.
    # The answer proposes a boundary criterion (definitional over
    # world-props, no authorial judgment required) intended to seed
    # the inference-model sketch. It does not retire the question
    # record — the question stays as the trigger for the sketch work.
    Description(
        id="D_parricide_incest_authored_not_derived_answer_by_llm_claude-opus-4-6_τ_a_20000",
        attached_to=anchor_desc("D_anagnorisis_logical_payload"),
        kind="reader-frame",
        attention=Attention.INTERPRETIVE,
        text=("The case for derivation is strongest when the compound "
              "predicate is purely definitional — when the rule is "
              "domain-invariant and its premises are already tracked "
              "as world-props. Both rules identified here "
              "(killed ∧ child_of ⇒ parricide; married ∧ child_of ⇒ "
              "incest) meet that criterion: the substrate already "
              "carries killed(oedipus, laius), child_of(oedipus, laius), "
              "married(oedipus, jocasta), and child_of(oedipus, jocasta) "
              "as world effects. A forward-chaining surface could "
              "derive parricide and incest the instant both premises "
              "obtain, without authorial intervention. The practical "
              "boundary should be: derive a compound predicate when "
              "(a) its rule can be stated in terms the substrate "
              "already tracks as world-props, and (b) the compound's "
              "truth-value is fully determined by those props with no "
              "authorial judgment required. Predicates that require "
              "contextual or tonal judgment — say, 'hubris' or "
              "'tragic irony' — cannot be captured by such rules and "
              "remain description-layer concerns. Under this boundary, "
              "author-assertion of parricide and incest becomes "
              "redundant once the rules exist, but the substrate need "
              "not attempt to derive open-textured moral or dramatic "
              "categories."),
        authored_by="llm:claude-opus-4-6",
        τ_a=20_000,
        metadata={
            "answers_question": "D_parricide_incest_authored_not_derived",
        },
    ),

    # Banked from the probe walk at τ_a=20000: the probe proposed an
    # edit replacing "τ_d=0" with τ_a-authorship coordinates (τ_a=5 /
    # τ_a=6). The edit was declined — the original claim is about the
    # audience's disclosure schedule (τ_d), which the ReaderView does
    # not expose; but narrowing to τ_a loses the reader-outruns-
    # character point. This question banks the surface tension for a
    # later sketch pass.
    Description(
        id="D_view_cannot_see_τ_d",
        attached_to=anchor_desc("D_anagnorisis_logical_payload"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("D_anagnorisis_logical_payload claims 'the reader has "
              "held both since τ_d=0', but ReaderView does not expose "
              "τ_d — the sjuzhet coordinate lives outside the view. "
              "A reader-model probe correctly flagged this and "
              "proposed an edit to τ_a coordinates; the edit was "
              "declined because τ_a names authorship, not disclosure "
              "schedule. The two are not the same. Open question for "
              "a future pass: should ReaderView gain sjuzhet "
              "visibility, or should descriptions stay inside what "
              "the view can see? This sits below the inference-model "
              "sketch on the dependency order."),
        is_question=True,
        authored_by="author",
        τ_a=20_001,
    ),

]


# ----------------------------------------------------------------------------
# Rules — inference-model-sketch-01 N1–N10
# ----------------------------------------------------------------------------
#
# The two compound predicates parricide and incest are no longer
# author-asserted at their canonical events (see E_crossroads_killing,
# E_marriage_and_crown, E_jocasta_realizes, E_oedipus_anagnorisis for
# the retirement comments). They derive via these rules at query time.
#
# Premises for both rules come from events already authored:
#     - child_of(X, Y) — authored at E_birth (multiple forms, plus
#       identity propositions that expand via substitution)
#     - killed(X, Y)   — authored at E_crossroads_killing
#     - married(X, Y)  — authored at E_marriage_and_crown
#
# Rules compose with identity substitution (N4). Both rules have depth
# 1 from the premises, so a depth_cap of 1 suffices for this encoding.

PARRICIDE_RULE = Rule(
    id="R_parricide_from_killed_and_parent",
    head=Prop("parricide", ("X", "Y")),
    body=(
        Prop("killed",   ("X", "Y")),
        Prop("child_of", ("X", "Y")),
    ),
)

INCEST_RULE = Rule(
    id="R_incest_from_married_and_parent",
    head=Prop("incest", ("X", "Y")),
    body=(
        Prop("married",  ("X", "Y")),
        Prop("child_of", ("X", "Y")),
    ),
)

RULES = (PARRICIDE_RULE, INCEST_RULE)
