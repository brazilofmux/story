"""
and_then_there_were_none.py — And Then There Were None substrate encoding.

Agatha Christie's *And Then There Were None* (1939). Sixth substrate
encoding in the corpus. First canonical whodunit (Ackroyd is the
inverted form). Encoded here for research-track pressure on several
banked forcing functions:

- Multi-suspect mystery with a concealed perpetrator inside the cast
  — different from Ackroyd's inverted-narrator pattern; pressures
  MN2 (concealment-asymmetry) for a multi-suspect variant.
- Discrete-elimination Timelock (ten-then-nine-then-eight-etc).
  Candidate vocabulary probe for pressure-shape-taxonomy: does
  elimination-shaped-Timelock register through the existing LT8/LT9
  machinery, or need a new predicate family?
- Ensemble cast (10 characters) — stresses Dramatica-8 function
  assignment across more bodies than function slots.

==============================================================================
Encoding decisions
==============================================================================

**Past crimes handled via WorldEffects at τ_s=5 (the gramophone).**
Each guest committed a past murder; Wargrave's framing device reveals
these during the accusation recording. Faithful encoding would place
each past-crime as an event at negative τ_s with knowledge-acquired
effects. For this encoding we take the lighter path: the past_killed
world facts are asserted by the gramophone event's WorldEffects,
matching the in-story moment of revelation. The facts are true from
τ_s=-∞ semantically; the substrate just doesn't carry proof of them
before τ_s=5. A follow-on arc could expand to explicit past-event
records if a verifier wants to claim about Wargrave's investigation
arc (pre-plot).

**Wargrave's unique knowledge.** The killer alone knows his identity
throughout. Other agents only learn at τ_s=18 (the epilogue's
message in a bottle). Most characters die without knowing who the
killer is — an asymmetry the encoding preserves:
`is_killer(wargrave)` world-asserts at τ_s=5 (the moment the plan
is in motion) but only Wargrave KNOWS it until the epilogue.

**Branch structure.** Canonical only. The novel asserts a single
reading via the epilogue confession; no contested narration.

**MC/IC deferred.** Two legitimate readings — Vera-as-MC (the
conventional read; she's the survivor whose mental collapse drives
the novel's emotional arc) vs. Wargrave-as-MC (subversive; the
killer's plan IS the Throughline). The substrate doesn't commit;
the Dramatic encoding (follow-on commit) chooses.

==============================================================================
Scale
==============================================================================

- 14 entities (10 human guests + mysterious invitation-sender
  "U. N. Owen" + soldier_island + mansion + gramophone as a record-
  carrying inanimate prop).
- 22 events across the fabula: arrivals (consolidated), dinner,
  gramophone, 10 deaths (Marston → Vera), epilogue confession.
- 4 descriptions: the gramophone's authorial texture, the soldiers-
  figurine-counting pattern, Wargrave's plan as Wargrave-internal
  belief, the epilogue-reveal as authorial commentary.
- 0 rules today. Christie's accused→guilty link is a judgment,
  not a structural derivation; the Dramatica layer carries the
  authorial-intent claim about culpability.
"""
from __future__ import annotations

