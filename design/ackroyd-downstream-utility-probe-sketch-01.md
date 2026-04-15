# Ackroyd — downstream utility probe — sketch 01

**Status:** draft, active
**Date:** 2026-04-15
**Supersedes:** nothing (new probe)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md), [verification-sketch-01.md](verification-sketch-01.md), [turn-of-the-screw-infeasibility-probe-sketch-01.md](turn-of-the-screw-infeasibility-probe-sketch-01.md)
**Superseded by:** nothing

## Purpose

Companion probe to the Turn of the Screw infeasibility test.
Per the feasibility discussion, #3 of the sharpest tests was:
"take the verifier output and try to produce actual authorial
revision advice. If the output is too thin to be useful, the
'homework-forcer' claim doesn't cash out."

This sketch executes that test against the Ackroyd Dramatic
encoding's verifier output (3 APPROVED reviews at 1.0 match,
67 coverage gaps across 4 record types). The question: **can
this output drive useful revision decisions by an author, or
is it ground-truth reportage that doesn't generate guidance?**

The finding, stated upfront: the output is genuinely useful for a
specific purpose (encoding-consistency verification) and
substantially less useful for a different purpose (story-level
authorial revision). The project's advertised "force humans/LLMs
to do their homework on stories" claim needs to distinguish between
these two kinds of homework. This probe names the distinction.

## Method

The verifier output:

```
Verifier: 3 results

  REVIEW [approved] target=dramatic:T_mc_sheppard
    match_strength: 1.00
    comment: main-character Throughline 'T_mc_sheppard': owner
    Character(s) ['C_sheppard'] lower to substrate Entity(ies)
    ['sheppard']; 13/13 of the Lowered substrate events have at
    least one owner Entity as a participant

  REVIEW [approved] target=dramatic:A_truth_recovers
    match_strength: 1.00
    comment: Argument A_truth_recovers (AFFIRM) trajectory at
    τ_s=8 (Poirot's reveal): killed(sheppard, ackroyd) world-
    literal: True; betrayer_of_trust derivable: True;
    driver_of_suicide derivable: True; Poirot KNOWS killed: True;
    4/4 truth-recovery signatures present

  REVIEW [approved] target=dramatic:S_poirot_reveal
    match_strength: 1.00
    comment: S_poirot_reveal result at τ_s=8: poirot KNOWS: True;
    caroline KNOWS: True; raglan KNOWS: True; flora KNOWS: True;
    4/4 cast-KNOWN-set signatures present

Coverage: 67 gaps
  by kind:
    characterization       6
    claim-moment           49
    claim-trajectory       12
  by record_type:
    Throughline            10
    Beat                   23
    Scene                  22
    Stakes                 12
```

Below, I attempt seven revision-advice items derivable from this
output. For each, I honestly evaluate whether it would help an
author revising the encoding (or the story behind it).

## Seven attempts at revision advice

### Item A: "MC-Antagonist alignment is verified cleanly."

**Derived from**: T_mc_sheppard REVIEW at 1.00; 13/13 participant
coverage.

**The advice**: "Your structural thesis — Sheppard as owner of the
main-character Throughline AND holder of the Antagonist function
slot — is verifying at full strength. The encoding's boldest
structural bet is paying out."

**Honest evaluation**: This is reassurance, not advice. It tells
the author "you're fine" rather than "change X." An author who
needed reassurance could use it, but it doesn't generate new
authorial action. **Utility: low-direct, moderate-as-confidence**.

### Item B: "Your counter-premise is named but never demonstrated."

