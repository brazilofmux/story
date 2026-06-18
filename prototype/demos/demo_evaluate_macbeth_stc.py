"""
demo_evaluate_macbeth_stc.py — decompile the generated Macbeth (Save-the-Cat)
draft BLIND and score its beat-sheet fidelity (dialect-parity bet).

The peer of demo_evaluate_malfi (Aristotelian) and the Rocky/Dramatica
evaluation: closes the StC loop substrate → prose (demo_generate_macbeth_stc)
→ structure (blind decompile) → fidelity. Answers "did the prose carry the
fifteen beats, in order, on Macbeth, with the marriage B story?" — scored in
Save-the-Cat's OWN terms, never forced through an Aristotelian lens.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_evaluate_macbeth_stc
    .venv/bin/python3 -m demos.demo_evaluate_macbeth_stc --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.save_the_cat_evaluator import (
    decompile_stc, compare_to_sheet, _slot_of_read,
)
from story_engine.core.save_the_cat_generation import StcStorySheet
from story_engine.encodings import macbeth_save_the_cat as S


def _sheet() -> StcStorySheet:
    return StcStorySheet(
        title="Macbeth", action_summary="x",
        beats=S.BEATS, strands=S.STRANDS, characters=S.CHARACTERS,
        beat_event_ids=S.BEAT_EVENT_IDS,
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
    p.add_argument("--draft", default="macbeth_stc_first_draft.md")
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

    sheet = _sheet()
    prose = _load_draft_prose(args.draft)
    words = len(prose.split())

    print("Save-the-Cat evaluator — blind decompile + beat-sheet fidelity")
    print(f"  draft: {args.draft}  ({words} words of prose)")
    print(f"  model: claude-opus-4-6  effort: {args.effort}")
    print(f"  authored: 15 beats | strands={len(sheet.strands)} | "
          f"protagonist=Macbeth")
    print()

    reading = decompile_stc(prose, title="Macbeth", effort=args.effort,
                            max_tokens=args.max_tokens, dry_run=args.dry_run)
    if args.dry_run:
        print("\n[dry run — prompt above; no decompilation performed]")
        return 0

    print("=" * 76)
    print("BLIND DECOMPILATION (the beat sheet the prose alone supports)")
    print("=" * 76)
    print(f"  protagonist: {reading.protagonist}")
    print(f"  B story: {reading.b_story or '(none)'}")
    print(f"  midpoint: {reading.midpoint or '(none)'}")
    print(f"  all is lost: {reading.all_is_lost or '(none)'}")
    print(f"  final mirrors opening: {reading.final_mirrors_opening or '?'}")
    print("  beats located (in prose order):")
    for b in reading.beats_identified:
        slot = _slot_of_read(b.beat)
        tag = f"[{slot:02d}]" if slot else "[??]"
        print(f"    {tag} {b.beat}: {b.what_happens}")
    print(f"  overall: {reading.overall_read}")
    print()

    report = compare_to_sheet(reading, sheet)
    print("=" * 76)
    print("BEAT-SHEET FIDELITY — substrate → prose → substrate round-trip")
    print("=" * 76)
    for f in report.findings:
        print(f"  {_verdict_mark(f.verdict)} {f.dimension:14s} "
              f"authored={f.authored!r:24s} read={f.decompiled!r}")
    print()
    pct = round(100 * report.score)
    print(f"  FIDELITY SCORE: {report.preserved}/{len(report.scored)} "
          f"dimensions preserved ({pct}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
