# Dramatic dialect — sketch 01

**Status:** draft, active
**Date:** 2026-04-14
**Supersedes:** nothing (new dialect)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md)
**Superseded by:** nothing yet

## Purpose

First upper-dialect sketch under architecture-sketch-02's stack.
The Dramatic dialect is a vocabulary for thinking about a story
as an *argument* — what the story is claiming, who embodies which
side of the claim, and how scenes push the argument forward.

This sketch is written in the Dramatic dialect's own terms. It
does not reach for concepts from other dialects in the stack; it
does not describe the dialect as a compilation target for any
lower dialect. The discipline is deliberate: dialects earn their
shape by being coherent on their own terms first. Connective
machinery — lowering relations, cross-boundary verifiers — is
architecture-sketch-02's concern and is outside this sketch's
scope.

The dialect is influenced by Dramatica theory but departs from it
where the author's experience with a broader range of stories
argues for more flexibility. Those departures are enumerated in
*Relation to Dramatica* below.

This sketch specifies:

- The dialect's central records: Story, Argument, Throughline,
  Character, Scene, Beat, Stakes, and Character Function (as a
  template vocabulary).
- The dialect's time concept (narrative position).
- Grid-snap within the dialect: what is structural, what is
  interpretive, what is authored-uncertainty.
- The dialect's description surface (analogous pattern to other
  dialects, realized here in Dramatic terms).
- The dialect's self-verification: coherence checks that operate
  purely within Dramatic vocabulary, independent of any other
  dialect.
- Templates: Dramatica-8, three-actor, two-actor, author-defined.
- A worked example (Oedipus) in Dramatic terms.
- Open questions and expected follow-on sketches.

## What this sketch is *not* committing to

- **How the dialect relates to other dialects in the stack.**
  Lowering relations, cross-boundary verifiers, and composition
  with any lower dialect are architecture-sketch-02 concerns.
  This sketch exists to give the Dramatic dialect a coherent
  standalone shape; how it binds to or compiles through other
  dialects is strictly separate work.
- **Prose-layer concerns.** The dialect operates at the level of
  argumentative structure, not paragraphs, dialogue, or
  rendering. Sentence-level craft is out of scope.
- **A single Dramatica-faithful implementation.** Dramatica has
  specific structural positions (e.g., four throughlines with
  fixed roles, eight character functions, dynamic/static story
  points) that this dialect admits as a *template* without
  treating them as the dialect's requirements.
- **Enforcement of structural completeness.** A story may use
  only part of the dialect — one throughline, no declared
  Argument, no character function template. The dialect's self-
  verifier emits observations on incompleteness; it never rejects
  incomplete stories.
- **Resolution of the Argument via the dialect's own machinery.**
  Whether the Argument "lands" emotionally, whether the resolution
  is earned, whether the theme resonates — these are interpretive
  questions handled by the description surface. The dialect does
  not attempt to adjudicate craft quality.
- **Psychological process theory.** Dramatica's Process / Dynamic
  / Approach / Justification vocabulary is rich and partially
  admissible as template-specific extension, but sketch 01 does
  not incorporate it as dialect-native. If a future Dramatica-
  template sketch wants it, it adds the vocabulary within its
  template declaration.
- **Sequence rhetoric.** How the ordering of scenes shapes the
  reader's understanding of the Argument (suspense, surprise,
  revelation) is a rich topic the dialect acknowledges but does
  not formalize in this sketch. Narrative position (see below)
  is a coarse-grained sequence; finer rhetoric sits in scene
  descriptions for now.

If a question starts with "how does the Dramatic record X lower
into Y?" or "what in the lower dialect realizes this?" — it is
out of scope by construction. This sketch is about Dramatic
records on their own terms.

## What this sketch *is* committing to

1. **M1 — A Story has zero or more Arguments.** An `Argument` is
   a first-class record naming a claim the story interrogates.
   A story may have no Argument (tonal / lyric / mood pieces), a
   single dominant Argument (most conventional dramatic stories),
   or several Arguments in parent/child relationship (polyphonic
   works, novels-of-ideas, multi-thread narratives). The dialect
   does not privilege one count over another.
2. **M2 — Throughlines are roles, not characters.** A
   `Throughline` is a structural role within a Story's argumentative
   shape. A `Character` may fill a Throughline; multiple
   Characters may share one; a Throughline may have no Character
   at all (e.g., an Overall-Situation Throughline owned by a
   community, an era, an institution). Throughlines compose into
   the Argument the story is making.
