"""
The Revenger's Tragedy — the encoded fabula (substrate skeleton).

Thomas Middleton (attrib.; long ascribed to Cyril Tourneur), performed
1606, printed 1607. The corpus's **seventh Aristotelian encoding**
(after Oedipus, Rashomon, Macbeth, Hamlet, Lear, Malfi) and its second
non-Shakespeare Jacobean tragedy after Webster's *Duchess*.

**Session 1 scope:** entities, canonical branches, prop
constructors, event helpers, FABULA (the canonical spine — 31 events
from the nine-years-prior poisoning of Gloriana through the masque
killings and Vindice's confession-and-execution), and zero derivation
rules. Knowledge effects authored only on the load-bearing deception /
recognition beats — the Piato disguise, the bedroom misdirection, the
execution mix-up, the poisoned-skull deception, the corpse-swap, and
Vindice's fatal confession. The Aristotelian overlay (mythos, phases,
characters, the OQ-pressures) lands in the sibling module
`revengers_tragedy_aristotelian.py` (Session 2).

**Session 3 scope (this file):** PREPLAY_DISCLOSURES (5 facts the
opening soliloquy hands the audience — the poisoning of Gloriana and
the corrupt court's lineage), SJUZHET (28 in-play entries with
focalization; Vindice focalizes 13 — the arc-hero dominates — while the
pathos-cluster focalizes near-zero: Castiza 1, Gloriana 0, Antonio's
wife 0. **The focalization asymmetry is the OQ-MALFI-3 surface at the
substrate layer: the pathos-centre cannot focalize because she is dead
and a prop** — the structural inverse of Malfi, where the pathos-bearer
Duchess focalized 10), and DESCRIPTIONS (interpretive records covering
Vindice's moral register, Gloriana's skull as pathos-emblem, the
distributed-pathos and main-anagnorisis-register reader frames, the
Middletonian black-comedy tone, and Castiza's chastity).

This encoding is authored specifically to pressure a banked Malfi-arc
forcing function:

- **OQ-MALFI-3** — Pathos-hero vs arc-hero split. Surfaced by the
  Malfi Session-6 re-probe: when the principal site of pity-and-fear
  (the Duchess in Webster) and the character bearing the main
  anagnorisis (Ferdinand) are DIFFERENT, the Aristotelian dialect has
  no primitive naming the pathos-centre at the ArMythos level. The
  probe proposed `ArMythos.pathos_character_ref_id`. The Revenger's
  Tragedy is the second-site encoding, and it presses the question
  HARDER than Malfi:

  * **Arc-hero / main anagnorisis = Vindice.** His fortune reverses
    through hamartia (revenge curdles into relish for killing), and
    his recognition is the self-undoing confession to Antonio — "'Tis
    time to die when we are our own foes." He recognises, too late,
    that his own cleverness damns him. The recognition is *belated /
    self-destroying*, so it may also press A20's anti/partial
    `anagnorisis_qualifier`.

  * **Pathos-centre ≠ Vindice.** The pity-and-fear pools not on the
    morally-compromised avenger but on the violated women — Gloriana
    (poisoned by the Duke nine years before, for refusing his lust),
    Antonio's wife (raped by the Duchess's youngest son, then suicide,
    the on-stage "house of mourning"), and the threatened Castiza
    (subjected to Vindice's own corruption-test).

  * **The sharp twist (stronger than Malfi).** Malfi's pathos-bearer
    (the Duchess) is a *living agent* who dies mid-play. The Revenger's
    emblematic pathos-bearer — **Gloriana** — is *dead before the play
    opens and present only as a skull-prop* that Vindice addresses and
    ultimately weaponises (the Duke kisses the poisoned skull and
    dies). So `pathos_character_ref_id` here would point at a figure
    who is not a living agent in the fabula at all — pressuring whether
    the field admits a non-agentive / absent / displaced pathos-centre,
    or whether a single ref id even suffices for a distributed
    violated-women cluster. Session 2 will make the pathos-centre
    authoring decision and bank the sub-question.

  This is the same "denser second site" dynamic that made Malfi the
  right OQ-LEAR-4 forcer: Lear surfaced the pressure with one subplot;
  Malfi pressed it with four arc-peripeteiai; here OQ-MALFI-3's
  pathos/arc split is pressed by a pathos-centre that is dead, a prop,
  and arguably plural.

- **OQ-MALFI-4 (related, banked)** — instrument-reversal event. Bosola
  turned on his wielders in Malfi; the Revenger's instrument-character
  question is different (Vindice is a self-directed avenger, not a
  wielded instrument), so OQ-MALFI-4 is not strongly re-pressured here.
  Noted for Session 2 to confirm.

- **A20 anti/partial anagnorisis (sketch-06, possible re-pressure).**
  Vindice's terminal recognition is self-undoing; whether it reads as
  `genuine`, `anti`, or `partial` is a Session-2 overlay call.

Encoding choices (explicit, so future readers understand the slice):

- **Branches: canonical only.** No contested-testimony structure; the
  text is what it is. No Rashomon-style branching.

- **Vindice's disguise.** Vindice operates as "Piato" through Acts
  I-IV. The alias is authored as a substrate fact `disguised_as(
  vindice, "piato")` from E_vindice_hired_as_piato; knowledge of the
  identity Piato=Vindice is the load-bearing epistemic asymmetry the
  plot turns on (Lussurioso never learns it; he later hires the
  *undisguised* Vindice to murder "Piato"). When the disguise is
  shed (E_vindice_hired_as_himself) the substrate identity does not
  change — only who-believes-what.

- **Gloriana as entity.** Gloriana is authored as a `kind="agent"`
  entity though she is dead before the play; `dead(gloriana)` is
  asserted at her pre-play poisoning. She must be a referenceable
  ArCharacter for the Session-2 OQ-MALFI-3 pathos-centre decision.
  Her skull is an instrument authored as a substrate fact
  (`poisoned_skull`), following the Malfi convention (the dead hand,
  the waxworks, the poisoned book are predicates, not Entity records).

- **Antonio's wife.** Unnamed in the text; entity id `antonio_wife`,
  display name "Antonio's wife." Her rape (by Junior Brother) and
  suicide are the play's living pathos beat. Authored as an agent so
  she can serve the pathos cluster in Session 2.

- **The Duchess's three sons.** Ambitioso (eldest), Supervacuo
  (middle), and Junior Brother (youngest) are her sons by a former
  marriage; the Duke is their stepfather. Junior rapes Antonio's wife;
  Ambitioso and Supervacuo engineer (by accident) Junior's execution
  while trying to kill their stepbrother Lussurioso.

- **Compressed minor characters.** Lussurioso's servants (Nencio,
  Sordido), Castiza's clown-servant Dondolo, the officers/judges, and
  the masquers are compressed into the events they enable; no entity
  records. Piero (a discontented lord) IS authored — he carries the
  noble-faction-revenge payload alongside Antonio.

- **The court is unnamed.** Webster-style: the Italian dukedom has no
  proper name in the text. `the_court` is the locus; `lodge` is the
  darkened meeting-place where the Duke is murdered; `prison` and
  `vindice_house` complete the set.

- **Time scale.** Gloriana's poisoning is "nine years before" — a deep
  standing fact at τ_s=-90 (the nine-year gap made legible). Other
  standing facts cluster τ_s=-40..-20; the in-play action runs
  τ_s=0..22, with Act V compressing aggressively as in Malfi.

Story content only. No substrate logic. Parallels `malfi.py`,
`hamlet.py`, and `lear.py` in shape.
"""

from __future__ import annotations

from story_engine.core.substrate import (
    Entity, Prop, Event,
    CANONICAL, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
    Description, Attention, DescStatus, anchor_event,
)


# ----------------------------------------------------------------------------
# Entities
# ----------------------------------------------------------------------------

