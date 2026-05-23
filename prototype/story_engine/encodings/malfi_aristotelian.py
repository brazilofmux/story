"""
malfi_aristotelian.py — *The Duchess of Malfi* encoded under the
Aristotelian dialect (aristotelian-sketch-01 A1–A9 + sketch-02
A10–A12 + sketch-03 A13–A14 + sketch-04 A15–A16 + sketch-05
A17–A18).

Sixth Aristotelian encoding after Oedipus, Rashomon, Macbeth,
Hamlet, and Lear. Substrate layer lives in
`prototype/story_engine/encodings/malfi.py`; this file references
substrate event ids by string only.

Session 2 of the Malfi multi-session research arc (Session 1
shipped the substrate skeleton at commit `0b5e0e3`). The Duchess
is the corpus's **first non-Shakespeare Jacobean tragedy** and
the first encoding authored specifically to pressure a Lear-arc
banked open question:

**OQ-LEAR-4 — Secondary peripeteia for subplot.** Lear's Session 6
probe surfaced the pressure with three concrete dialect-extension
candidates (`secondary_peripeteia_event_ids` field;
`ArPhase`-level `peripeteia_event_id`; `ArMythosRelation
kind='subplot'`) but flagged that **cross-encoding pressure is
the forcing criterion.** This is that cross-encoding pressure.

The Duchess of Malfi authors **four structurally-distinct
character-arc peripeteia events within a single mythos**, more
than any prior corpus encoding:

1. **The Duchess's arc peripeteia** at `E_capture_in_countryside`
   (τ_s=17). Her concealment collapses; she passes from
   secret-but-flourishing to captured-and-doomed. Classical
   Aristotelian peripeteia: fortune reverses direction at the
   end of the middle phase. This is what the encoding authors as
   `AR_MALFI_MYTHOS.peripeteia_event_id`.

2. **Ferdinand's arc peripeteia** at `E_ferdinand_views_corpse`
   (τ_s=23). "Cover her face; mine eyes dazzle: she died young."
   He passes from tormentor to madman in the same instant as the
   recognition lands. This event is `AR_MALFI_MYTHOS.
   anagnorisis_event_id` — the dialect carries it as the main
   anagnorisis (Ferdinand's recognition is the play's most
   textually-explicit one) but **the structural content is also
   Ferdinand's peripeteia**. One event, two structural roles
   that the dialect cannot simultaneously name.

3. **Bosola's arc peripeteia** at `E_bosola_resolves_revenge`
   (τ_s=24). The play's most explicit mid-arc reversal: the
   instrument becomes the avenger. The corpus's first character
   whose arc-shape is *primarily* a reversal-from-within (rather
   than a reversal-by-external-event). Authored as the second
   parallel chain step `AR_STEP_BOSOLA_RESOLVES`, post-main.
   The dialect carries this as a chain step — but the chain-step
   apparatus is for anagnorises supplementary to the main, not
   for peripeteiai. The shape mismatches the field.

4. **Antonio's arc peripeteia** at `E_bosola_kills_antonio`
   (τ_s=30). The bitterest reversal: Antonio is killed by Bosola
   *in the dark*, mistaken-identity, moments before
   reconciliation. Anti-recognition: both parties recognize the
   other mid-stab, after the wound is mortal. Authored as the
   third parallel chain step `AR_STEP_ANTONIO_DARK_RECOGNITION`
   — but again, the chain-step apparatus is for anagnorises, and
   Antonio's recognition is *anti*-anagnorisic (recognition
   arrives too late to alter outcome).

**OQ-LEAR-4 forcing summary:** the dialect's single
`peripeteia_event_id` slot cannot carry the four distinct arc
peripeteia events. The encoding has to **choose one** and
relegate the other three to chain steps + prose annotations.
The three sketch-05 candidate shapes (in order of structural
fit, per `OQ_LEAR_4_FINDING` below):

- `ArMythos.secondary_peripeteia_event_ids: Tuple[str, ...]`
  attached to the main peripeteia. Cleanest fit; admits all
  three additional Webster reversals as supplementary peripeteia
  events. The current chain-step apparatus would be reserved for
  anagnorises, restoring the field's semantic purity.

- `ArPhase`-level `peripeteia_event_id: Optional[str]`. Allows
  per-phase peripeteia. Bosola's reversal in the end phase
  (τ_s=24) and Antonio's anti-recognition in the end phase
  (τ_s=30) co-locate in the end phase, so the per-phase shape
  would have to either choose one or accept multiplicity. Less
  clean for Webster than for Lear.

- `ArMythosRelation kind="subplot"`. Captures structural plot-
  subordination (Lear's Gloucester subplot is genuinely subplotted
  beneath the Lear plot). Webster's structure is NOT subplot-shaped
  — all four arcs converge on the Duchess's death-and-aftermath;
  there is no causal subordination of the "Bosola arc" or
  "Ferdinand arc" beneath the "Duchess arc". Worst fit for Webster.

The encoding's recommendation (carried in `OQ_LEAR_4_FINDING`
prose, banked for the sketch-06 closure cycle): **option 1
(`secondary_peripeteia_event_ids` field)** is the right shape.
The Duchess pressures Lear's already-banked recommendation in
the same direction.

A second forcing function is implicit and is banked as
**OQ-MALFI-1 — instrument-shared-by-multiple-wielders.** The
Duchess authors two `kind="instrumental"` A13 relations on the
same instrument (Bosola) by two different wielders (Ferdinand
in the play's commission, Cardinal in pre-play galley service +
Act V re-employment). This is **a structural shape distinct from
Lear's polarity-contrast** (same target, opposite polarity, two
wielders). Webster's shape is *sequential wielding with shared
polarity* — the instrument is morally consistent (malicious in
both employments) but is passed across employers across time.
See `OQ_MALFI_1_FINDING` below.

Sketch-03 + sketch-04 + sketch-05 axis exercise:

- **A12 exercises BINDING_SEPARATED with distance 6.** Webster's
  peripeteia at τ_s=17 + anagnorisis at τ_s=23. Corpus context:
  Oedipus COINCIDENT, Macbeth COINCIDENT, Hamlet SEPARATED-9,
  Lear SEPARATED-14. **Malfi SEPARATED-6 — the narrowest
  SEPARATED in the corpus.** Re-resurfaces OQ-AP7 (already
  banked under sketch-04 after Hamlet's 9-distance surface, re-
  surfaced by Lear's 14-distance): a fourth data point at 6
  presses on the near/distant sub-axis. See `OQ_AP7_RE_SURFACE`.

- **A11 + A14 anagnorisis chain: two parallel post-main steps**,
  both authored to *carry* arc-peripeteia content the
  `peripeteia_event_id` slot cannot. This is a notable use of
  the chain apparatus — sketch-03's A11 commits chain steps to
  carry *anagnorises*, but the Bosola step carries a
  recognition-that-is-also-a-reversal and the Antonio step
  carries an anti-recognition. Both are post-main (after
  Ferdinand's τ_s=23). Both `step_kind="parallel"`. The
  semantic stretch of the chain apparatus is what OQ-LEAR-4
  is forcing.

- **A13: four relations.** Two canonical (foil + parallel), two
  non-canonical `kind="instrumental"`. Both instrumentals share
  target (Bosola) and polarity (malicious). The dialect's
  A7.15 check 5 (paired-non-canonical-polarity-contrast)
  recognizes only different-polarity pairs and so does not fire
  on this pair — surfacing a related-but-distinct shape that
  Lear's `Edmund→Gloucester (malicious) + Edgar→Gloucester
  (therapeutic)` exercised. OQ-MALFI-1 banks the new shape.

- **A18 (sketch-05) `anagnorisis_absent`:** The Duchess. Like
  Cordelia, she dies without recognition ("I am Duchess of Malfi
  still"). Sketch-05's field structurally carries the claim.
  Corpus second use after Cordelia. The pattern (sketch-05's
  closure) generalizes cleanly to a second site.

Unities. Unity of action: **asserts=True.** Unlike Lear (the
first corpus False), the Duchess's four character-arcs converge
causally on the Duchess's death-and-aftermath. Bosola's arc is
not subordinated nor parallel to the Duchess's — it is *within*
the Duchess's action, as the action's witnessing-and-executing
instrument. This is the distinction Lear's OQ-LEAR-2 implicitly
asked for and Webster instantiates: classical-unity-of-action +
multi-character-arc-peripeteia are structurally compatible.
Unity of time: asserts=False (decade-long fabula, τ_s span 63
from -30 to 33). Unity of place: asserts=False (six locations:
Amalfi, Ancona, Loretto, countryside, prison cell, Cardinal's
palace).

Catharsis. aims_at_catharsis=True per the dialect default. The
play's pathos shape is **dense mid-Act-IV cluster** (Duchess +
Cariola + younger children at τ_s=22, Ferdinand's collapse at
τ_s=23, Bosola's collapse at τ_s=24) plus **dispersed Act-V
night-violence** (Julia τ_s=27, Antonio τ_s=30, Cardinal τ_s=31,
Ferdinand+Bosola τ_s=32). The dense-cluster-plus-dispersed-
finale shape is distinct from Lear's dispersed-offstage shape
and Hamlet's clustered-onstage shape. If OQ-AP1 (ArPathos
grounding) opens, Malfi adds a fifth pathos shape to the corpus.

No ArMythosRelation authored. *The Duchess of Malfi* is single-
mythos; no Rashomon-style contest. `AR_MALFI_MYTHOS` stands
alone.

Running:
    cd prototype
    python3 -c "
    from story_engine.encodings.malfi import FABULA
    from story_engine.encodings.malfi_aristotelian import (
        AR_MALFI_MYTHOS, AR_MALFI_CHARACTER_ARC_RELATIONS,
    )
    from story_engine.core.aristotelian import verify
    observations = verify(
        AR_MALFI_MYTHOS,
        substrate_events=FABULA,
        mythoi=(AR_MALFI_MYTHOS,),
        character_arc_relations=AR_MALFI_CHARACTER_ARC_RELATIONS,
    )
    print(f'{len(observations)} observation(s)')
    for o in observations:
        print(f'  [{o.severity}] {o.code}: {o.message}')
    "
"""

