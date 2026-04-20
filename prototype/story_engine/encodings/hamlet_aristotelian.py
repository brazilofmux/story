"""
hamlet_aristotelian.py — *Hamlet* encoded under the Aristotelian
dialect (aristotelian-sketch-01 A1–A9 + sketch-02 A10–A12 +
sketch-03 A13–A14).

Fourth Aristotelian encoding after Oedipus (single mythos, complex
plot, separated peripeteia/anagnorisis at distance 5), Rashomon
(four-mythos contest, no anagnorisis), and Macbeth (single mythos,
coincident binding, non-precipitating staggered step). Substrate
layer lives in `prototype/story_engine/encodings/hamlet.py`; this
file references event ids by string only.

Sketch-03 migration (2026-04-20): A13 `ArCharacterArcRelation` and
A14 `step_kind` land as closures to two Hamlet-probe-surfaced
forcing functions. The encoding now authors two `ArCharacterArcRelation`
records (mirror Hamlet-Laertes + foil Hamlet-Claudius) expressing the
three-way tragic-hero parallelism structurally, and the anagnorisis
chain expands from one step to three: two same-character staging
steps (Ghost commission, Mousetrap verification) plus the existing
parallel-antagonist step (Claudius at prayer). OQ-AP5 formally
retires on two-negative-probe grounds; see `OQ_AP5_FINDING` prose.

Hamlet is the forcing case for two research forcing functions banked
from `aristotelian-probe-sketch-03`, both closed by sketch-03:

- **OQ-AP5 — ArFateAgent / ArProphecyStructure. RETIRED.** Hamlet's
  Ghost has a causal posture distinct from Macbeth's Witches: direct
  factual revelation (Claudius poisoned the king, method named) +
  commission to act (revenge demand), where the Witches offered
  equivocating prophecy. A second fate-agent encoding with a
  *different* causal posture was the forcing case probe-sketch-03
  banked. Both the Macbeth probe (2026-04-19) and the Hamlet probe
  (2026-04-20) read the fate-agent structurally without demanding a
  typed dialect record; sketch-03 formally retires OQ-AP5 on
  two-negative-probe grounds. The fate-agent function is recorded as
  correctly substrate-only. See `OQ_AP5_FINDING` below (prose
  preserved + retirement note appended).

- **OQ-AP6 — Intra-mythos parallel tragic-heroes. CLOSED.** Hamlet
  authors three `ArCharacter`s with `is_tragic_hero=True` (Hamlet,
  Claudius, Laertes) within one mythos. Sketch-03 A13
  `ArCharacterArcRelation` types the parallelism structurally:
  `AR_HAMLET_LAERTES_MIRROR` (both sons avenging murdered fathers via
  opposite tempers) and `AR_HAMLET_CLAUDIUS_FOIL` (will-to-act vs.
  will-to-retain) are authored below as pairwise decompositions of
  the three-way parallelism. Laertes-Claudius has no structural pair
  authored — the probe's language was pairwise ("between Hamlet's and
  Laertes's revenge paths"), and three-way single relations are
  deferred per sketch-03 OQ7. The dialect now has a structural hook
  for "these characters are in parallel WITHIN one mythos."

Sketch-02 axis exercise:

- **A12 exercises BINDING_SEPARATED with distance 9.** Hamlet's
  peripeteia fires at `E_hamlet_kills_polonius` (τ_s=8) — the reversal
  from avenger-with-clean-hands to fugitive-who-has-killed-the-wrong-
  man; his anagnorisis lands at `E_laertes_reveals_plot` (τ_s=17) —
  the deathbed recognition that Claudius's counter-plot has reached
  him and he is doomed. Distance 9. Oedipus's separated binding is
  distance 5; Hamlet's stretches separated across the entire middle
  phase — the play's famous "delay" rendered structurally. This is
  the widest-separation encoding in the corpus. The bound setting
  stays at the default of 3 (any distance > 3 is SEPARATED); the
  observation is that "separated" is one category over a wide
  numerical range. Whether a further dialect axis ("near-separated"
  vs "distant-separated") is warranted is a probe-surface question;
  recorded as `OQ_AP7_FINDING` for future probes.

- **A11 + A14 anagnorisis chain: three steps across two step_kinds.**
  Sketch-03 expands the chain from one step to three. Two same-
  character staging steps (A14 `step_kind="staging"`, precipitating
  by definition) stage Hamlet's own epistemic progression:
  `AR_STEP_HAMLET_GHOST_CLAIM` at `E_hamlet_meets_ghost` (τ_s=1,
  provisional revelation — held but not yet acted on) and
  `AR_STEP_HAMLET_MOUSETRAP` at `E_mousetrap_performance` (τ_s=6,
  the Ghost's claim promoted to verified certainty). The existing
  parallel step (A14 `step_kind="parallel"`) is retained:
  `AR_STEP_CLAUDIUS_PRAYS` at `E_claudius_prays` (τ_s=7) — Claudius's
  private recognition of moral bankruptcy, different character,
  non-precipitating. Together: Hamlet's three-stage coming-to-know
  (staging × 2) plus the antagonist's parallel-character recognition,
  orthogonal axes both carried by A14's step_kind vocabulary.

- **A11 forcing function for same-event staggered recognition.**
  Laertes's deathbed recognition of his own pawn-status is
  substrate-compressed into `E_laertes_reveals_plot` (τ_s=17), the
  same event as Hamlet's main anagnorisis. A11 invariant 3 forbids
  a chain step at the main event; Laertes is therefore NOT authored
  as a chain step. Recorded as `OQ_AP8_FINDING` — the dialect
  cannot currently express "staggered recognitions that land at the
  same substrate beat." Stays banked under sketch-03 (probe did not
  pressure relaxation).

Unities. Unity of action: asserts=True (single tragic action, from
Ghost's commission through Hamlet's revenge-and-death). Unity of
time: asserts=False (τ_s span is 118 units from Claudius-brother-of-
king at -100 through Hamlet's death at 18 — same choice as Oedipus
and Macbeth). Unity of place: asserts=False — the action spans
Elsinore's ramparts, great hall, closet, graveyard, and (briefly)
England.

Catharsis. aims_at_catharsis=True per the dialect's default. The
play's end-phase pathos is scattered across four deaths at τ_s=17–18
(Gertrude, Laertes, Claudius, Hamlet), distinct from Macbeth's
scattered-across-three-phases pattern and from Oedipus's
concentrated-at-end pattern. If OQ-AP1 (ArPathos + catharsis
grounding) opens in a future sketch, Hamlet is the candidate
forcing encoding for "cluster-pathos": four deaths in one beat with
different moral weights (innocent, redeemed-antagonist, regicide-
villain, tragic-hero) strains any uniform pathos record.

No ArMythosRelation authored. Hamlet is single-mythos; no Rashomon-
style contest; no frame narrative. `AR_HAMLET_MYTHOS` stands alone.
Sketch-03 authors two A13 `ArCharacterArcRelation` records (see
`AR_HAMLET_CHARACTER_ARC_RELATIONS`) — intra-mythos, not inter-mythos.

Running:
    cd prototype
    python3 -c "
    from story_engine.encodings.hamlet import FABULA
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS, AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    from story_engine.core.aristotelian import verify
    observations = verify(
        AR_HAMLET_MYTHOS,
        substrate_events=FABULA,
        mythoi=(AR_HAMLET_MYTHOS,),
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    print(f'{len(observations)} observation(s)')
    for o in observations:
        print(f'  [{o.severity}] {o.code}: {o.message}')
    "
"""

