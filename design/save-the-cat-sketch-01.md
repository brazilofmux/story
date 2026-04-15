# Save the Cat dialect — sketch 01

**Status:** draft, active
**Date:** 2026-04-15
**Supersedes:** nothing (new dialect)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md)
**Superseded by:** nothing

## Purpose

Second upper-dialect sketch under architecture-sketch-02's stack, after
[dramatic-sketch-01](dramatic-sketch-01.md). Written on the dialect's
own terms without reaching for substrate vocabulary; same discipline as
the Dramatic sketch (events, props, folds, identities, rules are not
mentioned). The dialect earns its shape by being coherent standalone
before connective machinery (Lowerings, verifiers) is added.

The Save the Cat dialect captures Blake Snyder's 15-beat structural
framework as taught in *Save the Cat!* (2005). It is far more
prescriptive than the Dramatic dialect: where Dramatic treats Throughline
counts and Argument structure as variable, Save the Cat asserts that
*every* commercial story has 15 beats in a specific order at specific
proportional positions. That prescriptivism is the dialect's value
proposition for the on-ramp use case: a writer who already knows Save
the Cat will recognize the structure immediately.

## Why this dialect

Three reasons:

1. **Multi-dialect architecture validation.** architecture-sketch-02
   commits to dialects being plural; until now only Dramatic exists.
   A second, structurally different upper dialect tests the architecture
   for real. Save the Cat is structurally different from Dramatic in a
   useful way: beat-driven where Dramatic is role-driven, prescriptive
   where Dramatic is parameterized, page-positioned where Dramatic uses
   abstract narrative_position.

2. **Familiar on-ramp.** Most working commercial writers know Save the
   Cat. Most do not know Dramatica or its terminology. Familiar surface
   reduces the threshold to engage with the verifier output — a writer
   sees *Catalyst* / *Break Into Two* / *Midpoint* and knows what's
   being claimed without looking up the term.

3. **Coverage of commercial-screenplay shape.** Dramatic encodes well
   for stage tragedy, classical narrative, literary fiction. Save the
   Cat encodes well for the modern commercial three-act feature, the
   genre Snyder targets. Together they cover more authorial territory
   than either alone.

## What this sketch specifies

- Record types for Save the Cat's structural elements: the 15 Beats,
  the optional Genre classification, A and B Story strands, and a Story
  root.
- The relation between the 15 fixed beat *slots* and an encoding's
  authored beats (every story is *expected* to fill all 15; the verifier
  surfaces unfilled slots as observations, not errors).
- Page targets as the dialect's positional coordinate (analogous to
  Dramatic's `narrative_position` but with concrete proportional
  meaning: page 12 of 110 ≈ beat at the 11% mark).
- Genre as a prescriptive Template carrying genre-specific archetypes
  and beat-meanings. (Initial sketch: 10 genres named, structure carried
  by the genre's Template; per-genre beat semantics deferred unless a
  forcing function appears.)
