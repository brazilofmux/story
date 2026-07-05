"""
winter_count.py — THE WINTER COUNT: an original Vastisetr story, encoded
substrate-first.

The companion piece to "The Price of Warmth" (same town, two generations
earlier, the same four-domain grid) with every commercial imperative
deliberately refused. This encoding exists to demonstrate that the engine
can hold a shape the market would note to death:

  - the protagonist's first significant act is refusing a starving family
    (the save-the-cat beat, inverted);
  - she is complicit, not innocent — her one lie is the hinge every later
    death hangs on;
  - she has NO arc: Resolve=Steadfast, and the last scene shows her doing
    exactly what the first scene shows her doing, at a table, counting;
  - Outcome=Failure (the goal is lost), Judgment=Bad (no consolation, no
    redeeming lesson);
  - there is no villain — every actor is right by their own lights;
  - the relationship story ends in severance and a body on the ice.

Why it should still work as a story: the reader holds the rot from the
third scene onward (a fifteen-scene dread runway of pure dramatic irony),
every turn is a decision with visible arithmetic behind it (Driver=
Decision — no storms of coincidence after the first), the options narrow
one by one (Optionlock), and the ending is inevitable in retrospect —
the tragedy contract, kept to the letter.

The knowledge discipline is the load-bearing wall here, not decoration:

  - E_rot_found puts `rot(granary)` into the WORLD and into ONE mind
    (Halla's). The town's `stores_enough` belief — held CERTAIN, via
    utterance-heard, from the public count — is thereafter FALSE, and the
    substrate knows it is false.
  - E_pass_vote is the hinge: the town, reasoning correctly on the false
    number, votes down the one option that could have saved it — and the
    substrate can show the vote was RATIONAL given what each voter held.
  - The sibling knowledge-lock: after E_shortfall, Halla cannot expose
    Eirik's forged chit without an audit exposing her false total; her
    lie shields his theft. Each secret is the other's hostage. No scene
    states this; it FOLLOWS from who knows what, when.

Title note: a winter count is a year-record that names the year after the
worst thing that happened in it. Vastisetr's ledger becomes one.
"""

from __future__ import annotations

from story_engine.core.substrate import (
    Entity, Prop, Event,
    CANONICAL, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect,
    SjuzhetEntry, Disclosure,
    Description, Attention, anchor_event,
)


# ----------------------------------------------------------------------------
# Entities
# ----------------------------------------------------------------------------

halla   = Entity(id="halla",  name="Halla Ketilsdottir", kind="agent")
eirik   = Entity(id="eirik",  name="Eirik Ketilsson",    kind="agent")
jorunn  = Entity(id="jorunn", name="Jorunn Lawspeaker",  kind="agent")
ragna   = Entity(id="ragna",  name="Ragna Ostergard",    kind="agent")
sifa    = Entity(id="sifa",   name="Sifa Ostergard",     kind="agent")
kol     = Entity(id="kol",    name="Kol Grimsson",       kind="agent")
# Dead before the story opens; exists so the flashback and the creed have
# a referent.
ketil   = Entity(id="ketil",  name="Ketil the Measurer", kind="agent")

vastisetr = Entity(id="vastisetr", name="Vastisetr",             kind="location")
granary   = Entity(id="granary",   name="the common granary",    kind="location")
beehive   = Entity(id="beehive",   name="the Beehive alehouse",  kind="location")
skarn     = Entity(id="skarn",     name="the Skarn Pass",        kind="location")
hestfell  = Entity(id="hestfell",  name="Hestfell",              kind="location")

# The compact itself — equal shares off a true tally — as a referenceable
# thing, because the story is about ITS death, not any person's.
the_count  = Entity(id="the_count",  name="the count",           kind="abstract")
the_ledger = Entity(id="the_ledger", name="the Measurer's ledger", kind="object")

ENTITIES = [
    halla, eirik, jorunn, ragna, sifa, kol, ketil,
    vastisetr, granary, beehive, skarn, hestfell,
    the_count, the_ledger,
]

# The council / town as knowledge-holders — the named adults who vote.
TOWN_IDS = ("jorunn", "kol", "ragna")


# ----------------------------------------------------------------------------
# Branches — canonical only
# ----------------------------------------------------------------------------

ALL_BRANCHES = {
    CANONICAL_LABEL: CANONICAL,
}


# ----------------------------------------------------------------------------
# Proposition constructors
# ----------------------------------------------------------------------------

def broke_the_count(who: str) -> Prop:
    return Prop("broke_the_count", (who,))

