"""
test_draft_convergence.py — the convergence controller, offline.

The control loop (stop conditions, splicing, score trajectory) is pure
once evaluate_fn / repair_fn / plan_fn are injected. We inject fakes
(scripted score sequences, a fake planner, a marker repairer) and pin
the loop's behavior without any API.
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.draft_convergence import converge, assemble
from story_engine.core.draft_repair import RepairDirective


class _FakeReport:
    def __init__(self, score):
        self.score = score
        self.findings = []


def _scenes():
    return [
        {"tau_d": 2, "event_id": "E_c", "prose": "third"},
        {"tau_d": 0, "event_id": "E_a", "prose": "first"},
        {"tau_d": 1, "event_id": "E_b", "prose": "second"},
    ]


def _scripted_eval(scores):
    """evaluate_fn returning the next scripted score each call."""
    box = {"i": 0}

    def ev(_text):
        i = min(box["i"], len(scores) - 1)
        box["i"] += 1
        return _FakeReport(scores[i])
    return ev


def _plan_one(event_id):
    """plan_fn that always asks to repair one fixed event (until the
    caller stops it via score/target)."""
    def plan(_report, _mythos):
        return [RepairDirective(event_id=event_id, dimension="anti_recognition",
                                instruction="fix", authored="X (anti)")]
    return plan


def _plan_none(_report, _mythos):
    return []


def _marker_repair(d):
    return f"REPAIRED::{d.event_id}"


def test_assemble_orders_by_tau_d():
    assert assemble(_scenes()) == "first\n\nsecond\n\nthird"


def test_converges_to_target():
    run = converge(
        scenes=_scenes(), mythos=None,
        evaluate_fn=_scripted_eval([0.8, 0.9, 1.0]),
        repair_fn=_marker_repair, plan_fn=_plan_one("E_a"),
        max_iters=5, target=1.0,
    )
    assert run.final_score == 1.0
    assert run.history[-1].stopped == "target reached"
    assert run.initial_score == 0.8
    assert run.improved == pytest_approx(0.2)


def test_stops_on_no_improvement():
    run = converge(
        scenes=_scenes(), mythos=None,
        evaluate_fn=_scripted_eval([0.8, 0.8, 0.8]),
        repair_fn=_marker_repair, plan_fn=_plan_one("E_a"),
        max_iters=5, target=1.0,
    )
    assert len(run.history) == 2
    assert run.history[-1].stopped == "no improvement over previous round"


def test_stops_when_no_directives():
    run = converge(
        scenes=_scenes(), mythos=None,
        evaluate_fn=_scripted_eval([0.7]),
        repair_fn=_marker_repair, plan_fn=_plan_none,
        max_iters=5, target=1.0,
    )
    assert len(run.history) == 1
    assert run.history[0].stopped == "no localizable drift remaining"


def test_splices_repaired_prose():
    scenes = _scenes()
    converge(
        scenes=scenes, mythos=None,
        evaluate_fn=_scripted_eval([0.5, 1.0]),
        repair_fn=_marker_repair, plan_fn=_plan_one("E_a"),
        max_iters=5, target=1.0,
    )
    spliced = next(s for s in scenes if s["event_id"] == "E_a")
    assert spliced["prose"] == "REPAIRED::E_a"
    # untouched scenes keep their prose
    assert next(s for s in scenes if s["event_id"] == "E_b")["prose"] == "second"


def test_respects_max_iters():
    run = converge(
        scenes=_scenes(), mythos=None,
        evaluate_fn=_scripted_eval([0.5, 0.6, 0.7]),
        repair_fn=_marker_repair, plan_fn=_plan_one("E_a"),
        max_iters=3, target=1.0,
    )
    assert len(run.history) == 3
    assert run.history[-1].stopped == "max_iters reached"


def test_no_op_repair_leaves_scene():
    scenes = _scenes()
    converge(
        scenes=scenes, mythos=None,
        evaluate_fn=_scripted_eval([0.5, 0.5]),
        repair_fn=lambda d: "",          # repair declines
        plan_fn=_plan_one("E_a"), max_iters=5, target=1.0,
    )
    assert next(s for s in scenes if s["event_id"] == "E_a")["prose"] == "first"


def pytest_approx(x, eps=1e-9):
    class _A:
        def __eq__(self, other):
            return abs(other - x) < eps
    return _A()


TESTS = [
    test_assemble_orders_by_tau_d,
    test_converges_to_target,
    test_stops_on_no_improvement,
    test_stops_when_no_directives,
    test_splices_repaired_prose,
    test_respects_max_iters,
    test_no_op_repair_leaves_scene,
]


def main() -> int:
    passed = failed = 0
    for fn in TESTS:
        try:
            fn()
        except Exception:
            failed += 1
            print(f"FAIL  {fn.__name__}")
            traceback.print_exc()
        else:
            passed += 1
            print(f"ok    {fn.__name__}")
    print(f"\n{passed} passed, {failed} failed, {passed + failed} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
