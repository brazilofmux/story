# Authoring interview — knowledge sketch 01 (who-knows-what-when: the substrate's teeth)

**Status:** active; landed (shared knowledge gap-spine + `learns`→KnowledgeEffect compile + extraction; 39 interview / 22 authoring tests; live)
**Date:** 2026-06-18
**Extends:** [authoring-interview-sketch-01](authoring-interview-sketch-01.md) (v1 explicitly deferred this), [authoring-interview-sketch-02](authoring-interview-sketch-02.md) (per-dialect overlays), [authoring-compile-sketch-01](authoring-compile-sketch-01.md) (the four compilers).
**Frames:** SoP-20 "what's next" #1; memory `project-goal-generation-tool`.

## The idea

The interview's v1 checked the structural skeleton and each dialect's homework
but left the substrate's deepest discipline — **who knows what, when** —
unprobed. That is the engine's real teeth: dramatic irony, secrets, reveals,
and recognition all *are* facts about epistemic state and its provenance. This
pass turns that discipline into interview questions and compiles the answers
into the substrate's real knowledge records.

Crucially, knowledge lives **below the dialect** — it's a substrate concept, not
an Aristotelian or Dramatica one. So the gap rules are **shared** (they run for
all four dialects) and the compile wiring is in `_build_substrate` (lands once
for all four). The substrate has *no* knowledge verifier of its own; this is
**net-new discipline**, not a mirror.

## The authoring surface (shared skeleton)

- a beat's **`learns`**: `[{who, fact, via}]` — at this beat, `who` comes to know
  `fact` (a predicate, e.g. `flaw_known(ana)`), and `via` how: `observation`
  (they're present), `told`, `inference`, `realization`, `deception`.
- a beat's **`establishes`** (already existed): world facts made true here.
- a character's **`knows`**: facts they hold — a *claim* the spine checks has a
  source.
- top-level **`preplay`** (already existed): facts the AUDIENCE knows entering
  — the ground of dramatic irony.

## The gap rules (`_knowledge_gaps`, deterministic, silent until knowledge is asserted)

- **`knows_no_source`** (structural) — a character `knows` a fact with no beat
  that teaches it (no `learns`, not `preplay`, not an `establishes` they're
  present for). *"X is said to know 'F', but no beat establishes it for them —
  which beat do they learn it, and how?"* The headline question.
- **`learns_unknown_who`** (blocking) — a `learns` names an undeclared character
  (the compiler can't place knowledge in a non-agent).
- **`learns_bad_fact`** (blocking) — a knowledge fact not in `predicate(arg)`
  form (the compiler parses it).
- **`learns_offstage`** (structural) — learned by `observation` but the learner
  isn't present in the beat — *were they told instead?* (observation needs
  presence.)
- **`learns_before_established`** (structural) — X learns F at a beat *earlier*
  than any beat that makes F true — a timeline violation, *or* a deliberate
  false belief (`via='deception'`). The causality tooth.
- **`anag_recognizer_learns_nothing`** (structural, Aristotelian overlay) — an
  anagnorisis whose recognizer learns nothing: a recognition labelled but not
  *real* in the substrate. Connects the existing recognizer to the knowledge model.

## The compile (dialect-agnostic, in `_build_substrate`)

Each `learns` becomes a `KnowledgeEffect(agent_id=who, held=Held(prop, slot,
confidence, via, provenance))` on the beat's `Event`. `via` picks the `Diegetic`
operator (`OBSERVATION` / `UTTERANCE_HEARD` / `INFERENCE` / `REALIZATION` /
`DECEPTION`); a **deception is held `BELIEVED`, not `KNOWN`** — a false belief,
the seed of dramatic irony. `preplay` already compiles to audience `Disclosure`s.
This lands for all four dialects at once.

## Live

A dramatic-irony Aristotelian brief ("Queen Reyna secretly poisoned the wells;
the audience knows, her son the young king does not; he learns it too late") was
interviewed multi-round: **round 0 surfaced two `knows_no_source` gaps** — *"Tobin
is said to know 'mother_loyal(reyna)', but no beat establishes it — which beat do
they learn it, and how?"* — the (AI-simulated) author supplied the establishing
beats, round 1 reached zero gaps, and it compiled clean (0 verifier
observations). The substrate's teeth, turned into a conversation.

## Scope / honesty

- The **spine is the load-bearing, tested part** (deterministic, offline). The
  rules are silent when a story commits no knowledge — they speak only once the
  author asserts who knows what, so they never spam a plain interview.
- This v1 checks **provenance and timeline**, not full epistemic consistency
  (contradictory holdings, identity-chain coherence, derived-fact premises). The
  substrate supports those; later passes could verify them.
- Adding the nested `learns` field pushed every dialect's extraction schema over
  the structured-output grammar ceiling, so **all four now extract via JSON
  mode** (see `authoring-compile-sketch-01` / the `Dialect.constrained` note).
- Extraction is still LLM-shaped and self-graded; the spine isn't.
