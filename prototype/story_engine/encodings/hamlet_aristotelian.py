"""
hamlet_aristotelian.py — *Hamlet* encoded under the Aristotelian
dialect (aristotelian-sketch-01 A1–A9 + sketch-02 A10–A12).

Fourth Aristotelian encoding after Oedipus (single mythos, complex
plot, separated peripeteia/anagnorisis at distance 5), Rashomon
(four-mythos contest, no anagnorisis), and Macbeth (single mythos,
coincident binding, non-precipitating staggered step). Substrate
layer lives in `prototype/story_engine/encodings/hamlet.py`; this
file references event ids by string only.

Hamlet is the forcing case for two research forcing functions banked
from `aristotelian-probe-sketch-03`:

- **OQ-AP5 — ArFateAgent / ArProphecyStructure.** Hamlet's Ghost has
  a causal posture distinct from Macbeth's Witches: direct factual
  revelation (Claudius poisoned the king, method named) + commission
  to act (revenge demand), where the Witches offered equivocating
  prophecy. A second fate-agent encoding with a *different* causal
  posture is the forcing case sketch-03 banked. Finding: the Ghost's
  role is structurally invisible at the Aristotelian layer — carried
  entirely at substrate (`apparition_of` + `ghost_claims_killed_by`
  + `ghost_demands_revenge`). See `OQ_AP5_FINDING` below.

- **OQ-AP6 — Intra-mythos parallel tragic-heroes.** Hamlet authors
  three `ArCharacter`s with `is_tragic_hero=True` (Hamlet, Claudius,
  Laertes) within one mythos. A10's `ArMythosRelation(kind="parallel")`
  types *inter*-mythos today; Hamlet forces the question of whether
  intra-mythos parallelism needs its own structural hook. Finding:
  the dialect admits the multiplicity (three booleans flip True) but
  has no structural way to say "these three are parallel WITHIN one
  mythos." See `OQ_AP6_FINDING` below.

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

- **A11 anagnorisis chain: one non-precipitating step.** Claudius at
  `E_claudius_prays` (τ_s=7) — his private recognition of moral
  bankruptcy ("May one be pardon'd and retain th'offence?"). Parallels
  Lady Macbeth's sleepwalking structurally: character-level,
  precipitates_main=False (his recognition does not causally drive
  Hamlet's τ_s=17 recognition — Hamlet observes Claudius praying but
  does not act, and the later reveal comes from Laertes, not
  Claudius). Macbeth's non-precipitating step lands at a different
  hero's collapse; Hamlet's lands at the antagonist's collapse —
  the same structural field (non-precipitating chain step) with a
  different character-role occupant.

- **A11 forcing function for same-event staggered recognition.**
  Laertes's deathbed recognition of his own pawn-status is
  substrate-compressed into `E_laertes_reveals_plot` (τ_s=17), the
  same event as Hamlet's main anagnorisis. A11 invariant 3 forbids
  a chain step at the main event; Laertes is therefore NOT authored
  as a chain step. Recorded as `OQ_AP8_FINDING` — the dialect
  cannot currently express "staggered recognitions that land at the
  same substrate beat."

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

Running:
    cd prototype
    python3 -c "
    from story_engine.encodings.hamlet import FABULA
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    from story_engine.core.aristotelian import verify
    observations = verify(AR_HAMLET_MYTHOS, substrate_events=FABULA)
    print(f'{len(observations)} observation(s)')
    for o in observations:
        print(f'  [{o.severity}] {o.code}: {o.message}')
    "
"""

from __future__ import annotations

