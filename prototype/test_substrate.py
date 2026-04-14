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
from typing import Optional

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


# The test-helper convention: a reasonable default Confidence for each Slot.
#
# This is NOT a substrate invariant. The substrate's Held record does not
# enforce any relationship between slot and confidence; see the explicit
# test_held_accepts_incoherent_slot_confidence_pairs below.
#
# The helper applies this default only so that the *common* test case — "I
# want a Held with slot=X, reasonable confidence" — does not silently pass
# slot=BELIEVED, confidence=CERTAIN into the suite and hide the looseness.
_DEFAULT_CONFIDENCE_BY_SLOT = {
    Slot.KNOWN:     Confidence.CERTAIN,
    Slot.BELIEVED:  Confidence.BELIEVED,
    Slot.SUSPECTED: Confidence.SUSPECTED,
    Slot.GAP:       Confidence.OPEN,
}


def held(prop: Prop, slot: Slot = Slot.KNOWN,
         conf: Optional[Confidence] = None,
         via: str = Diegetic.OBSERVATION.value) -> Held:
    """Build a Held with a coherent slot/confidence pair by default. Pass
    `conf` explicitly to construct an incoherent pair deliberately."""
    if conf is None:
        conf = _DEFAULT_CONFIDENCE_BY_SLOT[slot]
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
# Held record — looseness is pinned explicitly
# ============================================================================

def test_held_accepts_incoherent_slot_confidence_pairs():
    """The substrate's Held record does not enforce a relationship between
    Slot and Confidence. Calling code can build Held(slot=BELIEVED,
    confidence=CERTAIN) or any other combination; nothing raises.

    This is a known design gap. Slot and Confidence currently cover
    overlapping territory (KNOWN/CERTAIN, BELIEVED/BELIEVED, etc.) and
    it is not yet settled whether they should be independent axes or
    collapsed into one. This test pins the current looseness so later
    cleanup has an explicit target and the suite does not silently
    normalize around the ambiguity via helper defaults."""
    h = Held(
        prop=p("X", "A"),
        slot=Slot.BELIEVED,
        confidence=Confidence.CERTAIN,  # deliberately inconsistent with slot
        via=Diegetic.OBSERVATION.value,
    )
    # Construction does not raise. That is the current behavior.
    assert h.slot == Slot.BELIEVED
    assert h.confidence == Confidence.CERTAIN


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


def test_project_reader_rejects_event_on_other_contested_branch_when_reader_is_canonical():
    """Reader on :canonical, sjuzhet narrates an event on :b-a (a
    :contested branch). The event is on a shipped branch, so the
    shipped-branch check alone would pass — but the event is not in
    fold-scope for :canonical (canonical does not inherit from children),
    so the in_scope check must catch it."""
    b_a = Branch(label=":b-a", kind=BranchKind.CONTESTED, parent=CANONICAL_LABEL)
    all_b = {CANONICAL_LABEL: CANONICAL, ":b-a": b_a}
    e = ev("e", τ_s=0, τ_a=1, branches=frozenset({":b-a"}))
    entry = SjuzhetEntry(event_id="e", τ_d=0, focalizer_id=None,
                         disclosures=())
    try:
        project_reader([entry], [e], CANONICAL, all_b, up_to_τ_d=0)
    except ValueError:
        return
    raise AssertionError(
        "event on a sibling :contested branch should be out of scope "
        "when reader is on :canonical"
    )


