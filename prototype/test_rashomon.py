"""
test_rashomon.py — permanent tests over the Rashomon contested-branch
encoding, covering both the structural substrate and the description
surface.

These tests are story-specific: they import from `rashomon` and pin
properties of the substrate and description API as exercised by that
encoding. Substrate-level invariants that can be pinned *without* a
story live in `test_substrate.py`. This file exists because some
invariants only become load-bearing once a non-trivial :contested
example is folded through the substrate, and a regression in those
invariants would be invisible without a concrete case.

After the descriptions-sketch-01 refactor, this file also pins:

- Description-anchor invariants (every description's anchor resolves).
- Branch-scoping of descriptions (D4: inherit from anchor, with
  subset-override).
- Fold-description firewall (D1): fold functions do not see
  descriptions, and vice versa.

Discipline matches test_substrate.py:

- Plain assertions, no framework, no dependencies.
- Each test's docstring flags whether it pins a sketch-04 / -05
  commitment, a descriptions-sketch-01 commitment, or a narrower
  encoding choice.

Run:
    python3 test_rashomon.py
"""

from __future__ import annotations

import sys
import traceback
import inspect

from substrate import (
    Slot, Attention, Description, DescStatus, ReviewEntry, ReviewVerdict,
    Event, Branch, BranchKind, CANONICAL, CANONICAL_LABEL,
    scope, project_knowledge, project_reader, project_world,
    dramatic_ironies,
    descriptions_for, descriptions_on_branch, by_kind, open_questions,
    effective_branches, anchor_event, anchor_desc,
    reader_view, ingest_review, ingest_proposal, ingest_question_answer,
    accept_answer_proposal, decline_proposal,
    PromotionProposal, AnswerProposal,
    ReaderView, ViewEventRecord, ViewDescriptionRecord,
)
from rashomon import (
    EVENTS_ALL, SJUZHET_BY_BRANCH, AGENT_IDS, ALL_BRANCHES,
    CONTESTED_BRANCHES, DESCRIPTIONS,
    B_TAJOMARU, B_WIFE, B_HUSBAND, B_WOODCUTTER,
    killed, killed_with, stole, had_intercourse_with,
    dead, body_found_by, bound_to, at_location, fled,
)


# ============================================================================
# Sibling non-inheritance — the core :contested invariant
# ============================================================================

