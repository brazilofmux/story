# Compilation — sketch 01 (dialect-to-substrate compiler backend)

**Status:** draft, active
**Date:** 2026-04-21
**Supersedes:** nothing (new arc)
**Extends:** [architecture-sketch-02](architecture-sketch-02.md) (the dialect-stack frame this sketch names a backend for)
**Frames:** [lowering-sketch-01](lowering-sketch-01.md) + [lowering-sketch-02](lowering-sketch-02.md) (the reverse direction — Lowering records annotate the substrate↔dialect grounding relation; this sketch names the forward direction that generates substrate to satisfy dialect constraints); [reader-model-sketch-01](reader-model-sketch-01.md) (the LLM-as-probe role this sketch reshapes into LLM-as-ranker); every existing dialect sketch (aristotelian-sketch-01..-03; dramatic-sketch-01; save-the-cat-sketch-01; dramatica-template-sketch-01) whose commitments become compilation *inputs*
**Related:** [state-of-play-12](state-of-play-12.md) (tooling-frame memory and compiler-family vocabulary introduced over sketches 09–11); Codex-REVIEW-driven verifier extraction (the Tier-2 audit surface this sketch relies on as its compiler type-check)
**Superseded by:** nothing yet

## Purpose

Name the **forward compilation problem** at the dialect↔substrate boundary: given a set of dialect-level constraints (Aristotelian phase membership, peripeteia/anagnorisis pinning, Dramatica quad requirements, Save-the-Cat beat ordering, character relations, unity assertions) + a word budget + optional hints, produce **either** a substrate event sequence + Lowering records that satisfy every constraint, **or** a specific infeasibility error naming which constraints conflict.

This is a **framing sketch**. It commits to the compiler shape and the architectural decomposition. It does **not** commit to specific algorithms per stage — those land in per-stage follow-on sketches after the shape settles.

## Why now

Conversational origin, not a pre-banked OQ. The conversation on 2026-04-21 (immediately after state-of-play-12 committed) followed this arc:

1. User reframed project horizon: "I'd take the W if we can; otherwise produce strong inputs for a more-capable future AI." Saved as `project_solution_horizon.md`.
2. User sketched a concrete compilation strategy: "timeline / location hints + topological sort + parameterized generation (number of scenes) + random numbers."
3. First-pass response mapped it to **Partial-Order Causal Link (POCL) planning** and **procedural content generation (PCG)**.
4. User clarified: location is richer than clustering — **time+location causality** (presence required for physical action; communication channels substituting for presence; travel has time cost). Word count is the real output budget, but **Dramatica requires a minimum scene count** for the story argument to land. **Conflicting constraints = compiler error.** LLM chooses between feasible orderings (ranker, not generator).
5. The clarifications escalated the frame from "topological sort" to **classical AI planning (STRIPS/PDDL)**, a solved-problem-domain.

The compilation-sketch captures the shape before it drifts in memory. Per context-economy discipline: named shape in a durable artifact beats in-conversation agreement.

This sketch also engages the "falling out" claim explicitly (§The "falling out" observation below). Brief version: this conversation named a concrete compiler backend whose stages map individually to solved problems. It is not the implementation. The naming is the input-to-future-AI that `project_solution_horizon.md` anticipates.

## Scope — what this sketch does and doesn't do

