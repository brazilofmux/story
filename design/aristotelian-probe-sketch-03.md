# Aristotelian probe — sketch 03 (Macbeth first-probe under sketch-02)

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (extension, not consolidation)
**Extends:** [aristotelian-probe-sketch-01](aristotelian-probe-sketch-01.md) — APS1–APS6 unchanged; [aristotelian-probe-sketch-02](aristotelian-probe-sketch-02.md) — closure ledger continues
**Frames:** [aristotelian-sketch-01](aristotelian-sketch-01.md), [aristotelian-sketch-02](aristotelian-sketch-02.md) (A10–A12 + A7.6–A7.9 surface)
**Related:** `prototype/reader_model_macbeth_aristotelian_output.json` (the artifact JSON this sketch reads); `prototype/demos/demo_aristotelian_reader_model_macbeth.py` (the demo invocation); `prototype/story_engine/encodings/macbeth_aristotelian.py` (the third Aristotelian encoding, landed in commit 1988222)
**Superseded by:** nothing yet

## Purpose

First live probe on the **third Aristotelian encoding** (Macbeth), landed under sketch-02's A1–A12 surface. Macbeth is structurally distinct from Oedipus and Rashomon in two cells of the binding × precipitates matrix:

- First corpus use of **BINDING_COINCIDENT** (peripeteia = anagnorisis = E_macduff_reveals_birth). Oedipus covered BINDING_SEPARATED; BINDING_ADJACENT remains uncovered.
- First corpus use of **non-precipitating** `ArAnagnorisisStep` (AR_STEP_LADY_MACBETH_SLEEPWALKING, `precipitates_main=False`). Oedipus's AR_STEP_JOCASTA had `precipitates_main=True`. Both A11 polarities now have corpus coverage.

Secondary purpose: test whether sketch-02-closed proposals stay closed on a third-encoding probe, and whether sketch-02's banked OQ-AP1..OQ-AP4 gain forcing-function evidence.

**The third-encoding probe is the generalization test** of sketch-02's closure claim. Sketch-02's re-probe verified that Oedipus + Rashomon readings cite the closed records structurally. A truly-held closure must survive an independent third encoding whose structural profile differs from both prior encodings — which is what Macbeth provides.

## Why now

Macbeth Aristotelian landed at commit 1988222; the probe runs same-day (2026-04-19, the continuing one-day cadence). Same-day probe is methodologically preferred — the encoding's author hasn't yet drift-corrected against the probe's likely findings, so the reading is honest.

## Scope — what this sketch covers

**In:**
- Execution of a fresh live probe on Macbeth under the sketch-02-extended client surface (unchanged from the Oedipus + Rashomon v2 runs).
- Prediction outcomes against sketch-01 APS6 P1 / P3 / P4 + sketch-02 OQ-AP1 (as P5-exploratory) + OQ-AP4 (as P6-exploratory).
- A **closure ledger extension** — for each sketch-02 closure (A10 / A11 / A12), test whether the Macbeth reading honors it structurally.
- New findings (scope_limits_observed, relations_wanted) surfaced for the first time on this third encoding.
- A **disposition map** — which banked OQs force, which stay banked, what new OQs surface.

**Out:**
- Changes to the probe client surface. No sketch-02 client amendment needed.
- New dialect commitments — if Macbeth pressures extensions, they land in a future aristotelian-sketch-03, not here.
- Ackroyd / ATTWN Aristotelian encodings. Still future work (ATTWN substrate-only per sketch-10; Ackroyd has no Aristotelian encoding yet).
- Re-probe of Oedipus / Rashomon. Sketch-02 already verified closure there.

## Prediction outcomes (sketch-01 APS6 + sketch-02 OQ extensions)

