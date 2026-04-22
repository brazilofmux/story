# State of play — sketch 13

**Status:** active
**Date:** 2026-04-22
**Supersedes:** [state-of-play-12](state-of-play-12.md)

Cold-start orientation doc, rewritten (not amended) at the
milestone where the **compiler-family arc retires the project's
biggest risk end-to-end** (stage-2 arithmetic gate + stage-3 POCL
spike across three scenes / five operators / 4-step plans with
epistemic preconditions), and **the probe-driven sketch-closure
loop reaches its second corpus instantiation** via the **Lear
10-commit arc closing aristotelian-sketch-05**.

**Twenty-eight commits since state-of-play-12.** Largest delta
between consecutive state-of-play sketches by commit count
(SoP-11→SoP-12 was 21; SoP-12→SoP-13 is 28). Two
distinguishable arcs: (1) sixteen commits on 2026-04-21 driving
the compiler-family work from naming through stage-3-sketch-03;
(2) ten commits on 2026-04-22 driving the Lear arc end-to-end
plus a sketch-05 closure cycle.

## Headline — three load-bearing claims

### 1. Compiler feasibility proved end-to-end for minimum-viable case

The project's biggest risk per `feedback_risk_first_sequencing.md`
has been retired for the minimum-viable case. The compiler-family
arc spans:

- **Naming phase** (1 commit): `compilation-sketch-01` (`edc8d77`)
  names the dialect-to-substrate compiler backend shape — four
  stages (extract, feasibility, plan, rank), STRIPS planner +
  LLM-as-ranker + existing verifiers as type-check.

- **Compilation surface formalization** (3 commits):
  `dialect-compilation-surface-sketch-01` (`86c2a64`) names the
  two-sided dialect surface (DCS1-DCS6 abstract); `aristotelian-
  sketch-04` (`91b2e01` design + `0ab7660` impl) lands A15+A16
  as the first compilation-surface instantiation; PFS14
  (`9b701ad`) lands the schema layer.

- **Save-the-Cat second-dialect compilation surface** (3 commits):
  `save-the-cat-sketch-03` (`584d373` design + `8356099` impl +
  `980f621` review fix) instantiates DCS1-DCS6 on the second
  dialect (S14+S15+S16); PFS15 (`6ea79ad`) lands the schema
  layer.

- **Stage-2 feasibility-gate spike** (2 commits):
  `compilation-stage-2-sketch-01` (`72e201d` design + `b443789`
  impl) implements the arithmetic gate.

- **Stage-3 POCL planner spike** (7 commits, three sub-sketches):
  `compilation-stage-3-sketch-01` (`62bd8b9` + `7767571`)
  implements the primitive POCL mechanism (1 scene, 2 operators,
  3-step plan); `compilation-stage-3-sketch-02` (`1949e77` +
  `e7911ed`) adds typed variables + `acquire` operator + scene 2
  (2 scenes, 3 operators, 4-step plan with material acquisition);
  `compilation-stage-3-sketch-03` (`c72c95d` + `c839864`) adds
  epistemic preconditions + `learn_from` operator + scene 3
  (3 scenes, 5 operators, 4-step plan with mid-plan knowledge
  acquisition — Oedipus solving the Sphinx's riddle).

- **Edge-case fix** (1 commit): `aa8c0b9` fixes stage-2 and
  stage-3 corner cases.

The stage-3 spike covers the architecturally-hardest sub-axis of
OQ1 (state-representation richness) — flat propositional
`knows(agent, fact)` epistemic state composes uniformly with
spatial and material preconds; the planner needed no epistemic-
specific machinery. OQ1's harder sub-cases (nested knowledge,
modal slots, false belief, temporal epistemic reasoning) remain
banked as future work, but the easiest sub-case is closed.

**Risk-first stance update:** compiler is no longer the
project's biggest risk for minimum-viable case. Future risk-
first sequencing should re-evaluate against the now-shorter risk
list (per `project_compiler_feasibility_proved` memory).

### 2. Probe-driven sketch-closure loop reproducible on a second encoding

