# State of play — sketch 10

**Status:** active
**Date:** 2026-04-19
**Supersedes:** [state-of-play-09](state-of-play-09.md)

Cold-start orientation doc, rewritten (not amended) at the
milestone where the **cross-boundary schema layer begins**, the
**Tier-2 audit layer closes its first-round open questions**,
and the **Aristotelian dialect earns its second (amendment-only)
sketch via a probe-closure loop**.

**Fifteen commits since state-of-play-09** — eight production-
format / schema commits, four Tier-2 audit commits, one ATTWN
substrate-content commit, one Aristotelian-sketch-02 dialect-
amendment pair, and one production-infrastructure refactor
pulling audit primitives out of the test file into a reusable
module. All fifteen land on 2026-04-19 (continuing the one-day
cadence the corpus has held since sketch-07).

Grouped by arc:

- `329dcae` — production-format-sketch-07 (implementation).
  Second dialect schemas ship: `schema/save_the_cat/` gains
  `character.json` / `strand.json` / `beat.json` / `story.json`.
  +12 conformance tests (4 metaschema + 4 shape + 4 corpus).
  717 → 729 tests passing.
- `ee5820a` — production-format-sketch-08 (design only).
  Production C-opener. Commits two top-level schema
  subdirectories (`schema/lowering/`, `schema/verification/`),
  classifies 22 known Python record types into target
  namespaces or the deferred set, briefs PFS9–PFS12 per-record
  sketches.
- `31a9c48` — production-format-sketch-09 (design). Lowering
  family: 3 records (Lowering + AnnotationReview +
  LoweringObservation) + inline sub-record $defs
  (CrossDialectRef + Annotation + PositionRange).
- `964ebb6` — production-format-sketch-09 (implementation).
  Three JSON Schema files under `schema/lowering/`;
  +9 conformance tests. 729 → 738. First cross-boundary-tier
  landing.
- `42820a6` — production-format-sketch-10 (design).
  Verification family: 4 records (VerificationReview +
  StructuralAdvisory + VerificationAnswerProposal +
  VerifierCommentary). Re-inlines CrossDialectRef per PFS8-V
  guidance.
- `a232136` — production-format-sketch-10 (implementation).
  Four JSON Schema files under `schema/verification/`;
  +12 conformance tests. 738 → 750. Second cross-boundary
  family.
- `8b4f15e` — referential-integrity-sketch-01 (design only).
  Opens the Tier-2 audit topic. RI1–RI8 commit audit
  vocabulary, algorithm, scope, disposition protocol, and the
  first-arc three-audit selection (closing PFS5/OQ3,
  PFS6/OQ3, PFS7/OQ4).
- `a7a1223` — referential-integrity-sketch-01 (implementation).
  Three audit tests added. 313 Event branch-label refs + 132
  Aristotelian event-id refs + 132 Save-the-Cat intra-story
  refs, all clean. 750 → 753.
- `8d40103` — referential-integrity-sketch-02 (design).
  Six commitments (RI9–RI14) covering CrossDialectRef
  resolution + character_ref_id multi-dialect fallback.
- `9bb3bf5` — referential-integrity-sketch-02 (implementation).
  Two cross-encoding audit tests added + §D1 disposition
  (Dramatica-complete axis-label tokens `Story_goal` /
  `Story_consequence` accepted as non-record references).
  520 CrossDialectRef refs (512 clean, 8 dispositioned) +
  6 character_ref_id refs (all clean). 753 → 755.
- `43c4d74` — and_then_there_were_none substrate fill
  (research track). Sixth encoding with substrate layer
  authored: 14 entities, 15 events, 4 descriptions, 100
  per-listener KnowledgeEffects at the gramophone event.
  Dramatic/Dramatica-complete/Lowering/Verification still
  skeleton. Baseline 755 unchanged.
- `00c5733` — aristotelian-sketch-02 (design). First dialect-
  amendment sketch. A10–A12 add ArMythosRelation, ArAnagnorisis-
  Chain, ArPeripeteiaAnagnorisisBinding + A7.6–A7.9 self-
  verifier checks. Closes three of five probe-sketch-01
  relations_wanted; holds out ArFrameMythos (substrate-blocked)
  and rejects ArAnagnorisisLevel (A4/A8 scope).
- `2949284` — aristotelian-sketch-02 (implementation).
  `core/aristotelian.py` gains three dataclasses + four
  checker functions + extended `verify()` signature; Oedipus
  + Rashomon encodings migrate. +37 unit tests. 755 → 792.
- `0651121` — conformance module factoring (production
  infrastructure). Audit primitives + discovery helpers
  extracted into `story_engine/core/conformance.py` (1038
  lines). Test file shrinks 4568 → 3862 lines. 792 unchanged.
- `c7be699` — aristotelian-probe-sketch-02 (research track).
  Live re-probe of Oedipus + Rashomon under sketch-02
  extensions. All three closure hypotheses verified; four
  second-order OQs banked (OQ-AP1 ArPathos, OQ-AP2
  ArCanonicalFloor, OQ-AP3 ArProseOnlyCause, OQ-AP4
  peripeteia-in-beginning). Test count unchanged.

**Headline.** Three load-bearing claims.

