# Dramatica template — sketch 01

**Status:** draft, active
**Date:** 2026-04-14
**Supersedes:** nothing (new sketch within the Dramatic dialect)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md), [dramatic-sketch-01.md](dramatic-sketch-01.md)
**Superseded by:** nothing yet

## Purpose and terminology

Test the Dramatic dialect (dramatic-sketch-01) against a rich,
real-world narrative theory by drafting a specific Template within
the dialect that encodes Dramatica's full Grand Argument Story
theory. The question the sketch is meant to answer: is the
dialect's Template mechanism (M5, M9) expressive enough to carry
Dramatica, or does Dramatica's depth press past what the dialect
can currently represent?

Terminology used throughout:

- **Dramatic** — the generalized dialect from dramatic-sketch-01.
  Vocabulary includes Argument, Throughline, Scene, Character,
  Stakes, narrative_position, Character Function Templates.
- **Dramatica** — the specific narrative theory (Melanie Anne
  Phillips and Chris Huntley; also the software product of that
  name). A rich, opinionated theoretical apparatus.
- **Dramatica template** (in this sketch's usage: `dramatica-complete`)
  — the specific Template within the Dramatic dialect that
  encodes as much of Dramatica's theoretical apparatus as the
  dialect can accommodate.

The sketch is *not* a Dramatica tutorial. It presumes familiarity
with Dramatica's core concepts and translates them into dialect
records. Where Dramatica's theory pressed past the Dramatic
dialect's current expressive power, the sketch calls out a
forcing function for a future dramatic-sketch-02; it does not
retroactively revise dramatic-sketch-01.

Scope this sketch commits to:

- The Dramatica template as a named, declarable Template within
  the Dramatic dialect (per dramatic-sketch-01 M5).
- The Template's record-type extensions: Quad, DynamicStoryPoint,
  Signpost, and the Domain / Concern / Issue / Problem nested
  hierarchy.
- Story-level extensions the Template declares: Story Goal and
  Story Consequence.
- How the Dramatic dialect's self-verifier extends to check
  Template-specific structural rules.
- Where Dramatica's theory genuinely resists encoding in the
  dialect's current shape — the *forcing functions* this sketch
  exists to surface.
- A partial encoding of Oedipus Rex against `dramatica-complete`,
  continuing the worked example from dramatic-sketch-01.

Scope this sketch is *not* committing to:

- A middle dialect between Dramatic (with the Dramatica template)
  and Substrate. Whether something like Structural / Pacing /
  Plot-Shape belongs in the stack is an architecture question,
  decided later based on what lowering needs.
- Revisions to dramatic-sketch-01's M1–M10 commitments. Where
  the Dramatica template presses the dialect beyond M5's
  current Template shape, the pressure is flagged as a
  forcing function for dramatic-sketch-02, not resolved here.
- Dramatica's full vocabulary. The sketch covers the load-
  bearing joints (Goal, Consequence, Dynamic Story Points,
  Throughline-to-Domain assignment, Problem quad, Signposts,
  the Domain/Concern/Issue/Problem hierarchy); it does not
  expand into every single Dramatica table (Character
  Motivations quads, Means of Evaluation quads, Methodology
  quads, etc.). The pattern extends uniformly; the sketch
  demonstrates it without enumerating exhaustively.
- Dramatica's Justification / Process / Approach theory at
  record-level. Those are interpretive claims about *why* the
  theory's slots land the way they do, not structural slot
  declarations. They live in the description surface.
- Assertion that Dramatica-complete is *the* right way to
  encode dramatic structure. The Dramatic dialect already
  admits other Templates. This sketch is about expressive power,
  not endorsement.

## Relation to Dramatic dialect (dramatic-sketch-01)

The Dramatica template sits entirely within the Dramatic dialect.
It uses the dialect's base records (Story, Argument, Throughline,
Character, Scene, Beat, Stakes) unchanged. What it *adds* is:

- A rich vocabulary of Template-specific record types (Quad,
  DynamicStoryPoint, Signpost, Domain, Concern, Issue, Problem).
- Template-specific Story-level fields (Story Goal, Story
  Consequence).
- A Template-specific set of Character Function labels with
  per-label multiplicity (extending dramatic-sketch-01's already-
  shipped thin `dramatica-8` template into a richer
  `dramatica-complete`).
- Template-specific self-verification rules that compose with
  the dialect's base M8 checks.

