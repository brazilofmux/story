"""
oedipus_verification.py — first concrete cross-boundary verifier
runs against the Oedipus encoding.

Imports from substrate.py + oedipus.py + dramatic.py +
oedipus_dramatic.py + lowering.py + oedipus_lowerings.py +
verification.py simultaneously. Like oedipus_lowerings.py, this
module is connective tissue — it brings dialects together to do
work neither dialect could do alone.

Scope of this first pass: one Characterization check on
T_mc_oedipus, the main-character Throughline. The check verifies
that the substrate events lowered from T_mc_oedipus actually have
Oedipus (the entity that C_oedipus lowers to) as a participant.
A "main-character" Throughline whose lowered events do not center
on the owner is mis-classified or has the wrong Lowering set;
either way the verifier should flag it. For Oedipus, all 10
events on the L_mc_throughline binding have Oedipus as a
participant, so we expect verdict=approved with match_strength=1.0.

Future verification work (other primitives, other checks, other
encodings) extends this pattern: each encoding pairs its dialect
records with check functions, and the verifier orchestrator runs
them and emits observations.
"""

from __future__ import annotations

# Substrate-side imports (for resolving Entity ids and Event
# participants).
from substrate import Entity, Event
from oedipus import FABULA, ENTITIES

# Dramatic-side imports (for resolving Throughline owners and
# Character ids).
from dramatic import Throughline, Character
from oedipus_dramatic import THROUGHLINES, CHARACTERS, STORY

# Lowering-side imports (for resolving owner Characters to
# substrate Entities).
from lowering import (
    CrossDialectRef, cross_ref,
    Lowering, LoweringStatus, by_status,
)
from oedipus_lowerings import LOWERINGS

# Verifier primitive.
from verification import (
    VerificationReview, StructuralAdvisory,
    verify_characterization, run_characterization_checks,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH,
    VERDICT_NOTED,
    reviews_only, group_by_verdict,
)


# ============================================================================
# Helpers
# ============================================================================


def _throughline(throughline_id: str) -> Throughline:
    for t in THROUGHLINES:
        if t.id == throughline_id:
            return t
    raise KeyError(throughline_id)


def _substrate_event(event_id: str) -> Event:
    for e in FABULA:
        if e.id == event_id:
            return e
    raise KeyError(event_id)


def _is_abstract_owner(owner_id: str) -> bool:
    """Sentinel owner ids per dramatic.ABSTRACT_THROUGHLINE_OWNERS."""
    return owner_id in ("none", "the-situation", "the-relationship")


def _entity_id_for_character(character_id: str, lowerings: tuple) -> str:
    """Walk Lowerings to find the substrate Entity id that the given
    Dramatic Character lowers to. Returns the entity id string, or
    None if no ACTIVE Lowering exists or the lowering targets aren't
    substrate Entities."""
    char_ref = cross_ref("dramatic", character_id)
    for lw in lowerings:
        if lw.upper_record != char_ref:
            continue
        if lw.status != LoweringStatus.ACTIVE:
            continue
        for lr in lw.lower_records:
            if lr.dialect == "substrate":
                # Verify it's an Entity (vs. an Event); Entity ids
                # are lowercase agent names without an E_ prefix.
                if any(e.id == lr.record_id for e in ENTITIES):
                    return lr.record_id
    return None


def _event_participants_flat(event: Event) -> set:
    """Flatten an Event's participants dict into a set of entity ids.
    Substrate events sometimes use lists for participants like
    'targets'; this collapses those."""
    out = set()
    for v in event.participants.values():
        if isinstance(v, str):
            out.add(v)
        elif isinstance(v, (list, tuple)):
            for e in v:
                if isinstance(e, str):
                    out.add(e)
    return out


# ============================================================================
# Characterization check: main-character Throughline
# ============================================================================


