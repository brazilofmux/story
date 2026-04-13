"""
test_rashomon.py — permanent tests over the Rashomon contested-branch
encoding.

These tests are story-specific: they import from `rashomon` and pin
properties of the substrate as exercised by that encoding. Substrate-
level invariants that can be pinned *without* a story live in
`test_substrate.py`. This file exists because some invariants only
become load-bearing once a non-trivial :contested example is folded
through the substrate, and a regression in those invariants would be
invisible without a concrete case.

Discipline matches test_substrate.py:

- Plain assertions, no framework, no dependencies.
- Each test's docstring flags whether it pins a sketch-04 commitment
  or a narrower encoding choice.

Run:
    python3 test_rashomon.py
"""

from __future__ import annotations

import sys
import traceback

from substrate import (
    Slot,
    scope, project_knowledge, project_reader, project_world,
    dramatic_ironies,
)
from rashomon import (
    EVENTS_ALL, SJUZHET_BY_BRANCH, AGENT_IDS, ALL_BRANCHES,
    CONTESTED_BRANCHES,
    B_TAJOMARU, B_WIFE, B_HUSBAND, B_WOODCUTTER,
    killed, killed_with, coerced, yielded_willingly, duel_character,
    stole, had_intercourse_with, dead, body_found_by, begged_to_kill,
    bound_to, at_location,
)


# ============================================================================
# Sibling non-inheritance — the core :contested invariant
# ============================================================================

def test_stole_dagger_only_visible_on_woodcutter_branch():
    """Pins sketch-04 fold-scope rule: sibling :contested branches do
    not inherit from each other. stole(woodcutter, dagger) is authored
    only on :b-woodcutter. Every other branch's world projection must
    omit it."""
    prop = stole("woodcutter", "dagger")
    for b in CONTESTED_BRANCHES:
        scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
        world = project_world(scoped, 100)
        if b.label == B_WOODCUTTER.label:
            assert prop in world, \
                f"expected {prop} on {b.label}; world={world!r}"
        else:
            assert prop not in world, \
                f"{prop} leaked onto sibling branch {b.label}"


def test_each_branchs_killing_does_not_leak_to_siblings():
    """Each branch asserts its own killed(...) proposition; those
    claims must not appear on sibling branches. Pinned per branch to
    make regressions point at the offender."""
    expected = {
        B_TAJOMARU.label:   killed("tajomaru", "husband"),
        B_WIFE.label:       killed("wife",     "husband"),
        B_HUSBAND.label:    killed("husband",  "husband"),
        B_WOODCUTTER.label: killed("tajomaru", "husband"),
    }
    for b in CONTESTED_BRANCHES:
        scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
        world = project_world(scoped, 100)
        own = expected[b.label]
        assert own in world, f"{b.label} missing own claim {own}"
        for other_label, other_claim in expected.items():
            if other_label == b.label:
                continue
            # :b-tajomaru and :b-woodcutter happen to share the same
            # killed(tajomaru, husband) claim. That is a story-level
            # fact, not a leak; the check is only that *different*
            # claims do not cross.
            if other_claim == own:
                continue
            assert other_claim not in world, \
                f"{b.label} leaked {other_claim} from {other_label}"


def test_modality_of_intercourse_differs_by_branch():
    """Pins that branch-specific modality lives on the branch, not on
    canonical. Two branches assert coerced(tajomaru, wife); two assert
    yielded_willingly(wife, tajomaru); no branch asserts both."""
    coerced_on = set()
    willing_on = set()
    for b in CONTESTED_BRANCHES:
        scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
        world = project_world(scoped, 100)
        if coerced("tajomaru", "wife") in world:
            coerced_on.add(b.label)
        if yielded_willingly("wife", "tajomaru") in world:
            willing_on.add(b.label)
    assert coerced_on == {B_WIFE.label, B_WOODCUTTER.label}, \
        f"coerced_on={sorted(coerced_on)}"
    assert willing_on == {B_TAJOMARU.label, B_HUSBAND.label}, \
        f"willing_on={sorted(willing_on)}"
    assert coerced_on.isdisjoint(willing_on), \
        f"branch asserts both modalities: {coerced_on & willing_on}"


# ============================================================================
# Canonical-is-universal — the other half of the fold-scope rule
# ============================================================================

def test_canonical_intercourse_fact_visible_on_every_branch():
    """The bare fact had_intercourse_with(tajomaru, wife) is authored
    on :canonical. Every branch's fold must pick it up via the
    canonical-is-universal rule."""
    prop = had_intercourse_with("tajomaru", "wife")
    for b in CONTESTED_BRANCHES:
        scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
        world = project_world(scoped, 100)
        assert prop in world, f"canonical fact missing on {b.label}"


