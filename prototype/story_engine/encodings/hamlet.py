"""
Hamlet — the encoded fabula (substrate completion).

**Session 1 scope (edb25cb):** entities, canonical branches, prop
constructors, event helpers, FABULA (32 events covering pre-play
regicide through the duel finale), and three derivation rules.
Knowledge effects authored only on the load-bearing beats.

**Session 2 scope (9423f59):** Aristotelian overlay
(`hamlet_aristotelian.py`) pressuring OQ-AP5 (Ghost-as-fate-agent)
and OQ-AP6 (three tragic heroes in one mythos).

**Session 3 scope (this file):** PREPLAY_DISCLOSURES,
SJUZHET (26 in-play entries with focalization), DESCRIPTIONS
(~9 interpretive records covering Ghost ontology, Hamlet's
sanity, Gertrude's foreknowledge, Ophelia's death, the Mousetrap
as epistemic instrument, and the OQ-AP5/AP6 forcing-function
postures), and additional per-event knowledge projections —
especially the asymmetric-information beats that OQ-AP5/AP6 read
on (Claudius's sole pre-Mousetrap knowledge, the
Claudius-knows-Hamlet-knows hinge, Laertes's misled state
pre-deathbed, the public-vs-private Mousetrap reaction).

Story content only. No substrate logic. This file parallels
`macbeth.py` in shape and is the third Shakespeare-tragedy
encoding alongside Macbeth and the non-Shakespeare classical
corpus (Oedipus). Hamlet pressures two banked research forcing
functions from `aristotelian-probe-sketch-03`:

- **OQ-AP5** — ArFateAgent / ArProphecyStructure. Hamlet's Ghost
  occupies a causal position distinct from Macbeth's Witches:
  direct factual revelation (Claudius poisoned the king) plus
  commission to act (revenge demand), where the Witches offered
  equivocating prophecy. A second fate-agent encoding with a
  *different* causal posture is the forcing function sketch-03
  banked.
- **OQ-AP6** — Intra-mythos parallel-character-arc relation. Hamlet
  has at least three tragic-hero candidates (Hamlet himself,
  Claudius, Laertes) whose arcs run in parallel within a single
  mythos. A10's `ArMythosRelation(kind="parallel")` types *inter*-
  mythos today; the Hamlet encoding is the forcing case for whether
  intra-mythos parallel needs its own structural hook.

Encoding choices (explicit, so future readers understand the slice):

- **Branches: canonical only.** Hamlet has no Rashomon-style
  contested testimony. The question of Hamlet's sanity
  (feigned vs. actual), Gertrude's foreknowledge, and the Ghost's
  ontology are all descriptions-layer concerns rather than
  branch-level concerns; the substrate commits to the canonical
  narrative only.

- **Identity placeholders: none.** Like Macbeth (and unlike
  Oedipus), Hamlet never confuses who is who at substrate level.
  The Ghost's identity is ontologically uncertain (is it King
  Hamlet? a devil? a projection?) — that is a descriptions-layer
  authorial-uncertainty question, not a substrate identity puzzle.

- **Audience-pre-knowledge disclosures: moderate.** Elizabethan
  audiences knew the name but not the tragedy in detail; unlike
  Oedipus there is no myth-level front-loaded irony. The substrate
  takes for granted that King Hamlet is dead and Claudius is king
  as of Act 1 Scene 1 — these are the opening facts the play
  takes for granted rather than builds up to. See
  `PREPLAY_DISCLOSURES` below: seven facts (king_hamlet dead,
  Claudius king, Claudius-Gertrude marriage, Gertrude queen,
  Hamlet prince, Claudius-Hamlet brotherhood, Polonius serving
  crown). The murder *method*, the Ghost, and the revenge
  commission are NOT pre-known.

- **Focalization: largely Hamlet,** with excursions. See `SJUZHET`
  below. Most entries focalize Hamlet (14 of 26); court/plotting
  scenes omniscient (None); Ophelia's mad scene focalizes her;
  Claudius's prayer focalizes him (his soliloquy — the A11 chain
  step authored at `hamlet_aristotelian.py`); the final death
  focalizes Horatio (the sole survivor, charged to tell the
  story). Laertes focalizes his return scene.

- **Authored compound predicates:** fratricide(X, Y), regicide(X, Y),
  usurper(X). Candidate derivations per inference-model-sketch-01
  N9:
      killed(X, Y) ∧ brother_of(X, Y)   ⇒ fratricide(X, Y)
      killed(X, Y) ∧ king(Y, _)         ⇒ regicide(X, Y)
      fratricide(X, _) ∧ regicide(X, _) ∧ king(X, _) ⇒ usurper(X)
  The usurper rule is depth-2 — Claudius's usurper status follows
  from his fratricide (killing his brother) AND regicide (killing
  a king — the same victim) AND his own kingship.

- **Supernatural ontology: deliberately unsettled.** The Ghost is
  an Entity of kind "agent" distinct from `king_hamlet` (the dead
  king). Whether the Ghost IS King Hamlet's spirit, a devil in
  that shape, or Hamlet's guilty projection is an authorial-
  uncertainty question; substrate records only that Hamlet and
  Horatio observe a figure claiming to be the murdered king. The
  apparition_of proposition is authored as an observed-only fact
  (no world assertion that the ghost exists), same pattern as
  Macbeth's Banquo-ghost and the Weird Sisters.

- **Scope of the play encoded: essentially all of it at the event
  level,** compressed. Secondary beats (gravedigger scene, pirate
  rescue, Fortinbras's coda) are elided or mentioned only in
  comments. Rosencrantz, Guildenstern, Fortinbras, Osric,
  gravediggers, and the players are not authored as entities —
  their structural contributions are compressed into the events
  they enable (the mousetrap uses "players-off-stage" as a
  role; the England voyage uses a compressed
  E_hamlet_returns_from_england beat). Session 2+ may add these
  if a forcing function argues for it.
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

hamlet        = Entity(id="hamlet",        name="Hamlet",           kind="agent")
claudius      = Entity(id="claudius",      name="Claudius",         kind="agent")
gertrude      = Entity(id="gertrude",      name="Gertrude",         kind="agent")
# King Hamlet — the dead king, Hamlet's father. Referenced throughout
# the play even though he dies before τ_s=0. Same treatment as
# Macbeth's Duncan: a character who dies early still has substrate
# presence for relational and historical facts.
king_hamlet   = Entity(id="king_hamlet",   name="King Hamlet",      kind="agent")
# The Ghost — ontologically distinct from king_hamlet. Whether the
# Ghost IS King Hamlet's spirit is a descriptions-layer question; at
# substrate level the Ghost is an observable agent that speaks, and
# king_hamlet is the dead body of the former king. This separation
# preserves the authorial reticence Shakespeare built into the play.
ghost         = Entity(id="ghost",         name="the Ghost",        kind="agent")
polonius      = Entity(id="polonius",      name="Polonius",         kind="agent")
ophelia       = Entity(id="ophelia",       name="Ophelia",          kind="agent")
laertes       = Entity(id="laertes",       name="Laertes",          kind="agent")
horatio       = Entity(id="horatio",       name="Horatio",          kind="agent")

denmark       = Entity(id="denmark",       name="Denmark",          kind="location")
elsinore      = Entity(id="elsinore",      name="Elsinore (the royal castle)", kind="location")
ramparts      = Entity(id="ramparts",      name="the ramparts (at Elsinore)",  kind="location")
great_hall    = Entity(id="great_hall",    name="the great hall (at Elsinore)", kind="location")
graveyard     = Entity(id="graveyard",     name="the graveyard (near Elsinore)", kind="location")
england       = Entity(id="england",       name="England",          kind="location")


ENTITIES = [
    hamlet, claudius, gertrude, king_hamlet, ghost,
    polonius, ophelia, laertes, horatio,
    denmark, elsinore, ramparts, great_hall, graveyard, england,
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
# moral / affective / ontological register (is the Ghost real; is
# Hamlet mad; is Gertrude complicit) lives on descriptions.


def killed(killer: str, victim: str) -> Prop:
    return Prop("killed", (killer, victim))

def dead(who: str) -> Prop:
    return Prop("dead", (who,))

def king(who: str, realm: str) -> Prop:
    return Prop("king", (who, realm))

def queen(who: str, realm: str) -> Prop:
    return Prop("queen", (who, realm))

def prince_of(who: str, realm: str) -> Prop:
    return Prop("prince_of", (who, realm))

def married(a: str, b: str) -> Prop:
    return Prop("married", (a, b))

def parent_of(parent: str, child: str) -> Prop:
    return Prop("parent_of", (parent, child))

def brother_of(a: str, b: str) -> Prop:
    # Symmetric; authored both directions where used. Inference rules
    # may assume symmetry; the encoding asserts it explicitly.
    return Prop("brother_of", (a, b))

def at_location(who: str, where: str) -> Prop:
    return Prop("at_location", (who, where))

def served_by(lord: str, servant: str) -> Prop:
    # Polonius serves Claudius (and by extension the Danish crown);
    # the Lord Chamberlain / courtier hierarchy.
    return Prop("served_by", (lord, servant))

def ordered_killing(orderer: str, victim: str) -> Prop:
    return Prop("ordered_killing", (orderer, victim))

def apparition_of(entity: str, at: str) -> Prop:
    # Observed apparition. Same pattern as macbeth.py's apparition_of —
    # authored as agent-observation only, never as world-fact. The
    # ontological claim (whether the Ghost is real) is deliberately
    # unsettled at substrate level.
    return Prop("apparition_of", (entity, at))

def feigning_madness(who: str) -> Prop:
    # Hamlet's own claim to himself (and later to Horatio) that his
    # "antic disposition" is performance. Held at agent-level; the
    # substrate does not commit to whether it becomes genuine madness
    # later — another deliberate reticence.
    return Prop("feigning_madness", (who,))

def guilty_reaction(who: str) -> Prop:
    # Observable reaction — Claudius's mid-play panic at the dumb-show.
    # Structural predicate: the reaction happened and was observed;
    # whether it amounts to a confession is a descriptions-layer
    # read.
    return Prop("guilty_reaction", (who,))

def mad(who: str) -> Prop:
    # World-level madness claim. Ophelia's scenes commit to this;
    # Hamlet's do not (per `feigning_madness`).
    return Prop("mad", (who,))

def drowned(who: str) -> Prop:
    return Prop("drowned", (who,))

def poisoned_with_cup(who: str) -> Prop:
    # Structural distinction: poisoning-by-cup (Gertrude, attempted
    # on Hamlet, enabled for Claudius) is a distinct substrate event
    # from poisoning-by-blade (Laertes, Hamlet). Both contribute to
    # `killed` but the mechanism matters for the Ghost's revelation
    # (which specifies poison-in-the-ear — a third poisoning mode at
    # τ_s=-2).
    return Prop("poisoned_with_cup", (who,))

def poisoned_with_blade(who: str) -> Prop:
    return Prop("poisoned_with_blade", (who,))

def poisoned_in_ear(who: str) -> Prop:
    # King Hamlet's specific murder method — the Ghost names this
    # detail in its revelation.
    return Prop("poisoned_in_ear", (who,))

# Ghost-content predicates. Hamlet learns these from the Ghost's
# speech; semantically they are claims about pre-play state that
# Hamlet previously did not know. Authored as content-predicates to
# keep the Ghost's *claim* distinct from the world fact the claim
# refers to. After the Mousetrap validates the claim, Hamlet's
# held-belief (slot=BELIEVED, post-Mousetrap promoted to KNOWN)
# aligns with the world fact.

def ghost_claims_killed_by(victim: str, killer: str) -> Prop:
    # The Ghost's specific claim: X was killed by Y. Structurally
    # distinct from world-level killed(Y, X) — the Ghost's utterance
    # is a separate record whose truth Hamlet must verify. Parallels
    # Macbeth's prophecy_* predicates but in the retro-causal rather
    # than prospective direction.
    return Prop("ghost_claims_killed_by", (victim, killer))

def ghost_demands_revenge(target_of_revenge: str) -> Prop:
    # The Ghost's commission. Authored on Hamlet's held set only;
    # no world-level claim that a ghost made a demand.
    return Prop("ghost_demands_revenge", (target_of_revenge,))

def revealed_plot(revealer: str, plotter: str) -> Prop:
    # Laertes's deathbed reveal of Claudius's poisoning plot. World-
    # level record that the plot is now publicly known.
    return Prop("revealed_plot", (revealer, plotter))


# Compound / moral-register predicates. Authored as predicate
# constructors; derived via RULES below at query time (same pattern
# as Macbeth's kinslayer/regicide/tyrant).

def fratricide(slayer: str, victim: str) -> Prop:
    # ⇐ killed(X, Y) ∧ brother_of(X, Y)
    return Prop("fratricide", (slayer, victim))

def regicide(slayer: str, victim: str) -> Prop:
    # ⇐ killed(X, Y) ∧ king(Y, _)
    return Prop("regicide", (slayer, victim))

def usurper(who: str) -> Prop:
    # ⇐ fratricide(X, _) ∧ regicide(X, _) ∧ king(X, _)
    # Claudius is the corpus's first explicit usurper. Hamlet is
    # a regicide (killing Claudius) but not a usurper (he dies
    # before taking the throne).
    return Prop("usurper", (who,))


# ----------------------------------------------------------------------------
# Event helpers — same pattern as macbeth.py / oedipus.py.
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
#   - τ_s ≤ -10  : deep standing facts (kinship, royal lineage)
#   - τ_s = -2   : King Hamlet's murder (the crime that sets the play in motion)
#   - τ_s = -1   : Claudius's coronation and marriage to Gertrude
#   - τ_s = 0    : Act 1 opens (the Ghost is seen by the watch)
#   - τ_s ≥ 0    : the play proper
#
# The play compresses many days into fabula-close τ_s values (the
# gap between the duel and its aftermath events is ~0 substrate
# time); Session 2+ may refine.

FABULA = [

    # --- Pre-play (τ_s < 0) ---

    Event(
        id="E_king_hamlet_reigns",
        type="standing",
        τ_s=-30, τ_a=1,
        participants={"who": "king_hamlet"},
        effects=(
            # King Hamlet on the throne of Denmark. Standing fact that
            # precedes the action; his death at τ_s=-2 retracts it.
            world(king("king_hamlet", "denmark")),
            # Gertrude is his queen; Hamlet is their son and prince.
            world(married("king_hamlet", "gertrude")),
            world(queen("gertrude", "denmark")),
            world(parent_of("king_hamlet", "hamlet")),
            world(parent_of("gertrude", "hamlet")),
            world(prince_of("hamlet", "denmark")),
            # Court knowledge of the prior reign. Load-bearing for the
            # reader projection: every in-play character remembers who
            # the king was, what the family was, and who stood where —
            # the play's emotional economy runs on remembered state.
            observe("hamlet", king("king_hamlet", "denmark"), -30),
            observe("hamlet", married("king_hamlet", "gertrude"), -30),
            observe("hamlet", parent_of("king_hamlet", "hamlet"), -30),
            observe("hamlet", parent_of("gertrude", "hamlet"), -30),
            observe("hamlet", prince_of("hamlet", "denmark"), -30),
            observe("gertrude", married("king_hamlet", "gertrude"), -30),
            observe("gertrude", queen("gertrude", "denmark"), -30),
            observe("horatio", king("king_hamlet", "denmark"), -30,
                    note="Horatio the scholar knew the king"),
            observe("claudius", king("king_hamlet", "denmark"), -30,
                    note="Claudius knew who he would supplant"),
        ),
    ),

    Event(
        id="E_claudius_brother_of_king",
        type="standing",
        τ_s=-100, τ_a=2,
        participants={"a": "claudius", "b": "king_hamlet"},
        effects=(
            # Blood relation — Claudius and King Hamlet are brothers.
            # Authored at deep negative τ_s so the brother_of relation
            # is always in world-scope; load-bearing for the FRATRICIDE
            # rule derivation.
            world(brother_of("claudius", "king_hamlet")),
            world(brother_of("king_hamlet", "claudius")),
            # Claudius knows his lineage.
            observe("claudius", brother_of("claudius", "king_hamlet"), -100,
                    note="acknowledged kinship"),
            # As does everyone at court.
            observe("king_hamlet", brother_of("king_hamlet", "claudius"), -100),
            observe("hamlet",
                    brother_of("claudius", "king_hamlet"), -100,
                    note="Hamlet knows his uncle is his father's brother"),
        ),
    ),

    Event(
        id="E_polonius_family_standing",
        type="standing",
        τ_s=-20, τ_a=3,
        participants={"father": "polonius",
                      "daughter": "ophelia",
                      "son": "laertes"},
        effects=(
            world(parent_of("polonius", "ophelia")),
            world(parent_of("polonius", "laertes")),
            # Polonius is Lord Chamberlain — structurally serving the
            # crown. Captured as served_by between king_hamlet (the
            # reigning king at τ_s=-20) and polonius.
            world(served_by("king_hamlet", "polonius")),
            # Family observations — Polonius's children know who their
            # father is; load-bearing for Laertes's tragic-hero arc
            # (OQ-AP6). Laertes returns to avenge a father he knew.
            observe("polonius", parent_of("polonius", "ophelia"), -20),
            observe("polonius", parent_of("polonius", "laertes"), -20),
            observe("ophelia", parent_of("polonius", "ophelia"), -20),
            observe("laertes", parent_of("polonius", "laertes"), -20),
            # Siblings know each other (via their shared father).
            # Authored as a derived acquaintance observation; the
            # sibling relation itself is not a substrate predicate
            # but can be composed by the reader.
            observe("laertes", parent_of("polonius", "ophelia"), -20,
                    note="Laertes knows his sister"),
            observe("ophelia", parent_of("polonius", "laertes"), -20),
        ),
    ),

    Event(
        id="E_king_hamlet_poisoned",
        type="murder",
        τ_s=-2, τ_a=10,
        participants={"killer": "claudius", "victim": "king_hamlet"},
        effects=(
            # The fratricidal regicide that the entire tragedy hinges
            # on. Claudius poisons King Hamlet in the orchard by
            # pouring poison in his ear — the Ghost will reveal this
            # specific method to Hamlet at τ_s=1.
            world(killed("claudius", "king_hamlet")),
            world(dead("king_hamlet")),
            world(poisoned_in_ear("king_hamlet")),
            # Note: king(king_hamlet, denmark) is NOT retracted — per
            # macbeth.py's convention, the king fact persists
            # historically after death so the REGICIDE_RULE can fire
            # on `killed(X, Y) ∧ king(Y, R)`. The throne's vacancy is
            # recorded by the subsequent `world(king("claudius",
            # "denmark"))` assertion at τ_s=-1, not by retracting the
            # prior kingship.
            # Claudius knows what he did. Nobody else does (yet).
            observe("claudius", killed("claudius", "king_hamlet"), -2,
                    note="the murder only Claudius knows"),
            observe("claudius", poisoned_in_ear("king_hamlet"), -2,
                    note="the specific method"),
            # Everyone else observes only the *death*, not the murder.
            # This is the asymmetric-information fulcrum of the play:
            # the world is uniform about `dead(king_hamlet)` and split
            # about `killed(claudius, king_hamlet)`. Load-bearing for
            # OQ-AP5 (the Ghost reveals the killed() fact to Hamlet)
            # and for OQ-AP6 (Claudius's tragic arc is defined by his
            # sole possession of this fact until the Mousetrap).
            observe("hamlet", dead("king_hamlet"), -2,
                    note="Hamlet's bereavement — the death, not yet the cause"),
            observe("gertrude", dead("king_hamlet"), -2,
                    note="the widowed queen"),
            observe("horatio", dead("king_hamlet"), -2),
            observe("polonius", dead("king_hamlet"), -2),
            observe("laertes", dead("king_hamlet"), -2),
            observe("ophelia", dead("king_hamlet"), -2),
        ),
    ),

    Event(
        id="E_claudius_crowned",
        type="royal_decree",
        τ_s=-1, τ_a=11,
        participants={"who": "claudius"},
        effects=(
            # Claudius takes the throne, bypassing Hamlet (who was
            # the prince-heir). A Danish election elevated him — the
            # play leaves the politics compressed.
            world(king("claudius", "denmark")),
            # The court knows Claudius is now king.
            observe("hamlet", king("claudius", "denmark"), -1,
                    note="Hamlet's grievance"),
            observe("horatio", king("claudius", "denmark"), -1),
            observe("polonius", king("claudius", "denmark"), -1),
            # Polonius now serves Claudius.
            world(served_by("claudius", "polonius")),
        ),
    ),

    Event(
        id="E_claudius_marries_gertrude",
        type="marriage",
        τ_s=-1, τ_a=12,
        participants={"a": "claudius", "b": "gertrude"},
        effects=(
            # "Within a month" of the king's death — Hamlet's
            # grievance about the haste is a descriptions-layer read;
            # the substrate records only the marriage.
            world(married("claudius", "gertrude")),
            # Gertrude is now queen again, under Claudius.
            world(queen("gertrude", "denmark")),
            # Hamlet's knowledge of the marriage — sets up his
            # opening soliloquy.
            observe("hamlet", married("claudius", "gertrude"), -1,
                    note="'O, most wicked speed'"),
            # Public court ceremony — the rest of the court observes
            # the marriage too.
            observe("gertrude", married("claudius", "gertrude"), -1),
            observe("claudius", married("claudius", "gertrude"), -1),
            observe("horatio", married("claudius", "gertrude"), -1),
            observe("polonius", married("claudius", "gertrude"), -1),
            observe("laertes", married("claudius", "gertrude"), -1),
            observe("ophelia", married("claudius", "gertrude"), -1),
        ),
    ),

    # --- Act 1 — the Ghost (τ_s = 0..4) ---

    Event(
        id="E_ghost_seen_by_watch",
        type="apparition",
        τ_s=0, τ_a=20,
        participants={"observer": "horatio", "apparition": "ghost",
                      "location": "ramparts"},
        effects=(
            # First apparition. Horatio (and off-stage watch companions
            # Bernardo and Marcellus, compressed into horatio as the
            # substrate observer) sees a figure resembling the dead
            # king. Authored as observe only — no world-level claim
            # that the ghost is real. Same pattern as Macbeth's
            # banquet ghost.
            observe("horatio", apparition_of("ghost", "ramparts"), 0,
                    note="the watch's sighting; Horatio attempts to speak"),
        ),
    ),

    Event(
        id="E_horatio_tells_hamlet",
        type="utterance",
        τ_s=0, τ_a=21,
        participants={"speaker": "horatio", "listener": "hamlet"},
        effects=(
            # Horatio informs Hamlet that the Ghost walks. Hamlet's
            # held at BELIEVED — he trusts Horatio but will not
            # commit until he sees for himself.
            told_by("hamlet", "horatio",
                    apparition_of("ghost", "ramparts"), 0,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Horatio's report"),
        ),
    ),

    Event(
        id="E_hamlet_meets_ghost",
        type="revelation",
        τ_s=1, τ_a=30,
        participants={"speaker": "ghost", "listener": "hamlet",
                      "location": "ramparts"},
        effects=(
            # The Ghost's revelation — the load-bearing event for
            # OQ-AP5. The Ghost names both the crime (Claudius
            # poisoned the king) and the method (poison in the ear),
            # and issues the revenge commission.
            #
            # Hamlet's slot is BELIEVED rather than KNOWN because his
            # "spirit that I have seen may be the devil" doubt is
            # explicit in the text — he needs to verify before acting.
            # The Mousetrap at τ_s=6 promotes these to KNOWN.
            observe("hamlet", apparition_of("ghost", "ramparts"), 1,
                    note="direct witness; Hamlet's own meeting with the Ghost"),
            # The Ghost's claim — authored as a content predicate so
            # the *claim* is distinct from the world-fact it refers to.
            told_by("hamlet", "ghost",
                    ghost_claims_killed_by("king_hamlet", "claudius"), 1,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="the Ghost names the murderer"),
            # The specific method — poison-in-ear. Only Claudius and
            # (claimed) the Ghost know this; when the Mousetrap
            # triggers Claudius's reaction, Hamlet's held-belief
            # about the method shifts to KNOWN because the detail
            # was not publicly available — the forcing mechanism for
            # the Mousetrap's epistemic power.
            told_by("hamlet", "ghost", poisoned_in_ear("king_hamlet"), 1,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="'the leperous distilment in the porches of mine ears'"),
            # The revenge commission. Agent-only; no world-level claim
            # that a ghost commissioned anything.
            told_by("hamlet", "ghost", ghost_demands_revenge("claudius"), 1,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="'Revenge his foul and most unnatural murder'"),
        ),
    ),

    Event(
        id="E_hamlet_sworn_to_secrecy",
        type="utterance",
        τ_s=2, τ_a=40,
        participants={"speaker": "hamlet", "listener": "horatio"},
        effects=(
            # Hamlet tells Horatio about the Ghost (substrate-level:
            # the claim, not the verified fact). Horatio becomes the
            # only other person who holds the Ghost's claim.
            told_by("horatio", "hamlet",
                    ghost_claims_killed_by("king_hamlet", "claudius"), 2,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Hamlet confides in Horatio"),
        ),
    ),

    Event(
        id="E_hamlet_adopts_antic_disposition",
        type="resolution",
        τ_s=2, τ_a=41,
        participants={"who": "hamlet"},
        effects=(
            # Hamlet commits to feigning madness. Self-observation
            # only — nobody else yet knows it is performance.
            observe("hamlet", feigning_madness("hamlet"), 2,
                    note="Hamlet's own plan; private to him"),
            # Horatio is let in on the secret shortly after (compressed
            # into the same event).
            told_by("horatio", "hamlet", feigning_madness("hamlet"), 2,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Horatio knows the madness is performance"),
        ),
    ),

    # --- Act 2 — the court's response (τ_s = 3..5) ---

    Event(
        id="E_polonius_theory",
        type="utterance",
        τ_s=3, τ_a=50,
        participants={"speaker": "polonius", "listeners": ["claudius", "gertrude"]},
        effects=(
            # Polonius's theory: Hamlet is mad with love for Ophelia
            # (he has forbidden Ophelia to see Hamlet; he presents
            # Hamlet's letters to Ophelia as evidence). Claudius and
            # Gertrude accept the theory provisionally — it becomes
            # their working hypothesis until the Mousetrap.
            told_by("claudius", "polonius", mad("hamlet"), 3,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Polonius's love-madness theory"),
            told_by("gertrude", "polonius", mad("hamlet"), 3,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED),
        ),
    ),

    Event(
        id="E_players_arrive",
        type="arrival",
        τ_s=5, τ_a=60,
        participants={"arrivers": "players-off-stage",
                      "location": "elsinore"},
        effects=(
            # The traveling players arrive at Elsinore. Hamlet sees
            # the opportunity: he will insert lines into their
            # performance to test Claudius's reaction. The players
            # themselves are compressed as "players-off-stage";
            # Session 2+ can promote them to first-class entities if
            # a forcing function argues for it.
            observe("hamlet", at_location("hamlet", "elsinore"), 5,
                    note="Hamlet conceives the Mousetrap"),
        ),
    ),

    # --- Act 3 — the Mousetrap and the prayer scene (τ_s = 6..7) ---

    Event(
        id="E_mousetrap_performance",
        type="play_within_play",
        τ_s=6, τ_a=70,
        participants={"director": "hamlet",
                      "observer": "horatio",
                      "target": "claudius",
                      "witness": "gertrude",
                      "location": "great_hall"},
        effects=(
            # The Mousetrap — the load-bearing event for Hamlet's
            # epistemic arc. The players enact a regicide by poison-
            # in-the-ear; Claudius rises and storms out. Hamlet and
            # Horatio both observe the guilty reaction.
            world(guilty_reaction("claudius")),
            observe("hamlet", guilty_reaction("claudius"), 6,
                    note="the Mousetrap sprung"),
            observe("horatio", guilty_reaction("claudius"), 6,
                    note="Horatio's corroborating witness"),
            # Hamlet's held-belief about the Ghost's claim promotes
            # from BELIEVED to KNOWN. The specific poison-in-ear
            # detail is load-bearing: because that detail was not
            # publicly known, Claudius's panic at its dramatization
            # is (for Hamlet) proof that he knows the detail — which
            # means the Ghost's claim is true.
            remove_held("hamlet",
                        ghost_claims_killed_by("king_hamlet", "claudius"),
                        Slot.BELIEVED, Confidence.BELIEVED, 6,
                        note="promoted to KNOWN below"),
            observe("hamlet", killed("claudius", "king_hamlet"), 6,
                    note="'I'll take the Ghost's word for a thousand pound'"),
            remove_held("hamlet", poisoned_in_ear("king_hamlet"),
                        Slot.BELIEVED, Confidence.BELIEVED, 6,
                        note="the specific detail that clinches it"),
            observe("hamlet", poisoned_in_ear("king_hamlet"), 6,
                    note="the poison-in-ear detail is now certain"),
            # Claudius now knows Hamlet knows. This is the hinge of
            # the tragedy — from here, Claudius is actively plotting
            # against Hamlet. Claudius's epistemic state about
            # *Hamlet's* knowledge is the load-bearing fact for his
            # tragic-hero arc (OQ-AP6): before the Mousetrap he was
            # the sole knower; after, he is the exposed knower, and
            # every subsequent action (the England plot, the duel
            # conspiracy) follows from this inference. Authored as
            # Claudius holding `killed(claudius, king_hamlet)` at
            # slot KNOWN — the world-fact he always held — AND
            # observing his own guilty reaction (which, for him, IS
            # the evidence that Hamlet now holds the same fact).
            observe("claudius", guilty_reaction("claudius"), 6,
                    note="Claudius knows he betrayed himself"),
            # Horatio now also holds the Ghost's claim as effectively
            # validated — the corroborating-witness function of his
            # role. Authored here rather than at E_hamlet_meets_ghost
            # because the Mousetrap is what promotes Horatio's belief
            # from "Hamlet says so" to "Hamlet's test confirmed it."
            told_by("horatio", "hamlet",
                    killed("claudius", "king_hamlet"), 6,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Horatio now credits Hamlet's Ghost-claim"),
        ),
    ),

    Event(
        id="E_claudius_prays",
        type="private_scene",
        τ_s=7, τ_a=80,
        participants={"who": "claudius", "observer": "hamlet"},
        effects=(
            # Claudius attempts to pray for forgiveness; Hamlet enters
            # behind him sword-drawn but decides not to kill him at
            # prayer (fearing Claudius would go to heaven). Structural
            # record: Hamlet observes Claudius's attempted confession
            # but does not act on it.
            observe("hamlet", at_location("claudius", "elsinore"), 7,
                    note="Hamlet passes up the chance to kill Claudius"),
        ),
    ),

    # --- Act 3 — the closet scene (τ_s = 8) ---

    Event(
        id="E_polonius_hides_arras",
        type="positioning",
        τ_s=8, τ_a=90,
        participants={"who": "polonius", "location": "elsinore"},
        effects=(
            # Polonius hides behind the tapestry in Gertrude's closet
            # to eavesdrop on the Hamlet-Gertrude confrontation.
            world(at_location("polonius", "elsinore")),
        ),
    ),

    Event(
        id="E_hamlet_confronts_gertrude",
        type="confrontation",
        τ_s=8, τ_a=91,
        participants={"speaker": "hamlet", "listener": "gertrude",
                      "location": "elsinore"},
        effects=(
            # Hamlet accuses Gertrude of complicity in (or at least
            # culpable haste around) the marriage. He does NOT
            # explicitly accuse her of foreknowledge of the murder —
            # the text leaves her state deliberately ambiguous.
            # Substrate records only the confrontation; her
            # foreknowledge is a descriptions-layer question.
            observe("gertrude", at_location("hamlet", "elsinore"), 8,
                    note="the closet scene"),
        ),
    ),

    Event(
        id="E_hamlet_kills_polonius",
        type="murder",
        τ_s=8, τ_a=92,
        participants={"killer": "hamlet", "victim": "polonius"},
        effects=(
            # Hamlet stabs through the arras thinking it is Claudius
            # ("Is it the king?"). Polonius dies. Hamlet's first
            # killing — structurally important for the Laertes arc
            # (son avenging father) and for Hamlet's own trajectory
            # (from contemplation to action, but misdirected).
            world(killed("hamlet", "polonius")),
            world(dead("polonius")),
            observe("hamlet", killed("hamlet", "polonius"), 8,
                    note="'a rash and bloody deed'"),
            observe("gertrude", killed("hamlet", "polonius"), 8,
                    note="direct witness"),
            # Gertrude reports the killing to Claudius offstage at
            # Act 4.1; compressed as a told_by within this event
            # (same-beat) since the report motivates Claudius's
            # England decision at τ_s=9.
            told_by("claudius", "gertrude", killed("hamlet", "polonius"), 8,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Gertrude reports the killing to Claudius"),
        ),
    ),

    Event(
        id="E_ghost_in_closet",
        type="apparition",
        τ_s=8, τ_a=93,
        participants={"observer": "hamlet", "apparition": "ghost",
                      "non_observer": "gertrude",
                      "location": "elsinore"},
        effects=(
            # The Ghost appears in the closet scene. Gertrude does
            # not see it — the Ghost's ontology is again deliberately
            # unsettled. Authored on Hamlet only (no world fact).
            observe("hamlet", apparition_of("ghost", "elsinore"), 8,
                    note="the Ghost's second appearance; Gertrude sees nothing"),
        ),
    ),

    # --- Act 4 — Hamlet to England, Ophelia's drowning, Laertes returns (τ_s = 9..12) ---

    Event(
        id="E_hamlet_sent_to_england",
        type="royal_decree",
        τ_s=9, τ_a=100,
        participants={"decree": "claudius", "subject": "hamlet",
                      "destination": "england"},
        effects=(
            # Claudius packages Hamlet off to England with sealed
            # orders for his execution (compressed: the orders are
            # off-stage facts the substrate doesn't model beat-by-
            # beat). Hamlet's return voyage and the
            # Rosencrantz/Guildenstern substitution are elided; the
            # next substrate appearance of Hamlet is at τ_s=13 for
            # the graveyard scene.
            world(at_location("hamlet", "england")),
            # Claudius orders Hamlet's death in England — world fact
            # that Claudius's intent exists.
            world(ordered_killing("claudius", "hamlet")),
            observe("claudius", ordered_killing("claudius", "hamlet"), 9,
                    note="the sealed orders"),
            # The court observes Hamlet's departure (the stated pretext
            # was Polonius's killing + Hamlet's own safety; the sealed
            # orders are secret). Gertrude and Horatio know he has
            # gone but not that Claudius intends his death.
            observe("hamlet", at_location("hamlet", "england"), 9),
            observe("gertrude", at_location("hamlet", "england"), 9,
                    note="the stated pretext"),
            observe("horatio", at_location("hamlet", "england"), 9),
        ),
    ),

    Event(
        id="E_ophelia_madness",
        type="madness_scene",
        τ_s=10, τ_a=110,
        participants={"who": "ophelia", "witnesses": ["claudius", "gertrude"]},
        effects=(
            # Ophelia's mad scene — grief at her father's death and
            # at Hamlet's rejection. Unlike Hamlet's feigned madness,
            # Ophelia's is authored as a world-level mad() — the text
            # commits to its reality.
            world(mad("ophelia")),
            observe("claudius", mad("ophelia"), 10,
                    note="'poor Ophelia, divided from herself'"),
            observe("gertrude", mad("ophelia"), 10),
        ),
    ),

    Event(
        id="E_ophelia_drowns",
        type="death",
        τ_s=11, τ_a=120,
        participants={"who": "ophelia", "location": "denmark"},
        effects=(
            # Ophelia drowns in the brook. Shakespeare leaves
            # deliberate ambiguity about whether she fell or chose
            # her death — the gravediggers debate it in Act 5. The
            # substrate commits to drowned() but leaves causation
            # unspecified; the suicide-vs-accident question is a
            # descriptions-layer concern.
            world(dead("ophelia")),
            world(drowned("ophelia")),
            # Gertrude reports the drowning to Laertes (τ_s=12); her
            # speech is the audience's only account.
            observe("gertrude", drowned("ophelia"), 11,
                    note="'There is a willow grows aslant a brook'"),
        ),
    ),

    Event(
        id="E_laertes_returns",
        type="arrival",
        τ_s=12, τ_a=130,
        participants={"who": "laertes", "location": "denmark"},
        effects=(
            # Laertes returns from France demanding vengeance for his
            # father's death. Initially he believes Claudius is
            # responsible (and threatens to take the crown); Claudius
            # redirects his anger toward Hamlet.
            world(at_location("laertes", "denmark")),
            # Laertes learns of Polonius's death from Claudius — but
            # the specific killer (Hamlet) is named. Held at BELIEVED
            # because Laertes has Claudius's word; he will verify
            # during the duel plot discussion.
            told_by("laertes", "claudius",
                    killed("hamlet", "polonius"), 12,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Claudius frames the narrative"),
            told_by("laertes", "gertrude", drowned("ophelia"), 12,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="'Drown'd? O, where?'"),
            observe("laertes", dead("polonius"), 12),
            observe("laertes", dead("ophelia"), 12),
            # Laertes does NOT learn at this point that Claudius killed
            # King Hamlet. The substrate holds that fact on Claudius
            # alone, and on Hamlet+Horatio post-Mousetrap. Laertes will
            # die at τ_s=17 having never held it. This asymmetry is
            # load-bearing for OQ-AP6 — Laertes is a tragic hero whose
            # arc completes without the full-knowledge anagnorisis
            # Hamlet earns; his recognition is partial (he sees that
            # Claudius played him, not that Claudius is a regicide).
        ),
    ),

    # --- Act 4 / 5 — the duel plot (τ_s = 13) ---

    Event(
        id="E_duel_plotted",
        type="conspiracy",
        τ_s=13, τ_a=140,
        participants={"plotters": ["claudius", "laertes"],
                      "target": "hamlet"},
        effects=(
            # Claudius and Laertes plot the duel: Laertes will use
            # a rapier with the point anointed with a lethal unction;
            # Claudius has a backup poisoned cup ready in case the
            # rapier fails. Both know both halves of the plot.
            world(ordered_killing("claudius", "hamlet")),
            observe("claudius", ordered_killing("claudius", "hamlet"), 13,
                    note="the duel plot"),
            observe("laertes", ordered_killing("claudius", "hamlet"), 13,
                    note="Laertes agrees to the poisoned rapier"),
            # Gertrude is NOT told. She will drink the poisoned cup at
            # τ_s=16 without knowing it is poisoned — the substrate
            # captures her ignorance by the absence of any told_by on
            # poisoned_with_cup prior to τ_s=16.
        ),
    ),

    # --- Act 5 — the graveyard, the duel, the catastrophe (τ_s = 14..18) ---

    Event(
        id="E_graveyard_scene",
        type="encounter",
        τ_s=14, τ_a=150,
        participants={"observer": "hamlet",
                      "witness": "horatio",
                      "location": "graveyard"},
        effects=(
            # The graveyard scene — Hamlet and Horatio encounter the
            # gravedigger, hold Yorick's skull, and witness Ophelia's
            # funeral procession. Hamlet and Laertes grapple in her
            # open grave; the public confrontation foreshadows the
            # duel. Gravediggers are elided per the scope note;
            # substrate records only the location and the funeral
            # attendance.
            world(at_location("hamlet", "graveyard")),
            world(at_location("horatio", "graveyard")),
            # Hamlet now learns Ophelia is dead — he was in England
            # during her drowning.
            observe("hamlet", dead("ophelia"), 14,
                    note="at the funeral procession"),
            observe("hamlet", drowned("ophelia"), 14),
        ),
    ),

    Event(
        id="E_duel_begins",
        type="combat",
        τ_s=15, τ_a=160,
        participants={"combatants": ["hamlet", "laertes"],
                      "overseer": "claudius",
                      "witness_queen": "gertrude",
                      "witness_friend": "horatio",
                      "location": "great_hall"},
        effects=(
            # The formal duel begins. Claudius has arranged it as the
            # theatre of Hamlet's death; Laertes knows the rapier is
            # poisoned; Hamlet does not. Horatio and Gertrude attend
            # as witnesses.
            world(at_location("hamlet", "great_hall")),
            world(at_location("laertes", "great_hall")),
            world(at_location("claudius", "great_hall")),
            world(at_location("gertrude", "great_hall")),
        ),
    ),

    Event(
        id="E_gertrude_drinks_poison",
        type="poisoning",
        τ_s=16, τ_a=161,
        participants={"victim": "gertrude", "poisoner": "claudius"},
        effects=(
            # Gertrude toasts Hamlet's success with the cup Claudius
            # had poisoned as backup. Claudius tries to stop her and
            # fails. Her death sets off the catastrophe.
            world(poisoned_with_cup("gertrude")),
            world(killed("claudius", "gertrude")),
            world(dead("gertrude")),
            # Dying, Gertrude cries out that the drink is poisoned —
            # this is the first public revelation of any part of
            # Claudius's schemes.
            observe("hamlet", poisoned_with_cup("gertrude"), 16,
                    note="'the drink, the drink! I am poison'd'"),
            observe("laertes", poisoned_with_cup("gertrude"), 16),
            observe("horatio", poisoned_with_cup("gertrude"), 16),
        ),
    ),

    Event(
        id="E_hamlet_laertes_wounded",
        type="combat_exchange",
        τ_s=16, τ_a=162,
        participants={"first": "laertes", "second": "hamlet"},
        effects=(
            # In the scuffle the rapiers are exchanged (accident in
            # Shakespeare's staging); both Hamlet and Laertes are
            # wounded with the same poisoned blade. Laertes's wound
            # turns fatal first because Hamlet's hit was the cleaner.
            world(poisoned_with_blade("hamlet")),
            world(poisoned_with_blade("laertes")),
            observe("hamlet", poisoned_with_blade("hamlet"), 16,
                    note="Hamlet realizes he is dying"),
            observe("laertes", poisoned_with_blade("laertes"), 16,
                    note="Laertes also poisoned by his own trap"),
        ),
    ),

    Event(
        id="E_laertes_reveals_plot",
        type="deathbed_revelation",
        τ_s=17, τ_a=170,
        participants={"speaker": "laertes", "listener": "hamlet",
                      "witness": "horatio"},
        effects=(
            # Laertes, dying, tells Hamlet the truth: the rapier was
            # poisoned, the cup was poisoned, Claudius is to blame,
            # they are both doomed. World-level revealed_plot: the
            # conspiracy is now publicly known.
            world(revealed_plot("laertes", "claudius")),
            told_by("hamlet", "laertes",
                    ordered_killing("claudius", "hamlet"), 17,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="'the king — the king's to blame'"),
            told_by("horatio", "laertes",
                    ordered_killing("claudius", "hamlet"), 17,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="witness to the revelation"),
            # Claudius hears Laertes expose the plot — his final
            # epistemic moment. He knows the whole court now knows.
            observe("claudius", revealed_plot("laertes", "claudius"), 17,
                    note="the regicide-usurper exposed in his own hall"),
            # Hamlet's anagnorisis: the point of narrative resolution.
            # The Ghost's original commission has been honored at the
            # same beat as Hamlet recognizes he is doomed — the A12
            # peripeteia-anagnorisis binding at BINDING_SEPARATED
            # distance 9 (from E_hamlet_kills_polonius at τ_s=8 to
            # here at τ_s=17) closes here.
            observe("hamlet", revealed_plot("laertes", "claudius"), 17),
        ),
    ),

    Event(
        id="E_hamlet_kills_claudius",
        type="murder",
        τ_s=17, τ_a=171,
        participants={"killer": "hamlet", "victim": "claudius"},
        effects=(
            # Hamlet stabs Claudius with the poisoned blade AND forces
            # him to drink from the poisoned cup — revenge executed
            # in both modes. The Ghost's revenge commission is
            # discharged.
            world(killed("hamlet", "claudius")),
            world(dead("claudius")),
            world(poisoned_with_cup("claudius")),
            world(poisoned_with_blade("claudius")),
            # Note: king(claudius, denmark) is NOT retracted — per
            # macbeth.py's convention, the king fact persists
            # historically. Fortinbras inherits the throne at the
            # play's close, which would be authored by asserting
            # `king(fortinbras, denmark)` in a future Session if a
            # forcing function argues for it. The REGICIDE_RULE on
            # `killed(hamlet, claudius) ∧ king(claudius, _)` fires
            # for Hamlet's kill against Claudius as a second regicide
            # in the play.
            observe("horatio", killed("hamlet", "claudius"), 17,
                    note="Horatio as witness"),
        ),
    ),

    Event(
        id="E_laertes_dies",
        type="death",
        τ_s=17, τ_a=172,
        participants={"who": "laertes"},
        effects=(
            world(dead("laertes")),
        ),
    ),

    Event(
        id="E_hamlet_dies",
        type="death",
        τ_s=18, τ_a=180,
        participants={"who": "hamlet",
                      "witness": "horatio",
                      "location": "great_hall"},
        effects=(
            # Hamlet dies in Horatio's arms, having asked Horatio to
            # "report me and my cause aright" to those who come after.
            # Horatio is the sole surviving witness of the whole story
            # — load-bearing for the play's self-description as a tale
            # to be told.
            world(dead("hamlet")),
            # Hamlet's kingship — he was the rightful heir; in his
            # final moments he names Fortinbras as successor. Elided
            # at substrate level per scope note.
            observe("horatio", dead("hamlet"), 18,
                    note="'now cracks a noble heart'"),
        ),
    ),

]


# ----------------------------------------------------------------------------
# Preplay disclosures — audience-pre-knowledge.
# ----------------------------------------------------------------------------
#
# Hamlet opens with the audience already loaded with several facts
# that the play takes for granted rather than builds up to. The
# Elizabethan audience knows the ur-Hamlet outline but not the
# tragedy's beat-by-beat structure; the substrate preplay set
# captures only the Act-1-Scene-1 take-for-granted facts.
#
# Notably NOT preplay:
#   - the murder itself (killed(claudius, king_hamlet)) — the Ghost
#     reveals it
#   - the murder method (poisoned_in_ear) — the Ghost reveals it
#   - the revenge commission — the Ghost delivers it
#   - Hamlet's feigned madness — adopted on-stage
#   - Claudius's culpability in any form — disclosed only through
#     Hamlet's verification and Laertes's deathbed reveal
#
# These are the play's epistemic payoff. Keeping them off the
# preplay set is load-bearing for OQ-AP5 (the Ghost's revelation
# must land as news to the audience as well as to Hamlet).

PREPLAY_DISCLOSURES = (
    Disclosure(prop=dead("king_hamlet"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=king("claudius", "denmark"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=married("claudius", "gertrude"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=queen("gertrude", "denmark"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=prince_of("hamlet", "denmark"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=brother_of("claudius", "king_hamlet"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=served_by("claudius", "polonius"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
)


# ----------------------------------------------------------------------------
# Sjuzhet — largely linear; τ_d ≈ τ_s for in-play events.
# ----------------------------------------------------------------------------
#
# The pre-play events (E_king_hamlet_reigns, E_claudius_brother_of_king,
# E_polonius_family_standing, E_king_hamlet_poisoned, E_claudius_crowned,
# E_claudius_marries_gertrude) are NOT sjuzhet entries — they never appear
# as staged scenes. Their content enters the reader projection through
# the PREPLAY_DISCLOSURES set at τ_d=0 (the watch scene) and through
# later revelatory events (the Ghost's speech promotes killed() from the
# reader's absent state to BELIEVED, and the Mousetrap promotes it to
# KNOWN).
#
# Focalization distribution (26 entries):
#   hamlet:   12 entries (his play)
#   horatio:   2 entries (frame-opener and frame-closer)
#   claudius:  1 entry  (the prayer scene, A11 chain step)
#   ophelia:   1 entry  (the mad scene)
#   laertes:   1 entry  (his return)
#   polonius:  1 entry  (his theory pitch)
#   None:      8 entries (public court / plotting / ceremony scenes
#                         where no single focalizer carries the weight)

SJUZHET = [

    # τ_d=0 — Act 1 Scene 1. The watch on the ramparts; Horatio sees
    # the Ghost. The audience arrives loaded with the preplay
    # disclosures (King Hamlet dead, Claudius king, marriage
    # announced); the opening scene plants the apparition hook.
    SjuzhetEntry(
        event_id="E_ghost_seen_by_watch",
        τ_d=0,
        focalizer_id="horatio",
        disclosures=PREPLAY_DISCLOSURES,
    ),

    # τ_d=1 — Act 1.2 compressed (Horatio brings news to Hamlet).
    # Pivot to Hamlet's perspective.
    SjuzhetEntry(
        event_id="E_horatio_tells_hamlet",
        τ_d=1,
        focalizer_id="hamlet",
        disclosures=(),
    ),

    # τ_d=2 — Act 1.5. The Ghost's revelation. Load-bearing for OQ-AP5.
    SjuzhetEntry(
        event_id="E_hamlet_meets_ghost",
        τ_d=2,
        focalizer_id="hamlet",
        disclosures=(),
    ),

    # τ_d=3 — end of Act 1. Hamlet confides in Horatio.
    SjuzhetEntry(
        event_id="E_hamlet_sworn_to_secrecy",
        τ_d=3,
        focalizer_id="hamlet",
        disclosures=(),
    ),

    # τ_d=4 — still end of Act 1. Hamlet adopts the antic disposition.
    SjuzhetEntry(
        event_id="E_hamlet_adopts_antic_disposition",
        τ_d=4,
        focalizer_id="hamlet",
        disclosures=(),
    ),

    # τ_d=5 — Act 2.2. Polonius pitches his love-madness theory.
    # Polonius focalizes; his self-assurance is the scene's register.
    SjuzhetEntry(
        event_id="E_polonius_theory",
        τ_d=5,
        focalizer_id="polonius",
        disclosures=(),
    ),

    # τ_d=6 — Act 2.2 later. The players arrive; Hamlet conceives
    # the Mousetrap.
    SjuzhetEntry(
        event_id="E_players_arrive",
        τ_d=6,
        focalizer_id="hamlet",
        disclosures=(),
    ),

    # τ_d=7 — Act 3.2. The Mousetrap performance — epistemic hinge.
    SjuzhetEntry(
        event_id="E_mousetrap_performance",
        τ_d=7,
        focalizer_id="hamlet",
        disclosures=(),
    ),

    # τ_d=8 — Act 3.3. Claudius at prayer. A11 non-precipitating
    # chain step (the antagonist's recognition of his own moral
    # bankruptcy); Hamlet observes but the scene is Claudius's
    # soliloquy — Claudius focalizes.
    SjuzhetEntry(
        event_id="E_claudius_prays",
        τ_d=8,
        focalizer_id="claudius",
        disclosures=(),
    ),

    # τ_d=9 — Act 3.4 opening. Polonius positions behind the arras
    # in Gertrude's closet. Omniscient staging.
    SjuzhetEntry(
        event_id="E_polonius_hides_arras",
        τ_d=9,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=10 — Act 3.4. The closet confrontation.
    SjuzhetEntry(
        event_id="E_hamlet_confronts_gertrude",
        τ_d=10,
        focalizer_id="hamlet",
        disclosures=(),
    ),

    # τ_d=11 — same scene. Hamlet stabs through the arras. Hamlet's
    # peripeteia fires here (avenger → fugitive-who-killed-the-wrong-
    # man); see hamlet_aristotelian.py A12.
    SjuzhetEntry(
        event_id="E_hamlet_kills_polonius",
        τ_d=11,
        focalizer_id="hamlet",
        disclosures=(),
    ),

    # τ_d=12 — same scene, continued. The Ghost appears only to
    # Hamlet (Gertrude sees nothing) — Hamlet focalizes.
    SjuzhetEntry(
        event_id="E_ghost_in_closet",
        τ_d=12,
        focalizer_id="hamlet",
        disclosures=(),
    ),

    # τ_d=13 — Act 4.3/4.4. Court scene packaging Hamlet off to
    # England. Omniscient — Claudius's sealed orders are named by
    # the substrate but staged opaquely to the other characters.
    SjuzhetEntry(
        event_id="E_hamlet_sent_to_england",
        τ_d=13,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=14 — Act 4.5. Ophelia's mad scene. She focalizes — it is
    # her breakdown the scene inhabits.
    SjuzhetEntry(
        event_id="E_ophelia_madness",
        τ_d=14,
        focalizer_id="ophelia",
        disclosures=(),
    ),

    # τ_d=15 — Act 4.7, reported. Gertrude delivers the willow
    # speech; the drowning itself is offstage. Omniscient framing —
    # no focalizer since Gertrude *reports* rather than witnesses.
    SjuzhetEntry(
        event_id="E_ophelia_drowns",
        τ_d=15,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=16 — Act 4.5/4.7. Laertes storms back from France.
    SjuzhetEntry(
        event_id="E_laertes_returns",
        τ_d=16,
        focalizer_id="laertes",
        disclosures=(),
    ),

    # τ_d=17 — Act 4.7. Claudius and Laertes plot the duel.
    # Omniscient — two plotters, no single register.
    SjuzhetEntry(
        event_id="E_duel_plotted",
        τ_d=17,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=18 — Act 5.1. The graveyard and Ophelia's funeral.
    SjuzhetEntry(
        event_id="E_graveyard_scene",
        τ_d=18,
        focalizer_id="hamlet",
        disclosures=(),
    ),

    # τ_d=19 — Act 5.2. The formal duel begins. Omniscient —
    # public court event.
    SjuzhetEntry(
        event_id="E_duel_begins",
        τ_d=19,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=20 — mid-duel. Gertrude drinks the poisoned cup. Public
    # ceremony-turned-disaster; omniscient.
    SjuzhetEntry(
        event_id="E_gertrude_drinks_poison",
        τ_d=20,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=21 — rapier exchange; both combatants wounded.
    SjuzhetEntry(
        event_id="E_hamlet_laertes_wounded",
        τ_d=21,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=22 — Laertes's deathbed reveal. Hamlet's anagnorisis lands
    # here; the A12 peripeteia-anagnorisis binding (distance 9,
    # SEPARATED) closes. Hamlet focalizes — his recognition is the
    # scene's weight.
    SjuzhetEntry(
        event_id="E_laertes_reveals_plot",
        τ_d=22,
        focalizer_id="hamlet",
        disclosures=(),
    ),

    # τ_d=23 — Hamlet kills Claudius. Omniscient — public execution
    # of the revenge commission discharged.
    SjuzhetEntry(
        event_id="E_hamlet_kills_claudius",
        τ_d=23,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=24 — Laertes dies.
    SjuzhetEntry(
        event_id="E_laertes_dies",
        τ_d=24,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=25 — Hamlet dies in Horatio's arms. Horatio focalizes —
    # the sole survivor charged to "report me and my cause aright."
    # Structural frame-closer paired with τ_d=0's Horatio opening.
    SjuzhetEntry(
        event_id="E_hamlet_dies",
        τ_d=25,
        focalizer_id="horatio",
        disclosures=(),
    ),

]


# ----------------------------------------------------------------------------
# Descriptions — the interpretive peer surface.
# ----------------------------------------------------------------------------
#
# τ_a values start at 200 (after fabula τ_a values, which top out
# at 180). Later authoring passes can interleave without renumbering.
#
# Parallels the macbeth.py descriptions in two tracks:
#   1. Ontological reticence questions (Ghost, Hamlet's sanity,
#      Gertrude, Ophelia). Authored as authorial-uncertainty
#      descriptions marked is_question=True. These are the same
#      pattern as macbeth's D_witches_ontology_undecided and
#      D_banquet_ghost_ontology_undecided — the substrate
#      deliberately declines to commit, and that decision is
#      recorded here.
#   2. Structural reader-frames (trajectory, OQ-AP5/AP6 postures,
#      cumulative catastrophe). These name reading moves the
#      substrate supports rather than proposes as commitments.
#
# Probe-authored edits and answers (like the llm-authored
# supersessions in macbeth.py) are not present in Session 3; they
# would be added by a future probe pass against Hamlet.

DESCRIPTIONS = [

    Description(
        id="D_ghost_ontology_undecided",
        attached_to=anchor_event("E_hamlet_meets_ghost"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("The Ghost is encoded as an Entity of kind 'agent' "
              "distinct from king_hamlet. The substrate records "
              "apparition_of('ghost', …) as observation-only effects "
              "on the characters who see it (Horatio, Hamlet); no "
              "world-fact asserts the Ghost 'is' King Hamlet's spirit, "
              "nor that it is a devil in borrowed shape, nor that it "
              "is Hamlet's projection. Hamlet's own 'the spirit that I "
              "have seen may be the devil' names the question "
              "explicitly in Act 2.2. The Mousetrap supplies external "
              "corroboration for the Ghost's factual claim (Claudius "
              "killed the king) without resolving what the Ghost "
              "ontologically *is*. This reticence parallels Macbeth's "
              "Witches and Banquo's ghost — the same substrate "
              "pattern (agent-only, no world assertion) applied to "
              "the same interpretive question."),
        is_question=True,
        authored_by="author",
        τ_a=200,
    ),

    Description(
        id="D_hamlet_sanity_undecided",
        attached_to=anchor_event("E_hamlet_adopts_antic_disposition"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Hamlet's madness is encoded as feigning_madness(hamlet) "
              "— agent-level, observed only by Hamlet himself and, "
              "later, by Horatio. No world-fact mad(hamlet) is "
              "asserted (contrast ophelia at E_ophelia_madness, where "
              "world(mad('ophelia')) IS asserted). The substrate "
              "commits to the antic disposition being performance, "
              "but leaves open whether the performance becomes genuine "
              "over the course of the play — Ophelia's death, "
              "Hamlet's graveside vault with Laertes, the erratic "
              "tonal shifts between the closet scene and the duel "
              "preparation are readings that point toward something "
              "more than sustained performance. The structural "
              "choice: the substrate refuses to promote feigning to "
              "mad. A future encoding may wish to commit, or to "
              "introduce a partial-madness predicate; until then the "
              "reticence is the statement."),
        is_question=True,
        authored_by="author",
        τ_a=201,
    ),

    Description(
        id="D_gertrude_foreknowledge_undecided",
        attached_to=anchor_event("E_hamlet_confronts_gertrude"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Gertrude's state regarding Claudius's regicide is "
              "substrate-silent. She is not authored as holding "
              "killed('claudius', 'king_hamlet') at any slot — no "
              "observe, no told_by. She is equally not authored as "
              "holding its negation. The question — did Gertrude "
              "know? did she suspect? did she deliberately refuse "
              "to know? — is sustained by the play and left "
              "sustained here. The closet scene confrontation "
              "records Hamlet's accusations against her haste of "
              "remarriage but deliberately does not have him accuse "
              "her of complicity in the murder; she responds with "
              "grief but not with any signal the substrate can read "
              "as confession or denial. The cup-drinking at τ_s=16 "
              "is consistent with ignorance (she had no reason to "
              "distrust the cup) but does not require it. The "
              "substrate's silence here is the encoding's judgment: "
              "the text supplies no enough signal to commit."),
        is_question=True,
        authored_by="author",
        τ_a=202,
    ),

    Description(
        id="D_ophelia_death_undetermined",
        attached_to=anchor_event("E_ophelia_drowns"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("world(drowned('ophelia')) is asserted; the cause of "
              "the drowning is not. The substrate commits to the "
              "death and to its mechanism (drowning) but declines to "
              "author either suicide or accident. The play itself "
              "debates it in Act 5.1 (the gravediggers; the priest's "
              "'maimed rites'), so substrate-level commitment to "
              "either reading would flatten what the text "
              "deliberately keeps open. This is structurally parallel "
              "to the Ghost-ontology reticence: the substrate records "
              "observable facts and leaves the interpretive question "
              "for descriptions. A future branch (e.g., "
              ":b-ophelia-suicide) could author the suicide reading "
              "as a :contested branch, paralleling the Rashomon-style "
              "multi-branch pattern, if a forcing function argues "
              "for it."),
        is_question=True,
        authored_by="author",
        τ_a=203,
    ),

    Description(
        id="D_mousetrap_as_epistemic_instrument",
        attached_to=anchor_event("E_mousetrap_performance"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("The Mousetrap is the play's epistemic hinge. Before "
              "τ_s=6, Hamlet holds the Ghost's claim at BELIEVED "
              "(the explicit 'may be the devil' doubt); Claudius "
              "holds killed('claudius', 'king_hamlet') at KNOWN but "
              "believes nobody else does. After τ_s=6, Hamlet's hold "
              "promotes to KNOWN and Claudius infers Hamlet-knows. "
              "The mechanism is the specific detail of poison-in-ear "
              "— a fact not publicly available, shared between (by "
              "Hamlet's reading) exactly Claudius and the Ghost. "
              "When the play-within-a-play dramatizes precisely this "
              "detail and Claudius panics, Hamlet reads the panic as "
              "evidence Claudius recognized the detail — which means "
              "the Ghost had the detail — which (by Hamlet's "
              "reasoning) establishes the Ghost's reliability. The "
              "substrate captures this as a remove_held + observe "
              "pair at the Mousetrap event: the BELIEVED prop is "
              "retracted and the KNOWN prop is observed fresh. The "
              "structural move — a play-within-a-play as an epistemic "
              "verifier — is the corpus's first formal example of "
              "this pattern."),
        authored_by="author",
        τ_a=204,
    ),

    Description(
        id="D_revenge_delay_as_separated_binding",
        attached_to=anchor_event("E_hamlet_kills_polonius"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("Hamlet's 'delay' — the traditional interpretive "
              "problem (why does he wait so long?) — is rendered "
              "structurally as A12 BINDING_SEPARATED distance 9. "
              "Peripeteia fires here (τ_s=8): Hamlet stabs through "
              "the arras thinking it is Claudius, discovers he has "
              "killed Polonius, and the reversal lands — from the "
              "avenger-contemplating to the fugitive-who-has-killed-"
              "the-wrong-man. Anagnorisis lands at τ_s=17 "
              "(E_laertes_reveals_plot): the recognition that "
              "Claudius's counter-plot has reached him and he is "
              "doomed. Distance 9 is the widest-separation binding "
              "in the corpus (Oedipus=5, Macbeth=COINCIDENT). The "
              "structural rendering of 'delay' is the long arc "
              "between these two poles — not the famous soliloquies "
              "as individual beats but the entire middle phase as a "
              "stretched reversal-without-recognition. OQ-AP7 banks "
              "whether 'separated' as a single category is adequate "
              "over this range."),
        authored_by="author",
        τ_a=205,
    ),

    Description(
        id="D_parallel_tragic_heroes",
        attached_to=anchor_event("E_hamlet_dies"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("Three characters are authored with "
              "is_tragic_hero=True in hamlet_aristotelian.py: "
              "Hamlet, Claudius, and Laertes. OQ-AP6 pressure: the "
              "A10 dialect's ArMythosRelation(kind='parallel') types "
              "*inter*-mythos relations; Hamlet forces the question "
              "of whether intra-mythos parallel tragic arcs need "
              "their own structural hook. At the substrate layer, "
              "the three arcs are readable through their knowledge "
              "states: Hamlet (uncertain → verified → revenge); "
              "Claudius (sole knower → exposed → killed); Laertes "
              "(misled by Claudius's framing → co-conspirator → "
              "deathbed-partial-reversal). Only Hamlet earns the "
              "full recognition; Laertes dies without knowing that "
              "Claudius is a regicide, and Claudius dies without "
              "having repented in a way the substrate records. The "
              "three arcs share a mythos but do not share a moral "
              "structure — which is itself a reading the encoding "
              "supports and the dialect does not yet name."),
        authored_by="author",
        τ_a=206,
    ),

    Description(
        id="D_ghost_commission_posture",
        attached_to=anchor_event("E_hamlet_meets_ghost"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("OQ-AP5 pressure: the Ghost is a second fate-agent in "
              "the corpus after Macbeth's Witches, with a distinct "
              "causal posture. The Witches equivocate (literally "
              "true, catastrophically misleading prophecies); the "
              "Ghost gives direct factual revelation plus direct "
              "commission. Substrate: the Witches' prophecies are "
              "authored as agent-only (told_by Macbeth/Banquo, no "
              "world-facts); the Ghost's claim is similarly agent-"
              "only (told_by Hamlet), but bundled with a commission "
              "(ghost_demands_revenge) that has no Witch-equivalent. "
              "The commission is restricted to Hamlet alone — "
              "Horatio learns the Ghost's *claim* about the murder "
              "(E_hamlet_sworn_to_secrecy told_by) but not the "
              "revenge demand. This asymmetry is load-bearing: it "
              "makes Hamlet the sole possessor of the revenge "
              "commission, which is the substrate-level grounding "
              "for his unique tragic-hero status among the three "
              "heroes in this mythos."),
        authored_by="author",
        τ_a=207,
    ),

    Description(
        id="D_cumulative_catastrophe",
        attached_to=anchor_event("E_hamlet_dies"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("The catastrophe is scattered across a single beat-"
              "cluster: Gertrude dies at τ_s=16, Laertes + Claudius "
              "+ Hamlet at τ_s=17–18. Four deaths within two "
              "substrate-time units, with four different moral "
              "weights — innocent (Gertrude, poisoned by her own "
              "husband's plot), redeemed-antagonist (Laertes, whose "
              "deathbed reveal restores some moral standing), "
              "regicide-usurper (Claudius, killed by the rightful "
              "heir discharging the Ghost's commission), and "
              "tragic-hero (Hamlet, whose death at the conclusion "
              "of the revenge action ends the house of Denmark). "
              "Contrast Macbeth's pattern (catastrophe scattered "
              "across three phases) and Oedipus's pattern "
              "(concentrated-at-end, single recognition-driven "
              "collapse). If OQ-AP1 (ArPathos grounding) opens, "
              "Hamlet is the forcing case for cluster-pathos — a "
              "single beat carrying four distinct moral weights."),
        authored_by="author",
        τ_a=208,
    ),

]


# ----------------------------------------------------------------------------
# Rules — inference-model-sketch-01 N1–N10
# ----------------------------------------------------------------------------
#
# Three compound predicates (fratricide, regicide, usurper). The
# usurper rule is depth-2 — its body premises include `fratricide`
# and `regicide` which are themselves rule-derived. depth_cap of 2
# is required; the substrate default of 3 suffices.
#
# Claudius is the corpus's first explicit usurper — he killed his
# brother (fratricide), killed a king (regicide; same victim), and
# became king himself. Hamlet is a regicide (killing Claudius) but
# not a usurper (he dies before taking the throne; neither condition
# of the compound premise chain fires).
#
# Rules compose with identity substitution (N4); Hamlet's encoding
# uses no identity placeholders so substitution does not contribute.

FRATRICIDE_RULE = Rule(
    id="R_fratricide_from_killed_and_brother",
    head=Prop("fratricide", ("X", "Y")),
    body=(
        Prop("killed",     ("X", "Y")),
        Prop("brother_of", ("X", "Y")),
    ),
)

REGICIDE_RULE = Rule(
    id="R_regicide_from_killed_and_king",
    head=Prop("regicide", ("X", "Y")),
    body=(
        Prop("killed", ("X", "Y")),
        Prop("king",   ("Y", "R")),  # R is the realm; range-restricted
                                     # because R appears in the body.
    ),
)

USURPER_RULE = Rule(
    id="R_usurper_from_fratricide_regicide_and_king",
    head=Prop("usurper", ("X",)),
    body=(
        Prop("fratricide", ("X", "V1")),
        Prop("regicide",   ("X", "V2")),
        Prop("king",       ("X", "R")),
    ),
)

RULES = (
    FRATRICIDE_RULE,
    REGICIDE_RULE,
    USURPER_RULE,
)
