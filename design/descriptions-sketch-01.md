# Descriptions — sketch 01

**Status:** draft, active
**Date:** 2026-04-13
**Amended:** 2026-04-19 (see §Amendments)
**Supersedes:** nothing (new topic)
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [substrate-sketch-05.md](substrate-sketch-05.md)
**Superseded by:** nothing yet

## Purpose

Formalize the description surface promised by
[architecture-sketch-01.md](architecture-sketch-01.md) (A2 and A4)
and deferred by [substrate-sketch-05.md](substrate-sketch-05.md)
(open question 9). Descriptions are the fold-invisible, interpretive
peer to the substrate's typed facts. This sketch specifies:

- The description record's structural shape.
- The kind vocabulary (starting set, extension rule).
- The attention levels and their operational meaning.
- The review-state model (history, staleness under anchor edits).
- Branch semantics (default-from-anchor, explicit override).
- Promotion mechanics (description → fact is always an author act).
- The description API, and the firewall that keeps fold functions
  from touching descriptions.
- Tooling obligations for any component that renders or queries the
  fabula.
- Provenance absorption — how substrate-sketch-05's `provenance`
  tuple on `Held` records becomes a `kind=provenance` description.
- A worked example using the refactored Rashomon encoding.

## What this sketch is *not* committing to

- A storage engine for descriptions.
- An authoring UI or IDE.
- The LLM prompt surface that turns a description into a fact
  proposal.
- Keybindings, review queues, dashboards, or any tooling surface
  beyond the invariants it must uphold.
- The full kind vocabulary. Sketch 01 gives a starting set with
  extension rules.
- Description *content* semantics. Text is free-form; the substrate
  does not parse it.

If a question starts "what prompt do I send the LLM," "what UI
widget displays this," or "what is every possible kind string" — it
is out of scope.

## What this sketch *is* committing to

1. **D1 — Fold-invisibility.** No substrate fold function takes a
   description as input. The fold API and the description API are
   separate surfaces; crossing from fold to description is explicit.
2. **D2 — Structural attention affordances.** Descriptions carry
   typed metadata — kind, attention, review state — that makes
   non-schema content visible *as* non-schema content. A description
   cannot masquerade as a fact, and a reviewer cannot silently skim
   past one whose attention level demands scrutiny.
3. **D3 — Anchor-attached.** Descriptions attach to typed anchors:
   events, effects, propositions, sjuzhet entries, or other
   descriptions. A free-floating description is not a valid record.
4. **D4 — Branch semantics default from anchor, with override.** A
   description's branch membership defaults to its anchor's branch
   set. It may be explicitly scoped to a subset when interpretation
   is branch-specific.
5. **D5 — No auto-promotion.** A description never becomes a fact
   except by explicit author action, which produces a new event (or
   event amendment) and leaves an audit link on the description. No
   fold operation promotes descriptions; no LLM workflow promotes
   descriptions; only an author act does.

D1 through D5 are all retested under architecture-01 A3 — they are
structural rules about the description surface itself, and they
describe drift the schema catches (a fold that silently reads a
description, a promotion that bypasses authorial review, a
description that loses its anchor). All pass A3.

## Relation to architecture-sketch-01 and substrate-sketch-05

- Architecture-01 A2 declared facts and descriptions as peers with
  different semantics; D1–D5 formalize the description side.
- Architecture-01 A4 declared that descriptions draft attention;
  the *kind* and *attention* fields below are the structural
  mechanism.
- Architecture-01 open questions 1 (authorial action), 3
  (cross-description attachment), 4 (description branch semantics),
  5 (review-state decay), and 6 (LLM proposing facts) are addressed
  in this sketch. Architecture-01 open question 2 (ordinal vs
  categorical attention) was already resolved in architecture-01's
  A4 update.
- Substrate-05 open question 9 (description branch semantics) is
  answered by D4 below.
- Substrate-05's retired F1 (emotion/tension as parallel projection)
  has a natural home here: affect descriptions live on events with
  `kind=texture` or `kind=reader-frame` depending on who the affect
  is about.

## The description record

A description is an immutable record with the following fields.
Mirror to the substrate's Event record where sensible; authored-time
and branch semantics are shared; fold-visibility is not.

