"""
verifier_helpers.py — shared helpers for cross-boundary verifier
modules.

Extracted once the third encoding's verifier landed (REVIEW.md
Finding 3's trigger: "duplicated cross-boundary verifier logic that
will drift"). Previously the same five helpers lived in both
oedipus_verification.py and macbeth_verification.py with identical
bodies; macbeth_save_the_cat_verification.py had a trimmed subset.
This module holds the canonical definitions; each verifier module
imports what it needs.

Design: helpers take their collections explicitly (fabula,
throughlines, entities, lowerings) rather than closing over module-
level state. Each verifier module still owns its encoding-specific
imports — this module only holds the reusable logic. Dialect-
specific helpers (throughline / character / lowering walks) continue
to live here because the "cross-boundary verifier" pattern is where
they're reused; they're not general substrate utilities and don't
belong in substrate.py.
"""

from __future__ import annotations

from substrate import (
    Event, KnowledgeEffect, WorldEffect,
    IDENTITY_PREDICATE, in_scope, project_world, derive_all_world,
)
from dramatic import Throughline, ABSTRACT_THROUGHLINE_OWNERS
from lowering import cross_ref, LoweringStatus


# Role-name precedence for identifying an event's "primary actor" —
# the participant whose knowledge/agency the event centers. Ordered
# most-specific first; the first role present in an event's
# `participants` dict wins. Encodings that introduce new role names
# may extend this list, but the five below cover every event shape
# in the current Oedipus / Macbeth / Ackroyd encodings.
_PRIMARY_ACTOR_ROLES = ("killer", "speaker", "actor", "agent", "subject")


def find_substrate_event(event_id: str, fabula: tuple) -> Event:
    """Look up a substrate Event by id, or raise KeyError. Linear
    scan; fabulas are authored tuples and typically under 30 events,
    so no indexing overhead is warranted."""
    for e in fabula:
        if e.id == event_id:
            return e
    raise KeyError(f"no substrate event with id {event_id!r}")


def find_throughline(
    throughline_id: str, throughlines: tuple,
) -> Throughline:
    """Look up a Dramatic Throughline by id, or raise KeyError.
    Linear scan over the encoding's THROUGHLINES tuple."""
    for t in throughlines:
        if t.id == throughline_id:
            return t
    raise KeyError(f"no throughline with id {throughline_id!r}")


def is_abstract_throughline_owner(owner_id: str) -> bool:
    """True if the owner id is a Dramatic sentinel (none,
    the-situation, the-relationship) rather than a concrete
    Character id. Delegates to dramatic.ABSTRACT_THROUGHLINE_OWNERS
    as the single source of truth — previous hand-rolled copies of
    this check risked drifting from the canonical set."""
    return owner_id in ABSTRACT_THROUGHLINE_OWNERS


def event_participants_flat(event: Event) -> set:
    """Flatten an Event's participants dict into a set of entity ids.
    Substrate events sometimes use lists for participant slots (e.g.,
    'targets', 'killers'); this collapses those into a single flat
    set so callers can test entity-id membership directly."""
    out = set()
    for v in event.participants.values():
        if isinstance(v, str):
            out.add(v)
        elif isinstance(v, (list, tuple)):
            for e in v:
                if isinstance(e, str):
                    out.add(e)
    return out


def primary_actor_id(event: Event) -> str:
    """Return the entity id considered the event's primary actor,
    resolved via role-name precedence
    (`killer > speaker > actor > agent > subject`). Falls back to
    the first participant value if none of the privileged roles is
    present. Returns None if the event has no participants at all.

    For list-valued roles (e.g., `killers=[...]`) the first id in
    the list wins. Per EK2 in event-kind-taxonomy-sketch-01."""
    parts = event.participants or {}
    for role in _PRIMARY_ACTOR_ROLES:
        if role in parts:
            v = parts[role]
            if isinstance(v, (list, tuple)):
                return v[0] if v else None
            return v
    for v in parts.values():
        if isinstance(v, (list, tuple)):
            if v:
                return v[0]
        else:
            return v
    return None


