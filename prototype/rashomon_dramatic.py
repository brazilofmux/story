"""
rashomon_dramatic.py — Rashomon encoded in the Dramatic dialect,
using the multi-Story machinery from multi-story-sketch-01.

First multi-Story encoding. Rashomon's structure is one frame
Story at the gate (the woodcutter, the priest, the commoner
taking shelter from the rainstorm, arguing about what to trust
in human nature) nesting four inner Stories: the four testimonies
of the killing in the grove.

**Scope note.** This encoding is pragmatic-first-pass, not
canonical-scholarly. The frame Story carries a reasonably full
Dramatic encoding (Throughlines, Characters, Scenes, Beats,
Stakes). The four testimony Stories are deliberately skeletal —
each carries one Throughline (the MC throughline for that
witness's self-account), a minimal Character set, and a couple
of Scenes/Beats. The sketch-01 commitment explicitly allows
this: *"Testimony fragments may have incomplete Template records;
that's fine — the verifier will report the gaps."* The point is
to exercise the multi-Story machinery at the dialect layer and
see what per-Story verification surfaces.

Encoding choices:

- **Five Stories.** S_frame (root), S_bandit_ver, S_wife_ver,
  S_samurai_ver, S_woodcutter_ver. The `StoryEncoding` wraps
  them with containment + parallel-to relations.

- **Shared characters.** The woodcutter, priest, and commoner
  appear in the frame. The bandit (Tajōmaru), the wife, the
  samurai, and the woodcutter-as-witness appear in the
  testimonies. A single Character record per entity; multiple
  Stories reference the same Character via their character_ids
  tuples. (Entity-aliasing across Stories is OQ3 in the sketch;
  here we take the simple pragmatic choice of shared Character
  records by id.)

- **No Lowerings yet.** Lowering authoring is a follow-up pass.
  The cross-boundary verifier will surface each Story's lack of
  Lowerings via existing NOTED / advisory handling — that's
  exactly the shape of feedback this first-pass encoding is
  built to surface.

- **Narrative positions.** The frame's narrative_positions range
  across 0-7 (at the gate). Each testimony's positions are
  independent, rooted at 0 for that testimony.

Encoding honors dramatic-sketch-01 M1-M10 per Story independently
and multi-story-sketch-01 MS1-MS6 at the encoding layer.
"""

from __future__ import annotations

from dramatic import (
    Argument,
    Beat,
    Character,
    Scene,
    SceneAdvancement,
    Stakes,
    StakesOwner,
    StakesOwnerKind,
    Story,
    StoryEncoding,
    StoryRelation,
    Throughline,
    ArgumentContribution,
    ResolutionDirection,
    ArgumentSide,
)


# ============================================================================
# The Argument (only one — the frame's)
# ============================================================================
#
# Testimonies in Rashomon don't carry their own Arguments in any
# clean Dramatica sense. They're fragments. The frame's Argument is
# the one the film is actually making.

A_human_nature = Argument(
    id="A_human_nature",
    premise=("human nature can be trusted — or at least kept trust-"
             "worthy — in the face of evidence of its unreliability; "
             "the woodcutter's adoption of the abandoned baby at the "
             "end of the frame is the dramatic enactment of the "
             "premise."),
    counter_premise=("human nature is irredeemably self-serving; the "
                     "four testimonies' mutual incompatibility is "
                     "prima facie evidence that every account, "
                     "including the witness's, is a self-image "
                     "managed against the truth."),
    resolution_direction=ResolutionDirection.AFFIRM,
    domain="manipulation",
)


# ============================================================================
# Characters
# ============================================================================
#
# Shared across Stories via shared Character records by id. See
# encoding choices.

