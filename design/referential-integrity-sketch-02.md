# Referential integrity — sketch 02

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (amendment — commits the second-arc
audits referential-integrity-sketch-01 banked in OQ1 and OQ2)
**Extends:** [referential-integrity-sketch-01](referential-
integrity-sketch-01.md) RI1..RI8 (commitments unchanged)
**Frames:** [production-format-sketch-06](production-format-
sketch-06.md) OQ4 (cross-dialect character_ref_id audit);
[production-format-sketch-09](production-format-sketch-09.md)
PFS9-X4 (open dialect-token posture — the audit honors the
extensibility commitment by resolving tokens dynamically, not
via a closed registry); [production-format-sketch-10](
production-format-sketch-10.md) OQ1 (CrossDialectRef
resolution across namespaces)
**Related:** sketch-01's first-arc landing (three intra-
encoding audits, 577 references, zero findings) as the
pattern this arc extends
**Superseded by:** nothing yet

## Purpose

**Second-arc implementation.** Close the two CrossDialectRef-
flavored audits sketch-01 explicitly banked:

- **CrossDialectRef resolution** on Lowering, VerificationReview,
  StructuralAdvisory, VerificationAnswerProposal records. Every
  `(dialect, record_id)` pair names an existing record of the
  expected id-type in the encoding-family that the source
  record belongs to. Closes PFS10 OQ1.
- **ArCharacter.character_ref_id multi-dialect resolution.**
  Each aristotelian character's optional cross-dialect hook
  resolves to either a substrate Entity id or a Dramatic
  Character id in the paired encoding. Closes PFS6 OQ4.

No architectural principles change. This sketch extends
sketch-01's Tier-2 audit layer to the remaining banked
reference kinds; RI1..RI8 stay as the governance spine.

## Why now

- **Sketch-01 landed clean.** 577 references resolved across
  three audit kinds; zero dispositions surfaced. The audit
  pattern works; extending it is mechanical rather than
  experimental.
- **The corpus is dense at the cross-boundary tier.** 156
  Lowerings + 58 VerificationReviews + 1 StructuralAdvisory
  in the current runtime-generated corpus. Each carries one
  to several CrossDialectRef values. A typo detected here
  would be load-bearing (a Lowering pointing at a non-
  existent Character would silently route through the whole
  downstream verifier surface).
- **Cross-encoding lookup mechanism is finite and bounded.**
  Three dialect tokens in use (`substrate`, `dramatic`,
  `save-the-cat`); four if we count a future `dramatica-
  complete`; five if `aristotelian` ever produces Lowerings.
  A per-dialect resolution rule is small enough to ship today.
- **Closes two of three banked OQs in one arc.** PFS6 OQ4 +
  PFS10 OQ1 close under this sketch's implementation; sketch-01
  OQ5 (substrate-internal entity-id audits) remains deferred
  per its own forcing-function rationale.

## Scope — what this sketch covers

**In (second-arc extension):**

- **CrossDialectRef audit** on every record carrying the pair:
  - `Lowering.upper_record` (single ref per Lowering).
  - `Lowering.lower_records[*]` (array ref, size ≥ 1 when
    status=active per PFS9-X3).
  - `VerificationReview.target_record` (single ref per review).
  - `StructuralAdvisory.scope[*]` (array ref, may be empty).
  - `VerificationAnswerProposal.question_id` (single ref).
- **character_ref_id audit** on every `ArCharacter` reached
  through encoding-level `AR_*` mythos records. Multi-dialect
  fallback: checks substrate Entity ids OR Dramatic Character
  ids in the paired encoding.
- Per-dialect id-collection rules (RI10).
- Work-id extraction rules from lowering-module names (RI11).
- Findings vocabulary extension (none — reuses sketch-01's
  `unresolved` per RI4).

**Out (still banked):**

- **Dialect-catalog references** (e.g., `stc_genre_id` →
  StcGenre catalog id). Per sketch-01 §Scope; gated on
  dialect-catalog schema decisions (PFS7 OQ2).
- **Metadata-key references** (`Lowering.metadata["supersedes"]`
  → Lowering id). Per sketch-01 OQ3; low-urgency —
  `validate_lowerings` already checks at runtime.
- **Type-mismatch detection** (a Lowering with
  `upper_record=("substrate", "oedipus")` when the upper
  dialect should be "dramatic" — the record exists but of
  wrong type). Reserved for a third-arc.
