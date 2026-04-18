"""
Rocky (1976) — the encoded fabula and sjuzhet.

Story content only. No substrate logic. Fourth substrate after Oedipus,
Macbeth, and Ackroyd. First Timelock encoding in the corpus (per
rocky_dramatica_complete.py — DSP_limit=Timelock, fight scheduled on
the calendar; the clock is the antagonist the training races).

Authored in response to pressure-shape-taxonomy-sketch-01's Rocky
worked case: the sketch predicted Rocky's substrate would be
Timelock-consistent under LT3 (few or no convergence signals) and
named Rocky's substrate authoring as the forcing function for a
future LT3-strong predicate. This encoding supplies the real data.

Encoding choices:

- **Branches: canonical only.** Rocky has no contested testimony, no
  counterfactual branches, no Rashomon-style multiplicity. The scripted
  stunt-narrative Apollo intends is distinct from what actually happens
  in the ring — but both are on the same :canonical branch because
  Apollo's intention is only a held belief, not an alternative branch.

- **Identity placeholders: none.** Rocky is structurally Steadfast:
  he enters the club fight as himself and leaves the Apollo fight as
  himself writ larger. No equivalence classes collapse; no candidate
  identities resolve. "Italian Stallion" is a ring name Apollo reads
  off a list, not a distinct entity the reader or any character
  mistakenly distinguishes from Rocky Balboa. Per LT2 this means zero
  identity-resolution signal in the classifier.

- **Rules: one.** `went_the_distance(X, Y)` derives from
  `fought_rounds(X, Y, 15)` + `standing_at_final_bell(X)`. The
  compound IS load-bearing for the MC's articulated goal — "I just
  want to go the distance" at the night-before-fight scene — and
  authoring it as a rule rather than a direct assertion honors
  inference-model-sketch-01's derivation surface. This produces ONE
  rule-emergence signal under LT2, pushing the classifier toward
  Optionlock 0.33. That is an honest signal: Rocky's arc does build
  to a compound payoff, even though its terminal τ_s is fixed by
  the calendar rather than by the compound's derivation. A future
  LT3-strong predicate that separates "schedule-driven endpoint" from
  "convergence-driven endpoint" would classify this case correctly.

- **Retraction: one.** `scheduled_fight(mac, apollo)` retracts at
  Mac's injury. This is a pre-plot retraction; the main arc's
  endpoint is never retracted. Under LT2's current disjunction the
  classifier counts this as Optionlock signal, but the retraction
  is structurally the *premise* of the arc rather than its
  convergence — the kind of subplot-only convergence LT2 OQ3 names.

- **Compound-predicate choice for Rocky's arc:** only
  `went_the_distance`. No cumulative moral degradation (unlike
  Macbeth's tyrant), no identity resolution (unlike Oedipus's
  anagnorisis), no mystery solution (unlike Ackroyd's killer
  identification). The sparseness of rule-derivable compounds is
  itself Rocky's structural signature — Timelock stories tend to
  converge less, not because they lack meaning, but because their
  meaning lands at a scheduled moment rather than building through
  premise accretion.

- **Focalization:** mostly Rocky. Two exceptions are narrated but not
  focalized through Rocky — Apollo's selection scene (τ_s=-1) and the
  post-fight "ain't gonna be no rematch" beat (τ_s=57). Both are
  moments where what Rocky thinks is not the point.

- **Scope:** covers the arc from Mac's injury (the plot-trigger) to
  "ain't gonna be no rematch" (the closing beat). Twenty-one fabula
  events. Comparable density to oedipus.py's thirteen events for a
  shorter real-time arc (about eight weeks).

Expected classifier output (pressure-shape-taxonomy-sketch-01 LT2):

- retraction: 1 (Mac's scheduled fight retracted)
- identity-resolution: 0
- rule-emergence: 1 (went_the_distance)
- classification: "optionlock" (any signal → optionlock)
- strength: 0.67 (2-of-3 kinds firing)

This is NOT a clean Timelock-consistent signal under LT2 — it is the
exact case LT3 was written weakly to allow: a Timelock-declared arc
whose substrate exhibits mild convergence signals, which under LT5
reports `NEEDS_WORK` (substrate disagreeing with declaration) or
`PARTIAL_MATCH`. The finding is recorded in the Phase 3 README update;
it sharpens LT3's OQ3 (subplot-only convergence) with real data and
strengthens the case for LT3-strong detection (scheduling vocabulary).
"""

