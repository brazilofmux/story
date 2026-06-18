"""
test_dramatica_repair.py — Dramatica repair localization, offline.

plan_repairs is pure Python: given a DramaticaFidelityReport's drifts +
the storyform, does it localize the ending-shape drifts (judgment,
outcome, resolve) to the right scene and rebuild the intended shape from
the storyform's own dynamics — while declining to localize the diffuse
ones (throughline coverage, MC identity)?
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.dramatica_evaluator import (
    DramaticaReading, compare_to_storyform,
)
from story_engine.core.dramatica_repair import plan_repairs, _ending_event
from story_engine.core.dramatica_generation import DramaticaStoryform
from story_engine.encodings.rocky import SJUZHET
from story_engine.encodings import rocky_dramatica_complete as RD


def _storyform():
    return DramaticaStoryform(
        title="Rocky", action_summary="x",
        domain_assignments=RD.DOMAIN_ASSIGNMENTS, signposts=RD.ALL_SIGNPOSTS,
        dynamics=RD.DYNAMIC_STORY_POINTS, story_goal="g", story_consequence="c",
        canonical_ending=RD.CANONICAL_ENDING, act_event_ids=RD.ACT_EVENT_IDS,
    )


def _tragic_drift_read():
    """The prose collapsed the personal triumph into a tragedy — judgment
    Good→Bad, resolve Steadfast→Changed, ending → tragedy."""
    return DramaticaReading(
        story_goal="win the title", outcome="failure", judgment="bad",
        ending_shape="tragedy", main_character="Rocky", mc_resolve="changed",
        throughlines_present=["overall", "main character",
                              "influence character", "relationship"],
        overall_read="a man broken by the fight.",
    )


def _faithful_read():
    return DramaticaReading(
        story_goal="a clean title defense", outcome="failure", judgment="good",
        ending_shape="personal triumph", main_character="Rocky",
        mc_resolve="steadfast",
        throughlines_present=["overall", "main character",
                              "influence character", "relationship"],
        overall_read="loses the fight, wins everything else.")


def test_ending_event_is_last_beat_of_final_act():
    """The ending shape is sealed at the last staged beat of act 4."""
    target = _ending_event(_storyform(), SJUZHET)
    # act 4's last staged event is the final 'no rematch' coda
    assert target == "E_no_rematch"


def test_faithful_read_needs_no_repair():
    report = compare_to_storyform(_faithful_read(), _storyform())
    assert plan_repairs(report, _storyform(), SJUZHET) == []


def test_tragic_drift_localizes_to_the_ending():
    report = compare_to_storyform(_tragic_drift_read(), _storyform())
    directives = plan_repairs(report, _storyform(), SJUZHET)
    assert len(directives) == 1
    d = directives[0]
    assert d.event_id == "E_no_rematch"          # the ending scene
    assert d.dimension == "dramatica_shape"
    # bundles the drifted ending dimensions
    for dim in ("judgment", "mc_resolve", "ending_shape"):
        assert dim in d.authored


def test_directive_rebuilds_the_intended_shape():
    report = compare_to_storyform(_tragic_drift_read(), _storyform())
    instr = plan_repairs(report, _storyform(), SJUZHET)[0].instruction
    # in Dramatica's own terms, not Aristotle's
    assert "PERIPETEIA" not in instr and "anagnorisis" not in instr.lower()
    assert "OUTCOME = FAILURE" in instr
    assert "JUDGMENT = GOOD" in instr
    assert "personal triumph" in instr.lower()
    assert "not a tragedy" in instr.lower()
    assert "HOLDS their essential nature" in instr   # steadfast


def test_diffuse_throughline_loss_is_not_localized():
    """If only throughlines drop (a diffuse loss), no scene directive is
    forced — mirrors the Aristotelian repair declining diffuse losses."""
    read = DramaticaReading(
        story_goal="g", outcome="failure", judgment="good",
        ending_shape="personal triumph", main_character="Rocky",
        mc_resolve="steadfast",
        throughlines_present=["main character"],   # lost 3 throughlines
        overall_read="x")
    report = compare_to_storyform(read, _storyform())
    # throughline losses exist…
    assert any(f.dimension == "throughline" and f.verdict == "lost"
               for f in report.findings)
    # …but they are not localized to a scene.
    assert plan_repairs(report, _storyform(), SJUZHET) == []


def test_directive_targets_a_real_staged_scene():
    report = compare_to_storyform(_tragic_drift_read(), _storyform())
    staged = {s.event_id for s in SJUZHET}
    for d in plan_repairs(report, _storyform(), SJUZHET):
        assert d.event_id in staged


TESTS = [
    test_ending_event_is_last_beat_of_final_act,
    test_faithful_read_needs_no_repair,
    test_tragic_drift_localizes_to_the_ending,
    test_directive_rebuilds_the_intended_shape,
    test_diffuse_throughline_loss_is_not_localized,
    test_directive_targets_a_real_staged_scene,
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
