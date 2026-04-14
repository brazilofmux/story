"""
test_inference.py — permanent tests for the inference engine
(inference-model-sketch-01 N1–N10).

These tests exercise the substrate's rule-derivation machinery
directly with synthetic fixtures plus spot-checks against the
retired-compound-predicate encodings in oedipus.py and macbeth.py.

Coverage maps to the sketch's commitments:

- N1 — Horn-clause shape; range-restriction; non-empty body.
- N3 — query-time derivation (held sets remain literal).
- N4 — composition with identity substitution.
- N5 — per-fold scoping (one agent's rules fire over their state
  only; another agent with different state gets different answers).
- N6 — weakest-premise slot propagation (KNOWN>BELIEVED>SUSPECTED>GAP);
  GAP premise fails.
- N7 — bounded fixpoint with depth cap.
- N8 — proofs carry rule id, bindings, premise proofs, depth.
- N10 — authored facts win over derivation.

Plus integration: the Oedipus retirement (parricide/incest) and the
Macbeth retirement (kinslayer/regicide/breach_of_hospitality/tyrant)
produce the expected derivations at the expected folds.

Run:  python3 test_inference.py
"""

from __future__ import annotations

import sys
import traceback

from substrate import (
    Rule, Prop, Proof, Slot, Confidence, Held, KnowledgeState,
    CANONICAL, project_knowledge, project_world, in_scope,
    derive_all_agent, derive_all_world,
    holds_derived, world_holds_derived,
    is_variable,
)


# ----------------------------------------------------------------------------
# Synthetic fixtures — simple rules and states
# ----------------------------------------------------------------------------

def _state_with(props_and_slots):
    """Build a tiny KnowledgeState from [(Prop, Slot), ...]."""
    by_prop = tuple(
        Held(prop=p, slot=s, confidence=Confidence.CERTAIN, via="observation")
        for p, s in props_and_slots
    )
    return KnowledgeState(agent_id="a", by_prop=by_prop)


# Standard test rules.
PARRICIDE = Rule(
    id="R_parricide",
    head=Prop("parricide", ("X", "Y")),
    body=(
        Prop("killed",   ("X", "Y")),
        Prop("child_of", ("X", "Y")),
    ),
)

KINSLAYER = Rule(
    id="R_kinslayer",
    head=Prop("kinslayer", ("X", "Y")),
    body=(Prop("killed", ("X", "Y")), Prop("kinsman_of", ("X", "Y"))),
)

REGICIDE = Rule(
    id="R_regicide",
    head=Prop("regicide", ("X", "Y")),
    body=(Prop("killed", ("X", "Y")), Prop("king", ("Y", "R"))),
)

TYRANT = Rule(
    id="R_tyrant",
    head=Prop("tyrant", ("X",)),
    body=(
        Prop("kinslayer", ("X", "V1")),
        Prop("regicide",  ("X", "V2")),
        Prop("king",      ("X", "R")),
    ),
)


# ----------------------------------------------------------------------------
# N1 — Horn-clause shape, range-restriction, non-empty body
# ----------------------------------------------------------------------------


def test_is_variable_convention():
    """Variables are strings starting with ASCII uppercase. Entity ids
    are lowercase by convention."""
    assert is_variable("X")
    assert is_variable("Killer")
    assert is_variable("Y1")
    assert not is_variable("oedipus")
    assert not is_variable("the-exposed-baby")
    assert not is_variable("")
    assert not is_variable(42)  # non-string arg is not a variable
    assert not is_variable(None)


def test_range_restriction_rejected():
    """A rule with a head variable that doesn't appear in the body must
    be rejected at construction time."""
    try:
        Rule(
            id="R_bad",
            head=Prop("bad", ("X", "Y")),
            body=(Prop("foo", ("X",)),),  # Y escapes
        )
    except ValueError as e:
        assert "Y" in str(e), f"error should mention the escaping var: {e}"
        return
    raise AssertionError("expected ValueError for range-restriction violation")