| # | Prediction | Macbeth outcome | Verdict |
|---|---|---|---|
| P1 | ≥ 80% approved, 0 rejected across the ≥5 prose reviews | **5/6 (83%) approved, 1 needs-work, 0 rejected** | **PASS** |
| P3 | `observation_commentaries` empty — Macbeth verifies with zero observations | Empty | **PASS** |
| P4 | `read_on_terms ∈ {yes, partial}`, `drift_flagged` empty or near-empty | **yes**, `drift_flagged` **empty** | **PASS (strongest)** |
| P5-exploratory (OQ-AP1) | If probe surfaces pathos-typing pressure, OQ-AP1 forces | **no pathos/catharsis/ArPathos tokens in scope_limits or relations_wanted** | **OQ-AP1 DOES NOT FORCE** |
| P6-exploratory (OQ-AP4) | If probe flags peripeteia placement as atypical, OQ-AP4 forces | **no peripeteia-placement tokens** | **OQ-AP4 DOES NOT FORCE** |

**The one `needs-work`** is on `ph_macbeth_beginning:annotation` — a **genuine prose error**: the annotation says "Cawdor award confirms the prophecy's first clause" when the Witches' first prophecy has three clauses (Glamis → Cawdor → king hereafter) and Cawdor confirms the **second**, not the first. This is an encoding cleanup item, not a dialect-surface concern — goes on the probe-surfaced cleanups list (state-of-play-11 research-track #6), does not open a dialect-amendment arc.

## Closure ledger extension — sketch-02's three closures under Macbeth

Sketch-02 committed to closing ArMythosRelation (A10), ArAnagnorisisChain (A11), and ArPeripeteiaAnagnorisisBinding (A12). Sketch-02's re-probe verified all three on Oedipus + Rashomon. Macbeth tests generalization to a third encoding:

### A10 ArMythosRelation — **NOT TESTED (no relations authored)**

Macbeth is single-mythos; no ArMythosRelation records authored; A7.6 / A7.9 checks skip. Closure remains verified on Rashomon (sketch-02); Macbeth neither stresses nor re-verifies it.

### A11 ArAnagnorisisChain — **CLOSURE VERIFIED on non-precipitating branch**

Macbeth's AR_STEP_LADY_MACBETH_SLEEPWALKING carries `precipitates_main=False` (Oedipus's AR_STEP_JOCASTA was `precipitates_main=True`). The probe reads the step correctly:

> "The ArAnagnorisisStep for Lady Macbeth's sleepwalking correctly stagers her character-level recognition from Macbeth's and records the non-causal relation via precipitates_main=False."

> (from the AR_LADY_MACBETH hamartia review) "The claim that her recognition does not precipitate Macbeth's is structurally confirmed by precipitates_main=False in the ArAnagnorisisStep, and the Jocasta contrast stays cleanly within Aristotelian reference."

**Closure type:** authored + structurally load-bearing + generalizes from Oedipus's precipitating case to Macbeth's non-precipitating case. The field reads correctly in both polarities. A11 closure verified beyond the Oedipus case.

### A12 ArPeripeteiaAnagnorisisBinding — **CLOSURE VERIFIED on coincident branch**

Macbeth uses `peripeteia_anagnorisis_binding = BINDING_COINCIDENT` (peripeteia_event_id = anagnorisis_event_id = E_macduff_reveals_birth). Oedipus used `BINDING_SEPARATED`. The probe reads the coincident case correctly:

> "The coincident peripeteia and anagnorisis at E_macduff_reveals_birth, which the peripeteia_anagnorisis_binding='coincident' field makes explicit."

> "The complex-plot classification is justified by the coincident peripeteia and anagnorisis at E_macduff_reveals_birth, which the peripeteia_anagnorisis_binding='coincident' field makes explicit."

**Closure type:** authored + referenced multiple times in the probe's analysis + generalizes from Oedipus's separated case to Macbeth's coincident case. A12 closure verified beyond the Oedipus case. BINDING_ADJACENT remains uncovered in the corpus but has the same closure shape.

## New findings — proposals surfaced for the first time on Macbeth

Three findings. Each is recorded here with forcing-function analysis; none prompts an immediate sketch-03 dialect amendment.

### Finding 1 — Audience-level dramatic irony RE-SURFACES (third instance)

Macbeth probe scope_limits_observed:

> "Audience-level dramatic irony: the audience recognizes the Witches' equivocation well before Macbeth does (we hear 'none of woman born' and may suspect the loophole), but Aristotelian anagnorisis is character-level only — there is no primitive for the gap between audience recognition and character recognition, nor for the specific dramatic-ironic pleasure that gap generates."

**This is the third independent surfacing** of the audience-level-anagnorisis pressure:
- sketch-01 Rashomon v1: "audience-level anagnorisis (meta-anagnorisis)" in `relations_wanted`
- sketch-02 Rashomon v2: "ArAudienceAnagnorisis" (same pressure repackaged as ArMythosRelation modifier)
- sketch-03 Macbeth: "audience-level dramatic irony" (same pressure on a different encoding)

Three independent probe readings on three different encodings converge on this gap. Sketch-02 rejected `ArAudienceAnagnorisis` on sketch-01 A4/A8 scope grounds (reader-response territory). **The Macbeth re-surfacing confirms sketch-02's judgment extra-strongly**: the pressure is real, persistent, and encoding-independent — and it's still correctly outside sketch-01's committed scope. No new OQ. The rejection is genuine scope stance, not a punt.

**Interpretation for future sketches.** If a future arc considers amending sketch-01's A4/A8 to admit audience-level structure, this three-point re-surfacing is the strongest case for opening it. That's a sketch-01 amendment, not a probe-sketch-03 concern.

### Finding 2 — Supernatural agency under Aristotle's probability/necessity (NEW banked OQ-AP5)

Macbeth probe scope_limits_observed:

> "Supernatural agency and fate: the Witches occupy an ambiguous causal position (do they cause or merely predict?), and Aristotle's discussion of deus ex machina and probability/necessity (Poetics 1454a-b) does not cleanly map to agents whose prophecies are true but equivocal. The encoding handles this through prophecy-type events, but the Witches' structural role as equivocating fate-agents has no dedicated Aristotelian primitive."

**Genuinely new scope-limit.** Aristotle's 1451a εἰκός / ἀναγκαῖον (probability / necessity) and 1454a–b deus-ex-machina discussions are the classical Aristotelian treatments of causal-agency-in-plot. The Witches' structural role — equivocating fate-agents whose prophecies are *true but misleading* — occupies a region neither clean probability/necessity nor clean deus-ex-machina.

