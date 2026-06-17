"""
vantage_light_aristotelian.py — "The Vantage Light" under the
Aristotelian dialect (sketches 01–07).

The Aristotelian overlay for the ORIGINAL substrate in
`vantage_light.py`. Authored to exercise the full landed apparatus on a
story outside any canon:

- A1–A9 — complex plot; beginning / middle / end; peripeteia +
  anagnorisis; one tragic hero with a hamartia.
- A12 — BINDING_ADJACENT: the peripeteia (the ship founders, τ_s=9) and
  the anagnorisis (Halvard finds Inga, τ_s=11) are two beats apart.
- A20 (sketch-06) — an ANTI-recognition: Captain Rost, as his ship
  strikes the skerry, recognises too late that the steady light he
  trusted has betrayed him. Real, but powerless to alter the wreck.
- A22 (sketch-07) — the pathos-centre is SPLIT from the recognizer:
  Inga carries the play's pity-and-fear (she dies for her father's
  pride) while Halvard is the one who comes to knowledge. The exact
  OQ-MALFI-3 shape, on a brand-new story.

Verify:
    cd prototype
    python3 -c "
    from story_engine.encodings.vantage_light import FABULA
    from story_engine.encodings.vantage_light_aristotelian import (
        AR_VANTAGE_MYTHOS)
    from story_engine.core.aristotelian import verify
    obs = verify(AR_VANTAGE_MYTHOS, substrate_events=FABULA,
                 mythoi=(AR_VANTAGE_MYTHOS,))
    print(f'{len(obs)} observation(s)')
    for o in obs: print(' ', o.severity, o.code)
    "
"""

from __future__ import annotations

from story_engine.core.aristotelian import (
    ArAnagnorisisStep,
    ArCharacter,
    ArMythos,
    ArPhase,
    BINDING_ADJACENT,
    PHASE_BEGINNING,
    PHASE_END,
    PHASE_MIDDLE,
    PLOT_COMPLEX,
    QUALIFIER_ANTI,
)


# ============================================================================
# Phases — A2
# ============================================================================

PH_BEGINNING = ArPhase(
    id="ph_vantage_beginning",
    role=PHASE_BEGINNING,
    scope_event_ids=(
        "E_maren_lost",
        "E_inga_raised",
        "E_record_kept",
        "E_tobias_brings_warning",
    ),
    annotation=(
        "The antecedent wound and the inciting warning. Maren's drowning "
        "is the scar under the record; Inga is raised at the light; the "
        "thirty-year record is established as Halvard's honour. The "
        "beginning ends when Tobias brings the storm-glass and the warning "
        "— the complication that binds the action."
    ),
)

PH_MIDDLE = ArPhase(
    id="ph_vantage_middle",
    role=PHASE_MIDDLE,
    scope_event_ids=(
        "E_halvard_dismisses",
        "E_inga_sees_glass",
        "E_halvard_refuses",
        "E_storm_breaks",
        "E_ship_makes_run",
        "E_inga_takes_dory",
    ),
    annotation=(
        "The binding of the ties. Halvard's pride refuses the glass; Inga "
        "reads it and believes; he refuses to signal; the storm breaks; "
        "the captain, trusting the never-failing light, makes the run; and "
        "Inga, when her father will not act, takes the dory out herself. "
        "The middle ends at the daughter's resolve, the last beat before "
        "the reversal."
    ),
)

PH_END = ArPhase(
    id="ph_vantage_end",
    role=PHASE_END,
    scope_event_ids=(
        "E_ship_founders",
        "E_inga_drowns",
        "E_halvard_finds_inga",
        "E_halvard_dark",
    ),
    annotation=(
        "The unbinding. The peripeteia (the light guides the ship onto the "
        "skerry; the record breaks), the pathos (Inga drowns), the "
        "anagnorisis (Halvard finds her and recognises that his pride, not "
        "the sea, did this), and the catastrophe (he lets the light go "
        "dark). Recognition follows the reversal by necessity."
    ),
)


# ============================================================================
# Characters — A5 (+ A22/A23 sketch-07 pathos)
# ============================================================================

AR_HALVARD = ArCharacter(
    id="ar_halvard",
    name="Halvard",
    character_ref_id="halvard",
    hamartia_text=(
        "Pride in the unbroken record, mistaken for fidelity to the light. "
        "Halvard's error is not cruelty: it is that to raise the danger-"
        "signal would be to admit the sea can best his judgement — and "
        "after Maren, that admission is the one thing he cannot make. He "
        "trusts his own eye over the storm-glass and refuses to signal, "
        "choosing the record over the warning. The error is a missing-of-"
        "the-mark (Poetics 1453a), not a moral vice: he acts to keep faith "
        "with thirty years of duty, and the keeping is what kills."
    ),
    is_tragic_hero=True,
)