def test_stole_dagger_only_visible_on_woodcutter_branch():
    """Pins sketch-04/05 fold-scope rule: sibling :contested branches
    do not inherit from each other. stole(woodcutter, dagger) is
    authored only on :b-woodcutter. Every other branch's world
    projection must omit it."""
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
    """Sketch-04/05 guarantee: project_reader validates that every
    sjuzhet entry's event is in fold-scope for the target branch.
    Projecting Tajomaru's sjuzhet on :b-wife references events labeled
    only on :b-tajomaru, which are out of scope for :b-wife — sibling
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
    """Sketch-04/05 commits to branch-aware queries: in contested
    regions, Sternberg and irony queries return branch-indexed results.
    This test pins that the totals differ — if a regression collapsed
    branch-awareness back to canonical-only, all four counts would be
    equal. (Necessary-not-sufficient.)"""
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
    # Woodcutter's branch has extra disclosed facts (the theft) beyond
    # what other branches see, so its total should be the largest. This
    # pins a specific relation.
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
# Description surface — attachment, branch-scoping, firewall
# (descriptions-sketch-01 D1–D5)
# ============================================================================

def test_every_description_has_a_resolvable_anchor():
    """D3: descriptions attach to typed anchors. A free-floating
    description is not a valid record. Every description in the
    encoding must have an anchor that resolves to an existing event
    or description."""
    event_ids = {e.id for e in EVENTS_ALL}
    desc_ids  = {d.id for d in DESCRIPTIONS}
    for d in DESCRIPTIONS:
        if d.attached_to.kind == "event":
            assert d.attached_to.target_id in event_ids, \
                f"{d.id}: event anchor {d.attached_to.target_id!r} not found"
        elif d.attached_to.kind == "description":
            assert d.attached_to.target_id in desc_ids, \
                f"{d.id}: description anchor " \
                f"{d.attached_to.target_id!r} not found"
        else:
            raise AssertionError(
                f"{d.id}: unexpected anchor kind {d.attached_to.kind!r}"
            )


def test_intercourse_has_four_branch_scoped_textures_plus_canonical_frame():
    """Pins the descriptions-sketch-01 worked example: the canonical
    E_intercourse event carries four per-branch texture descriptions
    (one per contested branch) and a trans-branch reader-frame
    description scoped to :canonical."""
    attached = descriptions_for(anchor_event("E_intercourse"), DESCRIPTIONS)
    texture_by_branch = {}
    frame = None
    for d in attached:
        if d.kind == "texture":
            assert d.branches is not None and len(d.branches) == 1, \
                f"{d.id}: texture should be scoped to a single branch"
            (label,) = tuple(d.branches)
            texture_by_branch[label] = d
        elif d.kind == "reader-frame":
            frame = d
    expected = {b.label for b in CONTESTED_BRANCHES}
    assert set(texture_by_branch.keys()) == expected, \
        f"texture-branch coverage: got {sorted(texture_by_branch.keys())}, " \
        f"expected {sorted(expected)}"
    assert frame is not None, "no reader-frame description on E_intercourse"
    assert frame.branches == frozenset({":canonical"}), \
        f"frame should be :canonical-scoped; got {frame.branches}"


def test_branch_scoped_description_visible_only_on_its_branch():
    """D4: a branch-scoped description is visible on that branch and
    invisible on siblings. The wife's texture description on
    E_intercourse has branches={:b-wife}; :b-tajomaru, :b-husband, and
    :b-woodcutter must not see it."""
    anchor_desc_id = "D_intercourse_wife_texture"
    attached = descriptions_for(anchor_event("E_intercourse"), DESCRIPTIONS)
    for b in CONTESTED_BRANCHES:
        visible = descriptions_on_branch(
            branch=b, descriptions=attached, events=EVENTS_ALL,
            all_branches=ALL_BRANCHES, up_to_τ_a=10_000,
        )
        visible_ids = {d.id for d in visible}
        if b.label == B_WIFE.label:
            assert anchor_desc_id in visible_ids, \
                f"{anchor_desc_id} missing on own branch {b.label}"
        else:
            assert anchor_desc_id not in visible_ids, \
                f"{anchor_desc_id} leaked onto sibling {b.label}"


def test_canonical_scoped_description_visible_on_every_branch():
    """D4 + canonical-is-universal: a description scoped to :canonical
    is visible on every descendant branch. The reader-frame
    description on E_intercourse must surface in every contested
    branch's visible description set."""
    attached = descriptions_for(anchor_event("E_intercourse"), DESCRIPTIONS)
    for b in CONTESTED_BRANCHES:
        visible = descriptions_on_branch(
            branch=b, descriptions=attached, events=EVENTS_ALL,
            all_branches=ALL_BRANCHES, up_to_τ_a=10_000,
        )
        visible_ids = {d.id for d in visible}
        assert "D_intercourse_frame" in visible_ids, \
            f"canonical reader-frame missing on {b.label}"


def test_description_inherits_anchor_branches_when_no_override():
    """D4 default: a description without an explicit `branches` field
    inherits its anchor's branch set. The duel-character texture on
    E_t_duel does not set `branches`; it should inherit {:b-tajomaru}
    and therefore be visible on :b-tajomaru but not on sibling
    branches."""
    # D_t_duel_character has no branches field; it inherits from its
    # anchor E_t_duel which is on {:b-tajomaru}.
    target = "D_t_duel_character"
    d = next(d for d in DESCRIPTIONS if d.id == target)
    assert d.branches is None, \
        f"precondition: {target} should have no explicit branches"
    eff = effective_branches(d, EVENTS_ALL, DESCRIPTIONS)
    assert eff == frozenset({B_TAJOMARU.label}), \
        f"expected inherited branches {{:b-tajomaru}}, got {eff}"


def test_description_on_description_resolves_through_chain():
    """D3: descriptions can anchor on other descriptions. The
    authorial-uncertainty description is attached to the
    woodcutter-trust description. Its effective branches should
    resolve through the anchor chain — D_woodcutter_trust is scoped
    to :b-woodcutter, so the uncertainty description inherits that."""
    target = "D_wc_authorial_doubt"
    d = next(d for d in DESCRIPTIONS if d.id == target)
    assert d.attached_to.kind == "description", \
        f"precondition: {target} should anchor on another description"
    eff = effective_branches(d, EVENTS_ALL, DESCRIPTIONS)
    assert eff == frozenset({B_WOODCUTTER.label}), \
        f"expected inherited {{:b-woodcutter}} via description chain, " \
        f"got {eff}"


