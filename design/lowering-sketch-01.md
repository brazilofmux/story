# Lowering — sketch 01 (Oedipus exercise)

**Status:** draft, active
**Date:** 2026-04-14
**Supersedes:** nothing (new topic)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md), [dramatic-sketch-01.md](dramatic-sketch-01.md), [dramatica-template-sketch-01.md](dramatica-template-sketch-01.md)
**Superseded by:** nothing yet

## Purpose

Attempt a concrete lowering from an upper-dialect encoding down
to a substrate encoding, for one specific story (Sophocles' *Oedipus
Rex*), and see what the exercise reveals about architecture-sketch-02's
lowering claim. The upper encoding is the dramatica-complete Template
sketched in dramatica-template-sketch-01; the lower encoding is the
existing `oedipus.py` substrate encoding. Both exist in some form
already; the exercise is to author a concrete set of Lowering
records that bind them.

The deeper question this is meant to answer: architecture-sketch-02's
A6–A11 commit to a specific shape for how dialects connect
(author-driven lowering records; automated verification at each
boundary emitting observations). That shape has been asserted but
never pressured against a real example. Doing so will surface
what the Lowering mechanism actually needs to look like, what
cases the architecture handles cleanly, and where it cracks.

A secondary question this exercise is meant to answer: the
"sandwich question" — given a rich upper dialect (Dramatica) and
a rich lower dialect (substrate), is a middle dialect necessary,
or can Dramatica lower directly to substrate? The exercise forces
this from below.

This sketch is deliberately exploratory. Its output is *findings*,
not commitments. A future `lowering-sketch-02` (or
`lowering-record-sketch-01`) can synthesize commitments once
several exercises like this one have been done. Findings are
numbered F1..F7.

## What this exercise *is*

- A design walk-through. Prose descriptions of proposed Lowering
  records for the Oedipus dramatica-complete encoding against
  the `oedipus.py` substrate encoding. No code; no new records
  in either prototype.
- A diagnostic. For each upper record in the dramatica-complete
  encoding, the exercise asks: what substrate record(s) (or
  query) realizes it? It asks that honestly and reports what it
  finds.
- A pressure test for architecture-sketch-02. Where the
  architecture's lowering shape carries the case cleanly, the
  exercise confirms it. Where it cracks, the exercise names the
  crack.
- A pressure test for dramatic-sketch-01 and
  dramatica-template-sketch-01 from a direction those sketches
  did not try: the top-down view. Encoding a story in an upper
  dialect, then trying to lower it, surfaces dialect gaps
  different from the ones the Template depth probe surfaced.

## What this exercise is *not*

- A sketch of the Lowering record's shape. That sketch comes
  later, informed by this exercise and at least one other.
- A revision to any existing sketch. Where this exercise names
  gaps in dramatic-sketch-01, dramatica-template-sketch-01, or
  architecture-sketch-02, the gaps become forcing functions for
  those sketches' follow-ons, not retroactive revisions.
- An implementation. No code is produced.
- A complete lowering of Oedipus. Several upper records have
  substrate gaps (the substrate encoding cuts Tiresias, Creon,
  and most of the play's sjuzhet); the exercise does not fill
  those gaps. It reports them.

## The materials

### Upper encoding — Oedipus in dramatica-complete

Drawn from dramatica-template-sketch-01's worked example plus
the base dramatic-sketch-01 Oedipus encoding:

- 1 Story (S_oedipus_rex), with Template = dramatica-complete,
  story_goal = "identify the pollution causing the plague and
  expel it", story_consequence = "the plague continues; the
  city dies".
- 1 Argument (A_knowledge_unmakes), premise "knowledge of self
  is the unmaking of the self", resolution_direction = affirm.
- 4 Throughlines (T_overall_plague, T_mc_oedipus,
  T_impact_jocasta, T_relationship_oj), each with a DomainAssignment
  covering all four Domains once.
- 6 Characters (C_oedipus, C_jocasta, C_tiresias, C_creon,
  C_shepherd, C_messenger), with Character Function assignments
  per the dramatica-complete Template's 8-slot catalog (one slot
  intentionally unfilled: Antagonist).