# --- Vindice's family (the revengers) ---
vindice   = Entity(id="vindice",   name="Vindice (disguised as Piato)",
                   kind="agent")
hippolito = Entity(id="hippolito", name="Hippolito, his brother",
                   kind="agent")
castiza   = Entity(id="castiza",   name="Castiza, their sister",
                   kind="agent")
gratiana  = Entity(id="gratiana",  name="Gratiana, their widowed mother",
                   kind="agent")

# --- The Duke's household ---
duke       = Entity(id="duke",       name="the Duke",
                    kind="agent")
duchess    = Entity(id="duchess",    name="the Duchess (the Duke's second wife)",
                    kind="agent")
lussurioso = Entity(id="lussurioso", name="Lussurioso, the Duke's heir",
                    kind="agent")
spurio     = Entity(id="spurio",     name="Spurio, the Duke's bastard",
                    kind="agent")

# --- The Duchess's sons by a former marriage ---
ambitioso  = Entity(id="ambitioso",  name="Ambitioso, the Duchess's eldest son",
                    kind="agent")
supervacuo = Entity(id="supervacuo", name="Supervacuo, the Duchess's middle son",
                    kind="agent")
junior     = Entity(id="junior",     name="Junior Brother, the Duchess's youngest son",
                    kind="agent")

# --- The wronged nobles ---
antonio      = Entity(id="antonio",      name="Antonio, a discontented lord",
                      kind="agent")
antonio_wife = Entity(id="antonio_wife", name="Antonio's wife",
                      kind="agent")
piero        = Entity(id="piero",        name="Piero, a discontented lord",
                      kind="agent")

# --- The dead beloved (present only as a skull) ---
gloriana = Entity(id="gloriana",
                  name="Gloriana, Vindice's poisoned betrothed",
                  kind="agent")

# --- Locations ---
the_court     = Entity(id="the_court",     name="the ducal court",
                       kind="location")
vindice_house = Entity(id="vindice_house", name="Vindice and Gratiana's house",
                       kind="location")
prison        = Entity(id="prison",        name="the court prison",
                       kind="location")
lodge         = Entity(id="lodge",         name="the darkened lodge",
                       kind="location")