**In scope:**
- A compilation problem statement (input / output / error conditions).
- A four-stage pipeline decomposition with named stage responsibilities.
- Architectural commitments on three axes: STRIPS-shape logistical constraints; two-level budget feasibility; LLM-as-ranker-not-generator.
- Discipline: infeasibility is loud (compiler error on constraint conflict).
- Cross-check via existing verifier/audit tooling (the compiler's type-check).
- Open questions per stage, each with a named forcing function for future sketches.
- Honest "falling out" framing — the shape is named; the implementation is multi-sketch work.

**Out of scope:**
- Per-stage algorithm choice (PDDL vs POCL vs ASP; LLM-ranker strategy). Each gets its own sketch.
- Specific state representation (propositional vs richer). Banked as OQ1.
- Prose generation from substrate. User explicitly: *"generating prose from substrate is a separate problem."* Acknowledged as out of this engine's spine and out of this sketch entirely.
- Markdown-fenced author input. Long-term roadmap item; feeds the compiler's input side but not this sketch.
- Corpus-scale validation. Requires implementation first.
- Performance targets (response time, candidate space size, parallelism).
- Impact objective for the ranker. Banked as OQ4.
- Integration with existing encoding modules. Banked as OQ6.

## Commitments

Labels **CS1..CS7** commit to structural shape; **OQ1..OQ6** bank open questions with forcing criteria.

### CS1 — Compilation problem statement

**Input:**
- `dialect_constraints`: set of dialect-level commitments (ArMythos structural fields + Aristotelian phase membership + ArCharacter relations + Dramatica quad requirements + Save-the-Cat beat ordering + unity assertions + …).
- `word_budget`: integer — total word count for the output prose.
- `hints`: optional soft constraints (timeline-ordering hints, location-co-presence hints, pacing hints).
- `rng_seed`: integer — determinism knob for the stochastic stages.

**Output (success):**
- `substrate_sequence`: tuple of substrate `Event` + `Held` + `Branch` + `Description` + `Prop` + `Entity` records, τ_s-ordered.
- `lowering_records`: tuple of `Lowering` records annotating the substrate↔dialect grounding relation — one per dialect-level claim, linking it to the substrate events that satisfy it.

**Output (failure):**
- `infeasibility_error`: a structured error naming (a) which constraints conflict, (b) at what point in the pipeline the infeasibility was detected, and (c) minimally-sufficient relaxation suggestions when the compiler can compute them.

**Architectural posture:** the compiler is a **function**, not an interactive process. Given identical inputs + seed, identical outputs. The LLM-ranker stage (CS5) is wrapped in this determinism — its temperature is 0, its candidate enumeration is deterministic given the seed.

### CS2 — Four-stage pipeline

Sequential stages; each consumes its predecessors' outputs; each can independently emit an infeasibility error that halts the pipeline.

1. **Constraint extraction.** Dialect records → normalized constraint graph. Aristotelian peripeteia/anagnorisis event-ids become **pinning constraints** on the substrate event set. ArPhase scope_event_ids become **phase-membership constraints**. `anagnorisis_chain` steps become **ordering + character + kind constraints**. `ArCharacterArcRelation.over_event_ids` become **co-presence-or-causal-link constraints** on the relevant characters. Unity assertions become **meta-constraints** on the overall substrate (single-time-span / single-location subject to dialect tolerance).
2. **Feasibility check.** CS4 below. Before planning. Arithmetic + consistency: is the requested story-shape *representable* under the requested word budget and Dramatica-minimum-scene count? Infeasibility here is loud (CS6).
3. **Planner.** CS3 below. STRIPS/PDDL-shape. Generates intermediate events (travel, communication, object-handoff) to satisfy event preconditions. Output: a space of valid substrate plans — the full solution space, not a single plan.
4. **Enumerator + ranker.** CS5 below. Solution space → finite candidate set → ranked ordering → single output. LLM's role lives here and only here.

Stages are **independently testable**. Stage 2 can be tested with hand-wired dialect constraint inputs. Stage 3 can be tested with hand-wired (post-stage-2) feasibility-checked constraint sets. Stage 4 can be tested with hand-wired (post-stage-3) solution spaces.

### CS3 — Logistical constraints are STRIPS-style preconditions

Events have **preconditions** on world state and **effects** that update it. The compiler generates **intermediate events** (travel, message-delivery, object-handoff, co-presence-establishing-meetings) to satisfy preconditions the authored events require.

Examples:
- `E_hamlet_kills_polonius` has preconditions `(hamlet@closet, polonius@behind_arras, hamlet_has_sword, hamlet_believes_claudius_behind_arras)`. If the dialect asserts the event at τ_s=8 but the substrate has Hamlet at the graveyard at τ_s=7, the compiler must emit a `travel_hamlet_to_closet` event between them, or throw an infeasibility error if no valid travel path exists.
- `E_ghost_claims_killed_by_claudius` has preconditions `(hamlet@ramparts, ghost@ramparts)`. Ghost apparition is its own precondition-lite special case — author-supplied substrate can short-circuit the meet requirement.
- Remote-action events (bomb-drop, letter-delivery, phone-call) have *substitute* preconditions (device-present-at-location; communication-channel-established).

**Architectural classification: classical AI planning.** This maps to STRIPS (Fikes-Nilsson 1971) → PDDL (Planning Domain Definition Language). Modern planners (FastDownward and descendants) solve problems of this shape at industrial scale.

The compiler inherits that solved-problem-ness at stage 3, *conditional on* a workable PDDL encoding of story-events and world-state (OQ1 + OQ3 below).

### CS4 — Two-level budget feasibility

Two constraints interact at compile time:

- **Dramatica minimum**: the dialect's claim (specified in Dramatica's quad-storymind requirement) that **the story argument requires at least N beats to fully express**. `N` is dialect-dependent and varies with the encoding's specific throughline structure. Approximate range from Dramatica theory: ~32–48 beats for a full 4-throughline story.
- **Word budget**: the requested total word count for the output prose.

