# Compilation stage 2 (feasibility gate) — sketch 01

**Status:** draft, active
**Date:** 2026-04-21
**Supersedes:** nothing (new arc — first concrete compiler-stage implementation)
**Extends:** [compilation-sketch-01](compilation-sketch-01.md) — concretizes CS4 (two-level budget feasibility) + CS6 (infeasibility-is-loud) for the Aristotelian dialect
**Frames:** [aristotelian-sketch-04](aristotelian-sketch-04.md) — A15-SE1 phase event-count bounds are the first hard-constraint field to feed a real compiler gate
**Related:** `project_dialect_compilation_surface.md` (memory — the surface sketch-03 completed); `feedback_risk_first_sequencing.md` (memory — the PM discipline that motivates this spike); `feedback_llm_as_ranker.md` (memory — CS5 commitment stage-2 trivially preserves, since stage 2 has no LLM)
**Superseded by:** nothing yet

## Purpose

First concrete implementation of one of `compilation-sketch-01`'s four stages. Stage 2 — **feasibility gate** — is the smallest candidate: pure arithmetic + constraint-propagation, no planner, no LLM. Per CS4:

```
Σ_phases phase.min_event_count × W_min_per_event  ≤  word_budget
```

Infeasibility produces a structured error per CS6. Feasibility produces a structured success record with the implied word-count range for downstream use.

This sketch names the function shape, the arithmetic, the structured error type, the relaxation-suggestion discipline, and the scope. It does not commit to integration with stage 1 (constraint extraction) — the spike takes `ArMythos` directly, hand-wired-input style, per `compilation-sketch-01`'s explicit affordance: *"Stage 2 can be tested with hand-wired dialect constraint inputs."*

## Why now

Per `feedback_risk_first_sequencing.md` (saved 2026-04-21): the biggest unretired risk on the project is the compiler itself — the four stages of `compilation-sketch-01` have architectural commitments but no implementation. The dialect-compilation surface (A15/A16 + S14/S15) is built, schema-landed, and exercised on worked examples across two dialects; the next risk-reduction move is to make one compiler stage *functional*.

Stage 2 is the correct first move because:

1. **Smallest scope.** Pure arithmetic. No STRIPS representation (OQ1), no planner choice (OQ3), no ranker objective (OQ4), no candidate enumeration (OQ2). The sketch can close with one function + tests.
2. **Gate posture.** Stage 2 fails loudly before the planner runs. A working stage 2 is immediately useful — an encoding can ask "is my A15-SE1 authoring feasible at this budget?" without any other compiler stage existing.
3. **A15-SE1 surface is ready.** The `phase.min_event_count` / `max_event_count` fields landed 2026-04-21 across Python + Tier-1 schemas. Stage 2 is the first component that *consumes* them for a purpose beyond verification.
4. **CS6 discipline lands concretely.** The first structured `InfeasibilityError` is here. Future stages 1 / 3 / 4 inherit the error shape.
5. **No LLM or external planner.** Implementable today. Deterministic. Testable without external dependencies.

User directive in-conversation: *"let's try to spike it...risk-first....let's lean that way. We can return to the research stuff after we have a functional spike."*

## Scope — what this sketch does and doesn't do

**In scope:**

- A single-function API for stage-2 feasibility (S2F1).
- CS4 arithmetic on Aristotelian A15-SE1 fields: lower-bound word floor from Σ `phase.min_event_count` × `W_min_per_event` (S2F2).
- Current-authoring cardinality gate: `len(central_event_ids)` within `[Σ min, Σ max]` when bounds active (S2F3).
- Structured success/failure result type with feasible ranges and conflicting-constraint lists (S2F4).
- Minimally-sufficient relaxation suggestions per CS6 (S2F5).
- Aristotelian-only scope; STC and Dramatica deferred (S2F6).
- Python implementation + tests as a follow-on commit to this sketch.
- Worked example: Hamlet authored with A15-SE1 values at `ar_hamlet_beginning/middle/end = min 10/8/6` → total min 24 events. At `W_min_per_event = 200`, budget floor is 4,800 words.

**Out of scope:**

