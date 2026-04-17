# Event-kind taxonomy — sketch 01

**Status:** draft, active
**Date:** 2026-04-16
**Supersedes:** nothing (new topic; closes a specific verifier weakening)
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [architecture-sketch-02.md](architecture-sketch-02.md), [substrate-sketch-05.md](substrate-sketch-05.md), [verification-sketch-01.md](verification-sketch-01.md)
**Related:** [lowering-sketch-01.md](lowering-sketch-01.md) F5, `oedipus_dramatica_complete_verification.py`, `macbeth_dramatica_complete_verification.py`, `ackroyd_dramatica_complete_verification.py`
**Superseded by:** nothing yet

## Purpose

Close a tension surfaced by the dramatica-complete → substrate
verifier's three-point verdict-strength spectrum (APPROVED 0.69
Macbeth / PARTIAL 0.54 Ackroyd / NEEDS_WORK 0.31 Oedipus post-F5).
The NEEDS_WORK anchor is not a noise floor; it is a real finding
pointing at how the Activity / Do-er check classifies substrate
events. The check uses two frozen type-string sets —
`ACTIVITY_ACTION_KINDS` and `INTERNAL_STATE_KINDS` — under which
every `utterance`-typed event lands in the internal-state bucket.
That is correct for soliloquy but wrong for command, interrogation,
confrontation, and testimony, which are Sophocles's onstage grammar.

The fix is narrower than "refine the substrate event-kind vocabulary":
it is a verifier-layer change that reads fold-visible structural
features the substrate already carries. Substrate-sketch-05's
existing discipline is exactly right for this —

> Two events with the same effects and the same participants but
> different types produce the same fold result. If that feels wrong
> for a given case, the right move is to examine the effects, not to
> reach for type dispatch.

— and the verifier is the layer that should apply it.

## What this sketch is *not* committing to

- Reopening substrate-05's type-as-tag commitment. Type stays a
  categorical tag; the substrate does not dispatch on it.
- A new attribute on the event record (no `register` field, no
  speech-act axis). A3 rejects that move — see Candidate C below.
- A fixed, universal taxonomy of event kinds. Substrate-05's
  extension rule stands: event types are authored per story.
- Changing the `characterization` primitive itself. V3 /
  `verify_characterization` / `run_characterization_checks` are
  unchanged. Only the *check functions* that consume them change.
- Propagating the classifier beyond cross-boundary verifiers into
  substrate fold logic. It remains a library-level operator per
  substrate-05 L1.

If a question starts "should substrate events get a new attribute,"
"should `utterance` be split into finer substrate types by default,"
or "does the fold care about external-vs-internal" — it is out of
scope. This sketch touches only the verifier layer.

## The tension in one frame

Substrate-05 commits: *type is a categorical tag, not a dispatch
key.* Library-level operators may group by type — a genre template
counting combat events is the licensed case — but the substrate
itself does not branch on type, and the principle-of-last-resort
when type feels wrong is to examine effects and participants, not
to add type dispatch.

The cross-boundary verifier is a library-level operator in
substrate-05's vocabulary, so its use of type for classification is
licensed. But its classification is only sound if the types it
consumes are fine-grained enough to preserve the distinction it
cares about. Oedipus's `utterance` type is too coarse: it lumps
together at least five speech-act shapes with different downstream
character under Dramatica's Activity classification —

- **Soliloquy.** Speaker alone; no hearer. Effect: self-knowledge
  update.
- **Command.** Speaker + addressed subordinate. Effect: directive
  received; downstream action conditioned on obedience.
- **Interrogation.** Speaker + witness. Effect: bidirectional
  knowledge update (witness discloses, interrogator learns).
- **Confrontation.** Speaker + accused. Effect: accusation received;
  social stance shifts.
- **Testimony.** Speaker + audience. Effect: audience knowledge
  update; may close a gap the audience holds.

Dramatica's Activity classification reads the first as internal-state
and the other four as external action. The verifier can see the
difference from participants and effects; it cannot see the
difference from `type == "utterance"` alone.

This is the load-bearing observation. The verifier is missing
signal the substrate already has.

## Candidates considered

