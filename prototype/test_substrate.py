"""
test_substrate.py — permanent tests for the substrate reference implementation.

Deliberately not a test framework. Plain assertions, a minimal runner,
no dependencies. Run with:

    python3 test_substrate.py

Each test is a named function. The runner calls them all, counts
passes and failures, and exits non-zero if anything failed.

Discipline of this file:

- Lock in what sketch 04 commits to.
- Lock in current implementation behavior for regression.
- Flag in the docstring when a test passes for a reason that is *not*
  settled in sketch 04 — these are conventions we happen to have, not
  things the design has ratified. Examples: the operational definition
  of GAP in the prototype, the treatment of the Held record attached
  to a remove-effect, the coupling (or lack of) between Slot and
  Confidence.

These flags exist because story substrates are exceedingly hard to
schematize, and it is easy to turn conventions into dogma via test
coverage. The tests below try not to do that.
"""

from __future__ import annotations

import sys
import traceback

from substrate import (
    Entity, Prop, Branch, BranchKind, CANONICAL, CANONICAL_LABEL,
    Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect, Event, EventStatus,
    SjuzhetEntry, Disclosure,
    in_scope, scope, project_knowledge, project_reader, project_world,
    dramatic_ironies, sternberg_curiosity,
)


# ============================================================================
# Helpers used by multiple tests
# ============================================================================

def p(predicate, *args) -> Prop:
    return Prop(predicate=predicate, args=tuple(args))

def held(prop: Prop, slot: Slot = Slot.KNOWN,
         conf: Confidence = Confidence.CERTAIN,
         via: str = Diegetic.OBSERVATION.value) -> Held:
    return Held(prop=prop, slot=slot, confidence=conf, via=via, provenance=())

def ev(id: str, τ_s: int, τ_a: int,
       effects=(), branches=frozenset({CANONICAL_LABEL})) -> Event:
    return Event(
        id=id, type="test", τ_s=τ_s, τ_a=τ_a,
        participants={}, effects=tuple(effects),
        branches=branches,
    )


# ============================================================================
# Branch invariants (sketch 04 B1 + parent defaults)
# ============================================================================

def test_canonical_must_not_have_parent():
    try:
        Branch(label=":canonical-x", kind=BranchKind.CANONICAL, parent=":other")
    except ValueError:
        return
    raise AssertionError("canonical with parent should have raised")


def test_contested_defaults_parent_to_canonical():
    b = Branch(label=":b-alt", kind=BranchKind.CONTESTED)
    assert b.parent == CANONICAL_LABEL, f"got parent={b.parent!r}"


def test_contested_explicit_parent_preserved():
    """A nested contest (contested branch parented to another contested
    branch) is representable. Rare, but the parent default must not
    clobber an explicit value."""
    b = Branch(label=":b-nested", kind=BranchKind.CONTESTED, parent=":b-outer")
    assert b.parent == ":b-outer", f"got parent={b.parent!r}"


def test_draft_requires_explicit_parent():
    try:
        Branch(label=":draft-x", kind=BranchKind.DRAFT)
    except ValueError:
        return
    raise AssertionError("draft without parent should have raised")


def test_counterfactual_requires_explicit_parent():
    try:
        Branch(label=":cf-x", kind=BranchKind.COUNTERFACTUAL)
    except ValueError:
        return
    raise AssertionError("counterfactual without parent should have raised")


# ============================================================================
# Fold-scope rule (sketch 04 fold-scope across branches)
# ============================================================================

def test_canonical_event_in_scope_on_canonical():
    e = ev("e1", τ_s=0, τ_a=1)
    assert in_scope(e, CANONICAL, {CANONICAL_LABEL: CANONICAL})


def test_canonical_event_in_scope_on_contested_child():
    """A :contested branch with canonical as parent sees canonical events
    via ancestor chain. This is the `:canonical`-is-universal rule."""
    contested = Branch(label=":b-a", kind=BranchKind.CONTESTED)
    all_b = {CANONICAL_LABEL: CANONICAL, ":b-a": contested}
    e = ev("e1", τ_s=0, τ_a=1, branches=frozenset({CANONICAL_LABEL}))
    assert in_scope(e, contested, all_b)


