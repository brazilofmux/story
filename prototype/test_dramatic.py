"""
test_dramatic.py — permanent tests for the Dramatic dialect's
records and self-verifier (dramatic-sketch-01 M1-M10).

Synthetic-fixture tests pin the verifier's behavior on each M8
check independently. An integration test runs against
oedipus_dramatic.py to confirm the encoding produces the expected
three observations (and no surprise issues).

Run:
    python3 test_dramatic.py
"""

from __future__ import annotations

import sys
import traceback

from dramatic import (
    Story, Argument, Throughline, Character, Beat, Scene, Stakes,
    Template, FunctionSlot,
    ArgumentContribution, SceneAdvancement, StakesOwner,
    FunctionMultiplicity, ResolutionDirection, ArgumentSide,
    StakesOwnerKind,
    DRAMATICA_8, THREE_ACTOR, TWO_ACTOR, ENSEMBLE,
    STANDARD_TEMPLATES, standard_templates_index,
    THROUGHLINE_OWNER_NONE, THROUGHLINE_OWNER_SITUATION,
    THROUGHLINE_OWNER_RELATIONSHIP, ABSTRACT_THROUGHLINE_OWNERS,
    Observation,
    verify, group_by_severity, group_by_code,
)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


def _trivial_story(**overrides) -> Story:
    """A near-empty Story for narrow synthetic tests."""
    base = dict(
        id="S_test", title="test",
        character_function_template_id=None,
    )
    base.update(overrides)
    return Story(**base)


def _codes(observations: list) -> set:
    """Set of observation codes for ergonomic assertions."""
    return {o.code for o in observations}


# ----------------------------------------------------------------------------
# M5 / Templates — multiplicity vocabulary
# ----------------------------------------------------------------------------


def test_dramatica_8_has_eight_exactly_one_slots():
    assert len(DRAMATICA_8.function_slots) == 8
    for s in DRAMATICA_8.function_slots:
        assert s.multiplicity == FunctionMultiplicity.EXACTLY_ONE


def test_three_actor_template_has_two_required_one_at_least_one():
    slots_by_label = {s.label: s for s in THREE_ACTOR.function_slots}
    assert slots_by_label["Hero"].multiplicity == FunctionMultiplicity.EXACTLY_ONE
    assert slots_by_label["Obstacle"].multiplicity == FunctionMultiplicity.EXACTLY_ONE
    assert slots_by_label["Helper"].multiplicity == FunctionMultiplicity.AT_LEAST_ONE


def test_template_slot_for_label():
    s = DRAMATICA_8.slot_for("Protagonist")
    assert s is not None and s.label == "Protagonist"
    assert DRAMATICA_8.slot_for("not-a-real-label") is None


# ----------------------------------------------------------------------------
# M8.1 — id resolution
# ----------------------------------------------------------------------------


def test_unknown_template_id_surfaces_observation():
    s = _trivial_story(character_function_template_id="not-a-real-template")
    obs = verify(s)
    assert "id_unresolved" in _codes(obs)


def test_story_references_unknown_record_id():
    s = _trivial_story(argument_ids=("A_does_not_exist",))
    obs = verify(s)
    assert any(
        o.code == "id_unresolved" and "A_does_not_exist" in o.message
        for o in obs
    )


def test_throughline_owners_can_use_abstract_sentinels():
    """THROUGHLINE_OWNER_SITUATION etc. don't trigger id-resolution
    errors even though they aren't Character ids."""
    t = Throughline(
        id="T_x", role_label="overall-story",
        owners=(THROUGHLINE_OWNER_SITUATION,),
        subject="x",
    )
    s = _trivial_story(throughline_ids=("T_x",))
    obs = verify(s, throughlines=(t,))
    assert "id_unresolved" not in _codes(obs)


def test_throughline_owners_with_unknown_character_id_surfaces():
    t = Throughline(
        id="T_x", role_label="main-character",
        owners=("C_does_not_exist",),
        subject="x",
    )
    s = _trivial_story(throughline_ids=("T_x",))
    obs = verify(s, throughlines=(t,))
    assert any(
        o.code == "id_unresolved" and "C_does_not_exist" in o.message
        for o in obs
    )


