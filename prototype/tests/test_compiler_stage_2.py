"""
test_compiler_stage_2.py — tests for the stage-2 feasibility gate per
compilation-stage-2-sketch-01.

Synthetic-fixture tests pin the function's contract — CS4 arithmetic,
CS6 structured-error posture, relaxation computation, field-default
semantics. Corpus integration tests exercise the real Aristotelian
encodings against a range of word budgets.

Run:
    cd prototype
    python3 -m tests.test_compiler_stage_2
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.aristotelian import ArMythos, ArPhase
from story_engine.core.compiler import (
    DEFAULT_W_MIN_PER_EVENT,
    FeasibilityResult,
    InfeasibilityError,
    stage_2_feasibility,
)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


def _phase(
    id: str,
    role: str,
    event_count: int,
    *,
    min_event_count: int = 0,
    max_event_count: int = 0,
) -> ArPhase:
    return ArPhase(
        id=id, role=role,
        scope_event_ids=tuple(f"E_{id}_{i}" for i in range(event_count)),
        min_event_count=min_event_count,
        max_event_count=max_event_count,
    )


def _mythos(phases: tuple) -> ArMythos:
    """Minimal ArMythos with whatever phases you need. Other fields
    default; the stage-2 gate only reads `phases`."""
    central = tuple(
        eid for phase in phases for eid in phase.scope_event_ids
    )
    return ArMythos(
        id="m_test", title="Test",
        action_summary="test action",
        central_event_ids=central or ("E_placeholder",),
        plot_kind="simple",
        phases=phases,
    )


def _codes(result: FeasibilityResult) -> set:
    return {e.code for e in result.errors}


# ----------------------------------------------------------------------------
# Hamlet worked example (sketch-03 canonical case)
# ----------------------------------------------------------------------------


def test_hamlet_feasible_at_generous_budget():
    from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS
    result = stage_2_feasibility(AR_HAMLET_MYTHOS, word_budget=10000)
    assert result.is_feasible
    assert result.errors == ()
    assert result.aggregate_min_events == 24
    assert result.aggregate_max_events == 39  # all phases bounded
    assert result.min_word_floor == 4800
    assert result.word_budget == 10000
    assert result.W_min_per_event == DEFAULT_W_MIN_PER_EVENT


def test_hamlet_feasible_at_exact_floor():
    """Tight-fit case: word_budget == min_word_floor. No slack but
    still feasible."""
    from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS
    result = stage_2_feasibility(AR_HAMLET_MYTHOS, word_budget=4800)
    assert result.is_feasible
    assert result.min_word_floor == 4800


def test_hamlet_infeasible_by_one_word():
    """Boundary case: word_budget one word short of the floor.
    Relaxation should name a 1-word increase OR 1-event reduction."""
    from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS
    result = stage_2_feasibility(AR_HAMLET_MYTHOS, word_budget=4799)
    assert not result.is_feasible
    assert "budget_below_floor" in _codes(result)
    err = next(
        e for e in result.errors if e.code == "budget_below_floor"
    )
    assert "increase word_budget by >= 1 words" in err.relaxations
    assert any(
        "reduce aggregate phase.min_event_count by >= 1 events" in rel
        for rel in err.relaxations
    )


def test_hamlet_infeasible_at_thin_budget():
    """The sketch's canonical infeasible case: word_budget=3000 vs
    floor=4800; deficit 1800 words; event-deficit = ceil(1800/200)=9."""
    from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS
    result = stage_2_feasibility(AR_HAMLET_MYTHOS, word_budget=3000)
    assert not result.is_feasible
    err = next(
        e for e in result.errors if e.code == "budget_below_floor"
    )
    assert "increase word_budget by >= 1800 words" in err.relaxations
    assert any(
        "reduce aggregate phase.min_event_count by >= 9 events" in rel
        for rel in err.relaxations
    )


def test_budget_below_floor_names_all_three_constraints():
    """CS6: conflicting_constraints should name all three arithmetic
    operands — word_budget, aggregate_min_events, W_min_per_event."""
    from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS
    result = stage_2_feasibility(AR_HAMLET_MYTHOS, word_budget=1000)
    err = next(
        e for e in result.errors if e.code == "budget_below_floor"
    )
    joined = " ".join(err.conflicting_constraints)
    assert "word_budget=1000" in joined
    assert "aggregate_min_events=24" in joined
    assert "W_min_per_event=200" in joined


def test_deficit_ceiling_computation_rounds_up():
    """Event-deficit = ceil(word_deficit / W_min_per_event). Not
    floor. A 199-word deficit → 1 event (not 0)."""
    from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS
    # Hamlet floor = 4800; pick a budget 199 words below.
    result = stage_2_feasibility(AR_HAMLET_MYTHOS, word_budget=4601)
    err = next(
        e for e in result.errors if e.code == "budget_below_floor"
    )
    # 199-word deficit, W=200 → ceil(199/200) = 1 event.
    assert any(
        "reduce aggregate phase.min_event_count by >= 1 events" in rel
        for rel in err.relaxations
    )


# ----------------------------------------------------------------------------
# Synthetic — S2F3 per-phase gates
# ----------------------------------------------------------------------------


def test_synthetic_phase_bounds_inverted():
    """S2F3: a phase with min > max is infeasible independent of
    budget. Both relaxations are offered (raise max or lower min)."""
    phases = (
        _phase("ph_bad", "beginning", event_count=5,
               min_event_count=10, max_event_count=3),
    )
    m = _mythos(phases)
    result = stage_2_feasibility(m, word_budget=100_000)
    assert not result.is_feasible
    assert "phase_bounds_inverted" in _codes(result)
    err = next(
        e for e in result.errors if e.code == "phase_bounds_inverted"
    )
    assert any(
        "raise phases['ph_bad'].max_event_count to >= 10" in rel
        for rel in err.relaxations
    )
    assert any(
        "lower phases['ph_bad'].min_event_count to <= 3" in rel
        for rel in err.relaxations
    )


def test_synthetic_phase_authoring_below_min():
    """S2F3: a phase whose authored count falls below its declared
    min_event_count."""
    phases = (
        _phase("ph_thin", "beginning", event_count=3,
               min_event_count=8),
    )
    m = _mythos(phases)
    result = stage_2_feasibility(m, word_budget=100_000)
    assert not result.is_feasible
    assert "phase_authoring_below_min" in _codes(result)
    err = next(
        e for e in result.errors if e.code == "phase_authoring_below_min"
    )
    # 8 min - 3 authored = 5 event deficit
    assert any(
        "author >= 5 additional events" in rel for rel in err.relaxations
    )
    assert any(
        "lower phases['ph_thin'].min_event_count to <= 3" in rel
        for rel in err.relaxations
    )


def test_synthetic_phase_authoring_above_max():
    """S2F3: a phase whose authored count exceeds its declared
    max_event_count."""
    phases = (
        _phase("ph_fat", "middle", event_count=20,
               max_event_count=5),
    )
    m = _mythos(phases)
    result = stage_2_feasibility(m, word_budget=100_000)
    assert not result.is_feasible
    assert "phase_authoring_above_max" in _codes(result)
    err = next(
        e for e in result.errors if e.code == "phase_authoring_above_max"
    )
    # 20 authored - 5 max = 15 event excess
    assert any(
        "remove >= 15 events" in rel for rel in err.relaxations
    )


def test_multiple_errors_emitted_together():
    """Budget-floor + phase-inversion both fire on the same mythos.
    Stage 2 reports every independent infeasibility in one pass."""
    phases = (
        _phase("ph_inverted", "beginning", event_count=5,
               min_event_count=7, max_event_count=3),
        _phase("ph_normal", "middle", event_count=10,
               min_event_count=10, max_event_count=15),
    )
    m = _mythos(phases)
    # Budget below floor: aggregate_min = 7 + 10 = 17 → floor 3400.
    result = stage_2_feasibility(m, word_budget=500)
    codes = _codes(result)
    assert "phase_bounds_inverted" in codes
    assert "budget_below_floor" in codes
    assert not result.is_feasible


# ----------------------------------------------------------------------------
# Synthetic — S2F2 aggregate calculation + fallback
# ----------------------------------------------------------------------------


def test_aggregate_min_events_uses_bound_when_set():
    """When min_event_count > 0, the bound — not authoring — drives
    aggregate_min_events. (Bound=10, authored=5 → contribution 10.)"""
    phases = (
        _phase("ph_x", "beginning", event_count=5, min_event_count=10,
               max_event_count=20),
    )
    m = _mythos(phases)
    # Budget high enough to pass floor; phase authoring gate MUST
    # trip (5 < 10) — but aggregate_min is still 10, not 5.
    result = stage_2_feasibility(m, word_budget=100_000)
    assert result.aggregate_min_events == 10
    # Phase_authoring_below_min fires separately.
    assert "phase_authoring_below_min" in _codes(result)


def test_aggregate_min_events_falls_back_to_authored_count():
    """When min_event_count == 0 (default), aggregate_min uses
    len(scope_event_ids). S2F2 fallback — makes the gate meaningful
    against pre-sketch-04 encodings."""
    phases = (
        _phase("ph_1", "beginning", event_count=6),
        _phase("ph_2", "middle", event_count=6),
        _phase("ph_3", "end", event_count=4),
    )
    m = _mythos(phases)
    result = stage_2_feasibility(m, word_budget=100_000)
    assert result.aggregate_min_events == 16  # 6 + 6 + 4, all fallbacks
    assert result.min_word_floor == 3200       # 16 × 200


def test_aggregate_max_events_sum_when_all_bounded():
    phases = (
        _phase("ph_1", "beginning", event_count=3, min_event_count=3,
               max_event_count=5),
        _phase("ph_2", "middle", event_count=4, min_event_count=3,
               max_event_count=6),
        _phase("ph_3", "end", event_count=3, min_event_count=2,
               max_event_count=4),
    )
    m = _mythos(phases)
    result = stage_2_feasibility(m, word_budget=100_000)
    assert result.aggregate_max_events == 15  # 5 + 6 + 4


def test_aggregate_max_events_sentinel_when_any_phase_unbounded():
    """If any phase has max_event_count == 0 (default), aggregate_max
    is the unbounded sentinel 0 — regardless of other phases."""
    phases = (
        _phase("ph_1", "beginning", event_count=3, min_event_count=3,
               max_event_count=5),
        _phase("ph_2", "middle", event_count=4, min_event_count=3,
               max_event_count=0),  # unbounded
        _phase("ph_3", "end", event_count=3, min_event_count=2,
               max_event_count=4),
    )
    m = _mythos(phases)
    result = stage_2_feasibility(m, word_budget=100_000)
    assert result.aggregate_max_events == 0  # sentinel


# ----------------------------------------------------------------------------
# Input validation (exceptions reserved for malformed inputs)
# ----------------------------------------------------------------------------


def test_raises_on_negative_word_budget():
    m = _mythos((_phase("p", "beginning", event_count=1),))
    try:
        stage_2_feasibility(m, word_budget=-1)
    except ValueError as e:
        assert "word_budget" in str(e)
        return
    raise AssertionError("expected ValueError on negative word_budget")


def test_raises_on_zero_W_min_per_event():
    m = _mythos((_phase("p", "beginning", event_count=1),))
    try:
        stage_2_feasibility(m, word_budget=1000, W_min_per_event=0)
    except ValueError as e:
        assert "W_min_per_event" in str(e)
        return
    raise AssertionError("expected ValueError on zero W_min_per_event")


def test_raises_on_negative_W_min_per_event():
    m = _mythos((_phase("p", "beginning", event_count=1),))
    try:
        stage_2_feasibility(m, word_budget=1000, W_min_per_event=-10)
    except ValueError as e:
        assert "W_min_per_event" in str(e)
        return
    raise AssertionError(
        "expected ValueError on negative W_min_per_event"
    )


def test_accepts_zero_word_budget():
    """Zero is not negative — passes validation. For a mythos with
    no bounded phases and zero authoring, zero budget is feasible."""
    phases = (_phase("p", "beginning", event_count=0),)
    m = _mythos(phases)
    result = stage_2_feasibility(m, word_budget=0)
    assert result.is_feasible
    assert result.min_word_floor == 0


# ----------------------------------------------------------------------------
# W_min_per_event custom values
# ----------------------------------------------------------------------------


def test_custom_W_min_per_event_scales_floor():
    """Doubling W_min_per_event doubles the floor. Relaxations
    reflect the caller-specified value, not the default."""
    from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS
    result = stage_2_feasibility(
        AR_HAMLET_MYTHOS, word_budget=4800, W_min_per_event=400,
    )
    assert not result.is_feasible
    assert result.min_word_floor == 9600  # 24 × 400
    assert result.W_min_per_event == 400


# ----------------------------------------------------------------------------
# Corpus sanity — pre-sketch-04 Aristotelian encodings
# ----------------------------------------------------------------------------


def _corpus_mythoi() -> list:
    """All Aristotelian mythoi across the existing corpus. Hamlet
    declares A15-SE1 bounds; the others use the S2F2 fallback.
    Rashomon contributes four mythoi (one per contested account)."""
    from story_engine.encodings.oedipus_aristotelian import AR_OEDIPUS_MYTHOS
    from story_engine.encodings.macbeth_aristotelian import AR_MACBETH_MYTHOS
    from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS
    from story_engine.encodings.rashomon_aristotelian import AR_RASHOMON_MYTHOI
    return [
        ("oedipus", AR_OEDIPUS_MYTHOS),
        ("macbeth_aristotelian", AR_MACBETH_MYTHOS),
        ("hamlet", AR_HAMLET_MYTHOS),
    ] + [(f"rashomon/{m.id}", m) for m in AR_RASHOMON_MYTHOI]


def test_all_corpus_mythoi_feasible_at_generous_budget():
    """Corpus sanity: every Aristotelian mythos passes stage-2
    feasibility at word_budget=10,000. Catches regressions where a
    future encoding-migration accidentally bumps the aggregate floor
    past this bound."""
    failures = []
    for name, mythos in _corpus_mythoi():
        result = stage_2_feasibility(mythos, word_budget=10000)
        if not result.is_feasible:
            failures.append((name, [e.code for e in result.errors]))
    assert not failures, (
        f"corpus mythoi infeasible at W=10000: {failures}"
    )


def test_all_corpus_mythoi_infeasible_at_thin_budget():
    """Corpus sanity floor: every Aristotelian mythos FAILS at
    word_budget=500. Pins the 'stage 2 is a real gate' claim — a
    pathologically thin budget must trip the floor for every
    encoding, not silently pass."""
    passes = []
    for name, mythos in _corpus_mythoi():
        result = stage_2_feasibility(mythos, word_budget=500)
        if result.is_feasible:
            passes.append(name)
    assert not passes, (
        f"corpus mythoi feasible at W=500 (expected all to fail): "
        f"{passes}"
    )


def test_hamlet_floor_driven_by_bounds_not_authoring():
    """Hamlet is the only corpus encoding whose floor comes from
    A15-SE1 bounds rather than authoring. aggregate_min=24 from
    bounds (10+8+6), not 32 from authoring (13+11+8). This test
    pins that — if Hamlet's bounds get relaxed or removed, the test
    surfaces the change."""
    from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS
    authored_total = sum(
        len(p.scope_event_ids) for p in AR_HAMLET_MYTHOS.phases
    )
    assert authored_total == 32  # 13 + 11 + 8
    result = stage_2_feasibility(AR_HAMLET_MYTHOS, word_budget=10000)
    assert result.aggregate_min_events == 24  # bound-driven
    assert result.aggregate_min_events < authored_total


def test_pre_sketch_04_encodings_floor_driven_by_authoring():
    """Pre-sketch-04 encodings have no A15-SE1 bounds; their floor
    equals authored_count × W_min_per_event via S2F2 fallback.
    Sanity-pin: if a pre-sketch-04 encoding grows bounds later,
    this test will flag the change."""
    from story_engine.encodings.oedipus_aristotelian import AR_OEDIPUS_MYTHOS
    from story_engine.encodings.macbeth_aristotelian import AR_MACBETH_MYTHOS
    for m in (AR_OEDIPUS_MYTHOS, AR_MACBETH_MYTHOS):
        authored_total = sum(
            len(p.scope_event_ids) for p in m.phases
        )
        result = stage_2_feasibility(m, word_budget=10000)
        # Fallback path: aggregate_min == authored_total.
        assert result.aggregate_min_events == authored_total, (
            f"{m.id}: aggregate_min={result.aggregate_min_events} "
            f"but authored_total={authored_total}; S2F2 fallback "
            f"may be broken"
        )


# ----------------------------------------------------------------------------
# FeasibilityResult surface
# ----------------------------------------------------------------------------


def test_feasibility_result_echoes_inputs():
    from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS
    result = stage_2_feasibility(
        AR_HAMLET_MYTHOS, word_budget=7500, W_min_per_event=250,
    )
    assert result.word_budget == 7500
    assert result.W_min_per_event == 250


def test_feasibility_result_is_frozen():
    """Dataclass(frozen=True) — attempting to mutate raises
    FrozenInstanceError. The result is an immutable value."""
    from dataclasses import FrozenInstanceError
    from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS
    result = stage_2_feasibility(AR_HAMLET_MYTHOS, word_budget=10000)
    try:
        result.is_feasible = False  # type: ignore[misc]
    except FrozenInstanceError:
        return
    raise AssertionError(
        "FeasibilityResult should be frozen; mutation should raise"
    )


def test_infeasibility_error_is_frozen():
    from dataclasses import FrozenInstanceError
    err = InfeasibilityError(
        code="x", conflicting_constraints=(), message="",
    )
    try:
        err.code = "y"  # type: ignore[misc]
    except FrozenInstanceError:
        return
    raise AssertionError(
        "InfeasibilityError should be frozen; mutation should raise"
    )


# ----------------------------------------------------------------------------
# Test runner
# ----------------------------------------------------------------------------


TESTS = [
    # Hamlet worked example
    test_hamlet_feasible_at_generous_budget,
    test_hamlet_feasible_at_exact_floor,
    test_hamlet_infeasible_by_one_word,
    test_hamlet_infeasible_at_thin_budget,
    test_budget_below_floor_names_all_three_constraints,
    test_deficit_ceiling_computation_rounds_up,
    # S2F3 per-phase gates
    test_synthetic_phase_bounds_inverted,
    test_synthetic_phase_authoring_below_min,
    test_synthetic_phase_authoring_above_max,
    test_multiple_errors_emitted_together,
    # S2F2 aggregate calculation
    test_aggregate_min_events_uses_bound_when_set,
    test_aggregate_min_events_falls_back_to_authored_count,
    test_aggregate_max_events_sum_when_all_bounded,
    test_aggregate_max_events_sentinel_when_any_phase_unbounded,
    # Input validation
    test_raises_on_negative_word_budget,
    test_raises_on_zero_W_min_per_event,
    test_raises_on_negative_W_min_per_event,
    test_accepts_zero_word_budget,
    # Custom W_min_per_event
    test_custom_W_min_per_event_scales_floor,
    # Corpus sanity
    test_all_corpus_mythoi_feasible_at_generous_budget,
    test_all_corpus_mythoi_infeasible_at_thin_budget,
    test_hamlet_floor_driven_by_bounds_not_authoring,
    test_pre_sketch_04_encodings_floor_driven_by_authoring,
    # FeasibilityResult surface
    test_feasibility_result_echoes_inputs,
    test_feasibility_result_is_frozen,
    test_infeasibility_error_is_frozen,
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
