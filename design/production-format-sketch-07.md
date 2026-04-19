# Production format — sketch 07

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (second dialect-layer schema arc, extending
the dialect-stack portion of architecture-sketch-02)
**Frames:** [save-the-cat-sketch-01](save-the-cat-sketch-01.md)
S1 (15 canonical beat slots), S2 (page targets), S3 (A/B strands),
S4 (theme at Story level), S5 (Genre as Template), S6 (self-
verifier observation-only); [save-the-cat-sketch-02](save-the-
cat-sketch-02.md) S9 (StcCharacter), S10 (canonical-plus-open
role labels), S11 (reference wiring), S12 (archetype
assignments), S13 (three new verifier checks); [production-
format-sketch-01](production-format-sketch-01.md) PFS1 (JSON
Schema 2020-12), PFS2 (schemas-first); [production-format-
sketch-03](production-format-sketch-03.md) PFS3-E1 (cross-file
`$ref` via `jsonschema.referencing.Registry`); [production-
format-sketch-05](production-format-sketch-05.md) OQ3 (plain-
string event-id references); [production-format-sketch-06](
production-format-sketch-06.md) PFS6-N1 (dialect schema
namespace), PFS6-X1 (cross-file `$ref` at dialect layer),
PFS6-X2 (no event-id `$ref`), PFS6-D1..D5 (dump + discovery
pattern); [architecture-sketch-02](architecture-sketch-02.md)
A6–A11 (dialect stack)
**Related:** [aristotelian-sketch-01](aristotelian-sketch-01.md)
(first dialect shipped under the namespace convention;
structurally contrasting shape per §PFS7-X1 below); [dramatic-
sketch-01](dramatic-sketch-01.md) (third dialect; pending
dramatic-sketch-02 before its production sketch can ship
cleanly per PFS6 OQ2)
**Superseded by:** nothing yet

## Purpose

**Second dialect production sketch.** Ships JSON Schema 2020-12
files for four Save-the-Cat core records — `StcStory`,
`StcBeat`, `StcStrand`, `StcCharacter` — under the
`schema/save_the_cat/` namespace that PFS6-N1 committed as
precedent.

Save-the-Cat is the natural second dialect: it is field-level-
specified by save-the-cat-sketch-01 (S1–S8) plus the sketch-02
StcCharacter amendment (S9–S13); its scope is bounded (~4
authored record types at the core + two inline sub-record
shapes); the corpus exists (Macbeth + Ackroyd encodings, 2
StcStory + 30 StcBeat + 4 StcStrand + 16 StcCharacter records);
and no outstanding design forcing functions bank against the
dialect (contrast Dramatic, where dramatica-template-sketch-
01's "Where the dialect resists" lists six).

This sketch stays slim for the same reason PFS5 and PFS6 did:
**the design sketches have already done the structural work.**
S1 + S9 ship StcStory's field list; S1 + S11 ship StcBeat's;
S3 + S11 ship StcStrand's; S9 + S10 + S11 ship StcCharacter's;
S12 ships StcArchetypeAssignment's (inline sub-record); S3 +
the Python dataclass ship StrandAdvancement's (inline sub-
record). The work here is format-rendering — re-expressing the
record shapes in JSON Schema — plus a small number of
architectural commitments.

The one architectural finding worth surfacing explicitly:
**Save-the-Cat's reference topology differs from
Aristotelian's.** Aristotelian is tree-shaped (ArMythos contains
phases and characters as inline $ref objects per PFS6-X1); Save-
the-Cat is flat with id references (StcStory references beats /
strands / characters by id-string arrays to sibling records,
like the substrate layer). This sketch names the distinction as
PFS7-X1 and commits both shapes as admitted dialect-layer
patterns going forward.

## Why now

- **Dialect schema layer has begun** (state-of-play-09's
  headline — concretely: `schema/aristotelian/` ships three
  records + PFS6-N1 namespace convention + PFS6-X1 cross-file
  $ref + PFS6-X2 no-event-id-$ref postures).