3. **M3 — Scenes are units of argumentative work.** Each
   `Scene` carries a declared *purpose*: which Throughline it
   advances, which Beat within that Throughline it belongs to,
   and what changes in consequence. Scenes without declared
   purpose are admissible — but the self-verifier surfaces them
   as observations. A Scene's purpose is what distinguishes it
   from incidental material.
4. **M4 — Narrative position is the dialect's time.** Scenes
   occupy positions in an integer-ordered sequence
   (`narrative_position`). Beats within a Throughline are
   ordered (`beat_position`). These are the dialect's only time
   coordinates; the Dramatic dialect does not know about wall-
   clock time, chronology, or reading time. Position is the
   order in which the Argument unfolds.
5. **M5 — Character Functions are template-parameterized.** A
   `CharacterFunction` is a typed role (Protagonist, Antagonist,
   Reason, Emotion, and so on). Which functions exist in a Story
   is determined by a declared Template (Dramatica-8,
   three-actor, two-actor, author-defined). The dialect ships
   several standard templates and admits custom ones. No Story is
   required to use a function template; a story with no declared
   template has no functional roles in dialect terms, only
   Throughline roles.
6. **M6 — Stakes are first-class.** A `Stakes` record names what
   a Throughline (or the whole Story) has at risk and what it
   stands to gain. Stakes are not implicit in the Throughline;
   they are separately authored, because a throughline can exist
   without clear stakes (especially in draft form) and stakes are
   the primary driver of reader investment. Stakes carry
   authorial-uncertainty naturally: "are these stakes high enough?"
   is a native Dramatic question.
7. **M7 — Grid-snap: declarations are structural; landings are
   interpretive.** A Character's declared Function, a Scene's
   declared Purpose, an Argument's stated Premise — all
   structural. Whether a Function *feels filled*, a Scene
   *works*, a Premise is *earned* — all interpretive, living in
   the description surface with attention.
8. **M8 — The dialect self-verifies without reference to any
   other dialect.** A Dramatic-dialect story is coherent within
   Dramatic terms if (among other checks) every Throughline's
   character references resolve, every Scene's advanced-Throughline
   and advanced-Beat references resolve, every Stakes record's
   owner reference resolves, every Function declaration matches
   the chosen Template, and no Scene claims a Beat position that
   doesn't exist. Verification emits observations, never errors.
9. **M9 — Soft conformance to templates.** A Template declares
   what it *expects* (Dramatica-8 expects Protagonist + Antagonist
   + Reason + Emotion + four more); the dialect reports
   divergence as observation. A Story using a Template is not
   required to populate every slot; observations indicate
   incompleteness, and the author decides whether that is a
   choice or a gap to fix.
10. **M10 — Description surface mirrors the dialect pattern.**
    Every Dramatic record (Story, Argument, Throughline, Character,
    Scene, Beat, Stakes) admits anchored descriptions with
    attention levels (structural / interpretive / flavor). Questions
    (authorial-uncertainty descriptions) are first-class; their
    answers land as ordinary descriptions. The description surface
    follows the cross-dialect pattern architecture-sketch-02 A4
    admits, realized here in Dramatic terms.

M1 through M10 pass the schema-inclusion test within Dramatic
terms: each commitment describes drift that dialect-level schema
catches rather than content an attentive reader could self-police
from prose. Without M1's plurality, stories with nested or
parallel arguments have no native representation. Without M3,
there is no authored link between a Scene and the Argument work
it performs. Without M5's template parameterization, the dialect
commits to Dramatica's eight functions and cannot serve stories
with a different shape.

## Relation to Dramatica

This dialect is Dramatica-influenced — it shares the claim that
"a story is an argument" and adopts much of Dramatica's role
vocabulary — but it is not Dramatica-complete. Intentional
departures:

- **Number of Arguments.** Dramatica posits one Grand Argument
  Story per complete work. M1 admits zero, one, or many. Rationale:
  real stories run on a spectrum from argumentless (lyric works)
  through single-argument (most Hollywood structure) to
  polyphonic (Dostoevsky, Tolstoy, ensemble dramas). Dramatica's
  singular Argument is a useful template — a story can declare
  it — but it is not a dialect-level requirement.
