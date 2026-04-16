"""
test_dramatica_template.py — tests for the dramatica-complete Template.

Pins every validation rule and structural constraint the Template
enforces. Organized by the sketch's Q-number commitments.
"""

from __future__ import annotations

import sys
import traceback

from dramatica_template import (
    # Record types
    Quad, QuadPick, DomainAssignment, DynamicStoryPoint, Signpost,
    CharacterElementAssignment, ThematicPicks,
    # Enums
    Domain, DSPAxis, QuadPosition,
    Resolve, Growth, Approach, Limit, Outcome, Judgment,
    MotivationElement,
    DSP_VALID_CHOICES,
    # Shipped data
    DOMAIN_QUAD, CONCERN_QUADS_BY_DOMAIN,
    CONCERN_ACTIVITY_QUAD, CONCERN_SITUATION_QUAD,
    CONCERN_MANIPULATION_QUAD, CONCERN_FIXED_ATTITUDE_QUAD,
    ALL_SHIPPED_QUADS,
    ARCHETYPE_MOTIVATION_ELEMENTS,
    ISSUE_QUADS_BY_CONCERN, ELEMENT_QUADS_BY_ISSUE,
    register_issue_quad, register_element_quad,
    # Observation types
    DramaticaObservation, SEVERITY_NOTED, SEVERITY_ADVISES_REVIEW,
    # Verifier
    verify_dramatica_complete,
    verify_character_elements,
    verify_thematic_picks,
    # Derivation
    derive_from_problem,
    # Convenience
    canonical_ending,
)

from dramatic import (
    Throughline, Character,
    THROUGHLINE_OWNER_SITUATION, THROUGHLINE_OWNER_RELATIONSHIP,
)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


def _make_throughlines():
    """Minimal four-Throughline set for testing."""
    return (
        Throughline(id="T_os", role_label="overall-story",
                    owners=(THROUGHLINE_OWNER_SITUATION,), subject="os"),
        Throughline(id="T_mc", role_label="main-character",
                    owners=("C_mc",), subject="mc"),
        Throughline(id="T_ic", role_label="impact-character",
                    owners=("C_ic",), subject="ic"),
        Throughline(id="T_rs", role_label="relationship",
                    owners=(THROUGHLINE_OWNER_RELATIONSHIP,), subject="rs"),
    )


def _make_domain_assignments(throughlines=None):
    """Clean four-domain assignment set."""
    tls = throughlines or _make_throughlines()
    return (
        DomainAssignment(id="DA_1", throughline_id=tls[0].id,
                         domain=Domain.SITUATION),
        DomainAssignment(id="DA_2", throughline_id=tls[1].id,
                         domain=Domain.ACTIVITY),
        DomainAssignment(id="DA_3", throughline_id=tls[2].id,
                         domain=Domain.FIXED_ATTITUDE),
        DomainAssignment(id="DA_4", throughline_id=tls[3].id,
                         domain=Domain.MANIPULATION),
    )


def _make_dsps():
    """Clean six-DSP set."""
    return (
        DynamicStoryPoint(id="DSP_1", axis=DSPAxis.RESOLVE,
                          choice="change", story_id="S"),
        DynamicStoryPoint(id="DSP_2", axis=DSPAxis.GROWTH,
                          choice="stop", story_id="S"),
        DynamicStoryPoint(id="DSP_3", axis=DSPAxis.APPROACH,
                          choice="do-er", story_id="S"),
        DynamicStoryPoint(id="DSP_4", axis=DSPAxis.LIMIT,
                          choice="optionlock", story_id="S"),
        DynamicStoryPoint(id="DSP_5", axis=DSPAxis.OUTCOME,
                          choice="success", story_id="S"),
        DynamicStoryPoint(id="DSP_6", axis=DSPAxis.JUDGMENT,
                          choice="bad", story_id="S"),
    )


