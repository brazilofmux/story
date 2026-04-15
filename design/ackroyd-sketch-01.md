# The Murder of Roger Ackroyd — encoding plan — sketch 01

**Status:** draft, active
**Date:** 2026-04-15
**Supersedes:** nothing (new encoding)
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md), [substrate-sketch-05.md](substrate-sketch-05.md)
**Superseded by:** nothing

## Purpose

Encoding plan for the third story the engine will cover, picked after
the two-tragedy base (Oedipus, Macbeth) left the architecture
empirically untested on non-tragic material. Per REVIEW.md's
next-term item #1, the third encoding should be *structurally
dissimilar* — not another revelation-and-collapse — so the dialect
assumptions and substrate machinery face material they weren't
implicitly designed around.

Agatha Christie's *The Murder of Roger Ackroyd* (1926) is the choice
because it stresses precisely the parts of the substrate that Oedipus
and Macbeth left quiet: **the disclosure layer and the unreliable-
narration frontier**. The substrate's sjuzhet + focalizer machinery
has been present since substrate-sketch-03 but has received only
light exercise. Ackroyd pressures it hard: the entire novel is
narrated by one of its characters, that narrator is also the
murderer, and the narrator's withholding — present throughout the
text — is not revealed until the closing chapters.

If the substrate can hold Ackroyd honestly, the substrate's
epistemic + narrative-disclosure machinery is doing real work. If it
cannot, this encoding will surface what needs to change.

This sketch is a plan, not the encoding itself. The encoding lands
across `prototype/ackroyd.py` (substrate), `prototype/
ackroyd_dramatic.py` + companion lowerings and verifier, and
`prototype/ackroyd_save_the_cat.py` + companion lowerings and
verifier. Each piece gets its own commit; this sketch anchors the
plan they'll follow.

## Why Ackroyd rather than another Christie

Christie wrote 66 detective novels. The three obvious alternatives:

- **Murder on the Orient Express (1934).** Twelve passengers, twelve
  stab wounds, a shared conspiracy. Stresses many-suspects
  bookkeeping and multi-agent knowledge but plays the narrator
  straight. Poirot is the sole perspective and reports honestly;
  the substrate's sjuzhet layer would get a mild workout.

- **And Then There Were None (1939).** Ten strangers on an island,
  all die, the killer is among them. No Poirot; no continuous
  narrator. Stresses identity-collapse (U.N. Owen = Unknown) and
  posthumous reveal. The closest analog to Oedipus's identity
  machinery, but less interesting for the *disclosure* layer
  (there's no single continuous narrator whose trustworthiness is
  at issue).

- **The Murder of Roger Ackroyd (1926).** Poirot's second novel;
  narrated throughout by Dr. James Sheppard, village doctor, who is
  *also the murderer*. The narrator's withholding is the load-
  bearing structural feature. The reader's `BELIEVED` set about
  what happened the night of the murder is deliberately constructed
  by the narrator to mislead — and the final reveal requires that
  set to be recontextualized.

Ackroyd wins on the criterion "stress the substrate features that
have been quietest." Its other advantages compound: the cast is
tight (single country house + village), the time span is compact
(~2 weeks), and the genre fit is clean (*Whydunit* in Save the Cat
terms). It's also canonical enough that the authoritative reading
is stable; the encoding doesn't have to take an interpretive side
on unsettled textual questions, the way *Hamlet* would.

## What Ackroyd will pressure

### The disclosure layer (substrate-sketch-03)

Every chapter of Ackroyd is filtered through Sheppard. The substrate
already has `Disclosure` and `SjuzhetEntry` records with `focalizer_id`
— but Macbeth's encoding uses `focalizer_id=None` on most events
(omniscient stage perspective), and Oedipus's uses specific
focalizers but on characters whose reports are reliable. Ackroyd
introduces a sustained dishonest focalizer.

