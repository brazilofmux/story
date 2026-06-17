# Aristotelian dialect — sketch 06 (secondary_peripeteia_event_ids on ArMythos; anagnorisis_qualifier on ArAnagnorisisStep; A7.15 check 6 paired-polarity-concordance)

**Status:** landed; Session-6 re-probe verified closure
**Date:** 2026-06-16
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [aristotelian-sketch-01](aristotelian-sketch-01.md) A1–A9, [aristotelian-sketch-02](aristotelian-sketch-02.md) A10–A12, [aristotelian-sketch-03](aristotelian-sketch-03.md) A13–A14, [aristotelian-probe-sketch-04](aristotelian-probe-sketch-04.md) A15–A16, [aristotelian-sketch-05](aristotelian-sketch-05.md) A17–A18. All prior commitments unchanged.
**Frames:** [architecture-sketch-02](architecture-sketch-02.md), [aristotelian-sketch-03](aristotelian-sketch-03.md); `feedback_sketch_implement_rhythm_falsifies.md`; `feedback_research_production_alternation.md`
**Related:** Malfi research arc Sessions 1–5 (commits `0b5e0e3`→`bce79c4`, 2026-05-23→06) — primary forcing-function source; `prototype/reader_model_malfi_aristotelian_output.json` (Session-5 probe artifact, 15/15 approved); `prototype/story_engine/encodings/malfi_aristotelian.py` (the encoding carrying all three findings under semantic stretch) + `lear_aristotelian.py` (the second migration site for OQ-LEAR-4)
**Superseded by:** nothing yet

## Purpose

Close the three convergent forcing functions the *Duchess of Malfi* arc banked — two probe-validated in Session 5, one probe-surfaced new — as one coherent dialect amendment. Each finding currently lives in the encoding under an explicit *semantic stretch* of an existing apparatus; sketch-06 gives each its own typed home and removes the stretch.

- **OQ-LEAR-4 — Secondary peripeteia for one mythos's multiple tragic arcs. CROSS-ENCODING CONFIRMED.** Lear surfaced it with one encoding (Gloucester's blinding at τ_s=23 as a secondary peripeteia to Lear's stripping at τ_s=14, carried only in the prose of the parallel A13 relation). Webster pressures it with **four** structurally-distinct arc-peripeteia events in a single mythos — the Duchess at τ_s=17 (main slot), Ferdinand at τ_s=23 (collapsed into the main anagnorisis slot), Bosola at τ_s=24 and Antonio at τ_s=30 (both carried by `ArAnagnorisisStep` records that are not, strictly, anagnorises). The single `peripeteia_event_id` slot cannot carry four. Session 5's live probe proposed `ArMythos.secondary_peripeteia_event_ids` independently, matching the encoding's banked option #1. Sketch-06 ships it as **A19**.

- **OQ-MALFI-2 — Anti-anagnorisis (mis-recognition). NEW, probe-surfaced Session 5.** Antonio's dark-room death (τ_s=30): both parties recognize each other in the instant the mortal wound lands — the recognition is *real but too late to alter outcome*. The chain apparatus has a `step_kind` axis (parallel / precipitating / staging) but no axis for *whether the recognition is genuine, anti, or partial*. The Session-5 probe proposed `anagnorisis_qualifier: {genuine | anti | partial}`, citing Claudius's prayer-scene partial-recognition in *Hamlet* as an adjacent shape the corpus will eventually want. Sketch-06 ships it as **A20** on `ArAnagnorisisStep`.