from __future__ import annotations

from story_engine.core.aristotelian import (
    ArAnagnorisisStep,
    ArAudienceKnowledgeConstraint,
    ArCharacter,
    ArCharacterArcRelation,
    ArCoPresenceRequirement,
    ArMythos,
    ArPhase,
    ARC_RELATION_FOIL,
    ARC_RELATION_PARALLEL,
    BINDING_PREF_NEAR,
    BINDING_SEPARATED,
    DIRECTIONALITY_DIRECTIONAL,
    DIRECTIONALITY_SYMMETRIC,
    PACING_EVEN,
    PACING_RAPID_ESCALATION,
    PACING_SLOW_BURN,
    PHASE_BEGINNING,
    PHASE_END,
    PHASE_MIDDLE,
    PLOT_COMPLEX,
    POLARITY_MALICIOUS,
    STEP_KIND_PARALLEL,
    TONAL_REGISTER_TRAGIC_WITH_IRONY,
)


# ============================================================================
# Phases — A2 (three logical divisions)
# ============================================================================

PH_BEGINNING = ArPhase(
    id="ph_malfi_beginning",
    role=PHASE_BEGINNING,
    scope_event_ids=(
        # Pre-play standing facts (5 events)
        "E_aragon_family",
        "E_duchess_widowed",
        "E_cardinal_julia_liaison",
        "E_bosola_galley_service",
        "E_antonio_returns_from_france",
        # Act I — warning, hiring, secret marriage (4 events)
        "E_brothers_warn_duchess",
        "E_ferdinand_hires_bosola",
        "E_duchess_woos_antonio",
        "E_secret_marriage",
        # Act II — pregnancy, apricot ploy, horoscope, Bosola reports
        # (5 events)
        "E_duchess_pregnant_first",
        "E_apricot_ploy",
        "E_first_child_born",
        "E_horoscope_dropped",
        "E_bosola_letters_ferdinand",
    ),
    # A15-SE1 — current count 14. Bounds (12..16) admit modest
    # compression of the pre-play standing-fact cluster or expansion
    # to author additional Act-II beats (Webster's Act II has more
    # business than the encoded spine — Pescara/Roderigo dialogues,
    # the Cardinal's brief Act-II scene with Julia).
    min_event_count=12,
    max_event_count=16,
    # A16-SP3 — Webster's beginning is structurally tight but
    # tonally compressed: the brothers' warning + Bosola's
    # commission (Act I) and the apricot/horoscope sequence (Act
    # II) move with the calculation typical of the play's tone.
    # Not rapid escalation (the children sequence has its own
    # temporal compression); not slow burn (the action does not
    # build emotionally). PACING_EVEN is the closest fit.
    pacing_preference=PACING_EVEN,
    annotation=(
        "Antecedent conditions + the play's two catastrophic "
        "commitments. Pre-play (τ_s=-30..-3): the Aragonese family "
        "tree (Duchess + Ferdinand twins, Cardinal eldest), the "
        "Duchess's widowhood and rule over Amalfi, the Cardinal's "
        "established affair with Julia, Bosola's prior galley service "
        "for the Cardinal, Antonio's return from France as the "
        "Duchess's steward. Act I (τ_s=0..4): the brothers' warning "
        "against remarriage, Ferdinand's commission of Bosola as "
        "intelligencer (the play's first instrumental relation, "
        "AR_FERDINAND_BOSOLA_INSTRUMENTAL), the Duchess's wooing of "
        "Antonio in Cariola's concealed presence, the per verba "
        "secret marriage. Act II (τ_s=6..10): pregnancy and the "
        "apricot ploy, Antonio's dropped horoscope giving Bosola "
        "certain knowledge of the first child, Bosola's letter to "
        "Ferdinand carrying the news. The beginning closes with "
        "Ferdinand knowing the marriage exists but not the spouse's "
        "identity — the structural pressure that drives Act III's "
        "confrontation."
    ),
)

PH_MIDDLE = ArPhase(
    id="ph_malfi_middle",
    role=PHASE_MIDDLE,
    scope_event_ids=(
        # Act III — confrontation, flight, banishment, capture
        # (6 events)
        "E_ferdinand_confronts_duchess",
        "E_duchess_devises_pilgrimage",
        "E_flight_to_ancona",
        "E_banishment_at_loretto",
        "E_duchess_sends_antonio_away",
        "E_capture_in_countryside",
    ),
    # A15-SE1 — current count 6. Bounds (5..8) admit modest expansion
    # if Session 3+ refines the bedchamber-confrontation into its
    # distinct beats (Ferdinand's dagger gift, the lock-of-hair
    # delivery, the Duchess's lie about the rumour-source) or the
    # Loretto banishment into pre-banishment + ritual + post-ritual.
    min_event_count=5,
    max_event_count=8,
    # A16-SP3 — slow burn. Each event tightens the noose: the
    # confrontation, the cover-story, the flight, the banishment,
    # the separation, the capture. No pressure relief; relentless
    # narrowing.
    pacing_preference=PACING_SLOW_BURN,
    annotation=(
        "The binding. Webster's Act III is the play's longest "
        "structural arc — five preceding events that build toward "
        "the capture, plus the capture itself as the middle's "
        "closing event. The Duchess's secret marriage has held "
        "across years (Webster compresses; the substrate encodes "
        "two additional pregnancies as world-state at the same beat "
        "as the first; Sessions 3+ may refine). At τ_s=11, "
        "Ferdinand arrives in person with a dagger; she does not "
        "confirm. At τ_s=13, she devises the pilgrimage cover-story. "
        "At τ_s=14, the family flees to Ancona. At τ_s=15, the "
        "Cardinal performs the public banishment ritual at Loretto, "
        "by which point both brothers know the marriage and the "
        "spouse's identity. At τ_s=16, the Duchess parts from "
        "Antonio for safety. At τ_s=17, Bosola intercepts and "
        "captures her in the countryside — the **peripeteia**, "
        "the moment her concealment-and-survival strategy collapses "
        "utterly. The peripeteia is at the end of the middle, "
        "matching Aristotle's structural prescription; the "
        "Duchess's arc passes from secret-but-flourishing to "
        "captured-and-doomed in a single beat. The end phase opens "
        "on the consequences."
    ),
)

