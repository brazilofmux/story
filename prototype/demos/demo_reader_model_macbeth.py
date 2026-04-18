"""
demo_reader_model_macbeth.py — invoke the live reader-model over Macbeth.

Builds a ReaderView on the canonical branch through Malcolm's coronation
(τ_s ≤ 18, the full play) and hands it to Claude Opus 4.6. Macbeth's
seven descriptions include two authorial-uncertainty questions the
encoding leaves open (the Witches' ontology, the banquet ghost's
ontology), a third authorial-uncertainty marker for the now-retired
compound-predicate derivations, plus reader-frames on the moral
trajectory, the prophecy-ambiguity structure, and Lady Macbeth's
inverse arc.

Purpose: second live-LLM probe on a substrate encoding, structurally
different from Oedipus. Expected value: (a) confirms the probe
generalizes to a new encoding; (b) may surface reviews or edits that
press on the description surface in ways the Oedipus probe did not;
(c) may produce interesting answer-proposals on the two genuine open
questions about supernatural ontology; (d) given the encoding's
cumulative moral trajectory, may surface observations relevant to the
Claim-trajectory verifier primitive specified in verification-sketch-01.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_reader_model_macbeth

    # Dry run (no API call, prints the full prompt):
    .venv/bin/python3 -m demos.demo_reader_model_macbeth --dry-run

    # Save the full structured result as JSON:
    .venv/bin/python3 -m demos.demo_reader_model_macbeth --save-json reader_model_macbeth_output.json

    # Walk the probe's output interactively:
    .venv/bin/python3 -m demos.demo_reader_model_macbeth --walk
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict

from story_engine.core.substrate import (
    Attention,
    CANONICAL,
    ingest_edit_proposal,
    ingest_question_answer,
    reader_view,
)
from story_engine.encodings.macbeth import (
    ALL_BRANCHES,
    DESCRIPTIONS,
    FABULA,
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
        default=30_000,
        help=(
            "τ_a stamped on produced records (default: 30000). "
            "Must be strictly greater than every τ_a currently "
            "authored in the encoding. Macbeth's descriptions top "
            "out at τ_a=106; any walker-accepted records from prior "
            "rounds bump the high-water mark further. Bump this on "
            "every new probe round."
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
            "After the LLM call returns, drop into the interactive walker "
            "for reviews, answer proposals, and edit proposals."
        ),
    )
    return parser.parse_args()


def _print_section(title: str) -> None:
    print()
    print("=" * 76)
    print(title)
    print("=" * 76)


def _serialize_result(result, context: dict) -> dict:
    def description_to_dict(d):
        data = asdict(d)
        data["attention"] = d.attention.value
        data["status"] = d.status.value
        data["branches"] = sorted(d.branches) if d.branches else None
        return data

    reviews_dump = []
    for target_id, rv in result.review_candidates:
        reviews_dump.append({
            "target_description_id": target_id,
            "reviewer_id": rv.reviewer_id,
            "reviewed_at_τ_a": rv.reviewed_at_τ_a,
            "verdict": rv.verdict.value,
            "anchor_τ_a": rv.anchor_τ_a,
            "comment": rv.comment,
        })

    answers_dump = []
    for pa in result.answer_proposals:
        answers_dump.append({
            "question_description_id": pa.question_description_id,
            "proposed_description": description_to_dict(pa.proposed_description),
            "proposer_id": pa.proposer_id,
            "rationale": pa.rationale,
            "proposed_at_τ_a": pa.proposed_at_τ_a,
            "status": pa.status,
        })

    edits_dump = []
    for ep in result.edit_proposals:
        edits_dump.append({
            "source_description_id": ep.source_description_id,
            "proposed_description": description_to_dict(ep.proposed_description),
            "proposer_id": ep.proposer_id,
            "rationale": ep.rationale,
            "proposed_at_τ_a": ep.proposed_at_τ_a,
            "status": ep.status,
        })

    dropped_dump = []
    for d in result.dropped:
        raw_dump = d.raw.model_dump() if hasattr(d.raw, "model_dump") else str(d.raw)
        dropped_dump.append({"reason": d.reason, "raw": raw_dump})

    return {
        "context": context,
        "review_candidates": reviews_dump,
        "answer_proposals": answers_dump,
        "edit_proposals": edits_dump,
        "dropped": dropped_dump,
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

    # View spans the full Macbeth fabula through Malcolm's coronation
    # (τ_s ≤ 18). up_to_τ_a is set generously past every authored
    # record — macbeth.py's descriptions top out at τ_a=106, so the
    # bound has plenty of headroom for walker-accepted records from
    # earlier rounds.
    view = reader_view(
        branch=CANONICAL,
        events=FABULA,
        descriptions=DESCRIPTIONS,
        all_branches=ALL_BRANCHES,
        up_to_τ_s=18,
        up_to_τ_a=1_000_000,
        attention_filter=frozenset(
            {Attention.STRUCTURAL, Attention.INTERPRETIVE}
        ),
    )

    print("Reader-model probe — Macbeth :canonical, full play")
    print(f"  model: claude-opus-4-6")
    print(f"  effort: {args.effort}")
    print(f"  events in view: {len(view.events)}")
    print(f"  descriptions in view: {len(view.descriptions)}")
    print(f"  open questions: {len(view.open_questions)}")
    if view.open_questions:
        for q in view.open_questions:
            print(f"    · {q.description.id}")
    print(f"  current_τ_a: {args.current_tau_a}")

    from story_engine.core.reader_model_client import invoke_reader_model

    result = invoke_reader_model(
        view=view,
        events=FABULA,
        descriptions=DESCRIPTIONS,
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

    _print_section(f"REVIEWS ({len(result.review_candidates)})")
    if not result.review_candidates:
        print("  (none)")
    for target_id, rv in result.review_candidates:
        print()
        print(f"  target: {target_id}")
        print(f"  reviewer: {rv.reviewer_id}")
        print(f"  reviewed_at_τ_a: {rv.reviewed_at_τ_a}")
        print(f"  anchor_τ_a: {rv.anchor_τ_a}")
        print(f"  verdict: {rv.verdict.value}")
        if rv.comment:
            print(f"  comment:")
            for line in rv.comment.splitlines() or [""]:
                print(f"    {line}")

    if result.dropped:
        _print_section(f"DROPPED OUTPUTS ({len(result.dropped)})")
        for d in result.dropped:
            print(f"\n  reason: {d.reason}")
            raw_repr = d.raw.model_dump() if hasattr(d.raw, "model_dump") else str(d.raw)
            print(f"  raw: {raw_repr}")

    _print_section(f"ANSWER PROPOSALS ({len(result.answer_proposals)})")
    if not result.answer_proposals:
        print("  (none)")
    for pa in result.answer_proposals:
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

    _print_section(f"EDIT PROPOSALS ({len(result.edit_proposals)})")
    if not result.edit_proposals:
        print("  (none)")
    for ep in result.edit_proposals:
        d = ep.proposed_description
        print()
        print(f"  source: {ep.source_description_id}")
        print(f"  proposed description id: {d.id}")
        print(f"    kind: {d.kind}")
        print(f"    new text:")
        for line in d.text.splitlines() or [""]:
            print(f"      {line}")
        print(f"    rationale:")
        for line in ep.rationale.splitlines() or [""]:
            print(f"      {line}")

    _print_section("SUMMARY")
    for target_id, rv in result.review_candidates:
        print(f"  {target_id:<44} {rv.verdict.value}")

    if args.walk:
        from story_engine.core.proposal_walker import (
            print_decision_summary,
            walk_answer_proposals,
            walk_edit_proposals,
            walk_reviews,
        )

        _print_section("WALK — REVIEWS")
        descriptions_after, review_decisions = walk_reviews(
            result.review_candidates, list(DESCRIPTIONS),
        )

        queue: list = []
        for ap in result.answer_proposals:
            queue = ingest_question_answer(ap, queue)
        for ep in result.edit_proposals:
            queue = ingest_edit_proposal(ep, queue)

        _print_section("WALK — ANSWER PROPOSALS")
        descriptions_after, queue_after, answer_decisions = walk_answer_proposals(
            queue, descriptions_after,
        )

        _print_section("WALK — EDIT PROPOSALS")
        descriptions_after, queue_after, edit_decisions = walk_edit_proposals(
            queue_after, descriptions_after,
        )

        _print_section("WALK — RESULT")
        all_decisions = review_decisions + answer_decisions + edit_decisions
        print_decision_summary(all_decisions)

        print()
        print(
            f"  descriptions: {len(DESCRIPTIONS)} → {len(descriptions_after)}"
        )
        print(f"  queue entries: {len(queue_after)} (status per entry:)")
        for entry in queue_after:
            q_id = (
                getattr(entry, "question_description_id", None)
                or getattr(entry, "source_description_id", None)
                or getattr(entry, "description_id", None)
                or "?"
            )
            kind = type(entry).__name__
            print(f"    {q_id:<44} {kind:<18} {entry.status}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