The Lear 10-commit arc on 2026-04-22 reproduces the Hamlet 6-
session arc shape (Sessions 1-4: substrate + overlay + completion
+ tests; Session 5: probe; Session 6: re-probe under closure-
sketch). This is the second corpus instantiation of the full
research→production→verification loop.

- **Sessions 1-4** (`bfecd73`, `b75fa11`, `bc89a77`, `95e18f9`):
  substrate skeleton (45 events, 24 entities, 1 derivation rule)
  → Aristotelian overlay (5 ArCharacters incl. 3 tragic heroes,
  4 A13 relations incl. 2 non-canonical 'instrumental') →
  PREPLAY_DISCLOSURES + SJUZHET (42 entries) + DESCRIPTIONS (12
  records) → 13 encoding-specific tests.

- **Session 5** (`525c575`): first probe run. Direct hits on
  OQ-AP14 (instrumental-kind) with two probe-proposed dialect
  fields (`directionality`, `polarity`); three new forcing
  functions surfaced (OQ-LEAR-3 tragic-hero-without-anagnorisis,
  OQ-LEAR-4 secondary-peripeteia, OQ-LEAR-5 audience-level
  parallel-plot catharsis); three banked forcing functions
  (OQ-AP15, OQ-AP7, OQ-LEAR-1) failed to surface.

- **Author-fixes** (`90975b4`): three Session-5 needs-work prose
  corrections.

- **aristotelian-sketch-05** (`c7198de` design + `8503d22` impl
  + migrations): closes OQ-AP14 (A17 directionality + polarity)
  + OQ-LEAR-3 (A18 anagnorisis_absent). Migrates Lear (4 A13
  relations + AR_CORDELIA) and Hamlet (2 A13 relations).

- **Client extension** (`ecd3d6e`): renders new fields + adds
  sketch-05 SYSTEM_PROMPT paragraph.

- **Session 6** (`974d5f3`): re-probe verifies closure. P1=14/15
  (93%, up from Session 5's 80%). Probe explicitly cites the new
  fields as the closures it asked for. dialect_reading rationale:
  "Cordelia's anagnorisis_absent=true is a successful sketch-05
  extension." The full loop landed end-to-end in <24h.

**Pattern verification:** Hamlet (sketch-03 closure) + Lear
(sketch-05 closure) are now two independent instantiations of the
loop. The multi-session session-numbering convention scales; the
research→production→verification cycle reproduces; sketch-05's
shape decomposition (directionality + polarity as orthogonal
fields rather than a fourth canonical kind) is a sharper
closure than the encoding's three-axis 'instrumental' bundle —
probe-proposed shapes can be cleaner than encoding-author-
proposed shapes. New methodological trust signal.

### 3. "Highlight observation" semantic category enters the verifier

`A7.15 check 5` (paired-non-canonical-polarity-contrast) is the
first verifier check that emits `severity=noted` not to flag a
deficiency but to highlight a structurally-load-bearing
authorial pattern. When two non-canonical-kind A13 relations
share a target (defined as `character_ref_ids[1]` when
`directionality="directional"`) with different non-empty
polarities, the check emits a noted observation referencing both
record ids.

Session 6's probe validated the semantic distinction: *"This is
the most structurally significant observation in the set."* The
probe's commentary even proposed a tightening (verify
over_event_ids do NOT overlap to confirm causally-independent
wielder-chains).

The category name "highlight observation" is provisional
(adjacent to "noted" but semantically distinct from "advises-
review"); future sketches may formalize the distinction as a new
severity level or as a code-prefix convention. For now the check
is sketch-05 A7.15 #5; the methodological category it instantiates
is recorded in `project_lear_encoding` memory.

## Three forcing-function reclassifications — epistemic discipline working

Per `feedback_sketch_implement_rhythm_falsifies.md`:
"implementation regularly falsifies one [claim]". Sketch-05's
design doc § Out-of-scope-disposition records THREE forcing
functions weakened by Session 5's probe (which did not surface
them despite the encoding being engineered to pressure them):

