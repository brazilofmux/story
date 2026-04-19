# State of play — sketch 05

**Status:** active
**Date:** 2026-04-19
**Supersedes:** [state-of-play-04](state-of-play-04.md)

Cold-start orientation doc, rewritten (not amended) at the close
of the first Aristotelian-probe arc. Three commits since sketch-
04 consumed the Research-track item #1 (probe the Aristotelian
encodings) plus its design-first / implementation-second /
live-runs-third structure:

- `3f13af1` — aristotelian-probe-sketch-01 (design; five
  falsifiable predictions).
- `e6a89c7` — probe implementation (APA1–APA5): three additive
  records in `aristotelian.py`; `aristotelian_reader_model_
  client.py`; 23 tests; two demo scripts. Zero modifications to
  any pre-existing file outside `aristotelian.py`.
- `6d70199` — APA6 live probe runs: two opus-4-6 invocations
  (Oedipus baseline, Rashomon four-mythoi stress). Two JSON
  artifacts land (`reader_model_oedipus_aristotelian_output.
  json`, `reader_model_rashomon_aristotelian_output.json`).
  Zero DroppedOutputs.

**Headline:** the probe ran clean on its committed surface.
Three of five predictions (P3/P5, and P4 in spirit) passed; two
(P1/P2 by metric) failed *substantively* — the probe caught real
encoding issues the sketch hadn't anticipated. The probe
surfaced **five dialect-extension proposals** (ArMythosRelation,
ArFrameMythos, ArAnagnorisisLevel, ArAnagnorisisChain,
ArPeripeteiaAnagnorisisBinding) across the two runs, converting
sketch-01 A8's single flagged extension into a five-item banked
list for a hypothetical aristotelian-sketch-02.

