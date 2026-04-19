# Substrate Prop literal — sketch 01

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (new topic — record-shape detail for the
Prop literal substrate-sketch-05 §Ontology names but does not
structurally specify)
**Frames:** [substrate-sketch-05](substrate-sketch-05.md)
(§Ontology: "Proposition. A fact-shaped claim about entities at
a story-time. Propositions are not stored directly; they are
derived from the event log"; clarified below), [architecture-
sketch-01](architecture-sketch-01.md) A3 (drift discipline)
**Related:** [substrate-effect-shape-sketch-01](substrate-effect-
shape-sketch-01.md) (primary consumer: every WorldEffect + every
KnowledgeEffect carries a Prop); [descriptions-sketch-01](
descriptions-sketch-01.md) (secondary consumer: the
PropositionAnchor variant of Description.attached_to carries a
Prop literal; descriptions-sketch-01 §Required fields gestures
at this without defining the shape); [substrate-entity-record-
sketch-01](substrate-entity-record-sketch-01.md) (Entity-id
references in Prop args resolve against this);
[production-format-sketch-01](production-format-sketch-01.md)
(§PFS2 catches real drift surfaced the PropPlaceholder under-
specification as a forcing function — this sketch closes that
forcing function)
**Superseded by:** nothing yet

## Purpose

Structurally specify the Prop record — the **literal** form of a
proposition as it appears inside effects, description anchors,
and event preconditions. Substrate-sketch-05 §Ontology made the
ontological commitment ("a fact-shaped claim about entities at
a story-time") and the derivation claim ("propositions are not
stored directly; they are derived from the event log"), but
both claims are about propositions as *derived facts* — what the
`project_world` fold returns. The literal form — the hashable
tuple an author writes into `WorldEffect(prop=...)` or
`KnowledgeEffect(prop=...)` — has never been structurally
specified at the sketch level.

That gap is what `schema/description.json`'s `PropPlaceholder`
$def honestly flagged. This sketch closes it.

**Distinct from derivation.** This sketch is about the **input
shape**: what does an author write to assert or refer to a
proposition? The fold consumes Props as input to produce a Held
set or a world state; the folding mechanism is substrate-
effect-shape-sketch-01 + a future `substrate-knowledge-fold-
sketch-01` / `substrate-world-fold-sketch-01` work. Those
sketches describe *projection*; this one describes the *literal*.

**Derivation discipline.** First-principles from the substrate's
usage: Props appear as literals in three contexts (effects,
anchors, preconditions); the shape needs to serve all three,
with identity / equality / hashability as the load-bearing
invariant. The Python prototype's `Prop(predicate, args)` is a
conformance check; divergences resolve by sketch, not by
Python-match.

## Why now

- Effect-shape-sketch-01 landed with Prop as a type-reference;
  every WorldEffect and KnowledgeEffect example cites a Prop
  without its shape being defined. Unblocks effect schemas.
- Descriptions-sketch-01's PropositionAnchor variant was
  stubbed as `PropPlaceholder` in `schema/description.json`;
  this sketch provides the concrete type to replace the
  placeholder.
- Production-format-sketch-01 §PFS2 catches real drift named
  `substrate-prop-literal-sketch-01` as a specific forcing
  function. Writing this sketch is the resolution.
- Corpus survey (126 Prop instances across 102 events in 5
  encodings) confirms the shape's scope: 56 distinct
  predicates, arity 1/2/3, 229 string args + 1 int arg. Small
  enough that a clean sketch can land all the structural
  questions.

## Scope — what the sketch covers

**In:**

- The Prop record's field shape: `predicate` + `args`.
- The predicate's type (string) and vocabulary policy (open per
  story; no closed substrate enum).
- The args tuple's type and the admissible arg-value types.
- Equality / hashability invariants (Props are
  identity-by-structure, load-bearing for fold implementations
  that use Props as dict keys or set members).
- Arity policy (not enforced at Prop record level; semantic
  per-predicate).
