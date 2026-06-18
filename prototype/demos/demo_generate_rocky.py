"""
demo_generate_rocky.py — generate from a DRAMATICA storyform (second
dialect), on a NON-TRAGIC story.

The founding plural-dialect thesis, proven generatively. Rocky is not an
Aristotelian tragedy — there is no hamartia, no peripeteia, no
catastrophe. Its Dramatica storyform ends Outcome=Failure × Judgment=Good
= a *personal triumph*: he loses the fight and wins everything that
matters. The same dialect-agnostic generator that rendered Oedipus and
the originals renders Rocky here — driven by a DramaticaFrame instead of
the default tragic-arc frame, with zero changes to the generator.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_generate_rocky --save-md rocky_first_draft.md
    .venv/bin/python3 -m demos.demo_generate_rocky --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.draft_generator import generate_draft
from story_engine.core.dramatica_generation import (
    DramaticaStoryform, DramaticaFrame,
)
from story_engine.encodings.rocky import (
    FABULA, SJUZHET, DESCRIPTIONS, ENTITIES,
)
from story_engine.encodings import rocky_dramatica_complete as RD

_ACTION_SUMMARY = (
    "Rocky Balboa, an aging Philadelphia club fighter and loan-shark "
    "enforcer, is handed a one-in-a-million shot when the heavyweight "
    "champion Apollo Creed picks him as a publicity-stunt opponent for a "
    "bicentennial title bout. Rocky cannot win and knows it; he sets "
    "himself the private goal of going the distance — of still being on "
    "his feet at the final bell, to prove he is not just another bum from "
    "the neighborhood. He trains; he falls for Adrian; he goes the full "
    "fifteen rounds and loses the decision — and it does not matter, "
    "because he has done the thing he set out to do and he has Adrian."
)

_DIALECT_NOTE = (
    "A Dramatica storyform, not a tragedy. The structure is four "
    "throughlines and a four-act signpost progression; the ending is a "
    "PERSONAL TRIUMPH (the public goal fails, the personal judgment is "
    "good). Render warm, working-class, hopeful-against-the-odds prose — "
    "this story does not end in catastrophe."
)


def _storyform():
    return DramaticaStoryform(
        title="Rocky",
        action_summary=_ACTION_SUMMARY,
        domain_assignments=RD.DOMAIN_ASSIGNMENTS,
        signposts=RD.ALL_SIGNPOSTS,
        dynamics=RD.DYNAMIC_STORY_POINTS,
        story_goal=RD.STORY_GOAL,
        story_consequence=RD.STORY_CONSEQUENCE,
        canonical_ending=RD.CANONICAL_ENDING,
        act_event_ids=RD.ACT_EVENT_IDS,
    )


def _cli():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--effort", default="medium",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--max-tokens", type=int, default=4000)
    p.add_argument("--save-md", metavar="PATH")
    p.add_argument("--evaluate", action="store_true",
                   help="after generating, score Dramatica fidelity")
    return p.parse_args()


def main() -> int:
    args = _cli()
    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set (or pass --dry-run).",
              file=sys.stderr)
        return 1

    frame = DramaticaFrame(_storyform(), SJUZHET)

    print("Substrate → first-draft generator — Rocky (DRAMATICA, non-tragic)")
    print(f"  model: claude-opus-4-6  effort: {args.effort}")
    print(f"  fabula: {len(FABULA)} | sjuzhet: {len(SJUZHET)} | "
          f"dialect: Dramatica | ending: {RD.CANONICAL_ENDING}\n")

    def on_scene(s):
        if args.dry_run:
            print("=" * 72)
            print(f"BRIEF staged-τ_d={s.τ_d} ({s.event_id}) focalizer={s.focalizer}")
            print("=" * 72)
            print(s.brief + "\n")
        else:
            print(f"  [staged #{s.τ_d:>2}] {s.event_id:28s} → "
                  f"{len(s.prose.split())} w")

    result = generate_draft(
        title="Rocky", sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
        descriptions=DESCRIPTIONS, adapter=frame, dialect_note=_DIALECT_NOTE,
        effort=args.effort, max_tokens=args.max_tokens, dry_run=args.dry_run,
        on_scene=on_scene,
    )

    if args.dry_run:
        print("\n" + "=" * 72 + "\nSTORY BIBLE\n" + "=" * 72)
        print(result.story_bible)
        return 0

    print("\n" + "=" * 72)
    print(f"FIRST DRAFT — {result.title} ({len(result.draft.split())} words)")
    print("=" * 72)
    print(result.draft)

    if args.save_md:
        with open(args.save_md, "w") as f:
            f.write(f"# {result.title} — first draft (Dramatica dialect)\n\n")
            f.write("_Generated from a Dramatica storyform via the "
                    "dialect-agnostic generator — a non-tragic story type "
                    "(personal triumph), not an Aristotelian tragedy._\n\n")
            f.write(result.draft)
            f.write("\n\n---\n\n## Appendix — story bible\n\n```\n"
                    + result.story_bible + "\n```\n")
        print(f"\n[saved draft to {args.save_md}]")

    if args.evaluate:
        from story_engine.core.dramatica_evaluator import (
            decompile_dramatica, compare_to_storyform,
        )
        print("\n" + "=" * 72)
        print("DRAMATICA FIDELITY — decompile blind, score vs the storyform")
        print("=" * 72)
        reading = decompile_dramatica(
            result.draft, title="Rocky", dialect_note=_DIALECT_NOTE,
            effort="high", max_tokens=6000,
        )
        report = compare_to_storyform(reading, _storyform())
        mark = {"preserved": "✓", "drifted": "~", "lost": "✗", "added": "+"}
        for f in report.findings:
            print(f"  {mark.get(f.verdict, '?')} {f.dimension:16s} "
                  f"authored={f.authored!r:20s} read={f.decompiled!r}")
        print(f"\n  FIDELITY: {report.preserved}/{len(report.scored)} "
              f"preserved ({round(100*report.score)}%)")
        print(f"  ending read as: {reading.ending_shape!r} "
              f"(outcome={reading.outcome}, judgment={reading.judgment})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
