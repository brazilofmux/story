"""
test_sworn.py — the REVERSE-TOLD original ("Sworn").

Pins that an original story told in strict reverse chronological order
verifies clean under A1–A23 (the structure is ordinary; only the staging
is hard), and that the substrate genuinely stages it backward — the
variable the generation experiment isolates.
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.aristotelian import (
    verify, QUALIFIER_ANTI, BINDING_SEPARATED,
)
from story_engine.core.draft_generator import build_story_bible
from story_engine.encodings.sworn import (
    FABULA, SJUZHET, ENTITIES, PREPLAY_DISCLOSURES,
)
from story_engine.encodings.sworn_aristotelian import (
    AR_SWORN_MYTHOS, AR_STEP_ALEKS_VERDICT,
)


def test_verifies_clean():
    obs = verify(AR_SWORN_MYTHOS, substrate_events=tuple(FABULA),
                 mythoi=(AR_SWORN_MYTHOS,))
    assert obs == [], f"expected clean, got {[(o.severity, o.code) for o in obs]}"


def test_sjuzhet_is_strict_reverse():
    """The experiment's variable: the staging runs backward through
    story-time. τ_d order 0→9 must map to STRICTLY DESCENDING τ_s."""
    fab = {e.id: e.τ_s for e in FABULA}
    staged = sorted(SJUZHET, key=lambda s: s.τ_d)
    ts = [fab[s.event_id] for s in staged]
    assert ts == sorted(ts, reverse=True), ts
    # the opening staged scene is the latest in story-time (the ruin)…
    assert fab[staged[0].event_id] == max(fab.values())
    # …and the final staged scene is the earliest (the boyhood vow).
    assert fab[staged[-1].event_id] == min(fab.values())


def test_bible_flags_reverse_telling():
    """The generator surfaces the reverse staging so the renderer can
    honor it rather than defaulting to chronology."""
    bible = build_story_bible(
        title="Sworn", sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
        mythos=AR_SWORN_MYTHOS, preplay_disclosures=PREPLAY_DISCLOSURES,
        dialect_note="reverse",
    )
    assert "REVERSE-CHRONOLOGICAL" in bible
    assert "Do NOT silently reorder events into chronology" in bible
    # the staged→story-time map is present
    assert "staged #0 ← story-time τ_s=20" in bible


def test_pathos_split_and_anti_recognition():
    m = AR_SWORN_MYTHOS
    # pathos-centre (Aleks) split from recognizer (Tomas)
    assert m.pathos_character_ref_ids == ("ar_aleks",)
    assert m.anagnorisis_character_ref_id == "ar_tomas"
    aleks = next(c for c in m.characters if c.id == "ar_aleks")
    assert aleks.pathos_carrier is True and aleks.is_tragic_hero is False
    heroes = {c.id for c in m.characters if c.is_tragic_hero}
    assert heroes == {"ar_tomas"}
    # anti-recognition
    assert len(m.anagnorisis_chain) == 1
    assert AR_STEP_ALEKS_VERDICT.anagnorisis_qualifier == QUALIFIER_ANTI
    assert AR_STEP_ALEKS_VERDICT.precipitates_main is False


def test_binding_separated():
    m = AR_SWORN_MYTHOS
    assert m.peripeteia_anagnorisis_binding == BINDING_SEPARATED
    by_id = {e.id: e for e in FABULA}
    assert abs(by_id[m.peripeteia_event_id].τ_s
               - by_id[m.anagnorisis_event_id].τ_s) == 10


TESTS = [
    test_verifies_clean,
    test_sjuzhet_is_strict_reverse,
    test_bible_flags_reverse_telling,
    test_pathos_split_and_anti_recognition,
    test_binding_separated,
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
