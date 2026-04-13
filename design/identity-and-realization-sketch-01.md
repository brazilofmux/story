# Identity and realization — sketch 01

**Status:** draft, active
**Date:** 2026-04-13
**Supersedes:** nothing (new topic)
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [substrate-sketch-05.md](substrate-sketch-05.md)
**Superseded by:** nothing yet

## Purpose

Address a concrete slice of substrate-sketch-05's open question 2
(the inference model) — the one with a clean failure mode and a
forcing function. Jocasta's anagnorisis in the Oedipus encoding is
currently faked: a "realization" event manually removes old
propositions and adds new ones. The removal/addition is authored,
not derived, which means the substrate does not actually represent
what makes realization *realization*. It represents the outcome, not
the logical step.

What realization *is*: an agent learns that two entities the agent
had been tracking separately are in fact the same entity. Once that
assertion lodges, everything the agent already believed about either
entity applies to the other. No new domain facts are needed; what is
needed is *substitution under identity*.

This sketch commits to identity as a first-class proposition and to
substitution under identity as a query-time operation. It
deliberately does *not* add a general forward-chaining inference
engine. That work is bigger (substrate-05 open question 2 writ
large) and has a different shape; identity is a specific, bounded
piece that pays off the Oedipus encoding without opening the
inference-model door in full.

This sketch specifies:

- The identity proposition's shape and semantics.
- Per-fold scoping (world identity, agent identity, reader identity).
- Query-time substitution as the inference operation.
- Symmetry and transitivity of identity.
- How realization events produce identity assertions.
- Interaction with branches and with the reader's projection.
- What is explicitly *not* in scope (domain derivation rules,
  identity synthesis, negated identity, counterfactual identity).
- The relation to a future general inference-model sketch.
- A worked example using the Oedipus encoding.

## What this sketch is *not* committing to

- A general forward-chaining or Horn-clause inference engine.
  That is substrate-05 open question 2 writ large; this sketch is
  strictly narrower.
- Domain-specific derivation rules — e.g., "`exposed(X, C)` implies
  `child_of(C, X)`." Authors encode whatever domain relations they
  want in the event log directly; this sketch does not add an
  entailment layer beyond identity substitution.
- Identity inference *from* domain facts — e.g., "A and B were in
  the same location at the same time, therefore A=B." Almost always
  unsound; a library layer might *propose* identities for author
  review (via the reader-model proposal queue), but the substrate
  itself never synthesizes identity.
- Negated identity (`¬identity(A, B)` as a typed proposition).
  The substrate currently has no first-class negation mechanism;
  adding one is a separate decision. Tests of "the author does not
  assert identity(A, B)" are structural absences in the held set,
  not typed negations.
- Identity in counterfactual branches. The B1 fold-scope rule
  already handles per-branch identities; no special counterfactual
  machinery is needed.
- Realization events as new substrate construct. Realization is
  already a diegetic update operator (per substrate-sketch-04 K1,
  carried forward). This sketch sharpens what a realization *is*
  — it asserts an identity — without inventing a new event kind.

If a question starts "how do I write a rule that…" or "can the
substrate derive domain fact P from facts Q, R?" — it is out of
scope. Identity substitution is the whole inference budget of this
sketch.

## What this sketch *is* committing to

1. **I1 — Identity is a first-class proposition.** `identity(A, B)`
   is a `Prop` with distinguished semantics: it names two entity
   references as co-referential within the fold that holds it. The
   substrate treats `identity/2` as a reserved predicate name (per
   story: encoding-library extension is open via the usual
   per-story vocabulary rule).
2. **I2 — Identity scopes per fold.** A world-level identity lives
   in world state (asserted by a `WorldEffect`). An agent-level
   identity lives in that agent's held set (placed by a
   `KnowledgeEffect`). A reader-level identity lives in the
   reader's held set (placed by a narrative-update disclosure).
   Each fold applies identity substitution using only the identities
   in *that* fold. Alice's substitutions use Alice's identities, not
   the world's, not another agent's.
3. **I3 — Substitution is query-time, not commit-time.** An agent's
   held set remains literal — it contains exactly the propositions
   that were authored through effects. Substitution happens when the
   substrate is *queried* about the set ("does Jocasta hold P?"). No
   state mutation occurs at commit; no derived-fact storage; no
   truth-maintenance system. Identity + substitution is a pure view
   over the literal held set.
4. **I4 — Substitution is symmetric and transitive.** If agent
   holds `identity(A, B)`, then `P(…A…)` in the held set matches
   queries for `P(…B…)` and vice versa. If agent holds
   `identity(A, B)` and `identity(B, C)`, then `P(…A…)` also
   matches queries for `P(…C…)`. Identity chains compose; the
   query engine computes the transitive closure at query time.
