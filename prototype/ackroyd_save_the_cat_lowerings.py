"""
ackroyd_save_the_cat_lowerings.py — Save the Cat Ackroyd ↔ substrate
Lowerings.

Companion to macbeth_save_the_cat_lowerings.py. Same pattern: 15
beat Lowerings (some ACTIVE, some PENDING) + 2 strand Lowerings
with position_range. No Story-level Lowering.

Ackroyd's Save the Cat lowerings differ from Macbeth's in three
ways:

- **Fewer PENDING beats.** Macbeth had 4 PENDING (Opening Image,
  Theme Stated, Break Into Two, Dark Night); Ackroyd has 3 (Opening
  Image, Theme Stated, Dark Night). Ackroyd's Break Into Two is
  Poirot's commission by Flora — a staged event with substrate
  witness — so it lowers ACTIVE, unlike Macbeth's internal
  commit-to-kill moment. This is the Whydunit's cleaner genre-fit
  showing up at the Lowering layer: the detective's "I take the
  case" is a public event; the murderer's "I will do this" is
  interior.

- **Substrate-compresses-dialect-expands on the middle.** Four
  beats (Fun and Games, Midpoint, Bad Guys Close In, All Is Lost)
  all lower into E_poirot_investigates. The substrate collapsed
  the novel's long investigation middle into one event; the
  dialect reads four distinct structural phases within it. The
  mirror of Macbeth's situation, where the substrate had four
  events and the dialect (Save the Cat) collapsed them into one
  slot (Bad Guys Close In). Same play, different direction —
  cross-dialect-ackroyd-sketch-01 will call this out.

- **B story more distinct than in Macbeth.** Macbeth's B story
  (marriage) entangled tightly with the A story (political).
  Ackroyd's B story (Flora-Ralph love) is structurally separate:
  Ralph is absent from the A plot's inciting event, Ursula's
  confession is its own beat, the B story's payoff is Ralph's
  public clearing rather than intertwining with the killer's death.
  Save the Cat's A/B strand separation fits Ackroyd's shape better
  than Macbeth's.

Coupling kinds: every Lowering here is Realization (per L1, the
only kind Lowering records carry).
"""

from __future__ import annotations

from substrate import Entity, Event
from ackroyd import FABULA, ENTITIES

from save_the_cat import StcStory, StcBeat, StcStrand
from ackroyd_save_the_cat import STORY, BEATS, STRANDS

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


def _stc(record_id: str) -> CrossDialectRef:
    return cross_ref("save-the-cat", record_id)


def _substrate(record_id: str) -> CrossDialectRef:
    return cross_ref("substrate", record_id)


# ============================================================================
# Beat Lowerings — StcBeat → substrate Event(s)
# ============================================================================
#
# 15 canonical beats; 12 ACTIVE, 3 PENDING. The PENDINGs are beats
# the substrate deliberately does not stage: tonal opening, thematic
# prelude, interior pause before reveal.

