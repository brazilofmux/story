# Inference model — sketch 01

**Status:** draft, active
**Date:** 2026-04-14
**Supersedes:** nothing (new topic)
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [substrate-sketch-05.md](substrate-sketch-05.md), [identity-and-realization-sketch-01.md](identity-and-realization-sketch-01.md)
**Superseded by:** nothing yet

## Purpose

Close the remainder of substrate-sketch-05 open question 2 after
identity-and-realization-sketch-01 carved out the realization slice.
The question that sketch left open: can the substrate *derive*
domain facts from other domain facts via authored rules, rather
than requiring every derivable fact to be authored as an explicit
observation?

The forcing function is the Oedipus encoding extended with
`parricide(oedipus, laius)` and `incest(oedipus, jocasta)` as
authored world facts. Both are conclusions of obvious domain rules
(`killed(X,Y) ∧ child_of(X,Y) ⇒ parricide(X,Y)`;
`married(X,Y) ∧ child_of(X,Y) ⇒ incest(X,Y)`) that the substrate
currently cannot express. Authoring them explicitly makes the pinch
visible: every agent who reaches the premises via identity
substitution (Jocasta at τ_s=9, Oedipus at τ_s=13) also needs an
explicit `observe(...)` for the compound conclusion, because there
is no derivation surface. The author-asserted workaround retires in
this sketch in favor of authored rules.

A reader-model probe against the extended encoding, invited to
answer the open question `D_parricide_incest_authored_not_derived`,
proposed a boundary criterion:

> Derive a compound predicate when (a) its rule can be stated in
> terms the substrate already tracks as world-props, and (b) the
> compound's truth-value is fully determined by those props with
> no authorial judgment required. Predicates that require
> contextual or tonal judgment — 'hubris', 'tragic irony' —
> cannot be captured by such rules and remain description-layer
> concerns.

That criterion is the seed of the sketch's scope commitment (N9
below). The sketch widens what identity-and-realization deliberately
narrowed: identity substitution handles one specific shape of
inference (equivalence under realization); this sketch handles the
broader shape of conjunctive Horn-clause rules over typed
propositions, composed *with* identity substitution rather than
replacing it.

This sketch specifies:

- The rule record's shape and semantics.
- Where rules live (per-story vocabulary, like predicates).
- Derivation as a query-time operation composed with identity
  substitution.
- Per-fold scoping and slot propagation.
- Bounded fixpoint with a depth cap.
- Proof carrying on derived results.
- The derivable/non-derivable boundary (the probe's criterion,
  with caveats).
- What is explicitly *not* in scope (negation, disjunction,
  existentials, rule synthesis, rule attention).
- A worked example using the Oedipus encoding.

## What this sketch is *not* committing to

- Negation. No `¬P` in rule bodies, and no negation-as-failure.
  NAF in particular has subtle interaction with per-fold GAP slots
  (does absence of P from an agent's held set satisfy ¬P, or only
  an explicitly held GAP?). A coherent NAF semantics for this
  substrate is a sketch-02 problem.
- Disjunction in rule bodies. Authors needing `A ∨ B ⇒ C` write
  two rules: `A ⇒ C` and `B ⇒ C`. This is a Datalog-level
  restriction, intentional.
- Existential quantifiers in rule heads. A rule head may not
  introduce entities that do not appear in the body. Rules are
  bottom-up over known entities; they do not generate new
  individuals.
- Function symbols. Rule args are entity references or rule
  variables — never nested terms. `parricide(X, Y)` is admissible;
  `parricide(X, father_of(X))` is not. This is the Datalog
  restriction, and it is what keeps the fixpoint finite.
- Rule synthesis. The substrate does not propose rules from
  patterns in the held set. A reader-model *may* propose a rule
  for author review via the existing proposal queue (future
  sketch — reader-model-01 R3 covers the general partner-not-
  fallback shape); acceptance is an authorial act, never a
  substrate act.
- Rule-level attention. Rules are structural artifacts; they are
  not descriptions and do not carry STRUCTURAL / INTERPRETIVE /
  FLAVOR attention tags. If a rule itself is uncertain, that
  uncertainty lives in an `authorial-uncertainty` description
  attached to the rule, not in the rule record.
- Stratified or recursive rule sets beyond the depth bound (N7).
  Rules may be recursive within the depth bound; the depth bound
  is what makes inference decidable and fast.
- Interpretive heads. Rules may not derive predicates whose truth
  depends on authorial judgment (N9). If the author wants to say
  "this character's actions constitute hubris", that is a
  description anchored to the event(s), not a rule-derived fact.

If a question starts "how do I derive an open-textured moral or
dramatic category?" or "can the substrate notice X and infer Y?" —
it is out of scope unless Y is definitional in the N9 sense.

## What this sketch *is* committing to

