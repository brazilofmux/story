# Computational narrative systems

Systems that have attempted to generate, understand, or enforce stories computationally. Entries are survey notes built up over time.

## Index

| Entry | Author / Year | Status |
|-------|---------------|--------|
| [TALE-SPIN](tale-spin.md) | Meehan, 1976 | seeded |
| [MINSTREL](minstrel.md) | Turner, 1992/1994 | seeded |
| [MEXICA](mexica.md) | Pérez y Pérez, 1999 | seeded |
| [Façade](facade.md) | Mateas & Stern, 2005 | seeded |
| [LLM-era overview](llm-era-overview.md) | 2018–2026 | omnibus placeholder |

*(To be added — singly: Universe (Lebowitz); Fabulist (Riedl & Young); Brutus (Bringsjord & Ferrucci); Scheherazade (Li, Riedl et al.); IDtension (Szilas); Comme il Faut / Prom Week (McCoy, Mateas, Wardrip-Fruin); Versu (Evans & Short); Curveship (Montfort); StoryAssembler; Tracery. Planned split-out from the LLM-era overview: Dramatron; DOC; re3; RecurrentGPT; Generative Agents; AI Dungeon.)*

## Cross-cutting notes

### The architectural paradigms seen so far

1. **Simulation.** TALE-SPIN, Generative Agents. Characters with goals, world advances, transcript becomes story. Canonical failure: simulation is not narrative.
2. **Planner + author goals.** MINSTREL (and later Fabulist). Separate layer for authorial intent; case memory + TRAM, or partial-order planning. Handles theme; scales poorly.
3. **Engagement + reflection.** MEXICA. Cognitive-process model; no goals, no planner; emotion/tension substrate drives associative continuation, with critical reflection for coherence and impasse-handling.
4. **Drama manager + authored reactive agents.** Façade. Top-level dramatic arc enforces shape; richly authored characters fill in texture. Existence proof at heavy authorial cost.
5. **LLM pipelines.** Outline → draft → revise, with optional agent layer. Collapses authorial cost of surface but not of architecture.

These are **not** equivalent reformulations of the same idea. They make different claims about what a story *is* and what generating one requires. An engine that intends to cover the space will likely need components of more than one.

### Recurring failure modes across the field

- **Simulation absurdity** (Henry-Ant-drowned-by-gravity). Any system grounding output in a world model generates nonsense where the model has gaps. Visible in TALE-SPIN; re-emerges in Generative Agents.
- **Thematic canned-ness.** Author-goal systems have canned author goals; their stories can only be about what the author-layer already knows to be about.
- **Scale and corpus cost.** Case-based and engagement systems need curated memories. Hand-built corpora don't scale across genres.
- **Surface-quality vs. structure-quality tradeoff.** Pre-LLM systems could build correct structure and render it as awkward prose. LLMs render fluent prose and violate structure subtly. The failure migrated layers.
- **No reader model.** Near-universal. Every system above encodes dramatic effect as authorial annotation rather than modeling a reader's cognitive state. This is the single largest open front.
- **Authorial cost of infrastructure.** Façade's five years for twenty minutes. MEXICA's curated case library. LLM systems collapse per-story cost but the per-engine cost of the surrounding architecture remains high.

### What each system uniquely solves

- **Author/character layer split** — MINSTREL.
- **Emotion/tension as substrate** — MEXICA.
- **Creativity as retrieval + adaptation** — MINSTREL (TRAM); LLM-era retrieval-augmented generation.
- **Impasse as a first-class event** — MEXICA.
- **Theme as executable argument** — Dramatica (theory); Fabulist (partially).
- **Drama management as a real-time authorial layer** — Façade.
- **Beats as scheduling unit** — Façade.
- **Fluent surface generation** — LLM era.
- **Natural-language input, narrowly scoped** — Façade (discourse acts); LLM era (open-ended, with reliability cost).

No single system solves all of these at once. This is one useful framing for what a new engine could do that prior work has not.

### The reader-model gap

Combined with the Sternberg entry in the theories track: no surveyed system implements a reader model. Sternberg's narrative interests (suspense / curiosity / surprise) and Aristotle's anagnorisis both require tracking the reader's knowledge and expectations as an object in the system. This combination — **a substrate of per-agent knowledge states (including the reader), plus authorial operations over reader knowledge** — is the most concrete architectural commitment suggested by the survey so far. It is also almost certainly not enough on its own; but it is the right load-bearing primitive.

## Open questions

- Can simulation, planner-author-goals, engagement-reflection, and drama management be unified — or at least coordinated — within a single engine without one paradigm collapsing into another?
- What is the LLM era's actual architectural contribution, beyond the surface generator? Dramatron and re3 retain explicit structure; open-ended LLM continuation recapitulates TALE-SPIN at a new layer.
- Where is the **reader model**? No surveyed system has a real one. Addressing this appears to be the single highest-leverage open front.
- What is the right representation of a **beat** as a unit, and how does it sit between events and acts?
