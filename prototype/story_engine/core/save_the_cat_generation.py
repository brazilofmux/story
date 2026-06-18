"""
save_the_cat_generation.py — the Save-the-Cat dialect adapter (the THIRD
dialect through the generator).

A peer to `aristotelian_generation.AristotelianFrame` and
`dramatica_generation.DramaticaFrame`. Widens the proven dialect-agnostic
surface from two dialects to three: a third, structurally-alien
vocabulary — the commercial-screenplay 15-beat sheet (Opening Image,
Catalyst, Break Into Two, Midpoint, All Is Lost, Finale, Final Image) and
the A/B strands — driving the same generator with zero changes to it.

The generator stays dialect-clean: it imports no dialect and defines only
the neutral `DialectFrame` interface; this module is allowed to know both
the frame interface and the Save-the-Cat dialect, and is passed in via
`generate_draft(adapter=...)`.

Per-scene beat assignment is AUTHORED (a beat → substrate-event mapping),
read from the encoding — not guessed from a scene's proportional page.
When no mapping is given the frame falls back to a page-proportion split
and SAYS SO in the bible (the same honesty discipline as the Dramatica
act fallback).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from story_engine.core.draft_generator import DialectFrame
from story_engine.core.save_the_cat import CANONICAL_BEAT_BY_SLOT


@dataclass
class StcStorySheet:
    """The generatively-useful Save-the-Cat overlay: the authored beats,
    the strands, the characters, and (optionally) the authored
    beat→substrate-event mapping. A caller assembles this from a
    `*_save_the_cat` encoding's exports."""
    title: str
    action_summary: str
    beats: tuple            # StcBeat (authored, one+ per slot)
    strands: tuple = ()     # StcStrand (A / B story)
    characters: tuple = ()  # StcCharacter
    beat_event_ids: dict = field(default_factory=dict)  # {slot: (event_id,)}


class StcFrame(DialectFrame):
    """Surfaces a Save-the-Cat beat sheet for the renderer."""

    def __init__(self, sheet: StcStorySheet, sjuzhet):
        self.overlay = sheet
        self.sheet = sheet
        self._beat_by_slot = {}
        for b in sheet.beats:
            # first authored beat per slot wins for the bible description
            self._beat_by_slot.setdefault(b.slot, b)

        # event → beat slot: prefer the authored mapping; else page-proportion.
        self._beats_authored = bool(sheet.beat_event_ids)
        self._beat_of: dict = {}
        self._unplaced: list = []
        if self._beats_authored:
            for slot, event_ids in sheet.beat_event_ids.items():
                for eid in event_ids:
                    self._beat_of[eid] = int(slot)
        ordered = sorted(sjuzhet, key=lambda s: s.τ_d)
        if not self._beats_authored:
            # map each scene to the nearest authored slot by proportional page
            slots = sorted(self._beat_by_slot)
            n = max(1, len(ordered))
            for i, e in enumerate(ordered):
                # scene's position 0..1 → a slot among those authored
                idx = min(len(slots) - 1, i * len(slots) // n)
                self._beat_of[e.event_id] = slots[idx] if slots else 0
        else:
            self._unplaced = [
                e.event_id for e in ordered if e.event_id not in self._beat_of
            ]

    # -- bible -------------------------------------------------------------

    def bible_sections(self, *, name_map) -> list:
        s = self.sheet
        lines = ["\n## Save-the-Cat beat sheet (the 15-beat structure this "
                 "renders)"]
        if s.action_summary:
            lines.append(s.action_summary)
        if self._beats_authored and not self._unplaced:
            src = "every scene below is mapped to its beat (AUTHORED)"
        elif self._beats_authored:
            src = (f"beats authored, except {len(self._unplaced)} scene(s) "
                   f"placed by page position")
        else:
            src = ("NOTE: scene→beat assignment is APPROXIMATE — inferred "
                   "from page position, not authored")
        lines.append(f"\nThe fifteen beats in order ({src}):")
        for slot in range(1, 16):
            cb = CANONICAL_BEAT_BY_SLOT[slot]
            authored = self._beat_by_slot.get(slot)
            note = (authored.description_of_change
                    if authored and authored.description_of_change
                    else cb.purpose)
            lines.append(f"- [{slot}] {cb.name}: {note}")

        if s.strands:
            lines.append("\n## Strands (the A and B stories — weave both)")
            for st in s.strands:
                kind = st.kind.value if hasattr(st.kind, "value") else st.kind
                desc = getattr(st, "description", "") or ""
                lines.append(f"- {kind}: {desc}")

        if s.characters:
            lines.append("\n## Characters and their roles")
            for c in s.characters:
                roles = ", ".join(getattr(c, "role_labels", ()) or ())
                lines.append(f"- {c.name}"
                             + (f" ({roles})" if roles else ""))
        return lines

    # -- per scene ---------------------------------------------------------

    def scene_lines(self, *, entry, name_map) -> list:
        slot = self._beat_of.get(entry.event_id)
        if not slot:
            return []
        cb = CANONICAL_BEAT_BY_SLOT.get(slot)
        if cb is None:
            return []
        out = [f"** THIS IS THE \"{cb.name}\" BEAT (beat {slot} of 15) — "
               f"{cb.purpose} **"]
        authored = self._beat_by_slot.get(slot)
        if authored and authored.description_of_change:
            out.append(f"In this story, that beat is: "
                       f"{authored.description_of_change}")
        if authored and getattr(authored, "advances", ()):
            strands = ", ".join(a.strand_id for a in authored.advances)
            if strands:
                out.append(f"Advances: {strands}")
        return out