# Frame participants
C_woodcutter = Character(
    id="C_woodcutter", name="Woodcutter",
    function_labels=("Protagonist",),
)
C_priest = Character(
    id="C_priest", name="Priest",
    function_labels=("Emotion",),
)
C_commoner = Character(
    id="C_commoner", name="Commoner",
    function_labels=("Skeptic",),
)
C_bandit = Character(
    id="C_bandit", name="Tajōmaru",
    function_labels=("Antagonist",),
)
C_wife = Character(
    id="C_wife", name="The wife",
    function_labels=(),
)
C_samurai = Character(
    id="C_samurai", name="The samurai",
    function_labels=(),
)


# ============================================================================
# Throughlines — Frame Story
# ============================================================================

T_frame_overall = Throughline(
    id="T_frame_overall",
    role_label="overall",
    owners=("the-situation",),  # THROUGHLINE_OWNER_SITUATION
    subject=("the interpretive crisis at the gate — whether human "
             "nature can be trusted after hearing four irreconcilable "
             "accounts of the same killing."),
    argument_contributions=(
        ArgumentContribution(argument_id="A_human_nature", side=ArgumentSide.AFFIRMS),
    ),
    counterpoint_throughline_ids=(),
)

T_frame_mc = Throughline(
    id="T_frame_mc",
    role_label="main character",
    owners=("C_woodcutter",),
    subject=("the woodcutter's struggle to be the kind of witness he "
             "was not in the grove, and to make good on what he "
             "saw."),
    argument_contributions=(
        ArgumentContribution(argument_id="A_human_nature", side=ArgumentSide.AFFIRMS),
    ),
    counterpoint_throughline_ids=("T_frame_ic",),
)

T_frame_ic = Throughline(
    id="T_frame_ic",
    role_label="impact character",
    owners=("C_commoner",),
    subject=("the commoner's counter-position — that the woodcutter's "
             "belated confession is self-interested like every other "
             "account, and that human nature's self-serving nature "
             "is simply the truth."),
    argument_contributions=(
        ArgumentContribution(argument_id="A_human_nature", side=ArgumentSide.OPPOSES),
    ),
    counterpoint_throughline_ids=("T_frame_mc",),
)

T_frame_rel = Throughline(
    id="T_frame_rel",
    role_label="relationship",
    owners=("C_woodcutter", "C_priest"),
    subject=("the priest's crisis of faith in human nature, and the "
             "woodcutter's eventual act restoring it."),
    argument_contributions=(
        ArgumentContribution(argument_id="A_human_nature", side=ArgumentSide.AFFIRMS),
    ),
    counterpoint_throughline_ids=(),
)


# ============================================================================
# Throughlines — each Testimony Story (skeletal: MC only)
# ============================================================================

T_bandit_mc = Throughline(
    id="T_bandit_mc",
    role_label="main character",
    owners=("C_bandit",),
    subject=("Tajōmaru's self-account: the seduction, the duel, the "
             "samurai's fall. A narrative of prowess and noble "
             "contest."),
    argument_contributions=(),
    counterpoint_throughline_ids=(),
)

T_wife_mc = Throughline(
    id="T_wife_mc",
    role_label="main character",
    owners=("C_wife",),
    subject=("The wife's self-account: violation, shame, and a half-"
             "conscious act after her husband's gaze of contempt. A "
             "narrative of dissociation and compelled action."),
    argument_contributions=(),
    counterpoint_throughline_ids=(),
)

T_samurai_mc = Throughline(
    id="T_samurai_mc",
    role_label="main character",
    owners=("C_samurai",),
    subject=("The husband's self-account via the medium: his wife "
             "begging the bandit to kill him; his suicide with her "
             "dagger. A narrative of betrayed honor and ritual "
             "self-erasure."),
    argument_contributions=(),
    counterpoint_throughline_ids=(),
)

T_woodcutter_mc = Throughline(
    id="T_woodcutter_mc",
    role_label="main character",
    owners=("C_woodcutter",),
    subject=("The woodcutter's belated confession: a messy, "
             "cowardly fight; the wife goading both men; the "
             "woodcutter stealing the dagger from the scene. A "
             "narrative of reluctantly-admitted complicity."),
    argument_contributions=(),
    counterpoint_throughline_ids=(),
)


