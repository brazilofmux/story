"""
demo_aristotelian_reader_model_malfi.py — invoke the Aristotelian
reader-model probe on the Malfi Aristotelian encoding.

Session log:
- Session 1 (0b5e0e3): substrate skeleton (1616 lines: 16 entities,
  10 agents, 34 events spanning τ_s=-30..33).
- Session 2 (32acd45): Aristotelian overlay (1405 lines:
  AR_MALFI_MYTHOS, 5 ArCharacters, 4 ArCharacterArcRelations
  including 2 non-canonical kind="instrumental", 2-step
  post-main parallel anagnorisis chain).
- Session 3 (d9b2fb0): substrate completion (PREPLAY_DISCLOSURES
  6 facts, SJUZHET 30 entries with focalization, DESCRIPTIONS
  12 records).
- Session 4 (a9f8c89): encoding-specific tests (15 tests pinning
  Session 2+3 commitments).
- Session 5 (this run): live probe — the research payoff.

Banked forcing functions this encoding presses on:

* **OQ-LEAR-4 (cross-encoding pressure for sketch-06 closure)**.
  Malfi authors FOUR structurally-distinct character-arc
  peripeteia events within a single mythos: Duchess at capture
  (τ_s=17), Ferdinand at corpse-view (τ_s=23), Bosola at
  corpse-view (τ_s=24), Antonio in the dark (τ_s=30). The
  dialect's single peripeteia_event_id slot cannot carry them
  all; the encoding distributes the structural information
  across mythos field + anagnorisis chain steps + prose. Lear
  surfaced the question with one encoding; Malfi is the
  cross-encoding pressure that sketch-06 should now close.
  Recommended option (per OQ_LEAR_4_FINDING):
  `ArMythos.secondary_peripeteia_event_ids: Tuple[str, ...]`.

* **OQ-AP7 third-encoding re-surface (distance 6 — corpus
  narrowest)**. Malfi's peripeteia-anagnorisis distance is 6
  (capture τ_s=17 → Ferdinand-views-corpse τ_s=23). Three
  encodings under one BINDING_SEPARATED category now exhibit
  three analytical shapes: INTENSE (Malfi 6), DELAYED (Hamlet
  9), ACCUMULATING (Lear 14). Pressure on near-vs-distant
  refinement, or a numerical distance field, or named
  analytical-shape enum.

* **OQ-MALFI-1 (NEW forcing function)**. Two `kind="instrumental"`
  A13 relations sharing target (Bosola) AND polarity (malicious),
  distinguished by wielder + temporal phase (Cardinal: pre-play
  galley + Act V re-employment; Ferdinand: play's primary
  commission). Distinct from Lear's polarity-CONTRAST shape; the
  paired-non-canonical-polarity-CONCORDANCE shape is single-
  encoding for now. Three candidate canonical extensions named
  in OQ_MALFI_1_FINDING (new A7.15 check 6, temporal_phase
  field, or new kind="instrument-transferred").

Plus closure-verification on:

* **OQ-AP6 (intra-mythos parallel tragic heroes)** — sketch-03
  closure verified on Hamlet (Session 6) + Lear (Session 5).
  Malfi has three tragic heroes (Duchess + Bosola + Ferdinand).
  Probe should absorb without re-surfacing.

* **OQ-AP14 closure-confirmation** — sketch-05 (A17) closed the
  instrumental-kind question with directionality + polarity
  fields. Malfi exercises both fields on its two instrumental
  relations. Probe should read them as structurally typed, not
  as residual canonical-vocabulary pressure.

* **OQ-LEAR-2** — Lear authored asserts_unity_of_action=False
  (corpus first); Session 2 surfaced the question whether the
  True/False binary needed positively-named shape labels. Malfi
  authors asserts_unity_of_action=True despite four
  character-arc peripeteia, confirming the distinction is
  classical-unity vs parallel-actions, not lexical. Probe
  should read Malfi's True as adequate without demanding shape
  labels.

**Session 5 framing — two-way informativeness (per the Lear-Hamlet
precedent).**
1. Probe surfaces OQ-LEAR-4 / OQ-AP7 / OQ-MALFI-1 → forcing
   confirmed; sketch-06 closure candidate.
2. Probe reads them through without surfacing → encoding reads on
   sketch-03+04+05 terms; banked forcing functions stay banked
   pending further cross-encoding pressure.
3. Probe surfaces NEW forcing functions the encoding didn't
   anticipate → richest outcome.

Reviewable prose (under sketch-04 APA4-3): ~14 fields on Malfi
(1 action_summary + 3 phase annotations + 5 hamartia_texts + 2
chain-step annotations + 4 arc-relation annotations) — comparable
to Lear's ~15 and Hamlet's 12.

Predictions (sketch-04-style prediction stack):

- **P1 (prose review baseline)**: ≥ 80 % approved across ~14
  prose reviews, 0 rejected.
- **P3 (instrumental-noted commentary)**: `observation_
  commentaries` empty OR contains commentary on the TWO
  noted-severity instrumental-kind observations (both are
  expected per sketch-03 canonical-plus-open discipline; probe
  may or may not comment now that A17 polarity+directionality
  carry the structural content).
- **P4 (read-on-terms)**: `dialect_reading.read_on_terms` ∈
  {"yes", "partial"}; drift_flagged empty or minor.
- **P5 (forcing — OQ-LEAR-4 cross-encoding pressure).**
  EXPECTED: probe surfaces the four-arc-peripeteia distribution
  as structurally distinct from the single peripeteia_event_id
  shape; proposes the secondary_peripeteia_event_ids field (or
  equivalent). Sharp prediction: the probe reads Bosola's
  resolve (τ_s=24) and/or Antonio's anti-recognition (τ_s=30)
  as carrying arc-peripeteia content the chain-step apparatus
  cannot fully carry.
- **P6 (forcing — OQ-AP7 third-encoding distance-6).** EXPECTED:
  probe distinguishes Malfi's INTENSE distance-6 from Hamlet's
  DELAYED-9 and Lear's ACCUMULATING-14; proposes refinement
  (near/distant; or numerical field; or named analytical-shape
  enum). Sharp prediction: probe cites the dense Act-IV
  compression (capture → 3 tortures → strangling → recognition)
  as the analytical character of distance-6.
- **P7 (forcing — OQ-MALFI-1 sequentially-wielded-instrument).**
  EXPECTED: probe surfaces the two-wielders / one-target /
  same-polarity pattern as distinct from Lear's polarity-
  contrast. Sharp prediction: probe proposes either a check
  (A7.15 check 6 polarity-concordance) or a temporal-phase
  field, or reads the shape as one-relation-spanning-two-
  employers.
- **P8 (forcing-related — Bosola-as-co-protagonist)**. EXPECTED:
  probe surfaces the Duchess+Bosola dual-focalization (10+7
  SJUZHET entries) and reads Bosola as structurally
  co-protagonist with the Duchess. Sharp prediction: probe
  cites Bosola's arc-peripeteia at τ_s=24 as the play's
  central reversal.
- **P9 (closure-check — OQ-AP6 parallel-heroes)**. EXPECTED NO
  re-surfacing; probe should cite the three tragic heroes
  through the A13 apparatus (foil + parallel + instrumental
  relations) and the multi-character anagnorisis chain.
- **P10 (closure-check — OQ-AP14 sketch-05 closure)**. EXPECTED
  NO re-surfacing of the instrumental-kind question as
  vocabulary pressure; probe should accept directionality +
  polarity fields as structurally adequate.
- **P11 (closure-check — OQ-LEAR-2 unity binary)**. EXPECTED
  NO demand for positively-named shape labels on
  asserts_unity_of_action; probe should read Malfi's True as
  adequate.
- **P12 (retirement-check — OQ-AP5 fate-agent)**. EXPECTED NO
  signal (Malfi has no supernatural agents; fifth-negative
  confirmation after Macbeth Witches + Hamlet Ghost + Lear +
  Oedipus's oracle which IS supernatural-adjacent).

Substring matchers below are first-cut candidates; they can't
distinguish *citation of an authored record* from *demand for a
new record*. Commit message for this session cites JSON artifact
directly, not summary.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_malfi

    # Dry run (no API call, prints the full prompt):
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_malfi \\
        --dry-run

    # Save the full structured result as JSON:
    .venv/bin/python3 -m demos.demo_aristotelian_reader_model_malfi \\
        --save-json reader_model_malfi_aristotelian_output.json
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
from story_engine.encodings.malfi import FABULA
from story_engine.encodings.malfi_aristotelian import (
    AR_MALFI_CHARACTER_ARC_RELATIONS, AR_MALFI_MYTHOS,
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
    # observation list. Malfi is expected to produce exactly TWO
    # observations, both severity=noted and both flagging the
    # non-canonical kind="instrumental" under sketch-03's canonical-
    # plus-open discipline. Unlike Lear (whose two instrumentals
    # have opposite polarities → A7.15 check 5 fires a third
    # noted), Malfi's two instrumentals are polarity-concordant
    # (both malicious) so check 5 does NOT fire — OQ-MALFI-1.
    observations = tuple(verify(
        AR_MALFI_MYTHOS, substrate_events=FABULA,
        mythoi=(AR_MALFI_MYTHOS,),
        character_arc_relations=AR_MALFI_CHARACTER_ARC_RELATIONS,
    ))

    tragic_heroes = [
        c for c in AR_MALFI_MYTHOS.characters if c.is_tragic_hero
    ]
    non_tragic = [
        c for c in AR_MALFI_MYTHOS.characters if not c.is_tragic_hero
    ]
    instrumental_relations = [
        r for r in AR_MALFI_CHARACTER_ARC_RELATIONS
        if r.kind == "instrumental"
    ]
    anagnorisis_absent_chars = [
        c for c in AR_MALFI_MYTHOS.characters if c.anagnorisis_absent
    ]

    print("Aristotelian reader-model probe — Malfi")
    print(f"  model: claude-opus-4-6")
    print(f"  effort: {args.effort}")
    print(f"  mythoi: 1 ({AR_MALFI_MYTHOS.id})")
    print(f"  phases: {len(AR_MALFI_MYTHOS.phases)}")
    print(
        f"  characters: {len(AR_MALFI_MYTHOS.characters)} "
        f"({len(tragic_heroes)} tragic-hero + "
        f"{len(non_tragic)} non-tragic serving A13 relations)"
    )
    print(
        f"  anagnorisis_absent: {len(anagnorisis_absent_chars)} "
        f"(Duchess — corpus second after Cordelia)"
    )
    print(
        f"  asserts_unity_of_action: "
        f"{AR_MALFI_MYTHOS.asserts_unity_of_action} "
        f"(contrast Lear's False — confirms OQ-LEAR-2 binary)"
    )
    print(
        f"  binding: "
        f"{AR_MALFI_MYTHOS.peripeteia_anagnorisis_binding} "
        f"(narrowest separation in corpus — distance 6; OQ-AP7 "
        f"third-encoding re-surface)"
    )
    print(
        f"  anagnorisis_chain: "
        f"{len(AR_MALFI_MYTHOS.anagnorisis_chain)} steps "
        f"(both step_kind=parallel; both POST-MAIN; corpus first "
        f"multi-post-main chain — OQ-LEAR-4 forcing)"
    )
    print(
        f"  anagnorisis_character_ref_id: "
        f"{AR_MALFI_MYTHOS.anagnorisis_character_ref_id} "
        f"(Ferdinand — corpus first orchestrator-also-recognizer)"
    )
    print(
        f"  character_arc_relations: "
        f"{len(AR_MALFI_CHARACTER_ARC_RELATIONS)} "
        f"({len(instrumental_relations)} non-canonical "
        f"kind='instrumental'; OQ-MALFI-1 — polarity-CONCORDANT, "
        f"distinct from Lear's polarity-contrast)"
    )
    print(
        f"  complication_event_id: "
        f"{AR_MALFI_MYTHOS.complication_event_id}"
    )
    print(
        f"  denouement_event_id: "
        f"{AR_MALFI_MYTHOS.denouement_event_id}"
    )
    print(
        f"  observations: {len(observations)} "
        f"(expected 2 noted — instrumental-kind canonical-plus-open; "
        f"check 5 does NOT fire on Malfi's polarity-concordant pair)"
    )
    print(f"  substrate events (for grounding): {len(FABULA)}")
    print(f"  current_τ_a: {args.current_tau_a}")
    print(f"  anchor_τ_a: {args.anchor_tau_a or args.current_tau_a}")

    substrate_events = [] if args.no_substrate_context else list(FABULA)

    result = invoke_aristotelian_reader_model(
        mythoi=(AR_MALFI_MYTHOS,),
        observations=observations,
        substrate_events=substrate_events,
        character_arc_relations=AR_MALFI_CHARACTER_ARC_RELATIONS,
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
            "mythoi_ids": [AR_MALFI_MYTHOS.id],
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
            "  [P5-P12 below use unconstrained substring matching; "
            "'candidate' results must be verified against the JSON "
            "artifact.]"
        )

        # P5 — OQ-LEAR-4 cross-encoding-pressure forcing check.
        p5_tokens = (
            "secondary peripeteia", "secondary_peripeteia",
            "multiple peripeteia", "second peripeteia",
            "arc peripeteia", "arc-peripeteia",
            "character-arc peripeteia",
            "peripeteia per phase", "per-phase peripeteia",
            "Bosola's reversal", "Bosola's peripeteia",
            "Antonio's reversal", "Antonio's peripeteia",
            "Ferdinand's peripeteia", "subplot peripeteia",
        )
        p5_scope = _token_hits(dr.scope_limits_observed, p5_tokens)
        p5_rel = _token_hits(dr.relations_wanted, p5_tokens)
        p5_hit = bool(p5_scope or p5_rel)
        print(
            f"  P5 (forcing — OQ-LEAR-4 cross-encoding pressure): "
            f"{'candidate — verify in JSON' if p5_hit else 'no substring matches'}"
        )
        if p5_scope:
            print(f"       scope_limits hits: {p5_scope}")
        if p5_rel:
            print(f"       relations_wanted hits: {p5_rel}")

        # P6 — OQ-AP7 third-encoding distance-6 forcing check.
        p6_tokens = (
            "distance", "narrow", "near", "distant", "wide",
            "intense", "compressed", "rapid recognition",
            "dense cluster", "Act IV cluster", "numerical",
            "range of separated", "six τ_s", "six units",
        )
        p6_scope = _token_hits(dr.scope_limits_observed, p6_tokens)
        p6_rel = _token_hits(dr.relations_wanted, p6_tokens)
        p6_hit = bool(p6_scope or p6_rel)
        print(
            f"  P6 (forcing — OQ-AP7 third-encoding distance-6): "
            f"{'candidate — verify in JSON' if p6_hit else 'no substring matches'}"
        )
        if p6_scope:
            print(f"       scope_limits hits: {p6_scope}")
        if p6_rel:
            print(f"       relations_wanted hits: {p6_rel}")

        # P7 — OQ-MALFI-1 sequentially-wielded-instrument check.
        p7_tokens = (
            "two wielders", "two employers", "sequential",
            "temporal phase", "temporal-phase",
            "polarity concordance", "polarity-concordance",
            "polarity concordant", "polarity-concordant",
            "same polarity", "shared polarity",
            "shared instrument", "transferred instrument",
            "instrument transferred", "instrument-transferred",
            "Bosola as instrument", "passed across", "passed between",
        )
        p7_scope = _token_hits(dr.scope_limits_observed, p7_tokens)
        p7_rel = _token_hits(dr.relations_wanted, p7_tokens)
        p7_hit = bool(p7_scope or p7_rel)
        print(
            f"  P7 (forcing — OQ-MALFI-1 sequentially-wielded "
            f"instrument): "
            f"{'candidate — verify in JSON' if p7_hit else 'no substring matches'}"
        )
        if p7_scope:
            print(f"       scope_limits hits: {p7_scope}")
        if p7_rel:
            print(f"       relations_wanted hits: {p7_rel}")

        # P8 — Bosola-as-co-protagonist (related to OQ-LEAR-4).
        p8_tokens = (
            "Bosola is the protagonist", "Bosola is structurally",
            "Bosola as protagonist", "co-protagonist",
            "Bosola's arc", "structural protagonist",
            "instrument-character protagonist",
            "Bosola at the center", "Bosola at the structural",
        )
        p8_hits = _token_hits(all_surfaces, p8_tokens)
        p8_hit = bool(p8_hits)
        print(
            f"  P8 (forcing-related — Bosola-as-co-protagonist): "
            f"{'candidate — verify in JSON' if p8_hit else 'no substring matches'}"
        )
        if p8_hits:
            print(f"       hits: {p8_hits}")

        # P9 — OQ-AP6 closure-verification (should NOT re-surface).
        p9_tokens = (
            "three tragic", "multiple tragic", "three-hero",
            "intra-mythos parallel", "ArParallelHeroes",
        )
        p9_hits = _token_hits(all_surfaces, p9_tokens)
        p9_hit = bool(p9_hits)
        print(
            f"  P9 (closure-check — OQ-AP6 parallel-heroes): "
            f"{'candidate re-surface — verify in JSON' if p9_hit else 'clean (closure holds on third encoding)'}"
        )
        if p9_hits:
            print(f"       hits: {p9_hits}")

        # P10 — OQ-AP14 sketch-05 closure-verification (should NOT
        # re-surface as vocabulary pressure).
        p10_tokens = (
            "fourth canonical kind", "fourth kind",
            "canonicalize instrumental", "promote instrumental",
            "ARC_RELATION_INSTRUMENTAL",
            "instrumental should be canonical",
        )
        p10_hits = _token_hits(all_surfaces, p10_tokens)
        p10_hit = bool(p10_hits)
        print(
            f"  P10 (closure-check — OQ-AP14 sketch-05 closure): "
            f"{'candidate re-surface — verify in JSON' if p10_hit else 'clean (directionality+polarity adequate)'}"
        )
        if p10_hits:
            print(f"       hits: {p10_hits}")

        # P11 — OQ-LEAR-2 closure (asserts_unity binary).
        p11_tokens = (
            "unity of action shape", "unity_of_action_shape",
            "positively named", "named unity shape",
            "classical unity vs", "double-plot-parallel",
            "multi-testimony-contest",
        )
        p11_hits = _token_hits(all_surfaces, p11_tokens)
        p11_hit = bool(p11_hits)
        print(
            f"  P11 (closure-check — OQ-LEAR-2 unity binary): "
            f"{'candidate re-surface — verify in JSON' if p11_hit else 'clean (binary adequate)'}"
        )
        if p11_hits:
            print(f"       hits: {p11_hits}")

        # P12 — OQ-AP5 retirement-confirmation (should NOT surface
        # — Malfi has no supernatural agents).
        p12_tokens = (
            "ArFateAgent", "fate-agent", "fate agent",
            "prophecy", "supernatural", "oracle", "divine",
        )
        p12_hits = _token_hits(all_surfaces, p12_tokens)
        p12_hit = bool(p12_hits)
        print(
            f"  P12 (retirement — OQ-AP5 fate-agent): "
            f"{'candidate — verify in JSON' if p12_hit else 'clean (fifth negative confirmation)'}"
        )
        if p12_hits:
            print(f"       hits: {p12_hits}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
