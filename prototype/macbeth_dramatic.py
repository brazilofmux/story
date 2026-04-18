"""
macbeth_dramatic.py — *Macbeth* encoded in the Dramatic dialect.

Second encoding at the Dramatic dialect level (parallel to
oedipus_dramatic.py). Records the play's argumentative structure:
one Argument, four Throughlines under the dramatica-8 Template,
nine Characters, fourteen Scenes, four Stakes records,
twenty-one Beats.

Pure dialect content. No substrate references; no Lowering records.
This file pressures the Dramatic dialect on Macbeth's structurally
distinctive features (lowering-sketch-02), which Oedipus did not
exhibit:

- **Action-first MC.** Macbeth acts on the prophecy; the Throughline
  is about *doing*, not investigating. Argument contribution AFFIRMS.

- **Moral inversion rather than epistemic inversion.** The MC's
  Throughline is a descent through escalating killings, not a single
  anagnorisis moment. Beats reflect cumulative deterioration.

- **Multi-antagonist readings.** Macbeth has multiple defensible
  Antagonist assignments: Macduff (kills the MC at end), Lady Macbeth
  (drives initial regicide), the Witches (manipulate), Macbeth
  himself (self-destroying). This encoding picks Macduff as
  Antagonist on the structural-narrative-resolution criterion;
  the alternatives are documented but not encoded. A future
  encoding could exercise the verifier's overfilled-slot path by
  authoring two Antagonist labels.

- **Supernatural Throughline participants.** The Witches are encoded
  as one collective Character (matching macbeth.py's substrate
  encoding) carrying the Guardian function (the "warns of
  consequences" reading per Dramatica). Their non-human nature is
  a substrate concern; the dialect treats them as one Character
  among others.

- **Cumulative Judgment.** The MC Throughline's Beats track the
  trajectory: hero → first regicide → ordering second killing →
  ordering innocent killings → public unraveling at the banquet →
  doubling down on prophecy → moral nadir at Macduff family →
  realization the prophecy's protection fails → death. Six beats,
  each removing a moral inhibition.

- **Four genuinely independent Stakes records.** Unlike Oedipus
  (where Jocasta's and the Relationship's stakes are entwined with
  MC and Overall), Macbeth's four Throughlines have separable
  stakes (Macbeth's soul, Scotland's order, the marriage's
  existence, Lady Macbeth's sanity). All four are authored, so the
  verifier should produce zero throughline_no_stakes observations.

Expected verifier output (the encoding's contract):

- 0 slot_unfilled / slot_overfilled (all 8 dramatica-8 slots filled,
  exactly one each).
- 0 throughline_no_stakes (all 4 Throughlines have Stakes).
- 0 id_unresolved, no orphans, no duplicate positions, no scene-no-
  purpose observations.

A successful clean run on Macbeth — given that Oedipus produces 3
observations on the same dialect — is itself a finding: the dialect
admits both encodings without revision, and the verifier's output is
sensitive to authorial choices, not noise.

Run the M8 self-verifier on the encoding via:

    python3 -c 'import macbeth_dramatic as m; \
                from dramatic import verify, group_by_code; \
                obs = verify(m.STORY, arguments=m.ARGUMENTS, \
                             throughlines=m.THROUGHLINES, \
                             characters=m.CHARACTERS, scenes=m.SCENES, \
                             beats=m.BEATS, stakes=m.STAKES); \
                print(f"observations: {len(obs)}"); \
                [print(f"  [{x.severity}] {x.code}: {x.message[:80]}") \
                 for x in obs]'
"""

from __future__ import annotations

from dramatic import (
    Story, Argument, Throughline, Character, Beat, Scene, Stakes,
    ArgumentContribution, SceneAdvancement, StakesOwner,
    ResolutionDirection, ArgumentSide, StakesOwnerKind,
    THROUGHLINE_OWNER_SITUATION, THROUGHLINE_OWNER_RELATIONSHIP,
)


# ============================================================================
# Argument
# ============================================================================

