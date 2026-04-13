# LLM-Era Story Generation (consolidated overview)

## One-line summary

A single survey entry, intended to be split later, covering narrative generation systems built on large language models from ~2019 through 2026 — characterized by a step-change in *surface* quality (prose fluency) and by recapitulating prior eras' *structural* failures at a new layer, with a few systems making serious architectural contributions and the rest being variants of prompt scaffolding around a base model.

## Scope

Placeholder / omnibus entry. Each system below merits its own deepened entry once we have read primary sources. The purpose of this consolidation is to situate the current state of the field before descending.

## Representative systems, grouped by architectural contribution

### Outline-then-expand pipelines

- **Plan-and-Write** (Yao, Peng, Weston, Knight, et al., 2019). Two-stage: generate a title + storyline (ordered events), then expand each event into prose. Demonstrates that explicit intermediate structure reduces incoherence relative to end-to-end generation.
- **Hierarchical Neural Story Generation** (Fan, Lewis, Dauphin, 2018). Premise → story expansion; convolutional seq2seq; pre-LLM but methodologically ancestral.
- **DOC / Detailed Outline Control** (Yang, Klein, Peng, Tian, et al., 2022). Generate a detailed outline with character descriptions, then generate prose paragraph-by-paragraph under outline constraints. Preserves long-range coherence better than single-pass generation.
- **Dramatron** (Mirowski, Mathewson, Pittman, Evans, 2023). Hierarchical decomposition from log-line → title → characters → plot → location descriptions → scene-level dialogue. Targets screenplays/stage scripts. Deliberately uses three-act structure as scaffold. Coauthored with theater practitioners; one of the few systems evaluated in actual staged production.

### Drafting + revision / recursive reprompting

- **re3 / Recursive Reprompting and Revision** (Yang, Klein, Peng, Tian, 2022). Three-stage: plan, draft, revise. Revision pass catches plot inconsistencies and character contradictions the draft pass introduces. Structurally similar to MEXICA's engagement/reflection, at LLM scale.
- **RecurrentGPT** (Zhou, Jiang, Cui, et al., 2023). Maintains a long-term memory summary and a short-term context, iteratively extending the story. Addresses the context-window constraint that otherwise caps coherence at ~a few thousand tokens.

### Agent-based narrative