- Stage 1 (constraint extraction from raw dialect records into an intermediate constraint graph). Hand-wired `ArMythos` inputs only.
- Stage 3 (STRIPS planner). Stage-2 feasibility is the gate *before* the planner; planner logic lives elsewhere.
- Stage 4 (ranker). Same.
- STC S14-SE1 (page-tolerance) feasibility. Defer to sketch-02 or a separate STC-specific extension.
- Dramatica-minimum-beats feasibility. Dramatica-template is not DCS-instantiated yet; no authored `min_event_count` analog.
- Co-presence feasibility (A15-SE2). Requires substrate location state (DOQ-AR4-1) or STRIPS preconditions (CS3). Stage-2 arithmetic does not cover it.
- Audience-knowledge feasibility (A15-SE3). Same reason as co-presence.
- Integration with existing verifier framework. Stage 2 returns its own result type; not an `ArObservation`. Distinct machinery.
- Author-facing CLI / markdown-parsing entry point.
- Word-budget *upper* bound. Large budgets are always feasible (prose can be longer per event); only floors gate.
- Migration of pre-sketch-04 encodings to author `min_event_count` bounds. Feasibility on those encodings uses authored `len(central_event_ids)` alone when bounds stay at default 0.

## Commitments

Labels **S2F1..S2F6** commit to structural shape; **S2F-OQ1..S2F-OQ5** bank open questions with forcing criteria.

### S2F1 — Stage-2 feasibility is a single synchronous function

```python
def stage_2_feasibility(
    mythos: ArMythos,
    *,
    word_budget: int,
    W_min_per_event: int = 200,
) -> FeasibilityResult:
    ...
```

**Posture.** Gate, not observation pass. Returns a `FeasibilityResult` with an `is_feasible: bool` discriminator. Never raises on infeasibility — CS6's "loud" is *structured*, not exceptional. Exceptions are reserved for malformed inputs (e.g., `word_budget < 0`).

**Determinism.** Given identical inputs, identical outputs. No I/O, no randomness, no LLM. Consistent with CS1's function-not-interactive-process architectural posture.

**No stateful compiler object.** A function call is sufficient at this stage. Future stages may grow a `Compiler` class if stage-1-to-stage-4 state-passing demands it; for now the function is enough.

### S2F2 — CS4 budget-floor arithmetic

For each `ArPhase` in `mythos.phases`:

- If `phase.min_event_count > 0`: contributes `phase.min_event_count` to the aggregate minimum.
- If `phase.min_event_count == 0`: contributes `len(phase.scope_event_ids)` to the aggregate minimum. (Interpretation: "what's currently authored is the floor; the encoding hasn't declared a looser minimum.")

```
aggregate_min_events = Σ_phases max(phase.min_event_count, len(phase.scope_event_ids) if bound==0 else phase.min_event_count)
min_word_floor = aggregate_min_events × W_min_per_event
feasibility_gate = (word_budget ≥ min_word_floor)
```

**Semantics of the fallback.** When bounds are unset (default 0), the encoding's `len(central_event_ids)` is the de-facto floor. This is conservative: the compiler can't emit *fewer* events than are already authored (stage 3 may only add intermediate events, not remove authored ones). Once an encoding grows A15-SE1 bounds, the bound wins.

**Why aggregate across phases.** Each phase's word budget is not independent — stage 3 (planner) may distribute total events across phases however the constraints allow. The arithmetic gate is at mythos scope, not per-phase.

### S2F3 — Current-authoring cardinality gate

Orthogonal to the budget check: when A15-SE1 bounds are active on a phase, `len(phase.scope_event_ids)` must fall within `[min_event_count, max_event_count]`. This is already enforced by Tier-2 audit A7.12 — but stage 2's perspective is distinct: A7.12 checks whether the *current encoding* is consistent with its own declared bounds; stage 2's question is whether the bounds plus the current authoring imply something the *compiler* can satisfy.

For the spike, S2F3 delegates to A7.12 semantics: if A7.12 would fire on the authored mythos, stage 2 reports the same conflict under its own error codes. This produces a useful double-signal: Tier-2 says "encoding is inconsistent"; stage 2 says "therefore compilation is infeasible." Same root cause, two vantage points.

### S2F4 — Structured result type

```python
@dataclass(frozen=True)
class InfeasibilityError:
    code: str                              # e.g., "budget_below_floor"
    conflicting_constraints: Tuple[str, ...]  # readable names
    message: str                           # prose description
    relaxations: Tuple[str, ...]           # S2F5

@dataclass(frozen=True)
class FeasibilityResult:
    is_feasible: bool
    aggregate_min_events: int              # Σ from S2F2
    aggregate_max_events: int              # Σ from phase.max_event_count; 0 = unbounded
    min_word_floor: int                    # aggregate_min_events × W_min_per_event
    word_budget: int                       # echoed input
    W_min_per_event: int                   # echoed input
    errors: Tuple[InfeasibilityError, ...] # empty when feasible
```

