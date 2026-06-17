"""
test_draft_evaluator.py — the fidelity comparison (stage 2), offline.

Stage 1 (decompile_draft) needs the API and is exercised by the demo.
Stage 2 (compare_to_mythos) is pure Python and is the testable core:
given a blind prose reading, does it correctly score round-trip
fidelity against the authored mythos? We use the REAL Malfi mythos
(so the authored expectations are the genuine ones) and synthesize
faithful vs degraded readings.
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.draft_evaluator import (
    DecompiledStructure, RecognitionRead, compare_to_mythos,
    _name_matches,
)
from story_engine.encodings.malfi_aristotelian import AR_MALFI_MYTHOS


def _faithful_malfi_read() -> DecompiledStructure:
    """A blind reading that recovered Malfi's spine: complex, the
    Duchess as pathos-centre, Ferdinand as recognizer, Antonio's anti-
    recognition, the secondary falls."""
    return DecompiledStructure(
        plot_kind="complex",
        unity_of_action=True,
        peripeteia="The Duchess is captured in the countryside.",
        peripeteia_character="the Duchess",
        anagnorisis="Ferdinand sees the corpse and breaks.",
        anagnorisis_character="Ferdinand",
        pathos_centre_characters=["the Duchess of Amalfi"],
        tragic_hero_characters=["the Duchess", "Bosola", "Ferdinand"],
        staggered_recognitions=[
            RecognitionRead(character="Bosola",
                            summary="resolves to revenge", qualifier="genuine"),
            RecognitionRead(character="Antonio",
                            summary="killed in the dark by the man who would "
                                    "have saved him", qualifier="anti"),
        ],
        secondary_reversals=[
            "Ferdinand falls into madness",
            "Bosola turns avenger",
            "Antonio dies mistaken",
        ],
        overall_read="Holds as a distributed tragedy.",
    )


def _degraded_malfi_read() -> DecompiledStructure:
    """A reading where the prose lost the spine: the pathos-centre and
    the anti-recognition flattened, the recognizer drifted, the
    secondary arcs thinned."""
    return DecompiledStructure(
        plot_kind="complex",
        unity_of_action=True,
        peripeteia="Someone is captured.",
        peripeteia_character="Bosola",
        anagnorisis="Bosola understands his guilt.",
        anagnorisis_character="Bosola",          # drifted off Ferdinand
        pathos_centre_characters=["Bosola"],     # lost the Duchess
        tragic_hero_characters=["Bosola"],       # lost Duchess + Ferdinand
        staggered_recognitions=[
            RecognitionRead(character="Antonio", summary="dies",
                            qualifier="genuine"),   # anti flattened
        ],
        secondary_reversals=[],                  # multi-arc fall thinned
        overall_read="Reads as Bosola's single arc.",
    )


def test_name_matches_fuzzy():
    assert _name_matches("the Duchess of Amalfi", "the Duchess")
    assert _name_matches("Daniel de Bosola", "Bosola")
    assert _name_matches("Ferdinand, Duke of Calabria", "Ferdinand")
    assert not _name_matches("Ferdinand", "Antonio")
    assert not _name_matches("", "Bosola")


def test_faithful_read_scores_high():
    report = compare_to_mythos(_faithful_malfi_read(), AR_MALFI_MYTHOS)
    # Every scored dimension preserved.
    lost = [f for f in report.scored if f.verdict != "preserved"]
    assert lost == [], f"unexpected non-preserved: {[(f.dimension, f.verdict) for f in lost]}"
    assert report.score == 1.0


def test_degraded_read_scores_low():
    report = compare_to_mythos(_degraded_malfi_read(), AR_MALFI_MYTHOS)
    assert report.score < 0.5
    verdicts = {f.dimension: f.verdict for f in report.findings}
    # The Duchess pathos-centre was lost.
    pathos = [f for f in report.findings if f.dimension == "pathos_centre"]
    assert any(f.verdict == "lost" for f in pathos)
    # The anti-recognition flattened.
    anti = [f for f in report.findings if f.dimension == "anti_recognition"]
    assert anti and all(f.verdict == "lost" for f in anti)
    # The recognizer drifted off Ferdinand.
    anag = [f for f in report.findings if f.dimension == "anagnorisis_character"]
    assert anag and anag[0].verdict == "lost"


def test_pathos_centre_is_checked_against_authored():
    """The authored Malfi pathos-centre is the Duchess (sketch-07)."""
    report = compare_to_mythos(_faithful_malfi_read(), AR_MALFI_MYTHOS)
    pathos = [f for f in report.findings if f.dimension == "pathos_centre"]
    assert len(pathos) == 1
    assert "Duchess" in pathos[0].authored
    assert pathos[0].verdict == "preserved"


def test_added_pathos_centre_is_informational_not_a_loss():
    read = _faithful_malfi_read()
    read.pathos_centre_characters = ["the Duchess of Amalfi", "Cariola"]
    report = compare_to_mythos(read, AR_MALFI_MYTHOS)
    added = [f for f in report.findings if f.verdict == "added"]
    assert any("Cariola" in f.decompiled for f in added)
    # 'added' does not drag the score below the faithful baseline.
    assert report.score == 1.0


def test_report_score_is_preserved_over_scored():
    report = compare_to_mythos(_faithful_malfi_read(), AR_MALFI_MYTHOS)
    assert report.preserved == len(report.scored)
    assert 0.0 <= report.score <= 1.0


TESTS = [
    test_name_matches_fuzzy,
    test_faithful_read_scores_high,
    test_degraded_read_scores_low,
    test_pathos_centre_is_checked_against_authored,
    test_added_pathos_centre_is_informational_not_a_loss,
    test_report_score_is_preserved_over_scored,
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