1. **The cross-boundary schema layer has begun.**
   State-of-play-09 listed Production C (cross-boundary
   records) as a single line-item on the next-up list; sketch-
   10 moves it to "partially shipped with design scaffolding
   complete." Two top-level namespaces (`schema/lowering/`,
   `schema/verification/`) are committed; seven records across
   the two (3 Lowering + 4 Verification) ship as JSON Schema
   2020-12 files with corpus-conformance tests. The Production
   C namespace map (PFS8) classifies all 22 known Python
   record types; PFS11 (Aristotelian batch) and PFS12 (Save-
   the-Cat observation) remain, and PFS13 (Dramatic) is still
   gated on dramatic-sketch-02.

2. **The Tier-2 audit layer closes its first-round banked OQs.**
   Validation is a two-tier surface: shape (JSON Schema 2020-12
   files) and resolution (Python audit code). Sketch-10 lands
   the Tier-2 scaffold in five audit functions across two
   arcs. 5 of 5 first-round banked OQs from the PFS series
   close (PFS5/OQ3, PFS6/OQ3, PFS6/OQ4, PFS7/OQ4, PFS10/OQ1).
   One disposition surfaces (§D1: dramatica-complete
   `Story_goal` / `Story_consequence` axis labels accepted as
   non-record tokens). 1043 references resolved across six
   audit kinds. The audit primitives are then factored into
   `story_engine/core/conformance.py` so any downstream caller
   (future walker, pre-commit hook, CI wrapper) can invoke
   them without reading the test scaffolding.

3. **The Aristotelian dialect earns sketch-02 via a probe-
   closure loop.** First dialect amendment sketch. Aristotelian-
   probe-sketch-01 surfaced five relations_wanted; sketch-02
   closes three (ArMythosRelation, ArAnagnorisisChain,
   ArPeripeteiaAnagnorisisBinding), defers ArFrameMythos
   (substrate-blocked), rejects ArAnagnorisisLevel (A4/A8
   scope — audience-level anagnorisis would widen dialect scope
   into reader-response territory sketch-01 deliberately
   closed). Aristotelian-probe-sketch-02 then re-probes under
   the sketch-02 surface: the three well-forced proposals
   verifiably close (the probe cites them structurally in its
   v2 reading), and three genuinely-new second-order forcing
   functions bank (OQ-AP1..OQ-AP4). Rashomon `read_on_terms`
   upgrades from `partial` to `yes`; `drift_flagged` shrinks
   from 5 items to 0. Sketch-01's architectural verdict
   (extension-only, no core-record modification) extends
   cleanly through sketch-02 and the re-probe.