5. **I5 — Realization is the epistemic trigger; identity is what
   realization produces.** Realization events already exist as a
   diegetic update operator. This sketch does not change the event
   kind or its machinery. It sharpens what a realization's payload
   is: the effect placed on the realizing agent is a
   `KnowledgeEffect` whose `Held.prop` is an `identity(A, B)`
   proposition. No old propositions are removed from the agent's
   held set; realization is additive. Downstream "she now knows X,
   Y, and Z" is query-time derivation via substitution, not a
   state-mutation cascade.
6. **I6 — The substrate does not fabricate identities.** Every
   identity in any fold is authored — by a world-effect commit, a
   diegetic knowledge-effect, or a narrative disclosure. The
   substrate never synthesizes `identity(A, B)` from other facts.
   A library operator or reader-model proposal may *suggest* an
   identity for author review; acceptance produces an authored
   event. Automatic synthesis from domain facts (co-location,
   shared attribute, etc.) is out of scope and almost always
   unsound.
7. **I7 — Substitution fires only on KNOWN identities.** An
   `identity(A, B)` proposition in an agent's held set produces
   substitution only when the Held's slot is KNOWN. Identities
   held as BELIEVED, SUSPECTED, or GAP do not participate in
   equivalence-class construction; queries over the agent's state
   behave as if those identities were not held. Rationale:
   realization is the anagnorisis trigger, which is epistemically
   "click into place" — partial or tentative identity belongs in
   story surface (the agent is working something out) rather than
   in substitution semantics. A later sketch may revisit this
   (SUSPECTED identity producing BELIEVED derived facts is a
   coherent richer model); sketch 01 takes the simple rule.

I1 through I7 pass architecture-sketch-01 A3: each describes drift
the schema catches, not content an attentive reviewer could
self-police from prose. Without I1, authors must manually rewrite
held sets whenever an identity is learned, which is exactly the
kind of cross-cutting drift the substrate's purpose is to prevent.

## Relation to prior sketches

- **Architecture-01 A3.** Identity machinery passes A3 as above.
  Identity is not interpretive; it is structural — it changes what
  an agent's held set resolves to, which in turn changes what
  queries answer. Interpretation (was her realization earned? did
  it land?) remains description territory.
- **Substrate-05 E1, K1, K2.** Identity respects all existing
  fold rules. Identity propositions are Props; they enter held sets
  via effects; they are folded per the existing per-agent,
  per-world, per-reader projections. What changes is query
  semantics, not fold semantics.
- **Substrate-05 M1 (adverbial/modal rule).** Identity has
  downstream structural consequence (it changes query answers about
  everything the agent holds involving the identified entities);
  per M1, it earns its own event / proposition shape rather than
  being a description. That is what I1 does.
- **Substrate-05 OQ 2 (inference model).** This sketch closes one
  bounded slice of OQ2. The larger inference model — domain
  derivation rules, proof-carrying inference, bounded forward
  chaining — remains open. This sketch explicitly is *not* the
  inference-model sketch.