def test_empty_body_rejected():
    try:
        Rule(
            id="R_empty",
            head=Prop("head", ("X",)),
            body=(),
        )
    except ValueError as e:
        assert "empty body" in str(e)
        return
    raise AssertionError("expected ValueError for empty body")


# ----------------------------------------------------------------------------
# N3 — query-time derivation; held set stays literal
# ----------------------------------------------------------------------------


def test_held_set_unchanged_by_derivation():
    """Deriving a fact does not mutate the agent's by_prop. N3: query-
    time derivation is a view; state remains literal."""
    state = _state_with([
        (Prop("killed", ("a", "b")), Slot.KNOWN),
        (Prop("child_of", ("a", "b")), Slot.KNOWN),
    ])
    before = tuple(state.by_prop)
    _ = holds_derived(state, Prop("parricide", ("a", "b")), [PARRICIDE])
    assert state.by_prop == before, (
        "by_prop changed after derivation; N3 violated"
    )


# ----------------------------------------------------------------------------
# N4 — composition with identity substitution
# ----------------------------------------------------------------------------


def test_derivation_fires_under_identity_substitution():
    """An agent holds killed(a, placeholder) and identity(real, placeholder)
    at KNOWN; identity substitution lifts the premise; parricide should
    derive on (a, real)."""
    state = _state_with([
        (Prop("killed", ("a", "placeholder")), Slot.KNOWN),
        (Prop("child_of", ("a", "real")), Slot.KNOWN),
        (Prop("identity", ("real", "placeholder")), Slot.KNOWN),
    ])
    result = holds_derived(state, Prop("parricide", ("a", "real")), [PARRICIDE])
    assert result is not None, "substitution-enabled derivation missed"
    slot, proof = result
    assert slot == Slot.KNOWN
    assert proof.kind == "derived"
    assert proof.rule_id == "R_parricide"


def test_identity_substitution_alone_is_not_a_rule_derivation():
    """If the premises are already substitution-equivalent, the result
    should still be kind='derived' once a rule fires, not just
    'identity-substituted'."""
    state = _state_with([
        (Prop("killed", ("a", "placeholder")), Slot.KNOWN),
        (Prop("child_of", ("a", "placeholder")), Slot.KNOWN),
        (Prop("identity", ("real", "placeholder")), Slot.KNOWN),
    ])
    result = holds_derived(state, Prop("parricide", ("a", "real")), [PARRICIDE])
    assert result is not None
    _, proof = result
    assert proof.kind == "derived"
    assert proof.rule_id == "R_parricide"


# ----------------------------------------------------------------------------
# N5 — per-fold scoping
# ----------------------------------------------------------------------------


def test_rule_does_not_cross_agent_folds():
    """Rules fire per-fold. An agent with the premises derives the
    conclusion; another agent without the premises does not."""
    state_a = _state_with([
        (Prop("killed", ("a", "b")), Slot.KNOWN),
        (Prop("child_of", ("a", "b")), Slot.KNOWN),
    ])
    state_b = _state_with([
        (Prop("killed", ("a", "b")), Slot.KNOWN),
        # no child_of
    ])
    r_a = holds_derived(state_a, Prop("parricide", ("a", "b")), [PARRICIDE])
    r_b = holds_derived(state_b, Prop("parricide", ("a", "b")), [PARRICIDE])
    assert r_a is not None, "agent a should derive"
    assert r_b is None, "agent b lacks premises; should not derive"


# ----------------------------------------------------------------------------
# N6 — weakest-premise slot propagation; GAP fails
# ----------------------------------------------------------------------------


def test_both_premises_known_derives_known():
    state = _state_with([
        (Prop("killed", ("a", "b")), Slot.KNOWN),
        (Prop("child_of", ("a", "b")), Slot.KNOWN),
    ])
    slot, _ = holds_derived(state, Prop("parricide", ("a", "b")), [PARRICIDE])
    assert slot == Slot.KNOWN


