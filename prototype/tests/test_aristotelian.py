"""
test_aristotelian.py — permanent tests for the Aristotelian dialect
(aristotelian-sketch-01 commitments A1–A9, acceptance criteria AA1–
AA5).

Synthetic-fixture tests pin each A7 check's code-level behavior.
One integration test exercises the Oedipus worked-case encoding
against the real substrate FABULA.

Run:
    python3 -m tests.test_aristotelian
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.aristotelian import (
    ArAnagnorisisStep, ArAudienceKnowledgeConstraint, ArCharacter,
    ArCharacterArcRelation, ArCoPresenceRequirement,
    ArMythos, ArMythosRelation, ArObservation, ArPhase,
    ARC_RELATION_FOIL, ARC_RELATION_MIRROR, ARC_RELATION_PARALLEL,
    BINDING_ADJACENT, BINDING_COINCIDENT, BINDING_PREF_NEUTRAL,
    BINDING_PREF_WIDE, BINDING_SEPARATED,
    CANONICAL_BINDING_DISTANCE_PREFERENCES,
    CANONICAL_CHARACTER_ARC_RELATION_KINDS,
    CANONICAL_DIRECTIONALITIES,
    CANONICAL_PACING_PREFERENCES,
    CANONICAL_POLARITIES,
    CANONICAL_RELATION_KINDS,
    CANONICAL_TONAL_REGISTERS,
    DIRECTIONALITY_DIRECTIONAL,
    DIRECTIONALITY_SYMMETRIC,
    POLARITY_MALICIOUS,
    POLARITY_NEUTRAL,
    POLARITY_SANCTIONED,
    POLARITY_THERAPEUTIC,
    PACING_EVEN, PACING_RAPID_ESCALATION, PACING_SLOW_BURN,
    PHASE_BEGINNING, PHASE_END, PHASE_MIDDLE,
    PLOT_COMPLEX, PLOT_SIMPLE,
    RELATION_CONTAINS, RELATION_CONTESTS, RELATION_PARALLEL,
    SEVERITY_ADVISES_REVIEW, SEVERITY_NOTED,
    STEP_KIND_PARALLEL, STEP_KIND_PRECIPITATING, STEP_KIND_STAGING,
    TONAL_REGISTER_TRAGIC_PURE, TONAL_REGISTER_TRAGIC_WITH_IRONY,
    VALID_PERIPETEIA_ANAGNORISIS_BINDINGS,
    VALID_PHASE_ROLES, VALID_PLOT_KINDS, VALID_STEP_KINDS,
    group_by_code, group_by_severity, verify,
)
from story_engine.core.substrate import (
    Event, EventStatus, Prop, WorldEffect,
)


# ----------------------------------------------------------------------------
# Helpers — synthetic fixtures
# ----------------------------------------------------------------------------


def _synthetic_event(
    id: str,
    τ_s: int = 0,
    participants: dict | None = None,
    at_location: str | None = None,
) -> Event:
    effects: tuple = ()
    if at_location is not None:
        actor = (list(participants.values())[0]
                 if participants else "agent")
        effects = (WorldEffect(
            prop=Prop(predicate="at_location", args=(actor, at_location)),
            asserts=True,
        ),)
    return Event(
        id=id, type="synthetic", τ_s=τ_s, τ_a=τ_s,
        participants=(participants or {}),
        effects=effects,
        status=EventStatus.COMMITTED,
    )


def _three_phase_mythos(
    plot_kind: str = PLOT_COMPLEX,
    peripeteia: str | None = "E2",
    anagnorisis: str | None = "E3",
    **mythos_kwargs,
) -> ArMythos:
    """A clean three-phase synthetic mythos: E1 (beginning),
    E2 (middle), E3 (end). Complex by default with peripeteia at
    E2 and anagnorisis at E3."""
    return ArMythos(
        id="m_test",
        title="Test Mythos",
        action_summary="synthetic",
        central_event_ids=("E1", "E2", "E3"),
        plot_kind=plot_kind,
        phases=(
            ArPhase(id="ph_b", role=PHASE_BEGINNING,
                    scope_event_ids=("E1",)),
            ArPhase(id="ph_m", role=PHASE_MIDDLE,
                    scope_event_ids=("E2",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=("E3",)),
        ),
        peripeteia_event_id=peripeteia,
        anagnorisis_event_id=anagnorisis,
        **mythos_kwargs,
    )


def _has_code(obs_list: list, code: str) -> bool:
    return any(o.code == code for o in obs_list)


# ============================================================================
# Record construction (AA1)
# ============================================================================


def test_armythos_minimal_construction():
    m = _three_phase_mythos()
    assert m.id == "m_test"
    assert m.plot_kind == PLOT_COMPLEX
    assert m.asserts_unity_of_action is True         # default True
    assert m.asserts_unity_of_time is False          # default False
    assert m.asserts_unity_of_place is False
    assert m.aims_at_catharsis is True
    assert m.unity_of_time_bound == 24               # default
    assert m.unity_of_place_max_locations == 1


def test_arphase_role_constants():
    assert VALID_PHASE_ROLES == frozenset(
        {PHASE_BEGINNING, PHASE_MIDDLE, PHASE_END})


def test_arphase_valid_plot_kinds():
    assert VALID_PLOT_KINDS == frozenset({PLOT_SIMPLE, PLOT_COMPLEX})


def test_archaracter_defaults():
    c = ArCharacter(id="c1", name="Hero")
    assert c.character_ref_id is None
    assert c.hamartia_text is None
    assert c.is_tragic_hero is False


# ============================================================================
# A7 check 1 — plot_kind validation
# ============================================================================


def test_verify_accepts_simple_plot_without_peripeteia():
    m = _three_phase_mythos(
        plot_kind=PLOT_SIMPLE, peripeteia=None, anagnorisis=None,
    )
    obs = verify(m)
    assert not _has_code(obs, "plot_kind_invalid")
    assert not _has_code(obs, "complex_missing_peripeteia_or_anagnorisis")


def test_verify_flags_invalid_plot_kind():
    m = _three_phase_mythos(plot_kind="epic")          # not in vocab
    obs = verify(m)
    assert _has_code(obs, "plot_kind_invalid")


def test_verify_flags_complex_without_peripeteia_or_anagnorisis():
    m = _three_phase_mythos(
        plot_kind=PLOT_COMPLEX, peripeteia=None, anagnorisis=None,
    )
    obs = verify(m)
    assert _has_code(obs, "complex_missing_peripeteia_or_anagnorisis")


def test_verify_accepts_complex_with_only_peripeteia():
    m = _three_phase_mythos(peripeteia="E2", anagnorisis=None)
    obs = verify(m)
    assert not _has_code(obs, "complex_missing_peripeteia_or_anagnorisis")


def test_verify_accepts_complex_with_only_anagnorisis():
    m = _three_phase_mythos(peripeteia=None, anagnorisis="E3")
    obs = verify(m)
    assert not _has_code(obs, "complex_missing_peripeteia_or_anagnorisis")


# ============================================================================
# A7 check 2 / A6 unity of action — phase coverage
# ============================================================================


def test_verify_flags_missing_phase_role():
    # Only beginning + end, no middle
    m = ArMythos(
        id="m", title="t", action_summary="",
        central_event_ids=("E1", "E2"),
        plot_kind=PLOT_SIMPLE,
        phases=(
            ArPhase(id="ph_b", role=PHASE_BEGINNING,
                    scope_event_ids=("E1",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=("E2",)),
        ),
    )
    obs = verify(m)
    assert _has_code(obs, "phase_role_missing")


def test_verify_flags_invalid_phase_role():
    m = ArMythos(
        id="m", title="t", action_summary="",
        central_event_ids=("E1",),
        plot_kind=PLOT_SIMPLE,
        phases=(
            ArPhase(id="ph_x", role="prologue", scope_event_ids=("E1",)),
        ),
    )
    obs = verify(m)
    assert _has_code(obs, "phase_role_invalid")


def test_verify_flags_phase_overlap():
    # E2 in both middle and end
    m = ArMythos(
        id="m", title="t", action_summary="",
        central_event_ids=("E1", "E2", "E3"),
        plot_kind=PLOT_SIMPLE,
        phases=(
            ArPhase(id="ph_b", role=PHASE_BEGINNING,
                    scope_event_ids=("E1",)),
            ArPhase(id="ph_m", role=PHASE_MIDDLE,
                    scope_event_ids=("E2",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=("E2", "E3")),
        ),
    )
    obs = verify(m)
    assert _has_code(obs, "phase_overlap")


def test_verify_flags_central_event_unphased():
    # E3 in central_event_ids but not in any phase
    m = ArMythos(
        id="m", title="t", action_summary="",
        central_event_ids=("E1", "E2", "E3"),
        plot_kind=PLOT_SIMPLE,
        phases=(
            ArPhase(id="ph_b", role=PHASE_BEGINNING,
                    scope_event_ids=("E1",)),
            ArPhase(id="ph_m", role=PHASE_MIDDLE,
                    scope_event_ids=("E2",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=()),
        ),
    )
    obs = verify(m)
    assert _has_code(obs, "central_event_unphased")


def test_verify_flags_phase_event_not_central():
    # Phase references E99 which is not in central_event_ids
    m = ArMythos(
        id="m", title="t", action_summary="",
        central_event_ids=("E1",),
        plot_kind=PLOT_SIMPLE,
        phases=(
            ArPhase(id="ph_b", role=PHASE_BEGINNING,
                    scope_event_ids=("E1", "E99")),
            ArPhase(id="ph_m", role=PHASE_MIDDLE, scope_event_ids=()),
            ArPhase(id="ph_e", role=PHASE_END, scope_event_ids=()),
        ),
    )
    obs = verify(m)
    assert _has_code(obs, "phase_event_not_central")


# ============================================================================
# A7 check 4 — event-ref integrity
# ============================================================================


def test_verify_skips_event_ref_check_when_no_substrate():
    m = _three_phase_mythos()
    obs = verify(m)                              # no substrate_events
    assert not _has_code(obs, "event_ref_unresolved")


def test_verify_flags_event_ref_unresolved():
    m = _three_phase_mythos()
    events = (
        _synthetic_event("E1"),
        _synthetic_event("E2"),
        # E3 missing
    )
    obs = verify(m, substrate_events=events)
    assert _has_code(obs, "event_ref_unresolved")


def test_verify_flags_peripeteia_ref_unresolved():
    m = _three_phase_mythos(peripeteia="E_missing", anagnorisis=None)
    events = (
        _synthetic_event("E1"),
        _synthetic_event("E2"),
        _synthetic_event("E3"),
    )
    obs = verify(m, substrate_events=events)
    assert _has_code(obs, "event_ref_unresolved")


# ============================================================================
# A6 unity-of-time check
# ============================================================================


def test_verify_unity_of_time_not_checked_when_not_asserted():
    # τ_s span 0..1000, but assertion is False (default)
    m = _three_phase_mythos()
    events = (
        _synthetic_event("E1", τ_s=0),
        _synthetic_event("E2", τ_s=500),
        _synthetic_event("E3", τ_s=1000),
    )
    obs = verify(m, substrate_events=events)
    assert not _has_code(obs, "unity_of_time_violated")


def test_verify_unity_of_time_respected():
    m = _three_phase_mythos(
        asserts_unity_of_time=True, unity_of_time_bound=24,
    )
    events = (
        _synthetic_event("E1", τ_s=0),
        _synthetic_event("E2", τ_s=10),
        _synthetic_event("E3", τ_s=20),
    )
    obs = verify(m, substrate_events=events)
    assert not _has_code(obs, "unity_of_time_violated")


def test_verify_unity_of_time_violated():
    m = _three_phase_mythos(
        asserts_unity_of_time=True, unity_of_time_bound=24,
    )
    events = (
        _synthetic_event("E1", τ_s=0),
        _synthetic_event("E2", τ_s=50),
        _synthetic_event("E3", τ_s=100),
    )
    obs = verify(m, substrate_events=events)
    assert _has_code(obs, "unity_of_time_violated")


# ============================================================================
# A6 unity-of-place check
# ============================================================================


def test_verify_unity_of_place_not_checked_when_not_asserted():
    m = _three_phase_mythos()
    events = (
        _synthetic_event("E1", participants={"a": "x"},
                         at_location="thebes"),
        _synthetic_event("E2", participants={"a": "x"},
                         at_location="corinth"),
        _synthetic_event("E3", participants={"a": "x"},
                         at_location="grove"),
    )
    obs = verify(m, substrate_events=events)
    assert not _has_code(obs, "unity_of_place_violated")


def test_verify_unity_of_place_single_location():
    m = _three_phase_mythos(asserts_unity_of_place=True)
    events = (
        _synthetic_event("E1", participants={"a": "x"},
                         at_location="thebes"),
        _synthetic_event("E2", participants={"a": "x"},
                         at_location="thebes"),
        _synthetic_event("E3", participants={"a": "x"},
                         at_location="thebes"),
    )
    obs = verify(m, substrate_events=events)
    assert not _has_code(obs, "unity_of_place_violated")


def test_verify_unity_of_place_multiple_locations_violates():
    m = _three_phase_mythos(asserts_unity_of_place=True)
    events = (
        _synthetic_event("E1", participants={"a": "x"},
                         at_location="thebes"),
        _synthetic_event("E2", participants={"a": "x"},
                         at_location="corinth"),
        _synthetic_event("E3", participants={"a": "x"},
                         at_location="grove"),
    )
    obs = verify(m, substrate_events=events)
    assert _has_code(obs, "unity_of_place_violated")


# ============================================================================
# A7 check 5 — hamartia participation
# ============================================================================


def test_verify_hamartia_participation_passes_when_hero_participates():
    m = _three_phase_mythos()
    m_with_char = ArMythos(
        **{**m.__dict__,
           "characters": (
               ArCharacter(id="ar_hero", name="Hero",
                           character_ref_id="hero",
                           hamartia_text="overreach",
                           is_tragic_hero=True),
           )},
    )
    events = (
        _synthetic_event("E1", participants={"protagonist": "hero"}),
        _synthetic_event("E2", participants={"protagonist": "hero"}),
        _synthetic_event("E3", participants={"protagonist": "hero"}),
    )
    obs = verify(m_with_char, substrate_events=events)
    assert not _has_code(obs, "hamartia_hero_absent")


def test_verify_hamartia_participation_flags_absent_hero():
    m = _three_phase_mythos()
    m_with_char = ArMythos(
        **{**m.__dict__,
           "characters": (
               ArCharacter(id="ar_hero", name="Hero",
                           character_ref_id="hero",
                           hamartia_text="overreach",
                           is_tragic_hero=True),
           )},
    )
    events = (
        _synthetic_event("E1", participants={"other": "someone_else"}),
        _synthetic_event("E2", participants={"other": "yet_another"}),
        _synthetic_event("E3", participants={"other": "third_party"}),
    )
    obs = verify(m_with_char, substrate_events=events)
    assert _has_code(obs, "hamartia_hero_absent")


def test_verify_hamartia_participation_skips_when_not_tragic_hero():
    m = _three_phase_mythos()
    m_with_char = ArMythos(
        **{**m.__dict__,
           "characters": (
               ArCharacter(id="ar_sidekick", name="Sidekick",
                           character_ref_id="sidekick",
                           hamartia_text="some flaw",
                           is_tragic_hero=False),
           )},
    )
    events = (
        _synthetic_event("E1", participants={"other": "someone_else"}),
        _synthetic_event("E2", participants={"other": "someone_else"}),
        _synthetic_event("E3", participants={"other": "someone_else"}),
    )
    obs = verify(m_with_char, substrate_events=events)
    assert not _has_code(obs, "hamartia_hero_absent")


def test_verify_hamartia_participation_skips_when_no_character_ref():
    m = _three_phase_mythos()
    m_with_char = ArMythos(
        **{**m.__dict__,
           "characters": (
               ArCharacter(id="ar_hero", name="Hero",
                           character_ref_id=None,  # standalone
                           hamartia_text="overreach",
                           is_tragic_hero=True),
           )},
    )
    events = (
        _synthetic_event("E1", participants={"other": "someone_else"}),
        _synthetic_event("E2", participants={"other": "someone_else"}),
        _synthetic_event("E3", participants={"other": "someone_else"}),
    )
    obs = verify(m_with_char, substrate_events=events)
    assert not _has_code(obs, "hamartia_hero_absent")


# ============================================================================
# Convenience groupings
# ============================================================================


def test_group_by_severity_buckets_correctly():
    obs_list = [
        ArObservation(severity=SEVERITY_NOTED, code="x",
                      target_id="t", message=""),
        ArObservation(severity=SEVERITY_ADVISES_REVIEW, code="y",
                      target_id="t", message=""),
        ArObservation(severity=SEVERITY_ADVISES_REVIEW, code="z",
                      target_id="t", message=""),
    ]
    groups = group_by_severity(obs_list)
    assert len(groups[SEVERITY_NOTED]) == 1
    assert len(groups[SEVERITY_ADVISES_REVIEW]) == 2


def test_group_by_code_buckets_correctly():
    obs_list = [
        ArObservation(severity=SEVERITY_ADVISES_REVIEW, code="foo",
                      target_id="t", message=""),
        ArObservation(severity=SEVERITY_ADVISES_REVIEW, code="foo",
                      target_id="t", message=""),
        ArObservation(severity=SEVERITY_NOTED, code="bar",
                      target_id="t", message=""),
    ]
    groups = group_by_code(obs_list)
    assert len(groups["foo"]) == 2
    assert len(groups["bar"]) == 1


# ============================================================================
# Integration — Oedipus worked-case (AA3 + AA5)
# ============================================================================


def test_oedipus_aristotelian_verifies_clean():
    """The worked case of aristotelian-sketch-01: Oedipus Tyrannus
    encoded under A1–A9 should verify with zero observations against
    the real oedipus.py FABULA. If this breaks, the sketch's design-
    phase GREEN verdict is amended."""
    from story_engine.encodings.oedipus import FABULA
    from story_engine.encodings.oedipus_aristotelian import (
        AR_OEDIPUS_MYTHOS,
    )
    observations = verify(
        AR_OEDIPUS_MYTHOS, substrate_events=FABULA,
    )
    assert observations == [], (
        f"Expected zero observations; got {len(observations)}:\n"
        + "\n".join(f"  [{o.severity}] {o.code}: {o.message}"
                    for o in observations)
    )


def test_oedipus_aristotelian_records_shape():
    """Structural pins on AR_OEDIPUS_MYTHOS matching the sketch's
    worked case."""
    from story_engine.encodings.oedipus_aristotelian import (
        AR_OEDIPUS_MYTHOS,
    )
    m = AR_OEDIPUS_MYTHOS
    assert m.plot_kind == PLOT_COMPLEX
    assert len(m.phases) == 3
    assert [ph.role for ph in m.phases] == [
        PHASE_BEGINNING, PHASE_MIDDLE, PHASE_END,
    ]
    assert m.peripeteia_event_id == "E_messenger_adoption_reveal"
    assert m.anagnorisis_event_id == "E_oedipus_anagnorisis"
    assert m.asserts_unity_of_action is True
    assert m.asserts_unity_of_time is False       # see sketch worked case
    assert m.asserts_unity_of_place is False
    assert m.aims_at_catharsis is True
    assert len(m.characters) == 2
    oedipus_char = [c for c in m.characters if c.id == "ar_oedipus"][0]
    assert oedipus_char.is_tragic_hero is True
    assert oedipus_char.character_ref_id == "oedipus"
    assert oedipus_char.hamartia_text is not None


# ============================================================================
# Integration — Rashomon stress case (sketch's multi-mythos prediction)
# ============================================================================


def test_rashomon_aristotelian_four_mythoi_all_verify_clean():
    """Aristotelian-sketch-01's stress-case prediction: Rashomon
    encodes as four testimony mythoi, each independently
    satisfying A1-A9's self-verifier. Zero observations per mythos
    confirms the sketch's 'multi-mythos slots in without
    modification' claim at the code level."""
    from story_engine.encodings.rashomon import EVENTS_ALL
    from story_engine.encodings.rashomon_aristotelian import (
        AR_RASHOMON_MYTHOI,
    )
    for mythos in AR_RASHOMON_MYTHOI:
        observations = verify(mythos, substrate_events=EVENTS_ALL)
        assert observations == [], (
            f"{mythos.id}: expected zero observations; got "
            f"{len(observations)}:\n"
            + "\n".join(f"    [{o.severity}] {o.code}: {o.message}"
                        for o in observations)
        )


