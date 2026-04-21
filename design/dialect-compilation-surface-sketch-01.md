# Dialect compilation surface — sketch 01 (hard extensions + soft preferences)

**Status:** draft, active
**Date:** 2026-04-21
**Supersedes:** nothing (new arc)
**Extends:** [compilation-sketch-01](compilation-sketch-01.md) (refines CS1's `hints` input; clarifies the input language CS5's ranker reads)
**Frames:** every future per-dialect extension that grows hint/extension fields (Aristotelian, Dramatic, Save-the-Cat, Dramatica-template); the per-dialect sketch following this one is the first concrete instantiation
**Related:** [state-of-play-12](state-of-play-12.md); `project_grid_snap.md` (memory — the architectural principle this sketch instantiates at the dialect↔compiler boundary); `feedback_llm_as_ranker.md` (memory — CS5 commitment this sketch preserves and refines)
**Superseded by:** nothing yet

## Purpose

Name the **two-sided dialect-level surface** that connects each dialect to the compiler from `compilation-sketch-01`:

- **Side 1 — hard structural extensions.** Additional dialect-level constraints the compiler enforces deterministically. Flow through pipeline stages 1–3.
- **Side 2 — soft preference annotations.** Dialect-level preference statements the LLM ranker reads at stage 4. Bypass stages 1–3 entirely.

Within each side, every dialect grows its own taxonomy of *flavors* (cardinality, locality, audience-knowledge, texture, pacing, …). This sketch commits to the two-sided shape, the flow constraints, and the cross-cutting design discipline. **It does not commit to per-dialect flavors** — those fall out from the next per-dialect sketch.

This is a **framing sketch** in the same sense as `compilation-sketch-01`: it commits to the *surface shape*, not the per-flavor algorithms.

## Why now

Conversational origin, 2026-04-21 (immediately after `compilation-sketch-01` committed the four-stage pipeline). The arc:

1. User: "We need to focus now on the compilation. We may need to add hints at the dialect level. This is as close as I have ever felt to being to more-or-less generate well-structured stories."
2. First-pass response surfaced four candidate shapes for dialect-level hints (texture/tone, soft co-presence, compiler-objective, generation-shape pinning).
3. User clarified the architectural cut: **two sides, with multiple flavors per side.** Side 1 is hard constraints the compiler understands; side 2 is soft hints the LLM ranker reads. "Since everything else has the same two sides" — the user notes the recurring pattern (Tier-1/Tier-2 validation, verifier/probe, substrate/dialect, grid-snap structural/LLM-affective).
4. User: "Let's sketch abstractly first."

The two-sided cut maps onto CS5 (`feedback_llm_as_ranker.md`) without distortion. Side 1 stays in the deterministic compiler; side 2 lives where the LLM already lives. The grid-snap line (`project_grid_snap.md`) drops naturally between them. Capturing the shape in a durable artifact before per-dialect work begins is straight context-economy discipline.

## Scope — what this sketch does and doesn't do

**In scope:**
- Two-sided cut at the dialect surface (DCS1).
- Pipeline-flow commitments (DCS2 — side 1 through stages 1–3, side 2 to stage 4 only).
- Verifier-coverage bisection (DCS3 — side 1 Tier-2-checkable, side 2 not).
- Optionality (DCS4 — every flavor optional per dialect, per record).
- Dialect-locality of flavor taxonomies as the conservative default (DCS5).
- Refinement of `compilation-sketch-01` CS1's loose `hints` compile-time input (DCS6).
- Open questions per axis with named forcing functions.

