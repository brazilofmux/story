# Compilation stage 3 (planner spike) — sketch 04 (precondition-risk sort)

**Status:** draft, active
**Date:** 2026-05-22 (revised; first draft 2026-04-22)
**Supersedes:** nothing (new increment)
**Extends:** [compilation-stage-3-sketch-03](compilation-stage-3-sketch-03.md) — S3P1–S3P14 commitments unchanged
**Frames:** `compilation-sketch-01` CS3 (the planner stage); `feedback_risk_first_sequencing.md`
**Related:** `prototype/story_engine/core/compiler_stage_3.py` (the implementation this sketch hardens)
**Superseded by:** nothing yet

## Purpose

Close the largest remaining fragility in the current stage-3 planner: **precondition ordering in operator schemas affects plan quality (and in the limit, plan existence)**.

Sketch-03 surfaced the symptom concretely. When `defeat_by_riddle` lists its `at` preconditions before the `knows` precondition, the planner produces a valid but longer (5-step) plan in which the Oracle travels to Oedipus instead of Oedipus traveling to the Oracle. The 4-step "mythologically correct" plan was only found when the schema author manually put `knows` first (S3P14 ordering discipline).

This sketch makes precondition order a *planner concern* rather than a *schema-author concern*, so authors can list preconditions in whatever order reads naturally and still get the optimal plan.

## Revised framing (the path not taken)

The first draft of this sketch proposed a **minimal causal-link + threat-resolution layer** (demotion of threatening steps after a protected consumer). On implementation, that mechanism turned out to be analytically insufficient for the documented forcing case — see **Analytical finding** below. The actual mechanism is a one-pass **precondition-risk sort** inside `_plan_with_bindings`. The causal-link / threat-detection / demotion / promotion primitives still exist in the codebase as mathematically-correct scaffolding for future cases where they may become load-bearing, but they are inert in the current test corpus.

## Scope — what this sketch does and does not do

**In scope (S4P1–S4P5):**

- Sort the goal operator's grounded preconditions by a static "risk" key before iterating them in `_plan_with_bindings`. The key is the maximum `len(del_effects)` across operators whose `add_effects` can establish the precondition; tie-break by original schema order.
- Keep the threat-resolution primitives (`CausalLink`, `detect_threats`, `try_repair_by_demoting`, `try_repair_by_promoting`) in the module, mathematically correct, but not load-bearing.
- Thread sub-plan-local causal links through `_achieve` with proper offset re-indexing so that, when threats *do* arise, the link structure is coherent.
- Add a forcing test that constructs a `badly_ordered` copy of `DEFEAT_BY_RIDDLE` and passes it as the **goal operator** (not just as a library operator — see S4P5 below). Assert the 4-step optimal plan emerges.
- Keep the external API (`plan_to_goal`, `OperatorSchema`, `PlanningGoal`, emitted `Event` records) unchanged.
- Keep the output totally ordered (the spike still collapses any partial order to a total order for substrate emission).

**Out of scope (for this increment):**

- Full POCL with open preconditions, agenda, and flaw selection.
- Insertion-search (trying to place a sub-plan at multiple positions in the existing plan and picking the shortest). This is the next-level fix if the sort heuristic ever proves insufficient.
- Heuristic plan-length minimization beyond what the sort already provides ("first plan found" is still the search behavior; sort just changes which plan is found first).
- Removing the sketch-04 scaffolding primitives. They stay; their removal (or earned activation) is left for a later sketch with a concrete forcing scene.
- Any change to stage 1, 2, or 4.
- Richer state (still flat propositional).

## Commitments

### S4P1 — Precondition-risk sort (the principal mechanism)

In `_plan_with_bindings`, before iterating the goal operator's grounded preconditions, sort them by

```python
def _precondition_risk(p, operators) -> int:
    """Max len(del_effects) across operators whose add_effects unify with p."""
    ...
```

ascending, with original schema-order index as the tie-break. Iteration then proceeds in sorted order; the goal step is appended after all preconditions are satisfied.