The specific question this exposes: **does the current substrate
model distinguish `Sheppard BELIEVES X` (which is honest reporting
of his own mental state) from `Sheppard WRITES to the reader that X`
(which is performed narration aimed at the reader's `BELIEVED` set)?**
The two differ at exactly the Ackroyd-relevant points. When Sheppard
writes "I left Ackroyd alive at 8:50," his BELIEVED set contains
`ackroyd dead at 8:45` (he killed him); the narration is a
performative claim directed at the reader, not a report of his
belief.

Provisional answer: the substrate already admits this via `told_by`
with a reader-like recipient, but the convention hasn't been
exercised. If `told_by` isn't right for the reader-as-recipient case
(the reader isn't a substrate Entity), the encoding will surface
the need. Candidate substrate extensions:

- A `narrated_to_reader` effect kind distinct from `told_by`.
- A reader-frame `Entity` whose KNOWN/BELIEVED sets represent the
  reader's state across the sjuzhet.
- A `narrative_disclosure` record type parallel to `SjuzhetEntry`
  that carries the claim-being-narrated and its honesty flag.

The encoding will pick one; the pick becomes a data point for the
substrate's next iteration.

### Identity-as-role-stack

Sheppard holds multiple concurrent roles: village doctor (his day
job), narrator (the discourse layer), blackmailer of Mrs. Ferrars
(pre-murder), murderer of Ackroyd (the inciting event), keeper of
the suspect-diverting manuscript (post-murder). Oedipus's
identity-collapse machinery was designed for the case where one
Entity's identities are equated (shepherd = one-who-gave-child-away;
stranger = Laius; self = parricide + incest). Sheppard's case is
different: the identities are all simultaneously true from the
start; the question is which ones Sheppard *reveals* at each τ_d.

Provisional approach: encode Sheppard as one Entity with multiple
role facts, all true at the fabula layer from his first appearance.
The identity machinery proper (equivalence classes, gap_real_parents
analog) may not fire — and that non-firing is informative. If the
existing machinery doesn't help, a new record type (`RoleReveal`?)
may be warranted.

### Retroactive reveal / anagnorisis as a discourse-level event

In Oedipus, the anagnorisis is at the fabula layer: Oedipus *learns*
the truth at a specific event. The reader learns alongside him.
Ackroyd has an anagnorisis too — Poirot's deduction scene — but the
reader's anagnorisis is larger than Poirot's. The reader must
retroactively recontextualize *every earlier chapter*: what
Sheppard told them then was shaped to support a false conclusion.

The substrate's existing machinery handles Poirot's moment
(he forms new KNOWN facts, constructs a proof chain, presents to
the assembled cast). It does not yet have an explicit notion of
"the reader's prior BELIEVED facts are now to be re-read." This is
a genuine substrate gap and the encoding will surface it.

Provisional approach: encode Poirot's fabula-layer anagnorisis in
the usual way; encode the reader's discourse-layer anagnorisis as a
sjuzhet-level observation (perhaps a `NarrativeReveal` record, or
annotation on the final SjuzhetEntry). If neither fits, document
the gap and defer.

### Genre fit on Save the Cat

Ackroyd is a classic **Whydunit** in Save the Cat's typology — one
of the ten genres the dialect ships. The archetypes
("the detective", "the secret", "the dark turn") map cleanly:

- **the detective** → Poirot (with Sheppard as nominally-assisting
  narrator, a dark twist on the usual Watson role)
- **the secret** → Ackroyd's killer is the man telling you the
  story; the blackmail of Mrs. Ferrars; the dictaphone alibi
- **the dark turn** → Poirot's quiet "either you confess or I take
  it to the police tomorrow" ending, and Sheppard's implied
  suicide

Unlike Macbeth (where Rites of Passage was the least-bad fit but
strained against pre-modern tragedy), Ackroyd and Whydunit were
nearly designed for each other. The Save the Cat encoding will
probably produce a very clean verifier output — which is itself
informative: *the dialect's advertised fit for its native genre is
real*.

### Character / function mapping in Dramatic

Dramatica role assignments will be interesting:

- **Protagonist** → Poirot (he pursues the story goal: solve the
  murder)
- **Antagonist** → Sheppard (he opposes the goal: obscures
  evidence, misdirects the investigation, is the killer)
- **Main Character** — the *narrator* is usually the MC in
  detective fiction, but here the narrator is also the Antagonist.
  Dramatica admits double-function characters (Macbeth is
  Protagonist + Emotion). Sheppard as Antagonist + Main Character
  would be the encoding's structural thesis.
- **Impact Character** → Poirot (the force that moves the MC
  toward change — here, toward confession). A standard inversion
  of "MC = hero, IC = antagonist": in Ackroyd, **MC = villain, IC =
  hero**.
- **Reason / Emotion / Sidekick / Skeptic / Guardian / Contagonist**
  fills out with the village cast (Caroline Sheppard, Flora
  Ackroyd, Ralph Paton, Major Blunt, Inspector Raglan, Ursula
  Bourne). The exact assignments are an authorial choice the
  encoding will make explicit and defend.

The MC-is-also-Antagonist encoding is the Dramatic dialect's first
test on material where the Dramatica role-stack inverts. Dramatica
theory admits it; the encoding will exercise it.

## Cast (provisional)

Expected substrate Entities:

- `poirot` — retired, growing vegetable marrows; called in by Flora
- `sheppard` — narrator, village doctor, blackmailer, murderer
- `caroline_sheppard` — his sister; knows everything before anyone
- `ackroyd` — the victim; wealthy widower
- `mrs_ferrars` — widow, suicide (τ_s ≈ -1); poisoned her husband,
  was being blackmailed
- `mr_ferrars` — pre-dead (τ_s well before 0, poisoned)
- `ralph_paton` — stepson, fiance of Flora, main red herring
- `flora_ackroyd` — Roger's niece, engaged to Ralph
- `geoffrey_raymond` — Roger's secretary
- `major_blunt` — big-game hunter friend
- `mrs_cecil_ackroyd` — Roger's sister-in-law
- `ursula_bourne` — parlormaid (secretly married to Ralph)
- `parker` — butler
- `inspector_raglan` — local police
- `hammond` — Roger's solicitor

Fifteen Entities — roughly Macbeth's scale. A smaller cut might be
viable if the encoding gets unwieldy; `mrs_cecil_ackroyd` and
`hammond` can be dropped with minimal plot damage.

## Fabula skeleton (provisional)

τ_s anchor: τ_s=0 at the first chapter's opening (Mrs. Ferrars'
death discovered by Sheppard at breakfast). Pre-play facts
(marriages, deaths of prior spouses, Sheppard's blackmail campaign
against Mrs. Ferrars) get negative τ_s.

