# Aristotelian probe — sketch 02 (re-probe under sketch-02 A10–A12)

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [aristotelian-probe-sketch-01](aristotelian-probe-sketch-01.md) — APS1–APS6 unchanged; this sketch records second-run outcomes
**Frames:** [aristotelian-sketch-01](aristotelian-sketch-01.md), [aristotelian-sketch-02](aristotelian-sketch-02.md)
**Related:** `prototype/reader_model_oedipus_aristotelian_output_v2.json`, `prototype/reader_model_rashomon_aristotelian_output_v2.json` (the artifact JSONs this sketch reads)
**Superseded by:** nothing yet

## Purpose

Re-run the two live probes (Oedipus + Rashomon) after aristotelian-sketch-02 landed A10–A12 and the encodings migrated (AR_RASHOMON_CONTEST; AR_STEP_JOCASTA + binding="separated"). Record the findings against sketch-01 predictions P1–P5 and against the **closure hypothesis** sketch-02 stated: *the three well-forced proposals — ArMythosRelation, ArAnagnorisisChain, ArPeripeteiaAnagnorisisBinding — close by becoming authored*.

Secondary purpose: capture new forcing functions the second run surfaces, so the design corpus doesn't lose them.

**The re-probe is the test** of sketch-02's closure claim, in the same way sketch-01 was the test of architecture-sketch-02's dialect-stack claim. If the probe still surfaces the three closed proposals in `relations_wanted`, sketch-02 shipped the wrong shape. If the probe acknowledges the new records and moves on to the next layer, the closure is verified.

## Why now

Sketch-02 landed at commit 2949284; the re-probe runs two days later (2026-04-19, same day-cadence the arc has kept). Longer deferral would have let v1 behavior drift in memory and risked me re-probing against a stale hypothesis.

## Scope — what this sketch covers

**In:**
- Execution of two live probes under the sketch-02-extended client surface (`anagnorisis_chain` + `peripeteia_anagnorisis_binding` inline on ArMythos; `ArMythosRelation` in its own section for Rashomon).
- Prediction outcomes P1–P5 from sketch-01 APS6, now applied to v2 output.
- A **closure ledger** — for each v1 `relations_wanted` entry, classify v2 as *closed* / *persisted* / *deferred* / *rejected-but-persists*.
- New findings (scope_limits_observed, relations_wanted) surfaced for the first time in v2.
- No new commitments; this is a read-and-record sketch.

**Out:**
- Changes to the probe client beyond the sketch-02-extension minimal wiring (already landed).
- New dialect commitments — if v2 pressures extensions, they land in aristotelian-sketch-03 (a future amendment), not here.
- Retrospective review of v1: the v1 JSON stays as captured; comparisons read it but don't amend it.
- Macbeth / Ackroyd Aristotelian encodings. Still future work.

## Client-side changes landed before the run

Minimal, to let the LLM see sketch-02 content:

- `_ar_mythos_to_dict` renders the three new ArMythos fields (`anagnorisis_chain` as a list of step dicts; `peripeteia_anagnorisis_binding`; `peripeteia_anagnorisis_adjacency_bound`).
- New `_ar_relation_to_dict` + `_build_relations_section` renders `ArMythosRelation` records as a dedicated prompt section, parallel to the observations section; omitted when the encoding authors no relations.
- `build_user_prompt` + `invoke_aristotelian_reader_model` gain a `relations: tuple = ()` kwarg (default empty preserves pre-sketch-02 callers).
- System prompt adds one paragraph naming the three sketch-02 extensions and the expectation that `relations_wanted` may still flag *other* extensions (e.g., frame-mythos, audience-level recognition) the dialect still lacks.
- Demos: Oedipus unchanged (its sketch-02 additions flow through ArMythos). Rashomon imports `AR_RASHOMON_RELATIONS` and passes it to the invocation; context JSON gains `relation_count`.

Pydantic schemas, output records, translation logic: unchanged. The v2 output JSON shape is byte-identical to v1's.

## Prediction outcomes (sketch-01 APS6, applied to v2)

### Oedipus invocation