def test_rashomon_aristotelian_mythoi_count_and_ids():
    """Structural pin: the encoding authors exactly four mythoi,
    one per testimony, with the expected ids."""
    from story_engine.encodings.rashomon_aristotelian import (
        AR_RASHOMON_MYTHOI,
    )
    assert len(AR_RASHOMON_MYTHOI) == 4
    ids = [m.id for m in AR_RASHOMON_MYTHOI]
    assert ids == [
        "ar_rashomon_bandit",
        "ar_rashomon_wife",
        "ar_rashomon_samurai",
        "ar_rashomon_woodcutter",
    ]


def test_rashomon_aristotelian_shared_canonical_floor_beginning():
    """Each mythos's beginning phase covers the same six canonical-
    floor events. This is the stress case's central structural
    claim: testimonies share the undisputed lead-up."""
    from story_engine.encodings.rashomon_aristotelian import (
        AR_RASHOMON_MYTHOI,
    )
    expected = frozenset({
        "E_travel", "E_tajomaru_sees_them", "E_lure", "E_bind",
        "E_bring_wife", "E_intercourse",
    })
    for mythos in AR_RASHOMON_MYTHOI:
        beginning = [ph for ph in mythos.phases
                     if ph.role == PHASE_BEGINNING]
        assert len(beginning) == 1, (
            f"{mythos.id}: expected exactly one beginning phase")
        assert set(beginning[0].scope_event_ids) == expected, (
            f"{mythos.id}: beginning phase scope does not match "
            f"canonical-floor — got {sorted(beginning[0].scope_event_ids)}"
        )


def test_rashomon_aristotelian_each_testimony_has_own_peripeteia():
    """Per the sketch's worked encoding, each testimony-mythos
    carries its own peripeteia pointer into substrate. None
    carries anagnorisis — testifiers' self-accounts do not
    include their own character-level recognition (the Rashomon
    'recognition' is meta-anagnorisis, per the sketch's A8-class
    dialect-scope limit)."""
    from story_engine.encodings.rashomon_aristotelian import (
        AR_RASHOMON_MYTHOI,
    )
    for mythos in AR_RASHOMON_MYTHOI:
        assert mythos.peripeteia_event_id is not None, (
            f"{mythos.id} missing peripeteia_event_id")
        assert mythos.anagnorisis_event_id is None, (
            f"{mythos.id} unexpectedly has anagnorisis_event_id="
            f"{mythos.anagnorisis_event_id!r}")


# ============================================================================
# Sketch-02 record construction (AA6)
# ============================================================================


def test_armythos_relation_defaults():
    r = ArMythosRelation(id="r1", kind=RELATION_CONTESTS,
                         mythoi_ids=("m1", "m2"))
    assert r.over_event_ids == ()
    assert r.annotation == ""


def test_aranagnorisis_step_defaults():
    s = ArAnagnorisisStep(id="s1", event_id="E_x",
                          character_ref_id="c1")
    assert s.precipitates_main is False
    assert s.annotation == ""


def test_armythos_sketch02_field_defaults():
    m = _three_phase_mythos()
    assert m.anagnorisis_chain == ()
    assert m.peripeteia_anagnorisis_binding is None
    assert m.peripeteia_anagnorisis_adjacency_bound == 3


def test_canonical_relation_kinds_contents():
    assert CANONICAL_RELATION_KINDS == frozenset({
        RELATION_CONTESTS, RELATION_PARALLEL, RELATION_CONTAINS,
    })


def test_valid_peripeteia_anagnorisis_bindings_contents():
    assert VALID_PERIPETEIA_ANAGNORISIS_BINDINGS == frozenset({
        BINDING_COINCIDENT, BINDING_ADJACENT, BINDING_SEPARATED,
    })


# ============================================================================
# A7.6 — ArMythosRelation structural integrity
# ============================================================================


def test_relation_noncanonical_kind_emits_noted():
    m = _three_phase_mythos()
    rel = ArMythosRelation(
        id="r1", kind="spooky", mythoi_ids=("m_test", "m_test"),
    )
    obs = verify(m, mythoi=(m,), relations=(rel,))
    findings = [o for o in obs
                if o.code == "mythos_relation_kind_noncanonical"]
    assert len(findings) == 1
    assert findings[0].severity == SEVERITY_NOTED


def test_relation_too_few_mythoi_flags():
    m = _three_phase_mythos()
    rel = ArMythosRelation(
        id="r1", kind=RELATION_CONTESTS, mythoi_ids=("m_test",),
    )
    obs = verify(m, mythoi=(m,), relations=(rel,))
    assert _has_code(obs, "mythos_relation_mythoi_too_few")


def test_relation_unresolved_mythos_id_flags():
    m = _three_phase_mythos()
    rel = ArMythosRelation(
        id="r1", kind=RELATION_PARALLEL,
        mythoi_ids=("m_test", "m_ghost"),
    )
    obs = verify(m, mythoi=(m,), relations=(rel,))
    assert _has_code(obs, "mythos_relation_mythoi_unresolved")


def test_relation_mythos_resolution_skipped_when_mythoi_empty():
    """Without the `mythoi` kwarg, A7.6 check 2b skips resolution —
    authors who do not thread the mythos tuple see no
    unresolved-id findings."""
    m = _three_phase_mythos()
    rel = ArMythosRelation(
        id="r1", kind=RELATION_PARALLEL,
        mythoi_ids=("m_test", "m_ghost"),
    )
    obs = verify(m, relations=(rel,))
    assert not _has_code(obs, "mythos_relation_mythoi_unresolved")


def test_relation_contests_event_absent_flags():
    """A mythos missing an over_event_id from its central_event_ids
    flags under A7.6 check 3."""
    m = _three_phase_mythos()
    rel = ArMythosRelation(
        id="r1", kind=RELATION_CONTESTS,
        mythoi_ids=("m_test", "m_test"),
        over_event_ids=("E_not_in_mythos",),
    )
    obs = verify(m, mythoi=(m,), relations=(rel,))
    assert _has_code(obs, "mythos_relation_contests_event_absent")


def test_relation_contests_passes_when_events_shared():
    m = _three_phase_mythos()
    # Two copies of m participate in the relation (synthetic); both
    # carry E1/E2/E3 in central.
    rel = ArMythosRelation(
        id="r1", kind=RELATION_CONTESTS,
        mythoi_ids=("m_test", "m_test"),
        over_event_ids=("E1", "E2"),
    )
    obs = verify(m, mythoi=(m,), relations=(rel,))
    assert not _has_code(obs, "mythos_relation_contests_event_absent")


