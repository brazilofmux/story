# State of play — sketch 15

**Status:** active
**Date:** 2026-06-16
**Supersedes:** [state-of-play-14](state-of-play-14.md)

Catch-up refresh after **eight commits** in which SoP-14 went stale:
it was written the day **compilation-stage-3-sketch-04** landed and
predates the entire **Duchess of Malfi research arc** (five sessions)
and the **aristotelian-sketch-06** landing-plus-closure that this
session completed. The headline is a full research loop closing inside
one session — design → implement → live-probe-verify — and the
design-first → implementation-falsifies rhythm reaching a **fourth
arena**: the OQ-prediction layer.

Eight commits since SoP-14 (`49bb078..HEAD`), 2026-05-22 → 06-16:

- `20c74e7` — production-format-sketch-16: schema-layer landing for
  the sketch-03 A13/A14 + sketch-05 A17/A18 aristotelian fields.
- `761e9aa` — compilation-stage-3-sketch-04: the S4P-OQ3 forcing
  scene (phantom-operator inflates precondition risk); banked.
- `0b5e0e3` → `bce79c4` — the **Malfi arc**, Sessions 1–5: substrate
  skeleton → aristotelian overlay → substrate completion → encoding
  tests → live probe.
- `1dd728c` — **aristotelian-sketch-06**: A19/A20/A21 land; Malfi
  Session-6 re-probe verifies closure (this session).

## Headline — three load-bearing claims

### 1. The Malfi research arc completed and forced aristotelian-sketch-06

