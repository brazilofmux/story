"""
oedipus_lowerings.py — first authored Lowering bindings: Oedipus
Dramatic ↔ substrate.

This module is the project's first cross-dialect connection in code.
It imports from substrate.py + oedipus.py + dramatic.py +
oedipus_dramatic.py simultaneously, and it imports lowering.py for
the binding records themselves.

Per architecture-sketch-02 A6, dialects stand alone; this module is
the *connective tissue* that A7 (lowering is author-driven) names —
authored bindings that say "this Dramatic record is realized by this
substrate record (or set)". The pattern parallels how a build system
links separately-compiled modules: each dialect compiles standalone,
then explicit linkage records say what realizes what.

Scope of this first set:

- Character → Entity (1-to-1 Realization). Four active Lowerings for
  Characters with substrate counterparts (Oedipus, Jocasta, Shepherd,
  Messenger), two PENDING Lowerings for the Characters that
  oedipus.py cuts (Tiresias, Creon).
- Scene → Event(s) (1-to-many Realization). Four active Lowerings
  for Scenes whose substrate events exist (S_anagnorisis,
  S_messenger_arrives, S_jocasta_realizes, S_shepherd_testimony,
  S_jocasta_doubt_speech), four PENDING Lowerings for Scenes whose
  substrate events are missing (S_tiresias_accusation,
  S_jocasta_hangs, S_self_blinding, S_exile, S_prologue_plague,
  S_discovery_and_crown — these are gaps lowering-sketch-01's F5
  identified).
- One Throughline → set-of-events Lowering with a position_range,
  demonstrating the L7 position-correspondence mechanic on a
  substrate range (τ_s for fabula or τ_d for sjuzhet).

Most Lowerings have anchor_τ_a set from the substrate side. Entities
have no τ_a in this substrate (they're not authored events), so
Character → Entity Lowerings have anchor_τ_a=None — staleness is
undefined for those. Scene → Event Lowerings can compute anchor_τ_a
from the event's τ_a.

Coupling kinds across this set: every Lowering here is Realization
(per L1, the only kind Lowering records carry). Characterization
couplings (e.g., a Throughline's Domain assignment) and Claim
couplings (e.g., the Argument's resolution_direction) live in the
verifier surface and do not appear as Lowerings.
"""

from __future__ import annotations

# Substrate-side imports. Used to look up records the Lowerings
# reference and to compute anchor_τ_a from event τ_a values.
from substrate import Entity, Event
from oedipus import (
    FABULA,
    ENTITIES,
    DESCRIPTIONS as OEDIPUS_SUBSTRATE_DESCRIPTIONS,
)

# Dramatic-side imports. Used to identify the upper-side records
# (Characters, Scenes, Throughlines) the Lowerings reference.
from dramatic import Story, Character, Scene, Throughline
from oedipus_dramatic import (
    STORY,
    CHARACTERS,
    SCENES,
    THROUGHLINES,
    BEATS,
)

# Lowering-record machinery.
from lowering import (
    Lowering, CrossDialectRef, cross_ref,
    Annotation, AnnotationReview, PositionRange,
    LoweringStatus,
    ATTENTION_STRUCTURAL, ATTENTION_INTERPRETIVE,
)


# ============================================================================
# Helpers
# ============================================================================


def _substrate_event(event_id: str) -> Event:
    """Look up a substrate Event by id, or raise."""
    for e in FABULA:
        if e.id == event_id:
            return e
    raise KeyError(f"no substrate event with id {event_id!r}")


def _substrate_entity(entity_id: str) -> Entity:
    """Look up a substrate Entity by id, or raise."""
    for e in ENTITIES:
        if e.id == entity_id:
            return e
    raise KeyError(f"no substrate entity with id {entity_id!r}")


def _max_event_τ_a(*event_ids: str) -> int:
    """Compute max τ_a across the given event ids. Used to set
    anchor_τ_a on Lowerings whose lower side is one or more events."""
    return max(_substrate_event(eid).τ_a for eid in event_ids)


# Convenience: shorthand for cross_refs to the two dialects we use.

