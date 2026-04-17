"""
Ackroyd — the encoded fabula and sjuzhet for *The Murder of Roger
Ackroyd* (Christie, 1926).

Third authored substrate encoding, after oedipus.py and macbeth.py.
Story content only. No substrate logic. This file parallels the
existing pair in shape and pressure-tests the substrate on a
structurally dissimilar work — per REVIEW.md's next-term item #1
("add at least one structurally dissimilar third story before
locking more verifier assumptions in place") and per
ackroyd-sketch-01.md's plan.

What this encoding is meant to pressure:

- **The disclosure / sjuzhet layer.** The novel is narrated
  throughout by Dr. James Sheppard, who is also the murderer. His
  withholding is the load-bearing structural feature. Every
  SjuzhetEntry has `focalizer_id="sheppard"` — the reader sees only
  what he shows, at the τ_d he chooses. The murder itself (fabula
  τ_s=1) is narratively withheld until the final chapter (τ_d late),
  exposing the substrate's long-deferred disclosure case for the
  first time.

- **Identity-as-role-stack.** Sheppard is simultaneously: village
  doctor, blackmailer of Mrs. Ferrars, murderer of Ackroyd, the
  text's narrator. All four roles are true from his first
  appearance; the novel's structure is which role he reveals when.
  No identity collapse (he isn't-someone-else-all-along); the
  identities are all him at once.

- **Closed-circle epistemic investigation.** Like Oedipus, Ackroyd
  turns on working out who did it. Unlike Oedipus, the suspect
  pool is known from chapter one and the epistemic frames are
  many (Sheppard, Poirot, Caroline, each suspect). The substrate's
  agent-knowledge machinery (project_knowledge) gets broad
  exercise; the inference engine gets little (no compound moral
  derivations on the scale of tyrant(macbeth) — a single
  betrayer_of_trust rule is enough).

- **Retroactive reveal at the discourse level.** Poirot's
  anagnorisis is at the fabula layer (he learns killed(sheppard,
  ackroyd)); the *reader's* anagnorisis is at the disclosure
  layer (everything previously read is recontextualized). The
  substrate has no explicit notion of "reader retrocontextualizes
  prior narration" — this encoding surfaces that gap without
  (yet) filling it. See the encoding-choices section below.

Encoding choices (explicit, so future readers understand the slice):

- **Branches: canonical only.** Ackroyd has no Rashomon-style
  contested branches. The cast's individual beliefs diverge (Parker
  BELIEVES Ackroyd alive at 9:30pm via the dictaphone), but these
  are agent-knowledge facts on a single canonical world.

- **Identity placeholders: none in the Oedipus sense.** Sheppard's
  multiple roles do not require identity equivalence classes; he
  is one Entity with many role-facts. The prior-encoded
  `identity_prop` / `gap_*` machinery is not exercised here.

- **Unreliable narration encoding.** Fabula events are authored
  honestly (the murder is at τ_s=1, with killed(sheppard, ackroyd)
  as a world effect). The sjuzhet layer handles the withholding:
  the murder's SjuzhetEntry lands at τ_d=15 (the late chapter
  where Sheppard's confession manuscript fills the gap), not at
  τ_d=2 (where the fabula event sits). The gap between τ_s and
  τ_d *is* the unreliable narration in substrate terms. This is
  the substrate's natural handling for anachrony, repurposed for
  a withholding narrator.

- **The dictaphone-trick encoding.** Sheppard records Ackroyd's
  voice, then plays it back after killing him. Parker hears the
  voice and BELIEVES Ackroyd alive at 9:30pm — a deliberately-
  planted false belief. The substrate records Parker's BELIEVED
  set diverging from world-truth via a told_by with a falsified
  source (the dictaphone acting as Ackroyd). When the body is
  discovered at τ_s=2, Parker's BELIEVED is dislodged and
  replaced with KNOWN dead(ackroyd).

- **The reader as frame, not Entity.** Per ackroyd-sketch-01's
  open question, the encoding does NOT introduce a synthetic
  `reader` Entity. The reader's epistemic state is modeled by the
  sjuzhet's disclosures tuple (what the reader learns at each
  τ_d). If that turns out to be insufficient, a future substrate
  extension will revisit.

- **Compound predicates (candidate derivations).** Two moral rules,
  less than Macbeth's four:
      killed(X, Y) ∧ patient_of(Y, X)      ⇒ betrayer_of_trust(X, Y)
      blackmailed(X, Y) ∧ dead(Y)          ⇒ driver_of_suicide(X, Y)
        ∧ death_was_suicide(Y)
  The first fires on Sheppard killing Ackroyd (his patient and
  friend); the second on Sheppard's blackmail of Mrs. Ferrars
  (her death is suicide). Same pattern as Macbeth's
  author-assert-the-derivation-at-the-event practice.

- **Scope of the novel encoded.** Roughly all of it, at the event
  level — ~17 fabula events covering the ~3-week compressed
  action. Detailed village gossip (Caroline's chapter-opening
  roundups, the mah-jongg evenings, the tea-party exchanges) is
  collapsed into structural outcomes. The investigation's long
  middle is compressed: Poirot's questioning of individual
  suspects is condensed into 3-4 events, not 10+.
"""