def test_project_reader_rejects_event_on_sibling_contested_branch():
    """Reader on :b-b (a :contested branch), sjuzhet narrates an event
    on :b-a (a sibling :contested branch). Both are shipped kinds, but
    sibling contested branches do not inherit from each other, so the
    event is out of scope for :b-b and must be rejected."""
    b_a = Branch(label=":b-a", kind=BranchKind.CONTESTED, parent=CANONICAL_LABEL)
    b_b = Branch(label=":b-b", kind=BranchKind.CONTESTED, parent=CANONICAL_LABEL)
    all_b = {CANONICAL_LABEL: CANONICAL, ":b-a": b_a, ":b-b": b_b}
    e = ev("e", τ_s=0, τ_a=1, branches=frozenset({":b-a"}))
    entry = SjuzhetEntry(event_id="e", τ_d=0, focalizer_id=None,
                         disclosures=())
    try:
        project_reader([entry], [e], b_b, all_b, up_to_τ_d=0)
    except ValueError:
        return
    raise AssertionError(
        "event on a sibling :contested branch should be out of scope "
        "when reader is on a different :contested branch"
    )


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
    """A sjuzhet entry that sets a focalizer but has no disclosures
    must not place any propositions in the reader's state, even if
    the focalizer's own state is richly populated.

    Per focalization-sketch-01 F1, focalization constrains the slot
    of *disclosures* in the entry. It does not invent disclosures
    from the focalizer's state. This test pins the negative half of
    that invariant: no disclosures, no state changes, regardless of
    what the focalizer knows."""
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
# Focalization — F1-F5 per focalization-sketch-01
# ============================================================================
#
# F1: disclosure slot is min(author_slot, focalizer_slot) under
#     KNOWN > BELIEVED > SUSPECTED > GAP; focalizer-absent → GAP.
# F2: focalization-driven demotion does not override stronger prior
#     reader state; explicit author demotion still does.
# F3: focalizer's reference state is at the narrated event's τ_s.
# F4: focalizer_id=None passes through unchanged (existing tests).
# F5: focalizer's holds() is substitution-aware.


def _two_branch_map():
    return {CANONICAL_LABEL: CANONICAL}


def test_f1_passes_through_when_focalizer_holds_at_author_slot():
    """F1: if the focalizer holds the proposition at the author's slot
    or stronger, the disclosure lands at the author's slot (no demotion)."""
    prop = p("P", "x")
    e = ev("e1", τ_s=0, τ_a=1, effects=(
        KnowledgeEffect(agent_id="A", held=held(prop, slot=Slot.KNOWN)),
    ))
    entry = SjuzhetEntry(
        event_id="e1", τ_d=0, focalizer_id="A",
        disclosures=(Disclosure(
            prop=prop, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
            via=Narrative.DISCLOSURE.value,
        ),),
    )
    reader = project_reader([entry], [e], CANONICAL, _two_branch_map(),
                            up_to_τ_d=0)
    r = reader.holds(prop)
    assert r is not None and r.slot == Slot.KNOWN


def test_f1_demotes_known_disclosure_to_believed_when_focalizer_believes():
    """F1: min(author=KNOWN, focalizer=BELIEVED) = BELIEVED.
    Reader receives the disclosure at BELIEVED."""
    prop = p("P", "x")
    e = ev("e1", τ_s=0, τ_a=1, effects=(
        KnowledgeEffect(agent_id="A",
                        held=held(prop, slot=Slot.BELIEVED)),
    ))
    entry = SjuzhetEntry(
        event_id="e1", τ_d=0, focalizer_id="A",
        disclosures=(Disclosure(
            prop=prop, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
            via=Narrative.DISCLOSURE.value,
        ),),
    )
    reader = project_reader([entry], [e], CANONICAL, _two_branch_map(),
                            up_to_τ_d=0)
    r = reader.holds(prop)
    assert r is not None and r.slot == Slot.BELIEVED, \
        f"expected BELIEVED under F1 demotion; got {r.slot if r else None}"


def test_f1_demotes_to_gap_when_focalizer_does_not_hold_prop():
    """F1: the focalizer-absent case. If the focalizer does not hold
    the disclosed proposition, the disclosure lands at GAP in the
    reader's state."""
    disclosed = p("P", "x")
    unrelated = p("Q", "y")
    # Focalizer holds something else entirely; does not hold `disclosed`.
    e = ev("e1", τ_s=0, τ_a=1, effects=(
        KnowledgeEffect(agent_id="A", held=held(unrelated)),
    ))
    entry = SjuzhetEntry(
        event_id="e1", τ_d=0, focalizer_id="A",
        disclosures=(Disclosure(
            prop=disclosed, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
            via=Narrative.DISCLOSURE.value,
        ),),
    )
    reader = project_reader([entry], [e], CANONICAL, _two_branch_map(),
                            up_to_τ_d=0)
    r = reader.holds(disclosed)
    assert r is not None and r.slot == Slot.GAP, \
        f"expected focalizer-absent to demote to GAP; got " \
        f"{r.slot if r else None}"