from __future__ import annotations

from story_engine.core.substrate import (
    Entity, Prop, Event, EventStatus,
    Branch, BranchKind, CANONICAL, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
    Description, AnchorRef, Attention, anchor_event,
    Rule,
)


# ----------------------------------------------------------------------------
# Entities
# ----------------------------------------------------------------------------

rocky    = Entity(id="rocky",    name="Rocky Balboa",      kind="agent")
apollo   = Entity(id="apollo",   name="Apollo Creed",      kind="agent")
adrian   = Entity(id="adrian",   name="Adrian Pennino",    kind="agent")
paulie   = Entity(id="paulie",   name="Paulie Pennino",    kind="agent")
mickey   = Entity(id="mickey",   name="Mickey Goldmill",   kind="agent")
duke     = Entity(id="duke",     name='Tony "Duke" Evers', kind="agent")
gazzo    = Entity(id="gazzo",    name="Tony Gazzo",        kind="agent")
jergens  = Entity(id="jergens",  name="Miles Jergens",     kind="agent")
mac      = Entity(id="mac",      name="Mac Lee Green",     kind="agent")
spider   = Entity(id="spider_rico", name="Spider Rico",    kind="agent")
bob      = Entity(id="bob",      name="Bob (the dock worker)", kind="agent")

# Locations.
philadelphia  = Entity(id="philadelphia",  name="Philadelphia",        kind="location")
mickey_gym    = Entity(id="mickey_gym",    name="Mighty Mick's gym",   kind="location")
pet_store     = Entity(id="pet_store",     name="the J&M pet store",   kind="location")
rocky_apt     = Entity(id="rocky_apt",     name="Rocky's apartment",   kind="location")
meat_locker   = Entity(id="meat_locker",   name="Shamrock Meats",      kind="location")
ice_rink      = Entity(id="ice_rink",      name="the ice rink",        kind="location")
art_stairs    = Entity(id="art_stairs",    name="the Art Museum stairs", kind="location")
the_arena     = Entity(id="the_arena",     name="the Spectrum arena",  kind="location")
tavern        = Entity(id="tavern",        name="the Lucky Seven tavern", kind="location")

# The fight itself as a referenceable entity — useful for scheduling
# propositions that need a subject-of-schedule.
fight         = Entity(id="fight",         name="the bicentennial title fight",
                       kind="abstract")
mac_fight     = Entity(id="mac_fight",     name="the Mac-vs-Apollo title fight "
                                                "(cancelled)",
                       kind="abstract")

ENTITIES = [
    rocky, apollo, adrian, paulie, mickey, duke, gazzo, jergens,
    mac, spider, bob,
    philadelphia, mickey_gym, pet_store, rocky_apt, meat_locker,
    ice_rink, art_stairs, the_arena, tavern,
    fight, mac_fight,
]

AGENT_IDS = [e.id for e in ENTITIES if e.kind == "agent"]


# ----------------------------------------------------------------------------
# Branches — canonical only
# ----------------------------------------------------------------------------

ALL_BRANCHES = {
    CANONICAL_LABEL: CANONICAL,
}


# ----------------------------------------------------------------------------
# Proposition constructors
# ----------------------------------------------------------------------------

def champion(who: str, title: str) -> Prop:
    return Prop("champion", (who, title))

def injured(who: str) -> Prop:
    return Prop("injured", (who,))

def contender_for(who: str, champ: str) -> Prop:
    return Prop("contender_for", (who, champ))

