# State of play — sketch 14

**Status:** active
**Date:** 2026-05-22
**Supersedes:** [state-of-play-13](state-of-play-13.md)

Small-delta refresh marking **compilation-stage-3-sketch-04**
landing. One commit since state-of-play-13, but a methodologically
interesting one: the **design-first → implementation-falsifies
rhythm operated at sketch-design scale** this round, with the
sketch's original framing replaced during implementation by a
simpler mechanism that the analytical finding pointed at.

**One commit since state-of-play-13** (`686b031`), one month
after SoP-13. The project resumed from a month-long break to
land the recommended next step from SoP-13's "what's next" list
(the compiler stage-3 sketch-04 candidate). The same session
also extracted a scene-fixtures module (`compiler_scenes.py`)
that had been untracked since the sketch-03 work landed.

## Headline — two load-bearing claims

### 1. Sketch-04 lands; precondition ordering is now a planner concern, not a schema-author concern

`compilation-stage-3-sketch-04` (`686b031`) closes the largest
remaining fragility in the stage-3 planner. The sketch-03 spike
surfaced the symptom concretely: when `defeat_by_riddle` lists
its `at` preconditions before the `knows` precondition, the
planner produces a valid but longer (5-step) plan in which the
Oracle travels to Oedipus instead of Oedipus traveling to the
Oracle. The 4-step "mythologically correct" plan was only found
under the S3P14 ordering discipline (knows-before-at). Sketch-04
removes that authoring discipline: schema authors can now order
preconditions naturally and the planner finds the optimal plan
either way.

The mechanism that landed is a **precondition-risk sort** in
`_plan_with_bindings`: sort the goal operator's grounded
preconditions by `max(len(del_effects))` across operators whose
`add_effects` can establish them, ascending, with original schema
order as the tie-break. Safer preconditions (achievable by ops
with no del_effects, e.g. `learn_from`) get satisfied first;
riskier ones (e.g. `travel`, which deletes `at(AGENT, FROM)`)
get deferred.

The sketch's original framing was a **minimal threat-resolution
layer** (causal-link + demote primitives). Implementation
revealed the framing was insufficient — see claim 2.

This retires the S3P-OQ10 banked open question to "performance
hint only," not a correctness requirement.

### 2. The design-first → implementation-falsifies rhythm operated at sketch-design scale this round

Per `feedback_sketch_implement_rhythm_falsifies.md`:
"implementation regularly falsifies one [claim]." The rhythm has
operated at three arena scales now:

- **Probe-run scale** (Hamlet sketch-03; Lear sketch-05) — design
  hypotheses about which forcing functions will surface get
  falsified by probe data. SoP-13 documented this as the
  reproducible pattern.
- **Implementation-detail scale** (countless sketches) — design
  claims about specific mechanisms get refined during impl.
  Standard rhythm.
- **Sketch-design scale (new this round)** — sketch-04's central
  mechanism (threat detection + demotion) was analytically
  shown insufficient during implementation; the simpler
  precondition-risk sort replaced it as the load-bearing
  mechanism. The threat-resolution primitives ship correct but
  inert.

The analytical finding is the load-bearing methodological output:
the 5-step Oracle-travel plan contains **zero detectable
threats** under any reasonable causal-link semantics. Step 1
(travel d→t) deletes `at(oed, d)`, but the only link protecting
`at(oed, d)` runs from step 0 to step 1 — and step 1 IS the
consumer, not a third party caught strictly between. No
positional repair (demotion, promotion, or any in-place swap)
can transform the 5-step plan into the 4-step plan; the
4-step plan emerges from a *different sequence of variable
bindings*, not from rearranging steps. The actual fix is
upstream — change which preconditions get attempted first.

This is the third arena. Future sketches should explicitly
budget for the possibility that the proposed mechanism gets
falsified during implementation and resist sunk-cost-attachment
to the named approach.

---

## What is built — delta from sketch-13

### One commit, four files