The candidates were discussed in conversation before drafting; the
rationale is recorded here so later sketches can reopen with a
clean record.

### Candidate A — Split `utterance` into finer per-story types

Introduce `command`, `interrogation`, `confrontation`, `testimony`,
`soliloquy` as distinct substrate event types per story, per
substrate-05's extension rule. The verifier's type-string sets
recognize the external-action ones.

- **For.** Aligns with substrate-05's extension rule exactly.
  Zero structural change. Per-story; reversible.
- **Against.** Type proliferation is on the project's schema-drift
  smell list. Five sub-types of speech risks snowballing into
  dozens per story; the sub-types also vary across genres (Greek
  tragedy's types differ from mystery-novel types). It also
  *duplicates* information already present in participants and
  effects — the distinguishing feature of a command vs a soliloquy
  is already fold-visible.
- **Verdict.** Kept as a per-story fallback, not the primary fix.
  See the recommendation.

### Candidate B — Effect-and-participant-based classification at the verifier

Keep `utterance` as a single type. The verifier's
"is this external-action?" check reads `participants` and `effects`,
not a type-string set. The classifier becomes a function of
structural features.

- **For.** Honors substrate-05's "examine the effects" discipline
  literally. No new type vocabulary. Classification grounded in
  fold-visible substrate features. Generalizes across encodings
  automatically — the same classifier works on Macbeth's action
  events and Oedipus's speech events without per-story tuning.
- **Against.** More verifier complexity. Distinguishing
  interrogation (hearer + bidirectional knowledge update) from
  command (hearer + directive-shaped effect) requires careful
  reading of effect shape, not just participant count. Some events
  are genuinely borderline (see `prophecy_received` below).
- **Verdict.** Primary fix.

### Candidate C — Orthogonal axis on the event record

Add a required event attribute — `register ∈ {external, internal}`
or a Searle speech-act taxonomy — that the verifier reads directly.

- **For.** Explicit. Easy for the verifier.
- **Against.** **A3 fail.** External-vs-internal is not a
  distinction the schema catches that prose does not — an attentive
  LLM or human reading the scene would classify command vs
  soliloquy correctly from the text. The axis exists for the
  verifier's convenience, not because the substrate needs it.
  Substrate-05 M1 expressly routes this kind of content to
  descriptions, not to typed fields.
- **Verdict.** Rejected.

### Candidate D — Description-driven classification via reader-model probe

Attach descriptions that classify each event's register, authored or
LLM-derived. The verifier reads descriptions, not type.

- **For.** A3-compliant. Composes with architecture-02 A11's probe
  surface.
- **Against.** Loses the verifier's mechanical determinism. Turns a
  symbolic check into a probe task. The question "does this event
  have non-speaker participants and a knowledge effect on them?" is
  structural, not interpretive — no probe needed.
- **Verdict.** Rejected *for this purpose*. Still the right move
  for genuinely interpretive classifications (tonal, thematic).

### Candidate E — Accept NEEDS_WORK 0.31 as truthful signal

Do not refine anything. The verdict is a property of Oedipus's
substrate encoding being at a different grain than Dramatica's
Activity taxonomy.

- **For.** Zero cost. Respects the substrate's coarseness as part
  of its honesty.
- **Against.** Pins the three-point spectrum's NEEDS_WORK anchor
  permanently. Provides no path forward for any encoding whose
  substrate-grain is genuinely mismatched with an upper dialect's
  taxonomy. Masks the distinction between "the lowering is
  imperfect" (signal-worthy NEEDS_WORK) and "the verifier is
  reading the wrong feature" (correctable).
- **Verdict.** Rejected. The three-point spectrum is more valuable
  if it reports substrate-lowering honesty, not verifier-
  heuristic brittleness.

## Commitments

### EK1 — Verifier classification reads fold-visible structure, not type strings

The cross-boundary verifier's "is this external-action?" predicate
is a function of the event's `participants` and `effects`, not a
lookup into a type-string set. Type strings may inform the
classifier (e.g., as a cheap first-pass filter for obvious kinds
like `killing`) but may not be the only input.

### EK2 — The external-action predicate

An event is **external-action-shaped** if both hold:

- **Interpersonal.** `participants` contains at least two distinct
  entity ids. (Self-directed or single-participant events —
  soliloquy, realization — fail this clause.)
- **Outward-effect.** At least one of:
  - a `WorldEffect` (the event changes world state), or
  - a `KnowledgeEffect` whose target agent is not the event's
    primary actor (another participant's knowledge updates).

The primary actor is determined by role-name convention, with
fallback to the first participant:
`killer > speaker > actor > agent > subject > first participant`.

An event is **internal-state-shaped** if it is not
external-action-shaped. The two categories are exhaustive — this
sketch does not introduce a third bucket.

### EK3 — The classifier is encoding-agnostic and lives in `verifier_helpers.py`

Per REVIEW.md finding 3 and commit `bf5bfa0` (Extract shared
cross-boundary verifier helpers), the extracted classifier is the
canonical implementation; each verifier module imports it. The
`ACTIVITY_ACTION_KINDS` / `INTERNAL_STATE_KINDS` frozen sets are
removed from `oedipus_dramatica_complete_verification.py`,
`macbeth_dramatica_complete_verification.py`, and
`ackroyd_dramatica_complete_verification.py`.

### EK4 — Candidate A remains available as a per-story fallback

If a story's encoding uses `utterance`-shaped events whose
participants or effects do not carry the distinguishing
information (e.g., a command encoded with only one participant, or
a testimony whose KnowledgeEffect is misattributed), the encoding
may split `utterance` into finer types. EK4 is not a recommended
default. It is the escape hatch for substrate encodings whose
grain is intentionally coarse.

### EK5 — The external-vs-internal frame is a verifier concern, not a substrate one

The substrate makes no commitment to a two-bucket taxonomy.
Different upper dialects may ask different structural questions
("is this action-shaped?" is the Activity / Do-er question; a
Save-the-Cat verifier's "is this a plot-beat hit?" is a different
question entirely). EK1/EK2 specify one such classifier for the
dramatica-complete → substrate boundary. Other boundaries get
their own classifiers, written in the same style.

## Worked case — Oedipus events under EK2

`oedipus.py` at the current commit has 13 events spanning the
pre-play (τ_s ∈ [-1000, -100]) and in-play (τ_s ∈ [0, 100]) arcs.
Classification under EK2:

| Event | type | primary actor | distinct participants | outward effect | EK2 |
|---|---|---|---|---|---|
| E_birth | birth | — | 3 (child/father/mother) | WorldEffect | external |
| E_exposure | exposure | — | ≥2 | WorldEffect | external |
| E_upbringing | upbringing | — | 3 | WorldEffect | external |
| E_prophecy_received | prophecy_received | recipient | 1 (recipient only) | KnowledgeEffect on self | **internal** |
| E_crossroads_killing | killing | killer (oedipus) | 2 (killer/victim) | WorldEffect (dead) | external |
| E_marriage | marriage | husband (oedipus) | 2 | WorldEffect / social state | external |
| E_tiresias_accusation | utterance | speaker (tiresias) | 2 (speaker/listener) | KnowledgeEffect on listener (oedipus) | **external** |
| E_jocasta_discloses | utterance | speaker (jocasta) | 2 | KnowledgeEffect on listener | **external** |
| E_messenger_1 | utterance | speaker (messenger) | 2 | KnowledgeEffect on listener | **external** |
| E_messenger_2 | utterance | speaker (messenger) | 2 | KnowledgeEffect on listener | **external** |
| E_jocasta_realization | realization | agent (jocasta) | 1 (agent only) | KnowledgeEffect on self | **internal** |
| E_shepherd_testimony | utterance | speaker (shepherd) | 2 | KnowledgeEffect on listener | **external** |
| E_oedipus_anagnorisis | realization | agent (oedipus) | 1 | KnowledgeEffect on self | **internal** |
| E_jocasta_death | death | agent (jocasta) | ≥1 | WorldEffect (dead) | external |
| E_oedipus_blinding | blinding | agent (oedipus) | 1 (agent + location) | WorldEffect | borderline |
| E_oedipus_exile | exile | agent (creon) | 2 (agent/subject) | WorldEffect | external |

Borderline cases are flagged explicitly:

- **`E_prophecy_received`.** Apollo is the conceptual sender but is
  not encoded as a participant (the substrate does not commit to
  divine entities as Agents). Under EK2, internal. If a future
  encoding represents Apollo as an Entity, the event flips to
  external and the verifier should report the change. This is
  encoding honesty, not verifier fragility.
- **`E_oedipus_blinding`.** Only oedipus is a named participant
  (`location` is not an entity in the participant-identity sense
  EK2 reads). WorldEffect is present but inward-directed. Under
  EK2, this is a borderline-single-participant case; treated as
  internal. If the encoding adds a witness participant (the
  Chorus, Creon), it flips to external.
- **Realization events.** Always internal under EK2. This is
  correct for `project_knowledge` semantics — a realization is a
  self-contained knowledge-integration step. The fact that
  Oedipus's anagnorisis is the *payoff* of his external
  investigation is a sequence property (the realizations come
  after a chain of external events); it is not a property of the
  realization event itself. A future refinement (see Open
  Questions) might count a realization as external-adjacent if its
  immediate predecessors are external. Not in this sketch.

Counted for the `mc_throughline_activity_domain_check` against
T_mc_oedipus's lowered events (13 events on the MC Throughline's
PositionRange extent):

**Measured under the old type-string heuristic:** 4/13
external-action-kind (ratio 0.31 → NEEDS_WORK).

**Measured under EK2:** 10/13 external-action-shaped (ratio 0.77
→ APPROVED). The four `utterance` events, the `killing`, the
`marriage`, plus several pre-play / post-anagnorisis beats flip
to external because they have ≥2 agent-participants and outward
effects. Verdict moves from NEEDS_WORK → APPROVED (+46 pp).
`oedipus_do_er_approach_check` makes the same move against the
13 Oedipus-participation events (0.31 → 0.77, NEEDS_WORK →
APPROVED).

Post-EK2 Oedipus is 4-of-4 APPROVED at the dramatica-complete →
substrate boundary.

## Worked case — Macbeth under EK2 (no-regression check)

Macbeth's substrate is action-saturated: killings, battles,
coronations, sieges. Under EK2 these remain external — they have
WorldEffects and multiple participants.

**Measured:** DA_mc holds at PARTIAL 0.69 (9/13 external; same
count as the type-string heuristic). DSP_approach moves APPROVED
0.79 → APPROVED 0.71 (11/14 → 10/14 external). The single
downgraded event is signal EK2 is being *stricter* than the
type-string heuristic — an event whose type matched
`ACTIVITY_ACTION_KINDS` now fails the participant/effect predicate
(likely a single-participant event with a WorldEffect). That is
EK2 working as designed: less-brittle classification, fewer false
positives. Verdict bands preserved.

## Worked case — Ackroyd under EK2 (inversion preserved)

Ackroyd's MC (Sheppard) is Manipulation / Be-er. The DSP_approach
check uses EK2 inverted: internal-state-shaped is the complement
of external-action-shaped per EK2's final clause, so the same
predicate serves both directions by negation.

**Measured:** DSP_approach PARTIAL 0.38 → PARTIAL 0.46 (5/13 →
6/13 internal; one event that previously matched
`INTERNAL_STATE_KINDS` by type now flips to external under EK2's
structural predicate, and vice versa for another — net movement
toward the PARTIAL center). Verdict band holds.

**The DA_mc Manipulation check is not touched by EK2.** EK2
classifies external-vs-internal action-shape; Manipulation is a
different structural question. Per EK5 each upper-dialect
classification gets its own classifier. The Ackroyd
Manipulation-domain check keeps its `MANIPULATION_KINDS` set for
now; retiring it in favor of a structural predicate for
concealment-shape is banked as a follow-on, pressing only when a
second Manipulation-MC encoding lands.

## Relation to the three-point spectrum

The README's finding that the three verifiers span APPROVED 0.69 /
PARTIAL 0.54 / NEEDS_WORK 0.31 is real, but under EK2 the shape of
what the spectrum measures is sharper:

- **Before EK2.** The spectrum conflates two things: (a) how well
  the substrate encoding matches Dramatica's taxonomy (a substrate
  authoring question), and (b) how well the verifier's type-string
  heuristic matches the substrate's type vocabulary (a verifier
  heuristic question).