Expected events (15-20):

- Pre-play: Ferrars poisoning, Sheppard's blackmail, Flora-Ralph
  engagement.
- τ_s=0: Mrs. Ferrars' suicide discovered.
- τ_s=1: Sheppard dines with Ackroyd; Ackroyd receives Mrs. Ferrars'
  letter; **Sheppard murders Ackroyd** (the inciting event); dictaphone
  alibi set up.
- τ_s=2: Body discovered; Ralph's absence noted; Poirot summoned by
  Flora.
- τ_s=3..N: The investigation — Poirot questions each suspect;
  parallel red herrings (Ralph's affair with Ursula, Parker's
  attempted blackmail, Flora's theft of £40); gradual narrowing.
- τ_s=N-1: Poirot gathers the cast; lays out the solution.
- τ_s=N: Poirot's private confrontation with Sheppard; ultimatum.
  Sheppard's implied suicide is off-page; the novel's final
  chapter is his confession manuscript.

The murder at τ_s=1 is the fabula's structural inciting event;
its *narrated position* (what Sheppard tells us) is the hole in
the text.

## Expected verifier surface

If the substrate holds Ackroyd honestly:

- **Poirot's anagnorisis** lands as a claim-moment check at the
  confrontation — parallel to Oedipus's S_anagnorisis check and
  Macbeth's S_macbeth_dies check.
- **Sheppard's narration-vs-belief divergence** needs either a new
  check primitive or a carefully-scoped sjuzhet-level check.
  This is the encoding's most interesting verifier-side question.
- **Save the Cat's Whydunit genre archetypes** (detective, secret,
  dark turn) can be verified as characterization checks if
  StcGenre acquires Lowerings to substrate patterns. Previously
  deferred; Ackroyd forces the issue.

## Open questions

- **Do we extend the substrate before or during the encoding?**
  Preference: encode first, let the gaps surface, extend afterward.
  The substrate extension (if any) becomes substrate-sketch-06 with
  Ackroyd-encoded evidence rather than speculative design.

- **Reader-as-Entity or reader-as-frame?** If Ackroyd's narrator-
  reader relationship needs substrate representation, is the
  reader a substrate Entity (extending ENTITIES with a synthetic
  entity) or a frame outside the substrate's ontology? Authorial
  preference is the latter; the encoding may argue otherwise.

- **How far to push the Save the Cat Character gap?** The cross-
  dialect comparison sketch flagged Save the Cat's lack of a
  Character record as jarring on Macbeth. Ackroyd is even more
  character-dense; the gap will be more visible. Does Ackroyd
  force an `StcCharacter` amendment to save-the-cat-sketch-01, or
  does it confirm the dialect is correctly narrow and characters
  belong entirely substrate-side? The encoding's authorial
  experience is the deciding data.

- **Dramatica role-stack inversion.** MC + Antagonist on one
  Character is theoretically admitted; is the verifier machinery
  ready for it? The existing `main-character throughline
  characterization` check in verifier_helpers.py assumes the MC's
  owner Character is in the lowered events; that holds for
  Sheppard (he's in every event, as narrator and participant). But
  a future check asking "is the Antagonist opposing the story
  goal?" against the substrate will need to handle MC+Antagonist
  without double-counting.

## Session plan

Four sessions expected, one commit each:

1. **This sketch.** (You are here.) Frames the multi-session work;
   user pushback lands here before heavy coding.
2. **Substrate encoding** (`ackroyd.py`): Entities, Fabula,
   Disclosures, Sjuzhet, any Rules. The biggest single piece.
3. **Dramatic encoding** (`ackroyd_dramatic.py`, `ackroyd_
   lowerings.py`, `ackroyd_verification.py`).
4. **Save the Cat encoding** (`ackroyd_save_the_cat.py`, lowerings,
   verification). Plus a cross-dialect comparison sketch
   (`cross-dialect-ackroyd-sketch-01.md`) parallel to the Macbeth
   one.

If intermediate findings force a substrate extension
(substrate-sketch-06), that gets its own session between (2) and
(3) — don't let substrate work hide in an encoding commit.

## What this sketch is not

- Not a defense of Christie as canonical. Other mysteries would
  work; Ackroyd has the sharpest features for stressing the
  substrate.
- Not a commitment to every detail above. The cast list and fabula
  skeleton will be adjusted during encoding; this sketch is a plan,
  not a spec.
- Not a research survey of detective fiction. The Christie + Poirot
  frame is one tradition within the broader mystery genre; the
  engine's ability to handle other traditions (hard-boiled,
  procedural, cozy, non-Western) remains open after Ackroyd.
