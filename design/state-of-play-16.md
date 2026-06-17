# State of play — sketch 16

**Status:** active
**Date:** 2026-06-16
**Supersedes:** [state-of-play-15](state-of-play-15.md)

Single-arc refresh marking the **Revenger's Tragedy encoding arc**
(five sessions, `6693c6c`→`da79992`) — authored start to finish in one
working session to force **OQ-MALFI-3** (pathos-hero vs arc-hero split),
the strongest finding the Malfi Session-6 re-probe surfaced. The
headline: the methodology's full new-finding loop — *surface a finding
in one encoding → author a structurally-harder second-site encoding →
the probe confirms it and proposes the field shape* — has now run end
to end for a second time (OQ-LEAR-4 → sketch-06 was the first), and
this time the loop closed inside a single session.

Five commits since SoP-15 (`6ee5908..HEAD`), all 2026-06-16:

- `6693c6c` — Session 1: substrate skeleton (19 entities, 31 events,
  τ_s=-90..22).
- `c4fe422` — Session 2: Aristotelian overlay (verifies clean; the
  OQ-MALFI-3 stretch).
- `1c038c2` — Session 3: substrate completion (the focalization
  surface).
- `6561249` — Session 4: 15 encoding tests.
- `da79992` — Session 5: the live probe — OQ-MALFI-3 forced decisively.

## Headline — three load-bearing claims

### 1. OQ-MALFI-3 is cross-encoding CONFIRMED, with a probe-proposed shape