- **Save-the-Cat is the next dialect ready.** Field-level-
  detailed across two sketches; no outstanding design forcing
  functions; two corpus encodings already exercise every record
  type.
- **Second dialect validates PFS6's precedent.** PFS6-N1
  (namespace convention) and the PFS6-D1..D5 discovery pattern
  were authored as first-dialect choices; a second dialect's
  landing confirms they generalize.
- **A structurally different second dialect tests the
  architecture.** Save-the-Cat is beat-driven where
  Aristotelian is phase-driven; flat where Aristotelian is
  tree. If the namespace and discovery patterns hold across
  that contrast, they are load-bearing; if they don't, the
  contrast surfaces where they break. Landing Save-the-Cat
  closes that question.

## Scope — what the sketch covers

**In:**

- Four JSON Schema files for Save-the-Cat core records:
  - `schema/save_the_cat/story.json` (StcStory per S1/S4/
    S5/S11/S12).
  - `schema/save_the_cat/beat.json` (StcBeat per S1/S2/S3/
    S11; StrandAdvancement inline via `$defs`).
  - `schema/save_the_cat/strand.json` (StcStrand per S3/S11).
  - `schema/save_the_cat/character.json` (StcCharacter per
    S9/S10).
- The **flat-with-id-refs reference topology** (PFS7-X1)
  as an admitted dialect-layer pattern, complementing PFS6-X1's
  tree-with-inline-$ref topology. Both patterns coexist; each
  dialect chooses the one that matches its Python shape.
- **Inline `$defs` for sub-records** (PFS7-X2) —
  StcArchetypeAssignment inside story.json; StrandAdvancement
  inside beat.json. Sub-records without authorial ids live as
  inline `$defs` rather than sibling schema files.
- Dump-layer helpers: `_dump_stcstory`, `_dump_stcbeat`,
  `_dump_stcstrand`, `_dump_stccharacter` (PFS7-D1..D4) + an
  encoding-discovery helper (PFS7-D5) + registry registration
  (PFS7-D6).
- Conformance-test extension: four new metaschema tests, four
  new shape tests, four new corpus conformance tests (twelve
  total, matching PFS6's per-record test shape).
- `schema/README.md` sweep: the "Dialect layer" subsection
  grows to cover Save-the-Cat; "What's deferred" updated.

**Out:**

- `StcObservation`. Parallel to ArObservation's deferral (PFS6
  OQ1); ships as part of the cross-boundary / verifier-output
  Production C arc, not here. Rationale: ephemeral verifier
  output; no authored corpus; natural batch-partner with the
  dialect-agnostic verifier-output surface.
- `StcCanonicalBeat` (the 15 shipped-as-data canonical beats)
  and `StcGenre` (the 10 shipped-as-data genres). These are
  **dialect-catalog records** — module-level constants carried
  by the dialect itself, not per-encoding authored records.
  Structurally stable (15 and 10 entries hard-coded in
  `save_the_cat.py`); a schema would largely duplicate the
  Python shape for a one-time validation. Deferred to OQ2.
- Cross-dialect Lowering (Save-the-Cat ↔ Dramatic ↔ substrate)
  per architecture-sketch-02's dialect-stack A7. Lowering
  record schema lives in Production C.
- Dramatic dialect schemas. Gated on dramatic-sketch-02 per
  PFS6 OQ2.
- Any modification to `save-the-cat-sketch-01` / `sketch-02`
  commitments S1–S13. This sketch is format-rendering only.

## Commitments

### PFS7-N1 — Save-the-Cat schemas under `schema/save_the_cat/`

Inherits PFS6-N1 (`schema/<dialect>/<record>.json` subdirectory-
per-dialect) without modification. The dialect token is
`save_the_cat`, matching the Python module name
(`core/save_the_cat.py`); underscore-joined per PFS6-N1's
multi-word-dialect clarification.

