"""
Macbeth — the encoded fabula and sjuzhet.

Story content only. No substrate logic. This file parallels oedipus.py
in shape and pressure-tests the substrate on a structurally different
story: action-first rather than epistemic-investigation, cumulative
moral trajectory rather than single-moment anagnorisis, multiple
killings (Duncan, Banquo, Lady Macduff and her family, Lady Macbeth's
suicide, Macbeth's death at Macduff's hands), supernatural Throughline
participants (the Witches) whose ontology the encoding leaves
deliberately unsettled.

Serves the design work in:

- lowering-sketch-02 — which sketched both upper and lower encodings
  in prose for the four-coupling-kinds exercise. This file is the
  concrete substrate side that sketch anticipated; it gives any
  future end-to-end lowering a real set of records to bind against.
- inference-model-sketch-01 — authored compound predicates
  (kinslayer, regicide, breach_of_hospitality, tyrant) are candidate
  derivations for the rule engine once it lands. Same pattern as
  oedipus.py's parricide / incest authored-today-derived-later.

Encoding choices (explicit, so future readers understand the slice):

- Branches: canonical only. Macbeth has no Rashomon-style contested
  testimony and no counterfactual branches.

- Identity placeholders: none. Unlike Oedipus (which turned on
  identity realizations), Macbeth never confuses who is who. The
  Witches' apparitions in the second-prophecy scene are symbolic
  (a head, a bloody child, a crowned child) but are not identity
  puzzles in the substrate sense.

- Audience-pre-knowledge disclosures: light. Shakespeare's audience
  knew some chronicle facts (Scotland's thaneships, Duncan's
  kingship, Macbeth's existence as a historical figure), but
  nothing comparable to the Oedipus myth's front-loaded irony.
  The encoding includes a small PREPLAY_DISCLOSURES set covering
  the facts the opening scenes take for granted (Duncan is king,
  Macbeth is thane of Glamis, Scotland is at war) but does not
  disclose outcomes.

- Focalization: largely Macbeth. The sleepwalking scene focalizes
  through Lady Macbeth; the Macduff-family scene through the victims;
  the battle scenes are unfocalized (omniscient).

- Authored compound predicates: kinslayer(X, Y), regicide(X, Y),
  breach_of_hospitality(X, Y), tyrant(X). These are candidate
  derivations for the inference engine per inference-model-sketch-01:
      killed(X, Y) ∧ kinsman_of(X, Y) ⇒ kinslayer(X, Y)
      killed(X, Y) ∧ king(Y, _)        ⇒ regicide(X, Y)
      killed(X, Y) ∧ guest_of(Y, X)    ⇒ breach_of_hospitality(X, Y)
      kinslayer(X, _) ∧ regicide(X, _) ∧ king(X, _) ⇒ tyrant(X)
  Until the rule engine lands, these are author-asserted as world
  facts at the events that make them true, with comments pointing
  at the forcing-function structure. Same pattern as oedipus.py's
  parricide / incest.

- Supernatural ontology: deliberately unsettled. The Witches are an
  Entity of kind "agent" (a concession so observe / told_by helpers
  work on them); their encoding makes no claim about whether their
  prophecies are true foresight, causal manipulation, or the
  projection of Macbeth's own ambition. Banquo's ghost is encoded
  as an observation on Macbeth's held set only (no world-effect
  asserting the ghost exists at the feast). The substrate records
  what characters observe; descriptions handle the authorial
  reticence about what is.

- Scope of the play encoded: essentially all of it, at the event
  level. Detailed dialogue and secondary beats (Porter scene, the
  English exile discussion, the witches' apparitions in detail)
  are compressed into their structural outcomes. ~20 fabula events;
  ~20 sjuzhet entries (Macbeth is largely told in fabula order).
"""

from __future__ import annotations

from substrate import (
    Entity, Prop, Event, EventStatus,
    Branch, BranchKind, CANONICAL, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
    Description, AnchorRef, Attention, DescStatus,
    anchor_event, anchor_desc,
    Rule,
)


# ----------------------------------------------------------------------------
# Entities
# ----------------------------------------------------------------------------

macbeth       = Entity(id="macbeth",       name="Macbeth",        kind="agent")
lady_macbeth  = Entity(id="lady_macbeth",  name="Lady Macbeth",   kind="agent")
duncan        = Entity(id="duncan",        name="Duncan",         kind="agent")
malcolm       = Entity(id="malcolm",       name="Malcolm",        kind="agent")
donalbain     = Entity(id="donalbain",     name="Donalbain",      kind="agent")
banquo        = Entity(id="banquo",        name="Banquo",         kind="agent")
fleance       = Entity(id="fleance",       name="Fleance",        kind="agent")
macduff       = Entity(id="macduff",       name="Macduff",        kind="agent")
lady_macduff  = Entity(id="lady_macduff",  name="Lady Macduff",   kind="agent")
macduff_son   = Entity(id="macduff_son",   name="Macduff's son",  kind="agent")
ross          = Entity(id="ross",          name="Ross",           kind="agent")
murderers     = Entity(id="murderers",     name="the Murderers",  kind="agent")
# The Witches — treated as a single collective agent to keep observe/
# told_by helpers clean. The substrate has no "collective" kind; "agent"
# is the least-bad choice. The supernatural aspect is documented on
# descriptions, not on the entity type.
witches       = Entity(id="witches",       name="the Weird Sisters", kind="agent")

scotland      = Entity(id="scotland",      name="Scotland",        kind="location")
england       = Entity(id="england",       name="England",         kind="location")
inverness     = Entity(id="inverness",     name="Inverness (Macbeth's castle)", kind="location")
dunsinane     = Entity(id="dunsinane",     name="Dunsinane",       kind="location")
fife          = Entity(id="fife",          name="Fife (Macduff's seat)", kind="location")
the_heath     = Entity(id="the_heath",     name="the heath",       kind="location")
birnam_wood   = Entity(id="birnam_wood",   name="Birnam Wood",     kind="location")

ENTITIES = [
    macbeth, lady_macbeth, duncan, malcolm, donalbain,
    banquo, fleance, macduff, lady_macduff, macduff_son,
    ross, murderers, witches,
    scotland, england, inverness, dunsinane, fife, the_heath, birnam_wood,
]

AGENT_IDS = [e.id for e in ENTITIES if e.kind == "agent"]


# ----------------------------------------------------------------------------
# Branches — canonical only.
# ----------------------------------------------------------------------------

ALL_BRANCHES = {
    CANONICAL_LABEL: CANONICAL,
}


# ----------------------------------------------------------------------------
# Proposition constructors
# ----------------------------------------------------------------------------
#
# The core predicate set. Following substrate-sketch-05 M1, these
# predicates are structural — they admit typed queries. Anything
# tonal or modal (how brave was the battle, how guilt-wracked was
# the conspirator) lives on descriptions.