**Re-write this sketch** (don't amend — write sketch-06) at the
next milestone.

---

## What is built — delta from sketch-04

### The dialect stack (no structural change)

All four upper dialects unchanged. `aristotelian.py` gained three
**additive** probe-surface records — ArAnnotationReview,
ArObservationCommentary, DialectReading — per aristotelian-
probe-sketch-01 APA1. No modification to ArMythos, ArPhase,
ArCharacter, ArObservation, or `verify`. The constants duplication
(VERDICT_*, ASSESSMENT_*) matches `verification.py`'s precedent
for dialect-independence.

substrate, dramatic, dramatica_template, save_the_cat, lowering,
verification, verifier_helpers — **all unchanged**. Now three
state-of-play boundaries (03 → 04 → 05) and eight commits without
substrate or core-dialect modification, including through a
deliberate architectural-stability test (aristotelian-sketch-01)
AND a behavioral-stability test (this arc's probe).

### The probe stack

**New module** `core/aristotelian_reader_model_client.py` mirrors
`dramatic_reader_model_client.py`'s pattern — typed I/O,
scope-declared invocation, translation to dialect-native records,
DroppedOutput audit surface. The Aristotelian client is
dialect-isolated (APS1): no Dramatic / Dramatica-complete /
Save-the-Cat records appear in the prompt even on encodings that
have them.

Three output kinds (APS2):

- **AristotelianAnnotationReview** → ArAnnotationReview. Per-
  field verdict on prose (ArMythos.action_summary,
  ArPhase.annotation, ArCharacter.hamartia_text).
- **ObservationCommentary** → ArObservationCommentary. Zero
  on both runs (both encodings verify clean); shape validates
  for future encodings.
- **DialectReading** → DialectReading. One per invocation.
  Captures the methodological signal "did the LLM engage on
  the dialect's terms?" — unique to this probe; no analog in
  the dramatic client.

Three render helpers, three classifiers, three translators, a
unified `translate_raw_output` entry for tests and cached-output
re-translation.

### The encodings (unchanged)

Five fully-verified works: Oedipus, Macbeth, Ackroyd, Rocky,
Rashomon. Aristotelian-layer encodings: Oedipus (single mythos)
+ Rashomon (four mythoi). Sixth encoding bootstrapped (And Then
There Were None) — still skeleton. Dialect-only: Chinatown, Pride
and Prejudice, Turn of the Screw.

Test surface: **707 standard tests** (was 621 pre-probe; +23
new probe-client + 0 from the dialect records — additive records
carry no tests on their own data shape beyond Pydantic's parse
validation). **40 venv-gated tests** unchanged shape-wise.

### The probe (cross-boundary reader-model)

`core/dramatic_reader_model_client.py` — unchanged since sketch-
04. Four behavioral modes unchanged. Its Rashomon JSON chain
still has three links; the post-SC4 probe's three banked seeds
(bandit endpoint-substitution, wife prose-carried drivers,
woodcutter cross-branch signature) remain banked.

**First-ever Aristotelian probe JSON chain:**

- `reader_model_oedipus_aristotelian_output.json` — 6 annotation
  reviews (4 approved, 2 needs-work); DialectReading with
  read_on_terms="yes" and two relation proposals.
- `reader_model_rashomon_aristotelian_output.json` — 20
  annotation reviews (15 approved, 5 needs-work); DialectReading
  with read_on_terms="partial", four scope_limits_observed,
  three relation proposals, and a grounded `drift_flagged` list
  used as the audit surface APS3 described.

### Infrastructure

Unchanged.

---

## Shift-point test — refined reading after the probe arc

Sketch-04 declared the shift-point signal GREEN on the basis of
the architectural-stability test (sketch-01 + its implementation).
The probe arc adds a **behavioral** stability test: does the
dialect hold up when an interpretive peer reads it? The probe
produced five extension proposals — superficially that looks like
instability. But examine each:

- **ArMythosRelation**: sketch-01 A8 already flagged it as a
  candidate sketch-02 extension if a forcing function appeared.
  The probe IS the forcing function; this is extension-on-
  schedule, not surprise pressure.
- **ArFrameMythos**: new envelope-mythos record. Still additive:
  a new record type, not a modification to ArMythos or phases
  or characters.
- **ArAnagnorisisLevel**: a modifier/field distinguishing
  character-level from audience-level. Whether it's a new
  optional field on ArMythos or a new enum constant depends on
  sketch-02's design; both shapes are extensions, not
  modifications.
- **ArAnagnorisisChain**: multi-anagnorisis within one mythos.
  Structurally the same shape question as ArMythosRelation —
  a new relation record, not a modification of existing ones.
- **ArPeripeteiaAnagnorisisBinding**: structural declaration
  replacing a prose-level claim. Small additive record or
  optional field on ArMythos.

**Zero substrate pressure. Zero core-dialect-record modification
pressure.** Every extension would be an additive record type or
an optional field on an existing record — the same pattern Save-
the-Cat's StcCharacter followed (sketch-02 S9–S11) and
aristotelian-sketch-01 itself followed across A1–A9.

**Verdict — shift-point signal remains GREEN.** The dialect's
scope is narrower than the probe wants it to be, which is a
feature, not a break — the probe produced a sized, specific,
sketch-shaped extension list. That's the architecture
*working*, not the architecture *straining*. A real break would
have looked like: "the probe asked for a new substrate predicate
to represent X"; none did.

**What the probe arc clarified about the shift-point question:**
stability claims operate on two axes. Architectural-stability
(sketch-04's axis) asks "can the dialect stack be written
without substrate pressure?" — verified in sketch-01. Behavioral-
stability (this axis) asks "does the dialect hold up when read?" —
verified here, with sized additive pressure that stays on its
own layer. Both greens; production-direction work remains first-
class candidate.

---

## What the probe has revealed (arc outcomes)

### Encoding-side findings (five banked, two Oedipus + three Rashomon prose cleanups)

**Oedipus, 2 findings:**

- `ar_oedipus.action_summary`: "Recognition coincides with
  reversal" asserts a structural coincidence the encoding's
  own fields (peripeteia_event_id=E_messenger_adoption_reveal
  at τ_s=8; anagnorisis_event_id=E_oedipus_anagnorisis at
  τ_s=13; five substrate steps apart) contradict. Aristotle's
  *hama* (Poetics 1452a) is a qualitative dramatic claim, not
  a substrate-adjacency claim. Author walks and decides whether
  to amend the prose or flag the dramatic-vs-substrate
  distinction explicitly.
- `ar_jocasta.hamartia_text`: two errors. (a) Claims Poetics
  1453a groups Jocasta with Oedipus as a "secondary figure
  contributing to peripeteia" — Aristotle cites Oedipus /
  Thyestes only. (b) Causal direction: encoding has peripeteia
  at τ_s=8 preceding E_jocasta_realizes at τ_s=9; Jocasta's
  fall *follows from* the reversal, not "contributes to" it.

**Rashomon, 5 findings** — all cite cross-references to other
encoding layers (Descriptions, Lowering annotations, throughline-
lowering-scope-sketch-01 TL2) or non-Aristotelian vocabulary
("narrative temporal driver", "meta-epistemic arc") in phase
annotations. Specific targets: `ph_b_beginning`, `ph_w_beginning`,
`ph_w_middle`, `ph_h_beginning`, `ph_wc_end`. All are author-
discipline issues (the Aristotelian annotations shouldn't lean
on other dialect layers); none requires dialect change.

**Collectively:** 7 grounded probe findings on authored prose,
0 requiring dialect change. The probe does its job.

### Dialect-extension proposals (five banked for aristotelian-sketch-02)

Enumerated above in the shift-point section. The sketch-02
forcing-function discipline (enabling-retraction-preservation-
sketch-01 EP-style) would evaluate each proposal against:

- **Concrete downstream consumer?** ArMythosRelation has one
  (multi-mythos encoding contest-expression). ArFrameMythos has
  one (Rashomon frame). ArAnagnorisisLevel / Chain / Binding
  have *probe-proposed* consumers but no committed ones yet.
- **Second encoding exhibits the pattern?** Macbeth-Aristotelian
  and Ackroyd-Aristotelian are unauthored; either could provide
  a second instance (or could show the probe proposals don't
  generalize).
- **Authoring a case that requires the extension?** And Then
  There Were None under Aristotelian (if authored) might
  pressure ArMythosRelation (ten deaths as linked mythoi?) or
  ArAnagnorisisLevel (the reader's dawning realization is
  audience-level).

None holds today for all five. Two (ArMythosRelation,
ArFrameMythos) hold partially.

### Scope-limits observed (four banked)

Beyond meta-anagnorisis (which the sketch-01 analysis predicted):

- **Catharsis across competing mythoi** — work's cathartic
  effect emerges from testimony-friction; `aims_at_catharsis`
  is a per-mythos flag with no aggregate.
- **Narrator-as-tragic-hero** — woodcutter as self-
  incriminating narrator; Poetics 1448a's mode distinction
  (poet-in-his-own-person) is not a character-function; the
  dialect can't model the collapse.
- **Coincidence vs. adjacency** — Aristotle's *hama* is
  qualitative dramatic; dialect has no distinction between
  "same dramatic beat" and "same substrate step".
- **Testimony-specific event texture** — shared substrate event
  carries different significance per mythos; dialect can only
  repeat the event_id across mythoi, not express per-mythos
  reading.

Each informs a future sketch (arifrtotelian-probe-sketch-02 or
aristotelian-sketch-02) if a second encoding pressures.

### Closed since sketch-04

Nothing from sketch-04's banked lists closed; this arc was
entirely the probe.

---

## What's next (research AND production)

### Research track

In the order I'd work them:

1. **Encoding-side prose cleanup.** Two Oedipus edits + five
   Rashomon phase-annotation edits. Grounded, contained, no
   dialect change, minimal scope. Good candidate for the
   *smallest* next research step — closes the probe-surfaced
   findings immediately. Parallel to the throughline-lowering-
   scope-sketch-01 closing commit (`8c8358e`) in shape.
2. **Close one of the three banked scheduling-act-family
   seeds** (sketch-04 carried these forward unchanged).
   OQ2-reshaped (wife prose-carried drivers) remains the
   smallest; OQ1-reshaped (woodcutter cross-branch signature)
   remains the largest and most architecturally novel.
3. **Aristotelian-probe-sketch-02 candidate** — a refinement
   sketch addressing APS6 P4's metric (`drift_flagged` is the
   audit surface, not a tripwire) + a second probe run on a
   newly-authored Macbeth-Aristotelian or Ackroyd-Aristotelian
   encoding. The metric-refinement is small; the second probe
   run needs an encoding first.
4. **Aristotelian-sketch-02** — evaluate the five probe-
   surfaced relation proposals against the EP-style forcing-
   function criteria. Author decides which earn inclusion.
5. **A seventh encoding under the Aristotelian dialect**
   (Macbeth or Ackroyd). Provides the second instance the
   sketch-02 forcing functions need. Macbeth is the natural
   native-fit case; Ackroyd is more stressful (narrator-as-
   murderer, narrator-as-tragic-hero overlap).
6. **And Then There Were None content fill.** Unchanged from
   sketch-04. Large task.

### Production track (memory `project_longterm_roadmap`)

Unchanged from sketch-04. None touched this arc.

A. **Prose export round-trip starter** (roadmap item 3). Rocky
   scene; LLM prompt; reconstruction test. Still the smallest
   concrete production step.
B. **Goodreads import prototype** (roadmap item 2). Same.
C. **Markdown fenced-section parser** (roadmap item 1). Same.
D. **Port work** (roadmap item 4). Same — still premature
   before (A) or (B) surface spec gaps.

### Recommendation

State-of-play-04's recommendation — do one research item and one
production item to keep both tracks warm — still holds. Research
track's cheapest: item #1 (prose cleanup of 7 probe findings).
Production track's cheapest: item (A) (prose-export starter).
Either or both would continue the arc cleanly.

**The returnable question** (state-of-play-04 opened; still
open): **which track gets the next serious commit?** Two arcs in
a row have been research. The shift-point signal is twice-
confirmed (architectural + behavioral). Production-direction
work is overdue a concrete first step.

---

## Context-economy discipline (for cold-start continuity)

Rules unchanged from sketch-04. Validated again:

- **Sketches before implementation.** aristotelian-probe-
  sketch-01 landed design-first (`3f13af1`) with predictions
  APS6 P1–P5 stated *before* runs; implementation (`e6a89c7`)
  honored the sketch; live runs (`6d70199`) measured outcomes
  honestly against the stated predictions (P1/P4 failed by
  metric and the commit message says so).
- **Worked + stress cases.** Oedipus (native fit) + Rashomon
  (four-mythoi stress). Same pair structure as the parent
  sketch-01.
- **Deferral as a sketch** (implicit). Five relation-extension
  proposals banked for aristotelian-sketch-02 under the EP-
  style forcing-function criteria.
- **State-of-play at milestone boundaries.** This doc.
- **Commit messages are cross-session artifacts.** The three
  probe-arc commits run dense (382 + 687 + 1047 tokens in the
  body); any cold-start Claude reading `git log --oneline -10`
  can reconstruct the arc.
- **Prefer Grep / Read-slice over full Read** when the target
  is known.
- **Spawn Explore agents aggressively** for 3+-query research.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic.
2. This doc (`design/state-of-play-05.md`) — current corpus,
   open findings, shift-point state, research vs. production
   tracks.
3. `articles/2026-04-18-timelock-or-optionlock.md` — the paper.
4. `git log --oneline -30` — recent commits. The three probe-
   arc commits (`6d70199`, `e6a89c7`, `3f13af1`) carry dense
   bodies worth reading in full.
5. `design/aristotelian-probe-sketch-01.md` — the probe's
   falsifiable-predictions structure; useful precedent for
   future probe sketches against other dialects.
6. `design/aristotelian-sketch-01.md` — the dialect the probe
   reads.
7. The latest probe JSONs
   (`reader_model_oedipus_aristotelian_output.json`,
   `reader_model_rashomon_aristotelian_output.json`) — first
   Aristotelian probe output; the relation-extension proposals
   live here verbatim.
