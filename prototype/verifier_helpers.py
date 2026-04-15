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

from substrate import Event
from dramatic import Throughline, ABSTRACT_THROUGHLINE_OWNERS
from lowering import cross_ref, LoweringStatus


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
