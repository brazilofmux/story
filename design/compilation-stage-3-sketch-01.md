# Compilation stage 3 (planner spike) — sketch 01

**Status:** draft, active
**Date:** 2026-04-21
**Supersedes:** nothing (new arc)
**Extends:** [compilation-sketch-01](compilation-sketch-01.md) — first spike of CS3 (STRIPS-shape logistical constraints); [compilation-stage-2-sketch-01](compilation-stage-2-sketch-01.md) — stage 2's CS6 structured-error pattern transfers to stage 3 intact
**Frames:** per `feedback_risk_first_sequencing.md`, stage 3 is the project-feasibility test — if this works on a small case, the thesis holds; if it doesn't, we learn what blocks it
**Related:** `substrate.py` (Event shape; Event.preconditions is already a first-class field); `oedipus.py` (the descriptive-only encoding the spike complements with a planner-ready fresh one); `project_solution_horizon.md` (the dual-axis framing under which a working spike is load-bearing either way); `feedback_python_as_spec.md` (commits this spike to Python-first POCL; no FastDownward subprocess)
**Superseded by:** nothing yet

## Purpose

Prove — or fail to prove — that `compilation-sketch-01`'s stage-3 commitment (CS3: "logistical constraints are STRIPS-style preconditions; compiler generates intermediate events to satisfy them") holds on a minimum-viable concrete test. The compiler's hardest promise in microcosm:

> Given: a start state (set of propositions) + a target event with explicit preconditions.
> Produce: a sequence of intermediate substrate events whose cumulative effects satisfy the target's preconditions, and then the target event itself; OR a structured infeasibility error naming why no such sequence exists.

The user's framing: *"this is really the test of whether the entire project is feasible."* If POCL-in-Python can close a precondition gap on one Oedipus event, the thesis is supported for a small concrete case. If it can't, we learn specifically what blocks it (state representation? operator encoding? planner choice?) — still valuable per `project_solution_horizon.md`.

This is a **spike**, deliberately scoped narrower than "stage 3 implemented." Scope differences from a full stage-3 are flagged in "Out of scope" below.

## Why now

Per `feedback_risk_first_sequencing.md` (2026-04-21): the compiler is the project's biggest unretired risk. Stage 2 landed 2026-04-21 as the first compiler spike (pure arithmetic; no STRIPS, no LLM). Stage 2 is necessary but not sufficient evidence — it's a gate, not a synthesis. Stage 3 is where synthesis lives.

Per `compilation-sketch-01`'s own sequencing: *"Stage 3 (planner) — largest. Multi-sketch arc. OQ1 + OQ3 + OQ5 all bind here."* This sketch does not claim to close the multi-sketch arc — only to land the first concrete spike that tests the CS3 claim on a bounded case. Follow-on sketches close OQ1 / OQ3 / OQ5 if they become pressing; the spike may force one or more of them if the spike's minimal commitments hit a wall.

User directive in-conversation: *"Let's proceed with the stage-3 spike."*

## Scope — what this sketch does and doesn't do

**In scope:**

- POCL-in-Python planner (S3P1). No FastDownward, no Clingo, no external subprocess.
- Propositional + typed state representation (S3P2). Predicate-and-args style, matching `substrate.Prop`.
- Two operator schemas for the spike (S3P3):
  - `travel(agent, from, to)` — representative of a general-purpose precondition-setup operator.
  - `kills(killer, victim)` — the target event; represents the class "authored dialect-pointed event whose preconditions may not be met."
- One Oedipus worked-example gap (S3P4):
  - Start state: Oedipus in Corinth (armed); Laius in Thebes.
  - Goal: `kills(oedipus, laius)` event with co-location preconditions.
  - Expected plan: two travel events + the kill event.
- Substrate `Event` emission (S3P5). The planner's output is a tuple of substrate `Event` records, not a novel record type. Stage 3 inherits substrate's authored event shape.
- CS6 structured-error posture (S3P6) when planning fails. Identical error type pattern to stage-2's `InfeasibilityError`.
- Scope-creep firewall (S3P7): no epistemic state, no temporal reasoning, no soft preferences, no ranker, no dialect integration, no multi-goal planning, no heuristic optimization, no plan-length minimization. Any of these becoming pressing is a post-spike follow-on sketch.

