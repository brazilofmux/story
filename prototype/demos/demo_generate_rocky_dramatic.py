"""
demo_generate_rocky_dramatic.py — generate Rocky from the general DRAMATIC
dialect with a MINIMAL three-actor template (the fourth dialect path).

The deliberate contrast. `demo_generate_rocky.py` renders Rocky from the
heaviest Dramatica storyform; this renders the SAME substrate from the
leanest structure the parent dialect offers — three functions
(Hero / Obstacle / Helper), one thematic argument, the stakes. Same
dialect-agnostic generator, no changes; the structural vocabulary is
minimal.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_generate_rocky_dramatic --save-md rocky_dramatic_first_draft.md
    .venv/bin/python3 -m demos.demo_generate_rocky_dramatic --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.draft_generator import generate_draft
from story_engine.core.dramatic_generation import DramaticStory, DramaticFrame
from story_engine.encodings.rocky import (
    FABULA, SJUZHET, DESCRIPTIONS, ENTITIES,
)
from story_engine.encodings import rocky_dramatic_three_actor as D

_ACTION_SUMMARY = (
    "Rocky Balboa, an aging Philadelphia club fighter, is handed a "
    "one-in-a-million shot at the heavyweight title by the champion Apollo "
    "Creed, who wants a publicity-stunt opponent. Rocky cannot win and "
    "knows it; he sets himself the private goal of going the distance — of "
    "still being on his feet at the final bell — to prove to himself he is "
    "not just another bum from the neighborhood."
)

_DIALECT_NOTE = (
    "The general Dramatic dialect with a MINIMAL three-actor template — "
    "Hero, Obstacle, Helper. There is no act sheet and no storyform; the "
    "structure is lean: whose story this is, the single thematic argument "
    "the whole draft makes, and what is at stake. Render warm, working-"
    "class, hopeful-against-the-odds prose, and let every scene be a move "
    "in the argument."
)


def _story():
    return DramaticStory(
        title="Rocky", action_summary=_ACTION_SUMMARY,
        template_id=D.STORY.character_function_template_id,
        characters=D.CHARACTERS, arguments=(D.ARG_WORTH,),
        throughlines=D.THROUGHLINES, stakes=(D.STK_SELF_RESPECT,),
    )


def _cli():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--effort", default="medium",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--max-tokens", type=int, default=4000)
    p.add_argument("--save-md", metavar="PATH")
    return p.parse_args()


def main() -> int:
    args = _cli()
    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set (or pass --dry-run).",
              file=sys.stderr)
        return 1

    frame = DramaticFrame(_story(), FABULA)
    print("Substrate → first-draft — Rocky (DRAMATIC, minimal three-actor)")
    print(f"  model: claude-opus-4-6  effort: {args.effort}")
    print(f"  fabula: {len(FABULA)} | sjuzhet: {len(SJUZHET)} | "
          f"dialect: Dramatic (3-actor: Hero/Obstacle/Helper)\n")

    def on_scene(s):
        if args.dry_run:
            print("=" * 72)
            print(f"BRIEF τ_d={s.τ_d} ({s.event_id}) focalizer={s.focalizer}")
            print("=" * 72)
            print(s.brief + "\n")
        else:
            print(f"  [τ_d={s.τ_d:>2}] {s.event_id:28s} → "
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
            f.write(f"# {result.title} — first draft (Dramatic, three-actor)\n\n")
            f.write("_Generated from the general Dramatic dialect with a "
                    "minimal three-actor template — the leanest structure "
                    "(Hero/Obstacle/Helper + one argument + stakes), the "
                    "structural parent of the Dramatica storyform._\n\n")
            f.write(result.draft)
            f.write("\n\n---\n\n## Appendix — story bible\n\n```\n"
                    + result.story_bible + "\n```\n")
        print(f"\n[saved draft to {args.save_md}]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