def test_f1_author_weaker_than_focalizer_passes_through_at_author_slot():
    """F1: min(author=SUSPECTED, focalizer=KNOWN) = SUSPECTED. The
    focalizer's stronger state does not upgrade the author's choice."""
    prop = p("P", "x")
    e = ev("e1", τ_s=0, τ_a=1, effects=(
        KnowledgeEffect(agent_id="A", held=held(prop, slot=Slot.KNOWN)),
    ))
    entry = SjuzhetEntry(
        event_id="e1", τ_d=0, focalizer_id="A",
        disclosures=(Disclosure(
            prop=prop, slot=Slot.SUSPECTED, confidence=Confidence.SUSPECTED,
            via=Narrative.DISCLOSURE.value,
        ),),
    )
    reader = project_reader([entry], [e], CANONICAL, _two_branch_map(),
                            up_to_τ_d=0)
    r = reader.holds(prop)
    assert r is not None and r.slot == Slot.SUSPECTED


def test_f2_focalization_demotion_does_not_override_stronger_prior_state():
    """F2: the reader already holds P as KNOWN from an earlier
    omniscient entry. A later focalized entry attempts to disclose P
    at KNOWN, but the focalizer doesn't hold P — F1 demotes to GAP.
    The F2 guard fires: the reader's KNOWN persists."""
    prop = p("P", "x")
    unrelated = p("Q", "y")
    # e1: the event the omniscient entry narrates. No relevant effects.
    e1 = ev("e1", τ_s=0, τ_a=1, effects=())
    # e2: focalizer A holds only an unrelated prop; does NOT hold P.
    e2 = ev("e2", τ_s=1, τ_a=2, effects=(
        KnowledgeEffect(agent_id="A", held=held(unrelated)),
    ))
    entries = [
        SjuzhetEntry(
            event_id="e1", τ_d=0, focalizer_id=None,
            disclosures=(Disclosure(
                prop=prop, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                via=Narrative.DISCLOSURE.value,
            ),),
        ),
        SjuzhetEntry(
            event_id="e2", τ_d=1, focalizer_id="A",
            disclosures=(Disclosure(
                prop=prop, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                via=Narrative.DISCLOSURE.value,
            ),),
        ),
    ]
    reader = project_reader(entries, [e1, e2], CANONICAL, _two_branch_map(),
                            up_to_τ_d=10)
    r = reader.holds(prop)
    assert r is not None and r.slot == Slot.KNOWN, (
        f"F2 guard failed: reader state was demoted from KNOWN to "
        f"{r.slot if r else None} by a later focalization-driven demotion"
    )


def test_f2_explicit_author_demotion_via_omniscient_still_overrides():
    """F2 is scoped to focalization-driven demotion. An explicit
    author demotion — a later omniscient disclosure at a weaker slot —
    still overrides prior stronger state per the existing later-wins
    convention. Retroactive reframing (unreliable narrator, etc.)
    must continue to work."""
    prop = p("P", "x")
    e1 = ev("e1", τ_s=0, τ_a=1, effects=())
    e2 = ev("e2", τ_s=1, τ_a=2, effects=())
    entries = [
        SjuzhetEntry(
            event_id="e1", τ_d=0, focalizer_id=None,
            disclosures=(Disclosure(
                prop=prop, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                via=Narrative.DISCLOSURE.value,
            ),),
        ),
        SjuzhetEntry(
            event_id="e2", τ_d=1, focalizer_id=None,
            disclosures=(Disclosure(
                prop=prop, slot=Slot.BELIEVED,
                confidence=Confidence.BELIEVED,
                via=Narrative.RETROACTIVE_REFRAMING.value,
            ),),
        ),
    ]
    reader = project_reader(entries, [e1, e2], CANONICAL, _two_branch_map(),
                            up_to_τ_d=10)
    r = reader.holds(prop)
    assert r is not None and r.slot == Slot.BELIEVED, (
        f"explicit author demotion was not applied; reader slot "
        f"{r.slot if r else None} (expected BELIEVED)"
    )


