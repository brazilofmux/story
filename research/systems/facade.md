# Façade

## One-line summary

One-act interactive drama (released 2005) in which the player, as a dinner guest, witnesses and intervenes in the collapse of Trip and Grace's marriage; built on a purpose-designed drama-management architecture with per-beat dramatic goals, reactive character agents expressed in a custom language (ABL), and natural-language input parsing — a five-year research project that remains the landmark reference for AI-driven interactive narrative and a careful counter-example to the "story generator" framing.

## Origin

Michael Mateas (PhD, Carnegie Mellon, 2002; *Interactive Drama, Art and Artificial Intelligence*) and Andrew Stern (independent AI/interactive researcher, co-designer of *Petz*). Begun ~2000, public release July 2005 as a free download. Continued discussion and retrospectives from Mateas (now at UC Santa Cruz, Expressive Intelligence Studio) and Stern through the 2010s.

## Goal

Build a real work of interactive drama — not a story generator, not a branching game, not a chatbot — demonstrating that an AI-driven dramatic experience with character complexity and dramatic shape is *possible*. Explicitly positioned as an **existence proof** for a medium, not a scalable framework. Mateas's dissertation is equally important as the theoretical statement: interactive drama as a genre between game and film with its own architectural requirements.

## Architecture

Façade's architecture is the most thoroughly worked interactive-drama system to date.

- **Dramatic beats** as the primary unit of narrative. Each beat is a small, roughly 30-second to 2-minute chunk of interaction with its own dramatic function (e.g. "Grace reveals her resentment about the apartment," "Trip pushes Player to take sides on redecoration"). Façade contained on the order of ~25 beats, each authored at length.
- **Beat library.** Beats have preconditions (dramatic and world-state), entry conditions, exit conditions, and dramatic-value annotations (tension level, thematic relevance).
- **Drama Manager.** A top-level process that selects the next beat to play based on the current dramatic arc, player behavior, and tension trajectory. Implements an **Aristotelian tension curve** — rising action, climax, resolution — at the beat level, shaping the overall experience regardless of player actions. The drama manager is the "author surrogate": its job is to keep the piece *a play*.
- **ABL (A Behavior Language).** Purpose-designed reactive behavior language, an evolution of the ABT (behavior tree) tradition and a descendant of Hap (Loyall, 1997). Each character (Trip, Grace) is implemented as hundreds of ABL behaviors: small, interruptible, concurrent, goal-oriented scripts for physical action, dialogue selection, emotional response, and memory maintenance.
- **Natural-language understanding.** Player types free text; a surface parser maps utterances to a bounded set of **discourse acts** (praise, criticize, flirt, comfort, provoke, reference-a-topic, etc.) with object/target bindings. Characters react to the discourse act, not the literal words.
- **Memory.** Characters track what the player has said and done, and reference it in later beats (e.g. Grace remembering whose side the player took). Shallow but real.
- **Expressive output.** Animated 3D characters with real-time gesture, facial expression, proximity, and voiced dialogue pre-recorded in many variants and selected contextually. The surface was not LLM-generated — it was hand-authored at enormous scale.

Approximate authorial scope: ~27 beats, thousands of authored dialogue lines, dozens of natural-language response categories. Mateas and Stern have estimated the project took ~5 years of full-time work for a roughly 20-minute experience.

## Output

A playable interactive one-act. Opening: the player, visiting friends Trip and Grace, arrives at their apartment. The couple's marriage is disintegrating and the player's presence catalyzes a confrontation. Across roughly 20 minutes, the player's dialogue choices, physical movement, and active provocations shape which disclosures occur, whose side either spouse takes the player to be on, whether the marriage ends that night, and what last thing each character says to the other. Multiple endings, none of them "win/lose" — all are dramatic outcomes with emotional weight.

The piece is genuinely dramatic in a way few pieces of interactive media are. It was critically acclaimed on release and is still cited as the baseline any serious interactive-drama proposal must compare itself to.

## What worked

