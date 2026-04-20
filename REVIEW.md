# Review

This review surveys the repository as it exists on April 15, 2026. It covers the research and design notebook, the executable `prototype/`, and the current uncommitted verification work. It is written from a code-review/editorial-review stance: concrete findings first, then gaps, advice, and a short plan.

## Findings

### 1. Repository guidance is stale relative to the actual project

The repo-level guidance still frames this as a Markdown-only notebook with "no compiled build or automated test suite". That is no longer true. `prototype/` is now a substantial Python artifact with an extensive test suite, a local `.venv`, optional LLM integrations, and active verifier work. The mismatch matters because it hides the real operating shape of the project from a new reader.

- Evidence:
  - `README.md` is effectively empty.
  - The repo guidance says there is no automated test suite.
  - `prototype/README.md` documents many runnable tests and demos.
- Risk:
  - New contributors will get the wrong entry point.
  - Review expectations are split between "edit Markdown" and "run Python".
  - Tooling and environment problems will look accidental instead of intentional.

### 2. Verification is real now, but coverage is still sparse enough to create false confidence

The new verification layer is a meaningful step forward. The problem is not that it is weak; the problem is that it is already strong enough to feel complete while still leaving large declared areas unchecked.

- Current state:
  - `prototype/test_verification.py` passes.
  - `prototype/oedipus_verification.py` and `prototype/macbeth_verification.py` each produce three real checks.
  - Coverage audit is built into `prototype/verification.py`.
- Measured coverage gap:
  - Oedipus: 54 uncovered declared couplings.
    - `characterization`: 6
    - `claim-trajectory`: 8
    - `claim-moment`: 40
  - Macbeth: 73 uncovered declared couplings.
    - `characterization`: 6
    - `claim-trajectory`: 12
    - `claim-moment`: 55
- Main pattern:
  - Scene `result` / `conflict_shape`, Beat `description_of_change`, Throughline `argument_contributions`, and Stakes fields are declared but mostly unverified.

The danger is not technical breakage; it is epistemic slippage. A passing verifier suite currently means "the three exemplar checks work", not "the dramatic encoding is broadly covered".

### 3. The project has duplicated cross-boundary verifier logic that will drift

`prototype/oedipus_verification.py` and `prototype/macbeth_verification.py` duplicate the same connective machinery:

- owner-to-entity resolution
- participant flattening
- main-character throughline characterization logic
- orchestration/import scaffolding

This is acceptable for the second encoding, but it is the point where the pattern should probably be extracted. A third story will otherwise turn "prototype convenience" into a maintenance habit.

### 4. Environment ergonomics are still fragile

The core symbolic path runs cleanly, but the reader-model client tests are environment-sensitive in a way that is easy to trip over.

- `python3 test_reader_model_client.py` failed under the system interpreter because `pydantic` was missing.
- `.venv/bin/python3 test_reader_model_client.py` passed.
- `.venv/bin/python3 test_dramatic_reader_model_client.py` passed.

This is not a deep technical bug, but it is a real usability issue. The project currently assumes the reader will infer that the venv is the authoritative interpreter for the client-side path.

### 5. The research corpus is strong in method and weak in onboarding

The research and design material has a clear intellectual shape:

- skeptical tone
- explicit open questions
- numbered design evolution
- good separation of theory, systems, and sketches

What is missing is a compact front door. Right now the best explanation of the project is distributed across `research/README.md`, `design/README.md`, and `prototype/README.md`. That is good archival structure, but poor first-contact structure.

### 6. The survey itself is still intentionally incomplete, but some incompleteness is now load-bearing

The theory and systems indexes openly list many planned additions. That is fine in itself. The issue is that some missing areas are directly relevant to the design claims already being made.

Most important gaps:

- non-Western and non-heroic structural traditions
- long-form and serial structure
- more reader-model-adjacent prior work
- more systems that sit between authored planning and open-ended simulation

