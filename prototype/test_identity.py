"""
test_identity.py — permanent tests for the identity-and-realization
probe (identity-and-realization-sketch-01).

These tests exercise the substrate's identity-substitution machinery
directly with synthetic fixtures. They do not depend on the Oedipus
or Rashomon encodings — the probe adds substrate-level infrastructure,
and the tests here pin that infrastructure independently of any
particular story. Oedipus-specific integration (the
`realize_add`/`realize_remove` pattern refactored into identity
assertions) is a follow-on once this probe is committed.

Test coverage maps to the sketch's commitments:

- I3 (query-time substitution, held set stays literal) — several
  tests confirm by_prop is unchanged by query operations.
- I4 (symmetric, transitive) — direct tests for each direction.
- I6 (no synthesis) — implicit; no test can assert absence of a
  feature, but the firewall is that substrate code never calls
  any synthesis function.
- I7 (KNOWN-only substitution) — direct negative test.
- Multi-match resolution (strongest slot, earliest by_prop order
  as the τ_a proxy) — direct test.
- sternberg_curiosity stays literal (the explicit carve-out in the
  sketch's in-scope section).
- Irony composes with substitution — direct test of the
  anagnorisis collapse pattern.
- World-side substitution via world_holds — direct test.

Run:
    python3 test_identity.py
"""

from __future__ import annotations

import sys
import traceback

from substrate import (
    Prop, Held, Slot, Confidence, Diegetic,
    KnowledgeState,
    IDENTITY_PREDICATE,
    world_holds, world_holds_literal,
    _build_equivalence_classes, _prop_matches_under_substitution,
)


# ----------------------------------------------------------------------------
# Fixtures — synthetic Held records
# ----------------------------------------------------------------------------

def h(prop: Prop, slot: Slot = Slot.KNOWN,
      via: str = Diegetic.OBSERVATION.value) -> Held:
    return Held(
        prop=prop, slot=slot,
        confidence=Confidence.CERTAIN if slot == Slot.KNOWN else Confidence.BELIEVED,
        via=via,
    )


def identity_prop(a: str, b: str) -> Prop:
    return Prop(IDENTITY_PREDICATE, (a, b))


def P(*args) -> Prop:
    """Shorthand for building a test proposition with predicate 'P'."""
    return Prop("P", args)


# ============================================================================
# I3 — substitution is query-time; the held set stays literal
# ============================================================================

def test_by_prop_is_unchanged_by_queries():
    """I3: the literal held set is not mutated by `holds` queries.
    Running substitution-aware queries against an agent's state must
    leave by_prop exactly as it was — no implicit derived records."""
    state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a")),
            h(identity_prop("a", "b")),
        ),
    )
    before = state.by_prop
    # Run several substitution-aware queries.
    state.holds(P("a"))
    state.holds(P("b"))
    state.holds_all_matches(P("b"))
    state.equivalence_classes()
    assert state.by_prop is before, \
        "by_prop tuple identity changed after queries"
    assert state.by_prop == before, \
        "by_prop contents changed after queries"


def test_holds_literal_matches_exactly_by_prop():
    """holds_literal matches by Prop equality only; no substitution.
    Even with a KNOWN identity, holds_literal(P(b)) does not find
    the literally-held P(a)."""
    state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a")),
            h(identity_prop("a", "b")),
        ),
    )
    assert state.holds_literal(P("a")) is not None
    assert state.holds_literal(P("b")) is None, \
        "holds_literal must not substitute"


# ============================================================================
# I4 — symmetry and transitivity
# ============================================================================

def test_substitution_forward():
    """Agent holds P(a) and identity(a, b) both KNOWN. holds(P(b))
    returns the Held for P(a)."""
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a")),
            h(identity_prop("a", "b")),
        ),
    )
    result = alice_state.holds(P("b"))
    assert result is not None, "substitution did not fire forward"
    assert result.prop == P("a"), \
        f"expected literal match P('a'); got {result.prop}"
    assert result.slot == Slot.KNOWN


