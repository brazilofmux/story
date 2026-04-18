"""
oedipus_dramatic.py — *Oedipus Rex* encoded in the Dramatic dialect.

First encoding at the Dramatic dialect level (parallel to oedipus.py
at the substrate level). Records the story's argumentative structure:
one Argument, four Throughlines under the dramatica-8 Template,
six Characters, eight Scenes, two Stakes records, twenty-one Beats.

Pure dialect content. No substrate references; no Lowering records
(those will live in a separate module once lowering-record-sketch-01's
machinery is implemented). The encoding is meant to be self-contained
in Dramatic terms.

Encoding choices, made explicit:

- Template: dramatica-8 with one slot intentionally unfilled
  (Antagonist). The "antagonist" of *Oedipus Rex* is the truth itself,
  which resists assignment to a single Character. The verifier will
  surface this as a slot-unfilled observation; the author's choice is
  to accept it as a feature of the play (Sophocles built a story whose
  antagonist is abstract).

- Cuts: this encoding includes Tiresias and Creon (which oedipus.py
  cuts at the substrate level for the identity-probe slice) and the
  three post-anagnorisis Scenes (S_jocasta_hangs, S_self_blinding,
  S_exile). Future Lowering work will surface F5 substrate-gaps:
  these dialect Scenes have no substrate event to bind to until
  oedipus.py is extended.

- Authored-by: this file authors records as "author"; nothing is
  LLM-authored at this layer yet.

- narrative_position values: the play's roughly-linear structure
  matches sjuzhet ordering, so positions 0..14 track the play's
  unfolding. The Lowering work will declare position-correspondence
  to substrate τ_d.

Run the M8 self-verifier on the encoding via:

    python3 -c 'import oedipus_dramatic as o; \
                from story_engine.core.dramatic import verify; \
                obs = verify(o.STORY, arguments=o.ARGUMENTS, \
                             throughlines=o.THROUGHLINES, \
                             characters=o.CHARACTERS, scenes=o.SCENES, \
                             beats=o.BEATS, stakes=o.STAKES); \
                [print(f"[{x.severity}] {x.code}: {x.message}") for x in obs]'
"""

from __future__ import annotations

from story_engine.core.dramatic import (
    Story, Argument, Throughline, Character, Beat, Scene, Stakes,
    ArgumentContribution, SceneAdvancement, StakesOwner,
    ResolutionDirection, ArgumentSide, StakesOwnerKind,
    THROUGHLINE_OWNER_SITUATION, THROUGHLINE_OWNER_RELATIONSHIP,
)


# ============================================================================
# Argument
# ============================================================================

A_knowledge_unmakes = Argument(
    id="A_knowledge_unmakes",
    premise="knowledge of self is the unmaking of the self",
    counter_premise=("ignorance preserves what knowledge would destroy; "
                     "Jocasta's plea is the play's voice for the "
                     "counter-premise"),
    resolution_direction=ResolutionDirection.AFFIRM,
    domain="moral-philosophical",
)

ARGUMENTS = (A_knowledge_unmakes,)


# ============================================================================
# Throughlines
# ============================================================================

T_overall_plague = Throughline(
    id="T_overall_plague",
    role_label="overall-story",
    owners=(THROUGHLINE_OWNER_SITUATION,),
    subject=("a city under divine curse needs its pollution identified "
             "and expelled; the king investigates"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_knowledge_unmakes",
            side=ArgumentSide.COMPLICATES,
        ),
    ),
    stakes_id="Stakes_thebes",
)

T_mc_oedipus = Throughline(
    id="T_mc_oedipus",
    role_label="main-character",
    owners=("C_oedipus",),
    subject=("a king determined to find the truth of who killed his "
             "predecessor, at any cost to himself"),
    counterpoint_throughline_ids=("T_impact_jocasta",),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_knowledge_unmakes",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_oedipus_self",
)

T_impact_jocasta = Throughline(
    id="T_impact_jocasta",
    role_label="impact-character",
    owners=("C_jocasta",),
    subject=("a queen who has already chosen not to know, trying to "
             "pull the MC into her choice; her own anagnorisis comes "
             "first, but she keeps it from him"),
    counterpoint_throughline_ids=("T_mc_oedipus",),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_knowledge_unmakes",
            side=ArgumentSide.OPPOSES,
        ),
    ),
)