def test_open_questions_surface_authorial_uncertainty():
    """An is_question description routes to the open-questions queue
    per descriptions-sketch-01. The woodcutter-reliability question is
    the only one in the encoding; pinning that it surfaces protects
    the API contract."""
    questions = open_questions(DESCRIPTIONS)
    ids = {d.id for d in questions}
    assert "D_wc_authorial_doubt" in ids, \
        f"expected D_wc_authorial_doubt in open_questions; got {sorted(ids)}"


def test_by_kind_returns_consistent_counts():
    """by_kind should return exactly the descriptions whose kind field
    matches. Pins the starting-six vocabulary is exercised: the
    encoding uses texture, motivation, reader-frame, trust-flag, and
    authorial-uncertainty. (provenance is not yet exercised — a
    follow-on for the next iteration.)"""
    kinds_used = {d.kind for d in DESCRIPTIONS}
    expected_kinds = {
        "texture", "motivation", "reader-frame",
        "trust-flag", "authorial-uncertainty",
    }
    assert kinds_used == expected_kinds, \
        f"kinds used: {sorted(kinds_used)}; expected {sorted(expected_kinds)}"
    # And by_kind agrees with manual filtering (compared by id, since
    # Description carries a mutable metadata dict and is not hashable).
    for k in kinds_used:
        got = {d.id for d in by_kind(DESCRIPTIONS, k)}
        manual = {d.id for d in DESCRIPTIONS if d.kind == k}
        assert got == manual, f"by_kind({k!r}) diverges from manual filter"


# ============================================================================
# Firewall — fold functions do not accept descriptions (D1)
# ============================================================================

def test_fold_function_signatures_do_not_mention_descriptions():
    """D1: the fold API and the description API are separate surfaces.
    No fold function accepts a Description in its signature. This is a
    signature check — not a runtime guarantee, but a structural
    invariant that catches regressions where someone would pass
    descriptions through a fold by accident."""
    fold_functions = [project_knowledge, project_world, project_reader,
                      dramatic_ironies, scope]
    for fn in fold_functions:
        sig = inspect.signature(fn)
        for param_name in sig.parameters:
            assert "description" not in param_name.lower(), \
                f"fold function {fn.__name__} has description-adjacent " \
                f"parameter {param_name!r}; D1 firewall breach"


def test_fold_outputs_do_not_carry_description_values():
    """D1 from the other direction: projection outputs (reader state,
    world state) must not contain Description instances. They carry
    Held records and Prop records only. Pinning this catches a class
    of regression where a fold implementer might try to attach
    interpretive content to the fold's output structure."""
    for b in CONTESTED_BRANCHES:
        scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
        w = project_world(scoped, 100)
        for item in w:
            assert not isinstance(item, Description), \
                f"project_world leaked a Description on {b.label}"
        reader = project_reader(
            sjuzhet=SJUZHET_BY_BRANCH[b.label],
            all_events=EVENTS_ALL, branch=b,
            all_branches=ALL_BRANCHES, up_to_τ_d=100,
        )
        for h in reader.by_prop:
            assert not isinstance(h, Description), \
                f"project_reader leaked a Description on {b.label}"


# ============================================================================
# Reader-model probe (reader-model-sketch-01 R1, R2, R5)
# ============================================================================
#
# These tests exercise the tiny probe surface — reader_view, ingest_review,
# ingest_proposal — against the Rashomon encoding. Question-answer ingestion
# and refusal/malformed records are deferred to a later probe iteration; the
# current tests pin view shape, scope declarations, review ingestion
# producing a new immutable Description, and the structural separation of
# facts from descriptions in the view.


