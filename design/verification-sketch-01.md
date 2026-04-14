# Verification — sketch 01

**Status:** draft, active
**Date:** 2026-04-14
**Supersedes:** nothing (synthesis sketch; draws on lowering-sketch-01 and lowering-sketch-02)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md), [lowering-sketch-01.md](lowering-sketch-01.md), [lowering-sketch-02.md](lowering-sketch-02.md), [lowering-record-sketch-01.md](lowering-record-sketch-01.md)
**Superseded by:** nothing yet

## Purpose

Sibling to `lowering-record-sketch-01`. Architecture-sketch-02 A8
committed that verification at dialect boundaries is automated
linting emitting observations to the existing proposal queue,
but left the record shape and primitive kinds unspecified. Two
lowering exercises later, the verifier surface is concrete
enough to commit:

- Verification handles the coupling kinds that Lowering does
  not — Characterization and Claim (per lowering-sketch-01
  F1).
- Claim has two sub-kinds (lowering-sketch-02 F8): moment-
  pattern and trajectory-pattern. Each requires a distinct
  verifier primitive.
- Verification composes with inference-01's derivation surface
  (lowering-sketch-01 F7) — many checks consult derived
  substrate state, not just literal facts.
- Verification is separate from Lowering at the record level
  (lowering-sketch-01 F6, lowering-record-sketch-01 L10) —
  the two are not labor-divisions of the same mechanism.

This sketch specifies the verifier's output shape, three
primitive verifier kinds (Characterization, Claim-moment,
Claim-trajectory), how verifiers are declared per-record-type at
the dialect schema level, and how they compose with inference
and the proposal queue.

It explicitly does not cover dialect-internal constraint
propagation — the "pick propagates constraints on other picks"
pattern familiar from Dramatica's authoring software. That is a
within-dialect self-verification concern (an extension of
dramatic-sketch-01's M8 into the Template's theoretical
constraints), not a cross-boundary verification concern. The two
are complementary and share the proposal-queue output pipe, but
they are different concerns and belong in different sketches;
see the *Relation to dialect self-verification* section below.

## What this sketch *is* committing to

1. **V1 — Verification is automated linting at dialect
   boundaries.** Per architecture-sketch-02 A8, verification
   runs without authorial intervention over the upper records,
   the lower records, and (where applicable) the Lowering
   records between them, emitting observations about whether
   the coupling claims hold.
2. **V2 — Output is observations via the existing proposal
   queue, never errors.** Per architecture-02 A8. Verification
   emits `ReviewEntry` and specialized records (see *Output
   shape* below) that flow into the same queue
   `proposal_walker.py` already walks. Authors accept, decline,
   or skip each observation. No verifier can block a Story from
   being well-formed under its dialect; observations are
   advisory.
3. **V3 — Three primitive verifier kinds.** Characterization,
   Claim-moment, and Claim-trajectory. Each handles a specific
   coupling kind's verification (Characterization for
   Characterization couplings; Claim-moment and Claim-trajectory
   for the two Claim sub-kinds per lowering-sketch-02 F8).
   Realization is handled by Lowering records
   (lowering-record-sketch-01), not by a verifier of this sketch.
4. **V4 — Verifier speaks upper dialect's vocabulary,
   evaluates via lower dialect's queries.** Per A9. A
   Characterization verifier checking
   `DomainAssignment(T_overall_plague, domain="situation")`
   speaks in Domain and Throughline terms (upper), but the
   actual check is "do the Throughline's substrate events
   exhibit a situation-domain pattern?" — a query against
   substrate state. Verifier code for each boundary is
   dialect-pair-specific; the upper dialect provides the
   vocabulary of what to check, the lower dialect provides the
   query surface that answers it.