1. **N1 — Rules are Horn clauses with conjunctive bodies and
   single-literal heads.** A rule is a record
   `Rule(head, body, id)` where `head` is a Prop template (a
   `Prop` whose args may contain variables) and `body` is a
   non-empty tuple of Prop templates. The rule reads
   `∀ bindings. body₁ ∧ body₂ ∧ … ⇒ head`. All variables in
   `head` must appear in `body` (range-restricted). No
   disjunction, no negation, no existentials.
2. **N2 — Rules are authored per-story, like predicates.** The
   substrate supplies the rule-application engine; the encoding
   supplies the rules. Rule vocabulary is not substrate-built-in
   and not shared across encodings unless the encoding imports a
   library. This parallels the predicate rule (the substrate knows
   `identity` and `confidence`; every other predicate is
   per-story).
3. **N3 — Derivation is query-time.** Held sets and world state
   remain literal — they contain exactly the propositions authored
   through effects. Derivation happens when the substrate is
   queried ("does Jocasta hold `parricide(oedipus, laius)`?") and
   produces a view over the literal set plus the rule set plus (per
   I4) identity equivalence classes. No state mutation at commit;
   no derived-fact storage; no truth-maintenance system.
4. **N4 — Derivation composes with identity substitution.** A rule
   matches under the identity-expanded view of the fold. If an
   agent holds `killed(oedipus, the-crossroads-victim)` and
   `identity(laius, the-crossroads-victim)` at KNOWN and
   `child_of(oedipus, laius)`, the rule
   `killed(X,Y) ∧ child_of(X,Y) ⇒ parricide(X,Y)` derives
   `parricide(oedipus, laius)` by matching the first premise via
   substitution and the second literally. Identity substitution and
   rule application are one query-time operation, not two
   sequential passes.
5. **N5 — Derivation is per-fold.** Agent-level derivation uses
   only that agent's held set (after substitution). World-level
   derivation uses only world state. Reader-level derivation uses
   only the reader's held set. A rule that fires on the world does
   not thereby lodge a derived fact in an agent's state; each fold
   derives independently. This parallels I2 (identity scopes per
   fold) and E1 (the core fold rule).
6. **N6 — Weakest-premise slot propagation.** A derived fact's
   effective slot is the weakest slot among the premises that
   matched it, under the order
   `KNOWN > BELIEVED > SUSPECTED > GAP`. If all premises are
   KNOWN, the derivation is KNOWN. If any premise is BELIEVED, the
   derivation is BELIEVED. GAP premises do not participate — a
   held GAP is an acknowledged absence, not a premise; a rule body
   containing a GAP match fails. Confidence propagates the same
   way: weakest premise wins.
7. **N7 — Bounded fixpoint with depth cap.** Derivation iterates:
   derived facts from pass *k* are admissible premises in pass
   *k+1*. The iteration stops at a fixpoint or a depth cap,
   whichever comes first. Default cap is 3. Rule sets that require
   deeper chains document the deeper cap in the encoding; the
   substrate refuses unbounded recursion even under N1's range-
   restriction, because a pathological rule set over a rich held
   set can still be expensive.
8. **N8 — Derived facts carry their proof.** A query that returns
   a derived fact also returns the rule id that produced it and
   the premise bindings. If identity substitution contributed to a
   premise match, the substitution binding is part of the proof.
   Proofs are query-result metadata, not persisted records. A
   caller that does not want proof detail ignores it; a caller
   that wants to render "Oedipus now knows he killed his father
   because he killed Laius and Laius is his father" reads the
   proof and composes the explanation.
9. **N9 — The derivable boundary is definitional-over-world-props,
   not interpretive.** A rule head is admissible if and only if:
   (a) every body literal's predicate is a typed proposition
   already tracked in the fold the rule queries against — i.e.,
   the predicate appears in the encoding's predicate vocabulary
   and is the kind of thing that lands in held sets via effects,
   not a description-layer concept; and (b) the head's truth is
   fully determined by the body, with no authorial judgment
   required. Compound predicates like `parricide` or `incest`
   pass (b) trivially — they have sharp definitions. Open-
   textured predicates like `hubris(X)` or `tragic(Event)` fail
   (b); they remain description territory, not rule heads. N9 is
   the probe-derived criterion; it is a draft commitment that a
   richer encoding will probably pressure (see OQ3, OQ4).
10. **N10 — Authored facts win.** If an authored effect and a
    derivation would both place `P` in the same fold, the
    authored record is authoritative. Its slot, confidence,
    provenance, and via are preserved; derivation does not
    overwrite. If an author has explicitly asserted `P` at
    BELIEVED and a rule derives `P` at KNOWN, the queried slot
    is BELIEVED (the weaker authored state wins against the
    stronger derivation). Derivation is additive; it fills gaps,
    it does not rewrite. This is the inference-model analogue of
    I6 (substrate does not fabricate identities) and I3
    (substitution is a view, not a mutation).

