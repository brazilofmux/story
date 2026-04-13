# Reader-model — sketch 01

**Status:** draft, active
**Date:** 2026-04-13
**Supersedes:** nothing (new topic)
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [substrate-sketch-05.md](substrate-sketch-05.md), [descriptions-sketch-01.md](descriptions-sketch-01.md)
**Superseded by:** nothing yet

## Purpose

Formalize the reader-model surface that
[architecture-sketch-01.md](architecture-sketch-01.md) A5 commits to
and that [descriptions-sketch-01.md](descriptions-sketch-01.md) leaves
as an external dependency. The reader-model is the component — human
or LLM — that *reads* the fabula, sjuzhet, and descriptions and
produces interpretive outputs: reviews, promotion proposals, answers
to open questions. Without a specified reader-model, the description
surface is write-only; A5's "interpretation is a partner, not a
fallback" has no teeth.

This sketch specifies:

- The typed view the reader-model sees.
- Invocation modes (interactive, triggered, batch) and their scope.
- The typed output shape (reviews, proposals, question-answers).
- The firewall from the read side: descriptions are always labeled
  as descriptions; the reader-model cannot mistake them for facts.
- The partner-not-fallback invariant with operational teeth:
  reader-model outputs are suggestions; promotion is authorial.
- Cost and scope discipline: every invocation declares what it
  reads.
- Failure modes and how they are handled structurally.
- The API surface — what the substrate exposes and what lives in
  tooling.
- A worked example using the Rashomon encoding's existing
  descriptions.

## What this sketch is *not* committing to

- A specific LLM provider, model, or prompt template.
- The serialization format of the typed view (JSON, XML, Protobuf,
  something else — tooling decision).
- Prompt-engineering practices or chain-of-thought structures.
- Caching strategy beyond the staleness rule
  descriptions-sketch-01 already provides.
- Rate limiting, cost budgeting, or retry policy.
- Multi-turn LLM dialogue state or persistent conversational
  memory.
- UI surfaces for reviewing reader-model outputs.
- How human reviewers interact with the same surface (the sketch
  treats humans and LLMs as interchangeable reviewer kinds; the
  UX difference is out of scope).

If a question starts "what model," "what prompt format," "how do I
cache this," or "how does the review UI render this" — it is out of
scope.

## What this sketch *is* committing to

1. **R1 — Typed I/O.** The reader-model consumes a typed view and
   produces typed outputs. No free-form prose crosses the boundary
   between substrate and reader-model as a substrate-visible
   artifact. Prose lives *inside* typed record fields (description
   text, review comments, proposal rationale), never as the outer
   envelope.
2. **R2 — Descriptions are labeled in the view.** The view surface
   distinguishes facts from descriptions structurally. A reader-model
   cannot receive a description where a fact is expected, or
   vice versa. This is the read-side half of descriptions-sketch-01
   D1's firewall.
3. **R3 — Partner, not fallback.** The reader-model proposes; the
   author decides. Reader-model outputs never mutate substrate state
   directly. Accepted outputs produce new events, new reviews, or
   new descriptions via authorial act.
4. **R4 — Reviews and proposals are first-class, shared with
   humans.** An LLM review is a `ReviewEntry` with
   `reviewer_id="llm:<identifier>"`. A human review is a
   `ReviewEntry` with `reviewer_id="<human-id>"`. The substrate does
   not distinguish them beyond the id; staleness, queue priority,
   and promotion machinery treat both the same.
5. **R5 — Every invocation declares its scope.** A reader-model call
   names the branch, τ_a bound, attention filter, and the explicit
   descriptions (or anchor events) it is reading. There are no
   hidden LLM calls behind substrate fold functions. Cost is visible.
6. **R6 — Staleness via anchor-τ_a, uniformly.** An LLM review
   becomes stale under the same rule as a human review: when the
   anchor is edited at a later τ_a, the review's `anchor_τ_a` is
   stale. Re-invocation of the reader-model is an explicit act, not
   an automatic background pass.