5. **V5 — Coupling kind is declared per-record-type at the
   dialect schema level.** When a dialect declares its record
   types (e.g., dramatic-sketch-01's `Throughline`, `Scene`,
   `DynamicStoryPoint`), each declaration names the coupling
   kind(s) that apply: `Character → Realization`,
   `DomainAssignment → Characterization`,
   `DynamicStoryPoint(outcome) → Claim (moment)`,
   `Argument.resolution_direction → Claim (trajectory)`,
   `Argument.domain → Flavor`. The declaration tells both
   authors (what to expect) and verifiers (what checks to run).
   A record type may admit multiple coupling kinds if different
   fields couple differently (e.g., Argument has
   trajectory-Claim *and* Flavor fields).
6. **V6 — Verification composes with inference-01's derivation
   surface.** Verifier checks read substrate state that may
   include derived facts per inference-model-sketch-01. Per
   lowering-sketch-01 F7 and lowering-sketch-02's reinforcement,
   many Claim checks are tractable only because derivation
   produces the compound facts (`parricide`, `regicide`,
   `tyrant`, `breach_of_hospitality`) the claims refer to.
   Verifier queries use the substrate's `holds_derived` /
   `derive_all` surface in the same way query sites elsewhere
   do.
7. **V7 — Partial-match observations are first-class.** A
   Characterization's pattern often holds over most of the
   scope but not all (e.g., Macbeth's MC Throughline is 70%
   Activity-Domain-shaped, 30% Manipulation-shaped — the
   author chose Activity as predominant). A verifier returning
   "partial match" is legitimate output, more useful than a
   binary pass/fail. Observations include a match-strength
   signal where applicable.
8. **V8 — Separate mechanism from Lowering.** Verification
   and Lowering records are architecturally distinct (A7/A8
   split; lowering-sketch-01 F6; lowering-record-sketch-01
   L10). Verifiers *read* Lowering records as part of their
   input but do not produce Lowerings. Lowerings are authored
   through the proposal queue; verifier output is a different
   kind of record (reviews and specialized advisories).

V1 through V8 pass A3 within the verification mechanism's scope:
each describes drift the schema catches rather than content an
attentive reviewer could self-police. Without V3's primitive
distinction, verifiers conflate moment and trajectory checks and
produce observations that are right-answer-wrong-reason (Macbeth
ending dead satisfies a moment check for Judgment=Bad but misses
the arc). Without V5's per-record-type declaration, authors and
verifiers drift on what check applies where. Without V7, partial
matches force binary verdicts and force-drop useful information.

## Verifier output shape

Verification emits records to the proposal queue. Three shapes:

### `VerificationReview`

A review attached to a specific record (upper record, Lowering
record, or Template record). Same shape as the existing
`ReviewEntry` from descriptions-01, with verdict and comment.
Used when verification's finding is naturally attached to one
record: "this Lowering's annotation reads weak," "this
DomainAssignment doesn't match the substrate pattern."

```
VerificationReview {
    reviewer_id       ("verifier:dramatic-substrate-char")
    reviewed_at_τ_a
    verdict           ("approved" | "needs-work" | "partial-match"
                       | "noted")
    anchor_τ_a        (snapshot of the reviewed record's τ_a)
    comment
    match_strength    (optional float in [0,1] for partial matches)
    target_record     (CrossDialectRef to the record being reviewed)
}
```

A `partial-match` verdict is the concrete output shape for V7.
`match_strength` lets the verifier signal how partial — 0.7 for
Macbeth's MC Activity Domain, 0.3 for a weak match. Authors can
filter by strength when walking observations.

### `StructuralAdvisory`

An observation not attached to a specific record. Used when the
finding spans multiple records (a trajectory-pattern check that
finds something interesting across many substrate events) or
references a record-type pattern rather than a record.

```
StructuralAdvisory {
    advisor_id        ("verifier:dramatic-substrate-claim-trajectory")
    advised_at_τ_a
    severity          ("noted" | "suggest-review" | "suggest-revise")
    comment
    scope             (SketchScope: what records / τ_s range the
                       advisory spans)
    match_strength    (optional)
}
```

