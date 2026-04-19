"""
demo_aristotelian_reader_model_rashomon.py — invoke the Aristotelian
reader-model probe on the Rashomon multi-mythos Aristotelian
encoding.

Stress-case invocation. Aristotelian-sketch-01 predicted that
Rashomon would encode as a **multi-mythos tuple** — four ArMythos
records, one per testimony, sharing canonical-floor events as a
common beginning phase. The stress-case analysis named two
specific dialect-scope tensions — (a) the four testimonies contest
the same canonical-floor events; (b) no testifier experiences
character-level anagnorisis ("meta-anagnorisis" is audience-level
only). The probe is invited to engage these.

Predictions from aristotelian-probe-sketch-01 APS6, specific to
this invocation:

- P2: ≥ 1 of the 20 prose reviews surfaces a dialect-scope
  tension — typically on an action_summary (one testimony's
  "noble combat" reading of events another testimony reads
  oppositely) or on a hamartia_text (a tragic-hero claim inside
  one testimony's reading that another contradicts).
- P3: `observation_commentaries` is empty — Rashomon verifies
  with zero observations per aristotelian-sketch-01 AA5.
- P4: DialectReading.read_on_terms = "yes" or "partial"; no
  Dramatica drift. scope_limits_observed likely non-empty
  (meta-anagnorisis class).
- P5 (exploratory): `relations_wanted` names ArMythosRelation or
  a semantic equivalent — would be a probe-surfaced forcing
  function for a hypothetical aristotelian-sketch-02.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_rashomon

    # Dry run (no API call, prints the full prompt):
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_rashomon \\
        --dry-run

    # Save the full structured result as JSON:
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_rashomon \\
        --save-json reader_model_rashomon_aristotelian_output.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from story_engine.core.aristotelian import verify
from story_engine.core.aristotelian_reader_model_client import (
    invoke_aristotelian_reader_model,
)
from story_engine.encodings.rashomon import EVENTS_ALL
from story_engine.encodings.rashomon_aristotelian import (
    AR_RASHOMON_MYTHOI,
)


def _cli_args():
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n\n", 1)[0]
    )
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
        default=50_000,
        help=(
            "τ_a stamped on produced records (default: 50000). "
            "Must exceed every authored τ_a in the encoding."
        ),
    )
    parser.add_argument(
        "--anchor-tau-a",
        type=int,
        default=None,
        help=(
            "τ_a the encoding was last authored at (default: "
            "current_tau_a). Used as the ArAnnotationReview's "
            "anchor_τ_a for staleness."
        ),
    )
    parser.add_argument(
        "--no-substrate-context",
        action="store_true",
        help="Omit the substrate-context section from the prompt.",
    )
    parser.add_argument(
        "--save-json",
        metavar="PATH",
        help="Save the full structured result as JSON to PATH.",
    )
    return parser.parse_args()


def _print_section(title: str) -> None:
    print()
    print("=" * 76)
    print(title)
    print("=" * 76)


def _serialize_result(result, context: dict) -> dict:
    annotation_dump = []
    for r in result.annotation_reviews:
        annotation_dump.append({
            "target_kind": r.target_kind,
            "target_id": r.target_id,
            "field": r.field,
            "reviewer_id": r.reviewer_id,
            "reviewed_at_τ_a": r.reviewed_at_τ_a,
            "anchor_τ_a": r.anchor_τ_a,
            "verdict": r.verdict,
            "comment": r.comment,
        })

    commentaries_dump = []
    for c in result.observation_commentaries:
        target = c.target_observation
        commentaries_dump.append({
            "commenter_id": c.commenter_id,
            "commented_at_τ_a": c.commented_at_τ_a,
            "assessment": c.assessment,
            "comment": c.comment,
            "suggested_signature": c.suggested_signature,
            "target_observation": {
                "severity": target.severity,
                "code": target.code,
                "target_id": target.target_id,
                "message": target.message,
            },
        })

    dialect_reading_dump = None
    if result.dialect_reading is not None:
        dr = result.dialect_reading
        dialect_reading_dump = {
            "reader_id": dr.reader_id,
            "read_at_τ_a": dr.read_at_τ_a,
            "read_on_terms": dr.read_on_terms,
            "rationale": dr.rationale,
            "drift_flagged": list(dr.drift_flagged),
            "scope_limits_observed": list(dr.scope_limits_observed),
            "relations_wanted": list(dr.relations_wanted),
        }

    dropped_dump = []
    for d in result.dropped:
        raw_dump = (
            d.raw.model_dump() if hasattr(d.raw, "model_dump")
            else str(d.raw)
        )
        dropped_dump.append({"reason": d.reason, "raw": raw_dump})

    return {
        "context": context,
        "annotation_reviews": annotation_dump,
        "observation_commentaries": commentaries_dump,
        "dialect_reading": dialect_reading_dump,
        "dropped": dropped_dump,
        "raw_output": result.raw_output.model_dump(),
    }


def main() -> int:
    args = _cli_args()

    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "ERROR: ANTHROPIC_API_KEY is not set. Set it, or pass "
            "--dry-run to print the prompt without calling the API.",
            file=sys.stderr,
        )
        return 1

    # Verify each mythos; concatenate observations for the probe.
    # Expected: zero observations across all four (per
    # aristotelian-sketch-01 AA5).
    observations: tuple = ()
    for mythos in AR_RASHOMON_MYTHOI:
        observations = observations + tuple(verify(
            mythos, substrate_events=EVENTS_ALL,
        ))

    phase_count = sum(len(m.phases) for m in AR_RASHOMON_MYTHOI)
    character_count = sum(len(m.characters) for m in AR_RASHOMON_MYTHOI)

    print("Aristotelian reader-model probe — Rashomon (stress case)")
    print(f"  model: claude-opus-4-6")
    print(f"  effort: {args.effort}")
    print(f"  mythoi: {len(AR_RASHOMON_MYTHOI)} "
          f"({', '.join(m.id for m in AR_RASHOMON_MYTHOI)})")
    print(f"  phases: {phase_count}")
    print(f"  characters: {character_count}")
    print(f"  observations: {len(observations)}")
    print(f"  substrate events (for grounding): {len(EVENTS_ALL)}")
    print(f"  current_τ_a: {args.current_tau_a}")
    print(f"  anchor_τ_a: {args.anchor_tau_a or args.current_tau_a}")

    substrate_events = (
        [] if args.no_substrate_context else list(EVENTS_ALL)
    )

    result = invoke_aristotelian_reader_model(
        mythoi=AR_RASHOMON_MYTHOI,
        observations=observations,
        substrate_events=substrate_events,
        current_τ_a=args.current_tau_a,
        anchor_τ_a=args.anchor_tau_a,
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
            "anchor_τ_a": args.anchor_tau_a or args.current_tau_a,
            "mythoi_ids": [m.id for m in AR_RASHOMON_MYTHOI],
            "observation_count": len(observations),
            "substrate_context_included": (
                not args.no_substrate_context
            ),
        }
        with open(args.save_json, "w") as f:
            json.dump(
                _serialize_result(result, context),
                f, indent=2, ensure_ascii=False,
            )
        print(f"\n[saved full result to {args.save_json}]")

    _print_section(
        f"ANNOTATION REVIEWS ({len(result.annotation_reviews)})"
    )
    if not result.annotation_reviews:
        print("  (none)")
    # Group by target_kind for easier reading at 20 reviews
    for kind in ("ArMythos", "ArPhase", "ArCharacter"):
        kind_reviews = [
            r for r in result.annotation_reviews if r.target_kind == kind
        ]
        if not kind_reviews:
            continue
        print(f"\n  --- {kind} reviews ({len(kind_reviews)}) ---")
        for r in kind_reviews:
            print()
            print(f"  target: {r.target_kind}:{r.target_id}:{r.field}")
            print(f"  verdict: {r.verdict}")
            if r.comment:
                print(f"  comment:")
                for line in r.comment.splitlines() or [""]:
                    print(f"    {line}")

    _print_section(
        f"OBSERVATION COMMENTARIES "
        f"({len(result.observation_commentaries)})"
    )
    if not result.observation_commentaries:
        print("  (none — as expected; Rashomon verifies clean)")
    for c in result.observation_commentaries:
        print()
        print(f"  target observation: "
              f"[{c.target_observation.severity}] "
              f"{c.target_observation.code}")
        print(f"  assessment: {c.assessment}")
        if c.comment:
            print(f"  comment:")
            for line in c.comment.splitlines() or [""]:
                print(f"    {line}")
        if c.suggested_signature:
            print(f"  suggested_signature: {c.suggested_signature}")

    _print_section("DIALECT READING")
    if result.dialect_reading is None:
        print("  (none — refusal or malformed response)")
    else:
        dr = result.dialect_reading
        print(f"  read_on_terms: {dr.read_on_terms}")
        print(f"  rationale:")
        for line in dr.rationale.splitlines() or [""]:
            print(f"    {line}")
        print(f"  drift_flagged: "
              f"{list(dr.drift_flagged) if dr.drift_flagged else '(empty)'}")
        print(f"  scope_limits_observed:")
        if not dr.scope_limits_observed:
            print(f"    (empty)")
        for s in dr.scope_limits_observed:
            print(f"    - {s}")
        print(f"  relations_wanted:")
        if not dr.relations_wanted:
            print(f"    (empty)")
        for r in dr.relations_wanted:
            print(f"    - {r}")

    if result.dropped:
        _print_section(f"DROPPED OUTPUTS ({len(result.dropped)})")
        for d in result.dropped:
            print(f"\n  reason: {d.reason}")
            raw_repr = (
                d.raw.model_dump() if hasattr(d.raw, "model_dump")
                else str(d.raw)
            )
            print(f"  raw: {raw_repr}")

    _print_section("SUMMARY — check against sketch predictions")
    total = len(result.annotation_reviews)
    non_approved = sum(
        1 for r in result.annotation_reviews
        if r.verdict in ("needs-work", "noted")
    )
    tension_surfaced = non_approved >= 1
    print(
        f"  P2: {non_approved} of {total} prose reviews surfaced a "
        f"non-approved verdict: "
        f"{'PASS' if tension_surfaced else 'FAIL'}"
    )
    p3_pass = len(result.observation_commentaries) == 0
    print(
        f"  P3: observation_commentaries empty: "
        f"{'PASS' if p3_pass else 'FAIL'}"
    )
    if result.dialect_reading is not None:
        dr = result.dialect_reading
        p4_pass = (
            dr.read_on_terms in ("yes", "partial")
            and not dr.drift_flagged
        )
        print(
            f"  P4: read_on_terms={dr.read_on_terms}, "
            f"drift_flagged_count={len(dr.drift_flagged)}: "
            f"{'PASS' if p4_pass else 'FAIL'}"
        )
        p5_pass = len(dr.relations_wanted) >= 1
        print(
            f"  P5 (exploratory): relations_wanted has "
            f"{len(dr.relations_wanted)} entrie(s): "
            f"{'PASS' if p5_pass else 'FAIL'}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