def test_contested_event_in_scope_on_own_branch():
    contested = Branch(label=":b-a", kind=BranchKind.CONTESTED)
    all_b = {CANONICAL_LABEL: CANONICAL, ":b-a": contested}
    e = ev("e1", τ_s=0, τ_a=1, branches=frozenset({":b-a"}))
    assert in_scope(e, contested, all_b)


def test_contested_event_not_in_scope_on_sibling():
    """Sibling :contested branches do not share events. The whole point
    of keeping branches separate is that each one represents a different
    interpretation; leaking would destroy that."""
    a = Branch(label=":b-a", kind=BranchKind.CONTESTED)
    b = Branch(label=":b-b", kind=BranchKind.CONTESTED)
    all_b = {CANONICAL_LABEL: CANONICAL, ":b-a": a, ":b-b": b}
    e = ev("e1", τ_s=0, τ_a=1, branches=frozenset({":b-a"}))
    assert not in_scope(e, b, all_b)


def test_event_on_multiple_branches_visible_from_all_of_them():
    """Events can carry multiple branch labels (trans-branch-canonical
    declarations). An event labeled with both sibling :contested branches
    is visible from each."""
    a = Branch(label=":b-a", kind=BranchKind.CONTESTED)
    b = Branch(label=":b-b", kind=BranchKind.CONTESTED)
    all_b = {CANONICAL_LABEL: CANONICAL, ":b-a": a, ":b-b": b}
    e = ev("e1", τ_s=0, τ_a=1, branches=frozenset({":b-a", ":b-b"}))
    assert in_scope(e, a, all_b)
    assert in_scope(e, b, all_b)


# ============================================================================
# Fold determinism — (τ_s, τ_a) tiebreaker
# ============================================================================

def test_same_τ_s_resolved_by_τ_a_regardless_of_input_order():
    """Two events at the same story-time that both touch `P` for agent A:
    the later-τ_a event wins, no matter how the caller ordered the list.

    This is the regression test for the sort-key fix. Before the fix,
    fold result depended on Python list order."""
    prop = p("X", "A")

    e_earlier = Event(
        id="e_earlier", type="test", τ_s=10, τ_a=1,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop, slot=Slot.BELIEVED)),
        ),
    )
    e_later = Event(
        id="e_later", type="test", τ_s=10, τ_a=2,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop, slot=Slot.KNOWN)),
        ),
    )

    all_b = {CANONICAL_LABEL: CANONICAL}

    for events_in_some_order in ([e_earlier, e_later], [e_later, e_earlier]):
        s = scope(CANONICAL, events_in_some_order, all_b)
        state = project_knowledge("A", s, up_to_τ_s=10)
        h = state.holds(prop)
        assert h is not None, "proposition should be held"
        assert h.slot == Slot.KNOWN, (
            f"later-τ_a effect should win; got slot={h.slot}"
        )


# ============================================================================
# Knowledge projection (K1)
# ============================================================================

def test_observation_produces_held():
    prop = p("X", "A")
    e = Event(
        id="e", type="test", τ_s=5, τ_a=1,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop)),
        ),
    )
    all_b = {CANONICAL_LABEL: CANONICAL}
    s = scope(CANONICAL, [e], all_b)
    state = project_knowledge("A", s, up_to_τ_s=10)
    assert state.holds(prop) is not None


def test_fold_respects_up_to_τ_s_cutoff():
    prop = p("X", "A")
    e = Event(
        id="e", type="test", τ_s=10, τ_a=1,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop)),
        ),
    )
    all_b = {CANONICAL_LABEL: CANONICAL}
    s = scope(CANONICAL, [e], all_b)
    state_before = project_knowledge("A", s, up_to_τ_s=9)
    state_at = project_knowledge("A", s, up_to_τ_s=10)
    assert state_before.holds(prop) is None, "event at τ_s=10 must not apply at τ_s=9"
    assert state_at.holds(prop) is not None, "event at τ_s=10 must apply at τ_s=10"


