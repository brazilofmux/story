# Aristotelian dialect — sketch 07 (pathos_character_ref_ids on ArMythos; pathos_carrier on ArCharacter; A7.19 pathos-centre concordance)

**Status:** landed; Session-7 re-probe verified closure (both sites)
**Date:** 2026-06-17
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [aristotelian-sketch-01](aristotelian-sketch-01.md) A1–A9, [aristotelian-sketch-02](aristotelian-sketch-02.md) A10–A12, [aristotelian-sketch-03](aristotelian-sketch-03.md) A13–A14, [aristotelian-probe-sketch-04](aristotelian-probe-sketch-04.md) A15–A16, [aristotelian-sketch-05](aristotelian-sketch-05.md) A17–A18, [aristotelian-sketch-06](aristotelian-sketch-06.md) A19–A21. All prior commitments unchanged.
**Frames:** [architecture-sketch-02](architecture-sketch-02.md), [aristotelian-sketch-03](aristotelian-sketch-03.md); `feedback_sketch_implement_rhythm_falsifies.md`; `feedback_research_production_alternation.md`
**Related:** Revenger's Tragedy research arc Sessions 1–5 (commits `6693c6c`→`da79992`, 2026-06-16) — primary forcing-function source; `prototype/reader_model_revengers_aristotelian_output.json` (Session-5 probe artifact proposing both shapes); `prototype/story_engine/encodings/revengers_tragedy_aristotelian.py` (the encoding carrying the pathos-centre under semantic stretch) + `malfi_aristotelian.py` (the OQ-MALFI-3 origin site, second migration target); [state-of-play-16](state-of-play-16.md)
**Superseded by:** nothing yet

## Purpose

Close **OQ-MALFI-3** — the pathos-hero vs arc-hero split — as one coherent dialect amendment. The finding is the strongest the corpus has banked that is *both* probe-surfaced *and* cross-encoding-confirmed with a proposed shape: Malfi surfaced it (the Duchess is the pity-centre, Ferdinand the recognizer), and the Revenger's Tragedy re-forced it harder (Gloriana is a dead, arc-less, prop-borne pathos-centre; the avenger Vindice is morally corroded and hard to pity). The Session-5 Revenger's probe read the encoding fully on dialect terms, identified the pathos-centre gap as the *only* vocabulary strain, and independently proposed both shapes this sketch lands.

Today the pathos-centre claim lives under *semantic stretch*: an encoding can author the pity-object as an `ArCharacter`, but the dialect has no field naming it as the mythos's pathos-centre, so the claim survives only in annotations, the `action_summary`, the `OQ_MALFI_3_FINDING` constant, and (in the Revenger's) an overloaded `kind="parallel"` `ArCharacterArcRelation`. Sketch-07 gives the pathos-centre its own typed home and retires the stretch — the same redistribution sketch-06 performed for the secondary peripeteia.

The sketch adds ONE new optional field on `ArMythos` (A22), ONE new optional field on `ArCharacter` (A23), and ONE new self-verifier check (A7.19). Commitments A1–A21 are unchanged.

## Why now

The Revenger's Tragedy arc (Sessions 1–5, SoP-16) was the second cross-encoding instantiation of a banked finding, and its Session-5 probe was the corpus-cleanest run (0 observations; `read_on_terms=yes`; drift empty; 7/8 annotation reviews approved). Decisively:

1. It read the pathos-centre gap as the **only** vocabulary strain in an otherwise clean encoding, grounding it in Aristotle's own *pathos* (Poetics 1452b: "a structural-field gap, not a vocabulary failure").
2. It independently proposed **`ArMythos.pathos_character_ref_ids`** — explicitly a LIST/tuple (matching the encoding's pre-registered option #1 over the singular), naming "characters or objects that carry the play's pity-and-fear without possessing arcs of their own."
3. It independently proposed the companion **`ArCharacter.pathos_carrier: bool`** — "a character-level flag distinguishing pity-objects from arc-agents."
4. It recognised all three forcing axes (total split, non-agentive centre, distributed centre) including the stretch itself ("forced to overload ArCharacterArcRelation as a workaround").

This is the exact maturity that justified sketch-06: probe-surfaced **and** re-confirmed at a harder second site **with** a concrete proposed shape. Per the established precedent (probe surfaces forcing with a proposed shape → the next sketch lands it end-to-end and migrates the exercising encodings), sketch-07's role is to land both proposed surfaces and migrate the two encodings that stretch to carry them today: Revenger's (distributed, arc-less centre) and Malfi (single, arc-bearing centre split from the recognizer).

It also satisfies `feedback_research_production_alternation.md`: the last six commits are research-mode (the Revenger's arc); a dialect-landing sketch with a schema follow-on is the production-leaning counter-swing.

## Scope — what this sketch does and doesn't do

**In scope:**

- **A22.** One new optional field on `ArMythos`:
  - `pathos_character_ref_ids: Tuple[str, ...] = ()` — the mythos's pathos-centre(s), each id referencing an `ArCharacter` in `characters` by `.id`. Empty default preserves pre-sketch-07 silence.
- **A23.** One new optional field on `ArCharacter`:
  - `pathos_carrier: bool = False` — character-level pathos-carrier flag. `False` is the back-compat default.
- **A7.19.** Pathos-centre integrity + A22/A23 concordance (four checks: resolution, no-duplicates, named⇒flagged — all advises-review; flagged⇒named — noted).
- **Encoding migrations.** Revenger's authors `pathos_character_ref_ids=("ar_gloriana", "ar_antonio_wife")` with `pathos_carrier=True` on both, and de-stretches `AR_PATHOS_CLUSTER_PARALLEL`. Malfi authors `pathos_character_ref_ids=("ar_duchess",)` with `pathos_carrier=True` on the Duchess. Oedipus / Lear / Rashomon / Macbeth / Hamlet verify identically (no pathos-centre authored).

**Out of scope:**

- **A pathos↔anagnorisis binding / split-marking check.** A7.19 deliberately does NOT mark the *split* (pathos-centre ≠ tragic hero / ≠ recognizer) as a finding — the split and the coincidence are both valid Aristotelian shapes, and a NOTED firing on every split-encoding would be editorial noise. Whether the corpus eventually wants an explicit "pathos-split" signal is banked as **S7P-OQ1** below; no current forcing function (the field's mere presence + disjointness from `is_tragic_hero` already expresses the split readably).
- **`pathos_intensity` / distributed-vs-singular typing.** The Revenger's distributes pathos across two carriers; Malfi concentrates it on one. A22's flat tuple expresses both (length 1 vs 2) without a typed distinction. A categorical distributed/concentrated field is unforced — banked as **S7P-OQ2**.
- **Pathos at substrate/Lowering scope.** A22/A23 are dialect-local. No cross-dialect Lowering surface is added (A9 unchanged).
- **Changes to A1–A21 semantics.** All prior fields + invariants preserved. `is_tragic_hero`, `anagnorisis_character_ref_id`, A13 relations, the A7.15 check family — all unchanged. A22/A23 are orthogonal additions.
- **OQ-AP7, OQ-MALFI-1B, OQ-MALFI-4, S6P-OQ1** — unchanged from SoP-16; not pressured here.

## Commitments

### A22 — `ArMythos.pathos_character_ref_ids`

A new optional `Tuple[str, ...]` field, default `()`. Names the character(s) carrying the mythos's *pathos* — the pity-and-fear centre (Poetics 1452b) — each id referencing an `ArCharacter` in `characters` by `.id` (the convention the anagnorisis chain steps already use). The field is **orthogonal** on two axes:

- *Orthogonal to `anagnorisis_character_ref_id`:* the pathos-centre may BE the recognizer, or be split from it. Malfi's Duchess (pathos) ≠ Ferdinand (recognizer) is the split; an encoding where the suffering hero also recognizes is the coincidence. A7.19 forbids neither.
- *Orthogonal to `is_tragic_hero`:* the pathos-centre may be the tragic hero (Malfi's Duchess is both), or bear no arc at all (the Revenger's Gloriana — dead before the play, present only as a skull-prop). A22 admits arc-less, non-agentive referents; there is no arc requirement.

**A7.19 checks** (severity=advises-review unless noted):

1. **resolution.** Each id ∈ `pathos_character_ref_ids` resolves to an `ArCharacter` in `characters` (by `.id`). Code `pathos_character_unresolved`.
2. **no-duplicates.** No id appears twice. Code `pathos_character_duplicate`.
3. **named ⇒ flagged.** A resolved referent with `pathos_carrier=False` → the A22 (mythos) and A23 (character) surfaces disagree. Code `pathos_character_not_flagged`.
4. **flagged ⇒ named (noted).** An `ArCharacter` in `characters` with `pathos_carrier=True` that is NOT named in `pathos_character_ref_ids` → NOTED `pathos_carrier_not_in_mythos_list`. NOTED, not advises-review: a character may self-declare while a given mythos's centre-list is narrower (e.g. a character shared across mythoi). The asymmetry encodes the authoritative-list-with-character-echo design.

Deliberately NOT checked: distinctness from / coincidence with the anagnorisis character or the tragic-hero set (both shapes valid); any arc requirement (arc-less referents are the point).

**Classification: extension.** New optional field on a core record, default empty; new verifier-local checks over existing predicates + one new optional field. No core-record modification.

### A23 — `ArCharacter.pathos_carrier`

A new optional `bool` field, default `False`. An authorial claim that the character carries the play's pity-and-fear. `False` is the back-compat default; pre-sketch-07 characters verify unchanged. Orthogonal to `is_tragic_hero` (a character may be both, either, or neither). A23 is the character-local echo of the mythos-level A22 claim; A7.19 check 3 enforces that a named pathos-centre carries the flag.

**Classification: extension.** New optional field, default `False` preserving prior semantics. No change to any A5 invariant.

### A7.19 — pathos-centre integrity + concordance

The four checks above. The two concordance checks (3 and 4) make A22 and A23 load-bearing *together*: the mythos-level list is the authoritative pathos-centre claim, and the character-level flag is its echo; A7.19 keeps them in sync (asymmetrically — naming demands the flag; flagging merely suggests naming).

**Classification: extension.** Verifier-local check over the two new fields + existing `characters`; no record change beyond A22/A23.

## Encoding migrations

### Revenger's Tragedy (`revengers_tragedy_aristotelian.py`) — the distributed, arc-less centre

- **A22.** `AR_REVENGERS_MYTHOS.pathos_character_ref_ids = ("ar_gloriana", "ar_antonio_wife")` — the two pure pity-objects the Session-5 probe's own proposed field listed. Castiza is excluded (the probe read her as arc-bearing, not a pure pity-object; the Session-5 narrowing already aligned the relation to these two).
- **A23.** `pathos_carrier=True` on `AR_GLORIANA` and `AR_ANTONIO_WIFE`; `AR_CASTIZA` stays `False` (bordering case, deliberately omitted — no spurious check-4 NOTED).
- **De-stretch `AR_PATHOS_CLUSTER_PARALLEL`.** The pathos-centre content moves to A22; the relation either retires or has its annotation de-stretched to drop the "the dialect has no other way to mark it / semantic stretch" language now that A22 carries the claim. Decision at implementation: retire the relation (it existed *only* to give the pathos-centre structural footing) — A22 is its proper home, so removing it is the honest de-stretch, parallel to sketch-06 retiring the OQ-LEAR-4 chain-step stretch language.

### Malfi (`malfi_aristotelian.py`) — the single, arc-bearing centre split from the recognizer

- **A22.** `AR_MALFI_MYTHOS.pathos_character_ref_ids = ("ar_duchess",)` — the Duchess, the principal pathos site, named at mythos level. The split A22 makes explicit is pathos-centre (Duchess) vs `anagnorisis_character_ref_id` (Ferdinand the recognizer).
- **A23.** `pathos_carrier=True` on `AR_DUCHESS` — who is *also* `is_tragic_hero=True`. This is the corpus case proving A22/A23 orthogonality to `is_tragic_hero`: the pathos-centre that *is* an arc-bearing hero, contrasted with the Revenger's arc-less centre.
- **OQ_MALFI_3_FINDING → CLOSED** in both encodings, with a closure note pointing at sketch-07 and the Session-7 re-probe.

### Untouched encodings

Oedipus, Lear, Rashomon, Macbeth, Hamlet author no `pathos_character_ref_ids` and no `pathos_carrier` flags. All verify byte-identically under sketch-07 (regression surface). (Lear is a candidate *future* migration — Cordelia/Gloucester as pathos-centres distinct from Lear — but is out of scope here; sketch-07 migrates only the two OQ-MALFI-3 forcing sites.)

## Architectural judgment (design-phase)

Both commitments are **extension-only** under architecture-sketch-02's stability test: two new optional fields with prior-preserving defaults (`()` and `False`), and one verifier-local check over existing predicates plus the two new fields. No core-record field is modified; no existing primitive's semantics change; no new substrate effect kind is introduced. Sketch-01's GREEN holds through A23.

The finding the migration makes load-bearing: before sketch-07 the dialect was *expressively incomplete* for the pathos-split — it could name a pity-object as a character but had no way to say "this character is the mythos's pathos-centre" except by overloading a relation type built for arc-bearing agents. A22 does not add a concept the corpus lacked (every encoding already *had* a pathos-centre); it gives the existing concept a typed home and retires the overload. This is the same clean amendment shape as sketch-06: the encoding could already say it, but not in one voice.

Implementation is the second half of the test (acceptance criteria below). If code surfaces a gap the design missed — e.g. an A7.19 concordance interaction with multi-mythos shared characters, or an A22/`is_tragic_hero` orthogonality the verifier can't keep clean — the verdict is amended here and the architectural work resumes.

## Open questions

**Closed by this sketch:** OQ-MALFI-3 (A22 + A23 + two-site migration).

**Continuing (banked, unchanged from SoP-16):**

- **S6P-OQ1** — main-level `anagnorisis_qualifier`. Banked unforced (predicted twice, falsified twice). Needs a tragedy whose MAIN recognition is unambiguously anti/partial.
- **OQ-MALFI-1B** — temporal mode on concordant instrumentals. Awaits a third concordant-instrumental encoding.
- **OQ-MALFI-4** — instrument-reversal event. Banked.
- **OQ-AP7** — range-of-separated. Conjectural.

**New (banked by this sketch):**

- **S7P-OQ1 — explicit pathos-split signal.** A7.19 does not mark the split (pathos-centre ≠ tragic hero / ≠ recognizer) as a finding. If a probe or a downstream consumer (the generator's tonal ranker; a decompile evaluator) wants the split surfaced as a typed property rather than inferred from field disjointness, a `pathos_split: bool` derived flag or a NOTED is the candidate. No current forcing function. Pre-banked as a hypothesis for the Session-7 re-probe to test (per the established "author-predicted next-OQs are reliably falsifiable" rule).
- **S7P-OQ2 — distributed-vs-concentrated pathos typing.** A22's flat tuple expresses distribution by length (Revenger's 2, Malfi 1) but does not *type* it. A categorical field (`concentrated | distributed`) or an intensity weight is the candidate if an encoding forces a structural distinction the length cannot carry. Banked.

## Acceptance criteria

- **AA07-1.** A22 field added to `ArMythos`; A23 field added to `ArCharacter`.
- **AA07-2.** A7.19's four checks implemented and wired into `verify`.
- **AA07-3.** Revenger's migration: A22 tuple `(ar_gloriana, ar_antonio_wife)`; `pathos_carrier=True` on both; `AR_PATHOS_CLUSTER_PARALLEL` de-stretched/retired; encoding verifies clean.
- **AA07-4.** Malfi migration: A22 tuple `(ar_duchess,)`; `pathos_carrier=True` on the Duchess (coexisting with `is_tragic_hero=True`); encoding verifies clean.
- **AA07-5.** Oedipus / Lear / Rashomon / Macbeth / Hamlet verify byte-identically (regression).
- **AA07-6.** Test surface: new tests pin each A7.19 path (clean + each violation: unresolved, duplicate, not-flagged, the noted flagged⇒named) and the two migrations. Full stdlib core sweep green.
- **AA07-7.** Schema-layer landing (A22 on `mythos.json`; A23 on `character.json`) — folded in (small), with conformance property-set pins, per the sketch-06 precedent that landed its schema fields in-arc.
- **AA07-8.** `OQ_MALFI_3_FINDING` updated to CLOSED in both encodings, pointing at sketch-07.
- **AA07-9 (Session-7 re-probe).** Live re-probe of both encodings verifying the pathos-centre reads as closed (no pathos field re-proposed; attention moves to the next layer). Filled in below on completion.

## Session-7 closure result (AA07-9)

Live re-probe ran 2026-06-17 (`claude-opus-4-6`, effort=high, max_tokens 21000) on **both** migration sites. Outcome: **OQ-MALFI-3 reads as closed at both sites; zero drift; the pathos field reads as load-bearing without strain; attention moved to the next layer.** Artifacts: `prototype/reader_model_revengers_aristotelian_session7_output.json`, `prototype/reader_model_malfi_aristotelian_session7_output.json`.

### Revenger's Tragedy (the harder, arc-less, distributed site)

`read_on_terms=yes`; `drift_flagged=[]`; 6/7 annotation reviews approved, 0 rejected; 0 observation commentaries (verifies clean). The dialect_reading is explicit that A22 closes the gap:

> "The sketch-07 `pathos_character_ref_ids` field is tested with a strong forcing case: Gloriana is a skull, dead nine years before the play; Antonio's wife kills herself in Act I. Neither has agency or arc, yet the field expressively names them as pathos-centres **without requiring arc machinery** — the field's cardinality (list) and its orthogonality to `anagnorisis_character_ref_id` are both **confirmed as correct**."

No pathos field re-proposed. The probe also listed pathos among the "core Poetics apparatus … deployed precisely and without strain" alongside mythos/peripeteia/anagnorisis/hamartia.

### Malfi (the surfacing site; the coincidence case)

`read_on_terms=yes`; `drift_flagged=[]`; 14/15 approved, 0 rejected. The dialect_reading:

> "pathos (Duchess as named carrier via sketch-07's `pathos_character_ref_ids`) … The sketch-07 pathos field works here **without strain**: the Duchess is unambiguously the pity-and-fear centre, and the field's coarseness (names who, not how or when) **does not impede the read**."

No pathos field re-proposed. The "names who, not how or when" remark gently acknowledges S7P-OQ2 (distributed/concentrated or intensity typing) as a *possible* future refinement while explicitly declining to force it — exactly its banked status.

### Prediction honesty (design-first → probe-falsifies, at the OQ-prediction layer)

This sketch pre-banked two next-layer OQs — **S7P-OQ1** (explicit pathos-split signal) and **S7P-OQ2** (distributed-vs-concentrated typing). The probe surfaced *neither* as a demand. This is the fourth consecutive instance of the rule (sketch-06's S6P-OQ1/OQ2; the Revenger's arc's S6P-OQ1; now S7P-OQ1/OQ2): **author-predicted next-layer pressures are reliably falsifiable and usually unforced; probe-surfaced findings re-confirm.** OQ-MALFI-3 (probe-surfaced in Malfi Session 6) was re-forced and held, then closed — the asymmetry holds again.

### Next-layer forcing functions surfaced (banked, none a closure failure)

The probes' attention moved to genuinely new gaps, recorded here for future second-site forcing:

- **S7P-OQ3 — `memorial` / `debt` ArCharacterArcRelation kind** (Revenger's probe). A directional relation from a living agent to a *dead, non-agentive* character whose death is the living agent's motive force (Vindice → Gloriana — motivation, memorial, and literal weapon). Distinct from parallel/mirror/foil (which presuppose two arcs); the dead referent is also the pathos-centre, so it "would pair naturally with `pathos_character_ref_ids`." Strongest new finding; probe-surfaced unprompted.
- **S7P-OQ4 — `ArMythos.peripeteia_character_ref_id`** (Malfi probe). A field parallel to `anagnorisis_character_ref_id` naming the character whose arc carries the *main peripeteia*, for mythoi where peripeteia and anagnorisis land on different characters (Malfi: the Duchess's reversal vs Ferdinand's recognition). The binding axis (A12) is temporal only; the character axis is currently inferred. Adjacent to — but distinct from — the falsified S7P-OQ1.
- **S7P-OQ5 — ternary instrumental** (`target_of_instrument_ref_id` on `ArCharacterArcRelation`) (Malfi probe). The wielder→instrument→victim triple (Ferdinand→Bosola→Duchess) exceeds the two-slot `character_ref_ids`. This is the OQ-MALFI-4 family, re-surfaced.
- **OQ-MALFI-1B re-confirmed** — both probes re-proposed a temporal-ordering field on same-kind relations (`temporal_relation: precedes | concurrent | succeeds`) for the Cardinal-then-Ferdinand diachronic instrumentalism. Already banked; this is its third independent surfacing.
- **S7P-OQ6 — `catharsis_mode` / `ArCatharsis` record** (Revenger's probe). Typing the audience's affective trajectory (sympathetic-fall vs horrified-complicity vs unreconciled-suffering); `aims_at_catharsis: bool` is too coarse to discriminate. Audience-level; recurs with the long-banked audience-anagnorisis family.

These are the next research surface, not a sketch-07 deficiency. OQ-MALFI-3 is **closed**.
