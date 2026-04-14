# Lowering — sketch 02 (Macbeth exercise)

**Status:** draft, active
**Date:** 2026-04-14
**Supersedes:** nothing — second exercise parallel to [lowering-sketch-01.md](lowering-sketch-01.md)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md), [dramatic-sketch-01.md](dramatic-sketch-01.md), [dramatica-template-sketch-01.md](dramatica-template-sketch-01.md), [lowering-sketch-01.md](lowering-sketch-01.md)
**Superseded by:** nothing yet

## Purpose

Second lowering exercise, parallel to lowering-sketch-01's Oedipus
case, using Shakespeare's *Macbeth* as a structurally different
test. The primary question this exercise is meant to answer: does
the four-coupling-kinds framework that lowering-sketch-01 settled
on (Realization / Characterization / Claim / Flavor) hold up on a
story whose trajectory differs fundamentally from Oedipus's? If
yes, the framework is ready to inform synthesis sketches
(`lowering-record-sketch-01` and `verification-sketch-01`). If a
fifth kind emerges, the framework needs more work before
synthesis is appropriate.

This exercise deliberately resists the temptation to re-run the
Oedipus walk-through on a new story. The interesting question is
not *can we produce Lowering records for Macbeth* — of course we
can, the machinery exists — but *what pressure does Macbeth put
on the four-kinds distinction*. The sketch's core section looks
at Macbeth's specific structural features (action-first MC,
moral trajectory rather than epistemic inversion, multiple
readings of the Antagonist role, supernatural elements as
Throughline participants) and asks which coupling kinds they
surface and whether anything new emerges.

A secondary question: which of Oedipus's exercise findings
generalize? F1 through F7 were drawn from one encoding. Oedipus
is *heavily epistemic* — the whole play is dramatic irony with
the reader holding what the characters don't. Macbeth's structure
is *action and consequence* — the MC knows from early what he is
doing; the trajectory is moral, not epistemic. If findings that
were framed around Oedipus-as-epistemic-story still hold on
Macbeth, the framework is genuinely cross-story; if not, we know
which findings are Oedipus-specific.

## What this exercise *is*

- A targeted pressure test of lowering-sketch-01's four-coupling-
  kinds framework on a structurally different story.
- A sketched encoding of *Macbeth* in both the dramatica-complete
  Template and the substrate dialect, sufficient for the coupling
  exercise but not a full encoding. No `macbeth.py` is produced;
  the substrate side is specified in prose.
- An honest search for a fifth coupling kind. Candidates to
  probe: counterfactual-shaped couplings (Stakes, prophecy),
  promissory-shaped couplings (prophecy that binds future
  substrate state), negative-shaped couplings (missing or
  under-filled roles).
- A comparison with the Oedipus exercise, naming which findings
  generalize and which are Oedipus-specific.

## What this exercise is *not*

- A full substrate encoding. No `macbeth.py` is written. The
  substrate side is specified as prose sketch; what events
  would exist, which Entities, which Descriptions. A prototype
  task could later author it.
- A Lowering-record-shape commitment. The exercise informs the
  future record-shape sketch but does not pre-empt it.
- An exhaustive walk of every upper record. Where Oedipus went
  record-by-record through one play, Macbeth is walked
  selectively — the cases that pressure coupling kinds are
  the interesting ones, and this sketch stays on those.

## What Macbeth brings that Oedipus didn't

Before the exercise, a short catalog of Macbeth's structurally-
distinctive features. These are the specific places the four-
kinds framework might strain.

1. **Action-first MC.** Oedipus *investigates* (epistemic
   trajectory; gap closure is the arc). Macbeth *acts* (moral
   trajectory; the MC knows what he is doing at each step and
   does it anyway). The MC Throughline's Domain is likely
   Activity, not Situation.
2. **Moral inversion, not epistemic inversion.** Oedipus ends
   at an anagnorisis — one moment where everything changes.
   Macbeth ends at a moral nadir reached *gradually* — Duncan's
   murder, then Banquo's, then Lady Macduff's family, then the
   descent into paranoia, then Lady Macbeth's suicide, then his
   own death. The Argument's resolution is a trajectory, not a
   moment.
