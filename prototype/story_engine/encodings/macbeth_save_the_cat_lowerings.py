"""
macbeth_save_the_cat_lowerings.py — Save the Cat Macbeth ↔ substrate
Lowerings.

Third authored Lowering set (after oedipus_lowerings.py and
macbeth_lowerings.py). Same architecture-sketch-02 A6/A7 pattern:
dialects stand alone; Lowering records say what upper-side record is
realized by what lower-side record(s).

Save the Cat as a dialect pressures the Lowering surface in ways the
Dramatic encodings did not:

- **Beat-centric, not Scene+Beat-centric.** Where Dramatic has both
  Scenes (14 on Macbeth) and per-throughline Beats (25), Save the Cat
  has only Beats (15 canonical slots). The Lowerings here bind beats
  directly to substrate events; there's no Scene-level middle layer.

- **Several beats lower nothing (PENDING).** Four Save the Cat beats
  are dramatic-atmospheric or dramatic-internal moments that the
  substrate does not stage as discrete events:
    - slot 1 (Opening Image) — the heath, storm, witches; the play's
      first tonal establishment. The substrate's pre-play events are
      static kinship/office facts, not an "opening."
    - slot 2 (Theme Stated) — the Witches' "Fair is foul, and foul is
      fair" chant. No substrate event; a Description-layer
      substrate extension could hold it, but it is not there today.
    - slot 6 (Break Into Two) — the moment Macbeth commits to regicide.
      The substrate elides the committing between E_duncan_visits (3)
      and E_duncan_killed (5) — the decision has no event of its own.
    - slot 12 (Dark Night of the Soul) — the "Tomorrow" soliloquy.
      No substrate event; interior speech.
  PENDING status captures this cleanly; the Lowering exists to name
  the gap, not to hide it.

- **Strands need position_range binding across many events.** Mirrors
  how Dramatic Throughlines are lowered in macbeth_lowerings.py —
  each of Save the Cat's two strands binds to a span of substrate
  events with a `position_range` bound. The A strand spans τ_s
  [-100, 18] (pre-play kinship through Malcolm's coronation); the B
  strand spans τ_s [2, 14] (the marriage's in-play lifespan, which
  conveniently matches T_impact_lady_macbeth's bounds from the
  Dramatic encoding).

- **Beat ↔ Scene event overlap is intentional.** Several Save the Cat
  beats lower to the same substrate events that Dramatic Scenes
  already lower to. The substrate is the shared ground truth; both
  dialects read it and name what they see at their own granularity.
  Save the Cat's slot 10 (Bad Guys Close In) lowers to five substrate
  events that macbeth_lowerings.py has across four separate Dramatic
  Scenes. That's the cross-dialect-macbeth-sketch-01 compression
  pattern showing up concretely at the Lowering layer.

Coupling kinds: every Lowering here is Realization (per L1, the only
kind Lowering records carry). The claim-trajectory / claim-moment /
characterization hooks are exercised by macbeth_save_the_cat_
verification.py, not by Lowering records.
"""

from __future__ import annotations

from story_engine.core.substrate import Entity, Event
from story_engine.encodings.macbeth import FABULA, ENTITIES

from story_engine.core.save_the_cat import StcStory, StcBeat, StcStrand
from story_engine.encodings.macbeth_save_the_cat import STORY, BEATS, STRANDS