The Revenger's Tragedy presses the pathos/arc-hero split harder than
Malfi on three axes: **total split** (Vindice the avenger is morally
corroded and hard to pity, so the pathos has nowhere to live but the
violated women); **non-agentive pathos-centre** (Gloriana is dead
before the play and present only as a skull-prop); **distributed
pathos** (Gloriana + Antonio's wife). The split is carried under
*semantic stretch* — the dialect can author Gloriana as an ArCharacter
but has no field to mark her as the mythos's pathos-centre, so the
claim lives in annotations and an overloaded `kind="parallel"` relation
(the OQ-LEAR-4 / A19 pattern before sketch-06).

The Session-5 probe (`reader_model_revengers_aristotelian_output.json`)
read the encoding fully on dialect terms (`read_on_terms=yes`, drift
empty, 7/8 approved, 0 rejected) and surfaced the pathos-centre gap as
the **only** vocabulary strain. It independently proposed both of the
encoding's recommended shapes — **`ArMythos.pathos_character_ref_ids`**
(explicitly a LIST/tuple, matching option 1 over the singular) and
**`ArCharacter.pathos_carrier: bool`** — recognised all three forcing
axes including the stretch itself ("forced to overload
ArCharacterArcRelation as a workaround"), and grounded the gap in
Aristotle's own pathos (*Poetics* 1452b: "a structural-field gap, not a
vocabulary failure"). **sketch-07 is now well-forced**, with the same
design→implement→re-probe loop available that sketch-06 just ran.

### 2. The design-first → probe-falsifies rhythm recurs at the OQ-prediction layer (now a stable phenomenon)

The encoding predicted that Vindice's belated, self-destroying main
recognition ("'Tis time to die when we are our own foes") would force
**S6P-OQ1** — a main-level `anagnorisis_qualifier` (A20 types qualifiers
on chain steps only). The probe did **not** bear this out: it read the
main anagnorisis as clean and correct, with no demand for a qualifier.
S6P-OQ1 stays **banked unforced**.

This is the third consecutive instance of the rhythm operating at the
OQ-prediction layer (SoP-15's "fourth arena"): sketch-06 pre-banked
S6P-OQ1 and S6P-OQ2, both unforced; the Revenger's arc predicted
S6P-OQ1 again, unforced. The pattern is now stable enough to state as a
working rule: **forecasting which next-layer pressure a probe will
surface is reliably falsifiable, and the forecasts are wrong as often
as right.** Pre-banked next-OQs are hypotheses for the probe to test,
not roadmap. (OQ-MALFI-3, by contrast, was *surfaced by a probe* before
being re-forced by one — and it held. The asymmetry is informative:
probe-surfaced findings re-confirm; author-predicted ones often don't.)

### 3. A full second-site encoding now fits in one session

The Revenger's arc — substrate skeleton, dialect overlay, substrate
completion, 15 tests, and a live probe with findings + a probe-surfaced
refinement — was authored, verified, and committed across five
sessions in a single working span. The Malfi arc (the OQ-LEAR-4 forcer)
took five sessions across a calendar gap; the corpus's encoding
machinery (the substrate/overlay/probe triple, the format precedents,
the verify-clean bar) is now mature enough that a new forcing encoding
is a session's work, not a month's. This lowers the cost of the
core research move (author a second site to force a banked finding) and
makes the loop repeatable on demand.

---

## What is built — delta from sketch-15

### Two new encoding modules (the corpus's 7th Aristotelian encoding)

- `prototype/story_engine/encodings/revengers_tragedy.py` — substrate
  (Sessions 1+3): 19 entities, 31 events, 5 preplay disclosures, 28
  sjuzhet entries, 9 descriptions. The focalization surface is itself
  an OQ-MALFI-3 datum: Vindice (arc-hero) focalizes 13/28; the
  pathos-cluster focalizes near-zero (Gloriana 0, Antonio's wife 0,
  Castiza 1) — the pathos-centre cannot focalize because she is dead
  and a prop, the structural inverse of Malfi's focal-pathos-bearer.
- `prototype/story_engine/encodings/revengers_tragedy_aristotelian.py`
  — overlay (Session 2): 1 mythos, 3 phases (10+10+11), 7 characters
  (1 tragic hero, Vindice — the corpus's lean case), 2 parallel
  relations, a 1-step anti-anagnorisis chain, sketch-04 fields.
  Verifies clean (0 observations — corpus-cleanest). Carries
  `OQ_MALFI_3_FINDING` (CONFIRMED) and `S6P_OQ1_FINDING` (NOT FORCED).
- `prototype/demos/demo_aristotelian_reader_model_revengers.py` +
  `prototype/reader_model_revengers_aristotelian_output.json` — the
  Session-5 probe instrument and artifact.

### Dialect ledger — unchanged (A1–A21)

This arc *forces* sketch-07 but does not land it. The dialect is
untouched; the encoding presses on the absence of a pathos field, it
does not add one.

### Bonus corpus contributions (confirmed by the probe)

- **A20 `anti` generalised** to a second encoding — the Duke's dying
  recognition (a villain's too-late recognition, where Webster's
  Antonio was a victim's). The probe: "carries it without strain."
- **BINDING_ADJACENT** — the corpus's first use of the ADJACENT cell
  (peripeteia τ_s=20, anagnorisis τ_s=21, distance 1; the narrowest
  binding in the corpus). Read cleanly.

### Test surface

- **test_aristotelian: 222** (+15 Revenger's tests over SoP-15's 207).
  Full stdlib core sweep + conformance + reader-model client remain
  green (1069+ total).

---

## The banked-findings ledger after this arc

- **OQ-MALFI-3** — pathos field. **CONFIRMED cross-encoding, shape
  proposed.** sketch-07 candidate (land `pathos_character_ref_ids`
  tuple; Malfi migrates `(ar_duchess,)`, Revenger's `(ar_gloriana,
  ar_antonio_wife)`).
- **S6P-OQ1** — main-level anagnorisis_qualifier. **Banked UNFORCED**
  (predicted by sketch-06 and by this arc; both falsified). Needs a
  tragedy whose MAIN recognition is unambiguously anti.
- **OQ-MALFI-4** — instrument-reversal event. Banked; not re-pressured
  here (Vindice is self-directed, not a wielded instrument).
- **OQ-MALFI-1B** — temporal mode on concordant instrumentals. Banked
  (Malfi-surfaced; awaits a third concordant-instrumental encoding).
- **OQ-AP7** — range-of-separated. Conjectural (the Revenger's adds the
  ADJACENT cell but does not pressure the SEPARATED range).

---

## What's next (research AND production)

### Research track

1. **aristotelian-sketch-07 — land OQ-MALFI-3.** The well-forced
   candidate: `ArMythos.pathos_character_ref_ids` (tuple), optionally a
   companion `ArCharacter.pathos_carrier` flag, plus a self-verifier
   check (each ref resolves; distinct from anagnorisis is allowed not
   required; admits arc-less referents). Migrate Malfi + Revenger's;
   re-probe both to verify closure. Mirrors sketch-06 exactly.
2. **S6P-OQ1 second-site search.** A tragedy whose MAIN recognition is
   anti/partial (an avenger who recognises the wrong target as he
   kills; a protagonist whose central recognition is delusion). Banked
   until a clean site appears.
3. **Compiler stage-3 sketch-05 candidate / inert-scaffolding
   decision** — unchanged from SoP-15 (#4, #5).
4. **Further second-site encodings** for the remaining banked findings
   (OQ-MALFI-1B, OQ-MALFI-4) when forcing sites are identified.

### Production track

Unchanged from SoP-15: the sketch-06 schema fields are landed; the next
production candidate is a fresh schema/round-trip surface (markdown
author parser, prose-export round-trip, Goodreads import). Per
`feedback_research_production_alternation.md`, the last six commits are
research-mode (the Revenger's arc); a production swing — or
sketch-07's schema half — is the natural counter.

### Recommendation

**sketch-07** is the cleanest next move: OQ-MALFI-3 is the only banked
finding that is both probe-surfaced AND cross-encoding-confirmed with a
proposed shape, which is exactly the maturity that justified sketch-06.
It carries its own production half (the schema-layer pathos field).
sketch-07 → re-probe both encodings is the loop that closes the
OQ-MALFI-3 question the way sketch-06 closed OQ-LEAR-4/MALFI-1/MALFI-2.

---

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketches-04 through -15, with one sharpening:

- **Probe-surfaced findings re-confirm; author-predicted next-OQs
  often don't.** OQ-MALFI-3 (probe-surfaced in Malfi) was re-forced and
  held; S6P-OQ1/OQ2 (author-predicted in sketch-06 and this arc) were
  repeatedly unforced. When choosing a finding to invest a second-site
  encoding in, prefer one a probe has already surfaced unprompted.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic (the aristotelian
   index line stops at probe-sketch-03; sketches 03–06 and the Malfi /
   Revenger's encodings are not indexed there — read the files).
2. This doc (`design/state-of-play-16.md`) — current state.
3. `design/state-of-play-15.md` — supersedes-link; the Malfi arc +
   sketch-06 closure + the fourth rhythm-arena.
4. `design/aristotelian-sketch-06.md` — the latest *landed* dialect
   sketch (A19/A20/A21), incl. its Session-6 closure-result section.
5. `prototype/story_engine/encodings/revengers_tragedy_aristotelian.py`
   — the OQ-MALFI-3 forcer; `OQ_MALFI_3_FINDING` carries the confirmed
   result and the sketch-07 recommendation.
6. `prototype/reader_model_revengers_aristotelian_output.json` — the
   probe artifact proposing `pathos_character_ref_ids`.
7. `prototype/story_engine/core/aristotelian.py` — the dialect, A1–A21.
8. `git log --oneline 6ee5908..HEAD` — the five Revenger's commits
   between SoP-15 and SoP-16.
