# Compilation stage 3 (planner spike) — sketch 02 (typed variables + library growth)

**Status:** draft, active
**Date:** 2026-04-21
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [compilation-stage-3-sketch-01](compilation-stage-3-sketch-01.md) — S3P1–S3P7 unchanged structurally; S3P1 algorithm and S3P3 operator-library expanded
**Frames:** `compilation-sketch-01` CS3 (the spike this extends is its first concrete test); `feedback_python_as_spec.md`
**Related:** `prototype/story_engine/core/compiler_stage_3.py` (the sketch-01 implementation this sketch amends); `substrate.Prop` (the state-assertion shape now carrying type/2 records)
**Superseded by:** nothing yet

## Purpose

Address two findings from sketch-01's implementation:

1. **Fragility in free-variable enumeration.** Sketch-01's enumeration iterates every ground term over every free variable, including semantically-nonsensical bindings (e.g., `LOC = oedipus` producing goal `at(oedipus, oedipus)`). A visited-set guard in `_achieve` catches the resulting infinite regress, but user framing was explicit: *"visited state works, but it is probably not the final form."*

2. **One scene, two operators is thin evidence.** Sketch-01 proved the primitive mechanism on `kills(oedipus, laius)` with travel+kills. The thesis needs a marginal stress test: can the library grow, can the plan lengthen, does the primitive compose across operator kinds?

This sketch commits:

- **S3P8** — typed variables on operator schemas + typed enumeration in the planner. Nonsensical bindings never enumerated; fragility fix is *structural* rather than post-hoc. Visited-set guard remains as defensive belt-and-suspenders but ceases to be load-bearing.
- **S3P9** — third operator: `acquire(AGENT, ITEM, LOCATION)`. Precondition: both agent and item at the location. Effect: agent holds item; item no longer at the location.
- **S3P10** — second worked-example scene: *"Oedipus acquires sword en route."* Start state has Oedipus at Corinth unarmed, sword at crossroads, Laius at Thebes. Goal: `kills(oedipus, laius)`. Expected plan: 4 steps (two travels + one acquire + the kill).

Structural commitments from sketch-01 (S3P1–S3P7) remain intact. The API signature for `plan_to_goal` is unchanged. Tests for scene-1 continue to pass post-migration.

## Why now

Two reasons:

1. **User-framed fragility concern.** 2026-04-21, user: *"stage-3 spike is there. It is functional. It is also fragile. The visited state works, but it is probably not the final form."* Sketch-02 resolves the "not the final form" concern.

2. **Continued risk-reduction on the compiler.** Per `feedback_risk_first_sequencing.md`, the compiler is the project's biggest unretired risk. Sketch-01 answered *"can POCL-in-Python produce intermediate-event sequences at all?"* (yes). Sketch-02 answers the next risk-reduction question: *"does the primitive generalize to operator-library growth and longer plans?"* If it does, stage 3 is more than a single-lucky-case. If it doesn't, sketch-02 surfaces what breaks.

## Scope — what this sketch does and doesn't do

**In scope:**

- Typed-variables amendment to `OperatorSchema` (S3P8).
- Type-aware enumeration in `_achieve` and `plan_to_goal` (S3P8).
- Type registry extracted from start-state `type/2` propositions (S3P8).
- Third operator `acquire` (S3P9).
- Second worked-example scene + its tests (S3P10).
- Migration of existing TRAVEL / KILLS schemas + scene-1 tests to typed form.
- Keep visited-set guard; demote to defensive-only (document as such).

**Out of scope:**