# ============================================================================
# Scenes — Frame
# ============================================================================

S_frame_at_gate = Scene(
    id="S_frame_at_gate",
    title="Under the gate, in the rain",
    narrative_position=0,
    advances=(
        SceneAdvancement(throughline_id="T_frame_overall", beat_id="B_fr_1"),
    ),
    conflict_shape=("The three characters have taken shelter from a "
                    "torrential rainstorm at the gate. The woodcutter "
                    "and priest sit stunned; the commoner arrives and "
                    "presses them to explain their state."),
    result="the debate is set up; the testimonies will follow.",
)

S_frame_testimonies_reported = Scene(
    id="S_frame_testimonies_reported",
    title="Reporting the four accounts",
    narrative_position=1,
    advances=(
        SceneAdvancement(throughline_id="T_frame_overall", beat_id="B_fr_2"),
        SceneAdvancement(throughline_id="T_frame_rel", beat_id="B_fr_rel_1"),
    ),
    conflict_shape=("The woodcutter and priest recount, in sequence, "
                    "the testimonies given at the gate's court: "
                    "Tajōmaru's, the wife's, the samurai's (via the "
                    "medium). Each testimony becomes an inner Story "
                    "this Scene frames."),
    result=("the commoner's skepticism accretes across the sequence; "
            "the priest's faith is tested."),
)

S_frame_woodcutter_breaks = Scene(
    id="S_frame_woodcutter_breaks",
    title="The woodcutter's confession",
    narrative_position=2,
    advances=(
        SceneAdvancement(throughline_id="T_frame_mc", beat_id="B_fr_mc_1"),
        SceneAdvancement(throughline_id="T_frame_ic", beat_id="B_fr_ic_1"),
    ),
    conflict_shape=("Pressed by the commoner, the woodcutter gives "
                    "his own account — differing materially from the "
                    "first three. He admits he was there, admits to "
                    "stealing the dagger. The commoner frames this "
                    "as confirmation of human self-interest; the "
                    "woodcutter and priest try to hold a different "
                    "reading."),
    result=("the MC/IC clash lands; the counter-premise seems to "
            "win."),
)

S_frame_abandoned_baby = Scene(
    id="S_frame_abandoned_baby",
    title="The abandoned baby",
    narrative_position=3,
    advances=(
        SceneAdvancement(throughline_id="T_frame_overall", beat_id="B_fr_3"),
        SceneAdvancement(throughline_id="T_frame_mc", beat_id="B_fr_mc_2"),
        SceneAdvancement(throughline_id="T_frame_rel", beat_id="B_fr_rel_2"),
    ),
    conflict_shape=("A baby cries. The commoner strips the baby of "
                    "its clothing; the priest intervenes; the "
                    "woodcutter offers to take the baby home to his "
                    "existing children."),
    result=("the woodcutter's act resolves the frame; the priest's "
            "faith is restored; the commoner exits."),
)

S_frame_rain_stops = Scene(
    id="S_frame_rain_stops",
    title="The rain stops; the woodcutter leaves",
    narrative_position=4,
    advances=(
        SceneAdvancement(throughline_id="T_frame_overall", beat_id="B_fr_4"),
        SceneAdvancement(throughline_id="T_frame_rel", beat_id="B_fr_rel_3"),
    ),
    conflict_shape=("The rain stops. The woodcutter walks out holding "
                    "the baby. The priest watches him go. The frame "
                    "closes on restored-but-tentative human faith."),
    result=("the story's question — can human nature be trusted? — "
            "answered in the affirmative by the woodcutter's act."),
)


# ============================================================================
# Scenes — each Testimony Story (skeletal)
# ============================================================================