def test_scene_advances_unknown_throughline_surfaces():
    sc = Scene(
        id="Sc_x", title="x", narrative_position=1,
        advances=(SceneAdvancement(throughline_id="T_unknown"),),
    )
    s = _trivial_story(scene_ids=("Sc_x",))
    obs = verify(s, scenes=(sc,))
    assert any(
        o.code == "id_unresolved" and "T_unknown" in o.message
        for o in obs
    )


def test_beat_with_unknown_throughline_surfaces():
    b = Beat(id="B_x", throughline_id="T_unknown", beat_position=1)
    s = _trivial_story(beat_ids=("B_x",))
    obs = verify(s, beats=(b,))
    assert any(
        o.code == "id_unresolved" and "T_unknown" in o.message
        for o in obs
    )


def test_stakes_owner_throughline_id_must_resolve():
    st = Stakes(
        id="St_x",
        owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T_unknown"),
        at_risk="x", to_gain="y",
    )
    s = _trivial_story(stakes_ids=("St_x",))
    obs = verify(s, stakes=(st,))
    assert any(
        o.code == "id_unresolved" and "T_unknown" in o.message
        for o in obs
    )


def test_stakes_owner_story_id_must_match_story():
    st = Stakes(
        id="St_x",
        owner=StakesOwner(kind=StakesOwnerKind.STORY, id="S_wrong"),
        at_risk="x", to_gain="y",
    )
    s = _trivial_story(stakes_ids=("St_x",))
    obs = verify(s, stakes=(st,))
    assert any(
        o.code == "id_unresolved" and "S_wrong" in o.message
        for o in obs
    )


# ----------------------------------------------------------------------------
# M8.2 — beat sequencing
# ----------------------------------------------------------------------------


def test_duplicate_beat_positions_surface():
    t = Throughline(
        id="T_x", role_label="main-character", owners=("C_x",), subject="x",
    )
    c = Character(id="C_x", name="x")
    b1 = Beat(id="B1", throughline_id="T_x", beat_position=1)
    b2 = Beat(id="B2", throughline_id="T_x", beat_position=1)  # duplicate
    s = _trivial_story(
        throughline_ids=("T_x",), character_ids=("C_x",),
        beat_ids=("B1", "B2"),
    )
    obs = verify(s, throughlines=(t,), characters=(c,), beats=(b1, b2))
    assert "beat_position_duplicate" in _codes(obs)


def test_distinct_beat_positions_within_throughline_pass():
    t = Throughline(
        id="T_x", role_label="main-character", owners=("C_x",), subject="x",
    )
    c = Character(id="C_x", name="x")
    b1 = Beat(id="B1", throughline_id="T_x", beat_position=1)
    b2 = Beat(id="B2", throughline_id="T_x", beat_position=2)
    s = _trivial_story(
        throughline_ids=("T_x",), character_ids=("C_x",),
        beat_ids=("B1", "B2"),
    )
    obs = verify(s, throughlines=(t,), characters=(c,), beats=(b1, b2))
    assert "beat_position_duplicate" not in _codes(obs)


# ----------------------------------------------------------------------------
# M8.3 — scene sequencing
# ----------------------------------------------------------------------------


def test_duplicate_scene_positions_surface():
    sc1 = Scene(id="S1", title="x", narrative_position=1)
    sc2 = Scene(id="S2", title="y", narrative_position=1)  # duplicate
    s = _trivial_story(scene_ids=("S1", "S2"))
    obs = verify(s, scenes=(sc1, sc2))
    assert "scene_position_duplicate" in _codes(obs)


# ----------------------------------------------------------------------------
# M8.4 / M9 — template conformance and multiplicity
# ----------------------------------------------------------------------------


def test_unknown_function_label_surfaces():
    c = Character(id="C_x", name="x", function_labels=("NotARealFunction",))
    s = _trivial_story(
        character_function_template_id="dramatica-8",
        character_ids=("C_x",),
    )
    obs = verify(s, characters=(c,))
    assert "function_label_unknown" in _codes(obs)


def test_exactly_one_with_zero_count_surfaces_unfilled():
    s = _trivial_story(character_function_template_id="dramatica-8")
    obs = verify(s)
    # Every dramatica-8 slot is exactly-one with zero characters.
    unfilled = [o for o in obs if o.code == "slot_unfilled"]
    assert len(unfilled) == 8