- **Removing the visited-set guard.** Defer until sketch-03 or later, once type-enumeration robustness is proven across more operators. Removing it now is premature — if a type-hole exists that types don't catch, the guard is the safety net.
- **Type hierarchy / subtyping.** All types in this spike are flat and unrelated (agent, location, object). "Weapon is a subtype of object" is S3P-OQ8; deferred.
- **Inferred types from predicate positions.** Types declared explicitly on schemas and on ground terms. Inference is S3P-OQ7; deferred.
- **Central type registry per dialect.** Types live per-operator and per-state-assertion; no shared "all types in the Aristotelian world" registry yet. S3P-OQ7 covers this too.
- **Third scene / third extension.** Two scenes is the stress test; more is diminishing-returns for a spike.
- **Stage-1/stage-4 integration.** Still hand-wired.
- **PDDL export.** Python-as-spec; no translation to standard format yet.

## Commitments

Labels **S3P8..S3P10** continue sketch-01's S3P1..S3P7 numbering.

### S3P8 — Typed variables

`OperatorSchema` gains a required `variable_types` field:

```python
@dataclass(frozen=True)
class OperatorSchema:
    name: str
    params: Tuple[str, ...]
    variable_types: Dict[str, str]     # NEW — every variable (params + free vars) maps to a type name
    preconditions: Tuple[Prop, ...]
    add_effects: Tuple[Prop, ...]
    del_effects: Tuple[Prop, ...]
```

Every variable referenced in `params`, `preconditions`, `add_effects`, or `del_effects` MUST be a key in `variable_types`. Validation at `__post_init__` rejects schemas with missing entries.