def test_f2_focalization_equal_to_prior_is_a_no_op_write():
    """F2 edge: focalization-demoted effective_slot equals prior
    reader state's slot. The guard fires (>= check) and the write
    is skipped. Reader state is unchanged (same slot, but provenance
    reflects the earlier entry)."""
    prop = p("P", "x")
    e1 = ev("e1", τ_s=0, τ_a=1, effects=())
    e2 = ev("e2", τ_s=1, τ_a=2, effects=(
        KnowledgeEffect(agent_id="A", held=held(prop, slot=Slot.BELIEVED)),
    ))
    entries = [
        # Reader first gets BELIEVED from omniscient.
        SjuzhetEntry(
            event_id="e1", τ_d=0, focalizer_id=None,
            disclosures=(Disclosure(
                prop=prop, slot=Slot.BELIEVED,
                confidence=Confidence.BELIEVED,
                via=Narrative.DISCLOSURE.value,
            ),),
        ),
        # Later focalized entry: author says KNOWN but focalizer holds
        # BELIEVED; F1 demotes to BELIEVED. effective == prior → skip.
        SjuzhetEntry(
            event_id="e2", τ_d=1, focalizer_id="A",
            disclosures=(Disclosure(
                prop=prop, slot=Slot.KNOWN, confidence=Confidence.CERTAIN,
                via=Narrative.DISCLOSURE.value,
            ),),
        ),
    ]
    reader = project_reader(entries, [e1, e2], CANONICAL, _two_branch_map(),
                            up_to_τ_d=10)
    r = reader.holds(prop)
    assert r is not None and r.slot == Slot.BELIEVED


def test_f3_focalizer_reference_τ_s_includes_the_narrated_event():
    """F3: focalizer's reference state is at the narrated event's
    τ_s. The event's own effects on the focalizer are therefore
    visible — a participant (e.g., a killer) sees the event's own
    effects in their state at the reference τ_s."""
    killed_p = p("killed", "A", "B")
    # e: A observes their own act at τ_s=5. If focalizer's reference
    # τ_s excluded the event's effects, the observation wouldn't be
    # in scope, and F1 would demote the disclosure to GAP.
    e = ev("e", τ_s=5, τ_a=1, effects=(
        WorldEffect(prop=killed_p),
        KnowledgeEffect(agent_id="A", held=held(killed_p, slot=Slot.KNOWN)),
    ))
    entry = SjuzhetEntry(
        event_id="e", τ_d=0, focalizer_id="A",
        disclosures=(Disclosure(
            prop=killed_p, slot=Slot.KNOWN,
            confidence=Confidence.CERTAIN,
            via=Narrative.DISCLOSURE.value,
        ),),
    )
    reader = project_reader([entry], [e], CANONICAL, _two_branch_map(),
                            up_to_τ_d=0)
    r = reader.holds(killed_p)
    assert r is not None and r.slot == Slot.KNOWN, (
        f"F3: focalizer's state at the event's τ_s should include "
        f"the event's own effects; got slot="
        f"{r.slot if r else 'not-held'}"
    )