A_ambition_unmakes = Argument(
    id="A_ambition_unmakes",
    premise="unchecked ambition unmakes the one who indulges it",
    counter_premise=("ambition is what elevates; restraint is the "
                     "passive choice of the mediocre. Lady Macbeth "
                     "voices this position in Act 1; the play's "
                     "trajectory is the systematic refutation of it"),
    resolution_direction=ResolutionDirection.AFFIRM,
    domain="moral-philosophical",
)

ARGUMENTS = (A_ambition_unmakes,)


# ============================================================================
# Throughlines
# ============================================================================

T_overall_scotland = Throughline(
    id="T_overall_scotland",
    role_label="overall-story",
    owners=(THROUGHLINE_OWNER_SITUATION,),
    subject=("a kingdom usurped by unnatural means; its rightful "
             "succession at stake; a tyrant on the throne until the "
             "natural order reasserts"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_ambition_unmakes",
            side=ArgumentSide.COMPLICATES,
        ),
    ),
    stakes_id="Stakes_scotland",
)

T_mc_macbeth = Throughline(
    id="T_mc_macbeth",
    role_label="main-character",
    owners=("C_macbeth",),
    subject=("a capable warrior who acts on ambition and cannot stop, "
             "escalating from regicide through ordered killings to "
             "innocent slaughter; finally undone by the prophecy he "
             "trusted to protect him"),
    counterpoint_throughline_ids=("T_impact_lady_macbeth",),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_ambition_unmakes",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_macbeth_soul",
)

T_impact_lady_macbeth = Throughline(
    id="T_impact_lady_macbeth",
    role_label="impact-character",
    owners=("C_lady_macbeth",),
    subject=("a woman who demands the killing and then cannot bear "
             "what she demanded; the play's most direct embodiment of "
             "ambition's recoil"),
    counterpoint_throughline_ids=("T_mc_macbeth",),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_ambition_unmakes",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_lady_macbeth_sanity",
)