Re-write this sketch (don't amend — write sketch-11) at the
next milestone.

---

## What is built — delta from sketch-09

### The schema layer (two new top-level dirs + seven cross-boundary records + four Save-the-Cat dialect records)

**Cross-boundary tier, first landings:**

- `schema/lowering/lowering.json` (new, 141 lines) — Lowering
  per lowering-record-sketch-01 L1–L10, with inline $defs for
  CrossDialectRef + Annotation + PositionRange sub-records
  (PFS9-X1). Required id / upper_record / lower_records /
  status / anchor_τ_a / authored_by / annotation. status
  closed enum at {active, deferred, proposed, rejected}.
  allOf/if-then-else for status=active requires non-empty
  lower_records (PFS9-X3).
- `schema/lowering/annotation_review.json` (new, 33 lines) —
  shape for review_states array entries on Annotation +
  reader-model probe annotation_review_candidates.
- `schema/lowering/lowering_observation.json` (new, 31 lines)
  — severity + code + target_id + message; lifts
  validate_lowerings' emission pattern to schema.
- `schema/verification/verification_review.json` (new) —
  verdict closed enum {approved, needs-work, partial-match,
  noted}; optional match_strength (number in [0,1]).
- `schema/verification/structural_advisory.json` (new)
- `schema/verification/verification_answer_proposal.json` (new)
- `schema/verification/verifier_commentary.json` (new)

**Dialect tier, second dialect:**

- `schema/save_the_cat/character.json` (new, 37 lines) — PFS7-
  CH1..CH4. role_labels no-enum per S10's canonical-plus-open
  posture (Sheppard's overlapping protagonist/antagonist/
  narrator triple lands clean).
- `schema/save_the_cat/strand.json` (new, 34 lines) — PFS7-
  SR1..SR4. kind closed enum at {a-story, b-story}.
- `schema/save_the_cat/beat.json` (new, 68 lines) — PFS7-
  BT1..BT5 + PFS7-X2. slot integer 1..15 matching
  NUM_CANONICAL_BEATS. advances as inline $defs per PFS7-X2.
- `schema/save_the_cat/story.json` (new, 89 lines) — PFS7-
  ST1..ST6. beat_ids / strand_ids / character_ids as plain-
  string arrays (PFS7-X1 flat-with-id-refs topology,
  contrasting PFS6-X1 tree-with-inline-$ref).

**No substrate schema file changes.** The six substrate
schemas remain unchanged; substrate layer is still structurally
AND behaviorally complete per sketch-09.

**Schema README restructured twice:** once at PFS7 landing to
group the dialect layer by dialect (Aristotelian three + Save-
the-Cat four), once at PFS9 landing to add a "Cross-boundary
layer" supersection. Cross-file references narrative now names
two dialect topologies (tree-with-$ref; flat-with-id-refs) and
the registry-is-load-bearing distinction between Lowering
(outbound $ref) and Save-the-Cat (no outbound $ref).

### The design sketches (nine new)

- `design/production-format-sketch-07.md` (new, 762 lines).
  Second dialect production sketch — slim pattern, no design
  derivation (save-the-cat-sketch-01 + -02 had already
  committed field-level shape). PFS7-N1 inherits PFS6-N1
  namespace. PFS7-X1 flat-with-id-refs topology is admitted as
  the second dialect-layer reference shape. PFS7-X2 inline
  $defs for StrandAdvancement + ArchetypeAssignment (single-
  parent-context sub-records).
- `design/production-format-sketch-08.md` (new, 558 lines).
  Production C-opener. Two commitments: PFS8-N1 (two top-level
  role-named namespaces for cross-boundary records —
  structural vs. observational), PFS8-N2 (dialect-internal
  records stay under `schema/<dialect>/`). Twenty-two Python
  record types classified — 11 to new top-level namespaces,
  5 to existing dialect namespaces, 6 deferred as runtime/
  ephemeral.
- `design/production-format-sketch-09.md` (new, 612 lines).
  First per-record sketch under Production C. Ten Lowering
  commitments (PFS9-L1..L10) + four AnnotationReview
  (PFS9-AR1..AR4) + four LoweringObservation (PFS9-LO1..LO4)
  + four cross (PFS9-X1..X4) + eight dump/discovery
  (PFS9-D1..D8). Closes PFS8 OQ3 — CrossDialectRef.dialect is
  open string, not closed enum (architecture-sketch-02 A6
  extensibility commitment).
- `design/production-format-sketch-10.md` (new, ~750 lines).
  Second cross-boundary production sketch. Four record
  families (VR + SA + AP + VC) ship + PFS10-X1..X3 (re-inline
  CrossDialectRef per PFS8-V guidance; verdict closed enum;
  match_strength in [0,1]).
- `design/referential-integrity-sketch-01.md` (new, 476 lines).
  Opens the Tier-2 audit topic. RI1–RI8 commit audit
  vocabulary, algorithm, scope, disposition protocol, first-
  arc selection. Architectural claim: validation is a TWO-
  TIER surface (Tier 1 = shape / JSON Schema files; Tier 2 =
  resolution / Python audit in conformance test). Five OQs
  banked with forcing functions.
- `design/referential-integrity-sketch-02.md` (new, 474 lines
  after §D1 amendment). Six commitments (RI9–RI14) for cross-
  encoding audits + §D1 disposition (added at implementation
  time). Four OQs banked forward.
- `design/aristotelian-sketch-02.md` (new, 341 lines). First
  dialect amendment sketch. A10–A12 (three record/field
  additions) + A7.6–A7.9 (four self-verifier checks). AA1–AA11
  action items; AA11 explicitly defers schema-layer landing
  of A10–A12 to a future PFS arc. Six OQs banked.
- `design/aristotelian-probe-sketch-02.md` (new, 230 lines).
  Re-probe under sketch-02. APA2-1..APA2-4 acceptance
  criteria. Closure ledger: three CLOSED, one PERSISTS-AS-
  LIMIT (correct per deferral), one RE-SURFACES (correct per
  rejection). Four banked OQs (OQ-AP1..OQ-AP4) with forcing-
  function criteria for a hypothetical sketch-03.
- `design/README.md` — four new entries (per-topic active-
  sketches section): PFS7/8/9/10, RI sketches, Aristotelian
  sketch-02 + probe-sketch-02.

### The production infrastructure (conformance module extracted)

`prototype/story_engine/core/conformance.py` (new, 1038
lines). First time audit primitives are callable outside the
test file. Contents:

- `AuditFinding` + `AuditReport` frozen dataclasses. Reports
  expose `findings`, `stats`, `report_lines`,
  `is_clean() / failure_message() / print_report()`.
- Discovery helpers (`_iter_encoding_modules`,
  `_discover_encoding_events`,
  `_discover_encoding_aristotelian_records`,
  `_discover_encoding_save_the_cat_records`,
  `_discover_encoding_lowerings`,
  `_discover_encoding_verifier_output`).
- Dialect-resolution helpers (`DIALECT_TOKEN_SUFFIX`,
  `AXIS_LABEL_DISPOSITIONS`, `work_from_lowerings_module`,
  `work_from_verification_module`,
  `collect_dialect_record_ids`).
- Five audit functions, each returning `AuditReport`:
  - `audit_branch_labels` — RI7 #1 (closes PFS5 OQ3).
  - `audit_aristotelian_event_refs` — RI7 #2 (closes PFS6 OQ3).
  - `audit_save_the_cat_intra_story` — RI7 #3 (closes PFS7 OQ4).
  - `audit_cross_dialect_refs` — RI9–RI12 (closes PFS10 OQ1)
    + §D1.
  - `audit_character_ref_ids` — RI13 (closes PFS6 OQ4).

Test file internal structure: the five audit test bodies
shrink to 4–9 lines each (call `audit_*()`, print, assert
`is_clean()`). Discovery helpers duplicated between test file
and module (intentional pragmatic scope: tests keep inline
copies that stay aligned by convention).

### Python prototype touched (three places)

- `core/aristotelian.py` — ArMythosRelation + ArAnagnorisis-
  Step + three optional ArMythos fields + four checker
  functions + extended `verify()` signature. Backward-compat
  test pins that pre-sketch-02 call sites see identical
  behavior.
- `encodings/oedipus_aristotelian.py` — AR_STEP_JOCASTA +
  `anagnorisis_chain=(AR_STEP_JOCASTA,)` +
  `peripeteia_anagnorisis_binding=BINDING_SEPARATED`.
- `encodings/rashomon_aristotelian.py` — AR_RASHOMON_CONTEST +
  `AR_RASHOMON_RELATIONS = (AR_RASHOMON_CONTEST,)`.
- `encodings/and_then_there_were_none.py` — substrate fill
  (14 entities + 15 events + 4 descriptions + 100 per-
  listener KnowledgeEffects at the gramophone event).
- `core/aristotelian_reader_model_client.py` — relations
  kwarg + ArMythosRelation prompt section + three sketch-02
  fields rendered on ArMythos. Demo migration for Rashomon.

Net: the "production-track streak" phrased in prior
sketches-of-play (zero `story_engine/` changes across N
commits) ends mid-sketch-10 — the Aristotelian-sketch-02
implementation and the ATTWN substrate fill and the
conformance module extraction all touch core code. The broader
PFS2 discipline (schemas-first; Python-as-conformance-check)
still holds: every Python change in sketch-10 is either
(a) an encoding content addition, (b) a dialect amendment
authored under the sketch-first pattern with implementation
following the design commit, or (c) infrastructure factoring
that changes no behavior and is pinned by the existing 755
baseline.

### Corpus validation outcomes

- **Substrate corpus (delta from sketch-09):**
  - ATTWN adds 14 entities, 15 events, 4 descriptions, 100
    KnowledgeEffects at one event. ATTWN has zero rules
    today (gramophone-accusation → past_killed link is
    authorial fact, not structural derivation).
- **Aristotelian dialect corpus (delta from sketch-09):**
  - AR_RASHOMON_CONTEST (ArMythosRelation, kind=contests,
    over six canonical-floor events).
  - AR_STEP_JOCASTA (ArAnagnorisisStep at E_jocasta_realizes,
    τ_s=9, precipitates_main=True).
  - Oedipus mythos gains anagnorisis_chain + binding=
    "separated".
- **Save-the-Cat dialect corpus (first landing):**
  - StcStory: 2 (Macbeth + Ackroyd — 1 rites-of-passage +
    1 whydunit).
  - StcBeat: 30 (15 canonical slots × 2 encodings; 41 total
    StrandAdvancements).
  - StcStrand: 4 (2 a-story + 2 b-story).
  - StcCharacter: 16 (8 per encoding; 23 role_labels
    including Sheppard's overlapping triple).
- **Lowering corpus (PFS9 landing):**
  - Lowering: 156 records across all encodings with lowering
    modules; 21 carry metadata (supersedes / superseded_by).
  - AnnotationReview: 0 (expected per PFS9 — review_states
    land from probe output, not encodings).
  - LoweringObservation: 0 (expected — clean corpus emits
    zero observations).
- **Verification corpus (PFS10 landing):** four record types
  validate clean; corpus shape matches PFS10 expectations.
- **Tier-2 audit outcomes:**
  - branch-label: 313 Event refs clean across 16 encodings.
  - Aristotelian event-ref: 132 refs (20 records × 2 paired
    encodings) clean.
  - Save-the-Cat intra-story: 132 refs (36 records × 2
    encodings) clean.
  - CrossDialectRef: 520 refs (512 clean + 8 dispositioned
    per §D1).
  - character_ref_id: 6 refs clean (oedipus 22-union,
    rashomon 15-union).
  - Total: 1103 references resolved across five audit kinds.
- **Full test suite: 792 passing** (+75 from the 717 sketch-
  09 baseline).

---

## Shift-point — three claims stack

### Cross-boundary schema layer begins

Sketch-09 introduced the dialect schema layer; sketch-10 adds
the **cross-boundary** layer above both substrate and dialect.
Concretely:

- **Two top-level role-named namespaces ship**
  (`schema/lowering/` structural; `schema/verification/`
  observational). PFS8-N1 commits the split: Lowering is
  authored coupling, verifier output is finding about the
  record set. Different consumers, different evolution
  cadence.
- **Seven records ship as first-wave cross-boundary schemas.**
  Three Lowering-family + four Verification-family. The
  Production C namespace map is complete in design (22 Python
  record types classified); shipments continue under PFS11
  (Aristotelian batch) and PFS12 (Save-the-Cat observation).
- **CrossDialectRef ships inline, in two places.** PFS9
  inlines it in Lowering's $defs; PFS10 re-inlines it in
  each of the four Verification records' $defs. PFS8-V
  guidance — "re-inline rather than cross-namespace $ref" —
  is validated on two consumers. `dialect` field stays open
  string (PFS9-X4 closes PFS8 OQ3): architecture-sketch-02 A6
  extensibility holds.
- **Two dialect reference topologies coexist.** PFS6-X1 tree-
  with-inline-$ref (Aristotelian mythos → phase / character).
  PFS7-X1 flat-with-id-refs (Save-the-Cat story → beat_ids /
  strand_ids / character_ids arrays). The registry pattern
  is forgiving across both — Save-the-Cat's registration is
  present-but-unused (no outbound $ref), Aristotelian's is
  load-bearing.

**What's still under-specified at the cross-boundary layer.**
Aristotelian-cross-boundary records (ArObservation,
ArAnnotationReview, ArObservationCommentary, DialectReading
— four records, PFS11 candidate) and Save-the-Cat observation
(StcObservation, PFS12 candidate). Dramatic cross-boundary
records gated on dramatic-sketch-02 per PFS6 OQ2.

### Tier-2 validation layer operational

Sketch-09's schema layer was a Tier-1-only discipline (shape-
as-JSON-Schema files). Sketch-10 adds Tier-2 (resolution-as-
Python-audit-code):

- **Five audit functions, 1103 references, one disposition.**
  Each of five banked OQs from the PFS series closes on
  implementation (not on sketch): PFS5/OQ3 (branch-label
  audit), PFS6/OQ3 (Aristotelian event-id audit), PFS6/OQ4
  (character_ref_id multi-dialect fallback), PFS7/OQ4
  (Save-the-Cat intra-story), PFS10/OQ1 (CrossDialectRef
  resolution across namespaces). One disposition (§D1)
  surfaces on first contact with the corpus and names a real
  design convention (`Story_goal` / `Story_consequence` as
  axis-label tokens, not record ids) that had never been
  explicit.
- **Disposition protocol is parallel to PFS conformance-
  dispositions.** Known-accepted unresolved references get
  declared at the sketch layer. Explicit ban on "make the
  test pass by listing the finding" — drift isn't silently
  absorbed. §D1 stays scope-limited to two specific pairs;
  any typo of the axis labels still surfaces as a finding.
- **Audit primitives factor out.** `conformance.py` extracts
  `AuditReport` + five `audit_*()` functions into a module
  with a narrow interface — callable by any future walker /
  pre-commit hook / CI wrapper without reading test
  scaffolding. The duplication of discovery helpers between
  test file and module is intentional pragmatic scope.

**What's banked for second-round Tier-2 work.** Substrate-
internal entity-id audits (sketch-01 OQ5, low urgency —
strong construction-time invariants catch most cases).
Type-mismatch detection (RI4 banked vocabulary — reserved
but unused). Dialect-catalog references (stc_genre_id →
StcGenre; metadata-key references — RI14 banks for third-arc
if forcing functions argue).

### Aristotelian dialect amendment via probe closure

Sketch-10 introduces the first **dialect-amendment sketch**
(aristotelian-sketch-02) — opened by a probe arc, closed by a
re-probe. The pattern that emerged:

- **Amendment-only, not core-record modification.** A1–A9
  from sketch-01 stay unchanged. A10–A12 add new records /
  fields / checks. No migration of existing encoding data;
  both Oedipus + Rashomon encodings continue to verify clean
  under pre-sketch-02 paths (backward-compat test pins this).
- **Closure hypothesis verified by re-probe.** The three
  well-forced proposals close — the v2 probe uses the
  authored records structurally in its reading ("the
  ArMythosRelation 'contests' kind allowed the encoding to
  express inter-mythos friction without leaving the
  dialect"; "the sketch-02 extensions … cleanly captured the
  two-beat reversal-recognition structure"). The two held-out
  proposals behave as sketch-02 anticipated: ArFrameMythos
  persists as limit (correct per substrate-blocked deferral);
  ArAnagnorisisLevel re-surfaces under a new name
  (ArAudienceAnagnorisis — correct per rejection stance).
- **Sketch-02 buys read_on_terms upgrade + drift
  elimination.** Rashomon `read_on_terms` upgrades from
  `partial` (v1) to `yes` (v2); `drift_flagged` shrinks from
  5 items to 0. Closing the three well-forced proposals
  cleared the principal strain the dialect surface carried.
- **Second-order forcing functions surface immediately.**
  Four banked OQs (OQ-AP1 ArPathos + catharsis grounding;
  OQ-AP2 ArCanonicalFloor; OQ-AP3 ArProseOnlyCause; OQ-AP4
  peripeteia-in-beginning soft check) — each finer-grained
  than v1's proposals and each with a named forcing function.
  Sketch-03 is the home if they force open.

**What's still under-specified at the dialect-amendment
layer.** Aristotelian A10–A12 do not yet have schema-layer
shape (AA11 defers to a future PFS arc). Save-the-Cat has no
amendment sketch yet (sketches-01/-02 remain first-pass
field-detailed; no probe arc has run on Save-the-Cat).
Dramatic has dramatic-sketch-01 but no amendment sketch and
no probe.

---

## What the fifteen sketch-10 commits revealed

### Production C: the namespace decision compounds

PFS8 committed two top-level role-named namespaces
(`schema/lowering/` + `schema/verification/`). The decision
carried real weight: it distinguishes **structural coupling**
(Lowering encodes authored binding between an upper- and
lower-layer record) from **observational finding** (Verification-
family records encode what a verifier saw about the record
set). Those are different functional roles per architecture-
sketch-02 A7/A8; different consumer sets; different evolution
cadence. PFS8-N1's principle — "what a dialect produces OR
what the dialect alone consumes lives under `schema/<dialect>/`;
what is shared across dialects lives in a top-level role-named
namespace" — applies cleanly to the 22 known Python record
types.

The namespace decision is **one-shot** once shipped (per
sketch-09's schema-namespacing finding). PFS11 (Aristotelian
cross-boundary batch) and PFS12 (Save-the-Cat observation)
will follow the classification; their records live under
`schema/aristotelian/` and `schema/save_the_cat/` per PFS8-N2,
not under the two top-level namespaces.

### Slim production sketches keep scaling

PFS7 shipped four Save-the-Cat records in 762 lines — roughly
linear with PFS6 (three records at 540 lines). PFS9 shipped
three records in 612 lines; PFS10 shipped four records plus
the cross-boundary-tier CrossDialectRef re-inline at ~750
lines. The per-record cost stays at ~150 lines when the field-
level design sketch precedes. PFS2's "schemas depend on
design sketches, not on Python" discipline pays out at each
slim production sketch: zero design derivation, zero ambiguity
at schema-authoring time.

### Two dialect topologies, same registry

Aristotelian (PFS6-X1) and Save-the-Cat (PFS7-X1) encode
their intra-dialect references differently — tree-with-inline-
$ref vs. flat-with-id-refs. Both are admitted by the same
`jsonschema.referencing.Registry` pattern; Save-the-Cat's
registration is present-but-unused (no outbound $ref), but
the call site doesn't branch. Future dialect-schema arcs
choose the topology matching their Python; the registry
infrastructure is unchanged.

### The Tier-2 audit layer adds without new primitives

RI5's commitment — "the audit does NOT replace per-dialect
self-verifiers; it ADDS a second validation surface that
runs at conformance-test time unconditionally" — produces a
load-bearing architectural distinction on the ground.
Per-dialect checks (aristotelian.verify A7 check 4,
save_the_cat.verify S13 check 1) retain their runtime-verifier
role; the audits run always, surface findings via the same
print-and-assert pattern as shape tests, and don't require
per-dialect verifier orchestration. Duplication is the point,
not a smell.

§D1's disposition finding is the sharper architectural
payoff. A real design convention — axis-label tokens in
Dramatica-complete verifications — had never been made
explicit. The audit surfaced it on first contact with the
corpus. Without the audit, the convention would have stayed
implicit indefinitely. Tier-2 audits are not just validators;
they're convention-discovery tools.

### Factor-out discipline applies to tests too

The `conformance.py` extraction is the first infrastructure
factoring the project has landed. Five audits had grown into
~800 lines inside one test file, invisible to any caller
other than the test. The extraction produces a narrow
interface (`AuditReport` + `audit_*()` callables) suitable
for downstream tooling (pre-commit hook, CI wrapper, walker
script). Same "concrete-before-abstract" principle RI2
applied to audit functions earlier: factor when three or four
instances pressure duplication, not before.

### Probe-closure loop validates dialect-amendment shape

Aristotelian-sketch-02 + aristotelian-probe-sketch-02
together form a **probe → amendment → re-probe** triad. Each
step is small; the loop as a whole is a strong convergence
test. The probe's v2 reading CITES the sketch-02 records
structurally — not just "tolerates them" but "uses them in
its analysis." That's the strongest closure signal a probe
can produce. The loop generalizes: Save-the-Cat / Dramatic
amendment sketches (if forcing functions surface) would
follow the same shape.

**The rejection stance is load-bearing.** Sketch-02 rejected
ArAnagnorisisLevel on A4/A8 scope grounds; v2 re-surfaces the
pressure under a new name (ArAudienceAnagnorisis). The
correct response is to keep the rejection — the probe will
keep pressuring what the dialect genuinely doesn't cover; a
sketch-01 amendment (not sketch-02-style extension) is the
only opening path. This distinguishes "feature banked for
forcing function" from "scope stance against future arcs."
Both are valid dispositions; they carry different reversal
rules.

### ATTWN: substrate-only landings are first-class

ATTWN ships substrate-only: 14 entities + 15 events + 4
descriptions + 100 per-listener KnowledgeEffects. Dramatic /
Dramatica-complete / Lowering / Verification stay skeleton
(`THROUGHLINE_OWNER_NONE` placeholders, no beats, no
lowerings). This is a new arc shape in the corpus — **content
fill landed incrementally per layer**, not bundled into a
single "encoding complete" commit. The pattern buys two
things: (a) substrate-layer probe pressure can run
immediately without waiting on dialect fills; (b) dialect
fills are delayed until their layer-specific questions (MC/IC
decision, Save-the-Cat beat placement) get proper attention.
The six-encoding corpus now has two substrate-only members
(ATTWN, the skeleton chinatown); four with full
substrate+dramatic+dramatica-complete fills (oedipus,
rashomon, macbeth, ackroyd); two with Aristotelian fills
(oedipus, rashomon); two with Save-the-Cat fills (macbeth,
ackroyd).

---

## What's next (research AND production)

### Research track

1. **Third Aristotelian encoding (Macbeth or Ackroyd).**
   Largest single forcing-function payoff on the research
   track. Would pressure A10 (does `contests` cover anything
   besides Rashomon?), A11 (does anagnorisis_chain generalize
   past Oedipus?), A12 (peripeteia-in-beginning counter-
   example for OQ-AP4?), OQ-AP1 (disputed pathos placement
   forces ArPathos?). Corpus-infrastructure ready — both
   works have substrate fills; Aristotelian encoding is
   pure authorial content.
2. **ATTWN dramatic + dramatica-complete fills.** The MC/IC
   decision (Vera-as-MC conventional vs. Wargrave-as-MC
   subversive) is the first substantive question. Once
   landed, ATTWN becomes the fifth full-stack encoding and
   unblocks (a) probe runs on MN2 concealment-asymmetry +
   LT8/LT9 discrete-elimination Timelock, (b) Save-the-Cat
   fill (beat placement across the ten deaths), (c)
   Aristotelian fill (if genre-as-tragedy reading lands).
3. **Second Rashomon-derivative encoding.** Would force
   OQ-AP2 (ArCanonicalFloor typing). Unusual — requires
   identifying a second legal-testimony / multi-witness work
   in the target corpus. Lower priority.
4. **Probe-surfaced encoding cleanups** (sketch-05 → 06 →
   07 → 08 → 09 → 10 holdover, still unopened). 2 Oedipus
   prose fixes + 5 Rashomon phase-annotation cleanups.
   Smallest concrete research item.
5. **Close a banked scheduling-act-family seed** (OQ2-
   reshaped wife prose-carried drivers; OQ1-reshaped
   woodcutter cross-branch signature; bandit-refinement).
6. **Fourth Aristotelian encoding.** Only if a third lands
   clean and still leaves OQ-AP1..OQ-AP4 banked.

### Production track

Re-ordered by sketch-10's completions (items A-Save-the-Cat,
C-Lowering, C-Verification, and Tier-2 first arc closed):

A. **PFS11 — Aristotelian cross-boundary batch.** Four
   records (ArObservation + ArAnnotationReview +
   ArObservationCommentary + DialectReading) under
   `schema/aristotelian/`. Natural bundling per PFS8 §Per-
   record arc plan item 3. Design derivation minimal —
   aristotelian-probe-sketch-01/-02 field shapes already
   committed.
B. **PFS12 — Save-the-Cat observation.** One record
   (StcObservation) under `schema/save_the_cat/`. Smallest
   cross-boundary per-record arc; slim production sketch
   expected.
C. **PFS13 — Dramatic dialect schemas.** Gated on dramatic-
   sketch-02 per PFS6 OQ2 (six design forcing functions
   banked in dramatica-template-sketch-01). A dramatic-
   sketch-02 design-first arc is the prerequisite.
D. **PFS14 — Dramatica-complete dialect schemas.** Gated on
   PFS13 (Dramatic-schema readiness per dramatica-template-
   sketch-01 Template-extension pattern).
E. **Aristotelian A10–A12 schema landing.** Deferred by
   aristotelian-sketch-02 AA11; candidate for a future PFS
   extending `schema/aristotelian/mythos.json` with the new
   optional fields + shipping new
   `schema/aristotelian/mythos_relation.json` +
   `anagnorisis_step.json` schema files.
F. **substrate-world-fold-sketch-01** (parallel to the
   knowledge-fold sketch but for W1). Only if a forcing
   function surfaces — current corpus has no contradictory
   world-fact patterns that the later-wins default doesn't
   handle.
G. **Reader-model-client base extraction.** Three clients
   (basic / dramatic / aristotelian) now share large
   duplicate surface (system-prompt structure; build-user-
   prompt shape; dataclass-to-dict renderers; Pydantic
   output schema; translate-output-to-records). Candidate
   for a shared base in `core/reader_model_client_base.py`
   following the factor-out pattern the conformance module
   set. Factoring target, not behavior change — zero test
   deltas expected.
H. **Markdown-fenced author parser** (roadmap item 1).
   First consumer of the schemas outside the conformance
   test. Now consumes five namespaces (substrate +
   aristotelian + save_the_cat + lowering + verification)
   covering 13 record types.
I. **Prose export round-trip starter** (roadmap item 3).
J. **Goodreads import prototype** (roadmap item 2).
K. **Port work** (roadmap item 4). Substrate-layer fully
   unblocked (structural + behavioral). Dialect-layer
   unblocked for Aristotelian-core + Save-the-Cat-core.
   Dialect-amendment (Aristotelian A10–A12) still per-
   dialect-Python. Cross-boundary partially unblocked
   (Lowering + Verification families spec'd;
   Aristotelian-cross-boundary + Save-the-Cat-observation
   pending PFS11/12).

### Recommendation

Sketch-10's cadence mixed design-heavy + implementation arcs
across fifteen commits. Three candidates fit the small-arc
shape for sketch-11:

- **Research track #1** (third Aristotelian encoding —
  Macbeth or Ackroyd). Largest single forcing-function
  payoff. Pressures A10 / A11 / A12 + potentially OQ-AP1 /
  OQ-AP4. Substrate + save-the-cat encodings already in
  place; this is pure dialect-authorial content.