def killed(killer: str, victim: str) -> Prop:
    return Prop("killed", (killer, victim))

def dead(who: str) -> Prop:
    return Prop("dead", (who,))

def king(who: str, realm: str) -> Prop:
    return Prop("king", (who, realm))

def thane(who: str, where: str) -> Prop:
    return Prop("thane", (who, where))

def married(a: str, b: str) -> Prop:
    return Prop("married", (a, b))

def parent_of(parent: str, child: str) -> Prop:
    return Prop("parent_of", (parent, child))

def kinsman_of(a: str, b: str) -> Prop:
    # Symmetric in intent; the encoding authors both directions where
    # useful. A future inference rule can take symmetry for granted.
    return Prop("kinsman_of", (a, b))

def at_location(who: str, where: str) -> Prop:
    return Prop("at_location", (who, where))

def guest_of(guest: str, host: str) -> Prop:
    return Prop("guest_of", (guest, host))

def host_of(host: str, guest: str) -> Prop:
    return Prop("host_of", (host, guest))

def defended(defender: str, realm: str) -> Prop:
    return Prop("defended", (defender, realm))

def ordered_killing(orderer: str, victim: str) -> Prop:
    return Prop("ordered_killing", (orderer, victim))

def moving_toward(mover: str, destination: str) -> Prop:
    return Prop("moving_toward", (mover, destination))

def born_not_of_woman(who: str) -> Prop:
    # Shakespearean ritual language for the Caesarean-birth detail.
    # Macbeth holds this at KNOWN only at the final confrontation
    # with Macduff — the moment the second prophecy's protection
    # collapses.
    return Prop("born_not_of_woman", (who,))

def apparition_of(entity: str, at: str) -> Prop:
    # Observed apparition. Whether this is a world-level fact (a
    # real ghost) or an agent-only observation (Macbeth's guilt
    # manifesting) is a descriptions-layer question. The substrate
    # records the observation without committing to the ontology.
    return Prop("apparition_of", (entity, at))

# Prophecy-content predicates. Shakespearean: the Witches' prophecies
# are statements about future state. Authored as arity-1 predicates
# naming the subject; the content is in the predicate name. (Same
# pattern as oedipus.py's prophecy_will_kill_father_and_marry_mother.)

def prophecy_thane_of_cawdor(who: str) -> Prop:
    return Prop("prophecy_thane_of_cawdor", (who,))

def prophecy_will_be_king(who: str) -> Prop:
    return Prop("prophecy_will_be_king", (who,))

def prophecy_descendants_kings(who: str) -> Prop:
    return Prop("prophecy_descendants_kings", (who,))

def prophecy_beware_macduff(who: str) -> Prop:
    return Prop("prophecy_beware_macduff", (who,))

def prophecy_none_of_woman_born_shall_harm(who: str) -> Prop:
    return Prop("prophecy_none_of_woman_born_shall_harm", (who,))

def prophecy_safe_until_birnam_moves(who: str) -> Prop:
    return Prop("prophecy_safe_until_birnam_moves", (who,))

# Compound / moral-register predicates. Currently authored as world
# facts where their premises hold; candidate derivations for the
# inference engine once it lands (inference-model-sketch-01 N9).

def kinslayer(slayer: str, victim: str) -> Prop:
    # ⇐ killed(X, Y) ∧ kinsman_of(X, Y)
    return Prop("kinslayer", (slayer, victim))

def regicide(slayer: str, victim: str) -> Prop:
    # ⇐ killed(X, Y) ∧ king(Y, _)
    return Prop("regicide", (slayer, victim))

def breach_of_hospitality(host: str, guest: str) -> Prop:
    # ⇐ killed(X, Y) ∧ guest_of(Y, X)
    return Prop("breach_of_hospitality", (host, guest))

def tyrant(who: str) -> Prop:
    # ⇐ kinslayer(X, _) ∧ regicide(X, _) ∧ king(X, _)
    # Or: king(X, _) ∧ ordered_killing(X, innocent_civilian) — the
    # latter captures the Lady Macduff slaughter as tyranny-making,
    # not just regicide. The inference-02 sketch may refine.
    return Prop("tyrant", (who,))


# ----------------------------------------------------------------------------
# Event helpers — same pattern as oedipus.py's helpers.
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