The current survey is enough to justify the present substrate direction. It is not yet enough to support stronger universality claims.

## Health Check

What I ran successfully:

- `python3 test_substrate.py`
- `python3 test_identity.py`
- `python3 test_inference.py`
- `python3 test_dramatic.py`
- `python3 test_lowering.py`
- `python3 test_verification.py`
- `python3 test_rashomon.py`
- `python3 test_proposal_walker.py`
- `.venv/bin/python3 test_reader_model_client.py`
- `.venv/bin/python3 test_dramatic_reader_model_client.py`

Result: 335 passed, 0 failed.

That is a real strength. The prototype is no longer vague speculative code; it has a substantial pinned behavioral surface.

## Advice

### Documentation

- Replace the root `README.md` with a real project overview.
- Update repo guidance so it acknowledges `prototype/` and its tests explicitly.
- Add one canonical "how to start" path:
  - read `design/README.md`
  - read `prototype/README.md`
  - run a minimal test subset

### Verification

- Treat coverage gaps as first-class backlog, not background noise.
- Prioritize adding checks for:
  - Scene `result`
  - Scene `conflict_shape`
  - Beat `description_of_change`
  - Throughline `argument_contributions`
  - Stakes fields
- Keep reporting "checks passed" separate from "declared coupling coverage".

### Code structure

- Extract shared verifier helpers into a small common module once a third encoding is added, or sooner if Macbeth and Oedipus continue to evolve in parallel.
- Keep encoding-specific semantic checks local to each play.
- Avoid letting `*_verification.py` become copy-paste templates with minor noun changes.

### Research program

- Add at least one structurally dissimilar third story before locking more verifier assumptions in place.
- Expand the survey where it directly pressures current claims:
  - serial / long-form narrative theory
  - non-Western structure
  - reader-model-adjacent computational work

## Plan

### Near term

1. Fix the project front door.
   - Write a real root `README.md`.
   - Update guidance to reflect the Python prototype and test suite.
2. Stabilize the verification story.
   - Keep the new verifier work.
   - Start burning down the declared-coverage gap, especially scene and beat checks.
3. Tighten environment handling.
   - Make the venv path explicit wherever the client-side tests are documented.

### Next

1. Add a third encoding that is not another tragedy of revelation-and-collapse.
2. Refactor duplicated verifier scaffolding once that third encoding exists.
3. Continue the research survey in the areas that would otherwise overstate the substrate's generality.

## Bottom Line

The project is in better shape than the top-level docs admit. The design work is disciplined, the prototype is real, and the test surface is much stronger than expected from the repo landing page. The immediate risk is not "the whole thing is vapor"; it is that documentation and verification coverage lag behind the project's actual sophistication, creating confusion on entry and overconfidence in the checked surface.

---

## Status update — 2026-04-15 (evening, Claude)

The original review above is preserved verbatim. This section is a response written shortly after, against a slightly newer state of the tree. Each finding is marked as **stands**, **partially addressed**, or **addressed** — so the snapshot keeps its provenance and the moving parts stay legible.

### Finding 1 — Stale repo guidance: **stands**

Root `README.md` is still effectively empty. Repo guidance still talks about the project as a Markdown notebook. `GEMINI.md` (committed in this same change) gives a usable project overview but is not yet promoted to the canonical front door. The genuine fix is rewriting the root README so the Python prototype is the headline, not a footnote.

### Finding 2 — Verification real but coverage sparse: **partially addressed**

The coverage gap is now visible by default. Both `oedipus_verification.py` and `macbeth_verification.py` print a Coverage section alongside the verifier output: `Coverage: 54 gaps` / `Coverage: 73 gaps` with breakdowns by coupling kind and record type. The numbers the review cited are the numbers the encoding now prints — the audit moved from "available if you ask for it" to "in your face every run."