- **Production track A** (PFS11 Aristotelian cross-boundary
  batch). Extends PFS6 / PFS7 precedent directly; validates
  the PFS8-N2 classification (dialect-internal cross-boundary
  records live under `schema/<dialect>/`). Slim production
  sketch expected.
- **Production track G** (reader-model-client base
  extraction). Pure infrastructure factoring — three clients'
  duplicate surface pressures a shared base now that the
  pattern is stable across three invocations. Zero
  behavior change; zero test deltas expected. Test-suite-
  invariant scaffolding work.

Alternative: **Research track #2** (ATTWN dramatic fill) —
would make ATTWN the fifth full-stack encoding and unblock
three downstream probe + dialect fills. Larger arc; likely
needs more than one commit.

---

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketches-04 through -09. Validated
again across the 15 commits:

- **Orientation before commitment.** PFS7 began with a read
  of save-the-cat-sketch-01 + -02 (field-level shapes
  pre-committed) + the existing dialect schema
  (`schema/aristotelian/*`) as template. PFS8 began with a
  sweep of every Python record type not yet schema'd
  (22 types classified). RI1 began with a read of the five
  banked OQs in PFS5/6/7/10 that had forked the same
  question. Aristotelian-sketch-02 began with a careful
  read of probe-sketch-01's relations_wanted + scope_limits
  and the dispositional decision tree (close / defer /
  reject).