def test_view_separates_events_from_descriptions_structurally():
    """R2: facts and descriptions are in distinct containers. A
    reader-model consuming this view cannot receive a description
    where an event is expected, or vice versa, because they live in
    different tuples with different record types."""
    v = reader_view(
        branch=B_WOODCUTTER, events=EVENTS_ALL, descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES, up_to_τ_s=100, up_to_τ_a=10_000,
    )
    # Separate containers.
    assert isinstance(v.events, tuple)
    assert isinstance(v.descriptions, tuple)
    # Distinct types; neither list mixes the other's record kind.
    for r in v.events:
        assert isinstance(r, ViewEventRecord), \
            f"events list contained non-event record {type(r).__name__}"
    for r in v.descriptions:
        assert isinstance(r, ViewDescriptionRecord), \
            f"descriptions list contained non-description record " \
            f"{type(r).__name__}"


def test_view_respects_branch_scope_for_events_and_descriptions():
    """R5: the view's branch scope is declared and enforced. Events and
    descriptions visible only on a sibling branch must not leak."""
    v_wife = reader_view(
        branch=B_WIFE, events=EVENTS_ALL, descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES, up_to_τ_s=100, up_to_τ_a=10_000,
    )
    event_ids = {r.event.id for r in v_wife.events}
    desc_ids  = {r.description.id for r in v_wife.descriptions}
    # :b-tajomaru events should not appear on :b-wife's view.
    assert "E_t_duel" not in event_ids, "tajomaru event leaked into wife view"
    # :b-tajomaru texture description should not appear on :b-wife's view.
    assert "D_intercourse_tajomaru_texture" not in desc_ids, \
        "tajomaru texture leaked into wife view"
    # :b-wife-scoped description should appear.
    assert "D_intercourse_wife_texture" in desc_ids, \
        "wife texture missing from wife view"


def test_view_respects_τ_s_and_τ_a_bounds():
    """R5: the view's up_to_τ_s and up_to_τ_a bounds are enforced.
    Events with τ_s > up_to_τ_s or τ_a > up_to_τ_a are excluded;
    descriptions with τ_a > up_to_τ_a are excluded."""
    # Narrow bound — before the intercourse event (τ_s=5, τ_a=6) and
    # before any authored description (earliest is τ_a=100).
    v = reader_view(
        branch=B_WIFE, events=EVENTS_ALL, descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES, up_to_τ_s=3, up_to_τ_a=5,
    )
    event_ids = {r.event.id for r in v.events}
    desc_ids  = {r.description.id for r in v.descriptions}
    assert "E_intercourse" not in event_ids, \
        f"intercourse at τ_s=5 should be out of scope at up_to_τ_s=3"
    assert len(desc_ids) == 0, \
        f"no descriptions should be in scope at up_to_τ_a=5; got {desc_ids}"

    # Wide bound — everything in scope.
    v_wide = reader_view(
        branch=B_WIFE, events=EVENTS_ALL, descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES, up_to_τ_s=1000, up_to_τ_a=10_000,
    )
    wide_event_ids = {r.event.id for r in v_wide.events}
    assert "E_intercourse" in wide_event_ids


def test_view_applies_attention_filter():
    """R5: attention_filter declares which attention levels are in
    scope. A structural-only filter excludes interpretive and flavor
    descriptions."""
    v = reader_view(
        branch=B_WOODCUTTER, events=EVENTS_ALL, descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES, up_to_τ_s=100, up_to_τ_a=10_000,
        attention_filter=frozenset({Attention.STRUCTURAL}),
    )
    for r in v.descriptions:
        assert r.description.attention == Attention.STRUCTURAL, \
            f"non-structural description {r.description.id} " \
            f"leaked through attention_filter"


def test_view_applies_anchor_scope():
    """R5: anchor_scope narrows the view to specific anchor ids.
    Events not in the scope are excluded; descriptions whose anchor
    or self is in the scope are included."""
    scope_ids = frozenset({"E_wc_theft", "D_woodcutter_trust"})
    v = reader_view(
        branch=B_WOODCUTTER, events=EVENTS_ALL, descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES, up_to_τ_s=100, up_to_τ_a=10_000,
        anchor_scope=scope_ids,
    )
    event_ids = {r.event.id for r in v.events}
    desc_ids  = {r.description.id for r in v.descriptions}
    # Only E_wc_theft from the scope.
    assert event_ids == {"E_wc_theft"}, \
        f"anchor_scope did not narrow events as expected: {event_ids}"
    # D_woodcutter_trust itself (self in scope), plus D_wc_authorial_doubt
    # (attached_to D_woodcutter_trust, which is in scope).
    assert "D_woodcutter_trust" in desc_ids
    assert "D_wc_authorial_doubt" in desc_ids, \
        "description whose anchor is in scope should surface"


