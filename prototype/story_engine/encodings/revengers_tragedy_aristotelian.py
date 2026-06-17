"""
The Revenger's Tragedy — Aristotelian overlay (Session 2).

Sibling to `revengers_tragedy.py` (the substrate skeleton, Session 1).
Authors the Aristotelian dialect overlay (sketches 01-07): one ArMythos,
three ArPhases, seven ArCharacters, ONE ArCharacterArcRelation, a
one-step anagnorisis chain, the sketch-04 hard/soft extension fields,
and (sketch-07) the A22 pathos-centre field + A23 pathos_carrier flags.
Verifies clean against the real FABULA (noted-only observations
expected; see the Session-4 tests).

**LANDED (sketch-07, 2026-06-17).** OQ-MALFI-3 — the forcing target this
encoding was built to press — is now CLOSED. The pathos-centre claim,
described below as living under *semantic stretch*, now has its typed
home: A22 `ArMythos.pathos_character_ref_ids=("ar_gloriana",
"ar_antonio_wife")` + A23 `pathos_carrier=True` on both. The overloaded
`AR_PATHOS_CLUSTER_PARALLEL` relation (the stretch) is RETIRED. The
narrative below is preserved as the forcing record; OQ_MALFI_3_FINDING
carries the closure note.

**Primary forcing target: OQ-MALFI-3 (pathos-hero vs arc-hero split).**
Surfaced by the Malfi Session-6 re-probe and banked as the strongest
new finding: when the principal site of pity-and-fear and the character
bearing the main anagnorisis are different, the dialect has no
primitive naming the pathos-centre at the ArMythos level (the probe
proposed `ArMythos.pathos_character_ref_id`). This encoding presses the
question HARDER than Malfi, and the pressure is carried here under
*semantic stretch* — exactly as Malfi carried its four arc-peripeteiai
before sketch-06's A19 gave them a home:

  * **Arc-hero / anagnorisis-bearer = Vindice.** `anagnorisis_character_
    ref_id="ar_vindice"`; his self-undoing recognition lands at
    E_antonio_condemns_vindice (τ_s=21).

  * **Pathos-centre = Gloriana** (ar_gloriana). The dialect can author
    her as an ArCharacter but has NO field to mark her as the mythos's
    pathos-centre. The claim therefore lives in prose (her annotation +
    the action_summary + OQ_MALFI_3_FINDING) — the stretch the probe
    should surface.

  * **Two twists that make this a denser second site than Malfi.**
    (1) Gloriana is *dead before the play and present only as a
    skull-prop* — so a hypothetical `pathos_character_ref_id` would
    point at a non-agentive figure, pressuring whether the field admits
    a dead/absent referent. (2) The pathos is *distributed* — Gloriana,
    Antonio's wife, and Castiza form a parallel pity-cluster (carried,
    before sketch-07, by the now-retired AR_PATHOS_CLUSTER_PARALLEL),
    pressuring whether a single ref id even suffices — answered by A22's
    tuple shape. Malfi's pathos-bearer (the Duchess) was a single
    living agent; Webster's avenger was at least pitiable; Middleton's
    avenger (Vindice) is morally corroded and hard to pity, so the
    pathos has nowhere to go but the violated women.

**Secondary pressures (banked / confirmed):**

- **S6P-OQ1 (main-level anagnorisis_qualifier) — possibly FORCED.**
  Vindice's main recognition is *belated and self-destroying* — he
  recognises his own undoing in the instant it is sealed ("'Tis time to
  die when we are our own foes"). A20 types qualifiers on chain steps
  only; the main `anagnorisis_event_id` has no qualifier slot. Sketch-06
  banked S6P-OQ1 (a main-level qualifier) UNFORCED. Vindice's
  self-destroying main recognition is the second-site forcing candidate.
  See S6P_OQ1_FINDING.

- **A20 `anti` generalisation — CONFIRMED on a second encoding.** The
  Duke's dying recognition (he recognises his killer and his wife's
  adultery as the poison takes him, too late to act) is authored as a
  chain step with `anagnorisis_qualifier="anti"` — the corpus's second
  anti-anagnorisis after Webster's Antonio, confirming A20 generalises.

- **BINDING_ADJACENT — a lightly-covered corpus cell.** Vindice's
  peripeteia (the confession, τ_s=20) and anagnorisis (the
  condemnation, τ_s=21) are one τ_s apart — `peripeteia_anagnorisis_
  binding="adjacent"`, distance 1, the corpus's narrowest. Oedipus /
  Hamlet / Lear / Malfi were SEPARATED; Macbeth COINCIDENT; ADJACENT
  was uncovered until now.

- **OQ-MALFI-4 (instrument-reversal) — NOT re-pressured.** Vindice is a
  self-directed avenger, not a wielded instrument, so the Malfi
  instrument-reversal shape does not recur. (The Lussurioso-wields-
  "Piato" relation is the inverse — the secret avenger lets himself be
  wielded — but it is not authored as an instrumental A13 relation to
  keep the OQ-MALFI-3 signal clean.)

Story content only; no dialect logic. Parallels
`malfi_aristotelian.py` in shape.
"""

from __future__ import annotations