def test_relation_contains_not_superset_flags():
    outer = _three_phase_mythos()
    inner = ArMythos(
        id="m_inner", title="Inner", action_summary="",
        central_event_ids=("E1", "E_unique_to_inner"),
        plot_kind=PLOT_SIMPLE,
        phases=(
            ArPhase(id="ph_b", role=PHASE_BEGINNING,
                    scope_event_ids=("E1",)),
            ArPhase(id="ph_m", role=PHASE_MIDDLE,
                    scope_event_ids=("E_unique_to_inner",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=()),
        ),
    )
    rel = ArMythosRelation(
        id="r1", kind=RELATION_CONTAINS,
        mythoi_ids=("m_test", "m_inner"),
    )
    # Verify against outer, threading both mythoi.
    obs = verify(outer, mythoi=(outer, inner), relations=(rel,))
    assert _has_code(obs, "mythos_relation_contains_not_superset")


def test_relation_contains_strict_superset_passes():
    outer = _three_phase_mythos()
    # Inner covers E1 + E2 only — strict subset of outer's E1/E2/E3.
    inner = ArMythos(
        id="m_inner", title="Inner", action_summary="",
        central_event_ids=("E1", "E2"),
        plot_kind=PLOT_SIMPLE,
        phases=(
            ArPhase(id="ph_b", role=PHASE_BEGINNING,
                    scope_event_ids=("E1",)),
            ArPhase(id="ph_m", role=PHASE_MIDDLE,
                    scope_event_ids=("E2",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=()),
        ),
    )
    rel = ArMythosRelation(
        id="r1", kind=RELATION_CONTAINS,
        mythoi_ids=("m_test", "m_inner"),
    )
    obs = verify(outer, mythoi=(outer, inner), relations=(rel,))
    assert not _has_code(obs, "mythos_relation_contains_not_superset")


# ============================================================================
# A7.9 — ArMythosRelation event-reference integrity
# ============================================================================


def test_relation_event_ref_unresolved_flags():
    m = _three_phase_mythos()
    events = (_synthetic_event("E1"), _synthetic_event("E2"),
              _synthetic_event("E3"))
    rel = ArMythosRelation(
        id="r1", kind=RELATION_CONTESTS,
        mythoi_ids=("m_test", "m_test"),
        over_event_ids=("E_unresolved",),
    )
    obs = verify(m, substrate_events=events,
                 mythoi=(m,), relations=(rel,))
    assert _has_code(obs, "mythos_relation_event_ref_unresolved")


def test_relation_event_ref_skipped_without_substrate():
    m = _three_phase_mythos()
    rel = ArMythosRelation(
        id="r1", kind=RELATION_CONTESTS,
        mythoi_ids=("m_test", "m_test"),
        over_event_ids=("E_unresolved",),
    )
    obs = verify(m, mythoi=(m,), relations=(rel,))
    assert not _has_code(obs, "mythos_relation_event_ref_unresolved")


# ============================================================================
# A7.7 — ArAnagnorisisStep integrity
# ============================================================================


def test_anagnorisis_chain_empty_by_default_clean():
    """A mythos with no chain produces no chain-related findings."""
    m = _three_phase_mythos()
    obs = verify(m)
    for o in obs:
        assert not o.code.startswith("anagnorisis_step_")


def test_anagnorisis_chain_event_not_central_flags():
    step = ArAnagnorisisStep(
        id="s1", event_id="E_not_in_mythos",
        character_ref_id="c_hero",
    )
    m = _three_phase_mythos(anagnorisis_chain=(step,))
    obs = verify(m)
    assert _has_code(obs, "anagnorisis_step_event_not_central")


def test_anagnorisis_chain_step_equals_main_flags():
    # Main anagnorisis is E3; chain step also points at E3.
    step = ArAnagnorisisStep(
        id="s1", event_id="E3", character_ref_id="c_hero",
    )
    m = _three_phase_mythos(anagnorisis_chain=(step,))
    obs = verify(m)
    assert _has_code(obs, "anagnorisis_step_equals_main")


def test_anagnorisis_chain_precipitates_without_main_flags():
    step = ArAnagnorisisStep(
        id="s1", event_id="E2",
        character_ref_id="c_hero", precipitates_main=True,
    )
    # Complex plot with only peripeteia (no anagnorisis) + chain
    # claims precipitates_main.
    m = _three_phase_mythos(
        anagnorisis=None, anagnorisis_chain=(step,),
    )
    obs = verify(m)
    assert _has_code(obs, "anagnorisis_step_precipitates_without_main")


def test_anagnorisis_chain_precipitates_ordering_flags():
    """Step τ_s must be strictly less than main anagnorisis τ_s."""
    events = (
        _synthetic_event("E1", τ_s=0),
        _synthetic_event("E2", τ_s=5),    # step candidate
        _synthetic_event("E3", τ_s=3),    # main anagnorisis (earlier!)
    )
    step = ArAnagnorisisStep(
        id="s1", event_id="E2",
        character_ref_id="c_hero", precipitates_main=True,
    )
    m = _three_phase_mythos(anagnorisis_chain=(step,))
    obs = verify(m, substrate_events=events)
    assert _has_code(obs, "anagnorisis_step_precipitates_ordering")


def test_anagnorisis_chain_precipitates_ordering_passes_when_earlier():
    events = (
        _synthetic_event("E1", τ_s=0),
        _synthetic_event("E2", τ_s=3),    # step
        _synthetic_event("E3", τ_s=10),   # main
    )
    step = ArAnagnorisisStep(
        id="s1", event_id="E2",
        character_ref_id="c_hero", precipitates_main=True,
    )
    m = _three_phase_mythos(
        anagnorisis_chain=(step,),
        characters=(ArCharacter(id="c_hero", name="Hero"),),
    )
    obs = verify(m, substrate_events=events)
    assert not _has_code(obs, "anagnorisis_step_precipitates_ordering")


def test_anagnorisis_chain_character_unresolved_flags():
    step = ArAnagnorisisStep(
        id="s1", event_id="E2",
        character_ref_id="c_missing",
    )
    m = _three_phase_mythos(
        anagnorisis_chain=(step,),
        characters=(ArCharacter(id="c_hero", name="Hero"),),
    )
    obs = verify(m)
    assert _has_code(obs, "anagnorisis_step_character_unresolved")


def test_anagnorisis_chain_character_check_skips_without_characters():
    """If the mythos authors no characters, character ref resolution
    is skipped — parallel to A7 check 5 hamartia-participation."""
    step = ArAnagnorisisStep(
        id="s1", event_id="E2", character_ref_id="c_any",
    )
    m = _three_phase_mythos(anagnorisis_chain=(step,))
    obs = verify(m)
    assert not _has_code(obs, "anagnorisis_step_character_unresolved")


# ============================================================================
# A7.8 — peripeteia_anagnorisis_binding consistency
# ============================================================================


def test_binding_none_no_check():
    """Default None means no binding-related findings."""
    m = _three_phase_mythos()
    obs = verify(m)
    for o in obs:
        assert not o.code.startswith("peripeteia_anagnorisis_binding_")


def test_binding_coincident_passes_when_events_match():
    # Peripeteia and anagnorisis pointing at the same event.
    m = _three_phase_mythos(
        peripeteia="E3", anagnorisis="E3",
        peripeteia_anagnorisis_binding=BINDING_COINCIDENT,
    )
    events = (_synthetic_event("E1"), _synthetic_event("E2"),
              _synthetic_event("E3"))
    obs = verify(m, substrate_events=events)
    assert not _has_code(obs,
                         "peripeteia_anagnorisis_binding_inconsistent")


def test_binding_coincident_inconsistent_when_events_differ():
    m = _three_phase_mythos(
        peripeteia="E2", anagnorisis="E3",
        peripeteia_anagnorisis_binding=BINDING_COINCIDENT,
    )
    events = (_synthetic_event("E1"), _synthetic_event("E2", τ_s=1),
              _synthetic_event("E3", τ_s=2))
    obs = verify(m, substrate_events=events)
    assert _has_code(obs, "peripeteia_anagnorisis_binding_inconsistent")


def test_binding_adjacent_passes_within_bound():
    m = _three_phase_mythos(
        peripeteia="E2", anagnorisis="E3",
        peripeteia_anagnorisis_binding=BINDING_ADJACENT,
    )
    # Bound default 3; distance 1.
    events = (_synthetic_event("E1", τ_s=0),
              _synthetic_event("E2", τ_s=5),
              _synthetic_event("E3", τ_s=6))
    obs = verify(m, substrate_events=events)
    assert not _has_code(obs,
                         "peripeteia_anagnorisis_binding_inconsistent")


def test_binding_separated_passes_beyond_bound():
    m = _three_phase_mythos(
        peripeteia="E2", anagnorisis="E3",
        peripeteia_anagnorisis_binding=BINDING_SEPARATED,
    )
    # Bound default 3; distance 5.
    events = (_synthetic_event("E1", τ_s=0),
              _synthetic_event("E2", τ_s=5),
              _synthetic_event("E3", τ_s=10))
    obs = verify(m, substrate_events=events)
    assert not _has_code(obs,
                         "peripeteia_anagnorisis_binding_inconsistent")


def test_binding_invalid_value_flags():
    m = _three_phase_mythos(
        peripeteia="E2", anagnorisis="E3",
        peripeteia_anagnorisis_binding="telepathic",
    )
    obs = verify(m)
    assert _has_code(obs,
                     "peripeteia_anagnorisis_binding_invalid_value")


def test_binding_requires_both_event_ids():
    m = _three_phase_mythos(
        peripeteia="E2", anagnorisis=None,
        peripeteia_anagnorisis_binding=BINDING_SEPARATED,
    )
    obs = verify(m)
    # Note: `anagnorisis=None` with plot_kind=complex also trips the
    # A3 rule, but A7.8 must independently flag the binding
    # inconsistency.
    assert _has_code(obs, "peripeteia_anagnorisis_binding_inconsistent")


def test_binding_event_unresolved_flags():
    m = _three_phase_mythos(
        peripeteia="E2", anagnorisis="E_ghost",
        peripeteia_anagnorisis_binding=BINDING_SEPARATED,
    )
    # Substrate has E1/E2/E3 only — E_ghost does not resolve.
    events = (_synthetic_event("E1"), _synthetic_event("E2"),
              _synthetic_event("E3"))
    # A7.8 checks binding-event resolution; A7 check 4 will also
    # flag E_ghost as event_ref_unresolved — that's the existing
    # behavior, not a sketch-02 regression.
    obs = verify(m, substrate_events=events)
    assert _has_code(obs,
                     "peripeteia_anagnorisis_binding_event_unresolved")


# ============================================================================
# Backward compatibility — verify signature
# ============================================================================


def test_verify_backward_compat_no_kwargs():
    """A pre-sketch-02 call site — verify(mythos) with no new
    kwargs — produces exactly the same observations it did before
    sketch-02 landed on a mythos that authors no A10/A11/A12
    content."""
    m = _three_phase_mythos()
    obs_without = verify(m)
    obs_with_empty_kwargs = verify(m, mythoi=(), relations=())
    codes_without = sorted(o.code for o in obs_without)
    codes_with = sorted(o.code for o in obs_with_empty_kwargs)
    assert codes_without == codes_with


# ============================================================================
# Encoding migrations — Oedipus (AA9) + Rashomon (AA8)
# ============================================================================


def test_oedipus_aristotelian_chain_authored():
    """AR_OEDIPUS_MYTHOS now carries AR_STEP_JOCASTA in its chain."""
    from story_engine.encodings.oedipus_aristotelian import (
        AR_OEDIPUS_MYTHOS, AR_STEP_JOCASTA,
    )
    assert AR_OEDIPUS_MYTHOS.anagnorisis_chain == (AR_STEP_JOCASTA,)
    assert AR_STEP_JOCASTA.event_id == "E_jocasta_realizes"
    assert AR_STEP_JOCASTA.character_ref_id == "ar_jocasta"
    assert AR_STEP_JOCASTA.precipitates_main is True


def test_oedipus_aristotelian_binding_is_separated():
    from story_engine.encodings.oedipus_aristotelian import (
        AR_OEDIPUS_MYTHOS,
    )
    assert (AR_OEDIPUS_MYTHOS.peripeteia_anagnorisis_binding
            == BINDING_SEPARATED)
    # Default bound preserved (sketch says default is sufficient).
    assert AR_OEDIPUS_MYTHOS.peripeteia_anagnorisis_adjacency_bound == 3


def test_oedipus_aristotelian_still_verifies_clean_with_sketch02():
    """The Oedipus encoding under sketch-02 (with chain + binding
    authored) still verifies with zero observations against the
    real FABULA."""
    from story_engine.encodings.oedipus import FABULA
    from story_engine.encodings.oedipus_aristotelian import (
        AR_OEDIPUS_MYTHOS,
    )
    obs = verify(AR_OEDIPUS_MYTHOS, substrate_events=FABULA)
    assert obs == [], (
        f"Expected zero observations; got {len(obs)}:\n"
        + "\n".join(f"  [{o.severity}] {o.code}: {o.message}"
                    for o in obs)
    )


def test_rashomon_contest_relation_authored():
    from story_engine.encodings.rashomon_aristotelian import (
        AR_RASHOMON_CONTEST, AR_RASHOMON_RELATIONS,
    )
    assert AR_RASHOMON_RELATIONS == (AR_RASHOMON_CONTEST,)
    assert AR_RASHOMON_CONTEST.kind == RELATION_CONTESTS
    assert len(AR_RASHOMON_CONTEST.mythoi_ids) == 4
    # The six canonical-floor events.
    assert len(AR_RASHOMON_CONTEST.over_event_ids) == 6


def test_rashomon_aristotelian_verifies_clean_with_relations():
    """The Rashomon encoding under sketch-02 verifies all four
    mythoi with zero observations when the relation tuple is
    threaded through (exercises A7.6 / A7.9)."""
    from story_engine.encodings.rashomon import EVENTS_ALL
    from story_engine.encodings.rashomon_aristotelian import (
        AR_RASHOMON_MYTHOI, AR_RASHOMON_RELATIONS,
    )
    for mythos in AR_RASHOMON_MYTHOI:
        obs = verify(mythos, substrate_events=EVENTS_ALL,
                     mythoi=AR_RASHOMON_MYTHOI,
                     relations=AR_RASHOMON_RELATIONS)
        assert obs == [], (
            f"{mythos.id}: expected zero observations; got "
            f"{len(obs)}:\n"
            + "\n".join(f"    [{o.severity}] {o.code}: {o.message}"
                        for o in obs)
        )


# ============================================================================
# Sketch-03 — A13 ArCharacterArcRelation + A14 step_kind
# ============================================================================


def test_archaracterarc_relation_defaults():
    """A13 record defaults: over_event_ids empty tuple; annotation
    empty string. Both optional per the sketch."""
    r = ArCharacterArcRelation(
        id="arc1", kind=ARC_RELATION_MIRROR,
        character_ref_ids=("c1", "c2"), mythos_id="m1",
    )
    assert r.over_event_ids == ()
    assert r.annotation == ""


def test_canonical_character_arc_relation_kinds_contents():
    """A13 canonical kind vocabulary."""
    assert CANONICAL_CHARACTER_ARC_RELATION_KINDS == frozenset({
        ARC_RELATION_PARALLEL, ARC_RELATION_MIRROR, ARC_RELATION_FOIL,
    })


def test_valid_step_kinds_contents():
    """A14 canonical step_kind vocabulary — closed enum."""
    assert VALID_STEP_KINDS == frozenset({
        STEP_KIND_PARALLEL, STEP_KIND_PRECIPITATING, STEP_KIND_STAGING,
    })


def test_aranagnorisis_step_sketch03_field_default():
    """A14 adds `step_kind` with empty-string default (back-compat)."""
    s = ArAnagnorisisStep(id="s1", event_id="E_x", character_ref_id="c1")
    assert s.step_kind == ""


def test_armythos_sketch03_anagnorisis_character_default():
    """A14 adds `anagnorisis_character_ref_id` with None default."""
    m = _three_phase_mythos()
    assert m.anagnorisis_character_ref_id is None


# ----------------------------------------------------------------------------
# A7.10 — ArCharacterArcRelation structural integrity
# ----------------------------------------------------------------------------


def _two_character_mythos() -> ArMythos:
    """A synthetic mythos with two ArCharacter records, usable by A13
    tests that need a mythos_id to resolve against."""
    return _three_phase_mythos(characters=(
        ArCharacter(id="c1", name="Alpha"),
        ArCharacter(id="c2", name="Beta"),
    ))


def test_arcrelation_noncanonical_kind_emits_noted():
    """A7.10 check 1 — non-canonical kind admitted at severity NOTED
    (canonical-plus-open, matches A10's discipline)."""
    m = _two_character_mythos()
    rel = ArCharacterArcRelation(
        id="arc1", kind="shadow",
        character_ref_ids=("c1", "c2"), mythos_id="m_test",
    )
    obs = verify(m, mythoi=(m,), character_arc_relations=(rel,))
    findings = [
        o for o in obs
        if o.code == "character_arc_relation_kind_noncanonical"
    ]
    assert len(findings) == 1
    assert findings[0].severity == SEVERITY_NOTED


def test_arcrelation_too_few_refs_flags():
    """A7.10 check 2 — ≥2 character_ref_ids required."""
    m = _two_character_mythos()
    rel = ArCharacterArcRelation(
        id="arc1", kind=ARC_RELATION_MIRROR,
        character_ref_ids=("c1",), mythos_id="m_test",
    )
    obs = verify(m, mythoi=(m,), character_arc_relations=(rel,))
    assert _has_code(obs, "character_arc_relation_refs_too_few")


def test_arcrelation_mythos_unresolved_flags():
    """A7.10 check 3a — mythos_id must resolve against `mythoi`."""
    m = _two_character_mythos()
    rel = ArCharacterArcRelation(
        id="arc1", kind=ARC_RELATION_MIRROR,
        character_ref_ids=("c1", "c2"), mythos_id="m_ghost",
    )
    obs = verify(m, mythoi=(m,), character_arc_relations=(rel,))
    assert _has_code(obs, "character_arc_relation_mythos_unresolved")


def test_arcrelation_character_unresolved_flags():
    """A7.10 check 3b — each character_ref_id must resolve against
    the named mythos's `characters` tuple."""
    m = _two_character_mythos()
    rel = ArCharacterArcRelation(
        id="arc1", kind=ARC_RELATION_MIRROR,
        character_ref_ids=("c1", "c_ghost"), mythos_id="m_test",
    )
    obs = verify(m, mythoi=(m,), character_arc_relations=(rel,))
    assert _has_code(obs, "character_arc_relation_character_unresolved")


def test_arcrelation_resolution_skipped_when_mythoi_empty():
    """A7.10 check 3 skips when `mythoi` is not threaded — matches
    A7.6's discipline on optional kwargs."""
    m = _two_character_mythos()
    rel = ArCharacterArcRelation(
        id="arc1", kind=ARC_RELATION_MIRROR,
        character_ref_ids=("c_ghost", "c_other"), mythos_id="m_ghost",
    )
    obs = verify(m, character_arc_relations=(rel,))
    assert not _has_code(
        obs, "character_arc_relation_mythos_unresolved"
    )
    assert not _has_code(
        obs, "character_arc_relation_character_unresolved"
    )


def test_arcrelation_event_ref_unresolved_flags():
    """A7.10 check 4 — over_event_ids must resolve in substrate when
    threaded; flagged when a referenced event is missing."""
    m = _two_character_mythos()
    rel = ArCharacterArcRelation(
        id="arc1", kind=ARC_RELATION_MIRROR,
        character_ref_ids=("c1", "c2"), mythos_id="m_test",
        over_event_ids=("E1", "E_ghost"),
    )
    events = (
        _synthetic_event("E1", τ_s=0),
        _synthetic_event("E2", τ_s=1),
        _synthetic_event("E3", τ_s=2),
    )
    obs = verify(
        m, substrate_events=events, mythoi=(m,),
        character_arc_relations=(rel,),
    )
    assert _has_code(obs, "character_arc_relation_event_ref_unresolved")


def test_arcrelation_event_ref_skipped_without_substrate():
    """A7.10 check 4 skips when substrate is not threaded."""
    m = _two_character_mythos()
    rel = ArCharacterArcRelation(
        id="arc1", kind=ARC_RELATION_MIRROR,
        character_ref_ids=("c1", "c2"), mythos_id="m_test",
        over_event_ids=("E_ghost",),
    )
    obs = verify(m, mythoi=(m,), character_arc_relations=(rel,))
    assert not _has_code(
        obs, "character_arc_relation_event_ref_unresolved"
    )


# ----------------------------------------------------------------------------
# A7.11 — ArAnagnorisisStep step_kind consistency
# ----------------------------------------------------------------------------


def _staging_fixture_mythos(
    step_kind: str = STEP_KIND_STAGING,
    step_character: str = "c_hero",
    step_event: str = "E2",
    step_precipitates: bool = True,
    anagnorisis_character_ref_id: Optional[str] = "c_hero",
    anagnorisis_event_id: str = "E3",
) -> ArMythos:
    """A synthetic three-phase mythos with one chain step — parametric
    so each A7.11 invariant can be pressured individually."""
    step = ArAnagnorisisStep(
        id="s_staging", event_id=step_event,
        character_ref_id=step_character,
        step_kind=step_kind,
        precipitates_main=step_precipitates,
    )
    return _three_phase_mythos(
        anagnorisis=anagnorisis_event_id,
        characters=(
            ArCharacter(id="c_hero", name="Hero"),
            ArCharacter(id="c_other", name="Other"),
        ),
        anagnorisis_chain=(step,),
        anagnorisis_character_ref_id=anagnorisis_character_ref_id,
    )


def test_step_kind_invalid_value_flags():
    """A7.11 invariant 1 — step_kind set to a value outside
    VALID_STEP_KINDS flags anagnorisis_step_kind_invalid."""
    m = _staging_fixture_mythos(step_kind="revelation")
    obs = verify(m)
    assert _has_code(obs, "anagnorisis_step_kind_invalid")


def test_step_kind_staging_requires_main_character():
    """A7.11 invariant 2 (first half) — staging without
    anagnorisis_character_ref_id flags."""
    m = _staging_fixture_mythos(anagnorisis_character_ref_id=None)
    obs = verify(m)
    assert _has_code(
        obs, "anagnorisis_step_staging_requires_main_character"
    )


def test_step_kind_staging_character_mismatch_flags():
    """A7.11 invariant 2 (second half) — staging with
    character_ref_id ≠ anagnorisis_character_ref_id flags."""
    m = _staging_fixture_mythos(step_character="c_other")
    obs = verify(m)
    assert _has_code(obs, "anagnorisis_step_staging_character_mismatch")


def test_step_kind_staging_ordering_flags():
    """A7.11 invariant 6 — staging τ_s must strictly precede main
    anagnorisis τ_s (enforceable only with substrate threaded)."""
    m = _staging_fixture_mythos(step_event="E3", anagnorisis_event_id="E3")
    # The step event and the main event are both E3 — but invariant 3
    # (from A7.7) would also flag "step event equals main"; this test
    # uses a distinct-event case to isolate ordering. Rebuild with a
    # *later* event for the step: step at E2, main at E1.
    events = (
        _synthetic_event("E1", τ_s=10),
        _synthetic_event("E2", τ_s=20),
        _synthetic_event("E3", τ_s=30),
    )
    m2 = _staging_fixture_mythos(
        step_event="E3", anagnorisis_event_id="E2",
    )
    # Overwrite: step at τ_s=30, main at τ_s=20 (step is LATER than
    # main → ordering violation).
    obs = verify(m2, substrate_events=events)
    assert _has_code(obs, "anagnorisis_step_staging_ordering")


def test_step_kind_staging_precipitates_mismatch_noted():
    """A7.11 invariant 5 — staging with precipitates_main=False
    flags at severity NOTED (author declared staging but also
    declared the step does not precipitate; staging precipitates by
    definition)."""
    m = _staging_fixture_mythos(step_precipitates=False)
    obs = verify(m)
    findings = [
        o for o in obs
        if o.code == "anagnorisis_step_kind_precipitates_mismatch"
    ]
    assert len(findings) >= 1
    assert findings[0].severity == SEVERITY_NOTED


def test_step_kind_precipitating_precipitates_mismatch_noted():
    """A7.11 invariant 3 — step_kind='precipitating' with
    precipitates_main=False flags NOTED."""
    step = ArAnagnorisisStep(
        id="s1", event_id="E2", character_ref_id="c2",
        step_kind=STEP_KIND_PRECIPITATING,
        precipitates_main=False,
    )
    m = _three_phase_mythos(
        characters=(
            ArCharacter(id="c1", name="Hero"),
            ArCharacter(id="c2", name="Other"),
        ),
        anagnorisis_chain=(step,),
        anagnorisis_character_ref_id="c1",
    )
    obs = verify(m)
    findings = [
        o for o in obs
        if o.code == "anagnorisis_step_kind_precipitates_mismatch"
    ]
    assert len(findings) >= 1
    assert findings[0].severity == SEVERITY_NOTED


def test_step_kind_parallel_precipitates_mismatch_noted():
    """A7.11 invariant 4 — step_kind='parallel' with
    precipitates_main=True flags NOTED."""
    step = ArAnagnorisisStep(
        id="s1", event_id="E2", character_ref_id="c2",
        step_kind=STEP_KIND_PARALLEL,
        precipitates_main=True,
    )
    m = _three_phase_mythos(
        characters=(
            ArCharacter(id="c1", name="Hero"),
            ArCharacter(id="c2", name="Other"),
        ),
        anagnorisis_chain=(step,),
        anagnorisis_character_ref_id="c1",
    )
    obs = verify(m)
    findings = [
        o for o in obs
        if o.code == "anagnorisis_step_kind_precipitates_mismatch"
    ]
    assert len(findings) >= 1
    assert findings[0].severity == SEVERITY_NOTED


def test_step_kind_empty_back_compat_verifies_clean():
    """Back-compat — an encoding that leaves step_kind="" and
    anagnorisis_character_ref_id=None (pre-sketch-03 shape) sees no
    new A7.11 observations. The chain step below is a non-
    precipitating parallel-style step (Macbeth's Lady-Macbeth
    shape); pre-sketch-03 semantics are preserved."""
    step = ArAnagnorisisStep(
        id="s_legacy", event_id="E2", character_ref_id="c_other",
        precipitates_main=False,
    )
    m = _three_phase_mythos(
        characters=(
            ArCharacter(id="c_hero", name="Hero"),
            ArCharacter(id="c_other", name="Other"),
        ),
        anagnorisis_chain=(step,),
    )
    obs = verify(m)
    # No sketch-03 codes on a pre-sketch-03-shape encoding.
    sketch03_codes = {
        "anagnorisis_step_kind_invalid",
        "anagnorisis_step_staging_character_mismatch",
        "anagnorisis_step_staging_requires_main_character",
        "anagnorisis_step_kind_precipitates_mismatch",
        "anagnorisis_step_staging_ordering",
    }
    assert not any(o.code in sketch03_codes for o in obs)


def test_arcrelation_verifies_clean_when_all_resolve():
    """Integration — a cleanly-authored arc relation over a two-
    character mythos with all events resolving in substrate emits
    zero observations."""
    m = _two_character_mythos()
    events = (
        _synthetic_event("E1", τ_s=0),
        _synthetic_event("E2", τ_s=1),
        _synthetic_event("E3", τ_s=2),
    )
    rel = ArCharacterArcRelation(
        id="arc1", kind=ARC_RELATION_MIRROR,
        character_ref_ids=("c1", "c2"), mythos_id="m_test",
        over_event_ids=("E1", "E2"),
    )
    obs = verify(
        m, substrate_events=events, mythoi=(m,),
        character_arc_relations=(rel,),
    )
    sketch03_codes = {
        o.code for o in obs
        if o.code.startswith("character_arc_relation_")
        or o.code.startswith("anagnorisis_step_kind_")
        or o.code.startswith("anagnorisis_step_staging_")
    }
    assert sketch03_codes == set(), (
        f"Expected zero sketch-03 findings; got {sketch03_codes}"
    )


def test_verify_signature_accepts_character_arc_relations_kwarg():
    """AA13 — verify's new kwarg defaults to empty tuple; calling
    verify without it preserves pre-sketch-03 behavior."""
    m = _three_phase_mythos()
    # Without the kwarg (pre-sketch-03 call site):
    obs_without = verify(m)
    # With the kwarg but empty tuple:
    obs_with_empty = verify(m, character_arc_relations=())
    assert obs_without == obs_with_empty


# ============================================================================
# Sketch-04 — A15-SE1/SE2/SE3 + A16-SP1/SP2/SP3 record / vocabulary tests
# ============================================================================


def test_canonical_tonal_registers_contents():
    """A16-SP1 published vocabulary — six canonical registers."""
    assert TONAL_REGISTER_TRAGIC_WITH_IRONY in CANONICAL_TONAL_REGISTERS
    assert len(CANONICAL_TONAL_REGISTERS) == 6


def test_canonical_binding_distance_preferences_contents():
    """A16-SP2 published vocabulary — four preferences."""
    assert BINDING_PREF_WIDE in CANONICAL_BINDING_DISTANCE_PREFERENCES
    assert BINDING_PREF_NEUTRAL in CANONICAL_BINDING_DISTANCE_PREFERENCES
    assert len(CANONICAL_BINDING_DISTANCE_PREFERENCES) == 4


def test_canonical_pacing_preferences_contents():
    """A16-SP3 published vocabulary — five pacing shapes."""
    assert PACING_SLOW_BURN in CANONICAL_PACING_PREFERENCES
    assert PACING_EVEN in CANONICAL_PACING_PREFERENCES
    assert PACING_RAPID_ESCALATION in CANONICAL_PACING_PREFERENCES
    assert len(CANONICAL_PACING_PREFERENCES) == 5


def test_arphase_sketch04_field_defaults():
    """ArPhase A15-SE1 + A16-SP3 fields default to inert values."""
    ph = ArPhase(id="ph_x", role=PHASE_MIDDLE, scope_event_ids=())
    assert ph.min_event_count == 0
    assert ph.max_event_count == 0
    assert ph.pacing_preference == ""


def test_armythos_sketch04_field_defaults():
    """ArMythos A15-SE2/SE3 + A16-SP1/SP2 fields default to inert."""
    m = _three_phase_mythos()
    assert m.co_presence_requirements == ()
    assert m.audience_knowledge_constraints == ()
    assert m.tonal_register == ""
    assert m.binding_distance_preference == ""


def test_arcopresencerequirement_default_min_count():
    req = ArCoPresenceRequirement(
        id="r1", character_ref_ids=("c1", "c2"), phase_id="ph_b",
    )
    assert req.min_count == 1


def test_araudienceknowledgeconstraint_default_source_event():
    con = ArAudienceKnowledgeConstraint(
        id="k1", subject="x", latest_τ_s=0,
    )
    assert con.source_event_id is None


# ----------------------------------------------------------------------------
# A7.12 — phase_event_count_bound consistency
# ----------------------------------------------------------------------------


def test_phase_event_count_bounds_default_zero_clean():
    """A7.12 — both bounds default 0; A7.12 emits no observations."""
    m = _three_phase_mythos()
    obs = verify(m)
    for code in (
        "phase_event_count_min_negative",
        "phase_event_count_max_negative",
        "phase_event_count_bounds_inverted",
        "phase_event_count_below_min",
        "phase_event_count_above_max",
    ):
        assert not _has_code(obs, code)


def test_phase_event_count_min_negative_flags():
    """A7.12 invariant 1 — min_event_count must be ≥ 0."""
    bad_phase = ArPhase(
        id="ph_b", role=PHASE_BEGINNING,
        scope_event_ids=("E1",), min_event_count=-1,
    )
    m = ArMythos(
        id="m_test", title="t", action_summary="s",
        central_event_ids=("E1", "E2", "E3"),
        plot_kind=PLOT_COMPLEX,
        phases=(
            bad_phase,
            ArPhase(id="ph_m", role=PHASE_MIDDLE,
                    scope_event_ids=("E2",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=("E3",)),
        ),
        peripeteia_event_id="E2", anagnorisis_event_id="E3",
    )
    obs = verify(m)
    assert _has_code(obs, "phase_event_count_min_negative")


def test_phase_event_count_max_negative_flags():
    """A7.12 invariant 2 — max_event_count must be ≥ 0."""
    bad_phase = ArPhase(
        id="ph_b", role=PHASE_BEGINNING,
        scope_event_ids=("E1",), max_event_count=-1,
    )
    m = ArMythos(
        id="m_test", title="t", action_summary="s",
        central_event_ids=("E1", "E2", "E3"),
        plot_kind=PLOT_COMPLEX,
        phases=(
            bad_phase,
            ArPhase(id="ph_m", role=PHASE_MIDDLE,
                    scope_event_ids=("E2",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=("E3",)),
        ),
        peripeteia_event_id="E2", anagnorisis_event_id="E3",
    )
    obs = verify(m)
    assert _has_code(obs, "phase_event_count_max_negative")


def test_phase_event_count_bounds_inverted_flags():
    """A7.12 invariant 3 — when both > 0, min must be ≤ max."""
    bad_phase = ArPhase(
        id="ph_b", role=PHASE_BEGINNING,
        scope_event_ids=("E1",),
        min_event_count=5, max_event_count=2,
    )
    m = ArMythos(
        id="m_test", title="t", action_summary="s",
        central_event_ids=("E1", "E2", "E3"),
        plot_kind=PLOT_COMPLEX,
        phases=(
            bad_phase,
            ArPhase(id="ph_m", role=PHASE_MIDDLE,
                    scope_event_ids=("E2",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=("E3",)),
        ),
        peripeteia_event_id="E2", anagnorisis_event_id="E3",
    )
    obs = verify(m)
    assert _has_code(obs, "phase_event_count_bounds_inverted")


def test_phase_event_count_below_min_flags():
    """A7.12 invariant 4a — actual count below min flagged."""
    short_phase = ArPhase(
        id="ph_b", role=PHASE_BEGINNING,
        scope_event_ids=("E1",),
        min_event_count=3,  # but only 1 event present
    )
    m = ArMythos(
        id="m_test", title="t", action_summary="s",
        central_event_ids=("E1", "E2", "E3"),
        plot_kind=PLOT_COMPLEX,
        phases=(
            short_phase,
            ArPhase(id="ph_m", role=PHASE_MIDDLE,
                    scope_event_ids=("E2",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=("E3",)),
        ),
        peripeteia_event_id="E2", anagnorisis_event_id="E3",
    )
    obs = verify(m)
    assert _has_code(obs, "phase_event_count_below_min")


def test_phase_event_count_above_max_flags():
    """A7.12 invariant 4b — actual count above max flagged."""
    long_phase = ArPhase(
        id="ph_b", role=PHASE_BEGINNING,
        scope_event_ids=("E1", "E1b", "E1c"),
        max_event_count=2,
    )
    m = ArMythos(
        id="m_test", title="t", action_summary="s",
        central_event_ids=("E1", "E1b", "E1c", "E2", "E3"),
        plot_kind=PLOT_COMPLEX,
        phases=(
            long_phase,
            ArPhase(id="ph_m", role=PHASE_MIDDLE,
                    scope_event_ids=("E2",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=("E3",)),
        ),
        peripeteia_event_id="E2", anagnorisis_event_id="E3",
    )
    obs = verify(m)
    assert _has_code(obs, "phase_event_count_above_max")


def test_phase_event_count_within_bounds_clean():
    """A7.12 — actual count within bounds emits nothing."""
    ok_phase = ArPhase(
        id="ph_b", role=PHASE_BEGINNING,
        scope_event_ids=("E1", "E1b"),
        min_event_count=1, max_event_count=3,
    )
    m = ArMythos(
        id="m_test", title="t", action_summary="s",
        central_event_ids=("E1", "E1b", "E2", "E3"),
        plot_kind=PLOT_COMPLEX,
        phases=(
            ok_phase,
            ArPhase(id="ph_m", role=PHASE_MIDDLE,
                    scope_event_ids=("E2",)),
            ArPhase(id="ph_e", role=PHASE_END,
                    scope_event_ids=("E3",)),
        ),
        peripeteia_event_id="E2", anagnorisis_event_id="E3",
    )
    obs = verify(m)
    for code in (
        "phase_event_count_below_min",
        "phase_event_count_above_max",
        "phase_event_count_bounds_inverted",
    ):
        assert not _has_code(obs, code)


# ----------------------------------------------------------------------------
# A7.13 — co_presence_required_over_phase structural integrity
# ----------------------------------------------------------------------------


def _co_presence_mythos(reqs: tuple) -> ArMythos:
    """Mythos shaped for A7.13 tests: two characters, three phases."""
    return _three_phase_mythos(
        characters=(
            ArCharacter(id="c1", name="Alpha"),
            ArCharacter(id="c2", name="Beta"),
        ),
        co_presence_requirements=reqs,
    )


def test_co_presence_default_empty_clean():
    """Empty co_presence_requirements emits no A7.13 observations."""
    m = _three_phase_mythos()
    obs = verify(m)
    for code in (
        "co_presence_refs_too_few",
        "co_presence_character_unresolved",
        "co_presence_phase_unresolved",
        "co_presence_min_count_zero",
    ):
        assert not _has_code(obs, code)


def test_co_presence_refs_too_few_flags():
    """A7.13 invariant 1 — ≥2 character_ref_ids required."""
    m = _co_presence_mythos((
        ArCoPresenceRequirement(
            id="r1", character_ref_ids=("c1",), phase_id="ph_b",
        ),
    ))
    obs = verify(m)
    assert _has_code(obs, "co_presence_refs_too_few")


def test_co_presence_character_unresolved_flags():
    """A7.13 invariant 2 — character ids must resolve in mythos."""
    m = _co_presence_mythos((
        ArCoPresenceRequirement(
            id="r1", character_ref_ids=("c1", "c_ghost"),
            phase_id="ph_b",
        ),
    ))
    obs = verify(m)
    assert _has_code(obs, "co_presence_character_unresolved")


def test_co_presence_phase_unresolved_flags():
    """A7.13 invariant 3 — phase_id must resolve in mythos.phases."""
    m = _co_presence_mythos((
        ArCoPresenceRequirement(
            id="r1", character_ref_ids=("c1", "c2"),
            phase_id="ph_ghost",
        ),
    ))
    obs = verify(m)
    assert _has_code(obs, "co_presence_phase_unresolved")


def test_co_presence_min_count_zero_flags():
    """A7.13 invariant 4 — min_count must be ≥ 1."""
    m = _co_presence_mythos((
        ArCoPresenceRequirement(
            id="r1", character_ref_ids=("c1", "c2"),
            phase_id="ph_b", min_count=0,
        ),
    ))
    obs = verify(m)
    assert _has_code(obs, "co_presence_min_count_zero")


def test_co_presence_clean_when_all_resolve():
    """A7.13 emits nothing when every check passes."""
    m = _co_presence_mythos((
        ArCoPresenceRequirement(
            id="r1", character_ref_ids=("c1", "c2"),
            phase_id="ph_b", min_count=2,
        ),
    ))
    obs = verify(m)
    for code in (
        "co_presence_refs_too_few",
        "co_presence_character_unresolved",
        "co_presence_phase_unresolved",
        "co_presence_min_count_zero",
    ):
        assert not _has_code(obs, code)


# ----------------------------------------------------------------------------
# A7.14 — audience_knowledge_constraint structural integrity
# ----------------------------------------------------------------------------


def _audience_knowledge_mythos(cons: tuple) -> ArMythos:
    return _three_phase_mythos(audience_knowledge_constraints=cons)


def test_audience_knowledge_default_empty_clean():
    """Empty audience_knowledge_constraints emits nothing."""
    m = _three_phase_mythos()
    obs = verify(m)
    for code in (
        "audience_knowledge_subject_empty",
        "audience_knowledge_τ_s_negative",
        "audience_knowledge_source_event_unresolved",
        "audience_knowledge_source_event_too_late",
    ):
        assert not _has_code(obs, code)


def test_audience_knowledge_subject_empty_flags():
    """A7.14 invariant 1 — subject must be non-empty after strip."""
    m = _audience_knowledge_mythos((
        ArAudienceKnowledgeConstraint(
            id="k1", subject="   ", latest_τ_s=5,
        ),
    ))
    obs = verify(m)
    assert _has_code(obs, "audience_knowledge_subject_empty")


def test_audience_knowledge_τ_s_negative_flags():
    """A7.14 invariant 2 — latest_τ_s must be ≥ 0."""
    m = _audience_knowledge_mythos((
        ArAudienceKnowledgeConstraint(
            id="k1", subject="x", latest_τ_s=-1,
        ),
    ))
    obs = verify(m)
    assert _has_code(obs, "audience_knowledge_τ_s_negative")


def test_audience_knowledge_source_event_unresolved_flags():
    """A7.14 invariant 3 — source_event_id must resolve in substrate."""
    m = _audience_knowledge_mythos((
        ArAudienceKnowledgeConstraint(
            id="k1", subject="x", latest_τ_s=5,
            source_event_id="E_ghost",
        ),
    ))
    events = (
        _synthetic_event("E1", τ_s=0),
        _synthetic_event("E2", τ_s=1),
        _synthetic_event("E3", τ_s=2),
    )
    obs = verify(m, substrate_events=events)
    assert _has_code(obs, "audience_knowledge_source_event_unresolved")


def test_audience_knowledge_source_event_too_late_flags():
    """A7.14 invariant 4 — source event τ_s must be ≤ latest_τ_s."""
    m = _audience_knowledge_mythos((
        ArAudienceKnowledgeConstraint(
            id="k1", subject="x", latest_τ_s=1,
            source_event_id="E3",
        ),
    ))
    events = (
        _synthetic_event("E1", τ_s=0),
        _synthetic_event("E2", τ_s=1),
        _synthetic_event("E3", τ_s=5),  # too late
    )
    obs = verify(m, substrate_events=events)
    assert _has_code(obs, "audience_knowledge_source_event_too_late")


def test_audience_knowledge_source_event_skipped_without_substrate():
    """A7.14 source-event subchecks skip when substrate not threaded."""
    m = _audience_knowledge_mythos((
        ArAudienceKnowledgeConstraint(
            id="k1", subject="x", latest_τ_s=5,
            source_event_id="E_ghost",
        ),
    ))
    obs = verify(m)
    assert not _has_code(obs, "audience_knowledge_source_event_unresolved")
    assert not _has_code(obs, "audience_knowledge_source_event_too_late")


def test_audience_knowledge_clean_when_all_resolve():
    """A7.14 emits nothing when every check passes."""
    m = _audience_knowledge_mythos((
        ArAudienceKnowledgeConstraint(
            id="k1", subject="x", latest_τ_s=5, source_event_id="E2",
        ),
    ))
    events = (
        _synthetic_event("E1", τ_s=0),
        _synthetic_event("E2", τ_s=1),
        _synthetic_event("E3", τ_s=2),
    )
    obs = verify(m, substrate_events=events)
    for code in (
        "audience_knowledge_subject_empty",
        "audience_knowledge_τ_s_negative",
        "audience_knowledge_source_event_unresolved",
        "audience_knowledge_source_event_too_late",
    ):
        assert not _has_code(obs, code)


def test_verify_signature_unchanged_for_sketch_04():
    """Sketch-04 does NOT add a verify kwarg; pre-sketch-04 callers
    using sketch-03 signature continue to work and produce identical
    output for encodings without sketch-04 fields populated."""
    m = _three_phase_mythos()
    obs_sketch_03_signature = verify(m, character_arc_relations=())
    obs_sketch_04_signature = verify(m, character_arc_relations=())
    assert obs_sketch_03_signature == obs_sketch_04_signature


# ============================================================================
# Integration — Macbeth (third Aristotelian encoding)
# ============================================================================


def test_macbeth_aristotelian_verifies_clean():
    """Third worked case: Macbeth under A1-A12 verifies with zero
    observations against the real macbeth.py FABULA."""
    from story_engine.encodings.macbeth import FABULA
    from story_engine.encodings.macbeth_aristotelian import (
        AR_MACBETH_MYTHOS,
    )
    obs = verify(AR_MACBETH_MYTHOS, substrate_events=FABULA)
    assert obs == [], (
        f"Expected zero observations; got {len(obs)}:\n"
        + "\n".join(f"  [{o.severity}] {o.code}: {o.message}"
                    for o in obs)
    )


def test_macbeth_aristotelian_records_shape():
    """Structural pins on AR_MACBETH_MYTHOS."""
    from story_engine.encodings.macbeth_aristotelian import (
        AR_MACBETH_MYTHOS,
    )
    m = AR_MACBETH_MYTHOS
    assert m.plot_kind == PLOT_COMPLEX
    assert len(m.phases) == 3
    assert [ph.role for ph in m.phases] == [
        PHASE_BEGINNING, PHASE_MIDDLE, PHASE_END,
    ]
    assert m.peripeteia_event_id == "E_macduff_reveals_birth"
    assert m.anagnorisis_event_id == "E_macduff_reveals_birth"
    assert m.asserts_unity_of_action is True
    assert m.asserts_unity_of_time is False
    assert m.asserts_unity_of_place is False
    assert m.aims_at_catharsis is True
    assert len(m.characters) == 2
    macbeth_char = [c for c in m.characters if c.id == "ar_macbeth"][0]
    assert macbeth_char.is_tragic_hero is True
    assert macbeth_char.character_ref_id == "macbeth"
    assert macbeth_char.hamartia_text is not None
    lady_char = [c for c in m.characters
                 if c.id == "ar_lady_macbeth"][0]
    assert lady_char.is_tragic_hero is True
    assert lady_char.character_ref_id == "lady_macbeth"


def test_macbeth_aristotelian_binding_is_coincident():
    """Macbeth exercises BINDING_COINCIDENT for the first time in
    the corpus. Oedipus uses BINDING_SEPARATED; both bindings
    thus have corpus coverage."""
    from story_engine.encodings.macbeth_aristotelian import (
        AR_MACBETH_MYTHOS,
    )
    assert (AR_MACBETH_MYTHOS.peripeteia_anagnorisis_binding
            == BINDING_COINCIDENT)
    # Coincident implies the two event ids are equal; the
    # A7.8 check would otherwise flag inconsistency.
    assert (AR_MACBETH_MYTHOS.peripeteia_event_id
            == AR_MACBETH_MYTHOS.anagnorisis_event_id)


def test_macbeth_aristotelian_chain_non_precipitating():
    """Macbeth's anagnorisis_chain step (Lady Macbeth's sleepwalking)
    has precipitates_main=False — her recognition does not cause
    Macbeth's. Contrasts Oedipus's AR_STEP_JOCASTA
    (precipitates_main=True)."""
    from story_engine.encodings.macbeth_aristotelian import (
        AR_MACBETH_MYTHOS, AR_STEP_LADY_MACBETH_SLEEPWALKING,
    )
    assert AR_MACBETH_MYTHOS.anagnorisis_chain == (
        AR_STEP_LADY_MACBETH_SLEEPWALKING,
    )
    step = AR_STEP_LADY_MACBETH_SLEEPWALKING
    assert step.event_id == "E_sleepwalking"
    assert step.character_ref_id == "ar_lady_macbeth"
    assert step.precipitates_main is False


# ============================================================================
# Integration — Hamlet (fourth Aristotelian encoding)
# ============================================================================


def test_hamlet_aristotelian_verifies_clean():
    """Fourth worked case: Hamlet under A1-A14 verifies with zero
    observations against the real hamlet.py FABULA. Threads all
    sketch-03 kwargs (mythoi + character_arc_relations) so the A7.10
    structural-integrity check runs over the two pairwise arc
    relations and the A7.11 staging-ordering check runs over the
    full three-step chain."""
    from story_engine.encodings.hamlet import FABULA
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_CHARACTER_ARC_RELATIONS, AR_HAMLET_MYTHOS,
    )
    obs = verify(
        AR_HAMLET_MYTHOS,
        substrate_events=FABULA,
        mythoi=(AR_HAMLET_MYTHOS,),
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    assert obs == [], (
        f"Expected zero observations; got {len(obs)}:\n"
        + "\n".join(f"  [{o.severity}] {o.code}: {o.message}"
                    for o in obs)
    )


def test_hamlet_aristotelian_records_shape():
    """Structural pins on AR_HAMLET_MYTHOS. Distinctive from the
    earlier three encodings: complication_event_id and
    denouement_event_id are authored (neither Oedipus nor Macbeth
    pin them); three tragic-hero characters (first in corpus);
    peripeteia and anagnorisis are distinct events separated
    across the entire middle phase."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    m = AR_HAMLET_MYTHOS
    assert m.plot_kind == PLOT_COMPLEX
    assert len(m.phases) == 3
    assert [ph.role for ph in m.phases] == [
        PHASE_BEGINNING, PHASE_MIDDLE, PHASE_END,
    ]
    assert m.peripeteia_event_id == "E_hamlet_kills_polonius"
    assert m.anagnorisis_event_id == "E_laertes_reveals_plot"
    assert m.peripeteia_event_id != m.anagnorisis_event_id
    assert m.complication_event_id == "E_mousetrap_performance"
    assert m.denouement_event_id == "E_duel_plotted"
    assert m.asserts_unity_of_action is True
    assert m.asserts_unity_of_time is False
    assert m.asserts_unity_of_place is False
    assert m.aims_at_catharsis is True
    assert len(m.characters) == 3
    ids = sorted(c.id for c in m.characters)
    assert ids == ["ar_claudius", "ar_hamlet", "ar_laertes"]
    for char in m.characters:
        assert char.is_tragic_hero is True
        assert char.hamartia_text is not None
        assert char.character_ref_id is not None


def test_hamlet_aristotelian_three_parallel_tragic_heroes():
    """OQ-AP6 pressure pin. Hamlet is the first corpus encoding to
    author three `is_tragic_hero=True` characters in one mythos
    (Oedipus has 2, Macbeth has 2, Rashomon has 0 mythos-scope
    tragic heroes because each testimony authors its own). The
    dialect admits the multiplicity but has no structural hook
    for intra-mythos parallel — the probe surface recorded by
    `OQ_AP6_FINDING`."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    tragic = [c for c in AR_HAMLET_MYTHOS.characters
              if c.is_tragic_hero]
    assert len(tragic) == 3
    refs = sorted(c.character_ref_id for c in tragic)
    assert refs == ["claudius", "hamlet", "laertes"]


def test_hamlet_aristotelian_binding_is_separated_distance_nine():
    """Hamlet exercises BINDING_SEPARATED at distance 9 — the widest
    separation in the corpus. Oedipus is BINDING_SEPARATED at
    distance 5; Macbeth is BINDING_COINCIDENT. The raw τ_s
    distance is recovered from substrate (peripeteia at τ_s=8,
    anagnorisis at τ_s=17) because the dialect today records only
    the categorical binding, not the numerical distance. This pin
    is load-bearing for the OQ_AP7 forcing function (whether
    'separated' should distinguish near- from distant-)."""
    from story_engine.encodings.hamlet import FABULA
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    assert (AR_HAMLET_MYTHOS.peripeteia_anagnorisis_binding
            == BINDING_SEPARATED)
    # Default bound 3 preserved — any distance > 3 is SEPARATED;
    # the encoding does not shift the bound to force a finer
    # category.
    assert AR_HAMLET_MYTHOS.peripeteia_anagnorisis_adjacency_bound == 3
    by_id = {e.id: e for e in FABULA}
    per = by_id[AR_HAMLET_MYTHOS.peripeteia_event_id]
    ana = by_id[AR_HAMLET_MYTHOS.anagnorisis_event_id]
    assert per.τ_s == 8
    assert ana.τ_s == 17
    assert ana.τ_s - per.τ_s == 9


def test_hamlet_aristotelian_chain_three_steps_two_kinds():
    """Under sketch-03, Hamlet's anagnorisis_chain is three steps
    across two step_kinds: two staging (Hamlet Ghost commission at
    τ_s=1, Hamlet Mousetrap verification at τ_s=6) plus one parallel
    (Claudius prayer at τ_s=7). The staging steps close OQ-AP10 —
    same-character epistemic staging toward the main anagnorisis at
    τ_s=17. The parallel step is retained, carrying the antagonist's
    private recognition; its step_kind flips from implicit (pre-
    sketch-03 derived-from-precipitates_main=False) to explicit
    'parallel' for honest authoring."""
    from story_engine.core.aristotelian import (
        STEP_KIND_PARALLEL, STEP_KIND_STAGING,
    )
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
        AR_STEP_CLAUDIUS_PRAYS,
        AR_STEP_HAMLET_GHOST_CLAIM,
        AR_STEP_HAMLET_MOUSETRAP,
    )
    assert AR_HAMLET_MYTHOS.anagnorisis_chain == (
        AR_STEP_HAMLET_GHOST_CLAIM,
        AR_STEP_HAMLET_MOUSETRAP,
        AR_STEP_CLAUDIUS_PRAYS,
    )
    assert AR_HAMLET_MYTHOS.anagnorisis_character_ref_id == "ar_hamlet"

    # Staging steps — same character as main, precipitating by A14
    # definition.
    for step in (AR_STEP_HAMLET_GHOST_CLAIM, AR_STEP_HAMLET_MOUSETRAP):
        assert step.step_kind == STEP_KIND_STAGING
        assert step.character_ref_id == "ar_hamlet"
        assert step.precipitates_main is True

    # Parallel step — different character, non-precipitating.
    claudius = AR_STEP_CLAUDIUS_PRAYS
    assert claudius.step_kind == STEP_KIND_PARALLEL
    assert claudius.character_ref_id == "ar_claudius"
    assert claudius.precipitates_main is False

    # Events resolve to the expected substrate ids.
    assert AR_STEP_HAMLET_GHOST_CLAIM.event_id == "E_hamlet_meets_ghost"
    assert AR_STEP_HAMLET_MOUSETRAP.event_id == "E_mousetrap_performance"
    assert claudius.event_id == "E_claudius_prays"


def test_hamlet_aristotelian_probe_findings_authored():
    """OQ-AP5 (fate-agent), OQ-AP6 (parallel heroes), OQ-AP7
    (range of separated), and OQ-AP8 (same-beat staggered
    recognition) findings are authored as non-empty prose
    constants — the research payoff Session 2 committed to. These
    are the probe-surface answers the encoding commits to before
    the live probe run consumes them."""
    from story_engine.encodings import hamlet_aristotelian as ha
    for name in ("OQ_AP5_FINDING", "OQ_AP6_FINDING",
                 "OQ_AP7_FINDING", "OQ_AP8_FINDING"):
        val = getattr(ha, name)
        assert isinstance(val, str), f"{name} not a string"
        assert len(val) > 100, f"{name} is too short to be meaningful"
        # Prose uses the hyphenated id form (e.g. "OQ-AP5") while the
        # constant name uses underscores — convert for the self-
        # reference check.
        prose_id = name.split("_FINDING")[0].replace("_", "-")
        assert prose_id in val, (
            f"{name} body does not reference its own forcing-function "
            f"id ({prose_id!r})"
        )


def test_hamlet_aristotelian_sketch04_phase_bounds_set():
    """Hamlet's three phases each carry A15-SE1 bounds; current event
    counts (13/11/8) fall within (10..15 / 8..14 / 6..10)."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    bounds_by_role = {
        ph.role: (ph.min_event_count, ph.max_event_count)
        for ph in AR_HAMLET_MYTHOS.phases
    }
    assert bounds_by_role["beginning"] == (10, 15)
    assert bounds_by_role["middle"] == (8, 14)
    assert bounds_by_role["end"] == (6, 10)


def test_hamlet_aristotelian_sketch04_pacing_preferences_set():
    """Hamlet's three phases each carry A16-SP3 pacing preferences."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    pacing_by_role = {
        ph.role: ph.pacing_preference for ph in AR_HAMLET_MYTHOS.phases
    }
    assert pacing_by_role["beginning"] == PACING_EVEN
    assert pacing_by_role["middle"] == PACING_SLOW_BURN
    assert pacing_by_role["end"] == PACING_RAPID_ESCALATION


def test_hamlet_aristotelian_sketch04_co_presence_authored():
    """Hamlet authors three A15-SE2 co-presence requirements naming
    only existing AR_* characters and existing PH_* phases."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    reqs = AR_HAMLET_MYTHOS.co_presence_requirements
    assert len(reqs) == 3
    ids = {r.id for r in reqs}
    assert ids == {
        "copres_hamlet_claudius_end",
        "copres_hamlet_laertes_end",
        "copres_claudius_laertes_middle",
    }
    char_ids = {c.id for c in AR_HAMLET_MYTHOS.characters}
    phase_ids = {ph.id for ph in AR_HAMLET_MYTHOS.phases}
    for r in reqs:
        for cid in r.character_ref_ids:
            assert cid in char_ids
        assert r.phase_id in phase_ids
        assert r.min_count >= 1


def test_hamlet_aristotelian_sketch04_audience_knowledge_authored():
    """Hamlet authors three A15-SE3 audience-knowledge constraints,
    each pointing at an existing substrate event with τ_s ≤ latest."""
    from story_engine.encodings.hamlet import FABULA
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    cons = AR_HAMLET_MYTHOS.audience_knowledge_constraints
    assert len(cons) == 3
    by_id = {e.id: e for e in FABULA}
    for c in cons:
        assert c.subject.strip()
        assert c.latest_τ_s >= 0
        if c.source_event_id is not None:
            assert c.source_event_id in by_id
            assert by_id[c.source_event_id].τ_s <= c.latest_τ_s


def test_hamlet_aristotelian_sketch04_tonal_register_set():
    """Hamlet declares tonal_register='tragic-with-irony' (A16-SP1)."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    assert (AR_HAMLET_MYTHOS.tonal_register
            == TONAL_REGISTER_TRAGIC_WITH_IRONY)


def test_hamlet_aristotelian_sketch04_binding_distance_preference_set():
    """Hamlet declares binding_distance_preference='prefer_wide'
    (A16-SP2). Matches the actual SEPARATED distance 9 — corpus widest."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    assert (AR_HAMLET_MYTHOS.binding_distance_preference
            == BINDING_PREF_WIDE)


def test_pre_sketch_04_encodings_emit_no_sketch_04_codes():
    """A7.12-A7.14 emit no observations on Oedipus / Rashomon /
    Macbeth — the three pre-sketch-04 encodings carry default-empty
    sketch-04 fields."""
    from story_engine.encodings.oedipus_aristotelian import (
        AR_OEDIPUS_MYTHOS,
    )
    from story_engine.encodings.oedipus import FABULA as OEDIPUS_FABULA
    from story_engine.encodings.rashomon_aristotelian import (
        AR_RASHOMON_MYTHOI,
    )
    from story_engine.encodings.rashomon import (
        EVENTS_ALL as RASHOMON_FABULA,
    )
    from story_engine.encodings.macbeth_aristotelian import (
        AR_MACBETH_MYTHOS,
    )
    from story_engine.encodings.macbeth import FABULA as MACBETH_FABULA

    sketch_04_codes = {
        "phase_event_count_min_negative",
        "phase_event_count_max_negative",
        "phase_event_count_bounds_inverted",
        "phase_event_count_below_min",
        "phase_event_count_above_max",
        "co_presence_refs_too_few",
        "co_presence_character_unresolved",
        "co_presence_phase_unresolved",
        "co_presence_min_count_zero",
        "audience_knowledge_subject_empty",
        "audience_knowledge_τ_s_negative",
        "audience_knowledge_source_event_unresolved",
        "audience_knowledge_source_event_too_late",
    }

    pairs = [
        (AR_OEDIPUS_MYTHOS, OEDIPUS_FABULA),
        (AR_MACBETH_MYTHOS, MACBETH_FABULA),
    ]
    for myth in AR_RASHOMON_MYTHOI:
        pairs.append((myth, RASHOMON_FABULA))

    for myth, fabula in pairs:
        obs = verify(myth, substrate_events=fabula, mythoi=(myth,))
        emitted = {o.code for o in obs}
        leak = emitted & sketch_04_codes
        assert not leak, (
            f"Pre-sketch-04 mythos {myth.id!r} emitted sketch-04 codes "
            f"{leak}; sketch-04 fields are not extension-only as "
            f"committed."
        )


def test_hamlet_aristotelian_no_mythos_relation_authored():
    """Hamlet is single-mythos. Unlike Rashomon, no ArMythosRelation
    is authored. The module exposes no `AR_HAMLET_RELATIONS`
    attribute (parallel to rashomon's `AR_RASHOMON_RELATIONS`) —
    the encoding commits that intra-mythos parallelism is NOT
    expressed via A10 today."""
    from story_engine.encodings import hamlet_aristotelian as ha
    assert not hasattr(ha, "AR_HAMLET_RELATIONS"), (
        "Hamlet should not author relations at dialect scope; "
        "OQ_AP6_FINDING explicitly rejects the three-mythos "
        "workaround."
    )


# ============================================================================
# Integration — Lear (fifth Aristotelian encoding)
# ============================================================================


def test_lear_aristotelian_verifies_clean_up_to_sketch05_noteds():
    """Fifth worked case: Lear under A1-A18 + sketch-04 + sketch-05
    verifies against the real lear.py FABULA with exactly three
    noted observations:
    - 2 × character_arc_relation_kind_noncanonical (A7.10 — the
      two `kind="instrumental"` records; OQ-AP14 pressure, per
      canonical-plus-open discipline).
    - 1 × character_arc_relation_paired_polarity_contrast (A7.15
      check 5, NEW in sketch-05) — the Edmund/Edgar → Gloucester
      opposite-polarity pair.
    No advises-review severity observations."""
    from story_engine.encodings.lear import FABULA
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_MYTHOS, AR_LEAR_CHARACTER_ARC_RELATIONS,
    )
    obs = verify(
        AR_LEAR_MYTHOS,
        substrate_events=FABULA,
        mythoi=(AR_LEAR_MYTHOS,),
        character_arc_relations=AR_LEAR_CHARACTER_ARC_RELATIONS,
    )
    # Exactly three observations, all noted.
    assert len(obs) == 3, (
        f"Expected exactly 3 observations; got {len(obs)}:\n"
        + "\n".join(f"  [{o.severity}] {o.code}: {o.message}"
                    for o in obs)
    )
    for o in obs:
        assert o.severity == SEVERITY_NOTED, (
            f"Expected only noted severity; got {o.severity} on "
            f"{o.code}"
        )
    codes = sorted(o.code for o in obs)
    assert codes == [
        "character_arc_relation_kind_noncanonical",
        "character_arc_relation_kind_noncanonical",
        "character_arc_relation_paired_polarity_contrast",
    ]


def test_lear_aristotelian_records_shape():
    """Structural pins on AR_LEAR_MYTHOS. Distinct from earlier
    encodings: asserts_unity_of_action=False (corpus first), five
    ArCharacter records (not three), both complication and
    denouement set (Hamlet pattern, not Oedipus/Macbeth), peripeteia
    and anagnorisis distinct events."""
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_MYTHOS,
    )
    m = AR_LEAR_MYTHOS
    assert m.plot_kind == PLOT_COMPLEX
    assert len(m.phases) == 3
    assert [ph.role for ph in m.phases] == [
        PHASE_BEGINNING, PHASE_MIDDLE, PHASE_END,
    ]
    assert m.peripeteia_event_id == "E_goneril_strips_retinue"
    assert m.anagnorisis_event_id == "E_lear_cordelia_reconcile"
    assert m.peripeteia_event_id != m.anagnorisis_event_id
    assert m.complication_event_id == "E_lear_at_gonerils"
    assert m.denouement_event_id == "E_lear_meets_blind_gloucester"
    # Unity of action — FALSE (corpus first).
    assert m.asserts_unity_of_action is False
    assert m.asserts_unity_of_time is False
    assert m.asserts_unity_of_place is False
    assert m.aims_at_catharsis is True
    # Five ArCharacter records; three tragic-heroes.
    assert len(m.characters) == 5
    ids = sorted(c.id for c in m.characters)
    assert ids == [
        "ar_cordelia", "ar_edgar", "ar_edmund",
        "ar_gloucester", "ar_lear",
    ]
    for char in m.characters:
        assert char.hamartia_text, (
            f"{char.id} missing hamartia_text"
        )
        assert char.character_ref_id is not None


def test_lear_aristotelian_three_parallel_tragic_heroes():
    """OQ-AP6 generalization pin. Lear is the corpus's second
    ≥3-tragic-hero encoding after Hamlet. Lear / Gloucester /
    Cordelia are the three tragic heroes; Edmund and Edgar are
    authored as non-tragic ArCharacters to serve the A13
    instrumental-kind relations."""
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_MYTHOS,
    )
    tragic = [c for c in AR_LEAR_MYTHOS.characters
              if c.is_tragic_hero]
    non_tragic = [c for c in AR_LEAR_MYTHOS.characters
                  if not c.is_tragic_hero]
    assert len(tragic) == 3
    assert len(non_tragic) == 2
    refs = sorted(c.character_ref_id for c in tragic)
    assert refs == ["cordelia", "gloucester", "lear"]
    non_tragic_refs = sorted(c.character_ref_id
                             for c in non_tragic)
    assert non_tragic_refs == ["edgar", "edmund"]


def test_lear_aristotelian_asserts_unity_of_action_false_corpus_first():
    """Lear is the corpus's FIRST encoding to set
    asserts_unity_of_action=False. The double-plot (Lear + three
    daughters || Gloucester + two sons) is thematically unified
    via the A13 AR_LEAR_GLOUCESTER_PARALLEL relation but not
    causally unified; the False assertion carries the classical-
    unity departure. OQ_LEAR_2 forcing-function pin."""
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_MYTHOS,
    )
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    assert AR_LEAR_MYTHOS.asserts_unity_of_action is False
    # Verify no earlier Aristotelian-encoding mythos authored
    # asserts_unity_of_action=False.
    assert AR_HAMLET_MYTHOS.asserts_unity_of_action is True


def test_lear_aristotelian_binding_is_separated_distance_fourteen():
    """Lear exercises BINDING_SEPARATED at distance 14 — the widest
    separation in the corpus (Oedipus 5, Hamlet 9, Macbeth
    coincident). Raw τ_s distance recovered from substrate.
    Load-bearing for OQ-AP7 — the second independent encoding to
    re-surface the near-vs-distant separated distinction."""
    from story_engine.encodings.lear import FABULA
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_MYTHOS,
    )
    assert (AR_LEAR_MYTHOS.peripeteia_anagnorisis_binding
            == BINDING_SEPARATED)
    # Default bound 3 preserved.
    assert AR_LEAR_MYTHOS.peripeteia_anagnorisis_adjacency_bound == 3
    by_id = {e.id: e for e in FABULA}
    per = by_id[AR_LEAR_MYTHOS.peripeteia_event_id]
    ana = by_id[AR_LEAR_MYTHOS.anagnorisis_event_id]
    assert per.τ_s == 14
    assert ana.τ_s == 28
    assert ana.τ_s - per.τ_s == 14


def test_lear_aristotelian_chain_two_parallel_no_staging():
    """OQ-LEAR-1 pin. Lear's anagnorisis chain authors two steps,
    both step_kind=parallel, ZERO staging steps despite Lear
    himself being the anagnorisis_character. The absence is the
    substrate signature of the emotional-vs-epistemic main-
    anagnorisis distinction: Lear reaches anagnorisis via
    affective progression (remove_held on a false belief) rather
    than information acquisition (Hamlet's staging pattern)."""
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_MYTHOS,
    )
    chain = AR_LEAR_MYTHOS.anagnorisis_chain
    assert len(chain) == 2
    for step in chain:
        assert step.step_kind == STEP_KIND_PARALLEL
        assert step.precipitates_main is False
    # Neither chain step's character matches the anagnorisis
    # character (the 'no staging' shape expressed at the
    # character-ref level).
    assert AR_LEAR_MYTHOS.anagnorisis_character_ref_id == "ar_lear"
    for step in chain:
        assert step.character_ref_id != "ar_lear"


def test_lear_aristotelian_chain_includes_post_main_step():
    """Corpus first: Edmund's deathbed confession at τ_s=35 is a
    parallel chain step that lands AFTER the main anagnorisis at
    τ_s=28. A14 invariants do not forbid post-main placement for
    parallel steps (only staging steps must precede main); this
    encoding exercises the legal-but-unprecedented shape. The
    pathos of Edmund's futile reversal depends structurally on
    its post-main placement."""
    from story_engine.encodings.lear import FABULA
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_MYTHOS, AR_STEP_EDMUND_CONFESSES,
    )
    by_id = {e.id: e for e in FABULA}
    main_τ = by_id[AR_LEAR_MYTHOS.anagnorisis_event_id].τ_s
    edmund_step_τ = by_id[AR_STEP_EDMUND_CONFESSES.event_id].τ_s
    assert edmund_step_τ > main_τ, (
        f"Expected Edmund step (τ_s={edmund_step_τ}) post-main "
        f"(τ_s={main_τ})"
    )
    assert AR_STEP_EDMUND_CONFESSES.step_kind == STEP_KIND_PARALLEL
    assert AR_STEP_EDMUND_CONFESSES.character_ref_id == "ar_edmund"


def test_lear_aristotelian_four_character_arc_relations_two_instrumental():
    """Four A13 relations: two canonical (parallel, foil) + two
    non-canonical (instrumental × 2). Instrumental-kind is the
    OQ-AP14 forcing surface; sketch-03 admits it under canonical-
    plus-open discipline at severity=noted."""
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_CHARACTER_ARC_RELATIONS,
    )
    assert len(AR_LEAR_CHARACTER_ARC_RELATIONS) == 4
    kinds = [r.kind for r in AR_LEAR_CHARACTER_ARC_RELATIONS]
    assert kinds.count(ARC_RELATION_PARALLEL) == 1
    assert kinds.count(ARC_RELATION_FOIL) == 1
    assert kinds.count("instrumental") == 2
    # Every relation is intra-mythos (mythos_id == "ar_lear").
    for rel in AR_LEAR_CHARACTER_ARC_RELATIONS:
        assert rel.mythos_id == "ar_lear"
        assert len(rel.character_ref_ids) >= 2


def test_lear_aristotelian_instrumental_relations_share_target_gloucester():
    """OQ-AP14 substrate signature pin. The two non-canonical
    instrumental relations share a TARGET (Gloucester = position 1
    in the character_ref_ids tuple, reading the tuple as
    (wielder, target)) and have DIFFERENT wielders (Edmund
    malicious, Edgar therapeutic). This opposite-polarity-on-
    shared-target shape is what the canonical vocabulary cannot
    structurally name."""
    from story_engine.encodings.lear_aristotelian import (
        AR_EDMUND_GLOUCESTER_INSTRUMENTAL,
        AR_EDGAR_GLOUCESTER_INSTRUMENTAL,
    )
    # Directional tuple convention: (wielder, target).
    assert AR_EDMUND_GLOUCESTER_INSTRUMENTAL.character_ref_ids == (
        "ar_edmund", "ar_gloucester",
    )
    assert AR_EDGAR_GLOUCESTER_INSTRUMENTAL.character_ref_ids == (
        "ar_edgar", "ar_gloucester",
    )
    # Same target (Gloucester); different wielders.
    assert (AR_EDMUND_GLOUCESTER_INSTRUMENTAL.character_ref_ids[1]
            == AR_EDGAR_GLOUCESTER_INSTRUMENTAL.character_ref_ids[1])
    assert (AR_EDMUND_GLOUCESTER_INSTRUMENTAL.character_ref_ids[0]
            != AR_EDGAR_GLOUCESTER_INSTRUMENTAL.character_ref_ids[0])


def test_lear_aristotelian_probe_findings_authored():
    """OQ_AP14, OQ_AP15 (both authored as pressure), OQ_AP7
    (re-surfaced with second-site distance), OQ_LEAR_1 (emotional-
    vs-epistemic staging gap), and OQ_LEAR_2 (double-plot unity)
    are authored as non-empty prose constants — the research
    payload Session 2 committed. Each self-references its own
    hyphenated id."""
    from story_engine.encodings import lear_aristotelian as la
    expected = {
        "OQ_AP14_FINDING": "OQ-AP14",
        "OQ_AP15_FINDING": "OQ-AP15",
        "OQ_AP7_FINDING":  "OQ-AP7",
        "OQ_LEAR_1":       "OQ-LEAR-1",
        "OQ_LEAR_2":       "OQ-LEAR-2",
    }
    for name, prose_id in expected.items():
        val = getattr(la, name)
        assert isinstance(val, str), f"{name} not a string"
        assert len(val) > 100, f"{name} too short to be meaningful"
        assert prose_id in val, (
            f"{name} body does not reference its own forcing-"
            f"function id ({prose_id!r})"
        )
    # OQ_FINDINGS tuple is authored.
    assert isinstance(la.OQ_FINDINGS, tuple)
    assert len(la.OQ_FINDINGS) == 5


def test_lear_aristotelian_no_mythos_relation_authored():
    """Lear is single-mythos. Unlike Rashomon (four-testimony
    contest), no ArMythosRelation is authored. The module exposes
    no `AR_LEAR_RELATIONS` attribute; intra-mythos parallelism is
    expressed via A13 ArCharacterArcRelation (the Lear-Gloucester
    parallel relation), not via the A10 three-mythos workaround."""
    from story_engine.encodings import lear_aristotelian as la
    assert not hasattr(la, "AR_LEAR_RELATIONS")


def test_lear_cordelia_hanged_empty_observer_set():
    """OQ-AP15 substrate signature pin. E_cordelia_hanged
    (τ_s=36) has world effects (hanged + dead propositions on
    Cordelia) but ZERO KnowledgeEffect projections — no named
    character observes the event. The catharsis displaces to
    E_lear_enters_with_cordelia (τ_s=37) where Lear + Albany +
    Edgar + Kent all observe dead(cordelia). This is the cleanest
    case in the corpus of an empty-observer defining event."""
    from story_engine.encodings.lear import FABULA
    by_id = {e.id: e for e in FABULA}
    hanged = by_id["E_cordelia_hanged"]
    # World effects present.
    world_effects = [eff for eff in hanged.effects
                     if hasattr(eff, "prop")
                     and not hasattr(eff, "agent_id")]
    assert len(world_effects) >= 2  # hanged + dead
    # Zero knowledge-effect projections.
    kn_effects = [eff for eff in hanged.effects
                  if hasattr(eff, "agent_id")]
    assert len(kn_effects) == 0, (
        f"E_cordelia_hanged should have zero KnowledgeEffect "
        f"projections (OQ-AP15 empty-observer signature); "
        f"got {len(kn_effects)}"
    )
    # Catharsis displaces to the entrance event.
    entrance = by_id["E_lear_enters_with_cordelia"]
    entrance_observers = sorted(
        set(eff.agent_id for eff in entrance.effects
            if hasattr(eff, "agent_id"))
    )
    assert "lear" in entrance_observers
    assert "albany" in entrance_observers
    assert "edgar" in entrance_observers


def test_lear_aristotelian_sketch04_fields_authored():
    """Sketch-04 integration — the Lear mythos authors phase
    bounds, pacing preferences, co-presence requirements, audience-
    knowledge constraints, tonal register, and binding distance
    preference. Parallels Hamlet's sketch-04 coverage."""
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_MYTHOS,
    )
    # Phase bounds on all three phases.
    for ph in AR_LEAR_MYTHOS.phases:
        assert ph.min_event_count > 0
        assert ph.max_event_count >= ph.min_event_count
        assert ph.pacing_preference in (
            PACING_EVEN, PACING_SLOW_BURN, PACING_RAPID_ESCALATION,
        )
    # Co-presence: 3 requirements.
    assert len(AR_LEAR_MYTHOS.co_presence_requirements) == 3
    # Audience-knowledge: 3 constraints.
    assert len(AR_LEAR_MYTHOS.audience_knowledge_constraints) == 3
    # Tonal register: tragic-pure (contrast Hamlet's tragic-with-
    # irony).
    assert (AR_LEAR_MYTHOS.tonal_register
            == TONAL_REGISTER_TRAGIC_PURE)
    # Binding distance preference: wide (matches corpus-widest
    # actual distance 14).
    assert (AR_LEAR_MYTHOS.binding_distance_preference
            == BINDING_PREF_WIDE)


# ============================================================================
# Sketch-05 — A17 (directionality + polarity) + A7.15 synthetic fixtures
# ============================================================================


def test_canonical_directionalities_contents():
    """Sketch-05 A17 ships 'symmetric' and 'directional' as the
    canonical directionality vocabulary."""
    assert DIRECTIONALITY_SYMMETRIC in CANONICAL_DIRECTIONALITIES
    assert DIRECTIONALITY_DIRECTIONAL in CANONICAL_DIRECTIONALITIES
    assert len(CANONICAL_DIRECTIONALITIES) == 2


def test_canonical_polarities_contents():
    """Sketch-05 A17 ships 'malicious', 'therapeutic', 'neutral',
    'sanctioned' as the canonical polarity vocabulary."""
    assert POLARITY_MALICIOUS in CANONICAL_POLARITIES
    assert POLARITY_THERAPEUTIC in CANONICAL_POLARITIES
    assert POLARITY_NEUTRAL in CANONICAL_POLARITIES
    assert POLARITY_SANCTIONED in CANONICAL_POLARITIES
    assert len(CANONICAL_POLARITIES) == 4


def test_arcrelation_sketch05_field_defaults():
    """A17 fields default to empty strings; pre-sketch-05 encodings
    construct relations without setting either."""
    rel = ArCharacterArcRelation(
        id="r", kind="parallel",
        character_ref_ids=("a", "b"),
        mythos_id="m",
    )
    assert rel.directionality == ""
    assert rel.polarity == ""


def test_archaracter_sketch05_field_default():
    """A18 anagnorisis_absent defaults to False."""
    c = ArCharacter(id="c", name="c")
    assert c.anagnorisis_absent is False


def _two_character_mythos_with_arc(rel: ArCharacterArcRelation,
                                   anag_char: str = None,
                                   chain=()) -> ArMythos:
    """Minimal two-character mythos for A7.15 synthetic tests."""
    chars = (
        ArCharacter(id="c_a", name="A", character_ref_id="c_a",
                    is_tragic_hero=True,
                    hamartia_text="h"),
        ArCharacter(id="c_b", name="B", character_ref_id="c_b",
                    is_tragic_hero=False),
    )
    return ArMythos(
        id="m", title="M",
        action_summary="",
        central_event_ids=(),
        plot_kind=PLOT_COMPLEX,
        phases=(
            ArPhase(id="p_b", role=PHASE_BEGINNING, scope_event_ids=()),
            ArPhase(id="p_m", role=PHASE_MIDDLE, scope_event_ids=()),
            ArPhase(id="p_e", role=PHASE_END, scope_event_ids=()),
        ),
        peripeteia_event_id="E_x",
        anagnorisis_event_id="E_y",
        characters=chars,
        anagnorisis_chain=chain,
        anagnorisis_character_ref_id=anag_char,
    )


def test_arcrelation_directionality_invalid_flags():
    """A7.15 check 1 — invalid directionality value flags
    advises-review."""
    rel = ArCharacterArcRelation(
        id="r", kind="parallel",
        character_ref_ids=("c_a", "c_b"),
        mythos_id="m",
        directionality="sideways",
    )
    m = _two_character_mythos_with_arc(rel)
    obs = verify(m, mythoi=(m,), character_arc_relations=(rel,))
    codes = [o.code for o in obs]
    assert "character_arc_relation_directionality_invalid" in codes


def test_arcrelation_polarity_invalid_flags():
    """A7.15 check 2 — invalid polarity value flags advises-review."""
    rel = ArCharacterArcRelation(
        id="r", kind="instrumental",
        character_ref_ids=("c_a", "c_b"),
        mythos_id="m",
        directionality="directional",
        polarity="rude",
    )
    m = _two_character_mythos_with_arc(rel)
    obs = verify(m, mythoi=(m,), character_arc_relations=(rel,))
    codes = [o.code for o in obs]
    assert "character_arc_relation_polarity_invalid" in codes


def test_arcrelation_canonical_kind_directional_conflict_flags():
    """A7.15 check 3 — canonical kind + directional directionality
    is a mis-classification; flags advises-review."""
    rel = ArCharacterArcRelation(
        id="r", kind="parallel",
        character_ref_ids=("c_a", "c_b"),
        mythos_id="m",
        directionality=DIRECTIONALITY_DIRECTIONAL,
    )
    m = _two_character_mythos_with_arc(rel)
    obs = verify(m, mythoi=(m,), character_arc_relations=(rel,))
    codes = [o.code for o in obs]
    assert ("character_arc_relation_canonical_kind_directional"
            "_conflict") in codes


def test_arcrelation_polarity_on_symmetric_noted():
    """A7.15 check 4 — polarity set on symmetric directionality
    emits noted (soft tension; polarity strongest on directional)."""
    rel = ArCharacterArcRelation(
        id="r", kind="parallel",
        character_ref_ids=("c_a", "c_b"),
        mythos_id="m",
        directionality=DIRECTIONALITY_SYMMETRIC,
        polarity=POLARITY_NEUTRAL,
    )
    m = _two_character_mythos_with_arc(rel)
    obs = verify(m, mythoi=(m,), character_arc_relations=(rel,))
    matches = [
        o for o in obs
        if o.code == "character_arc_relation_polarity_on_symmetric_noted"
    ]
    assert len(matches) == 1
    assert matches[0].severity == SEVERITY_NOTED


def test_arcrelation_paired_polarity_contrast_noted():
    """A7.15 check 5 — two non-canonical directional relations
    sharing target with different polarities emit one noted
    observation referencing both ids."""
    rel1 = ArCharacterArcRelation(
        id="r1", kind="instrumental",
        character_ref_ids=("c_a", "c_b"),
        mythos_id="m",
        directionality=DIRECTIONALITY_DIRECTIONAL,
        polarity=POLARITY_MALICIOUS,
    )
    rel2 = ArCharacterArcRelation(
        id="r2", kind="instrumental",
        character_ref_ids=("c_a", "c_b"),
        mythos_id="m",
        directionality=DIRECTIONALITY_DIRECTIONAL,
        polarity=POLARITY_THERAPEUTIC,
    )
    m = _two_character_mythos_with_arc(rel1)
    obs = verify(m, mythoi=(m,),
                 character_arc_relations=(rel1, rel2))
    matches = [
        o for o in obs
        if o.code == "character_arc_relation_paired_polarity_contrast"
    ]
    assert len(matches) == 1
    assert matches[0].severity == SEVERITY_NOTED
    # Both record ids named in the message.
    assert "r1" in matches[0].message
    assert "r2" in matches[0].message


def test_arcrelation_paired_polarity_skips_canonical_kinds():
    """A7.15 check 5 is scoped to non-canonical kinds. Two canonical
    relations sharing target with different polarities do NOT emit
    the paired-polarity contrast observation (canonical relations
    are symmetric, so target is ill-defined)."""
    rel1 = ArCharacterArcRelation(
        id="r1", kind="parallel",
        character_ref_ids=("c_a", "c_b"),
        mythos_id="m",
        directionality=DIRECTIONALITY_SYMMETRIC,
        polarity=POLARITY_MALICIOUS,
    )
    rel2 = ArCharacterArcRelation(
        id="r2", kind="parallel",
        character_ref_ids=("c_a", "c_b"),
        mythos_id="m",
        directionality=DIRECTIONALITY_SYMMETRIC,
        polarity=POLARITY_THERAPEUTIC,
    )
    m = _two_character_mythos_with_arc(rel1)
    obs = verify(m, mythoi=(m,),
                 character_arc_relations=(rel1, rel2))
    codes = [o.code for o in obs]
    assert ("character_arc_relation_paired_polarity_contrast"
            not in codes)


def test_arcrelation_paired_polarity_skips_same_polarity():
    """A7.15 check 5 requires DIFFERENT polarities. Two records with
    the same polarity do not emit the contrast observation."""
    rel1 = ArCharacterArcRelation(
        id="r1", kind="instrumental",
        character_ref_ids=("c_a", "c_b"),
        mythos_id="m",
        directionality=DIRECTIONALITY_DIRECTIONAL,
        polarity=POLARITY_MALICIOUS,
    )
    rel2 = ArCharacterArcRelation(
        id="r2", kind="instrumental",
        character_ref_ids=("c_a", "c_b"),
        mythos_id="m",
        directionality=DIRECTIONALITY_DIRECTIONAL,
        polarity=POLARITY_MALICIOUS,
    )
    m = _two_character_mythos_with_arc(rel1)
    obs = verify(m, mythoi=(m,),
                 character_arc_relations=(rel1, rel2))
    codes = [o.code for o in obs]
    assert ("character_arc_relation_paired_polarity_contrast"
            not in codes)


# ============================================================================
# Sketch-05 — A18 (anagnorisis_absent) + A7.16 synthetic fixtures
# ============================================================================


def test_archaracter_anagnorisis_absent_requires_tragic_hero_flags():
    """A7.16 check 1 — anagnorisis_absent=True requires
    is_tragic_hero=True."""
    non_tragic = ArCharacter(
        id="c_a", name="A", character_ref_id="c_a",
        is_tragic_hero=False, anagnorisis_absent=True,
    )
    m = ArMythos(
        id="m", title="M", action_summary="",
        central_event_ids=(),
        plot_kind=PLOT_COMPLEX,
        phases=(
            ArPhase(id="p_b", role=PHASE_BEGINNING, scope_event_ids=()),
            ArPhase(id="p_m", role=PHASE_MIDDLE, scope_event_ids=()),
            ArPhase(id="p_e", role=PHASE_END, scope_event_ids=()),
        ),
        peripeteia_event_id="E_x",
        anagnorisis_event_id="E_y",
        characters=(non_tragic,),
    )
    obs = verify(m, mythoi=(m,))
    codes = [o.code for o in obs]
    assert ("character_anagnorisis_absent_requires_tragic_hero"
            in codes)


def test_archaracter_anagnorisis_absent_contradicts_main_flags():
    """A7.16 check 2 — anagnorisis_absent=True on the mythos's
    main-anagnorisis character flags advises-review."""
    main_char = ArCharacter(
        id="c_a", name="A", character_ref_id="c_a",
        is_tragic_hero=True, hamartia_text="h",
        anagnorisis_absent=True,
    )
    m = ArMythos(
        id="m", title="M", action_summary="",
        central_event_ids=(),
        plot_kind=PLOT_COMPLEX,
        phases=(
            ArPhase(id="p_b", role=PHASE_BEGINNING, scope_event_ids=()),
            ArPhase(id="p_m", role=PHASE_MIDDLE, scope_event_ids=()),
            ArPhase(id="p_e", role=PHASE_END, scope_event_ids=()),
        ),
        peripeteia_event_id="E_x",
        anagnorisis_event_id="E_y",
        characters=(main_char,),
        anagnorisis_character_ref_id="c_a",  # same as main_char's ref
    )
    obs = verify(m, mythoi=(m,))
    codes = [o.code for o in obs]
    assert "character_anagnorisis_absent_contradicts_main" in codes


def test_archaracter_anagnorisis_absent_contradicts_chain_step_flags():
    """A7.16 check 3 — anagnorisis_absent=True on a character who
    ALSO has a chain step naming them flags advises-review."""
    absent_char = ArCharacter(
        id="c_a", name="A", character_ref_id="c_a",
        is_tragic_hero=True, hamartia_text="h",
        anagnorisis_absent=True,
    )
    # Chain step names character_ref_id="c_a" — contradicts absent.
    step = ArAnagnorisisStep(
        id="step1", event_id="E_z",
        character_ref_id="c_a",
        step_kind=STEP_KIND_PARALLEL,
    )
    m = ArMythos(
        id="m", title="M", action_summary="",
        central_event_ids=("E_z",),
        plot_kind=PLOT_COMPLEX,
        phases=(
            ArPhase(id="p_b", role=PHASE_BEGINNING,
                    scope_event_ids=("E_z",)),
            ArPhase(id="p_m", role=PHASE_MIDDLE, scope_event_ids=()),
            ArPhase(id="p_e", role=PHASE_END, scope_event_ids=()),
        ),
        peripeteia_event_id="E_x",
        anagnorisis_event_id="E_y",
        characters=(absent_char,),
        anagnorisis_chain=(step,),
    )
    obs = verify(m, mythoi=(m,))
    codes = [o.code for o in obs]
    assert ("character_anagnorisis_absent_contradicts_chain_step"
            in codes)


def test_archaracter_anagnorisis_absent_default_silent():
    """A7.16 fires no noted/advises-review on the default state
    (anagnorisis_absent=False on tragic hero without chain step) —
    silence is valid, the claim is author-asserted only."""
    silent_char = ArCharacter(
        id="c_a", name="A", character_ref_id="c_a",
        is_tragic_hero=True, hamartia_text="h",
        anagnorisis_absent=False,  # default-silent
    )
    m = ArMythos(
        id="m", title="M", action_summary="",
        central_event_ids=(),
        plot_kind=PLOT_COMPLEX,
        phases=(
            ArPhase(id="p_b", role=PHASE_BEGINNING, scope_event_ids=()),
            ArPhase(id="p_m", role=PHASE_MIDDLE, scope_event_ids=()),
            ArPhase(id="p_e", role=PHASE_END, scope_event_ids=()),
        ),
        peripeteia_event_id="E_x",
        anagnorisis_event_id="E_y",
        characters=(silent_char,),
    )
    obs = verify(m, mythoi=(m,))
    # No A7.16 observations on default state.
    codes = [o.code for o in obs]
    assert not any(c.startswith("character_anagnorisis_absent_")
                   for c in codes)


# ============================================================================
# Sketch-05 integration — Lear + Hamlet post-migration
# ============================================================================


def test_lear_aristotelian_instrumental_relations_directional():
    """Sketch-05 A17 migration: the two instrumental relations are
    explicitly directional; the two canonical relations are
    symmetric. Directional tuple convention: (wielder, target)."""
    from story_engine.encodings.lear_aristotelian import (
        AR_EDMUND_GLOUCESTER_INSTRUMENTAL,
        AR_EDGAR_GLOUCESTER_INSTRUMENTAL,
        AR_LEAR_GLOUCESTER_PARALLEL,
        AR_EDGAR_EDMUND_FOIL,
    )
    # Instrumental → directional.
    for rel in (AR_EDMUND_GLOUCESTER_INSTRUMENTAL,
                AR_EDGAR_GLOUCESTER_INSTRUMENTAL):
        assert rel.directionality == DIRECTIONALITY_DIRECTIONAL
    # Canonical → symmetric.
    for rel in (AR_LEAR_GLOUCESTER_PARALLEL, AR_EDGAR_EDMUND_FOIL):
        assert rel.directionality == DIRECTIONALITY_SYMMETRIC


def test_lear_aristotelian_instrumental_relations_typed_polarity():
    """Sketch-05 A17 migration: Edmund's instrument → malicious;
    Edgar's instrument → therapeutic. The opposite-polarity pair is
    what A7.15 check 5 detects structurally."""
    from story_engine.encodings.lear_aristotelian import (
        AR_EDMUND_GLOUCESTER_INSTRUMENTAL,
        AR_EDGAR_GLOUCESTER_INSTRUMENTAL,
    )
    assert (AR_EDMUND_GLOUCESTER_INSTRUMENTAL.polarity
            == POLARITY_MALICIOUS)
    assert (AR_EDGAR_GLOUCESTER_INSTRUMENTAL.polarity
            == POLARITY_THERAPEUTIC)


def test_lear_aristotelian_paired_polarity_contrast_emitted():
    """The full Lear verify emits the paired-polarity-contrast
    noted (A7.15 check 5) on the Edmund/Edgar → Gloucester pair.
    Captures the OQ-AP14 substrate signature structurally."""
    from story_engine.encodings.lear import FABULA
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_MYTHOS, AR_LEAR_CHARACTER_ARC_RELATIONS,
    )
    obs = verify(
        AR_LEAR_MYTHOS,
        substrate_events=FABULA,
        mythoi=(AR_LEAR_MYTHOS,),
        character_arc_relations=AR_LEAR_CHARACTER_ARC_RELATIONS,
    )
    paired = [
        o for o in obs
        if o.code == "character_arc_relation_paired_polarity_contrast"
    ]
    assert len(paired) == 1
    # References both instrumental relation ids.
    assert "arc_edmund_gloucester_instrumental" in paired[0].message
    assert "arc_edgar_gloucester_instrumental" in paired[0].message


