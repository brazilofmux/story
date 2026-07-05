"""Structural conformance for THE WINTER COUNT encoding + storyform —
all offline: referential integrity, act coverage, signpost quads, the
anti-marketing dynamics grid, and a dry-run brief build."""

from story_engine.core.dramatica_template import (
    CONCERN_SITUATION_QUAD, CONCERN_FIXED_ATTITUDE_QUAD,
    CONCERN_MANIPULATION_QUAD, CONCERN_ACTIVITY_QUAD,
    DSPAxis,
)
from story_engine.core.dramatica_generation import (
    DramaticaStoryform, DramaticaFrame,
)
from story_engine.core.draft_generator import generate_draft
from story_engine.encodings import winter_count as WC
from story_engine.encodings import winter_count_dramatica_complete as WD


def _storyform():
    return DramaticaStoryform(
        title="The Winter Count",
        action_summary="test",
        domain_assignments=WD.DOMAIN_ASSIGNMENTS,
        signposts=WD.ALL_SIGNPOSTS,
        dynamics=WD.DYNAMIC_STORY_POINTS,
        story_goal=WD.STORY_GOAL,
        story_consequence=WD.STORY_CONSEQUENCE,
        canonical_ending=WD.CANONICAL_ENDING,
        act_event_ids=WD.ACT_EVENT_IDS,
    )


def test_participants_and_staging_resolve():
    ent_ids = {e.id for e in WC.ENTITIES}
    for ev in WC.FABULA:
        for role, eid in ev.participants.items():
            assert eid in ent_ids, (ev.id, role, eid)
    fab_ids = {e.id for e in WC.FABULA}
    staged = [s.event_id for s in WC.SJUZHET]
    assert set(staged) <= fab_ids
    assert len(staged) == len(set(staged))


def test_descriptions_anchor_to_real_events():
    fab_ids = {e.id for e in WC.FABULA}
    noted = {d.attached_to.target_id for d in WC.DESCRIPTIONS}
    assert noted <= fab_ids
    # Every scene carries its authorial note — the texture is total.
    assert noted == fab_ids


def test_act_map_partitions_the_fabula():
    fab_ids = {e.id for e in WC.FABULA}
    acted = [eid for evs in WD.ACT_EVENT_IDS.values() for eid in evs]
    assert len(acted) == len(set(acted))
    assert set(acted) == fab_ids
    assert sorted(WD.ACT_EVENT_IDS) == [1, 2, 3, 4]


def test_signposts_use_each_concern_once_per_throughline():
    quad_by_tl = {
        "T_os_sealed_winter": CONCERN_SITUATION_QUAD,
        "T_mc_halla": CONCERN_FIXED_ATTITUDE_QUAD,
        "T_ic_eirik": CONCERN_MANIPULATION_QUAD,
        "T_rel_siblings": CONCERN_ACTIVITY_QUAD,
    }
    for tl, quad in quad_by_tl.items():
        sps = [s for s in WD.ALL_SIGNPOSTS if s.throughline_id == tl]
        assert sorted(s.signpost_position for s in sps) == [1, 2, 3, 4]
        assert {s.signpost_element for s in sps} == {
            quad.element_A, quad.element_B, quad.element_C, quad.element_D,
        }


def test_the_anti_marketing_grid_holds():
    dyn = {d.axis: d.choice for d in WD.DYNAMIC_STORY_POINTS}
    assert dyn[DSPAxis.RESOLVE] == "steadfast"     # no arc
    assert dyn[DSPAxis.OUTCOME] == "failure"       # the goal is lost
    assert dyn[DSPAxis.JUDGMENT] == "bad"          # no consolation
    assert dyn[DSPAxis.DRIVER] == "decision"       # no coincidence
    assert WD.CANONICAL_ENDING == "tragedy"


def test_signpost_details_cover_all_sixteen():
    assert set(WD.SIGNPOST_DETAILS) == {s.id for s in WD.ALL_SIGNPOSTS}


def test_rot_is_single_witness_and_retracts_public_belief():
    """The dread engine: E_rot_found contradicts the world's held belief
    and informs exactly one mind."""
    ev = next(e for e in WC.FABULA if e.id == "E_rot_found")
    world_retracts = [
        eff for eff in ev.effects
        if hasattr(eff, "asserts") and not eff.asserts
    ]
    assert any(eff.prop.predicate == "stores_enough"
               for eff in world_retracts)
    knowers = [eff.agent_id for eff in ev.effects
               if hasattr(eff, "agent_id")]
    assert knowers == ["halla"]


def test_dry_run_builds_bible_and_briefs_offline():
    frame = DramaticaFrame(_storyform(), WC.SJUZHET)
    result = generate_draft(
        title="The Winter Count", sjuzhet=WC.SJUZHET, fabula=WC.FABULA,
        entities=WC.ENTITIES, descriptions=WC.DESCRIPTIONS, adapter=frame,
        dialect_note="test", dry_run=True,
    )
    assert len(result.scenes) == len(WC.SJUZHET)
    assert "AUTHORED" in result.story_bible          # act boundaries
    assert "STEADFAST" in result.story_bible
    assert "FAILURE" in result.story_bible
    # The flashback brief carries its authorial note.
    flashback = next(s for s in result.scenes
                     if s.event_id == "E_ketil_fall")
    assert "Authorial note (texture)" in flashback.brief