The intuition: a precondition achievable by an operator that doesn't delete state (risk = 0, e.g. `learn_from`) is safe to satisfy first — its sub-plan can't undo state that later preconditions might depend on. A precondition achievable only by an operator that deletes state (risk ≥ 1, e.g. `travel` deleting `at(AGENT, FROM)`) is deferred. In the sphinx case this puts `knows` before the two `at` preconditions and lets Oedipus learn from the Oracle at Delphi before traveling on to the gates of Thebes.

This makes precondition ordering invisible to the schema author: the same plan emerges regardless of how the preconditions are listed in the schema.

### S4P2 — `CausalLink` record (scaffolding, currently inert)

A minimal internal record:

```python
@dataclass(frozen=True)
class CausalLink:
    establisher_idx: int    # index in the plan step list
    prop: Prop              # the precondition being protected
    consumer_idx: int       # index in the plan step list
```

Records are created in `_achieve` when an operator step is accepted as the establisher of one of its own preconditions, and propagated through recursive sub-plans with `offset`-based re-indexing.

This primitive is exercised by unit-level tests of the threat machinery but not by any whole-planner test in the current corpus.

### S4P3 — `detect_threats` helper (scaffolding, currently inert)

```python
def detect_threats(
    plan_steps, causal_links, candidate_step_idx, candidate_del_effects,
) -> list[tuple[CausalLink, int]]: ...
```

A del-effect threatens a link iff it unifies with the link's protected prop and the candidate step's position lies *strictly* after the establisher and *strictly* before the consumer in the total order being built. Returns `[]` for the entire current corpus (the precondition-risk sort prevents the threat configurations that would have populated this list).

### S4P4 — `try_repair_by_demoting` and `try_repair_by_promoting` (scaffolding, currently inert)

Two symmetric functions:

- **Demotion** moves a threatening step to the position immediately after the threatened link's consumer.
- **Promotion** moves it to the position immediately before the threatened link's establisher.

Both return `(repaired_steps, repaired_links)` on success or `None` on failure (no repair is possible, or the move creates a new threat). They are mathematically correct (covered by primitive-level checks) but never reached on any whole-planner path in the current test corpus.

These remain in the module because they are the natural primitives for the next increment if a forcing scene appears that S4P1 cannot handle — e.g., two preconditions of equal risk whose default schema order conflicts (the tie-break case where sort alone is undecided).

### S4P5 — Forcing test

`test_scene_3_bad_precondition_order_still_finds_optimal_plan` asserts that the planner returns the 4-step mythological plan when the **goal operator** lists its preconditions as `(at, at, alive, alive, knows)` — i.e., `knows` last.

A subtle requirement: the bad-ordered operator must be passed as `goal.operator`, not merely included in the operators tuple. `plan_to_goal` iterates `goal.operator.preconditions`, so only the goal's ordering exercises the bad-ordering path; an operator buried in the library is never reached by the goal-precondition iteration.

The pre-S4P1 planner returns a 5-step plan with the Oracle traveling to the gates of Thebes. The S4P1 planner returns a 4-step plan with Oedipus traveling through Delphi.

The existing "good order" tests continue to pass. The visited-guard counter for scene 3 remains at 67 firings (unchanged from sketch-03).

## Analytical finding: why threat resolution alone is insufficient

The original sketch-04 framing was that threat detection + demotion would convert the 5-step plan into the 4-step plan. It does not. The 5-step plan

```
0: travel(oedipus, corinth → delphi)
1: travel(oedipus, delphi → thebes_gates)
2: travel(oracle,  delphi → thebes_gates)
3: learn_from(oedipus, oracle, riddle_answer, thebes_gates)
4: defeat_by_riddle(oedipus, sphinx)
```

contains **zero detectable threats**:

- Step 1 deletes `at(oedipus, delphi)`. The only link protecting `at(oedipus, delphi)` runs from step 0 (establisher) to step 1 (consumer — step 1 itself needs it). The threat-detection condition `establisher < threatening < consumer` is strict, so step 1 cannot threaten the link to which it is the consumer.
- Step 2 deletes `at(oracle, delphi)`. No link protects `at(oracle, delphi)` because nothing in the plan needs `oracle` to remain at Delphi after step 3.
- Step 4 deletes `alive(sphinx)`. No link protects `alive(sphinx)` (only the goal step itself needs it).