- **OQ-AP15 (absent-character catharsis)** → substrate-signature-
  only pressure. Cordelia's offstage hanging with empty observer
  set + observer-wave on the entrance event is self-consistent at
  substrate scope; probe did not pressure dialect extension.
  Session 6 confirmed (no re-surface).

- **OQ-AP7 (range-of-separated)** → conjectural. Lear at distance
  14 (corpus widest) was an ideal second-site; probe read it as
  "separated" without discomfort. Hamlet's one-site claim does
  not generalize.

- **OQ-LEAR-1 (emotional-vs-epistemic staging)** → substrate-
  signature-only. Probe approved Lear's 2-parallel-no-staging
  chain without flagging the emotional progression as a gap. The
  `remove_held` at E_lear_cordelia_reconcile is the substrate
  marker; the dialect does not need a `step_kind="affective"`.

Three weakenings in one sketch is the discipline working —
design-first speculation falsified by probe data, acknowledged
in-place. The compiler-arc work has the parallel pattern: stage-
3-sketch-01's hypothesis "schema-author MUST order preconditions
knows-before-at" was falsified by stage-3-sketch-03's
implementation showing the planner is more flexible (S3P14
refined: schema ordering is an optimization, not correctness).

## Two new forcing functions banked with concrete shape proposals

- **OQ-LEAR-4 — Secondary peripeteia for subplot.** Single-site
  (Lear). Session 6 returned three concrete dialect-extension
  proposals: `ArMythos.secondary_peripeteia_event_ids` field, OR
  `ArPhase`-level `peripeteia_event_id`, OR `ArMythosRelation
  kind='subplot'` (using existing A10 apparatus). Forcing-criterion:
  second encoding with parallel-plot peripeteia. Candidates:
  Webster's *The White Devil* / *The Duchess of Malfi*
  (subplot-rich Jacobean tragedies); Tourneur's *The Revenger's
  Tragedy*; or any non-Shakespeare double-plot tragedy.

- **OQ-LEAR-8 — Promote 'instrumental' to canonical
  ArCharacterArcRelation kind.** Single-encoding pressure
  (Lear has 2 instrumental relations; probe explicitly asks for
  promotion). Forcing-criterion: either (a) cross-encoding —
  second encoding authors 'instrumental' independently
  (candidates: any encoding with manipulator-victim dynamic —
  Iago/Othello, Vindice/Hippolito-various-targets in *Revenger's
  Tragedy*), OR (b) single-encoding-saturation — sketch-06
  promotes on argument-from-structural-recurrence alone.

Probe also surfaced a candidate A7-check signature
(`kind_promotion_candidate`) that would mechanize the (b) path:
when ≥2 non-canonical relations share kind in one encoding,
emit noted suggesting canonical consideration. Banked candidate
for sketch-06 if the OQ-LEAR-8 closure is taken.

---

## What is built — delta from sketch-12

### The corpus (fifth Aristotelian encoding + second multi-session research arc)

**Lear Aristotelian** — the dialect's fifth encoding, the
corpus's second multi-session research arc, and the second
encoding to force a dialect amendment (A17 + A18).

