"""
demo_aristotelian_reader_model_revengers.py — invoke the Aristotelian
reader-model probe on the Revenger's Tragedy Aristotelian encoding.

Session log:
- Session 1 (6693c6c): substrate skeleton (19 entities, 31 events,
  τ_s=-90..22).
- Session 2 (c4fe422): Aristotelian overlay — 1 mythos, 3 phases, 7
  ArCharacters (1 tragic hero: Vindice), 2 parallel relations, a 1-step
  anti-anagnorisis chain. Verifies clean (0 observations).
- Session 3 (1c038c2): substrate completion — 5 disclosures, 28 sjuzhet
  (Vindice focalizes 13; pathos-cluster 0+0+1), 9 descriptions.
- Session 4 (6561249): encoding tests (15 pins; test_aristotelian 222).
- Session 5 (this run): live probe — the research payoff.

**Primary forcing target: OQ-MALFI-3 (pathos-hero vs arc-hero split).**
The Malfi Session-6 re-probe surfaced it; this encoding presses it
HARDER and at a second site. The split is carried under semantic
stretch (the OQ-LEAR-4/A19 pattern before sketch-06):

  * Arc-hero / anagnorisis-bearer = Vindice (anagnorisis_character_ref_
    id="ar_vindice"; self-undoing recognition at τ_s=21).
  * Pathos-centre = Gloriana (ar_gloriana) — dead before the play,
    present only as a skull-prop, with NO dialect field to mark her.
    The claim lives in her annotation, the action_summary, and the
    AR_PATHOS_CLUSTER_PARALLEL relation (itself a stretch).
  * Three axes harder than Malfi: total split (Vindice unpitiable);
    non-agentive pathos-centre (a dead prop); distributed pathos
    (Gloriana + Antonio's wife + Castiza).

Two-way informativeness (per the Malfi/Lear precedent):
1. Probe surfaces the missing pathos field → OQ-MALFI-3 cross-encoding
   CONFIRMED; the sharp test is whether it proposes the SINGULAR
   (pathos_character_ref_id) or the TUPLE (pathos_character_ref_ids)
   shape given the distributed/dead-prop pathos-centre.
2. Probe reads through without surfacing → the stretch is invisible to
   the reader; OQ-MALFI-3 stays banked single-site (Malfi only).
3. Probe surfaces something new the encoding did not anticipate →
   richest outcome.

Predictions:

- **P1 (annotation-review baseline)**: ≥ 80 % approved across the prose
  surface, 0 rejected.
- **P3 (observation commentaries)**: EXPECTED EMPTY — the encoding
  verifies clean (0 observations), so there are no noted observations
  to comment on. (Contrast Malfi's 3 noteds.)
- **P4 (read-on-terms)**: read_on_terms ∈ {"yes", "partial"};
  drift_flagged empty or minor.
- **P5 (forcing — OQ-MALFI-3 pathos field).** EXPECTED: probe surfaces
  that the pathos-centre cannot be marked at the mythos level; proposes
  a pathos field. Sharp: singular vs tuple.
- **P6 (forcing — OQ-MALFI-3 non-agentive / distributed sub-questions).**
  EXPECTED: probe notes the pathos-centre is dead / a prop / absent,
  and/or distributed across the violated-women cluster.
- **P7 (forcing — S6P-OQ1 main-level anagnorisis_qualifier).** EXPECTED:
  probe surfaces that Vindice's MAIN recognition is anti/partial
  (belated, self-destroying) and that the qualifier lives only on chain
  steps; proposes a main-level qualifier.
- **P8 (closure-confirm — A20 anti generalization).** The Duke's dying
  recognition (anagnorisis_qualifier='anti') should read as load-
  bearing, NOT be re-proposed — confirming sketch-06 A20 generalizes.
- **P9 (closure-confirm — BINDING_ADJACENT).** The adjacent binding
  (distance 1) should read cleanly, not be flagged as a gap.
- **P10 (single-tragic-hero).** The single-tragic-hero shape should be
  accepted without demand for more (contrast Malfi's three).
- **P11 (retirement — fate-agent).** EXPECTED clean: the Revenger's
  Tragedy has no supernatural agents (the masque's blazing star is an
  omen, not an agent); sixth negative confirmation of OQ-AP5's
  retirement.

Substring matchers below are first-cut candidates; they can't
distinguish *citation of an authored record* from *demand for a new
record*. Verify against the JSON artifact.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_revengers

    # Dry run (no API call, prints the full prompt):
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_revengers \\
        --dry-run

    # Save the full structured result as JSON:
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_revengers \\
        --save-json reader_model_revengers_aristotelian_output.json
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
from story_engine.encodings.revengers_tragedy import FABULA
from story_engine.encodings.revengers_tragedy_aristotelian import (
    AR_REVENGERS_CHARACTER_ARC_RELATIONS, AR_REVENGERS_MYTHOS,
)


def _cli_args():
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n\n", 1)[0]
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the full prompt and exit without calling the API.",
    )
    parser.add_argument(
        "--effort", default="high",
        choices=["low", "medium", "high", "max"],
        help="output_config.effort (default: high).",
    )
    parser.add_argument(
        "--max-tokens", type=int, default=21_000,
        help=(
            "max_tokens for the probe response (default: 21000, the "
            "non-streaming ceiling for an unknown model: 600*128000/3600 "
            "≈ 21333). effort=high thinking can overrun the 16000 client "
            "default and truncate the JSON."
        ),
    )
    parser.add_argument(
        "--current-tau-a", type=int, default=50_000,
        help="τ_a stamped on produced records (default: 50000).",
    )
    parser.add_argument(
        "--anchor-tau-a", type=int, default=None,
        help="τ_a the encoding was last authored at (default: current).",
    )
    parser.add_argument(
        "--no-substrate-context", action="store_true",
        help="Omit the substrate-context section from the prompt.",
    )
    parser.add_argument(
        "--save-json", metavar="PATH",
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
    """Case-insensitive substring scan. First-cut candidate-surface
    matcher; 'candidate' results must be verified against the JSON
    artifact."""
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

    # The Revenger's Tragedy verifies CLEAN — zero observations (both
    # arc relations are canonical kind=parallel; the anti chain step is
    # non-precipitating). The probe sees an empty observation list and
    # reviews the prose surface + reads the dialect.
    observations = tuple(verify(
        AR_REVENGERS_MYTHOS, substrate_events=FABULA,
        mythoi=(AR_REVENGERS_MYTHOS,),
        character_arc_relations=AR_REVENGERS_CHARACTER_ARC_RELATIONS,
    ))

    tragic_heroes = [
        c for c in AR_REVENGERS_MYTHOS.characters if c.is_tragic_hero
    ]
    pathos_cluster = [
        c for c in AR_REVENGERS_MYTHOS.characters
        if c.id in ("ar_gloriana", "ar_antonio_wife", "ar_castiza")
    ]

    print("Aristotelian reader-model probe — The Revenger's Tragedy")
    print(f"  model: claude-opus-4-6")
    print(f"  effort: {args.effort}")
    print(f"  mythoi: 1 ({AR_REVENGERS_MYTHOS.id})")
    print(f"  phases: {len(AR_REVENGERS_MYTHOS.phases)}")
    print(
        f"  characters: {len(AR_REVENGERS_MYTHOS.characters)} "
        f"({len(tragic_heroes)} tragic hero: Vindice — corpus lean "
        f"case; {len(pathos_cluster)} pathos-cluster)"
    )
    print(
        f"  anagnorisis_character_ref_id: "
        f"{AR_REVENGERS_MYTHOS.anagnorisis_character_ref_id} "
        f"(Vindice — the arc-hero; pathos-centre is Gloriana, a "
        f"DIFFERENT character the dialect cannot mark — OQ-MALFI-3)"
    )
    print(
        f"  peripeteia → anagnorisis: "
        f"{AR_REVENGERS_MYTHOS.peripeteia_event_id} (τ_s=20) → "
        f"{AR_REVENGERS_MYTHOS.anagnorisis_event_id} (τ_s=21)"
    )
    print(
        f"  binding: "
        f"{AR_REVENGERS_MYTHOS.peripeteia_anagnorisis_binding} "
        f"(distance 1 — corpus-first ADJACENT cell)"
    )
    print(
        f"  anagnorisis_chain: "
        f"{len(AR_REVENGERS_MYTHOS.anagnorisis_chain)} step "
        f"(the Duke's dying recognition, anagnorisis_qualifier='anti' "
        f"— corpus 2nd anti, A20 generalization)"
    )
    print(
        f"  secondary_peripeteia_event_ids: "
        f"{len(AR_REVENGERS_MYTHOS.secondary_peripeteia_event_ids)} "
        f"(empty — single tragic arc; OQ-LEAR-4 not re-pressured)"
    )
    print(
        f"  character_arc_relations: "
        f"{len(AR_REVENGERS_CHARACTER_ARC_RELATIONS)} "
        f"(both kind='parallel': Vindice-Hippolito + the pathos-cluster "
        f"stretch)"
    )
    print(
        f"  observations: {len(observations)} "
        f"(expected 0 — corpus-cleanest; nothing to comment on)"
    )
    print(f"  substrate events (for grounding): {len(FABULA)}")
    print(f"  current_τ_a: {args.current_tau_a}")
    print(f"  anchor_τ_a: {args.anchor_tau_a or args.current_tau_a}")

    substrate_events = [] if args.no_substrate_context else list(FABULA)

    result = invoke_aristotelian_reader_model(
        mythoi=(AR_REVENGERS_MYTHOS,),
        observations=observations,
        substrate_events=substrate_events,
        character_arc_relations=AR_REVENGERS_CHARACTER_ARC_RELATIONS,
        current_τ_a=args.current_tau_a,
        anchor_τ_a=args.anchor_tau_a,
        effort=args.effort,
        max_tokens=args.max_tokens,
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
            "mythoi_ids": [AR_REVENGERS_MYTHOS.id],
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
        if r.comment:
            print(f"  comment:")
            for line in r.comment.splitlines() or [""]:
                print(f"    {line}")

    _print_section(
        f"OBSERVATION COMMENTARIES "
        f"({len(result.observation_commentaries)})"
    )
    if not result.observation_commentaries:
        print("  (none — encoding verifies clean, nothing to comment on)")
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
        print(f"       → {'PASS' if approval_pct >= 80 and rejected == 0 else 'FAIL'}")
    else:
        print("  P1: no annotation reviews emitted (unexpected)")
    print(
        f"  P3 (observation commentaries — expected empty, clean "
        f"encoding): {len(result.observation_commentaries)} commentaries"
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
            list(dr.scope_limits_observed) + list(dr.relations_wanted)
        )
        rationale = [dr.rationale]
        everything = all_surfaces + rationale

        print(
            "  [P5-P11 below use unconstrained substring matching; "
            "'candidate' results must be verified against the JSON "
            "artifact.]"
        )

        # P5 — OQ-MALFI-3 pathos-field forcing.
        p5_tokens = (
            "pathos_character", "pathos character", "pathos-character",
            "pathos centre", "pathos center", "pathos-centre",
            "pathos-center", "pathos bearer", "pathos-bearer",
            "pathos role", "pathos field", "site of pity",
            "principal site of pity", "pity-centre", "pity centre",
            "pity-bearer", "pathos_character_ref",
        )
        p5_scope = _token_hits(dr.scope_limits_observed, p5_tokens)
        p5_rel = _token_hits(dr.relations_wanted, p5_tokens)
        p5_hit = bool(p5_scope or p5_rel)
        print(
            f"  P5 (forcing — OQ-MALFI-3 pathos field): "
            f"{'candidate — verify in JSON' if p5_hit else 'no substring matches'}"
        )
        if p5_scope:
            print(f"       scope_limits hits: {p5_scope}")
        if p5_rel:
            print(f"       relations_wanted hits: {p5_rel}")

        # P6 — OQ-MALFI-3 non-agentive / distributed sub-questions.
        p6_tokens = (
            "skull", "dead before", "non-agentive", "not an agent",
            "no arc", "absent", "prop", "memento", "distributed",
            "cluster", "tuple", "multiple pathos", "several characters",
            "violated women", "more than one pathos", "plural",
        )
        p6_hits = _token_hits(everything, p6_tokens)
        print(
            f"  P6 (forcing — OQ-MALFI-3 non-agentive/distributed): "
            f"{'candidate — verify in JSON' if p6_hits else 'no substring matches'}"
        )
        if p6_hits:
            print(f"       hits: {p6_hits}")

        # P7 — S6P-OQ1 main-level anagnorisis_qualifier forcing.
        p7_tokens = (
            "main anagnorisis qualifier", "main-level qualifier",
            "main-level anagnorisis", "qualifier on the main",
            "qualifier on the mythos", "anagnorisis_qualifier on the",
            "main recognition", "self-undoing", "self undoing",
            "too late", "too-late", "belated recognition",
            "anti recognition for the main", "main anti",
        )
        p7_scope = _token_hits(dr.scope_limits_observed, p7_tokens)
        p7_rel = _token_hits(dr.relations_wanted, p7_tokens)
        p7_hit = bool(p7_scope or p7_rel)
        print(
            f"  P7 (forcing — S6P-OQ1 main-level qualifier): "
            f"{'candidate — verify in JSON' if p7_hit else 'no substring matches'}"
        )
        if p7_scope:
            print(f"       scope_limits hits: {p7_scope}")
        if p7_rel:
            print(f"       relations_wanted hits: {p7_rel}")

        # P8 — A20 anti generalization (should read load-bearing, not
        # be re-proposed as a missing field).
        p8_tokens = (
            "ArAntiAnagnorisis", "anti-anagnorisis field",
            "qualifier for anti", "anti qualifier needed",
            "no way to mark anti", "anti recognition record",
        )
        p8_hits = _token_hits(all_surfaces, p8_tokens)
        print(
            f"  P8 (closure-confirm — A20 anti generalization): "
            f"{'candidate RE-PROPOSAL — verify in JSON' if p8_hits else 'clean (anti reads load-bearing)'}"
        )
        if p8_hits:
            print(f"       hits: {p8_hits}")

        # P9 — BINDING_ADJACENT (should read cleanly, not flagged).
        p9_tokens = (
            "adjacent binding", "binding cell", "no adjacent",
            "binding too narrow", "distance field", "binding distance",
        )
        p9_hits = _token_hits(all_surfaces, p9_tokens)
        print(
            f"  P9 (closure-confirm — BINDING_ADJACENT): "
            f"{'candidate flag — verify in JSON' if p9_hits else 'clean (adjacent reads fine)'}"
        )
        if p9_hits:
            print(f"       hits: {p9_hits}")

        # P10 — single-tragic-hero (should be accepted).
        p10_tokens = (
            "more tragic heroes", "additional tragic hero",
            "second tragic hero", "only one tragic hero",
            "single tragic hero seems", "Hippolito should be a tragic",
        )
        p10_hits = _token_hits(everything, p10_tokens)
        print(
            f"  P10 (single-tragic-hero accepted): "
            f"{'candidate — verify in JSON' if p10_hits else 'clean (single hero accepted)'}"
        )
        if p10_hits:
            print(f"       hits: {p10_hits}")

        # P11 — fate-agent retirement (no supernatural agents).
        p11_tokens = (
            "ArFateAgent", "fate-agent", "fate agent", "prophecy",
            "supernatural", "blazing star", "comet", "omen", "divine",
        )
        p11_hits = _token_hits(everything, p11_tokens)
        print(
            f"  P11 (retirement — fate-agent): "
            f"{'candidate — verify in JSON' if p11_hits else 'clean (sixth negative confirmation)'}"
        )
        if p11_hits:
            print(f"       hits: {p11_hits}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
