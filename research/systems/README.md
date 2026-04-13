# Computational narrative systems

Systems that have attempted to generate, understand, or enforce stories computationally. Entries are survey notes built up over time.

## Index

| Entry | Author / Year | Status |
|-------|---------------|--------|
| [TALE-SPIN](tale-spin.md) | Meehan, 1976 | seeded |
| [MINSTREL](minstrel.md) | Turner, 1992/1994 | seeded |
| [MEXICA](mexica.md) | Pérez y Pérez, 1999 | seeded |

*(To be added: Universe (Lebowitz); Joseph (Lang); Fabulist (Riedl & Young); Brutus (Bringsjord & Ferrucci); Scheherazade (Li, Riedl et al.); Façade (Mateas & Stern); IDtension (Szilas); Comme il Faut / Prom Week (McCoy, Mateas, Wardrip-Fruin); Versu (Evans & Short); Curveship (Montfort); StoryAssembler; Tracery; GPT-era work — Plan-and-Write (Yao et al.); Dramatron (Mirowski et al.); DOC (Yang et al.); re3; RecurrentGPT; agent-based narrative systems circa 2023–2026; AI Dungeon and descendants as a separate branch.)*

## Cross-cutting notes

### The three architectural paradigms seen so far

1. **Simulation.** TALE-SPIN. Characters with goals, world advances, transcript becomes story. Canonical failure: simulation is not narrative.
2. **Planner + author goals.** MINSTREL (and later Fabulist). Separate layer for authorial intent; case memory + TRAM, or partial-order planning. Handles theme; scales poorly.
3. **Engagement + reflection.** MEXICA. Cognitive-process model; no goals, no planner; emotion/tension substrate drives associative continuation, with critical reflection for coherence and impasse-handling.

These are **not** equivalent reformulations of the same idea. They make different claims about what a story *is* and what generating one requires. An engine that intends to cover the space will likely need components of more than one.

### Recurring failure modes across the field

- **Simulation absurdity** (the Henry-Ant-drowned-by-gravity class). Any system that grounds output in a world model will generate nonsense where the model has gaps.
- **Thematic canned-ness.** Author-goal systems have canned author goals; their stories can only be about what the author-layer already knows to be about.
- **Scale and corpus cost.** Case-based and engagement systems need curated memories. Hand-built corpora do not scale genres.
- **Surface-quality vs. structure-quality tradeoff.** Pre-LLM systems could build correct structure and render it as awkward prose. LLMs can render fluent prose and violate structure subtly. The failure migrated layers.
- **No reader model.** Almost universal. Every system above encodes dramatic effect as authorial annotation rather than simulating a reader's cognitive state.

### Recurring solved-by-one-system gaps

- **Author/character layer split** — MINSTREL solves.
- **Emotion/tension as substrate** — MEXICA solves.
- **Creativity as retrieval + adaptation** — MINSTREL (TRAM) solves.
- **Impasse as a first-class event** — MEXICA solves.
- **Theme as executable argument** — Dramatica (theory) and Fabulist (partially) attempt.

No single system solves all of these at once. This is one useful framing for what an engine could do that prior work has not.

## Open questions

- Can simulation, planner-author-goals, and engagement-reflection be unified — or at least coordinated — within a single engine without one paradigm collapsing into another?
- What is the LLM era's actual architectural contribution, beyond the surface generator? Some work (Dramatron, re3, agent systems) retains explicit structure; other work (open-ended LLM story continuation) reruns TALE-SPIN at a new layer.
- Where is the **reader model** in any of this? No surveyed system has a real one. This may be the single largest open front.