R1 through R6 pass architecture-sketch-01 A3: they describe drift
the schema catches (untyped LLM output, descriptions masquerading as
facts, hidden side-effects, mixing reviewer identities), not content
an attentive reviewer could self-police from prose.

## Relation to architecture-sketch-01, substrate-sketch-05, descriptions-sketch-01

- Architecture-01 A5 named LLM/human interpretation as first-class;
  this sketch specifies the surface that makes A5 executable.
- Architecture-01 A2's two-surface semantics extend: the reader-model
  reads both surfaces, always labeled, and writes only into a third
  surface (review records, proposal queue, new descriptions) that
  feeds back into the description surface via authorial acceptance.
- Descriptions-sketch-01 specified `review_states`, the proposal
  queue, and the `is_question` flag. This sketch specifies who
  produces those records, under what invocation, and what view they
  work from.
- Substrate-sketch-05 L1 called out library operators as consumers
  of fold state; the reader-model is not a library operator — it
  sits alongside, consuming the *same* view tooling a library
  operator might consume. The difference: library operators produce
  typed queries over structure; the reader-model produces typed
  judgments over interpretation.

The four-sketch stack, in reading order:

1. **Architecture-01** — the frame. What kind of thing is this
   project.
2. **Substrate-05** — the typed-fact surface.
3. **Descriptions-01** — the typed-interpretive-record surface.
4. **Reader-model-01** — how interpretation gets done. *(this
   sketch)*

## The reader-model view

The view is a typed structure. Tooling serializes it for a specific
reader (a JSON prompt for an LLM, a rendered document for a human
reviewer, a compact representation for a batch job). The substrate
produces the view; the reader consumes it.

### View shape

A `ReaderView` carries:

- **branch** — the branch label the view is scoped to.
- **up_to_τ_s** — story-time bound. Events later than this are
  excluded.
- **up_to_τ_a** — authored-time bound. Descriptions and review
  history later than this are excluded. Used for reproducibility:
  re-running the view at a later τ_a produces a strict superset of
  what the earlier view saw, in the common case.
- **attention_filter** — which attention levels are included in the
  descriptions section. A structural-only invocation excludes flavor
  and interpretive descriptions, keeping the view small.
- **events** — ordered list of `EventRecord` entries (see below),
  each carrying:
  - The structural event data (id, type, τ_s, participants,
    effects, branches).
  - A **facts** tag: every effect is labeled as a fact.
- **descriptions** — ordered list of `DescriptionRecord` entries,
  each carrying:
  - The description data (id, kind, attention, text, authored_by,
    τ_a, branches, review_states, is_question).
  - A **description** tag: the record is labeled as interpretive.
  - **anchor reference** resolving the description's `attached_to`
    to an event or another description within the view.
  - **effectively-unreviewed** flag computed at the view's τ_a.
  - **stale review entries** flagged individually.
- **open_questions** — the subset of descriptions where
  `is_question=True`. Pulled out for convenience; duplicated from
  `descriptions`.
- **optional queries** — precomputed substrate queries the tooling
  chose to include: reader's current gaps, live ironies at τ_s,
  etc. The view does not *require* these; a minimal view ships
  just events+descriptions.

### What the view does NOT include

- Hidden fields the substrate knows but did not disclose. If the
  tooling passes the full view, it passes the full view; no secret
  state.
- Events from out-of-scope branches. Branch scoping applies to the
  view the same way it applies to a fold.
- Descriptions from out-of-scope branches. D4 branch semantics
  apply.
- Free-form prose summaries. The view is the data; tooling
  constructs any narrative summary it wants *outside* the typed
  surface.

### Structural distinction between facts and descriptions

The view is, structurally, two lists. Events carry effects (facts);
descriptions carry text (interpretation). A reader — LLM or human —
consuming a serialized view must be able to tell, for every item in
the view, which kind it is. Tooling renders the distinction loudly:

- A JSON serialization uses separate top-level arrays
  (`"events": [...]`, `"descriptions": [...]`), not a merged
  `"items"` list.
- A prose serialization (for human or LLM consumption) uses
  distinct section headers, and within the descriptions section
  each entry is prefixed with its kind and attention (`[texture /
  interpretive]`).
