# Architecture — sketch 01

**Status:** draft, active
**Date:** 2026-04-13
**Supersedes:** nothing (new topic)
**Superseded by:** nothing yet

## Purpose

Capture the cross-cutting architectural commitments that frame every
substrate sketch. These commitments are not about *what* the substrate
represents (that is the domain of `substrate-sketch-NN`) but about
*what kind of thing the substrate is* and *where its authority ends*.

This sketch exists because the Rashomon encoding revealed schema drift
— predicates like `duel_character(A, B, "noble")` and the
`coerced`/`yielded_willingly` split — that did not trip any single
substrate commitment but added weight that a cleaner architectural
frame would have caught. The choices below are the frame.

This sketch is meta-level. It is referenced by substrate sketches and
by future topic sketches (event vocabulary, descriptions, inference
model). When a future sketch proposes adding something to the schema,
the tests below apply.

## What this sketch is *not* committing to

- Any specific schema, ontology, or vocabulary. Those are substrate
  sketches' domain.
- LLM provider, model, or integration surface.
- Authoring tools, UIs, or workflows.
- Any particular representation of descriptions beyond the shape of
  their surface (formalization is deferred to a descriptions sketch).

## What this sketch *is* committing to

1. **A1 — Grid-snap scope.** The substrate is a hybrid tool. Its
   schema grid-snaps *structural* facts that would otherwise drift
   under author or LLM freehand. It does not attempt to capture
   gradient, affective, or interpretive content. That content is
   first-class in the project but lives on a different surface (see
   A2).
2. **A2 — Two-surface semantics.** The substrate has two kinds of
   assertion, kept semantically distinct:
   - **Facts** — typed, truth-evaluable, fold-visible.
   - **Descriptions** — free-form, interpretive, fold-invisible.
   A description never promotes to a fact except by explicit
   authorial action.
3. **A3 — Test for schema inclusion.** Before a field, predicate, or
   event attribute is added to the schema, it must pass the
   constraint-against-drift test (below). If it fails, the content
   belongs in a description.
4. **A4 — Descriptions draft attention.** Descriptions are not
   unstructured blobs. They carry structural affordances — kind,
   attention level, review state — that make non-schema content
   visible *as* non-schema content. The surface actively solicits
   review from humans or LLMs rather than allowing silent skimming.
5. **A5 — Interpretation is a partner, not a fallback.** LLM (or
   human) interpretation of descriptions is a first-class part of
   the system, not a last resort for things the schema "could not
   figure out yet." The schema's refusal to schematize affect is a
   commitment, not a limitation to be overcome.

## A1 — Grid-snap scope

A metaphor the project uses: the substrate *grid-snaps* story
structure the way a vector tool grid-snaps a freehand line. The
underlying line is still freehand (a human or LLM has authored the
story). The grid does not draw the line for you. It constrains where
the line lands at structurally significant points — endpoints,
intersections, corners — so the line does not drift silently.

What the grid snaps:

- **Branch identity and fold scope.** Which branch is this event on?
  Which branches does the sjuzhet draw from?
- **Epistemic state.** Who knows what at τ_s? What slot
  (known / believed / suspected / gap)?
- **Precedence and temporal coordinates.** τ_s, τ_d, τ_a.
- **Preconditions and their satisfaction.** Does this event's
  precondition hold in the world state at its story-time?
- **Dramatic-irony, Sternberg-curiosity, and similar derivable
  queries** — computed by substrate algebra, not authored.

What the grid does not snap:

- The emotional weight of a moment.
- Whether a character's choice is noble or ignoble, warm or cold,
  believable or not.
- Authorial intent, tonal register, rhetorical effect.
- Anything that an attentive human reader or LLM would classify
  differently than a different attentive reader or LLM might.

## A2 — Two-surface semantics

The substrate represents assertions on two semantically distinct
surfaces:

**Facts.** Typed, truth-evaluable, fold-visible. Every fact is a
structured value — proposition, effect, event, branch label, slot
assignment. Facts compose. Facts can be true or false relative to a
branch fold. Facts participate in substrate queries; the fold sees
them.

**Descriptions.** Free-form, interpretive, fold-invisible. A
description is a text annotation attached to a typed anchor (an
event, an effect, a proposition, a sjuzhet entry). Descriptions
carry texture — motivation, affect, tonal shading, authorial
uncertainty — that a human or LLM reads and interprets. The
substrate passes descriptions through without reasoning over them.
The fold does not see them.

The separation is load-bearing. The two surfaces have different
semantics, different handling, different failure modes, and
different authority:

| | Facts | Descriptions |
|---|---|---|
| Shape | structured | free text (with metadata) |
| Truth | truth-evaluable | not truth-evaluable |
| Fold-visible | yes | no |
| Promotable by machine | n/a | no — author only |
| Queryable | yes | no |
| Drift discipline | schema + tests | attention + review |

**Promotion rule.** A description never becomes a fact except by
explicit authorial action. An LLM reading a description may *propose*
a fact; promotion is always an author act. The substrate must not
offer an automated path from description to fact.

**Precedent.** The current substrate's `provenance` field on Held
records is a proto-description surface: a tuple of unstructured
strings, never queried, used for audit and human inspection. The
descriptions sketch (next topic) should absorb and widen that
pattern into a proper surface.

## A3 — Test for schema inclusion

Before adding a field, predicate, or event attribute to the schema,
answer:

> *Would an attentive LLM or human author reliably catch drift in
> this content without the schema?*
>
> - If **yes** → the content belongs in a Description.
> - If **no** → the content belongs in the Facts grid.

Examples of drift the schema catches:

- Who knew what at when (agents cannot silently gain knowledge).
- Branch identity of an event (events cannot silently migrate).
- Whether a precondition holds (narrative inconsistency surfaces).

If a field does this kind of work, it is schema material.

Examples of content that fails the test:

- `duel_character(A, B, "noble")` — "noble" is a reader's
  interpretation, not a constraint. An LLM or author can determine
  it from prose just as reliably. Belongs in a description.
- `coerced(X, Y)` vs `yielded_willingly(Y, X)` — modality of an
  act. Same argument: interpretive, not structural. Belongs in a
  description attached to the act.
- `trust_level(agent, 0.7)` — scalar affect. Not constraint.
  Belongs in a description.

The test's teeth: if a sketch proposes a schema field that an LLM
reading well-written prose could extract with comparable reliability,
that field probably does not belong in the schema.

## A4 — Descriptions draft attention

Descriptions are not unstructured blobs floating in string fields.
They have enough structure to make themselves visible, and to invite
review rather than silent acceptance.

The descriptions sketch will formalize the exact shape. This sketch
commits only to the surface's purpose: every description-carrying
tool — inspector, linter, sjuzhet renderer, anything that walks the
fabula — must also walk descriptions and present them, loudly,
alongside the facts they annotate. A description cannot be silently
dropped from a reviewable view.

Elements the descriptions sketch is expected to include:

- **kind** — what sort of interpretation this is (texture, motivation,
  reader-frame, authorial-uncertainty, trust-flag, …).
- **attention** — categorical, not ordinal. Tells a reviewer *what
  kind of scrutiny* this description warrants:
  - `structural` — this description bears on how a nearby fact
    should be read. Must be reviewed; can change interpretation of
    the grid around it.
  - `interpretive` — meaningful texture a reader or LLM should
    consider when reading the scene. Should be reviewed.
  - `flavor` — background color. Review is optional.
- **review state** — unreviewed, LLM-reviewed, author-approved.
  An unreviewed `structural` description is itself a signal.
- **attached_to** — the typed anchor (event id, effect, proposition,
  sjuzhet entry) this description hangs off.
- **open-question marker** — optional; lets an author write a
  description-as-question that routes to a review queue.

Categorical attention is preferred over ordinal (low / medium /
high) because the level carries *why* — what kind of review this
needs — rather than *how much*. A three-point Likert scale invites
bikeshedding about whether something is medium or high; three
categories name the different jobs a reviewer would do.

The failure mode this prevents: descriptions sliding into the tool's
background and being treated as comments rather than as a parallel
interpretive surface. The substrate's commitment is that non-schema
content is visible *as* non-schema content.

## A5 — Interpretation is a partner, not a fallback

The substrate's refusal to schematize affect or texture is a positive
commitment, not a deferral. LLM or human interpretation of
descriptions is in-scope for the system as a whole, even though it is
out of scope for the substrate's fold.

This has a consequence worth naming: some questions the project
ultimately cares about — "does this irony land emotionally?" "does
this character's choice feel earned?" — will *never* be answerable by
substrate query alone. They require reading the descriptions and
forming a judgment. That judgment is a reader-model or
editor-in-the-loop act.

Design work elsewhere (reader-model sketch, authoring-UI sketches)
will cover how interpretation is invoked, cached, reviewed, and
integrated with structural queries. This sketch only fixes the
division: *the substrate refuses to do this work, and that is the
right division of labor.*