def test_exactly_one_with_two_counts_surfaces_overfilled():
    c1 = Character(id="C1", name="a", function_labels=("Protagonist",))
    c2 = Character(id="C2", name="b", function_labels=("Protagonist",))
    # Two-actor template requires Protagonist + Antagonist.
    s = _trivial_story(
        character_function_template_id="two-actor",
        character_ids=("C1", "C2"),
    )
    obs = verify(s, characters=(c1, c2))
    overfilled = [
        o for o in obs
        if o.code == "slot_overfilled" and "Protagonist" in o.target_id
    ]
    assert len(overfilled) == 1


def test_at_least_one_with_zero_count_surfaces_unfilled():
    # Three-actor: Hero, Obstacle, Helper(at-least-one). Provide no Helpers.
    c1 = Character(id="C1", name="a", function_labels=("Hero",))
    c2 = Character(id="C2", name="b", function_labels=("Obstacle",))
    s = _trivial_story(
        character_function_template_id="three-actor",
        character_ids=("C1", "C2"),
    )
    obs = verify(s, characters=(c1, c2))
    helper_unfilled = [
        o for o in obs
        if o.code == "slot_unfilled" and "Helper" in o.target_id
    ]
    assert len(helper_unfilled) == 1


def test_at_least_one_with_multiple_count_passes():
    c1 = Character(id="C1", name="a", function_labels=("Hero",))
    c2 = Character(id="C2", name="b", function_labels=("Obstacle",))
    c3 = Character(id="C3", name="c", function_labels=("Helper",))
    c4 = Character(id="C4", name="d", function_labels=("Helper",))
    s = _trivial_story(
        character_function_template_id="three-actor",
        character_ids=("C1", "C2", "C3", "C4"),
    )
    obs = verify(s, characters=(c1, c2, c3, c4))
    # No multiplicity violations.
    assert "slot_unfilled" not in _codes(obs)
    assert "slot_overfilled" not in _codes(obs)


def test_any_multiplicity_never_triggers():
    # Ensemble template: voice = at-least-one. Construct a Template that
    # uses ANY for the test.
    custom = Template(
        id="custom", name="custom",
        function_slots=(FunctionSlot("Voice", FunctionMultiplicity.ANY),),
    )
    templates = {"custom": custom}
    s = _trivial_story(character_function_template_id="custom")
    obs = verify(s, templates=templates)
    assert "slot_unfilled" not in _codes(obs)
    assert "slot_overfilled" not in _codes(obs)


def test_no_template_means_no_multiplicity_check():
    """A Story with no declared template gets no multiplicity
    observations even with characters carrying labels."""
    c = Character(id="C1", name="x", function_labels=("Anything",))
    s = _trivial_story(character_ids=("C1",))
    obs = verify(s, characters=(c,))
    assert not any(
        o.code in ("slot_unfilled", "slot_overfilled", "function_label_unknown")
        for o in obs
    )


# ----------------------------------------------------------------------------
# M8.5 — argument completeness (soft)
# ----------------------------------------------------------------------------


def test_argument_with_no_contributing_throughline_surfaces():
    arg = Argument(
        id="A1", premise="x",
        resolution_direction=ResolutionDirection.AFFIRM,
    )
    s = _trivial_story(argument_ids=("A1",))
    obs = verify(s, arguments=(arg,))
    assert "argument_no_throughline_contribution" in _codes(obs)


def test_argument_with_contribution_but_no_resolving_scene_surfaces():
    arg = Argument(
        id="A1", premise="x",
        resolution_direction=ResolutionDirection.AFFIRM,
    )
    t = Throughline(
        id="T1", role_label="main-character", owners=("C1",), subject="x",
        argument_contributions=(
            ArgumentContribution(argument_id="A1", side=ArgumentSide.AFFIRMS),
        ),
    )
    c = Character(id="C1", name="x")
    sc = Scene(
        id="S1", title="x", narrative_position=1,
        advances=(SceneAdvancement(throughline_id="T1"),),
        # result is empty
    )
    s = _trivial_story(
        argument_ids=("A1",), throughline_ids=("T1",),
        character_ids=("C1",), scene_ids=("S1",),
    )
    obs = verify(s, arguments=(arg,), throughlines=(t,), characters=(c,), scenes=(sc,))
    assert "argument_no_resolving_scene" in _codes(obs)