Compatibility condition:
```
N_dramatica_minimum × W_min_per_beat  ≤  word_budget
```
where `W_min_per_beat` is a dialect-imposed floor on per-beat prose (empirically ~200 words; probably OQ-able).

**Infeasibility if the product exceeds the budget.** The compiler stops at stage 2, emits an error naming the conflict, and offers relaxation suggestions: increase word budget, drop Dramatica-completeness (fall to Aristotelian-only for a shorter story), or relax the minimum-beat count via a simpler throughline structure.

**This feasibility check runs BEFORE the planner.** A simpler constraint-propagation pass catches infeasibility cheaply; no planner effort wasted on impossible requests.

### CS5 — LLM is a ranker, not a generator

The compiler's stage-3 output is a **solution space** — many valid substrate sequences (multiple topological orderings; multiple event-selection parameterizations; multiple valid precondition-gap-filling sequences). Stage 4 selects one.

Architectural commitment: the LLM selects; the LLM does not generate. Specifically:
- The LLM **never emits substrate events directly**. Every event it touches came out of the planner.
- The LLM **never mutates the solution space**. It picks from what stage 3 provided.
- The LLM's output is a **ranking function**, optionally normalized to a single top-1 selection.

Consequences:
- The compiler is **independently testable without any LLM**. Stage 3 produces the solution space deterministically; any ranker (including a uniform-random RNG) produces a valid output.
- The LLM's task is **discriminative**, not generative. Picking best-of-N is easier than authoring from scratch. Smaller capability ask than LLM-as-author.
- The ranker is **swappable**. Uniform-random for structural tests. Heuristic-scored for deterministic baseline. LLM-scored for production.

CS5 also separates this compiler concretely from LLM-as-author systems like Façade's drama manager — the drama manager *selects and composes* but operates over a larger design space. CS5's ranker is strictly narrower: pick-from-candidates, no compose.

### CS6 — Conflicting constraints are compiler errors

No silent fallback. No "close enough." No "we'll just make it work."

When the constraint system is **infeasible** — at any of the four stages — the compiler halts with a **structured error** specifying:
- Which constraints participate in the conflict.
- At which pipeline stage the infeasibility was detected (stage 2 arithmetic; stage 3 planning; stage 4 no-valid-candidates).
- Minimally-sufficient relaxations when computable (e.g., "increase word_budget by ≥ X" or "drop peripeteia_event_id pinning").