def scheduled_fight(a: str, b: str) -> Prop:
    """A title bout is on the calendar between a and b."""
    return Prop("scheduled_fight", (a, b))

def trained_by(fighter: str, trainer: str) -> Prop:
    return Prop("trained_by", (fighter, trainer))

def romantic_partnership(a: str, b: str) -> Prop:
    return Prop("romantic_partnership", (a, b))

def fought_rounds(a: str, b: str, n: int) -> Prop:
    return Prop("fought_rounds", (a, b, n))

def standing_at_final_bell(who: str, fight_id: str) -> Prop:
    return Prop("standing_at_final_bell", (who, fight_id))

def won_fight(winner: str, loser: str) -> Prop:
    return Prop("won_fight", (winner, loser))

def went_the_distance(who: str, against: str) -> Prop:
    """Rule-derivable compound: fought 15 rounds AND was still standing at
    the final bell. See WENT_THE_DISTANCE_RULE below."""
    return Prop("went_the_distance", (who, against))

def called_out(speaker: str, listener: str) -> Prop:
    """X called out Y's name (ringside to the crowd)."""
    return Prop("called_out", (speaker, listener))

def refused_rematch(who: str) -> Prop:
    return Prop("refused_rematch", (who,))


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


def world(p: Prop, asserts: bool = True) -> WorldEffect:
    return WorldEffect(prop=p, asserts=asserts)


# ----------------------------------------------------------------------------
# Fabula — all events on :canonical, status=committed
# ----------------------------------------------------------------------------
#
# τ_s scale: approximate days from the opening club fight (τ_s=0). The
# fight itself is at τ_s ≈ 46 (about seven weeks of training), with
# post-fight beats at τ_s ≤ 57. Pre-plot events (Mac's injury, Apollo's
# selection) are at negative τ_s. The scale is ordinal, not metric —
# comparisons are the substrate's semantic surface.