def test_canonical_outcome_dead_husband_visible_on_every_branch():
    """dead(husband) is the one outcome every account agrees on, and
    is authored canonically. It must fold in on every branch."""
    prop = dead("husband")
    for b in CONTESTED_BRANCHES:
        scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
        world = project_world(scoped, 100)
        assert prop in world, f"dead(husband) missing on {b.label}"


def test_canonical_binding_observations_reach_agents_on_every_branch():
    """The bind event's observation effects populate husband's and
    tajomaru's knowledge states. As canonical events, those observations
    must appear on every branch's per-agent fold — the canonical-is-
    universal rule applies to knowledge effects too, not only world
    effects."""
    prop = bound_to("husband", "tree")
    for b in CONTESTED_BRANCHES:
        scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
        husband_state = project_knowledge("husband", scoped, 4)
        held = husband_state.holds(prop)
        assert held is not None and held.slot == Slot.KNOWN, \
            f"bound_to not known to husband on {b.label} at τ_s=4"


# ============================================================================
# Per-branch reader projection
# ============================================================================

def test_reader_on_tajomaru_branch_knows_tajomaru_killed_husband():
    reader = project_reader(
        sjuzhet=SJUZHET_BY_BRANCH[B_TAJOMARU.label],
        all_events=EVENTS_ALL,
        branch=B_TAJOMARU,
        all_branches=ALL_BRANCHES,
        up_to_τ_d=100,
    )
    held = reader.holds(killed("tajomaru", "husband"))
    assert held is not None and held.slot == Slot.KNOWN


def test_reader_on_husband_branch_knows_husband_killed_himself():
    reader = project_reader(
        sjuzhet=SJUZHET_BY_BRANCH[B_HUSBAND.label],
        all_events=EVENTS_ALL,
        branch=B_HUSBAND,
        all_branches=ALL_BRANCHES,
        up_to_τ_d=100,
    )
    held = reader.holds(killed("husband", "husband"))
    assert held is not None and held.slot == Slot.KNOWN
    # And the reader on this branch does NOT hold killed(tajomaru, husband)
    # — the husband's account does not assign Tajomaru the killing.
    assert reader.holds(killed("tajomaru", "husband")) is None


def test_reader_on_woodcutter_branch_knows_theft():
    """stole(woodcutter, dagger) is a :b-woodcutter-exclusive fact.
    The reader on that branch picks it up via disclosure; the reader
    on any other branch does not, because the sjuzhet entry that
    discloses it does not belong to those branches' sjuzhets."""
    reader = project_reader(
        sjuzhet=SJUZHET_BY_BRANCH[B_WOODCUTTER.label],
        all_events=EVENTS_ALL,
        branch=B_WOODCUTTER,
        all_branches=ALL_BRANCHES,
        up_to_τ_d=100,
    )
    held = reader.holds(stole("woodcutter", "dagger"))
    assert held is not None and held.slot == Slot.KNOWN

    for b in (B_TAJOMARU, B_WIFE, B_HUSBAND):
        other_reader = project_reader(
            sjuzhet=SJUZHET_BY_BRANCH[b.label],
            all_events=EVENTS_ALL,
            branch=b,
            all_branches=ALL_BRANCHES,
            up_to_τ_d=100,
        )
        assert other_reader.holds(stole("woodcutter", "dagger")) is None, \
            f"theft leaked into reader on {b.label}"


def test_reader_on_every_branch_shares_the_canonical_preamble():
    """The preamble disclosures are the same on every branch sjuzhet
    (by construction). Pinning this means a regression that drops one
    branch's preamble would surface here."""
    shared = [
        at_location("husband", "forest_road"),
        at_location("wife",    "forest_road"),
        bound_to("husband", "tree"),
        had_intercourse_with("tajomaru", "wife"),
    ]
    for b in CONTESTED_BRANCHES:
        reader = project_reader(
            sjuzhet=SJUZHET_BY_BRANCH[b.label],
            all_events=EVENTS_ALL,
            branch=b,
            all_branches=ALL_BRANCHES,
            up_to_τ_d=100,
        )
        for prop in shared:
            held = reader.holds(prop)
            assert held is not None, \
                f"{prop} missing from reader on {b.label}"


# ============================================================================
# Sjuzhet validation — the substrate rejects mis-labeled entries
# ============================================================================

def test_project_reader_rejects_tajomaru_sjuzhet_projected_on_wife_branch():
    """Sketch-04 guarantee: project_reader validates that every sjuzhet
    entry's event is in fold-scope for the target branch. Projecting
    Tajomaru's sjuzhet on :b-wife references events labeled only on
    :b-tajomaru, which are out of scope for :b-wife — sibling
    contested. This must raise."""
    try:
        project_reader(
            sjuzhet=SJUZHET_BY_BRANCH[B_TAJOMARU.label],
            all_events=EVENTS_ALL,
            branch=B_WIFE,
            all_branches=ALL_BRANCHES,
            up_to_τ_d=100,
        )
    except ValueError:
        return
    raise AssertionError(
        "expected ValueError when projecting tajomaru sjuzhet on :b-wife"
    )