from story_engine.core.lowering import (
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
# 15 canonical beats, 11 ACTIVE, 4 PENDING. The PENDINGs mark
# dramatic-atmospheric / dramatic-internal moments that have no
# discrete substrate realization (see module docstring).

L_B_01_opening_pending = Lowering(
    id="L_B_01_opening_pending",
    upper_record=_stc("B_01_opening"),
    lower_records=(),
    annotation=Annotation(
        text=("B_01_opening (heath + storm + witches; the play's first "
              "tonal establishment before any human action) has no "
              "substrate event. The substrate's pre-play facts "
              "(E_macbeth_thane_of_glamis at τ_s=-50; "
              "E_duncan_king_of_scotland at τ_s=-30; "
              "E_macbeth_kinsman_of_duncan at τ_s=-100) are static "
              "kinship/office facts, not a staged opening image. The "
              "dialect's Opening Image slot names something the "
              "substrate layer deliberately excludes (mood, tonal "
              "priming). A Description-layer substrate extension could "
              "eventually carry it. PENDING."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=300,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "opening-image tonal priming has no "
                             "substrate-event counterpart"},
)

L_B_02_theme_pending = Lowering(
    id="L_B_02_theme_pending",
    upper_record=_stc("B_02_theme"),
    lower_records=(),
    annotation=Annotation(
        text=("B_02_theme (Witches' 'Fair is foul, and foul is fair') "
              "has no substrate event. The chant is a dramatic speech-"
              "act the play uses to prime the audience's moral "
              "expectations; the substrate does not stage it because "
              "its effect is tonal rather than fact-altering. "
              "PENDING until macbeth.py is extended with a speech-act "
              "record (or the Theme Stated beat is reclassified as a "
              "Description-layer record with no substrate "
              "realization)."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=301,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "theme-statement speech-act is tonal, "
                             "not fact-altering"},
)

L_B_03_setup = Lowering(
    id="L_B_03_setup",
    upper_record=_stc("B_03_setup"),
    lower_records=(
        _substrate("E_macbeth_kinsman_of_duncan"),
        _substrate("E_macbeth_thane_of_glamis"),
        _substrate("E_duncan_king_of_scotland"),
        _substrate("E_macbeth_defends_scotland"),
    ),
    annotation=Annotation(
        text=("B_03_setup (Macbeth as loyal thane; Duncan as king; the "
              "marriage shown intact) realizes across the substrate's "
              "pre-play kinship/office facts plus the opening battle "
              "where Macbeth wins the war for Duncan. The four bound "
              "events establish the status quo the play will break: "
              "kinship (macbeth kinsman_of duncan), office "
              "(thane_of_glamis), political order (king_of_scotland), "
              "and loyalty-in-action (defends_scotland). The marriage "
              "itself is not a substrate event — it's a standing "
              "relationship that becomes salient when the letter "
              "arrives at B_07."),
    ),
    τ_a=302,
    anchor_τ_a=_max_event_τ_a(
        "E_macbeth_kinsman_of_duncan", "E_macbeth_thane_of_glamis",
        "E_duncan_king_of_scotland", "E_macbeth_defends_scotland",
    ),
)

L_B_04_catalyst = Lowering(
    id="L_B_04_catalyst",
    upper_record=_stc("B_04_catalyst"),
    lower_records=(_substrate("E_prophecy_first"),),
    annotation=Annotation(
        text=("B_04_catalyst (the Witches deliver the first prophecy; "
              "the Cawdor half is confirmed within minutes by royal "
              "messengers) realizes as substrate event E_prophecy_"
              "first. The event records the literal prophetic speech-"
              "acts and Macbeth's adoption of prophecy_will_be_king at "
              "KNOWN — which is the catalytic fact-change the dialect "
              "names. Note: E_thane_of_cawdor_awarded (τ_s=1) is the "
              "prophecy's first literalization but is not bound here "
              "— the Catalyst slot is the prophecy itself, not its "
              "first confirmation."),
    ),
    τ_a=303,
    anchor_τ_a=_substrate_event("E_prophecy_first").τ_a,
)

L_B_05_debate = Lowering(
    id="L_B_05_debate",
    upper_record=_stc("B_05_debate"),
    lower_records=(
        _substrate("E_letter_to_lady_macbeth"),
        _substrate("E_duncan_visits"),
    ),
    annotation=Annotation(
        text=("B_05_debate (Macbeth's hesitation meets Lady Macbeth's "
              "pressure; 'If it were done when 'tis done...') realizes "
              "across two substrate events that frame the debate "
              "without being the debate: E_letter_to_lady_macbeth "
              "(τ_s=2; she learns the prophecy and decides for both) "
              "and E_duncan_visits (τ_s=3; the king arrives at the "
              "house, making the deed locally possible). The debate "
              "itself — the verbal back-and-forth between the spouses "
              "— has no discrete substrate event; its effect is "
              "visible only in what follows (E_duncan_killed at "
              "τ_s=5). The dialect's Debate slot is substrate-"
              "elided at its rhetorical core."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=304,
    anchor_τ_a=_max_event_τ_a(
        "E_letter_to_lady_macbeth", "E_duncan_visits",
    ),
)

L_B_06_break_into_two_pending = Lowering(
    id="L_B_06_break_into_two_pending",
    upper_record=_stc("B_06_break_into_two"),
    lower_records=(),
    annotation=Annotation(
        text=("B_06_break_into_two (Macbeth commits: 'I am settled, "
              "and bend up each corporal agent to this terrible "
              "feat') has no substrate event. The committing-to-"
              "regicide moment is dramatic-internal — a change in "
              "Macbeth's mental state between E_duncan_visits (τ_s=3) "
              "and E_duncan_killed (τ_s=5). The substrate records "
              "the deed, not the commitment. PENDING; could be "
              "addressed by a speech-act or intent-forming event in a "
              "future macbeth.py extension (the Dramatic "
              "L_plot_pending records the companion gap on that "
              "side)."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=305,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "commit-to-kill is a mental-state change, "
                             "not a staged event"},
)

L_B_07_b_story = Lowering(
    id="L_B_07_b_story",
    upper_record=_stc("B_07_b_story"),
    lower_records=(_substrate("E_letter_to_lady_macbeth"),),
    annotation=Annotation(
        text=("B_07_b_story (the marriage surfaces as the play's moral "
              "engine; the partnership is most effectively one) "
              "realizes as substrate event E_letter_to_lady_macbeth. "
              "The letter is where the marriage becomes the "
              "conspiracy's carrier — Lady Macbeth reads, chooses for "
              "both, calls on darkness. Same event as B_05_debate "
              "partially binds to: the substrate event is one, the "
              "two dialect beats read different aspects of it. The B "
              "Story slot's job is to surface the marriage as its own "
              "arc distinct from the A plot; this event is the arc's "
              "first movement."),
    ),
    τ_a=306,
    anchor_τ_a=_substrate_event("E_letter_to_lady_macbeth").τ_a,
)

L_B_08_fun_and_games = Lowering(
    id="L_B_08_fun_and_games",
    upper_record=_stc("B_08_fun_and_games"),
    lower_records=(
        _substrate("E_duncan_killed"),
        _substrate("E_duncan_discovered"),
        _substrate("E_macbeth_crowned"),
    ),
    annotation=Annotation(
        text=("B_08_fun_and_games (Duncan murdered, grooms framed, "
              "sons flee, Macbeth crowned — the 'promise of the "
              "premise' sequence where the prophecy literalizes) "
              "realizes across three substrate events spanning τ_s "
              "5-6: the killing, the discovery (with sons fleeing), "
              "and the coronation. The depth-1 rules fire immediately "
              "at τ_s=5: kinslayer, regicide, breach_of_hospitality "
              "all derive from killed(macbeth, duncan) plus the "
              "kinship/office/hospitality facts established in "
              "B_03_setup. The dialect's Fun and Games slot names the "
              "sequence's external ease (Macbeth navigates the new "
              "world of kingship); the substrate records the moral "
              "cost accruing underneath."),
    ),
    τ_a=307,
    anchor_τ_a=_max_event_τ_a(
        "E_duncan_killed", "E_duncan_discovered", "E_macbeth_crowned",
    ),
)

L_B_09_midpoint = Lowering(
    id="L_B_09_midpoint",
    upper_record=_stc("B_09_midpoint"),
    lower_records=(_substrate("E_macbeth_crowned"),),
    annotation=Annotation(
        text=("B_09_midpoint (the coronation; the false stability; the "
              "A and B stories collide because the prophecy's Banquo-"
              "line half means the seized prize is temporary) realizes "
              "as substrate event E_macbeth_crowned. Same event as "
              "B_08's third member: the dialect reads the coronation "
              "as both 'the promise of the premise fulfilled' (B_08) "
              "and 'the midpoint at which the screws tighten' (B_09). "
              "Overlap at the substrate is expected — Save the Cat's "
              "slot boundaries are conceptual, not event-count "
              "boundaries. Past this moment, the depth-2 TYRANT_RULE "
              "becomes derivable (kinslayer + regicide + "
              "king(macbeth, scotland) all now hold)."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=308,
    anchor_τ_a=_substrate_event("E_macbeth_crowned").τ_a,
)

L_B_10_bad_guys_close_in = Lowering(
    id="L_B_10_bad_guys_close_in",
    upper_record=_stc("B_10_bad_guys_close_in"),
    lower_records=(
        _substrate("E_banquo_killed"),
        _substrate("E_banquet_ghost"),
        _substrate("E_prophecy_second"),
        _substrate("E_macduff_flees"),
        _substrate("E_macduff_family_killed"),
    ),
    annotation=Annotation(
        text=("B_10_bad_guys_close_in (Banquo murdered; banquet ghost; "
              "second prophecy; Macduff flees; Macduff family "
              "slaughtered — the rising action's cascade) realizes "
              "across five substrate events spanning τ_s 8-12. This "
              "is the compression instance called out in cross-"
              "dialect-macbeth-sketch-01: the Dramatic encoding "
              "distributes these same events across four separate "
              "Scenes (S_banquo_killing, S_banquet_ghost, "
              "S_second_prophecy, S_macduff_family); Save the Cat "
              "collapses them into one slot because the dialect's "
              "rising-action allocation is singular. Save the Cat "
              "admits multiple events per beat without fuss; what it "
              "loses is the ability to name individual moments "
              "structurally. The substrate carries the moments; the "
              "beat carries the arc-shape claim."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=309,
    anchor_τ_a=_max_event_τ_a(
        "E_banquo_killed", "E_banquet_ghost", "E_prophecy_second",
        "E_macduff_flees", "E_macduff_family_killed",
    ),
)

L_B_11_all_is_lost = Lowering(
    id="L_B_11_all_is_lost",
    upper_record=_stc("B_11_all_is_lost"),
    lower_records=(_substrate("E_lady_macbeth_dies"),),
    annotation=Annotation(
        text=("B_11_all_is_lost (Lady Macbeth dies; the B story's "
              "protagonist is gone; Macbeth is alone with what he has "
              "become) realizes as substrate event "
              "E_lady_macbeth_dies (τ_s=14). This is the B-strand's "
              "terminal event — the marriage ends not with rupture "
              "but with the simple removal of the other person. "
              "E_sleepwalking (τ_s=13) is the immediate precursor "
              "but belongs to the arc's late middle rather than its "
              "terminus; it is bound to the Strand_B_marriage "
              "Lowering below, not here."),
    ),
    τ_a=310,
    anchor_τ_a=_substrate_event("E_lady_macbeth_dies").τ_a,
)

L_B_12_dark_night_pending = Lowering(
    id="L_B_12_dark_night_pending",
    upper_record=_stc("B_12_dark_night"),
    lower_records=(),
    annotation=Annotation(
        text=("B_12_dark_night ('Tomorrow, and tomorrow, and tomorrow' "
              "soliloquy — Macbeth's response to his wife's death) has "
              "no substrate event. The soliloquy is interior speech: "
              "a mental-state snapshot the substrate does not stage. "
              "Its effect is rhetorical and tonal — it records "
              "Macbeth's arrived-at despair — but nothing in the "
              "substrate's world-facts or knowledge-facts changes on "
              "its delivery. PENDING; a substrate extension admitting "
              "speech-acts-with-no-fact-change could carry it, but "
              "the current substrate is deliberately thinner than "
              "that."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=311,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "interior soliloquy changes no facts, "
                             "only tone"},
)

L_B_13_break_into_three = Lowering(
    id="L_B_13_break_into_three",
    upper_record=_stc("B_13_break_into_three"),
    lower_records=(_substrate("E_birnam_moves"),),
    annotation=Annotation(
        text=("B_13_break_into_three (news arrives that Birnam Wood "
              "moves on Dunsinane; the second prophecy's first "
              "protection collapses; Macbeth arms anyway) realizes as "
              "substrate event E_birnam_moves (τ_s=15). The event "
              "records the literal impossible-thing (an army "
              "camouflaged in Birnam boughs) and Macbeth's uptake of "
              "the collapsing prophecy-reading at KNOWN. His 'commit "
              "to the final approach' is substrate-visible only as "
              "his subsequent action (fighting at τ_s=17); the "
              "committing itself is, as at slot 6, dramatic-internal "
              "and not separately staged."),
    ),
    τ_a=312,
    anchor_τ_a=_substrate_event("E_birnam_moves").τ_a,
)

L_B_14_finale = Lowering(
    id="L_B_14_finale",
    upper_record=_stc("B_14_finale"),
    lower_records=(
        _substrate("E_macduff_reveals_birth"),
        _substrate("E_macbeth_killed"),
    ),
    annotation=Annotation(
        text=("B_14_finale (Macbeth faces Macduff; boasts of the "
              "prophecy; Macduff reveals the Caesarean birth; the "
              "last protection collapses; Macbeth fights anyway and "
              "is killed) realizes across two substrate events at "
              "τ_s=17: E_macduff_reveals_birth (the epistemic reveal; "
              "born_not_of_woman(macduff) enters Macbeth's KNOWN set; "
              "the prophecy-protection reading is dislodged) and "
              "E_macbeth_killed (the deed that ends the A plot). "
              "Same two events as the Dramatic encoding's "
              "L_macbeth_dies — both dialects see the finale as two "
              "paired events. The B strand closes alongside: with "
              "Macbeth's death, the marriage has both principals "
              "gone."),
    ),
    τ_a=313,
    anchor_τ_a=_max_event_τ_a(
        "E_macduff_reveals_birth", "E_macbeth_killed",
    ),
)

L_B_15_final_image = Lowering(
    id="L_B_15_final_image",
    upper_record=_stc("B_15_final_image"),
    lower_records=(_substrate("E_malcolm_crowned"),),
    annotation=Annotation(
        text=("B_15_final_image (Malcolm crowned at Scone; the "
              "kingdom names its new king; the play closes on "
              "political order that inverts the supernatural disorder "
              "of the Opening Image) realizes as substrate event "
              "E_malcolm_crowned (τ_s=18). The coronation establishes "
              "king(malcolm, scotland) in the world-facts, completing "
              "the A strand's restoration arc. The 'mirrors and "
              "inverts the Opening Image' claim the dialect makes is "
              "not directly substrate-checkable — the substrate has "
              "no Opening Image beat to mirror against — but the "
              "restoration claim is: a king who is not a tyrant sits "
              "on the throne."),
    ),
    τ_a=314,
    anchor_τ_a=_substrate_event("E_malcolm_crowned").τ_a,
)


# ============================================================================
# Strand Lowerings — StcStrand → many-events (with position_range)
# ============================================================================
#
# Mirrors how Dramatic Throughlines are lowered in macbeth_lowerings.py.
# Each strand binds to the substrate events composing its arc, with a
# position_range bound.

L_Strand_A_scotland = Lowering(
    id="L_Strand_A_scotland",
    upper_record=_stc("Strand_A_scotland"),
    lower_records=(
        _substrate("E_macbeth_kinsman_of_duncan"),
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
        text=("Strand_A_scotland (the political arc: loyal thane → "
              "prophecy → regicide → usurpation → tyranny → overthrow "
              "→ restoration) realizes across the substrate events "
              "that move Scotland's political order. position_range "
              "frames this as fabula τ_s ∈ [-100, 18] — from the "
              "pre-play kinship fact (macbeth kinsman_of duncan, "
              "which later becomes the precondition for "
              "kinslayer/regicide) through Malcolm's coronation. The "
              "A strand spans the widest τ_s range of any record in "
              "this encoding; it's the arc that predates and "
              "postdates every other arc in the play."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=320,
    position_range=PositionRange(coord="τ_s", min_value=-100, max_value=18),
    anchor_τ_a=_max_event_τ_a(
        "E_macbeth_kinsman_of_duncan", "E_duncan_king_of_scotland",
        "E_prophecy_first", "E_duncan_killed", "E_duncan_discovered",
        "E_macbeth_crowned", "E_banquo_killed",
        "E_macduff_family_killed", "E_birnam_moves", "E_macbeth_killed",
        "E_malcolm_crowned",
    ),
)

L_Strand_B_marriage = Lowering(
    id="L_Strand_B_marriage",
    upper_record=_stc("Strand_B_marriage"),
    lower_records=(
        _substrate("E_letter_to_lady_macbeth"),
        _substrate("E_duncan_killed"),
        _substrate("E_banquet_ghost"),
        _substrate("E_sleepwalking"),
        _substrate("E_lady_macbeth_dies"),
    ),
    annotation=Annotation(
        text=("Strand_B_marriage (the marriage arc: partnership → "
              "conspiracy → unified execution → isolation → "
              "sleepwalking → death) realizes across substrate events "
              "where the marriage is focal or where Lady Macbeth's "
              "presence/absence shapes Macbeth's action. "
              "position_range frames this as fabula τ_s ∈ [2, 14] — "
              "the in-play lifespan of her dramatic agency. Identical "
              "τ_s bounds to the Dramatic encoding's T_impact_lady_"
              "macbeth Throughline, a convergence worth noting: "
              "different dialect vocabularies, same substrate span. "
              "E_banquo_killed is omitted (Macbeth acts there without "
              "telling her — the marriage's rupture) for the same "
              "reason it's omitted from L_ic_throughline."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=321,
    position_range=PositionRange(coord="τ_s", min_value=2, max_value=14),
    anchor_τ_a=_max_event_τ_a(
        "E_letter_to_lady_macbeth", "E_duncan_killed",
        "E_banquet_ghost", "E_sleepwalking", "E_lady_macbeth_dies",
    ),
)


# ============================================================================
# Exports
# ============================================================================


LOWERINGS = (
    # Beat → Event(s) (15; 11 ACTIVE, 4 PENDING)
    L_B_01_opening_pending,
    L_B_02_theme_pending,
    L_B_03_setup,
    L_B_04_catalyst,
    L_B_05_debate,
    L_B_06_break_into_two_pending,
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
    L_Strand_A_scotland,
    L_Strand_B_marriage,
)
