# Substrate knowledge fold — sketch 01

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (new topic — fold-mechanics consolidation
that substrate-sketch-04 §Fold scope across branches and substrate-
held-record-sketch-01 §Fold-implementation mechanics both name but
neither structurally specifies)
**Frames:** [substrate-sketch-04](substrate-sketch-04.md) §Fold
scope across branches — "the rule for which events are 'in scope'
when folding state for a given branch b"; §Update operators —
"forgetting: confidence decays; a proposition moves toward or out
of the state"; open question 13 (branch reconvergence); open
question 14 (draft supersession); [substrate-held-record-sketch-01](
substrate-held-record-sketch-01.md) SH1 (Held as the K1 fold's per-
proposition cell), SH5 (authored-not-derived), SH8 (`remove: bool`
is a KnowledgeEffect-level polarity); open questions 5 (fold
semantics on conflicting same-prop effects), 6 (remove semantics
across branches), 7 (forgetting's fold semantics); [substrate-
sketch-05](substrate-sketch-05.md) K1 knowledge-projection fold
**Related:** [substrate-effect-shape-sketch-01](substrate-effect-
shape-sketch-01.md) ES3-amendment (effect → fold → Held
interface); [production-format-sketch-04](production-format-
sketch-04.md) (Held schema landing — `remove`, `via`, `slot`,
`confidence`, `provenance` all spec'd); [production-format-sketch-
05](production-format-sketch-05.md) (Branch schema landing —
`kind`, `parent`, optional `metadata`); [architecture-sketch-
01](architecture-sketch-01.md) A3 (drift discipline)
**Superseded by:** nothing yet

## Purpose