N1 through N10 pass architecture-sketch-01 A3: each describes drift
the schema catches rather than content an attentive reviewer could
self-police from prose. Without N1, there is no way to distinguish
a rule from an observation, and authors manually replicate
derivable facts across folds (the Oedipus parricide/incest problem
today). Without N3, commit-time state balloons. Without N9, the
rule surface devours description territory.

## Relation to prior sketches

- **Architecture-01 A3.** N1–N10 pass A3; none depend on tonal
  judgment. The derivable boundary (N9) is precisely the A3 cut
  applied to rule heads — structural predicates inside, interpretive
  predicates outside.
- **Architecture-01 A5.** The reader-model probe seeded N9 directly;
  the partner-not-fallback pattern produced a design-bearing
  commitment rather than a fallback suggestion. A future rule-
  proposal flow will extend A5 into rule-vocabulary territory.
- **Substrate-05 E1, K1, K2.** Rule derivation respects all fold
  rules. Rules do not create new effect kinds; they read the fold's
  literal held set and world state, expand under identity per I4,
  and iterate to fixpoint. What changes is query semantics, not
  fold semantics.
- **Substrate-05 M1 (adverbial/modal routing).** Rule heads that
  pass N9 are structural — they sit in the typed-proposition
  surface, which is exactly where M1 places predicates with
  downstream structural consequence. Rules do not live in
  description territory.
- **Substrate-05 OQ2.** This sketch closes the remaining slice of
  OQ2. Together with identity-and-realization-sketch-01, OQ2 is
  now covered for the bounded Horn + identity shape. Richer
  inference (NAF, existentials, rule-level attention) becomes a
  sketch-02 problem if a forcing function demands it.
- **Identity-and-realization-01.** This sketch and identity compose
  per N4. Identity substitution continues to do exactly what I1–I7
  specify; rules read the substituted view. Neither machinery
  dominates the other; they are orthogonal and cooperate at query
  time.
- **Descriptions-01.** A rule is structural; it is not a
  description and does not carry attention. But a rule *may* be
  the subject of a description — the rule record has an id (N1),
  and an `authorial-uncertainty` description can anchor to that id
  via a new `AnchorRef.kind == "rule"` (see OQ2). Descriptions
  attach to rules the way they attach to events or descriptions.
- **Reader-model-01.** A reader-model may (eventually) propose
  rules; acceptance produces authored rule records. The firewall
  holds: no substrate-level rule synthesis. This sketch does not
  formalize the proposal flow for rules — that is deferred to a
  reader-model extension — but the shape is the existing proposal
  queue, specialized.
- **Focalization-01.** Focalization constrains disclosure slots
  under min(author, focalizer). Derivation under N6 uses the same
  min-of-premises-slot rule within a fold. The two don't interact
  directly — focalization shapes what enters the reader's state;
  derivation reads whatever state it finds — but they share a
  family resemblance as min-of-inputs slot rules.

## The rule record

### Shape

```python
@dataclass(frozen=True)
class Rule:
    id: str
    head: Prop       # may contain variables
    body: tuple      # tuple[Prop, ...], non-empty, may contain variables
    metadata: dict   # provenance, commentary; not substrate-semantic
```

- `id` is a stable string. Descriptions can anchor to it; proofs
  carry it; logs reference it. Rule ids are per-story, like event
  ids.
- `head` and `body` entries use the existing `Prop` type. Args
  are either entity ids (strings naming an `Entity`) or variable
  strings (by convention, uppercase letters: `"X"`, `"Y"`; see
  below).
- `body` is non-empty. A zero-body rule (a pure assertion) is
  just an authored fact — write it as an effect, not as a rule.
- Variables in `head` must appear in `body` (range-restriction
  per N1).

### Variable convention

A Prop arg is a variable iff it is a non-empty string whose first
character is uppercase (ASCII `[A-Z]`). Entity ids in the encoding
are lowercase (`"oedipus"`, `"laius"`, `"the-exposed-baby"`);
variables are uppercase (`"X"`, `"Y"`, `"Killer"`). The
convention is enforced by the rule-registration API, not by the
`Prop` type itself — `Prop` remains the same record as before.

This is the same dodge Datalog uses. It is slightly gross
(string-level variable syntax) but avoids introducing a `Var`
wrapper that would ripple into every `Prop` consumer.

### What is NOT in the record

- Attention. Rules are structural (per N9); they do not carry
  INTERPRETIVE / FLAVOR tags.
- Per-fold scope. A rule is a pure form over propositions; it
  fires in whichever fold the query targets (N5). The *decision*
  to query world vs. agent vs. reader lives at the query site.