- **Sketches before implementation.** PFS7 / 8 / 9 / 10,
  RI1 / RI2, aristotelian-sketch-02, and aristotelian-probe-
  sketch-02 each shipped design commit before
  implementation commit (except PFS7 and PFS8 which were
  design-only / impl-in-same-commit; PFS8 was design-only).
- **First-principles vs. retroactive recognition.** RI1 / RI2
  were partially retroactive (the five forked OQs named the
  same gap; sketch-01 committed the shared audit vocabulary).
  Aristotelian-sketch-02 was partially retroactive (the
  probe surfaced the forcing functions; sketch-02
  recognized which were well-forced enough to close).
  PFS7 / 9 / 10 were primarily format-rendering (retroactive
  on lowering-record-sketch-01 / save-the-cat-sketch-01-02
  / verification-sketch-01 pre-committed shapes).
- **Banking with forcing-function criteria.** Every sketch-10
  OQ carries a named forcing function, not "TBD." PFS7: 5
  OQs. PFS8: 5 OQs. PFS9: 5 OQs. PFS10: 5 OQs. RI1: 5 OQs.
  RI2: 4 OQs (closes 2). Aristotelian-sketch-02: 6 OQs.
  Aristotelian-probe-sketch-02: 4 new (OQ-AP1..OQ-AP4). The
  discipline now covers 70+ banked OQs across the design
  corpus.