def test_remove_effect_deletes_proposition():
    """A remove-KnowledgeEffect deletes the proposition from the state.

    Convention flag: the current implementation only consults the `.prop`
    field of the Held bundled in a remove-effect; the slot/confidence/via/
    provenance on that Held are ignored. The effect carries a full Held
    for symmetry with the non-remove case, but that symmetry is thin.
    Worth revisiting when the event-vocabulary sketch lands."""
    prop = p("X", "A")
    e_add = Event(
        id="e_add", type="test", τ_s=1, τ_a=1,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop)),
        ),
    )
    e_del = Event(
        id="e_del", type="test", τ_s=2, τ_a=2,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop), remove=True),
        ),
    )
    all_b = {CANONICAL_LABEL: CANONICAL}
    s = scope(CANONICAL, [e_add, e_del], all_b)
    state = project_knowledge("A", s, up_to_τ_s=10)
    assert state.holds(prop) is None


def test_later_non_remove_effect_overwrites_earlier():
    prop = p("X", "A")
    e1 = Event(
        id="e1", type="test", τ_s=1, τ_a=1,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A",
                            held=held(prop, slot=Slot.BELIEVED)),
        ),
    )
    e2 = Event(
        id="e2", type="test", τ_s=2, τ_a=2,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop, slot=Slot.KNOWN)),
        ),
    )
    all_b = {CANONICAL_LABEL: CANONICAL}
    s = scope(CANONICAL, [e1, e2], all_b)
    state = project_knowledge("A", s, up_to_τ_s=10)
    h = state.holds(prop)
    assert h is not None and h.slot == Slot.KNOWN


def test_agent_scoping_keeps_other_agents_state_separate():
    prop = p("X", "A")
    e = Event(
        id="e", type="test", τ_s=1, τ_a=1,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop)),
        ),
    )
    all_b = {CANONICAL_LABEL: CANONICAL}
    s = scope(CANONICAL, [e], all_b)
    a_state = project_knowledge("A", s, up_to_τ_s=10)
    b_state = project_knowledge("B", s, up_to_τ_s=10)
    assert a_state.holds(prop) is not None
    assert b_state.holds(prop) is None


# ============================================================================
# Reader projection (K2) — validation and behavior
# ============================================================================

def _one_canonical_event_with_disclosure(prop: Prop):
    """Minimal two-piece fixture: an event on :canonical and a sjuzhet
    entry that discloses a proposition to the reader."""
    e = ev("e", τ_s=0, τ_a=1)
    entry = SjuzhetEntry(
        event_id="e", τ_d=0, focalizer_id=None,
        disclosures=(Disclosure(
            prop=prop, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
            via=Narrative.DISCLOSURE.value,
        ),),
    )
    return [e], [entry]


def test_project_reader_rejects_draft_branch():
    events, sjuzhet = _one_canonical_event_with_disclosure(p("X", "A"))
    draft = Branch(label=":draft-x", kind=BranchKind.DRAFT, parent=CANONICAL_LABEL)
    all_b = {CANONICAL_LABEL: CANONICAL, ":draft-x": draft}
    try:
        project_reader(sjuzhet, events, draft, all_b, up_to_τ_d=0)
    except ValueError:
        return
    raise AssertionError("project_reader should reject a :draft branch")


def test_project_reader_rejects_counterfactual_branch():
    events, sjuzhet = _one_canonical_event_with_disclosure(p("X", "A"))
    cf = Branch(label=":cf-x", kind=BranchKind.COUNTERFACTUAL, parent=CANONICAL_LABEL)
    all_b = {CANONICAL_LABEL: CANONICAL, ":cf-x": cf}
    try:
        project_reader(sjuzhet, events, cf, all_b, up_to_τ_d=0)
    except ValueError:
        return
    raise AssertionError("project_reader should reject a :counterfactual branch")


def test_project_reader_rejects_unknown_event_id():
    # sjuzhet references an event that isn't in the fabula at all.
    entry = SjuzhetEntry(event_id="ghost", τ_d=0, focalizer_id=None,
                         disclosures=())
    all_b = {CANONICAL_LABEL: CANONICAL}
    try:
        project_reader([entry], [], CANONICAL, all_b, up_to_τ_d=0)
    except ValueError:
        return
    raise AssertionError("unknown event id should raise")


