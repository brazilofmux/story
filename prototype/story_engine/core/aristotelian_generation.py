"""
aristotelian_generation.py — the Aristotelian dialect adapter for the
generator.

A peer to `dramatica_generation.DramaticaFrame`. The generator
(`draft_generator.py`) defines only the neutral `DialectFrame` interface
and privileges no dialect; this module ships the Aristotelian frame,
which reads a tragic-arc overlay (an ArMythos) and surfaces it as bible
sections + per-scene structural marks (the phases, the peripeteia and
anagnorisis, the secondary reversals, the staggered-recognition chain
incl. anti-recognitions, the pathos-centre, the tragic heroes and their
hamartia).

It reads the overlay purely by duck-typing (getattr) — it does not even
import the Aristotelian dialect core; it only knows the ArMythos shape.
The generator's `mythos=` parameter routes here by default (an ArMythos
is an Aristotelian overlay), but the routing lives in the generator's
`_resolve_frame`, not in any privileged base class.
"""

from __future__ import annotations

from story_engine.core.draft_generator import DialectFrame, _char_name


class AristotelianFrame(DialectFrame):
    """Surfaces a tragic-arc overlay (ArMythos-shaped) for the renderer."""

    def __init__(self, overlay):
        super().__init__(overlay)
        # Per-scene lookups precomputed from the overlay.
        self._phase_of: dict = {}
        self._peri_id = None
        self._anag_id = None
        self._secondary: set = set()
        self._chain_by_event: dict = {}
        m = overlay
        if m is not None:
            for ph in getattr(m, "phases", ()) or ():
                for eid in getattr(ph, "scope_event_ids", ()):
                    self._phase_of[eid] = getattr(ph, "role", None)
            self._peri_id = getattr(m, "peripeteia_event_id", None)
            self._anag_id = getattr(m, "anagnorisis_event_id", None)
            self._secondary = set(
                getattr(m, "secondary_peripeteia_event_ids", ()) or ())
            for s in getattr(m, "anagnorisis_chain", ()) or ():
                eid = getattr(s, "event_id", None)
                if eid:
                    self._chain_by_event[eid] = s

    def bible_sections(self, *, name_map) -> list:
        m = self.overlay
        lines: list = []
        if m is None:
            return lines
        lines.append("\n## Dramatic arc")
        if getattr(m, "action_summary", ""):
            lines.append(m.action_summary)
        if self._peri_id:
            lines.append(f"\n- PERIPETEIA (the reversal) lands at: "
                         f"{self._peri_id}")
        if self._anag_id:
            lines.append(f"- ANAGNORISIS (the recognition) lands at: "
                         f"{self._anag_id}")
        secondary = getattr(m, "secondary_peripeteia_event_ids", ()) or ()
        if secondary:
            lines.append(f"- SECONDARY REVERSALS (other arcs falling): "
                         f"{', '.join(secondary)}")
        chain = getattr(m, "anagnorisis_chain", ()) or ()
        if chain:
            lines.append("\n## Staggered recognitions (the chain)")
            for step in chain:
                who = _char_name(getattr(step, "character_ref_id", ""),
                                 m, name_map)
                qual = getattr(step, "anagnorisis_qualifier", "") or ""
                tag = ""
                if qual == "anti":
                    tag = " — an ANTI-recognition: real, but arrives too " \
                          "late to change anything"
                elif qual == "partial":
                    tag = " — a PARTIAL recognition (incomplete grasp)"
                lines.append(
                    f"- {who} recognizes at {getattr(step, 'event_id', '?')}"
                    f"{tag}")
        pathos = getattr(m, "pathos_character_ref_ids", ()) or ()
        if pathos:
            names = ", ".join(_char_name(p, m, name_map) for p in pathos)
            lines.append(
                f"\n## Pathos-centre (the play's pity-and-fear lives here)\n"
                f"- {names} — render their suffering as the emotional centre, "
                f"even where they are not the one who comes to knowledge")
        chars = getattr(m, "characters", ()) or ()
        heroes = [c for c in chars if getattr(c, "is_tragic_hero", False)]
        if heroes:
            lines.append("\n## Tragic hero(es) and the error that undoes them")
            for c in heroes:
                ham = getattr(c, "hamartia_text", None)
                base = getattr(c, "name", c.id)
                if getattr(c, "pathos_carrier", False):
                    base += " (also the pathos-centre)"
                lines.append(f"- {base}: {ham}" if ham else f"- {base}")
        phases = getattr(m, "phases", ()) or ()
        if phases:
            lines.append("\n## Phase structure")
            for ph in phases:
                role = getattr(ph, "role", "?")
                lines.append(f"- {role}: {', '.join(ph.scope_event_ids)}")
        return lines

    def scene_lines(self, *, entry, name_map) -> list:
        m = self.overlay
        out: list = []
        eid = entry.event_id
        phase_role = self._phase_of.get(eid)
        if phase_role:
            out.append(f"Phase: {phase_role}")
        marks = []
        if eid == self._peri_id:
            marks.append("THIS IS THE PERIPETEIA (the reversal)")
        if eid == self._anag_id:
            marks.append("THIS IS THE ANAGNORISIS (the recognition)")
        if eid in self._secondary:
            marks.append("THIS IS A SECONDARY REVERSAL (another arc falling "
                         "here — give it weight, but not the main reversal's)")
        chain_step = self._chain_by_event.get(eid)
        if chain_step is not None:
            who = _char_name(getattr(chain_step, "character_ref_id", ""),
                             m, name_map)
            qual = getattr(chain_step, "anagnorisis_qualifier", "") or ""
            if qual == "anti":
                marks.append(f"{who} RECOGNIZES here — but it is an "
                             f"ANTI-recognition: the truth lands too late to "
                             f"change the outcome (render the bitterness of "
                             f"recognition-without-remedy)")
            elif qual == "partial":
                marks.append(f"{who} PARTIALLY recognizes here (an incomplete "
                             f"grasp of the truth)")
            else:
                marks.append(f"{who} RECOGNIZES here (a staggered recognition "
                             f"in the chain)")
        if marks:
            out.append("** " + "; ".join(marks) + " **")
        return out