FABULA = [

    # --- Pre-plot (τ_s < 0) — the scheduling premise of the whole arc ---

    Event(
        id="E_apollo_schedules_mac",
        type="scheduling",
        τ_s=-10, τ_a=1,
        participants={"champion": "apollo", "challenger": "mac"},
        effects=(
            world(champion("apollo", "heavyweight")),
            world(scheduled_fight("apollo", "mac")),
            # Apollo knows his next fight is against Mac; Mac knows.
            observe("apollo", scheduled_fight("apollo", "mac"), -10),
            observe("mac", scheduled_fight("apollo", "mac"), -10),
        ),
    ),

    Event(
        id="E_mac_injured",
        type="injury",
        τ_s=-5, τ_a=2,
        participants={"patient": "mac"},
        effects=(
            # Mac breaks his hand in training. The retraction of
            # scheduled_fight(apollo, mac) is the pre-plot pressure that
            # forces the rest of the substrate into existence. Counted
            # by LT2 as one retraction signal (see module docstring).
            world(injured("mac")),
            world(scheduled_fight("apollo", "mac"), asserts=False),
            observe("mac", injured("mac"), -5,
                    note="broken hand in sparring"),
            observe("apollo", injured("mac"), -5,
                    via=Diegetic.UTTERANCE_HEARD.value,
                    note="told by Duke / Jergens"),
            observe("jergens", injured("mac"), -5),
        ),
    ),

    Event(
        id="E_apollo_selects_rocky",
        type="selection",
        τ_s=-1, τ_a=3,
        participants={"selector": "apollo", "selected": "rocky",
                      "promoter": "jergens"},
        effects=(
            # The "Italian Stallion" ring name caught Apollo's eye in
            # the rankings book. The new scheduled fight enters world
            # state; Apollo and Jergens hold it as intended publicity
            # stunt. Rocky does NOT yet know.
            world(scheduled_fight("apollo", "rocky")),
            world(contender_for("rocky", "apollo")),
            observe("apollo", scheduled_fight("apollo", "rocky"), -1,
                    note="the Italian Stallion — he likes the nickname"),
            observe("jergens", scheduled_fight("apollo", "rocky"), -1,
                    note="reluctant; agrees for the storyline"),
        ),
    ),

    # --- Act 1 — Rocky before the offer (τ_s 0-4) ---

    Event(
        id="E_club_fight_spider",
        type="fight",
        τ_s=0, τ_a=4,
        participants={"fighter_a": "rocky", "fighter_b": "spider_rico"},
        effects=(
            # The Resurrection A.C.: forty dollars a round, an illegal
            # headbutt, a scrappy win. Rocky as he is at story open.
            world(Prop("club_win", ("rocky", "spider_rico"))),
            observe("rocky", Prop("club_win", ("rocky", "spider_rico")), 0),
        ),
    ),

    Event(
        id="E_mickey_clears_locker",
        type="confrontation",
        τ_s=1, τ_a=5,
        participants={"speaker": "mickey", "listener": "rocky"},
        effects=(
            # Mickey has reassigned Rocky's locker. "You had the talent
            # to become a good fighter, but you became a leg-breaker for
            # some cheap second-rate loan shark." Rocky learns his own
            # trainer has written him off.
            observe("rocky", Prop("mickey_wrote_me_off", ("mickey",)), 1,
                    via=Diegetic.UTTERANCE_HEARD.value,
                    note="locker cleaned out; stated rejection"),
        ),
    ),

    Event(
        id="E_gazzo_assignment",
        type="assignment",
        τ_s=2, τ_a=6,
        participants={"employer": "gazzo", "employee": "rocky",
                      "target": "bob"},
        effects=(
            # Gazzo sends Rocky to collect — and, implicitly, to break
            # Bob's thumbs. Rocky refuses the escalation. The character
            # beat that Mickey was responding to at the locker.
            observe("rocky", Prop("collection_job", ("rocky", "bob")), 2),
            observe("gazzo", Prop("collection_job", ("rocky", "bob")), 2,
                    note="assigns the job; expects thumbs broken"),
        ),
    ),

    Event(
        id="E_pet_store_courtship",
        type="courtship",
        τ_s=3, τ_a=7,
        participants={"suitor": "rocky", "beloved": "adrian"},
        effects=(
            # Rocky's third or hundredth visit to the pet store to
            # flirt at the counter. Adrian does not visibly respond.
            observe("rocky", Prop("flirted_at", ("rocky", "adrian")), 3,
                    note="the jokes, the persistence"),
        ),
    ),

    # --- Act 1 climax — the offer (τ_s 5-6) ---

    Event(
        id="E_jergens_offers_fight",
        type="offer",
        τ_s=5, τ_a=8,
        participants={"promoter": "jergens", "champion": "apollo",
                      "challenger": "rocky"},
        effects=(
            # Jergens's office. The dollar amount. The photograph on
            # the poster. Rocky agrees before he quite knows why.
            # scheduled_fight was already in world state at τ_s=-1;
            # Rocky only learns it here.
            observe("rocky", scheduled_fight("apollo", "rocky"), 5,
                    via=Diegetic.UTTERANCE_HEARD.value,
                    note="the offer delivered in Jergens's office"),
            observe("rocky", contender_for("rocky", "apollo"), 5),
        ),
    ),

    Event(
        id="E_mickey_offers_to_manage",
        type="offer",
        τ_s=6, τ_a=9,
        participants={"offerer": "mickey", "fighter": "rocky"},
        effects=(
            # Mickey at Rocky's apartment. The scene turns from rejection
            # (the locker) to late arrival (the home). Rocky accepts.
            world(trained_by("rocky", "mickey")),
            observe("rocky", trained_by("rocky", "mickey"), 6,
                    note="the apartment scene; accepts the offer"),
            observe("mickey", trained_by("rocky", "mickey"), 6),
        ),
    ),

    # --- Act 2 — the relationship (τ_s 8-9) ---

    Event(
        id="E_thanksgiving_turkey",
        type="social_disruption",
        τ_s=8, τ_a=10,
        participants={"disruptor": "paulie", "sister": "adrian",
                      "host": "rocky"},
        effects=(
            # Paulie throws the turkey out into the alley. Adrian,
            # coatless, goes to Rocky's apartment. The forced introduction.
            observe("adrian", Prop("at_location", ("adrian", "rocky_apt")), 8,
                    note="brought over by Paulie"),
            observe("rocky", Prop("at_location", ("adrian", "rocky_apt")), 8),
        ),
    ),

    Event(
        id="E_first_kiss",
        type="romantic_commitment",
        τ_s=9, τ_a=11,
        participants={"lover_a": "rocky", "lover_b": "adrian"},
        effects=(
            # After the ice rink date. "I don't like to lose." The
            # relationship begins. This is a romantic commitment, not a
            # world-fact retraction of any prior state.
            world(romantic_partnership("rocky", "adrian")),
            observe("rocky", romantic_partnership("rocky", "adrian"), 9),
            observe("adrian", romantic_partnership("rocky", "adrian"), 9),
        ),
    ),

    # --- Act 2 montage — the training (τ_s 10-25) ---

    Event(
        id="E_training_begins",
        type="training",
        τ_s=10, τ_a=12,
        participants={"fighter": "rocky", "trainer": "mickey"},
        effects=(
            observe("rocky", Prop("training", ("rocky",)), 10,
                    note="meat locker, runs, gym"),
            observe("mickey", Prop("training", ("rocky",)), 10),
        ),
    ),

    Event(
        id="E_meat_locker_session",
        type="training",
        τ_s=15, τ_a=13,
        participants={"fighter": "rocky", "witness": "paulie",
                      "observer": "adrian"},
        effects=(
            # The sides of beef; Adrian watches; Paulie's presence
            # tacitly moves from tavern-friend to camp-witness.
            observe("rocky", Prop("hardened_hands", ("rocky",)), 15),
        ),
    ),

    Event(
        id="E_stairs_run",
        type="training",
        τ_s=25, τ_a=14,
        participants={"fighter": "rocky"},
        effects=(
            # The Art Museum stairs, arms up, the city below. The
            # iconic midpoint: the body is now ready, the question
            # becomes what the man will do inside the ropes.
            observe("rocky", Prop("ready", ("rocky",)), 25,
                    note="the stairs scene; physical readiness peak"),
        ),
    ),

    # --- Night before — the articulated goal (τ_s 45) ---

    Event(
        id="E_night_before_fight",
        type="private_reflection",
        τ_s=45, τ_a=15,
        participants={"fighter": "rocky", "witness": "adrian"},
        effects=(
            # Rocky alone in the ring, late, the arena empty. "I just
            # want to go the distance." The goal is articulated smaller
            # than winning; this is Rocky's Throughline's central line.
            observe("rocky",
                    Prop("articulated_goal", ("rocky", "went_the_distance")),
                    45,
                    note="the empty-ring scene"),
        ),
    ),

    # --- Fight night (τ_s 46-56) ---

    Event(
        id="E_fight_bell",
        type="fight_begins",
        τ_s=46, τ_a=16,
        participants={"fighter_a": "rocky", "fighter_b": "apollo",
                      "location": "the_arena"},
        effects=(
            # Apollo enters as George Washington; the publicity stunt
            # element is at full dress. First bell.
            observe("apollo", Prop("scripted_stunt", ("apollo", "rocky")), 46,
                    note="George Washington costume; dismissive showmanship"),
            observe("rocky", Prop("in_the_ring", ("rocky", "apollo")), 46),
        ),
    ),

    Event(
        id="E_round_one_knockdown",
        type="knockdown",
        τ_s=47, τ_a=17,
        participants={"striker": "apollo", "downed": "rocky"},
        effects=(
            # The first round goes as Apollo planned. Rocky goes down.
            # The scripted-stunt belief holds for Apollo up to this
            # moment.
            observe("rocky", Prop("knocked_down", ("rocky",)), 47),
            observe("apollo", Prop("knocked_down", ("rocky",)), 47,
                    note="on schedule"),
        ),
    ),

    Event(
        id="E_rocky_gets_up",
        type="recovery",
        τ_s=48, τ_a=18,
        participants={"fighter": "rocky"},
        effects=(
            # Rocky rises. The unscripted turn — the moment Apollo's
            # held belief scripted_stunt begins to erode. No world-fact
            # retraction here: Apollo's belief is a held proposition,
            # not a world fact. The erosion is epistemic, not world.
            observe("apollo", Prop("scripted_stunt_holding", ("apollo",)), 48,
                    slot=Slot.SUSPECTED, confidence=Confidence.SUSPECTED,
                    note="the dismissive stance begins to crack; Duke "
                         "said 'ain't gonna be a joke' before the bell"),
            observe("duke", Prop("told_you_so", ("duke", "apollo")), 48),
        ),
    ),

    Event(
        id="E_fight_ends",
        type="fight_ends",
        τ_s=55, τ_a=19,
        participants={"winner": "apollo", "loser": "rocky"},
        effects=(
            # Fifteen rounds. Split decision to Apollo. Rocky is still
            # standing at the final bell. fought_rounds + standing
            # together make went_the_distance derivable (see RULES).
            world(fought_rounds("rocky", "apollo", 15)),
            world(standing_at_final_bell("rocky", "fight")),
            world(won_fight("apollo", "rocky")),
            # Rocky holds his achievement literally; Apollo holds his
            # win literally.
            observe("rocky", fought_rounds("rocky", "apollo", 15), 55),
            observe("rocky", standing_at_final_bell("rocky", "fight"), 55),
            observe("apollo", won_fight("apollo", "rocky"), 55),
            observe("adrian", fought_rounds("rocky", "apollo", 15), 55,
                    note="watching on television / at the arena"),
        ),
    ),

    Event(
        id="E_adrian_called",
        type="utterance",
        τ_s=56, τ_a=20,
        participants={"speaker": "rocky", "listener": "adrian",
                      "location": "the_arena"},
        effects=(
            # The film's final image. Rocky ringside, Adrian through
            # the crowd, the decision almost not mattering. The world
            # fact called_out(rocky, adrian) lands.
            world(called_out("rocky", "adrian")),
            observe("rocky", called_out("rocky", "adrian"), 56),
            observe("adrian", called_out("rocky", "adrian"), 56),
        ),
    ),

    Event(
        id="E_no_rematch",
        type="utterance",
        τ_s=57, τ_a=21,
        participants={"speaker_a": "rocky", "speaker_b": "apollo"},
        effects=(
            # "Ain't gonna be no rematch." / "Don't want one." Both
            # men refuse a rematch — Rocky because the articulated
            # goal has landed and the rest is extension; Apollo because
            # the encounter has changed his attitude without changing
            # his scorecards.
            world(refused_rematch("rocky")),
            world(refused_rematch("apollo")),
            observe("rocky", refused_rematch("rocky"), 57),
            observe("apollo", refused_rematch("apollo"), 57),
        ),
    ),

]