*The Duchess of Malfi* (Webster, 1612–13) was authored as the
**first cross-encoding instantiation of OQ-LEAR-4** (secondary
peripeteia for a mythos with multiple tragic arcs). It is the corpus's
sixth Aristotelian encoding (after Oedipus, Rashomon, Macbeth, Hamlet,
Lear) and its structurally densest: four arc-peripeteiai in one
mythos, a main anagnorisis belonging to the orchestrator (Ferdinand)
rather than the pathos-bearer (the Duchess), an anti-anagnorisis
(Antonio's dark-room death), and a sequentially-wielded instrument
(Bosola, passed Cardinal→Ferdinand→Cardinal).

The Session-5 live probe (`bce79c4`) was the **corpus's first
100%-approval run** (15/15 annotation reviews) and did the richest
possible thing: it **validated two banked forcing functions and
surfaced a third in the same run**, proposing concrete field shapes
for all three — `secondary_peripeteia_event_ids` (OQ-LEAR-4), a
`paired_polarity_concordance` check (OQ-MALFI-1), and an
`anagnorisis_qualifier` enum (OQ-MALFI-2, NEW).

### 2. Sketch-06 closed all three findings; the Session-6 re-probe verified it

`aristotelian-sketch-06` (`1dd728c`) lands three **extension-only**
commitments — architecture-sketch-02's stability test holds through
A21:

- **A19** `ArMythos.secondary_peripeteia_event_ids` + A7.17 (OQ-LEAR-4).
- **A20** `ArAnagnorisisStep.anagnorisis_qualifier` (`"" | genuine |
  anti | partial`) + A7.18 (OQ-MALFI-2).
- **A21** A7.15 check 6, paired-polarity-**concordance** — the sibling
  to sketch-05's contrast check, reusing its grouping (OQ-MALFI-1).

The load-bearing design idea: the dialect was already structurally
*complete* for Webster but **unevenly distributed** — the four
arc-peripeteiai were spread across the main slot, the main-anagnorisis
slot, two chain steps, and prose. A19 adds no expressive power; it
**redistributes the same information onto one uniform apparatus and
retires three semantic stretches**. The chain steps stay (they are
genuine recognitions); only their peripeteia content moves to A19.

The **Session-6 re-probe** (this session;
`reader_model_malfi_aristotelian_session6_output.json`) verified
closure end-to-end: the dialect_reading engages "secondary" and "anti"
as **live Aristotelian vocabulary**; the observation commentary
**endorses** the concordance check as "structurally load-bearing";
13/15 approved, 0 rejected, `drift_flagged` empty. Schema folded in
the same session (the layer is kept in sync through sketch-05).

### 3. The design-first → implementation-falsifies rhythm reached a fourth arena: OQ-prediction

SoP-14 recorded three arenas (probe-run, implementation-detail,
sketch-design). Sketch-06 adds a fourth. The sketch **pre-banked two
next-layer open questions** — S6P-OQ1 (main-level qualifier) and
S6P-OQ2 (secondary-peripeteia↔recognition binding) — as forecasts of
what the re-probe would surface once the surface findings closed. The
probe surfaced **neither**. It surfaced three different ones:

- **OQ-MALFI-3** — pathos-hero vs arc-hero split
  (`ArMythos.pathos_character_ref_id`). When the pity-centre (Duchess)
  ≠ the main-anagnorisis character (Ferdinand). Corpus-first; the
  strongest new finding.
- **OQ-MALFI-4** — instrument-reversal event
  (`ArCharacterArcRelation.instrument_reversal_event_id`): where the
  instrument turns on the wielder (Bosola kills Ferdinand).
- **OQ-MALFI-1B** — temporal mode on concordant instrumentals
  (`bracketing | continuous | episodic`): the probe independently
  re-proposed the OQ-MALFI-1 option-2/3 successor.

Recorded for future sketches: forecasting *which* next-layer pressure a
re-probe will surface is itself falsifiable, and was falsified here.
The probe's attention is genuinely exploratory; pre-banked next-OQs
are hypotheses, not roadmap.

---

## What is built — delta from sketch-14

### Aristotelian dialect ledger (now A1–A21)

- A1–A9 (sketch-01), A10–A12 (sketch-02), A13–A14 (sketch-03),
  A15–A16 (sketch-04), A17–A18 (sketch-05), **A19–A21 (sketch-06)**.
- Self-verifier: A7 checks 1–5 + A7.6–A7.9 + A7.10–A7.11 +
  A7.12–A7.14 + A7.15 (now **six** sub-checks, check 6 new) + A7.16 +
  **A7.17 + A7.18**.
- Six encodings verify clean: Oedipus, Rashomon, Macbeth, Hamlet,
  Lear, **Malfi**. All extension-only; sketch-01's architectural GREEN
  holds through A21.

### Files (this arc)

- `prototype/story_engine/encodings/malfi.py` — substrate (16
  entities, 34 events, SJUZHET, PREPLAY_DISCLOSURES, DESCRIPTIONS).
- `prototype/story_engine/encodings/malfi_aristotelian.py` — the
  overlay; now carries the sketch-06 migration + seven OQ-finding
  constants (`OQ_FINDINGS`), three CLOSED + three NEW + OQ-AP7.
- `prototype/story_engine/core/aristotelian.py` — A19/A20/A21
  implementation (+213 lines this commit).
- `prototype/story_engine/core/aristotelian_reader_model_client.py` —
  renders the sketch-06 fields + a sketch-06 system-prompt paragraph
  (the Session-6 re-probe precondition).
- `prototype/story_engine/encodings/lear_aristotelian.py` — A19
  migration (Gloucester's blinding as secondary peripeteia).
- `schema/aristotelian/{mythos,anagnorisis_step}.json` — A19/A20
  fields (AS06-1, AS06-2).
- `design/aristotelian-sketch-06.md` — the sketch as landed, with the
  Session-6 closure-result section.
- `prototype/reader_model_malfi_aristotelian_{,session6_}output.json` —
  the Session-5 and Session-6 probe artifacts.

### Test surface

- **1069 tests passing, 0 failing**: 923 stdlib core (14 files) + 107
  production-format conformance (venv) + 39 aristotelian reader-model
  client (venv). `test_aristotelian.py` is now **207** (+18 sketch-06).

---

## What's next (research AND production)

### Research track

1. **OQ-MALFI-3 (pathos-hero vs arc-hero split)** — strongest new
   finding; `ArMythos.pathos_character_ref_id`. Forcing function: a
   second split-pathos encoding (a revenge tragedy where the avenger
   recognizes but a victim bears the pathos). The natural sketch-07
   candidate if a second site is authored.
2. **OQ-MALFI-4 + OQ-MALFI-1B (instrumental-relation enrichment
   cluster)** — instrument-reversal event + temporal mode. Pair
   naturally; both forced by a second instrument-character encoding.
3. **OQ-AP7 (range-of-separated)** — three encodings (Hamlet 9, Lear
   14, Webster 6) under one `separated` category. Reclassified
   conjectural; the Session-6 probe read all three without structural
   discomfort. Banked.
4. **Compiler stage-3 sketch-05 candidate** — pressure-test the
   precondition-risk sort (S4P-OQ3 banked a phantom-operator forcing
   case at `761e9aa`; insertion-search is the next escalation if a
   real over-defer case appears). Unchanged from SoP-14 #4.
5. **Compiler inert-scaffolding decision (S4P-OQ4)** — threat-
   resolution primitives still inert two increments on; removal is the
   default. Unchanged from SoP-14 #7.
6. **Multi-session arc candidates** — Marlowe's *Edward II*,
   Tourneur's *Revenger's Tragedy* remain the OQ-LEAR-4-adjacent /
   OQ-MALFI-3 pool.

### Production track

- **PFS17+** — the sketch-06 schema fields folded into the existing
  files this session, so no separate PFS arc is owed for them. The
  next production candidate is a fresh schema/round-trip surface
  (markdown-fenced author parser, prose-export round-trip, Goodreads
  import) — all unchanged from SoP-14's roadmap list.

### Recommendation

Per `feedback_research_production_alternation.md`: the last commit
(`1dd728c`) is research-leaning (probe arc) but **already carried its
own production half** (schema + conformance). The cleanest next move is
**OQ-MALFI-3**, the strongest probe-surfaced finding — but it needs a
second encoding site to force (single-site findings stay banked per the
corpus discipline). So the honest options are: (a) author a second
split-pathos tragedy to force OQ-MALFI-3 (research, larger); (b) a
production swing on the roadmap parser/export surface; or (c) the
compiler stage-5 / inert-scaffolding cleanup (small, banked).

---

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketches-04 through -14, with one addition:

- **Re-probe next-OQ forecasts are falsifiable (the fourth
  rhythm-arena).** A sketch may pre-bank what it predicts the closure
  re-probe will surface, but the prediction is a hypothesis the probe
  data corrects — sketch-06's S6P-OQ1/OQ2 were both unforced; the
  probe surfaced OQ-MALFI-3/4/1B instead. Record the forecast and its
  falsification honestly.

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic (note: the
   aristotelian index line stops at probe-sketch-03; sketches 03–06
   are not indexed there — read the files directly).
2. This doc (`design/state-of-play-15.md`) — current state.
3. `design/state-of-play-14.md` — supersedes-link; carries the
   sketch-04 precondition-risk-sort framing and the third
   rhythm-arena.
4. `design/aristotelian-sketch-06.md` — the latest dialect sketch as
   landed, including the Session-6 closure-result section.
5. `prototype/story_engine/core/aristotelian.py` — the dialect, now
   A1–A21; `verify` orchestrates all checks.
6. `prototype/story_engine/encodings/malfi_aristotelian.py` — the
   densest corpus encoding; `OQ_FINDINGS` carries the seven-finding
   ledger (three CLOSED, three NEW, OQ-AP7 conjectural).
7. `prototype/reader_model_malfi_aristotelian_session6_output.json` —
   the closure-verification artifact.
8. `git log --oneline 49bb078..HEAD` — the eight commits between
   SoP-14 and SoP-15.
9. SoP-13's reading list (Lear encoding, dialect core, prior stage-3
   sketches) — remains relevant under SoP-15.