def test_unresolved_argument_skips_completeness_check():
    arg = Argument(
        id="A1", premise="x",
        resolution_direction=ResolutionDirection.UNRESOLVED,
    )
    s = _trivial_story(argument_ids=("A1",))
    obs = verify(s, arguments=(arg,))
    # No completeness observations for unresolved arguments.
    assert "argument_no_throughline_contribution" not in _codes(obs)
    assert "argument_no_resolving_scene" not in _codes(obs)


# ----------------------------------------------------------------------------
# M8.6 — stakes coverage
# ----------------------------------------------------------------------------


def test_throughline_with_no_stakes_surfaces():
    t = Throughline(
        id="T1", role_label="main-character", owners=("C1",), subject="x",
    )
    c = Character(id="C1", name="x")
    s = _trivial_story(throughline_ids=("T1",), character_ids=("C1",))
    obs = verify(s, throughlines=(t,), characters=(c,))
    assert "throughline_no_stakes" in _codes(obs)


def test_throughline_with_stakes_via_owner_passes():
    t = Throughline(
        id="T1", role_label="main-character", owners=("C1",), subject="x",
    )
    c = Character(id="C1", name="x")
    st = Stakes(
        id="St1",
        owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE, id="T1"),
        at_risk="x", to_gain="y",
    )
    s = _trivial_story(
        throughline_ids=("T1",), character_ids=("C1",), stakes_ids=("St1",),
    )
    obs = verify(s, throughlines=(t,), characters=(c,), stakes=(st,))
    assert "throughline_no_stakes" not in _codes(obs)


def test_throughline_with_stakes_id_field_passes():
    """Stakes coverage should detect via Throughline.stakes_id even if
    no Stakes record is in the bundle (it would surface as
    id_unresolved separately, which is correct)."""
    t = Throughline(
        id="T1", role_label="main-character", owners=("C1",), subject="x",
        stakes_id="St_unknown",
    )
    c = Character(id="C1", name="x")
    s = _trivial_story(throughline_ids=("T1",), character_ids=("C1",))
    obs = verify(s, throughlines=(t,), characters=(c,))
    # No "throughline_no_stakes" — the field is set, even if the id
    # doesn't resolve. (Resolution is M8.1's concern; this is M8.6.)
    assert "throughline_no_stakes" not in _codes(obs)


# ----------------------------------------------------------------------------
# M8.7 — scene purpose
# ----------------------------------------------------------------------------


def test_scene_with_empty_advances_surfaces():
    sc = Scene(id="S1", title="x", narrative_position=1, advances=())
    s = _trivial_story(scene_ids=("S1",))
    obs = verify(s, scenes=(sc,))
    assert "scene_no_purpose" in _codes(obs)


def test_scene_with_advances_passes():
    t = Throughline(
        id="T1", role_label="main-character", owners=("C1",), subject="x",
    )
    c = Character(id="C1", name="x")
    sc = Scene(
        id="S1", title="x", narrative_position=1,
        advances=(SceneAdvancement(throughline_id="T1"),),
    )
    s = _trivial_story(
        throughline_ids=("T1",), character_ids=("C1",), scene_ids=("S1",),
    )
    obs = verify(s, throughlines=(t,), characters=(c,), scenes=(sc,))
    assert "scene_no_purpose" not in _codes(obs)


# ----------------------------------------------------------------------------
# M8.8 — orphans
# ----------------------------------------------------------------------------


def test_record_not_listed_in_story_ids_surfaces_orphan():
    arg = Argument(
        id="A_orphan", premise="x",
        resolution_direction=ResolutionDirection.UNRESOLVED,
    )
    # Story does not list A_orphan in argument_ids.
    s = _trivial_story()
    obs = verify(s, arguments=(arg,))
    assert "record_orphan" in _codes(obs)


# ----------------------------------------------------------------------------
# Grouping helpers
# ----------------------------------------------------------------------------


def test_group_by_severity_buckets_correctly():
    obs = [
        Observation(severity="noted", code="x", target_id="t1", message="m"),
        Observation(severity="advises-review", code="y", target_id="t2", message="m"),
        Observation(severity="noted", code="z", target_id="t3", message="m"),
    ]
    g = group_by_severity(obs)
    assert len(g["noted"]) == 2
    assert len(g["advises-review"]) == 1