### Required fields

- **id** — a stable identifier, scoped per story. Enables
  cross-reference and linking.
- **attached_to** — an anchor reference. One of:
  - an event id
  - an effect locator (event id + effect index or effect id)
  - a proposition (represented as a typed Prop value, not a stable
    id — propositions are derived, not stored)
  - a sjuzhet entry id
  - another description id (D3 allows description-on-description)
- **kind** — one of the declared kinds (see *Kinds* below).
  Extensible per story with documentation.
- **attention** — one of `structural`, `interpretive`, `flavor`.
  Categorical. See *Attention* below.
- **text** — free-form UTF-8 string. The substrate does not parse it.
- **authored_by** — author reference. Can be a human id, an LLM
  identifier ("llm:claude-sonnet-4-6"), or "unknown" for imported
  content. Reviewers can distinguish sources in the queue.
- **τ_a** — authored time. Monotonic per story, shared with the
  substrate's τ_a sequence so descriptions and events can be
  ordered together.

### Optional fields

- **is_question** — boolean. A description-as-question ("should
  this beat be here?") routes to an answer-me queue rather than
  being treated as an assertion. Orthogonal to kind; a
  `kind=texture, is_question=True` description is legal.
- **branches** — explicit branch scope, a subset of the anchor's
  branches. If omitted, defaults to the anchor's full branch set
  (D4).
- **review_states** — a tuple of `ReviewEntry` records (see *Review
  state* below). If omitted, the description is treated as having
  only unreviewed history.
- **promoted_to** — reference to an event id, if an author has
  promoted content from this description into a fact. Immutable
  audit link. See *Promotion mechanics* below.
- **status** — `committed`, `provisional`, or `superseded`. The
  first two share the axis with events: committed descriptions are
  signed off; provisional descriptions are drafts an author has not
  yet blessed. `superseded` is the edit-chain marker (see
  §Record-level invariants): when a successor is authored, the
  successor is `committed` and carries `metadata.supersedes =
  <source-id>`, and the source's status flips to `superseded` with
  `metadata.superseded_by = <successor-id>`. Tooling renders
  supersession chains as history, not as current state.
- **metadata** — open dict for tooling-specific extension. The
  substrate does not interpret most of its contents; the
  exceptions are the supersession pointers (`supersedes`,
  `superseded_by`) written by the edit-chain mechanism — see
  §Record-level invariants.

### Record-level invariants

- Once authored at τ_a = n, a description's **semantic content**
  (text, kind, attention, attached_to, authored_by, τ_a,
  is_question, branches) is immutable. Edits append a new
  description at τ_a = n+k; the successor is `status=committed`
  with `metadata.supersedes` pointing at the source, and the
  source's `status` flips to `superseded` with
  `metadata.superseded_by` pointing at the successor. These two
  fields — `status` and the supersession pointers in `metadata` —
  are the sole mutation surface on an existing record; they exist
  to make the edit-chain traversable without a parallel journal.
  Any other mutation is drift.
- A description's `attached_to` must resolve to an existing anchor
  at the description's τ_a. A description cannot be attached to a
  future event.
- A description's `branches` (if set) must be a subset of the
  anchor's branches at the description's τ_a.

## Kinds

The starting vocabulary. Each kind is a rough categorization of what
sort of interpretation the description carries. Extension is
expected; a story introducing a new kind documents what it is for.

- **texture** — tonal / affective content. Describes how a scene,
  act, utterance, or moment feels. "The blow was tentative; he had
  never struck anyone before."
- **motivation** — why an agent does something, beyond what the
  typed propositions capture. "She hesitated not from doubt but
  from the weight of her mother's advice."
- **reader-frame** — how the reader is positioned toward the
  content. "Played for sympathy, not horror." "The scene reads as
  comic to a first-time viewer and as tragic on re-read."
- **authorial-uncertainty** — the author is not sure. "I don't know
  if this beat is earned by the preceding scene." These are
  first-class; `attention=structural` unreviewed
  authorial-uncertainty descriptions are a tooling signal that the
  draft is not ready.
- **trust-flag** — a credibility annotation. "The woodcutter is
  unreliable here; weight his testimony accordingly." This is
  interpretation, not a fact — facts about his unreliability would
  be in events or propositions. The flag is a reader-side hint.
- **provenance** — audit trail. "Observed by shepherd at τ_s=-99."
  Absorbs the `provenance` tuple from the current Held record (see
  *Provenance absorption* below). Typically `attention=flavor`
  unless the provenance is itself load-bearing.
- **authoring-note** — commentary about the *encoding choice*
  itself, addressed to a future reader (human or LLM) who needs to
  understand why this substrate shape was chosen over a plausible
  alternative. Distinct from `authorial-uncertainty` (which is
  doubt about the story) and from `reader-frame` (which is how the
  reader should approach the story); authoring-notes describe the
  *representation*, not the represented. Typically
  `attention=interpretive`; `structural` when a downstream tool or
  reader could draw the wrong conclusion without the note. Example:
  "`scheduled_fight(apollo, mac)` and later
  `scheduled_fight(apollo, rocky)` encode Rocky's Timelock pressure
  structurally — a future τ_s is committed as early as τ_s=-10..."
  (rocky.py D_timelock_not_natively_detectable).

### Extension rule

A new kind is introduced in the encoding or sketch where it first
appears, with:

- a one-line description of what the kind is for
- a note on what attention level(s) it typically uses
- an example text snippet

If a proposed new kind is subsumed by an existing kind, use the
existing one. The vocabulary should stay small enough to be
memorable; a sprawling kind list defeats the point of categorization.

### Anti-kinds — what does not belong

- **affect-projection.** Substrate-sketch-05 retired F1. A
  description of a character's affect uses `kind=texture` (for
  tonal color) or `kind=motivation` (for emotional causation); it
  does not become a typed projection.