- `prototype/story_engine/encodings/lear.py` (substrate, ~1600
  lines across Sessions 1+3). 45 substrate events, 24 entities,
  full τ_s ordering from Lear-reigns (τ_s=-30) through
  Lear-dies (τ_s=38). 1 derivation rule (FRATRICIDE for Edgar/
  Edmund — corpus's first sanctioned kin-killing).
- `prototype/story_engine/encodings/lear_aristotelian.py`
  (overlay, ~1100 lines across Sessions 2 + post-sketch-05).
  AR_LEAR_MYTHOS: complex plot, 45 central events, three phases
  (16/16/13 events), peripeteia=E_goneril_strips_retinue
  (τ_s=14), anagnorisis=E_lear_cordelia_reconcile (τ_s=28),
  BINDING_SEPARATED distance 14 (corpus widest, exceeds Hamlet's
  9 and Oedipus's 5), anagnorisis_character_ref_id="ar_lear",
  asserts_unity_of_action=False (corpus first), tonal_register=
  TRAGIC_PURE. Five ArCharacter records (Lear / Gloucester /
  Cordelia tragic-hero=True; Edmund / Edgar False — first ≥4
  ArCharacters in corpus). Cordelia: anagnorisis_absent=True
  (corpus first; A18 sketch-05 closure of OQ-LEAR-3).
  AR_LEAR_CHARACTER_ARC_RELATIONS: 4 records (parallel + foil +
  2 instrumental — first multi-record, multi-kind A13 set in
  corpus). Anagnorisis chain: 2 parallel steps
  (AR_STEP_GLOUCESTER_BLINDING pre-main + AR_STEP_EDMUND_CONFESSES
  post-main; first post-main parallel step in corpus).
- `prototype/tests/test_aristotelian.py`: +13 Session-4 Lear
  tests + 21 sketch-05 tests (synthetic + integration). 174
  total aristotelian tests.
- `prototype/reader_model_lear_aristotelian_output.json`
  (Session 5, pre-sketch-05) +
  `reader_model_lear_aristotelian_output_v2.json` (Session 6,
  post-sketch-05) — two JSON artifacts preserved for diff.

**Aristotelian dialect corpus (post-sketch-13)**: five
encodings — oedipus, rashomon, macbeth, hamlet, lear.
- Binding coverage: SEPARATED (oedipus distance 5, hamlet 9,
  lear 14), COINCIDENT (macbeth), ADJACENT uncovered.
- Anagnorisis chain shapes: precipitating (Oedipus Jocasta),
  parallel (Macbeth Lady-Macbeth + Hamlet Claudius-prays + Lear
  Gloucester-blinding + Lear Edmund-confesses POST-MAIN), staging
  (Hamlet GHOST_CLAIM + MOUSETRAP).
- Character-arc relations: kinds parallel (Lear-Gloucester),
  mirror (Hamlet-Laertes), foil (Hamlet-Claudius + Edgar-Edmund),
  instrumental NON-CANONICAL (Edmund→Gloucester +
  Edgar→Gloucester).
- anagnorisis_absent: Cordelia (Lear; corpus first).
- asserts_unity_of_action=False: Lear (corpus first).

### The dialect layer (aristotelian-sketch-05)

Two new commitments + two new self-verifier checks:

- **A17** — `directionality` (`'symmetric' | 'directional' | ''`)
  + `polarity` (`'malicious' | 'therapeutic' | 'neutral' |
  'sanctioned' | ''`) on `ArCharacterArcRelation`. Closes
  OQ-AP14. Empty-string defaults preserve back-compat.
  Canonical kinds (parallel/mirror/foil) are symmetric by
  construction; non-canonical kinds (e.g., 'instrumental') are
  typically directional and carry polarity.

- **A18** — `anagnorisis_absent: bool = False` on `ArCharacter`.
  Closes OQ-LEAR-3. Marks tragic heroes whose hamartia produces
  catastrophe for others but whose own arc has no recognition
  moment (Cordelia).

- **A7.15** — five invariants on the new fields, including the
  novel **paired-non-canonical-polarity-contrast NOTED** (check
  5) — first "highlight observation" in the dialect. Folds
  OQ-LEAR-6 + OQ-LEAR-7 (probe-suggested A7 signatures from
  Session 5 commentaries).

- **A7.16** — three advises-review invariants on
  `anagnorisis_absent` (requires tragic_hero, not main, no
  contradicting chain step). Deliberately NO implicit-gap
  detection.

Extension-only: A1–A16 semantics unchanged. Pre-sketch-05
encodings (Oedipus, Rashomon, Macbeth) verify identically;
Hamlet migrates two A13 relations to symmetric+empty-polarity
(zero observations post-migration).

### The reader-model client (sketch-05 rendering extensions)

- `_ar_character_to_dict` renders `anagnorisis_absent`.
- `_ar_character_arc_relation_to_dict` renders `directionality`
  + `polarity`.
- SYSTEM_PROMPT gains a sketch-05 paragraph naming both
  extensions, directional tuple convention, canonical
  vocabularies, and adjacent-gap invitation (subplot peripeteia
  apparatus, parallel-plot catharsis).

Pattern parallels probe-sketch-04's APA4-1..APA4-6: sketch-N's
dialect extensions require client-layer rendering for the next
session's probe to engage with them.

### The compiler layer (stages 2+3, three sketches)

`prototype/story_engine/core/compiler_stage_2.py` +
`compiler_stage_3.py` ship the feasibility gate + POCL planner
spike. Three stage-3 sketches stress different OQ1 sub-axes:

- Stage-3 sketch-01 (1 scene / 2 operators / 3-step plan):
  primitive POCL mechanism works in <300 LOC core.
- Stage-3 sketch-02 (2 scenes / 3 operators / 4-step plan):
  typed variables + material acquisition.
- Stage-3 sketch-03 (3 scenes / 5 operators / 4-step plan):
  flat propositional epistemic state composes uniformly.

Tests: `test_compiler_stage_2.py` (28 tests) +
`test_compiler_stage_3.py` (52 tests). All green.

### The schema layer (PFS14 + PFS15)

- **PFS14** — Aristotelian sketch-03 schema landing. Closes
  sketch-03 AA15. Three new schema files
  (`character_arc_relation.json`, etc.) under
  `schema/aristotelian/`.
- **PFS15** — sketch-04 A15+A16 schema landing.

Sketch-05 schema landing (A17 + A18) deferred — PFS16 candidate,
gated on sketch-05 stabilization (production-format track
follows the dialect by 1-2 sketches).

### Test suite

**992 passing, +113 from sketch-12's 879 baseline.** Breakdown:
- +24 test_compiler_stage_2 (stage-2 sketch-01)
- +52 test_compiler_stage_3 (stage-3 sketches 01+02+03)
- +13 test_aristotelian (Lear Session 4)
- +21 test_aristotelian (sketch-05 synthetic + integration)
- +3 various other modules' bumps

---

## Shift-point — sketch-13 is the first state-of-play with two complete probe-driven closure arcs

Prior shape (sketch-12):
- One probe-driven sketch closure complete (Hamlet → sketch-03);
  closure verified in Session 6 of Hamlet arc. The pattern was
  established but had only one instantiation.

Sketch-13's shape:
- Hamlet sketch-03 closure verified.
- **Lear sketch-05 closure verified.** Two encodings independently
  followed the same pattern: probe surfaces forcing → closure-
  sketch designs response → impl + migration → client extension
  → re-probe verifies closure landed.

The pattern is no longer one-shot; it's reproducible. New
multi-session research arcs (Ackroyd, ATTWN, Lear's siblings —
Webster, Tourneur, Marlowe) inherit the convention and can
follow the same arc shape with confidence the loop will land.

**The sketch-13 pattern — "two independent closure arcs with
matching shape" — is the methodology working.** Arc-by-arc
discipline: design-first sketches forced to falsify, retire, or
amend by probe data; weakened forcing functions reclassified
honestly; new pressures banked with concrete shape proposals.

---

## What the twenty-eight commits revealed

### Compiler retires for minimum-viable case in three sub-sketches

Stage-3 across three sub-sketches retired three OQ1 sub-axes:
spatial+material (sketch-01+02) and epistemic (sketch-03). The
sketch-03 work also surfaced S3P-OQ10/11/12 — banked as the
NEXT sub-axes (POCL threat resolution, nested epistemic state,
knowledge-acquisition primitives beyond `learn_from`). Those
banked OQs are the natural sketch-04+ candidates for the
compiler track if the user decides to push compiler further.

### Probe-proposed shape decompositions can be sharper than encoding-author shapes

Lear Session 2 banked OQ-AP14 with a three-axis "instrumental
kind" candidate (directional + artifact-mediated + polarity-
inverted, bundled). Session 5's probe proposed a TWO-FIELD
decomposition (directionality + polarity as orthogonal axes).
Sketch-05 shipped the probe's shape, not the encoding's.
Methodological observation: probe-driven dialect extensions can
out-decompose author-driven ones because the probe sees the
dialect surface as a whole and proposes against the existing
field-shapes, where the author may be over-attached to the
single-record framing of the forcing case.

Recorded for future sketch-closure cycles: take probe's shape
proposals seriously even when they differ structurally from the
encoding's hypothesized shape.

### Three weakenings is the rhythm working

Session 2's claims about OQ-AP15 / OQ-AP7 / OQ-LEAR-1 were
falsified by Session 5's probe in one run. Sketch-05 §Out-of-
scope-disposition records all three reclassifications honestly.
This is the second corpus instance of the rhythm
(`feedback_sketch_implement_rhythm_falsifies.md`) operating
at probe-run scale rather than implementation-detail scale.

The probe's silence is informative — three banked forcing
functions failed to elicit dialect-extension proposals despite
the encoding being engineered to pressure them. The weakening is
data, not failure.

### The reader-model client plays a load-bearing role in the closure cycle

Without the sketch-05 client extension (commit `ecd3d6e`),
Session 6's re-probe would have read the sketch-05-migrated
encoding through the sketch-04 prompt — the new fields would not
be visible to the LLM. The "client extension" step (parallel to
probe-sketch-04 for Hamlet) is required for the closure
verification to work; future sketch-N closures must remember to
extend the client before re-probing.

This is the third explicit step in the closure cycle:
1. design + impl + migration (sketch).
2. client extension (probe-sketch or amendment commit).
3. re-probe (Session N+1 of the encoding's arc).

Skipping (2) means (3) reads stale.

---

## What's next (research AND production)

### Research track

1. **OQ-LEAR-4 second-site search.** Subplot-with-own-peripeteia
   tragedy. Candidates: Webster's *Duchess of Malfi* (Antonio
   subplot), Marlowe's *Edward II* (Mortimer's parallel arc),
   Tourneur's *Revenger's Tragedy* (Lussurioso/Spurio sub-plot).
   Forcing criterion: second encoding with structurally-distinct
   subplot peripeteia. Would unlock sketch-06 design choice
   between secondary_peripeteia_event_ids field, ArPhase-level
   peripeteia, or ArMythosRelation kind='subplot'.