**Forcing-function criterion for a hypothetical ArFateAgent or ArProphecyStructure record (OQ-AP5).** Either (a) a second encoding with similar fate-agent ambiguity (Hamlet's Ghost, Greek chorus-as-fate, Cassandra), (b) a cross-dialect probe that needs to bind Dramatica's Antagonist / Contagonist roles to Aristotelian fate-agent categories, or (c) a verifier check wanting to distinguish "prophecy fulfilled by probability" from "prophecy fulfilled by equivocation." Banked.

**Rashomon's contest-kind relation vs. Macbeth's fate-agent pressure.** Sketch-02's A10 (ArMythosRelation) solves Rashomon's multi-testimony structure; ArFateAgent (hypothetical) would address a different axis — not between mythoi but within a mythos's causal architecture. These are non-overlapping gaps.

### Finding 3 — Intra-mythos parallel-character-arc relation (NEW banked OQ-AP6)

Macbeth probe relations_wanted:

> "ArMythosRelation kind='parallel' between Macbeth's and Lady Macbeth's tragic arcs within the single mythos — the anagnorisis_chain stagers their recognitions temporally, but a formal parallel-arc relation would express that both are tragic heroes with independent hamartiai converging on the same catastrophe without one precipitating the other."

**First corpus-surfaced intra-mythos structural pressure.** Sketch-02's A10 (ArMythosRelation) types **inter-mythos** friction — its `mythos_ids` tuple points at multiple ArMythos records. The Macbeth probe is asking for an **intra-mythos parallel-character-arc** relation — two tragic arcs *within* a single mythos, neither precipitating the other.

**Note on existing machinery.** Macbeth already carries this structure partially:
- Two ArCharacter records (AR_MACBETH, AR_LADY_MACBETH), both `is_tragic_hero=True`.
- One ArAnagnorisisStep (AR_STEP_LADY_MACBETH_SLEEPWALKING, `precipitates_main=False`), which the probe cites as "correctly stagers their character-level recognition … records the non-causal relation via precipitates_main=False."

The probe's reading acknowledges that the *non-precipitating* step encodes the non-causal relation; the relations_wanted then asks for a *formal* parallel-arc relation that would make the structural claim more explicit than the negation-of-precipitation currently expresses.

**Forcing-function criterion for a hypothetical ArCharacterArcRelation or intra-mythos ArMythosRelation extension (OQ-AP6).** Either (a) a second encoding with ≥2 tragic heroes in a single mythos (Hamlet's prince + father; King Lear's Lear + Gloucester — the classical parallel-arc cases), (b) a verifier check wanting to distinguish "independent arcs converging" from "staggered single arc," or (c) a cross-dialect Lowering needing to bind Dramatica's IC (Impact Character) → Aristotelian's parallel-tragic-hero. Banked.

**Design tension.** Reusing A10's ArMythosRelation record with a `character_ids` or `sub_arc_ids` field would extend the record's meaning; a new record type (ArCharacterArcRelation) would keep A10 single-purpose. Premature to decide — the forcing function hasn't arrived.

## What sketch-03 got right and what it didn't anticipate

**Got right:**
- Predicted that A11 and A12 would generalize cleanly from their sketch-02 Oedipus/Rashomon exercise to Macbeth's complementary polarities (BINDING_COINCIDENT and non-precipitating step). The generalization held.
- Predicted that OQ-AP1 (pathos) and OQ-AP4 (peripeteia-in-beginning) would probably not force on Macbeth. Macbeth's peripeteia is firmly end-phase (OQ-AP4 quiescent as expected); Macbeth's pathos is scattered across three events (E_macduff_family_killed + E_lady_macbeth_dies + E_macbeth_killed) but the probe did **not** feel pressure for typed ArPathos — the scattering was absorbed within the implicit end-phase + scope-event pattern the sketch-02 surface admits. **Mild surprise**: the pre-probe hypothesis from the demo's docstring expected possible OQ-AP1 forcing; in practice the dialect handled Macbeth's scattered pathos without structural strain.

**Didn't anticipate:**
- The **third consecutive audience-level-anagnorisis re-surfacing**. Sketch-02 anticipated the re-surfacing on Rashomon; it did not anticipate that an encoding with no multi-narrator structure (Macbeth has a single narrative authority, not Rashomon's four testimonies) would pressure the same gap through dramatic irony rather than through meta-anagnorisis. The pressure is not Rashomon-structural; it's any-encoding-with-dramatic-irony-structural.
- The **intra-mythos parallel-character-arc pressure**. Sketch-02 banked second-order OQs around A10's extension (ArCanonicalFloor, ArProseOnlyCause), all inter-mythos-adjacent. The intra-mythos axis (OQ-AP6) is a new extension direction sketch-02 didn't anticipate.
- The **supernatural-agency scope limit**. Sketch-02 banked OQ-AP3 (ArProseOnlyCause) for prose-only causal elements; OQ-AP5 is adjacent but different — fate-agents are *structural* causal elements (the Witches drive the plot) whose relationship to probability/necessity is unclassified rather than prose-only-absent.

## Disposition of new findings

Two new OQs banked; one re-surfacing documents sketch-02's rejection stance; one encoding cleanup:

- **OQ-AP5 — ArFateAgent / ArProphecyStructure (supernatural-agency scope).** Forcing: second encoding with fate-agent ambiguity, cross-dialect Lowering pressure, or verifier-check for probability-vs-equivocation distinction.
- **OQ-AP6 — Intra-mythos parallel-character-arc relation.** Forcing: second encoding with ≥2 tragic heroes in a single mythos (Hamlet, Lear), or cross-dialect IC-binding pressure.
- **ArAudienceAnagnorisis (three-point re-surfacing; not a new OQ).** Sketch-02's rejection stance is confirmed and strengthened — any amendment requires a sketch-01 A4/A8 revisit, not a sketch-03-level change. Recorded here as the third data point for a hypothetical future A4/A8 amendment.
- **Encoding cleanup — ph_macbeth_beginning:annotation prose error.** "First clause" → "second clause" re: Cawdor confirmation. Goes to the probe-surfaced-encoding-cleanups list (state-of-play-11 research #6). Author-side only; no dialect / schema impact.

Sketch-02's OQ-AP1..OQ-AP4 status updates:
- **OQ-AP1 (ArPathos) — stays banked.** Macbeth's scattered pathos did not force. The sketch-02 forcing criterion ("second encoding where pathos placement is ambiguous or disputed") did not trigger — the probe read Macbeth's end-phase + intermediate-phase scattering as within the admissible implicit-pathos space. Next potential forcer: a cross-dialect Lowering pressuring typed pathos, or a fourth encoding with more radical pathos displacement.
- **OQ-AP2 (ArCanonicalFloor) — stays banked; not pressured (Macbeth has no contest-kind structure).**
- **OQ-AP3 (ArProseOnlyCause) — stays banked; not pressured by Macbeth (Macbeth's "gaze-of-contempt"-style prose-only drivers are not structurally load-bearing in the same way Rashomon's were).**
- **OQ-AP4 (peripeteia-in-beginning) — stays banked; not pressured (Macbeth's peripeteia is end-phase, sketch-02-predicted).**

## Acceptance criteria

Labels **APA3-1** through **APA3-5** extend sketch-02's APA2-1..APA2-4.

- **[APA3-1]** One JSON artifact saved at `prototype/reader_model_macbeth_aristotelian_output.json`. No prior Macbeth Aristotelian probe file existed; no pre-existing file to preserve. **DONE.**
- **[APA3-2]** Predictions P1 / P3 / P4 + P5-exploratory (OQ-AP1) + P6-exploratory (OQ-AP4) evaluated against the probe output with PASS/FAIL verdicts explicitly recorded here. **DONE** (all standard predictions PASS; both exploratory predictions report "does not force").
- **[APA3-3]** Closure ledger extension — sketch-02's A10 / A11 / A12 retested on Macbeth's structurally-complementary profile. **DONE** (A11 and A12 verified on new polarities; A10 not tested — Macbeth is single-mythos).
- **[APA3-4]** New findings recorded as banked OQs with named forcing-function criteria. **DONE** (OQ-AP5 supernatural-agency; OQ-AP6 intra-mythos parallel-character-arc).
- **[APA3-5]** Sketch-02 OQ-AP1..OQ-AP4 status updates recorded. **DONE** (all four stay banked under Macbeth; sketch-02's criteria remain in effect).

No code / schema changes. No test changes.

## Summary

The Macbeth probe is the **third-encoding generalization test** of sketch-02's closure. Sketch-02 verified on Oedipus + Rashomon; sketch-03 verifies the same closures generalize to a structurally-complementary third encoding (BINDING_COINCIDENT + non-precipitating anagnorisis step — cells not exercised by the prior two encodings).

All standard predictions PASS (P1 / P3 / P4). The single `needs-work` verdict is a real encoding prose error (cleanup item, not dialect pressure). Both exploratory predictions for banked OQ forcing — OQ-AP1 pathos-typing and OQ-AP4 peripeteia-in-beginning — report DOES NOT FORCE. All sketch-02 banked OQs stay banked; sketch-02's rejection stance on ArAudienceAnagnorisis is confirmed extra-strongly by a third independent re-surfacing.

Two new second-order OQs bank forward: OQ-AP5 (supernatural-agency under Aristotle's probability/necessity; new scope-limit unique to fate-agent encodings) and OQ-AP6 (intra-mythos parallel-character-arc relation; new extension axis distinct from sketch-02's inter-mythos A10).

**Sketch-02's amendment-only posture continues to hold.** Three encodings now verify clean under A1–A12; the sketch-02 closures read as load-bearing structural elements across all three; the probe's attention moves progressively to finer-grained second-order concerns (OQ-AP1..OQ-AP6 now span six banked extensions, each with a distinct forcing function).

If a future arc surfaces forcing-function evidence for OQ-AP5 or OQ-AP6, aristotelian-sketch-03 would be the home. No current commitment to open one.
