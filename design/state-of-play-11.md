# State of play — sketch 11

**Status:** active
**Date:** 2026-04-19
**Supersedes:** [state-of-play-10](state-of-play-10.md)

Cold-start orientation doc, rewritten (not amended) at the
milestone where the **third Aristotelian encoding lands**, the
**first banked scheduling-act-family seed closes**, and the
**reader-model-client shared base factors out**.

**Three commits since state-of-play-10.** Smallest inter-sketch
delta since the state-of-play series began — each commit closes
one state-of-play-10 candidate, none open new design arcs. All
three land on 2026-04-19 (the one-day cadence continues).

Grouped by arc:

- `1988222` — macbeth_aristotelian (research track). Third
  Aristotelian encoding. First corpus exercise of
  BINDING_COINCIDENT (A12) and of a non-precipitating
  ArAnagnorisisStep (A11). +4 tests. 792 → 796.
- `3cfa6ff` — scheduling-act-utterance-sketch-02 (design +
  impl). Closes the OQ2-reshaped post-SC4 Rashomon probe seed
  carried since state-of-play-04. SC6–SC10 commit a
  prose-carried substring-token convention on Lowering
  annotation.text. +11 tests. 796 → 807.
- `91afd15` — reader-model-client-base (production
  infrastructure). Three primitives factor out of the three
  reader-model clients into `core/reader_model_client_base.py`.
  807 unchanged.

**Headline.** Three load-bearing claims.

1. **The Aristotelian dialect corpus reaches three encodings
   and covers two of three canonical binding values.**
   Macbeth lands with `peripeteia_anagnorisis_binding =
   BINDING_COINCIDENT`, where Oedipus committed
   BINDING_SEPARATED. BINDING_ADJACENT remains uncovered (no
   forcing function banked). Macbeth also exercises A11's
   non-precipitating branch: AR_STEP_LADY_MACBETH_SLEEPWALKING
   carries `precipitates_main=False` — Lady Macbeth's
   character-level recognition collapses parallel to (not
   causally into) Macbeth's end-phase anagnorisis. Both
   polarities of A11 `precipitates_main` now have corpus
   coverage. The encoding ships without schema or sketch
   changes; aristotelian-sketch-02's A1–A12 surface held a
   third independent encoding clean on first contact.

2. **First banked scheduling-act-family seed closes.**
   Scheduling-act-utterance-sketch-02 (SC6–SC10) converts a
   banked forcing function (OQ2-reshaped, since sketch-04)
   into an implemented verifier-helper extension. The design
   chooses the lightest-weight path consistent with LT3's
   honest-asymmetry contract: a case-sensitive substring
   token (`"prose-carried"`) on Lowering `annotation.text`,
   detected by a new helper, threaded through the existing
   timelock-consistent weak-fallback comment only — no
   verdict-strength lift, no schema change, no typed
   boolean. Two banked seeds remain
   (bandit-refinement MC-mediated endpoint substitution;
   OQ1-reshaped woodcutter cross-branch signature detector);
   each has its own forcing function.

3. **Factor-out discipline extends to the reader-model-client
   layer.** The conformance-module extraction (sketch-10) set
   the pattern; `reader_model_client_base.py` applies it to
   the three reader-model clients that had accreted
   near-identical DroppedOutput dataclasses, SYSTEM_PROMPT
   opening sentences, and Anthropic parse-call boilerplate.
   Three primitives share; per-dialect output schemas /
   build_user_prompt helpers / classify-and-translate stay
   unshared (intentional, documented in the base module
   docstring — dialect-specific content without duplicated
   structure to forcing-function a factor-out). Zero
   behavior delta; byte-identical SYSTEM_PROMPT rendering
   verified; source-compatible re-export preserves every
   per-client `from <client> import DroppedOutput` call
   site.