- **After EK2.** The spectrum measures (a) only. Verifier
  heuristic brittleness is removed as a confound. A NEEDS_WORK
  verdict under EK2 is a claim about the substrate encoding —
  which is exactly what the verifier should be reporting.

This is the main argument for landing EK2: it makes the spectrum
mean the thing we want it to mean.

## Implementation brief

Concrete change, in order of landing:

1. **Add `classify_event_action_shape` to `verifier_helpers.py`.**
   Takes an `Event` and returns one of `"external"`, `"internal"`.
   Primary-actor resolution via the role-name precedence list in
   EK2. Unit tests in `test_verification.py` pin the classifier
   against a small fixture table (one per borderline case listed
   above plus the clean cases).
2. **Rewrite `mc_throughline_activity_domain_check` in
   `oedipus_dramatica_complete_verification.py`.** Replace the
   `_event_kind(e) in ACTIVITY_ACTION_KINDS` lookup with
   `classify_event_action_shape(e) == "external"`. Remove the
   `ACTIVITY_ACTION_KINDS` / `INTERNAL_STATE_KINDS` module-level
   frozen sets.
3. **Rewrite `oedipus_do_er_approach_check`.** Same change.
4. **Apply the parallel rewrite to
   `macbeth_dramatica_complete_verification.py`.**