from story_engine.core.aristotelian import (
    ArAnagnorisisStep,
    ArAudienceKnowledgeConstraint,
    ArCharacter,
    ArCharacterArcRelation,
    ArCoPresenceRequirement,
    ArMythos,
    ArPhase,
    ARC_RELATION_PARALLEL,
    BINDING_ADJACENT,
    BINDING_PREF_NEAR,
    DIRECTIONALITY_SYMMETRIC,
    PACING_EVEN,
    PACING_RAPID_ESCALATION,
    PHASE_BEGINNING,
    PHASE_END,
    PHASE_MIDDLE,
    PLOT_COMPLEX,
    QUALIFIER_ANTI,
    STEP_KIND_PARALLEL,
    TONAL_REGISTER_TRAGIC_WITH_IRONY,
)


# ============================================================================
# Phases — A2 (three logical divisions)
# ============================================================================

PH_BEGINNING = ArPhase(
    id="ph_revengers_beginning",
    role=PHASE_BEGINNING,
    scope_event_ids=(
        # Pre-play (3): the originating poison + the two lineages
        "E_gloriana_poisoned",
        "E_court_lineage",
        "E_vindice_family",
        # Act I (7): the skull, the Piato plan, the rape + trial, the
        # hiring, the suicide, the house of mourning
        "E_vindice_skull_soliloquy",
        "E_hippolito_brings_commission",
        "E_junior_rapes_antonio_wife",
        "E_junior_trial",
        "E_vindice_hired_as_piato",
        "E_antonio_wife_suicide",
        "E_antonio_displays_corpse",
    ),
    min_event_count=8,
    max_event_count=12,
    # The beginning lays the two wounds (Gloriana's poisoning, Antonio's
    # wife's rape) and engages the revenge engine; it moves with
    # Middleton's brisk, accumulating-business rhythm rather than rapid
    # escalation or slow burn.
    pacing_preference=PACING_EVEN,
    annotation=(
        "Antecedent wounds + the revenge engaged. Pre-play: the Duke "
        "poisons Gloriana nine years before for refusing his lust "
        "(E_gloriana_poisoned) — the pathos-centre established dead, a "
        "skull. The court's corruption (E_court_lineage) and Vindice's "
        "reduced house (E_vindice_family) frame the discontent. Act I: "
        "Vindice with the skull resolves on revenge and takes the "
        "'Piato' disguise to enter Lussurioso's service; the Duchess's "
        "youngest son rapes Antonio's wife and the Duke declines to "
        "punish him; Antonio's wife kills herself and the discontented "
        "lords swear revenge over her corpse — the living pathos beat "
        "beside Gloriana's pre-play one."
    ),
)

PH_MIDDLE = ArPhase(
    id="ph_revengers_middle",
    role=PHASE_MIDDLE,
    scope_event_ids=(
        # Act II (5): the corruption-test, the false report, the bedroom
        # trap, the warrant + secret release
        "E_vindice_tests_castiza",
        "E_gratiana_yields",
        "E_vindice_false_report_to_lussurioso",
        "E_bedroom_misdirection",
        "E_duke_warrant_and_secret_release",
        # Act III (5): the execution mix-up + the central revenge
        "E_brothers_rush_warrant",
        "E_junior_executed_by_mistake",
        "E_duke_lured_to_lodge",
        "E_duke_killed_by_skull",
        "E_brothers_realize_junior_dead",
    ),
    min_event_count=8,
    max_event_count=12,
    # The middle is the play's engine of recoiling plots — the bedroom
    # misdirection, the warrant that kills the wrong brother, the
    # skull-kiss. Even pacing of escalating reversals.
    pacing_preference=PACING_EVEN,
    annotation=(
        "Plots that recoil on their authors. The corruption-test "
        "bifurcates (Castiza holds; Gratiana falls). The bedroom "
        "misdirection lands Lussurioso in treason; the Duke's secret "
        "release turns the brothers' execution-warrant onto their own "
        "youngest (E_junior_executed_by_mistake). At the phase's centre "
        "is the play's titular deed: the Duke kisses Gloriana's poisoned "
        "skull in the dark and is stabbed, made to watch his Duchess's "
        "adultery as he dies (E_duke_killed_by_skull) — the central "
        "revenge, and the Duke's anti-recognition."
    ),
)