def test_one_premise_believed_derives_believed():
    state = _state_with([
        (Prop("killed", ("a", "b")), Slot.KNOWN),
        (Prop("child_of", ("a", "b")), Slot.BELIEVED),
    ])
    slot, _ = holds_derived(state, Prop("parricide", ("a", "b")), [PARRICIDE])
    assert slot == Slot.BELIEVED, f"expected BELIEVED, got {slot}"


def test_one_premise_suspected_derives_suspected():
    state = _state_with([
        (Prop("killed", ("a", "b")), Slot.BELIEVED),
        (Prop("child_of", ("a", "b")), Slot.SUSPECTED),
    ])
    slot, _ = holds_derived(state, Prop("parricide", ("a", "b")), [PARRICIDE])
    assert slot == Slot.SUSPECTED


def test_gap_premise_fails():
    """A GAP premise means the body does not match — no derivation."""
    state = _state_with([
        (Prop("killed", ("a", "b")), Slot.KNOWN),
        (Prop("child_of", ("a", "b")), Slot.GAP),
    ])
    result = holds_derived(state, Prop("parricide", ("a", "b")), [PARRICIDE])
    assert result is None


# ----------------------------------------------------------------------------
# N7 — bounded fixpoint with depth cap
# ----------------------------------------------------------------------------


def test_depth_2_chain_requires_cap_at_least_2():
    """tyrant requires kinslayer and regicide, each depth 1, so tyrant
    is depth 2. Cap 1 should fail; cap 2 should succeed."""
    state = _state_with([
        (Prop("killed", ("k", "v")), Slot.KNOWN),
        (Prop("kinsman_of", ("k", "v")), Slot.KNOWN),
        (Prop("king", ("v", "realm")), Slot.KNOWN),
        (Prop("king", ("k", "realm")), Slot.KNOWN),
    ])
    rules = [KINSLAYER, REGICIDE, TYRANT]

    r1 = holds_derived(state, Prop("tyrant", ("k",)), rules, depth_cap=1)
    assert r1 is None, f"depth_cap=1 should not reach tyrant; got {r1}"

    r2 = holds_derived(state, Prop("tyrant", ("k",)), rules, depth_cap=2)
    assert r2 is not None, "depth_cap=2 should reach tyrant"
    _, proof = r2
    assert proof.depth == 2


def test_depth_cap_prevents_unbounded_iteration():
    """A deliberately-pathological rule set: P(X) ⇐ P(X) (self-reference).
    The fixpoint should terminate at the depth cap without error."""
    self_rule = Rule(
        id="R_selfref",
        head=Prop("p", ("X",)),
        body=(Prop("p", ("X",)),),
    )
    state = _state_with([(Prop("p", ("a",)), Slot.KNOWN)])
    # This should not hang; depth_cap bounds iteration.
    r = holds_derived(state, Prop("p", ("a",)), [self_rule], depth_cap=3)
    # p(a) was authored, so it's there at kind=authored.
    assert r is not None
    slot, proof = r
    assert proof.kind == "authored"


# ----------------------------------------------------------------------------
# N8 — proofs carry rule id, bindings, premise proofs, depth
# ----------------------------------------------------------------------------


def test_proof_carries_rule_id_and_bindings():
    state = _state_with([
        (Prop("killed", ("alice", "bob")), Slot.KNOWN),
        (Prop("child_of", ("alice", "bob")), Slot.KNOWN),
    ])
    _, proof = holds_derived(state, Prop("parricide", ("alice", "bob")), [PARRICIDE])
    assert proof.rule_id == "R_parricide"
    bindings = dict(proof.bindings)
    assert bindings == {"X": "alice", "Y": "bob"}
    assert proof.depth == 1


def test_proof_carries_premise_proofs():
    state = _state_with([
        (Prop("killed", ("alice", "bob")), Slot.KNOWN),
        (Prop("child_of", ("alice", "bob")), Slot.KNOWN),
    ])
    _, proof = holds_derived(state, Prop("parricide", ("alice", "bob")), [PARRICIDE])
    assert len(proof.premises) == 2
    for p in proof.premises:
        assert p.kind == "authored"


