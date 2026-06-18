"""
dramatic_generation.py — the (general) DRAMATIC dialect adapter.

The FOURTH frame, and structurally the PARENT of the Dramatica one.
Where `dramatica_generation.DramaticaFrame` reads the heaviest Template
(the full storyform), this reads the general Dramatic dialect with a
MINIMAL template (three-actor: Hero / Obstacle / Helper). The
generatively-useful core of the parent dialect is lean: whose story it
is (the character functions), what the story ARGUES (the thematic
Argument — a premise against its counter), and what is at STAKE — plus
the throughlines that carry the argument. No signposts, no acts, no
beat sheet.

Same seam as every other frame: the generator imports no dialect; a
caller builds a `DramaticFrame` and passes it via
`generate_draft(adapter=...)`. This module is allowed to know both the
frame interface and the Dramatic dialect.

Per-scene marks surface the FUNCTIONS present in the beat — when the
Hero and the Obstacle share a scene it is a confrontation; when a Helper
is with the Hero it is aid — read from the substrate event's
participants against the character→function map. That is the whole
minimal apparatus: who is in the room, and what role they play in the
argument.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from story_engine.core.draft_generator import DialectFrame


@dataclass
class DramaticStory:
    """The generatively-useful Dramatic overlay: the Story root, its
    Argument(s), Throughlines, Characters (with function labels), and
    Stakes. A caller assembles this from a `*_dramatic*` encoding."""
    title: str
    action_summary: str
    template_id: str
    characters: tuple = ()    # dramatic.Character
    arguments: tuple = ()      # dramatic.Argument
    throughlines: tuple = ()   # dramatic.Throughline
    stakes: tuple = ()         # dramatic.Stakes


def _flatten(values):
    out = []
    for v in values:
        if isinstance(v, (list, tuple)):
            out.extend(v)
        else:
            out.append(v)
    return out


class DramaticFrame(DialectFrame):
    """Surfaces a general-Dramatic overlay (minimal template) for the
    renderer: the thematic argument, the character functions, the
    stakes, the throughlines; and per scene, which functions are
    present."""

    def __init__(self, story: DramaticStory, fabula):
        self.overlay = story
        self.story = story
        # character id → its (first) function label
        self._func_of = {}
        for c in story.characters:
            labels = getattr(c, "function_labels", ()) or ()
            if labels:
                self._func_of[c.id] = labels[0]
        self._name_of = {c.id: getattr(c, "name", c.id) for c in story.characters}
        # event id → set of participant ids (flattened; roles may be lists)
        self._participants_of = {}
        for e in fabula:
            self._participants_of[e.id] = set(
                _flatten(getattr(e, "participants", {}).values()))

    def _cast_by_function(self):
        out = {}
        for cid, fn in self._func_of.items():
            out.setdefault(fn, []).append(self._name_of.get(cid, cid))
        return out

    # -- bible -------------------------------------------------------------

    def bible_sections(self, *, name_map) -> list:
        s = self.story
        lines = ["\n## Dramatic structure (the general dialect — minimal "
                 f"'{s.template_id}' template)"]
        if s.action_summary:
            lines.append(s.action_summary)

        # The thematic Argument — what the story is arguing.
        if s.arguments:
            lines.append("\n## The argument (what this story is arguing)")
            for a in s.arguments:
                direction = getattr(a, "resolution_direction", "")
                direction = getattr(direction, "value", direction)
                lines.append(f"- The story {str(direction).upper()}S this "
                             f"claim: {getattr(a, 'premise', '')}")
                cp = getattr(a, "counter_premise", None)
                if cp:
                    lines.append(f"  ...against the counter-claim it must "
                                 f"answer: {cp}")
            lines.append("Let the whole draft argue this — every scene is a "
                         "move in it, for or against.")

        # The cast by function (the minimal template).
        cast = self._cast_by_function()
        if cast:
            lines.append("\n## The cast by function (who plays what in the "
                         "argument)")
            for fn in ("Hero", "Protagonist", "Obstacle", "Antagonist",
                       "Helper", "voice"):
                if fn in cast:
                    lines.append(f"- {fn}: {', '.join(cast[fn])}")
            for fn, names in cast.items():
                if fn not in ("Hero", "Protagonist", "Obstacle", "Antagonist",
                              "Helper", "voice"):
                    lines.append(f"- {fn}: {', '.join(names)}")

        # The throughlines (the roles within the argument).
        if s.throughlines:
            lines.append("\n## Throughlines (the strands that carry the "
                         "argument)")
            for t in s.throughlines:
                subj = getattr(t, "subject", "")
                role = getattr(t, "role_label", "")
                sides = [getattr(getattr(ac, "side", ""), "value",
                                 getattr(ac, "side", ""))
                         for ac in getattr(t, "argument_contributions", ())]
                tag = f" [{', '.join(sides)}]" if sides else ""
                lines.append(f"- {role}: {subj}{tag}")

        # The stakes.
        if s.stakes:
            lines.append("\n## Stakes (what is at risk, what is to gain)")
            for st in s.stakes:
                lines.append(f"- AT RISK: {getattr(st, 'at_risk', '')}")
                lines.append(f"  TO GAIN: {getattr(st, 'to_gain', '')}")
        return lines

    # -- per scene ---------------------------------------------------------

    def scene_lines(self, *, entry, name_map) -> list:
        present = self._participants_of.get(entry.event_id, set())
        funcs = [(self._func_of[p], self._name_of.get(p, p))
                 for p in present if p in self._func_of]
        if not funcs:
            return []
        who = "; ".join(f"{fn} ({nm})" for fn, nm in funcs)
        out = [f"Functions present in this beat: {who}"]
        labels = {fn for fn, _ in funcs}
        if labels & {"Hero", "Protagonist"} and labels & {"Obstacle",
                                                           "Antagonist"}:
            out.append("The Hero and the Obstacle share this beat — it is a "
                       "CONFRONTATION; let the argument's two sides collide "
                       "here.")
        elif labels & {"Hero", "Protagonist"} and "Helper" in labels:
            out.append("A Helper is with the Hero here — render the aid (or "
                       "its cost) the Hero's quest needs.")
        return out
