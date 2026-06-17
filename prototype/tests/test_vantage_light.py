"""
test_vantage_light.py — the ORIGINAL encoding ("The Vantage Light").

Pins that a brand-new story (not from any canon) compiles and verifies
clean under the full Aristotelian apparatus (A1–A23), and that it
exercises the load-bearing landed features: the A22 pathos-split (Inga
suffers, Halvard recognizes) and the A20 anti-recognition (the captain,
too late, at the wreck).
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.aristotelian import verify, QUALIFIER_ANTI, BINDING_ADJACENT
from story_engine.encodings.vantage_light import FABULA, SJUZHET, ENTITIES
from story_engine.encodings.vantage_light_aristotelian import (
    AR_VANTAGE_MYTHOS, AR_STEP_CAPTAIN_WRECK,
)


def test_original_verifies_clean():
    """The headline: an original story verifies with ZERO observations
    under the full A1–A23 apparatus — the dialect is a general grammar,
    not overfit to the canon."""
    obs = verify(AR_VANTAGE_MYTHOS, substrate_events=tuple(FABULA),
                 mythoi=(AR_VANTAGE_MYTHOS,))
    assert obs == [], f"expected clean, got {[(o.severity, o.code) for o in obs]}"


def test_substrate_shape():
    assert len(FABULA) == 14
    fab = {e.id for e in FABULA}
    assert {s.event_id for s in SJUZHET} == fab          # every event staged
    assert len(SJUZHET) == 14
    # τ_s spans antecedent wound to final dark.
    assert min(e.τ_s for e in FABULA) == -40
    assert max(e.τ_s for e in FABULA) == 13


def test_pathos_split_oq_malfi_3_on_an_original():
    """A22: the pathos-centre (Inga) is split from the recognizer
    (Halvard) and from the tragic-hero set — the OQ-MALFI-3 shape, on a
    story the model never read."""
    m = AR_VANTAGE_MYTHOS
    assert m.pathos_character_ref_ids == ("ar_inga",)
    inga = next(c for c in m.characters if c.id == "ar_inga")
    assert inga.pathos_carrier is True
    assert inga.is_tragic_hero is False
    # recognizer is Halvard, NOT the pathos-centre.
    assert m.anagnorisis_character_ref_id == "ar_halvard"
    assert "ar_halvard" not in m.pathos_character_ref_ids
    heroes = {c.id for c in m.characters if c.is_tragic_hero}
    assert heroes == {"ar_halvard"}
    assert heroes.isdisjoint(set(m.pathos_character_ref_ids))


def test_anti_recognition_on_an_original():
    """A20: the captain's wreck-recognition is an anti-recognition."""
    chain = AR_VANTAGE_MYTHOS.anagnorisis_chain
    assert len(chain) == 1
    assert chain[0] is AR_STEP_CAPTAIN_WRECK
    assert chain[0].anagnorisis_qualifier == QUALIFIER_ANTI
    assert chain[0].event_id == "E_ship_founders"
    assert chain[0].precipitates_main is False


def test_binding_adjacent():
    """A12: peripeteia (τ_s=9) and anagnorisis (τ_s=11) are two beats
    apart — ADJACENT."""
    m = AR_VANTAGE_MYTHOS
    assert m.peripeteia_anagnorisis_binding == BINDING_ADJACENT
    by_id = {e.id: e for e in FABULA}
    p = by_id[m.peripeteia_event_id].τ_s
    a = by_id[m.anagnorisis_event_id].τ_s
    assert abs(p - a) == 2


def test_tragic_hero_participates():
    """The tragic hero (Halvard) participates in the action — hamartia
    participation is satisfiable on an original."""
    halvard_events = [e for e in FABULA
                      if "halvard" in e.participants.values()]
    assert len(halvard_events) >= 4


TESTS = [
    test_original_verifies_clean,
    test_substrate_shape,
    test_pathos_split_oq_malfi_3_on_an_original,
    test_anti_recognition_on_an_original,
    test_binding_adjacent,
    test_tragic_hero_participates,
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
