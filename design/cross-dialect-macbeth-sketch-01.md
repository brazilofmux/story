# Cross-dialect comparison — Macbeth — sketch 01

**Status:** draft, active
**Date:** 2026-04-15
**Supersedes:** nothing (new kind of sketch)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md), [dramatic-sketch-01.md](dramatic-sketch-01.md), [save-the-cat-sketch-01.md](save-the-cat-sketch-01.md)
**Superseded by:** nothing

## Purpose

architecture-sketch-02 commits to the dialect layer being plural: the
substrate is single and load-bearing, but the upper-dialect layer is
open-ended, holding as many dialects as story traditions we care to
encode. That commitment has been hypothetical until now — only the
Dramatic dialect existed, and a single-dialect claim of pluralism is
not evidence.

Two things changed in April 2026:

- `save-the-cat-sketch-01` landed the second dialect (Blake Snyder's
  15-beat commercial-screenplay framework).
- `prototype/macbeth_save_the_cat.py` landed a second upper-dialect
  encoding of the same play already encoded in `macbeth_dramatic.py`.

For the first time, the architecture's multi-dialect claim is
empirically testable: one play, two dialects, two self-verifiers both
running clean. This sketch is the audit that comparison produces.

The goal is not to rank the dialects. The goal is to name precisely
what each dialect captures about Macbeth that the other does not, so
that future design decisions (which dialect to add next; which record
types to port across; what a third dialect should bring that neither
has) are grounded in concrete expressive-power findings rather than
impression.

## Method

Both `macbeth_dramatic.py` and `macbeth_save_the_cat.py` were authored
against their respective dialect sketches without trying to make the
two encodings parallel. Each encoding is the best reading the dialect
supports of the same play (Shakespeare's *Macbeth*, no adaptation,
same source material on both sides). Differences between them are
dialect-driven, not authorial-preference-driven.

Both encodings' self-verifiers run with zero adverse observations:

- Dramatic: 0 observations (all dramatica-8 slots filled, all
  throughlines have stakes, no orphans).
- Save the Cat: 1 observation, severity `noted`,
  code `genre_archetypes_declared` (informational; no structural
  concern).

That both encodings pass cleanly is itself a finding: the dialects'
self-consistency checks do not prefer either encoding's shape. Any
asymmetry between them is expressive, not diagnostic.

## What each dialect records

### Dramatic: 6 authored record types, 57 records on Macbeth

| Record type | Count | What it names |
|---|---|---|
| Argument | 1 | the story's central claim + its counter-premise |
| Throughline | 4 | the four role-locus arcs (OS, MC, IC, Relationship) |
| Character | 9 | the full cast, with 6 carrying Dramatica functions |
| Scene | 14 | authored dramatic moments with conflict_shape / result |
| Beat | 25 | per-throughline progression (5/9/5/6 distribution) |
| Stakes | 4 | separable per-throughline stakes records |

### Save the Cat: 2 authored record types, 17 records on Macbeth

| Record type | Count | What it names |
|---|---|---|
| Strand | 2 | the A story (political) and B story (marriage) |
| Beat | 15 | one per canonical slot (1..15), page-positioned |

(Story declares `theme_statement` directly — it's a field, not a
separate record. Genre is dialect-shipped data: the Story references
`rites-of-passage` from the ten ship-with-the-dialect genres, but
no `StcGenre` record is *authored* by the Macbeth encoding.)

A ratio of roughly 3:1 in record count at the same play. The
immediate implication is not that Dramatic is "more detailed" — it's
that Dramatic's schema demands more authored choices per encoding.
Save the Cat's prescriptivism means fewer choices are open: the 15
beats are fixed, positions are canonical, the archetype layer is
carried by the Genre template.

## What each dialect captures that the other cannot

### Dramatic captures, Save the Cat does not

- **Characters, individually.** Save the Cat has no `Character`
  record type. Macbeth, Lady Macbeth, Macduff, Banquo, Malcolm, the
  Witches, Duncan, Lady Macduff, Fleance all exist in the Save the
  Cat encoding only as prose in `description_of_change` strings. In
  Dramatic they are first-class records with function assignments.

