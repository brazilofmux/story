"""
demo_crosscheck_malfi.py — cross-MODEL blind decompile of one draft.

The same generated draft (substrate → prose) is read BLIND by two
different model families — Claude and Grok — in the Aristotelian dialect,
and each reading is scored against the substrate the draft came from. Then
the two readings are diffed against EACH OTHER.

Why this and not single-model scoring: a fidelity score from one model is
that model grading prose another instance of the same model wrote — and
same-family voting just amplifies a shared blind spot rather than checking
it (the manufactured-agreement trap). Bringing in a genuinely different
family (xAI's Grok) makes agreement load-bearing: when Claude AND Grok
independently read the same peripeteia, the same pathos-centre, the same
recognizer out of the prose, that's corroboration the substrate actually
landed in the text. Where they DISAGREE is exactly where the prose is
ambiguous — the honest signal, not noise to average away.

The provider is chosen by the model name (see story_engine/core/llm.py):
`claude-*` routes to Anthropic, `grok-*` to xAI. Pass any model ids you
have keys for via --models.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...        # for the claude-* arm
    export XAI_API_KEY=...              # for the grok-* arm
    .venv/bin/python3 -m demos.demo_crosscheck_malfi
    .venv/bin/python3 -m demos.demo_crosscheck_malfi --models claude-opus-4-6,grok-4.3
    .venv/bin/python3 -m demos.demo_crosscheck_malfi --dry-run     # prompt only, one model
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from story_engine.core.llm import provider_for
from story_engine.core.draft_evaluator import (
    decompile_draft, compare_to_mythos,
)
from story_engine.encodings.malfi_aristotelian import AR_MALFI_MYTHOS


def _load_prose_from_json(path: str) -> str:
    """Assemble the draft prose from a saved generation payload (the shape
    `draft_generator.result_to_payload` emits): scenes in sjuzhet order,
    prose joined. Prose only — no bible, no briefs — to keep the read blind."""
    with open(path) as f:
        payload = json.load(f)
    scenes = sorted(payload.get("scenes", []), key=lambda s: s.get("tau_d", 0))
    return "\n\n".join(s.get("prose", "").strip() for s in scenes).strip()


# The dimensions we cross-check between the two blind readings. Each maps a
# DecompiledStructure field to a small normalizer so "Ferdinand" / "ferdinand."
# compare equal and lists compare order-insensitively.
def _norm_scalar(v):
    return (str(v).strip().lower().rstrip(".") if v is not None else "")


def _norm_set(v):
    return frozenset(_norm_scalar(x) for x in (v or []) if _norm_scalar(x))


_CROSS_DIMS = [
    ("plot_kind", _norm_scalar),
    ("unity_of_action", _norm_scalar),
    ("peripeteia_character", _norm_scalar),
    ("anagnorisis_character", _norm_scalar),
    ("pathos_centre_characters", _norm_set),
    ("tragic_hero_characters", _norm_set),
]


def _verdict_mark(v: str) -> str:
    return {"preserved": "✓", "drifted": "~", "lost": "✗",
            "added": "+"}.get(v, "?")


def _print_reading(model: str, reading) -> None:
    print("-" * 76)
    print(f"BLIND READING — {model}  (provider: {provider_for(model)})")
    print("-" * 76)
    print(f"  plot_kind: {reading.plot_kind}  | "
          f"unity_of_action: {reading.unity_of_action}")
    print(f"  peripeteia: {reading.peripeteia_character} — {reading.peripeteia}")
    print(f"  anagnorisis: {reading.anagnorisis_character} — "
          f"{reading.anagnorisis}")
    print(f"  pathos-centre: {', '.join(reading.pathos_centre_characters)}")
    print(f"  tragic hero(es): {', '.join(reading.tragic_hero_characters)}")
    print()


def _cli():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--draft", default="malfi_draft.json",
                   help="Saved generation payload (result_to_payload JSON).")
    p.add_argument("--models", default="claude-opus-4-6,grok-4.3",
                   help="Comma-separated model ids; provider inferred by name.")
    p.add_argument("--effort", default="high",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--max-tokens", type=int, default=8000)
    p.add_argument("--dry-run", action="store_true",
                   help="Print the decompile prompt for the FIRST model, exit.")
    return p.parse_args()


def _key_missing(model: str) -> str:
    """Return the name of the missing API-key env var for `model`, or ''."""
    prov = provider_for(model)
    if prov == "anthropic" and not os.environ.get("ANTHROPIC_API_KEY"):
        return "ANTHROPIC_API_KEY"
    if prov == "xai" and not os.environ.get("XAI_API_KEY"):
        return "XAI_API_KEY"
    return ""


def main() -> int:
    args = _cli()
    models = [m.strip() for m in args.models.split(",") if m.strip()]

    if not os.path.exists(args.draft):
        print(f"ERROR: draft not found: {args.draft}", file=sys.stderr)
        return 1
    prose = _load_prose_from_json(args.draft)
    words = len(prose.split())

    print("Cross-model blind decompile — Aristotelian fidelity (Malfi)")
    print(f"  draft: {args.draft}  ({words} words of prose)")
    print(f"  models: {', '.join(models)}")
    print(f"  authored spine: pathos-centre="
          f"{', '.join(AR_MALFI_MYTHOS.pathos_character_ref_ids)} | "
          f"recognizer={AR_MALFI_MYTHOS.anagnorisis_character_ref_id}")
    print()

    if args.dry_run:
        decompile_draft(prose, title="The Duchess of Malfi",
                        model=models[0], effort=args.effort,
                        max_tokens=args.max_tokens, dry_run=True)
        print("\n[dry run — prompt above; no decompilation performed]")
        return 0

    readings: dict = {}
    for model in models:
        missing = _key_missing(model)
        if missing:
            print(f"  SKIP {model}: {missing} not set.", file=sys.stderr)
            continue
        reading = decompile_draft(
            prose, title="The Duchess of Malfi", model=model,
            effort=args.effort, max_tokens=args.max_tokens,
        )
        readings[model] = reading
        _print_reading(model, reading)
        report = compare_to_mythos(reading, AR_MALFI_MYTHOS)
        pct = round(100 * report.score)
        print(f"  {model} FIDELITY vs substrate: "
              f"{report.preserved}/{len(report.scored)} preserved ({pct}%)")
        for f in report.findings:
            print(f"    {_verdict_mark(f.verdict)} {f.dimension:22s} "
                  f"authored={f.authored!r:36s} read={f.decompiled!r}")
        print()

    # Cross-model agreement — the load-bearing part.
    if len(readings) >= 2:
        names = list(readings.keys())
        a, b = names[0], names[1]
        ra, rb = readings[a], readings[b]
        print("=" * 76)
        print(f"CROSS-MODEL AGREEMENT — {a}  vs  {b}")
        print("(where two different families read the SAME structure out of "
              "the prose)")
        print("=" * 76)
        agree = 0
        for field, norm in _CROSS_DIMS:
            va, vb = getattr(ra, field, None), getattr(rb, field, None)
            same = norm(va) == norm(vb)
            agree += same
            mark = "=" if same else "≠"
            print(f"  {mark} {field:26s} {a}={_show(va)!r:32s} "
                  f"{b}={_show(vb)!r}")
        print()
        print(f"  AGREEMENT: {agree}/{len(_CROSS_DIMS)} structural dimensions "
              f"read identically across families.")
        print("  Disagreements mark where the prose is genuinely ambiguous — "
              "the honest signal.")
    elif len(readings) == 1:
        print("Only one model ran — set the other provider's key for the "
              "cross-check.", file=sys.stderr)
    return 0


def _show(v):
    if isinstance(v, (list, tuple)):
        return ", ".join(str(x) for x in v)
    return v


if __name__ == "__main__":
    raise SystemExit(main())
