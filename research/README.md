# Research

Long-running survey of prior work relevant to building a story-telling engine. Two parallel tracks:

- [`theories/`](theories/README.md) — theories of story structure and narrative (3-act, 5-act, Propp, Campbell, Dramatica, Story Grid, Truby, McKee, Save the Cat, Freytag, and more).
- [`systems/`](systems/README.md) — computational narrative systems, past and present (TALE-SPIN, MINSTREL, Mexica, Scheherazade, Façade, Brutus, LLM-era work).

## Working rules

- **Honest surveys, not cheerleading.** Record what each theory or system *actually* does, where it is coherent, and where it falls apart. "Dramatica is load-bearing but its authors cannot fully explain it" is a real finding and belongs in the entry.
- **Formalizability is a first-class question.** For every theory, the entry must consider: *what would it take to encode this as data + rules an engine could operate on?* If the theory resists formalization, that is a finding too.
- **Cite the primary source.** Secondhand summaries accumulate errors. When we haven't yet read the primary source, mark the entry's claims as tentative.
- **One file per theory / system.** Long-form, permanent, deepened over time. Indexes cross-reference.
- **Cross-cutting notes belong in index READMEs**, not in individual entries.

## Entry templates

See `theories/_template.md` and `systems/_template.md`.