from __future__ import annotations

from story_engine.core.aristotelian import (
    ArAnagnorisisStep,
    ArCharacter,
    ArCharacterArcRelation,
    ArMythos,
    ArPhase,
    ARC_RELATION_FOIL,
    ARC_RELATION_MIRROR,
    BINDING_SEPARATED,
    PHASE_BEGINNING,
    PHASE_END,
    PHASE_MIDDLE,
    PLOT_COMPLEX,
    STEP_KIND_PARALLEL,
    STEP_KIND_STAGING,
)


# ============================================================================
# Phases — A2 (three logical divisions)
# ============================================================================

PH_BEGINNING = ArPhase(
    id="ph_hamlet_beginning",
    role=PHASE_BEGINNING,
    scope_event_ids=(
        "E_king_hamlet_reigns",
        "E_claudius_brother_of_king",
        "E_polonius_family_standing",
        "E_king_hamlet_poisoned",
        "E_claudius_crowned",
        "E_claudius_marries_gertrude",
        "E_ghost_seen_by_watch",
        "E_horatio_tells_hamlet",
        "E_hamlet_meets_ghost",
        "E_hamlet_sworn_to_secrecy",
        "E_hamlet_adopts_antic_disposition",
        "E_polonius_theory",
        "E_players_arrive",
    ),
    annotation=(
        "Antecedent conditions, the secret crime, and the Ghost's "
        "commission that makes it actionable. The five pre-play world "
        "facts (king_hamlet's reign, Claudius's kinship, Polonius's "
        "family, the poisoning, Claudius's coronation-and-marriage) "
        "supply the terrain; the Ghost's revelation at τ_s=1 converts "
        "private crime into commissioned revenge; Hamlet's adoption of "
        "the antic disposition and the players' arrival set up the "
        "means of verification. The beginning closes at τ_s=5, with "
        "Hamlet planning the Mousetrap — the moment where the "
        "verifying action is about to fire."
    ),
)

