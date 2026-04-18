"""
ackroyd_lowerings.py — third authored Lowering set: Ackroyd Dramatic
↔ substrate.

Companion to oedipus_lowerings.py and macbeth_lowerings.py. Same
architecture-sketch-02 A6/A7 pattern: dialects stand alone, then
explicit Lowering records say what upper-side record is realized by
what lower-side record(s).

Ackroyd contrasts with the previous pair in ways this module exercises:

- **Character cast is fully present substrate-side.** All twelve
  Ackroyd Characters have substrate Entity counterparts. Oedipus had
  PENDING Lowerings for Tiresias and Creon (substrate cut); Macbeth
  was clean; Ackroyd is cleaner still — the substrate was authored
  knowing the dialect encoding to come.

- **One Scene bundles three substrate events.** S_ackroyd_killed
  lowers to E_sheppard_plants_dictaphone (τ_s=1) +
  E_sheppard_murders_ackroyd (τ_s=1) + E_sheppard_leaves_fernly
  (τ_s=1) — the dialect Scene bundles the three micro-events that
  compose the "killing-with-alibi" moment at the substrate layer.
  Same pattern as Macbeth's S_discovery_and_crown.

- **Two Scenes share one substrate event.** S_investigation and
  S_ursula_confession both lower to E_poirot_investigates — the
  substrate compresses the investigation sequence into one event
  (matching the novel's compressed middle); the dialect splits it
  into two Scenes to separate the general investigation from the
  specific Ursula-confession structural moment. Cross-dialect
  compression happening in opposite directions: substrate compresses,
  dialect expands.

- **The MC's Throughline bounds start pre-play.** T_mc_sheppard
  position_range starts at τ_s=-18 — when Sheppard deduces Mrs.
  Ferrars' poisoning (the substrate event where his arc begins,
  even though the novel opens at τ_s=0). The MC's Dramatic arc
  spans pre-play backstory + the in-play action.

- **Argument has no Lowering.** A_truth_recovers is a Claim coupling
  per L1, same as Oedipus's A_knowledge_unmakes and Macbeth's
  A_ambition_unmakes. The verifier surface
  (ackroyd_verification.py) is where the Argument's trajectory
  signatures bind to substrate.

Coupling kinds across this set: every Lowering here is Realization
(per L1, the only kind Lowering records carry).
"""

from __future__ import annotations

from substrate import Entity, Event
from ackroyd import FABULA, ENTITIES