- **tension-score, intensity.** Scalar interpretive values do not
  belong. Descriptions are qualitative; if a story needs a
  structural tension signal, it uses substrate queries over gap
  state, not a description field.
- **summary.** A description summarizing what the fold already
  returns is redundant. Summaries belong in tooling, not in the
  description record.

## Attention

Three categorical levels. The level tells a reviewer *what kind of
scrutiny* the description demands, not *how much*.

- **structural** — this description bears on how a nearby fact
  should be read or understood. Must be reviewed. An unreviewed
  structural description is itself a signal that the draft is not
  ready for downstream tooling.
- **interpretive** — meaningful texture a reader or LLM should
  consider when reading the scene. Should be reviewed. An
  unreviewed interpretive description is a backlog item but not a
  blocker.
- **flavor** — background color. Review is optional. Included for
  completeness of authorial voice, not because it changes
  interpretation.

### What goes where, by kind

A rough default mapping (not normative — per-story calls override):

- `texture` → typically `interpretive` or `flavor`.
- `motivation` → typically `interpretive`; `structural` if the
  motivation would change how a later event reads.
- `reader-frame` → typically `structural` (it shapes the whole
  scene's reading) but can be `interpretive` for per-moment frames.
- `authorial-uncertainty` → usually `structural` (an author saying
  "I'm not sure" is a flag that a reviewer should act on).
- `trust-flag` → typically `interpretive`.
- `provenance` → typically `flavor`.
- `authoring-note` → typically `interpretive`; `structural` when
  the encoding choice would be misread without the note.

## Review state

Descriptions carry a history of reviews as a tuple of `ReviewEntry`
records. An entry has:

- **reviewer_id** — who reviewed (human id or LLM identifier).
- **reviewed_at_τ_a** — when, in the shared authored-time.
- **verdict** — `approved`, `needs-work`, `rejected`, or `noted`.
  `noted` means the reviewer read it without taking a position.
- **anchor_τ_a** — the τ_a of the anchor at the time of review. This
  is the key to staleness tracking.
- **comment** — optional free-form text.

### Staleness under anchor edits

When the description's anchor is edited (i.e., a new version of the
anchor event is authored at a later τ_a), every review entry whose
`anchor_τ_a` is less than the new anchor τ_a is considered **stale**.
The entry is not cleared; the staleness is a computed property of
the pair (entry, current-anchor-τ_a). Tooling renders stale entries
as "reviewed at an earlier version; re-review recommended."

This preserves audit history across edits — you can still see that
someone approved an earlier version — while surfacing that the
current version has not been re-blessed.