PH_END = ArPhase(
    id="ph_malfi_end",
    role=PHASE_END,
    scope_event_ids=(
        # Act IV — imprisonment, tortures, strangling, recognitions
        # (7 events)
        "E_imprisonment",
        "E_dead_hand_scene",
        "E_waxworks_scene",
        "E_madmen_masque",
        "E_strangling",
        "E_ferdinand_views_corpse",
        "E_bosola_resolves_revenge",
        # Act V — lycanthropy, poisoning, night-violence, the heir
        # returns (7 events)
        "E_ferdinand_lycanthropy",
        "E_cardinal_poisons_julia",
        "E_bosola_visits_cardinal_at_night",
        "E_bosola_kills_antonio",
        "E_bosola_kills_cardinal",
        "E_mutual_wounding_ferdinand_bosola",
        "E_delio_arrives_with_heir",
    ),
    # A15-SE1 — current count 14. Bounds (12..16) reflect the
    # density of the end cluster (eight named deaths in 11 events
    # at the end of the phase) and admit modest expansion if
    # Session 3 splits Webster's compressed Act-IV sequence
    # (madmen-then-executioners → madmen + dance + executioners
    # entrance + strangling separately).
    min_event_count=12,
    max_event_count=16,
    # A16-SP3 — rapid escalation. Webster's Act V is the corpus's
    # densest single-act catastrophe: six killings (Julia,
    # Cardinal, Antonio, Ferdinand, Bosola, plus the offstage
    # younger children retrospectively) in τ_s=27-33. Each beat
    # accelerates toward the mutual-wounding finale.
    pacing_preference=PACING_RAPID_ESCALATION,
    annotation=(
        "The unbinding plus the catastrophe. Act IV opens on the "
        "imprisonment (τ_s=18) and proceeds through three "
        "instrument-tortures (dead hand τ_s=19, waxworks τ_s=20, "
        "madmen-masque τ_s=21) to the strangling (τ_s=22 — Duchess "
        "+ Cariola + the two younger children). At τ_s=23 "
        "Ferdinand enters and views the corpse: 'Cover her face; "
        "mine eyes dazzle: she died young.' The recognition-and-"
        "reversal is the main anagnorisis (the dialect carries it "
        "via AR_MALFI_MYTHOS.anagnorisis_event_id) and "
        "simultaneously Ferdinand's arc peripeteia — the dialect's "
        "field structure cannot mark both, which is one face of "
        "OQ-LEAR-4. At τ_s=24, Bosola alone with the body resolves "
        "to revenge — the play's most explicit mid-arc reversal "
        "and Bosola's arc peripeteia, carried by the chain-step "
        "apparatus (AR_STEP_BOSOLA_RESOLVES) under semantic stretch "
        "of A11. Act V (τ_s=25-33) compresses the catastrophe: "
        "Ferdinand's lycanthropy manifests (τ_s=25); the Cardinal "
        "poisons Julia for what she has learned (τ_s=27); Bosola "
        "visits the Cardinal's chambers at night (τ_s=29) and "
        "Antonio enters into the dark (τ_s=30, the play's anti-"
        "recognition — Antonio is killed by mistake by the man "
        "who would have allied with him; Antonio's arc peripeteia, "
        "carried by AR_STEP_ANTONIO_DARK_RECOGNITION); Bosola "
        "kills the Cardinal (τ_s=31); Ferdinand enters in his "
        "lycanthropy and wounds Bosola mortally, Bosola wounds "
        "Ferdinand fatally (τ_s=32); Delio arrives with the "
        "Duchess's eldest son (τ_s=33), the survivor and heir. "
        "The phase carries the corpus's first explicit four-"
        "character-arc-peripeteia structure within a single "
        "mythos."
    ),
)


# ============================================================================
# Characters — A5
# ============================================================================
#
# Five ArCharacter records. Three with `is_tragic_hero=True` —
# Duchess, Bosola, Ferdinand. Two with `is_tragic_hero=False` —
# Antonio and Cardinal.
#
# Webster's play is unusual in that the structurally-most-explicit
# arc is NOT the title character's — Bosola is on stage longer
# than the Duchess, speaks more lines than her, and undergoes the
# most explicit mid-play reversal. Critics from Empson onward
# have argued Bosola is structurally the protagonist by length
# and onstage presence; the encoding marks him as one of three
# tragic heroes alongside the Duchess (who carries the title and
# the principal pathos) and Ferdinand (who carries the
# orchestrating-tormentor-becomes-madman arc).
#
# Three-tragic-hero pressure on OQ-AP6 (already closed by Lear's
# Session-2 sketch-04 closure): Webster confirms the closure
# generalizes to a third encoding. OQ-AP6 stays CLOSED.

AR_DUCHESS = ArCharacter(
    id="ar_duchess",
    name="the Duchess of Amalfi",
    character_ref_id="duchess",
    hamartia_text=(
        "Marrying secretly across rank in defiance of brothers who "
        "command otherwise. The Duchess's act of marrying Antonio "
        "per verba de praesenti is, by the play's own canon-law "
        "frame, valid; her act of concealing it from her brothers "
        "is the structural error. She knows the brothers will "
        "object — their opening warning explicitly forbids — and "
        "she chooses concealment over confrontation. The choice "
        "is principled at the level of love ('I have heard lawyers "
        "say, a contract in a chamber / Per verba presenti, is "
        "absolute marriage') but tactically catastrophic at the "
        "level of family politics. Her hamartia is the mismatch "
        "between her assessment of the brothers' enforcement "
        "capacity and the actual capacity Ferdinand demonstrates "
        "with Bosola, the dead-hand torture, and finally the "
        "execution. Webster gives her several scenes of stoic "
        "self-possession in the prison ('I am Duchess of Malfi "
        "still') — the famous declaration is what makes her "
        "anagnorisis_absent: she dies *without* recognizing the "
        "hamartia, holding her ground that the secret marriage "
        "was right. The play's tragic frame depends on this "
        "absence — if she had recognized her error in concealing, "
        "the catastrophe would shift register from honourable-"
        "defiance-of-tyranny to wretched-collapse-into-confession. "
        "Webster keeps her in the honourable register through to "
        "the strangling. A18 (`anagnorisis_absent=True`) carries "
        "the claim structurally — corpus second use after "
        "Cordelia."
    ),
    is_tragic_hero=True,
    # A18 (sketch-05): corpus second use of anagnorisis_absent
    # after Cordelia. The Duchess dies "Duchess of Malfi still"
    # — without recognition. Cordelia's anagnorisis_absent
    # carries hamartia-without-recognition; the Duchess's
    # carries defiance-without-collapse.
    anagnorisis_absent=True,
)

AR_ANTONIO = ArCharacter(
    id="ar_antonio",
    name="Antonio Bologna",
    character_ref_id="antonio",
    hamartia_text=(
        "Trusting the secret marriage to hold under the brothers' "
        "scrutiny — and, more structurally, accepting the Duchess's "
        "wooing in the first place, given the position-asymmetry. "
        "Antonio is the Duchess's steward when she proposes; he "
        "marries up by a vast rank-gap, in defiance of the play's "
        "political framework. His own assessment in the opening "
        "scene was that he could 'reform the world by my own "
        "behaviour' through faithful service; the marriage commits "
        "him to a path of secrecy and flight that culminates in "
        "his being killed in the dark by the man he had come to "
        "ally with. Webster's structurally-cruelest death — "
        "Antonio entering the Cardinal's chambers at night "
        "(τ_s=30) intending reconciliation, killed by Bosola "
        "who is at that moment turned against the brothers and "
        "would have helped him. The recognition is "
        "*anti*-anagnorisic: both Bosola and Antonio recognize "
        "the other's identity in the same instant as the wound "
        "lands, after the wound is mortal. No anagnorisis-"
        "before-action; no chance to alter outcome. "
        "`is_tragic_hero=False` — Antonio's arc is reactive "
        "throughout (he is wooed; he is fled; he is killed); he "
        "lacks the classical tragic hero's hamartia-with-"
        "deliberation shape. Authored as an ArCharacter for the "
        "A13 parallel relation with the Duchess "
        "(AR_DUCHESS_ANTONIO_PARALLEL) and for the dark-room "
        "anti-recognition chain step "
        "(AR_STEP_ANTONIO_DARK_RECOGNITION)."
    ),
    is_tragic_hero=False,
)

AR_BOSOLA = ArCharacter(
    id="ar_bosola",
    name="Daniel de Bosola",
    character_ref_id="bosola",
    hamartia_text=(
        "Accepting Ferdinand's commission against his own better "
        "judgement. Bosola opens the play already cynical about "
        "his prior service to the Cardinal ('I have done you "
        "better service than to be slighted thus'); when "
        "Ferdinand offers the intelligencer post, Bosola "
        "self-aware refers to himself as the devil's preacher and "
        "accepts anyway, for the money and the office. The "
        "hamartia is the accepting — knowing the work is "
        "corrupting and undertaking it. The corpus's most "
        "explicit instrument-character: every torture of the "
        "Duchess in Act IV is wielded by Bosola at Ferdinand's "
        "commission. The reversal lands at τ_s=24, alone with "
        "the Duchess's body, his recognition that the work he "
        "executed exceeds anything his hamartia allowed for: 'I "
        "am angry with myself, now that I wake.' From that beat "
        "forward he is the avenger — but every act of his "
        "vengeance (the night-room sequence in the Cardinal's "
        "palace) miscarries: he kills Antonio by mistake (the "
        "man he wanted to ally with), he kills the Cardinal but "
        "is killed in turn by Ferdinand. His final speech, "
        "'Mine is another voyage,' lands at τ_s=32. **Bosola is "
        "the structurally most explicit tragic hero of the play "
        "by length and onstage presence**; the title character is "
        "the principal pathos site and the play's name, but the "
        "play's structural arc-shape belongs to Bosola — "
        "instrument becoming avenger becoming corpse. "
        "`is_tragic_hero=True`."
    ),
    is_tragic_hero=True,
)