def test_substitution_reverse():
    """Agent holds P(b) and identity(a, b) both KNOWN. holds(P(a))
    returns the Held for P(b). Symmetry per I4: the identity need
    not be asserted in both directions."""
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("b")),
            h(identity_prop("a", "b")),
        ),
    )
    result = alice_state.holds(P("a"))
    assert result is not None, "substitution did not fire in reverse"
    assert result.prop == P("b")


def test_substitution_transitive():
    """Agent holds P(a), identity(a, b), identity(b, c) all KNOWN.
    Query P(c) substitutes transitively through the chain and
    returns P(a)."""
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a")),
            h(identity_prop("a", "b")),
            h(identity_prop("b", "c")),
        ),
    )
    result = alice_state.holds(P("c"))
    assert result is not None, "transitive substitution did not fire"
    assert result.prop == P("a")


def test_equivalence_classes_computes_transitive_closure():
    """equivalence_classes returns the transitive closure of the
    agent's KNOWN identity propositions. Three chained identities
    produce one class of four elements."""
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(identity_prop("a", "b")),
            h(identity_prop("b", "c")),
            h(identity_prop("c", "d")),
        ),
    )
    classes = alice_state.equivalence_classes()
    assert len(classes) == 1, \
        f"expected one equivalence class; got {classes}"
    assert classes[0] == frozenset({"a", "b", "c", "d"})


# ============================================================================
# I7 — substitution fires only on KNOWN identities
# ============================================================================

def test_identity_at_believed_slot_does_not_substitute():
    """I7: an identity held at BELIEVED does not participate in
    substitution. Agent holds P(a) KNOWN and identity(a, b) as
    BELIEVED. Query P(b) returns None — substitution does not
    fire."""
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a"), slot=Slot.KNOWN),
            h(identity_prop("a", "b"), slot=Slot.BELIEVED),
        ),
    )
    assert alice_state.holds(P("b")) is None, \
        "BELIEVED identity fired substitution — violates I7"
    # But the literal P(a) is still there.
    assert alice_state.holds(P("a")) is not None
    # And the classes are empty (no KNOWN identity propositions).
    assert alice_state.equivalence_classes() == []


def test_identity_at_suspected_slot_does_not_substitute():
    """I7 corollary: SUSPECTED identity also does not substitute."""
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a")),
            h(identity_prop("a", "b"), slot=Slot.SUSPECTED),
        ),
    )
    assert alice_state.holds(P("b")) is None


def test_identity_at_gap_slot_does_not_substitute():
    """I7 corollary: GAP identity (the agent is aware of an open
    question about whether two entities are the same) also does
    not substitute."""
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a")),
            h(identity_prop("a", "b"), slot=Slot.GAP),
        ),
    )
    assert alice_state.holds(P("b")) is None


# ============================================================================
# Multi-match resolution — strongest slot, earliest by_prop order
# ============================================================================

def test_multi_match_returns_strongest_slot():
    """If multiple literal records match under substitution with
    different slots, holds(p) returns the strongest-slot record.
    KNOWN > BELIEVED > SUSPECTED > GAP."""
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a"), slot=Slot.BELIEVED),
            h(P("b"), slot=Slot.KNOWN),
            h(identity_prop("a", "b")),
        ),
    )
    result = alice_state.holds(P("a"))
    assert result is not None
    assert result.slot == Slot.KNOWN, \
        f"expected KNOWN (strongest); got {result.slot}"
    assert result.prop == P("b")


def test_multi_match_tiebreak_by_by_prop_order():
    """If multiple matches tie on slot, the earlier record in
    by_prop wins. by_prop order is the τ_a proxy (project_knowledge
    builds by_prop in τ_s, τ_a event order)."""
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a"), slot=Slot.KNOWN),  # earlier
            h(P("b"), slot=Slot.KNOWN),  # later
            h(identity_prop("a", "b")),
        ),
    )
    result = alice_state.holds(P("a"))
    assert result.prop == P("a"), \
        "tiebreak should prefer the earlier by_prop entry"


