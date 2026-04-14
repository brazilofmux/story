# Lowering record — sketch 01

**Status:** draft, active
**Date:** 2026-04-14
**Supersedes:** nothing (synthesis sketch; draws on lowering-sketch-01 and lowering-sketch-02)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md), [lowering-sketch-01.md](lowering-sketch-01.md), [lowering-sketch-02.md](lowering-sketch-02.md)
**Superseded by:** nothing yet

## Purpose

Specify the Lowering record's shape, informed by two concrete
exercises (Oedipus in lowering-sketch-01, Macbeth in
lowering-sketch-02). Architecture-sketch-02 committed (A7) that
lowering between dialects is author-driven, but left the record
shape as a strawman. Two exercises later, the shape is concrete
enough to commit.

The sketch's scope is deliberately narrow:

- **Realization coupling only.** Per lowering-sketch-01 F1 and
  lowering-sketch-02's confirmation, upper-to-lower coupling
  comes in four kinds (Realization / Characterization / Claim /
  Flavor). Lowering records handle *Realization only*. The
  other three kinds use verification (see
  `verification-sketch-01`) or nothing (Flavor). Folding
  Characterization or Claim coupling into the Lowering record
  would be an architectural mistake.
- **Shape, not engine.** The sketch specifies fields and semantics
  of the record; implementation (storage, querying, walker
  integration) is a subsequent prototype task.

The sketch's load-bearing commitments are L1–L10 below.

## What this sketch *is* committing to

1. **L1 — Lowering records carry Realization couplings only.**
   The Lowering mechanism binds an upper-dialect record to the
   lower-dialect records that *realize* it. Characterization
   (pattern classifications) and Claim (moment-pattern and
   trajectory-pattern assertions) are handled by verification,
   not by Lowering. Flavor is not formal at all. L1 is the
   guardrail against scope creep — the Lowering record must
   stay for Realization and resist expansion.

2. **L2 — Record shape.**

   ```
   Lowering {
       id                   (string, unique within the story)
       upper_record         (CrossDialectRef: {dialect, record_id})
       lower_records        (tuple[CrossDialectRef, ...], non-empty
                             unless status = pending)
       annotation           (Annotation: {text, attention,
                             authored_by, review_states})
       position_range       (optional PositionRange, per L7)
       status               ("active" | "pending", per L8)
       authored_by
       τ_a
       anchor_τ_a           (snapshot of max(lower_records' τ_a)
                             at authoring time, per L6)
       metadata             (dict, dialect-specific or boundary-
                             specific extensions)
   }
   ```

   Field-by-field semantics are given in the sections below.
   The shape is the sketch's load-bearing commitment and should
   change only with strong forcing-function evidence.

3. **L3 — Many-to-many binding.** One Lowering points at many
   lower records (the `lower_records` tuple). One lower record
   can be the target of many Lowerings (no uniqueness constraint
   on lower-side records across Lowerings). Binding is
   symmetrically many-to-many; the architecture already named
   this (lowering-sketch-01 "reverse relationships" section).
   No record-level deduplication is performed or required.

4. **L4 — `lower_records` admits typed-fact records and
   description records interchangeably.** Descriptions are
   substrate records per descriptions-01; a Lowering binding to
   a description is still Realization, just targeting the
   interpretive surface rather than the typed surface
   (lowering-sketch-01 F3, F2 refinement). The record shape does
   *not* structurally distinguish description targets from
   typed-fact targets. The verifier (verification-sketch-01) may
   behave differently depending on target kind, but the Lowering
   record's schema is uniform.