- **Character functions (Protagonist / Antagonist / …).** The
  dramatica-8 role assignment — the encoding's thesis that Macduff is
  Antagonist, Lady Macbeth is Contagonist, the Witches are Guardian —
  simply has no expression in Save the Cat. Genre archetypes ("the
  life problem", "the wrong way", "the acceptance") are Save the
  Cat's nearest analog, but they're abstract labels attached to the
  genre template, not role assignments on specific authored characters.

- **Arguments with counter-premise.** Dramatic's
  `A_ambition_unmakes` carries both the premise and the
  counter-premise ("ambition is what elevates; restraint is passive").
  Save the Cat's Theme Stated records only the literal line ("Fair is
  foul, and foul is fair") — a slogan, not a thesis with a
  documented opposition. Dramatic's Argument is designed for the
  encoding to be self-aware about what it's *arguing against*.

- **Separable Stakes records.** Dramatic's 4 Stakes records name
  Macbeth's soul, Scotland's order, Lady Macbeth's sanity, and the
  marriage's existence as four distinct things at risk. Save the Cat
  has no Stakes record type; what's at stake is implicit in the B
  story's description and in the descriptions of individual beats.

- **Per-throughline progression.** Dramatic's 25 beats are
  distributed across four throughlines: Macbeth's moral descent has
  9 beats, the marriage has 6, Scotland has 5, Lady Macbeth has 5.
  Each throughline has its own inciting / rising / midpoint / climax /
  denouement shape. Save the Cat collapses all of this to a single
  15-beat axis: there is only one midpoint for the whole story, not
  one per locus.

- **Scenes with authored conflict and result.** Dramatic's Scene
  record carries `conflict_shape` and `result` — the scene is named
  and its dramatic contribution articulated independently of the beats
  it advances. Save the Cat has no Scene analog: the equivalent
  information is flattened into beat descriptions. The banquet ghost
  is a Scene in Dramatic ("a king hosts a feast; the murdered friend
  appears at the table; the king cracks publicly; the queen covers")
  but is a sub-detail inside Save the Cat's slot-10 description.

### Save the Cat captures, Dramatic does not

- **Opening Image / Final Image symmetry as a first-class concern.**
  Save the Cat's slots 1 and 15 assert that the play's first moment
  and last moment mirror each other — in Macbeth, supernatural
  disorder (heath + storm) inverted into political order (Malcolm
  crowned). Dramatic has no such slot; the Macbeth Dramatic encoding
  has 14 Scenes, the first of which is the prophecy, not the storm.
  The Witches' opening is simply absent from Dramatic's Macbeth.

- **Theme Stated as literal dialogue.** Save the Cat promotes the
  actual spoken line ("Fair is foul, and foul is fair") to a
  structural slot; the Theme Stated beat's job is to dramatize the
  theme through character speech. Dramatic's Argument describes the
  claim conceptually ("unchecked ambition unmakes the one who indulges
  it") but does not ask the encoding to name where in the play the
  theme is verbally stated.

- **A-story / B-story strand distinction.** Save the Cat separates
  the external plot (political: regicide → tyranny → restoration) from
  the internal / relational plot (the marriage's conspiracy → unity →
  isolation → grief) as two named strands, with each beat declaring
  which strand(s) it advances. In Dramatic, the four throughlines are
  role-shaped (OS / MC / IC / Relationship), not plot-shaped (external
  / internal). The difference matters: Dramatic asks "whose perspective
  is this moment?" and Save the Cat asks "which of the two arcs is
  this moment advancing?" These are not the same partition.

- **Proportional position (page targets).** Save the Cat's
  `page_actual` places each beat proportionally against a canonical
  110-page sheet; monotonic ordering is checked by the self-verifier.
  Dramatic's `narrative_position` on Scenes is an ordinal index
  (1..14) with no dimensional meaning — scene 7 is between scenes 6
  and 8, but there is no commitment to "scene 7 is at the 50% mark
  of the story". Save the Cat's proportionality is a structural
  claim; Dramatic's ordering is topology-only.

- **Genre as a prescriptive template.** Save the Cat names 10
  genres, each carrying archetypes the encoding is checked against.
  Macbeth's Save the Cat encoding declares `rites-of-passage`, which
  carries "the life problem", "the wrong way", "the acceptance" as
  archetype labels. Dramatic has a character-function template
  (dramatica-8) but no story-genre template; the story's genre is
  not a Dramatic concept.

- **Prescriptive skeleton.** The 15 beats are not optional in Save
  the Cat; they are mandatory, in order, at target positions. The
  self-verifier treats a missing slot as a surfaceable observation,
  not a design choice. Dramatic's shape is parameterized: the
  dramatica-8 template is one of possibly many character-function
  templates, Argument count is variable, Throughline count depends
  on the template. A Save the Cat encoding tells you what shape to
  expect before any content is authored; a Dramatic encoding does
  not.

## Where the dialects agree

Both dialects:

- have a Story root record aggregating the encoding
- carry beats as the smallest unit of dramatic change
- have a notion of the play's arc having a **Midpoint** (Dramatic as
  a `beat_type`, Save the Cat as a canonical slot name)
- verify without looking outside the dialect (S6 of Save the Cat, M8
  of Dramatic — both scope to in-dialect checks only)
- treat verification as advisory, not gatekeeping (all observations
  are `noted` / `advises-review`, never errors)
- are silent about substrate; the connective machinery belongs to
  Lowerings, not to the dialect

Both dialects *could* be extended to carry the other's distinctive
features, but that would be a schema change, not a verifier change.

## The compression pattern: slot 10

Save the Cat's slot 10 (`Bad Guys Close In`) collapses four distinct
Dramatic Scenes into one beat:

| Dramatic Scene | Position | Save the Cat slot |
|---|---|---|
| S_banquo_killing | narrative_position=6 | slot 10 |
| S_banquet_ghost | narrative_position=7 | slot 10 |
| S_second_prophecy | narrative_position=8 | slot 10 |
| S_macduff_family | narrative_position=9 | slot 10 |

This is not an authorial choice; it is the dialect's prescriptive
ceiling showing. Save the Cat allocates one slot to the
rising-action-and-complications block, Dramatic has no such allocation
constraint and splits the same dramatic territory into four authored
scenes. A reader wanting to talk about "the banquet ghost moment"
separately from "the Macduff family slaughter" can do so in Dramatic
directly; in Save the Cat, they must either drop into the beat's
description prose or author multiple beats per slot (which the
dialect admits per S1 but the self-verifier notes).

The symmetric observation: Save the Cat's slot 3 (Set-Up) and slot 8
(Fun and Games) each compress multiple Dramatic-side events. The
compression is not localized to any one phase; it is a general feature
of Save the Cat's coarser granularity.

## What this finding means for the architecture

- **Neither dialect is a superset of the other.** If the architecture
  wanted to pick a single dialect and retire the other, it would lose
  expressive power in one direction or another. Save the Cat without
  Dramatic loses character and stakes articulation; Dramatic without
  Save the Cat loses opening/final-image symmetry, theme-as-dialogue,
  and prescriptive structural skeleton.

- **The architecture's multi-dialect bet pays out on first examination.**
  architecture-sketch-02's commitment to dialect plurality is not a
  hedge — the two dialects genuinely capture different things about
  the same play. Adding a third dialect (e.g., a long-form / serial
  structure dialect, or a non-Western structural tradition) is
  likely to surface *more* dimensions the existing two miss, not
  fewer.

- **The substrate's role as the coordination layer is reinforced.**
  The substrate is the only representation that can hold both
  dialects' readings at once without choosing sides. Dramatic's
  Scenes and Save the Cat's Beats both ground in substrate events;
  Dramatic's Characters and Save the Cat's Strand-advances both
  reference substrate entities. Lowerings are where the two dialects'
  views meet — which makes the Save the Cat → substrate Lowering work
  (option B from the 2026-04-15 plan) the natural next exercise.

- **Dialect-specific strengths suggest dialect-specific uses.** A
  writer working in commercial screenplay should probably encode at
  Save the Cat; a writer working in stage tragedy should probably
  encode at Dramatic. The architecture does not force one choice for
  all authors. This is load-bearing for the "force humans to do
  their homework" goal: the dialect is the homework's shape, and
  different traditions ask different homework.

## Open questions

- **Should Save the Cat acquire a Character record type?** The
  finding that Save the Cat's Macbeth encoding names zero characters
  is jarring. Save the Cat in practice does not talk this way — real
  writers using the framework think about protagonists and love
  interests explicitly. The dialect may be under-specified; a
  minimal StcCharacter record with optional function-label slots
  (protagonist / love-interest / mentor / antagonist) would bring it
  closer to how the framework is actually used. Deferred pending a
  second Save the Cat encoding to surface whether this is a systematic
  gap or a Macbeth-specific artifact.

- **Should Dramatic acquire an Opening-Image / Final-Image concern?**
  The Witches' heath-opening is a real dramatic moment absent from
  the Macbeth Dramatic encoding — not because the author forgot it,
  but because Dramatic has no slot for "the play's first image as
  such." A Dramatic extension could admit a `frame_scenes` concept
  without adopting Save the Cat's prescriptive skeleton.

- **Are the four 4:1 compression instances (slot 10 especially) a
  general Save the Cat weakness for late-rising-action?** Likely
  yes, given the fixed-slot structure; verifying requires more
  encodings.

- **Does the Dramatic Argument / Save the Cat Theme Stated pair
  suggest a shared underlying record type?** Both name the claim the
  story is making. Dramatic names it conceptually
  (premise / counter-premise); Save the Cat names it verbally
  (literal line). A future normalization could carry both — the
  literal line as `verbal_statement`, the underlying claim as
  `premise`. Deferred.

## What's next

1. **Save the Cat → substrate Lowering** (option B from the
   2026-04-15 plan). Create `macbeth_save_the_cat_verification.py`
   parallel to `macbeth_verification.py`, exercising the
   `COUPLING_DECLARATIONS` already declared in `save_the_cat.py`
   against the substrate. This produces coverage numbers for the
   Save the Cat encoding analogous to the 73 gaps the Dramatic
   encoding now prints, and surfaces where the dialect's
   `claim-moment` / `claim-trajectory` / `characterization`
   couplings actually land.

2. **Second encoding at each dialect.** A non-tragedy (comedy,
   serial, non-Western) would pressure both dialects against material
   they're currently untested on. This is REVIEW.md's next-term item
   #1; it remains the right move once the Save the Cat substrate
   coupling is exercised.

3. **Dialect extension proposals.** The open questions above (Save
   the Cat Character, Dramatic frame-scenes) are candidate dialect
   amendments. Each would need a sketch update (not just a prototype
   change) because the commitment is to the dialect's shape.

4. **A third dialect.** Whatever the third dialect is (a long-form
   arc system, Campbell's monomyth, something non-Western), running
   it through the same comparison exercise on Macbeth — or on the
   next story encoded — is the natural way to keep the architecture's
   pluralism honest.