Consuming code interacts via `result.is_feasible` (truthy check) plus `result.errors` (walk for structured diagnostics). Echoing inputs lets a caller present the full arithmetic picture without recomputing.

**Why not use the existing `ArObservation` type?** Intentional architectural separation. Observations live in the verification layer (severity-graded advice). `InfeasibilityError` lives in the compiler layer (gate decisions). They share the shape "target + code + message" but serve different workflows; conflating them would invite future confusion about whether a compiler error is "just an observation."

### S2F5 — Relaxation-suggestion discipline

Per CS6: "minimally-sufficient relaxations when computable." For the spike, stage 2 computes relaxations for the budget-floor error only (the other error codes are consistency gates whose "relaxation" is "fix the encoding," which is trivially stateable but not mechanically computed).

Budget-floor relaxations:

1. **Increase word_budget.** `relaxation = f"increase word_budget by ≥ {min_word_floor - word_budget} words"`
2. **Reduce aggregate_min_events.** `relaxation = f"reduce aggregate phase.min_event_count by ≥ {ceil((min_word_floor - word_budget) / W_min_per_event)} events across all phases"` — this is the integer deficit in event-count terms.

Both are emitted when applicable. Authors pick the relaxation that fits their authorial intent.

**Not in the spike:** per-phase relaxation allocation ("reduce phase_X by N, phase_Y by M"). The spike reports the aggregate deficit; per-phase allocation is a refinement for when multiple feasible relaxation shapes need presenting.

### S2F6 — Aristotelian-only scope

This sketch applies to Aristotelian mythoi only. Extensions are explicitly deferred:

- **STC extension.** S14-SE1 page-tolerance is positional, not cardinality-based. A STC-specific arithmetic gate would calculate `Σ StcBeat(page_actual + page_tolerance_before...page_actual + page_tolerance_after) ≤ page_count_cap` — different arithmetic. Defer to `compilation-stage-2-sketch-02` or an extension sketch.
- **Dramatica extension.** Dramatica-template does not currently have a DCS-instantiated surface (S14-analog). Dramatica-minimum-beats referenced in CS4 is an authorial claim about throughline structure; mapping it to a per-mythos arithmetic gate requires Dramatica's DCS instantiation first.

The discipline is: each dialect's stage-2 arithmetic is dialect-local (mirrors DCS5's dialect-locality default for flavor taxonomies). If patterns converge across dialects, a sketch-02 can abstract them. If they stay local, each dialect gets its own stage-2 function.

## Worked example — Hamlet under stage-2

Hamlet's sketch-04 authoring:

| Phase | min_event_count | max_event_count | len(scope_event_ids) |
|---|---|---|---|
| beginning | 10 | 15 | 13 |
| middle | 8 | 14 | 11 |
| end | 6 | 10 | 8 |
| **Σ** | **24** | **39** | **32** |

At `W_min_per_event = 200`:
- `aggregate_min_events = 24`
- `min_word_floor = 24 × 200 = 4,800`

Feasibility outcomes:
- `word_budget = 4,800` → feasible (tight; no slack).
- `word_budget = 10,000` → feasible (5,200 words of slack above floor).
- `word_budget = 3,000` → **infeasible, budget_below_floor.**
  - Relaxations: "increase word_budget by ≥ 1,800 words" OR "reduce aggregate phase.min_event_count by ≥ 9 events across all phases."
- `word_budget = 4,799` → infeasible by 1 word. Relaxations: "increase word_budget by ≥ 1" OR "reduce aggregate phase.min_event_count by ≥ 1 event."

Current-authoring gate: Hamlet's `len(central_event_ids) = 32` falls within `[24, 39]`. No S2F3 error.

## Pre-sketch-04 corpus feasibility (Oedipus / Rashomon / Macbeth / Ackroyd)

Pre-sketch-04 Aristotelian encodings have `phase.min_event_count = 0` (default). The S2F2 fallback (use `len(phase.scope_event_ids)` as floor) still yields a meaningful gate:

| Encoding | Authored events | min_word_floor @ W=200 |
|---|---|---|
| Oedipus | 23 (8+9+6) | 4,600 |
| Rashomon | ~25 | ~5,000 |
| Macbeth (aristotelian) | ~28 | ~5,600 |
| Hamlet | 32 | 6,400 |

Expected test: each pre-sketch-04 encoding passes stage-2 feasibility at `word_budget = 10,000`. Each fails at `word_budget = 1,000`. Corpus sanity is a bounded sweep.