**This is the expert-system posture concretely.** The user's framing (`project_expert_system_goal.md`) says the system's job is to be **unforgiving** — to force humans and LLMs to do their homework. Compiler errors on constraint conflicts *are* that posture at the substrate-generation boundary. The author is forced to relax a constraint or accept that no story exists that satisfies them all. The compiler refuses to paper over the conflict.

CS6 also distinguishes this compiler from LLM-based story generators that quietly drop constraints when they conflict. The compiler fails loudly; the LLM-as-author fails quietly. The former is debuggable; the latter is not. The user's architecture makes this tradeoff explicitly, and CS6 is the commitment it rests on.

### CS7 — Cross-check by existing verifiers

The compiler's output is a substrate sequence + Lowering records. **Existing tools already verify this shape exactly**:

- **Tier-1 shape validation** (JSON Schema 2020-12 on substrate + Lowering + dialect records). Conformance test runs this battery. Covers record-level shape only.
- **Tier-2 audits** (referential integrity, aristotelian-event-refs, character-ref-ids, branch-label-consistency, save-the-cat-intra-story, CrossDialectRef). Covers cross-record structural integrity.
- **Dialect verifiers** (A7.1..A7.11 for Aristotelian; analogous check families for other dialects). Covers dialect-specific semantic correctness.

**The compiled substrate must re-verify under the dialect it was compiled FROM.** If the compiler claims "I produced a substrate satisfying these Aristotelian constraints" and `aristotelian.verify()` then emits observations on the output, the compiler has a bug.

This is the **compiler's type-check** in classical-compilation terminology. The back-end emits IR; the IR verifier confirms well-formedness. Here:
- Compiler back-end = the four-stage pipeline.
- IR = substrate + Lowering records.
- IR verifier = the existing tier-1 + tier-2 + dialect-verifier stack.

CS7 is a load-bearing **cost-saving architectural decision**: the project does not need to build a compiler-validation stack. It already has one. The compiler inherits the entire verification stack as its test harness.

## Open questions — banked for per-stage follow-on sketches

### OQ1 — State representation granularity

STRIPS state is propositional (a bag of atoms). Stories need richer state:

- **Epistemic** (who knows what): partially captured by substrate `Held` records. May need extension.
- **Affective** (who feels what): not captured at substrate layer; may live at dialect layer (Aristotelian hamartia; Dramatica relationship stories) or require substrate extension.
- **Relational** (alliance, suspicion, trust): substrate-adjacent but not typed. Character-to-character state over τ_s.

**Forcing function:** first stage-3 planner implementation attempts to satisfy a concrete scene's preconditions. If propositional state can't express "Hamlet believes Claudius is behind the arras," the representation is too thin. If it can, no extension needed yet.

### OQ2 — Candidate enumeration strategy for stage 4

The solution space from stage 3 can be large. Three strategies for getting finite candidates to the ranker:

- **RNG-sample then rank.** Cheap; may miss high-impact outliers.
- **Heuristic pre-filter to top-k.** Requires heuristic; k determines ranker cost.
- **Iterative refinement.** LLM proposes direction; compiler verifies; LLM refines. Expensive; hardest to test.

**Forcing function:** first stage-4 implementation attempts to rank for a concrete corpus encoding. If the valid space is small enough to enumerate exhaustively, OQ2 closes trivially. If not, the strategy choice becomes consequential.

### OQ3 — Planner choice

Three candidate directions:

- **PDDL + off-the-shelf (FastDownward or descendant).** Industrial strength; needs PDDL encoding of story-events + world-state. Interop via STDIN/STDOUT subprocess.
- **POCL custom.** Partial-order causal link planner, implemented in-tree. Closer to story-structure semantics (partial-order output is natural). Requires implementation.
- **Constraint logic programming / Answer Set Programming (Clingo / DLV).** Declarative; good for soft constraints + preference specification. Interop via subprocess.