T_relationship_macbeths = Throughline(
    id="T_relationship_macbeths",
    role_label="relationship",
    owners=(THROUGHLINE_OWNER_RELATIONSHIP,),
    subject=("a marriage-as-conspiracy; once the conspiracy succeeds, "
             "the marriage has no other content and curdles into "
             "mutual isolation"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_ambition_unmakes",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_marriage",
)

THROUGHLINES = (
    T_overall_scotland, T_mc_macbeth, T_impact_lady_macbeth,
    T_relationship_macbeths,
)


# ============================================================================
# Characters
# ============================================================================
#
# dramatica-8 slot assignment for this encoding:
#
#   Protagonist  → C_macbeth
#   Antagonist   → C_macduff   (alternative readings noted below)
#   Reason       → C_malcolm
#   Emotion      → C_macbeth   (also Protagonist; Dramatica admits
#                              double-function MCs)
#   Skeptic      → C_macduff   (also Antagonist; flees in Act 4
#                              because skeptical of Macbeth's
#                              legitimacy)
#   Sidekick     → C_banquo    (loyal until killed)
#   Guardian     → C_witches   (warn-of-consequences reading; their
#                              prophecies forecast outcomes)
#   Contagonist  → C_lady_macbeth  (drives the protagonist into the
#                                  wrong action)
#
# Multi-antagonist alternatives (NOT encoded, but documented):
#
#   - C_lady_macbeth as Antagonist (Act 1-2 reading: she drives the
#     initial murder; she is the antagonistic force the MC fights
#     against in his hesitation)
#   - C_witches as Antagonist (the manipulators-of-fate reading)
#   - C_macbeth as his own Antagonist (the self-destruction reading)
#
# A future encoding could exercise the verifier's overfilled-slot
# path by authoring multiple Antagonist labels. This encoding picks
# Macduff for the structural-narrative-resolution criterion (he
# delivers the killing blow that ends the play's central conflict).

C_macbeth = Character(
    id="C_macbeth", name="Macbeth",
    function_labels=("Protagonist", "Emotion"),
)

C_lady_macbeth = Character(
    id="C_lady_macbeth", name="Lady Macbeth",
    function_labels=("Contagonist",),
)

C_macduff = Character(
    id="C_macduff", name="Macduff",
    function_labels=("Antagonist", "Skeptic"),
)

C_banquo = Character(
    id="C_banquo", name="Banquo",
    function_labels=("Sidekick",),
)

C_malcolm = Character(
    id="C_malcolm", name="Malcolm",
    function_labels=("Reason",),
)

C_witches = Character(
    id="C_witches", name="the Weird Sisters",
    function_labels=("Guardian",),
)

# Characters present in events but carrying no Dramatica function
# (victims, supporting figures). Their inclusion in the Story's
# character_ids is what distinguishes "in this Story" from "absent
# from the cast"; they have no slot to fill or under-fill.

C_duncan = Character(
    id="C_duncan", name="Duncan",
    function_labels=(),
)

C_lady_macduff = Character(
    id="C_lady_macduff", name="Lady Macduff",
    function_labels=(),
)

C_fleance = Character(
    id="C_fleance", name="Fleance",
    function_labels=(),
)

CHARACTERS = (
    C_macbeth, C_lady_macbeth, C_macduff, C_banquo, C_malcolm,
    C_witches, C_duncan, C_lady_macduff, C_fleance,
)


# ============================================================================
# Beats — per Throughline, ordered by beat_position
# ============================================================================

BEATS = (
    # T_overall_scotland — Scotland's arc from Macbeth's coup to
    # Malcolm's restoration
    Beat(id="B_op_1", throughline_id="T_overall_scotland",
         beat_position=1, beat_type="inciting",
         description_of_change=("Witches name Macbeth king-hereafter; "
                                "the kingdom's succession is in "
                                "question before any human acts")),
    Beat(id="B_op_2", throughline_id="T_overall_scotland",
         beat_position=2, beat_type="rising",
         description_of_change=("Duncan murdered, Malcolm flees; "
                                "natural succession is broken; "
                                "Macbeth crowned through usurpation")),
    Beat(id="B_op_3", throughline_id="T_overall_scotland",
         beat_position=3, beat_type="midpoint",
         description_of_change=("Banquo killed and Macduff family "
                                "slaughtered; tyranny extends from "
                                "political necessity to indiscriminate "
                                "killing")),
    Beat(id="B_op_4", throughline_id="T_overall_scotland",
         beat_position=4, beat_type="climax",
         description_of_change=("Birnam Wood moves; Macbeth's "
                                "supernatural protection collapses; "
                                "Macduff kills Macbeth")),
    Beat(id="B_op_5", throughline_id="T_overall_scotland",
         beat_position=5, beat_type="denouement",
         description_of_change=("Malcolm crowned; rightful order "
                                "restored; the kingdom can begin "
                                "again")),

    # T_mc_macbeth — the moral descent, beat by escalating beat
    Beat(id="B_mc_1", throughline_id="T_mc_macbeth",
         beat_position=1, beat_type="inciting",
         description_of_change=("hero of Scotland meets prophecy; "
                                "ambition kindled but not yet "
                                "committed")),
    Beat(id="B_mc_2", throughline_id="T_mc_macbeth",
         beat_position=2, beat_type="rising",
         description_of_change=("plots Duncan's murder under his own "
                                "roof; first decisive moral threshold "
                                "crossed mentally")),
    Beat(id="B_mc_3", throughline_id="T_mc_macbeth",
         beat_position=3, beat_type="rising",
         description_of_change=("kills Duncan; the regicide that "
                                "founds the trajectory; cannot say "
                                "'amen'")),
    Beat(id="B_mc_4", throughline_id="T_mc_macbeth",
         beat_position=4, beat_type="rising",
         description_of_change=("orders Banquo killed; first cold "
                                "calculation; killing for security "
                                "rather than necessity")),
    Beat(id="B_mc_5", throughline_id="T_mc_macbeth",
         beat_position=5, beat_type="midpoint",
         description_of_change=("the banquet ghost; the public crack "
                                "in the king's composure; the secret "
                                "leaks at the surface")),
    Beat(id="B_mc_6", throughline_id="T_mc_macbeth",
         beat_position=6, beat_type="rising",
         description_of_change=("doubles down on the second prophecy; "
                                "supernatural certainty mistaken for "
                                "protection")),
    Beat(id="B_mc_7", throughline_id="T_mc_macbeth",
         beat_position=7, beat_type="rising",
         description_of_change=("orders Macduff family killed; the "
                                "moral nadir; tyranny targeting "
                                "innocents with no political pretext")),
    Beat(id="B_mc_8", throughline_id="T_mc_macbeth",
         beat_position=8, beat_type="climax",
         description_of_change=("Birnam Wood moves to Dunsinane; the "
                                "first of the second-encounter "
                                "prophecy's protective readings "
                                "collapses; Macbeth hears the "
                                "impossible has happened and still "
                                "commits to fighting. The companion "
                                "Macduff Caesarean-birth reveal is "
                                "elided at the beat layer in this "
                                "encoding — its narrative force is "
                                "absorbed into B_mc_9 (the killing "
                                "itself), so no separate Scene/Beat "
                                "pair")),
    Beat(id="B_mc_9", throughline_id="T_mc_macbeth",
         beat_position=9, beat_type="denouement",
         description_of_change=("killed by Macduff; the descent's "
                                "terminus; the tyrant overthrown")),

    # T_impact_lady_macbeth — the IC's parallel descent
    Beat(id="B_ic_1", throughline_id="T_impact_lady_macbeth",
         beat_position=1, beat_type="inciting",
         description_of_change=("reads the letter; chooses for both "
                                "of them; calls on darkness to "
                                "unsex her")),
    Beat(id="B_ic_2", throughline_id="T_impact_lady_macbeth",
         beat_position=2, beat_type="rising",
         description_of_change=("chides Macbeth into the killing; "
                                "handles the daggers; smears the "
                                "grooms' blood; her capacity to act "
                                "on ambition peaks here")),
    Beat(id="B_ic_3", throughline_id="T_impact_lady_macbeth",
         beat_position=3, beat_type="midpoint",
         description_of_change=("at the banquet, covers for Macbeth's "
                                "fit but cannot reach him; the "
                                "marriage's collaboration is failing")),
    Beat(id="B_ic_4", throughline_id="T_impact_lady_macbeth",
         beat_position=4, beat_type="climax",
         description_of_change=("sleepwalking; the unraveling shows; "
                                "'all the perfumes of Arabia will not "
                                "sweeten this little hand'")),
    Beat(id="B_ic_5", throughline_id="T_impact_lady_macbeth",
         beat_position=5, beat_type="denouement",
         description_of_change=("dies; the IC's voice silenced; "
                                "ambition's recoil completed in her "
                                "before it kills the MC")),

    # T_relationship_macbeths — the marriage's arc
    Beat(id="B_rel_1", throughline_id="T_relationship_macbeths",
         beat_position=1, beat_type="inciting",
         description_of_change=("the letter announces the prophecy; "
                                "the marriage gains a shared project")),
    Beat(id="B_rel_2", throughline_id="T_relationship_macbeths",
         beat_position=2, beat_type="rising",
         description_of_change=("the plot to kill Duncan unifies them; "
                                "the marriage becomes a conspiracy")),
    Beat(id="B_rel_3", throughline_id="T_relationship_macbeths",
         beat_position=3, beat_type="midpoint",
         description_of_change=("after Duncan's killing they are "
                                "still partners; this is the marriage "
                                "at its fullest collaboration")),
    Beat(id="B_rel_4", throughline_id="T_relationship_macbeths",
         beat_position=4, beat_type="rising",
         description_of_change=("Macbeth orders Banquo killed without "
                                "telling her; the conspiracy becomes "
                                "his alone; the marriage starts "
                                "isolating")),
    Beat(id="B_rel_5", throughline_id="T_relationship_macbeths",
         beat_position=5, beat_type="climax",
         description_of_change=("by the sleepwalking, they live in "
                                "different houses of the same horror; "
                                "the marriage exists in name only")),
    Beat(id="B_rel_6", throughline_id="T_relationship_macbeths",
         beat_position=6, beat_type="denouement",
         description_of_change=("she dies; Macbeth's response is the "
                                "'tomorrow' soliloquy; the marriage "
                                "ends, having ended long before")),
)


# ============================================================================
# Scenes
# ============================================================================

S_prophecy = Scene(
    id="S_prophecy", title="The Witches' first prophecy",
    narrative_position=1,
    advances=(
        SceneAdvancement(throughline_id="T_overall_scotland", beat_id="B_op_1"),
        SceneAdvancement(throughline_id="T_mc_macbeth",       beat_id="B_mc_1"),
    ),
    conflict_shape=("the supernatural addresses the human; an "
                    "ambition that hadn't named itself receives a "
                    "name and a path"),
    result=("Macbeth holds the prophecy; the question of what to "
            "do with it now exists in him"),
)

S_letter = Scene(
    id="S_letter", title="Lady Macbeth reads the letter",
    narrative_position=2,
    advances=(
        SceneAdvancement(throughline_id="T_relationship_macbeths", beat_id="B_rel_1"),
        SceneAdvancement(throughline_id="T_impact_lady_macbeth",   beat_id="B_ic_1"),
    ),
    conflict_shape=("a letter arrives announcing prophecy; a wife "
                    "reads it and decides for both, before her "
                    "husband returns"),
    result=("the marriage now contains the prophecy as a shared "
            "secret; LM has chosen what they will do"),
)

S_plot = Scene(
    id="S_plot", title="The Macbeths plot Duncan's murder",
    narrative_position=3,
    advances=(
        SceneAdvancement(throughline_id="T_relationship_macbeths", beat_id="B_rel_2"),
        SceneAdvancement(throughline_id="T_impact_lady_macbeth",   beat_id="B_ic_2"),
        SceneAdvancement(throughline_id="T_mc_macbeth",            beat_id="B_mc_2"),
    ),
    conflict_shape=("Macbeth wavers; LM presses; her resolve carries "
                    "his hesitation; the plan is fixed"),
    result=("the plot is set; Macbeth has crossed the moral threshold "
            "mentally even before the act"),
)

S_duncan_killing = Scene(
    id="S_duncan_killing", title="The killing of Duncan",
    narrative_position=4,
    advances=(
        SceneAdvancement(throughline_id="T_overall_scotland", beat_id="B_op_2"),
        SceneAdvancement(throughline_id="T_mc_macbeth",       beat_id="B_mc_3"),
        SceneAdvancement(throughline_id="T_relationship_macbeths", beat_id="B_rel_3"),
    ),
    conflict_shape=("the king sleeps under his subject's roof; the "
                    "subject brings the dagger; the act is done"),
    result=("Duncan dead; the natural order broken; the marriage "
            "bound now by murder; Macbeth cannot say 'amen'"),
)

S_discovery_and_crown = Scene(
    id="S_discovery_and_crown",
    title="Duncan discovered; sons flee; Macbeth crowned",
    narrative_position=5,
    advances=(
        SceneAdvancement(throughline_id="T_overall_scotland", beat_id="B_op_2"),
    ),
    conflict_shape=("the body found; suspicion turns; Malcolm and "
                    "Donalbain flee, taking suspicion with them; "
                    "Macbeth ascends without contest"),
    result=("Macbeth is king; the public order is restored on "
            "false foundations"),
)

S_banquo_killing = Scene(
    id="S_banquo_killing", title="The killing of Banquo",
    narrative_position=6,
    advances=(
        SceneAdvancement(throughline_id="T_mc_macbeth",            beat_id="B_mc_4"),
        SceneAdvancement(throughline_id="T_overall_scotland",      beat_id="B_op_3"),
        SceneAdvancement(throughline_id="T_relationship_macbeths", beat_id="B_rel_4"),
    ),
    conflict_shape=("the king plots against the friend; the killing "
                    "succeeds on the friend but the friend's son "
                    "escapes; the prophecy's other promise stays "
                    "alive"),
    result=("Banquo dead; Fleance fled; Macbeth has killed for "
            "security rather than necessity, and done it without "
            "telling LM"),
)

S_banquet_ghost = Scene(
    id="S_banquet_ghost", title="The banquet — Banquo's ghost",
    narrative_position=7,
    advances=(
        SceneAdvancement(throughline_id="T_mc_macbeth",            beat_id="B_mc_5"),
        SceneAdvancement(throughline_id="T_impact_lady_macbeth",   beat_id="B_ic_3"),
    ),
    conflict_shape=("a king hosts a feast; the murdered friend "
                    "appears at the table; the king cracks publicly; "
                    "the queen covers"),
    result=("the secret has surfaced once; the public has seen the "
            "king unhinged; LM cannot reach him through the cover"),
)

S_second_prophecy = Scene(
    id="S_second_prophecy", title="The Witches' second prophecy",
    narrative_position=8,
    advances=(
        SceneAdvancement(throughline_id="T_mc_macbeth", beat_id="B_mc_6"),
    ),
    conflict_shape=("the king returns to the prophets; he asks for "
                    "certainty; he receives statements he can read "
                    "as protection"),
    result=("Macbeth interprets the prophecies as invulnerability; "
            "he doubles down, takes the bait the supernatural laid"),
)

S_macduff_family = Scene(
    id="S_macduff_family", title="The Macduff family slaughtered",
    narrative_position=9,
    advances=(
        SceneAdvancement(throughline_id="T_mc_macbeth",       beat_id="B_mc_7"),
        SceneAdvancement(throughline_id="T_overall_scotland", beat_id="B_op_3"),
    ),
    conflict_shape=("Macduff has fled to England; in his absence the "
                    "tyrant strikes at what he left behind; murderers "
                    "kill wife and children"),
    result=("the moral nadir reached; tyranny no longer has even a "
            "political pretext; Macduff's grief becomes the play's "
            "agency-of-restoration"),
)

S_sleepwalking = Scene(
    id="S_sleepwalking", title="Lady Macbeth sleepwalks",
    narrative_position=10,
    advances=(
        SceneAdvancement(throughline_id="T_impact_lady_macbeth",   beat_id="B_ic_4"),
        SceneAdvancement(throughline_id="T_relationship_macbeths", beat_id="B_rel_5"),
    ),
    conflict_shape=("the queen, asleep, performs the conscience the "
                    "waking queen suppressed; doctor and gentlewoman "
                    "watch; she cannot wash the imagined blood"),
    result=("the secret has surfaced again, this time on her side; "
            "the doctor knows too much; the marriage now exists in "
            "name only"),
)

S_lady_macbeth_dies = Scene(
    id="S_lady_macbeth_dies", title="The death of Lady Macbeth",
    narrative_position=11,
    advances=(
        SceneAdvancement(throughline_id="T_impact_lady_macbeth",   beat_id="B_ic_5"),
        SceneAdvancement(throughline_id="T_relationship_macbeths", beat_id="B_rel_6"),
    ),
    conflict_shape=("the king receives news of his wife's death; "
                    "his answer is the 'tomorrow' soliloquy — "
                    "exhaustion not grief"),
    result=("LM is dead; the IC's voice silenced; the marriage "
            "ends; Macbeth has lost his last human attachment"),
)

S_birnam_moves = Scene(
    id="S_birnam_moves", title="Birnam Wood moves",
    narrative_position=12,
    advances=(
        SceneAdvancement(throughline_id="T_overall_scotland", beat_id="B_op_4"),
        SceneAdvancement(throughline_id="T_mc_macbeth",       beat_id="B_mc_8"),
    ),
    conflict_shape=("Malcolm's army cuts boughs from Birnam; Macbeth "
                    "hears the impossible has happened; the second "
                    "prophecy's first protection collapses"),
    result=("Macbeth's confidence cracks but he fights; the prophecy "
            "is literally true and catastrophically misleading"),
)

S_macbeth_dies = Scene(
    id="S_macbeth_dies", title="Macduff kills Macbeth",
    narrative_position=13,
    advances=(
        SceneAdvancement(throughline_id="T_mc_macbeth",       beat_id="B_mc_9"),
        SceneAdvancement(throughline_id="T_overall_scotland", beat_id="B_op_4"),
    ),
    conflict_shape=("Macduff faces the man who killed his family; "
                    "Macbeth boasts of the prophecy; Macduff reveals "
                    "the Caesarean birth; the prophecy's last "
                    "protection collapses; Macbeth fights anyway"),
    result=("Macbeth killed; the tyrant overthrown; the play's "
            "central conflict resolved"),
)

S_malcolm_crowned = Scene(
    id="S_malcolm_crowned", title="Malcolm crowned",
    narrative_position=14,
    advances=(
        SceneAdvancement(throughline_id="T_overall_scotland", beat_id="B_op_5"),
    ),
    conflict_shape=("the lords gather; Malcolm receives the crown; "
                    "the kingdom acknowledges its rightful heir"),
    result=("Malcolm is king; rightful order restored; the play "
            "closes on the natural succession the regicide had "
            "broken"),
)

SCENES = (
    S_prophecy, S_letter, S_plot, S_duncan_killing,
    S_discovery_and_crown, S_banquo_killing, S_banquet_ghost,
    S_second_prophecy, S_macduff_family, S_sleepwalking,
    S_lady_macbeth_dies, S_birnam_moves, S_macbeth_dies,
    S_malcolm_crowned,
)


# ============================================================================
# Stakes
# ============================================================================

Stakes_macbeth_soul = Stakes(
    id="Stakes_macbeth_soul",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T_mc_macbeth"),
    at_risk=("Macbeth's humanity — his capacity to feel horror at "
             "what he has done; his salvation in any cosmic sense; "
             "his ability to live with himself; ultimately his life"),
    to_gain=("the throne, briefly; the satisfaction of having "
             "outpaced his own moral hesitations; the vindication "
             "of the prophecy he chose to act on"),
    external_manifestation=("the cumulative killings; his inability "
                            "to say 'amen' after the regicide; the "
                            "banquet ghost; the 'tomorrow' soliloquy; "
                            "his end on the battlefield"),
)

Stakes_scotland = Stakes(
    id="Stakes_scotland",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T_overall_scotland"),
    at_risk=("the kingdom's natural succession; the polity's "
             "capacity to hold its own moral order; the safety of "
             "its subjects under tyranny"),
    to_gain=("restoration to the rightful king; the return of "
             "natural order; the end of the unnatural omens "
             "(disrupted weather, animals devouring each other) "
             "Shakespeare frames the usurpation through"),
    external_manifestation=("the offstage portents; Macduff's family "
                            "killed; the army that finally takes "
                            "Dunsinane; Malcolm's coronation"),
)

Stakes_lady_macbeth_sanity = Stakes(
    id="Stakes_lady_macbeth_sanity",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T_impact_lady_macbeth"),
    at_risk=("Lady Macbeth's mind — her capacity to bear what she "
             "demanded; her ability to keep her crime separate from "
             "her sleep; ultimately her life"),
    to_gain=("the queenship she wanted before she had it; the "
             "vindication of having been the one strong enough to "
             "act"),
    external_manifestation=("the sleepwalking; her death (cause "
                            "unspecified, suicide implied); the "
                            "doctor's report"),
)

Stakes_marriage = Stakes(
    id="Stakes_marriage",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T_relationship_macbeths"),
    at_risk=("the marriage's existence as a partnership; the only "
             "human bond either of them retains"),
    to_gain=("a shared throne; the consummation of a project they "
             "undertook together"),
    external_manifestation=("their conversations growing colder "
                            "across the play; Macbeth ordering "
                            "Banquo's killing without telling LM; "
                            "the sleepwalking she does alone; his "
                            "'tomorrow' soliloquy on her death"),
)

STAKES = (
    Stakes_macbeth_soul, Stakes_scotland,
    Stakes_lady_macbeth_sanity, Stakes_marriage,
)


# ============================================================================
# Story root
# ============================================================================

STORY = Story(
    id="S_macbeth",
    title="Macbeth",
    character_function_template_id="dramatica-8",
    argument_ids=tuple(a.id for a in ARGUMENTS),
    throughline_ids=tuple(t.id for t in THROUGHLINES),
    character_ids=tuple(c.id for c in CHARACTERS),
    scene_ids=tuple(s.id for s in SCENES),
    beat_ids=tuple(b.id for b in BEATS),
    stakes_ids=tuple(s.id for s in STAKES),
)
