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

## Upcoming sketches

Planned work, in dependency order. Each is a sketch-to-write; filenames are provisional.

1. **Descriptions surface** — *descriptions-sketch-01.md.* Formalizes architecture-sketch-01 A2 and A4. Specifies the description record (kind, attention, review state, attached_to), the promotion rule's operational shape, and tooling obligations. Absorbs and widens the current `provenance` convention. Substrate-sketch-05 defers the description record's shape to this sketch.
2. **Inference model** — addresses substrate-sketch-05 open question 2. Realization-as-integration needs a bounded inference layer; the shape (forward chaining, proof-carrying, something else) is open.
3. **Proper focalization semantics** — closes the weakening the prototype flagged. Requires τ_d-scoped reader-state tracking.
4. **Reader-model integration** — how LLM/human interpretation of descriptions is invoked, cached, reviewed, and integrated with structural queries. Architecture-sketch-01 A5 says this work is in scope; the shape of the integration is open.

After descriptions-sketch-01 lands, the prototype iterates: the Rashomon encoding refactor per substrate-sketch-05's worked example, `provenance` absorbed into the description surface, and tests updated to pin description-attachment invariants. That is the next unit of prototype work.

## Superseded sketches

Kept as historical record of the design's evolution. Do not use as a starting point.

- [Substrate — sketch 01](substrate-sketch-01.md) — initial substrate statement. Too strong on T1 (single ground truth), conflated slot identity with update source for reader vs. character, too narrow on library claim.
- [Substrate — sketch 02](substrate-sketch-02.md) — delta on 01. Revised T1, K2, and library claim, but left fact/state semantics inconsistent across canonical and contested regions, and retained character-centric slot names.
- [Substrate — sketch 03](substrate-sketch-03.md) — first consolidation. Fixed sketch 02's inconsistencies but conflated three branch uses (contested / draft / counterfactual) under one concept, claimed post-contested canonical consistency "by construction" without a mechanism to back it, and used an undeclared epistemic slot in the worked example.
- [Substrate — sketch 04](substrate-sketch-04.md) — second consolidation. Separated branch kinds (contested / draft / counterfactual), parameterized queries by branch, defined fold scope across branches, and simplified event status to two values. Committed to F1 (emotion/tension as parallel projections), which architecture-sketch-01's A3 later ruled out; left event type's role ambiguous; offered no principled routing rule for adverbial/modal content. Superseded by sketch 05.
