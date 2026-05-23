"""
The Duchess of Malfi — the encoded fabula (substrate skeleton).

**Session 1 scope:** entities, canonical branches, prop constructors,
event helpers, FABULA (the canonical spine, ~34 events from pre-play
standing facts through the Act-V mutual killings and Delio's return
with the heir), and zero derivation rules (rationale below).
Knowledge effects authored only on the load-bearing beats —
Bosola's spying, the apricot ploy, the horoscope, Ferdinand's
bedchamber confrontation, the dead-hand and waxworks tortures,
the strangling, the corpse-view recognitions, the night-violence
of Act V. Deferred to Session 2+: Aristotelian overlay
(`malfi_aristotelian.py`), PREPLAY_DISCLOSURES, SJUZHET,
DESCRIPTIONS, full per-event knowledge projections,
encoding-specific tests, live reader-model probe run.

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