def test_f5_focalizer_access_is_substitution_aware():
    """F5: focalizer's holds() is substitution-aware. If the focalizer
    holds an identity at KNOWN and a proposition under the identified
    entity, substitution gives them access — and the disclosure passes
    through at the author's slot without F1 demotion."""
    from substrate import IDENTITY_PREDICATE
    # Focalizer holds P(a) and identity(a, b) — substitution gives P(b).
    e = ev("e", τ_s=0, τ_a=1, effects=(
        KnowledgeEffect(agent_id="A",
                        held=held(p("P", "a"), slot=Slot.KNOWN)),
        KnowledgeEffect(
            agent_id="A",
            held=held(Prop(IDENTITY_PREDICATE, ("a", "b")),
                      slot=Slot.KNOWN),
        ),
    ))
    # Author discloses P(b) — which A holds only via substitution.
    entry = SjuzhetEntry(
        event_id="e", τ_d=0, focalizer_id="A",
        disclosures=(Disclosure(
            prop=p("P", "b"), slot=Slot.KNOWN,
            confidence=Confidence.CERTAIN,
            via=Narrative.DISCLOSURE.value,
        ),),
    )
    reader = project_reader([entry], [e], CANONICAL, _two_branch_map(),
                            up_to_τ_d=0)
    r = reader.holds(p("P", "b"))
    assert r is not None and r.slot == Slot.KNOWN, (
        f"F5: substitution-aware focalizer access failed — "
        f"reader slot={r.slot if r else 'not-held'}"
    )


def test_f5_suspected_identity_does_not_give_focalizer_access():
    """F5 corollary: per identity-sketch I7, substitution fires only
    on KNOWN identities. An identity held SUSPECTED by the focalizer
    does NOT extend their focalization-access, so F1 demotes to GAP."""
    from substrate import IDENTITY_PREDICATE
    e = ev("e", τ_s=0, τ_a=1, effects=(
        KnowledgeEffect(agent_id="A",
                        held=held(p("P", "a"), slot=Slot.KNOWN)),
        KnowledgeEffect(
            agent_id="A",
            held=held(Prop(IDENTITY_PREDICATE, ("a", "b")),
                      slot=Slot.SUSPECTED),
        ),
    ))
    entry = SjuzhetEntry(
        event_id="e", τ_d=0, focalizer_id="A",
        disclosures=(Disclosure(
            prop=p("P", "b"), slot=Slot.KNOWN,
            confidence=Confidence.CERTAIN,
            via=Narrative.DISCLOSURE.value,
        ),),
    )
    reader = project_reader([entry], [e], CANONICAL, _two_branch_map(),
                            up_to_τ_d=0)
    r = reader.holds(p("P", "b"))
    # Focalizer does not hold P(b) literally (only via SUSPECTED
    # identity, which I7 excludes). F1 demotes to GAP.
    assert r is not None and r.slot == Slot.GAP


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


def test_oedipus_does_not_query_know_parentage_before_anagnorisis():
    """Temporal contract: Oedipus's realization of his parentage lands
    at E_oedipus_anagnorisis (τ_s=13), not at E_shepherd_testimony
    (τ_s=12). At τ_s=12 the shepherd gives him parentage FACTS about
    the-exposed-baby, but the identity assertion (oedipus =
    the-exposed-baby) is Oedipus's own realization — the shepherd
    does not assert it. So substitution-aware holds must still
    return None for child_of(oedipus, laius) at τ_s=12."""
    from oedipus import FABULA, child_of
    all_b = {CANONICAL_LABEL: CANONICAL}
    scoped = scope(CANONICAL, FABULA, all_b)
    pre = project_knowledge("oedipus", scoped, 12)
    post = project_knowledge("oedipus", scoped, 13)
    assert pre.holds(child_of("oedipus", "laius")) is None, (
        "Oedipus query-knows child_of(oedipus, laius) at τ_s=12 — "
        "the anagnorisis payoff is landing a beat early"
    )
    assert pre.holds(child_of("oedipus", "jocasta")) is None, (
        "Oedipus query-knows child_of(oedipus, jocasta) at τ_s=12 — "
        "the anagnorisis payoff is landing a beat early"
    )
    # After the anagnorisis, both derive via substitution.
    assert post.holds(child_of("oedipus", "laius")) is not None
    assert post.holds(child_of("oedipus", "jocasta")) is not None