def test_view_open_questions_subsets_descriptions():
    """The view's open_questions is precisely the subset of its
    descriptions where is_question=True."""
    v = reader_view(
        branch=B_WOODCUTTER, events=EVENTS_ALL, descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES, up_to_τ_s=100, up_to_τ_a=10_000,
    )
    desc_ids = {r.description.id for r in v.descriptions}
    question_ids = {r.description.id for r in v.open_questions}
    assert question_ids.issubset(desc_ids), \
        "open_questions is not a subset of descriptions"
    for r in v.open_questions:
        assert r.description.is_question, \
            f"non-question in open_questions: {r.description.id}"
    # The encoding has one question on :b-woodcutter.
    assert "D_wc_authorial_doubt" in question_ids, \
        f"expected D_wc_authorial_doubt in open_questions; got {question_ids}"


def test_view_flags_effectively_unreviewed_descriptions():
    """Descriptions with no approving review are flagged
    effectively_unreviewed=True at view-construction time. The
    Rashomon encoding has no reviews authored yet, so every
    description in the view is effectively unreviewed."""
    v = reader_view(
        branch=B_WOODCUTTER, events=EVENTS_ALL, descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES, up_to_τ_s=100, up_to_τ_a=10_000,
    )
    for r in v.descriptions:
        assert r.effectively_unreviewed, \
            f"{r.description.id} flagged reviewed, but no reviews exist " \
            f"in the encoding"


def test_ingest_review_produces_new_immutable_description():
    """R4 + descriptions-01 record-level invariants: ingesting a
    review returns a new Description with the review appended to
    review_states. The original is unchanged (immutability); the new
    record has exactly one more review than the original."""
    original = next(d for d in DESCRIPTIONS if d.id == "D_wc_authorial_doubt")
    assert len(original.review_states) == 0, \
        "precondition: description has no reviews yet"

    review = ReviewEntry(
        reviewer_id="llm:mock",
        reviewed_at_τ_a=10_001,
        verdict=ReviewVerdict.NOTED,
        anchor_τ_a=original.τ_a,
        comment="Mock review for probe test.",
    )
    updated = ingest_review(original, review)

    # Original unchanged (immutability).
    assert len(original.review_states) == 0, \
        "original description was mutated; immutability violated"
    # New record has the review.
    assert len(updated.review_states) == 1
    assert updated.review_states[0] == review
    # Other fields preserved.
    assert updated.id == original.id
    assert updated.text == original.text
    assert updated.τ_a == original.τ_a


def test_ingest_review_flips_effectively_unreviewed_in_next_view():
    """After ingesting an approving review at the current anchor τ_a,
    the description is no longer effectively_unreviewed in a view
    built over the updated collection. This pins the feedback loop:
    reader-model output flows back through the view."""
    target_id = "D_wc_authorial_doubt"
    original = next(d for d in DESCRIPTIONS if d.id == target_id)
    review = ReviewEntry(
        reviewer_id="llm:mock",
        reviewed_at_τ_a=10_001,
        verdict=ReviewVerdict.APPROVED,
        anchor_τ_a=original.τ_a,
        comment="",
    )
    updated = ingest_review(original, review)

    # Swap in the updated record.
    updated_descriptions = [
        updated if d.id == target_id else d
        for d in DESCRIPTIONS
    ]
    v = reader_view(
        branch=B_WOODCUTTER, events=EVENTS_ALL,
        descriptions=updated_descriptions,
        all_branches=ALL_BRANCHES, up_to_τ_s=100, up_to_τ_a=10_001,
    )
    match = [r for r in v.descriptions if r.description.id == target_id]
    assert len(match) == 1
    assert not match[0].effectively_unreviewed, \
        "approved review did not flip effectively_unreviewed in the view"


