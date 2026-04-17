"""
rocky_lowerings.py — Lowering bindings: Rocky Dramatic ↔ substrate.

Fourth *_lowerings.py after Oedipus / Macbeth / Ackroyd. Authored as
Phase 2 of the three-phase Rocky encoding, alongside
rocky_dramatica_complete_verification.py.

Scope (parallels oedipus_lowerings.py):

- Character → Entity (1-to-1): 10 active Lowerings for every
  rocky_dramatic Character with a rocky.py Entity counterpart.
- Scene → Event(s) (1-to-many): 11 active Lowerings for Scenes whose
  substrate events exist, 1 PENDING for S_ice_skating (the rink date
  is handled in prose / the rel-throughline at the dialect layer; no
  dedicated substrate event, by design — Rocky's rel-Throughline is
  description-carried).
- Throughline → many-events with position_range: T_mc_rocky realizes
  across Rocky's participation events from τ_s=0 (the Spider Rico
  club fight) through τ_s=57 (no rematch). Parallel to Oedipus's
  L_mc_throughline binding.

Coupling kinds: every Lowering is Realization (per L1). DSP and
Story-level Characterization / Claim couplings live in the verifier
surface (rocky_dramatica_complete_verification.py), not here.
"""

from __future__ import annotations

from substrate import Entity, Event
from rocky import (
    FABULA,
    ENTITIES,
    DESCRIPTIONS as ROCKY_SUBSTRATE_DESCRIPTIONS,
)

from dramatic import Story, Character, Scene, Throughline
from rocky_dramatic import (
    STORY,
    CHARACTERS,
    SCENES,
    THROUGHLINES,
    BEATS,
)

from lowering import (
    Lowering, CrossDialectRef, cross_ref,
    Annotation, PositionRange,
    LoweringStatus,
    ATTENTION_STRUCTURAL, ATTENTION_INTERPRETIVE,
)


# ============================================================================
# Helpers
# ============================================================================


def _substrate_event(event_id: str) -> Event:
    for e in FABULA:
        if e.id == event_id:
            return e
    raise KeyError(f"no substrate event with id {event_id!r}")


def _max_event_τ_a(*event_ids: str) -> int:
    return max(_substrate_event(eid).τ_a for eid in event_ids)


def _dramatic(record_id: str) -> CrossDialectRef:
    return cross_ref("dramatic", record_id)


def _substrate(record_id: str) -> CrossDialectRef:
    return cross_ref("substrate", record_id)


# ============================================================================
# Character → Entity Lowerings (1-to-1)
# ============================================================================

L_rocky = Lowering(
    id="L_rocky",
    upper_record=_dramatic("C_rocky"),
    lower_records=(_substrate("rocky"),),
    annotation=Annotation(
        text=("Dramatic Character C_rocky (Protagonist, MC Throughline "
              "owner) realizes as substrate Entity 'rocky'."),
    ),
    τ_a=300,
)

L_apollo = Lowering(
    id="L_apollo",
    upper_record=_dramatic("C_apollo"),
    lower_records=(_substrate("apollo"),),
    annotation=Annotation(
        text=("C_apollo (Antagonist, IC Throughline owner) → Entity "
              "'apollo'."),
    ),
    τ_a=301,
)

L_mickey = Lowering(
    id="L_mickey",
    upper_record=_dramatic("C_mickey"),
    lower_records=(_substrate("mickey"),),
    annotation=Annotation(text="C_mickey (Guardian) → Entity 'mickey'."),
    τ_a=302,
)

L_paulie = Lowering(
    id="L_paulie",
    upper_record=_dramatic("C_paulie"),
    lower_records=(_substrate("paulie"),),
    annotation=Annotation(text="C_paulie (Contagonist) → Entity 'paulie'."),
    τ_a=303,
)

L_adrian = Lowering(
    id="L_adrian",
    upper_record=_dramatic("C_adrian"),
    lower_records=(_substrate("adrian"),),
    annotation=Annotation(text="C_adrian (Emotion) → Entity 'adrian'."),
    τ_a=304,
)