Advisories are informational. They never carry an imperative;
`severity` is a hint, not a mandate. An author can walk
advisories the same way they walk reviews.

### `VerificationAnswerProposal`

A proposal specifically answering an upper-dialect authorial-
uncertainty question, produced by a verifier that found
evidence answering the question. Parallels
`AnswerProposal` from reader-model-01 but sourced from the
verifier rather than the reader-model. For example: Oedipus's
`D_witches_ontology_undecided` (a question about whether the
Witches are real supernatural agents) could receive a
`VerificationAnswerProposal` from a verifier that checks
whether the substrate treats the Witches' utterances as world-
level causal (which would imply real foresight) or as
agent-only effects (which leaves ontology open).

```
VerificationAnswerProposal {
    proposer_id       ("verifier:dramatic-substrate-claim-moment")
    question_id       (CrossDialectRef to the question)
    proposed_description
    rationale         (why the verifier believes its answer;
                       includes substrate evidence)
    proposed_at_τ_a
    status            ("pending" | "accepted" | "declined")
}
```

All three shapes flow through the existing proposal queue;
`proposal_walker.py` handles them with minor extensions (new
entry kinds to walk; accept/decline routes to specialized
ingest functions).

## The three primitive verifier kinds

### Characterization verifier

Checks that an upper record's *classification* matches a
substrate pattern.

**Signature:** given `upper_record`, `lower_scope` (the set of
substrate records the upper record classifies), and a
classification function, count how many lower records fit the
classification vs. how many don't. Return a `VerificationReview`
with `match_strength` if partial.

**Example:** `DomainAssignment(T_mc_oedipus, domain="activity")`
classifies the MC Throughline's events as activity-domain-
shaped. The verifier's check: for each event in the Throughline's
scope, does the event's type / predicate vocabulary match
activity-domain patterns? Output: "approved" if all or nearly
all match; "partial-match" with strength if some fraction match;
"needs-work" if very few match.

**Composition with inference:** the check may consult derived
facts. An event carrying `parricide(macbeth, duncan)` as a
derived fact matches the "activity-domain" pattern (killing is
activity) as well as it would if `parricide` were authored.

### Claim-moment verifier

Checks an upper record's assertion that substrate state at a
specific τ_s satisfies a specific condition.

**Signature:** given `upper_record`, the τ_s point the claim
references, and the substrate query the claim amounts to,
evaluate the query against the substrate fold at that τ_s.
Return a `VerificationReview` (binary: satisfied or not).

**Example:** `DynamicStoryPoint(axis=outcome, choice=success)`
claims the Story Goal is satisfied at the end. For Oedipus, Goal
= identify the pollution; check = `oedipus holds identity(
oedipus, the-crossroads-killer) at KNOWN at τ_s ≥ 13`. For
Macbeth, Goal = restore rightful succession; check =
`world_holds(king(malcolm, scotland)) at τ_s ≥ 18`. Binary:
satisfied or not.

**Composition with inference:** most interesting
Claim-moment checks require derived facts. Oedipus's
Outcome=Success check needs `parricide` or `regicide` or similar
compound truths; those are derived under inference-01's rule
surface. The verifier queries `holds_derived(...)`, not
`holds_literal(...)`.

### Claim-trajectory verifier

Checks an upper record's assertion about substrate state *across
a range of τ_s*. The check is a signature over the trajectory,
not a query at a single point.

**Signature:** given `upper_record`, the τ_s range the claim
references, and a trajectory signature function, iterate the
substrate fold across the range and evaluate the signature.
Return a `VerificationReview` or `StructuralAdvisory` depending
on whether the finding is attached to one record or spans many.

**Examples:**

