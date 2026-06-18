"""
demo_evaluate_rocky_dramatic.py — decompile the generated Rocky (general
Dramatic dialect) draft BLIND and score its fidelity (dialect-parity bet).

The fourth dialect to reach evaluate-parity. Closes the loop substrate →
prose (demo_generate_rocky_dramatic) → structure (blind decompile) →
fidelity, scored in the DRAMATIC dialect's own terms: who is the Hero, the
Obstacle, the Helper; does the prose AFFIRM the story's argument; are the
stakes legible? The Dramatic target is softer than Save-the-Cat's fifteen
beats by nature (no beat sheet) — the claim and stakes are token-overlap
(fuzzy) matches, labelled as such.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_evaluate_rocky_dramatic
    .venv/bin/python3 -m demos.demo_evaluate_rocky_dramatic --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.dramatic_evaluator import (
    decompile_dramatic, compare_to_story,
)
from story_engine.core.dramatic_generation import DramaticStory
from story_engine.encodings import rocky_dramatic_three_actor as D


def _story() -> DramaticStory:
    return DramaticStory(
        title="Rocky", action_summary="x",
        template_id=D.STORY.character_function_template_id,
        characters=D.CHARACTERS, arguments=(D.ARG_WORTH,),
        throughlines=D.THROUGHLINES, stakes=(D.STK_SELF_RESPECT,),
    )


def _load_draft_prose(path: str) -> str:
    with open(path) as f:
        text = f.read()
    marker = "\n---\n\n## Appendix"
    if marker in text:
        text = text.split(marker, 1)[0]
    lines = text.splitlines()
    body = [ln for ln in lines
            if not ln.startswith("# ") and not ln.startswith("_Generated")]
    return "\n".join(body).strip()


def _verdict_mark(v: str) -> str:
    return {"preserved": "✓", "drifted": "~", "lost": "✗",
            "added": "+"}.get(v, "?")


def _cli():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--draft", default="rocky_dramatic_first_draft.md")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--effort", default="high",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--max-tokens", type=int, default=6000)
    return p.parse_args()


def main() -> int:
    args = _cli()
    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set (or pass --dry-run).",
              file=sys.stderr)
        return 1
    if not os.path.exists(args.draft):
        print(f"ERROR: draft not found: {args.draft}", file=sys.stderr)
        return 1

    story = _story()
    prose = _load_draft_prose(args.draft)
    words = len(prose.split())

    print("Dramatic evaluator — blind decompile + argument/function fidelity")
    print(f"  draft: {args.draft}  ({words} words of prose)")
    print(f"  model: claude-opus-4-6  effort: {args.effort}")
    print(f"  authored: Hero/Obstacle/Helper + one argument (AFFIRM) + stakes")
    print()

    reading = decompile_dramatic(prose, title="Rocky", effort=args.effort,
                                 max_tokens=args.max_tokens,
                                 dry_run=args.dry_run)
    if args.dry_run:
        print("\n[dry run — prompt above; no decompilation performed]")
        return 0

    print("=" * 76)
    print("BLIND DECOMPILATION (the Dramatic structure the prose supports)")
    print("=" * 76)
    print(f"  hero: {reading.hero}")
    print(f"  obstacle: {reading.obstacle}")
    print(f"  helper: {reading.helper or '(none)'}")
    print(f"  argues: {reading.argument_claim}")
    print(f"  resolution: {reading.argument_resolution}")
    print(f"  stakes: {reading.stakes or '(none)'}")
    print(f"  overall: {reading.overall_read}")
    print()

    report = compare_to_story(reading, story)
    print("=" * 76)
    print("DRAMATIC FIDELITY — substrate → prose → substrate round-trip")
    print("=" * 76)
    for f in report.findings:
        print(f"  {_verdict_mark(f.verdict)} {f.dimension:20s} "
              f"authored={f.authored!r:34s} read={f.decompiled!r}")
        if f.note:
            print(f"      → {f.note}")
    print()
    pct = round(100 * report.score)
    print(f"  FIDELITY SCORE: {report.preserved}/{len(report.scored)} "
          f"dimensions preserved ({pct}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