**`$id` URIs** follow the same pattern as Aristotelian:

- `https://brazilofmux.github.io/story/schema/save_the_cat/story.json`
- `https://brazilofmux.github.io/story/schema/save_the_cat/beat.json`
- `https://brazilofmux.github.io/story/schema/save_the_cat/strand.json`
- `https://brazilofmux.github.io/story/schema/save_the_cat/character.json`

**Precedent validation.** Second dialect landing under the
same namespace convention confirms it generalizes. Subsequent
dialects (Dramatic per PFS6 OQ2, Dramatica-complete per
architecture-sketch-02 A11) will ship under
`schema/dramatic/` / `schema/dramatica_complete/` by the same
rule.

### PFS7-ST1..ST6 — Story record shape

`schema/save_the_cat/story.json` ships the StcStory record per
save-the-cat-sketch-01 S4/S5 + sketch-02 S11/S12.

- **PFS7-ST1.** Required fields: `id`, `title`.
  Everything else is optional — Save-the-Cat stories admit
  progressive authoring (the minimal encoding is id + title;
  the full encoding adds beats, strands, characters, theme,
  genre, archetype assignments incrementally).
- **PFS7-ST2.** `id` and `title` are non-empty strings.
- **PFS7-ST3.** `theme_statement` is an optional string
  (empty admissible) per S4. The verifier surfaces emptiness
  as a NOTED observation (`theme_statement_empty`); the schema
  does not.
- **PFS7-ST4.** `stc_genre_id` is an **optional non-empty
  string**. Plain-string reference per PFS7-X3 (parallel to
  PFS6-X2's no-event-id-$ref posture); the genre-catalog
  consistency audit lifts to OQ4.
- **PFS7-ST5.** `beat_ids`, `strand_ids`, `character_ids` are
  **optional arrays of non-empty strings** — plain-string
  references to sibling-record ids per PFS7-X1. Empty arrays
  are legal (admits progressive authoring, matches Python
  default of `()`).
- **PFS7-ST6.** `archetype_assignments` is an **optional
  array of archetype-assignment objects** defined inline via
  `$defs` per PFS7-X2. Each archetype-assignment requires
  `archetype` (non-empty string); `character_id` (optional
  non-empty string) and `note` (optional string) are admitted
  unconditionally — the S13 exactly-one-of constraint stays at
  the verifier, not the schema (explanation: empty-vs-non-
  empty string distinction is a runtime-semantic check JSON
  Schema doesn't express cleanly without `minLength` on a
  field whose empty-string form is also admitted; see
  anticipated non-finding 3 below). `authored_by` is an
  optional string (Python default `"author"`).
- **`additionalProperties: false`** throughout — top-level and
  in the inline `archetype_assignment` definition.

### PFS7-BT1..BT5 — Beat record shape

`schema/save_the_cat/beat.json` ships the StcBeat record per
save-the-cat-sketch-01 S1/S2/S3 + sketch-02 S11.

- **PFS7-BT1.** Required fields: `id`, `slot`, `page_actual`.
- **PFS7-BT2.** `id` is a non-empty string. `slot` is an
  integer in closed range 1..15 — the bounds match Save-the-
  Cat's 15 canonical beat slots (S1; `NUM_CANONICAL_BEATS` in
  Python). The schema expresses this as
  `{"type": "integer", "minimum": 1, "maximum": 15}`; the
  Python `__post_init__` enforces the same range at
  construction time. `page_actual` is an integer (no bound —
  encodings map to novel / play / prose at authored page
  counts; the monotonicity check stays at the verifier).
- **PFS7-BT3.** `description_of_change` is an optional string
  (Python default `""`); `authored_by` is an optional string
  (Python default `"author"`).
- **PFS7-BT4.** `advances` is an **optional array of strand-
  advancement objects** defined inline via `$defs` per
  PFS7-X2. Each strand-advancement requires `strand_id`
  (non-empty string); `note` is an optional string (Python
  default `""`).