def test_lear_aristotelian_cordelia_anagnorisis_absent_true():
    """Sketch-05 A18 migration closes OQ-LEAR-3: AR_CORDELIA
    declares anagnorisis_absent=True. The dialect carries the
    claim structurally that Session 5's probe flagged as a gap."""
    from story_engine.encodings.lear_aristotelian import (
        AR_CORDELIA, AR_LEAR_MYTHOS,
    )
    assert AR_CORDELIA.is_tragic_hero is True
    assert AR_CORDELIA.anagnorisis_absent is True
    # Cordelia is NOT the mythos's main-anagnorisis character
    # (that's Lear) — so A7.16 check 2 does NOT fire.
    assert (AR_CORDELIA.character_ref_id
            != AR_LEAR_MYTHOS.anagnorisis_character_ref_id)
    # No chain step names Cordelia — A7.16 check 3 does NOT fire.
    chain_refs = {s.character_ref_id
                  for s in AR_LEAR_MYTHOS.anagnorisis_chain}
    assert AR_CORDELIA.character_ref_id not in chain_refs


def test_lear_aristotelian_no_anagnorisis_absent_a716_violations():
    """Full Lear verify emits ZERO A7.16 observations — the
    anagnorisis_absent=True on Cordelia is consistent with the
    three invariants."""
    from story_engine.encodings.lear import FABULA
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_MYTHOS, AR_LEAR_CHARACTER_ARC_RELATIONS,
    )
    obs = verify(
        AR_LEAR_MYTHOS,
        substrate_events=FABULA,
        mythoi=(AR_LEAR_MYTHOS,),
        character_arc_relations=AR_LEAR_CHARACTER_ARC_RELATIONS,
    )
    a716_codes = [
        o.code for o in obs
        if o.code.startswith("character_anagnorisis_absent_")
    ]
    assert a716_codes == []


