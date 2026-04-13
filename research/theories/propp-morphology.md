# Propp's Morphology of the Folktale

## One-line summary

Structural analysis (1928) of Russian wonder tales reducing them to a fixed sequence of 31 "functions" (plot-level actions defined by their role in the tale) and 7 spheres of action (character roles), demonstrating that within the genre nearly all tales are recombinations of the same invariant building blocks in a fixed partial order.

## Origin

Vladimir Propp, *Morfologiya skazki* (*Morphology of the Folktale*), Leningrad, 1928. Russian formalist, later Soviet folklorist. Corpus: approximately 100 Russian wonder tales from the Afanasyev collection (tales 50–151 by one common numbering), selected for being of one genre — the *volshebnaya skazka* (wonder tale). Not translated into English until 1958 (University of Texas Press).

## Core claim

Within the Russian wonder tale, story variation is lexical, not structural. Different tales use different characters, objects, and settings, but the *functions* performed — and the *order* in which they can occur — are constant. Story is a syntax; particular tales are sentences in it.

## Structural elements

**7 spheres of action** (character role-types, not fixed persons):

1. Villain
2. Donor / provider
3. (Magical) Helper
4. Princess and her father (sought-for person and the dispatcher of the hero to find them)
5. Dispatcher
6. Hero (seeker or victimized)
7. False hero

A single character can occupy multiple spheres; a single sphere can be shared across characters.

**31 functions**, abbreviated, and always in the following order when present (though any can be skipped):

0. Initial situation (not a function; the setup).
1. Absentation — a family member leaves.
2. Interdiction — the hero is warned.
3. Violation — the interdiction is broken.
4. Reconnaissance — the villain probes.
5. Delivery — the villain gains information.
6. Trickery — the villain attempts deception.
7. Complicity — the victim is deceived.
8. Villainy / Lack — the central motivator: harm, kidnapping, or lack.
9. Mediation — the lack becomes known; the hero is dispatched.
10. Counteraction — the hero agrees to act.
11. Departure.
12. First function of the donor — hero is tested.
13. Hero's reaction.
14. Receipt of a magical agent.
15. Guidance — spatial transference.
16. Struggle — hero and villain in direct combat.
17. Branding — hero is marked.
18. Victory — villain defeated.
19. Liquidation — initial misfortune or lack resolved.
20. Return.
21. Pursuit.
22. Rescue.
23. Unrecognized arrival.
24. Unfounded claims — false hero's claim.
25. Difficult task.
26. Solution.
27. Recognition.
28. Exposure — of the false hero.
29. Transfiguration — hero's new appearance.
30. Punishment — of the villain.
31. Wedding / ascension.

The sequence is partial — many tales contain only a subset — but relative order is preserved. Propp also identified *moves* (a misfortune-to-resolution cycle): a tale may consist of one or several moves in series.

## What it explains well

- The uncanny structural sameness of folktales despite surface variety.
- Why genre pastiche is so tractable: once the function-order is known, recombination produces recognizable tales.
- Why characters in folktales feel flat — they are defined by function, not interiority. Propp would say this is correct, not a failure.
- A natural computational target: functions are enumerable, the order is partial, characters are role-slots.

## What it doesn't explain / gaps

- **Genre-bound.** Propp himself is clear: the morphology is of the Russian *wonder tale*. He does not claim it generalizes to all folktales, much less all stories. Later writers (Campbell, Hollywood) generalized it in ways Propp did not sanction.
- **No account of style, tone, theme, meaning.** Deliberately — the morphology brackets these to isolate structure. But a story engine needs them eventually.
- **No account of character interiority.** Characters are functions; psychology is absent.
- **No account of the narrator / audience.** Fabula only; no sjuzhet in the later Russian Formalist sense.
- **Rigidity.** Non-wonder-tale stories (psychological novels, modernist fiction, ensemble drama) resist the sequence — not because Propp is wrong about wonder tales, but because these are different objects.

## Relationship to other theories

- **Reaction to and against** the motif-based taxonomy of the Finnish school (Aarne-Thompson), which categorized tales by superficial content. Propp's move is to shift from *what* appears to *what it does*.
- **Ancestor of structuralist narratology** — Greimas (actants, a compression of Propp's spheres), Barthes, Bremond, Todorov all descend from Propp.
- **Overlaps heavily with** Campbell's monomyth — Campbell's hero's-journey stages map onto large stretches of Propp's function sequence, though Campbell's interpretive apparatus (archetypes, mythic meaning) is Jungian and Propp's is formalist.
- **Orthogonal to** Aristotle: Propp is descriptive and functional; Aristotle is prescriptive and dramatic.
- **Direct lineage to computational narrative:** Propp's functions were one of the earliest formalisms attempted for story generation. Systems since the 1970s have used Propp-inspired grammars.

## Formalizability

High — the highest of the major story theories. Propp's morphology is *already* in a form close to what an engine can consume.

- **Functions are enumerable** (31) and nameable. Each is definable by its role (e.g. "an event in which a lack is introduced or a villain inflicts harm"), which is close to an executable predicate.
- **Sphere-of-action roles** are role-slots — a natural fit for a typed character system.
- **The partial-order constraint** is directly expressible as a grammar or ordering relation.
- **Natural generation target:** pick a subset of functions respecting the order, bind each to agents in the spheres-of-action, render. This is essentially what Propp-grammar story generators have done since the 1970s.

**Resists formalization:**

- The distinction between *villainy* and *lack* (function 8) is sometimes a judgment call.
- What counts as a *function* vs. mere *event* requires applying Propp's functional definition in a contestable way.
- Extending beyond the wonder tale without destroying the theory.

The cleanest formal payoff from Propp is this: a story as a partially-ordered sequence of typed events with typed role-bindings. If nothing else survives the wonder-tale genre restriction, that skeleton does.

## Sources

- Propp, Vladimir. *Morphology of the Folktale*. 2nd ed. Translated by Laurence Scott, revised by Louis A. Wagner. Austin: University of Texas Press, 1968. **[Primary translation — not yet read.]**
- Propp, Vladimir. *Theory and History of Folklore*. Translated by Ariadna Martin and Richard Martin. Minneapolis: University of Minnesota Press, 1984. **[Propp's later essays, including his response to Lévi-Strauss — not yet read.]**
- Lévi-Strauss, Claude. "Structure and Form: Reflections on a Work by Vladimir Propp." 1960. **[Major critique — not yet read; Propp responded to it directly.]**

*Function-number count (31) and sphere count (7) are well-established. Specific function names vary slightly between translations and summaries.*