def test_project_reader_rejects_event_on_draft_only_branch():
    """An event labeled only with a :draft branch cannot be narrated,
    even if referenced by sjuzhet."""
    draft = Branch(label=":draft-x", kind=BranchKind.DRAFT, parent=CANONICAL_LABEL)
    all_b = {CANONICAL_LABEL: CANONICAL, ":draft-x": draft}

    # Event only on the draft branch, not on :canonical.
    e = ev("e", τ_s=0, τ_a=1, branches=frozenset({":draft-x"}))
    entry = SjuzhetEntry(event_id="e", τ_d=0, focalizer_id=None,
                         disclosures=())
    try:
        project_reader([entry], [e], CANONICAL, all_b, up_to_τ_d=0)
    except ValueError:
        return
    raise AssertionError("draft-only narrated event should raise")


def test_disclosure_places_proposition_in_reader_state():
    prop = p("X", "A")
    events, sjuzhet = _one_canonical_event_with_disclosure(prop)
    all_b = {CANONICAL_LABEL: CANONICAL}
    reader = project_reader(sjuzhet, events, CANONICAL, all_b, up_to_τ_d=0)
    h = reader.holds(prop)
    assert h is not None and h.slot == Slot.KNOWN


def test_later_disclosure_overrides_earlier():
    prop = p("X", "A")
    e1 = ev("e1", τ_s=0, τ_a=1)
    e2 = ev("e2", τ_s=1, τ_a=2)
    sjuzhet = [
        SjuzhetEntry(event_id="e1", τ_d=0, focalizer_id=None, disclosures=(
            Disclosure(prop=prop, slot=Slot.BELIEVED, confidence=Confidence.BELIEVED,
                       via=Narrative.DISCLOSURE.value),
        )),
        SjuzhetEntry(event_id="e2", τ_d=1, focalizer_id=None, disclosures=(
            Disclosure(prop=prop, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                       via=Narrative.DISCLOSURE.value),
        )),
    ]
    all_b = {CANONICAL_LABEL: CANONICAL}
    reader = project_reader(sjuzhet, [e1, e2], CANONICAL, all_b, up_to_τ_d=5)
    h = reader.holds(prop)
    assert h is not None and h.slot == Slot.KNOWN


def test_focalization_alone_does_not_mutate_reader_state():
    """Focalization is metadata-only in this prototype. A sjuzhet entry
    that sets a focalizer but has no disclosures must not place any
    propositions in the reader's state, even if the focalizer's own
    state is richly populated.

    Convention flag: sketch 04 defines focalization as a *constraint*
    on reader access (propositions the focalizer lacks become reader
    gaps; misconstrued ones become reader-believed). The prototype
    does neither. When real focalization semantics land, this test
    will need to change — it is currently pinned to a deliberate
    weakening, not to a sketch commitment."""
    prop = p("X", "A")
    e = Event(
        id="e", type="test", τ_s=0, τ_a=1,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop)),
        ),
    )
    entry = SjuzhetEntry(event_id="e", τ_d=0, focalizer_id="A",
                         disclosures=())
    all_b = {CANONICAL_LABEL: CANONICAL}
    reader = project_reader([entry], [e], CANONICAL, all_b, up_to_τ_d=0)
    assert reader.holds(prop) is None, (
        "focalization must not leak the focalizer's state into the reader"
    )


# ============================================================================
# Queries: dramatic irony
# ============================================================================

def _reader_state_with(prop: Prop, slot: Slot = Slot.KNOWN) -> "KnowledgeState":
    """Construct a reader state holding one proposition, bypassing the
    sjuzhet. Used where a test is isolating the irony query."""
    from substrate import KnowledgeState
    return KnowledgeState(
        agent_id="reader",
        by_prop=(Held(prop=prop, slot=slot,
                      confidence=Confidence.CERTAIN,
                      via=Narrative.DISCLOSURE.value),),
    )


