"""
dramatica_repair.py — close the generate → evaluate → REPAIR loop for
the Dramatica dialect (parity with `draft_repair.py`).

The Dramatica evaluator finds where a Dramatica-generated draft drifted
from its storyform (the judgment slid from Good toward tragic; the
outcome read wrong; the protagonist's resolve flipped). This module
turns those findings into a targeted re-render — in DRAMATICA's terms,
not Aristotle's.

Where Aristotelian drifts localize to a single structural event (the
anti-recognition beat), a Dramatica shape-drift — outcome / judgment /
ending shape / MC resolve — is sealed at the ENDING. So `plan_repairs`
localizes those to the climactic resolution scene (the last beat of the
authored final act) and rebuilds the intended shape from the storyform's
own dynamics. Diffuse dimensions (a whole throughline reading faintly,
the MC's identity) are NOT forced onto one scene — they are reported,
not localized, exactly as the Aristotelian repair declines diffuse
losses.

`plan_repairs` is pure Python (offline-testable). Re-rendering reuses
`draft_repair.repair_scene(adapter=DramaticaFrame(...))` — the generator
is dialect-agnostic, so the same machinery re-renders a Dramatica scene.
Convergence (`draft_convergence.converge`) is already dependency-injected
and therefore already dialect-agnostic: wire the Dramatica evaluate /
plan / repair functions into it and it iterates to a fidelity ceiling
the same way.
"""

from __future__ import annotations

from story_engine.core.draft_repair import RepairDirective
from story_engine.core.dramatica_evaluator import _dyn_map


# Dimensions whose drift is sealed at the ending and is therefore
# localizable there. Throughline coverage and MC identity are diffuse and
# are deliberately NOT localized (reported, not forced onto a scene).
_ENDING_DIMENSIONS = ("judgment", "outcome", "ending_shape", "mc_resolve")


def _ending_event(storyform, sjuzhet):
    """The scene where the story's shape is sealed — the last staged beat
    of the authored final act, or the final staged beat if no act
    structure is authored."""
    if not sjuzhet:
        return None
    td = {s.event_id: s.τ_d for s in sjuzhet}
    acts = getattr(storyform, "act_event_ids", None) or {}
    final_act = acts.get(max(acts)) if acts else None
    if final_act:
        in_play = [e for e in final_act if e in td]
        if in_play:
            return max(in_play, key=lambda e: td[e])
    return max(sjuzhet, key=lambda s: s.τ_d).event_id


def _shape_directive(drifted, storyform) -> str:
    """Rebuild the intended ending shape from the storyform's dynamics,
    as a corrective directive — in Dramatica's own terms."""
    dyn = _dyn_map(storyform)
    outcome = (dyn.get("outcome") or "").lower()
    judgment = (dyn.get("judgment") or "").lower()
    resolve = (dyn.get("resolve") or "").lower()
    ending = (getattr(storyform, "canonical_ending", "") or "").replace("-", " ")

    parts = ["CRITICAL STRUCTURAL FIX — render the ENDING to its intended "
             "Dramatica shape:"]
    if ending:
        parts.append(f"This is a {ending.upper()}. Hold the two axes APART:")
    if outcome:
        verb = "is NOT achieved" if outcome == "failure" else "IS achieved"
        parts.append(f"- OUTCOME = {outcome.upper()}: the objective / public "
                     f"goal {verb}. Render that result plainly.")
    if judgment:
        state = ("personally FULFILLED, resolved, at peace" if judgment == "good"
                 else "personally UNRESOLVED, in anguish")
        parts.append(f"- JUDGMENT = {judgment.upper()}: the Main Character "
                     f"ends {state} — INDEPENDENT of the outcome. Do not let "
                     f"the objective result dictate the personal feeling.")
    if outcome == "failure" and judgment == "good":
        parts.append("So: he LOSES the contest and WINS what matters. This is "
                     "a personal triumph, NOT a tragedy — do not end in "
                     "catastrophe, despair, or defeat-as-anguish.")
    if resolve:
        held = ("HOLDS their essential nature (does not change)"
                if resolve == "steadfast" else "CHANGES their essential nature")
        parts.append(f"- The Main Character {held}.")
    return "\n".join(parts)


def plan_repairs(report, storyform, sjuzhet) -> list:
    """Map a DramaticaFidelityReport's localizable drifts to a corrective
    re-render of the ending scene. Returns 0 or 1 directive (the ending-
    shape directive bundles every drifted ending dimension)."""
    drifted = [f for f in getattr(report, "findings", [])
               if f.dimension in _ENDING_DIMENSIONS
               and f.verdict in ("drifted", "lost")]
    if not drifted:
        return []
    target = _ending_event(storyform, sjuzhet)
    if target is None:
        return []
    dims = ", ".join(sorted({f.dimension for f in drifted}))
    return [RepairDirective(
        event_id=target,
        dimension="dramatica_shape",
        authored=dims,
        instruction=_shape_directive(drifted, storyform),
    )]