L_duke = Lowering(
    id="L_duke",
    upper_record=_dramatic("C_duke"),
    lower_records=(_substrate("duke"),),
    annotation=Annotation(text="C_duke (Reason) → Entity 'duke'."),
    τ_a=305,
)

L_gazzo = Lowering(
    id="L_gazzo",
    upper_record=_dramatic("C_gazzo"),
    lower_records=(_substrate("gazzo"),),
    annotation=Annotation(text="C_gazzo (Sidekick) → Entity 'gazzo'."),
    τ_a=306,
)

L_jergens = Lowering(
    id="L_jergens",
    upper_record=_dramatic("C_jergens"),
    lower_records=(_substrate("jergens"),),
    annotation=Annotation(text="C_jergens (Skeptic) → Entity 'jergens'."),
    τ_a=307,
)

L_spider_rico = Lowering(
    id="L_spider_rico",
    upper_record=_dramatic("C_spider_rico"),
    lower_records=(_substrate("spider_rico"),),
    annotation=Annotation(
        text=("C_spider_rico (no dramatica-8 function; opponent in the "
              "opening club fight) → Entity 'spider_rico'."),
    ),
    τ_a=308,
)

L_bob = Lowering(
    id="L_bob",
    upper_record=_dramatic("C_bob"),
    lower_records=(_substrate("bob"),),
    annotation=Annotation(
        text=("C_bob (no dramatica-8 function; the dock worker Rocky "
              "refuses to break) → Entity 'bob'."),
    ),
    τ_a=309,
)


# ============================================================================
# Scene → Event(s) Lowerings (mostly 1-to-1, some 1-to-many)
# ============================================================================

L_club_fight = Lowering(
    id="L_club_fight",
    upper_record=_dramatic("S_club_fight"),
    lower_records=(_substrate("E_club_fight_spider"),),
    annotation=Annotation(
        text=("S_club_fight (the Resurrection A.C. opener; Rocky as a "
              "club fighter) → E_club_fight_spider."),
    ),
    τ_a=320,
    anchor_τ_a=_substrate_event("E_club_fight_spider").τ_a,
)

L_mickey_locker = Lowering(
    id="L_mickey_locker",
    upper_record=_dramatic("S_mickey_locker"),
    lower_records=(_substrate("E_mickey_clears_locker"),),
    annotation=Annotation(
        text=("S_mickey_locker (Mickey writes Rocky off) → "
              "E_mickey_clears_locker. The Gazzo-assignment and "
              "Bob-refusal context — not a Dramatic Scene but the MC "
              "beat the Mickey confrontation is responding to — is "
              "covered by E_gazzo_assignment, bound via the MC "
              "Throughline lowering below."),
    ),
    τ_a=321,
    anchor_τ_a=_substrate_event("E_mickey_clears_locker").τ_a,
)

