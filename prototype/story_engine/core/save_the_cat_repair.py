"""
save_the_cat_repair.py — close the generate → evaluate → REPAIR loop for
the Save-the-Cat dialect (parity with `draft_repair.py` and
`dramatica_repair.py`).

The StC evaluator finds which of the fifteen canonical beats failed to read
in the prose. Unlike a Dramatica shape-drift (sealed at the ending) or an
Aristotelian recognition (one event), an StC beat loss is the MOST cleanly
localizable drift in the corpus: each beat is authored to a substrate
event (`sheet.beat_event_ids[slot]`), so a lost beat re-renders exactly the
scene that was supposed to carry it, with a directive naming the beat and
what fills it in this story.

Diffuse dimensions — `beat_order` (a property of the whole sequence),
`protagonist`, `b_story` — are NOT forced onto one scene; they are reported,
not localized, the same discipline the peer repairers keep.

`plan_repairs` is pure Python (offline-testable). Re-rendering reuses
`draft_repair.repair_scene(adapter=StcFrame(...))` — the generator is
dialect-agnostic. Convergence (`draft_convergence.converge`) is already
dependency-injected: wire the StC evaluate / plan / repair functions into it
and it iterates to a fidelity ceiling the same way the Aristotelian stack does.
"""

from __future__ import annotations

from story_engine.core.draft_repair import RepairDirective
from story_engine.core.save_the_cat import CANONICAL_BEAT_BY_SLOT


_BEAT_DIM_PREFIX = "beat["


def _slot_of_dimension(dim: str):
    """Extract the slot int from a 'beat[NN]' dimension label, or None."""
    if not dim.startswith(_BEAT_DIM_PREFIX) or not dim.endswith("]"):
        return None
    try:
        return int(dim[len(_BEAT_DIM_PREFIX):-1])
    except ValueError:
        return None


def _authored_beat_by_slot(sheet) -> dict:
    """First authored StcBeat per slot (matches StcFrame's bible choice)."""
    out: dict = {}
    for b in getattr(sheet, "beats", ()) or ():
        out.setdefault(b.slot, b)
    return out


def _target_event(slot: int, sheet, td: dict):
    """The substrate event that should carry this beat — the first authored
    event for the slot that is actually staged in the sjuzhet."""
    for eid in (getattr(sheet, "beat_event_ids", {}) or {}).get(slot, ()):
        if eid in td:
            return eid
    return None


def _beat_directive(slot: int, sheet) -> str:
    cb = CANONICAL_BEAT_BY_SLOT[slot]
    parts = [
        f"STRUCTURAL FIX — this scene must land the \"{cb.name}\" beat "
        f"(beat {slot} of 15) so a reader can recognize it.",
        f"What the beat does: {cb.purpose}.",
    ]
    authored = _authored_beat_by_slot(sheet).get(slot)
    if authored and getattr(authored, "description_of_change", ""):
        parts.append(f"In THIS story, that beat is: "
                     f"{authored.description_of_change}")
    if authored and getattr(authored, "advances", ()):
        strands = ", ".join(a.strand_id for a in authored.advances)
        if strands:
            parts.append(f"Advance: {strands}.")
    parts.append("Render the beat plainly enough that its function is "
                 "legible; do not bury it.")
    return "\n".join(parts)


def plan_repairs(report, sheet, sjuzhet) -> list:
    """Map an StcFidelityReport's LOST/DRIFTED beats to corrective
    re-renders. Each lost beat localizes to the substrate event authored to
    carry it. Diffuse dimensions (beat_order, protagonist, b_story) are not
    localized. Returns a possibly-empty, event-deduplicated list."""
    if not sjuzhet:
        return []
    td = {s.event_id: s.τ_d for s in sjuzhet}

    out: list = []
    seen = set()
    for f in getattr(report, "findings", []):
        slot = _slot_of_dimension(f.dimension)
        if slot is None or f.verdict not in ("lost", "drifted"):
            continue
        target = _target_event(slot, sheet, td)
        if target is None:
            continue
        key = (target, slot)
        if key in seen:
            continue
        seen.add(key)
        out.append(RepairDirective(
            event_id=target,
            dimension=f.dimension,
            authored=CANONICAL_BEAT_BY_SLOT[slot].name,
            instruction=_beat_directive(slot, sheet),
        ))
    return out