PH_MIDDLE = ArPhase(
    id="ph_hamlet_middle",
    role=PHASE_MIDDLE,
    scope_event_ids=(
        "E_mousetrap_performance",
        "E_claudius_prays",
        "E_polonius_hides_arras",
        "E_hamlet_confronts_gertrude",
        "E_hamlet_kills_polonius",
        "E_ghost_in_closet",
        "E_hamlet_sent_to_england",
        "E_ophelia_madness",
        "E_ophelia_drowns",
        "E_laertes_returns",
        "E_duel_plotted",
    ),
    annotation=(
        "The binding. The Mousetrap (τ_s=6) verifies the Ghost's "
        "claim — Hamlet's held-belief about Claudius's crime "
        "promotes from BELIEVED to KNOWN. The prayer scene (τ_s=7) "
        "is Hamlet's missed opportunity and Claudius's private "
        "recognition of his own bankruptcy. The peripeteia fires in "
        "the closet scene: Hamlet stabs through the arras at what he "
        "thinks is Claudius and kills Polonius instead (τ_s=8). From "
        "that reversal the binding tightens automatically — exile to "
        "England (τ_s=9), Ophelia's madness and drowning (τ_s=10–11), "
        "Laertes's return demanding vengeance (τ_s=12), and the duel "
        "plotted with its doubled poison (τ_s=13). `E_duel_plotted` "
        "closes the middle — every element of the catastrophe is now "
        "set in motion."
    ),
)

PH_END = ArPhase(
    id="ph_hamlet_end",
    role=PHASE_END,
    scope_event_ids=(
        "E_graveyard_scene",
        "E_duel_begins",
        "E_gertrude_drinks_poison",
        "E_hamlet_laertes_wounded",
        "E_laertes_reveals_plot",
        "E_hamlet_kills_claudius",
        "E_laertes_dies",
        "E_hamlet_dies",
    ),
    annotation=(
        "The unbinding. The graveyard scene (τ_s=14) is the "
        "meditative threshold — Hamlet contemplates Yorick's skull "
        "and Ophelia's funeral, then moves forward to the duel. "
        "Gertrude's poisoning (τ_s=16) is the first crack in "
        "Claudius's plot; Hamlet-Laertes's exchange-wound (τ_s=16) "
        "commits them both. Laertes's deathbed revelation (τ_s=17) "
        "IS the anagnorisis — Hamlet recognizes the full plot, the "
        "poisons doubled, Claudius as architect. The recognition "
        "and the revenge are same-event: Hamlet kills Claudius with "
        "blade and cup (τ_s=17), discharging the Ghost's commission. "
        "Laertes dies, then Hamlet (τ_s=18) in Horatio's arms. Four "
        "deaths clustered at the catastrophe — pity for Hamlet's "
        "belated recognition, fear at the machinery that delayed it "
        "so long the recognition and the death could not be "
        "separated."
    ),
)


# ============================================================================
# Characters — A5
# ============================================================================
#
# Three tragic-heroes (is_tragic_hero=True), all participating in
# central events. This multiplicity is the forcing case for OQ-AP6
# (intra-mythos parallel-hero relation): the dialect admits three
# booleans set True but has no structural hook for "these three
# stand in parallel within one mythos." See OQ_AP6_FINDING below.

AR_HAMLET = ArCharacter(
    id="ar_hamlet",
    name="Hamlet",
    character_ref_id="hamlet",
    hamartia_text=(
        "The delay. Hamlet demands perfect certainty (he stages the "
        "Mousetrap before trusting the Ghost) and perfect occasion "
        "(he passes up the chance to kill Claudius at prayer, "
        "reasoning that death-in-prayer would send him to heaven), "
        "and his demand for perfection of the vengeance-moment lets "
        "opportunities pass until the moment finds him instead. His "
        "hamartia is not inaction — he kills Polonius rashly, ships "
        "Rosencrantz and Guildenstern to their deaths, kills Laertes "
        "and Claudius in the final scene — but an error of "
        "calibration: he acts on the wrong occasions and hesitates on "
        "the right ones. 'Thus conscience does make cowards of us "
        "all' is Hamlet's own diagnosis; Aristotle's sense of "
        "'missing the mark' (not moral failure but erroneous "
        "judgment) fits."
    ),
    is_tragic_hero=True,
)

AR_CLAUDIUS = ArCharacter(
    id="ar_claudius",
    name="Claudius",
    character_ref_id="claudius",
    hamartia_text=(
        "Self-deception about the stability of a crime gained by "
        "murder. 'May one be pardon'd and retain th'offence?' — "
        "Claudius in prayer recognizes he cannot repent while "
        "keeping the crown and queen the crime bought him, but "
        "neither does he renounce them. His hamartia is believing "
        "the crime can be paid for without undoing the gain; his "
        "strategic response to Hamlet's Mousetrap (exile, then the "
        "duel plot with doubled poison) is a man who knows he's been "
        "exposed and still tries to manage the exposure rather than "
        "confess it. Classically the antagonist; structurally a "
        "second tragic-hero whose fall is as complete as the "
        "protagonist's. Unlike Oedipus, no moment of public "
        "recognition — Claudius dies still holding the crown."
    ),
    is_tragic_hero=True,
)