**Derived from**: A_truth_recovers REVIEW shows the AFFIRM side
holds with 4 signatures; nothing in the verifier output shows the
COUNTER-premise ("the patient deceiver controls what can be
known") ever holding.

**The advice**: "Your Argument has a counter-premise, but no
substrate event demonstrates the counter-premise as even
momentarily true. Consider: is there a moment where Sheppard's
deception is operationally successful, from a perspective other
than his own? If the counter-premise isn't dramatized as holding
even briefly, your Argument is a stacked deck — the AFFIRM side
wins because the other side was never given breath."

**Honest evaluation**: This is real advice and points at a
genuine encoding/story question. An author might respond by:
(a) adding a beat where Sheppard's deception appears successful
to other characters; (b) concluding the counter-premise is correctly
unassailed because the novel is the AFFIRM's victory without pause;
(c) acknowledging the Argument's shape as deliberately one-sided.
Any of these is authorially productive. **Utility: high**.

### Item C: "Your Scene.conflict_shape claims are prose; consider whether they're verifiable."

**Derived from**: 22 Scene gaps all on conflict_shape
(claim-moment). None covered.

**The advice**: "Your 12 Scenes each carry a conflict_shape string
that claims something about the scene's dramatic tension. None are
machine-checkable in the current encoding. For each conflict_shape,
ask: what would a substrate probe look like? If you can articulate
one ('at τ_s=X, predicate Y holds'), author the check. If you
can't, the conflict_shape is routing at the descriptions layer, not
the structural layer — consider whether Scene needs a
machine-checkable field separate from the interpretive conflict_shape."

**Honest evaluation**: Mixed. Half of this is homework-about-
homework ("write more checks"); half is a real architectural
question ("are conflict_shapes structural or interpretive?"). The
architectural question has bite — if *most* Scene.conflict_shapes
are prose-only, the Scene record type may be carrying more
interpretive load than the M1 descriptions-routing rule wants. That's
a dialect-design question the Dramatic sketch might want to revisit.
**Utility: low-as-per-scene advice; moderate-as-meta-question**.

### Item D: "Stakes's at_risk may not be structurally verifiable."

**Derived from**: 12 Stakes claim-trajectory gaps, all on
fields like at_risk / to_gain / external_manifestation.

**The advice**: "Your 4 Stakes each claim what's at-risk in prose
— 'the village's moral and legal order,' 'Sheppard's life,
liberty, reputation,' 'Poirot's rational method's viability.'
None of these are directly substrate-testable: the substrate has
no predicate for 'moral order' at a community level, no predicate
for 'method viability.' Consider: are Stakes a structural commitment
the verifier should be able to probe, or an interpretive gloss
routing to descriptions? If the former, you need to invent
substrate-visible correlates (e.g., 'moral order = no innocent is
publicly accused at τ_s=end'). If the latter, Stakes' claim-
trajectory declaration may be mis-coupled."

**Honest evaluation**: Real and uncomfortable. This is a genuine
design question — Stakes are carrying significant interpretive
content, and the verifier is honestly unable to probe most of it.
The author's options are narrow: manufacture substrate correlates
(at the cost of forcing interpretive content into structural
shape) or revise the dialect's coupling declarations. Either
response is authorially productive. **Utility: high-as-design-
question**.

### Item E: "Beat.description_of_change on 23 beats: what's changing?"

**Derived from**: 23 Beat claim-moment gaps on description_of_change.

**The advice**: "Each of your 23 Beats claims a change — some
explicit ('Mrs. Ferrars dies'), some performative ('performs
the discovery next morning'), some internal ('the moral decision
is made'). For each, ask: what substrate state is different before
and after this beat? Explicit changes map to substrate effects
(dead, killed, derivable). Performative changes might not
('performs the discovery' leaves the substrate unchanged even
though something dramatic happened). Internal changes are often
invisible to the substrate (Sheppard's moral decision is a
mental-state change the substrate does not stage). If more than
half your beats are performative or internal, you're authoring
drama the substrate cannot probe, which limits the verifier's
reach."

**Honest evaluation**: Useful in aggregate, low per-beat. The
pattern-finding ("more than half your beats may be performative")
is a meaningful encoding-review question — it would surface a
potential dialect weakness. Per-beat advice is too thin to act on.
**Utility: moderate-as-pattern; low-per-item**.

### Item F: "Throughline role_label checks are asymmetric."

**Derived from**: Main-character Throughline has a check; the
other three Throughlines (overall-story, impact-character,
relationship) have role_label gaps uncovered.

**The advice**: "You verify the main-character Throughline by
checking the owner Character is a participant in lowered events.
That check has a name and a criterion. What are the analogous
criteria for the other three role_labels? For impact-character:
does the owner Character appear in events that *move* the MC's
position? For relationship: do lowered events involve the
relationship's two parties in scenes together? For overall-story:
does the lowered event-set span the story's conflict? Each
role_label is a structural claim; each should have a checkable
criterion. Currently only one does."

**Honest evaluation**: This is verifier-design advice, not
authorial advice. An author of a Dramatic encoding would say "I'm
not the person who invents the impact-character check; that's
dialect-design." The advice is useful for the engine's development,
not for revising *this* story. **Utility: high-for-engine-
development; low-for-encoding-revision**.

### Item G: "Dramatic and Save the Cat converge at the reveal — what is Dramatic adding?"

**Derived from**: Cross-dialect observation (from
cross-dialect-ackroyd-sketch-01) that both dialects' finale
checks exercise the same four substrate probes.

**The advice**: "Your Dramatic dialect's claim-moment check on
S_poirot_reveal and your Save the Cat dialect's claim-moment check
on B_14_finale produce identical substrate probes. At this
moment, the two dialects are agreeing rather than adding
complementary information. If dialects don't differ at
claim-moments, what DO they differ on? The answer should be:
Dramatic's arguments, counter-premises, stakes articulation, and
character functions; Save the Cat's 15-beat positional skeleton
and genre archetypes. Your encodings show these distinctions
elsewhere — but *not at claim-moments*. That's worth flagging as
a dialect-design property: claim-moments converge because they
probe the substrate; trajectory-and-characterization checks
diverge because they carry dialect-specific vocabulary."

**Honest evaluation**: This is an observation, not advice. It
names a pattern but doesn't tell the author what to do. It's more
useful as a note for dialect-design than for story revision.
**Utility: low-as-advice; moderate-as-design-finding**.

## Aggregate: what fraction is useful?

Of 7 advice items:

- **Genuinely useful to an author revising the encoding**: 2 (B
  and D). Both point at real gaps between the encoding's claims
  and the substrate's capacity; both suggest authorial actions
  that aren't "write more tests."
- **Useful as meta-questions about dialect design**: 3 (C, F, G).
  These inform future sketch amendments, not current story
  revision.
- **Useful per-pattern but thin per-item**: 1 (E). Aggregate
  pattern-finding; no per-beat action.
- **Reassurance, not advice**: 1 (A). Makes the author feel good;
  doesn't change what they do.

Of 7, **2 are directly actionable for authorial revision**. The
rest are either reassurance, dialect-design questions, or pattern
observations.

## What this tells us about the "homework-forcer" claim

The project memory records the goal as "force humans/LLMs to do
their homework on stories." This probe suggests a refinement:

The verifier forces **encoding homework** — it tells you where
your structural claims lack substrate support, where your
declarations are unchecked, where your Argument's counter-premise
is not demonstrated. This is real homework.

It does not force **story homework** — it cannot tell you whether
your story is working dramatically, whether a scene is flat,
whether a character needs more dimension, whether the pacing is
right. It is agnostic about story quality.

This is a meaningful distinction for the project's scope claim:

- **If the goal is encoding-homework**: the infrastructure is
  doing what it claims. The verifier output is useful; coverage
  gaps are a real backlog; partial-matches are informative.
- **If the goal is story-homework**: the infrastructure is doing
  a small part of it. It forces the author to be structurally
  honest, which eliminates one failure mode (inconsistent
  encoding). But it cannot assess dramatic quality.

## Relationship to the LLM integration track

The Ackroyd Dramatic output could plausibly drive useful advice
**if fed to an LLM with the story text**. An LLM could:

- Read the encoding + text together
- Notice which encoded claims are dramatically thin
- Suggest scenes that would strengthen the counter-premise
- Evaluate whether Stakes.at_risk language connects to felt peril
  in the prose

But this requires the LLM. The verifier output *alone* produces
the 2-of-7 utility ratio documented above. The engine's value in
author-assistance is largely as machine-readable input to a
reasoning layer we haven't yet built.

This repositions the project's value claim:

- **Weak claim** (supported): the engine produces structured,
  machine-readable, machine-verifiable encodings. The encodings
  are consistent; the verifier produces concrete output; gaps
  are queryable.
- **Strong claim** (not yet supported): the engine drives authorial
  revision directly. This probe shows the unmediated output is
  mostly not useful for that. An LLM-mediated layer might close
  the gap, but it doesn't exist yet.

## Verdict

**Downstream utility is partial.** The output is useful for
encoding-consistency work and for dialect-design questions. It is
not, unmediated, useful for story revision. The "homework-forcer"
claim holds for *encoding* homework; for *story* homework, the
engine is infrastructure awaiting a reasoning layer.

This is not project-killing. It is a scope-sharpening finding,
companion to the Turn of the Screw probe's scope-narrowing:

- **Turn of the Screw** narrows the claim from "story" to
  "assertion-heavy story."
- **This probe** narrows the claim from "force homework on
  stories" to "force encoding homework; story homework awaits
  LLM-mediated reasoning."

Both findings sharpen what the project actually is. A 20-year
project benefits from knowing what it is not.

## What's next after these two probes

The probes suggest the project's next-most-valuable move is
likely the LLM-mediated reasoning layer — the thing that would
convert 2-of-7 direct utility into something closer to 5-of-7
mediated utility. This was item #2 on the original feasibility
test list ("machine-assistability infeasibility: give the engine
+ docs to an LLM and ask it to encode a new story"). That probe
is now upstream of a more interesting one: "give the engine's
output to an LLM alongside the story text, and see what it
generates."

Not-yet-scoped. The probe order is roughly right: narrow the
positive scope first (these two probes), then test whether the
scope-narrowed claim can be augmented by LLM reasoning.
