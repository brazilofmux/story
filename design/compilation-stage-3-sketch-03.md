# Compilation stage 3 (planner spike) — sketch 03 (epistemic preconditions + Oedipus vs Sphinx)

**Status:** draft, active
**Date:** 2026-04-21
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [compilation-stage-3-sketch-01](compilation-stage-3-sketch-01.md), [compilation-stage-3-sketch-02](compilation-stage-3-sketch-02.md) — S3P1–S3P10 unchanged structurally; operator library and scene count grow
**Frames:** `compilation-sketch-01` OQ1 (state-representation richness — this sketch exercises the propositional-plus-fact form of epistemic state and pressures OQ1 concretely); `compilation-sketch-01` CS3 (the compiler's hardest promise, now tested with a 4-step plan whose intermediate step is knowledge-acquisition); `feedback_risk_first_sequencing.md`
**Related:** `prototype/story_engine/core/compiler_stage_3.py` (unchanged by this sketch; new operators live as test-file fixtures per sketch-02 S3P9 convention)
**Superseded by:** nothing yet

## Purpose

Scene 3: Oedipus defeats the Sphinx by answering its riddle. Tests the third load-bearing question about stage 3's viability — can the planner handle **epistemic preconditions** (knowledge the agent must have), not just spatial/material ones (location, possession, liveness).

Per `compilation-sketch-01` OQ1: *"Stories need richer state: epistemic (who knows what), affective (who feels what), relational (alliance, suspicion, trust)."* Scene 3 is the first OQ1 probe. The spike's answer: if flat propositional `knows(agent, fact)` works, OQ1's epistemic axis is handled; if it doesn't, we learn the constraint.

The scene also lengthens the plan to 4 steps via a deliberate detour: Oedipus starts at Corinth, but the Oracle (who knows the riddle's answer) is at Delphi. The planner must synthesize a Corinth → Delphi → Thebes-gates route, with knowledge acquired in the middle.

## Why now

Third spike on stage 3, continuing the compiler risk-reduction arc per `feedback_risk_first_sequencing.md`. Each spike stresses stage 3 from a new angle:

- Sketch-01: primitive mechanism works (one scene, two operators, 3-step plan).
- Sketch-02: operator library grows and typed discipline lands (two scenes, three operators, up to 4-step plan).
- Sketch-03: **epistemic state works** (three scenes, five operators, 4-step plan with mid-plan knowledge acquisition).

If scene 3 succeeds, OQ1's epistemic axis is answered in the affirmative for flat propositional knowledge. The axis's harder sub-cases (nested knowledge, modal slots, temporal reasoning) remain as future work.

User directive: *"Proceed."*

## Scope — what this sketch does and doesn't do

**In scope:**

- **S3P11.** Declare the new type `fact` (joining `agent`, `location`, `object`).
- **S3P12.** Two new operators — `learn_from` and `defeat_by_riddle` — as test-file fixtures.
- **S3P13.** Scene 3 start state and expected plan.
- **S3P14.** Schema-level precondition ordering discipline (knows-before-at) pragmatically honored; banked as OQ for threat-resolution replacement.
- No changes to `compiler_stage_3.py` core algorithm. The `fact` type is just a type-name; typed enumeration handles it uniformly.

**Out of scope:**

- Nested knowledge (`knows(A, knows(B, P))`). Flat propositional knowledge only.
- Modal slots (known / believed / suspected). No confidence grading; `knows` is binary.
- Temporal reasoning on knowledge ("A knew P at τ=5"). No τ_s-indexed epistemic state.
- Knowledge via inference (derivation rules). Knowledge comes only from direct acquisition via `learn_from`.
- Threat-resolution / proper POCL promotion-demotion. Sketch-03 relies on pragmatic schema-level ordering and banks the real fix as S3P-OQ10.
- Forgetting / loss of knowledge. `learn_from` adds `knows`; no operator removes it.

## Commitments

Labels **S3P11..S3P14** continue sketch-02's numbering.

### S3P11 — New type `fact`

A fourth type joining the existing flat catalog:

```
AGENT_TYPE    = "agent"
LOCATION_TYPE = "location"
OBJECT_TYPE   = "object"
FACT_TYPE     = "fact"            # NEW (S3P11)
```

Type assertions in state:

```python
Prop("type", ("riddle_answer", "fact"))
```

No subtyping. `fact` is unrelated to `object`; they're flat sibling types per sketch-02's S3P-OQ8 deferral of type hierarchy.

**Semantics.** A `fact` term is a labeled knowledge claim. The spike models it as an opaque string token (`"riddle_answer"`, `"laius_is_king_of_thebes"`); the planner does not introspect facts. Real dialects may later upgrade to structured fact shapes (Prop-nested), but the spike doesn't commit to that.

### S3P12 — Two new operators

#### `learn_from(STUDENT, TEACHER, FACT, LOCATION)`

```python
LEARN_FROM = OperatorSchema(
    name="learn_from",
    params=("STUDENT", "TEACHER", "FACT", "LOCATION"),
    variable_types={
        "STUDENT": AGENT_TYPE,
        "TEACHER": AGENT_TYPE,
        "FACT": FACT_TYPE,
        "LOCATION": LOCATION_TYPE,
    },
    preconditions=(
        Prop("knows", ("TEACHER", "FACT")),           # teacher knows (ordered first!)
        Prop("at", ("STUDENT", "LOCATION")),
        Prop("at", ("TEACHER", "LOCATION")),
    ),
    add_effects=(Prop("knows", ("STUDENT", "FACT")),),
    del_effects=(),
)
```

Student + teacher co-located; teacher knows the fact; effect: student now knows the fact too. No del-effects (knowledge accumulates).

**Ordering note.** `knows(TEACHER, FACT)` is listed first deliberately per S3P14 — sequential regression satisfies preconds in order, and putting the knowledge-binding first causes the planner to enumerate over `FACT` before `LOCATION`, which reduces wasted exploration.

#### `defeat_by_riddle(AGENT, OPPONENT, FACT, LOC)`

```python
DEFEAT_BY_RIDDLE = OperatorSchema(
    name="defeat_by_riddle",
    params=("AGENT", "OPPONENT"),
    variable_types={
        "AGENT": AGENT_TYPE,
        "OPPONENT": AGENT_TYPE,
        "FACT": FACT_TYPE,
        "LOC": LOCATION_TYPE,
    },
    preconditions=(
        Prop("knows", ("AGENT", "FACT")),             # S3P14 — knows BEFORE at
        Prop("at", ("AGENT", "LOC")),
        Prop("at", ("OPPONENT", "LOC")),
        Prop("alive", ("AGENT",)),
        Prop("alive", ("OPPONENT",)),
    ),
    add_effects=(Prop("dead", ("OPPONENT",)),),
    del_effects=(Prop("alive", ("OPPONENT",)),),
)
```

Models the Oedipus-Sphinx encounter. Answering the riddle correctly defeats the Sphinx. The spike simplifies the mythological cliff-jumping to "effect: dead(opponent)" — structurally equivalent.

**Precondition ordering, S3P14-compliant.** `knows` first so the planner establishes knowledge before attempting spatial setup. Under the current sequential-regression planner, this ordering avoids the self-invalidation pathology described in S3P-OQ10 below.

### S3P13 — Scene 3 worked example

Start state:

```python
SCENE_3_START = _type_assertions_scene_3() | frozenset({
    # Oedipus starts at Corinth. Unarmed (kills preconditions not tested here).
    Prop("at", ("oedipus", "corinth")),
    Prop("alive", ("oedipus",)),
    # Sphinx at thebes_gates. Alive until defeated.
    Prop("at", ("sphinx", "thebes_gates")),
    Prop("alive", ("sphinx",)),
    # Oracle at Delphi. Knows the riddle answer; is alive.
    Prop("at", ("oracle", "delphi")),
    Prop("alive", ("oracle",)),
    Prop("knows", ("oracle", "riddle_answer")),
    # Path graph: Corinth → Delphi → Thebes-gates. No direct
    # Corinth → Thebes-gates path; the planner MUST route via Delphi.
    Prop("path", ("corinth", "delphi")),
    Prop("path", ("delphi", "thebes_gates")),
})
```

Type assertions (extended):

```python
def _type_assertions_scene_3() -> frozenset:
    return frozenset({
        Prop("type", ("oedipus", AGENT_TYPE)),
        Prop("type", ("sphinx",  AGENT_TYPE)),
        Prop("type", ("oracle",  AGENT_TYPE)),
        Prop("type", ("corinth",      LOCATION_TYPE)),
        Prop("type", ("delphi",       LOCATION_TYPE)),
        Prop("type", ("thebes_gates", LOCATION_TYPE)),
        Prop("type", ("riddle_answer", FACT_TYPE)),
    })
```

Goal:

```python
goal = PlanningGoal(
    operator=DEFEAT_BY_RIDDLE,
    bindings={"AGENT": "oedipus", "OPPONENT": "sphinx"},
)
```

FACT and LOC are free variables, typed `fact` and `location` respectively. Only one fact-typed term (`riddle_answer`) exists in state, so FACT binds unambiguously. LOC enumerates over {corinth, delphi, thebes_gates} — only thebes_gates works (sphinx is there).

Expected plan (4 steps):

```
Step 1 (τ_s=-100, τ_a=1): travel(oedipus, corinth, delphi)
Step 2 (τ_s=-99,  τ_a=2): learn_from(oedipus, oracle, riddle_answer, delphi)
Step 3 (τ_s=-98,  τ_a=3): travel(oedipus, delphi, thebes_gates)
Step 4 (τ_s=-97,  τ_a=4): defeat_by_riddle(oedipus, sphinx, riddle_answer, thebes_gates)
```

Cumulative-state invariant check:

- Before step 1: `at(oedipus, corinth)` ✓, `path(corinth, delphi)` ✓.
- Before step 2: `knows(oracle, riddle_answer)` ✓ (state), `at(oedipus, delphi)` ✓ (step 1), `at(oracle, delphi)` ✓ (state).
- Before step 3: `at(oedipus, delphi)` ✓ (step 1), `path(delphi, thebes_gates)` ✓.
- Before step 4: `knows(oedipus, riddle_answer)` ✓ (step 2), `at(oedipus, thebes_gates)` ✓ (step 3), `at(sphinx, thebes_gates)` ✓ (state), `alive(oedipus)` ✓, `alive(sphinx)` ✓.

Final state: `dead(sphinx)`, `knows(oedipus, riddle_answer)`, `at(oedipus, thebes_gates)`. The `alive(sphinx)` proposition is retracted by step 4's del-effect.

### S3P14 — Precondition ordering discipline (optimization, not correctness)

**Initial hypothesis (pre-implementation):** the current sequential-regression planner iterates preconditions in schema-declared order and threads cumulative state forward, so schema authors MUST order preconditions knows-before-at to avoid invalidation-cascades.

**What implementation surfaced:** the planner is more flexible than the hypothesis credited. With AT-first ordering on `defeat_by_riddle`, the planner still finds a plan — 5 steps instead of 4, because it **travels the Oracle to thebes_gates** rather than requiring Oedipus to come to Delphi:

```
1. travel(oedipus, corinth, delphi)
2. travel(oedipus, delphi, thebes_gates)
3. travel(oracle, delphi, thebes_gates)     # the Oracle follows
4. learn_from(oedipus, oracle, riddle_answer, thebes_gates)
5. defeat_by_riddle(oedipus, sphinx, riddle_answer, thebes_gates)
```

The 5-step plan is valid. Precondition ordering determined *which* plan the planner found (shorter vs longer), not *whether* it found one.

**Why the hypothesis was wrong:** the planner can satisfy `knows(oedipus, riddle_answer)` by moving either the student to the teacher OR the teacher to the student, because both are AGENT-typed and TRAVEL accepts any AGENT. The "student must travel to teacher's location" constraint only holds if the teacher is structurally immobile (different type that TRAVEL rejects, e.g., a shrine or inscription).

**Refined S3P14 (post-implementation):** knows-first ordering is an **optimization discipline** — it yields the shorter, more mythologically-faithful plan (Oedipus consults the Delphic Oracle, then continues to Thebes). AT-first ordering still yields a valid plan, just a longer one where the teacher follows the student. Either is correct.

**When S3P14 would become correctness-critical:** if TRAVEL's AGENT type were narrower than the teacher's type — e.g., if the Oracle were typed `"shrine"` and TRAVEL required `"mobile_agent"`. In that case, the Oracle couldn't travel and the AT-first ordering would be unable to satisfy `knows`. Scene 3 doesn't engineer this case (Oracle is mobile), so S3P14 stays an optimization discipline in the spike.

**S3P-OQ10 refined consequently:** the real issue isn't precondition ordering per se — it's that the current planner finds valid-but-non-optimal plans whose optimality depends on author-chosen schema ordering. A proper POCL with threat resolution + a plan-length heuristic would find the optimal plan regardless of schema order. Banked.

## Open questions — banked

### S3P-OQ10 — Precondition-ordering fragility

Current planner: schema-order sequential regression with threaded state. If preconds are ordered wrong, plans that a proper POCL would find become unreachable.

Proper fix: threat-safe POCL with promotion/demotion:
- When an action A's del-effect invalidates a causal link supporting B's precond P, the planner must **promote** A (move it before the establisher of the link) or **demote** A (move it after B's consumption of P).
- Classical POCL literature (McAllester-Rosenblitt 1991, Weld 1994) covers this thoroughly.

**Forcing function:** an operator-library / scene combination where no legal precondition ordering exists. Likely candidates: scenes where two learn_from acts are needed in separate locations AND agents must visit both before the final action. Current spike avoids this by construction.

Spike stance: accept pragmatic ordering discipline; bank threat resolution for sketch-04 or later.

### S3P-OQ11 — Knowledge-state model richness

Flat propositional `knows(AGENT, FACT)` handles scene 3. What it doesn't handle:

- **Nested knowledge.** `knows(A, knows(B, P))` — A knows that B knows P. Requires Prop-nested args.
- **Modal slots.** `believes(A, P)` vs `knows(A, P)` vs `suspects(A, P)`. Substrate's `Held` records model these; the spike's planner doesn't.
- **False belief.** An agent can `believes(A, P)` where P is world-false. Substrate models this; spike doesn't.
- **Temporal indexing.** "At τ=5, A knew P; at τ=10, A no longer remembers." No τ_s coordinate on knowledge props.
- **Knowledge from inference.** A knows P ∧ B, therefore A knows P. Requires derivation rules (substrate has these for identity substitution).

**Forcing function:** first scene whose target event has a non-flat epistemic precondition. Candidates: `E_jocasta_realizes` (anagnorisis — belief migration), `E_oedipus_doubts_self` (knows-that-knows-that structure), `E_messenger_lies` (false-belief effects).

### S3P-OQ12 — Knowledge acquisition primitives beyond `learn_from`

`learn_from` is one primitive. Stories need others:
- **Perceive.** Agent at location observes a world-true fact. No teacher required.
- **Infer.** Agent combines two known facts via a rule.
- **Read.** Agent at location accesses an inscribed/written fact. Inscription is the "teacher."
- **Overhear.** Agent passively picks up a fact from a conversation they're not a party to.

**Forcing function:** second scene needing knowledge acquisition that `learn_from` can't model. Banked.

## Implementation brief

- **No changes to `compiler_stage_3.py`.** The `fact` type is a string token like any other; existing typed enumeration handles it. The visited-guard, max-depth, unification, and event-emission all work unchanged.
- **All additions to `tests/test_compiler_stage_3.py`:**
  - Add `FACT_TYPE` constant.
  - Add `LEARN_FROM` and `DEFEAT_BY_RIDDLE` operator fixtures.
  - Add `_type_assertions_scene_3()` and `_scene_3_start_state()` helpers.
  - New tests:
    - Scene 3 returns 4-event plan.
    - Scene 3 plan has expected type sequence: travel + learn_from + travel + defeat_by_riddle.
    - Learn_from happens between Oedipus's two travels.
    - Cumulative-state preconds satisfied at each step.
    - Final state has dead(sphinx) + knows(oedipus, riddle_answer).
    - S3P14 ordering pin: defeat_by_riddle's first precondition IS knows.
    - Infeasibility variant: remove oracle's knowledge → no_plan_found.
    - Visited-guard firings bounded (< 200).
  - `TESTS` list updated.

Expected test count: ~10-12 new tests; full stage-3 module ~51-53; full suite ~958-960.

## What a cold-start Claude should read first

1. `compilation-stage-3-sketch-01.md` — the primitive-mechanism foundation.
2. `compilation-stage-3-sketch-02.md` — typed variables + operator library growth.
3. This sketch — epistemic preconditions.
4. `prototype/tests/test_compiler_stage_3.py` — the worked example's home.
5. `compilation-sketch-01.md` OQ1 — the architectural question this spike pressure-tests.

## Honest framing

Scene 3 is a modest extension: one new type, two new operators, one new scene. The architectural question it answers (does propositional `knows(agent, fact)` suffice for epistemic-precondition planning?) is real but bounded.

**What scene 3 does NOT prove:** state-representation sufficiency for all epistemic stories. Nested knowledge, false beliefs, modal slots, and temporal epistemic reasoning remain OQ1's harder sub-questions. Scene 3 closes the easiest sub-case.

**What it DOES prove (if it succeeds):** the POCL primitive mechanism composes over epistemic preconds identically to spatial and material preconds. Knowledge is just another proposition; `learn_from` is just another operator. The planner doesn't need epistemic-specific machinery. That's a real architectural observation.

**What happens if it fails:** we diagnose. Candidates:
- **Planner issue** (precondition ordering, enumeration blowup) — fixable in the spike, per S3P14.
- **State-representation issue** (flat knowledge not expressive enough) — binds OQ1 harder.
- **Test expectation bug** — debug and re-run.

Per `project_solution_horizon.md`: scene 3 is incrementally stronger input than scene 2. A planner that handles 5 operators / 3 scenes / 4-step plans with epistemic preconditions is more convincing than one that handles 3 operators / 2 scenes / 4-step plans with only spatial-material preconditions. The delta isn't architectural (same primitive mechanism), but the coverage is wider.