def _make_signposts_for(throughline_id, domain):
    """Clean four-signpost set for one Throughline."""
    cq = CONCERN_QUADS_BY_DOMAIN[domain]
    return (
        Signpost(id=f"SP_{throughline_id}_1",
                 throughline_id=throughline_id,
                 signpost_position=1,
                 signpost_element=cq.element_A),
        Signpost(id=f"SP_{throughline_id}_2",
                 throughline_id=throughline_id,
                 signpost_position=2,
                 signpost_element=cq.element_B),
        Signpost(id=f"SP_{throughline_id}_3",
                 throughline_id=throughline_id,
                 signpost_position=3,
                 signpost_element=cq.element_C),
        Signpost(id=f"SP_{throughline_id}_4",
                 throughline_id=throughline_id,
                 signpost_position=4,
                 signpost_element=cq.element_D),
    )


def _codes(observations):
    return {o.code for o in observations}


def _full_clean_encoding():
    """Return (throughlines, das, dsps, all_signposts) that should
    produce 0 observations from verify_dramatica_complete."""
    tls = _make_throughlines()
    das = _make_domain_assignments(tls)
    dsps = _make_dsps()
    sps = ()
    for da in das:
        sps += _make_signposts_for(da.throughline_id, da.domain)
    return tls, das, dsps, sps


# ============================================================================
# Q2 — Quad structure
# ============================================================================


def test_quad_has_four_elements():
    q = DOMAIN_QUAD
    elements = {q.element_A, q.element_B, q.element_C, q.element_D}
    assert len(elements) == 4


def test_quad_dynamic_pairs():
    q = DOMAIN_QUAD
    assert q.dynamic_pairs == (
        (q.element_A, q.element_C),
        (q.element_B, q.element_D),
    )


def test_quad_companion_pairs():
    q = DOMAIN_QUAD
    assert q.companion_pairs == (
        (q.element_A, q.element_B),
        (q.element_C, q.element_D),
    )


def test_quad_element_at():
    q = DOMAIN_QUAD
    assert q.element_at(QuadPosition.A) == Domain.ACTIVITY.value
    assert q.element_at(QuadPosition.D) == Domain.FIXED_ATTITUDE.value


def test_quad_dynamic_pair_of():
    q = DOMAIN_QUAD
    assert q.dynamic_pair_of(QuadPosition.A) == QuadPosition.C
    assert q.dynamic_pair_of(QuadPosition.C) == QuadPosition.A
    assert q.dynamic_pair_of(QuadPosition.B) == QuadPosition.D


# ============================================================================
# Shipped theory data
# ============================================================================


def test_domain_quad_has_four_domains():
    elements = {DOMAIN_QUAD.element_A, DOMAIN_QUAD.element_B,
                DOMAIN_QUAD.element_C, DOMAIN_QUAD.element_D}
    assert elements == {d.value for d in Domain}


def test_concern_quads_cover_all_domains():
    assert set(CONCERN_QUADS_BY_DOMAIN.keys()) == set(Domain)


def test_each_concern_quad_has_four_distinct_elements():
    for domain, cq in CONCERN_QUADS_BY_DOMAIN.items():
        elements = {cq.element_A, cq.element_B,
                    cq.element_C, cq.element_D}
        assert len(elements) == 4, (
            f"Concern quad for {domain.value} has duplicate elements"
        )


def test_shipped_quads_total_five():
    assert len(ALL_SHIPPED_QUADS) == 5


# ============================================================================
# DynamicStoryPoint construction validation
# ============================================================================


def test_dsp_valid_choice_accepted():
    dsp = DynamicStoryPoint(
        id="test", axis=DSPAxis.RESOLVE, choice="change", story_id="S",
    )
    assert dsp.choice == "change"


def test_dsp_invalid_choice_rejected():
    try:
        DynamicStoryPoint(
            id="bad", axis=DSPAxis.RESOLVE, choice="maybe", story_id="S",
        )
        assert False, "should have raised ValueError"
    except ValueError:
        pass


def test_dsp_all_axes_have_exactly_two_valid_choices():
    for axis, choices in DSP_VALID_CHOICES.items():
        assert len(choices) == 2, (
            f"axis {axis.value} should have 2 choices; got {len(choices)}"
        )


# ============================================================================
# Signpost construction validation
# ============================================================================


def test_signpost_valid_position_accepted():
    sp = Signpost(id="sp", throughline_id="T", signpost_position=1,
                  signpost_element="learning")
    assert sp.signpost_position == 1


