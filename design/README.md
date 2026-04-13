# Design

Architectural sketches and design notes for the story-telling engine. Each sketch is numbered and dated; revisions do not overwrite predecessors. Old sketches are left in place as a record of how the design changed, so the reasoning over time is preserved.

## Convention

- Files named `{topic}-sketch-NN.md` where NN is sequential per topic.
- Every sketch has a **Status** (*draft, active*, *superseded*, *abandoned*) and a **Date** at the top.
- **Active sketches are self-contained.** A reader should be able to understand the current design from the active sketch alone, without chasing a chain of deltas. When corrections pile up, consolidate into a new sketch rather than let the active starting point depend on superseded context.
- When a sketch is superseded, its status is updated and a link to the successor is added — but the file stays.
- Sketches are not specifications. They are the design thinking in progress. Claims and commitments may be wrong. Open questions are first-class.

## Active sketches

These are the sketches to read. Each is self-contained; no need to chase predecessors unless you want the history.

- [Substrate — sketch 04](substrate-sketch-04.md) — the event-log + per-agent-knowledge-projection substrate, with contested-fabula support for ambiguous fiction, source-agnostic epistemic slots, disjoint diegetic/narrative update operators, and explicit branch kinds (contested / draft / counterfactual).

## Superseded sketches

Kept as historical record of the design's evolution. Do not use as a starting point.

- [Substrate — sketch 01](substrate-sketch-01.md) — initial substrate statement. Too strong on T1 (single ground truth), conflated slot identity with update source for reader vs. character, too narrow on library claim.
- [Substrate — sketch 02](substrate-sketch-02.md) — delta on 01. Revised T1, K2, and library claim, but left fact/state semantics inconsistent across canonical and contested regions, and retained character-centric slot names.
- [Substrate — sketch 03](substrate-sketch-03.md) — first consolidation. Fixed sketch 02's inconsistencies but conflated three branch uses (contested / draft / counterfactual) under one concept, claimed post-contested canonical consistency "by construction" without a mechanism to back it, and used an undeclared epistemic slot in the worked example.