PH_END = ArPhase(
    id="ph_revengers_end",
    role=PHASE_END,
    scope_event_ids=(
        # Act IV (4): Piato condemned, Vindice hired undisguised, the
        # corpse-swap, Gratiana's repentance
        "E_lussurioso_orders_piato_killed",
        "E_vindice_hired_as_himself",
        "E_corpse_dressed_as_piato",
        "E_gratiana_repents",
        # Act V (7): the body found, the masque, the mutual slaughter,
        # the confession, the condemnation, the execution
        "E_duke_death_discovered",
        "E_revengers_plan_masque",
        "E_lussurioso_killed_at_masque",
        "E_second_masque_mutual_slaughter",
        "E_vindice_confesses",
        "E_antonio_condemns_vindice",
        "E_vindice_executed",
    ),
    min_event_count=9,
    max_event_count=13,
    # Act V compresses to a single masque-night of slaughter and the
    # avenger's self-betrayal — rapid escalation to the confession that
    # springs the trap on Vindice himself.
    pacing_preference=PACING_RAPID_ESCALATION,
    annotation=(
        "The avenger undone by his own appetite. The grim joke at the "
        "structural centre: Lussurioso hires the undisguised Vindice to "
        "murder 'Piato' — Vindice contracted to kill his own alias. The "
        "Duke's corpse is dressed as Piato to mask the murder; Gratiana "
        "repents. Act V: Lussurioso proclaimed Duke, then killed at the "
        "coronation masque while the second masque-party slaughters "
        "itself for the empty throne. Antonio is made Duke; Vindice, "
        "unable to keep silent about so fine a piece of work, boasts to "
        "him that he killed the old Duke — and is condemned in the same "
        "breath. **The peripeteia** (the confession recoiling, τ_s=20) "
        "and **the main anagnorisis** ('Tis time to die when we are our "
        "own foes', τ_s=21) fall one beat apart."
    ),
)

AR_REVENGERS_PHASES = (PH_BEGINNING, PH_MIDDLE, PH_END)


# ============================================================================
# Characters — A5
# ============================================================================
#
# Seven ArCharacter records. ONE tragic hero — Vindice. The rest serve
# the pathos cluster (Gloriana, Antonio's wife, Castiza), the parallel
# companion (Hippolito), and the revenge's targets (the Duke,
# Lussurioso). The single-tragic-hero shape is the corpus's lean case
# (Malfi had three) and is correct for the play: Vindice owns the only
# hamartia-with-deliberation arc; everyone else is pity-object,
# instrument, or target.

AR_VINDICE = ArCharacter(
    id="ar_vindice",
    name="Vindice",
    character_ref_id="vindice",
    hamartia_text=(
        "Revenge curdling into an appetite for killing that outlives "
        "its justice. Vindice's cause is real — the Duke poisoned his "
        "betrothed Gloriana nine years before for refusing his lust — "
        "and his first revenge (the poisoned-skull murder of the Duke) "
        "is the play's centre of moral gravity. But the hamartia is "
        "not the revenge; it is the *relish*. He cannot stop at "
        "justice: he tests his own sister's chastity, contracts to "
        "murder his own alias, and stages the masque-slaughter with a "
        "craftsman's pride. The error of judgement that destroys him is "
        "the final boast — exhilarated by his success, he cannot keep "
        "silent and confesses the Duke's murder to the newly-made Duke "
        "Antonio, who condemns him on the instant. The recognition is "
        "self-undoing: 'Tis time to die when we are our own foes.' He "
        "recognises, too late, that his own nature — the appetite the "
        "revenge fed — is the foe that kills him. Webster's Duchess "
        "dies without recognition (anagnorisis_absent); Middleton's "
        "Vindice dies *of* his recognition, in the same breath that "
        "seals it."
    ),
    is_tragic_hero=True,
)

# --- The pathos cluster — the play's pity-and-fear, distributed across
#     three violated women, none of whom is the arc-hero. The OQ-MALFI-3
#     forcing lives here: the dialect can author them as ArCharacters
#     but cannot mark any of them as the mythos's pathos-centre.

AR_GLORIANA = ArCharacter(
    id="ar_gloriana",
    name="Gloriana",
    character_ref_id="gloriana",
    hamartia_text=None,
    # is_tragic_hero=False — Gloriana has no arc, no hamartia, no
    # recognition. She is dead before the play and present only as a
    # skull. She is the play's PATHOS-CENTRE — the emblem of its grief,
    # the motive of its revenge, and (dressed and poisoned) the
    # instrument of its central murder. The dialect has no field to mark
    # this role: anagnorisis_character_ref_id names the recognizer
    # (Vindice), and there is no pathos_character_ref_id. The claim that
    # Gloriana is the pathos-centre lives only in this annotation, the
    # action_summary, and OQ_MALFI_3_FINDING. **This absence IS the
    # OQ-MALFI-3 forcing, pressed harder than Malfi: the pathos-centre
    # here is not merely distinct from the recognizer but is a dead,
    # non-agentive, prop-borne figure.**
    is_tragic_hero=False,
    # A23 (sketch-07) — the pathos-carrier flag, landed. Gloriana is the
    # mythos's pathos-centre (named in AR_REVENGERS_MYTHOS.pathos_
    # character_ref_ids). The arc-less, non-agentive pity-object the
    # field was designed to admit.
    pathos_carrier=True,
)

AR_ANTONIO_WIFE = ArCharacter(
    id="ar_antonio_wife",
    name="Antonio's wife",
    character_ref_id="antonio_wife",
    hamartia_text=None,
    # The living pathos beat — raped by the Duchess's youngest son, she
    # takes her own life when the court refuses justice (the "house of
    # mourning"). Part of the distributed pathos cluster; is_tragic_hero
    # =False (she has no deliberative arc — she is wronged and dies).
    is_tragic_hero=False,
    # A23 (sketch-07) — pathos-carrier. The living pity-object beside
    # Gloriana; the second member of the mythos's distributed pathos-
    # centre (pathos_character_ref_ids).
    pathos_carrier=True,
)

