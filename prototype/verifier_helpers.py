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

from substrate import Event, KnowledgeEffect, WorldEffect
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
