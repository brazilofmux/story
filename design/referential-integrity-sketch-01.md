# Referential integrity — sketch 01

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (new topic — a second validation layer
underneath the shape schemas)
**Frames:** [production-format-sketch-05](production-format-
sketch-05.md) OQ3 (branch-label cross-reference audit);
[production-format-sketch-06](production-format-sketch-06.md)
OQ3 (dialect-layer event-id cross-reference audit), OQ4
(cross-dialect character_ref_id audit); [production-format-
sketch-07](production-format-sketch-07.md) OQ4 (Save-the-Cat
id referential integrity); [production-format-sketch-09](
production-format-sketch-09.md) OQ5 (CrossDialectRef dialect-
token open-string);
[production-format-sketch-10](production-format-sketch-10.md)
OQ1 (CrossDialectRef resolution across namespaces)
**Related:** the per-dialect self-verifiers that already carry
runtime id-resolution checks — aristotelian.verify A7 check 4
(event-ref integrity), save_the_cat.verify S13 checks 1
(character-id resolution, archetype-character-id resolution,
strand-character-id resolution); [architecture-sketch-02](
architecture-sketch-02.md) A6 (dialects are plural and
author-extensible — open dialect tokens follow from this)
**Superseded by:** nothing yet

## Purpose

**Open the validation-layer topic.** Four production-format
sketches have forked the same open question: schemas validate
record **shape**; a conformance-test-layer audit would extend
validation to **resolution**. This sketch commits the audit
vocabulary, algorithm, disposition protocol, and scope for a
first implementation arc.

Resolution is the check: every id-string reference a record
carries — event-id on an ArPhase, character-id on an
StcArchetypeAssignment, branch label on an Event — names an
**existing record of the expected type in the same encoding**.
Schemas have always carried shape; resolution has lived
scattered across per-dialect self-verifiers (when it's checked
at all), reachable only by running those verifiers manually.
The audit lifts the check into the conformance-test surface
so it runs unconditionally when tests run.

**The forcing functions converged.** Each of the five banked
OQs named the same criterion: "a typo in an id string, or a
renamed record not cleaned up at its references, that the
schema shape check would miss." Waiting for each forcing
function to fire individually would leave the gap open across
five record types. Closing them together is cheaper per OQ.

## Why now

- **Five sketches have banked the same OQ with the same forcing
  function.** PFS5 OQ3 (branch labels on Event), PFS6 OQ3
  (Aristotelian event-ids), PFS6 OQ4 (character_ref_id),
  PFS7 OQ4 (Save-the-Cat id references), PFS10 OQ1
  (CrossDialectRef). The OQs themselves are cheap individually;
  the aggregate is a principle — validate resolution, not just
  shape — that deserves its own topic sketch.
- **The corpus is large enough to find typos.** 156 Lowering
  records + 58 VerificationReview records + 33 Description +
  377 Entity + 458 Event + 199 Held + 25 Branch + 5 ArMythos
  (with 15 ArPhase + 6 ArCharacter) + 2 StcStory (with 30
  StcBeat + 4 StcStrand + 16 StcCharacter + 6 StcArchetypeAssignment)
  = ~1,400 records carrying id-references. A single typo across
  that corpus is the expected case if no resolution check runs.
- **Per-dialect verifiers already prove the check is
  implementable.** Aristotelian's A7 check 4 does event-ref
  integrity; Save-the-Cat's S13 check 1 does character-id
  resolution. The audit doesn't invent a new check; it lifts
  existing checks into a shared, dialect-agnostic conformance
  layer.
- **PFS2 discipline points at this.** Schemas first, Python as
  conformance. The conformance test already validates shape.
  The same infrastructure (loaders + discovery + dump
  + validate) extends naturally to resolution; the test
  already iterates every corpus record, so an additional
  per-record audit pass is near-free per record.

## Scope — what this sketch covers

**In (first implementation arc):**

- A committed audit algorithm: discovery → target-set
  collection → per-reference resolution → failure-vocabulary
  surfacing.
