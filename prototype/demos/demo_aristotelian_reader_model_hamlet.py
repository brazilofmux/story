"""
demo_aristotelian_reader_model_hamlet.py — invoke the Aristotelian
reader-model probe on the Hamlet Aristotelian encoding.

**Fourth Aristotelian probe.** Hamlet is the encoding landed across
Sessions 1–4 (edb25cb, 9423f59, b9aa560, ff77592). It stresses the
dialect at axes the earlier three probes did not exercise:

- **Three `is_tragic_hero=True` characters in one mythos** — first
  in corpus (Oedipus=2, Macbeth=2, Rashomon=0 at mythos scope). The
  dialect admits the multiplicity but has no structural hook for
  "these three stand in parallel WITHIN one mythos." OQ-AP6
  forcing case.

- **BINDING_SEPARATED at distance 9** — widest gap in corpus.
  Oedipus is BINDING_SEPARATED at distance 5; Macbeth is
  BINDING_COINCIDENT. The "separated" category covers 4..∞; Hamlet
  is the forcing case for whether distance typing (near vs distant,
  or a raw numerical field) is warranted. OQ-AP7 forcing case.

- **First encoding to author `complication_event_id` AND
  `denouement_event_id`.** Oedipus and Macbeth leave both None;
  Hamlet pins complication at `E_mousetrap_performance` (first
  middle event — Hamlet commits to the revenge path by verifying
  the Ghost's claim) and denouement at `E_duel_plotted` (last
  middle event — every element of the catastrophe set in motion).
  Whether the probe engages these fields or ignores them is a read
  on whether the dialect currently carries them as live surface.

- **Same-beat staggered recognition.** Laertes's deathbed
  recognition is substrate-compressed into `E_laertes_reveals_plot`
  (τ_s=17) — the same event as Hamlet's main anagnorisis. A11
  invariant 3 forbids a chain step at the main event, so Laertes
  is NOT authored as `AR_STEP_LAERTES_*`. OQ-AP8 forcing case:
  whether the dialect needs to admit same-event staggered
  recognition (distinguished by character-subject).

- **Ghost as fate-agent with commission posture (substrate-only).**
  The Ghost reveals the murder and commands revenge. OQ-AP5
  forcing case — whether the dialect wants `ArFateAgent /
  ArProphecyStructure`. Prediction: carried at substrate layer
  (apparition_of + ghost_claims_killed_by + ghost_demands_revenge),
  NOT visible at the Aristotelian dialect surface; the probe may
  therefore not surface OQ-AP5 pressure, which is itself the
  finding — the fate-agent lives below the dialect.

- **Clustered catharsis (four deaths at τ_s=17–18).** Gertrude,
  Laertes, Claudius, Hamlet — innocent, redeemed-antagonist,
  regicide-villain, tragic-hero. Four different moral weights in
  one beat. If the probe surfaces pressure around pathos-typing or
  catharsis-grounding (vocabulary like pathos / cluster / weight),
  OQ-AP1 (banked in aristotelian-probe-sketch-02) gains a third
  independent forcing signal on top of Macbeth's scattered pathos.

Predictions from aristotelian-probe-sketch-01 APS6 + -02/-03
banked forcing functions, specific to this invocation:

- P1: ≥ 80 % of prose reviews (7 fields: 1 action_summary + 3
  phase annotations + 3 hamartia_texts) earn `approved`, 0
  `rejected`.
- P3: `observation_commentaries` is empty — Hamlet verifies with
  zero observations per
  test_hamlet_aristotelian_verifies_clean.
- P4: `dialect_reading.read_on_terms` ∈ {"yes", "partial"};
  drift_flagged expected near-empty.
- P5 (forcing — OQ-AP6 parallel-heroes): the probe reaches for
  some structural way to type three heroes in one mythos
  (tokens: "parallel", "mirror", "foil", "intra-mythos",
  "ArParallelHeroes", "three", "tragic-hero"). Non-empty hits in
  `scope_limits_observed` or `relations_wanted` confirms OQ-AP6
  forces.
- P6 (forcing — OQ-AP7 range-of-separated): the probe notes that
  distance 9 reads differently from distance 4 (tokens: "distance",
  "near", "distant", "far", "separated", "numerical"). Non-empty
  confirms OQ-AP7 forces.
- P7 (forcing — OQ-AP8 same-beat staggered recognition): the
  probe wants to type Laertes's deathbed self-recognition at the
  main anagnorisis event (tokens: "Laertes", "same event",
  "staggered", "character-subject", "chain step at main"). Any
  non-empty hit confirms OQ-AP8 forces.
- P8 (exploratory — OQ-AP5 fate-agent): the probe surfaces
  pressure wanting to type the Ghost's role (tokens:
  "ArFateAgent", "prophecy", "commission", "Ghost", "revelation").
  Prediction: NO — the Ghost is substrate-only and stays invisible
  at the dialect surface; a NO here is a negative finding
  supporting the OQ_AP5_FINDING claim (fate-agent lives below the
  dialect).
- P9 (exploratory — OQ-AP1 pathos-typing): the probe surfaces
  pressure around the four-death cluster (tokens: "pathos",
  "catharsis", "cluster", "pity", "fear", "weight"). If hit,
  OQ-AP1 gains a third independent forcing signal.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_hamlet

    # Dry run (no API call, prints the full prompt):
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_hamlet \\
        --dry-run

    # Save the full structured result as JSON:
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_hamlet \\
        --save-json reader_model_hamlet_aristotelian_output.json
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
from story_engine.encodings.hamlet import FABULA
from story_engine.encodings.hamlet_aristotelian import AR_HAMLET_MYTHOS


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


def _token_hits(hay_list, tokens):
    """Return the subset of `hay_list` strings that contain any
    token in `tokens` (case-insensitive substring match).

    This is a first-cut scan, not a definitive forcing-function
    classifier. Substrings are loose — e.g., "Laertes" or "Ghost"
    match any scope_limit or relation_wanted that mentions the
    character for unrelated reasons. Commit 6e5e41c documented
    three false positives from this matcher on Session 5 (P6/P7/P8).
    Treat hits as candidates for manual review against the JSON
    artifact, not as confirmed forcing signals.
    """
    return [
        s for s in hay_list
        if any(t.lower() in s.lower() for t in tokens)
    ]


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
    # observation list. Hamlet is expected to produce zero
    # observations per test_hamlet_aristotelian_verifies_clean.
    observations = tuple(verify(
        AR_HAMLET_MYTHOS, substrate_events=FABULA,
    ))

    tragic_heroes = [
        c for c in AR_HAMLET_MYTHOS.characters if c.is_tragic_hero
    ]

    print("Aristotelian reader-model probe — Hamlet")
    print(f"  model: claude-opus-4-6")
    print(f"  effort: {args.effort}")
    print(f"  mythoi: 1 ({AR_HAMLET_MYTHOS.id})")
    print(f"  phases: {len(AR_HAMLET_MYTHOS.phases)}")
    print(
        f"  characters: {len(AR_HAMLET_MYTHOS.characters)} "
        f"({len(tragic_heroes)} tragic-hero — first ≥3 in corpus)"
    )
    print(
        f"  binding: "
        f"{AR_HAMLET_MYTHOS.peripeteia_anagnorisis_binding} "
        f"(widest separation in corpus — distance 9)"
    )
    print(
        f"  anagnorisis_chain: "
        f"{len(AR_HAMLET_MYTHOS.anagnorisis_chain)} step "
        f"(non-precipitating, antagonist-occupant)"
    )
    print(
        f"  complication_event_id: "
        f"{AR_HAMLET_MYTHOS.complication_event_id} "
        f"(first corpus authoring)"
    )
    print(
        f"  denouement_event_id: "
        f"{AR_HAMLET_MYTHOS.denouement_event_id} "
        f"(first corpus authoring)"
    )
    print(f"  observations: {len(observations)}")
    print(f"  substrate events (for grounding): {len(FABULA)}")
    print(f"  current_τ_a: {args.current_tau_a}")
    print(f"  anchor_τ_a: {args.anchor_tau_a or args.current_tau_a}")

    substrate_events = [] if args.no_substrate_context else list(FABULA)

    result = invoke_aristotelian_reader_model(
        mythoi=(AR_HAMLET_MYTHOS,),
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
            "mythoi_ids": [AR_HAMLET_MYTHOS.id],
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
        print("  (none — as expected; Hamlet verifies clean)")
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

        all_surfaces = (
            list(dr.scope_limits_observed)
            + list(dr.relations_wanted)
        )

        print(
            "  [P5-P9 below use unconstrained substring matching; "
            "'candidate' results must be verified against the JSON "
            "artifact. See commit 6e5e41c for false-positive "
            "examples.]"
        )

        # P5 — OQ-AP6 parallel-heroes forcing check.
        p5_tokens = (
            "parallel", "mirror", "foil", "intra-mythos",
            "ArParallelHeroes", "three hero", "tragic hero",
            "multiple tragic",
        )
        p5_scope = _token_hits(dr.scope_limits_observed, p5_tokens)
        p5_rel = _token_hits(dr.relations_wanted, p5_tokens)
        p5_hit = bool(p5_scope or p5_rel)
        print(
            f"  P5 (forcing — OQ-AP6 parallel-heroes): "
            f"{'candidate — verify in JSON' if p5_hit else 'no substring matches'}"
        )
        if p5_scope:
            print(f"       scope_limits hits: {p5_scope}")
        if p5_rel:
            print(f"       relations_wanted hits: {p5_rel}")

        # P6 — OQ-AP7 range-of-separated forcing check.
        p6_tokens = (
            "distance", "near", "distant", "far apart",
            "numerical", "range", "gap",
        )
        p6_scope = _token_hits(dr.scope_limits_observed, p6_tokens)
        p6_rel = _token_hits(dr.relations_wanted, p6_tokens)
        p6_hit = bool(p6_scope or p6_rel)
        print(
            f"  P6 (forcing — OQ-AP7 range-of-separated): "
            f"{'candidate — verify in JSON' if p6_hit else 'no substring matches'}"
        )
        if p6_scope:
            print(f"       scope_limits hits: {p6_scope}")
        if p6_rel:
            print(f"       relations_wanted hits: {p6_rel}")

        # P7 — OQ-AP8 same-beat staggered recognition forcing
        # check.
        p7_tokens = (
            "same event", "same-event", "same beat", "same-beat",
            "Laertes", "staggered", "character-subject",
            "chain step at main", "shared event",
        )
        p7_hits = _token_hits(all_surfaces, p7_tokens)
        p7_hit = bool(p7_hits)
        print(
            f"  P7 (forcing — OQ-AP8 same-beat staggered): "
            f"{'candidate — verify in JSON' if p7_hit else 'no substring matches'}"
        )
        if p7_hits:
            print(f"       hits: {p7_hits}")

        # P8 — OQ-AP5 fate-agent exploratory. Prediction NO
        # because the Ghost is substrate-only. NO confirms the
        # OQ_AP5_FINDING negative claim.
        p8_tokens = (
            "ArFateAgent", "fate-agent", "fate agent",
            "prophecy", "commission", "Ghost", "revelation",
            "divine", "oracle",
        )
        p8_hits = _token_hits(all_surfaces, p8_tokens)
        p8_hit = bool(p8_hits)
        print(
            f"  P8 (exploratory — OQ-AP5 fate-agent): "
            f"{'candidate — verify in JSON' if p8_hit else 'no substring matches (consistent with OQ_AP5_FINDING negative)'}"
        )
        if p8_hits:
            print(f"       hits: {p8_hits}")

        # P9 — OQ-AP1 pathos-typing / catharsis exploratory.
        # Clustered catharsis (four deaths τ_s=17–18) is the
        # corpus's most stressful cluster case.
        p9_tokens = (
            "pathos", "catharsis", "cluster", "pity", "fear",
            "weight", "ArPathos",
        )
        p9_hits = _token_hits(all_surfaces, p9_tokens)
        p9_hit = bool(p9_hits)
        print(
            f"  P9 (exploratory — OQ-AP1 pathos-typing): "
            f"{'candidate — verify in JSON' if p9_hit else 'no substring matches'}"
        )
        if p9_hits:
            print(f"       hits: {p9_hits}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