- `Argument(A_ambition_unmakes).resolution_direction = affirm`
  for Macbeth. Check: does Macbeth's held-state trajectory
  exhibit progressive unmaking? Iterate τ_s = 0, 1, ..., 17;
  at each, count derived facts like `kinslayer`, `regicide`,
  `breach_of_hospitality`, `tyrant`; check that the count is
  monotonically non-decreasing and reaches a tyrant-labeled
  peak before his death. If yes, "approved." If the
  trajectory shows the MC becoming *better* (which would
  contradict the premise), "needs-work."

- `DynamicStoryPoint(axis=judgment, choice=bad)` for Macbeth
  (trajectory reading). Check: the MC's moral state declines
  cumulatively across the trajectory. Signature: derived
  tyrant-count increases; the final state is worse than the
  initial state by some measurable combination of predicates.

**Composition with inference:** trajectory signatures are the
workload where composition with inference matters most. Without
the compound-predicate derivations, the verifier would have to
inspect every killing event and judge its moral weight manually
— an interpretive task that does not belong in the verifier.
With the derivations, the verifier reads already-labeled
substrate state and the trajectory signature is mechanical.

## Declaring coupling kinds at the dialect schema level

Per V5, a dialect's record-type declarations name the coupling
kind(s) that apply. This is a dialect-schema concern that
dramatic-sketch-01 and dramatica-template-sketch-01 did not yet
formalize. The form (sketch-level, provisional):

```
RecordTypeDeclaration {
    name                  (e.g., "Character", "DomainAssignment")
    dialect               (e.g., "dramatic")
    fields                (the record's fields)
    coupling_kinds        (tuple of CouplingSpec)
}

CouplingSpec {
    kind                  ("realization" | "characterization"
                           | "claim-moment" | "claim-trajectory"
                           | "flavor")
    applies_to            (optional field name; if absent, applies
                           to the whole record)
    verifier_hint         (optional function or reference to
                           verifier code)
}
```

For example, `Character` couples via Realization (whole-record);
`DomainAssignment` couples via Characterization; `Argument` has
two couplings — `resolution_direction` via Claim-trajectory,
`domain` via Flavor.

The dialect's tooling reads these declarations to know what
verifier to run for each record. Implementation is tool-level,
not substrate-level; the declarations are data the dialect
module exports.

This piece is provisional because sketch 01 for each dialect
does not yet carry these declarations. A follow-on pass would
add them to dramatic-sketch-01 M10 or a dramatic-sketch-02
amendment.

## Composition with inference-01

Many verifier checks — especially Claim-trajectory —
consult substrate state that includes derived facts. The
substrate's query surface under inference-model-sketch-01
(`holds_derived`, `derive_all`) is what the verifier calls.

Implication: the substrate's prototype work on inference-01
(which is pending) is load-bearing for the verifier's
implementation. Until inference-01 lands in code, verifiers can
run against author-asserted compound predicates (as
`parricide`/`incest` are in oedipus.py today, or
`kinslayer`/`regicide`/`tyrant` in macbeth.py). Once inference-01
lands, the author-asserted compounds retire; the verifier's
checks do not change semantically — they still query the same
predicates — but the predicates now derive.

This is the cross-sketch dependency the architecture earns by
keeping verification a separate mechanism from Lowering: the
verifier evolves with the substrate's query surface, not with
Lowering's record shape.

## Partial-match handling

Per V7, a Characterization or Claim-trajectory check often
returns "mostly yes, not entirely." The verifier returns
`match_strength` (float in [0, 1]) alongside a
`partial-match` verdict.

Authors can filter observations by strength when walking. A
strength of 0.95 is a near-approval with a small flag; 0.5 is a
real divergence worth attention; 0.3 is "you should probably
revise this claim or the substrate."

Match strength is not a score for authorial evaluation — it's a
signal the verifier computed, not a grade. The author's decision
(accept / decline / skip) is the authorial act; the verifier's
strength is input, not output.

## Relation to architecture-sketch-02