- Branches. Branch scope is fold-relative (substrate-05 B1); a
  rule does not commit to a branch. The fold the rule queries
  against is already branch-scoped.
- τ_a. Rules do not have their own authored-time stamp in
  sketch 01. (A future sketch may revisit; see OQ6.) A rule
  exists for the duration of the encoding's runtime.
- `via`. Provenance of a *derived fact* names the rule id and
  the premise bindings (N8), not a diegetic `via`.

## Derivation semantics

### The core procedure

A query `holds_derived(fold, Q)` — where `fold` is an agent's
held set, the world state, or a reader-state projection, and `Q`
is a ground `Prop` — answers by:

1. Materialize the *starting set*: every literal held proposition
   in `fold`, expanded under identity per I4 to include all
   propositions reachable by substitution from each equivalence
   class. Associate each member with its source slot (literal Held
   slot; identity-substituted facts inherit the source Held's
   slot).
2. For each rule in the rule set: find all variable bindings
   under which every body literal matches a member of the current
   set. For each satisfying binding, compute the derived head
   and its slot per N6 (weakest input slot). Add the derived
   result to the next iteration's set.
3. Merge the next iteration's set with the current set,
   preserving the strongest existing slot for any proposition
   already present. If the set grew, iterate; if it did not, we
   have reached fixpoint. Stop at fixpoint or at the depth cap
   (N7), whichever comes first.
4. Answer: `Q` holds iff `Q` appears in the final set at some
   non-GAP slot. The slot returned is the strongest at which
   `Q` appears (authored > derived, per N10). Proof is the
   shortest derivation: the rule id and binding that first
   introduced `Q`, plus identity substitutions that contributed.

Cost is `O(|rules| · |set|^|body|)` per iteration, bounded by the
depth cap. For the rule sets this sketch targets (small, per-story,
hand-authored), this is fast.

### Authored facts and the starting set

Authored facts are the starting set's floor. They are present at
iteration 0 with their authored slots. Rule derivation can add new
propositions and new slot annotations, but per N10 it cannot
override an authored fact's slot. Concretely: when the iteration
merge encounters `(P, derived_slot)` and `P` is already in the
set with an authored slot, the authored slot wins regardless of
which is stronger. Derivation-vs-derivation merges use the
strongest slot (both are equally derived; the stronger proof
stands).

### Identity substitution and the starting set

Step 1 of the procedure pre-expands the held set under identity.
This is semantically equivalent to (but implementation-distinct
from) matching each body literal against the post-substitution
view at rule-application time. Pre-expansion is simpler; it also
makes the proof simpler — the substitution that contributed to a
premise match is a fixed fact of the starting set, not a
rule-time side computation.

Slot propagation through identity: if an agent holds
`identity(A, B)` at KNOWN and `killed(X, A)` at BELIEVED, the
substituted fact `killed(X, B)` is at BELIEVED (the source Held's
slot). If the identity is KNOWN and the source is GAP, the
substituted is GAP (and does not participate in rule bodies per
N6). This is consistent with I7: substitution fires only on
KNOWN identities, but the *derived* fact's slot is the *source
fact's* slot, not the identity's slot.

### Per-fold derivation

A rule fires in whichever fold the query targets. A query against
Jocasta's state fires the rule over Jocasta's identity-expanded
held set. A query against the world fires the rule over world
state (ignoring any agent's identity, since the world has none
unless one was asserted as a WorldEffect). A query against the
reader-state projection fires it over the reader's view.

Cross-fold rule firing never happens. A rule that derives
`parricide` from the world state does not thereby give Jocasta
`parricide` — she has to independently satisfy the body in her
own held set. This is the I2 rule generalized from identity to
rules.

### Weakest-premise slot, the details

Under the ordering `KNOWN > BELIEVED > SUSPECTED > GAP`:

- A rule body with all premises at KNOWN → derived at KNOWN.
- A rule body with at least one BELIEVED → derived at BELIEVED.
- A rule body with at least one SUSPECTED → derived at SUSPECTED.
- A rule body with any GAP premise → the body does not match;
  no derivation.

Rationale: a GAP is an acknowledged absence; it is not half-true
or tentative. If the author has explicitly said "the agent does
not know Y", then a rule conclusion requiring Y in the agent's
head simply does not fire — the agent does not know it.

Multiple premises at different slots: the weakest non-GAP wins.
This matches the epistemic reading: "he believed X, was certain
of Y; therefore he believed (at best) X ∧ Y ⇒ Z."

Confidence propagates the same way. If the encoding uses
confidence more finely than the slot ordering, the
weakest-confidence-wins rule applies there too.

### Fixpoint semantics, briefly

