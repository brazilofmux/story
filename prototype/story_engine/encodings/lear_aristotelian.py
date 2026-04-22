"""
lear_aristotelian.py — *King Lear* encoded under the Aristotelian
dialect (aristotelian-sketch-01 A1–A9 + sketch-02 A10–A12 +
sketch-03 A13–A14 + sketch-04 A15–A16).

Fifth Aristotelian encoding after Oedipus, Rashomon, Macbeth, and
Hamlet. Substrate layer lives in
`prototype/story_engine/encodings/lear.py`; this file references
event ids by string only.

Session 2 of the Lear multi-session research arc (Session 1 shipped
the substrate skeleton at commit `bfecd73`; this file is Session 2
per the Hamlet precedent). Lear is banked as the second-site forcing
case for two forcing functions surfaced by Hamlet's Session 6 probe
(`aristotelian-probe-sketch-04`, 2026-04-21):

- **OQ-AP14 — Instrumental-kind ArCharacterArcRelation.** Hamlet
  surfaced the pressure with one A13 candidate (Claudius wielding
  Laertes as pawn in the duel-plot). Lear authors **two** A13
  records with the non-canonical kind `"instrumental"` operating on
  the same target (Gloucester) with opposite moral polarity:
  `AR_EDMUND_GLOUCESTER_INSTRUMENTAL` (malicious — the forged-letter
  chain) and `AR_EDGAR_GLOUCESTER_INSTRUMENTAL` (therapeutic — the
  staged Dover fall). The polarity contrast is substrate-grounded
  (substrate predicates `forged_letter`, `staged_wound`,
  `staged_cliff_fall` are all world-true facts in lear.py with
  distinct belief-effects on Gloucester). The kinds are authored
  with `kind="instrumental"`; sketch-03's canonical-plus-open
  discipline admits them at severity `noted`. Probe is expected
  either to propose a canonical extension (`instrumental` as a
  fourth canonical kind, possibly with a polarity sub-axis) or
  to read them structurally without requiring canonicalization.

- **OQ-AP15 — Absent-character catharsis.** Hamlet's probe
  surfaced the pressure in passing. Lear authors **four** offstage
  deaths whose substrate shape has world effects with zero or
  minimal observer projections:
  - `E_cordelia_hanged` (τ_s=36) — no observers at all; the
    catharsis lands through Lear's entrance at
    `E_lear_enters_with_cordelia` (τ_s=37).
  - `E_gloucester_dies` (τ_s=36) — a single observer (Edgar), and
    even he reports the death retrospectively.
  - `E_goneril_suicide` (τ_s=34) — only Albany observes, via a
    Gentleman's report.
  - `E_cornwall_dies` (compressed into
    `E_cornwall_regan_blind_gloucester`) — no explicit observer
    event; the death is a collateral consequence of the servant's
    intervention.
  This is the corpus's densest site of the offstage-death shape.
  The encoding does not author a typed ArAbsentCatharsisStep or
  similar record (sketch-03/sketch-04 do not ship one); the pressure
  lives in the substrate + phase coverage + `AR_LEAR_MYTHOS.central_
  event_ids` reach of the offstage events, and in the
  `OQ_AP15_FINDING` prose below.

Sketch-03 + sketch-04 axis exercise:

- **A12 exercises BINDING_SEPARATED with distance 14.** Lear's
  peripeteia fires at `E_goneril_strips_retinue` (τ_s=14) — the
  reversal from king-with-a-hundred-knights to unaccommodated-man,
  produced by Lear's own act of dividing the kingdom; his anagnorisis
  lands at `E_lear_cordelia_reconcile` (τ_s=28) — the deathbed-adjacent
  recognition that Cordelia's love was always world-true. Distance
  14. **Widest separation in the corpus** (Hamlet was 9, Oedipus 5,
  Macbeth COINCIDENT). OQ_AP7 (Hamlet-surfaced "near-separated vs
  distant-separated" distinction) is now forced on two independent
  encodings; see `OQ_AP7_FINDING` re-surface note below.

- **A11 + A14 anagnorisis chain: two parallel steps, no staging.**
  Unlike Hamlet's chain (two staging + one parallel), Lear's chain
  authors only `step_kind="parallel"` steps. Gloucester's
  anagnorisis at the blinding (τ_s=23) is parallel-character, pre-
  main, non-precipitating; Edmund's deathbed confession (τ_s=35) is
  parallel-character, **post-main** (the first post-main parallel
  step in the corpus), non-precipitating. The absence of staging
  steps is structurally load-bearing: Lear reaches his main
  anagnorisis by emotional progression (reconciliation with
  Cordelia) rather than epistemic acquisition (Hamlet's Ghost-claim
  + Mousetrap verification pattern). The dialect's `staging`
  step_kind admits only epistemic waypoints; Lear's emotional
  waypoints (the storm's "unaccommodated man" realization at τ_s=18,
  the mock trial's grievance-crystallization at τ_s=21, the
  heath-meeting with Gloucester at τ_s=27) are structurally analogous
  but semantically distinct. Banked as `OQ_LEAR_1` below.

- **Plot structure: double-plot unity question.** The Lear plot
  (Lear + his three daughters) and the Gloucester plot (Gloucester
  + his two sons) run in structural parallel across beginning,
  middle, and end. The two plots do converge at Dover (the
  heath-meeting, the battle) but are not subordinated one to the
  other. Classical Aristotelian unity of action requires one
  unified plot; Shakespeare's double-plot here is a well-known
  departure. The encoding authors `asserts_unity_of_action=False`
  — **the first corpus encoding to do so**. OQ_AP6's "three tragic
  heroes in one mythos" pressure is related but distinct: OQ-AP6
  asks whether multiple tragic arcs fit one mythos; Lear pressures
  whether the mythos itself is one action or two. See `OQ_LEAR_2`
  below.

Unities. Unity of action: **asserts=False** (corpus first — the
double-plot with thematic rather than causal integration). Unity of
time: asserts=False (τ_s span 68 units from -30 to 38). Unity of
place: asserts=False (Britain + four castles + heath + Dover + camp
+ prison).

Catharsis. aims_at_catharsis=True per the dialect's default. The
play's end-phase pathos is scattered across four offstage deaths
plus two onstage reports and one onstage final death — an unusually
dispersed pathos shape. OQ-AP1 (ArPathos grounding) stays banked;
Lear would be another candidate forcing encoding if OQ-AP1 opens,
distinct from Hamlet's cluster-pathos shape (Lear's is dispersed-
offstage rather than clustered-onstage).

No ArMythosRelation authored. Lear is single-mythos; no Rashomon-
style contest. `AR_LEAR_MYTHOS` stands alone.

Running:
    cd prototype
    python3 -c "
    from story_engine.encodings.lear import FABULA
    from story_engine.encodings.lear_aristotelian import (
        AR_LEAR_MYTHOS, AR_LEAR_CHARACTER_ARC_RELATIONS,
    )
    from story_engine.core.aristotelian import verify
    observations = verify(
        AR_LEAR_MYTHOS,
        substrate_events=FABULA,
        mythoi=(AR_LEAR_MYTHOS,),
        character_arc_relations=AR_LEAR_CHARACTER_ARC_RELATIONS,
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
    BINDING_PREF_WIDE,
    BINDING_SEPARATED,
    PACING_EVEN,
    PACING_RAPID_ESCALATION,
    PACING_SLOW_BURN,
    PHASE_BEGINNING,
    PHASE_END,
    PHASE_MIDDLE,
    PLOT_COMPLEX,
    STEP_KIND_PARALLEL,
    TONAL_REGISTER_TRAGIC_PURE,
)


# ============================================================================
# Phases — A2 (three logical divisions)
# ============================================================================

PH_BEGINNING = ArPhase(
    id="ph_lear_beginning",
    role=PHASE_BEGINNING,
    scope_event_ids=(
        # Pre-play standing (3 events)
        "E_lear_reigns",
        "E_gloucester_family",
        "E_edmund_resolves_to_plot",
        # Main plot Act I (8 events)
        "E_lear_announces_division",
        "E_love_test_goneril",
        "E_love_test_regan",
        "E_love_test_cordelia",
        "E_cordelia_disinherited",
        "E_kent_banished",
        "E_france_marries_cordelia",
        "E_kingdom_divided",
        # Gloucester subplot Act I (5 events)
        "E_edmund_forges_letter",
        "E_edmund_shows_gloucester",
        "E_edmund_warns_edgar",
        "E_edmund_stages_wound",
        "E_edgar_flees",
    ),
    # A15-SE1 — current count 16; bounds (14..18) admit modest
    # compression or expansion. Lear's beginning is structurally
    # larger than Hamlet's (13) because it has to set up both plots
    # + carry the love-test machinery across four speech events
    # (announce + three daughter responses).
    min_event_count=14,
    max_event_count=18,
    # A16-SP3 — the beginning moves at a steady tempo through the
    # love-test and kingdom-division, with the Gloucester subplot
    # as structural counterpoint. Neither plot accelerates; both
    # establish their terrain.
    pacing_preference=PACING_EVEN,
    annotation=(
        "Antecedent conditions + the two catastrophic decisions that "
        "set both plots in motion. Main plot: Lear announces the "
        "division (τ_s=0), the love-test (τ_s=1–3) produces "
        "Cordelia's refusal, Lear disinherits her (τ_s=4), Kent is "
        "banished (τ_s=5), France marries Cordelia dowerless (τ_s=6), "
        "and the kingdom is divided between Goneril and Regan (τ_s=7). "
        "Gloucester subplot: Edmund's three-beat instrumental chain "
        "opens — forged letter (τ_s=8), shown to Gloucester (τ_s=9), "
        "warning to Edgar (τ_s=10), staged wound (τ_s=11) — and Edgar "
        "flees (τ_s=12). The beginning closes with both plots' "
        "catastrophic decisions made: Lear has disinherited his "
        "loving daughter, Gloucester has turned against his loyal son. "
        "Each plot's first reversal is staged in the middle."
    ),
)

PH_MIDDLE = ArPhase(
    id="ph_lear_middle",
    role=PHASE_MIDDLE,
    scope_event_ids=(
        # Main plot Act II — Lear's humiliation (6 events)
        "E_lear_at_gonerils",
        "E_kent_returns_disguised",
        "E_goneril_strips_retinue",
        "E_lear_to_regans",
        "E_regan_also_strips",
        "E_lear_flees_to_heath",
        # Act III — storm, hovel, blinding (6 events)
        "E_storm_on_heath",
        "E_edgar_becomes_poor_tom",
        "E_gloucester_meets_poor_tom",
        "E_lear_mock_trial",
        "E_gloucester_sends_lear_to_dover",
        "E_cornwall_regan_blind_gloucester",
        # Act IV — Dover, Cordelia's return (4 events)
        "E_edgar_leads_blind_gloucester",
        "E_gloucester_suicide_attempt",
        "E_cordelia_returns",
        "E_lear_meets_blind_gloucester",
    ),
    # A15-SE1 — current count 16; bounds (13..18) admit a tighter
    # middle (compressing Act III's multiple heath-scenes) or a wider
    # middle (adding back the elided scenes like Oswald's death at
    # Edgar's hand, the Gentleman's reports, or the Doctor-and-Cordelia
    # recovery scene).
    min_event_count=13,
    max_event_count=18,
    # A16-SP3 — the middle is the corpus's clearest case of slow
    # burn. From Goneril's stripping (τ_s=14) through the storm, the
    # hovel, the mock trial, the blinding, Dover, and the two
    # reunions (τ_s=20 through τ_s=27), the pressure builds
    # relentlessly without relief; each scene adds to Lear's and
    # Gloucester's suffering rather than resolving it.
    pacing_preference=PACING_SLOW_BURN,
    annotation=(
        "The binding. Lear lodges with Goneril (τ_s=13) — the "
        "consequence of the division. Goneril strips his retinue "
        "(τ_s=14) — the peripeteia, the reversal-by-own-action: "
        "Lear's choice to demand flattery and disinherit honesty "
        "has turned against him. The second stripping at Regan's "
        "(τ_s=16) confirms it; Lear flees into the storm. Act III "
        "compresses the storm, the hovel encounter with "
        "Edgar-as-Poor-Tom, the mock trial of the absent daughters, "
        "and Gloucester's blinding — the Gloucester subplot's "
        "peripeteia-analog, with an anagnorisis (Gloucester's "
        "recognition of Edmund's betrayal, authored as the parallel "
        "chain-step `AR_STEP_GLOUCESTER_BLINDING`) bound to it in "
        "the same scene. Act IV stages Edgar's therapeutic Dover "
        "instrument + Cordelia's military return + the two reunions "
        "(Lear-Gloucester on the heath, setting the tone for "
        "Cordelia's return). Middle ends with `E_lear_meets_blind_"
        "gloucester` (τ_s=27) — the denouement, the point where both "
        "broken fathers are in each other's presence and the "
        "emotional register of the reconciliation is set."
    ),
)

PH_END = ArPhase(
    id="ph_lear_end",
    role=PHASE_END,
    scope_event_ids=(
        "E_lear_cordelia_reconcile",
        "E_battle",
        "E_lear_cordelia_captured",
        "E_edmund_orders_cordelia_hanged",
        "E_edgar_defeats_edmund",
        "E_regan_dies",
        "E_goneril_suicide",
        "E_edmund_confesses",
        "E_cordelia_hanged",
        "E_gloucester_dies",
        "E_lear_enters_with_cordelia",
        "E_lear_dies",
        "E_edmund_dies",
    ),
    # A15-SE1 — current count 13; bounds (11..16) reflect that the
    # end cluster is dense with deaths (seven in Lear, distinct
    # causes) and admits modest expansion if Session 3's SJUZHET
    # distinguishes (e.g., splitting the offstage Cornwall death
    # out of the blinding scene into its own event; adding E_rescue_
    # attempt_too_late as a distinct event between E_edmund_confesses
    # and E_cordelia_hanged).
    min_event_count=11,
    max_event_count=16,
    # A16-SP3 — rapid escalation: the anagnorisis-reconciliation
    # (τ_s=28) is immediately followed by the battle (τ_s=29),
    # capture (τ_s=30), the cascade of deaths at τ_s=32–38. The
    # seven deaths in the end phase are structurally the fastest
    # catastrophe cluster in the corpus.
    pacing_preference=PACING_RAPID_ESCALATION,
    annotation=(
        "The unbinding. Lear's anagnorisis — the reconciliation with "
        "Cordelia at τ_s=28 — is the turning of the whole play from "
        "suffering-and-recognition to catastrophe-and-release. From "
        "the moment Lear recognizes Cordelia's love, every subsequent "
        "beat is a death or a death-adjacent reversal: the battle "
        "(τ_s=29) in which the French lose, the capture of Lear "
        "and Cordelia (τ_s=30), Edmund's hanging order (τ_s=31), "
        "Edgar's anonymous trial-by-combat victory (τ_s=32), the "
        "collateral offstage deaths (Regan τ_s=33, Goneril τ_s=34), "
        "Edmund's deathbed confession-and-reversal (τ_s=35, the "
        "corpus's first post-main parallel chain step), and the "
        "four final deaths at τ_s=36–38: Cordelia hanged offstage "
        "(the rescue arrives too late), Gloucester offstage (joy-"
        "shock on Edgar's revelation), Lear onstage with Cordelia's "
        "body (the catharsis site), Edmund offstage (duel wounds). "
        "Four offstage deaths in one phase is the corpus's densest "
        "site of the OQ-AP15 absent-character catharsis shape."
    ),
)


# ============================================================================
# Characters — A5
# ============================================================================
#
# Five ArCharacter records. Three with `is_tragic_hero=True` —
# Lear, Gloucester, Cordelia. Two with `is_tragic_hero=False` —
# Edmund (antagonist with partial redemption, not classical tragic
# hero) and Edgar (survivor-restorer, classical comic-ending shape
# within the tragedy).
#
# Having five ArCharacters (vs Hamlet's three) reflects Lear's
# double-plot structure and the A13 instrumental-kind forcing
# requirements (OQ-AP14 needs Edmund + Edgar as the wielders of
# the two instrumental chains on Gloucester).
#
# Three-tragic-hero pressure on OQ-AP6 (sketch-03 closure) — Lear
# is the second corpus encoding to meet the criterion. Hamlet's
# three tragic heroes were the forcing case; Lear confirms the
# closure generalizes. OQ-AP6 stays CLOSED (no new pressure).

AR_LEAR = ArCharacter(
    id="ar_lear",
    name="Lear",
    character_ref_id="lear",
    hamartia_text=(
        "Demand for the performance of love in place of its "
        "substance. Lear's love-test stages a scheme where "
        "declarations of love determine inheritance shares; what he "
        "wants is not evidence of love but the performance of it, "
        "scaled to the portions he plans to grant. Cordelia refuses "
        "on principle — 'love, and be silent' — and Lear reads the "
        "refusal as absence. His hamartia is not cruelty but "
        "miscalibration: he stakes the kingdom's stability and his "
        "own retirement on a test whose measurement structure he "
        "cannot see is broken. The test rewards flattery by "
        "construction and punishes honesty for the same reason. 'How "
        "sharper than a serpent's tooth it is / To have a thankless "
        "child!' is Lear's own later diagnosis, but the thanklessness "
        "he received (from Goneril and Regan) is what his test was "
        "designed to extract. The world gives him back what he asked "
        "for — the performance of love — and when it turns out that "
        "performance and love were different, it is too late. "
        "Classical Aristotelian hamartia: an error of judgment about "
        "what can be measured, not a moral failing."
    ),
    is_tragic_hero=True,
)

AR_GLOUCESTER = ArCharacter(
    id="ar_gloucester",
    name="Gloucester",
    character_ref_id="gloucester",
    hamartia_text=(
        "Credulity — specifically, the inability to hold his sons' "
        "characters in view when presented with documentary evidence "
        "of betrayal. Gloucester accepts Edmund's forged letter "
        "without demanding corroboration; he accepts Edmund's staged "
        "wound as further evidence; he sends for Edgar's blood with "
        "no more deliberation than the love-test required of Lear. "
        "His hamartia parallels Lear's: a failure to distinguish "
        "surface from substance under the pressure of a test he did "
        "not design and does not understand he is being given. Edmund "
        "wields the test; Gloucester fails it — 'these late eclipses "
        "in the sun and moon portend no good to us' is Gloucester "
        "reading patterns he has constructed his own vulnerability "
        "to. The blinding at Cornwall's hands is the outward sign of "
        "the inward failure; his anagnorisis at the same scene (Regan "
        "reveals it was Edmund) completes the pattern. Structurally: "
        "a second tragic hero whose arc runs in parallel with Lear's, "
        "both old men who trust the wrong child and ruin the right "
        "one."
    ),
    is_tragic_hero=True,
)

AR_CORDELIA = ArCharacter(
    id="ar_cordelia",
    name="Cordelia",
    character_ref_id="cordelia",
    hamartia_text=(
        "Truth-telling where the rhetorical frame requires flattery. "
        "Cordelia's 'Nothing, my lord' is principled and correct — "
        "her sisters' declarations ARE false, and the love-test as "
        "structured cannot extract the love she actually holds. But "
        "the test's participants do not know that the test is "
        "broken; they only see one daughter who answered and two who "
        "refused. Cordelia's hamartia is not her honesty but her "
        "decision to deploy that honesty at a moment when the "
        "alternative — a minimal, knowingly-inadequate, face-saving "
        "speech — was available and would have preserved her "
        "father's stake in her. She reads the test as a test of "
        "love; her sisters read it as a test of rhetorical "
        "performance; her father designed it as the latter but "
        "will punish her for failing the former. Her refusal is "
        "structurally admirable and narratively catastrophic — 'I "
        "cannot heave my heart into my mouth' stakes everything on a "
        "reading of the scene her father does not share. She returns "
        "with an army and saves Lear emotionally before being hanged "
        "offstage in a prison-cell at Edmund's order. Her tragic-hero "
        "status rests on the hamartia-anagnorisis shape: her early "
        "refusal produces the cascade; her return produces the "
        "recognition; her death is the catharsis."
    ),
    is_tragic_hero=True,
)

AR_EDMUND = ArCharacter(
    id="ar_edmund",
    name="Edmund",
    character_ref_id="edmund",
    hamartia_text=(
        "The bastard's inverted primogeniture. Edmund's opening "
        "soliloquy ('Thou, nature, art my goddess') rejects the "
        "convention that excludes him from inheritance and resolves "
        "to take what law will not give him. His hamartia is not the "
        "ambition — many characters in the corpus have ambition — "
        "but the instrumental wielding of everyone else's trust to "
        "serve it. He forges Edgar's letter; he stages his own "
        "wound; he betrays his father to Cornwall; he seduces both "
        "Goneril and Regan; he orders Cordelia hanged. His deathbed "
        "reversal ('some good I mean to do, despite of mine own "
        "nature') is partial and late — he names the order against "
        "Cordelia, but the rescue arrives after the hanging. "
        "Structurally: a non-classical tragic hero. Aristotle's "
        "tragic hero falls from high estate through a flaw of "
        "judgment; Edmund rises from low estate through a flaw of "
        "will and is cut down by the justice of the trial-by-combat. "
        "`is_tragic_hero=False` — Edmund is the antagonist whose "
        "partial redemption stops short of the tragic-hero shape. "
        "His arc is authored primarily to serve the A13 instrumental-"
        "kind relations; the deathbed-reversal chain step "
        "`AR_STEP_EDMUND_CONFESSES` carries the partial redemption."
    ),
    is_tragic_hero=False,
)

AR_EDGAR = ArCharacter(
    id="ar_edgar",
    name="Edgar",
    character_ref_id="edgar",
    hamartia_text=(
        "Credulity — the same hamartia as his father, exercised "
        "briefly. Edgar believes Edmund's warning without demanding "
        "corroboration and flees; the flight grounds the entire "
        "Gloucester-subplot middle-phase. But Edgar's arc is "
        "restorative, not tragic: he assumes the Poor Tom disguise, "
        "leads his blinded father through therapeutic deception, "
        "challenges Edmund in anonymous trial-by-combat, reveals "
        "himself to Gloucester in time for the old man to die of "
        "joy, and survives to rule (Folio) or to advise Albany's "
        "rule (Q1). `is_tragic_hero=False` — the arc is too "
        "restorative for tragic-hero status. Edgar is authored as "
        "an ArCharacter primarily for the A13 relations: he is the "
        "foil to Edmund (`AR_EDGAR_EDMUND_FOIL`) and the therapeutic-"
        "polarity wielder in the second instrumental relation on "
        "Gloucester (`AR_EDGAR_GLOUCESTER_INSTRUMENTAL`). His "
        "reconciliation with Gloucester is offstage and reported; "
        "his survival into Act V makes him the closest thing the "
        "tragedy has to a comic-ending figure."
    ),
    is_tragic_hero=False,
)


# ============================================================================
# Anagnorisis chain — A11 (sketch-02) + A14 (sketch-03)
# ============================================================================
#
# Two steps, both `step_kind="parallel"`:
#
# 1. AR_STEP_GLOUCESTER_BLINDING (τ_s=23). Gloucester's character-
#    level anagnorisis at the blinding: Regan reveals it was Edmund
#    who betrayed him. Different character from main (ar_gloucester
#    vs ar_lear), non-precipitating (Gloucester's recognition does
#    not cause Lear's).
# 2. AR_STEP_EDMUND_CONFESSES (τ_s=35). Edmund's deathbed reversal:
#    reveals the hanging order and tries to retract it. Different
#    character from main (ar_edmund vs ar_lear), non-precipitating
#    (Edmund's confession does not cause Lear's reconciliation —
#    that has already happened). **Post-main parallel step.**
#
# Main anagnorisis: E_lear_cordelia_reconcile (τ_s=28) on Lear
# himself. AR_LEAR_MYTHOS names anagnorisis_character_ref_id=
# "ar_lear" (A14). No staging steps — Lear's progression toward
# reconciliation is emotional rather than epistemic, and the
# dialect's `staging` step_kind admits only epistemic waypoints.
# The gap is banked as OQ_LEAR_1 (emotional-vs-epistemic staging
# distinction) below.
#
# Edmund's deathbed step is the corpus's first post-main parallel
# step. A14 invariants do not forbid post-main placement for
# `step_kind="parallel"` (only staging steps must precede main);
# the structural shape is legal but unprecedented. Session 5's
# probe run will test whether the dialect reads it naturally or
# demands a distinguishing pre-main / post-main sub-axis.

AR_STEP_GLOUCESTER_BLINDING = ArAnagnorisisStep(
    id="arstep_gloucester_blinding",
    event_id="E_cornwall_regan_blind_gloucester",
    character_ref_id="ar_gloucester",
    step_kind=STEP_KIND_PARALLEL,
    precipitates_main=False,
    annotation=(
        "Gloucester's anagnorisis: at the same scene where Cornwall "
        "blinds him, Regan reveals that it was Edmund who betrayed "
        "him. Gloucester recognizes — too late, too physically — "
        "that his credulity about the forged letter + staged wound "
        "ruined the son he loved. 'O my follies! then Edgar was "
        "abused.' The outward and inward recognitions are compressed "
        "into one substrate beat: his eyes are put out as he "
        "acquires KNOWN(it-was-Edmund). Parallel step, different "
        "character from main (ar_gloucester vs ar_lear), non-"
        "precipitating: Gloucester's recognition is structurally "
        "independent of Lear's — the two fathers' parallel anagnorises "
        "are one of the play's famous mirrorings, but neither causes "
        "the other. Structurally analogous to Claudius-at-prayer in "
        "Hamlet (different-character parallel-step to a sole "
        "protagonist main), but with opposite occupant role: Claudius "
        "is antagonist recognizing his own bankruptcy; Gloucester is "
        "parallel-protagonist recognizing his own error."
    ),
)

AR_STEP_EDMUND_CONFESSES = ArAnagnorisisStep(
    id="arstep_edmund_confesses",
    event_id="E_edmund_confesses",
    character_ref_id="ar_edmund",
    step_kind=STEP_KIND_PARALLEL,
    precipitates_main=False,
    annotation=(
        "Edmund's deathbed reversal: mortally wounded by Edgar in "
        "trial-by-combat, Edmund names the hanging order against "
        "Cordelia and tries — too late — to retract it. 'Some good "
        "I mean to do, despite of mine own nature.' The partial "
        "redemption is characterological rather than epistemic; "
        "Edmund has known his acts throughout, and the 'despite of "
        "mine own nature' names the recognition that his nature was "
        "itself the hamartia. Parallel step, different character "
        "from main, non-precipitating. **Post-main** (τ_s=35 > "
        "τ_s=28): the first post-main parallel step in the corpus. "
        "Lear's main anagnorisis has already landed when Edmund's "
        "comes; Edmund's reversal does not feed back into Lear's "
        "recognition. Structurally: the antagonist's belated moral "
        "awareness lands too late to prevent the catastrophe it "
        "enabled. Cordelia dies because the rescue Edgar dispatches "
        "reaches the prison after the hanging. The post-main "
        "placement is what makes the pathos work — if Edmund's "
        "confession came pre-main it would be redemption; post-main "
        "it is futility rendered as structural irony."
    ),
)


# ============================================================================
# Character-arc relations — A13 (sketch-03) + OQ-AP14 pressure
# ============================================================================
#
# Four pairwise ArCharacterArcRelation records. Two canonical kinds
# (parallel, foil) match sketch-03's corpus-shipped vocabulary; two
# non-canonical records use kind="instrumental", authored per
# sketch-03's canonical-plus-open discipline at severity `noted`.
#
# The two instrumental relations share a target (Gloucester) and
# differ in moral polarity. This is the substrate signature OQ-AP14
# pressure was banked against: the dialect's `parallel / mirror /
# foil` vocabulary does not admit the structural shape "character X
# wields an instrument-chain against character Y". Sketch-03's
# canonical-plus-open discipline admits `kind="instrumental"` at
# severity noted; probe-side pressure will test whether the fourth
# canonical kind should be added, whether a polarity sub-axis
# (malicious/therapeutic/sanctioned) should accompany it, or
# whether the structural shape is better carried elsewhere (a new
# record type, or substrate-only).

AR_LEAR_GLOUCESTER_PARALLEL = ArCharacterArcRelation(
    id="arc_lear_gloucester_parallel",
    kind=ARC_RELATION_PARALLEL,
    character_ref_ids=("ar_lear", "ar_gloucester"),
    mythos_id="ar_lear",
    over_event_ids=(
        # Both fathers' pre-peripeteia misjudgments
        "E_cordelia_disinherited",           # Lear's (τ_s=4)
        "E_edmund_shows_gloucester",         # Gloucester's (τ_s=9)
        "E_edmund_stages_wound",             # Gloucester's reinforcement (τ_s=11)
        # Both fathers' peripeteiai
        "E_goneril_strips_retinue",          # Lear's (τ_s=14)
        "E_cornwall_regan_blind_gloucester", # Gloucester's (τ_s=23; bound to
                                             # Gloucester's parallel chain-step
                                             # AR_STEP_GLOUCESTER_BLINDING)
        # Their convergence — the heath meeting
        "E_lear_meets_blind_gloucester",     # τ_s=27 (denouement)
        # Both fathers' deaths
        "E_gloucester_dies",                 # τ_s=36 (offstage, reported)
        "E_lear_dies",                       # τ_s=38 (onstage, grief)
    ),
    annotation=(
        "Lear and Gloucester run structurally parallel arcs: both "
        "old men misread a test-of-loyalty (Lear's love-test; "
        "Gloucester's forged-letter-plus-staged-wound), both "
        "misattribute the loyal child's silence/flight as betrayal "
        "and the unloyal child's performance/framing as devotion, "
        "both undergo peripeteia when the ingrate children turn on "
        "them (Goneril's stripping; Cornwall's blinding), both have "
        "anagnorises in which they recognize the inversion, both "
        "reconcile with the wronged child, and both die at the end "
        "— one onstage with the child's body, one offstage of "
        "joy-shock at recognition. The parallelism is the structural "
        "ground of the play's title-and-subtitle shape: Lear's "
        "tragedy is one part; Gloucester's tragedy is the other "
        "part; the play asks the audience to read each through the "
        "other. Classical Aristotelian unity-of-action is "
        "deliberately not asserted on this mythos "
        "(`asserts_unity_of_action=False`) — the two parallel arcs "
        "are one thematic action but not one causal action, and "
        "the dialect carries this distinction via the parallel A13 "
        "rather than subordinating one plot to the other."
    ),
)

AR_EDGAR_EDMUND_FOIL = ArCharacterArcRelation(
    id="arc_edgar_edmund_foil",
    kind=ARC_RELATION_FOIL,
    character_ref_ids=("ar_edgar", "ar_edmund"),
    mythos_id="ar_lear",
    over_event_ids=(
        # Their pre-play standing
        "E_gloucester_family",       # (τ_s=-25, legitimate/illegitimate)
        "E_edmund_resolves_to_plot", # (τ_s=-5, Edmund's opening posture)
        # Edmund's ascent via instrument
        "E_edmund_forges_letter",
        "E_edmund_shows_gloucester",
        "E_edmund_warns_edgar",
        "E_edmund_stages_wound",
        # Edgar's flight + disguise
        "E_edgar_flees",
        "E_edgar_becomes_poor_tom",
        # Their parallel therapeutic/malicious wielding of Gloucester
        "E_gloucester_suicide_attempt",
        # The reversal: Edgar's trial-by-combat victory
        "E_edgar_defeats_edmund",
        "E_edmund_confesses",
    ),
    annotation=(
        "Edgar and Edmund are structurally opposed brothers: "
        "legitimate / illegitimate, honest / cunning, loyal son / "
        "forger of letters, restoring the father's hope via staged "
        "Dover deception / ruining the father's life via staged "
        "wound-deception. Both use instruments on Gloucester; the "
        "polarity inversion is the foil's content. Edgar's Poor Tom "
        "disguise is concealment-for-preservation; Edmund's "
        "machinations are concealment-for-destruction. Both brothers "
        "end the play in the scene of Edmund's death: Edgar as "
        "victor-avenger-revealer, Edmund as dying-confessor. The "
        "reveal — 'My name is Edgar, and thy father's son' — "
        "completes the foil: the hidden-legitimate and the known-"
        "illegitimate come back into symmetric view, and the law "
        "(trial-by-combat sanctions the killing) restores what "
        "primogeniture excluded. A13's `foil` kind ships canonical "
        "at sketch-03; Hamlet-Claudius was the first corpus foil "
        "(will-to-act vs will-to-retain); Edgar-Edmund is the second."
    ),
)

AR_EDMUND_GLOUCESTER_INSTRUMENTAL = ArCharacterArcRelation(
    id="arc_edmund_gloucester_instrumental",
    kind="instrumental",  # non-canonical; sketch-03 admits at severity=noted
    character_ref_ids=("ar_edmund", "ar_gloucester"),
    mythos_id="ar_lear",
    over_event_ids=(
        # The three-beat instrumental chain
        "E_edmund_forges_letter",    # forgery fact (τ_s=8)
        "E_edmund_shows_gloucester", # Gloucester BELIEVES(plots_against) (τ_s=9)
        "E_edmund_stages_wound",     # reinforcement — physical evidence (τ_s=11)
        # Second branch: Edmund's subsequent betrayal of Gloucester
        "E_gloucester_sends_lear_to_dover", # Edmund informs Cornwall (τ_s=22)
        # The instrument's target undone — anagnorisis + death
        "E_cornwall_regan_blind_gloucester", # Gloucester blinded as direct
                                             # consequence of Edmund's
                                             # informing (τ_s=23)
    ),
    annotation=(
        "Edmund wields Gloucester's trust as an instrument of his "
        "own advancement. The three-beat chain: (1) forge a letter "
        "purporting to be from Edgar plotting against Gloucester "
        "(world-level `forged_letter(edmund, edgar)` at τ_s=8); (2) "
        "show the letter to Gloucester with feigned reluctance, "
        "causing Gloucester to acquire BELIEVED(plots_against(edgar, "
        "gloucester)) — the instrument's first payload (τ_s=9); (3) "
        "stage a self-inflicted wound whose world-true existence "
        "promotes Gloucester's belief from BELIEVED toward KNOWN "
        "(τ_s=11). A fourth scene extends the chain: Edmund observes "
        "his father's loyalty to Lear (E_gloucester_sends_lear_to_"
        "dover, τ_s=22) and informs Cornwall, whose retaliation "
        "blinds Gloucester at τ_s=23 — the instrument's ultimate "
        "consequence.\n\n"
        "`kind=\"instrumental\"` is non-canonical at sketch-03. "
        "The relation's structural content is not parallel (the two "
        "arcs are not running in parallel — one is wielding the "
        "other), not mirror (the arcs are not inverted over shared "
        "pressure — they are asymmetric by construction), and not "
        "foil (the arcs are not structurally opposed over shared "
        "pressure — one is causing the other). A fourth canonical "
        "kind is pressured; see `OQ_AP14_FINDING` below. Polarity: "
        "malicious — Edmund wields Gloucester's belief to ruin him.\n\n"
        "The instrumental relation is DIRECTIONAL: the "
        "`character_ref_ids` tuple is ordered (wielder, target), not "
        "symmetric like parallel/mirror/foil. Sketch-03's A13 does "
        "not distinguish directional from symmetric relations at the "
        "field-shape level; this encoding treats tuple order as "
        "carrying the wielder→target direction, and the probe may "
        "propose formalizing that convention."
    ),
)

AR_EDGAR_GLOUCESTER_INSTRUMENTAL = ArCharacterArcRelation(
    id="arc_edgar_gloucester_instrumental",
    kind="instrumental",  # non-canonical; sketch-03 admits at severity=noted
    character_ref_ids=("ar_edgar", "ar_gloucester"),
    mythos_id="ar_lear",
    over_event_ids=(
        "E_edgar_leads_blind_gloucester",  # (τ_s=24)
        "E_gloucester_suicide_attempt",     # (τ_s=25) — staged cliff fall
    ),
    annotation=(
        "Edgar wields Gloucester's despair as an instrument of his "
        "healing. The inverse polarity of Edmund's instrumental "
        "relation on the same target: where Edmund's forged letter "
        "moves Gloucester toward ruin via false belief, Edgar's "
        "staged Dover cliff-fall moves Gloucester toward acceptance "
        "via false belief. The instrument-shape is identical — a "
        "fabricated world state (letter, or staged fall) that "
        "induces a belief in the target that world-state does not "
        "warrant — but the outcomes are opposite: Gloucester's "
        "belief about Edgar's betrayal leads to peripeteia; "
        "Gloucester's belief that he fell from the cliff and "
        "survived leads to 'bear free and patient thoughts.'\n\n"
        "Substrate predicates parallel exactly: `forged_letter`, "
        "`staged_wound`, `staged_cliff_fall` are all world-true "
        "facts (the instruments exist); Gloucester's belief in each "
        "instrument's authorized reading is what the instrument "
        "produces. The symmetry is not decorative — the play asks "
        "the audience to read the second chain through the first, "
        "and Edgar's 'thy life's a miracle' (IV.vi) is the explicit "
        "textual marker.\n\n"
        "Same non-canonical `kind=\"instrumental\"` as above. The "
        "two relations TOGETHER are the forcing ground for OQ-AP14 "
        "— one instrumental kind is noteworthy; two instrumental "
        "kinds on the same target with opposite polarity is the "
        "dialect-layer signature of a structural shape the canonical "
        "vocabulary cannot express. Polarity: therapeutic — Edgar "
        "wields Gloucester's belief to heal him."
    ),
)

AR_LEAR_CHARACTER_ARC_RELATIONS = (
    AR_LEAR_GLOUCESTER_PARALLEL,
    AR_EDGAR_EDMUND_FOIL,
    AR_EDMUND_GLOUCESTER_INSTRUMENTAL,
    AR_EDGAR_GLOUCESTER_INSTRUMENTAL,
)


# ============================================================================
# Co-presence requirements — A15-SE2 (sketch-04)
# ============================================================================
#
# Three hard co-presence requirements naming load-bearing character
# pairings. Each names characters whose simultaneous presence at
# substrate events within a named phase is *required* by the dialect
# for the mythos's structural integrity — not merely related via A13.

AR_LEAR_CO_PRESENCE = (
    ArCoPresenceRequirement(
        id="copres_lear_cordelia_end",
        character_ref_ids=("ar_lear", "ar_cordelia"),
        phase_id="ph_lear_end",
        # The reconciliation (τ_s=28) + the catastrophe-scene where
        # Lear enters with Cordelia's body (τ_s=37). Two events.
        min_count=2,
    ),
    ArCoPresenceRequirement(
        id="copres_lear_gloucester_middle",
        character_ref_ids=("ar_lear", "ar_gloucester"),
        phase_id="ph_lear_middle",
        # E_gloucester_meets_poor_tom (τ_s=20; both in the hovel
        # scene though Gloucester doesn't recognize the others yet)
        # + E_lear_meets_blind_gloucester (τ_s=27, denouement). Two
        # events.
        min_count=2,
    ),
    ArCoPresenceRequirement(
        id="copres_edmund_gloucester_beginning",
        character_ref_ids=("ar_edmund", "ar_gloucester"),
        phase_id="ph_lear_beginning",
        # E_edmund_shows_gloucester (τ_s=9) + E_edmund_stages_wound
        # (τ_s=11) — both instrumental-chain deployment scenes.
        # Required for the A13 instrumental relation to have
        # structural footing.
        min_count=2,
    ),
)


# ============================================================================
# Audience-knowledge constraints — A15-SE3 (sketch-04)
# ============================================================================
#
# Three load-bearing pieces of dramatic-irony knowledge. Lear's
# dramatic irony density is high (the Kent-disguise, the Edgar-
# disguise, the hanging order in flight); three representative
# constraints cover the key sites.

AR_LEAR_AUDIENCE_KNOWLEDGE = (
    ArAudienceKnowledgeConstraint(
        id="ak_edmund_is_a_forger",
        subject="edmund_forged_letter_against_edgar",
        # Audience knows at τ_s=8 — the forgery event itself. Grounds
        # the entire Gloucester-subplot reading, especially the
        # Edgar-flight and the staged-wound scenes which would
        # otherwise read as Edgar's actual attack on Edmund.
        latest_τ_s=8,
        source_event_id="E_edmund_forges_letter",
    ),
    ArAudienceKnowledgeConstraint(
        id="ak_edgar_is_poor_tom",
        subject="edgar_disguised_as_poor_tom",
        # Audience knows at τ_s=19 — the disguise-adoption event.
        # Grounds the hovel scenes (Gloucester and Lear both fail
        # to recognize Edgar for several scenes; the audience's
        # knowledge frames every line Edgar speaks as Poor Tom as
        # dramatic irony).
        latest_τ_s=19,
        source_event_id="E_edgar_becomes_poor_tom",
    ),
    ArAudienceKnowledgeConstraint(
        id="ak_edmund_orders_cordelia_hanged",
        subject="edmund_has_ordered_cordelia_hanged",
        # Audience knows at τ_s=31 — the order event. Grounds the
        # trial-by-combat scene (τ_s=32–35) and the confession-and-
        # rescue attempt (τ_s=35–36). The audience's knowledge of
        # the running clock is structurally the whole end phase's
        # tension: every line of the duel is read against "Cordelia
        # is being hanged while this happens."
        latest_τ_s=31,
        source_event_id="E_edmund_orders_cordelia_hanged",
    ),
)


# ============================================================================
# Mythos — A1
# ============================================================================

AR_LEAR_MYTHOS = ArMythos(
    id="ar_lear",
    title="King Lear",
    action_summary=(
        "The king, retiring, offers the kingdom to the daughters in "
        "proportion to their declarations of love. Two flatter, one "
        "refuses; the refuser is disinherited; the loyal counselor "
        "who objects is banished. In parallel, Gloucester's bastard "
        "son Edmund forges a letter implicating his legitimate brother "
        "Edgar in a plot against their father; Edgar flees and "
        "assumes a mad beggar's disguise. The flattering daughters, "
        "receiving the halves of the kingdom, strip their father's "
        "retinue to nothing; Lear flees into a storm on the heath. "
        "Gloucester, who helped send Lear to meet Cordelia's landed "
        "French army at Dover, is betrayed by Edmund to Cornwall, "
        "who plucks out his eyes; a servant fatally wounds Cornwall "
        "in turn. The blinded Gloucester, led by his disguised son "
        "through therapeutic deception at Dover, meets Lear on the "
        "heath, and Cordelia finds her father; their reconciliation "
        "is the anagnorisis. The French lose the battle; Lear and "
        "Cordelia are captured; Edmund sends instructions to hang "
        "Cordelia. Edgar challenges Edmund in anonymous trial-by-"
        "combat and mortally wounds him; Edmund, dying, confesses "
        "the order and tries to rescind it, too late. Goneril poisons "
        "Regan out of jealousy over Edmund and then kills herself; "
        "Gloucester dies offstage of joy at recognizing Edgar; Lear "
        "enters carrying Cordelia's body; he dies over her, believing "
        "(perhaps) that she still breathes. Edmund dies of his duel "
        "wounds. Edgar, Albany, and Kent survive the catastrophe. "
        "The kingdom is restored through the catastrophe; the "
        "characters are not."
    ),
    central_event_ids=(
        # Pre-play
        "E_lear_reigns",
        "E_gloucester_family",
        "E_edmund_resolves_to_plot",
        # Beginning
        "E_lear_announces_division",
        "E_love_test_goneril",
        "E_love_test_regan",
        "E_love_test_cordelia",
        "E_cordelia_disinherited",
        "E_kent_banished",
        "E_france_marries_cordelia",
        "E_kingdom_divided",
        "E_edmund_forges_letter",
        "E_edmund_shows_gloucester",
        "E_edmund_warns_edgar",
        "E_edmund_stages_wound",
        "E_edgar_flees",
        # Middle
        "E_lear_at_gonerils",
        "E_kent_returns_disguised",
        "E_goneril_strips_retinue",
        "E_lear_to_regans",
        "E_regan_also_strips",
        "E_lear_flees_to_heath",
        "E_storm_on_heath",
        "E_edgar_becomes_poor_tom",
        "E_gloucester_meets_poor_tom",
        "E_lear_mock_trial",
        "E_gloucester_sends_lear_to_dover",
        "E_cornwall_regan_blind_gloucester",
        "E_edgar_leads_blind_gloucester",
        "E_gloucester_suicide_attempt",
        "E_cordelia_returns",
        "E_lear_meets_blind_gloucester",
        # End
        "E_lear_cordelia_reconcile",
        "E_battle",
        "E_lear_cordelia_captured",
        "E_edmund_orders_cordelia_hanged",
        "E_edgar_defeats_edmund",
        "E_regan_dies",
        "E_goneril_suicide",
        "E_edmund_confesses",
        "E_cordelia_hanged",
        "E_gloucester_dies",
        "E_lear_enters_with_cordelia",
        "E_lear_dies",
        "E_edmund_dies",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=(PH_BEGINNING, PH_MIDDLE, PH_END),
    # Complication: first event of middle — the lodging at Goneril's
    # that brings Lear and his ingrate daughter together under the
    # terms of the division. Parallels Hamlet's E_mousetrap_
    # performance (first middle, the act that commits to the
    # consequences of the pre-established premises).
    complication_event_id="E_lear_at_gonerils",
    # Denouement: last event of middle — the heath meeting of Lear
    # and the blinded Gloucester. Both broken fathers in one frame;
    # the scene sets the emotional register of the reconciliation
    # that opens the end phase.
    denouement_event_id="E_lear_meets_blind_gloucester",
    # A12 — BINDING_SEPARATED with distance 14. Widest in the corpus
    # (Hamlet: 9; Oedipus: 5; Macbeth: coincident). OQ_AP7 is now
    # pressured by two independent encodings; see OQ_AP7_FINDING.
    #
    # Peripeteia: Goneril strips Lear's retinue. The reversal-by-own-
    # action: Lear's choice to stake the kingdom on flattery has
    # turned against him — the daughter he elevated on rhetorical
    # performance is now reducing him to nothing. Strict Aristotle:
    # peripeteia as change-of-situation-into-the-opposite, produced
    # by the hero's own action.
    peripeteia_event_id="E_goneril_strips_retinue",
    # Anagnorisis: Lear recognizes Cordelia. The retraction of the
    # false held-belief planted at the love-test scene (the substrate's
    # `remove_held` effect at E_lear_cordelia_reconcile materializes
    # the recognition at substrate scope). 'I am a very foolish fond
    # old man... Do not laugh at me; for, as I am a man, I think this
    # lady to be my child Cordelia.'
    anagnorisis_event_id="E_lear_cordelia_reconcile",
    # Unity of action: **asserts=False** — corpus first. The double
    # plot is thematically unified (two old fathers misled about
    # their children) but causally parallel — the two arcs run in
    # structural parallel without subordination, and converge at
    # Dover only partially. Classical Aristotelian unity requires one
    # unified action; Shakespeare's double-plot here is the canonical
    # departure. The A13 parallel relation
    # (AR_LEAR_GLOUCESTER_PARALLEL) carries the thematic-unity
    # claim; unity_of_action=False carries the causal-non-unity
    # claim. See OQ_LEAR_2 below.
    asserts_unity_of_action=False,
    asserts_unity_of_time=False,
    asserts_unity_of_place=False,
    aims_at_catharsis=True,
    characters=(AR_LEAR, AR_GLOUCESTER, AR_CORDELIA, AR_EDMUND, AR_EDGAR),
    # A11 + A14 — two-step chain, both parallel kind. No staging
    # step (Lear's progression to main anagnorisis is emotional, not
    # epistemic). AR_STEP_EDMUND_CONFESSES is **post-main** — the
    # first post-main parallel step in the corpus.
    anagnorisis_chain=(
        AR_STEP_GLOUCESTER_BLINDING,
        AR_STEP_EDMUND_CONFESSES,
    ),
    # A12 — SEPARATED with distance 14 (τ_s=14 → τ_s=28). Corpus
    # widest.
    peripeteia_anagnorisis_binding=BINDING_SEPARATED,
    # A14 — the character whose recognition lands at
    # anagnorisis_event_id. Lear himself. No staging steps require
    # this field for their verification; it is still set for A7.11
    # derivation consistency on any future staging authoring.
    anagnorisis_character_ref_id="ar_lear",
    # A15-SE2 — three hard co-presence requirements.
    co_presence_requirements=AR_LEAR_CO_PRESENCE,
    # A15-SE3 — three audience-knowledge timing constraints.
    audience_knowledge_constraints=AR_LEAR_AUDIENCE_KNOWLEDGE,
    # A16-SP1 — soft tonal preference. 'tragic-pure' captures the
    # unrelieved pathos of the end (the pieta shape of Lear carrying
    # Cordelia's body, the absence of any redeeming social order
    # restoration within the mythos). The middle's ironies (Fool's
    # commentary, Kent-as-Caius, Edgar-as-Poor-Tom) are present but
    # swallowed by the end's catastrophe. Contrast Hamlet's
    # 'tragic-with-irony' where the reflexive commentary structures
    # the register throughout.
    tonal_register=TONAL_REGISTER_TRAGIC_PURE,
    # A16-SP2 — soft preference for wide peripeteia-anagnorisis
    # distance. The actual A12 binding is SEPARATED with distance 14
    # — corpus widest. The preference matches: Lear's emotional shape
    # lives in the fourteen τ_s of progressive loss between the
    # stripping of his retinue and the reconciliation with Cordelia.
    binding_distance_preference=BINDING_PREF_WIDE,
)


# ============================================================================
# Probe-surface findings — OQ-AP14 + OQ-AP15 (sketch-04 banked);
# re-surface of OQ_AP7; two Lear-specific OQs banked
# ============================================================================
#
# Prose constants for reference by future probe runs and sketch-04+
# design. The dialect has no typed record for probe findings at
# encoding scope; these constants carry what the encoding surfaced,
# structured for future extraction.

OQ_AP14_FINDING = (
    "OQ-AP14 — Instrumental-kind ArCharacterArcRelation. Authored as "
    "pressure by this encoding (second-site after Hamlet's single-"
    "candidate surface in Session 6). Lear authors TWO relations "
    "with the non-canonical kind `instrumental`, both operating on "
    "the same target (Gloucester) with opposite moral polarity: "
    "`AR_EDMUND_GLOUCESTER_INSTRUMENTAL` (malicious; forged-letter + "
    "staged-wound chain) and `AR_EDGAR_GLOUCESTER_INSTRUMENTAL` "
    "(therapeutic; staged Dover cliff-fall). Sketch-03's canonical-"
    "plus-open discipline admits both at severity `noted`.\n\n"
    "The structural content the dialect admits only as noncanonical: "
    "(a) directional relation (wielder → target), distinct from the "
    "symmetric shapes of parallel/mirror/foil; (b) instrument-"
    "mediated causation, where the A-on-B effect travels through a "
    "world-state artifact rather than character-to-character "
    "presence; (c) polarity (malicious/therapeutic/sanctioned), the "
    "sub-axis Edgar-vs-Edmund exercises with an instrument-shape "
    "that is structurally identical across polarities. The two Lear "
    "instrumental relations exhibit all three (directional, "
    "artifact-mediated, polarity-inverted); Hamlet's single candidate "
    "(Claudius-Laertes via the duel-plot) exhibits (a) and (b) but "
    "not the polarity-inversion. Lear's polarity-inversion is the "
    "dialect-scope signature the canonical vocabulary cannot "
    "structurally name.\n\n"
    "Candidate canonical extensions, in order of structural weight:\n"
    "1. `instrumental` as a fourth canonical kind, flat (no polarity "
    "   distinction) — matches the current three-kind structure and "
    "   admits Hamlet's + Lear's four instrumental candidates "
    "   uniformly.\n"
    "2. `instrumental` plus a polarity sub-axis "
    "   `{malicious, therapeutic, sanctioned}` — captures Lear's "
    "   polarity-inversion and Hamlet's sanctioned-revenge reading "
    "   (Hamlet wielding the Mousetrap as therapeutic-for-himself "
    "   instrument, distinct from Claudius wielding Laertes).\n"
    "3. A new record type `ArInstrumentalRelation` separate from "
    "   A13 — captures directional + artifact-mediated + polarity in "
    "   its own shape; leaves A13 purely for symmetric relations.\n\n"
    "Session 5's live probe will test which extension (if any) the "
    "reader finds. Session 6's re-probe under any sketch-05 "
    "extension will verify. Pre-sketch forcing-function recorded "
    "here for reader's reference."
)

OQ_AP15_FINDING = (
    "OQ-AP15 — Absent-character catharsis. Authored as pressure by "
    "this encoding (second-site after Hamlet's single-sentence "
    "surface in Session 6). Lear is the corpus's densest site of "
    "the offstage-death shape:\n"
    "- `E_cordelia_hanged` (τ_s=36): world effects only, ZERO observer "
    "  projections at this event. The catharsis lands through Lear's "
    "  entrance carrying her body at `E_lear_enters_with_cordelia` "
    "  (τ_s=37) — the first moment any named character observes "
    "  dead(cordelia). A substrate absence-of-observation shape at "
    "  the moment of death; the death's world-fact exists, the "
    "  dialect's ArCharacter-bound catharsis shape is satisfied "
    "  (Cordelia has an ArCharacter record with is_tragic_hero=True), "
    "  but the substrate signature of the event is distinct from "
    "  deaths whose defining event carries observer projections.\n"
    "- `E_gloucester_dies` (τ_s=36): single observer (Edgar), and "
    "  the reveal-and-death happens offstage, reported "
    "  retrospectively.\n"
    "- `E_goneril_suicide` (τ_s=34): offstage; Albany observes via "
    "  Gentleman's report.\n"
    "- Cornwall's death: compressed into `E_cornwall_regan_blind_"
    "  gloucester` (τ_s=23) — no explicit event, no named observers "
    "  beyond the participants already present at the blinding.\n\n"
    "The dialect's current ArPathos-style reach (via ArCharacter's "
    "tragic-hero status and the end-phase scope) admits the "
    "catharsis claim for Cordelia's death despite the empty "
    "observer set — is_tragic_hero=True is sufficient by itself for "
    "the dialect to treat her death as cathartic. The structural "
    "shape the dialect cannot name: that the catharsis is "
    "substrate-displaced from the death event to the reveal event, "
    "and that the reveal event's strength depends on the death "
    "event's substrate-level observer emptiness.\n\n"
    "Candidate dialect extensions:\n"
    "1. `ArCatharsisDisplacement` — typed record naming the pair "
    "   (death_event_id, reveal_event_id) with reader-side rationale. "
    "   Would let the dialect verify that reveal events carry "
    "   observer projections equal-or-greater than the displaced "
    "   death event's participant set.\n"
    "2. A field on ArCharacter — `catharsis_displaced_to_event_id: "
    "   Optional[str]` — lighter-weight, attached to the character "
    "   whose death is displaced. Covers Cordelia cleanly; "
    "   Gloucester's retrospective-report shape less cleanly.\n"
    "3. Substrate-only + prose — the dialect stays mute on the "
    "   displacement; the reader-model prompt notes the substrate "
    "   observer-emptiness and the reveal event's observer density "
    "   when rendering. Minimal-extension path.\n\n"
    "Session 5's live probe will test which the reader prefers. "
    "Pre-sketch forcing-function recorded for reader's reference."
)

OQ_AP7_FINDING = (
    "OQ-AP7 — Numerical range of BINDING_SEPARATED. Re-surfaced by "
    "Lear (second independent encoding after Hamlet's 9-distance "
    "surface). Lear's peripeteia-anagnorisis distance is 14. Under "
    "the default bound of 3, any distance > 3 is 'separated': "
    "Oedipus at 5, Hamlet at 9, Lear at 14, all categorically "
    "identical at dialect scope despite clearly distinct analytical "
    "meanings.\n\n"
    "Lear's 14-step separation reflects the deliberate arc-length of "
    "the protagonist's journey through humiliation-storm-madness-"
    "reconciliation — structurally distinct from Oedipus's 5-step "
    "compression (messenger-to-reveal) and Hamlet's 9-step delay "
    "(verification-to-belated-recognition). Three encodings, three "
    "distinct analytical shapes, one dialect category. The "
    "distinction Hamlet's OQ_AP7 proposed — near-separated (4..10) "
    "vs distant-separated (>10) — is now pressured with Lear at "
    "14. Alternatively, a numerical `peripeteia_anagnorisis_distance` "
    "field could accompany the categorical binding, surfacing the "
    "raw distance for reader-side interpretation.\n\n"
    "Re-surfaced; remains banked under sketch-04. Probe will verify "
    "the pressure is real or whether the reader reads all three "
    "distances under 'separated' without structural discomfort."
)

OQ_LEAR_1 = (
    "OQ-LEAR-1 — Emotional-vs-epistemic staging distinction. NEW "
    "forcing function surfaced during Session 2 authorship. Lear's "
    "anagnorisis chain authors ZERO staging steps despite Lear "
    "himself being the main-anagnorisis character (the structural "
    "pre-condition for staging). The absence is load-bearing: Lear's "
    "progression to the reconciliation with Cordelia is emotional "
    "(the storm's 'unaccommodated man' realization at τ_s=18, the "
    "mock trial's grievance-crystallization at τ_s=21, the "
    "heath-meeting with Gloucester at τ_s=27), not epistemic in the "
    "Hamlet sense (the Ghost's factual revelation, the Mousetrap's "
    "empirical verification).\n\n"
    "Sketch-03's `staging` step_kind semantics — 'epistemic waypoint "
    "on that character's staged coming-to-know' — excludes Lear's "
    "emotional waypoints by construction. The gap is neither a bug "
    "nor a forced extension on its own; it is a recognition that "
    "two structurally-distinct main-anagnorisis trajectories exist "
    "in the corpus:\n"
    "- Epistemic: character acquires information that promotes "
    "  held-beliefs (Hamlet).\n"
    "- Emotional: character undergoes affective transformation that "
    "  retracts held-beliefs without new information (Lear).\n\n"
    "Candidate dialect extensions:\n"
    "1. `step_kind=\"affective\"` — a fifth canonical step_kind "
    "   (after parallel, precipitating, staging) for same-character "
    "   emotional waypoints. Lear's E_storm_on_heath, E_lear_mock_"
    "   trial, E_lear_meets_blind_gloucester become admissible as "
    "   affective chain steps.\n"
    "2. A polarity axis on `staging`: `staging_epistemic` vs "
    "   `staging_affective`. Preserves staging's cognitive unity at "
    "   the schema level with a sub-distinction.\n"
    "3. Status quo — the dialect stays mute on emotional waypoints; "
    "   substrate-level held-effects (Lear's `remove_held` at "
    "   reconciliation) carry what the dialect does not name.\n\n"
    "Session 5's live probe will test whether the reader surfaces "
    "the gap structurally or reads Lear's main anagnorisis as "
    "unstaged without remark. Banked."
)

OQ_LEAR_2 = (
    "OQ-LEAR-2 — Double-plot unity-of-action. NEW forcing function "
    "surfaced during Session 2 authorship. Lear is the first corpus "
    "encoding to author `asserts_unity_of_action=False`. The "
    "structural ground: the Lear plot (Lear + three daughters) and "
    "the Gloucester plot (Gloucester + two sons) run in parallel "
    "across all three phases with only partial causal convergence "
    "(Dover at τ_s=22–27; the battle and catastrophe at τ_s=29–38). "
    "The A13 `AR_LEAR_GLOUCESTER_PARALLEL` carries the thematic-unity "
    "claim at dialect scope; `asserts_unity_of_action=False` carries "
    "the causal-non-unity claim at mythos scope.\n\n"
    "The dialect's `asserts_unity_of_action` semantics were pinned "
    "at A6 (sketch-01) as 'unity of action required'. Sketch-01's "
    "three encodings (Oedipus, Rashomon, Macbeth) and sketch-03's "
    "Hamlet all asserted True. Lear is the first False, and the "
    "distinction the dialect needs to carry is: `False` means 'the "
    "work admits unity-of-action violation' NOT 'the work has no "
    "unity'. The A13 parallel relation carries thematic unity; the "
    "mythos-level unity_of_action=False names the absence of "
    "classical unity.\n\n"
    "Candidate dialect refinements:\n"
    "1. `unity_of_action_shape: Optional[str]` — 'classical' | "
    "   'double-plot-parallel' | 'multi-testimony-contest' | "
    "   'episodic' — positively naming the shape when "
    "   unity_of_action=False, rather than leaving the False value "
    "   semantically undetermined.\n"
    "2. Leave unity_of_action as bool, rely on A13 to carry the "
    "   structural shape, treat `False` as 'not-classical-unity, see "
    "   A13 relations for structure'. Lean solution.\n\n"
    "Session 5's live probe will test whether the reader surfaces "
    "double-plot structure as a shape distinct from classical "
    "unity-violation. Banked."
)

# Tuple export for probe-side consumption.
OQ_FINDINGS = (
    ("OQ_AP14", OQ_AP14_FINDING),
    ("OQ_AP15", OQ_AP15_FINDING),
    ("OQ_AP7",  OQ_AP7_FINDING),
    ("OQ_LEAR_1", OQ_LEAR_1),
    ("OQ_LEAR_2", OQ_LEAR_2),
)
