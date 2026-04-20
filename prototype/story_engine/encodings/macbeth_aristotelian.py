"""
macbeth_aristotelian.py — *Macbeth* encoded under the Aristotelian
dialect (aristotelian-sketch-01 A1–A9 + sketch-02 A10–A12).

Third Aristotelian encoding after Oedipus (single mythos, complex
plot, separated peripeteia/anagnorisis) and Rashomon (four-mythos
contest, no anagnorisis). Macbeth is the paradigmatic Shakespearean
tragedy — the one Aristotelians most often read forward into after
Oedipus — and its structure pressures sketch-02 at two axes Oedipus +
Rashomon did not:

- **A12 exercises BINDING_COINCIDENT for the first time.** Macbeth's
  peripeteia (the Witches' "none of woman born" apparition's
  equivocation exposed) and anagnorisis (Macbeth's recognition of
  that equivocation) land in the same substrate event —
  `E_macduff_reveals_birth` (τ_s=17). Macduff's Caesarean reveal IS
  the reversal from safety to vulnerability AND the recognition of
  the equivocation, in one beat. Oedipus's separated binding
  (distance 5) and this coincident binding together exercise two of
  the three canonical BINDING values.

- **A11 carries a non-precipitating anagnorisis_chain step.** Lady
  Macbeth's sleepwalking (`E_sleepwalking`, τ_s=13) is a staggered
  character-level recognition of guilt four τ_s-steps before
  Macbeth's — but unlike Jocasta in Oedipus, Lady Macbeth's
  recognition does NOT precipitate Macbeth's. She dies (τ_s=14)
  before the reveal (τ_s=17); her recognition is parallel collapse,
  not causal pressure. `precipitates_main=False` distinguishes the
  two patterns structurally.

Pathos structure (scope observation, not commitment). Macbeth
scatters pathos across three events: `E_macduff_family_killed`
(τ_s=12, innocent victims), `E_lady_macbeth_dies` (τ_s=14,
suicide-implied), `E_macbeth_killed` (τ_s=17, the tyrant's fall).
The dialect has no typed `ArPathos` record today — the events carry
the suffering by their end-phase placement and authorial annotation
only. If a future sketch-03 opens on OQ-AP1 (ArPathos + catharsis
grounding), Macbeth is a candidate forcing encoding: its three
pathos events span two phases and three different victims, making
the implicit-via-end-phase pattern strained.

No ArMythosRelation authored. Macbeth is single-mythos; no Rashomon-
style contest; no frame narrative. `AR_MACBETH_MYTHOS` stands alone.

Substrate layer: `prototype/story_engine/encodings/macbeth.py`.
This file references substrate event ids by string only.

Running:
    cd prototype
    python3 -c "
    from story_engine.encodings.macbeth import FABULA
    from story_engine.encodings.macbeth_aristotelian import (
        AR_MACBETH_MYTHOS,
    )
    from story_engine.core.aristotelian import verify
    observations = verify(AR_MACBETH_MYTHOS, substrate_events=FABULA)
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
    BINDING_COINCIDENT,
    PHASE_BEGINNING,
    PHASE_END,
    PHASE_MIDDLE,
    PLOT_COMPLEX,
)


# ============================================================================
# Phases — A2 (three logical divisions)
# ============================================================================

PH_BEGINNING = ArPhase(
    id="ph_macbeth_beginning",
    role=PHASE_BEGINNING,
    scope_event_ids=(
        "E_macbeth_defends_scotland",
        "E_macbeth_kinsman_of_duncan",
        "E_macbeth_thane_of_glamis",
        "E_duncan_king_of_scotland",
        "E_prophecy_first",
        "E_thane_of_cawdor_awarded",
        "E_letter_to_lady_macbeth",
        "E_duncan_visits",
    ),
    annotation=(
        "Antecedent conditions and the prophecy that activates them. "
        "The four pre-play world facts (valor, kinship, thaneship of "
        "Glamis, Duncan's kingship) establish the terrain on which "
        "ambition can act; the Witches' first prophecy converts "
        "latent possibility into articulated temptation; the Cawdor "
        "award confirms the prophecy's second clause and supplies the "
        "empirical foothold for believing the rest; the letter and "
        "Duncan's visit set the scene for the crime."
    ),
)

PH_MIDDLE = ArPhase(
    id="ph_macbeth_middle",
    role=PHASE_MIDDLE,
    scope_event_ids=(
        "E_duncan_killed",
        "E_duncan_discovered",
        "E_macbeth_crowned",
        "E_banquo_killed",
        "E_banquet_ghost",
        "E_prophecy_second",
        "E_macduff_flees",
        "E_macduff_family_killed",
        "E_sleepwalking",
    ),
    annotation=(
        "The binding — each security-seeking act enlarges the circle "
        "of guilt. Duncan's regicide precipitates the crown; the "
        "crown's insecurity precipitates Banquo's murder; the "
        "banquet-ghost pushes Macbeth back to the Witches, whose "
        "second prophecy supplies equivocating reassurance; Macduff's "
        "flight precipitates the moral nadir at Fife; Lady Macbeth's "
        "sleepwalking marks the private breaking that the end phase "
        "makes mechanical. `E_sleepwalking` closes the middle: the "
        "last 'binding' event, where consequence catches up to the "
        "conspirator who goaded the first crime."
    ),
)

PH_END = ArPhase(
    id="ph_macbeth_end",
    role=PHASE_END,
    scope_event_ids=(
        "E_lady_macbeth_dies",
        "E_birnam_moves",
        "E_macduff_reveals_birth",
        "E_macbeth_killed",
        "E_malcolm_crowned",
    ),
    annotation=(
        "The unbinding. Lady Macbeth's death answers her sleepwalking; "
        "Birnam's movement falsifies the first apparition-reassurance; "
        "Macduff's Caesarean reveal falsifies the second — and here "
        "peripeteia and anagnorisis coincide: reversal into exposure "
        "AND recognition of the equivocation in one beat. Macbeth's "
        "death follows immediately; Malcolm's coronation restores "
        "legitimate succession. Catastrophe and catharsis in the "
        "Aristotelian sense: pity for Macbeth's self-knowledge at "
        "the last, fear at the machinery of ambition that brought "
        "him there."
    ),
)


# ============================================================================
# Characters — A5
# ============================================================================

AR_MACBETH = ArCharacter(
    id="ar_macbeth",
    name="Macbeth",
    character_ref_id="macbeth",
    hamartia_text=(
        "Not simple ambition — Macbeth begins the play already "
        "honored, already thane, already trusted. The hamartia is "
        "his *credulity toward equivocation*: taking the Witches' "
        "'none of woman born' as absolute protection rather than as "
        "the riddle it is. He acts on the prophecies' literal "
        "reading at every step and is destroyed by their hidden "
        "alternative readings. Aristotle's 'missing the mark' fits "
        "precisely: the error is not moral (he knows the regicide is "
        "wrong — 'pity, like a naked new-born babe, / Striding the "
        "blast') but epistemic — he trusts the Witches' language to "
        "mean what it seems to mean."
    ),
    is_tragic_hero=True,
)

AR_LADY_MACBETH = ArCharacter(
    id="ar_lady_macbeth",
    name="Lady Macbeth",
    character_ref_id="lady_macbeth",
    hamartia_text=(
        "Parallel hamartia — the 'unsex me here' confidence that "
        "decisive will can carry what conscience will not. She goads "
        "Macbeth past his hesitation at the regicide; her "
        "sleepwalking four acts later is the conscience she thought "
        "she had exorcised returning as compulsive speech. Her death "
        "at τ_s=14 — suicide strongly implied — closes her arc "
        "before the second-apparition equivocation is exposed. "
        "Unlike Jocasta in Oedipus, her recognition does not "
        "precipitate Macbeth's; they collapse in parallel."
    ),
    is_tragic_hero=True,
)


# ============================================================================
# Anagnorisis chain — A11 (sketch-02)
# ============================================================================
#
# Lady Macbeth realizes at E_sleepwalking (τ_s=13), four substrate
# steps before Macbeth's recognition at E_macduff_reveals_birth
# (τ_s=17). precipitates_main=False: her recognition does not cause
# Macbeth's — she dies (τ_s=14) before Macbeth meets Macduff. This
# distinguishes Macbeth's chain from Oedipus's, where Jocasta's
# recognition (E_jocasta_realizes) actively pressures Oedipus toward
# his through the intervening shepherd's testimony.

AR_STEP_LADY_MACBETH_SLEEPWALKING = ArAnagnorisisStep(
    id="arstep_lady_macbeth_sleepwalking",
    event_id="E_sleepwalking",
    character_ref_id="ar_lady_macbeth",
    precipitates_main=False,
    annotation=(
        "Lady Macbeth's sleepwalking is the eruption of compulsive "
        "confession — the 'out, damned spot' speech. The Doctor and "
        "Gentlewoman overhear; the kingdom gains rumor. This is her "
        "character-level anagnorisis: she recognizes in her own "
        "sleep what her waking self had denied. Its structural "
        "relation to Macbeth's later recognition is adjacency in "
        "time and theme, not causation — she never tells Macbeth, "
        "and dies before the second-apparition equivocation is "
        "exposed. The chain records the staggering; "
        "precipitates_main=False records that the stagger is not "
        "causal."
    ),
)


# ============================================================================
# Mythos — A1
# ============================================================================

AR_MACBETH_MYTHOS = ArMythos(
    id="ar_macbeth",
    title="Macbeth",
    action_summary=(
        "A Scottish war-hero, valor already proved and thaneships "
        "already held, hears three prophecies from the Witches: "
        "thane of Glamis (true), thane of Cawdor (confirmed moments "
        "later), and king hereafter (the temptation). His wife "
        "amplifies the prophecy into plan; he kills his king in his "
        "own house. Each subsequent security-seeking act enlarges "
        "the circle of guilt — Banquo's murder, the Macduff-family "
        "slaughter — and each act tightens the conditions under "
        "which the later apparition-reassurances can still hold. "
        "Lady Macbeth's sleepwalking (τ_s=13) announces the private "
        "collapse; Birnam's movement (τ_s=15) falsifies the first "
        "apparition; at Dunsinane, Macduff's revelation that he was "
        "'from his mother's womb untimely ripp'd' (τ_s=17) "
        "falsifies the second — and there peripeteia and "
        "anagnorisis coincide: the reversal into vulnerability and "
        "the recognition of the equivocation are one beat. "
        "Macbeth's death follows; Malcolm's coronation closes the "
        "arc."
    ),
    central_event_ids=(
        "E_macbeth_defends_scotland",
        "E_macbeth_kinsman_of_duncan",
        "E_macbeth_thane_of_glamis",
        "E_duncan_king_of_scotland",
        "E_prophecy_first",
        "E_thane_of_cawdor_awarded",
        "E_letter_to_lady_macbeth",
        "E_duncan_visits",
        "E_duncan_killed",
        "E_duncan_discovered",
        "E_macbeth_crowned",
        "E_banquo_killed",
        "E_banquet_ghost",
        "E_prophecy_second",
        "E_macduff_flees",
        "E_macduff_family_killed",
        "E_sleepwalking",
        "E_lady_macbeth_dies",
        "E_birnam_moves",
        "E_macduff_reveals_birth",
        "E_macbeth_killed",
        "E_malcolm_crowned",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=(PH_BEGINNING, PH_MIDDLE, PH_END),
    # Complication: first event of middle — the regicide that
    # converts the prophecy's implied path into achieved action.
    complication_event_id="E_duncan_killed",
    # Denouement: last event of middle — Lady Macbeth's sleepwalking
    # marks the turn where the machinery of tyranny starts coming
    # apart from inside; parallels Oedipus's E_shepherd_testimony
    # as the last "binding" event before the end-phase unbinding.
    denouement_event_id="E_sleepwalking",
    # A12 COINCIDENT: peripeteia and anagnorisis at the same event.
    # Macduff's reveal IS both the reversal (protection → exposure)
    # and the recognition (the Witches' equivocation exposed). This
    # exercises BINDING_COINCIDENT for the first time in the corpus;
    # Oedipus uses BINDING_SEPARATED.
    peripeteia_event_id="E_macduff_reveals_birth",
    anagnorisis_event_id="E_macduff_reveals_birth",
    # The dramatic present of the play spans hours to days; the
    # mythos's central action spans from Macbeth's antecedent
    # kinship (τ_s=-100) through Malcolm's coronation (τ_s=18) —
    # roughly 118 units. Same choice as Oedipus: unity of time is
    # not asserted at mythos scope.
    asserts_unity_of_action=True,
    asserts_unity_of_time=False,
    asserts_unity_of_place=False,
    aims_at_catharsis=True,
    characters=(AR_MACBETH, AR_LADY_MACBETH),
    # A11 — Lady Macbeth's sleepwalking as non-precipitating
    # staggered recognition. Contrasts Oedipus's precipitating
    # Jocasta step.
    anagnorisis_chain=(AR_STEP_LADY_MACBETH_SLEEPWALKING,),
    # A12 — peripeteia and anagnorisis at the same event.
    peripeteia_anagnorisis_binding=BINDING_COINCIDENT,
)