5. **L5 — `annotation` carries descriptions-01-style attention.**
   The annotation is prose rationale ("why this binding?"). It
   carries `attention` (structural / interpretive / flavor) per
   descriptions-01's pattern, supports `review_states` (reviewed
   by author or by reader-model partner), and can be superseded
   through the existing proposal queue supersession pattern
   (descriptions-01 OQ1 / description-edit-proposals). Structural
   annotations assert binding ("this Scene binds to this event");
   interpretive annotations discuss how well the binding reads
   ("the Scene's argumentative work is realized partially by
   this event plus the following descriptions"). The annotation
   is part of the substrate of author intent; it is not a
   comment.

6. **L6 — Staleness via `anchor_τ_a`.** Every Lowering captures,
   at authoring time, `anchor_τ_a = max(r.τ_a for r in
   lower_records)`. Comparing `anchor_τ_a` to the current
   `τ_a` of the lower_records (after later edits) yields the
   staleness signal. This is the descriptions-01 staleness
   pattern generalized to Lowerings: when a lower record is
   edited, every Lowering referencing it may need review.
   Staleness is a signal, not an invalidation — an edited
   lower record doesn't automatically break the Lowering; it
   raises the Lowering for author re-review via the proposal
   queue.

7. **L7 — Optional `position_range` for position correspondence.**
   When the upper and lower dialects both use positional
   ordering and the Lowering covers a range, `position_range`
   captures the lower-dialect range that realizes the upper
   record. Shape: `{lower_dialect_coord, min_value, max_value}`.
   Example: a Signpost at `signpost_position = 1` in the
   Dramatic dialect lowers to `SjuzhetEntry(τ_d ∈ [0, 3])` in
   the substrate; the `position_range` is
   `{coord: "τ_d", min: 0, max: 3}`. Position correspondence is
   author-declared per lowering-sketch-01 F4 — the verifier does
   not derive it, and the Lowering record is where it lives.

8. **L8 — `status = pending` for Lowerings authored ahead of
   their lower realization.** An author may know that an upper
   record should lower (Scene(S_tiresias_accusation) wants to
   lower to a `E_tiresias_accusation` event), but the lower
   record hasn't been authored yet. A `pending` status lets the
   Lowering exist as a promissory annotation; `lower_records`
   may be empty under `pending`. A later authoring pass
   converts the Lowering to `active` by populating
   `lower_records` once the lower records are created.
   Rationale: lowering-sketch-01 F5 surfaced substrate gaps as a
   first-class case; `pending` makes the gap visible in the
   Lowering collection, rather than hiding it as "this upper
   record doesn't have a Lowering at all."

9. **L9 — Authored through the proposal queue; never
   synthesized.** Lowering records enter the store only through
   author acceptance via the existing proposal queue. A
   reader-model partner (A11) may *propose* a Lowering record;
   acceptance is an authorial act using the existing walker
   pattern. The architecture never synthesizes a Lowering from
   upper-and-lower evidence; synthesis is out of scope.

10. **L10 — Lowering records do not carry verification logic.**
    A Lowering binds; it does not check. Verification of the
    binding's honesty (does the lower record actually realize the
    upper claim?) is a separate mechanism in
    `verification-sketch-01`. Enforcing the separation at the
    record level is what keeps Lowering small and Verification
    expressive; conflating them would duplicate work and produce
    a messier schema.

L1 through L10 pass architecture-sketch-01's A3 within the
Lowering record's scope: each describes drift the schema catches
rather than content an attentive reviewer could self-police.
Without L1, the record expands to cover non-Realization coupling
and loses focus. Without L6, stale Lowerings go unnoticed.
Without L8, partial lowerings look like architectural problems
(missing Lowerings) rather than what they actually are
(deliberate annotations of upper records whose lower realizations
are pending).

## Field-by-field detail

### `id`

A string, unique within the story's Lowering collection. Stable
across editing — a Lowering's id does not change when its
annotation or lower_records are updated; supersession produces a
new Lowering with a new id and a `metadata["supersedes"]` back-
reference (descriptions-01's supersession pattern applied here).

### `upper_record`

```
CrossDialectRef {
    dialect        ("dramatic" | "substrate" | "dramatica-complete" | ...)
    record_id
}
```

`dialect` is a string naming the dialect. The sketch does not
formalize a dialect registry; the value is whatever the dialect's
authoring tool declares. `record_id` points at a specific record
in that dialect. A Lowering whose `upper_record.dialect` is
`"substrate"` would be pointing *down* past the engine's sink,
which is out of scope (substrate is the lowest managed dialect);
the record shape admits the form but the verifier would reject
it.

### `lower_records`

A tuple of `CrossDialectRef`, each naming a lower-dialect
record. Non-empty under `status = active`; may be empty under
`status = pending` (L8). Order is meaningful only if the author
declares it meaningful in the annotation; the record shape does
not privilege any ordering.

Each ref's `dialect` must be a dialect that sits below the
upper_record's dialect in the stack (or at a sibling position the
stack admits via cross-cutting). The Lowering does not verify
this; the dialect-boundary verifier (verification-sketch-01) does.

### `annotation`

