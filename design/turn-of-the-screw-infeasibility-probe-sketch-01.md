# Turn of the Screw — infeasibility probe — sketch 01

**Status:** draft, active
**Date:** 2026-04-15
**Supersedes:** nothing (new probe)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md), [substrate-sketch-05.md](substrate-sketch-05.md)
**Superseded by:** nothing

## Purpose

First deliberately-adversarial encoding probe. Per the feasibility
discussion following session 4 of the Ackroyd arc, a "good" answer
for this project includes the possibility of determining it is
infeasible. That answer can only come from tests that genuinely
risk failure.

Henry James's *The Turn of the Screw* (1898) is the first such
test. Its central structural feature is **sustained ontological
undecidability**: the novella refuses — at the textual level — to
commit to whether the ghosts the governess sees are real or are
projections of a hysteric. This undecidability is not a puzzle the
reader is supposed to solve; it is load-bearing to what the
novella IS. The critical literature has spent 127 years not
resolving it.

The test: can the substrate hold a text whose effect depends on
not committing to a world-fact?

The answer, documented below: **mechanically yes, semantically no.**
The substrate can hold a governess-perspective-only encoding that
never commits to ghost-existence at world-fact layer. But what it
cannot hold is *the ambiguity itself* — the property of the text
that the world-layer's non-commitment is deliberate and meaningful,
not missing. The substrate's silence looks identical to "we haven't
authored that fact yet."

## Method

A compact encoding (`prototype/turn_of_the_screw.py`, 7 fabula
events, 12 entities, 0 rules). Smoke-tested against the substrate's
projection machinery. Three encoding approaches were considered;
one was implemented. The other two are documented in code comments
and evaluated below.

The probe is not a production-quality encoding and is not intended
to lower to either dialect. The file exists as a discovery
instrument, not as a record we'll build on.

## What worked mechanically

Approach 1 (agent-belief-only) holds up against the substrate's
available machinery:

| Substrate query | Expected | Actual |
|---|---|---|
| `dead(peter_quint)` world-true | True (pre-play fact) | True |
| `dead(miles)` world-true | True (terminal event) | True |
| `apparition_of(peter_quint, the_tower)` world-true | *undetermined* | False |
| Governess holds `apparition_of(peter_quint, the_tower)` | KNOWN | KNOWN |
| Mrs. Grose holds same | BELIEVED (she hears the description) | BELIEVED |

The substrate's KNOWN/BELIEVED distinction captures the epistemic
gap the novella's prose opens between the governess and Mrs. Grose.
The agent-knowledge layer does real work here.

## What the substrate cannot hold

### The ambiguity itself as a property of the text

The substrate's silence on `apparition_of(peter_quint, the_tower)`
as a world-fact could mean any of:

- **the ghost is real but we haven't authored the fact yet** (a gap
  in the encoding),
- **the ghost is not real; we authored only the governess's
  belief** (a definite encoding choice),
- **the question is undetermined at world-fact layer by authorial
  intent** (what the novella claims is true).

The substrate has no way to distinguish these three cases from the
outside. A verifier asking "is `apparition_of` world-true?" will
get False identically under all three encodings. The ambiguity IS
the novella's subject, and the substrate represents it as the
absence of a fact — which is not a stable representation of a
load-bearing feature.

Contrast with Rashomon, where the contested branches let the
substrate say *positively*: "fact X holds on `:b-tajomaru`, fact X
does not hold on `:b-wife`, both branches are sibling-canonical."
Turn of the Screw's ambiguity is not a disagreement between
witnesses the substrate can branch; it is a refusal of the text to
adjudicate a single witness. Branches don't fit.

### Miles's cause of death

Miles dies in the final scene. Under the supernatural reading, his
death is the severance from possession; under the psychological
reading, his death is from fright or from the governess herself.
The substrate can hold `dead(miles)` without committing to a
cause — which the encoding did — but the text's entire effect turns
on the cause being undetermined.

A follow-on Dramatic encoding would want to name the scene's
conflict_shape and result. "Miles dies" is not a result; the text's
result is "Miles dies and we will never know why." Dramatic's Scene
record demands a `result` string; honest encoding would have to
render that undecidability into prose — which is exactly what
architecture-sketch-01 A3 said to route to descriptions, not
structure. The structure layer is being asked to carry what the
structure layer was designed to exclude.

### The inference engine has nothing to fire on

Macbeth's substrate produces derivations — tyrant from kinslayer +
regicide + king; betrayer_of_trust from killed + patient_of. These
derivations depend on world-fact antecedents. When the text refuses
world-fact commitment, the Horn-clause rule engine has no
antecedents. This is a structural finding: **the substrate's rule
engine cannot fire on a refused-commitment text.** Not because the
rules are wrong, but because the premises aren't there and won't
be.

For *Turn of the Screw*, no compound moral derivation is safely
authorable. `killed(governess, miles)` would require taking a side;
`released_from_possession(miles)` would require taking the other
side; no shared-across-readings predicate names the scene. The
RULES tuple is empty and must be.

### The frame narration is deeper than Sheppard's