- **Substrate-internal audits** (event.participants → entity
  ids, etc.). Per sketch-01 OQ5; banked.

## Commitments

### RI9 — Dialect-token to module-path mapping

The three dialect tokens in the corpus map to module paths
under `story_engine.encodings`:

```
substrate       → {work}                     (e.g., oedipus)
dramatic        → {work}_dramatic            (e.g., oedipus_dramatic)
save-the-cat    → {work}_save_the_cat        (note: dash → underscore)
```

**Name-mangling.** The `save-the-cat` dialect token uses dash
(per corpus convention — see `cross_ref("save-the-cat", ...)`
call sites); the module path uses underscore (`save_the_cat`,
per Python's module-naming convention committed by PFS6-N1).
The audit translates token → module-path: `s/-/_/` on the
dialect token.

**Rationale for keeping the dash in the token.** The dialect
token is a first-class value shipped through CrossDialectRef
records; changing it to `save_the_cat` would require migrating
the authored corpus. The underscore form in the module path
was committed by PFS6-N1 as a Python-naming convention. Until
a forcing function unifies the two (and there's no such
function today), they coexist with the mapping.

**Future dialect tokens** (`dramatica-complete`, `aristotelian`)
don't appear in Lowerings today. If a future sketch authors
Lowerings at those boundaries, extend the RI9 mapping:

```
dramatica-complete → {work}_dramatica_complete
aristotelian       → {work}_aristotelian
```

### RI10 — Per-dialect id-collection rules

For each encoded dialect, the audit collects authored record
ids from the module's known exports:

- **`substrate`** — union of `ENTITIES` ids + `FABULA` (or
  `EVENTS_ALL`) ids + `DESCRIPTIONS` ids. Braches labels
  (`ALL_BRANCHES` keys) are **not** included in the substrate
  id-set: they are a different id-namespace, and CrossDialectRef
  pointing at a branch label would be a category error.
- **`dramatic`** — union of `CHARACTERS` ids + `THROUGHLINES`
  ids + `SCENES` ids + `BEATS` ids + `STORY.id`. Uses all
  Dramatic record types with authorial ids.
- **`save-the-cat`** — union of `STORY.id` + `BEATS` ids +
  `STRANDS` ids + `CHARACTERS` ids.

**Union-by-union.** A CrossDialectRef to a given dialect
carries no record-type tag; the audit doesn't know whether
`("dramatic", "C_oedipus")` targets a Character, Throughline,
or Scene. Resolution is union-membership: the `record_id` must
appear in the dialect's authored-id union. Type-mismatch
detection is reserved (see sketch-01 RI4 `type-mismatch`
placeholder).

**Defensive attribute lookup.** If a module doesn't export a
known attribute (e.g., an old-format substrate module without
`DESCRIPTIONS`), the audit skips the attribute silently rather
than failing. Missing attributes are a corpus-authoring
concern, not an audit concern.

### RI11 — Work-id extraction from lowering-module names

Lowerings live in modules named:

- `{work}_lowerings.py` — Dramatic↔substrate Lowerings.
- `{work}_save_the_cat_lowerings.py` — STC↔substrate Lowerings.

Work-id extraction:

- Strip `_lowerings` suffix.
- If the remainder ends in `_save_the_cat`, strip it too —
  the work is the leading part.

**Examples:**

```
oedipus_lowerings                       → work="oedipus"
macbeth_save_the_cat_lowerings          → work="macbeth"
rashomon_lowerings                      → work="rashomon"
and_then_there_were_none_lowerings      → work="and_then_there_were_none"
```

**For VerificationReview / StructuralAdvisory /
VerificationAnswerProposal records** (emitted by
`*_verification.py` modules), work-id extraction parallels:

- Strip `_verification` suffix.
- If the remainder ends in `_dramatica_complete` or
  `_save_the_cat`, strip it too.

**Examples:**

```
oedipus_verification                        → work="oedipus"
macbeth_dramatica_complete_verification     → work="macbeth"
macbeth_save_the_cat_verification           → work="macbeth"
```

### RI12 — CrossDialectRef audit algorithm

For each corpus record carrying CrossDialectRef values:

1. **Determine the record's source work-id** via RI11.
2. **Resolve the CrossDialectRef's dialect token** to a module
   path via RI9: `dialect_token → {work}_{mangled_suffix}`
   (or `{work}` for substrate).
3. **Collect the dialect's authored-id set** from the module
   via RI10.
4. **Check membership:** `record_id in authored-id set`.
5. **Surface unresolved references** as findings
   (`unresolved` kind per sketch-01 RI4).

**Error modes that also surface as findings:**

- The target module doesn't exist (e.g., a Lowering pointing
  at `dialect="dramatic"` for a work that has no
  `{work}_dramatic.py`). Surfaced as `unresolved` with a
  message naming the missing module.
