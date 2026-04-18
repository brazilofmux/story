"""
demo_dramatic_reader_model_macbeth.py — invoke the cross-boundary
reader-model probe on the Macbeth encoding.

Builds the cross-boundary surface — Macbeth's Dramatic records,
Macbeth's Lowerings, and the verifier's output on Macbeth — and hands
it to Claude Opus 4.6. The LLM produces:

  - Annotation reviews on the Lowerings (whether each binding's
    annotation is faithful to the records on both sides).
  - Verifier commentaries on the verifier's output (whether each
    review's verdict is sensible; whether the check missed a
    signature).

This is the second-item natural-next-move after the Macbeth Lowerings
+ verifier landed: now that the verifier produces output on Macbeth,
the LLM gets to read that output and comment on it.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_dramatic_reader_model_macbeth

    # Dry run (no API call, prints the full prompt):
    .venv/bin/python3 -m demos.demo_dramatic_reader_model_macbeth --dry-run

    # Save the full structured result as JSON:
    .venv/bin/python3 -m demos.demo_dramatic_reader_model_macbeth \\
        --save-json reader_model_macbeth_dramatic_output.json

    # Restrict to a subset of Lowerings or verifier reviews:
    .venv/bin/python3 -m demos.demo_dramatic_reader_model_macbeth \\
        --lowerings L_macbeth,L_macbeth_dies,L_mc_throughline \\
        --reviews vr_0,vr_2
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict

from story_engine.encodings.macbeth import ENTITIES, FABULA
from story_engine.encodings.macbeth_dramatic import (
    ARGUMENTS, BEATS, CHARACTERS, SCENES, STAKES, THROUGHLINES,
)
from story_engine.encodings.macbeth_lowerings import LOWERINGS
from story_engine.encodings.macbeth_verification import run as run_macbeth_verifier


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
        default=40_000,
        help=(
            "τ_a stamped on produced records (default: 40000). Must "
            "exceed every authored τ_a in the Macbeth encoding "
            "(Lowerings top out around 233; verifier reviews are "
            "stamped at 300; bump on each new probe round)."
        ),
    )
    parser.add_argument(
        "--lowerings",
        metavar="ID,ID,...",
        help=(
            "Comma-separated Lowering ids to review. Default: every "
            "Lowering. Pass an empty string to skip annotation reviews."
        ),
    )
    parser.add_argument(
        "--reviews",
        metavar="ID,ID,...",
        help=(
            "Comma-separated verifier-review synthetic ids ('vr_0', "
            "'vr_1', …) to comment on. Default: every "
            "VerificationReview. Pass an empty string to skip "
            "commentaries."
        ),
    )
    parser.add_argument(
        "--no-substrate-context",
        action="store_true",
        help=(
            "Omit the substrate-context section from the prompt. The "
            "LLM will still see Lowering lower_records as id strings "
            "but won't see the underlying event/entity records."
        ),
    )
    parser.add_argument(
        "--save-json",
        metavar="PATH",
        help="Save the full structured result as JSON to PATH.",
    )
    parser.add_argument(
        "--walk",
        action="store_true",
        help=(
            "After the LLM call returns, drop into the interactive "
            "walker for annotation reviews and verifier commentaries."
        ),
    )
    return parser.parse_args()


def _print_section(title: str) -> None:
    print()
    print("=" * 76)
    print(title)
    print("=" * 76)


def _serialize_result(result, context: dict) -> dict:
    annotation_reviews_dump = []
    for lowering_id, review in result.annotation_review_candidates:
        annotation_reviews_dump.append({
            "target_lowering_id": lowering_id,
            "reviewer_id": review.reviewer_id,
            "reviewed_at_τ_a": review.reviewed_at_τ_a,
            "verdict": review.verdict,
            "anchor_τ_a": review.anchor_τ_a,
            "comment": review.comment,
        })

    commentaries_dump = []
    for c in result.verifier_commentaries:
        target = c.target_review
        commentaries_dump.append({
            "commenter_id": c.commenter_id,
            "commented_at_τ_a": c.commented_at_τ_a,
            "assessment": c.assessment,
            "comment": c.comment,
            "suggested_signature": c.suggested_signature,
            "target_review": {
                "reviewer_id": target.reviewer_id,
                "verdict": target.verdict,
                "match_strength": target.match_strength,
                "target_record": (
                    f"{target.target_record.dialect}:"
                    f"{target.target_record.record_id}"
                ),
                "comment": target.comment,
            },
        })

    dropped_dump = []
    for d in result.dropped:
        raw_dump = (
            d.raw.model_dump() if hasattr(d.raw, "model_dump") else str(d.raw)
        )
        dropped_dump.append({"reason": d.reason, "raw": raw_dump})

    return {
        "context": context,
        "annotation_reviews": annotation_reviews_dump,
        "verifier_commentaries": commentaries_dump,
        "dropped": dropped_dump,
        "raw_output": result.raw_output.model_dump(),
    }


def _parse_csv_or_none(s):
    """Parse a comma-separated string. None → None (use default).
    Empty string → []. Non-empty → list of stripped tokens."""
    if s is None:
        return None
    if s.strip() == "":
        return []
    return [t.strip() for t in s.split(",") if t.strip()]


def main() -> int:
    args = _cli_args()

    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "ERROR: ANTHROPIC_API_KEY is not set. Set it, or pass --dry-run "
            "to print the prompt without calling the API.",
            file=sys.stderr,
        )
        return 1

    verifier_results = run_macbeth_verifier()

    print("Cross-boundary reader-model probe — Macbeth")
    print(f"  model: claude-opus-4-6")
    print(f"  effort: {args.effort}")
    print(f"  Dramatic records: "
          f"{len(ARGUMENTS)} arguments, {len(THROUGHLINES)} throughlines, "
          f"{len(CHARACTERS)} characters, {len(SCENES)} scenes, "
          f"{len(BEATS)} beats, {len(STAKES)} stakes")
    print(f"  Lowerings: {len(LOWERINGS)}")
    print(f"  verifier results: {len(verifier_results)}")
    print(f"  current_τ_a: {args.current_tau_a}")

    lowerings_to_review = _parse_csv_or_none(args.lowerings)
    reviews_to_comment_on = _parse_csv_or_none(args.reviews)

    substrate_events = [] if args.no_substrate_context else list(FABULA)
    substrate_entities = [] if args.no_substrate_context else list(ENTITIES)

    from story_engine.core.dramatic_reader_model_client import invoke_dramatic_reader_model

    result = invoke_dramatic_reader_model(
        arguments=ARGUMENTS,
        throughlines=THROUGHLINES,
        characters=CHARACTERS,
        scenes=SCENES,
        beats=BEATS,
        stakes=STAKES,
        lowerings=LOWERINGS,
        verifier_results=verifier_results,
        substrate_events=substrate_events,
        substrate_entities=substrate_entities,
        lowerings_to_review=lowerings_to_review,
        reviews_to_comment_on=reviews_to_comment_on,
        current_τ_a=args.current_tau_a,
        effort=args.effort,
        dry_run=args.dry_run,
    )

    if args.dry_run:
        return 0

    if args.save_json:
        context = {
            "model": "claude-opus-4-6",
            "effort": args.effort,
            "current_τ_a": args.current_tau_a,
            "lowering_ids": [lw.id for lw in LOWERINGS],
            "verifier_review_count": sum(
                1 for r in verifier_results
                if hasattr(r, "verdict") and hasattr(r, "target_record")
            ),
            "lowerings_to_review": lowerings_to_review,
            "reviews_to_comment_on": reviews_to_comment_on,
            "substrate_context_included": not args.no_substrate_context,
        }
        with open(args.save_json, "w") as f:
            json.dump(
                _serialize_result(result, context),
                f, indent=2, ensure_ascii=False,
            )
        print(f"\n[saved full result to {args.save_json}]")

    _print_section(
        f"ANNOTATION REVIEWS ({len(result.annotation_review_candidates)})"
    )
    if not result.annotation_review_candidates:
        print("  (none)")
    for lowering_id, review in result.annotation_review_candidates:
        print()
        print(f"  target Lowering: {lowering_id}")
        print(f"  reviewer: {review.reviewer_id}")
        print(f"  verdict: {review.verdict}")
        print(f"  anchor_τ_a: {review.anchor_τ_a}")
        if review.comment:
            print(f"  comment:")
            for line in review.comment.splitlines() or [""]:
                print(f"    {line}")

    _print_section(
        f"VERIFIER COMMENTARIES ({len(result.verifier_commentaries)})"
    )
    if not result.verifier_commentaries:
        print("  (none)")
    for c in result.verifier_commentaries:
        print()
        print(f"  target verifier review:")
        print(f"    reviewer: {c.target_review.reviewer_id}")
        print(f"    target_record: "
              f"{c.target_review.target_record.dialect}:"
              f"{c.target_review.target_record.record_id}")
        print(f"    verdict: {c.target_review.verdict}", end="")
        if c.target_review.match_strength is not None:
            print(f"  (match_strength={c.target_review.match_strength:.2f})")
        else:
            print()
        print(f"  commenter: {c.commenter_id}")
        print(f"  assessment: {c.assessment}")
        print(f"  comment:")
        for line in c.comment.splitlines() or [""]:
            print(f"    {line}")
        if c.suggested_signature:
            print(f"  suggested_signature:")
            for line in c.suggested_signature.splitlines() or [""]:
                print(f"    {line}")

    if result.dropped:
        _print_section(f"DROPPED OUTPUTS ({len(result.dropped)})")
        for d in result.dropped:
            print(f"\n  reason: {d.reason}")
            raw_repr = (
                d.raw.model_dump() if hasattr(d.raw, "model_dump")
                else str(d.raw)
            )
            print(f"  raw: {raw_repr}")

    _print_section("SUMMARY")
    for lowering_id, review in result.annotation_review_candidates:
        print(f"  annotation  {lowering_id:<32} {review.verdict}")
    for c in result.verifier_commentaries:
        target_id = c.target_review.target_record.record_id
        print(f"  verifier    {target_id:<32} {c.assessment}")

    if args.walk:
        from story_engine.core.proposal_walker import (
            print_decision_summary,
            walk_annotation_reviews,
            walk_verifier_commentaries,
        )

        _print_section("WALK — ANNOTATION REVIEWS")
        lowerings_after, annotation_decisions = walk_annotation_reviews(
            result.annotation_review_candidates, list(LOWERINGS),
        )

        _print_section("WALK — VERIFIER COMMENTARIES")
        kept_commentaries, commentary_decisions = walk_verifier_commentaries(
            result.verifier_commentaries,
        )

        _print_section("WALK — RESULT")
        all_decisions = annotation_decisions + commentary_decisions
        print_decision_summary(all_decisions)

        print()
        print(f"  lowerings: {len(LOWERINGS)} → {len(lowerings_after)} "
              f"(annotation review_states grew on accepts)")
        print(f"  kept verifier commentaries: {len(kept_commentaries)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