def exiled_onto_ice(who: str) -> Prop:
    return Prop("exiled_onto_ice", (who,))

def pass_sealed(which: str) -> Prop:
    return Prop("pass_sealed", (which,))

def stores_enough(store: str) -> Prop:
    """The published tally clears the winter — the town's load-bearing
    belief, and (after E_rot_found) a false one."""
    return Prop("stores_enough", (store,))

def rot(store: str) -> Prop:
    return Prop("rot", (store,))

def ledger_false(ledger: str) -> Prop:
    return Prop("ledger_false", (ledger,))

def advance_refused(measurer: str, house: str) -> Prop:
    return Prop("advance_refused", (measurer, house))

def chit_forged(who: str) -> Prop:
    return Prop("chit_forged", (who,))

def dark_grain(house: str) -> Prop:
    """Grain moving outside the tally."""
    return Prop("dark_grain", (house,))

def books_short(ledger: str) -> Prop:
    return Prop("books_short", (ledger,))

def dead(who: str) -> Prop:
    return Prop("dead", (who,))

def crossing_rejected(to_where: str) -> Prop:
    return Prop("crossing_rejected", (to_where,))

def count_sworn_true(by_whom: str) -> Prop:
    return Prop("count_sworn_true", (by_whom,))

def rations_cut(store: str) -> Prop:
    return Prop("rations_cut", (store,))

def truth_public(what: str) -> Prop:
    return Prop("truth_public", (what,))

def compact_dead(compact: str) -> Prop:
    return Prop("compact_dead", (compact,))

def burned(place: str) -> Prop:
    return Prop("burned", (place,))

def gone_over_ice(who: str) -> Prop:
    return Prop("gone_over_ice", (who,))

def pass_open(which: str) -> Prop:
    return Prop("pass_open", (which,))

def keeps_count_of_dead(who: str) -> Prop:
    return Prop("keeps_count_of_dead", (who,))


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


def told(agent_id: str, p: Prop, τ: int,
         confidence: Confidence = Confidence.CERTAIN,
         slot: Slot = Slot.KNOWN, note: str = "") -> KnowledgeEffect:
    return observe(agent_id, p, τ, confidence=confidence, slot=slot,
                   note=note, via=Diegetic.UTTERANCE_HEARD.value)


def world(p: Prop, asserts: bool = True) -> WorldEffect:
    return WorldEffect(prop=p, asserts=asserts)


# ----------------------------------------------------------------------------
# Fabula — all events on :canonical, status=committed
# ----------------------------------------------------------------------------
#
# τ_s scale: days from the early freeze (τ_s=0). Ketil's fall is twenty
# years back at τ_s=-7300. The thaw lands at τ_s=95. Ordinal, not metric.