from __future__ import annotations

from substrate import (
    Entity, Prop, Event, EventStatus,
    Branch, BranchKind, CANONICAL, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
    Rule,
)


# ----------------------------------------------------------------------------
# Entities
# ----------------------------------------------------------------------------

poirot            = Entity(id="poirot",            name="Hercule Poirot",        kind="agent")
sheppard          = Entity(id="sheppard",          name="Dr. James Sheppard",    kind="agent")
caroline_sheppard = Entity(id="caroline_sheppard", name="Caroline Sheppard",     kind="agent")
ackroyd           = Entity(id="ackroyd",           name="Roger Ackroyd",         kind="agent")
mrs_ferrars       = Entity(id="mrs_ferrars",       name="Mrs. Ferrars",          kind="agent")
mr_ferrars        = Entity(id="mr_ferrars",        name="Mr. Ferrars",           kind="agent")
ralph_paton       = Entity(id="ralph_paton",       name="Ralph Paton",           kind="agent")
flora_ackroyd     = Entity(id="flora_ackroyd",     name="Flora Ackroyd",         kind="agent")
geoffrey_raymond  = Entity(id="geoffrey_raymond",  name="Geoffrey Raymond",      kind="agent")
major_blunt       = Entity(id="major_blunt",       name="Major Blunt",           kind="agent")
ursula_bourne     = Entity(id="ursula_bourne",     name="Ursula Bourne",         kind="agent")
parker            = Entity(id="parker",            name="Parker",                kind="agent")
inspector_raglan  = Entity(id="inspector_raglan",  name="Inspector Raglan",      kind="agent")

kings_abbot       = Entity(id="kings_abbot",       name="King's Abbot village",  kind="location")
fernly_park       = Entity(id="fernly_park",       name="Fernly Park (Ackroyd's house)", kind="location")
sheppards_house   = Entity(id="sheppards_house",   name="Sheppards' house",      kind="location")