def test_group_by_code_buckets_correctly():
    obs = [
        Observation(severity="noted", code="A", target_id="t1", message="m"),
        Observation(severity="noted", code="A", target_id="t2", message="m"),
        Observation(severity="noted", code="B", target_id="t3", message="m"),
    ]
    g = group_by_code(obs)
    assert len(g["A"]) == 2
    assert len(g["B"]) == 1


# ----------------------------------------------------------------------------
# Integration — the Oedipus dramatic encoding
# ----------------------------------------------------------------------------


def test_oedipus_dramatic_produces_expected_observations():
    """The encoding's verifier output is the contract: three
    observations (1 slot_unfilled for Antagonist; 2 throughline_no_
    stakes for T_impact_jocasta and T_relationship_oj). All other
    checks pass: id resolution, beat sequencing, scene sequencing,
    no orphans, no scene-no-purpose, no argument-incompleteness."""
    import oedipus_dramatic as o
    obs = verify(
        o.STORY,
        arguments=o.ARGUMENTS, throughlines=o.THROUGHLINES,
        characters=o.CHARACTERS, scenes=o.SCENES,
        beats=o.BEATS, stakes=o.STAKES,
    )
    by_code = group_by_code(obs)

    # Exactly one slot_unfilled, the Antagonist.
    assert len(by_code.get("slot_unfilled", [])) == 1
    antagonist = by_code["slot_unfilled"][0]
    assert "Antagonist" in antagonist.target_id

    # Exactly two throughline_no_stakes, IC and Relationship.
    no_stakes = by_code.get("throughline_no_stakes", [])
    assert len(no_stakes) == 2
    no_stakes_ids = {o.target_id for o in no_stakes}
    assert no_stakes_ids == {"T_impact_jocasta", "T_relationship_oj"}

    # No id_unresolved, no orphans, no scene-no-purpose.
    assert "id_unresolved" not in by_code
    assert "record_orphan" not in by_code
    assert "scene_no_purpose" not in by_code
    assert "beat_position_duplicate" not in by_code
    assert "scene_position_duplicate" not in by_code


def test_oedipus_dramatic_argument_resolves_in_view():
    """The Argument is AFFIRM and has Throughline contributions and
    Scenes with `result` text advancing those Throughlines, so the
    soft argument_completeness check passes."""
    import oedipus_dramatic as o
    obs = verify(
        o.STORY,
        arguments=o.ARGUMENTS, throughlines=o.THROUGHLINES,
        characters=o.CHARACTERS, scenes=o.SCENES,
        beats=o.BEATS, stakes=o.STAKES,
    )
    assert "argument_no_throughline_contribution" not in _codes(obs)
    assert "argument_no_resolving_scene" not in _codes(obs)


# ----------------------------------------------------------------------------
# Integration — the Macbeth dramatic encoding
# ----------------------------------------------------------------------------


def test_macbeth_dramatic_produces_zero_observations():
    """The encoding's verifier output is the contract: zero
    observations. Every dramatica-8 slot is filled, all four
    Throughlines have Stakes, every Scene declares advances, all
    ids resolve, no orphans, no duplicate positions. Macbeth's
    encoding is honest about its design choices: where Oedipus
    leaves the Antagonist deliberately unfilled, Macbeth assigns
    Macduff; where Oedipus leaves IC and Relationship Stakes
    entwined with the MC, Macbeth treats them as separable.

    A successful clean run on Macbeth — given that Oedipus produces
    3 observations on the same dialect — is itself a finding: the
    dialect admits both encodings without revision, and the
    verifier's output is sensitive to authorial choices, not noise.
    """
    import macbeth_dramatic as m
    obs = verify(
        m.STORY,
        arguments=m.ARGUMENTS, throughlines=m.THROUGHLINES,
        characters=m.CHARACTERS, scenes=m.SCENES,
        beats=m.BEATS, stakes=m.STAKES,
    )
    assert len(obs) == 0, (
        f"Macbeth dramatic should produce 0 observations; got "
        f"{len(obs)}: {[o.code for o in obs]}"
    )


