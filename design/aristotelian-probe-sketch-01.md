# Aristotelian probe — sketch 01

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing
**Frames:** [aristotelian-sketch-01](aristotelian-sketch-01.md)
(the dialect whose surface this probe reads),
[reader-model-sketch-01](reader-model-sketch-01.md)
(the probe contract, R1–R6)
**Related:** `prototype/story_engine/core/
dramatic_reader_model_client.py` (the cross-boundary-surface probe
the Aristotelian probe's shape is parallel to);
`prototype/story_engine/encodings/oedipus_aristotelian.py`,
`rashomon_aristotelian.py` (the two encodings the probe reads);
state-of-play-04 "What's next — Research track #1"
**Superseded by:** nothing yet

## Purpose

Specify the Aristotelian-dialect probe surface and run it. First
probe against a dialect other than Dramatic / Dramatica-complete;
first probe against a dialect with **no Lowerings** (A9 scopes
cross-dialect Lowering out) and a **different verifier output
shape** (`ArObservation`, not `VerificationReview`). The existing
`dramatic_reader_model_client.py`'s two output kinds —
`AnnotationReview` (over Lowering annotations) and
`VerifierCommentary` (over VerificationReviews) — do not retrofit;
both of its load-bearing record types are absent from Aristotelian.

State-of-play-04 flagged this explicitly: *"The probe's own read
of the new dialect is itself data — does the reader-model engage
with the Aristotelian surface on its own terms, or try to
translate back into Dramatica / substrate?"* The methodological
question has to be codified as a falsifiable test, not left as a
vibe check.

**The sketch IS the test.** Per aristotelian-sketch-01's precedent
(the parent dialect sketch was itself an explicit, falsifiable
stability test of architecture-sketch-02), this probe sketch's
predictions are stated before the probe runs. If the predictions
hold, the probe's surface and contract are sound and the run
gets its first Aristotelian closing artifact. If a prediction
fails, the failure is the finding — the sketch is amended, not
the outcome.

## Why now

- State-of-play-04 names this as Research-track #1.
- The Aristotelian dialect ships with two worked cases (Oedipus,
  Rashomon) that cover the native-fit / stress axis the probe
  needs. No additional encoding is required to run the probe.
- Both encodings verify with 0 observations. The interesting
  probe surface is the dialect's *author prose* — `ArMythos.
  action_summary`, `ArPhase.annotation`, `ArCharacter.
  hamartia_text` — and the dialect's *expressive scope*. Neither
  is visible through the existing Dramatic probe.
- First dialect-only probe sets the pattern for future
  non-Dramatica dialects (sketch-02 named Freytag / author-defined
  as candidates).

## Scope — what the sketch covers

**In:**
- A new probe client module mirroring
  `dramatic_reader_model_client.py`'s pattern (typed I/O,
  scope-declared invocation, translation to substrate / dialect-
  native records, dropped-outputs audit surface).
- Three output kinds covering (a) dialect prose review,
  (b) observation commentary (the `VerificationReview` analog —
  stubbed as empty in both runs, contract specified anyway), and
  (c) a bounded free-form *dialect reading* capturing the
  methodological signal "did the LLM engage the dialect on its
  own terms?"
- Two invocations: Oedipus (native-fit baseline) and Rashomon
  four-mythoi (stress). Parallel to the aristotelian-sketch-01
  worked / stress pair.
- Falsifiable predictions stated before the runs.
- Expected closing artifact: `reader_model_oedipus_aristotelian_
  output.json` + `reader_model_rashomon_aristotelian_output.json`,
  plus a state-of-play-05 or aristotelian-probe-sketch-02
  reading.

**Out:**
- Cross-dialect commentary (LLM asked to relate an `ArMythos` to
  the Dramatic encoding of the same work — Oedipus has both
  layers, Rashomon has the Dramatica-complete stack). A9 scopes
  cross-dialect Lowering out of the dialect; by parallel the
  probe doesn't cross the layer either. When a cross-dialect
  Lowering sketch lands (architecture-sketch-02 A8), a sibling
  probe sketch would.
- Multi-model ensembling, consensus resolution (reader-model-
  sketch-01 OQ 5).
- Cost accounting (reader-model-sketch-01 OQ 8).
- Retry / refusal policy beyond Malformed / Refusal surfacing
  per R1.
- Automated detection of "LLM drifted into Dramatica vocabulary".
  The dialect-reading output kind *captures* drift when present;
  detecting it structurally is a sketch-02 OQ if a forcing
  function appears.

## Commitments

Labels **APS** (Aristotelian Probe Sketch). Parallel to the
parent dialect sketch's A1–A9 and its AA1–AA5 implementation
criteria.

### APS1 — Probe surface: dialect-only, no cross-layer

The probe reads **only** the Aristotelian records of one
encoding and a lightweight substrate summary for grounding.
It does not read the encoding's Dramatic / Dramatica-complete /
Save-the-Cat layers, even when they exist (Oedipus has all
four). This is the structural parallel to A9's "cross-dialect
Lowering out of scope": the probe stays inside one dialect.

The substrate summary is intentionally minimal — a list of
event ids that the `central_event_ids` / phase scopes
reference, each rendered as `(id, type, τ_s, participants)`,
no full effect lists. This mirrors
`dramatic_reader_model_client._substrate_event_summary` — just
enough context for the LLM to ground the Aristotelian prose
against the events it names, not a second probe surface on
substrate in disguise.

**Methodological rationale:** the test is *whether the LLM
engages Aristotelian on its own terms*. Handing it the
Dramatica layer would contaminate the test — an LLM asked to
comment on both layers can always fall back to Dramatica
vocabulary. Dialect-isolation makes the test sharp.

### APS2 — Three output kinds

The probe returns three kinds of record. Two mirror the
dramatic client's shape contract; the third is new and specific
to this probe's methodological purpose.

**(A) `AristotelianAnnotationReview`** — verdict on one prose
field of one Aristotelian record.

```python
class AristotelianAnnotationReview(BaseModel):
    target_kind: Literal["ArMythos", "ArPhase", "ArCharacter"]
    target_id: str
    field: Literal[
        "action_summary",   # ArMythos only
        "annotation",       # ArPhase only
        "hamartia_text",    # ArCharacter only
    ]
    verdict: Literal["approved", "needs-work", "rejected", "noted"]
    rationale: str          # 1-3 sentences, grounded
```

Verdict semantics parallel AnnotationReview's: *approved* = the
prose faithfully describes the substrate events it names;
*needs-work* = specific problem (overstatement, unclear claim,
unflagged tension); *rejected* = misreads what the substrate
carries; *noted* = read but no position. R1 holds: `rationale`
is the only prose field; the rest is typed.

The review surface is **per-field**, not per-record. `ArMythos`
has one prose field (`action_summary`); each `ArPhase` has one
(`annotation`); each `ArCharacter` has one (`hamartia_text`).
A review targets exactly one field — `(target_kind, target_id,
field)` identifies it uniquely.

**(B) `ObservationCommentary`** — verdict on one `ArObservation`.

```python
class ObservationCommentary(BaseModel):
    target_observation_id: str  # synthetic, assigned in prompt
    assessment: Literal["endorses", "qualifies", "dissents", "noted"]
    rationale: str
    suggested_signature: Optional[str] = None
```

Parallel to `DramaticReaderVerifierCommentary`. Synthetic ids
(`ao_0`, `ao_1`, …) assigned in prompt, resolved back at
translation time.

**Important:** both Oedipus and Rashomon verify with **zero
observations** (state-of-play-04, aristotelian-sketch-01 AA5).
The contract is committed anyway — the first Aristotelian
encoding that surfaces an observation (e.g., a future Macbeth
encoding with a contested phase scope) runs the same probe path
with non-empty input. Zero-input runs still validate the shape.

**(C) `DialectReading`** — one per invocation, bounded free-form
commentary on the dialect surface *as a whole*.

```python
class DialectReading(BaseModel):
    read_on_terms: Literal["yes", "partial", "no"]
    rationale: str    # 3-8 sentences, hard-capped
    drift_flagged: list[str] = []
    scope_limits_observed: list[str] = []
    relations_wanted: list[str] = []
```

This is new — no direct analog in `dramatic_reader_model_client.
py`. It captures the methodological signal the probe exists to
produce.

- `read_on_terms`: the LLM's own assessment of whether its
  review engaged Aristotelian vocabulary (peripeteia,
  anagnorisis, hamartia, unity) on the dialect's terms, or
  reverted to Dramatica / Save-the-Cat / general-structural
  vocabulary.
- `rationale`: 3–8 sentences explaining the `read_on_terms`
  verdict. Bounded so the output stays auditable.
- `drift_flagged`: specific phrases or record types from outside
  Aristotelian the LLM noticed itself using or wanting to use
  (e.g., "I wanted to reference DSP_limit's pressure-shape
  taxonomy"). Empty list = clean in-dialect read.
- `scope_limits_observed`: dialect-scope limits the LLM
  perceived (expected for Rashomon: meta-anagnorisis; expected
  to be empty or trivial for Oedipus).
- `relations_wanted`: structured extensions the LLM thought
  would help (expected for Rashomon: `ArMythosRelation` —
  sketch-01 A8's flagged extension — to express the four
  testimonies' contest). Probe-surfaced forcing functions for a
  hypothetical sketch-02 of the dialect.

### APS3 — Prompt discipline: render Aristotelian, not translate

The system prompt states, verbatim: *"Engage these records in
Aristotelian vocabulary. Do not translate to Dramatica /
Save-the-Cat / modern-screenplay vocabulary. Use peripeteia,
anagnorisis, hamartia, unity, catharsis where they apply; say so
explicitly if you find yourself wanting to use other
vocabularies."* The prompt's own framing is the
methodological lever.

The user prompt renders three sections:
1. **ArMythos / ArPhase / ArCharacter records.** Full fields
   JSON-serialized. Prose fields (`action_summary`, phase
   `annotation`, `hamartia_text`) surfaced alongside structural
   fields (`central_event_ids`, `peripeteia_event_id`, etc.).
2. **ArObservations** (if any). Each rendered as `(synthetic_id,
   severity, code, target_id, message)`. Both runs produce an
   empty section.
3. **Substrate context** — event-id list with
   `(id, type, τ_s, participants)` per referenced event. For
   grounding prose reviews against what the named events
   actually carry.

No Dramatic / Dramatica-complete / Save-the-Cat records appear
in the prompt, even when the encoding has them.

### APS4 — Translation contract: parallel to the dramatic client

Same shape: typed LLM output → typed substrate / dialect-native
records. The dialect-native targets are new:

- `AristotelianAnnotationReview` → a new `ArAnnotationReview`
  record (id, reviewer_id, reviewed_at_τ_a, target_kind,
  target_id, field, verdict, comment). Shape parallels
  `AnnotationReview` from `lowering.py` but targets a dialect
  record's prose field, not a Lowering's annotation. Lives in
  `aristotelian.py` so the dialect owns its review record.
- `ObservationCommentary` → a new `ArObservationCommentary`
  record. Same shape as `VerifierCommentary` but targets an
  `ArObservation` and lives in `aristotelian.py`.
- `DialectReading` → a `DialectReading` record (as above,
  de-Pydantic'd to a frozen dataclass). Lives in
  `aristotelian.py`.

A scope / id-resolution validator (parallel to
`_classify_annotation_review`) drops out-of-scope or unresolved
outputs into a `DroppedOutput` list, exactly like the dramatic
client. R5 enforcement via code, not just prompt.

### APS5 — No dialect / substrate / architecture change

The probe client is an **additive** tooling module. It imports
from `aristotelian.py` but does not modify it. The new review /
commentary / reading record types (APS4) extend `aristotelian.
py` additively — new frozen dataclasses; no change to
`ArMythos`, `ArPhase`, `ArCharacter`, `ArObservation`, `verify`,
or `group_by_severity` / `group_by_code`.

**If the implementation surfaces a need to modify an existing
Aristotelian record, halt.** The parent sketch's verdict was
GREEN on extension-only; a probe-shape requirement that forces
dialect modification would amend that verdict. No such
requirement is anticipated.

### APS6 — Falsifiable predictions

The test. Each prediction has a pass / fail criterion readable
from the probe's output JSON alone. These are stated before the
runs.

**(P1) Oedipus prose reviews: majority approved.**
The encoding was authored from Aristotle's own worked example
(Poetics 1452a). `E_messenger_adoption_reveal` as peripeteia is
canonical; `E_oedipus_anagnorisis` as anagnorisis is canonical;
the hamartia texts for Oedipus and Jocasta cite Aristotle
directly. Prediction: ≥ 80% of the 5 prose fields (1 action
summary + 3 phase annotations + 2 hamartia_texts = 6, minus any
empty — call it 6) earn `approved`. **Fail:** < 80% approved
or any `rejected`. **Pass:** ≥ 80% approved, ≤ 1 `needs-work`
or `noted`, 0 `rejected`.

**(P2) Rashomon prose reviews: at least one structured tension
surfaced.**
The stress case's sketch-01 analysis named two specific
dialect-scope tensions: (a) the four testimonies contest the
same canonical-floor events; (b) none of the testifiers
experience character-level anagnorisis (sketch's "meta-
anagnorisis" limit). Prediction: at least one prose review
across the four mythoi flags one of these — typically on an
`action_summary` ("Tajōmaru's noble-contest account vs.
identical canonical-floor events") or on a `hamartia_text`
whose claim only holds inside one testimony's reading.
**Fail:** all 4 × (1 + 3 + ≥1) = ≥ 20 prose reviews come back
`approved` with generic rationales, zero surfaced tensions.
**Pass:** ≥ 1 review with `needs-work` or `noted` citing one of
the sketch-01 tensions.

**(P3) ObservationCommentary empty for both runs.**
Both encodings produce zero `ArObservation` records; the probe
has no observations to comment on. Prediction: the LLM returns
an empty `observation_commentaries` list (it has nothing to
comment on). **Fail:** the LLM fabricates observations or
commentaries that don't target anything the probe showed it —
these land in `DroppedOutput` by validator rules. **Pass:**
empty list, no drops from that surface.

**(P4) DialectReading stays in-dialect.**
This is the probe's distinctive methodological signal.
Prediction: `read_on_terms` = `"yes"` for Oedipus (native fit,
no reason to drift); may be `"partial"` for Rashomon (the
`relations_wanted` list likely names `ArMythosRelation` — which
IS the sketch-01 A8 extension flag; that's not drift, that's
a sketch-surfaced extension). `drift_flagged` empty or minimal.
`scope_limits_observed` for Rashomon includes something in the
meta-anagnorisis / character-level-only class. **Fail:**
`drift_flagged` contains Dramatica-vocabulary terms
(`DSP_limit`, `Signpost`, `Domain`, `pressure-shape`,
`inciting-beat`) — the LLM reverted. **Pass:** dialect-reading
text uses peripeteia / anagnorisis / hamartia / unity /
catharsis, not DSP / pressure / beat / signpost.

**(P5) Rashomon specifically surfaces `ArMythosRelation` as
`relations_wanted`.**
The parent sketch anticipated this: "Adding a relation record
is a sketch-02 concern if a forcing function appears." If the
LLM independently asks for `ArMythosRelation` without prompting
— after seeing four ArMythos records with overlapping central
event sets — that's a probe-surfaced forcing function for
aristotelian-sketch-02. Prediction: `relations_wanted` contains
a relation-shaped string (doesn't need to be the exact name;
semantically equivalent qualifies — "a way to express contest
between mythoi", "a relation between ArMythos records", etc.).
**Fail:** `relations_wanted` empty for Rashomon. **Pass:** any
relation-shaped entry.

Predictions P1 through P4 are acceptance; P5 is *exploratory* —
if it passes, the probe produces a sketch-02 forcing function;
if it fails, the probe's shape is still sound but that specific
extension doesn't pressure from the LLM's reading.

## Worked case — Oedipus prose-review surface

What the LLM sees for the Oedipus invocation:

**Records rendered:** 1 × `ArMythos` (`ar_oedipus`) + 3 ×
`ArPhase` (`ph_beginning`, `ph_middle`, `ph_end`) + 2 ×
`ArCharacter` (`ar_oedipus`, `ar_jocasta`). Six prose fields
total.

**Substrate summary:** the 16 event ids `ar_oedipus`'s
`central_event_ids` names, with `type` + `τ_s` +
`participants`. The LLM can check: the action_summary claims "A
king, investigating a plague ... discovers that he himself is
the murderer of his predecessor"; the substrate summary shows
`E_oedipus_anagnorisis` at its τ_s with oedipus as participant;
`E_crossroads_killing` earlier with oedipus + laius. Both
claims grounded.

**Observations rendered:** empty. The `ArObservations` section
reports "(no observations — encoding verifies clean)".

Predicted LLM behavior (P1, P4):
- 6 prose reviews produced, 5–6 approved, 0 rejected. Rationales
  cite Poetics 1452a or the event ids by id.
- `DialectReading.read_on_terms = "yes"`; `drift_flagged = []`;
  `scope_limits_observed = []`; `relations_wanted = []`
  (nothing structural pressures for extension — Oedipus *is*
  the canonical case).

The Oedipus run's purpose is baseline: if the probe can't
produce a clean read on the encoding Aristotle built his theory
from, the probe's surface / prompt / contract is mis-specified
before it ever sees stress.

## Stress case — Rashomon prose-review surface

What the LLM sees for the Rashomon invocation:

**Records rendered:** 4 × `ArMythos` (bandit, wife, samurai,
woodcutter) + 3 × `ArPhase` per mythos (12 total) + 1 ×
`ArCharacter` per mythos (4 total; different tragic heroes).
Total prose fields: 4 `action_summary` + 12 `annotation` + 4
`hamartia_text` = 20.

**Substrate summary:** the canonical-floor 6 events
(`E_travel` … `E_intercourse`) are each referenced by all four
mythoi's beginning phases. The testimony-branch events
(B_TAJOMARU, B_WIFE, B_HUSBAND, B_WOODCUTTER branches) are
each referenced by exactly one mythos. The LLM sees 22 event
ids total.

**Observations rendered:** empty (same as Oedipus).

Predicted LLM behavior (P2, P4, P5):
- 20 prose reviews, most approved, at least one surfacing a
  dialect-scope tension (the `action_summary` for one testimony
  claims "noble combat" / "pure violation" / "righteous anger"
  over a set of canonical-floor events other testimonies
  read identically structurally but oppositely interpretively;
  OR a `hamartia_text` naming one tragic hero's error that
  another testimony's `hamartia_text` contradicts).
- `DialectReading.read_on_terms = "partial"` with
  `scope_limits_observed` including meta-anagnorisis-class
  language; `relations_wanted` including `ArMythosRelation`-
  class language. Both predicted by aristotelian-sketch-01 at
  the sketch level; the probe is the empirical check.
- `drift_flagged` ideally empty. If non-empty and names a
  Dramatica-vocabulary concept, that's a finding about the
  prompt's strength, not the dialect's fit.

The Rashomon run's purpose is the methodological test: can the
probe produce differentiated output on a work whose testimonies
contest each other's interpretations, without the LLM reverting
to Dramatica multi-Story vocabulary? If yes, the probe surface
scales; if no, the prompt needs sharpening.

## Not in scope

- **Triggered / batched invocations.** reader-model-sketch-01
  admits all three modes (interactive, triggered, batch); this
  probe runs **interactive only**. Two explicit author-invoked
  runs. No auto-trigger on encoding change.
- **Prose-review of ArCharacter `name`.** The `name` field is
  not prose (identifier-like). No review surface on it.
- **Reviewing the absence of `is_tragic_hero=True` elsewhere.**
  The probe reviews prose fields on records that were authored;
  it does not flag missing records (e.g., "this mythos has no
  tragic-hero ArCharacter"). That is an author / author-
  discipline concern, not a probe concern in v1.
- **Cross-mythos review within one invocation.** The LLM sees
  four ArMythos records for Rashomon and may cite cross-mythos
  contest in a `hamartia_text`'s rationale — that's fair game.
  But the probe does not ship a `CrossMythosCommentary` output
  record; cross-mythos relation-extensions surface via
  `DialectReading.relations_wanted` (APS5 / P5).
- **Macbeth or Ackroyd encodings under Aristotelian.** Named in
  state-of-play-04 as future research; a later probe sketch
  covers them once the encoding lands.
- **Multi-run / ensemble / self-critique.** One invocation per
  encoding at one `current_τ_a`. reader-model-sketch-01 OQ 5
  / OQ 7 handle these as future concerns; no commitment here.

## Open questions

1. **OQ1 — Structured dialect-reading output in sketch-02.**
   `DialectReading` ships three list fields (`drift_flagged`,
   `scope_limits_observed`, `relations_wanted`) as free-form
   strings. If sketch-02 (a probe against Macbeth-Aristotelian,
   say) surfaces that the same scope limits / relations appear
   repeatedly, a typed enum might replace the free-form shape.
   Forcing function: ≥ 3 probe invocations; ≥ 2 share the same
   relation-wanted; 0 ambiguous cases in the ≥ 3 invocations'
   `drift_flagged` lists.
2. **OQ2 — Substrate-side grounding beyond event summary.**
   The probe ships `(id, type, τ_s, participants)` per
   referenced event. Not `effects`. If a prose review claims
   "the peripeteia event reverses fortune" and the effect list
   would substantiate or undermine the claim, the probe misses
   the grounding. Candidate: opt-in `with_effects=True` flag on
   the probe. Defer until a review's rationale is undermined by
   substrate detail the probe hid.
3. **OQ3 — Character-ref-id resolution in the prompt.**
   `ArCharacter.character_ref_id` names a substrate Entity (or
   Dramatic Character) id. The probe renders the id string; it
   does not fetch and render the Entity record. If the LLM's
   hamartia_text review would benefit from "oedipus is a
   substrate Entity of kind=person, appearing as
   agent/patient/etc. in N events", the probe could surface
   that. Defer until a hamartia_text review is obviously
   weakened by the absence.
4. **OQ4 — Should the probe distinguish `noted` for "no
   position" from `noted` for "incompetent"?** The annotation-
   review surface currently lumps them. Mild refinement; defer
   unless a probe run surfaces a specific noted-as-what-kind
   ambiguity.
5. **OQ5 — `ArObservationCommentary` + `ArAnnotationReview`
   promotion to `verification.py` / `lowering.py`?** If a
   second dialect (Freytag?) probes similarly and wants the
   same review / commentary surface, promoting those records to
   a shared location might be right. Defer — one-dialect usage
   is not pressure; two is.
6. **OQ6 — Refusal / malformed handling.** Inherited from
   reader-model-sketch-01's contract. Follow the dramatic
   client's pattern (DroppedOutput for scope violations;
   Pydantic parse errors surface as exceptions from
   `client.messages.parse()`; no Refusal record type yet in
   the dramatic client either). First Refusal encountered
   drives the shape; not pre-engineered.

## Acceptance criteria

Labels **APA** (Aristotelian Probe Acceptance). Parallel to the
parent dialect sketch's AA1–AA5.

- **[APA1]** Three new records in `aristotelian.py`:
  `ArAnnotationReview` (frozen dataclass: id, reviewer_id,
  reviewed_at_τ_a, target_kind, target_id, field, verdict,
  comment, anchor_τ_a), `ArObservationCommentary` (frozen
  dataclass: commenter_id, commented_at_τ_a, assessment,
  target_observation, comment, suggested_signature), and
  `DialectReading` (frozen dataclass: reader_id, read_at_τ_a,
  read_on_terms, rationale, drift_flagged,
  scope_limits_observed, relations_wanted). Additive; no
  change to existing records.
- **[APA2]** New module `prototype/story_engine/core/
  aristotelian_reader_model_client.py`. Pydantic schemas per
  APS2. Helper functions to render `ArMythos`, `ArPhase`,
  `ArCharacter`, `ArObservation`, substrate-event summaries.
  SYSTEM_PROMPT per APS3. Public entry point
  `invoke_aristotelian_reader_model(...)` with `dry_run` path
  (parallel to the dramatic client's dry-run).
- **[APA3]** Translation + scope-validation functions parallel
  to `_classify_annotation_review` /
  `_translate_annotation_review` from the dramatic client.
  `DroppedOutput` surface for scope violations.
- **[APA4]** Test module `prototype/tests/test_aristotelian_
  reader_model_client.py` covering: (a) prompt-construction
  dry-run for Oedipus + Rashomon (the rendered prompt shape
  is validated without an API call); (b) translation for each
  of the three output kinds; (c) scope validator rejects
  out-of-scope targets. Target: 15–20 tests.
- **[APA5]** Demo scripts
  `prototype/demos/demo_aristotelian_reader_model_oedipus.py`
  and `demo_aristotelian_reader_model_rashomon.py`, patterned
  on the dramatic demos. Each writes its probe JSON to
  `prototype/` root: `reader_model_oedipus_aristotelian_output.
  json` and `reader_model_rashomon_aristotelian_output.json`.
- **[APA6]** Two live probe runs after APA1–APA5 land. The
  run commit carries both JSON files and reports the
  outcome of predictions P1–P5 against the captured output.
- **[APA7]** All existing tests continue to pass (no
  modification to any pre-existing file under `prototype/`
  other than test totals in per-encoding test modules if the
  dialect gains test counts — and it shouldn't, because
  APA1–APA5 add new modules, not modifications).

If APA6's probe results invalidate a P1–P4 prediction, the
finding lands as aristotelian-probe-sketch-02 or amends this
sketch. P5 may pass or fail without amendment (it's
exploratory).

## Summary

A falsifiable probe sketch for the Aristotelian dialect. The
existing Dramatic probe doesn't retrofit — Aristotelian has no
Lowerings and a different verifier output shape. New client
module mirrors the dramatic-client pattern; three output kinds
cover dialect prose review, observation commentary (specified
even though both runs will produce zero observations), and a
bounded dialect-reading that captures the probe's distinctive
methodological signal. Two invocations: Oedipus (native fit) +
Rashomon (four-mythos stress). Five predictions stated before
the runs. Extension-only — new additive records in
`aristotelian.py`, new client module, new demo scripts, new
tests; no change to `ArMythos` / `ArPhase` / `ArCharacter` /
`ArObservation` / `verify`.

If P1–P4 hold, the probe surface and contract are sound and
the Aristotelian dialect earns its first probe closing
artifact. If P5 holds additionally, the probe produces a
forcing function for an eventual aristotelian-sketch-02
(`ArMythosRelation` as typed record, anticipated by
sketch-01's A8 discussion). If any of P1–P4 fails, the failure
is the finding and the sketch is amended.