Sketch 01's fixpoint is ground-fact-level: we stop when the set
of `(Prop, slot)` pairs stops growing. We do *not* track proofs
as part of the fixpoint test — two different proofs of the same
`(P, slot)` collapse to one. A future sketch may distinguish
proofs (relevant for counterfactual analysis), but sketch 01
does not.

Slot upgrades at fixpoint: if rule application on iteration *k*
produces `(P, BELIEVED)` and on iteration *k+1* produces
`(P, KNOWN)` via a stronger body, the set records the strongest
slot (`KNOWN`) and iteration continues. This is a real fixpoint
condition: slot-strength can strictly increase, so fixpoint
requires both "no new propositions" and "no slot upgrades."

### Depth cap (N7)

Default 3. This is enough to cover the compositions we expect:
- Depth 1: `killed ∧ child_of ⇒ parricide`.
- Depth 2: `sibling(X,Y) ∧ child_of(Y,Z) ⇒ niece_or_nephew(X,Z)`
  composed with `parent(Z) ∧ birth_order(A,Z,B) ⇒ sibling(A,B)`.
- Depth 3: reserved room for recursive chains.

A depth cap is *not* a correctness guarantee; it is a performance
fence. Rule sets that terminate cleanly within N1's
range-restriction will hit fixpoint well before the cap. The cap
exists to bound worst-case runtime when the author has written a
rule set that does not terminate cleanly (typically because of a
cycle under a rich held set).

Setting the cap higher is per-encoding: the rule-registration API
takes an optional `depth_cap` parameter. Going above 10 without a
reason is a smell.

## The derivable boundary (N9) in practice

The probe's criterion:

> Derive iff (a) stateable in world-props, (b) truth-value fully
> determined, no authorial judgment required.

Clear cases:

- `parricide(X, Y) ⇐ killed(X, Y) ∧ child_of(X, Y)` — passes.
- `incest(X, Y) ⇐ married(X, Y) ∧ child_of(X, Y)` — passes.
- `sibling(X, Y) ⇐ child_of(X, P) ∧ child_of(Y, P) ∧ ¬equal(X, Y)` — passes
  *once* sketch 02 admits a way to express the non-reflexive
  condition. Today, it would need to be written as two rules
  per parent, or the author accepts that a child is its own
  sibling (which is wrong, but not catastrophic until it is).
- `uncle(X, Y) ⇐ sibling(X, P) ∧ child_of(Y, P)` — passes,
  compositional with the `sibling` rule.

Unclear cases the sketch is honest about:

- `widow(X) ⇐ married(X, Y) ∧ dead(Y) ∧ female(X)` — gender
  predicates are structural in most encodings, so this passes N9
  literally. But the predicate "widow" carries cultural
  connotation (status, role) that some encodings may want to
  reserve as description-level. Pass or fail by N9 depends on
  whether `female` is in the encoding's typed vocabulary at all.
  Sketch 01 does not legislate.
- `orphan(X) ⇐ child_of(X, M) ∧ child_of(X, F) ∧ dead(M) ∧ dead(F) ∧ ¬equal(M, F)`
  — similar shape. Also needs sketch-02 NAF or rule duplication.
- `betrayed(X, Y) ⇐ promised(X, Y, P) ∧ did_not_keep(X, P)` —
  arguably definitional if `promised` and `did_not_keep` are
  typed predicates, but "betrayed" carries moral weight. N9 says
  yes *if the encoding has typed `did_not_keep`*; the encoding
  may instead prefer to treat betrayal descriptively. Sketch 01
  does not legislate.

The pattern: N9 is a necessary condition, not a sufficient one.
A predicate whose rule passes N9 *may* be derived; whether it
*should* be is an encoding-level decision the sketch leaves to
authors. The sketch's commitment is the necessary condition: if
the predicate cannot be stated as a conjunction of typed facts,
it must not be a rule head. This rules out `hubris`, `tragic`,
`ironic`, `earned`, `deserves`, `mourns`, etc.

## Interaction with branches

Branches are fold parameters, not rule parameters. A query
`holds_derived(fold(agent, branch=:b-woodcutter), Q)` fires the
rule set against the already-branch-scoped fold. The rule doesn't
know the branch; it sees a set of premises and derives
consequences. This is the B1 parameterization rule playing out
for rules.

Cross-branch rule firing does not occur. Rules do not read across
branches. If an agent's state on `:b-woodcutter` derives `P`,
that `P` is a fact about the `:b-woodcutter` fold; nothing is
added to `:canonical` or other branches.

## Interaction with the reader

The reader-outruns-character phenomenon composes neatly with
rules: the reader's held set, at τ_d=0 in the Oedipus encoding,
contains `killed(oedipus, laius)`, `child_of(oedipus, laius)`,
`married(oedipus, jocasta)`, and `child_of(oedipus, jocasta)` via
the preplay disclosures. With the two rules in this sketch, the
reader derives `parricide(oedipus, laius)` and
`incest(oedipus, jocasta)` from τ_d=0 — not because the author
disclosed them, but because the author disclosed the premises. The
reader has the conclusion before any character does.