3. **Multiple Antagonist readings.** Macduff (kills Macbeth);
   Lady Macbeth (drives the initial murder); the Witches
   (prophesy and manipulate); Macbeth himself (agent of his own
   destruction). A dramatica-complete Template expects exactly
   one Antagonist. Macbeth genuinely fits no single assignment
   cleanly.
4. **Supernatural Throughline participants.** The Witches are
   causal in the narrative but are not Characters in the full
   Dramatic sense (they have no backstory, no interiority, no
   stakes; they are *forces*). Can a Throughline owner be a
   force rather than a Character? The dialect's M2 admits
   abstract owners; Macbeth tests whether it admits supernatural
   ones.
5. **Prophecy as binding on future state.** The Witches'
   prophecies are upper-dialect commitments about substrate
   state at future τ_s. "You will be king" commits the substrate
   to realize `king(macbeth, scotland)` eventually. This is a
   *promissory* relationship between upper and lower, not clearly
   any of the four Oedipus kinds.
6. **Stakes-as-counterfactual.** Oedipus's Stakes were articulated
   in terms of what would-be-lost. Macbeth's Stakes are similar
   but sharper: at each killing, the MC's soul moves further
   out of reach. Stakes articulate an *alternate possible
   trajectory* — what the soul could have been had the killing
   not happened. Counterfactual couplings may or may not fit
   the four kinds.
7. **Cumulative Judgment.** Oedipus's Judgment=Bad lands at one
   moment (the anagnorisis + self-blinding). Macbeth's
   Judgment=Bad accumulates across multiple moments. The Claim
   coupling for Judgment may need to be trajectory-shaped
   rather than moment-shaped.

## The upper encoding — Macbeth in dramatica-complete

Sketched, not exhaustively specified. Italics indicate
declarations made here specifically to have something to walk
through, with alternatives noted where the reading is
genuinely contested.

### Story and Argument

```
Story {
    id = "S_macbeth"
    title = "Macbeth"
    character_function_template = "dramatica-complete"
    story_goal = "restore rightful succession and kingly order
                  to Scotland"
    story_consequence = "Scotland remains under tyranny;
                         unnatural order endures"
}

Argument {
    id = "A_ambition_unmakes"
    premise = "unchecked ambition unmakes the one who indulges it"
    counter_premise = "ambition is what elevates; restraint is
                       the passive choice of the mediocre"
    resolution_direction = "affirm"
}
```

### Throughlines and Domain Assignments

```
Throughline { id = "T_overall_scotland",
              role_label = "overall-story",
              owners = [ "the-situation" ],
              subject = "a kingdom usurped by unnatural means;
                         its rightful succession at stake",
              argument_contribution =
                  { arg: A_ambition_unmakes, side: "complicates" }
            }
DomainAssignment { throughline = T_overall_scotland,
                   domain = "situation" }

Throughline { id = "T_mc_macbeth",
              role_label = "main-character",
              owners = [ C_macbeth ],
              subject = "a capable warrior who acts on ambition
                         and cannot stop, escalating until he
                         is undone",
              counterpoints = [ T_impact_lady_macbeth ],
              argument_contribution =
                  { arg: A_ambition_unmakes, side: "affirms" }
            }
DomainAssignment { throughline = T_mc_macbeth,
                   domain = "activity" }

Throughline { id = "T_impact_lady_macbeth",
              role_label = "impact-character",
              owners = [ C_lady_macbeth ],
              subject = "a woman who demands the killing and
                         then cannot bear what she demanded",
              counterpoints = [ T_mc_macbeth ],
              argument_contribution =
                  { arg: A_ambition_unmakes, side: "affirms" }
            }
DomainAssignment { throughline = T_impact_lady_macbeth,
                   domain = "manipulation" }

Throughline { id = "T_relationship_macbeths",
              role_label = "relationship",
              owners = [ "the-relationship" ],
              subject = "a marriage-as-conspiracy that curdles
                         into mutual isolation",
              argument_contribution =
                  { arg: A_ambition_unmakes, side: "affirms" }
            }
DomainAssignment { throughline = T_relationship_macbeths,
                   domain = "fixed-attitude" }
```

### Characters