ENTITIES = [
    # The revengers
    vindice, hippolito, castiza, gratiana,
    # The Duke's household
    duke, duchess, lussurioso, spurio,
    # The Duchess's sons
    ambitioso, supervacuo, junior,
    # The wronged nobles
    antonio, antonio_wife, piero,
    # The dead beloved
    gloriana,
    # Locations
    the_court, vindice_house, prison, lodge,
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
# Structural predicates (substrate-sketch-05 M1) — typed queries. The
# moral / affective register (is Vindice a justified avenger or a
# corrupted murderer; is Gloriana a martyr or a memento mori; is
# Castiza's chastity heroic or schematic) lives on descriptions
# (Session 3).


def sovereign(who: str) -> Prop:
    # The Duke is sovereign(duke) — the unnamed dukedom's ruler.
    # Lussurioso becomes sovereign(lussurioso) at his accession; Antonio
    # becomes sovereign(antonio) at the close. The realm is unnamed.
    return Prop("sovereign", (who,))

def consort_of(a: str, b: str) -> Prop:
    # The Duchess is consort_of(duchess, duke) — the Duke's second wife.
    # Distinct from sovereign: she rules nothing in her own right.
    return Prop("consort_of", (a, b))

def heir_of(heir: str, of: str) -> Prop:
    # Lussurioso heir_of(lussurioso, duke) — the Duke's son by his
    # first marriage and named successor.
    return Prop("heir_of", (heir, of))

def bastard_of(child: str, parent: str) -> Prop:
    # Spurio bastard_of(spurio, duke) — the Duke's illegitimate son,
    # who resents his exclusion and beds the Duchess in revenge.
    return Prop("bastard_of", (child, parent))

def stepson_of(child: str, parent: str) -> Prop:
    # The Duchess's three sons are stepson_of(_, duke). Their
    # blood-mother is the Duchess; the Duke is their stepfather by her
    # second marriage.
    return Prop("stepson_of", (child, parent))

def son_of(child: str, parent: str) -> Prop:
    # Blood parentage. The Duchess's three sons son_of(_, duchess).
    return Prop("son_of", (child, parent))

def sibling_of(a: str, b: str) -> Prop:
    # Symmetric; authored both directions where used. Vindice/Hippolito/
    # Castiza are pairwise siblings; Ambitioso/Supervacuo/Junior are
    # pairwise siblings. Shape-only.
    return Prop("sibling_of", (a, b))

def widow(who: str) -> Prop:
    # Gratiana is widow(gratiana) — Vindice's father is dead before the
    # play; the family's reduced fortune is part of their discontent.
    return Prop("widow", (who,))

def betrothed(a: str, b: str) -> Prop:
    # Vindice betrothed(vindice, gloriana) — nine years before the play.
    # The bond the Duke's poisoning of Gloriana severs and Vindice's
    # revenge answers.
    return Prop("betrothed", (a, b))

def chaste(who: str) -> Prop:
    # Castiza is chaste(castiza); Gloriana was chaste(gloriana) (she
    # refused the Duke, and was poisoned for it). The play's pathos
    # cluster turns on assaulted chastity.
    return Prop("chaste", (who,))

def lusts_after(who: str, whom: str) -> Prop:
    # The Duke lusted after Gloriana (pre-play). Lussurioso lusts after
    # Castiza (the procurement plot). The Duke's lust drives the
    # poisoning; Lussurioso's drives the Piato commission.
    return Prop("lusts_after", (who, whom))

def at_location(who: str, where: str) -> Prop:
    return Prop("at_location", (who, where))

def disguised_as(who: str, alias: str) -> Prop:
    # Vindice disguised_as(vindice, "piato"). The load-bearing epistemic
    # asymmetry of Acts I-IV. The substrate identity never changes; the
    # disguise governs only who-believes-what (see the KnowledgeEffects
    # on the hiring beats). When Vindice serves Lussurioso undisguised
    # (E_vindice_hired_as_himself) this fact is retracted.
    return Prop("disguised_as", (who, alias))

def procurer(agent: str, employer: str) -> Prop:
    # Vindice-as-Piato serves as procurer(vindice, lussurioso) (to win
    # Castiza) and later procurer(vindice, duke) (for the Duke's own
    # assignation — the trap that kills him). The archetypal corrupt-
    # service relation; Session 2 may read it as an instrumental shape.
    return Prop("procurer", (agent, employer))

def adultery(a: str, b: str) -> Prop:
    # Spurio + the Duchess. Authored as a substrate fact so the Duke's
    # death-scene (forced to watch them) can read as recognition.
    return Prop("adultery", (a, b))

def raped(victim: str, by: str) -> Prop:
    # Antonio's wife, by Junior Brother, at the court revels. The crime
    # the Duke declines to punish — the play's opening injustice.
    return Prop("raped", (victim, by))

def poisoned_skull(of: str) -> Prop:
    # Gloriana's skull, dressed and poisoned by Vindice — the instrument
    # that kills the Duke. Predicate, not an Entity record (Malfi
    # instrument convention).
    return Prop("poisoned_skull", (of,))

def in_the_dark(at: str) -> Prop:
    # The lodge is darkened for the Duke's assignation; he cannot see
    # that the "lady" is a poisoned skull, nor that his murderers stand
    # by. Supports the deception-recognition reading.
    return Prop("in_the_dark", (at,))

def warrant_against(orderer: str, victim: str) -> Prop:
    # The Duke's execution warrant against Lussurioso, handed to
    # Ambitioso and Supervacuo. The countermanding release is authored
    # as a separate fact (released).
    return Prop("warrant_against", (orderer, victim))

def released(who: str) -> Prop:
    # The Duke secretly releases Lussurioso — the countermand the
    # brothers never learn of, which turns their warrant onto Junior.
    return Prop("released", (who,))

def lusts_avenged(avenger: str, against: str) -> Prop:
    # Marks the completion of a revenge strand: Vindice against the Duke
    # at E_duke_killed_by_skull; the revengers against Lussurioso at the
    # masque. Structural bookkeeping for Session 2's peripeteia mapping.
    return Prop("lusts_avenged", (avenger, against))

def ordered_killing(orderer: str, victim: str) -> Prop:
    # Lussurioso orders Piato killed (E_lussurioso_orders_piato_killed).
    # Ambitioso + Supervacuo's warrant-rush is an ordered killing of
    # Lussurioso that miscarries onto Junior.
    return Prop("ordered_killing", (orderer, victim))

def killed(killer: str, victim: str) -> Prop:
    # Direct-action substrate fact. Vindice (+ Hippolito) kill the Duke
    # and Lussurioso; the officers execute Junior; the second masque-
    # group kill each other; Antonio's officers execute Vindice +
    # Hippolito.
    return Prop("killed", (killer, victim))

def executed(who: str) -> Prop:
    # Judicial / sanctioned death: Junior (by mistake), and Vindice +
    # Hippolito (by Antonio's order at the close).
    return Prop("executed", (who,))

def suicide(who: str) -> Prop:
    # Antonio's wife, in shame after the rape.
    return Prop("suicide", (who,))

def dead(who: str) -> Prop:
    return Prop("dead", (who,))

def poisoned(who: str) -> Prop:
    # Gloriana (pre-play, by the Duke); the Duke (by Gloriana's skull).
    return Prop("poisoned", (who,))


# ----------------------------------------------------------------------------
# Event helpers — same pattern as malfi.py / hamlet.py / lear.py.
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

def believe_false(agent_id: str, p: Prop, τ: int, note: str = "") -> KnowledgeEffect:
    # A deception beat: the agent acquires a BELIEVED-slot held that does
    # not match the world. Used for Lussurioso's bedroom misdirection,
    # the brothers' execution mix-up, and the Duke's skull deception.
    return KnowledgeEffect(
        agent_id=agent_id,
        held=Held(
            prop=p, slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
            via=Diegetic.INFERENCE.value,
            provenance=(f"deceived @ τ_s={τ}{(': ' + note) if note else ''}",),
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
# Fabula — all events on :canonical, status=committed by default.
# ----------------------------------------------------------------------------
#
# τ_s convention:
#   - τ_s = -90      : the nine-years-prior poisoning of Gloriana
#   - τ_s = -40..-20 : standing facts (court lineage, Vindice's family,
#                      the betrothal, Spurio's bastardy)
#   - τ_s = 0..4     : Act I (the skull soliloquy, the Piato plan, the
#                      rape + trial, Antonio's wife's suicide)
#   - τ_s = 5..8     : Act II (the corruption-test, the bedroom trap,
#                      the warrant)
#   - τ_s = 9..13    : Act III (the execution mix-up, the Duke's murder)
#   - τ_s = 14..15   : Act IV (Piato condemned, Vindice hired undisguised,
#                      the corpse-swap, Gratiana's repentance)
#   - τ_s = 16..22   : Act V (the body discovered, the masque, the
#                      mutual slaughter, the confession, the execution)

FABULA = [

    # --- Pre-play: the wound that starts everything (τ_s = -90) ---

    Event(
        id="E_gloriana_poisoned",
        type="standing",
        τ_s=-90, τ_a=1,
        participants={"killer": "duke", "victim": "gloriana",
                      "betrothed": "vindice"},
        effects=(
            # Nine years before the play, the Duke poisons Gloriana for
            # refusing his lust. The originating crime; Vindice has kept
            # her skull ever since. The pathos-centre of the play is
            # established here — dead before the action begins.
            world(betrothed("vindice", "gloriana")),
            world(betrothed("gloriana", "vindice")),
            world(chaste("gloriana")),
            world(lusts_after("duke", "gloriana")),
            world(poisoned("gloriana")),
            world(dead("gloriana")),
            world(ordered_killing("duke", "gloriana")),
            world(killed("duke", "gloriana")),
            # Vindice knows who killed her and why — the knowledge that
            # becomes nine years of grief and the revenge motive.
            observe("vindice", killed("duke", "gloriana"), -90,
                    note="the wound Vindice carries, and the skull"),
        ),
    ),

    # --- Standing facts (τ_s = -40..-20) ---

    Event(
        id="E_court_lineage",
        type="standing",
        τ_s=-40, τ_a=2,
        participants={"duke": "duke", "duchess": "duchess",
                      "heir": "lussurioso", "bastard": "spurio"},
        effects=(
            # The corrupt court's structure. The Duke rules; his second
            # wife the Duchess brings three sons by a former marriage;
            # Lussurioso is his heir by his first marriage; Spurio is his
            # resented bastard.
            world(sovereign("duke")),
            world(consort_of("duchess", "duke")),
            world(heir_of("lussurioso", "duke")),
            world(bastard_of("spurio", "duke")),
            # The Duchess's three sons: blood-sons of the Duchess,
            # stepsons of the Duke.
            world(son_of("ambitioso", "duchess")),
            world(son_of("supervacuo", "duchess")),
            world(son_of("junior", "duchess")),
            world(stepson_of("ambitioso", "duke")),
            world(stepson_of("supervacuo", "duke")),
            world(stepson_of("junior", "duke")),
            world(sibling_of("ambitioso", "supervacuo")),
            world(sibling_of("supervacuo", "ambitioso")),
            world(sibling_of("ambitioso", "junior")),
            world(sibling_of("junior", "ambitioso")),
            world(sibling_of("supervacuo", "junior")),
            world(sibling_of("junior", "supervacuo")),
        ),
    ),

    Event(
        id="E_vindice_family",
        type="standing",
        τ_s=-35, τ_a=3,
        participants={"avenger": "vindice", "brother": "hippolito",
                      "sister": "castiza", "mother": "gratiana"},
        effects=(
            # Vindice's family: three siblings and their widowed mother.
            # Their father is dead; the family's reduced fortune feeds
            # their discontent (Hippolito serves at the corrupt court).
            world(sibling_of("vindice", "hippolito")),
            world(sibling_of("hippolito", "vindice")),
            world(sibling_of("vindice", "castiza")),
            world(sibling_of("castiza", "vindice")),
            world(sibling_of("hippolito", "castiza")),
            world(sibling_of("castiza", "hippolito")),
            world(son_of("vindice", "gratiana")),
            world(son_of("hippolito", "gratiana")),
            world(widow("gratiana")),
            world(chaste("castiza")),
        ),
    ),

    # --- Act I (τ_s = 0..4) ---

    Event(
        id="E_vindice_skull_soliloquy",
        type="scene",
        τ_s=0, τ_a=4,
        participants={"avenger": "vindice"},
        effects=(
            # Act I.i. Vindice, holding Gloriana's skull, watches the
            # ducal train pass and names the court's corruptions. The
            # play opens inside his grief and resolve. The skull is
            # already the instrument-in-waiting.
            world(poisoned_skull("gloriana")),
            world(at_location("vindice", "the_court")),
        ),
    ),

    Event(
        id="E_hippolito_brings_commission",
        type="scene",
        τ_s=1, τ_a=5,
        participants={"avenger": "vindice", "brother": "hippolito",
                      "target_lord": "lussurioso"},
        effects=(
            # Act I.i. Hippolito reports that Lussurioso seeks a procurer
            # to win a virgin he lusts after. The brothers seize it as
            # the way in: Vindice will take the disguise of "Piato."
            world(lusts_after("lussurioso", "castiza")),
            observe("vindice", lusts_after("lussurioso", "castiza"), 1,
                    via=Diegetic.UTTERANCE_HEARD.value,
                    note="Hippolito's report; the way into the court"),
        ),
    ),

    Event(
        id="E_junior_rapes_antonio_wife",
        type="scene",
        τ_s=1, τ_a=6,
        participants={"ravisher": "junior", "victim": "antonio_wife"},
        effects=(
            # Act I.ii (offstage, just before the trial). The Duchess's
            # youngest son rapes Antonio's virtuous wife at the court
            # revels. The play's living atrocity — the pathos beat that
            # is on-stage, as against Gloriana's pre-play one.
            world(raped("antonio_wife", "junior")),
            world(chaste("antonio_wife")),
        ),
    ),

    Event(
        id="E_junior_trial",
        type="scene",
        τ_s=2, τ_a=7,
        participants={"accused": "junior", "judge": "duke",
                      "duchess": "duchess", "bastard": "spurio"},
        effects=(
            # Act I.ii. Junior is arraigned for the rape; the Duke
            # suspends judgment rather than condemn his stepson. The
            # Duchess, slighted, vows to cuckold the Duke; Spurio agrees
            # to be her lover (his revenge for his bastardy).
            world(adultery("spurio", "duchess")),
            world(adultery("duchess", "spurio")),
            # Antonio and Piero witness the court's refusal of justice —
            # the seed of the noble faction's revenge.
            observe("antonio", raped("antonio_wife", "junior"), 2,
                    note="the rape the court will not punish"),
            observe("piero", raped("antonio_wife", "junior"), 2),
        ),
    ),

    Event(
        id="E_vindice_hired_as_piato",
        type="scene",
        τ_s=3, τ_a=8,
        participants={"avenger": "vindice", "employer": "lussurioso"},
        effects=(
            # Act I.iii. Disguised as "Piato," Vindice is hired by
            # Lussurioso as procurer; the target is named — Castiza,
            # Vindice's own sister. Vindice resolves to test his mother
            # and sister. The disguise begins; Lussurioso never learns
            # Piato is Vindice (the asymmetry that runs to Act V).
            world(disguised_as("vindice", "piato")),
            world(procurer("vindice", "lussurioso")),
            # Lussurioso believes "Piato" a stranger-pander.
            believe_false("lussurioso", procurer("piato", "lussurioso"), 3,
                          note="Lussurioso never learns Piato is Vindice"),
        ),
    ),

    Event(
        id="E_antonio_wife_suicide",
        type="scene",
        τ_s=3, τ_a=9,
        participants={"victim": "antonio_wife"},
        effects=(
            # Between I.ii and I.iv. Shamed and unavenged, Antonio's wife
            # takes her own life.
            world(suicide("antonio_wife")),
            world(dead("antonio_wife")),
        ),
    ),

    Event(
        id="E_antonio_displays_corpse",
        type="scene",
        τ_s=4, τ_a=10,
        participants={"husband": "antonio", "lord": "piero",
                      "brother": "hippolito", "victim": "antonio_wife"},
        effects=(
            # Act I.iv. Antonio displays his wife's body to the
            # discontented lords; over the corpse they swear revenge on
            # the Duchess's son and the court. The "house of mourning."
            observe("antonio", dead("antonio_wife"), 4),
            observe("piero", dead("antonio_wife"), 4),
            observe("hippolito", dead("antonio_wife"), 4),
        ),
    ),

    # --- Act II (τ_s = 5..8) ---

    Event(
        id="E_vindice_tests_castiza",
        type="scene",
        τ_s=5, τ_a=11,
        participants={"tempter": "vindice", "sister": "castiza",
                      "mother": "gratiana"},
        effects=(
            # Act II.i. "Piato" tempts Castiza with Lussurioso's gold;
            # she refuses fiercely (and boxes his ear). Then he tempts
            # Gratiana — and the mother yields, agreeing to bawd her own
            # daughter. The corruption-test bifurcates: chastity holds,
            # motherhood breaks.
            world(chaste("castiza")),
            observe("vindice", chaste("castiza"), 5,
                    note="the test confirms her; the relief and horror"),
        ),
    ),

    Event(
        id="E_gratiana_yields",
        type="scene",
        τ_s=5, τ_a=12,
        participants={"tempter": "vindice", "mother": "gratiana"},
        effects=(
            # Act II.i. Gratiana takes the bribe — the play's bleakest
            # private beat for Vindice (his own mother). Marked as a
            # world fact so the Act-IV repentance can retract it.
            world(Prop("corrupted", ("gratiana",))),
        ),
    ),

    Event(
        id="E_vindice_false_report_to_lussurioso",
        type="scene",
        τ_s=6, τ_a=13,
        participants={"avenger": "vindice", "employer": "lussurioso"},
        effects=(
            # Act II.ii. "Piato" tells Lussurioso that Castiza is
            # weakening — feeding the lust to keep the access. Lussurioso
            # resolves to take her "within this hour."
            believe_false("lussurioso", Prop("yielding", ("castiza",)), 6,
                          note="Piato's false encouragement"),
        ),
    ),

    Event(
        id="E_bedroom_misdirection",
        type="scene",
        τ_s=7, τ_a=14,
        participants={"avenger": "vindice", "heir": "lussurioso",
                      "duke": "duke", "duchess": "duchess",
                      "bastard": "spurio"},
        effects=(
            # Act II.ii-iii. The trick: "Piato" sends Lussurioso to
            # surprise Spurio in the Duchess's bed — but it is the DUKE,
            # lawfully bedded with the Duchess, whom Lussurioso bursts in
            # upon, sword drawn. Lussurioso is seized for treason
            # (threatening his father's life).
            believe_false("lussurioso", adultery("spurio", "duchess"), 7,
                          note="led to expect Spurio; finds the Duke"),
            world(Prop("arrested", ("lussurioso",))),
        ),
    ),

    Event(
        id="E_duke_warrant_and_secret_release",
        type="scene",
        τ_s=8, τ_a=15,
        participants={"duke": "duke", "heir": "lussurioso",
                      "elder_son": "ambitioso", "middle_son": "supervacuo"},
        effects=(
            # Act II.iii. The Duke hands Ambitioso and Supervacuo a
            # warrant for Lussurioso's execution — then secretly signs a
            # countermanding release. The brothers (who want Lussurioso
            # dead so they may inherit) never learn of the release: the
            # hinge of the Act-III mix-up.
            world(warrant_against("duke", "lussurioso")),
            world(released("lussurioso")),
            # The brothers believe the warrant still stands and that
            # they are hastening Lussurioso to the block.
            believe_false("ambitioso", warrant_against("duke", "lussurioso"), 8,
                          note="ignorant of the secret release"),
            believe_false("supervacuo", warrant_against("duke", "lussurioso"), 8),
        ),
    ),

    # --- Act III (τ_s = 9..13) ---

    Event(
        id="E_brothers_rush_warrant",
        type="scene",
        τ_s=9, τ_a=16,
        participants={"elder_son": "ambitioso", "middle_son": "supervacuo"},
        effects=(
            # Act III.i-iii. Ambitioso and Supervacuo race the warrant to
            # the prison, urging instant execution — believing they speed
            # Lussurioso's death and their own advancement.
            world(ordered_killing("ambitioso", "lussurioso")),
            world(ordered_killing("supervacuo", "lussurioso")),
        ),
    ),

    Event(
        id="E_junior_executed_by_mistake",
        type="scene",
        τ_s=10, τ_a=17,
        participants={"victim": "junior", "elder_son": "ambitioso",
                      "middle_son": "supervacuo", "heir": "lussurioso"},
        effects=(
            # Act III.iii-iv. Lussurioso is already freed; the officers,
            # holding the warrant and the brothers' frantic urging, behead
            # the only nobleman left in the cell — Junior Brother, the
            # brothers' own youngest. Their plot recoils onto their blood.
            world(executed("junior")),
            world(dead("junior")),
            # The officers execute; the brothers caused it via their
            # warrant-rush. Causation, not direct action — ordered_killing,
            # matching the malfi.py order-vs-act distinction.
            world(ordered_killing("ambitioso", "junior")),
            world(ordered_killing("supervacuo", "junior")),
        ),
    ),

    Event(
        id="E_duke_lured_to_lodge",
        type="scene",
        τ_s=11, τ_a=18,
        participants={"avenger": "vindice", "duke": "duke"},
        effects=(
            # Act III.v. The Duke, lusting still, hires "Piato" to procure
            # him a secret country lady for a darkened assignation at a
            # lodge. Vindice now serves the Duke as procurer — the trap.
            world(procurer("vindice", "duke")),
            world(at_location("duke", "lodge")),
            world(in_the_dark("lodge")),
            believe_false("duke", Prop("assignation", ("duke",)), 11,
                          note="expects a living lady at the lodge"),
        ),
    ),

    Event(
        id="E_duke_killed_by_skull",
        type="scene",
        τ_s=12, τ_a=19,
        participants={"avenger": "vindice", "brother": "hippolito",
                      "duke": "duke", "duchess": "duchess",
                      "bastard": "spurio", "betrothed": "gloriana"},
        effects=(
            # Act III.v. The central revenge. Vindice has dressed
            # Gloriana's poisoned skull as a masked lady; the Duke kisses
            # it in the dark and the poison takes his lips and tongue.
            # Vindice and Hippolito reveal themselves, name Gloriana, and
            # stab him — forcing him, dying, to watch the Duchess and
            # Spurio embrace. Nine years answered in one beat.
            world(poisoned("duke")),
            world(killed("vindice", "duke")),
            world(killed("hippolito", "duke")),
            world(dead("duke")),
            world(lusts_avenged("vindice", "duke")),
            # The Duke recognises, too late, who kills him and why — and
            # is made to recognise his wife's adultery in the same beat.
            observe("duke", killed("vindice", "duke"), 12,
                    note="recognition at the point of death; Gloriana named"),
            observe("duke", adultery("duchess", "spurio"), 12,
                    note="forced to watch as he dies"),
        ),
    ),

    Event(
        id="E_brothers_realize_junior_dead",
        type="scene",
        τ_s=13, τ_a=20,
        participants={"elder_son": "ambitioso", "middle_son": "supervacuo",
                      "heir": "lussurioso", "victim": "junior"},
        effects=(
            # Act III.vi. The brothers exult, certain Lussurioso is dead —
            # then Lussurioso enters alive, and the severed head they are
            # sent is their own brother's. Their recognition: the plot
            # devoured the wrong man.
            observe("ambitioso", dead("junior"), 13,
                    note="the head is Junior's; the plot recoiled"),
            observe("supervacuo", dead("junior"), 13),
            remove_held("ambitioso", warrant_against("duke", "lussurioso"),
                        Slot.BELIEVED, Confidence.BELIEVED, 13,
                        note="too late; Lussurioso lives"),
        ),
    ),

    # --- Act IV (τ_s = 14..15) ---

    Event(
        id="E_lussurioso_orders_piato_killed",
        type="scene",
        τ_s=14, τ_a=21,
        participants={"heir": "lussurioso", "brother": "hippolito",
                      "avenger": "vindice"},
        effects=(
            # Act IV.i. Lussurioso, suspicious of the meddling "Piato,"
            # orders him killed — and asks Hippolito to find him a new
            # servant. Hippolito offers his brother Vindice, undisguised:
            # Lussurioso will hire Vindice to murder "Piato" — i.e.
            # himself.
            world(ordered_killing("lussurioso", "vindice")),  # "Piato"
        ),
    ),

    Event(
        id="E_vindice_hired_as_himself",
        type="scene",
        τ_s=14, τ_a=22,
        participants={"avenger": "vindice", "heir": "lussurioso",
                      "brother": "hippolito"},
        effects=(
            # Act IV.ii. Vindice appears as himself and is engaged by
            # Lussurioso to kill "Piato." The disguise is shed; the
            # substrate identity is unchanged, but Lussurioso now holds
            # two beliefs about one man. The grim joke at the play's
            # structural centre: the avenger hired to murder his own
            # alias.
            world(disguised_as("vindice", "piato"), asserts=False),
            believe_false("lussurioso", Prop("distinct", ("vindice", "piato")), 14,
                          note="believes Vindice and Piato two men"),
        ),
    ),

    Event(
        id="E_corpse_dressed_as_piato",
        type="scene",
        τ_s=15, τ_a=23,
        participants={"avenger": "vindice", "brother": "hippolito",
                      "duke": "duke", "heir": "lussurioso"},
        effects=(
            # Act IV.ii. To satisfy the contract to "kill Piato," Vindice
            # and Hippolito dress the Duke's corpse in Piato's clothes.
            # When the body is found, the court will read it as Piato,
            # who murdered the Duke and fled in his victim's garments.
            believe_false("lussurioso", killed("vindice", "duke"), 15,
                          note="will read the disguised corpse as Piato's guilt"),
        ),
    ),

    Event(
        id="E_gratiana_repents",
        type="scene",
        τ_s=15, τ_a=24,
        participants={"avenger": "vindice", "brother": "hippolito",
                      "mother": "gratiana", "sister": "castiza"},
        effects=(
            # Act IV.iv. The brothers confront Gratiana with drawn daggers
            # over her willingness to bawd Castiza; she weeps and repents.
            # Castiza, who had feigned consent to test her mother, is
            # confirmed chaste. The one redemptive beat — retracts the
            # corruption from E_gratiana_yields.
            world(Prop("corrupted", ("gratiana",)), asserts=False),
            observe("vindice", chaste("castiza"), 15,
                    note="the mother reclaimed; the sister never fell"),
        ),
    ),

    # --- Act V (τ_s = 16..22) ---

    Event(
        id="E_duke_death_discovered",
        type="scene",
        τ_s=16, τ_a=25,
        participants={"heir": "lussurioso", "duke": "duke"},
        effects=(
            # Act V.i. The Duke's body is found (in Piato's clothes).
            # Lussurioso, blaming the absent "Piato," is proclaimed Duke.
            world(sovereign("lussurioso"), asserts=True),
            world(sovereign("duke"), asserts=False),
            observe("lussurioso", dead("duke"), 16),
        ),
    ),

    Event(
        id="E_revengers_plan_masque",
        type="scene",
        τ_s=17, τ_a=26,
        participants={"avenger": "vindice", "brother": "hippolito",
                      "lord": "antonio", "second_lord": "piero"},
        effects=(
            # Act V.ii. Vindice, Hippolito, Piero, and a fourth lord
            # resolve to dance the coronation masque and kill Lussurioso
            # and his favourites at the banquet. The noble revenge and
            # Vindice's revenge converge on one beat.
            observe("antonio", killed("vindice", "duke"), 17,
                    note="not yet — Antonio does not yet know who killed the Duke"),
        ),
    ),

    Event(
        id="E_lussurioso_killed_at_masque",
        type="scene",
        τ_s=18, τ_a=27,
        participants={"avenger": "vindice", "brother": "hippolito",
                      "heir": "lussurioso", "lord": "antonio"},
        effects=(
            # Act V.iii. The masque. As a blazing star crosses overhead,
            # the revengers' dance turns to murder: Lussurioso and his
            # nobles are stabbed at the feast. Vindice's triumph — and
            # the peripeteia's hinge, for the success is about to undo
            # him.
            world(killed("vindice", "lussurioso")),
            world(killed("hippolito", "lussurioso")),
            world(dead("lussurioso")),
            world(lusts_avenged("vindice", "lussurioso")),
        ),
    ),

    Event(
        id="E_second_masque_mutual_slaughter",
        type="scene",
        τ_s=19, τ_a=28,
        participants={"elder_son": "ambitioso", "middle_son": "supervacuo",
                      "bastard": "spurio"},
        effects=(
            # Act V.iii. The second masque-party — Ambitioso, Supervacuo,
            # Spurio — enters to claim the throne over the bodies, finds
            # the work done, and turns on itself: each kills the next in
            # the scramble for the crown. The court devours its own
            # remainder.
            world(killed("supervacuo", "ambitioso")),
            world(killed("spurio", "supervacuo")),
            world(dead("ambitioso")),
            world(dead("supervacuo")),
            world(dead("spurio")),
        ),
    ),

    Event(
        id="E_vindice_confesses",
        type="scene",
        τ_s=20, τ_a=29,
        participants={"avenger": "vindice", "brother": "hippolito",
                      "lord": "antonio"},
        effects=(
            # Act V.iii. Antonio, the last honest lord, is made Duke and
            # restores order. Vindice, unable to keep silent about so fine
            # a piece of work, whispers to Antonio that he and Hippolito
            # killed the old Duke. The boast that springs the trap on
            # himself.
            world(sovereign("antonio")),
            observe("antonio", killed("vindice", "duke"), 20,
                    note="Vindice's own confession — the fatal disclosure"),
            observe("antonio", killed("hippolito", "duke"), 20),
        ),
    ),

    Event(
        id="E_antonio_condemns_vindice",
        type="scene",
        τ_s=21, τ_a=30,
        participants={"lord": "antonio", "avenger": "vindice",
                      "brother": "hippolito"},
        effects=(
            # Act V.iii. Antonio answers at once: "You that would murder
            # him would murder me" — and sends the brothers to immediate
            # execution. Vindice's recognition lands in the same breath:
            # "'Tis time to die when we are our own foes." The avenger's
            # cleverness is his self-undoing; the anagnorisis is the
            # discovery that his own nature has condemned him.
            world(ordered_killing("antonio", "vindice")),
            world(ordered_killing("antonio", "hippolito")),
            observe("vindice", ordered_killing("antonio", "vindice"), 21,
                    note="the self-undoing recognition; he accepts it"),
        ),
    ),

    Event(
        id="E_vindice_executed",
        type="scene",
        τ_s=22, τ_a=31,
        participants={"avenger": "vindice", "brother": "hippolito",
                      "lord": "antonio"},
        effects=(
            # Act V.iii (close). Vindice and Hippolito are led off to
            # death; Antonio's rule begins over a swept-clean court. The
            # revenger's tragedy completes — the instrument of justice
            # destroyed by the same appetite that drove it.
            world(executed("vindice")),
            world(executed("hippolito")),
            world(dead("vindice")),
            world(dead("hippolito")),
        ),
    ),

]


# ----------------------------------------------------------------------------
# Session 3 — substrate completion: disclosures, sjuzhet, descriptions
# ----------------------------------------------------------------------------


# --- Preplay disclosures ---------------------------------------------------
#
# What Vindice's opening soliloquy (and the procession it watches) hands
# the audience at τ_d=0. The Revenger's Tragedy front-loads its
# motive: the very first speech, over the skull, tells us the Duke
# poisoned Gloriana for refusing his lust. Five disclosures — comparable
# to Lear's six, lighter than Hamlet's seven.

PREPLAY_DISCLOSURES = (
    # The wound that starts the play — Vindice names it in the first
    # speech, skull in hand.
    Disclosure(prop=betrothed("vindice", "gloriana"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=killed("duke", "gloriana"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    # The corrupt court's lineage — disclosed through the opening
    # procession Vindice anatomises.
    Disclosure(prop=sovereign("duke"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=heir_of("lussurioso", "duke"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=bastard_of("spurio", "duke"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
)


# --- Sjuzhet ----------------------------------------------------------------
#
# The three pre-play standing events (E_gloriana_poisoned τ_s=-90,
# E_court_lineage τ_s=-40, E_vindice_family τ_s=-35) are not staged;
# their content reaches the audience through PREPLAY_DISCLOSURES at
# τ_d=0 and the opening soliloquy. The 28 in-play events (τ_s=0..22)
# stage largely in fabula order — the play is linear; τ_d ≈ τ_s.
#
# Focalization distribution (28 in-play entries):
#   vindice:     13   (the arc-hero — soliloquies, the disguise, the
#                      tests, the lodge-trap, the central revenge, the
#                      masque, the fatal confession, the recognition)
#   lussurioso:   3   (the bedroom dupe; ordering Piato killed; his
#                      brief reign)
#   duke:         2   (the trial he corrupts; the warrant + secret
#                      release)
#   ambitioso:    2   (the warrant-rush; the recognition of the mix-up)
#   antonio:      2   (the house of mourning; the restored order)
#   hippolito:    1   (bringing Vindice the commission)
#   supervacuo:   1   (the prison mix-up)
#   castiza:      1   (resisting the corruption-test)
#   None:         3   (the offstage rape; the offstage suicide; the
#                      second masque-party's self-slaughter)
#
# **The OQ-MALFI-3 surface at the focalization layer.** Vindice (the
# arc-hero) focalizes 13 of 28; the pathos-cluster focalizes near-zero
# — Castiza 1, Gloriana 0, Antonio's wife 0. The pathos-centre CANNOT
# focalize: Gloriana is dead and a prop, Antonio's wife is violated
# offstage and shown only as a corpse. This is the structural inverse
# of Malfi, where the pathos-bearer (the Duchess) focalized 10 of 30 —
# there the pathos-centre WAS the focal protagonist; here the pathos
# and the focalization come apart completely. The asymmetry is the
# substrate-layer evidence for OQ-MALFI-3 (the pathos-centre is not the
# arc-hero) and for its non-agentive twist (the pathos-centre is not
# even a perceiver).

SJUZHET = [

    # τ_d=0 — Act I.i. Vindice alone with Gloriana's skull, anatomising
    # the ducal train as it passes. The play opens inside his grief and
    # resolve; PREPLAY_DISCLOSURES attach here.
    SjuzhetEntry(event_id="E_vindice_skull_soliloquy", τ_d=0,
                 focalizer_id="vindice", disclosures=PREPLAY_DISCLOSURES),

    # τ_d=1 — Act I.i. Hippolito brings word that Lussurioso seeks a
    # procurer. Hippolito focalizes the report.
    SjuzhetEntry(event_id="E_hippolito_brings_commission", τ_d=1,
                 focalizer_id="hippolito", disclosures=()),

    # τ_d=2 — Act I.ii (offstage atrocity). Junior rapes Antonio's wife
    # at the revels. Reported, not staged through any single POV.
    SjuzhetEntry(event_id="E_junior_rapes_antonio_wife", τ_d=2,
                 focalizer_id=None, disclosures=()),

    # τ_d=3 — Act I.ii. The arraignment. The Duke presides and suspends
    # judgment on his stepson; the Duchess vows revenge, Spurio pacts
    # with her. The Duke's corrupt authority focalizes.
    SjuzhetEntry(event_id="E_junior_trial", τ_d=3,
                 focalizer_id="duke",
                 disclosures=(
                     Disclosure(prop=raped("antonio_wife", "junior"),
                                slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                                via=Narrative.DISCLOSURE.value),
                 )),

    # τ_d=4 — Act I.iii. Vindice, disguised as Piato, is hired by
    # Lussurioso; Castiza is named. His POV — the disguise is his.
    SjuzhetEntry(event_id="E_vindice_hired_as_piato", τ_d=4,
                 focalizer_id="vindice", disclosures=()),

    # τ_d=5 — Act I.iv (offstage). Antonio's wife takes her own life.
    SjuzhetEntry(event_id="E_antonio_wife_suicide", τ_d=5,
                 focalizer_id=None, disclosures=()),

    # τ_d=6 — Act I.iv. The house of mourning: Antonio displays the
    # corpse; the lords swear revenge. Antonio focalizes his grief.
    SjuzhetEntry(event_id="E_antonio_displays_corpse", τ_d=6,
                 focalizer_id="antonio", disclosures=()),

    # τ_d=7 — Act II.i. The corruption-test of Castiza. Her fierce
    # resistance is the scene's pathos beat — she focalizes (the one
    # focal entry the pathos-cluster gets).
    SjuzhetEntry(event_id="E_vindice_tests_castiza", τ_d=7,
                 focalizer_id="castiza", disclosures=()),

    # τ_d=8 — Act II.i. Gratiana yields to the bribe. Vindice's horror
    # at his own mother focalizes the beat.
    SjuzhetEntry(event_id="E_gratiana_yields", τ_d=8,
                 focalizer_id="vindice", disclosures=()),

    # τ_d=9 — Act II.ii. Piato feeds Lussurioso false hope.
    SjuzhetEntry(event_id="E_vindice_false_report_to_lussurioso", τ_d=9,
                 focalizer_id="vindice", disclosures=()),

    # τ_d=10 — Act II.ii-iii. The bedroom misdirection. Lussurioso, the
    # dupe, bursts in on the Duke and is seized for treason — his POV.
    SjuzhetEntry(event_id="E_bedroom_misdirection", τ_d=10,
                 focalizer_id="lussurioso", disclosures=()),

    # τ_d=11 — Act II.iii. The Duke's cunning: the warrant and the
    # secret release. The Duke focalizes his own double-dealing.
    SjuzhetEntry(event_id="E_duke_warrant_and_secret_release", τ_d=11,
                 focalizer_id="duke", disclosures=()),

    # τ_d=12 — Act III.i. The brothers race the warrant, scheming.
    SjuzhetEntry(event_id="E_brothers_rush_warrant", τ_d=12,
                 focalizer_id="ambitioso", disclosures=()),

    # τ_d=13 — Act III.iii-iv. The prison mix-up; Junior is beheaded by
    # mistake. Supervacuo focalizes the brothers' grim error.
    SjuzhetEntry(event_id="E_junior_executed_by_mistake", τ_d=13,
                 focalizer_id="supervacuo", disclosures=()),

    # τ_d=14 — Act III.v. Vindice lures the Duke to the darkened lodge.
    SjuzhetEntry(event_id="E_duke_lured_to_lodge", τ_d=14,
                 focalizer_id="vindice", disclosures=()),

    # τ_d=15 — Act III.v. THE central revenge: the Duke kisses the
    # poisoned skull and is stabbed, made to watch the adultery as he
    # dies. Vindice's POV of triumph; the Duke's dying anti-recognition.
    SjuzhetEntry(event_id="E_duke_killed_by_skull", τ_d=15,
                 focalizer_id="vindice",
                 disclosures=(
                     Disclosure(prop=adultery("duchess", "spurio"),
                                slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                                via=Narrative.DISCLOSURE.value),
                 )),

    # τ_d=16 — Act III.vi. The brothers recognise the head is Junior's.
    SjuzhetEntry(event_id="E_brothers_realize_junior_dead", τ_d=16,
                 focalizer_id="ambitioso", disclosures=()),

    # τ_d=17 — Act IV.i. Lussurioso, suspicious, orders Piato killed.
    SjuzhetEntry(event_id="E_lussurioso_orders_piato_killed", τ_d=17,
                 focalizer_id="lussurioso", disclosures=()),

    # τ_d=18 — Act IV.ii. The grim joke: Vindice, undisguised, is hired
    # to murder "Piato." His POV.
    SjuzhetEntry(event_id="E_vindice_hired_as_himself", τ_d=18,
                 focalizer_id="vindice", disclosures=()),

    # τ_d=19 — Act IV.ii. The Duke's corpse dressed in Piato's clothes.
    SjuzhetEntry(event_id="E_corpse_dressed_as_piato", τ_d=19,
                 focalizer_id="vindice", disclosures=()),

    # τ_d=20 — Act IV.iv. The brothers bring Gratiana to repentance;
    # Castiza is confirmed chaste. Vindice's POV.
    SjuzhetEntry(event_id="E_gratiana_repents", τ_d=20,
                 focalizer_id="vindice", disclosures=()),

    # τ_d=21 — Act V.i. The Duke's body found; Lussurioso proclaimed
    # Duke, blaming the absent "Piato." His brief reign begins.
    SjuzhetEntry(event_id="E_duke_death_discovered", τ_d=21,
                 focalizer_id="lussurioso", disclosures=()),

    # τ_d=22 — Act V.ii. The revengers plan the coronation masque.
    SjuzhetEntry(event_id="E_revengers_plan_masque", τ_d=22,
                 focalizer_id="vindice", disclosures=()),

    # τ_d=23 — Act V.iii. The masque: Lussurioso and his nobles cut down
    # as the blazing star crosses. Vindice's triumph.
    SjuzhetEntry(event_id="E_lussurioso_killed_at_masque", τ_d=23,
                 focalizer_id="vindice", disclosures=()),

    # τ_d=24 — Act V.iii. The second masque-party finds the work done
    # and slaughters itself for the empty throne. Chaotic, multi-agent.
    SjuzhetEntry(event_id="E_second_masque_mutual_slaughter", τ_d=24,
                 focalizer_id=None, disclosures=()),

    # τ_d=25 — Act V.iii. Vindice, exhilarated, boasts to Antonio that
    # he killed the old Duke — the fatal confession. His POV.
    SjuzhetEntry(event_id="E_vindice_confesses", τ_d=25,
                 focalizer_id="vindice", disclosures=()),

    # τ_d=26 — Act V.iii. Antonio condemns him on the instant; Vindice's
    # self-undoing recognition lands ("'Tis time to die when we are our
    # own foes"). The peripeteia-and-anagnorisis beat; Vindice's POV
    # carries the recognition.
    SjuzhetEntry(event_id="E_antonio_condemns_vindice", τ_d=26,
                 focalizer_id="vindice", disclosures=()),

    # τ_d=27 — Act V.iii (close). Vindice and Hippolito led to death;
    # Antonio's order begins over the swept court.
    SjuzhetEntry(event_id="E_vindice_executed", τ_d=27,
                 focalizer_id="antonio", disclosures=()),

]


# --- Descriptions -----------------------------------------------------------
#
# Interpretive records: the moral/affective register the structural
# substrate leaves open. The headline frames carry the OQ-MALFI-3 and
# S6P-OQ1 reader questions the Session-5 probe will be invited to press.

DESCRIPTIONS = [

    Description(
        id="D_gloriana_skull_pathos_centre",
        attached_to=anchor_event("E_vindice_skull_soliloquy"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("Gloriana — poisoned nine years before the play for "
              "refusing the Duke, present on stage only as the skull "
              "Vindice addresses and finally weaponises — is the play's "
              "PATHOS-CENTRE: the emblem of its grief, the motive of "
              "its revenge, the instrument of its central murder. Yet "
              "the Aristotelian dialect has no field to mark her as "
              "such. `anagnorisis_character_ref_id` names the recognizer "
              "(Vindice); there is no `pathos_character_ref_id`. The "
              "pathos and the arc come wholly apart here — and harder "
              "than in Malfi, where the pathos-bearer (the Duchess) was "
              "the living title character and focal protagonist. "
              "Gloriana is dead, a prop, and unable even to focalize "
              "(0 sjuzhet entries). **This is the OQ-MALFI-3 forcing "
              "rendered at the reader-frame layer; see "
              "revengers_tragedy_aristotelian.OQ_MALFI_3_FINDING.**"),
        is_question=False,
        authored_by="author",
        τ_a=200,
    ),

    Description(
        id="D_pathos_distributed_cluster",
        attached_to=anchor_event("E_antonio_displays_corpse"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("The play's pity is not single but DISTRIBUTED across "
              "three violated women: Gloriana (poisoned for her "
              "chastity), Antonio's wife (raped and driven to suicide — "
              "the house of mourning staged here), and Castiza "
              "(threatened by Vindice's own corruption-test and "
              "holding). They share no arc — they are pity-objects, not "
              "agents — but together they carry the pathos the corroded "
              "avenger cannot. A single pathos ref could not name the "
              "cluster; this is the sub-question OQ-MALFI-3 raised about "
              "whether the field should be a tuple. Sketch-07 answered it: "
              "the overlay now names them in A22 "
              "`ArMythos.pathos_character_ref_ids` (a tuple), retiring the "
              "earlier overloaded arc-relation that gave the cluster its "
              "only footing."),
        is_question=False,
        authored_by="author",
        τ_a=201,
    ),

    Description(
        id="D_vindice_moral_register_undecided",
        attached_to=anchor_event("E_duke_killed_by_skull"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Vindice's first revenge — the poisoned-skull murder of "
              "the Duke — is the play's centre of moral gravity; what "
              "his whole arc MEANS is left open. Three readings the "
              "text supports: (a) JUST AVENGER CORRUPTED — Vindice "
              "begins with a true cause and is destroyed by the "
              "appetite the revenge feeds; the tragedy is the corrosion "
              "of justice into relish (the reading the hamartia_text "
              "leans toward). (b) ALWAYS-ALREADY DAMNED — Vindice's "
              "delight in cruelty (testing his own sister, the "
              "craftsman's pride in the skull-trick) was prior to the "
              "revenge; the cause is a pretext for a disposition. "
              "(c) SATIRIC INSTRUMENT — Middleton's morality-play "
              "machinery, where Vindice ('Revenge') is less a character "
              "than the vehicle of a savage civic satire, and his fall "
              "is the genre's bookkeeping, not a psychology. The "
              "substrate commits to none; the structural arc (revenge "
              "achieved, then self-undone by the confession) is what is "
              "asserted."),
        is_question=True,
        authored_by="author",
        τ_a=202,
    ),

    Description(
        id="D_vindice_anagnorisis_register_undecided",
        attached_to=anchor_event("E_antonio_condemns_vindice"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Vindice's terminal recognition — 'Tis time to die when "
              "we are our own foes' — is the main anagnorisis, but its "
              "register is open, and the dialect cannot type it: A20's "
              "`anagnorisis_qualifier` lives on chain steps, not on the "
              "mythos's main `anagnorisis_event_id` (S6P-OQ1). Is the "
              "recognition (a) GENUINE — a real, if belated, moral "
              "comprehension that he is his own foe; (b) ANTI — a "
              "recognition-too-late, arriving only as the confession "
              "seals his death, with no possibility of acting on it "
              "(the same too-late shape as the Duke's dying "
              "recognition, but at the main slot); or (c) PARTIAL — a "
              "wry, half-rueful acknowledgement of the joke rather than "
              "a full reckoning, in keeping with Middleton's tone? The "
              "self-destroying, belated quality is exactly what would "
              "force a main-level qualifier; see "
              "revengers_tragedy_aristotelian.S6P_OQ1_FINDING."),
        is_question=True,
        authored_by="author",
        τ_a=203,
    ),

    Description(
        id="D_duke_anti_recognition_frame",
        attached_to=anchor_event("E_duke_killed_by_skull"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("The Duke's recognition as he dies — learning, in one "
              "beat, who kills him (and why, nine years on) and that "
              "his wife embraces his bastard — is an ANTI-anagnorisis: "
              "real, complete, and wholly too late, the poison already "
              "mortal. The dialect types it with A20's "
              "`anagnorisis_qualifier='anti'` on the chain step "
              "AR_STEP_DUKE_DYING_RECOGNITION — the corpus's second "
              "anti-anagnorisis after Webster's Antonio, and a "
              "complementary shape: Antonio's was a victim's too-late "
              "recognition, the Duke's is a villain's. Confirms the "
              "sketch-06 A20 value generalises beyond its surfacing "
              "encoding."),
        is_question=False,
        authored_by="author",
        τ_a=204,
    ),

    Description(
        id="D_middleton_black_comedy_texture",
        attached_to=anchor_event("E_vindice_hired_as_himself"),
        kind="texture",
        attention=Attention.STRUCTURAL,
        text=("Middleton's tonal signature: a savage black comedy that "
              "runs under the tragedy without softening it. The skull "
              "dressed as a lady for a kiss; the avenger hired to "
              "murder his own alias; the brothers who behead their own "
              "youngest by overzealous scheming; the masque of "
              "murderers dancing in a second masque of murderers. The "
              "tonal_register is 'tragic-with-irony' (shared with "
              "Hamlet and Malfi) but colder and more grotesque than "
              "either — closer to structural farce than to reflexive "
              "wit. The comedy is part of the play's moral instrument: "
              "it makes the court's corruption ludicrous as well as "
              "lethal, and implicates the audience's relish alongside "
              "Vindice's."),
        is_question=False,
        authored_by="author",
        τ_a=205,
    ),

    Description(
        id="D_castiza_chastity_register_undecided",
        attached_to=anchor_event("E_vindice_tests_castiza"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Castiza ('chastity') resists the corruption-test "
              "absolutely — the one member of the pathos cluster who is "
              "threatened and holds. What her chastity IS dramatically "
              "is open: (a) HEROIC — a genuine moral centre against "
              "which the court's rot is measured, the play's one "
              "unfallen value; (b) SCHEMATIC — a morality-play emblem "
              "(her name is her function), less a character than a "
              "fixed point; (c) IRONISED — even Castiza wavers for a "
              "line under her mother's corrupted urging before "
              "recovering, so that the play tests whether ANY virtue is "
              "secure in this court. The substrate asserts only "
              "`chaste(castiza)` held across the test; the register is "
              "reader-side."),
        is_question=True,
        authored_by="author",
        τ_a=206,
    ),

    Description(
        id="D_binding_adjacent_register",
        attached_to=anchor_event("E_vindice_confesses"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("Vindice's peripeteia (the confession recoiling, τ_s=20) "
              "and his anagnorisis (the self-undoing recognition, "
              "τ_s=21) fall ONE beat apart — `peripeteia_anagnorisis_"
              "binding='adjacent'`, distance 1, the corpus's narrowest "
              "and the first use of the ADJACENT cell (Oedipus / Hamlet "
              "/ Lear / Malfi were SEPARATED; Macbeth COINCIDENT). The "
              "tightness is the point: the boast IS the reversal, and "
              "the recognition treads on its heel — Vindice undoes "
              "himself and knows it in almost the same breath. The "
              "structural compression is Middleton's, and the binding "
              "field now carries a cell the corpus had not exercised."),
        is_question=False,
        authored_by="author",
        τ_a=207,
    ),

    Description(
        id="D_revengers_unity_of_action",
        attached_to=anchor_event("E_junior_executed_by_mistake"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("The Duchess's-sons subplot (Ambitioso, Supervacuo, and "
              "the doomed Junior) reads as separable but is woven into "
              "the main action: Junior's rape of Antonio's wife is the "
              "injustice that arms the noble faction; the brothers' "
              "warrant-rush, recoiling onto their own youngest, is the "
              "court consuming itself and clearing Vindice's path. The "
              "encoding asserts `unity_of_action=True` (contrast Lear's "
              "False) — the subplot feeds the revenge rather than "
              "running a genuinely independent second plot. A reader "
              "could dispute this; the claim is that the Revenger's "
              "court is one organism devouring itself, not two plots "
              "braided."),
        is_question=False,
        authored_by="author",
        τ_a=208,
    ),

]