AR_CASTIZA = ArCharacter(
    id="ar_castiza",
    name="Castiza",
    character_ref_id="castiza",
    hamartia_text=None,
    # Vindice's chaste sister, subjected to his own corruption-test. The
    # threatened-but-unfallen member of the pathos cluster: where
    # Gloriana is destroyed and Antonio's wife violated, Castiza holds —
    # the pathos of endangered innocence. is_tragic_hero=False.
    is_tragic_hero=False,
)

# --- The parallel companion and the revenge's targets.

AR_HIPPOLITO = ArCharacter(
    id="ar_hippolito",
    name="Hippolito",
    character_ref_id="hippolito",
    hamartia_text=None,
    # Vindice's brother and instrument-in-revenge; he acts beside
    # Vindice through every killing and is condemned and executed beside
    # him. is_tragic_hero=False — his arc is the loyal-companion's, with
    # no independent hamartia or recognition (Vindice does the
    # recognizing for both). Authored for AR_VINDICE_HIPPOLITO_PARALLEL.
    is_tragic_hero=False,
)

AR_DUKE = ArCharacter(
    id="ar_duke",
    name="the Duke",
    character_ref_id="duke",
    hamartia_text=None,
    # The originating villain — Gloriana's poisoner, the lust that
    # starts the play. is_tragic_hero=False (he is the revenge's first
    # target, not a tragic hero). Authored for the anti-recognition
    # chain step at his death (AR_STEP_DUKE_DYING_RECOGNITION).
    is_tragic_hero=False,
)

AR_LUSSURIOSO = ArCharacter(
    id="ar_lussurioso",
    name="Lussurioso",
    character_ref_id="lussurioso",
    hamartia_text=None,
    # The Duke's lustful heir, the revenge's second great target, killed
    # at the masque. is_tragic_hero=False. Authored for hamartia-
    # participation grounding and the revenge structure.
    is_tragic_hero=False,
)

AR_REVENGERS_CHARACTERS = (
    AR_VINDICE,
    AR_GLORIANA, AR_ANTONIO_WIFE, AR_CASTIZA,
    AR_HIPPOLITO, AR_DUKE, AR_LUSSURIOSO,
)


# ============================================================================
# Character-arc relations — A13
# ============================================================================
#
# Two canonical kind="parallel" relations, both symmetric, polarity
# empty. No instrumental relations: Vindice is a self-directed avenger,
# not a wielded instrument (so OQ-MALFI-4 / OQ-MALFI-1 do not recur).

AR_VINDICE_HIPPOLITO_PARALLEL = ArCharacterArcRelation(
    id="arc_vindice_hippolito_parallel",
    kind=ARC_RELATION_PARALLEL,
    character_ref_ids=("ar_vindice", "ar_hippolito"),
    mythos_id="ar_revengers",
    over_event_ids=(
        "E_duke_killed_by_skull",        # the central revenge, done together
        "E_lussurioso_killed_at_masque",  # the masque slaughter
        "E_vindice_confesses",            # the boast that damns both
        "E_antonio_condemns_vindice",     # condemned together
        "E_vindice_executed",             # executed together
    ),
    annotation=(
        "The avenger brothers. Hippolito introduces Vindice to the "
        "court, stands at every killing, and is condemned and executed "
        "beside him. Their arcs run in strict parallel — but it is "
        "Vindice who carries the hamartia and the recognition; Hippolito "
        "is the loyal instrument who shares the deed and the death "
        "without the deliberation. Symmetric, canonical kind; polarity "
        "empty."
    ),
    directionality=DIRECTIONALITY_SYMMETRIC,
)

# NOTE (sketch-07): the distributed pathos-centre was previously carried
# here by an `AR_PATHOS_CLUSTER_PARALLEL` ArCharacterArcRelation grouping
# Gloriana + Antonio's wife — a **semantic stretch**, since that record
# types relations between arc-bearing agents' *arcs*, and these two pity-
# objects have no arcs. The Session-5 probe flagged exactly this ("forced
# to overload ArCharacterArcRelation as a workaround") and proposed the
# mythos-level pathos field. Sketch-07 lands A22 `pathos_character_ref_ids`
# as that field, so the relation is RETIRED: the pathos-centre claim now
# lives in its proper home (AR_REVENGERS_MYTHOS.pathos_character_ref_ids
# + per-character pathos_carrier flags), not in an overloaded arc-relation.
# This is the honest de-stretch — the relation existed only to give the
# pathos-centre structural footing, and A22 is that footing.

AR_REVENGERS_CHARACTER_ARC_RELATIONS = (
    AR_VINDICE_HIPPOLITO_PARALLEL,
)


# ============================================================================
# Anagnorisis chain — A11 / A14 / A20
# ============================================================================
#
# One step: the Duke's dying recognition. A genuine supplementary
# recognition that is *anti* — real but too late to alter outcome —
# the corpus's second anti-anagnorisis after Webster's Antonio,
# confirming A20 (sketch-06) generalises to a second encoding.

