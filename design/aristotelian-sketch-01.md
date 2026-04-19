# Aristotelian dialect — sketch 01

**Status:** draft, active
**Date:** 2026-04-18
**Supersedes:** nothing
**Frames:** [architecture-sketch-02](architecture-sketch-02.md)
(the dialect stack), [dramatic-sketch-01](dramatic-sketch-01.md)
(upper-dialect pattern), [save-the-cat-sketch-01](save-the-cat-
sketch-01.md) + [sketch-02](save-the-cat-sketch-02.md) (non-
Dramatica dialect precedent)
**Related:** [dramatica-template-sketch-01](dramatica-template-
sketch-01.md) (depth-probe sibling), [lowering-record-sketch-01](
lowering-record-sketch-01.md), [verification-sketch-01](
verification-sketch-01.md); `prototype/story_engine/encodings/
oedipus.py` (worked-case substrate)
**Superseded by:** nothing yet

## Purpose

Third upper-dialect sketch under architecture-sketch-02's dialect
stack — and **the first that is a deliberate falsifiable test of
the architecture itself**. Aristotle's *Poetics* predates Dramatica
by ~2400 years and was written describing a specific theatrical
tradition (5th-century BCE Athenian tragedy) rather than a general
theory of story. If the architecture's claim — that Dramatica is
one Template among many and the dialect stack admits theoretically
distinct frames by clean extension — is right, an Aristotelian
dialect lands with no core-record modification, on the pattern
Save-the-Cat set (sketch-01 landed the Template; sketch-02 added
`StcCharacter` as a clean extension, not a modification).

The shift-point question (state-of-play-03's research-to-
production framing; memory `project_longterm_roadmap`): is the
substrate / dialect stack stable enough that the Python code is
ready to be treated as a spec? The architecture has gone ~N probe
cycles without substrate or dialect-record modification — a
stability signal. This sketch tests whether the signal is real or
whether we've stopped stressing the architecture.

**Methodology.** The sketch IS the test. Each commitment A1–A9 is
evaluated for what it requires of the architecture:

- *Extension* — new Template-level records; new verifier-local
  checks over existing substrate; new annotations. Clean; the
  architecture holds.
- *Modification* — adds a field to a core record (Event,
  Throughline, Scene, Beat, Lowering, Description, Entity, Fact);
  changes an existing primitive's semantics; requires a new
  substrate effect kind. The architecture's core is not yet
  stable; shift point is further out.

If every commitment is extension-only, the sketch lands and
implementation follows. If any commitment forces modification, we
stop at that commitment and re-open the architectural question it
raises.

## Why now

- state-of-play-03's maybe-next-5 item named non-Dramatica
  Templates (Freytag / Aristotelian / author-defined) as
  architecturally meaningful.
- No substrate- or dialect-record change has landed since
  substrate-sketch-05 / dramatic-sketch-01 / lowering-record-sketch-
  01 / dramatica-template-sketch-01. Recent churn has been verifier-
  local vocabulary (LT2 → LT12/LT13/LT14, LT8 → SC2), author
  discipline (SC1, TL3), and per-encoding content. The architecture
  *looks* stable. This sketch tests whether it *is* stable.
- Freytag was the other candidate. Rejected for this test: the
  five-phase pyramid is so mechanical it would slot in trivially
  and wouldn't stress the architecture. Aristotelian brings
  structural primitives (unity of action), character primitives
  (hamartia — deliberately overlapping with Dramatica Main Character
  concerns), plot devices (peripeteia / anagnorisis — potentially
  requiring reversal semantics the substrate does not carry), and
  an audience-effect primitive (catharsis — potentially requiring
  reader-response machinery). Each is a potential stress point.

## Scope — what the sketch covers

In: structural primitives (unity of action; beginning/middle/end);
plot devices (peripeteia, anagnorisis; simple vs complex plot);
character primitives (hamartia); the three unities, differentiated
as Aristotelian-vs-neoclassical; the self-verifier pattern within
Aristotelian vocabulary.