def test_proof_carries_premise_proofs_recursively_for_depth_2():
    """For a depth-2 derivation, at least one premise proof should be
    kind='derived' (a prior rule firing) and carry its own premises."""
    state = _state_with([
        (Prop("killed", ("k", "v")), Slot.KNOWN),
        (Prop("kinsman_of", ("k", "v")), Slot.KNOWN),
        (Prop("king", ("v", "realm")), Slot.KNOWN),
        (Prop("king", ("k", "realm")), Slot.KNOWN),
    ])
    rules = [KINSLAYER, REGICIDE, TYRANT]
    _, proof = holds_derived(state, Prop("tyrant", ("k",)), rules, depth_cap=3)
    derived_premises = [p for p in proof.premises if p.kind == "derived"]
    assert len(derived_premises) >= 1, (
        "depth-2 derivation should have at least one derived premise"
    )
    # Each derived premise should itself have authored-leaf premises.
    for p in derived_premises:
        assert all(q.kind == "authored" for q in p.premises)


# ----------------------------------------------------------------------------
# N10 — authored wins
# ----------------------------------------------------------------------------


def test_authored_at_weaker_slot_beats_derivation():
    """An author-asserted fact at BELIEVED should not be overridden by
    a rule-derivable fact at KNOWN. The authored slot wins per N10."""
    state = _state_with([
        (Prop("killed", ("a", "b")), Slot.KNOWN),
        (Prop("child_of", ("a", "b")), Slot.KNOWN),
        (Prop("parricide", ("a", "b")), Slot.BELIEVED),  # authored weaker
    ])
    slot, proof = holds_derived(state, Prop("parricide", ("a", "b")), [PARRICIDE])
    assert slot == Slot.BELIEVED, (
        f"authored BELIEVED should win over derived KNOWN; got {slot}"
    )
    assert proof.kind == "authored"


def test_authored_at_stronger_slot_also_wins():
    """Consistency: authored always wins, regardless of slot."""
    state = _state_with([
        (Prop("killed", ("a", "b")), Slot.BELIEVED),
        (Prop("child_of", ("a", "b")), Slot.BELIEVED),
        (Prop("parricide", ("a", "b")), Slot.KNOWN),  # authored stronger
    ])
    slot, proof = holds_derived(state, Prop("parricide", ("a", "b")), [PARRICIDE])
    assert slot == Slot.KNOWN
    assert proof.kind == "authored"


# ----------------------------------------------------------------------------
# derive_all — bulk derivation returns expected set
# ----------------------------------------------------------------------------


def test_derive_all_returns_derived_facts():
    state = _state_with([
        (Prop("killed", ("a", "b")), Slot.KNOWN),
        (Prop("child_of", ("a", "b")), Slot.KNOWN),
    ])
    facts = derive_all_agent(state, [PARRICIDE])
    # Should contain the two authored premises plus the derived parricide.
    assert Prop("killed", ("a", "b")) in facts
    assert Prop("child_of", ("a", "b")) in facts
    assert Prop("parricide", ("a", "b")) in facts
    assert facts[Prop("parricide", ("a", "b"))][1].kind == "derived"


def test_derive_all_world_handles_identity_expansion():
    """World-level derivation with an identity in the world set expands
    substitutionally."""
    world = {
        Prop("killed", ("a", "x")),
        Prop("child_of", ("a", "real")),
        Prop("identity", ("real", "x")),
    }
    facts = derive_all_world(world, [PARRICIDE])
    # parricide should be present either as (a, real) or (a, x) —
    # identity substitution should make both derivable.
    derived_parricides = [
        p for p in facts if p.predicate == "parricide"
    ]
    assert len(derived_parricides) >= 1


# ----------------------------------------------------------------------------
# Integration — Oedipus retirement
# ----------------------------------------------------------------------------