- **PFS7-BT5.** `participant_ids` is an **optional array of
  non-empty strings** — plain-string references to
  StcCharacter ids per PFS7-X1. Empty array is legal (beats
  without wired participants continue to verify; some beats
  describe environmental or collective moments without a named
  character roster).
- **`additionalProperties: false`** throughout.

### PFS7-SR1..SR4 — Strand record shape

`schema/save_the_cat/strand.json` ships the StcStrand record
per save-the-cat-sketch-01 S3 + sketch-02 S11.

- **PFS7-SR1.** Required fields: `id`, `kind`.
- **PFS7-SR2.** `id` is a non-empty string. `kind` is a
  **closed enum** at two values: `{"a-story", "b-story"}`.
  Per S3 — Save-the-Cat distinguishes exactly two strand
  kinds; Python's `StrandKind` enum carries these same two
  values. Matches the dialect's commitment that A and B are
  structural, not nominal.
- **PFS7-SR3.** `description` is an optional string (Python
  default `""`).
- **PFS7-SR4.** `focal_character_id` is an **optional non-
  empty string** — plain-string reference to a StcCharacter
  id per PFS7-X1. Admits `None` in Python (dump omits when
  None per PFS7-D3).
- **`authored_by`** is an optional string (Python default
  `"author"`).
- **`additionalProperties: false`.**

### PFS7-CH1..CH4 — Character record shape

`schema/save_the_cat/character.json` ships the StcCharacter
record per save-the-cat-sketch-02 S9/S10.

- **PFS7-CH1.** Required fields: `id`, `name`.
- **PFS7-CH2.** `id` and `name` are non-empty strings.
- **PFS7-CH3.** `description` is an optional string (Python
  default `""`).
- **PFS7-CH4.** `role_labels` is an **optional array of non-
  empty strings**. Schema admits **any** string (no closed
  enum) per S10's canonical-plus-open posture — the canonical
  ten labels (`protagonist`, `antagonist`, etc.) are
  *recognized* by the verifier for the one-protagonist
  advisory and archetype-matching, but the schema does not
  restrict to them. Open strings (per-genre archetypes,
  author-introduced labels) are admissible. Role-label audit
  lifts to OQ3.
- **`authored_by`** is an optional string (Python default
  `"author"`).
- **`additionalProperties: false`.**

### PFS7-X1 — Flat reference topology at the dialect layer

**Save-the-Cat uses plain-string id references between
sibling records**, not inline `$ref`-bound record arrays.
Concretely:

- `StcStory.beat_ids` is `array<string>`, not `array<StcBeat>`
  (contrast ArMythos.phases which is `array<ArPhase>` via
  cross-file `$ref`).
- `StcStory.strand_ids` is `array<string>`, not `array<StcStrand>`.
- `StcStory.character_ids` is `array<string>`, not
  `array<StcCharacter>`.
- `StcStrand.focal_character_id` is `string` (optional), not
  `StcCharacter` (optional).
- `StcBeat.participant_ids` is `array<string>`, not
  `array<StcCharacter>`.
- `StcArchetypeAssignment.character_id` is `string` (optional),
  not `StcCharacter` (optional).

**Comparison with PFS6-X1.** PFS6-X1 (Aristotelian) used
cross-file `$ref` to inline phase and character records
inside a mythos. That choice reflected Python's `ArMythos.phases`
being `tuple[ArPhase, ...]` — contained records, not id
references.

Save-the-Cat's Python dataclasses use id references (see
StcStory.beat_ids et al.) because beats / strands / characters
live as siblings, authored as module-level tuples (`BEATS`,
`STRANDS`, `CHARACTERS`), with the StcStory indexing them by id.
The same flat-with-id-refs pattern the substrate layer has used
since PFS1 (events reference entities by id-string,
descriptions reference held records by id-string, etc.).