FABULA = [

    # --- Pre-plot (τ_s < 0) — the creed's origin; staged mid-story ---

    Event(
        id="E_ketil_fall",
        type="judgment",
        τ_s=-7300, τ_a=1,
        participants={"condemned": "ketil", "daughter": "halla",
                      "son": "eirik", "place": "vastisetr"},
        effects=(
            # The hunger year of their childhood: Ketil the Measurer was
            # caught giving hidden weight to the houses he favored. The
            # town weighed him by his own ledger and put him out onto the
            # winter ice. Halla, twelve, held Eirik, seven, and watched.
            # Everything she is, is this event; everything he is, is
            # watching her become it.
            world(broke_the_count("ketil")),
            world(exiled_onto_ice("ketil")),
            world(dead("ketil")),
            observe("halla", broke_the_count("ketil"), -7300,
                    note="watched the weighing; twelve years old"),
            observe("eirik", broke_the_count("ketil"), -7300,
                    note="seven; remembers the crowd's sound, not the scale"),
            observe("halla", exiled_onto_ice("ketil"), -7300),
            observe("eirik", exiled_onto_ice("ketil"), -7300),
            observe("jorunn", broke_the_count("ketil"), -7300,
                    note="young then; spoke the sentence's law"),
        ),
    ),

    # --- Act 1 — the present: freeze, count, rot, lie (τ_s 0-9) ---

    Event(
        id="E_hard_freeze",
        type="onset",
        τ_s=0, τ_a=2,
        participants={"town": "vastisetr", "pass": "skarn"},
        effects=(
            # Winter a month early; the Skarn Pass closes behind the last
            # sledge. The stores were laid for a NORMAL winter. From here
            # to thaw, Vastisetr is a sealed room.
            world(pass_sealed("skarn")),
            observe("halla", pass_sealed("skarn"), 0),
            observe("eirik", pass_sealed("skarn"), 0),
            observe("jorunn", pass_sealed("skarn"), 0),
            observe("kol", pass_sealed("skarn"), 0),
            observe("ragna", pass_sealed("skarn"), 0),
        ),
    ),

    Event(
        id="E_public_count",
        type="ceremony",
        τ_s=2, τ_a=3,
        participants={"measurer": "halla", "store": "granary",
                      "town": "vastisetr", "ledger": "the_ledger"},
        effects=(
            # The public count: sacks tallied aloud, the ledger open on
            # the granary steps for any eye. The number clears the winter
            # with nothing to spare. The town believes it because the
            # Measurer's count has never been wrong — trust in HER is the
            # town's entire epistemology, which is exactly what makes the
            # later lie structural rather than personal.
            world(stores_enough("granary")),
            observe("halla", stores_enough("granary"), 2,
                    note="her own tally, sack by sack"),
            told("jorunn", stores_enough("granary"), 2,
                 note="the public count, from the Measurer's mouth"),
            told("kol", stores_enough("granary"), 2),
            told("ragna", stores_enough("granary"), 2),
            told("eirik", stores_enough("granary"), 2),
        ),
    ),

    Event(
        id="E_rot_found",
        type="discovery",
        τ_s=5, τ_a=4,
        participants={"measurer": "halla", "store": "granary"},
        effects=(
            # Alone, by lantern, in the deep bins: blight. A third of the
            # store is black and sweet-smelling under sound grain. The
            # WORLD now contradicts the town's held belief — and exactly
            # one mind knows it. This is the scene the whole dread runway
            # hangs from.
            world(rot("granary")),
            world(stores_enough("granary"), asserts=False),
            observe("halla", rot("granary"), 5,
                    note="deep bins, lantern light, her hands in it"),
        ),
    ),

    Event(
        id="E_the_lie",
        type="decision",
        τ_s=6, τ_a=5,
        participants={"measurer": "halla", "ledger": "the_ledger",
                      "store": "granary"},
        effects=(
            # The first driver decision. She seals the deep bins, and the
            # ledger keeps the published total — "until she can be sure,"
            # she tells herself, and knows as she writes that it is not
            # true. Panic, she reasons, kills faster than hunger; the
            # count is the only wall. Her father broke the count for
            # favor. She breaks it for the town. The ledger cannot tell
            # the difference.
            world(ledger_false("the_ledger")),
            observe("halla", ledger_false("the_ledger"), 6,
                    via=Diegetic.REALIZATION.value,
                    note="her own hand on the page; she names it to herself"),
        ),
    ),

    Event(
        id="E_eirik_asks",
        type="refusal",
        τ_s=9, τ_a=6,
        participants={"keeper": "eirik", "measurer": "halla",
                      "house": "ragna"},
        effects=(
            # At the Beehive after close: Eirik asks an advance ration
            # for the Ostergards — Ragna's children are fevered and thin.
            # Halla refuses: equal shares off the tally; the count does
            # not know a sick child from a well one. The inverted
            # save-the-cat beat, played in full view.
            world(advance_refused("halla", "ragna")),
            told("eirik", advance_refused("halla", "ragna"), 9,
                 note="'the count does not bend' — her exact words"),
            told("ragna", advance_refused("halla", "ragna"), 10,
                 note="Eirik brings the refusal back gently, and it is "
                      "still the refusal"),
        ),
    ),

    # --- Act 2 — the future argued and foreclosed (τ_s 12-30) ---

    Event(
        id="E_forged_chit",
        type="deception",
        τ_s=12, τ_a=7,
        participants={"forger": "eirik", "house": "ragna",
                      "store": "granary"},
        effects=(
            # Eirik draws the Measurer's mark better than she draws it —
            # he has watched her hand since he was seven. Two sacks move
            # to the Ostergards under a forged chit. Ragna takes them as
            # a lawful mercy-draw; only Eirik knows otherwise.
            world(chit_forged("eirik")),
            world(dark_grain("ragna")),
            observe("eirik", chit_forged("eirik"), 12,
                    note="his own hand, her mark"),
            told("ragna", dark_grain("ragna"), 12,
                 confidence=Confidence.BELIEVED, slot=Slot.BELIEVED,
                 note="believes it a lawful mercy-draw signed by the "
                      "Measurer"),
        ),
    ),

    Event(
        id="E_shortfall",
        type="discovery",
        τ_s=19, τ_a=8,
        participants={"measurer": "halla", "ledger": "the_ledger"},
        effects=(
            # Weekly reconciliation: the books are short two sacks against
            # a chit she never cut. She knows the hand that could have
            # done it — one suspicion, not yet certainty. And she cannot
            # cry thief: an audit opens the deep bins, and the deep bins
            # open HER. The knowledge-lock closes: her lie is now the
            # roof his theft shelters under.
            world(books_short("the_ledger")),
            observe("halla", books_short("the_ledger"), 19,
                    note="two sacks, one chit she never cut"),
            observe("halla", chit_forged("eirik"), 19,
                    confidence=Confidence.SUSPECTED, slot=Slot.SUSPECTED,
                    via=Diegetic.INFERENCE.value,
                    note="who else draws her mark true enough to pass?"),
        ),
    ),

    Event(
        id="E_sifa_dies",
        type="death",
        τ_s=26, τ_a=9,
        participants={"child": "sifa", "mother": "ragna",
                      "keeper": "eirik"},
        effects=(
            # The fever takes Sifa with grain in the house — the stolen
            # sacks bought nothing but a fed child dying warm. The town
            # reads it on the honest arithmetic it holds: the Measurer's
            # hard shares starve children. They are wrong about the
            # mechanism and right about the woman, which is worse.
            world(dead("sifa")),
            observe("ragna", dead("sifa"), 26),
            told("eirik", dead("sifa"), 26,
                 note="he carried the sacks; he counts them now against "
                      "one small weight"),
            told("halla", dead("sifa"), 27),
            told("jorunn", dead("sifa"), 27),
            told("kol", dead("sifa"), 27),
        ),
    ),

    Event(
        id="E_pass_vote",
        type="decision",
        τ_s=30, τ_a=10,
        participants={"lawspeaker": "jorunn", "measurer": "halla",
                      "hunter": "kol", "place": "beehive"},
        effects=(
            # THE HINGE. Council at the Beehive: Jorunn proposes a
            # crossing party to Hestfell while the high snow will still
            # bear sledges — grain against spring debt, medicine, six
            # strong men risked. On the PUBLISHED count the risk is
            # needless; on the TRUE count it is the town's one exit.
            # Jorunn asks the only question that matters, point-blank:
            # "Does the count hold, Measurer?" Halla — who alone in the
            # room knows — says the ledger is true. The vote follows the
            # number; the number is hers; the one door out closes with
            # a sound like a page turning. Every voter reasons CORRECTLY
            # from what they hold. That is the whole tragedy, in one
            # scene, and the substrate can prove it.
            world(count_sworn_true("halla")),
            world(crossing_rejected("hestfell")),
            told("jorunn", stores_enough("granary"), 30,
                 note="sworn to the council by the Measurer herself"),
            told("kol", stores_enough("granary"), 30),
            told("ragna", stores_enough("granary"), 30),
            observe("halla", crossing_rejected("hestfell"), 30,
                    note="she watched her own number close the door"),
            observe("eirik", count_sworn_true("halla"), 30,
                    note="watches his sister swear; files the ring of it — "
                         "something under the words"),
        ),
    ),

    # --- Act 3 — everything visibly changing (τ_s 40-47) ---

    Event(
        id="E_rations_cut",
        type="decision",
        τ_s=40, τ_a=11,
        participants={"measurer": "halla", "store": "granary",
                      "town": "vastisetr"},
        effects=(
            # She cuts the ration a fifth, "prudence against a long
            # thaw." The town does the arithmetic she taught it: a true
            # count does not need prudence. Fear moves into the space
            # where trust lived. Hunger begins in earnest — real hunger,
            # the kind with a sound.
            world(rations_cut("granary")),
            told("jorunn", rations_cut("granary"), 40,
                 note="'prudence' — but a true count needs none, and "
                      "Jorunn has kept law long enough to hear a seam"),
            told("kol", rations_cut("granary"), 40),
            told("ragna", rations_cut("granary"), 40),
            told("eirik", rations_cut("granary"), 40),
        ),
    ),

    Event(
        id="E_confession",
        type="revelation",
        τ_s=44, τ_a=12,
        participants={"keeper": "eirik", "measurer": "halla",
                      "place": "granary"},
        effects=(
            # Eirik comes to confess the chit — you swore the count held,
            # so my two sacks matter, take them out of my share. And
            # Halla, worn past cunning, says: "I know. I've known since
            # the reconciliation." He does the arithmetic on her silence
            # in front of her — a Measurer who catches a forged chit and
            # says NOTHING has a reason to fear an audit — and pulls the
            # rot out of her in three questions. Two people now hold the
            # truth, roped together by what each could do to the other.
            world(Prop("secrets_mutual", ("halla", "eirik"))),
            observe("halla", chit_forged("eirik"), 44,
                    note="his confession makes the suspicion certain"),
            observe("eirik", ledger_false("the_ledger"), 44,
                    via=Diegetic.INFERENCE.value,
                    note="deduced from her silence about the chit, then "
                         "said aloud and not denied"),
            observe("eirik", rot("granary"), 44,
                    via=Diegetic.UTTERANCE_HEARD.value,
                    note="she opens the deep bins and shows him"),
        ),
    ),

    Event(
        id="E_ultimatum",
        type="confrontation",
        τ_s=47, τ_a=13,
        participants={"keeper": "eirik", "measurer": "halla"},
        effects=(
            # Eirik: tell them, or I will. People are deciding — who
            # eats, who mends, who prays — on a number you know is false.
            # Halla, steadfast, with the whole cold engine of her creed:
            # the truth now buys nothing but panic; the count is the last
            # wall; father broke it for favor, I am HOLDING it. Eirik:
            # "You are holding the ledger. The count died at the vote."
            # Neither yields. This is the scene where the reader wants
            # her to change, and she does not, because she is who the
            # first scene made her.
            world(Prop("ultimatum", ("eirik", "halla"))),
            told("halla", Prop("ultimatum", ("eirik", "halla")), 47,
                 note="three days, sister"),
        ),
    ),

    # --- Act 4 — the past arrives; the reckoning (τ_s 50-95) ---

    Event(
        id="E_eirik_tells",
        type="revelation",
        τ_s=50, τ_a=14,
        participants={"keeper": "eirik", "lawspeaker": "jorunn",
                      "hunter": "kol", "place": "beehive"},
        effects=(
            # Eirik stands up at the Beehive — his own house, his own
            # taproom — and tells it all: the rot, the false total, the
            # sworn count at the vote, his own forged chit first so no
            # one can say he spared himself. The authority of the count
            # does not survive the hour. Not because of the rot: because
            # of the lie. A town can forgive a short store; it cannot
            # forgive discovering its arithmetic was performed.
            world(truth_public("ledger_false")),
            world(compact_dead("the_count")),
            told("jorunn", rot("granary"), 50),
            told("jorunn", ledger_false("the_ledger"), 50),
            told("kol", rot("granary"), 50),
            told("kol", ledger_false("the_ledger"), 50),
            told("ragna", ledger_false("the_ledger"), 51,
                 note="and understands, coldly, whose mark fed her "
                      "children and whose word buried one"),
            observe("eirik", compact_dead("the_count"), 50,
                    via=Diegetic.REALIZATION.value,
                    note="he watches it die as he speaks and finishes "
                         "speaking anyway"),
        ),
    ),

    Event(
        id="E_the_breaking",
        type="catastrophe",
        τ_s=51, τ_a=15,
        participants={"hunter": "kol", "keeper": "eirik",
                      "store": "granary", "town": "vastisetr"},
        effects=(
            # The night after: with the compact dead, shares are just
            # sacks and sacks belong to the strong. Kol comes for the
            # granary with torches for light and men for weight. Eirik —
            # done forever with counts, cheated by one and orphaned by
            # another — throws the doors open himself: better handed out
            # than fought over. It is neither. In the scramble a lamp
            # goes into the chaff, and what the rot left, the fire takes.
            world(burned("granary")),
            world(dead("kol"), asserts=False),  # wounded in the crush, lives
            observe("halla", burned("granary"), 51,
                    note="she carries the ledger out; it is what her "
                         "hands took"),
            observe("eirik", burned("granary"), 51),
            observe("jorunn", burned("granary"), 51),
            observe("kol", burned("granary"), 51),
            observe("ragna", burned("granary"), 51),
        ),
    ),

    Event(
        id="E_dying_weeks",
        type="aftermath",
        τ_s=60, τ_a=16,
        participants={"measurer": "halla", "keeper": "eirik",
                      "town": "vastisetr", "pass": "skarn"},
        effects=(
            # The silent weeks. What was not burned is hoarded behind
            # doors; the old share-lines are teeth-lines now. The hungry
            # dead begin, and Halla — nothing left to measure — opens the
            # ledger's back pages and keeps the only count remaining.
            # Eirik packs for the Skarn Pass in the worst month: if no
            # help was sent for, he will BE the sending, forty years too
            # stubborn, exactly his sister's brother. She does not stop
            # him. Neither says what both hold: that this is the other
            # exile, re-run, and she is the town that lets him walk onto
            # the ice.
            world(gone_over_ice("eirik")),
            world(keeps_count_of_dead("halla")),
            observe("halla", gone_over_ice("eirik"), 60,
                    note="she watched him past the cairns until the light "
                         "failed"),
            told("jorunn", gone_over_ice("eirik"), 61),
        ),
    ),

    Event(
        id="E_thaw",
        type="reckoning",
        τ_s=95, τ_a=17,
        participants={"measurer": "halla", "lawspeaker": "jorunn",
                      "pass": "skarn", "town": "vastisetr"},
        effects=(
            # The pass opens. Hestfell traders come up the thaw road to
            # sell to a town that is mostly doors nailed shut. They carry
            # something down from the high cairns wrapped in sail-cloth:
            # the ice gave Eirik back, a day short of the summit. Halla
            # sits at her table in the cold granary office and enters the
            # last names in a straight column — Eirik Ketilsson, keeper,
            # the Beehive — and rules the line, and squares the book.
            # The count is perfect now. It counts the dead.
            world(pass_open("skarn")),
            world(dead("eirik")),
            told("halla", dead("eirik"), 95,
                 note="the traders' foreman, cap in hand, not knowing "
                      "who she is to the name"),
            told("jorunn", dead("eirik"), 95),
            observe("halla", keeps_count_of_dead("halla"), 95,
                    via=Diegetic.REALIZATION.value,
                    note="the ledger balances for the first time since "
                         "the deep bins — and she understands what her "
                         "steadfastness has purchased, and holds it "
                         "anyway, because it is all that is left"),
        ),
    ),
]