- `design/compilation-stage-3-sketch-04.md` (new, 153 lines) —
  the sketch, updated post-impl to reflect what landed rather
  than the original draft framing. Includes an explicit
  "Analytical finding" section walking through the 5-step plan's
  links and del-effects to show why threat resolution alone
  could not have closed S3P-OQ10.
- `prototype/story_engine/core/compiler_scenes.py` (new, 246
  lines) — scene + operator fixtures (TRAVEL / KILLS / ACQUIRE
  / LEARN_FROM / DEFEAT_BY_RIDDLE + the three scene start-states
  + the two goal builders) extracted from
  `test_compiler_stage_3.py` for reuse.
- `prototype/story_engine/core/compiler_stage_3.py` (+316/-37) —
  sketch-04 implementation: `_precondition_risk` + sort in
  `_plan_with_bindings`; `CausalLink` record; `detect_threats`;
  `try_repair_by_demoting`; `try_repair_by_promoting`;
  sub-link offset re-indexing in `_achieve`. The sort is the
  principal load-bearing change. The other primitives are
  mathematically correct but inert in the current test corpus.
- `prototype/tests/test_compiler_stage_3.py` (+57/-235) — imports
  from `compiler_scenes`; new forcing test
  `test_scene_3_bad_precondition_order_still_finds_optimal_plan`
  with the bad-ordered operator as the **goal operator** (not
  merely in the library — `plan_to_goal` iterates
  `goal.operator.preconditions`, so only the goal's ordering
  exercises the bad-ordering path).

### Test surface

- **53 stage-3 tests** (up from 52). +1 forcing test.
- **889 stdlib core tests pass** across 14 files. (Cf. SoP-13's
  992 figure included reader-model + venv-required tests; the
  stdlib core is the AGENTS.md-required sweep and is sketch-04's
  regression surface.)

### Open question explicit-bookkeeping

Sketch-04 adds four open questions (S4P-OQ1 through S4P-OQ4) and
weakens S3P-OQ10 to "performance hint only." S4P-OQ4 is the
notable one: **when should the inert threat-resolution
scaffolding (S4P2–S4P4) be removed if no forcing scene activates
it?** Per AGENTS.md "no speculative generalization," removal is
the default after one or two more increments without invocation;
demote/promote are easy to re-introduce when earned.

---

## What the analytical finding revealed about sketch design itself

The sketch-04 first-draft framing ("minimal threat resolution")
was a reasonable hypothesis — POCL threat resolution IS the
classical mechanism for precondition ordering. The
hypothesis was wrong because regression-based planning commits
to variable bindings *before* the threat structure is visible:
by the time step 1 (travel d→t) is added, the plan has already
committed to learn_from happening at thebes_gates (because oed
is at thebes_gates by that point), and the alternative
binding (learn_from at delphi) is never in the plan to be a
target of demotion.

The classical POCL threat-resolution literature works under
*least-commitment partial-order* search — open preconditions on
an agenda, no early binding commitments. Translating that
machinery into a regression planner with eager commitment is
where the analytical mismatch lives. The sketch-04 first draft
silently inherited the classical framing without re-examining
whether the underlying planner shape supported it.

Recorded for future sketches: when adopting a mechanism by name
from prior literature, verify the underlying control-flow shape
supports it before committing to the named mechanism in the
sketch. Threat resolution is **a real and useful primitive** —
just not the one that closes S3P-OQ10 in this planner's shape.

---

## What's next (research AND production)

### Research track

Compared to SoP-13's "what's next" list:

1. **OQ-LEAR-4 second-site search.** Unchanged from SoP-13.
   Subplot-with-own-peripeteia tragedy. Webster's *Duchess of
   Malfi* / Marlowe's *Edward II* / Tourneur's *Revenger's
   Tragedy* candidates.
