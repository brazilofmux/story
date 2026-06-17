"""
sworn_aristotelian.py — "Sworn" under the Aristotelian dialect.

The overlay for the reverse-told original in `sworn.py`. The mythos's
STRUCTURE is ordinary Aristotelian (phases, peripeteia, anagnorisis in
chronological story-time) — deliberately, so that the only hard variable
is the SJUZHET, which the substrate stages in strict reverse. The
overlay verifies clean under A1–A23; the experiment is whether the
generator honours the backward staging the substrate specifies.

Exercises: A5 hamartia (honesty mistaken for virtue — the vanity of the
plain-truth man); A12 BINDING_SEPARATED (peripeteia at the testimony,
τ_s=0; anagnorisis ten beats later, τ_s=10); A20 anti-recognition
(Aleks, condemned, sees too late that his friend's vanity killed him);
A22 pathos-split (Aleks carries the pity-and-fear, Tomas carries the
recognition).
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
    QUALIFIER_ANTI,
)


# ============================================================================
# Phases — A2 (in chronological story-time, NOT staging order)
# ============================================================================

PH_BEGINNING = ArPhase(
    id="ph_sworn_beginning",
    role=PHASE_BEGINNING,
    scope_event_ids=(
        "E_friendship",
        "E_tomas_creed",
        "E_viktor_dies",
        "E_aleks_asks",
    ),
    annotation=(
        "The bond, the creed, and the dilemma. The boyhood vow; Tomas's "
        "name built on never lying; the killing Aleks is innocently present "
        "for; and Aleks's plea that Tomas merely stay silent. The beginning "
        "ends at the plea — the complication that binds the action."
    ),
)

PH_MIDDLE = ArPhase(
    id="ph_sworn_middle",
    role=PHASE_MIDDLE,
    scope_event_ids=(
        "E_tomas_chooses",
        "E_the_testimony",
        "E_the_verdict",
    ),
    annotation=(
        "The binding tightens. Tomas resolves that his creed forbids even a "
        "deceiving silence; he gives the bare fact at the trial; Aleks is "
        "condemned on it. The peripeteia (the testimony) sits here — the "
        "honesty turned weapon."
    ),
)

PH_END = ArPhase(
    id="ph_sworn_end",
    role=PHASE_END,
    scope_event_ids=(
        "E_execution",
        "E_tomas_alone",
        "E_tomas_silent",
    ),
    annotation=(
        "The unbinding. Aleks is executed (the pathos); Tomas, alone, "
        "recognises he chose his name over his friend (the anagnorisis); and "
        "the man of plain words is undone into permanent silence."
    ),
)


# ============================================================================
# Characters — A5 (+ A22/A23)
# ============================================================================

AR_TOMAS = ArCharacter(
    id="ar_tomas",
    name="Tomas",
    character_ref_id="tomas",
    hamartia_text=(
        "Honesty mistaken for virtue — the vanity of the plain-truth man. "
        "Tomas's error is not malice: it is that his whole identity is built "
        "on never lying, not even by a silence that deceives, and he cannot "
        "set that creed down even to save an innocent friend. He gives the "
        "bare fact and lets it kill, mistaking the literal truth for the "
        "deeper one. The hamartia is a missing-of-the-mark (Poetics 1453a): "
        "he loves being the honest man more than he loves the man he could "
        "have saved, and does not see it until the saving is impossible."
    ),
    is_tragic_hero=True,
)

AR_ALEKS = ArCharacter(
    id="ar_aleks",
    name="Aleks",
    character_ref_id="aleks",
    hamartia_text=None,
    # A22/A23 — the pathos-centre. Aleks is innocent; he carries the play's
    # pity-and-fear and pays for Tomas's creed with his life, without being
    # the agent of the recognition. is_tragic_hero=False. The split is the
    # OQ-MALFI-3 shape: pathos-centre (Aleks) distinct from the recognizer
    # (Tomas).
    is_tragic_hero=False,
    pathos_carrier=True,
)


# ============================================================================
# Anagnorisis chain — A11 / A14 / A20
# ============================================================================

AR_STEP_ALEKS_VERDICT = ArAnagnorisisStep(
    id="arstep_aleks_verdict",
    event_id="E_the_verdict",
    character_ref_id="ar_aleks",
    precipitates_main=False,
    anagnorisis_qualifier=QUALIFIER_ANTI,
    annotation=(
        "An anti-recognition (A20). Condemned on his friend's bare fact, "
        "Aleks looks at Tomas and recognises — too late, and unable to alter "
        "it — that Tomas's honesty was vanity: he loved being the honest man "
        "more than he loved the friend he is now sending to the rope. The "
        "recognition is real and complete and powerless. It does not "
        "precipitate Tomas's own recognition, which comes later, alone."
    ),
)


# ============================================================================
# Mythos — A1
# ============================================================================

AR_SWORN_MYTHOS = ArMythos(
    id="ar_sworn",
    title="Sworn",
    action_summary=(
        "A man whose whole name is built on never lying — not even by a "
        "silence that deceives — is the one witness who saw his innocent, "
        "sworn friend at the scene of a killing the friend tried to stop. "
        "The friend begs only for his silence; the creed forbids it. At the "
        "trial Tomas gives the bare fact without the saving context, and the "
        "plain truth he is proudest of condemns the man he loves — the "
        "peripeteia, his honesty turned the instrument of an innocent's "
        "death. The friend, condemned, sees too late that vanity, not truth, "
        "has killed him; he is executed, the pathos-centre, the one who pays "
        "for the creed. Alone afterward, Tomas recognises that there was a "
        "truth deeper than the facts — mercy, the friend before the name — "
        "and that he betrayed it; the recognition comes too late to save "
        "anyone. The man of plain words never speaks again. The tale is told "
        "backward, from the silence to the boyhood vow."
    ),
    central_event_ids=(
        "E_friendship",
        "E_tomas_creed",
        "E_viktor_dies",
        "E_aleks_asks",
        "E_tomas_chooses",
        "E_the_testimony",
        "E_the_verdict",
        "E_execution",
        "E_tomas_alone",
        "E_tomas_silent",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=(PH_BEGINNING, PH_MIDDLE, PH_END),
    complication_event_id="E_aleks_asks",
    denouement_event_id="E_the_verdict",
    # Peripeteia: the plain testimony condemns the innocent (τ_s=0).
    # Anagnorisis: alone, Tomas recognises he chose his name over his friend
    # (τ_s=10). Ten beats apart — SEPARATED.
    peripeteia_event_id="E_the_testimony",
    anagnorisis_event_id="E_tomas_alone",
    anagnorisis_character_ref_id="ar_tomas",
    asserts_unity_of_action=True,
    asserts_unity_of_time=False,
    asserts_unity_of_place=False,
    aims_at_catharsis=True,
    characters=(AR_TOMAS, AR_ALEKS),
    # A11 / A20 — Aleks's anti-recognition at the verdict.
    anagnorisis_chain=(AR_STEP_ALEKS_VERDICT,),
    # A12 — SEPARATED: peripeteia (τ_s=0) and anagnorisis (τ_s=10).
    peripeteia_anagnorisis_binding=BINDING_SEPARATED,
    # A22 — the pathos-centre (Aleks), split from the recognizer (Tomas).
    pathos_character_ref_ids=("ar_aleks",),
)