AR_FERDINAND = ArCharacter(
    id="ar_ferdinand",
    name="Ferdinand, Duke of Calabria",
    character_ref_id="ferdinand",
    hamartia_text=(
        "Possessive-incestuous obsession with his twin sister "
        "manifesting as proxy violence. Ferdinand's relation to "
        "the Duchess is the play's most psychologically dense "
        "registration: he is her twin, structurally bonded by "
        "Webster's twin_of substrate predicate, and his violent "
        "policing of her sexual conduct exceeds rational political "
        "interest (the Cardinal's interest IS political; "
        "Ferdinand's is not). His hamartia is the misrecognition "
        "of his obsession AS political interest, with consequent "
        "actions (commissioning Bosola, orchestrating the dead-"
        "hand and waxworks tortures, ordering the strangling) "
        "that he cannot afterwards bear. The recognition lands "
        "at τ_s=23 with the Duchess's corpse: 'Cover her face; "
        "mine eyes dazzle: she died young.' The classical "
        "anagnorisis structure — knowledge dawning that the act "
        "the agent has committed exceeds what the agent can "
        "bear — and the simultaneous arc peripeteia: tormentor "
        "becomes madman in the same instant. mad(ferdinand) "
        "acquired at τ_s=23; lycanthropy(ferdinand) manifest at "
        "τ_s=25 with the wolf-skin delusion. He dies in the "
        "night-room sequence (τ_s=32), mortally wounded by "
        "Bosola, never recovered from the recognition. "
        "`is_tragic_hero=True` — the corpus's first tragic hero "
        "whose recognition is simultaneously the play's main "
        "anagnorisis but who is also structurally the orchestrator "
        "of the catastrophe. The role-combination is unprecedented "
        "in the corpus: prior orchestrators (Claudius in Hamlet, "
        "Edmund in Lear) carry only partial recognition (Claudius's "
        "prayer-without-repentance, Edmund's deathbed reversal); "
        "Ferdinand's is the most complete recognition by an "
        "orchestrator."
    ),
    is_tragic_hero=True,
)

AR_CARDINAL = ArCharacter(
    id="ar_cardinal",
    name="the Cardinal",
    character_ref_id="cardinal",
    hamartia_text=(
        "Politically-calculated complicity in the brothers' policing "
        "of the Duchess. The Cardinal participates in the warning "
        "(τ_s=0), the banishment ritual at Loretto (τ_s=15), and the "
        "post-mortem violence (poisoning Julia at τ_s=27 to silence "
        "her confession); his role is the play's purely-political "
        "register against Ferdinand's psychic one. The Cardinal "
        "does not recognize anything during the play's events — he "
        "calculates from his entrance to his death. His final "
        "scene (τ_s=31) is being stabbed by Bosola while his own "
        "attendants, per his earlier instruction, refuse to come "
        "to his aid; Webster's blackest comedy. He dies BELIEVED-"
        "knowing-he-is-dying but with no anagnorisic structure. "
        "`is_tragic_hero=False` — the corpus's most calculating "
        "antagonist. Authored as an ArCharacter for the second "
        "instrumental A13 relation (AR_CARDINAL_BOSOLA_"
        "INSTRUMENTAL — Bosola's prior galley service for the "
        "Cardinal at τ_s=-12 plus the Act V re-employment "
        "implicit in the body-disposal request at τ_s=29) and for "
        "the structural role of Ferdinand's political counterpart."
    ),
    is_tragic_hero=False,
)


# ============================================================================
# Anagnorisis chain — A11 (sketch-02) + A14 (sketch-03)
# ============================================================================
#
# Two chain steps, both `step_kind="parallel"`, both **post-main**.
# Each is authored under a notable semantic stretch of the A11 chain
# apparatus — the chain commits to anagnorises, but Webster's two
# post-main beats are arc-peripeteiai that the
# `peripeteia_event_id` slot cannot carry (OQ-LEAR-4 forcing).
#
# 1. AR_STEP_BOSOLA_RESOLVES (τ_s=24). Bosola alone with the
#    Duchess's body. The recognition lands ('I am angry with
#    myself, now that I wake'); the same beat carries his arc
#    peripeteia (instrument → avenger). Different character from
#    main (ar_bosola vs ar_ferdinand), non-precipitating
#    (Ferdinand's anagnorisis at τ_s=23 has already landed).
#    Post-main parallel step, the corpus's second after Lear's
#    Edmund-confesses.
#
# 2. AR_STEP_ANTONIO_DARK_RECOGNITION (τ_s=30). Antonio entering
#    the Cardinal's chambers at night, killed by Bosola in
#    mistaken-identity. The anti-recognition: both parties
#    recognize the other in the same instant, after the wound is
#    mortal. Different character from main (ar_antonio vs
#    ar_ferdinand), non-precipitating. Post-main parallel step.
#    The chain-step apparatus is here under maximum stretch: the
#    "step" carries an arc peripeteia + an *anti*-anagnorisic
#    recognition.
#
# Main anagnorisis: E_ferdinand_views_corpse (τ_s=23) on Ferdinand
# himself. AR_MALFI_MYTHOS names anagnorisis_character_ref_id=
# "ar_ferdinand" (A14). No staging steps — Ferdinand's progression
# toward the recognition is mostly act-and-react rather than
# epistemic-waypoint-shape; the dialect's `staging` step_kind
# admits only epistemic waypoints, and Ferdinand's arc does not
# stage epistemic acquisitions.
#
# The post-main pattern (Bosola at τ_s=24, Antonio at τ_s=30)
# echoes Lear's Edmund-confesses post-main step but with a
# distinction: Lear's post-main was a single deathbed-reversal;
# Webster's two post-main steps span the entire end phase. **The
# corpus's first multi-post-main-step chain.**

AR_STEP_BOSOLA_RESOLVES = ArAnagnorisisStep(
    id="arstep_bosola_resolves",
    event_id="E_bosola_resolves_revenge",
    character_ref_id="ar_bosola",
    step_kind=STEP_KIND_PARALLEL,
    precipitates_main=False,
    annotation=(
        "Bosola alone with the Duchess's body at τ_s=24. The "
        "recognition lands explicitly: 'I am angry with myself, "
        "now that I wake.' He attempts to revive her; she "
        "briefly recovers ('Mercy.'); she dies again; he resolves "
        "to revenge. The same beat carries his arc peripeteia "
        "(instrument → avenger; `avenger(bosola)` asserted at "
        "substrate scope at this event). Webster's most explicit "
        "mid-arc reversal in the corpus. **Post-main parallel "
        "step.** Different character from main (ar_bosola vs "
        "ar_ferdinand), non-precipitating: Bosola's resolve does "
        "not feed back into Ferdinand's recognition — Ferdinand "
        "has already left the chamber in his own collapse. The "
        "two corpse-side beats (Ferdinand at τ_s=23, Bosola at "
        "τ_s=24) are structurally serial, not coupled. **A "
        "semantic stretch of A11**: the chain is for anagnorises "
        "supplementary to the main; Bosola's beat is an "
        "anagnorisis (the recognition is explicit and verbal) "
        "but is *simultaneously* an arc peripeteia, which the "
        "main-peripeteia field cannot carry. OQ-LEAR-4 forcing "
        "manifest at this record."
    ),
)

AR_STEP_ANTONIO_DARK_RECOGNITION = ArAnagnorisisStep(
    id="arstep_antonio_dark_recognition",
    event_id="E_bosola_kills_antonio",
    character_ref_id="ar_antonio",
    step_kind=STEP_KIND_PARALLEL,
    precipitates_main=False,
    annotation=(
        "Antonio entering the Cardinal's chambers at night (τ_s=30) "
        "intending reconciliation, killed by Bosola who at that "
        "beat is turned against the brothers and would have allied "
        "with him. The recognition is *anti*-anagnorisic: both "
        "parties recognize the other in the same instant as the "
        "wound lands, after the wound is mortal. Webster's "
        "structurally-cruelest moment in the play — the rescue and "
        "alliance that the audience has been hoping for arrives in "
        "the same beat as the death that prevents it. **Post-main "
        "parallel step**, the second of two post-main steps in the "
        "chain (after AR_STEP_BOSOLA_RESOLVES); the corpus's first "
        "multi-post-main chain. Different character from main "
        "(ar_antonio vs ar_ferdinand), non-precipitating. **A "
        "deeper semantic stretch of A11 than the Bosola step**: "
        "Bosola's beat is an anagnorisis (the recognition is real, "
        "even if accompanied by an arc peripeteia); Antonio's beat "
        "is an *anti*-anagnorisis (the recognition is real but "
        "comes too late to alter outcome) plus an arc peripeteia "
        "(Antonio's arc reverses from secret-husband-in-exile to "
        "killed-in-the-dark). The chain step carries neither "
        "purely; both shapes pressure the apparatus. See "
        "`OQ_LEAR_4_FINDING` for the structural argument."
    ),
)