- Failure vocabulary: `unresolved` (first-arc focus) plus
  named placeholders for future-arc kinds (`ambiguous-target`,
  `type-mismatch`).
- Disposition protocol parallel to the existing PFS
  conformance-dispositions protocol: known-accepted
  unresolved-references may be declared at the sketch layer
  (amend the design sketch; then the test accepts them).
- Scope enumeration for this first arc (RI7 below) — which
  reference types get audited, which are banked for follow-
  on arcs.
- Compositional rules with per-dialect self-verifiers (RI5).

**Out (banked):**

- CrossDialectRef resolution across namespaces (Lowering's
  upper_record / lower_records, VerificationReview's
  target_record, etc.) — requires cross-encoding lookup
  mechanism. Banked to referential-integrity-sketch-02.
  Forcing function: the first-arc audit lands cleanly and we
  want to close PFS10 OQ1.
- Typed `IntegrityFinding` record type. First arc surfaces
  failures as conformance-test output (print + assert); a
  future arc may promote findings to typed records with
  their own schema file and walker integration. Forcing
  function: a downstream consumer wants to ingest findings
  as records.
- Dialect-catalog reference resolution (e.g., `stc_genre_id`
  → StcGenre catalog). Gated on dialect-catalog schema
  decisions (PFS7 OQ2). Banked.