# ----------------------------------------------------------------------------
# Sjuzhet — chronological, EXCEPT the flashback: Ketil's fall is staged
# fifth, immediately after the lie, so the reader learns why the lie is
# unthinkable in the same hour they watch her tell it.
# ----------------------------------------------------------------------------

SJUZHET = [
    SjuzhetEntry(event_id="E_hard_freeze",   τ_d=0, focalizer_id="halla"),
    SjuzhetEntry(event_id="E_public_count",  τ_d=1, focalizer_id="halla"),
    SjuzhetEntry(event_id="E_rot_found",     τ_d=2, focalizer_id="halla"),
    SjuzhetEntry(event_id="E_the_lie",       τ_d=3, focalizer_id="halla"),

    # The flashback. Focalized through Halla — this is memory, not
    # narration; the disclosures put the creed's origin into the reader.
    SjuzhetEntry(
        event_id="E_ketil_fall", τ_d=4, focalizer_id="halla",
        disclosures=(
            Disclosure(prop=broke_the_count("ketil"), slot=Slot.KNOWN,
                       confidence=Confidence.CERTAIN,
                       via=Narrative.DISCLOSURE.value),
            Disclosure(prop=exiled_onto_ice("ketil"), slot=Slot.KNOWN,
                       confidence=Confidence.CERTAIN,
                       via=Narrative.DISCLOSURE.value),
        ),
    ),

    SjuzhetEntry(event_id="E_eirik_asks",    τ_d=5,  focalizer_id="eirik"),
    SjuzhetEntry(event_id="E_forged_chit",   τ_d=6,  focalizer_id="eirik"),
    SjuzhetEntry(event_id="E_shortfall",     τ_d=7,  focalizer_id="halla"),
    SjuzhetEntry(event_id="E_sifa_dies",     τ_d=8,  focalizer_id="ragna"),
    SjuzhetEntry(event_id="E_pass_vote",     τ_d=9,  focalizer_id="halla"),
    SjuzhetEntry(event_id="E_rations_cut",   τ_d=10, focalizer_id="halla"),
    SjuzhetEntry(event_id="E_confession",    τ_d=11, focalizer_id="eirik"),
    SjuzhetEntry(event_id="E_ultimatum",     τ_d=12, focalizer_id="halla"),
    SjuzhetEntry(event_id="E_eirik_tells",   τ_d=13, focalizer_id="eirik"),
    SjuzhetEntry(event_id="E_the_breaking",  τ_d=14, focalizer_id="halla"),
    SjuzhetEntry(event_id="E_dying_weeks",   τ_d=15, focalizer_id="halla"),
    SjuzhetEntry(event_id="E_thaw",          τ_d=16, focalizer_id="halla"),
]

