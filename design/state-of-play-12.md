# State of play — sketch 12

**Status:** active
**Date:** 2026-04-21
**Supersedes:** [state-of-play-11](state-of-play-11.md)

Cold-start orientation doc, rewritten (not amended) at the
milestone where the **fourth Aristotelian encoding lands via a
multi-session research arc**, the **Aristotelian dialect reaches
sketch-03** closing two probe-surfaced forcing functions and
retiring a third, and the **cross-boundary schema layer completes
its three remaining per-record arcs**.

**Twenty-one commits since state-of-play-11.** Largest
inter-sketch delta the series has had — by volume, by test
delta, and by depth of the research+production coupling. The
Hamlet multi-session arc drove most of it; two research sessions
turned into one research→production cycle (probe → sketch-03 →
probe-sketch-04 → Session 6 verification) covering a week of
on-one-day-cadence commits (2026-04-19 through 2026-04-21).

Grouped by arc:

### Arc 1 — Aristotelian dialect reaches sketch-03 (11 commits)

- `e22285b` / `8ce2a24` — production-format-sketch-11
  (Aristotelian cross-boundary batch). Four records ship under
  `schema/aristotelian/`: observation, annotation_review,
  observation_commentary, dialect_reading. Closes sketch-10
  production item A. 807 → 819.
- `5c7f43d` — macbeth Aristotelian probe demo. Third Aristotelian
  reader-model probe demo module lands.
- `2f9a0f8` — aristotelian-probe-sketch-03 (Macbeth first-probe).
  sketch-02 closure generalizes to a third encoding;
  surfaces OQ-AP1 non-force (scattered pathos absorbed),
  OQ-AP5 (supernatural agency, banked), OQ-AP6 (intra-mythos
  parallel-character-arc, banked).
- `bfcfd5b` — macbeth encoding cleanup. Closes the "first clause"
  prose error probe-sketch-03 surfaced. 822 tests.
- `edb25cb` / `9423f59` / `b9aa560` / `ff77592` / `6e5e41c`
  — Hamlet multi-session arc Sessions 1–5 (substrate skeleton
  → Aristotelian overlay → substrate completion → encoding-
  specific tests → first probe run). Session 5 produces the
  forcing-function payload: OQ-AP6 direct hit, OQ-AP10
  (NEW — protagonist-scope chain extension), OQ-AP9
  (audience-level dramatic irony, fourth site), OQ-AP1 polis
  catharsis (third independent signal), OQ-AP5 fate-agent
  (second-negative confirmation).
- `6918a32` / `7a86e1e` / `ac926e2` — aristotelian-sketch-03
  (A13 ArCharacterArcRelation + A14 step_kind +
  anagnorisis_character_ref_id + A7.10 + A7.11). Design-first
  → demo-relabel (false-positive discipline) → implementation
  + Hamlet migration + OQ-AP5 formal retirement. 822 → 844.
- `4c978c4` / `8b52c98` / `4b30291` — aristotelian-probe-sketch-04
  (sketch-03 prompt-rendering extensions + Session 6 re-probe).
  Design-first → APA4-1..APA4-6 client extensions → Session 6
  closure-verification. 844 → 879.

### Arc 2 — Cross-boundary schema layer completes three per-record arcs (3 commits)

- `8ce2a24` — PFS11 Aristotelian four-record batch (above;
  counted in Arc 1 but also a Production C arc).
- `70738ee` — production-format-sketch-12 (Save-the-Cat
  observation). One record (StcObservation) under
  `schema/save_the_cat/`. Smallest per-record arc in the
  Production C series. 819 → 822.
- `1f869dd` — production-format-sketch-13 (Aristotelian
  sketch-02 A10–A12 schema landing). Closes aristotelian-
  sketch-02 AA11. First Production C arc to amend an
  existing dialect-core schema (`schema/aristotelian/mythos.json`
  gains `anagnorisis_chain`, `peripeteia_anagnorisis_binding`,
  `peripeteia_anagnorisis_adjacency_bound`) plus two new
  schema files (`mythos_relation.json`,
  `anagnorisis_step.json`). 822 → 828.

### Arc 3 — Verifier refactor-out track drains Codex REVIEW.md findings (2 commits + 1 README update)

- `09c65f5` — README review findings refresh. Codex REVIEW.md
  updated with current-state callouts.
