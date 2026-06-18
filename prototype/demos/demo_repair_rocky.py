"""
demo_repair_rocky.py — the Dramatica generate → evaluate → REPAIR loop,
controlled regression-recovery on the ending.

Parity proof for the second dialect. A Dramatica story's shape is sealed
at the ending (Outcome × Judgment); the headline failure mode is the
*tragedy-collapse* — the prose lets the lost contest drag the personal
judgment down into anguish, turning a personal triumph into a tragedy.
An Aristotelian evaluator cannot see this (it has no Judgment axis); the
Dramatica evaluator can, and the Dramatica repair fixes it.

Scoped to the ending scene (where Dramatica shape lives — no need to
re-decompile 33k words):

1. INJECT — re-render the ending as a despairing TRAGEDY (a known
   regression).
2. EVALUATE — the Dramatica evaluator reads the drifted ending; Judgment
   slides Good → Bad.
3. PLAN — dramatica_repair localizes the shape-drift to this ending.
4. REPAIR — re-render with the storyform's intended shape (personal
   triumph) restored.
5. VERIFY — the Dramatica evaluator re-reads; Judgment back to Good.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_repair_rocky
"""

from __future__ import annotations

import os
import sys

from story_engine.core.draft_generator import render_scene_prose
from story_engine.core.draft_repair import RepairDirective, repair_scene
from story_engine.core.dramatica_generation import DramaticaFrame
from story_engine.core.dramatica_evaluator import (
    decompile_dramatica, compare_to_storyform,
)
from story_engine.core.dramatica_repair import plan_repairs
from story_engine.encodings.rocky import (
    FABULA, SJUZHET, DESCRIPTIONS, ENTITIES,
)
from demos.demo_generate_rocky import _storyform, _DIALECT_NOTE

_ENDING = "E_no_rematch"
_INJECT = (
    "Render this ending as a DESPAIRING TRAGEDY: Rocky is broken — the loss "
    "has destroyed him; he is defeated in body and spirit, the dream "
    "exposed as a humiliation, no comfort and no meaning left. End in "
    "anguish and emptiness."
)
# The evaluator must read BLIND — it is NOT told the intended shape, only
# what to look for. (Telling it "this is a personal triumph" would lead it.)
_EVAL_NOTE = (
    "The closing scene of a story. Read the Dramatica structure it actually "
    "shows — especially the Main Character's personal resolution (JUDGMENT: "
    "ends fulfilled/at peace = good, or unresolved/in anguish = bad) and the "
    "ending's shape. Report what the prose does, not what it ought to do."
)


def _judgment(prose, client=None):
    return decompile_dramatica(
        prose, title="(closing scene)", dialect_note=_EVAL_NOTE,
        effort="high", max_tokens=3000, client=client)


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        return 1

    storyform = _storyform()
    frame = DramaticaFrame(storyform, SJUZHET)
    ending = next(e for e in SJUZHET if e.event_id == _ENDING)

    print("Dramatica generate → evaluate → REPAIR — Rocky (ending regression)")
    print(f"  intended ending: {storyform.canonical_ending} "
          f"(outcome=failure × judgment=good)\n")

    # 1. INJECT a tragic regression into the ending. NO frame and a neutral
    #    note — this simulates a generation that drifted because the
    #    storyform shape was NOT surfaced; otherwise the bible's insistence
    #    on the personal-triumph shape overrides the tragic directive (the
    #    substrate is that load-bearing — a real finding, but it leaves
    #    nothing to repair).
    print(f"[1/5] INJECT — re-rendering {_ENDING} as a tragedy (unframed)...")
    drifted = render_scene_prose(
        entry=ending, sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
        descriptions=DESCRIPTIONS, adapter=None, title="Rocky",
        dialect_note="", extra_directive=_INJECT,
        effort="medium", max_tokens=3000)
    print(f"      regressed ending ({len(drifted.split())} words)")

    # 2. EVALUATE the drifted ending (blind).
    print("\n[2/5] EVALUATE — reading the drifted ending (Dramatica, blind)...")
    r1 = _judgment(drifted)
    print(f"      judgment={r1.judgment!r}  ending_shape={r1.ending_shape!r}  "
          f"mc_resolve={r1.mc_resolve!r}")
    report = compare_to_storyform(r1, storyform)
    drifts = [f.dimension for f in report.findings
              if f.verdict in ("drifted", "lost")]
    print(f"      drifted dimensions: {drifts}")

    # 3. PLAN.
    print("\n[3/5] PLAN — localizing the shape-drift...")
    directives = plan_repairs(report, storyform, SJUZHET)
    if not directives:
        print("      no localizable shape-drift detected — the ending read "
              "faithfully even after injection. Nothing to repair.")
        return 0
    d = directives[0]
    print(f"      → repair {d.dimension} at {d.event_id} (restore: {d.authored})")

    # 4. REPAIR.
    print(f"\n[4/5] REPAIR — re-rendering {d.event_id} to the intended shape...")
    rr = repair_scene(
        d, sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
        descriptions=DESCRIPTIONS, adapter=frame, title="Rocky",
        dialect_note=_DIALECT_NOTE, effort="medium", max_tokens=3000)
    print(f"      repaired ending ({len(rr.after.split())} words)")

    # 5. VERIFY (blind).
    print("\n[5/5] VERIFY — re-reading the repaired ending (Dramatica, blind)...")
    r2 = _judgment(rr.after)
    print(f"      judgment={r2.judgment!r}  ending_shape={r2.ending_shape!r}  "
          f"mc_resolve={r2.mc_resolve!r}")

    fixed = (r2.judgment or "").lower() == "good"
    print("\n" + "=" * 64)
    print(f"  Judgment: {r1.judgment!r} (tragic) → {r2.judgment!r} "
          f"({'✓ RECOVERED to personal triumph' if fixed else '✗ still drifted'})")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