**Out of scope:**
- Per-dialect flavor catalogs (worked first concretely on Aristotelian in the next sketch; abstraction reverified after).
- Ranker scoring algorithm (still `compilation-sketch-01` OQ4).
- The full hard-vs-soft constraint discipline (still `compilation-sketch-01` OQ5; this sketch refines part of it but doesn't close it).
- Author UX for filling in the surface (markdown parser arc — `project_longterm_roadmap.md`).
- Whether the existing dialect schemas need restructuring to accommodate the new surface (anticipated to be additive only, but verified per dialect).
- Specific JSON Schema shapes for the new fields (Tier-1 cross-boundary work follows the per-dialect sketch).

## Commitments

Labels **DCS1..DCS6** commit to structural shape; **DOQ1..DOQ7** bank open questions with forcing criteria.

### DCS1 — Two-sided dialect surface

The dialect grows two architecturally distinct surfaces, both expressed as optional fields on dialect records:

- **Side 1 — hard structural extensions.** Fields whose value is mechanically interpretable: integers, enums, references, structured constraints. Their semantics are *enforcement* — the compiler treats them as additional constraints alongside the existing dialect-structural fields.
- **Side 2 — soft preference annotations.** Fields whose value is interpreted by the LLM ranker: controlled-vocabulary tokens, free-text rubrics, ranked-list preferences. Their semantics are *guidance* — the ranker reads them to score candidates from stage 3's solution space.

Both surfaces share the dialect schema. They differ in three architectural ways: who reads them (compiler vs ranker), where in the pipeline they bind (stages 1–3 vs stage 4), and whether they're verifier-checkable (Tier-2 vs not).

**Naming discipline.** Calling side 1 a "hint" is a category error — side 1 *is* a constraint, just one expressed at the dialect level rather than at compile-time input. Internal vocabulary: side 1 = **extensions**, side 2 = **preferences**. The user's conversational "hints at the dialect level" frame refers to the *combined* surface; this sketch splits the term.

### DCS2 — Pipeline flow

- **Side 1 → stage 1 → stages 2–3.** Stage 1 (constraint extraction) consumes side-1 extensions alongside the existing structural dialect fields and folds them into the constraint graph. Stage 2 (feasibility check) accounts for them in arithmetic/consistency. Stage 3 (planner) treats them as preconditions/effects/pinning constraints. Stage 4 may *also* read them, but only for ranker context — not for filtering.
- **Side 2 → bypass stages 1–3 → stage 4.** Side-2 preferences do not affect feasibility or solution-space cardinality. They are *aggregated forward* — gathered from all dialect records during stage 1 (cheap walk) and passed as ranker input to stage 4.

**Consequence.** Side-2 preferences cannot make a previously-feasible compilation infeasible. They cannot prune the solution space. They only re-rank within it. This preserves CS5 (LLM doesn't generate or mutate; only ranks) and CS6 (infeasibility is loud, and only side 1 can produce it).

### DCS3 — Verifier coverage bisection

- **Side 1 is Tier-2-checkable.** Hard extensions admit referential integrity, range, cardinality, and consistency checks under the existing audit infrastructure. Side-1 fields may also participate in dialect-specific verifier check families (the A7.x analog for whichever dialect grows them). Side 1 is part of the "compiler's type-check" (CS7).
- **Side 2 is not mechanically verifiable, by construction.** "Phase X should feel claustrophobic" admits no boolean check. "Prefer adjacency of peripeteia and anagnorisis" is a preference that admits multiple satisfying outputs by design.

This is the **grid-snap line drawn at exactly the right place.** Per `project_grid_snap.md`: structural facts grid-snap into machine-checkable form; affective/interpretive load is LLM-carried. Side 1 is the dialect's contribution to grid-snap; side 2 is the dialect's contribution to LLM load.

Tier-2 audits get *new check families* covering side 1 per dialect; Tier-2 does not gain check families for side 2. The probe (reader model) MAY review side 2 — see DOQ7.

### DCS4 — Optionality

Every flavor on either side is **optional**. Empty side-1 fields produce no additional constraints (compiler behaves as if the field weren't present). Empty side-2 fields produce neutral ranker behavior (DOQ5 banks the specific neutrality semantics).

A dialect MAY:
- Grow only side-1 flavors (e.g., a structurally-tight dialect with no texture vocabulary).
- Grow only side-2 flavors (e.g., a structurally-permissive dialect that wants to guide ranker behavior heavily).
- Grow neither (the existing dialect surface remains; compilation works on the existing constraints alone).
- Grow both, asymmetrically, per record kind.

**Pre-existing dialect encodings remain valid.** The four current Aristotelian encodings (Oedipus, Rashomon, Macbeth, Hamlet) verify identically before and after their dialect grows extension/preference fields, provided the new fields are optional and default-empty. Extension-only — no breaking change.

### DCS5 — Dialect-local flavor taxonomies (conservative default)

Each dialect defines its own catalog of flavors on each side. There is **no global preference vocabulary** by default. The Aristotelian dialect's side-2 vocabulary is consumed by the Aristotelian ranker; the Save-the-Cat dialect's side-2 vocabulary is consumed by the Save-the-Cat ranker. They may overlap in human-readable terms ("tragic", "ironic") but they do not share a schema.

**Why dialect-local.** Mirrors the existing dialect-locality of structural semantics: an Aristotelian phase has no Save-the-Cat-beat equivalent at the schema level; preference vocabularies inherit the same locality.

**Cross-dialect symmetry MAY emerge** as multiple dialects grow their surfaces — DOQ2 banks the question of when (if ever) to globalize a flavor.

### DCS6 — Subsumes `compilation-sketch-01` CS1 `hints` input

`compilation-sketch-01` CS1 lists the compiler input as `(dialect_constraints, word_budget, hints, rng_seed)` where `hints` is a loose bag of "timeline-ordering hints, location-co-presence hints, pacing hints." Under DCS1, those decompose:

- Timeline-ordering, location-co-presence, audience-knowledge timing → side 1 (hard extensions per the relevant dialect).
- Pacing, tonal, ranker-objective preferences → side 2 (preference annotations per the relevant dialect).

The compile-time `hints` slot is **refined to a dialect-overlay**: the author submits a partial dialect record carrying values for extension/preference fields, and the compiler merges this overlay onto the canonical dialect record before stage 1. The schema for the overlay IS the dialect's own surface — there is no separate "hints schema."

DOQ3 banks the schema-shape choice for the overlay (full-record vs side-2-only vs no-overlay).

**Concrete refinement to CS1:** `hints: optional dialect-overlay records`. Loose `hints` bag is removed. Compile-time author input that doesn't fit the dialect surface is by definition outside the compiler's input language and must be encoded into the dialect first.

## Open questions — banked for follow-on sketches

### DOQ1 — Flavor catalog per side

What flavor categories are canonical within each side? Hypotheses (not commitments):

**Side 1 (hard extensions):**
- Structural cardinality (e.g., phase event-count floor/ceiling).
- Co-presence / locality (hard form: "events X and Y must share location"; "character C must be present at events {E_i}").
- Audience-knowledge timing (e.g., "secret S must be known to audience by τ_s ≤ N"; "dramatic-irony window must overlap event E").
- Pinning extensions (e.g., specific event must occur in specific phase; specific event must precede/follow another by ≤N steps).
- Communication-channel availability (e.g., "communication channel C is available throughout phase P" — affects CS3 STRIPS preconditions for remote-action events).

**Side 2 (soft preferences):**
- Texture/tone (e.g., "claustrophobic", "ironic", "elegiac" from a dialect-local controlled vocabulary).
- Pacing (e.g., "rapid escalation in third phase", "slow burn in first phase").
- Co-presence preference (soft form of side 1's hard co-presence; admits multiple satisfying substrates with different scores).
- Ranker-objective preferences (e.g., "prefer near-binding of peripeteia and anagnorisis", "prefer co-located catharsis", "prefer multi-character witness to peripeteia").
- Negative preferences (e.g., "avoid coincident peripeteia and anagnorisis even though admissible").
- Density preferences (e.g., "prefer dense final phase even at the cost of sparse middle phase").

**Forcing function:** the next per-dialect sketch (likely Aristotelian, given precedent) attempts to grow 2–3 side-1 and 2–3 side-2 flavors. The catalog falls out from the worked example. After the second dialect's worked example, the catalog stabilizes or DOQ2 fires.

### DOQ2 — Cross-dialect symmetry

Should some flavor categories be globally consistent across dialects? Tradeoffs:

- **Cross-dialect symmetry** helps multi-dialect stories share a ranker; helps authors who think across dialects; opens possibility of a "global preference vocabulary" (e.g., a tonal vocabulary shared across all narrative dialects).
- **Dialect-locality** preserves dialect-specific semantics that don't translate; matches the existing dialect-locality of structural fields; keeps each dialect independently authorable.

DCS5 commits to dialect-local as the conservative default. DOQ2 reopens it after evidence: when ≥2 dialects grow their surfaces, do their vocabularies overlap enough to globalize?

**Forcing function:** second dialect grows its surface. Symmetry visible iff vocabularies overlap on at least one axis.

### DOQ3 — Compile-time overlay schema (per DCS6)

Three options for what an author can submit at compile time:

- **(a) Full-record overlay.** Author submits a partial dialect record with any subset of extension/preference fields populated; compiler merges field-by-field. Most expressive; biggest blast radius for typos.
- **(b) Side-2-only overlay.** Overlay restricted to preference fields (side 2); hard extensions cannot be mutated at compile time. Forces hard constraints to live in the canonical dialect record. Tighter but less flexible.
- **(c) No overlay.** Preferences are dialect-record-internal only; no per-compilation overrides. Author re-edits the dialect record per compilation. Simplest; least author ergonomic.

**Forcing function:** first author-facing input attempt (markdown parser arc upstream of compiler — `project_longterm_roadmap.md` item 1). Choice may be dialect-local — different dialects may pick differently — though uniformity is desirable.

### DOQ4 — Conflict resolution within a side

If two side-1 hard extensions conflict (e.g., "phase must contain ≥5 events" + "phase must contain exactly 3 events"):

- **Verification error preferred** when conflict is single-record / single-dialect — fail at Tier-2 audit before compilation begins.
- **Compiler error (CS6)** when conflict is cross-record and only visible at constraint extraction.

If two side-2 preferences conflict, the ranker resolves via scoring (no error). Preference contradiction is admissible by definition; the ranker produces the best-compromise candidate and the score reflects the unresolved tension.

**Forcing function:** first encoded conflict (likely emerges as a side-effect of OQ4 work or first per-dialect surface extension).

### DOQ5 — Empty side-2 ranker behavior

When all side-2 fields on the relevant dialect records are empty, the ranker has no preference signal. Behavior options:

- **Uniform-random selection from the solution space** (deterministic given seed).
- **Heuristic baseline** — per-dialect default scoring (e.g., Aristotelian default favors near-binding without explicit preference).
- **Arbitrary-valid selection** — first valid candidate in deterministic enumeration order.

**Forcing function:** first stage-4 implementation. Choice ties to OQ4 (impact objective): if the impact objective has a defensible default-zero baseline, that becomes the empty-side-2 behavior.

### DOQ6 — Lowering interaction

`Lowering` records annotate the substrate↔dialect grounding relation per `lowering-sketch-01` and `-02`. Interaction with the new surface:

- **Side 1 may add new constraints requiring new Lowering kinds.** E.g., if "audience-knowledge timing" becomes a side-1 flavor, the substrate may need explicit epistemic-state entries (currently captured partially via `Held` records); those need Lowering coverage. May extend OQ1 (state representation) from `compilation-sketch-01`.
- **Side 2 does not need new Lowering kinds.** Preferences don't generate substrate; they re-rank existing substrate. No grounding relation to annotate.

**Forcing function:** first side-1 flavor that requires substrate effects beyond what existing substrate records can express.

### DOQ7 — Probe access to side-2 fields

The probe (reader model client) currently walks specific reviewable fields per dialect — Aristotelian probe-sketch-04 reviews 5 record kinds × specific fields each (action_summary, hamartia_text, phase annotations, chain-step annotations, arc-relation annotations). Side-2 preference fields ARE LLM-readable by the ranker — does the probe also surface them for review?

Three positions:

- **(a) Probe reads side-2.** Probe interprets preferences in its annotation reviews; can surface preference-vs-substrate consistency observations.
- **(b) Probe ignores side-2.** Strict separation: probe reviews dialect-structural correctness only; ranker reads preferences; no overlap.
- **(c) Probe reads side-2 but only as context.** Probe sees preferences but does not surface them as reviewable; preferences inform interpretation without becoming probe targets.

**Forcing function:** first per-dialect surface extension creates the probe-relevant decision. Dialect-local is admissible — probe behavior may differ per dialect.

## Concrete next arcs (candidates)

This sketch is abstract by design — concrete catalog falls out from the per-dialect application.

1. **First per-dialect surface — Aristotelian.** Apply this sketch to the Aristotelian dialect: grow 2–3 side-1 flavors and 2–3 side-2 flavors. Verify the abstraction holds; surface DOQ1 candidates. Likely sketch name: `dialect-compilation-surface-sketch-02-aristotelian` or `aristotelian-sketch-04` (the latter if the work fits within Aristotelian's existing arc numbering).
2. **Second per-dialect surface — Save-the-Cat or Dramatic.** Forces DOQ2 (cross-dialect symmetry) to fire. Reveals whether flavor vocabularies want to globalize.
3. **`compilation-sketch-02` (or amendment to -01).** Commit DCS6 — `hints` compile-time input subsumed by dialect-overlay. Possibly bundled with stage-1 or stage-2 implementation work.
4. **Tier-1 cross-boundary work for the new fields.** PFS-N for each dialect's surface extension, following PFS13's pattern (additive-only schema amendments).

Per `feedback_research_production_alternation.md`, the natural sequence is design-first this sketch (done by writing it) → per-dialect application (production track on Aristotelian) → re-examine this sketch (research track) for amendment or sketch-02. Probes between stages remain unchanged.

## Relationship to prior commitments

| Prior | Refined by this sketch | How |
|---|---|---|
| `compilation-sketch-01` CS1 | DCS6 | `hints` compile-time input → dialect-overlay |
| `compilation-sketch-01` CS5 | DCS2 | Side 2 IS the ranker's input language; CS5's "ranker is swappable" becomes "any ranker implementing the dialect's preference DSL is admissible" |
| `compilation-sketch-01` CS6 | DCS2 | Only side 1 can produce infeasibility; side 2 cannot |
| `compilation-sketch-01` CS7 | DCS3 | Side 1 extends the existing verifier "type-check"; side 2 is outside the type-check by construction |
| `compilation-sketch-01` OQ5 (hard vs soft) | DCS1, partially | The two-sided cut answers the *where they live* axis; the *how to weight* axis remains open |
| `project_grid_snap.md` (memory) | DCS1, DCS3 | Grid-snap line drawn at side-1/side-2 boundary at the dialect level |

## What a cold-start Claude should read first

1. `compilation-sketch-01.md` — CS1 (input/output) and CS5 (LLM-as-ranker) for the architecture this sketch refines.
2. This sketch.
3. `project_grid_snap.md` (memory) — the architectural principle this sketch instantiates.
4. `feedback_llm_as_ranker.md` (memory) — CS5 commitment this sketch preserves.
5. (when it exists) The first per-dialect application of this surface — concrete instantiation that makes DCS1's vocabulary land.
6. `state-of-play-12.md` — current corpus and dialect status to ground "which dialects might grow surfaces first."

## Honest framing

This sketch is **pure architecture**. It commits to a shape that admits future flavor catalogs without prejudging them. It does not by itself increase what the engine can do. Its value is downstream: it establishes the surface every per-dialect extension can grow into without re-deciding the architecture each time.

The user's conversational frame — "as close as I have ever felt to being to more-or-less generate well-structured stories" — is the motivating energy, not the deliverable. The deliverable is a clean two-sided surface that preserves CS5, instantiates grid-snap at the dialect↔compiler boundary, and unblocks per-dialect flavor work without locking in any specific flavor.

Per `project_solution_horizon.md`: this sketch is a **strong input** either way. If this engine grows the surfaces and implements the compiler, the surfaces are ready. If a future more-capable AI does it, it inherits the surface shape, the verifier-coverage bisection, and the pipeline-flow commitments — not just the four-stage pipeline naming, but the dialect-side language the pipeline binds to.