**Commitment: both topologies are admitted.** Each dialect's
schema shape matches its Python shape. The dialect-schema-
namespace convention (PFS6-N1) holds in both cases; the cross-
file `$ref` infrastructure (PFS3-E1's registry-based
resolution) holds where used, trivially unused where it isn't.
**No cross-file `$ref` in any of the four Save-the-Cat
schemas.**

**Consequence for D6 (registry registration).** The Save-the-
Cat schemas do not require each-other for resolution; the
conformance test's `_build_schema_registry` registers them for
symmetry with Aristotelian and for `$id` lookup convenience,
but there are no outbound `$ref`s from any of them. The
registry is only load-bearing when cross-file `$ref` is used;
this sketch exercises the case where it is present-but-unused
at the dialect layer.

**Why this matters.** It confirms that **PFS3-E1's registry
pattern is forgiving** — schemas that don't `$ref` each other
pay no cost by being registered alongside those that do. The
dialect-layer infrastructure (namespace + registry + dump +
discovery) generalizes across both topology choices.

### PFS7-X2 — Inline `$defs` for sub-records without ids

Two Save-the-Cat sub-records do not carry authorial ids:
`StcArchetypeAssignment` (lives inside StcStory's
`archetype_assignments`) and `StrandAdvancement` (lives inside
StcBeat's `advances`). Per PFS7-X2, these ship as **inline
`$defs`** in their parent schema files, not as sibling schema
files:

- `schema/save_the_cat/story.json` carries `$defs/archetype_assignment`.
- `schema/save_the_cat/beat.json` carries `$defs/strand_advancement`.

**Rationale.** Cross-file `$ref` is the right mechanism for
records that:

1. Have ids the user can reference externally, AND
2. May appear across multiple contexts (e.g., ArPhase is used
   by ArMythos today but could be referenced by future
   Aristotelian records).

Archetype-assignment and strand-advancement fail both tests:
no id (binding-only records, keyed by their archetype /
strand_id respectively), and single parent context (archetype-
assignment only appears on StcStory's
`archetype_assignments`; strand-advancement only appears on
StcBeat's `advances`). Inline `$defs` keeps the schema
topology aligned with the Python one.

**Precedent for future dialects.** Dialect-specific sub-
records without authorial ids ship inline. Dialect-specific
records with authorial ids ship as sibling schema files.
Records like Dramatic's `Scene` (has id, one parent context)
are the edge case — sibling file by default, in line with
PFS6-N1's namespace-per-dialect consistency.

### PFS7-X3 — No genre-id or event-id `$ref`

Parallel to PFS6-X2. Event-id strings (if any at the dialect
layer; StcBeat has none today but a future extension might)
would remain plain strings, not `$ref`-typed. The same posture
extends to `stc_genre_id` on StcStory — a reference to a
dialect-catalog StcGenre record, treated as a plain non-empty
string until OQ2 opens (StcGenre schema-ification).

**Consistency with the PFS5/PFS6 posture.** Cross-record
string references remain plain strings unless a forcing
function argues otherwise. The conformance test's audit
surface — referential-integrity verification at validate-time
— stays aligned with OQ4 below (parallel to PFS5 OQ3 /
PFS6 OQ3).

## Dump-layer commitments

Parallel to PFS5-D1/D2 for Branch and PFS6-D1..D3 for
Aristotelian core.

### PFS7-D1 — `_dump_stcstory(story: StcStory) -> dict`

Field-for-field isomorphic. Omits optional fields that default
to `None` (`stc_genre_id` per PFS6-D3's pattern for
`character_ref_id`). Empty tuple fields emit as empty arrays
(matches the dataclass's tuple-default semantics). Nested
`archetype_assignments` tuple is walked and each
`StcArchetypeAssignment` is rendered via a helper that omits
`character_id` when None and emits `note` unconditionally (the
Python default `""` is a string literal, not None; per PFS6-D2
precedent on `annotation`).

### PFS7-D2 — `_dump_stcbeat(beat: StcBeat) -> dict`

Field-for-field. `slot` and `page_actual` emit as integers.
`description_of_change` / `authored_by` emit unconditionally
(string defaults, per PFS6-D2's `annotation` precedent).
`advances` tuple is walked and each `StrandAdvancement` is
rendered with `strand_id` required and `note` unconditional.
`participant_ids` emits as array of strings (empty array when
the Python tuple is empty).

### PFS7-D3 — `_dump_stcstrand(strand: StcStrand) -> dict`

Field-for-field. `kind` dumps as its enum string value
(`"a-story"` or `"b-story"`). `description` / `authored_by`
unconditional. `focal_character_id` omitted when None.

### PFS7-D4 — `_dump_stccharacter(character: StcCharacter) -> dict`

Field-for-field. `name` required; `description` unconditional;
`role_labels` emits as array of strings (empty tuple → empty
array); `authored_by` unconditional.

### PFS7-D5 — `_discover_encoding_save_the_cat(modules: list)`

Returns a quadruple `(stories, beats, strands, characters)` —
four lists — by walking encoding modules. Save-the-Cat
encodings export:

- A singleton `STORY` at module level (an `StcStory`
  instance).
- A tuple `BEATS` (tuple of `StcBeat`).
- A tuple `STRANDS` (tuple of `StcStrand`).
- A tuple `CHARACTERS` (tuple of `StcCharacter`; per
  save-the-cat-sketch-02 S11 wiring).

Both `macbeth_save_the_cat.py` and `ackroyd_save_the_cat.py`
follow this naming. The discovery helper walks these
attributes by name (uppercase `STORY` / `BEATS` / `STRANDS` /
`CHARACTERS`) for every module passed in; accumulates into
four encoding-scoped lists; returns the quadruple.

**No `STC_*` prefix is needed** (contrast PFS6-D4's `AR_*`
prefix for Aristotelian mythos singletons / tuples). Save-the-
Cat encodings are single-Story per module, so the canonical
`STORY` / `BEATS` / `STRANDS` / `CHARACTERS` naming suffices.
Dedup-by-id within an encoding is unnecessary (no shared-
record pattern like Aristotelian Rashomon's repeated-mythos
exports).

### PFS7-D6 — Registry registration

The conformance test's `_build_schema_registry` gains four
new entries: story.json, beat.json, strand.json, character.json.
Order is not load-bearing (no cross-file `$ref` among them per
PFS7-X1); canonical alphabetical order keeps the code
readable.

## Conformance dispositions (anticipated)

No active dispositions anticipated. Four **anticipated non-
findings**:

1. **`description_of_change` and `description` fields default
   to `""` in Python and emit as empty string.** Same pattern
   as PFS6's `annotation` — empty string validates against
   `{"type": "string"}` cleanly; no schema adjustment needed.

2. **`authored_by="author"` always emits (default-valued
   string).** The dump is isomorphic to the Python dataclass;
   schema admits it unconditionally; no disposition.

3. **`archetype_assignments` with `note=""` and no
   `character_id`.** S13's `_check_archetype_assignment_...`
   verifier check flags this as `archetype_assignment_neither_set`,
   but the schema admits it (both fields are optional at the
   schema layer per PFS7-ST6). The check is semantic (empty-
   vs-non-empty string), not structural (field-present-vs-
   absent), and JSON Schema's `required` semantics operate on
   the latter. Schema admits; verifier decides. Not a
   conformance issue — the schema never flags what the
   verifier does.

4. **Characters without canonical `role_labels`.** S10 admits
   open strings; the schema admits any non-empty string per
   PFS7-CH4. Sheppard's `("protagonist", "antagonist",
   "narrator")` tuple validates cleanly — all three are
   canonical. Macbeth's `("ally", "threshold-guardian")` for
   Lady Macbeth (example from sketch-02) also validates —
   both canonical. If a future encoding introduces a genuinely
   open-string role label, schema still admits it; only the
   role-label audit (OQ3) would surface the cross-canonical
   mismatch.

## Corpus expectations

- **StcStory**: 2 records (1 Macbeth + 1 Ackroyd).
- **StcBeat**: 30 records (15 × 2 — every encoding fills all
  15 canonical slots per S1's expectation).
- **StcStrand**: 4 records (2 × 2 — each encoding carries
  one A strand and one B strand per S3).
- **StcCharacter**: 16 records (8 × 2 — the sketch-02
  migration authored 8 characters per encoding).

Every corpus record expected to validate clean under the
implementation. If a non-finding materializes as a true
conformance issue, this sketch gains a §Dispositions section
(none anticipated).

## Open questions

1. **OQ1 — `StcObservation` schema (cross-boundary, Production C).**
   Parallel to PFS6 OQ1 / ArObservation. `StcObservation` is
   ephemeral verifier output; no authored corpus. Ships as
   part of the cross-boundary / verifier-output arc (Lowering,
   VerificationReview, StructuralAdvisory, VerifierCommentary,
   ArObservation, StcObservation, dialect-reading records).
   The cross-boundary schema namespace decision — where these
   records live (`schema/verification/`? `schema/cross_boundary/`?
   flat-at-schema-root?) — is the Production C-opener OQ that
   state-of-play-09 named as a candidate next arc.

2. **OQ2 — Dialect-catalog schemas (`StcCanonicalBeat`,
   `StcGenre`; and a future Aristotelian parallel if any
   surface).** The 15 canonical beats and 10 genres ship as
   module-level constants in `save_the_cat.py`, not as per-
   encoding authored records. A schema would validate them as
   a one-time fixture at module-load; the cost-benefit is
   small (Python already validates via dataclass construction
   + module-load-time assertions `NUM_CANONICAL_BEATS == 15`
   and `len(GENRES) == 10`). Forcing function: a second Save-
   the-Cat variant (author-extended canonical sheet, different
   genres) or a port that wants to validate the catalog
   independently of the Python module. Deferred until one
   surfaces.

3. **OQ3 — Cross-dialect role-label audit.** S10's canonical-
   plus-open role-label set lives in `save_the_cat.py` as
   `CANONICAL_ROLE_LABELS`; open strings are admissible per
   S10. A conformance-test audit could check that every
   StcCharacter.role_labels string is either in the canonical
   set OR in the declared StcGenre's archetypes OR a
   documented author-open label. Useful for catching typos
   (`"antogonist"` for `"antagonist"`). Forcing function: a
   typo case or a multi-encoding drift. Today every non-
   canonical label in the corpus is intentional; banked.

4. **OQ4 — Genre-id and character-id referential integrity
   audit.** Parallel to PFS5 OQ3 / PFS6 OQ3. Every
   `stc_genre_id` on a Story should resolve to a known
   StcGenre (the S6 verifier's `_check_id_resolution` does
   this at verify-time); every id in `beat_ids` / `strand_ids`
   / `character_ids` / `participant_ids` /
   `focal_character_id` / `archetype_assignment.character_id`
   should resolve in the encoding's sibling collections (the
   S6 + S13 checks do this at verify-time). A conformance-
   test-layer audit would extend validation to validate-time.
   Forcing function: an encoding whose ids don't resolve.
   Today the corpus resolves clean; banked.

5. **OQ5 — Dramatic-dialect schemas (PFS8 candidate, gated).**
   Per PFS6 OQ2 — dramatic-sketch-02 is the prerequisite if
   any of the six forcing functions in dramatica-template-
   sketch-01's "Where the dialect resists" section argues for
   a shape change. PFS7's landing validates that the namespace
   + dump + discovery pattern generalizes across two dialects;
   the design-layer question for Dramatic is orthogonal.

## Discipline

Same-as-always under the PFS2 discipline:

- **Sketches before schema.** save-the-cat-sketch-01 S1–S8
  and sketch-02 S9–S13 did the design-layer work for the four
  records shipped here. PFS7 is pure format-rendering plus a
  small number of schema-layer commitments (topology naming;
  inline `$defs` convention; D5 discovery naming).
- **Schemas before code.** No Python change is anticipated
  (the Save-the-Cat dataclasses already match the shapes
  S1/S3/S4/S9/S10/S11/S12 committed). If a conformance issue
  surfaces, the posture is the same as all prior arcs: amend
  the design sketch first; then schema; then Python.
- **First-dialect sets precedent, second-dialect validates.**
  PFS6-N1 and PFS6-D1..D5 were authored as first-dialect
  commitments. PFS7's landing confirms they generalize across
  a structurally different dialect (flat-vs-tree, beat-vs-
  phase, id-ref vs inline-$ref). Generalization is the
  architectural payoff; without a second dialect the
  commitment's load-bearing-ness remains hypothetical.
- **Slim when the design is done.** Same discipline as PFS5 /
  PFS6. Four records instead of three makes this sketch
  slightly longer than PFS6 in record-commitments but the
  governance sections stay stable.
- **Name the contrast.** PFS7-X1 names the flat-vs-tree
  topology distinction explicitly rather than leaving it as
  implicit pattern. Future dialect-schema arcs will cite
  PFS7-X1 (or PFS6-X1) by name when choosing their topology.

## Summary

Second dialect production sketch. Four JSON Schema files for
Save-the-Cat core records (StcStory, StcBeat, StcStrand,
StcCharacter) shipped under a new `schema/save_the_cat/`
subdirectory. Twenty-three commitments:

- **PFS7-N1** — namespace inherits PFS6-N1
  (`schema/save_the_cat/`).
- **PFS7-ST1..ST6** — Story shape (required id/title; optional
  theme / genre / beat_ids / strand_ids / character_ids /
  archetype_assignments; archetype_assignment inline via
  `$defs`).
- **PFS7-BT1..BT5** — Beat shape (required id / slot /
  page_actual; slot bounded 1..15; advances as array of
  inline strand_advancement; participant_ids as string array).
- **PFS7-SR1..SR4** — Strand shape (required id / kind; kind
  closed enum at `{a-story, b-story}`; optional description /
  focal_character_id).
- **PFS7-CH1..CH4** — Character shape (required id / name;
  optional description / role_labels; no closed enum on
  role_labels per S10 canonical-plus-open).
- **PFS7-X1** — flat-with-id-ref reference topology admitted
  alongside PFS6-X1's tree-with-inline-$ref. Each dialect's
  shape matches its Python shape.
- **PFS7-X2** — inline `$defs` convention for sub-records
  without authorial ids (archetype_assignment, strand_advancement).
- **PFS7-X3** — no `$ref` on genre-id or future event-id
  cross-references (plain-string, parallel to PFS6-X2).
- **PFS7-D1..D6** — dump helpers (4) + discovery helper +
  registry registration.

Five open questions banked with forcing functions:
StcObservation + cross-boundary records (OQ1, Production C);
dialect-catalog schemas (OQ2); role-label cross-check audit
(OQ3); referential-integrity audit (OQ4); Dramatic-dialect
schemas (OQ5, gated).

No design derivation needed. Save-the-cat-sketch-01 +
sketch-02 already committed the record shapes; this sketch
renders them as JSON Schema 2020-12, names the flat-vs-tree
topology contrast with Aristotelian, commits the inline-$defs
convention for id-less sub-records, and hands off to
implementation.

Python untouched at the sketch layer. Dump-layer + discovery +
test-suite extensions land in the implementation commit.
Substrate schema layer remains structurally + behaviorally
complete; dialect schema layer grows to two-of-four landed
(Aristotelian + Save-the-Cat), with Dramatic and Dramatica-
complete still pending.