- **Descriptions-01.** Identity is structural; it does not touch
  the description surface. Descriptions *about* an identity
  assertion ("she realizes it piecemeal; the first beat is the
  shepherd's detail") are ordinary descriptions attached to the
  realization event or to the identity proposition's effect. No
  new description machinery is needed.
- **Reader-model-01.** A reader-model may propose an identity
  assertion from a description (an LLM reading prose spots "these
  two characters are clearly the same person"). Proposals feed the
  promotion queue; an author accepts, producing an authored
  realization event. The firewall holds: the reader-model does not
  lodge identity into any held set directly.

## The identity proposition

### Shape

```
Prop(predicate="identity", args=(entity_a_id, entity_b_id))
```

A proposition in the substrate's existing `Prop` type. The
predicate name is `"identity"`; the arity is 2; the arguments are
entity ids (strings per the existing `Entity.id` convention). No
new record type; no distinguished subtype; no metaclass.

Canonical ordering: the substrate treats `identity(A, B)` and
`identity(B, A)` as distinct `Prop` values (because `Prop` is
compared by args-tuple equality), but substitution treats them
equivalently per I4. A canonicalization convention — store args in
sorted order — is a tooling simplification, not a substrate
requirement.

### What counts as an entity reference

Any string that is used as an `Entity.id` in the encoding. The
substrate does not distinguish "real" entities from placeholders
(`"the-exposed-child"` is as legitimate an entity id as
`"oedipus"` until a realization asserts their identity).
Authored-as-distinct, realized-as-same is precisely the shape
Oedipus needs.

### What is NOT an identity proposition

- Predicates other than `identity`. `same_as(A, B)`,
  `equivalent(A, B)`, `is_a(A, B)` — if authors use these, the
  substrate does not treat them as identities. Identity machinery
  is reserved to the `identity` predicate. (A later encoding-
  library can normalize synonyms.)
- Higher-arity identities. `identity(A, B, C)` has no defined
  meaning; arity-2 only. Authors needing three-way identity
  assert it as three pairs.
- Identity predicates with non-entity args. `identity("red",
  "crimson")` is a property-name identity, not covered by this
  sketch. Scope is entity co-reference.

## Substitution semantics

Substitution is the single inference rule this sketch adds. It is
pure, query-time, and reversible (unapplying means simply not
applying; no derived state to retract).

### The rule

Given a fold `F` (world, agent, or reader) and a set `I_F` of
`identity/2` propositions in that fold's held set, substitution
computes the transitive closure:

- Build an equivalence relation over the entity ids that appear as
  arguments in any `identity(A, B) ∈ I_F`. Every entity id in an
  identity chain is in the same equivalence class.
- For any proposition `P(…, x, …)` in the fold's held set and any
  query `P(…, y, …)`, substitution matches if `x` and `y` are in
  the same equivalence class (or are literally equal, the trivial
  case).

An agent "holds" proposition `P` under substitution if there exists
some literal `P'` in the agent's held set such that `P'` equals `P`
under the equivalence-class mapping.

### Examples

**Single identity, forward substitution.**

Agent holds:
- `loves(bob, carol)`
- `identity(bob, david)`

Query: does agent hold `loves(david, carol)`? *Yes*, via
substitution: `bob` and `david` are in the same class; `loves(bob,
carol)` matches.

**Transitive chain.**

Agent holds:
- `saw(alice, bob)`
- `identity(bob, david)`
- `identity(david, evan)`

Query: does agent hold `saw(alice, evan)`? *Yes*. The class is
`{bob, david, evan}`; all match.

**Reverse substitution.**

Agent holds:
- `child_of(the-baby, jocasta)`
- `identity(oedipus, the-baby)`

Query: does agent hold `child_of(oedipus, jocasta)`? *Yes*. The
literal term is `the-baby`; the query term is `oedipus`; they are
in the same class.

**Non-example — identity the agent does not hold.**

The world holds `identity(bob, david)`. Alice's state does NOT hold
the identity. Alice holds `loves(bob, carol)`.

Query on Alice: does she hold `loves(david, carol)`? *No*. Only
Alice's identities apply to her state; the world's identity does
not leak into Alice.

### Literal-set preservation

The held set itself is unchanged by query-time substitution. Two
observations matter:

1. **Fold determinism.** `project_knowledge(agent, events, τ_s)`
   returns the same held set before and after identity machinery
   lands. The set contains exactly the propositions the effects
   placed there. Identity substitution is a property of *queries
   over* the set, not of the set.
2. **Query surface is where the change appears.** `holds(p)`,
   `holds_as(p, slot)`, and similar query methods on
   `KnowledgeState` compute substitution. A caller that wants the
   raw literal set (e.g., for debugging or for a view that should
   surface the un-substituted facts) can still access
   `by_prop` directly.

The substrate exposes both: `holds(p)` (substitution-aware) and
`holds_literal(p)` (literal match only). Tooling picks per use
case.

### Multi-match resolution

`holds(p)` returns a `Held`, not just a boolean. Under substitution,
several literal records can match the same query. The return shape
must be deterministic.

**The rule.** Among all literal `Held` records that match `p` under
the equivalence-class mapping, return the one with the *strongest*
slot. Slot ordering, strongest to weakest: KNOWN > BELIEVED >
SUSPECTED > GAP. If multiple matches tie on slot, return the
record with the earliest `τ_a` (the first-authored belief is
canonical; later records that restate it are redundant).

**Rationale.** If an agent literally holds `P(a)` as KNOWN and
`P(b)` as BELIEVED with `identity(a, b)` known, asking "does the
agent hold P(a)?" should answer "yes, KNOWN" — their stronger
belief wins. This matches how beliefs integrate: knowing something
from one path and merely believing it from another yields net
knowledge. The tie-break to earliest τ_a is purely for
determinism.

**Provenance.** The returned `Held` carries its own literal
provenance. The substrate does not fabricate a merged-provenance
record by joining information across multiple matches; if a
caller wants the full set of matches, `holds_all_matches(p)`
returns every `Held` in slot-then-τ_a order.

**Exception — `holds_literal(p)`.** Always returns the literal
`Held` whose `prop` is exactly `p`, with no substitution, no
multi-match resolution. Useful for testing invariants on the
raw set.

## Symmetry and transitivity (I4)

### Symmetry

`identity(A, B)` implies substitution works both directions. The
agent does not need to separately assert `identity(B, A)`.
Canonicalization is a tooling question; the substrate's
substitution is symmetric by implementation.

### Transitivity

Identity chains compose. If the held set contains `identity(A, B)`
and `identity(B, C)`, substitution treats `A`, `B`, and `C` as one
equivalence class.

The transitive closure is computed at query time, once per query.
Naive implementation: union-find over the held set's identity
propositions; amortized near-linear. For the prototype's scale the
closure is computed per call; memoization is a future optimization.

### No reflexivity check

`identity(A, A)` is a trivially true proposition. The substrate
does not treat it specially. An author who asserts it is asserting
something tautologically correct but useless; linting can flag it,
but it is not an error.

### Contradictions

If Alice holds `identity(A, B)` and `identity(B, C)`, she also
holds (via closure) `identity(A, C)`. Suppose the story also has
some other fact Alice holds that would be semantically incompatible
with `A = C` — e.g., `different_from(A, C)` is in her state. The
substrate does not police consistency; Alice holds a contradictory
belief. That is data about Alice, not a substrate error. If the
story wants "Alice realizes the contradiction," the author writes
that realization.

## Realization and identity

### Realization events in the current substrate

The existing `Diegetic.REALIZATION` operator (substrate.py) is a
knowledge-update operator. A realization event carries a
`KnowledgeEffect` whose `Held.via` is `"realization"`. Semantically
it marks the effect as the diegetic moment at which the agent
gained this belief through insight rather than observation or
utterance.

### What realization places

Under this sketch: a realization event's payload is a
`KnowledgeEffect` whose `Held.prop` is an `identity(A, B)`
proposition, placed into the realizing agent's held set.

What realization does *not* do:

- It does not remove prior propositions from the agent's held
  set. The old beliefs (pre-identity) stay literal; substitution
  handles the rest.
- It does not compute a diff of "what the agent now believes
  differently." That diff is a query-time comparison between the
  literal held set and the substitution-aware held set; it is a
  *derived* quantity, not a substrate commitment.
- It does not assert anything about the world. An agent's
  realization is their epistemic update; the world state is
  unaffected unless the story also authors a world effect
  (usually not — realizations are internal).

### Prior encoding's workaround, and its retirement

The current Oedipus encoding fakes realization by authoring a
realization event that *removes* old propositions (e.g.,
`stranger_at_crossroads_lives`) and *adds* new propositions
(e.g., `killed(oedipus, laius)`). This works but misrepresents
what happened: Jocasta didn't gain `killed(oedipus, laius)` by a
miracle of insight; she gained `identity(stranger, oedipus)` and
her already-held `killed(stranger, laius)` substitutes.

Under this sketch, the encoding is rewritten to:

- Author the per-agent relational facts explicitly (Jocasta's
  knowledge of who she married, who her child was, where they
  ended up, whom she heard killed whom).
- Realization events assert identities; remove nothing.
- Queries that previously checked for `killed(oedipus, laius)`
  continue to succeed — via substitution, not via state mutation.

This is the refactor the Oedipus prototype iteration will apply
when this sketch's probe lands.

### Non-realization identity sources

Not every identity assertion is a realization. Three other
sources are legitimate:

- **World-level identity.** A `WorldEffect(identity(A, B))`
  asserts the identity into world state. Useful for encoding a
  truth the author wants queryable even if no in-story agent
  knows it (e.g., "Oedipus IS the stranger, whether or not
  anyone has realized it").
- **Observation / utterance-heard.** An agent may be *told* an
  identity rather than *realize* it. The `Held.via` field
  distinguishes; semantically both produce the same substitution
  result.
- **Reader disclosure.** The narration informs the reader that
  two entities are the same. This is a `Disclosure` whose `prop`
  is an `identity` Prop; it lodges into the reader's state.

The distinction between these sources is diegetic — who placed
the belief, by what means. *Substitution behavior is not a
function of source.* Per I7, substitution fires when the
resulting `identity(A, B)` is held at slot=KNOWN; if a source
lodges the identity at BELIEVED or SUSPECTED (a rumor an agent
only half-trusts, a hint the reader suspects but is not told
outright), substitution does not fire. A realization placing an
identity at KNOWN and an utterance placing the same identity at
KNOWN substitute identically; a realization at KNOWN and an
utterance at BELIEVED do not.

So: source affects diegesis; slot affects substitution. The two
axes are orthogonal.

## Interaction with branches

Identity follows B1. A `WorldEffect(identity(A, B))` on a
contested branch lives on that branch; per the fold-scope rule,
sibling contested branches do not inherit it. A `KnowledgeEffect`
placing `identity(A, B)` into an agent's state on a specific
branch lives there.

Concretely: one branch can assert `identity(stranger, oedipus)`
and a sibling branch can refuse to (or assert `identity(stranger,
someone-else)`). This is contested-identity — same agent's
substitution differs per branch, which is correct.

## Interaction with the reader

The reader holds identities the same way agents do. A reader's
`holds(p)` query substitutes through the reader's known
identities. This has a direct application to dramatic irony:

- Reader knows `identity(oedipus, stranger)`.
- Jocasta knows `killed(stranger, laius)` but not the identity.
- Query: does the reader hold `killed(oedipus, laius)`? Yes, via
  substitution over reader's own disclosures plus reader's known
  identity.
- Query: does Jocasta hold `killed(oedipus, laius)`? No (until
  the realization event). The substrate reports a reader-over-
  character irony.
- Post-realization: Jocasta gains `identity(stranger, oedipus)`;
  substitution fires on her state; the irony collapses.

This is exactly the pattern the Oedipus demo already produces,
but derived cleanly from the substitution rule rather than
manufactured by a hand-authored realization that happens to
rewrite Jocasta's beliefs into the right shape.

## What is and is not in the inference budget

### In scope for this sketch

- Identity as a first-class proposition.
- Substitution under identity as a query-time operation.
- Symmetry and transitivity.
- Realization events producing identity assertions.
- `holds`, `holds_as`, and dramatic-irony queries gain
  substitution-aware behavior.
- A substitution-aware query surface for world state
  (`world_holds`), mirroring the agent-state query change.
- `sternberg_curiosity` remains literal (see below).

### Sternberg-curiosity stays literal

The GAP slot is an explicit authorial marker for "this agent is
aware there is an open question about this proposition."
Substitution does not auto-resolve acknowledged gaps: an agent
who has committed a GAP record is asserting awareness of the
open question, independent of whether substitution could now
derive an answer via identity. If the author wants "the gap
resolves at realization," they author a `KnowledgeEffect` with
`remove=True` targeting the GAP record — the same mechanism
that has always been available.

This makes sternberg_curiosity consistent with the literal-set
discipline of I3: the GAP slot is part of the literal set; the
literal set changes only via authored effects. Substitution is
a property of queries about *what is held*, not about *what is
acknowledged as open*.

Irony, by contrast, is a *derived* comparison across two agents'
substitution-aware states. It is fully derived; no authorial
"irony is live here" marker exists. So irony composes with
substitution cleanly; curiosity does not.

### Out of scope (deferred)

- **Domain derivation rules.** `exposed(X, C) ⇒ child_of(C, X)`
  is a story-specific relational inference. If an encoding needs
  it, the encoding authors the consequent facts explicitly. A
  future inference-model sketch may introduce a rules engine; this
  sketch does not.
- **Negated identity.** `¬identity(A, B)` as a typed proposition.
  Requires substrate-level negation, which the current substrate
  does not have.
- **Identity discovery.** The substrate does not derive
  `identity(A, B)` from other facts. If an encoding wants to
  suggest identities to the author (e.g., "these two agents share
  many attributes — maybe they are the same?"), that lives in a
  library or reader-model probe; it proposes for author review
  (per reader-model-01), never synthesizes autonomously.
- **Identity decay.** Once lodged, an identity stays. If an
  author retracts it, they author a retraction event (using the
  existing remove-effect mechanism on `KnowledgeEffect`); the
  substrate does not forget identities on its own.
- **Equality over compound terms.** `identity(father(bob),
  father(david))` — identity over function-applied entities — is
  not supported. The Prop grammar is flat args; compound
  identities are out of scope.

### Distinction from the general inference model

Substrate-05 OQ 2 names the inference-model work as a general
open question. This sketch does not close it; it carves out the
one slice that pays off Oedipus's forcing function. The general
inference model — domain rules, proof carrying, bounded forward
chaining — remains OQ 2 post-this-sketch. A successor sketch
(`inference-model-sketch-01`) will take it up with a wider scope.

The clean division: *identity substitution* is the inference every
realization requires; *domain derivation* is the inference some
encodings additionally want. First one is universal enough to be
substrate machinery; second is optional and story-shaped, so it
lives a layer above.

## API implications

### New or modified query functions

- **`holds(p)` on `KnowledgeState`.** Gains substitution-aware
  semantics by default, scoped to KNOWN identities per I7.
  Multi-match resolution per the strongest-slot rule above. The
  literal match is still available via `holds_literal(p)`.
- **`holds_literal(p)` on `KnowledgeState`.** New. Literal
  match against `by_prop` only; no substitution. Useful for
  debugging, for rendering an agent's "un-realized" beliefs, and
  for pinning the literal-set-preservation property in tests.
- **`holds_all_matches(p)` on `KnowledgeState`.** New. Returns
  every `Held` that matches under substitution, in slot-then-τ_a
  order. Callers that need the full substitution set (not just
  the strongest) use this.
- **`equivalence_classes()` on `KnowledgeState`.** New. Returns a
  list of sets, each a class of co-referential entity ids under
  the agent's KNOWN identities. A singleton class is implicit
  (not returned).
- **`known()`, `believed()`, `suspected()`, `gaps()` on
  `KnowledgeState`.** Unchanged in signature. They return the
  literal Held records — introspection over the literal set, not
  a substitution view. Callers that want "everything Jocasta
  believes under substitution" compose `known()` output with the
  substitution operation at the call site, or use
  `holds_all_matches(p)` per-proposition.
- **`world_holds(p, world_props)` — new module-level function.**
  Substitution-aware query over world state. `world_props` is the
  set returned by `project_world`; the function extracts world
  identity propositions from that set and computes the
  equivalence classes under which `p` matches. Returns a bool
  (world state is a set of Props, not Held records; there is no
  "strongest match" to pick). A `world_holds_literal(p,
  world_props)` companion is just `p in world_props`.

### Substrate internal changes

- `dramatic_ironies` composes with substitution: a reader-over-
  character irony fires for `P` if the reader holds `P`
  (substitution-aware, KNOWN identities only per I7) and the
  character does not. The character's substitution is over
  *their* identities, not the reader's.
- `sternberg_curiosity` stays literal per the Sternberg-stays-
  literal decision above. It returns the GAP slot contents of
  the held set, unchanged.
- `project_knowledge`, `project_world`, `project_reader`: fold
  signatures and behavior unchanged. They produce the literal
  held set or world set; substitution is a consumer-side
  computation via the `holds*` / `world_holds` query surface.

### What stays out of the API

- No direct substitution function callable by tooling outside the
  substrate. Substitution is internal to query methods. If a
  future caller needs to reason about identity classes
  independently of query, they use `equivalence_classes()` (for
  an agent) or compute the world's equivalence classes from the
  world set; the substrate does not expose substitution as a
  general-purpose rewriter.

## Worked example — Jocasta's anagnorisis

The current Oedipus prototype fakes Jocasta's realization. Under
this sketch, the encoding splits into two parts: the literal
per-agent relational facts, and a realization event that asserts
identity.

### Before realization

Jocasta's held set (literal):

- `married(jocasta, oedipus)` — KNOWN (from the wedding event)
- `had_child_with(jocasta, laius)` — KNOWN (from the conception
  backstory)
- `child_of(the-exposed-baby, jocasta)` — KNOWN (she knows she
  bore a child; the child's id is `the-exposed-baby`)
- `exposed(jocasta, the-exposed-baby)` — KNOWN (the exposure was
  her act)
- `killed_stranger_at_crossroads(oedipus)` — KNOWN (Oedipus told
  her; she heard him)
- `dead(laius)` — KNOWN
- `killed_at(laius, the-crossroads)` — KNOWN (she knows where
  Laius was killed; from the messenger)

Jocasta does NOT hold (at this τ_s):

- `identity(oedipus, the-exposed-baby)` — the key realization
- `child_of(oedipus, jocasta)` — deriving this requires identity
- `married(jocasta, own-child)` — same
- `killed(oedipus, laius)` — requires
  `identity(oedipus, the-stranger)` *and* knowledge that Laius
  was the stranger

All the literal facts are there. What is missing is the identity.

### The realization event

At τ_s=Jocasta-realizes, an event:

```
Event(
    id="E_jocasta_realizes_oedipus_is_her_child",
    type="realization",
    τ_s=…, τ_a=…,
    participants={"realizer": "jocasta",
                  "a": "oedipus", "b": "the-exposed-baby"},
    effects=(
        KnowledgeEffect(
            agent_id="jocasta",
            held=Held(
                prop=Prop("identity",
                          ("oedipus", "the-exposed-baby")),
                slot=Slot.KNOWN,
                confidence=Confidence.CERTAIN,
                via=Diegetic.REALIZATION.value,
                provenance=("the shepherd's testimony + "
                            "the messenger's detail about "
                            "the foot",),
            ),
        ),
    ),
)
```

A second realization event handles the stranger identity:

```
Event(
    id="E_jocasta_realizes_oedipus_is_the_stranger",
    type="realization",
    τ_s=…+1, τ_a=…,
    participants={"realizer": "jocasta",
                  "a": "oedipus", "b": "the-stranger"},
    effects=(
        KnowledgeEffect(
            agent_id="jocasta",
            held=Held(
                prop=Prop("identity",
                          ("oedipus", "the-stranger")),
                slot=Slot.KNOWN,
                confidence=Confidence.CERTAIN,
                via=Diegetic.REALIZATION.value,
            ),
        ),
    ),
)
```

(Whether these are one event or two is an encoding choice. Two
events model the two beats of Jocasta's realization discretely;
one event models it as a single collapse. Either works.)

### After realization

Jocasta's held set, literal:

- All the prior propositions (unchanged).
- `identity(oedipus, the-exposed-baby)` — KNOWN.
- `identity(oedipus, the-stranger)` — KNOWN.

### Queries after realization

**"Does Jocasta know that Oedipus is her child?"**
Query `child_of(oedipus, jocasta)`. Literal: not in the held set.
Substitution: `{oedipus, the-exposed-baby}` is an equivalence
class; `child_of(the-exposed-baby, jocasta)` is in the set;
substitution yields match. *Answer: yes.*

**"Does Jocasta know that Oedipus killed Laius?"**
Query `killed(oedipus, laius)`. Literal: not in set. Substitution:
`{oedipus, the-stranger}` is an equivalence class;
`killed_stranger_at_crossroads(oedipus)` is in the set — hmm. This
requires the encoding to have already connected "the stranger at
the crossroads" to Laius's killing via a relational fact.
Specifically, Jocasta needs `killed(the-stranger, laius)` in her
held set, not `killed_stranger_at_crossroads(oedipus)`.

This is an encoding call. The current prototype uses the
composite predicate as a workaround for existential gaps
(substrate-05 OQ 1). Under this sketch's encoding, the cleaner
authoring is:

- `killed(the-stranger, laius)` — KNOWN (Jocasta has been told
  Laius was killed by a stranger at the crossroads; "the
  stranger" is an entity id for the anonymous killer).
- `killed_stranger_at_crossroads(oedipus)` is either dropped in
  favor of `killed(oedipus, the-stranger-at-crossroads)` (which
  needs Jocasta to hear Oedipus tell her that) or is kept as a
  second-string encoding of the same fact.

The refactor is: name the stranger entity explicitly as
`the-stranger-at-crossroads`; author `killed(the-stranger-at-
crossroads, laius)` into Jocasta's state when she is told; author
`killed_at_crossroads(oedipus)` into Jocasta's state when Oedipus
tells her *he* killed someone there. The second realization
asserts `identity(oedipus, the-stranger-at-crossroads)`.

Substitution then cleanly yields `killed(oedipus, laius)` via two
chain links: `{oedipus, the-stranger-at-crossroads}` is one class;
`killed(the-stranger-at-crossroads, laius)` substitutes to
`killed(oedipus, laius)`. *Answer: yes.*

This is the ergonomic shape: more explicit entity-naming up front,
fewer composite predicates, cleaner substitution chains.

### Dramatic irony before and after

**Before realization:**

Reader holds (from earlier disclosures):
- `identity(oedipus, the-exposed-baby)` — KNOWN.
- `identity(oedipus, the-stranger-at-crossroads)` — KNOWN.
- All the relational facts Jocasta holds, *plus* the identities.

Reader's substitution-aware view: the reader holds
`child_of(oedipus, jocasta)`, `killed(oedipus, laius)`, and
`married(jocasta, own-child)` — all via substitution.

Jocasta's substitution-aware view: she lacks the identities, so
substitution does nothing for her. Her view is the literal set.

`dramatic_ironies` with these two states: reader-over-Jocasta
irony on each of the derived propositions. The demo's
τ_d=0-reader-outruns-Oedipus pattern now holds not because of
hand-authored irony records, but because substitution on the
reader side produces beliefs the characters' literal-only states
do not.

**After realization:**

Jocasta's state gains the two identities. Her substitution-aware
view now matches the reader's on the previously-ironic
propositions. The ironies collapse. *This is the anagnorisis,
derived cleanly.*

## Relation to the general inference model (substrate-05 OQ 2)

OQ 2 as stated in substrate-05:

> Realization-as-integration (Jocasta realizing the man-she-married
> is the son-she-bore) needs either an inference layer or a
> composite-proposition mechanism. Currently realizations are
> authored events.

This sketch closes OQ 2 for the realization case, via the
identity-as-proposition-plus-substitution approach. What remains
open under OQ 2:

- Domain rules (`exposed(X, C) ⇒ child_of(C, X)` and similar).
- Forward chaining (multi-step derivation).
- Proof-carrying inference (why does a conclusion hold?).
- Negation and contradiction management.
- Compound-term identity.

A successor sketch (`inference-model-sketch-01`) takes these up.
Until then, encodings that want domain derivation author the
consequent facts explicitly, with an encoding-library helper
function if the pattern recurs (e.g., `mark_parent_child(parent,
child)` authors both `child_of(child, parent)` and any other
facts the author wants about parenthood).

## Open questions

1. **Canonicalization of `identity(A, B)` vs `identity(B, A)`.**
   The substrate's `Prop` equality distinguishes them; substitution
   treats them equivalently. A linting convention (sorted args) is
   a tooling choice; whether the substrate should enforce it is
   open. Probably not — the Prop record should stay dumb.
2. **Performance at scale.** Equivalence-class computation per
   query is naive. If story scale grows, memoization keyed by
   `(agent_id, τ_s)` is natural. Not urgent at prototype scale.
3. **Identity across agents' held sets.** If Alice and Bob both
   hold different identities, queries that "join" their states
   (are there any?) would need a design. Currently the substrate
   does not offer such queries; per-agent answers are the norm.
4. **Realization cascades.** If Alice realizes `identity(A, B)`,
   and separately realizes `identity(B, C)`, the two realizations
   are distinct events. The equivalence class grows to
   `{A, B, C}`. No issue. But: should a second realization *at
   the moment it happens* be a distinct dramatic beat, or is the
   substitution "always there" once both identities are in the
   set? Both readings are legitimate; tooling surfaces the
   cascade differently depending on what the author wants.
5. **World-vs-agent identity drift.** If the world holds
   `identity(A, B)` but an agent holds `identity(A, C)` (and the
   world does not assert `identity(A, C)`), the agent is wrong in
   the world's frame but self-consistent. The substrate represents
   both; tooling may want to flag the drift but the substrate is
   silent.
6. **Entities under negation.** If the substrate later adds
   negation (`¬P`), `¬identity(A, B)` is interesting: "Alice knows
   they are NOT the same." Substitution must not fire for agents
   holding the negation; the fold semantics of negated identity
   need a sketch of their own.
7. **Reader-model proposing identities.** An LLM reading prose
   spots "these two characters are obviously the same person."
   The reader-model proposes `identity(A, B)` via the proposal
   queue (reader-model-01 R3). Author accepts → authored event.
   No substrate change; the existing proposal machinery covers it.
8. **Literal-set-preservation in contested branches.** Identity on
   one contested branch changes what queries on that branch
   answer. Queries on a sibling branch are unaffected. This falls
   out of B1; no special handling.
9. **Implementation order of the probe.** The probe should land
   `holds_literal()` first (pins the invariant before
   substitution exists), then substitution, then verify
   `holds_literal` still passes alongside substitution-aware
   `holds()`. That order keeps the regression surface obvious.
10. **Sternberg re-consideration.** This sketch commits to
    sternberg_curiosity staying literal. If later encoding
    experience shows that "gap acknowledged by authoring, answer
    implicit by substitution" is a confusing pattern for readers
    or tools, a future sketch may introduce a substitution-aware
    curiosity query that reports gaps whose answers remain
    underivable via identity. Not urgent; flagged for revisit.

## Discipline

Process expectations for work against this sketch:

- **Identity is always authored.** No inference of
  `identity(A, B)` from other facts ever enters the substrate.
  Libraries that suggest identities propose them; acceptance is
  an authored realization (or world effect).
- **Realization events assert, do not rewrite.** A realization's
  effect is an identity `KnowledgeEffect`. Removing old
  propositions (the previous prototype's workaround) is retired;
  the substitution rule handles the rewrite at query time.
- **Encodings name entities explicitly.** Composite predicates
  (`killed_stranger_at_crossroads`) are workarounds for missing
  entity-naming granularity. Where identity substitution would
  benefit from an explicit entity id (`the-stranger-at-
  crossroads`), the encoding names it.
- **Queries document substitution expectation.** Tests that use
  `holds(p)` pin a substitution-aware answer; tests that use
  `holds_literal(p)` pin the literal set. The distinction is
  visible at call sites, not buried.
- **The sketch is a slice.** Identity is one bounded slice of
  OQ 2. A later inference-model sketch will widen; this sketch
  does not try to cover domain rules or general chaining.

## Summary of the commitments

| | Substrate | Identity + substitution |
|---|---|---|
| Identity as proposition | N/A (OQ 2 open) | I1 — first-class Prop |
| Scope | per fold, existing rules | I2 — per fold, same rules |
| Inference timing | state mutation via effects | I3 — query-time only |
| Symmetry/transitivity | N/A | I4 — both, at query time |
| Realization | rewrites held set | I5 — asserts identity only |
| Source of identity | N/A | I6 — authored, never synthesized |
| Slot required for substitution | N/A | I7 — KNOWN only |
| Multi-match resolution | N/A | strongest slot, earliest τ_a tiebreak |
| Agent query API | `holds`, `holds_as`, … | substitution-aware; `holds_literal`, `holds_all_matches`, `equivalence_classes` added |
| World query API | `p in project_world(...)` | `world_holds(p, world_props)` substitution-aware; literal query unchanged |
| Irony queries | compare literal states | substitution-aware per I7 |
| Curiosity queries | literal GAP slot | still literal — GAP is an authorial marker |
| Domain derivation | out of scope (author's job) | still out of scope — deferred to inference-model-sketch |
