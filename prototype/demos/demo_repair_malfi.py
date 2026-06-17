"""
demo_repair_malfi.py — the generate → evaluate → REPAIR → verify loop.

The engine improving its own output against the substrate. Starting from
the generated Malfi draft:

1. EVALUATE — decompile the draft blind, score structural fidelity.
2. PLAN     — map each localizable structural loss to the substrate
              event that carries it (pure Python).
3. REPAIR   — re-render those scenes with a corrective directive.
4. VERIFY   — decompile each repaired scene and confirm the structure
              the substrate specified now reads in the prose.

The first run's known drift: the authored anti-recognition is Antonio's
(mutual, as the blade lands), but the prose rendered Antonio dying
unknowing and relocated the recognition to Bosola. This loop should
re-render that beat so Antonio recognizes too-late, and verify it.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_repair_malfi
    .venv/bin/python3 -m demos.demo_repair_malfi --save-md malfi_repairs.md
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.draft_evaluator import (
    decompile_draft, compare_to_mythos, _name_matches,
)
from story_engine.core.draft_repair import plan_repairs, repair_scene
from story_engine.encodings.malfi import (
    FABULA, SJUZHET, DESCRIPTIONS, ENTITIES, PREPLAY_DISCLOSURES,
)
from story_engine.encodings.malfi_aristotelian import AR_MALFI_MYTHOS

_DIALECT_NOTE = "Aristotelian tragedy (complex plot, distributed fall)."


def _load_draft_prose(path: str) -> str:
    with open(path) as f:
        text = f.read()
    marker = "\n---\n\n## Appendix"
    if marker in text:
        text = text.split(marker, 1)[0]
    lines = [ln for ln in text.splitlines()
             if not ln.startswith("# ") and not ln.startswith("_Generated")]
    return "\n".join(lines).strip()


def _verify_repair(directive, after_prose: str, *, effort, client=None) -> tuple:
    """Decompile the repaired scene alone and confirm the directive's
    structure now reads. Returns (ok: bool, evidence: str)."""
    scene_struct = decompile_draft(
        after_prose, title="The Duchess of Malfi (repaired scene)",
        dialect_note=_DIALECT_NOTE, effort=effort, max_tokens=4000,
        client=client,
    )
    if directive.dimension == "anti_recognition":
        who = directive.authored.split(" (")[0]
        hits = [r for r in scene_struct.staggered_recognitions
                if (r.qualifier or "").lower() == "anti"
                and _name_matches(who, r.character)]
        if hits:
            return True, f"{who} now reads as an anti-recognition: " \
                         f"{hits[0].summary}"
        # peripeteia/anagnorisis fields can also carry the recognition
        if _name_matches(who, scene_struct.anagnorisis_character):
            return True, f"{who} reads as the recognizer: " \
                         f"{scene_struct.anagnorisis}"
        return False, "no anti-recognition on the authored character in " \
                      "the repaired scene"
    if directive.dimension == "anagnorisis_character":
        who = directive.authored
        ok = _name_matches(who, scene_struct.anagnorisis_character)
        return ok, (f"recognizer reads as {scene_struct.anagnorisis_character}"
                    if not ok else f"{who} carries the recognition")
    return False, "no verifier for this dimension"


def _cli_args():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--draft", default="malfi_first_draft.md")
    p.add_argument("--effort", default="high",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--max-tokens", type=int, default=8000)
    p.add_argument("--save-md", metavar="PATH",
                   help="Save the repaired scenes + verdicts to PATH.")
    return p.parse_args()


def main() -> int:
    args = _cli_args()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        return 1
    if not os.path.exists(args.draft):
        print(f"ERROR: draft not found: {args.draft}", file=sys.stderr)
        return 1

    prose = _load_draft_prose(args.draft)
    print("Generate → Evaluate → Repair → Verify — The Duchess of Malfi")
    print(f"  draft: {args.draft} ({len(prose.split())} words)")
    print(f"  model: claude-opus-4-6  effort: {args.effort}\n")

    # 1. EVALUATE
    print("[1/4] EVALUATE — decompiling the draft blind...")
    decompiled = decompile_draft(
        prose, title="The Duchess of Malfi", dialect_note=_DIALECT_NOTE,
        effort=args.effort, max_tokens=args.max_tokens,
    )
    report = compare_to_mythos(decompiled, AR_MALFI_MYTHOS)
    pct = round(100 * report.score)
    print(f"      fidelity: {report.preserved}/{len(report.scored)} "
          f"preserved ({pct}%)")
    losses = [f for f in report.findings if f.verdict in ("lost", "drifted")]
    for f in losses:
        print(f"      ✗ {f.dimension}: authored {f.authored!r} → "
              f"read {f.decompiled!r}")

    # 2. PLAN
    print("\n[2/4] PLAN — localizing repairs to substrate events...")
    directives = plan_repairs(report, AR_MALFI_MYTHOS)
    if not directives:
        print("      no localizable structural drift — the draft is "
              "faithful on the repairable dimensions. Nothing to repair.")
        return 0
    for d in directives:
        print(f"      → repair {d.dimension} at {d.event_id} "
              f"(restore: {d.authored})")

    # 3 + 4. REPAIR + VERIFY (per directive)
    results = []
    for i, d in enumerate(directives, 1):
        print(f"\n[3/4] REPAIR {i}/{len(directives)} — re-rendering "
              f"{d.event_id}...")
        rr = repair_scene(
            d, sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
            descriptions=DESCRIPTIONS, mythos=AR_MALFI_MYTHOS,
            preplay_disclosures=PREPLAY_DISCLOSURES,
            title="The Duchess of Malfi", dialect_note=_DIALECT_NOTE,
            effort="medium", max_tokens=4000,
        )
        if rr is None:
            print(f"      (event {d.event_id} not in sjuzhet — skipped)")
            continue
        print(f"      re-rendered scene τ_d={rr.τ_d} "
              f"({len(rr.after.split())} words)")
        print(f"\n[4/4] VERIFY {i}/{len(directives)} — decompiling the "
              f"repaired scene...")
        ok, evidence = _verify_repair(d, rr.after, effort=args.effort)
        mark = "✓ FIXED" if ok else "✗ STILL DRIFTED"
        print(f"      {mark}: {evidence}")
        results.append((d, rr, ok, evidence))

    fixed = sum(1 for *_, ok, _ in results if ok)
    print(f"\n=== REPAIR LOOP COMPLETE: {fixed}/{len(results)} drifted "
          f"beats repaired and verified ===")

    if args.save_md:
        with open(args.save_md, "w") as f:
            f.write("# The Duchess of Malfi — repair pass\n\n")
            f.write(f"Initial fidelity: {pct}%. "
                    f"{fixed}/{len(results)} drifted beats repaired.\n\n")
            for d, rr, ok, evidence in results:
                f.write(f"## {d.dimension} @ {d.event_id} "
                        f"({'FIXED' if ok else 'STILL DRIFTED'})\n\n")
                f.write(f"**Directive:** {d.instruction}\n\n")
                f.write(f"**Verification:** {evidence}\n\n")
                f.write("**Repaired scene:**\n\n")
                f.write(rr.after + "\n\n---\n\n")
        print(f"[saved repair pass to {args.save_md}]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