def classify_event_action_shape(
    event: Event,
    *,
    agent_ids: frozenset = None,
) -> str:
    """Classify an Event as `"external"` or `"internal"` action-shaped
    per EK2 (event-kind-taxonomy-sketch-01).

    An event is **external-action-shaped** iff both hold:
      1. **Interpersonal.** Its participants include at least two
         distinct entity ids. If `agent_ids` is provided, only
         participants in that set count toward this clause — so a
         location or non-agent placeholder does not inflate the
         count. (Callers pass `agent_ids` built from their encoding's
         ENTITIES tuple; see the `agent_ids_from_entities` helper.)
      2. **Outward-effect.** Either a `WorldEffect` is present, or
         a `KnowledgeEffect` whose target agent is not the event's
         primary actor (so the event updates someone *else's*
         knowledge).

    If either clause fails, the event is **internal-state-shaped**.
    These two categories are exhaustive — EK2 defines internal-state
    as the complement of external-action.

    The classifier reads fold-visible structural features only. It
    does not branch on the event's `type` string, per EK1's
    discipline ("verifier classification reads fold-visible
    structure, not type strings"). Substrate-05 M1 routes modality
    with downstream fold consequence to effects; EK2 reads those
    effects and turns them into a yes/no answer."""
    parts = event.participants or {}
    all_ids = []
    for v in parts.values():
        if isinstance(v, (list, tuple)):
            all_ids.extend(x for x in v if isinstance(x, str))
        elif isinstance(v, str):
            all_ids.append(v)
    if agent_ids is not None:
        filtered = [i for i in all_ids if i in agent_ids]
    else:
        filtered = list(all_ids)
    interpersonal = len(set(filtered)) >= 2

    actor = primary_actor_id(event)
    has_world_effect = any(
        isinstance(ef, WorldEffect) for ef in event.effects
    )
    has_outward_knowledge = any(
        isinstance(ef, KnowledgeEffect) and ef.agent_id != actor
        for ef in event.effects
    )
    outward = has_world_effect or has_outward_knowledge

    if interpersonal and outward:
        return "external"
    return "internal"


# ----------------------------------------------------------------------------
# Arc-level limit-shape classifier — pressure-shape-taxonomy-sketch-01
# ----------------------------------------------------------------------------


def _effect_is_identity_proposition(effect) -> bool:
    """True if the effect asserts an identity/2 proposition on either
    the world or an agent's knowledge state."""
    if isinstance(effect, WorldEffect):
        return effect.prop.predicate == IDENTITY_PREDICATE
    if isinstance(effect, KnowledgeEffect):
        return effect.held.prop.predicate == IDENTITY_PREDICATE
    return False