AR_LAERTES = ArCharacter(
    id="ar_laertes",
    name="Laertes",
    character_ref_id="laertes",
    hamartia_text=(
        "Grief weaponized by the wrong framer. Laertes returns from "
        "France with just cause (father killed, sister drowned) and "
        "righteous will; Claudius redirects that grief into the "
        "poisoned-rapier plot in a few scenes. Laertes's hamartia is "
        "the credulity that accepts Claudius's narrative without "
        "verification — he takes at face value what Hamlet in the "
        "parallel situation spent an entire act stage-managing a "
        "play to test. His deathbed recognition ('the king — the "
        "king's to blame') IS his anagnorisis and IS his reveal to "
        "Hamlet, collapsed into a single substrate beat. The parallel "
        "with Hamlet — both sons avenging murdered fathers — is the "
        "play's explicit structural mirror: 'by the image of my "
        "cause, I see / the portraiture of his'."
    ),
    is_tragic_hero=True,
)


# ============================================================================
# Anagnorisis chain — A11 (sketch-02) + A14 (sketch-03)
# ============================================================================
#
# Three steps across two step_kinds:
#
# 1. AR_STEP_HAMLET_GHOST_CLAIM (step_kind="staging", τ_s=1). Hamlet's
#    first epistemic waypoint: the Ghost's direct revelation, held
#    provisionally pending verification.
# 2. AR_STEP_HAMLET_MOUSETRAP (step_kind="staging", τ_s=6). Hamlet's
#    second epistemic waypoint: the Mousetrap converts the Ghost's
#    claim from tentative to verified.
# 3. AR_STEP_CLAUDIUS_PRAYS (step_kind="parallel", τ_s=7). Claudius's
#    private recognition of moral bankruptcy — different character,
#    non-precipitating, parallels Lady Macbeth's sleepwalking step
#    in Macbeth with a different occupant role (antagonist, not
#    parallel protagonist).
#
# Main anagnorisis lands at E_laertes_reveals_plot (τ_s=17) on
# Hamlet himself; AR_HAMLET_MYTHOS names anagnorisis_character_ref_id=
# "ar_hamlet" (A14) so the staging steps verify same-character-as-
# main against it.
#
# Laertes's deathbed recognition IS at the same substrate beat as
# Hamlet's main anagnorisis (both at E_laertes_reveals_plot, τ_s=17).
# A11 invariant 3 forbids a chain step at the main event; Laertes
# is therefore NOT authored as a chain step here. The forcing
# function is recorded in OQ_AP8_FINDING below — the dialect cannot
# currently express "staggered recognitions that land at the same
# substrate beat." Laertes's parallel-hero status is carried by his
# ArCharacter record (is_tragic_hero=True) and by the
# AR_HAMLET_LAERTES_MIRROR relation authored below; the structural
# recognition-relation to Hamlet's main anagnorisis is invisible at
# this dialect layer.

AR_STEP_HAMLET_GHOST_CLAIM = ArAnagnorisisStep(
    id="arstep_hamlet_ghost_claim",
    event_id="E_hamlet_meets_ghost",
    character_ref_id="ar_hamlet",
    step_kind=STEP_KIND_STAGING,
    precipitates_main=True,
    annotation=(
        "Hamlet's first epistemic waypoint: the Ghost's direct "
        "revelation of Claudius's guilt. Not the recognition — Hamlet "
        "holds it provisionally ('The spirit that I have seen / May "
        "be the devil'), does not yet act on it, requires "
        "corroboration via the Mousetrap. Structurally: the "
        "commission grounds the action (without it, Hamlet has no "
        "cause for revenge), but the knowledge stays tentative until "
        "verified. First of three staging steps culminating in the "
        "main anagnorisis at E_laertes_reveals_plot (τ_s=17); the "
        "distance from here (τ_s=1) to there (16 substrate steps) is "
        "the structural weight of the famous Hamlet delay."
    ),
)