- The reader-model's contract: *never conflate the two surfaces*.
  A prompt that reads "here are the facts, which include the
  wife's yielding" is a contract violation; the yielding is a
  description, and the prompt must label it so.

This is R2 with teeth.

## Invocation modes

Three modes. Each has a different use case and scope discipline.

### Interactive

The author asks a specific question. Synchronous, small scope.

- "Review these five unreviewed structural descriptions on
  `:b-woodcutter`."
- "Propose any facts you think should be promoted from description
  `D_intercourse_wife_texture`."
- "Answer the question in `D_wc_authorial_doubt`."

The invocation names the descriptions (or events) in its scope. The
view is constructed around that scope; the reader-model returns
typed outputs; the author reviews each output before anything lands.

### Triggered

An event in the authoring workflow fires a reader-model invocation
as part of the event's completion. Examples:

- A new `attention=structural` description is authored; the
  workflow triggers an LLM review as part of the commit, queuing
  the review for the author's attention.
- An anchor event is edited, making all existing reviews stale; the
  workflow triggers a re-review pass on the affected descriptions.

Triggered invocations have narrow, declared scope. The trigger
specifies what the reader-model sees and the output is ingested
into the review queue without blocking the triggering act (the
description still commits; the review lands alongside).

### Batch

The author runs an explicit scan over the whole story, a branch, or
a τ_a range. Slower, broader scope.

- "Walk all descriptions on all branches and flag any that look
  inconsistent with the facts they anchor to."
- "Propose any promotions the last ten commits might warrant."

Batch invocations are explicit, not scheduled. The substrate does
not run them on its own; some external process (author script,
tooling job) invokes them.

### No fourth mode

The substrate does not automatically invoke the reader-model. No
fold function triggers an LLM call. No query internally consults
interpretive content. This is R5 with teeth: every invocation is
visible, declared, and auditable.

## Output shape

The reader-model returns typed records. Three kinds:

### Review records

```
ReviewEntry(
    reviewer_id="llm:claude-sonnet-4-6",
    reviewed_at_τ_a=<current τ_a>,
    verdict=<approved|needs-work|rejected|noted>,
    anchor_τ_a=<anchor τ_a at review time>,
    comment="<rationale>",
)
```

One per description the reader-model reviewed. `comment` is where
the reader-model's reasoning lives as prose, stored as a field
value. The rest of the record is typed.

### Promotion proposals

```
PromotionProposal(
    description_id=<source description id>,
    proposed_fact=<Event or Effect record>,
    proposer_id="llm:claude-sonnet-4-6",
    rationale="<why>",
    proposed_at_τ_a=<current τ_a>,
    status="pending",
)
```

One per proposal. The `proposed_fact` is a constructed record — not
yet committed; it lives only in the proposal until an author
accepts. Shape per descriptions-sketch-01.

### Question-answers

For descriptions with `is_question=True`, the reader-model can
propose an answer. An answer is *itself* a new description (kind
depending on the question) attached to the anchor the question was
asking about:

```
Description(
    id=<new>,
    attached_to=<original anchor — not the question description>,
    kind=<author's pick — often motivation or reader-frame>,
    attention=interpretive,
    text="<answer text>",
    authored_by="llm:claude-sonnet-4-6",
    τ_a=<current τ_a>,
    metadata={"answers_question": <question description id>},
)
```

The answer is a *proposed* description. It lands in the proposal
queue alongside fact proposals; an author accepts or declines. The
accepting act promotes the proposed description into the committed
description set, with the link back to the question via metadata.

An accepted answer does not delete the question. The question
stays, with the answer linked. Future review sees both.

### Refusals and malformed output

The reader-model may refuse a task (safety filter, context limit,
confidence too low) or return malformed output. Both cases are
explicit:

- **Refusal** — a `Refusal` record: which task was refused, why
  (if the reader-model gives a reason), and whether retry is
  advisable. Refusals are not errors; they are first-class
  outputs. The author sees them and decides whether to escalate.