# ============================================================================
# Character-arc relations — A13 (sketch-03) + sketch-05 A17
# ============================================================================
#
# Four pairwise ArCharacterArcRelation records:
#
# - 2 canonical (`foil`, `parallel`) — symmetric, polarity-empty.
# - 2 non-canonical (`kind="instrumental"`) — directional,
#   polarity="malicious".
#
# The two instrumental relations exercise a structural shape
# **distinct from Lear's** instrumental pair: Lear had two
# wielders (Edmund, Edgar) with the *same target* (Gloucester)
# and *opposite polarity* (malicious vs therapeutic). Webster has
# two wielders (Ferdinand, Cardinal) with the *same target*
# (Bosola) and *same polarity* (malicious in both); the
# distinguishing axis is *temporal* — the Cardinal's wielding of
# Bosola is pre-play (galley service) plus brief Act-V re-
# employment, while Ferdinand's is the play's primary
# commission. The A7.15 check 5 paired-non-canonical-polarity-
# contrast does not fire here (it requires *different* polarities);
# the shape Webster authors is *paired-non-canonical-polarity-
# concordance with temporal-sequencing*. See OQ_MALFI_1_FINDING
# below for the candidate canonical extension.

AR_DUCHESS_FERDINAND_TWIN_FOIL = ArCharacterArcRelation(
    id="arc_duchess_ferdinand_twin_foil",
    kind=ARC_RELATION_FOIL,
    character_ref_ids=("ar_duchess", "ar_ferdinand"),
    mythos_id="ar_malfi",
    over_event_ids=(
        # Pre-play: the twin bond
        "E_aragon_family",
        # Act I: the warning + Duchess's defiance via secret marriage
        "E_brothers_warn_duchess",
        "E_secret_marriage",
        # Act III: Ferdinand's bedchamber confrontation
        "E_ferdinand_confronts_duchess",
        # Act IV: the tortures + strangling
        "E_dead_hand_scene",
        "E_strangling",
        # Act IV: the corpse-view + Ferdinand's collapse
        "E_ferdinand_views_corpse",
        # Act V: Ferdinand's lycanthropic death
        "E_mutual_wounding_ferdinand_bosola",
    ),
    annotation=(
        "The play's deepest structural relation. Ferdinand and the "
        "Duchess are twins — `twin_of(ferdinand, duchess)` at "
        "substrate scope from the pre-play standing-facts forward. "
        "The twin bond is structurally load-bearing: Webster's most "
        "psychologically dense registration is Ferdinand's "
        "possessive-incestuous obsession with his sister, manifest "
        "in his violent policing of her sexual conduct and "
        "collapsed (literally — lycanthropy) at the recognition of "
        "her corpse. The arc-shape is FOIL: the Duchess elects "
        "love, secrecy, and motherhood; Ferdinand elects "
        "control, public violence, and mad collapse. Each arc is "
        "the structural inverse of the other across the same "
        "pressures (the secret marriage as the test; the twin bond "
        "as the stake). Symmetric — the tuple order is not load-"
        "bearing. Polarity empty — canonical kind."
    ),
    directionality=DIRECTIONALITY_SYMMETRIC,
)

AR_DUCHESS_ANTONIO_PARALLEL = ArCharacterArcRelation(
    id="arc_duchess_antonio_parallel",
    kind=ARC_RELATION_PARALLEL,
    character_ref_ids=("ar_duchess", "ar_antonio"),
    mythos_id="ar_malfi",
    over_event_ids=(
        # Act I: the wooing + marriage
        "E_duchess_woos_antonio",
        "E_secret_marriage",
        # Act II: the household sequence
        "E_first_child_born",
        # Act III: flight + banishment + parting
        "E_flight_to_ancona",
        "E_banishment_at_loretto",
        "E_duchess_sends_antonio_away",
        # Act V: Antonio's death in the dark
        "E_bosola_kills_antonio",
    ),
    annotation=(
        "The marital arc — Duchess and Antonio share fortune and "
        "ruin in structural parallel across the play. The wooing "
        "(τ_s=3), the per verba marriage (τ_s=4), the secret "
        "household (τ_s=6-10), the discovery and flight (τ_s=11-"
        "16), and the parting (τ_s=16) all carry both characters' "
        "fortunes in the same direction. They are separated for "
        "the catastrophe — the Duchess captured and strangled at "
        "Amalfi (τ_s=17-22), Antonio in transit and killed in the "
        "dark in Rome (τ_s=30) — but the arc-shape remains "
        "parallel: both die for the same act (the marriage), at "
        "the hands of Ferdinand-and-Bosola, neither in the other's "
        "presence. Webster's symmetry is explicit: the parting at "
        "τ_s=16 names both their fates structurally aligned. "
        "Symmetric — the tuple order is not load-bearing. "
        "Polarity empty — canonical kind."
    ),
    directionality=DIRECTIONALITY_SYMMETRIC,
)

AR_FERDINAND_BOSOLA_INSTRUMENTAL = ArCharacterArcRelation(
    id="arc_ferdinand_bosola_instrumental",
    kind="instrumental",  # non-canonical; sketch-03 admits at severity=noted
    character_ref_ids=("ar_ferdinand", "ar_bosola"),
    mythos_id="ar_malfi",
    over_event_ids=(
        # Commission (Act I)
        "E_ferdinand_hires_bosola",
        # Intelligence-gathering (Act II)
        "E_apricot_ploy",
        "E_bosola_letters_ferdinand",
        # Capture and torture deployment (Acts III-IV)
        "E_capture_in_countryside",
        "E_dead_hand_scene",
        "E_waxworks_scene",
        "E_madmen_masque",
        "E_strangling",
        # The instrument's collapse: Bosola turns avenger
        "E_bosola_resolves_revenge",
        # And eventually kills the wielder (mutual wounding)
        "E_mutual_wounding_ferdinand_bosola",
    ),
    annotation=(
        "Ferdinand wields Bosola as the play's primary instrument "
        "of violence against the Duchess. The instrumental chain "
        "is the corpus's most extensive: Ferdinand's commission "
        "(τ_s=1) initiates an arc that carries through every "
        "torture (dead-hand, waxworks, madmen-masque), the "
        "strangling itself (Bosola is the strangler at "
        "Ferdinand's order), and ultimately the strangler's "
        "recognition-and-reversal (τ_s=24, Bosola alone with the "
        "corpse). Bosola is the corpus's first instrument-character "
        "whose arc includes the instrument-turning-against-wielder "
        "shape: he kills Ferdinand in the mutual wounding "
        "(τ_s=32), closing the instrumental relation with a "
        "literal reversal of agency.\n\n"
        "`kind=\"instrumental\"` is non-canonical at sketch-03; "
        "sketch-05's canonical-plus-open discipline admits it at "
        "severity `noted`. Directional: the tuple is ordered "
        "(wielder, target) = (ferdinand, bosola). Polarity "
        "malicious. The structural shape — character X wields "
        "character Y as instrument of violence against character "
        "Z — is the same shape Lear's two instrumental relations "
        "exercise (Edmund and Edgar wielding instruments against "
        "Gloucester), but Webster's Ferdinand-Bosola relation is "
        "**human-on-human direct** rather than artifact-mediated "
        "(no forged letter, no staged wound, no horoscope — the "
        "instrument is a person)."
    ),
    directionality=DIRECTIONALITY_DIRECTIONAL,
    polarity=POLARITY_MALICIOUS,
)

AR_CARDINAL_BOSOLA_INSTRUMENTAL = ArCharacterArcRelation(
    id="arc_cardinal_bosola_instrumental",
    kind="instrumental",  # non-canonical; sketch-03 admits at severity=noted
    character_ref_ids=("ar_cardinal", "ar_bosola"),
    mythos_id="ar_malfi",
    over_event_ids=(
        # Pre-play: prior galley service
        "E_bosola_galley_service",
        # Act V: re-employment for the body-disposal request and
        # the night-room sequence
        "E_bosola_visits_cardinal_at_night",
        # The instrument turns: Bosola kills the second wielder
        "E_bosola_kills_cardinal",
    ),
    annotation=(
        "Bosola's *prior* employment as instrument by the "
        "Cardinal — the relation that brackets the play. Pre-play "
        "(τ_s=-12), the Cardinal used Bosola for unspecified "
        "violent service ('the gallies' is Webster's reference); "
        "the play opens with Bosola resentful of un-rewarded prior "
        "work. Act V reactivates the relation: the Cardinal asks "
        "Bosola to dispose of Julia's body (τ_s=29), instructing "
        "his attendants to ignore any cries from the chamber that "
        "night. The instrument's response is to turn on the second "
        "wielder: Bosola kills the Cardinal at τ_s=31, in the same "
        "dark-room sequence that began with Antonio's accidental "
        "death.\n\n"
        "**The corpus's first instance of a single instrument "
        "being wielded by two distinct employers**. Lear's two "
        "instrumental relations were two distinct wielders on a "
        "shared target (Gloucester) with opposite polarity; "
        "Webster's two instrumental relations are two distinct "
        "wielders on a shared *instrument* (Bosola) with same "
        "polarity. The structural shape is "
        "paired-non-canonical-polarity-concordance with temporal-"
        "sequencing — see OQ_MALFI_1_FINDING.\n\n"
        "`kind=\"instrumental\"` non-canonical, directional "
        "(wielder=cardinal, target=bosola), polarity=malicious. "
        "The A7.15 check 5 paired-non-canonical-polarity-contrast "
        "does not fire because both Webster instrumentals are "
        "malicious; the dialect's existing check signature does "
        "not catch the paired-concordance shape."
    ),
    directionality=DIRECTIONALITY_DIRECTIONAL,
    polarity=POLARITY_MALICIOUS,
)