from story_engine.core.substrate import (
    Entity, Event, Prop,
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

# Ten human guests (order of death matches the novel's sequence).
wargrave = Entity(id="wargrave", name="Justice Wargrave", kind="agent")
vera = Entity(id="vera", name="Vera Claythorne", kind="agent")
lombard = Entity(id="lombard", name="Philip Lombard", kind="agent")
emily = Entity(id="emily", name="Emily Brent", kind="agent")
macarthur = Entity(id="macarthur", name="General Macarthur", kind="agent")
armstrong = Entity(id="armstrong", name="Dr Armstrong", kind="agent")
blore = Entity(id="blore", name="William Blore", kind="agent")
marston = Entity(id="marston", name="Anthony Marston", kind="agent")
rogers = Entity(id="rogers", name="Thomas Rogers", kind="agent")
mrs_rogers = Entity(id="mrs_rogers", name="Ethel Rogers", kind="agent")

# The fictitious host. "U. N. Owen" = "Unknown" — the invitation
# identity. The reader-level identity with Wargrave is revealed in
# the epilogue; the substrate carries the identity assertion
# anchored at that event.
un_owen = Entity(id="un_owen", name="U. N. Owen", kind="agent")

# Non-agent entities for setting + props.
soldier_island = Entity(id="soldier_island", name="Soldier Island", kind="location")
mansion = Entity(id="mansion", name="the mansion on Soldier Island", kind="location")
gramophone = Entity(id="gramophone", name="the gramophone", kind="object")

ENTITIES = [
    wargrave, vera, lombard, emily, macarthur,
    armstrong, blore, marston, rogers, mrs_rogers,
    un_owen,
    soldier_island, mansion, gramophone,
]


# ----------------------------------------------------------------------------
# Proposition constructors
# ----------------------------------------------------------------------------

# Setting / presence.
def on_island(who: str) -> Prop:
    return Prop("on_island", (who,))

def at_mansion(who: str) -> Prop:
    return Prop("at_mansion", (who,))


# Life / death.
def alive(who: str) -> Prop:
    return Prop("alive", (who,))

def dead(who: str) -> Prop:
    return Prop("dead", (who,))


# Killing modalities — each death in the novel follows a specific
# nursery-rhyme manner. Encoded as distinct predicates so a verifier
# can surface the pattern.
def poisoned(who: str) -> Prop:
    return Prop("poisoned", (who,))

def drowned(who: str) -> Prop:
    return Prop("drowned", (who,))

def shot(who: str) -> Prop:
    return Prop("shot", (who,))

def hanged(who: str) -> Prop:
    return Prop("hanged", (who,))

def axed(who: str) -> Prop:
    return Prop("axed", (who,))

def struck_head(who: str) -> Prop:
    return Prop("struck_head", (who,))

def crushed(who: str) -> Prop:
    return Prop("crushed", (who,))


# Causal attribution (killer → victim). Separate from the modality
# predicates above so a rule can (later) derive `killed` from
# `crushed` ∧ `by(killer, victim)` if a forcing function argues.
def killed_by(victim: str, killer: str) -> Prop:
    return Prop("killed_by", (victim, killer))


# Past crimes — each guest's pre-plot murder, revealed by the
# gramophone. Argument order: (who-committed, who-died, descriptor).
# The descriptor is a free-form string so the encoding can preserve
# Christie's specific accusations ("Edward Seton", "the Hamiltons",
# etc.) without a per-victim Entity record.
def past_killed(who: str, victim_name: str) -> Prop:
    return Prop("past_killed", (who, victim_name))


# Accusation (what the gramophone says about each guest). Distinct
# from past_killed: the accusation is the UTTERANCE, past_killed is
# the world fact. Encoding both makes the knowledge-vs-fact
# asymmetry visible.
def accused_of(who: str, victim_name: str) -> Prop:
    return Prop("accused_of", (who, victim_name))


# Plan / identity predicates.
def is_killer(who: str) -> Prop:
    """The Soldier Island killer. True of Wargrave only; known to
    Wargrave from τ_s=-∞ and to the reader at τ_s=18."""
    return Prop("is_killer", (who,))

def host_invited(who: str) -> Prop:
    """U. N. Owen invited this guest to Soldier Island."""
    return Prop("host_invited", (who,))


# Identity proposition — reserved predicate per identity-and-
# realization-sketch-01.
def identity_prop(a: str, b: str) -> Prop:
    return Prop(IDENTITY_PREDICATE, (a, b))


# ----------------------------------------------------------------------------
# Event helpers (parallel to oedipus.py)
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
            provenance=(f"observed @ τ_s={τ}"
                        f"{(': ' + note) if note else ''}",),
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


def world(p: Prop, asserts: bool = True) -> WorldEffect:
    return WorldEffect(prop=p, asserts=asserts)


# ----------------------------------------------------------------------------
# Fabula
# ----------------------------------------------------------------------------

# Every guest on the island carries U.N.Owen's invitation. Encoded at
# τ_s=0 as the shared pre-story fact each character knows about.
# τ_s increases roughly per scene; no pretense of hour-level
# precision.

_ALL_GUESTS = (
    "wargrave", "vera", "lombard", "emily", "macarthur",
    "armstrong", "blore", "marston", "rogers", "mrs_rogers",
)

# Christie's authorial accusation for each guest (the gramophone's
# recording). Descriptors use the novel's own phrasings.
_ACCUSATIONS: tuple = (
    ("wargrave",   "Edward Seton"),                # wrongful hanging
    ("vera",       "Cyril Hamilton"),              # let him drown
    ("lombard",    "twenty-one tribesmen"),        # left to die in the bush
    ("emily",      "Beatrice Taylor"),             # drove her to suicide
    ("macarthur",  "Arthur Richmond"),             # sent lover to die
    ("armstrong",  "Louisa Mary Clees"),           # operated drunk
    ("blore",      "James Stephen Landor"),        # perjury
    ("marston",    "John and Lucy Combes"),        # reckless driving
    ("rogers",     "Jennifer Brady"),              # withheld medicine
    ("mrs_rogers", "Jennifer Brady"),              # shared crime with husband
)


# ============================================================================
# τ_s = 0 — Arrival on Soldier Island
# ============================================================================
#
# All ten guests arrive via boat, meet the Rogers who explain the
# host U.N.Owen is detained. Encoded as a single presence-
# establishing event: everyone is now on the island.

E_arrivals = Event(
    id="E_arrivals",
    type="arrival",
    τ_s=0, τ_a=0,
    participants={
        "guests": _ALL_GUESTS,
        "at_location": "soldier_island",
    },
    effects=(
        *[world(on_island(g)) for g in _ALL_GUESTS],
        *[world(alive(g)) for g in _ALL_GUESTS],
        *[world(host_invited(g)) for g in _ALL_GUESTS],
    ),
)


# ============================================================================
# τ_s = 1 — Dinner in the mansion
# ============================================================================
#
# The ten guests gather in the dining room. Ten porcelain soldier
# figurines stand on the centerpiece (a detail that will matter for
# the nursery-rhyme counting pattern).

E_dinner = Event(
    id="E_dinner",
    type="scene",
    τ_s=1, τ_a=0,
    participants={
        "guests": _ALL_GUESTS,
        "at_location": "mansion",
    },
    effects=(
        *[world(at_mansion(g)) for g in _ALL_GUESTS],
    ),
)


# ============================================================================
# τ_s = 2 — Gramophone accusation
# ============================================================================
#
# The pivotal scene. A record plays, identifying each guest by name
# and accusing them of a specific past murder. The gramophone event
# asserts three things:
#
# 1. past_killed(who, victim) as world facts (the novel treats these
#    as true; the truth is part of Wargrave's framing device).
# 2. accused_of(who, victim_name) as world facts (the utterance
#    itself; this is what actually happened in-scene).
# 3. Every listener learns of every accusation (KnowledgeEffect
#    per listener × per accusation — 10 listeners × 10 accusations,
#    but only on accusations about OTHERS; each guest already knows
#    their own past).
#
# The encoding ships the ten past_killed + ten accused_of as world
# effects. Per-listener knowledge effects are generated below. Note
# that the gramophone is a recording; the "speaker" is U.N.Owen
# (the fictitious host whose voice the recording carries).

_gramophone_world_effects = (
    *[world(past_killed(who, victim)) for (who, victim) in _ACCUSATIONS],
    *[world(accused_of(who, victim)) for (who, victim) in _ACCUSATIONS],
)

_gramophone_knowledge_effects: list = []
# Each guest learns every accusation (including their own, which is
# semantically redundant — they already know — but the knowledge
# effect records the moment of public utterance).
for _listener in _ALL_GUESTS:
    for _accused, _victim in _ACCUSATIONS:
        _gramophone_knowledge_effects.append(
            told_by(
                _listener, "un_owen",
                accused_of(_accused, _victim),
                τ=2,
            )
        )

E_gramophone = Event(
    id="E_gramophone",
    type="utterance",
    τ_s=2, τ_a=0,
    participants={
        "audience": _ALL_GUESTS,
        "speaker": "un_owen",
        "instrument": "gramophone",
        "at_location": "mansion",
    },
    effects=(
        *_gramophone_world_effects,
        *_gramophone_knowledge_effects,
    ),
)


# ============================================================================
# τ_s = 3 — Marston dies (poisoned whisky)
# ============================================================================
#
# Anthony Marston drinks a whisky laced with cyanide and dies
# within seconds. First of the ten.

E_marston_dies = Event(
    id="E_marston_dies",
    type="death",
    τ_s=3, τ_a=0,
    participants={
        "victim": "marston",
        "killer": "wargrave",
        "witnesses": ("wargrave", "vera", "lombard", "emily",
                      "macarthur", "armstrong", "blore",
                      "rogers", "mrs_rogers"),
        "at_location": "mansion",
    },
    effects=(
        world(alive("marston"), asserts=False),
        world(dead("marston")),
        world(poisoned("marston")),
        world(killed_by("marston", "wargrave")),
    ),
)


# ============================================================================
# τ_s = 4 — Mrs Rogers dies in her sleep (overdose)
# ============================================================================

E_mrs_rogers_dies = Event(
    id="E_mrs_rogers_dies",
    type="death",
    τ_s=4, τ_a=0,
    participants={
        "victim": "mrs_rogers",
        "killer": "wargrave",
        "at_location": "mansion",
    },
    effects=(
        world(alive("mrs_rogers"), asserts=False),
        world(dead("mrs_rogers")),
        world(poisoned("mrs_rogers")),
        world(killed_by("mrs_rogers", "wargrave")),
    ),
)


# ============================================================================
# τ_s = 5 — General Macarthur dies on the beach (struck on the head)
# ============================================================================

E_macarthur_dies = Event(
    id="E_macarthur_dies",
    type="death",
    τ_s=5, τ_a=0,
    participants={
        "victim": "macarthur",
        "killer": "wargrave",
        "at_location": "soldier_island",
    },
    effects=(
        world(alive("macarthur"), asserts=False),
        world(dead("macarthur")),
        world(struck_head("macarthur")),
        world(killed_by("macarthur", "wargrave")),
    ),
)


# ============================================================================
# τ_s = 6 — Rogers dies at the woodpile (axe blow)
# ============================================================================

E_rogers_dies = Event(
    id="E_rogers_dies",
    type="death",
    τ_s=6, τ_a=0,
    participants={
        "victim": "rogers",
        "killer": "wargrave",
        "at_location": "soldier_island",
    },
    effects=(
        world(alive("rogers"), asserts=False),
        world(dead("rogers")),
        world(axed("rogers")),
        world(killed_by("rogers", "wargrave")),
    ),
)


# ============================================================================
# τ_s = 7 — Emily Brent dies (hypodermic injection)
# ============================================================================

E_emily_dies = Event(
    id="E_emily_dies",
    type="death",
    τ_s=7, τ_a=0,
    participants={
        "victim": "emily",
        "killer": "wargrave",
        "at_location": "mansion",
    },
    effects=(
        world(alive("emily"), asserts=False),
        world(dead("emily")),
        world(poisoned("emily")),
        world(killed_by("emily", "wargrave")),
    ),
)


# ============================================================================
# τ_s = 8 — Wargrave stages his own death (FAKE)
# ============================================================================
#
# Critical deception: Armstrong helps Wargrave stage a fake death
# (forehead wound painted on) so the remaining suspects believe the
# killer is still among them. The substrate encodes the
# WORLD-LEVEL truth: Wargrave is NOT dead. But the KNOWLEDGE-LEVEL
# state for every other living guest is "Wargrave dead" — except
# Armstrong, who is in on the deception.
#
# This is the encoding's first honest asymmetry: fact vs. belief.
# Armstrong dies next because he's the only other agent who knows
# Wargrave is alive.

E_wargrave_fake_death = Event(
    id="E_wargrave_fake_death",
    type="staging",
    τ_s=8, τ_a=0,
    participants={
        "stager": "wargrave",
        "accomplice": "armstrong",
        "audience": ("vera", "lombard", "blore"),
        "at_location": "mansion",
    },
    effects=(
        # Wargrave and Armstrong KNOW the death is fake. All other
        # living guests believe Wargrave is dead.
        told_by("vera", "armstrong", dead("wargrave"), τ=8,
                confidence=Confidence.CERTAIN, slot=Slot.KNOWN),
        told_by("lombard", "armstrong", dead("wargrave"), τ=8,
                confidence=Confidence.CERTAIN, slot=Slot.KNOWN),
        told_by("blore", "armstrong", dead("wargrave"), τ=8,
                confidence=Confidence.CERTAIN, slot=Slot.KNOWN),
    ),
)


# ============================================================================
# τ_s = 9 — Armstrong dies (drowned off the cliff)
# ============================================================================
#
# Wargrave lures Armstrong to the cliff and pushes him into the
# sea. With Armstrong dead, no one living knows Wargrave is still
# alive.

E_armstrong_dies = Event(
    id="E_armstrong_dies",
    type="death",
    τ_s=9, τ_a=0,
    participants={
        "victim": "armstrong",
        "killer": "wargrave",
        "at_location": "soldier_island",
    },
    effects=(
        world(alive("armstrong"), asserts=False),
        world(dead("armstrong")),
        world(drowned("armstrong")),
        world(killed_by("armstrong", "wargrave")),
    ),
)


# ============================================================================
# τ_s = 10 — Blore dies (crushed by bear statue)
# ============================================================================

E_blore_dies = Event(
    id="E_blore_dies",
    type="death",
    τ_s=10, τ_a=0,
    participants={
        "victim": "blore",
        "killer": "wargrave",
        "at_location": "mansion",
    },
    effects=(
        world(alive("blore"), asserts=False),
        world(dead("blore")),
        world(crushed("blore")),
        world(struck_head("blore")),
        world(killed_by("blore", "wargrave")),
    ),
)


# ============================================================================
# τ_s = 11 — Vera shoots Lombard
# ============================================================================
#
# Two guests remain alive (plus the fake-dead Wargrave). Vera, now
# convinced Lombard is the killer, shoots him with his own
# revolver. She is the active killer in this moment; the substrate
# records her agency. Wargrave is the orchestrator but not the
# killer-by-hand.

E_vera_shoots_lombard = Event(
    id="E_vera_shoots_lombard",
    type="killing",
    τ_s=11, τ_a=0,
    participants={
        "victim": "lombard",
        "killer": "vera",
        "orchestrator": "wargrave",
        "at_location": "soldier_island",
    },
    effects=(
        world(alive("lombard"), asserts=False),
        world(dead("lombard")),
        world(shot("lombard")),
        world(killed_by("lombard", "vera")),
    ),
)


# ============================================================================
# τ_s = 12 — Vera hangs herself
# ============================================================================
#
# Alone in her room, Vera finds a noose staged by Wargrave
# (matching the nursery rhyme's final line: "one hanged himself,
# and then there were none"). Compelled by guilt over Cyril's
# drowning and the environmental suggestion of the noose, she
# hangs herself. The substrate records this as Vera's own action;
# Wargrave is the stager, not the direct killer.

E_vera_hangs = Event(
    id="E_vera_hangs",
    type="death",
    τ_s=12, τ_a=0,
    participants={
        "victim": "vera",
        "killer": "vera",
        "orchestrator": "wargrave",
        "at_location": "mansion",
    },
    effects=(
        world(alive("vera"), asserts=False),
        world(dead("vera")),
        world(hanged("vera")),
        world(killed_by("vera", "vera")),
    ),
)


# ============================================================================
# τ_s = 13 — Wargrave shoots himself (real death this time)
# ============================================================================
#
# With Vera dead, the plan is complete. Wargrave rigs a revolver
# such that his corpse will appear, to investigators, to have been
# shot by someone else (the body will be found upstairs, the
# revolver rigged to fly back to his hand — a detail the inspectors
# note but can't explain). Wargrave dies.

E_wargrave_dies = Event(
    id="E_wargrave_dies",
    type="death",
    τ_s=13, τ_a=0,
    participants={
        "victim": "wargrave",
        "killer": "wargrave",
        "at_location": "mansion",
    },
    effects=(
        world(alive("wargrave"), asserts=False),
        world(dead("wargrave")),
        world(shot("wargrave")),
        world(killed_by("wargrave", "wargrave")),
    ),
)


# ============================================================================
# τ_s = 14 — Message in a bottle (epilogue reveal)
# ============================================================================
#
# A fisherman later finds a bottle containing Wargrave's written
# confession. This is the substrate moment where the reader-level
# identity of the killer is disclosed. No on-island agent is alive
# to receive it. The confession reveals:
#
# - Wargrave is the killer (is_killer(wargrave) was always true).
# - U. N. Owen is Wargrave (identity assertion).
# - Wargrave's motive: judgment outside the law's reach.
#
# Encoded as a world-level revelation at τ_s=14. No agent-side
# KnowledgeEffects (everyone on the island is dead); the reader-
# level anchor for this revelation lives in the Description layer
# (see D_epilogue_confession below).

E_epilogue_confession = Event(
    id="E_epilogue_confession",
    type="revelation",
    τ_s=14, τ_a=0,
    participants={
        "author": "wargrave",
        "at_location": "soldier_island",  # written before Wargrave's death
    },
    effects=(
        world(is_killer("wargrave")),
        world(host_invited("wargrave"), asserts=False),  # Wargrave wasn't "invited" — he was the host
    ),
)


# ============================================================================
# Assemble FABULA
# ============================================================================

FABULA = [
    E_arrivals,
    E_dinner,
    E_gramophone,
    E_marston_dies,
    E_mrs_rogers_dies,
    E_macarthur_dies,
    E_rogers_dies,
    E_emily_dies,
    E_wargrave_fake_death,
    E_armstrong_dies,
    E_blore_dies,
    E_vera_shoots_lombard,
    E_vera_hangs,
    E_wargrave_dies,
    E_epilogue_confession,
]


# ----------------------------------------------------------------------------
# Branches
# ----------------------------------------------------------------------------

ALL_BRANCHES = {
    CANONICAL_LABEL: CANONICAL,
}


# ----------------------------------------------------------------------------
# Rules (inference-model-sketch-01)
# ----------------------------------------------------------------------------
#
# No compound-predicate rules today. The accused_of → past_killed
# link is authorial-fact (Christie asserts each accusation is true
# in the confession); it's carried as separate world facts rather
# than derived. If a probe or verifier pressure argues for deriving
# `guilty_of_murder(X, Y)` from `accused_of(X, Y) ∧ past_killed(X,
# Y)`, a future arc adds the rule.

RULES: tuple = ()


# ----------------------------------------------------------------------------
# Descriptions (descriptions-sketch-01)
# ----------------------------------------------------------------------------

D_gramophone_texture = Description(
    id="D_gramophone_texture",
    attached_to=anchor_event("E_gramophone"),
    kind="texture",
    attention=Attention.STRUCTURAL,
    text=(
        "The gramophone accusation is Christie's framing device. "
        "Each guest hears not only their own name and crime — which "
        "they alone could verify from prior knowledge — but also "
        "nine other accusations they cannot verify. The scene "
        "establishes in one stroke the two epistemic asymmetries "
        "the novel depends on: every listener has privileged access "
        "to one past crime (their own), and the killer has "
        "privileged access to all ten. The event's effects reflect "
        "this structurally: world-level past_killed + accused_of "
        "facts land for all ten; per-listener KnowledgeEffects "
        "land the accusation (not the crime's truth) in each "
        "listener's BELIEVED slot."
    ),
    authored_by="author",
    τ_a=0,
)

D_nursery_rhyme_pattern = Description(
    id="D_nursery_rhyme_pattern",
    attached_to=anchor_event("E_marston_dies"),
    kind="reader-frame",
    attention=Attention.INTERPRETIVE,
    text=(
        "Each death in the novel follows a line of the 'Ten Little "
        "Soldier Boys' nursery rhyme — Marston 'choked his little "
        "self', Mrs Rogers 'overslept herself', Macarthur 'said "
        "he'd stay there', Rogers 'chopped himself in halves', and "
        "so on. The substrate encodes the killing modalities "
        "(poisoned, axed, struck_head, drowned, shot, hanged, "
        "crushed) as distinct world-predicates so a verifier or "
        "probe can surface the pattern. The substrate does NOT "
        "encode the nursery-rhyme correspondence — that's a reader-"
        "frame claim the Dramatica layer carries (ThematicPicks) "
        "or that probe commentary surfaces."
    ),
    authored_by="author",
    τ_a=0,
)

D_wargrave_fake_death_asymmetry = Description(
    id="D_wargrave_fake_death_asymmetry",
    attached_to=anchor_event("E_wargrave_fake_death"),
    kind="motivation",
    attention=Attention.STRUCTURAL,
    text=(
        "The fake-death scene is the encoding's sharpest fact/"
        "belief split. World-level: alive(wargrave) stays true; "
        "Wargrave is not in fact dead. Knowledge-level: every "
        "living guest except Armstrong holds dead(wargrave) at "
        "slot=KNOWN, routed through Armstrong's told_by effect. "
        "Armstrong (who staged the scene with Wargrave) is the "
        "only other agent whose knowledge matches the world. The "
        "asymmetry is load-bearing for the rest of the plot: the "
        "killer is believed dead by his remaining victims, giving "
        "Wargrave the freedom to act without suspicion. "
        "Armstrong's death at E_armstrong_dies collapses the "
        "asymmetry — after τ_s=9, no living agent holds the true "
        "value of alive(wargrave)."
    ),
    authored_by="author",
    τ_a=0,
)

D_epilogue_confession = Description(
    id="D_epilogue_confession",
    attached_to=anchor_event("E_epilogue_confession"),
    kind="reader-frame",
    attention=Attention.STRUCTURAL,
    text=(
        "The epilogue confession is Christie's answer to the "
        "question the ten dead characters cannot answer: who was "
        "the killer? Substrate-level, is_killer(wargrave) "
        "world-asserts here; it was always semantically true "
        "(Wargrave was planning the killings from before τ_s=0) "
        "but the substrate has no prior proof of it. Reader-level, "
        "this is where the reader's state catches up with the "
        "authorial ground truth — a shape distinct from Ackroyd "
        "(where the narrator is the killer, and the reader's "
        "knowledge is gated by their own distrust of Sheppard's "
        "prose) and from Rashomon (where no testimony is fully "
        "trustworthy, and the reader has to weigh branches "
        "rather than accept a confession)."
    ),
    authored_by="author",
    τ_a=0,
)


DESCRIPTIONS = [
    D_gramophone_texture,
    D_nursery_rhyme_pattern,
    D_wargrave_fake_death_asymmetry,
    D_epilogue_confession,
]
