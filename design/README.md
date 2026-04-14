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
- [Reader-model — sketch 01](reader-model-sketch-01.md) — how human or LLM interpretation of descriptions is invoked, reviewed, and fed back into authorial acts. Commitments R1–R6 (typed I/O, descriptions labeled in the view, partner-not-fallback, shared review-entry type across humans and LLMs, declared-scope invocations, anchor-τ_a staleness). Specifies the ReaderView, invocation modes (interactive, triggered, batch), the typed output shape (reviews, promotion proposals, question-answers), refusal/malformed handling, and the API/firewall boundary between substrate and tooling. The first prototype probe (substrate.py: `reader_view`, `ingest_review`, `ingest_proposal`; 11 tests in `test_rashomon.py`) exercises the view + review plumbing against the Rashomon encoding.
- [Identity and realization — sketch 01](identity-and-realization-sketch-01.md) — closes one bounded slice of substrate-sketch-05 open question 2 (the inference model): identity as a first-class proposition plus query-time substitution. Commitments I1–I7 (identity as typed Prop, per-fold scoping, query-time substitution with no state mutation, symmetry and transitivity, realization as identity-assertion trigger without held-set rewrite, no identity synthesis, KNOWN-only substitution). Specifies the substitution rule, multi-match resolution (strongest slot wins), agent and world query surfaces (`holds_literal` / `holds` / `holds_all_matches` / `equivalence_classes` / `world_holds`), branch interaction, and the Jocasta anagnorisis worked example. Retires the "realization rewrites held set" workaround in favor of "realization asserts identity; substitution does the rewrite at query time." General forward-chaining / domain-rule inference remains OQ2 for a future sketch.
- [Focalization — sketch 01](focalization-sketch-01.md) — closes the known weakening in `project_reader` (focalizer recorded as metadata only, no semantic effect). Commitments F1–F6 (focalization constrains disclosure slot via `min(author, focalizer)` under KNOWN>BELIEVED>SUSPECTED>GAP; focalization-driven demotion never overrides stronger prior reader state, distinguished from explicit author demotion; reference τ_s is the narrated event's τ_s; omniscient default unchanged; focalizer access is substitution-aware per I3/I7; narrator intrusion and external focalization deferred). Side-steps the "τ_d-scoped reader-state tracking" concern from substrate-04 by writing-rather-than-rewriting: focalization constrains disclosures as they land, never re-visits prior entries' effects. Turns the prototype's "deliberate deferred weakening" into proper semantics without new machinery.

## Upcoming sketches

Planned work. Each is a sketch-to-write; filenames are provisional. Dependency order is approximate; sketches are advanced when a forcing function argues for it (e.g., the descriptions surface shipped write-only, which advanced reader-model; Jocasta's anagnorisis had a clean failure mode, which advanced identity-and-realization; the `project_reader` weakening had a clean forcing function in both encodings, which advanced focalization).

1. **Inference model — general** — the remainder of substrate-sketch-05 OQ2 after identity-and-realization closed the realization slice. Open shape: domain derivation rules (`exposed(X, C) ⇒ child_of(C, X)`), bounded forward chaining, proof carrying, negation. Identity-and-realization deliberately drew a small circle around substitution; this sketch decides whether to widen.
2. **Prescriptive / upper-layer sketch** (provisional) — a Dramatica-adjacent layer that sits *above* the substrate and consults its queries. Gemini's framing (a type-checker / linter over the substrate, not a sibling schema) is probably the right shape: the upper layer is library operators per L1 that run queries like "at τ_d=midpoint, does the protagonist's epistemic state shift from GAP to KNOWN on their fatal flaw?" against narrative templates. No new schema; just expressive enough substrate queries + a template vocabulary.

The next unit of prototype work is a second reader-model probe iteration once a real LLM-backed tooling layer is in place: exercise the view against a live model, ingest structured reviews, and surface a proposal queue the author can walk.

## Superseded sketches

Kept as historical record of the design's evolution. Do not use as a starting point.

- [Substrate — sketch 01](substrate-sketch-01.md) — initial substrate statement. Too strong on T1 (single ground truth), conflated slot identity with update source for reader vs. character, too narrow on library claim.
- [Substrate — sketch 02](substrate-sketch-02.md) — delta on 01. Revised T1, K2, and library claim, but left fact/state semantics inconsistent across canonical and contested regions, and retained character-centric slot names.
- [Substrate — sketch 03](substrate-sketch-03.md) — first consolidation. Fixed sketch 02's inconsistencies but conflated three branch uses (contested / draft / counterfactual) under one concept, claimed post-contested canonical consistency "by construction" without a mechanism to back it, and used an undeclared epistemic slot in the worked example.
- [Substrate — sketch 04](substrate-sketch-04.md) — second consolidation. Separated branch kinds (contested / draft / counterfactual), parameterized queries by branch, defined fold scope across branches, and simplified event status to two values. Committed to F1 (emotion/tension as parallel projections), which architecture-sketch-01's A3 later ruled out; left event type's role ambiguous; offered no principled routing rule for adverbial/modal content. Superseded by sketch 05.
