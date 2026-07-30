"""Pins for the shared evaluator core (`fidelity.py`,
evaluator-shared-core-sketch-01): the single name-matching policy all
four dialect evaluators now score with, the fuzzy content matcher, and
the report arithmetic. Standard library only."""

import sys
import traceback

from story_engine.core.fidelity import (
    FidelityFinding, FidelityReport,
    name_matches, any_name_match, normalize_name,
    content_overlap, char_name,
)


# ---- name matching (ESC3) --------------------------------------------------

def test_core_token_overlap_matches():
    """'the Duchess of Amalfi' and 'Amalfi' align on the proper noun."""
    assert name_matches("the Duchess of Amalfi", "Amalfi")
    assert name_matches("Rocky Balboa", "Rocky")


def test_title_only_name_matches_via_title_fallback():
    """A name that is ONLY a title still matches a titled fuller name —
    the Malfi case that motivated the old role-word fallback."""
    assert name_matches("the Duchess", "the Duchess of Amalfi")
    assert name_matches("the Cardinal", "Cardinal Monticelso")


def test_disjoint_titles_do_not_match():
    """'the Duchess' vs 'the Duke' share only an article — never a
    match. The pre-extraction Dramatica matcher had no stop set and
    would have matched these on 'the' (the latent false-positive the
    sketch names)."""
    assert not name_matches("the Duchess", "the Duke")
    assert not name_matches("the King", "the Thane")


def test_empty_or_blank_never_matches():
    assert not name_matches("", "Rocky")
    assert not name_matches("Rocky", "")
    assert not name_matches("  ", "the")


def test_cross_corpus_titles_are_one_set():
    """Macbeth vocabulary and Malfi vocabulary strip under the same
    policy: 'Lady Macbeth' matches 'Macbeth' the way 'Duke Ferdinand'
    matches 'Ferdinand' — no per-dialect stop set."""
    assert name_matches("Lady Macbeth", "Macbeth")
    assert name_matches("Duke Ferdinand", "Ferdinand")
    assert normalize_name("the Thane of Cawdor") == {"cawdor"}


def test_any_name_match_over_pool():
    assert any_name_match("the Duchess", ["Antonio", "the Duchess of Amalfi"])
    assert not any_name_match("Bosola", ["Antonio", "the Duchess"])


# ---- fuzzy content overlap (ESC3) ------------------------------------------

def test_content_overlap_requires_content_tokens():
    """Function words alone must not carry a fuzzy match."""
    assert content_overlap("the price of loyalty", "loyalty has a price")
    assert not content_overlap("the of a an", "what they are")
    assert not content_overlap("", "anything")


# ---- report arithmetic (ESC1) ----------------------------------------------

def test_report_scores_exclude_added():
    """'added' findings are informational — never in the denominator."""
    r = FidelityReport(title="t")
    r.findings.append(FidelityFinding("d1", "a", "a", "preserved"))
    r.findings.append(FidelityFinding("d2", "a", "b", "drifted"))
    r.findings.append(FidelityFinding("d3", "(not authored)", "x", "added"))
    assert len(r.scored) == 2
    assert r.preserved == 1
    assert r.score == 0.5


def test_empty_report_scores_zero():
    assert FidelityReport(title="t").score == 0.0


# ---- authored-side lookup (ESC3) -------------------------------------------

class _C:
    def __init__(self, id, name, ref=None):
        self.id = id
        self.name = name
        if ref is not None:
            self.character_ref_id = ref


class _M:
    def __init__(self, chars):
        self.characters = chars


def test_char_name_resolves_id_and_ref():
    m = _M([_C("c1", "the Duchess", ref="E_duchess")])
    assert char_name("c1", m) == "the Duchess"
    assert char_name("E_duchess", m) == "the Duchess"
    assert char_name("unknown", m) == "unknown"


TESTS = [
    test_core_token_overlap_matches,
    test_title_only_name_matches_via_title_fallback,
    test_disjoint_titles_do_not_match,
    test_empty_or_blank_never_matches,
    test_cross_corpus_titles_are_one_set,
    test_any_name_match_over_pool,
    test_content_overlap_requires_content_tokens,
    test_report_scores_exclude_added,
    test_empty_report_scores_zero,
    test_char_name_resolves_id_and_ref,
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