def classify_arc_limit_shape(
    fabula,
    rules,
    canonical_branch,
    all_branches: dict,
) -> tuple:
    """Classify an arc's limit-pressure shape per LT2/LT3 in
    pressure-shape-taxonomy-sketch-01.

    Reads fold-visible fabula structure only (events, effects,
    rule-derivable world facts) — no type-string dispatch, per LT1.
    The three LT2 convergence signals are computed independently:

      1. **Retraction.** Count events with a `WorldEffect.asserts=False`
         that retracts a proposition previously asserted in the fabula.
      2. **Identity resolution.** Count events whose effects include
         at least one identity/2 proposition (either as a `WorldEffect`
         prop or as a `KnowledgeEffect.held.prop`).
      3. **Rule-derivable emergence.** Count world-facts derivable at
         the arc's end (via `derive_all_world`) whose proof kind is
         `"derived"` and which were not derivable from the empty
         initial world.

    Returns `(classification, strength, signals)` where:

      - `classification`: `"optionlock"` if ≥ 1 signal kind fires
        (LT2 disjunction); `"timelock-consistent"` if 0 signal kinds
        fire (LT3 complement-only detection).
      - `strength`: `min(1.0, signal_kinds / 3.0)`. 1 kind → 0.33,
        2 kinds → 0.67, 3 kinds → 1.0. Reports how many distinct
        convergence mechanisms the arc exhibits, not how many events
        fire each — multiplicity is reported in `signals`.
      - `signals`: tuple of `"<kind>:<count>"` tags documenting which
        mechanisms fired (e.g., `("retraction:1", "rule-emergence:4")`).
        Empty tuple for timelock-consistent arcs.

    LT3 asymmetry is deliberate: the Timelock side is weaker than the
    Optionlock side because substrate-05 has no scheduling vocabulary.
    The complement-only signal ("zero convergence") is consistent with
    Timelock but not affirmative evidence of it. Callers should apply
    LT5's disposition table (the author's DSP_limit declaration
    determines verdict polarity; the classifier only reports observed
    shape).
    """
    events = [
        e for e in fabula if in_scope(e, canonical_branch, all_branches)
    ]
    events_sorted = sorted(
        events, key=lambda e: (e.τ_s if e.τ_s is not None else 0, e.τ_a)
    )

    # Signal 1 — retractions that unwind a prior assertion.
    asserted_so_far: set = set()
    retraction_count = 0
    for e in events_sorted:
        for ef in e.effects:
            if not isinstance(ef, WorldEffect):
                continue
            if ef.asserts:
                asserted_so_far.add(ef.prop)
            else:
                if ef.prop in asserted_so_far:
                    retraction_count += 1
                    asserted_so_far.discard(ef.prop)

    # Signal 2 — identity-proposition effects (equivalence-class collapses).
    identity_resolution_count = sum(
        1 for e in events_sorted
        if any(_effect_is_identity_proposition(ef) for ef in e.effects)
    )

    # Signal 3 — rule-derivable compounds that emerge mid-arc. Strip
    # any authored fact whose predicate matches a rule head before
    # deriving, since N10 ("authored wins") hides rule firings behind
    # already-authored compounds. The substrate commitment is that rule
    # heads are dedicated compound predicates, so stripping by predicate
    # is safe here.
    rule_emergence_count = 0
    rules_tuple = tuple(rules)
    if events_sorted and rules_tuple:
        end_τ = max(e.τ_s for e in events_sorted if e.τ_s is not None)
        end_world = project_world(events_sorted, up_to_τ_s=end_τ)
        rule_head_preds = {r.head.predicate for r in rules_tuple}
        stripped_end_world = {
            p for p in end_world if p.predicate not in rule_head_preds
        }
        stripped_derivations = derive_all_world(
            stripped_end_world, rules_tuple,
        )
        rule_emergence_count = sum(
            1 for _p, proof in stripped_derivations.items()
            if proof.kind == "derived"
        )

    signals: list = []
    if retraction_count > 0:
        signals.append(f"retraction:{retraction_count}")
    if identity_resolution_count > 0:
        signals.append(f"identity-resolution:{identity_resolution_count}")
    if rule_emergence_count > 0:
        signals.append(f"rule-emergence:{rule_emergence_count}")

    kinds_firing = len(signals)
    if kinds_firing == 0:
        return ("timelock-consistent", 0.0, ())
    strength = min(1.0, kinds_firing / 3.0)
    return ("optionlock", strength, tuple(signals))


