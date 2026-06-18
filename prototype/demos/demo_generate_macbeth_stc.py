"""
demo_generate_macbeth_stc.py — generate Macbeth from a SAVE-THE-CAT beat
sheet (the third dialect).

Widens the dialect-agnostic generator from two dialects to three. The
same machinery that rendered Oedipus (Aristotelian) and Rocky (Dramatica)
renders Macbeth here from Blake Snyder's commercial-screenplay 15-beat
structure — Opening Image, Catalyst, Break Into Two, Midpoint, All Is
Lost, Finale, Final Image — and the A/B strands, driven by an StcFrame
instead of a tragic arc or a storyform, with zero changes to the
generator.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_generate_macbeth_stc --save-md macbeth_stc_first_draft.md
    .venv/bin/python3 -m demos.demo_generate_macbeth_stc --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.draft_generator import generate_draft
from story_engine.core.save_the_cat_generation import StcStorySheet, StcFrame
from story_engine.encodings.macbeth import (
    FABULA, SJUZHET, DESCRIPTIONS, ENTITIES, PREPLAY_DISCLOSURES,
)
from story_engine.encodings import macbeth_save_the_cat as S

_ACTION_SUMMARY = (
    "Macbeth, a victorious Scottish thane, is told by three witches that he "
    "will be king. Spurred by the prophecy and by his wife, he murders the "
    "good king Duncan in his sleep and takes the crown — and then must kill "
    "and kill again to hold a throne the same prophecy said would pass to "
    "another man's line. His wife unravels into madness and death; he "
    "hardens into a tyrant with nothing left to feel; and the prophecy's "
    "promised protections turn out to be the trap that destroys him."
)

_DIALECT_NOTE = (
    "A Save-the-Cat beat sheet (commercial-screenplay structure), not a "
    "tragic arc or a storyform. Render to the 15 beats and the A/B strands "
    "below; honor each beat's structural job. Macbeth's is a dark 'rites of "
    "passage' shape — the protagonist's transformation is a corruption, and "
    "the Final Image inverts the Opening into restored order. Render as "
    "dramatic prose."
)


def _sheet():
    return StcStorySheet(
        title="Macbeth", action_summary=_ACTION_SUMMARY,
        beats=S.BEATS, strands=S.STRANDS, characters=S.CHARACTERS,
        beat_event_ids=S.BEAT_EVENT_IDS,
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

    frame = StcFrame(_sheet(), SJUZHET)
    print("Substrate → first-draft generator — Macbeth (SAVE-THE-CAT, 3rd dialect)")
    print(f"  model: claude-opus-4-6  effort: {args.effort}")
    print(f"  fabula: {len(FABULA)} | sjuzhet: {len(SJUZHET)} | "
          f"dialect: Save-the-Cat (15 beats, A/B strands)\n")

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
        title="Macbeth", sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
        descriptions=DESCRIPTIONS, adapter=frame,
        preplay_disclosures=PREPLAY_DISCLOSURES, dialect_note=_DIALECT_NOTE,
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
            f.write(f"# {result.title} — first draft (Save-the-Cat dialect)\n\n")
            f.write("_Generated from a Save-the-Cat 15-beat sheet via the "
                    "dialect-agnostic generator — a third dialect, a "
                    "commercial-screenplay structure._\n\n")
            f.write(result.draft)
            f.write("\n\n---\n\n## Appendix — story bible\n\n```\n"
                    + result.story_bible + "\n```\n")
        print(f"\n[saved draft to {args.save_md}]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
