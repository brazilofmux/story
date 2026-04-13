# MINSTREL

## One-line summary

Case-based story generator (1994) that produced short King Arthur tales by combining character-level goals with explicit *author-level* goals, retrieving and adapting prior story fragments from memory through a transformation mechanism called TRAM — the direct theoretical response to TALE-SPIN's "simulation is not story" failure.

## Origin

Scott R. Turner, PhD dissertation, UCLA, 1992. Published as *The Creative Process: A Computer Model of Storytelling and Creativity*. Hillsdale, NJ: Lawrence Erlbaum, 1994. Supervised by Michael Dyer; part of a broader UCLA effort on AI models of creativity and case-based reasoning.

## Goal

Demonstrate that story generation is a **creative** act distinct from simulation: that generating a story requires not only characters with goals but an *author* with goals — about what the story should teach, evoke, or dramatize. Concretely, generate short Arthurian stories that read as intentional narratives, not as transcripts of a world simulation.

## Architecture

MINSTREL's design is the first major system to structurally separate the two layers TALE-SPIN conflated.

- **Character-level goals.** As in TALE-SPIN: agents with goals, plans, actions in a world.
- **Author-level goals.** Explicit representations of what the *story* should achieve:
  - **Thematic goals** — the story should illustrate a proverb-like lesson (e.g. "deception is punished").
  - **Dramatic goals** — the story should produce suspense, surprise, tragedy, irony.
  - **Consistency goals** — the story should remain coherent, non-contradictory, causally linked.
  - **Presentation goals** — the story should be told in a certain order, at a certain level of detail.
  - Author goals compete and are scheduled by a priority mechanism; satisfying one may require sub-story-fragments to be generated and adapted.
- **Case-based memory.** A library of prior story fragments (scenes, events, schemas). Generation proceeds by *remembering* similar past fragments and adapting them to current constraints rather than planning from first principles.
- **TRAM — Transform-Recall-Adapt Method.** MINSTREL's core creativity mechanism. When a direct memory lookup fails, TRAM systematically *transforms* the query — generalize one element, substitute another, relax a constraint — then *recalls* on the transformed query, then *adapts* the retrieved case back toward the original problem. Iterated, this produces novel combinations from a finite case library. TRAM is MINSTREL's main contribution to case-based reasoning beyond its storytelling domain.
- **Schema library.** Conceptual patterns — e.g. *thwarted-love*, *deception-punished*, *knight-kills-monster* — at a higher level than individual events, used to scaffold coherent sequences.
- **Surface generator.** Templates over the underlying event/scene representation, producing short English prose.

## Output

Short (a few paragraphs to a page) Arthurian stories. A widely-cited example (reconstructed; details vary across sources):

> *Once upon a time, a knight named Lancelot loved a princess named Andrea. But Andrea did not love Lancelot. Lancelot went into the forest to fight the dragon, because he thought that if he killed the dragon, Andrea would love him. But in the forest, Lancelot met a troll, and the troll killed Lancelot. Lancelot was dead.*

Turner's thesis documents many such stories and carefully catalogs where MINSTREL succeeded and where it produced non-story output or miscombined schemas.

## What worked

- **Layered goals.** The character/author separation was a genuine advance over TALE-SPIN and shaped subsequent computational narrative research.
- **Case-based generation.** Re-using and adapting prior story material handled many causality and coherence problems that pure planners struggled with — the system inherited common-sense implicit in its cases.
- **TRAM as a creativity mechanism.** A concrete, implementable algorithm for "novel combination" that could be explained independent of storytelling — a rare thing in AI-creativity work.
- **Thematic coherence on small inputs.** For its scale, MINSTREL's stories could legibly illustrate a theme, which is what TALE-SPIN's could not.

## What failed

- **Scale.** The case library was small and hand-built. Extending to more genres or longer forms would have required enormous manual curation, and the TRAM search space grew quickly.
- **Author goals were canned.** The *author* in MINSTREL had a small fixed repertoire of dramatic intents. There was no model of *why* a particular theme was being pursued in this story, only a scheduled goal.
- **Surface quality.** Output prose was recognizably computer-generated; the surface generator was limited by 1990s NLG tools.
- **No reader model.** Like TALE-SPIN, MINSTREL had no explicit model of a reader; dramatic effects were encoded as author goals rather than predicted on a simulated audience. (Turner discusses this as future work.)
- **Character shallowness.** Characters were functional — goal-bearing agents, as in TALE-SPIN — with only the interiority their current schema required. No developed theory of character arc.
- **Brittleness at boundaries.** When TRAM's transformations retrieved a poorly-matching case, adaptation could produce subtly wrong events. Turner catalogs these as part of the creative-process analysis, not as bugs to be patched over.

## Lessons for an engine

1. **Author layer is mandatory.** Any engine that omits an author-level goal structure will reproduce TALE-SPIN's failure mode at a new level of sophistication. MINSTREL is the canonical demonstration.
2. **Creative generation ≈ search over adaptations of remembered cases.** This is now a commonplace in case-based creativity research, but MINSTREL is where it was first made concrete for narrative. An LLM-era engine can substitute "retrieval-augmented generation over a narrative corpus" for MINSTREL's case library without changing the architecture's shape.
3. **Separate theme from plot from scene from surface.** MINSTREL's four layers (author goals, schemas, events, surface) are approximately the right decomposition. Subsequent systems and our own engine will want something close to this stack.
4. **TRAM's "transform, retrieve, adapt" loop is reusable** outside storytelling — a general-purpose creativity pattern MINSTREL happens to apply to narrative.
5. **Canned author intent is a ceiling.** Real authors form intent about *this* story, often mid-writing, often by discovering what it is about. A long-running engine will need a model of author intent that is itself generated, critiqued, and revised — not a fixed list.

## Relationship to other systems

- **Direct response to TALE-SPIN.** Same team tradition (Schankian AI), same language family (CD-style representations), but a deliberate architectural rejection of pure character-goal simulation.
- **Parallel to, not derived from, MEXICA** (Pérez y Pérez, 1999), which reached a related conclusion — stories are not just planned — via a completely different route: engagement/reflection cycles instead of layered goals and TRAM.
- **Succeeded by Riedl's author-goal planners** (Fabulist and descendants), which formalized the author/character split as a two-level partial-order planning problem.
- **Influences LLM-era work** indirectly: retrieval-augmented narrative generation, explicit prompt-level "author goals," and drafting-then-editing pipelines all re-discover MINSTREL's basic shape.

## Sources

- Turner, Scott R. *The Creative Process: A Computer Model of Storytelling and Creativity*. Hillsdale, NJ: Lawrence Erlbaum, 1994. **[Primary — not yet read.]**
- Turner, Scott R. *MINSTREL: A Computer Model of Creativity and Storytelling*. PhD dissertation, UCLA, 1992. **[Primary — not yet read.]**
- Re-examinations and extensions: Tearse, Mawhorter, Mateas, and Wardrip-Fruin on reconstructing and critiquing MINSTREL in the 2010s (UC Santa Cruz group). **[Not yet read — important modern commentary.]**

*Example story above is reconstructed from secondary sources; exact text should be verified against Turner's thesis.*