- **Malformed** — if the LLM returns prose that cannot be parsed
  into typed records, the ingest layer wraps it in a `Malformed`
  record with the raw text preserved and a parse-error description.
  No partial state is mutated; the review/proposal did not happen.

Refusal and malformed outputs are ingested into the same queue as
successful outputs, flagged distinctly. They are visible to the
author.

## Scope discipline

Every `reader_view` call declares, explicitly:

- **branch** — which branch.
- **up_to_τ_s** — story-time bound.
- **up_to_τ_a** — authored-time bound.
- **attention_filter** — which descriptions to include.
- **anchor_scope** — optional: a specific set of anchor ids (events
  or descriptions) to restrict to, for narrow invocations.

No `reader_view` call consults state not reachable from those
parameters. Two identical `reader_view` calls at the same τ_a
produce identical views. This is reproducibility.

The substrate does not pay for a reader-model call the caller did
not request. Tooling chooses when to invoke; the substrate offers
the view and the ingest path.

## Failure modes

### LLM returns malformed output

Parse fails → `Malformed` record ingested. No state mutated beyond
the queue entry. Author sees the failure.

### LLM refuses

Refusal record ingested. Author decides whether to re-invoke, with
different context, or to give up.

### LLM references a description that has been edited since the
invocation began

The review's `anchor_τ_a` reflects the view's snapshot. If the
anchor was edited during the LLM's runtime, the ingested review
is already stale per R6. Author sees the staleness and decides
whether to re-invoke.

### LLM proposes a structurally invalid fact

The proposal queue carries malformed proposals with a validation
note. The author can amend the proposal before accepting, or
decline.

### LLM disagrees with a prior human review

No special handling. The description's `review_states` tuple
carries both reviews. The author sees both and reconciles.
Disagreement is data, not an error.

### LLM outputs at different runs disagree with each other

Same — both reviews are preserved. No automatic majority vote or
consensus mechanism. If the author wants that, it lives in
tooling.

## API surface

The substrate exposes:

### View construction

```
reader_view(
    branch: Branch,
    events: list[Event],
    descriptions: list[Description],
    all_branches: dict,
    up_to_τ_s: int,
    up_to_τ_a: int,
    attention_filter: set[Attention] | None,
    anchor_scope: set[str] | None,
    include_queries: list[str] | None,
) -> ReaderView
```

Deterministic, pure, no side effects. Suitable to call repeatedly;
caching is tooling's job (the view is reproducible at the same
τ_a).

### Ingest

```
ingest_review(
    description: Description,
    review: ReviewEntry,
) -> Description
```

Appends the review to the description's `review_states`, returning
a new immutable `Description` record (per descriptions-sketch-01's
record-level invariants — edits append, do not mutate).

```
ingest_proposal(
    proposal: PromotionProposal,
    queue: list[PromotionProposal],
) -> list[PromotionProposal]
```

Appends to the proposal queue. The queue is a list because ordering
(by `proposed_at_τ_a`) matters for review.

```
ingest_question_answer(
    answer: Description,
    queue: list[PromotionProposal],
) -> list[PromotionProposal]
```

An answer proposal lands in the same queue, typed as a description
proposal rather than a fact proposal. The queue carries both kinds;
the author's workflow distinguishes.

### What is NOT on the substrate side

- The LLM call itself. `reader_view` produces the view; a separate
  tooling layer calls the LLM, parses the response, and calls
  `ingest_*` with the results. The substrate does not own the
  network.
- The prompt template. Tooling concern.
- The retry / rate-limit / context-window strategy. Tooling.
- The queue's persistence. Tooling (same as descriptions-sketch-01
  OQ 3).
- Cost accounting. Tooling.

## Worked example — Rashomon

The encoding committed two descriptions with direct reader-model
relevance:

- `D_woodcutter_trust` — trust-flag, `attention=interpretive`,
  attached to `E_wc_theft` on `:b-woodcutter`.
- `D_wc_authorial_doubt` — authorial-uncertainty,
  `attention=structural`, `is_question=True`, attached to
  `D_woodcutter_trust`.