```
Character { id="C_macbeth",     functions=[Protagonist, Emotion] }
Character { id="C_lady_macbeth", functions=[Contagonist] }
Character { id="C_macduff",     functions=[Antagonist, Skeptic] }
Character { id="C_banquo",      functions=[Sidekick] }
Character { id="C_malcolm",     functions=[Reason] }
Character { id="C_witches",     functions=[Guardian] }
# Duncan, Lady Macduff, Fleance, and others appear as
# participants in events but do not carry named functions.
```

The Antagonist=Macduff reading is one defensible choice; many
productions read Lady Macbeth (Contagonist) as the functional
antagonist of the first half. The sketch makes Macduff the
Antagonist on the "kills the MC" criterion and notes the
ambiguity as a surfaced case below.

### DynamicStoryPoints

```
DynamicStoryPoint { axis=resolve,  choice=change    }
DynamicStoryPoint { axis=growth,   choice=stop      }  # Macbeth must stop
                                                        # killing; cannot
DynamicStoryPoint { axis=approach, choice=do-er    }
DynamicStoryPoint { axis=limit,    choice=optionlock }
DynamicStoryPoint { axis=outcome,  choice=success  }
DynamicStoryPoint { axis=judgment, choice=bad     }
# Outcome × Judgment = Personal Tragedy. Same canonical ending
# as Oedipus, different shape of trajectory.
```

The Outcome=Success pick reads Scotland's restoration as the
Overall Story Goal: the Goal is *satisfied* (Malcolm is crowned,
tyranny ends). An alternative reading takes Macbeth's personal
goal (become and stay king) as the Story Goal; under that
reading Outcome=Failure. The dialect's M1 allows multiple
Arguments; a future pass might split these.

### Scenes (named; positions schematic)

```
Scene { id = "S_prophecy",         narrative_position =  1 }
Scene { id = "S_letter",           narrative_position =  2 }
Scene { id = "S_plot",             narrative_position =  3 }
Scene { id = "S_duncan_killed",    narrative_position =  4 }
Scene { id = "S_macbeth_crowned",  narrative_position =  5 }
Scene { id = "S_banquo_killed",    narrative_position =  6 }
Scene { id = "S_banquo_ghost",     narrative_position =  7 }
Scene { id = "S_second_prophecy",  narrative_position =  8 }
Scene { id = "S_macduff_flees",    narrative_position =  9 }
Scene { id = "S_macduff_family",   narrative_position = 10 }
Scene { id = "S_sleepwalking",     narrative_position = 11 }
Scene { id = "S_lady_macbeth_dies",narrative_position = 12 }
Scene { id = "S_macbeth_dies",     narrative_position = 13 }
Scene { id = "S_malcolm_crowned",  narrative_position = 14 }
```

### Stakes

```
Stakes { id = "Stakes_scotland",
         owner = { kind: "throughline", id: T_overall_scotland },
         at_risk = "the kingdom's rightful succession and natural
                    order",
         to_gain = "restoration to rightful king and the lifting
                    of unnatural omens" }

Stakes { id = "Stakes_macbeth_soul",
         owner = { kind: "throughline", id: T_mc_macbeth },
         at_risk = "Macbeth's humanity — his capacity to feel
                    horror at what he has done",
         to_gain = "nothing he doesn't already have by Act 3.
                    By play's end the to_gain is empty." }
```

## The lower encoding — Macbeth in substrate (sketched)

No `macbeth.py` is written here; this is a design sketch of what
the substrate would contain. Enough to do the coupling walk.

### Entities

- `macbeth`, `lady_macbeth`, `duncan`, `macduff`, `banquo`,
  `malcolm`, `fleance`, `lady_macduff`, `ross`.
- `the_witches` as a single entity of kind `supernatural-force`
  (or three separate entities — `witch_first`, `witch_second`,
  `witch_third` — depending on how the encoding wants to handle
  them; the exercise picks the collective form to surface the
  ownership-by-force question).
- Locations: `scotland`, `dunsinane`, `inverness`, `birnam_wood`,
  `england`.

### Events (partial list)

- `E_battle_macbeth_hero` (τ_s = -5, pre-play) — Macbeth
  defends Scotland; world-true `defended(macbeth, scotland)`;
  agent-observed by various.