ENTITIES = [
    poirot, sheppard, caroline_sheppard,
    ackroyd, mrs_ferrars, mr_ferrars,
    ralph_paton, flora_ackroyd, geoffrey_raymond, major_blunt,
    ursula_bourne, parker, inspector_raglan,
    kings_abbot, fernly_park, sheppards_house,
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

def killed(killer: str, victim: str) -> Prop:
    return Prop("killed", (killer, victim))

def dead(who: str) -> Prop:
    return Prop("dead", (who,))

def alive(who: str) -> Prop:
    # Used for the dictaphone-trick false-belief case; Parker BELIEVES
    # alive(ackroyd) at 9:30pm because Sheppard staged the recording.
    # The substrate records what's believed; the falseness is that
    # dead(ackroyd) already holds world-wise at this τ_s.
    return Prop("alive", (who,))

def doctor(who: str) -> Prop:
    return Prop("doctor", (who,))

def patient_of(patient: str, doctor: str) -> Prop:
    return Prop("patient_of", (patient, doctor))

def widow_of(widow: str, spouse: str) -> Prop:
    return Prop("widow_of", (widow, spouse))

def widower_of(widower: str, spouse: str) -> Prop:
    return Prop("widower_of", (widower, spouse))

def wealthy(who: str) -> Prop:
    return Prop("wealthy", (who,))

def niece_of(niece: str, uncle: str) -> Prop:
    return Prop("niece_of", (niece, uncle))

def stepson_of(stepson: str, stepparent: str) -> Prop:
    return Prop("stepson_of", (stepson, stepparent))

def engaged(a: str, b: str) -> Prop:
    return Prop("engaged", (a, b))

def married(a: str, b: str) -> Prop:
    return Prop("married", (a, b))

def secretly_married(a: str, b: str) -> Prop:
    # Ralph and Ursula's marriage, concealed from the household.
    # Distinguished from `married` so the visible-vs-concealed
    # status is queryable.
    return Prop("secretly_married", (a, b))

def secretary_of(secretary: str, employer: str) -> Prop:
    return Prop("secretary_of", (secretary, employer))

def sibling_of(a: str, b: str) -> Prop:
    return Prop("sibling_of", (a, b))

def butler_of(butler: str, household: str) -> Prop:
    return Prop("butler_of", (butler, household))

def parlormaid_of(maid: str, household: str) -> Prop:
    return Prop("parlormaid_of", (maid, household))

def at_location(who: str, where: str) -> Prop:
    return Prop("at_location", (who, where))

def poisoned(poisoner: str, victim: str) -> Prop:
    return Prop("poisoned", (poisoner, victim))

def blackmailed(blackmailer: str, victim: str) -> Prop:
    return Prop("blackmailed", (blackmailer, victim))

def death_was_suicide(who: str) -> Prop:
    # Modality on a death. Not all deaths in Ackroyd are suicides;
    # this flag lets the driver_of_suicide rule discriminate.
    return Prop("death_was_suicide", (who,))

def accused_of_murder(who: str, of_whom: str) -> Prop:
    # Ralph Paton is publicly accused (flees, looks guilty). This is
    # a social/public fact, not a derived moral one.
    return Prop("accused_of_murder", (who, of_whom))

# Compound / moral-register predicates. Authored as world facts where
# their premises hold; candidate derivations for the rule engine.

def betrayer_of_trust(who: str, victim: str) -> Prop:
    # ⇐ killed(X, Y) ∧ patient_of(Y, X)
    # The doctor who murders his patient. Sheppard on Ackroyd.
    return Prop("betrayer_of_trust", (who, victim))

def driver_of_suicide(who: str, victim: str) -> Prop:
    # ⇐ blackmailed(X, Y) ∧ dead(Y) ∧ death_was_suicide(Y)
    # The blackmailer whose pressure drove the suicide. Sheppard on
    # Mrs. Ferrars. Named morally-loaded so the verifier surface can
    # ask "is Sheppard a driver_of_suicide?" as a claim-moment check.
    return Prop("driver_of_suicide", (who, victim))


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

    # --- Pre-play (τ_s < 0) — static facts and backstory ---

    Event(
        id="E_ackroyd_wealthy_widower",
        type="standing",
        τ_s=-100, τ_a=1,
        participants={"who": "ackroyd"},
        effects=(
            world(wealthy("ackroyd")),
            # Ackroyd's first wife died years before the action.
            # Her death is pre-play backstory and not authored as
            # its own event; only the widower-standing matters.
            world(widower_of("ackroyd", "first-wife-deceased")),
        ),
    ),

    Event(
        id="E_sheppard_is_doctor",
        type="standing",
        τ_s=-100, τ_a=2,
        participants={"who": "sheppard"},
        effects=(
            world(doctor("sheppard")),
            # Sheppard is Ackroyd's doctor — the trust relationship
            # that makes killed(sheppard, ackroyd) a
            # betrayer_of_trust derivation.
            world(patient_of("ackroyd", "sheppard")),
            # And Mrs. Ferrars' doctor — how he discovers her
            # poisoning of her husband, which is what he then
            # blackmails her over.
            world(patient_of("mrs_ferrars", "sheppard")),
            world(sibling_of("sheppard", "caroline_sheppard")),
            world(sibling_of("caroline_sheppard", "sheppard")),
        ),
    ),

    Event(
        id="E_household_standing",
        type="standing",
        τ_s=-100, τ_a=3,
        participants={"patriarch": "ackroyd"},
        effects=(
            # The cast's standing relations at Fernly Park, authored
            # at a distant τ_s so they're always in world-scope.
            world(niece_of("flora_ackroyd", "ackroyd")),
            world(stepson_of("ralph_paton", "ackroyd")),
            world(engaged("flora_ackroyd", "ralph_paton")),
            world(secretary_of("geoffrey_raymond", "ackroyd")),
            world(butler_of("parker", "fernly_park")),
            world(parlormaid_of("ursula_bourne", "fernly_park")),
        ),
    ),

    Event(
        id="E_ralph_ursula_secretly_married",
        type="marriage",
        τ_s=-10, τ_a=4,
        participants={"spouses": ["ralph_paton", "ursula_bourne"]},
        effects=(
            # Pre-play secret marriage — not revealed to the household
            # until Ursula confesses during Poirot's investigation.
            # Authored as world fact + both spouses holding it at
            # KNOWN; concealment is that no other Entity is told.
            world(secretly_married("ralph_paton", "ursula_bourne")),
            world(married("ralph_paton", "ursula_bourne")),
            observe("ralph_paton",
                    secretly_married("ralph_paton", "ursula_bourne"), -10,
                    note="their shared secret"),
            observe("ursula_bourne",
                    secretly_married("ralph_paton", "ursula_bourne"), -10),
        ),
    ),

    Event(
        id="E_mr_ferrars_poisoned",
        type="killing",
        τ_s=-20, τ_a=5,
        participants={"killer": "mrs_ferrars", "victim": "mr_ferrars"},
        effects=(
            # Mrs. Ferrars poisons her husband to be free of him.
            # The fact stays hidden from most of the village; only
            # Sheppard (as her doctor) pieces it together.
            world(dead("mr_ferrars")),
            world(killed("mrs_ferrars", "mr_ferrars")),
            world(poisoned("mrs_ferrars", "mr_ferrars")),
            world(widow_of("mrs_ferrars", "mr_ferrars")),
            # Mrs. Ferrars knows what she did.
            observe("mrs_ferrars",
                    killed("mrs_ferrars", "mr_ferrars"), -20),
            observe("mrs_ferrars",
                    poisoned("mrs_ferrars", "mr_ferrars"), -20),
        ),
    ),

    Event(
        id="E_sheppard_deduces_poisoning",
        type="deduction",
        τ_s=-18, τ_a=6,
        participants={"deducer": "sheppard", "subject": "mrs_ferrars"},
        effects=(
            # Sheppard — as the attending physician to Mr. Ferrars'
            # illness and death — works out what really happened.
            # This is how he comes into possession of the leverage
            # he will then use for blackmail.
            observe("sheppard",
                    killed("mrs_ferrars", "mr_ferrars"), -18,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="medical-pattern deduction"),
            observe("sheppard",
                    poisoned("mrs_ferrars", "mr_ferrars"), -18,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN),
        ),
    ),

    Event(
        id="E_sheppard_blackmails_ferrars",
        type="blackmail_begins",
        τ_s=-15, τ_a=7,
        participants={"blackmailer": "sheppard",
                      "victim": "mrs_ferrars"},
        effects=(
            # Sheppard begins extorting Mrs. Ferrars on the strength
            # of what he knows. The blackmail runs for ~15 τ_s units
            # (substrate time; story-months) until her suicide.
            world(blackmailed("sheppard", "mrs_ferrars")),
            # Both participants hold the blackmail relation at KNOWN
            # (she knows who's pressuring her; he knows he's the one
            # doing it).
            observe("sheppard",
                    blackmailed("sheppard", "mrs_ferrars"), -15,
                    note="the lever he uses; motive for later murder"),
            observe("mrs_ferrars",
                    blackmailed("sheppard", "mrs_ferrars"), -15,
                    note="knows her blackmailer's identity"),
        ),
    ),

    # --- In-play (τ_s ≥ 0) ---

    Event(
        id="E_mrs_ferrars_suicide",
        type="death_by_suicide",
        τ_s=0, τ_a=10,
        participants={"who": "mrs_ferrars",
                      "attending_physician": "sheppard"},
        effects=(
            # The novel opens with Mrs. Ferrars dead. Sheppard has
            # been summoned in the night (as her doctor) and
            # pronounces death; the household regards it as overdose.
            # Mrs. Ferrars has left a letter for Ackroyd naming her
            # blackmailer (unnamed here; the letter is an authored
            # object whose contents are disclosed via the next
            # event).
            world(dead("mrs_ferrars")),
            world(death_was_suicide("mrs_ferrars")),
            # The rule head — authored here at the event where the
            # premises are all satisfied (blackmailed + dead + suicide).
            # A future rule-engine run will derive the same fact.
            world(driver_of_suicide("sheppard", "mrs_ferrars")),
            # Sheppard knows — he was her doctor, pronounced her
            # death, and (crucially) knows he was the blackmailer.
            observe("sheppard", dead("mrs_ferrars"), 0),
            observe("sheppard", death_was_suicide("mrs_ferrars"), 0),
            observe("sheppard",
                    driver_of_suicide("sheppard", "mrs_ferrars"), 0,
                    note="moral derivation visible to himself"),
            # The village learns by morning.
            observe("caroline_sheppard", dead("mrs_ferrars"), 0),
            observe("ackroyd", dead("mrs_ferrars"), 0,
                    note="the bereaved; she was his intended"),
        ),
    ),

    Event(
        id="E_ackroyd_dines_with_sheppard",
        type="dinner_meeting",
        τ_s=1, τ_a=11,
        participants={"host": "ackroyd", "guest": "sheppard"},
        effects=(
            # Evening of the murder. Ackroyd invites Sheppard to
            # dinner; during the study portion he reveals he has
            # received Mrs. Ferrars' letter from the morning's post
            # — a confession of the poisoning AND naming her
            # blackmailer. Ackroyd has not yet opened / finished
            # reading it.
            world(at_location("sheppard", "fernly_park")),
            world(at_location("ackroyd", "fernly_park")),
            observe("sheppard", at_location("ackroyd", "fernly_park"), 1),
            # Ackroyd tells Sheppard about receiving the letter.
            # (He does not know Sheppard IS the blackmailer.)
            told_by("sheppard", "ackroyd",
                    Prop("received_letter_from_ferrars", ("ackroyd",)),
                    1,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="trigger event for the murder — Ackroyd is "
                         "about to read a document that names "
                         "Sheppard"),
        ),
    ),

    Event(
        id="E_sheppard_plants_dictaphone",
        type="preparation",
        τ_s=1, τ_a=12,
        participants={"agent": "sheppard"},
        effects=(
            # Before leaving Ackroyd's study, Sheppard sets up the
            # dictaphone to replay a recording of Ackroyd's voice
            # later. The trick establishes the false time-of-death
            # (after Sheppard has left and has an alibi).
            # No world-level fact changes here; this is the setup.
            observe("sheppard",
                    Prop("dictaphone_set_to_play", ("sheppard",)), 1,
                    note="staged the alibi"),
        ),
    ),

    Event(
        id="E_sheppard_murders_ackroyd",
        type="killing",
        τ_s=1, τ_a=13,
        participants={"killer": "sheppard", "victim": "ackroyd"},
        effects=(
            # The novel's central hidden event. Sheppard kills
            # Ackroyd in the study (stabbed with a Tunisian dagger
            # from Ackroyd's curio collection) before Ackroyd can
            # finish reading Mrs. Ferrars' letter. Sheppard locks
            # the study door from the inside and exits through the
            # window, which he then secures.
            world(dead("ackroyd")),
            world(killed("sheppard", "ackroyd")),
            # Authored rule head — betrayer_of_trust derivable from
            # killed + patient_of.
            world(betrayer_of_trust("sheppard", "ackroyd")),
            # Sheppard knows what he did. This is his KNOWN set
            # from τ_s=1 onward — the exact set he will withhold
            # from the narration until the final chapter.
            observe("sheppard", killed("sheppard", "ackroyd"), 1,
                    note="withheld from narration until τ_d=15"),
            observe("sheppard", dead("ackroyd"), 1),
            observe("sheppard",
                    betrayer_of_trust("sheppard", "ackroyd"), 1,
                    note="the moral fact he carries"),
        ),
    ),

    Event(
        id="E_sheppard_leaves_fernly",
        type="departure",
        τ_s=1, τ_a=14,
        participants={"who": "sheppard"},
        effects=(
            # Sheppard leaves the house visibly (ensuring his
            # departure is witnessed by Parker). This is the alibi's
            # observable half: he was seen leaving before the
            # dictaphone-faked "later conversation" in the study.
            world(at_location("sheppard", "kings_abbot")),
            observe("parker",
                    at_location("sheppard", "kings_abbot"), 1,
                    note="saw Sheppard leaving; builds the alibi"),
        ),
    ),

    Event(
        id="E_dictaphone_plays",
        type="staged_disclosure",
        τ_s=1, τ_a=15,
        participants={"device_operator": "sheppard",
                      "audience": "parker"},
        effects=(
            # Half an hour later the dictaphone plays; Parker,
            # passing the study, hears Ackroyd's voice and BELIEVES
            # Ackroyd alive. The substrate records the belief as
            # told_by from a falsified speaker.
            told_by("parker", "ackroyd-via-dictaphone",
                    alive("ackroyd"), 1,
                    slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                    note="dictaphone-trick: Parker deceived by recording"),
            # The world is already dead(ackroyd); the substrate does
            # not revoke that. Parker's BELIEVED set diverges from
            # the world-facts — the substrate holds both honestly.
        ),
    ),

    Event(
        id="E_body_discovered",
        type="discovery",
        τ_s=2, τ_a=16,
        participants={"discoverer": "parker",
                      "also_present": ["sheppard", "raymond"],
                      "victim": "ackroyd"},
        effects=(
            # Morning after. Sheppard (called back to the house on
            # a pretext, or returning as doctor at Parker's urgent
            # call) is present when the study is broken into. The
            # body is discovered.
            observe("parker", dead("ackroyd"), 2),
            observe("sheppard", dead("ackroyd"), 2,
                    note="feigned surprise; he knew"),
            observe("geoffrey_raymond", dead("ackroyd"), 2),
            # Parker's earlier BELIEVED alive(ackroyd) is now
            # dislodged — what he thought he heard at 9:30pm has
            # been shown false.
            remove_held("parker", alive("ackroyd"),
                        Slot.BELIEVED, Confidence.BELIEVED, 2,
                        note="dictaphone-trick belief undone by "
                             "discovery of the body"),
        ),
    ),

    Event(
        id="E_ralph_missing",
        type="fact",
        τ_s=2, τ_a=17,
        participants={"who": "ralph_paton"},
        effects=(
            # Ralph has vanished — he was at Fernly the evening of
            # the murder and has not been seen since. He becomes
            # the prime suspect. His disappearance is authored
            # as a fact at the morning of discovery.
            observe("parker",
                    Prop("missing", ("ralph_paton",)), 2),
            observe("flora_ackroyd",
                    Prop("missing", ("ralph_paton",)), 2,
                    note="his fiancée notices first"),
            # Public accusation forms within hours; the village /
            # police converge on Ralph-as-killer.
            world(accused_of_murder("ralph_paton", "ackroyd")),
        ),
    ),

    Event(
        id="E_flora_summons_poirot",
        type="commission",
        τ_s=2, τ_a=18,
        participants={"client": "flora_ackroyd",
                      "detective": "poirot"},
        effects=(
            # Flora — convinced Ralph is innocent — goes to Poirot,
            # whom the Sheppards know as "the retiree with the
            # vegetable marrows" next door. She asks him to
            # investigate. This is when Poirot enters the fabula
            # as the Protagonist on the story goal.
            observe("poirot",
                    Prop("commissioned_by", ("poirot", "flora_ackroyd")),
                    2,
                    note="Flora's conviction of Ralph's innocence "
                         "motivates the investigation"),
            observe("poirot", dead("ackroyd"), 2),
            observe("poirot",
                    accused_of_murder("ralph_paton", "ackroyd"), 2),
        ),
    ),

    Event(
        id="E_poirot_investigates",
        type="investigation_sequence",
        τ_s=5, τ_a=19,
        participants={"detective": "poirot",
                      "assistant": "sheppard",
                      "subjects": ["flora_ackroyd", "major_blunt",
                                   "geoffrey_raymond", "parker",
                                   "ursula_bourne"]},
        effects=(
            # Compressed: Poirot interviews the household over
            # several days. Each interview adds to his BELIEVED
            # set; specific plot-threads surface:
            # - Flora's £40 theft (Raymond sees her leaving study)
            # - Parker's earlier blackmail attempt at another post
            # - Raymond's overheard snippet of "the call upon you..."
            # - Ursula's secret marriage to Ralph (she confesses)
            # - Major Blunt's love for Flora (his own reason for
            #   keeping quiet)
            # The encoding collapses the inquiry into structural
            # outcomes rather than authoring each interview as its
            # own event.
            observe("poirot",
                    secretly_married("ralph_paton", "ursula_bourne"), 5,
                    note="Ursula confesses during interview"),
            observe("poirot",
                    Prop("overheard_phrase",
                         ("raymond",
                          "the_call_upon_you_for_restitution")),
                    5,
                    note="Raymond's partial testimony"),
            # Sheppard accompanies Poirot throughout, nominally as
            # assistant/Watson; in fact managing what Poirot sees.
            # He holds the complete set of his own KNOWN guilt-facts
            # through every interview.
            observe("sheppard",
                    Prop("assists_investigation", ("sheppard",)), 5,
                    note="present at every interview; controls "
                         "what he can of Poirot's field of view"),
        ),
    ),

    Event(
        id="E_poirot_reveals_solution",
        type="anagnorisis_public",
        τ_s=8, τ_a=20,
        participants={"detective": "poirot",
                      "cast": ["sheppard", "flora_ackroyd",
                               "major_blunt", "geoffrey_raymond",
                               "ursula_bourne", "parker",
                               "caroline_sheppard",
                               "inspector_raglan"]},
        effects=(
            # Poirot's drawing-room scene: he walks the cast
            # through the reconstruction. The killer is named —
            # Sheppard. The narrative twist is that the reader has
            # just realized the narrator is the murderer.
            # Poirot's KNOWN set at this event now contains the
            # full truth.
            observe("poirot", killed("sheppard", "ackroyd"), 8,
                    note="constructed proof via dictaphone analysis, "
                         "phone-call trace, blackmail motive, "
                         "patient_of-trust position"),
            observe("poirot",
                    betrayer_of_trust("sheppard", "ackroyd"), 8),
            observe("poirot",
                    blackmailed("sheppard", "mrs_ferrars"), 8,
                    note="the motive — Ackroyd was about to read "
                         "the name in the letter"),
            observe("poirot",
                    driver_of_suicide("sheppard", "mrs_ferrars"), 8),
            # The cast learns too. Each household member's KNOWN
            # set updates with killed(sheppard, ackroyd) at this
            # moment.
            observe("caroline_sheppard",
                    killed("sheppard", "ackroyd"), 8,
                    note="her brother — the hardest hearer"),
            observe("flora_ackroyd",
                    killed("sheppard", "ackroyd"), 8),
            observe("inspector_raglan",
                    killed("sheppard", "ackroyd"), 8),
            # Public naming of Sheppard retracts the earlier
            # accused_of_murder(ralph_paton, ackroyd) fact. Ralph
            # is cleared by the same reveal that names the killer —
            # the substrate must now record that state transition
            # explicitly so downstream queries see him un-accused.
            # Without this, "Ralph cleared" would remain a purely
            # social inference the substrate cannot witness.
            world(accused_of_murder("ralph_paton", "ackroyd"),
                  asserts=False),
        ),
    ),

    Event(
        id="E_poirot_private_confrontation",
        type="ultimatum",
        τ_s=9, τ_a=21,
        participants={"detective": "poirot", "killer": "sheppard"},
        effects=(
            # After the public reveal, Poirot speaks with Sheppard
            # privately. He gives Sheppard a night's grace — make
            # the right choice for the family's sake. The
            # confrontation is the novel's structural denouement:
            # Poirot has the case but lets Sheppard close it
            # himself.
            told_by("sheppard", "poirot",
                    Prop("ultimatum_confession_or_disclosure",
                         ("sheppard",)),
                    9,
                    slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                    note="take your own way out, or I go to "
                         "Raglan in the morning"),
        ),
    ),

    Event(
        id="E_sheppard_writes_manuscript",
        type="confession_writing",
        τ_s=10, τ_a=22,
        participants={"writer": "sheppard"},
        effects=(
            # Overnight, Sheppard completes the manuscript the
            # reader has been reading. The final chapter is the
            # confession — the first honest narration Sheppard
            # has produced. The manuscript ends with his intended
            # overdose.
            observe("sheppard",
                    Prop("wrote_confession", ("sheppard",)), 10,
                    note="the text we've been reading becomes "
                         "honest only in its final chapter"),
        ),
    ),

    Event(
        id="E_sheppard_suicide",
        type="death_by_suicide",
        τ_s=11, τ_a=23,
        participants={"who": "sheppard"},
        effects=(
            # Off-page in the novel proper — the manuscript's final
            # page describes the intent; the reader infers the
            # completion. Encoded here as the fabula event.
            world(dead("sheppard")),
            world(death_was_suicide("sheppard")),
        ),
    ),

]


