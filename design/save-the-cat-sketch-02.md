# Save the Cat dialect — sketch 02 (StcCharacter amendment)

**Status:** draft, active
**Date:** 2026-04-16
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [save-the-cat-sketch-01.md](save-the-cat-sketch-01.md) — commitments S1–S8 unchanged
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md), [dramatic-sketch-01.md](dramatic-sketch-01.md)
**Related:** [cross-dialect-macbeth-sketch-01.md](cross-dialect-macbeth-sketch-01.md), [cross-dialect-ackroyd-sketch-01.md](cross-dialect-ackroyd-sketch-01.md)
**Superseded by:** nothing yet

## Purpose

Close the StcCharacter gap flagged as an open question after Macbeth
and pressed harder by Ackroyd: the Save the Cat dialect currently
names zero character records, so structural claims about who plays
what role in the story cannot be expressed at the dialect layer.

The gap's clearest consequence is the Ackroyd encoding: Sheppard's
entire novel pivots on *which character is the killer*, and the
dramatic-layer `C_sheppard` with `function_labels=("Antagonist",)` +
ownership of `T_mc_sheppard` makes that structural claim visible.
The Save the Cat encoding carries the same claim only implicitly —
Sheppard is "a person referenced in beat descriptions." No role
label, no verification check can reach him.

This sketch adds five commitments (S9–S13) that introduce a minimal
StcCharacter record, canonical role labels, reference wiring from
beats and strands, optional archetype-to-character assignment on the
Story, and three new verifier checks. Commitments S1–S8 from
sketch 01 are unchanged.

## Scope — what this sketch does and doesn't do

**In scope:**

- A character record record type with a small set of fields.
- Role labels as a canonical-plus-open vocabulary.
- Wiring: StcBeat may name participant characters; StcStrand may
  name a focal character; StcStory aggregates characters and
  archetype assignments.
- Verifier checks for id resolution, single-protagonist advisory,
  and archetype-coverage.
- Encoding migrations for `macbeth_save_the_cat.py` and
  `ackroyd_save_the_cat.py` to author their characters.

**Out of scope:**

- Character-character relations (adversary-of, ally-of, mentor-to,
  etc.). Deferred; carry as prose descriptions for now.
- Per-character arcs (Snyder's *wants vs needs*; the B-story
  character's transformation). Deferred until a third encoding
  presses it.
- Cross-boundary verifier changes at the Save the Cat → substrate
  boundary. This amendment is within-dialect only; a follow-on
  pass can extend the existing save_the_cat_verification modules
  to consume the new records.
- Integration with Dramatic's `Character.function_labels`. The
  two dialects name their own characters independently per
  architecture-sketch-02; mapping between them is a Lowering
  concern, not a sketch-02 concern.

## Commitments

### S9 — StcCharacter is a new authored record type

```python
@dataclass(frozen=True)
class StcCharacter:
    id: str
    name: str
    description: str = ""
    role_labels: Tuple[str, ...] = ()
    authored_by: str = "author"
```

The record is deliberately minimal. `role_labels` is a tuple (not a
set) to preserve author intent when the same character carries
multiple overlapping roles — the Ackroyd case where Sheppard is
`("protagonist", "antagonist", "narrator")`.

The record is **optional**. A Save the Cat encoding that chooses
not to author characters continues to self-verify; the verifier's
new checks only activate if the Story declares `character_ids` or
`archetype_assignments`.

### S10 — Role labels are canonical-plus-open

The dialect ships a small **canonical** set of role labels that
the verifier recognizes and the walker can group by:

- `"protagonist"`, `"antagonist"` — the two structural poles most
  beats reference
- `"love-interest"` — per the B-story convention
- `"mentor"`, `"confidant"`, `"ally"` — common support roles
- `"narrator"` — first-person / frame narrator; load-bearing on
  unreliable-narrator encodings
- `"victim"`, `"suspect"` — carry weight in Whydunit and
  Institutionalized
- `"threshold-guardian"` — Snyder's term for the obstacle at
  Break Into Two

Per-genre archetypes (e.g., Whydunit's `"the detective"`, `"the
secret"`, `"the dark turn"`) are valid role labels when the
Story's genre lists them. Open strings (any author-introduced
label) are admissible.

**The canonical set is recognized, not required.** A character
without any canonical label is not an error; a character with
only an open-string label is not an error. The verifier uses the
canonical labels for its one-protagonist advisory and for
matching against genre archetypes.

### S11 — Reference wiring on beats, strands, and story

Three reference additions, all optional (default empty):

- `StcBeat.participant_ids: tuple = ()` — characters present in
  the beat. Parallels the existing `advances: tuple[StrandAdvancement, ...]`
  field (strand-level advances + character-level participants).
- `StcStrand.focal_character_id: Optional[str] = None` — the one
  character the strand is structurally about. A story may have an
  A strand whose focal character is the protagonist and a B strand
  whose focal character is the love interest; Snyder's framework
  leans this way.
- `StcStory.character_ids: tuple = ()` — the Story's authoritative
  list of characters. Parallels the existing `beat_ids` and
  `strand_ids`.

The three references are independent. An encoding may author
characters and name them in `StcStory.character_ids` without
wiring them into beats or strands; this surfaces as a "character
unreferenced" observation (advisory — authors sometimes declare
cast up front and wire in later).