What it does *not* add:

- A new time concept. narrative_position (M4) and beat_position
  are the dialect's time; the Template uses them as-is.
- A new description surface. All Dramatica-specific description
  kinds (Domain-rationale, Problem-interpretation, Signpost-
  commentary, Justification-note) sit on the dialect's existing
  description machinery (M10).
- Any reaching across dialect boundaries. The sketch observes
  the same no-substrate-vocabulary discipline dramatic-sketch-01
  observed.

## What this sketch *is* committing to

1. **Q1 — Templates may extend the Dramatic dialect with their
   own record types and Story-level fields.** A Template is not
   limited to a labels+multiplicities list (which is the
   minimum dramatic-sketch-01 M5 requires). A Template may
   declare new record types whose instances live within a Story
   and which the Template's self-verifier then checks for
   structural conformance. This extends M5 deliberately; if the
   Dramatic dialect wants to admit rich templates like
   Dramatica, Templates must be schema-extensible. This is a
   forcing function on dramatic-sketch-02 (flagged under *Where
   the dialect resists* below).
2. **Q2 — A Quad is the Dramatica template's core structural
   record type.** A Quad has four labeled positions arranged in
   a specific static/dynamic crosshatch (two dimensions of
   opposition: Dramatica's `dynamic_pair` and `companion_pair`
   structure). The Dramatica template declares many Quads; each
   is a `Quad` record with a `kind` tag and four element
   references.
3. **Q3 — Dramatica's Domain/Concern/Issue/Problem hierarchy is
   a nested quad structure.** Four Domains (one per Throughline);
   one Concern per Domain (chosen from a quad of Concerns for
   that Domain); one Issue per Concern (chosen from a quad of
   Issues); one Problem per Issue (chosen from a quad of
   Problems). The hierarchy is realized as nested Quad records
   plus explicit pick records.
4. **Q4 — Story Goal and Story Consequence are Template-
   specific Story-level fields.** They are declared as extensions
   to the base Story record, available when the Story's
   `character_function_template` is `dramatica-complete`. Authors
   using a different Template do not see these fields.
5. **Q5 — Dynamic Story Points are six labeled binary-choice
   records.** `Resolve` (Change / Steadfast), `Growth` (Start /
   Stop), `Approach` (Do-er / Be-er), `Limit` (Timelock /
   Optionlock), `Outcome` (Success / Failure), `Judgment` (Good /
   Bad). Each is a `DynamicStoryPoint` record attached to the
   Story. Dramatica has specific rules about which combinations
   are coherent (e.g., Outcome and Judgment together produce the
   four canonical endings); the Template encodes the records,
   and description-surface annotations handle the theory of
   coherence.