# ----------------------------------------------------------------------------
# Sjuzhet — Rocky is largely told in fabula order
# ----------------------------------------------------------------------------
#
# The film opens on the club fight (τ_s=0) and proceeds sequentially.
# Pre-plot events (Mac's injury, Apollo's selection) are disclosed on
# the movie's own timeline: the Apollo selection scene appears after
# Rocky's introduction scenes, not before. So the audience learns
# about Mac / Apollo's selection around τ_d=6 (after the Rocky
# establishing beats).

SJUZHET = [

    # τ_d=0 — the Spider Rico fight.
    SjuzhetEntry(
        event_id="E_club_fight_spider",
        τ_d=0, focalizer_id="rocky",
        disclosures=(),
    ),

    # τ_d=1 — gym rejection.
    SjuzhetEntry(
        event_id="E_mickey_clears_locker",
        τ_d=1, focalizer_id="rocky",
        disclosures=(),
    ),

    # τ_d=2 — the dock-job refusal.
    SjuzhetEntry(
        event_id="E_gazzo_assignment",
        τ_d=2, focalizer_id="rocky",
        disclosures=(),
    ),

    # τ_d=3 — pet store flirtation.
    SjuzhetEntry(
        event_id="E_pet_store_courtship",
        τ_d=3, focalizer_id="rocky",
        disclosures=(),
    ),

    # τ_d=4 — pre-plot disclosure: the audience learns Apollo had Mac
    # scheduled and Mac broke his hand. The film shows Apollo's office
    # here, not on the true τ_s=-10 / -5 timeline.
    SjuzhetEntry(
        event_id="E_mac_injured",
        τ_d=4, focalizer_id=None,
        disclosures=(
            Disclosure(prop=injured("mac"), slot=Slot.KNOWN,
                       confidence=Confidence.CERTAIN,
                       via=Narrative.DISCLOSURE.value),
            Disclosure(prop=scheduled_fight("apollo", "mac"), slot=Slot.KNOWN,
                       confidence=Confidence.CERTAIN,
                       via=Narrative.DISCLOSURE.value),
        ),
    ),

    # τ_d=5 — Apollo selects Rocky.
    SjuzhetEntry(
        event_id="E_apollo_selects_rocky",
        τ_d=5, focalizer_id=None,
        disclosures=(
            Disclosure(prop=scheduled_fight("apollo", "rocky"),
                       slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                       via=Narrative.DISCLOSURE.value),
        ),
    ),

    # τ_d=6 — Jergens's office offer.
    SjuzhetEntry(
        event_id="E_jergens_offers_fight",
        τ_d=6, focalizer_id="rocky",
        disclosures=(),
    ),

    # τ_d=7 — Mickey at the apartment.
    SjuzhetEntry(
        event_id="E_mickey_offers_to_manage",
        τ_d=7, focalizer_id="rocky",
        disclosures=(),
    ),

    # τ_d=8 — Thanksgiving.
    SjuzhetEntry(
        event_id="E_thanksgiving_turkey",
        τ_d=8, focalizer_id="rocky",
        disclosures=(),
    ),

    # τ_d=9 — the first kiss.
    SjuzhetEntry(
        event_id="E_first_kiss",
        τ_d=9, focalizer_id="rocky",
        disclosures=(),
    ),

    # τ_d=10 — training montage begins.
    SjuzhetEntry(
        event_id="E_training_begins",
        τ_d=10, focalizer_id="rocky",
        disclosures=(),
    ),

    SjuzhetEntry(
        event_id="E_meat_locker_session",
        τ_d=11, focalizer_id="rocky",
        disclosures=(),
    ),

    SjuzhetEntry(
        event_id="E_stairs_run",
        τ_d=12, focalizer_id="rocky",
        disclosures=(),
    ),

    # τ_d=13 — the night before.
    SjuzhetEntry(
        event_id="E_night_before_fight",
        τ_d=13, focalizer_id="rocky",
        disclosures=(),
    ),

    # τ_d=14-17 — the fight.
    SjuzhetEntry(
        event_id="E_fight_bell",
        τ_d=14, focalizer_id=None,
        disclosures=(),
    ),

    SjuzhetEntry(
        event_id="E_round_one_knockdown",
        τ_d=15, focalizer_id=None,
        disclosures=(),
    ),

    SjuzhetEntry(
        event_id="E_rocky_gets_up",
        τ_d=16, focalizer_id="apollo",  # Apollo's attitude cracks
        disclosures=(),
    ),

    SjuzhetEntry(
        event_id="E_fight_ends",
        τ_d=17, focalizer_id=None,
        disclosures=(),
    ),

    # τ_d=18 — "Adrian!"
    SjuzhetEntry(
        event_id="E_adrian_called",
        τ_d=18, focalizer_id="rocky",
        disclosures=(),
    ),

    # τ_d=19 — "ain't gonna be no rematch." Not focalized through
    # Rocky — the scene belongs to both men and to what the film has
    # been arguing. Per focalization-sketch-01 a null focalizer means
    # the omniscient default.
    SjuzhetEntry(
        event_id="E_no_rematch",
        τ_d=19, focalizer_id=None,
        disclosures=(),
    ),

]