Re-write this sketch (don't amend — write sketch-12) at the
next milestone.

---

## What is built — delta from sketch-10

### The corpus (seventh full Aristotelian encoding slot)

- `prototype/story_engine/encodings/macbeth_aristotelian.py`
  (new). AR_MACBETH_MYTHOS: complex plot, 22 central events,
  three phases (8 / 9 / 5), complication=E_duncan_killed
  (first of middle), denouement=E_sleepwalking (last of
  middle), peripeteia=anagnorisis=E_macduff_reveals_birth,
  `aims_at_catharsis=True`. Unity of time/place not asserted
  (118 τ_s-units; multiple locations). Two ArCharacter
  (AR_MACBETH credulity-toward-equivocation; AR_LADY_MACBETH
  unsex-me-here). One ArAnagnorisisStep
  (AR_STEP_LADY_MACBETH_SLEEPWALKING, τ_s=13,
  `precipitates_main=False`). No ArMythosRelation (single-
  mythos).
- `prototype/tests/test_aristotelian.py` +4 tests (72 → 76):
  verifies-clean; records-shape; binding-is-coincident;
  chain-non-precipitating.

Aristotelian dialect corpus (post-sketch-11): three encodings
— oedipus, rashomon, macbeth. Two use anagnorisis
(oedipus, macbeth — one precipitating, one non-precipitating);
two use multiple mythoi (none — Rashomon is four-mythos with
ArMythosRelation `contests`, but the others are single-mythos).
Binding coverage: SEPARATED (oedipus), COINCIDENT (macbeth),
ADJACENT uncovered.

### The verifier layer (SC6–SC10 prose-carried signal)

- `prototype/story_engine/core/verifier_helpers.py`:
  - New `PROSE_CARRIED_MARKER = "prose-carried"` constant.
  - New `_prose_carried_lowerings(lowerings)` helper; defensive
    against non-string annotation text.
  - `dsp_limit_characterization_check` gains optional
    `lowerings: tuple = ()` kwarg. Default preserves
    pre-sketch-02 behavior; existing call sites binary-
    compatible. On timelock-consistent weak-fallback (VERDICT_
    NOTED + strength=None), the comment gains a trailing
    sentence naming the Lowering id(s) and the representational
    gap. Verdict stays NOTED; strength stays None (LT3
    contract preserved).
- `prototype/story_engine/encodings/rashomon_dramatica_complete_verification.py`:
  imports `LOWERINGS_BY_STORY` from `rashomon_lowerings`;
  `_run_testimony_dsp_limit_check` threads
  `LOWERINGS_BY_STORY[story_id]` through per testimony.
- `prototype/tests/test_verification.py` +11 tests (182 → 193):
  SC6 helper (empty / match / skip / substring),
  SC7 back-compat (default empty preserves shape),
  SC8 comment specialization (timelock-consistent surfaces
  suffix; timelock-strong does not; optionlock does not),
  SC9 Rashomon end-to-end (wife gains suffix; bandit/samurai
  preserved APPROVED 0.5; woodcutter stays NOTED None with
  no suffix).

Worked-case outcomes (pre-/post-):
- Rashomon S_wife_ver: NOTED None → NOTED None + prose-carried
  suffix naming L_wife_violated.
- Rashomon S_bandit_ver / S_samurai_ver: APPROVED 0.5
  preserved (timelock-strong via requested_killing; SC8 path
  not reached).
- Rashomon S_woodcutter_ver: NOTED None unchanged (no
  prose-carried annotation in its LOWERINGS_BY_STORY subset).
- Rocky: APPROVED 1.00 unchanged (timelock-strong via
  scheduled_fight — SC8 not reached even though L_ice_skating
  carries prose-carried text, correct by SC10 scope).
- Oedipus / Macbeth / Ackroyd: Optionlock paths unchanged.

### The production infrastructure (reader_model_client_base)

`prototype/story_engine/core/reader_model_client_base.py`
(new, 154 lines). Three primitives:

- `DroppedOutput` frozen dataclass. Canonical shape
  (`reason: str`, `raw: str | None`). Each client re-exports
  via `from …reader_model_client_base import DroppedOutput`;
  every existing `from <client> import DroppedOutput` call
  site sees the same class (isinstance / construction /
  equality source-compatible).
- `SYSTEM_PROMPT_OPENING` string constant. Shared two-sentence
  opener (reader-model role + pointer to reader-model-sketch-01).
  Each client composes its full SYSTEM_PROMPT as an f-string
  prefix; post-rendering text is byte-identical to
  pre-refactor (verified: substrate 5694 / dramatic 5665 /
  aristotelian 6523 chars).
- `invoke_parse_helper()`. The ~25-line Anthropic
  `messages.parse` boilerplate each client repeated: dry-run
  printing, lazy client construction from env, the exact
  parse-call shape (thinking=adaptive, cache-controlled system
  block, single user message, caller-supplied output_format).
  Each client's `invoke_*_reader_model` calls the helper,
  then applies its own classify/translate post-processing on
  raw output.

Intentionally not factored (documented in the base module's
docstring): per-dialect record-to-dict helpers, Pydantic
output schemas, `build_user_prompt` functions, `_classify_*` /
`_translate_*` helpers, result dataclasses
(ReaderModelResult / DramaticReaderModelResult /
AristotelianReaderModelResult). Each carries dialect-specific
fields or content types; sharing would require inventing
machinery without a forcing function.

Line deltas (three clients + new base):
- `reader_model_client.py`: 927 → 900 (−27)
- `dramatic_reader_model_client.py`: 1133 → 1109 (−24)
- `aristotelian_reader_model_client.py`: 1151 → 1129 (−22)
- `reader_model_client_base.py`: new +154
- Net +81; the win is single source of truth, not line count.

### Corpus audit outcomes (Tier-2 update)

Macbeth lands under the `*_aristotelian` suffix convention
(RI9); audits pick it up automatically:

- `audit_aristotelian_event_refs`: 24 records / 180 event-id
  refs clean across three paired encodings (was 20 / 132 across
  two).
- `audit_character_ref_ids`: 8 ArCharacter records clean (was
  6). AR_MACBETH and AR_LADY_MACBETH resolve against macbeth's
  20 substrate entities + 9 dramatic characters = 29-union.
- Branch-label, save-the-cat intra-story, CrossDialectRef:
  unchanged in shape (no new lowerings / verifications /
  save-the-cat records; macbeth_save_the_cat already existed
  in sketch-10).

Five audit functions total; ~1151 references resolved across
kinds (1103 sketch-10 baseline + 48 new Aristotelian
event-ref+character refs from Macbeth).

### Test suite

807 passing, +15 from sketch-10 baseline of 792. Breakdown:
+4 test_aristotelian (Macbeth); +11 test_verification (SC6–SC9);
reader-model-client-base adds zero test deltas.

---

## Shift-point — narrow but coherent

The three sketch-11 commits do not open a new layer
(sketch-10's three claims — cross-boundary schema begins;
Tier-2 audit operational; Aristotelian dialect earns
amendment sketch — still frame the project's current shape).
What they do, collectively, is advance the three active
tracks **without forcing** new scope:

- **Research track advances without schema pressure.**
  Macbeth lands clean under aristotelian-sketch-02's surface.
  Two previously-uncovered cells in the binding × precipitates
  matrix fill. The dialect's A1–A12 commitments absorbed an
  independent third encoding on first contact. No
  amendment-sketch pressure surfaced; OQ-AP1 (scattered
  pathos) observation banks as non-probe-visible authorial
  note, not as forcing function.

- **Verifier track closes one banked seed with minimal
  machinery.** SC6–SC10 add a single substring token, a
  defensive helper, a backward-compatible kwarg, and one
  comment-line-composition path. LT3's honest-asymmetry
  contract (weak fallback means weak fallback; no
  promotion-by-convention) explicitly preserved by scope
  commitments (SC10). Two seeds remain banked; the
  incremental discipline survives.

- **Factor-out track extends without test deltas.**
  Conformance module (sketch-10) + reader-model-client-base
  (sketch-11) are the two factor-out commits the project has
  landed. Both follow the same rule: factor when three
  instances pressure duplication, not earlier; surface a
  narrow callable interface; duplicate what is
  intentionally-not-factored. Test-suite-invariant
  scaffolding; ready for downstream consumers (CI hook,
  walker, model-config registry) to use without re-reading
  per-client source.

**The sketch-11 pattern — "small commit closes sketch-10
candidate without opening new scope" — is repeatable.**
Remaining sketch-10 candidates that fit this shape: PFS11
(Aristotelian cross-boundary batch, field shapes
pre-committed), PFS12 (Save-the-Cat observation, smallest
per-record arc), research-track encoding cleanups (2 Oedipus
prose fixes + 5 Rashomon phase-annotation cleanups holdover
from sketches-05..-10). Each is a small arc under a
pre-committed surface.

---

## What the three commits revealed

### Third Aristotelian encoding lands clean: the sketch-02
surface absorbed a genuinely different shape

Oedipus and Rashomon — the two encodings aristotelian-sketch-02
drew from — cover: single mythos + separated binding +
precipitating anagnorisis (Oedipus); four mythoi + contests
relation + no anagnorisis (Rashomon). Macbeth covers a third
region: single mythos + coincident binding + non-precipitating
anagnorisis step. The encoding verified clean on first write
— no A10–A12 extension pressure, no A7-check escalation, no
authorial workaround ("close enough to Oedipus"). This
validates the **amendment-only posture** aristotelian-sketch-02
committed: A10–A12 added record / field / check capacity; the
capacity absorbed an independent third encoding without
further amendment.

The scope observations banked in macbeth_aristotelian's commit
body (OQ-AP1 pathos strain; OQ-AP4 not pressured) are
**authorial notes**, not commitments. If a future probe run
on Macbeth makes OQ-AP1 probe-visible (reader-model demands
typed ArPathos to read cleanly), OQ-AP1 converts from banked
to forcing; if not, it stays observation.

### Prose-carried signal: the smallest compatible verifier
extension

SC6–SC10 is the minimum viable answer to the OQ2-reshaped
pressure. Every SC10 scope exclusion is a real alternative
that was considered and rejected:

- **No verdict-strength lift.** Would violate LT3; would
  force weak-fallback paths to bifurcate into "weak-with-
  prose-hint" vs. "weak-without-prose-hint" strength
  classes.
- **No Optionlock extension.** Probe framing is Timelock-
  specific; Optionlock's weak-fallback semantics are
  different; the prose-carried signal's meaning there is
  not the same question.
- **No typed Annotation boolean.** Banks as OQ7 for a future
  arc if the substring convention proves too loose — but
  today the substring is cheap, visible in prose, and
  authored alongside the Lowering narrative.
- **Lowering annotations only.** Cross-dialect scan would
  widen scope to every place annotation.text lives; the
  Lowering is where the representational gap is named.
- **No back-application to other seeds.** Each banked seed
  has its own forcing function; OQ2-reshaped was the one
  a probe surfaced under a clear criterion.

The two-commit pattern — design doc + implementation — that
the verifier-sketch / scheduling-act-sketch / lowering-sketch
series has held since sketch-04 scales: SC6–SC10 is a 370-line
design + ~30-line verifier_helpers patch + 11 tests.

### Factor-out rule: concrete-before-abstract remains honest

Three reader-model clients accreted near-identical copies of
three distinct surfaces over sketches 4 / 6 / 10. The shared
base extraction landed in sketch-11 after the pattern
stabilized across all three. This matches the conformance-
module rule: factor when three concrete instances pressure
duplication, not on the second, not on speculation.

The **intentional non-factoring** is the sharper signal. The
base module docstring documents it: record-to-dict helpers,
Pydantic schemas, classify/translate helpers, and result
dataclasses stay per-client because they carry dialect-
specific content, not dialect-specific **structure**. The
distinction — "shared structure, per-dialect content" — is
the factor-out discipline's architectural commitment. Future
sketches that introduce a fourth reader-model client
(Save-the-Cat? Dramatic-cross-boundary?) will extend the
three shared primitives without touching per-dialect
machinery.

---

## What's next (research AND production)

### Research track

1. **Macbeth Aristotelian live probe (first-of-kind for the
   third encoding).** Pressures four axes simultaneously:
   - A12: does the reader-model probe accept
     BINDING_COINCIDENT as equivalent-force to Oedipus's
     BINDING_SEPARATED?
   - A11: does the probe read Lady Macbeth's sleepwalking
     as load-bearing anagnorisis_chain content (not mere
     character color)?
   - OQ-AP1: Macbeth's scattered pathos (E_macduff_family_
     killed + E_lady_macbeth_dies + E_macbeth_killed across
     two phases and three victims) is the corpus's most
     stressful pathos case — does the probe demand typed
     ArPathos?
   - OQ-AP4 (peripeteia-in-beginning): not expected to fire
     — Macbeth's peripeteia is end-phase. Probe results
     would only surprise if pathos scatter bleeds into the
     peripeteia question.
   Would open aristotelian-probe-sketch-03 candidate if
   OQ-AP1 forces open.

2. **ATTWN dramatic + dramatica-complete fills.** Unchanged
   from sketch-10. MC/IC decision (Vera-as-MC conventional vs.
   Wargrave-as-MC subversive) is the first substantive
   question. Unblocks probe runs on MN2 concealment-asymmetry
   + LT8/LT9 discrete-elimination Timelock + ATTWN Save-the-
   Cat + potentially Aristotelian fill.

3. **Post-sketch-02 Rashomon aristotelian re-probe verification
   under current surface.** A narrower-scope probe rerun: does
   Rashomon's v2 reading still cite A10–A12 structurally now
   that a third encoding exists in the corpus? Optional —
   sketch-10 probe already verified v2 closure.

4. **Fourth Aristotelian encoding (Ackroyd or Chinatown).**
   Pressures BINDING_ADJACENT gap; remaining uncovered cell.
   Only if the Macbeth probe surfaces clean closure on
   existing A10–A12 surface.

5. **Remaining two scheduling-act-family seeds.** Bandit-
   refinement MC-mediated endpoint substitution; OQ1-reshaped
   woodcutter cross-branch signature detector. Each has a
   distinct forcing function; deferred until those signals
   surface concretely.

6. **Probe-surfaced encoding cleanups** (sketches-05..-10
   holdover, still unopened). 2 Oedipus prose fixes + 5
   Rashomon phase-annotation cleanups. Smallest concrete
   research item.

### Production track

Re-ordered by sketch-11's completions (item G closed;
sketch-10's A / B / E / F / H / I / J / K remain):

A. **PFS11 — Aristotelian cross-boundary batch.** Four
   records (ArObservation + ArAnnotationReview +
   ArObservationCommentary + DialectReading) under
   `schema/aristotelian/`. Field shapes pre-committed in
   aristotelian-probe-sketch-01 / -02. Slim production
   sketch expected (PFS6 / PFS7 pattern). Closes sketch-10
   production item A.
B. **PFS12 — Save-the-Cat observation.** One record
   (StcObservation) under `schema/save_the_cat/`. Smallest
   cross-boundary per-record arc; slim production sketch.
C. **PFS13 — Dramatic dialect schemas.** Gated on
   dramatic-sketch-02 (PFS6 OQ2; six design forcing
   functions banked in dramatica-template-sketch-01).
   Dramatic-sketch-02 design-first arc is prerequisite.
D. **PFS14 — Dramatica-complete dialect schemas.** Gated
   on PFS13.
E. **Aristotelian A10–A12 schema landing.** Deferred by
   aristotelian-sketch-02 AA11; candidate for a future PFS
   extending `schema/aristotelian/mythos.json` with new
   optional fields + shipping new
   `schema/aristotelian/mythos_relation.json` +
   `anagnorisis_step.json` schemas.
F. **substrate-world-fold-sketch-01.** Unchanged from
   sketch-10 — forcing function not yet surfaced.
G. **~~Reader-model-client base extraction~~** — closed in
   sketch-11 as commit `91afd15`.
H. **Markdown-fenced author parser** (roadmap item 1). First
   consumer of the schemas outside the conformance test.
   Now consumes five namespaces (substrate + aristotelian +
   save_the_cat + lowering + verification) covering 13
   record types.
I. **Prose export round-trip starter** (roadmap item 3).
J. **Goodreads import prototype** (roadmap item 2).
K. **Port work** (roadmap item 4). Cross-boundary partially
   unblocked (Lowering + Verification spec'd; Aristotelian-
   cross-boundary + Save-the-Cat-observation pending
   PFS11/12).

### Recommendation

Mixed arc — one production + one research probe. Validated
candidates:

- **Production track A (PFS11)** — Aristotelian cross-boundary
  batch. Slim design + impl pair under pre-committed field
  shapes. Closes sketch-10 production item A; validates
  PFS8-N2 classification (dialect-internal cross-boundary
  records live under `schema/<dialect>/`).
- **Research track #1 (Macbeth Aristotelian live probe)** —
  first-of-kind for the third encoding. Highest forcing-
  function payoff on the research track; pressures four
  axes (A11 / A12 / OQ-AP1 / OQ-AP4) simultaneously.

Alternative (deferred if time runs short): **Production
track B (PFS12)** — Save-the-Cat observation; smallest
cross-boundary per-record arc.

---

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketches-04 through -10. Validated
again across the three sketch-11 commits:

- **Orientation before commitment.** Macbeth authoring began
  with a read of existing oedipus_aristotelian.py +
  rashomon_aristotelian.py + aristotelian-sketch-02 A10–A12
  + core/aristotelian.py dataclass signatures. SC6–SC10
  design began with a read of scheduling-act-utterance-
  sketch-01's SC1–SC5 + the banked OQ2-reshaped forcing
  function + verifier_helpers dsp_limit_characterization_
  check. Reader-model-client-base extraction began with a
  read of all three client files in parallel to identify
  shared surfaces.
- **Sketches before implementation.** SC6–SC10 shipped as
  design commit + implementation commit pair (compressed to
  a single commit per the post-sketch-04 consolidation
  pattern for small arcs). Macbeth ships without a design
  sketch — authorial content under a pre-committed surface.
  Reader-model-client-base ships without a design sketch —
  pure factor-out per state-of-play-10 item G's brief.
- **Banking with forcing-function criteria.** SC10 banks
  OQ7 (typed Annotation boolean) with a named forcing
  function (substring convention proves too loose). OQ-AP1
  Macbeth-scattered-pathos bank is observation, not forcing
  — converts to forcing if probe surfaces it.
- **State-of-play at milestone boundaries.** This doc.
  Milestone: third Aristotelian encoding + first banked
  scheduling-act-family seed closes + reader-model-client
  factor-out.
- **Commit messages as cross-session artifacts.** All three
  sketch-11 commits carry 80–140-line bodies; a cold-start
  Claude reading `git log --oneline -20` + `git show` on
  each can reconstruct sketch-11's arcs fully from commit
  bodies.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic.
2. This doc (`design/state-of-play-11.md`) — current corpus,
   shift-point state, research + production tracks.
3. `schema/README.md` — the three-tier production layer
   (substrate / dialect / cross-boundary).
4. `git log --oneline -20` — the three sketch-11 commits +
   sketch-10's fifteen carry dense readable bodies; together
   they cover the last two design milestones.
5. `design/state-of-play-10.md` — sketch-10's cold-start
   doc. Sketch-11 supersedes it as the active state-of-play,
   but sketch-10 carries the full context for the
   cross-boundary schema + Tier-2 audit + Aristotelian
   amendment milestones it landed.
6. `design/aristotelian-sketch-02.md` +
   `aristotelian-probe-sketch-02.md` — the amendment + probe-
   closure loop Macbeth now stress-tests.
7. `design/scheduling-act-utterance-sketch-02.md` — the
   SC6–SC10 prose-carried commitments, for anyone extending
   verifier comment-composition paths.
8. `prototype/story_engine/core/conformance.py` +
   `prototype/story_engine/core/reader_model_client_base.py`
   — the two factor-out modules. Read module docstrings +
   top-level callable signatures; the rest is helper detail.