AR_STEP_HAMLET_MOUSETRAP = ArAnagnorisisStep(
    id="arstep_hamlet_mousetrap",
    event_id="E_mousetrap_performance",
    character_ref_id="ar_hamlet",
    step_kind=STEP_KIND_STAGING,
    precipitates_main=True,
    annotation=(
        "Hamlet's second epistemic waypoint: the Mousetrap "
        "performance converts the Ghost's claim from tentative-"
        "revelation to verified-certainty. 'I'll take the ghost's "
        "word for a thousand pound' (III.ii). The Ghost's "
        "commission-revelation at τ_s=1 held as BELIEVED; Claudius's "
        "flinching exit from the play-within-the-play at τ_s=6 "
        "promotes the belief to KNOWN. Second staging step; narrows "
        "the remaining epistemic gap to the structural shape of "
        "Claudius's counter-response (the sealed execution orders, "
        "the exile to England, the duel plot) which Hamlet does not "
        "yet understand is a counter-plot in motion. Precedes the "
        "main anagnorisis at τ_s=17 by 11 τ_s-steps."
    ),
)

AR_STEP_CLAUDIUS_PRAYS = ArAnagnorisisStep(
    id="arstep_claudius_prays",
    event_id="E_claudius_prays",
    character_ref_id="ar_claudius",
    step_kind=STEP_KIND_PARALLEL,
    precipitates_main=False,
    annotation=(
        "Claudius's prayer scene — 'O, my offence is rank, it smells "
        "to heaven.' He names his crime (the 'primal eldest curse, / "
        "A brother's murder') and recognizes he cannot truly repent "
        "while retaining its gains ('Of those effects for which I "
        "did the murder, / My crown, mine own ambition, and my "
        "queen'). This is his character-level anagnorisis: "
        "recognition of moral bankruptcy. step_kind='parallel' "
        "(different character from main): the scene does not causally "
        "drive Hamlet's τ_s=17 recognition — Hamlet enters behind "
        "Claudius but declines to kill him at prayer (misreading the "
        "scene as true confession rather than failed confession), and "
        "the later anagnorisis comes through Laertes's deathbed "
        "reveal, not through any channel from Claudius. Parallel "
        "collapse, not causal pressure — same structural role as "
        "Lady Macbeth's sleepwalking in Macbeth, with antagonist "
        "rather than parallel-protagonist as occupant."
    ),
)


# ============================================================================
# Character-arc relations — A13 (sketch-03)
# ============================================================================
#
# Two pairwise ArCharacterArcRelation records express Hamlet's
# three-way tragic-hero parallelism. A third Laertes-Claudius
# relation is NOT authored — the structural content is the pawn/
# puppeteer dynamic, which is handled at substrate-level (via
# Claudius redirecting Laertes's grief) and in hamartia_text prose;
# the probe's language was pairwise, and a three-way single relation
# would lose the mirror-vs-foil distinction. See sketch-03 OQ7 for
# the three-way-relation deferral.

AR_HAMLET_LAERTES_MIRROR = ArCharacterArcRelation(
    id="arc_hamlet_laertes_mirror",
    kind=ARC_RELATION_MIRROR,
    character_ref_ids=("ar_hamlet", "ar_laertes"),
    mythos_id="ar_hamlet",
    over_event_ids=(
        "E_hamlet_meets_ghost",       # (Ghost's commission —
        #                               Hamlet's revenge ground)
        "E_hamlet_kills_polonius",    # (Laertes's father, Hamlet's
        #                               deed — the mirror's trigger)
        "E_ophelia_drowns",
        "E_laertes_returns",
        "E_duel_plotted",
        "E_duel_begins",
        "E_hamlet_laertes_wounded",
        "E_laertes_reveals_plot",
        "E_laertes_dies",
        "E_hamlet_dies",
    ),
    annotation=(
        "Hamlet and Laertes mirror each other as sons avenging "
        "murdered fathers. The structural inversion: Hamlet's revenge "
        "proceeds via delay, verification, and internal dialogue "
        "with moral scruple; Laertes's proceeds via immediate return "
        "and immediate commitment to violent action. Both fathers "
        "killed by Claudius's agency (King Hamlet directly; Polonius "
        "indirectly via the arras-stabbing Claudius provoked Hamlet "
        "toward). Both sons die at the end having accomplished the "
        "revenge; Laertes recognizes his pawn-status in the same "
        "beat that reveals the shape of Claudius's plot to Hamlet. "
        "The mirror is not decorative — it is what makes the duel-"
        "plot work dramatically, and it is what the play's catharsis "
        "depends on. Structural parallelism of this weight belongs "
        "at dialect scope; hamartia_text prose alone cannot render "
        "it to the walker. Laertes's own line names it: 'by the "
        "image of my cause, I see / the portraiture of his.'"
    ),
)