- `5bec864` — verification: extract template orchestration.
  Shared template-selection + header-rendering logic lifted
  out of the five dramatica-complete verifier modules.
- `b0b0eba` — verification: extract `fabula_end_τ_s` +
  `events_lowered_from_throughline`. Two remaining per-encoding
  helpers factored to `verifier_helpers.py`.

## Headline — three load-bearing claims

### 1. The Aristotelian dialect ran a full research→production→verification loop driven by Hamlet, and it held

Aristotelian-sketch-02 (state-of-play-11 milestone) committed to
closing three well-forced proposals (ArMythosRelation,
ArAnagnorisisChain, ArPeripeteiaAnagnorisisBinding) + absorbing
Macbeth as a third encoding without amendment pressure. The
Macbeth probe (sketch-03, commit `2f9a0f8`) verified that
closure on the third encoding. Hamlet then forced two NEW
extensions:

- **OQ-AP6** (intra-mythos parallel tragic-heroes) —
  Hamlet authors three `is_tragic_hero=True` characters;
  the probe's `relations_wanted` explicitly proposes
  `ArMythosRelation kind='parallel'`, and `scope_limits_
  observed` flags the three-way-hero ranking gap. Two
  independent probe surfaces of the same gap. Forcing.

- **OQ-AP10** (protagonist-scope anagnorisis chain extension)
  — Hamlet's three-stage epistemic progression (Ghost
  commission τ_s=1 → Mousetrap verification τ_s=6 → Laertes
  reveal τ_s=17) pressured the chain for **intra-character**
  staggering, which A11's shape mechanically admitted but
  didn't structurally distinguish from **parallel-character**
  recognition (Lady Macbeth). Forcing.

Aristotelian-sketch-03 closed both (A13 ArCharacterArcRelation;
A14 step_kind + anagnorisis_character_ref_id + A7.10/A7.11).
Hamlet migrated to the new surface: two pairwise arc relations
(mirror Hamlet-Laertes, foil Hamlet-Claudius), three-step
chain (2 staging × Hamlet + 1 parallel × Claudius). OQ-AP5
(fate-agent) formally retired on two-negative-probe grounds
(Macbeth Witches + Hamlet Ghost both stayed below dialect).

**Aristotelian-probe-sketch-04 caught the LLM-prompt-rendering
up to sketch-03's new surface** (step_kind inline; new arc-
relations section; new kwarg; sketch-03 paragraph in
SYSTEM_PROMPT; reviewable-prose surface grows from 3 record
kinds to 5 — +16 tests, +5 reviewable-field types). Session 6
(commit `4b30291`) re-probed Hamlet under the extended client:
the sketch-03 closures are not just accepted but **structurally
load-bearing** in the probe's reasoning. The probe used the
step_kind distinction to catch an encoding error (GHOST_CLAIM
annotation miscount: "first of three staging" when only two
are staging-kind), cited the mirror/foil relations structurally
in its annotation reviews, and independently identified two new
forcing functions (OQ-AP14 instrumental-kind; OQ-AP15 absent-
character catharsis) neither anticipated by sketch-03 nor
sketch-04.

Hamlet is the corpus's first multi-session research arc
(Sessions 1–6 spanning substrate skeleton → full probe-
verification). The session-numbering convention (introduced by
Hamlet) scales — each session's commit body cites its prior
sessions and its forward candidates. Future multi-session arcs
(Ackroyd / Lear / ATTWN) inherit the pattern.

### 2. Cross-boundary schema layer completes three per-record arcs

Production C (sketch-06's decision to ship per-record cross-
boundary schemas under `schema/<dialect>/` namespaces) reaches
a completion milestone:

- **PFS11** (Aristotelian four-record batch) — observation,
  annotation_review, observation_commentary, dialect_reading.
  Closes sketch-10 production item A.
- **PFS12** (Save-the-Cat observation) — single-record arc,
  the smallest shape under Production C.
- **PFS13** (Aristotelian A10–A12 schema landing) — first
  Production C arc to amend an existing dialect-core schema
  (mythos.json gains three optional properties), plus two new
  single-record schemas (mythos_relation.json,
  anagnorisis_step.json). Closes aristotelian-sketch-02 AA11.

**Post-sketch-12 schema status.** Five namespaces cover 17
record types:
- `substrate`: 5 (branch, description, entity, event, held, prop)
- `aristotelian`: 9 (mythos, phase, character, observation,
  annotation_review, observation_commentary, dialect_reading,
  mythos_relation, anagnorisis_step)
