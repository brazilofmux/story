"""
oedipus_aristotelian.py — Oedipus Tyrannus encoded under the
Aristotelian dialect (aristotelian-sketch-01).

Worked example of aristotelian-sketch-01 A1–A9 on the example
Aristotle built the theory from. Oedipus is cited explicitly in
the *Poetics* (1452a) for the messenger's reveal — the peripeteia
— and for the unity of its anagnorisis and peripeteia.

Substrate layer: `prototype/story_engine/encodings/oedipus.py`.
This file references substrate event ids by string; it does not
import the Event records themselves. Callers that want to run the
A7 self-verifier with unity-of-time / unity-of-place / event-ref
/ hamartia-participation checks should import `FABULA` from
`oedipus.py` and pass it to `verify()`.

Sketch-02 extensions authored:

- A11 (ArAnagnorisisStep): `AR_STEP_JOCASTA` records Jocasta's
  private recognition at `E_jocasta_realizes` (τ_s=9), four
  substrate steps before Oedipus's own recognition at
  `E_oedipus_anagnorisis` (τ_s=13). `precipitates_main=True`:
  Jocasta's realization pressures Oedipus's. The singular
  `anagnorisis_event_id` remains Oedipus's; the chain names
  Jocasta's as the staggered earlier.
- A12 (peripeteia_anagnorisis_binding): `"separated"` — the
  peripeteia fires at `E_messenger_adoption_reveal` (τ_s=8); the
  anagnorisis lands five steps later at τ_s=13. The typed
  declaration replaces the earlier prose claim of coincidence;
  A7.8 verifies the τ_s distance is consistent with the binding.

Running:
    cd prototype
    python3 -c "
    from story_engine.encodings.oedipus import FABULA
    from story_engine.encodings.oedipus_aristotelian import (
        AR_OEDIPUS_MYTHOS,
    )
    from story_engine.core.aristotelian import verify
    observations = verify(AR_OEDIPUS_MYTHOS, substrate_events=FABULA)
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
    id="ph_oedipus_beginning",
    role=PHASE_BEGINNING,
    scope_event_ids=(
        "E_birth",
        "E_exposure_and_rescue",
        "E_upbringing_in_corinth",
        "E_oracle_to_oedipus",
        "E_crossroads_killing",
        "E_marriage_and_crown",
    ),
    annotation=(
        "Antecedent action, dramatically compressed into narrative "
        "exposition. Oedipus's identity and guilt are structurally "
        "complete before the play opens: the oracle, the killing at "
        "the crossroads, the marriage to his mother. The Sophoclean "
        "play begins in medias res; the Aristotelian mythos includes "
        "the antecedent events that make the recognition intelligible."
    ),
)

PH_MIDDLE = ArPhase(
    id="ph_oedipus_middle",
    role=PHASE_MIDDLE,
    scope_event_ids=(
        "E_tiresias_accusation",
        "E_jocasta_mentions_crossroads",
        "E_messenger_polybus_dead",
        "E_messenger_adoption_reveal",
        "E_jocasta_realizes",
        "E_shepherd_testimony",
    ),
    annotation=(
        "The investigation — Poetics' 'binding' of the ties. Each "
        "testimony narrows the identity. Middle ends with the "
        "shepherd's testimony, the last piece of evidence before "
        "Oedipus's recognition."
    ),
)

PH_END = ArPhase(
    id="ph_oedipus_end",
    role=PHASE_END,
    scope_event_ids=(
        "E_oedipus_anagnorisis",
        "E_jocasta_suicide",
        "E_self_blinding",
        "E_exile",
    ),
    annotation=(
        "Unbinding of the ties. Recognition, Jocasta's suicide, "
        "self-blinding, exile — the consequences follow from "
        "recognition by necessity (Poetics 1452a: 'the natural "
        "kind of tragic incident')."
    ),
)


# ============================================================================
# Characters — A5
# ============================================================================

AR_OEDIPUS = ArCharacter(
    id="ar_oedipus",
    name="Oedipus",
    character_ref_id="oedipus",          # substrate Entity id
    hamartia_text=(
        "The investigator's virtue — pursuing truth to save the "
        "city — is the mechanism of his destruction. Hamartia is "
        "not a moral flaw (Bradleyan reading) but a missing-the-"
        "mark: ignorance of identity driving action that fulfills "
        "the prophecy he thought he was fleeing. He acts rightly "
        "on every piece of information he has; he simply cannot "
        "have the information that would redirect him."
    ),
    is_tragic_hero=True,
)

AR_JOCASTA = ArCharacter(
    id="ar_jocasta",
    name="Jocasta",
    character_ref_id="jocasta",
    hamartia_text=(
        "Parallel hamartia — ignorance of identity. She realizes "
        "before Oedipus does (E_jocasta_realizes, τ_s=9); her "
        "suicide at recognition mirrors Oedipus's self-blinding. "
        "The peripeteia (E_messenger_adoption_reveal, τ_s=8) "
        "strips the reassurance she had offered Oedipus; her fall "
        "follows from, rather than contributes to, the reversal."
    ),
    is_tragic_hero=False,
)


# ============================================================================
# Anagnorisis chain — A11 (sketch-02)
# ============================================================================
#
# Jocasta realizes at E_jocasta_realizes (τ_s=9), four substrate
# steps before Oedipus's own recognition at E_oedipus_anagnorisis
# (τ_s=13). Pre-sketch-02 the encoding placed her realization in
# the middle phase as a workaround for the singular
# anagnorisis_event_id; sketch-02 A11 lets the chain carry the
# staggered earlier recognition without retouching the main slot.

AR_STEP_JOCASTA = ArAnagnorisisStep(
    id="arstep_jocasta_realizes",
    event_id="E_jocasta_realizes",
    character_ref_id="ar_jocasta",
    precipitates_main=True,
    annotation=(
        "Jocasta realizes before Oedipus does. Her recognition "
        "precipitates the pressure toward his — she begs him to "
        "stop the investigation; her suicide follows. In the "
        "play's fabula she leaves the stage; in the mythos's "
        "structure she has triggered the recognition Oedipus will "
        "reach four τ_s-steps later at the shepherd's testimony. "
        "The dialect's singular anagnorisis_event_id names "
        "Oedipus's as the mythos's main recognition; this step "
        "names Jocasta's as the precipitating earlier."
    ),
)


# ============================================================================
# Mythos — A1
# ============================================================================

AR_OEDIPUS_MYTHOS = ArMythos(
    id="ar_oedipus",
    title="Oedipus Tyrannus",
    action_summary=(
        "A king, investigating a plague sent to punish his city's "
        "unpurged blood-guilt, discovers through a chain of "
        "witnesses that he himself is the murderer of his "
        "predecessor — and the son of his wife. Reversal and "
        "recognition are staged as a two-beat movement — "
        "peripeteia fires at the messenger's reveal (τ_s=8), "
        "five steps before explicit anagnorisis at the shepherd's "
        "testimony (τ_s=13). Catastrophe follows."
    ),
    central_event_ids=(
        "E_birth",
        "E_exposure_and_rescue",
        "E_upbringing_in_corinth",
        "E_oracle_to_oedipus",
        "E_crossroads_killing",
        "E_marriage_and_crown",
        "E_tiresias_accusation",
        "E_jocasta_mentions_crossroads",
        "E_messenger_polybus_dead",
        "E_messenger_adoption_reveal",
        "E_jocasta_realizes",
        "E_shepherd_testimony",
        "E_oedipus_anagnorisis",
        "E_jocasta_suicide",
        "E_self_blinding",
        "E_exile",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=(PH_BEGINNING, PH_MIDDLE, PH_END),
    complication_event_id="E_tiresias_accusation",
    denouement_event_id="E_shepherd_testimony",
    # Aristotle Poetics 1452a cites this moment specifically: the
    # messenger who came to cheer Oedipus and free him from his fears
    # about his mother, by revealing his origin, produced the opposite
    # effect. The reversal fires at the messenger's reveal, not at the
    # anagnorisis event proper — they are adjacent in τ_s (8 and 13).
    peripeteia_event_id="E_messenger_adoption_reveal",
    anagnorisis_event_id="E_oedipus_anagnorisis",
    # The *action* Oedipus dramatizes in performance is compressed (a
    # single day); the *central action* the Aristotelian mythos tracks
    # spans from Oedipus's birth (τ_s=-100) through exile (τ_s=17) —
    # roughly 117 units. Unity of time in Aristotle's sketchy sense
    # applies to the dramatic present only; the mythos record captures
    # the broader action. Not a dialect limitation; a design choice.
    asserts_unity_of_action=True,
    asserts_unity_of_time=False,
    asserts_unity_of_place=False,
    aims_at_catharsis=True,
    characters=(AR_OEDIPUS, AR_JOCASTA),
    # A11 — staggered recognition (Jocasta precedes + precipitates
    # Oedipus's). See AR_STEP_JOCASTA above.
    anagnorisis_chain=(AR_STEP_JOCASTA,),
    # A12 — peripeteia (E_messenger_adoption_reveal, τ_s=8) and
    # anagnorisis (E_oedipus_anagnorisis, τ_s=13) are separated by
    # five substrate steps; default adjacency_bound=3 is sufficient
    # to classify this as "separated" under A7.8.
    peripeteia_anagnorisis_binding=BINDING_SEPARATED,
)