def main_character_throughline_check(
    upper_ref: CrossDialectRef,
    lower_refs: tuple,
) -> tuple:
    """Characterization check for a Throughline whose role_label is
    'main-character'. The check verifies that the owner Character's
    lowered substrate Entity appears as a participant in most/all of
    the lowered substrate events.

    Returns (verdict, match_strength, comment). Verdicts:
      - 'approved' if ≥95% of events have the owner as participant
      - 'partial-match' if 50%-94%
      - 'needs-work' if <50%
      - 'noted' if the check can't be evaluated (no owner, no
        Entity Lowerings, no event lower records)
    """
    throughline = _throughline(upper_ref.record_id)

    if throughline.role_label != "main-character":
        return (
            VERDICT_NOTED,
            None,
            (f"check applies to main-character Throughlines; "
             f"this one is {throughline.role_label!r}"),
        )

    owner_chars = [
        o for o in throughline.owners if not _is_abstract_owner(o)
    ]
    if not owner_chars:
        return (
            VERDICT_NOTED,
            None,
            "no concrete owner Characters; check skipped",
        )

    owner_entity_ids = []
    for char_id in owner_chars:
        entity_id = _entity_id_for_character(char_id, LOWERINGS)
        if entity_id is not None:
            owner_entity_ids.append(entity_id)

    if not owner_entity_ids:
        return (
            VERDICT_NOTED,
            None,
            (f"owner Characters {owner_chars} have no ACTIVE "
             f"Character→Entity Lowerings; check cannot evaluate"),
        )

    event_lower_refs = [
        lr for lr in lower_refs
        if lr.dialect == "substrate"
        and any(e.id == lr.record_id for e in FABULA)
    ]
    if not event_lower_refs:
        return (
            VERDICT_NOTED,
            None,
            "no substrate events in lower side",
        )

    matched = 0
    for lr in event_lower_refs:
        event = _substrate_event(lr.record_id)
        participants = _event_participants_flat(event)
        if any(eid in participants for eid in owner_entity_ids):
            matched += 1

    strength = matched / len(event_lower_refs)
    if strength >= 0.95:
        verdict = VERDICT_APPROVED
    elif strength >= 0.5:
        verdict = VERDICT_PARTIAL_MATCH
    else:
        verdict = VERDICT_NEEDS_WORK

    comment = (
        f"main-character Throughline {throughline.id!r}: owner "
        f"Character(s) {owner_chars} lower to substrate "
        f"Entity(ies) {owner_entity_ids}; "
        f"{matched}/{len(event_lower_refs)} of the "
        f"Lowered substrate events have at least one owner Entity "
        f"as a participant"
    )
    return (verdict, strength, comment)


# ============================================================================
# Driver — run the check
# ============================================================================


# The set of (upper_record_id, upper_dialect, check_fn) triples this
# encoding's verification module exposes. A future orchestrator could
# enumerate per-record automatically based on
# dramatic.COUPLING_DECLARATIONS; for now, this is hand-wired.

CHARACTERIZATION_CHECKS = (
    ("T_mc_oedipus", "dramatic", main_character_throughline_check),
)


def run() -> tuple:
    """Run all characterization checks for the Oedipus encoding.
    Returns the verifier output tuple (mix of VerificationReview
    and StructuralAdvisory)."""
    return run_characterization_checks(
        CHARACTERIZATION_CHECKS,
        LOWERINGS,
        reviewer_id="verifier:dramatic-substrate-characterization",
        reviewed_at_τ_a=300,
    )


if __name__ == "__main__":
    results = run()
    print(f"Characterization verifier: {len(results)} results")
    print()
    for r in results:
        if isinstance(r, VerificationReview):
            print(f"  REVIEW [{r.verdict}] target={r.target_record}")
            if r.match_strength is not None:
                print(f"    match_strength: {r.match_strength:.2f}")
            print(f"    anchor_τ_a: {r.anchor_τ_a}")
            print(f"    comment: {r.comment}")
        elif isinstance(r, StructuralAdvisory):
            print(f"  ADVISORY [{r.severity}] scope={r.scope}")
            print(f"    {r.comment}")
        print()