def test_ingest_proposal_appends_to_queue_without_mutation():
    """R3 + D5 + descriptions-01 proposal queue: ingesting a
    PromotionProposal returns a new queue with the proposal appended.
    The original queue is unchanged."""
    queue = []
    proposal = PromotionProposal(
        description_id="D_intercourse_wife_texture",
        proposed_fact=None,  # tooling would supply an Event or Effect here
        proposer_id="llm:mock",
        rationale="coercion appears to warrant a coercion event if the "
                  "story later tracks trauma-state (substrate-05 M1).",
        proposed_at_τ_a=10_002,
    )
    new_queue = ingest_proposal(proposal, queue)
    assert queue == [], "original queue mutated"
    assert len(new_queue) == 1
    assert new_queue[0].status == "pending", \
        "new proposal should land pending"


def _make_answer_proposal(question_id: str, new_desc_id: str, τ_a: int = 20_000):
    """Helper: build an AnswerProposal whose proposed_description is a
    plausible answer to D_wc_authorial_doubt. Used by the accept/decline
    tests below."""
    question = next(d for d in DESCRIPTIONS if d.id == question_id)
    proposed = Description(
        id=new_desc_id,
        attached_to=question.attached_to,
        kind="reader-frame",
        attention=Attention.INTERPRETIVE,
        text="test answer text",
        authored_by="llm:mock",
        τ_a=τ_a,
        branches=question.branches,
        status=DescStatus.PROVISIONAL,
        metadata={"answers_question": question_id},
    )
    return AnswerProposal(
        question_description_id=question_id,
        proposed_description=proposed,
        proposer_id="llm:mock",
        rationale="test rationale",
        proposed_at_τ_a=τ_a,
    )


def test_ingest_question_answer_appends_answer_proposal_to_queue():
    """reader-model-sketch-01 §Question-answers: an AnswerProposal
    lands in the same queue as PromotionProposals, distinguished by
    type. The queue carries both kinds; a walker can iterate and
    dispatch by isinstance."""
    queue = []
    ap = _make_answer_proposal(
        "D_wc_authorial_doubt", "D_wc_authorial_doubt_answer_test"
    )
    new_queue = ingest_question_answer(ap, queue)
    assert queue == [], "original queue mutated"
    assert len(new_queue) == 1
    assert isinstance(new_queue[0], AnswerProposal)
    assert new_queue[0].status == "pending"


def test_accept_answer_proposal_commits_new_description():
    """R3 authorial-act: accepting a pending AnswerProposal appends a
    committed Description to the descriptions collection and flips the
    queue entry's status to accepted. The committed description carries
    the metadata link back to the question (answers_question pointer)."""
    queue = ingest_question_answer(
        _make_answer_proposal(
            "D_wc_authorial_doubt", "D_wc_authorial_doubt_answer_accept"
        ),
        [],
    )
    proposal = queue[0]
    new_desc, new_queue = accept_answer_proposal(
        proposal, list(DESCRIPTIONS), queue
    )

    # Descriptions grew by exactly one, and the new record is committed.
    assert len(new_desc) == len(DESCRIPTIONS) + 1
    committed = new_desc[-1]
    assert committed.id == "D_wc_authorial_doubt_answer_accept"
    assert committed.status == DescStatus.COMMITTED, (
        f"accepted answer should be committed; got {committed.status}"
    )
    assert committed.metadata.get("answers_question") == "D_wc_authorial_doubt"

    # Queue entry status flipped; proposal object itself unchanged.
    assert proposal.status == "pending", "original proposal was mutated"
    assert new_queue[0].status == "accepted"
    assert len(new_queue) == 1, "queue length should be stable on accept"


def test_accept_answer_proposal_surfaces_in_subsequent_view():
    """Accepted answer flows back through the view: a reader_view built
    over the extended descriptions collection includes the committed
    answer description on :b-woodcutter (the question's branch)."""
    queue = ingest_question_answer(
        _make_answer_proposal(
            "D_wc_authorial_doubt", "D_wc_authorial_doubt_answer_view"
        ),
        [],
    )
    new_desc, _ = accept_answer_proposal(
        queue[0], list(DESCRIPTIONS), queue
    )
    v = reader_view(
        branch=B_WOODCUTTER, events=EVENTS_ALL,
        descriptions=new_desc,
        all_branches=ALL_BRANCHES,
        up_to_τ_s=100, up_to_τ_a=30_000,
    )
    desc_ids = {r.description.id for r in v.descriptions}
    assert "D_wc_authorial_doubt_answer_view" in desc_ids, (
        "accepted answer description should appear in a subsequent "
        "reader_view on :b-woodcutter"
    )