- **A6 (stack of dialects).** Verification runs at boundaries.
  The stack's shape is presupposed.
- **A7 (lowering is author-driven).** Verifier reads Lowering
  records; does not author them. L10 restated: Verification and
  Lowering are separate record types and separate mechanisms.
- **A8 (verification at boundaries emits observations).** This
  sketch is the specification of A8's machinery.
- **A9 (verifier vocabulary).** V4 restates A9: verifier
  implemented in upper dialect's terms, evaluated via lower
  dialect's queries.
- **A10 (dialects opt-in, plural).** Verification runs only at
  boundaries the Story opts into. A Story with no dramatic-
  dialect records receives no dramatic-substrate verification.
- **A11 (reader-model probe generalizes).** The probe can
  collaborate with the verifier — observing where verifier
  confidence is low and proposing richer observations. Probe
  and verifier complement each other; they do not duplicate.

## Relation to dialect self-verification (M8) and Template constraint propagation

This sketch covers **cross-boundary** verification — upper records
verified against lower records. There is a parallel concern —
**within-dialect** verification — which this sketch does not
cover:

- Dramatic-sketch-01's M8 already specifies dialect self-
  verification for the base dialect (id resolution,
  Throughline/Character consistency, template multiplicity,
  etc.). These are *within-dialect* schema checks.
- A Template's *theoretical constraint propagation* — what
  Dramatica's "16,384 valid story forms" experience is
  actually made of — is also within-dialect: picking
  Approach=do-er and Problem=Pursuit constrains which
  Concern picks are coherent under Dramatica's joint theory.
  An attempted encoding with incoherent joint picks produces
  within-dialect constraint violations, independent of whether
  the substrate exists at all.

Both of these are within-dialect concerns. They complement
cross-boundary verification (this sketch) but are different
machinery:

| Concern                        | Mechanism                         | Sketch                                           |
|-------------------------------|------------------------------------|--------------------------------------------------|
| Schema check within-dialect   | Dialect self-verifier              | dramatic-sketch-01 M8                            |
| Template joint-theory check   | Template constraint-propagation    | dramatic-sketch-02 or a Template-constraint sketch |
| Realization binding           | Lowering record                    | lowering-record-sketch-01                        |
| Cross-boundary characterization | Cross-boundary verifier          | this sketch (verification-sketch-01)             |
| Cross-boundary claim (moment / trajectory) | Cross-boundary verifier | this sketch                                     |

All four emit to the same proposal queue. Authors walk a unified
queue; the queue entry's origin (self-verifier, template-
constraint checker, cross-boundary verifier) is visible but
doesn't bifurcate the walker.

**Why Dramatica's constraint-propagation is not in this sketch:**