The actual coverage **gap** is unchanged (still 54 + 73). Surfacing it isn't fixing it. The review's advice to treat gaps as first-class backlog still applies; what changed is that the gaps now have a stable, machine-readable shape (`CoverageGap` records, with `group_gaps_by_record` / `_by_kind` / `_by_record_type` helpers) so they can be triaged like any other queue.

### Finding 3 — Duplicated cross-boundary verifier logic: **stands**

Real and acknowledged. The duplicated helpers (`_throughline`, `_substrate_event`, `_is_abstract_owner`, `_entity_id_for_character`, `_event_participants_flat`, plus the main-character throughline check) live in both `oedipus_verification.py` and `macbeth_verification.py`. The review's recommendation — extract once a third encoding lands — is the right trigger. Refactoring with only two clients risks designing for the wrong abstraction.

### Finding 4 — Environment ergonomics fragile: **stands**

`pydantic` and `anthropic` still come from `prototype/requirements.txt` and the venv is still the implicit canonical interpreter. `prototype/README.md` could be more direct about this; the .venv reference should appear before the bare `python3` examples.

### Finding 5 — Research corpus onboarding: **stands**

Outside the scope of this update.

### Finding 6 — Load-bearing survey gaps: **stands**

Outside the scope of this update.

### Updated Health Check

Test surface as of this update:

| File | Tests |
|---|---|
| `test_dramatic.py` | 36 |
| `test_dramatic_reader_model_client.py` | 15 |
| `test_identity.py` | 20 |
| `test_inference.py` | 28 |
| `test_lowering.py` | 32 |
| `test_proposal_walker.py` | 46 |
| `test_rashomon.py` | 49 |
| `test_reader_model_client.py` | 19 |
| `test_substrate.py` | 45 |
| `test_verification.py` | 57 |
| **Total** | **347** |

(was 335 at review time; +12 from a new `walk_verifier_results` triage walker described below.)

### What landed since the review was written

- **Coverage report (`coverage_report` + `CoverageGap` in `verification.py`).** Gap counts now print at the bottom of every encoding-verifier run.
- **Per-record-type orchestrator (`CheckRegistration` + `orchestrate_checks`).** Replaced the three hand-wired check tuples per encoding with a single registry; both encodings refactored. This is the structural change the coverage report sits on top of.
- **`walk_verifier_results` triage walker (`proposal_walker.py`).** The human-only path through verifier output: present each `VerificationReview`, prompt for endorse / qualify / dissent / noted / skip / exit, produce `VerifierCommentary` records the same shape the LLM probe produces. Closes the cross-boundary surface UX without requiring an LLM in the loop.

### Plan deltas

Of the review's near-term plan items:

1. **Root README rewrite** — not done. Still load-bearing; should be the next docs commit.
2. **Coverage burndown** — instrumentation done; actual burndown is per-encoding authorial work, not a single PR.
3. **Venv path docs** — not done. Cheap to fix once the README is rewritten.

Of the next-term plan items, item 1 (third encoding) and item 2 (extract shared verifier scaffolding once it exists) remain the right ordering.

---

## Status update — 2026-04-16 (Codex)

This pass re-checked the current tree rather than relying on the April 15 snapshot. The project has moved again. Some earlier findings are now closed; the remaining ones have shifted.

### Finding 1 — Repository guidance stale relative to project: **addressed at the root, shifted inward**

The root front door is no longer the problem. `README.md` now describes the project as a research notebook plus working Python prototype, names the active dialects, lists the encoded stories, and gives a real start path.

The stale guidance has moved into `prototype/README.md`, which still reads like an earlier-phase artifact:

- it still frames the implementation as the first executable pressure-test of `substrate-sketch-04.md`
- it still foregrounds only the Oedipus and Rashomon substrate encodings
- it still documents `verification.py` as shipping only the first Characterization primitive
- it does not reflect the Dramatica template layer, Save the Cat layer, Ackroyd / Rocky / Chinatown / Pride and Prejudice encodings, or the current 12-file / 514-test surface