def test_reader_over_character_irony_fires_when_character_lacks():
    prop = p("X", "A")
    # A character exists but does not hold the proposition.
    events = []
    all_b = {CANONICAL_LABEL: CANONICAL}
    reader = _reader_state_with(prop)
    ironies = dramatic_ironies(
        agent_ids=["A"], reader_state=reader,
        all_events=events, branch=CANONICAL,
        all_branches=all_b, τ_s=0,
    )
    matching = [i for i in ironies if i.informed_id == "reader"
                and i.uninformed_id == "A" and i.prop == prop]
    assert len(matching) == 1


def test_reader_over_character_irony_does_not_fire_when_character_knows():
    prop = p("X", "A")
    e = Event(
        id="e", type="test", τ_s=0, τ_a=1,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop)),
        ),
    )
    all_b = {CANONICAL_LABEL: CANONICAL}
    reader = _reader_state_with(prop)
    ironies = dramatic_ironies(
        agent_ids=["A"], reader_state=reader,
        all_events=[e], branch=CANONICAL,
        all_branches=all_b, τ_s=5,
    )
    matching = [i for i in ironies if i.informed_id == "reader"
                and i.uninformed_id == "A" and i.prop == prop]
    assert matching == [], (
        "no reader-over-character irony should fire when character also knows"
    )


def test_character_over_character_irony_fires_with_reader_aware():
    """A knows what B doesn't; reader is aware of the asymmetry."""
    prop = p("X", "subject")
    e = Event(
        id="e", type="test", τ_s=0, τ_a=1,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop)),
        ),
    )
    all_b = {CANONICAL_LABEL: CANONICAL}
    reader = _reader_state_with(prop)
    ironies = dramatic_ironies(
        agent_ids=["A", "B"], reader_state=reader,
        all_events=[e], branch=CANONICAL,
        all_branches=all_b, τ_s=5,
    )
    matching = [i for i in ironies if i.informed_id == "A"
                and i.uninformed_id == "B" and i.prop == prop]
    assert len(matching) == 1


def test_character_over_character_irony_does_not_fire_without_reader_aware():
    """If the reader doesn't hold the proposition, there's no cross-character
    irony to report. The reader being aware of the asymmetry is constitutive."""
    prop = p("X", "subject")
    e = Event(
        id="e", type="test", τ_s=0, τ_a=1,
        participants={}, effects=(
            KnowledgeEffect(agent_id="A", held=held(prop)),
        ),
    )
    all_b = {CANONICAL_LABEL: CANONICAL}
    from substrate import KnowledgeState
    empty_reader = KnowledgeState(agent_id="reader", by_prop=())
    ironies = dramatic_ironies(
        agent_ids=["A", "B"], reader_state=empty_reader,
        all_events=[e], branch=CANONICAL,
        all_branches=all_b, τ_s=5,
    )
    cross = [i for i in ironies if i.informed_id != "reader"]
    assert cross == []


# ============================================================================
# Oedipus integration — the payoff, pinned
# ============================================================================

def test_oedipus_τ_d_0_reader_outruns_oedipus_on_central_props():
    """The opening of the play: the reader knows the myth; Oedipus
    does not. Core Reader > Oedipus ironies on the three central
    propositions he lacks must fire."""
    from oedipus import FABULA, SJUZHET, child_of, killed
    all_b = {CANONICAL_LABEL: CANONICAL}

    reader = project_reader(SJUZHET, FABULA, CANONICAL, all_b, up_to_τ_d=0)
    ironies = dramatic_ironies(
        agent_ids=["oedipus", "jocasta"],
        reader_state=reader,
        all_events=FABULA, branch=CANONICAL,
        all_branches=all_b, τ_s=-46,  # just after the marriage, pre-play
    )
    props_reader_ahead_of_oedipus = {
        i.prop for i in ironies
        if i.informed_id == "reader" and i.uninformed_id == "oedipus"
    }
    for expected in [
        child_of("oedipus", "laius"),
        child_of("oedipus", "jocasta"),
        killed("oedipus", "laius"),
    ]:
        assert expected in props_reader_ahead_of_oedipus, f"missing irony on {expected}"