AR_MALFI_CHARACTER_ARC_RELATIONS = (
    AR_DUCHESS_FERDINAND_TWIN_FOIL,
    AR_DUCHESS_ANTONIO_PARALLEL,
    AR_FERDINAND_BOSOLA_INSTRUMENTAL,
    AR_CARDINAL_BOSOLA_INSTRUMENTAL,
)


# ============================================================================
# Co-presence requirements — A15-SE2 (sketch-04)
# ============================================================================
#
# Three hard co-presence requirements, each carrying structural
# integrity for one of the play's load-bearing pairings.

AR_MALFI_CO_PRESENCE = (
    ArCoPresenceRequirement(
        id="copres_duchess_antonio_beginning",
        character_ref_ids=("ar_duchess", "ar_antonio"),
        phase_id="ph_malfi_beginning",
        # E_duchess_woos_antonio (τ_s=3) + E_secret_marriage (τ_s=4)
        # — the wooing and the marriage itself, both in Cariola's
        # concealed presence. The two-event minimum forces the
        # marriage-arc to have structural footing.
        min_count=2,
    ),
    ArCoPresenceRequirement(
        id="copres_ferdinand_bosola_beginning",
        character_ref_ids=("ar_ferdinand", "ar_bosola"),
        phase_id="ph_malfi_beginning",
        # E_ferdinand_hires_bosola (τ_s=1) — the commission scene.
        # Required for the instrumental relation to have its
        # establishing beat.
        min_count=1,
    ),
    ArCoPresenceRequirement(
        id="copres_bosola_duchess_end",
        character_ref_ids=("ar_bosola", "ar_duchess"),
        phase_id="ph_malfi_end",
        # E_strangling (τ_s=22, Bosola executes) + E_bosola_resolves
        # _revenge (τ_s=24, Bosola alone with the body). Two events.
        # Required for Bosola's arc peripeteia to have structural
        # footing.
        min_count=2,
    ),
)


# ============================================================================
# Audience-knowledge constraints — A15-SE3 (sketch-04)
# ============================================================================
#
# Three load-bearing pieces of dramatic-irony knowledge. Webster's
# dramatic irony shape is dense from Act II onward; three constraints
# cover the play's structural sites.

AR_MALFI_AUDIENCE_KNOWLEDGE = (
    ArAudienceKnowledgeConstraint(
        id="ak_secret_marriage_known",
        subject="secret_marriage_of_duchess_and_antonio_per_verba",
        # Audience knows at τ_s=4 — the marriage event itself.
        # Grounds Act II's pregnancy and the apricot-ploy scenes
        # (the audience knows what Bosola is trying to discover);
        # grounds Act III's confrontation (Ferdinand's "rumour" is
        # the marriage the audience has watched); grounds Act IV's
        # tortures (the dead-hand is fake to the audience because
        # the audience knows Antonio is alive and elsewhere).
        latest_τ_s=4,
        source_event_id="E_secret_marriage",
    ),
    ArAudienceKnowledgeConstraint(
        id="ak_bosola_intelligencer",
        subject="bosola_is_ferdinands_intelligencer_against_duchess",
        # Audience knows at τ_s=1 — the commission event. Grounds
        # every Bosola-Duchess scene from Act II forward: the
        # apricot ploy is read as Bosola probing, not as courtly
        # courtesy; the body-disposal request from the Cardinal in
        # Act V (τ_s=29) is read against the audience's knowledge
        # of Bosola's structural position as instrument.
        latest_τ_s=1,
        source_event_id="E_ferdinand_hires_bosola",
    ),
    ArAudienceKnowledgeConstraint(
        id="ak_antonio_alive_when_dead_hand_displayed",
        subject="antonio_alive_separately_from_dead_hand_displayed",
        # Audience knows at τ_s=16 — the parting scene (the last
        # the audience sees of Antonio before Act V). The dead-
        # hand scene at τ_s=19 lands as torture-by-deception
        # specifically because the audience knows the deception
        # ('this is not Antonio's hand') in advance of the
        # Duchess. The audience's knowledge across τ_s=19-22 is
        # the structural ground of the strangling-scene's pathos:
        # the Duchess dies believing Antonio dead, the audience
        # knows he is alive (and will live until τ_s=30).
        latest_τ_s=19,
        source_event_id="E_duchess_sends_antonio_away",
    ),
)


# ============================================================================
# Mythos — A1
# ============================================================================