# ----------------------------------------------------------------------------
# Preplay disclosures
# ----------------------------------------------------------------------------
#
# Village-knowledge the reader starts with in chapter 1. Less
# mythologically loaded than Oedipus's preplay set — Christie's
# 1926 reader is expected to know nothing specific about King's
# Abbot; the disclosures are whatever Sheppard's opening chapter
# establishes as settled village fact.

PREPLAY_DISCLOSURES = (
    Disclosure(prop=wealthy("ackroyd"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=doctor("sheppard"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=sibling_of("sheppard", "caroline_sheppard"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=niece_of("flora_ackroyd", "ackroyd"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=engaged("flora_ackroyd", "ralph_paton"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=stepson_of("ralph_paton", "ackroyd"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=secretary_of("geoffrey_raymond", "ackroyd"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
    Disclosure(prop=butler_of("parker", "fernly_park"),
               slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
               via=Narrative.DISCLOSURE.value),
)


# ----------------------------------------------------------------------------
# Sjuzhet — the reader's-timeline ordering of events.
# ----------------------------------------------------------------------------
#
# Every entry has focalizer_id="sheppard". This is the load-bearing
# encoding move: the novel is a continuous first-person narration
# by one character, and that character's withholding shapes what
# the reader sees at each τ_d.
#
# Three patterns of τ_d vs τ_s:
#
# 1. Honestly narrated events: τ_d closely tracks τ_s. Mrs.
#    Ferrars' suicide, the dinner at Fernly, the morning's body-
#    discovery — all at their natural positions.
#
# 2. Events outside Sheppard's direct witness: the dictaphone
#    playing to Parker, Poirot's investigation interviews where
#    Sheppard is present — narrated by Sheppard at the τ_d he
#    writes about them; mostly in fabula order.
#
# 3. Withheld events — the murder itself (E_sheppard_murders_
#    ackroyd) and its setup (E_sheppard_plants_dictaphone). These
#    are authored at τ_s=1 but only disclosed at τ_d=15-16, when
#    Sheppard's confession manuscript fills the gap. The entry
#    for E_sheppard_murders_ackroyd has τ_d=15, not τ_d=2 — the
#    reader does not learn of the murder at its fabula position.
#
# This third pattern is the substrate's handling of unreliable
# narration in its current shape: not a new record type, but a
# use of the existing τ_d-τ_s separation to represent narrative
# withholding. Whether that's the right long-run model is
# ackroyd-sketch-01's open question OQ1.

SJUZHET = [

    # τ_d=0 — opening chapter. Sheppard returns from pronouncing
    # Mrs. Ferrars dead; breakfast with Caroline; village gossip.
    SjuzhetEntry(
        event_id="E_mrs_ferrars_suicide",
        τ_d=0,
        focalizer_id="sheppard",
        disclosures=PREPLAY_DISCLOSURES,
    ),

    # τ_d=1 — the dinner at Fernly. Sheppard's account of the
    # evening Ackroyd reveals the letter. Narrated honestly at
    # this point — Sheppard has not yet acted.
    SjuzhetEntry(
        event_id="E_ackroyd_dines_with_sheppard",
        τ_d=1,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    # τ_d=2 — morning after. Sheppard narrates Parker's summons,
    # the body discovered, the household's shock. Sheppard's
    # narration of his own reaction is the novel's first major
    # act of performed innocence; the withholding of his prior
    # acts is the omission.
    SjuzhetEntry(
        event_id="E_body_discovered",
        τ_d=2,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    # τ_d=3 — Ralph's absence, rumors, Flora's conviction.
    SjuzhetEntry(
        event_id="E_ralph_missing",
        τ_d=3,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    # τ_d=4 — Flora approaches Poirot. Sheppard's POV is the
    # bemused-neighbor framing — Poirot the retired eccentric with
    # the vegetable marrows.
    SjuzhetEntry(
        event_id="E_flora_summons_poirot",
        τ_d=4,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    # τ_d=5-8 — middle of the novel: the investigation sequence.
    # Compressed here as a single sjuzhet entry matching the single
    # fabula event. The novel spends 8-10 chapters here; the
    # encoding collapses.
    SjuzhetEntry(
        event_id="E_poirot_investigates",
        τ_d=5,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    # τ_d=12 — Parker's 9:30pm dictaphone experience. In the novel,
    # Parker's testimony about hearing Ackroyd's voice comes out
    # during Poirot's interviews; the reader encounters it mid-
    # investigation, not at τ_d=1 when it happened. We place the
    # sjuzhet entry here to reflect when the reader learns of it,
    # not when it occurred. This is one of the substrate's
    # τ_s-vs-τ_d divergence cases.
    SjuzhetEntry(
        event_id="E_dictaphone_plays",
        τ_d=12,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    # τ_d=14 — Poirot gathers the cast; the reveal scene begins.
    SjuzhetEntry(
        event_id="E_poirot_reveals_solution",
        τ_d=14,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    # τ_d=15 — the late-chapter disclosure: Sheppard's confession
    # manuscript retrocontextualizes the novel. Here the two
    # withheld events — the dictaphone setup and the murder —
    # finally receive sjuzhet entries. τ_d is large, τ_s is small
    # (=1); the gap *is* the unreliable narration.
    SjuzhetEntry(
        event_id="E_sheppard_plants_dictaphone",
        τ_d=15,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    SjuzhetEntry(
        event_id="E_sheppard_murders_ackroyd",
        τ_d=15,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    SjuzhetEntry(
        event_id="E_sheppard_leaves_fernly",
        τ_d=15,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    # τ_d=16 — the private confrontation between Poirot and
    # Sheppard, narrated by Sheppard from retrospect.
    SjuzhetEntry(
        event_id="E_poirot_private_confrontation",
        τ_d=16,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    # τ_d=17 — the confession manuscript's final pages.
    SjuzhetEntry(
        event_id="E_sheppard_writes_manuscript",
        τ_d=17,
        focalizer_id="sheppard",
        disclosures=(),
    ),

    # τ_d=18 — the intended overdose. Off-page in the novel; the
    # sjuzhet entry represents the reader's inference from the
    # manuscript's closing words.
    SjuzhetEntry(
        event_id="E_sheppard_suicide",
        τ_d=18,
        focalizer_id="sheppard",
        disclosures=(),
    ),
]


# ----------------------------------------------------------------------------
# Rules — candidate compound-predicate derivations.
# ----------------------------------------------------------------------------
#
# Two depth-1 rules. Less than Macbeth's four because Ackroyd is a
# whodunit rather than a moral-escalation tragedy — its rule-engine
# pressure is narrower. Both are authored as world-effects at the
# events where their premises satisfy; the RULES tuple lets
# verification layer queries fire the derivation independently.

BETRAYER_OF_TRUST_RULE = Rule(
    id="betrayer_of_trust",
    head=Prop("betrayer_of_trust", ("X", "Y")),
    body=(
        Prop("killed", ("X", "Y")),
        Prop("patient_of", ("Y", "X")),
    ),
)

DRIVER_OF_SUICIDE_RULE = Rule(
    id="driver_of_suicide",
    head=Prop("driver_of_suicide", ("X", "Y")),
    body=(
        Prop("blackmailed", ("X", "Y")),
        Prop("dead", ("Y",)),
        Prop("death_was_suicide", ("Y",)),
    ),
)

RULES = (
    BETRAYER_OF_TRUST_RULE,
    DRIVER_OF_SUICIDE_RULE,
)
