# MEXICA

## One-line summary

Story generator (1999) built on a cognitive model of creative writing as an alternation of *engagement* (associative generation) and *reflection* (critical evaluation), producing short narratives set in the pre-Hispanic Mexica (Aztec) world — the principal architectural alternative to goal-directed planner and author-goal paradigms.

## Origin

Rafael Pérez y Pérez, PhD dissertation, University of Sussex, 1999, supervised by Mike Sharples. Built on Sharples' cognitive theory of writing as engagement–reflection (Sharples, *How We Write*, 1999). Subsequent development continued at UAM Cuajimalpa (Mexico City) for over two decades, yielding MEXICA and its successors as an ongoing research platform.

## Goal

Test whether a plausible **cognitive model of how humans write** — specifically Sharples' engagement/reflection account — could produce stories, and to do so **without** relying on explicit goal-plan-action planning or author-level goal scheduling. Build creativity in as process, not as an annotated output.

## Architecture

Two alternating phases operate on a shared **story-in-progress** (a sequence of story actions performed by characters in a world, each annotated with emotional and tension state).

- **Engagement.** Given the current story-so-far, retrieve from memory story fragments that match the current **emotional and tension context** (not character goals). Chain one retrieved action onto the current draft. No look-ahead, no goal planning — associative, context-driven continuation.
- **Reflection.** Pause engagement. Check the current draft for:
  - **Coherence** — are preconditions satisfied for each action?
  - **Novelty** — is the emerging story too close to a memorized one?
  - **Interestingness** — is emotional/tension variation within acceptable range?
  - **Breaks in narrative flow** — impasses where engagement cannot continue.
  Apply fixes: insert preconditioning actions, prune, modify state. When satisfied, return to engagement.
- **Story actions.** Typed events in the Mexica world (warriors, princesses, priests, jaguar knights, sacrificial rites). Each action has preconditions and emotion/tension effects defined relative to participants.
- **Previous-stories memory.** A hand-curated corpus of prior Mexica tales (authored by Pérez y Pérez) provides the associative substrate for engagement.
- **Emotional links.** Between any pair of characters, a dynamic (love, rivalry, fear, gratitude). Engagement retrieval is driven largely by the pattern of current emotional links plus global tension.
- **Tension.** A scalar (or structured) measure of dramatic intensity, evolving over the draft; shaping the engagement retrieval and the reflection's "interestingness" check.

Critically: **no explicit author goals and no character goals.** The system does not plan toward an ending. Stories end when engagement cannot proceed, reflection cannot unblock the impasse, and a closing action is reached.

## Output

Short narratives, Mexica/Aztec setting, in English:

> *The jaguar knight was an inhabitant of the Great Tenochtitlan. The princess was an inhabitant of the Great Tenochtitlan. The jaguar knight was walking when Ehecatl (god of the wind) took him to the lake of the moon. Suddenly, a snake appeared from the water and attacked him. The jaguar knight fought the snake. The princess observed the fight. The jaguar knight killed the snake. The princess fell in love with the jaguar knight...*

(Exact text varies across papers; representative of the shape.)

## What worked

- **A real architectural alternative.** Demonstrated that capable story generation does not require the planner + author-goals stack. Engagement + reflection, operating on an emotion/tension substrate, can do meaningful work.
- **Emotion and tension as primary drivers.** Pérez y Pérez's central thesis — that readers track emotional dynamics and tension curves more than goal-completion — turned out to be empirically resonant with reader studies and with reader-response theory.
- **Impasse as a first-class event.** Reflection exists specifically to handle moments when engagement gives up. Explicitly modeling creative impasse is philosophically and practically important; few systems before or since make it central.
- **Long-running research program.** Unlike many one-shot AI-narrative systems, MEXICA has been extended, critiqued, and reimplemented for 25+ years by Pérez y Pérez and collaborators — providing a rare longitudinal record.

## What failed

- **Genre-bound corpus.** The memorized stories are all Mexica-world tales authored by the researcher. Portability to other genres requires recreating the corpus. Reflection rules also encode domain knowledge.
- **Limited surface generation.** Output prose is templated and stilted by modern standards.
- **No explicit theme.** Engagement/reflection is beautiful at producing *something interesting* but less forceful at producing a story *about* a specific idea. Later MEXICA variants and collaborator work have tried to layer thematic control on top.
- **Shallow characters.** Like other pre-LLM systems, characters have functional slots, not interiority.
- **Scaling.** Longer stories require larger memories and more complex reflection rule-sets; the cognitive elegance that works on short tales strains over chapter-length or novel-length drafts.

## Lessons for an engine

1. **Planner + author-goals is not the only viable stack.** Engagement/reflection is a credible alternative whose strengths (emotion-driven coherence, explicit impasse-handling) are complementary to planner strengths (goal directedness, causal guarantees). A mature engine may want both, used at different layers.
2. **Emotion and tension are first-class state.** Any story substrate that does not represent them as primary dynamic variables will under-represent what readers actually track.
3. **Impasse-handling is real creative work.** Engines that silently stall or silently generate nonsense when they run out of material fail in a specific way MEXICA identifies and addresses. Modeling the impasse explicitly — and having a reflection step that fixes it — is an architectural choice worth copying.
4. **Reflection needs domain knowledge.** Coherence and interestingness checks are not domain-neutral. A multi-genre engine will need parameterized reflection rules, not a single fixed checker.
5. **LLM parallel.** "Engagement" maps loosely onto LLM next-token continuation; "reflection" maps onto critique/revision passes. MEXICA's structure anticipates what is now called *iterative drafting* with LLMs — not because MEXICA used LLMs but because Sharples' cognitive model is what humans do, and LLM scaffolds rediscover it.

## Relationship to other systems

- **Opposes** TALE-SPIN, MINSTREL, and Fabulist on the question of whether planning/goals are the right substrate. MEXICA says no: cognitive process, not goal plans.
- **Closest sibling** is Sharples' own cognitive-writing work — MEXICA is arguably Sharples' theory, instantiated.
- **Influences** modern agent-based and critique-driven LLM narrative systems: drafting-then-reflecting pipelines, self-refinement loops, and planner-free creative agents all echo the engagement/reflection split.
- **Cited as counterexample** in debates about whether story generation can be reduced to planning.

## Sources

- Pérez y Pérez, Rafael. *MEXICA: A Computer Model of Creativity in Writing*. PhD dissertation, University of Sussex, 1999. **[Primary — not yet read.]**
- Pérez y Pérez, Rafael, and Mike Sharples. "MEXICA: A Computer Model of a Cognitive Account of Creative Writing." *Journal of Experimental & Theoretical Artificial Intelligence* 13, no. 2 (2001): 119–139. **[Primary — not yet read.]**
- Sharples, Mike. *How We Write: Writing as Creative Design*. London: Routledge, 1999. **[The cognitive theory MEXICA implements — not yet read.]**
- Pérez y Pérez, Rafael. *Mexica: 20 Years – 20 Stories*. 2017 (edited volume reflecting on two decades of the system). **[Not yet read.]**

*Sample output above is representative, reconstructed from standard summaries; exact text should be verified against primary sources.*
