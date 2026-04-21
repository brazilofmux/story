# Aristotelian probe — sketch 04 (Hamlet re-probe under sketch-03 A13–A14)

**Status:** draft, active
**Date:** 2026-04-21
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [aristotelian-probe-sketch-01](aristotelian-probe-sketch-01.md) — APS1–APS6 unchanged; [aristotelian-probe-sketch-02](aristotelian-probe-sketch-02.md) — closure ledger continues; [aristotelian-probe-sketch-03](aristotelian-probe-sketch-03.md) — Macbeth-first-probe outcomes unchanged
**Frames:** [aristotelian-sketch-01](aristotelian-sketch-01.md), [aristotelian-sketch-02](aristotelian-sketch-02.md), [aristotelian-sketch-03](aristotelian-sketch-03.md) (A13 ArCharacterArcRelation + A14 step_kind + anagnorisis_character_ref_id; A7.10 + A7.11)
**Related:** `prototype/reader_model_hamlet_aristotelian_output.json` (the Session 5 pre-sketch-03 artifact this sketch re-runs against); `prototype/demos/demo_aristotelian_reader_model_hamlet.py` (the demo threaded through); `prototype/story_engine/encodings/hamlet_aristotelian.py` (the sketch-03-migrated encoding); `prototype/story_engine/core/aristotelian_reader_model_client.py` (the client this sketch extends)
**Superseded by:** nothing yet

## Purpose

Re-run the Hamlet live probe (Session 6 of the Hamlet multi-session research arc) after aristotelian-sketch-03 landed A13–A14 and the Hamlet encoding migrated (two pairwise `ArCharacterArcRelation` records + three-step `anagnorisis_chain` with explicit `step_kind`s + `anagnorisis_character_ref_id="ar_hamlet"`). Parallels probe-sketch-02's re-probe of Oedipus + Rashomon after sketch-02 landed.

The re-probe tests sketch-03's **closure hypothesis**: the two probe-surfaced forcing functions from Session 5 — **OQ-AP6** (intra-mythos parallel tragic-heroes) and **OQ-AP10** (protagonist-scope anagnorisis chain) — close by becoming authored. If Session 6 still surfaces them in `relations_wanted`, sketch-03 shipped the wrong shape. If the probe acknowledges the new records (mirror-Hamlet-Laertes, foil-Hamlet-Claudius, three-step staging chain) and moves on, the closure is verified.

Secondary purpose: catch the reader-model client up to sketch-03. Sketch-03 landed the dialect-layer records and the verifier but did not extend the LLM-prompt rendering; without the client extensions below, sketch-03's new content is invisible to the probe and the closure cannot be evaluated.

## Why now

Sketch-03 landed at commit `ac926e2` (2026-04-20); the re-probe runs the following day (2026-04-21). Same-day+1 cadence matches probe-sketch-02's two-day gap. Longer deferral would let Session 5 behavior drift in memory and risk re-probing against a stale hypothesis.

Session 5 alternation-rhythm note: Session 5 was research; sketch-03 (design + impl) was the production half of the alternation; this sketch is the next research beat. The last substantive commit (`ac926e2`) was production; research is due.

## Scope — what this sketch covers

**In:**

- **Client-side sketch-03 rendering extensions** — the minimal wiring to let the LLM see A13 + A14 content. Without these, the probe cannot evaluate the closure. Spec in §Client-side changes below.
- Execution of a single live re-probe on Hamlet under the sketch-03-extended client surface. Output versioned as `reader_model_hamlet_aristotelian_output_v2.json` to preserve Session 5's `reader_model_hamlet_aristotelian_output.json` alongside.
- Prediction outcomes against sketch-01 APS6 P1 / P3 / P4 + **closure-check predictions** P5–P5b + **still-banked predictions** P6–P10 carried over from Session 5.
- A **closure ledger** — for sketch-03's two closures (A13 / A14), test whether the Hamlet Session 6 reading honors them structurally. Parallel to probe-sketch-02's A10 / A11 / A12 closure ledger.
- A **retirement check** — OQ-AP5 (fate-agent) retired by sketch-03 on two-negative-probe grounds. Session 6 is a third-signal check; a hit would challenge the retirement. Parallels closure-check logic with inverted polarity.
- New findings: `scope_limits_observed` / `relations_wanted` items that surface on Session 6 for the first time, or that re-surface from Session 5 under the new rendering.
- Disposition map of still-banked Session 5 OQs (OQ-AP1 polis catharsis, OQ-AP7 range-of-separated, OQ-AP8 same-beat, OQ-AP9 audience-level dramatic irony).

**Out:**