L_apollo_announces = Lowering(
    id="L_apollo_announces",
    upper_record=_dramatic("S_apollo_announces"),
    lower_records=(
        _substrate("E_apollo_schedules_mac"),
        _substrate("E_mac_injured"),
        _substrate("E_apollo_selects_rocky"),
    ),
    annotation=Annotation(
        text=("S_apollo_announces (the premise-trigger montage: Mac's "
              "scheduled fight, Mac's broken hand, Apollo picking the "
              "Italian Stallion from the rankings) realizes as three "
              "pre-plot substrate events. One Dramatic Scene bundles "
              "three substrate events because the scene's argumentative "
              "work is 'the fight exists because Mac can't fight it'; "
              "the substrate splits them because each carries distinct "
              "world effects (scheduling → injury → rescheduling)."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=322,
    anchor_τ_a=_max_event_τ_a(
        "E_apollo_schedules_mac", "E_mac_injured",
        "E_apollo_selects_rocky",
    ),
)

L_jergens_office = Lowering(
    id="L_jergens_office",
    upper_record=_dramatic("S_jergens_office"),
    lower_records=(_substrate("E_jergens_offers_fight"),),
    annotation=Annotation(
        text=("S_jergens_office (the offer delivered; Rocky accepts "
              "without quite knowing why) → E_jergens_offers_fight."),
    ),
    τ_a=323,
    anchor_τ_a=_substrate_event("E_jergens_offers_fight").τ_a,
)

L_mickey_apartment = Lowering(
    id="L_mickey_apartment",
    upper_record=_dramatic("S_mickey_apartment"),
    lower_records=(_substrate("E_mickey_offers_to_manage"),),
    annotation=Annotation(
        text=("S_mickey_apartment (Mickey shows up after the offer; "
              "turns from rejection to late arrival) → "
              "E_mickey_offers_to_manage."),
    ),
    τ_a=324,
    anchor_τ_a=_substrate_event("E_mickey_offers_to_manage").τ_a,
)

L_thanksgiving = Lowering(
    id="L_thanksgiving",
    upper_record=_dramatic("S_thanksgiving"),
    lower_records=(_substrate("E_thanksgiving_turkey"),),
    annotation=Annotation(
        text=("S_thanksgiving (Paulie throws the turkey; Adrian ends "
              "up at Rocky's apartment) → E_thanksgiving_turkey."),
    ),
    τ_a=325,
    anchor_τ_a=_substrate_event("E_thanksgiving_turkey").τ_a,
)

L_ice_skating_pending = Lowering(
    id="L_ice_skating_pending",
    upper_record=_dramatic("S_ice_skating"),
    lower_records=(),
    annotation=Annotation(
        text=("S_ice_skating (Rocky rents the rink for ten minutes; "
              "walks beside Adrian while she skates; the conversation "
              "that opens her) has no dedicated substrate event — it is "
              "a relationship-throughline beat whose work happens "
              "between world-fact changes, not via them. The content "
              "lives in the dramatic Beats' prose and will surface via "
              "descriptions rather than typed fabula. PENDING."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=326,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": ("relationship beat authored in prose; "
                              "no typed world-effect to lower to")},
)

L_first_kiss = Lowering(
    id="L_first_kiss",
    upper_record=_dramatic("S_first_kiss"),
    lower_records=(_substrate("E_first_kiss"),),
    annotation=Annotation(
        text=("S_first_kiss (Rocky's apartment; 'I don't like to "
              "lose'; the relationship commits) → E_first_kiss. "
              "World fact romantic_partnership(rocky, adrian) lands "
              "at this event."),
    ),
    τ_a=327,
    anchor_τ_a=_substrate_event("E_first_kiss").τ_a,
)

L_training_montage = Lowering(
    id="L_training_montage",
    upper_record=_dramatic("S_training_montage"),
    lower_records=(
        _substrate("E_training_begins"),
        _substrate("E_meat_locker_session"),
        _substrate("E_stairs_run"),
    ),
    annotation=Annotation(
        text=("S_training_montage (the whole training arc — meat "
              "locker, pre-dawn runs, stairs) realizes as three "
              "substrate events representing onset (τ_s=10), middle "
              "(meat locker τ_s=15), and peak (stairs τ_s=25). "
              "Dramatic Scene bundles the montage; substrate splits "
              "by physical-readiness signposts."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=328,
    position_range=PositionRange(coord="τ_s", min_value=10, max_value=25),
    anchor_τ_a=_max_event_τ_a(
        "E_training_begins", "E_meat_locker_session", "E_stairs_run",
    ),
)

L_night_before = Lowering(
    id="L_night_before",
    upper_record=_dramatic("S_night_before"),
    lower_records=(_substrate("E_night_before_fight"),),
    annotation=Annotation(
        text=("S_night_before (Rocky alone in the empty arena; 'I just "
              "want to go the distance') → E_night_before_fight. The "
              "MC's articulated goal is recorded in Rocky's knowledge "
              "state here — the Growth=Start transition point."),
    ),
    τ_a=329,
    anchor_τ_a=_substrate_event("E_night_before_fight").τ_a,
)

L_fight = Lowering(
    id="L_fight",
    upper_record=_dramatic("S_fight"),
    lower_records=(
        _substrate("E_fight_bell"),
        _substrate("E_round_one_knockdown"),
        _substrate("E_rocky_gets_up"),
        _substrate("E_fight_ends"),
    ),
    annotation=Annotation(
        text=("S_fight (fifteen rounds; Apollo wins on scorecards; "
              "Rocky stays on his feet) realizes as four substrate "
              "events: the opening bell, the round-one knockdown, "
              "Rocky rising (the unscripted turn Apollo's dismissive "
              "stance can't absorb), and the final bell with the "
              "split decision. The compound went_the_distance derives "
              "at E_fight_ends via the WENT_THE_DISTANCE_RULE."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=330,
    position_range=PositionRange(coord="τ_s", min_value=46, max_value=55),
    anchor_τ_a=_max_event_τ_a(
        "E_fight_bell", "E_round_one_knockdown",
        "E_rocky_gets_up", "E_fight_ends",
    ),
)

L_after = Lowering(
    id="L_after",
    upper_record=_dramatic("S_after"),
    lower_records=(
        _substrate("E_adrian_called"),
        _substrate("E_no_rematch"),
    ),
    annotation=Annotation(
        text=("S_after ('Adrian!' through the crowd; then the mutual "
              "refusal of a rematch) realizes as two substrate events. "
              "One Dramatic Scene; two substrate events because the "
              "'Adrian!' moment and the 'no rematch' exchange are "
              "distinct beats with distinct participants and effects."),
    ),
    τ_a=331,
    anchor_τ_a=_max_event_τ_a("E_adrian_called", "E_no_rematch"),
)


# ============================================================================
# Throughline T_mc_rocky → many events (with position_range)
# ============================================================================

L_mc_throughline = Lowering(
    id="L_mc_throughline",
    upper_record=_dramatic("T_mc_rocky"),
    lower_records=(
        _substrate("E_club_fight_spider"),
        _substrate("E_mickey_clears_locker"),
        _substrate("E_gazzo_assignment"),
        _substrate("E_pet_store_courtship"),
        _substrate("E_jergens_offers_fight"),
        _substrate("E_mickey_offers_to_manage"),
        _substrate("E_thanksgiving_turkey"),
        _substrate("E_first_kiss"),
        _substrate("E_training_begins"),
        _substrate("E_meat_locker_session"),
        _substrate("E_stairs_run"),
        _substrate("E_night_before_fight"),
        _substrate("E_fight_bell"),
        _substrate("E_round_one_knockdown"),
        _substrate("E_rocky_gets_up"),
        _substrate("E_fight_ends"),
        _substrate("E_adrian_called"),
        _substrate("E_no_rematch"),
    ),
    annotation=Annotation(
        text=("Dramatic Throughline T_mc_rocky (Rocky's MC arc: club "
              "fighter to man who went the distance) realizes across "
              "substrate events from τ_s=0 (the Spider Rico club fight) "
              "through τ_s=57 (no rematch). The pre-plot events "
              "(Mac's injury, Apollo's selection) are OS-Throughline "
              "(T_overall_fight), not MC — Rocky is not yet a "
              "participant at those τ_s. Eighteen events total; Rocky "
              "is a direct participant in all of them."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=340,
    position_range=PositionRange(coord="τ_s", min_value=0, max_value=57),
    anchor_τ_a=_max_event_τ_a(
        "E_club_fight_spider", "E_mickey_clears_locker",
        "E_gazzo_assignment", "E_pet_store_courtship",
        "E_jergens_offers_fight", "E_mickey_offers_to_manage",
        "E_thanksgiving_turkey", "E_first_kiss",
        "E_training_begins", "E_meat_locker_session", "E_stairs_run",
        "E_night_before_fight",
        "E_fight_bell", "E_round_one_knockdown",
        "E_rocky_gets_up", "E_fight_ends",
        "E_adrian_called", "E_no_rematch",
    ),
)


# ============================================================================
# Aggregate
# ============================================================================

LOWERINGS = (
    # Character → Entity
    L_rocky, L_apollo, L_mickey, L_paulie, L_adrian,
    L_duke, L_gazzo, L_jergens, L_spider_rico, L_bob,
    # Scene → Event(s)
    L_club_fight, L_mickey_locker, L_apollo_announces,
    L_jergens_office, L_mickey_apartment, L_thanksgiving,
    L_first_kiss, L_training_montage, L_night_before,
    L_fight, L_after,
    # Scene with no substrate event (PENDING)
    L_ice_skating_pending,
    # Throughline → many-events with position_range
    L_mc_throughline,
)