def test_shepherd_and_messenger_do_not_hold_oedipus_identity_at_exposure():
    """Temporal contract: identity(oedipus, the-exposed-baby) is not
    lodged into the shepherd's or messenger's state at τ_s=-99. At
    that story-time 'Oedipus' is not yet a named referent — the baby
    has just been delivered; the naming and upbringing are decades
    later. The shepherd never holds the identity in this encoding;
    the messenger learns it at E_upbringing_in_corinth (τ_s=-50)."""
    from oedipus import FABULA
    from substrate import IDENTITY_PREDICATE
    all_b = {CANONICAL_LABEL: CANONICAL}
    scoped = scope(CANONICAL, FABULA, all_b)

    def has_identity(agent_id: str, τ_s: int) -> bool:
        state = project_knowledge(agent_id, scoped, τ_s)
        target = Prop(IDENTITY_PREDICATE, ("oedipus", "the-exposed-baby"))
        return state.holds_literal(target) is not None

    # At τ_s=-99 (exposure), neither agent holds the identity literally.
    assert not has_identity("shepherd", -99), (
        "shepherd holds identity(oedipus, the-exposed-baby) at τ_s=-99 — "
        "smuggles later knowledge backward into earlier state"
    )
    assert not has_identity("messenger", -99), (
        "messenger holds identity(oedipus, the-exposed-baby) at τ_s=-99 — "
        "Oedipus is not yet named at this story-time"
    )
    # At τ_s=-50 (upbringing), the messenger forms the identity. The
    # shepherd still does not hold it (he is isolated in the countryside
    # and never learns the adopted name in this encoding).
    assert has_identity("messenger", -50), (
        "messenger should hold the identity by τ_s=-50, when Oedipus is "
        "named at Polybus's court"
    )
    assert not has_identity("shepherd", 13), (
        "shepherd should never hold identity(oedipus, the-exposed-baby) "
        "in this encoding; the combinatorial insight is Oedipus's"
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
    # Held record looseness
    test_held_accepts_incoherent_slot_confidence_pairs,
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
    test_project_reader_rejects_event_on_other_contested_branch_when_reader_is_canonical,
    test_project_reader_rejects_event_on_sibling_contested_branch,
    test_disclosure_places_proposition_in_reader_state,
    test_later_disclosure_overrides_earlier,
    test_focalization_alone_does_not_mutate_reader_state,
    # Queries
    test_reader_over_character_irony_fires_when_character_lacks,
    test_reader_over_character_irony_does_not_fire_when_character_knows,
    test_character_over_character_irony_fires_with_reader_aware,
    test_character_over_character_irony_does_not_fire_without_reader_aware,
    # Focalization (focalization-sketch-01 F1-F5)
    test_f1_passes_through_when_focalizer_holds_at_author_slot,
    test_f1_demotes_known_disclosure_to_believed_when_focalizer_believes,
    test_f1_demotes_to_gap_when_focalizer_does_not_hold_prop,
    test_f1_author_weaker_than_focalizer_passes_through_at_author_slot,
    test_f2_focalization_demotion_does_not_override_stronger_prior_state,
    test_f2_explicit_author_demotion_via_omniscient_still_overrides,
    test_f2_focalization_equal_to_prior_is_a_no_op_write,
    test_f3_focalizer_reference_τ_s_includes_the_narrated_event,
    test_f5_focalizer_access_is_substitution_aware,
    test_f5_suspected_identity_does_not_give_focalizer_access,
    # Oedipus integration
    test_oedipus_τ_d_0_reader_outruns_oedipus_on_central_props,
    test_jocasta_anagnorisis_collapses_reader_jocasta_killed_irony,
    test_oedipus_anagnorisis_collapses_all_central_ironies,
    test_oedipus_does_not_query_know_parentage_before_anagnorisis,
    test_shepherd_and_messenger_do_not_hold_oedipus_identity_at_exposure,
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
