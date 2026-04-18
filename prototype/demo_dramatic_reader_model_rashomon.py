"""
demo_dramatic_reader_model_rashomon.py — cross-boundary reader-model
probe on the Rashomon **multi-Story** dramatica-complete encoding.

First probe run against a multi-Story encoding. Rashomon is five
Stories (S_frame + four testimony Stories) under one StoryEncoding;
per multi-story-sketch-01 MS4, per-Story verification produces five
VerificationReviews. The probe sees all five Stories' records plus
all five reviews together; the probe's own read of how to handle the
multi-Story structure is part of what we're measuring.

Primary signals the probe may engage with:

- **Four testimony DSP_limits declared Timelock, all verifying
  differently.** S_bandit_ver and S_samurai_ver land NEEDS_WORK
  (strength 0.67) because the `frees-husband` events retract
  `bound_to(husband, tree)` in the middle arc, firing LT2's
  retraction signal. S_wife_ver and S_woodcutter_ver land NOTED
  (LT3 weak-fallback, Timelock-consistent). The probe has seen
  Timelock-declared-but-substrate-disagreement before (Rocky sketch-01);
  the question is whether it flags the asymmetry across four testimonies
  as a substantive finding or treats it as four independent checks.

- **S_frame: NOTED coordinating verdict.** Frame carries full
  Dramatica-8 declarations (6 DSPs, Story_goal, Story_consequence,
  DSP_limit=Optionlock) but no ACTIVE Lowerings — grove-only
  substrate scope. The probe may suggest substrate extension, propose
  that frame declarations shouldn't have been encoded without lowering
  scope, or read this as honest deferral.

- **Multi-Story containment structure.** Four StoryRelations of kind
  "contains" (S_frame contains each testimony) + six parallel-to
  relations among the testimonies. Whether the probe picks up on this
  structure from the Dramatic records (each Story has its own
  character_ids, throughline_ids, etc.) is a signal about the
  readability of the multi-Story encoding surface.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 demo_dramatic_reader_model_rashomon.py

    # Dry run (no API call, prints full prompt):
    .venv/bin/python3 demo_dramatic_reader_model_rashomon.py --dry-run

    # Save structured result as JSON:
    .venv/bin/python3 demo_dramatic_reader_model_rashomon.py \\
        --save-json reader_model_rashomon_output.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from rashomon import ENTITIES, EVENTS_ALL
from rashomon_dramatic import (
    ARGUMENTS, BEATS, CHARACTERS, SCENES, STAKES, THROUGHLINES,
    RASHOMON_ENCODING,
)
from rashomon_dramatica_complete import (
    ALL_DOMAIN_ASSIGNMENTS,
    ALL_DYNAMIC_STORY_POINTS,
    STORY_GOAL_FRAME,
    STORY_CONSEQUENCE_FRAME,
)
from rashomon_lowerings import LOWERINGS
from rashomon_dramatica_complete_verification import run as run_rashomon_verifier


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
            "exceed every authored τ_a in the Rashomon encoding."
        ),
    )
    parser.add_argument(
        "--lowerings",
        metavar="ID,ID,...",
        help=(
            "Comma-separated Lowering ids to review. Default: every "
            "Lowering. Pass '' to skip annotation reviews."
        ),
    )
    parser.add_argument(
        "--reviews",
        metavar="ID,ID,...",
        help=(
            "Comma-separated verifier-review synthetic ids ('vr_0', "
            "'vr_1', …) to comment on. Default: every review."
        ),
    )
    parser.add_argument(
        "--no-substrate-context",
        action="store_true",
        help="Omit the substrate-context section from the prompt.",
    )
    parser.add_argument(
        "--no-template-records",
        action="store_true",
        help="Omit the Template-records section from the prompt.",
    )
    parser.add_argument(
        "--save-json",
        metavar="PATH",
        help="Save the full structured result as JSON to PATH.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=20_000,
        help=(
            "max_tokens for the API call (default: 20000). Rashomon's "
            "combined multi-Story payload is large; give the probe room."
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
    if s is None:
        return None
    if s.strip() == "":
        return []
    return [t.strip() for t in s.split(",") if t.strip()]


def _print_multistory_banner() -> None:
    """Print the multi-Story structure so readers of the demo output
    see what scope the probe is being handed."""
    enc = RASHOMON_ENCODING
    print()
    print(f"  StoryEncoding: {enc.title}  (entry: {enc.entry_story_id})")
    for s in enc.stories:
        print(f"    · {s.id:<22} {s.title}")
    contains = [r for r in enc.relations if r.kind == "contains"]
    parallel = [r for r in enc.relations if r.kind == "parallel-to"]
    print(f"  StoryRelations: {len(contains)} contains, "
          f"{len(parallel)} parallel-to")


def main() -> int:
    args = _cli_args()

    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "ERROR: ANTHROPIC_API_KEY is not set. Set it, or pass "
            "--dry-run to print the prompt without calling the API.",
            file=sys.stderr,
        )
        return 1

    verifier_results = run_rashomon_verifier()

    print("Cross-boundary reader-model probe — Rashomon (multi-Story)")
    print(f"  model: claude-opus-4-6")
    print(f"  effort: {args.effort}")
    print(f"  max_tokens: {args.max_tokens}")
    _print_multistory_banner()
    print(f"  Dramatic records (combined across 5 Stories):")
    print(f"    {len(ARGUMENTS)} arguments, {len(THROUGHLINES)} throughlines, "
          f"{len(CHARACTERS)} characters")
    print(f"    {len(SCENES)} scenes, {len(BEATS)} beats, {len(STAKES)} stakes")
    print(f"  Template records (combined):")
    print(f"    {len(ALL_DOMAIN_ASSIGNMENTS)} DomainAssignments, "
          f"{len(ALL_DYNAMIC_STORY_POINTS)} DSPs")
    print(f"    1 Story_goal, 1 Story_consequence (frame only)")
    print(f"  Lowerings: {len(LOWERINGS)}")
    print(f"  verifier results: {len(verifier_results)}")
    print(f"  current_τ_a: {args.current_tau_a}")

    lowerings_to_review = _parse_csv_or_none(args.lowerings)
    reviews_to_comment_on = _parse_csv_or_none(args.reviews)

    substrate_events = [] if args.no_substrate_context else list(EVENTS_ALL)
    substrate_entities = [] if args.no_substrate_context else list(ENTITIES)

    if args.no_template_records:
        template_kwargs = {}
    else:
        template_kwargs = dict(
            domain_assignments=ALL_DOMAIN_ASSIGNMENTS,
            dynamic_story_points=ALL_DYNAMIC_STORY_POINTS,
            story_goal=STORY_GOAL_FRAME,
            story_consequence=STORY_CONSEQUENCE_FRAME,
        )

    from dramatic_reader_model_client import invoke_dramatic_reader_model

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
        max_tokens=args.max_tokens,
        dry_run=args.dry_run,
        **template_kwargs,
    )

    if args.dry_run:
        return 0

    if args.save_json:
        context = {
            "model": "claude-opus-4-6",
            "effort": args.effort,
            "max_tokens": args.max_tokens,
            "current_τ_a": args.current_tau_a,
            "encoding": {
                "id": RASHOMON_ENCODING.id,
                "title": RASHOMON_ENCODING.title,
                "story_ids": [s.id for s in RASHOMON_ENCODING.stories],
                "relation_count": len(RASHOMON_ENCODING.relations),
            },
            "lowering_ids": [lw.id for lw in LOWERINGS],
            "verifier_review_count": len(verifier_results),
            "lowerings_to_review": lowerings_to_review,
            "reviews_to_comment_on": reviews_to_comment_on,
            "substrate_context_included": not args.no_substrate_context,
            "template_records_included": not args.no_template_records,
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
        print(f"  annotation  {lowering_id:<36} {review.verdict}")
    for c in result.verifier_commentaries:
        target_id = c.target_review.target_record.record_id
        print(f"  verifier    {target_id:<36} {c.assessment}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