Consolidate five banked open questions about **K1 fold mechanics**
— the semantics the knowledge-projection fold uses to resolve
conflicting effects, apply dislodgements, and respect branch
scope. Each OQ was banked by its originating sketch with an
explicit pointer to a "future `substrate-knowledge-fold-sketch-
01`" as the proper home. This is that sketch.

The five:

- **Held-sketch OQ5** — conflict resolution for same-prop
  effects. Python uses later-wins; no sketch committed.
- **Held-sketch OQ6** — `remove` semantics across branches.
  Current fold machinery handles it; held sketch's commitment
  was only that `remove` is a polarity, not a branch-claim.
- **Held-sketch OQ7** — `via="forgetting"` decay vs. deletion.
  Substrate-sketch-04 §Update operators is deliberately
  non-committal.
- **Substrate-04 OQ13** — branch reconvergence semantics. Three
  candidate resolutions enumerated (permanent split / explicit
  authorial merge / trans-branch-canonical declaration); sketch-04
  said "prototype can start with permanent-split as the default"
  but did not commit.
- **Substrate-04 OQ14** — draft supersession semantics. Three
  candidate mechanisms enumerated (event-level / effect-level /
  removal); sketch-04 said "prototype can begin with event-level
  supersession and append-on-promote" but did not commit.

Each of the five sits behind existing Python behavior the prototype
has relied on without a design-level commitment. The gap is not
"code vs. spec has diverged" — it's "code implements one reading
of a genuinely-open design question and the corpus hasn't forced
the hand."

This sketch closes three of the five with prototype-aligned
commitments (**KF1**, **KF4**, **KF5-default**), treats one as
derivable from existing commitments (**KF3**), and sharpens the
one that must stay banked (**KF2**). The remaining shape — what
this sketch does NOT commit to — is itemized in §Open questions
with forcing-function criteria.

No schema deliverable today. No Python change today. This is a
design-level consolidation under the PFS2 discipline: bring the
sketches into alignment with settled behavior; leave genuinely-
open behavior banked with named forcing functions.

## What this sketch is *not* committing to

- **Automatic confidence decay over story-time.** The fold does
  not implement half-life curves, time-weighted confidence
  erosion, or any implicit state degradation. `via="forgetting"`
  remains an authorial label, not a structural operator (KF2).
- **Explicit authorial merge events** as a reconvergence
  mechanism. One of sketch-04 OQ13's three candidates; stays
  banked (see §Open questions OQ-KF1).
- **Trans-branch-canonical declaration** as a reconvergence
  mechanism. Second of sketch-04 OQ13's three candidates; stays
  banked (see §Open questions OQ-KF2).
- **Effect-level override** as a draft-supersession mechanism.
  Second of sketch-04 OQ14's three candidates; stays banked
  (see §Open questions OQ-KF3).
- **Removal** (explicit `removes(event_id)`) as a draft-specific
  dislodgement mechanism. Third of sketch-04 OQ14's three
  candidates; stays banked (see §Open questions OQ-KF4).
- **Draft-of-draft supersession composition.** Stays banked
  (see §Open questions OQ-KF5).
- **Draft-to-canonical promotion semantics** (append vs. rewrite).
  Stays banked (see §Open questions OQ-KF6).
- **Counterfactual-branch removal semantics** beyond sketch-04
  §Fold scope's "minus events removed by the query on c." Stays
  banked (see §Open questions OQ-KF7).
- **Fold-layer performance engineering** (memoization, incremental
  folds, snapshot anchors). Substrate-sketch-04 OQ9's territory;
  no commitment here. The commitments below permit any of those
  implementations but require none.
- **The W1 world-projection fold.** This sketch covers **K1 only**
  (knowledge). W1 has its own fold (`project_world`) whose
  mechanics parallel K1 but carry their own analogues of the
  same questions. A sibling `substrate-world-fold-sketch-01` is
  the natural follow-on if W1 needs equivalent consolidation.
- **The reader's K2 projection.** `project_reader` composes K1
  with focalization (focalization-sketch-01 F1–F6) and sjuzhet
  order; this sketch does not re-litigate F1–F6.
- **Tension, emotional projection, or any F1-retired projection
  shape.** Substrate-sketch-05 retires F1; nothing here adds it
  back.

## What this sketch *is* committing to

Five fold-mechanics commitments, closing four OQs outright,
sharpening one, and deriving one from existing commitments:

- **KF1 — Conflict resolution is last-write-wins on `(τ_s, τ_a)`
  ordering.** Resolves held-sketch OQ5. The fold's input event
  sequence is sorted by `(τ_s, τ_a)` ascending; for any set of
  effects targeting the same `(agent_id, prop)`, the one whose
  event appears latest in that ordering wins. `τ_a` is the
  load-bearing tiebreaker; without it the fold is not
  deterministic.
- **KF2 — `via="forgetting"` is an authorial label, not a fold
  operator.** Sharpens held-sketch OQ7. The fold does not decay.
  Authors author a specific effect shape (slot=GAP, or
  `remove=True`); `via="forgetting"` is a provenance-layer
  annotation, not a fold-time behavior. Decay-over-time, if it
  is ever admitted, is a new operator — not a re-interpretation
  of this via-label.
- **KF3 — `remove` respects the fold-scope rule.** Derives from
  substrate-sketch-04 B1 + held-sketch SH8. A `remove=True`
  effect authored on branch b dislodges any prior Held for the
  same `(agent_id, prop)` produced by effects in b's fold scope
  at `τ_s' ≤ τ_s_of_remove`. Cross-branch behavior falls out of
  the scope rule directly. This is a statement, not a new
  commitment — no derivation beyond what sketch-04 + held-sketch
  already committed.