S_bandit_seduction = Scene(
    id="S_bandit_seduction", title="Tajōmaru: the seduction",
    narrative_position=0,
    advances=(
        SceneAdvancement(throughline_id="T_bandit_mc", beat_id="B_bandit_1"),
    ),
    conflict_shape=("Tajōmaru lures the samurai off-road with a story "
                    "about a buried sword, ties him up, and brings "
                    "the wife to the grove to seduce her — in his "
                    "telling, successfully and with her eventual "
                    "willingness."),
    result="she agrees to the duel; the samurai agrees to fight.",
)

S_bandit_duel = Scene(
    id="S_bandit_duel", title="Tajōmaru: the noble duel",
    narrative_position=1,
    advances=(
        SceneAdvancement(throughline_id="T_bandit_mc", beat_id="B_bandit_2"),
    ),
    conflict_shape=("The bandit and the samurai fight for twenty-"
                    "three strokes (a detail Tajōmaru emphasizes). "
                    "Tajōmaru wins on the twenty-third. The wife has "
                    "fled."),
    result="the samurai is dead; Tajōmaru's account ends.",
)

S_wife_violated = Scene(
    id="S_wife_violated", title="The wife: the violation",
    narrative_position=0,
    advances=(
        SceneAdvancement(throughline_id="T_wife_mc", beat_id="B_wife_1"),
    ),
    conflict_shape=("The bandit violates the wife. Afterward she "
                    "pleads with her tied husband; his response is "
                    "a look of contempt."),
    result=("she is dissociated; the husband's contempt becomes the "
            "pivot of her account."),
)

S_wife_killing = Scene(
    id="S_wife_killing", title="The wife: the half-conscious act",
    narrative_position=1,
    advances=(
        SceneAdvancement(throughline_id="T_wife_mc", beat_id="B_wife_2"),
    ),
    conflict_shape=("In the wife's account, she kills her husband in "
                    "a half-conscious act after his gaze of contempt, "
                    "then tries and fails to kill herself."),
    result="the husband is dead by her hand in this account.",
)

S_samurai_begging = Scene(
    id="S_samurai_begging", title="The samurai: the begging",
    narrative_position=0,
    advances=(
        SceneAdvancement(throughline_id="T_samurai_mc", beat_id="B_samurai_1"),
    ),
    conflict_shape=("Speaking through the medium, the samurai says "
                    "the wife went willingly with the bandit after "
                    "the seduction, and begged the bandit to kill "
                    "her husband. The bandit refused."),
    result="the bandit refuses; the wife flees.",
)

S_samurai_suicide = Scene(
    id="S_samurai_suicide", title="The samurai: ritual suicide",
    narrative_position=1,
    advances=(
        SceneAdvancement(throughline_id="T_samurai_mc", beat_id="B_samurai_2"),
    ),
    conflict_shape=("The samurai takes his own life with his wife's "
                    "dagger after being abandoned. In his account, "
                    "the death is ritual and willed."),
    result="the samurai is dead by his own hand in this account.",
)

S_woodcutter_fight = Scene(
    id="S_woodcutter_fight", title="Woodcutter: the messy fight",
    narrative_position=0,
    advances=(
        SceneAdvancement(throughline_id="T_woodcutter_mc", beat_id="B_woodcutter_1"),
    ),
    conflict_shape=("In the woodcutter's belated account, the bandit "
                    "and the samurai fight — but cowardly and messily, "
                    "nothing like Tajōmaru's twenty-three strokes. "
                    "The wife goads both men."),
    result="the samurai dies in a stumbling finish.",
)

S_woodcutter_theft = Scene(
    id="S_woodcutter_theft", title="Woodcutter: the theft",
    narrative_position=1,
    advances=(
        SceneAdvancement(throughline_id="T_woodcutter_mc", beat_id="B_woodcutter_2"),
    ),
    conflict_shape=("After the fight ends, the woodcutter returns to "
                    "the scene and takes the wife's pearl-inlaid "
                    "dagger. This is the detail that incriminates his "
                    "own testimony — he was there; he stole."),
    result=("the woodcutter's hands are not clean; his confession "
            "becomes the frame's pivot."),
)


