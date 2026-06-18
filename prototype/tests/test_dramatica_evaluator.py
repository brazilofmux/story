"""
test_dramatica_evaluator.py — Dramatica fidelity comparison, offline.

Stage 1 (decompile_dramatica) needs the API; the demo exercises it.
Stage 2 (compare_to_storyform) is pure Python: given a blind Dramatica
reading, does it correctly score round-trip fidelity against Rocky's
real storyform — and, crucially, hold Outcome and Judgment apart (the
non-tragedy axes an Aristotelian evaluator cannot see)?
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.dramatica_evaluator import (
    DramaticaReading, compare_to_storyform, _perspective_of,
)
from story_engine.core.dramatica_generation import DramaticaStoryform
from story_engine.encodings import rocky_dramatica_complete as RD


def _storyform():
    return DramaticaStoryform(
        title="Rocky", action_summary="x",
        domain_assignments=RD.DOMAIN_ASSIGNMENTS, signposts=RD.ALL_SIGNPOSTS,
        dynamics=RD.DYNAMIC_STORY_POINTS, story_goal="g", story_consequence="c",
        canonical_ending=RD.CANONICAL_ENDING,
    )


def _faithful_read():
    """A blind read that recovered Rocky's storyform: the goal fails, the
    judgment is good (personal triumph), Rocky steadfast, all four
    throughlines present."""
    return DramaticaReading(
        story_goal="a clean publicity title defense for Apollo Creed",
        outcome="failure", judgment="good", ending_shape="personal triumph",
        main_character="Rocky", mc_resolve="steadfast",
        influence_character="Apollo", relationship="Rocky and Adrian",
        throughlines_present=["overall", "main character",
                              "influence character", "relationship"],
        overall_read="he loses the fight and wins everything else.",
    )


def _tragic_drift_read():
    """A read where the prose collapsed the triumph into a tragedy — the
    exact failure mode the Aristotelian evaluator could NOT catch."""
    return DramaticaReading(
        story_goal="win the title", outcome="failure", judgment="bad",
        ending_shape="tragedy", main_character="Rocky", mc_resolve="changed",
        influence_character="", relationship="",
        throughlines_present=["main character"],
        overall_read="a man broken by a fight he could not win.",
    )


def test_perspective_detection():
    assert _perspective_of("T_overall_fight") == "overall"
    assert _perspective_of("T_mc_rocky") == "main character"
    assert _perspective_of("T_ic_apollo") == "influence character"
    assert _perspective_of("T_rel_rocky_adrian") == "relationship"


def test_faithful_read_scores_high():
    report = compare_to_storyform(_faithful_read(), _storyform())
    lost = [f for f in report.scored if f.verdict != "preserved"]
    assert lost == [], f"unexpected: {[(f.dimension, f.verdict) for f in lost]}"
    assert report.score == 1.0


def test_outcome_and_judgment_are_independent_axes():
    """The headline: a faithful Rocky read scores Outcome and Judgment
    separately, both preserved. Outcome is authored DUAL ({failure,
    success}); a 'failure' read lands a spanned pole, so it is preserved.
    Judgment is a plain binary 'good'."""
    report = compare_to_storyform(_faithful_read(), _storyform())
    by_dim = {f.dimension: f for f in report.findings}
    assert by_dim["outcome"].authored == "failure|success"   # dual span shown
    assert by_dim["outcome"].verdict == "preserved"          # failure ∈ span
    assert by_dim["judgment"].authored == "good"
    assert by_dim["judgment"].verdict == "preserved"


def test_tragic_drift_is_caught():
    """If the prose turns Rocky into a tragedy (judgment drifts to bad),
    the Dramatica evaluator catches what an Aristotelian one cannot."""
    report = compare_to_storyform(_tragic_drift_read(), _storyform())
    by_dim = {f.dimension: f for f in report.findings}
    assert by_dim["judgment"].verdict == "drifted"      # good → bad
    assert by_dim["ending_shape"].verdict == "drifted"  # triumph → tragedy
    assert by_dim["mc_resolve"].verdict == "drifted"    # steadfast → changed
    assert report.score < 0.5


def test_outcome_preserved_even_in_drift():
    """Both reads agree the goal FAILS — outcome is preserved; only the
    judgment axis drifts. Proves the axes are scored independently."""
    report = compare_to_storyform(_tragic_drift_read(), _storyform())
    by_dim = {f.dimension: f for f in report.findings}
    assert by_dim["outcome"].verdict == "preserved"     # failure == failure


def _triumphant_success_read():
    """A blind read where the prose's triumphant framing led the reader to
    score the OUTCOME as 'success' — the documented run-to-run flip
    (commit 7165324). Judgment is still 'good'. For Rocky's DUAL outcome
    this read is FAITHFUL, not drift: the story genuinely is both."""
    return DramaticaReading(
        story_goal="prove he could go the distance with the champion",
        outcome="success", judgment="good", ending_shape="triumph",
        main_character="Rocky", mc_resolve="steadfast",
        influence_character="Apollo", relationship="Rocky and Adrian",
        throughlines_present=["overall", "main character",
                              "influence character", "relationship"],
        overall_read="he goes the distance and wins what the fight was about.",
    )


def test_dual_outcome_either_pole_is_faithful():
    """The ambiguity-honest payoff: Rocky's Outcome is authored DUAL
    ({failure, success}). A read of EITHER pole is preserved — the
    run-to-run flip that used to score as drift is now read as the real
    ambiguity it is (dramatica-precision-limit), not a fidelity loss."""
    fail = compare_to_storyform(_faithful_read(), _storyform())
    succ = compare_to_storyform(_triumphant_success_read(), _storyform())
    fdim = {f.dimension: f for f in fail.findings}
    sdim = {f.dimension: f for f in succ.findings}
    assert fdim["outcome"].verdict == "preserved"   # read 'failure'
    assert sdim["outcome"].verdict == "preserved"   # read 'success'
    # the finding discloses the duality rather than hiding it behind one pole
    assert "DUAL" in sdim["outcome"].note
    assert sdim["outcome"].authored == "failure|success"


def test_binary_judgment_stays_strict_under_dual_outcome():
    """The integrity guard: making OUTCOME dual must NOT loosen the binary
    JUDGMENT axis. A read that flips Judgment good→bad is still drift — a
    genuine tragedy collapse is still caught. Ambiguity is declared per
    axis by the author; it is not a blanket forgiveness."""
    report = compare_to_storyform(_tragic_drift_read(), _storyform())
    by_dim = {f.dimension: f for f in report.findings}
    assert by_dim["outcome"].verdict == "preserved"   # failure ∈ dual span
    assert by_dim["judgment"].verdict == "drifted"    # good→bad, STRICT


def test_throughline_coverage():
    report = compare_to_storyform(_faithful_read(), _storyform())
    tl = [f for f in report.findings if f.dimension == "throughline"]
    assert len(tl) == 4
    assert all(f.verdict == "preserved" for f in tl)
    # the drift read only had the MC throughline
    drift = compare_to_storyform(_tragic_drift_read(), _storyform())
    lost_tl = [f for f in drift.findings
               if f.dimension == "throughline" and f.verdict == "lost"]
    assert len(lost_tl) == 3


TESTS = [
    test_perspective_detection,
    test_faithful_read_scores_high,
    test_outcome_and_judgment_are_independent_axes,
    test_tragic_drift_is_caught,
    test_outcome_preserved_even_in_drift,
    test_dual_outcome_either_pole_is_faithful,
    test_binary_judgment_stays_strict_under_dual_outcome,
    test_throughline_coverage,
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
