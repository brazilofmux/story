"""
demo_generate_sworn.py — generate the REVERSE-TOLD original "Sworn" and
score it: structural fidelity AND whether the backward telling was honored.

The hard-telling experiment. The story's structure is ordinary
Aristotelian (it verifies clean); the staging runs in strict reverse. We
generate, then decompile the prose blind and check two things:
  1. did the structural spine survive (peripeteia, anagnorisis, the
     pathos-split, the anti-recognition)? — compare_to_mythos;
  2. did the prose actually tell it BACKWARD? — the blind read's
     `telling_order`, which should come back 'reverse' if the generator
     honored the substrate's staging instead of defaulting to chronology.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_generate_sworn --save-md sworn_first_draft.md
    .venv/bin/python3 -m demos.demo_generate_sworn --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.draft_generator import generate_draft
from story_engine.core.draft_evaluator import decompile_draft, compare_to_mythos
from story_engine.encodings.sworn import (
    FABULA, SJUZHET, DESCRIPTIONS, ENTITIES, PREPLAY_DISCLOSURES,
)
from story_engine.encodings.sworn_aristotelian import AR_SWORN_MYTHOS

_DIALECT_NOTE = (
    "Aristotelian tragedy told in REVERSE chronological order. The staging "
    "opens on the aftermath — the man who never lied, now silent — and "
    "walks backward in time to the boyhood vow. The audience knows the "
    "outcome from the first scene and watches the cause assemble; build the "
    "dramatic irony of a told-backward tragedy in every scene. The "
    "peripeteia is the plain testimony that condemns an innocent; the "
    "pathos-centre (the condemned friend) is distinct from the recognizer "
    "(the witness). Render as spare, grave dramatic prose."
)


def _cli():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--effort", default="medium",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--max-tokens", type=int, default=4000)
    p.add_argument("--save-md", metavar="PATH")
    p.add_argument("--no-evaluate", action="store_true")
    return p.parse_args()


def main() -> int:
    args = _cli()
    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set (or pass --dry-run).",
              file=sys.stderr)
        return 1

    print("Substrate → first-draft generator — Sworn (ORIGINAL, told BACKWARD)")
    print(f"  model: claude-opus-4-6  effort: {args.effort}")
    print(f"  fabula: {len(FABULA)} | sjuzhet: {len(SJUZHET)} (strict reverse) "
          f"| pathos-centre: {', '.join(AR_SWORN_MYTHOS.pathos_character_ref_ids)} "
          f"| recognizer: {AR_SWORN_MYTHOS.anagnorisis_character_ref_id}\n")

    def on_scene(s):
        if args.dry_run:
            print("=" * 72)
            print(f"BRIEF staged-τ_d={s.τ_d} ({s.event_id}) focalizer={s.focalizer}")
            print("=" * 72)
            print(s.brief + "\n")
        else:
            print(f"  [staged #{s.τ_d}] {s.event_id:22s} "
                  f"focalizer={s.focalizer:10s} → {len(s.prose.split())} w")

    result = generate_draft(
        title="Sworn", sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
        descriptions=DESCRIPTIONS, mythos=AR_SWORN_MYTHOS,
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
            f.write(f"# {result.title} — first draft (original, told backward)\n\n")
            f.write("_Generated from a verified ORIGINAL substrate whose sjuzhet "
                    "runs in strict reverse; the engine is the author of record._\n\n")
            f.write(result.draft)
            f.write("\n\n---\n\n## Appendix — story bible\n\n```\n"
                    + result.story_bible + "\n```\n")
        print(f"\n[saved draft to {args.save_md}]")

    if not args.no_evaluate:
        print("\n" + "=" * 72)
        print("EVALUATION — decompile blind: structural fidelity + telling order")
        print("=" * 72)
        decompiled = decompile_draft(
            result.draft, title="Sworn", dialect_note=_DIALECT_NOTE,
            effort="high", max_tokens=8000,
        )
        report = compare_to_mythos(decompiled, AR_SWORN_MYTHOS)
        mark = {"preserved": "✓", "drifted": "~", "lost": "✗", "added": "+"}
        for fnd in report.findings:
            print(f"  {mark.get(fnd.verdict, '?')} {fnd.dimension:22s} "
                  f"authored={fnd.authored!r:30s} read={fnd.decompiled!r}")
        print(f"\n  STRUCTURAL FIDELITY: {report.preserved}/{len(report.scored)} "
              f"preserved ({round(100*report.score)}%)")
        told = (decompiled.telling_order or "").strip().lower()
        ok = "reverse" in told
        print(f"  TELLING ORDER (blind read): {decompiled.telling_order!r} "
              f"→ {'✓ the backward staging was HONORED' if ok else '✗ told in a different order'}")
        print(f"  blind read: pathos-centre="
              f"{', '.join(decompiled.pathos_centre_characters)} | "
              f"recognizer={decompiled.anagnorisis_character}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