- **OQ-MALFI-1 — Sequentially-wielded instrument with polarity *concordance*. Probe-validated Session 5.** Webster authors two `kind="instrumental"` A13 relations sharing target (Bosola) and polarity (malicious) but differing in wielder (Ferdinand vs Cardinal) and temporal phase (the play's primary commission vs pre-play galley service + Act-V re-employment). The sketch-05 A7.15 check 5 catches Lear's instrumental pair (shared target, *contrasting* polarity); it is silent on Webster's shared-target *concordant*-polarity pair. The Session-5 probe proposed the sibling check directly. Sketch-06 ships it as **A21** — A7.15 check 6, reusing the grouping check 5 already computes.

The sketch adds ONE new optional field on `ArMythos` (A19), ONE new optional field on `ArAnagnorisisStep` (A20), and ONE new self-verifier sub-check extending the A7.15 family (A21). Commitments A1–A18 are unchanged.

## Why now

The Malfi arc (Sessions 1–5) was the first cross-encoding instantiation of OQ-LEAR-4, and the Session-5 probe was the corpus's first 100%-approval run (15/15 annotation_reviews approved). It is *also* the first probe in the arc to validate two banked forcing functions AND surface a third in the same run, with the reader-model proposing concrete field shapes for all three:

1. It read four arc-peripeteia events in one mythos and independently proposed `secondary_peripeteia_event_ids` — matching the encoding's pre-registered option #1, not the per-phase or subplot-relation alternatives.
2. It read the Antonio dark-room beat as structurally distinct from a genuine recognition and proposed an `anagnorisis_qualifier` enum.
3. It distinguished Webster's concordant-polarity instrumental pair from Lear's contrasting pair and proposed the concordance sibling-check.

Per the Hamlet-Session-5 → sketch-03 and Lear-Session-5 → sketch-05 precedent (probe surfaces forcing with a proposed shape; the next sketch lands it end-to-end and migrates the exercising encodings), sketch-06's role is to land all three probe-proposed extensions and migrate the encodings that stretch to carry them today: Malfi (all three) and Lear (OQ-LEAR-4 second site only).

This also satisfies `feedback_research_production_alternation.md`: the last five substantive commits are research-mode (the Malfi probe arc); a dialect-landing sketch with schema follow-on is the production-leaning counter-swing.

## Scope — what this sketch does and doesn't do

**In scope:**

- **A19.** One new optional field on `ArMythos`:
  - `secondary_peripeteia_event_ids: Tuple[str, ...] = ()` — supplementary arc-peripeteia events beyond the singular `peripeteia_event_id`. Empty default preserves pre-sketch-06 silence.
- **A20.** One new optional field on `ArAnagnorisisStep`:
  - `anagnorisis_qualifier: str = ""` — `"" | "genuine" | "anti" | "partial"`; `""` is the back-compat default and is read as genuine/unspecified (no claim).
- **A7.17.** `secondary_peripeteia_event_ids` invariants (four checks, one severity level — advises-review).
- **A7.18.** `anagnorisis_qualifier` vocabulary check (one closed-enum check, advises-review on invalid; one noted on anti/partial co-located with `precipitates_main=True`).
- **A21 / A7.15 check 6.** Paired-non-canonical-polarity-*concordance* detection — sibling to sketch-05's check 5, emitting NOTED when ≥2 non-canonical directional records share kind + target + mythos + a single shared non-empty polarity.
- **Encoding migrations.** Malfi migrates the three post-main / collapsed arc-peripeteiai into `secondary_peripeteia_event_ids` and qualifies Antonio's step `anti`; Lear migrates Gloucester's blinding into `secondary_peripeteia_event_ids`. Oedipus / Rashomon / Macbeth / Hamlet verify identically (single-arc mythoi, no concordant instrumental pairs).

**Out of scope:**

- **OQ-AP7 (numerical range of BINDING_SEPARATED).** Three encodings now (Hamlet 9, Lear 14, Webster 6) under one `separated` category, with three analytical shapes (*delayed*, *accumulating*, *intense*). Re-surface is established but the candidate refinements (three-bucket categorical / raw-distance field / arc-shape enum) are not probe-proposed as a *required* extension — the reader read all three under `separated` without structural discomfort. **Stays banked**; a fourth encoding or a cross-dialect Lowering pressure is the forcing function.
- **OQ-MALFI-1 options 2 & 3 (`temporal_phase` field; `kind="instrument-transferred"`).** The probe validated option #1 (the check). The finer temporal-sequencing distinction (sequential vs concurrent wielding) and a dedicated transferred-instrument kind both add expressive surface the single Webster site does not yet force. **Stay banked** pending a third concordant-instrumental encoding.
- **`ArMythos`-level main `anagnorisis_qualifier`.** A20 sites the qualifier on `ArAnagnorisisStep` because the only anti/partial case in the corpus (Antonio) is a chain step. The main `anagnorisis_event_id` carries no qualifier; every corpus main-anagnorisis is genuine. A main-level qualifier is a clean future extension when a *main* recognition is anti/partial (no current forcing function).
- **`ArPhase`-level `peripeteia_event_id` (OQ-LEAR-4 option #2).** Rejected for the same reason the finding gave: three of Webster's four arc-peripeteiai co-locate in the end phase, so per-phase peripeteia collapses back into the multiplicity problem at smaller scope. A19's flat tuple is the cleaner shape.
- **`ArMythosRelation kind="subplot"` (OQ-LEAR-4 option #3).** Rejected: Webster's four arcs converge on the Duchess's death with no causal subordination — not subplot-shaped. Worst fit for the cross-encoding case.
- **Changes to A1–A18 semantics.** All prior fields + invariants preserved. A13's `kind` canonical set, A14's `step_kind` enum, A17's directionality/polarity vocabularies, A18's `anagnorisis_absent` all unchanged.
- **Cross-dialect Lowering (A9 unchanged).** None of the three new surfaces cross dialect boundaries.

## Commitments

### A19 — `ArMythos.secondary_peripeteia_event_ids`

A new optional `Tuple[str, ...]` field, default `()`. Names arc-peripeteia substrate events beyond the singular main `peripeteia_event_id`. The field is *orthogonal to the anagnorisis apparatus*: a single substrate event may legitimately be BOTH a secondary peripeteia (named here) AND an anagnorisis (named by the main `anagnorisis_event_id` or by a chain step). Webster's Ferdinand beat at τ_s=23 is exactly this — main anagnorisis and a secondary peripeteia at once.

**A7.17 checks** (all severity=advises-review unless noted):

1. **central-membership.** Each id ∈ `central_event_ids`. Code `secondary_peripeteia_event_not_central`.
2. **distinct-from-main.** No id equals `peripeteia_event_id` (redundant). Code `secondary_peripeteia_equals_main`.
3. **no-duplicates.** No id appears twice within the tuple. Code `secondary_peripeteia_duplicate`.
4. **substrate-resolution.** Each id resolves in `events_by_id` when substrate is threaded (skips when not, per the A7-check-4 discipline). Code `secondary_peripeteia_event_unresolved`.

Deliberately NOT checked: overlap with `anagnorisis_event_id` or chain-step event ids (orthogonal axes); any ordering constraint relative to the main peripeteia (a secondary peripeteia may precede or follow the main — Webster's three all follow; the dialect makes no temporal-ordering claim).

**Classification: extension.** New optional field on a core record, default empty; new verifier-local checks over existing substrate predicates. No core-record modification.

### A20 — `ArAnagnorisisStep.anagnorisis_qualifier`

A new optional `str` field, default `""`. Closed enum `{"", "genuine", "anti", "partial"}`:

- `""` — unspecified; read as genuine. Back-compat default; pre-sketch-06 chains verify unchanged.
- `"genuine"` — explicit genuine recognition (the ordinary case, made explicit when an author wants the contrast with a sibling anti/partial step visible).
- `"anti"` — mis-recognition / recognition-too-late: the recognition is real but arrives after it can alter outcome (Antonio's dark-room death).
- `"partial"` — incomplete recognition: the character grasps part of the truth (the probe's cited *Hamlet* Claudius-prayer shape; no corpus site yet, vocabulary pre-placed).

**A7.18 checks:**

1. **vocabulary.** `anagnorisis_qualifier ∈ {"", "genuine", "anti", "partial"}`; invalid → advises-review, code `anagnorisis_qualifier_invalid`.
2. **anti/partial informational co-location** (noted). An `anti` or `partial` step with `precipitates_main=True` emits NOTED `anagnorisis_qualifier_precipitates_noted` — an anti/partial recognition that *causes* the main genuine recognition is structurally unusual (not forbidden; Webster's anti step is non-precipitating, so this is silent for the corpus). Highlights the shape for author review.

**Classification: extension.** New optional field, default `""` preserving prior semantics; one vocabulary check + one informational check. No change to `step_kind` or any A14 invariant.

### A21 — A7.15 check 6 (paired-non-canonical-polarity-concordance)

Extends the sketch-05 A7.15 check family with a sibling to check 5. Check 5 already groups non-canonical directional relations by `(kind, target, mythos_id)` where `target = character_ref_ids[1]`, filtering to records with non-empty polarity. For each group of ≥2:

- **check 5 (sketch-05, unchanged):** if the group holds ≥2 *distinct* polarities → NOTED `character_arc_relation_paired_polarity_contrast`.
- **check 6 (NEW):** if the group holds exactly one shared polarity across ≥2 records → NOTED `character_arc_relation_paired_polarity_concordance`, naming all participating record ids and the shared polarity.

The two are mutually exclusive partitions of the same grouping (a group of ≥2 either has one polarity or more than one), so check 6 is a few lines in the existing loop, not a new pass.

**Classification: extension.** New verifier-local sub-check over existing fields; no new field, no record change.

## Encoding migrations

### Malfi (`malfi_aristotelian.py`) — all three findings

- **A19.** `AR_MALFI_MYTHOS.secondary_peripeteia_event_ids = ("E_ferdinand_views_corpse", "E_bosola_resolves_revenge", "E_bosola_kills_antonio")`. Main `peripeteia_event_id` stays `E_capture_in_countryside` (τ_s=17). The three end-phase arc-peripeteiai now have a typed home.
- **A20.** `AR_STEP_ANTONIO_DARK_RECOGNITION.anagnorisis_qualifier = "anti"`. `AR_STEP_BOSOLA_RESOLVES` may set `"genuine"` explicitly (its recognition is real) to make the contrast with the sibling anti-step visible, or leave `""`.
- **De-stretch the chain-step annotations.** The two post-main steps remain in `anagnorisis_chain` (they ARE recognitions — Bosola's explicit, Antonio's anti) but their annotations drop the "arc peripeteia the slot cannot carry" stretch language now that A19 carries the peripeteia content. The chain returns to purely-anagnorisic semantics; the OQ-LEAR-4 stretch is retired in prose, not just in structure.
- **A21.** No encoding change needed — `AR_FERDINAND_BOSOLA_INSTRUMENTAL` + `AR_CARDINAL_BOSOLA_INSTRUMENTAL` already share kind/target/mythos/polarity; check 6 fires on the existing records, upgrading the inspection-only observation in `OQ_MALFI_1_FINDING` to a machine-emitted NOTED.

### Lear (`lear_aristotelian.py`) — OQ-LEAR-4 second site only

- **A19.** `AR_LEAR_MYTHOS.secondary_peripeteia_event_ids = ("E_gloucester_blinded",)` (τ_s=23) — Gloucester's blinding, currently carried only in the prose of the parallel A13 relation, gets the typed home. The `arstep_gloucester_blinding` chain step stays (it is Gloucester's anagnorisis); the *peripeteia* aspect moves to the new field.
- No A20 change (Lear has no anti/partial recognition). No A21 change (Lear's instrumental pair is polarity-*contrast*, already caught by check 5).

### Untouched encodings

Oedipus, Rashomon, Macbeth, Hamlet author no `secondary_peripeteia_event_ids`, no anti/partial steps, and no concordant non-canonical instrumental pairs. All verify byte-identically under sketch-06 (regression surface).

## Architectural judgment (design-phase)

All three commitments are **extension-only** under architecture-sketch-02's stability test: two new optional fields with prior-preserving defaults, and one verifier-local sub-check over existing predicates. No core-record field is modified; no existing primitive's semantics change; no new substrate effect kind is introduced. Sketch-01's GREEN holds through A21.

The finding the migration makes load-bearing: the dialect's apparatus was *structurally complete but unevenly distributed* before sketch-06 — Webster's four arc-peripeteiai were spread across the main peripeteia slot, the main anagnorisis slot, two chain steps, and prose. A19 does not add expressive power the encoding lacked; it *redistributes* the same structural information onto one uniform apparatus, retiring three semantic stretches. This is the cleanest kind of dialect amendment: the encoding could already say it, but not in one voice.

Implementation is the second half of the test (acceptance criteria below). If code surfaces a gap the design missed — e.g., a check-6 grouping interaction with check 5, or an A19/chain-step orthogonality the verifier can't keep clean — the verdict is amended here and the architectural work resumes.

## Open questions

**Closed by this sketch:** OQ-LEAR-4 (A19 + two-site migration), OQ-MALFI-1 (A21), OQ-MALFI-2 (A20).

**Continuing (banked, unchanged):**

- **OQ-AP7** — range-of-separated. Three encodings, three shapes, one category. Forcing function: a fourth encoding whose distance is pathological under the single category, or cross-dialect Lowering pressure.
- **OQ-MALFI-1-b** (renamed from options 2/3) — `temporal_phase` field + `kind="instrument-transferred"`. Forcing function: a third concordant-instrumental encoding distinguishing sequential from concurrent wielding structurally.
- **OQ-AP1 / OQ-AP5 / OQ-AP6** and the audience-anagnorisis re-surfacing — unchanged from prior sketches.

**New (banked by this sketch):**

- **S6P-OQ1 — main-level `anagnorisis_qualifier`.** A20 sites the qualifier on chain steps only. When a corpus encoding's *main* anagnorisis is anti or partial (a tragedy whose central recognition is itself too-late — candidate: a revenge tragedy where the avenger recognizes the truth only as he dies), the qualifier wants a home on `ArMythos` beside `anagnorisis_event_id`. Pre-placed; no current site.
- **S6P-OQ2 — secondary-peripeteia ↔ secondary-anagnorisis binding.** A19 types secondary peripeteiai; A11 types supplementary anagnorises; A12 types the *main* peripeteia↔anagnorisis binding. There is no apparatus typing the binding between a *secondary* peripeteia and its corresponding recognition (Webster's Bosola beat is both, at one event — a "coincident" secondary binding). Forcing function: an encoding where a secondary peripeteia and its recognition are *separated* in τ_s, making the per-secondary binding structurally visible. Banked.

## Acceptance criteria

- **AA06-1.** A19 field added to `ArMythos`; A7.17's four checks implemented and wired into `verify`.
- **AA06-2.** A20 field added to `ArAnagnorisisStep`; A7.18's two checks implemented and wired.
- **AA06-3.** A7.15 check 6 added to `_check_character_arc_relation_sketch05_fields`, reusing the existing `by_key` grouping.
- **AA06-4.** Malfi migration: A19 tuple authored; Antonio step qualified `anti`; chain-step annotations de-stretched; check 6 fires on the existing instrumental pair.
- **AA06-5.** Lear migration: Gloucester blinding authored into `secondary_peripeteia_event_ids`.
- **AA06-6.** Oedipus / Rashomon / Macbeth / Hamlet verify byte-identically (regression).
- **AA06-7.** Test surface: new tests pin each A7.17 / A7.18 / check-6 path (clean + each violation) and the two migrations. Full stdlib core sweep green.
- **AA06-8.** Schema-layer landing (A19 field on `mythos.json`; A20 field on `anagnorisis_step.json`) — deferred to a follow-on PFS arc per the sketch-02/05 schema-deferral precedent, OR folded in if small. Decided at implementation time.
- **AA06-9 (Session 6 re-probe). DONE — closure verified.** See §Session-6 closure result below.

## Session-6 closure result (AA06-9)

Live re-probe ran 2026-06-16 (`claude-opus-4-6`, effort=high, max_tokens 21000; artifact `prototype/reader_model_malfi_aristotelian_session6_output.json`). Outcome: **all three findings read as closed; zero drift; attention moved to the next layer.**

- **C1 / OQ-LEAR-4 (A19) — CLOSED.** The dialect_reading rationale lists "secondary" among the live Aristotelian vocabulary it engaged ("peripeteia and anagnorisis including main, **secondary**, genuine, and anti qualifiers"). No secondary-peripeteia apparatus re-proposed.
- **C2 / OQ-MALFI-2 (A20) — CLOSED.** The probe read "an explicit anti-anagnorisis typing a recognition-too-late shape" as load-bearing; did not re-propose the qualifier enum.
- **C3 / OQ-MALFI-1 (A21) — CLOSED.** The observation commentary **endorsed** the machine-emitted `paired_polarity_concordance` note as "structurally load-bearing."
- **Read quality:** 13/15 annotation reviews approved, 0 rejected; 3 observation commentaries all *endorse*; `drift_flagged: []`. The 2 needs-work reviews were genuine prose-precision bugs (the end-phase annotation overclaimed the four-peripeteia structure as wholly contained in that phase; the Duchess–Antonio parallel relation's `over_event_ids` omitted the Duchess's strangling) — both fixed in the encoding this session, neither a dialect-scope signal.
- **`read_on_terms` moved `yes`→`partial`.** Honest, not a regression: with the surface findings closed, the probe surfaced genuine deeper scope-limits (below).

**Next-layer forcing functions surfaced (banked, none a closure failure):** these are authored as constants in `malfi_aristotelian.py` (`OQ_MALFI_3_FINDING`, `OQ_MALFI_4_FINDING`, `OQ_MALFI_1B_FINDING`) and join `OQ_FINDINGS`.

- **OQ-MALFI-3 — pathos-hero vs arc-hero split** (`ArMythos.pathos_character_ref_id`). Strongest new finding; corpus-first. When the pity-centre (Duchess) ≠ the main-anagnorisis character (Ferdinand), the dialect has no primitive naming the pathos-centre at mythos level.
- **OQ-MALFI-4 — instrument-reversal event** (`ArCharacterArcRelation.instrument_reversal_event_id`) with a verifier check that the reversal post-dates all wielding events.
- **OQ-MALFI-1B — temporal mode on concordant instrumentals** (`bracketing | continuous | episodic`). The probe re-proposed the OQ-MALFI-1 option-2/3 successor independently, refining check 6.

**Prediction honesty (design-first → probe-falsifies, at the OQ-prediction layer).** This sketch pre-banked two next-layer OQs — S6P-OQ1 (main-level qualifier) and S6P-OQ2 (secondary-peripeteia↔recognition binding). The probe surfaced *neither*; it surfaced OQ-MALFI-3/4/1B instead. S6P-OQ1/OQ2 remain plausible-but-unforced and stay banked unforced; the probe's actual next-layer attention is recorded above. The rhythm operated as expected: our forecast of *which* next-layer pressure would appear was wrong, and the probe data corrected it.