| # | Prediction | v2 outcome | Verdict |
|---|---|---|---|
| P1 | ≥ 80% approved, ≤ 1 needs-work, 0 rejected across 6 prose reviews | 5/6 approved (83%), 1 needs-work, 0 rejected | **PASS** |
| P3 | `observation_commentaries` empty | Empty | **PASS** |
| P4 | `read_on_terms="yes"`, `drift_flagged` empty | yes, empty | **PASS** |

No P2 (Rashomon-only) / P5 (exploratory) on Oedipus.

**v1 → v2 quality shift.** The one needs-work is on a different field than v1's. v1 flagged the action_summary's claim of "recognition coincides with reversal" as contradicted by the separated events; v2's prose was fixed pre-commit, and v2 now finds a fresh prose-quality tension — the action_summary conflates the shepherd's testimony (denouement) with Oedipus's recognition (anagnorisis). Comment length in v2 reviews is ~25% shorter than v1; the dialect is reading tighter with the structural fields filled in.

### Rashomon invocation

| # | Prediction | v2 outcome | Verdict |
|---|---|---|---|
| P2 | ≥ 1 prose review surfaces a dialect-scope tension (needs-work / noted) | 2 needs-work out of 20 | **PASS** |
| P3 | `observation_commentaries` empty | Empty | **PASS** |
| P4 | `read_on_terms ∈ {yes, partial}`, no Dramatica drift | **yes** (v1 was partial), `drift_flagged` empty (v1 had 5) | **PASS, strengthened** |
| P5 (exploratory) | `relations_wanted` names ArMythosRelation or equivalent | AR_RASHOMON_CONTEST is authored; probe explicitly cites "the ArMythosRelation 'contests' kind allowed the encoding to express inter-mythos friction without leaving the dialect." 3 *new* relation wants surface. | **PASS (closure-verified)** |

**v1 → v2 read_on_terms upgraded from `partial` to `yes`.** The authored ArMythosRelation removed the principal source of strain v1 flagged ("Aristotle's framework is mythos-singular; [the dialect] can mark aims_at_catharsis on each mythos individually but cannot express that the work's catharsis emerges from their contest"). The probe keeps its honest limits but no longer needs other-dialect language to articulate them.

## Closure ledger — the three well-forced v1 proposals

Sketch-02 committed to closing three of the five v1 relations_wanted. The v2 run is the closure test:

### ArMythosRelation — **CLOSED**

v2's dialect_reading rationale (Rashomon) names the record explicitly: *"The ArMythosRelation 'contests' kind allowed the encoding to express inter-mythos friction without leaving the dialect."* `relations_wanted` does not ask for ArMythosRelation. The authored AR_RASHOMON_CONTEST is visible to the probe in a dedicated records section; its annotation prose is read as context without needing its own review target.

**Closure type:** the probe sees the authored record and treats the dialect-scope gap as filled.

### ArAnagnorisisChain — **CLOSED**

v2's Oedipus dialect_reading rationale: *"The sketch-02 extensions — ArAnagnorisisStep for Jocasta's staggered recognition, peripeteia_anagnorisis_binding typed as 'separated' — cleanly captured the two-beat reversal-recognition structure that Aristotle himself singles out (Poetics 1452a)."*

Further, one of the 6 prose reviews cites the step: *"The anagnorisis_chain's ArAnagnorisisStep corroborates the precipitating relationship the prose describes."* The probe treats the step as a first-class structural element in its reasoning, which is what a closed extension should look like.

**Closure type:** authored + structurally load-bearing in the probe's analysis.

### ArPeripeteiaAnagnorisisBinding — **CLOSED**

Same v2 rationale as above — the binding is acknowledged as "cleanly captur[ing]" the two-beat structure. No v2 request for a typed binding; no re-flagging of the prose-vs-structure tension that v1 named on the action_summary.

**Closure type:** authored + referenced by the probe in its overall reading.

## Closure ledger — the two held-out v1 proposals

### ArFrameMythos — **PERSISTS AS LIMIT (correct)**

