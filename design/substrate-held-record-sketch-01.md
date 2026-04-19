# Substrate Held record — sketch 01

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (new topic — record-shape detail for the
Held fold-output / effect-input record substrate-sketch-05 K1 and
substrate-effect-shape-sketch-01 ES3 both name but neither
structurally specifies)
**Frames:** [substrate-sketch-05](substrate-sketch-05.md)
(§The three time axes K1 knowledge-projection fold — "per agent,
per story-time, per branch: a set of held propositions with
slot, via, and provenance"), [substrate-effect-shape-sketch-01](
substrate-effect-shape-sketch-01.md) (§Scope OUT Held —
"Held is an OUTPUT of folding effects, not an effect kind. A
future sketch … specifies it"), [identity-and-realization-
sketch-01](identity-and-realization-sketch-01.md) (I7 —
"substitution fires only on KNOWN identities"; I3 — "held set
remains literal"; §Sternberg-stays-literal — "the author
authors a KnowledgeEffect with `remove=True` targeting the
GAP record — the same mechanism that has always been available")
**Related:** [substrate-entity-record-sketch-01](substrate-entity-
record-sketch-01.md) + [substrate-prop-literal-sketch-01](
substrate-prop-literal-sketch-01.md) (record-shape sketch
precedent), [production-format-sketch-01](production-format-
sketch-01.md) §PFS2 catches real drift (same methodology this
sketch applies), [architecture-sketch-01](architecture-sketch-
01.md) A3 (drift discipline), [architecture-sketch-02](
architecture-sketch-02.md) (grid-snap)
**Superseded by:** nothing yet

## Purpose

Structurally specify the **Held** record — the per-proposition
cell that lives inside an agent's `KnowledgeState`, produced by
the K1 knowledge-projection fold and (under this sketch) also
the shape an author supplies on a `KnowledgeEffect`.

Two existing sketches gesture at Held without specifying it:

- Substrate-sketch-05 §K1 commits that `project_knowledge`
  returns "per-agent held propositions with slot, via, and
  provenance" but never enumerates the fields.
- Substrate-effect-shape-sketch-01 explicitly defers Held
  (ES3 §Scope OUT: "Held is … a future sketch specifies it").

This sketch closes the gap. The schema derives
(`production-format-sketch-04`, pending); the canonical
`schema/held.json` lands behind that sketch.

**Derivation discipline.** First-principles from what the fold
actually does and from what the authoring surface actually needs
— not from the Python prototype's `Held` dataclass. The
prototype is a conformance check. Where sketch and Python
disagree, sketch wins (or sketch explicitly amends; see §Amendments
below for one such case).

## Why now

- Two layers above — effect-shape-sketch-01 and identity-and-
  realization-sketch-01 — reference Held fields (`slot`, `via`,
  `provenance`) without a canonical shape. Production-format
  work on Event has already stubbed around this gap; closing
  it unblocks the Held schema and tightens the KnowledgeEffect
  schema.
- **State-of-play-06 research item #2 is miscalibrated.**
  Item #2 framed the 7 remaining `remove=True` KnowledgeEffect
  cases as residue of identity-and-realization-sketch-01's
  retired "realization-removes-propositions" workaround, and
  predicted the audit baseline "drops to 0" after cleanup.
  Reading the encodings shows the retirement has **already
  happened** (oedipus.py §Authoring conventions, lines 36–42:
  "Factual dislodgements … stay as `remove=True` knowledge
  effects. Those are legitimate factual updates … distinct from
  the realization-driven rewrite"). All 7 remaining cases route
  through the `remove_held` helper each encoding defines for
  evidence-triggered dislodgement — the pattern identity-and-
  realization-sketch-01 §Sternberg-stays-literal explicitly
  endorses. This sketch both (a) makes that endorsement
  first-class by committing `remove` as a field on
  KnowledgeEffect, and (b) corrects the state-of-play's
  predicted cleanup target (the audit baseline is the intended
  final state, not drift to zero).
- Corpus survey — 102 unique events across 5 encodings (458
  with re-export inflation, per state-of-play-06 §Conformance
  dispositions) — exercises every Held shape dimension the
  sketch needs to commit to, including the 7 `remove=True`
  cases deduped at event-id level.

## Scope — what the sketch covers

**In:**

- The Held record's field shape: `prop`, `slot`, `confidence`,
  `via`, `provenance`.
- The slot closed vocabulary and its relationship to identity
  substitution (I7) and Sternberg-curiosity queries.
- The confidence closed vocabulary and its relationship to
  slot (paired; orthogonal in principle, co-varying in practice).
- The commitment that Held's shape is **authored**, not
  fold-derived — the author specifies the Held record on a
  KnowledgeEffect; the fold writes it into the KnowledgeState
  verbatim (with later-wins-on-conflict semantics).
- The corresponding amendment to substrate-effect-shape-sketch-
  01 ES3 (§Amendments below): the effect carries a Held
  record and an optional `remove` polarity; slot/confidence/
  provenance are thereby effect-input, not fold-derived-from-via.
- Timelessness at record level (parallel to SE5, ES7, PL7).

**Out:**

- **Fold-implementation mechanics.** How K1 resolves conflicting
  effects, interprets via=forgetting, handles branch scope, or
  indexes Held records by Prop is fold-layer concern, not
  record-shape concern. A future `substrate-knowledge-fold-
  sketch-01` addresses. See OQ5.
- **Identity substitution semantics.** Identity-and-realization-
  sketch-01 owns. This sketch only references I7's constraint
  on which slot participates.
- **The reader's Held-set.** Substrate-sketch-05 §Entities K2
  says the reader is "an agent of a distinct kind". Whether the
  reader's projection uses the same Held record shape as a
  character-agent — the sketch's commitment: yes, same shape;
  via vocabulary is the only disjoint part. But a future
  `substrate-reader-projection-sketch-01` may widen. See OQ4.
- **Cross-branch Held semantics.** A Held record appears
  inside a specific (agent, branch, τ_s) KnowledgeState;
  branch-crossing semantics belong to B1 (sketch-04 §Branch
  representation) and to fold scoping. See OQ6.
- **BLANK slot.** The Python collapses BLANK to GAP (substrate.py
  line 131). Whether BLANK warrants a distinct slot is OQ2.

## First-principles commitments

Labels **SH** (Substrate Held record).

### SH1 — Held is the K1 fold's per-proposition cell

An agent's `KnowledgeState` at `(agent, branch, τ_s)` is a set
of Held records — one per proposition the agent holds at that
coordinate. A Held record is the atomic unit of that set: a
proposition plus the epistemic qualifiers the fold needs to
answer downstream queries (`holds`, `holds_as`, `known`,
`believed`, `suspected`, `gaps`, dramatic irony, Sternberg
curiosity).

Held does not carry (agent_id, branch, τ_s). Those coordinates
are implicit in the containing `KnowledgeState` — the Held
record belongs to exactly one (agent, branch, τ_s) cell, and
its identity as a record is scoped inside that cell, not
across it.

### SH2 — Five required fields

A Held record is exactly five required fields:

- **`prop`** — a `Prop` record per substrate-prop-literal-
  sketch-01. The proposition this record asserts the agent
  holds at the current (branch, τ_s).
- **`slot`** — a value from the closed slot vocabulary (SH3).
  The agent's epistemic classification of this proposition
  (knows it; believes it; suspects it; treats it as an open
  question).
- **`confidence`** — a value from the closed confidence
  vocabulary (SH4). An ordinal confidence level, paired with
  (but not identical to) slot.
- **`via`** — a string from the via-operator closed vocabulary
  (substrate-effect-shape-sketch-01 ES4). The operator that
  *most recently placed* this Held into the agent's set. After
  the fold processes multiple effects on the same prop,
  `via` is the winning (last, per τ_s / τ_a) effect's
  via-operator.
- **`provenance`** — an ordered tuple of short strings. A
  human-readable authoring trail suitable for debugging and
  review-interface rendering. Not substrate-machinery-visible;
  consumers read it only for display, never for dispatch.

No optional fields. Five-field shape is complete for v1.

### SH3 — Slot vocabulary (closed, extensible by sketch amendment)

Slots at v1:

- **`"known"`** — the agent treats the proposition as true and
  certain. Identity-and-realization-sketch-01 I7: substitution
  fires only on KNOWN identity propositions. Holds-as-known
  is the strongest epistemic state the substrate represents.
- **`"believed"`** — the agent treats the proposition as
  probably true. A secondhand fact from a trusted utterance
  default-places at BELIEVED (oedipus.py `told_by` helper);
  an inference from partial evidence typically does too.
- **`"suspected"`** — the agent has a hunch, a reading, or a
  partial inference. Weaker than BELIEVED; the agent is aware
  that the proposition could be wrong.
- **`"gap"`** — the agent is aware that a question is open.
  The proposition here is not something the agent *holds* in
  the positive sense; it is an explicitly-acknowledged
  uncertainty. Sternberg-curiosity queries (substrate-sketch-04
  §Sternberg's interests as queries) scan GAP-slot records.
  Per identity-and-realization-sketch-01 §Sternberg-stays-
  literal: substitution does not auto-resolve GAP records
  even when substitution could derive an answer.

**Why these four and no more.** Each corresponds to a structural
dispatch in the substrate:

- KNOWN vs. rest: identity substitution participates (I7).
- BELIEVED / SUSPECTED: ordinal strength signaling; readers and
  verifier machinery inspect for "confident belief" vs. "tentative
  belief" patterns.
- GAP vs. rest: Sternberg curiosity queries; the GAP slot is
  the sole explicit-acknowledged-uncertainty marker.

**BLANK collapsed to GAP.** Python substrate.py line 131 notes:
"BLANK deliberately collapsed to GAP in this prototype." This
sketch carries that collapse forward (a BLANK in the
informal substrate-sketch literature becomes "not in the held
set" or "held at GAP"). Re-opening BLANK as a distinct slot
is OQ2, gated on a corpus case that needs it.

**Closed, extensible by sketch amendment.** Adding a slot
requires (1) a named structural consumer the substrate
dispatches on, (2) amendment of this sketch + the Held schema,
(3) amendment of identity-and-realization-sketch-01 I7 if the
new slot interacts with substitution. Grid-snap: new slots
earn their place via structural consequence, not via narrative
texture.

### SH4 — Confidence vocabulary (closed, paired-with-slot)

Confidences at v1:

- **`"certain"`** — the agent holds the proposition as fully
  reliable. Typical pairing: slot=KNOWN.
- **`"believed"`** — the agent is confident but not certain.
  Typical pairing: slot=BELIEVED.
- **`"suspected"`** — the agent considers it plausible.
  Typical pairing: slot=SUSPECTED.
- **`"open"`** — the agent treats the proposition as an open
  question; confidence is deliberately unassigned. Typical
  pairing: slot=GAP.

**Slot and confidence are orthogonal in principle.** The
vocabulary is structured to allow, e.g., `(slot=BELIEVED,
confidence=SUSPECTED)` to signal "the agent notionally believes
but their confidence is shaky" — a texture distinction the
encoding may or may not use. In practice the corpus co-varies
them strongly (the `told_by` and `observe` helpers pair
slot=BELIEVED with confidence=BELIEVED, slot=KNOWN with
confidence=CERTAIN).

**Why two fields instead of one.** Collapsing to a single field
is the natural simplification (OQ1). The sketch retains both
fields at v1 for two reasons:

1. **Backward compatibility.** The Python prototype carries both;
   collapsing would force every encoding rewrite. State-of-play-06
   item #2's misread shows that Python-is-sneaky on this axis
   (the shape looks vestigial but the two axes are conceptually
   distinct).
2. **Authorial headroom.** An encoding may yet find a slot /
   confidence split useful (a character's politics: "believed"
   public-position, "suspected" private-doubt — two distinct
   propositions? or one with split slot/confidence? the two-
   field shape admits the latter).

If no encoding exercises the orthogonality within N (2–3?)
future arcs, this sketch gets amended and the collapse happens.
OQ1 names the forcing function.

### SH5 — Held is authored, not derived

This is the load-bearing amendment to substrate-effect-shape-
sketch-01 ES3. Spelled out in the §Amendments section below;
summarized here:

**The author specifies the Held record.** A `KnowledgeEffect`
carries a Held record (via the effect's `held` field) that the
author has fully authored — prop, slot, confidence, via,
provenance. The fold processes effects and writes the authored
Held into the KnowledgeState at the effect's event's (branch,
τ_s) coordinate. Later effects on the same prop overwrite
earlier ones (the prototype's fold rule); effects with
`remove=True` (see SH8) dislodge.

**The fold does not derive slot from via.** ES3's written claim
— "the fold determines a holder's slot for a prop by
accumulating effects by via" — presumes a via→slot mapping the
substrate does not actually have, and could not stably have
(the same via like `utterance-heard` lands at BELIEVED in some
cases and at SUSPECTED in others, depending on authorial
reading of source reliability). The authored-shape commitment
pushes this judgment where it belongs: in the encoding.

**Consequence for the effect.** A `KnowledgeEffect` is
effectively `(holder, held, remove)` — a holder reference,
the authored Held record, and a retraction-polarity flag (SH8).
The via-operator lives inside the Held record; there is no
separate `via` on the effect. This aligns the record-to-record
interface (effect → fold → Held) to a single representation.

### SH6 — Provenance is a free-form string tuple

A Held's `provenance` field is a tuple of short human-readable
strings, ordered by authorial-time. Typical entries: `"observed
@ τ_s=3"`, `"told by messenger @ τ_s=8: revealed polybus
adoption"`, `"dislodged @ τ_s=9: shepherd's testimony"`.

**Not substrate-machinery-visible.** No fold dispatches on
provenance strings; no verifier parses them; no schema validates
their internal structure. Provenance is *display-layer* content
the authoring tool surfaces to humans (and eventually to
reader-model probes as a low-priority prompt appendage).

**Grow is free.** When multiple effects converge on the same
prop (the fold's overwrite rule discards prior Held values; the
new Held's provenance is the new effect's provenance), an
encoding that wants a compound trail authors the trail at the
final effect. The sketch does not commit that the fold
concatenates prior provenance onto later ones — that is
fold-mechanics (OQ5).

### SH7 — Held records are timeless at record level

Parallel to SE5 (Entity), ES7 (Effect), PL7 (Prop).

A Held record carries no `τ_a`, `τ_s`, or branch. Temporal and
branch coordinates come from:

- The containing `KnowledgeState`, which is scoped at exactly
  one `(agent, branch, τ_s)` by construction. Every Held record
  inside that state inherits those coordinates.
- The authoring `KnowledgeEffect`'s containing Event, for
  authored-shape purposes. The event's `τ_a` is when the author
  placed the Held; `τ_s` is when the agent receives it; the
  event's branches are where it applies.

The Held record is thus *fungible* across (agent, branch, τ_s)
cells in the same sense a Prop literal is fungible across
containers (PL7): the same Held representation `(prop=killed(A,
B), slot=KNOWN, confidence=CERTAIN, via="observation",
provenance=("observed @ τ_s=5",))` may appear verbatim in two
agents' states (two witnesses) without being the "same" Held
in an identity sense; each occurrence is distinct by containing
cell.

### SH8 — `remove: bool` is a KnowledgeEffect-level polarity

See §Amendments §ES3-amendment for the full discussion.
Summary: the effect carries an optional `remove: bool`
(default False). A `remove=True` effect **dislodges** the Held
record at the effect's (holder, prop) cell at the effect's
(branch, τ_s): the fold drops the prior Held, and the effect's
own Held (if present) is *not* written in (remove-effects are
polarity-only, not replacement-plus-remove).

**Why this shape and not via="forgetting".** The sketch
considered the alternative: retire `remove` and route
dislodgement through `via="forgetting"` (with the fold knowing
`forgetting` means "delete"). Rejected because:

1. **The forgetting semantics are under-specified.** Substrate-
   sketch-04 §Update operators described forgetting as "confidence
   decays; proposition moves toward or out of the state" —
   deliberately non-committal between decay and deletion. Deciding
   this at the Held-sketch level would close ES3 OQ1 prematurely
   and force a decision that has its own forcing-function
   requirements elsewhere.
2. **Dislodgement is authorially distinct from forgetting.** A
   messenger revealing Oedipus was adopted does not cause
   Oedipus to *forget* `child_of(oedipus, polybus)` — it
   causes his belief to be *dislodged by new evidence*. The
   author's intent is "this specific belief is now wrong", not
   "this belief fades over time". Conflating these under one
   operator loses the distinction.
3. **The pattern is already in place and working.** 7 corpus
   instances across 3 encodings (Oedipus, Macbeth, Ackroyd)
   route through per-encoding `remove_held` helpers that pair
   `remove=True` with `via="inference"` (the proposition is
   dislodged because subsequent evidence changed the agent's
   inferential state). The pattern is coherent; retiring it
   trades working-code for the appearance of cleaner form.

Grid-snap applies: `remove` is a polarity the fold dispatches
on (dislodge vs. write); it earns its place as a field.

## Amendments to prior sketches

This sketch makes two explicit amendments.

### ES3-amendment — KnowledgeEffect's shape

Substrate-effect-shape-sketch-01 ES3 commits:

> Three-field record:
> - `holder` — an Entity id (string)
> - `prop` — a Prop record
> - `via` — a string from the via-operator vocabulary
>
> No `asserts` field … No explicit confidence-slot field.
> Slots are fold-output state, not effect-input. The fold
> determines a holder's slot for a prop by accumulating effects
> by via.

This sketch revises to:

> Three-field record:
> - `holder` — an Entity id (string)
> - `held` — a Held record per substrate-held-record-sketch-01
> - `remove` — an optional boolean (default False)
>
> The effect carries no separate `prop` or `via` — both live on
> `held`. The `remove` polarity discriminates write (default)
> from dislodge (remove=True).

**Justification for the amendment.** ES3's via→slot derivation
claim does not match authorial practice: the same via
(`utterance-heard`) lands at different slots across the corpus
(BELIEVED when the utterer is trusted; SUSPECTED when they are
not). Pushing the slot judgment into the fold either forces a
via→slot mapping the substrate cannot robustly have, or makes
the fold depend on event-context (participants' roles, event-
type, prior Held-state) in ways that blow up fold complexity.
Authoring the slot on the effect is the honest representation.

**Consequence for schema/event.json.** The Event schema's
`KnowledgeEffect` sub-schema (currently `{kind, holder, prop,
via}`) is amended by `production-format-sketch-04` (pending)
to `{kind, holder, held, remove?}` with `held` as a `$ref` to
`schema/held.json`. The `via` field moves from effect-level to
Held-level. The `prop` field moves from effect-level to
Held-level.

**Conformance implication.** The Python prototype's
KnowledgeEffect `(agent_id, held, remove)` shape already matches
the amended record at the field level; the only schema-side
translation the dump layer must do is `agent_id` →
`holder` (which it already does for the current ES3-shaped
schema) and, new under this amendment, emit `held` as a
nested record and propagate `remove` through. Oedipus's 7
`remove=True` instances validate under the amended schema
without encoding rewrites; every `remove=False` instance
validates too. No corpus event is invalidated by the amendment.

### Identity-and-realization-sketch-01 §Sternberg-stays-literal —
consistency note

The prior sketch already endorsed `remove=True` as a legitimate
authored mechanism for gap-resolution. This sketch formalizes
that endorsement as SH8 — no substantive change; the prior
wording is now backed by a structural commitment on the
KnowledgeEffect record.

## Worked examples

### Held — Alice hears a rumor (slot=BELIEVED)

```
Held(
    prop=Prop(predicate="owner_of",
              args=("locket", "bobs_grandmother")),
    slot=Slot.BELIEVED,
    confidence=Confidence.BELIEVED,
    via=Diegetic.UTTERANCE_HEARD.value,
    provenance=("told by bob @ τ_s=5",),
)
```

Inside a `KnowledgeEffect(holder="alice", held=<above>,
remove=False)`. The fold, processing Alice's (branch=canonical,
τ_s≥5) slice, writes this Held into her KnowledgeState.

### Held — Oedipus knows the oracle's words (slot=KNOWN)

```
Held(
    prop=Prop(predicate="prophecy_will_kill_father_and_marry_mother",
              args=("oedipus",)),
    slot=Slot.KNOWN,
    confidence=Confidence.CERTAIN,
    via=Diegetic.OBSERVATION.value,
    provenance=("heard oracle directly @ τ_s=-20",),
)
```

### Held — Oedipus wonders about his parentage (slot=GAP)

```
Held(
    prop=Prop(predicate="real_parents_identified",
              args=("oedipus",)),
    slot=Slot.GAP,
    confidence=Confidence.OPEN,
    via=Diegetic.INFERENCE.value,
    provenance=("suspicion kindled @ τ_s=3: drunkard's remark",),
)
```

A GAP-slot Held. Substrate machinery does *not* auto-resolve
this even when identity substitution could derive
`child_of(oedipus, laius)` — per identity-and-realization-
sketch-01 §Sternberg-stays-literal, authored GAPs are
explicitly-acknowledged uncertainties that persist until an
effect (typically with `remove=True`) dislodges them.

### KnowledgeEffect — the messenger's reveal dislodges a belief

The messenger tells Oedipus he was adopted. Oedipus's prior
BELIEVED `child_of(oedipus, polybus)` is no longer warranted.
The encoding's `remove_held` helper emits:

```
KnowledgeEffect(
    holder="oedipus",
    held=Held(
        prop=Prop(predicate="child_of",
                  args=("oedipus", "polybus")),
        slot=Slot.BELIEVED,
        confidence=Confidence.BELIEVED,
        via=Diegetic.INFERENCE.value,
        provenance=("dislodged @ τ_s=7: messenger's reveal",),
    ),
    remove=True,
)
```

The fold, seeing `remove=True`, dislodges Oedipus's existing
`child_of(oedipus, polybus)` Held. The Held nested in the effect
carries a provenance string documenting *why* the dislodgement
happened, but the fold does not write this Held into the state
— remove-effects are polarity-only. (The nested Held's presence
is a tooling convenience: the author names what is being
dislodged; the `remove_held` helper formalizes the pattern.)

### KnowledgeEffect — Jocasta asserts an identity

Per identity-and-realization-sketch-01 §Worked example, a
realization-event's payload is an identity assertion:

```
KnowledgeEffect(
    holder="jocasta",
    held=Held(
        prop=Prop(predicate="identity",
                  args=("oedipus", "the-exposed-baby")),
        slot=Slot.KNOWN,
        confidence=Confidence.CERTAIN,
        via=Diegetic.REALIZATION.value,
        provenance=("identity asserted @ τ_s=10: "
                    "shepherd's + messenger's testimony",),
    ),
    remove=False,
)
```

`remove=False` (default). Identity substitution (I7) then fires
on Jocasta's state because the new Held is slot=KNOWN and
predicate="identity".

## Not in scope

Re-stating the out-of-scope list for emphasis:

- **Fold-implementation mechanics.** How K1 resolves
  conflicting effects across τ_s, interprets `via="forgetting"`,
  indexes by Prop, or handles branch-scope inheritance is
  fold-layer. This sketch commits only to the record shapes
  the fold consumes + produces.
- **Identity substitution.** Identity-and-realization-sketch-01
  owns. SH3 references I7 for context.
- **Reader's Held.** SH2 commits the reader uses the same
  five-field shape. A future sketch (`substrate-reader-
  projection-sketch-01`) can widen. OQ4.
- **BLANK slot.** Collapsed to GAP per Python's existing
  convention. OQ2.
- **Provenance structure.** Free-form strings. A richer shape
  (event / effect pointers) is OQ3.
- **World Held.** World state is a set of Props (not Helds);
  no slot / confidence / via. This sketch is agent-scoped.

## Open questions

1. **OQ1 — Collapse slot and confidence.** The two fields
   co-vary strongly in the current corpus. If no encoding
   exercises the orthogonality within the next 2–3 encoding
   arcs, collapse to one field (a single `epistemic`? `strength`?
   enum). Forcing function for *retaining*: an encoding that
   uses `(slot=X, confidence=Y)` with X ≠ Y at-paired-position
   and the distinction is structurally read (by a verifier, a
   fold, a reader-model probe). Forcing function for
   *collapsing*: none yet, but 3 arcs pass with unused
   orthogonality, collapse.
2. **OQ2 — BLANK as distinct slot.** Substrate.py currently
   collapses BLANK to GAP. A BLANK slot would represent "the
   agent's state has no record whatsoever for this proposition"
   — subtly different from GAP ("the agent explicitly knows
   the question is open"). If an encoding needs the distinction
   (a reader-model probe wants to treat "never-thought-about-it"
   differently from "acknowledged-open"), this sketch amends
   to add BLANK. Corpus has no forcing case today.
3. **OQ3 — Structured provenance.** Current provenance is a
   tuple of short strings. A structured shape (e.g., a tuple
   of `ProvenanceLink(kind, event_id, effect_index, note)`
   records) would let verifier machinery trace a Held back to
   its authoring event precisely. Forcing function: a verifier
   check that wants provenance-traceability (a lowering
   auditor, a reader-model proposal that cites specific authored
   events). Not forced at v1.
4. **OQ4 — Reader's Held-record shape.** SH2 commits the
   reader uses the five-field shape with the narrative via
   vocabulary. If reader-specific machinery needs additional
   fields (focalization-source pointer? narrative-frame id?),
   a sibling sketch carves out a Reader-specific record or
   amends Held. Not forced at v1; the Aristotelian probe work
   uses reader Held as currently shaped.
5. **OQ5 — Fold semantics on conflicting same-prop effects.**
   The Python fold uses "later-wins" — later τ_s / τ_a effect
   on the same (holder, prop) overwrites the earlier Held.
   This is not a Held-record question per se, but the Held
   sketch has to be compatible with whatever fold semantics
   the substrate commits to. A `substrate-knowledge-fold-
   sketch-01` (future) addresses. Today's Python works; no
   forcing function.
6. **OQ6 — Remove semantics across branches.** A `remove=True`
   effect on `:canonical` at τ_s=5 dislodges the prior Held;
   what does a `:contested` branch see? Per B1, the contested
   branch inherits the `:canonical` event up to the divergence
   point. If the remove is on `:canonical` post-divergence,
   the contested branch does NOT see it. Current fold machinery
   handles this; the sketch's commitment is that `remove` is
   a polarity, not a record-level temporal claim. Reopens if
   a branch-crossing edge case surfaces.
7. **OQ7 — Forgetting's fold semantics.** Substrate-sketch-04
   left `via="forgetting"` deliberately non-committal between
   decay and deletion. This sketch does not decide. A fold
   sketch (future) commits. The Held shape admits either
   reading (a forgetting effect can author a Held with
   slot=GAP, or a `remove=True` effect can dislodge the Held
   entirely, or a future decay-mechanism can author a Held
   with degraded confidence). Banked.

## Discipline

Process expectations for work against this sketch:

- **Record-level specification before schema.** This sketch is
  the design-level source of truth for `schema/held.json`. Any
  schema draft that does not cite this sketch is PFS2 drift.
- **Authored, not derived.** The commitment at SH5 is
  load-bearing. Tools that want a "what does the fold *actually*
  derive?" reading must not silently widen slot / confidence /
  provenance to fold-computed — the author authors, the fold
  writes.
- **Closed vocabularies + extension protocol.** Slots,
  confidences, and via-operators each grow by sketch amendment
  with a named structural consumer. Grid-snap applies at each
  axis.
- **`remove` is polarity.** SH8 + ES3-amendment commit `remove`
  as a first-class KnowledgeEffect field. Retiring it requires
  retiring the 7 corpus cases AND defining a replacement
  dislodgement mechanism with equivalent semantic clarity. The
  sketch's read: `remove` earns its place; future arcs may
  widen the pattern (e.g., adding `asserts` to KnowledgeEffect
  if a polarity distinction emerges for the positive case) but
  are unlikely to retire it.

## Summary

Record-shape sketch for Held — the K1 fold's per-proposition
cell, and (via the ES3-amendment) the authored shape a
KnowledgeEffect carries.

- **Five fields:** prop, slot, confidence, via, provenance.
- **Slot closed at four values** (KNOWN, BELIEVED, SUSPECTED,
  GAP); BLANK collapsed to GAP. Each slot has a named substrate
  dispatch (identity-substitution, Sternberg-curiosity).
- **Confidence closed at four values** (CERTAIN, BELIEVED,
  SUSPECTED, OPEN); orthogonal-in-principle to slot, co-varying
  in practice; collapse banked as OQ1.
- **Authored, not derived** (SH5). The author specifies the
  Held record; the fold writes it. Amends substrate-effect-
  shape-sketch-01 ES3 accordingly (effect carries `held` not
  `prop + via`; also admits `remove: bool`).
- **Timeless at record level** (SH7); temporal + branch
  coordinates inherit from the containing KnowledgeState /
  authoring Event.
- **`remove` polarity** (SH8) for factual dislodgement —
  formalizes the pattern identity-and-realization-sketch-01
  §Sternberg-stays-literal already endorsed and the corpus
  already uses.

**Corrects state-of-play-06 item #2.** The 7 `remove=True`
corpus cases are legitimate (the realization-workaround
retirement already happened); the audit baseline is the
intended final state, not a drift-to-zero cleanup target.
Next state-of-play (sketch-07, post-this-arc) rewrites that
framing.

Unblocks `production-format-sketch-04` → `schema/held.json` +
`schema/event.json` amendment. Seven OQs banked with
forcing-function criteria. No substrate or dialect record
change is forced by this sketch; the existing corpus (102
unique events across 5 encodings) validates every commitment
SH1–SH8 (conformance surface belongs to the production-format
sketch, not here).

The sketch's load-bearing discipline: **Held is a record, not
a computation.** The author writes what they mean; the fold's
only machinery is ordering and polarity. Grid-snap at the
epistemic-cell layer.