def test_decline_answer_proposal_flips_status_no_new_description():
    """Declining a pending AnswerProposal flips its queue status to
    declined without touching the descriptions collection."""
    queue = ingest_question_answer(
        _make_answer_proposal(
            "D_wc_authorial_doubt", "D_wc_authorial_doubt_answer_decline"
        ),
        [],
    )
    new_queue = decline_proposal(queue[0], queue)
    assert new_queue[0].status == "declined"
    assert queue[0].status == "pending", "original proposal was mutated"


def test_decline_promotion_proposal_also_works():
    """decline_proposal is generic over AnswerProposal and
    PromotionProposal; the queue carries both kinds and declining is
    uniform."""
    queue = ingest_proposal(
        PromotionProposal(
            description_id="D_intercourse_wife_texture",
            proposed_fact=None,
            proposer_id="llm:mock",
            rationale="not worth promoting this round",
            proposed_at_τ_a=10_003,
        ),
        [],
    )
    new_queue = decline_proposal(queue[0], queue)
    assert new_queue[0].status == "declined"


def test_accept_declined_proposal_raises():
    """A proposal that has already been declined cannot be re-accepted.
    This pins the invariant that status transitions are one-shot:
    pending → accepted | declined, and neither terminal state flows
    back to pending."""
    queue = ingest_question_answer(
        _make_answer_proposal(
            "D_wc_authorial_doubt", "D_wc_authorial_doubt_answer_reaccept"
        ),
        [],
    )
    declined_queue = decline_proposal(queue[0], queue)
    try:
        accept_answer_proposal(
            declined_queue[0], list(DESCRIPTIONS), declined_queue,
        )
    except ValueError:
        return
    raise AssertionError(
        "re-accepting a declined proposal should raise ValueError"
    )


def test_anchor_in_view_false_when_description_anchor_is_filtered_out():
    """The anchor_in_view flag answers 'is the anchor in *this view*?'
    — not 'does the anchor exist in the collection?'. When a structural-
    only filter retains a structural description whose interpretive
    anchor description is filtered out, anchor_in_view must be False
    so the reader-model knows its context is thin."""
    v = reader_view(
        branch=B_WOODCUTTER, events=EVENTS_ALL, descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES, up_to_τ_s=100, up_to_τ_a=10_000,
        attention_filter=frozenset({Attention.STRUCTURAL}),
    )
    match = [r for r in v.descriptions
             if r.description.id == "D_wc_authorial_doubt"]
    assert len(match) == 1, \
        "precondition: structural D_wc_authorial_doubt should remain"
    record = match[0]

    view_ids = {r.description.id for r in v.descriptions}
    assert "D_woodcutter_trust" not in view_ids, \
        "precondition: interpretive anchor should be filtered out " \
        f"under attention=structural; got {view_ids}"

    assert record.anchor_in_view is False, \
        "anchor_in_view should be False when the anchor description " \
        "is filtered out of the view, even if it exists in the full " \
        "description collection"