# ============================================================================
# Beats — Frame
# ============================================================================

B_fr_1 = Beat(
    id="B_fr_1", throughline_id="T_frame_overall",
    beat_position=1, beat_type="inciting",
    description_of_change=("the interpretive crisis is introduced — "
                           "the woodcutter and priest state that "
                           "something has happened they cannot make "
                           "sense of."),
)

B_fr_2 = Beat(
    id="B_fr_2", throughline_id="T_frame_overall",
    beat_position=2, beat_type="rising",
    description_of_change=("testimonies accumulate; each is plausible "
                           "on its own terms; mutual incompatibility "
                           "builds."),
)

B_fr_3 = Beat(
    id="B_fr_3", throughline_id="T_frame_overall",
    beat_position=3, beat_type="climax",
    description_of_change=("the abandoned baby introduces a new "
                           "moral stake the characters must respond "
                           "to immediately; the frame's test lands."),
)

B_fr_4 = Beat(
    id="B_fr_4", throughline_id="T_frame_overall",
    beat_position=4, beat_type="denouement",
    description_of_change=("the rain stops; the woodcutter exits "
                           "holding the baby; the priest's faith is "
                           "restored; the frame closes."),
)

B_fr_mc_1 = Beat(
    id="B_fr_mc_1", throughline_id="T_frame_mc",
    beat_position=1, beat_type="midpoint",
    description_of_change=("the woodcutter is cornered into "
                           "confessing his own presence at the grove "
                           "— a confession he had withheld for the "
                           "whole frame."),
)

B_fr_mc_2 = Beat(
    id="B_fr_mc_2", throughline_id="T_frame_mc",
    beat_position=2, beat_type="climax",
    description_of_change=("the woodcutter's adoption of the baby — "
                           "the MC's act that makes good on what his "
                           "earlier silence failed to."),
)

B_fr_ic_1 = Beat(
    id="B_fr_ic_1", throughline_id="T_frame_ic",
    beat_position=1, beat_type="climax",
    description_of_change=("the commoner's cynicism articulates at "
                           "full force — everyone lies; the "
                           "woodcutter's confession proves it; human "
                           "nature is the self-serving thing it "
                           "always was."),
)

B_fr_rel_1 = Beat(
    id="B_fr_rel_1", throughline_id="T_frame_rel",
    beat_position=1, beat_type="rising",
    description_of_change=("the priest's faith is tested by each "
                           "testimony; the woodcutter watches the "
                           "test without yet intervening."),
)

B_fr_rel_2 = Beat(
    id="B_fr_rel_2", throughline_id="T_frame_rel",
    beat_position=2, beat_type="climax",
    description_of_change=("the priest sees the woodcutter's "
                           "adoption of the baby and, in that seeing, "
                           "his faith is restored."),
)

B_fr_rel_3 = Beat(
    id="B_fr_rel_3", throughline_id="T_frame_rel",
    beat_position=3, beat_type="denouement",
    description_of_change=("the priest acknowledges the restoration "
                           "with few words; the relationship closes."),
)


# ============================================================================
# Beats — Testimony Stories (skeletal, 2 per story)
# ============================================================================

B_bandit_1 = Beat(
    id="B_bandit_1", throughline_id="T_bandit_mc",
    beat_position=1, beat_type="inciting",
    description_of_change="Tajōmaru's account: the seduction lands.",
)
B_bandit_2 = Beat(
    id="B_bandit_2", throughline_id="T_bandit_mc",
    beat_position=2, beat_type="climax",
    description_of_change="Tajōmaru's account: the noble duel; Tajōmaru wins.",
)

B_wife_1 = Beat(
    id="B_wife_1", throughline_id="T_wife_mc",
    beat_position=1, beat_type="inciting",
    description_of_change="The wife's account: violation; contempt from husband.",
)
B_wife_2 = Beat(
    id="B_wife_2", throughline_id="T_wife_mc",
    beat_position=2, beat_type="climax",
    description_of_change="The wife's account: the half-conscious killing.",
)