def test_signpost_invalid_position_rejected():
    try:
        Signpost(id="bad", throughline_id="T", signpost_position=0,
                 signpost_element="x")
        assert False, "position 0 should be rejected"
    except ValueError:
        pass
    try:
        Signpost(id="bad2", throughline_id="T", signpost_position=5,
                 signpost_element="x")
        assert False, "position 5 should be rejected"
    except ValueError:
        pass


# ============================================================================
# Throughline count validation
# ============================================================================


def test_throughline_count_exactly_four_passes():
    tls, das, dsps, sps = _full_clean_encoding()
    obs = verify_dramatica_complete(
        throughlines=tls, domain_assignments=das,
        dynamic_story_points=dsps, signposts=sps,
        story_goal="g", story_consequence="c",
    )
    assert "throughline_count_wrong" not in _codes(obs)


def test_throughline_count_three_flagged():
    tls = _make_throughlines()[:3]
    obs = verify_dramatica_complete(
        throughlines=tls, story_goal="g", story_consequence="c",
    )
    assert "throughline_count_wrong" in _codes(obs)


def test_missing_throughline_role_flagged():
    tls = list(_make_throughlines())
    # Replace relationship with a second main-character.
    tls[3] = Throughline(id="T_mc2", role_label="main-character",
                         owners=("C_x",), subject="mc2")
    obs = verify_dramatica_complete(
        throughlines=tuple(tls), story_goal="g", story_consequence="c",
    )
    assert "throughline_role_missing" in _codes(obs)


# ============================================================================
# Domain assignment validation
# ============================================================================


def test_domain_assignments_clean_passes():
    tls, das, dsps, sps = _full_clean_encoding()
    obs = verify_dramatica_complete(
        throughlines=tls, domain_assignments=das,
        dynamic_story_points=dsps, signposts=sps,
        story_goal="g", story_consequence="c",
    )
    domain_codes = {o.code for o in obs if "domain" in o.code}
    assert len(domain_codes) == 0


def test_domain_duplicate_flagged():
    tls = _make_throughlines()
    das = (
        DomainAssignment(id="DA_1", throughline_id="T_os",
                         domain=Domain.SITUATION),
        DomainAssignment(id="DA_2", throughline_id="T_mc",
                         domain=Domain.SITUATION),  # DUPE
        DomainAssignment(id="DA_3", throughline_id="T_ic",
                         domain=Domain.FIXED_ATTITUDE),
        DomainAssignment(id="DA_4", throughline_id="T_rs",
                         domain=Domain.MANIPULATION),
    )
    obs = verify_dramatica_complete(
        throughlines=tls, domain_assignments=das,
        story_goal="g", story_consequence="c",
    )
    codes = _codes(obs)
    assert "domain_assignment_duplicate" in codes
    assert "domain_assignment_incomplete" in codes


def test_domain_missing_assignment_flagged():
    tls = _make_throughlines()
    das = _make_domain_assignments(tls)[:3]  # only 3
    obs = verify_dramatica_complete(
        throughlines=tls, domain_assignments=das,
        story_goal="g", story_consequence="c",
    )
    assert "domain_assignment_count_wrong" in _codes(obs)


# ============================================================================
# DSP validation
# ============================================================================


def test_dsp_all_six_passes():
    tls, das, dsps, sps = _full_clean_encoding()
    obs = verify_dramatica_complete(
        throughlines=tls, domain_assignments=das,
        dynamic_story_points=dsps, signposts=sps,
        story_goal="g", story_consequence="c",
    )
    assert "dsp_missing" not in _codes(obs)


def test_dsp_missing_axis_flagged():
    dsps = _make_dsps()[:5]  # drop judgment
    obs = verify_dramatica_complete(
        throughlines=_make_throughlines(),
        dynamic_story_points=dsps,
        story_goal="g", story_consequence="c",
    )
    assert "dsp_missing" in _codes(obs)


def test_dsp_duplicate_axis_flagged():
    dsps = _make_dsps() + (
        DynamicStoryPoint(id="DSP_dup", axis=DSPAxis.RESOLVE,
                          choice="steadfast", story_id="S"),
    )
    obs = verify_dramatica_complete(
        throughlines=_make_throughlines(),
        dynamic_story_points=dsps,
        story_goal="g", story_consequence="c",
    )
    assert "dsp_duplicate" in _codes(obs)


