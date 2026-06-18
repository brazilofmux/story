"""
test_dramatic_evaluator.py — general-Dramatic fidelity comparison, offline.

Stage 1 (decompile_dramatic) needs the API; the demo exercises it. Stage 2
(compare_to_story) is pure Python: given a blind Dramatic reading, does it
score the Hero / Obstacle / Helper functions (crisp), the argument's
resolution direction, and the claim / stakes (fuzzy) against Rocky's
three-actor Dramatic encoding — without ever seeing it?

Pins dramatic_evaluator parity with the peer evaluators (dialect-parity bet).
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.dramatic_evaluator import (
    DramaticReading, compare_to_story, _norm_resolution, _names_for,
    _HERO_FUNCS, _HELPER_FUNCS,
)
from story_engine.core.dramatic_generation import DramaticStory
from story_engine.encodings import rocky_dramatic_three_actor as D


def _story() -> DramaticStory:
    return DramaticStory(
        title="Rocky", action_summary="x",
        template_id=D.STORY.character_function_template_id,
        characters=D.CHARACTERS, arguments=(D.ARG_WORTH,),
        throughlines=D.THROUGHLINES, stakes=(D.STK_SELF_RESPECT,),
    )


def _faithful_read() -> DramaticReading:
    return DramaticReading(
        hero="Rocky Balboa",
        obstacle="Apollo Creed",
        helper="Mickey",
        argument_claim="you earn your worth by enduring what would break you, "
                       "not by winning",
        argument_resolution="affirm",
        stakes="proof he can go the full fifteen rounds and is not a nobody",
        overall_read="a club fighter endures the unwinnable fight and proves "
                     "his worth.",
    )


def test_resolution_normalization():
    assert _norm_resolution("affirm") == "affirm"
    assert _norm_resolution("affirms the claim") == "affirm"
    assert _norm_resolution("the story upholds it") == "affirm"
    assert _norm_resolution("negate") == "negate"
    assert _norm_resolution("it refutes the premise") == "negate"
    assert _norm_resolution("complicates") == "complicate"
    assert _norm_resolution("") == ""


def test_function_extraction():
    assert _names_for(_story(), _HERO_FUNCS) == ["Rocky Balboa"]
    # both Mickey and Adrian carry the Helper function in the encoding
    helpers = _names_for(_story(), _HELPER_FUNCS)
    assert "Mickey Goldmill" in helpers and "Adrian Pennino" in helpers


def test_faithful_read_scores_high():
    report = compare_to_story(_faithful_read(), _story())
    bad = [f for f in report.scored if f.verdict != "preserved"]
    assert bad == [], f"unexpected: {[(f.dimension, f.verdict) for f in bad]}"
    assert report.score == 1.0


def test_hero_and_obstacle_drift_are_caught():
    read = _faithful_read()
    read.hero = "Apollo Creed"      # the Obstacle, not the Hero
    read.obstacle = "Mickey"        # wrong
    report = compare_to_story(read, _story())
    by_dim = {f.dimension: f for f in report.findings}
    assert by_dim["hero"].verdict == "lost"
    assert by_dim["obstacle"].verdict == "lost"


def test_helper_preserved_if_any_authored_helper_found():
    """The encoding authors two Helpers (Mickey, Adrian); finding EITHER
    preserves the dimension."""
    read = _faithful_read()
    read.helper = "Adrian"
    report = compare_to_story(read, _story())
    by_dim = {f.dimension: f for f in report.findings}
    assert by_dim["helper"].verdict == "preserved"


def test_argument_resolution_drift_is_caught():
    """The thematic outcome: Rocky AFFIRMS its claim. A read that the story
    NEGATES it is a drift the function checks alone cannot see."""
    read = _faithful_read()
    read.argument_resolution = "negate"
    report = compare_to_story(read, _story())
    by_dim = {f.dimension: f for f in report.findings}
    assert by_dim["argument_resolution"].authored == "affirm"
    assert by_dim["argument_resolution"].verdict == "drifted"


def test_fuzzy_claim_and_stakes_are_labelled_fuzzy():
    """Claim and stakes are token-overlap matches — the findings must SAY so,
    so a soft match is never mistaken for a crisp one."""
    report = compare_to_story(_faithful_read(), _story())
    by_dim = {f.dimension: f for f in report.findings}
    assert "FUZZY" in by_dim["argument_claim"].note
    assert "FUZZY" in by_dim["stakes"].note
    assert by_dim["argument_claim"].verdict == "preserved"   # shares content
    # a claim with no overlap drifts
    read = _faithful_read()
    read.argument_claim = "love conquers all in the end"
    drift = compare_to_story(read, _story())
    assert {f.dimension: f for f in drift.findings}["argument_claim"].verdict \
        == "drifted"


TESTS = [
    test_resolution_normalization,
    test_function_extraction,
    test_faithful_read_scores_high,
    test_hero_and_obstacle_drift_are_caught,
    test_helper_preserved_if_any_authored_helper_found,
    test_argument_resolution_drift_is_caught,
    test_fuzzy_claim_and_stakes_are_labelled_fuzzy,
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