The user's observation about Dramatica's 16,384 forms and the
"click into place" effect of picks constraining other picks is
a *within-dialect* phenomenon — Dramatica's joint theory relates
its own records to each other. A user making incoherent joint
picks is not failing to realize the substrate; they're failing
to cohere under Dramatica's theory. The right place for that
machinery is either a Template-level constraint-propagation
extension of M8 (probably dramatic-sketch-02's territory) or a
dedicated Template-constraint sketch. It is not this sketch.

The architecture keeps both concerns in scope without collapsing
them: cross-boundary verifier says "does the upper record's
claim match the substrate?"; within-dialect constraint
propagation says "do the upper records cohere under the
Template's theory?". Both run automatically, both emit to the
proposal queue, both respect "observations, not errors."

## Open questions

1. **OQ1 — Verifier cost.** Trajectory verifiers iterate substrate
   folds across τ_s ranges. Stories with many events and rich
   rule sets could produce expensive checks. The sketch does
   not specify when verifiers run (on commit? on demand? on a
   schedule?). Tooling decision, deferred to implementation.
2. **OQ2 — Verifier registration and discovery.** V5 specifies
   coupling-kind declarations per record-type; it does not say
   how a dialect *registers* its verifiers. Probably a
   per-dialect module exports both record-type declarations and
   verifier implementations, and the tooling wires them up. A
   future Tools sketch can formalize.
3. **OQ3 — Interactive verifier refinement.** An author walking
   observations might want to refine a verifier's
   configuration ("ignore partial-matches below 0.3 strength"
   or "skip Claim-trajectory checks for this Throughline").
   Is this tool-level or schema-level? Leaning tool-level;
   defer.
4. **OQ4 — Reader-model + verifier cooperation.** Architecture-02
   A11 says the reader-model probe generalizes to cross-boundary
   partner. The interaction with this sketch's verifier is
   undefined: does the verifier run first and the probe refine
   its observations? Does the probe run first and the verifier
   validate? Both? This sketch says "they complement" but does
   not specify the protocol. A future A11 refinement sketch
   can.
5. **OQ5 — Per-Story verifier tuning.** Different Stories may
   legitimately want different verifier strictnesses (a
   draft-state Story with pending Lowerings shouldn't be
   flooded with observations; a final-state Story might want
   the strictest possible checks). How does Story-level tuning
   interact with dialect-level verifier declarations?
   Provisionally: verifier settings are per-Story metadata;
   implementation choice.
6. **OQ6 — Verifier output at dialect-internal boundaries.** A
   two-dialect stack above substrate (Dramatic + Structural,
   if Structural ever lands) has a Dramatic↔Structural
   boundary as well as both-to-Substrate boundaries. A
   Structural record characterized by a Dramatic record uses
   a Dramatic↔Structural verifier; the sketch's three
   primitive kinds apply, but the verifier's lower query
   surface is now Structural, not substrate. The sketch's
   mechanics generalize cleanly, but multi-dialect stacks
   haven't been exercised — flagged for future pressure.
7. **OQ7 — Verifier provenance and reproducibility.** Should a
   verifier's output record *how* it arrived at its verdict
   (which substrate queries it ran, which derivations it
   consulted) for later reproducibility? Useful for debugging,
   expensive for storage. Lean toward "yes, via metadata,"
   defer.

## What happens next

1. **Commit the Lowering + Verification pair.** Both this
   sketch and `lowering-record-sketch-01` land together. The
   pair forms the load-bearing foundation for implementable
   cross-boundary machinery.
2. **Draft per-record-type coupling-kind declarations** as an
   amendment to dramatic-sketch-01 (or a short dramatic-
   sketch-01.5, or as a new field-addition to dramatic-sketch-02).
   Declarations name the coupling kind per record type so
   verifiers know which check to run where.
3. **Implementation pass in the prototype.** Add a tooling-
   level `verifier.py` alongside `proposal_walker.py`. The
   walker extends to handle `StructuralAdvisory` and
   `VerificationAnswerProposal` entries. A first verifier
   runs against Oedipus's Dramatic encoding (dramatic-sketch-01
   worked example) and emits observations into the existing
   proposal queue.
4. **Retire the substrate's author-asserted compound
   predicates** (parricide/incest in oedipus.py;
   kinslayer/regicide/breach_of_hospitality/tyrant in
   macbeth.py) by implementing inference-model-sketch-01 in
   the prototype, so verifiers consume derived facts rather
   than authored ones. Per V6, this doesn't change verifier
   semantics but removes a layer of author-asserted debt.
5. **Run cross-boundary reader-model probe** (architecture-02
   A11) on Oedipus and Macbeth dramatic-dialect encodings.
   First live test of A11; informs whether the probe and the
   verifier need a coordination protocol (OQ4).
6. **Draft dramatic-sketch-02 or a Template-constraint sketch**
   to cover Dramatica's "16,384 valid forms" constraint-
   propagation machinery. That is the within-dialect
   complement to this sketch's cross-boundary verifier and is
   needed before dramatica-complete becomes implementable.