### Interactive invocation — answer the open question

The author asks: "Answer the question in `D_wc_authorial_doubt`,
using the view for `:b-woodcutter` at τ_a=10_000."

```
view = reader_view(
    branch=B_WOODCUTTER,
    events=EVENTS_ALL,
    descriptions=DESCRIPTIONS,
    all_branches=ALL_BRANCHES,
    up_to_τ_s=100,
    up_to_τ_a=10_000,
    attention_filter={Attention.STRUCTURAL, Attention.INTERPRETIVE},
    anchor_scope={"D_wc_authorial_doubt", "D_woodcutter_trust",
                  "E_wc_theft", "E_wc_fight"},
    include_queries=None,
)
```

The view contains:

- Events: `E_wc_fight`, `E_wc_theft`, plus their canonical
  ancestors (`E_travel`, `E_lure`, etc., visible via the
  canonical-is-universal rule). All labeled as facts.
- Descriptions: `D_woodcutter_trust` and `D_wc_authorial_doubt`,
  both labeled as descriptions. The description-on-description
  chain is resolved: `D_wc_authorial_doubt.anchor_reference`
  points at `D_woodcutter_trust` within the view.
- `open_questions`: includes `D_wc_authorial_doubt`.

The LLM returns an `Answer`:

```
Description(
    id="D_wc_authorial_doubt_answer_1",
    attached_to=anchor_event("E_wc_theft"),
    kind="reader-frame",
    attention=Attention.INTERPRETIVE,
    text="The film holds the woodcutter's reliability deliberately "
         "open; his self-incrimination argues candor, but the priest "
         "at the gate never endorses his account above the others. "
         "The current encoding's refusal to adjudicate matches the "
         "film's refusal to adjudicate.",
    authored_by="llm:claude-sonnet-4-6",
    τ_a=10_001,
    metadata={"answers_question": "D_wc_authorial_doubt"},
)
```

Plus a `ReviewEntry` on the question itself:

```
ReviewEntry(
    reviewer_id="llm:claude-sonnet-4-6",
    reviewed_at_τ_a=10_001,
    verdict=ReviewVerdict.NOTED,
    anchor_τ_a=185,
    comment="Question answered; see D_wc_authorial_doubt_answer_1.",
)
```

Ingest:

```
DESCRIPTIONS_v2 = [...as before..., answer_description]
question_v2 = ingest_review(question_v1, review)
```

The question is no longer effectively-unreviewed at its anchor τ_a.
The proposed answer sits in the queue. The author reviews the
proposed answer, decides whether the reader-frame description it
offers is accurate enough to accept into the encoding, and either
promotes it (new description committed) or declines it (queue
entry marked declined; question remains, with a noted review).

### Triggered invocation — LLM-review of a new structural description

A future author adds a new `kind=motivation`,
`attention=structural` description explaining why the woodcutter
steals the dagger. The triggered invocation scope:

- `branch=B_WOODCUTTER`
- `anchor_scope={<new description id>, E_wc_theft}`
- `attention_filter={STRUCTURAL}`

The LLM returns a `ReviewEntry` with verdict=approved or
needs-work. The commit completes; the review lands in the
description's `review_states`.

### Batch invocation — scan for unreviewed structurals

At a milestone, the author runs a batch scan:

```
view = reader_view(
    branch=B_CANONICAL,  # and each contested branch in turn
    events=EVENTS_ALL,
    descriptions=DESCRIPTIONS,
    all_branches=ALL_BRANCHES,
    up_to_τ_s=1000,
    up_to_τ_a=current_τ_a,
    attention_filter={Attention.STRUCTURAL},
    anchor_scope=None,
    include_queries=["open_questions"],
)
```

The LLM reviews every structural description not already
effectively-reviewed. Output: a batch of `ReviewEntry` records and
(possibly) `PromotionProposal` records. The author works the batch
over time.

## Open questions

1. **Context-window management.** The view for a large story may
   exceed an LLM's context. Chunking strategies (per-branch,
   per-scene, per-anchor) are tooling decisions; the sketch does
   not prescribe. If a standard chunking emerges, a follow-on
   sketch documents it.
