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
    ArAnagnorisisStep, ArCharacter, ArMythos, ArMythosRelation,
    ArObservation, ArPhase,
    BINDING_ADJACENT, BINDING_COINCIDENT, BINDING_SEPARATED,
    CANONICAL_RELATION_KINDS,
    PHASE_BEGINNING, PHASE_END, PHASE_MIDDLE,
    PLOT_COMPLEX, PLOT_SIMPLE,
    RELATION_CONTAINS, RELATION_CONTESTS, RELATION_PARALLEL,
    SEVERITY_ADVISES_REVIEW, SEVERITY_NOTED,
    VALID_PERIPETEIA_ANAGNORISIS_BINDINGS,
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
    # Macbeth — third Aristotelian encoding
    test_macbeth_aristotelian_verifies_clean,
    test_macbeth_aristotelian_records_shape,
    test_macbeth_aristotelian_binding_is_coincident,
    test_macbeth_aristotelian_chain_non_precipitating,
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