def dsp_limit_characterization_check(
    fabula,
    rules,
    canonical_branch,
    all_branches: dict,
    declared_choice: str,
) -> tuple:
    """Shared DSP_limit characterization check for the dramatica-
    complete → substrate verifier surface. Called by each encoding's
    verifier module with its own fabula/rules/canonical scope.

    Returns `(verdict, strength, comment)` per the LT5 disposition
    table in pressure-shape-taxonomy-sketch-01:

      - Optionlock declared + Optionlock-shaped → `APPROVED`.
      - Timelock declared + timelock-consistent → `NOTED`
        (consistent-but-not-affirmed; LT3's honest asymmetry).
      - Optionlock declared + no convergence signals → `NEEDS_WORK`.
      - Timelock declared + convergence signals present →
        `PARTIAL_MATCH` or `NEEDS_WORK` by signal strength.
      - Unknown declared_choice → `NOTED` with a diagnostic.

    `declared_choice` is the DSP_limit record's `.choice` value
    (e.g., `Limit.OPTIONLOCK.value` or `Limit.TIMELOCK.value`)."""
    classification, strength, signals = classify_arc_limit_shape(
        fabula, rules, canonical_branch, all_branches,
    )
    declared_normalized = (declared_choice or "").lower()
    signal_text = (
        ", ".join(signals) if signals else "no convergence signals"
    )

    # Import verdict constants lazily to keep verifier_helpers' import
    # graph narrow (verification.py imports verifier_helpers indirectly
    # via the verifier modules; avoid a cycle).
    from verification import (
        VERDICT_APPROVED, VERDICT_NEEDS_WORK,
        VERDICT_PARTIAL_MATCH, VERDICT_NOTED,
    )

    if declared_normalized == "optionlock":
        if classification == "optionlock":
            return (
                VERDICT_APPROVED, strength,
                f"DSP_limit=Optionlock declared; substrate exhibits "
                f"convergence shape ({signal_text}). Arc ends because "
                f"alternatives are eliminated (LT2). Strength "
                f"{strength:.2f} reflects {len(signals)}/3 signal "
                f"kinds firing.",
            )
        return (
            VERDICT_NEEDS_WORK, 0.0,
            f"DSP_limit=Optionlock declared, but substrate shows no "
            f"convergence signals (no retractions, no identity "
            f"resolutions, no rule-derivable emergences). LT2 cannot "
            f"confirm the declared pressure shape; either the "
            f"substrate is missing a convergence mechanism or the "
            f"DSP choice is mislabeled.",
        )
    if declared_normalized == "timelock":
        if classification == "timelock-consistent":
            return (
                VERDICT_NOTED, None,
                f"DSP_limit=Timelock declared; substrate shows no "
                f"convergence signals (consistent with Timelock). "
                f"LT3 is complement-only and does NOT affirmatively "
                f"detect scheduling — substrate-05 has no scheduling "
                f"vocabulary yet. This is LT3's honest asymmetry, not "
                f"a verifier weakness on this encoding.",
            )
        # Timelock-declared but substrate shows convergence.
        if strength >= 0.5:
            return (
                VERDICT_NEEDS_WORK, 1.0 - strength,
                f"DSP_limit=Timelock declared, but substrate exhibits "
                f"strong convergence shape ({signal_text}). The arc "
                f"looks Optionlock-shaped in substrate. Either the "
                f"DSP choice needs revisiting or the subplot-only "
                f"convergence hypothesis in sketch OQ3 applies.",
            )
        return (
            VERDICT_PARTIAL_MATCH, 1.0 - strength,
            f"DSP_limit=Timelock declared; substrate shows mild "
            f"convergence signals ({signal_text}). May be subplot-only "
            f"convergence in an otherwise schedule-driven arc (LT2 "
            f"OQ3). Worth the author's attention.",
        )
    return (
        VERDICT_NOTED, None,
        f"DSP_limit choice {declared_choice!r} is not recognized "
        f"(expected 'optionlock' or 'timelock'); classifier observed "
        f"{classification} with {signal_text}.",
    )


def agent_ids_from_entities(entities: tuple) -> frozenset:
    """Build the `agent_ids` frozenset the EK2 classifier expects,
    from an encoding's `ENTITIES` tuple. Selects entities whose
    `kind == "agent"` — excluding locations, objects, and abstract
    placeholders. Used by cross-boundary verifiers; each encoding
    passes its own ENTITIES in."""
    return frozenset(e.id for e in entities if e.kind == "agent")


def entity_id_for_character(
    character_id: str,
    lowerings: tuple,
    entities: tuple,
) -> str:
    """Walk `lowerings` to find the substrate Entity id that the
    given Dramatic Character lowers to. Returns the entity id string,
    or None if no ACTIVE Lowering exists or the lowering targets
    aren't substrate Entities.

    `entities` disambiguates Entity ids from Event ids — both live in
    the 'substrate' dialect namespace, but Character Lowerings should
    target Entities. A lowering whose lower_records name substrate
    Events (not Entities) is skipped, so a misauthored Lowering
    pointing a Character at an Event doesn't silently pass.
    """
    char_ref = cross_ref("dramatic", character_id)
    for lw in lowerings:
        if lw.upper_record != char_ref:
            continue
        if lw.status != LoweringStatus.ACTIVE:
            continue
        for lr in lw.lower_records:
            if lr.dialect == "substrate":
                if any(e.id == lr.record_id for e in entities):
                    return lr.record_id
    return None