- **Generative Agents** (Park, O'Brien, Cai, Morris, Liang, Bernstein, 2023). Town of simulated agents with memory streams, reflection, and planning — not strictly a story generator, but produces emergent narratives readers can follow. TALE-SPIN reborn with LLMs; interesting precisely because it inherits TALE-SPIN's failure mode (simulation ≠ narrative) at a new fluency level.
- **Various 2024–2026 agent-based drama systems.** Multiple groups have built drama-manager-plus-LLM-characters systems that echo Façade with generative surface. Open question: do they scale authoring or just move the cost around.

### Human-in-the-loop / co-writing

- **Wordcraft** (Coenen, Davis, Ippolito, Reif, Yuan, 2021) and related Google efforts. Co-writing interfaces rather than autonomous generators. Architecturally minimal; valuable for what they reveal about where humans want AI to insert creative contribution.
- **Sudowrite, NovelAI, various commercial tools (2021–present).** Productized co-writing. Not research systems per se but instructive for what scale-of-use teaches about failure modes.

### Interactive fiction / game-style

- **AI Dungeon** (Walton, 2019) and descendants. Open-ended text adventure with an LLM DM. Demonstrated LLM's capacity for surprise and fluency in an interactive setting and its weakness at memory, consistency, and dramatic shape. A public-scale experiment of enormous value for understanding what breaks.
- **Various agent-based TTRPG / interactive drama systems, 2023–2026.** Some combining Façade-style drama management with LLM surface.

### Research platforms

- **Storium / Story-platform corpora** (Akoury, Wang, Whiting, et al., 2020). Large annotated datasets of human-authored collaborative stories, used to benchmark generation systems.

## Cross-cutting observations

### What LLMs changed

- **Surface quality.** The prose-quality ceiling moved dramatically. Many pre-LLM systems produced structurally sound but awkward prose; LLMs produce fluent prose — with varying quality of structure underneath.
- **Default content availability.** Description, dialogue, proper-noun coverage, genre pastiche, and voice are cheap. Where pre-LLM systems had to specify, LLMs fill in.
- **Failure mode migration.** Characteristic failures moved from "grammatically awkward" and "obvious template" to "surface-coherent but wrong" — internal contradictions, character drift, plot holes that read smoothly past.

### What LLMs did not change

- **Structure still needs explicit support.** Systems with outlines, plans, drama managers, or reflection loops beat systems without them on long-range coherence. This matches the pre-LLM era's findings.
- **Author intent is still not generated.** LLMs will happily continue a story in any direction. Without a specification of what the story is *about*, drift is certain.
- **Reader model is still absent.** As in the pre-LLM era. Sternberg-style interests are not being tracked or optimized by any surveyed system.
- **Evaluation is still hard.** "Is this story good?" remains under-operationalized; most evaluations are either automated proxies (perplexity, BERTScore) or human ratings (expensive, noisy, genre-inflected).

### Failure modes characteristic of LLM-era systems

- **Smooth wrongness.** Prose reads fluently while characters forget motivations, timelines contradict, rules break. The TALE-SPIN drowning-ant is now the character who was introduced as deceased on page 30 and reappears on page 80 with no explanation.
- **Convergence to the mean.** Without strong authorial specification, outputs gravitate toward generic patterns in the training distribution — suburban American domestic drama, fantasy-quest monomyth, airport-thriller beats.
- **Shallow character.** Characters' interiority is often a consistent voice rather than a consistent psychology; the distinction becomes visible over longer works.
- **Context-window clifflessness.** Beyond the window, the model has no access unless retrieval or summarization scaffolding is provided; this scaffolding is where architectural differences matter.

### What is genuinely new

- **Viable surface generation as a commodity.** For the first time, the surface layer can be taken as roughly-solved (for English prose of moderate ambition) and attention can move to the harder layers above it.
- **Retrieval-augmented creativity.** LLMs + vector retrieval over large corpora approximate MINSTREL's case-based generation at much larger scale.
- **Low authorial cost per run.** Façade was five years for twenty minutes. An LLM can produce a comparable-surface short story in seconds. The *authorial cost of the infrastructure* remains high; the *per-story cost* collapses.
- **Genuine NLU for player/reader input.** The Façade-style narrow-discourse-act parser is replaced by meaningfully open natural language comprehension — at the cost of reliability and introspectability.

## Lessons for an engine

1. **Treat the LLM as the surface generator and a general-purpose case-adapter, not as the story engine.** The pre-LLM lessons (author layer, drama manager, reflection, reader model, event log with knowledge projections) all remain load-bearing. The LLM is the newest tool, not a replacement for the architecture.
2. **The failure modes migrated, they did not disappear.** A system that ignores MINSTREL and MEXICA because it has GPT-class models will reproduce their failures with better prose.
3. **Structure must be represented outside the LLM.** The event log, character state, reader model, and drama beats belong in an explicit data model that the LLM reads from and writes to under constraint. Any structure that lives only in the prompt disappears when the prompt rolls off the context window.
4. **This is the era the engine is being built in.** Decisions about how deeply to integrate LLMs, and where to hold the line on explicit representation, are *this engine's* central architectural choices. Not a future-compatibility concern — a present one.

## Sources

A partial primary-source list to split into per-entry references when this survey splits:

- Fan, A., Lewis, M., Dauphin, Y. "Hierarchical Neural Story Generation." *ACL* 2018. **[Primary — not yet read.]**
- Yao, L., Peng, N., Weischedel, R., Knight, K., Zhao, D., Yan, R. "Plan-and-Write: Towards Better Automatic Storytelling." *AAAI* 2019. **[Primary — not yet read.]**
- Yang, K., Klein, D., Peng, N., Tian, Y. "DOC: Improving Long Story Coherence With Detailed Outline Control." *ACL* 2023. **[Primary — not yet read.]**
- Yang, K., Tian, Y., Peng, N., Klein, D. "Re3: Generating Longer Stories With Recursive Reprompting and Revision." *EMNLP* 2022. **[Primary — not yet read.]**
- Mirowski, P., Mathewson, K., Pittman, J., Evans, R. "Co-Writing Screenplays and Theatre Scripts with Language Models." *CHI* 2023. **[Dramatron. Primary — not yet read.]**
- Park, J. S., O'Brien, J., Cai, C. J., Morris, M. R., Liang, P., Bernstein, M. S. "Generative Agents: Interactive Simulacra of Human Behavior." *UIST* 2023. **[Primary — not yet read.]**
- Zhou, W., Jiang, Y. E., et al. "RecurrentGPT: Interactive Generation of (Arbitrarily) Long Text." 2023. **[Primary — not yet read.]**
- Akoury, N., Wang, S., Whiting, J., Hood, S., Peng, N., Iyyer, M. "STORIUM: A Dataset and Evaluation Platform for Machine-in-the-Loop Story Generation." *EMNLP* 2020. **[Primary — not yet read.]**

*All claims above should be treated as tentative summaries until primary sources are consulted. The field moves fast; specific technical claims about individual systems are the most likely to be out of date or misremembered.*