Ackroyd's unreliable narration was handled by τ_s/τ_d divergence:
the murder's SjuzhetEntry at τ_d=15 rather than τ_d=2 encodes
Sheppard's withholding as "the reader learns this later." Turn of
the Screw has an outer framing device (Douglas reads the
manuscript aloud to a gathered audience, one member of whom is the
anonymous frame-narrator who tells *us* the story-of-the-reading),
which itself contains the governess's manuscript. Two nesting
levels of narration, each with its own BELIEVED-about-what-happened
state. The substrate has no machinery for nested narrators; the
sjuzhet's focalizer_id is a single agent per entry.

The encoding flattens this (focalizer_id="governess" throughout),
which is dishonest to the text's frame. Honest handling would need
a substrate extension for nested narration — not a minor addition.

## What this tells us about project feasibility

**The substrate holds facts, not epistemic regimes.** Its machinery
(world-facts + per-agent BELIEVED/KNOWN) is designed for texts that
*assert* things, where agents can be wrong about what's asserted.
It is not designed for texts that *withhold assertion itself* as
their structural move. Turn of the Screw is the latter.

This is a genuine boundary, not an engineering gap:

- **A new record type** (`UndeterminedClaim`?) that represents "this
  question is authorially-refused" would need to propagate through
  the verification layer. What would a verifier do with it? "Check
  that no substrate fact decides this"? That's a negative check, not
  a positive one, and doesn't produce the kind of generative
  guidance a 5-step author flow would want.

- **Descriptions carry interpretive content** per M1, which could
  hold a Description annotating the encoding with "undetermined-by-
  text." But Descriptions are informative, not verifiable. Routing
  the load-bearing feature to a layer the verifier doesn't probe
  makes the feature invisible to the infrastructure that was
  supposed to do author's-homework.

- **Branches work for Rashomon** because the text itself presents
  four candidate readings as contestants and never adjudicates.
  They don't work for Turn of the Screw because the text presents
  *one* reading (the governess's) and the question is whether to
  trust it. Adding a `:b-supernatural` / `:b-psychological` pair
  flattens the text's refusal into two distinct readings — neither
  of which is the text.

The project's claim that the engine "holds story" is genuine for
*story as asserted fact with agent-knowledge divergence*. It is
narrower than "holds story" in general. Turn of the Screw shows
there is a class of literary texts where the engine's machinery
has no purchase at structural layer.

## Is this infeasibility or just a limit?

Worth distinguishing:

1. **Strong infeasibility**: the engine fundamentally cannot
   represent a meaningful fraction of story. → NOT what the probe
   shows. Most stories commit to fact. Oedipus, Macbeth, Ackroyd
   all work.

2. **Weak infeasibility**: the engine cannot represent some
   literary effects that depend on authorial refusal-to-commit. →
   What the probe shows. The boundary is real and identifiable.

3. **Engineering limit**: we could extend the substrate to handle
   this with N more record types. → Possibly, but see the author-
   UX cost discussion below.

The probe's honest finding is (2) with some of (3) as a design
question rather than a feasibility one. The class of texts Turn of
the Screw represents (Borges' *The Garden of Forking Paths*, some
Kafka, some late James, some Faulkner) is a real and respected
literary tradition. The engine will not be general-purpose without
handling it. Whether handling it is worth the UX cost — which
would include asking authors to distinguish "not asserted" from
"authorially-refused" — is a project-scope decision, not a
technical one.

## What stays, what doesn't

What the probe *does not* undermine:

- The three existing encodings (Oedipus, Macbeth, Ackroyd) work
  and produce verifier output that finds real things. The
  architecture for assertion-heavy texts is doing useful work.
- The multi-dialect claim is empirically supported: two dialects
  capture genuinely different information about the same text.
- The substrate's epistemic machinery (project_knowledge,
  KNOWN/BELIEVED/KNOWN-FALSE) is load-bearing and works.
- The verifier infrastructure (orchestrate_checks, coverage_report)
  is reusable and does produce checks that flag real encoding gaps.

What the probe *does* undermine:

- Any claim that the engine is a *general* story-encoding
  machinery. It is a story-encoding machinery for stories within
  a subclass (roughly: assertion-heavy, 19th-century-realist-
  and-derivatives, individual-authorial-voice).
- The assumption that "extending the substrate" would be cheap
  for non-assertion-heavy texts. Adding UndeterminedClaim would
  ramify through every verifier; the UX cost to authors would be
  significant; and the generative payoff is unclear.

## Verdict

**Partial infeasibility surfaced; not project-killing.** The engine
works for a real and substantial subset of literary texts. It does
not work for the ambiguity-load-bearing subset. The honest answer
is not "stop" but "the project's scope claim narrows from *story*
to *asserted-fact story*, and any advertising should reflect
that."

This is a good outcome in the sense the feasibility framing
anticipated: a finding is produced, not a failure hidden. The
project continues, knowing its boundary.

A companion probe (*infeasibility-probe-02*? on downstream utility
— "can the verifier output produce useful authorial advice?") is
the next intended test.