This is significant. The probe's declined edit on
`D_anagnorisis_logical_payload` tried to narrow the "reader has
held both since τ_d=0" claim to τ_a authorship coordinates.
Under this sketch, the original claim is vindicated: the reader's
derivation surface is active from τ_d=0, and the conclusions are
reachable from the disclosed premises. The authored
`parricide`/`incest` disclosures in `PREPLAY_DISCLOSURES` become
redundant once the rules exist — the reader derives them from the
already-disclosed premises.

(That does not close `D_view_cannot_see_τ_d`, the other banked
question. Whether the *description* `D_anagnorisis_logical_payload`
can refer to τ_d coordinates the view doesn't expose is still
open; this sketch just says the *inference* works.)

## Query surface

This sketch adds:

- `holds_derived(fold, prop) -> Optional[(slot, proof)]` — the
  derivation-aware analogue of `holds_literal`. Returns `None` if
  no derivation succeeds. Composes with identity per I4.
- `derive_all(fold, rule_set, depth_cap=3) -> dict[Prop, (slot, proof)]`
  — the bulk form. Returns every derivable ground fact at its
  strongest slot, with proof. Used by projections that want to
  render a full "what does this agent effectively know" view.
- `derived_equivalence_classes(fold, rule_set)` — like the
  identity surface's equivalence_classes, but returning per-
  equivalence-class derived facts. (Optional; a tooling
  convenience, not substrate-essential.)

Existing queries (`holds_literal`, `holds`, `holds_all_matches`,
`equivalence_classes`, `world_holds`) retain their current
semantics. `holds` under this sketch is extended to consult rules
where previously it consulted only identity substitution:

- Old `holds(fold, P)` = literal match, then identity-substituted
  match.
- New `holds(fold, P)` = literal match, then
  identity-substituted match, then rule-derived match.

The composition order preserves the existing authored-wins
property (N10): a literal authored fact shortcut the deeper
checks.

## Rule registration

Rules live in the encoding. The encoding module exports a
`RULES: tuple[Rule, ...]` constant the way it exports `FABULA`,
`DESCRIPTIONS`, etc. A query site passes the rule set explicitly:

```python
holds_derived(fold, prop, rules=RULES)
```

Not via module-level global, not via registry-at-import. This
parallels the events-pass-in pattern the existing query surface
uses; the substrate stays free of per-story global state.

A future encoding library (sketch TBD) may bundle a
`common_kinship.RULES` or `common_tragedy.RULES` that stories
compose into their own rule sets. That is a library-layer concern,
not a substrate-layer one.

## Proof shape

A proof returned with a derived fact has the shape:

```python
@dataclass(frozen=True)
class Proof:
    rule_id: str
    bindings: dict[str, str]   # variable → entity id
    premise_proofs: tuple      # tuple[PremiseSource, ...]
    depth: int                 # at which iteration this derivation landed

PremiseSource = Union[
    LiteralHeld,          # authored Held record from the fold
    IdentitySubstituted,  # (source Held, identity Held)
    Derived,              # Proof (recursive; derivation via another rule)
]
```

The shape is self-describing enough that a rendering layer can
walk the tree and produce an explanation of arbitrary verbosity.
Sketch 01 does not specify a rendering format; that is a tooling
concern.

## Worked example: Oedipus, parricide and incest

### Rules

```python
from substrate import Prop, Rule

PARRICIDE_RULE = Rule(
    id="R_parricide_from_killed_and_parent",
    head=Prop("parricide", ("X", "Y")),
    body=(
        Prop("killed",   ("X", "Y")),
        Prop("child_of", ("X", "Y")),
    ),
)

INCEST_RULE = Rule(
    id="R_incest_from_married_and_parent",
    head=Prop("incest", ("X", "Y")),
    body=(
        Prop("married",  ("X", "Y")),
        Prop("child_of", ("X", "Y")),
    ),
)

RULES = (PARRICIDE_RULE, INCEST_RULE)
```

### Agent-level firing: Oedipus after his anagnorisis

After the anagnorisis event at τ_s=13, Oedipus's held set
(literal) includes:

- `killed(oedipus, the-crossroads-victim)` at KNOWN (via observation
  at τ_s=-48).
- `identity(laius, the-crossroads-victim)` at KNOWN (via realization
  at τ_s=13).
- `child_of(the-exposed-baby, laius)` at KNOWN (via the shepherd's
  testimony at τ_s=12, plus…)
- `identity(oedipus, the-exposed-baby)` at KNOWN (via realization
  at τ_s=13).
- `married(oedipus, jocasta)` at KNOWN (from τ_s=-46).
- `child_of(the-exposed-baby, jocasta)` at KNOWN (via the shepherd).