AR_STEP_DUKE_DYING_RECOGNITION = ArAnagnorisisStep(
    id="arstep_duke_dying_recognition",
    event_id="E_duke_killed_by_skull",
    character_ref_id="ar_duke",
    step_kind=STEP_KIND_PARALLEL,
    precipitates_main=False,
    anagnorisis_qualifier=QUALIFIER_ANTI,    # A20 — corpus's 2nd anti
    annotation=(
        "The Duke kisses Gloriana's poisoned skull in the dark and, as "
        "the venom takes his lips, Vindice and Hippolito reveal "
        "themselves and name Gloriana — and force the dying Duke to "
        "watch his Duchess embrace his bastard Spurio. In one beat the "
        "Duke recognises both who kills him (and why, nine years on) "
        "and his wife's adultery. The recognition is *anti*-anagnorisic: "
        "real, complete, and wholly too late — the poison is already "
        "mortal; nothing he now knows can be acted on. Different "
        "character from the main recognizer (ar_duke vs ar_vindice), "
        "non-precipitating, parallel. The corpus's second anti-"
        "anagnorisis after Webster's Antonio (τ_s=30 in Malfi); A20's "
        "`anagnorisis_qualifier='anti'` carries it, confirming the "
        "sketch-06 value generalises to a second encoding and a second "
        "shape (a villain's too-late recognition, where Antonio's was a "
        "victim's)."
    ),
)

AR_REVENGERS_ANAGNORISIS_CHAIN = (
    AR_STEP_DUKE_DYING_RECOGNITION,
)


# ============================================================================
# Co-presence requirements — A15-SE2 (sketch-04)
# ============================================================================

AR_REVENGERS_CO_PRESENCE = (
    ArCoPresenceRequirement(
        id="copres_vindice_lussurioso_middle",
        character_ref_ids=("ar_vindice", "ar_lussurioso"),
        phase_id="ph_revengers_beginning",
        # E_vindice_hired_as_piato (τ_s=3) — the procurement commission,
        # the relation the whole disguise-plot rests on.
        min_count=1,
    ),
    ArCoPresenceRequirement(
        id="copres_vindice_duke_middle",
        character_ref_ids=("ar_vindice", "ar_duke"),
        phase_id="ph_revengers_middle",
        # E_duke_lured_to_lodge (τ_s=11) + E_duke_killed_by_skull
        # (τ_s=12) — the trap and the central revenge.
        min_count=2,
    ),
)


# ============================================================================
# Audience-knowledge constraints — A15-SE3 (sketch-04)
# ============================================================================

AR_REVENGERS_AUDIENCE_KNOWLEDGE = (
    ArAudienceKnowledgeConstraint(
        id="auk_piato_is_vindice",
        subject="Piato is Vindice in disguise",
        # The audience must hold the Piato=Vindice identity from the
        # hiring scene onward; the dramatic irony of Acts I-IV (and the
        # grim joke of Vindice hired to kill 'Piato') depends on the
        # audience knowing what Lussurioso never learns.
        latest_τ_s=3,
        source_event_id="E_vindice_hired_as_piato",
    ),
    ArAudienceKnowledgeConstraint(
        id="auk_skull_is_gloriana",
        subject="the dressed lady at the lodge is Gloriana's poisoned skull",
        # The audience must know the skull's identity before the Duke
        # kisses it, for the central murder to land as revenge rather
        # than accident.
        latest_τ_s=12,
        source_event_id="E_duke_lured_to_lodge",
    ),
)


# ============================================================================
# Mythos — A1
# ============================================================================