def test_jocasta_anagnorisis_collapses_reader_jocasta_killed_irony():
    """At τ_s=9 Jocasta realizes Oedipus killed Laius. The Reader >
    Jocasta irony on that proposition, live before, must disappear."""
    from oedipus import FABULA, SJUZHET, killed
    all_b = {CANONICAL_LABEL: CANONICAL}
    reader = project_reader(SJUZHET, FABULA, CANONICAL, all_b, up_to_τ_d=9)

    before = dramatic_ironies(
        agent_ids=["oedipus", "jocasta"], reader_state=reader,
        all_events=FABULA, branch=CANONICAL,
        all_branches=all_b, τ_s=8,
    )
    after = dramatic_ironies(
        agent_ids=["oedipus", "jocasta"], reader_state=reader,
        all_events=FABULA, branch=CANONICAL,
        all_branches=all_b, τ_s=9,
    )
    target = killed("oedipus", "laius")
    was_live_before = any(i.informed_id == "reader"
                          and i.uninformed_id == "jocasta"
                          and i.prop == target for i in before)
    assert was_live_before, "Reader > Jocasta irony on killed() should be live at τ_s=8"
    still_live_after = any(i.informed_id == "reader"
                           and i.uninformed_id == "jocasta"
                           and i.prop == target for i in after)
    assert not still_live_after, (
        "Reader > Jocasta irony on killed() should collapse after her "
        "anagnorisis at τ_s=9"
    )


def test_oedipus_anagnorisis_collapses_all_central_ironies():
    """At τ_s=13 every central-proposition irony must be cleared."""
    from oedipus import FABULA, SJUZHET, child_of, killed, married
    all_b = {CANONICAL_LABEL: CANONICAL}
    reader = project_reader(SJUZHET, FABULA, CANONICAL, all_b, up_to_τ_d=13)
    ironies = dramatic_ironies(
        agent_ids=["oedipus", "jocasta"], reader_state=reader,
        all_events=FABULA, branch=CANONICAL,
        all_branches=all_b, τ_s=13,
    )
    central = {
        killed("oedipus", "laius"),
        child_of("oedipus", "laius"),
        child_of("oedipus", "jocasta"),
        married("oedipus", "jocasta"),
    }
    leftover = [i for i in ironies if i.prop in central]
    assert leftover == [], (
        f"expected no central-prop ironies post-anagnorisis; got {leftover}"
    )


# ============================================================================
# Runner
# ============================================================================

TESTS = [
    # Branch invariants
    test_canonical_must_not_have_parent,
    test_contested_defaults_parent_to_canonical,
    test_contested_explicit_parent_preserved,
    test_draft_requires_explicit_parent,
    test_counterfactual_requires_explicit_parent,
    # Fold-scope rule
    test_canonical_event_in_scope_on_canonical,
    test_canonical_event_in_scope_on_contested_child,
    test_contested_event_in_scope_on_own_branch,
    test_contested_event_not_in_scope_on_sibling,
    test_event_on_multiple_branches_visible_from_all_of_them,
    # Fold determinism
    test_same_τ_s_resolved_by_τ_a_regardless_of_input_order,
    # Knowledge projection
    test_observation_produces_held,
    test_fold_respects_up_to_τ_s_cutoff,
    test_remove_effect_deletes_proposition,
    test_later_non_remove_effect_overwrites_earlier,
    test_agent_scoping_keeps_other_agents_state_separate,
    # Reader projection
    test_project_reader_rejects_draft_branch,
    test_project_reader_rejects_counterfactual_branch,
    test_project_reader_rejects_unknown_event_id,
    test_project_reader_rejects_event_on_draft_only_branch,
    test_disclosure_places_proposition_in_reader_state,
    test_later_disclosure_overrides_earlier,
    test_focalization_alone_does_not_mutate_reader_state,
    # Queries
    test_reader_over_character_irony_fires_when_character_lacks,
    test_reader_over_character_irony_does_not_fire_when_character_knows,
    test_character_over_character_irony_fires_with_reader_aware,
    test_character_over_character_irony_does_not_fire_without_reader_aware,
    # Oedipus integration
    test_oedipus_τ_d_0_reader_outruns_oedipus_on_central_props,
    test_jocasta_anagnorisis_collapses_reader_jocasta_killed_irony,
    test_oedipus_anagnorisis_collapses_all_central_ironies,
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