## Open questions — banked for follow-on stage-2 work

### S2F-OQ1 — `W_min_per_event` default

The `compilation-sketch-01` CS4 text quotes "empirically ~200 words; probably OQ-able." The spike picks 200 as a working default. Real ranges:

- Cinematic beat (Save the Cat, ~110-page screenplay): conventional page ≈ 250 words; beats span 1–15 pages → 250–3,750 words/beat. Mean ≈ 1,200. **Much more than 200.**
- Aristotelian substrate event (prose fiction): single "incident" may be 100–2,000 words depending on density. 200 is a conservative lower bound.
- Short-form / flash fiction: 50–200 words/event plausible.

**Forcing function:** first corpus-scale feasibility run against real target word budgets. If the 200 default produces nonsense gates (e.g., long-form novel encodings pass trivially), the value needs per-encoding or per-form override. Banked; 200 is a starting reference, not a commitment.

### S2F-OQ2 — `W_max_per_event` ceiling

The spike has no word-budget *upper* bound. A pathologically large budget trivially passes stage 2 (the arithmetic is one-sided). Is that correct? Two positions:

- **Yes, one-sided is right.** Stage 2 gates feasibility of *being able to produce* the story; a large budget is always feasible at the arithmetic layer. Prose-density questions are downstream (stage 4 ranker may prefer denser per-event prose; still not a stage-2 concern).
- **No, a ceiling matters.** If `word_budget > aggregate_max_events × W_max_per_event`, the compiler will produce an over-dense result (stage 3 can't emit more events than A15-SE1 ceilings allow). Stage 2 could surface this as an advisory — not an infeasibility, but a "your budget exceeds the encoding's capacity" signal.

**Forcing function:** first author ships a word budget that trivially exceeds the encoding's natural capacity. Banked; spike does not emit the advisory.

### S2F-OQ3 — Extension to STC S14-SE1

STC's page-tolerance arithmetic differs from Aristotelian's count arithmetic. A cross-dialect stage-2 could either:

- **Unified gate.** Abstract "positional/cardinality constraints with an arithmetic relation to word budget"; map each dialect's fields to the abstraction.
- **Dialect-local gates.** `aristotelian_stage_2_feasibility()` and `stc_stage_2_feasibility()` as parallel functions; dispatch at callers.

**Forcing function:** first STC-shaped feasibility test attempt. Depends partly on DOQ2 globalization (`project_doq2_judgment.md`): if co-presence and tonal_register globalize across dialects but cardinality stays local, unification at the stage-2 layer becomes principled. Banked until STC stage-2 implementation is attempted.

### S2F-OQ4 — Extension to Dramatica throughline-minimum-beats

Dramatica-template doesn't currently have a DCS surface. Dramatica-minimum-beats (the CS4 reference) lives in Dramatica theory, not in the encoded Dramatica-template records. Three paths:

- **Dramatica DCS instantiation first.** Grow Dramatica's own S14-SE1 equivalent. Stage-2 extension follows from the field.
- **Dramatica-theory-hardcoded constants.** The compiler hard-codes "a full 4-throughline story requires ≥ 32 beats"; stage 2 applies it to any Dramatica-declared encoding. Simpler; less principled.
- **Author-declared per-encoding.** Each Dramatica encoding declares its own minimum-beats; stage 2 reads it. Matches the A15-SE1 per-encoding pattern.

**Forcing function:** first Dramatica compilation attempt. Banked pending Dramatica-template DCS instantiation (which would be a separate research-production arc).

### S2F-OQ5 — Integration with stage 1 (constraint extraction)

The spike hand-wires `ArMythos` → `stage_2_feasibility`. Eventually stage 1 will emit a normalized constraint graph that stage 2 consumes. Does the stage-1 output *superset* the `ArMythos` fields stage-2 uses, or does stage-2's arithmetic need dialect-specific structure stage-1 flattens out?

Two hypotheses:

- **Superset.** Stage 1's constraint graph preserves A15-SE1 bounds as named per-phase constraints; stage 2 reads them by name. Clean abstraction.
- **Loss.** Stage 1 loses per-phase structure in flattening (e.g., emits only "aggregate_min = 24" without per-phase attribution); stage 2's relaxation suggestions become less targeted.

**Forcing function:** first stage-1 implementation sketch. Banked.

## Relationship to prior commitments

| Prior | Refined / concretized by stage-2 sketch | How |
|---|---|---|
| `compilation-sketch-01` CS1 | Partially instantiated | Stage-2-function shape (input/output/error) concrete for one stage |
| `compilation-sketch-01` CS4 | Fully instantiated for Aristotelian | Budget-floor arithmetic named and implemented |
| `compilation-sketch-01` CS5 | Trivially preserved | Stage 2 has no LLM; no ranker concern |
| `compilation-sketch-01` CS6 | First concrete instantiation | `InfeasibilityError` type + relaxation-suggestion discipline |
| `compilation-sketch-01` CS7 | Not engaged | Stage 2 emits no substrate; verifier cross-check applies only downstream |
| `compilation-sketch-01` OQ2 / OQ3 / OQ4 | Unaffected | Stage 2 does not touch planner, ranker, or candidate enumeration |
| `aristotelian-sketch-04` A15-SE1 | First use as compiler input | `phase.min_event_count` / `max_event_count` feed the gate |
| `aristotelian-sketch-04` A15-SE2 / A15-SE3 | Explicitly deferred | Require stage 3 / substrate machinery |
| `aristotelian-sketch-04` A16-* | Not engaged | Soft preferences belong to stage 4 |
| `feedback_risk_first_sequencing.md` | Acted on | First compiler-risk-reduction move |

## Implementation brief

Concrete changes, in order:

1. **Module.** `prototype/story_engine/core/compiler.py` — new single-file module. Houses `FeasibilityResult`, `InfeasibilityError`, and `stage_2_feasibility()` at module scope. Future stages can be added to the same module (or the module can promote to a `compiler/` package) without breaking the public API.
2. **Tests.** `prototype/tests/test_compiler_stage_2.py` — new test module following the `test_save_the_cat.py` pattern (synthetic-fixture tests + integration pins against real encodings). Coverage:
   - Feasible cases: Hamlet at generous budget; Oedipus at default-600-words-per-event generous budget; all pre-sketch-04 Aristotelian corpus at W=10,000.
   - Infeasible cases: Hamlet at 3,000 (below floor); synthetic mythos with conflicting bounds (min > max) surfacing S2F3.
   - Error code pins: at least one test per emitted `InfeasibilityError.code`.
   - Relaxation pins: feasibility-failure cases assert the computed relaxation strings.
3. **Test registration.** New test module added to the prototype README's run list.
4. **No changes to existing modules.** Stage 2 is read-only on `ArMythos` / `ArPhase` dataclasses. No schema changes. No verifier changes. No encoding changes.

Expected test count: ~15–20 synthetic tests + 4 corpus-sanity integration pins ≈ 20 new tests total. Full suite: ~898 (from 878).

## What a cold-start Claude should read first

1. `compilation-sketch-01.md` — CS4 + CS6 are the architectural commitments this sketch concretizes.
2. `aristotelian-sketch-04.md` — A15-SE1 fields (the compiler's first hard-constraint input).
3. This sketch.
4. `prototype/story_engine/core/aristotelian.py` — `ArMythos` / `ArPhase` dataclasses (stage 2's input type).
5. `prototype/story_engine/encodings/hamlet_aristotelian.py` — the worked-example payload.
6. `feedback_risk_first_sequencing.md` (memory) — the PM discipline that motivated the spike order.

## Honest framing

This is the project's first compiler-stage implementation. The arithmetic is simple by design — stage 2 is the smallest of the four and doing it first lets the *harder* work (stage 3 STRIPS, stage 4 ranker) start from a position where the scaffolding exists (error types, result shapes, test patterns, dialect-to-compiler call conventions).

The spike deliberately does *less* than full CS4. It covers Aristotelian only, covers only the arithmetic gate (no co-presence / audience-knowledge feasibility), and hand-wires stage-1 inputs. This is not scope creep into a Dramatica-complete story-generator. It is the minimum viable first compiler-stage implementation that produces a functional artifact — one the user can invoke, get a loud feasibility verdict, and build downstream stages against.

The expert-system posture (`project_expert_system_goal.md`) lands concretely for the first time at compile scope: the compiler will tell you, loudly and structurally, that your encoding × budget combination can't produce the story you want. No papering over. Relaxations on offer. Authorial choice preserved. The compiler enforces; the author decides.

Per `project_solution_horizon.md`: stage 2 is a **strong input either way.** If this engine implements stages 1 / 3 / 4, stage 2 is load-bearing infrastructure. If a future more-capable AI does them instead, stage 2 is a concrete pattern for how a compiler stage *shaped this way* reads a dialect, emits a structured error, and composes with its neighbors — less abstract than the four-stage-pipeline naming alone.
