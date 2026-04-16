"""
chinatown_dramatic.py — *Chinatown* (1974) encoded in the Dramatic
dialect.

Sixth encoding at the Dramatic dialect level (after Oedipus, Macbeth,
Ackroyd, Pride and Prejudice, Rocky). Records the film's
argumentative structure: one Argument, four Throughlines under the
dramatica-8 Template, eight function-carrying Characters, ten Scenes,
four Stakes records, twenty Beats.

Pure dialect content. No substrate references; no Lowering records.
This encoding completes the canonical-ending matrix. Prior
encodings covered:

- personal-tragedy (Success × Bad): Oedipus, Macbeth, Ackroyd
- triumph (Success × Good): Pride and Prejudice
- personal-triumph (Failure × Good): Rocky

Chinatown is the first **tragedy** (Failure × Bad) in the corpus:

- **Outcome = Failure.** Jake fails to save Evelyn (she is shot
  dead in the final scene); fails to protect Katherine (Cross
  takes her); fails to stop the water conspiracy (Cross will
  have his dam). The OS goal — recover the truth and stop Cross
  — is not achieved; every lever of the investigation becomes a
  handle Cross uses against it.

- **Judgment = Bad.** Jake is broken. The film's final lines —
  'Forget it, Jake. It's Chinatown.' — are the MC accepting
  that he cannot help, cannot know, cannot intervene. He goes
  back to 'as little as possible.'

Notable features:

- **Change MC who changes BACKWARD.** Unlike Oedipus and
  Macbeth (who change toward destruction) or Pride and
  Prejudice (who changes toward happiness), Jake changes from
  competent confidence to shattered withdrawal. The change is
  real; the direction is toward the Solution (Avoid) but from
  the wrong side of the story's Argument.

- **Power-conceals-its-own-discovery Argument.** The film's
  thesis is that some truths cannot be uncovered because the
  thing to be uncovered is powerful enough to shape what can
  be known. Noah Cross IS the water department, IS the
  police's orbit, IS Evelyn's father, IS Katherine's
  grandfather-father. Each fact Jake uncovers arrives attached
  to a handle Cross will use.

- **The Guardian who is killed for warning.** Ida Sessions —
  the woman who hired Jake pretending to be Evelyn Mulwray —
  tries to warn him when she realizes things have gone wrong.
  She is killed for it. This is the first encoding in which
  the Guardian function is held by a character who dies
  mid-story for executing the Guardian role.

- **Dramatica-8 slot filled with eight distinct characters.**
  No double-function characters. Parallels Ackroyd, P&P, and
  Rocky in cleanness.

Expected verifier output (the encoding's contract):

- 0 slot_unfilled / slot_overfilled (all 8 dramatica-8 slots
  filled by distinct characters).
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

A_power_conceals = Argument(
    id="A_power_conceals",
    premise=("power sufficient to shape a place shapes what can be "
             "known about that place; the investigator who takes "
             "the case is investigating the investigator's frame"),
    counter_premise=("patient investigation eventually uncovers "
                     "truth; a skilled detective finds what is "
                     "there to be found. This is the private-eye's "
                     "operating creed, voiced by Jake throughout, "
                     "refuted by the final scene"),
    resolution_direction=ResolutionDirection.AFFIRM,
    domain="moral-epistemic",
)

ARGUMENTS = (A_power_conceals,)


# ============================================================================
# Throughlines
# ============================================================================

T_overall_water = Throughline(
    id="T_overall_water",
    role_label="overall-story",
    owners=(THROUGHLINE_OWNER_SITUATION,),
    subject=("Los Angeles in 1937; a manufactured drought; water "
             "diverted from the valley into the river at night; a "
             "land grab under cover of public-works rhetoric; the "
             "chief engineer who refused the dam found drowned in "
             "a freshwater reservoir. Noah Cross's scheme to bring "
             "the valley into the city at his price, with his "
             "name on the new intake"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_power_conceals",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_city_truth",
)

T_mc_jake = Throughline(
    id="T_mc_jake",
    role_label="main-character",
    owners=("C_jake",),
    subject=("a former LAPD officer now a private detective working "
             "matrimonial cases; carries a Chinatown wound — a woman "
             "he tried to help who was hurt because he tried to help. "
             "Takes the Mulwray case expecting another matrimonial; "
             "his arc is the full repetition of the Chinatown wound "
             "at larger scale, ending in the articulation of the "
             "lesson he cannot unlearn"),
    counterpoint_throughline_ids=("T_ic_evelyn",),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_power_conceals",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_jake_trying",
)

T_ic_evelyn = Throughline(
    id="T_ic_evelyn",
    role_label="impact-character",
    owners=("C_evelyn",),
    subject=("the dead engineer's widow; the daughter of Noah Cross; "
             "mother and sister of the same child. Carries a fixed "
             "attitude — the unreachable core formed by her father's "
             "abuse — and a fixed protective posture toward Katherine. "
             "Her impact on Jake is the slow disclosure of the thing "
             "she cannot say until the scene in which she says it, "
             "which is the scene before her death"),
    counterpoint_throughline_ids=("T_mc_jake",),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_power_conceals",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_evelyn_katherine",
)

T_rel_jake_evelyn = Throughline(
    id="T_rel_jake_evelyn",
    role_label="relationship",
    owners=(THROUGHLINE_OWNER_RELATIONSHIP,),
    subject=("a client-detective relationship that becomes a romance "
             "that is always a mutual manipulation — she hides what "
             "she cannot say, he presses toward what he cannot yet "
             "see. The relationship's shape is the escalating tension "
             "between his investigation and her withholding; it ends "
             "in the same moment she tries to deliver Katherine to "
             "safety"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_power_conceals",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_trust",
)

THROUGHLINES = (
    T_overall_water, T_mc_jake, T_ic_evelyn, T_rel_jake_evelyn,
)


# ============================================================================
# Characters
# ============================================================================
#
# dramatica-8 slot assignment for this encoding:
#
#   Protagonist   → C_jake         (pursues the case; considers
#                                    each piece of evidence; the
#                                    PI's pursuit is the Protagonist
#                                    function's cleanest form)
#   Antagonist    → C_cross        (avoids disclosure by controlling
#                                    what can be disclosed; the
#                                    ultimate author of the
#                                    counter-investigation)
#   Reason        → C_walsh        (one of Jake's partners; the
#                                    voice of professional caution;
#                                    boxing-gym logic of casework)
#   Emotion       → C_evelyn       (the film's emotional axis; her
#                                    composure conceals a feeling
#                                    core the investigation
#                                    eventually opens)
#   Sidekick      → C_duffy        (Jake's other partner; loyal,
#                                    supportive; the faith-and-
#                                    support role)
#   Skeptic       → C_escobar      (LAPD lieutenant; doubts Jake,
#                                    opposes Jake's methods,
#                                    represents the legal system's
#                                    indifference to truth)
#   Guardian      → C_ida_sessions (the woman who hired Jake as
#                                    fake-Evelyn; tries to warn him
#                                    ('you know why I didn't use my
#                                    real name'); killed for it —
#                                    the Guardian function executed
#                                    at the cost of the Guardian's
#                                    life)
#   Contagonist   → C_mulvihill    (Cross's enforcer; the man who
#                                    cuts Jake's nose; hinders the
#                                    investigation, tempts Jake to
#                                    abandon)
#
# Eight distinct characters, eight distinct function slots. No
# double-function overlap at the function_label level. Jake's MC
# role is Throughline ownership, not a second label. Characters
# present but carrying no dramatica-8 function: Hollis Mulwray (the
# murdered engineer — appears in the opening-scene autopsy and as
# backstory), Yelburton (Mulwray's deputy at Water and Power —
# passive obstacle), Katherine Mulwray (Evelyn's daughter-sister —
# the innocent whose future is the story's deepest loss).

C_jake = Character(
    id="C_jake", name="J.J. \"Jake\" Gittes",
    function_labels=("Protagonist",),
)

C_evelyn = Character(
    id="C_evelyn", name="Evelyn Cross Mulwray",
    function_labels=("Emotion",),
)

C_cross = Character(
    id="C_cross", name="Noah Cross",
    function_labels=("Antagonist",),
)

C_walsh = Character(
    id="C_walsh", name="Walsh",
    function_labels=("Reason",),
)

C_duffy = Character(
    id="C_duffy", name="Duffy",
    function_labels=("Sidekick",),
)

C_escobar = Character(
    id="C_escobar", name="Lt. Lou Escobar",
    function_labels=("Skeptic",),
)

C_ida_sessions = Character(
    id="C_ida_sessions", name="Ida Sessions",
    function_labels=("Guardian",),
)

C_mulvihill = Character(
    id="C_mulvihill", name="Claude Mulvihill",
    function_labels=("Contagonist",),
)

# Narratively important but carrying no dramatica-8 function slot.

C_hollis_mulwray = Character(
    id="C_hollis_mulwray", name="Hollis Mulwray",
    function_labels=(),
)

C_yelburton = Character(
    id="C_yelburton", name="Russ Yelburton",
    function_labels=(),
)

C_katherine = Character(
    id="C_katherine", name="Katherine Mulwray",
    function_labels=(),
)

CHARACTERS = (
    C_jake, C_evelyn, C_cross, C_walsh, C_duffy,
    C_escobar, C_ida_sessions, C_mulvihill,
    C_hollis_mulwray, C_yelburton, C_katherine,
)


# ============================================================================
# Beats — per Throughline, ordered by beat_position
# ============================================================================

BEATS = (
    # T_overall_water — the water-scheme arc from the opening
    # misdirection to the Chinatown street
    Beat(id="B_op_1", throughline_id="T_overall_water",
         beat_position=1, beat_type="inciting",
         description_of_change=("fake Evelyn hires Jake to follow her "
                                "husband; the water-and-power engineer "
                                "is photographed with a young woman; "
                                "the real Mrs. Mulwray surfaces with "
                                "a lawyer and the case pivots")),
    Beat(id="B_op_2", throughline_id="T_overall_water",
         beat_position=2, beat_type="rising",
         description_of_change=("Hollis Mulwray is found drowned in a "
                                "freshwater reservoir; the city has a "
                                "murdered chief engineer and a "
                                "drought; the case Jake was hired to "
                                "run matrimonial on has become a "
                                "murder and a scheme")),
    Beat(id="B_op_3", throughline_id="T_overall_water",
         beat_position=3, beat_type="rising",
         description_of_change=("Jake follows the water — valley "
                                "orchards poisoned at night, reservoirs "
                                "dumped in the river, a land grab under "
                                "cover of public works; the scheme "
                                "resolves into Noah Cross's name")),
    Beat(id="B_op_4", throughline_id="T_overall_water",
         beat_position=4, beat_type="climax",
         description_of_change=("final Chinatown scene; Evelyn shot "
                                "while fleeing with Katherine; Cross "
                                "takes Katherine; Escobar restrains "
                                "Jake; the scheme wins, unblocked and "
                                "permanent")),
    Beat(id="B_op_5", throughline_id="T_overall_water",
         beat_position=5, beat_type="denouement",
         description_of_change=("'as little as possible'; the dam "
                                "will be built; Cross will have the "
                                "valley; the investigation has "
                                "produced the evidence, but the "
                                "evidence will not be used")),

    # T_mc_jake — the PI's arc from confident pursuit to shattered
    # acceptance
    Beat(id="B_mc_1", throughline_id="T_mc_jake",
         beat_position=1, beat_type="inciting",
         description_of_change=("Jake takes the fake-Evelyn case; "
                                "professional confidence; runs "
                                "matrimonials well; this looks like "
                                "another one")),
    Beat(id="B_mc_2", throughline_id="T_mc_jake",
         beat_position=2, beat_type="rising",
         description_of_change=("real Evelyn's lawsuit exposes the "
                                "frame; Jake realizes he's been used "
                                "to manufacture a scandal; the "
                                "professional wound goes from "
                                "matrimonial to real")),
    Beat(id="B_mc_3", throughline_id="T_mc_jake",
         beat_position=3, beat_type="rising",
         description_of_change=("Mulvihill and the man with the "
                                "knife in the orange grove; the "
                                "slit nose; the investigation has "
                                "cost Jake's face; he keeps going")),
    Beat(id="B_mc_4", throughline_id="T_mc_jake",
         beat_position=4, beat_type="climax",
         description_of_change=("the slap scene with Evelyn — 'my "
                                "sister / my daughter / my sister "
                                "AND my daughter'; the Chinatown "
                                "wound at full scale; the "
                                "investigation has found what it "
                                "cannot make right")),
    Beat(id="B_mc_5", throughline_id="T_mc_jake",
         beat_position=5, beat_type="denouement",
         description_of_change=("Chinatown again; Evelyn dead; the "
                                "lesson the PI cannot unlearn is "
                                "articulated for him by Walsh: "
                                "'forget it, Jake. It's Chinatown'")),

    # T_ic_evelyn — the interior figure whose disclosure kills her
    Beat(id="B_ic_1", throughline_id="T_ic_evelyn",
         beat_position=1, beat_type="inciting",
         description_of_change=("Evelyn arrives in Jake's office with "
                                "her lawyer; composed surface; the "
                                "lawsuit is performed, not felt; the "
                                "fixed attitude presents itself as "
                                "control")),
    Beat(id="B_ic_2", throughline_id="T_ic_evelyn",
         beat_position=2, beat_type="rising",
         description_of_change=("she hires Jake in earnest after "
                                "Hollis's death; a reluctant "
                                "collaboration; Jake finds her "
                                "evasions everywhere — the composure "
                                "is the cover story")),
    Beat(id="B_ic_3", throughline_id="T_ic_evelyn",
         beat_position=3, beat_type="midpoint",
         description_of_change=("the hidden Katherine; Evelyn's "
                                "protective posture revealed in "
                                "action; Jake does not yet know who "
                                "Katherine is, only that Evelyn "
                                "shields her")),
    Beat(id="B_ic_4", throughline_id="T_ic_evelyn",
         beat_position=4, beat_type="climax",
         description_of_change=("the slapping scene — 'my daughter, "
                                "my sister'; the fixed attitude's "
                                "ground laid bare; she discloses "
                                "what she has spent fifteen years "
                                "not disclosing")),
    Beat(id="B_ic_5", throughline_id="T_ic_evelyn",
         beat_position=5, beat_type="denouement",
         description_of_change=("shot through the back of the head "
                                "in the car; the attempted escape "
                                "with Katherine fails; the "
                                "disclosure's cost is her life")),

    # T_rel_jake_evelyn — a relationship of escalating mutual
    # manipulation
    Beat(id="B_rel_1", throughline_id="T_rel_jake_evelyn",
         beat_position=1, beat_type="inciting",
         description_of_change=("client-detective first contact; "
                                "lawsuit as opening move; her "
                                "composure; his professionalism; "
                                "each reads the other incorrectly")),
    Beat(id="B_rel_2", throughline_id="T_rel_jake_evelyn",
         beat_position=2, beat_type="rising",
         description_of_change=("the real hiring; the reluctant "
                                "collaboration; Jake presses, "
                                "Evelyn evades; the detective-subject "
                                "dance, conducted politely")),
    Beat(id="B_rel_3", throughline_id="T_rel_jake_evelyn",
         beat_position=3, beat_type="rising",
         description_of_change=("the night they become lovers; "
                                "tenderness that does not dissolve "
                                "the withholding; he sees the "
                                "bathing-and-bandaging of her "
                                "bruises")),
    Beat(id="B_rel_4", throughline_id="T_rel_jake_evelyn",
         beat_position=4, beat_type="climax",
         description_of_change=("the slapping confession; the "
                                "relationship reaches the disclosure "
                                "Evelyn has avoided; Jake promises "
                                "to help her escape")),
    Beat(id="B_rel_5", throughline_id="T_rel_jake_evelyn",
         beat_position=5, beat_type="denouement",
         description_of_change=("Chinatown; the escape fails; "
                                "Evelyn shot; Jake held back by "
                                "Escobar; the relationship ends at "
                                "the cost of her life and his "
                                "agency")),
)


# ============================================================================
# Scenes
# ============================================================================

S_fake_evelyn_hire = Scene(
    id="S_fake_evelyn_hire", title="The fake Evelyn hires Jake",
    narrative_position=1,
    advances=(
        SceneAdvancement(throughline_id="T_overall_water",
                         beat_id="B_op_1"),
        SceneAdvancement(throughline_id="T_mc_jake",
                         beat_id="B_mc_1"),
    ),
    conflict_shape=("a woman presents herself as Mrs. Mulwray and "
                    "asks Jake to follow her husband; the hiring "
                    "conversation is professional; the case looks "
                    "routine"),
    result=("Jake takes the case; Ida Sessions's role is concealed "
            "behind the performance of an aggrieved wife"),
)

S_hollis_surveillance = Scene(
    id="S_hollis_surveillance",
    title="Surveillance and the photographed girl",
    narrative_position=2,
    advances=(
        SceneAdvancement(throughline_id="T_mc_jake",
                         beat_id="B_mc_2"),
    ),
    conflict_shape=("Jake follows Hollis Mulwray; public meetings "
                    "with engineers; a young woman photographed "
                    "with him at the park; the photos run in the "
                    "papers next morning"),
    result=("the scandal is public; Jake has delivered what he was "
            "hired for; the real Mrs. Mulwray is reading it over "
            "coffee"),
)

S_real_evelyn_arrives = Scene(
    id="S_real_evelyn_arrives",
    title="The real Evelyn Mulwray",
    narrative_position=3,
    advances=(
        SceneAdvancement(throughline_id="T_ic_evelyn",
                         beat_id="B_ic_1"),
        SceneAdvancement(throughline_id="T_rel_jake_evelyn",
                         beat_id="B_rel_1"),
    ),
    conflict_shape=("the real Evelyn arrives in Jake's office with "
                    "her lawyer and a lawsuit; the lawsuit is the "
                    "opening move; Jake realizes he has been "
                    "manipulated into producing a scandal"),
    result=("Jake is on the hook; the case was a frame; the woman "
            "across from him is the actual Mrs. Mulwray and she is "
            "not what he expected"),
)

S_hollis_found = Scene(
    id="S_hollis_found",
    title="Hollis Mulwray drowned",
    narrative_position=4,
    advances=(
        SceneAdvancement(throughline_id="T_overall_water",
                         beat_id="B_op_2"),
    ),
    conflict_shape=("Hollis Mulwray's body is pulled from a "
                    "freshwater reservoir in a dry city; Escobar "
                    "and the LAPD attend; Jake attends; the "
                    "engineer who refused the dam is dead"),
    result=("the case is now a murder; the water scheme is active; "
            "Jake moves from matrimonial work to investigation of "
            "a killing"),
)

S_orange_grove = Scene(
    id="S_orange_grove",
    title="The orange grove and the knife",
    narrative_position=5,
    advances=(
        SceneAdvancement(throughline_id="T_overall_water",
                         beat_id="B_op_3"),
        SceneAdvancement(throughline_id="T_mc_jake",
                         beat_id="B_mc_3"),
    ),
    conflict_shape=("Jake investigates the night-dumping of water "
                    "in the orchards; is caught by Mulvihill and a "
                    "small knife-carrying henchman; his nose is "
                    "slit; he keeps going"),
    result=("Jake is warned in blood; he continues; the investigation "
            "costs him his face and he raises the price of what "
            "he's investigating"),
)

S_ida_sessions_call = Scene(
    id="S_ida_sessions_call",
    title="Ida Sessions tries to warn him",
    narrative_position=6,
    advances=(
        SceneAdvancement(throughline_id="T_overall_water",
                         beat_id="B_op_3"),
    ),
    conflict_shape=("the real fake-Evelyn calls Jake to warn him "
                    "— 'you know why I didn't use my real name'; "
                    "she gives him a partial clue about the "
                    "obituary page"),
    result=("Jake has a new clue; Ida Sessions has executed the "
            "Guardian function; when Jake reaches her apartment "
            "she is dead on the kitchen floor"),
)

S_affair_night = Scene(
    id="S_affair_night",
    title="The night they become lovers",
    narrative_position=7,
    advances=(
        SceneAdvancement(throughline_id="T_rel_jake_evelyn",
                         beat_id="B_rel_3"),
        SceneAdvancement(throughline_id="T_ic_evelyn",
                         beat_id="B_ic_2"),
    ),
    conflict_shape=("Evelyn bandages Jake's nose at her house; "
                    "tenderness that does not disclose; an affair "
                    "that does not dissolve the withholding; Jake "
                    "sees a flaw in her iris in morning light"),
    result=("the relationship has a before and an after; neither "
            "party has been candid; the tenderness is real and "
            "the withholding is real"),
)

S_hidden_katherine = Scene(
    id="S_hidden_katherine",
    title="Jake finds Katherine",
    narrative_position=8,
    advances=(
        SceneAdvancement(throughline_id="T_ic_evelyn",
                         beat_id="B_ic_3"),
        SceneAdvancement(throughline_id="T_rel_jake_evelyn",
                         beat_id="B_rel_2"),
    ),
    conflict_shape=("Jake finds Evelyn hiding a young woman in a "
                    "house under domestic-servant names; Evelyn's "
                    "cover story does not hold; she will not tell "
                    "him who the girl is"),
    result=("Jake sees the protective posture without seeing its "
            "ground; the relationship is now a triangle with an "
            "unnamed third party; Evelyn's evasions are the "
            "posture he does not yet read correctly"),
)

S_slap_confession = Scene(
    id="S_slap_confession",
    title="'My sister. My daughter.'",
    narrative_position=9,
    advances=(
        SceneAdvancement(throughline_id="T_mc_jake",
                         beat_id="B_mc_4"),
        SceneAdvancement(throughline_id="T_ic_evelyn",
                         beat_id="B_ic_4"),
        SceneAdvancement(throughline_id="T_rel_jake_evelyn",
                         beat_id="B_rel_4"),
    ),
    conflict_shape=("Jake corners Evelyn; the slapping cascade; "
                    "'my sister / my daughter / my sister AND my "
                    "daughter'; the fifteen-year concealment "
                    "arrives in a sentence"),
    result=("Jake learns what Evelyn has not been able to say; the "
            "disclosure is the relationship's highest trust and "
            "the story's deepest wound; Jake promises to help her "
            "escape with Katherine"),
)

S_chinatown = Scene(
    id="S_chinatown", title="Chinatown",
    narrative_position=10,
    advances=(
        SceneAdvancement(throughline_id="T_overall_water",
                         beat_id="B_op_4"),
        SceneAdvancement(throughline_id="T_overall_water",
                         beat_id="B_op_5"),
        SceneAdvancement(throughline_id="T_mc_jake",
                         beat_id="B_mc_5"),
        SceneAdvancement(throughline_id="T_ic_evelyn",
                         beat_id="B_ic_5"),
        SceneAdvancement(throughline_id="T_rel_jake_evelyn",
                         beat_id="B_rel_5"),
    ),
    conflict_shape=("the escape to Mexico through Chinatown at "
                    "night; the police waiting; Cross claiming "
                    "Katherine; Evelyn shooting and being shot in "
                    "the head by the police fire through the car; "
                    "Escobar restraining Jake"),
    result=("Evelyn dead; Katherine taken by her grandfather-father; "
            "the water scheme unblocked; Walsh says the line that "
            "has been the story's hidden thesis: 'forget it, Jake. "
            "It's Chinatown.'"),
)

SCENES = (
    S_fake_evelyn_hire, S_hollis_surveillance, S_real_evelyn_arrives,
    S_hollis_found, S_orange_grove, S_ida_sessions_call,
    S_affair_night, S_hidden_katherine, S_slap_confession,
    S_chinatown,
)


# ============================================================================
# Stakes
# ============================================================================

Stakes_city_truth = Stakes(
    id="Stakes_city_truth",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_overall_water"),
    at_risk=("the truth of how Los Angeles is being watered; the "
             "integrity of the public-works apparatus; the lives "
             "already lost (Hollis Mulwray, Ida Sessions) and the "
             "lives still at risk (Evelyn, Katherine); the moral "
             "standing of the city"),
    to_gain=("recovery of the scheme; restoration of the water; "
             "the murderer named publicly; the innocent protected; "
             "the dam prevented"),
    external_manifestation=("the night-dumping in the orange groves; "
                            "the obituary scheme (dead people as "
                            "landowners); the photographs used and "
                            "mis-used; the reservoir autopsy; the "
                            "final Chinatown scene"),
)

Stakes_jake_trying = Stakes(
    id="Stakes_jake_trying",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_mc_jake"),
    at_risk=("Jake's capacity to try; the PI's operating creed "
             "that a case is workable; the professional self that "
             "has been rebuilt since the Chinatown wound; his "
             "willingness to help the next woman who walks in"),
    to_gain=("the case broken cleanly; Cross indicted; Evelyn "
             "and Katherine out; the Chinatown wound refuted by "
             "a case that ends differently"),
    external_manifestation=("the slit nose; the professional "
                            "confidence eroding across scenes; the "
                            "slap-confession where trying reaches "
                            "its limit; the final 'forget it, Jake' "
                            "as the trying's surrender"),
)

Stakes_evelyn_katherine = Stakes(
    id="Stakes_evelyn_katherine",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_ic_evelyn"),
    at_risk=("Katherine's protection from her grandfather-father; "
             "Evelyn's fifteen-year concealment; the fixed "
             "attitude that has been the structure holding Evelyn's "
             "life together since the abuse"),
    to_gain=("Katherine in Mexico, out of Cross's reach; the "
             "disclosure to Jake as the first time Evelyn has "
             "told anyone; the release of the fixed attitude "
             "into something a life can be built on"),
    external_manifestation=("the hiding of Katherine under "
                            "servant names; the composed surfaces "
                            "across scenes; the bandaging of Jake "
                            "that does not disclose; the "
                            "slap-confession; the final car and "
                            "the shot through the head"),
)

Stakes_trust = Stakes(
    id="Stakes_trust",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_rel_jake_evelyn"),
    at_risk=("whether the relationship can hold the withholdings "
             "on both sides; whether Jake can trust what Evelyn "
             "does not say; whether Evelyn can trust Jake with "
             "the thing she cannot say"),
    to_gain=("a relationship that survives the disclosure; a "
             "partnership across the case that ends it cleanly "
             "and leaves both parties standing"),
    external_manifestation=("the cold first meetings; the real "
                            "hiring; the affair night; the hidden "
                            "Katherine; the slap-confession; the "
                            "final escape attempt that does not "
                            "succeed"),
)

STAKES = (
    Stakes_city_truth, Stakes_jake_trying,
    Stakes_evelyn_katherine, Stakes_trust,
)


# ============================================================================
# Story root
# ============================================================================

STORY = Story(
    id="S_chinatown",
    title="Chinatown",
    character_function_template_id="dramatica-8",
    argument_ids=tuple(a.id for a in ARGUMENTS),
    throughline_ids=tuple(t.id for t in THROUGHLINES),
    character_ids=tuple(c.id for c in CHARACTERS),
    scene_ids=tuple(s.id for s in SCENES),
    beat_ids=tuple(b.id for b in BEATS),
    stakes_ids=tuple(s.id for s in STAKES),
)