- `E_prophecy` (τ_s = 0) — Witches meet Macbeth and Banquo.
  Key effects: agent-observed `prophecy(macbeth, will_be_king)`
  for Macbeth; agent-observed `prophecy(banquo, descendants_kings)`
  for Banquo; both at slot=KNOWN, via=UTTERANCE_HEARD.
- `E_letter_written` (τ_s = 1) — Macbeth writes to Lady
  Macbeth reporting the prophecy. Not directly observed by
  reader yet but authored for lowering purposes.
- `E_plot` (τ_s = 2) — Macbeth and Lady Macbeth agree on
  Duncan's killing.
- `E_duncan_killed` (τ_s = 3) — world-true `killed(macbeth,
  duncan)`, `dead(duncan)`. Macbeth agent-observes it. Lady
  Macbeth is complicit but does not swing the dagger.
- `E_macbeth_crowned` (τ_s = 4) — world-true `king(macbeth,
  scotland)`.
- `E_banquo_killed` (τ_s = 5) — world-true `killed(murderers,
  banquo)`, `dead(banquo)`; world-true `ordered_killing(macbeth,
  banquo)`.
- `E_fleance_escapes` (τ_s = 5.5) — Banquo's son escapes; the
  Witches' prophecy about Banquo's descendants remains alive.
- `E_banquo_ghost_appears` (τ_s = 6) — world-true
  `apparition_of(banquo, feast)`. Whether this is a supernatural
  event or a hallucination is a descriptions-01 question; the
  substrate records the apparition as world-true and leaves the
  ontology to descriptions.
- `E_second_prophecy` (τ_s = 7) — Macbeth returns to the
  Witches. Agent-observed: `prophecy(macbeth, safe_from_woman_born)`,
  `prophecy(macbeth, safe_until_birnam_wood_moves)`. Slot=KNOWN.
- `E_lady_macduff_killed` (τ_s = 9).
- `E_sleepwalking` (τ_s = 10) — Lady Macbeth's unraveling,
  observed by Doctor and Gentlewoman.
- `E_lady_macbeth_suicide` (τ_s = 11) — world-true
  `dead(lady_macbeth)`.