# ============================================================================
# Signpost validation
# ============================================================================


def test_signposts_clean_passes():
    tls, das, dsps, sps = _full_clean_encoding()
    obs = verify_dramatica_complete(
        throughlines=tls, domain_assignments=das,
        dynamic_story_points=dsps, signposts=sps,
        story_goal="g", story_consequence="c",
    )
    sp_codes = {o.code for o in obs if "signpost" in o.code}
    assert len(sp_codes) == 0


def test_signpost_missing_flagged():
    tls, das, dsps, _ = _full_clean_encoding()
    # Only give signposts for first Throughline
    sps = _make_signposts_for(tls[0].id, das[0].domain)
    obs = verify_dramatica_complete(
        throughlines=tls, domain_assignments=das,
        dynamic_story_points=dsps, signposts=sps,
        story_goal="g", story_consequence="c",
    )
    assert "signpost_count_wrong" in _codes(obs)


def test_signpost_wrong_element_flagged():
    tls, das, dsps, _ = _full_clean_encoding()
    # Give MC signposts with a wrong-domain element
    bad_sps = (
        Signpost(id="SP_1", throughline_id=tls[1].id,
                 signpost_position=1, signpost_element="understanding"),
        Signpost(id="SP_2", throughline_id=tls[1].id,
                 signpost_position=2, signpost_element="the-past"),  # WRONG
        Signpost(id="SP_3", throughline_id=tls[1].id,
                 signpost_position=3, signpost_element="doing"),
        Signpost(id="SP_4", throughline_id=tls[1].id,
                 signpost_position=4, signpost_element="obtaining"),
    )
    other_sps = ()
    for i in [0, 2, 3]:
        other_sps += _make_signposts_for(tls[i].id, das[i].domain)
    obs = verify_dramatica_complete(
        throughlines=tls, domain_assignments=das,
        dynamic_story_points=dsps, signposts=bad_sps + other_sps,
        story_goal="g", story_consequence="c",
    )
    assert "signpost_element_invalid" in _codes(obs)


def test_signpost_duplicate_position_flagged():
    tls, das, dsps, _ = _full_clean_encoding()
    cq = CONCERN_QUADS_BY_DOMAIN[das[1].domain]
    bad_sps = (
        Signpost(id="SP_1", throughline_id=tls[1].id,
                 signpost_position=1, signpost_element=cq.element_A),
        Signpost(id="SP_2", throughline_id=tls[1].id,
                 signpost_position=1, signpost_element=cq.element_B),  # DUPE pos
        Signpost(id="SP_3", throughline_id=tls[1].id,
                 signpost_position=3, signpost_element=cq.element_C),
        Signpost(id="SP_4", throughline_id=tls[1].id,
                 signpost_position=4, signpost_element=cq.element_D),
    )
    other_sps = ()
    for i in [0, 2, 3]:
        other_sps += _make_signposts_for(tls[i].id, das[i].domain)
    obs = verify_dramatica_complete(
        throughlines=tls, domain_assignments=das,
        dynamic_story_points=dsps, signposts=bad_sps + other_sps,
        story_goal="g", story_consequence="c",
    )
    assert "signpost_positions_invalid" in _codes(obs)


# ============================================================================
# Story Goal / Consequence validation
# ============================================================================


def test_story_goal_empty_flagged():
    obs = verify_dramatica_complete(
        throughlines=_make_throughlines(),
        story_goal="", story_consequence="c",
    )
    assert "story_goal_empty" in _codes(obs)


def test_story_consequence_empty_flagged():
    obs = verify_dramatica_complete(
        throughlines=_make_throughlines(),
        story_goal="g", story_consequence="",
    )
    assert "story_consequence_empty" in _codes(obs)


# ============================================================================
# Canonical ending derivation
# ============================================================================


def test_canonical_ending_personal_tragedy():
    assert canonical_ending("success", "bad") == "personal-tragedy"


def test_canonical_ending_triumph():
    assert canonical_ending("success", "good") == "triumph"


