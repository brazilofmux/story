"""
demo_aristotelian_reader_model_lear.py — invoke the Aristotelian
reader-model probe on the Lear Aristotelian encoding.

Session log:
- Sessions 1-4 (bfecd73, b75fa11, bc89a77, 95e18f9): substrate +
  overlay + substrate completion + encoding-specific tests.
- Session 5 (this run): first probe run. Pressures five banked
  forcing functions:
    * OQ-AP14 (instrumental-kind A13, second-site after Hamlet's
      single-candidate surface — Lear offers two instrumental
      relations sharing Gloucester as target with opposite moral
      polarity)
    * OQ-AP15 (absent-character catharsis — four offstage deaths
      in the end phase; Cordelia's hanging with ZERO observer
      projections at the defining event)
    * OQ-AP7 re-surface (second independent encoding, distance 14
      — corpus widest)
    * OQ-LEAR-1 (emotional-vs-epistemic staging — Lear's chain
      has zero staging despite being same-character main)
    * OQ-LEAR-2 (double-plot unity — first corpus encoding with
      asserts_unity_of_action=False)
  Plus closure-verification:
    * OQ-AP6 (intra-mythos parallel tragic heroes — sketch-03
      closure verified on Hamlet Session 6; Lear should absorb
      without re-surfacing)

**Session 5 framing — two-way informativeness.**
1. Probe surfaces OQ-AP14 / OQ-AP15 / OQ-LEAR-1 / OQ-LEAR-2 → forcing
   confirmed; sketch-05+ closure candidate.
2. Probe reads them through without surfacing → encoding reads on
   sketch-03/sketch-04 terms; banked forcing functions stay
   banked pending cross-encoding re-surface.
3. Probe surfaces NEW forcing functions the encoding didn't
   anticipate → richest outcome, same as Hamlet Session 5.

Reviewable prose under sketch-04 APA4-3: ~15 fields on Lear
(1 action_summary + 3 phase annotations + 5 hamartia_texts + 2
chain-step annotations + 4 arc-relation annotations) vs Hamlet's
12.

Predictions (sketch-04-style prediction stack):

- P1: ≥ 80 % approved across ~15 prose reviews, 0 rejected.
- P3: `observation_commentaries` empty OR contains commentary on
  the TWO noted-severity instrumental-kind observations (both are
  expected per sketch-03 canonical-plus-open discipline; probe
  may or may not comment).
- P4: `dialect_reading.read_on_terms` ∈ {"yes", "partial"};
  drift_flagged empty or minor.
- **P5 (forcing — OQ-AP14 instrumental-kind).** Expected: probe
  surfaces the instrumental relation as structurally distinct
  from parallel/mirror/foil; proposes canonical extension (fourth
  canonical kind; or polarity sub-axis; or new record type).
  Sharp prediction: the probe reads the two instrumental relations
  AS structural (not as tagged but substrate-equivalent to A13).
- **P6 (forcing — OQ-AP15 absent catharsis).** Expected: probe
  surfaces the catharsis-displacement pattern on Cordelia's
  offstage hanging. Sharp prediction: the probe reads the
  empty-observer defining-event as load-bearing for the catharsis
  (not as an oversight).
- P7 (forcing — OQ-AP7 range-of-separated, second site).
  Expected: probe cites distance 14 as analytically distinct
  from Hamlet's 9 and Oedipus's 5; may propose numerical distance
  field or near/distant distinction.
- **P8 (forcing — OQ-LEAR-1 emotional staging).** Expected: probe
  surfaces that Lear's chain lacks staging despite the main-
  character being Lear himself. Sharp prediction: probe reads the
  reconciliation as emotional rather than epistemic; notes the
  dialect's staging vocabulary's epistemic-only premise.
- **P9 (forcing — OQ-LEAR-2 double-plot unity).** Expected: probe
  surfaces the asserts_unity_of_action=False as substantive (not
  as incomplete authorship). Sharp prediction: probe reads the
  Lear-Gloucester parallel as thematic unity coexisting with
  causal non-unity.
- P10 (closure-check — OQ-AP6 parallel-heroes). Expected NO
  re-surfacing; probe should cite the A13 parallel relation as
  the structural hook.
- P11 (retirement-check — OQ-AP5 fate-agent). Expected NO signal
  (Lear has no supernatural agents; fourth-negative confirmation
  after Macbeth Witches + Hamlet Ghost + Lear).

Substring matchers below are first-cut candidates; they can't
distinguish *citation of an authored record* from *demand for a
new record*. Commit message for this session cites JSON artifact
directly, not summary.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_lear

    # Dry run (no API call, prints the full prompt):
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_lear \\
        --dry-run

    # Save the full structured result as JSON:
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_lear \\
        --save-json reader_model_lear_aristotelian_output.json
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
from story_engine.encodings.lear import FABULA
from story_engine.encodings.lear_aristotelian import (
    AR_LEAR_CHARACTER_ARC_RELATIONS, AR_LEAR_MYTHOS,
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

    # Verify the encoding first so the probe sees the real
    # observation list. Lear is expected to produce exactly TWO
    # observations, both severity=noted and both flagging the
    # non-canonical kind="instrumental" under sketch-03's canonical-
    # plus-open discipline (per test_lear_aristotelian_verifies_
    # clean_up_to_instrumental_noted).
    observations = tuple(verify(
        AR_LEAR_MYTHOS, substrate_events=FABULA,
        mythoi=(AR_LEAR_MYTHOS,),
        character_arc_relations=AR_LEAR_CHARACTER_ARC_RELATIONS,
    ))

    tragic_heroes = [
        c for c in AR_LEAR_MYTHOS.characters if c.is_tragic_hero
    ]
    non_tragic = [
        c for c in AR_LEAR_MYTHOS.characters if not c.is_tragic_hero
    ]
    instrumental_relations = [
        r for r in AR_LEAR_CHARACTER_ARC_RELATIONS
        if r.kind == "instrumental"
    ]

    print("Aristotelian reader-model probe — Lear")
    print(f"  model: claude-opus-4-6")
    print(f"  effort: {args.effort}")
    print(f"  mythoi: 1 ({AR_LEAR_MYTHOS.id})")
    print(f"  phases: {len(AR_LEAR_MYTHOS.phases)}")
    print(
        f"  characters: {len(AR_LEAR_MYTHOS.characters)} "
        f"({len(tragic_heroes)} tragic-hero + "
        f"{len(non_tragic)} non-tragic serving A13 relations)"
    )
    print(
        f"  asserts_unity_of_action: "
        f"{AR_LEAR_MYTHOS.asserts_unity_of_action} "
        f"(corpus first; OQ_LEAR_2)"
    )
    print(
        f"  binding: "
        f"{AR_LEAR_MYTHOS.peripeteia_anagnorisis_binding} "
        f"(widest separation in corpus — distance 14; OQ-AP7 "
        f"second site)"
    )
    print(
        f"  anagnorisis_chain: "
        f"{len(AR_LEAR_MYTHOS.anagnorisis_chain)} steps "
        f"(both step_kind=parallel; ZERO staging despite "
        f"same-character main — OQ_LEAR_1)"
    )
    print(
        f"  character_arc_relations: "
        f"{len(AR_LEAR_CHARACTER_ARC_RELATIONS)} "
        f"({len(instrumental_relations)} non-canonical "
        f"kind='instrumental'; OQ-AP14 pressure)"
    )
    print(
        f"  complication_event_id: "
        f"{AR_LEAR_MYTHOS.complication_event_id}"
    )
    print(
        f"  denouement_event_id: "
        f"{AR_LEAR_MYTHOS.denouement_event_id}"
    )
    print(
        f"  observations: {len(observations)} "
        f"(expected 2 noted — instrumental-kind canonical-plus-open)"
    )
    print(f"  substrate events (for grounding): {len(FABULA)}")
    print(f"  current_τ_a: {args.current_tau_a}")
    print(f"  anchor_τ_a: {args.anchor_tau_a or args.current_tau_a}")

    substrate_events = [] if args.no_substrate_context else list(FABULA)

    result = invoke_aristotelian_reader_model(
        mythoi=(AR_LEAR_MYTHOS,),
        observations=observations,
        substrate_events=substrate_events,
        character_arc_relations=AR_LEAR_CHARACTER_ARC_RELATIONS,
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
            "mythoi_ids": [AR_LEAR_MYTHOS.id],
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
        print("  (none — probe did not comment on noted observations)")
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
    p3_note = (
        "P3: observation_commentaries present (optional — the 2 "
        "noted-severity instrumental-kind observations are "
        "expected per sketch-03 canonical-plus-open)"
    )
    print(
        f"  {p3_note}: "
        f"{len(result.observation_commentaries)} commentaries"
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
            "  [P5-P11 below use unconstrained substring matching; "
            "'candidate' results must be verified against the JSON "
            "artifact.]"
        )

        # P5 — OQ-AP14 instrumental-kind forcing check.
        p5_tokens = (
            "instrumental", "wielder", "target",
            "instrument-mediated", "polarity", "directional",
            "malicious", "therapeutic",
        )
        p5_scope = _token_hits(dr.scope_limits_observed, p5_tokens)
        p5_rel = _token_hits(dr.relations_wanted, p5_tokens)
        p5_hit = bool(p5_scope or p5_rel)
        print(
            f"  P5 (forcing — OQ-AP14 instrumental-kind): "
            f"{'candidate — verify in JSON' if p5_hit else 'no substring matches'}"
        )
        if p5_scope:
            print(f"       scope_limits hits: {p5_scope}")
        if p5_rel:
            print(f"       relations_wanted hits: {p5_rel}")

        # P6 — OQ-AP15 absent catharsis forcing check.
        p6_tokens = (
            "offstage", "off-stage", "absent", "displaced",
            "catharsis", "reported", "empty observer",
            "hanging", "unobserved",
        )
        p6_scope = _token_hits(dr.scope_limits_observed, p6_tokens)
        p6_rel = _token_hits(dr.relations_wanted, p6_tokens)
        p6_hit = bool(p6_scope or p6_rel)
        print(
            f"  P6 (forcing — OQ-AP15 absent catharsis): "
            f"{'candidate — verify in JSON' if p6_hit else 'no substring matches'}"
        )
        if p6_scope:
            print(f"       scope_limits hits: {p6_scope}")
        if p6_rel:
            print(f"       relations_wanted hits: {p6_rel}")

        # P7 — OQ-AP7 range-of-separated forcing check (second site).
        p7_tokens = (
            "distance", "near", "distant", "far apart",
            "numerical", "range", "gap", "fourteen",
        )
        p7_hits = _token_hits(all_surfaces, p7_tokens)
        p7_hit = bool(p7_hits)
        print(
            f"  P7 (forcing — OQ-AP7 range-of-separated, 2nd site): "
            f"{'candidate — verify in JSON' if p7_hit else 'no substring matches'}"
        )
        if p7_hits:
            print(f"       hits: {p7_hits}")

        # P8 — OQ-LEAR-1 emotional-vs-epistemic staging forcing
        # check.
        p8_tokens = (
            "staging", "emotional", "affective", "epistemic",
            "remove_held", "same-character", "waypoint",
            "reconciliation",
        )
        p8_hits = _token_hits(all_surfaces, p8_tokens)
        p8_hit = bool(p8_hits)
        print(
            f"  P8 (forcing — OQ-LEAR-1 emotional staging): "
            f"{'candidate — verify in JSON' if p8_hit else 'no substring matches'}"
        )
        if p8_hits:
            print(f"       hits: {p8_hits}")

        # P9 — OQ-LEAR-2 double-plot unity forcing check.
        p9_tokens = (
            "double plot", "double-plot", "double-arc",
            "double arc", "two plot", "subplot",
            "unity of action", "unity_of_action",
            "parallel plot", "subordinat",
        )
        p9_hits = _token_hits(all_surfaces, p9_tokens)
        p9_hit = bool(p9_hits)
        print(
            f"  P9 (forcing — OQ-LEAR-2 double-plot unity): "
            f"{'candidate — verify in JSON' if p9_hit else 'no substring matches'}"
        )
        if p9_hits:
            print(f"       hits: {p9_hits}")

        # P10 — OQ-AP6 closure-verification (should NOT re-surface).
        p10_tokens = (
            "three tragic", "multiple tragic", "three-hero",
            "intra-mythos parallel", "ArParallelHeroes",
        )
        p10_hits = _token_hits(all_surfaces, p10_tokens)
        p10_hit = bool(p10_hits)
        print(
            f"  P10 (closure-check — OQ-AP6 parallel-heroes): "
            f"{'candidate re-surface — verify in JSON' if p10_hit else 'clean (closure holds on second encoding)'}"
        )
        if p10_hits:
            print(f"       hits: {p10_hits}")

        # P11 — OQ-AP5 retirement-confirmation (should NOT surface
        # — Lear has no supernatural agents).
        p11_tokens = (
            "ArFateAgent", "fate-agent", "fate agent",
            "prophecy", "supernatural", "oracle", "divine",
        )
        p11_hits = _token_hits(all_surfaces, p11_tokens)
        p11_hit = bool(p11_hits)
        print(
            f"  P11 (retirement — OQ-AP5 fate-agent): "
            f"{'candidate — verify in JSON' if p11_hit else 'clean (fourth negative confirmation)'}"
        )
        if p11_hits:
            print(f"       hits: {p11_hits}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