Under identity substitution (I4), the identity-expanded starting
set also includes:

- `killed(oedipus, laius)` at KNOWN (via substitution of `laius`
  for `the-crossroads-victim`).
- `child_of(oedipus, laius)` at KNOWN (via substitution of
  `oedipus` for `the-exposed-baby`).
- `child_of(oedipus, jocasta)` at KNOWN (same).

The `parricide` rule, with bindings `X=oedipus, Y=laius`, finds
both body premises in the identity-expanded set at KNOWN. It
derives `parricide(oedipus, laius)` at KNOWN. Proof:

- rule_id: `R_parricide_from_killed_and_parent`
- bindings: `{X: oedipus, Y: laius}`
- premise_proofs:
  - `killed(oedipus, laius)` — via identity substitution of
    `killed(oedipus, the-crossroads-victim)` under
    `identity(laius, the-crossroads-victim)`.
  - `child_of(oedipus, laius)` — via identity substitution of
    `child_of(the-exposed-baby, laius)` under
    `identity(oedipus, the-exposed-baby)`.

The `incest` rule, with bindings `X=oedipus, Y=jocasta`, finds
both body premises in the identity-expanded set at KNOWN. It
derives `incest(oedipus, jocasta)` at KNOWN.

### What drops out of the encoding

The current author-asserted `parricide`/`incest` facts in
`oedipus.py` become redundant:

- `world(parricide("oedipus", "laius"))` at `E_crossroads_killing`
  → remove. The world derives it from the world-effects already
  present (`killed` and `child_of`).
- `world(incest("oedipus", "jocasta"))` at `E_marriage_and_crown`
  → remove. Same argument.
- Both agent-level observations at the two anagnoreses → remove.
  The substitution + rule derivation gives them both.
- Both `Disclosure` entries in `PREPLAY_DISCLOSURES` → remove.
  The reader's rule firing on the already-disclosed premises
  covers them.

A follow-on prototype pass retires these. Until the rule engine
lands, the author-asserted facts stand, with the current "candidate
for inference-rule derivation" comments pointing at this sketch.

### What does not drop out

Jocasta's anagnorisis at τ_s=9 gives her:

- `identity(oedipus, the-exposed-baby)` at KNOWN.
- `identity(oedipus, the-crossroads-killer)` at KNOWN.

And she already held (literally):

- `child_of(the-exposed-baby, jocasta)` at KNOWN (from the birth).
- `married(oedipus, jocasta)` at KNOWN (from τ_s=-46).
- `killed(the-crossroads-killer, laius)` at KNOWN (from τ_s=-47).

Under identity substitution, her state after the realization
includes `child_of(oedipus, jocasta)`, `killed(oedipus, laius)`.
Under the rules, she derives both `parricide(oedipus, laius)` and
`incest(oedipus, jocasta)` at KNOWN.

This works. Jocasta's realization, previously hand-augmented with
compound observations, now gets them from substitution + rule.

### What gets authored, not derived, after this sketch

The *domain facts* — `killed`, `child_of`, `married`, `identity` —
remain authored at their events. Rules cannot derive them (they
are primary premises, not compound conclusions). The sketch's
payoff is narrower than it might appear: it retires the
*compound* predicates, not the *primary* ones.

## Open questions

1. **OQ1 — Negation, for real.** Several rules that pass N9 in
   spirit need a non-equality or a NAF-style absence test to work
   in practice (`sibling`, `orphan`, `widowhood`). Sketch 02 should
   decide: (a) add typed inequality as a premise form (`X ≠ Y`
   against ground entities), (b) add stratified NAF, (c) force
   authors to expand rule families manually. (a) is cheap and
   covers many cases; (b) is more powerful but semantically
   subtle; (c) is ugly and loses the leverage rules are supposed
   to provide.