def test_canonical_ending_tragedy():
    assert canonical_ending("failure", "bad") == "tragedy"


def test_canonical_ending_personal_triumph():
    assert canonical_ending("failure", "good") == "personal-triumph"


# ============================================================================
# Full clean encoding: zero observations
# ============================================================================


def test_full_clean_encoding_produces_zero_observations():
    """A fully-populated clean encoding should produce zero
    observations from the Dramatica-complete verifier."""
    tls, das, dsps, sps = _full_clean_encoding()
    obs = verify_dramatica_complete(
        throughlines=tls, domain_assignments=das,
        dynamic_story_points=dsps, signposts=sps,
        story_goal="identify the killer",
        story_consequence="the killer goes free",
    )
    assert len(obs) == 0, (
        f"expected 0 observations on a clean encoding; got "
        f"{len(obs)}: {[o.code for o in obs]}"
    )


# ============================================================================
# Integration: Oedipus against dramatica-complete
# ============================================================================


def test_oedipus_partial_encoding_surfaces_expected_gaps():
    """Oedipus with MC Signposts only — the other 3 Throughlines
    should surface signpost_count_wrong observations."""
    from oedipus_dramatic import THROUGHLINES

    das = (
        DomainAssignment(id="DA_1", throughline_id="T_overall_plague",
                         domain=Domain.SITUATION),
        DomainAssignment(id="DA_2", throughline_id="T_mc_oedipus",
                         domain=Domain.ACTIVITY),
        DomainAssignment(id="DA_3", throughline_id="T_impact_jocasta",
                         domain=Domain.FIXED_ATTITUDE),
        DomainAssignment(id="DA_4", throughline_id="T_relationship_oj",
                         domain=Domain.MANIPULATION),
    )
    dsps = (
        DynamicStoryPoint(id="D1", axis=DSPAxis.RESOLVE, choice="change", story_id="S"),
        DynamicStoryPoint(id="D2", axis=DSPAxis.GROWTH, choice="stop", story_id="S"),
        DynamicStoryPoint(id="D3", axis=DSPAxis.APPROACH, choice="do-er", story_id="S"),
        DynamicStoryPoint(id="D4", axis=DSPAxis.LIMIT, choice="optionlock", story_id="S"),
        DynamicStoryPoint(id="D5", axis=DSPAxis.OUTCOME, choice="success", story_id="S"),
        DynamicStoryPoint(id="D6", axis=DSPAxis.JUDGMENT, choice="bad", story_id="S"),
    )
    mc_sps = _make_signposts_for("T_mc_oedipus", Domain.ACTIVITY)

    obs = verify_dramatica_complete(
        throughlines=THROUGHLINES,
        domain_assignments=das,
        dynamic_story_points=dsps,
        signposts=mc_sps,
        story_goal="identify the pollution causing the plague",
        story_consequence="the plague continues; the city dies",
    )
    codes = _codes(obs)
    assert "signpost_count_wrong" in codes
    # Exactly 3 missing (OS, IC, RS — MC has its 4)
    sp_missing = [o for o in obs if o.code == "signpost_count_wrong"]
    assert len(sp_missing) == 3


# ============================================================================
# Pick chain + derivation
# ============================================================================


# A test Issue Quad registered for the Activity Domain's "understanding"
# Concern. Lets us test the chain validation without needing the full
# 64-Variation data set.
_TEST_ISSUE_QUAD_UNDERSTANDING = Quad(
    id="issue_understanding_test",
    kind="issue-quad",
    element_A="instinct",
    element_B="senses",
    element_C="interpretation",
    element_D="conditioning",
)
register_issue_quad("understanding", _TEST_ISSUE_QUAD_UNDERSTANDING)

# A test Element Quad registered under the Issue "instinct".
_TEST_ELEMENT_QUAD_INSTINCT = Quad(
    id="element_instinct_test",
    kind="element-quad",
    element_A="pursue",
    element_B="prevent",
    element_C="avoid",
    element_D="reconsider",
)
register_element_quad("instinct", _TEST_ELEMENT_QUAD_INSTINCT)


