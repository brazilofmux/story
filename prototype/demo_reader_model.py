"""
demo_reader_model.py — invoke the live reader-model over Rashomon.

Builds a ReaderView for :b-woodcutter (the branch with the project's one
authorial-uncertainty open question — D_wc_authorial_doubt), hands it to
Claude Opus 4.6 via the reader-model client, and prints the LLM's reviews
and proposed answers.

This is the first LLM-in-the-loop moment in the project. Prior probes
were mock-only. The output of this demo is the first time interpretation
has been a partner (architecture-sketch-01 A5) rather than a promissory
surface.

Usage:
    cd prototype
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 demo_reader_model.py

    # Dry run (no API call, prints the full prompt):
    .venv/bin/python3 demo_reader_model.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict

from substrate import Attention, reader_view
from rashomon import (
    ALL_BRANCHES,
    B_WOODCUTTER,
    DESCRIPTIONS,
    EVENTS_ALL,
)


def _cli_args():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the full prompt and exit without calling the API.",
    )
    parser.add_argument(
        "--effort",
        default="high",
        choices=["low", "medium", "high", "max"],
        help="output_config.effort (default: high).",
    )
    parser.add_argument(
        "--current-tau-a",
        type=int,
        default=20_000,
        help="τ_a stamped on produced records (default: 20000).",
    )
    parser.add_argument(
        "--save-json",
        metavar="PATH",
        help=(
            "Save the full structured result (reviews, proposed_answers, "
            "raw LLM output) as JSON to PATH. Reviews and proposed "
            "descriptions are serialized in enough detail to round-trip "
            "back into substrate records."
        ),
    )
    return parser.parse_args()


def _print_section(title: str) -> None:
    print()
    print("=" * 76)
    print(title)
    print("=" * 76)


def _serialize_result(result, context: dict) -> dict:
    """Dump ReaderModelResult as plain JSON-friendly dicts. Includes the
    raw LLM output (via Pydantic's model_dump) alongside translated
    substrate records so a reader can reconstruct either view later."""
    def description_to_dict(d):
        data = asdict(d)
        # AnchorRef is a dataclass; asdict handles it. Enum/frozenset need
        # explicit coercion:
        data["attention"] = d.attention.value
        data["status"] = d.status.value
        data["branches"] = sorted(d.branches) if d.branches else None
        # Prop tuples in metadata — none in this probe, but be tolerant:
        return data

    reviews_dump = []
    for rv in result.reviews:
        reviews_dump.append({
            "reviewer_id": rv.reviewer_id,
            "reviewed_at_τ_a": rv.reviewed_at_τ_a,
            "verdict": rv.verdict.value,
            "anchor_τ_a": rv.anchor_τ_a,
            "comment": rv.comment,
        })

    answers_dump = []
    for pa in result.proposed_answers:
        answers_dump.append({
            "question_description_id": pa.question_description_id,
            "proposed_description": description_to_dict(pa.proposed_description),
            "rationale": pa.rationale,
        })

    return {
        "context": context,
        "reviews": reviews_dump,
        "proposed_answers": answers_dump,
        "raw_output": result.raw_output.model_dump(),
    }


def main() -> int:
    args = _cli_args()

    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "ERROR: ANTHROPIC_API_KEY is not set. Set it, or pass --dry-run "
            "to print the prompt without calling the API.",
            file=sys.stderr,
        )
        return 1

    # Build the view. :b-woodcutter has the open question
    # D_wc_authorial_doubt, attached to D_woodcutter_trust (the film's
    # contested-reliability trust flag). Structural + interpretive
    # attention gives the LLM a full spread to judge against.
    view = reader_view(
        branch=B_WOODCUTTER,
        events=EVENTS_ALL,
        descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES,
        up_to_τ_s=100,
        up_to_τ_a=10_000,
        attention_filter=frozenset(
            {Attention.STRUCTURAL, Attention.INTERPRETIVE}
        ),
    )

    print("Reader-model probe — :b-woodcutter")
    print(f"  model: claude-opus-4-6")
    print(f"  effort: {args.effort}")
    print(f"  events in view: {len(view.events)}")
    print(f"  descriptions in view: {len(view.descriptions)}")
    print(f"  open questions: {len(view.open_questions)}")
    if view.open_questions:
        for q in view.open_questions:
            print(f"    · {q.description.id}")
    print(f"  current_τ_a: {args.current_tau_a}")

    # Import the client late so dry-run users without deps can at least
    # get the ImportError message clearly if they skip pip install.
    from reader_model_client import invoke_reader_model

    result = invoke_reader_model(
        view=view,
        events=EVENTS_ALL,
        descriptions=DESCRIPTIONS,
        current_τ_a=args.current_tau_a,
        effort=args.effort,
        dry_run=args.dry_run,
    )

    if args.dry_run:
        # The client's dry_run mode prints the prompt itself.
        return 0

    if args.save_json:
        context = {
            "model": "claude-opus-4-6",
            "effort": args.effort,
            "current_τ_a": args.current_tau_a,
            "branch": view.branch_label,
            "up_to_τ_s": view.up_to_τ_s,
            "up_to_τ_a": view.up_to_τ_a,
            "events_in_view": [r.event.id for r in view.events],
            "descriptions_in_view": [
                r.description.id for r in view.descriptions
            ],
            "open_questions": [r.description.id for r in view.open_questions],
        }
        with open(args.save_json, "w") as f:
            json.dump(
                _serialize_result(result, context),
                f,
                indent=2,
                ensure_ascii=False,
            )
        print(f"\n[saved full result to {args.save_json}]")

    _print_section(f"REVIEWS ({len(result.reviews)})")
    if not result.reviews:
        print("  (none)")
    for rv in result.reviews:
        print()
        print(f"  reviewer: {rv.reviewer_id}")
        print(f"  reviewed_at_τ_a: {rv.reviewed_at_τ_a}")
        print(f"  anchor_τ_a: {rv.anchor_τ_a}")
        print(f"  verdict: {rv.verdict.value}")
        if rv.comment:
            print(f"  comment:")
            for line in rv.comment.splitlines() or [""]:
                print(f"    {line}")

    _print_section(f"PROPOSED ANSWERS ({len(result.proposed_answers)})")
    if not result.proposed_answers:
        print("  (none)")
    for pa in result.proposed_answers:
        d = pa.proposed_description
        print()
        print(f"  answers: {pa.question_description_id}")
        print(f"  proposed description id: {d.id}")
        print(f"    kind: {d.kind}")
        print(f"    attention: {d.attention.value}")
        print(f"    attached_to: {d.attached_to.kind}:{d.attached_to.target_id}")
        print(f"    branches: {sorted(d.branches) if d.branches else '(inherit)'}")
        print(f"    status: {d.status.value}")
        print(f"    text:")
        for line in d.text.splitlines() or [""]:
            print(f"      {line}")
        print(f"    rationale:")
        for line in pa.rationale.splitlines() or [""]:
            print(f"      {line}")

    # Quick mapping from each reviewed description id to verdict, for scan-
    # ability after scrolling through rationale prose.
    _print_section("SUMMARY")
    by_id = {rv.reviewer_id: [] for rv in result.reviews}
    for rv in result.reviews:
        # One reviewer per probe, so this always collapses to a single row.
        pass
    verdicts = {}
    for rv, raw in zip(result.reviews, result.raw_output.reviews):
        verdicts[raw.description_id] = rv.verdict.value
    for desc_id, verdict in verdicts.items():
        print(f"  {desc_id:<38} {verdict}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