```
Annotation {
    text           (prose rationale)
    attention      (Attention: structural | interpretive | flavor)
    authored_by
    review_states  (tuple of ReviewEntry)
}
```

Attention at the annotation level matters because annotations
themselves can be reviewed: "this Lowering's annotation reads
weak" is a reader-model observation that flows through the
existing review pipe. Structural annotations are
bindings-as-declarations; interpretive annotations discuss how
well a binding reads; flavor annotations are author-side-
commentary not expected to be pressed. The default is
`structural`.

### `position_range` (optional)

```
PositionRange {
    coord           (string: the lower-dialect coordinate name,
                     e.g., "τ_d" for substrate sjuzhet,
                     "narrative_position" for Dramatic)
    min_value       (inclusive)
    max_value       (inclusive)
}
```

Omitted when the Lowering doesn't span a position range (a
Lowering binding a single lower record doesn't need one; a
Lowering binding a set of lower records at the same position
doesn't need one). Present when the binding covers a contiguous
position range and the author wants to declare that range
explicitly. The verifier may use it; the Lowering record just
carries it.

### `status`

```
status: "active" | "pending"
```

`active` is the default. `pending` is used when the Lowering is
authored as a promissory annotation — the upper record exists,
the author intends the lowering, but the lower records don't
exist yet. Transitions: `pending → active` when `lower_records`
is populated; `active → pending` is unusual but admissible if
all lower records get deleted. `pending → declined` is not a
real transition — a Lowering the author no longer wants is
deleted (or superseded); `pending` status is a live intent.

### `authored_by`, `τ_a`

Same semantics as descriptions-01. `authored_by` names the
authoring agent (author, reader-model partner, or another tool);
`τ_a` is the authored-time stamp.

### `anchor_τ_a`

A derived snapshot: `max(r.τ_a for r in lower_records)` at
authoring time. Used for staleness comparison (L6). Updated only
when the Lowering itself is re-authored (i.e., superseded into a
new Lowering).

### `metadata`

Dialect-specific or boundary-specific extensions. Uses include
`metadata["supersedes"]` for supersession chains,
`metadata["source_proposal"]` for tracking which proposal
produced the Lowering when a reader-model partner proposed it,
and `metadata["why_pending"]` explaining the reason a Lowering
is in `pending` status.

## Cross-dialect refs — briefly

`CrossDialectRef` is a new type this sketch introduces (or names
for first-class use — the shape is simple). Fields:

```
CrossDialectRef {
    dialect          (string)
    record_id        (string)
}
```

Two dialect tools referencing each other's records need a common
ref type. `CrossDialectRef` is that type, minimal. A future
dialect-infrastructure sketch may formalize dialect names, refs,
and registry mechanics; for now, the pair is sufficient.

## Relation to architecture-sketch-02

- **A6 (stack of dialects).** Lowering records connect dialects.
  They exist because dialects do; they require the stack's shape
  to be meaningful.
- **A7 (lowering is author-driven).** L9 is A7 restated with the
  record shape: Lowerings are authored through the proposal
  queue, never synthesized. This sketch specifies *what* the
  author is authoring.
- **A8 (verification at boundaries).** Verification is a
  *separate* sketch (`verification-sketch-01`). L10 draws the
  boundary: Lowering records do not carry verification. The
  architecture's separation between authoring (A7) and checking
  (A8) is preserved at the record level.
- **A9 (verifier vocabulary).** The verifier reads Lowering
  records but the record shape does not constrain how it reads
  them. Verifier implementation details live in the sister
  sketch.
- **A10 (dialects opt-in, plural).** Lowering is always between
  two specific dialects; opt-in is a Story-level decision,
  realized by whether the author creates Lowerings for a given
  boundary.
- **A11 (reader-model probe generalizes).** A probe at the
  dialect boundary may propose Lowerings. Acceptance through
  the walker; no new pipe needed.

## Relation to the four coupling kinds

- **Realization → Lowering.** L1. This is the sketch's entire
  scope.
- **Characterization → verification-sketch-01.** Not handled
  here.
- **Claim → verification-sketch-01.** Not handled here. Claim
  splits into moment-pattern and trajectory-pattern sub-kinds
  (lowering-sketch-02 F8); both are verification concerns, not
  Lowering concerns.
- **Flavor → not formalized.** Lives on the description
  surface with `attention = flavor`; doesn't enter the Lowering
  record machinery.

## Relation to other sketches