- Corpus-observed structural primitive (the `fought_rounds`
  int arg) and the principled justification for admitting
  primitive-valued args alongside Entity-id args.

**Out:**

- **Predicate vocabulary policing.** The substrate does not
  maintain a closed set of predicates. Each story authors what
  it needs; classifier / verifier layers (LT2 retraction
  detector; EK2 external-action detector; SC2's `scheduled_*`
  prefix recognition) read predicates by pattern, not by
  enumeration. See OQ1.
- **Arity-per-predicate.** The substrate does not enforce "every
  `killed(X, Y)` has exactly two args". If an author writes
  `killed(X)` or `killed(X, Y, Z)`, that is authored shape;
  tooling may warn, but no substrate invariant is violated.
- **Argument-type-per-predicate.** The substrate does not know
  that `at_location`'s second arg should be an Entity of
  kind=location. Verifier machinery (dialect-layer) may
  enforce; the Prop record does not.
- **Negation.** This sketch's Prop has no negation field. A
  WorldEffect carries `asserts: bool` for polarity
  (substrate-effect-shape-sketch-01 ES2); a KnowledgeEffect
  has no polarity (via encodes direction, ES3). Proposition-
  anchored descriptions carry a Prop *literal* — if an author
  wants to point a description at a "not-P" proposition, the
  convention is a separate Prop literal, not an inverse. See
  OQ3.
- **Quantification / higher-order.** No `for_all X: P(X)` or
  `exists X: P(X)`. Props are ground. If a story needs
  quantified structure, the author encodes per-witness
  propositions explicitly. See OQ4.
- **Composite values inside args** (tuples, lists, dicts, sub-
  Props). Out — see PL5.

## First-principles commitments

Labels **PL** (Prop Literal).

### PL1 — Prop is a (predicate, args) pair

Prop is exactly two fields:

- **`predicate`** — a non-empty string. The relation name.
- **`args`** — an ordered tuple (n ≥ 0) of atomic values.

No other fields. Temporal coordinates (τ_s, τ_a) come from the
containing record (Event for effects and preconditions,
Description for PropositionAnchor). Branch scope comes from
the containing record too. Authored-by comes from the
containing record. A Prop is a literal structural fact; its
presence in the fabula is what gives it temporal and branch
meaning.

### PL2 — Predicate is a string from an open per-story vocabulary

The substrate does not maintain a closed predicate enum. Each
encoding authors the predicates it needs; the only substrate
commitment is that a predicate is a non-empty string.

Why open:

- **The corpus has 56 distinct predicates across 5 encodings.**
  A closed substrate enum would either be enormous (to
  anticipate every encoding's needs) or forever incomplete
  (as encodings author new predicates).
- **Pattern-matching classifiers work by prefix / structural
  shape, not by enumeration.** `scheduled_*` (SC2) matches on
  prefix; `identity` (identity-and-realization-sketch-01) is a
  reserved substrate-level predicate the substrate is free to
  recognize specially. A mixed closed-plus-open model would
  have to carve out the substrate's reserved subset and
  allow user extensions — harder than "every string is a
  predicate; the substrate knows some by name, is silent on
  the rest".
- **The discipline for good predicate naming lives in
  design-sketch text**, not in a substrate-level allowlist.
  Sketch-05 §M1 tells authors when to reach for a new
  predicate (structural downstream consequence) vs. a
  description (no fold consequence). Authors apply M1;
  substrate does not police.

Substrate-reserved predicates (those the substrate itself
inspects by name) are documented per-consumer. Known at v1:

- `identity(A, B)` — identity-and-realization-sketch-01's
  realization machinery reads `identity` specially.
- `at_location(X, L)` — unity-of-place checks read this
  predicate (aristotelian-sketch-01 A6).

More may appear; a future sketch may codify a substrate-
reserved-predicate registry if pressure accumulates. For v1
there is no enum, no registry — just two documented reserved
names that specific machinery happens to care about.

### PL3 — args is an ordered tuple of atomic values

The args tuple is ordered; position is load-bearing
(`killed(A, B)` is not `killed(B, A)`). The tuple may be empty
for nullary propositions (rare; a predicate-with-no-args asserts
a binary proposition-valued fact like `dawn_broke` or
`war_ended`; the current corpus has none but the shape admits
them).

Arity is not substrate-enforced. A predicate that appears with
2 args on one event and 3 args on another is a smell (the
encoder has inconsistent authoring), but the Prop records are
individually well-formed. Verifier tooling may catch cross-
occurrence inconsistency.

### PL4 — Each arg is a string, int, float, or bool

The admissible arg value types form a closed primitive set:

- **string** — an Entity id reference. Resolution: the string
  should equal the `id` field of some Entity record in the
  encoding's ENTITIES. The substrate does not check resolution
  at Prop-record-construction time — a broken reference is a
  cross-record integrity finding, surfaced by the verifier or
  by downstream tooling, not a Prop well-formedness violation.
- **int** — a numeric literal that has structural downstream
  consequence (fold, verifier, rule-based derivation). The
  corpus contains exactly one as of this sketch's writing:
  `fought_rounds(rocky, apollo, 15)`, which feeds Rocky's
  `WENT_THE_DISTANCE_RULE` derivation.
- **float** — a numeric literal with a fractional component.
  No corpus instance yet, but the substrate admits: a story
  with a structural distance measure or a prob-weighted
  derivation would use float.
- **bool** — a true/false literal. No corpus instance yet, but
  admissible: a predicate like `alive(X)` could theoretically
  bind a bool as its target-state-value instead of using two
  separate predicates `alive(X)` / `dead(X)`. In practice the
  corpus uses paired predicates (the `dead` predicate appears
  14 times; no corresponding `alive` with bool-arg).

### PL5 — No nested / composite / null values in args

An arg is an atomic primitive. Excluded:

- **Tuples, lists, dicts inside args.** A Prop with list-valued
  args would be saying "A killed B with either sword OR
  dagger" — which is two Props: `killed_with(A, B, sword)`
  and `killed_with(A, B, dagger)`, possibly on different
  branches. Composite structure inside a single Prop is a
  smell; a predicate needing to pack structure into args is
  doing too much.
- **Sub-Props.** No `caused_by(P1, P2)` where P1 and P2 are
  Props. Higher-order logic over propositions would need a
  Held-or-reification machinery beyond v1 substrate scope. A
  causal chain is modeled as event-to-event ordering (sketch-05
  event-log), not as nested propositions.
- **`null` / `None`.** No sentinel "unknown" or "any" value.
  An agent not knowing something is a Held-state slot (Gap
  or Blank); a predicate with a missing arg is ill-formed,
  not "partially specified".
- **Other object types.** No datetime, no regex, no custom
  classes. The substrate's cross-language portability
  (memory: `feedback_python_as_spec` — "favor explicit /
  translatable") argues for atomic primitives that every
  serializer / deserializer handles consistently.

### PL6 — Equality is structural

Two Props `(predicate=p, args=a)` and `(predicate=p', args=a')`
are equal iff `p == p'` and `a == a'` element-wise. This makes
Props:

- **Hashable.** A set of Props can be used as an agent's Held-
  set (identity-and-realization-sketch-01's substitution
  semantics relies on Held-set membership being decidable in
  constant time).
- **Deduplicable.** Two events that both assert
  `at_location(X, L)` at different τ_s do not multiply the
  fact; the fold sees one assertion-state.
- **Keyable.** `project_world(τ_s, branch) → { Prop: bool }`
  keys on Prop; the mapping would be ill-defined without
  structural equality.

This is not a field; it is a behavioral invariant. Any
implementation — Python, Rust, TypeScript, JSON Schema
validator equivalence-class — MUST preserve it.

### PL7 — Prop literals are timeless at record level

Parallel to substrate-entity-record-sketch-01 SE5 and
substrate-effect-shape-sketch-01 ES7: a Prop literal carries no
τ_s, τ_a, or branch. Presence in the fabula at a particular
(τ_s, branch) comes from the containing Event; in a
Description's PropositionAnchor, from the containing
Description's τ_a and branch scope.

A Prop literal is fungible across containers: the *same* Prop
`killed(oedipus, laius)` appears in an event's effect, in a
description's anchor, and potentially in a future event's
preconditions. Its identity is structural; each occurrence
gets temporal meaning from its container.

## Worked examples

### Entity-id args (the common case — 229/230 corpus)

```
Prop(predicate="killed", args=("oedipus", "laius"))
Prop(predicate="at_location", args=("husband", "grove"))
Prop(predicate="identity",
     args=("oedipus", "stranger_at_crossroads"))
Prop(predicate="scheduled_fight", args=("apollo", "rocky"))
Prop(predicate="king", args=("oedipus",))               # arity 1
```

Each string in args resolves to an Entity id (substrate-
entity-record-sketch-01 SE2). The Prop literal is the same
object whether it appears in a WorldEffect, a KnowledgeEffect,
or a Description's PropositionAnchor.

### Primitive-valued arg (corpus case: fought_rounds)

```
Prop(predicate="fought_rounds", args=("rocky", "apollo", 15))
```

Structural justification: Rocky's `WENT_THE_DISTANCE_RULE`
derivation reads `fought_rounds(X, Y, N)` and derives
`went_the_distance(X, Y)` when `N >= 15` and
`standing_at_final_bell(X)` holds. The `15` participates in
rule application; it is fold-visible structural data per
sketch-05 §M1.

This is the only corpus instance as of 2026-04-19. The shape
admits it without sketch amendment. A future encoding needing
float (distance in miles; probability weights) or bool (a
two-valued predicate with its value as an arg) is similarly
covered.

### Nullary prop (admitted but uncorpsed)

```
Prop(predicate="dawn_broke", args=())
```

A nullary Prop asserts a binary-truth-valued fact with no
arguments. Admissible per PL3 (empty tuple is a valid tuple).
No corpus instance yet; shape admits.

### Not-a-Prop (what's rejected under PL5)

```
# Nested list — rejected
Prop(predicate="killed_with", args=("A", "B", ["sword", "dagger"]))

# Sub-Prop — rejected
Prop(predicate="caused",
     args=(Prop("killed", ("A", "B")), Prop("stole", ("A", "C"))))

# Null — rejected
Prop(predicate="at_location", args=("X", None))

# Dict — rejected
Prop(predicate="meta", args=({"kind": "event", "id": "E1"},))
```

Each of these requires modeling the structure by different
primitives: two separate `killed_with` Props on different
branches; two events with event-log ordering expressing
causation; a predicate that doesn't bind the "null" arg vs.
one that does (distinct predicates); a reserved predicate
whose args are a single Entity id pointing at a dict-carrying
metadata Entity of kind=abstract.

## Not in scope

See §Scope "Out". Key re-emphases:

- **Predicate vocabulary policing.** Out. Open per story.
- **Arity enforcement.** Out. Per-occurrence well-formedness
  only; cross-occurrence consistency is a verifier concern.
- **Negation.** Out. Asserts-polarity lives on WorldEffect,
  not Prop (ES2).
- **Quantifiers / higher-order.** Out. Props are ground.
- **Structured / composite args.** Out per PL5.

## Open questions

1. **OQ1 — Substrate-reserved predicate registry.** Two
   predicates (`identity`, `at_location`) are already read by
   name by substrate / dialect machinery. If a third or fourth
   reserved predicate appears, a registry sketch consolidates
   them. Forcing function: ≥ 3 reserved predicates, OR
   conflict between two encodings over a predicate name's
   meaning. Neither holds today.
2. **OQ2 — Predicate signature declarations.** A future
   encoding might want to declare "`at_location(X, L)` expects
   X: Entity, L: Entity kind=location" and have the substrate
   verify per-Prop. This is a predicate-signatures sketch;
   forcing function is a verifier-desired check that doesn't
   yet exist. Not forced at v1.
3. **OQ3 — Negation convention.** No Prop negation field. If
   a proposition-anchored Description wants to point at
   "not-P", today's convention is a separate Prop literal
   (e.g., `alive(X)` and `dead(X)` as paired predicates). If
   an encoding forces a "point at not-P" use case, a sketch
   revisits — possibly adding a `negated: bool` field (parallel
   to WorldEffect's asserts). Corpus has none today.
4. **OQ4 — Quantified propositions.** Props are ground. A
   future encoding needing "every guest was poisoned" as a
   structural fact (not a flood of per-guest Props) would
   force a quantified-Prop sketch. Candidate name:
   `substrate-quantified-prop-sketch-01`. Not forced at v1 —
   And Then There Were None, the natural pressure-case for
   quantified-over-suspects propositions, is unauthored.
5. **OQ5 — Args containing other story-domain primitives**
   (τ_s timestamps as int args; branch labels as string args).
   A Prop `witnessed_at(X, E, τ_s=5)` embedding a τ_s value is
   legal under PL4 (int is admissible) but tangles with event-
   level τ_s: if the witnessing is an event, its τ_s is the
   event's; an additional τ_s int arg is duplicating. Corpus
   has no instance; banked.
6. **OQ6 — Unicode / normalization of predicate strings.** A
   Prop `killed(A, B)` and `killed(A,B)` (whitespace) and
   `Killed(A, B)` (case) should all be... equal? Non-equal?
   The sketch commits: non-equal (structural equality is
   literal). Encoders keep predicate names stable by
   convention. A normalization sketch re-opens if a forcing
   function appears; today none.

## Discipline

- **Shape-before-schema.** Written at design-sketch-level so
  the production-layer schema
  (`schema/prop.json`, eventual) has a source of truth.
- **Atomic args.** PL5's closed primitive set is load-bearing.
  Admitting nested / composite structure invites the same
  predicate proliferation memory `feedback_schema_drift`
  warns about — predicates absorbing richness that belongs in
  descriptions or in event-log structure.
- **Open predicate vocabulary + grid-snap routing.** Authors
  reach for a new predicate only when M1 says so
  (sketch-05 §M1 — downstream structural consequence
  required). The substrate does not enforce this; the
  discipline does.

## Summary

Record-shape sketch for the Prop literal.

- Two fields: `predicate` (non-empty string; open per-story
  vocabulary) + `args` (ordered tuple of atomic primitives).
- Atomic primitives are exactly {string, int, float, bool}. A
  string arg is an Entity-id reference; int / float / bool are
  literal values with structural fold-consequence.
- No nested structures, sub-Props, nulls, or dicts inside
  args (PL5).
- Structural equality + hashability (PL6) — load-bearing for
  fold implementations that key on Props.
- Timeless at record level (PL7); temporal / branch
  coordinates inherit from the containing record.

Unblocks two consumers:

- `schema/event.json` (via substrate-effect-shape-sketch-01's
  WorldEffect.prop / KnowledgeEffect.prop fields; both resolve
  to this Prop shape).
- `schema/description.json`'s `PropositionAnchor` variant —
  the `PropPlaceholder` $def can be replaced with a concrete
  Prop schema in a future `production-format-sketch-03`.

Six OQs banked, all with forcing-function criteria. No
substrate or dialect record change forced; the corpus's 126
Prop instances all conform (229 string args + 1 int arg, all
satisfying PL4).

The sketch's load-bearing discipline: **a Prop is a
ground-term fact; complexity lives elsewhere** — in events
(for temporal structure), branches (for contested structure),
descriptions (for interpretive texture). Grid-snap at the
proposition layer.
