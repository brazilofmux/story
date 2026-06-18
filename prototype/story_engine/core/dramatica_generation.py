"""
dramatica_generation.py — the Dramatica dialect adapter for the generator.

Proves the founding plural-dialect thesis: the generator
(`draft_generator.py`) is dialect-agnostic by construction (it imports no
dialect; it consumes a `DialectFrame`). This module is the SECOND frame —
it reads a Dramatica storyform (four throughlines, the signpost act-
progression, the six dynamics, the story goal) and surfaces it as bible
sections + per-scene marks, exactly as the default tragic-arc frame does
for an ArMythos.

The generator stays clean: IT does not import this module; a CALLER that
wants Dramatica generation builds a `DramaticaFrame` and passes it as
`generate_draft(adapter=...)`. This file is allowed to know about both
the generator's frame interface and the Dramatica dialect.

What this unlocks: story types Aristotle's tragic vocabulary cannot
represent. Rocky's ending is Outcome=Failure × Judgment=Good — a
*personal triumph*, not a tragedy. The frame surfaces that shape so the
renderer writes a man who loses the fight and wins everything else.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from story_engine.core.draft_generator import DialectFrame


# ----------------------------------------------------------------------------
# Storyform bundle (what the frame reads)
# ----------------------------------------------------------------------------

@dataclass
class DramaticaStoryform:
    """The generatively-useful subset of a Dramatica storyform. A caller
    assembles this from a `*_dramatica_complete` encoding's exports and
    hands it to DramaticaFrame."""
    title: str
    action_summary: str
    domain_assignments: tuple   # DomainAssignment (4)
    signposts: tuple            # Signpost (16)
    dynamics: tuple             # DynamicStoryPoint (6)
    story_goal: str
    story_consequence: str
    canonical_ending: str = ""
    # Authored act structure: {act_position (1..4): (event_id, ...)}. When
    # provided, the frame reads the TRUE act boundaries instead of guessing
    # them from sjuzhet position. Empty = no authoring; the frame falls back
    # to a positional split AND says so in the bible (no silent heuristic).
    act_event_ids: dict = field(default_factory=dict)


# Renderer-facing glosses for the Dramatica vocabulary (theory labels →
# plain guidance the prose model can act on).
_PERSPECTIVE = {
    "overall": ("Overall Story", "the objective trouble everyone is caught in"),
    "mc": ("Main Character", "the protagonist's own throughline — their "
           "personal angle on the trouble"),
    "ic": ("Influence Character", "the character who pressures the Main "
           "Character to change (or to hold steady)"),
    "rel": ("Relationship Story", "the central relationship that grows or "
            "strains as the story moves"),
}

_DOMAIN_GLOSS = {
    "situation": "a fixed external SITUATION (the trouble is a circumstance "
                 "everyone is stuck in)",
    "activity": "an ACTIVITY (the trouble is in what people are doing — "
                "action, effort, doing)",
    "fixed-attitude": "a FIXED ATTITUDE (the trouble is a settled state of "
                      "mind that will not bend)",
    "manipulation": "MANIPULATION (the trouble is in how people are worked "
                    "on, conned, or made to change)",
}

_DSP_GLOSS = {
    "resolve": ("Resolve", {
        "steadfast": "the Main Character does NOT change — they hold their "
                     "nature; what changes is the world's evidence of it",
        "changed": "the Main Character changes their nature by the end"}),
    "growth": ("Growth", {
        "start": "the Main Character must START doing/believing something",
        "stop": "the Main Character must STOP doing/believing something"}),
    "approach": ("Approach", {
        "do-er": "a DO-ER — action-first; the throughline is doing",
        "be-er": "a BE-ER — adaptation-first; the throughline is inner"}),
    "limit": ("Limit", {
        "timelock": "a TIMELOCK — the clock is the antagonist; events race "
                    "a deadline",
        "optionlock": "an OPTIONLOCK — the story ends when options run out"}),
    "outcome": ("Outcome", {
        "success": "the Overall Story goal IS achieved",
        "failure": "the Overall Story goal is NOT achieved"}),
    "judgment": ("Judgment", {
        "good": "the Main Character ends personally resolved / fulfilled",
        "bad": "the Main Character ends personally unresolved / in anguish"}),
}


def _perspective_of(throughline_id: str) -> str:
    t = throughline_id.lower()
    if "overall" in t or t.startswith("t_os"):
        return "overall"
    if "_mc" in t or "mc_" in t:
        return "mc"
    if "_ic" in t or "ic_" in t:
        return "ic"
    if "_rel" in t or "rel_" in t or "_rs" in t:
        return "rel"
    return "overall"


def _subject_of(throughline_id: str) -> str:
    # "T_mc_rocky" → "rocky"; "T_rel_rocky_adrian" → "rocky adrian"
    parts = throughline_id.split("_")
    return " ".join(parts[2:]) if len(parts) > 2 else throughline_id


class DramaticaFrame(DialectFrame):
    """A DialectFrame that reads a Dramatica storyform. Overrides both
    surfaces; scenes map to the four-act signpost progression by their
    position in the sjuzhet (acts are the quarters of the narrative)."""

    def __init__(self, storyform: DramaticaStoryform, sjuzhet):
        self.overlay = storyform
        self.sf = storyform
        # event → act (1..4). Prefer the AUTHORED act structure; fall back
        # to a positional sjuzhet-quartile split only when none is given —
        # and remember which, so the bible can be honest about it.
        self._acts_authored = bool(storyform.act_event_ids)
        self._act_of: dict = {}
        self._unplaced: list = []
        if self._acts_authored:
            for act, event_ids in storyform.act_event_ids.items():
                for eid in event_ids:
                    self._act_of[eid] = int(act)
        ordered = sorted(sjuzhet, key=lambda s: s.τ_d)
        if not self._acts_authored:
            n = max(1, len(ordered))
            self._act_of = {
                e.event_id: min(4, i * 4 // n + 1)
                for i, e in enumerate(ordered)
            }
        else:
            # Any staged event the author did not place falls back
            # positionally, and is recorded so the bible can flag it.
            n = max(1, len(ordered))
            self._unplaced = [
                e.event_id for e in ordered if e.event_id not in self._act_of
            ]
            for i, e in enumerate(ordered):
                self._act_of.setdefault(e.event_id, min(4, i * 4 // n + 1))
        # (throughline_id, position) → signpost element
        self._sp = {
            (sp.throughline_id, sp.signpost_position): sp.signpost_element
            for sp in storyform.signposts
        }
        # ordered throughlines: OS, MC, IC, RS
        order = {"overall": 0, "mc": 1, "ic": 2, "rel": 3}
        self._throughlines = sorted(
            storyform.domain_assignments,
            key=lambda da: order.get(_perspective_of(da.throughline_id), 9),
        )
        self._dyn = {d.axis.value if hasattr(d.axis, "value") else d.axis:
                     d.leans for d in storyform.dynamics}
        # Axes the author declared as genuinely dual (span >1 pole) — the
        # bible frames these as contested rather than flat, so the prose can
        # carry the ambiguity instead of being pushed to one binary pole.
        self._dual = {d.axis.value if hasattr(d.axis, "value") else d.axis:
                      sorted(d.poles) for d in storyform.dynamics
                      if getattr(d, "is_dual", False)}

    def _axis_phrase(self, axis: str, lean: str) -> str:
        """Render one ending axis for the bible. A single-pole axis reads
        flat ('FAILURE: …'). A DUAL axis is framed as genuinely contested —
        the prose should carry BOTH poles at once, not resolve to one."""
        gloss = _DSP_GLOSS.get(axis, ("", {}))[1]
        dual = self._dual.get(axis)
        if dual:
            both = " and ".join(p.upper() for p in dual)
            reads = "; ".join(f"{p.upper()} ({gloss.get(p, '')})" for p in dual)
            return (f"genuinely BOTH {both} — this axis is CONTESTED, not "
                    f"resolved to one pole. Hold both true at once: {reads}. "
                    f"Render the ambiguity; do not collapse it to a binary.")
        return f"{lean.upper()}: {gloss.get(lean, '')}"

    # -- bible -------------------------------------------------------------

    def bible_sections(self, *, name_map) -> list:
        sf = self.sf
        lines = ["\n## Dramatica storyform (the structure this renders)"]
        if sf.action_summary:
            lines.append(sf.action_summary)

        # The ending SHAPE — the anti-tragedy signal.
        outcome = self._dyn.get("outcome", "")
        judgment = self._dyn.get("judgment", "")
        if sf.canonical_ending or (outcome and judgment):
            lines.append(
                f"\n## Ending shape — {sf.canonical_ending or '(derived)'}\n"
                f"- Outcome = {self._axis_phrase('outcome', outcome)}\n"
                f"- Judgment = {self._axis_phrase('judgment', judgment)}\n"
                f"Render to THIS shape — do not force a tragic catastrophe if "
                f"the judgment is Good, and do not force a happy ending if the "
                f"outcome is Failure. The two axes are independent.")

        # The story goal.
        if sf.story_goal:
            lines.append(f"\n## Story goal (what the Overall Story is trying "
                         f"to achieve)\n- {sf.story_goal}")
        if sf.story_consequence:
            lines.append(f"- Consequence if it fails: {sf.story_consequence}")

        # The four throughlines.
        lines.append("\n## The four throughlines (the four angles on the "
                     "trouble — give each its due)")
        for da in self._throughlines:
            persp_key = _perspective_of(da.throughline_id)
            label, gloss = _PERSPECTIVE[persp_key]
            domain = da.domain.value if hasattr(da.domain, "value") else da.domain
            dgloss = _DOMAIN_GLOSS.get(domain, domain)
            subject = _subject_of(da.throughline_id)
            lines.append(f"- {label} ({subject}) — {gloss}; its domain is "
                         f"{dgloss}")

        # The Main Character dynamics.
        lines.append("\n## Main Character dynamics (how the protagonist's "
                     "throughline moves)")
        for axis in ("resolve", "growth", "approach", "limit"):
            choice = self._dyn.get(axis)
            if choice:
                name, glosses = _DSP_GLOSS[axis]
                lines.append(f"- {name}: {choice.upper()} — "
                             f"{glosses.get(choice, '')}")

        # The signpost act-progression per throughline.
        if self._acts_authored and not self._unplaced:
            src = "the four-act boundaries below are AUTHORED"
        elif self._acts_authored:
            src = (f"act boundaries are authored, except "
                   f"{len(self._unplaced)} unplaced scene(s) approximated by "
                   f"position")
        else:
            src = ("NOTE: act boundaries are APPROXIMATE — inferred from "
                   "scene position, not authored; treat the act of a "
                   "boundary scene as a hint, not a fact")
        lines.append(f"\n## Signpost progression (each throughline moves "
                     f"through four acts; {src})")
        for da in self._throughlines:
            label = _PERSPECTIVE[_perspective_of(da.throughline_id)][0]
            steps = [self._sp.get((da.throughline_id, pos), "?")
                     for pos in (1, 2, 3, 4)]
            lines.append(f"- {label}: " + " → ".join(steps))
        return lines

    # -- per scene ---------------------------------------------------------

    def scene_lines(self, *, entry, name_map) -> list:
        act = self._act_of.get(entry.event_id)
        if not act:
            return []
        out = [f"Dramatica act: {act} of 4 (the narrative's "
               f"{['first', 'second', 'third', 'fourth'][act - 1]} quarter)"]
        concerns = []
        for da in self._throughlines:
            label = _PERSPECTIVE[_perspective_of(da.throughline_id)][0]
            element = self._sp.get((da.throughline_id, act))
            if element:
                concerns.append(f"{label}={element}")
        if concerns:
            out.append("This act's signpost concern per throughline — advance "
                       "these: " + "; ".join(concerns))
        return out