Example (sketch-01's TRAVEL migrated to typed form):

```python
TRAVEL = OperatorSchema(
    name="travel",
    params=("AGENT", "FROM", "TO"),
    variable_types={
        "AGENT": "agent",
        "FROM": "location",
        "TO": "location",
    },
    preconditions=(
        Prop("at", ("AGENT", "FROM")),
        Prop("path", ("FROM", "TO")),
    ),
    add_effects=(Prop("at", ("AGENT", "TO")),),
    del_effects=(Prop("at", ("AGENT", "FROM")),),
)
```

KILLS similarly:

```python
KILLS = OperatorSchema(
    name="kills",
    params=("KILLER", "VICTIM"),
    variable_types={
        "KILLER": "agent",
        "VICTIM": "agent",
        "LOC": "location",
        "WEAPON": "object",
    },
    preconditions=(
        Prop("at", ("KILLER", "LOC")),
        Prop("at", ("VICTIM", "LOC")),
        Prop("has", ("KILLER", "WEAPON")),
        Prop("alive", ("KILLER",)),
        Prop("alive", ("VICTIM",)),
    ),
    add_effects=(Prop("dead", ("VICTIM",)),),
    del_effects=(Prop("alive", ("VICTIM",)),),
)
```

### S3P8 — State-side type assertions

Ground terms declare their type via `Prop("type", (term, type_name))`:

```python
START_STATE = frozenset({
    Prop("type", ("oedipus", "agent")),
    Prop("type", ("laius", "agent")),
    Prop("type", ("corinth", "location")),
    Prop("type", ("thebes", "location")),
    Prop("type", ("crossroads", "location")),
    Prop("type", ("sword", "object")),
    # … and the non-type propositions from before
    Prop("at", ("oedipus", "corinth")),
    # …
})
```

The `"type"` predicate name is unused elsewhere in the substrate (verified against `substrate.py` and `encodings/`) so there is no collision.

### S3P8 — Typed enumeration

The planner's `_enumerate_variable_bindings` function consults the type registry:

- Extract `type_registry: Dict[str, str]` from the start state's `type/2` propositions (term → type_name).
- Group terms by type: `terms_by_type: Dict[str, List[str]]`.
- For each free variable V with declared type T, enumerate only over `terms_by_type[T]` rather than the full universe.
- A variable whose declared type has zero terms in the state produces zero candidates — immediate infeasibility; planner surfaces as part of the PlanningError.

**Fallback for untyped legacy variables:** removed. Every schema variable must have a type declared. Existing code (sketch-01's TRAVEL/KILLS) migrates in the implementation commit.

### S3P8 — Visited-set guard demoted (partially)

The visited-set guard in `_achieve` remains in the code. Its role shifts:

- **Before sketch-02:** load-bearing for two overlapping reasons:
  - (a) Preventing infinite recursion from nonsensical-typed bindings (e.g., LOC=oedipus → goal `at(oedipus, oedipus)` → recurse forever).
  - (b) Pruning sub-problem repetition during legitimate dead-end exploration (e.g., the planner tries LOC=corinth before finding LOC=crossroads; the corinth branch attempts to move Laius to corinth, which recurses through `at(laius, corinth)` via a TRAVEL chain that eventually re-encounters the same subgoal).

- **After sketch-02:** typed enumeration eliminates (a) entirely — LOC is never bound to `oedipus` because their types don't match. But (b) remains — typed dead-end exploration still needs cycle-pruning, because the same legitimate subgoal can be re-requested through different operator/binding chains while backtracking.

**Observed behavior post-implementation.** On scene 1 success, the guard fires ~6 times — all from (b), none from (a). On scene 2 success with the extended operator library, it fires ~9 times. These are bounded, productive firings: they prune repeated subgoals within a single planning call, making search efficient.

**The 0-firings claim in a preliminary version of this sketch was incorrect.** Implementation surfaced (b) as a legitimate second role for the guard. The sketch now claims bounded (not zero) firings as the success invariant.

Test pins:
- Scene 1 success: guard fires < 50 times (observed ~6).
- Scene 2 success: guard fires < 100 times (observed ~9).

A future regression where firings explode to thousands would signal either a new failure mode (type-hole; something (a)-adjacent) or that typed enumeration has silently broken.

Removing the guard entirely is no longer defensible for sketch-03 without an alternative cycle-pruning mechanism (e.g., proper POCL causal links). The guard has a real job; "belt-and-suspenders" was the wrong framing.

S3P-OQ9 (below) is refined accordingly.

### S3P9 — Third operator: `acquire`

```python
ACQUIRE = OperatorSchema(
    name="acquire",
    params=("AGENT", "ITEM", "LOCATION"),
    variable_types={
        "AGENT": "agent",
        "ITEM": "object",
        "LOCATION": "location",
    },
    preconditions=(
        Prop("at", ("AGENT", "LOCATION")),
        Prop("at", ("ITEM", "LOCATION")),
    ),
    add_effects=(
        Prop("has", ("AGENT", "ITEM")),
    ),
    del_effects=(
        Prop("at", ("ITEM", "LOCATION")),
    ),
)
```

**Semantic note.** The operator asserts `has(AGENT, ITEM)` and retracts `at(ITEM, LOCATION)`. The spike's item model is holder-OR-location, not both — once an item is acquired, it tracks with its holder via the has relation, and its location proposition is gone. This is a deliberate simplification; full world-modeling (item at holder's current location) is deferred.

**Why `acquire` specifically:**
- Exercises the operator library growing from 2 → 3 without adding a new type (agent/location/object already in sketch-01's universe).
- Its preconditions include *two* agent-location relations (the agent and the item must both be at the location), testing precondition-conjunction handling.
- Its effect pattern (add a has; del an at) is fundamentally different from travel (del old at, add new at) and kills (add dead, del alive). Tests pattern diversity.

### S3P10 — Second worked-example scene: "Oedipus acquires sword en route"

Start state:

```python
SCENE_2_START = frozenset({
    # Type assertions (S3P8)
    Prop("type", ("oedipus", "agent")),
    Prop("type", ("laius", "agent")),
    Prop("type", ("corinth", "location")),
    Prop("type", ("thebes", "location")),
    Prop("type", ("crossroads", "location")),
    Prop("type", ("sword", "object")),
    # World state
    Prop("at", ("oedipus", "corinth")),
    Prop("at", ("laius", "thebes")),
    Prop("at", ("sword", "crossroads")),    # sword is at a location, not held
    Prop("path", ("corinth", "crossroads")),
    Prop("path", ("thebes", "crossroads")),
    Prop("alive", ("oedipus",)),
    Prop("alive", ("laius",)),
})
```

Goal: `kills(oedipus, laius)` — KILLER and VICTIM bound; LOC and WEAPON enumerated by planner.

Expected plan (4 steps; ordering of the two travels may swap):

```
Step 1 (τ_s=-100, τ_a=1): travel(oedipus, corinth, crossroads)
Step 2 (τ_s=-99,  τ_a=2): travel(laius,   thebes,  crossroads)
Step 3 (τ_s=-98,  τ_a=3): acquire(oedipus, sword, crossroads)
Step 4 (τ_s=-97,  τ_a=4): kills(oedipus, laius)
```

Invariant at each step: cumulative state satisfies the step's preconditions.

- Before step 1: `at(oedipus, corinth)` ✓, `path(corinth, crossroads)` ✓.
- Before step 2: (state now has `at(oedipus, crossroads)`) — `at(laius, thebes)` ✓, `path(thebes, crossroads)` ✓.
- Before step 3: `at(oedipus, crossroads)` ✓ (step 1), `at(sword, crossroads)` ✓ (unchanged from start).
- Before step 4: `at(oedipus, crossroads)` ✓, `at(laius, crossroads)` ✓ (step 2), `has(oedipus, sword)` ✓ (step 3), `alive(oedipus)` ✓, `alive(laius)` ✓.

Final state: `dead(laius)`; `has(oedipus, sword)`; `at(oedipus, crossroads)`; `at(laius, crossroads)` still holds (kills doesn't del location). The sword's `at` was deled at step 3.

## Open questions — banked

### S3P-OQ7 — Type registry home

Types live per-schema (`variable_types`) and per-ground-term (state `type/2` propositions). A shared "all types in the world" registry does not exist. Open questions:

- Should there be a dialect-level type registry (Aristotelian types, STC types, etc.) analogous to role-label vocabularies in STC S10?
- Should `agent`, `location`, `object` be cross-dialect shared types (parallel to the DOQ2 judgment's recommendation to globalize certain dialect fields)?
- Should types be inferred from predicate positions (e.g., `at(X, Y)`'s second arg is always a location)?

**Forcing function:** second dialect growing stage-3 operators. Banked.

### S3P-OQ8 — Subtyping / type hierarchy

All types in sketch-02 are flat. `"weapon"` is not a subtype of `"object"`; they're unrelated. A variable typed `"object"` binds to ANY object-typed term, including swords, daggers, and non-weapons.

If a future operator needs "must be a weapon" specifically (beyond "is an object"), flat types fall short.

**Forcing function:** first operator that needs a narrower type than the existing flat types admit. Banked.

### S3P-OQ9 — Visited-set replacement (not removal)

Sketch-02 implementation refined the original question. The guard is NOT removable without replacement — it does real work pruning sub-problem repetition during dead-end search exploration. Two replacement paths:

- **Proper POCL with causal links.** Track which actions provide which preconditions as first-class data; re-entering a subgoal is legitimate if the requesting causal slot differs. This is classical POCL semantics (Weld 1994) and would be the "right" replacement — the current visited-set is essentially a degenerate form of causal-link tracking.
- **Memoization by (subgoal, state_hash).** Cache successful subplans so they're reused rather than re-derived. Orthogonal to the guard; complementary.

**Forcing function:** operator library growth sufficient to make the current per-call-chain visited set inefficient (firings grow faster than plan size warrants). Concrete threshold: ~6 operators or longer plans (~8+ steps) where re-deriving subplans across branches becomes noticeable.

Spike stance: keep the visited-set; accept bounded firings as the invariant; replace when the replacement pays its own freight. Removing it prematurely regresses to sketch-01's fragility plus loses (b)'s pruning benefit.

## Worked example verification — scene 1 under sketch-02

Scene 1's goal, start state, and expected plan are unchanged from sketch-01. Under sketch-02's typed enumeration:

- `LOC` is declared type `location`. Enumeration considers only `{corinth, thebes, crossroads}` — 3 candidates instead of the full-universe 6. For each, the planner tries to satisfy co-location.
- `WEAPON` is declared type `object`. Enumeration considers only `{sword}` — 1 candidate. No nonsensical bindings.
- Total candidate product: 3 × 1 = 3, versus sketch-01's 6 × 6 = 36. **12× smaller search space.** The win grows quadratically in universe size.

Test that scene-1's plan is identical to sketch-01's output (same 3 events, same effects); assert the visited-set guard's instrumentation counter is 0.

## Implementation brief

1. **core/compiler_stage_3.py**:
   - Add `variable_types: Dict[str, str]` field to `OperatorSchema`.
   - Validate completeness in `__post_init__`: every variable in params, preconditions, add_effects, del_effects must be a key in variable_types.
   - Define `ACQUIRE` operator schema at module scope? **No** — per sketch-01's convention, operators are defined at call sites (test fixtures, future encoding modules). `ACQUIRE` lives in the test file as a fixture, not in `compiler_stage_3.py`.
   - Replace `_extract_ground_terms` with `_build_type_registry` returning `Dict[str, str]` (term → type_name).
   - Replace `_enumerate_variable_bindings(free_vars, universe)` with `_enumerate_variable_bindings(free_vars, variable_types, type_registry)` — signature change.
   - Update `_achieve` and `plan_to_goal` call sites to pass the type registry.
   - Add instrumentation counter for visited-set firings: module-level `_VISITED_GUARD_FIRES` counter, resettable via `_reset_visited_guard_counter()` for tests.
   - Document visited-set guard as "defensive; should be 0-firing under sketch-02 types."

2. **tests/test_compiler_stage_3.py**:
   - Migrate TRAVEL and KILLS fixtures to include `variable_types`.
   - Add `type/2` propositions to all start-state fixtures.
   - Add `ACQUIRE` fixture at module scope.
   - Add scene-2 fixtures + 4-step plan verification tests.
   - Add typed-enumeration regression tests: invalid variable type in schema → ValueError; variable type with zero terms → infeasibility.
   - Add visited-set-counter test: scene 1 under sketch-02 fires the guard zero times.

3. **Zero changes to sketch-01's sketch document.** Sketch-02 extends but doesn't rewrite sketch-01.

Expected test count: sketch-01's 24 + ~12 new (scene 2, acquire, typed-enum edge cases, visited-counter assertion). Full suite: ~940.

## What a cold-start Claude should read first

1. `compilation-stage-3-sketch-01.md` — the foundation.
2. This sketch — the amendment.
3. `prototype/story_engine/core/compiler_stage_3.py` — the post-migration implementation.
4. `prototype/tests/test_compiler_stage_3.py` — the test fixtures, including ACQUIRE, both scenes.

## Honest framing

Sketch-02 is a modest extension: one operator, one scene, typed enumeration replacing a hack. Its value is *confirming that the sketch-01 primitive generalizes* rather than proving new architectural ground. Small-delta, meaningful risk-reduction.

The fragility concern the user raised is addressed structurally, not via additional runtime guards. Typed variables prevent nonsensical enumerations at the source. The visited-set guard stays in defensively, with a counter to prove it doesn't fire under sketch-02's types — if a future sketch introduces the guard firing, we'll see it immediately and investigate.

Per `project_solution_horizon.md`: sketch-02 is slightly-stronger input than sketch-01. A working operator library of 3 (not 2) with typed discipline is more convincing than 2-with-visited-hack. The delta isn't huge, but the direction of travel is the right one: each stage-3 sketch should either grow the operator library, grow the scene complexity, or address a known weakness — and each is the smallest-honest-increment that pressure-tests the primitive mechanism from a new angle.