2. **OQ-LEAR-8 first-encoding-saturation closure** (alternative
   path). Sketch-06 promotes 'instrumental' to canonical kind on
   single-encoding-recurrence argument plus probe-validation.
   Concrete deliverable: sketch-06 A19 — `ARC_RELATION_INSTRUMENTAL`
   added to `CANONICAL_CHARACTER_ARC_RELATION_KINDS`; A7.10
   check 1 admits 'instrumental' without firing the noncanonical-
   kind noted; A7.15 check 5 unchanged.

3. **OQ-LEAR-8 cross-encoding closure** (alternative path).
   Author a second encoding with `kind="instrumental"` —
   candidates: Iago/Othello, Sheppard/Ackroyd-investigators,
   Vera/Wargrave-victims. Cross-encoding pressure is the
   sketch-02 forcing-criterion baseline.

4. **OQ-LEAR-5 / OQ-AP1 convergence search.** Audience-level
   parallel-plot catharsis (Lear) + cluster-pathos (Hamlet) +
   scattered-pathos (Macbeth) + concentrated-end-pathos
   (Oedipus) + dispersed-offstage-pathos (Lear). Five distinct
   pathos shapes; if a sixth converges on a typed-pathos shape,
   OQ-AP1 forcing-function-ready.

5. **Compiler stage-3 sketch-04 candidate** — POCL threat
   resolution (S3P-OQ10). Single banked OQ from stage-3-sketch-03;
   could close the planner's pragmatic-ordering fragility. Would
   require ~300 LOC of POCL-classical machinery (promotion +
   demotion). Not architecturally hard but materially work.

