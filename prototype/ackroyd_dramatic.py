"""
ackroyd_dramatic.py — *The Murder of Roger Ackroyd* encoded in the
Dramatic dialect.

Third encoding at the Dramatic dialect level (parallel to
oedipus_dramatic.py and macbeth_dramatic.py). Records the novel's
argumentative structure: one Argument, four Throughlines under the
dramatica-8 Template, twelve Characters, twelve Scenes, four Stakes
records, twenty-three Beats.

Pure dialect content. No substrate references; no Lowering records.
This file pressures the Dramatic dialect on Ackroyd's structurally
distinctive feature per ackroyd-sketch-01's thesis: **Sheppard as
Main Character AND Antagonist**, and symmetrically **Poirot as
Protagonist AND Impact Character**. Dramatica theory admits
double-function Characters (Macbeth encodes Protagonist + Emotion on
Macbeth himself); this is the first encoding in which BOTH the MC
and IC carry a second function, and in which the MC aligns with
the Antagonist rather than the Protagonist.

Notable features the encoding exercises:

- **MC-Antagonist alignment.** Sheppard is the novel's voice (the
  reader follows him) and the force opposing the story goal
  (solving the murder, which is by solving *him*). This flips the
  standard "MC is the reader's sympathetic lead" pattern. In
  Dramatic dialect terms: the same Character (C_sheppard) owns the
  main-character Throughline AND holds the Antagonist function slot.
  Throughline role_labels ("main-character") are distinct from
  Character function_labels ("Antagonist"); the alignment is that
  one Character carries both.

- **IC-Protagonist alignment.** Poirot owns the impact-character
  Throughline AND holds the Protagonist function slot. Detective
  fiction tradition pairs "detective = Protagonist, reader follows
  narrator-assistant"; Christie inverts by making the narrator the
  Antagonist.

- **No identity collapse.** Unlike Oedipus, Ackroyd's anagnorisis
  is not about who-is-who. Sheppard is Sheppard throughout;
  Poirot's discovery is about what-was-done, not what-identity-
  equals-what. The encoding's Characters and their function_labels
  hold stable across the novel.

- **A performed Argument.** A_truth_recovers claims "the truth can
  be reasoned out of concealment"; Sheppard's counter-premise is
  that "a patient performance of innocence defeats investigation."
  The novel's trajectory affirms the premise: Poirot recovers the
  truth despite the narrator's best effort to withhold it. The
  Argument's resolution_direction is AFFIRM.

- **One Throughline per dramatica-8 slot; all four have Stakes.**
  Four Throughlines (overall-story, main-character, impact-
  character, relationship); no gaps. Four Stakes, one per
  Throughline.

- **Scenes include the withheld murder.** The Dramatic dialect
  cares about the play's argumentative structure, not about
  disclosure timing — so S_ackroyd_killed is a Scene at its
  fabula position, even though the substrate-layer sjuzhet
  defers its reader-facing disclosure to the late confession
  chapter. The dialect sees the drama; the discourse-level
  withholding is a substrate + sjuzhet concern that
  ackroyd_lowerings.py will address.

Expected verifier output (the encoding's contract):

- 0 slot_unfilled / slot_overfilled (all 8 dramatica-8 slots
  filled; Protagonist, Antagonist, Reason, Emotion, Skeptic,
  Sidekick, Guardian, Contagonist).
- 0 throughline_no_stakes (all 4 Throughlines have Stakes).
- 0 id_unresolved, no orphans, no duplicate positions.
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

A_truth_recovers = Argument(
    id="A_truth_recovers",
    premise=("the truth about a deed committed in concealment can be "
             "recovered by patient reasoning from what the concealer "
             "cannot hide"),
    counter_premise=("a sufficiently patient performance of innocence "
                     "defeats investigation; the narrator controls "
                     "what can be known. Sheppard voices this "
                     "position by his practice — his manuscript is "
                     "the counter-premise's most confident form. "
                     "The novel's trajectory systematically refutes "
                     "it"),
    resolution_direction=ResolutionDirection.AFFIRM,
    domain="moral-epistemic",
)

ARGUMENTS = (A_truth_recovers,)


# ============================================================================
# Throughlines
# ============================================================================

T_overall_case = Throughline(
    id="T_overall_case",
    role_label="overall-story",
    owners=(THROUGHLINE_OWNER_SITUATION,),
    subject=("a country-house murder; moral and legal order disturbed; "
             "an investigation that eventually restores it. Ralph's "
             "apparent guilt hangs over the village until Poirot's "
             "reveal; the innocent accused is exonerated only at the "
             "climax"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_truth_recovers",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_moral_order",
)

T_mc_sheppard = Throughline(
    id="T_mc_sheppard",
    role_label="main-character",
    owners=("C_sheppard",),
    subject=("the killer-as-narrator; a doctor who murders his "
             "friend-patient, then positions himself as the "
             "investigation's assistant and writes the manuscript the "
             "reader has in hand. His arc is the slow failure of "
             "performed innocence under Poirot's patient attention"),
    counterpoint_throughline_ids=("T_ic_poirot",),
    argument_contributions=(
        # Sheppard's existence IS the problem the Argument is arguing
        # about — his practiced concealment is what the premise
        # claims can be penetrated. His trajectory is the
        # Argument's test material.
        ArgumentContribution(
            argument_id="A_truth_recovers",
            side=ArgumentSide.COMPLICATES,
        ),
    ),
    stakes_id="Stakes_sheppard_life",
)

T_ic_poirot = Throughline(
    id="T_ic_poirot",
    role_label="impact-character",
    owners=("C_poirot",),
    subject=("the retired detective who takes the case despite his "
             "advertised retirement among the vegetable marrows; "
             "applies reason to what the narrator has tried to hide; "
             "becomes the force that moves the MC toward confession "
             "and its consequence"),
    counterpoint_throughline_ids=("T_mc_sheppard",),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_truth_recovers",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_poirot_method",
)

T_rel_sheppard_poirot = Throughline(
    id="T_rel_sheppard_poirot",
    role_label="relationship",
    owners=(THROUGHLINE_OWNER_RELATIONSHIP,),
    subject=("a partnership of apparent collaboration — detective and "
             "narrator-assistant — that contains its own refutation. "
             "Each interview Sheppard moderates is one more piece of "
             "data Poirot will use against him. The relationship's "
             "true shape is adversarial throughout, visible only to "
             "Sheppard until the reveal"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_truth_recovers",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_collaboration",
)

THROUGHLINES = (
    T_overall_case, T_mc_sheppard, T_ic_poirot, T_rel_sheppard_poirot,
)


# ============================================================================
# Characters
# ============================================================================
#
# dramatica-8 slot assignment for this encoding:
#
#   Protagonist        → C_poirot        (double-function MC-IC)
#   Antagonist         → C_sheppard      (double-function MC)
#   Main Character     → C_sheppard
#   Impact Character   → C_poirot
#   Reason             → C_raymond       (Ackroyd's secretary — the
#                                         methodical witness whose
#                                         overheard phrase is the key)
#   Emotion            → C_flora         (her love for Ralph is the
#                                         emotional engine forcing
#                                         Poirot's engagement)
#   Skeptic            → C_raglan        (police Inspector; doubts
#                                         both Ralph's flight and
#                                         Poirot's theory)
#   Sidekick           → C_blunt         (Major Blunt — loyal to Flora,
#                                         supports Poirot's work once
#                                         engaged)
#   Guardian           → C_caroline      (the village oracle; her
#                                         intuition — "such a nice
#                                         man, the doctor" — is the
#                                         Guardian's ironic form here,
#                                         warning-of-consequences by
#                                         sustained attention to the
#                                         village pattern)
#   Contagonist        → C_ralph_paton   (his flight diverts the
#                                         investigation; though he is
#                                         passive/innocent, his
#                                         disappearance IS the
#                                         misdirection)
#
# MC + Antagonist on C_sheppard and Protagonist + IC on C_poirot are
# the encoding's structural thesis. Both are admitted by Dramatica;
# the verifier's slot-coverage check should report all 8 dramatica-8
# slots filled exactly once.

C_poirot = Character(
    id="C_poirot", name="Hercule Poirot",
    function_labels=("Protagonist",),
    # The Impact Character role is carried by T_ic_poirot's owner
    # edge (owners=("C_poirot",)); Dramatica role_labels live on
    # Throughlines, not Character function_labels.
)

C_sheppard = Character(
    id="C_sheppard", name="Dr. James Sheppard",
    function_labels=("Antagonist",),
    # The Main Character role is carried by T_mc_sheppard's owner
    # edge (owners=("C_sheppard",)); same convention as C_poirot.
    # The encoding's structural thesis is that ONE character owns
    # both the main-character Throughline and the Antagonist function
    # slot — Dramatica admits the alignment; this Character carries it.
)

C_raymond = Character(
    id="C_raymond", name="Geoffrey Raymond",
    function_labels=("Reason",),
)

C_flora = Character(
    id="C_flora", name="Flora Ackroyd",
    function_labels=("Emotion",),
)

C_raglan = Character(
    id="C_raglan", name="Inspector Raglan",
    function_labels=("Skeptic",),
)

C_blunt = Character(
    id="C_blunt", name="Major Blunt",
    function_labels=("Sidekick",),
)

C_caroline = Character(
    id="C_caroline", name="Caroline Sheppard",
    function_labels=("Guardian",),
)

C_ralph_paton = Character(
    id="C_ralph_paton", name="Ralph Paton",
    function_labels=("Contagonist",),
)

# Characters present in the substrate but carrying no Dramatica
# function — victims, supporting figures, and the blackmail-victim
# whose death is pre-play backstory.

C_ackroyd = Character(
    id="C_ackroyd", name="Roger Ackroyd",
    function_labels=(),
)

C_mrs_ferrars = Character(
    id="C_mrs_ferrars", name="Mrs. Ferrars",
    function_labels=(),
)

C_ursula_bourne = Character(
    id="C_ursula_bourne", name="Ursula Bourne",
    function_labels=(),
)

C_parker = Character(
    id="C_parker", name="Parker",
    function_labels=(),
)

CHARACTERS = (
    C_poirot, C_sheppard, C_raymond, C_flora, C_raglan,
    C_blunt, C_caroline, C_ralph_paton,
    C_ackroyd, C_mrs_ferrars, C_ursula_bourne, C_parker,
)


# ============================================================================
# Beats — per Throughline, ordered by beat_position
# ============================================================================

BEATS = (

    # T_overall_case — the novel's central-case arc
    Beat(id="B_op_1", throughline_id="T_overall_case",
         beat_position=1, beat_type="inciting",
         description_of_change=("Mrs. Ferrars dies (suicide); her "
                                "letter to Ackroyd names her "
                                "blackmailer; the pre-play machinery "
                                "of concealment begins to fail")),
    Beat(id="B_op_2", throughline_id="T_overall_case",
         beat_position=2, beat_type="rising",
         description_of_change=("Ackroyd is murdered in his study; "
                                "the moral-legal breach is complete; "
                                "the investigation becomes necessary")),
    Beat(id="B_op_3", throughline_id="T_overall_case",
         beat_position=3, beat_type="rising",
         description_of_change=("Ralph is missing; public suspicion "
                                "converges on him; the wrong suspect "
                                "pool forms and the investigation has "
                                "its initial (mis-)direction")),
    Beat(id="B_op_4", throughline_id="T_overall_case",
         beat_position=4, beat_type="midpoint",
         description_of_change=("Ursula confesses her marriage to "
                                "Ralph; suspects are cleared one by "
                                "one as their private secrets are "
                                "exposed; the investigation's "
                                "rational pressure narrows the pool")),
    Beat(id="B_op_5", throughline_id="T_overall_case",
         beat_position=5, beat_type="climax",
         description_of_change=("Poirot reveals the killer in the "
                                "drawing room; Sheppard is named; the "
                                "case closes")),
    Beat(id="B_op_6", throughline_id="T_overall_case",
         beat_position=6, beat_type="denouement",
         description_of_change=("Sheppard's suicide — the private "
                                "ultimatum accepted; moral order "
                                "restored at the cost of one final "
                                "death; Ralph's name cleared")),

    # T_mc_sheppard — the MC's arc (killer-as-narrator)
    Beat(id="B_mc_1", throughline_id="T_mc_sheppard",
         beat_position=1, beat_type="inciting",
         description_of_change=("Mrs. Ferrars' suicide — driven by his "
                                "blackmail — is the inciting event "
                                "for his own arc, not just the case's; "
                                "he carries the knowledge that her "
                                "letter to Ackroyd may name him")),
    Beat(id="B_mc_2", throughline_id="T_mc_sheppard",
         beat_position=2, beat_type="rising",
         description_of_change=("at the Fernly dinner he learns "
                                "Ackroyd is about to read that "
                                "letter; he makes the moral "
                                "decision to kill his friend-patient "
                                "rather than be exposed")),
    Beat(id="B_mc_3", throughline_id="T_mc_sheppard",
         beat_position=3, beat_type="rising",
         description_of_change=("kills Ackroyd; stages the dictaphone "
                                "alibi; the first murder committed by "
                                "a trusted doctor on his patient — "
                                "the betrayer_of_trust derivation "
                                "fires")),
    Beat(id="B_mc_4", throughline_id="T_mc_sheppard",
         beat_position=4, beat_type="rising",
         description_of_change=("performs the discovery next morning; "
                                "plays the concerned doctor; the "
                                "narration of 'I was shocked to find' "
                                "is the first sustained piece of "
                                "performed innocence")),
    Beat(id="B_mc_5", throughline_id="T_mc_sheppard",
         beat_position=5, beat_type="midpoint",
         description_of_change=("attaches himself to Poirot's "
                                "investigation as assistant / Watson; "
                                "the narrator is now also managing "
                                "what the detective sees. The "
                                "counter-premise is operating at "
                                "peak confidence")),
    Beat(id="B_mc_6", throughline_id="T_mc_sheppard",
         beat_position=6, beat_type="climax",
         description_of_change=("named by Poirot in the drawing room; "
                                "the performance fails; the "
                                "counter-premise's refutation is "
                                "public")),
    Beat(id="B_mc_7", throughline_id="T_mc_sheppard",
         beat_position=7, beat_type="denouement",
         description_of_change=("accepts the ultimatum; writes the "
                                "confession's final pages; the "
                                "manuscript (which the reader has "
                                "been reading all along) becomes "
                                "honest in its last chapter; the "
                                "suicide follows")),

    # T_ic_poirot — the IC's arc (the detective's work)
    Beat(id="B_ic_1", throughline_id="T_ic_poirot",
         beat_position=1, beat_type="inciting",
         description_of_change=("Flora commissions him; he accepts "
                                "despite retirement; the 'vegetable "
                                "marrows' bit is revealed as cover")),
    Beat(id="B_ic_2", throughline_id="T_ic_poirot",
         beat_position=2, beat_type="rising",
         description_of_change=("interviews the household; collects "
                                "everyone's private secrets; notes "
                                "the dictaphone and the phone call's "
                                "origin as problems to solve")),
    Beat(id="B_ic_3", throughline_id="T_ic_poirot",
         beat_position=3, beat_type="midpoint",
         description_of_change=("the breakthrough — the dictaphone's "
                                "mechanism, the phone-call trace, "
                                "Raymond's overheard phrase all "
                                "align; the set of possible killers "
                                "narrows to the one who had motive, "
                                "opportunity, and the means to stage "
                                "the alibi")),
    Beat(id="B_ic_4", throughline_id="T_ic_poirot",
         beat_position=4, beat_type="climax",
         description_of_change=("the reveal scene; method applied to "
                                "its hardest case yields the name")),
    Beat(id="B_ic_5", throughline_id="T_ic_poirot",
         beat_position=5, beat_type="denouement",
         description_of_change=("the private conversation — gives "
                                "Sheppard the choice to end it his "
                                "way; the detective's quiet mercy as "
                                "resolution")),

    # T_rel_sheppard_poirot — the relationship arc
    Beat(id="B_rel_1", throughline_id="T_rel_sheppard_poirot",
         beat_position=1, beat_type="inciting",
         description_of_change=("Poirot takes Sheppard into his "
                                "confidence as the local medical man; "
                                "the detective-assistant pairing "
                                "forms on apparent good faith")),
    Beat(id="B_rel_2", throughline_id="T_rel_sheppard_poirot",
         beat_position=2, beat_type="rising",
         description_of_change=("Sheppard assists through the "
                                "investigation; the collaboration "
                                "looks productive; Sheppard controls "
                                "what he can of Poirot's field of "
                                "view")),
    Beat(id="B_rel_3", throughline_id="T_rel_sheppard_poirot",
         beat_position=3, beat_type="midpoint",
         description_of_change=("Poirot's confidence increases as "
                                "data accrues; Sheppard's unease "
                                "rises as the dictaphone analysis "
                                "begins — neither acknowledges the "
                                "shift")),
    Beat(id="B_rel_4", throughline_id="T_rel_sheppard_poirot",
         beat_position=4, beat_type="climax",
         description_of_change=("Poirot reveals; the collaboration "
                                "inverts publicly — the assistant is "
                                "the subject; what looked like "
                                "partnership was always adversarial")),
    Beat(id="B_rel_5", throughline_id="T_rel_sheppard_poirot",
         beat_position=5, beat_type="denouement",
         description_of_change=("the private conversation between "
                                "them; the pairing's actual history "
                                "named between them; closes with "
                                "Sheppard's implied suicide")),
)


# ============================================================================
# Scenes
# ============================================================================

S_ferrars_death = Scene(
    id="S_ferrars_death", title="Mrs. Ferrars' death",
    narrative_position=1,
    advances=(
        SceneAdvancement(throughline_id="T_overall_case", beat_id="B_op_1"),
        SceneAdvancement(throughline_id="T_mc_sheppard",  beat_id="B_mc_1"),
    ),
    conflict_shape=("a widow's suicide opens the novel; village "
                    "gossip, a letter en route to the victim's closest "
                    "friend, and one village doctor who knows far more "
                    "than he says"),
    result=("Mrs. Ferrars dead; Ackroyd expecting her letter; "
            "Sheppard carrying the knowledge his blackmail drove her "
            "to this; the village's surface unruffled"),
)

S_ackroyd_dinner = Scene(
    id="S_ackroyd_dinner", title="The Fernly Park dinner",
    narrative_position=2,
    advances=(
        SceneAdvancement(throughline_id="T_mc_sheppard", beat_id="B_mc_2"),
    ),
    conflict_shape=("the doctor dines with the intended victim; the "
                    "letter is on the desk; Sheppard learns he is "
                    "minutes from being named"),
    result=("the moral decision is made — Sheppard will kill Ackroyd "
            "rather than be exposed; Ackroyd's fate is sealed "
            "before he reads the letter's end"),
)

S_ackroyd_killed = Scene(
    id="S_ackroyd_killed", title="The killing of Ackroyd",
    narrative_position=3,
    advances=(
        SceneAdvancement(throughline_id="T_mc_sheppard",  beat_id="B_mc_3"),
        SceneAdvancement(throughline_id="T_overall_case", beat_id="B_op_2"),
    ),
    conflict_shape=("a trusted doctor kills his patient and host; the "
                    "room is locked from inside; the dictaphone is "
                    "set; the alibi is staged"),
    result=("Ackroyd dead; betrayer_of_trust derivable; the "
            "investigation's inciting fact in place; Sheppard's "
            "narration from this point forward is managed silence"),
)

S_body_discovery = Scene(
    id="S_body_discovery", title="The body discovered",
    narrative_position=4,
    advances=(
        SceneAdvancement(throughline_id="T_overall_case", beat_id="B_op_3"),
        SceneAdvancement(throughline_id="T_mc_sheppard",  beat_id="B_mc_4"),
    ),
    conflict_shape=("morning in the house; Parker's increasing "
                    "concern; the door broken; Sheppard in "
                    "attendance, performing the shocked doctor's "
                    "role"),
    result=("the murder is public; the household begins its turn to "
            "suspicion; Sheppard's first sustained performance of "
            "innocence completes successfully"),
)

S_ralph_flight = Scene(
    id="S_ralph_flight", title="Ralph missing; suspicion converges",
    narrative_position=5,
    advances=(
        SceneAdvancement(throughline_id="T_overall_case", beat_id="B_op_3"),
    ),
    conflict_shape=("the stepson cannot be found; his being at the "
                    "house that night, his financial motive, his "
                    "temperament — the village converges on Ralph as "
                    "killer without needing evidence"),
    result=("Ralph accused in public opinion; the investigation's "
            "initial misdirection established; Flora's conviction of "
            "his innocence becomes the Emotion function's engine"),
)

S_flora_hires_poirot = Scene(
    id="S_flora_hires_poirot", title="Flora commissions Poirot",
    narrative_position=6,
    advances=(
        SceneAdvancement(throughline_id="T_ic_poirot",           beat_id="B_ic_1"),
        SceneAdvancement(throughline_id="T_rel_sheppard_poirot", beat_id="B_rel_1"),
    ),
    conflict_shape=("the retired detective with vegetable marrows; "
                    "the young woman in love with the prime suspect; "
                    "an engagement entered despite Poirot's stated "
                    "retirement"),
    result=("Poirot is on the case; Sheppard attached as local "
            "medical assistant; the adversarial relationship is "
            "formed on apparent good faith"),
)

S_investigation = Scene(
    id="S_investigation", title="The investigation",
    narrative_position=7,
    advances=(
        SceneAdvancement(throughline_id="T_ic_poirot",           beat_id="B_ic_2"),
        SceneAdvancement(throughline_id="T_rel_sheppard_poirot", beat_id="B_rel_2"),
        SceneAdvancement(throughline_id="T_mc_sheppard",         beat_id="B_mc_5"),
    ),
    conflict_shape=("Poirot's systematic interviews with the "
                    "household — Flora, Raymond, Major Blunt, Parker, "
                    "Ursula, Raglan. Each private secret exposed, "
                    "each alibi tested. Sheppard present at every "
                    "session, managing what he can"),
    result=("the suspect pool narrows as secrets clear their "
            "holders (Flora's theft, Parker's history, Raymond's "
            "overheard phrase); the case's shape tightens around "
            "the one person who has been in every scene"),
)

S_ursula_confession = Scene(
    id="S_ursula_confession", title="Ursula's confession",
    narrative_position=8,
    advances=(
        SceneAdvancement(throughline_id="T_overall_case", beat_id="B_op_4"),
    ),
    conflict_shape=("the parlormaid finally admits her secret "
                    "marriage to Ralph; her motive is not guilt but "
                    "concealment of class-crossing; Poirot uses the "
                    "confession to clear both her and Ralph from the "
                    "suspect pool"),
    result=("Ralph's absence is re-read (she knows where he is, and "
            "why); the last red-herring clears; the investigation's "
            "arrow points inward to the one remaining presence"),
)

S_dictaphone_breakthrough = Scene(
    id="S_dictaphone_breakthrough",
    title="The dictaphone and the phone call",
    narrative_position=9,
    advances=(
        SceneAdvancement(throughline_id="T_ic_poirot",           beat_id="B_ic_3"),
        SceneAdvancement(throughline_id="T_rel_sheppard_poirot", beat_id="B_rel_3"),
    ),
    conflict_shape=("Poirot works through the alibi's physical "
                    "mechanism: the dictaphone that 'was' Ackroyd's "
                    "voice at 9:30pm, the phone call whose origin "
                    "does not match its supposed source. Sheppard "
                    "watches Poirot advance and cannot intervene"),
    result=("the solution's shape is visible to Poirot; Sheppard "
            "knows he has been solved; neither party speaks it yet"),
)

S_poirot_reveal = Scene(
    id="S_poirot_reveal", title="The reveal in the drawing room",
    narrative_position=10,
    advances=(
        SceneAdvancement(throughline_id="T_overall_case",        beat_id="B_op_5"),
        SceneAdvancement(throughline_id="T_mc_sheppard",         beat_id="B_mc_6"),
        SceneAdvancement(throughline_id="T_ic_poirot",           beat_id="B_ic_4"),
        SceneAdvancement(throughline_id="T_rel_sheppard_poirot", beat_id="B_rel_4"),
    ),
    conflict_shape=("the drawing-room scene; Poirot walks the cast "
                    "through the reconstruction; each piece placed "
                    "until only the narrator's chair is left empty; "
                    "Sheppard is named"),
    result=("the case is solved publicly; the cast's KNOWN sets all "
            "update with killed(sheppard, ackroyd); Caroline hears "
            "her brother named; the collaboration's true shape is "
            "now visible to every party"),
)

S_private_ultimatum = Scene(
    id="S_private_ultimatum",
    title="The private conversation",
    narrative_position=11,
    advances=(
        SceneAdvancement(throughline_id="T_ic_poirot",           beat_id="B_ic_5"),
        SceneAdvancement(throughline_id="T_rel_sheppard_poirot", beat_id="B_rel_5"),
        SceneAdvancement(throughline_id="T_mc_sheppard",         beat_id="B_mc_7"),
    ),
    conflict_shape=("detective and killer, alone; a night's grace "
                    "offered; the choice between public arraignment "
                    "and a private ending"),
    result=("Sheppard accepts the terms; the manuscript's honest "
            "ending will be written; Poirot's mercy is the "
            "investigator's final act"),
)

S_sheppard_death = Scene(
    id="S_sheppard_death", title="Sheppard's end",
    narrative_position=12,
    advances=(
        SceneAdvancement(throughline_id="T_overall_case", beat_id="B_op_6"),
    ),
    conflict_shape=("the manuscript's last pages; overdose as the "
                    "chosen method; Ralph cleared publicly; Caroline "
                    "left with the knowledge"),
    result=("Sheppard dead; the case closed on all sides; the novel "
            "the reader has been reading reaches its honest final "
            "paragraph"),
)

SCENES = (
    S_ferrars_death, S_ackroyd_dinner, S_ackroyd_killed,
    S_body_discovery, S_ralph_flight, S_flora_hires_poirot,
    S_investigation, S_ursula_confession, S_dictaphone_breakthrough,
    S_poirot_reveal, S_private_ultimatum, S_sheppard_death,
)


# ============================================================================
# Stakes
# ============================================================================

Stakes_moral_order = Stakes(
    id="Stakes_moral_order",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T_overall_case"),
    at_risk=("the village's moral and legal order; the safety of a "
             "community where a trusted doctor can be a killer; "
             "Ralph's life and reputation while accused"),
    to_gain=("restoration — the truth revealed, the innocent "
             "cleared, the killer accountable; the rationalist "
             "tradition's claim (truth is recoverable through "
             "patient reasoning) demonstrated on a hard case"),
    external_manifestation=("Ralph's disappearance and eventual "
                            "clearing; the household's secrets "
                            "exposed one by one during interviews; "
                            "Poirot's drawing-room reconstruction; "
                            "Sheppard's suicide as the moral "
                            "terminus"),
)

Stakes_sheppard_life = Stakes(
    id="Stakes_sheppard_life",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T_mc_sheppard"),
    at_risk=("Sheppard's life; his liberty; his reputation as village "
             "doctor; the constructed self his narration projects — "
             "his ability to go on being 'the doctor' after what he "
             "has done"),
    to_gain=("continued liberty; the performance's success; the "
             "published memoir he has told the reader he is writing "
             "('an account of Poirot's one great failure') — which "
             "is the counter-premise's most confident form"),
    external_manifestation=("the blackmail of Mrs. Ferrars; the "
                            "dictaphone setup; the dinner invitation "
                            "he accepts; the manuscript he composes "
                            "chapter-by-chapter; his eventual "
                            "overdose"),
)

Stakes_poirot_method = Stakes(
    id="Stakes_poirot_method",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T_ic_poirot"),
    at_risk=("the viability of Poirot's rational method against a "
             "performed opponent; his retirement's integrity "
             "(whether he can stay retired); the method's "
             "applicability to cases where the assistant is also "
             "the subject"),
    to_gain=("confirmation — the method works; the truth is "
             "recoverable even when the narrator is the killer; the "
             "detective tradition's central premise stands under its "
             "hardest pressure"),
    external_manifestation=("the interviews; the dictaphone "
                            "analysis; the phone-call trace; the "
                            "reveal's reconstruction; the quiet "
                            "ultimatum at the end"),
)

Stakes_collaboration = Stakes(
    id="Stakes_collaboration",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T_rel_sheppard_poirot"),
    at_risk=("the collaboration's apparent shape — the Watson-Poirot "
             "pairing visible to the village; each party's trust in "
             "what the other actually is"),
    to_gain=("the discovery of what the relationship has been all "
             "along — adversarial from the first handshake, visible "
             "as such only to Sheppard until the reveal; for Poirot, "
             "the recognition comes as data before it comes as "
             "acknowledgment"),
    external_manifestation=("the household interviews Sheppard "
                            "attends as assistant; Poirot's steady "
                            "questioning; the drawing-room inversion; "
                            "the private conversation that names the "
                            "collaboration's true history between "
                            "them"),
)

STAKES = (
    Stakes_moral_order, Stakes_sheppard_life,
    Stakes_poirot_method, Stakes_collaboration,
)


# ============================================================================
# Story root
# ============================================================================

STORY = Story(
    id="S_ackroyd",
    title="The Murder of Roger Ackroyd",
    character_function_template_id="dramatica-8",
    argument_ids=tuple(a.id for a in ARGUMENTS),
    throughline_ids=tuple(t.id for t in THROUGHLINES),
    character_ids=tuple(c.id for c in CHARACTERS),
    scene_ids=tuple(s.id for s in SCENES),
    beat_ids=tuple(b.id for b in BEATS),
    stakes_ids=tuple(s.id for s in STAKES),
)