T_relationship_oj = Throughline(
    id="T_relationship_oj",
    role_label="relationship",
    owners=(THROUGHLINE_OWNER_RELATIONSHIP,),
    subject=("a marriage in which truth is the third party; its "
             "revelation ends the marriage"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_knowledge_unmakes",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
)

THROUGHLINES = (
    T_overall_plague, T_mc_oedipus, T_impact_jocasta, T_relationship_oj,
)


# ============================================================================
# Characters
# ============================================================================

C_oedipus = Character(
    id="C_oedipus", name="Oedipus",
    function_labels=("Protagonist", "Emotion"),
)

C_jocasta = Character(
    id="C_jocasta", name="Jocasta",
    function_labels=("Skeptic",),
)

C_tiresias = Character(
    id="C_tiresias", name="Tiresias",
    function_labels=("Reason",),
)

C_creon = Character(
    id="C_creon", name="Creon",
    function_labels=("Sidekick",),
)

C_shepherd = Character(
    id="C_shepherd", name="the Theban Shepherd",
    function_labels=("Guardian",),
)

C_messenger = Character(
    id="C_messenger", name="the Corinthian Messenger",
    function_labels=("Contagonist",),
)

# Notably no Character carries the Antagonist label. The
# dramatica-8 Template's Antagonist slot will surface as
# "slot_unfilled" — author-accepted gap.

CHARACTERS = (
    C_oedipus, C_jocasta, C_tiresias, C_creon, C_shepherd, C_messenger,
)


# ============================================================================
# Beats — per Throughline, ordered by beat_position
# ============================================================================

BEATS = (
    # T_overall_plague — the kingdom's investigation arc
    Beat(id="B_op_1", throughline_id="T_overall_plague",
         beat_position=1, beat_type="inciting",
         description_of_change=("the plague forces the question; "
                                "Oedipus pledges to find its source")),
    Beat(id="B_op_2", throughline_id="T_overall_plague",
         beat_position=2, beat_type="rising",
         description_of_change=("Tiresias accuses the king; the public "
                                "investigation has its first shock")),
    Beat(id="B_op_3", throughline_id="T_overall_plague",
         beat_position=3, beat_type="midpoint",
         description_of_change=("the messenger's reveal collapses the "
                                "Polybus assumption; the question turns "
                                "from 'who killed Laius' to 'who is Oedipus'")),
    Beat(id="B_op_4", throughline_id="T_overall_plague",
         beat_position=4, beat_type="climax",
         description_of_change=("the shepherd's testimony locks in the "
                                "answer the city needed and the king feared")),
    Beat(id="B_op_5", throughline_id="T_overall_plague",
         beat_position=5, beat_type="denouement",
         description_of_change=("Oedipus exiled; the pollution leaves "
                                "with him; the plague will lift")),

    # T_mc_oedipus — Oedipus's epistemic descent
    Beat(id="B_mc_1", throughline_id="T_mc_oedipus",
         beat_position=1, beat_type="inciting",
         description_of_change=("the king accepts the duty to investigate; "
                                "his certainty about himself is total")),
    Beat(id="B_mc_2", throughline_id="T_mc_oedipus",
         beat_position=2, beat_type="rising",
         description_of_change=("Tiresias's accusation; Oedipus rejects "
                                "it but the seed is planted")),
    Beat(id="B_mc_3", throughline_id="T_mc_oedipus",
         beat_position=3, beat_type="midpoint",
         description_of_change=("Jocasta's mention of the crossroads "
                                "introduces the first private dread")),
    Beat(id="B_mc_4", throughline_id="T_mc_oedipus",
         beat_position=4, beat_type="rising",
         description_of_change=("the messenger's adoption reveal "
                                "dislodges the Polybus identity; gap opens")),
    Beat(id="B_mc_5", throughline_id="T_mc_oedipus",
         beat_position=5, beat_type="climax",
         description_of_change=("the anagnorisis: identity assertions "
                                "lock; he is the killer, the son, the husband")),
    Beat(id="B_mc_6", throughline_id="T_mc_oedipus",
         beat_position=6, beat_type="denouement",
         description_of_change=("self-blinding and exile; the resolved-into-"
                                "tyrant arc closes")),

    # T_impact_jocasta — Jocasta's parallel descent (compressed)
    Beat(id="B_ic_1", throughline_id="T_impact_jocasta",
         beat_position=1, beat_type="inciting",
         description_of_change=("she counsels Oedipus that prophecies "
                                "fail; her counter-premise voiced")),
    Beat(id="B_ic_2", throughline_id="T_impact_jocasta",
         beat_position=2, beat_type="rising",
         description_of_change=("she mentions the crossroads detail; "
                                "her own anagnorisis begins forming")),
    Beat(id="B_ic_3", throughline_id="T_impact_jocasta",
         beat_position=3, beat_type="climax",
         description_of_change=("her anagnorisis lands; she begs the "
                                "king to stop; he refuses")),
    Beat(id="B_ic_4", throughline_id="T_impact_jocasta",
         beat_position=4, beat_type="denouement",
         description_of_change=("she hangs herself off-stage; the "
                                "counter-premise's voice silenced")),

    # T_relationship_oj — the marriage's collapse arc
    Beat(id="B_rel_1", throughline_id="T_relationship_oj",
         beat_position=1, beat_type="inciting",
         description_of_change=("the marriage exists as functioning "
                                "queen-king bond; the truth has not "
                                "yet entered the room")),
    Beat(id="B_rel_2", throughline_id="T_relationship_oj",
         beat_position=2, beat_type="rising",
         description_of_change=("Jocasta tries to comfort him; her "
                                "counter-premise about prophecies is "
                                "the marriage's voice for the wrong answer")),
    Beat(id="B_rel_3", throughline_id="T_relationship_oj",
         beat_position=3, beat_type="midpoint",
         description_of_change=("the messenger's reveal; the marriage "
                                "now contains a question that cannot "
                                "be unspoken")),
    Beat(id="B_rel_4", throughline_id="T_relationship_oj",
         beat_position=4, beat_type="climax",
         description_of_change=("Jocasta's anagnorisis; she knows the "
                                "marriage is a horror; he does not yet")),
    Beat(id="B_rel_5", throughline_id="T_relationship_oj",
         beat_position=5, beat_type="denouement",
         description_of_change=("the marriage ends in his recognition "
                                "and her death")),
)


# ============================================================================
# Scenes
# ============================================================================

S_prologue_plague = Scene(
    id="S_prologue_plague", title="The plague",
    narrative_position=1,
    advances=(
        SceneAdvancement(throughline_id="T_overall_plague", beat_id="B_op_1"),
        SceneAdvancement(throughline_id="T_mc_oedipus",     beat_id="B_mc_1"),
    ),
    conflict_shape=("the city brings its suffering to the king; the "
                    "king binds himself to its solution"),
    result=("Oedipus pledges to find Laius's killer; the investigation "
            "is launched"),
)

S_tiresias_accusation = Scene(
    id="S_tiresias_accusation", title="Tiresias accuses",
    narrative_position=2,
    advances=(
        SceneAdvancement(throughline_id="T_overall_plague", beat_id="B_op_2"),
        SceneAdvancement(throughline_id="T_mc_oedipus",     beat_id="B_mc_2"),
    ),
    conflict_shape=("the blind prophet, pressed for truth, names the "
                    "MC as the pollution; the MC rejects this as "
                    "political attack"),
    result=("MC's investigative certainty deepens, now including "
            "suspicion of Tiresias+Creon conspiracy; the name is in "
            "the air"),
)

S_jocasta_doubt_speech = Scene(
    id="S_jocasta_doubt_speech", title="Jocasta doubts the oracles",
    narrative_position=3,
    advances=(
        SceneAdvancement(throughline_id="T_impact_jocasta",  beat_id="B_ic_1"),
        SceneAdvancement(throughline_id="T_relationship_oj", beat_id="B_rel_2"),
        SceneAdvancement(throughline_id="T_mc_oedipus",      beat_id="B_mc_3"),
    ),
    conflict_shape=("she tries to comfort him by dismissing prophecy; "
                    "her example mentions the crossroads"),
    result=("MC's first private dread; the IC's counter-premise is now "
            "in the marriage"),
)

S_messenger_arrives = Scene(
    id="S_messenger_arrives", title="The Corinthian messenger",
    narrative_position=4,
    advances=(
        SceneAdvancement(throughline_id="T_overall_plague",  beat_id="B_op_3"),
        SceneAdvancement(throughline_id="T_mc_oedipus",      beat_id="B_mc_4"),
        SceneAdvancement(throughline_id="T_impact_jocasta",  beat_id="B_ic_2"),
        SceneAdvancement(throughline_id="T_relationship_oj", beat_id="B_rel_3"),
    ),
    conflict_shape=("a messenger meaning to comfort reveals the "
                    "Polybus-not-father fact; the wrong question turns "
                    "into the right one"),
    result=("Oedipus's adopted-by-Polybus belief is dislodged; a gap "
            "opens about his real parentage"),
)

S_jocasta_realizes = Scene(
    id="S_jocasta_realizes", title="Jocasta's anagnorisis",
    narrative_position=5,
    advances=(
        SceneAdvancement(throughline_id="T_impact_jocasta",  beat_id="B_ic_3"),
        SceneAdvancement(throughline_id="T_relationship_oj", beat_id="B_rel_4"),
    ),
    conflict_shape=("she sees what he hasn't yet; she begs him to "
                    "stop the investigation"),
    result=("Jocasta knows; she pleads; he refuses; she leaves the "
            "stage to hang herself"),
)

S_shepherd_testimony = Scene(
    id="S_shepherd_testimony", title="The shepherd's testimony",
    narrative_position=6,
    advances=(
        SceneAdvancement(throughline_id="T_overall_plague", beat_id="B_op_4"),
    ),
    conflict_shape=("the king pressures the witness who can confirm "
                    "or deny what he most fears"),
    result=("the shepherd's account combines with the messenger's into "
            "the inevitable conclusion"),
)

S_anagnorisis = Scene(
    id="S_anagnorisis", title="Oedipus realizes",
    narrative_position=7,
    advances=(
        SceneAdvancement(throughline_id="T_mc_oedipus", beat_id="B_mc_5"),
    ),
    conflict_shape=("the testimonies' combination is the recognition; "
                    "no further pressure needed; he sees"),
    result=("the Argument's premise lands in the MC's own perception; "
            "knowledge of self has unmade him"),
)

S_jocasta_hangs = Scene(
    id="S_jocasta_hangs", title="Jocasta found dead",
    narrative_position=8,
    advances=(
        SceneAdvancement(throughline_id="T_impact_jocasta",  beat_id="B_ic_4"),
        SceneAdvancement(throughline_id="T_relationship_oj", beat_id="B_rel_5"),
    ),
    conflict_shape=("the marriage's IC voice silenced by self-killing; "
                    "the MC arrives too late"),
    result=("Jocasta is dead; the marriage has ended physically as "
            "well as epistemically"),
)

S_self_blinding = Scene(
    id="S_self_blinding", title="The self-blinding",
    narrative_position=9,
    advances=(
        SceneAdvancement(throughline_id="T_mc_oedipus", beat_id="B_mc_6"),
    ),
    conflict_shape=("the MC turns his agency on himself; the eyes "
                    "that saw too much are unmade"),
    result=("Oedipus blinds himself with Jocasta's brooches; the "
            "tragedy's signature image lands"),
)

S_exile = Scene(
    id="S_exile", title="Exile",
    narrative_position=10,
    advances=(
        SceneAdvancement(throughline_id="T_overall_plague", beat_id="B_op_5"),
    ),
    conflict_shape=("the city sends out its pollution; the MC accepts "
                    "his expulsion"),
    result=("Oedipus exits the polis; the plague will lift; Thebes can "
            "begin again under Creon"),
)

SCENES = (
    S_prologue_plague,
    S_tiresias_accusation,
    S_jocasta_doubt_speech,
    S_messenger_arrives,
    S_jocasta_realizes,
    S_shepherd_testimony,
    S_anagnorisis,
    S_jocasta_hangs,
    S_self_blinding,
    S_exile,
)


# ============================================================================
# Stakes
# ============================================================================

Stakes_oedipus_self = Stakes(
    id="Stakes_oedipus_self",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T_mc_oedipus"),
    at_risk=("Oedipus's identity as legitimate king; his marriage; "
             "his innocence of the very crime he's investigating; "
             "ultimately his sight and his place in Thebes"),
    to_gain=("the city's salvation from plague; the satisfaction of "
             "his oath to his people"),
    external_manifestation=("the plague itself — withering crops, "
                            "miscarrying women — insists the stakes "
                            "into visibility"),
)

Stakes_thebes = Stakes(
    id="Stakes_thebes",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T_overall_plague"),
    at_risk="the kingdom itself; its capacity to continue as Thebes",
    to_gain="restoration of natural order; the lifting of divine punishment",
    external_manifestation=("the same plague Oedipus's stakes manifest "
                            "through; the city's stakes and the king's "
                            "are externally indistinguishable until "
                            "the anagnorisis"),
)

STAKES = (Stakes_oedipus_self, Stakes_thebes)


# ============================================================================
# Story root
# ============================================================================

STORY = Story(
    id="S_oedipus_rex",
    title="Oedipus Rex",
    character_function_template_id="dramatica-8",
    argument_ids=tuple(a.id for a in ARGUMENTS),
    throughline_ids=tuple(t.id for t in THROUGHLINES),
    character_ids=tuple(c.id for c in CHARACTERS),
    scene_ids=tuple(s.id for s in SCENES),
    beat_ids=tuple(b.id for b in BEATS),
    stakes_ids=tuple(s.id for s in STAKES),
)