2. **Persistent conversational state between invocations.** Each
   `reader_view` call is independent. Multi-turn dialogue (an LLM
   reviewing, asking a clarifying question, waiting for a human
   answer, resuming) is out of scope. A future sketch may add it.
3. **Reviewer identity granularity.** "llm:claude-sonnet-4-6" is
   the format; the identifier's internal shape (version, prompt,
   temperature) is tooling's to decide. When a model upgrades, old
   reviews under the old id should probably be revalidated, but
   the trigger condition for that is open.
4. **Human/LLM review equivalence.** The sketch treats them as
   interchangeable record kinds. A human who disagrees with an
   LLM review might want a different weight; the sketch does not
   provide weighting. If needed, it lives in a follow-on sketch
   (review-weighting).
5. **Consensus across multiple LLM reviewers.** If the same
   description is reviewed by three LLMs and they disagree, no
   automatic resolution happens. Consensus machinery (majority
   vote, escalation to human) is out of scope. All reviews are
   preserved; the author reconciles.
6. **Reader-model proposing description *edits*.** The sketch
   covers review, promotion-proposal, and question-answer. It
   does not cover "the LLM suggests rephrasing the text of a
   description." Probably fits via a proposal that produces a new
   description version (descriptions are immutable; edits append).
   Out of scope for this sketch but natural next addition.
7. **Reader-model reading reader-model output.** An LLM review of
   a prior LLM review. Possible; the sketch permits it (review
   records are data like anything else). Whether it's *useful* is
   empirical; no prescription here.
8. **Cost/quota discipline.** The sketch states reader-model
   invocations are explicit; it does not prescribe cost accounting
   or budget limits. Those live in tooling. A follow-on sketch may
   formalize if the scale warrants.
9. **Reader-model over sjuzhet entries (not just events and
   descriptions).** Sjuzhet entries are anchor-eligible per
   descriptions-sketch-01. The sketch's view includes events and
   descriptions; it does not explicitly call out sjuzhet entries.
   Extending the view to include them is mechanical; held back
   until a case exercises it.
10. **Whether a reader-model can be *preregistered* to be invoked
    on specific triggers.** ("Every time a structural description
    is authored on :b-*, invoke the LLM automatically.") The
    sketch says triggers are tooling. A follow-on workflow sketch
    might formalize a registry.

## Discipline

Process expectations for work against this sketch:

- **Views are typed, not prose blobs.** A `reader_view` function
  returns structured data. Prose lives inside typed fields. Any
  tooling that serializes the view documents the mapping.
- **Outputs are typed, not free prose.** The reader-model returns
  `ReviewEntry`, `PromotionProposal`, and `Description` records —
  not a monolithic response blob. Tooling that calls an LLM and
  cannot obtain structured output is responsible for parsing.
- **No hidden invocations.** The substrate never calls the
  reader-model implicitly. Fold functions remain pure. A regression
  where a query internally invokes an LLM is a contract violation.
- **Reviewer identity is faithful.** `reviewer_id` records the
  actual reviewer. An LLM-generated review never claims a human
  author; a human-authored review never claims an LLM identity.
- **Refusals and malformed outputs are visible.** They are not
  swallowed, logged, and forgotten. They become first-class queue
  entries.
- **Staleness applies uniformly.** An LLM review stales when its
  anchor edits, same as a human review. No special casing for the
  machine.

## Summary of the reader-model surface

| | Facts (events, effects) | Descriptions | Reader-model |
|---|---|---|---|
| Typed | yes | yes | yes (typed I/O) |
| Truth-evaluable | yes | no | n/a |
| Fold-visible | yes | no | no |
| Produced by | authorial events | authorial records | human or LLM |
| Mutates substrate | yes (authored events) | yes (authored records) | no — proposes only |
| Invocation | any query | any query | explicit, scoped |
| Staleness | n/a | review-state vs anchor τ_a | same as descriptions |
| Partner to | — | facts (A2) | descriptions (A5) |