B_samurai_1 = Beat(
    id="B_samurai_1", throughline_id="T_samurai_mc",
    beat_position=1, beat_type="inciting",
    description_of_change="The samurai's account: the wife begs the bandit to kill him.",
)
B_samurai_2 = Beat(
    id="B_samurai_2", throughline_id="T_samurai_mc",
    beat_position=2, beat_type="climax",
    description_of_change="The samurai's account: ritual suicide.",
)

B_woodcutter_1 = Beat(
    id="B_woodcutter_1", throughline_id="T_woodcutter_mc",
    beat_position=1, beat_type="inciting",
    description_of_change="Woodcutter's account: the cowardly fight.",
)
B_woodcutter_2 = Beat(
    id="B_woodcutter_2", throughline_id="T_woodcutter_mc",
    beat_position=2, beat_type="climax",
    description_of_change="Woodcutter's account: he takes the dagger.",
)


# ============================================================================
# Stakes (frame only)
# ============================================================================

STAKES_human_nature = Stakes(
    id="STAKES_human_nature",
    owner=StakesOwner(kind=StakesOwnerKind.STORY, id="S_frame"),
    at_risk=("the priest's faith in human nature — and, by extension, "
             "the frame's (and the audience's) willingness to believe "
             "redemption possible."),
    to_gain=("a restored, if tentative, account of human nature — "
             "one that can survive the evidence of self-serving "
             "testimony without collapsing."),
    external_manifestation=("the adoption of the abandoned baby; the "
                            "priest's words at the gate."),
)


# ============================================================================
# Stories
# ============================================================================

S_frame = Story(
    id="S_frame",
    title="Rashomon — the frame",
    character_function_template_id="dramatica-8",
    argument_ids=("A_human_nature",),
    throughline_ids=(
        "T_frame_overall", "T_frame_mc", "T_frame_ic", "T_frame_rel",
    ),
    character_ids=("C_woodcutter", "C_priest", "C_commoner"),
    scene_ids=(
        "S_frame_at_gate",
        "S_frame_testimonies_reported",
        "S_frame_woodcutter_breaks",
        "S_frame_abandoned_baby",
        "S_frame_rain_stops",
    ),
    beat_ids=(
        "B_fr_1", "B_fr_2", "B_fr_3", "B_fr_4",
        "B_fr_mc_1", "B_fr_mc_2",
        "B_fr_ic_1",
        "B_fr_rel_1", "B_fr_rel_2", "B_fr_rel_3",
    ),
    stakes_ids=("STAKES_human_nature",),
)

S_bandit_ver = Story(
    id="S_bandit_ver",
    title="Rashomon — Tajōmaru's testimony",
    character_function_template_id=None,  # skeletal, no Template
    argument_ids=(),
    throughline_ids=("T_bandit_mc",),
    character_ids=("C_bandit", "C_wife", "C_samurai"),
    scene_ids=("S_bandit_seduction", "S_bandit_duel"),
    beat_ids=("B_bandit_1", "B_bandit_2"),
)

S_wife_ver = Story(
    id="S_wife_ver",
    title="Rashomon — the wife's testimony",
    character_function_template_id=None,
    argument_ids=(),
    throughline_ids=("T_wife_mc",),
    character_ids=("C_wife", "C_bandit", "C_samurai"),
    scene_ids=("S_wife_violated", "S_wife_killing"),
    beat_ids=("B_wife_1", "B_wife_2"),
)

S_samurai_ver = Story(
    id="S_samurai_ver",
    title="Rashomon — the samurai's testimony (via medium)",
    character_function_template_id=None,
    argument_ids=(),
    throughline_ids=("T_samurai_mc",),
    character_ids=("C_samurai", "C_bandit", "C_wife"),
    scene_ids=("S_samurai_begging", "S_samurai_suicide"),
    beat_ids=("B_samurai_1", "B_samurai_2"),
)