# ============================================================================
# Dramatic-irony queries — branch-aware
# ============================================================================

def test_dramatic_irony_results_differ_per_branch():
    """Sketch-04 commits to branch-aware queries: in contested regions,
    Sternberg and irony queries return branch-indexed results. This
    test pins that the totals differ — if a regression collapsed
    branch-awareness back to canonical-only, all four counts would be
    equal. (This is a necessary-not-sufficient check; a stronger one
    would compare the specific Irony records per branch, but that is
    brittle against encoding refinement.)"""
    counts = {}
    for b in CONTESTED_BRANCHES:
        reader = project_reader(
            sjuzhet=SJUZHET_BY_BRANCH[b.label],
            all_events=EVENTS_ALL,
            branch=b,
            all_branches=ALL_BRANCHES,
            up_to_τ_d=100,
        )
        ironies = dramatic_ironies(
            agent_ids=AGENT_IDS,
            reader_state=reader,
            all_events=EVENTS_ALL,
            branch=b,
            all_branches=ALL_BRANCHES,
            τ_s=100,
        )
        counts[b.label] = len(ironies)
    # Woodcutter's branch has extra disclosed facts (the theft, the
    # cowardly-duel character) beyond what other branches see, so its
    # total should be the largest. This pins a specific relation.
    assert counts[B_WOODCUTTER.label] > counts[B_WIFE.label], \
        f"expected :b-woodcutter ({counts[B_WOODCUTTER.label]}) > " \
        f":b-wife ({counts[B_WIFE.label]}); counts={counts}"
    # Not all four branches have identical counts.
    assert len(set(counts.values())) > 1, \
        f"branch-aware irony counts collapsed to single value: {counts}"


def test_reader_over_character_irony_on_contested_fact():
    """The reader on :b-wife knows killed(wife, husband) (from the
    disclosure). None of the in-story agents — not even the wife
    herself, within the :b-wife fabula — hold killed(wife, husband)
    as KNOWN, because we did not author an observation effect for it
    on any agent. An irony should fire."""
    reader = project_reader(
        sjuzhet=SJUZHET_BY_BRANCH[B_WIFE.label],
        all_events=EVENTS_ALL,
        branch=B_WIFE,
        all_branches=ALL_BRANCHES,
        up_to_τ_d=100,
    )
    ironies = dramatic_ironies(
        agent_ids=AGENT_IDS,
        reader_state=reader,
        all_events=EVENTS_ALL,
        branch=B_WIFE,
        all_branches=ALL_BRANCHES,
        τ_s=100,
    )
    target = killed("wife", "husband")
    hits = [i for i in ironies
            if i.informed_id == "reader" and i.prop == target]
    assert hits, f"expected reader > * irony on {target}, got none"


# ============================================================================
# Scope sanity — for every branch, event count is preamble + branch-only
# ============================================================================

def test_branch_scope_sizes_add_up():
    """Each branch sees exactly the canonical events plus its own
    branch-labeled events. Pinning the count catches two classes of
    regression: the scope function silently widening (sibling leakage)
    or narrowing (dropping canonical)."""
    canonical_only = [e for e in EVENTS_ALL
                      if e.branches == frozenset({":canonical"})]
    for b in CONTESTED_BRANCHES:
        own = [e for e in EVENTS_ALL if b.label in e.branches]
        expected_ids = {e.id for e in canonical_only} | {e.id for e in own}
        scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
        got_ids = {e.id for e in scoped}
        assert got_ids == expected_ids, \
            f"{b.label}: expected {sorted(expected_ids)}, " \
            f"got {sorted(got_ids)}"


# ============================================================================
# Runner
# ============================================================================

TESTS = [
    # Sibling non-inheritance
    test_stole_dagger_only_visible_on_woodcutter_branch,
    test_each_branchs_killing_does_not_leak_to_siblings,
    test_modality_of_intercourse_differs_by_branch,
    # Canonical-is-universal
    test_canonical_intercourse_fact_visible_on_every_branch,
    test_canonical_outcome_dead_husband_visible_on_every_branch,
    test_canonical_binding_observations_reach_agents_on_every_branch,
    # Reader projection
    test_reader_on_tajomaru_branch_knows_tajomaru_killed_husband,
    test_reader_on_husband_branch_knows_husband_killed_himself,
    test_reader_on_woodcutter_branch_knows_theft,
    test_reader_on_every_branch_shares_the_canonical_preamble,
    # Sjuzhet validation
    test_project_reader_rejects_tajomaru_sjuzhet_projected_on_wife_branch,
    # Branch-aware queries
    test_dramatic_irony_results_differ_per_branch,
    test_reader_over_character_irony_on_contested_fact,
    # Scope sanity
    test_branch_scope_sizes_add_up,
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