# ----------------------------------------------------------------------------
# Descriptions — one scene-note per event: the dramatic texture the facts
# alone don't carry. These render into the per-scene briefs as authorial
# notes.
# ----------------------------------------------------------------------------

def _note(n: int, event_id: str, text: str) -> Description:
    return Description(
        id=f"D_wc_{event_id[2:]}", attached_to=anchor_event(event_id),
        kind="texture", attention=Attention.INTERPRETIVE,
        text=text, authored_by="author", τ_a=100 + n,
    )

DESCRIPTIONS = (
    _note(1, "E_ketil_fall",
          "Memory, not narration: Halla is twelve, holding Eirik, seven. "
          "Ketil weighed by his own ledger before the assembled town and "
          "put out onto the winter ice for giving hidden weight to the "
          "houses he favored. Render the crowd as a sound, the scale as "
          "the only clear image, and the lesson as it enters the child: "
          "the count is what keeps love from becoming theft. Jorunn, "
          "young then, speaks the law. This is the creed's forge — and "
          "staged HERE, right after the lie, it must cut both ways: the "
          "reader sees why the lie is unthinkable in the same hour they "
          "watched her tell it."),
    _note(2, "E_hard_freeze",
          "Winter arrives a month early; the Skarn Pass closes behind "
          "the last sledge like a door being locked from outside. Open "
          "on work, not weather-poetry: Halla moving through the town "
          "doing sums — hides, fish-racks, wood-cords, mouths. The cold "
          "is a fact among facts. End on the granary: the stores were "
          "laid for a normal winter."),
    _note(3, "E_public_count",
          "The public count is Vastisetr's high ceremony: sacks tallied "
          "aloud on the granary steps, the ledger open for any eye, "
          "children on shoulders to watch the Measurer work. The number "
          "clears the winter with nothing to spare — she says so "
          "plainly, and the town exhales. Their trust in her IS the "
          "town's epistemology; make the reader feel how good it is, "
          "because every later horror is this scene inverted."),
    _note(4, "E_rot_found",
          "Alone, by lantern, in the deep bins: blight — black, sweet-"
          "smelling, a third of the store gone under sound grain. No "
          "witness, no counsel, the lantern hissing. She does the "
          "arithmetic three times because the first two must be wrong. "
          "The scene ends before she decides anything: just the number, "
          "and her hands in the ruined grain."),
    _note(5, "E_the_lie",
          "The hinge of her soul, played small: a woman at a desk, "
          "sealing the deep bins, entering the OLD total in her own "
          "steady hand. 'Until I can be sure' — and she knows as she "
          "writes it that it is not true. Her reasoning must be shown "
          "and must be GOOD: panic kills faster than hunger; the count "
          "is the only wall. Father broke the count for favor; she "
          "breaks it for the town; the ledger cannot tell the "
          "difference. No music. The scratch of the pen."),
    _note(6, "E_eirik_asks",
          "The Beehive after close, chairs up, one lamp. Eirik asks an "
          "advance for the Ostergards — Ragna's children fevered and "
          "thin. Halla refuses: equal shares off the tally; the count "
          "does not know a sick child from a well one. THE INVERTED "
          "SAVE-THE-CAT: her first significant act on the page is "
          "refusing a starving family, and her reasons must be exactly "
          "her creed, delivered without cruelty — which is worse. Eirik "
          "watches his sister and starts, quietly, to conceive."),
    _note(7, "E_forged_chit",
          "Eirik draws the Measurer's mark better than she draws it — "
          "he has watched her hand since he was seven. Two sacks move "
          "in the dark to the Ostergards under a forged chit; Ragna "
          "receives them as lawful mercy, signed. Render the forgery "
          "with craft-love and dread: mercy wearing a stolen mark. His "
          "guilt is real and he does it anyway; that is the whole man."),
    _note(8, "E_shortfall",
          "Weekly reconciliation: two sacks short against a chit she "
          "never cut. She knows within a page whose hand could pass her "
          "mark. And the trap closes with a click the reader must hear: "
          "she cannot cry thief — an audit opens the deep bins, and the "
          "deep bins open HER. Her lie is now the roof his theft "
          "shelters under. She closes the ledger and says nothing. "
          "Sibling secrets, mutually hostage."),
    _note(9, "E_sifa_dies",
          "Focalized through Ragna. The fever takes Sifa with grain in "
          "the house — the stolen sacks bought a fed child dying warm, "
          "nothing more. No villain in the room; that is the point. The "
          "town, reasoning honestly on what it holds, reads it as the "
          "Measurer's hard shares starving children — wrong about the "
          "mechanism, right about the woman, and the wrongness of the "
          "whisper must not comfort anyone. Small coffin, frozen "
          "ground, iron."),
    _note(10, "E_pass_vote",
          "THE HINGE OF THE STORY. Council at the Beehive: Jorunn "
          "proposes a crossing to Hestfell while the high snow will "
          "still bear sledges — grain against spring debt, six strong "
          "men risked. On the published count the risk is needless; on "
          "the true count it is the town's one exit; one person in the "
          "room knows which count is real. Jorunn asks point-blank: "
          "'Does the count hold, Measurer?' The reflex answer — 'The "
          "count holds' — must land like a page turning, not thunder. "
          "EVERY voter reasons correctly from what they hold; the vote "
          "is rational; the door closes. The horror is arithmetic."),
    _note(11, "E_rations_cut",
          "She cuts the ration a fifth — 'prudence against a long "
          "thaw.' The town does the sums she taught it to do: a true "
          "count needs no prudence. Trust curdles into watching. "
          "Hunger begins in earnest, the kind with a sound. Jorunn "
          "hears the seam in 'prudence' and files it, lawspeaker-wise, "
          "saying nothing yet."),
    _note(12, "E_confession",
          "The granary office, cold enough to see breath. Eirik comes "
          "to confess the chit — take it out of my share, you swore the "
          "count held. And Halla, worn past cunning: 'I know. I've "
          "known since the reconciliation.' He does the arithmetic on "
          "her silence IN FRONT of her — a Measurer who catches a "
          "forgery and says nothing fears an audit — and pulls the rot "
          "out of her in three questions. Then she opens the deep bins "
          "and shows him. Two minds, one truth, roped together by what "
          "each could do to the other. The closest scene to love in "
          "the story."),
    _note(13, "E_ultimatum",
          "Eirik: tell them, or I will — people are deciding who eats "
          "on a number you know is false. Halla, steadfast, the whole "
          "cold engine of the creed: truth now buys nothing but panic; "
          "the count is the last wall; father broke it for favor, I am "
          "HOLDING it. Eirik: 'You are holding the ledger. The count "
          "died at the vote.' Neither yields. This is the scene where "
          "the reader begs her to change, and she does not, because "
          "she is who the flashback made her. Three days, sister."),
    _note(14, "E_eirik_tells",
          "Eirik stands up in his own taproom and tells it all — his "
          "forged chit FIRST, so no one can say he spared himself, then "
          "the rot, the false total, the sworn count at the vote. The "
          "authority of the count does not survive the hour. Not "
          "because of the rot — a town can forgive a short store — but "
          "because its arithmetic was performed. Render the room's "
          "silence as the compact dying; Halla is not present, and her "
          "absence is a presence."),
    _note(15, "E_the_breaking",
          "The night after: shares are just sacks now, and sacks belong "
          "to the strong. Kol comes for the granary with torches and "
          "men; Eirik — done forever with counts — throws the doors "
          "open himself: better handed out than fought over. It is "
          "neither. A lamp goes into the chaff in the scramble, and "
          "what the rot left, the fire takes. Halla walks INTO the "
          "burning granary and comes out carrying the ledger — let the "
          "image state the indictment; no one needs to speak it."),
    _note(16, "E_dying_weeks",
          "The silent weeks. Doors nailed, share-lines become teeth-"
          "lines, the hungry dead begin. Halla opens the ledger's back "
          "pages and keeps the only count remaining. Eirik packs for "
          "the Skarn Pass in the worst month — if no help was sent for, "
          "he will BE the sending. She does not stop him. Neither says "
          "what both hold: this is the other exile re-run, and she is "
          "the town letting him walk onto the ice. The relationship's "
          "last transaction is silence."),
    _note(17, "E_thaw",
          "Spring, administratively. The pass opens; Hestfell traders "
          "come up the thaw road to a town that is mostly nailed doors, "
          "and carry something down from the high cairns wrapped in "
          "sail-cloth — the ice gives Eirik back a day short of the "
          "summit. The foreman, cap in hand, does not know who the name "
          "is to her. Halla at her table enters the last names in a "
          "straight column — Eirik Ketilsson, keeper, the Beehive — "
          "rules the line, squares the book. The count is perfect now; "
          "it counts the dead. Close the loop of the opening: a woman "
          "at a table, counting. NO CONSOLATION: no tear, no lesson, "
          "no spring warmth allowed into the prose. Judgment: bad."),
)

PREPLAY_DISCLOSURES = ()