def test_holds_all_matches_returns_all_in_order():
    """holds_all_matches returns every substitution-equivalent Held,
    ordered by slot-strength then by_prop order."""
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a"), slot=Slot.BELIEVED),
            h(P("b"), slot=Slot.KNOWN),
            h(P("c"), slot=Slot.SUSPECTED),
            h(identity_prop("a", "b")),
            h(identity_prop("b", "c")),
        ),
    )
    matches = alice_state.holds_all_matches(P("a"))
    assert len(matches) == 3
    # KNOWN first, BELIEVED second, SUSPECTED third.
    assert matches[0].slot == Slot.KNOWN
    assert matches[0].prop == P("b")
    assert matches[1].slot == Slot.BELIEVED
    assert matches[1].prop == P("a")
    assert matches[2].slot == Slot.SUSPECTED
    assert matches[2].prop == P("c")


# ============================================================================
# Identity does not leak across agents (I2)
# ============================================================================

def test_identity_in_one_agents_state_does_not_apply_to_another():
    """I2: per-fold scoping. Alice's identity does not substitute
    for Bob. Bob must hold his own identity to get substitution."""
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a")),
            h(identity_prop("a", "b")),
        ),
    )
    bob_state = KnowledgeState(
        agent_id="bob",
        by_prop=(
            h(P("a")),  # no identity for Bob
        ),
    )
    assert alice_state.holds(P("b")) is not None
    assert bob_state.holds(P("b")) is None, \
        "Alice's identity propagated to Bob — violates I2"


# ============================================================================
# World-side substitution (world_holds)
# ============================================================================

def test_world_holds_substitutes_via_world_identity():
    """world_holds is substitution-aware over a world-state set.
    World identity props participate in substitution regardless of
    slot (world state has no slot concept; world props are
    assertions)."""
    world = {
        P("a"),
        identity_prop("a", "b"),
    }
    assert world_holds(P("b"), world) is True, \
        "world_holds did not substitute via world identity"
    assert world_holds(P("a"), world) is True
    assert world_holds(P("c"), world) is False


def test_world_holds_literal_is_strict_membership():
    """world_holds_literal is exactly Prop in set — no substitution,
    no aliasing."""
    world = {
        P("a"),
        identity_prop("a", "b"),
    }
    assert world_holds_literal(P("a"), world) is True
    assert world_holds_literal(P("b"), world) is False
    assert world_holds_literal(identity_prop("a", "b"), world) is True


# ============================================================================
# sternberg_curiosity stays literal — the explicit carve-out
# ============================================================================

def test_sternberg_curiosity_stays_literal_under_substitution():
    """The sketch's explicit decision: GAP slot is an authorial
    marker for acknowledged open questions. Substitution does not
    auto-fill acknowledged gaps. Even if substitution could derive
    an answer, the literal GAP record remains reportable."""
    from substrate import sternberg_curiosity
    alice_state = KnowledgeState(
        agent_id="alice",
        by_prop=(
            h(P("a"), slot=Slot.GAP),
            h(P("b"), slot=Slot.KNOWN),
            h(identity_prop("a", "b"), slot=Slot.KNOWN),
        ),
    )
    gaps = sternberg_curiosity(alice_state)
    gap_props = {g.prop for g in gaps}
    # The literal GAP record stays reported even though substitution
    # could derive the answer via P(b) + identity(a, b).
    assert P("a") in gap_props, \
        "literal GAP record should stay in curiosity report"


# ============================================================================
# Irony composes with substitution — the anagnorisis collapse pattern
# ============================================================================