**Forcing function:** attempt stage-3 implementation on a concrete corpus encoding (likely Oedipus — smallest complete Aristotelian encoding) and measure fit between the encoding's structure and each candidate's native model. Python-as-spec discipline (`feedback_python_as_spec.md`) suggests a Python-first POCL that can later port to a production language.

### OQ4 — Impact objective for the ranker

What does "max emotional impact per word" mean computationally? Options:

- **(a) LLM scores candidates on a rubric** (cliffhangers at phase boundaries; rising tension within phase; peripeteia placement; catharsis weight distribution; hamartia proximity to peripeteia).
- **(b) Heuristic scoring from dialect fields** (peripeteia near middle-end; catharsis concentration in end phase; phase-weight balance matches dialect; binding distance under some rule).
- **(c) Human-preference learning** from a labeled corpus.

**Forcing function:** first stage-4 implementation needs an objective; the choice above determines the ranker's shape and test harness. (c) requires a labeled corpus which we don't have. (a) is fast but opaque. (b) is slow to tune but debuggable.

### OQ5 — Hard vs soft constraint discipline

Dialect structural fields (`peripeteia_event_id`) are hard — they point at specific events; compiler must honor them exactly. Hint-level constraints ("early-middle") are soft — admit multiple satisfying substrates with different costs.

Two architectural postures:
- **All-hard preprocessing.** Soft hints compile to hard constraints via rules ("early-middle" → τ_s in [phase_middle_start, phase_middle_start + N]). Simpler planner; loses graceful degradation.
- **Mixed.** Hard for pinning; soft for hints; planner respects hard and minimizes hint-relaxation cost. Richer behavior; harder to implement.

**Forcing function:** first user-facing hint-input attempt (not in scope for stage-3 alone). Banked until the author-facing input layer (markdown-fenced parser, roadmap item 1) creates concrete soft-constraint pressure.

### OQ6 — Integration with existing encoding modules

The current Python encoding modules (`hamlet.py`, `hamlet_aristotelian.py`, etc.) hand-author substrate + dialect together. The compiler inverts this: dialect in, substrate out. Integration questions:

- Do existing encoding modules become **test fixtures** (dialect inputs; substrate expected-outputs)?
- Or do they become **specifications** (dialect constraints; substrate is regenerated each compile)?
- Is there a migration path that preserves the current substrate authorings while adding compiler-generated cases?

**Forcing function:** first compiler-to-corpus integration (post-stage-4). Likely surfaces tension between hand-authored substrate's specific prose-shaped events and compiler-output's generic-template events. May force substrate extensions or compilation-surface refinements.

## The "falling out" observation

The `project_solution_horizon.md` memory (stated 2026-04-20) anticipated a future more-capable AI recognizing a compiler form in this repo, with the solution "falling out" as a side effect. This sketch commits the first concrete articulation of that compiler shape.

Honest reading:

- **Yes, this is a shape that can "fall out."** The four-stage pipeline is concrete; each stage maps to a solved-problem domain (STRIPS/PDDL for stage 3; arithmetic for stage 2; PCG + LLM-ranker patterns for stage 4); the cross-check is provided by existing verifier infrastructure (CS7). Stage 1 is straightforward dialect-walk. Nothing magical is required per stage.

- **No, the naming is not the implementation.** Stages 1–4 represent multi-sketch, multi-session work. State representation (OQ1) is a genuine open research question. Impact objective (OQ4) is another. The implementation of stage 3 alone is several sketches of work. The compiler's end-to-end shape is named; execution remains.

- **The combination is the contribution.** Prior story-generation systems (Tale-Spin, Mexica, Minstrel, Façade) composed subsets of these primitives — Mexica's engagement/reflection cycle is adjacent to stage 4; Tale-Spin's goal-satisfaction is adjacent to stage 3; Façade's drama-management is adjacent to ranker selection. None composed all four stages with this architectural separation (deterministic compiler producing solution space; LLM confined to stage 4 ranking; existing verifier infrastructure as type-check).

