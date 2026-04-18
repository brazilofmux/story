"""
macbeth_lowerings.py — second authored Lowering set: Macbeth Dramatic
↔ substrate.

Companion to oedipus_lowerings.py. Same architecture-sketch-02 A6/A7
pattern: dialects stand alone, then explicit Lowering records say what
upper-side record is realized by what lower-side record(s).

Macbeth contrasts with Oedipus along several axes that this module
exercises:

- Character cast is fully present substrate-side. Oedipus's encoding
  cuts Tiresias and Creon (PENDING Lowerings); macbeth.py keeps every
  Dramatic Character's substrate counterpart, so all nine Character →
  Entity Lowerings here are ACTIVE. The PENDING status is exercised
  on the Scene side instead.
- Scene cast is also nearly complete. Thirteen of fourteen Dramatic
  Scenes have substrate event(s) to bind. Only S_plot — the
  Macbeth/Lady Macbeth conspiracy that the play stages between
  E_letter_to_lady_macbeth and E_duncan_visits — has no discrete
  substrate event; its work is implicit in the surrounding events'
  effects. PENDING.
- Four Throughlines (Oedipus has three) — each gets a position_range
  Lowering across its substrate events. The relationship throughline
  bounds tightly (the marriage's in-play life: τ_s 2..14); the
  overall-story throughline spans the play (τ_s -30..18).
- Argument A_ambition_unmakes is a Claim coupling per L1 / lowering-
  sketch-01 F1 — no Lowering record. The verifier surface
  (macbeth_verification.py) is where this binds to substrate.

Coupling kinds across this set: every Lowering here is Realization
(per L1, the only kind Lowering records carry).
"""

from __future__ import annotations

# Substrate-side imports.
from substrate import Entity, Event
from macbeth import (
    FABULA,
    ENTITIES,
    DESCRIPTIONS as MACBETH_SUBSTRATE_DESCRIPTIONS,
)