**Out of scope:**

- **Stage 1 integration.** The spike hand-wires start state + goal + operators. Eventually stage 1 extracts these from `ArMythos` + encoding modules; for the spike, they're Python literals inlined in the test module.
- **Stage 2 integration.** The spike does not call `stage_2_feasibility` first. Production stage 3 does; the spike decouples them to isolate the planner.
- **Stage 4 (ranker).** The spike returns the first valid plan the planner finds, not a ranked best-of-N. Candidate enumeration (compilation-sketch-01 OQ2) is a stage-4 concern.
- **Rich state (epistemic, affective, relational per compilation-sketch-01 OQ1).** Propositional + typed is the minimum. If the spike's target event needs more (e.g., "Oedipus believes Laius is a stranger"), OQ1 binds; we bank it.
- **Operator schema authoring convention.** The spike hardcodes two operators as Python dataclasses inline. Where operator schemas *should* live in the codebase (per-dialect? shared dialect-agnostic library? encoding-supplied?) is S3P-OQ3.
- **Full Oedipus plan.** The spike targets one precondition gap, not the full 16-event Oedipus. Manually STRIPS-encoding 16 events' worth of preconditions and effects is weeks of work; the spike is days.
- **Plan optimality.** The spike finds a valid plan; it does not minimize plan length, prefer semantically interesting intermediate events, or anything else ranker-adjacent.
- **Multi-branch substrate output.** The spike emits canonical-branch events only. Contested / draft branches are out.
- **Identity substitution at planning time.** The substrate's identity-substitution machinery is read-only at the planner; the planner treats `oedipus` and `the-crossroads-killer` as distinct if the spike's state doesn't assert `identity(oedipus, the-crossroads-killer)`. The spike avoids this case entirely.
- **Timeout or resource limits.** POCL on a 2-operator, 3-action problem is trivially fast. Real concerns (search-space blowup; timeouts) are production-stage-3 issues.
- **Integration with existing substrate verification.** The planner's output should verify under substrate structural audits (CS7), but the spike does not yet plug into the conformance-test suite — that's a follow-on.

## Commitments

Labels **S3P1..S3P7** commit to structural shape. **S3P-OQ1..S3P-OQ6** bank open questions with forcing functions.

### S3P1 — POCL-in-Python

Partial-Order Causal Link planner (Weld 1994 and descendants) implemented in Python. No external planning subprocess. Not PDDL; no full-fidelity STRIPS semantics required — the subset we need is:

- Actions have preconditions (propositions required to hold immediately before the action).
- Actions have effects (propositions asserted or retracted by the action).
- A plan is a totally-ordered (for the spike) sequence of actions from an initial state whose cumulative application satisfies the goal.

POCL's partial-order output shape (flexible ordering subject to causal-link constraints) is natural for story structure — multiple travel events can be concurrent in story-time if no causal dependency orders them. However, the spike emits a totally-ordered sequence because substrate `Event.τ_s` requires total ordering and the spike doesn't attempt to solve ordering-preference issues.

