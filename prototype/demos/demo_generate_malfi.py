"""
demo_generate_malfi.py — substrate → first-draft prose, on The Duchess
of Malfi.

The SECOND generation demo (after Oedipus), proving the substrate→prose
path is not Oedipus-specific and that the richer Aristotelian apparatus
is load-bearing in generation. Malfi exercises the full ledger the
research arc built:

  - A19 secondary_peripeteia_event_ids — four falling arcs in one mythos
    (the Duchess, Ferdinand, Bosola, Antonio), not a single reversal.
  - A20 anagnorisis_qualifier — Antonio's dark-room death is an
    ANTI-recognition (real, but too late).
  - A22 pathos_character_ref_ids (sketch-07) — the Duchess is the
    pathos-centre, SPLIT from the recognizer (Ferdinand). The generator
    surfaces this so the prose renders her suffering as the emotional
    centre even though Ferdinand is the one who comes to knowledge.

The substrate is the source of truth; the model is the renderer.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_generate_malfi

    # Inspect what the substrate hands the renderer (bible + briefs),
    # no API call:
    .venv/bin/python3 -m demos.demo_generate_malfi --dry-run

    # Save the draft (and the per-scene briefs) to a markdown file:
    .venv/bin/python3 -m demos.demo_generate_malfi \\
        --save-md malfi_first_draft.md
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.draft_generator import generate_draft
from story_engine.encodings.malfi import (
    FABULA, SJUZHET, DESCRIPTIONS, ENTITIES, PREPLAY_DISCLOSURES,
)
from story_engine.encodings.malfi_aristotelian import AR_MALFI_MYTHOS


def _cli_args():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--dry-run", action="store_true",
                   help="Build the bible + briefs and exit (no API).")
    p.add_argument("--effort", default="medium",
                   choices=["low", "medium", "high", "max"],
                   help="output_config.effort per scene (default: medium).")
    p.add_argument("--max-tokens", type=int, default=4000,
                   help="max_tokens per scene (default: 4000).")
    p.add_argument("--save-md", metavar="PATH",
                   help="Save the assembled draft + briefs to PATH.")
    return p.parse_args()


def main() -> int:
    args = _cli_args()
    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set (or pass --dry-run).",
              file=sys.stderr)
        return 1

    print("Substrate → first-draft generator — The Duchess of Malfi")
    print(f"  model: claude-opus-4-6  effort: {args.effort}")
    print(f"  fabula events: {len(FABULA)}  |  staged scenes (sjuzhet): "
          f"{len(SJUZHET)}  |  descriptions: {len(DESCRIPTIONS)}")
    print(f"  arc: peripeteia={AR_MALFI_MYTHOS.peripeteia_event_id} | "
          f"anagnorisis={AR_MALFI_MYTHOS.anagnorisis_event_id}")
    print(f"  secondary reversals: "
          f"{len(AR_MALFI_MYTHOS.secondary_peripeteia_event_ids)} | "
          f"pathos-centre: {', '.join(AR_MALFI_MYTHOS.pathos_character_ref_ids)}")
    print()

    def on_scene(scene):
        if args.dry_run:
            print("=" * 76)
            print(f"BRIEF — scene τ_d={scene.τ_d} ({scene.event_id}) | "
                  f"focalizer: {scene.focalizer}")
            print("=" * 76)
            print(scene.brief)
            print()
        else:
            words = len(scene.prose.split())
            print(f"  [scene τ_d={scene.τ_d:>2}] {scene.event_id:32s} "
                  f"focalizer={scene.focalizer:18s} → {words} words")

    result = generate_draft(
        title="The Duchess of Malfi",
        sjuzhet=SJUZHET,
        fabula=FABULA,
        entities=ENTITIES,
        descriptions=DESCRIPTIONS,
        mythos=AR_MALFI_MYTHOS,
        preplay_disclosures=PREPLAY_DISCLOSURES,
        dialect_note=(
            "Aristotelian tragedy (complex plot) with a DISTRIBUTED fall: "
            "one mythos carrying several tragic arcs (the Duchess, then "
            "Ferdinand, Bosola, Antonio), a pathos-centre (the Duchess) "
            "split from the recognizer (Ferdinand), and an anti-"
            "recognition (Antonio's dark-room death — truth too late). "
            "Render as dramatic prose in Webster's cold, ironic register."
        ),
        effort=args.effort,
        max_tokens=args.max_tokens,
        dry_run=args.dry_run,
        on_scene=on_scene,
    )

    if args.dry_run:
        print("\n[dry run — story bible above each brief in the system "
              "prompt; no prose generated]")
        print("\n" + "=" * 76)
        print("STORY BIBLE (cached in system prompt)")
        print("=" * 76)
        print(result.story_bible)
        return 0

    print()
    print("=" * 76)
    print(f"FIRST DRAFT — {result.title}")
    print("=" * 76)
    print(result.draft)

    if args.save_md:
        with open(args.save_md, "w") as f:
            f.write(f"# {result.title} — first draft\n\n")
            f.write("_Generated from the verified substrate; the engine "
                    "is the author of record, the model the renderer._\n\n")
            f.write(result.draft)
            f.write("\n\n---\n\n## Appendix — per-scene briefs "
                    "(the substrate that drove each scene)\n\n")
            f.write("```\n" + result.story_bible + "\n```\n\n")
            for s in result.scenes:
                f.write(f"### Scene τ_d={s.τ_d} — {s.event_id} "
                        f"(focalizer: {s.focalizer})\n\n")
                f.write("```\n" + s.brief + "\n```\n\n")
        print(f"\n[saved draft + briefs to {args.save_md}]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