from dramatic import Story, Character, Scene, Throughline
from ackroyd_dramatic import (
    STORY, CHARACTERS, SCENES, THROUGHLINES, BEATS,
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

L_poirot = Lowering(
    id="L_poirot",
    upper_record=_dramatic("C_poirot"),
    lower_records=(_substrate("poirot"),),
    annotation=Annotation(
        text=("C_poirot (Protagonist on the dramatica-8 slot + owner "
              "of T_ic_poirot, the impact-character Throughline) → "
              "Entity 'poirot'. The double-role is the encoding's "
              "structural thesis; both attachments point to the same "
              "substrate Entity."),
    ),
    τ_a=100,
)

L_sheppard = Lowering(
    id="L_sheppard",
    upper_record=_dramatic("C_sheppard"),
    lower_records=(_substrate("sheppard"),),
    annotation=Annotation(
        text=("C_sheppard (Antagonist on the dramatica-8 slot + owner "
              "of T_mc_sheppard, the main-character Throughline) → "
              "Entity 'sheppard'. The MC-is-Antagonist alignment is "
              "the encoding's structural thesis; the substrate carries "
              "his cumulative KNOWN set (the blackmail, the murder, "
              "the staged alibi) that Dramatica describes him "
              "opposing the story goal from."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=101,
)

L_raymond = Lowering(
    id="L_raymond",
    upper_record=_dramatic("C_raymond"),
    lower_records=(_substrate("geoffrey_raymond"),),
    annotation=Annotation(
        text=("C_raymond (Reason) → Entity 'geoffrey_raymond'. The "
              "secretary whose overheard phrase is a key piece of "
              "Poirot's reconstruction — the Reason function served "
              "through the methodical-witness role."),
    ),
    τ_a=102,
)

L_flora = Lowering(
    id="L_flora",
    upper_record=_dramatic("C_flora"),
    lower_records=(_substrate("flora_ackroyd"),),
    annotation=Annotation(
        text=("C_flora (Emotion) → Entity 'flora_ackroyd'. Her "
              "conviction of Ralph's innocence drives Poirot's "
              "engagement."),
    ),
    τ_a=103,
)

L_raglan = Lowering(
    id="L_raglan",
    upper_record=_dramatic("C_raglan"),
    lower_records=(_substrate("inspector_raglan"),),
    annotation=Annotation(
        text=("C_raglan (Skeptic) → Entity 'inspector_raglan'. The "
              "police Inspector; doubts both Ralph's flight as "
              "evidence and Poirot's eventual theory — the Skeptic's "
              "institutional form."),
    ),
    τ_a=104,
)

L_blunt = Lowering(
    id="L_blunt",
    upper_record=_dramatic("C_blunt"),
    lower_records=(_substrate("major_blunt"),),
    annotation=Annotation(
        text=("C_blunt (Sidekick) → Entity 'major_blunt'. The "
              "retired major who becomes Poirot's informal informant "
              "in the household — his knowledge of Fernly Park and "
              "its inhabitants (including a quiet regard for Flora) "
              "supplies the ground-level testimony the Skeptic "
              "(Raglan) refuses to credit. Participates in "
              "E_poirot_investigates (as witness) and "
              "E_poirot_reveals_solution (as assembled audience). "
              "The Sidekick function manifests as provisional support "
              "— Blunt lends Poirot credibility in the household "
              "without the institutional challenge a Skeptic or "
              "Antagonist would bring."),
    ),
    τ_a=105,
)

L_caroline = Lowering(
    id="L_caroline",
    upper_record=_dramatic("C_caroline"),
    lower_records=(_substrate("caroline_sheppard"),),
    annotation=Annotation(
        text=("C_caroline (Guardian) → Entity 'caroline_sheppard'. "
              "The village oracle; the Guardian role's ironic form — "
              "she 'knows everyone' but does not know her own "
              "brother. The Guardian function-of-warning lands "
              "structurally on her capacity for pattern-recognition "
              "even where she mis-reads the specific man."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=106,
)

L_ralph = Lowering(
    id="L_ralph",
    upper_record=_dramatic("C_ralph_paton"),
    lower_records=(_substrate("ralph_paton"),),
    annotation=Annotation(
        text=("C_ralph_paton (Contagonist) → Entity 'ralph_paton'. "
              "His disappearance IS the misdirection; his passive "
              "innocence is the Contagonist function served through "
              "the red-herring role."),
    ),
    τ_a=107,
)

L_ackroyd = Lowering(
    id="L_ackroyd",
    upper_record=_dramatic("C_ackroyd"),
    lower_records=(_substrate("ackroyd"),),
    annotation=Annotation(
        text="C_ackroyd (no function; victim) → Entity 'ackroyd'.",
    ),
    τ_a=108,
)

L_mrs_ferrars = Lowering(
    id="L_mrs_ferrars",
    upper_record=_dramatic("C_mrs_ferrars"),
    lower_records=(_substrate("mrs_ferrars"),),
    annotation=Annotation(
        text=("C_mrs_ferrars (no function; pre-dead) → Entity "
              "'mrs_ferrars'. Her pre-play poisoning of her husband, "
              "Sheppard's blackmail, and her suicide at τ_s=0 are "
              "the triggers for the whole case."),
    ),
    τ_a=109,
)

L_ursula_bourne = Lowering(
    id="L_ursula_bourne",
    upper_record=_dramatic("C_ursula_bourne"),
    lower_records=(_substrate("ursula_bourne"),),
    annotation=Annotation(
        text=("C_ursula_bourne (no function) → Entity 'ursula_bourne'. "
              "The parlormaid whose secret marriage to Ralph "
              "misdirects and then clears."),
    ),
    τ_a=110,
)

L_parker = Lowering(
    id="L_parker",
    upper_record=_dramatic("C_parker"),
    lower_records=(_substrate("parker"),),
    annotation=Annotation(
        text=("C_parker (no function) → Entity 'parker'. The butler "
              "whose 9:30pm dictaphone-deceived BELIEVED is part of "
              "the alibi Poirot unwinds."),
    ),
    τ_a=111,
)


# ============================================================================
# Scene → Event(s) Lowerings
# ============================================================================

L_ferrars_death = Lowering(
    id="L_ferrars_death",
    upper_record=_dramatic("S_ferrars_death"),
    lower_records=(_substrate("E_mrs_ferrars_suicide"),),
    annotation=Annotation(
        text=("S_ferrars_death (the novel's opening, Sheppard "
              "returning from pronouncing her dead, the letter-to-"
              "Ackroyd's expected arrival) realizes as substrate "
              "event E_mrs_ferrars_suicide (τ_s=0). The substrate "
              "event records dead(mrs_ferrars), "
              "death_was_suicide(mrs_ferrars), and — authored at "
              "the event — driver_of_suicide(sheppard, mrs_ferrars) "
              "as the rule head that derives from Sheppard's prior "
              "blackmail."),
    ),
    τ_a=120,
    anchor_τ_a=_substrate_event("E_mrs_ferrars_suicide").τ_a,
)

L_ackroyd_dinner = Lowering(
    id="L_ackroyd_dinner",
    upper_record=_dramatic("S_ackroyd_dinner"),
    lower_records=(_substrate("E_ackroyd_dines_with_sheppard"),),
    annotation=Annotation(
        text=("S_ackroyd_dinner (the moral-decision scene; Sheppard "
              "learns Ackroyd is about to name him) realizes as "
              "substrate event E_ackroyd_dines_with_sheppard (τ_s=1). "
              "The substrate event carries the told_by effect where "
              "Ackroyd informs Sheppard of the letter — the last "
              "piece of information Sheppard receives before "
              "acting."),
    ),
    τ_a=121,
    anchor_τ_a=_substrate_event("E_ackroyd_dines_with_sheppard").τ_a,
)

L_ackroyd_killed = Lowering(
    id="L_ackroyd_killed",
    upper_record=_dramatic("S_ackroyd_killed"),
    lower_records=(
        _substrate("E_sheppard_plants_dictaphone"),
        _substrate("E_sheppard_murders_ackroyd"),
        _substrate("E_sheppard_leaves_fernly"),
    ),
    annotation=Annotation(
        text=("S_ackroyd_killed (the Dramatic-layer scene of the "
              "killing and its alibi) bundles three contiguous "
              "substrate events at τ_s=1: the dictaphone preparation, "
              "the murder itself, and the visible departure. The "
              "substrate separates them because each produces "
              "distinct world + knowledge effects (setup, killing + "
              "betrayer_of_trust derivation, alibi-observable). The "
              "Dramatic Scene reads them as one argumentative moment "
              "— the Antagonist's central act."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=122,
    anchor_τ_a=_max_event_τ_a(
        "E_sheppard_plants_dictaphone",
        "E_sheppard_murders_ackroyd",
        "E_sheppard_leaves_fernly",
    ),
)

L_body_discovery = Lowering(
    id="L_body_discovery",
    upper_record=_dramatic("S_body_discovery"),
    lower_records=(_substrate("E_body_discovered"),),
    annotation=Annotation(
        text=("S_body_discovery (morning after; the shock; Sheppard's "
              "performed concern) realizes as substrate event "
              "E_body_discovered (τ_s=2). The substrate event "
              "dislodges Parker's dictaphone-deceived BELIEVED "
              "alive(ackroyd) — the unreliable-narration's first "
              "substrate-visible correction."),
    ),
    τ_a=123,
    anchor_τ_a=_substrate_event("E_body_discovered").τ_a,
)

L_ralph_flight = Lowering(
    id="L_ralph_flight",
    upper_record=_dramatic("S_ralph_flight"),
    lower_records=(_substrate("E_ralph_missing"),),
    annotation=Annotation(
        text=("S_ralph_flight (the contagonist's diverting "
              "absence) realizes as substrate event E_ralph_missing "
              "(τ_s=2), which authors accused_of_murder(ralph_paton, "
              "ackroyd) as a world fact."),
    ),
    τ_a=124,
    anchor_τ_a=_substrate_event("E_ralph_missing").τ_a,
)

L_flora_hires_poirot = Lowering(
    id="L_flora_hires_poirot",
    upper_record=_dramatic("S_flora_hires_poirot"),
    lower_records=(_substrate("E_flora_summons_poirot"),),
    annotation=Annotation(
        text=("S_flora_hires_poirot (Flora commissions Poirot; "
              "detective-assistant pairing forms) realizes as "
              "substrate event E_flora_summons_poirot (τ_s=2). "
              "Poirot enters the fabula at this event; his earlier "
              "retirement is preplay."),
    ),
    τ_a=125,
    anchor_τ_a=_substrate_event("E_flora_summons_poirot").τ_a,
)

L_investigation = Lowering(
    id="L_investigation",
    upper_record=_dramatic("S_investigation"),
    lower_records=(_substrate("E_poirot_investigates"),),
    annotation=Annotation(
        text=("S_investigation (the general investigation-sequence) "
              "realizes as substrate event E_poirot_investigates "
              "(τ_s=5). The substrate compresses the novel's long "
              "investigation middle into one event; the dialect "
              "splits the same territory into S_investigation (the "
              "general inquiry) and S_ursula_confession (the specific "
              "structural moment)."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=126,
    anchor_τ_a=_substrate_event("E_poirot_investigates").τ_a,
)

L_ursula_confession = Lowering(
    id="L_ursula_confession",
    upper_record=_dramatic("S_ursula_confession"),
    lower_records=(_substrate("E_poirot_investigates"),),
    annotation=Annotation(
        text=("S_ursula_confession (the marriage-secret revealed) "
              "realizes as substrate event E_poirot_investigates "
              "(τ_s=5) — the same event S_investigation lowers to. "
              "Shared binding: two Dramatic Scenes read different "
              "aspects of one substrate investigation-event. The "
              "substrate authors Ursula's confession as an observe "
              "effect within E_poirot_investigates's effects tuple; "
              "both Scenes are reading that moment through different "
              "lenses."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=127,
    anchor_τ_a=_substrate_event("E_poirot_investigates").τ_a,
)

L_dictaphone_breakthrough = Lowering(
    id="L_dictaphone_breakthrough",
    upper_record=_dramatic("S_dictaphone_breakthrough"),
    lower_records=(
        _substrate("E_dictaphone_plays"),
        _substrate("E_poirot_investigates"),
    ),
    annotation=Annotation(
        text=("S_dictaphone_breakthrough (Poirot's reconstruction of "
              "the alibi's mechanism) bundles the substrate event "
              "whose effect is the alibi being staged "
              "(E_dictaphone_plays at τ_s=1) with the investigation "
              "event where Poirot works out what happened "
              "(E_poirot_investigates at τ_s=5). The Dramatic Scene "
              "reads the earlier event's fact and the later event's "
              "reasoning as one argumentative beat — the moment "
              "Poirot solves it privately."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=128,
    anchor_τ_a=_max_event_τ_a(
        "E_dictaphone_plays", "E_poirot_investigates",
    ),
)

L_poirot_reveal = Lowering(
    id="L_poirot_reveal",
    upper_record=_dramatic("S_poirot_reveal"),
    lower_records=(_substrate("E_poirot_reveals_solution"),),
    annotation=Annotation(
        text=("S_poirot_reveal (the drawing-room reconstruction) "
              "realizes as substrate event E_poirot_reveals_solution "
              "(τ_s=8). The substrate event carries the cast's "
              "epistemic updates: Poirot, Caroline, Flora, Raglan — "
              "all add killed(sheppard, ackroyd) to their KNOWN sets "
              "at this moment. This is the Argument's AFFIRM "
              "resolution event."),
    ),
    τ_a=129,
    anchor_τ_a=_substrate_event("E_poirot_reveals_solution").τ_a,
)

L_private_ultimatum = Lowering(
    id="L_private_ultimatum",
    upper_record=_dramatic("S_private_ultimatum"),
    lower_records=(_substrate("E_poirot_private_confrontation"),),
    annotation=Annotation(
        text=("S_private_ultimatum (the detective-killer private "
              "conversation) realizes as substrate event "
              "E_poirot_private_confrontation (τ_s=9). The ultimatum "
              "fact enters Sheppard's KNOWN set via told_by(sheppard, "
              "poirot, ultimatum_confession_or_disclosure)."),
    ),
    τ_a=130,
    anchor_τ_a=_substrate_event("E_poirot_private_confrontation").τ_a,
)

L_sheppard_death = Lowering(
    id="L_sheppard_death",
    upper_record=_dramatic("S_sheppard_death"),
    lower_records=(
        _substrate("E_sheppard_writes_manuscript"),
        _substrate("E_sheppard_suicide"),
    ),
    annotation=Annotation(
        text=("S_sheppard_death (the manuscript's honest close + "
              "Sheppard's overdose) bundles two substrate events: "
              "the writing (τ_s=10) and the death (τ_s=11). The "
              "Dramatic Scene treats them as one denouement beat — "
              "the novel's final paragraph and its implied "
              "completion."),
    ),
    τ_a=131,
    anchor_τ_a=_max_event_τ_a(
        "E_sheppard_writes_manuscript", "E_sheppard_suicide",
    ),
)


# ============================================================================
# Throughline → many-events Lowerings (with position_range)
# ============================================================================

L_overall_throughline = Lowering(
    id="L_overall_throughline",
    upper_record=_dramatic("T_overall_case"),
    lower_records=(
        _substrate("E_mr_ferrars_poisoned"),
        _substrate("E_sheppard_blackmails_ferrars"),
        _substrate("E_mrs_ferrars_suicide"),
        _substrate("E_sheppard_murders_ackroyd"),
        _substrate("E_body_discovered"),
        _substrate("E_ralph_missing"),
        _substrate("E_flora_summons_poirot"),
        _substrate("E_poirot_investigates"),
        _substrate("E_poirot_reveals_solution"),
        _substrate("E_sheppard_suicide"),
    ),
    annotation=Annotation(
        text=("T_overall_case (the kingdom's-moral-order analog — the "
              "village's legal-and-moral order disturbed, "
              "investigated, restored) realizes across the substrate "
              "events that move the case. position_range frames this "
              "as fabula τ_s ∈ [-20, 11] — from Mr. Ferrars' "
              "poisoning (the deepest backstory that becomes case-"
              "relevant) through Sheppard's suicide. Side-on-Argument "
              "is AFFIRMS: the case's resolution demonstrates "
              "truth-recovery."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=140,
    position_range=PositionRange(coord="τ_s", min_value=-20, max_value=11),
    anchor_τ_a=_max_event_τ_a(
        "E_mr_ferrars_poisoned", "E_sheppard_blackmails_ferrars",
        "E_mrs_ferrars_suicide", "E_sheppard_murders_ackroyd",
        "E_body_discovered", "E_ralph_missing",
        "E_flora_summons_poirot", "E_poirot_investigates",
        "E_poirot_reveals_solution", "E_sheppard_suicide",
    ),
)

L_mc_throughline = Lowering(
    id="L_mc_throughline",
    upper_record=_dramatic("T_mc_sheppard"),
    lower_records=(
        _substrate("E_sheppard_deduces_poisoning"),
        _substrate("E_sheppard_blackmails_ferrars"),
        _substrate("E_mrs_ferrars_suicide"),
        _substrate("E_ackroyd_dines_with_sheppard"),
        _substrate("E_sheppard_plants_dictaphone"),
        _substrate("E_sheppard_murders_ackroyd"),
        _substrate("E_sheppard_leaves_fernly"),
        _substrate("E_body_discovered"),
        _substrate("E_poirot_investigates"),
        _substrate("E_poirot_reveals_solution"),
        _substrate("E_poirot_private_confrontation"),
        _substrate("E_sheppard_writes_manuscript"),
        _substrate("E_sheppard_suicide"),
    ),
    annotation=Annotation(
        text=("T_mc_sheppard (the MC's arc: doctor-investigator-of-"
              "Ferrars → blackmailer → murderer → performer → "
              "assistant → named → writer → dead) realizes across "
              "the substrate events that compose Sheppard's "
              "trajectory. position_range frames this as fabula τ_s "
              "∈ [-18, 11] — from when he deduces Mrs. Ferrars' "
              "poisoning (where his arc begins, and the novel's "
              "pre-play rot sets in) through his death. The MC owns "
              "7 beats on this Throughline. Side-on-Argument is "
              "COMPLICATES: his existence is the Argument's test "
              "material."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=141,
    position_range=PositionRange(coord="τ_s", min_value=-18, max_value=11),
    anchor_τ_a=_max_event_τ_a(
        "E_sheppard_deduces_poisoning",
        "E_sheppard_blackmails_ferrars",
        "E_mrs_ferrars_suicide",
        "E_ackroyd_dines_with_sheppard",
        "E_sheppard_plants_dictaphone",
        "E_sheppard_murders_ackroyd",
        "E_sheppard_leaves_fernly",
        "E_body_discovered",
        "E_poirot_investigates",
        "E_poirot_reveals_solution",
        "E_poirot_private_confrontation",
        "E_sheppard_writes_manuscript",
        "E_sheppard_suicide",
    ),
)

L_ic_throughline = Lowering(
    id="L_ic_throughline",
    upper_record=_dramatic("T_ic_poirot"),
    lower_records=(
        _substrate("E_flora_summons_poirot"),
        _substrate("E_poirot_investigates"),
        _substrate("E_poirot_reveals_solution"),
        _substrate("E_poirot_private_confrontation"),
    ),
    annotation=Annotation(
        text=("T_ic_poirot (the detective's in-play arc: engagement "
              "→ investigation → reveal → ultimatum) realizes across "
              "the four substrate events where Poirot is focal. "
              "position_range frames this as fabula τ_s ∈ [2, 9] — "
              "Poirot's in-play lifespan; his earlier retirement is "
              "pre-play. Shorter τ_s span than T_mc_sheppard: the IC "
              "arrives on scene only after the inciting murder. "
              "Side-on-Argument is AFFIRMS: his work IS the "
              "demonstration."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=142,
    position_range=PositionRange(coord="τ_s", min_value=2, max_value=9),
    anchor_τ_a=_max_event_τ_a(
        "E_flora_summons_poirot", "E_poirot_investigates",
        "E_poirot_reveals_solution", "E_poirot_private_confrontation",
    ),
)

L_relationship_throughline = Lowering(
    id="L_relationship_throughline",
    upper_record=_dramatic("T_rel_sheppard_poirot"),
    lower_records=(
        _substrate("E_flora_summons_poirot"),
        _substrate("E_poirot_investigates"),
        _substrate("E_poirot_reveals_solution"),
        _substrate("E_poirot_private_confrontation"),
        _substrate("E_sheppard_suicide"),
    ),
    annotation=Annotation(
        text=("T_rel_sheppard_poirot (the pairing's arc: formed on "
              "apparent good faith → collaborative through the "
              "investigation → inverted publicly at the reveal → "
              "ended in the private conversation and Sheppard's "
              "death) realizes across the five substrate events "
              "where they are co-present or the pairing is the "
              "subject. position_range frames this as fabula τ_s ∈ "
              "[2, 11] — from their first meeting through Sheppard's "
              "death."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=143,
    position_range=PositionRange(coord="τ_s", min_value=2, max_value=11),
    anchor_τ_a=_max_event_τ_a(
        "E_flora_summons_poirot", "E_poirot_investigates",
        "E_poirot_reveals_solution", "E_poirot_private_confrontation",
        "E_sheppard_suicide",
    ),
)


# ============================================================================
# Exports
# ============================================================================


LOWERINGS = (
    # Character → Entity (12; all ACTIVE)
    L_poirot, L_sheppard, L_raymond, L_flora, L_raglan,
    L_blunt, L_caroline, L_ralph, L_ackroyd, L_mrs_ferrars,
    L_ursula_bourne, L_parker,

    # Scene → Event(s) (12; all ACTIVE)
    L_ferrars_death, L_ackroyd_dinner, L_ackroyd_killed,
    L_body_discovery, L_ralph_flight, L_flora_hires_poirot,
    L_investigation, L_ursula_confession,
    L_dictaphone_breakthrough, L_poirot_reveal,
    L_private_ultimatum, L_sheppard_death,

    # Throughline → many-events (4; all ACTIVE with position_range)
    L_overall_throughline, L_mc_throughline,
    L_ic_throughline, L_relationship_throughline,
)