Sketch-02 deferred this (blocked by Rashomon's substrate-layer absence of frame events). v2 does NOT re-surface "ArFrameMythos" by name. But the related absence is re-flagged at a finer grain:

> "Narrator-as-tragic-hero: the woodcutter's mythos (and to a lesser extent the other three) is a tragedy whose hero is also its narrator — a structure the Poetics does not address."

This is a different framing than v1's ArFrameMythos request — narrower, more specific. The probe hasn't forgotten the frame-narrative gap; it's restated the concrete piece of the gap that shows up in the encoded surface. Sketch-02's deferral rationale ("dialect extension alone can't bind — substrate fill first") is unchallenged.

**Correct behavior:** sketch-02 said "defer pending substrate fill"; v2 doesn't force the deferral open.

### ArAnagnorisisLevel — **RE-SURFACES UNDER NEW NAME**

Sketch-02 rejected this as against sketch-01 A4/A8 scope. v2 re-surfaces it as `ArAudienceAnagnorisis`:

> "ArAudienceAnagnorisis: an audience-level recognition modifier on ArMythosRelation, expressing that the friction between contesting mythoi produces a recognition in the audience that no single mythos's characters achieve. This would address the meta-anagnorisis scope limit."

This is the same request sketch-02 explicitly rejected — now bundled into an ArMythosRelation modifier rather than an ArMythos modifier. The re-surfacing confirms sketch-02's judgment that rejecting was a genuine design decision, not a punt — the probe continues to pressure on this axis, because the dialect genuinely doesn't cover it.

**Interpretation:** sketch-02's rejection is not a bug; it's a scope stance the probe will re-flag every run. The response discipline is to keep the rejection (per A4/A8) and let the probe keep pressuring; reopening requires amending sketch-01's A4/A8 commitments, which is a bigger decision than any single probe run authorizes.

## New findings — forcing functions surfaced for the first time in v2

Three genuinely new proposals. Each is a *second-order* extension — something only visible once the first-order gaps (sketch-02's three) closed.

### Oedipus probe: ArPathos record + catharsis grounding mechanism

v2 dialect_reading scope_limits_observed (Oedipus):

> "Pathos as a typed structural element: the encoding records Jocasta's suicide and Oedipus's self-blinding as scope events in the end-phase, but the Aristotelian dialect surface has no typed 'pathos' (suffering) record parallel to ArAnagnorisisStep. Aristotle names pathos as the third part of the complex plot alongside peripeteia and anagnorisis (Poetics 1452b); the current dialect encodes it only implicitly via event presence in the end-phase."

> "Audience-level catharsis grounding: the mythos asserts aims_at_catharsis=true, but the dialect provides no structural mechanism for grounding pity and fear in the arrangement of incidents — e.g., which events are pity-bearing, which are fear-bearing, and how their sequence produces cathartic effect."

And in relations_wanted:

> "ArPathos record type: a typed record parallel to ArAnagnorisisStep that identifies which events constitute the suffering (πάθος) and links them to the recognition and reversal, completing Aristotle's triad of complex-plot parts."

> "Catharsis grounding mechanism: a way to annotate which events carry pity (ἔλεος) and which carry fear (φόβος), so that aims_at_catharsis could be structurally verified rather than merely asserted."

**Forcing-function analysis.** Aristotle names three parts of the complex plot: peripeteia, anagnorisis, pathos (Poetics 1452b). Sketch-02 landed typed structure for the first two (peripeteia via the adjacency binding; anagnorisis via the chain). Pathos remains only *implicit* — events in the end-phase carry the suffering, but nothing types which events count as pathos. The probe's request completes Aristotle's own triad.

**Relationship to sketch-01 OQ1.** Sketch-01 OQ1 banked "typed ArAffect record (catharsis/pity/fear)" with a forcing-function criterion: "if a second Aristotelian encoding lands and the probe finds the free-form approach too loose, sketch-02 upgrades." OQ1 was not closed in sketch-02 (no second encoding). v2 names the need at finer grain — not "affect record" generally, but specifically (a) `ArPathos` parallel to `ArAnagnorisisStep`, (b) catharsis grounding via pity-bearing / fear-bearing event tags.

**Forcing-function criterion for a hypothetical ArPathos arc:** either (a) a second Aristotelian encoding where pathos placement is ambiguous or disputed between readings (Macbeth? Hamlet?), (b) a verifier check that wants to compute "does the end-phase structurally demonstrate catharsis" and needs typed inputs, or (c) a cross-dialect Lowering that needs to bind catharsis-related claims (e.g., Dramatic's Story_consequence ↔ Aristotelian pathos — sketch-01 OQ5 territory).

### Rashomon probe: ArCanonicalFloor / ArSharedEventSet

> "ArCanonicalFloor or ArSharedEventSet: a typed record collecting the subset of substrate events agreed upon across all contesting mythoi (E_travel through E_intercourse). Currently the canonical-floor status is expressed only in prose annotations; a typed surface would let the dialect formally distinguish contested from uncontested events within an ArMythosRelation."

**Forcing-function analysis.** A10's `over_event_ids` names the contested events. The dual concept — events *agreed upon* across all participating mythoi — is derivable (intersection of the mythoi's `central_event_ids`), but not typed. The v1 probe flagged "canonical floor" as *drift* (system-internal term); sketch-02's A10 admitted the term into the dialect implicitly via `over_event_ids`, but did not type the shared-agreement side of the contest.

**Possible response directions:**
- A derived (not authored) helper: `canonical_floor(relation, mythoi) -> set[event_id]` computes the intersection at verify-time. No new record.
- A new record `ArSharedEventSet` paired to each `ArMythosRelation(kind="contests")`. Authored declaration; author states "these events are agreed; contest is over arrangement."
- Extend `ArMythosRelation` with a `shared_event_ids` field parallel to `over_event_ids`.

Defer the decision until a second contest-kind encoding surfaces (Rashomon-like works are unusual — Akutagawa's other Rashomon-derivatives, court-case multi-testimony works).

### Rashomon probe: ArProseOnlyCause

> "ArProseOnlyCause: a typed marker within an ArPhase for causal elements that are structurally load-bearing but exist only in prose (not in the substrate event model). The wife's 'gaze of contempt' is the paradigm case."

**Forcing-function analysis.** One of the Rashomon prose reviews flagged the wife's mythos middle-phase annotation as naming an emotional driver (the husband's gaze) that exists only in prose. The substrate doesn't model gaze-directions or emotional reactions — those live in Descriptions. A typed surface that says "this phase's arrangement depends on a non-substrate causal element named here" would let the probe flag the absence explicitly rather than as drift-adjacent.

**Tension with grid-snap.** This proposal sits exactly on the architecture-sketch-01 A3 boundary between structural facts (typed) and interpretive content (Descriptions). `ArProseOnlyCause` is proposing to *type the admission* that something is prose-only — a kind of meta-structural marker. That's an architectural decision sketch, not a casual extension.

**Recommendation:** defer. This one wants a wider design discussion about how the dialect acknowledges what it doesn't model. A hypothetical sketch-03 would need to examine whether the right answer is (a) a typed ArProseOnlyCause marker, (b) a Description.kind convention (e.g., `kind="aristotelian-prose-only-cause"`), or (c) accept the probe's current behavior (flag as scope limit) as honest enough.

### Rashomon probe: peripeteia-in-beginning scope-limit (narrower observation)

Not a relations_wanted, but a new scope_limits_observed item:

> "Peripeteia in the beginning phase: the wife's mythos places its peripeteia_event_id (E_intercourse) within the beginning phase's scope_event_ids. Aristotelian vocabulary expects reversals to occur in the middle or at the transition to denouement; having a reversal in the beginning stretches the structural model, though it is defensible as encoding how the assault is both a canonical-floor event and the wife's distinctive reversal."

**Forcing-function analysis.** The wife-mythos places `E_intercourse` (τ_s=2, in the shared canonical-floor) as its peripeteia. The sketch-01 encoding chose this to express that the wife's account reads the assault itself as the reversal. v2 flags it as structural strain — reversals in Aristotle typically land in the middle, not the beginning.

Two options: (a) amend the wife-mythos encoding to place the peripeteia elsewhere (but that changes the authorial claim about the wife's reading); (b) add a soft verifier check — "peripeteia in beginning phase emits NOTED, not advises-review." The sketch-02 verify path emits no such check today. Defer unless a second encoding repeats the pattern.

## What sketch-02 got right and what it didn't name

**Got right:**

- Closing the three well-forced proposals produced their closure. The probe's v2 reading *uses* the new records (not just tolerates them), which is the strongest closure signal.
- Deferring ArFrameMythos correctly. The gap is real but substrate-blocked, as sketch-02 named.
- Rejecting ArAnagnorisisLevel correctly. The probe re-surfaces the pressure under a new name, confirming it's genuine — but also confirming sketch-02's stance that admitting it would be a sketch-01 scope amendment.

**Didn't anticipate:**

- The *second-order* findings (pathos; canonical-floor typing; prose-only cause markers) would emerge so fast. Sketch-02 anticipated that closing the three would clear the probe's attention; it didn't anticipate the probe would immediately point at Aristotle's own triad completion (pathos).
- The `drift_flagged` list would go from 5 items (v1) to 0 items (v2). Sketch-02 didn't predict this — drift items are noise at the prompt level, but their elimination is a real shift in how the probe engaged.

## Disposition of new findings

None land as sketch-02 amendments. All stay banked with forcing-function criteria, per the project's standing OQ discipline. The next Aristotelian probe sketch (sketch-03) would be the home if forcing functions arrive:

- **ArPathos / catharsis grounding (OQ-AP1).** Forcing: either a second Aristotelian encoding where pathos placement is disputed, OR a cross-dialect Lowering sketch needing to bind catharsis to Dramatica's Story_consequence.
- **ArCanonicalFloor / ArSharedEventSet (OQ-AP2).** Forcing: a second contest-kind encoding (Rashomon-derivative, legal-testimony work).
- **ArProseOnlyCause (OQ-AP3).** Forcing: a wider architectural discussion sketch about how the dialect admits what it doesn't model. Not small.
- **Peripeteia-in-beginning soft check (OQ-AP4).** Forcing: a second encoding where peripeteia lands outside the middle phase. Otherwise author-side only.
- **ArAudienceAnagnorisis (explicit reject from sketch-02).** Forcing: a sketch-01 amendment opening A4/A8. Not a sketch-03 concern unless the A4/A8 revisit happens first.

Closes sketch-01 OQ1 at finer grain (pathos + catharsis-grounding as separable requests, not a single ArAffect) — still banked, not closed.

## Acceptance criteria

Labels **APA2-1** through **APA2-4** continue sketch-01's APA1–APA7.

- **[APA2-1]** Two JSON artifacts saved at `prototype/`:
  `reader_model_oedipus_aristotelian_output_v2.json` +
  `reader_model_rashomon_aristotelian_output_v2.json`. v1 files
  preserved unchanged. **DONE.**
- **[APA2-2]** Predictions P1–P5 evaluated against v2 output with
  PASS/FAIL verdicts explicitly recorded here. **DONE** (all
  PASS; P4 Rashomon strengthened from partial to yes).
- **[APA2-3]** Closure ledger for each of v1's five
  `relations_wanted` entries: CLOSED / DEFERRED / REJECTED-WITH-
  PERSISTENCE. **DONE.**
- **[APA2-4]** New findings recorded as banked OQs with named
  forcing-function criteria. **DONE** (OQ-AP1..OQ-AP4).

No code / schema changes. No test changes.

## Summary

The re-probe verifies sketch-02's closure hypothesis. The three well-forced proposals close — the probe reads the new records and uses them structurally. The two held-out proposals behave as sketch-02 anticipated: ArFrameMythos persists as limit (correct per the deferral rationale); ArAnagnorisisLevel re-surfaces as ArAudienceAnagnorisis (correct per the rejection stance — the probe will keep pressuring what the dialect genuinely doesn't cover).

Three new forcing functions emerge — pathos + catharsis grounding (Oedipus), canonical-floor typing (Rashomon), prose-only-cause markers (Rashomon) — each finer-grained than v1's proposals and each with a clear forcing-function criterion for when a hypothetical sketch-03 should open.

Read_on_terms upgraded from `partial` to `yes` for Rashomon; drift_flagged went from 5 items to 0. The sketch-02 closure cleared the principal strain the dialect surface carried. Sketch-01's architectural verdict — extension-only, no core-record modification — extends cleanly through sketch-02 and this re-probe.

If future arcs surface forcing functions for OQ-AP1..OQ-AP4, sketch-03 is the home. No current commitment to open one.