- **Throughline count.** Dramatica requires four Throughlines
  (Overall Story, Main Character, Impact Character, Relationship).
  The dialect admits any count. A monologue has one Throughline
  (the Main Character); a journalistic ensemble piece might have
  only an Overall; a buddy movie centers on the Relationship. The
  four-throughline shape is a useful template; the dialect ships
  it; it is not required.
- **Character Function catalog.** Dramatica's eight functions
  (Protagonist, Antagonist, Reason, Emotion, Skeptic, Sidekick,
  Guardian, Contagonist) are a rich template, and the dialect
  includes them as one named Template. Other templates (three-
  actor: hero/helper/obstacle; two-actor: protagonist/antagonist;
  ensemble: voices-in-tension) are equally first-class.
- **Justification / Process apparatus.** Dramatica's deeper
  psychological theory (how characters justify their positions,
  what motivates change versus stasis, the dynamics of
  approach/resolve/growth/outcome/judgment) is out of scope for
  sketch 01. A Dramatica-template sketch may elect to surface it
  as template-specific records.
- **Stakes.** Dramatica treats stakes implicitly, via the MC
  Problem / Solution pair. The dialect promotes Stakes to a
  first-class record (M6) because drafts often have clear
  Throughlines with unclear Stakes, and that gap is diagnostic.

Retained from Dramatica:

- The core thesis: a story is an argument about a human problem.
- The distinction between Overall, Main Character, and Impact
  perspectives (as Throughline *templates*, not requirements).
- The Relationship Throughline as a first-class idea (one
  Throughline can be owned by a relationship, not a character).
- Character Functions as structural roles distinct from
  individual characters.