2. **OQ2 — Descriptions on rules.** An `authorial-uncertainty`
   description ("I'm not sure if this rule should fire on
   BELIEVED premises") needs to anchor to a rule. Adding
   `AnchorRef.kind == "rule"` is clean but is new
   description-surface territory. Descriptions-sketch-01's
   extensibility statement admits it; we defer the concrete
   wiring to a descriptions-sketch-02 pass.
3. **OQ3 — The probe criterion (N9) under pressure.** N9 is a
   necessary condition but not always sufficient. Cultural /
   moral compound predicates (`widow`, `orphan`, `betrayed`)
   pass N9 literally but carry connotation. Authors will pick
   differently across encodings. A later sketch may introduce a
   finer boundary — e.g., "rule heads may pass N9 but still be
   marked `description-preferred` for the encoding's library" —
   but sketch 01 declines to pre-design it.
4. **OQ4 — Interpretive predicates via substrate-backed pattern
   matching.** It is *possible* to express "X is hubristic" as a
   conjunction of typed premises (high status, prior warning
   ignored, acted against the warning's object). Such rules fail
   N9 (b): the judgment is not fully determined by the premises;
   the same pattern might fit two agents, only one of whom reads
   as hubristic. If a story encoding is honest about the
   imperfection, is such a rule admissible as a *proposal* rule
   (producing suggestions for author-reviewed descriptions), not
   a substrate rule? Sketch 01 says no; sketch 02 might revisit.
5. **OQ5 — Rule attention under staleness.** If a rule is edited
   (via a descriptions-style supersede + new-rule pattern), every
   previously derived fact's proof becomes stale. Does the query
   layer need a staleness signal comparable to
   `effectively_unreviewed`? Probably, once rule editing exists.
   Sketch 01 assumes rules are stable per-encoding and does not
   model rule staleness.
6. **OQ6 — Rule τ_a.** Should rules have their own authored-time
   stamp? The sketch punts: rules exist for the encoding's
   runtime. If an encoding adds a rule halfway through an
   authoring session, the rule should "have always been there"
   (all folds redrive, no state persists). Temporal rule scope
   — "this rule held only between τ_a=X and τ_a=Y" — is out of
   scope. A rule-versioning sketch can revisit.
7. **OQ7 — Proof-carrying query cost.** Returning proofs with
   every derivation is cheap for the Oedipus rule set but can
   inflate for richer encodings. Does the query API admit
   "derive without proofs" as a fast path? Probably yes, lazily:
   the proof is computed only if the caller reads it. Sketch 01
   treats the question as implementation.
8. **OQ8 — Multi-proof policies.** If the same fact is derivable
   via multiple rules or multiple binding sets, which proof is
   returned? Sketch 01 says "the shortest." Sketch 02 may give
   authors a choice (shortest, or "the one that uses rule X",
   or "all proofs"). For rendering anagnorisis chains, "all
   proofs" is informative; for most queries, "shortest" is what
   you want.
9. **OQ9 — Innocent-civilian tagging for tighter compound
   derivations.** Surfaced by the Macbeth reader-model probe
   (provenance: `prototype/reader_model_macbeth_output.json`,
   answer to `D_compound_predicates_candidate_for_derivation`).
   Macbeth's tyrant rule as currently authored
   (`kinslayer(X,_) ∧ regicide(X,_) ∧ king(X,_) ⇒ tyrant(X)`)
   derives `tyrant(macbeth)` at coronation (τ_s=6) — the moment
   he is first kinslayer, regicide, AND king. That misses an
   important shading: the *Macduff-family slaughter* at τ_s=12
   (`ordered_killing(macbeth, lady_macduff)`,
   `ordered_killing(macbeth, macduff_son)`) is what canonically
   *earns* the tyrant label in many readings — it's tyranny
   targeting innocents, distinct from tyranny by usurpation.
   The probe's proposed candidate:
   `ordered_killing(X, Y) ∧ innocent(Y) ∧ king(X, _) ⇒ tyrant(X)`.
   This requires a typed `innocent(...)` predicate the substrate
   does not yet have. Inference-02 territory: either add an
   `innocent` predicate authored per encoding, or generalize
   to a typed-inequality / NAF-based "Y is not a participant
   in any rebellion" condition (see OQ1). The probe's deeper
   point: a rule set should be permissive enough that several
   derivations of the same head can co-exist as alternative
   proofs — multi-proof per OQ8 — letting the trajectory
   verifier read which path actually fired.

## What happens next

1. **Prototype the rule engine.** Add `Rule`, `holds_derived`,
   `derive_all` to `substrate.py`. Add proof shape. Tests:
   rule firing per-fold, identity composition, slot propagation,
   fixpoint depth, authored-wins.
2. **Retire the author-asserted `parricide` / `incest` in
   `oedipus.py`.** Add a `RULES = (PARRICIDE_RULE, INCEST_RULE)`
   export. Remove the six author-asserted sites (two world
   effects, two agent-level observations at each anagnorisis,
   two reader disclosures). Existing tests should pass after the
   retirement; new tests check that derivation reproduces the
   previously-authored facts.
3. **Push the reader-model probe against the post-retirement
   encoding.** Two questions: does the probe notice that
   `parricide`/`incest` are now derived (and say sensible things
   about the move)? Does the probe, seeing `child_of` in both
   directions on the anagnorisis, propose *more* rules (sibling,
   uncle)? If yes to the second, we have the forcing function
   for OQ1 or OQ3 naturally.
4. **Bank OQ4 against a prescriptive-layer sketch.** "Rules as
   substrate-level assertions" vs. "rules as proposal-producing
   operators" is the inflection point between this sketch and
   the planned prescriptive / upper-layer sketch.