AR_REVENGERS_MYTHOS = ArMythos(
    id="ar_revengers",
    title="The Revenger's Tragedy",
    action_summary=(
        "Nine years before the play, the Duke poisons Gloriana, "
        "Vindice's betrothed, for refusing his lust; Vindice has kept "
        "her skull ever since. **Gloriana — dead, a skull, the emblem "
        "of the play's grief — is its pathos-centre** (named, with "
        "Antonio's wife, in pathos_character_ref_ids). When the corrupt "
        "court "
        "needs a procurer, Vindice takes the disguise of 'Piato' to "
        "enter Lussurioso's service and avenge himself. Around him the "
        "court rots: the Duchess's youngest son rapes Antonio's wife "
        "(who kills herself) and goes unpunished; the Duchess takes the "
        "Duke's bastard Spurio as her lover. As Piato, Vindice tests "
        "his own sister Castiza (who holds) and mother Gratiana (who "
        "falls, then repents); misdirects Lussurioso into treason; and "
        "watches the Duchess's elder sons engineer, by a warrant the "
        "Duke has secretly countermanded, the execution of their own "
        "youngest brother. The central revenge: Vindice dresses "
        "Gloriana's poisoned skull as a lady and the Duke, kissing it "
        "in the dark, is poisoned and stabbed, made to watch his wife's "
        "adultery as he dies — **his anti-recognition**. Lussurioso, "
        "now Duke, unknowingly hires the undisguised Vindice to murder "
        "'Piato'; the Duke's corpse is dressed in Piato's clothes. At "
        "the coronation masque Vindice and Hippolito kill Lussurioso "
        "and his favourites, while a second masque-party slaughters "
        "itself for the empty throne. Antonio, the last honest lord, is "
        "made Duke. Then Vindice, exhilarated and unable to keep "
        "silent, boasts to Antonio that he killed the old Duke — and "
        "Antonio condemns him and Hippolito to instant execution. "
        "**The peripeteia** is the confession recoiling on its author; "
        "**the main anagnorisis** follows one beat later — 'Tis time to "
        "die when we are our own foes' — Vindice recognising, too late, "
        "that the appetite his revenge fed is the foe that kills him. "
        "The revenger's tragedy: the instrument of justice destroyed by "
        "the same hunger that drove it."
    ),
    central_event_ids=(
        # Beginning (10)
        "E_gloriana_poisoned",
        "E_court_lineage",
        "E_vindice_family",
        "E_vindice_skull_soliloquy",
        "E_hippolito_brings_commission",
        "E_junior_rapes_antonio_wife",
        "E_junior_trial",
        "E_vindice_hired_as_piato",
        "E_antonio_wife_suicide",
        "E_antonio_displays_corpse",
        # Middle (10)
        "E_vindice_tests_castiza",
        "E_gratiana_yields",
        "E_vindice_false_report_to_lussurioso",
        "E_bedroom_misdirection",
        "E_duke_warrant_and_secret_release",
        "E_brothers_rush_warrant",
        "E_junior_executed_by_mistake",
        "E_duke_lured_to_lodge",
        "E_duke_killed_by_skull",
        "E_brothers_realize_junior_dead",
        # End (11)
        "E_lussurioso_orders_piato_killed",
        "E_vindice_hired_as_himself",
        "E_corpse_dressed_as_piato",
        "E_gratiana_repents",
        "E_duke_death_discovered",
        "E_revengers_plan_masque",
        "E_lussurioso_killed_at_masque",
        "E_second_masque_mutual_slaughter",
        "E_vindice_confesses",
        "E_antonio_condemns_vindice",
        "E_vindice_executed",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=AR_REVENGERS_PHASES,
    # Complication (desis): the revenger enters the court in disguise.
    complication_event_id="E_vindice_hired_as_piato",
    # Denouement (lusis): the central revenge, after which everything
    # unravels toward the masque and the confession.
    denouement_event_id="E_duke_killed_by_skull",
    # Peripeteia: the confession recoils on its author — Vindice's boast,
    # meant as triumph, produces his condemnation. The reversal of HIS
    # fortune (distinct from the central revenge, which is the revenge's
    # success, not the tragic hero's reversal).
    peripeteia_event_id="E_vindice_confesses",
    # Anagnorisis: Vindice's self-undoing recognition, one beat later.
    anagnorisis_event_id="E_antonio_condemns_vindice",
    # A14 — Vindice is the recognizer.
    anagnorisis_character_ref_id="ar_vindice",
    # Unity of action — TRUE. The Duchess's-sons subplot feeds the main
    # action (the rape motivates the nobles; the execution mix-up is the
    # court's self-consumption that clears Vindice's path) rather than
    # running as a separable second plot. More unified than Lear (which
    # asserts False).
    asserts_unity_of_action=True,
    characters=AR_REVENGERS_CHARACTERS,
    # A11 / A20 — one anti-recognition chain step (the Duke's death).
    anagnorisis_chain=AR_REVENGERS_ANAGNORISIS_CHAIN,
    # A12 — ADJACENT. Peripeteia (confession, τ_s=20) and anagnorisis
    # (condemnation, τ_s=21) are one τ_s apart — the corpus's narrowest
    # binding, and the first use of the ADJACENT cell (Oedipus/Hamlet/
    # Lear/Malfi SEPARATED; Macbeth COINCIDENT).
    peripeteia_anagnorisis_binding=BINDING_ADJACENT,
    # A15-SE2 / A15-SE3 — hard structural constraints.
    co_presence_requirements=AR_REVENGERS_CO_PRESENCE,
    audience_knowledge_constraints=AR_REVENGERS_AUDIENCE_KNOWLEDGE,
    # A16-SP1 — Middleton's savage black comedy: the skull-kiss, the
    # 'Piato hired to kill Piato' joke, the masque of murderers. Colder
    # and more grotesque than Hamlet's reflexive irony, but the same
    # canonical register.
    tonal_register=TONAL_REGISTER_TRAGIC_WITH_IRONY,
    # A16-SP2 — NEAR. The actual A12 distance is 1, the corpus narrowest.
    binding_distance_preference=BINDING_PREF_NEAR,
    # A19 (sketch-06) — empty. The Revenger's Tragedy has a SINGLE tragic
    # arc (Vindice); the other reversals (the Duke's, Lussurioso's, the
    # brothers') are villain falls, not tragic-hero arc-peripeteiai. So
    # OQ-LEAR-4 / A19 is not re-pressured here — the encoding's pressure
    # is OQ-MALFI-3 (pathos/arc split), not multiplicity of tragic arcs.
    secondary_peripeteia_event_ids=(),
    # A22 (sketch-07) — the pathos-centre, now with a typed home. The
    # play's pity-and-fear is carried by two arc-less pity-objects, NOT
    # by the morally-corroded avenger (Vindice, the tragic hero and
    # recognizer). This is OQ-MALFI-3 landed: the pathos-centre is split
    # off from BOTH the tragic hero and the recognizer, and is borne by
    # characters with no arcs — Gloriana (dead before the play, present
    # only as a skull) and Antonio's wife (raped, driven to suicide).
    # Castiza is deliberately excluded: the Session-5 probe read her as
    # arc-bearing (resistance + vindication), not a pure pity-object, and
    # proposed exactly this two-member list. The claim that previously
    # lived in annotations + an overloaded parallel relation now lives
    # here. See OQ_MALFI_3_FINDING (CLOSED).
    pathos_character_ref_ids=("ar_gloriana", "ar_antonio_wife"),
)


# ============================================================================
# Open-question findings — prose constants for probe-side consumption
# ============================================================================

OQ_MALFI_3_FINDING = (
    "OQ-MALFI-3 — Pathos-hero vs arc-hero split. **Cross-encoding "
    "pressure now CONFIRMED, and pressed harder than the surfacing "
    "site.** The Malfi Session-6 re-probe surfaced this as the strongest "
    "new finding: when the principal site of pity-and-fear (Webster's "
    "Duchess) and the character bearing the main anagnorisis (Ferdinand) "
    "differ, the dialect has no primitive naming the pathos-centre at "
    "the ArMythos level. The probe proposed "
    "`ArMythos.pathos_character_ref_id`. The Revenger's Tragedy is the "
    "second-site encoding and presses the question on THREE axes Malfi "
    "did not:\n\n"
    "1. **Sharper split.** Webster's Duchess is at least pitiable AND "
    "   the title character; Middleton's avenger (Vindice) is morally "
    "   corroded and hard to pity, so the pathos has nowhere to live "
    "   but the violated women — the split is total, not partial.\n"
    "2. **Non-agentive pathos-centre.** The emblematic pathos-bearer, "
    "   Gloriana (ar_gloriana), is dead before the play and present "
    "   only as a skull-prop. A hypothetical `pathos_character_ref_id` "
    "   would point at a figure with no arc, no agency, no presence but "
    "   a memento. Pressures whether the field admits a dead / absent / "
    "   prop-borne referent.\n"
    "3. **Distributed pathos-centre.** The pity is shared across a "
    "   parallel cluster — Gloriana, Antonio's wife, Castiza "
    "   (AR_PATHOS_CLUSTER_PARALLEL). A single `pathos_character_ref_id` "
    "   could not capture the cluster; pressures whether the field "
    "   wants to be a tuple, or whether a distinct apparatus is "
    "   needed.\n\n"
    "**Carried under semantic stretch in this encoding** (the OQ-LEAR-4 "
    "/ A19 pattern before sketch-06): the pathos-centre claim lives in "
    "ar_gloriana's annotation, the action_summary, and a kind='parallel' "
    "ArCharacterArcRelation (AR_PATHOS_CLUSTER_PARALLEL) that is itself "
    "a stretch — it types relations between *arcs*, but Gloriana and "
    "Antonio's wife have no arcs. The right home is a mythos-level "
    "pathos field.\n\n"
    "Candidate canonical extensions, in order of structural fit:\n\n"
    "1. **`ArMythos.pathos_character_ref_ids: Tuple[str, ...]`** (a "
    "   tuple, not a single ref — admitting the distributed cluster). "
    "   Names the character(s) bearing the principal pity-and-fear when "
    "   distinct from `anagnorisis_character_ref_id`. Admits dead / "
    "   non-agentive referents (the ArCharacter need not have an arc). "
    "   **Recommended.** The probe (Session 5 of this arc) will test "
    "   whether the reader-model proposes the singular or the tuple "
    "   shape.\n"
    "2. **`ArMythos.pathos_character_ref_id: Optional[str]`** (singular, "
    "   per the probe's original Malfi proposal). Cleaner but cannot "
    "   carry the Webster-plus-Middleton distributed case.\n"
    "3. **A pathos-role flag on ArCharacter** (`is_pathos_centre: "
    "   bool`). Distributes the claim onto the characters rather than "
    "   the mythos; admits multiplicity naturally but loses the "
    "   single-locus mythos-level reading.\n\n"
    "Recommendation: sketch-07 should land option 1 (the tuple), with "
    "Malfi migrating `(ar_duchess,)` and the Revenger's migrating "
    "`(ar_gloriana, ar_antonio_wife)`.\n\n"
    "**CONFIRMED — Session-5 probe (this arc).** The pathos-centre gap "
    "was the ONLY vocabulary strain in an otherwise fully-clean read "
    "(read_on_terms=yes, drift empty, 7/8 approved, 0 rejected). The "
    "probe independently proposed BOTH the encoding's recommended "
    "shapes: (1) `ArMythos.pathos_character_ref_ids` — explicitly a "
    "LIST/tuple 'naming characters or objects that carry the play's "
    "pity-and-fear without possessing arcs of their own (Gloriana's "
    "skull, Antonio's wife)', and orthogonal to ArCharacterArcRelation; "
    "(2) `ArCharacter.pathos_carrier: bool`. It recognised all three "
    "forcing axes — non-agentive ('Gloriana as skull… pity-objects "
    "without arcs'), distributed ('spread across multiple non-agent "
    "characters'), and the stretch itself ('forced to overload "
    "ArCharacterArcRelation as a workaround') — and grounded the gap in "
    "Aristotle's own pathos (Poetics 1452b: 'a structural-field gap, "
    "not a vocabulary failure'). The probe's pathos field listed only "
    "Gloriana and Antonio's wife, NOT Castiza; in the same run it "
    "flagged (one needs-work) that grouping Castiza with the arc-less "
    "pity-objects was imprecise, since Castiza holds under the "
    "corruption-test and so has a minimal arc. The encoding's cluster "
    "relation was narrowed to `(ar_gloriana, ar_antonio_wife)` "
    "accordingly. OQ-MALFI-3 is now cross-encoding CONFIRMED with a "
    "probe-proposed shape; sketch-07 is its home.\n\n"
    "**CLOSED — sketch-07 (2026-06-17).** Landed exactly as recommended: "
    "A22 `ArMythos.pathos_character_ref_ids` (the tuple, option 1) + A23 "
    "`ArCharacter.pathos_carrier` (the probe's companion flag), with the "
    "A7.19 concordance check. This encoding migrated to "
    "`pathos_character_ref_ids=('ar_gloriana', 'ar_antonio_wife')` with "
    "`pathos_carrier=True` on both; the overloaded "
    "AR_PATHOS_CLUSTER_PARALLEL relation is RETIRED (the stretch is gone, "
    "not merely re-annotated). Malfi migrated `(ar_duchess,)`. All three "
    "forcing axes are now expressible in one voice: the total split "
    "(pathos-centre disjoint from the tragic-hero set), the non-agentive "
    "referent (A22 imposes no arc requirement — Gloriana the skull is a "
    "valid referent), and the distribution (the tuple carries two). "
    "Verified by the Session-7 re-probe (see aristotelian-sketch-07.md).\n\n"
    "Artifact: reader_model_revengers_aristotelian_output.json (Session 5, "
    "forcing); reader_model_revengers_aristotelian_session7_output.json "
    "(Session 7, closure)."
)

S6P_OQ1_FINDING = (
    "S6P-OQ1 — Main-level anagnorisis_qualifier. **Banked UNFORCED by "
    "sketch-06; this encoding is the second-site forcing candidate.** "
    "A20 (sketch-06) types `anagnorisis_qualifier ∈ {'', 'genuine', "
    "'anti', 'partial'}` on `ArAnagnorisisStep` — i.e. on supplementary "
    "chain recognitions only. The MAIN recognition "
    "(`ArMythos.anagnorisis_event_id`) has no qualifier slot; sketch-06 "
    "banked S6P-OQ1 (a main-level qualifier) but noted no corpus site "
    "forced it (every corpus main anagnorisis was genuine).\n\n"
    "Vindice's main anagnorisis is the forcing candidate. His "
    "recognition — 'Tis time to die when we are our own foes' — is "
    "*belated and self-destroying*: it arrives in the instant his "
    "confession seals his death, with no possibility of acting on it. "
    "It is not cleanly 'genuine' (it is a recognition-too-late, an "
    "`anti`/`partial`-shaped main recognition) but the dialect can only "
    "qualify chain steps. To type Vindice's main recognition as anti, "
    "the encoding would have to demote it to a chain step — losing its "
    "status as THE main anagnorisis.\n\n"
    "Candidate canonical extension: **`ArMythos.main_anagnorisis_"
    "qualifier: str`** (same closed enum as A20).\n\n"
    "**NOT FORCED — Session-5 probe (this arc); prediction falsified.** "
    "The probe read Vindice's main anagnorisis as clean and correct "
    "('anagnorisis (Vindice's self-recognition as his own foe) … "
    "correctly deployed'); it did NOT surface a main-level qualifier as "
    "a gap. The expectation that Vindice's belated, self-destroying "
    "recognition would force S6P-OQ1 was the encoding's hypothesis, and "
    "the probe data did not bear it out — the reader was content to "
    "read the main recognition as genuine-with-tragic-timing rather "
    "than as needing an anti/partial qualifier. The design-first → "
    "probe-falsifies rhythm operating at the OQ-prediction layer (cf. "
    "sketch-06's S6P-OQ1/OQ2, also predicted and unforced). S6P-OQ1 "
    "stays BANKED UNFORCED; a different forcing site is needed (a "
    "tragedy whose MAIN recognition is unambiguously anti — the avenger "
    "who recognises the wrong target as he kills, say). Artifact: "
    "reader_model_revengers_aristotelian_output.json."
)

# Tuple export for probe-side consumption. The Revenger's Tragedy's
# primary contribution is OQ-MALFI-3 (cross-encoding confirmation); its
# secondary contribution is the S6P-OQ1 forcing candidate. A20's `anti`
# generalisation (the Duke's dying recognition) is a closure-confirmation
# data point, not a new finding, so it is documented on the chain step
# rather than as a finding constant.
OQ_FINDINGS = (
    ("OQ_MALFI_3", OQ_MALFI_3_FINDING),
    ("S6P_OQ1",    S6P_OQ1_FINDING),
)