5. **Apply the parallel rewrite to
   `ackroyd_dramatica_complete_verification.py`.** Note the
   inversion: the Ackroyd check measures
   `classify_event_action_shape(e) == "internal"` for the Be-er
   case.
6. **Re-measure the three-point spectrum.** Record the new
   strengths in the README finding. If any verdict boundary flips
   (Oedipus NEEDS_WORK → PARTIAL / APPROVED; Macbeth APPROVED
   stays; Ackroyd PARTIAL stays), document the new numbers as the
   EK2 baseline.
7. **Update `test_verification.py` integration tests** to pin the
   new verdict ranges. The test is not "the verdict is exactly
   0.69"; it is "the verdict is in the expected band (APPROVED /
   PARTIAL / NEEDS_WORK)." Exact match_strength values are
   allowed to drift with encoding edits.

No substrate changes. No new event types. No schema changes in any
dialect.

## Discipline

- **Future cross-boundary verifier checks use the same pattern.**
  When writing a new characterization check (beyond the
  Activity/Do-er shapes this sketch addresses — e.g., Universe
  domain, Psychology domain, Obstacle Character stakes),
  classifier functions live in `verifier_helpers.py` and read
  participants / effects / authored descriptions; they do not
  reach for type-string sets.
- **Type-string sets are a warning sign.** If a reviewer sees a
  frozen set of type strings as the only distinguishing feature in
  a new verifier check, that is a signal to write the classifier
  as a structural predicate first. EK1 is the rule; type-set
  shortcuts are the exception that must be justified.
