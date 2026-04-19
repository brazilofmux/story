# State of play — sketch 04

**Status:** superseded by [state-of-play-05](state-of-play-05.md)
**Date:** 2026-04-19
**Supersedes:** [state-of-play-03](state-of-play-03.md)

A cold-start orientation doc, rewritten (per the sketch-01 → sketch-
02 → sketch-03 discipline — "don't amend, write sketch-04 at the
next milestone") at the close of the architectural-stability-test
arc. Sketch-04 marks a category shift in the project's "What's
next" queue: for the first time, production-direction work
(memory `project_longterm_roadmap`) is as live a candidate as
further research.

Four commits since sketch-03 consumed all of sketch-03's
"What's next" list plus an architecture-stability test the list
didn't have:

- `72dfdbe` — post-SC4 Rashomon probe; third link in the Rashomon
  JSON chain; four new sketch seeds (sketch-03's item #1, closed).
- `8c8358e` — throughline-lowering-scope-sketch-01 +
  implementation; closed two NEEDS_WORK annotation-review findings
  from `72dfdbe`.
- `f4a03ec` — aristotelian-sketch-01 (design; falsifiable
  architecture-stability test). Every commitment A1–A9
  extension-only; Oedipus baseline + Rashomon stress case at
  worked-example depth.
- `a3a09a8` — aristotelian-sketch-01 implementation (AA1–AA5);
  `aristotelian.py` + `oedipus_aristotelian.py` + 31 tests; zero
  modifications to any existing file. Design-phase verdict
  confirmed in code.
- `1949277` — Rashomon-Aristotelian multi-mythos stress case in
  code; four `ArMythos` records, 0 observations each; the sketch's
  final prediction confirmed.

**Headline result:** the architecture passed both halves of a
deliberate, falsifiable stability test. See "Shift-point test
result" below.

Re-write this sketch (don't amend — write sketch-05) at the next
milestone. Stale state-of-play is worse than none.

---

## What is built

### The dialect stack (core machinery)

Now **four** upper dialects under architecture-sketch-02's stack,
up from two pre-aristotelian:

- **substrate** (`core/substrate.py`) — typed facts, events,
  branches, descriptions. Unchanged since substrate-sketch-05.
- **dramatic** (`core/dramatic.py`) — Throughlines, Characters,
  Scenes, Beats, Arguments, Stakes; StoryEncoding + StoryRelation
  for multi-Story. Unchanged since sketch-03.
- **dramatica-complete** (`core/dramatica_template.py`) — DSPs on 6
  axes, DomainAssignments, Signposts, ThematicPicks,
  CharacterElementAssignments, Story_goal, Story_consequence.
  Unchanged since sketch-03.
- **save_the_cat** (`core/save_the_cat.py`) — StcBeat, StcStrand,
  StcGenre, StcCharacter. Unchanged since sketch-03.
- **aristotelian** (`core/aristotelian.py`) — **NEW since sketch-
  03**. ArMythos (mythos-as-soul; primary record), ArPhase
  (beginning/middle/end), ArCharacter (optional cross-dialect
  ref), ArObservation. Self-verifier runs A7 checks 1–5 inside
  Aristotelian vocabulary. Specified by aristotelian-sketch-01.

- **lowering** (`core/lowering.py`) — the cross-dialect binding
  record. Unchanged.
- **verification** (`core/verification.py`) — VerificationReview +
  StructuralAdvisory. Unchanged.
- **verifier_helpers** (`core/verifier_helpers.py`) — LT1–LT14,
  EK2, AG1–AG6, SC2/SC3. Unchanged since sketch-03.

Package adjuncts in `core/` (unchanged): proposal_walker,
reader_model_client, dramatic_reader_model_client.

**The substrate and existing dialect records have now gone two
sketches (03 → 04) and five commits without modification — and
this despite a deliberate architectural stress test (aristotelian-
sketch-01) designed to break them.** The stability claim has
earned evidence.

### The encodings

Five fully-verified works (unchanged): **Oedipus**, **Macbeth**,
**Ackroyd**, **Rocky**, **Rashomon**. Rashomon's bandit and
samurai remain APPROVED 0.5 (post-SC4); the post-SC4 probe
endorsed samurai and qualified the other three in
architecturally-distinct ways (see "closed since sketch-03" below).

Sixth encoding (bootstrapped, content pending since sketch-03):
**And Then There Were None**. No change — still skeleton + docstring.

Dialect-only encodings (unchanged): **Chinatown** (Dramatic-layer
tragedy), **Pride and Prejudice** (Dramatic-layer triumph),
**Turn of the Screw** (substrate stub from the infeasibility
probe).

**New in sketch-04: Aristotelian encodings.**

1. **Oedipus under Aristotelian** (`oedipus_aristotelian.py`). 16
   central events across 3 phases; peripeteia at
   `E_messenger_adoption_reveal` (Poetics 1452a); anagnorisis at
   `E_oedipus_anagnorisis` (a substrate event named pre-sketch —
   the original `oedipus.py` encoder was thinking Aristotelian).
   Verifies with 0 observations.
2. **Rashomon under Aristotelian** (`rashomon_aristotelian.py`).
   **Four** ArMythos records, one per testimony. Each shares the
   6 canonical-floor events (E_travel through E_intercourse) as a
   common beginning phase; each diverges across testimony-branch
   events in middle/end; each carries its own peripeteia, tragic
   hero, and hamartia. No `ArMythosRelation` record — the dialect-
   scope limit for contested mythos relations is acknowledged as
   a sketch-02 OQ (aristotelian-sketch-01 stress case), not
   implemented. Each mythos verifies with 0 observations
   independently.

Test surface: **621 standard tests** (was 586 pre-aristotelian;
+35 aristotelian), **40 venv-gated tests** (unchanged).

### The probe (cross-boundary reader-model)

`core/dramatic_reader_model_client.py` — no code change. Four
behavioral modes still observed (architectural-finding,
implementation-refinement, bar-raising, bar-raising-through-
endorsement). Rashomon probe JSON chain now has **three** links:

- `reader_model_rashomon_output.json` — pre-LT12.
- `reader_model_rashomon_post_lt12_output.json` — post-sketch-03.
- `reader_model_rashomon_post_sc4_output.json` — **new since
  sketch-03** (`72dfdbe`), the scheduling-act arc's closing
  artifact.

The post-SC4 probe did not close the arc cleanly — it endorsed
the bandit and samurai SC4 verdicts and produced four new sketch
seeds (see "open, new" below). One seed was closed immediately by
throughline-lowering-scope-sketch-01; three remain.

**Not yet run:** a probe against the new Aristotelian dialect
(`oedipus_aristotelian.py`, `rashomon_aristotelian.py`). A probe
on a new dialect is itself a signal — does the reader-model
engage with the Aristotelian surface on its own terms, or try to
translate back into Dramatica / substrate? Candidate state-of-play-
05 arc.

### The article

`articles/2026-04-18-timelock-or-optionlock.md`, published 2026-
04-18 — unchanged. The Rashomon hypothesis it raised in Section 8
has now cycled: probe → sketch-03 → probe → scheduling-act-
utterance-sketch → probe → throughline-lowering-scope-sketch +
aristotelian-sketch.

### Infrastructure

Unchanged from sketch-03: package structure (`story_engine/{core,
encodings,tools}/` + `tests/`, `demos/`), skeleton generator
(`story_engine/tools/skeleton.py`), probe JSONs at `prototype/`
root.

---

## Shift-point test result

The headline finding of this arc. State-of-play-03 flagged the
shift-point question: *is the substrate / dialect stack stable
enough that the Python code is ready to be treated as a spec, per
the "Python is a spec language" discipline (memory
`feedback_python_as_spec`)?*

Aristotelian-sketch-01 was written as a **deliberately falsifiable
test** of that stability. Methodology: Aristotle's *Poetics*
predates Dramatica by ~2400 years and was written describing a
specific theatrical tradition; it brings primitives (peripeteia,
anagnorisis, hamartia, catharsis, three unities) that *could*
have required substrate-level changes (fortune-state, audience-
response, structural reversal semantics). If architecture-sketch-
02's claim that Dramatica is one Template among many is right, an
Aristotelian dialect lands with no core-record modification, on
the pattern Save-the-Cat set. If it forces modification, the
architecture isn't yet stable.

**Three test predictions:**

1. *Design phase:* every commitment A1–A9 classifies as *extension*
   (new Template records, new verifier-local checks over existing
   substrate predicates, new annotations). **GREEN** (`f4a03ec`):
   all nine commitments extension-only; stress points on
   peripeteia, anagnorisis, hamartia, unity of time / place,
   catharsis all navigated by existing architecture.

2. *Implementation phase (Oedipus):* code lands in new files only;
   no change to any existing core record; Oedipus verifies clean.
   **GREEN** (`a3a09a8`): three new files
   (`aristotelian.py`, `oedipus_aristotelian.py`,
   `test_aristotelian.py`); `git status` confirms zero
   modifications to any pre-existing file; Oedipus verifies with
   0 observations.

3. *Implementation phase (Rashomon stress):* multi-mythos encoding
   slots in without sketch modification. **GREEN** (`1949277`):
   four `ArMythos` records, 0 observations each; no new record
   type in `aristotelian.py`; no sketch amendment.

All three cleared. **The shift-point signal is confirmed.** The
architecture held under a deliberate, theory-informed stress test
— not just "we didn't stress it." Two dialect-scope limits
surfaced honestly (meta-anagnorisis at A8-class; contested-mythos
relations as potential `ArMythosRelation` extension) and neither
forced code change.

**What this means for the project:**

- The Python code is spec-ready in the sense architecture-sketch-
  02 claimed. Porting (roadmap item 4 — DSL, Ragel-G2, recursive-
  descent, C++) is now a reasonable forcing function rather than a
  premature one.
- Research can continue in parallel — the shift-point is not a
  binary switch. Open findings from the post-SC4 probe remain; the
  probe itself continues to find seeds; sketch-02 OQs bank for
  future forcing functions.
- Production-direction work (roadmap items 1–3, 5, 6) is now first-
  class candidate next work, alongside further research.

---

## What the probe has revealed (closed since sketch-03)

Two closures — one implemented, three banked for later.

### Closed by implementation

- **Throughline-lowering scope (two NEEDS_WORK annotation-review
  findings from `72dfdbe`)** → closed by throughline-lowering-
  scope-sketch-01 (`8c8358e`). TL1–TL4 codify the distinction
  between `Throughline.subject` (interpretive) and
  `Lowering.lower_records` (structural); branch-scoped testimony
  Throughline Lowerings are admitted; annotation-explicit scoping
  required when the distinction makes scope non-obvious. Two
  annotation-text edits on `L_bandit_mc_throughline` and
  `L_wife_mc_throughline`. No schema change.

### Banked (sketch-02 forcing-function criteria; not closed)

Three post-SC4 probe seeds opened as sketch-02 pending and not
acted on:

- **Bandit refinement: MC-mediated endpoint substitution.** Probe
  qualifies DSP_bandit_limit's APPROVED 0.5 by proposing a
  distinction between "scheduling predicates that name the
  endpoint directly" vs. "scheduling predicates whose demanded
  endpoint is transformed by the MC's agency" (wife requests
  killing; bandit realizes duel). Banked; sketch-02 or sibling
  sketch when sketched.
- **OQ2 reshaped (wife): prose-carried temporal drivers.** Probe
  qualifies DSP_wife_limit's NOTED 0.5 by proposing a
  flag-Timelock-declared-stories-whose-driver-is-Lowering-
  identified-as-prose-carried check. Sharpens sketch-01's OQ2 from
  "situational_forcing" into a concrete Lowering-annotation
  signal.
- **OQ1 reshaped (woodcutter): cross-branch signature detector.**
  Probe qualifies DSP_woodcutter_limit's NOTED 0.5 by proposing a
  cross-branch pattern: "when the same participant role initiates
  an utterance event at the same τ_s across branches, and each
  branch's arc ends in the same outcome, the utterance may
  function as a scheduling predicate even without explicit
  scheduling semantics." Reshapes sketch-01's OQ1 from
  `provoked_*`/`goaded_*` prefix extension into a cross-branch
  pattern detector — architecturally different; per-Story → cross-
  Story verification.

## What the probe has revealed (open, new since sketch-03)

None not already enumerated above. The post-SC4 probe is the
single open-finding source since sketch-03; its four seeds are
either closed (throughline-lowering-scope) or banked (three
above).

---

## What's next (research AND production)

For the first time, the "What's next" list branches into two
orthogonal tracks. Both are first-class candidates.

### Research track

In the order I'd work them:

1. **Probe the Aristotelian encodings.** The reader-model client
   has only ever seen Dramatic / Dramatica-complete. How does it
   react to an `ArMythos` + four-mythos Rashomon surface? The
   probe's own read of the new dialect is itself data. Likely
   short — the dialect is narrower than Dramatica, so probe
   commentary will be crisper. Candidate for an aristotelian-
   probe-sketch-01 closing artifact.
2. **Close one of the three banked scheduling-act-family seeds.**
   OQ2 reshaped (prose-carried drivers, wife) is the smallest
   because the probe supplied a concrete signal (the Lowering
   annotation explicitly says "prose-carried"). OQ1 reshaped
   (cross-branch signature, woodcutter) is the largest and most
   architecturally novel. Bandit-refinement (endpoint
   substitution) is middle-sized.
3. ***And Then There Were None* content fill.** The bootstrap
   docstring anticipates that authoring it will stress MN2
   (concealment-asymmetry) and LT8/LT9 for a `counted_*` /
   `enumerated_*` scheduling vocabulary. Large task.
4. **A seventh encoding under the Aristotelian dialect.** Macbeth
   would be the natural next — Shakespearean tragedy in an
   Aristotelian read. Ackroyd would be more interesting stress
   (narrator-as-murderer; Aristotle's character-level anagnorisis
   doesn't fit cleanly — would confirm or break the meta-
   anagnorisis scope-out from the sketch's A8 class).

### Production track (memory `project_longterm_roadmap`)

For the first time, available *because* the shift-point signal is
GREEN:

A. **Prose export round-trip starter** (roadmap item 3). Pick one
   Rocky scene; author a tight LLM prompt that produces prose
   given the substrate + Descriptions; see whether a reader can
   reconstruct the substrate from the prose. If yes → substrate is
   expressive enough for the "prose" step of the 5-step author
   flow (memory `project_expert_system_goal`). If no → the
   reconstruction gap is architectural feedback. Either outcome is
   useful.
B. **Goodreads import prototype** (roadmap item 2). Pick a
   Goodreads review / summary of a work not in the corpus (or
   maybe pick a work already in the corpus, like Rocky, to
   validate LLM-from-external-source against authored-from-
   scratch). Structured LLM prompt driving the skeleton generator
   + initial substrate population. LLM-heavy; structured help is
   where the dialect stack earns production-facing value.
C. **Markdown fenced-section parser** (roadmap item 1). Author-
   document-surface-sketch-01 is the sketch that already exists in
   the Cross-cutting section. Parser concretizes the sketch.
   Depends on (A) indirectly — parser is the author-in, prose
   export is the author-out.
D. **Port work** (roadmap item 4). Largest, most definitive
   forcing function. Premature until (A) or (B) has surfaced any
   remaining spec gaps. Candidate state-of-play-05+ work.

### My recommendation if asked

The post-SC4 probe-closure work (research) and roadmap item (A) —
prose export round-trip starter — are both cheap. Doing one each
would keep both tracks warm without committing to one over the
other.

---

## Context-economy discipline (for cold-start continuity)

Rules unchanged from sketch-03. Validated again:

- **Sketches before implementation.** aristotelian-sketch-01
  landed design-first (`f4a03ec`) with commitments A1–A9 classified
  by expected architecture impact; implementation-second
  (`a3a09a8` + `1949277`) confirmed the design-phase classification
  empirically. The discipline produces real falsifiability.
- **Worked cases + stress cases.** aristotelian-sketch-01 had
  both. Oedipus (native-fit confirmation) + Rashomon (deliberate
  stress); the combination is sharper than either alone.
- **Deferral as a sketch.** Three banked post-SC4 seeds continue
  the pattern (enabling-retraction-preservation-sketch-01 was the
  first). Findings enumerated with revisit criteria; not dropped;
  not prematurely implemented.
- **State-of-play at milestone boundaries.** This doc.
- **Commit messages are cross-session artifacts.** Every commit
  since `72dfdbe` carries substantive dense records. Keep writing.
- **Prefer Grep / Read-slice over full Read** when the target is
  known. Reserve full Read for unfamiliar files.
- **Spawn Explore agents aggressively** for 3+-query research.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic (now includes
   Aristotelian under dialect sketches; Throughline-lowering-scope
   under the post-LT12/SC4 probe-closing cluster).
2. This doc (`design/state-of-play-04.md`) — current corpus + open
   findings + shift-point test result.
3. `articles/2026-04-18-timelock-or-optionlock.md` — the paper.
4. `git log --oneline -30` — recent commits.
5. `design/aristotelian-sketch-01.md` — the architecture-stability
   test write-up. Both the test and the result live there.
6. The latest probe JSON
   (`reader_model_rashomon_post_sc4_output.json`) until a probe
   against the Aristotelian dialect runs.
