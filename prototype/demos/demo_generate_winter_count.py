"""
demo_generate_winter_count.py — generate THE WINTER COUNT: the
anti-marketing tragedy, end to end.

The showcase run for the Failure × Bad corner of the grid: a steadfast
protagonist (no arc), a goal that is lost, a judgment that stays bad, no
villain anywhere — and a generation pipeline that can hold that shape
against every gravitational pull toward redemption. The evaluator's
blind read is the proof: if the draft drifts one degree toward comfort
(an earned lesson, a softened vote, a spared child, a thaw that reads
as hope), the storyform comparison catches the drift and the repair
loop renders it back out.

Usage:
    cd prototype
    export ANTHROPIC_API_KEY=...

    # Inspect briefs + bible without an API call:
    .venv/bin/python3 -m demos.demo_generate_winter_count --dry-run

    # Generate a first draft:
    .venv/bin/python3 -m demos.demo_generate_winter_count \\
        --save-md winter_count_first_draft.md

    # Generate, blind-evaluate, and converge to the fidelity ceiling:
    .venv/bin/python3 -m demos.demo_generate_winter_count \\
        --converge --max-iters 3 --save-md winter_count_converged.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from story_engine.core.draft_generator import (
    generate_draft, result_to_payload,
)
from story_engine.core.dramatica_generation import (
    DramaticaStoryform, DramaticaFrame,
)
from story_engine.encodings.winter_count import (
    FABULA, SJUZHET, DESCRIPTIONS, ENTITIES,
)
from story_engine.encodings import winter_count_dramatica_complete as WD

_ACTION_SUMMARY = (
    "Halla Ketilsdottir, Measurer of Vastisetr, holds the town's common "
    "store through the earliest winter in memory. When she finds rot in "
    "the deep bins — a third of the grain gone — she seals the bins and "
    "lets the published count stand, reasoning that panic kills faster "
    "than hunger. Her brother Eirik forges her mark to feed a starving "
    "family; her lie shields his theft, his theft hostages her lie. On "
    "the strength of the false number the town votes down its one exit "
    "— a crossing to Hestfell — while the high snow would still bear "
    "sledges. A child dies, the ration is cut, the truth comes out at "
    "the Beehive alehouse, and the compact of the count dies with it: "
    "the granary burns in the riot, the hungry weeks fill the ledger's "
    "back pages, and Eirik dies on the pass trying to be the help "
    "nobody sent for. Spring finds Halla at her table, unchanged, "
    "keeping a perfect count of the dead."
)

_DIALECT_NOTE = (
    "A Dramatica storyform in the FAILURE x BAD corner: a full tragedy, "
    "and a STEADFAST Main Character — she does not arc, does not learn "
    "a redeeming lesson, does not soften. The reader carries the rot "
    "from the third scene onward; every catastrophe after is a DECISION "
    "made rationally on false arithmetic, never a coincidence. Render "
    "in cold, precise, unornamented prose — ledger prose, Norse-winter "
    "register, no melodrama: the horror is arithmetic, and the coldest "
    "sentences should be the ones doing sums. Do NOT sand the edges: "
    "the vote must be reasonable, the child must die off no one's "
    "villainy, the ending must refuse consolation. The final scene "
    "closes the loop of the first: a woman at a table, counting.\n\n"
    "=== SIGNPOST TERRITORY (the exact structural ground of each act) ===\n"
    + "\n".join(
        f"- {sp_id}: {detail}" for sp_id, detail in WD.SIGNPOST_DETAILS.items()
    )
)


def _storyform() -> DramaticaStoryform:
    return DramaticaStoryform(
        title="The Winter Count",
        action_summary=_ACTION_SUMMARY,
        domain_assignments=WD.DOMAIN_ASSIGNMENTS,
        signposts=WD.ALL_SIGNPOSTS,
        dynamics=WD.DYNAMIC_STORY_POINTS,
        story_goal=WD.STORY_GOAL,
        story_consequence=WD.STORY_CONSEQUENCE,
        canonical_ending=WD.CANONICAL_ENDING,
        act_event_ids=WD.ACT_EVENT_IDS,
    )


def _cli():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--effort", default="high",
                   choices=["low", "medium", "high", "max"])
    p.add_argument("--max-tokens", type=int, default=6000)
    p.add_argument("--save-md", metavar="PATH")
    p.add_argument("--save-json", default="winter_count_draft.json",
                   help="Structured draft artifact (default: "
                        "winter_count_draft.json).")
    p.add_argument("--from-json", metavar="PATH",
                   help="Load a structured draft instead of generating.")
    p.add_argument("--evaluate", action="store_true",
                   help="After generating, blind-decompile and score "
                        "Dramatica fidelity.")
    p.add_argument("--converge", action="store_true",
                   help="Iterate evaluate -> repair -> re-evaluate to the "
                        "fidelity ceiling.")
    p.add_argument("--max-iters", type=int, default=3)
    p.add_argument("--eval-effort", default="high",
                   choices=["low", "medium", "high", "max"])
    return p.parse_args()


def _evaluate(draft_text: str, storyform, effort: str):
    from story_engine.core.dramatica_evaluator import (
        decompile_dramatica, compare_to_storyform,
    )
    reading = decompile_dramatica(
        draft_text, title="The Winter Count", effort=effort,
        max_tokens=6000,
    )
    return compare_to_storyform(reading, storyform), reading


def _print_report(report, reading=None):
    mark = {"preserved": "✓", "drifted": "~", "lost": "✗", "added": "+"}
    for f in report.findings:
        print(f"  {mark.get(f.verdict, '?')} {f.dimension:16s} "
              f"authored={f.authored!r:24s} read={f.decompiled!r}")
    print(f"\n  FIDELITY: {report.preserved}/{len(report.scored)} "
          f"preserved ({round(100 * report.score)}%)")
    if reading is not None:
        print(f"  ending read as: {reading.ending_shape!r} "
              f"(outcome={reading.outcome}, judgment={reading.judgment})")


def main() -> int:
    args = _cli()
    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set (or pass --dry-run).",
              file=sys.stderr)
        return 1

    storyform = _storyform()
    frame = DramaticaFrame(storyform, SJUZHET)

    print("Substrate → first-draft generator — THE WINTER COUNT")
    print(f"  dialect: Dramatica | ending: {WD.CANONICAL_ENDING} "
          f"(Failure × Bad) | resolve: steadfast")
    print(f"  fabula: {len(FABULA)} | sjuzhet: {len(SJUZHET)} | "
          f"effort: {args.effort}\n")

    def on_scene(s):
        if args.dry_run:
            print("=" * 72)
            print(f"BRIEF staged-τ_d={s.τ_d} ({s.event_id}) "
                  f"focalizer={s.focalizer}")
            print("=" * 72)
            print(s.brief + "\n")
        else:
            print(f"  [staged #{s.τ_d:>2}] {s.event_id:20s} → "
                  f"{len(s.prose.split())} w")

    # 0. Obtain a structured draft (generate, or reload a saved one).
    if args.from_json and os.path.exists(args.from_json):
        print(f"[load] structured draft from {args.from_json}")
        payload = json.load(open(args.from_json))
    else:
        result = generate_draft(
            title="The Winter Count", sjuzhet=SJUZHET, fabula=FABULA,
            entities=ENTITIES, descriptions=DESCRIPTIONS, adapter=frame,
            dialect_note=_DIALECT_NOTE, effort=args.effort,
            max_tokens=args.max_tokens, dry_run=args.dry_run,
            on_scene=on_scene,
        )
        if args.dry_run:
            print("\n" + "=" * 72 + "\nSTORY BIBLE\n" + "=" * 72)
            print(result.story_bible)
            return 0
        payload = result_to_payload(result)
        json.dump(payload, open(args.save_json, "w"), indent=1)
        print(f"\n[saved structured draft to {args.save_json}]")

    scenes = payload["scenes"]

    # 1. Converge (evaluate → repair → splice → re-evaluate), or a single
    #    blind evaluation.
    if args.converge:
        from story_engine.core.draft_convergence import converge, assemble
        from story_engine.core.draft_repair import repair_scene
        from story_engine.core.dramatica_repair import plan_repairs

        def evaluate_fn(text):
            report, _ = _evaluate(text, storyform, args.eval_effort)
            return report

        def repair_fn(directive):
            rr = repair_scene(
                directive, sjuzhet=SJUZHET, fabula=FABULA,
                entities=ENTITIES, descriptions=DESCRIPTIONS,
                adapter=frame, title="The Winter Count",
                dialect_note=_DIALECT_NOTE, effort=args.effort,
                max_tokens=args.max_tokens,
            )
            return rr.after if rr else None

        def on_round(rec, report, directives):
            print(f"\n[round {rec.iteration}] fidelity "
                  f"{round(100 * rec.score)}% — "
                  f"{rec.n_directives} directive(s)")
            _print_report(report)

        run = converge(
            scenes=scenes, mythos=storyform,
            evaluate_fn=evaluate_fn, repair_fn=repair_fn,
            plan_fn=lambda report, sf: plan_repairs(report, sf, SJUZHET),
            max_iters=args.max_iters, on_round=on_round,
        )
        print(f"\n[converged] {round(100 * run.initial_score)}% → "
              f"{round(100 * run.final_score)}% in "
              f"{len(run.history)} round(s) "
              f"({run.history[-1].stopped})")
        json.dump(payload, open(args.save_json, "w"), indent=1)
        draft_text = assemble(scenes)
    else:
        from story_engine.core.draft_convergence import assemble
        draft_text = assemble(scenes)
        if args.evaluate:
            print("\n" + "=" * 72)
            print("DRAMATICA FIDELITY — decompile blind, score vs storyform")
            print("=" * 72)
            report, reading = _evaluate(draft_text, storyform,
                                        args.eval_effort)
            _print_report(report, reading)

    print("\n" + "=" * 72)
    print(f"DRAFT — The Winter Count ({len(draft_text.split())} words)")
    print("=" * 72)
    print(draft_text)

    if args.save_md:
        with open(args.save_md, "w") as f:
            f.write("# The Winter Count — first draft "
                    "(Dramatica dialect)\n\n")
            f.write("_An original Vastisetr tragedy generated from the "
                    "verified substrate: Outcome=Failure, Judgment=Bad, "
                    "Resolve=Steadfast — every commercial imperative "
                    "refused, every structural commitment kept. The "
                    "engine is the author of record; the model is the "
                    "renderer._\n\n")
            f.write(draft_text)
            f.write("\n\n---\n\n## Appendix — story bible\n\n```\n"
                    + payload.get("story_bible", "") + "\n```\n")
        print(f"\n[saved draft to {args.save_md}]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
