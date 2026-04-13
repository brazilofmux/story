# Sternberg's Universal Narrative Interests

## One-line summary

A reader-side theory of narrative (1978, developed through the 1990s and 2000s) identifying three universal interests that every narrative deploys by manipulating the relation between story-time and discourse-time: **suspense** (the future is uncertain), **curiosity** (the past is uncertain), and **surprise** (a prior understanding is overturned) — the cleanest decomposition in the field of what readers actually experience moment to moment.

## Origin

Meir Sternberg, Israeli literary theorist. Principal works:

- *Expositional Modes and Temporal Ordering in Fiction* (Johns Hopkins, 1978) — the first full statement.
- *The Poetics of Biblical Narrative* (Indiana, 1985) — extended application.
- *Telling in Time* series, *Poetics Today* (1990, 1992, 2006) — deepest theoretical elaboration.

Draws on the Russian Formalist *fabula / sjuzhet* distinction (story vs. discourse) and on Aristotle, but its contribution is distinctly reader-facing.

## Core claim

Narrative is, at the level of reader experience, the **play of knowledge discrepancies over time**. At every moment the reader knows some things, doesn't know others, thinks they know things they don't. A narrative's power derives from how it arranges three fundamental discrepancies:

- **Suspense.** The reader knows something *is* going to be resolved in the future but doesn't know *how*. Prospective gap.
- **Curiosity.** The reader knows something *has* happened in the past but doesn't know *what*, *how*, or *why*. Retrospective gap.
- **Surprise.** The reader thought they knew, and is shown they were wrong. Reconfigurative shock.

All three are functions of the relation between **story order** (when events happened in the world) and **discourse order** (when the reader learns about them). Different arrangements of the same events produce radically different narrative interests. The same murder told chronologically is suspense; told with the killer's identity withheld is curiosity; told with the wrong killer implied until the final chapter is surprise.

## Structural elements

- **Three interests**, as above — logically exhaustive for information-state discrepancies along the temporal axis.
- **Gaps.** Places where the reader knows they don't know (prospective → suspense; retrospective → curiosity).
- **Blanks.** Places where the reader doesn't yet know they don't know — the substrate of surprise. Blanks become gaps retroactively.
- **Expositional mode.** Where, how, and in what order backstory is revealed. A story can frontload exposition (leaving no blanks, producing mostly suspense), defer it (leaving blanks that become curiosity-gaps when hinted at), or weaponize it (false exposition, later overturned — surprise).
- **Primacy and recency effects.** What the reader encounters first and last disproportionately shapes their running model. Sternberg is careful here: narrative manipulates these cognitive biases by design.

## What it explains well

- **Why mystery and thriller feel different**, despite both involving crimes: thrillers are suspense-dominant (the reader knows the threat and worries forward), mysteries are curiosity-dominant (the reader knows a thing happened and works backward).
- **Why revealing plot points out of order** is not a stylistic flourish but a genre-selecting operation: reordering the same fabula produces a different object.
- **Why dramatic irony** is a special case of curiosity-from-the-character-side: the reader's knowledge projection exceeds the character's.
- **Why surprise only works once and curiosity only works until resolved, but suspense can be renewed indefinitely.** Different interests have different decay profiles — a fact craft theories intuit but rarely formalize.

## What it doesn't explain / gaps

- **Emotional beyond cognitive.** Sternberg's trio is about information states. It says little about warmth, grief, wonder, disgust, aesthetic pleasure. MEXICA-style emotion/tension is complementary, not redundant.
- **Theme.** The theory is about how narrative manages reader knowledge, not about what narratives *mean*.
- **Character interiority.** A character-side theory (how characters know and feel) is not Sternberg's project.
- **Multi-layered readerships.** A reader on a second reading has no blanks and few gaps; curiosity and surprise collapse, suspense partially survives. The theory handles this by accepting that a re-reader is a different audience — elegant but arguably thin.
- **Scale.** Works best on a scene or chapter; sustaining explicit gap-management across a 200,000-word novel requires machinery Sternberg gestures at but does not fully elaborate.

## Relationship to other theories

- **Ancestor:** Russian Formalist fabula/sjuzhet (Shklovsky, Tomashevsky), and Aristotle's peripeteia/anagnorisis (anagnorisis is Sternberg's *surprise-via-curiosity-resolution* in miniature).
- **Sibling:** Gerald Prince's narratology; Genette's *Narrative Discourse* (especially on order, duration, frequency). Sternberg's interests live within the Genette-style discourse/story distinction.
- **Complementary to:** Aristotle (dramatic structure), MEXICA (emotion/tension), Propp (function-level syntax). Sternberg operates on a different axis — reader knowledge — and can be overlaid on any of them.
- **Unique contribution:** the strongest case in print that **narrative = temporal manipulation of reader knowledge**. This is the load-bearing insight for our engine.

## Formalizability

Extremely high, and — crucially — **directly compatible with the event-log + per-agent-knowledge-projection substrate** already under consideration.

- **Model.** Treat the reader as another agent in the knowledge graph. At every point in the discourse, the reader has a set of known facts, a set of hypothesized facts, and a set of blanks they don't know they have.
- **Query.** At each moment of narration, compute:
  - *Suspense:* does the reader's future model contain an unresolved question with known stakes?
  - *Curiosity:* does the reader know an outcome but lack causes?
  - *Surprise:* does new information contradict a prior model state?
- **Operation.** Authorial choices become operations on the reader's knowledge state:
  - Reveal a fact → close a gap.
  - Hint at a fact → open a gap, convert blank to curiosity.
  - Mislead → set up a future surprise.
- **Measurement.** Gap counts, blank counts, and surprise frequency become computable metrics of narrative interest — candidates for the reader-model critic layer the field is otherwise missing.

The integration is almost too neat to be coincidence: the substrate needed for dramatic irony, mystery, and reveal (per-agent knowledge over time) **is** the substrate needed for Sternberg's interests (reader as an agent).

This is the entry that changed my mind about where to begin building. If we formalize one reader-side theory first, it should be this one.

## Sources

- Sternberg, Meir. *Expositional Modes and Temporal Ordering in Fiction*. Baltimore: Johns Hopkins University Press, 1978. **[Primary — not yet read.]**
- Sternberg, Meir. *The Poetics of Biblical Narrative: Ideological Literature and the Drama of Reading*. Bloomington: Indiana University Press, 1985. **[Primary — not yet read.]**
- Sternberg, Meir. "Telling in Time (I): Chronology and Narrative Theory." *Poetics Today* 11, no. 4 (1990): 901–948. **[Primary — not yet read.]**
- Sternberg, Meir. "Telling in Time (II): Chronology, Teleology, Narrativity." *Poetics Today* 13, no. 3 (1992): 463–541. **[Primary — not yet read.]**
- Sternberg, Meir. "Telling in Time (III): Chronology, Estrangement, and Stories of Literary History." *Poetics Today* 27, no. 1 (2006): 125–235. **[Primary — not yet read.]**

*Sternberg is dense and his articles are long. A serious engagement with one of the *Poetics Today* papers is likely the right investment before deepening this entry.*