L_B_01_opening_pending = Lowering(
    id="L_B_01_opening_pending",
    upper_record=_stc("B_01_opening"),
    lower_records=(),
    annotation=Annotation(
        text=("B_01_opening (the narrator's morning walk home from "
              "the Ferrars house; English-village tone; the "
              "knowledge the doctor carries) has no substrate event. "
              "The opening is tonal — establishing voice and "
              "setting — not fact-altering. Authored facts (doctor, "
              "household standing) come through in B_03_setup's "
              "bindings; the opening image itself has no "
              "discrete substrate counterpart. PENDING."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=400,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "tonal establishment without fact change"},
)

L_B_02_theme_pending = Lowering(
    id="L_B_02_theme_pending",
    upper_record=_stc("B_02_theme"),
    lower_records=(),
    annotation=Annotation(
        text=("B_02_theme ('The truth will out' — Poirot's "
              "rationalist claim implicit in the genre's premise) "
              "has no substrate event. The theme is articulated by "
              "the genre rather than stated in authored dialogue "
              "at a specific event. PENDING; could be addressed if "
              "macbeth.py-style speech-act events are added to "
              "ackroyd.py."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=401,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "theme articulated by genre, not "
                             "by a specific substrate speech-act"},
)

L_B_03_setup = Lowering(
    id="L_B_03_setup",
    upper_record=_stc("B_03_setup"),
    lower_records=(
        _substrate("E_ackroyd_wealthy_widower"),
        _substrate("E_sheppard_is_doctor"),
        _substrate("E_household_standing"),
        _substrate("E_ralph_ursula_secretly_married"),
        _substrate("E_sheppard_blackmails_ferrars"),
    ),
    annotation=Annotation(
        text=("B_03_setup (the village's status quo; the closed-"
              "circle cast in place; the pre-existing tensions) "
              "realizes across five pre-play substrate events that "
              "establish the standing facts: Ackroyd's wealth, "
              "Sheppard's profession and relationships, the household "
              "roles, the Ralph-Ursula secret marriage, and the "
              "Sheppard-Ferrars blackmail campaign. All five at "
              "pre-play τ_s; the setup IS backstory."),
    ),
    τ_a=402,
    anchor_τ_a=_max_event_τ_a(
        "E_ackroyd_wealthy_widower", "E_sheppard_is_doctor",
        "E_household_standing", "E_ralph_ursula_secretly_married",
        "E_sheppard_blackmails_ferrars",
    ),
)

L_B_04_catalyst = Lowering(
    id="L_B_04_catalyst",
    upper_record=_stc("B_04_catalyst"),
    lower_records=(_substrate("E_mrs_ferrars_suicide"),),
    annotation=Annotation(
        text=("B_04_catalyst (Mrs. Ferrars' suicide; the letter in "
              "motion) realizes as substrate event "
              "E_mrs_ferrars_suicide (τ_s=0). The event records "
              "dead(mrs_ferrars), death_was_suicide(mrs_ferrars), "
              "and — authored at the event where its premises all "
              "hold — driver_of_suicide(sheppard, mrs_ferrars) as "
              "rule-head."),
    ),
    τ_a=403,
    anchor_τ_a=_substrate_event("E_mrs_ferrars_suicide").τ_a,
)

L_B_05_debate = Lowering(
    id="L_B_05_debate",
    upper_record=_stc("B_05_debate"),
    lower_records=(_substrate("E_ackroyd_dines_with_sheppard"),),
    annotation=Annotation(
        text=("B_05_debate (the Fernly dinner; Sheppard sits across "
              "from Ackroyd knowing his name is in the letter) "
              "realizes as substrate event "
              "E_ackroyd_dines_with_sheppard (τ_s=1). The 'debate' "
              "— will Sheppard act? — is interior to Sheppard on one "
              "side of the table; the substrate carries the told_by "
              "effect where Ackroyd informs Sheppard the letter "
              "exists, which is the debate's trigger."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=404,
    anchor_τ_a=_substrate_event("E_ackroyd_dines_with_sheppard").τ_a,
)

L_B_06_break_into_two = Lowering(
    id="L_B_06_break_into_two",
    upper_record=_stc("B_06_break_into_two"),
    lower_records=(_substrate("E_flora_summons_poirot"),),
    annotation=Annotation(
        text=("B_06_break_into_two (Poirot accepts Flora's "
              "commission; the detective crosses the threshold into "
              "the case) realizes as substrate event "
              "E_flora_summons_poirot (τ_s=2). Contrast with "
              "Macbeth's slot 6 — which was PENDING because the "
              "commit-to-kill is interior. Ackroyd's protagonist "
              "commit is public, witnessed, staged as a substrate "
              "event. This is the Whydunit's cleaner structural fit "
              "showing up at the Lowering layer."),
    ),
    τ_a=405,
    anchor_τ_a=_substrate_event("E_flora_summons_poirot").τ_a,
)

L_B_07_b_story = Lowering(
    id="L_B_07_b_story",
    upper_record=_stc("B_07_b_story"),
    lower_records=(_substrate("E_ralph_missing"),),
    annotation=Annotation(
        text=("B_07_b_story (Flora's conviction of Ralph's "
              "innocence; the love arc surfaces as the novel's "
              "moral engine) realizes as substrate event "
              "E_ralph_missing (τ_s=2). The event authors "
              "accused_of_murder(ralph_paton, ackroyd) — the public "
              "fact the B story's premise ('the one I love is "
              "telling the truth') pushes against."),
    ),
    τ_a=406,
    anchor_τ_a=_substrate_event("E_ralph_missing").τ_a,
)

L_B_08_fun_and_games = Lowering(
    id="L_B_08_fun_and_games",
    upper_record=_stc("B_08_fun_and_games"),
    lower_records=(_substrate("E_poirot_investigates"),),
    annotation=Annotation(
        text=("B_08_fun_and_games (the investigation's procedural "
              "pleasures) realizes as substrate event "
              "E_poirot_investigates (τ_s=5). The substrate "
              "compresses the novel's long investigation middle "
              "into one event; the dialect reads four distinct "
              "phases within it (this beat, plus Midpoint, Bad Guys "
              "Close In, and All Is Lost below). Cross-dialect-"
              "ackroyd-sketch-01 will document this — the "
              "direction-of-compression opposite to Macbeth's slot "
              "10."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=407,
    anchor_τ_a=_substrate_event("E_poirot_investigates").τ_a,
)

L_B_09_midpoint = Lowering(
    id="L_B_09_midpoint",
    upper_record=_stc("B_09_midpoint"),
    lower_records=(
        _substrate("E_dictaphone_plays"),
        _substrate("E_poirot_investigates"),
    ),
    annotation=Annotation(
        text=("B_09_midpoint (the dictaphone breakthrough) bundles "
              "the earlier substrate event where the alibi is "
              "staged (E_dictaphone_plays at τ_s=1) with the "
              "investigation event where Poirot works out what "
              "happened (E_poirot_investigates at τ_s=5). Same "
              "pattern as the Dramatic dialect's "
              "S_dictaphone_breakthrough Scene — both dialects bind "
              "the same two events at this structural moment, "
              "because the breakthrough IS the intersection of "
              "staged-fact + detective-reasoning."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=408,
    anchor_τ_a=_max_event_τ_a(
        "E_dictaphone_plays", "E_poirot_investigates",
    ),
)

L_B_10_bad_guys_close_in = Lowering(
    id="L_B_10_bad_guys_close_in",
    upper_record=_stc("B_10_bad_guys_close_in"),
    lower_records=(_substrate("E_poirot_investigates"),),
    annotation=Annotation(
        text=("B_10_bad_guys_close_in (the noose tightens — Ursula's "
              "confession, Ralph's exculpation, Sheppard's growing "
              "unease) realizes as substrate event "
              "E_poirot_investigates (τ_s=5) — the third dialect "
              "beat reading this single substrate event. The "
              "substrate compresses the novel's procedural middle; "
              "the dialect sees distinct structural phases within "
              "it."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=409,
    anchor_τ_a=_substrate_event("E_poirot_investigates").τ_a,
)

L_B_11_all_is_lost = Lowering(
    id="L_B_11_all_is_lost",
    upper_record=_stc("B_11_all_is_lost"),
    lower_records=(_substrate("E_poirot_investigates"),),
    annotation=Annotation(
        text=("B_11_all_is_lost (Sheppard's private rock-bottom — "
              "he knows he has been solved; the performance is over) "
              "realizes as substrate event E_poirot_investigates "
              "(τ_s=5) — the fourth dialect beat reading this "
              "single investigation event. In a Whydunit, 'all is "
              "lost' is felt from the killer's side, not the "
              "detective's; the substrate does not stage that "
              "interior moment, but the investigation event's "
              "effects (what Poirot has deduced by this phase) are "
              "what Sheppard-the-narrator knows Poirot knows."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=410,
    anchor_τ_a=_substrate_event("E_poirot_investigates").τ_a,
)

L_B_12_dark_night_pending = Lowering(
    id="L_B_12_dark_night_pending",
    upper_record=_stc("B_12_dark_night"),
    lower_records=(),
    annotation=Annotation(
        text=("B_12_dark_night (the quiet beat before the reveal — "
              "Sheppard's manuscript-composition, Poirot's decision "
              "how to close the case) has no substrate event. "
              "Interior pauses are not staged. PENDING, same "
              "rationale as Macbeth STC's slot 12 PENDING (the "
              "'Tomorrow' soliloquy; interior speech changes no "
              "facts)."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=411,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "interior pause before reveal "
                             "has no substrate event"},
)

L_B_13_break_into_three = Lowering(
    id="L_B_13_break_into_three",
    upper_record=_stc("B_13_break_into_three"),
    lower_records=(_substrate("E_poirot_reveals_solution"),),
    annotation=Annotation(
        text=("B_13_break_into_three (Poirot commits to the "
              "public reveal; the cast is gathered) bundles into "
              "substrate event E_poirot_reveals_solution (τ_s=8). "
              "The commit-to-reveal and the reveal itself are one "
              "substrate event; B_13 and B_14 both lower to it, "
              "reading the anticipation and the execution "
              "respectively."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=412,
    anchor_τ_a=_substrate_event("E_poirot_reveals_solution").τ_a,
)

L_B_14_finale = Lowering(
    id="L_B_14_finale",
    upper_record=_stc("B_14_finale"),
    lower_records=(
        _substrate("E_poirot_reveals_solution"),
        _substrate("E_poirot_private_confrontation"),
    ),
    annotation=Annotation(
        text=("B_14_finale (the drawing-room reveal + the private "
              "ultimatum) bundles two substrate events at τ_s=8 and "
              "τ_s=9. The reveal is public; the private conversation "
              "immediately follows; the dialect sees them as one "
              "finale beat — the Whydunit's signature scene + its "
              "quiet coda. Ralph is cleared publicly at the first "
              "event; Sheppard accepts the ultimatum at the second."),
    ),
    τ_a=413,
    anchor_τ_a=_max_event_τ_a(
        "E_poirot_reveals_solution", "E_poirot_private_confrontation",
    ),
)

L_B_15_final_image = Lowering(
    id="L_B_15_final_image",
    upper_record=_stc("B_15_final_image"),
    lower_records=(
        _substrate("E_sheppard_writes_manuscript"),
        _substrate("E_sheppard_suicide"),
    ),
    annotation=Annotation(
        text=("B_15_final_image (the manuscript's closing paragraph "
              "+ the implied overdose) bundles E_sheppard_writes_"
              "manuscript (τ_s=10) and E_sheppard_suicide (τ_s=11). "
              "The dialect reads the novel's last page and its "
              "implied completion as one closing image — the doctor "
              "at his desk at night, the reverse of the Opening "
              "Image's doctor walking home at morning."),
    ),
    τ_a=414,
    anchor_τ_a=_max_event_τ_a(
        "E_sheppard_writes_manuscript", "E_sheppard_suicide",
    ),
)


# ============================================================================
# Strand Lowerings — StcStrand → many-events (with position_range)
# ============================================================================

L_Strand_A_case = Lowering(
    id="L_Strand_A_case",
    upper_record=_stc("Strand_A_case"),
    lower_records=(
        _substrate("E_mr_ferrars_poisoned"),
        _substrate("E_sheppard_blackmails_ferrars"),
        _substrate("E_mrs_ferrars_suicide"),
        _substrate("E_ackroyd_dines_with_sheppard"),
        _substrate("E_sheppard_murders_ackroyd"),
        _substrate("E_body_discovered"),
        _substrate("E_flora_summons_poirot"),
        _substrate("E_poirot_investigates"),
        _substrate("E_poirot_reveals_solution"),
        _substrate("E_poirot_private_confrontation"),
        _substrate("E_sheppard_suicide"),
    ),
    annotation=Annotation(
        text=("Strand_A_case (the investigation arc: setup → "
              "inciting crime → investigation → reveal → aftermath) "
              "realizes across the substrate events that move the "
              "external case. position_range frames this as fabula "
              "τ_s ∈ [-20, 11] — the same span as the Dramatic "
              "dialect's T_overall_case Throughline. Two dialects "
              "reading the same substrate window: the Whydunit's "
              "external plot."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=420,
    position_range=PositionRange(coord="τ_s", min_value=-20, max_value=11),
    anchor_τ_a=_max_event_τ_a(
        "E_mr_ferrars_poisoned", "E_sheppard_blackmails_ferrars",
        "E_mrs_ferrars_suicide", "E_ackroyd_dines_with_sheppard",
        "E_sheppard_murders_ackroyd", "E_body_discovered",
        "E_flora_summons_poirot", "E_poirot_investigates",
        "E_poirot_reveals_solution",
        "E_poirot_private_confrontation", "E_sheppard_suicide",
    ),
)

L_Strand_B_flora_ralph = Lowering(
    id="L_Strand_B_flora_ralph",
    upper_record=_stc("Strand_B_flora_ralph"),
    lower_records=(
        _substrate("E_ralph_ursula_secretly_married"),
        _substrate("E_ralph_missing"),
        _substrate("E_flora_summons_poirot"),
        _substrate("E_poirot_investigates"),
        _substrate("E_poirot_reveals_solution"),
    ),
    annotation=Annotation(
        text=("Strand_B_flora_ralph (the love arc: engagement, "
              "marriage-to-other, disappearance, accusation, "
              "vindication) realizes across the substrate events "
              "where the love's shape is visible or its "
              "implications surface. position_range frames this as "
              "fabula τ_s ∈ [-10, 8] — from the pre-play secret "
              "marriage through the public reveal that clears "
              "Ralph. Ursula's confession within "
              "E_poirot_investigates is what turns the B arc's "
              "visible state; the reveal at E_poirot_reveals_"
              "solution is its payoff."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=421,
    position_range=PositionRange(coord="τ_s", min_value=-10, max_value=8),
    anchor_τ_a=_max_event_τ_a(
        "E_ralph_ursula_secretly_married", "E_ralph_missing",
        "E_flora_summons_poirot", "E_poirot_investigates",
        "E_poirot_reveals_solution",
    ),
)


# ============================================================================
# Exports
# ============================================================================


LOWERINGS = (
    # Beat → Event(s) (15; 12 ACTIVE, 3 PENDING)
    L_B_01_opening_pending,
    L_B_02_theme_pending,
    L_B_03_setup,
    L_B_04_catalyst,
    L_B_05_debate,
    L_B_06_break_into_two,
    L_B_07_b_story,
    L_B_08_fun_and_games,
    L_B_09_midpoint,
    L_B_10_bad_guys_close_in,
    L_B_11_all_is_lost,
    L_B_12_dark_night_pending,
    L_B_13_break_into_three,
    L_B_14_finale,
    L_B_15_final_image,

    # Strand → many-events (2; both ACTIVE with position_range)
    L_Strand_A_case, L_Strand_B_flora_ralph,
)