# ----------------------------------------------------------------------------
# Descriptions — sparse. Rocky's substrate is clean enough that most
# interpretive load lives in the prose the film itself supplies
# (costume, music, camera). Two descriptions document the non-obvious
# authoring decisions.
# ----------------------------------------------------------------------------

D_scripted_stunt_is_epistemic_not_world = Description(
    id="D_scripted_stunt_is_epistemic",
    attached_to=anchor_event("E_round_one_knockdown"),
    kind="authoring-note",
    attention=Attention.INTERPRETIVE,
    text=("Apollo's intention to stage a scripted-stunt win is encoded "
          "as a held belief, not a world fact. There is no world-level "
          "`scripted_stunt(apollo, rocky)` that gets retracted when the "
          "fight becomes real. This is deliberate — the stunt narrative "
          "is Apollo's plan, not the world's state, and it erodes "
          "epistemically as Rocky stays up. LT2's retraction signal "
          "detects world retractions only; Apollo's attitude change is "
          "not counted (which is correct — it is not a convergence of "
          "the MC arc, it is an IC-Throughline shift). See "
          "pressure-shape-taxonomy-sketch-01 for the classifier."),
    authored_by="author",
    τ_a=100,
)

D_timelock_not_natively_detectable = Description(
    id="D_timelock_not_natively_detectable",
    attached_to=anchor_event("E_apollo_schedules_mac"),
    kind="authoring-note",
    attention=Attention.STRUCTURAL,
    text=("`scheduled_fight(apollo, mac)` and later "
          "`scheduled_fight(apollo, rocky)` encode Rocky's Timelock "
          "pressure structurally — a future τ_s is committed as early "
          "as τ_s=-10. Under substrate-05's current vocabulary the "
          "classifier cannot detect 'this schedule IS the arc's "
          "endpoint'. LT3-weak reports complement-only; LT3-strong "
          "would read this description-kind or a substrate-06 "
          "scheduling effect. Banked as a forcing function for the "
          "next pass at pressure-shape-taxonomy-sketch."),
    authored_by="author",
    τ_a=100,
)

DESCRIPTIONS = [
    D_scripted_stunt_is_epistemic_not_world,
    D_timelock_not_natively_detectable,
]


# ----------------------------------------------------------------------------
# Rules — one. went_the_distance from fought_rounds + standing_at_final_bell.
# ----------------------------------------------------------------------------
#
# Authored per inference-model-sketch-01's per-story rule discipline.
# The MC's articulated goal (Act 2 midpoint, "I just want to go the
# distance") is the compound this rule derives. Premises accrete at
# E_fight_ends (τ_s=55); derivation fires at query time.
#
# Not authored as a world fact directly because that would hide the
# compound's two-premise structure — Rocky's achievement is the
# conjunction, not a single world predicate. The rule surface makes
# the conjunction queryable.
#
# Depth cap: 1 (head derives directly from body premises, no chaining).

WENT_THE_DISTANCE_RULE = Rule(
    id="R_went_the_distance",
    head=Prop("went_the_distance", ("X", "Y")),
    body=(
        Prop("fought_rounds", ("X", "Y", 15)),
        Prop("standing_at_final_bell", ("X", "fight")),
    ),
)

RULES = (WENT_THE_DISTANCE_RULE,)