Per the solution-horizon memory's dual-axis framing (solve if we can; otherwise produce strong inputs for a future AI): this sketch is a **strong input either way**. If this engine implements the four stages, it solves the forward compilation problem. If a future more-capable AI does it instead, it inherits the named shape + the mapped solved problems + the existing verifier stack as type-check — a much tighter problem statement than "build a story engine."

The "falling out" is not *implementation*. The "falling out" is **reduction to solved problems + named architectural separation + reusable type-check**. This sketch captures that reduction. The user correctly identified this moment.

## Commitment summary

CS1..CS7 commit to:
- Compilation problem statement (input / output / infeasibility).
- Four-stage pipeline decomposition.
- STRIPS-shape logistical constraints at stage 3.
- Two-level budget feasibility at stage 2.
- LLM-as-ranker-not-generator at stage 4.
- Infeasibility-is-loud discipline at every stage.
- Cross-check via existing verifier stack as type-check.

## Non-commitments

Out of this sketch, banked per stage:
- Specific planner (OQ3).
- State representation granularity (OQ1).
- Candidate enumeration strategy (OQ2).
- Impact objective (OQ4).
- Hard vs soft constraint discipline (OQ5).
- Integration with existing encoding modules (OQ6).
- Implementation timeline.
- Prose generation (entirely separate problem per user 2026-04-21; not this compiler's concern).
- Author input layer (markdown-fenced parser is a separate roadmap item upstream of this compiler).

## Next arcs (not commitments — candidates)

Each stage deserves its own sketch + implementation. Smallest-first:

- **Stage 2 (feasibility check) — smallest.** Arithmetic + constraint propagation on Dramatica-minimum-beats × min-words-per-beat vs word budget. Does not require stage 1 to be complete (hand-wired dialect constraint inputs suffice). Likely first concrete implementation.
- **Stage 1 (constraint extraction).** Walk the existing Aristotelian encoding modules (oedipus / rashomon / macbeth / hamlet) and emit constraint-graph records. Simple dialect walk; incremental.
- **Stage 3 (planner) — largest.** Multi-sketch arc. OQ1 + OQ3 + OQ5 all bind here. Likely starts with POCL-in-Python for Oedipus's tiny state space.
- **Stage 4 (enumerator + ranker).** OQ2 + OQ4 bind here. Lowest risk if stage 3's solution-space size stays small at first; if so, exhaustive enumeration + heuristic ranker is adequate.

Alternation (per `feedback_research_production_alternation.md`): each stage's first sketch is design-first + impl pair; probes between stages are research-track ("does stage 2 produce the error we expect when constraint sets conflict?").

## What a cold-start Claude should read first

1. This sketch (`compilation-sketch-01.md`) — the compiler-backend shape and its architectural commitments.
2. [state-of-play-12](state-of-play-12.md) — current corpus, tooling-frame, cross-check infrastructure.
3. [architecture-sketch-02](architecture-sketch-02.md) — the dialect-stack this compiler is a backend for.
4. [lowering-sketch-02](lowering-sketch-02.md) — the reverse-direction records the compiler's output includes.
5. `prototype/story_engine/core/aristotelian.py` — the largest dialect's verifier surface (the compiler's type-check for Aristotelian-compiled output).
6. `prototype/story_engine/encodings/oedipus_aristotelian.py` — smallest complete dialect-level encoding; candidate first corpus for stage-1 + stage-3 implementation.
7. `project_technical_target.md` (memory) — the compiler's objective function at the macro level (many-to-many mapping; max emotional impact per word; constrained randomness).
8. `project_solution_horizon.md` (memory) — the framing that motivates producing this sketch whether or not this engine implements the stages.