### S12 — Archetype assignments bind genre archetypes to characters or prose

When a Story declares a genre (`stc_genre_id`), the genre's
`archetypes` tuple (Whydunit's three, Monster-in-the-House's three,
etc.) becomes a set the encoding is expected to address — each
archetype either lands on a character or is acknowledged as
non-character content.

```python
@dataclass(frozen=True)
class StcArchetypeAssignment:
    archetype: str              # must be in the declared genre's archetypes
    character_id: Optional[str] = None
    note: str = ""
```

`character_id` names an StcCharacter when the archetype is a
person (Whydunit's `"the detective"` → Poirot). `note` names the
archetype's content when it isn't a person (Whydunit's
`"the secret"` → "Sheppard's identity as Mrs. Ferrars's blackmailer
and Ackroyd's killer"). Exactly one of the two must be set per
assignment; the verifier checks this.

The Story's `archetype_assignments: tuple[StcArchetypeAssignment, ...]`
collects all assignments. Each archetype in the genre may appear
zero or one times in `archetype_assignments`; the verifier
surfaces missing archetypes as advisory ("did you mean for this
to be unassigned, or to bind it to a character or prose note?").

### S13 — Three new verifier checks

The S6 self-verifier gains three checks, all **observational**
(never error-raising) per sketch-01 S6's discipline:

1. **Character-id resolution.** Every id named in
   `StcBeat.participant_ids`, `StcStrand.focal_character_id`,
   `StcStory.character_ids`, and
   `StcArchetypeAssignment.character_id` must resolve in the
   characters collection. Unresolved ids advise-review.
2. **One-protagonist advisory.** Exactly zero or one character
   carrying `"protagonist"` in `role_labels` is the expected
   shape. Multiple protagonists advise-review (admissible —
   ensemble stories exist — but worth flagging). Zero
   protagonists is noted (informational).
3. **Archetype coverage.** If the Story declares a genre with
   archetypes, every archetype in `genre.archetypes` should
   appear in exactly one `archetype_assignments` entry. Missing
   archetypes advise-review; duplicated archetypes advise-review;
   extraneous archetypes (not in the genre's list) advise-review.
   Each assignment must have exactly one of `character_id` /
   `note` set; the other-one-or-both-set advise-review.

No existing check is modified. S6's verifier surface grows; its
semantics don't.

## Worked case — Ackroyd under S9–S13

The Ackroyd encoding gets eight StcCharacter records; the load-
bearing one is Sheppard:

```python
C_sheppard = StcCharacter(
    id="C_sheppard",
    name="Dr. James Sheppard",
    description=(
        "the village doctor; first-person narrator; Ackroyd's "
        "confidant and the novel's killer. The role overlap is "
        "the structural engine: the protagonist of the narrative "
        "(the voice we inhabit) is simultaneously its antagonist "
        "(the concealed killer whose reveal the plot works "
        "toward)."
    ),
    role_labels=("protagonist", "antagonist", "narrator"),
)
```

`C_poirot` carries `("the detective",)` — the Whydunit archetype
role label, bound to the character via the Story's
`archetype_assignments`. `C_ackroyd` carries `("victim",)`.
`C_flora`, `C_ralph`, `C_ursula`, `C_caroline`, `C_raglan`,
`C_parker` carry role labels drawn from the canonical set plus
the Whydunit's suspect pool.

`STORY.archetype_assignments`:

- `StcArchetypeAssignment(archetype="the detective", character_id="C_poirot")`
- `StcArchetypeAssignment(archetype="the secret", note="Sheppard's identity as Mrs. Ferrars's blackmailer and Ackroyd's killer; concealed from Poirot and the household until τ_s=8")`
- `StcArchetypeAssignment(archetype="the dark turn", note="the drawing-room reveal + Poirot's private mercy + Sheppard's suicide as the novel's concluding sequence")`

All three archetypes covered. The first binds to a character;
the other two carry prose notes because they aren't people — the
genre's archetypes legitimately split character/non-character.
The verifier reports coverage clean.

**Beat wiring** is light by default; beats that name specific
characters in their existing `description_of_change` text gain
`participant_ids`. For Ackroyd, the reveal beat:

```python
B_14_finale = StcBeat(
    id="B_14_finale",
    slot=14,
    ...
    participant_ids=("C_poirot", "C_sheppard", "C_flora",
                     "C_ralph", "C_raglan", "C_caroline"),
)
```

**Strand focal characters.** `Strand_A_case.focal_character_id =
"C_poirot"` (the investigator drives the A story).
`Strand_B_flora_ralph.focal_character_id = "C_flora"` (Flora's
belief is the B story's engine).

## Worked case — Macbeth under S9–S13

Macbeth's genre is Rites of Passage, whose archetypes are
`"the life problem"`, `"the wrong way"`, `"the acceptance"`. None
of these is cleanly a character — they're internal stages. All
three archetype assignments carry prose notes:

- `archetype="the life problem"` → "Macbeth's ambition + the
  witches' prophecy creating a future he must either accept or
  refuse"
- `archetype="the wrong way"` → "the regicide of Duncan and the
  cascade of defensive killings that follow"
- `archetype="the acceptance"` → "the 'tomorrow and tomorrow'
  recognition of what he has become"

Macbeth's characters get the standard canonical labels. The
interesting case is the antagonist — Macbeth's encoding admits
multiple candidates (Lady Macbeth, the Witches, Macduff, Macbeth
himself in the self-destruction sense). The S10 tuple of
`role_labels` accommodates: Macduff carries `("antagonist",)` as
the structural opponent who ends the arc; Lady Macbeth carries
`("ally", "threshold-guardian")` for her catalyzing role; the
Witches carry `("mentor",)` in an ironic/malign sense or an open
label like `"oracular-catalyst"` if the author prefers.

**The archetype-coverage check is the central new affordance on
Macbeth.** It surfaces the structural claim the Dramatic dialect
already makes: Macbeth's Rites-of-Passage reading is
internalized; the archetypes don't bind to characters by design;
the encoding declares this honestly via prose notes rather than
leaving the archetypes unassigned. This is what "Save the Cat
fits pre-modern tragedy imperfectly" (cross-dialect-macbeth's
central finding) looks like structurally.

## Verifier behavior under S13

Expected observations on the two migrated encodings:

- **Macbeth**: previous observations (1 noted:
  `genre_archetypes_declared`) + 0 from S13 checks (all
  archetypes assigned via notes; no unresolved character ids;
  one protagonist — Macbeth — carrying that canonical label).
  Equivalent pass.
- **Ackroyd**: previous observations (1 noted:
  `genre_archetypes_declared`) + 0 from S13 checks (archetype
  coverage clean with one character binding and two prose notes;
  one protagonist — Sheppard — even though he also carries
  antagonist; no unresolved references). Equivalent pass.

Synthetic-fixture tests in `test_save_the_cat.py` pin each new
check's observation codes directly, independent of the encodings.

## What S9–S13 does not change

- The 15 canonical beats (S1).
- Page-target positional coordinate (S2).
- A/B story strands (S3).
- Story-level theme statement (S4).
- Genre as Template-shaped data (S5).
- Self-verifier-as-observations-never-errors (S6).
- Description-surface inheritance (S7).
- Out-of-scope for connective relations (S8).

The S6 verifier surface grows by three checks; its shape
(observations grouped by severity / code; no check rejects a
Story) is unchanged.

## Open questions

1. **Character-character relations.** The amendment doesn't model
   adversary-of / ally-of / mentor-to relations between
   characters. A sketch 03 would pick this up if a forcing
   function appears — e.g., a verifier check that wants to
   assert "the protagonist's antagonist-relation resolves at
   slot 14."

2. **Character arcs.** Snyder's "wants vs needs" framing maps to
   a character's internal trajectory across the 15 beats. The
   amendment doesn't carry a per-character arc record. If a
   future encoding wants to verify that the protagonist's *need*
   is articulated by the B-story focal character and resolved in
   the Finale, a sketch 03 would specify the record.

3. **Cross-boundary StcCharacter ↔ substrate Entity.** Lowering
   from StcCharacter to substrate Entity is the obvious
   connective move; save-the-cat-sketch-01 S8 kept this out of
   scope. A later exercise ("stc-lowerings"-style modules) can
   exercise the coupling against Macbeth and Ackroyd; the
   cross-dialect Ackroyd sketch already flags the Poirot ↔
   `poirot` correspondence as load-bearing.

4. **Role-label taxonomy stability.** The canonical set in S10
   is nine labels. Rehashing this vocabulary every time a new
   encoding lands is a drift risk. A sketch 03 or an encoding
   that presses the vocabulary (serial / ensemble / non-Western
   form) is the natural home to stabilize or expand.

5. **Multi-protagonist stories.** The one-protagonist check is
   advisory, not restrictive — but it pushes against ensemble
   forms (heist, institutional drama). Whether ensemble belongs
   as a tenth genre or as an explicit multi-protagonist
   declaration on the Story is a sketch-01 S5 / sketch-02 S10
   tension worth revisiting when an ensemble encoding lands.

## Implementation brief

Concrete changes, in order of landing:

1. **`save_the_cat.py`** — add `StcCharacter`,
   `StcArchetypeAssignment`, `CANONICAL_ROLE_LABELS` constant;
   extend `StcBeat` / `StcStrand` / `StcStory` with the optional
   reference fields; add three new check functions to the S6
   verifier and wire them into `verify()`.
2. **`macbeth_save_the_cat.py`** — author 8 StcCharacter records
   (Macbeth, Lady Macbeth, Duncan, Banquo, Macduff, Malcolm, the
   Witches, Ross); add `character_ids` and
   `archetype_assignments` to `STORY`; optionally wire
   `participant_ids` on a handful of beats where the identities
   are load-bearing.
3. **`ackroyd_save_the_cat.py`** — author 8 StcCharacter records
   (Sheppard, Poirot, Ackroyd, Flora, Ralph, Ursula, Caroline,
   Raglan); Sheppard carries the three-label overlap the sketch
   names; add `character_ids` and `archetype_assignments`;
   wire `participant_ids` on the reveal and finale beats;
   set strand `focal_character_id`s.
4. **`test_save_the_cat.py`** — synthetic-fixture tests for each
   new record type and check; integration tests against both
   migrated encodings pinning the "no new adverse observations"
   contract.

Expected test count: 30 synthetic tests currently pin S1–S8; the
amendment adds roughly 12–15 (record construction, canonical
labels, each verifier observation code, one-protagonist edge
cases, archetype-coverage edge cases, integration pins on the
two encodings). Final test_save_the_cat.py count: ~45.

## Summary

- StcCharacter gap closed with a minimal record (S9), a canonical
  role-label vocabulary that doesn't restrict authoring (S10),
  optional reference wiring that existing encodings can adopt
  incrementally (S11), genre archetype assignments that force
  the Whydunit-vs-Rites-of-Passage contrast into view (S12), and
  three new verifier checks (S13).
- Sheppard's MC-Antagonist-Narrator overlap becomes expressible:
  `role_labels=("protagonist", "antagonist", "narrator")` on a
  single character. The structural claim Ackroyd's Dramatic
  encoding makes via `C_sheppard` + function_labels is now
  reachable from the Save the Cat dialect.
- Macbeth's Rites-of-Passage archetype-as-internal-stages honest
  representation: archetypes bind via `note` rather than
  `character_id` — the verifier sees "genre-native archetype
  structure has prose content, not character content" as a
  structural claim, not a gap.
- S1–S8 unchanged. The sketch-01 dialect continues to be the
  basis; sketch-02 extends rather than supersedes.
