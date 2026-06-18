"""
demo_converge_malfi.py — iterate generate → evaluate → repair to a
structural-fidelity ceiling, on a structured Malfi draft.

This is the repair loop made a PIPELINE: each iteration evaluates the
WHOLE draft, repairs the localizable drifts, splices the re-rendered
scenes back in, and the NEXT iteration's whole-draft evaluation is the
proof the repairs improved fidelity. Loops until fidelity stops climbing.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...

    # Generate a structured draft, then converge (saves malfi_draft.json):
    .venv/bin/python3 -m demos.demo_converge_malfi --max-iters 3

    # Re-run convergence on an already-generated structured draft (cheap —
    # skips the 30-scene generation):
    .venv/bin/python3 -m demos.demo_converge_malfi --from-json malfi_draft.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from story_engine.core.draft_generator import (
    generate_draft, result_to_payload,
)
from story_engine.core.draft_evaluator import decompile_draft, compare_to_mythos
from story_engine.core.draft_repair import repair_scene
from story_engine.core.draft_convergence import converge, assemble
from story_engine.encodings.malfi import (
    FABULA, SJUZHET, DESCRIPTIONS, ENTITIES, PREPLAY_DISCLOSURES,
)
from story_engine.encodings.malfi_aristotelian import AR_MALFI_MYTHOS

_DIALECT_NOTE = (
    "Aristotelian tragedy (complex plot) with a DISTRIBUTED fall: one "
    "mythos carrying several tragic arcs (the Duchess, then Ferdinand, "
    "Bosola, Antonio), a pathos-centre (the Duchess) split from the "
    "recognizer (Ferdinand), and an anti-recognition (Antonio's dark-room "
    "death — truth too late). Render as dramatic prose in Webster's cold, "
    "ironic register."
)


def _generate_structured(effort, max_tokens):
    print(f"[generate] rendering {len(SJUZHET)} scenes...")

    def on_scene(s):
        print(f"  [τ_d={s.τ_d:>2}] {s.event_id:30s} → {len(s.prose.split())} w")

    result = generate_draft(
        title="The Duchess of Malfi", sjuzhet=SJUZHET, fabula=FABULA,
        entities=ENTITIES, descriptions=DESCRIPTIONS, mythos=AR_MALFI_MYTHOS,
        preplay_disclosures=PREPLAY_DISCLOSURES, dialect_note=_DIALECT_NOTE,
        effort=effort, max_tokens=max_tokens, on_scene=on_scene,
    )
    return result_to_payload(result)


def _cli_args():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--from-json", metavar="PATH",
                   help="Load a structured draft instead of generating.")
    p.add_argument("--save-json", default="malfi_draft.json",
                   help="Where to save the structured draft (default: "
                        "malfi_draft.json).")
    p.add_argument("--save-md", default="malfi_converged.md")
    p.add_argument("--max-iters", type=int, default=3)
    p.add_argument("--inject-drift", metavar="EVENT_ID",
                   help="Before converging, re-render this scene with a "
                        "drift directive (Antonio dies unknowing) to "
                        "deterministically exercise the recovery path.")
    p.add_argument("--gen-effort", default="medium",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--eval-effort", default="high",
                   choices=["low", "medium", "high", "max"])
    return p.parse_args()


def main() -> int:
    args = _cli_args()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        return 1

    # 0. Obtain a structured draft.
    if args.from_json and os.path.exists(args.from_json):
        print(f"[load] structured draft from {args.from_json}")
        payload = json.load(open(args.from_json))
    else:
        payload = _generate_structured(args.gen_effort, 4000)
        json.dump(payload, open(args.save_json, "w"), indent=1)
        print(f"[saved structured draft to {args.save_json}]")

    scenes = payload["scenes"]

    # Optional: inject a known structural regression to exercise the
    # recovery path (a controlled demonstration, not a real drift).
    if args.inject_drift:
        from story_engine.core.draft_repair import repair_scene
        from story_engine.core.draft_repair import RepairDirective
        drift = RepairDirective(
            event_id=args.inject_drift, dimension="injected_drift",
            authored="(controlled regression)",
            instruction=(
                "Antonio dies COMPLETELY UNKNOWING — he never realizes who "
                "strikes him in the dark or why; render NO recognition for "
                "Antonio. Tell the killing entirely from Bosola's "
                "perspective; Antonio is a body in the dark, not a mind "
                "arriving at truth."
            ),
        )
        print(f"[inject-drift] regressing {args.inject_drift} "
              f"(Antonio dies unknowing)...")
        rr = repair_scene(
            drift, sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
            descriptions=DESCRIPTIONS, mythos=AR_MALFI_MYTHOS,
            preplay_disclosures=PREPLAY_DISCLOSURES,
            title="The Duchess of Malfi", dialect_note=_DIALECT_NOTE,
            effort="medium", max_tokens=4000,
        )
        if rr:
            for s in scenes:
                if s["event_id"] == args.inject_drift:
                    s["prose"] = rr.after
            print(f"      regressed scene τ_d={rr.τ_d} "
                  f"({len(rr.after.split())} words)\n")

    print(f"\nConverging — The Duchess of Malfi "
          f"({len(scenes)} scenes, {len(assemble(scenes).split())} words)")
    print(f"  authored spine: pathos-centre="
          f"{', '.join(AR_MALFI_MYTHOS.pathos_character_ref_ids)} | "
          f"recognizer={AR_MALFI_MYTHOS.anagnorisis_character_ref_id} | "
          f"max-iters={args.max_iters}\n")

    # Wire the real evaluate / repair functions into the controller.
    def evaluate_fn(text):
        decompiled = decompile_draft(
            text, title="The Duchess of Malfi",  # genre-only note (blind)
            effort=args.eval_effort, max_tokens=8000,
        )
        return compare_to_mythos(decompiled, AR_MALFI_MYTHOS)

    def repair_fn(directive):
        rr = repair_scene(
            directive, sjuzhet=SJUZHET, fabula=FABULA, entities=ENTITIES,
            descriptions=DESCRIPTIONS, mythos=AR_MALFI_MYTHOS,
            preplay_disclosures=PREPLAY_DISCLOSURES,
            title="The Duchess of Malfi", dialect_note=_DIALECT_NOTE,
            effort="medium", max_tokens=4000,
        )
        return rr.after if rr else ""

    def on_round(rec, report, directives):
        print(f"  [iter {rec.iteration}] fidelity "
              f"{report.preserved}/{len(report.scored)} "
              f"({round(100*rec.score)}%)")
        for f in report.findings:
            if f.verdict in ("lost", "drifted"):
                print(f"      ✗ {f.dimension}: {f.authored!r} → {f.decompiled!r}")
        if directives:
            print(f"      → repairing: "
                  f"{', '.join(d.event_id for d in directives)}")

    run = converge(
        scenes=scenes, mythos=AR_MALFI_MYTHOS,
        evaluate_fn=evaluate_fn, repair_fn=repair_fn,
        max_iters=args.max_iters, target=1.0, on_round=on_round,
    )

    print("\n" + "=" * 70)
    print("CONVERGENCE TRAJECTORY")
    print("=" * 70)
    for rec in run.history:
        tail = f"  [{rec.stopped}]" if rec.stopped else ""
        rep = (f"  repaired: {', '.join(rec.repaired_events)}"
               if rec.repaired_events else "")
        print(f"  iter {rec.iteration}: {round(100*rec.score)}%{rep}{tail}")
    print(f"\n  {round(100*run.initial_score)}% → {round(100*run.final_score)}% "
          f"({'+' if run.improved >= 0 else ''}{round(100*run.improved)} pts)")

    # Persist the converged draft.
    payload["scenes"] = run.scenes
    json.dump(payload, open(args.save_json, "w"), indent=1)
    with open(args.save_md, "w") as f:
        f.write(f"# {payload['title']} — converged draft\n\n")
        f.write(f"_Fidelity {round(100*run.initial_score)}% → "
                f"{round(100*run.final_score)}% over {len(run.history)} "
                f"round(s) of evaluate → repair against the substrate._\n\n")
        f.write(assemble(run.scenes))
    print(f"\n[saved converged draft to {args.save_md} + {args.save_json}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
