"""
King Lear — the encoded fabula (substrate skeleton).

**Session 1 scope (bfecd73):** entities, canonical branches, prop
constructors, event helpers, FABULA (45 events covering pre-play
standing facts through the final deaths), and one derivation rule.
Knowledge effects authored only on the load-bearing beats.

**Session 2 scope (b75fa11):** Aristotelian overlay
(`lear_aristotelian.py`) pressuring OQ-AP14 (instrumental-kind A13)
and OQ-AP15 (absent-character catharsis).

**Session 3 scope (this file):** PREPLAY_DISCLOSURES (4 facts — Lear
opens with less audience-pre-knowledge than Hamlet; only the kingdom-
political-structure and Gloucester-family structure are pre-loaded),
SJUZHET (42 in-play entries with focalization — Lear focalizes 17,
distributed across Gloucester / Edgar / Edmund / Cordelia / Kent /
Fool and omniscient public scenes), DESCRIPTIONS (12 interpretive
records covering Lear's madness, Cordelia's motivation, the Fool's
disappearance, Edmund's deathbed reversal, the OQ-AP14/OQ-AP15
reader frames, the OQ-LEAR-1/OQ-LEAR-2 structural questions, the
double-plot unity reading, the offstage-catharsis reading, the
parallel-tragic-fathers frame, and the Gloucester-blinding-as-
symbolic-inversion motif).

Story content only. No substrate logic. This file parallels
`hamlet.py` in shape and is the fourth Shakespeare-tragedy encoding
alongside Macbeth and Hamlet (plus the non-Shakespeare classical
corpus Oedipus). Lear is the corpus's second ≥3-tragic-hero
encoding (after Hamlet) and is banked as the second-site forcing
case for two open questions surfaced by Hamlet's Session 6 probe
(`aristotelian-probe-sketch-04`):

- **OQ-AP14** — Instrumental-kind `ArCharacterArcRelation`. Lear's
  Gloucester subplot runs on a chain of *instruments*: Edmund
  forges a letter (E_edmund_forges_letter) whose content is
  believed by Gloucester (E_edmund_shows_gloucester), then
  reinforces the forgery with a self-inflicted wound
  (E_edmund_stages_wound) whose observation cements Gloucester's
  false belief. Later Edgar-as-Poor-Tom stages a different
  instrument — a non-existent Dover-cliff fall — to shift
  Gloucester's despair into acceptance. Both brothers wield
  instruments on their father, with opposite moral polarity.
  Hamlet surfaces the instrumental-kind pressure with a single
  A13 candidate (Claudius wielding Laertes as instrument in the
  poisoning plot); Lear offers three structurally parallel
  instrumentation chains (Edmund→letter→Gloucester;
  Edmund→wound→Gloucester; Edgar→Dover-staging→Gloucester) plus
  a separate instrumental chain in the main plot
  (Goneril→Oswald against Lear).

- **OQ-AP15** — Absent-character catharsis. Lear's climactic
  catharsis lands on Cordelia's body carried onstage by Lear —
  but the hanging itself is never shown. The dialect currently
  binds catharsis to ArCharacter records whose defining events
  are structurally visible; Cordelia's death is reported and
  visually present (as corpse) but its defining event is
  offstage. Parallel offstage deaths: Gloucester's death (joy-
  shock, reported by Edgar, E_gloucester_dies), Cornwall's
  death (servant's wound, E_cornwall_dies authored but not
  itself a center-stage event), Regan's collapse (collateral of
  Goneril's earlier poisoning). Lear is the corpus's densest
  site of absent-death catharsis.

Encoding choices (explicit, so future readers understand the slice):

- **Branches: canonical only.** Lear has no Rashomon-style contested
  testimony. The text is textually contested (Q1 vs F differ on the
  ending and on several scenes), but the encoding follows the Folio
  tradition; the authorial-intent question is a descriptions-layer
  concern. Edmund's motivations and Edgar's disguises are
  performed but not contested.

- **Identity placeholders: none.** Like Macbeth and Hamlet (and
  unlike Oedipus), Lear has no substrate-level identity
  confusion. Edgar's "Poor Tom" and Kent's "Caius" are
  *disguises* — authored at the agent level (the agents know
  who they really are; Lear and Gloucester do not). Gloucester's
  failure to recognize Edgar-as-guide at Dover is a believed-
  identity question, not a substrate identity-predicate question.

- **Audience-pre-knowledge disclosures: minimal.** Unlike Macbeth
  or Hamlet, Lear has no folkloric pre-loading; the audience
  comes in fresh. The substrate takes for granted only the
  existence of the British realm and the three daughters as of
  τ_s=-30; nothing else is preplay for a general Jacobean
  audience. Session 3's PREPLAY_DISCLOSURES will be shorter than
  Hamlet's seven-fact set (candidate: four facts — Lear is king;
  he has three daughters; Gloucester is a nobleman; Gloucester
  has two sons with Edmund younger and illegitimate). The murder
  plots, the forgery, the division, and the catastrophe are
  entirely built up through the play.

- **Focalization: distributed.** Lear has two parallel plots
  running concurrently; Session 3's SJUZHET will distribute
  focalization across Lear, Gloucester, Edgar, Edmund, Kent,
  Cordelia, and occasional omniscient-court entries. Unlike
  Hamlet (primarily Hamlet-focalized), Lear's plot structure
  requires shifting focalization to carry the Gloucester subplot.
  Deferred to Session 3.

- **Authored compound predicates:** only `fratricide(X, Y)`. The
  derivation `killed(X, Y) ∧ brother_of(X, Y) ⇒ fratricide(X, Y)`
  fires on Edgar killing Edmund at E_edgar_defeats_edmund. Lear's
  thematic registers (filial ingratitude, Nature-vs-convention,
  madness-as-sight) do not reduce cleanly to substrate-derivable
  compounds; they live on descriptions (Session 3) and on the
  Aristotelian overlay (Session 2). No regicide rule (no king is
  killed in Lear — he dies of grief). No usurper rule (Goneril/
  Regan inherit rather than usurp). No patricide rule (no
  parent-killing, though Goneril/Regan come close in cruelty).

- **Supernatural ontology: absent.** Unlike Hamlet's Ghost and
  Macbeth's Witches, Lear has no supernatural agents on stage.
  The gods are invoked rhetorically ("As flies to wanton boys, are
  we to the gods — they kill us for their sport") but never
  appear or act. Fate-agent pressure does not arise; OQ-AP5 is
  neither re-surfaced nor re-opened by Lear.

- **Scope of the play encoded: the full canonical spine of both
  plots, compressed.** Secondary scenes (Oswald's death at
  Edgar's hand, the Gentleman's reports, Fool's songs, some
  messenger traffic) are elided or compressed into their
  containing events. Curan (the courtier who tips Edmund off),
  the Doctor, and the nameless Captain who actually hangs
  Cordelia are not authored as entities — their structural
  contributions are compressed into the events they enable.

- **The Fool's disappearance** (after III.vi, "And my poor fool
  is hang'd") is not modeled as a substrate event; the Fool's
  final presence on stage is at E_lear_mock_trial, and after
  that he simply vanishes from FABULA — matching the
  authorial reticence.

- **"Forged letter" as predicate, not entity.** Following the
  Hamlet pattern for non-agent instruments (the Mousetrap play
  is a predicate/event, not an entity), the forged letter is
  encoded as a world-level `forged_letter(forger, imputed_author)`
  fact plus belief-effects at the reading event. No Entity record
  for the letter itself. Dover cliff is an entity (it's a
  location); the "staged fall" at it is an event with effects.

Encoding pressures the two banked OQs (OQ-AP14, OQ-AP15) without
sketch-03-level modification of the substrate or the substrate's
shape. All predicate and event constructions reuse the existing
substrate vocabulary.
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

# --- Main plot: Lear's family and court ---
lear       = Entity(id="lear",       name="Lear",             kind="agent")
goneril    = Entity(id="goneril",    name="Goneril",          kind="agent")
regan      = Entity(id="regan",      name="Regan",            kind="agent")
cordelia   = Entity(id="cordelia",   name="Cordelia",         kind="agent")
albany     = Entity(id="albany",     name="Duke of Albany",   kind="agent")
cornwall   = Entity(id="cornwall",   name="Duke of Cornwall", kind="agent")
kent       = Entity(id="kent",       name="Earl of Kent",     kind="agent")
fool       = Entity(id="fool",       name="the Fool",         kind="agent")
france     = Entity(id="france",     name="King of France",   kind="agent")
burgundy   = Entity(id="burgundy",   name="Duke of Burgundy", kind="agent")
oswald     = Entity(id="oswald",     name="Oswald",           kind="agent")

# --- Subplot: Gloucester's family ---
gloucester = Entity(id="gloucester", name="Earl of Gloucester", kind="agent")
edgar      = Entity(id="edgar",      name="Edgar",            kind="agent")
edmund     = Entity(id="edmund",     name="Edmund",           kind="agent")

# --- Locations ---
britain           = Entity(id="britain",           name="Britain",
                           kind="location")
lears_court       = Entity(id="lears_court",       name="Lear's court",
                           kind="location")
gonerils_castle   = Entity(id="gonerils_castle",   name="Goneril's castle",
                           kind="location")
# Regan shares Cornwall's castle; in the Folio she returns to Gloucester's
# castle for the blinding scene (Cornwall is hosted by Gloucester at that
# point). The encoding uses Gloucester's castle as the shared Cornwall
# residence for the blinding, and a separate regans_castle for Lear's
# arrival there before he flees to the heath.
regans_castle     = Entity(id="regans_castle",     name="Regan's residence",
                           kind="location")
gloucesters_castle = Entity(id="gloucesters_castle",
                            name="Gloucester's castle",
                            kind="location")
the_heath         = Entity(id="the_heath",         name="the heath",
                           kind="location")
hovel             = Entity(id="hovel",             name="the hovel (on the heath)",
                           kind="location")
dover             = Entity(id="dover",             name="Dover (and the cliff)",
                           kind="location")
british_camp      = Entity(id="british_camp",      name="the British camp",
                           kind="location")
prison            = Entity(id="prison",            name="the prison (at the British camp)",
                           kind="location")


ENTITIES = [
    # Main plot
    lear, goneril, regan, cordelia, albany, cornwall, kent, fool,
    france, burgundy, oswald,
    # Subplot
    gloucester, edgar, edmund,
    # Locations
    britain, lears_court, gonerils_castle, regans_castle,
    gloucesters_castle, the_heath, hovel, dover, british_camp,
    prison,
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
# moral / affective / ontological register (is Lear mad; is Edmund
# merely ambitious or wholly evil; is Cordelia's "nothing" pride or
# honesty) lives on descriptions.


def king(who: str, realm: str) -> Prop:
    return Prop("king", (who, realm))

def duke_of(who: str, realm_portion: str) -> Prop:
    # Albany and Cornwall as dukes; after the division each inherits
    # a half of the realm through their wives.
    return Prop("duke_of", (who, realm_portion))

def earl_of(who: str, realm_portion: str) -> Prop:
    # Kent, Gloucester — nobles of a rank below duke.
    return Prop("earl_of", (who, realm_portion))

def parent_of(parent: str, child: str) -> Prop:
    return Prop("parent_of", (parent, child))

def married(a: str, b: str) -> Prop:
    return Prop("married", (a, b))

def brother_of(a: str, b: str) -> Prop:
    # Symmetric; authored both directions where used. Edgar and Edmund
    # are half-brothers by blood (different mothers) but the text uses
    # "brother" and the rule FRATRICIDE fires on the relation. The
    # legitimacy distinction is a separate `illegitimate` predicate
    # below; it does not affect brother_of.
    return Prop("brother_of", (a, b))

def illegitimate(who: str) -> Prop:
    # Thematic register but authored as a substrate fact — Edmund's
    # illegitimacy is structurally load-bearing in the play (primogeniture
    # excludes him, which his opening soliloquy inverts). Gloucester and
    # Edgar are implicitly legitimate by the play's world; the predicate
    # is asserted only on Edmund.
    return Prop("illegitimate", (who,))

def at_location(who: str, where: str) -> Prop:
    return Prop("at_location", (who, where))

def served_by(lord: str, servant: str) -> Prop:
    # Used for Oswald serving Goneril, and (initially) Kent and
    # Gloucester serving Lear. Disguised service (Kent-as-Caius) is
    # authored as a separate serves_as_caius predicate at the disguise
    # event.
    return Prop("served_by", (lord, servant))

def banished(who: str) -> Prop:
    return Prop("banished", (who,))

def disinherited(who: str) -> Prop:
    # Cordelia at E_cordelia_disinherited. Separate from banished (Kent).
    return Prop("disinherited", (who,))

def disguised_as(who: str, alias: str) -> Prop:
    # Kent-as-"caius" post-banishment; Edgar-as-"poor_tom" post-flight.
    # The alias is a string token, not an Entity; authorial reticence
    # about whether Poor Tom has an independent fictive existence.
    return Prop("disguised_as", (who, alias))

def killed(killer: str, victim: str) -> Prop:
    return Prop("killed", (killer, victim))

def dead(who: str) -> Prop:
    return Prop("dead", (who,))

def blinded(who: str) -> Prop:
    return Prop("blinded", (who,))

def hanged(who: str) -> Prop:
    return Prop("hanged", (who,))

def poisoned(who: str) -> Prop:
    return Prop("poisoned", (who,))

def suicide(who: str) -> Prop:
    # Goneril off-stage. Distinct cause-of-death from killed(X, Y).
    return Prop("suicide", (who,))

def ordered_killing(orderer: str, victim: str) -> Prop:
    # Edmund orders Cordelia hanged; Cornwall orders Gloucester blinded
    # (authored; the act is then accomplished by Cornwall himself with
    # Regan). Substrate records the order distinct from the act.
    return Prop("ordered_killing", (orderer, victim))

def mad(who: str) -> Prop:
    # World-level claim. Lear's madness is an unstable authored claim —
    # the substrate marks the onset at E_storm_on_heath and the
    # partial dissipation at E_lear_cordelia_reconcile. Descriptions
    # layer carries the interpretive question (is Lear's madness
    # clinically real, performatively assumed, or authorially
    # ambiguous).
    return Prop("mad", (who,))

def divided_realm(realm: str) -> Prop:
    # Marker fact asserted at E_kingdom_divided. The realm is no longer
    # a single polity; portions are held by Goneril+Albany and
    # Regan+Cornwall respectively.
    return Prop("divided_realm", (realm,))


# Instrumental-shape predicates. The OQ-AP14 forcing surface. Each
# records a world-level fact about an instrument and its wielder; the
# effects of the instrument on its target land as KnowledgeEffects at
# the relevant events.

def forged_letter(forger: str, imputed_author: str) -> Prop:
    # Edmund forges a letter purporting to be from Edgar. The predicate
    # asserts the forgery at world-level; the imputed author is a
    # separate substrate fact from the actual forger.
    return Prop("forged_letter", (forger, imputed_author))

def staged_wound(agent: str) -> Prop:
    # Edmund cuts his own arm at E_edmund_stages_wound. The wound is
    # world-real; its *cause* is world-level Edmund (self-inflicted)
    # whereas Gloucester and others attribute it to Edgar. Distinct
    # from genuine injury sustained in combat.
    return Prop("staged_wound", (agent,))

def staged_cliff_fall(agent: str, location: str) -> Prop:
    # Edgar-as-Poor-Tom stages the Dover suicide scene for Gloucester.
    # World-level fact: the "cliff" was flat ground; Gloucester's
    # belief that he fell is a belief effect, not a world effect.
    return Prop("staged_cliff_fall", (agent, location))

def plots_against(plotter: str, target: str) -> Prop:
    # Content predicate used for the forged-letter contents: the
    # letter *claims* Edgar plots against Gloucester. At world level
    # this is FALSE (no such plot exists); Gloucester acquires it
    # as a BELIEVED held-fact, not a KNOWN one, and the author's
    # reticence about held-state vs world-state carries the
    # instrument's deception.
    return Prop("plots_against", (plotter, target))


# Compound / moral-register predicates. Authored as predicate
# constructors; derived via RULES below at query time (same pattern
# as Macbeth's kinslayer and Hamlet's fratricide/regicide/usurper).

def fratricide(slayer: str, victim: str) -> Prop:
    # ⇐ killed(X, Y) ∧ brother_of(X, Y)
    # Edgar kills (mortally wounds) Edmund at E_edgar_defeats_edmund.
    # Half-brother status is sufficient per the text; the brother_of
    # predicate is authored symmetrically on Edgar/Edmund in E_gloucester_
    # family regardless of legitimacy.
    return Prop("fratricide", (slayer, victim))


# ----------------------------------------------------------------------------
# Event helpers — same pattern as macbeth.py / hamlet.py / oedipus.py.
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
#   - τ_s ≤ -20  : deep standing facts (kingship, marriages, families)
#   - τ_s = -5   : Edmund's internal-resentment precursor (knowledge only)
#   - τ_s = 0    : Act I opens (Lear announces intent to divide the realm)
#   - τ_s = 1..8 : Act I (love test, disinheritance, kingdom divided, Gloucester
#                 subplot opens with Edmund's forgery)
#   - τ_s = 9..17: Act II (Lear's humiliation at Goneril's and Regan's)
#   - τ_s = 18..22: Act III (storm, hovel, mock trial, blinding)
#   - τ_s = 23..27: Act IV (Dover, Cordelia's return, reconciliation)
#   - τ_s = 28..35: Act V (battle, duel, offstage deaths, final catastrophe)
#
# The play's time compresses aggressively in Acts IV–V — the duel, the
# simultaneous poisoning/suicide/confession, and the hanging attempt
# all occur within a substrate-close cluster. Session 3+ may refine
# τ_s for the final cluster if the SJUZHET layer needs sharper
# distinctions.

FABULA = [

    # --- Pre-play (τ_s < 0) ---

    Event(
        id="E_lear_reigns",
        type="standing",
        τ_s=-30, τ_a=1,
        participants={"who": "lear"},
        effects=(
            # Lear is king of Britain with three daughters, two married.
            # Goneril and Regan are married to Albany and Cornwall
            # respectively. Cordelia is unmarried; her impending betrothal
            # is what the love-test purports to decide.
            world(king("lear", "britain")),
            world(parent_of("lear", "goneril")),
            world(parent_of("lear", "regan")),
            world(parent_of("lear", "cordelia")),
            world(married("goneril", "albany")),
            world(married("regan", "cornwall")),
            world(duke_of("albany", "north")),
            world(duke_of("cornwall", "south")),
            # Kent is Lear's loyal earl-counselor.
            world(earl_of("kent", "britain")),
            world(served_by("lear", "kent")),
            # Oswald serves Goneril as steward.
            world(served_by("goneril", "oswald")),
            # Court knowledge of the reigning structure. Every named
            # agent knows who the king is and the family composition.
            observe("lear", king("lear", "britain"), -30),
            observe("goneril", king("lear", "britain"), -30),
            observe("regan", king("lear", "britain"), -30),
            observe("cordelia", king("lear", "britain"), -30),
            observe("kent", king("lear", "britain"), -30,
                    note="Kent the loyal counselor knows his king"),
            observe("cordelia", parent_of("lear", "cordelia"), -30),
            observe("goneril", parent_of("lear", "goneril"), -30),
            observe("regan", parent_of("lear", "regan"), -30),
        ),
    ),

    Event(
        id="E_gloucester_family",
        type="standing",
        τ_s=-25, τ_a=2,
        participants={"father": "gloucester",
                      "legitimate_son": "edgar",
                      "bastard_son": "edmund"},
        effects=(
            # Gloucester is Earl of Gloucester; Edgar is his legitimate
            # son and heir. Edmund is his illegitimate son. Authored
            # at deep negative τ_s so the brother_of relation is always
            # in world-scope; load-bearing for the FRATRICIDE rule at
            # E_edgar_defeats_edmund.
            world(earl_of("gloucester", "britain")),
            world(parent_of("gloucester", "edgar")),
            world(parent_of("gloucester", "edmund")),
            world(brother_of("edgar", "edmund")),
            world(brother_of("edmund", "edgar")),
            # Edmund's illegitimacy — structurally load-bearing for the
            # Gloucester subplot. Primogeniture excludes him; his
            # opening soliloquy turns this into a motive.
            world(illegitimate("edmund")),
            # Family awareness. Gloucester and both sons know the
            # structure; Lear's court also knows (Gloucester is an
            # earl of the realm, and Kent meets Edmund in the opening
            # scene with Gloucester introducing him).
            observe("gloucester", parent_of("gloucester", "edgar"), -25),
            observe("gloucester", parent_of("gloucester", "edmund"), -25),
            observe("edgar", parent_of("gloucester", "edgar"), -25),
            observe("edgar", brother_of("edgar", "edmund"), -25),
            observe("edmund", parent_of("gloucester", "edmund"), -25),
            observe("edmund", brother_of("edmund", "edgar"), -25),
            observe("edmund", illegitimate("edmund"), -25,
                    note="Edmund knows his status and resents it"),
            observe("kent", parent_of("gloucester", "edgar"), -25),
            observe("kent", parent_of("gloucester", "edmund"), -25),
        ),
    ),

    Event(
        id="E_edmund_resolves_to_plot",
        type="internal_resolve",
        τ_s=-5, τ_a=3,
        participants={"plotter": "edmund"},
        effects=(
            # Edmund's resolution to displace Edgar via forgery. No
            # world-level effect (the plot is not yet executed); only
            # Edmund holds the intention. Authored as an agent-internal
            # knowledge fact using an opaque BELIEVED slot on
            # plots_against — the intention exists; its execution does
            # not. Later events establish the world-level forgery.
            #
            # This is a minimal Session-1 authorship of the soliloquy;
            # Session 3 will give it structure with DESCRIPTIONS
            # ("Now, gods, stand up for bastards!") and may add
            # additional held-fact projections.
            observe("edmund", plots_against("edmund", "edgar"), -5,
                    confidence=Confidence.CERTAIN,
                    slot=Slot.KNOWN,
                    note="Edmund's internal resolution — "
                         "matches the 'stand up for bastards' "
                         "soliloquy"),
        ),
    ),

    # --- Act I: the love test and the kingdom divided ---

    Event(
        id="E_lear_announces_division",
        type="royal_decree",
        τ_s=0, τ_a=10,
        participants={"king": "lear", "heirs": ("goneril", "regan", "cordelia")},
        effects=(
            # Lear announces his intent to divide the kingdom among his
            # daughters in proportion to their declarations of love.
            # The love-test structure is itself the decree — the
            # division does not yet happen; it is the proposed scheme.
            #
            # Agents present: the entire court. Kent, Gloucester, Albany,
            # Cornwall, the three daughters, France and Burgundy (the
            # suitors for Cordelia). Edmund is at Gloucester's side as
            # his newly-introduced bastard son.
            observe("lear", king("lear", "britain"), 0,
                    note="the king affirms his intent to step down"),
            observe("goneril", at_location("goneril", "lears_court"), 0),
            observe("regan", at_location("regan", "lears_court"), 0),
            observe("cordelia", at_location("cordelia", "lears_court"), 0),
            observe("kent", at_location("kent", "lears_court"), 0),
            observe("gloucester", at_location("gloucester", "lears_court"), 0),
            observe("edmund", at_location("edmund", "lears_court"), 0,
                    note="Edmund meets the court for the first time"),
            observe("france", at_location("france", "lears_court"), 0),
            observe("burgundy", at_location("burgundy", "lears_court"), 0),
        ),
    ),

    Event(
        id="E_love_test_goneril",
        type="speech_act",
        τ_s=1, τ_a=11,
        participants={"speaker": "goneril", "addressee": "lear"},
        effects=(
            # Goneril's false declaration: "Sir, I love you more than
            # words can wield the matter." The court hears it; Lear
            # believes it. Cordelia is observing; her internal reaction
            # is the wedge that drives her "nothing" at τ_s=3.
            observe("lear", at_location("lear", "lears_court"), 1),
            # Cordelia observes Goneril's speech and marks it as
            # performance — this is load-bearing for her refusal below.
            observe("cordelia", at_location("goneril", "lears_court"), 1,
                    note="Cordelia hears Goneril's flattery"),
            # No world-level effect on love (the play carefully leaves
            # Goneril's *actual* affection unspecified; subsequent
            # events show the flattery was instrumental).
        ),
    ),

    Event(
        id="E_love_test_regan",
        type="speech_act",
        τ_s=2, τ_a=12,
        participants={"speaker": "regan", "addressee": "lear"},
        effects=(
            # Regan matches and exceeds: "I am made of that self
            # metal as my sister, and prize me at her worth." Again
            # instrumental; Cordelia observes both.
            observe("cordelia", at_location("regan", "lears_court"), 2,
                    note="Cordelia hears Regan's flattery"),
        ),
    ),

    Event(
        id="E_love_test_cordelia",
        type="speech_act",
        τ_s=3, τ_a=13,
        participants={"speaker": "cordelia", "addressee": "lear"},
        effects=(
            # Cordelia's "Nothing, my lord" — the play's first tragic
            # inflection. World-level, Cordelia's love is real (the play
            # affirms this at IV.vii reconciliation); her refusal to
            # perform it under her sisters' terms is the structural
            # peripeteia for the main plot.
            #
            # Lear BELIEVES his daughter does not love him (world-
            # false). Session 3 will refine this into a finer
            # held-state projection. For Session 1 the load-bearing
            # fact is that Lear leaves the scene with a false belief.
            told_by("lear", "cordelia", plots_against("cordelia", "lear"),
                    3, slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Lear reads Cordelia's 'nothing' as rejection — "
                         "plots_against here stands in for the more "
                         "nuanced 'daughter does not love me' claim "
                         "Lear comes to hold; Session 3 may refine"),
            observe("kent", at_location("cordelia", "lears_court"), 3,
                    note="Kent marks Cordelia's honesty"),
        ),
    ),

    Event(
        id="E_cordelia_disinherited",
        type="royal_decree",
        τ_s=4, τ_a=14,
        participants={"king": "lear", "child": "cordelia"},
        effects=(
            # Lear disinherits Cordelia. World-level fact.
            world(disinherited("cordelia")),
            observe("cordelia", disinherited("cordelia"), 4),
            observe("kent", disinherited("cordelia"), 4),
            observe("gloucester", disinherited("cordelia"), 4),
            observe("france", disinherited("cordelia"), 4),
            observe("burgundy", disinherited("cordelia"), 4),
            observe("goneril", disinherited("cordelia"), 4),
            observe("regan", disinherited("cordelia"), 4),
        ),
    ),

    Event(
        id="E_kent_banished",
        type="royal_decree",
        τ_s=5, τ_a=15,
        participants={"king": "lear", "noble": "kent"},
        effects=(
            # Kent objects to the disinheritance ("See better, Lear");
            # Lear banishes him under pain of death. World-level.
            world(banished("kent")),
            observe("kent", banished("kent"), 5),
            observe("lear", banished("kent"), 5),
            observe("cordelia", banished("kent"), 5),
            observe("gloucester", banished("kent"), 5),
        ),
    ),

    Event(
        id="E_france_marries_cordelia",
        type="betrothal",
        τ_s=6, τ_a=16,
        participants={"bride": "cordelia", "groom": "france"},
        effects=(
            # France takes Cordelia without dowry; Burgundy refuses.
            # "Fairest Cordelia, that art most rich being poor."
            world(married("cordelia", "france")),
            observe("cordelia", married("cordelia", "france"), 6),
            observe("lear", married("cordelia", "france"), 6),
            observe("france", married("cordelia", "france"), 6),
        ),
    ),

    Event(
        id="E_kingdom_divided",
        type="royal_act",
        τ_s=7, τ_a=17,
        participants={"king": "lear", "heirs": ("goneril", "regan")},
        effects=(
            # Cordelia's third is divided between Goneril and Regan.
            # Lear retains the title of king and a retinue of a
            # hundred knights, to be hosted alternately by the two
            # daughters.
            world(divided_realm("britain")),
            observe("lear", divided_realm("britain"), 7),
            observe("goneril", divided_realm("britain"), 7),
            observe("regan", divided_realm("britain"), 7),
            observe("albany", divided_realm("britain"), 7),
            observe("cornwall", divided_realm("britain"), 7),
            observe("gloucester", divided_realm("britain"), 7),
        ),
    ),

    # --- Act I, continued: Gloucester subplot opens ---
    # Edmund's instrumental chain (OQ-AP14 forcing ground). Three
    # beats: forge the letter (world-level forgery fact), show it to
    # Gloucester (Gloucester acquires false-belief), stage a wound
    # (Gloucester graduates from BELIEVED to near-KNOWN). The chain
    # unfolds over τ_s=8..11, interleaving with the main plot.

    Event(
        id="E_edmund_forges_letter",
        type="instrument_creation",
        τ_s=8, τ_a=18,
        participants={"forger": "edmund"},
        effects=(
            # Edmund forges a letter purporting to be from Edgar,
            # outlining a plot against Gloucester. World-level fact:
            # the letter is a forgery. Gloucester has not yet seen it.
            world(forged_letter("edmund", "edgar")),
            # Edmund knows what he's done — the forgery's agent and
            # imputed-author asymmetry is held by Edmund alone at this
            # point.
            observe("edmund", forged_letter("edmund", "edgar"), 8,
                    note="Edmund's sole knowledge of the forgery"),
        ),
    ),

    Event(
        id="E_edmund_shows_gloucester",
        type="instrument_deployment",
        τ_s=9, τ_a=19,
        participants={"agent": "edmund", "target": "gloucester"},
        effects=(
            # Gloucester sees the letter; Edmund feigns reluctance to
            # show it. Gloucester reads; his reaction is rage against
            # Edgar. Substrate-level: Gloucester acquires the letter's
            # content as a BELIEVED held-fact — "Edgar plots against
            # Gloucester" — with confidence elevated by the apparent
            # authenticity of the document. World-state: plots_against
            # is NEVER asserted; the letter's content is a lie.
            told_by("gloucester", "edmund",
                    plots_against("edgar", "gloucester"),
                    9, slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Gloucester reads the forged letter — the "
                         "instrument's first payload"),
            # Edmund knows what Gloucester now holds. The asymmetry
            # between Edmund's knowledge and Gloucester's belief is
            # the substrate signature of the instrumental relation.
            observe("edmund", plots_against("edgar", "gloucester"), 9,
                    slot=Slot.BELIEVED, confidence=Confidence.SUSPECTED,
                    note="Edmund tracks Gloucester's new belief-state "
                         "— with confidence SUSPECTED because Edmund "
                         "knows the claim is false but is modelling "
                         "Gloucester's holding of it"),
        ),
    ),

    Event(
        id="E_edmund_warns_edgar",
        type="instrument_branch",
        τ_s=10, τ_a=20,
        participants={"agent": "edmund", "target": "edgar"},
        effects=(
            # Edmund tells Edgar that Gloucester is furious with him
            # and that he must flee. This is the second branch of the
            # instrument: the same forgery operates on both Edgar and
            # Gloucester with inverse effects (Gloucester believes
            # Edgar plots; Edgar believes Gloucester is mysteriously
            # enraged). Edgar does not know the cause; he believes
            # Edmund is his friend.
            told_by("edgar", "edmund",
                    plots_against("gloucester", "edgar"),
                    10, slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Edgar's inverse of Gloucester's belief — "
                         "he thinks his father has turned on him "
                         "for some unknown reason"),
        ),
    ),

    Event(
        id="E_edmund_stages_wound",
        type="instrument_reinforcement",
        τ_s=11, τ_a=21,
        participants={"agent": "edmund", "target": "gloucester"},
        effects=(
            # Edmund cuts his own arm and claims Edgar attacked him in
            # the garden. The wound is world-real; the attribution is
            # false. Gloucester's belief promotes from BELIEVED toward
            # KNOWN under the weight of physical evidence.
            world(staged_wound("edmund")),
            observe("edmund", staged_wound("edmund"), 11),
            # Gloucester believes the wound's cover story. The
            # substrate records this as a second fact — Edgar
            # attempted murder — not just a refinement of the prior
            # belief. Session 3 may refine the relation between these
            # two beliefs (one implies, one reinforces the other).
            told_by("gloucester", "edmund", killed("edgar", "edmund"), 11,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Gloucester believes Edgar attempted fratricide "
                         "— a belief whose inverse (no attempt) remains "
                         "the world-fact. The FRATRICIDE rule does NOT "
                         "fire on this belief; rules operate on world "
                         "facts only."),
        ),
    ),

    Event(
        id="E_edgar_flees",
        type="flight",
        τ_s=12, τ_a=22,
        participants={"fugitive": "edgar"},
        effects=(
            # Edgar flees Gloucester's castle; the disguise as Poor Tom
            # is not yet adopted (it happens at E_edgar_becomes_poor_tom
            # on the heath). Between τ_s=12 and τ_s=21 Edgar is in
            # hiding — no events are authored for this interval in
            # Session 1.
            observe("edgar", banished("edgar"), 12,
                    note="effectively banished — Gloucester has ordered "
                         "him hunted down"),
        ),
    ),

    # --- Act II: Lear's humiliation ---

    Event(
        id="E_lear_at_gonerils",
        type="visit",
        τ_s=13, τ_a=23,
        participants={"guest": "lear", "host": "goneril"},
        effects=(
            # Lear arrives at Goneril's castle with his hundred knights,
            # per the terms of the division. The Fool is with him;
            # Kent (now disguised as "Caius") joins Lear's service here.
            world(at_location("lear", "gonerils_castle")),
            observe("lear", at_location("lear", "gonerils_castle"), 13),
            observe("goneril", at_location("lear", "gonerils_castle"), 13),
            observe("fool", at_location("fool", "gonerils_castle"), 13),
        ),
    ),

    Event(
        id="E_kent_returns_disguised",
        type="disguise_adoption",
        τ_s=13, τ_a=24,
        participants={"noble": "kent"},
        effects=(
            # Kent, banished, returns in disguise as "Caius" to serve
            # Lear. World-level: disguised_as(kent, "caius"). Lear
            # does not know; the audience does. Substrate records this
            # exactly — Kent holds KNOWN("disguised_as kent caius"),
            # Lear does not.
            world(disguised_as("kent", "caius")),
            observe("kent", disguised_as("kent", "caius"), 13,
                    note="Kent's sole knowledge of his own disguise"),
        ),
    ),

    Event(
        id="E_goneril_strips_retinue",
        type="betrayal_act",
        τ_s=14, τ_a=25,
        participants={"ingrate": "goneril", "victim": "lear"},
        effects=(
            # Goneril demands Lear reduce his knights from a hundred
            # to fifty. The scene culminates in Lear's curse ("Hear,
            # Nature, hear! dear goddess, hear! ... Into her womb
            # convey sterility!") — authored as a substrate observation
            # rather than a world effect (the curse is performative,
            # not metaphysically efficacious).
            observe("lear", plots_against("goneril", "lear"), 14,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Lear reads Goneril's stripping as betrayal "
                         "— unlike Gloucester's false belief about "
                         "Edgar, this belief is WORLD-TRUE; Goneril "
                         "IS against Lear, though not in the murder-"
                         "plot sense of the predicate"),
            # Lear curses Goneril and leaves for Regan's. Fool
            # commentary omitted; Session 3's SJUZHET will carry it.
        ),
    ),

    Event(
        id="E_lear_to_regans",
        type="travel",
        τ_s=15, τ_a=26,
        participants={"traveller": "lear"},
        effects=(
            # Lear, Fool, and Caius travel to Regan's residence. In
            # the play the intermediate action at Gloucester's castle
            # (where Cornwall and Regan are staying as guests) merges
            # this travel with the Gloucester subplot's storm-arc.
            # Substrate compresses: Lear arrives at regans_castle.
            world(at_location("lear", "regans_castle")),
            observe("lear", at_location("lear", "regans_castle"), 15),
            observe("regan", at_location("lear", "regans_castle"), 15),
            observe("cornwall", at_location("lear", "regans_castle"), 15),
        ),
    ),

    Event(
        id="E_regan_also_strips",
        type="betrayal_act",
        τ_s=16, τ_a=27,
        participants={"ingrate": "regan", "victim": "lear"},
        effects=(
            # Regan demands Lear reduce further — from fifty to
            # twenty-five, then to none ("What need one?"). Goneril
            # arrives; the two daughters together cast him out. The
            # substrate records Lear's second realization of betrayal,
            # now doubled and mirrored.
            observe("lear", plots_against("regan", "lear"), 16,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="second betrayal — structurally parallel to "
                         "E_goneril_strips_retinue; the A13 mirror "
                         "relation between the two ingrate-daughters "
                         "will be authored in the overlay"),
        ),
    ),

    Event(
        id="E_lear_flees_to_heath",
        type="flight",
        τ_s=17, τ_a=28,
        participants={"fugitive": "lear"},
        effects=(
            # Lear, Fool, and Caius exit into the storm. Regan orders
            # the castle gates shut. World-level: Lear is on the heath.
            world(at_location("lear", "the_heath")),
            observe("lear", at_location("lear", "the_heath"), 17),
            observe("fool", at_location("fool", "the_heath"), 17),
            observe("kent", at_location("kent", "the_heath"), 17),
        ),
    ),

    # --- Act III: the storm, the hovel, the mock trial, the blinding ---

    Event(
        id="E_storm_on_heath",
        type="onset_of_madness",
        τ_s=18, τ_a=29,
        participants={"who": "lear"},
        effects=(
            # The storm breaks. Lear rages against the elements. The
            # onset of his madness is authored at this event — world-
            # level mad(lear) begins. The substrate holds this
            # continuously until E_lear_cordelia_reconcile partially
            # lifts it; complete dissipation does not occur (Lear
            # dies mad-with-grief, not clinically lucid).
            world(mad("lear")),
            observe("lear", mad("lear"), 18,
                    note="Lear is partially aware of his own mental state "
                         "— 'O! let me not be mad, not mad, sweet heaven!'"),
            observe("kent", mad("lear"), 18),
            observe("fool", mad("lear"), 18),
        ),
    ),

    Event(
        id="E_edgar_becomes_poor_tom",
        type="disguise_adoption",
        τ_s=19, τ_a=30,
        participants={"who": "edgar"},
        effects=(
            # Edgar takes on the "Poor Tom o' Bedlam" disguise —
            # a naked, gibbering mad beggar. World-level: Edgar is
            # disguised. Edgar knows; no one else does. The disguise
            # is adopted on the heath and persists until
            # E_edgar_challenges_edmund.
            world(disguised_as("edgar", "poor_tom")),
            observe("edgar", disguised_as("edgar", "poor_tom"), 19),
            observe("edgar", at_location("edgar", "the_heath"), 19),
        ),
    ),

    Event(
        id="E_gloucester_meets_poor_tom",
        type="encounter",
        τ_s=20, τ_a=31,
        participants={"host": "gloucester",
                      "tom": "edgar",
                      "guests": ("lear", "kent", "fool")},
        effects=(
            # Gloucester brings the party from the heath into the hovel
            # and then into a farmhouse. Edgar-as-Poor-Tom is present;
            # Gloucester does not recognize his son (the OQ-AP15-adjacent
            # "absent recognition" shape: Edgar is structurally present
            # but identity-absent to the father). Lear and Kent also
            # do not penetrate the disguise.
            #
            # The scene carries heavy authorial irony; Session 3's
            # DESCRIPTIONS will structure the reader-projection. For
            # Session 1 the load-bearing fact is that Gloucester,
            # Lear, Kent, and the Fool all observe "Poor Tom" without
            # observing Edgar.
            world(at_location("gloucester", "hovel")),
            world(at_location("lear", "hovel")),
            observe("gloucester", disguised_as("edgar", "poor_tom"), 20,
                    slot=Slot.BELIEVED, confidence=Confidence.OPEN,
                    note="Gloucester sees the figure but does not connect "
                         "him to his son — confidence=OPEN marks the "
                         "failure-of-recognition structurally"),
            # Author-only observation that Edgar recognizes his father.
            # Held as KNOWN by Edgar with an anguish-register that
            # descriptions will carry.
            observe("edgar", at_location("gloucester", "hovel"), 20,
                    note="Edgar recognizes his father and can say nothing"),
        ),
    ),

    Event(
        id="E_lear_mock_trial",
        type="mad_scene",
        τ_s=21, τ_a=32,
        participants={"judge": "lear",
                      "jurors": ("kent", "fool", "edgar")},
        effects=(
            # Lear arraigns Goneril and Regan on joint-stools in
            # absentia. The Fool, Edgar-as-Poor-Tom, and Kent-as-Caius
            # serve as the court. Mad register; no world effects of
            # consequence. Session 3's DESCRIPTIONS will carry the
            # symbolic load.
            #
            # This is the Fool's last scene in the Folio; he disappears
            # after this event (his "And my poor fool is hang'd" line
            # near the end of the play is structurally unresolved as
            # to referent — the Fool, or Cordelia). Session 1 respects
            # the authorial reticence: no E_fool_dies event.
            observe("kent", mad("lear"), 21),
            observe("fool", mad("lear"), 21),
            observe("edgar", mad("lear"), 21),
        ),
    ),

    Event(
        id="E_gloucester_sends_lear_to_dover",
        type="loyal_act",
        τ_s=22, τ_a=33,
        participants={"loyal": "gloucester", "beneficiary": "lear"},
        effects=(
            # Gloucester, having learned that Cordelia has returned
            # with a French force at Dover, arranges for Lear to be
            # conveyed there. Cornwall and Regan learn of this through
            # Edmund's betrayal of his father — Edmund, having seen a
            # letter that Gloucester confided to him, turns it over to
            # Cornwall. This event fires two knowledge effects:
            # Gloucester informs Kent-as-Caius of the Dover plan, and
            # Edmund secretly observes Gloucester's movements.
            observe("kent", at_location("cordelia", "dover"), 22,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Gloucester's tip — Cordelia has landed with "
                         "the French army"),
            # Edmund sees; this is the hinge of his second instrumental
            # act (betraying his father to Cornwall). The betrayal's
            # effects land at E_cornwall_regan_blind_gloucester.
            observe("edmund", at_location("cordelia", "dover"), 22,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Edmund observes his father's loyalty and "
                         "resolves to betray him a second time — "
                         "the instrumental chain expands from the "
                         "forgery-on-Edgar to the informer-on-"
                         "Gloucester"),
        ),
    ),

    Event(
        id="E_cornwall_regan_blind_gloucester",
        type="atrocity",
        τ_s=23, τ_a=34,
        participants={"perpetrators": ("cornwall", "regan"),
                      "victim": "gloucester"},
        effects=(
            # Cornwall and Regan, learning (via Edmund's betrayal)
            # that Gloucester has helped Lear escape to Dover, bind
            # him to a chair and pluck out his eyes. Cornwall puts
            # out the first eye ("Out, vile jelly!"); Regan urges
            # him to pluck the other. A servant intervenes, fatally
            # wounding Cornwall, and is killed by Regan in return.
            # Gloucester is then turned out onto the heath.
            #
            # Structural peripeteia for the Gloucester subplot:
            # the outward blinding mirrors the inward blindness that
            # allowed Edmund's forgery to succeed. Session 2's
            # Aristotelian overlay will author this as Gloucester's
            # anagnorisis-event; his recognition that he was wrong
            # about Edgar comes here, as Regan reveals that it was
            # Edmund who betrayed him.
            world(ordered_killing("cornwall", "gloucester")),
            world(blinded("gloucester")),
            observe("gloucester", blinded("gloucester"), 23),
            # Cornwall is mortally wounded by the servant. The servant
            # is not authored as an entity; Cornwall's wound is
            # attributed to an "unnamed_servant" string token in the
            # killed predicate — but since no rule fires on this, the
            # substrate records it as a world-level killed prop with
            # the servant's name as a string. Minimal scope.
            world(killed("unnamed_servant", "cornwall")),
            # Regan reveals to Gloucester that it was Edmund who
            # betrayed him. Gloucester's anagnorisis.
            told_by("gloucester", "regan",
                    plots_against("edmund", "gloucester"),
                    23, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Gloucester's anagnorisis: he was wrong about "
                         "Edgar; it was Edmund who betrayed him. The "
                         "forgery-instrument's deception is undone in "
                         "the same scene as his physical blinding."),
            # Gloucester's new belief about Edgar: that he was wronged.
            told_by("gloucester", "regan", plots_against("edgar", "gloucester"),
                    23, slot=Slot.BELIEVED, confidence=Confidence.SUSPECTED,
                    note="Gloucester now doubts what he was so certain of "
                         "at E_edmund_shows_gloucester — confidence "
                         "retracts from BELIEVED to SUSPECTED; Session 3 "
                         "may refine to a full retraction effect."),
            world(dead("cornwall")),  # Cornwall's wound is mortal; death follows
                                      # swiftly. Authored here rather than as a
                                      # separate event per Session-1 compression.
        ),
    ),

    # --- Act IV: Dover, Cordelia's return, reconciliation ---

    Event(
        id="E_edgar_leads_blind_gloucester",
        type="loyal_act_incognito",
        τ_s=24, τ_a=35,
        participants={"guide": "edgar", "led": "gloucester"},
        effects=(
            # Edgar, still disguised as Poor Tom, finds his blinded
            # father wandering on the heath and leads him toward
            # Dover. Gloucester asks to be led to the cliff to throw
            # himself off; Edgar resolves to save him with a therapeutic
            # deception — the same instrument-shape Edmund used
            # maliciously, now wielded with opposite polarity.
            #
            # Substrate records: Edgar and Gloucester are together;
            # Gloucester does not recognize his guide. This is a
            # continuing non-recognition, not a new one.
            world(at_location("gloucester", "dover")),
            world(at_location("edgar", "dover")),
            observe("gloucester", at_location("gloucester", "dover"), 24,
                    note="Gloucester is led blind; his trust in the guide "
                         "is total and tragic"),
        ),
    ),

    Event(
        id="E_gloucester_suicide_attempt",
        type="instrument_therapy",
        τ_s=25, τ_a=36,
        participants={"staging_agent": "edgar",
                      "beneficiary": "gloucester"},
        effects=(
            # At Dover, Edgar stages the cliff fall. Gloucester believes
            # he jumps from a great height; in world-fact he falls flat
            # onto the ground. Edgar then re-addresses him in a
            # different voice, claims he has miraculously survived, and
            # encourages him to "bear free and patient thoughts."
            # Gloucester's despair abates; he accepts continued life.
            #
            # OQ-AP14 polarity: the same instrument-shape Edmund used
            # to catastrophic effect (forged letter, staged wound)
            # Edgar uses to therapeutic effect (staged cliff fall). The
            # Aristotelian overlay's instrumental-kind A13 relation
            # must accommodate both polarities.
            world(staged_cliff_fall("edgar", "dover")),
            observe("edgar", staged_cliff_fall("edgar", "dover"), 25),
            # Gloucester believes he has fallen and survived; in
            # world-fact neither event happened as believed. The
            # substrate marks this parallel to Edmund's staged_wound
            # belief structure.
            told_by("gloucester", "edgar",
                    Prop("fell_from_cliff", ("gloucester", "dover")),
                    25, slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="Gloucester believes he jumped and lived — the "
                         "therapeutic instrument's payload"),
        ),
    ),

    Event(
        id="E_cordelia_returns",
        type="military_return",
        τ_s=26, τ_a=37,
        participants={"returning": "cordelia",
                      "with_army": "france"},
        effects=(
            # Cordelia lands at Dover with a French force (in the
            # Folio, commanded by her officers rather than her
            # husband France, who has returned to France on state
            # business; the encoding compresses to "Cordelia returns
            # with an army"). She searches for her father.
            world(at_location("cordelia", "dover")),
            observe("cordelia", at_location("cordelia", "dover"), 26),
        ),
    ),

    Event(
        id="E_lear_meets_blind_gloucester",
        type="encounter",
        τ_s=27, τ_a=38,
        participants={"mad_king": "lear", "blind_earl": "gloucester"},
        effects=(
            # Lear, in full madness and crowned with weeds, meets
            # blind Gloucester on the heath near Dover. The scene's
            # emotional register is one of the play's peaks; its
            # structural significance is that both broken men
            # confront each other's broken-ness.
            observe("lear", at_location("gloucester", "dover"), 27),
            observe("gloucester", at_location("lear", "dover"), 27,
                    note="Gloucester recognizes Lear by voice — 'the "
                         "trick of that voice I do well remember'"),
        ),
    ),

    Event(
        id="E_lear_cordelia_reconcile",
        type="reconciliation",
        τ_s=28, τ_a=39,
        participants={"father": "lear", "daughter": "cordelia"},
        effects=(
            # Cordelia's people find Lear; she watches over him as he
            # sleeps; he wakes to her. "I am a very foolish fond old
            # man... Do not laugh at me; for, as I am a man, I think
            # this lady to be my child Cordelia."
            #
            # Lear's anagnorisis (main plot). His earlier BELIEVED
            # held-fact that Cordelia did not love him is retracted;
            # he now KNOWS she does. The substrate's Session 3 SJUZHET
            # will structure this reconciliation as the main-plot
            # anagnorisis event.
            remove_held("lear", plots_against("cordelia", "lear"),
                        Slot.BELIEVED, Confidence.BELIEVED, 28,
                        note="Lear's false belief from E_love_test_cordelia "
                             "is retracted — the play's largest individual "
                             "held-fact retraction"),
            # Partial dissipation of madness — Lear is lucid enough
            # to recognize his daughter, though the substrate does
            # not retract mad(lear) entirely (he will be mad-with-
            # grief again at the final scene).
            observe("lear", at_location("cordelia", "dover"), 28,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Lear's anagnorisis — he recognizes Cordelia"),
        ),
    ),

    # --- Act V: battle, duel, cluster of deaths, final catastrophe ---

    Event(
        id="E_battle",
        type="battle",
        τ_s=29, τ_a=40,
        participants={"victor_side": ("edmund", "goneril", "regan", "albany"),
                      "defeated_side": ("cordelia", "lear")},
        effects=(
            # The British forces (nominally under Albany, effectively
            # under Edmund) defeat the French. Lear and Cordelia are
            # captured. The battle itself happens offstage in the
            # play; Edgar returns from the battlefield having fought
            # valiantly for the French.
            world(at_location("lear", "british_camp")),
            world(at_location("cordelia", "british_camp")),
        ),
    ),

    Event(
        id="E_lear_cordelia_captured",
        type="capture",
        τ_s=30, τ_a=41,
        participants={"captives": ("lear", "cordelia"),
                      "captors": ("edmund",)},
        effects=(
            # Lear and Cordelia are taken under guard to prison. Lear
            # is serene: "We two alone will sing like birds i' the
            # cage." The substrate compresses the capture and the
            # movement to prison into one event.
            world(at_location("lear", "prison")),
            world(at_location("cordelia", "prison")),
            observe("lear", at_location("cordelia", "prison"), 30,
                    note="Lear is content to be imprisoned with Cordelia"),
        ),
    ),

    Event(
        id="E_edmund_orders_cordelia_hanged",
        type="ordered_killing",
        τ_s=31, τ_a=42,
        participants={"orderer": "edmund", "victim": "cordelia"},
        effects=(
            # Edmund gives a captain written instructions to hang
            # Cordelia and make it look like suicide. The order is
            # world-true at this τ_s; its execution is later
            # (E_cordelia_hanged). Edmund conceals this from Albany
            # and Regan; Goneril is complicit.
            world(ordered_killing("edmund", "cordelia")),
            observe("edmund", ordered_killing("edmund", "cordelia"), 31),
            # Goneril knows of the plan (she has been conspiring with
            # Edmund against her husband Albany and against the
            # prisoners).
            observe("goneril", ordered_killing("edmund", "cordelia"), 31),
        ),
    ),

    Event(
        id="E_edgar_defeats_edmund",
        type="trial_by_combat",
        τ_s=32, τ_a=43,
        participants={"challenger": "edgar",
                      "defendant": "edmund"},
        effects=(
            # Albany, having been shown Goneril's intercepted letter
            # plotting Edmund's elevation and Albany's death, summons
            # a trial by combat. An anonymous challenger (Edgar, still
            # in disguise) appears and fights Edmund. Edgar mortally
            # wounds Edmund. The FRATRICIDE rule fires here —
            # killed(edgar, edmund) ∧ brother_of(edgar, edmund) ⇒
            # fratricide(edgar, edmund). Edgar joins the corpus's
            # small set of kin-killers, though his act is sanctioned
            # (trial by combat) rather than murderous.
            world(killed("edgar", "edmund")),
            # Note: world(dead("edmund")) is NOT asserted here — Edmund
            # lingers long enough to confess and attempt to save
            # Cordelia. The dead prop lands at E_edmund_dies.
            observe("edgar", killed("edgar", "edmund"), 32),
            observe("albany", killed("edgar", "edmund"), 32),
        ),
    ),

    Event(
        id="E_regan_dies",
        type="collateral_death",
        τ_s=33, τ_a=44,
        participants={"victim": "regan", "agent": "goneril"},
        effects=(
            # Regan has been poisoned (earlier in the action, offstage,
            # by Goneril) out of jealousy over Edmund. She collapses
            # and dies during or immediately after the trial by combat
            # scene. The substrate compresses the poisoning and its
            # effect into this single event — the poisoning itself is
            # not given its own event in Session 1; Session 3 may
            # expand it if forcing.
            world(poisoned("regan")),
            world(killed("goneril", "regan")),
            world(dead("regan")),
            observe("albany", dead("regan"), 33),
            observe("goneril", killed("goneril", "regan"), 33,
                    note="Goneril, cornered, will not deny her deed"),
        ),
    ),

    Event(
        id="E_goneril_suicide",
        type="offstage_death",
        τ_s=34, τ_a=45,
        participants={"victim": "goneril"},
        effects=(
            # Goneril, her plot exposed by the intercepted letter,
            # flees the scene and kills herself offstage. Her death
            # is reported by a Gentleman. World-level: suicide(goneril)
            # and dead(goneril).
            world(suicide("goneril")),
            world(dead("goneril")),
            observe("albany", dead("goneril"), 34,
                    note="reported by a Gentleman; Goneril's body is "
                         "brought out; the offstage nature of her death "
                         "contributes to OQ-AP15's forcing surface"),
        ),
    ),

    Event(
        id="E_edmund_confesses",
        type="deathbed_reversal",
        τ_s=35, τ_a=46,
        participants={"confessor": "edmund"},
        effects=(
            # Dying, Edmund repents: "Some good I mean to do, despite
            # of mine own nature." He reveals the order against
            # Cordelia, hoping to save her. Albany dispatches Edgar
            # and an officer to rescind the order, but the substrate
            # subsequently records that the rescue arrives too late.
            #
            # Edmund's confession is a second-site anagnorisis event
            # structurally analogous to Laertes's deathbed reveal in
            # Hamlet (A14 staging-step territory, though Lear does
            # not have a sketched A11 chain in Session 1). Session 2
            # will structure this in the Aristotelian overlay.
            observe("albany", ordered_killing("edmund", "cordelia"), 35,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
            observe("edgar", ordered_killing("edmund", "cordelia"), 35),
            # Public revelation: now everyone present at the scene
            # knows of the hanging order, though its execution cannot
            # be reversed in time.
        ),
    ),

    Event(
        id="E_cordelia_hanged",
        type="offstage_death",
        τ_s=36, τ_a=47,
        participants={"victim": "cordelia", "orderer": "edmund"},
        effects=(
            # Cordelia is hanged in prison per Edmund's earlier order.
            # The event occurs offstage; the audience and characters
            # learn of it through Lear's entrance carrying her body.
            # World-level: hanged and dead. No observers among the
            # principal cast (the captain executes, Lear presumably
            # prevented or asleep at the moment). The empty
            # observer-set is the defining shape OQ-AP15 pressures.
            world(hanged("cordelia")),
            world(dead("cordelia")),
            # Deliberately: no observe() calls on this event. The
            # catharsis lands through Lear's discovery at
            # E_lear_enters_with_cordelia below.
        ),
    ),

    Event(
        id="E_gloucester_dies",
        type="offstage_death",
        τ_s=36, τ_a=48,
        participants={"victim": "gloucester"},
        effects=(
            # Gloucester, having been reunited with Edgar immediately
            # after the trial-by-combat (offstage in the Folio),
            # dies of "joy-shock" — his heart "'twixt two extremes of
            # passion, joy and grief, / Burst smilingly." Edgar reports
            # this at the final scene. World-level: dead(gloucester).
            # The offstage reveal (by Edgar) is another OQ-AP15-
            # pressure surface.
            world(dead("gloucester")),
            observe("edgar", dead("gloucester"), 36,
                    note="Edgar reveals himself to his father before "
                         "the final scene; Gloucester dies in Edgar's "
                         "arms. The reveal-and-death happens offstage "
                         "and is reported retrospectively."),
        ),
    ),

    Event(
        id="E_lear_enters_with_cordelia",
        type="catharsis_reveal",
        τ_s=37, τ_a=49,
        participants={"bearer": "lear", "borne": "cordelia"},
        effects=(
            # Lear enters carrying Cordelia's body. "Howl, howl, howl,
            # howl! O you are men of stones!" The catharsis of the
            # entire play lands on this moment — a dead daughter
            # borne by a dying father. The substrate records that
            # every named surviving character observes this; their
            # observation of dead(cordelia) is the OQ-AP15-shaped
            # absent-event-catharsis structure.
            #
            # World-level: dead(cordelia) has already been asserted at
            # E_cordelia_hanged; this event records the observation
            # wave.
            observe("lear", dead("cordelia"), 37,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="Lear's grief-knowledge: 'she's gone for ever'"),
            observe("albany", dead("cordelia"), 37),
            observe("edgar", dead("cordelia"), 37),
            observe("kent", dead("cordelia"), 37),
        ),
    ),

    Event(
        id="E_lear_dies",
        type="death_of_grief",
        τ_s=38, τ_a=50,
        participants={"who": "lear"},
        effects=(
            # Lear, still gazing at Cordelia's lips for breath, dies.
            # "Look, her lips, look there, look there!" The substrate
            # leaves ambiguous whether he dies believing she lives
            # (a last-minute held-fact flicker) or knowing she does
            # not — the Folio and Q1 differ. Session 3's DESCRIPTIONS
            # will carry the textual-uncertainty question.
            #
            # World-level: dead(lear). Not killed by any agent — the
            # catalogue of deaths in Lear is rich and distinct:
            #   killed(edgar, edmund)            — trial by combat
            #   killed(goneril, regan)           — poisoning
            #   killed(unnamed_servant, cornwall) — servant's intervention
            #   suicide(goneril)                 — self-inflicted
            #   hanged(cordelia)                 — offstage execution
            #   dead(gloucester)                 — joy-shock, no agent
            #   dead(lear)                       — grief, no agent
            world(dead("lear")),
            observe("edgar", dead("lear"), 38),
            observe("kent", dead("lear"), 38,
                    note="'Vex not his ghost: O! let him pass; he hates "
                         "him / That would upon the rack of this tough "
                         "world / Stretch him out longer.'"),
            observe("albany", dead("lear"), 38),
        ),
    ),

    Event(
        id="E_edmund_dies",
        type="death_from_wound",
        τ_s=38, τ_a=51,
        participants={"who": "edmund"},
        effects=(
            # Edmund dies of the wound Edgar inflicted at
            # E_edgar_defeats_edmund. The substrate records this as
            # a separate event at the same τ_s as Lear's death,
            # reflecting the Folio's compressed final cluster.
            world(dead("edmund")),
        ),
    ),
]


# ----------------------------------------------------------------------------
# Preplay disclosures — audience-pre-knowledge.
# ----------------------------------------------------------------------------
#
# Lear's audience comes in with less pre-loading than Hamlet's
# (seven-fact set) or Oedipus's (myth-level front-loading). The
# Jacobean audience knows the general political structure of a
# Britain-with-old-king-and-three-daughters as an opening frame,
# and the Gloucester-family structure is established in Act 1
# Scene 1's opening forty lines before Lear enters (Kent and
# Gloucester chat about the king's favor between Cornwall and
# Albany; Gloucester introduces Edmund as his bastard son). The
# substrate preplay set captures only what the curtain-rise takes
# for granted before the love-test begins.
#
# Notably NOT preplay:
#   - Edmund's intention to displace Edgar — disclosed at τ_s=-5
#     (the soliloquy) + acted on from τ_s=8 forward
#   - Edmund's forgery / the letter — disclosed at τ_s=8
#   - Edgar's eventual disguise — disclosed at τ_s=19
#   - Kent's eventual disguise — disclosed at τ_s=13 (E_kent_returns_
#     disguised)
#   - The hanging order — disclosed at τ_s=31
#   - Cordelia's love-in-silence stance — disclosed at τ_s=3
#     through her "Nothing, my lord"
#
# These are the play's epistemic payoff. Keeping them off the
# preplay set is load-bearing for OQ-AP14 (the audience learns
# Edmund's instruments as they deploy, not before) and OQ-AP15
# (the audience's grief for Cordelia depends on seeing her love
# develop across the play, not on pre-knowing it).

PREPLAY_DISCLOSURES = (
    Disclosure(prop=king("lear", "britain"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=parent_of("lear", "goneril"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=parent_of("lear", "regan"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=parent_of("lear", "cordelia"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=earl_of("gloucester", "britain"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=illegitimate("edmund"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
)


# ----------------------------------------------------------------------------
# Sjuzhet — largely linear; τ_d ≈ τ_s for in-play events.
# ----------------------------------------------------------------------------
#
# The three pre-play events (E_lear_reigns, E_gloucester_family,
# E_edmund_resolves_to_plot) are NOT sjuzhet entries — the first
# two are standing facts that never appear as staged scenes, and
# E_edmund_resolves_to_plot is an internal-resolve event whose
# content the audience learns through Edmund's opening soliloquy
# at Act 1 Scene 2, reader-time-bundled with the letter-forging
# beat. The pre-play events' content enters the reader projection
# through PREPLAY_DISCLOSURES at τ_d=0 (the love-test's opening)
# and through later revelatory events.
#
# Focalization distribution (42 entries):
#   lear:        17 entries (his plot — the largest focalizer share)
#   None:         7 entries (public court / ceremonial / offstage —
#                            the kingdom-divided decree, the battle,
#                            the trial-by-combat, Regan's collapse,
#                            Goneril's suicide report, Cordelia's
#                            offstage hanging, Edmund's final death)
#   edmund:       6 entries (soliloquy-derived forgery chain + order
#                            + deathbed confession — triple-Edmund
#                            focalization at τ_d=8-11 is structurally
#                            unusual)
#   edgar:        4 entries (flight, disguise adoption, guide,
#                            Gloucester-reports final-death beat)
#   gloucester:   4 entries (hovel encounter, Dover-tip, blinding
#                            anagnorisis, Dover acceptance)
#   cordelia:     2 entries (her French-marriage beat + her return)
#   kent:         2 entries (banishment + disguise adoption)
#
# Unlike Hamlet (hamlet-dominant focalization with 12-entry share),
# Lear distributes focalization across the double-plot's load-
# bearing characters. The 17-entry Lear share still dominates but
# the 6/5/5 shares for Gloucester/Edgar/Edmund reflect the subplot's
# structural weight. This distribution is itself a reading of
# OQ_LEAR_2 (double-plot unity): focalization-distribution at
# sjuzhet scope is the substrate's answer to the question the
# mythos's asserts_unity_of_action=False opens.

SJUZHET = [

    # τ_d=0 — Act 1 Scene 1 opens. The love-test's announcement.
    # Lear focalizes; the play's register is his from the start.
    # PREPLAY_DISCLOSURES attach here.
    SjuzhetEntry(
        event_id="E_lear_announces_division",
        τ_d=0,
        focalizer_id="lear",
        disclosures=PREPLAY_DISCLOSURES,
    ),

    # τ_d=1 — Goneril's flattering declaration. Lear focalizes —
    # his reading of her speech is the scene's weight.
    SjuzhetEntry(
        event_id="E_love_test_goneril",
        τ_d=1,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=2 — Regan's echo-plus-more. Same focalization.
    SjuzhetEntry(
        event_id="E_love_test_regan",
        τ_d=2,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=3 — Cordelia's 'Nothing, my lord'. The play's first
    # tragic inflection. Lear focalizes — the recognition-of-refusal
    # is HIS, and the substrate's BELIEVED plots_against attaches
    # to his held-set at this beat.
    SjuzhetEntry(
        event_id="E_love_test_cordelia",
        τ_d=3,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=4 — Lear disinherits Cordelia. His act; his focalization.
    SjuzhetEntry(
        event_id="E_cordelia_disinherited",
        τ_d=4,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=5 — Kent's objection and banishment. Kent focalizes — he
    # IS the objector; the 'See better, Lear' is his reading of the
    # scene, and the banishment lands on him.
    SjuzhetEntry(
        event_id="E_kent_banished",
        τ_d=5,
        focalizer_id="kent",
        disclosures=(),
    ),

    # τ_d=6 — France takes Cordelia dowerless. Cordelia focalizes —
    # this is her scene, her choice-against-alternatives moment.
    # 'Fairest Cordelia, that art most rich being poor' is France's
    # voice but Cordelia's narrative.
    SjuzhetEntry(
        event_id="E_france_marries_cordelia",
        τ_d=6,
        focalizer_id="cordelia",
        disclosures=(),
    ),

    # τ_d=7 — Kingdom divided. Formal, ceremonial; omniscient —
    # no single focalizer.
    SjuzhetEntry(
        event_id="E_kingdom_divided",
        τ_d=7,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=8 — Act 1 Scene 2 opens. Edmund's opening soliloquy +
    # letter-forging. Edmund focalizes — the scene is his
    # self-introduction to the audience, via the 'Now, gods, stand
    # up for bastards' soliloquy collapsed into the forgery event.
    SjuzhetEntry(
        event_id="E_edmund_forges_letter",
        τ_d=8,
        focalizer_id="edmund",
        disclosures=(),
    ),

    # τ_d=9 — Gloucester reads the letter. Edmund focalizes — he
    # stages the reveal with feigned reluctance; the scene's
    # rhetorical register is his manipulation of Gloucester's
    # response.
    SjuzhetEntry(
        event_id="E_edmund_shows_gloucester",
        τ_d=9,
        focalizer_id="edmund",
        disclosures=(),
    ),

    # τ_d=10 — Edmund warns Edgar. Edmund continues to focalize
    # this second-branch deployment of the forgery instrument;
    # Edgar is present and acquires his own BELIEVED(plots_against)
    # but the scene is Edmund's con.
    SjuzhetEntry(
        event_id="E_edmund_warns_edgar",
        τ_d=10,
        focalizer_id="edmund",
        disclosures=(),
    ),

    # τ_d=11 — Edmund cuts his own arm. Private to Edmund; a third
    # Edmund-focalized scene in sequence, which is structurally
    # unusual — three consecutive Edmund-soliloquy-equivalent
    # beats. The substrate records this concentration; the reader's
    # immersion in Edmund's plot here is a central shape of the
    # subplot's opening.
    SjuzhetEntry(
        event_id="E_edmund_stages_wound",
        τ_d=11,
        focalizer_id="edmund",
        disclosures=(),
    ),

    # τ_d=12 — Edgar flees. Edgar's first focalized beat; the
    # scene pivots to him.
    SjuzhetEntry(
        event_id="E_edgar_flees",
        τ_d=12,
        focalizer_id="edgar",
        disclosures=(),
    ),

    # τ_d=13 — Act 1 Scenes 3-4 compressed. Lear arrives at
    # Goneril's castle. Lear focalizes — his expectation of the
    # reception he arranged.
    SjuzhetEntry(
        event_id="E_lear_at_gonerils",
        τ_d=13,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=14 — Kent-as-Caius enters Lear's service. Kent focalizes
    # — his own return-under-disguise is a private act of
    # self-loyalty. The audience knows; Lear does not.
    SjuzhetEntry(
        event_id="E_kent_returns_disguised",
        τ_d=14,
        focalizer_id="kent",
        disclosures=(),
    ),

    # τ_d=15 — Goneril demands Lear reduce his knights. Lear
    # focalizes — his first recognition of the reversal starts
    # here ('I did her wrong' at I.v) and culminates in the curse.
    SjuzhetEntry(
        event_id="E_goneril_strips_retinue",
        τ_d=15,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=16 — Lear travels to Regan's.
    SjuzhetEntry(
        event_id="E_lear_to_regans",
        τ_d=16,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=17 — Regan strips Lear further; the two sisters together
    # reduce him to nothing. Lear focalizes — the double-betrayal
    # recognition lands here, and the curse-and-flight that follow
    # are his response.
    SjuzhetEntry(
        event_id="E_regan_also_strips",
        τ_d=17,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=18 — Lear exits into the storm.
    SjuzhetEntry(
        event_id="E_lear_flees_to_heath",
        τ_d=18,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=19 — Act 3 Scene 2. The storm breaks; Lear rages. Lear's
    # 'Blow, winds, and crack your cheeks' and the 'unaccommodated
    # man' recognition at Scene 4 are collapsed here. The
    # 'onset of madness' world-fact attaches at substrate; the
    # focalization is the mad-scene weight as Lear experiences it.
    SjuzhetEntry(
        event_id="E_storm_on_heath",
        τ_d=19,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=20 — Edgar, elsewhere on the heath, adopts the Poor Tom
    # disguise. Edgar focalizes — a private self-transformation.
    SjuzhetEntry(
        event_id="E_edgar_becomes_poor_tom",
        τ_d=20,
        focalizer_id="edgar",
        disclosures=(),
    ),

    # τ_d=21 — The hovel encounter. Multi-presence scene; Gloucester
    # focalizes — his attempt to aid Lear, his non-recognition of
    # the figure who is his son, and his own danger (running this
    # errand against Cornwall's orders) is the scene's structural
    # weight.
    SjuzhetEntry(
        event_id="E_gloucester_meets_poor_tom",
        τ_d=21,
        focalizer_id="gloucester",
        disclosures=(),
    ),

    # τ_d=22 — Act 3 Scene 6. Lear's mock trial. Lear focalizes —
    # the delirium-scene is his alone; the jurors (Kent-as-Caius,
    # Edgar-as-Poor-Tom, Fool) are audiences.
    SjuzhetEntry(
        event_id="E_lear_mock_trial",
        τ_d=22,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=23 — Gloucester helps Lear to Dover. Gloucester focalizes
    # — his loyal-act-against-orders is the scene, and it is
    # Edmund's hinge to betray him.
    SjuzhetEntry(
        event_id="E_gloucester_sends_lear_to_dover",
        τ_d=23,
        focalizer_id="gloucester",
        disclosures=(),
    ),

    # τ_d=24 — The blinding scene. Gloucester focalizes — his
    # peripeteia, his anagnorisis, his physical mutilation. The
    # most extended Gloucester-focalized beat, reflecting A14 chain
    # step AR_STEP_GLOUCESTER_BLINDING's structural weight.
    SjuzhetEntry(
        event_id="E_cornwall_regan_blind_gloucester",
        τ_d=24,
        focalizer_id="gloucester",
        disclosures=(),
    ),

    # τ_d=25 — Edgar leads his blinded father. Edgar focalizes —
    # the therapeutic-instrument chain begins here, and the
    # non-recognition is from Edgar's side anguish rather than
    # Gloucester's confusion.
    SjuzhetEntry(
        event_id="E_edgar_leads_blind_gloucester",
        τ_d=25,
        focalizer_id="edgar",
        disclosures=(),
    ),

    # τ_d=26 — Dover cliff. Gloucester focalizes — the scene's
    # weight is his belief-acceptance. Edgar stages the fall, but
    # the scene's experience is the old man's. 'Thy life's a
    # miracle' reframes it for him; he adopts the reframing.
    SjuzhetEntry(
        event_id="E_gloucester_suicide_attempt",
        τ_d=26,
        focalizer_id="gloucester",
        disclosures=(),
    ),

    # τ_d=27 — Cordelia lands with the French. Her second focalized
    # beat; her agency in the play returns here.
    SjuzhetEntry(
        event_id="E_cordelia_returns",
        τ_d=27,
        focalizer_id="cordelia",
        disclosures=(),
    ),

    # τ_d=28 — The two broken fathers meet on the heath. Lear
    # focalizes — he enters mad and recognizes Gloucester only by
    # voice; the scene's register is his peculiar delirium-register
    # more than Gloucester's despair.
    SjuzhetEntry(
        event_id="E_lear_meets_blind_gloucester",
        τ_d=28,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=29 — The reconciliation. Lear's main anagnorisis; Lear
    # focalizes. 'I am a very foolish fond old man' is his own
    # voice, and the retraction of the plots_against belief lands
    # here as a held-fact removal on his own state.
    SjuzhetEntry(
        event_id="E_lear_cordelia_reconcile",
        τ_d=29,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=30 — The battle. Offstage in the play; reported.
    # Omniscient.
    SjuzhetEntry(
        event_id="E_battle",
        τ_d=30,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=31 — Lear and Cordelia captured. Lear focalizes — 'we
    # two alone will sing like birds i' the cage' is his serene
    # register.
    SjuzhetEntry(
        event_id="E_lear_cordelia_captured",
        τ_d=31,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=32 — Edmund orders the hanging. Private order; Edmund
    # focalizes. The audience knows; the rescue possibility opens
    # against the ticking clock.
    SjuzhetEntry(
        event_id="E_edmund_orders_cordelia_hanged",
        τ_d=32,
        focalizer_id="edmund",
        disclosures=(),
    ),

    # τ_d=33 — Trial by combat. Formal, public; omniscient.
    SjuzhetEntry(
        event_id="E_edgar_defeats_edmund",
        τ_d=33,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=34 — Regan collapses and dies from Goneril's poisoning.
    # Public scene; omniscient.
    SjuzhetEntry(
        event_id="E_regan_dies",
        τ_d=34,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=35 — Goneril's suicide. Offstage; reported via Gentleman.
    # Omniscient.
    SjuzhetEntry(
        event_id="E_goneril_suicide",
        τ_d=35,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=36 — Edmund's deathbed confession. Edmund focalizes — his
    # 'some good I mean to do' is his own voice, and the reversal
    # is characterological.
    SjuzhetEntry(
        event_id="E_edmund_confesses",
        τ_d=36,
        focalizer_id="edmund",
        disclosures=(),
    ),

    # τ_d=37 — Cordelia hanged. OFFSTAGE, ZERO OBSERVERS — the
    # OQ-AP15 site. No focalizer (no character is present whose
    # experience the scene inhabits). This is the substrate's
    # cleanest case of an absent-defining-event; the reader learns
    # of the hanging only through the subsequent entrance.
    SjuzhetEntry(
        event_id="E_cordelia_hanged",
        τ_d=37,
        focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=38 — Gloucester's offstage death. Edgar focalizes — he
    # reports the death in his final scene entrance. The reveal-
    # and-death are a single offstage beat (Edgar tells Gloucester
    # who he is; Gloucester's heart bursts smilingly); focalization
    # attaches to the reporter because no one else witnesses.
    SjuzhetEntry(
        event_id="E_gloucester_dies",
        τ_d=38,
        focalizer_id="edgar",
        disclosures=(),
    ),

    # τ_d=39 — Lear enters carrying Cordelia. The catharsis site.
    # Lear focalizes — 'Howl, howl, howl, howl!' is his voice, the
    # pieta-image is his carrying, the entire catharsis rests on
    # his stricken consciousness.
    SjuzhetEntry(
        event_id="E_lear_enters_with_cordelia",
        τ_d=39,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=40 — Lear's death. Lear focalizes — his 'Look, her lips'
    # is the final subjective register, and Kent's epitaph 'Vex not
    # his ghost' comes after. Lear is the focalizer of his own
    # death; Hamlet's was Horatio. Distinct final-beat shape.
    SjuzhetEntry(
        event_id="E_lear_dies",
        τ_d=40,
        focalizer_id="lear",
        disclosures=(),
    ),

    # τ_d=41 — Edmund dies of duel wounds. Offstage or peripheral
    # at this point; omniscient framing.
    SjuzhetEntry(
        event_id="E_edmund_dies",
        τ_d=41,
        focalizer_id=None,
        disclosures=(),
    ),

]


# ----------------------------------------------------------------------------
# Descriptions — the interpretive peer surface.
# ----------------------------------------------------------------------------
#
# τ_a values start at 200 (after fabula τ_a values, which top out
# at 51). Later authoring passes can interleave without renumbering.
#
# Lear's descriptions track three groups:
#   1. Authorial-uncertainty questions the substrate deliberately
#      declines to commit on (Lear's madness register; Cordelia's
#      motivation; the Fool's fate; Edmund's repentance; Lear's
#      final belief). Marked is_question=True; these parallel the
#      Hamlet Ghost-ontology / sanity / Gertrude-foreknowledge /
#      Ophelia-death pattern.
#   2. Structural reader-frames for the forcing-function
#      signatures the dialect layer banks (OQ-AP14 instrumental-
#      kind double-polarity; OQ-AP15 absent-catharsis displacement;
#      OQ-LEAR-1 emotional-vs-epistemic staging; OQ-LEAR-2 double-
#      plot unity). These name reading moves the substrate
#      supports; the Aristotelian overlay's OQ_*_FINDING prose
#      constants carry the dialect-layer finding-prose, and these
#      descriptions carry the substrate-layer reader frames.
#   3. Parallel-tragic-hero reader frames (Lear-Gloucester parallel
#      arcs; Gloucester-blinding-as-symbolic-inversion motif).
#
# Probe-authored edits and answers (like the llm-authored
# supersessions in macbeth.py) are not present in Session 3; they
# would be added by a future probe pass against Lear (Session 5+).

DESCRIPTIONS = [

    Description(
        id="D_lear_madness_register_undecided",
        attached_to=anchor_event("E_storm_on_heath"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Lear's madness is encoded as world(mad('lear')) from "
              "E_storm_on_heath (τ_s=18) onward. Unlike Hamlet's "
              "feigning_madness (agent-level, never promoted to "
              "world-fact), Lear's is asserted at world-level — but "
              "the substrate's commitment is to the onset and to the "
              "non-clinical register, not to a fine-grained reading "
              "of the madness. Lear's 'O! let me not be mad, not "
              "mad, sweet heaven!' names his own partial awareness; "
              "the storm-register's 'unaccommodated man' recognition "
              "is performed-by-a-madman AND philosophically lucid; "
              "the mock-trial's delirium is madness-as-moral-clarity. "
              "The substrate records world(mad(lear)) without "
              "committing to whether this is clinical, "
              "performative-turned-genuine (Hamlet-inflected), grief-"
              "induced, or strategic. A future branch (e.g., "
              ":b-lear-performs-madness) could author a competing "
              "reading; the default canonical substrate commits to "
              "the world-fact without its interpretation. Contrast "
              "with Ophelia's mad(ophelia) assertion in Hamlet's "
              "Act 4.5, which the substrate there left similarly "
              "register-undetermined."),
        is_question=True,
        authored_by="author",
        τ_a=200,
    ),

    Description(
        id="D_cordelia_motivation_undecided",
        attached_to=anchor_event("E_love_test_cordelia"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Cordelia's 'Nothing, my lord' is substrate-recorded "
              "as her refusal to perform the love-test's rhetorical "
              "terms; what drives the refusal is not. Three readings "
              "the text supports: (a) HONESTY — the test is broken, "
              "love cannot be rhetorically weighed, silence is the "
              "only honest response; (b) PRIDE — Cordelia reads "
              "Goneril and Regan's performance as transgressing a "
              "standard she holds and refuses to participate in the "
              "transgression even at cost; (c) FAITH — Cordelia "
              "trusts her father's underlying knowledge of her love "
              "enough to risk the inheritance on the assumption the "
              "test is not what it appears. The substrate commits to "
              "none of these. Cordelia's later 'I cannot heave my "
              "heart into my mouth' names the inability but not its "
              "source. Authorial reticence preserved; descriptions-"
              "layer question banked for probe-surface resolution."),
        is_question=True,
        authored_by="author",
        τ_a=201,
    ),

    Description(
        id="D_fool_disappearance_undecided",
        attached_to=anchor_event("E_lear_mock_trial"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("The Fool's final authored presence is at "
              "E_lear_mock_trial (τ_s=21). After that, the substrate "
              "does not author any Fool-present events — he simply "
              "vanishes from FABULA. The text's Act 5 Scene 3 line "
              "'And my poor fool is hang'd' has two candidate "
              "referents (the Fool as character; Cordelia as "
              "figure-of-address) and two authorial traditions "
              "(Elizabethan-boy-actor doubling Cordelia and the Fool "
              "argues he is off-stage performing Cordelia during the "
              "French-army scenes; alternative reading has the Fool "
              "killed by Cornwall's forces somewhere between the "
              "hovel and Dover). The substrate declines to commit: "
              "no E_fool_dies event, no world(dead('fool')) "
              "assertion, no observation of his absence by the "
              "remaining characters. The authorial reticence is the "
              "position — the character slips out of the substrate "
              "as he slips out of the text. A future branch could "
              "author either reading; the default canonical "
              "substrate leaves the question open."),
        is_question=True,
        authored_by="author",
        τ_a=202,
    ),

    Description(
        id="D_edmund_deathbed_reversal_undecided",
        attached_to=anchor_event("E_edmund_confesses"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Edmund's 'some good I mean to do, despite of mine "
              "own nature' is substrate-recorded as revelation of "
              "the hanging order and attempt to retract it; what "
              "the reversal MEANS at character-level is not. Three "
              "readings: (a) GENUINE REPENTANCE — near death, Edmund "
              "recognizes his acts as acts and tries to mitigate; "
              "(b) WEAKNESS — mortally wounded, Edmund no longer has "
              "the will to sustain his 'nature' and lets the order "
              "surface; (c) VANITY — Edmund, dying, wants the last "
              "word, and revealing the order accomplishes a final "
              "act of agency. The substrate's A14 chain step "
              "AR_STEP_EDMUND_CONFESSES records the reversal as "
              "structural without committing to its moral content. "
              "Aristotle's tragic-hero shape requires the reversal "
              "to be part of the hamartia-anagnorisis arc; Edmund's "
              "is_tragic_hero=False (per lear_aristotelian.py) "
              "precisely because the reversal stops short of "
              "classical anagnorisis — it is characterological and "
              "partial, not epistemic and complete. Which of (a-c) "
              "drives it is the descriptions-layer question."),
        is_question=True,
        authored_by="author",
        τ_a=203,
    ),

    Description(
        id="D_lear_final_belief_undecided",
        attached_to=anchor_event("E_lear_dies"),
        kind="authorial-uncertainty",
        attention=Attention.STRUCTURAL,
        text=("Lear's final 'Look, her lips, look there, look "
              "there!' names an observation the substrate does not "
              "commit on: does he see breath on Cordelia's lips (a "
              "hallucination or wishful interpretation, given "
              "world(dead('cordelia')) is asserted at τ_s=36) or does "
              "he see their final stillness and die of the "
              "recognition? The Folio and Q1 differ on the stage "
              "direction and the line's delivery. The substrate "
              "records world(dead('lear')) at τ_s=38 with no "
              "knowledge-effect updating Lear's held-set in that "
              "final moment — he dies without the substrate asserting "
              "either retraction or confirmation of the 'lips-"
              "breathing' perception. Authorial reticence preserved: "
              "the character's last subjective state is exactly the "
              "text's last ambiguity. Contrast Hamlet's death-state "
              "where 'the rest is silence' commits to completion of "
              "knowing; Lear's 'look there' leaves it open."),
        is_question=True,
        authored_by="author",
        τ_a=204,
    ),

    Description(
        id="D_instrumental_chain_malicious_vs_therapeutic",
        attached_to=anchor_event("E_gloucester_suicide_attempt"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("OQ-AP14 pressure: Edmund and Edgar both wield "
              "instrument-chains on the same target (Gloucester) "
              "with inverted moral polarity. Edmund's chain: forge a "
              "letter (world(forged_letter)), show it to Gloucester "
              "(Gloucester acquires BELIEVED(plots_against(edgar))), "
              "stage a wound (world(staged_wound), Gloucester's "
              "belief promoted toward KNOWN). Edgar's chain: stage "
              "a cliff fall (world(staged_cliff_fall)), Gloucester "
              "acquires BELIEVED(fell_from_cliff) which the world-"
              "state does not warrant but which the therapeutic "
              "effect DOES depend on. The substrate's shape is "
              "identical: world-level artifact + induced belief + "
              "behavioral-consequence-via-belief. The polarity "
              "inversion is carried at substrate as outcome-polarity "
              "(blinding-and-despair vs acceptance) and at dialect "
              "as the two A13 ArCharacterArcRelation records with "
              "non-canonical kind='instrumental'. The reader-side "
              "reading the substrate supports: deception IS the "
              "instrument-shape regardless of polarity; the kind "
              "'instrumental' names a structural move, not a moral "
              "one; Edgar's therapeutic lie and Edmund's malicious "
              "one use the same machinery. This is the OQ-AP14 "
              "forcing-function ground."),
        authored_by="author",
        τ_a=205,
    ),

    Description(
        id="D_cordelia_absent_catharsis",
        attached_to=anchor_event("E_lear_enters_with_cordelia"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("OQ-AP15 pressure: Cordelia's death is substrate-"
              "authored at E_cordelia_hanged (τ_s=36) with ONLY "
              "world effects and ZERO observer projections — the "
              "first event in the corpus designed with an empty "
              "observer set at the defining event. The catharsis "
              "substrate-displaces to E_lear_enters_with_cordelia "
              "(τ_s=37), where Lear and every named surviving "
              "character observe dead(cordelia) for the first time. "
              "Reader-side: the grief-at-the-hanging is NOT the "
              "grief-at-the-recognition; the pathos builds entirely "
              "on the reveal event's observer-wave, amplified by the "
              "preceding rescue-attempt-too-late setup (E_edmund_"
              "confesses's reveal + the Albany/Edgar dispatches) "
              "that makes the audience foreknow the hanging they "
              "never see. The dialect's catharsis-record attaches "
              "to the mythos as aims_at_catharsis=True and to the "
              "ArCharacter (is_tragic_hero=True) without naming the "
              "displacement. Substrate carries the displacement via "
              "the empty-observer-set at the death event + the "
              "observer-dense reveal event. Reader frame for "
              "probe-side rendering: when computing reader's held-"
              "state at τ_s=37, the substrate's observer projections "
              "at the entrance event should be read as the "
              "catharsis-wave the dialect-level record implies but "
              "does not name."),
        authored_by="author",
        τ_a=206,
    ),

    Description(
        id="D_lear_emotional_staging_substrate_signature",
        attached_to=anchor_event("E_lear_cordelia_reconcile"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("OQ-LEAR-1 pressure: Lear's main anagnorisis at "
              "E_lear_cordelia_reconcile retracts his held "
              "BELIEVED(plots_against(cordelia, lear)) via a "
              "substrate-level remove_held effect, without any prior "
              "informational acquisition. Hamlet's staging steps "
              "(Ghost's factual revelation + Mousetrap's empirical "
              "verification) produce the anagnorisis via belief-"
              "promotion on new information; Lear's reconciliation "
              "produces it via belief-retraction under affective "
              "pressure. The substrate's remove_held effect is the "
              "structural marker — a BELIEVED held-fact is "
              "extinguished, not promoted to KNOWN — and there is "
              "no corresponding add-of-new-information event in "
              "Lear's trajectory toward the reconciliation; Cordelia "
              "does not TELL Lear anything he didn't already have "
              "cognitive access to; her presence and her forgiveness "
              "do the work. The chain steps the dialect admits for "
              "same-character main-anagnorisis (staging) presuppose "
              "the Hamlet shape; Lear's substrate trajectory "
              "(storm's unaccommodated-man realization, mock-trial's "
              "grievance-working-through, heath-meeting-with-"
              "Gloucester's mirror-recognition) consists of "
              "affective waypoints with no new-information content. "
              "This substrate signature — `remove_held` at anagnorisis "
              "without antecedent `observe` or `told_by` of the "
              "retracted proposition's negation — is OQ-LEAR-1's "
              "forcing ground."),
        authored_by="author",
        τ_a=207,
    ),

    Description(
        id="D_double_plot_structural_unity",
        attached_to=anchor_event("E_lear_meets_blind_gloucester"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("OQ-LEAR-2 pressure: the Lear plot and the Gloucester "
              "subplot run as structurally-parallel arcs with only "
              "partial causal convergence. Main-plot beats (love-"
              "test → disinheritance → humiliation → storm → "
              "reconciliation → battle → death) structurally mirror "
              "subplot beats (forgery → disinheritance → flight → "
              "Dover-therapeutic → reunion → duel → death), with "
              "both fathers undergoing peripeteia-by-own-action + "
              "anagnorisis + death. Causal convergence happens at "
              "three loci: (1) Gloucester's Dover-tip gets him "
              "betrayed by Edmund (τ_s=22-23); (2) Gloucester meets "
              "blind-Lear on the heath (τ_s=27, this event); (3) "
              "the battle and its consequences collapse all strands "
              "together (τ_s=29+). Between those three loci the "
              "two plots are structurally independent. The substrate "
              "carries the thematic unity via parallel-event-shape "
              "(both fathers' peripeteiai at τ_s=14 and τ_s=23; both "
              "anagnorises via recognition-of-wronged-child at "
              "τ_s=23 and τ_s=28; both deaths at τ_s=36 and τ_s=38). "
              "The dialect carries it via A13 ArCharacterArcRelation "
              "kind='parallel' (AR_LEAR_GLOUCESTER_PARALLEL). Unity "
              "of action is NOT asserted at mythos scope — the "
              "first corpus encoding to set asserts_unity_of_action="
              "False — but the substrate's event-parallelism is the "
              "evidence the overlay's non-assertion points at."),
        authored_by="author",
        τ_a=208,
    ),

    Description(
        id="D_gloucester_blinding_symbolic_inversion",
        attached_to=anchor_event("E_cornwall_regan_blind_gloucester"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("Gloucester's outward blinding at Cornwall's hands is "
              "the substrate marker for his inward anagnorisis "
              "(Regan reveals Edmund's betrayal in the same scene, "
              "authored as a told_by effect promoting Gloucester's "
              "held-state to KNOWN). The play's famous inversion — "
              "Gloucester sees more blind than he saw sighted — is "
              "substrate-supported but not substrate-committed. "
              "World(blinded('gloucester')) records the physical "
              "mutilation; Gloucester's subsequent held-states record "
              "the epistemic promotion. The inversion-as-reading "
              "(physical blindness as enabling-of-insight) lives in "
              "the Dover scenes that follow: Gloucester accepts the "
              "therapeutic Dover fall (Edgar's instrument) and his "
              "final 'bear free and patient thoughts' marks the "
              "acceptance. Contrast Lear's madness (world-fact, "
              "onset at storm) with Gloucester's blindness (world-"
              "fact, onset at Cornwall): both are physical/mental "
              "markers of an inward turning. The substrate records "
              "both as world-level facts; the inversion-reading is "
              "the descriptions-layer claim."),
        authored_by="author",
        τ_a=209,
    ),

    Description(
        id="D_parallel_fathers_reader_frame",
        attached_to=anchor_event("E_lear_enters_with_cordelia"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("Three characters are authored with "
              "is_tragic_hero=True in lear_aristotelian.py: Lear, "
              "Gloucester, and Cordelia. This is the corpus's second "
              "≥3-tragic-heroes encoding (after Hamlet), confirming "
              "that OQ-AP6's closure (via A13 ArCharacterArcRelation) "
              "generalizes. Unlike Hamlet's three heroes (Hamlet / "
              "Claudius / Laertes — protagonist + antagonist + "
              "ally-becomes-pawn), Lear's three are two parallel "
              "fathers and their shared wronged child: the "
              "father-father mirroring (Lear / Gloucester, authored "
              "as parallel relation) and the father-daughter and "
              "father-son redemption arcs (Lear / Cordelia "
              "reconciliation; Gloucester / Edgar reveal-before-"
              "death). Cordelia's tragic-hero status is the most "
              "debatable of the three but is structurally grounded "
              "in the hamartia-anagnorisis shape: her 'Nothing' "
              "catalyzes the peripeteia (Lear's disinheritance "
              "decision); her return catalyzes the anagnorisis (the "
              "reconciliation); her death catalyzes the catharsis "
              "(Lear's entrance with her body). Three distinct "
              "catalyst-beats, hamartia-structured; admits the "
              "tragic-hero status under Aristotle's A4 'a person "
              "who is neither outstandingly good nor outstandingly "
              "bad but whose misfortune comes through an error of "
              "judgment' (Poetics 1453a)."),
        authored_by="author",
        τ_a=210,
    ),

    Description(
        id="D_cumulative_catastrophe_dispersed",
        attached_to=anchor_event("E_lear_dies"),
        kind="reader-frame",
        attention=Attention.STRUCTURAL,
        text=("The catastrophe is dispersed across τ_s=32-38 with "
              "SEVEN deaths of distinct cause-shapes: fratricide-in-"
              "trial-by-combat (Edgar-Edmund, τ_s=32, the FRATRICIDE "
              "rule fires), poison-collateral (Goneril-Regan, "
              "τ_s=33), suicide (Goneril, τ_s=34, offstage), hanging-"
              "by-order (Cordelia, τ_s=36, offstage, empty observer "
              "set), joy-shock (Gloucester, τ_s=36, offstage, single "
              "observer Edgar), grief (Lear, τ_s=38, onstage), and "
              "duel-wounds-delayed (Edmund, τ_s=38, peripheral). "
              "Contrast Hamlet's cluster-pattern (four deaths at "
              "τ_s=17-18, all onstage, four distinct cause-shapes) "
              "and Oedipus's concentrated-at-end pattern (one death "
              "— Jocasta's — with Oedipus's blinding-and-exile "
              "following). Lear's catastrophe is the corpus's most "
              "DISPERSED: four of seven deaths offstage; six τ_s "
              "units span the catastrophe cluster (vs Hamlet's 2). "
              "If OQ-AP1 (ArPathos grounding) opens in a future "
              "sketch, Lear is the forcing case for 'dispersed "
              "offstage pathos' distinct from Hamlet's 'clustered "
              "onstage cluster-pathos' and Oedipus's 'concentrated-"
              "end single-recognition-collapse'. Three distinct "
              "pathos-shapes, three forcing encodings, one banked OQ."),
        authored_by="author",
        τ_a=211,
    ),

]


# ----------------------------------------------------------------------------
# Rules — inference-model-sketch-01 N1–N10
# ----------------------------------------------------------------------------
#
# One compound predicate: fratricide. Lear's thematic registers do not
# reduce to substrate-derivable compounds beyond this — the filial-
# ingratitude theme, Nature-vs-convention, and madness-as-sight all
# live on descriptions (Session 3) and on the Aristotelian overlay
# (Session 2).
#
# Edgar is the corpus's first "sanctioned" kin-killer — killing Edmund
# in trial by combat makes the act structurally lawful in the world
# of the play, even though FRATRICIDE_RULE fires on the shape alone
# (the rule does not carry moral valence; that lives on descriptions).
# Hamlet's Claudius was the corpus's first unambiguous usurper;
# Macbeth's kinslayer rule fires on similar shape-only grounds; Lear's
# fratricide is the first kin-killing whose moral register the rule
# cannot carry. That contrast is substrate-sketch-05 M1 discipline in
# action — the rule gets the shape right; descriptions get the
# register.

FRATRICIDE_RULE = Rule(
    id="R_fratricide_from_killed_and_brother",
    head=Prop("fratricide", ("X", "Y")),
    body=(
        Prop("killed",     ("X", "Y")),
        Prop("brother_of", ("X", "Y")),
    ),
)

RULES = (
    FRATRICIDE_RULE,
)
