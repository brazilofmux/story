"""
demo_aristotelian_reader_model_macbeth.py — invoke the Aristotelian
reader-model probe on the Macbeth Aristotelian encoding.

**Third Aristotelian probe, first of its kind under sketch-02.**
Macbeth is the encoding landed in commit 1988222 (state-of-play-11
commit body); it stresses the dialect at axes Oedipus + Rashomon
did not exercise:

- A12 BINDING_COINCIDENT is exercised for the first time. Peripeteia
  and anagnorisis both land at E_macduff_reveals_birth; Oedipus's
  BINDING_SEPARATED and Macbeth's BINDING_COINCIDENT cover two of
  the three canonical binding values (ADJACENT still uncovered).
- A11 carries a **non-precipitating** anagnorisis_chain step.
  AR_STEP_LADY_MACBETH_SLEEPWALKING has `precipitates_main=False`;
  Oedipus's AR_STEP_JOCASTA has `precipitates_main=True`. Both
  polarities now have corpus coverage.
- Macbeth's **scattered pathos** (E_macduff_family_killed τ_s=12;
  E_lady_macbeth_dies τ_s=14; E_macbeth_killed τ_s=17 — three
  events across two phases, three different victims) is the
  corpus's most stressful pathos case. If this forces the probe
  to want typed ArPathos, OQ-AP1 (banked in aristotelian-probe-
  sketch-02) gains a forcing function.

Predictions from aristotelian-probe-sketch-01 APS6 + -02 OQ-AP1..
OQ-AP4, specific to this invocation:

- P1: ≥ 80% of the 3 prose reviews (AR_MACBETH_MYTHOS.action_summary,
  AR_MACBETH.hamartia_text, AR_LADY_MACBETH.hamartia_text, plus
  phase annotations if present) earn `approved`, 0 `rejected`.
- P3: `observation_commentaries` is empty — Macbeth verifies with
  zero observations per test_macbeth_aristotelian_verifies_clean.
- P4: DialectReading.read_on_terms ∈ {"yes", "partial"};
  drift_flagged expected to be empty or near-empty — the
  encoding sits squarely within A1–A12 surface.
- P5 (exploratory — OQ-AP1 forcing check): if the probe surfaces
  pressure around Macbeth's scattered pathos (Macduff family
  killing + Lady Macbeth's death + Macbeth's death), expect
  `scope_limits_observed` or `relations_wanted` to name pathos-
  typing, catharsis-grounding, or ArPathos. Non-empty here
  converts OQ-AP1 from banked to forcing and opens an aristotelian-
  probe-sketch-03 candidate.
- P6 (exploratory — OQ-AP4 peripeteia-outside-middle): Macbeth's
  peripeteia is end-phase (τ_s=17 in the 5-event end phase). If
  the probe flags this as atypical, OQ-AP4 gains a forcing
  function; if it reads as natural, OQ-AP4 stays banked.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_macbeth

    # Dry run (no API call, prints the full prompt):
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_macbeth \\
        --dry-run

    # Save the full structured result as JSON:
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_macbeth \\
        --save-json reader_model_macbeth_aristotelian_output.json
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
from story_engine.encodings.macbeth import FABULA
from story_engine.encodings.macbeth_aristotelian import AR_MACBETH_MYTHOS


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

    # Verify the encoding first so the probe sees the real
    # observation list. Macbeth is expected to produce zero
    # observations per test_macbeth_aristotelian_verifies_clean.
    observations = tuple(verify(
        AR_MACBETH_MYTHOS, substrate_events=FABULA,
    ))

    print("Aristotelian reader-model probe — Macbeth")
    print(f"  model: claude-opus-4-6")
    print(f"  effort: {args.effort}")
    print(f"  mythoi: 1 ({AR_MACBETH_MYTHOS.id})")
    print(f"  phases: {len(AR_MACBETH_MYTHOS.phases)}")
    print(f"  characters: {len(AR_MACBETH_MYTHOS.characters)}")
    print(
        f"  binding: "
        f"{AR_MACBETH_MYTHOS.peripeteia_anagnorisis_binding} "
        f"(first BINDING_COINCIDENT corpus exercise)"
    )
    print(
        f"  anagnorisis_chain: "
        f"{len(AR_MACBETH_MYTHOS.anagnorisis_chain)} step "
        f"(non-precipitating — first in corpus)"
    )
    print(f"  observations: {len(observations)}")
    print(f"  substrate events (for grounding): {len(FABULA)}")
    print(f"  current_τ_a: {args.current_tau_a}")
    print(f"  anchor_τ_a: {args.anchor_tau_a or args.current_tau_a}")

    substrate_events = [] if args.no_substrate_context else list(FABULA)

    result = invoke_aristotelian_reader_model(
        mythoi=(AR_MACBETH_MYTHOS,),
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
            "mythoi_ids": [AR_MACBETH_MYTHOS.id],
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
    for r in result.annotation_reviews:
        print()
        print(f"  target: {r.target_kind}:{r.target_id}:{r.field}")
        print(f"  reviewer: {r.reviewer_id}")
        print(f"  verdict: {r.verdict}")
        print(f"  anchor_τ_a: {r.anchor_τ_a}")
        if r.comment:
            print(f"  comment:")
            for line in r.comment.splitlines() or [""]:
                print(f"    {line}")

    _print_section(
        f"OBSERVATION COMMENTARIES "
        f"({len(result.observation_commentaries)})"
    )
    if not result.observation_commentaries:
        print("  (none — as expected; Macbeth verifies clean)")
    for c in result.observation_commentaries:
        print()
        print(f"  target observation: "
              f"[{c.target_observation.severity}] "
              f"{c.target_observation.code}")
        print(f"  assessment: {c.assessment}")
        print(f"  commenter: {c.commenter_id}")
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
    approved = sum(
        1 for r in result.annotation_reviews if r.verdict == "approved"
    )
    rejected = sum(
        1 for r in result.annotation_reviews if r.verdict == "rejected"
    )
    if total:
        approval_pct = 100 * approved // total
        print(f"  P1: {approved}/{total} ({approval_pct}%) approved, "
              f"{rejected} rejected")
        p1_pass = approval_pct >= 80 and rejected == 0
        print(f"       → {'PASS' if p1_pass else 'FAIL'}")
    else:
        print("  P1: no annotation reviews emitted (unexpected)")
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
        # P5 exploratory — OQ-AP1 pathos-typing forcing check.
        # Look for pathos / catharsis / ArPathos in scope_limits
        # or relations_wanted.
        pathos_tokens = ("pathos", "catharsis", "ArPathos")
        scope_hits = [
            s for s in dr.scope_limits_observed
            if any(t.lower() in s.lower() for t in pathos_tokens)
        ]
        relations_hits = [
            r for r in dr.relations_wanted
            if any(t.lower() in r.lower() for t in pathos_tokens)
        ]
        p5_hit = bool(scope_hits or relations_hits)
        print(
            f"  P5 (exploratory — OQ-AP1): pathos-typing pressure "
            f"surfaced: {'YES — OQ-AP1 FORCES' if p5_hit else 'no'}"
        )
        if scope_hits:
            print(f"       scope_limits pathos hits: {scope_hits}")
        if relations_hits:
            print(f"       relations_wanted pathos hits: {relations_hits}")
        # P6 exploratory — OQ-AP4 peripeteia-in-beginning forcing
        # (not expected to fire; Macbeth's peripeteia is end-phase).
        peripeteia_tokens = ("peripeteia", "end-phase", "middle-phase")
        peripeteia_hits = [
            s for s in (
                list(dr.scope_limits_observed)
                + list(dr.relations_wanted)
                + list(dr.drift_flagged)
            )
            if any(t.lower() in s.lower() for t in peripeteia_tokens)
        ]
        print(
            f"  P6 (exploratory — OQ-AP4): peripeteia-placement "
            f"pressure surfaced: "
            f"{'YES — OQ-AP4 FORCES' if peripeteia_hits else 'no'}"
        )
        if peripeteia_hits:
            print(f"       hits: {peripeteia_hits}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