def test_oedipus_parricide_derives_in_world():
    """After retirement, parricide(oedipus, laius) should derive in
    world state via PARRICIDE_RULE."""
    import oedipus
    events = [e for e in oedipus.FABULA if in_scope(e, CANONICAL, oedipus.ALL_BRANCHES)]
    world_facts = project_world(events_in_scope=events, up_to_τ_s=100)
    # parricide should NOT be in world as authored:
    assert oedipus.parricide("oedipus", "laius") not in world_facts, (
        "parricide should have retired from authored world facts"
    )
    # But it SHOULD derive:
    proof = world_holds_derived(
        world_facts, oedipus.parricide("oedipus", "laius"), oedipus.RULES
    )
    assert proof is not None and proof.kind == "derived"
    assert proof.rule_id == "R_parricide_from_killed_and_parent"


def test_oedipus_incest_derives_in_world():
    import oedipus
    events = [e for e in oedipus.FABULA if in_scope(e, CANONICAL, oedipus.ALL_BRANCHES)]
    world_facts = project_world(events_in_scope=events, up_to_τ_s=100)
    assert oedipus.incest("oedipus", "jocasta") not in world_facts
    proof = world_holds_derived(
        world_facts, oedipus.incest("oedipus", "jocasta"), oedipus.RULES
    )
    assert proof is not None and proof.kind == "derived"


def test_oedipus_post_anagnorisis_holds_parricide_via_identity_and_rule():
    """Oedipus's post-anagnorisis state should derive parricide under
    identity substitution (killed(oedipus, the-crossroads-victim) +
    identity(laius, the-crossroads-victim) + child_of via the-exposed-
    baby identity) plus PARRICIDE_RULE."""
    import oedipus
    events = [e for e in oedipus.FABULA if in_scope(e, CANONICAL, oedipus.ALL_BRANCHES)]
    state = project_knowledge(agent_id="oedipus", events_in_scope=events, up_to_τ_s=13)
    result = holds_derived(state, oedipus.parricide("oedipus", "laius"), oedipus.RULES)
    assert result is not None, (
        "Oedipus should derive parricide at the anagnorisis"
    )
    slot, proof = result
    assert slot == Slot.KNOWN
    assert proof.kind == "derived"


def test_jocasta_pre_anagnorisis_does_not_derive_incest():
    """Pre-anagnorisis Jocasta lacks the identity to unify oedipus with
    the-exposed-baby, so she doesn't hold child_of(oedipus, jocasta)
    under substitution, so incest should not derive."""
    import oedipus
    events = [e for e in oedipus.FABULA if in_scope(e, CANONICAL, oedipus.ALL_BRANCHES)]
    state = project_knowledge(agent_id="jocasta", events_in_scope=events, up_to_τ_s=8)
    result = holds_derived(state, oedipus.incest("oedipus", "jocasta"), oedipus.RULES)
    assert result is None, (
        "Jocasta pre-anagnorisis should not derive incest"
    )


# ----------------------------------------------------------------------------
# Integration — Macbeth retirement
# ----------------------------------------------------------------------------


def test_macbeth_kinslayer_derives_after_duncan_killing():
    import macbeth
    events = [e for e in macbeth.FABULA if in_scope(e, CANONICAL, macbeth.ALL_BRANCHES)]
    world_facts = project_world(events_in_scope=events, up_to_τ_s=5)
    assert macbeth.kinslayer("macbeth", "duncan") not in world_facts
    proof = world_holds_derived(
        world_facts, macbeth.kinslayer("macbeth", "duncan"), macbeth.RULES
    )
    assert proof is not None and proof.kind == "derived"


def test_macbeth_regicide_derives_for_both_killings():
    """Both Macbeth's killing of Duncan (the tyrant forming) and
    Macduff's killing of Macbeth (the tyrant falling) are regicide per
    the rule (both victims are kings at time of killing)."""
    import macbeth
    events = [e for e in macbeth.FABULA if in_scope(e, CANONICAL, macbeth.ALL_BRANCHES)]

    # After Duncan's killing: regicide(macbeth, duncan) derives.
    w1 = project_world(events_in_scope=events, up_to_τ_s=5)
    assert world_holds_derived(w1, macbeth.regicide("macbeth", "duncan"), macbeth.RULES) is not None

    # After Macbeth's killing: regicide(macduff, macbeth) derives.
    w2 = project_world(events_in_scope=events, up_to_τ_s=17)
    assert world_holds_derived(w2, macbeth.regicide("macduff", "macbeth"), macbeth.RULES) is not None