- Eight-function vocabulary (as an available Template, not the
  dialect's only option).

The dialect is honest that Dramatica is one frame among many and
that writers who find it too rigid (or who work in traditions
Dramatica underserves) should have dialect-level support for
alternatives.

## Relation to architecture-sketch-02

Architecture-sketch-02 A6–A11 lock the dialect's place in the
broader architecture:

- **A6.** Dramatic is a dialect in the stack; its records and
  semantics are distinct from any other dialect's. The dialect's
  internal coherence is self-sufficient; its external
  compositions happen through architecture-02's lowering
  mechanism (outside this sketch).
- **A7.** Any future lowering from Dramatic to another dialect is
  author-driven, never synthesized. The dialect has no opinion on
  what its records "lower to" — that is the author's choice when
  binding.
- **A8.** The dialect's self-verifier (M8) emits observations to
  the cross-dialect proposal queue architecture-02 specifies.
  Internal verification uses the same pipe cross-boundary
  verification does; the proposal queue is the output channel for
  *all* verifier activity.
- **A9.** The dialect's verifier speaks Dramatic vocabulary. It
  never speaks in the terms of any other dialect. (Cross-boundary
  verifiers are different — they speak the upper dialect while
  querying the lower — but self-verification is purely within-
  dialect.)
- **A10.** The dialect is opt-in. A Story that uses no Dramatic
  records is silent under this dialect's verifier. A Story that
  uses some Dramatic records gets partial verification.
- **A11.** A reader-model partner may operate on Dramatic records
  the same way it operates on other dialects' records — reading
  Dramatic records + their descriptions, emitting reviews and
  proposals to the proposal queue. The partner pattern is
  dialect-agnostic.

## The records

Each record has an id (unique within its Story), an authored_by
(who or what authored it), a narrative position or beat position
where applicable, and permits anchored descriptions per M10.
Fields are named descriptively; exact schema shape is a
refinement concern once this sketch has been pressured by
encoding work.

### Story

The dialect's root record. A coherent dramatic work.

```
Story {
    id
    title
    authored_by
    arguments             (zero or more Argument record ids)
    throughlines          (zero or more Throughline record ids)
    characters            (zero or more Character record ids)
    scenes                (zero or more Scene record ids; ordered
                           by narrative_position)
    character_function_template  (optional: name of declared
                                  Template; absent means no
                                  function roles declared)
}
```

Why a root record exists: it is the anchor for story-level
descriptions, the scope for uniqueness of ids, and the unit a
verifier operates on. An encoding with multiple Stories (a short-
story collection, a multi-book series) has multiple roots; the
dialect makes no claims about cross-Story coherence.

### Argument

The story's claim. What the story is *about*, in thesis terms.

```
Argument {
    id
    premise               (the position the story explores)
    counter_premise       (the opposing position; optional)
    resolution_direction  ("affirm" / "negate" / "complicate" /
                           "unresolved" — the story's stance on
                           the premise)
    domain                (optional tag: moral / practical /
                           psychological / political / ... — an
                           author-free-form category)
    parent_argument       (optional: id of another Argument this
                           one is nested under; admits M1's
                           multi-Argument polyphony)
    authored_by
}
```

Premise is structural (it is the authored claim). Whether the
premise is clearly articulated, whether the counter-premise is
fairly represented, whether the resolution feels earned — these
are interpretive and live in descriptions attached to the
Argument.

### Throughline

A structural role within the Argument.

```
Throughline {
    id
    role_label            (author-chosen label: "overall-story",
                           "main-character", "impact-character",
                           "relationship", or any author string)
    owners                (zero or more Character ids, or the
                           sentinel "none" / "the-situation" /
                           "the-relationship")
    subject               (what the throughline's conflict is
                           about — free text, short)
    counterpoints         (zero or more Throughline ids this one
                           is in dialogue with; admits templates
                           that require paired throughlines)
    argument_contribution (optional: which Argument id, and what
                           side of that argument — "affirms" /
                           "opposes" / "complicates" — this
                           throughline contributes to)
    beats                 (ordered Beat record ids)
    stakes                (optional Stakes record id)
    authored_by
}
```

`owners` is a list, not a single field, because a throughline can
be shared. "none" is legitimate for abstract throughlines (the
Overall Story throughline often has no single owner).

### Character

A person (or anthropomorphized agent) in the story.

```
Character {
    id
    name
    functions             (zero or more CharacterFunction labels
                           per the Story's declared Template)
    authored_by
}
```

Characters in the Dramatic dialect are lighter than one might
expect — just enough to anchor functions and descriptions. Rich
character description (backstory, voice, motivations, flaws)
lives in the description surface attached to the Character
record. This matches M7: declaration is structural,
characterization is interpretive.

**On ownership of Throughlines.** `Throughline.owners` is the
single authoritative source for which Characters own which
Throughlines. The Character record does not repeat that
information as an authored field. Tooling that wants the
Character-to-Throughlines lookup iterates Throughlines and
filters on `owners`; the dialect forbids that inverse from being
re-asserted on the Character record, because two authoritative-
looking fields that could disagree is exactly the internal drift
the schema-inclusion test rules out.

### Scene

A unit of argumentative work.

```
Scene {
    id
    title                 (short, for author reference)
    narrative_position    (integer; the Scene's order in the
                           Story's scene sequence)
    advances              (zero or more { throughline_id, beat_id }
                           tuples — which Throughline beats this
                           Scene pushes forward)
    conflict_shape        (free-text short description of the
                           in-scene pressure: who pushes against
                           whom, over what)
    result                (free-text short description of how the
                           advanced Throughlines are changed by
                           the Scene's end)
    authored_by
}
```

A Scene that declares no advancement is *admissible*. It surfaces
via M8 as an observation ("this Scene has no declared purpose");
the author either adds a purpose (it was intended to advance
something that wasn't written down) or accepts the observation
(it is incidental / color / atmospheric material). The dialect
does not assume Scenes without declared purpose are worthless.

### Beat

A developmental moment within a Throughline.

```
Beat {
    id
    throughline           (parent Throughline id)
    beat_position         (integer; order within the Throughline)
    beat_type             (optional: a template-vocabulary tag
                           such as "inciting" / "rising" /
                           "midpoint" / "peak" / "denouement"; or
                           author-free-form)
    description_of_change (free text: what changes in the
                           Throughline at this Beat)
    authored_by
}
```

Beats are per-Throughline. They give Scenes somewhere to attach.
A Scene advancing the Main Character Throughline at its
"midpoint" beat has a concrete target: the specific Beat record
that represents the midpoint.

### Stakes

Risk and reward for a Throughline (or Story).

```
Stakes {
    id
    owner                 ({ kind: "throughline" | "story",
                            id: <target id> })
    at_risk               (free text: what stands to be lost)
    to_gain               (free text: what stands to be won)
    external_manifestation (free text: how the stakes become
                            legible to the reader / audience)
    authored_by
}
```

Stakes are separate from Throughlines because the two are often
authored at different times. A first-draft Throughline says "the
MC investigates the killer's identity"; the Stakes record that
later clarifies "the MC risks his own identity and crown" is a
distinct authorial move, and surfacing the temporal gap between
Throughline-exists and Stakes-exists is diagnostic (a Throughline
with no Stakes is a candidate for an authorial-uncertainty
question).

### Character Function (template-defined)

A `CharacterFunction` is not a standalone record — it is a label
drawn from a Template's vocabulary and attached to a Character.

A `Template` is:

```
Template {
    name                  (e.g., "dramatica-8", "three-actor")
    functions = [
        {
            label             (e.g., "Protagonist")
            multiplicity      ("exactly-one" | "at-most-one" |
                               "at-least-one" | "any")
        },
        ...
    ]
}
```

The `functions` list is authoritative for two separate things:
which labels are *known* to the Template (any Character carrying
a label not in this list surfaces as an unknown-label
observation) and *how many* Characters the Template expects to
carry each label. Multiplicity is per-label and mandatory — every
function declared by a Template must state whether it is a
singular slot, a capped slot, a minimum-one slot, or an open set.
No implicit default; a Template's authoring act is partly a
commitment on cardinality for every function it admits.

Standard Templates (dialect-shipped):

- **dramatica-8** — eight singular-slot functions:
  ```
  [ (Protagonist,  exactly-one),
    (Antagonist,   exactly-one),
    (Reason,       exactly-one),
    (Emotion,      exactly-one),
    (Skeptic,      exactly-one),
    (Sidekick,     exactly-one),
    (Guardian,     exactly-one),
    (Contagonist,  exactly-one) ]
  ```
  A Dramatica-template Story with three Antagonists, or with
  zero Protagonists, surfaces an observation per M9 soft
  conformance.
- **three-actor** —
  ```
  [ (Hero,     exactly-one),
    (Obstacle, exactly-one),
    (Helper,   at-least-one) ]
  ```
- **two-actor** —
  ```
  [ (Protagonist, exactly-one),
    (Antagonist,  exactly-one) ]
  ```
- **ensemble** — functions and multiplicities are author-
  declared per Story; the shipped ensemble Template has
  `[ (voice, at-least-one) ]` as its only default. Authors
  extend the Template with story-specific labels and their
  multiplicities.

A Story that declares `character_function_template = None` has
no function declarations and self-verification does not check
for them. A Story that declares a Template has its Characters'
function labels checked against the Template's vocabulary *and*
multiplicities.

## The description surface

Every Dramatic record admits anchored descriptions. The
description surface within the Dramatic dialect follows the
dialect-pattern that architecture-02 A4 admits across the stack,
realized here in Dramatic-native terms:

- **Attention levels:** structural / interpretive / flavor.
  Structural descriptions might repeat or clarify a declared
  field ("the MC's Protagonist function specifically manifests
  as investigative tenacity"). Interpretive descriptions live in
  the craft-judgment territory ("the relationship throughline is
  the one where the argument's tragedy actually lands"). Flavor
  is tonal.
- **Kinds:** argument-rationale (commentary on an Argument's
  premise / resolution), throughline-texture (what this role
  *feels like* in practice), character-motivation (why this
  character does what they do beyond structural role), scene-
  purpose (elaborating a Scene's argumentative work beyond the
  structural `advances`), stakes-texture (emotional register of
  the stakes), arg-to-throughline (how a specific Throughline
  inflects the Argument), and author-free-form kinds as needed.
- **Questions:** `is_question` descriptions of kind
  `authorial-uncertainty` carry author-surfaced doubt. Typical
  Dramatic questions: "is the Antagonist clearly the Antagonist,
  or is this ensemble?"; "are the stakes high enough?"; "does
  the MC's resolve really shift, or is this steadfast?".
- **Review and supersession:** as in other dialects' description
  surfaces. A reviewed description carries its review history;
  edits supersede prior versions; staleness tracks the
  description's anchor at authoring time.

## Narrative position — the dialect's time

Scenes occupy integer positions in a sequence. Beats occupy
integer positions within their Throughline. These are ordinal
only — the dialect cares about *order*, not intervals.

What narrative_position is *not*:

- It is not a chronology. Two Scenes depicting events from
  different historical periods can be adjacent in narrative_
  position if the Story's rhetoric places them there.
- It is not a reading time. A single-Scene sequence can be long
  or short; the dialect does not care.
- It is strictly Dramatic-local: the order in which the
  argumentative work unfolds. The dialect takes no position on
  how this ordering relates to anything outside the dialect.

The dialect permits non-integer positions (via convention: insert
a Scene at position 4.5 between 4 and 5) but treats them as
ordered. Authors needing fine-grained position granularity pick
their own convention; the dialect enforces only the ordering.

## Self-verification without reference to any other dialect

The dialect's self-verifier runs these checks within Dramatic
vocabulary:

1. **Id resolution.** Every record reference (Character ids in
   Throughline.owners, Throughline ids in Scene.advances, Beat
   ids in Scene.advances, Argument ids in Throughline.argument_
   contribution, Stakes.owner targets, Beat.throughline, etc.)
   resolves to an existing record within the Story.
2. **Beat sequencing.** Beats within a Throughline have distinct
   `beat_position` values; no gaps are required (the dialect is
   not strict about contiguous beat numbers) but duplicates are
   surfaced.
3. **Scene sequencing.** Scenes have distinct `narrative_position`
   values.
4. **Template conformance (soft).** If the Story declares a
   Character Function Template:
   - **Known-label check.** Every label in any Character's
     `functions` field must appear in the Template's `functions`
     list. Unknown labels surface as observations.
   - **Multiplicity check.** For each function label the Template
     declares, the verifier counts how many Characters carry that
     label and compares against the declared multiplicity.
     `exactly-one` with count 0 surfaces as "slot unfilled" and
     with count ≥ 2 as "slot overfilled". `at-most-one` with
     count ≥ 2 surfaces as "slot overfilled". `at-least-one` with
     count 0 surfaces as "slot unfilled". `any` never triggers.
     Each violation is one observation, naming the label and the
     mismatch.
5. **Argument completeness (soft).** If an Argument declares a
   `resolution_direction`, the self-verifier notes whether any
   Scene's `result` or Throughline's final Beat is described as
   resolving the Argument. This is *literal text check*,
   deliberately weak — genuine resolution is interpretive and
   lives in descriptions; the verifier only flags the total
   absence of any resolution-shaped Scene/Beat.
6. **Stakes coverage (observation).** Throughlines with no
   Stakes record surface as observations ("this Throughline has
   no declared stakes").
7. **Scene purpose (observation).** Scenes with empty `advances`
   surface as observations ("this Scene declares no argumentative
   work").
8. **Orphans.** Records not reachable from the Story root
   (Throughlines with no scenes and no contribution to any
   Argument; Stakes with no owner; etc.) surface as observations.

All checks emit to the proposal queue as observations (per A8).
No check rejects a Story; incomplete or inconsistent Stories are
admissible with surfaced observations.

## Worked example — Oedipus in Dramatic terms

A first-cut Dramatic encoding of Sophocles' *Oedipus Rex*.
Deliberately schematic.

### Story

```
Story {
    id = "S_oedipus_rex"
    title = "Oedipus Rex"
    authored_by = "author"
    character_function_template = "dramatica-8"
    arguments = [ A_knowledge_unmakes ]
    throughlines = [ T_overall_plague, T_mc_oedipus,
                     T_impact_jocasta, T_relationship_oj ]
    characters = [ C_oedipus, C_jocasta, C_tiresias,
                   C_creon, C_shepherd, C_messenger ]
    scenes = [ S_prologue_plague, S_tiresias_accusation,
               S_jocasta_doubt_speech, S_messenger_arrives,
               S_shepherd_testimony, S_anagnorisis,
               S_jocasta_hangs, S_self_blinding, S_exile ]
}
```

### Argument

```
Argument {
    id = "A_knowledge_unmakes"
    premise = "knowledge of one's self is the unmaking of the self"
    counter_premise = "ignorance preserves what knowledge would destroy"
    resolution_direction = "affirm"
    domain = "moral-philosophical"
}
```

The Story affirms its premise: the protagonist's pursuit of
self-knowledge completes his destruction. The counter-premise is
given voice (Jocasta argues for letting the oracles go
unquestioned) but does not prevail.

### Throughlines (four, Dramatica-template default)

```
Throughline {
    id = "T_overall_plague"
    role_label = "overall-story"
    owners = [ "the-situation" ]   # Thebes-under-plague
    subject = "a city under divine curse needs its pollution identified
               and expelled"
    argument_contribution = { arg: A_knowledge_unmakes,
                              side: "complicates" }
}

Throughline {
    id = "T_mc_oedipus"
    role_label = "main-character"
    owners = [ C_oedipus ]
    subject = "a king determined to find the truth of who killed his
               predecessor, at any cost to himself"
    counterpoints = [ T_impact_jocasta ]
    argument_contribution = { arg: A_knowledge_unmakes, side: "affirms" }
    stakes = Stakes_mc_oedipus
}

Throughline {
    id = "T_impact_jocasta"
    role_label = "impact-character"
    owners = [ C_jocasta ]
    subject = "a queen who has already chosen not to know, trying to
               pull the MC into her choice"
    counterpoints = [ T_mc_oedipus ]
    argument_contribution = { arg: A_knowledge_unmakes, side: "opposes" }
    stakes = Stakes_ic_jocasta
}

Throughline {
    id = "T_relationship_oj"
    role_label = "relationship"
    owners = [ "the-relationship" ]
    subject = "a marriage in which truth is the third party; its
               revelation ends the marriage"
    argument_contribution = { arg: A_knowledge_unmakes, side: "affirms" }
}
```

### Characters and Functions (Dramatica-8)

```
Character { id = "C_oedipus",   name = "Oedipus",    functions = [Protagonist, Emotion] }
Character { id = "C_jocasta",   name = "Jocasta",    functions = [Skeptic] }
Character { id = "C_tiresias",  name = "Tiresias",   functions = [Reason] }
Character { id = "C_creon",     name = "Creon",      functions = [Sidekick] }
Character { id = "C_shepherd",  name = "Shepherd",   functions = [Guardian] }
Character { id = "C_messenger", name = "Messenger",  functions = [Contagonist] }
# Antagonist function is unassigned — the "antagonist" in Oedipus is
# the truth itself, which resists assignment to a character. The
# dramatica-8 Template declares Antagonist with multiplicity
# exactly-one; zero Characters carry the label, so the M8.4
# multiplicity check surfaces a "slot unfilled" observation for the
# Antagonist label. The author's choice: accept it (it is a genuine
# feature of the story), interpret one of the existing characters as
# Antagonist, or switch to a Template (e.g., ensemble) whose
# multiplicities do not require a singular Antagonist.
```

### Stakes

```
Stakes {
    id = "Stakes_mc_oedipus"
    owner = { kind: "throughline", id: T_mc_oedipus }
    at_risk = "his identity as legitimate king, as husband, as father;
               his wife's life; his own sight"
    to_gain = "the city's salvation from plague"
    external_manifestation = "the plague itself — withering crops,
                              miscarrying women — insists the stakes
                              into visibility"
}
```

### Scenes (skeletal)

```
Scene {
    id = "S_tiresias_accusation"
    title = "Tiresias accuses Oedipus"
    narrative_position = 10
    advances = [ { throughline: T_mc_oedipus,     beat: B_oedipus_denial },
                 { throughline: T_overall_plague, beat: B_first_naming }  ]
    conflict_shape = "The blind prophet, pressed for truth, names the MC as
                      the pollution; the MC rejects this as political attack."
    result = "MC's investigative certainty deepens, now including suspicion
              of Tiresias+Creon conspiracy. The name is in the air; cannot
              be unsaid."
}

Scene {
    id = "S_anagnorisis"
    title = "Oedipus realizes"
    narrative_position = 70
    advances = [ { throughline: T_mc_oedipus,         beat: B_oedipus_collapse },
                 { throughline: T_overall_plague,     beat: B_pollution_identified },
                 { throughline: T_relationship_oj,    beat: B_marriage_ends_recognition } ]
    conflict_shape = "Shepherd's testimony plus Messenger's adoption reveal
                      plus MC's own prior suspicion combine without further
                      resistance. The MC collapses into recognition."
    result = "The Argument's premise (knowledge unmakes) lands in the MC's
              own perception. The marriage ends in the mind even before
              Jocasta's death confirms it physically."
}
```

(Other scenes as sketched by the Scenes list above; the two shown
illustrate the shape.)

### Self-verifier observations (illustrative)

Running M8 over this Story surfaces, among others:

- **Antagonist slot unfilled** — multiplicity `exactly-one` with
  zero Characters carrying the label (M8.4 multiplicity check,
  M9 soft conformance).
- **Overall Story Throughline has no declared Stakes** (M8 item 6).
- **Scene `S_jocasta_hangs` has no declared `advances`** (M8 item 7) —
  because the skeletal list above didn't populate advances for every
  Scene.

Each observation lands in the proposal queue. The author reads,
decides, responds. No error blocks the story from being
Dramatic-encoded.

## Open questions

1. **OQ1 — Multi-Argument Stories.** M1 admits zero or more
   Arguments per Story. The dialect has a `parent_argument` field
   for nesting. It does not yet specify how polyphonic Arguments
   (multiple peers with no nesting) relate to Throughlines that
   contribute to more than one. A concrete encoding with two
   parallel Arguments will force this.
2. **OQ2 — Relationship Throughline ownership.** A Throughline
   owned by "the-relationship" (not by a Character) is admitted
   but under-specified. Does the relationship have its own
   identity independent of the two characters that make it up?
   Does it inherit stakes from both owners' Stakes records? This
   sketch says Relationship Throughlines are first-class but
   leaves the ownership mechanics to a follow-on sketch.
3. **OQ3 — Beat vocabulary standardization.** Beat types in the
   worked example (B_oedipus_denial, B_first_naming, etc.) are
   ad-hoc. Dramatica has a rich beat vocabulary (signposts, plot
   progression); three-act has a thinner one (inciting, midpoint,
   climax, resolution). Should the dialect ship Beat vocabulary
   templates parallel to Character Function templates? Likely
   yes; defer.
4. **OQ4 — Resolution-direction options.** M1 lists "affirm /
   negate / complicate / unresolved" as resolution directions.
   Is this the right set? Some stories explicitly *refuse* to
   resolve and that is their argument ("life is the ongoing
   question"). Adding a "refuse-to-answer" distinct from
   "unresolved" may matter; defer to concrete encodings.
5. **OQ5 — Dramatic identity across retellings.** Two Dramatic
   encodings of Oedipus (one Freudian, one Sophoclean) would
   share the same Story plot but might have different Arguments
   and different Character Function assignments. Does the
   dialect have a concept of "this is a version of that Story"?
   Probably out of scope; this is re-encoding, not a dialect
   primitive.
6. **OQ6 — Author-defined Character Function templates.** The
   dialect ships four Templates (dramatica-8, three-actor,
   two-actor, ensemble). Custom Templates are admitted via the
   Template record. The mechanics of Template authoring — where
   they live, how they're shared across Stories — are left for
   a Template-management sketch.
7. **OQ7 — Staleness of Dramatic records.** If an author revises
   the Argument mid-drafting, dependent Throughline contributions
   may be stale ("this Throughline opposed a premise that no
   longer exists in that form"). How does the dialect surface
   cross-record staleness? The description surface has its own
   staleness machinery; the record-to-record version of it is
   less obvious. Defer.
8. **OQ8 — Thematic material beyond Argument.** Some stories
   have thematic work that doesn't resolve into a single claim
   (sustained atmosphere, lyric preoccupations, rhetorical
   figures). Does the dialect need a vocabulary for theme *as
   not-yet-an-argument*? A `Motif` record, perhaps. Deferred;
   the first sketch stays tight.

## What happens next

1. **Pressure the dialect with a second encoding.** Oedipus is
   the worked example here. A second encoding (something
   structurally unlike Oedipus — a Dostoevsky novel, an
   ensemble drama, a sustained-mood piece) will surface
   dialect gaps the first encoding can't. Good candidates:
   *Macbeth* (clearer Antagonist shape, different MC resolve),
   *The Brothers Karamazov* (multi-Argument, dense character
   functions), *The Remains of the Day* (Main-Character-only
   throughline, little Overall Story).
2. **Extract dialect templates.** The sketch names dramatica-8
   as a Template and several others as named Templates; actually
   constructing and shipping those Template records is
   follow-on work.
3. **Defer lowering and cross-dialect anything** until the
   dialect holds up under several encodings on its own terms.
   That is architecture-02's concern when we pick it back up;
   this dialect needs to stand on its own first.
4. **Consider a Structural dialect** as a parallel-pole
   follow-on. The Dramatic dialect deliberately does *not*
   include act structure, pacing, or plot-point machinery;
   those belong in a parallel dialect. Separating them keeps
   each dialect coherent and admits stories that use one
   without the other.