Out: cross-dialect lowering (Aristotelian ↔ Dramatic ↔ substrate)
per architecture-sketch-02 A8 (separate sketch when a concrete
encoding lands); the four qualities of character (good,
appropriate, lifelike, consistent) as verifiable claims; dianoia
(thought/argument) as a dialect primitive; comedy / satyr play
genres (tragedy shape is this sketch's scope); lexis / melos /
opsis (production-layer, below substrate).

## Commitments

### A1 — The plot is the sketch's primary record

Aristotle: *"the arrangement of the incidents"* (mythos) is the
soul of tragedy. Not character, not language, not spectacle. The
Aristotelian dialect's primary record is `ArMythos`:

```python
@dataclass(frozen=True)
class ArMythos:
    id: str
    title: str
    action_summary: str
    central_event_ids: Tuple[str, ...]   # substrate event refs
    plot_kind: str                        # "simple" | "complex"
    phases: Tuple["ArPhase", ...]         # (beginning, middle, end)
    complication_event_id: Optional[str] = None
    denouement_event_id: Optional[str] = None
    peripeteia_event_id: Optional[str] = None
    anagnorisis_event_id: Optional[str] = None
    asserts_unity_of_action: bool = True
    asserts_unity_of_time: bool = False
    asserts_unity_of_place: bool = False
    aims_at_catharsis: bool = True
    characters: Tuple["ArCharacter", ...] = ()
```

**Architectural classification: extension.** New Template-level
record type in a new dialect module `aristotelian.py`. References
substrate events by id (exactly as Dramatica's `Signpost.anchor_
event_ids` does). No core-record modification.

### A2 — Three phases, logical not temporal

Beginning, middle, end are *logical* divisions of the action —
connected by necessity or probability — not equal-page-target
beats (contrast Save-the-Cat's S2 page-target discipline).

```python
@dataclass(frozen=True)
class ArPhase:
    id: str
    role: str                    # "beginning" | "middle" | "end"
    scope_event_ids: Tuple[str, ...]
    annotation: str = ""
```

**Architectural classification: extension.** New Template record;
references substrate events.

### A3 — Simple vs complex plot

Aristotle distinguishes **simple plots** (a single change of
fortune, no peripeteia / no anagnorisis) from **complex plots** (a
change of fortune involving peripeteia, anagnorisis, or both).
Tragedy's highest form is complex; not all tragedies are.

`ArMythos.plot_kind` is one of `"simple"` or `"complex"`. If
`"complex"`, at least one of `peripeteia_event_id` /
`anagnorisis_event_id` MUST be non-None. The self-verifier (A7)
checks this.

**Architectural classification: extension.** ArMythos field +
self-verifier rule. No core modification.

### A4 — Peripeteia and anagnorisis are interpretive pointers

**Peripeteia**: the event where fortune reverses direction —
*"a change from one state of affairs to its opposite"* (Poetics
1452a).

**Anagnorisis**: the event where a character moves from ignorance
to knowledge — *"a change from ignorance to knowledge"* (ibid.).

Both are represented as **substrate event ids on ArMythos** (A1),
not as independent records in v1. The **reversal** and
**recognition** claims are interpretive — the event structurally
exists in the substrate; the interpretive claim that the event
reverses fortune / realizes recognition lives in ArMythos's
pointer plus a prose annotation.

**Stress point acknowledged:** substrate **does not carry fortune-
state**. substrate-sketch-05 retired F1 (emotion/tension as
parallel projection) explicitly — interpretive content lives in
Descriptions, not in substrate facts. The "peripeteia reverses
fortune" claim is therefore purely interpretive, consistent with
grid-snap discipline. This is **not a modification** — it's what
the architecture was built to admit.

**Anagnorisis is closer to structural**: the substrate's identity-
and-realization machinery (identity-and-realization-sketch-01)
carries knowledge-state transitions — `realized(id, believer, at)`
is already a substrate predicate. An anagnorisis event IS a
substrate-visible realization event; the Aristotelian dialect
simply picks out the critical one.

**Architectural classification: extension.** ArMythos fields
referencing substrate events. No core modification. Substrate
already carries realization primitives.

### A5 — Hamartia is a character-level attribute

Aristotle: the tragic hero falls through **hamartia** — *"missing
the mark"* (Poetics 1453a). Not a moral flaw (Bradley's Victorian
reading); an error in judgment or action, typically arising from
ignorance of some fact the hero could not reasonably know.

```python
@dataclass(frozen=True)
class ArCharacter:
    id: str
    name: str
    character_ref_id: Optional[str] = None   # substrate Entity or
                                             # Dramatic Character id
    hamartia_text: Optional[str] = None
    is_tragic_hero: bool = False
```

`character_ref_id` is the cross-dialect identity hook. Aristotelian
does not duplicate character modeling; it points at an existing
Entity (substrate) or Character (Dramatic) record when one exists.
When the Aristotelian encoding stands alone (no Dramatic layer
authored), the ref is None and the Aristotelian dialect carries
the character on its own.

**Architectural classification: extension.** New Template record
with optional cross-dialect ref. **Notable**: this is the same
pattern Save-the-Cat's StcCharacter followed (sketch-02 S9–S11)
and the cross-dialect alignment is explicitly architecture-sketch-
02 A8's concern (out-of-scope for this sketch).

The overlap with Dramatica Main Character's "problem" is real but
NOT a stress point: different dialects express the same content
differently; cross-dialect Lowering handles the alignment when an
encoding wants both dialects active.

### A6 — Three unities, differentiated

Aristotle explicitly argues for **unity of action** (Poetics
1451a). He mentions tragedy "endeavoring to keep within a single
revolution of the sun" as a *tendency*, not a rule. **Unity of
place** is a Renaissance-neoclassical addition (Castelvetro 1570)
— not Aristotelian.

```python
ArMythos.asserts_unity_of_action: bool = True   # Aristotelian
ArMythos.asserts_unity_of_time:   bool = False  # opt-in, neoclassical-leaning
ArMythos.asserts_unity_of_place:  bool = False  # opt-in, strictly neoclassical
```

Self-verifier checks (A7):

- **Unity of action (always checked):** every `central_event_ids`
  event appears in exactly one `phases[k].scope_event_ids`; the
  union of phase scopes equals `central_event_ids` as a set.
- **Unity of time (only if asserted):** `max(τ_s) - min(τ_s)` over
  `central_event_ids` ≤ a configurable bound (default 24 — the
  unit is encoding-defined; the verifier passes the bound as a
  parameter).
- **Unity of place (only if asserted):** every
  `central_event_ids` event has at most one `at_location` effect,
  and the set of locations across all central events has cardinality
  ≤ a configurable bound (default 1).

**Architectural classification: extension.** Verifier-local checks
over existing substrate predicates (`τ_s`, `at_location`). No new
substrate record types. `at_location` already exists as a world-
state predicate (used in Rashomon's `E_lure`, for example —
`world(at_location("husband", "grove"))`).

### A7 — Self-verifier within Aristotelian vocabulary

Mirrors Save-the-Cat's S6 and Dramatic's M8. Runs on Aristotelian
records only — no substrate reading except through the explicit
event-id refs and the unity-of-time / unity-of-place checks.

Checks:

1. **A3 consistency:** if `plot_kind == "complex"`, at least one
   of `peripeteia_event_id` / `anagnorisis_event_id` is non-None.
2. **A6 unity of action:** phase scope coverage (as above).
3. **A6 unity of time / place:** conditional on assertion.
4. **Event-ref integrity:** every event id in `central_event_ids`,
   phase scopes, `complication_event_id`, `denouement_event_id`,
   `peripeteia_event_id`, `anagnorisis_event_id` resolves to a
   substrate event in the encoding.
5. **Hamartia participation:** if an `ArCharacter` carries
   `hamartia_text` and is flagged `is_tragic_hero=True`, the
   referenced substrate Entity (via `character_ref_id`) must
   participate in at least one `central_event_ids` event. (If
   `character_ref_id` is None, skip — self-contained Aristotelian
   encoding.)

**Architectural classification: extension.** Dialect-local verifier
pass. Mirrors the Save-the-Cat self-verifier pattern (save-the-cat-
sketch-01 S6). Produces advisories / VerificationReviews via the
existing verification-sketch-01 record surface.

### A8 — Catharsis, pity, and fear are authorial claims

Audience emotional effect. The substrate does not model reader /
audience response — by design. descriptions-sketch-01 keeps
affective content on the Description surface; reader-model-sketch-
01 models what readers *know* (inference), not what they *feel*.

The Aristotelian dialect treats catharsis as an authorial claim:
`ArMythos.aims_at_catharsis: bool = True`. Pity/fear descriptions
on specific events live on the existing `Description` surface
(descriptions-sketch-01) with author-chosen kind strings —
e.g., `kind="aristotelian-pity"`, `kind="aristotelian-fear"`. The
self-verifier does not check catharsis achievement; it records the
claim.

**Architectural classification: extension.** Record field plus
Description conventions. No new record type for audience-response
semantics. **OQ2:** should the Aristotelian dialect ship typed
`ArAffect(kind, about_event_id, text)` records, or is free-form
Description sufficient? Defer to sketch-02.

### A9 — Cross-dialect connective machinery is out of scope

Per architecture-sketch-02 A8 and save-the-cat-sketch-01 S8. A
Lowering between Aristotelian records and Dramatic or substrate
records is separate work (`lowering-sketch-04` or per-encoding
`_aristotelian_lowerings.py` once a concrete encoding lands). The
cross-dialect character-identity alignment via `character_ref_id`
(A5) is a hint, not a committed cross-dialect check.

**Architectural classification: scoping commitment.** No code.

## Worked example — Oedipus Tyrannus under A1–A9

Oedipus is Aristotle's worked example in the *Poetics*. If the
sketch cannot encode Oedipus in Aristotelian terms, the sketch
fails its own test. The substrate encoding exists at
`prototype/story_engine/encodings/oedipus.py`; event ids below
are real.

```python
AR_OEDIPUS_MYTHOS = ArMythos(
    id="ar_oedipus",
    title="Oedipus Tyrannus",
    action_summary=(
        "A king, investigating a plague sent to punish his city's "
        "unpurged blood-guilt, discovers through a chain of "
        "witnesses that he himself is the murderer of his "
        "predecessor — and the son of his wife. Recognition "
        "coincides with reversal; catastrophe follows."
    ),
    plot_kind="complex",
    central_event_ids=(
        "E_birth",
        "E_exposure_and_rescue",
        "E_upbringing_in_corinth",
        "E_oracle_to_oedipus",
        "E_crossroads_killing",
        "E_marriage_and_crown",
        "E_tiresias_accusation",
        "E_jocasta_mentions_crossroads",
        "E_messenger_polybus_dead",
        "E_messenger_adoption_reveal",
        "E_jocasta_realizes",
        "E_shepherd_testimony",
        "E_oedipus_anagnorisis",
        "E_jocasta_suicide",
        "E_self_blinding",
        "E_exile",
    ),
    phases=(
        ArPhase(
            id="ph_beginning", role="beginning",
            scope_event_ids=(
                "E_birth", "E_exposure_and_rescue",
                "E_upbringing_in_corinth", "E_oracle_to_oedipus",
                "E_crossroads_killing", "E_marriage_and_crown",
            ),
            annotation=(
                "Antecedent action, dramatically compressed into "
                "narrative exposition. Oedipus's identity and guilt "
                "are structurally complete before the play opens."
            ),
        ),
        ArPhase(
            id="ph_middle", role="middle",
            scope_event_ids=(
                "E_tiresias_accusation",
                "E_jocasta_mentions_crossroads",
                "E_messenger_polybus_dead",
                "E_messenger_adoption_reveal",
                "E_jocasta_realizes", "E_shepherd_testimony",
            ),
            annotation=(
                "The investigation — ties binding. Each testimony "
                "narrows identity. Middle ends with the last piece "
                "of evidence the shepherd provides."
            ),
        ),
        ArPhase(
            id="ph_end", role="end",
            scope_event_ids=(
                "E_oedipus_anagnorisis", "E_jocasta_suicide",
                "E_self_blinding", "E_exile",
            ),
            annotation=(
                "Ties unbinding. Recognition, Jocasta's suicide, "
                "self-blinding, exile — the consequences follow "
                "from recognition by necessity."
            ),
        ),
    ),
    complication_event_id="E_tiresias_accusation",
    denouement_event_id="E_shepherd_testimony",
    peripeteia_event_id="E_messenger_adoption_reveal",
    anagnorisis_event_id="E_oedipus_anagnorisis",
    asserts_unity_of_action=True,
    asserts_unity_of_time=False,
    asserts_unity_of_place=False,
    aims_at_catharsis=True,
    characters=(
        ArCharacter(
            id="ar_oedipus", name="Oedipus",
            character_ref_id="oedipus",       # substrate Entity id
            hamartia_text=(
                "The investigator's virtue — pursuing truth to save "
                "the city — is the mechanism of his destruction. "
                "Hamartia is not a moral flaw but a missing-the-mark: "
                "ignorance of identity driving action that fulfills "
                "the prophecy he thought he was fleeing."
            ),
            is_tragic_hero=True,
        ),
        ArCharacter(
            id="ar_jocasta", name="Jocasta",
            character_ref_id="jocasta",
            hamartia_text=(
                "Parallel hamartia — ignorance of identity; her "
                "suicide at recognition mirrors Oedipus's blinding."
            ),
            is_tragic_hero=False,
        ),
    ),
)
```

**Note on peripeteia placement.** Aristotle (Poetics 1452a) names
Oedipus specifically: *"the messenger who came to cheer Oedipus
and free him from his fears about his mother, by revealing his
origin, produced the opposite effect."* The peripeteia lives at
the messenger's adoption-reveal event, not at the anagnorisis
itself — though in Oedipus, Aristotle notes, reversal and
recognition **coincide in effect** even if structurally adjacent.
`peripeteia_event_id` = `E_messenger_adoption_reveal` captures
this.

**Unity-of-time decision.** `False`. The *action* Oedipus dramatizes
onstage is compressed (a single day, roughly), but the *central
action* the Aristotelian mythos tracks spans from Oedipus's birth
through his exile — years of elapsed world time. Unity-of-time in
Aristotle's sketchy sense would apply to the dramatic present only;
the mythos record names the broader action. This is an intentional
design choice, not a dialect limitation — authors may set
`asserts_unity_of_time=True` with a tight bound if they want the
dramatic-present check.

## Stress case — Rashomon under A1–A9

Oedipus is the example Aristotle built the theory from. If the
sketch cannot encode Oedipus, it fails trivially. A fair stability
test needs at least one case that could *resist* Aristotelian
encoding. Rashomon is that case: Dramatica's multi-Story machinery
(multi-story-sketch-01) handles it natively; does the Aristotelian
dialect?

### What the Rashomon substrate actually provides

Rashomon's substrate (`prototype/story_engine/encodings/rashomon.py`)
contains 22 events, partitioned:

- **Canonical-floor** (8 events, no branch): `E_travel`,
  `E_tajomaru_sees_them`, `E_lure`, `E_bind`, `E_bring_wife`,
  `E_intercourse`, `E_husband_dead`, `E_body_found`.
- **B_TAJOMARU branch** (3 events): `E_t_wife_requests_killing`,
  `E_t_frees_husband`, `E_t_duel`.
- **B_WIFE branch** (2 events): `E_w_tajomaru_leaves`,
  `E_w_killing`.
- **B_HUSBAND branch** (5 events): `E_h_wife_requests_killing`,
  `E_h_tajomaru_refuses`, `E_h_wife_flees`, `E_h_frees_husband`,
  `E_h_suicide`.
- **B_WOODCUTTER branch** (4 events): `E_wc_wife_goads`,
  `E_wc_fight`, `E_wc_wife_flees`, `E_wc_theft`.

**The frame is absent from substrate.** Gate, rainstorm, priest,
commoner, baby — all exist only at the Dramatic dialect layer
(state-of-play-02/03: "S_frame carries full Dramatica-8
declarations but no ACTIVE Lowerings — grove-only substrate
scope"). An Aristotelian encoding bound to substrate has no
frame material to draw on.

### The encoding decision

Four paths considered:

1. **Frame-as-mythos** — encode the priest's crisis-and-partial-
   recovery as the mythos. **Rejected:** substrate carries no
   frame events; nothing to bind.
2. **Canonical-floor-only mythos** — one ArMythos over the 8
   undisputed events. **Rejected** as dishonest: 14 of Rashomon's
   22 substrate events are testimony-branch; a mythos that
   excludes 64% of the substrate is not a good-faith encoding of
   the work.
3. **Dialect-scope refusal** — the self-verifier returns "cannot
   coherently encode under A1–A9." Defensible but unhelpful. Also
   false: each testimony IS a coherent Aristotelian arc in
   isolation.
4. **Multi-mythos encoding** — author four `ArMythos` records,
   one per testimony, sharing canonical-floor events as common
   beginning material and diverging in middle/end over each
   testimony's branch events.

Path 4 is taken. Nothing in A1–A9 forbids multiple `ArMythos`
records in one encoding — `central_event_ids` overlap is permitted;
the self-verifier runs per-mythos.

### Worked four-mythos encoding (skeletal)

Four `ArMythos` records, each complex plot, each sharing the
canonical-floor events E_travel … E_intercourse as a common
beginning phase:

```python
AR_RASHOMON_MYTHOI = (
    ArMythos(
        id="ar_rashomon_bandit",
        title="Rashomon — Tajōmaru's account",
        action_summary=(
            "A bandit seduces a samurai's wife, then — at her "
            "request — kills the samurai in honorable combat."
        ),
        plot_kind="complex",
        central_event_ids=(
            "E_travel", "E_tajomaru_sees_them", "E_lure", "E_bind",
            "E_bring_wife", "E_intercourse",
            "E_t_wife_requests_killing", "E_t_frees_husband",
            "E_t_duel", "E_husband_dead",
        ),
        phases=(
            ArPhase(id="ph_b_beg", role="beginning", scope_event_ids=(
                "E_travel", "E_tajomaru_sees_them", "E_lure", "E_bind",
                "E_bring_wife", "E_intercourse",
            )),
            ArPhase(id="ph_b_mid", role="middle", scope_event_ids=(
                "E_t_wife_requests_killing", "E_t_frees_husband",
            )),
            ArPhase(id="ph_b_end", role="end", scope_event_ids=(
                "E_t_duel", "E_husband_dead",
            )),
        ),
        peripeteia_event_id="E_t_wife_requests_killing",
        anagnorisis_event_id=None,
        asserts_unity_of_action=True,
        asserts_unity_of_time=True,   # single day in the grove
        asserts_unity_of_place=True,  # the grove
        aims_at_catharsis=False,      # Tajōmaru's account is boastful
        characters=(
            ArCharacter(id="ar_b_tajomaru", name="Tajōmaru",
                        character_ref_id="tajomaru",
                        hamartia_text="Overweening confidence in his own prowess.",
                        is_tragic_hero=True),
        ),
    ),
    # ... three sibling ArMythos for wife / samurai / woodcutter
    # testimonies, each with its own peripeteia, hamartia, unities.
)
```

Each testimony-mythos:

- **Unity of action:** holds within the testimony's own scope.
- **Unity of time / place:** all four testimonies assert both
  (single day; the grove). Substrate's `at_location("husband",
  "grove")` predicate supports the check.
- **Peripeteia:** each testimony's "requested killing" event
  (the wife's speech act) serves as the reversal — the moment
  the fortune-direction tips toward death.
- **Anagnorisis:** none of the testifiers experience recognition
  within their own account. Each testimony is a self-serving
  narrative without character-level revelation. `anagnorisis_
  event_id = None` for all four; `plot_kind = "complex"` survives
  because peripeteia alone qualifies under A3 ("at least one of
  peripeteia / anagnorisis").
- **Hamartia:** per-testimony, different claim per testifier
  about whose error.

### What stretches (and what doesn't)

Three stress points surface:

1. **Plurality of mythoi.** The sketch's prose framing (A1: "the
   Aristotelian dialect's primary record is ArMythos") *reads* as
   one-mythos-per-encoding, but no commitment actually restricts
   the count. A tuple of `ArMythos` records encodes Rashomon
   without sketch modification. **Architecturally: no break.**
   Clarification worth adding to A1 (acceptance sub-criterion
   AA1').

2. **Meta-anagnorisis.** The Dramatic-layer frame delivers the
   work's most important recognition — the priest / audience
   realizing no testimony is fully true, the woodcutter's
   confession of theft. This is *meta-level*: the reader / audience
   recognizes, not a character within a mythos. **Aristotle's
   anagnorisis is character-level only.** The Aristotelian dialect
   therefore cannot express Rashomon's most important move.
   **Architecturally: not a break.** This is a *dialect-scope
   limit* in the same class as A8's catharsis-as-authorial-claim.
   Aristotelian captures what it captures; meta-anagnorisis lives
   outside its vocabulary, captured (by default) in Descriptions
   or by a Dramatica encoding of the same work alongside.

3. **Contested relations between mythoi.** The four testimony
   mythoi are not independent — they contest the same canonical-
   floor events. Dramatic's multi-Story dialect expresses this
   with `StoryRelation(kind="contains"/"parallel-to")`. Aristotelian
   has no equivalent. Options:
   - Live with it — each mythos is a standalone arc; the contest
     is encoded in Descriptions and in Dramatica-layer StoryRelations.
   - Sketch-02 extension: `ArMythosRelation(kind="contests",
     a_mythos_id, b_mythos_id, over_event_ids=...)`. **Dialect-
     level extension, not core modification.**

   Sketch-01 takes the first option. Adding a relation record is
   a sketch-02 concern if a forcing function appears.

### Stress-case verdict

Rashomon encodes under A1–A9 as a multi-mythos tuple. One dialect-
scope limit is acknowledged (meta-anagnorisis) — not a break, of
the same kind as the catharsis scope-out in A8. One potential
extension is flagged (`ArMythosRelation`) but not forced. **No
core-record modification required; no substrate change; no new
effect kind.**

This is a weaker result than Oedipus (where the dialect fits
natively) but not a break: the dialect has honest limits, and the
limits are sized by the theory itself, not by the architecture.
Aristotle did not claim his *Poetics* covered every story-shape;
he claimed it covered tragedy.

---

## Architectural judgment

**Every commitment A1–A9 is extension-only. No core-record
modification. No new substrate primitive. No new effect kind.**

Specific stress points that could have broken the architecture and
did not:

1. **Peripeteia's reversal semantics.** Architecture requires
   fortune-state to BE interpretive (grid-snap, substrate-sketch-
   05 F1-retirement). Aristotelian peripeteia represented as
   interpretive pointer. **Holds.**
2. **Anagnorisis.** Required a knowledge-state transition record.
   Substrate already had it (identity-and-realization-sketch-01).
   **Holds.**
3. **Hamartia.** Required per-character attributes overlapping
   with Dramatica Main Character. Solved by new `ArCharacter`
   record + `character_ref_id` cross-dialect hook, same pattern as
   Save-the-Cat. **Holds.**
4. **Unity of time / place.** Required substrate to carry position
   and location. Substrate carries both (`τ_s`; `at_location`
   predicate). Verifier pass is local. **Holds.**
5. **Catharsis / pity / fear.** Required audience-response
   modeling. Architecture explicitly scopes audience response out
   (descriptions + author-claim suffice). **Holds** — by
   acknowledging an architectural limit rather than stretching.

**Rashomon stress case confirms:** multi-mythos encoding slots in
without modifying A1–A9. One dialect-scope limit surfaces (meta-
anagnorisis, same class as catharsis A8), one extension flagged
(`ArMythosRelation`) and not forced. Core architecture unchanged.

**Conclusion of the design phase of the test: GREEN, with one
honest qualification.** The architecture admits Aristotelian
poetics by clean extension, including under deliberate stress from
a work Aristotle's theory does not natively cover. The substrate /
dialect stack is stable in the sense that architecture-sketch-02
claimed.

The qualification: the stress case (Rashomon) surfaces **dialect-
scope limits** that the architecture does not hide. Meta-
anagnorisis is genuinely outside Aristotelian vocabulary; the
architecture lets us say so cleanly rather than forcing the
dialect to stretch. That is the *correct* behavior of a well-
designed dialect stack — each dialect has a scope, and the
architecture doesn't paper over it.

Implementation (AA1–AA5) will tell the second half of the story.
If encoding Oedipus or multi-mythos Rashomon surfaces a gap the
sketch didn't see, the judgment flips and we have found the shift-
point work.

## Not in scope

- **Cross-dialect Lowering** (Aristotelian ↔ Dramatic; Aristotelian
  ↔ substrate). Separate sketch. A concrete multi-dialect encoding
  (Oedipus authored under both Dramatica AND Aristotelian; the
  existing Dramatica encoding exists) is a sketch-02 concern.
- **Four qualities of character** (good, appropriate, lifelike,
  consistent). Qualitative; not verifier-checkable in v1.
  Candidate Description-kind conventions.
- **Dianoia** (thought / argumentative speech as dialect primitive).
  Overlaps with Dramatic Scene/Beat content surface. No independent
  record in v1.
- **Comedy / satyr play genres.** Tragedy is this sketch's scope;
  genre-widening is sketch-02+.
- **Production-layer primitives** (lexis, melos, opsis). Below
  substrate.
- **Magnitude** ("proper size" — neither too small nor too large).
  Qualitative; defers to author judgment. Potential sketch-02 OQ:
  surface a structural proxy (event-count range? phase-coverage
  ratio?).

## Open questions

1. **OQ1 — Typed ArAffect record (catharsis/pity/fear).** A8
   punts to free-form Descriptions with author-chosen kind strings.
   If a second Aristotelian encoding (Macbeth? Rashomon's samurai?)
   lands and the probe finds the free-form approach too loose,
   sketch-02 upgrades to a typed record. Forcing function pending.
2. **OQ2 — Magnitude as a structural proxy.** Aristotle's
   "proper size" defies verifier check, but event-count and phase-
   coverage ratios might provide an advisory. Defer; not a
   sketch-01 commitment.
3. **OQ3 — Oedipus's peripeteia is conventionally placed at the
   messenger's adoption-reveal, but an alternative reading places
   it at the shepherd-testimony event** (where Jocasta has already
   realized and Oedipus is still pressing — the moment reversal is
   already structurally complete). The worked case picks the
   conventional placement; an encoding note preserves the
   alternative. Probe target.
4. **OQ4 — Does the dialect need an `ArChorus` record?** Greek
   tragedy's Chorus has no direct parallel in modern dramaturgy
   and no substrate representation. Deferred until an encoding
   actually wants to model the Chorus.
5. **OQ5 — Cross-dialect OQ inheritance.** When a work has both
   Dramatica and Aristotelian encodings (e.g., Oedipus), does the
   Dramatica `Story_consequence` align with Aristotelian
   `pathos`? Partly yes, partly no. Deferred to the cross-dialect
   sketch.

## Acceptance criteria

- [AA1] Dialect module `aristotelian.py` in
  `prototype/story_engine/core/` defines `ArMythos`, `ArPhase`,
  `ArCharacter`. Frozen dataclasses. No imports from substrate.
  Annotations via existing Description surface.
- [AA2] Self-verifier `aristotelian_self_verify(mythos, entities,
  events) -> VerificationReview list` implements A7 checks 1–5.
- [AA3] Encoding `encodings/oedipus_aristotelian.py` renders
  `AR_OEDIPUS_MYTHOS` per the worked example; imports only
  `aristotelian` core and `oedipus` substrate event ids.
- [AA4] Test `tests/test_aristotelian.py` covers A7 checks 1–5
  and the worked-case Oedipus encoding. Target: ~15–25 tests.
- [AA5] All tests pass; no change to any existing core record;
  post-sketch test totals update the state-of-play count.

If implementation surfaces a commitment that requires a core-
record change, halt and re-open the architectural question.

## Summary

A falsifiable stability test of the dialect stack. Aristotle's
*Poetics* carries primitives (plot unity, peripeteia, anagnorisis,
hamartia, catharsis) that *could* have required substrate-level
changes (fortune-state, audience-response, cross-dialect character
identity). Each is re-expressible within the existing architecture
by extension — new Template-level records, author-opt-in
assertions, verifier-local checks over existing substrate
predicates. No core-record modification.

Design-phase verdict: **architecture holds**. Oedipus (Aristotle's
own example) encodes natively. Rashomon (deliberate stress —
multi-testimony, no substrate frame) encodes as a multi-mythos
tuple, with one dialect-scope limit acknowledged (meta-anagnorisis,
same class as A8's catharsis scope-out) and one extension flagged
but not forced (`ArMythosRelation`, sketch-02 if a forcing function
appears).

Implementation is the second half of the test. If the code
encoding lands clean, the shift-point signal is confirmed; if it
surfaces a gap, this sketch's verdict is amended and the
architectural work resumes.