6. **Q6 — The Dramatica template fixes the Character Function
   catalog at the eight known labels and assigns each to a
   specific Throughline role.** The eight functions (Protagonist,
   Antagonist, Reason, Emotion, Skeptic, Sidekick, Guardian,
   Contagonist) each get multiplicity `exactly-one` per
   dramatic-sketch-01 M5. The Template further commits:
   Protagonist is in the Overall-Story + Main-Character
   Throughlines; Antagonist is in the Overall-Story Throughline;
   (and so on, following Dramatica's fixed assignments). A
   Character carrying a function that is not in the expected
   Throughline surfaces as an observation.
7. **Q7 — Signposts are four per Throughline, representing plot-
   progression moments.** A `Signpost` record attaches to a
   Throughline with a signpost_position (1–4) and a
   Domain-vocabulary label (drawn from Dramatica's
   theory-specific progression tables). The Dramatic dialect's
   Beats (per M9) remain per-Throughline developmental moments;
   Signposts are a Template-specific overlay that names *which
   part of the Throughline's Domain the Throughline is passing
   through at that position*.
8. **Q8 — Interpretive Dramatica concepts live in the
   description surface, not as records.** Justification ("why
   the character defends this position"), Process ("how the
   character moves through Domains"), Approach ("how the story
   thinks about the problem"), and similar theory-heavy
   interpretive moves are description kinds (with `attention =
   interpretive`), not structural records. The Template's
   structural apparatus is *about* what can be declared
   crisply; the rest is description territory per dramatic-
   sketch-01 M7.
9. **Q9 — The Template's self-verifier extends the dialect's
   M8 checks without replacing them.** The Template's checks
   include: exactly four Throughlines with the four Dramatica
   role_labels, one Domain per Throughline with the four
   Domains covered collectively without duplication, exactly
   one Concern per Domain drawn from that Domain's concern quad,
   exactly one Issue per Concern, exactly one Problem per Issue,
   six Dynamic Story Points present, four Signposts per
   Throughline, eight Characters carrying the Function labels
   with expected Throughline assignments.
10. **Q10 — Where Dramatica's theory resists the dialect's
    current shape, the resistance becomes a forcing function,
    not a dialect-silent failure.** This sketch names every
    such place explicitly (see *Where the dialect resists*
    below). The author's choice when hitting such a place is:
    (a) encode the Dramatica concept with the expressive power
    currently available (possibly awkwardly), (b) push dramatic-
    sketch-02 to extend the dialect, or (c) accept that the
    concept is interpretive and belongs in descriptions.

Q1 through Q10 pass schema-inclusion within the Template's own
terms: each describes what the Template machinery needs to catch
that the dialect's base M-series alone does not catch. Without
Q1, Dramatica cannot be expressed as a Template at all — the
dialect would require Dramatica-specific dialect-level records,
which defeats the Template-parameterization premise.

## The quad structure

A `Quad` is the central Dramatica structural unit. Dramatica
organizes its theory as quads at many levels: Domains,
Concerns, Issues, Problems, Character Motivations, Means of
Evaluation, Purposes, Approaches, Evaluations, and more. Each
quad is four elements arranged with specific internal structure:

```
   A  ←── dynamic pair ──→  C
   ↕                        ↕
   companion                companion
   pair                     pair
   ↕                        ↕
   B  ←── dynamic pair ──→  D
```

The arrangement commits that A and C are in *dynamic*
opposition (fundamentally opposed across a dimension of
tension); A and B are *companions* (related but not opposed);
A and D are *dependents* (related through both the dynamic and
companion axes). Dramatica's theoretical claims about a Story
often turn on which element of a quad the Story picks and what
that implies about the others.

Record shape:

```
Quad {
    id
    kind                  (e.g., "domain-quad", "problem-mc-quad")
    position_A, element_A
    position_B, element_B
    position_C, element_C
    position_D, element_D
    dynamic_pairs = [ (A, C), (B, D) ]
    companion_pairs = [ (A, B), (C, D) ]
    # (dependent_pairs derivable: (A, D), (B, C))
    authored_by
}
```

Note: the `position_X` fields are convention — Dramatica has
specific position conventions for each quad kind (Activity is
always top-left in a Domain quad, etc.). The Template's
validator checks the convention per kind.

Every Dramatica record that picks "one element from a quad"
(e.g., "the Main Character's Problem is Pursuit, chosen from
the Pursuit/Avoid/Consider/Reconsider quad") is a separate
`QuadPick` record:

```
QuadPick {
    id
    quad                  (Quad record id)
    chosen_position       ("A" | "B" | "C" | "D")
    attached_to           (what record this pick is on — Story,
                           MC Throughline, etc.)
    authored_by
}
```

This is deliberately normalized: the Quad exists as a record
(so the dialect can review it, describe it, question it), and
picks reference the Quad.

## The Domain / Concern / Issue / Problem hierarchy

Dramatica's most-argued-over structural claim: every Story has a
specific nested structure of Domain → Concern → Issue → Problem
at four levels of specificity, once per Throughline. The
Dramatica template encodes it as nested Quad records plus
QuadPicks.

### Domains

Four Domains exist in total: **Activity**, **Situation**,
**Manipulation**, **Fixed Attitude**. They form a single Quad:

```
Quad {
    id = "dramatica_domain_quad"
    kind = "domain-quad"
    position_A = "activity"            (external + process)
    position_B = "situation"           (external + state)
    position_C = "manipulation"        (internal + process)
    position_D = "fixed-attitude"      (internal + state)
    dynamic_pairs = [ (A, C), (B, D) ]
    companion_pairs = [ (A, B), (C, D) ]
}
```

Each Throughline is assigned one Domain. Dramatica requires all
four Domains to be covered across the four Throughlines — no
duplicates. That's a `DomainAssignment` record per Throughline:

```
DomainAssignment {
    id
    throughline           (Throughline id)
    domain                ("activity" | "situation" |
                           "manipulation" | "fixed-attitude")
    authored_by
}
```

### Concerns

Each Domain has its own Quad of Concerns. Dramatica specifies
these concretely (Activity Domain: Obtaining / Doing / Learning
/ Understanding; Situation Domain: The Present / The Past / The
Future / How Things Are Changing; and so on — four quads total).

Each Throughline picks one Concern from its assigned Domain's
Concern Quad:

```
Quad {
    id = "activity_concern_quad"
    kind = "concern-quad"
    position_A = "obtaining"
    position_B = "doing"
    position_C = "learning"
    position_D = "understanding"
    ...
}

QuadPick {
    id
    quad = "activity_concern_quad"
    chosen_position = "D"   # Overall Story is about "understanding"
    attached_to = { kind: "throughline", id: T_overall_story }
}
```

### Issues, Problems, Solutions

The pattern nests one more level: each Concern has its own Quad
of Issues; each Issue has its own Quad of Problems; and the
Problem chosen drives the Solution / Symptom / Response
triangulation within a separate Problem Quad.

Dramatica specifies all four levels' quad contents per Domain
(that's 4 × 4 × 4 × 4 = 256 positions in total, though only 4
are picked per Throughline — one per level). The Dramatica
template ships these Quads as Template constants and the
QuadPick records are per-Story.

```
# Per Throughline, four QuadPicks:
#   (i) which Concern (from the Throughline's Domain's Concern Quad)
#   (ii) which Issue (from the chosen Concern's Issue Quad)
#   (iii) which Problem (from the chosen Issue's Problem Quad)
#   (iv) the Solution is automatically the Problem's dynamic-pair
#        element in the Problem Quad; it is not an independent pick.
```

The Solution is *derivable* from the Problem pick (the dynamic-
pair element in the Problem Quad). Similarly, Symptom and
Response are the companion-pair and dependent-pair elements of
the Problem — derived, not picked. This is a forcing function
for the dialect (see *Where the dialect resists*).

## Dynamic Story Points

Six binary-choice records attached to the Story as a whole:

```
DynamicStoryPoint {
    id
    axis                  ("resolve" | "growth" | "approach" |
                           "limit" | "outcome" | "judgment")
    choice                (value depends on axis)
    attached_to           (Story id)
    authored_by
}
```

Axes and choices:

| axis       | choices              |
|------------|----------------------|
| resolve    | change / steadfast   |
| growth     | start / stop         |
| approach   | do-er / be-er        |
| limit      | timelock / optionlock|
| outcome    | success / failure    |
| judgment   | good / bad           |

Dramatica's canonical claim: Outcome × Judgment yields the four
story-level endings (Triumph / Tragedy / Personal Triumph /
Personal Tragedy). The Template does not encode the derived
ending as its own field — authors read it off the two records.

The Q5 commitment is that six DynamicStoryPoint records are
*expected* when the Template is `dramatica-complete`; absence
of any surfaces as an observation.

## Story Goal and Story Consequence

Story-level fields the Template adds:

```
Story {  # base record, under dramatica-complete Template
    id, title, authored_by, ...
    arguments, throughlines, characters, scenes   # per base dialect
    character_function_template = "dramatica-complete"

    # Template extensions under dramatica-complete:
    story_goal            (free-text short statement of what the
                           Overall Story is pursuing)
    story_consequence     (free-text short statement of what
                           happens if the Goal fails)
}
```

These are structural declarations (the author's stated Goal and
Consequence), not interpretations of whether the Goal is
compelling or the Consequence bites. Interpretation lives on
description surface anchored to the Story.

Dramatica ties Goal and Consequence to specific axes of Concern
and Issue within the Overall Story Throughline. The Template
expresses that via explicit `goal_concern_link` and
`consequence_issue_link` fields on the Story (each pointing at
a QuadPick record). This is deliberately heavy — Dramatica's
theory *is* heavy — but it stays record-shaped.

## Signposts

Four per Throughline, at positions 1 through 4. Each Signpost
names a Domain-specific progression element (drawn from
Dramatica's per-Domain signpost tables: Activity Signposts are
Learning → Understanding → Doing → Obtaining in some order
determined by the Throughline's Concern pick, and so on).

```
Signpost {
    id
    throughline           (parent Throughline id)
    signpost_position     (1 | 2 | 3 | 4)
    signpost_element      (Dramatica-vocabulary label per Domain)
    expected_scenes       (zero or more Scene ids whose
                           narrative_position places them in this
                           Signpost's span; optional link the
                           author declares, not derived)
    authored_by
}
```

The four Signposts of a Throughline are meant to segment the
Throughline's unfolding across the story. Whether Scene X
belongs to Signpost 2 or 3 is a position-in-narrative question
the author declares; the Template does not compute it.

## Character Functions — Template-assigned Throughlines

The Dramatica template refines dramatic-sketch-01's `dramatica-8`
Template further: each of the eight Functions has not only
multiplicity `exactly-one` but also a *required Throughline
association*. Per Dramatica theory:

| Function     | Primary Throughline(s)            |
|--------------|-----------------------------------|
| Protagonist  | Overall Story + Main Character    |
| Antagonist   | Overall Story                     |
| Reason       | Overall Story                     |
| Emotion      | Overall Story                     |
| Skeptic      | Overall Story                     |
| Sidekick     | Overall Story                     |
| Guardian     | Overall Story or Impact Character |
| Contagonist  | Overall Story                     |

(Dramatica is more specific than the above; the full treatment
is a cross-table the Template ships as configuration data, not
narrative prose.)

A Character carrying `functions = [Protagonist]` is *expected*
to own (be in the `owners` list of) both the Overall Story and
the Main Character Throughlines per this table. Divergence
surfaces as an observation, not an error — Dramatica-adjacent
stories sometimes split the Protagonist across the two
Throughlines onto different Characters (the MC is not the
Protagonist), and Dramatica itself recognizes this pattern.

## Justification and interpretation — descriptions, not records

Dramatica's deep psychological theory — how characters justify
their positions, the Inner/Outer process distinction, Linear vs
Holistic thinking, Male/Female character types — is *theory
about why the structural slots land the way they do*, not slot
declarations themselves. The Template does not encode these as
records. It exposes them as Template-suggested description
kinds:

- `justification` — interpretive notes on why a character holds
  their Problem.
- `process-note` — interpretive notes on how the MC moves
  through their Domain.
- `linear-holistic-note` — interpretive notes on the MC's
  thinking style.

Each is `kind = <above>`, `attention = interpretive`, anchored
to the relevant Character or Throughline record. The Template's
self-verifier does not require them; they are affordances the
author can use.

This preserves M7 (declarations structural, landings
interpretive) and keeps the Template from exploding into
psychological-record territory where it would not provide
leverage.

## Self-verification under the Dramatica template

Composes with dramatic-sketch-01's M8. The Template adds:

1. **Throughline count exactly four**, with role_labels covering
   Overall-Story, Main-Character, Impact-Character, Relationship
   exactly once each.
2. **Domain assignment complete and non-duplicative** — four
   DomainAssignment records, one per Throughline, covering all
   four Domains without repetition.
3. **Concern / Issue / Problem picks per Throughline** — each
   Throughline has exactly one QuadPick at each hierarchy level
   (Concern, Issue, Problem), and each pick's Quad is the one
   appropriate to the chain's prior picks.
4. **Solution / Symptom / Response derivations consistent.**
   Every Problem QuadPick has implied Solution / Symptom /
   Response positions. If the author has also authored explicit
   Solution / Symptom / Response picks, they must agree with
   the derivation.
5. **Six Dynamic Story Points.** One record per axis, each with
   a valid choice from its axis's values.
6. **Four Signposts per Throughline**, positions 1–4 distinct,
   elements drawn from the Throughline's Domain-appropriate
   signpost table.
7. **Character Function–Throughline alignment.** Each of the
   eight Functions is assigned to at least one Throughline; the
   Throughline matches the Dramatica-specified assignment per
   the Function-Throughline table.
8. **Story Goal and Story Consequence present** when Template is
   `dramatica-complete`; absence surfaces as observation.

All checks emit to the proposal queue as observations (per
architecture-02 A8). The Dramatica template is strict about
shape but never strict about completion: an encoding that is
partway through Dramatica-fication surfaces observations
naming exactly what's missing.

## Where the dialect resists — forcing functions for dramatic-sketch-02

The Dramatica template surfaced several places where the Dramatic
dialect's current shape (dramatic-sketch-01) is too thin. Each is
a real design question for a future sketch.

1. **Template-level schema extension (Q1).** Dramatic-sketch-01's
   M5 specifies Templates as lists of `(label, multiplicity)`
   tuples. Dramatica's Template needs its own record types
   (Quad, QuadPick, DynamicStoryPoint, Signpost, DomainAssignment).
   The Template must be able to declare these record types and
   their constraints. Either (a) the dialect admits Template-
   declared record types as a first-class extension mechanism, or
   (b) Templates are limited to label-sets and Dramatica has to
   be encoded through awkward workarounds. Current sketch picks
   (a) as a Q1 commitment; that commitment presses past M5 as
   written, so dramatic-sketch-02 should formalize it.
2. **Derived fields and consistency between picks.** Problem →
   Solution / Symptom / Response derivation is a structural
   consequence of a QuadPick plus the Quad's dynamic/companion
   pairs. The dialect has no current concept of "this field is
   derived from that record." Either dramatic-sketch-02 adds
   derived-field semantics (similar to inference-model-sketch-01's
   rule derivation but at the dialect level), or the Template
   authors the derivation manually per Story (making the author
   maintain consistency the schema should catch).
3. **Story-level Template extensions (Q4).** The Template adds
   story_goal, story_consequence, goal_concern_link,
   consequence_issue_link, and the `character_function_template`
   field to the Story record. The dialect would need a clean
   story about Template-declared field extensions to the base
   records. Without that, the Story record's actual shape
   depends on which Template is active — which might be fine if
   the dialect commits to it, but it is not committed today.
4. **Per-Template Character Function constraints.** Dramatica
   ties Functions to specific Throughlines. Dramatic-sketch-01's
   Template shape allows per-Function multiplicity but not
   per-Function relationship-to-other-records constraints. This
   is a generalization the Template machinery needs to handle.
5. **Heavy Template data.** The Dramatica template ships Quad
   content: the names of Domains, the names of Concerns within
   each Domain, the names of Issues within each Concern, and so
   on. Dramatica has on the order of 300+ labeled positions as
   theory-data. The dialect currently has no mechanism for
   Templates to ship structured theory-data as part of their
   declaration; a Template is currently a label set with
   multiplicities, not a label set plus a taxonomy. This needs
   formalization.
6. **Quad-shape typed validator.** A `kind = "domain-quad"` Quad
   has a specific four-element shape (Activity, Situation,
   Manipulation, Fixed Attitude) that is not arbitrary. The
   dialect needs a way for Templates to declare "a Quad of kind
   X must have exactly these four positions with these labels,
   arranged with these dynamic and companion pairs." Without
   this, any Quad with any four elements passes the generic
   validator, and Dramatica's specific theoretical structure is
   lost.

Each of these is a legitimate dramatic-sketch-02 agenda item.
Noting them here: the sketch's function is to force the
question, not to resolve it.

## Worked example — Oedipus Rex under `dramatica-complete`

A partial encoding continuing from dramatic-sketch-01's Oedipus
example. The base Dramatic records (Argument, Throughlines,
Characters, Scenes, Stakes) are unchanged from that sketch.
Here we add the Template-specific records.

### Dynamic Story Points for Oedipus

```
DynamicStoryPoint { axis = "resolve",   choice = "change"      # Oedipus changes — catastrophically
                    attached_to = S_oedipus_rex }
DynamicStoryPoint { axis = "growth",    choice = "stop"        # He must stop pursuing — he cannot
                    attached_to = S_oedipus_rex }
DynamicStoryPoint { axis = "approach",  choice = "do-er"       # Oedipus acts; does not retreat inward
                    attached_to = S_oedipus_rex }
DynamicStoryPoint { axis = "limit",     choice = "optionlock"  # He runs out of options, not time
                    attached_to = S_oedipus_rex }
DynamicStoryPoint { axis = "outcome",   choice = "success"     # The plague-killer is found
                    attached_to = S_oedipus_rex }
DynamicStoryPoint { axis = "judgment",  choice = "bad"         # At personal cost — Personal Tragedy
                    attached_to = S_oedipus_rex }
```

Outcome × Judgment = Success × Bad = "Personal Tragedy" in
Dramatica's canonical four-way categorization. The story
achieves its external goal (identifying the killer, ending the
plague) but at catastrophic personal cost. That derived label
is not a Template field; the author reads it off the two axes.

### Domain Assignments

```
DomainAssignment { throughline = T_overall_plague,    domain = "situation"       }
DomainAssignment { throughline = T_mc_oedipus,        domain = "activity"        }
DomainAssignment { throughline = T_impact_jocasta,    domain = "fixed-attitude"  }
DomainAssignment { throughline = T_relationship_oj,   domain = "manipulation"    }
```

All four Domains covered, no duplicates — the Template's
domain-coverage check passes.

### Story Goal and Consequence

```
Story {
    ...
    story_goal        = "identify the pollution causing the plague and
                         expel it from Thebes"
    story_consequence = "the plague continues; the city dies"
    goal_concern_link = QuadPick { quad: "situation_concern_quad",
                                   chosen_position: "C"   # "the past" as
                                                          # the key hidden cause
                                 }
    consequence_issue_link = QuadPick { ... }
}
```

### Problem / Solution / Symptom / Response for MC Throughline

A partial pick, illustrative:

```
QuadPick {
    id = "oedipus_mc_problem_pick"
    quad = "activity_problem_quad_under_mc_issue_pick"
    chosen_position = "A"
    attached_to = { kind: "throughline", id: T_mc_oedipus }
    # chosen element: e.g., "Pursuit" — Oedipus's defining action
}

# Derived from the Problem pick's Quad:
#   Solution is at position C (dynamic pair):   e.g., "Avoid"
#   Symptom is at position B (companion pair):  e.g., "Consider"
#   Response is at position D (dependent pair): e.g., "Reconsider"
# The dialect's current shape requires the author to assert these
# derived picks redundantly; the Q-forcing-function #2 above is
# the dialect-level fix.
```

Oedipus's Problem is Pursuit (he will not stop pursuing the
truth); his Solution would be Avoid (the thing he cannot do).
The Problem drives the story; the un-chosen Solution is the
narrative's structural pressure.

### Signposts for MC Throughline

```
Signpost { throughline = T_mc_oedipus, signpost_position = 1,
           signpost_element = "learning"       # initial investigation phase
         }
Signpost { throughline = T_mc_oedipus, signpost_position = 2,
           signpost_element = "understanding"  # Tiresias's accusation —
                                               # what it means sinks in
         }
Signpost { throughline = T_mc_oedipus, signpost_position = 3,
           signpost_element = "doing"          # the sustained questioning;
                                               # Jocasta, Messenger, Shepherd
         }
Signpost { throughline = T_mc_oedipus, signpost_position = 4,
           signpost_element = "obtaining"      # he obtains the truth
                                               # (and is undone by it)
         }
```

This is the Activity Domain's default signpost ordering for
Oedipus's Concern; the Template's per-Domain signpost tables
would specify the required ordering given the Throughline's
Concern pick.

### Self-verifier observations under this encoding

- Throughline count is 4, role_labels cover all four required
  — passes.
- Four DomainAssignments covering all four Domains — passes.
- Six DynamicStoryPoints present — passes.
- Four Signposts on T_mc_oedipus (the partial encoding shown);
  three other Throughlines would need their own four-Signpost
  sets — observation surfacing the gaps.
- Antagonist slot unfilled (as in dramatic-sketch-01's encoding)
  — observation carries forward from the base-dialect check; the
  Template adds no change here.
- QuadPick records for Concerns / Issues / Problems on three of
  the four Throughlines are missing in this partial encoding —
  observation.
- Goal and Consequence present; goal_concern_link references a
  QuadPick that would need its referenced Quad to actually
  exist in the Template data — observation if the Template's
  shipped Quad data hasn't been fully authored.

The encoding is demonstrably incomplete, and the self-verifier
names exactly what's missing. That is the Template working as
intended.

## Open questions

1. **OQ1 — Quad positional semantics.** The sketch uses A/B/C/D
   as positional labels for a Quad's four slots, with fixed
   semantics (A–C is dynamic, A–B is companion, A–D is
   dependent). Is there a more intuitive positional vocabulary?
   Dramatica itself uses Top-Left / Top-Right / Bottom-Left /
   Bottom-Right, which is visually cleaner but implies a spatial
   layout the dialect does not actually have. The sketch picks
   A/B/C/D for alphabetical legibility; defer.
2. **OQ2 — Solution / Symptom / Response as derived vs.
   author-authored.** The Q-forcing-function #2 already calls
   out this dialect-level gap. The open question is whether
   dramatic-sketch-02 should build a dialect-level derivation
   mechanism (parallel to inference-model-sketch-01's Rule
   machinery but for the Dramatic dialect) or whether Templates
   should carry a lighter "these fields are derived from that
   field per this rule" affordance. The latter is simpler; the
   former is more powerful.
3. **OQ3 — Character-type quads and Methodology quads.**
   Dramatica has Character Type quads (Pursuit / Consider /
   Avoid / Reconsider as Motivations), Methodology quads (how
   characters think), Purpose quads, Means of Evaluation
   quads, and a few more. The sketch stops at the Domain /
   Concern / Issue / Problem hierarchy plus the six DSPs plus
   Signposts. Adding the rest is pattern repetition, not new
   forcing function; defer.
4. **OQ4 — Story Mind as a distinct record.** Dramatica's
   "Story Mind" concept is that the whole Grand Argument
   Story represents a single human mind working through a
   problem, with each Throughline and each Character standing
   in for aspects of that mind. Is Story Mind a derived
   concept (the whole Template encoding *is* the Story Mind)
   or does the Template need an explicit `StoryMind` record
   that collects its components? The sketch treats Story Mind
   as emergent; a later pass might argue for a record.
5. **OQ5 — The 4 × 4 × 4 × 4 = 256 Quad-element labels.**
   Dramatica ships, as theory data, the exact label sets for
   every Quad at every level in every Domain. That is a large
   configuration payload. Where does it live — in the Template
   itself (very heavy), in an external data file the Template
   references, or is the Template's shape flexible enough to
   admit author-supplied Quad contents? This sketch assumes
   the Template ships the full theory data; the storage and
   loading mechanics are tooling, not schema.
6. **OQ6 — Partial-Dramatica encodings.** Many stories fit
   Dramatica partially. The Template as drafted expects full
   conformance and surfaces incompleteness as observations.
   Should the dialect admit "dramatica-partial" or
   "dramatica-aware" as softer Templates? The dramatic-sketch-01
   soft-conformance rule (M9) already gives this — an author
   who uses `dramatica-complete` but leaves most of it empty
   just gets a lot of observations. The question is whether
   that is the right user experience or whether a softer
   Template is worth shipping.
7. **OQ7 — Whether Dramatica is the *right* Template to make
   this sketch's point.** The sketch bills itself as testing
   the Dramatic dialect's expressive power. Dramatica is one
   of the richest, most-dogmatic narrative theories in
   circulation. If the dialect handles Dramatica (pending
   dramatic-sketch-02 for the dialect-level gaps), the dialect
   can likely handle any other theory. But "expressive enough
   for Dramatica" is not a theorem; other theories (Dan Harmon's
   Story Circle, Lajos Egri's premise-driven structure) may
   press the dialect in different ways. The sketch makes no
   claim that Dramatica is the limit of what the dialect must
   handle.
8. **OQ8 — The sandwich question.** The top of the stack is a
   title / premise / "what's this about" — barely a dialect at
   all, just a one-sentence statement. The Dramatica template
   is the rich upper layer. The substrate is the rich lower
   layer. Does anything sit between Dramatica and substrate?
   Candidate middle dialects — a plot-shape / pacing / act-
   structure layer, a scene-function layer, something else —
   remain open. The sketch does not commit. Whether lowering
   can go directly from Dramatica-records to substrate records
   or needs intermediate stops is a design question best
   answered when a concrete lowering is attempted. This is
   flagged for architecture-sketch-02's next revision.

## What happens next

1. **Decide whether dramatic-sketch-02 is the right next
   design work**, driven by the forcing functions this sketch
   surfaced (Template-level schema extension, derived fields,
   story-level Template extensions, heavy Template data). If
   yes, that sketch re-opens M5 with the expressive power
   Dramatica pressed for.
2. **Or pressure-test dramatic-sketch-01 with another story**
   (Macbeth / Karamazov / Remains-of-the-Day) against the
   shipped `dramatica-complete` template or against a different
   shipped Template. More encodings → more forcing functions;
   dramatic-sketch-02 gets more evidence.
3. **Or return to the parallel-dialect question** (Structural
   or another upper dialect), now that Dramatica-depth has
   been probed. The answer to "is Structural a genuine parallel
   pole" may depend on what the Dramatica template cannot
   reach — places the dialect genuinely cannot go are where a
   parallel dialect earns its place.
4. **Revisit the sandwich question.** With a rich top-of-stack
   (Dramatica-complete) and a rich bottom-of-stack (substrate
   + inference + identity + focalization + descriptions),
   architecture-sketch-02 can be re-examined for what — if
   anything — sits between.
