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
