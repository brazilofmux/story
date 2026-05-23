"""
The Duchess of Malfi — the encoded fabula (substrate skeleton).

**Session 1 scope (0b5e0e3):** entities, canonical branches, prop
constructors, event helpers, FABULA (the canonical spine, 34
events from pre-play standing facts through the Act-V mutual
killings and Delio's return with the heir), and zero derivation
rules (rationale below). Knowledge effects authored only on the
load-bearing beats — Bosola's spying, the apricot ploy, the
horoscope, Ferdinand's bedchamber confrontation, the dead-hand
and waxworks tortures, the strangling, the corpse-view
recognitions, the night-violence of Act V.

**Session 2 scope (32acd45):** Aristotelian overlay in the
sibling module `malfi_aristotelian.py` (sketches 01-05). The
overlay pressures **OQ-LEAR-4 (secondary peripeteia for
subplot)** with four structurally-distinct character-arc
peripeteia events within a single mythos — the Duchess at
capture (τ_s=17), Ferdinand at corpse-view (τ_s=23), Bosola at
corpse-view (τ_s=24), Antonio in the dark (τ_s=30). Surfaces
two additional banked open questions (OQ-AP7 third-encoding
re-surface; OQ-MALFI-1 new — sequentially-wielded-instrument).

**Session 3 scope (this file):** PREPLAY_DISCLOSURES (4 facts —
The Duchess opens with less audience-pre-knowledge than Hamlet
or Macbeth; the Aragonese family structure, the Duchess's
widowhood, the Cardinal's office, and Ferdinand's ducal title
are pre-loaded), SJUZHET (30 in-play entries with focalization —
the Duchess focalizes 10, Bosola 7, Ferdinand 5, Cardinal 2,
Antonio 2, Delio 1, with 3 omniscient public-or-chaos scenes;
Bosola's near-Duchess focalization count is the encoding's
structural surface for the critical-tradition reading that
Bosola is the play's structural co-protagonist), DESCRIPTIONS
(12 interpretive records covering Bosola's transformation
register, Ferdinand's lycanthropy reading, the Cardinal's
interiority absence, the Duchess's marriage motivation, the
OQ-LEAR-4/OQ-AP7/OQ-MALFI-1 reader frames, Webster's parodic-
Catholic setting, the play's instrument density, the "Duchess
of Malfi still" reading, Antonio's anti-recognition register,
and the eldest son's survival as structural payload).

Story content only. No substrate logic. This file parallels
`hamlet.py` and `lear.py` in shape and is the **fifth Shakespearean-
or-Jacobean tragedy encoding** in the corpus alongside Macbeth,
Hamlet, and Lear (plus the non-Shakespeare classical corpus
Oedipus). Webster's *Duchess* is the corpus's **first non-
Shakespeare Jacobean tragedy** and the first encoding authored
specifically to pressure a banked Lear-arc forcing function:

- **OQ-LEAR-4** — Secondary peripeteia for subplot. Lear surfaced
  the pressure with a single encoding: a main-plot peripeteia
  (E_goneril_strips_retinue) plus a subplot-arc that runs
  parallel (Gloucester's blinding, structurally separable from
  Lear's reversal). The dialect currently models peripeteia at
  the `ArMythos` level (one event id per mythos); Lear's
  Gloucester subplot fits awkwardly. Session 6 of the Lear probe
  returned three concrete dialect-extension proposals
  (`secondary_peripeteia_event_ids` field, `ArPhase`-level
  peripeteia, `ArMythosRelation kind='subplot'`) but flagged that
  cross-encoding pressure is the natural forcing criterion. The
  Duchess is the second-site encoding. It is denser on the
  question than Lear because the Duchess's tragedy carries
  **four structurally-distinct character-arc peripeteia events
  within a single mythos**:

  1. **The Duchess's arc peripeteia** at E_capture_in_countryside
     (τ_s=17) — the moment her concealment collapses and her
     fate is sealed. Aristotelian peripeteia proper: fortune
     reverses direction from secret-but-flourishing to
     captured-and-doomed.

  2. **Bosola's arc peripeteia** at E_bosola_resolves_revenge
     (τ_s=24) — viewing the Duchess's corpse turns him from
     instrument-of-tyranny to avenger. Internal recognition
     paired with structural turn; the play's most explicit
     mid-character arc-reversal.

  3. **Ferdinand's arc peripeteia** at E_ferdinand_views_corpse
     (τ_s=23) — also at the corpse, distinct event, distinct
     character. "Cover her face; mine eyes dazzle: she died
     young." Recognition + reversal from tormentor to madman.
     Lycanthropy manifests at τ_s=25.

  4. **Antonio's arc peripeteia** at E_bosola_kills_antonio
     (τ_s=30) — the bitterest reversal in the play. Antonio is
     killed by Bosola *in the dark*, by mistake, moments before
     Bosola would have allied with him. The reversal is
     structurally peripeteial (fortune reverses); the recognition
     is anti-recognition (neither party sees who the other is).

  The dialect's current single-peripeteia-per-mythos shape
  cannot carry all four. The forcing function for OQ-LEAR-4 is
  whether the second-site corpus needs any of the three sketch-05
  candidate shapes, or pressures a fourth.

  Lear also surfaced the related **OQ-LEAR-5** — audience-level
  parallel-plot catharsis. The Duchess pressures this orthogonally:
  three of the four arc-peripeteia events (Bosola, Ferdinand,
  Antonio) generate distinct cathartic registers within the same
  mythos. Banked for re-evaluation if Sessions 2+ surface it.

- **OQ-AP14 (already closed in sketch-05)** — instrumental-kind
  ArCharacterArcRelation. The Duchess does not RE-pressure A17;
  sketch-05 landed it. But the encoding does instantiate the
  shape: Ferdinand wields Bosola as instrument against the
  Duchess (the corpus's first instrumental-via-intelligencer
  relation distinct from Hamlet's Claudius-Laertes
  poisoning-plot and Lear's brothers-via-forgery instruments).
  Session 2's overlay will author `ArCharacterArcRelation
  kind="instrumental"` for Ferdinand→Bosola and possibly
  Cardinal→Bosola.

Encoding choices (explicit, so future readers understand the slice):

- **Branches: canonical only.** *The Duchess of Malfi* has no
  contested-testimony structure; the text is what it is. The
  Quartos differ on minor textual points but not on the canonical
  events. No Rashomon-style branching.

- **Identity placeholders: none.** The Duchess's secret marriage
  is a knowledge-state question (Ferdinand, the Cardinal, Bosola,
  the court do not know; the principals know), not a substrate
  identity-predicate question. Webster also gives no disguises in
  the Edgar-as-Poor-Tom or Kent-as-Caius sense. Bosola's
  intelligencer role is openly Ferdinand's commission to him; the
  characters he reports on do not know about it, but his identity
  is never disguised.

- **Audience-pre-knowledge disclosures: minimal.** Unlike Hamlet
  (Ghost lore, regicide already accomplished) or Macbeth (witches
  pre-loaded), the Duchess opens with a clean slate. The audience
  knows the dramatis personae, the court at Amalfi, and the
  brothers' general disposition only after the opening exposition.
  Session 3's PREPLAY_DISCLOSURES will be short — three or four
  facts: the Aragonese family tree, the Duchess's widowhood, the
  Cardinal's prior employment of Bosola.

- **Focalization: distributed across four arcs.** Like Lear, the
  Duchess runs multiple parallel character arcs concurrently
  (Duchess, Bosola, Ferdinand, Antonio, Cardinal, Julia). Session
  3's SJUZHET will distribute focalization across these, with
  Bosola carrying the largest share (he is the play's structural
  observer and increasingly its conscience). Deferred to Session 3.

- **Authored compound predicates: none.** Lear shipped one
  (`fratricide`). The Duchess's killings do not reduce to direct-
  shape compound predicates: Ferdinand and the Cardinal *order*
  the Duchess's death (sibling-orchestrated killing) but the
  direct killing is by Bosola. The substrate's `killed(X, Y)`
  predicate marks direct action; a compound capturing "sibling
  orchestrated via instrument" would need a 3-place rule body
  involving `ordered_killing`, `sibling_of`, and `killed` with
  three distinct variables. This is principled-but-substantial;
  authored compound predicates beyond direct-action are deferred
  to a future increment.

- **Supernatural ontology: absent.** No ghosts, witches, or
  prophecies. Ferdinand's lycanthropy is a clinical-or-symbolic
  madness — Webster authors it as transformation (the Duke
  digging up graves and howling) but the substrate marks it as
  `lycanthropy(ferdinand)` at τ_s=25 without taking a position on
  whether the transformation is real, hysterical, or punitive.
  Descriptions layer (Session 3) will carry the interpretive
  ambiguity.

- **Scope of the play encoded: the full canonical spine of all
  arcs, compressed.** Secondary characters (Castruchio is in;
  Pescara, Roderigo, Grisolan, Silvio, Malateste, the Marquis,
  the Doctor, the various courtiers and madmen) are compressed
  into the events they enable. The Duchess's two younger
  children (named in the text as the daughter and the second son)
  are not authored as entities; their strangling is asserted as
  a substrate fact at E_strangling but no entity records are
  introduced. The eldest son (who survives, and whom Delio
  returns with at the end) IS authored as `duchess_son` because
  he carries the structural "surviving heir" payload in the
  closing scene.

- **The Cardinal's name.** Webster does not name the Cardinal;
  he is referred to throughout as "the Cardinal." The encoding
  uses `cardinal` as the entity id and "the Cardinal" as the
  display name; no surname is invented.

- **The Duchess's name.** Historically Giovanna d'Aragona, Duchess
  of Amalfi; the play refers to her only by title. The encoding
  uses `duchess` as id and "the Duchess of Amalfi" as display
  name.

- **Instruments authored as substrate facts.** The horoscope
  Antonio drops, the dead hand Ferdinand displays, the waxworks
  of the "dead" Antonio and children, the masque of madmen, and
  the poisoned book the Cardinal gives Julia are all
  substrate-level facts asserted at their respective events.
  Following the Hamlet / Lear pattern (Mousetrap, forged letter,
  staged wound), instruments are predicates and event-effects,
  not Entity records.

- **Webster's catastrophic body-count.** The play kills the
  Duchess, Cariola, both younger children (offstage but at
  E_strangling), Julia (Cardinal's poison), Antonio (Bosola's
  mistake), the Cardinal (Bosola), Ferdinand (Bosola), and
  Bosola (Ferdinand's mortal wound, then expires after Delio
  arrives). That is eight named deaths in the play's span — the
  highest in the corpus (Hamlet has six, Lear seven, Oedipus
  one, Macbeth ten if Lady Macbeth's offstage death is counted
  with the on-stage four). The deaths cluster in Acts IV-V;
  Session 3 may surface OQ-AP1 (ArPathos grounding) pressure on
  Webster's distinct catastrophe shape ("dense mid-Act IV
  cluster plus dispersed Act-V night-violence").

Encoding pressures OQ-LEAR-4 (parallel-plot peripeteia) without
sketch-level modification of the substrate or its shape. All
predicate and event constructions reuse the existing substrate
vocabulary.
"""

from __future__ import annotations

from story_engine.core.substrate import (
    Entity, Prop, Event,
    CANONICAL, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
    Description, Attention, DescStatus, anchor_event,
    Rule,
)


# ----------------------------------------------------------------------------
# Entities
# ----------------------------------------------------------------------------

# --- Aragonese family: the Duchess and her brothers ---
duchess   = Entity(id="duchess",   name="the Duchess of Amalfi",
                   kind="agent")
ferdinand = Entity(id="ferdinand", name="Ferdinand, Duke of Calabria",
                   kind="agent")
cardinal  = Entity(id="cardinal",  name="the Cardinal",
                   kind="agent")

# --- The Duchess's household and the secret marriage ---
antonio  = Entity(id="antonio",  name="Antonio Bologna",   kind="agent")
cariola  = Entity(id="cariola",  name="Cariola",           kind="agent")
duchess_son = Entity(id="duchess_son",
                     name="the Duchess's eldest son",
                     kind="agent")

# --- The intelligencer ---
bosola = Entity(id="bosola", name="Daniel de Bosola", kind="agent")

# --- The Cardinal's circle ---
julia      = Entity(id="julia",      name="Julia",      kind="agent")
castruchio = Entity(id="castruchio", name="Castruchio", kind="agent")

# --- Antonio's friend / survivor witness ---
delio = Entity(id="delio", name="Delio", kind="agent")

# --- Locations ---
amalfi             = Entity(id="amalfi",             name="Amalfi (the Duchess's court)",
                            kind="location")
ancona             = Entity(id="ancona",             name="Ancona",
                            kind="location")
loretto            = Entity(id="loretto",            name="Loretto (pilgrimage shrine)",
                            kind="location")
countryside        = Entity(id="countryside",        name="the countryside near Ancona",
                            kind="location")
prison_cell        = Entity(id="prison_cell",        name="the Duchess's prison cell at Amalfi",
                            kind="location")
cardinals_palace   = Entity(id="cardinals_palace",   name="the Cardinal's palace at Rome",
                            kind="location")