AR_INGA = ArCharacter(
    id="ar_inga",
    name="Inga",
    character_ref_id="inga",
    hamartia_text=None,
    # A22/A23 — the pathos-centre. Inga carries the play's pity-and-fear
    # without being the agent of the recognition: she believed the glass
    # her father taught her to read, acted when he would not, and the sea
    # took her. is_tragic_hero=False (she has no hamartia-driven arc — she
    # is the one who PAYS for Halvard's). The split is the OQ-MALFI-3
    # shape: pathos-centre (Inga) distinct from the recognizer (Halvard).
    is_tragic_hero=False,
    pathos_carrier=True,
)

AR_CAPTAIN = ArCharacter(
    id="ar_captain",
    name="Captain Rost",
    character_ref_id="captain_rost",
    hamartia_text=None,
    # The victim whose trust in the light is the play's cruelest irony.
    # is_tragic_hero=False; authored for the A20 anti-recognition step at
    # the wreck.
    is_tragic_hero=False,
)


# ============================================================================
# Anagnorisis chain — A11 / A14 / A20
# ============================================================================

AR_STEP_CAPTAIN_WRECK = ArAnagnorisisStep(
    id="arstep_captain_wreck",
    event_id="E_ship_founders",
    character_ref_id="ar_captain",
    precipitates_main=False,
    anagnorisis_qualifier=QUALIFIER_ANTI,
    annotation=(
        "An anti-recognition (A20). As his ship strikes the skerry, "
        "Captain Rost recognises that the steady Vantage Light he trusted "
        "has led him onto the rocks — the keeper never signalled the "
        "danger. The recognition is real and complete, and wholly too late "
        "to alter the wreck. It is co-located with the peripeteia event "
        "(the founder is both the reversal of Halvard's record and the "
        "captain's too-late knowledge) but does not precipitate Halvard's "
        "main recognition, which comes two beats later over Inga's body."
    ),
)


# ============================================================================
# Mythos — A1
# ============================================================================

AR_VANTAGE_MYTHOS = ArMythos(
    id="ar_vantage",
    title="The Vantage Light",
    action_summary=(
        "A lighthouse keeper whose thirty-year unbroken record is the scar "
        "over his drowned wife refuses a storm-glass warning out of pride "
        "— to signal danger would be to admit the sea can best him. His "
        "daughter, who reads the falling glass he taught her, takes the "
        "dory out to warn the inbound ship herself when he will not. The "
        "storm breaks; the captain, trusting the never-failing light, makes "
        "the harbour run, and the steady light guides his ship onto the "
        "skerry — the peripeteia, the keeper's own virtue turned the "
        "instrument of the wreck, the record broken in the same instant. "
        "The daughter drowns in the attempt; she is the pathos-centre, the "
        "one who pays for the pride. Finding her body and the spent "
        "hand-lantern, the keeper recognises — too late — that the sea did "
        "not best him: he bested himself. He lets the light go dark."
    ),
    central_event_ids=(
        "E_maren_lost",
        "E_inga_raised",
        "E_record_kept",
        "E_tobias_brings_warning",
        "E_halvard_dismisses",
        "E_inga_sees_glass",
        "E_halvard_refuses",
        "E_storm_breaks",
        "E_ship_makes_run",
        "E_inga_takes_dory",
        "E_ship_founders",
        "E_inga_drowns",
        "E_halvard_finds_inga",
        "E_halvard_dark",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=(PH_BEGINNING, PH_MIDDLE, PH_END),
    complication_event_id="E_tobias_brings_warning",
    denouement_event_id="E_inga_takes_dory",
    # Peripeteia: the never-failing light becomes the instrument of the
    # wreck (τ_s=9). Anagnorisis: Halvard finds Inga and recognises his
    # pride did this (τ_s=11). Two beats apart.
    peripeteia_event_id="E_ship_founders",
    anagnorisis_event_id="E_halvard_finds_inga",
    anagnorisis_character_ref_id="ar_halvard",
    asserts_unity_of_action=True,
    asserts_unity_of_time=False,
    asserts_unity_of_place=False,
    aims_at_catharsis=True,
    characters=(AR_HALVARD, AR_INGA, AR_CAPTAIN),
    # A11 / A20 — the captain's anti-recognition at the wreck.
    anagnorisis_chain=(AR_STEP_CAPTAIN_WRECK,),
    # A12 — ADJACENT: peripeteia (τ_s=9) and anagnorisis (τ_s=11) are two
    # τ_s apart (within the default adjacency bound of 3).
    peripeteia_anagnorisis_binding=BINDING_ADJACENT,
    # A22 (sketch-07) — the pathos-centre, split from the recognizer.
    # Inga carries the pity-and-fear; Halvard (anagnorisis_character_ref_id)
    # carries the recognition.
    pathos_character_ref_ids=("ar_inga",),
)
