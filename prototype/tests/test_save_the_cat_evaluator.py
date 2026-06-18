"""
test_save_the_cat_evaluator.py — Save-the-Cat fidelity comparison, offline.

Stage 1 (decompile_stc) needs the API; the demo exercises it. Stage 2
(compare_to_sheet) is pure Python: given a blind StC reading, does it score
beat coverage, beat ORDER, protagonist, and B-story against Macbeth's
authored beat sheet — without ever seeing the sheet?

Pins save_the_cat_evaluator parity with the Aristotelian / Dramatica
evaluators (dialect-parity bet).
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.save_the_cat_evaluator import (
    StcReading, StcBeatRead, compare_to_sheet, _slot_of_read, _protagonist_of,
)
from story_engine.core.save_the_cat_generation import StcStorySheet
from story_engine.core.save_the_cat import CANONICAL_BEAT_BY_SLOT
from story_engine.encodings import macbeth_save_the_cat as S


def _sheet() -> StcStorySheet:
    return StcStorySheet(
        title="Macbeth", action_summary="x",
        beats=S.BEATS, strands=S.STRANDS, characters=S.CHARACTERS,
        beat_event_ids=S.BEAT_EVENT_IDS,
    )


def _all_beats_in_order():
    """Every canonical beat, labelled by its exact name, in canonical order."""
    return [StcBeatRead(beat=CANONICAL_BEAT_BY_SLOT[s].name,
                        what_happens=f"beat {s} happens")
            for s in range(1, 16)]


def _faithful_read() -> StcReading:
    return StcReading(
        protagonist="Macbeth",
        beats_identified=_all_beats_in_order(),
        theme_stated="fair is foul",
        b_story="Macbeth and Lady Macbeth's marriage",
        midpoint="false victory — the crown is won",
        all_is_lost="Lady Macbeth's death",
        final_mirrors_opening="yes",
        overall_read="a complete tyrant's rise and fall.",
    )


def test_slot_name_resolution_distinguishes_lookalikes():
    """'Break Into Two' and 'Break Into Three' must not collide; nor must
    'Opening Image' and 'Final Image'."""
    assert _slot_of_read("Break Into Two") == 6
    assert _slot_of_read("Break Into Three") == 13
    assert _slot_of_read("Opening Image") == 1
    assert _slot_of_read("Final Image") == 15
    assert _slot_of_read("All Is Lost") == 11
    assert _slot_of_read("nonsense beat") is None


def test_protagonist_resolution():
    assert _protagonist_of(_sheet()) == "Macbeth"


def test_faithful_read_scores_high():
    report = compare_to_sheet(_faithful_read(), _sheet())
    lost = [f for f in report.scored if f.verdict != "preserved"]
    assert lost == [], f"unexpected: {[(f.dimension, f.verdict) for f in lost]}"
    assert report.score == 1.0


def test_lost_beats_are_caught():
    """Drop the Catalyst and the All Is Lost beats — both must read as lost."""
    beats = [b for b in _all_beats_in_order()
             if b.beat not in ("Catalyst", "All Is Lost")]
    read = _faithful_read()
    read.beats_identified = beats
    report = compare_to_sheet(read, _sheet())
    by_dim = {f.dimension: f for f in report.findings}
    assert by_dim["beat[04]"].verdict == "lost"   # Catalyst
    assert by_dim["beat[11]"].verdict == "lost"    # All Is Lost
    assert by_dim["beat[09]"].verdict == "preserved"  # Midpoint still there
    assert report.score < 1.0


def test_beat_order_drift_is_caught():
    """If the prose presents beats out of canonical sequence, the order
    finding drifts even when coverage is complete."""
    read = _faithful_read()
    scrambled = _all_beats_in_order()
    scrambled[0], scrambled[5] = scrambled[5], scrambled[0]  # swap 1 and 6
    read.beats_identified = scrambled
    report = compare_to_sheet(read, _sheet())
    by_dim = {f.dimension: f for f in report.findings}
    assert by_dim["beat_order"].verdict == "drifted"
    # coverage itself is unaffected — every beat still present
    assert by_dim["beat[01]"].verdict == "preserved"


def test_protagonist_drift_is_caught():
    read = _faithful_read()
    read.protagonist = "Macduff"
    report = compare_to_sheet(read, _sheet())
    by_dim = {f.dimension: f for f in report.findings}
    assert by_dim["protagonist"].verdict == "lost"


def test_b_story_loss_is_caught():
    read = _faithful_read()
    read.b_story = ""
    report = compare_to_sheet(read, _sheet())
    by_dim = {f.dimension: f for f in report.findings}
    assert by_dim["b_story"].verdict == "lost"


TESTS = [
    test_slot_name_resolution_distinguishes_lookalikes,
    test_protagonist_resolution,
    test_faithful_read_scores_high,
    test_lost_beats_are_caught,
    test_beat_order_drift_is_caught,
    test_protagonist_drift_is_caught,
    test_b_story_loss_is_caught,
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