ENTITIES = [
    # Aragonese family
    duchess, ferdinand, cardinal,
    # Duchess's household + secret marriage + surviving son
    antonio, cariola, duchess_son,
    # The intelligencer
    bosola,
    # Cardinal's circle
    julia, castruchio,
    # Survivor witness
    delio,
    # Locations
    amalfi, ancona, loretto, countryside, prison_cell, cardinals_palace,
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
# moral / affective / ontological register (is Bosola damned or
# redeemed; is Ferdinand's lycanthropy real or hysterical; is the
# Duchess a martyr or a transgressor) lives on descriptions.


def duchess_of(who: str, realm: str) -> Prop:
    # Sovereign of a duchy. Female. The Duchess is duchess_of(amalfi);
    # there is no other duchy in the encoding.
    return Prop("duchess_of", (who, realm))

def duke_of(who: str, realm: str) -> Prop:
    # Ferdinand is duke_of(calabria). The Duchess's first husband
    # (off-stage, deceased pre-play) was duke of Amalfi but is not
    # an entity in the encoding; his title persists on the Duchess
    # via duchess_of(amalfi).
    return Prop("duke_of", (who, realm))

def churchman(who: str) -> Prop:
    # Cardinal holds ecclesiastical office. Not a duke title; the
    # text uses "the Cardinal" throughout.
    return Prop("churchman", (who,))

def sibling_of(a: str, b: str) -> Prop:
    # Symmetric; authored both directions where used. The Aragonese
    # three are pairwise siblings (Ferdinand/Cardinal, Ferdinand/
    # Duchess, Cardinal/Duchess). Half-blood or full-blood is not
    # textually specified; the predicate is shape-only.
    return Prop("sibling_of", (a, b))

def twin_of(a: str, b: str) -> Prop:
    # Symmetric; Ferdinand and the Duchess. Webster makes the twin
    # bond structurally load-bearing (Ferdinand's psychic collapse
    # at her death). Authored as a substrate fact so the dialect
    # overlay can read the twin-bond as ArCharacterArcRelation
    # later.
    return Prop("twin_of", (a, b))

def parent_of(parent: str, child: str) -> Prop:
    # Authored for: Duchess → her three children (only the eldest is
    # an entity, but parent_of(duchess, duchess_son) is asserted at
    # E_first_birth; the younger two are not asserted as parent_of
    # facts in Session 1 since they are not entities). Also the
    # late Duke of Aragon is implicitly parent of the three siblings
    # but is not an entity — the sibling_of relation suffices.
    return Prop("parent_of", (parent, child))

def married(a: str, b: str) -> Prop:
    # Public marriages: Julia + Castruchio. The Duchess and Antonio
    # are NOT married() — their union is secret_marriage(). When the
    # marriage becomes known (E_ferdinand_confronts_duchess, when
    # Ferdinand realises she has remarried) the *substrate* fact
    # does not change — what changes is the knowledge state of the
    # discoverer. The public/secret distinction is at the predicate
    # level, not at the held-state level.
    return Prop("married", (a, b))

def secret_marriage(a: str, b: str) -> Prop:
    # Per verba de praesenti marriage between the Duchess and Antonio,
    # witnessed only by Cariola. World-level fact (the marriage is
    # canonically valid by the play's standards). Distinct from
    # married() because the publicness/concealment is structurally
    # load-bearing — the entire plot mechanism turns on it.
    return Prop("secret_marriage", (a, b))

def widow(who: str) -> Prop:
    # The Duchess is widow(duchess) at play-opening (her first husband,
    # the Duke of Amalfi, is dead before the play begins). The brothers'
    # injunction against remarriage is the play's opening pressure on
    # this status.
    return Prop("widow", (who,))

def mistress_of(a: str, b: str) -> Prop:
    # Julia is mistress_of(cardinal). Distinct from married() (Julia
    # is married to Castruchio) and secret_marriage() (no marriage
    # involved).
    return Prop("mistress_of", (a, b))

def at_location(who: str, where: str) -> Prop:
    return Prop("at_location", (who, where))

def served_by(lord: str, servant: str) -> Prop:
    # Authored for: Duchess served_by Antonio (his steward office, the
    # role that brings them together); Ferdinand served_by Bosola
    # (intelligencer commission). Cariola is the Duchess's waiting
    # woman — served_by(duchess, cariola).
    return Prop("served_by", (lord, servant))

def intelligencer(employer: str, agent: str) -> Prop:
    # Bosola accepts Ferdinand's commission at E_ferdinand_hires_bosola
    # as intelligencer (provisor of horses, openly, with the spying
    # commission secret). Distinct from served_by because the role's
    # function is observation-and-report, not personal service.
    # OQ-AP14 instrumental-shape support: intelligencer is the
    # archetypal instrumental relation in Webster.
    return Prop("intelligencer", (employer, agent))

def pregnant(who: str) -> Prop:
    return Prop("pregnant", (who,))

def captured(who: str, by: str) -> Prop:
    # Duchess captured by Bosola at E_capture_in_countryside. Distinct
    # from imprisoned() (which marks the confinement state) — captured()
    # marks the moment of seizure.
    return Prop("captured", (who, by))

def imprisoned(who: str) -> Prop:
    # Duchess imprisoned() from E_imprisonment forward. Cariola is
    # imprisoned alongside her.
    return Prop("imprisoned", (who,))

def killed(killer: str, victim: str) -> Prop:
    # Direct-action substrate fact. Webster's killings are mostly
    # ordered-by-one-agent-and-executed-by-another; the executor is
    # the killed()-relation party. Bosola is the executor for the
    # Duchess strangling, the Cardinal stabbing, and (mistakenly) the
    # Antonio death. Ferdinand kills Bosola in the mutual wounding.
    return Prop("killed", (killer, victim))

def ordered_killing(orderer: str, victim: str) -> Prop:
    # Sibling-orchestrated killings: Ferdinand and the Cardinal order
    # the Duchess's death. Cardinal orders Julia poisoned (acts as
    # both orderer and executor for Julia — the poisoned book is his
    # own gift). Substrate records the order distinct from the act,
    # following the lear.py convention.
    return Prop("ordered_killing", (orderer, victim))

def dead(who: str) -> Prop:
    return Prop("dead", (who,))

def strangled(who: str) -> Prop:
    # Cause-of-death specifier. Duchess, Cariola, and the two younger
    # children (asserted-as-strangled at E_strangling without entity
    # records).
    return Prop("strangled", (who,))

def poisoned(who: str) -> Prop:
    # Julia, by the Cardinal's poisoned book.
    return Prop("poisoned", (who,))

def stabbed(who: str) -> Prop:
    # Cardinal (Bosola), Ferdinand (Bosola), Bosola (Ferdinand), Antonio
    # (Bosola, mistaken). The Act-V night-violence is a sequence of
    # stabbings in the dark.
    return Prop("stabbed", (who,))

def mad(who: str) -> Prop:
    # World-level claim about a character's mental state. Ferdinand
    # acquires mad(ferdinand) at E_ferdinand_views_corpse (onset) and
    # the substrate marks the transformation explicit with lycanthropy()
    # at E_ferdinand_lycanthropy.
    return Prop("mad", (who,))

def lycanthropy(who: str) -> Prop:
    # Ferdinand's specific madness — the wolf-man transformation
    # Webster's play stages literally (or hysterically; the question
    # belongs to descriptions). Distinct from mad() because lycanthropy
    # carries a specific behavioural shape (graveyard-digging, howling,
    # hair-on-the-inside delusion).
    return Prop("lycanthropy", (who,))

def banished(who: str, from_realm: str) -> Prop:
    # Duchess and Antonio banished from Amalfi at E_banishment_loretto.
    # The Cardinal performs the banishment ritual at the Loretto shrine.
    return Prop("banished", (who, from_realm))

def avenger(who: str) -> Prop:
    # Bosola declares himself avenger at E_bosola_resolves_revenge.
    # World-level fact authored as a substrate marker; not derived.
    # The descriptions layer (Session 3) will carry the interpretive
    # question (revenge-tragedy reading vs. damnation-reading).
    return Prop("avenger", (who,))


# Instrumental-shape predicates. Each records a world-level fact about
# an instrument used in the play. The Duchess of Malfi exercises six
# distinct instruments — Webster is the corpus's densest instrument-
# user.

def horoscope_dropped(by: str) -> Prop:
    # Antonio drops a horoscope of his and the Duchess's first child
    # in E_horoscope_dropped (τ_s=9). Bosola finds it and reads it,
    # which is the substrate origin of his report to Ferdinand. The
    # horoscope is encoded as a predicate (a thing that exists in the
    # world), not as an entity — same convention as Lear's
    # forged_letter and Hamlet's mousetrap.
    return Prop("horoscope_dropped", (by,))

def dead_hand_displayed(by: str, to: str) -> Prop:
    # Ferdinand presents the Duchess with a severed hand bearing a
    # ring (purporting to be Antonio's hand and the wedding ring he
    # gave her). The substrate marks the act; the *belief* the Duchess
    # acquires (that Antonio is dead) lands as a KnowledgeEffect at
    # the same event. World-level fact: the hand is a dead man's
    # hand but not Antonio's — Webster makes the contrivance explicit
    # in the next scene.
    return Prop("dead_hand_displayed", (by, to))

def waxworks_displayed(by: str, to: str) -> Prop:
    # The waxen figures of "dead" Antonio and his children, displayed
    # by Ferdinand to torture the Duchess. World-level fact + belief-
    # effect on the Duchess (same pattern as the dead hand).
    return Prop("waxworks_displayed", (by, to))

def madmen_masque_performed(commissioned_by: str, audience: str) -> Prop:
    # Ferdinand sends a troupe of madmen to the Duchess's prison to
    # dance and rave around her. The dance precedes the strangling
    # (Webster's stage-direction is "Enter Eight Madmen, with music
    # appropriate"). World-level event marker.
    return Prop("madmen_masque_performed", (commissioned_by, audience))

def poisoned_book(by: str, against: str) -> Prop:
    # The Cardinal gives Julia a Bible (or prayer book; the text is
    # editor-contested) whose binding he has poisoned. She kisses it
    # to swear secrecy. World-level instrument predicate.
    return Prop("poisoned_book", (by, against))

def in_the_dark(at: str) -> Prop:
    # The Cardinal's chamber is darkened during Act V scene 5; Bosola
    # cannot see whom he stabs. Authored as a substrate fact at the
    # relevant events so the Aristotelian overlay (Session 2) can
    # read the Antonio death as an anti-recognition reversal.
    return Prop("in_the_dark", (at,))


# ----------------------------------------------------------------------------
# Event helpers — same pattern as macbeth.py / hamlet.py / lear.py /
# oedipus.py.
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
# Fabula — all events on :canonical, status=committed by default.
# ----------------------------------------------------------------------------
#
# τ_s convention:
#   - τ_s ≤ -10 : deep standing facts (the Aragonese family, the
#                 Duchess's widowhood, Bosola's prior galley service,
#                 the Cardinal-Julia liaison)
#   - τ_s = -3  : Antonio's return from France (Act I.i, pre-warning)
#   - τ_s = 0..5 : Act I (the brothers warn, Bosola hired, secret
#                 marriage)
#   - τ_s = 6..10: Act II (children born, apricot ploy, horoscope,
#                 Bosola reports)
#   - τ_s = 11..17: Act III (confrontation, flight, banishment, capture)
#   - τ_s = 18..24: Act IV (imprisonment, dead hand, waxworks, madmen,
#                  strangling, corpse-viewings)
#   - τ_s = 25..33: Act V (lycanthropy, Julia poisoned, night-violence
#                  in the Cardinal's chamber, Delio returns)
#
# The play's time compresses aggressively in Act V — Julia's poisoning,
# Bosola's visit to the Cardinal, the dark-room stabbings, and the
# mutual wounding occur in close substrate-proximity. Session 3+ may
# refine τ_s for the night-cluster if the SJUZHET layer needs sharper
# ordering.

FABULA = [

    # --- Pre-play (τ_s < 0) ---

    Event(
        id="E_aragon_family",
        type="standing",
        τ_s=-30, τ_a=1,
        participants={"first_brother": "ferdinand",
                      "second_brother": "cardinal",
                      "sister": "duchess"},
        effects=(
            # The Aragonese three are siblings. Ferdinand and the
            # Duchess are twins; the Cardinal is the eldest. Webster
            # does not state primogeniture but the Cardinal's role
            # as head-of-house is implicit in the brothers' opening
            # scene (he carries the political authority; Ferdinand
            # carries the personal pathology).
            world(sibling_of("ferdinand", "duchess")),
            world(sibling_of("duchess",   "ferdinand")),
            world(sibling_of("ferdinand", "cardinal")),
            world(sibling_of("cardinal",  "ferdinand")),
            world(sibling_of("cardinal",  "duchess")),
            world(sibling_of("duchess",   "cardinal")),
            world(twin_of("ferdinand", "duchess")),
            world(twin_of("duchess",   "ferdinand")),
            # Titles. Ferdinand holds Calabria; the Cardinal is a
            # prince of the Church (no realm-territory). The Duchess's
            # standing-as-duchess derives from her first marriage,
            # asserted at E_duchess_widowed below.
            world(duke_of("ferdinand", "calabria")),
            world(churchman("cardinal")),
            # Family awareness — every Aragon knows the family tree.
            observe("ferdinand", sibling_of("ferdinand", "duchess"), -30),
            observe("ferdinand", sibling_of("ferdinand", "cardinal"), -30),
            observe("ferdinand", twin_of("ferdinand", "duchess"), -30,
                    note="the twin bond Ferdinand will eventually "
                         "collapse around"),
            observe("cardinal",  sibling_of("cardinal", "duchess"), -30),
            observe("cardinal",  sibling_of("cardinal", "ferdinand"), -30),
            observe("duchess",   sibling_of("duchess", "ferdinand"), -30),
            observe("duchess",   sibling_of("duchess", "cardinal"), -30),
            observe("duchess",   twin_of("duchess", "ferdinand"), -30),
        ),
    ),

    Event(
        id="E_duchess_widowed",
        type="standing",
        τ_s=-20, τ_a=2,
        participants={"who": "duchess"},
        effects=(
            # The Duchess's first husband (the late Duke of Amalfi,
            # not an entity in the encoding) is dead before the play
            # opens. She has inherited the duchy and rules in her
            # own name. Widow status is the spring of the play's
            # opening pressure — the brothers' injunction against
            # remarriage.
            world(duchess_of("duchess", "amalfi")),
            world(widow("duchess")),
            world(at_location("duchess", "amalfi")),
            observe("duchess",   duchess_of("duchess", "amalfi"), -20),
            observe("duchess",   widow("duchess"), -20),
            observe("ferdinand", duchess_of("duchess", "amalfi"), -20),
            observe("ferdinand", widow("duchess"), -20),
            observe("cardinal",  duchess_of("duchess", "amalfi"), -20),
            observe("cardinal",  widow("duchess"), -20),
        ),
    ),

    Event(
        id="E_cardinal_julia_liaison",
        type="standing",
        τ_s=-15, τ_a=3,
        participants={"churchman": "cardinal", "lover": "julia",
                      "husband": "castruchio"},
        effects=(
            # The Cardinal's affair with Julia (married to Castruchio)
            # is established before the play opens. Webster makes the
            # liaison openly known to both parties and tacitly tolerated
            # by Castruchio. Authorial note: Julia's death at the
            # Cardinal's hand at τ_s=28 is structurally a parallel
            # to the Duchess's death — a woman killed for what she
            # knows about a brother.
            world(married("julia", "castruchio")),
            world(married("castruchio", "julia")),
            world(mistress_of("julia", "cardinal")),
            # The principals know; the Duchess and Ferdinand do not
            # explicitly know (or do not care to acknowledge) at this
            # pre-play stage. Session 3 may extend the knowledge map.
            observe("cardinal",   mistress_of("julia", "cardinal"), -15),
            observe("julia",      mistress_of("julia", "cardinal"), -15),
            observe("castruchio", married("julia", "castruchio"), -15,
                    note="he is the de-jure husband; the de-facto "
                         "situation is the Cardinal's"),
        ),
    ),

    Event(
        id="E_bosola_galley_service",
        type="standing",
        τ_s=-12, τ_a=4,
        participants={"agent": "bosola", "employer": "cardinal"},
        effects=(
            # Bosola served the Cardinal previously in some violent
            # capacity (the text mentions "two pollings of his beard"
            # and his "moping in the galleys"); the play opens with
            # him resentful of being un-rewarded. The substrate marks
            # the prior service as a standing fact — Bosola was
            # previously the Cardinal's instrument, which makes
            # Ferdinand's recruitment of him a hand-off between
            # brothers. The intelligencer relation Ferdinand
            # establishes at τ_s=1 will be the new instance; this
            # pre-play one is recorded so the dialect can read the
            # pattern.
            observe("bosola",   served_by("cardinal", "bosola"), -12,
                    note="Bosola's resentment of un-rewarded service "
                         "is the play's opening character note"),
            observe("cardinal", served_by("cardinal", "bosola"), -12,
                    note="and the Cardinal's calculated indifference "
                         "is the answering opening note"),
        ),
    ),

    Event(
        id="E_antonio_returns_from_france",
        type="arrival",
        τ_s=-3, τ_a=5,
        participants={"who": "antonio", "destination": "amalfi"},
        effects=(
            # Antonio returns to Amalfi from a French embassy. He is
            # the Duchess's steward (a household office, not a
            # peerage). Delio greets him in the opening scene; the
            # play's first speech ("You are welcome to your country,
            # my dear Antonio") opens here.
            world(at_location("antonio", "amalfi")),
            world(at_location("delio",   "amalfi")),
            world(served_by("duchess", "antonio")),
            observe("antonio", at_location("antonio", "amalfi"), -3),
            observe("delio",   at_location("antonio", "amalfi"), -3,
                    note="Delio's welcome opens the play"),
            observe("antonio", served_by("duchess", "antonio"), -3),
            observe("duchess", served_by("duchess", "antonio"), -3),
        ),
    ),

    # --- Act I: warning, hiring, secret marriage ---

    Event(
        id="E_brothers_warn_duchess",
        type="speech_act",
        τ_s=0, τ_a=10,
        participants={"speaker_1": "ferdinand",
                      "speaker_2": "cardinal",
                      "addressee": "duchess"},
        effects=(
            # The brothers in Act I.i jointly warn the Duchess against
            # remarrying. Ferdinand's speech carries the dominant
            # affect — possessive, threat-tinged ("Be not cunning; /
            # For they whose faces do belie their hearts / Are
            # witches ere they arrive at twenty year, / Ay, and give
            # the devil suck"). The Cardinal is colder, more political.
            # No world-level change; this is the standing-disapproval
            # establishment. The Duchess's response in soliloquy
            # — "If all my royal kindred lay in my way unto this
            # marriage, I'd make them my low footsteps" — is at
            # τ_s=2.
            world(at_location("ferdinand", "amalfi")),
            world(at_location("cardinal",  "amalfi")),
            world(at_location("duchess",   "amalfi")),
            observe("ferdinand", at_location("duchess", "amalfi"), 0),
            observe("cardinal",  at_location("duchess", "amalfi"), 0),
            observe("duchess",   at_location("ferdinand", "amalfi"), 0,
                    note="she registers the threat-affect in his "
                         "delivery"),
            observe("duchess",   at_location("cardinal", "amalfi"), 0),
        ),
    ),

    Event(
        id="E_ferdinand_hires_bosola",
        type="commission",
        τ_s=1, τ_a=11,
        participants={"employer": "ferdinand", "intelligencer": "bosola"},
        effects=(
            # Ferdinand commissions Bosola as the Duchess's "provisor
            # of horses" — an open office. The actual mission is to
            # spy on her behaviour, particularly her sexual conduct.
            # The intelligencer relation is the structural foundation
            # for OQ-AP14 instrumental-shape pressure in this
            # encoding (and Session 2's ArCharacterArcRelation
            # kind="instrumental" between Ferdinand and Bosola, with
            # the Duchess as target).
            world(intelligencer("ferdinand", "bosola")),
            world(at_location("bosola",    "amalfi")),
            observe("bosola",    intelligencer("ferdinand", "bosola"), 1,
                    note="Bosola accepts the commission with self-"
                         "loathing — 'Sometimes the devil doth "
                         "preach.'"),
            observe("ferdinand", intelligencer("ferdinand", "bosola"), 1),
            # Bosola knows he is to spy on the Duchess; she does not.
            # The asymmetric knowledge is the central plot mechanism
            # through Act II.
        ),
    ),

    Event(
        id="E_duchess_woos_antonio",
        type="proposal",
        τ_s=3, τ_a=12,
        participants={"wooer": "duchess", "wooed": "antonio",
                      "witness": "cariola"},
        effects=(
            # The Duchess woos Antonio in the opening of Act I.iii,
            # in the presence (concealed) of Cariola. Webster's most
            # famous scene of female-initiated wooing in early modern
            # drama: she inverts the seduction-conventions explicitly
            # ("The misery of us that are born great! / We are forced
            # to woo, because none dare woo us.").
            world(at_location("cariola", "amalfi")),
            observe("antonio", at_location("duchess", "amalfi"), 3),
            observe("duchess", at_location("antonio", "amalfi"), 3),
            observe("cariola", at_location("duchess", "amalfi"), 3,
                    note="Cariola observes from behind the arras"),
            observe("cariola", at_location("antonio", "amalfi"), 3),
            # Note: the marriage itself happens at τ_s=4 in a single
            # uninterrupted scene-block. Webster compresses; the
            # substrate separates the proposal from the act.
        ),
    ),

    Event(
        id="E_secret_marriage",
        type="speech_act",
        τ_s=4, τ_a=13,
        participants={"spouse_1": "duchess", "spouse_2": "antonio",
                      "witness": "cariola"},
        effects=(
            # Per verba de praesenti marriage with Cariola as the
            # required witness. In Webster's world (and historically)
            # such a marriage is canonically valid. The Duchess: "I
            # have heard lawyers say, a contract in a chamber / Per
            # verba presenti, is absolute marriage."
            world(secret_marriage("duchess", "antonio")),
            world(secret_marriage("antonio", "duchess")),
            observe("duchess", secret_marriage("duchess", "antonio"), 4),
            observe("antonio", secret_marriage("duchess", "antonio"), 4),
            observe("cariola", secret_marriage("duchess", "antonio"), 4,
                    note="the witness — Webster makes Cariola's "
                         "knowledge structurally load-bearing for "
                         "her own death at τ_s=22"),
            # Crucially: Ferdinand, the Cardinal, Bosola, and the rest
            # of the court do NOT acquire this knowledge. The
            # secret_marriage() predicate is world-true; the
            # discovered() / known-by axis lives on KnowledgeEffects
            # at the discovery events (E_ferdinand_confronts_duchess
            # at τ_s=11, E_bosola_reads_horoscope at τ_s=10).
        ),
    ),

    # --- Act II: pregnancy, apricots, horoscope, Bosola's report ---

    Event(
        id="E_duchess_pregnant_first",
        type="state_change",
        τ_s=6, τ_a=20,
        participants={"who": "duchess"},
        effects=(
            # Time-compression. The play opens Act II with the Duchess
            # visibly pregnant. The substrate marks the pregnancy
            # arrival at τ_s=6 (between marriage and the apricot
            # scene). Cariola knows; Antonio knows; no one else.
            world(pregnant("duchess")),
            observe("duchess", pregnant("duchess"), 6),
            observe("antonio", pregnant("duchess"), 6),
            observe("cariola", pregnant("duchess"), 6),
        ),
    ),

    Event(
        id="E_apricot_ploy",
        type="instrument_deployed",
        τ_s=7, τ_a=21,
        participants={"intelligencer": "bosola", "target": "duchess"},
        effects=(
            # Bosola offers the Duchess unripe (or doctored) apricots
            # in Act II.i, suspecting pregnancy. She accepts; her
            # discomfort and subsequent sudden labour confirm his
            # suspicion. The apricots are the first explicit
            # instrument Bosola wields (predecessor to the horoscope-
            # find, the prison provocations, the wax-figures
            # carriage). The instrument's effect is partial: Bosola
            # gains BELIEVED-confidence in the pregnancy.
            observe("bosola", at_location("duchess", "amalfi"), 7),
            observe("bosola", pregnant("duchess"), 7,
                    confidence=Confidence.BELIEVED,
                    slot=Slot.BELIEVED,
                    note="Bosola infers from her sudden discomfort "
                         "after the apricots; not yet certain"),
        ),
    ),

    Event(
        id="E_first_child_born",
        type="birth",
        τ_s=8, τ_a=22,
        participants={"mother": "duchess", "father": "antonio",
                      "child": "duchess_son"},
        effects=(
            # The first child is born secretly that same night. Antonio
            # and Cariola attend; the household commotion alerts
            # Bosola, who finds the horoscope at τ_s=9. The child is
            # the future Duchess's-son entity; he will survive (per
            # Delio's closing speech) to inherit.
            world(parent_of("duchess", "duchess_son")),
            world(parent_of("antonio", "duchess_son")),
            world(at_location("duchess_son", "amalfi")),
            world(pregnant("duchess"), asserts=False),
            observe("duchess", parent_of("duchess", "duchess_son"), 8),
            observe("antonio", parent_of("antonio", "duchess_son"), 8),
            observe("cariola", parent_of("duchess", "duchess_son"), 8),
            # Crucially: NO one outside the household knows the child
            # exists. Bosola's discovery is via the dropped horoscope
            # at τ_s=9.
        ),
    ),

    Event(
        id="E_horoscope_dropped",
        type="instrument_dropped",
        τ_s=9, τ_a=23,
        participants={"who": "antonio", "found_by": "bosola"},
        effects=(
            # Antonio, distracted by the birth-night commotion, drops
            # a paper bearing the infant's horoscope. Bosola finds it;
            # the substrate marks both the predicate (the horoscope
            # exists as an instrument) and the read-effect on Bosola
            # (he acquires the child's existence as KNOWN, transferred
            # from his earlier BELIEVED-pregnancy state).
            world(horoscope_dropped("antonio")),
            observe("bosola", horoscope_dropped("antonio"), 9,
                    note="Bosola reads the horoscope and infers"),
            observe("bosola", parent_of("duchess", "duchess_son"), 9,
                    confidence=Confidence.CERTAIN,
                    slot=Slot.KNOWN,
                    note="the horoscope establishes the child's "
                         "existence; Bosola does not yet know the "
                         "father"),
            # The horoscope does NOT name Antonio as father; the
            # substrate reflects this — Bosola moves from BELIEVED
            # to KNOWN about the child's *existence* but his belief
            # about the *father* remains absent until the post-flight
            # discovery.
            remove_held("bosola", pregnant("duchess"),
                        slot=Slot.BELIEVED,
                        confidence=Confidence.BELIEVED,
                        τ=9,
                        note="superseded by certain knowledge of birth"),
        ),
    ),

    Event(
        id="E_bosola_letters_ferdinand",
        type="report",
        τ_s=10, τ_a=24,
        participants={"sender": "bosola", "recipient": "ferdinand"},
        effects=(
            # Bosola sends a letter to Ferdinand reporting the birth.
            # Ferdinand reads it; the substrate transfers the child's
            # existence as KNOWN to Ferdinand (and, through Ferdinand
            # at the next sibling-conference, the Cardinal).
            told_by("ferdinand", "bosola",
                    parent_of("duchess", "duchess_son"), 10,
                    confidence=Confidence.BELIEVED,
                    slot=Slot.BELIEVED,
                    note="Bosola's letter — Ferdinand believes it but "
                         "the letter is silent on the father"),
            # Ferdinand's reaction (his rage at the Duchess's sexual
            # secrecy, the "I could kill her now" scene with the
            # Cardinal) is structurally at this τ_s; the substrate
            # records the knowledge transfer; the affect lives on
            # descriptions (Session 3).
        ),
    ),

    # --- Act III: confrontation, flight, banishment, capture ---

    Event(
        id="E_ferdinand_confronts_duchess",
        type="confrontation",
        τ_s=11, τ_a=30,
        participants={"confronter": "ferdinand", "confronted": "duchess"},
        effects=(
            # Several years' time-compression (Webster glosses over
            # the birth of two additional children); Ferdinand
            # finally arrives in person with a dagger, in the
            # Duchess's bedchamber. He does not name Antonio; he
            # accuses her of unchastity. She does not confirm the
            # marriage. The encoded fact: Ferdinand now BELIEVES
            # she has remarried (the dagger gesture + his speeches
            # signal this); she does not confirm.
            observe("ferdinand", at_location("duchess", "amalfi"), 11),
            observe("duchess",   at_location("ferdinand", "amalfi"), 11),
            # Ferdinand's belief about the marriage upgrades from
            # BELIEVED to STRONG-BELIEVED but he has no name. The
            # substrate marks the elevated suspicion.
            observe("ferdinand", secret_marriage("duchess", "antonio"), 11,
                    confidence=Confidence.BELIEVED,
                    slot=Slot.BELIEVED,
                    note="Ferdinand suspects but has not identified "
                         "Antonio"),
        ),
    ),

    Event(
        id="E_duchess_devises_pilgrimage",
        type="plan",
        τ_s=13, τ_a=31,
        participants={"who": "duchess",
                      "partner": "antonio",
                      "witness": "cariola"},
        effects=(
            # The Duchess devises the cover-story of a pilgrimage to
            # Loretto (a real Marian shrine; the pilgrimage is the
            # public reason; the actual reason is to put her family
            # beyond Ferdinand's immediate grasp). Cariola disapproves
            # ("I do not like this jesting with religion"); the
            # substrate records the plan but not the religious-
            # ambiguity (which lives on descriptions).
            observe("antonio", at_location("antonio", "amalfi"), 13),
            observe("cariola", at_location("cariola", "amalfi"), 13),
        ),
    ),

    Event(
        id="E_flight_to_ancona",
        type="travel",
        τ_s=14, τ_a=32,
        participants={"who_1": "duchess", "who_2": "antonio",
                      "destination": "ancona",
                      "with_child": "duchess_son"},
        effects=(
            # The Duchess, Antonio, and the eldest son travel to
            # Ancona under the pilgrimage cover. The two younger
            # children remain at Amalfi (Webster compresses; the
            # encoding follows). Cariola accompanies; her knowledge
            # of the marriage makes her structurally attached.
            world(at_location("duchess",     "ancona"), asserts=True),
            world(at_location("duchess",     "amalfi"), asserts=False),
            world(at_location("antonio",     "ancona"), asserts=True),
            world(at_location("antonio",     "amalfi"), asserts=False),
            world(at_location("cariola",     "ancona"), asserts=True),
            world(at_location("cariola",     "amalfi"), asserts=False),
            world(at_location("duchess_son", "ancona"), asserts=True),
            world(at_location("duchess_son", "amalfi"), asserts=False),
            observe("duchess", at_location("duchess", "ancona"), 14),
            observe("antonio", at_location("antonio", "ancona"), 14),
            observe("cariola", at_location("cariola", "ancona"), 14),
        ),
    ),

    Event(
        id="E_banishment_at_loretto",
        type="banishment",
        τ_s=15, τ_a=33,
        participants={"banished_1": "duchess",
                      "banished_2": "antonio",
                      "banished_3": "duchess_son",
                      "performed_by": "cardinal",
                      "location": "loretto"},
        effects=(
            # The Cardinal performs a public banishment ritual at the
            # Loretto shrine (Webster stages this as a dumb-show with
            # the Cardinal installed as a soldier ahead of the
            # Forli campaign — he strips off ecclesiastical robes,
            # invests himself with arms, then performs the banishment
            # of the Duchess and Antonio). This is the moment the
            # secret_marriage() becomes known to the public — the
            # Cardinal has acted on it openly. The substrate marks
            # Antonio's identity-as-spouse becoming known to the
            # Cardinal (and through him, Ferdinand, who is not
            # present at Loretto but is reported to).
            world(at_location("cardinal", "loretto")),
            world(at_location("duchess",  "loretto")),
            world(at_location("antonio",  "loretto")),
            world(banished("duchess", "amalfi")),
            world(banished("antonio", "amalfi")),
            world(banished("duchess_son", "amalfi")),
            # By this point the Cardinal knows the marriage and the
            # spouse's identity (Ferdinand's intelligencers reporting
            # from Ancona). He performs the banishment as the
            # Aragonese family's collective political act.
            observe("cardinal",  secret_marriage("duchess", "antonio"), 15,
                    confidence=Confidence.CERTAIN, slot=Slot.KNOWN),
            observe("duchess",   banished("duchess", "amalfi"), 15),
            observe("antonio",   banished("antonio", "amalfi"), 15),
        ),
    ),

    Event(
        id="E_duchess_sends_antonio_away",
        type="separation",
        τ_s=16, τ_a=34,
        participants={"sender": "duchess", "sent": "antonio",
                      "with_child": "duchess_son"},
        effects=(
            # After the banishment the Duchess separates from Antonio
            # for safety: he travels onward with the eldest son to
            # Milan, while she remains with the two younger children
            # and Cariola. Webster makes the separation explicit and
            # tearful; it is the last meeting in life between
            # husband and wife. (Antonio sees the Duchess again only
            # in the wax-figure deception at τ_s=20; he learns of
            # her death only via Delio later in Act V.)
            world(at_location("antonio",     "ancona"), asserts=False),
            world(at_location("duchess_son", "ancona"), asserts=False),
            # Antonio and the eldest son travel onward — destination
            # Milan, then Rome (the Cardinal's palace). The substrate
            # tracks "in transit / unknown to other principals" via
            # absence of at_location() rather than authoring a
            # transit predicate.
            observe("antonio", at_location("duchess", "ancona"), 16,
                    note="the parting"),
            observe("duchess", at_location("antonio", "ancona"), 16,
                    note="the parting"),
        ),
    ),

    Event(
        id="E_capture_in_countryside",
        type="capture",
        τ_s=17, τ_a=35,
        participants={"captor": "bosola", "captured": "duchess",
                      "also_captured_1": "cariola"},
        effects=(
            # Bosola intercepts the Duchess in the countryside between
            # Ancona and Amalfi (Webster compresses geography; the
            # encoding uses 'countryside' as a single waypoint). The
            # two younger children are with her; they are captured
            # alongside (not authored as entities, but their
            # captivity is recorded at world-level via the
            # E_strangling event below).
            #
            # ** Structural marker: OQ-LEAR-4 main-arc peripeteia. **
            # Up to this point the Duchess's concealment was holding;
            # at τ_s=17 it collapses utterly. Her arc reverses from
            # secret-but-flourishing (children, marriage, intact
            # household) to captured-and-doomed. The Aristotelian
            # overlay (Session 2) will mark this event as
            # peripeteia_event_id for the Duchess's main arc.
            world(at_location("duchess",  "countryside")),
            world(at_location("cariola",  "countryside")),
            world(at_location("bosola",   "countryside")),
            world(at_location("duchess",  "ancona"), asserts=False),
            world(captured("duchess", "bosola")),
            world(captured("cariola", "bosola")),
            observe("bosola",  captured("duchess", "bosola"), 17,
                    note="Bosola masked; the Duchess does not yet "
                         "know who the captor is — Webster makes "
                         "the mask explicit"),
            observe("duchess", captured("duchess", "bosola"), 17,
                    confidence=Confidence.BELIEVED,
                    slot=Slot.BELIEVED,
                    note="she suspects Ferdinand's hand but not yet "
                         "the executor's identity"),
            observe("cariola", captured("duchess", "bosola"), 17),
        ),
    ),

    # --- Act IV: imprisonment, torture, strangling, corpse-recognitions ---

    Event(
        id="E_imprisonment",
        type="confinement",
        τ_s=18, τ_a=40,
        participants={"who": "duchess", "with": "cariola",
                      "at": "prison_cell"},
        effects=(
            # The Duchess and Cariola are returned to Amalfi and
            # confined. The two younger children are imprisoned with
            # them (asserted at world-level only; no entity records).
            # Ferdinand and Bosola have free access; the Cardinal
            # is in Rome.
            world(at_location("duchess",  "prison_cell")),
            world(at_location("cariola",  "prison_cell")),
            world(at_location("duchess",  "countryside"), asserts=False),
            world(at_location("cariola",  "countryside"), asserts=False),
            world(imprisoned("duchess")),
            world(imprisoned("cariola")),
            observe("duchess", imprisoned("duchess"), 18),
            observe("cariola", imprisoned("cariola"), 18),
            observe("ferdinand", at_location("duchess", "prison_cell"), 18),
            observe("bosola",    at_location("duchess", "prison_cell"), 18),
        ),
    ),

    Event(
        id="E_dead_hand_scene",
        type="instrument_torture",
        τ_s=19, τ_a=41,
        participants={"tormentor": "ferdinand", "victim": "duchess"},
        effects=(
            # Ferdinand presents the Duchess in the darkened cell with
            # a severed hand (a dead man's hand bearing a wedding
            # ring). She believes — Ferdinand intends she believe —
            # that the hand is Antonio's. The substrate authors the
            # instrument-predicate and the belief-effect on the
            # Duchess; the world-level fact (the hand is NOT
            # Antonio's) is encoded as a separate dead() retraction
            # for Antonio (omitted — the substrate cannot encode
            # NOT-dead since dead() is added on death only; the
            # encoding instead relies on the absence of dead(antonio)
            # at τ_s=19, with Antonio's actual death authored at
            # τ_s=30).
            world(dead_hand_displayed("ferdinand", "duchess")),
            observe("duchess", dead_hand_displayed("ferdinand", "duchess"), 19,
                    note="she takes the hand"),
            # Belief-effect: she believes Antonio is dead. The belief
            # is FALSE at τ_s=19; world-state-of-truth is corrected
            # only at τ_s=30 (her death precedes Antonio's; she dies
            # believing him dead).
            observe("duchess", dead("antonio"), 19,
                    confidence=Confidence.BELIEVED,
                    slot=Slot.BELIEVED,
                    note="the dead-hand persuades; she will die "
                         "believing him already dead"),
        ),
    ),

    Event(
        id="E_waxworks_scene",
        type="instrument_torture",
        τ_s=20, τ_a=42,
        participants={"tormentor": "ferdinand", "victim": "duchess"},
        effects=(
            # A second torture: waxen figures of "dead" Antonio and
            # the children, displayed behind a curtain. Reinforces
            # the belief established at τ_s=19. The substrate
            # records the instrument; the dialect will be able to
            # read the dead-hand + waxworks pair as a coordinated
            # instrumental sequence.
            world(waxworks_displayed("ferdinand", "duchess")),
            observe("duchess", waxworks_displayed("ferdinand", "duchess"), 20,
                    note="figures of Antonio + the two younger "
                         "children, posed as corpses"),
        ),
    ),

    Event(
        id="E_madmen_masque",
        type="instrument_torture",
        τ_s=21, τ_a=43,
        participants={"commissioned_by": "ferdinand",
                      "performed_for": "duchess",
                      "witness": "cariola"},
        effects=(
            # Ferdinand sends a troupe of madmen — Webster's stage-
            # direction "Enter Eight Madmen" — to dance and rave
            # around the Duchess. The masque is the third torture.
            # Cariola is present; her own death is approaching.
            world(madmen_masque_performed("ferdinand", "duchess")),
            observe("duchess", madmen_masque_performed("ferdinand", "duchess"), 21),
            observe("cariola", madmen_masque_performed("ferdinand", "duchess"), 21),
        ),
    ),

    Event(
        id="E_strangling",
        type="multiple_killing",
        τ_s=22, τ_a=44,
        participants={"executor": "bosola",
                      "orderer": "ferdinand",
                      "primary_victim": "duchess",
                      "secondary_victim": "cariola",
                      "tertiary_victim": "duchess_son"},
        effects=(
            # Bosola strangles the Duchess. Cariola attempts to escape,
            # protests her unmarried status, claims she is pregnant —
            # all rejected — and is strangled. The two younger
            # children are then strangled offstage (Webster's stage-
            # direction "Enter executioners, with children strangled").
            # The eldest son is, at this point, with Antonio in transit
            # (not at the prison; he is not killed here — Webster's
            # narrative protects him for the closing scene).
            #
            # ** Substrate fact corrections. ** The two younger children
            # are not entities in the encoding but their strangling is
            # asserted via the participants dict and via a
            # generic-strangled assertion on the duchess_son line —
            # which is INCORRECT. Correction: the eldest son
            # (duchess_son) is NOT strangled at τ_s=22; he is in
            # transit with Antonio. The participants tertiary_victim
            # is a role-label for "the children killed at this event"
            # that the encoding handles via the strangled() predicate
            # asserted on the participants. Authorial reticence: the
            # two unnamed younger children are not authored as
            # entities, so their strangling is recorded at participant-
            # level only.
            world(ordered_killing("ferdinand", "duchess")),
            world(ordered_killing("ferdinand", "cariola")),
            world(killed("bosola", "duchess")),
            world(killed("bosola", "cariola")),
            world(strangled("duchess")),
            world(strangled("cariola")),
            world(dead("duchess")),
            world(dead("cariola")),
            observe("bosola",    killed("bosola", "duchess"), 22,
                    note="Bosola executes; his anagnorisis is "
                         "imminent at τ_s=23"),
            observe("ferdinand", ordered_killing("ferdinand", "duchess"), 22),
            # Witnesses to the strangling: Bosola, Ferdinand (he is
            # offstage in this scene but arrives immediately after);
            # the executioners are not entities. The Duchess herself,
            # at the moment of death, is recorded as observing only
            # her own act-of-dying — Webster: "I am Duchess of Malfi
            # still." Substrate-wise, dying agents do not retain
            # post-death held-states; the observation is on the
            # dying-side τ_s=22 boundary.
            observe("duchess", dead("antonio"), 22,
                    confidence=Confidence.BELIEVED,
                    slot=Slot.BELIEVED,
                    note="she dies still believing Antonio dead — "
                         "the false belief from the dead-hand scene "
                         "is never corrected for her"),
        ),
    ),

    Event(
        id="E_ferdinand_views_corpse",
        type="recognition_reversal",
        τ_s=23, τ_a=45,
        participants={"viewer": "ferdinand", "corpse": "duchess"},
        effects=(
            # Ferdinand enters and sees the Duchess's body. The
            # canonical line "Cover her face; mine eyes dazzle: she
            # died young" lands here. The reversal is immediate: he
            # turns on Bosola ("I bade thee, when I was distracted of
            # my wits, / Go kill my dearest friend, and thou hast
            # done't.").
            #
            # ** Structural marker: OQ-LEAR-4 Ferdinand-arc peripeteia. **
            # His arc reverses from tormentor to madman in this
            # event. Webster makes the recognition explicit at the
            # same beat as the reversal — Ferdinand cannot
            # comprehend his own act and his mind collapses. mad()
            # acquired here; lycanthropy() at τ_s=25 marks the
            # transformation's behavioural shape.
            observe("ferdinand", at_location("duchess", "prison_cell"), 23),
            observe("ferdinand", dead("duchess"), 23,
                    note="'she died young' — the recognition lands"),
            world(mad("ferdinand")),
            observe("ferdinand", mad("ferdinand"), 23,
                    confidence=Confidence.BELIEVED,
                    slot=Slot.BELIEVED,
                    note="self-recognition of the mind's collapse, "
                         "in the same instant as the corpse-recognition"),
        ),
    ),

    Event(
        id="E_bosola_resolves_revenge",
        type="recognition_reversal",
        τ_s=24, τ_a=46,
        participants={"viewer": "bosola", "corpse": "duchess"},
        effects=(
            # Bosola alone with the body. The Duchess briefly revives
            # (Webster gives her a few last words: "Mercy."), then dies
            # again. Bosola attempts to attend to her body and
            # resolves to seek vengeance — initially on Antonio's
            # behalf, ultimately against both Ferdinand and the
            # Cardinal.
            #
            # ** Structural marker: OQ-LEAR-4 Bosola-arc peripeteia. **
            # The corpus's most explicit mid-play character-arc-reversal:
            # the instrument becomes the avenger. The Aristotelian
            # overlay (Session 2) will mark this event as the
            # peripeteia_event_id for Bosola's arc, distinct from the
            # Duchess's own peripeteia at τ_s=17 and Ferdinand's at
            # τ_s=23.
            world(avenger("bosola")),
            observe("bosola", dead("duchess"), 24,
                    note="he realises the full shape of what he has "
                         "executed"),
            observe("bosola", avenger("bosola"), 24,
                    note="'I am angry with myself, now that I wake.' "
                         "the instrument's recognition lands"),
        ),
    ),

    # --- Act V: lycanthropy, night-violence, the heir returns ---

    Event(
        id="E_ferdinand_lycanthropy",
        type="madness_manifest",
        τ_s=25, τ_a=50,
        participants={"who": "ferdinand", "at": "amalfi"},
        effects=(
            # Ferdinand's madness manifests as lycanthropy in Act V.ii.
            # Webster stages a court-physician scene where the doctor
            # (not an entity) reports Ferdinand "told me / He was a
            # wolf, only the difference / Was, a wolf's skin was
            # hairy on the outside, / His on the inside; bade them
            # take their swords, / Rip up his flesh, and try."
            # Substrate records the lycanthropy onset; descriptions
            # will carry the interpretive frame (real / hysterical /
            # punitive).
            world(lycanthropy("ferdinand")),
            world(at_location("ferdinand", "amalfi")),
            observe("ferdinand", lycanthropy("ferdinand"), 25,
                    note="the wolf-skin delusion"),
            observe("bosola",    lycanthropy("ferdinand"), 25,
                    note="Bosola witnesses; the news reaches the "
                         "Cardinal via report (not modelled)"),
        ),
    ),

    Event(
        id="E_cardinal_poisons_julia",
        type="killing",
        τ_s=27, τ_a=51,
        participants={"executor": "cardinal", "victim": "julia"},
        effects=(
            # Julia has extracted from the Cardinal a confession that
            # he ordered the Duchess's murder (she demanded the
            # confession as a love-token, in a scene where she
            # parodies the Duchess's role-inverting wooing). The
            # Cardinal, alarmed at what she now knows, has her kiss
            # the poisoned Bible to seal her oath of secrecy. She
            # dies in his presence, in pain. Bosola is hidden behind
            # the arras and overhears.
            world(poisoned_book("cardinal", "julia")),
            world(at_location("cardinal", "cardinals_palace")),
            world(at_location("julia",    "cardinals_palace")),
            world(at_location("bosola",   "cardinals_palace")),
            world(killed("cardinal", "julia")),
            world(poisoned("julia")),
            world(dead("julia")),
            observe("cardinal", killed("cardinal", "julia"), 27,
                    note="he watches her die; calculated"),
            observe("bosola",   killed("cardinal", "julia"), 27,
                    note="from behind the arras; Bosola now knows "
                         "the Cardinal kills witnesses"),
            observe("bosola",   ordered_killing("cardinal", "duchess"), 27,
                    confidence=Confidence.CERTAIN, slot=Slot.KNOWN,
                    note="Julia's confession (which Bosola overheard) "
                         "establishes the Cardinal's share in the "
                         "Duchess's murder, alongside Ferdinand's"),
        ),
    ),

    Event(
        id="E_bosola_visits_cardinal_at_night",
        type="dark_chamber_setup",
        τ_s=29, τ_a=52,
        participants={"visitor": "bosola", "host": "cardinal",
                      "at": "cardinals_palace"},
        effects=(
            # The Cardinal, anxious to dispose of Julia's body, asks
            # Bosola for help. He instructs his attendants that
            # whatever they hear from his chamber tonight — cries
            # for help included — is to be ignored ("howsoe'er he do
            # entreat you, be deaf to him"). Webster sets up the
            # dark-chamber chaos with this instruction. Substrate
            # marks the chamber-state as in_the_dark.
            world(in_the_dark("cardinals_palace")),
            observe("bosola",   at_location("cardinal", "cardinals_palace"), 29),
            observe("cardinal", at_location("bosola",   "cardinals_palace"), 29),
        ),
    ),

    Event(
        id="E_bosola_kills_antonio",
        type="mistaken_killing",
        τ_s=30, τ_a=53,
        participants={"killer": "bosola", "victim": "antonio",
                      "at": "cardinals_palace"},
        effects=(
            # Antonio, who has secretly returned to Rome to seek
            # reconciliation with the Cardinal (Delio's plan; Delio
            # accompanies him), enters the darkened palace and is
            # killed by Bosola, who mistakes him for the Cardinal
            # (or for one of the Cardinal's hired killers — the text
            # is ambiguous). Antonio dies in Bosola's arms after
            # the recognition.
            #
            # ** Structural marker: OQ-LEAR-4 Antonio-arc peripeteia. **
            # Anti-recognition: Antonio's death is the play's
            # bitterest reversal — he is killed by the man who
            # would have saved him, moments before reconciliation
            # was possible. Webster authors the dramatic irony
            # explicitly. The Aristotelian overlay (Session 2) will
            # mark this event as Antonio's arc peripeteia, an
            # anti-recognition event distinct from the corpse-view
            # recognitions of Ferdinand (τ_s=23) and Bosola (τ_s=24).
            world(at_location("antonio", "cardinals_palace")),
            world(at_location("delio",   "cardinals_palace")),
            world(killed("bosola", "antonio")),
            world(stabbed("antonio")),
            world(dead("antonio")),
            observe("bosola",  killed("bosola", "antonio"), 30,
                    note="the recognition arrives mid-stab"),
            observe("bosola",  dead("antonio"), 30),
            observe("delio",   dead("antonio"), 30,
                    note="Delio witnesses, survives, will carry "
                         "the closing speech"),
            # Antonio dies before he can transfer the final knowledge
            # (his location of the eldest son) explicitly; Delio
            # carries the son's information separately.
        ),
    ),

    Event(
        id="E_bosola_kills_cardinal",
        type="killing",
        τ_s=31, τ_a=54,
        participants={"killer": "bosola", "victim": "cardinal",
                      "at": "cardinals_palace"},
        effects=(
            # Bosola, having dispatched (mistakenly) Antonio, turns
            # his blade on the Cardinal. The Cardinal cries out;
            # his attendants, per his own earlier instruction
            # (τ_s=29), refuse to come to his aid. Webster's
            # blackest comedy in the play.
            world(killed("bosola", "cardinal")),
            world(stabbed("cardinal")),
            world(dead("cardinal")),
            observe("bosola",   killed("bosola", "cardinal"), 31,
                    note="the Cardinal cries out; no help comes"),
            observe("cardinal", dead("cardinal"), 31,
                    confidence=Confidence.BELIEVED,
                    slot=Slot.BELIEVED,
                    note="he knows he is dying — 'Look to my brother, / "
                         "He gave us these large wounds'"),
        ),
    ),

    Event(
        id="E_mutual_wounding_ferdinand_bosola",
        type="mutual_killing",
        τ_s=32, τ_a=55,
        participants={"agent_1": "ferdinand", "agent_2": "bosola",
                      "at": "cardinals_palace"},
        effects=(
            # Ferdinand enters in his lycanthropic state, attacks both
            # Bosola and the dying Cardinal. He wounds Bosola
            # mortally and is in turn stabbed by Bosola. Both die
            # within the same beat. Webster compresses the deaths
            # into a single confrontation; the substrate marks two
            # killed() relations and two dead() retractions of
            # alive().
            world(at_location("ferdinand", "cardinals_palace")),
            world(killed("ferdinand", "bosola")),
            world(killed("bosola",    "ferdinand")),
            world(stabbed("ferdinand")),
            world(stabbed("bosola")),
            world(dead("ferdinand")),
            world(dead("bosola")),
            observe("bosola",    killed("bosola", "ferdinand"), 32,
                    note="Bosola's last act of vengeance — he kills "
                         "the brother who ordered the Duchess's death"),
            observe("ferdinand", killed("ferdinand", "bosola"), 32,
                    note="in his madness Ferdinand cannot register "
                         "what he has done"),
            # Bosola's final speech ("Mine is another voyage") lands
            # here; his death is the play's last named one. Substrate
            # records his death as concurrent with Ferdinand's; the
            # τ_a sequence preserves authorial order (Ferdinand
            # registered as agent_1 to honour Webster's stage-
            # ordering).
        ),
    ),

    Event(
        id="E_delio_arrives_with_heir",
        type="closing",
        τ_s=33, τ_a=56,
        participants={"survivor": "delio", "heir": "duchess_son",
                      "at": "cardinals_palace"},
        effects=(
            # Delio arrives with the eldest son (the Duchess and
            # Antonio's child, who was with Antonio in transit
            # throughout Acts III-V). The eldest son is heir-
            # apparent to Amalfi; Delio's closing speech commends
            # him to Pescara and the surviving court ("In all our
            # quest of greatness, / Like wanton boys, whose
            # pastime is their care, / We follow after bubbles
            # blown in the air."). The substrate marks Delio +
            # son at the palace, the duchess_son's surviving
            # status (no dead()), and the location-update.
            world(at_location("delio",       "cardinals_palace")),
            world(at_location("duchess_son", "cardinals_palace")),
            observe("delio", dead("duchess"),   33,
                    note="Delio learns of the Duchess's fate at this "
                         "scene; he had been Antonio's friend, not "
                         "the Duchess's confidant"),
            observe("delio", dead("antonio"),   33),
            observe("delio", dead("cardinal"),  33),
            observe("delio", dead("ferdinand"), 33),
            observe("delio", dead("bosola"),    33),
            # The eldest son, a child, observes the carnage but
            # acquires beliefs about it that the substrate does not
            # authoritatively track; deferred to Session 3.
        ),
    ),

]


# ----------------------------------------------------------------------------
# Rules — inference-model-sketch-01 N1–N10
# ----------------------------------------------------------------------------
#
# Zero compound predicates in Session 1. Webster's killings do not
# reduce to direct-shape derivations:
#
# - The Duchess's strangling: Ferdinand and the Cardinal *ordered*;
#   Bosola *executed*. A "sibling-orchestrated killing" predicate
#   would require a 3-place rule (orderer, executor, victim) with
#   the orderer-sibling-of-victim and the executor-killed-victim
#   relations. Possible to author but more substantial than Session-1
#   discipline allows; deferred.
#
# - Bosola's killings of the Cardinal and Ferdinand at τ_s=31-32 are
#   not kin-killings (Bosola is no relation to either) and do not
#   trigger fratricide-shape rules.
#
# - The Cardinal's killing of Julia is not kin-killing (she is his
#   lover, not relative).
#
# - Antonio's killing by Bosola is mistaken, not ordered; no
#   compound shape captures the anti-recognition without taxing
#   the substrate's predicate machinery.
#
# Session 2 (Aristotelian overlay) and Session 3 (descriptions) will
# carry the structural-shape reading without needing substrate-level
# compound derivations. The pattern parallels Oedipus's Session 1 —
# the encoding ships zero rules and lets the dialect layers carry
# the interpretive shape.

RULES = ()


# ============================================================================
# Session 3 — PREPLAY_DISCLOSURES + SJUZHET + DESCRIPTIONS
# ============================================================================


# ----------------------------------------------------------------------------
# Preplay disclosures
# ----------------------------------------------------------------------------
#
# What does a Jacobean audience know coming into *The Duchess of Malfi*?
# Less than for Hamlet (the regicide is pre-loaded by folklore + the
# Ghost's exposition) and less than for Macbeth (the witch-prophecy
# tradition pre-loads supernatural agency). Webster's play opens with
# Antonio's return from France in the Duchess's court — a clean
# expository slate, with the opening dialogue between Delio and
# Antonio establishing the dramatis personae fresh.
#
# Four pre-play disclosures: the Aragonese family structure (Duchess
# + Ferdinand + Cardinal as siblings), the Duchess's widowhood and
# her sovereignty over Amalfi, the Cardinal's ecclesiastical office,
# and Ferdinand's ducal title (Calabria). These are the elements the
# audience grasps within the first hundred lines and that the
# play's action depends on knowing.
#
# Deliberately NOT in preplay: the secret marriage, Bosola's
# intelligencer commission, Ferdinand's psychic obsession with his
# sister, the Cardinal's relationship with Julia. Each is established
# *during* the action. The audience's gradual acquisition of these
# is the play's primary epistemic engine — especially the secret
# marriage, whose acquisition by Ferdinand+Cardinal across Acts II-III
# is the play's central dramatic-irony arc.
#
# These four mirror Lear's "minimal disclosures" posture (Lear shipped
# six; Hamlet shipped seven with the Ghost-lore included). Webster
# is the corpus's lightest preplay-knowledge encoding.

PREPLAY_DISCLOSURES = (
    Disclosure(prop=sibling_of("ferdinand", "duchess"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=sibling_of("cardinal", "duchess"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=duchess_of("duchess", "amalfi"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=widow("duchess"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=churchman("cardinal"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=duke_of("ferdinand", "calabria"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
)


# ----------------------------------------------------------------------------
# Sjuzhet — largely linear; τ_d ≈ τ_s ordering for in-play events.
# ----------------------------------------------------------------------------
#
# The five pre-play events (E_aragon_family, E_duchess_widowed,
# E_cardinal_julia_liaison, E_bosola_galley_service,
# E_antonio_returns_from_france) span τ_s=-30 to τ_s=-3. Of these,
# only E_antonio_returns_from_france is staged — it IS Webster's
# opening scene (Delio welcomes Antonio back from France, Act I.i).
# The other four are standing facts; their content reaches the
# audience through PREPLAY_DISCLOSURES at τ_d=0 (the opening
# scene's first entry) and through subsequent exposition.
#
# Focalization distribution (30 in-play sjuzhet entries):
#   duchess:    10 entries  (wooing/marriage/pregnancy/pilgrimage/
#                            parting/imprisonment/3-tortures/strangling)
#   bosola:      7 entries  (commission-acceptance/apricot/horoscope/
#                            capture/corpse-resolve/kills-antonio/
#                            kills-cardinal)
#   ferdinand:   5 entries  (warning/letter-reading/bedchamber/
#                            corpse-view/lycanthropy)
#   cardinal:    2 entries  (Julia poisoning, night-room setup)
#   antonio:     2 entries  (return + welcome, first child birth)
#   delio:       1 entry    (closing speech with heir)
#   None:        3 entries  (the Loretto banishment dumb-show, the
#                            flight to Ancona, the mutual-wounding
#                            chaos)
#
# Bosola's near-Duchess focalization count (7 vs 10) is the
# substrate-layer surface for the critical-tradition reading that
# Bosola is the play's structural co-protagonist (Empson 1935, Lucas
# 1927/1958, Bradbrook 1980). The Duchess is the title character and
# the principal pathos site; Bosola is the structural witness and
# the play's recognition-and-reversal carrier. The 17-point Bosola/
# Duchess focalization sum (10+7) is the corpus's most concentrated
# bi-focal distribution — contrast Lear (17 lear / 6 edmund / 5
# edgar / 5 gloucester = wide), Hamlet (12 hamlet + 4 others = single-
# focal-dominant), and Oedipus (10 oedipus + 4 others = single-focal-
# dominant).
#
# The 5-entry Ferdinand share reflects his role as orchestrator-also-
# recognizer (corpus first per Session 2 — Aristotelian overlay). The
# Cardinal's 2-entry share is structurally minimal — Webster gives him
# few solo scenes; he is a recurring antagonist but rarely the
# scene's focalizing center. The 3 None entries cover ceremonial
# (Loretto), in-transit (flight), and chaotic-multi-agent (the
# mutual-wounding finale).

SJUZHET = [

    # τ_d=0 — Act 1 Scene 1 opens. Antonio's return from France;
    # Delio's welcome. The play's first staged event. Antonio
    # focalizes — the welcome is to him, the dialogue is between
    # him and Delio, and Webster gives Antonio the opening
    # exposition ('In seeking to reduce both State and People /
    # To a fix'd order, their judicious King / Begins at home').
    # PREPLAY_DISCLOSURES attach here.
    SjuzhetEntry(
        event_id="E_antonio_returns_from_france",
        τ_d=0,
        focalizer_id="antonio",
        disclosures=PREPLAY_DISCLOSURES,
    ),

    # τ_d=1 — Act 1 Scene 1 mid: the Cardinal + Ferdinand confer,
    # then jointly warn the Duchess against remarriage. Ferdinand
    # focalizes — his speeches dominate the warning scene
    # ('Marry! they are most luxurious / Will wed twice'), his
    # affect is the scene's primary register, and Webster gives
    # him the famous incest-undertone speech ('Inform her... /
    # Of his low birth and dowerless state'). The Duchess's
    # response is brief; the warning is Ferdinand's.
    SjuzhetEntry(
        event_id="E_brothers_warn_duchess",
        τ_d=1,
        focalizer_id="ferdinand",
        disclosures=(),
    ),

    # τ_d=2 — Act 1 Scene 1 close: Ferdinand commissions Bosola.
    # Bosola focalizes — the scene's weight is his cynical
    # acceptance ('Take your devils, / Which hell calls angels;
    # these cursed gifts would make / You a corrupter, me an
    # impudent traitor; / And should I take these, they'd take
    # me to hell'). Self-aware corruption is the scene's
    # structural center; Ferdinand is the offerer, Bosola is the
    # accepter, but Bosola's reluctance-overcome is what Webster
    # foregrounds.
    SjuzhetEntry(
        event_id="E_ferdinand_hires_bosola",
        τ_d=2,
        focalizer_id="bosola",
        disclosures=(),
    ),

    # τ_d=3 — Act 1 Scene 1 final: the Duchess woos Antonio with
    # Cariola concealed. The Duchess focalizes — Webster gives her
    # the role-inverting speech ('The misery of us that are born
    # great! / We are forced to woo, because none dare woo us')
    # and the proposal is hers. Cariola is the witness; Antonio
    # is the recipient; the Duchess is the agent and the
    # focalizer.
    SjuzhetEntry(
        event_id="E_duchess_woos_antonio",
        τ_d=3,
        focalizer_id="duchess",
        disclosures=(),
    ),

    # τ_d=4 — Act 1 Scene 1 closing per-verba marriage. The Duchess
    # focalizes — the canon-law speech ('I have heard lawyers say,
    # a contract in a chamber / Per verba presenti, is absolute
    # marriage') is hers; the marriage's structural authority is
    # her assertion of it; the scene closes the act with her
    # voice carrying the action's stakes.
    SjuzhetEntry(
        event_id="E_secret_marriage",
        τ_d=4,
        focalizer_id="duchess",
        disclosures=(),
    ),

    # τ_d=5 — Act 2 Scene 1 implicit. The Duchess is visibly
    # pregnant; Webster opens Act II with Bosola noting her
    # changed appearance. The pregnancy event itself is
    # internal-state-change but the staged scene around it
    # establishes it for the audience. The Duchess focalizes —
    # the pregnancy is her body, her secrecy, her structural
    # vulnerability; Bosola's noting in the same scene becomes
    # the apricot-ploy at τ_d=6.
    SjuzhetEntry(
        event_id="E_duchess_pregnant_first",
        τ_d=5,
        focalizer_id="duchess",
        disclosures=(),
    ),

    # τ_d=6 — Act 2 Scene 1 mid: the apricot ploy. Bosola
    # focalizes — the scene's structural center is his
    # intelligencer's instrument (the apricots, possibly doctored),
    # his observation of the Duchess's discomfort, and his
    # inferential leap ('I have a strange suspicion / She has
    # had some pollution'). Webster foregrounds Bosola's mind
    # working through the test.
    SjuzhetEntry(
        event_id="E_apricot_ploy",
        τ_d=6,
        focalizer_id="bosola",
        disclosures=(),
    ),

    # τ_d=7 — Act 2 Scene 2 implicit. The first child is born
    # offstage during a household commotion. Webster gives Antonio
    # the worried-husband scene ('Heaven open all secret springs
    # of comfort / On her safe delivery!'). Antonio focalizes —
    # the birth is his structural moment as father, his anxiety
    # is the scene's weight, and his subsequent error (dropping
    # the horoscope) is the consequence-of-distraction.
    SjuzhetEntry(
        event_id="E_first_child_born",
        τ_d=7,
        focalizer_id="antonio",
        disclosures=(),
    ),

    # τ_d=8 — Act 2 Scene 3: Antonio drops the horoscope; Bosola
    # finds it. Bosola focalizes — the discovery is his, the
    # reading is his, the inference (the child's existence) is
    # his. Webster gives Bosola the soliloquy of inference ('I
    # have it! This is some boy's nativity, and the day / Of
    # birth'); the scene's structural center is the
    # intelligencer's confirmation of what the apricot-ploy
    # suggested.
    SjuzhetEntry(
        event_id="E_horoscope_dropped",
        τ_d=8,
        focalizer_id="bosola",
        disclosures=(),
    ),

    # τ_d=9 — Act 2 Scene 5: Ferdinand reads Bosola's letter,
    # rages. The scene's structural center is Ferdinand's
    # response — his 'Damn her! that body of hers' speech with
    # the Cardinal restraining him. Ferdinand focalizes — his
    # affect is the scene's weight, his violence-of-affect
    # establishes the play's psychic register, and the Cardinal's
    # restraining role positions him as the scene's secondary
    # foil.
    SjuzhetEntry(
        event_id="E_bosola_letters_ferdinand",
        τ_d=9,
        focalizer_id="ferdinand",
        disclosures=(),
    ),

    # τ_d=10 — Act 3 Scene 2: Ferdinand confronts the Duchess in
    # her bedchamber with a dagger. The scene's structural center
    # is Ferdinand's calculated entrance + dagger-gesture +
    # speech ('Die then, quickly!'); the Duchess responds but
    # does not confirm the marriage. Ferdinand focalizes — the
    # scene's pressure is what his appearance carries, and the
    # bedchamber's intimacy reads as transgression by his
    # presence in it. Webster's most psychologically dense scene
    # before the strangling.
    SjuzhetEntry(
        event_id="E_ferdinand_confronts_duchess",
        τ_d=10,
        focalizer_id="ferdinand",
        disclosures=(),
    ),

    # τ_d=11 — Act 3 Scene 2 close: the Duchess devises the
    # pilgrimage cover-story. The Duchess focalizes — the plan
    # is hers, Cariola's protest ('I do not like this jesting
    # with religion') is voiced but overruled, and the strategy
    # of fleeing-under-cover is the Duchess's response to
    # Ferdinand's pressure. Webster's stage-management has
    # Antonio listening + accepting; the Duchess is the agent
    # and the focalizer.
    SjuzhetEntry(
        event_id="E_duchess_devises_pilgrimage",
        τ_d=11,
        focalizer_id="duchess",
        disclosures=(),
    ),

    # τ_d=12 — Act 3 Scene 4 implicit (the family travels). The
    # flight to Ancona is in-transit; Webster compresses. No
    # single focalizer; the scene's structural weight is
    # geographical (movement away from Amalfi) rather than
    # character-internal. None focalizes.
    SjuzhetEntry(
        event_id="E_flight_to_ancona",
        τ_d=12,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=13 — Act 3 Scene 4: the Loretto banishment ritual. The
    # Cardinal performs a dumb-show — strips ecclesiastical robes,
    # invests himself with arms for the Forli campaign, then
    # banishes the Duchess + Antonio + eldest son. Webster's
    # stage-direction frames this as a dumb-show with two
    # pilgrim commentators describing the action. None focalizes
    # — the dumb-show is ceremonial and the pilgrims' commentary
    # is the audience-side reading; no single character carries
    # the scene's weight.
    SjuzhetEntry(
        event_id="E_banishment_at_loretto",
        τ_d=13,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=14 — Act 3 Scene 5: the Duchess parts from Antonio. The
    # Duchess focalizes — the parting speech ('Be a good mother
    # to your little ones, / And save them from the tiger') is
    # hers; her instructions to Antonio about the eldest son's
    # safety carry the scene; her recognition that this is the
    # last meeting in life is the scene's emotional weight.
    SjuzhetEntry(
        event_id="E_duchess_sends_antonio_away",
        τ_d=14,
        focalizer_id="duchess",
        disclosures=(),
    ),

    # τ_d=15 — Act 3 Scene 5 close: the capture in the
    # countryside. Bosola focalizes — the masked interception is
    # his, his speech to the Duchess ('You are a Duchess, but
    # there is a difference / Between the noblest and the
    # vilest woman') is the scene's verbal center, and his
    # masked-and-then-unmasking shape is the scene's structural
    # motion (the masking carries the dramatic-irony moment as
    # the Duchess does not yet know her captor's identity).
    # **This is the Duchess's main arc peripeteia** per
    # AR_MALFI_MYTHOS; the focalizer is Bosola because the
    # scene's structural agent is the captor, not the captured.
    SjuzhetEntry(
        event_id="E_capture_in_countryside",
        τ_d=15,
        focalizer_id="bosola",
        disclosures=(),
    ),

    # τ_d=16 — Act 4 Scene 1: the imprisonment opens. The
    # Duchess focalizes — the prison-cell scene's structural
    # center is her endurance; the famous 'I am Duchess of Malfi
    # still' will land at τ_d=20 but its register begins here
    # with her response to confinement ('I'll tell thee a
    # miracle; / I am not mad yet, to my cause of sorrow'). Her
    # stoic self-possession is the scene's primary affect.
    SjuzhetEntry(
        event_id="E_imprisonment",
        τ_d=16,
        focalizer_id="duchess",
        disclosures=(),
    ),

    # τ_d=17 — Act 4 Scene 1 mid: the dead-hand torture. The
    # Duchess focalizes — the scene's structural test is her
    # response to the deception, and Webster makes the test of
    # her stoicism the focal load. Ferdinand has left the chamber
    # darkened; the dead-hand is presented mute, with the
    # candle then lit revealing the figures. The Duchess's
    # speech ('What witchcraft doth he practise, that he hath
    # left / A dead man's hand here?') is the scene's
    # interpretive center.
    SjuzhetEntry(
        event_id="E_dead_hand_scene",
        τ_d=17,
        focalizer_id="duchess",
        disclosures=(),
    ),

    # τ_d=18 — Act 4 Scene 1 close: the waxworks torture. The
    # Duchess focalizes — the discovery of the wax figures of
    # 'dead' Antonio and the children is hers, the grief is
    # hers, the despair-speech ('There is not between heaven
    # and earth one wish / I stay for after this') is the scene's
    # weight.
    SjuzhetEntry(
        event_id="E_waxworks_scene",
        τ_d=18,
        focalizer_id="duchess",
        disclosures=(),
    ),

    # τ_d=19 — Act 4 Scene 2 opens: the madmen masque. The
    # Duchess focalizes — her endurance of the dance-of-madmen
    # is the scene's structural test, her speech to Cariola
    # about the madmen ('Th' heaven o'er my head seems made of
    # molten brass, / The earth of flaming sulphur') carries the
    # scene's affect; the masque is performed FOR her.
    SjuzhetEntry(
        event_id="E_madmen_masque",
        τ_d=19,
        focalizer_id="duchess",
        disclosures=(),
    ),

    # τ_d=20 — Act 4 Scene 2 close: the strangling. The Duchess
    # focalizes — the famous 'I am Duchess of Malfi still' is
    # hers, the scene's moral center is her defiance, Bosola is
    # the executor but the scene's structural weight is her
    # final speech. Webster makes the strangling structurally
    # her scene even though Bosola is the agent — her last words
    # carry; her death is the climax of her arc and the play's
    # primary pathos. Cariola's strangling immediately follows
    # (compressed into the same SJUZHET entry); the children's
    # strangling is offstage and authorial-reticent.
    SjuzhetEntry(
        event_id="E_strangling",
        τ_d=20,
        focalizer_id="duchess",
        disclosures=(),
    ),

    # τ_d=21 — Act 4 Scene 2 final: Ferdinand views the corpse.
    # **The main anagnorisis** per AR_MALFI_MYTHOS. Ferdinand
    # focalizes — the famous 'Cover her face; mine eyes dazzle:
    # she died young' is his line; the scene's recognition-and-
    # reversal lands in his speech; his madness-onset is the
    # scene's structural turn. The Duchess is dead and cannot
    # focalize.
    SjuzhetEntry(
        event_id="E_ferdinand_views_corpse",
        τ_d=21,
        focalizer_id="ferdinand",
        disclosures=(),
    ),

    # τ_d=22 — Act 4 Scene 2 epilogue: Bosola alone with the
    # corpse. Bosola focalizes — **the play's most explicit
    # mid-arc reversal**, the resolution to revenge, the
    # brief revival of the Duchess ('Mercy.') and her final
    # death, and Bosola's recognition speech ('I am angry with
    # myself, now that I wake'). Webster makes the scene
    # structurally Bosola's — the instrument's collapse into
    # avenger.
    SjuzhetEntry(
        event_id="E_bosola_resolves_revenge",
        τ_d=22,
        focalizer_id="bosola",
        disclosures=(),
    ),

    # τ_d=23 — Act 5 Scene 2: Ferdinand's lycanthropy. Webster
    # stages the court-physician scene where the doctor (not an
    # entity) reports Ferdinand's wolf-skin delusion. Ferdinand
    # focalizes — the lycanthropy is his; his behaviour is the
    # scene's structural weight; his speech 'Strangling is a
    # very quiet death' surfaces his persistent obsession with
    # the act he ordered.
    SjuzhetEntry(
        event_id="E_ferdinand_lycanthropy",
        τ_d=23,
        focalizer_id="ferdinand",
        disclosures=(),
    ),

    # τ_d=24 — Act 5 Scene 2 mid: the Cardinal poisons Julia.
    # The Cardinal focalizes — the calculation is his, the
    # poisoned-Bible setup is his, Julia is the recipient but
    # the Cardinal is the agent. Bosola is hidden behind the
    # arras and overhears the confession; his knowledge is
    # crucial but he is not the scene's focalizer (he is the
    # eavesdropper). The Cardinal's speech 'I am puzzled in a
    # question about hell' carries the scene.
    SjuzhetEntry(
        event_id="E_cardinal_poisons_julia",
        τ_d=24,
        focalizer_id="cardinal",
        disclosures=(),
    ),

    # τ_d=25 — Act 5 Scene 5 opens: Bosola visits the Cardinal.
    # The Cardinal focalizes — his instruction to attendants
    # ('howsoe'er he do entreat you, be deaf to him') is the
    # scene's setup, his calculation is the scene's structural
    # ground, his self-trapping is the scene's dramatic irony.
    # Webster's blackest-comedy is the Cardinal's instruction
    # turning against him.
    SjuzhetEntry(
        event_id="E_bosola_visits_cardinal_at_night",
        τ_d=25,
        focalizer_id="cardinal",
        disclosures=(),
    ),

    # τ_d=26 — Act 5 Scene 5 mid: Bosola kills Antonio by
    # mistake. **Antonio's arc peripeteia** per AR_STEP_ANTONIO_
    # DARK_RECOGNITION. Bosola focalizes — the dark-room
    # confusion is his, the stab is his, the recognition mid-
    # wound is his ('Antonio! / The man I would have sav'd
    # 'bove mine own life!'). Antonio is the victim and dies
    # almost immediately; the scene's structural agent is
    # Bosola. The anti-recognition shape is carried in his
    # speech.
    SjuzhetEntry(
        event_id="E_bosola_kills_antonio",
        τ_d=26,
        focalizer_id="bosola",
        disclosures=(),
    ),

    # τ_d=27 — Act 5 Scene 5 mid: Bosola kills the Cardinal.
    # Bosola focalizes — the stab is his, the Cardinal's cries
    # for help (ignored by attendants per the earlier
    # instruction) are the scene's dramatic irony, Bosola's
    # speech 'Now it seems thy greatness was only outward' is
    # the scene's verbal center.
    SjuzhetEntry(
        event_id="E_bosola_kills_cardinal",
        τ_d=27,
        focalizer_id="bosola",
        disclosures=(),
    ),

    # τ_d=28 — Act 5 Scene 5 close: the mutual wounding. Ferdinand
    # enters in his lycanthropic state and the three-way
    # confrontation collapses into mutual stabbings. No single
    # focalizer — Webster's scene is chaos with multiple
    # competing affects: Ferdinand's mad rage, the dying
    # Cardinal's bitter recognition, Bosola's final-act speech.
    # None focalizes the chaos.
    SjuzhetEntry(
        event_id="E_mutual_wounding_ferdinand_bosola",
        τ_d=28,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=29 — Act 5 Scene 5 final: Delio enters with the eldest
    # son. **The play's closing.** Delio focalizes — the closing
    # speech is his ('In all our quest of greatness, / Like
    # wanton boys, whose pastime is their care, / We follow
    # after bubbles blown in the air'), the structural payload
    # (the surviving heir entrusted to the audience's hope) is
    # his to carry, the scene's affect (rueful witness) is his.
    SjuzhetEntry(
        event_id="E_delio_arrives_with_heir",
        τ_d=29,
        focalizer_id="delio",
        disclosures=(),
    ),

]


# ----------------------------------------------------------------------------
# Descriptions — fold-invisible interpretive records
# ----------------------------------------------------------------------------
#
# Twelve descriptions covering:
#
#   1. Three character-register questions the substrate declines to
#      settle (Bosola's transformation, Ferdinand's lycanthropy, the
#      Cardinal's interiority).
#   2. Two character-motivation questions (the Duchess's marriage,
#      Antonio's passivity).
#   3. Three reader frames carrying the Session-2 OQ findings into
#      substrate scope (OQ-LEAR-4 four-arc-peripeteia,
#      OQ-AP7 third-encoding distance-6,
#      OQ-MALFI-1 sequentially-wielded-instrument).
#   4. Two thematic-structural readings (Webster's parodic-Catholic
#      setting, the play's instrument density relative to the
#      corpus).
#   5. Two iconic-line readings (the "Duchess of Malfi still"
#      moment, the eldest son's survival as structural payload).
#
# Probe-authored edits and answers are not present in Session 3;
# they would be added by Session 5's probe pass against Malfi.

DESCRIPTIONS = [

    Description(
        id="D_bosola_transformation_register_undecided",
        attached_to=anchor_event("E_bosola_resolves_revenge"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Bosola's reversal at τ_s=24 — alone with the "
              "Duchess's corpse, attempting revival, resolving to "
              "revenge — is substrate-recorded as the moment "
              "`avenger(bosola)` is asserted; what the reversal "
              "MEANS at character-register level is not. Three "
              "readings the text supports: (a) GENUINE REPENTANCE "
              "— Bosola recognizes his complicity in an act that "
              "exceeds what his hamartia (accepting the "
              "commission knowing the work was corrupting) "
              "allowed for, and turns to vengeance as moral "
              "reconstruction; his subsequent killings of "
              "Cardinal and Ferdinand are then redemptive even as "
              "they consume him. (b) HIRELING RESENTMENT — Bosola "
              "was always going to turn on whoever betrayed him; "
              "the Duchess's body is the proximate cause but his "
              "structural disposition was prior; the avenger-arc "
              "is character-internal and not particularly moral. "
              "(c) DAMNATION-VIA-RECOGNITION — Bosola sees what "
              "he has done and cannot un-do it; his subsequent "
              "acts (the night-room sequence, the killing of "
              "Antonio by mistake) are post-redemption damnation, "
              "where the recognition arrives but cannot save. The "
              "substrate commits to none of these. Bosola's last "
              "speech ('Mine is another voyage') names the "
              "transit but not its destination. Webster's dark "
              "comedy of moral ambiguity is the substrate's "
              "position — the reversal is structural, the moral "
              "register is reader-side. Sketch-04 OQ-AP14's "
              "instrumental-relation discipline carries the "
              "structural arc; descriptions-layer carries the "
              "interpretive question."),
        is_question=True,
        authored_by="author",
        τ_a=200,
    ),

    Description(
        id="D_ferdinand_lycanthropy_register_undecided",
        attached_to=anchor_event("E_ferdinand_lycanthropy"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Ferdinand's lycanthropy at τ_s=25 — the wolf-skin "
              "delusion, the graveyard-digging, the howling — is "
              "substrate-recorded as `lycanthropy(ferdinand)`; "
              "what the transformation IS in the play's "
              "ontology is not. Four candidate readings: (a) "
              "CLINICAL — Ferdinand suffers a real psychiatric "
              "lycanthropic condition (a textually-attested early-"
              "modern diagnostic category; Robert Burton's "
              "*Anatomy of Melancholy* describes it). The "
              "doctor-scene treats it medically. (b) HYSTERICAL "
              "— Webster's dark comedy renders Ferdinand's "
              "madness as performance; the wolf-skin delusion is "
              "psychogenic rather than literal. (c) PUNITIVE — "
              "divine retribution for the Duchess's murder; the "
              "transformation is supernatural-providential, even "
              "if the play does not name a deity. (d) SYMBOLIC — "
              "Webster makes the brother's bestiality literal; "
              "the wolf-form is the moral truth of Ferdinand's "
              "possessive-incestuous violence rendered as flesh. "
              "Each reading carries the play differently: "
              "clinical reads as case-study; hysterical reads as "
              "satire of the brother-orchestrator's collapse; "
              "punitive reads as divine-providence-in-tragedy; "
              "symbolic reads as moral-allegorical. The substrate "
              "commits to none. Unlike Hamlet's feigning_madness "
              "(agent-level, never promoted to world-fact) and "
              "Lear's mad('lear') (world-asserted at storm-onset, "
              "register left open by description), Webster's "
              "lycanthropy IS asserted at world-level as a "
              "specific behavioral shape — but the metaphysical "
              "register of the assertion is reader-side."),
        is_question=True,
        authored_by="author",
        τ_a=201,
    ),

    Description(
        id="D_cardinal_interiority_register_undecided",
        attached_to=anchor_event("E_cardinal_poisons_julia"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("The Cardinal has no soliloquy of self-reckoning in "
              "the entire play. Webster gives him brief moments "
              "of self-questioning ('I am puzzled in a question "
              "about hell'; 'How tedious is a guilty conscience!') "
              "but no extended interior monologue equivalent to "
              "Hamlet's 'To be or not to be', Edmund's 'Now, gods, "
              "stand up for bastards', or Macbeth's 'Tomorrow and "
              "tomorrow and tomorrow'. The Cardinal's substrate "
              "trace is calculation throughout: warning, "
              "Loretto-banishment-ritual, Julia-poisoning, "
              "body-disposal arrangement, killed-while-attendants-"
              "ignore. Three readings: (a) PURE CALCULATOR — "
              "Webster's anti-Catholic gibe; the prince of the "
              "Church is morally vacuous, his interiority is "
              "stage-machinery for political acts, his absence "
              "of soliloquy IS the character. (b) HIDDEN GRIEF — "
              "the Cardinal too loved his sister and the "
              "absence of self-reckoning is Webster's "
              "characteristic withholding of interiority that "
              "the audience would expect; the 'puzzled in a "
              "question about hell' line is the surface of "
              "depth he will not let us see. (c) PSYCHOPATHIC "
              "SHALLOWNESS — there is no interiority because "
              "there is nothing to render; the Cardinal is "
              "Webster's portrait of moral absence, distinct "
              "from Ferdinand's pathology and Bosola's "
              "self-aware corruption. Each reading would commit "
              "the play to a different anti-Catholic register; "
              "the substrate declines."),
        is_question=True,
        authored_by="author",
        τ_a=202,
    ),

    Description(
        id="D_duchess_marriage_motivation_undecided",
        attached_to=anchor_event("E_duchess_woos_antonio"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("The Duchess's wooing of Antonio at τ_s=3 is "
              "substrate-recorded as her initiative; what drives "
              "the initiative is not. Three readings the text "
              "supports: (a) LOVE — the Duchess genuinely loves "
              "Antonio (the role-reversed wooing scene, with its "
              "explicit acknowledgment of the rank-gap and "
              "explicit consent-clearing, reads as careful "
              "courtship rather than impulsive). (b) DEFIANCE — "
              "the brothers' opening warning at τ_s=0 against "
              "remarriage prompts the act; without the warning, "
              "the Duchess might not have proposed; the marriage "
              "is structurally a response. (c) PRINCIPLE — the "
              "per-verba marriage is canonically valid by the "
              "play's standards, the Duchess's articulation "
              "('I have heard lawyers say, a contract in a "
              "chamber / Per verba presenti, is absolute "
              "marriage') deploys legal-religious authority; the "
              "marriage is right by the canonical frame and the "
              "Duchess is asserting that rightness. The "
              "substrate commits to none. Cordelia's "
              "motivation-question (D_cordelia_motivation_"
              "undecided in lear.py) is the parallel — both "
              "tragic-hero women elect an act that defies "
              "male-orchestrated expectations, and both "
              "rationales (honesty/pride/faith for Cordelia; "
              "love/defiance/principle for the Duchess) are "
              "left textually plural. The pattern is corpus-"
              "wide: female tragic-hero motivation under male-"
              "pressured circumstances tends to authorial "
              "reticence."),
        is_question=True,
        authored_by="author",
        τ_a=203,
    ),

    Description(
        id="D_antonio_passivity_register",
        attached_to=anchor_event("E_bosola_kills_antonio"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Antonio's arc is structurally reactive throughout: "
              "wooed (he does not initiate), fled (the Duchess "
              "directs), separated (the Duchess sends him away), "
              "killed (Bosola in the dark, by mistake). The "
              "play's anti-tragic-hero shape per malfi_"
              "aristotelian.py's `AR_ANTONIO.is_tragic_hero="
              "False`. Two reading-registers: (a) PASSIVE "
              "RECIPIENT OF FORTUNE — Antonio carries the marital "
              "fate without agency; his death by mistake is the "
              "extension of his structural passivity into the "
              "final beat; his arc is the play's saddest because "
              "least chosen. (b) FULLY-CONSENSUAL PARTICIPANT — "
              "Antonio's acceptance of the Duchess's proposal is "
              "active consent across the rank-gap, his "
              "willingness to abandon his children with her at "
              "the parting is a moral decision, his return to "
              "Rome for reconciliation with the Cardinal is "
              "deliberate; his death is tragic precisely because "
              "the chosen-path turns at the last instant from "
              "reconciliation to murder-in-the-dark. The "
              "substrate's reactive trace (Antonio observes more "
              "than he initiates across the play's events) is "
              "consistent with reading (a); but Antonio's "
              "world-fact involvement (accepting the marriage, "
              "co-parenting, returning to Rome) is consistent "
              "with reading (b). The Aristotelian overlay's "
              "is_tragic_hero=False marks the absence of "
              "classical hamartia-with-deliberation, not the "
              "absence of agency. The descriptions-layer carries "
              "the question."),
        is_question=True,
        authored_by="author",
        τ_a=204,
    ),

    Description(
        id="D_oq_lear_4_reader_frame",
        attached_to=anchor_event("E_strangling"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("**OQ-LEAR-4 substrate-layer reader frame.** Webster's "
              "*Duchess of Malfi* authors four structurally-distinct "
              "character-arc peripeteia events within a single "
              "mythos: the Duchess at E_capture_in_countryside "
              "(τ_s=17, main arc reversal), Ferdinand at "
              "E_ferdinand_views_corpse (τ_s=23, tormentor→madman), "
              "Bosola at E_bosola_resolves_revenge (τ_s=24, "
              "instrument→avenger), Antonio at E_bosola_kills_"
              "antonio (τ_s=30, anti-recognition). The dialect's "
              "single `peripeteia_event_id` slot at "
              "AR_MALFI_MYTHOS scope carries one of the four (the "
              "Duchess's at τ_s=17); the main anagnorisis slot at "
              "AR_MALFI_MYTHOS.anagnorisis_event_id carries "
              "Ferdinand's recognition at τ_s=23; the anagnorisis "
              "chain steps (AR_STEP_BOSOLA_RESOLVES, AR_STEP_"
              "ANTONIO_DARK_RECOGNITION) carry the third and "
              "fourth under semantic stretch of A11. The "
              "uneven-distribution of structural information "
              "across these four sites is OQ-LEAR-4's substrate "
              "signature.\n\n"
              "Reader-side question (Session 5 probe): do you "
              "read the four peripeteia events as structurally "
              "coordinated (one unified arc-shape with four "
              "instantiation sites) or as structurally distinct "
              "(four separate arcs converging by accident)? The "
              "dialect's current shape forces the latter "
              "reading; the candidate sketch-06 extension "
              "(`secondary_peripeteia_event_ids` field per "
              "malfi_aristotelian.py's OQ_LEAR_4_FINDING) would "
              "support the former. Cross-encoding pressure with "
              "Lear's Gloucester-subplot peripeteia is now real."),
        is_question=True,
        authored_by="author",
        τ_a=210,
    ),

    Description(
        id="D_oq_ap7_reader_frame",
        attached_to=anchor_event("E_ferdinand_views_corpse"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("**OQ-AP7 substrate-layer reader frame.** Webster's "
              "peripeteia-anagnorisis distance is 6 (τ_s=17 → "
              "τ_s=23), the corpus narrowest SEPARATED. Three "
              "encodings under one dialect category exhibit three "
              "analytical shapes:\n\n"
              "- Webster's 6: INTENSE. The dense Act-IV "
              "  compression. Capture → imprisonment → three "
              "  tortures → strangling → recognition. Six τ_s "
              "  units span the unbinding-to-recognition arc; "
              "  the structural content is INTENSITY rather than "
              "  DELAY.\n"
              "- Hamlet's 9: DELAYED. The verification-to-belated-"
              "  recognition arc. The structural content IS the "
              "  delay (Hamlet's famous procrastination).\n"
              "- Lear's 14: ACCUMULATING. The slow-burn-of-"
              "  suffering arc. The structural content is the "
              "  ACCUMULATION of suffering before recognition.\n\n"
              "Three distinct analytical shapes, one dialect "
              "category. Reader-side question (Session 5 probe): "
              "do you read the three under a single 'separated' "
              "frame or do you spontaneously distinguish them? "
              "Webster's encoding presses the case for a "
              "tripartite refinement (intense / delayed / "
              "accumulating) or a numerical "
              "peripeteia_anagnorisis_distance field. See "
              "malfi_aristotelian.py's OQ_AP7_RE_SURFACE for the "
              "dialect-layer surface."),
        is_question=True,
        authored_by="author",
        τ_a=211,
    ),

    Description(
        id="D_oq_malfi_1_reader_frame",
        attached_to=anchor_event("E_bosola_visits_cardinal_at_night"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("**OQ-MALFI-1 substrate-layer reader frame.** Webster "
              "authors two `kind=\"instrumental\"` "
              "ArCharacterArcRelation records on the same target "
              "(Bosola) with the same polarity (malicious) but "
              "distinct wielders and temporal phases — the "
              "Cardinal in pre-play galley service plus the Act V "
              "body-disposal re-employment (substrate-grounded at "
              "E_bosola_galley_service τ_s=-12 and E_bosola_visits_"
              "cardinal_at_night τ_s=29); Ferdinand in the play's "
              "primary commission through every torture, the "
              "strangling, and the mutual wounding (substrate-"
              "grounded at E_ferdinand_hires_bosola τ_s=1 through "
              "E_mutual_wounding_ferdinand_bosola τ_s=32). The "
              "structural shape — one instrument-character passed "
              "across two employers across time with consistent "
              "moral polarity — is distinct from Lear's "
              "polarity-contrast shape (Edmund and Edgar wielding "
              "two distinct instrument-chains against Gloucester "
              "with opposite polarity).\n\n"
              "Reader-side question (Session 5 probe): do you read "
              "the Cardinal-Bosola brackets (pre-play service + "
              "Act V re-employment) as a SINGLE instrumental "
              "relation persisting across time, or as TWO distinct "
              "deployments? The substrate authors it as one "
              "relation; the temporal-discontinuity is reader-"
              "visible. The play's tragic-irony depends on this "
              "transferability — Bosola's willingness to be "
              "re-employed by the Cardinal in Act V (after a play "
              "of service to Ferdinand) is part of what makes his "
              "arc peripeteia at τ_s=24 explicit (he turns "
              "against BOTH wielders simultaneously). See "
              "malfi_aristotelian.py's OQ_MALFI_1_FINDING for the "
              "dialect-layer surface and the three candidate "
              "canonical extensions."),
        is_question=True,
        authored_by="author",
        τ_a=212,
    ),

    Description(
        id="D_websters_parodic_catholic_setting",
        attached_to=anchor_event("E_banishment_at_loretto"),
        kind="texture",
        attention=Attention.INTERPRETIVE,
        text=("Webster's setting is nominally Catholic Italy "
              "(Amalfi, Rome, Loretto) and the play's apparatus "
              "is thoroughly Catholic — the per verba marriage's "
              "canonical validity, the Cardinal's ecclesiastical "
              "office, the Loretto pilgrimage shrine, the "
              "poisoned Bible. But the play's treatment of Catholic "
              "institutions is satirical-bordering-on-violently-"
              "hostile: the Cardinal abandons his ecclesiastical "
              "office in a stage-direction dumb-show (literally "
              "removing his robes for armour at Loretto, τ_s=15), "
              "the per-verba marriage's canonical validity is "
              "structurally vindicated by the Duchess's death "
              "(she dies 'Duchess of Malfi still' — meaning the "
              "marriage held), the poisoned Bible (τ_s=27) makes "
              "the most-Catholic object a murder weapon. The "
              "play's parodic-Catholic reading is a deliberate "
              "Jacobean Protestant inflection: Webster (writing "
              "for a Protestant English audience under James I) "
              "displays Catholic institutional moral collapse as "
              "the play's social register. The substrate marks "
              "the Catholic apparatus structurally without "
              "endorsing the satire; the descriptions-layer "
              "carries the parodic reading. The corpus's first "
              "encoding to author institutional-religious "
              "satire as structural ground (Hamlet's Catholic-"
              "Protestant axis is present but not satirical; "
              "Lear's gods-as-flies invocation is rhetorical "
              "rather than institutional)."),
        is_question=False,
        authored_by="author",
        τ_a=220,
    ),

    Description(
        id="D_play_instrument_density",
        attached_to=anchor_event("E_madmen_masque"),
        kind="texture",
        attention=Attention.STRUCTURAL,
        text=("Webster's play is the corpus's densest "
              "instrument-user. Six distinct instruments operate "
              "across the action:\n\n"
              "1. The apricots (E_apricot_ploy, τ_s=7) — Bosola's "
              "   doctored fruit, the play's first instrument.\n"
              "2. The horoscope (E_horoscope_dropped, τ_s=9) — "
              "   Antonio's dropped paper bearing the child's "
              "   nativity; Bosola's inference engine.\n"
              "3. The dead hand (E_dead_hand_scene, τ_s=19) — "
              "   Ferdinand's torture-instrument, a severed hand "
              "   bearing a wedding ring.\n"
              "4. The waxworks (E_waxworks_scene, τ_s=20) — "
              "   wax figures of 'dead' Antonio and the children.\n"
              "5. The madmen masque (E_madmen_masque, τ_s=21) — "
              "   eight masked dancers commissioned to torment "
              "   the Duchess; the play's most theatrical "
              "   instrument.\n"
              "6. The poisoned Bible (E_cardinal_poisons_julia, "
              "   τ_s=27) — the Cardinal's instrument against "
              "   Julia.\n\n"
              "Plus the play's PERSONAL instruments: Bosola "
              "as Ferdinand's instrument (the AR_FERDINAND_BOSOLA_"
              "INSTRUMENTAL A13 relation), Bosola as the "
              "Cardinal's instrument (AR_CARDINAL_BOSOLA_"
              "INSTRUMENTAL). Compare:\n\n"
              "- Hamlet: 1 instrument (the Mousetrap) + 1 personal "
              "  (Laertes as Claudius's instrument).\n"
              "- Lear: 3 instruments (forged letter, staged "
              "  wound, staged cliff-fall) + 0 personal.\n"
              "- Macbeth, Oedipus, Rashomon: 0 instruments each.\n\n"
              "Webster's 6 + 2 = 8 instrument-and-instrumental-"
              "relation count is the corpus high by a wide "
              "margin. The density is structurally load-bearing: "
              "the play's anti-Catholic satire (a Bible as poison) "
              "and the Aristotelian overlay's two non-canonical "
              "instrumental relations (OQ-MALFI-1) both turn on "
              "the instrument-dense surface. If OQ-AP14 forces a "
              "canonical extension (sketch-06 candidate per "
              "lear_aristotelian.py's OQ_AP14_FINDING), Webster's "
              "instrument-density would be the second-site forcing "
              "evidence."),
        is_question=False,
        authored_by="author",
        τ_a=221,
    ),

    Description(
        id="D_duchess_of_malfi_still_reading",
        attached_to=anchor_event("E_strangling"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("'I am Duchess of Malfi still.' Webster's most "
              "famous line, spoken by the Duchess at τ_s=22 "
              "moments before the strangling. The substrate "
              "records the strangling event and the Duchess's "
              "death; the line itself is reader-side. Two "
              "structural readings:\n\n"
              "- ANAGNORISIS-REFUSAL. The Duchess could in "
              "  principle recognize her hamartia (marrying "
              "  secretly across rank in defiance of the "
              "  brothers' enforcement capacity) at the threshold "
              "  of death; she refuses to. The line is the "
              "  rhetorical seal on her refusal. Sketch-05 A18 "
              "  `anagnorisis_absent=True` on AR_DUCHESS (per "
              "  malfi_aristotelian.py) structurally carries the "
              "  refusal — corpus second use of the field after "
              "  Cordelia. The Cordelia parallel is meaningful: "
              "  both women die holding the ground their "
              "  hamartia chose; both deaths are pathos sites "
              "  because the anagnorisis-refusal is not "
              "  cowardice but principle.\n"
              "- ASSERTION-OF-PERSISTENCE. The Duchess "
              "  declares that her title (and by extension her "
              "  worth, her marriage's validity, her standing-"
              "  before-history) persists into death. The "
              "  per-verba marriage's canonical validity is "
              "  structurally vindicated by her continued "
              "  Duchess-status at the moment of strangling; the "
              "  line is the substrate-vindication of "
              "  secret_marriage(duchess, antonio) as a world-"
              "  fact that her killers cannot dissolve. Reading "
              "  (b) is reader-completionist; reading (a) is "
              "  dialect-load-bearing.\n\n"
              "The two readings are compatible — the refusal "
              "is by means of the assertion. The substrate "
              "commits to neither separately; the line's "
              "interpretive weight is reader-side, but the "
              "anagnorisis-refusal IS now structurally carried by "
              "the A18 field at dialect scope (Session 2)."),
        is_question=False,
        authored_by="author",
        τ_a=230,
    ),

    Description(
        id="D_eldest_son_survival_structural_payload",
        attached_to=anchor_event("E_delio_arrives_with_heir"),
        kind="texture",
        attention=Attention.STRUCTURAL,
        text=("The play's closing structural payload: Delio "
              "arrives at the Cardinal's palace with the "
              "Duchess's eldest son (substrate-grounded by "
              "duchess_son entity, surviving the Acts III-V "
              "catastrophe in transit with Antonio). Delio's "
              "closing speech entrusts the boy to Pescara and "
              "the surviving court: 'In all our quest of "
              "greatness, / Like wanton boys, whose pastime is "
              "their care, / We follow after bubbles blown in "
              "the air.'\n\n"
              "The structural-payload role parallels Edgar's at "
              "Lear's close (the wronged-son-restored, surviving "
              "the catastrophe to inherit and rule) and "
              "Horatio's at Hamlet's close (the survivor-witness "
              "tasked to tell the story). But the Duchess's son "
              "is a CHILD, not an adult inheritor — the "
              "structural shape differs: where Edgar and Horatio "
              "are present-tense survivors with immediate "
              "agency, the Duchess's son is future-tense "
              "promise. The play's restoration is deferred to "
              "the offstage future; Webster will not show "
              "what becomes of the boy. The catharsis is split "
              "between the catastrophe (the Duchess's death, "
              "Bosola's recognition, Ferdinand's lycanthropy, "
              "the brothers' mutual collapse) and the deferred "
              "hope (the boy who may grow up to be Duke of "
              "Amalfi, who may have heard the story, who may "
              "make different choices). Cordelia's offstage "
              "hanging is the corpus's emptiest closing pathos "
              "site; the Duchess's surviving son is the corpus's "
              "most deferred. Both are non-classical Aristotelian "
              "shapes; both register as legitimate-but-restless "
              "endings.\n\n"
              "Webster's closing line — 'These wretched eminent "
              "things / Leave no more fame behind 'em, than "
              "should one / Fall in a frost, and leave his "
              "print in snow' — sets the boy's future-tense "
              "against the catastrophe's past-tense. The "
              "substrate marks the eldest son's survival "
              "structurally; the descriptions-layer carries the "
              "thematic weight."),
        is_question=False,
        authored_by="author",
        τ_a=231,
    ),

]