from story_engine.core.aristotelian import (
    ArAnagnorisisStep,
    ArCharacter,
    ArMythos,
    ArPhase,
    BINDING_SEPARATED,
    PHASE_BEGINNING,
    PHASE_END,
    PHASE_MIDDLE,
    PLOT_COMPLEX,
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
# Anagnorisis chain — A11 (sketch-02)
# ============================================================================
#
# One step: Claudius at the prayer scene (τ_s=7), non-precipitating.
# Structurally parallels Lady Macbeth's sleepwalking (Macbeth) —
# same non-precipitating-chain-step field, different occupant role
# (antagonist, not parallel protagonist). Macbeth's chain step
# stages the *protagonist's wife's* private recognition of guilt;
# Hamlet's stages the *antagonist's* private recognition of
# inability-to-repent.
#
# Laertes's deathbed recognition IS at the same substrate beat as
# Hamlet's main anagnorisis (both at E_laertes_reveals_plot, τ_s=17).
# A11 invariant 3 forbids a chain step at the main event; Laertes
# is therefore NOT authored as a chain step here. The forcing
# function is recorded in OQ_AP8_FINDING below — the dialect cannot
# currently express "staggered recognitions that land at the same
# substrate beat." Laertes's parallel-hero status is carried by his
# ArCharacter record (is_tragic_hero=True); the structural
# recognition-relation to Hamlet's main anagnorisis is invisible
# at this dialect layer.

AR_STEP_CLAUDIUS_PRAYS = ArAnagnorisisStep(
    id="arstep_claudius_prays",
    event_id="E_claudius_prays",
    character_ref_id="ar_claudius",
    precipitates_main=False,
    annotation=(
        "Claudius's prayer scene — 'O, my offence is rank, it smells "
        "to heaven.' He names his crime (the 'primal eldest curse, / "
        "A brother's murder') and recognizes he cannot truly repent "
        "while retaining its gains ('Of those effects for which I "
        "did the murder, / My crown, mine own ambition, and my "
        "queen'). This is his character-level anagnorisis: "
        "recognition of moral bankruptcy. precipitates_main=False: "
        "the scene does not causally drive Hamlet's τ_s=17 "
        "recognition — Hamlet enters behind Claudius but declines to "
        "kill him at prayer (misreading the scene as true confession "
        "rather than failed confession), and the later anagnorisis "
        "comes through Laertes's deathbed reveal, not through any "
        "channel from Claudius. Parallel collapse, not causal "
        "pressure — same structural role as Lady Macbeth's "
        "sleepwalking in Macbeth, with antagonist rather than "
        "parallel-protagonist as occupant."
    ),
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
    # A11 — Claudius's prayer-scene recognition as non-precipitating
    # staggered step. Parallels Macbeth's Lady-Macbeth-sleepwalking
    # step in shape; differs in occupant (antagonist, not parallel
    # protagonist).
    anagnorisis_chain=(AR_STEP_CLAUDIUS_PRAYS,),
    # A12 — SEPARATED with distance 9. Exercises the widest end of
    # the separated category.
    peripeteia_anagnorisis_binding=BINDING_SEPARATED,
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
    "OQ-AP5 — ArFateAgent / ArProphecyStructure. Pressure confirmed. "
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
    "{prophecy, revelation, commission} would let the Ghost's role "
    "be named at dialect scope. Sketch-04 candidate."
)

OQ_AP6_FINDING = (
    "OQ-AP6 — Intra-mythos parallel tragic-heroes. Pressure "
    "confirmed. Three `ArCharacter` records author `is_tragic_hero="
    "True`: Hamlet, Claudius, Laertes. The dialect admits the "
    "multiplicity but has no structural way to declare 'these three "
    "are in parallel WITHIN one mythos.' Workaround attempts that "
    "do not work: (1) authoring three ArMythos records and an "
    "ArMythosRelation(kind='parallel') treats them as three "
    "different arrangements of the action, which is wrong — they are "
    "three characters within one arrangement. (2) The "
    "`anagnorisis_chain` expresses staggered recognitions, which is "
    "a thinner relation than parallel tragic-hero-ship. (3) "
    "`hamartia_text` on each character describes the parallelism in "
    "prose, which works for the walker's review but puts the "
    "structural relation below the verify surface. Candidate "
    "dialect extension: a typed `ArParallelHeroes` record naming "
    "≥2 ArCharacter ids (or a `parallel_to` field on ArCharacter "
    "itself) with a 'kind' vocabulary {mirror, foil, doubled-fall}. "
    "Mirror: Hamlet-Laertes (both sons avenging fathers). Foil: "
    "Hamlet-Claudius (will to act vs. will to retain). Doubled-fall: "
    "all three dying in the same beat. Sketch-04 candidate."
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