def _dramatic(record_id: str) -> CrossDialectRef:
    return cross_ref("dramatic", record_id)


def _substrate(record_id: str) -> CrossDialectRef:
    return cross_ref("substrate", record_id)


# ============================================================================
# Character → Entity Lowerings (1-to-1)
# ============================================================================
#
# Four Characters whose substrate Entities exist; two Characters
# (Tiresias, Creon) that the substrate slice cuts. Anchor_τ_a is
# None for all six because substrate Entities have no τ_a.

L_oedipus = Lowering(
    id="L_oedipus",
    upper_record=_dramatic("C_oedipus"),
    lower_records=(_substrate("oedipus"),),
    annotation=Annotation(
        text=("Dramatic Character C_oedipus realizes as the substrate "
              "Entity 'oedipus' — same name, same role across both "
              "dialects. The Dramatic Character carries function "
              "labels (Protagonist + Emotion); those have no substrate "
              "counterpart and stay dialect-local."),
    ),
    τ_a=200,
)

L_jocasta = Lowering(
    id="L_jocasta",
    upper_record=_dramatic("C_jocasta"),
    lower_records=(_substrate("jocasta"),),
    annotation=Annotation(text="C_jocasta → Entity 'jocasta'."),
    τ_a=201,
)

L_shepherd = Lowering(
    id="L_shepherd",
    upper_record=_dramatic("C_shepherd"),
    lower_records=(_substrate("shepherd"),),
    annotation=Annotation(text="C_shepherd → Entity 'shepherd'."),
    τ_a=202,
)

L_messenger = Lowering(
    id="L_messenger",
    upper_record=_dramatic("C_messenger"),
    lower_records=(_substrate("messenger"),),
    annotation=Annotation(text="C_messenger → Entity 'messenger'."),
    τ_a=203,
)