6. **Compiler stage-3 sketch-04 alternative** — Richer epistemic
   state (S3P-OQ11). Nested knowledge / modal slots / false
   belief / temporal indexing. Architecturally interesting; would
   pressure substrate's Held-record modal structure. Higher-risk
   spike.

7. **Multi-session arc candidates** — Ackroyd (narrator-as-
   tragic-hero question; deferred fate-agent pressure from
   sketch-03), ATTWN (discrete-elimination pathos), or any
   non-Shakespeare candidate (Webster / Tourneur / Marlowe /
   Sophocles' *Antigone*). Each could surface fresh forcing
   functions.

### Production track

A. **PFS16 — Aristotelian sketch-05 schema landing.** Closes
   sketch-05 AA15-equivalent. Single new field addition to
   `character_arc_relation.json` (directionality + polarity
   enums) + single new field on `character.json`
   (anagnorisis_absent bool). Smallest per-record arc in
   Production C series. Follows PFS13/PFS14/PFS15 pattern.

B. **PFS17 — Dramatic dialect schemas.** Gated on
   dramatic-sketch-02 design-first arc.

C. **PFS18 — Dramatica-complete dialect schemas.** Gated on
   PFS17.

D. **substrate-world-fold-sketch-01.** Unchanged from sketches-
   10/-11/-12 — forcing function not yet surfaced.

E. **Markdown-fenced author parser** (roadmap item 1). First
   consumer of the schemas outside the conformance test.

F. **Prose export round-trip starter** (roadmap item 3).

G. **Goodreads import prototype** (roadmap item 2).

H. **Port work** (roadmap item 4). Cross-boundary fully spec'd
   post-PFS13/14/15; sketch-05 surface pending PFS16.

### Recommendation

Per `feedback_research_production_alternation.md` — the last
substantive commit (`974d5f3`) is research mode (Session 6
re-probe). Next should lean production. Candidates ordered by
fit:

- **PFS16 (sketch-05 schema landing)** — small, follows precedent,
  closes the sketch-05 arc cleanly. Strongest production fit.
- **OQ-LEAR-4 second-site search via Webster** — research, but
  the user may want this if cross-encoding pressure is the
  highest-value next probe target.
- **Compiler stage-3 sketch-04 (POCL or richer epistemic)** —
  research; could bank the next compiler-arc segment.

Alternative (high-novelty, possibly defer): **fourth Dramatica
quad layer** (roadmap item 5) — mechanical, storage-cheap,
probe-context-expensive per `project_longterm_roadmap`. Defer
unless user wants a mechanical interlude.

---

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketches-04 through -12, with one
addition:

- **Client-extension is a load-bearing closure-cycle step.**
  Sketch-N closure cycles must include: sketch-N design + impl
  + encoding migration + client extension + re-probe. Skipping
  client extension means the re-probe reads stale dialect surface.
  Pattern instantiated twice (probe-sketch-04 for Hamlet,
  ecd3d6e for Lear).

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic.
2. This doc (`design/state-of-play-13.md`) — current corpus,
   shift-point state, research + production tracks.
3. `schema/README.md` — the three-tier production layer.
4. `git log --oneline --reverse 8d617a1..HEAD` — the 28
   sketch-13 commits carry dense readable bodies; the Lear
   10-commit arc on 2026-04-22 is reconstructable from the
   commit sequence alone.
5. `design/state-of-play-12.md` — sketch-12's cold-start doc.
   Sketch-13 supersedes it, but sketch-12 carries the Hamlet-
   closure milestone.
6. `design/aristotelian-sketch-05.md` — the A17 + A18 + A7.15 +
   A7.16 closures and the three-weakening reclassification.
7. `design/compilation-stage-3-sketch-03.md` — the epistemic-
   precondition spike that retires the planner-feasibility
   sub-axis of OQ1.
8. `prototype/story_engine/encodings/lear.py` +
   `lear_aristotelian.py` — the fifth Aristotelian encoding,
   second to force a dialect amendment, second multi-session
   research arc.
9. `prototype/reader_model_lear_aristotelian_output.json` (v1,
   Session 5) +
   `reader_model_lear_aristotelian_output_v2.json` (v2,
   Session 6) — diff shows the sketch-05 closure shape end-to-
   end.
10. `prototype/story_engine/core/aristotelian.py` — the dialect
    core; A7.15 check 5 is the corpus's first highlight
    observation.
11. `prototype/story_engine/core/compiler_stage_3.py` — the
    POCL-spike implementation; minimum-viable compiler core
    that retired the project's biggest risk.