The 4-step plan reaches its result by a *different sequence of variable bindings and operator choices*, not by rearranging the steps of the 5-step plan. No purely positional repair (demotion, promotion, or any other in-place swap) can transform one into the other.

This is why the actual fix is upstream: change the order in which preconditions are *attempted*, so the planner commits to bindings that don't paint itself into the corner step 1 paints itself into.

## Open questions

- **S4P-OQ1 (deferred):** When demotion and promotion are both applicable, which should we prefer? Moot at present (neither fires in the current corpus); revisit when a real forcing scene appears.
- **S4P-OQ2:** Should causal links be persisted on the final plan object returned to callers? Currently internal to the search; `Event.preconditions` already give downstream consumers enough information. Re-open if a stage-4 consumer needs the establisher relationships.
- **S4P-OQ3 (forcing scene landed; banked for the next increment):** When is the precondition-risk sort *insufficient*? The heuristic is overcautious — it takes the max `del_effects` across *all* operators that could achieve a precondition, even operators whose own preconditions are never satisfiable in the current state. **Forcing case:** add a `PHANTOM_VISION` operator to the sphinx scene 3 operator library. Vision achieves `knows(AGENT, FACT)` with three `del_effects` (three at-deletions) but requires `has(AGENT, FOCUS)` with `FOCUS` typed as `OBJECT_TYPE` — and scene 3's universe has no object-typed term, so the planner can never bind `FOCUS`. The phantom is unreachable in every state. Yet its mere presence in the library inflates `risk(knows)` from 0 to 3; the sort then orders preconditions as `alive×2 (0), at×2 (1), knows (3)` — i.e., `knows` last — and the planner regresses to the 5-step Oracle-travel plan that S4P1 thought it had retired. Test: `test_s4p_oq3_phantom_operator_inflates_risk_score_documenting_finding` pins both arms (4 steps without phantom, 5 steps with). The forcing case is **banked, not fixed** — the natural escalation is insertion-search (§Next steps) which sidesteps the risk heuristic entirely; the test's second assertion is written so it will fire (revealing the fix) when insertion-search or state-aware risk lands.
- **S4P-OQ4 (new):** Should the threat-resolution scaffolding (S4P2–S4P4) be removed if a follow-up sketch doesn't earn its use? Per AGENTS.md "no speculative generalization," removal is the default after one or two more increments without invocation. Promote/demote are easy to re-introduce when needed.

## Relationship to larger compiler

This increment keeps the spike's "Python-as-spec, no external solver" discipline. The sort is a one-line key function plus a sort call; the threat scaffolding is small, pure, and reviewable. When (not if) we later need a real POCL for more complex stories, the threat vocabulary (`CausalLink`, `threat`, `demote`, `promote`) is already there to be activated rather than introduced cold.

The sort is also a useful pedagogical artifact in its own right: it makes the connection between **operator-level del-effects** and **plan-level ordering** explicit, without committing to least-commitment partial orders.

## Next steps after this sketch lands

- If a forcing scene appears that the sort heuristic cannot handle (e.g., equal-risk preconditions whose order matters, or a case where the sort defers a precondition that, in this state, doesn't actually conflict), the next increment escalates to **insertion-search** in `_plan_with_bindings`: for each precondition, try satisfying it from each intermediate state of the existing plan and pick the position with the shortest sub-plan.
- If a forcing scene appears that *insertion-search* cannot handle either, the next increment activates the threat scaffolding (S4P2–S4P4) by threading links through `_plan_with_bindings` proper, allowing detect_threats / demote / promote to fire on cross-precondition link violations.
- Beyond that lies real POCL with open-precondition queues and flaw selection.

The next pressure on stage 3 will almost certainly come from richer epistemic or relational operators (S3P-OQ11), which are likely to create the tie-break configurations S4P-OQ3 anticipates.

---

**Status note for the series:** Sketches 01–03 proved the primitive works and can grow. Sketch 04 hardens precondition ordering so growth doesn't require heroic schema-authoring discipline. The mechanism that landed (a sort) was simpler than the one this sketch initially proposed (threat resolution); the threat-resolution work was not wasted — it generated the analytical finding that pointed at the simpler fix and left correct primitives in place for whenever they're earned.