# Dramatic-side imports.
from dramatic import Story, Character, Scene, Throughline
from macbeth_dramatic import (
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
    """Compute max τ_a across the given event ids — used for
    anchor_τ_a on Lowerings whose lower side is one or more events."""
    return max(_substrate_event(eid).τ_a for eid in event_ids)


def _dramatic(record_id: str) -> CrossDialectRef:
    return cross_ref("dramatic", record_id)


def _substrate(record_id: str) -> CrossDialectRef:
    return cross_ref("substrate", record_id)


# ============================================================================
# Character → Entity Lowerings (1-to-1)
# ============================================================================
#
# All nine Macbeth Characters have substrate Entity counterparts.
# anchor_τ_a is None throughout — substrate Entities have no τ_a, so
# staleness is undefined for these.

L_macbeth = Lowering(
    id="L_macbeth",
    upper_record=_dramatic("C_macbeth"),
    lower_records=(_substrate("macbeth"),),
    annotation=Annotation(
        text=("Dramatic Character C_macbeth realizes as substrate "
              "Entity 'macbeth' — the Protagonist + Emotion (double "
              "function MC) on the Dramatic side, the agent on whom "
              "the substrate's moral-derivation chain (kinslayer → "
              "regicide → tyrant) lands. Function labels stay dialect-"
              "local; the substrate carries his actions and knowledge."),
    ),
    τ_a=200,
)

L_lady_macbeth = Lowering(
    id="L_lady_macbeth",
    upper_record=_dramatic("C_lady_macbeth"),
    lower_records=(_substrate("lady_macbeth"),),
    annotation=Annotation(
        text=("C_lady_macbeth (Contagonist; also the Impact Character "
              "owner T_impact_lady_macbeth) → Entity 'lady_macbeth'. "
              "Her sleepwalking and death are substrate events; her "
              "Dramatic role is to push Macbeth across the moral "
              "threshold."),
    ),
    τ_a=201,
)

L_macduff = Lowering(
    id="L_macduff",
    upper_record=_dramatic("C_macduff"),
    lower_records=(_substrate("macduff"),),
    annotation=Annotation(
        text=("C_macduff (Antagonist + Skeptic) → Entity 'macduff'. The "
              "play picks Macduff as Antagonist on the structural-"
              "resolution criterion (he is the agent of overthrow); "
              "alternative readings name Lady Macbeth, the Witches, or "
              "Macbeth's own ambition. The substrate doesn't take a "
              "side — it just records killed(macduff, macbeth) at the "
              "end."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=202,
)

L_banquo = Lowering(
    id="L_banquo",
    upper_record=_dramatic("C_banquo"),
    lower_records=(_substrate("banquo"),),
    annotation=Annotation(text="C_banquo (Sidekick) → Entity 'banquo'."),
    τ_a=203,
)

L_malcolm = Lowering(
    id="L_malcolm",
    upper_record=_dramatic("C_malcolm"),
    lower_records=(_substrate("malcolm"),),
    annotation=Annotation(text="C_malcolm (Reason) → Entity 'malcolm'."),
    τ_a=204,
)

L_witches = Lowering(
    id="L_witches",
    upper_record=_dramatic("C_witches"),
    lower_records=(_substrate("witches"),),
    annotation=Annotation(
        text=("C_witches (Guardian, on the warn-of-consequences "
              "reading) → Entity 'witches'. The substrate Entity is a "
              "single agent representing the trio; whether the witches "
              "are real metaphysical agents, manipulative tricksters, "
              "or projections of Macbeth's own ambition is a "
              "descriptions-layer question the substrate stays out of. "
              "The Dramatic Guardian assignment leans on the warn-of-"
              "consequences reading; the substrate is compatible with "
              "any."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=205,
)

L_duncan = Lowering(
    id="L_duncan",
    upper_record=_dramatic("C_duncan"),
    lower_records=(_substrate("duncan"),),
    annotation=Annotation(text="C_duncan → Entity 'duncan'."),
    τ_a=206,
)

L_lady_macduff = Lowering(
    id="L_lady_macduff",
    upper_record=_dramatic("C_lady_macduff"),
    lower_records=(_substrate("lady_macduff"),),
    annotation=Annotation(text="C_lady_macduff → Entity 'lady_macduff'."),
    τ_a=207,
)

L_fleance = Lowering(
    id="L_fleance",
    upper_record=_dramatic("C_fleance"),
    lower_records=(_substrate("fleance"),),
    annotation=Annotation(text="C_fleance → Entity 'fleance'."),
    τ_a=208,
)


# ============================================================================
# Scene → Event(s) Lowerings (1-to-many)
# ============================================================================
#
# Most Macbeth Scenes have one substrate event each; three Scenes
# bundle two events (S_discovery_and_crown, S_macduff_family,
# S_macbeth_dies). One Scene (S_plot) has no substrate event — it
# stays PENDING.

L_prophecy = Lowering(
    id="L_prophecy",
    upper_record=_dramatic("S_prophecy"),
    lower_records=(_substrate("E_prophecy_first"),),
    annotation=Annotation(
        text=("Dramatic Scene S_prophecy (the Witches' first prophecy on "
              "the heath; the Inciting Incident on T_overall_scotland "
              "and T_mc_macbeth) realizes as substrate event "
              "E_prophecy_first. The Scene names the prophecy's effect "
              "on Macbeth — that ambition now has a name and a path; "
              "the substrate event records the literal prophetic "
              "speech-acts and Macbeth's adoption of "
              "prophecy_will_be_king at KNOWN."),
    ),
    τ_a=210,
    anchor_τ_a=_substrate_event("E_prophecy_first").τ_a,
)

L_letter = Lowering(
    id="L_letter",
    upper_record=_dramatic("S_letter"),
    lower_records=(_substrate("E_letter_to_lady_macbeth"),),
    annotation=Annotation(
        text=("S_letter (LM reads the letter; she chooses what they "
              "will do; the Inciting Incident on the relationship and "
              "impact-character throughlines) realizes as substrate "
              "event E_letter_to_lady_macbeth. The Scene names her "
              "decision-for-both; the substrate records the literal "
              "letter-passing and her uptake of the prophecy at "
              "KNOWN."),
    ),
    τ_a=211,
    anchor_τ_a=_substrate_event("E_letter_to_lady_macbeth").τ_a,
)

L_plot_pending = Lowering(
    id="L_plot_pending",
    upper_record=_dramatic("S_plot"),
    lower_records=(),
    annotation=Annotation(
        text=("S_plot (the Macbeths plotting Duncan's murder between "
              "the letter and the killing) has no discrete substrate "
              "event — the substrate elides the scheming as implicit "
              "between E_letter_to_lady_macbeth (τ_s=2) and "
              "E_duncan_visits (τ_s=3) → E_duncan_killed (τ_s=5). "
              "The Dramatic Scene is the dialogic centerpiece of the "
              "first act (LM presses, M wavers, the plan is fixed); "
              "the substrate treats it as scene-setting whose effects "
              "show up in the next event's preconditions. PENDING "
              "until macbeth.py is extended with an explicit plotting "
              "event (or the scene is reclassified as a "
              "characterization-only Scene with no substrate "
              "realization)."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=212,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "substrate elides the plotting between the "
                             "letter and the killing"},
)

L_duncan_killing = Lowering(
    id="L_duncan_killing",
    upper_record=_dramatic("S_duncan_killing"),
    lower_records=(_substrate("E_duncan_killed"),),
    annotation=Annotation(
        text=("S_duncan_killing (the play's moral inflection — the "
              "subject brings the dagger; the act is done) realizes as "
              "substrate event E_duncan_killed. The Scene names the "
              "natural-order break and the marriage-bound-by-murder; "
              "the substrate event records killed(macbeth, duncan), "
              "from which kinslayer/regicide/breach_of_hospitality all "
              "derive (under the four RULES) at this moment."),
    ),
    τ_a=213,
    anchor_τ_a=_substrate_event("E_duncan_killed").τ_a,
)

L_discovery_and_crown = Lowering(
    id="L_discovery_and_crown",
    upper_record=_dramatic("S_discovery_and_crown"),
    lower_records=(
        _substrate("E_duncan_discovered"),
        _substrate("E_macbeth_crowned"),
    ),
    annotation=Annotation(
        text=("S_discovery_and_crown bundles two substrate events the "
              "play stages contiguously — Duncan's body discovered "
              "(with the sons fleeing and suspicion turning) and "
              "Macbeth's coronation. The Scene's argumentative work is "
              "the public order's restoration on false foundations; "
              "the substrate keeps them as two events because their "
              "effects differ (one closes the regicide; the other "
              "establishes king(macbeth, scotland), the precondition "
              "the depth-2 TYRANT_RULE eventually fires on)."),
    ),
    τ_a=214,
    anchor_τ_a=_max_event_τ_a("E_duncan_discovered", "E_macbeth_crowned"),
)

L_banquo_killing = Lowering(
    id="L_banquo_killing",
    upper_record=_dramatic("S_banquo_killing"),
    lower_records=(_substrate("E_banquo_killed"),),
    annotation=Annotation(
        text=("S_banquo_killing (M kills for security rather than "
              "necessity; Fleance escapes; the prophecy's other "
              "promise — Banquo's descendants as kings — stays alive) "
              "realizes as substrate event E_banquo_killed. This is "
              "the Scene that widens M's **victim-set** without LM "
              "(she doesn't plan or know in advance); the marriage's "
              "first private fracture. Note: Banquo is NOT Macbeth's "
              "kinsman in the substrate (kinship is authored only "
              "between Macbeth and Duncan, via "
              "E_macbeth_kinsman_of_duncan); 'kinslayer' derives from "
              "the Duncan killing specifically, not from Banquo's. "
              "The Banquo killing is politically-motivated fratricide-"
              "of-a-comrade, structurally distinct."),
    ),
    τ_a=215,
    anchor_τ_a=_substrate_event("E_banquo_killed").τ_a,
)

L_banquet_ghost = Lowering(
    id="L_banquet_ghost",
    upper_record=_dramatic("S_banquet_ghost"),
    lower_records=(_substrate("E_banquet_ghost"),),
    annotation=Annotation(
        text=("S_banquet_ghost (Banquo's apparition at the feast; M "
              "cracks publicly; LM covers) realizes as substrate event "
              "E_banquet_ghost. The substrate authors the apparition "
              "as observation by Macbeth alone (apparition_of(banquo, "
              "the_banquet_hall)) without committing to whether the "
              "ghost is metaphysically real or a guilt-projection — "
              "the dialect-local question the Scene's conflict_shape "
              "leaves open."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=216,
    anchor_τ_a=_substrate_event("E_banquet_ghost").τ_a,
)

L_second_prophecy = Lowering(
    id="L_second_prophecy",
    upper_record=_dramatic("S_second_prophecy"),
    lower_records=(_substrate("E_prophecy_second"),),
    annotation=Annotation(
        text=("S_second_prophecy (M returns to the prophets; he reads "
              "what he hears as protection; the supernatural's bait is "
              "taken) realizes as substrate event E_prophecy_second. "
              "The substrate records three told_by KnowledgeEffects "
              "into M's KNOWN slot — beware-Macduff, none-of-woman-"
              "born, safe-until-Birnam. M's *interpretation* of those "
              "as invulnerability is a derived belief the substrate "
              "doesn't author directly; the dislodgement at τ_s=17 is "
              "where that derivation gets observed in the substrate's "
              "remove_held."),
    ),
    τ_a=217,
    anchor_τ_a=_substrate_event("E_prophecy_second").τ_a,
)

L_macduff_family = Lowering(
    id="L_macduff_family",
    upper_record=_dramatic("S_macduff_family"),
    lower_records=(
        _substrate("E_macduff_flees"),
        _substrate("E_macduff_family_killed"),
    ),
    annotation=Annotation(
        text=("S_macduff_family bundles two substrate events — "
              "Macduff's flight to England (the precondition the "
              "Scene names as 'in his absence') and the slaughter "
              "itself. The Scene names the moral nadir and Macduff's "
              "grief becoming the play's agency-of-restoration; the "
              "substrate event E_macduff_family_killed is also the "
              "candidate trigger for the inference-02 refinement that "
              "tightens tyrant() — the depth-2 TYRANT_RULE fires "
              "earlier (at τ_s=6, on the kinslayer + regicide + king "
              "triple) but innocent-civilian killings are the "
              "intuitive point at which 'tyrant' lands morally."),
    ),
    τ_a=218,
    anchor_τ_a=_max_event_τ_a("E_macduff_flees", "E_macduff_family_killed"),
)

L_sleepwalking = Lowering(
    id="L_sleepwalking",
    upper_record=_dramatic("S_sleepwalking"),
    lower_records=(_substrate("E_sleepwalking"),),
    annotation=Annotation(
        text=("S_sleepwalking (the queen, asleep, performs the "
              "conscience the waking queen suppressed) realizes as "
              "substrate event E_sleepwalking. The Scene names the "
              "secret resurfacing on her side; the substrate records "
              "her utterances and the doctor's overhearing. The "
              "marriage-in-name-only is a Scene-level result the "
              "substrate doesn't directly assert."),
    ),
    τ_a=219,
    anchor_τ_a=_substrate_event("E_sleepwalking").τ_a,
)

L_lady_macbeth_dies = Lowering(
    id="L_lady_macbeth_dies",
    upper_record=_dramatic("S_lady_macbeth_dies"),
    lower_records=(_substrate("E_lady_macbeth_dies"),),
    annotation=Annotation(
        text=("S_lady_macbeth_dies (the death; M's 'tomorrow' "
              "soliloquy as response — exhaustion not grief) realizes "
              "as substrate event E_lady_macbeth_dies. The Scene "
              "names the IC's voice silenced and M's last human "
              "attachment lost; the substrate authors dead("
              "lady_macbeth) and lets the soliloquy stay dialect-"
              "local."),
    ),
    τ_a=220,
    anchor_τ_a=_substrate_event("E_lady_macbeth_dies").τ_a,
)

L_birnam_moves = Lowering(
    id="L_birnam_moves",
    upper_record=_dramatic("S_birnam_moves"),
    lower_records=(_substrate("E_birnam_moves"),),
    annotation=Annotation(
        text=("S_birnam_moves (the army cuts boughs; Macbeth hears the "
              "impossible has happened; the second prophecy's first "
              "protection collapses) realizes as substrate event "
              "E_birnam_moves. The Scene names the prophecy's "
              "literal-truth-and-catastrophic-misleading; the "
              "substrate authors moving_toward(forces, dunsinane) and "
              "M's induction that prophecy_safe_until_birnam_moves is "
              "no longer protective."),
    ),
    τ_a=221,
    anchor_τ_a=_substrate_event("E_birnam_moves").τ_a,
)

L_macbeth_dies = Lowering(
    id="L_macbeth_dies",
    upper_record=_dramatic("S_macbeth_dies"),
    lower_records=(
        _substrate("E_macduff_reveals_birth"),
        _substrate("E_macbeth_killed"),
    ),
    annotation=Annotation(
        text=("S_macbeth_dies bundles two substrate events the play "
              "stages on the same battlefield moment — Macduff's "
              "Caesarean-birth reveal (the second prophecy's last "
              "protection collapses) and the killing itself. The "
              "Scene names the central conflict's resolution; the "
              "substrate keeps them as two events because their "
              "effects differ (one is M's terminal epistemic update — "
              "born_not_of_woman(macduff) at KNOWN, prophecy_none_of_"
              "woman_born dislodged; the other is dead(macbeth) and "
              "killed(macduff, macbeth)). Both at τ_s=17, sequential "
              "τ_a."),
    ),
    τ_a=222,
    anchor_τ_a=_max_event_τ_a("E_macduff_reveals_birth", "E_macbeth_killed"),
)

L_malcolm_crowned = Lowering(
    id="L_malcolm_crowned",
    upper_record=_dramatic("S_malcolm_crowned"),
    lower_records=(_substrate("E_malcolm_crowned"),),
    annotation=Annotation(
        text=("S_malcolm_crowned (the rightful succession restored; "
              "the play closes on the natural order the regicide had "
              "broken) realizes as substrate event E_malcolm_crowned. "
              "The Scene names the resolution; the substrate records "
              "king(malcolm, scotland) + the dislodgement of "
              "king(macbeth, scotland) (the latter via asserts=False "
              "world effect — Macbeth was king until this event; the "
              "removal is the inference-layer cleanup of a fact whose "
              "holder is dead and succeeded)."),
    ),
    τ_a=223,
    anchor_τ_a=_substrate_event("E_malcolm_crowned").τ_a,
)


# ============================================================================
# Throughline → many-events Lowerings (with position_range)
# ============================================================================
#
# Four Throughlines, four position_range Lowerings. Each Throughline
# binds across the substrate events that compose its arc. Where the
# Throughline corresponds to an agent (MC, IC), the lower_records
# focus on events that agent is in or affected by; where the
# Throughline is structural (overall, relationship), the bounds
# include any event that advances it.

L_overall_throughline = Lowering(
    id="L_overall_throughline",
    upper_record=_dramatic("T_overall_scotland"),
    lower_records=(
        _substrate("E_duncan_king_of_scotland"),
        _substrate("E_prophecy_first"),
        _substrate("E_duncan_killed"),
        _substrate("E_duncan_discovered"),
        _substrate("E_macbeth_crowned"),
        _substrate("E_banquo_killed"),
        _substrate("E_macduff_family_killed"),
        _substrate("E_birnam_moves"),
        _substrate("E_macbeth_killed"),
        _substrate("E_malcolm_crowned"),
    ),
    annotation=Annotation(
        text=("T_overall_scotland (the kingdom's situation: rightful "
              "rule disturbed by usurpation, restored by overthrow) "
              "realizes across the substrate events that move "
              "Scotland's order — Duncan's reign as the baseline, the "
              "regicide that breaks it, the tyrant's escalating "
              "violence, the overthrow, and Malcolm's restoration. "
              "position_range frames this as fabula τ_s ∈ [-30, 18] — "
              "from Duncan's authored kingship through Malcolm's "
              "coronation. Side-on-Argument is COMPLICATES: the "
              "kingdom's situation is what *complicates* the premise "
              "rather than directly affirming it."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=230,
    position_range=PositionRange(coord="τ_s", min_value=-30, max_value=18),
    anchor_τ_a=_max_event_τ_a(
        "E_duncan_king_of_scotland", "E_prophecy_first", "E_duncan_killed",
        "E_duncan_discovered", "E_macbeth_crowned", "E_banquo_killed",
        "E_macduff_family_killed", "E_birnam_moves", "E_macbeth_killed",
        "E_malcolm_crowned",
    ),
)

L_mc_throughline = Lowering(
    id="L_mc_throughline",
    upper_record=_dramatic("T_mc_macbeth"),
    lower_records=(
        _substrate("E_macbeth_defends_scotland"),
        _substrate("E_prophecy_first"),
        _substrate("E_thane_of_cawdor_awarded"),
        _substrate("E_letter_to_lady_macbeth"),
        _substrate("E_duncan_killed"),
        _substrate("E_macbeth_crowned"),
        _substrate("E_banquo_killed"),
        _substrate("E_banquet_ghost"),
        _substrate("E_prophecy_second"),
        _substrate("E_macduff_family_killed"),
        _substrate("E_birnam_moves"),
        _substrate("E_macduff_reveals_birth"),
        _substrate("E_macbeth_killed"),
    ),
    annotation=Annotation(
        text=("T_mc_macbeth (the MC's moral descent: hero-defender "
              "through prophecy-touched ambition through unilateral "
              "tyranny through battlefield dissolution) realizes "
              "across the substrate events that compose Macbeth's "
              "trajectory. position_range frames this as fabula τ_s "
              "∈ [-5, 17] — from the battle that earns him the "
              "prophecy through his death. The MC owns 9 beats on "
              "this Throughline; this is also the Throughline whose "
              "Stakes (Stakes_macbeth_soul) include the highest at-"
              "risk: humanity, salvation, life. Side-on-Argument is "
              "AFFIRMS: Macbeth's arc is the Argument's primary "
              "demonstration."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=231,
    position_range=PositionRange(coord="τ_s", min_value=-5, max_value=17),
    anchor_τ_a=_max_event_τ_a(
        "E_macbeth_defends_scotland", "E_prophecy_first",
        "E_thane_of_cawdor_awarded", "E_letter_to_lady_macbeth",
        "E_duncan_killed", "E_macbeth_crowned", "E_banquo_killed",
        "E_banquet_ghost", "E_prophecy_second", "E_macduff_family_killed",
        "E_birnam_moves", "E_macduff_reveals_birth", "E_macbeth_killed",
    ),
)

L_ic_throughline = Lowering(
    id="L_ic_throughline",
    upper_record=_dramatic("T_impact_lady_macbeth"),
    lower_records=(
        _substrate("E_letter_to_lady_macbeth"),
        _substrate("E_duncan_killed"),
        _substrate("E_banquet_ghost"),
        _substrate("E_sleepwalking"),
        _substrate("E_lady_macbeth_dies"),
    ),
    annotation=Annotation(
        text=("T_impact_lady_macbeth (the IC's arc: the woman who "
              "decides for both, presses M past hesitation, then "
              "cannot bear what she carried) realizes across the "
              "substrate events where LM is focal or where her "
              "presence/absence shapes M's action. position_range "
              "frames this as fabula τ_s ∈ [2, 14] — the in-play "
              "lifespan of her dramatic agency, from the letter that "
              "triggers her decision through her death. E_banquo_"
              "killed is omitted: M acts there *without telling her* "
              "— the Scene-level rupture of the partnership. The "
              "counterpoint_throughline_ids edge to T_mc_macbeth "
              "marks her as M's IC across the play."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=232,
    position_range=PositionRange(coord="τ_s", min_value=2, max_value=14),
    anchor_τ_a=_max_event_τ_a(
        "E_letter_to_lady_macbeth", "E_duncan_killed", "E_banquet_ghost",
        "E_sleepwalking", "E_lady_macbeth_dies",
    ),
)

L_relationship_throughline = Lowering(
    id="L_relationship_throughline",
    upper_record=_dramatic("T_relationship_macbeths"),
    lower_records=(
        _substrate("E_letter_to_lady_macbeth"),
        _substrate("E_duncan_killed"),
        _substrate("E_macbeth_crowned"),
        _substrate("E_banquo_killed"),
        _substrate("E_sleepwalking"),
        _substrate("E_lady_macbeth_dies"),
    ),
    annotation=Annotation(
        text=("T_relationship_macbeths (the marriage as character: "
              "shared ambition forged by the letter, bound by the "
              "killing, fractured by Banquo, dissolved by her "
              "sleepwalking and death) realizes across the substrate "
              "events where the partnership advances or breaks. "
              "position_range frames this as fabula τ_s ∈ [2, 14] — "
              "the marriage's in-play duration, identical bounds to "
              "the IC throughline because both end at her death. "
              "E_banquo_killed is included here (unlike on the IC "
              "throughline) because the rupture of *the relationship* "
              "is itself a relationship-event — the marriage advances "
              "negatively when M acts without LM."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=233,
    position_range=PositionRange(coord="τ_s", min_value=2, max_value=14),
    anchor_τ_a=_max_event_τ_a(
        "E_letter_to_lady_macbeth", "E_duncan_killed", "E_macbeth_crowned",
        "E_banquo_killed", "E_sleepwalking", "E_lady_macbeth_dies",
    ),
)


# ============================================================================
# Aggregate
# ============================================================================

LOWERINGS = (
    # Character → Entity (all active)
    L_macbeth, L_lady_macbeth, L_macduff, L_banquo, L_malcolm,
    L_witches, L_duncan, L_lady_macduff, L_fleance,
    # Scene → Event(s) (active + one pending)
    L_prophecy, L_letter, L_plot_pending,
    L_duncan_killing, L_discovery_and_crown,
    L_banquo_killing, L_banquet_ghost, L_second_prophecy,
    L_macduff_family, L_sleepwalking, L_lady_macbeth_dies,
    L_birnam_moves, L_macbeth_dies, L_malcolm_crowned,
    # Throughline → many-events (with position_range)
    L_overall_throughline, L_mc_throughline,
    L_ic_throughline, L_relationship_throughline,
)