- 9 Scenes (S_prologue_plague, S_tiresias_accusation,
  S_jocasta_doubt_speech, S_messenger_arrives,
  S_shepherd_testimony, S_anagnorisis, S_jocasta_hangs,
  S_self_blinding, S_exile), with narrative_position and
  declared `advances` pointers.
- 1 Stakes record (Stakes_mc_oedipus) for the Main Character
  Throughline.
- 6 DynamicStoryPoints (Resolve=Change, Growth=Stop,
  Approach=Do-er, Limit=Optionlock, Outcome=Success,
  Judgment=Bad).
- 4 DomainAssignments.
- QuadPicks at Concern / Issue / Problem levels per Throughline
  (partial — only the MC Throughline's Problem=Pursuit pick is
  fully sketched).
- Signposts — four per Throughline (only MC Throughline's four
  are sketched concretely).

### Lower encoding — Oedipus in substrate (`oedipus.py`)

- 14 Entities: 6 named characters (`oedipus`, `jocasta`, `laius`,
  `polybus`, `merope`, `messenger`, `shepherd`) + 3 identity-
  placeholder entities (`the-exposed-baby`, `the-crossroads-
  killer`, `the-crossroads-victim`) + 4 locations + 1 more.
  Notably *missing*: `tiresias`, `creon`.
- 12 FABULA events spanning the pre-play chronology (birth,
  exposure, upbringing, oracle, crossroads killing, marriage)
  and the in-play sjuzhet (Jocasta mentions crossroads,
  messenger's reveals, both anagnoreses, shepherd's testimony).
- 7 SjuzhetEntries at τ_d = 0, 5, 7, 8, 9, 12, 13.
- PREPLAY_DISCLOSURES — 12 disclosures at τ_d=0 (the audience
  enters the play with myth facts and identity facts pre-loaded).
- 5 Descriptions: `D_oedipus_anagnorisis_texture`,
  `D_anagnorisis_logical_payload`,
  `D_parricide_incest_authored_not_derived` (+ its accepted
  answer), `D_view_cannot_see_τ_d`.

## The lowering attempt, by finding category

The walk-through below is organized by the *shape* of the
lowering rather than by upper-record type, because the interesting
finding is that lowerings come in several distinct shapes. Each
sub-section names the shape and gives examples.

### Clean lowerings (1-to-1 or 1-to-small-set)

These are the boring cases — and the sketch should be honest
that boring is good. A lowering mechanism that handled *only*
these cases would still be useful.

- **`Character(C_oedipus)` → `Entity("oedipus")`.** One-to-one.
  The upper Character's id and name match the substrate Entity's
  id and name (or can be author-declared to match). The
  Character's `functions` field (e.g., `[Protagonist, Emotion]`)
  has no substrate counterpart and stays upper-dialect-only.
- **`Character(C_jocasta)` → `Entity("jocasta")`, `Character(C_shepherd)`
  → `Entity("shepherd")`, `Character(C_messenger)` →
  `Entity("messenger")`.** Same pattern.
- **`Scene(S_anagnorisis)` → `Event(E_oedipus_anagnorisis)` +
  `SjuzhetEntry(τ_d=13)` + `Description(D_oedipus_anagnorisis_texture)` +
  `Description(D_anagnorisis_logical_payload)`.** One-to-four.
  The Scene's Dramatic identity ("the anagnorisis") maps to one
  substrate event, its sjuzhet entry, and the two descriptions
  that gloss it. The lowering record names the four targets; the
  author's annotation explains the binding.