- Type-mismatch detection (e.g., a reference that resolves
  to a record of the wrong type — a `participant_ids` value
  that's actually an Event id rather than a Character id).
  Requires a type-aware resolution model. Banked to a future
  arc.
- Cross-encoding ambiguity detection (same id in two
  encodings). Most useful after CrossDialectRef audit lands.
  Banked.

## Commitments

### RI1 — The audit runs in the conformance test, not in the shape validator

The audit is a **second validation layer**, executed at
conformance-test time using the same discovery + dump
infrastructure as the existing shape tests. Schema files
remain shape-only; the resolution check is code, not schema.

**Rationale.** JSON Schema 2020-12 has no referential-
integrity primitive. Extensions exist in the wider JSON Schema
ecosystem (e.g., `relational-json-schema`, custom keyword
vocabularies), but adopting one would weaken the PFS1
commitment to vanilla 2020-12. Python-code-in-the-test is the
right place for resolution logic.

**Where it lives.**
`prototype/tests/test_production_format_sketch_01_conformance.py`
gains a new `# Referential integrity` section with audit
functions. New tests in the same module, not a new file — the
audit shares the schema loaders, encoding discovery, and dump
helpers with the shape tests.

### RI2 — Per-reference-kind audit functions

Each reference kind gets its own audit function named
`_audit_<reference_kind>`. Functions collect target-id sets
from the encoding, iterate reference sources, and return a
list of findings (`unresolved` findings for this first arc).

**Naming convention.**

- `_audit_branch_labels_on_events` — Event.branches → Branch
  labels (PFS5 OQ3).
- `_audit_aristotelian_event_refs` — ArMythos and ArPhase
  event-ids → Event ids in the same encoding (PFS6 OQ3).
- `_audit_save_the_cat_intra_story_refs` — StcStory /
  StcBeat / StcStrand / StcArchetypeAssignment id references
  → the matching sibling record collection (PFS7 OQ4).

Each audit function owns its resolution rule. The shared
algorithm (collect target set, iterate sources, classify
failures) is inlined per function in this first arc —
factoring to a shared helper is a second-arc concern when
the third or fourth audit function ships and the duplication
pressure argues for it (parallel to PFS5's attention-based
vs. typed approach — abstract when the concrete has enough
cases to pressure it, not before).

### RI3 — Resolution model: target-set collection + membership check

The audit's operational model:

1. **Collect target sets per encoding.** For the Aristotelian
   event-ref audit, the target set is the encoding's Event
   id collection. For the Save-the-Cat character-id audit,
   the target set is the encoding's StcCharacter id set.
2. **Iterate reference sources.** For each record, extract
   its id-references (the schema has already validated they
   are non-empty strings).
3. **Check membership.** Reference resolves iff the id
   string is in the target set.
4. **Classify failures.** Unresolved reference → `unresolved`
   finding.

**Per-encoding scoping.** The audit operates **within an
encoding**: an ArPhase in Oedipus's encoding references an
Event id that must exist in Oedipus's encoding, not in some
other encoding. Cross-encoding reference (what's the encoding
an ArMythos belongs to?) is a CrossDialectRef audit concern,
banked to sketch-02.

**Implicit dialect binding.** Save-the-Cat references operate
across sibling records within one `*_save_the_cat.py` module
(STORY + BEATS + STRANDS + CHARACTERS). Aristotelian event-id
references span the Aristotelian encoding (`*_aristotelian.py`)
and the substrate encoding (`*.py`, e.g., `oedipus.py`) sharing
the same work-id prefix. Discovery matches the work-id prefix:
`oedipus_aristotelian` → `oedipus`; `macbeth_save_the_cat` is
self-contained (STORY + BEATS + STRANDS + CHARACTERS in one
module).

### RI4 — Failure vocabulary

First-arc vocabulary:

- `unresolved` — the reference's id string has no matching
  target record. Most common failure; indicates either a
  typo, a renamed-not-updated target, or a reference to a
  record that doesn't exist yet.

**Reserved for future arcs:**

- `ambiguous-target` — the id resolves to multiple records
  (e.g., same id in two encodings). Only meaningful under
  cross-encoding CrossDialectRef audit. Reserved.
- `type-mismatch` — the id resolves to a record of the wrong
  type (e.g., a character-id that matches an Event id).
  Requires type-aware resolution. Reserved.

**No severity gradation in first arc.** All first-arc
findings are asymmetric errors — an unresolved reference is
always a problem, always surfaced. A future arc may add a
`noted` severity for known-accepted cases (parallel to
LoweringObservation.severity), but the disposition protocol
(RI6 below) handles the known-accepted case more directly.

### RI5 — Composition with per-dialect self-verifiers

Aristotelian's `aristotelian.verify` A7 check 4 already does
event-ref integrity. Save-the-Cat's `save_the_cat.verify`
S13 check 1 already does character-id resolution. The audit
**does not remove** these per-dialect checks; they retain
their role as runtime verification invoked by callers of
`verify()`.

**The audit's distinct value.**

- **Runs unconditionally at test time.** Per-dialect
  verifiers run only when `verify()` is called; the audit
  runs every test invocation.
- **Shares the conformance-test output convention.** Findings
  surface via the same print-and-assert pattern as every
  other corpus-conformance test, reachable by test-runner
  output consumers.
- **Single pass.** One audit invocation covers all encodings
  of all record types in one iteration; per-dialect verifiers
  would each need to be invoked separately and their outputs
  aggregated.

**Explicit overlap.** For Aristotelian event-refs and Save-
the-Cat character-ids, the audit duplicates the per-dialect
check. Duplication is intentional — the audit is a
*different* validation *surface*, not a replacement for the
verifier. Dropping the per-dialect check would couple the
verifier-API surface to the conformance-test surface in an
unwanted way.

### RI6 — Dispositions protocol (parallel to PFS)

If a first-arc audit surfaces an unresolved reference that
turns out to be intentional (a PENDING-style forward
reference to a record that doesn't yet exist; a deliberate
external-system id that the audit shouldn't try to resolve),
the sketch layer gets amended to declare the known case.

**Mechanism:**

1. **Audit surfaces the finding.** Test fails with
   unresolved-reference output.
2. **The finding is evaluated.** Either (a) the reference is
   a typo — fix the encoding; or (b) the reference is
   intentional — the sketch gets a §Dispositions entry
   naming the known case.
3. **The test accepts the disposition.** The audit function
   gets a disposition-check-in: if the finding matches a
   known disposition, it does not fail the test.

**Explicit ban on "make the test pass by listing the
finding".** Dispositions require sketch-level amendment —
the test is not the right place to silently accept new drift
(parallel to PFS §Known dispositions protocol).

**No dispositions anticipated for first-arc audit.** Corpus
is expected clean. If findings surface, we follow the
protocol.

### RI7 — First-arc scope

This sketch's first implementation arc covers **three**
audits:

1. **Substrate branch labels** — every `event.branches` label
   resolves to a key in the encoding's `ALL_BRANCHES` dict.
   Closes PFS5 OQ3.
2. **Aristotelian event-id references** — every `event_id`
   field on ArMythos (central_event_ids, complication,
   denouement, peripeteia, anagnorisis) and ArPhase
   (scope_event_ids) resolves to an Event id in the paired
   substrate encoding. Closes PFS6 OQ3.
3. **Save-the-Cat intra-story references** — every id
   reference on StcStory (beat_ids / strand_ids /
   character_ids), StcBeat (participant_ids,
   advances[*].strand_id), StcStrand (focal_character_id),
   and StcArchetypeAssignment (character_id) resolves to
   the matching sibling record in the encoding. Closes
   PFS7 OQ4.

**Deferred to second-arc (referential-integrity-sketch-02):**

- CrossDialectRef resolution (Lowering, Verification-family
  records) — requires cross-encoding lookup.
- Cross-dialect character_ref_id (ArCharacter.character_ref_id
  → substrate Entity or Dramatic Character) — requires
  multi-dialect resolution rules (PFS6 OQ4).
- Dialect-catalog references (stc_genre_id → StcGenre).
- Substrate-internal entity-id resolutions (event.participants,
  effect args, held prop args). Partially redundant with the
  substrate's existing invariants (Event __post_init__
  doesn't check, but many invariants assume resolution).
  Banked pending corpus-surfaced need.
- Supersession metadata chains (Lowering.metadata["supersedes"]
  → Lowering id; Branch.metadata["supersedes"] → Branch
  label). Already checked at runtime by
  `validate_lowerings` / substrate fold machinery; the
  conformance-test audit would add a second check surface.
  Banked; low urgency.

### RI8 — No new records, no new schema files (first arc)

The first arc produces no typed output records; findings are
conformance-test prints + assertions. A future arc may
promote findings to a typed `IntegrityFinding` record with
its own schema under `schema/verification/` (it's observation-
shaped, would fit the existing verification namespace per
PFS10-N1's precedent). Forcing function: a downstream
consumer — a walker surface, a CI pipeline tracking findings
across runs — that wants typed records rather than test
output.

## Anticipated conformance (first-arc)

No active dispositions anticipated. Three anticipated
**clean-pass** outcomes:

1. **Branch labels on Events resolve.** Every corpus Event's
   branches tuple contains only labels that appear as keys
   in the encoding's ALL_BRANCHES. If this fails, it
   indicates either a typo (author meant one label, wrote
   another) or a removed-but-not-cleaned branch reference.
2. **Aristotelian event-ids resolve.** The A7 self-verifier
   already runs this check when Aristotelian encodings are
   verified; the audit-layer version runs at conformance
   time instead of verifier-invocation time. No new
   findings expected.
3. **Save-the-Cat intra-story references resolve.** The S13
   self-verifier already runs the character-id portion of
   this; archetype_assignment.character_id is an additional
   surface. Expected clean.

If any of the three surfaces findings, the sketch gains a
§Dispositions section and the finding is evaluated per the
RI6 protocol.

## Open questions

1. **OQ1 — Second-arc CrossDialectRef audit.** The load-
   bearing next audit: Lowering.upper_record,
   Lowering.lower_records, VerificationReview.target_record,
   StructuralAdvisory.scope[*],
   VerificationAnswerProposal.question_id all need
   resolution. Requires a cross-encoding lookup mechanism
   (encoding A's Lowering may point at encoding B's
   records through shared id conventions). Banked to
   referential-integrity-sketch-02 when first-arc lands
   cleanly. Closes PFS10 OQ1.

2. **OQ2 — Cross-dialect character_ref_id audit.**
   ArCharacter.character_ref_id points at either a substrate
   Entity id or a Dramatic Character id in the same encoding.
   Resolution requires a multi-dialect fallback lookup. The
   first-arc Aristotelian audit does NOT cover this;
   character_ref_id stays unvalidated until a second-arc
   extension. Closes PFS6 OQ4.

3. **OQ3 — Disposition file format.** If dispositions
   accumulate (not anticipated but possible), a per-sketch
   disposition markdown or a per-encoding disposition file
   becomes warranted. Banked.

4. **OQ4 — Typed IntegrityFinding record.** Would belong in
   `schema/verification/` per PFS10-N1's precedent. Schema
   shape: severity + code + target_record +
   reference_source + reference_target + message — plus a
   `kind` field with the first-arc + future-arc vocabulary.
   Banked pending downstream consumer.

5. **OQ5 — Substrate-internal entity-id audits.**
   event.participants[role], effect.prop.args,
   held.prop.args, held.provenance all carry id-references
   that could be audited. Substrate records are the layer
   with the densest references; auditing them comprehensively
   would surface a large target-set lookup per event (every
   record references one or more entities). Banked because
   (a) the substrate has strong construction-time invariants
   that catch most of these, and (b) the target-set
   construction cost is O(N) per encoding per audit function.
   A forcing function — e.g., a typo found in production
   that the substrate invariants missed — would change the
   calculus.

## Discipline

- **Design sketch first.** This sketch. It commits the
  audit vocabulary, algorithm, and scope before
  implementation. The one-commit design-only shape matches
  the PFS8 opener's.
- **Implementation follows the sketch.** Three audit
  functions (RI7 scope) + the discovery integration +
  per-audit corpus conformance tests. Expected ~6 new
  conformance tests (one per audit function + one "no
  dispositions" integration).
- **Conformance-test layer, not schema layer.** RI1.
  Schemas stay shape-only; audit is code.
- **Additive to per-dialect verifiers, not a replacement.**
  RI5. The audit's value is its always-on nature, not a
  substitute for the per-dialect-verifier surface.
- **Close-what's-converged, bank-what's-independent.** RI7.
  First arc closes 3 of 5 OQs that converged; the 2
  remaining (CrossDialectRef; cross-dialect
  character_ref_id) get their own arc under sketch-02.

## Summary

First topic sketch in a new design area: **conformance-test-
layer referential integrity**. Commits the audit vocabulary
(unresolved finding; reserved ambiguous-target / type-
mismatch), the algorithm (collect target set → iterate
references → check membership), the disposition protocol
(sketch-level amendment for known-accepted cases), and the
first-arc scope (substrate branch labels, Aristotelian
event-id references, Save-the-Cat intra-story references).

Eight commitments (RI1..RI8). Five OQs banked with forcing
functions: CrossDialectRef audit (OQ1, sketch-02);
character_ref_id multi-dialect audit (OQ2, sketch-02);
disposition file format (OQ3); typed IntegrityFinding
record (OQ4); substrate-internal entity-id audits (OQ5).

Closes three of five OQs from the prior-sketch bank (PFS5
OQ3, PFS6 OQ3, PFS7 OQ4) on implementation. Two more (PFS6
OQ4, PFS10 OQ1) move to referential-integrity-sketch-02.

No schema file created; no new record type; no Python
prototype change. The conformance-test surface extends in
one principled way: shape validation + resolution audit,
both at the same layer.

The audit's architectural claim: validation of records is a
**two-tier** surface. Tier 1 = shape (what fields,
what types, what enums) — served by JSON Schema 2020-12
files under `schema/`. Tier 2 = resolution (do the
id-references resolve to real records) — served by Python
audit code in the conformance test. Both tiers use the same
infrastructure (discovery + dump + corpus iteration); both
tiers surface findings via the same print-and-assert
pattern. Adding Tier 2 now — with the corpus large enough
to find typos — completes a validation surface that can
carry the whole production story-engine record set without
leaving gaps.