- New dialect commitments beyond sketch-03. If Session 6 pressures further extensions, they land in a future aristotelian-sketch-04, not here.
- Re-probe of Oedipus / Rashomon / Macbeth. Sketch-02's closures verified on those; sketch-03's closures are Hamlet-specific (OQ-AP6 / OQ-AP10 were Hamlet-forcing). No cross-encoding generalization test of A13 / A14 in this sketch — it would require a second encoding with ≥2 tragic heroes or an intra-character staging chain, which the current corpus doesn't have. Banked for a future probe.
- Schema-layer landing of A13 + A14 under `schema/aristotelian/` (sketch-03's AA15 item, deferred per sketch-03). This probe operates at the Python-client layer; schema-layer files are not on the probe's prompt surface today.
- Changes to the Pydantic output-schema surface. A13 / A14 are input-side (what the probe reads); the three probe-output records (ArAnnotationReview, ObservationCommentary, DialectReading) are unchanged.
- Markdown-surface / author-document rendering. Separate arc.

## Client-side changes landed before the run

Minimal, to let the LLM see sketch-03 content. Four surfaces touched, all in `aristotelian_reader_model_client.py`:

### APA4-1 — `_ar_anagnorisis_step_to_dict` renders `step_kind`

Current:
```python
def _ar_anagnorisis_step_to_dict(step) -> dict:
    return {
        "kind": "ArAnagnorisisStep",
        "id": step.id,
        "event_id": step.event_id,
        "character_ref_id": step.character_ref_id,
        "precipitates_main": step.precipitates_main,
        "annotation": step.annotation,
    }
```

Adds `"step_kind": step.step_kind` — a string, `"parallel" | "precipitating" | "staging"` when set, empty string when derived. No derivation in the rendering — the LLM sees what the encoding authored (empty-string steps derive under A14 per sketch-03; the LLM reasons over authored content + the system prompt's A14 explanation).

### APA4-2 — `_ar_mythos_to_dict` renders `anagnorisis_character_ref_id`

Current rendering omits the field. Adds `"anagnorisis_character_ref_id": mythos.anagnorisis_character_ref_id` — a string or None. When None, the LLM sees the absence (and correctly infers that `step_kind=""` steps derive to parallel/precipitating, not staging).

### APA4-3 — New `_ar_character_arc_relation_to_dict` + `_build_character_arc_relations_section`

A13's `ArCharacterArcRelation` records live at encoding scope (parallel to A10's `ArMythosRelation`). New rendering helper:

```python
def _ar_character_arc_relation_to_dict(rel) -> dict:
    return {
        "kind": "ArCharacterArcRelation",
        "id": rel.id,
        "relation_kind": rel.kind,
        "character_ref_ids": list(rel.character_ref_ids),
        "mythos_id": rel.mythos_id,
        "over_event_ids": list(rel.over_event_ids),
        "annotation": rel.annotation,
    }
```

Renders in a **dedicated prompt section** — parallel shape to the `ArMythosRelation` section probe-sketch-02 added. Omitted when the encoding authors no relations. Section heading: `## ArCharacterArcRelation records` with a preamble explaining the intra-mythos scope and the three canonical kinds (`parallel`, `mirror`, `foil`) and noting the `annotation` field carries authored prose.

**Reviewable-prose decision.** The `annotation` field on ArCharacterArcRelation is authored prose with structural weight comparable to ArPhase annotation or ArMythos action_summary. Session 6 threads it through as a reviewable field — the probe's task list gains `ArCharacterArcRelation:<id>:annotation` for each authored relation. The Pydantic output schema's `target_kind` already supports arbitrary strings, so this is a prompt-level change only.

Same decision for ArAnagnorisisStep annotation prose (sketch-03 adds two staging-step annotations on Hamlet). Previously un-reviewable; Session 6 makes it reviewable since sketch-03's staging steps carry authorial content the probe should be able to call tension on.

### APA4-4 — `build_user_prompt` + `invoke_aristotelian_reader_model` gain `character_arc_relations: tuple = ()` kwarg

Default empty preserves pre-sketch-03 call sites (Oedipus / Rashomon / Macbeth demos unchanged). The kwarg threads through to `_build_character_arc_relations_section`. Parallels probe-sketch-02's `relations` kwarg addition.

### APA4-5 — SYSTEM_PROMPT sketch-03 awareness

Current SYSTEM_PROMPT carries a sketch-02 paragraph naming A10–A12. Extends with a **sketch-03 paragraph** naming the three new extensions:

> Note on sketch-03: the dialect now ships `ArCharacterArcRelation` (kinds: `'parallel'` | `'mirror'` | `'foil'`) expressing intra-mythos structural relations between two or more ArCharacter records within a single ArMythos — orthogonal to sketch-02's ArMythosRelation (which is inter-mythos). It also adds `step_kind` on ArAnagnorisisStep (`"parallel"` | `"precipitating"` | `"staging"`) — `staging` is new and names same-character epistemic waypoints on the path to the main anagnorisis. ArMythos gains `anagnorisis_character_ref_id` naming who the main anagnorisis belongs to. If an encoding authors these, they appear inline (step_kind on steps; anagnorisis_character_ref_id on ArMythos) or in a dedicated `ArCharacterArcRelation records` section. If an encoding does NOT author them but they would help, flag them in `relations_wanted`. If the dialect still lacks something you wanted — e.g., three-way character-arc relations, numerical peripeteia-anagnorisis distance, same-beat staggered recognition — flag that too.

Adjacent update to the annotation-review section: a brief note that `target_kind` now also accepts `ArCharacterArcRelation` (for `annotation` reviews) and `ArAnagnorisisStep` (for `annotation` reviews). No other client changes.

### APA4-6 — Demo migration

`demo_aristotelian_reader_model_hamlet.py` is already partly migrated for sketch-03 (imports `AR_HAMLET_CHARACTER_ARC_RELATIONS` and threads it through `verify`). Extends:

- Thread `character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS` through `invoke_aristotelian_reader_model`.
- Update docstring session log (Session 6, post-sketch-03 re-probe framing; predictions reframed as closure-check per §Predictions below).
- Save path: `--save-json reader_model_hamlet_aristotelian_output_v2.json` (preserves Session 5's v1 alongside).
- Substring-matcher P5–P10 block: unchanged logic; reframed in commentary as closure-discriminating-ambiguous (factual citations of authored records look like forcing hits to the substring matcher). JSON stays ground-truth.

Oedipus / Rashomon / Macbeth demos: unchanged (their encodings don't author sketch-03 records; the empty-kwarg defaults preserve pre-sketch-03 prompt shape).

Pydantic schemas, output records, translation logic: unchanged. The v2 output JSON shape is additive-only — annotation_reviews may grow (more reviewable fields) but the record-level shape is the same.

## Prediction outcomes (Session 6 under sketch-03 rendering)

Labels **P1 / P3 / P4** are sketch-01 APS6 inheritances; **P5 / P5b** are closure-check predictions sketch-04 introduces; **P6–P10** carry over Session 5's still-banked predictions with unchanged expectations.

| # | Prediction | Expected outcome |
|---|---|---|
| P1 | ≥ 80% approved, 0 rejected across ≥ 7 prose reviews. Sketch-03 grows reviewable prose from 7 fields to 11 (+2 staging-step annotations + 2 arc-relation annotations); prediction is on proportion. | PASS expected. Session 5 was 7/7 approved. |
| P3 | `observation_commentaries` is empty — Hamlet verifies clean under sketch-03 per `test_hamlet_aristotelian_verifies_clean`. | PASS expected. |
| P4 | `read_on_terms ∈ {"yes", "partial"}`, `drift_flagged` empty or near-empty. | PASS expected. Session 5 was "yes" with empty drift; sketch-03 gives the probe more vocabulary to stay in-dialect, expected to stay at "yes" or stronger. |
| **P5 (closure-check — OQ-AP6 parallel-heroes)** | The probe reads the two pairwise `ArCharacterArcRelation` records as structurally load-bearing (cites mirror-Hamlet-Laertes and/or foil-Hamlet-Claudius in its rationale) and does NOT propose new structural records for the same parallelism. | Pass criterion: probe cites ≥1 authored arc relation + 0 `relations_wanted` for intra-mythos parallel-hero typing. Fail = residual parallel-hero pressure (sketch-03 under-specified). |
| **P5b (closure-check — OQ-AP10 protagonist-chain)** | The probe reads the three-step chain with explicit `step_kind`s as sufficient for Hamlet's staggered coming-to-know; does NOT propose chain extension for intra-character epistemic staging. Residual pressure to distinguish staging from parallel is closure-confirming (the dialect now does). | Pass criterion: probe cites the staging steps + 0 `relations_wanted` for intra-character chain expansion. Fail = residual chain-extension pressure. |
| P6 (still-banked — OQ-AP7 range-of-separated) | Session 5 did not force; no change expected. The distance-9 BINDING_SEPARATED remains the same; Session 6 has a third-chance signal opportunity. Prediction: no forcing. | Stays banked on third-negative-probe signal. |
| P7 (still-banked — OQ-AP8 same-beat staggered) | Laertes's deathbed recognition remains invisible as a chain step; Session 5 did not force; no change expected. Prediction: no forcing. | Stays banked on third-negative-probe signal. |
| **P8 (retirement-check — OQ-AP5 fate-agent)** | Sketch-03 retired OQ-AP5 on two-negative-probe grounds. Expected: no fate-agent pressure (third-negative confirmation). A HIT here would challenge the retirement. | Stays retired; a hit would re-open. |
| P9 (still-banked — OQ-AP1 pathos-typing) | Session 5 surfaced polis-catharsis as the third independent signal (after Macbeth's scattered pathos and Hamlet's cluster pathos). Session 6 prediction: the polis-catharsis signal likely re-surfaces under the same encoding + the same prose-clustering. Fourth **convergent** signal (same axis as Session 5's polis-catharsis) is the sketch-03-stated forcing criterion. | Banked; fourth convergent signal would force a future sketch. |
| P10 (still-banked — OQ-AP9 audience-level dramatic irony) | Session 5 surfaced audience-level dramatic irony as a NEW finding. Session 6 under the same encoding: expected re-surfacing (fifth site overall: Rashomon-v1, Rashomon-v2, Macbeth, Hamlet-Session-5, Hamlet-Session-6). Remains correctly out of sketch-01 A4/A8 scope. | Stays scope-rejected; fifth re-surfacing strengthens the rejection-as-stance. |

**P5 / P5b discrimination discipline.** The substring matcher in the demo's summary can't distinguish *factual citation of an authored record* from *a demand for a new record*. The commit message for Session 6 must cite the JSON directly, not the summary, for P5 / P5b verdicts. The JSON's `relations_wanted` list is authoritative: empty or focused on different extensions = closure-verified; non-empty items about intra-mythos parallel-hero typing or intra-character chain expansion = closure-unverified.

## Closure ledger — sketch-03's two closures under Hamlet Session 6

Sketch-03 committed to closing OQ-AP6 (via A13) and OQ-AP10 (via A14) and retiring OQ-AP5. The Session 6 run is the closure test. Structure parallel to probe-sketch-02's A10 / A11 / A12 closure ledger and probe-sketch-03's Macbeth closure-verification.

### A13 ArCharacterArcRelation — closure test TBD

Hamlet authors two relations (`AR_HAMLET_LAERTES_MIRROR`, `AR_HAMLET_CLAUDIUS_FOIL`). Session 6 verdict: closure-verified iff (a) the probe cites at least one authored relation structurally in its rationale, AND (b) `relations_wanted` contains no new intra-mythos parallel-character-arc proposals. Partial-verification if (a) but not (b); unverified if neither.

### A14 step_kind + anagnorisis_character_ref_id — closure test TBD

Hamlet authors `anagnorisis_character_ref_id="ar_hamlet"` and a three-step chain (`STEP_KIND_STAGING` × 2 for Hamlet's Ghost-claim / Mousetrap, `STEP_KIND_PARALLEL` × 1 for Claudius-prays). Session 6 verdict: closure-verified iff (a) the probe cites at least one staging step structurally (preferably both, and the parallel step), AND (b) `relations_wanted` contains no new chain-extension proposals for intra-character epistemic staging.

### OQ-AP5 retirement — retention test TBD

Hamlet's Ghost stays at substrate layer (the encoding's `OQ_AP5_FINDING` prose preserves sketch-03's retirement rationale). Session 6 verdict: retention-verified iff the probe does NOT re-surface fate-agent pressure in `scope_limits_observed` or `relations_wanted`. A hit would challenge the retirement decision and require re-opening the OQ.

### Cross-encoding generalization — DEFERRED

A14's `"parallel"` and `"precipitating"` derivations handle pre-sketch-03 encodings (Oedipus's Jocasta, Macbeth's Lady Macbeth) identically under the derivation rules. Sketch-03 verified this at the verifier layer (their tests still pass). A cross-encoding probe-layer generalization — rendering Oedipus / Macbeth with their derived `step_kind`s and checking the probe reads them correctly — is out of scope for this sketch; banked for a future probe if OQ-AP6 or OQ-AP10 behavior surprises.

## Disposition of Session 5 findings under Session 6

Session 5 surfaced four live findings (two closed by sketch-03, two banked) plus two negative-confirmations. Session 6 dispositions:

- **OQ-AP6 (parallel-heroes, CLOSED by sketch-03).** Session 6 is the closure-verification. Expected: no `relations_wanted` pressure; probe cites authored mirror / foil relations.
- **OQ-AP10 (protagonist-chain, CLOSED by sketch-03).** Session 6 is the closure-verification. Expected: no `relations_wanted` pressure for chain extension; probe cites authored staging steps.
- **OQ-AP5 (fate-agent, RETIRED by sketch-03).** Session 6 is the third-negative confirmation. Expected: continued silence.
- **OQ-AP1 (pathos-typing, banked).** Session 5 third-signal (polis catharsis). Session 6 prediction: polis signal re-surfaces under same encoding + prose. Not counted as a fourth *convergent* signal for forcing purposes unless a different pathos-axis surfaces alongside (non-convergent data doesn't add to the forcing count).
- **OQ-AP7 (range-of-separated, banked).** Session 5 non-forcing. Session 6 third-chance; expected non-forcing.
- **OQ-AP8 (same-beat staggered, banked).** Session 5 non-forcing. Session 6 third-chance; expected non-forcing.
- **OQ-AP9 (audience-level dramatic irony, scope-rejected).** Session 5 fourth re-surfacing. Session 6 fifth-site expected; strengthens rejection-as-stance.

## Acceptance criteria

Labels **APA4-1** through **APA4-7** extend probe-sketch-03's APA3-1..APA3-5 and probe-sketch-02's APA2-1..APA2-4.

- **APA4-1.** Client extensions land per §Client-side changes APA4-1..APA4-5. Oedipus / Rashomon / Macbeth demos are byte-identical through the probe interface (default-empty kwargs preserve their prompt shape); their JSON output v1 artifacts remain authoritative.
- **APA4-2.** Session 6 runs against the extended client. Output saved as `reader_model_hamlet_aristotelian_output_v2.json`. Session 5's `reader_model_hamlet_aristotelian_output.json` preserved for diff.
- **APA4-3.** P1 / P3 / P4 PASS (sketch-01 APS6 inheritance).
- **APA4-4.** P5 / P5b closure-check verdicts dispositioned in the commit message, citing specific JSON paths (not the substring summary).
- **APA4-5.** P8 retirement-check verdict dispositioned.
- **APA4-6.** P6 / P7 / P9 / P10 still-banked predictions dispositioned — each either confirmed (expected) or newly forcing (surprise, banked for sketch-05).
- **APA4-7.** Any new findings (first-time `scope_limits_observed` / `relations_wanted` under Session 6's rendering) are recorded in a Session 6 findings appendix to this sketch or in the commit message's findings section, with forcing-function analysis.

## Open questions (banked for sketch-05 if they force)

- **OQ-AP11 — arc-relation three-way shape.** Sketch-03 OQ7 banked this: whether a three-way single relation with structurally-distinct-from-pairwise content ever emerges in corpus. Hamlet's three-way parallelism (Hamlet / Claudius / Laertes) authored as two pairwise relations per sketch-03's decision. Session 6 may pressure the three-way shape if the probe flags "pairwise decomposition loses a three-way structural content" — a hit here would force OQ-AP11 to the top.
- **OQ-AP12 — step-kind vocabulary expansion.** Sketch-03 shipped `parallel` / `precipitating` / `staging`. Session 6 may surface additional step kinds (`preparatory`, `mistaken-recognition`, `pre-ecstatic`) that Hamlet's chain pressures. Probably quiet — the three kinds cover the structural distinctions Hamlet's chain makes — but flagged here for vocabulary-expansion watch.
- **OQ-AP13 — reviewable-prose scope creep.** APA4-3's decision to thread arc-relation and staging-step annotations through as reviewable prose grows the reviewable-field count from 7 to 11 on Hamlet. If Session 6's prose-review quality holds (P1 passes at the new size), no change; if it degrades (approval proportion drops or reviews thin out), the sketch-04 decision may have been over-aggressive and a future sketch may narrow reviewable-prose back to ArMythos / ArPhase / ArCharacter.

## Session log contribution

On completion, this sketch + the Session 6 probe-run commit together close the Hamlet multi-session research arc's **closure-verification milestone** — Sessions 1–4 built the encoding; Session 5 probed pre-migration; sketch-03 closed the probe-surfaced gaps; Session 6 verifies the closures. A state-of-play refresh (state-of-play-12) after Session 6 is the natural next move — sketch-11 predates five commits and would benefit from a cold-start refresh before the arc's next beat.

**Post-Session-6 alternation.** Session 6 is research; the next substantive commit should be production-track per the alternation rule. Natural candidates: (a) state-of-play-12 refresh (housekeeping production — counts as production-track by rhythm, though it's design work not code); (b) sketch-03 schema-layer landing (AA15 deferred item — production-format-sketch-14 on `schema/aristotelian/` for A13–A14 files); (c) next Dramatica-layer or cross-dialect work. User decides at that point.
