# Design

Architectural sketches and design notes for the story-telling engine. Each sketch is numbered and dated; revisions do not overwrite predecessors. Old sketches are left in place as a record of how the design changed, so the reasoning over time is preserved.

## Convention

- Files named `{topic}-sketch-NN.md` where NN is sequential per topic. A *topic* is a coherent design area — `substrate`, `architecture`, `descriptions`, and so on. Each topic has its own sequence.
- Every sketch has a **Status** (*draft, active*, *superseded*, *abandoned*) and a **Date** at the top.
- **Active sketches are self-contained within their topic.** A reader should be able to understand the current state of *that topic* from the active sketch alone, without chasing a chain of deltas. When corrections pile up, consolidate into a new sketch rather than let the active starting point depend on superseded context.
- **Cross-topic sketches are expected.** Some sketches (notably architecture-level ones) apply across topics. They do not supersede the sketches they constrain; they add a frame that future topic sketches are expected to satisfy. Reading a topic sketch alone gives the reader that topic's current state; reading the cross-topic sketches additionally gives them the frame those topic sketches sit inside.
- When a sketch is superseded, its status is updated and a link to the successor is added — but the file stays.
- Sketches are not specifications. They are the design thinking in progress. Claims and commitments may be wrong. Open questions are first-class.

## Active sketches

These are the sketches to read. Each is self-contained within its topic; no need to chase predecessors for that topic. Cross-topic sketches (architecture) sit alongside and add a frame.

**Cross-topic (applies across topics):**

- [Architecture — sketch 01](architecture-sketch-01.md) — grid-snap scope, two-surface semantics (facts vs descriptions), test for schema inclusion, descriptions draft attention. Frames all substrate and descriptions work. See its *Relation to substrate-sketch-04* section for how it interacts with the current substrate sketch, including the one point of genuine tension (F1).

**Per topic:**

- [Substrate — sketch 05](substrate-sketch-05.md) — consolidated substrate, aligned with architecture-sketch-01. Retires F1 (emotion/tension as parallel projection); adds M1 (adverbial/modal routing rule); makes event type an extensible categorical tag rather than a dispatch key; applies A3 retroactively to every carried-forward commitment. Current substrate statement; read alone for the substrate's shape.
- [Descriptions — sketch 01](descriptions-sketch-01.md) — the fold-invisible interpretive peer surface to the substrate's typed facts. Commitments D1–D5 (fold-invisibility, attention affordances, anchor-attachment, branch-default-from-anchor, no-auto-promotion). Specifies the description record, kind vocabulary, attention levels, review state with staleness under anchor edits, promotion mechanics via proposal queue, and tooling obligations. Absorbs substrate provenance.
- [Reader-model — sketch 01](reader-model-sketch-01.md) — how human or LLM interpretation of descriptions is invoked, reviewed, and fed back into authorial acts. Commitments R1–R6 (typed I/O, descriptions labeled in the view, partner-not-fallback, shared review-entry type across humans and LLMs, declared-scope invocations, anchor-τ_a staleness). Specifies the ReaderView, invocation modes (interactive, triggered, batch), the typed output shape (reviews, promotion proposals, question-answers), refusal/malformed handling, and the API/firewall boundary between substrate and tooling.

## Upcoming sketches

Planned work. Each is a sketch-to-write; filenames are provisional. Dependency order is approximate — reader-model was originally third but was advanced because the description surface shipped write-only without it.

1. **Inference model** — addresses substrate-sketch-05 open question 2. Realization-as-integration needs a bounded inference layer; the shape (forward chaining, proof-carrying, something else) is open.
2. **Proper focalization semantics** — closes the weakening the prototype flagged. Requires τ_d-scoped reader-state tracking.
3. **Prescriptive / upper-layer sketch** (provisional) — a Dramatica-adjacent layer that sits *above* the substrate and consults its queries. Addresses the "multiple models operating simultaneously" intuition: the substrate grid-snaps low-level structure; this layer would carry scene-level, act-level, or throughline-level prescription. Opens a new topic sibling to substrate and descriptions, related via shared coordinates (τ_s, τ_d, τ_a, entity/branch ids), not inheritance.

The next unit of prototype work is a second reader-model probe iteration once a real LLM-backed tooling layer is in place: exercise the view against a live model, ingest structured reviews, and surface a proposal queue the author can walk.

## Superseded sketches

Kept as historical record of the design's evolution. Do not use as a starting point.

- [Substrate — sketch 01](substrate-sketch-01.md) — initial substrate statement. Too strong on T1 (single ground truth), conflated slot identity with update source for reader vs. character, too narrow on library claim.
- [Substrate — sketch 02](substrate-sketch-02.md) — delta on 01. Revised T1, K2, and library claim, but left fact/state semantics inconsistent across canonical and contested regions, and retained character-centric slot names.
- [Substrate — sketch 03](substrate-sketch-03.md) — first consolidation. Fixed sketch 02's inconsistencies but conflated three branch uses (contested / draft / counterfactual) under one concept, claimed post-contested canonical consistency "by construction" without a mechanism to back it, and used an undeclared epistemic slot in the worked example.
- [Substrate — sketch 04](substrate-sketch-04.md) — second consolidation. Separated branch kinds (contested / draft / counterfactual), parameterized queries by branch, defined fold scope across branches, and simplified event status to two values. Committed to F1 (emotion/tension as parallel projections), which architecture-sketch-01's A3 later ruled out; left event type's role ambiguous; offered no principled routing rule for adverbial/modal content. Superseded by sketch 05.
