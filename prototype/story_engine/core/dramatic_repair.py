"""
dramatic_repair.py — close the generate → evaluate → REPAIR loop for the
general DRAMATIC dialect (parity with the peer repairers).

The Dramatic dialect is diffuse: the argument is carried across the whole
draft and the functions (Hero/Obstacle/Helper) recur scene to scene. Almost
nothing localizes to a single event — which is exactly why the honesty
discipline is the point of this module.

The ONE cleanly-localizable drift is the **argument's resolution**: like a
Dramatica ending-shape drift, whether the prose AFFIRMS / NEGATES /
COMPLICATES its claim is sealed at the ENDING. So `plan_repairs` localizes
that to the final staged beat and rebuilds the intended resolution from the
authored Argument. Everything else — a Hero read as the wrong character, a
thinned claim, faint stakes — is DIFFUSE and is reported (visible in the
fidelity report), never forced onto one scene. That mirrors how
`draft_repair` declines diffuse pathos losses and `dramatica_repair` declines
throughline-coverage losses.

`plan_repairs` is pure Python (offline-testable). Re-rendering reuses
`draft_repair.repair_scene(adapter=DramaticFrame(...))`. Convergence
(`draft_convergence.converge`) is dependency-injected and therefore already
dialect-agnostic.
"""

from __future__ import annotations

from story_engine.core.draft_repair import RepairDirective


# The only dimension sealed at the ending and therefore localizable. Hero /
# obstacle / helper identity, the claim's content, and the stakes are diffuse
# and are deliberately NOT localized.
_ENDING_DIMENSIONS = ("argument_resolution",)


def _ending_event(sjuzhet):
    """The scene where the argument is sealed — the final staged beat. The
    Dramatic dialect authors no acts, so there is no act boundary to prefer."""
    if not sjuzhet:
        return None
    return max(sjuzhet, key=lambda s: s.τ_d).event_id


def _argument_directive(story) -> str:
    """Rebuild the intended argument resolution as a corrective directive,
    in the Dramatic dialect's own terms."""
    args = getattr(story, "arguments", ()) or ()
    if not args:
        return ""
    arg = args[0]
    a_dir = getattr(getattr(arg, "resolution_direction", ""), "value",
                    getattr(arg, "resolution_direction", ""))
    a_dir = str(a_dir).lower()
    premise = getattr(arg, "premise", "")
    counter = getattr(arg, "counter_premise", "") or ""

    verb = {
        "affirm": "AFFIRM — the ending must uphold and prove this claim",
        "negate": "NEGATE — the ending must refute / undercut this claim",
        "complicate": "COMPLICATE — the ending must both support AND qualify "
                      "this claim, not resolve it cleanly to one side",
        "unresolved": "leave UNRESOLVED — the ending must hold the claim open, "
                      "neither proving nor refuting it",
    }.get(a_dir, f"resolve ({a_dir})")

    parts = [
        "CRITICAL STRUCTURAL FIX — land the story's ARGUMENT at its ending, "
        "in the Dramatic dialect's terms:",
        f"The story argues: {premise}",
        f"Its ending must {verb}.",
    ]
    if counter:
        parts.append(f"It does so by answering the counter-claim: {counter}")
    parts.append("Render the final beat so a reader feels the argument LAND "
                 "this way — do not let the resolution drift to the opposite "
                 "side or go slack.")
    return "\n".join(parts)


def plan_repairs(report, story, sjuzhet) -> list:
    """Map a DramaticFidelityReport's localizable drift (the argument
    resolution) to a corrective re-render of the ending scene. Returns 0 or 1
    directive. Diffuse dimensions are not localized."""
    drifted = [f for f in getattr(report, "findings", [])
               if f.dimension in _ENDING_DIMENSIONS
               and f.verdict in ("drifted", "lost")]
    if not drifted:
        return []
    target = _ending_event(sjuzhet)
    if target is None:
        return []
    directive = _argument_directive(story)
    if not directive:
        return []
    return [RepairDirective(
        event_id=target,
        dimension="argument_resolution",
        authored=drifted[0].authored,
        instruction=directive,
    )]