def test_irony_fires_when_character_lacks_identity_reader_has_it():
    """Synthetic analog to Jocasta's pre-anagnorisis state. Reader
    holds identity(oedipus, stranger) KNOWN; character does not.
    Reader's substitution-aware state holds killed(oedipus, laius)
    via identity; character's does not. Irony fires."""
    # killed(stranger, laius) is what character holds literally.
    killed = Prop("killed", ("stranger", "laius"))
    # killed(oedipus, laius) is what the substitution derives.
    killed_oedipus = Prop("killed", ("oedipus", "laius"))

    reader_state = KnowledgeState(
        agent_id="reader",
        by_prop=(
            h(killed),  # reader heard the story
            h(identity_prop("oedipus", "stranger")),  # reader knows the identity
        ),
    )
    jocasta_state = KnowledgeState(
        agent_id="jocasta",
        by_prop=(
            h(killed),  # Jocasta heard the same story, lacks identity
        ),
    )
    # Both "hold" killed(stranger, laius); only reader "holds"
    # killed(oedipus, laius) — via substitution.
    assert reader_state.holds(killed_oedipus) is not None
    assert reader_state.holds(killed_oedipus).slot == Slot.KNOWN
    assert jocasta_state.holds(killed_oedipus) is None, \
        "Jocasta should not derive the identity without the assertion"


def test_irony_collapses_when_character_gains_identity():
    """Anagnorisis: once the character gains the identity at KNOWN,
    substitution fires and queries that previously missed now hit."""
    killed = Prop("killed", ("stranger", "laius"))
    killed_oedipus = Prop("killed", ("oedipus", "laius"))

    # Pre-realization: Jocasta lacks identity.
    pre = KnowledgeState(
        agent_id="jocasta",
        by_prop=(h(killed),),
    )
    assert pre.holds(killed_oedipus) is None

    # Post-realization: Jocasta now holds the identity (the same
    # literal set plus the identity proposition, as an identity-
    # assertion realization would produce per I5).
    post = KnowledgeState(
        agent_id="jocasta",
        by_prop=(
            h(killed),
            h(identity_prop("oedipus", "stranger")),
        ),
    )
    result = post.holds(killed_oedipus)
    assert result is not None, \
        "after realization, substitution should fire"
    assert result.slot == Slot.KNOWN
    assert result.prop == killed  # the literal match


# ============================================================================
# Branch scoping — identity follows B1 (sanity check via the raw helpers)
# ============================================================================

def test_build_equivalence_classes_ignores_non_identity_props():
    """The helper extracts classes from identity/2 props only. Other
    props with arity 2 or different predicates do not produce
    classes."""
    fake_identity = Prop("married", ("a", "b"))  # not identity
    classes = _build_equivalence_classes([fake_identity])
    assert classes == {}


def test_build_equivalence_classes_handles_reflexive_input():
    """identity(a, a) is a tautology; it produces a singleton class
    of {a} in the class map. The substrate does not raise; linting
    may flag it as pointless."""
    reflexive = Prop(IDENTITY_PREDICATE, ("a", "a"))
    classes = _build_equivalence_classes([reflexive])
    assert "a" in classes
    assert classes["a"] == frozenset({"a"})


# ============================================================================
# Runner
# ============================================================================

TESTS = [
    # I3 — literal-set preservation
    test_by_prop_is_unchanged_by_queries,
    test_holds_literal_matches_exactly_by_prop,
    # I4 — symmetry and transitivity
    test_substitution_forward,
    test_substitution_reverse,
    test_substitution_transitive,
    test_equivalence_classes_computes_transitive_closure,
    # I7 — KNOWN-only
    test_identity_at_believed_slot_does_not_substitute,
    test_identity_at_suspected_slot_does_not_substitute,
    test_identity_at_gap_slot_does_not_substitute,
    # Multi-match
    test_multi_match_returns_strongest_slot,
    test_multi_match_tiebreak_by_by_prop_order,
    test_holds_all_matches_returns_all_in_order,
    # I2 — per-fold scoping
    test_identity_in_one_agents_state_does_not_apply_to_another,
    # world_holds
    test_world_holds_substitutes_via_world_identity,
    test_world_holds_literal_is_strict_membership,
    # Sternberg stays literal
    test_sternberg_curiosity_stays_literal_under_substitution,
    # Irony composition
    test_irony_fires_when_character_lacks_identity_reader_has_it,
    test_irony_collapses_when_character_gains_identity,
    # Helpers
    test_build_equivalence_classes_ignores_non_identity_props,
    test_build_equivalence_classes_handles_reflexive_input,
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