- **descriptions-01.** Annotation attention and supersession
  patterns are lifted directly (L5, id-stability note under L9).
- **lowering-sketch-01 and lowering-sketch-02.** The two
  concrete exercises this sketch synthesizes. Every commitment
  L1–L10 traces to a finding in those sketches; the sketch is
  not introducing new ideas, only consolidating.
- **dramatic-sketch-01, dramatica-template-sketch-01.** The
  source dialects for the first two exercises. Lowering records
  connect these dialects' records to the substrate.
- **substrate-sketch-05.** The sink dialect. Substrate records
  are the lower side of most Lowerings in the current stack.

## Open questions

1. **OQ1 — Dialect registry.** The sketch uses strings for
   dialect names (`"dramatic"`, `"substrate"`, etc.) without a
   central registry. Is that sufficient forever? Probably yes
   at this project's scale; a richer story-engine with many
   dialects might eventually want a registry. Defer.
2. **OQ2 — Cross-dialect refs vs. typed references.** A
   typed-reference approach (imported dialect types carry
   record refs naturally) would be more IDE-friendly than
   string pairs. Trade-off: typed refs require dialect modules
   to import each other, which architecture-02 deliberately
   avoided (dialects stand alone). String-paired refs preserve
   dialect independence at the cost of type-checker help.
   Defer; revisit when implementation starts.
3. **OQ3 — `pending` Lowerings as first-class or special-case.**
   L8 admits `pending` Lowerings. Are they important enough to
   be first-class — with their own reports, walker handling,
   and proposal-queue interactions — or are they special-case
   entries that mostly look like `active` but with empty
   `lower_records`? The sketch leaves this open; first
   implementation will clarify.
4. **OQ4 — Ordering within `lower_records`.** The sketch says
   ordering is meaningful only if the author says so in the
   annotation. Is there ever a case where ordering is
   *intrinsic* to the binding (e.g., the substrate records
   should be read in a specific order to realize the upper
   record)? Possibly for Scenes that bundle multiple events
   with cause-and-effect relations. The sketch provisionally
   says no; a future pass can add an `ordered: bool` flag if
   needed.
5. **OQ5 — Multiple upper records sharing one Lowering.** The
   sketch commits to one upper record per Lowering. But
   sometimes two upper records might *jointly* realize through
   the same lower records — e.g., a Scene and a Beat both bind
   to the same event bundle. The current shape requires two
   separate Lowerings. Is that right, or should
   `upper_records` (plural) be admitted? Provisionally: keep
   it one-to-many (one upper, many lowers); two upper records
   sharing a lower set is two Lowerings. Revisit if
   encountered.
6. **OQ6 — Cross-story Lowerings.** A Lowering's upper and
   lower records must be within the same Story (a Story being
   the scope of the dialect's base record). What about
   cross-Story or cross-encoding relationships? Out of scope;
   same-Story only for sketch 01.
7. **OQ7 — Lowering collections as first-class records.** A
   Story accumulates many Lowerings; is the *collection*
   itself a first-class record (enabling review of the
   collection as a whole, completeness metrics, etc.)? The
   sketch treats Lowerings as individual records; a
   collection-wrapper might be a future refinement.

## What happens next

1. **Draft `verification-sketch-01`** as the sibling. Lowering
   and Verification are the load-bearing pair; L10 explicitly
   defers verification concerns to that sketch. The pair needs
   to land together to be implementable.
2. **First implementation pass.** Once both sketches land, a
   `Lowering` record type can be added to the substrate
   prototype (as tooling, not substrate-core; Lowerings are
   cross-dialect artifacts, not substrate records). The
   existing proposal-queue machinery extends naturally to
   handle `LoweringProposal` alongside the existing
   `ReviewEntry`, `AnswerProposal`, `EditProposal`.
3. **Produce a concrete set of Lowerings for Oedipus or
   Macbeth.** With both record sketches in hand, lowering-
   sketch-01's Oedipus exercise or lowering-sketch-02's
   Macbeth exercise can be converted from prose into actual
   Lowering records. The exercise becomes a first
   end-to-end-implemented cross-boundary example.
4. **Revisit the dramatic-sketch-02 forcing functions.** Once
   Lowerings are concrete and a verifier can run, some of
   dramatic-sketch-02's open items (Template-level schema
   extension, derived-field semantics for Solution/Symptom/
   Response) will clarify — the verifier's constraint checks
   will pressure the dialect's shape from below.