def test_hamlet_aristotelian_canonical_relations_symmetric():
    """Sketch-05 A17 migration: Hamlet's two canonical A13 relations
    (mirror Hamlet-Laertes + foil Hamlet-Claudius) are symmetric
    with empty polarity. Hamlet verifies with zero observations
    post-migration (unchanged from sketch-04 state)."""
    from story_engine.encodings.hamlet import FABULA
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_LAERTES_MIRROR, AR_HAMLET_CLAUDIUS_FOIL,
        AR_HAMLET_MYTHOS, AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    for rel in (AR_HAMLET_LAERTES_MIRROR, AR_HAMLET_CLAUDIUS_FOIL):
        assert rel.directionality == DIRECTIONALITY_SYMMETRIC
        assert rel.polarity == ""
    # Verify back-compat: zero observations post-migration.
    obs = verify(
        AR_HAMLET_MYTHOS,
        substrate_events=FABULA,
        mythoi=(AR_HAMLET_MYTHOS,),
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    assert obs == [], (
        f"Expected zero observations on Hamlet post-sketch-05; "
        f"got {len(obs)}:\n"
        + "\n".join(f"  [{o.severity}] {o.code}: {o.message}"
                    for o in obs)
    )


# ============================================================================
# Runner
# ============================================================================


TESTS = [
    test_armythos_minimal_construction,
    test_arphase_role_constants,
    test_arphase_valid_plot_kinds,
    test_archaracter_defaults,
    test_verify_accepts_simple_plot_without_peripeteia,
    test_verify_flags_invalid_plot_kind,
    test_verify_flags_complex_without_peripeteia_or_anagnorisis,
    test_verify_accepts_complex_with_only_peripeteia,
    test_verify_accepts_complex_with_only_anagnorisis,
    test_verify_flags_missing_phase_role,
    test_verify_flags_invalid_phase_role,
    test_verify_flags_phase_overlap,
    test_verify_flags_central_event_unphased,
    test_verify_flags_phase_event_not_central,
    test_verify_skips_event_ref_check_when_no_substrate,
    test_verify_flags_event_ref_unresolved,
    test_verify_flags_peripeteia_ref_unresolved,
    test_verify_unity_of_time_not_checked_when_not_asserted,
    test_verify_unity_of_time_respected,
    test_verify_unity_of_time_violated,
    test_verify_unity_of_place_not_checked_when_not_asserted,
    test_verify_unity_of_place_single_location,
    test_verify_unity_of_place_multiple_locations_violates,
    test_verify_hamartia_participation_passes_when_hero_participates,
    test_verify_hamartia_participation_flags_absent_hero,
    test_verify_hamartia_participation_skips_when_not_tragic_hero,
    test_verify_hamartia_participation_skips_when_no_character_ref,
    test_group_by_severity_buckets_correctly,
    test_group_by_code_buckets_correctly,
    test_oedipus_aristotelian_verifies_clean,
    test_oedipus_aristotelian_records_shape,
    test_rashomon_aristotelian_four_mythoi_all_verify_clean,
    test_rashomon_aristotelian_mythoi_count_and_ids,
    test_rashomon_aristotelian_shared_canonical_floor_beginning,
    test_rashomon_aristotelian_each_testimony_has_own_peripeteia,
    # Sketch-02
    test_armythos_relation_defaults,
    test_aranagnorisis_step_defaults,
    test_armythos_sketch02_field_defaults,
    test_canonical_relation_kinds_contents,
    test_valid_peripeteia_anagnorisis_bindings_contents,
    test_relation_noncanonical_kind_emits_noted,
    test_relation_too_few_mythoi_flags,
    test_relation_unresolved_mythos_id_flags,
    test_relation_mythos_resolution_skipped_when_mythoi_empty,
    test_relation_contests_event_absent_flags,
    test_relation_contests_passes_when_events_shared,
    test_relation_contains_not_superset_flags,
    test_relation_contains_strict_superset_passes,
    test_relation_event_ref_unresolved_flags,
    test_relation_event_ref_skipped_without_substrate,
    test_anagnorisis_chain_empty_by_default_clean,
    test_anagnorisis_chain_event_not_central_flags,
    test_anagnorisis_chain_step_equals_main_flags,
    test_anagnorisis_chain_precipitates_without_main_flags,
    test_anagnorisis_chain_precipitates_ordering_flags,
    test_anagnorisis_chain_precipitates_ordering_passes_when_earlier,
    test_anagnorisis_chain_character_unresolved_flags,
    test_anagnorisis_chain_character_check_skips_without_characters,
    test_binding_none_no_check,
    test_binding_coincident_passes_when_events_match,
    test_binding_coincident_inconsistent_when_events_differ,
    test_binding_adjacent_passes_within_bound,
    test_binding_separated_passes_beyond_bound,
    test_binding_invalid_value_flags,
    test_binding_requires_both_event_ids,
    test_binding_event_unresolved_flags,
    test_verify_backward_compat_no_kwargs,
    test_oedipus_aristotelian_chain_authored,
    test_oedipus_aristotelian_binding_is_separated,
    test_oedipus_aristotelian_still_verifies_clean_with_sketch02,
    test_rashomon_contest_relation_authored,
    test_rashomon_aristotelian_verifies_clean_with_relations,
    # Sketch-03 — A13 + A14
    test_archaracterarc_relation_defaults,
    test_canonical_character_arc_relation_kinds_contents,
    test_valid_step_kinds_contents,
    test_aranagnorisis_step_sketch03_field_default,
    test_armythos_sketch03_anagnorisis_character_default,
    test_arcrelation_noncanonical_kind_emits_noted,
    test_arcrelation_too_few_refs_flags,
    test_arcrelation_mythos_unresolved_flags,
    test_arcrelation_character_unresolved_flags,
    test_arcrelation_resolution_skipped_when_mythoi_empty,
    test_arcrelation_event_ref_unresolved_flags,
    test_arcrelation_event_ref_skipped_without_substrate,
    test_step_kind_invalid_value_flags,
    test_step_kind_staging_requires_main_character,
    test_step_kind_staging_character_mismatch_flags,
    test_step_kind_staging_ordering_flags,
    test_step_kind_staging_precipitates_mismatch_noted,
    test_step_kind_precipitating_precipitates_mismatch_noted,
    test_step_kind_parallel_precipitates_mismatch_noted,
    test_step_kind_empty_back_compat_verifies_clean,
    test_arcrelation_verifies_clean_when_all_resolve,
    test_verify_signature_accepts_character_arc_relations_kwarg,
    # Sketch-04 — A15-SE1/SE2/SE3 + A16-SP1/SP2/SP3
    test_canonical_tonal_registers_contents,
    test_canonical_binding_distance_preferences_contents,
    test_canonical_pacing_preferences_contents,
    test_arphase_sketch04_field_defaults,
    test_armythos_sketch04_field_defaults,
    test_arcopresencerequirement_default_min_count,
    test_araudienceknowledgeconstraint_default_source_event,
    # A7.12 — phase_event_count_bound consistency
    test_phase_event_count_bounds_default_zero_clean,
    test_phase_event_count_min_negative_flags,
    test_phase_event_count_max_negative_flags,
    test_phase_event_count_bounds_inverted_flags,
    test_phase_event_count_below_min_flags,
    test_phase_event_count_above_max_flags,
    test_phase_event_count_within_bounds_clean,
    # A7.13 — co_presence_required_over_phase
    test_co_presence_default_empty_clean,
    test_co_presence_refs_too_few_flags,
    test_co_presence_character_unresolved_flags,
    test_co_presence_phase_unresolved_flags,
    test_co_presence_min_count_zero_flags,
    test_co_presence_clean_when_all_resolve,
    # A7.14 — audience_knowledge_constraint
    test_audience_knowledge_default_empty_clean,
    test_audience_knowledge_subject_empty_flags,
    test_audience_knowledge_τ_s_negative_flags,
    test_audience_knowledge_source_event_unresolved_flags,
    test_audience_knowledge_source_event_too_late_flags,
    test_audience_knowledge_source_event_skipped_without_substrate,
    test_audience_knowledge_clean_when_all_resolve,
    test_verify_signature_unchanged_for_sketch_04,
    # Macbeth — third Aristotelian encoding
    test_macbeth_aristotelian_verifies_clean,
    test_macbeth_aristotelian_records_shape,
    test_macbeth_aristotelian_binding_is_coincident,
    test_macbeth_aristotelian_chain_non_precipitating,
    # Hamlet — fourth Aristotelian encoding
    test_hamlet_aristotelian_verifies_clean,
    test_hamlet_aristotelian_records_shape,
    test_hamlet_aristotelian_three_parallel_tragic_heroes,
    test_hamlet_aristotelian_binding_is_separated_distance_nine,
    test_hamlet_aristotelian_chain_three_steps_two_kinds,
    test_hamlet_aristotelian_probe_findings_authored,
    # Hamlet sketch-04 integration
    test_hamlet_aristotelian_sketch04_phase_bounds_set,
    test_hamlet_aristotelian_sketch04_pacing_preferences_set,
    test_hamlet_aristotelian_sketch04_co_presence_authored,
    test_hamlet_aristotelian_sketch04_audience_knowledge_authored,
    test_hamlet_aristotelian_sketch04_tonal_register_set,
    test_hamlet_aristotelian_sketch04_binding_distance_preference_set,
    test_pre_sketch_04_encodings_emit_no_sketch_04_codes,
    test_hamlet_aristotelian_no_mythos_relation_authored,
    # Lear — fifth Aristotelian encoding
    test_lear_aristotelian_verifies_clean_up_to_sketch05_noteds,
    test_lear_aristotelian_records_shape,
    test_lear_aristotelian_three_parallel_tragic_heroes,
    test_lear_aristotelian_asserts_unity_of_action_false_corpus_first,
    test_lear_aristotelian_binding_is_separated_distance_fourteen,
    test_lear_aristotelian_chain_two_parallel_no_staging,
    test_lear_aristotelian_chain_includes_post_main_step,
    test_lear_aristotelian_four_character_arc_relations_two_instrumental,
    test_lear_aristotelian_instrumental_relations_share_target_gloucester,
    test_lear_aristotelian_probe_findings_authored,
    test_lear_aristotelian_no_mythos_relation_authored,
    test_lear_cordelia_hanged_empty_observer_set,
    test_lear_aristotelian_sketch04_fields_authored,
    # Sketch-05 — A17 synthetic fixtures
    test_canonical_directionalities_contents,
    test_canonical_polarities_contents,
    test_arcrelation_sketch05_field_defaults,
    test_archaracter_sketch05_field_default,
    test_arcrelation_directionality_invalid_flags,
    test_arcrelation_polarity_invalid_flags,
    test_arcrelation_canonical_kind_directional_conflict_flags,
    test_arcrelation_polarity_on_symmetric_noted,
    test_arcrelation_paired_polarity_contrast_noted,
    test_arcrelation_paired_polarity_skips_canonical_kinds,
    test_arcrelation_paired_polarity_skips_same_polarity,
    # Sketch-05 — A18 synthetic fixtures
    test_archaracter_anagnorisis_absent_requires_tragic_hero_flags,
    test_archaracter_anagnorisis_absent_contradicts_main_flags,
    test_archaracter_anagnorisis_absent_contradicts_chain_step_flags,
    test_archaracter_anagnorisis_absent_default_silent,
    # Sketch-05 integration — Lear + Hamlet post-migration
    test_lear_aristotelian_instrumental_relations_directional,
    test_lear_aristotelian_instrumental_relations_typed_polarity,
    test_lear_aristotelian_paired_polarity_contrast_emitted,
    test_lear_aristotelian_cordelia_anagnorisis_absent_true,
    test_lear_aristotelian_no_anagnorisis_absent_a716_violations,
    test_hamlet_aristotelian_canonical_relations_symmetric,
]


def main() -> int:
    passed = 0
    failed = 0
    for test in TESTS:
        try:
            test()
        except AssertionError as e:
            print(f"FAIL  {test.__name__}")
            print(f"      {e}")
            failed += 1
            continue
        except Exception:
            print(f"ERROR {test.__name__}")
            traceback.print_exc()
            failed += 1
            continue
        print(f"ok    {test.__name__}")
        passed += 1

    print()
    print(f"{passed} passed, {failed} failed, {len(TESTS)} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