A description is **effectively unreviewed** if it has no review
entries with `anchor_τ_a` ≥ current anchor τ_a and verdict in
{`approved`, `noted`}. A `rejected` or `needs-work` description is
not unreviewed; it has been seen and flagged. The review queue
prioritizes effectively-unreviewed `attention=structural`
descriptions.

### Verdict semantics

- **approved** — reviewer signs off. The description is considered
  read and accepted at that anchor version.
- **needs-work** — reviewer has objections. Description should be
  edited (appending a new version) or removed by its author.
- **rejected** — reviewer argues the description should not exist
  or its content is wrong in a way that editing won't fix. Rare;
  usually a signal that an author and reviewer disagree about
  whether something is description territory at all.
- **noted** — reviewer read it but chose not to take a position
  (they lack context, or the description is outside their
  expertise). Counts as review for staleness purposes.

## Branch semantics

D4 commits: descriptions default to their anchor's branch set and
can be explicitly scoped to a subset.

### Default: inherit the anchor's branches

A description attached to an event on `{":canonical"}` defaults to
`{":canonical"}`. A description attached to an event on
`{":b-wife"}` defaults to `{":b-wife"}`. If the anchor is on
multiple branches, the description is visible on all of them by
default.

### Override: scope to a subset

An author can explicitly set `branches` to a non-empty subset of
the anchor's branch set. Common case: a canonical event that reads
differently through a specific contested branch's frame.

Example: the canonical event `E_intercourse` under the refactored
Rashomon encoding carries per-branch texture descriptions:

- description(kind=texture, attached_to=E_intercourse,
  branches={":b-wife"}, text="violation — she fights, loses, goes
  silent")
- description(kind=texture, attached_to=E_intercourse,
  branches={":b-tajomaru"}, text="she yields; what begins as
  coercion becomes consent")

Same canonical event, different descriptions on different branches.
The fold still sees one event on canonical (visible to all
branches); the descriptions partition by branch scope.

### Trans-branch descriptions

A description with `branches = {":canonical"}` attached to a
`:canonical` event is visible on every branch via
canonical-is-universal. This is how a description that *compares*
branches lives:

- description(kind=reader-frame, attached_to=E_intercourse,
  branches={":canonical"}, text="across all four testimonies the
  intercourse is the pivot; what differs is whose agency is
  foregrounded in each")

Such descriptions are read on every branch's view. Use them for
cross-branch commentary.

### Subset-override rules

- `branches` must be a non-empty subset of the anchor's `branches`.
- An empty `branches` set is illegal (a description not visible on
  any branch is a bug, not a feature).
- If the anchor's branches change (e.g., an event gets a new branch
  label), the description's branches do not automatically update.
  This is deliberate — branch change is an authorial act; existing
  descriptions should be re-reviewed.

## Promotion mechanics

D5 commits: no auto-promotion. Description → fact is always an
authorial act. Operationally:

### The proposal queue

An LLM or reviewer can *propose* a fact derived from a description.
A proposal is a separate record:

- **PromotionProposal**
  - description_id
  - proposed_fact — an Event or Effect record (constructed but not
    yet added to the event log)
  - proposer_id
  - rationale — free-form text explaining how the proposal derives
    from the description
  - proposed_at_τ_a
  - status — `pending` | `accepted` | `declined`

Proposals live in a queue outside the event log. Tooling renders
the queue; authors review it.

### Author acceptance

When an author accepts a proposal, three things happen:

1. A new event is authored. The event's τ_a is current; it goes
   through normal event authoring (branches, preconditions, effects
   all explicit). The author may modify the proposed fact before
   accepting.
2. The description gains a `promoted_to` link pointing at the new
   event's id. This is an append, not a mutation — the description
   record is immutable, but the *current* description's metadata
   reflects the promotion via a follow-on record at a later τ_a
   whose only change is the added link. (Alternative for
   implementers: a separate `PromotionLink` record pointing
   description → fact; this sketch does not normatively pick.)
3. The proposal's status flips to `accepted`, with the new event's
   id recorded.

### Author decline

When an author declines a proposal, the proposal's status flips to
`declined` with an optional rationale. The description is
unaffected. The proposal record stays in the queue as history (for
audit and to avoid re-proposing the same thing).

### The invariant this protects

Never does an automated process *create facts* from descriptions.
An LLM can read descriptions and propose. An author can accept. The
fold never looks at descriptions; it only folds events. Promotion
is a new event authored by a human (or by an LLM acting with
explicit author identity and review), not a derived computation.

This is where architecture-01 A5 ("interpretation is a partner, not
a fallback") has teeth. Interpretation proposes; authors decide.

## Description API

The substrate's description API is separate from the fold API. They
do not share types in a way that would let a fold function receive
a description.

### Query surface

- `descriptions_for(anchor_ref) -> list[Description]` — all
  descriptions attached to a specific anchor.
- `descriptions_on_branch(branch, up_to_τ_a) -> list[Description]`
  — all descriptions visible on a branch at τ_a.
- `unreviewed(attention: Attention = structural) -> list[Description]`
  — descriptions effectively unreviewed at the current anchor τ_a,
  filtered by attention level. Default is structural (the ones that
  block).
- `open_questions() -> list[Description]` — descriptions with
  `is_question = True`.
- `by_kind(kind: str) -> list[Description]` — filter by kind.
- `promoted() -> list[(Description, Event)]` — descriptions that
  have been promoted, paired with their resulting events. Audit
  surface.
- `proposal_queue(status: Status = pending) -> list[PromotionProposal]`
  — the promotion proposal queue.

### The firewall

Fold functions (`project_knowledge`, `project_world`,
`project_reader` in the substrate) take events and event-derived
structures as input. They do not take descriptions, and their
signatures do not admit descriptions in any field.

At the type level (when implemented), this is enforced by not having
Description be a subtype of any type the fold accepts. There is no
mixed collection that holds both events and descriptions in a way
that could be accidentally folded. Callers that want to display
facts + descriptions together do so at the rendering layer, not the
substrate layer.

## Tooling obligations

Any tool or component that walks the fabula and renders, queries,
or summarizes it must also surface descriptions. Specifically:

- **Rendering a scene.** A demo or report that prints an event
  prints its descriptions alongside, grouped by kind. Structural
  descriptions get visual callouts (the "HEY, check this"
  affordance from architecture-01 A4).
- **Linting.** A linter for a story encoding checks that every
  structural description has at least one non-stale approved review
  at current anchor τ_a. Unreviewed structurals become lint errors;
  stale ones become warnings.
- **Change diffs.** When an anchor is edited, the diff tool shows
  which descriptions lose currency of review (stale).
- **Queries to authors.** An open-question description
  (`is_question=True`) is queued for authorial response; tooling
  can render the queue and track responses.
- **LLM readers.** Any LLM-facing reader of the fabula reads
  descriptions alongside facts. The reader distinguishes the two
  (a description is labeled in prompts so the LLM does not treat
  it as a fold-derived fact). The reader can propose promotions;
  it cannot create facts directly.

These obligations are the teeth of A4's "attention-drafting." A
tool that silently drops descriptions violates the commitment.

## Provenance absorption

Substrate-sketch-05 carries forward a `provenance` field on `Held`
records: a tuple of free-form strings recording where an agent's
knowledge came from ("observed @ τ_s=-99", "told by messenger @
τ_s=7"). This is a proto-description.

Under this sketch, provenance is absorbed into the description
surface:

- A `KnowledgeEffect` or `WorldEffect` with provenance content gains
  one or more `kind=provenance` descriptions attached to the effect.
- The current tuple-of-strings format is preserved for backward
  compatibility; each string becomes the `text` of one
  `kind=provenance` description.
- The description's `attention` is `flavor` by default. If a
  provenance note is itself load-bearing (e.g., "this detail is a
  retcon — see draft notes"), the description author can elevate
  to `interpretive` or `structural`.
- The `authored_by` field on a provenance description is typically
  the author of the containing event.
- Branches default from the anchor effect (effectively, the
  containing event's branches).

When the prototype iterates to use descriptions, the `provenance`
tuple is deprecated in favor of a `descriptions` attachment on
`KnowledgeEffect` and `WorldEffect`. Encodings migrate at their own
pace; the transition is mechanical.

## Worked example — Rashomon under sketch 05 + descriptions

This example shows the refactored Rashomon encoding, applying both
substrate-sketch-05's M1 rule and this sketch's description surface.

The `E_intercourse_bare` canonical event plus per-branch
`E_w_coerced` / `E_t_yields` events are replaced by one canonical
`E_intercourse` event with per-branch texture descriptions, plus a
reader-frame description on canonical:

```
Event(
    id="E_intercourse",
    type="intercourse",
    τ_s=5, τ_a=6,
    participants={"a": "tajomaru", "b": "wife"},
    branches=frozenset({":canonical"}),
    effects=(
        world(had_intercourse_with("tajomaru", "wife")),
        observe("tajomaru", had_intercourse_with("tajomaru", "wife"), 5),
        observe("wife",     had_intercourse_with("tajomaru", "wife"), 5),
        observe("husband",  had_intercourse_with("tajomaru", "wife"), 5),
    ),
)

# Per-branch texture descriptions scoped to their branches:
Description(
    id="D_intercourse_wife_texture",
    attached_to=anchor_event("E_intercourse"),
    kind="texture",
    attention=structural,
    text="violation — she fights, loses, goes silent",
    branches=frozenset({":b-wife"}),
    authored_by="author",
    τ_a=6,
)

Description(
    id="D_intercourse_tajomaru_texture",
    attached_to=anchor_event("E_intercourse"),
    kind="texture",
    attention=structural,
    text="she yields; what begins as coercion becomes consent",
    branches=frozenset({":b-tajomaru"}),
    authored_by="tajomaru-testimony",
    τ_a=6,
)

# ... similar for :b-husband and :b-woodcutter

# Trans-branch reader-frame description:
Description(
    id="D_intercourse_frame",
    attached_to=anchor_event("E_intercourse"),
    kind="reader-frame",
    attention=structural,
    text="across all four testimonies the intercourse is the pivot; "
         "what differs is whose agency is foregrounded",
    branches=frozenset({":canonical"}),
    authored_by="author",
    τ_a=6,
    is_question=False,
)
```

Similarly, the combat event on `:b-tajomaru` that previously
carried `duel_character(A, B, "noble")` as a typed proposition
keeps only the structural facts and attaches a texture description:

```
Event(
    id="E_t_duel",
    type="combat",
    τ_s=9, τ_a=23,
    participants={"a": "tajomaru", "b": "husband"},
    branches=frozenset({":b-tajomaru"}),
    effects=(
        world(killed("tajomaru", "husband")),
        world(killed_with("tajomaru", "husband", "sword")),
    ),
)

Description(
    id="D_t_duel_character",
    attached_to=anchor_event("E_t_duel"),
    kind="texture",
    attention=interpretive,
    text="twenty-three strokes; Tajomaru fought as to an equal, "
         "respecting the husband's skill",
    branches=frozenset({":b-tajomaru"}),
    authored_by="tajomaru-testimony",
    τ_a=23,
)
```

The `duel_character` predicate is gone. The "noble" quality lives
in prose that a reader or LLM reads; no fold dispatches on it.

### An authorial-uncertainty example

The woodcutter's confession is read in the film as partially
self-serving. This is interpretation, not a fact. Representing the
author's own uncertainty:

```
Description(
    id="D_woodcutter_trust",
    attached_to=anchor_event("E_wc_theft"),
    kind="trust-flag",
    attention=interpretive,
    text="woodcutter's self-incrimination (the stolen dagger) "
         "reads as candor, but he's also the last witness and "
         "the only one without an alibi. The film declines to "
         "adjudicate; this encoding does the same.",
    branches=frozenset({":b-woodcutter"}),
    authored_by="author",
    τ_a=84,
)

Description(
    id="D_wc_authorial_doubt",
    attached_to=anchor_desc("D_woodcutter_trust"),
    kind="authorial-uncertainty",
    attention=structural,
    text="am I representing this right? the film's stance on "
         "woodcutter's reliability is famously contested.",
    is_question=True,
    authored_by="author",
    τ_a=84,
)
```

Note the description-on-description: `D_wc_authorial_doubt` is
attached to `D_woodcutter_trust`, carrying the author's open
question about their own interpretation. The review queue surfaces
this because `attention=structural` and it is effectively
unreviewed.

## Amendments

### 2026-04-19 — `authoring-note` kind + `superseded` status

This amendment adds one kind and one status value that the corpus
and the substrate edit-chain machinery have been using for some
time without explicit §Kinds or §Optional fields support. Both are
retroactive recognitions of load-bearing patterns, not new
commitments.

#### Addition 1 — `authoring-note` as a seventh kind

**What changed.** Added `authoring-note` to §Kinds with typical
attention, distinguishing semantics, and an example; added the
corresponding row to §Attention §What goes where, by kind.

**Structural justification.** The rocky encoding uses the kind
on two descriptions at two distinct attention levels
(`prototype/story_engine/encodings/rocky.py`):

- `D_scripted_stunt_is_epistemic` — `interpretive`; explains why
  Apollo's scripted-stunt intention is encoded as a held belief
  rather than a world fact.
- `D_timelock_not_natively_detectable` — `structural`; explains
  how Rocky's Timelock pressure is encoded structurally via early
  `scheduled_fight` effects rather than a dedicated predicate, and
  what that means for downstream classifiers.

Two records on one encoding is a smaller corpus than the six
starting kinds enjoy, but the content each authoring-note carries
is genuinely distinct from the six. It is not uncertainty about
the story (`authorial-uncertainty`), not reader framing
(`reader-frame`), not tonal affect (`texture`), not per-agent
motivation (`motivation`), not a trust annotation (`trust-flag`),
and not audit provenance (`provenance`). It is commentary about
*how the substrate represents the story* — why this event is a
held belief not a world fact, why this pressure is carried by
structure not by predicate — addressed to a future reader (human
or LLM) trying to understand the encoding. Subsumption by an
existing kind was considered and rejected; a seventh kind is the
honest home.

Per §Extension rule, a new kind is introduced with a one-line
description, a typical attention level, and an example; this
amendment supplies all three.

**Grid-snap posture.** `authoring-note` documents the encoding
choice; the fold does not touch it, and a downstream tool that
filters by kind can select or omit it trivially. The kind adds
authoring-surface richness without asking the substrate to carry
more structural load — schema grid-snap holds.

#### Addition 2 — `superseded` as a third status value

**What changed.** Extended `status` in §Optional fields from
`{committed, provisional}` to `{committed, provisional,
superseded}`; clarified §Record-level invariants to distinguish
content-immutability (strict, on the semantic fields) from the
two-field mutation surface (status + supersession metadata) that
the edit-chain mechanism requires.

**Structural justification.** §Record-level invariants already
commits to append-on-edit: "Once authored at τ_a = n, a
description is not mutated. Edits append a new description at τ_a
= n+k." That commitment was incomplete — it did not name the
marker distinguishing current head-of-chain from superseded
predecessors. The substrate's edit-chain code
(`prototype/story_engine/core/substrate.py
apply_description_edit`) and the reader-model-client edit paths
(`prototype/story_engine/core/reader_model_client.py`) have been
using `DescStatus.SUPERSEDED` plus `metadata.{supersedes,
superseded_by}` pointers as that marker since the feature was
added; the macbeth encoding ships superseded descriptions in its
corpus directly. Without `superseded` in the sketch, the sketch's
own append-on-edit commitment cannot be implemented.

The revised §Record-level invariants text acknowledges the precise
scope of the mutation: only the source record's `status` flag and
supersession metadata change when a successor lands; text, kind,
attention, and the other semantic fields remain immutable. The
successor is a fresh record with its own τ_a.

**Grid-snap posture.** `superseded` and the supersession pointers
are structural — the substrate reads them (see `substrate.py
descriptions_on_branch` with `include_superseded`) to filter
supersession chains out of visible-state views. The interpretive
load — *why* a description was superseded — stays in the
successor's text, not in the supersession metadata. Schema
grid-snap holds.

#### Conformance implication

`prototype/tests/test_production_format_sketch_01_conformance.py`
has carried two dispositions (`DISPOSITION_KIND_AUTHORING_NOTE`,
`DISPOSITION_STATUS_SUPERSEDED`) that tolerate schema-rejection
of these values while this amendment was pending. Both retire
under the follow-on implementation commit for this amendment:
`schema/description.json` adds each value to its enum, and the
disposition constants plus their classification branches are
removed from the conformance test. The Description corpus goes
clean on both axes.

## Open questions

1. **Description versioning.** The sketch commits to immutability
   with append-on-edit. The exact shape of an "edit chain" (back-
   references, diff semantics) is left to tooling. Revisit when a
   second iteration of the prototype produces its first
   description edit.
2. **Review-state granularity.** Should review verdicts be per-
   field (you can approve the text but flag the attention level)
   or per-description (approve or not)? Sketch 01 goes with per-
   description. If reviewers end up wanting sub-record verdicts,
   revisit.
3. **Proposal queue persistence.** The proposal queue is out of the
   event log but the sketch does not specify where it lives. Same
   place as descriptions? Separate journal? Tooling decision.
4. **LLM identity in authored_by.** Representing "this description
   was written by Claude Sonnet 4.6 with temperature 0.7 at
   2026-04-13" is useful for audit but also a versioning nightmare.
   The sketch accepts "llm:<identifier>" as the format; the
   identifier's internal shape is out of scope.
5. **Extended kinds across the project.** The starting six
   (texture, motivation, reader-frame, authorial-uncertainty,
   trust-flag, provenance) cover the current encoding. As more
   stories are encoded, additional kinds will be proposed. A
   kind-registry is a natural tooling surface; sketch 01 does not
   mandate one.
6. **Cascading staleness.** If a description is attached to another
   description, and the outer description is edited, does the
   inner description's reviews become stale? Probably yes
   (interpretation-on-interpretation depends on what it comments
   on), but the rule deserves explicit spelling out in a future
   iteration.
7. **Descriptions on provisional content.** A description attached
   to a `provisional` event — is it also considered provisional
   regardless of its own status? Sketch 01 says descriptions have
   their own status independent of anchor, but the rendering
   convention should probably inherit provisionality visually.
8. **Canonical merge of branch-scoped descriptions.** If two
   sibling contested branches carry compatible descriptions on a
   shared canonical anchor, is there a mechanism to merge them to
   canonical? Probably yes, via an authorial act. Spelling it out
   is deferred.
9. **Description diff ergonomics.** When an anchor edit invalidates
   five reviews, the tooling surface for "re-review these five"
   matters a lot for practical use. Out of scope for this sketch
   but flagged as an adoption risk.
10. **The promotion audit link's exact representation.** Sketch 01
    describes `promoted_to` on the description but punts on whether
    that is a mutation-via-append or a separate `PromotionLink`
    record. A sketch iteration should normatively pick one.

## Discipline

Process expectations for work against this sketch:

- **New kinds are introduced with documentation.** A sketch or
  encoding that adds a kind beyond the starting six includes a
  one-line description, typical attention level, and an example.
  Subsuming an existing kind is preferred to adding a new one.
- **High-attention descriptions are reviewed before a sketch or
  encoding ships.** Structural descriptions that are effectively
  unreviewed at publication time are a signal that the work is not
  ready.
- **Authorial-uncertainty descriptions are not permanent.** They
  are promises to resolve. A draft that ships with a structural
  authorial-uncertainty description unresolved is incomplete.
- **Tooling that renders the fabula renders descriptions.** No
  tool that presents events to a reader (human or LLM) may omit
  descriptions silently. Filtering is explicit and visible.
- **A description never becomes a fact via automated pipeline.**
  Promotion is always an event authored by a human (or by an LLM
  acting with explicit author identity and review). Proposal
  queues are fine; direct promotion is not.

## Summary of the description surface

| | Facts (events, effects, propositions) | Descriptions |
|---|---|---|
| Typed structure | yes | yes (fields + text blob) |
| Truth-evaluable | yes | no |
| Fold-visible | yes | no |
| Query API | substrate fold | description API |
| Attached_to | — | required (an anchor) |
| Attention affordance | — | required (categorical) |
| Review state | — | tracked, stale-on-anchor-edit |
| Promotion direction | — | description → fact, authorial only |
| Branches | membership set on the record | default from anchor, override allowed |
| Carried by prototype | events, effects, Held records | not yet; pending iteration |