def test_derive_solution_is_dynamic_pair():
    """Solution is the dynamic pair of the Problem position."""
    pick = QuadPick(
        id="P1", quad_id="element_instinct_test",
        chosen_position=QuadPosition.A,
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    derived = derive_from_problem(pick, _TEST_ELEMENT_QUAD_INSTINCT)
    assert derived["solution"] == (QuadPosition.C, "avoid"), (
        f"Problem at A ('pursue') → Solution should be at C "
        f"('avoid'); got {derived['solution']}"
    )


def test_derive_symptom_is_companion():
    """Symptom is the companion of the Problem (A↔B, C↔D)."""
    pick = QuadPick(
        id="P1", quad_id="element_instinct_test",
        chosen_position=QuadPosition.A,
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    derived = derive_from_problem(pick, _TEST_ELEMENT_QUAD_INSTINCT)
    assert derived["symptom"] == (QuadPosition.B, "prevent"), (
        f"Problem at A → Symptom should be at B ('prevent'); "
        f"got {derived['symptom']}"
    )


def test_derive_response_is_dependent():
    """Response is the dependent (diagonal) of the Problem."""
    pick = QuadPick(
        id="P1", quad_id="element_instinct_test",
        chosen_position=QuadPosition.A,
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    derived = derive_from_problem(pick, _TEST_ELEMENT_QUAD_INSTINCT)
    assert derived["response"] == (QuadPosition.D, "reconsider"), (
        f"Problem at A → Response should be at D ('reconsider'); "
        f"got {derived['response']}"
    )


def test_pick_chain_clean_passes():
    """A correctly-chained set of picks — Concern from Domain's quad,
    Issue from Concern's Issue Quad, Problem from Issue's Element
    Quad — produces no chain-related observations."""
    tls = _make_throughlines()
    das = _make_domain_assignments(tls)
    # MC is T_mc, Domain = ACTIVITY. Concern Quad = Activity's.
    concern_pick = QuadPick(
        id="CP_mc", quad_id=CONCERN_ACTIVITY_QUAD.id,
        chosen_position=QuadPosition.A,  # "understanding"
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    issue_pick = QuadPick(
        id="IP_mc", quad_id=_TEST_ISSUE_QUAD_UNDERSTANDING.id,
        chosen_position=QuadPosition.A,  # "instinct"
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    problem_pick = QuadPick(
        id="PP_mc", quad_id=_TEST_ELEMENT_QUAD_INSTINCT.id,
        chosen_position=QuadPosition.A,  # "pursue"
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    tp = ThematicPicks(
        throughline_id="T_mc",
        concern_pick=concern_pick,
        issue_pick=issue_pick,
        problem_pick=problem_pick,
    )
    obs = verify_thematic_picks(
        picks_list=(tp,), domain_assignments=das,
    )
    chain_codes = {o.code for o in obs
                   if "pick" in o.code or "override" in o.code}
    assert len(chain_codes) == 0, (
        f"expected no chain observations; got {chain_codes}"
    )


def test_pick_chain_wrong_concern_quad_flagged():
    """If the Concern pick references the wrong Domain's Concern
    Quad, the chain validator catches it."""
    tls = _make_throughlines()
    das = _make_domain_assignments(tls)
    # MC is in ACTIVITY but we reference SITUATION's Concern Quad.
    concern_pick = QuadPick(
        id="CP_bad", quad_id=CONCERN_SITUATION_QUAD.id,  # WRONG
        chosen_position=QuadPosition.A,
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    issue_pick = QuadPick(
        id="IP", quad_id="whatever",
        chosen_position=QuadPosition.A,
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    problem_pick = QuadPick(
        id="PP", quad_id="whatever",
        chosen_position=QuadPosition.A,
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    tp = ThematicPicks(
        throughline_id="T_mc",
        concern_pick=concern_pick,
        issue_pick=issue_pick,
        problem_pick=problem_pick,
    )
    obs = verify_thematic_picks(
        picks_list=(tp,), domain_assignments=das,
    )
    assert "concern_pick_wrong_quad" in _codes(obs)


def test_pick_chain_solution_override_mismatch_flagged():
    """If an explicit Solution override disagrees with the derivation,
    the validator catches it."""
    tls = _make_throughlines()
    das = _make_domain_assignments(tls)
    concern_pick = QuadPick(
        id="CP", quad_id=CONCERN_ACTIVITY_QUAD.id,
        chosen_position=QuadPosition.A,
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    issue_pick = QuadPick(
        id="IP", quad_id=_TEST_ISSUE_QUAD_UNDERSTANDING.id,
        chosen_position=QuadPosition.A,
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    problem_pick = QuadPick(
        id="PP", quad_id=_TEST_ELEMENT_QUAD_INSTINCT.id,
        chosen_position=QuadPosition.A,  # "pursue" → solution = "avoid"
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    tp = ThematicPicks(
        throughline_id="T_mc",
        concern_pick=concern_pick,
        issue_pick=issue_pick,
        problem_pick=problem_pick,
        solution_override="prevent",  # WRONG — should be "avoid"
    )
    obs = verify_thematic_picks(
        picks_list=(tp,), domain_assignments=das,
    )
    assert "solution_override_mismatch" in _codes(obs)


def test_pick_chain_correct_override_passes():
    """If an explicit Solution override agrees with the derivation,
    no mismatch observation."""
    tls = _make_throughlines()
    das = _make_domain_assignments(tls)
    concern_pick = QuadPick(
        id="CP", quad_id=CONCERN_ACTIVITY_QUAD.id,
        chosen_position=QuadPosition.A,
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    issue_pick = QuadPick(
        id="IP", quad_id=_TEST_ISSUE_QUAD_UNDERSTANDING.id,
        chosen_position=QuadPosition.A,
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    problem_pick = QuadPick(
        id="PP", quad_id=_TEST_ELEMENT_QUAD_INSTINCT.id,
        chosen_position=QuadPosition.A,  # "pursue" → solution = "avoid"
        attached_to_kind="throughline", attached_to_id="T_mc",
    )
    tp = ThematicPicks(
        throughline_id="T_mc",
        concern_pick=concern_pick,
        issue_pick=issue_pick,
        problem_pick=problem_pick,
        solution_override="avoid",  # CORRECT
    )
    obs = verify_thematic_picks(
        picks_list=(tp,), domain_assignments=das,
    )
    assert "solution_override_mismatch" not in _codes(obs)


# ============================================================================
# Character Element decomposition — Motivation Elements
# ============================================================================


def test_motivation_elements_count_sixteen():
    assert len(MotivationElement) == 16


def test_archetype_elements_cover_all_sixteen():
    """Each of the 16 Motivation Elements should appear exactly once
    across the 8 archetypes' canonical mappings."""
    all_elements = set()
    for fn, elements in ARCHETYPE_MOTIVATION_ELEMENTS.items():
        for e in elements:
            assert e not in all_elements, (
                f"Element {e.value!r} appears in multiple "
                f"archetypes (found in {fn!r})"
            )
            all_elements.add(e)
    assert all_elements == set(MotivationElement), (
        f"Archetype mappings should cover all 16 Motivation "
        f"Elements; missing: "
        f"{set(MotivationElement) - all_elements}"
    )


def test_element_uniqueness_clean_passes():
    """Assigning each element to exactly one character produces no
    uniqueness observations."""
    assignments = (
        CharacterElementAssignment(id="A1", character_id="C_hero",
                                   element=MotivationElement.PURSUE),
        CharacterElementAssignment(id="A2", character_id="C_villain",
                                   element=MotivationElement.PREVENT),
    )
    obs = verify_character_elements(assignments=assignments)
    assert "element_assigned_to_multiple_characters" not in _codes(obs)


def test_element_duplicate_flagged():
    """Assigning the same element to two characters is caught."""
    assignments = (
        CharacterElementAssignment(id="A1", character_id="C_hero",
                                   element=MotivationElement.PURSUE),
        CharacterElementAssignment(id="A2", character_id="C_villain",
                                   element=MotivationElement.PURSUE),
    )
    obs = verify_character_elements(assignments=assignments)
    assert "element_assigned_to_multiple_characters" in _codes(obs)


def test_archetype_conformance_clean_passes():
    """A character whose function label matches its element
    assignments produces no divergence observation."""
    char = Character(id="C_hero", name="Hero",
                     function_labels=("Protagonist",))
    assignments = (
        CharacterElementAssignment(id="A1", character_id="C_hero",
                                   element=MotivationElement.PURSUE),
        CharacterElementAssignment(id="A2", character_id="C_hero",
                                   element=MotivationElement.CONSIDER),
    )
    obs = verify_character_elements(
        assignments=assignments, characters=(char,),
    )
    assert "archetype_element_divergence" not in _codes(obs)


def test_archetype_divergence_noted():
    """A character carrying Protagonist function but non-canonical
    elements produces a NOTED divergence observation — valid for
    complex characters, but flagged so the author knows."""
    char = Character(id="C_complex", name="Complex Hero",
                     function_labels=("Protagonist",))
    assignments = (
        CharacterElementAssignment(id="A1", character_id="C_complex",
                                   element=MotivationElement.PURSUE),
        CharacterElementAssignment(id="A2", character_id="C_complex",
                                   element=MotivationElement.LOGIC),
    )
    obs = verify_character_elements(
        assignments=assignments, characters=(char,),
    )
    assert "archetype_element_divergence" in _codes(obs)
    divergence = [o for o in obs
                  if o.code == "archetype_element_divergence"][0]
    assert divergence.severity == SEVERITY_NOTED


# ============================================================================
# Runner
# ============================================================================


TESTS = [
    # Quad structure (Q2)
    test_quad_has_four_elements,
    test_quad_dynamic_pairs,
    test_quad_companion_pairs,
    test_quad_element_at,
    test_quad_dynamic_pair_of,
    # Shipped data
    test_domain_quad_has_four_domains,
    test_concern_quads_cover_all_domains,
    test_each_concern_quad_has_four_distinct_elements,
    test_shipped_quads_total_five,
    # DSP construction (Q5)
    test_dsp_valid_choice_accepted,
    test_dsp_invalid_choice_rejected,
    test_dsp_all_axes_have_exactly_two_valid_choices,
    # Signpost construction (Q7)
    test_signpost_valid_position_accepted,
    test_signpost_invalid_position_rejected,
    # Throughline validation
    test_throughline_count_exactly_four_passes,
    test_throughline_count_three_flagged,
    test_missing_throughline_role_flagged,
    # Domain assignment validation
    test_domain_assignments_clean_passes,
    test_domain_duplicate_flagged,
    test_domain_missing_assignment_flagged,
    # DSP validation
    test_dsp_all_six_passes,
    test_dsp_missing_axis_flagged,
    test_dsp_duplicate_axis_flagged,
    # Signpost validation
    test_signposts_clean_passes,
    test_signpost_missing_flagged,
    test_signpost_wrong_element_flagged,
    test_signpost_duplicate_position_flagged,
    # Story Goal / Consequence
    test_story_goal_empty_flagged,
    test_story_consequence_empty_flagged,
    # Canonical ending
    test_canonical_ending_personal_tragedy,
    test_canonical_ending_triumph,
    test_canonical_ending_tragedy,
    test_canonical_ending_personal_triumph,
    # Full clean encoding
    test_full_clean_encoding_produces_zero_observations,
    # Integration
    test_oedipus_partial_encoding_surfaces_expected_gaps,
    # Pick chain + derivation
    test_derive_solution_is_dynamic_pair,
    test_derive_symptom_is_companion,
    test_derive_response_is_dependent,
    test_pick_chain_clean_passes,
    test_pick_chain_wrong_concern_quad_flagged,
    test_pick_chain_solution_override_mismatch_flagged,
    test_pick_chain_correct_override_passes,
    # Character Elements
    test_motivation_elements_count_sixteen,
    test_archetype_elements_cover_all_sixteen,
    test_element_uniqueness_clean_passes,
    test_element_duplicate_flagged,
    test_archetype_conformance_clean_passes,
    test_archetype_divergence_noted,
]


def main() -> int:
    passed = 0
    failed = 0
    for test in TESTS:
        try:
            test()
        except (AssertionError, Exception) as e:
            print(f"FAIL  {test.__name__}")
            traceback.print_exc()
            failed += 1
        else:
            print(f"ok    {test.__name__}")
            passed += 1
    print(f"\n{passed} passed, {failed} failed, {passed + failed} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