AR_MALFI_MYTHOS = ArMythos(
    id="ar_malfi",
    title="The Duchess of Malfi",
    action_summary=(
        "The widowed Duchess of Amalfi, against her brothers' "
        "explicit injunction, secretly marries her steward Antonio "
        "in a per verba de praesenti ceremony witnessed only by "
        "her waiting woman Cariola. Her twin brother Ferdinand "
        "commissions Bosola — a returning malcontent with prior "
        "galley service for the Cardinal — as intelligencer to spy "
        "on her. Across years (Webster compresses), the Duchess "
        "bears children; Bosola, by an apricot ploy and a "
        "dropped horoscope, confirms the first pregnancy and "
        "reports to Ferdinand. Ferdinand arrives in person and "
        "confronts the Duchess in her bedchamber; she does not "
        "confirm. She devises a pilgrimage to Loretto as cover "
        "and flees with Antonio and the eldest son to Ancona. "
        "The Cardinal performs the public banishment ritual at "
        "Loretto. The Duchess sends Antonio onward with the "
        "eldest son for safety; Bosola intercepts her in the "
        "countryside and captures her — **the peripeteia of the "
        "Duchess's main arc**, the moment her concealment "
        "strategy collapses utterly. She and Cariola and the two "
        "younger children are imprisoned at Amalfi; Ferdinand "
        "tortures her with a dead hand, waxen figures of 'dead' "
        "Antonio and children, and a masque of madmen; Bosola at "
        "Ferdinand's order strangles her, Cariola, and the "
        "children. Ferdinand views the body — **the main "
        "anagnorisis** — 'Cover her face; mine eyes dazzle: she "
        "died young' — and his arc reverses from tormentor to "
        "madman in the same instant. Bosola, alone with the "
        "corpse, resolves to revenge; the play's most explicit "
        "mid-arc reversal. Ferdinand's lycanthropy manifests. "
        "The Cardinal poisons Julia for what she has learned. "
        "Bosola visits the Cardinal's chambers at night; Antonio "
        "enters into the dark, intending reconciliation, killed "
        "by Bosola who would have allied with him — **Antonio's "
        "arc peripeteia, an anti-recognition**. Bosola kills the "
        "Cardinal. Ferdinand enters in his madness, mortally "
        "wounds Bosola, is killed by Bosola in turn. Delio "
        "arrives with the Duchess's eldest son, the surviving "
        "heir. The catastrophe leaves no orchestrator standing. "
        "The Aragonese family is gone; the duchy passes to a "
        "child."
    ),
    central_event_ids=(
        # Pre-play (5)
        "E_aragon_family",
        "E_duchess_widowed",
        "E_cardinal_julia_liaison",
        "E_bosola_galley_service",
        "E_antonio_returns_from_france",
        # Beginning (Act I + Act II) (9)
        "E_brothers_warn_duchess",
        "E_ferdinand_hires_bosola",
        "E_duchess_woos_antonio",
        "E_secret_marriage",
        "E_duchess_pregnant_first",
        "E_apricot_ploy",
        "E_first_child_born",
        "E_horoscope_dropped",
        "E_bosola_letters_ferdinand",
        # Middle (Act III) (6)
        "E_ferdinand_confronts_duchess",
        "E_duchess_devises_pilgrimage",
        "E_flight_to_ancona",
        "E_banishment_at_loretto",
        "E_duchess_sends_antonio_away",
        "E_capture_in_countryside",
        # End (Act IV + Act V) (14)
        "E_imprisonment",
        "E_dead_hand_scene",
        "E_waxworks_scene",
        "E_madmen_masque",
        "E_strangling",
        "E_ferdinand_views_corpse",
        "E_bosola_resolves_revenge",
        "E_ferdinand_lycanthropy",
        "E_cardinal_poisons_julia",
        "E_bosola_visits_cardinal_at_night",
        "E_bosola_kills_antonio",
        "E_bosola_kills_cardinal",
        "E_mutual_wounding_ferdinand_bosola",
        "E_delio_arrives_with_heir",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=(PH_BEGINNING, PH_MIDDLE, PH_END),
    # Complication: the bedchamber confrontation. First event of
    # the middle phase; the structural moment Ferdinand makes the
    # marriage-pressure manifest in his own person, after Bosola's
    # discovery in Act II.
    complication_event_id="E_ferdinand_confronts_duchess",
    # Denouement: the capture. Last event of the middle phase, and
    # the Duchess's main arc peripeteia. The unbinding begins
    # immediately on the imprisonment (first end-phase event).
    denouement_event_id="E_capture_in_countryside",
    # A12 — BINDING_SEPARATED with distance 6. Corpus context:
    # Oedipus COINCIDENT, Macbeth COINCIDENT, Hamlet SEPARATED-9,
    # Lear SEPARATED-14, Malfi SEPARATED-6. Narrowest SEPARATED
    # in the corpus. OQ_AP7 (banked under sketch-04) is now
    # pressured by three independent encodings with distances
    # 6, 9, and 14 — see OQ_AP7_RE_SURFACE below.
    #
    # Peripeteia: the Duchess's capture in the countryside. The
    # Duchess's main arc reversal — from secret-but-flourishing
    # to captured-and-doomed. Selected as the main peripeteia
    # because the dialect's `peripeteia_event_id` slot admits one
    # event and the Duchess is the title character whose arc the
    # main slot must carry. The play's three additional arc-
    # peripeteia events (Ferdinand at τ_s=23, Bosola at τ_s=24,
    # Antonio at τ_s=30) are carried by anagnorisis chain steps
    # and prose annotations — under semantic stretch of A11. See
    # OQ_LEAR_4_FINDING for the structural argument.
    peripeteia_event_id="E_capture_in_countryside",
    # Anagnorisis: Ferdinand's corpse-view recognition. The play's
    # most textually-explicit recognition ("Cover her face; mine
    # eyes dazzle: she died young"). Simultaneously Ferdinand's
    # arc peripeteia — recognition and reversal in the same beat.
    # The dialect's field structure cannot mark both simultaneously;
    # the slot is used for the recognition (anagnorisis_event_id +
    # anagnorisis_character_ref_id), the reversal is carried by
    # prose at this annotation and at AR_FERDINAND.
    anagnorisis_event_id="E_ferdinand_views_corpse",
    # **Unity of action: asserts=True**. Unlike Lear (corpus first
    # False), Webster's four character-arc-peripeteia events
    # converge causally on the Duchess's death-and-aftermath. The
    # Bosola arc is not subordinated (subplot) nor parallel
    # (independent action); it is *within* the Duchess's action
    # as the action's witnessing-and-executing instrument. The
    # Ferdinand arc is the orchestrating-half of the same action.
    # The Antonio arc is the marital-collateral of the same
    # action. Classical Aristotelian unity-of-action permits "one
    # action with many character-arc reversals" — a distinction
    # the dialect's `asserts_unity_of_action` field carries
    # implicitly. Lear's OQ-LEAR-2 asked whether the True/False
    # binary needed positively-named shape labels; Webster
    # confirms that the binary holds — the structural distinction
    # is between unity-of-action (one action) and parallel-actions
    # (Lear's two parallel plots with thematic-but-not-causal
    # integration).
    asserts_unity_of_action=True,
    asserts_unity_of_time=False,
    asserts_unity_of_place=False,
    aims_at_catharsis=True,
    characters=(AR_DUCHESS, AR_ANTONIO, AR_BOSOLA, AR_FERDINAND, AR_CARDINAL),
    # A11 + A14 — two-step chain, both parallel kind, both **post-
    # main**. The corpus's first multi-post-main chain. Both
    # steps carry arc-peripeteia content the main slot cannot;
    # under semantic stretch of A11, the chain apparatus carries
    # the OQ-LEAR-4 forcing pressure.
    anagnorisis_chain=(
        AR_STEP_BOSOLA_RESOLVES,
        AR_STEP_ANTONIO_DARK_RECOGNITION,
    ),
    # A12 — SEPARATED with distance 6. Corpus narrowest SEPARATED.
    # OQ_AP7 re-surface (third independent encoding).
    peripeteia_anagnorisis_binding=BINDING_SEPARATED,
    # A14 — the character whose recognition lands at
    # anagnorisis_event_id. Ferdinand — the corpus's first
    # orchestrator-also-recognizer (Claudius had partial prayer-
    # recognition; Edmund had deathbed-recognition; Ferdinand has
    # the full classical anagnorisis structure as the corpse
    # registers).
    anagnorisis_character_ref_id="ar_ferdinand",
    # A15-SE2 — three hard co-presence requirements.
    co_presence_requirements=AR_MALFI_CO_PRESENCE,
    # A15-SE3 — three audience-knowledge timing constraints.
    audience_knowledge_constraints=AR_MALFI_AUDIENCE_KNOWLEDGE,
    # A16-SP1 — soft tonal preference. Webster's signature: the
    # calculated savagery, the dark comedy of the Cardinal's
    # attendants-don't-come scene, the moral ambiguity of Bosola's
    # final voyage — the play's tonal register is "tragic with
    # irony" more cleanly than any prior corpus encoding.
    # Contrast Lear's "tragic-pure" (the unrelieved pathos of
    # the carrying-Cordelia scene; the Fool's swallowed irony)
    # and Hamlet's "tragic-with-irony" (the reflexive commentary
    # of the play-within-a-play, the gravedigger scene). Webster's
    # irony is colder than Hamlet's — closer to dramatic structural
    # irony than to reflexive verbal irony.
    tonal_register=TONAL_REGISTER_TRAGIC_WITH_IRONY,
    # A16-SP2 — soft preference for narrow (near) peripeteia-
    # anagnorisis distance. The actual A12 distance is 6 — the
    # narrowest SEPARATED in the corpus. The preference matches:
    # Webster's structure compresses the recognition into the
    # six-step span of the imprisonment-and-execution sequence,
    # producing the dense mid-Act-IV cluster that is the play's
    # primary pathos site.
    binding_distance_preference=BINDING_PREF_NEAR,
)


# ============================================================================
# Probe-surface findings — OQ-LEAR-4 (sketch-04 banked; now
# cross-encoding pressured); OQ_AP7 re-surface; OQ_MALFI_1 new
# ============================================================================
#
# Prose constants for reference by future probe runs and sketch-06
# design. The dialect has no typed record for probe findings at
# encoding scope; these constants carry what the encoding surfaced,
# structured for future extraction.

OQ_LEAR_4_FINDING = (
    "OQ-LEAR-4 — Secondary peripeteia for subplot. **Cross-"
    "encoding pressure now confirmed.** Lear surfaced the "
    "pressure with one encoding (Gloucester subplot's blinding "
    "at τ_s=23 as structurally a secondary peripeteia to Lear's "
    "stripping at τ_s=14); Webster's Duchess pressures it with "
    "**four** structurally-distinct character-arc peripeteia "
    "events within a single mythos, more than any prior corpus "
    "encoding:\n\n"
    "1. The Duchess at E_capture_in_countryside (τ_s=17) — main "
    "   arc peripeteia. **Carried by AR_MALFI_MYTHOS."
    "peripeteia_event_id.**\n"
    "2. Ferdinand at E_ferdinand_views_corpse (τ_s=23) — arc "
    "   peripeteia + main anagnorisis in the same beat. **The "
    "   anagnorisis_event_id slot carries the recognition;** the "
    "   reversal-content lives in prose at AR_FERDINAND and at "
    "   this annotation.\n"
    "3. Bosola at E_bosola_resolves_revenge (τ_s=24) — arc "
    "   peripeteia + supplementary anagnorisis. **Carried by "
    "   chain step AR_STEP_BOSOLA_RESOLVES under semantic stretch "
    "   of A11** (the chain step apparatus is for anagnorises, "
    "   but Bosola's beat is also a peripeteia).\n"
    "4. Antonio at E_bosola_kills_antonio (τ_s=30) — arc "
    "   peripeteia + anti-recognition. **Carried by chain step "
    "   AR_STEP_ANTONIO_DARK_RECOGNITION under deeper semantic "
    "   stretch of A11** (the step carries an anti-anagnorisic "
    "   shape the chain semantics do not name).\n\n"
    "The dialect's single `peripeteia_event_id` slot cannot carry "
    "the four. The current encoding is structurally well-formed "
    "but the structural information is unevenly distributed: the "
    "main slot, the main anagnorisis slot, two chain steps, and "
    "prose annotation each carry a portion of what one apparatus "
    "should ideally carry uniformly.\n\n"
    "Candidate canonical extensions, in order of structural fit "
    "(restated from Lear-Session-2's surface and confirmed by "
    "cross-encoding pressure):\n\n"
    "1. **`ArMythos.secondary_peripeteia_event_ids: Tuple[str, "
    "   ...]`** attached to the main peripeteia. Cleanest fit: "
    "   admits Webster's three additional arc-peripeteia events "
    "   (Ferdinand at τ_s=23, Bosola at τ_s=24, Antonio at "
    "   τ_s=30) as supplementary peripeteia events alongside "
    "   the main. Restores the anagnorisis chain apparatus to "
    "   purely-anagnorisic semantics (the Bosola and Antonio "
    "   steps would migrate from the chain to the new field). "
    "   Lear's encoding would similarly migrate Gloucester's "
    "   blinding from prose-of-the-parallel-A13-relation to a "
    "   `secondary_peripeteia_event_ids` entry. **Webster "
    "   recommends this option.**\n\n"
    "2. **`ArPhase`-level `peripeteia_event_id: Optional[str]`.** "
    "   Allows per-phase peripeteia. Lear's structure fits this "
    "   cleanly (Lear's peripeteia in middle, Gloucester's "
    "   peripeteia also in middle but in the second-plot's "
    "   beat). Webster's structure fits less cleanly: three of "
    "   the four arc peripeteia (Ferdinand, Bosola, Antonio) "
    "   co-locate in the end phase, so the per-phase shape would "
    "   have to either choose one per phase or admit multiplicity "
    "   per phase — collapsing back into the same multiplicity "
    "   problem at a smaller scope.\n\n"
    "3. **`ArMythosRelation kind=\"subplot\"`.** Captures "
    "   structural plot-subordination. Lear's Gloucester subplot "
    "   is genuinely subplotted (subordinated beneath the Lear "
    "   plot in causal density and stage time). Webster's "
    "   structure is NOT subplot-shaped — all four arcs converge "
    "   on the Duchess's death-and-aftermath; there is no causal "
    "   subordination. Worst fit for Webster.\n\n"
    "Recommendation: sketch-06 should land option 1, with "
    "migration of Lear's Gloucester subplot reversal and "
    "Webster's three additional arc peripeteia into the new "
    "field. The A11 anagnorisis chain returns to purely-"
    "anagnorisic semantics. Session 5's live probe will test "
    "whether the reader-model surfaces the same recommendation "
    "or proposes a different shape."
)

OQ_AP7_RE_SURFACE = (
    "OQ-AP7 — Numerical range of BINDING_SEPARATED. **Third-"
    "encoding re-surface** with the corpus narrowest distance. "
    "Hamlet surfaced at distance 9; Lear re-surfaced at distance "
    "14; Webster's Duchess at distance 6. Under the default "
    "bound of 3, all three are categorically 'separated' — but "
    "the analytical content differs:\n\n"
    "- Webster's 6: the dense Act-IV compression. Capture at "
    "  τ_s=17 → imprisonment → tortures → strangling → Ferdinand's "
    "  recognition at τ_s=23. Six τ_s units span the unbinding-"
    "  to-recognition arc; the structural content is *intense* "
    "  rather than *delayed*.\n"
    "- Hamlet's 9: the verification-to-belated-recognition arc. "
    "  Peripeteia at the Mousetrap → Closet → Polonius → Laertes "
    "  → duel → recognition. The structural content is the *delay* "
    "  itself (Hamlet's famous procrastination).\n"
    "- Lear's 14: the slow-burn-of-suffering arc. Stripping at "
    "  τ_s=14 → storm → mock trial → blinding → Dover → "
    "  reconciliation at τ_s=28. The structural content is the "
    "  *accumulation* of suffering before recognition.\n\n"
    "Three encodings, three analytical shapes — *intense*, "
    "*delayed*, *accumulating* — all under one dialect category. "
    "OQ-AP7's near-separated-vs-distant-separated proposal "
    "(Hamlet) is now joined by a still-narrower data point. "
    "Candidate canonical refinements:\n\n"
    "- Three-bucket categorical: `narrow_separated` (4..6), "
    "  `medium_separated` (7..10), `wide_separated` (>10). "
    "  Webster, Hamlet, Lear fall into one bucket each.\n"
    "- Numerical `peripeteia_anagnorisis_distance` field alongside "
    "  the categorical binding, surfacing the raw distance for "
    "  reader-side interpretation.\n"
    "- A `peripeteia_anagnorisis_arc_shape` enum: `intense | "
    "  delayed | accumulating`, named structurally rather than "
    "  numerically. Captures the analytical content the bare "
    "  distance cannot.\n\n"
    "Banked. Session 5's live probe will surface whether the "
    "reader distinguishes these three shapes or reads them under "
    "'separated' without structural discomfort. Re-surface "
    "established with three independent encodings."
)

OQ_MALFI_1_FINDING = (
    "OQ-MALFI-1 — Sequentially-wielded-instrument with polarity-"
    "concordance. **NEW forcing function surfaced during Session "
    "2 authorship.** Webster authors two A13 records with "
    "`kind=\"instrumental\"` sharing target (Bosola) and polarity "
    "(malicious) but distinct in *wielder* and *temporal phase*:\n\n"
    "- `AR_CARDINAL_BOSOLA_INSTRUMENTAL`: pre-play galley service "
    "  (τ_s=-12) + Act V re-employment (τ_s=29-31). The Cardinal "
    "  wields Bosola in the play's brackets.\n"
    "- `AR_FERDINAND_BOSOLA_INSTRUMENTAL`: the play's primary "
    "  commission (τ_s=1) through every torture, the strangling, "
    "  the corpse-recognition, and the mutual wounding at τ_s=32. "
    "  Ferdinand wields Bosola through the play's main action.\n\n"
    "The structural shape is **paired-non-canonical-polarity-"
    "concordance with temporal-sequencing**: one instrument-"
    "agent (Bosola) is passed across two employers across time, "
    "with consistent moral polarity throughout. The play's "
    "tragic shape depends on this transferability — Bosola's "
    "willingness to be re-employed by the Cardinal in Act V "
    "(after a play of service to Ferdinand) is part of what makes "
    "his arc peripeteia at τ_s=24 explicit (he turns against "
    "BOTH wielders, not just the current one).\n\n"
    "**Distinct from Lear's instrumental pair.** Lear's "
    "Edmund→Gloucester + Edgar→Gloucester pair shares target "
    "(Gloucester) and has *opposite* polarity (malicious vs "
    "therapeutic). The A7.15 check 5 paired-non-canonical-"
    "polarity-contrast catches Lear's shape: two wielders, one "
    "target, polarity contrast. Webster's shape evades that check: "
    "two wielders, one target, polarity concordance. **The same "
    "wielder/target/polarity shape but with the wielders "
    "*sequentially* (not concurrently) operative.**\n\n"
    "Candidate canonical extensions:\n\n"
    "1. **A7.15 check 6 — paired-non-canonical-polarity-concordance**. "
    "   Sibling-shape to check 5: emit `noted` when two non-"
    "   canonical records share target and polarity. Caught by "
    "   inspection only at present.\n"
    "2. **`ArCharacterArcRelation.temporal_phase` field** "
    "   (`pre_play | early | mid | end | post_play | spanning`). "
    "   Distinguishes Webster's sequential-wielding shape from "
    "   Lear's concurrent shape. Adds expressive surface but "
    "   admits authoring complexity.\n"
    "3. **A new `ArCharacterArcRelation kind=\"instrument-"
    "transferred\"`** — captures the shape directly, distinct "
    "   from the canonical-or-non-canonical kinds. Cleanest if "
    "   the shape recurs in a third encoding (cross-encoding "
    "   pressure needed).\n\n"
    "Banked. Session 5's probe will test whether the reader "
    "structurally distinguishes Webster's shape from Lear's, "
    "and what the recommended canonical extension might be. The "
    "shape is single-encoding for now (Hamlet's Claudius-Laertes "
    "is concurrent-wielding-of-one-instrument, not sequential; "
    "Lear's pair is concurrent-with-polarity-contrast); cross-"
    "encoding pressure for OQ-MALFI-1 awaits a third encoding."
)

# Tuple export for probe-side consumption.
OQ_FINDINGS = (
    ("OQ_LEAR_4",       OQ_LEAR_4_FINDING),
    ("OQ_AP7",          OQ_AP7_RE_SURFACE),
    ("OQ_MALFI_1",      OQ_MALFI_1_FINDING),
)
