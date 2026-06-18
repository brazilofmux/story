# Authoring front-end — sketch 01 (the interview: the substrate's homework becomes the conversation)

**Status:** active; deterministic gap-spine + extraction schema landing
**Date:** 2026-06-18
**Supersedes:** nothing (new topic)
**Extends:** `authoring.py` (the `.story.toml` front-end) — same compile target, a friendlier surface.
**Frames:** [state-of-play-19](state-of-play-19.md); memory `project-goal-generation-tool` (generation-first end goal).

## The idea

`authoring.py` already lets a writer author a story in a plain-text
`.story.toml` that compiles to the verified substrate + Aristotelian overlay
the engine consumes. But TOML is still a form to learn. The front-end we want
is a **conversation**: an AI interviewer elicits the story and compiles the
answers into the same authoring dict — no format to learn.

The elegant part, and why this fits the project rather than bolting an LLM on:
the engine's whole thesis is *force the author to do the structural homework*.
The compiler's hard requirements (every event needs a story-time `when`; an
`anagnorisis` needs a `recognizer`) and the Aristotelian structural marks (a
complex plot wants a peripeteia and a recognition) are **exactly the questions
an interviewer should ask.** So the interview is not a separate UX layer — it
is the verifier/compiler, turned around to face the author.

## Architecture — three parts, one already exists

```
  free-text answers ──(LLM extract/merge)──▶ authoring dict ──(authoring.compile_story)──▶ substrate
        ▲                                          │
        │                                          ▼
        └────────(phrase as questions)──── interview_gaps(doc)   ← the spine
```

1. **`interview_gaps(doc) -> [Gap]` — the spine (pure, deterministic, no API).**
   Reads the authoring dict and reports what is missing or under-committed,
   each as a human-facing question with a severity:
   - **blocking** — `compile_story` would refuse (no title, no events, an event
     with no `when` or `summary`, a participant who is not a declared
     character);
   - **structural** — the Aristotelian homework (no peripeteia marked; an
     anagnorisis with no recognizer; a tragic-hero with no hamartia; no
     pathos-centre; beats not divided into beginning/middle/end).
   This is the conceptual heart and it needs no model — it is the substrate's
   demands, enumerated.

2. **`extract_story_draft(brief, prior=None, answers=None) -> dict` (LLM).**
   Turns a natural brief (and successive answers) into / merges into the
   authoring dict — typed extraction (pydantic, like the evaluators), so the
   model fills structured fields, not prose. Lazily imported so the spine stays
   standard-library.

3. **`authoring.compile_story` / `verify_compiled` — already exist.** The
   interview loop ends by compiling, running the dialect self-verifier, and
   handing the result to the generation pipeline.

## The loop

```
draft = extract_story_draft(opening_brief)
while gaps := [g for g in interview_gaps(draft) if g.severity == "blocking"] or structural_gaps(draft):
    ask the top gaps as questions  →  answers
    draft = extract_story_draft(brief, prior=draft, answers=answers)
compiled = compile_story(draft);  verify_compiled(compiled);  generate
```

Blocking gaps gate compilation; structural gaps are offered but the author may
decline (a simple plot is allowed). The interviewer asks the substrate's
questions in the substrate's priority order, and stops when the story is
well-formed enough to generate.

## Scope / honesty

- **Aristotelian-first**, matching `authoring.py`'s overlay vocabulary
  (tragic-hero / pathos-centre / figure; peripeteia / anagnorisis). The dict
  target and the gap rules generalize to the other dialects later, the same way
  the rest of the stack did.
- **The deep who-knows-what-when discipline is only lightly probed in v1.** The
  spine checks the structural skeleton (events, marks, recognizer, phases); the
  substrate's full knowledge-fold homework (every "X knows Y" wants an
  establishing event) is a later gap-rule pass once the skeleton path is solid.
- **The extraction is LLM-shaped and self-graded** like everything else — the
  same named caveat. The *spine* is deterministic and testable, which is where
  the load-bearing correctness lives.

## Why this is the right front-end

A blank `.story.toml` asks the author to already know the structure. The
interview inverts it: the author tells the story however they think of it, and
the system asks for exactly the commitments the substrate needs to verify and
generate — no more, no less. The homework-forcing rigor that the whole engine
is built on becomes the thing that makes the front-end *helpful* rather than
demanding.