def test_macbeth_dramatic_overfilling_antagonist_surfaces():
    """If an alternative encoding gives Lady Macbeth the Antagonist
    label too, the multi-antagonist reading surfaces as a slot
    overfilled observation. This pins the verifier's behavior on
    the deliberate authorial choice the canonical encoding declines
    to make."""
    import macbeth_dramatic as m
    # Build a modified Lady Macbeth carrying both Contagonist and
    # Antagonist; substitute her in the characters tuple.
    modified_lady = Character(
        id="C_lady_macbeth", name="Lady Macbeth",
        function_labels=("Contagonist", "Antagonist"),
    )
    modified_characters = tuple(
        modified_lady if c.id == "C_lady_macbeth" else c
        for c in m.CHARACTERS
    )
    obs = verify(
        m.STORY,
        arguments=m.ARGUMENTS, throughlines=m.THROUGHLINES,
        characters=modified_characters, scenes=m.SCENES,
        beats=m.BEATS, stakes=m.STAKES,
    )
    # Antagonist now has count=2; expected slot_overfilled.
    overfilled = [
        o for o in obs
        if o.code == "slot_overfilled" and "Antagonist" in o.target_id
    ]
    assert len(overfilled) == 1, (
        f"expected one Antagonist slot_overfilled; got "
        f"{[o.target_id for o in obs if o.code == 'slot_overfilled']}"
    )


# ----------------------------------------------------------------------------
# Test runner
# ----------------------------------------------------------------------------


TESTS = [
    # M5 / Templates
    test_dramatica_8_has_eight_exactly_one_slots,
    test_three_actor_template_has_two_required_one_at_least_one,
    test_template_slot_for_label,
    # M8.1 — id resolution
    test_unknown_template_id_surfaces_observation,
    test_story_references_unknown_record_id,
    test_throughline_owners_can_use_abstract_sentinels,
    test_throughline_owners_with_unknown_character_id_surfaces,
    test_scene_advances_unknown_throughline_surfaces,
    test_beat_with_unknown_throughline_surfaces,
    test_stakes_owner_throughline_id_must_resolve,
    test_stakes_owner_story_id_must_match_story,
    # M8.2 / 8.3 — sequencing
    test_duplicate_beat_positions_surface,
    test_distinct_beat_positions_within_throughline_pass,
    test_duplicate_scene_positions_surface,
    # M8.4 / M9 — template conformance
    test_unknown_function_label_surfaces,
    test_exactly_one_with_zero_count_surfaces_unfilled,
    test_exactly_one_with_two_counts_surfaces_overfilled,
    test_at_least_one_with_zero_count_surfaces_unfilled,
    test_at_least_one_with_multiple_count_passes,
    test_any_multiplicity_never_triggers,
    test_no_template_means_no_multiplicity_check,
    # M8.5 — argument completeness
    test_argument_with_no_contributing_throughline_surfaces,
    test_argument_with_contribution_but_no_resolving_scene_surfaces,
    test_unresolved_argument_skips_completeness_check,
    # M8.6 — stakes coverage
    test_throughline_with_no_stakes_surfaces,
    test_throughline_with_stakes_via_owner_passes,
    test_throughline_with_stakes_id_field_passes,
    # M8.7 — scene purpose
    test_scene_with_empty_advances_surfaces,
    test_scene_with_advances_passes,
    # M8.8 — orphans
    test_record_not_listed_in_story_ids_surfaces_orphan,
    # Helpers
    test_group_by_severity_buckets_correctly,
    test_group_by_code_buckets_correctly,
    # Integration — Oedipus
    test_oedipus_dramatic_produces_expected_observations,
    test_oedipus_dramatic_argument_resolves_in_view,
    # Integration — Macbeth
    test_macbeth_dramatic_produces_zero_observations,
    test_macbeth_dramatic_overfilling_antagonist_surfaces,
]


def main() -> int:
    passed = 0
    failed = 0
    for test in TESTS:
        try:
            test()
        except AssertionError as e:
            print(f"FAIL  {test.__name__}")
            print(f"      {e}")
            failed += 1
            continue
        except Exception:
            print(f"ERROR {test.__name__}")
            traceback.print_exc()
            failed += 1
            continue
        print(f"ok    {test.__name__}")
        passed += 1

    print()
    print(f"{passed} passed, {failed} failed, {len(TESTS)} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