- `save_the_cat`: 5 (story, character, beat, strand, observation)
- `lowering`: 3 (lowering, annotation_review,
  lowering_observation)
- `verification`: 4 (structural_advisory, verifier_commentary,
  verification_review, verification_answer_proposal)

Remaining Production C arcs:
- **PFS14** (Aristotelian sketch-03 schema landing — deferred
  by sketch-03's AA15). Single-schema-amendment +
  two-optional-field amendments to existing schemas. Follows
  PFS13's pattern.
- **PFS15** (Dramatic dialect schemas). Gated on
  dramatic-sketch-02 design-first arc.
- **PFS16** (Dramatica-complete dialect schemas). Gated on
  PFS15.

### 3. Verifier refactor-out track drains Codex REVIEW.md findings

Two commits (`5bec864`, `b0b0eba`) extract three previously-
per-encoding helpers into `verifier_helpers.py`:

- `extract_template_orchestration`: template-selection and
  header-rendering shared across the five dramatica-complete
  verifier modules.
- `extract_fabula_end_τ_s`: per-encoding fabula-end computation.
- `extract_events_lowered_from_throughline`: per-encoding
  lowering-walk.

All five dramatica-complete demos produce identical final
output (byte-diff verified). Rashomon's verifier unchanged
(didn't use these helpers). Three previously-orphaned tests
register in `TESTS`; `test_verification.py` grows 193 → 199.

The refactor track continues sketch-11's factor-out discipline
(factor when three instances pressure duplication; surface a
narrow callable; duplicate what is intentionally-not-factored).
The `verifier_helpers.py` module now carries six extracted
primitives (sketch-11's `_prose_carried_lowerings` +
`PROSE_CARRIED_MARKER` + sketch-12's three).

Rewrite this sketch (don't amend — write sketch-13) at the
next milestone.

---

## What is built — delta from sketch-11

### The corpus (fourth Aristotelian encoding + third multi-session arc)

**Hamlet Aristotelian** — the dialect's fourth encoding, the
corpus's first multi-session research arc, and the first
encoding to force a dialect amendment (A13 + A14).

- `prototype/story_engine/encodings/hamlet.py` (substrate,
  1097+727 lines across sessions 1 + 3). 32 substrate events,
  20 entities, full τ_s ordering from Claudius-brother-of-king
  (τ_s=-100) through Hamlet's death (τ_s=18).
- `prototype/story_engine/encodings/hamlet_aristotelian.py`
  (overlay, 574 lines sessions 2 + 574+165 post-sketch-03).
  AR_HAMLET_MYTHOS: complex plot, 32 central events, three
  phases (13/11/8), complication=E_mousetrap_performance,
  denouement=E_duel_plotted, peripeteia=E_hamlet_kills_polonius
  (τ_s=8), anagnorisis=E_laertes_reveals_plot (τ_s=17),
  BINDING_SEPARATED distance 9 (widest in corpus),
  anagnorisis_character_ref_id="ar_hamlet" (first in corpus).
  Three ArCharacter records (HAMLET, CLAUDIUS, LAERTES — all
  is_tragic_hero=True; first ≥3 in corpus).
  AR_HAMLET_CHARACTER_ARC_RELATIONS: two records (mirror
  Hamlet-Laertes, foil Hamlet-Claudius; first A13 corpus use).
  Anagnorisis chain: three steps (GHOST_CLAIM staging τ_s=1,
  MOUSETRAP staging τ_s=6, CLAUDIUS_PRAYS parallel τ_s=7;
  first A14 step_kind corpus use, all three step_kinds
  exercised across the corpus when Oedipus/Macbeth's derived
  kinds are counted).
- `prototype/tests/test_aristotelian.py`: +22 tests covering
  sketch-03 A7.10/A7.11 + Hamlet encoding verifies clean under
  A13+A14+A7.10+A7.11.
- `prototype/reader_model_hamlet_aristotelian_output.json`
  (Session 5, pre-sketch-03) +
  `reader_model_hamlet_aristotelian_output_v2.json` (Session 6,
  post-sketch-03) — two JSON artifacts preserved for diff.

**Aristotelian dialect corpus (post-sketch-12)**: four
encodings — oedipus, rashomon, macbeth, hamlet.
- Binding coverage: SEPARATED (oedipus, hamlet), COINCIDENT
  (macbeth), ADJACENT uncovered (no forcing function banked).
- Anagnorisis chain polarities: precipitating (Oedipus
  Jocasta), parallel (Macbeth Lady Macbeth + Hamlet Claudius-
  prays), **staging** (Hamlet GHOST_CLAIM + MOUSETRAP — new
  under A14, no pre-sketch-03 corpus analog).
- Character-arc relations: kinds mirror + foil exercised
  (Hamlet); parallel not exercised (canonical-plus-open;
  'doubled-fall'/'shadow' banked in sketch-03 OQ8;
  'instrumental'/'manipulation' banked as Session-6-surfaced
  OQ-AP14).

### The dialect layer (aristotelian-sketch-03)

Three new commitments plus two new self-verifier checks:

- **A13 `ArCharacterArcRelation`** — intra-mythos structural
  relation between ≥2 ArCharacter records within one ArMythos.
  Canonical kinds `parallel | mirror | foil`. Distinguished
  from sketch-02's A10 (inter-mythos). N-ary via
  `character_ref_ids` tuple.
- **A14 `step_kind` field** on `ArAnagnorisisStep` —
  `parallel | precipitating | staging`. Soft-deprecates A11's
  `precipitates_main` (kept as verifier-cross-checked
  redundancy). `anagnorisis_character_ref_id` added to
  `ArMythos` to let staging steps verify against the main's
  subject.
- **A7.10** — ArCharacterArcRelation structural integrity
  (kind canonicity, refs cardinality, mythos/character
  resolution, event-ref substrate resolution).
- **A7.11** — Step_kind consistency (six invariants, including
  staging_requires_main_character, staging_ordering,
  precipitates_main cross-check).

Extension-only: A1–A12 semantics unchanged. Pre-sketch-03
encodings (Oedipus / Rashomon / Macbeth) verify identically
under A14's back-compat derivation (empty step_kind →
parallel/precipitating by precipitates_main + same-character
check).

### The probe client (probe-sketch-04 APA4-1..APA4-6)

Catches the LLM-prompt-rendering up to sketch-03:

- `_ar_anagnorisis_step_to_dict` renders `step_kind`.
- `_ar_mythos_to_dict` renders `anagnorisis_character_ref_id`.
- New `_ar_character_arc_relation_to_dict` +
  `_build_character_arc_relations_section` rendering intra-
  mythos arc relations in a dedicated section (parallel shape
  to the sketch-02 ArMythosRelation section).
- `character_arc_relations: tuple = ()` kwarg threaded through
  `build_user_prompt` + `invoke_aristotelian_reader_model` +
  `translate_raw_output` + `_eligible_targets` +
  `_records_by_kind_id`.
- Pydantic `ReviewTargetKind` Literal grows: 5 kinds
  (`ArMythos`, `ArPhase`, `ArCharacter` pre-sketch-04 + new
  `ArAnagnorisisStep`, `ArCharacterArcRelation`). The
  reviewable-prose surface expands: chain-step `annotation`
  and arc-relation `annotation` become reviewable fields.
- SYSTEM_PROMPT gains a sketch-03 paragraph naming the three
  new extensions and the reviewable-prose expansion.
- Default-empty kwarg preserves pre-sketch-03 call sites;
  Oedipus / Rashomon / Macbeth demos' prompts stay
  byte-identical through the new code path (verified by
  test).

Reviewable prose on Hamlet grows from 7 fields (1
action_summary + 3 phase annotations + 3 hamartia_texts) to
12 (+3 chain-step annotations — all three chain members carry
non-empty prose + 2 arc-relation annotations).

### The schema layer (PFS11 + PFS12 + PFS13)

**PFS11 — Aristotelian cross-boundary batch (four schemas).**

- `schema/aristotelian/observation.json`
- `schema/aristotelian/annotation_review.json`
- `schema/aristotelian/observation_commentary.json`
- `schema/aristotelian/dialect_reading.json`

Four records under the dialect's own namespace per PFS8-N2's
classification (dialect-internal records live under
`schema/<dialect>/`, not under a top-level role-named
namespace). Field shapes pre-committed in aristotelian-
probe-sketch-01 / -02. The aristotelian namespace reaches 7
records post-PFS11 (adds mythos_relation + anagnorisis_step
under PFS13 to reach 9).

**PFS12 — Save-the-Cat observation (one schema).**

- `schema/save_the_cat/observation.json`

Smallest per-record arc in Production C. The save_the_cat
namespace reaches 5 records (pre-existing beat, character,
story, strand + new observation).

**PFS13 — Aristotelian A10–A12 schema landing.**

- `schema/aristotelian/mythos_relation.json` (new)
- `schema/aristotelian/anagnorisis_step.json` (new)
- `schema/aristotelian/mythos.json` (amendment: three new
  optional properties — `anagnorisis_chain` array of $ref to
  anagnorisis_step.json; `peripeteia_anagnorisis_binding`
  closed enum; `peripeteia_anagnorisis_adjacency_bound`
  integer).

First Production C arc to amend an existing dialect-core
schema. Sets the pattern for future sketch-03 schema landing
(PFS14 gated on this work).

Conformance-test extensions: two new schema loaders, registry
entries, dump helpers (`_dump_ar_mythos_relation`,
`_dump_ar_anagnorisis_step`), `_dump_armythos` extended for
three new fields, `_discover_encoding_aristotelian_records`
extended to collect steps transitively via
`mythos.anagnorisis_chain`,
`_discover_encoding_aristotelian_relations` added for
module-level `AR_*_RELATIONS` walk.

### The verifier layer (three extracted helpers)

- `verifier_helpers.py` gains:
  - `extract_template_orchestration` (template-selection +
    header-rendering).
  - `extract_fabula_end_τ_s` (explicit fabula parameter).
  - `extract_events_lowered_from_throughline` (explicit
    lowerings parameter).

Five dramatica-complete verifier modules reduce duplication;
Rashomon verifier unchanged (didn't use these helpers). All
five dramatica-complete demos produce byte-identical output.

Three previously-orphaned tests register in the `TESTS` list
(`event_participants_flat` regression + two
`run_direct_review_checks` tests). `test_verification.py`
reaches 199 (193 → 199, +6 total: 3 newly-running + 3 new
unit tests pinning the extracted helpers).

### Corpus audit outcomes (Tier-2 update)

Hamlet lands under the `*_aristotelian` suffix convention
(RI9); audits pick it up automatically:

- `audit_aristotelian_event_refs`: 63 records / 269 event-id
  refs clean across four paired encodings (was 24 / 180
  across three post-sketch-11).
- `audit_character_ref_ids`: 11 ArCharacter records clean
  (was 8). HAMLET/CLAUDIUS/LAERTES resolve against Hamlet's
  20-entity substrate.
- `audit_aristotelian_character_arc_relations` (NEW, added
  under A13): two records across four paired encodings
  (Hamlet's mirror + foil); structural-integrity checks run
  cleanly.
- `audit_aristotelian_anagnorisis_steps` extends to include
  step_kind consistency (A7.11); four corpus steps covered
  (Jocasta precipitating; Lady Macbeth parallel; GHOST_CLAIM
  + MOUSETRAP staging; CLAUDIUS_PRAYS parallel).

Six audit functions total; ~1220 references resolved across
kinds (1151 sketch-11 baseline + 69 new Aristotelian
event-ref+character+arc-relation refs from Hamlet + Macbeth
cleanup).

### Test suite

879 passing, **+72 from sketch-11's 807 baseline**. Breakdown:
- +22 test_aristotelian (Hamlet verification + A7.10 + A7.11)
- +16 test_aristotelian_reader_model_client (probe-sketch-04
  APA4 rendering extensions)
- +6 test_verification (Codex REVIEW refactor tests)
- +11 test_production_format_sketch_01_conformance (PFS11 +
  PFS12 + PFS13 — 5+4+6 = 15 new tests; net +11 after
  baseline shifts)
- +17 across other modules (sketch-03 A13/A14 implementation
  tests in test_aristotelian cumulative)

---

## Shift-point — sketch-03 is the first sketch driven end-to-end by a probe-surfaced forcing function

Prior sketch shape:

- Sketch-02 (aristotelian-sketch-02) landed A10–A12 in
  anticipation of probe-surfaced pressure, then probe-sketch-02
  verified the anticipation via re-probe. Closure was the shape.
- Probe-sketch-03 (Macbeth first-probe) verified closure
  generalizes and banked two new OQs (OQ-AP5, OQ-AP6) without
  immediate sketch response.

Sketch-03's shape is different:

- **Session 5 probe surfaces forcing** (OQ-AP6 direct hit,
  OQ-AP10 new).
- **Sketch-03 dialect sketch closes** (A13 + A14 + A7.10/A7.11
  + OQ-AP5 retirement).
- **Probe-sketch-04 catches the client up** (APA4-1..APA4-6).
- **Session 6 re-probe verifies** (closures structurally
  load-bearing; zero residual pressure on either closed axis).

This is the first end-to-end cycle in the Aristotelian series
where the probe forced the dialect shape rather than verifying
an anticipated one. The pattern — probe → sketch → probe-sketch
→ re-probe — is the full research→production→verification loop
the compiler-family framing (state-of-play-11 tooling frame)
always implied, now instantiated.

**The sketch-12 pattern — "probe-forced dialect sketch closes
end-to-end within one encoding's multi-session arc" — is
repeatable.** Candidate encodings that could drive a similar
arc: Ackroyd (narrator-as-tragic-hero question; deferred
fate-agent pressure from sketch-03), ATTWN (discrete-
elimination pathos; dialectically-absent-narrator edge case),
Lear (second ≥3-tragic-hero encoding, which would force
OQ-AP14 closure if the instrumental-kind pressure holds).

---

## What the twenty-one commits revealed

### Hamlet's multi-session shape works as a research primitive

Sessions 1–6 decomposed a single encoding arc into substrate-
skeleton, dialect-overlay, substrate-completion, encoding-tests,
first-probe, closure-sketch, client-sketch, re-probe. Each
session's commit body cites prior sessions by number + commit
SHA; each closes one concrete deliverable (skeleton, overlay,
completion, tests, JSON artifact, migration, client, v2 JSON).
A cold-start reader can reconstruct the arc from
`git log --oneline --reverse edb25cb..4b30291` plus the eight
commit bodies in sequence.

The **multi-session session-numbering convention** scales. It
lets an encoding that would otherwise be a single 2000-line
commit decompose into reviewable units without losing the
cross-session narrative (each body names its N-of-N position).

### Probe-surfaced closures are structurally load-bearing, not just accepted

Session 6's single sharpest result: the probe used A14's
step_kind distinction to catch an encoding error the verifier
could not (GHOST_CLAIM annotation's "first of three staging"
miscount against the chain's actual 2 staging + 1 parallel
shape). A closure that is merely *accepted* reads like
pre-sketch commentary — "the field makes this explicit." A
closure that is *load-bearing* reads like structural logic —
"the annotation should say 'first of two' because the chain
carries only two staging-kind steps; the third is parallel-
kind on a different character." The latter is what happened.

The same pattern appeared on A13: the probe's annotation
review on AR_HAMLET_CLAUDIUS_FOIL cited the foil relation's
structural content to CALL TENSION on the prose claim that
"each recognizes the other's failure." The foil is the
probe's reasoning ground, not its output.

### The reviewable-prose surface expansion (APA4-3) was productive, not thinning

Sketch-04 banked OQ-AP13 anticipating that expanding
reviewable prose from 3 record kinds (ArMythos / ArPhase /
ArCharacter) to 5 kinds (+ ArAnagnorisisStep +
ArCharacterArcRelation) might degrade P1 (proportion of prose
reviews approved). Session 6's P1 came in at 75% (9/12
approved), below sketch-01's ≥80% threshold — numerically
failing. **But all three needs-work findings are encoding
cleanups on the new surfaces** — the staging-step count error,
an ungrounded substrate reference in HAMLET hamartia_text, and
an overread in CLAUDIUS_FOIL's annotation. The new surfaces
did what they were designed to do: catch prose tensions the
verifier can't. OQ-AP13 therefore closes with opposite polarity
(expansion productive, not thinning); P1's numerical threshold
should be reconsidered at the next reviewable-prose expansion.

### Codex REVIEW.md findings continue to drain

Two refactor commits (`5bec864`, `b0b0eba`) close three
previously-flagged duplication patterns across the five
dramatica-complete verifier modules. The refactor-out
discipline extends sketch-11's pattern: factor when three
instances pressure duplication, explicit-parameter interfaces,
byte-identical outputs. The verifier-helpers module continues
to be the accumulator for extracted verifier primitives (six
primitives post-sketch-12; room for future extractions as the
duplication surface stabilizes further).

### Production C approaches completion

Post-sketch-12, three schema arcs remain under Production C:
PFS14 (Aristotelian sketch-03 landing), PFS15 (Dramatic),
PFS16 (Dramatica-complete). PFS14 is unblocked (sketch-03
shipped; AA15 deferred schema landing); PFS15/16 are gated on
the Dramatic arc's design-first work (dramatic-sketch-02).

The schema layer now covers 17 record types across five
namespaces. The next expansion axis is **amending existing
schemas** (PFS13 set the precedent; PFS14 is the second case).

---

## What's next (research AND production)

### Research track

1. **Encoding cleanups surfaced by Session 6.** Three small
   author-side fixes:
   - AR_STEP_HAMLET_GHOST_CLAIM.annotation: "first of three
     staging" → "first of two staging" (or "first of three
     chain steps").
   - AR_HAMLET.hamartia_text: remove or recontextualize the
     Rosencrantz-Guildenstern reference (not in central events
     or substrate).
   - AR_HAMLET_CLAUDIUS_FOIL.annotation: remove "each recognizes
     the other's failure" overread.
   Smallest concrete research item. Follow-up to probe-sketch-03
   Macbeth "first clause" cleanup precedent.
2. **Post-Session-6 probe on Macbeth under sketch-04 rendering.**
   Narrower-scope re-probe: does Macbeth's v2 reading cite A14's
   step_kind distinction when rendering AR_STEP_LADY_MACBETH_
   SLEEPWALKING? Retrospective, optional — closure already
   verified on Hamlet; Macbeth's probe under sketch-04 would
   provide a second closure-verification site. Defer unless
   a second site feels worth the cost.
3. **Fourth Aristotelian encoding candidate for ADJACENT binding.**
   The BINDING_ADJACENT gap in the corpus persists. No canonical
   text has been banked; candidate hunt would be research
   (close-reading to find a text with peripeteia and anagnorisis
   separated by 1–3 τ_s steps). Low priority — the gap is
   identified, not forcing.
4. **ATTWN dramatic + dramatica-complete fills.** Unchanged
   from sketch-11. MC/IC decision (Vera vs. Wargrave) unblocks
   MN2 concealment-asymmetry + LT8/LT9 discrete-elimination +
   ATTWN Save-the-Cat + ATTWN Aristotelian.
5. **OQ-AP14 second-site search.** Instrumental/manipulation
   A13 kind. Hamlet alone forces it with margin (encoding-
   author agreement + probe-surface convergence), but a second
   corpus site would strengthen the forcing criterion. Lear is
   the obvious candidate (Lear/Gloucester + Goneril/Regan +
   Edgar/Edmund — instrumental-kind pressure likely).
6. **OQ-AP15 second-site search.** Absent-but-catharsis-
   relevant characters. Corpus-wide scan (Gertrude in Hamlet;
   minor characters in Macbeth / Rashomon whose deaths matter
   for catharsis but who have no ArCharacter records).
   Structural question: does the dialect admit a lightweight
   "catharsis-participant" typing, or does catharsis lean on
   substrate-scope participation?
7. **Remaining scheduling-act-family seeds.** Bandit-refinement
   MC-mediated endpoint substitution; OQ1-reshaped woodcutter
   cross-branch signature detector. Each has a distinct forcing
   function; unchanged from sketch-11.

### Production track

Re-ordered by sketch-12's completions (items A / B / E closed;
sketch-11's C / D / F / H / I / J / K remain):

A. **~~PFS11 Aristotelian cross-boundary batch~~** — closed in
   sketch-12 as commit `8ce2a24`.
B. **~~PFS12 Save-the-Cat observation~~** — closed in sketch-12
   as commit `70738ee`.
C. **~~PFS13 Aristotelian A10–A12 schema landing~~** — closed
   in sketch-12 as commit `1f869dd`.
D. **PFS14 — Aristotelian sketch-03 schema landing.** Closes
   sketch-03 AA15. Amends existing schemas (mythos.json gains
   anagnorisis_character_ref_id; anagnorisis_step.json gains
   step_kind) + adds one new schema
   (character_arc_relation.json). Follows PFS13's amendment
   pattern.
E. **PFS15 — Dramatic dialect schemas.** Gated on
   dramatic-sketch-02 (PFS6 OQ2; six design forcing functions
   banked in dramatica-template-sketch-01). Dramatic-sketch-02
   design-first arc is prerequisite.
F. **PFS16 — Dramatica-complete dialect schemas.** Gated on
   PFS15.
G. **substrate-world-fold-sketch-01.** Unchanged from
   sketches-10/-11 — forcing function not yet surfaced.
H. **Markdown-fenced author parser** (roadmap item 1). First
   consumer of the schemas outside the conformance test. Now
   consumes five namespaces covering 17 record types.
I. **Prose export round-trip starter** (roadmap item 3).
J. **Goodreads import prototype** (roadmap item 2).
K. **Port work** (roadmap item 4). Cross-boundary fully
   spec'd post-PFS13; Aristotelian sketch-03 pending PFS14.

### Recommendation

Mixed arc — one production + one research item.

- **Production track D (PFS14)** — sketch-03 schema landing.
  Small arc under PFS13's amendment precedent. Closes
  aristotelian-sketch-03 AA15. Unblocks downstream port work
  on the sketch-03 surface.
- **Research track 1 (Session-6-surfaced encoding cleanups)** —
  three concrete author-side fixes. Smallest concrete research
  item; doesn't block anything but cleans the Hamlet encoding
  after Session 6's diagnostic output.

Alternative (deferred if time runs short): **Research track 5
(Lear for OQ-AP14)** — second-site search for the
instrumental-kind pressure. Substantial; would open a new
multi-session arc (Lear Sessions 1–N following Hamlet's
precedent).

---

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketches-04 through -11. Validated across
the twenty-one sketch-12 commits, with one new addition:

- **Session-numbered research arcs** (Hamlet introduced the
  convention; other multi-session encodings inherit). Each
  session's commit body cites prior sessions by number + SHA
  and carries the arc's forward candidates. A reader can
  reconstruct a multi-session encoding arc from its session
  commits alone.
- **JSON-as-ground-truth, summary-as-scan** (probe-sketch-04
  APA4-7 codified what commit `7a86e1e` introduced). Commit
  messages on probe-run research commits must cite the JSON
  artifact directly, not the demo's substring-matcher summary.
  Session 6's commit message models the pattern.
- **Probe-sketch-N extends client-layer for dialect-sketch-N**
  (probe-sketch-02 precedent + probe-sketch-04 continuation).
  When a dialect sketch adds new records or fields, the
  matching probe-sketch's first deliverable is catching the
  LLM-prompt surface up. This is load-bearing: sketch-03's
  closures couldn't be probe-verified without APA4-1..APA4-5,
  even though the records existed at the Python layer.
- **Orientation before commitment** + **sketches before
  implementation** + **banking with forcing-function criteria**
  + **commit messages as cross-session artifacts** — all
  unchanged from sketch-11.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic.
2. This doc (`design/state-of-play-12.md`) — current corpus,
   shift-point state, research + production tracks.
3. `schema/README.md` — the three-tier production layer
   (substrate / dialect / cross-boundary), now covering 17
   record types across five namespaces.
4. `git log --oneline --reverse ffcef4f..HEAD` — the 21
   sketch-12 commits carry dense readable bodies; the Hamlet
   multi-session arc in particular is reconstructable from its
   commit sequence.
5. `design/state-of-play-11.md` — sketch-11's cold-start doc.
   Sketch-12 supersedes it, but sketch-11 carries the Macbeth-
   landing + SC6–SC10 prose-carried signal + reader-model-
   client-base milestones.
6. `design/aristotelian-sketch-03.md` — the A13 + A14 + A7.10 +
   A7.11 extensions that close OQ-AP6 / OQ-AP10 and retire
   OQ-AP5.
7. `design/aristotelian-probe-sketch-04.md` — the client-
   rendering extensions + Session 6 re-probe framing. Session 6
   closure-verification is the probe-run that ships under this
   sketch.
8. `prototype/story_engine/encodings/hamlet.py` +
   `hamlet_aristotelian.py` — the fourth Aristotelian encoding,
   first to force a dialect amendment, first multi-session
   research arc.
9. `prototype/reader_model_hamlet_aristotelian_output.json` (v1,
   Session 5) +
   `reader_model_hamlet_aristotelian_output_v2.json` (v2,
   Session 6) — the two JSON artifacts. Diff shows the closure-
   verification shape end-to-end.
10. `prototype/story_engine/core/verifier_helpers.py` — the
    accumulator for extracted verifier primitives; six
    primitives post-sketch-12 with room for future extractions.
