# Dramatica

## One-line summary

An ambitious, totalizing theory of story (1993) claiming that every complete story is an analogy to a single mind grappling with a problem, expressible as a combinatorial selection from a four-throughline, multi-level structural framework; the theory is detailed, internally consistent in its own terms, and notoriously opaque — including, at points, to its own authors.

## Origin

Melanie Anne Phillips and Chris Huntley. *Dramatica: A New Theory of Story*. Burbank, CA: Screenplay Systems (later Write Brothers), first edition 1993; current editions substantially revised. Accompanied from the start by *Dramatica Pro* software (1994 onward), which is essentially the theory as a questionnaire-driven tool that narrows ~32,768 possible "story forms" to one by eliminating incompatible choices.

## Core claim

A fully told story (a "Grand Argument Story" in Dramatica's vocabulary) is an analogy to a single mind working a problem to completion. Every story therefore has the same underlying cognitive shape, and the apparent diversity of stories is the result of different *choices* at a large but finite number of structural decision points.

The theory posits four *throughlines* any Grand Argument Story must have:

1. **Overall Story Throughline (OS)** — the objective problem, seen from outside. Plot.
2. **Main Character Throughline (MC)** — the protagonist's personal problem, seen from inside their head.
3. **Influence Character Throughline (IC)** — a second character (not always the "antagonist") whose worldview challenges the MC's. The MC and IC are locked in a philosophical argument across the story.
4. **Relationship Throughline (RS)** — the evolving relationship between MC and IC, treated as its own arc.

Each throughline occupies one of four *domains* (Situation, Activity, Fixed Attitude, Manipulation) in a constrained pattern, and each domain is subdivided recursively into *concerns*, *issues*, and *problems* — a four-by-four-by-four-by-four lattice (the *Dramatica Table of Story Elements*).

The user (author) makes a small number of high-level choices; the system (software, or in principle a reader-theorist) propagates them through the lattice to a single consistent story form.

## Structural elements

- **Grand Argument Story (GAS).** A complete story that makes an argument by dramatizing the consequences of one approach to a problem (MC's) while contrasting it with another (IC's).
- **Four throughlines** — described above.
- **Four domains** — Situation (external state), Activity (external process), Fixed Attitude (internal state), Manipulation (internal process). Each throughline inhabits exactly one domain; the four throughlines cover all four domains.
- **Quads.** Dramatica is built from recursive quads: any choice is a selection from four options, each of which subdivides into four, and so on. This is the theory's characteristic mathematical shape.
- **Elements.** At the leaves: 64 "Dramatic Elements" — pairs of character motivations (e.g. *Pursuit/Avoidance*, *Logic/Feeling*, *Consideration/Reconsideration*). Characters are built as sets of elements.
- **Story Mind.** The metaphor that unifies it all: the story is one mind, and the characters are facets of that mind engaged in the same internal argument.
- **Main Character resolve.** The MC either *changes* (adopts the IC's view) or *remains steadfast* (holds their own). Combined with whether the outcome is *success* or *failure*, this yields four archetypal story "judgments."
- **Author's Intent.** Made explicit: the author must know whether the MC is ultimately right or wrong, because the argument the story makes hinges on it.

## What it explains well

- Why some stories feel *complete* and others feel *unfinished* even when structurally well-formed in a three-act sense: completeness in Dramatica requires all four throughlines to close.
- The structural role of a character who is not the antagonist but is philosophically opposed to the protagonist — what other theories call the *reflection character* or *shadow*. Dramatica makes the IC a first-class element.
- Why the same plot can feel tragic or redemptive: change-vs-steadfast × success-vs-failure yields a 2×2 that distinguishes (e.g.) a classical tragedy from a redemption arc from a cautionary tale.
- Tight integration of *theme* into *structure* — the story's argument is literally built into the lattice.

## What it doesn't explain / gaps

- **Stories that are not Grand Argument Stories.** Dramatica acknowledges these exist (episodic, slice-of-life, tone poems) and largely brackets them. For a general theory of story this is a significant omission.
- **Short forms and episodic TV.** The GAS framework requires a completed argument; serialized television and many short stories resist this.
- **Subplots beyond the four throughlines.** Ensemble works with many parallel arcs are hard to fit without declaring most of them non-GAS.
- **Opacity and internal jargon.** The theory uses idiosyncratic vocabulary (*Mental Sex*, *Problem-Solving Style*, *Approach*, *Dynamic Pairs*) that does not map cleanly onto pre-existing craft vocabulary, and definitions cross-reference each other in ways that can be circular on a first read.
- **Self-explainability.** The theory's own authors have at times acknowledged that certain components are difficult to explain or to justify in non-Dramatica terms. This is the key finding for us: a theory so intricate that its inventors cannot fully unfold it is either profound, incomplete, or both — and distinguishing those cases is itself part of the research task.

## Relationship to other theories

- **In contact with** most Western craft theory (three-act, Campbell, McKee) — Dramatica sometimes re-describes the same phenomena in its own vocabulary, sometimes draws genuinely novel distinctions (most clearly the IC/MC philosophical argument and the four throughlines).
- **Closest in ambition to** computational narrative work: the theory *wants* to be an expert system. The software is an expert system, of a sort.
- **Opposed by** practitioner theorists who find the framework over-engineered (Story Grid's Coyne, for example, pulls structural analysis back toward genre-level obligatory scenes).
- **Heir to** Aristotle's ambition (a complete theory of dramatic form) with a structuralist-combinatorial twist Aristotle would not recognize.

## Formalizability

Paradoxically, very high *in form* and very hard *in practice*.

- **High in form:** Dramatica is the most explicitly combinatorial story theory we have. It is *designed* to be a finite-choice system. The Dramatica software instantiates it. In principle, an engine could consume a Dramatica "story form" and use it as a high-level constraint on generation.
- **Hard in practice:**
  - The operational meaning of many elements (*Conscience*, *Temptation*, *Consideration*) is defined in Dramatica terms and requires internalizing the whole lattice to apply.
  - Mapping actual human stories *into* the Dramatica lattice is reported to be difficult and sometimes contentious between experienced users.
  - The relationship between the abstract lattice and concrete scene-level events is weakly specified: the theory tells you what the story *is about* at a high level, not what characters should *do* on page 47.
  - The known opacity of the theory itself is a hazard: formalizing something we don't fully understand risks formalizing the wrong thing confidently.

The valuable move for a story engine is probably not to adopt Dramatica wholesale, but to extract what it does uniquely well — the four-throughline model, the MC-IC philosophical argument, the change-vs-steadfast × success-vs-failure quad, and the insistence on theme-as-argument — and let the rest sit as a research hazard.

## Sources

- Phillips, Melanie Anne, and Chris Huntley. *Dramatica: A New Theory of Story*. Write Brothers, 1993; current revised editions through the 2010s. **[Primary — not yet read in full.]**
- Huntley, Chris, and Melanie Anne Phillips. *Dramatica Theory Book*, current online edition at dramatica.com. **[Primary — not yet read in full.]**
- *Dramatica Pro* software (Write Brothers). **[The theory in executable form — not yet exercised.]**

*Dramatica is a case where careful engagement with the primary source is more important than usual: secondhand summaries of Dramatica are reliably inaccurate. This entry itself should be treated as a rough sketch to be rewritten after a primary reading.*