def test_staleness_computed_at_view_τ_a_bound():
    """R6 + the ReaderView contract: staleness uses the anchor's τ_a
    as of the view's up_to_τ_a bound, not its present τ_a. A
    historical view must not classify a review as stale based on
    anchor edits outside its scope. This test uses synthetic data —
    an anchor event edited at a later τ_a — because the Rashomon
    encoding does not yet exercise anchor-edit flows."""
    # Original anchor event at τ_a=6.
    E_original = Event(
        id="E_test",
        type="test",
        τ_s=0, τ_a=6,
        participants={},
        effects=(),
        branches=frozenset({CANONICAL_LABEL}),
    )
    # Edited anchor event — same id, later τ_a. Represents an author's
    # revision that would make prior reviews stale under R6.
    E_edited = Event(
        id="E_test",
        type="test",
        τ_s=0, τ_a=500,
        participants={},
        effects=(),
        branches=frozenset({CANONICAL_LABEL}),
    )
    # Description with one approving review; the review was taken
    # against the original anchor version (anchor_τ_a=6).
    D_test = Description(
        id="D_test",
        attached_to=anchor_event("E_test"),
        kind="texture",
        attention=Attention.INTERPRETIVE,
        text="irrelevant",
        authored_by="author",
        τ_a=100,
        review_states=(ReviewEntry(
            reviewer_id="llm:mock",
            reviewed_at_τ_a=120,
            verdict=ReviewVerdict.APPROVED,
            anchor_τ_a=6,
            comment="",
        ),),
    )
    events = [E_original, E_edited]
    descriptions = [D_test]
    all_branches = {CANONICAL_LABEL: CANONICAL}

    # View bounded before the edit — the τ_a=500 revision is out of
    # scope; the anchor's current-in-view τ_a is 6; the review at
    # anchor_τ_a=6 is NOT stale.
    v_before = reader_view(
        branch=CANONICAL, events=events, descriptions=descriptions,
        all_branches=all_branches, up_to_τ_s=1000, up_to_τ_a=200,
    )
    assert len(v_before.descriptions) == 1
    assert v_before.descriptions[0].stale_review_ids == (), \
        f"review at anchor_τ_a=6 should NOT be stale when view's " \
        f"up_to_τ_a=200 excludes the τ_a=500 edit; got " \
        f"stale_ids={v_before.descriptions[0].stale_review_ids}"

    # View bounded after the edit — the τ_a=500 revision is in scope;
    # the anchor's current-in-view τ_a is 500; the review at
    # anchor_τ_a=6 IS stale.
    v_after = reader_view(
        branch=CANONICAL, events=events, descriptions=descriptions,
        all_branches=all_branches, up_to_τ_s=1000, up_to_τ_a=600,
    )
    assert len(v_after.descriptions) == 1
    assert v_after.descriptions[0].stale_review_ids == (0,), \
        f"review at anchor_τ_a=6 should be stale when view's " \
        f"up_to_τ_a=600 includes the τ_a=500 edit; got " \
        f"stale_ids={v_after.descriptions[0].stale_review_ids}"


def test_view_is_reproducible_at_same_bounds():
    """Determinism: two reader_view calls with the same arguments
    produce equal results. This is the reproducibility property R5
    implies — caching the view is safe, and so is diffing views
    across τ_a."""
    kwargs = dict(
        branch=B_WIFE, events=EVENTS_ALL, descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES, up_to_τ_s=100, up_to_τ_a=10_000,
    )
    v1 = reader_view(**kwargs)
    v2 = reader_view(**kwargs)
    assert v1 == v2, "reader_view is not reproducible at identical args"


# ============================================================================
# Runner
# ============================================================================

TESTS = [
    # Sibling non-inheritance
    test_stole_dagger_only_visible_on_woodcutter_branch,
    test_each_branchs_killing_does_not_leak_to_siblings,
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
    # Description surface (descriptions-sketch-01)
    test_every_description_has_a_resolvable_anchor,
    test_intercourse_has_four_branch_scoped_textures_plus_canonical_frame,
    test_branch_scoped_description_visible_only_on_its_branch,
    test_canonical_scoped_description_visible_on_every_branch,
    test_description_inherits_anchor_branches_when_no_override,
    test_description_on_description_resolves_through_chain,
    test_open_questions_surface_authorial_uncertainty,
    test_by_kind_returns_consistent_counts,
    # Firewall
    test_fold_function_signatures_do_not_mention_descriptions,
    test_fold_outputs_do_not_carry_description_values,
    # Reader-model probe (reader-model-sketch-01)
    test_view_separates_events_from_descriptions_structurally,
    test_view_respects_branch_scope_for_events_and_descriptions,
    test_view_respects_τ_s_and_τ_a_bounds,
    test_view_applies_attention_filter,
    test_view_applies_anchor_scope,
    test_view_open_questions_subsets_descriptions,
    test_view_flags_effectively_unreviewed_descriptions,
    test_ingest_review_produces_new_immutable_description,
    test_ingest_review_flips_effectively_unreviewed_in_next_view,
    test_ingest_proposal_appends_to_queue_without_mutation,
    test_ingest_question_answer_appends_answer_proposal_to_queue,
    test_accept_answer_proposal_commits_new_description,
    test_accept_answer_proposal_surfaces_in_subsequent_view,
    test_decline_answer_proposal_flips_status_no_new_description,
    test_decline_promotion_proposal_also_works,
    test_accept_declined_proposal_raises,
    test_anchor_in_view_false_when_description_anchor_is_filtered_out,
    test_staleness_computed_at_view_τ_a_bound,
    test_view_is_reproducible_at_same_bounds,
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