- The target module imports but fails attribute access. Same
  treatment.

**Per-record-kind iteration:**

- **Lowering:** iterate `upper_record` + each
  `lower_records[*]`.
- **VerificationReview:** iterate `target_record`.
- **StructuralAdvisory:** iterate each `scope[*]`.
- **VerificationAnswerProposal:** iterate `question_id`.
- **VerifierCommentary:** iterate
  `target_review.target_record` transitively (the nested
  review's own target).

### RI13 — character_ref_id multi-dialect fallback

`ArCharacter.character_ref_id` is optional. When set, it points
at either a substrate Entity id OR a Dramatic Character id in
the paired encoding. Resolution rule:

1. **Determine paired work-id** from the Aristotelian module
   name: `{work}_aristotelian → work`.
2. **Collect substrate Entity ids** from `{work}` module's
   `ENTITIES` attribute.
3. **Collect Dramatic Character ids** from
   `{work}_dramatic` module's `CHARACTERS` attribute (if the
   module exists; not all works have a Dramatic encoding).
4. **Check membership:** `character_ref_id ∈ (substrate
   entities ∪ dramatic characters)`.

**The union is explicit.** A character_ref_id resolving against
EITHER source is clean. This matches aristotelian-sketch-01 A5:
the field is a cross-dialect identity hook, not a strict-typed
reference to one of the two.

