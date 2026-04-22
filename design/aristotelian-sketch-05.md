# Aristotelian dialect — sketch 05 (directionality + polarity on ArCharacterArcRelation; anagnorisis_absent on ArCharacter)

**Status:** draft, active
**Date:** 2026-04-22
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [aristotelian-sketch-01](aristotelian-sketch-01.md) A1–A9, [aristotelian-sketch-02](aristotelian-sketch-02.md) A10–A12, [aristotelian-sketch-03](aristotelian-sketch-03.md) A13–A14, [aristotelian-probe-sketch-04](aristotelian-probe-sketch-04.md) A15–A16. All prior commitments unchanged.
**Frames:** [architecture-sketch-02](architecture-sketch-02.md), [aristotelian-sketch-03](aristotelian-sketch-03.md); `feedback_risk_first_sequencing.md`; `feedback_sketch_implement_rhythm_falsifies.md`
**Related:** Lear Session 5 probe run (commit `525c575`, 2026-04-22) — primary forcing-function source; `prototype/reader_model_lear_aristotelian_output.json` (the probe's JSON artifact); `prototype/story_engine/encodings/lear_aristotelian.py` + `hamlet_aristotelian.py` (the two encodings that will migrate)
**Superseded by:** nothing yet

## Purpose

Close two forcing functions surfaced directly by Lear Session 5's probe run (the first Aristotelian encoding whose probe output both verified a banked forcing function with probe-proposed dialect extensions AND surfaced a genuinely new one in the same session):

- **OQ-AP14 — Instrumental-kind ArCharacterArcRelation. DIRECT HIT.** The Lear encoding authored two non-canonical `kind="instrumental"` A13 relations sharing Gloucester as target with opposite moral polarity (Edmund malicious, Edgar therapeutic). The probe's `relations_wanted` proposed TWO specific dialect fields — `directionality` and `polarity` — as a sharper decomposition than the encoding's bundled three-axis candidate (directional + artifact-mediated + polarity bundled into "instrumental" kind). Sketch-05 ships both fields on A13.

- **OQ-LEAR-3 — Tragic hero without encoded anagnorisis. NEW.** Lear's Cordelia is authored with `is_tragic_hero=True` and `hamartia_text` but has no `ArAnagnorisisStep` and is not the mythos's `anagnorisis_character_ref_id`. The probe flagged `ar_cordelia:hamartia_text` as `needs-work` for overstating the shape and proposed `ArAnagnorisisStep.step_kind='absent'` OR `a dedicated ArCharacter field`. Sketch-05 takes the latter path — `ArCharacter.anagnorisis_absent: bool` — as the simpler shape-match.

The sketch adds TWO new optional fields on existing dialect records and TWO new self-verifier checks. Commitments A1–A16 from sketches 01/02/03/04 are unchanged.

## Why now

Lear Session 5 (commit `525c575`, 2026-04-22) is the first probe in the Aristotelian arc to:
1. Read a non-canonical A13 kind ("instrumental") on multiple records in one encoding with opposite polarities.
2. Catch a tragic-hero-without-anagnorisis encoding overstatement via annotation review + propose a specific dialect extension.

Both are *probe-driven* pressures with probe-proposed shapes — the probe named the dialect extension, not the encoding. Per the Hamlet-Session-5 → sketch-03 precedent (probe surfaces forcing; next sketch closes it end-to-end), sketch-05's role is to land both probe-proposed extensions and migrate the two encodings that exercise them.

OQ-LEAR-3's case is *stronger than* Hamlet's OQ-AP8 (same-beat staggered recognition) because OQ-LEAR-3 is an authorial gap (Cordelia genuinely has no recognition), whereas OQ-AP8 is a structural compression (Laertes's recognition coincides with the main event). A18 closes the gap-shape; OQ-AP8 stays banked as the compression-shape, requiring a different extension.

OQ-AP14's case is *stronger than* OQ-AP6 (which sketch-03 closed with one encoding-site) because it is two-site: Hamlet's single-candidate surface in Session 6 + Lear's two-candidate surface in Session 5. The probe's dual-field proposal (directionality + polarity as independent axes) is architecturally cleaner than a fourth canonical kind.

User directive: *"Author-fixes + sketch-05 closure response"*.

## Scope — what this sketch does and doesn't do

**In scope:**

- **A17.** Two new optional fields on `ArCharacterArcRelation`:
  - `directionality: str = ""` — `"" | "symmetric" | "directional"`; back-compat derivation from `kind`
  - `polarity: str = ""` — `"" | "malicious" | "therapeutic" | "neutral" | "sanctioned"`; no derived default
- **A18.** One new optional field on `ArCharacter`:
  - `anagnorisis_absent: bool = False`
- **A7.15.** ArCharacterArcRelation directionality/polarity invariants (five checks, two severity levels).
- **A7.16.** ArCharacter anagnorisis_absent invariants (three checks, all advises-review).
- **Encoding migrations.** Lear (four A13 relations + ar_cordelia) and Hamlet (two A13 relations) migrate to the new fields. Oedipus / Rashomon / Macbeth verify identically (no A13 relations, no anagnorisis_absent tragic heroes).
- **OQ-LEAR-6 + OQ-LEAR-7 folded into A7.15.** The probe's suggested signatures ("kind-justification-present" + "paired-non-canonical-polarity") fold into A7.15 check 5 (paired-polarity-contrast emits noted).

**Out of scope:**

- **OQ-AP8 (same-beat staggered recognition).** Different shape from OQ-LEAR-3; Laertes has a recognition, Cordelia doesn't. Stays banked.
- **OQ-LEAR-4 (secondary peripeteia for subplot).** Single-site (Lear only). Stays banked pending second-site pressure (Shakespeare's Gloucester-in-Lear + candidate second: Gloucester-in-post-Macbeth; or Clytemnestra-in-Aeschylus; or similar double-plot tragedy).
- **OQ-LEAR-5 (audience-level parallel-plot catharsis).** Related to OQ-AP1 (ArPathos) from a different angle; stays banked, converging with OQ-AP1's re-surfacings.
- **OQ-AP15 (absent-character catharsis).** Session 5 verified the substrate signature (empty-observer defining event + observer-wave reveal event) is self-consistent at substrate scope; the dialect has no visible deficiency. **Reclassifying from "forcing function" to "substrate-signature-only pressure";** see §Out of scope disposition.
- **OQ-AP7 (range-of-separated).** Second-site pressure failed to emerge in Lear Session 5. Reclassifying from "forcing function" to "conjectural" — the distinction Hamlet's Session 5 surfaced did not generalize to Lear's 14-distance.
- **OQ-LEAR-1 (emotional-vs-epistemic staging).** Probe approved Lear's 2-parallel-no-staging chain without flagging. Reclassifying from "forcing function" to "substrate-signature-only"; the `remove_held` shape at E_lear_cordelia_reconcile is the substrate signature.
- **Changes to A1–A16 commitment semantics.** All prior fields + invariants preserved. A13's `kind` canonical set unchanged.
- **Cross-dialect Lowering (A9 unchanged).** `directionality` and `polarity` don't cross dialect boundaries.

### Out-of-scope disposition: three weakened forcing functions

**OQ-AP15 reclassification.** Session 5's probe did not cite Cordelia's offstage hanging or catharsis-displacement as a dialect gap. The substrate signature (empty observer set on E_cordelia_hanged + observer-wave on E_lear_enters_with_cordelia) reads as self-consistent without dialect-level apparatus. Two encoding-sites (Hamlet + Lear) did not pressure the dialect; the reader-model reads the substrate shape through to the catharsis without requiring typed records. OQ-AP15 moves to "substrate-signature-only pressure" — the substrate records the shape; the dialect-level claim that an extension would add value is retracted. No sketch-06 candidate.

**OQ-AP7 reclassification.** Hamlet's Session 5 surfaced a numerical-range concern ("separated as a single category over a wide distance"). Lear at distance 14 (wider than Hamlet's 9) was an ideal second-site pressure. The probe read 14 as "separated" without discomfort. The distinction near-separated / distant-separated is not probe-pressured; OQ-AP7 moves to "conjectural" — one-site author-pressure that doesn't generalize.

**OQ-LEAR-1 reclassification.** The probe approved both of Lear's parallel chain steps and did not flag the absence of staging. The Session 2 encoding's claim that emotional-vs-epistemic main-anagnorisis trajectories needed dialect distinction was speculative; the probe's silence is falsification. OQ-LEAR-1 moves to "substrate-signature-only" — the `remove_held` at E_lear_cordelia_reconcile is the substrate marker; the dialect does not need a step_kind="affective" to carry it.

Three weakenings in one sketch. Per `feedback_sketch_implement_rhythm_falsifies.md`: "implementation regularly falsifies one [claim]" — Session 5's probe falsified three Session 2 claims in one run. The sketch-05 scope-narrowing acknowledges this as the process working.

## Commitments

Labels **A17** and **A18** continue sketches 01/02/03/04's A1–A16 numbering. **A7.15** and **A7.16** extend A7's numbered check list.

### A17 — directionality + polarity fields on ArCharacterArcRelation

```python
@dataclass(frozen=True)
class ArCharacterArcRelation:
    id: str
    kind: str                              # canonical-plus-open (A13, unchanged)
    character_ref_ids: Tuple[str, ...]     # ≥ 2 character ids (A13, unchanged)
    mythos_id: str                         # (A13, unchanged)
    over_event_ids: Tuple[str, ...] = ()   # (A13, unchanged)
    annotation: str = ""                   # (A13, unchanged)
    # NEW (sketch-05, A17):
    directionality: str = ""               # "" | "symmetric" | "directional"
    polarity: str = ""                     # "" | "malicious" | "therapeutic" | "neutral" | "sanctioned"
```

**Canonical directionality values:**

- `"symmetric"` — the relation is symmetric between the referenced characters; tuple order is not load-bearing. Canonical kinds (parallel, mirror, foil) are symmetric by construction.
- `"directional"` — the relation is directed; `character_ref_ids[0]` is conventionally the wielder / subject / agent; `character_ref_ids[1]` is the target / object / patient. Instrumental relations are directional by construction.

**Canonical polarity values:**

- `"malicious"` — the relation's outcome on the target is destructive to the target's interests. Edmund → Gloucester.
- `"therapeutic"` — the relation's outcome on the target is restorative / healing. Edgar → Gloucester at Dover.
- `"neutral"` — the relation's moral valence is not load-bearing. Canonical-kind relations (Lear-Gloucester parallel, Hamlet-Laertes mirror) typically use neutral.
- `"sanctioned"` — the relation is authorized by moral / legal / institutional structure despite having destructive outcome. Edgar killing Edmund in trial-by-combat is sanctioned; A12 BINDING is not affected.

**Empty-string semantics:**

- `directionality=""`: treated as "derive from kind". Canonical kind → derived `"symmetric"`. Non-canonical kind → derived empty (the verifier does not enforce a default; authors SHOULD set explicitly on non-canonical kinds).
- `polarity=""`: not applicable / not specified. No derived default.

**Back-compat derivation (for `directionality=""`):**

```python
if directionality == "":
    if kind in CANONICAL_CHARACTER_ARC_RELATION_KINDS:
        derived_directionality = "symmetric"
    else:
        derived_directionality = ""  # no structural claim
```

This lets pre-sketch-05 encodings (Hamlet's sketch-04 state, any post-sketch-03 encoding) verify identically — canonical-kind relations behave as symmetric by implication; non-canonical-kind relations have no implied directionality.

**Directional tuple convention.** When `directionality="directional"`, the convention is `character_ref_ids = (wielder, target)`. This is not structurally enforced by A7.15 (tuple-position checking would require substrate knowledge of which character holds the agency); authors observe it by documentation. A7.15 check 3 (canonical-kind + directional conflict) catches the most common error shape (treating a symmetric relation as directional).

**Architectural classification: extension.** Two new optional fields on an existing dataclass. Empty-string defaults preserve the sketch-03 shape.

### A18 — anagnorisis_absent field on ArCharacter

```python
@dataclass(frozen=True)
class ArCharacter:
    id: str                                # (A5, unchanged)
    name: str                              # (A5, unchanged)
    character_ref_id: Optional[str] = None # (A5, unchanged)
    hamartia_text: str = ""                # (A5, unchanged)
    is_tragic_hero: bool = False           # (A5, unchanged)
    # NEW (sketch-05, A18):
    anagnorisis_absent: bool = False
```

**Semantics:**

- `anagnorisis_absent=False` (default): the dialect makes no claim about whether this character has an anagnorisis. The character may be the mythos's main-anagnorisis character; may have a chain step; may be outside the chain structurally (the standard silent-on-shape default).
- `anagnorisis_absent=True`: an authorial claim that this character is a tragic hero whose hamartia produces catastrophe for others but whose own arc does not contain a recognition moment. The character will NOT be the mythos's main-anagnorisis character and will NOT have a chain step naming them — those would contradict the absent claim.

**When to set True:** when the character has `is_tragic_hero=True`, has meaningful `hamartia_text`, is substrate-present in the mythos, but the play's structural shape does not include a recognition-moment for this character. The canonical case: Cordelia — her hamartia (truth-telling at the wrong moment) catalyzes the cascade, her death produces the catharsis, but the play never dramatizes a Cordelia-recognizes-X moment.

**When NOT to set True (despite surface plausibility):**

- Laertes in Hamlet — he DOES recognize, at the same beat as Hamlet's main (OQ-AP8 substrate-compression). His anagnorisis exists; it's substrate-compressed, not absent.
- Claudius in Hamlet — he has a parallel chain step (`AR_STEP_CLAUDIUS_PRAYS`); not absent.
- Any character whose substrate holds a `remove_held` or `observe` effect at the anagnorisis_event_id recognizing their own error-of-judgment. The "absent" claim is a claim about narrative shape, not about substrate-level epistemic history.

**Architectural classification: extension.** One new optional field on `ArCharacter`. False default preserves pre-sketch-05 semantics.

### A7.15 — ArCharacterArcRelation directionality + polarity invariants

For each `ArCharacterArcRelation`:

1. `directionality ∈ {"", "symmetric", "directional"}` — invalid values emit `severity=advises-review` with code `character_arc_relation_directionality_invalid`.

2. `polarity ∈ {"", "malicious", "therapeutic", "neutral", "sanctioned"}` — invalid values emit `severity=advises-review` with code `character_arc_relation_polarity_invalid`.

3. If `kind ∈ CANONICAL_CHARACTER_ARC_RELATION_KINDS` AND `directionality == "directional"`: emit `severity=advises-review` with code `character_arc_relation_canonical_kind_directional_conflict`. Canonical kinds (parallel / mirror / foil) are symmetric by construction; a directional-flagged canonical-kind relation is almost certainly a mis-classification. Authors wanting a directional relation on canonical kind should either use non-canonical kind or leave directionality empty.

4. If `polarity != ""` AND `directionality == "symmetric"`: emit `severity=noted` with code `character_arc_relation_polarity_on_symmetric_noted`. Polarity semantics are strongest on directional relations (wielder → target has a direction, which has a moral valence); on symmetric relations the polarity claim is either vacuous or pressures the tuple for ordering. Not an error — emits noted to flag the soft tension.

5. **Paired-non-canonical-polarity detection** (folds OQ-LEAR-6 + OQ-LEAR-7). Within a single `character_arc_relations` tuple, if two records:
   - share the same non-canonical `kind` (i.e., `kind ∉ CANONICAL_CHARACTER_ARC_RELATION_KINDS`), AND
   - share the same target character (defined as `character_ref_ids[1]` when `directionality="directional"`, otherwise skipped), AND
   - have different non-empty polarities, AND
   - were authored for the same mythos_id,

   THEN emit `severity=noted` with code `character_arc_relation_paired_polarity_contrast` referencing both record ids. The polarity-inversion on shared target is a structurally-load-bearing authorial pattern (Lear's Edmund/Edgar → Gloucester); the noted observation highlights it rather than flagging an error.

### A7.16 — ArCharacter anagnorisis_absent invariants

For each `ArCharacter` whose `anagnorisis_absent=True`:

1. `is_tragic_hero` must be `True` — only tragic heroes can meaningfully have the "absent recognition" shape. Violation: `severity=advises-review` with code `character_anagnorisis_absent_requires_tragic_hero`. (A non-tragic-hero with anagnorisis_absent=True is authorial confusion; minor characters don't carry a tragic-hero arc with or without recognition.)

2. If `character_ref_id == mythos.anagnorisis_character_ref_id`: violation: `severity=advises-review` with code `character_anagnorisis_absent_contradicts_main`. A character cannot be the mythos's main-anagnorisis subject AND absent-from-anagnorisis.

3. If any step in `mythos.anagnorisis_chain` has `step.character_ref_id == character.character_ref_id`: violation: `severity=advises-review` with code `character_anagnorisis_absent_contradicts_chain_step`. A character who has a chain step naming them (at any step_kind) cannot be absent.

**NO implicit-gap detection.** The verifier does NOT fire a noted observation when a tragic-hero character has `anagnorisis_absent=False` and no chain step and is not main — this is the default-silent shape. Whether to mark a gap is the author's authorial decision; the verifier accepts silence. (Contrast: the probe's annotation review flagged the Cordelia overstatement as needs-work prose; the verifier closes this by admitting the `anagnorisis_absent=True` field, not by proactively flagging silence.)

### A7 orchestration — verify signature unchanged

```python
def verify(
    mythos: ArMythos,
    *,
    substrate_events: tuple = (),
    mythoi: Tuple[ArMythos, ...] = (),
    relations: Tuple[ArMythosRelation, ...] = (),
    character_arc_relations: Tuple[ArCharacterArcRelation, ...] = (),
) -> list:
    ...
```

No new kwargs. A7.15 runs on the existing `character_arc_relations` input; A7.16 runs on `mythos.characters`. `group_by_severity` / `group_by_code` unchanged.

## Worked cases

### Lear migration (primary forcing encoding)

**Four A13 relations migrate:**

```python
AR_LEAR_GLOUCESTER_PARALLEL = ArCharacterArcRelation(
    # ... existing fields ...
    directionality="symmetric",     # NEW
    polarity="neutral",             # NEW
)

AR_EDGAR_EDMUND_FOIL = ArCharacterArcRelation(
    # ... existing fields ...
    directionality="symmetric",     # NEW
    polarity="neutral",             # NEW
)

AR_EDMUND_GLOUCESTER_INSTRUMENTAL = ArCharacterArcRelation(
    kind="instrumental",            # (unchanged — non-canonical)
    character_ref_ids=("ar_edmund", "ar_gloucester"),  # wielder, target
    # ... existing fields ...
    directionality="directional",   # NEW
    polarity="malicious",           # NEW
)

AR_EDGAR_GLOUCESTER_INSTRUMENTAL = ArCharacterArcRelation(
    kind="instrumental",            # (unchanged — non-canonical)
    character_ref_ids=("ar_edgar", "ar_gloucester"),   # wielder, target
    # ... existing fields ...
    directionality="directional",   # NEW
    polarity="therapeutic",         # NEW
)
```

**AR_CORDELIA migration:**

```python
AR_CORDELIA = ArCharacter(
    # ... existing fields ...
    is_tragic_hero=True,
    anagnorisis_absent=True,        # NEW — closes OQ-LEAR-3
)
```

**Expected verifier output post-migration:**
- Two `noted` observations for `character_arc_relation_kind_noncanonical` on the two instrumental relations (A7.10, unchanged from sketch-03 — canonical-plus-open).
- ONE additional `noted` observation for `character_arc_relation_paired_polarity_contrast` (A7.15 check 5) — the Edmund/Edgar → Gloucester polarity pair.
- Zero other observations. Three total.

The ar_cordelia `hamartia_text` prose (already cleaned up in Session 5's author-fix commit `90975b4`) names OQ-LEAR-3 explicitly; the new `anagnorisis_absent=True` field structurally carries what the prose named.

### Hamlet migration (canonical-relations-only; no non-canonical kinds)

```python
AR_HAMLET_LAERTES_MIRROR = ArCharacterArcRelation(
    # ... existing fields ...
    directionality="symmetric",     # NEW
    polarity="neutral",             # NEW
)

AR_HAMLET_CLAUDIUS_FOIL = ArCharacterArcRelation(
    # ... existing fields ...
    directionality="symmetric",     # NEW
    polarity="neutral",             # NEW
)
```

No A18 migration — Laertes is NOT anagnorisis_absent (he recognizes at the main event; substrate-compressed per OQ-AP8). Claudius is NOT anagnorisis_absent (he has a chain step). Hamlet is NOT anagnorisis_absent (he is main).

**Expected verifier output post-migration:** zero observations (unchanged from sketch-04 state).

### Oedipus / Rashomon / Macbeth — no migration

No A13 relations authored. No A5 characters with `is_tragic_hero=True` and ambiguous recognition status. Verify identically to pre-sketch-05.

## Open questions — banked

### OQ9 — Directionality semantics on tuple position

Sketch-05's `directionality="directional"` establishes a convention (tuple position 0 = wielder, position 1 = target) without enforcing it structurally. Enforcement would require either: (a) substrate-level role annotations on events (which of {wielder, target} participates in each over_event_id); (b) a dedicated `wielder_ref_id` / `target_ref_id` pair replacing the tuple. Neither is pressured by Lear; (b) would also complicate the symmetric case. Stays banked; forcing-function: second encoding with ≥3-character instrumental relation (directed tree, not dyad).

### OQ10 — Polarity-on-main-anagnorisis-event invariant

A potential A7.15 check 6: if `polarity="malicious"` AND `directionality="directional"` AND one of the `over_event_ids` IS the mythos's `anagnorisis_event_id`: emit noted — the author may be conflating the wielder's malice with the target's recognition. Not authored today because it would false-positive on Edmund's deathbed confession (τ_s=35) scenes where Edmund's prior malice context persists in over_event_ids. Stays banked.

### OQ11 — Catharsis-bearing anagnorisis_absent interaction

A tragic hero with `anagnorisis_absent=True` whose death is the catharsis (Cordelia): does the dialect admit structural connection between the absent-recognition and the catharsis-bearing death? Currently: no. `aims_at_catharsis` is a mythos-scope bool; no per-character catharsis-weighting. Related to OQ-AP1 (ArPathos) and OQ-LEAR-5 (audience-level parallel-plot catharsis). Stays banked; convergence candidate.

### OQ12 — Mixed-canonical-non-canonical directionality sets

If an encoding authors both a non-canonical kind (e.g., "instrumental") AND a canonical kind (e.g., "foil") on the same character pair, A7.15 does not check cross-record consistency. Structurally legal but possibly confusing. Not forced by any current encoding; stays banked.

## Implementation brief

- **Add to `story_engine/core/aristotelian.py`:**
  - `CANONICAL_DIRECTIONALITIES = frozenset({"symmetric", "directional"})`.
  - `CANONICAL_POLARITIES = frozenset({"malicious", "therapeutic", "neutral", "sanctioned"})`.
  - Extend `ArCharacterArcRelation` with two new optional fields.
  - Extend `ArCharacter` with one new optional field.
  - Add `_check_a7_15(character_arc_relations)` function implementing the five invariants.
  - Add `_check_a7_16(characters, mythos)` function implementing the three invariants.
  - Thread both into `verify()` orchestration.

- **Add to `prototype/tests/test_aristotelian.py`:**
  - Synthetic fixtures + unit tests for each invariant (~10-12 new tests).
  - Integration tests against the post-migration Lear encoding (~3-4 new tests).
  - Back-compat test: pre-sketch-05 encoding snapshots verify identically.

- **Encoding migrations:**
  - `prototype/story_engine/encodings/lear_aristotelian.py` — four A13 relations + AR_CORDELIA.
  - `prototype/story_engine/encodings/hamlet_aristotelian.py` — two A13 relations.

- **No schema-layer landing in sketch-05.** Schema update (`schema/aristotelian/character_arc_relation.json` extension + `schema/aristotelian/character.json` extension) is deferred to a follow-on production-format sketch, gated on:
  (a) PFS14 (sketch-03 A13 + A14 schema landing, currently deferred from sketch-03 AA15),
  (b) the sketch-05 + sketch-06 (if any) stabilization window.

Expected test count: ~12-14 new tests in test_aristotelian.py; total ~167-171 after migration.

## Falsifiable predictions

- **F1 (A17 fields):** Lear post-migration produces exactly three observations: two `character_arc_relation_kind_noncanonical` (noted) + one `character_arc_relation_paired_polarity_contrast` (noted). All other severity counts zero.
- **F2 (A18 field):** Lear post-migration with `AR_CORDELIA.anagnorisis_absent=True` produces zero A7.16 advises-review violations.
- **F3 (Hamlet back-compat):** Hamlet post-migration produces zero observations (unchanged from sketch-04 state).
- **F4 (pre-sketch-05 encodings):** Oedipus, Rashomon, Macbeth produce the same observations as pre-sketch-05 (zero new observations from A7.15/A7.16).
- **F5 (paired-polarity on canonical kinds):** If an encoding has two canonical-kind (parallel/mirror/foil) records sharing target with different polarities, A7.15 check 5 does NOT fire (the check is scoped to non-canonical kinds; canonical relations are symmetric so "target" is ill-defined).
- **F6 (OQ-LEAR-3 probe re-closure on Session 6):** The probe's needs-work verdict on ar_cordelia:hamartia_text should promote to approved once the prose names OQ-LEAR-3 explicitly and the structural field carries the claim.

**Partial success (still useful):**
- F1 fires two-noted but not the paired-polarity: the check 5 logic is under-specified; amend in-place.
- F6 partially — prose approved but dialect_reading still lists it in scope_limits: the shape is the whole reading, not the local noted check.

**Honest failure:**
- Probe's Session 6 re-probe surfaces a NEW forcing function Lear Session 5 didn't: legitimate — amend sketch-05 or open sketch-06.
- Migration of a Hamlet A13 relation fails because `kind="mirror"` + `directionality="symmetric"` is rejected: would mean A7.15 check 3 false-positives; amend invariant.

## What a cold-start Claude should read first

1. `design/aristotelian-sketch-03.md` — A13/A14 + the canonical-plus-open discipline sketch-05 extends.
2. `design/aristotelian-probe-sketch-04.md` — the sketch-04 client extensions + Hamlet's Session 6 re-probe framing (precedent for Lear Session 6).
3. This sketch (`design/aristotelian-sketch-05.md`).
4. `prototype/reader_model_lear_aristotelian_output.json` — the Lear Session 5 JSON artifact. `dialect_reading.relations_wanted` fields (1)+(2) are the probe's dialect-extension proposals this sketch directly closes. `annotation_reviews[...verdict=needs-work]` fields include the three author-fix sites.
5. `design/compilation-sketch-01.md` — the compiler backend framing (sketch-05 doesn't interact with it but the broader dialect-surface arc motivates cross-referencing).
6. `prototype/story_engine/encodings/lear_aristotelian.py` — the primary migration target.
7. `git log --oneline --reverse 525c575..HEAD` — sketch-05's commit arc (author-fixes → sketch → impl+migration → Session 6 re-probe).

## Honest framing

Sketch-05 closes two forcing functions with probe-proposed shapes. Both landings are minimal-extension (optional fields with empty defaults; pre-sketch-05 encodings verify identically). The paired-polarity-contrast noted (A7.15 check 5) is the most novel mechanical claim — a verifier check that *highlights* a structural pattern rather than flagging an error. If the mechanism generalizes, future sketches may adopt "highlight observation" as a class (adjacent to noted, but semantically different).

**What sketch-05 does NOT prove:** that the directionality + polarity decomposition generalizes beyond Lear's Edmund/Edgar → Gloucester pattern. Without a second encoding with directional A13 relations (forcing function: Shakespeare's Iago-Othello as directional-malicious; or similar), A17's architectural payoff is one-encoding-verified.

**What sketch-05 DOES prove (if it succeeds):** that probe-driven dialect-extension closure is a repeatable pattern. Hamlet Session 5 → sketch-03 closed OQ-AP6 + OQ-AP10 with author-proposed shapes. Lear Session 5 → sketch-05 closes OQ-AP14 + OQ-LEAR-3 with PROBE-proposed shapes. The second instance is tighter — the probe's relations_wanted directly named the extensions, and the sketch takes them verbatim.

The three weakened forcing functions (OQ-AP15, OQ-AP7, OQ-LEAR-1) are the sketch-05 cost of honest probe-reading. Session 2 authored them as pressure; Session 5 did not surface them. Per `feedback_sketch_implement_rhythm_falsifies.md` — the rhythm is working: design-first speculation falsified by probe data, acknowledged in-place.