## Relation to substrate-sketch-04

Substrate-sketch-04 remains the current substrate statement. Its
structural commitments — E1–E3 (event-primary, typed, tri-temporal),
T1 (contested fabula), K1 (per-agent knowledge projection), K2 (reader
as epistemic subject with disjoint update operators), B1 (branch
kinds), L1 (library operators) — are all grid-snap territory and pass
A3 cleanly. Reading substrate-sketch-04 alone still gives the
reader the substrate's current shape.

Two specific points of interaction are worth naming rather than
hiding.

**F1 is retired.** Substrate-sketch-04 commits to "Emotion and
tension as parallel projections with the same discipline as
knowledge." That is exactly the kind of affective/interpretive
content A3 says the schema must not attempt to capture, and F1 was
overreach. Architecture-01 retires it:

- Affect, mood, and tonal content are descriptions attached to
  events (or effects, or sjuzhet entries) per A2. They do not form
  a parallel typed projection.
- Any pacing / tension-management query that is genuinely structural
  (e.g., "what open narrative questions exist at τ_d?", "which
  reader-gaps are overdue for resolution?") is reformulated as a
  query over description kinds and fact-level gap state — not as a
  query over a separate affect projection.
- There is no substrate-level "tension level" scalar, curve, or
  projection. If the project later needs tension-shaping tooling, it
  lives above the substrate and consults descriptions + epistemic
  state.

F1 is not currently exercised by the prototype (neither the Oedipus
nor Rashomon encodings use emotion or tension projections), so this
retirement is a forward commitment rather than a breaking change.
The formal removal from the substrate lineage lands when
substrate-sketch-05 (event vocabulary) supersedes substrate-sketch-04;
in the meantime, no new work should start to exercise F1.

**Provenance is proto-description.** Substrate-sketch-04 treats
`provenance` as a minimal unstructured trail on Held records. A2 and
A4 name this as the seed of the descriptions surface. The
descriptions sketch is expected to absorb and widen provenance —
same role, more structure, more visibility. This is a widening, not
a contradiction; sketch-04's treatment remains correct within its
own scope.

No other sketch-04 commitments are in tension with architecture-01.

Work to do, in sketch order:

1. **Event-vocabulary sketch (substrate-sketch-05).** Carves the
   event grid's joints. Applies A3 to event attribute choices. Hands
   interpretive content off to descriptions explicitly. Retires the
   Rashomon-specific encoding ugliness where that encoding tried to
   schematize interpretation.
2. **Descriptions sketch (descriptions-sketch-01).** Formalizes A2
   and A4. Specifies the description record's fields, attached_to
   targets, attention levels, and review states. Absorbs and widens
   `provenance`.

After those land, a consolidated substrate sketch (substrate-sketch-06
or beyond) can integrate the structural substrate with the
descriptions surface as a unified statement.

## Open questions

1. **What counts as "explicit authorial action" for promoting a
   description to a fact?** A UI click? A commit? An annotation
   field? The promotion rule is declared (A2) but its operational
   shape is open.
2. **Can a description be attached to another description?**
   (Commentary on an interpretation.) Probably yes, but not urgent.
3. **Does the description surface have its own branch semantics?**
   A description attached to a `:b-wife`-only event lives on that
   branch. But a description that *compares* the four testimonies
   — where does that live? Probably on `:canonical` as a trans-
   branch annotation. Needs thought.
4. **Review state decay.** If a description is author-approved and
   then the event it annotates changes, should the review state
   drop back to unreviewed automatically? Yes, probably, but the
   trigger conditions need spelling out.
5. **LLM proposing facts from descriptions.** The promotion rule
   forbids automatic promotion, but a proposal queue ("the LLM
   suggests this fact based on description X") is useful and
   consistent with A5. Where that lives (substrate-adjacent tool?
   descriptions sketch?) is open.

## Discipline

This sketch introduces rules. The rules only have teeth if applied.
Process expectations for future sketches and prototype work:

- Any proposed schema field is justified against A3 in the sketch
  where it is introduced. If a field cannot pass the test, the
  sketch says so and routes the content to a description instead.
- Any field that fails retroactively (as Rashomon's
  `duel_character` did) is flagged in the sketch that removes it,
  with a note pointing at A3.
- Descriptions get first-class treatment in tooling outputs. If the
  prototype renders a scene, it renders descriptions alongside facts.
- The test-for-schema-inclusion is not a blocker that kills useful
  fields; it is a prompt for honest framing. Fields can still be
  added if they genuinely earn it. The burden is explicitness.