2. **OQ-LEAR-8 closure paths.** Unchanged from SoP-13.
3. **OQ-LEAR-5 / OQ-AP1 convergence search.** Unchanged.
4. **Compiler stage-3 sketch-05 candidate** — pressure-test the
   precondition-risk sort. Per sketch-04 S4P-OQ3: find a forcing
   scene where the heuristic over-defers a precondition that, in
   the specific state, doesn't actually conflict. If found, the
   next escalation is **insertion-search**: try satisfying each
   precondition at each intermediate position of the existing
   plan, pick the position with the shortest sub-plan.
5. **Compiler stage-3 richer-epistemic alternative** (S3P-OQ11
   from SoP-13's list #6) — unchanged. Nested knowledge / modal
   slots / false belief / temporal indexing.
6. **Multi-session arc candidates** — unchanged from SoP-13.
7. **Compiler stage-3 inert-scaffolding decision** (new). Per
   S4P-OQ4: after one or two more compiler increments without
   the threat primitives activating, remove them. Track via
   `_VISITED_GUARD_FIRES`-style telemetry if useful.

The sketch-04 candidate from SoP-13 #5 is now landed (this
SoP). SoP-13 #6 (POCL threat resolution) is the path-not-taken
this round; sketch-04 still didn't activate it. SoP-14's #4 is
the natural follow-up if a forcing case appears.

### Production track

Unchanged from SoP-13:

A. **PFS16** — Aristotelian sketch-05 schema landing.
B. **PFS17** — Dramatic dialect schemas. Gated.
C. **PFS18** — Dramatica-complete. Gated.
D. **substrate-world-fold-sketch-01** — forcing function not yet
   surfaced.
E. **Markdown-fenced author parser** (roadmap #1).
F. **Prose export round-trip starter** (roadmap #3).
G. **Goodreads import prototype** (roadmap #2).
H. **Port work** (roadmap #4).

### Recommendation

Per `feedback_research_production_alternation.md` — the last
substantive commit (`686b031`) is research mode (compiler
sketch). Next should lean production. Candidates ordered by fit:

- **PFS16 (Aristotelian sketch-05 schema landing)** — smallest
  per-record arc, follows precedent, closes the sketch-05 arc
  cleanly. Strongest production fit. Unchanged from SoP-13's
  recommendation.
- **OQ-LEAR-4 second-site search via Webster** — research,
  cross-encoding pressure target.
- **Sketch-04 stress-test (S4P-OQ3 forcing case)** — research,
  short. Would either bank a real forcing case for insertion-
  search or strengthen confidence in the sort heuristic.

Alternative (high-novelty, possibly defer): **fourth Dramatica
quad layer** (roadmap #5). Unchanged.

---

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketches-04 through -13, with one addition:

- **Sketch-design hypotheses can be falsified by implementation
  (the third rhythm-arena).** Sketches should be writable
  post-impl to reflect what landed rather than what was first
  proposed; "Revised framing" + "Analytical finding" sections
  are a legitimate part of an active sketch's body. The
  sketch-04 doc demonstrates the convention.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic.
2. This doc (`design/state-of-play-14.md`) — current state.
3. `design/state-of-play-13.md` — supersedes-link; sketch-13
   carries the compiler-feasibility-proved milestone framing,
   the dialect-corpus inventory, and the Lear/Hamlet
   probe-driven-closure pattern verification.
4. `schema/README.md` — production layer.
5. `git log --oneline b5ba0f1..HEAD` — the one sketch-04 commit
   between SoP-13 and SoP-14.
6. `design/compilation-stage-3-sketch-04.md` — the sketch as
   landed, including the Revised framing + Analytical finding
   sections that record the path-not-taken.
7. `prototype/story_engine/core/compiler_stage_3.py` — the
   POCL-spike implementation post-sketch-04. `_plan_with_bindings`
   carries the sort; `CausalLink` / `detect_threats` /
   `try_repair_by_demoting` / `try_repair_by_promoting` are
   the scaffolding primitives.
8. `prototype/story_engine/core/compiler_scenes.py` — scene
   fixtures extracted from the test file for reuse.
9. SoP-13's reading list items #6–#11 — Lear encoding, dialect
   core, prior stage-3 sketches — remain relevant under SoP-14.