- **State-of-play at milestone boundaries.** This doc.
  Milestone: cross-boundary schema layer begins + Tier-2
  audit layer closes first-round OQs + Aristotelian dialect
  earns amendment sketch.
- **Commit messages as cross-session artifacts.** All fifteen
  sketch-10 commits carry 60–170 line bodies; a cold-start
  Claude reading `git log --oneline -20` + `git show` on
  each can reconstruct sketch-10's arcs fully from commit
  bodies.
- **Probe JSONs are disposable context.** Probe-sketch-01
  reader-model output JSONs (v1) and probe-sketch-02 v2
  JSONs are large (151 + 399 + 151 + 399 lines). The
  corresponding probe sketches read + synthesize them; the
  sketches carry the durable content. Future sessions can
  read the sketches without re-reading the JSONs unless
  pressure-testing the closure claim.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic (now
   includes PFS7/8/9/10, RI01/02, aristotelian-sketch-02,
   aristotelian-probe-sketch-02).
2. This doc (`design/state-of-play-10.md`) — current corpus,
   shift-point state, research + production tracks.
3. `schema/README.md` — the production layer's discipline,
   now structured in three tiers: substrate (six records),
   dialect (Aristotelian + Save-the-Cat, seven core), cross-
   boundary (Lowering three + Verification four).
4. `git log --oneline -20` — the fifteen sketch-10 commits +
   sketch-09's three carry dense readable bodies.
5. `design/production-format-sketch-08.md` — Production C-
   opener. Load-bearing for any future cross-boundary schema
   work; commits the namespace classification for 22 Python
   record types.
6. `design/referential-integrity-sketch-01.md` + `-02.md` —
   the Tier-2 audit layer's design commitments + §D1
   disposition. Load-bearing for any future audit kind.
7. `design/aristotelian-sketch-02.md` +
   `aristotelian-probe-sketch-02.md` — the dialect-
   amendment + probe-closure loop pattern. Template for
   future Save-the-Cat / Dramatic amendment sketches.
8. `prototype/story_engine/core/conformance.py` — the audit
   primitives module. Read the module docstring + the five
   `audit_*()` signatures; the rest is helper detail.
9. The two v2 probe JSONs (`reader_model_oedipus_
   aristotelian_output_v2.json`,
   `reader_model_rashomon_aristotelian_output_v2.json`) are
   only needed if pressure-testing the sketch-02 closure
   claim. The probe sketches carry the durable findings.