**Optional field, zero-audit when absent.** If
`character_ref_id is None`, no audit runs for that
ArCharacter. The schema-layer shape test (PFS6-C3: "optional
non-empty string") already validates the absent-vs-non-empty
shape; the audit adds the resolution layer when the field is
present.

### RI14 — Second-arc scope boundary

This arc ships two audits (RI12 CrossDialectRef + RI13
character_ref_id). Any further referential-integrity audit is
a third-arc concern (not blocked — the third arc ships when a
forcing function argues).

**Explicitly NOT in this arc** (banked for third-arc if
forcing functions land):

- Dialect-catalog references (stc_genre_id → StcGenre). Gated
  on PFS7 OQ2's dialect-catalog schema decision.
- Metadata-key references (Lowering.metadata["supersedes"] →
  Lowering id; Branch.metadata["supersedes"] → Branch label).
  Per sketch-01 OQ3; `validate_lowerings` already checks at
  runtime.
- Substrate-internal entity-id references (event.participants
  → entity ids, effect.prop.args → entity ids, etc.). Per
  sketch-01 OQ5.
- Type-mismatch detection (reserved in sketch-01 RI4).
- `target_review.target_record` transitive resolution on
  VerifierCommentary — the inner VerificationReview already
  gets its own RI12 audit if it appears in runtime verifier
  output; commentary records live only in probe JSONs today,
  so transitive checking is redundant. Deferred until
  commentary flows through verifier output.

## Anticipated outcomes

**Expected clean.** The Tier-2 landing has set precedent:
sketch-01's three audits resolved all 577 references cleanly
on first contact. For the second arc:

- **CrossDialectRef audit:** ~500 refs across 156 Lowerings
  (upper + lower records) + 58 VerificationReviews +
  1 StructuralAdvisory. Expected clean: every Lowering was
  authored against records that exist in the paired
  encoding modules, and the VerificationReviews' target_record
  is computed from the same Throughline ids the Template
  records already carry.
- **character_ref_id audit:** 6 ArCharacter records (5 from
  Rashomon + Jocasta from Oedipus + Oedipus himself from
  Oedipus — actually 2 from Oedipus + 4 from Rashomon). Each
  character_ref_id points at a substrate Entity id
  (`"oedipus"`, `"jocasta"`, `"bandit"`, etc.). Expected
  clean — the substrate Entity set covers all six.

**If findings surface.** RI6 dispositions protocol applies.
Either fix the encoding or amend the sketch with a disposition
naming the intentional case.

**Pending Lowerings admit empty lower_records.** PENDING
Lowerings with `lower_records=()` trivially pass the audit
(nothing to resolve). PENDING Lowerings with non-empty
lower_records still run the audit — the references must
resolve, even if the Lowering itself is promissory
(`validate_lowerings` separately flags this as
`pending_lowering_has_records` NOTED).

## Open questions

1. **OQ1 — `record_id` disambiguation on same-id-across-
   dialects.** Theoretically, a work could author an Entity
   named `"oedipus"` AND a Dramatic Character named
   `"oedipus"` (both with lowercase). Today's corpus uses
   `C_oedipus` for Dramatic and `oedipus` for substrate, so
   the disambiguation is implicit by naming convention. If a
   corpus case surfaces where a record_id legitimately
   exists in two dialects (e.g., an encoding that maps
   Character→Entity 1:1 with identical ids), the audit
   passes both — it checks union membership, not exact
   dialect matching. A future type-mismatch audit (reserved
   per sketch-01 RI4) would catch the case.

2. **OQ2 — Third-arc scope.** If a future sketch-03 lands,
   the most likely scope is (a) type-mismatch detection, or
   (b) dialect-catalog references (stc_genre_id). Neither
   has a forcing function today.

3. **OQ3 — Dialect-token to module mangling as a first-class
   mapping.** RI9's `save-the-cat → save_the_cat` is a one-
   off translation. If future dialect tokens use more
   complex conventions (mixed case? dialect-version suffix?),
   a first-class mapping function may become warranted.
   Today the one-off dash→underscore is cheap.

4. **OQ4 — character_ref_id forward-resolving targets.**
   ArCharacter.character_ref_id could point at a Dramatic
   Character whose own CharacterFunction Throughline
   assignment determines downstream verifier behavior.
   Resolving against the union doesn't validate this
   downstream semantic. A future audit could compose RI13
   with dialect-internal cross-reference audits (e.g., does
   the Dramatic Character exist AND have the expected
   Throughline binding). Reserved.

## Discipline

Same as sketch-01:

- **Additive, not replacement.** Per-dialect self-verifiers
  (aristotelian.verify A7 check 4; save_the_cat.verify S13)
  continue to carry their runtime resolution checks. The
  audit adds a conformance-test-layer surface; the verifier
  layer remains for runtime-of-verify() callers.
- **Findings via print-and-assert, not typed records.**
  Consistent with sketch-01 RI8; typed `IntegrityFinding`
  records remain reserved for a future arc if a consumer
  forces them.
- **Dispositions only via sketch amendment.** Per sketch-01
  RI6. Silent test-pass-via-listing is forbidden.
- **Scope discipline.** This arc is two audits. The third
  arc's scope is named in OQ2 but unscheduled.

## Summary

Second-arc audit extension to referential-integrity-sketch-01.
Six commitments (RI9..RI14):

- **RI9** — Dialect-token → module-path mapping (substrate,
  dramatic, save-the-cat).
- **RI10** — Per-dialect id-collection rules (unions of
  known record-type exports).
- **RI11** — Work-id extraction from lowering-module and
  verification-module names.
- **RI12** — CrossDialectRef audit algorithm (iterate records,
  resolve each pair via RI9+RI10, surface unresolved
  findings).
- **RI13** — character_ref_id multi-dialect fallback
  (substrate ∪ dramatic character ids in the paired
  encoding).
- **RI14** — Second-arc scope boundary; third-arc surface
  banked.

Closes two banked OQs on implementation:

- **PFS10 OQ1** — CrossDialectRef resolution across
  namespaces.
- **PFS6 OQ4** — cross-dialect character_ref_id audit.

Four OQs banked forward to potential third-arc:
record_id disambiguation across dialects (OQ1); third-arc
scope (OQ2); dialect-token-mangling mapping (OQ3);
character_ref_id forward-resolving targets (OQ4).

No schema file change. No Python prototype change
anticipated. Implementation commit extends
`test_production_format_sketch_01_conformance.py` with the
two new audit tests + their supporting helpers. Twentieth
consecutive production-track commit on track to avoid
`prototype/story_engine/` modifications.

The Tier-2 audit layer covers, at this arc's landing, the
three banked sketch-01 OQs + the two banked sketch-02 OQs =
**five of five banked OQs closed**. The single remaining
deferred audit kind (substrate-internal entity-id resolution,
sketch-01 OQ5) has its own low-urgency rationale; the
cross-boundary and dialect-layer surfaces are fully covered.
