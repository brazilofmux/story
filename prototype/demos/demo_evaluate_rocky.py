"""
demo_evaluate_rocky.py — live confirmation for OQ-AMB-1 (the ambiguity-
honest substrate; design/ambiguity-honest-substrate-sketch-01.md).

Rocky's Outcome is authored DUAL — {failure, success} — because the story
genuinely is both: he loses the decision on the scorecards yet wins
everything the fight was really about. The blind Dramatica evaluator was
already observed to flip failure↔success run-to-run (commit 7165324). The
offline tests encode that flip as faithful; this demo SHOWS it live.

It decompiles `rocky_first_draft.md` BLIND (genre-only note, never the
storyform) N times and reports, per run:
  - the Outcome the reader perceived, and
  - the fidelity verdict for that read.
The claim under test: the Outcome reads SCATTER across {failure, success}
while EVERY read scores `preserved` — the ambiguity is read faithfully, not
as drift — AND the binary Judgment axis stays stably good/preserved (the
control: dual on one axis does not loosen the others).

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_evaluate_rocky            # 5 runs
    .venv/bin/python3 -m demos.demo_evaluate_rocky --runs 7
    .venv/bin/python3 -m demos.demo_evaluate_rocky --dry-run  # prompt only
"""

from __future__ import annotations

import argparse
import os
import sys

from story_engine.core.dramatica_evaluator import (
    decompile_dramatica, compare_to_storyform,
)
from story_engine.core.dramatica_generation import DramaticaStoryform
from story_engine.encodings import rocky_dramatica_complete as RD

_ACTION_SUMMARY = (
    "Rocky Balboa, an aging Philadelphia club fighter, is handed a "
    "one-in-a-million shot at the heavyweight champion Apollo Creed in a "
    "bicentennial publicity bout. He cannot win and knows it; he sets "
    "himself the private goal of going the distance. He goes the full "
    "fifteen rounds and loses the decision — and it does not matter, "
    "because he has done the thing he set out to do and he has Adrian."
)


def _storyform() -> DramaticaStoryform:
    return DramaticaStoryform(
        title="Rocky",
        action_summary=_ACTION_SUMMARY,
        domain_assignments=RD.DOMAIN_ASSIGNMENTS,
        signposts=RD.ALL_SIGNPOSTS,
        dynamics=RD.DYNAMIC_STORY_POINTS,
        story_goal=RD.STORY_GOAL,
        story_consequence=RD.STORY_CONSEQUENCE,
        canonical_ending=RD.CANONICAL_ENDING,
        act_event_ids=RD.ACT_EVENT_IDS,
    )


def _load_draft_prose(path: str) -> str:
    """Read a generated draft markdown and return ONLY the prose — strip
    the title/provenance header and the per-scene-brief appendix."""
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
    p.add_argument("--draft", default="rocky_first_draft.md")
    p.add_argument("--runs", type=int, default=5,
                   help="How many independent blind reads to take.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the decompile prompt and exit (no API).")
    p.add_argument("--effort", default="high",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--max-tokens", type=int, default=6000)
    return p.parse_args()


def _dim(report, name):
    for f in report.findings:
        if f.dimension == name:
            return f
    return None


def main() -> int:
    args = _cli()
    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set (or pass --dry-run).",
              file=sys.stderr)
        return 1
    if not os.path.exists(args.draft):
        print(f"ERROR: draft not found: {args.draft}", file=sys.stderr)
        return 1

    storyform = _storyform()
    out_dsp = {d.axis.value: d for d in RD.DYNAMIC_STORY_POINTS}["outcome"]
    prose = _load_draft_prose(args.draft)
    words = len(prose.split())

    print("Ambiguity-honest live confirmation — OQ-AMB-1 (Rocky Outcome)")
    print(f"  draft: {args.draft}  ({words} words of prose)")
    print(f"  model: claude-opus-4-6  effort: {args.effort}  runs: {args.runs}")
    print(f"  authored Outcome: DUAL span={sorted(out_dsp.poles)} "
          f"leans={out_dsp.leans!r}  | Judgment: binary 'good' (control)")
    print(f"  canonical ending: {RD.CANONICAL_ENDING}")
    print()

    if args.dry_run:
        decompile_dramatica(prose, title="Rocky", effort=args.effort,
                            max_tokens=args.max_tokens, dry_run=True)
        print("\n[dry run — prompt above; no decompilation performed]")
        return 0

    out_tally: dict = {}
    rows = []
    all_outcome_preserved = True
    all_judgment_preserved = True

    for i in range(1, args.runs + 1):
        reading = decompile_dramatica(
            prose, title="Rocky", effort=args.effort,
            max_tokens=args.max_tokens,
        )
        report = compare_to_storyform(reading, storyform)
        o = _dim(report, "outcome")
        j = _dim(report, "judgment")
        out_tally[reading.outcome] = out_tally.get(reading.outcome, 0) + 1
        if o.verdict != "preserved":
            all_outcome_preserved = False
        if j and j.verdict != "preserved":
            all_judgment_preserved = False
        rows.append((i, reading.outcome, o.verdict,
                     reading.judgment, j.verdict if j else "-",
                     reading.ending_shape))
        print(f"  run {i}: outcome={reading.outcome!r:10s} "
              f"{_verdict_mark(o.verdict)}{o.verdict:10s}  "
              f"judgment={reading.judgment!r:7s} "
              f"{_verdict_mark(j.verdict) if j else '?'}{(j.verdict if j else '-'):10s}  "
              f"ending={reading.ending_shape!r}")

    print()
    print("=" * 76)
    print("SCATTER — did the Outcome reads cross the dual span?")
    print("=" * 76)
    for pole in sorted(out_tally):
        in_span = "in-span" if pole.lower() in out_dsp.poles else "OUT-OF-SPAN"
        print(f"  outcome={pole!r:12s} ×{out_tally[pole]}   [{in_span}]")
    distinct = {p.lower() for p in out_tally}
    crossed = len(distinct & out_dsp.poles) >= 2

    print()
    print("=" * 76)
    print("VERDICT")
    print("=" * 76)
    print(f"  Outcome reads scattered across ≥2 spanned poles: "
          f"{'YES' if crossed else 'no'} ({sorted(distinct)})")
    print(f"  EVERY Outcome read scored preserved (ambiguity = faithful): "
          f"{'YES' if all_outcome_preserved else 'NO'}")
    print(f"  Judgment (binary control) stayed preserved every run: "
          f"{'YES' if all_judgment_preserved else 'NO'}")
    print()
    if crossed and all_outcome_preserved:
        print("  → OQ-AMB-1 CONFIRMED: the run-to-run flip is read as the real "
              "ambiguity it is, not as drift. The dual value earns its keep.")
    elif all_outcome_preserved and not crossed:
        print("  → PARTIAL: every read preserved, but the reads did not scatter "
              "this session (the prose may read stably to one pole today). "
              "The dual still scores honestly; re-run for more spread.")
    else:
        print("  → NOT CONFIRMED: an Outcome read fell outside the dual span. "
              "Report honestly; do not widen the span to chase it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