def remove_held(agent_id: str, p: Prop, slot: Slot,
                confidence: Confidence, τ: int,
                via: str = None, note: str = "") -> KnowledgeEffect:
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
        id="E_macbeth_defends_scotland",
        type="battle",
        τ_s=-5, τ_a=1,
        participants={"defender": "macbeth", "realm": "scotland"},
        effects=(
            # World truth: Macbeth defended Scotland against the rebel
            # Macdonwald and the Norwegian invader. Act 1 opens with
            # reports of his heroism.
            world(defended("macbeth", "scotland")),
            observe("macbeth", defended("macbeth", "scotland"), -5,
                    note="leads Scotland's forces; acclaimed as hero"),
            # Duncan (and by extension the court) observes the heroism
            # by report, not by direct witness — but the substrate
            # collapses the chain: the king is aware at KNOWN via
            # utterance-heard (the Captain's report).
            told_by("duncan", "captain-off-stage",
                    defended("macbeth", "scotland"), -5,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="the Captain's report in Act 1 Scene 2"),
        ),
    ),

    Event(
        id="E_macbeth_kinsman_of_duncan",
        type="standing",
        τ_s=-100, τ_a=2,
        participants={"a": "macbeth", "b": "duncan"},
        effects=(
            # Historical / genealogical fact: Macbeth and Duncan are
            # cousins (both grandsons of Malcolm II in the chronicle).
            # Authored at a distant τ_s so the kinsman_of relation is
            # always in world-scope. Symmetric.
            world(kinsman_of("macbeth", "duncan")),
            world(kinsman_of("duncan", "macbeth")),
            # Macbeth knows his lineage.
            observe("macbeth", kinsman_of("macbeth", "duncan"), -100,
                    note="known family relation"),
            # So does Duncan. (And everyone at court; the ceremonial
            # kinship is a public fact — the substrate takes it as
            # world-known.)
            observe("duncan", kinsman_of("macbeth", "duncan"), -100),
        ),
    ),

    Event(
        id="E_macbeth_thane_of_glamis",
        type="standing",
        τ_s=-50, τ_a=3,
        participants={"who": "macbeth"},
        effects=(
            world(thane("macbeth", "glamis")),
            observe("macbeth", thane("macbeth", "glamis"), -50,
                    note="inherited standing"),
        ),
    ),

    Event(
        id="E_duncan_king_of_scotland",
        type="standing",
        τ_s=-30, τ_a=4,
        participants={"who": "duncan"},
        effects=(
            world(king("duncan", "scotland")),
            # Malcolm is Duncan's heir apparent; parent_of is authored
            # at the same standing-facts level.
            world(parent_of("duncan", "malcolm")),
            world(parent_of("duncan", "donalbain")),
            # And Macbeth has a wife, Macduff has a wife and a son —
            # family facts used later.
            world(married("macbeth", "lady_macbeth")),
            world(married("macduff", "lady_macduff")),
            world(parent_of("macduff", "macduff_son")),
            world(parent_of("banquo", "fleance")),
        ),
    ),

    # --- Play (τ_s ≥ 0) ---

    Event(
        id="E_prophecy_first",
        type="prophecy_received",
        τ_s=0, τ_a=10,
        participants={"prophets": "witches",
                      "recipients": ["macbeth", "banquo"]},
        effects=(
            world(at_location("macbeth", "the_heath")),
            world(at_location("banquo", "the_heath")),
            # Macbeth hears three hails: Glamis (already true),
            # Cawdor (not yet true but pending), King-hereafter (not
            # yet true). The Glamis hail is confirmation, not news.
            told_by("macbeth", "witches",
                    thane("macbeth", "glamis"), 0,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Witches confirm an existing fact"),
            told_by("macbeth", "witches",
                    prophecy_thane_of_cawdor("macbeth"), 0,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="second hail; will be verified shortly"),
            told_by("macbeth", "witches",
                    prophecy_will_be_king("macbeth"), 0,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="third hail; ambition kindled"),
            # Banquo is told his descendants will be kings.
            told_by("banquo", "witches",
                    prophecy_descendants_kings("banquo"), 0,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Banquo's share of the prophecy"),
        ),
    ),

    Event(
        id="E_thane_of_cawdor_awarded",
        type="royal_decree",
        τ_s=1, τ_a=11,
        participants={"decree": "duncan", "subject": "macbeth"},
        effects=(
            # The existing thane of Cawdor has betrayed Scotland; Duncan
            # confers the title on Macbeth. The prophecy's second hail
            # is verified.
            world(thane("macbeth", "cawdor")),
            told_by("macbeth", "ross",
                    thane("macbeth", "cawdor"), 1,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Ross brings the news"),
            # No factual dislodgement — the earlier prophecy is
            # confirmed, not overwritten.
        ),
    ),

    Event(
        id="E_letter_to_lady_macbeth",
        type="correspondence",
        τ_s=2, τ_a=12,
        participants={"writer": "macbeth", "reader": "lady_macbeth"},
        effects=(
            # Macbeth's letter transmits the prophecy to his wife. She
            # holds its content at KNOWN — she believes the Witches'
            # words completely, more than Macbeth himself does in the
            # near-term.
            told_by("lady_macbeth", "macbeth",
                    prophecy_thane_of_cawdor("macbeth"), 2,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            told_by("lady_macbeth", "macbeth",
                    thane("macbeth", "cawdor"), 2,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            told_by("lady_macbeth", "macbeth",
                    prophecy_will_be_king("macbeth"), 2,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
        ),
    ),

    Event(
        id="E_duncan_visits",
        type="arrival",
        τ_s=3, τ_a=13,
        participants={"guest": "duncan", "host": "macbeth",
                      "at": "inverness"},
        effects=(
            world(at_location("duncan", "inverness")),
            world(guest_of("duncan", "macbeth")),
            world(host_of("macbeth", "duncan")),
            observe("macbeth",  guest_of("duncan", "macbeth"), 3),
            observe("duncan",   guest_of("duncan", "macbeth"), 3),
            observe("lady_macbeth", guest_of("duncan", "macbeth"), 3),
        ),
    ),

    Event(
        id="E_duncan_killed",
        type="killing",
        τ_s=5, τ_a=14,
        participants={"killer": "macbeth", "victim": "duncan"},
        effects=(
            # Primary fact: Macbeth kills the sleeping king under his
            # own roof. All three Dramatica-worth moral weights fire
            # here: kinslayer (Duncan is kin), regicide (Duncan is
            # king), breach_of_hospitality (Duncan is Macbeth's
            # guest). Until the inference engine lands, each is
            # authored as world-true at this event; the comments point
            # at the rule that would derive it.
            world(killed("macbeth", "duncan")),
            world(dead("duncan")),
            # The compound predicates kinslayer, regicide, and
            # breach_of_hospitality are no longer authored here. With
            # inference-model-sketch-01 implemented in the substrate,
            # each derives at query time from the rules in RULES
            # below. Premises: killed (just authored); kinsman_of
            # (E_macbeth_kinsman_of_duncan); king(duncan, scotland)
            # (E_duncan_king_of_scotland); guest_of(duncan, macbeth)
            # (E_duncan_visits). All three derivations land at query
            # time with depth=1.
            # Macbeth holds the killing at KNOWN. He did it.
            observe("macbeth", killed("macbeth", "duncan"), 5,
                    note="self-witnessed; the dagger-in-his-hand scene"),
            observe("macbeth", dead("duncan"), 5),
            # Lady Macbeth is complicit — she handled the daggers after
            # the killing and smeared the grooms' blood. She knows.
            observe("lady_macbeth", killed("macbeth", "duncan"), 5,
                    note="co-conspirator; handled the daggers"),
            observe("lady_macbeth", dead("duncan"), 5),
        ),
    ),

    Event(
        id="E_duncan_discovered",
        type="discovery",
        τ_s=5, τ_a=15,  # same τ_s, sequential τ_a
        participants={"discoverer": "macduff", "victim": "duncan"},
        effects=(
            # Macduff finds the body. Suspicion lands on the grooms
            # (dead themselves, killed by Macbeth to cover his tracks
            # — not encoded here as a separate event), then on
            # Malcolm and Donalbain (fleeing), then slowly on Macbeth.
            observe("macduff", dead("duncan"), 5,
                    note="discovers the body"),
            told_by("lady_macbeth", "macduff",
                    dead("duncan"), 5,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="she reacts as if hearing it for the first time"),
            # Malcolm and Donalbain flee (to England and Ireland
            # respectively). Their absence turns suspicion.
            world(at_location("malcolm", "england")),
        ),
    ),

    Event(
        id="E_macbeth_crowned",
        type="coronation",
        τ_s=6, τ_a=16,
        participants={"new_king": "macbeth"},
        effects=(
            world(king("macbeth", "scotland")),
            observe("macbeth", king("macbeth", "scotland"), 6),
            observe("lady_macbeth", king("macbeth", "scotland"), 6),
            # Banquo, at this point, begins to suspect. Encoded at
            # BELIEVED on his state.
            observe("banquo", killed("macbeth", "duncan"), 6,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    via=Diegetic.INFERENCE.value,
                    note="suspects because the prophecy's upper hails "
                         "are all coming true"),
        ),
    ),

    Event(
        id="E_banquo_killed",
        type="killing",
        τ_s=8, τ_a=17,
        participants={"orderer": "macbeth", "killers": "murderers",
                      "victim": "banquo"},
        effects=(
            # Second killing. Macbeth hires murderers; the attack
            # succeeds on Banquo but Fleance escapes. The escape is
            # the load-bearing detail: Banquo's prophesied descendants-
            # kings line remains alive.
            world(killed("murderers", "banquo")),
            world(dead("banquo")),
            world(ordered_killing("macbeth", "banquo")),
            # Fleance — the son — survives and flees. at_location is
            # authored opaquely (not in scotland); the substrate
            # doesn't track "fled" as its own predicate.
            world(at_location("fleance", "england")),  # symbolic safe-haven
            # Macbeth hears the result from the murderers' report.
            told_by("macbeth", "murderers",
                    dead("banquo"), 8,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            told_by("macbeth", "murderers",
                    at_location("fleance", "england"), 8,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Fleance's escape reported; exact whereabouts "
                         "unknown"),
            # Macbeth's tyranny deepens; the ordered-killing-of-a-
            # comrade is the second moral step.
            observe("macbeth", ordered_killing("macbeth", "banquo"), 8),
        ),
    ),

    Event(
        id="E_banquet_ghost",
        type="apparition",
        τ_s=9, τ_a=18,
        participants={"perceiver": "macbeth", "apparition_of": "banquo"},
        effects=(
            # Deliberately NOT a world-effect asserting the ghost
            # exists. The substrate records Macbeth's observation;
            # whether a ghost "really" sat at the feast is left to
            # descriptions. This parallels oedipus.py's authorial
            # reticence about the gods' hand in the oracle.
            observe("macbeth", apparition_of("banquo", "dunsinane"), 9,
                    note="ghost at the banquet; others see nothing"),
            # Lady Macbeth explicitly does NOT observe the ghost —
            # she covers for Macbeth's fit. Her held set does not
            # contain the apparition.
            # Other guests observe Macbeth's disturbance only.
        ),
    ),

    Event(
        id="E_prophecy_second",
        type="prophecy_received",
        τ_s=10, τ_a=19,
        participants={"prophets": "witches", "recipient": "macbeth"},
        effects=(
            world(at_location("macbeth", "the_heath")),
            # Three ritual apparitions: an armed head, a bloody child,
            # a crowned child. The substrate records the prophecies
            # they deliver; the visual ceremony is description
            # territory.
            told_by("macbeth", "witches",
                    prophecy_beware_macduff("macbeth"), 10,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            told_by("macbeth", "witches",
                    prophecy_none_of_woman_born_shall_harm("macbeth"), 10,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Macbeth takes this as absolute protection. "
                         "He is wrong."),
            told_by("macbeth", "witches",
                    prophecy_safe_until_birnam_moves("macbeth"), 10,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Macbeth takes this as impossible. He is wrong."),
        ),
    ),

    Event(
        id="E_macduff_flees",
        type="flight",
        τ_s=11, τ_a=20,
        participants={"fugitive": "macduff", "to": "england"},
        effects=(
            remove_held("macduff", at_location("macduff", "scotland"),
                        Slot.KNOWN, Confidence.CERTAIN, 11,
                        note="no longer in Scotland"),
            world(at_location("macduff", "england")),
            observe("macduff", at_location("macduff", "england"), 11),
            # Macbeth hears of the flight and decides to strike at
            # what Macduff left behind.
            told_by("macbeth", "ross",
                    at_location("macduff", "england"), 11,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
        ),
    ),

    Event(
        id="E_macduff_family_killed",
        type="killing",
        τ_s=12, τ_a=21,
        participants={"orderer": "macbeth", "killers": "murderers",
                      "victims": ["lady_macduff", "macduff_son"]},
        effects=(
            # Third killing — and the moral nadir. Innocent civilians;
            # a wife and child; ordered without even the political
            # pretext the earlier killings had. The tyrant predicate
            # is canonically earned here.
            world(killed("murderers", "lady_macduff")),
            world(dead("lady_macduff")),
            world(killed("murderers", "macduff_son")),
            world(dead("macduff_son")),
            world(ordered_killing("macbeth", "lady_macduff")),
            world(ordered_killing("macbeth", "macduff_son")),
            # tyrant(macbeth) is no longer authored here. Under
            # TYRANT_RULE (see RULES below), it derives at query time
            # from:
            #     kinslayer(X, _) ∧ regicide(X, _) ∧ king(X, _)
            # All three premises hold for Macbeth after E_duncan_killed
            # (kinslayer and regicide derive there) and E_macbeth_
            # crowned (king). So tyrant actually derives at τ_s=6
            # (coronation), which is arguable Shakespeare reading —
            # tyranny begins with the usurping kinslaying-regicide,
            # not with the later innocent-killing. A richer inference
            # model (with innocent-civilian tagging) could tighten
            # to the Macduff-family event; this sketch's rule is
            # coarser on purpose.
        ),
    ),

    Event(
        id="E_sleepwalking",
        type="unraveling",
        τ_s=13, τ_a=22,
        participants={"focal": "lady_macbeth",
                      "observers": ["doctor-off-stage",
                                    "gentlewoman-off-stage"]},
        effects=(
            # Lady Macbeth sleepwalks, confesses through fragments.
            # The substrate records her agent-state: her BELIEVED
            # dead(duncan) and killed(macbeth, duncan) now surface as
            # compulsive speech. No new facts are authored — but the
            # dam of her complicity breaks. The Doctor overhears;
            # the kingdom hears rumors.
            #
            # Encoded effect: the Doctor comes to hold at BELIEVED
            # that Macbeth killed Duncan, via utterance-heard.
            told_by("doctor-off-stage", "lady_macbeth",
                    killed("macbeth", "duncan"), 13,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="overheard during her sleepwalking; the Doctor "
                         "knows too much"),
        ),
    ),

    Event(
        id="E_lady_macbeth_dies",
        type="death",
        τ_s=14, τ_a=23,
        participants={"who": "lady_macbeth"},
        effects=(
            # Shakespeare leaves the manner of death ambiguous
            # (suicide is strongly implied). The substrate records
            # the fact; descriptions address the implication.
            world(dead("lady_macbeth")),
            told_by("macbeth", "messenger-off-stage",
                    dead("lady_macbeth"), 14,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="'She should have died hereafter.' The report "
                         "lands; Macbeth's response is the 'tomorrow' "
                         "speech."),
        ),
    ),

    Event(
        id="E_birnam_moves",
        type="siege",
        τ_s=15, τ_a=24,
        participants={"movers": "malcolm-and-macduff-forces"},
        effects=(
            # Malcolm's soldiers cut boughs from Birnam Wood as
            # camouflage. The substrate records the literal event:
            # the wood (or its branches, materially speaking) moves
            # toward Dunsinane. The second prophecy's unfalsifiable
            # condition is met.
            world(moving_toward("birnam_wood", "dunsinane")),
            told_by("macbeth", "messenger-off-stage",
                    moving_toward("birnam_wood", "dunsinane"), 15,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="the news reaches Dunsinane"),
        ),
    ),

    Event(
        id="E_macduff_reveals_birth",
        type="utterance",
        τ_s=17, τ_a=25,
        participants={"speaker": "macduff", "listener": "macbeth"},
        effects=(
            # On the battlefield, Macduff reveals the Caesarean birth —
            # he was "not of woman born" in the prophecy's specific
            # sense. Macbeth realizes the second prophecy's unfalsifiable
            # protection has collapsed.
            world(born_not_of_woman("macduff")),
            told_by("macbeth", "macduff",
                    born_not_of_woman("macduff"), 17,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            # The protective reading of prophecy_none_of_woman_born is
            # not "removed" — the literal fact still stands. But
            # Macbeth's inferred protection collapses. Authored here
            # as the dislodgement of a derived belief; the substrate
            # represents it as a remove-held on a BELIEVED safe-from-
            # all-men proposition. (A future inference layer could
            # derive this transition cleanly.)
            remove_held("macbeth",
                        prophecy_none_of_woman_born_shall_harm("macbeth"),
                        Slot.KNOWN, Confidence.CERTAIN, 17,
                        via=Diegetic.INFERENCE.value,
                        note="his reading of protection collapses; "
                             "the prophecy is literally true but "
                             "catastrophically misleading"),
        ),
    ),

    Event(
        id="E_macbeth_killed",
        type="killing",
        τ_s=17, τ_a=26,  # same τ_s, sequential τ_a
        participants={"killer": "macduff", "victim": "macbeth"},
        effects=(
            world(killed("macduff", "macbeth")),
            world(dead("macbeth")),
            # Macduff knows; he did it.
            observe("macduff", killed("macduff", "macbeth"), 17),
            # kinsman_of is NOT asserted between Macduff and Macbeth;
            # they are not kin. So this is not kinslaying. It IS
            # regicide in the formal sense (Macbeth was king), though
            # the moral weight is reversed — this is the tyrant's
            # rightful overthrow. Derives via REGICIDE_RULE from
            # killed(macduff, macbeth) + king(macbeth, scotland); no
            # authored assertion needed.
        ),
    ),

    Event(
        id="E_malcolm_crowned",
        type="coronation",
        τ_s=18, τ_a=27,
        participants={"new_king": "malcolm"},
        effects=(
            # The succession restored. The story goal — rightful
            # order to Scotland — is satisfied at this event.
            world(king("malcolm", "scotland")),
            # Malcolm's kingship dislodges Macbeth's — by this point
            # Macbeth is dead, but the world predicate king(macbeth, _)
            # held until now and should be marked ended. Encoded as
            # a removal via inference (the fact is not-true anymore
            # because the holder is dead and succeeded).
            world(king("macbeth", "scotland"), asserts=False),
            observe("malcolm", king("malcolm", "scotland"), 18),
        ),
    ),

]


# ----------------------------------------------------------------------------
# Sjuzhet — Macbeth is largely linear; τ_d ≈ τ_s for in-play events.
# ----------------------------------------------------------------------------
#
# Preplay disclosures are minimal — Shakespeare's audience is expected
# to know Macbeth is a thane and Duncan is king, but the play reveals
# most of the fabula as it unfolds. No myth-foreknowledge comparable to
# Oedipus.

PREPLAY_DISCLOSURES = (
    Disclosure(prop=king("duncan", "scotland"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=thane("macbeth", "glamis"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=defended("macbeth", "scotland"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=kinsman_of("macbeth", "duncan"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=married("macbeth", "lady_macbeth"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
)


SJUZHET = [

    # τ_d=0 — the audience enters with the preplay disclosures loaded.
    # The first scene (Witches on the heath) is a preview; τ_d=0 is
    # the battle report in Act 1 Scene 2, which anchors the preplay
    # facts. We use E_macbeth_defends_scotland as the anchor event.
    SjuzhetEntry(
        event_id="E_macbeth_defends_scotland",
        τ_d=0,
        focalizer_id=None,  # omniscient framing (the Captain reports)
        disclosures=PREPLAY_DISCLOSURES,
    ),

    # τ_d=1 — Witches + Macbeth + Banquo on the heath.
    SjuzhetEntry(
        event_id="E_prophecy_first",
        τ_d=1,
        focalizer_id="macbeth",  # the scene's perspective is his
        disclosures=(),
    ),

    # τ_d=2 — Cawdor thaneship conferred.
    SjuzhetEntry(
        event_id="E_thane_of_cawdor_awarded",
        τ_d=2,
        focalizer_id="macbeth",
        disclosures=(),
    ),

    # τ_d=3 — Lady Macbeth reads the letter.
    SjuzhetEntry(
        event_id="E_letter_to_lady_macbeth",
        τ_d=3,
        focalizer_id="lady_macbeth",
        disclosures=(),
    ),

    # τ_d=4 — Duncan arrives at Inverness.
    SjuzhetEntry(
        event_id="E_duncan_visits",
        τ_d=4,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=5 — the killing (offstage, but the sjuzhet entry is the
    # scene of its aftermath: the daggers, the washing, the Porter).
    SjuzhetEntry(
        event_id="E_duncan_killed",
        τ_d=5,
        focalizer_id="macbeth",
        disclosures=(),
    ),

    # τ_d=6 — discovery and the sons' flight.
    SjuzhetEntry(
        event_id="E_duncan_discovered",
        τ_d=6,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=7 — coronation, Banquo's soliloquy of suspicion.
    SjuzhetEntry(
        event_id="E_macbeth_crowned",
        τ_d=7,
        focalizer_id="banquo",  # Banquo's suspicions are where the
                                # scene's weight sits
        disclosures=(),
    ),

    # τ_d=8 — Banquo's killing (offstage to the audience, reported
    # by murderers).
    SjuzhetEntry(
        event_id="E_banquo_killed",
        τ_d=8,
        focalizer_id="macbeth",
        disclosures=(),
    ),

    # τ_d=9 — the banquet; ghost appears to Macbeth only.
    SjuzhetEntry(
        event_id="E_banquet_ghost",
        τ_d=9,
        focalizer_id="macbeth",
        disclosures=(),
    ),

    # τ_d=10 — second prophecy.
    SjuzhetEntry(
        event_id="E_prophecy_second",
        τ_d=10,
        focalizer_id="macbeth",
        disclosures=(),
    ),

    # τ_d=11 — Macduff flees; news reaches Macbeth.
    SjuzhetEntry(
        event_id="E_macduff_flees",
        τ_d=11,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=12 — the Macduff-family slaughter.
    SjuzhetEntry(
        event_id="E_macduff_family_killed",
        τ_d=12,
        focalizer_id="lady_macduff",  # the scene centers on the victims
        disclosures=(),
    ),

    # τ_d=13 — Lady Macbeth sleepwalks.
    SjuzhetEntry(
        event_id="E_sleepwalking",
        τ_d=13,
        focalizer_id="lady_macbeth",
        disclosures=(),
    ),

    # τ_d=14 — Lady Macbeth's death; Macbeth's "tomorrow" soliloquy.
    SjuzhetEntry(
        event_id="E_lady_macbeth_dies",
        τ_d=14,
        focalizer_id="macbeth",
        disclosures=(),
    ),

    # τ_d=15 — Birnam Wood moves.
    SjuzhetEntry(
        event_id="E_birnam_moves",
        τ_d=15,
        focalizer_id="macbeth",
        disclosures=(),
    ),

    # τ_d=16 — Macduff's reveal on the battlefield.
    SjuzhetEntry(
        event_id="E_macduff_reveals_birth",
        τ_d=16,
        focalizer_id="macbeth",
        disclosures=(),
    ),

    # τ_d=17 — Macbeth killed.
    SjuzhetEntry(
        event_id="E_macbeth_killed",
        τ_d=17,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=18 — Malcolm crowned; order restored.
    SjuzhetEntry(
        event_id="E_malcolm_crowned",
        τ_d=18,
        focalizer_id=None,
        disclosures=(),
    ),

]


# ----------------------------------------------------------------------------
# Descriptions — the interpretive peer surface.
# ----------------------------------------------------------------------------
#
# τ_a values start at 100 (after all fabula τ_a values, which top out
# at 27). Later authoring passes can interleave without renumbering.

DESCRIPTIONS = [

    Description(
        id="D_macbeth_moral_trajectory",
        attached_to=anchor_event("E_macbeth_killed"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("Macbeth's arc is a descent traced by killings — Duncan "
              "(kin, king, guest; three moral breaches at once), "
              "Banquo (sworn comrade; cold calculation), Lady Macduff "
              "and her children (innocents; pure tyranny). Each "
              "killing removes another inhibition. By the battle at "
              "Dunsinane, the hero of Act 1 is unrecognizable. The "
              "Argument's affirmation (ambition unmakes the one who "
              "indulges it) is realized across the whole trajectory "
              "— no single scene carries it."),
        authored_by="author",
        τ_a=100,
    ),

    Description(
        id="D_prophecy_ambiguity",
        attached_to=anchor_event("E_prophecy_first"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("The Witches' prophecies are literally true and "
              "catastrophically misleading. 'Thane of Cawdor' — "
              "true. 'Will be king' — true, but the path is "
              "Macbeth's to choose and Macbeth chooses murder. "
              "Similarly in the second prophecy: 'none of woman "
              "born' — Macduff's Caesarean birth satisfies the "
              "letter while violating the implied promise of "
              "protection. 'Until Birnam Wood moves' — camouflage "
              "branches satisfy it. The prophecies do not lie; "
              "Macbeth's interpretations do."),
        authored_by="author",
        τ_a=101,
    ),

    Description(
        id="D_witches_ontology_undecided",
        attached_to=anchor_event("E_prophecy_first"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("The substrate encoding takes no position on what the "
              "Witches are. Supernatural agents with real foresight? "
              "Manipulators inducing the behavior they 'foretell'? "
              "Projections of Macbeth's own ambition given external "
              "voice? The encoding records their utterances as "
              "agent-state effects on Macbeth and Banquo; it does "
              "not author a world-fact asserting the Witches can "
              "foresee. A future encoding pass may wish to commit "
              "one way or the other, or to keep the authorial "
              "reticence explicit as a commitment."),
        is_question=True,
        authored_by="author",
        τ_a=102,
    ),

    Description(
        id="D_banquet_ghost_ontology_undecided",
        attached_to=anchor_event("E_banquet_ghost"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Banquo's ghost is encoded as an observation on "
              "Macbeth's held set only; no world-effect asserts "
              "the ghost 'really' sits at the table. Whether the "
              "apparition is a visitation (world-real) or a "
              "projection of Macbeth's guilt (agent-only) is not "
              "settled. The choice is consistent with the Witches' "
              "encoding: the substrate records what characters "
              "observe; the ontology of the supernatural is a "
              "description-layer question."),
        is_question=True,
        authored_by="author",
        τ_a=103,
    ),

    Description(
        id="D_lady_macbeth_inverse_arc",
        attached_to=anchor_event("E_sleepwalking"),
        kind="texture",
        attention=Attention.INTERPRETIVE,
        text=("Lady Macbeth is the play's driving force in Act 1 and "
              "Act 2 — she reads the letter and decides; she chides "
              "Macbeth into the killing; she handles the daggers after. "
              "Then the arc reverses. Macbeth becomes the calculating "
              "one (Banquo, the Macduff family); Lady Macbeth becomes "
              "the one who cannot bear it. The sleepwalking is the "
              "external symptom of the inversion complete; her suicide "
              "precedes his death by the smallest possible interval. "
              "The Impact Character role's *direction* is not constant "
              "across the play; the role itself inverts."),
        authored_by="author",
        τ_a=104,
        status=DescStatus.SUPERSEDED,
        metadata={
            "superseded_by": "D_lady_macbeth_inverse_arc_edit_by_llm_claude-opus-4-6_τ_a_30000",
        },
    ),

    # Probe-authored edit, accepted at τ_a=30000. Provenance:
    # reader_model_macbeth_output.json. The probe correctly caught two
    # ungrounded claims in the prior text: (1) "her suicide" attributes
    # cause that E_lady_macbeth_dies (typed "death") does not assert;
    # (2) "smallest possible interval" overstates proximity given
    # τ_s=14 → τ_s=17 with intervening events.
    Description(
        id="D_lady_macbeth_inverse_arc_edit_by_llm_claude-opus-4-6_τ_a_30000",
        attached_to=anchor_event("E_sleepwalking"),
        kind="texture",
        attention=Attention.INTERPRETIVE,
        text=("Lady Macbeth is the play's driving force in Act 1 and "
              "Act 2 — she reads the letter and decides; she chides "
              "Macbeth into the killing; she handles the daggers after. "
              "Then the arc reverses. Macbeth becomes the calculating "
              "one (Banquo, the Macduff family); Lady Macbeth becomes "
              "the one who cannot bear it. The sleepwalking is the "
              "external symptom of the inversion complete; her death "
              "at τ_s=14 precedes his at τ_s=17, the two endpoints "
              "nearly adjacent in the play's compressed finale. The "
              "Impact Character role's *direction* is not constant "
              "across the play; the role itself inverts."),
        authored_by="llm:claude-opus-4-6",
        τ_a=30_000,
        metadata={
            "supersedes": "D_lady_macbeth_inverse_arc",
        },
    ),

    Description(
        id="D_compound_predicates_candidate_for_derivation",
        attached_to=anchor_event("E_duncan_killed"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("kinslayer(macbeth, duncan), regicide(macbeth, duncan), "
              "and breach_of_hospitality(macbeth, duncan) were "
              "originally authored as world facts at this killing "
              "event, paired with tyrant(macbeth) at E_macduff_family_"
              "killed. They are the conclusions of domain rules. "
              "RESOLVED (2026-04-14): the inference engine per "
              "inference-model-sketch-01 is now implemented in the "
              "substrate. All four compound predicates derive at "
              "query time via RULES (see the RULES export at the end "
              "of this module). The authored assertions have retired. "
              "Rules: "
              "`killed(X,Y) ∧ kinsman_of(X,Y) ⇒ kinslayer(X,Y)`, "
              "`killed(X,Y) ∧ king(Y,R) ⇒ regicide(X,Y)`, "
              "`killed(X,Y) ∧ guest_of(Y,X) ⇒ breach_of_hospitality(X,Y)`, "
              "`kinslayer(X,_) ∧ regicide(X,_) ∧ king(X,_) ⇒ tyrant(X)`. "
              "The tyrant rule is depth-2 (consumes two depth-1 "
              "derivations); all other rules are depth-1. A follow-"
              "on inference-02 pass may tighten tyrant to a more "
              "specific rule once typed inequality / innocent-"
              "civilian tagging exists."),
        is_question=True,
        authored_by="author",
        τ_a=105,
    ),

    Description(
        id="D_cumulative_judgment",
        attached_to=anchor_event("E_lady_macbeth_dies"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        status=DescStatus.SUPERSEDED,
        metadata={
            "superseded_by": "D_cumulative_judgment_edit_by_llm_claude-opus-4-6_τ_a_30000",
        },
        text=("Under dramatica-complete's DynamicStoryPoint(judgment=bad), "
              "Macbeth's Judgment is earned across the trajectory, not "
              "at any moment. Duncan's killing is the precipitation "
              "that drops him into the descent, but judgment=bad lands "
              "cumulatively: Banquo's killing removes the comradeship; "
              "the Macduff-family slaughter removes the pretext of "
              "political necessity; the 'tomorrow' soliloquy removes "
              "the capacity to feel. A single-moment verifier at "
              "τ_s=17 (Macbeth's death) could confirm judgment=bad for "
              "the wrong reason (the MC ends dead). A trajectory-"
              "pattern verifier that reads the accumulating descent is "
              "the right check. This is the forcing case for "
              "lowering-sketch-02's F8."),
        authored_by="author",
        τ_a=106,
    ),

    # Probe-authored edit, accepted at τ_a=30000. Provenance:
    # reader_model_macbeth_output.json. The probe correctly caught
    # that the prior text referenced "the 'tomorrow' soliloquy",
    # which is not encoded as any event in the view. The corrected
    # version anchors that step in Lady Macbeth's death (which IS
    # in the view, E_lady_macbeth_dies at τ_s=14), preserving the
    # escalating-loss structure of the trajectory argument.
    Description(
        id="D_cumulative_judgment_edit_by_llm_claude-opus-4-6_τ_a_30000",
        attached_to=anchor_event("E_lady_macbeth_dies"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("Under dramatica-complete's DynamicStoryPoint(judgment=bad), "
              "Macbeth's Judgment is earned across the trajectory, not "
              "at any moment. Duncan's killing is the precipitation "
              "that drops him into the descent, but judgment=bad lands "
              "cumulatively: Banquo's killing removes the comradeship; "
              "the Macduff-family slaughter removes the pretext of "
              "political necessity; Lady Macbeth's death severs his "
              "last human attachment. A single-moment verifier at "
              "τ_s=17 (Macbeth's death) could confirm judgment=bad for "
              "the wrong reason (the MC ends dead). A trajectory-"
              "pattern verifier that reads the accumulating descent is "
              "the right check. This is the forcing case for "
              "lowering-sketch-02's F8."),
        authored_by="llm:claude-opus-4-6",
        τ_a=30_000,
        metadata={
            "supersedes": "D_cumulative_judgment",
        },
    ),

    # Probe-authored answer to D_witches_ontology_undecided, accepted
    # at τ_a=30000. The probe argues for preserving the encoding's
    # ontological reticence as an explicit, permanent commitment
    # rather than a gap awaiting resolution; proposes that future
    # ontology commitments live on :contested branches rather than
    # on :canonical.
    Description(
        id="D_witches_ontology_undecided_answer_by_llm_claude-opus-4-6_τ_a_30000",
        attached_to=anchor_event("E_prophecy_first"),
        kind="reader-frame",
        attention=Attention.INTERPRETIVE,
        text=("The encoding's ontological reticence about the Witches "
              "should be preserved as an explicit, permanent commitment "
              "rather than treated as a gap awaiting resolution. The "
              "event structure records prophecy content as agent_"
              "knowledge effects on macbeth and banquo (via utterance-"
              "heard) without any world-fact asserting foresight or "
              "causal power — and this is the right representation. "
              "The play supports at least three readings (genuine "
              "supernatural foresight, self-fulfilling manipulation, "
              "externalized ambition), and collapsing to one would "
              "lose interpretive range that the source material "
              "deliberately sustains. A formal marker such as "
              "ontology_of(witches) = deliberately_uncommitted would "
              "elevate this reticence from an implicit absence to a "
              "principled modeling decision. If a future branch wishes "
              "to explore a committed ontology, it can do so as a "
              ":contested branch (e.g., :b-witches-supernatural adding "
              "world-facts for foresight), leaving :canonical "
              "uncommitted."),
        authored_by="llm:claude-opus-4-6",
        τ_a=30_000,
        metadata={
            "answers_question": "D_witches_ontology_undecided",
        },
    ),

    # Probe-authored answer to D_banquet_ghost_ontology_undecided.
    # Argues that Witches' and ghost's ontology questions should
    # resolve (or stay open) as a pair, since they share the agent-
    # only encoding pattern.
    Description(
        id="D_banquet_ghost_ontology_undecided_answer_by_llm_claude-opus-4-6_τ_a_30000",
        attached_to=anchor_event("E_banquet_ghost"),
        kind="reader-frame",
        attention=Attention.INTERPRETIVE,
        text=("The ghost's agent-only encoding should be maintained "
              "as a deliberate parallel to the Witches' ontological "
              "reticence. E_banquet_ghost records the apparition as "
              "an agent_knowledge effect on macbeth alone — no other "
              "participant gains knowledge of the ghost, and no "
              "world-fact asserts its presence. This mirrors the "
              "dramatic structure: the ghost is perceptible only to "
              "Macbeth, making it structurally ambiguous between "
              "visitation and hallucination. Committing a world-fact "
              "(ghost-is-real) would invalidate the guilt-projection "
              "reading; committing to hallucination-only would lose "
              "the supernatural resonance with the Witches' "
              "prophecies. The two ontological questions (Witches, "
              "ghost) should be resolved — or left unresolved — as a "
              "pair, since the substrate treats them with the same "
              "pattern and they reinforce each other's interpretive "
              "openness."),
        authored_by="llm:claude-opus-4-6",
        τ_a=30_000,
        metadata={
            "answers_question": "D_banquet_ghost_ontology_undecided",
        },
    ),

    # Probe-authored answer to D_compound_predicates_candidate_for_
    # derivation. Validates the resolved status of the original
    # question and proposes a substantive inference-02 candidate
    # rule for tightening tyrant() to the Macduff-family event.
    Description(
        id="D_compound_predicates_candidate_for_derivation_answer_by_llm_claude-opus-4-6_τ_a_30000",
        attached_to=anchor_event("E_duncan_killed"),
        kind="provenance",
        attention=Attention.INTERPRETIVE,
        text=("The RESOLVED status is well-earned: the four inference "
              "rules correctly derive from base facts present in the "
              "view. kinslayer(macbeth, duncan) follows from "
              "E_duncan_killed + E_macbeth_kinsman_of_duncan; "
              "regicide(macbeth, duncan) from E_duncan_killed + "
              "E_duncan_king_of_scotland; breach_of_hospitality"
              "(macbeth, duncan) from E_duncan_killed + E_duncan_"
              "visits. The depth-2 tyrant(macbeth) derivation chains "
              "through kinslayer and regicide plus E_macbeth_crowned. "
              "The acknowledged gap around the tyrant rule is "
              "substantive: E_macduff_family_killed records ordered_"
              "killing(macbeth, lady_macduff) and ordered_killing"
              "(macbeth, macduff_son), but these facts do not "
              "contribute to the tyrant derivation. A candidate "
              "refinement for inference-02 would be: ordered_killing"
              "(X, Y) ∧ innocent(Y) ∧ king(X, _) ⇒ tyrant(X), which "
              "would give the Macduff-family slaughter independent "
              "force in the derivation rather than leaving tyrant "
              "dependent solely on the Duncan killing's compound "
              "breaches."),
        authored_by="llm:claude-opus-4-6",
        τ_a=30_000,
        metadata={
            "answers_question": "D_compound_predicates_candidate_for_derivation",
        },
    ),

    # Author-authored authorial-uncertainty question banking the
    # substantive proposal from the probe's witches/ghost answers
    # (the substrate-level ontology-meta-marker idea). Authored at
    # τ_a=30001 — just after the probe's records, marking it as a
    # follow-on consideration.
    Description(
        id="D_ontology_meta_marker_proposal",
        attached_to=anchor_desc(
            "D_witches_ontology_undecided_answer_by_llm_claude-opus-4-6_τ_a_30000"
        ),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("The Macbeth probe's witches/ghost answers proposed a "
              "new substrate-level marker: ontology_of(X) = "
              "deliberately_uncommitted. This would distinguish "
              "'we haven't decided' (a gap awaiting work) from 'we "
              "deliberately won't decide' (an authorial commitment "
              "to interpretive openness). The substrate today has "
              "no such marker; an authorial-uncertainty description "
              "(like D_witches_ontology_undecided itself) is the "
              "only mechanism for the second case, but it conflates "
              "the two. Open question: should the substrate add a "
              "first-class meta-marker for deliberate ontological "
              "commitment-to-reticence, or is the description "
              "surface sufficient? Banked for a future descriptions-"
              "sketch-02 or substrate-sketch-06 pass."),
        is_question=True,
        authored_by="author",
        τ_a=30_001,
    ),

]


# ----------------------------------------------------------------------------
# Rules — inference-model-sketch-01 N1–N10
# ----------------------------------------------------------------------------
#
# The four compound predicates (kinslayer, regicide,
# breach_of_hospitality, tyrant) are no longer author-asserted at their
# canonical events (see E_duncan_killed, E_macduff_family_killed, and
# E_macbeth_killed for the retirement comments). They derive via these
# rules at query time.
#
# Depth distribution:
#   - KINSLAYER_RULE, REGICIDE_RULE, BREACH_OF_HOSPITALITY_RULE:
#     depth 1 (each premise is authored world fact).
#   - TYRANT_RULE: depth 2 (premises are depth-1 derived predicates
#     kinslayer and regicide, plus the authored king fact).
#
# A depth_cap of 2 is required for this RULES set; the default 3 is
# sufficient. Rules compose with identity substitution (N4); none of
# Macbeth's encoding uses identity placeholders, so substitution does
# not contribute to these particular derivations.

KINSLAYER_RULE = Rule(
    id="R_kinslayer_from_killed_and_kinsman",
    head=Prop("kinslayer", ("X", "Y")),
    body=(
        Prop("killed",     ("X", "Y")),
        Prop("kinsman_of", ("X", "Y")),
    ),
)

REGICIDE_RULE = Rule(
    id="R_regicide_from_killed_and_king",
    head=Prop("regicide", ("X", "Y")),
    body=(
        Prop("killed", ("X", "Y")),
        Prop("king",   ("Y", "R")),  # R is the realm; unused in the head
                                     # but part of king/2. Range-restricted
                                     # because R appears in the body.
    ),
)

BREACH_OF_HOSPITALITY_RULE = Rule(
    id="R_breach_of_hospitality_from_killed_and_guest",
    head=Prop("breach_of_hospitality", ("X", "Y")),
    body=(
        Prop("killed",   ("X", "Y")),
        Prop("guest_of", ("Y", "X")),
    ),
)

TYRANT_RULE = Rule(
    id="R_tyrant_from_kinslayer_regicide_and_king",
    head=Prop("tyrant", ("X",)),
    body=(
        Prop("kinslayer", ("X", "V1")),
        Prop("regicide",  ("X", "V2")),
        Prop("king",      ("X", "R")),
    ),
)

RULES = (
    KINSLAYER_RULE,
    REGICIDE_RULE,
    BREACH_OF_HOSPITALITY_RULE,
    TYRANT_RULE,
)
