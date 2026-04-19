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
    ArCharacter, ArMythos, ArObservation, ArPhase,
    PHASE_BEGINNING, PHASE_END, PHASE_MIDDLE,
    PLOT_COMPLEX, PLOT_SIMPLE,
    SEVERITY_ADVISES_REVIEW, SEVERITY_NOTED,
    VALID_PHASE_ROLES, VALID_PLOT_KINDS,
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