Rationale for POCL over forward-search or regression: POCL's output is a plan graph, which maps naturally onto substrate's partial causal structure (reader-model's unity-of-time interacts naturally with partial-order). For the spike, the partial-order structure is collapsed to a total order; but the choice leaves room for richer output as the spike evolves.

Per `feedback_python_as_spec.md`: the Python implementation is the spec. If the spike works, a future port to Rust/Go is cleaner than if we had started from FastDownward bindings.

### S3P2 — Propositional + typed state

World state is a set of `substrate.Prop` records (or equivalent — shape compatible with `Prop(predicate, args)`). Propositions are first-order atoms: predicate name + tuple of entity ids or primitive values. No negation in the state; "not P" is represented by P's absence from the set. No quantification.

```python
# Spike start state:
{
    Prop("at", ("oedipus", "corinth")),
    Prop("at", ("laius", "thebes")),
    Prop("has", ("oedipus", "sword")),
    Prop("path", ("corinth", "crossroads")),
    Prop("path", ("thebes", "crossroads")),
    Prop("alive", ("oedipus",)),
    Prop("alive", ("laius",)),
}
```

Typed in the sense that predicates have fixed arities and arg-kinds (entity / location / object), enforced at operator application, not at schema-definition-time (Python-is-spec; type-checking is runtime-assertion rather than static-schema).

**Limits acknowledged upfront:**
- No epistemic state ("Oedipus believes…"). If the spike's target event needs it, OQ1 fires.
- No temporal state ("at time τ"). Plan ordering is τ_s assignment, not reasoning-about-τ_s.
- No negation, no disjunction, no quantification. Plain atom-and-args.

### S3P3 — Two operator schemas for the spike

```python
@dataclass(frozen=True)
class OperatorSchema:
    name: str
    params: Tuple[str, ...]           # parameter names (by position)
    preconditions: Tuple[Proposition, ...]  # schematic props (args may be param refs)
    add_effects: Tuple[Proposition, ...]
    del_effects: Tuple[Proposition, ...]
```

Two operators for the spike:

```python
TRAVEL = OperatorSchema(
    name="travel",
    params=("agent", "from_loc", "to_loc"),
    preconditions=(
        ("at", ("agent", "from_loc")),
        ("path", ("from_loc", "to_loc")),
    ),
    add_effects=(
        ("at", ("agent", "to_loc")),
    ),
    del_effects=(
        ("at", ("agent", "from_loc")),
    ),
)

KILLS = OperatorSchema(
    name="kills",
    params=("killer", "victim"),
    preconditions=(
        ("at", ("killer", "LOC")),       # same-location binding via var
        ("at", ("victim", "LOC")),
        ("has", ("killer", "WEAPON")),
        ("alive", ("killer",)),
        ("alive", ("victim",)),
    ),
    add_effects=(
        ("dead", ("victim",)),
    ),
    del_effects=(
        ("alive", ("victim",)),
    ),
)
```

(Schematic syntax above is illustrative — the implementation uses Python-native structures.)

The `LOC` and `WEAPON` in `KILLS`'s preconditions are free variables the planner must bind. The planner's job: find bindings such that the preconditions unify with provable state after some action sequence. Classic unification.

**Why just two operators:** enough to prove the spike. Real stage 3 would have dozens (communicate, perceive, build, destroy, persuade, confront, reveal, conceal, etc.). The spike tests the *primitive mechanism*, not the operator library.

### S3P4 — One worked-example gap

Target event: `kills(oedipus, laius)`.

Start state (S3P2):
- Oedipus at Corinth, armed, alive.
- Laius at Thebes, alive.
- Paths: Corinth → crossroads; Thebes → crossroads.

Gap: to apply `KILLS`, the planner must bind `LOC = crossroads` and `WEAPON = sword`. The `at(killer, LOC)` and `at(victim, LOC)` preconditions are not satisfied in start state. The planner must produce:

1. `travel(oedipus, corinth, crossroads)` → satisfies `at(oedipus, crossroads)`.
2. `travel(laius, thebes, crossroads)` → satisfies `at(laius, crossroads)`.
3. `kills(oedipus, laius)` with bindings `{LOC: crossroads, WEAPON: sword}` → goal.

Or some valid reordering. The spike accepts any valid total-order sequence.

This is a deliberately narrow test. If it succeeds, CS3's primitive mechanism works. If it fails, something in POCL-in-Python or state representation is broken in a way we can debug.

### S3P5 — Substrate Event emission

Each planned action becomes a `substrate.Event`:

```python
Event(
    id="planned_oedipus_travel_corinth_to_crossroads",
    type="travel",
    τ_s=-100,                               # assigned by planner
    τ_a=1,                                  # plan-step order
    participants={"agent": "oedipus",
                  "from_loc": "corinth",
                  "to_loc": "crossroads"},
    effects=(
        WorldEffect(Prop("at", ("oedipus", "crossroads")), asserts=True),
        WorldEffect(Prop("at", ("oedipus", "corinth")), asserts=False),
    ),
    preconditions=(
        Prop("at", ("oedipus", "corinth")),
        Prop("path", ("corinth", "crossroads")),
    ),
    status=EventStatus.PROVISIONAL,  # planner output is provisional
    branches=frozenset({CANONICAL_LABEL}),
)
```

Key commitments:
- `τ_s` is assigned sequentially by the planner (start negative for pre-play; real τ_s planning is a stage-4 concern but the spike assigns monotonic values).
- `τ_a` is the plan-step ordinal (τ_a=1, 2, 3, …).
- `status=PROVISIONAL` — planned events are not committed canonical until a separate step promotes them. The spike emits provisional only.
- `preconditions` mirrors the operator schema's preconditions after variable binding.
- `effects` is a tuple of `WorldEffect` records, matching substrate's existing effect shape.
- `branches` is `frozenset({CANONICAL_LABEL})` — single-branch only for the spike.

Reusing substrate types is load-bearing: the compiler's output is the substrate's input. No translation layer, no novel record kind. CS7's "existing verifiers are the type-check" relies on this.

### S3P6 — Structured infeasibility error

When no plan exists, return a `PlanningError` (sibling to `InfeasibilityError` from stage 2):

```python
@dataclass(frozen=True)
class PlanningError:
    code: str                           # e.g., "no_plan_found"
    goal: str                           # prose description of what failed
    unsatisfied_preconditions: Tuple[str, ...]  # which preconditions the planner couldn't satisfy
    message: str
    relaxations: Tuple[str, ...] = ()
```

Minimum codes for the spike:
- `no_plan_found`: search exhausted without finding a valid sequence.
- `operator_precondition_unsatisfiable`: a specific precondition has no operator that asserts it in its add-effects (static check; short-circuits search).
- `start_state_already_satisfies_goal`: degenerate case — the goal event's preconditions are already true in start state. Not an error, but worth signaling for test clarity.

CS6 discipline preserved: structured error, not exceptional. Callers dispatch on result type. Exceptions reserved for malformed inputs (e.g., operator with empty name).

### S3P7 — Module placement

New sibling module: `prototype/story_engine/core/compiler_stage_3.py`. Imports from:
- `story_engine.core.substrate` — `Event`, `Prop`, `WorldEffect`, `EventStatus`, `CANONICAL_LABEL`.
- `story_engine.core.compiler` — reuse `InfeasibilityError`-adjacent patterns; the spike does NOT refactor `compiler.py` to add stage-3 types.

Parallel to `compiler.py`'s stage-2 home. If stage 3 grows beyond one file post-spike, `core/compiler/` becomes a package with submodules.

**Not in the spike:** a unified `Compiler` class orchestrating stages 1/2/3/4. The spike remains function-level composable, matching stage-2's posture.

## Open questions — banked

### S3P-OQ1 — State representation richness

The spike uses propositional + typed. The target event (`kills(oedipus, laius)`) doesn't need epistemic state; Oedipus kills Laius regardless of whether either knows who the other is. But richer events will need more:

- `E_oedipus_answers_sphinx` — precondition: Oedipus believes the answer is "man."
- `E_tiresias_utters_truth` — effect: specific epistemic update on Oedipus (disclosure).
- `E_jocasta_realizes` — effect: anagnorisis, belief migration.

If a follow-on spike targets any of these, propositional state runs out. Options (per compilation-sketch-01 OQ1):

- Extend `Prop` to carry modality markers: `Prop("believes", ("oedipus", subsumed_prop))`.
- First-order epistemic logic (Kripke frames; possible-worlds reasoning). Heavy.
- Stay propositional; force authors to flatten epistemic claims to atoms.

**Forcing function:** second stage-3 spike whose target event has an epistemic precondition. Banked.

### S3P-OQ2 — Planner search strategy inside POCL

POCL can be implemented with several search strategies:
- Forward-from-initial.
- Regression-from-goal.
- Bidirectional / best-first.

For the spike's 2-operator, ~3-action problem, any strategy finds a plan in milliseconds. Choice becomes consequential at larger scales.

**Forcing function:** third / fourth operator in the library exposes search-strategy implications (branching factor grows). Banked; the spike picks regression-from-goal (it's the most direct match for "fill preconditions" semantics and makes the infeasibility-detection path cleanest — when no operator has the required goal proposition in its add-effects, regression dead-ends immediately).

### S3P-OQ3 — Operator schema home

For the spike, operators are Python literals in the test module. Real stage 3 needs a home for operator libraries. Three shapes:

- **Per-dialect.** Each dialect ships its own operator library (Aristotelian operators, STC operators, …). Admits dialect-specific semantics. Risks duplication.
- **Dialect-agnostic core + per-dialect extensions.** Travel, communicate, meet, perceive in a shared core; dialect-specific operators in dialect modules. Matches DCS5's dialect-locality layered on a core.
- **Encoding-supplied.** Each encoding authors its own operators. Maximum flexibility; risks encoding-to-encoding drift.

**Forcing function:** second dialect attempts stage 3. If Save-the-Cat's "Fun and Games" beat needs genre-specific operators (Monster-in-the-House's "monster attacks"), dialect-agnostic-core becomes stressed. Banked.

### S3P-OQ4 — Goal specification granularity

The spike's goal is one authored event with explicit preconditions. Real stage 3's goal might be:

- A single event with preconditions (spike's case).
- A set of preconditions the substrate must eventually satisfy (no specific event).
- A dialect-level assertion (e.g., A15-SE2 co-presence requirement) that the planner translates to preconditions.
- A multi-event goal (plan for A, then B, then C).

**Forcing function:** first integration with stage 1 (constraint extraction emits goals; stage 3 reads them). Banked.

### S3P-OQ5 — Stage-2-to-stage-3 handoff

Production stage 3 runs after stage-2 feasibility passes. The spike skips stage 2. At production, stage 2 knows `aggregate_min_events = N`; stage 3 must produce exactly ≥N events. Does stage 2 pass stage 3 a *count* requirement, or does stage 3 independently meet the dialect-level cardinality?

**Forcing function:** first multi-stage integration attempt (stage 1 → 2 → 3 pipeline). Banked.

### S3P-OQ6 — Branch labeling on planned events

Spike emits `CANONICAL_LABEL` only. Real stage 3 may emit to contested / draft branches (e.g., "hypothetical plan variant"; "what-if explorations"; "this plan vs. that plan" for ranker input at stage 4). How does the planner know which branch to target?

**Forcing function:** first stage-3+stage-4 integration where ranker examines multiple planned branches. Banked.

## Worked example — Oedipus crossroads spike

### Start state

```python
START_STATE = {
    Prop("at", ("oedipus", "corinth")),
    Prop("at", ("laius", "thebes")),
    Prop("has", ("oedipus", "sword")),
    Prop("path", ("corinth", "crossroads")),
    Prop("path", ("thebes", "crossroads")),
    Prop("alive", ("oedipus",)),
    Prop("alive", ("laius",)),
}
```

### Goal

Apply `KILLS` with bindings the planner chooses. Expected final bindings: `killer=oedipus, victim=laius`.

Expected plan (one of; ordering of the two travels is interchangeable):

```
Step 1 (τ_s=-100, τ_a=1): travel(oedipus, corinth, crossroads)
Step 2 (τ_s=-99,  τ_a=2): travel(laius,   thebes,  crossroads)
Step 3 (τ_s=-98,  τ_a=3): kills(oedipus, laius)
```

Verification: after applying all three events' effects to start state:
- `at(oedipus, crossroads)` — asserted by step 1.
- `at(laius, crossroads)` — asserted by step 2.
- `has(oedipus, sword)` — unchanged from start.
- `alive(oedipus)` — unchanged.
- `dead(laius)` — asserted by step 3.
- `alive(laius)` — retracted by step 3.

All of `KILLS`'s preconditions satisfied immediately before step 3. Plan is valid.

### Infeasibility variant

Change start state: remove `Prop("has", ("oedipus", "sword"))`. Re-run. Expected outcome:

- `PlanningError` with code `no_plan_found`.
- `unsatisfied_preconditions = ("has(killer, WEAPON)",)` (or similar representation).
- No operator in the spike's library adds a `has` proposition. Planner dead-ends; error surfaces cleanly.

If we wanted to close this gap, we'd add an operator like `acquire(agent, item)` with its own preconditions. The spike does not; the infeasibility case is what a missing operator looks like.

### Degenerate variant

Start state already has Oedipus and Laius at the crossroads. Expected outcome:

- `PlanningError` with code `start_state_already_satisfies_goal`, OR
- A one-step plan: just `kills(oedipus, laius)`.

The spike emits the one-step plan (not an error) — the planner succeeds trivially. The degenerate code exists for test clarity more than production behavior.

## Success / failure criteria

**Success:**
- Planner returns a valid plan (list of `substrate.Event` records) for the crossroads case.
- Plan length is 3 (± any reordering). Longer plans would indicate search inefficiency — noted but not a spike failure.
- Each event's preconditions are satisfied by the cumulative state at its τ_s position (sanity check applied by the test harness).
- Removing the weapon from start state produces a structured `PlanningError`.
- Test suite passes. Full prototype suite stays green.

**Failure modes to watch for:**
- Planner loops infinitely (spike has ~20-action search horizon; beyond that, declare infeasible and investigate).
- Propositional state insufficient — if the spike's authored `KILLS` preconditions need epistemic state (e.g., "Oedipus doesn't recognize Laius"), S3P-OQ1 binds; sketch amended.
- Operator schema authoring is onerous — if authoring 2 operators takes >2 hours including debugging, S3P-OQ3 binds and scope-creep risk rises.
- POCL implementation complexity exceeds spike target (~300 LOC core). If it doesn't fit, simplify to forward-search (lose partial-order benefits; retain primitive-mechanism test).

**Partial success (still useful per `project_solution_horizon.md`):**
- Planner works on the easy case but can't close the infeasibility case. Learn: error detection needs more work; not an architecture problem.
- Planner works only with explicit variable bindings passed in (not general unification). Learn: unification needs its own iteration.

**Honest failure:**
- The spike cannot produce a plan for the 3-action crossroads case even with full debugging effort. Escalates to OQ3 (planner choice) and forces the sketch-02 discussion — maybe POCL-in-Python isn't the right primitive; maybe ASP or PDDL-subprocess is needed.

## Relationship to prior commitments

| Prior | Refined / engaged by stage-3 spike | How |
|---|---|---|
| `compilation-sketch-01` CS3 | First concrete test | STRIPS-shape primitives implemented; success/failure answers feasibility question |
| `compilation-sketch-01` CS1 | Partially instantiated | Stage-3 function shape concrete |
| `compilation-sketch-01` CS5 | Trivially preserved | No LLM in the spike |
| `compilation-sketch-01` CS6 | Error-pattern transferred | `PlanningError` mirrors `InfeasibilityError` |
| `compilation-sketch-01` CS7 | Honored | Output is `substrate.Event`; existing substrate audits are the type-check |
| `compilation-sketch-01` OQ1 | May bind during spike | Spike starts propositional; if target-event needs epistemic state, OQ1 fires |
| `compilation-sketch-01` OQ3 | Partially committed | POCL-in-Python picked for the spike; other planner choices deferred |
| `compilation-sketch-01` OQ5 | Unaffected | No soft constraints in the spike |
| `compilation-stage-2-sketch-01` S2F4 | Mirrored | `PlanningError` shape parallels `InfeasibilityError`; callers dispatch on result type |
| `feedback_risk_first_sequencing.md` | Second acted-on instance | Stage-2 was the first; stage-3 is the load-bearing one |
| `feedback_python_as_spec.md` | Honored | Python POCL; no FastDownward subprocess |
| `project_solution_horizon.md` | Load-bearing | Strong input either way: succeed → thesis supported; fail → concrete block identified |

## Implementation brief

1. **Module.** `prototype/story_engine/core/compiler_stage_3.py` — new sibling module. Public API: `PlanningError`, `OperatorSchema`, `PlanningGoal`, `plan_to_goal(start_state, goal, operators) -> Union[Tuple[Event, ...], PlanningError]`.
2. **Core types.** Reuse `substrate.Prop`, `substrate.Event`, `substrate.WorldEffect`, `substrate.EventStatus`, `substrate.CANONICAL_LABEL`. No new record types except `PlanningError`, `OperatorSchema`, `PlanningGoal`.
3. **Planner.** Regression-from-goal search per S3P-OQ2. Maintains open-subgoals + causal-links + action-list; expands by inserting an operator whose add-effects unify with an open subgoal; backtracks on conflict.
4. **Unification.** Python dict-based binding: `{"LOC": "crossroads", "WEAPON": "sword"}`. No occurs-check for spike (propositional; no self-referential terms).
5. **Tests.** `prototype/tests/test_compiler_stage_3.py`. Fixtures + tests:
   - Worked example: crossroads plan found; ≥3-step; each event's preconditions satisfied at its τ_s.
   - Infeasibility: weapon removed → `PlanningError(code="no_plan_found")` with specific unsatisfied precondition named.
   - Degenerate: start state already at crossroads → 1-step plan.
   - Operator-library sanity: both `TRAVEL` and `KILLS` construct; schemas pass basic shape validation.
   - Substrate integration: emitted events have `status=PROVISIONAL`, `branches={CANONICAL_LABEL}`, correct participants dicts, preconditions tuples mirror operator schema.
   - Negative: operator with empty name / missing params → `ValueError`.
6. **Test registration.** README bulk-run list updated.
7. **Zero changes to existing modules.** Spike adds; it doesn't modify.

Expected test count: 12-18 tests. Full suite: ~920 (from 904).

## What a cold-start Claude should read first

1. `compilation-sketch-01.md` — CS3 is the target commitment.
2. `compilation-stage-2-sketch-01.md` — the sibling stage's pattern this spike mirrors.
3. This sketch.
4. `prototype/story_engine/core/substrate.py` §Event, §Prop, §WorldEffect — the types the planner emits.
5. `prototype/story_engine/encodings/oedipus.py` — the descriptive-only encoding the spike complements with a planner-ready fresh one.
6. `feedback_risk_first_sequencing.md` (memory) — the sequencing discipline that motivated the spike order.
7. `project_solution_horizon.md` (memory) — dual-axis framing.

## Honest framing

This spike is narrow by design. Two operators, one goal event, one Oedipus scene. Success doesn't prove stage 3 works on Hamlet's 32 events; failure doesn't prove stage 3 is impossible. What the spike proves or disproves is whether the *primitive mechanism* — POCL-in-Python producing intermediate events to satisfy preconditions — works for a minimum-viable concrete test.

Per the user's in-conversation framing: *"It's really the test of whether the entire project is feasible."* The spike honors that framing by testing the hardest promise (synthesis, not gate, not selection) on the smallest honest case. If the primitive mechanism works, the path to scale is engineering — more operators, richer state, better search, integration with stages 1/2/4. If it doesn't, we've identified the actual block and can decide whether to attack it (enrich state; different planner) or declare that axis infeasible (and the solution-horizon framing still leaves value in the naming).

Per `project_solution_horizon.md`: the spike is a strong input either way. If this engine implements a full stage 3 from here, the spike is the foundation. If a future more-capable AI implements stage 3, it inherits:
- The POCL-in-Python primitive mechanism (proven on Oedipus).
- The `substrate.Event`-as-planner-output convention.
- The `PlanningError`-mirrors-`InfeasibilityError` error-handling pattern.
- The OQ framing (state richness; planner choice; operator schema home; goal granularity).

That's substantially more concrete than "stage 3 is STRIPS-shape." The spike is the reduction to something a future AI — or this one in a later session — can extend step by step.

The spike is also honest about what it can't tell us. A 3-action plan on a contrived scene does not validate the architecture for multi-act stories with epistemic complexity and soft preferences. The spike closes one question and names the next ones. That's the right posture for a risk-reduction spike on a multi-year project.