S_woodcutter_ver = Story(
    id="S_woodcutter_ver",
    title="Rashomon — the woodcutter's belated testimony",
    character_function_template_id=None,
    argument_ids=(),
    throughline_ids=("T_woodcutter_mc",),
    character_ids=("C_woodcutter", "C_bandit", "C_wife", "C_samurai"),
    scene_ids=("S_woodcutter_fight", "S_woodcutter_theft"),
    beat_ids=("B_woodcutter_1", "B_woodcutter_2"),
)


# ============================================================================
# StoryEncoding — the multi-Story wrapper
# ============================================================================

RASHOMON_ENCODING = StoryEncoding(
    id="rashomon_encoding",
    title="Rashomon",
    entry_story_id="S_frame",
    stories=(
        S_frame,
        S_bandit_ver,
        S_wife_ver,
        S_samurai_ver,
        S_woodcutter_ver,
    ),
    relations=(
        # Frame contains each inner testimony.
        StoryRelation(kind="contains", a_story_id="S_frame",
                      b_story_id="S_bandit_ver",
                      notes="bandit's testimony reported in frame"),
        StoryRelation(kind="contains", a_story_id="S_frame",
                      b_story_id="S_wife_ver",
                      notes="wife's testimony reported in frame"),
        StoryRelation(kind="contains", a_story_id="S_frame",
                      b_story_id="S_samurai_ver",
                      notes="samurai's testimony via medium reported in frame"),
        StoryRelation(kind="contains", a_story_id="S_frame",
                      b_story_id="S_woodcutter_ver",
                      notes="woodcutter's belated confession in frame"),
        # Four inner testimonies are pairwise parallel-to (six pairs).
        StoryRelation(kind="parallel-to", a_story_id="S_bandit_ver",
                      b_story_id="S_wife_ver"),
        StoryRelation(kind="parallel-to", a_story_id="S_bandit_ver",
                      b_story_id="S_samurai_ver"),
        StoryRelation(kind="parallel-to", a_story_id="S_bandit_ver",
                      b_story_id="S_woodcutter_ver"),
        StoryRelation(kind="parallel-to", a_story_id="S_wife_ver",
                      b_story_id="S_samurai_ver"),
        StoryRelation(kind="parallel-to", a_story_id="S_wife_ver",
                      b_story_id="S_woodcutter_ver"),
        StoryRelation(kind="parallel-to", a_story_id="S_samurai_ver",
                      b_story_id="S_woodcutter_ver"),
    ),
)


# ============================================================================
# Flat exports (for consumers that want all records in one place)
# ============================================================================

ARGUMENTS = (A_human_nature,)

CHARACTERS = (
    C_woodcutter, C_priest, C_commoner,
    C_bandit, C_wife, C_samurai,
)

THROUGHLINES = (
    T_frame_overall, T_frame_mc, T_frame_ic, T_frame_rel,
    T_bandit_mc, T_wife_mc, T_samurai_mc, T_woodcutter_mc,
)

SCENES = (
    S_frame_at_gate, S_frame_testimonies_reported,
    S_frame_woodcutter_breaks, S_frame_abandoned_baby,
    S_frame_rain_stops,
    S_bandit_seduction, S_bandit_duel,
    S_wife_violated, S_wife_killing,
    S_samurai_begging, S_samurai_suicide,
    S_woodcutter_fight, S_woodcutter_theft,
)

BEATS = (
    B_fr_1, B_fr_2, B_fr_3, B_fr_4,
    B_fr_mc_1, B_fr_mc_2, B_fr_ic_1,
    B_fr_rel_1, B_fr_rel_2, B_fr_rel_3,
    B_bandit_1, B_bandit_2,
    B_wife_1, B_wife_2,
    B_samurai_1, B_samurai_2,
    B_woodcutter_1, B_woodcutter_2,
)

STAKES = (STAKES_human_nature,)

STORIES = RASHOMON_ENCODING.stories
