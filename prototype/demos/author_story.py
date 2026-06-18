"""
author_story.py — the human front-end CLI.

Author a story in a plain-text `.story.toml` file (no Python), then:

  1. COMPILE it to the verified substrate + Aristotelian overlay;
  2. VERIFY the structure (the same self-verifier the Python encodings
     use) and show the author any findings to fix;
  3. optionally GENERATE a first draft, and EVALUATE its fidelity.

This is the loop a writer runs — author, verify, fix, generate — with
the substrate staying the source of truth.

Usage:
    cd prototype
    # just compile + verify (no API):
    .venv/bin/python3 -m demos.author_story stories/quarter.story.toml

    # verify, then generate a draft (needs ANTHROPIC_API_KEY):
    .venv/bin/python3 -m demos.author_story stories/quarter.story.toml \\
        --generate --evaluate --save-md quarter_first_draft.md
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.authoring import (
    load_story_file, verify_compiled, StoryFormatError,
)


def _cli():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("story", help="path to a .story.toml file")
    p.add_argument("--generate", action="store_true",
                   help="generate a first draft if the story verifies clean")
    p.add_argument("--evaluate", action="store_true",
                   help="after generating, score structural fidelity")
    p.add_argument("--force", action="store_true",
                   help="generate even if the verifier reports findings")
    p.add_argument("--effort", default="medium",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--max-tokens", type=int, default=4000)
    p.add_argument("--save-md", metavar="PATH")
    return p.parse_args()


def main() -> int:
    args = _cli()

    # 1. COMPILE
    try:
        story = load_story_file(args.story)
    except FileNotFoundError:
        print(f"ERROR: no such file: {args.story}", file=sys.stderr)
        return 1
    except StoryFormatError as e:
        print(f"AUTHORING ERROR: {e}", file=sys.stderr)
        return 1

    print(f"Compiled '{story.title}'")
    print(f"  {len(story.entities)} entities | {len(story.fabula)} events | "
          f"{len(story.sjuzhet)} staged scenes")
    m = story.mythos
    print(f"  plot: {m.plot_kind} | peripeteia: {m.peripeteia_event_id} | "
          f"anagnorisis: {m.anagnorisis_event_id}")
    if m.pathos_character_ref_ids:
        print(f"  pathos-centre: {', '.join(m.pathos_character_ref_ids)} | "
              f"recognizer: {m.anagnorisis_character_ref_id}")

    # 2. VERIFY
    obs = verify_compiled(story)
    print()
    if not obs:
        print("✓ VERIFIES CLEAN — the structure is Aristotelian-consistent.")
    else:
        print(f"⚠ {len(obs)} finding(s) — the structure needs the author's "
              f"attention:")
        for o in obs:
            print(f"  [{o.severity}] {o.code}")
            print(f"      {o.message}")

    if not args.generate:
        return 0

    if obs and not args.force:
        print("\nNot generating: fix the findings above, or pass --force.",
              file=sys.stderr)
        return 1

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nERROR: ANTHROPIC_API_KEY not set (needed to generate).",
              file=sys.stderr)
        return 1

    # 3. GENERATE
    from story_engine.core.draft_generator import generate_draft
    print("\nGenerating first draft...")

    def on_scene(s):
        print(f"  [staged #{s.τ_d}] {s.event_id:24s} → {len(s.prose.split())} w")

    dialect_note = (
        "Aristotelian tragedy compiled from an author's story file. "
        + (story.logline or ""))
    result = generate_draft(
        title=story.title, sjuzhet=story.sjuzhet, fabula=story.fabula,
        entities=story.entities, descriptions=story.descriptions,
        mythos=story.mythos, preplay_disclosures=story.preplay_disclosures,
        dialect_note=dialect_note, effort=args.effort,
        max_tokens=args.max_tokens, on_scene=on_scene,
    )
    print("\n" + "=" * 72)
    print(f"FIRST DRAFT — {result.title} ({len(result.draft.split())} words)")
    print("=" * 72)
    print(result.draft)

    if args.save_md:
        with open(args.save_md, "w") as f:
            f.write(f"# {result.title} — first draft\n\n")
            f.write(f"_{story.logline}_\n\n")
            f.write("_Authored in a plain `.story.toml` and generated from "
                    "the verified substrate._\n\n")
            f.write(result.draft)
        print(f"\n[saved draft to {args.save_md}]")

    # 4. EVALUATE
    if args.evaluate:
        from story_engine.core.draft_evaluator import (
            decompile_draft, compare_to_mythos,
        )
        print("\n" + "=" * 72)
        print("STRUCTURAL FIDELITY — decompile blind, score vs the authored substrate")
        print("=" * 72)
        decompiled = decompile_draft(
            result.draft, title=story.title,  # genre-only note (blind)
            effort="high", max_tokens=8000,
        )
        report = compare_to_mythos(decompiled, story.mythos)
        mark = {"preserved": "✓", "drifted": "~", "lost": "✗", "added": "+"}
        for fnd in report.findings:
            print(f"  {mark.get(fnd.verdict, '?')} {fnd.dimension:20s} "
                  f"authored={fnd.authored!r:28s} read={fnd.decompiled!r}")
        print(f"\n  FIDELITY: {report.preserved}/{len(report.scored)} "
              f"preserved ({round(100*report.score)}%)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