AR_HAMLET_CLAUDIUS_FOIL = ArCharacterArcRelation(
    id="arc_hamlet_claudius_foil",
    kind=ARC_RELATION_FOIL,
    character_ref_ids=("ar_hamlet", "ar_claudius"),
    mythos_id="ar_hamlet",
    over_event_ids=(
        "E_king_hamlet_poisoned",
        "E_claudius_crowned",
        "E_mousetrap_performance",
        "E_claudius_prays",
        "E_hamlet_kills_claudius",
    ),
    annotation=(
        "Hamlet and Claudius are structurally opposed tragic heroes: "
        "Hamlet's hamartia is failure-of-action (scruple, delay, "
        "'enterprise of great pith and moment / lose the name of "
        "action'); Claudius's is failure-of-renunciation (will to "
        "retain the crime's gains while knowing the moral cost — "
        "'may one be pardon'd and retain th'offence?'). Each "
        "recognizes the other's failure in the moment of their own "
        "catastrophe: Claudius's prayer-scene names the scourge he "
        "has earned; Hamlet's final killing of Claudius is the act "
        "his hamartia delayed throughout. Foil, not mirror: the "
        "structural shape is opposition, not symmetry. The two sons "
        "(Hamlet, Laertes) mirror; the revenger and the criminal "
        "(Hamlet, Claudius) foil; the criminal and the pawn "
        "(Claudius, Laertes) is a pawn/puppeteer dynamic carried at "
        "substrate not at dialect scope."
    ),
)

AR_HAMLET_CHARACTER_ARC_RELATIONS = (
    AR_HAMLET_LAERTES_MIRROR,
    AR_HAMLET_CLAUDIUS_FOIL,
)


# ============================================================================
# Mythos — A1
# ============================================================================