- **`Scene(S_messenger_arrives)` → `Event(E_messenger_polybus_dead)` +
  `Event(E_messenger_adoption_reveal)` + `SjuzhetEntry(τ_d=7)` +
  `SjuzhetEntry(τ_d=8)`.** One-to-four, but the Scene collects
  multiple events (the messenger's two-part reveal) under one
  Scene-level bundle.

The clean cases suggest the Lowering record shape
architecture-02 strawmanned (`upper_record`, `lower_records`
as a tuple, an annotation) is sufficient here. Multi-record
targets are natural; the tuple-form covers it.

### Substrate gaps — lowerings that cannot be authored

These are upper records that *would* lower cleanly except the
substrate doesn't contain the required records.

- **`Character(C_tiresias)` → no substrate Entity exists.**
  `oedipus.py` explicitly cuts Tiresias ("Tiresias, Creon, and
  the chorus are cut"). The upper encoding commits to Tiresias
  as a Character carrying the Reason function; the lower
  encoding has no corresponding Entity.
- **`Character(C_creon)` → no substrate Entity exists.** Same
  situation.
- **`Scene(S_tiresias_accusation)` → no substrate event exists.**
  The Scene would bind to an `E_tiresias_accuses` event and
  its sjuzhet entry, neither of which the substrate encoding
  contains.
- **`Scene(S_jocasta_hangs)` → no substrate event exists.**
  Jocasta's suicide is a crucial plot beat; `oedipus.py`'s
  slice cuts it.
- **`Scene(S_self_blinding)` → no substrate event exists.**
  Similarly cut.
- **`Scene(S_exile)` → no substrate event exists.** Cut.

These substrate gaps are real design pressure from the lowering
exercise, visible nowhere else. The decisions they surface:

- *Extend the substrate encoding* to cover Tiresias, Creon, and
  the post-anagnorisis plot beats. This is authorial work,
  bounded and concrete.
- *Prune the upper encoding* to match the substrate slice. This
  keeps the upper encoding honest — you don't get to claim a
  Scene you don't have a realization for — but it makes the
  Dramatica-complete encoding incomplete.
- *Mark the lowering as pending*. Admit the upper record
  exists, admit the lower records don't, and annotate. A
  well-designed Lowering record shape probably admits this
  state explicitly (a `pending` status, with the unrealized
  upper record visible).

The exercise favors extending the substrate. The substrate
encoding was cut for the identity-and-realization probe, not
for the full-play encoding a Dramatica lowering wants.
Extending is a bounded next prototype task.

### Upper records with no lowering target

Some upper records do not realize in the substrate, and this is
fine — they are upper-dialect-only characterizations.

- **`DomainAssignment(T_overall_plague, domain="situation")`.**
  The Domain choice is a statement about *what kind of pressure
  the Throughline exerts* (external state). It does not realize
  as any substrate record or substrate fact. The lowering is
  empty; the assignment is a pure-upper claim.
- **`QuadPick(concern="understanding")` on T_overall_plague.**
  Same. "Understanding" as a Concern is a characterization of
  the Throughline's shape. Nothing in the substrate says "this
  Throughline is about Understanding"; the substrate says what
  happens, and the upper dialect characterizes it.
- **`QuadPick(issue=...)` and `QuadPick(problem=...)`.** Same
  pattern. The Dramatica hierarchy of Domain / Concern / Issue
  / Problem is progressively more specific characterization,
  but none of it has a direct substrate realization.
- **`Argument.domain = "moral-philosophical"`.** A thematic tag,
  no substrate realization.

A Lowering mechanism that requires every upper record to have a
lower-side binding would mishandle these. The architecture has
to admit *empty* lowerings (or explicit "no lowering, by design"
annotations) as first-class. This is F1 below.

### Lowerings to substrate queries, not substrate records

Some upper records lower to *patterns* or *queries* over
substrate state, not to specific substrate records.

- **`DynamicStoryPoint(axis=outcome, choice=success)`.** Outcome
  = Success means the Story Goal is achieved. The Story Goal is
  "identify the pollution causing the plague and expel it." The
  substrate records that realize this: Oedipus's holding
  `identity(oedipus, the-crossroads-killer)` at KNOWN, plus
  `parricide(oedipus, laius)` being world-true, at τ_s ≥ 13.
  Lowering here is not a single substrate record — it is a
  *state-at-a-moment claim*.

  One way to express it: the lowering binds to the earliest
  substrate event at which the Goal-satisfaction state first
  holds. For Oedipus, that is `E_oedipus_anagnorisis`. A second
  way: the lowering binds to a *query* against the substrate
  at a moment. The verifier's check would be: does
  `world_holds(parricide(oedipus, laius)) at τ_s ≥ 13` hold
  in the substrate? Does `oedipus holds identity(...) at
  τ_s=13` hold? Binding to a query is richer than binding to
  records because it can check derived state.

- **`DynamicStoryPoint(axis=judgment, choice=bad)`.** Judgment
  is about the MC's personal-satisfaction outcome. Bad means
  the MC ends in a worse state. The lowering binds to... what?
  Oedipus's self-blinding event (which is not in the substrate,
  see gaps above) or, if we prune, to the state at the
  anagnorisis where `gap_real_parents` closes into a catastrophe.
  Either way, lowering is to a substrate *state pattern*: "at
  the end, `suffering(oedipus)` holds (or is derivable)." For
  the current substrate encoding there is no `suffering`
  predicate; for the verifier to work, either the predicate
  needs to exist or the Judgment dimension doesn't verify.

- **`Outcome=Success × Judgment=Bad = Personal Tragedy`** (the
  canonical Dramatica derivation). This is an upper-dialect
  derived fact from two DynamicStoryPoint records. It doesn't
  lower as such — it emerges from the two lowerings of its
  constituents. The Personal Tragedy claim is verified by
  checking *both* Outcome and Judgment's lowerings
  simultaneously.

F2 below: the Lowering mechanism must admit query/pattern-shaped
targets, not just record-shaped targets.

### Lowerings to descriptions, not typed facts

Some upper records have no typed-fact realization in substrate
but have description-surface realizations.

- **`Stakes(Stakes_mc_oedipus)`.** The Stakes record says
  Oedipus's identity, his wife's life, and his sight are at
  risk. The substrate has no typed predicate for "at-risk-ness"
  — and it probably shouldn't (that would be an A3 fail: "at
  risk" is a hypothetical-loss claim, interpretive at its core).
  But the substrate could carry descriptions that articulate
  the stakes. `D_stakes_oedipus_risk_of_sight` (a description
  kind = "stakes-texture") would be a legitimate substrate
  anchor for the Stakes record's lowering.

  So: `Stakes_mc_oedipus` lowers to a description (possibly
  anchored to one of the in-narrative events that makes stakes
  visible — the plague event, an early scene that foreshadows
  the self-blinding gesture). Not to typed facts.

- **`Argument.resolution_direction = affirm`** may lower
  partially to descriptions too — specifically, descriptions
  that articulate *how* the premise is affirmed. Note that
  the current substrate encoding has
  `D_anagnorisis_logical_payload` — a description explicitly
  articulating how the Argument's premise "knowledge unmakes"
  is realized at the anagnorisis. That description *is*, in
  effect, the lowered-to-description-form of part of the
  Argument's affirmation.

F3 below: lower-side bindings admit both typed-fact targets
and description targets.

### Verification vs. lowering — not always the same relationship

Some upper records have no *lowering* at all (no substrate
realization), but have a *verification* relationship with
substrate state — does the substrate exhibit the signature the
upper record claims?

- **`Argument(A_knowledge_unmakes)`.** No single substrate
  record realizes the Argument. The Argument's *premise*
  ("knowledge unmakes") is a claim about the whole
  state-trajectory: does the substrate show the protagonist's
  knowledge increasing and the protagonist's standing
  decreasing, coincidentally, over narrative time? That's a
  verification question — a check across substrate state — not
  a lowering binding to specific records.

  The distinction matters: a Lowering record can be authored
  for things that *realize*; it makes less sense for things
  that *are true about* the realization. The Argument is the
  latter.

  One model: the Argument has *no Lowering record*, but the
  cross-boundary verifier at the Dramatic↔Substrate boundary
  runs a check — "does the substrate's fold trajectory match
  the Argument's declared resolution_direction under some
  signature criterion?" — and emits an observation. This is
  pure verification, not lowering.

  Another model: lower the Argument to the full set of
  substrate records that exhibit the pattern (every event
  + every description + every disclosure). This is
  technically lowering-to-everything, which is indistinguishable
  from "no lowering" in practice.

  The first model is cleaner. Lowerings are for upper records
  that specific lower records *realize*; verification is for
  upper records that are true *about* the substrate as a whole.

F6 below: the architecture's distinction between Lowering
(author-driven binding) and Verification (automated check)
turns out to be more than a labor division — they are genuinely
different relationships, and some upper records engage one but
not the other.

### Position correspondence — needs per-lowering declaration

Position-based upper records (Signposts, narrative-position on
Scenes) raise a specific question: how do upper-dialect positions
map to substrate positions?

- **`Signpost(throughline=T_mc_oedipus, signpost_position=1,
  element="learning")`.** Position 1 of the MC Throughline
  names the initial investigation phase. Which substrate
  sjuzhet entries fall in this signpost's span?

  The Dramatic dialect's `narrative_position` is per-Dramatic-
  Story ordering; the substrate's sjuzhet has τ_d. They are
  different coordinate systems, and no formal correspondence is
  declared. An author lowering a Signpost authors a binding:
  "Signpost 1 covers `SjuzhetEntry(τ_d=0)` through
  `SjuzhetEntry(τ_d=8)`" — a τ_d range.

  Substrate position range → upper-dialect position range is
  author-declared, not derived. This matches A7 (lowering is
  author-driven) but specializes it: position correspondence
  across dialects is not inferable even when both dialects use
  positional ordering.

F4 below: position correspondence between dialects is authored,
not derived.

### Reverse relationships — one substrate record realizes many upper records

A single substrate event can be the lowering target of many
upper records, at different levels of the Dramatica apparatus.

- **`Event(E_oedipus_anagnorisis)` realizes:**
  - `Scene(S_anagnorisis)` (at the Scene level).
  - The final Beat of `T_mc_oedipus` (the MC's Peak).
  - The final Beat of `T_relationship_oj` (the Relationship's
    collapse).
  - `Signpost(T_mc_oedipus, position=4, element="obtaining")`
    — Oedipus obtains the truth (and is undone by it).
  - `DynamicStoryPoint(outcome=success)` — the Goal is
    achieved at this event.
  - Part of the Argument's affirmation (the premise lands here).

The Lowering mechanism has to admit many-to-many relationships
between upper and lower records (architecture-02 already names
this). The exercise shows it happening in practice: one substrate
event is a shared target of multiple upper records at multiple
Dramatica levels. Each such binding is a separate Lowering
record; they compose.

## Findings

### F1 — Not every upper record lowers

Many upper records are *characterizations* without substrate
realizations. Domain assignments, Concern / Issue / Problem
picks, thematic tags on Arguments — all legitimate upper-dialect
records with no substrate counterparts. The Lowering mechanism
must admit "this upper record has no lowering, by design" as a
first-class state, not a gap.

*Implication:* A `Lowering` record should not be mandatory for
every upper record. A collection of Lowerings for a Story is
intrinsically partial. A record that specifically affirms
"no lowering" (distinguished from "lowering not yet authored")
may be useful for documentation purposes.

### F2 — Lowering targets are heterogeneous

Some upper records lower to:

- specific substrate records (Character → Entity)
- sets of substrate records (Scene → Event + SjuzhetEntry +
  Descriptions)
- substrate queries or state patterns (DynamicStoryPoint(outcome
  = success) → "world_holds(parricide(oedipus, laius)) at τ_s ≥
  13")

The first two compose naturally into a tuple of record
references. The third pressures the Lowering record's
`lower_records` shape: either the shape admits queries as
first-class targets (a `lower_query` field alongside
`lower_records`), or query-style lowerings get expressed
awkwardly as "every record that would match the query."

*Implication:* The Lowering record's lower-side needs to admit
both record references and query/pattern targets.

### F3 — Some upper records lower to descriptions

Stakes lowers (naturally) to descriptions rather than to typed
facts. Parts of the Argument's realization lower to descriptions
(the existing `D_anagnorisis_logical_payload` is, in effect, a
description-form realization of part of the Argument).

The substrate's description surface is already part of the
substrate dialect. Lowering to a description is lowering to a
substrate record — just to the description-surface part rather
than the typed-fact part.

*Implication:* The Lowering record does not need to distinguish
description targets from typed-fact targets structurally — both
are substrate records. But the *verifier* may behave differently
(a description can't be checked for factual consistency; it can
only be checked for anchoring, authorship, and review state).

### F4 — Position correspondence is author-declared

Upper-dialect positional ordering (narrative_position in
Dramatic; signpost_position) does not auto-map to substrate
sjuzhet ordering (τ_d). Signposts, Scenes with narrative_position,
and any position-based upper record that spans a range of
substrate time must declare the correspondence explicitly in
the Lowering record.

*Implication:* Lowerings may carry range-expressions on the
lower side ("substrate sjuzhet entries at τ_d in [0, 8]"),
which is a query/pattern again — supporting F2.

### F5 — Substrate gaps surface concretely via lowering

Upper records that commit to story elements the substrate
encoding doesn't contain (Tiresias, Creon, the post-anagnorisis
plot beats) cannot be lowered. The gaps are visible at the
lowering attempt, not visible from within either dialect alone.

*Implication:* Lowering is a forcing function for substrate
completeness under a given upper encoding. If a Story commits
Dramatica-complete records, the substrate encoding either
realizes all of them or the lowering surface is incomplete.
Substrate completeness is relative to the upper encoding's
commitments.

This is useful in both directions: if the substrate encoding is
deliberately a slice (as `oedipus.py` is — the identity-probe
slice), the Dramatica-complete upper encoding should match the
slice, not the full play. If the upper encoding is the full
play, the substrate encoding needs to be extended to match.

### F6 — Verification and lowering are different relationships

The Argument has no lowering (no substrate records specifically
realize it); it has a verification relationship (does the
substrate's trajectory match the Argument's declared signature?).
Architecture-02 named Lowering and Verification as separate, and
this exercise confirms they are genuinely different — they
are not labor-divisions of the same thing, they are different
kinds of relationship between upper and lower records.

*Implication:* The architecture's split between Lowering
(author-authored binding; A7) and Verification (automated
check; A8) is load-bearing. A future lowering-record sketch
needs to preserve this split; a future verification sketch
needs to own the verification surface independently.

### F7 — Derivation composes with lowering

The Outcome=Success lowering depends on Oedipus holding
`identity(oedipus, the-crossroads-killer)` at KNOWN, plus
world-true `parricide(oedipus, laius)`. The identity is an
authored fact. But `parricide` is currently an authored world-
fact in the substrate, and under inference-model-sketch-01 it
would be a *derived* fact. Either way, the Lowering's
verification consults substrate state that may include derived
facts.

*Implication:* Lowerings that bind to queries/patterns pressure
the substrate's inference surface. The verifier runs its check
over substrate state that includes derived facts (per
inference-01's `holds_derived`). This connects the two sketches:
inference-01 is what makes some Lowerings' verification
tractable.

## The sandwich question

The exercise was partly meant to answer: is a middle dialect
between Dramatica and substrate necessary, or can Dramatica
lower directly?

**Answer: direct lowering is possible for most upper records.**
The exercise showed clean lowerings for Characters, Scenes,
Throughlines (as sets of substrate records), DynamicStoryPoints
(as queries), Stakes (as descriptions). The ones that do not
lower at all (Domain / Concern / Issue / Problem quad picks) do
not need a middle dialect — they are pure-upper characterizations
with no substrate realization in any form. No intermediate
would change that.

**However, a middle dialect *would* make some lowerings more
natural.** Specifically:

- Signposts' position correspondence to substrate sjuzhet would
  be cleaner if a middle dialect owned "acts" and "act positions"
  against which both Signpost positions (upper) and sjuzhet
  entries (lower) could register. The middle would provide a
  shared position vocabulary.
- Scenes as units of argumentative work (upper) could lower to
  *plot-beats* (middle) rather than directly to events + sjuzhet
  entries + descriptions. The middle layer makes the
  many-to-many binding cleaner.
- Tension-curve observations about pacing (which the Dramatic
  dialect deliberately excludes) would live naturally in a
  middle Structural dialect.

The middle is *useful but not strictly required*. Architecture-02
A10 already admits this: dialects are opt-in. A Story author who
cares about pacing can add Structural records and their Lowerings;
an author who doesn't care can skip the middle and lower Dramatica
directly to substrate.

**Practical conclusion for now:** keep the stack flat (Dramatica
→ substrate), add Structural as a parallel opt-in pole if and
when the exercise shows it earning its keep. The exercise did
not produce a case where Structural was strictly necessary.

## Relation to architecture-02 A6–A11

- **A6 (stack of dialects).** Vindicated. The exercise worked
  within the stack shape without needing architectural
  revisions.
- **A7 (lowering is author-driven).** Vindicated and
  specialized: the exercise showed that position
  correspondence, annotation rationale, and heterogeneous
  target types all need author judgment. A verifier couldn't
  have derived these lowerings.
- **A8 (verification at boundaries emits observations).** Not
  directly exercised (the sketch is a design exercise, no
  automated verifier ran). The sketch's *manual* verification
  (checking that each proposed Lowering actually makes sense)
  is the human-run analog of what A8 specifies.
- **A9 (verifier speaks upper vocabulary, evaluates via lower
  queries).** Implied to be needed by F2 (query-shaped lower
  targets) and F7 (derivation composition). The verifier must
  speak Dramatic-upper vocabulary and issue substrate-lower
  queries.
- **A10 (dialects are opt-in, plural).** Vindicated. The
  sandwich-question answer turns on this.
- **A11 (reader-model probe generalizes as cross-boundary
  partner).** Not exercised. But the sketch's findings suggest
  a natural probe invocation: given the upper encoding + the
  lower encoding + the author's proposed Lowerings, a reader-
  model probe could emit reviews ("this Lowering's annotation
  reads weak") and proposals ("have you considered lowering
  Stakes_mc_oedipus to a description anchored on
  E_marriage_and_crown?"). That is the natural next probe
  forcing function.

## Forcing functions for a future `lowering-record-sketch-01`

This exercise hands the record-shape sketch a concrete brief.
When that sketch is drafted, it will need to address:

1. **Optional lowerings.** Not every upper record lowers.
   A Lowering collection for a Story is intrinsically partial.
   Explicit "no-lowering-by-design" records may be useful
   documentation.
2. **Heterogeneous lower-side targets.** Lowerings admit
   tuples of record references *and* query/pattern targets
   *and* description targets. The record shape must carry all
   three.
3. **Position correspondence as first-class.** When upper and
   lower dialects both have positional ordering, their
   correspondence is author-declared and often range-shaped
   (e.g., `τ_d ∈ [0, 8]` for one Signpost).
4. **Staleness.** Per architecture-02's staleness note:
   Lowerings reference records that can change. The Lowering's
   `anchor_τ_a` compared to its targets' `τ_a` is the staleness
   signal.
5. **Many-to-many binding.** One lower record can be the
   target of many Lowerings; one Lowering can point at many
   lower records. Symmetric.
6. **Annotation attention.** The Lowering's annotation is
   prose rationale. The descriptions-01 pattern (attention
   structural/interpretive/flavor + review state + staleness)
   carries over.
7. **Separation from verification.** The Lowering record does
   not duplicate verification logic; it is the authored binding.
   The verifier is a separate machinery that reads Lowerings.

## What happens next

1. **Extend the substrate encoding.** The lowering exercise's
   most concrete prototype action is extending `oedipus.py` to
   cover Tiresias, Creon, and the post-anagnorisis plot beats
   (S_jocasta_hangs, S_self_blinding, S_exile). This isn't
   about the design; it's about making a future lowering of
   Dramatica-complete-Oedipus possible in full.
2. **Consider a cross-boundary reader-model probe invocation.**
   Feed the probe the upper encoding + lower encoding + a set
   of proposed Lowerings and have it emit reviews + proposals.
   This would exercise A11 for the first time at a real
   boundary.
3. **Draft `lowering-record-sketch-01`** using this exercise's
   findings as the concrete brief. Define the Lowering record's
   fields: `id`, `upper_record`, `lower_records`, `lower_query`,
   `annotation`, `position_range`, `authored_by`, `τ_a`,
   `metadata`. Specify how annotations carry attention.
4. **Draft `dramatic-sketch-02`** addressing
   dramatica-template-sketch-01's six forcing functions. The
   lowering exercise didn't pressure those functions further
   (they were already known), but it did add evidence for F2
   here — Templates extending the dialect with record types
   needs to admit query-shaped Lowering targets cleanly when
   the Template's records lower.
5. **Run the exercise on a second story.** Macbeth, Brothers
   Karamazov, or Remains of the Day. A second exercise would
   show whether Oedipus's findings generalize; the record-shape
   sketch gains a second data point.
6. **Revisit the "sandwich question" when a second upper
   dialect exists.** The current answer (direct lowering works;
   middle dialect is opt-in) is based on one upper dialect. A
   Structural or Pacing dialect as a second pole would
   re-pressure the question.