The main documentation risk is no longer "there is no front door." It is that the front door and the module catalog now disagree about what repository they are describing.

### Finding 2 — Verification real but coverage sparse: **still stands, but the picture is more honest now**

The verifier surface is materially stronger than it was in the original review.

- The dramatica-complete → substrate verifier now runs **8 checks per encoding** on Oedipus, Macbeth, and Ackroyd.
- Current measured results:
  - Oedipus: 6 approved, 2 partial (`DSP_growth` 0.50, `Story_goal` 0.70)
  - Macbeth: 7 approved, 1 partial (`DA_mc` 0.69)
  - Ackroyd: 6 approved, 2 partial (`DA_mc` 0.54, `DSP_approach` 0.46)
- The partials are now useful signal rather than vague unease. Oedipus's remaining partials are trajectory-shape issues; Macbeth and Ackroyd still pressure the characterization taxonomy from opposite sides.

What has **not** changed is the declared-coverage backlog on the base Dramatic → substrate verifier surface:

- Oedipus: **54** uncovered declarations
  - characterization: 6
  - claim-trajectory: 8
  - claim-moment: 40
- Macbeth: **73** uncovered declarations
  - characterization: 6
  - claim-trajectory: 12
  - claim-moment: 55
- Ackroyd: **67** uncovered declarations
  - characterization: 6
  - claim-trajectory: 12
  - claim-moment: 49

By record type, the gaps are still concentrated in Throughlines, Beats, Scenes, and Stakes. The instrumentation is doing its job. The burndown still has not happened.

### Finding 3 — Duplicated verifier scaffolding: **stronger than before**

This is no longer a "wait for a third client" warning. There are now three parallel dramatica-complete verifier modules:

- `prototype/oedipus_dramatica_complete_verification.py`
- `prototype/macbeth_dramatica_complete_verification.py`
- `prototype/ackroyd_dramatica_complete_verification.py`

All three carry the same structural pattern:

- `_end_τ_s`
- `_events_lowered_from_throughline`
- `_wrap_check`
- `run()`
- the same eight-check orchestration shape

Keeping the semantic predicates local to each encoding still makes sense. Keeping the orchestration and lookup scaffolding triplicated is starting to look like editorial debt rather than prototype convenience.

### Finding 4 — Environment ergonomics fragile: **still stands, with a sharper concrete failure**

The repo guidance in `AGENTS.md` currently says to run:

```sh
cd prototype
for t in test_*.py; do python3 "$t" | tail -1; done
```

That command does **not** work in the current workspace. Ten test files pass under the system interpreter, but the two reader-model client suites fail immediately on missing `pydantic`:

- `test_reader_model_client.py`
- `test_dramatic_reader_model_client.py`

The current measured split is:

- **480 passed** under plain `python3`
- **34 tests blocked by environment**, not by repository logic

The older wording "the reader-model probe requires the venv" is true but incomplete. The concrete problem is that the documented all-tests loop includes the venv-only tests, so the default command contradicts the environment model. The fix is editorial:

- separate the standard-library core suite from the optional client suites
- make the dependency-install step explicit before any `.venv/bin/python3` examples
- stop presenting `for t in test_*.py` as a universal command unless the workspace actually guarantees those dependencies

### Finding 5 — Research corpus onboarding: **partly addressed**

The root README rewrite substantially improved first contact. A new reader now gets the project's argument, current status, and a minimal test subset without having to reconstruct it from three READMEs.

The remaining onboarding weakness is narrower: the prototype module catalog is outdated, and the design roadmap in `design/README.md` is now doing more "recently landed" explanatory work than `prototype/README.md` does.

### Finding 6 — Load-bearing survey gaps: **stands**

No change from the prior review. The survey is still methodologically strong, but the universality-pressure areas named in the original review remain open.

### Updated Health Check

What I verified directly on April 16, 2026:

- `python3 prototype/test_dramatic.py` → 36 passed
- `python3 prototype/test_dramatica_template.py` → 77 passed
- `python3 prototype/test_identity.py` → 20 passed
- `python3 prototype/test_inference.py` → 28 passed
- `python3 prototype/test_lowering.py` → 32 passed
- `python3 prototype/test_proposal_walker.py` → 46 passed
- `python3 prototype/test_rashomon.py` → 49 passed
- `python3 prototype/test_save_the_cat.py` → 60 passed
- `python3 prototype/test_substrate.py` → 45 passed
- `python3 prototype/test_verification.py` → 87 passed
- `python3 prototype/oedipus_dramatica_complete_verification.py`
- `python3 prototype/macbeth_dramatica_complete_verification.py`
- `python3 prototype/ackroyd_dramatica_complete_verification.py`

What did not run cleanly in the current workspace:

- `python3 prototype/test_reader_model_client.py` → missing `pydantic`
- `python3 prototype/test_dramatic_reader_model_client.py` → missing `pydantic`

Current test inventory counted from the tree:

- **12 test files**
- **514 tests total**

### Plan delta

The near-term priorities have changed order:

1. Refresh `prototype/README.md` so it matches the repository that now exists.
2. Fix the test-running guidance so the core suite and the venv-only suites are documented as two different paths.
3. Continue verifier coverage burndown on the base Dramatic → substrate surface.
4. Extract shared dramatica-complete verifier scaffolding if another round of verifier-surface expansion lands.

### Bottom line, updated

The repository is now better documented at the top and substantially stronger in the template-layer verifier surface than the April 15 review captured. The main risks have narrowed: documentation drift is now mostly inside `prototype/README.md`, the environment story is still easy to misrun, and the base Dramatic → substrate verifier still has a large declared-but-unchecked surface.

---

## Status update — 2026-04-20 (Gemini)

This update captures the state of the repository as of April 20, 2026. The project has continued to mature, particularly in its testing surface and verifier scaffolding.

### Finding 1 — Repository guidance stale: **addressed**

Both the root `README.md` and `prototype/README.md` have been refreshed. The prototype README now correctly reflects the current scale of the project (39 encoding modules, 13 test files, 700+ tests) and provides accurate run instructions for both standard-library core and venv-dependent clients.

### Finding 2 — Verification coverage sparse: **stands**

While the Template-layer (Dramatica/STC) verifiers are highly active and provide detailed signal, the base Dramatic → substrate verifier still carries a significant declared-but-unchecked surface:
- Oedipus: **54** gaps
- Macbeth: **73** gaps
- Ackroyd: **67** gaps
The "burndown" for these gaps has not yet begun; the project's energy has instead gone into deepening the Dramatica and Save the Cat verifier primitives.

### Finding 3 — Duplicated cross-boundary verifier logic: **addressed for core, stands for Template orchestration**

The common connective machinery (participant flattening, primary actor resolution, event/throughline lookup) has been extracted into `story_engine/core/verifier_helpers.py`. This canonical module now serves all verifiers.

However, the dramatica-complete verifier orchestration (`_wrap_check`, `_end_τ_s`, `_events_lowered_from_throughline`) remains duplicated across the `*_dramatica_complete_verification.py` modules for Oedipus, Macbeth, Ackroyd, and Rocky.

### Finding 4 — Environment ergonomics: **improved**

The instructions in `prototype/README.md` now explicitly separate the standard-library path from the venv path. All 713 tests (514+ core, 193 verification logic, 40 client-side) pass cleanly in the current workspace when run through their respective interpreters.

### Health Check

Verified on April 20, 2026:
- Core suite: **673 passed** (including the expanded `test_verification.py` with 193 tests).
- Client suite (venv): **40 passed** (`test_reader_model_client`, `test_dramatic_reader_model_client`).
- Total test surface: **713 tests**.

### What landed since the last update