- **Beat-driven drama management.** Separating *what the piece is doing dramatically* from *what characters are doing locally* was the right cut. The drama manager could preserve narrative shape across wildly varying player behavior.
- **ABL + reactive agents.** Characters felt alive in short bursts — not because they were deeply simulated, but because they were *expressive* in the ABL-engineered sense: they reacted, interrupted each other, remembered, shifted mood. Good authoring in a good language outperformed any amount of goal-directed planning.
- **Natural-language *as input*, carefully scoped.** The parser doesn't understand English; it understands Façade-relevant discourse acts. By narrowing ambition, it achieved usefulness.
- **Dramatic quality.** The piece works as a piece of theater. This is the rarest success in the field.

## What failed (or bounded the work)

- **Authorial cost.** Five years of work for ~20 minutes of experience. The piece does not scale; its architecture does not straightforwardly produce longer or different dramas without commensurate authoring effort.
- **Fragility at boundaries.** Player utterances far outside the parser's coverage produce deflections or awkward non-sequiturs. The illusion holds for most players but breaks for exploratory ones.
- **Single drama, single genre.** Façade is a specific piece, not a platform. Abandoning the drama and trying to reuse the engine for a different story requires re-authoring the beat library, ABL behaviors, character memory, and parser vocabulary.
- **No generative surface.** All dialogue was pre-authored; the piece does not compose new lines. This is a deliberate choice (reliability, quality, performance), not a failing — but it means Façade cannot respond to genuinely novel player input with genuinely novel character language.
- **The sequel problem.** Mateas and Stern began a successor project (*The Party*) aimed at a larger cast and more flexibility; it did not reach public release. This is informative: the architecture's authorial cost did not yield gracefully to scope expansion.

## Lessons for an engine

1. **Drama management is a first-class architectural layer.** Separate from world simulation, from character agents, and from surface generation. The drama manager is where the *authorial* function lives operationally. MINSTREL had author goals; Façade put them in charge of beat selection in real time.
2. **Beats are a useful unit.** Larger than events, smaller than acts. Each beat has a dramatic purpose that can be checked, satisfied, or failed. A long-form engine should probably retain beats (or something like them) as the scheduling unit between raw events and structural phases.
3. **Authored richness beats inferred richness, when affordable.** Façade succeeds because its characters were hand-built to an absurd level of expressive depth. An LLM-era engine does not need to pre-author every line, but it should inherit the insight: *character richness must be specified somewhere*; it does not emerge from a thin representation.
4. **Narrow the NLU problem until it becomes solvable.** Classify into discourse acts; do not attempt free-form language understanding. This generalizes: *do the minimum comprehension the narrative requires, and no more*.
5. **Existence proofs bound ambition honestly.** Façade demonstrated that AI interactive drama is possible at great authorial cost. A twenty-year engine should know where Façade drew its boundary and be explicit about which of its constraints to relax (surface generation via LLMs), which to keep (drama management), and which to design around (authorial cost).

## Relationship to other systems

- **Successor in spirit to** early interactive drama (Oz Project at CMU, the Virtual Theater Project at Stanford). ABL is a descendant of Hap (Bates, Loyall, Reilly, Oz Project, early 1990s).
- **Sibling to** narrative-rich interactive fiction (Inform 7 games, *Galatea* by Emily Short, Versu by Emily Short and Richard Evans).
- **Influences** subsequent interactive-narrative research — Prom Week (McCoy, Mateas, Wardrip-Fruin), Versu (Evans, Short), agent-based LLM drama systems.
- **Complementary to** story-generation work (TALE-SPIN / MINSTREL / MEXICA lineage): Façade is about *playing out* a story interactively; the story-generation lineage is about *producing* a story to be read. Both lineages need drama management, but for different reasons.

## Sources

- Mateas, Michael. *Interactive Drama, Art and Artificial Intelligence*. PhD dissertation, Carnegie Mellon University, 2002. **[Primary — not yet read.]**
- Mateas, Michael, and Andrew Stern. "Structuring Content in the Façade Interactive Drama Architecture." *AIIDE* 2005. **[Primary — not yet read.]**
- Mateas, Michael, and Andrew Stern. "Writing Façade: A Case Study in Procedural Authorship." In *Second Person: Role-Playing and Story in Games and Playable Media*, MIT Press, 2007. **[Primary — not yet read.]**
- *Façade* the work itself. Free download, originally from interactivestory.net. **[Playable — worth running before deepening this entry.]**

*This entry would benefit most from actually playing through Façade a few times with deliberate attention to the seams — what the drama manager is doing is most visible when you push on it.*