- `E_birnam_moves` (τ_s = 12) — world-true
  `moving_toward(birnam_wood, dunsinane)` (realized by
  Malcolm's soldiers carrying branches).
- `E_macduff_kills_macbeth` (τ_s = 13) — world-true
  `killed(macduff, macbeth)`, `dead(macbeth)`; world-true
  `born_not_of_woman(macduff)` (Caesarean birth) disclosed as
  agent-observation to Macbeth just before.
- `E_malcolm_crowned` (τ_s = 14) — world-true `king(malcolm,
  scotland)`.

### Sjuzhet (partial)

The play opens with the Witches on the heath. `τ_d = 0` is the
prophecy; `τ_d = 13` is Macbeth's death; `τ_d = 14` is
Malcolm's coronation. The battle (pre-play) can be a preplay
disclosure. No audience-knowledge-of-myth preamble comparable
to Oedipus's — *Macbeth* is fabula-first, with the audience
learning the backstory as the play unfolds.

### Descriptions (partial, illustrative)

- `D_prophecy_ambiguity` — the Witches' prophecies are
  literally true but catastrophically misleading.
- `D_macbeth_moral_trajectory` — Macbeth's descent from
  hero-of-Scotland to tyrant-of-Scotland is continuous, not
  stepwise; each killing removes another inhibition.
- `D_lady_macbeth_inverse` — Lady Macbeth is the driving force
  in Act 1 and 2; she unravels in Act 4 and 5. The Impact
  Character role's *direction* reverses.
- `D_witches_status` — whether the Witches are supernatural
  agents, projections of Macbeth's own ambition, or actual
  metaphysical forces is not adjudicated. The substrate records
  their utterances as events; the description records the
  authorial reticence.
- `D_argument_trajectory` — the Argument's premise ("ambition
  unmakes") is affirmed across the trajectory, not at any one
  moment. The proof is cumulative.

### Rules (inference-01 style, illustrative)

- `killed(X, Y) ∧ kinsman_of(X, Y) → kinslayer(X, Y)` —
  Macbeth kills Duncan, his kinsman; derived `kinslayer(macbeth,
  duncan)`.
- `killed(X, Y) ∧ king(Y, _) ∧ usurps(X, _) → regicide(X, Y)` —
  Macbeth kills Duncan while usurping; derived `regicide(macbeth,
  duncan)`.
- `killed(X, Y) ∧ guest_of(Y, X) → breach_of_hospitality(X, Y)`
  — Duncan was Macbeth's guest when killed.

These rules would each pass N9 definitionally. They matter for
the Judgment claim below.

## Coupling exercise, organized by kind

The exercise proceeds by coupling kind. Each sub-section names
the kind, walks through Macbeth's interesting cases, and asks
whether the kind's framing holds up.

### Realization couplings

- **`Character(C_macbeth) → Entity("macbeth")`.** Clean.
- **`Character(C_lady_macbeth) → Entity("lady_macbeth")`.**
  Clean.
- **`Character(C_macduff) → Entity("macduff")`.** Clean.
- **`Character(C_witches) → Entity("the_witches")`.** Clean
  under the collective-entity choice. If the substrate had
  chosen three separate Entities, this Lowering would be
  one-to-three. Authorial choice for the lowering; no
  framework strain.
- **`Scene(S_prophecy) → Event(E_prophecy) + SjuzhetEntry(τ_d=0)
  + Description(D_prophecy_ambiguity)`.** Clean, multi-record,
  same pattern as Oedipus's `S_anagnorisis`.
- **`Scene(S_duncan_killed) → Event(E_duncan_killed) +
  SjuzhetEntry(τ_d=3) + Description(D_macbeth_moral_trajectory,
  partial anchor)`.** Clean. Note the description is shared
  across multiple Scenes (the descent); one description can be
  a lowering target for several Scenes.
- **`Throughline(T_mc_macbeth) → {every event with macbeth as
  participant; every description focalized on macbeth}`.**
  Clean, large-set realization. Same pattern as Oedipus.

*Assessment: Realization coupling handles Macbeth's standard
cases without strain. The pattern generalizes from Oedipus
cleanly.*

### Characterization couplings

- **`DomainAssignment(T_mc_macbeth, activity)`.** The MC
  Throughline is claimed to be Activity Domain — external,
  process-oriented. Verifier check: do the events in
  T_mc_macbeth's scope predominantly involve external action
  (killing, fighting, ordering, moving)? For Macbeth: yes, at
  Act 1–3; ambiguous in Act 4 (the paranoia sections are more
  internal); yes again at Act 5. A verifier counting action
  events vs. internal-state-change events would find this
  *mostly* characterization-confirming, with one stretch
  (Act 4's psychological deterioration) that might reasonably
  be characterized as Manipulation instead. The Characterization
  coupling works but reveals the substrate's pattern isn't
  uniform; the author chose Activity as the predominant reading.
- **`DomainAssignment(T_impact_lady_macbeth, manipulation)`.**
  Manipulation Domain is about internal process. Lady Macbeth's
  Throughline is largely about psychological manipulation (of
  Macbeth, of herself, of the evidence she tries to wash from
  her hands). A verifier looking for internal-process events
  finds them throughout her Throughline's scope. Clean
  characterization.
- **`QuadPick(concern=doing)` on T_mc_macbeth** (within
  Activity Domain's Concern quad). "Doing" as the MC's Concern:
  Macbeth is characterized by doing — not obtaining, not
  learning, not understanding, but doing. Verifier: count
  action-type events in scope. Clean.

*Assessment: Characterization holds. The verifier's checks here
are "does the pattern of substrate events match the
classification label?" and they work. One discovery: characterization
claims can be *partially* true (Activity fits 70% of Macbeth's
trajectory; Manipulation fits the middle 30%). This is fine —
the author picked the predominant reading; the verifier's
observations would note partial mismatch without rejecting.*

### Claim (moment-pattern) couplings

- **`DynamicStoryPoint(outcome=success)`.** Story Goal: restore
  rightful succession. Substrate state at τ_s = 14: world-true
  `king(malcolm, scotland)`, world-true `dead(macbeth)`,
  world-true `dead(lady_macbeth)`. The Goal is satisfied at
  τ_s ≥ 14. Verifier check: `world_holds(king(malcolm,
  scotland)) at τ_s ≥ 14` — yes. Clean moment-pattern Claim.
- **`DynamicStoryPoint(judgment=bad)` (as moment-pattern
  reading).** Judgment=Bad could be read as a moment-pattern
  check at the MC's final state: `dead(macbeth) ∧ tyrant(macbeth)`
  at the end. Verifier: does the MC end in a personally-bad
  state? Yes. Clean moment-pattern.

But — this is where Macbeth strains. Judgment=Bad for Macbeth
reads more naturally as *trajectory-pattern* than
*moment-pattern*. A final-moment check would confirm it but
miss the point. The point is that the MC's state *worsened
across the trajectory* — hero to tyrant to corpse. A single
final-moment verifier misses the arc. See the next sub-section.

### Claim (trajectory-pattern) couplings

This is where Macbeth exerts its distinctive pressure.

- **`Argument(A_ambition_unmakes).resolution_direction = affirm`.**
  The Argument claims that ambition unmakes the one who indulges
  it. Verifier must check the *trajectory*: does Macbeth's state
  exhibit progressive unmaking? A single-moment check at τ_s = 13
  confirms only that he is dead. The Argument's affirmation needs
  cumulative evidence: `killed` count rises; `king(macbeth, _)`
  holds transiently; his psychological descriptions
  (D_macbeth_moral_trajectory) show progressive loss; the rules
  would derive a compound `tyrant(macbeth)` accumulating from
  each unjust killing.

  The verifier here is genuinely trajectory-shaped. It reads
  substrate state across multiple τ_s points and evaluates a
  trajectory signature. This is a different class of check
  than the moment-pattern Outcome=Success check above.

- **`DynamicStoryPoint(judgment=bad)` (trajectory reading).**
  Judgment=Bad is *better* characterized as a trajectory: each
  killing removes another piece of Macbeth's humanity; by the
  time he says "I have almost forgot the taste of fears" (Act 5
  scene 5), his Judgment=Bad has been earned over many scenes.
  A trajectory-pattern verifier tracks descriptions or rule-
  derived `tyrant` / `regicide` / `kinslayer` / `breach_of_hospitality`
  accumulating across τ_s.

*Assessment: Trajectory-pattern Claim is genuinely distinct
from moment-pattern Claim, and both are distinct from
Realization and Characterization. Macbeth makes this difference
load-bearing where Oedipus didn't — Oedipus's Judgment=Bad
landed at a moment, so the distinction didn't bite. In Macbeth,
a moment-only verifier would approve Judgment=Bad for the wrong
reason (the MC ended dead and tyrannical, so yes, bad) and would
miss the Argument's actual structural work (ambition **unmakes**
— the unmaking is a process).*

This is lowering-sketch-01's F6 (Verification is load-bearing)
now specialized: **the verifier surface needs both moment-pattern
and trajectory-pattern primitives**, and they are genuinely
different.

### Flavor couplings

- **`Argument.domain = "moral-philosophical"` or "tragic-moral"
  or "ethical"** — author-free-form. No verifier, no
  realization. Purely documentation.

Standard. Same as Oedipus.

## Looking for a fifth coupling kind

The exercise deliberately probes for cases that might require
a fifth coupling kind. Three candidates examined:

### Counterfactual coupling (Stakes-as-possible-loss)

Stakes articulate what could be lost. `Stakes_macbeth_soul`
says Macbeth's humanity is at risk. The substrate can show
what happened (he lost it, as witnessed by the trajectory of
killings and the descriptions of his moral descent), but
Stakes' claim is specifically about the counterfactual: what
he *could have remained* had he not killed Duncan.

Is this a new coupling kind? Assessment: No. Stakes couples to
the substrate via:

1. **Realization** (the Stakes record may have a description
   lowered to the substrate's description surface — e.g.,
   `D_macbeth_conscience_before_murder` realizing that the
   soul-at-risk claim is substantively authored).
2. **Characterization** (the Stakes classify the Throughline's
   pressure — "the soul is at risk" is a pattern-label about
   what the Throughline is *about*).
3. **Claim (trajectory)** (the Stakes are verified by the
   trajectory's unfolding — the soul is lost across the
   trajectory, affirming that it *was* at risk).

The counterfactual aspect ("what could have been") is not a
separate coupling to substrate — it is an *implication* of the
Stakes record, derivable within the Dramatic dialect without
substrate lookup. A Dramatic-dialect query "what does
Stakes_macbeth_soul imply about Macbeth's possible alternative
trajectory?" stays within the Dramatic dialect.

**Verdict: Counterfactual is not a fifth coupling kind.**
Counterfactuals live within-dialect; their relationship to
substrate decomposes into combinations of the existing four.

### Promissory coupling (prophecy → future state)

The Witches' prophecy at `E_prophecy` says "Macbeth will be
king." This is an upper-dialect claim about a future substrate
state. The substrate at τ_s = 4 realizes `E_macbeth_crowned`,
making `king(macbeth, scotland)` world-true.

Is this a new coupling kind? Assessment: No. Here's why.

The prophecy is a substrate-dialect record: `E_prophecy` with an
agent-knowledge-effect giving Macbeth a Held(prop =
`prophecy(macbeth, will_be_king)`, slot = KNOWN). That's a
substrate fact — the *content* is an upper-dialect-style claim
about the future, but the *record* is a substrate Held
proposition.

So the prophecy is *already* in the substrate. It does not
lower from the upper encoding because the upper encoding
doesn't contain a "prophecy" record — the Witches are a
Character, the prophecy-scene is a Scene, and the fact that
Macbeth becomes king is a consequence visible in the trajectory.

What the upper encoding does contain is the Argument
(`ambition unmakes`) which the prophecy's fulfillment helps
confirm. That connection is **Claim (trajectory)** — the
Argument's affirmation reads the prophecy-and-its-fulfillment
as part of the trajectory. Not a new kind.

**Verdict: Promissory is not a fifth coupling kind.** The
upper encoding doesn't contain promissory records; promissory
*content* lives in substrate agent-held propositions, and the
upper encoding's Argument couples to the unfolding via Claim
(trajectory).

### Negative coupling (missing or under-filled roles)

Oedipus surfaced an unfilled Antagonist slot. Macbeth surfaces
a contested Antagonist (multiple defensible readings). Is
"missing role" or "contested role" a coupling kind?

Assessment: No. The Antagonist slot being under-filled or
multiply-filled is handled by:

1. Dialect-level self-verification (M8.4 multiplicity check).
2. Template-level observation — "Antagonist slot has multiple
   plausible assignments; the Template's `exactly-one`
   multiplicity is violated by the multiple readings."

Neither requires a coupling to substrate. The "missing"
information is entirely within-dialect.

**Verdict: Negative coupling is not a fifth coupling kind.**
Structural absence is a within-dialect self-verification
concern, not a coupling to substrate.

### Provisional conclusion — the four kinds hold

No candidate fifth kind passed examination. The four kinds
(Realization / Characterization / Claim / Flavor) accommodate
every coupling case Macbeth raised, with the one refinement
that **Claim subdivides into moment-pattern and trajectory-
pattern forms**, and both need verifier primitives.

This refinement is not a new coupling kind — it is a
specialization of Claim into two sub-kinds differing in their
verifier-primitive requirements.

## Comparison with Oedipus

What from lowering-sketch-01 generalized, and what was Oedipus-
specific:

- **F1 (four coupling kinds).** Holds. Macbeth provides a
  second data point that no fifth kind is required.
- **F2 (heterogeneous Realization targets; queries go to the
  verifier).** Holds. Macbeth's realization cases are similarly
  heterogeneous (records, record sets, descriptions), and the
  Claim cases similarly require verifier checks.
- **F3 (coupling via description surface).** Holds. Macbeth's
  Stakes_macbeth_soul couples through a description
  (D_macbeth_conscience_before_murder or similar) rather than
  through typed facts.
- **F4 (position correspondence is author-declared).** Holds
  and strengthens. Macbeth's longer narrative with more Scenes
  makes position correspondence more load-bearing, and the
  intuition that it must be authored (not derived) is
  reinforced.
- **F5 (substrate gaps surface via lowering).** Holds — and
  this time the exercise is entirely about a substrate
  encoding that doesn't exist (`macbeth.py` is not written).
  The exercise could proceed because the substrate side was
  sketched in prose; a full implementation would require
  authoring the substrate.
- **F6 (Lowering and Verification are genuinely different
  relationships).** Holds, *and strengthens*. Macbeth makes
  Verification's trajectory-shape load-bearing. Oedipus's
  moment-shape Verification was sufficient for its cases; many
  of Macbeth's most important checks require trajectory-shape.
- **F7 (derivation composes with verification).** Holds and
  strengthens. Macbeth's kinslayer / regicide / breach_of_
  hospitality derivations are what make the Judgment=Bad
  trajectory-verifier tractable — otherwise the verifier has
  to check each killing's moral weight manually. With the
  derivations, the verifier reads the derived state and the
  trajectory is immediate.

**New finding specific to this exercise:**

- **F8 (new) — Claim coupling has two sub-kinds.** Claim at
  a moment (e.g., Outcome=Success) and Claim across a
  trajectory (e.g., Argument affirmation; Judgment=Bad in the
  Macbeth sense) are both Claim couplings but require
  different verifier primitives. A Verification sketch should
  separate moment-verifiers from trajectory-verifiers; the
  latter need to read substrate state across τ_s.

## Implications

1. **`lowering-record-sketch-01` is ready to draft** with
   confidence. The four-coupling-kinds framework held on two
   stories with different structural shapes; one more exercise
   would strengthen the base but is not strictly required.
   Lowering handles Realization only. The record shape is now
   concretely scoped.

2. **`verification-sketch-01` (as a sibling to the Lowering
   record sketch) needs to specify two primitive kinds of
   verifier**: moment-pattern (evaluate a substrate query at a
   specific τ_s) and trajectory-pattern (evaluate a signature
   over a range of τ_s). The two primitives are different in
   their query shape; they are not a labor-division of one
   concept.

3. **Dialect-level schema should declare coupling kind per
   record type.** An upper dialect's schema for each record
   type could declare which coupling kinds apply:
   `Character` → Realization. `DomainAssignment` →
   Characterization. `DynamicStoryPoint(outcome)` → Claim
   (moment). `Argument.resolution_direction` → Claim (trajectory).
   `Argument.domain` → Flavor. Making this declarative means
   both authors and verifiers know what to expect without
   deducing it case by case.

4. **Substrate encoding of Macbeth would be a useful prototype
   action** — both for completing the lowering exercise end-to-
   end (producing actual Lowering records rather than sketches)
   and for pressure-testing the substrate under a structurally
   different story. The existing Oedipus + Rashomon substrate
   encodings are both limited in ways Macbeth would extend
   (trajectory-heavy, moral rather than epistemic, multiple
   antagonist readings).

## What happens next

1. **Draft `lowering-record-sketch-01`.** The concrete record-
   shape sketch, informed by two exercises. Bounded scope:
   Realization couplings only. Seven requirements from
   lowering-sketch-01 plus the four-kinds clarification from
   this sketch's F1 generalization and F8 new finding.

2. **Draft `verification-sketch-01`** as a sibling. Owns
   Characterization and Claim couplings. Specifies moment-
   pattern and trajectory-pattern verifier primitives. Does
   not duplicate Lowering's record shape.

3. **Author `macbeth.py`** as a prototype substrate encoding.
   Parallels `oedipus.py` in shape; provides the concrete
   substrate for a complete Macbeth lowering exercise. Also
   gives the reader-model probe a second story to run against.

4. **Extend `oedipus.py`** (still on the upcoming list from
   lowering-sketch-01) to cover the cut plot beats. The Macbeth
   exercise reinforces that partial substrate encodings produce
   partial lowerings; the more complete the substrate, the
   more useful the exercise.

5. **Later — a third lowering exercise on a structurally
   *different* story.** Macbeth and Oedipus share being tragic
   trajectories. A comedy (A Midsummer Night's Dream?), an
   ensemble (The Great Gatsby? The Wire?), or a tonal / lyric
   piece (To the Lighthouse?) would stress-test the framework
   in a direction neither Oedipus nor Macbeth touched. This is
   well-deferred — one more exercise after the record sketches
   are drafted would show whether the framework held or needs
   revision.