L_tiresias_pending = Lowering(
    id="L_tiresias_pending",
    upper_record=_dramatic("C_tiresias"),
    lower_records=(),
    annotation=Annotation(
        text=("C_tiresias has no substrate Entity yet — oedipus.py's "
              "encoding cuts Tiresias for the identity-probe slice. "
              "The Lowering is PENDING; once the substrate is extended "
              "with a 'tiresias' Entity, this can flip to ACTIVE."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=204,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "substrate cuts Tiresias"},
)

L_creon_pending = Lowering(
    id="L_creon_pending",
    upper_record=_dramatic("C_creon"),
    lower_records=(),
    annotation=Annotation(
        text=("C_creon has no substrate Entity yet — same reason as "
              "Tiresias. PENDING until oedipus.py is extended."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=205,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "substrate cuts Creon"},
)


# ============================================================================
# Scene → Event(s) Lowerings (1-to-many)
# ============================================================================
#
# Some Dramatic Scenes have one substrate event; a couple have
# multiple. Several Scenes have no substrate event at all (the
# substrate's identity-probe slice cuts most of the post-anagnorisis
# play and the early prologue/coronation beats).

L_jocasta_doubt_speech = Lowering(
    id="L_jocasta_doubt_speech",
    upper_record=_dramatic("S_jocasta_doubt_speech"),
    lower_records=(_substrate("E_jocasta_mentions_crossroads"),),
    annotation=Annotation(
        text=("Dramatic Scene S_jocasta_doubt_speech (Jocasta tries to "
              "comfort Oedipus by dismissing prophecy; mentions the "
              "crossroads detail) realizes as substrate event "
              "E_jocasta_mentions_crossroads. The Dramatic Scene "
              "names the IC's first beat (B_ic_1) and the MC's first "
              "private dread (B_mc_3); the substrate event records the "
              "literal speech-act and its agent-knowledge effects on "
              "Oedipus."),
    ),
    τ_a=210,
    anchor_τ_a=_substrate_event("E_jocasta_mentions_crossroads").τ_a,
)

L_messenger_arrives = Lowering(
    id="L_messenger_arrives",
    upper_record=_dramatic("S_messenger_arrives"),
    lower_records=(
        _substrate("E_messenger_polybus_dead"),
        _substrate("E_messenger_adoption_reveal"),
    ),
    annotation=Annotation(
        text=("Dramatic Scene S_messenger_arrives (the messenger "
              "meaning-to-comfort reveals the Polybus-not-father "
              "fact) realizes as TWO substrate events — the messenger "
              "first announces Polybus's death, then makes the "
              "adoption reveal. The Scene bundles them as one unit "
              "of argumentative work; the substrate keeps them as "
              "two distinct events because their epistemic effects "
              "are distinct."),
    ),
    τ_a=211,
    anchor_τ_a=_max_event_τ_a(
        "E_messenger_polybus_dead", "E_messenger_adoption_reveal",
    ),
)

L_jocasta_realizes = Lowering(
    id="L_jocasta_realizes",
    upper_record=_dramatic("S_jocasta_realizes"),
    lower_records=(_substrate("E_jocasta_realizes"),),
    annotation=Annotation(
        text=("Dramatic Scene S_jocasta_realizes (her anagnorisis; "
              "she sees what Oedipus hasn't yet; she begs him to "
              "stop) realizes as substrate event E_jocasta_realizes. "
              "The substrate event carries her identity assertions "
              "and the dislodgement of her dead(the-exposed-baby) "
              "belief; the Scene names the dramatic shape these "
              "effects perform."),
    ),
    τ_a=212,
    anchor_τ_a=_substrate_event("E_jocasta_realizes").τ_a,
)

L_shepherd_testimony = Lowering(
    id="L_shepherd_testimony",
    upper_record=_dramatic("S_shepherd_testimony"),
    lower_records=(_substrate("E_shepherd_testimony"),),
    annotation=Annotation(
        text=("S_shepherd_testimony → E_shepherd_testimony. Direct "
              "1-to-1; the substrate event is the testimony; the "
              "Dramatic Scene is its argumentative role (the witness "
              "testimony that locks in the answer)."),
    ),
    τ_a=213,
    anchor_τ_a=_substrate_event("E_shepherd_testimony").τ_a,
)

L_anagnorisis = Lowering(
    id="L_anagnorisis",
    upper_record=_dramatic("S_anagnorisis"),
    lower_records=(_substrate("E_oedipus_anagnorisis"),),
    annotation=Annotation(
        text=("S_anagnorisis (Oedipus realizes; the Argument's "
              "premise lands in the MC's perception) realizes as "
              "substrate event E_oedipus_anagnorisis. This is the "
              "play's structural climax in both dialects."),
    ),
    τ_a=214,
    anchor_τ_a=_substrate_event("E_oedipus_anagnorisis").τ_a,
)


# Pending Lowerings — Dramatic Scenes whose substrate realization
# the substrate slice cuts. lowering-sketch-01 F5 named these as
# the canonical case for the PENDING status.

L_prologue_plague_pending = Lowering(
    id="L_prologue_plague_pending",
    upper_record=_dramatic("S_prologue_plague"),
    lower_records=(),
    annotation=Annotation(
        text=("S_prologue_plague (the city brings its suffering to "
              "the king; the king pledges investigation) has no "
              "substrate event — oedipus.py's slice begins at the "
              "central irony machinery and skips the plague-prologue. "
              "PENDING."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=220,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "substrate slice cuts the prologue"},
)

L_tiresias_accusation_pending = Lowering(
    id="L_tiresias_accusation_pending",
    upper_record=_dramatic("S_tiresias_accusation"),
    lower_records=(),
    annotation=Annotation(
        text=("S_tiresias_accusation has no substrate event — both "
              "Tiresias the character and the accusation event are "
              "cut from the substrate slice. PENDING until extension."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=221,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "substrate cuts Tiresias and the accusation"},
)

L_discovery_and_crown_pending = Lowering(
    id="L_discovery_and_crown_pending",
    upper_record=_dramatic("S_discovery_and_crown"),
    lower_records=(),
    annotation=Annotation(
        text=("Macbeth's S_discovery_and_crown analog doesn't exist "
              "in oedipus_dramatic; this Lowering corresponds to "
              "no Oedipus Scene and is pending only as a placeholder "
              "for the Oedipus-equivalent event flow that the "
              "substrate slice elides."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=222,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "no Oedipus Scene corresponds; placeholder"},
)

L_jocasta_hangs_pending = Lowering(
    id="L_jocasta_hangs_pending",
    upper_record=_dramatic("S_jocasta_hangs"),
    lower_records=(),
    annotation=Annotation(
        text=("S_jocasta_hangs has no substrate event — Jocasta's "
              "death is part of the post-anagnorisis play that the "
              "substrate slice cuts. PENDING."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=223,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "substrate cuts post-anagnorisis events"},
)

L_self_blinding_pending = Lowering(
    id="L_self_blinding_pending",
    upper_record=_dramatic("S_self_blinding"),
    lower_records=(),
    annotation=Annotation(
        text=("S_self_blinding has no substrate event — same reason "
              "as S_jocasta_hangs. PENDING."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=224,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "substrate cuts post-anagnorisis events"},
)

L_exile_pending = Lowering(
    id="L_exile_pending",
    upper_record=_dramatic("S_exile"),
    lower_records=(),
    annotation=Annotation(
        text=("S_exile has no substrate event. PENDING."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=225,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "substrate cuts post-anagnorisis events"},
)


# ============================================================================
# Throughline → many-events Lowering (with position_range)
# ============================================================================
#
# T_mc_oedipus realizes across Oedipus's substrate events from his
# birth through the anagnorisis — fabula τ_s ∈ [-100, 13]. The
# position_range expresses this directly.

L_mc_throughline = Lowering(
    id="L_mc_throughline",
    upper_record=_dramatic("T_mc_oedipus"),
    lower_records=(
        _substrate("E_birth"),
        _substrate("E_upbringing_in_corinth"),
        _substrate("E_oracle_to_oedipus"),
        _substrate("E_crossroads_killing"),
        _substrate("E_marriage_and_crown"),
        _substrate("E_jocasta_mentions_crossroads"),
        _substrate("E_messenger_polybus_dead"),
        _substrate("E_messenger_adoption_reveal"),
        _substrate("E_shepherd_testimony"),
        _substrate("E_oedipus_anagnorisis"),
    ),
    annotation=Annotation(
        text=("Dramatic Throughline T_mc_oedipus (the MC's epistemic "
              "descent from confident king to anagnorisis) realizes "
              "across the substrate events that define Oedipus's "
              "epistemic trajectory — birth and upbringing (background), "
              "oracle (the prophecy's plant), crossroads killing and "
              "marriage (the actions), then the in-play discovery "
              "events. The position_range frames this as fabula τ_s "
              "from -100 (birth) to 13 (anagnorisis). E_jocasta_realizes "
              "is omitted: that's Jocasta's anagnorisis, which "
              "advances T_impact_jocasta, not the MC's."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=230,
    position_range=PositionRange(coord="τ_s", min_value=-100, max_value=13),
    anchor_τ_a=_max_event_τ_a(
        "E_birth", "E_upbringing_in_corinth", "E_oracle_to_oedipus",
        "E_crossroads_killing", "E_marriage_and_crown",
        "E_jocasta_mentions_crossroads", "E_messenger_polybus_dead",
        "E_messenger_adoption_reveal", "E_shepherd_testimony",
        "E_oedipus_anagnorisis",
    ),
)


# ============================================================================
# Aggregate
# ============================================================================

LOWERINGS = (
    # Character → Entity (active + pending)
    L_oedipus, L_jocasta, L_shepherd, L_messenger,
    L_tiresias_pending, L_creon_pending,
    # Scene → Event(s) (active)
    L_jocasta_doubt_speech, L_messenger_arrives, L_jocasta_realizes,
    L_shepherd_testimony, L_anagnorisis,
    # Scene → no-substrate-event (pending)
    L_prologue_plague_pending, L_tiresias_accusation_pending,
    L_discovery_and_crown_pending, L_jocasta_hangs_pending,
    L_self_blinding_pending, L_exile_pending,
    # Throughline → many-events (with position_range)
    L_mc_throughline,
)
