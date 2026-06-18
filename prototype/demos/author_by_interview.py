"""
author_by_interview.py — the AI-interview authoring front-end, end to end.

The loop: a natural brief → extract the authoring draft (LLM) → the draft's
gaps become the interviewer's questions (deterministic spine) → answer → extract
again → when no blocking gap remains, compile to the verified substrate, run the
self-verifier, and (optionally) generate.

Usage:
    cd prototype

    # No API: show the SPINE — a deliberately-partial story, and the exact
    # questions the interviewer would ask, in priority order. The skeleton (●)
    # is dialect-agnostic; the structural homework (○) is per-dialect:
    PYTHONPATH=. python3 -m demos.author_by_interview --dry-run
    PYTHONPATH=. python3 -m demos.author_by_interview --dry-run --dialect dramatica

    # Live: extract a draft from a brief and show what it still needs.
    export ANTHROPIC_API_KEY=...
    PYTHONPATH=. .venv/bin/python3 -m demos.author_by_interview \
        --brief "A lighthouse keeper, proud of his great lens, ..." \
        --answers "The reversal is when the lens fails in the storm; ..."

    # Add --generate to render the first scene once it compiles clean.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from story_engine.core.authoring_interview import (
    interview_gaps, blocking_gaps, is_compilable, extract_story_draft,
    run_interview, DIALECTS,
)
from story_engine.core.authoring import compile_story, verify_compiled


_SPARSE_BRIEF = "A lighthouse keeper's pride costs a ship. It ends badly."


def _simulated_author(premise, effort):
    """An answer_fn backed by an LLM playing the AUTHOR: it answers the
    interviewer's questions from the premise, inventing consistent specifics
    a writer would — so the multi-round loop runs autonomously."""
    from pydantic import BaseModel, Field
    from story_engine.core.reader_model_client_base import invoke_parse_helper

    class Answers(BaseModel):
        answers: str = Field(description="concise, concrete answers to the "
                             "interviewer's questions")

    def answer_fn(questions, _doc):
        if not questions:
            return ""
        q = "\n".join(f"- {x}" for x in questions)
        out = invoke_parse_helper(
            system_prompt="You are the AUTHOR of a story being interviewed by "
                          "a story-structure engine. Answer concretely and "
                          "consistently, committing to specifics a writer "
                          "would choose. Keep it brief.",
            user_prompt=f"Your story premise:\n{premise}\n\nThe interviewer "
                        f"asks:\n{q}\n\nAnswer each, briefly.",
            output_format=Answers, model="claude-opus-4-6",
            max_tokens=1500, effort=effort, dry_run=False,
        )
        return out.answers if out else ""
    return answer_fn


_SAMPLE_BRIEF = (
    "A lighthouse keeper named Halvard is proud of his great lens — prouder of "
    "the instrument than of the sea it serves. One storm night the lens he "
    "over-trusts fails at the worst moment and a ship goes down; his daughter "
    "Mara is the one who has to live with what his pride cost. He finally sees "
    "it, too late."
)

# A deliberately-partial authoring draft, for the no-API spine demo: it has
# beats but no story-time order, no phases, and no structural marks yet —
# exactly what the interviewer should ask about next.
_PARTIAL_DOC = {
    "title": "The Vantage Light",
    "characters": [
        {"id": "halvard", "name": "Halvard", "role": "tragic-hero"},
        {"id": "mara", "name": "Mara", "role": "figure"},
    ],
    "events": [
        {"id": "calm", "who": ["halvard"],
         "summary": "Halvard polishes the great lens, proud of its reach."},
        {"id": "storm", "who": ["halvard", "mara"],
         "summary": "The storm rises and the lens fails."},
        {"id": "wreck", "who": ["halvard"],
         "summary": "A ship goes down within sight of the light."},
    ],
}


def _show_questions(doc, dialect="aristotelian"):
    gaps = interview_gaps(doc, dialect)
    blk = [g for g in gaps if g.severity == "blocking"]
    stc = [g for g in gaps if g.severity == "structural"]
    print(f"\nThe interview would ask ({len(blk)} blocking, "
          f"{len(stc)} structural; dialect: {dialect}):")
    for g in blk:
        print(f"  ● [{g.code}] {g.question}")
    for g in stc:
        print(f"  ○ [{g.code}] {g.question}")
    if not gaps:
        print("  (nothing — the story is well-formed and ready to generate.)")
    return blk


def _cli():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--brief", default=_SAMPLE_BRIEF)
    p.add_argument("--answers", default="",
                   help="The author's answers to a prior round of questions.")
    p.add_argument("--dry-run", action="store_true",
                   help="Show the spine on a built-in partial story (no API).")
    p.add_argument("--interview", action="store_true",
                   help="Run the multi-round loop from a SPARSE brief with an "
                        "AI-simulated author answering each round (autonomous).")
    p.add_argument("--generate", action="store_true",
                   help="If the draft compiles clean, render the first scene.")
    p.add_argument("--dialect", default="aristotelian",
                   choices=sorted(DIALECTS),
                   help="Which dialect's structural homework to elicit.")
    p.add_argument("--effort", default="high",
                   choices=["low", "medium", "high", "max"])
    return p.parse_args()


def _compile_or_note(doc, dialect):
    """Compile the well-formed draft. The live TOML→substrate compiler lands
    the skeleton + the Aristotelian overlay; the other dialects' structural
    homework is fully elicited and gap-checked here, and their record is
    verified by the existing per-dialect encodings — the TOML→overlay compiler
    for them is the remaining, named seam. Returns the CompiledStory, or None."""
    if dialect != "aristotelian":
        print(f"\nNo blocking gaps — the {dialect} record is well-formed and "
              f"its structural homework is complete.\n[Note: the live "
              f"TOML→substrate compiler targets the Aristotelian overlay; the "
              f"{dialect} overlay compiler is not yet wired (see the coverage "
              f"grid). The record is verifier-ready in the {dialect} encodings.]")
        return None
    print("\nNo blocking gaps — compiling to the verified substrate...")
    compiled = compile_story(doc)
    obs = verify_compiled(compiled)
    print(f"  compiled: {len(compiled.fabula)} events, "
          f"{len(compiled.entities)} entities; "
          f"verifier observations: {len(obs)}")
    return compiled


def main() -> int:
    args = _cli()

    if args.dry_run:
        print("=" * 72)
        print("SPINE DEMO (no API) — the substrate's homework as questions")
        print("=" * 72)
        print(f"\nPartial draft:\n{json.dumps(_PARTIAL_DOC, indent=1)}")
        _show_questions(_PARTIAL_DOC, args.dialect)
        print(f"\n[dry run — each ● must be answered before it compiles; each ○ "
              f"is {args.dialect} polish the author may decline. The skeleton "
              f"(●) is the same in every dialect; the homework (○) is not — "
              f"try --dialect save-the-cat / dramatica / dramatic.]")
        return 0

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set (or pass --dry-run).",
              file=sys.stderr)
        return 1

    if args.interview:
        brief = args.brief if args.brief != _SAMPLE_BRIEF else _SPARSE_BRIEF
        print("=" * 72)
        print("MULTI-ROUND INTERVIEW (AI-simulated author)")
        print("=" * 72)
        print(f"\nSparse brief: {brief}\n")

        def on_round(rec, blocking, structural):
            print(f"  [round {rec.round}] {rec.n_blocking} blocking, "
                  f"{rec.n_structural} structural"
                  + (f" — STOP: {rec.stopped}" if rec.stopped else ""))
            for g in (blocking + structural)[:3]:
                print(f"      ? {g.question}")
            if rec.answers:
                print(f"      ↳ author: {rec.answers[:160].strip()}…")

        run = run_interview(
            brief=brief, dialect=args.dialect,
            extract_fn=lambda b, prior, ans: extract_story_draft(
                b, dialect=args.dialect, prior=prior, answers=ans,
                effort=args.effort),
            answer_fn=_simulated_author(brief, args.effort),
            max_rounds=6, on_round=on_round,
        )
        print(f"\n{'complete' if run.complete else 'stopped: ' + run.rounds[-1].stopped}"
              f" after {len(run.rounds)} round(s); "
              f"compilable: {run.compilable}")
        if run.compilable:
            _compile_or_note(run.final_doc, args.dialect)
        return 0

    print("=" * 72)
    print("INTERVIEW — brief → draft → questions")
    print("=" * 72)
    print(f"\nBrief: {args.brief}\n")

    doc = extract_story_draft(args.brief, dialect=args.dialect,
                              answers=args.answers or None, effort=args.effort)
    print("Extracted authoring draft:")
    print(json.dumps(doc, indent=1))
    blk = _show_questions(doc, args.dialect)

    if not is_compilable(doc, args.dialect):
        print(f"\n[{len(blk)} blocking question(s) remain — answer them and "
              f"re-run with --answers to continue the interview.]")
        return 0

    compiled = _compile_or_note(doc, args.dialect)

    if compiled is not None and args.generate:
        from story_engine.core.draft_generator import generate_draft
        print("\nGenerating the first scene...")
        result = generate_draft(
            title=compiled.title, sjuzhet=compiled.sjuzhet[:1],
            fabula=compiled.fabula, entities=compiled.entities,
            descriptions=compiled.descriptions, mythos=compiled.mythos,
            preplay_disclosures=compiled.preplay_disclosures,
            dialect_note=f"{args.dialect} story authored by interview.",
            effort="medium", max_tokens=2000,
        )
        print("\n" + (result.draft or "(no prose)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