- **Substrate-05 M1 still governs event types themselves.** EK4's
  escape hatch — splitting `utterance` per story — applies the
  substrate-05 extension rule; it does not invent a new one. Any
  story-level type split is documented per substrate-05 discipline.
- **The no-Realization-at-Template-layer finding persists.** EK2
  is not a Realization coupling; it is a refinement of the
  Characterization primitive's symbolic check. No `*_lowerings.py`
  changes follow from this sketch.

## Open questions

1. **Realization-as-external-adjacent.** Oedipus's anagnorisis is
   the payoff of external investigation; under EK2 the realization
   event itself is internal. A sequence-aware refinement might
   count a realization as external-adjacent if its immediate
   predecessors (in sjuzhet or τ_s proximity) are external. This
   changes the verifier's result on investigation-arc stories but
   not on internally-driven realization stories. Deferred pending a
   concrete forcing function.

2. **Multi-actor events.** EK2's primary-actor fallback chain
   (`killer > speaker > actor > agent > subject > first`) assumes a
   single primary actor. Events like `battle` (macbeth) or
   `conspiracy` may genuinely have two or more primary actors on
   equal footing. The classifier still works (as long as at least
   one participant is non-self-directed and effects reach beyond
   the primary, the event is external), but the primary-actor
   identification may become a reporting-only concern. Watch for
   pressure on this from save-the-cat-sketch-02 or a future
   dialect.