- **KF4 — Permanent split is the prototype default for branch
  reconvergence.** Partially resolves substrate-sketch-04 OQ13.
  Sibling `:contested` branches each fold independently. No
  automatic merge; no trans-branch fiat. Post-contest `:canonical`
  events remain `:canonical` and universal (per B1's "fold all
  events labeled `:canonical`"), so they are inherited by all
  contested branches as a consequence of the scope rule, not as
  a merge mechanism. The two remaining OQ13 candidates — merge
  event and trans-branch declaration — stay banked (OQ-KF1 /
  OQ-KF2).
- **KF5 — Event-level supersession is the prototype default for
  draft branches.** Partially resolves substrate-sketch-04 OQ14.
  A `:draft` branch's fold is the parent's fold PLUS events
  labeled d MINUS events whose id appears in d's authored
  supersession set. The carrier for the supersession set is
  Branch-level metadata (Branch.metadata admits this per
  production-format-sketch-05 B6); a later sketch may typed-
  promote the field if a second draft-exercising encoding
  surfaces. Effect-level override and removal-marker mechanisms
  stay banked (OQ-KF3 / OQ-KF4). Composition across stacked
  drafts and promotion-to-canonical both stay banked (OQ-KF5 /
  OQ-KF6).

## Scope

**In scope:**

- The K1 per-agent knowledge fold: input (ordered events),
  output (KnowledgeState of Helds), conflict resolution,
  dislodgement via `remove`, and branch-scope application.
- `:canonical`, `:contested`, `:draft`, and `:counterfactual`
  branch semantics *as they affect the fold*. The four branch
  kinds themselves are substrate-sketch-04's commitment; this
  sketch covers only the fold-time consequences.
- The interaction between `remove=True` and the fold-scope rule.
- The meaning of `via="forgetting"` at the fold layer.

**Out of scope:**

- W1 world-projection fold (`project_world`). Parallel topic;
  sibling sketch candidate.
- K2 reader projection (`project_reader`). Governed by
  focalization-sketch-01; sjuzhet-time composition on top of K1.
- Performance engineering (memoization, incremental evaluation,
  snapshot anchors).
- Effect authoring — the sketch takes effects as given and
  describes what the fold does with them. Effect shape lives in
  substrate-effect-shape-sketch-01 and substrate-held-record-
  sketch-01.
- Enforcement / verification over fold outputs — lives in
  verification-sketch-01's cross-boundary primitives and the
  per-dialect verifier surfaces. The fold produces state; the
  enforcement layer reads it.

## Ontology — fold-layer terminology

Before the commitments, the vocabulary the sketch needs:

### Fold input

A **fold input** is a deterministic sequence of events pre-filtered
to a given branch's fold scope. Specifically:

- `events_in_scope(b, τ_s)` — all events `e` such that `e.τ_s ≤
  τ_s` and `b.label ∈ e.branches OR b'.label ∈ e.branches for
  some ancestor b' of b`, ordered by `(e.τ_s, e.τ_a)` ascending.
- For `:canonical`, ancestors are empty; scope is pure canonical.
- For `:contested`, ancestors include `:canonical`; scope is
  canonical ∪ own events.
- For `:draft d` with parent p, scope is `events_in_scope(p,
  τ_s) ∪ events labeled d` minus events superseded by d (per
  KF5).
- For `:counterfactual c` rooted at source s, scope is
  `events_in_scope(s, τ_s) ∪ events posited by the query` minus
  events removed by the query.

The ordering `(τ_s, τ_a)` is total by construction — `τ_a` is a
per-fabula sequence number — and is the foundation KF1 rests on.

### Fold output

The fold produces a **KnowledgeState** — substrate-held-record-
sketch-01 SH1's per-agent, per-branch, per-τ_s cell set. The
output is a tuple of **Held** records: one per proposition the
agent holds at fold-output time, in an order derived from the
input (the fold's write order, which itself is `(τ_s, τ_a)`
order). The Held record is fully spec'd by substrate-held-record-
sketch-01; this sketch only discusses how the fold places records
into or removes records from the output.

### Fold operation

The fold iterates its input once, in order, and maintains a
working map `by_prop: Prop → Held`. For each KnowledgeEffect
targeting the requested `agent_id`:

- If `effect.remove` is False: `by_prop[effect.held.prop] =
  effect.held` (overwrite any prior entry).
- If `effect.remove` is True: `by_prop.pop(effect.held.prop, None)`
  (drop any prior entry).

At the end, the values of `by_prop` become the KnowledgeState's
tuple. This is the operation the five commitments below fully
specify.

## KF1 — Conflict resolution is last-write-wins on `(τ_s, τ_a)` ordering

**Closes held-sketch OQ5.**

For any set of KnowledgeEffects targeting the same `(agent_id,
prop)` in a given fold's input, the effect whose event appears
latest in the `(τ_s, τ_a)` ordering is the one whose Held the
fold writes into the output (or, if `remove=True`, the one whose
dislodgement the fold applies).

**Why `(τ_s, τ_a)` and not `τ_s` alone.** Two events at the same
story-time can author effects on the same proposition (a rapid
reveal, a contested observation, a speech-act and its reaction).
Story-time alone does not make "later-wins" well-defined. The
authorial-time tiebreaker `τ_a` is load-bearing: it is a per-
fabula sequence number, totally ordered, strictly monotonic in
authorial act. The fold's determinism requires it.

**Why last-write-wins and not union / strongest-confidence /
explicit-conflict.** The alternatives require either additional
machinery the substrate does not today carry (confidence algebra;
conflict objects) or interpretive choices the author would have
to make at authoring time. Last-write-wins is the only strategy
compatible with today's primitives and today's corpus. It is
also the strategy that makes authorial intent tractable: the
latest authored effect IS what the author most-recently decided;
earlier contradictions have been superseded by the author's own
later work.

**What this does NOT say.** It does not say effects are
unitarily additive; they are not. An effect on `(agent, P)` at
τ_s=5 followed by a second effect on `(agent, P)` at τ_s=7
produces one Held at τ_s=7 — not two. This matches sketch-04
§State-at-τ's "the union of all committed effects": effects
compose by replacement, not by accumulation, within the same
`(agent, prop)` cell.

**Reopens if.** An encoding authors a structured conflict on a
proposition the fold is asked to carry as both-held, and the
corpus forces the substrate to admit such a shape as first-class
(not as two propositions the inference layer reconciles). No
corpus case today.

**Prototype conformance.** `substrate.py` `project_knowledge`
implements KF1 exactly; `substrate.py` `scope` provides the
`(τ_s, τ_a)` pre-sort that makes KF1 well-defined. The docstring
at `scope` already names the property: "the τ_a tiebreaker is
load-bearing … the 'later effects win' fold rule is only well-
defined if the ordering is total and deterministic." This
sketch lifts that local docstring claim to a design-level
commitment.

## KF2 — `via="forgetting"` is an authorial label, not a fold operator

**Sharpens held-sketch OQ7.** The sketch stays banked on the
mechanism; the posture is committed.

The fold has no decay primitive. No timer, no half-life, no
confidence-erosion-over-story-time, no sleep-forgetting-model.
The substrate's knowledge state changes only when an effect is
authored against it.

`via="forgetting"` is therefore a *provenance label*, not a
structural operator. Authors express forgetting as one of two
effect shapes:

- **Soft forgetting.** A KnowledgeEffect with `slot=GAP`,
  `via="forgetting"`, and an authored Held that represents the
  agent's awareness that the prop has become uncertain. The fold
  writes this Held over any prior stronger Held via KF1.
- **Hard forgetting.** A KnowledgeEffect with `remove=True`,
  `via="forgetting"`, dropping the prior Held entirely (see KF3).
  Use when the agent no longer has awareness of the prop at all
  (the more common case in the corpus — Oedipus's 7 `remove=True`
  effects are of this shape).

Both shapes use existing primitives (slot, remove) already
committed by held-sketch SH1–SH8. KF2 is not adding new machinery;
it is asserting that the machinery stays as-is and the via label
earns no special treatment.

**What KF2 commits to.** The fold does not introspect on `via`.
The via field is carried through unchanged onto the written
Held (for effects that write) or is simply ignored (for
remove-effects, since no Held is written). Authors, verifiers,
and downstream tools may read `via` to distinguish authorial
intent; the fold itself does not.

**What stays banked.** Whether the substrate should eventually
grow an automatic-decay operator — a new effect kind, or a
scheduled-decay primitive — is a real open question. It is
called out as OQ-KF8 below. No forcing function in today's
corpus; all observed forgetting is authorial.

**Reopens if.** An encoding needs time-weighted confidence
behavior that cannot be modeled by explicit authored effects at
the decay points. Candidate shapes: very long fabula (decades,
dynasties) where per-τ_s authoring of decay is infeasible; or
psychological realism claims that need continuous-curve
provenance. Neither exists today.

## KF3 — `remove` respects the fold-scope rule

**Derived from substrate-sketch-04 B1 and held-sketch SH8; no new
commitment.**

The held sketch committed that `remove` is a polarity. The
substrate-04 sketch committed branch-scoped folding. Their
composition, when unpacked, produces exactly the behavior the
Python already implements. KF3 states the composition as a
derived rule so it can be cited without chasing two sketches.

**Rule.** A KnowledgeEffect with `remove=True` authored on an
event in branch b's fold scope at story-time τ_s_rm dislodges
any Held for `(effect.agent_id, effect.held.prop)` that was
produced by earlier-in-the-input effects from the same fold
scope. It does not affect the state of any agent on any branch
not rooted in b; it does not reach into sibling `:contested`
branches; it does not dislodge from the `:canonical` fold unless
the event itself carries `:canonical` as a label.

**Consequence 1 — canonical-level remove.** A `remove=True`
event labeled `:canonical` at τ_s=X is in the fold scope of every
branch that inherits `:canonical` (all of them by sketch-04's
universal-canonical rule). Every inheriting branch sees the
dislodgement at `fold(b, τ_s ≥ X)`.

**Consequence 2 — contested-branch remove.** A `remove=True`
event labeled `:b-theft` only at τ_s=X is in `:b-theft`'s fold
scope and in no other sibling contested branch's scope. It does
not affect `:b-inheritance`'s fold. This is the held-sketch OQ6
edge case answered directly.

**Consequence 3 — draft remove.** A `remove=True` event labeled
on a `:draft d` at τ_s=X is in d's fold scope. Whether this
interacts with KF5's event-level supersession is an authoring
question, not a fold question: a draft can contain
`remove=True` effects of its own (like any branch), and can also
supersede parent events (dropping them from the fold input
entirely). The two mechanisms are orthogonal.

**Not a new commitment.** This section is derivation, not
extension. If substrate-04 B1 or held-sketch SH8 is amended, KF3
restates automatically; no independent statement to retire.

## KF4 — Permanent split is the prototype default for branch reconvergence

**Partially closes substrate-sketch-04 OQ13.**

For reconvergence — the question of what happens downstream of a
contested region — the substrate's default posture is **permanent
split**. Sibling `:contested` branches do not inherit from each
other. A proposition contested on branches `:b-a` / `:b-b` /
`:b-c` remains branch-indexed downstream; there is no automatic
re-collapse into a single canonical reading.

**What makes permanent split the right default.**

- **Rashomon and *Turn of the Screw* require it.** These stories
  are ambiguous *by design*; reconverging them would be a lie
  about the artifact. Sketch-04 §How the theories map onto the
  substrate names them as parallel-contested-no-reconvergence.
- **It is the only mechanism compatible with zero author
  intervention.** The other two candidates (merge event, trans-
  branch declaration) both require explicit authorial acts.
- **It composes cleanly with sketch-04 §Fold scope across
  branches.** Post-contest `:canonical` events, if any, remain
  canonical and universal — they are inherited by every contested
  branch via the universal-canonical rule, not because of a
  reconvergence mechanism. The substrate admits the shape sketch-
  04 called "trans-branch canonical" purely by labeling events
  `:canonical` rather than any one contested branch.

**What permanent split does not do.**

- It does not prevent merge events or trans-branch declarations
  from being added later. Both remain valid sketch-04 OQ13
  candidates; the substrate refuses to silently pick them over
  split, but it will pick them if the author explicitly does.
- It does not solve the "canonical event downstream depends on a
  contested proposition" case. Sketch-04 §Fold scope named this
  explicitly: such an event is ill-formed unless the author
  branch-indexes it, merges the contest, or declares the event
  trans-branch-canonical. The substrate surfaces the ill-formed
  case; it does not auto-resolve it.

**What KF4 commits, precisely.** The fold, absent authorial
merge/declaration machinery, does not inherit content across
sibling contested branches. Sketches that define merge/
declaration must specify how they compose with the fold; neither
exists today.

**Prototype conformance.** `substrate.py` `in_scope` implements
permanent split by construction — a branch's fold input is
filtered to the branch's own label plus ancestor labels, with no
sibling-inheritance path. The docstring names the property
directly: "The event is NOT in scope if it is only on a sibling
:contested branch — sibling contested branches do not inherit
from each other."

## KF5 — Event-level supersession is the prototype default for draft branches

**Partially closes substrate-sketch-04 OQ14.**

For draft-supersession — the mechanism by which a `:draft d`
branch overrides parent events — the substrate's default is
**event-level supersession**. The draft declares a set of parent
event ids it supersedes; the fold on d skips those events
entirely when computing d's scope; the draft supplies replacement
events of its own.

**Record shape.** The supersession set is carried as Branch
metadata. Production-format-sketch-05 PFS5-B6 admitted `Branch.
metadata` as an optional open object for "authorial notes,
creation τ_a, disposition history — particularly relevant for
drafts and counterfactuals." This sketch names supersession as
one specific metadata use:

    Branch(
        label=":draft-alt-ending-3",
        kind=BranchKind.DRAFT,
        parent=":canonical",
        metadata={
            "supersedes": ["E_42", "E_47"],
            # ... other authorial metadata ...
        },
    )

The substrate reads `metadata.supersedes` (if present) as a
tuple of event ids to exclude from the draft's fold scope. A
later sketch — if a second draft-exercising encoding surfaces —
may promote `supersedes` to a typed field on Branch. Today no
encoding exercises draft branches at all (state-of-play-08
confirms the corpus's 25 branches are 17 canonical + 8 contested,
zero drafts / counterfactuals). KF5 commits the mechanism the
Python would need; it does not yet commit a typed field carrying
it.

**What the fold does.** `events_in_scope(draft, τ_s)` equals
`events_in_scope(parent, τ_s) ∪ events_labeled_draft` with the
ids in `draft.metadata["supersedes"]` (if any) removed. The draft
can then author replacement events — with its own label, its own
`(τ_s, τ_a)` coordinates, its own effects — which enter the fold
scope via the `events_labeled_draft` term. KF1 handles conflicts
that remain (replacement events at the same `(τ_s, τ_a)` as
superseded events; later KF1-wins applies).

**What stays banked.**

- **Effect-level override** (one of sketch-04 OQ14's three
  candidates) — marking specific effects of a parent event as
  overridden without removing the event itself. Sharper for
  small changes (different dialogue, different witness set) but
  adds an effect-id-addressable layer the substrate does not
  today carry. Not forced; OQ-KF3.
- **Removal markers** (the third candidate) — explicit
  `removes(event_id)` marker on a draft, distinct from a
  `supersedes(event_id)` marker. Hard to distinguish from
  supersede-with-empty-replacement; the draft's replacement set
  happens to contain no replacement for the superseded id.
  Banked as a naming/semantic question; OQ-KF4.
- **Draft-of-draft supersession composition.** A draft d' with
  parent a draft d — does d'.supersedes compose with d.supersedes
  by union, or does d' re-specify from scratch? The Python
  prototype's `ancestor_chain` at `substrate.py` line 267
  ambiguates; no corpus case. OQ-KF5.
- **Promotion semantics** (append vs. rewrite the canonical log
  on draft-to-canonical promotion). Sketch-04 OQ14 named the
  question; no prototype implementation. OQ-KF6.

**Prototype conformance.** The prototype does not yet implement
draft supersession. `substrate.py` `in_scope`'s docstring
acknowledges the gap: "Draft supersession (open question 14) and
counterfactual removal are not yet implemented. When the
prototype gains those, this function gains an exclusion check
against branch-specific supersession/removal metadata." KF5
commits the exclusion-check mechanism the comment anticipates; a
future commit wires it under the first draft-exercising encoding.
This is grid-snap-consistent: the sketch specifies the mechanism;
the Python will match when forced.

## Fold-layer performance

Explicitly **not** committed here. The five commitments above
permit any of the performance strategies substrate-sketch-04
OQ9 itemized:

- Memoization of `project_knowledge(agent_id, scope, τ_s)`
  results keyed on `(branch, agent_id, τ_s, scope-fingerprint)`.
- Incremental folds — re-fold from the last cached τ_s rather
  than from 0 on each query.
- Snapshot anchors — authored or periodic KnowledgeState
  snapshots at anchor τ_s's, with folds resuming from the
  anchor.

None of these change the semantics KF1–KF5 specify; all operate
as implementations of the same function. A performance-oriented
sketch at the fold layer is a future candidate (`substrate-fold-
performance-sketch-01`) when the naive fold is measurably
insufficient. Today it is not.

## Discipline

Process expectations for work against this sketch:

- **Fold mechanics are design commitments, not Python
  implementation details.** Any Python change that alters the
  semantics of KF1–KF5 without a sketch amendment is PFS2 drift.
  The reverse — the sketch being amended and Python following —
  is the normal direction.
- **Grid-snap applies.** KF1 is structural (deterministic
  conflict resolution); KF2 is interpretive (authors label,
  fold ignores); KF3 is derived; KF4 is structural (split by
  default); KF5 is structural (event-level exclusion as
  mechanism). Where the fold has room for interpretation, the
  interpretation is authorial, not fold-automated.
- **Authored-not-derived (SH5) holds at the fold layer too.**
  The fold writes what authors authored via effects. It does not
  synthesize new Helds (no decay, no auto-inference, no implicit
  state). Inference lives in `holds_derived` / `derive_all`
  (inference-model-sketch-01 N1–N10), which is a *query-time*
  operator over the fold output — not a fold primitive.
- **Banked is first-class.** Seven banked questions (OQ-KF1
  through OQ-KF7 below) carry named forcing-function criteria.
  When an encoding surfaces one of them, the response is a
  sketch amendment, not a silent Python extension.

## Open questions

Carried forward (from the originating sketches, sharpened against
the KF1–KF5 commitments here), plus one new one.

1. **OQ-KF1 — Explicit authorial merge events as a reconvergence
   mechanism.** Second of substrate-04 OQ13's three candidates.
   A merge event declares at some τ_s that contested branches
   reconverge, specifying how post-merge state combines. Forcing
   function: an encoding with genuinely-contested middle and
   genuinely-single-valued end (the classic case: "regardless of
   how Bob acquired the locket, it is in his hand at the
   wedding"). No corpus case today; Rashomon + *Turn of the
   Screw* + the Rashomon-derived test encodings all want the
   permanent-split shape KF4 commits.

2. **OQ-KF2 — Trans-branch-canonical declaration as a
   reconvergence mechanism.** Third of substrate-04 OQ13's
   candidates. Declares specific events or propositions canonical
   across all contested branches by authorial fiat — they hold
   the same way on every branch even if the paths to them differ.
   Mostly subsumable by labeling the event `:canonical` in the
   first place (the universal-canonical rule under B1), but the
   subtle case is where the *proposition* is trans-branch but
   the *events supporting it* are not. Forcing function: an
   encoding where the same proposition is reached via genuinely
   different contested paths but must hold uniformly. No corpus
   case today.

3. **OQ-KF3 — Effect-level override as a draft mechanism.** Second
   of substrate-04 OQ14's three candidates. Allows a draft to
   modify a parent event without removing it — for small changes
   that don't warrant a full replacement (different dialogue,
   different witness set, different single effect). Forcing
   function: a draft-exercising encoding where the author wants
   to override a single effect of a parent event and keep the
   rest. No corpus case today.

4. **OQ-KF4 — Removal markers vs. supersede-with-empty-replacement.**
   Third of substrate-04 OQ14's candidates, restated. Whether a
   draft's `removes(event_id)` should be a distinct primitive
   from `supersedes(event_id)` with an empty replacement set.
   Sharpens to: is there a semantic difference worth carrying, or
   is the distinction purely notational. Forcing function: a
   draft that structurally needs "remove without replacement" as
   a different *shape* of draft (e.g., a draft whose thesis IS
   the removal — "alt-ending-without-Act-3"). No corpus case
   today.

5. **OQ-KF5 — Draft-of-draft supersession composition.** Do
   nested drafts compose supersedes by union, or does the inner
   draft re-specify from scratch? Related: do nested drafts
   inherit each other's replacement events. Forcing function: a
   two-level-deep draft tree. No corpus case today; no prototype
   support.

6. **OQ-KF6 — Draft-to-canonical promotion semantics.** When a
   draft is promoted to canonical, does the canonical log
   rewrite in place (losing the supersession history), or append
   the draft's events with retained supersession metadata
   (preserving authored-time history at the cost of log clutter)?
   Sketch-04 OQ14 named both candidates. Forcing function: the
   first encoding that promotes a draft. No corpus case today.

7. **OQ-KF7 — Counterfactual removal semantics beyond scope-rule
   minus-clause.** Substrate-sketch-04 §Fold scope names
   counterfactuals as "minus events removed by the query on c"
   without further specifying. Does the removal cascade — if E4
   is removed, are events that depended on E4's preconditions
   also auto-removed, or do they remain and become ill-formed
   (surfaced as enforcement failures)? Forcing function: a
   counterfactual-exercising encoding. No corpus case today; the
   25 corpus branches include zero counterfactuals.

8. **OQ-KF8 — Automatic confidence decay over story-time.**
   Whether the substrate should eventually grow a structural
   decay operator — distinct from the authorial `via="forgetting"`
   label KF2 commits to. Forcing function: a very-long-fabula
   encoding (decades, dynasties) where per-τ_s authoring of decay
   is infeasible; or a psychological-realism claim that needs
   continuous-curve provenance. No corpus case today; all
   observed forgetting is authorial.

## Summary

Consolidation sketch for fold mechanics, no schema deliverable.
Five commitments (KF1–KF5) close four banked OQs with prototype-
aligned defaults (KF1 conflict resolution, KF4 reconvergence,
KF5 draft supersession) plus one sharpened-stay-banked (KF2
forgetting-label semantics) plus one derivation (KF3 remove
across branches). Seven remaining OQs stay banked (OQ-KF1
through OQ-KF7) plus one new one (OQ-KF8) added to sharpen KF2's
banked surface. Every banked OQ carries a named forcing function;
every commitment is grounded in either prototype behavior, a
cited sketch, or a derivation. No Python change required today;
no schema deliverable yet; the natural schema follow-on — if one
is ever needed — is a production-format sketch for the
`Branch.metadata.supersedes` field KF5 specifies, behind the first
draft-exercising encoding.