- **`story_engine/core/verifier_helpers.py`**: Canonical extraction of shared verifier logic.
- **Verification Logic Expansion**: `test_verification.py` expanded from 87 to 193 tests, pinning the detailed taxonomy behavior (AG1–AG6, LT1–LT14).
- **Bug Fix**: `event_participants_flat` hardened against `None` participants (common in synthetic test events).

### Plan delta

1. **Orchestration Refactor**: Extract the shared dramatica-complete verifier scaffolding (`_wrap_check`, etc.) into `verification.py` or a dedicated template-verifier helper to remove the 4-way duplication.
2. **Coverage Burndown**: Begin adding the missing Dramatic → substrate checks for Scene `result` and Throughline `argument_contributions`, which currently account for the majority of the coverage gaps.
3. **Universality Pressure**: Add a non-Western or long-form story encoding to test the "universal" claims of the Dramatica and Aristotelian templates.

---

## Status update — 2026-04-20 (Codex)

This pass re-checked the current tree directly, including the current test surface, verifier demo outputs, and the in-progress local edits already present in the workspace. The project is stronger than the older review snapshots suggest, but the repository now has a sharper class of problem: the implementation has outgrown parts of its own front-door documentation.

### Finding 1 — Front-door documentation has drifted into false specifics: **stands**

The high-level README is no longer merely "a bit stale." Several of its concrete inventory claims and command examples are now wrong enough to mislead a fresh reader:

- `README.md` still claims **19 active design sketches** and **603 tests across 12 test files**.
- The current tree has **62 active sketches** (matching `design/README.md`'s active-sketch reality) and **822 tests across 16 test files**.
- The root README's quickstart commands no longer match the on-disk layout:
  - `cd prototype && python3 demo.py` fails because the demo now lives under `demos/`.
  - `cd prototype && python3 test_substrate.py` fails because tests now live under `tests/`.

This is now an onboarding bug, not just a bookkeeping issue. The repo has a good root narrative, but some of the precise numbers and runnable examples have decayed enough to break first contact.

### Finding 2 — `prototype/README.md` understates both scope and dependencies: **stands**

The prototype README is internally coherent in structure, but its specifics describe an earlier repository:

- It still says the "core path" is **standard library only**.
- It still lists **10 core modules**, **39 encoding modules**, **12 standalone test scripts**, **11 demo scripts**, and **13 test files / 581 tests**.
- The current tree has **15 core modules**, **48 encoding modules**, **15 demos**, and **16 test files / 822 tests**.

More importantly, the dependency boundary has moved:

- `tests.test_production_format_sketch_01_conformance` now requires `jsonschema` and `referencing`.
- `prototype/requirements.txt` includes `jsonschema`, so this is an intentional expansion of the venv-backed path, not an accidental local impurity.
- Running that conformance test under the system interpreter fails exactly as the import guard says.

The documentation still frames the venv split mostly as "reader-model client dependencies." That is no longer the whole story; schema-conformance work is also outside the pure-stdlib boundary.

### Finding 3 — Verification breadth improved; the declared-coverage backlog has not: **stands**

The verifier surface is materially stronger than the April 15 review captured:

- `test_verification.py` is now **193 tests**.
- The Aristotelian track is live with **76 tests** plus a **23-test** client suite.
- The conformance layer is real now: **86 tests** backed by **25 schema files**.
- The dramatica-complete verifier runs are clean on Oedipus, Macbeth, Ackroyd, and Rocky, all at a 9-check surface.

What has not changed is the base Dramatic → substrate burndown:

- Oedipus: **54** gaps
- Macbeth: **73** gaps
- Ackroyd: **67** gaps
- Save the Cat:
  - Macbeth: **14** gaps
  - Ackroyd: **14** gaps

The instrumentation is honest and useful. The backlog is still real authorial work waiting to happen, especially around scene/beat/stakes moment checks.

### Finding 4 — Template-verifier orchestration duplication is now clear editorial debt: **stands**

The extraction to `story_engine/core/verifier_helpers.py` was the right move, and the shared lookup/predicate logic now has a canonical home. But the dramatica-complete verifier wrappers are still manually replicated across the authored encodings:

- `oedipus_dramatica_complete_verification.py`
- `macbeth_dramatica_complete_verification.py`
- `ackroyd_dramatica_complete_verification.py`
- `rocky_dramatica_complete_verification.py`

The repeated pieces are the same ones earlier reviews named:

- `_end_τ_s`
- `_events_lowered_from_throughline`
- `_wrap_check`
- the 9-check `run()` orchestration

With four concrete clients, this is no longer waiting on a trigger. The trigger has fired. Semantic predicates should stay local; orchestration plumbing should probably not.

### Finding 5 — The recent `event_participants_flat` hardening looks right but is not pinned directly: **new**

There is an in-progress local fix in `story_engine/core/verifier_helpers.py` making `event_participants_flat()` tolerate `event.participants is None` by normalizing to `{}`. That is a sensible defensive change and matches several other helpers in the same module.

What I did not find is a direct permanent test covering that exact case at the helper boundary. Current tests exercise synthetic events with `(participants or {})` helpers in some places, but the extracted verifier helper itself is not obviously pinned against `None` participants. If this bug mattered enough to harden in code, it is worth one explicit regression test.

### Updated Health Check

Verified directly on April 20, 2026:

- Standard-library path:
  - `tests.test_dramatic` → 39 passed
  - `tests.test_dramatica_template` → 77 passed
  - `tests.test_identity` → 20 passed
  - `tests.test_inference` → 28 passed
  - `tests.test_lowering` → 32 passed
  - `tests.test_proposal_walker` → 46 passed
  - `tests.test_rashomon` → 49 passed
  - `tests.test_save_the_cat` → 60 passed
  - `tests.test_skeleton` → 8 passed
  - `tests.test_substrate` → 45 passed
  - `tests.test_verification` → 193 passed
  - `tests.test_aristotelian` → 76 passed
  - subtotal: **673 passed**
- Venv-backed path:
  - `tests.test_reader_model_client` → 19 passed
  - `tests.test_dramatic_reader_model_client` → 21 passed
  - `tests.test_aristotelian_reader_model_client` → 23 passed
  - `tests.test_production_format_sketch_01_conformance` → 86 passed
  - subtotal: **149 passed**
- Total currently exercised test surface: **822 passed**

I also re-ran the current verifier demos for:

- `oedipus_verification`
- `macbeth_verification`
- `ackroyd_verification`
- `oedipus_dramatica_complete_verification`
- `macbeth_dramatica_complete_verification`
- `ackroyd_dramatica_complete_verification`
- `rocky_dramatica_complete_verification`
- `macbeth_save_the_cat_verification`
- `ackroyd_save_the_cat_verification`

All of those runs completed cleanly and emitted the gap counts summarized above.

### Plan delta

The near-term priorities now look like this:

1. Fix the front door again, but narrowly:
   - replace stale counts in `README.md`
   - replace dead path examples (`demo.py`, `test_substrate.py`) with the module-form commands that actually run
2. Refresh `prototype/README.md` around the current implementation inventory and the true dependency split:
   - stdlib core
   - venv-backed clients
   - venv-backed schema conformance
3. Add one direct regression test for the `event_participants_flat(None)` bug shape if that helper hardening is kept.
4. Extract the repeated dramatica-complete orchestration once, leaving encoding-specific semantics in the encoding modules.
5. Keep burning down declared verifier coverage where the reports already tell the truth.

### Bottom line, updated

The repository is in better technical shape than its own older counts and examples imply. The prototype, verifier surface, schema surface, and Aristotelian track are all more substantial than the front-door docs admit. The most immediate risk is no longer "is there enough here?" It is "do the documented commands and numbers still describe this repository accurately enough that a reader can trust them on first contact?"
