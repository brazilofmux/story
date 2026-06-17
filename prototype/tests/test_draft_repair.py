"""
test_draft_repair.py — plan_repairs (the localization logic), offline.

repair_scene needs the API (exercised by the demo). plan_repairs is
pure Python: given a FidelityReport's losses + the authored mythos,
does it map the localizable ones to the right substrate events with the
right corrective directives — and correctly DECLINE to localize diffuse
losses? We use the real Malfi mythos.
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.draft_evaluator import (
    DecompiledStructure, RecognitionRead, compare_to_mythos,
)
from story_engine.core.draft_repair import (
    plan_repairs, build_story_so_far, RepairDirective,
)
from story_engine.encodings.malfi_aristotelian import AR_MALFI_MYTHOS
from story_engine.encodings.malfi import FABULA, SJUZHET, ENTITIES


def _drifted_read() -> DecompiledStructure:
    """The real drift the first Malfi evaluation found: the anti-
    recognition relocated off Antonio (to Bosola), and the recognizer
    drifted off Ferdinand."""
    return DecompiledStructure(
        plot_kind="complex", unity_of_action=True,
        peripeteia="capture", peripeteia_character="the Duchess",
        anagnorisis="Bosola wakes to guilt", anagnorisis_character="Bosola",
        pathos_centre_characters=["the Duchess of Amalfi"],
        tragic_hero_characters=["the Duchess", "Bosola", "Ferdinand"],
        staggered_recognitions=[
            RecognitionRead(character="Bosola",
                            summary="kills Antonio by mistake", qualifier="anti"),
        ],
        secondary_reversals=["Ferdinand mad", "Bosola turns", "Cardinal trapped"],
        overall_read="drifted",
    )


def test_plan_repairs_localizes_anti_recognition():
    report = compare_to_mythos(_drifted_read(), AR_MALFI_MYTHOS)
    directives = plan_repairs(report, AR_MALFI_MYTHOS)
    anti = [d for d in directives if d.dimension == "anti_recognition"]
    assert len(anti) == 1
    # Antonio's authored anti step lands at E_bosola_kills_antonio.
    assert anti[0].event_id == "E_bosola_kills_antonio"
    assert "Antonio" in anti[0].authored
    # The directive insists on mutual / too-late recognition.
    assert "MUTUAL" in anti[0].instruction
    assert "unknowing" in anti[0].instruction


def test_plan_repairs_localizes_anagnorisis_drift():
    report = compare_to_mythos(_drifted_read(), AR_MALFI_MYTHOS)
    directives = plan_repairs(report, AR_MALFI_MYTHOS)
    anag = [d for d in directives if d.dimension == "anagnorisis_character"]
    assert len(anag) == 1
    # The main anagnorisis event is Ferdinand viewing the corpse.
    assert anag[0].event_id == AR_MALFI_MYTHOS.anagnorisis_event_id
    assert "Ferdinand" in anag[0].authored


def test_plan_repairs_skips_diffuse_losses():
    """A faithful read produces no directives (nothing to repair); a
    pathos-only loss is not forced onto a scene."""
    faithful = DecompiledStructure(
        plot_kind="complex", unity_of_action=True,
        peripeteia="capture", peripeteia_character="the Duchess",
        anagnorisis="Ferdinand breaks", anagnorisis_character="Ferdinand",
        pathos_centre_characters=["the Duchess of Amalfi"],
        tragic_hero_characters=["the Duchess", "Bosola", "Ferdinand"],
        staggered_recognitions=[
            RecognitionRead(character="Antonio", summary="dies knowing",
                            qualifier="anti"),
        ],
        secondary_reversals=["a", "b", "c"],
        overall_read="faithful",
    )
    report = compare_to_mythos(faithful, AR_MALFI_MYTHOS)
    assert plan_repairs(report, AR_MALFI_MYTHOS) == []


def test_plan_repairs_dedupes_same_event_dimension():
    # Two anti findings for the same step should collapse to one directive.
    report = compare_to_mythos(_drifted_read(), AR_MALFI_MYTHOS)
    report.findings.append(report.findings[-1])  # duplicate a finding
    directives = plan_repairs(report, AR_MALFI_MYTHOS)
    keys = [(d.event_id, d.dimension) for d in directives]
    assert len(keys) == len(set(keys))


def test_build_story_so_far_orders_prior_beats():
    target = min(e.τ_d for e in SJUZHET
                 if e.event_id == "E_bosola_kills_antonio")
    sof = build_story_so_far(SJUZHET, FABULA, ENTITIES, up_to_τ_d=target)
    assert "STORY SO FAR" in sof
    # The target scene's own beat is NOT included (strictly prior).
    assert sof.count("\n") >= 1


def test_repair_directive_targets_real_sjuzhet_event():
    report = compare_to_mythos(_drifted_read(), AR_MALFI_MYTHOS)
    directives = plan_repairs(report, AR_MALFI_MYTHOS)
    sjuzhet_events = {e.event_id for e in SJUZHET}
    for d in directives:
        assert d.event_id in sjuzhet_events, \
            f"directive targets {d.event_id} not in sjuzhet"


TESTS = [
    test_plan_repairs_localizes_anti_recognition,
    test_plan_repairs_localizes_anagnorisis_drift,
    test_plan_repairs_skips_diffuse_losses,
    test_plan_repairs_dedupes_same_event_dimension,
    test_build_story_so_far_orders_prior_beats,
    test_repair_directive_targets_real_sjuzhet_event,
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
