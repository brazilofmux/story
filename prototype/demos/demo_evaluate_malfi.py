"""
demo_evaluate_malfi.py — decompile the generated Malfi draft and score
its structural fidelity (terminus #2, first run).

Closes the generation loop: substrate → prose (demo_generate_malfi) →
structure (blind decompile) → fidelity score (compare to the substrate
the draft came from). Answers "is the generated draft structurally
good?" — did the prose carry the Duchess's pathos-centre, Ferdinand's
recognition, Antonio's anti-recognition, and the multi-arc fall?

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_evaluate_malfi

    # Inspect the prompt the decompiler would send, no API call:
    .venv/bin/python3 -m demos.demo_evaluate_malfi --dry-run

    # Point at a different draft markdown:
    .venv/bin/python3 -m demos.demo_evaluate_malfi --draft malfi_first_draft.md
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.draft_evaluator import (
    decompile_draft, compare_to_mythos,
)
from story_engine.encodings.malfi_aristotelian import AR_MALFI_MYTHOS


def _load_draft_prose(path: str) -> str:
    """Read a generated draft markdown and return ONLY the prose — strip
    the title/italic header and the per-scene-brief appendix."""
    with open(path) as f:
        text = f.read()
    # Drop the appendix (briefs + bible) — the decompiler reads prose only.
    marker = "\n---\n\n## Appendix"
    if marker in text:
        text = text.split(marker, 1)[0]
    # Drop the leading "# Title — first draft" + italic provenance line.
    lines = text.splitlines()
    body = [ln for ln in lines
            if not ln.startswith("# ") and not ln.startswith("_Generated")]
    return "\n".join(body).strip()


def _cli_args():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--draft", default="malfi_first_draft.md",
                   help="Path to the generated draft markdown.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the decompile prompt and exit (no API).")
    p.add_argument("--effort", default="high",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--max-tokens", type=int, default=8000)
    return p.parse_args()


def _verdict_mark(v: str) -> str:
    return {"preserved": "✓", "drifted": "~", "lost": "✗",
            "added": "+"}.get(v, "?")


def main() -> int:
    args = _cli_args()
    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set (or pass --dry-run).",
              file=sys.stderr)
        return 1

    if not os.path.exists(args.draft):
        print(f"ERROR: draft not found: {args.draft} "
              f"(run demos.demo_generate_malfi --save-md first).",
              file=sys.stderr)
        return 1

    prose = _load_draft_prose(args.draft)
    words = len(prose.split())

    print("Draft evaluator — decompile + structural fidelity (Malfi)")
    print(f"  draft: {args.draft}  ({words} words of prose)")
    print(f"  model: claude-opus-4-6  effort: {args.effort}")
    print(f"  authored spine: pathos-centre="
          f"{', '.join(AR_MALFI_MYTHOS.pathos_character_ref_ids)} | "
          f"recognizer={AR_MALFI_MYTHOS.anagnorisis_character_ref_id} | "
          f"secondary reversals="
          f"{len(AR_MALFI_MYTHOS.secondary_peripeteia_event_ids)}")
    print()

    decompiled = decompile_draft(
        prose,
        title="The Duchess of Malfi",  # genre-only note (blind)
        effort=args.effort,
        max_tokens=args.max_tokens,
        dry_run=args.dry_run,
    )
    if args.dry_run:
        print("\n[dry run — prompt above; no decompilation performed]")
        return 0

    print("=" * 76)
    print("BLIND DECOMPILATION (the structure the prose alone supports)")
    print("=" * 76)
    print(f"  plot_kind: {decompiled.plot_kind}  | "
          f"unity_of_action: {decompiled.unity_of_action}")
    print(f"  peripeteia: {decompiled.peripeteia_character} — "
          f"{decompiled.peripeteia}")
    print(f"  anagnorisis: {decompiled.anagnorisis_character} — "
          f"{decompiled.anagnorisis}")
    print(f"  pathos-centre: {', '.join(decompiled.pathos_centre_characters)}")
    print(f"  tragic hero(es): "
          f"{', '.join(decompiled.tragic_hero_characters)}")
    if decompiled.staggered_recognitions:
        print("  staggered recognitions:")
        for r in decompiled.staggered_recognitions:
            q = f" [{r.qualifier}]" if r.qualifier else ""
            print(f"    - {r.character}{q}: {r.summary}")
    if decompiled.secondary_reversals:
        print("  secondary reversals:")
        for s in decompiled.secondary_reversals:
            print(f"    - {s}")
    print(f"  overall: {decompiled.overall_read}")
    print()

    report = compare_to_mythos(decompiled, AR_MALFI_MYTHOS)
    print("=" * 76)
    print("STRUCTURAL FIDELITY — substrate → prose → substrate round-trip")
    print("=" * 76)
    for f in report.findings:
        print(f"  {_verdict_mark(f.verdict)} {f.dimension:22s} "
              f"authored={f.authored!r:42s} read={f.decompiled!r}")
        if f.note:
            print(f"      → {f.note}")
    print()
    pct = round(100 * report.score)
    print(f"  FIDELITY SCORE: {report.preserved}/{len(report.scored)} "
          f"structural dimensions preserved ({pct}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