def test_macbeth_not_kinslaying_when_victim_not_kin():
    """Macduff killing Macbeth is regicide but not kinslaying — they
    aren't kin."""
    import macbeth
    events = [e for e in macbeth.FABULA if in_scope(e, CANONICAL, macbeth.ALL_BRANCHES)]
    world_facts = project_world(events_in_scope=events, up_to_τ_s=17)
    proof = world_holds_derived(
        world_facts, macbeth.kinslayer("macduff", "macbeth"), macbeth.RULES
    )
    assert proof is None, "Macduff is not kin to Macbeth; kinslayer should not fire"


def test_macbeth_tyrant_requires_coronation():
    """tyrant(macbeth) requires kinslayer + regicide + king(macbeth, _).
    Pre-coronation, king(macbeth, _) is not yet true, so tyrant does
    not derive."""
    import macbeth
    events = [e for e in macbeth.FABULA if in_scope(e, CANONICAL, macbeth.ALL_BRANCHES)]

    # At τ_s=5 (just after Duncan killed, before coronation at τ_s=6):
    pre = project_world(events_in_scope=events, up_to_τ_s=5)
    result_pre = world_holds_derived(pre, macbeth.tyrant("macbeth"), macbeth.RULES)
    assert result_pre is None, "tyrant should not derive before coronation"

    # At τ_s=6 (coronation): all three premises satisfied.
    post = project_world(events_in_scope=events, up_to_τ_s=6)
    result_post = world_holds_derived(post, macbeth.tyrant("macbeth"), macbeth.RULES)
    assert result_post is not None, "tyrant should derive at coronation"
    assert result_post.depth == 2, f"tyrant is depth 2; got depth {result_post.depth}"


# ----------------------------------------------------------------------------
# Test runner
# ----------------------------------------------------------------------------


TESTS = [
    # N1 — Horn-clause shape
    test_is_variable_convention,
    test_range_restriction_rejected,
    test_empty_body_rejected,
    # N3 — query-time
    test_held_set_unchanged_by_derivation,
    # N4 — identity composition
    test_derivation_fires_under_identity_substitution,
    test_identity_substitution_alone_is_not_a_rule_derivation,
    # N5 — per-fold
    test_rule_does_not_cross_agent_folds,
    # N6 — slot propagation
    test_both_premises_known_derives_known,
    test_one_premise_believed_derives_believed,
    test_one_premise_suspected_derives_suspected,
    test_gap_premise_fails,
    # N7 — fixpoint depth
    test_depth_2_chain_requires_cap_at_least_2,
    test_depth_cap_prevents_unbounded_iteration,
    # N8 — proofs
    test_proof_carries_rule_id_and_bindings,
    test_proof_carries_premise_proofs,
    test_proof_carries_premise_proofs_recursively_for_depth_2,
    # N10 — authored wins
    test_authored_at_weaker_slot_beats_derivation,
    test_authored_at_stronger_slot_also_wins,
    # derive_all
    test_derive_all_returns_derived_facts,
    test_derive_all_world_handles_identity_expansion,
    # Oedipus retirement
    test_oedipus_parricide_derives_in_world,
    test_oedipus_incest_derives_in_world,
    test_oedipus_post_anagnorisis_holds_parricide_via_identity_and_rule,
    test_jocasta_pre_anagnorisis_does_not_derive_incest,
    # Macbeth retirement
    test_macbeth_kinslayer_derives_after_duncan_killing,
    test_macbeth_regicide_derives_for_both_killings,
    test_macbeth_not_kinslaying_when_victim_not_kin,
    test_macbeth_tyrant_requires_coronation,
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