3. **Prophecy_received as a borderline.** EK2 classifies
   `E_prophecy_received` as internal because Apollo is not a
   participant. The substrate could encode divine senders as
   Entities (no substrate change — Entity is the base type); that
   would flip this event to external and shift at least one
   strength score. Is there an argument against encoding gods as
   Entities? Deferred; this is more an encoding discipline question
   than a verifier question.

4. **EK2 on descriptions-carried couplings.** Some Characterization
   checks will target record fields lowered not to events but to
   descriptions (per lowering-sketch-01 F3). The external-action
   predicate does not apply directly to descriptions. A description-
   targeted check has its own shape — and EK1 still holds ("read
   fold-visible structure, not type strings"): the classifier for
   descriptions reads description kind / attention / anchor, not a
   type-string set. This sketch does not specify that classifier;
   flag it as a follow-on when a real description-targeted check
   lands.

5. **Save-the-Cat boundary.** This sketch is scoped to the
   dramatica-complete → substrate boundary. A parallel sketch for
   save-the-cat → substrate will face a different question
   (beat-hit classification, not action-shape classification) and
   should apply the same EK1 discipline independently. A shared
   "classifier library" in `verifier_helpers.py` is the natural
   home.

## Summary

- The verifier's type-string heuristic is the brittle layer. The
  substrate's type vocabulary is fine.
- The fix is a structural predicate over participants and effects
  (EK2), promoted into `verifier_helpers.py` (EK3), with A as a
  per-story fallback (EK4) and the frame declared verifier-local
  (EK5).
- No substrate changes. No new dialect commitments. Only the
  verifier layer moves.
- After the implementation pass, the three-point spectrum measures
  substrate-lowering honesty rather than verifier heuristic
  brittleness — which is the signal it was meant to carry.

## Implementation landed

This sketch has been implemented. `classify_event_action_shape` and
`agent_ids_from_entities` live in `verifier_helpers.py`; the two
Characterization checks in each of the three dramatica-complete
verifier modules now call EK2; the old `ACTIVITY_ACTION_KINDS` /
`INTERNAL_STATE_KINDS` frozen sets are removed from Oedipus and
Macbeth (Ackroyd keeps `MANIPULATION_KINDS` for its Manipulation-
domain check, which EK2 does not address).

**Post-EK2 spectrum, measured:**

| Encoding | DA_mc | DSP_approach | DSP_outcome | DSP_judgment |
|---|---|---|---|---|
| Macbeth | PARTIAL 0.69 | APPROVED 0.71 | APPROVED 1.00 | APPROVED 1.00 |
| Oedipus | APPROVED 0.77 | APPROVED 0.77 | APPROVED 1.00 | APPROVED 1.00 |
| Ackroyd | PARTIAL 0.54 (manip.) | PARTIAL 0.46 | APPROVED 1.00 | APPROVED 1.00 |

(Pre-EK2 Oedipus: NEEDS_WORK 0.31 / NEEDS_WORK 0.31. Pre-EK2
Macbeth: PARTIAL 0.69 / APPROVED 0.79. Pre-EK2 Ackroyd:
PARTIAL 0.54 / PARTIAL 0.38.)

Oedipus moves from 2-of-4 APPROVED to 4-of-4 APPROVED at this
boundary. The finding "NEEDS_WORK on Oedipus is verifier-heuristic
brittleness, not substrate-encoding honesty" is vindicated. The
surviving three-point spread is now truthful signal about
encoding / taxonomy match: Macbeth and Ackroyd sit where they sit
because of their substrate shape (Macbeth's MC Throughline
includes a handful of soliloquy-like beats; Ackroyd's Be-er
approach is cinematic at the edges) — exactly the signal the
spectrum was meant to carry.

Tests: 15 new tests in `test_verification.py` (12 classifier unit
tests + 3 integration pins on the three verifiers' post-EK2
verdict bands). Full suite: 320 → 335 passed.