AR_HAMLET_MYTHOS = ArMythos(
    id="ar_hamlet",
    title="Hamlet",
    action_summary=(
        "Denmark under the shadow of a secret murder. King Hamlet's "
        "brother Claudius, having poisoned the king two months before "
        "the action opens, has married the queen and taken the "
        "throne, bypassing Prince Hamlet. The Ghost of the murdered "
        "king reveals the crime to Hamlet and commands him to "
        "revenge — direct factual revelation rather than equivocating "
        "prophecy. Hamlet doubts (the spirit 'may be the devil') and "
        "stages a play that reenacts the murder; Claudius's panicked "
        "exit verifies the Ghost's claim. Hamlet passes up the "
        "chance to kill Claudius at prayer (fearing heaven for him) "
        "and in the subsequent closet scene stabs through the arras "
        "at what he thinks is Claudius, killing Polonius instead — "
        "the peripeteia, the reversal from avenger-with-clean-hands "
        "to fugitive. Claudius exiles him to England with sealed "
        "orders for his execution; Hamlet escapes but returns to "
        "find Ophelia drowned and Laertes returned from France "
        "demanding vengeance for his father. Claudius redirects "
        "Laertes's grief into a duel plotted with a poisoned rapier "
        "and a backup poisoned cup. In the duel Gertrude drinks the "
        "cup by accident, Laertes and Hamlet exchange wounds with "
        "the poisoned blade, and Laertes — dying — reveals the "
        "entire plot. Hamlet, himself dying, kills Claudius with "
        "both poisons. The recognition and the revenge are one beat: "
        "Hamlet understands the full shape of his doom only at the "
        "moment he accomplishes the Ghost's commission."
    ),
    central_event_ids=(
        "E_king_hamlet_reigns",
        "E_claudius_brother_of_king",
        "E_polonius_family_standing",
        "E_king_hamlet_poisoned",
        "E_claudius_crowned",
        "E_claudius_marries_gertrude",
        "E_ghost_seen_by_watch",
        "E_horatio_tells_hamlet",
        "E_hamlet_meets_ghost",
        "E_hamlet_sworn_to_secrecy",
        "E_hamlet_adopts_antic_disposition",
        "E_polonius_theory",
        "E_players_arrive",
        "E_mousetrap_performance",
        "E_claudius_prays",
        "E_polonius_hides_arras",
        "E_hamlet_confronts_gertrude",
        "E_hamlet_kills_polonius",
        "E_ghost_in_closet",
        "E_hamlet_sent_to_england",
        "E_ophelia_madness",
        "E_ophelia_drowns",
        "E_laertes_returns",
        "E_duel_plotted",
        "E_graveyard_scene",
        "E_duel_begins",
        "E_gertrude_drinks_poison",
        "E_hamlet_laertes_wounded",
        "E_laertes_reveals_plot",
        "E_hamlet_kills_claudius",
        "E_laertes_dies",
        "E_hamlet_dies",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=(PH_BEGINNING, PH_MIDDLE, PH_END),
    # Complication: first event of middle — the Mousetrap, which
    # converts Hamlet's doubt about the Ghost into verified knowledge
    # and commits him to the revenge path. Parallels Macbeth's
    # E_duncan_killed (first middle event: the regicide commits the
    # action) and Oedipus's E_oedipus_curses_murderer (first middle
    # event: the curse commits the investigation).
    complication_event_id="E_mousetrap_performance",
    # Denouement: last event of middle — the duel plot, where every
    # element of the catastrophe is set in motion (poisoned rapier,
    # backup poisoned cup, Laertes's agreement, scheduled combat).
    # Parallels Macbeth's E_sleepwalking in shape: the last "binding"
    # event before the end phase's unbinding.
    denouement_event_id="E_duel_plotted",
    # A12 — BINDING_SEPARATED with distance 9 (τ_s=8 to τ_s=17).
    # Widest separation in the corpus; Oedipus is distance 5 and
    # Macbeth is COINCIDENT. The "separated" category admits a wide
    # range of τ_s distances at the current bound of 3; the dialect
    # does not today distinguish near-separated from distant-
    # separated. See OQ_AP7_FINDING below.
    #
    # Peripeteia: Hamlet kills Polonius through the arras, thinking
    # it is Claudius. The reversal is from "avenger with moral
    # warrant and opportunity" to "fugitive who has killed the wrong
    # man" — the mistake that makes exile, Laertes's return, and the
    # duel plot inevitable. In strict Aristotelian sense (Poetics
    # 1452a): a change of the situation into the opposite, produced
    # by the hero's own action.
    peripeteia_event_id="E_hamlet_kills_polonius",
    # Anagnorisis: Laertes's deathbed reveal of the full conspiracy.
    # Hamlet recognizes — too late — the shape of Claudius's
    # counter-plot and his own doom within it. This is the tragic
    # recognition that accompanies catastrophe; the earlier Mousetrap
    # verification (τ_s=6) was a narrower epistemic confirmation of
    # the Ghost's specific claim, not the structural recognition A12
    # names.
    anagnorisis_event_id="E_laertes_reveals_plot",
    # Unity of action: asserts=True (A6) — one tragic action from
    # Ghost's commission to Hamlet's death. Unity of time: False
    # (τ_s span 118 from Claudius-brother-of-king at -100 through
    # Hamlet's death at 18). Unity of place: False — Elsinore's
    # ramparts, great hall, closet, graveyard, and England.
    asserts_unity_of_action=True,
    asserts_unity_of_time=False,
    asserts_unity_of_place=False,
    aims_at_catharsis=True,
    characters=(AR_HAMLET, AR_CLAUDIUS, AR_LAERTES),
    # A11 + A14 — three-step chain. Two staging steps stage Hamlet's
    # own coming-to-know (Ghost commission at τ_s=1, Mousetrap
    # verification at τ_s=6), both same-character-as-main and
    # precipitating by A14 definition. One parallel step
    # (Claudius at prayer, τ_s=7) carries the antagonist's non-
    # precipitating private recognition. Chain order matches τ_s
    # order (1 → 6 → 7 → main at 17).
    anagnorisis_chain=(
        AR_STEP_HAMLET_GHOST_CLAIM,
        AR_STEP_HAMLET_MOUSETRAP,
        AR_STEP_CLAUDIUS_PRAYS,
    ),
    # A12 — SEPARATED with distance 9. Exercises the widest end of
    # the separated category.
    peripeteia_anagnorisis_binding=BINDING_SEPARATED,
    # A14 — the character whose recognition lands at
    # anagnorisis_event_id. Required for the staging steps above to
    # verify (A7.11 invariant 2: staging steps' character_ref_id
    # must equal this value).
    anagnorisis_character_ref_id="ar_hamlet",
)


# ============================================================================
# Probe-surface findings — OQ-AP5, OQ-AP6, and two new forcing
# functions surfaced during the encoding (OQ-AP7, OQ-AP8)
# ============================================================================
#
# These are prose constants for reference by future probe runs and
# sketch-04 design. The dialect has no typed record for probe
# findings at encoding scope; these constants carry what the
# encoding surfaced, structured for future extraction.

OQ_AP5_FINDING = (
    "OQ-AP5 — ArFateAgent / ArProphecyStructure. RETIRED by sketch-03 "
    "(2026-04-20) on two-negative-probe grounds. Authorial pressure "
    "below preserved as the cross-session record of what this "
    "encoding surfaced, but the dialect has formally declined to "
    "absorb the fate-agent function: both the Macbeth probe "
    "(probe-sketch-03, 2026-04-19) and the Hamlet live probe "
    "(Session 5, 2026-04-20) read their respective fate-agents "
    "structurally without proposing a typed dialect record. The "
    "sketch-02 forcing-function discipline names 'no probe surfaces "
    "the pressure across two complementary encodings' as the "
    "retirement signal; that is what happened. The fate-agent "
    "function is recorded as correctly substrate-only — an "
    "Aristotelian-dialect observation about substrate-layer causal "
    "mechanics, not a dialect extension.\n\n"
    "Author-pressure (preserved for the record): "
    "The Ghost's causal posture (direct factual revelation + "
    "commission, no equivocation) is structurally invisible at the "
    "Aristotelian layer. Carried entirely at substrate: "
    "`apparition_of(ghost, ramparts)` as observe-only predicate, "
    "`ghost_claims_killed_by(king_hamlet, claudius)` as content "
    "predicate on Hamlet's held set, `ghost_demands_revenge(claudius)` "
    "likewise, `poisoned_in_ear(king_hamlet)` as the specific detail "
    "that drives the Mousetrap's epistemic power. At dialect layer, "
    "Hamlet's ArCharacter hamartia_text mentions the Ghost's "
    "commission in prose but the dialect has no typed field for "
    "'this character's action is commissioned by a fate-agent with "
    "revelation posture'. Contrast Macbeth: the Witches' "
    "equivocating prophecies are also substrate-only, but their "
    "structural function (furnishing the equivocation Macbeth "
    "trusts) is nameable in prose via hamartia_text and was the "
    "only dialect surface sufficient for sketch-01 encoding. "
    "Hamlet's Ghost is further out: its commission is not a hamartia "
    "trigger (Hamlet does not fail by believing the Ghost — the "
    "Ghost tells him the truth) but a structural cause of the action "
    "itself. A typed ArFateAgent with posture ∈ "
    "{prophecy, revelation, commission} would have let the Ghost's "
    "role be named at dialect scope. Two probes, two encodings, no "
    "probe-side pressure: retirement."
)

OQ_AP6_FINDING = (
    "OQ-AP6 — Intra-mythos parallel tragic-heroes. CLOSED by "
    "sketch-03 (2026-04-20). Three `ArCharacter` records author "
    "`is_tragic_hero=True`: Hamlet, Claudius, Laertes. Sketch-03 "
    "A13 `ArCharacterArcRelation` types the parallelism "
    "structurally; the two pairwise relations authored in this "
    "encoding — `AR_HAMLET_LAERTES_MIRROR` (kind='mirror') and "
    "`AR_HAMLET_CLAUDIUS_FOIL` (kind='foil') — realize what this "
    "finding proposed (kinds 'mirror' and 'foil' ship canonical; "
    "'doubled-fall' deferred per sketch-03 OQ8 without corpus "
    "pressure beyond the single Hamlet case). The pairwise "
    "decomposition matches the probe's language ('between Hamlet's "
    "and Laertes's revenge paths') and preserves the mirror-vs-foil "
    "distinction that a three-way single relation would lose; "
    "sketch-03 OQ7 tracks whether a three-way relation with "
    "structurally-distinct-from-pairwise content ever emerges."
)

OQ_AP7_FINDING = (
    "OQ-AP7 — Numerical range of BINDING_SEPARATED. New forcing "
    "function. Hamlet's peripeteia-anagnorisis distance is 9; "
    "Oedipus's is 5. Both are 'separated' under the default bound of "
    "3. The category 'separated' covers 4..∞ — any value from barely-"
    "not-adjacent to arbitrarily-far. Hamlet's 9-step separation is "
    "analytically meaningful (the famous Hamlet delay rendered "
    "structurally) in a way Oedipus's 5-step separation is not — "
    "Oedipus's distance reflects the narrative compression of "
    "messenger-scene-to-reveal, while Hamlet's reflects the "
    "protagonist's hesitation spanning an entire act-and-a-half. A "
    "further distinction — near-separated (4..10) vs distant-"
    "separated (>10) — might be warranted, or the dialect might "
    "want a numerical `peripeteia_anagnorisis_distance` field "
    "surfacing the raw distance alongside the categorical binding. "
    "Probe-surface; may or may not make sketch-04."
)

OQ_AP8_FINDING = (
    "OQ-AP8 — Same-beat staggered recognition. New forcing function. "
    "Laertes's deathbed recognition of his own pawn-status is "
    "structurally an anagnorisis staggered from Hamlet's (Laertes "
    "recognizes first, in order to speak; Hamlet recognizes by "
    "hearing) but substrate-compressed into one event "
    "(E_laertes_reveals_plot, τ_s=17). A11 invariant 3 forbids a "
    "chain step at the main event, so Laertes cannot be authored as "
    "a chain step without either (a) splitting the substrate beat "
    "or (b) relaxing invariant 3. The split-substrate workaround is "
    "possible (add E_laertes_realizes at τ_s=16.5) but feels like "
    "encoding fiction — the recognition and the reveal are genuinely "
    "one action. Relaxing invariant 3 to admit same-event chain "
    "steps would require a new invariant about ordering within the "
    "event (character-subject identity distinguishes the step from "
    "the main, since Laertes's and Hamlet's recognitions at the same "
    "event are distinct recognitions). Probe-surface; candidate for "
    "sketch-04."
)
