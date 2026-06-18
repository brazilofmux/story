"""
demo_generate_vantage.py — generate a first draft of the ORIGINAL story
"The Vantage Light", and score its structural fidelity.

The real test of the whole pipeline: a story that is not in any canon,
authored as a verified substrate + Aristotelian overlay, rendered to
prose, then decompiled blind and scored against the substrate it came
from. If an original comes out structurally faithful, the engine
GENERATES; it does not merely re-render works the model already knows.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_generate_vantage --save-md vantage_first_draft.md
    .venv/bin/python3 -m demos.demo_generate_vantage --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.draft_generator import generate_draft
from story_engine.core.draft_evaluator import decompile_draft, compare_to_mythos
from story_engine.encodings.vantage_light import (
    FABULA, SJUZHET, DESCRIPTIONS, ENTITIES, PREPLAY_DISCLOSURES,
)
from story_engine.encodings.vantage_light_aristotelian import AR_VANTAGE_MYTHOS

_DIALECT_NOTE = (
    "Aristotelian tragedy (complex plot): a single action moving through "
    "beginning / middle / end to a peripeteia (the keeper's own light, his "
    "pride, becomes the instrument of the wreck) and an anagnorisis (he "
    "recognises too late that his pride, not the sea, did this). The "
    "pathos-centre (the daughter, who drowns for his error) is distinct "
    "from the recognizer (the father). Render as spare, weather-bitten "
    "dramatic prose."
)


def _cli():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--effort", default="medium",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--max-tokens", type=int, default=4000)
    p.add_argument("--save-md", metavar="PATH")
    p.add_argument("--no-evaluate", action="store_true",
                   help="Skip the fidelity evaluation after generation.")
    return p.parse_args()


def main() -> int:
    args = _cli()
    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set (or pass --dry-run).",
              file=sys.stderr)
        return 1

    print("Substrate → first-draft generator — The Vantage Light (ORIGINAL)")
    print(f"  model: claude-opus-4-6  effort: {args.effort}")
    print(f"  fabula: {len(FABULA)} | sjuzhet: {len(SJUZHET)} | "
          f"pathos-centre: {', '.join(AR_VANTAGE_MYTHOS.pathos_character_ref_ids)} "
          f"| recognizer: {AR_VANTAGE_MYTHOS.anagnorisis_character_ref_id}\n")

    def on_scene(s):
        if args.dry_run:
            print("=" * 72)
            print(f"BRIEF τ_d={s.τ_d} ({s.event_id}) focalizer={s.focalizer}")
            print("=" * 72)
            print(s.brief + "\n")
        else:
            print(f"  [τ_d={s.τ_d:>2}] {s.event_id:28s} "
                  f"focalizer={s.focalizer:14s} → {len(s.prose.split())} w")

    result = generate_draft(
        title="The Vantage Light", sjuzhet=SJUZHET, fabula=FABULA,
        entities=ENTITIES, descriptions=DESCRIPTIONS, mythos=AR_VANTAGE_MYTHOS,
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
            f.write(f"# {result.title} — first draft (original story)\n\n")
            f.write("_Generated from a verified ORIGINAL substrate; the "
                    "engine is the author of record, the model the renderer._\n\n")
            f.write(result.draft)
            f.write("\n\n---\n\n## Appendix — story bible\n\n```\n"
                    + result.story_bible + "\n```\n")
        print(f"\n[saved draft to {args.save_md}]")

    if not args.no_evaluate:
        print("\n" + "=" * 72)
        print("STRUCTURAL FIDELITY — decompile the original blind, score vs substrate")
        print("=" * 72)
        decompiled = decompile_draft(
            result.draft, title="The Vantage Light",  # genre-only note (blind)
            effort="high", max_tokens=8000,
        )
        report = compare_to_mythos(decompiled, AR_VANTAGE_MYTHOS)
        mark = {"preserved": "✓", "drifted": "~", "lost": "✗", "added": "+"}
        for fnd in report.findings:
            print(f"  {mark.get(fnd.verdict, '?')} {fnd.dimension:22s} "
                  f"authored={fnd.authored!r:34s} read={fnd.decompiled!r}")
        print(f"\n  FIDELITY: {report.preserved}/{len(report.scored)} "
              f"preserved ({round(100*report.score)}%)")
        print(f"  blind read: pathos-centre="
              f"{', '.join(decompiled.pathos_centre_characters)} | "
              f"recognizer={decompiled.anagnorisis_character}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