- The thematic claim (the *Theme Stated* beat's content) as a Story-
  level field, parallel to Dramatic's Argument.
- A self-verifier (M8-equivalent for Save the Cat) checking beat
  completeness, beat-position uniqueness, page-target ordering, and
  genre conformance.

## Commitments

### S1. The 15 beats are canonical

Save the Cat asserts that every commercial story has these 15 beats in
this order. The dialect treats them as a fixed list of slots:

1. Opening Image
2. Theme Stated
3. Set-Up
4. Catalyst
5. Debate
6. Break Into Two
7. B Story
8. Fun and Games
9. Midpoint
10. Bad Guys Close In
11. All Is Lost
12. Dark Night of the Soul
13. Break Into Three
14. Finale
15. Final Image

Each authored beat carries a `slot` field naming which canonical beat
it fills. Two beats may share a slot if the author wants to express
that the slot lands across multiple discrete moments (rare; surfaces
as an observation, not an error).

### S2. Page targets are the dialect's position coordinate

Snyder's framework assumes a 110-page screenplay and gives target page
numbers for each beat (Catalyst = page 12, Break Into Two = page 25,
Midpoint = page 55, etc.). The dialect carries these as `page_target`
on each canonical beat, with `page_actual` on the authored beat for
where the author placed it.

For non-screenplay encodings (novels, short stories, plays), page
targets are interpreted proportionally — Catalyst at "the ~11% mark."
The dialect doesn't enforce 110-page conformance.

### S3. A Story and B Story are first-class strands

Save the Cat distinguishes the *A story* (the external plot) from the
*B story* (typically the romance / spiritual / relationship arc that
embodies the theme). The dialect carries `StcStrand` records for each;
beats may advance one or both.

The B Story beat at slot 7 is by convention where the B story is
introduced. The dialect doesn't enforce this; a verifier check can.

### S4. Theme is a Story-level field

The *Theme Stated* beat traditionally carries a literal line of dialogue
stating the story's thematic claim ("greed is bad"; "love conquers all").
The dialect promotes the theme to a Story-level field
(`Story.theme_statement`), so it can be referenced from elsewhere
without parsing the beat content. The Theme Stated beat itself can
mention how the theme is dramatized.

### S5. Genre is a Template (prescriptive, optional)

Snyder names ten genres (Monster in the House, Golden Fleece, Out of
the Bottle, Dude with a Problem, Rites of Passage, Buddy Love,
Whydunit, Fool Triumphant, Institutionalized, Superhero), each with
distinct archetypes and beat-flavor. The dialect carries `StcGenre` as
a Template-shaped record; a Story optionally declares
`stc_genre_id`. If declared, a self-verifier checks the encoding
against the genre's required archetypes (`genre.archetypes`).

The initial sketch ships the ten genre records as data only — names,
descriptions, archetype labels — without per-genre beat semantics.
Per-genre beat-meanings are deferred until a concrete encoding pressures
them.

### S6. Self-verifier scope

The Save the Cat self-verifier (analogous to Dramatic's M8) runs only
within Save the Cat vocabulary. It does not look at substrate or other
dialects. It checks:

- All 15 beat slots are filled. Unfilled slots surface as
  `severity=advises-review` observations (the encoding is still usable;
  some authors use the dialect partially while drafting).
- No two authored beats share a slot (or, if they do, an observation
  surfaces noting the duplication — not an error, see S1).
- `page_actual` values on authored beats are monotonically increasing
  in slot order. A beat authored later in the slot order with an
  earlier page is an `advises-review` observation.
- If `stc_genre_id` is set, the genre's required archetypes are present
  in the encoding.
- `theme_statement` is non-empty (advisory).

### S7. Description surface inherited

Following dramatic-sketch-01 M10's intent, Save the Cat records are
description-anchorable in the same way Dramatic records are. (The actual
Description-on-Dramatic-records surface is itself sketched-but-not-yet-
implemented; this commitment matches that future state, not current
implementation.)

### S8. Connective relations out of scope

Lowering and cross-boundary verification (Save the Cat → substrate,
Save the Cat → Dramatic) are architecture-sketch-02's concern and
out of scope here. This sketch specifies the dialect alone. A
companion `lowering-sketch-03` (or per-encoding `_lowerings.py`) would
exercise the connective machinery once an encoding lands.

## Worked example: Macbeth

A future `macbeth_save_the_cat.py` would encode Shakespeare's *Macbeth*
against the Save the Cat dialect. Sketched mapping:

| Slot | Beat | Macbeth content |
|---|---|---|
| 1 | Opening Image | The heath; storm; the witches |
| 2 | Theme Stated | "Fair is foul, and foul is fair" |
| 3 | Set-Up | Macbeth as loyal thane; Duncan as king; the marriage |
| 4 | Catalyst | The witches' first prophecy |
| 5 | Debate | Macbeth's hesitation; Lady Macbeth's pressure |
| 6 | Break Into Two | The decision to kill Duncan |
| 7 | B Story | The marriage's moral entanglement |
| 8 | Fun and Games | Murder of Duncan; framing the guards; ascension |
| 9 | Midpoint | The coronation; the false stability |
| 10 | Bad Guys Close In | Banquo's murder; banquet ghost; second prophecy |
| 11 | All Is Lost | Lady Macbeth dies |
| 12 | Dark Night of the Soul | "Tomorrow and tomorrow" soliloquy |
| 13 | Break Into Three | Birnam Wood moves |
| 14 | Finale | Macduff confrontation; the prophecy collapses; death |
| 15 | Final Image | Malcolm crowned |

The mapping is not perfect — *Macbeth* predates Snyder by four centuries
and the *B Story* fits awkwardly on a marriage that is itself the
catalyst of the moral collapse. That awkwardness is a feature of the
worked example: it shows where Save the Cat's commercial-feature
template strains against pre-modern tragedy. A future Lowering exercise
will surface those strains as observations.

## Open questions

- **Per-genre beat semantics.** Snyder's genres each have distinct beat
  meanings (a *Monster in the House* Catalyst is not a *Buddy Love*
  Catalyst). The initial implementation treats genres as labels with
  archetypes; per-genre beat-flavor would require either subclassing
  the beats or carrying a `genre_specific_meaning` field. Defer until
  a forcing function appears.
- **A/B story enforcement.** Snyder's framework strongly implies the B
  story is introduced at slot 7 and resolves alongside the A story.
  The dialect could enforce this (B-story-first-mention requires
  slot ≤ 7) or carry it as an authored relationship. Initial sketch:
  carry it as a relationship between strand and beat; let the verifier
  observe rather than enforce.
- **Multi-act variants.** Some Save the Cat practitioners use a
  variant with sub-beats (e.g., "the Promise of the Premise" within
  Fun and Games). Defer.
- **The "save the cat" beat itself.** Snyder's namesake — an early
  scene establishing the protagonist as someone the audience roots for
  — is conventionally part of the Set-Up beat, not its own slot.
  Initial sketch follows this convention.

## What's next after this sketch

If the dialect ships and an encoding lands, the natural follow-ons:

1. `lowering-sketch-03` exercising the cross-dialect coupling for a
   Save the Cat encoding (likely Macbeth, since the substrate already
   exists).
2. A per-encoding verifier registry parallel to `macbeth_verification.py`
   for the Save the Cat encoding.
3. Comparison of the same story encoded at both dialects (Macbeth at
   Dramatic + Macbeth at Save the Cat), surfacing what each dialect
   captures and what it misses. The architecture-sketch-02 multi-dialect
   commitment becomes empirical at that point.
