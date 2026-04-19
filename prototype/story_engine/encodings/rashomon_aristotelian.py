"""
rashomon_aristotelian.py — Rashomon encoded under the Aristotelian
dialect (aristotelian-sketch-01 stress case).

Implementation of the sketch's Rashomon stress case. The sketch's
design-phase finding was that Rashomon admits an Aristotelian
encoding as a **multi-mythos tuple** — four ArMythos records (one
per testimony) sharing canonical-floor events as common beginning
phase. This file lands that encoding in code to verify the claim.

The substrate (`prototype/story_engine/encodings/rashomon.py`) has
22 events: 8 canonical-floor (undisputed road-and-grove lead-up +
the husband's death) and 14 testimony-branch (3 Tajōmaru + 2 Wife
+ 5 Samurai + 4 Woodcutter). The frame — gate, rainstorm, priest,
commoner, baby — exists only at the Dramatic dialect layer; no
substrate realization to encode Aristotelian-ly.

Two honest dialect-scope limits (per aristotelian-sketch-01 stress
case) are NOT covered by this file and stay as authorial content:

- Meta-anagnorisis (priest / audience realizing no testimony is
  fully true). Reader-level, not character-level; outside
  Aristotle's vocabulary.
- Contested relations between mythoi (the four testimonies contest
  the same canonical-floor events). Sketch-02 extension
  (ArMythosRelation) if a forcing function appears; this file
  omits it.

Running:
    cd prototype
    python3 -c "
    from story_engine.encodings.rashomon import EVENTS_ALL
    from story_engine.encodings.rashomon_aristotelian import (
        AR_RASHOMON_MYTHOI,
    )
    from story_engine.core.aristotelian import verify
    for m in AR_RASHOMON_MYTHOI:
        obs = verify(m, substrate_events=EVENTS_ALL)
        print(f'{m.id}: {len(obs)} observation(s)')
        for o in obs:
            print(f'  [{o.severity}] {o.code}: {o.message[:100]}')
    "
"""

from __future__ import annotations

from story_engine.core.aristotelian import (
    ArCharacter,
    ArMythos,
    ArPhase,
    PHASE_BEGINNING,
    PHASE_END,
    PHASE_MIDDLE,
    PLOT_COMPLEX,
)


# ============================================================================
# Shared canonical-floor phase template
# ============================================================================
#
# Every testimony shares the same undisputed lead-up: husband + wife
# travel the forest road; Tajōmaru sees them; lures the husband; binds
# him; brings the wife; the intercourse event whose moral quality is
# the core testimony dispute. All four testimonies agree these events
# occurred. Per the sketch's stress-case encoding, each testimony-
# mythos gets its own ArPhase (distinct id; same scope_event_ids).

_CANONICAL_FLOOR_BEGINNING_SCOPE: tuple = (
    "E_travel",
    "E_tajomaru_sees_them",
    "E_lure",
    "E_bind",
    "E_bring_wife",
    "E_intercourse",
)


# ============================================================================
# Mythos 1 — Tajōmaru's account
# ============================================================================

AR_RASHOMON_BANDIT = ArMythos(
    id="ar_rashomon_bandit",
    title="Rashomon — Tajōmaru's account",
    action_summary=(
        "The bandit's boast: he sees a samurai and wife on the "
        "forest road; lures the husband off and binds him; brings "
        "the wife; takes her by force (which he frames as seduction "
        "ending in consent); at her request, frees the husband for "
        "a fair duel; kills him in twenty-three strokes."
    ),
    central_event_ids=(
        *_CANONICAL_FLOOR_BEGINNING_SCOPE,
        "E_t_wife_requests_killing",
        "E_t_frees_husband",
        "E_t_duel",
        "E_husband_dead",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=(
        ArPhase(
            id="ph_b_beginning",
            role=PHASE_BEGINNING,
            scope_event_ids=_CANONICAL_FLOOR_BEGINNING_SCOPE,
            annotation=(
                "Canonical-floor lead-up; undisputed across all four "
                "testimonies. These incidents function as what "
                "Aristotle calls that which does not itself follow "
                "anything by causal necessity (Poetics 1450b) — the "
                "shared given from which the bandit's distinctive "
                "action (seduction, not violation) proceeds."
            ),
        ),
        ArPhase(
            id="ph_b_middle",
            role=PHASE_MIDDLE,
            scope_event_ids=(
                "E_t_wife_requests_killing", "E_t_frees_husband",
            ),
            annotation=(
                "The testimony-specific action: the wife's request "
                "(which Tajōmaru frames as the woman deciding "
                "between her two men); the unbinding that transforms "
                "a captive-beside-execution scene into a fair "
                "combat."
            ),
        ),
        ArPhase(
            id="ph_b_end",
            role=PHASE_END,
            scope_event_ids=("E_t_duel", "E_husband_dead"),
            annotation=(
                "The duel itself and the husband's death. Tajōmaru "
                "dwells on the combat's honor; the substrate records "
                "the death as a canonical-floor fact across all "
                "testimonies."
            ),
        ),
    ),
    complication_event_id="E_t_wife_requests_killing",
    denouement_event_id="E_t_duel",
    peripeteia_event_id="E_t_wife_requests_killing",
    anagnorisis_event_id=None,
    asserts_unity_of_action=True,
    asserts_unity_of_time=False,      # span τ_s=0..20; unity not asserted
    asserts_unity_of_place=False,     # forest_road → grove across events
    aims_at_catharsis=False,          # boastful account, not tragic
    characters=(
        ArCharacter(
            id="ar_b_tajomaru",
            name="Tajōmaru",
            character_ref_id="tajomaru",
            hamartia_text=(
                "Overweening confidence in his own prowess — the "
                "entire account is structured to preserve his "
                "self-image as noble bandit. In Aristotelian terms, "
                "the hamartia is ignorance of how the world reads a "
                "rape: he cannot acknowledge the event's criminal "
                "shape even in his own telling."
            ),
            is_tragic_hero=True,
        ),
    ),
)


# ============================================================================
# Mythos 2 — The wife's account
# ============================================================================

AR_RASHOMON_WIFE = ArMythos(
    id="ar_rashomon_wife",
    title="Rashomon — The wife's account",
    action_summary=(
        "The wife's self-account: Tajōmaru assaults her; after he "
        "leaves, she turns to her husband and cannot endure his "
        "gaze of contempt; she kills him half-consciously, "
        "dissociating from her own act."
    ),
    central_event_ids=(
        *_CANONICAL_FLOOR_BEGINNING_SCOPE,
        "E_w_tajomaru_leaves",
        "E_w_killing",
        "E_husband_dead",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=(
        ArPhase(
            id="ph_w_beginning",
            role=PHASE_BEGINNING,
            scope_event_ids=_CANONICAL_FLOOR_BEGINNING_SCOPE,
            annotation=(
                "Canonical-floor lead-up; the same shared incidents "
                "the other testimonies begin from. In the wife's "
                "mythos these events take on a different character "
                "— the arrangement aims toward her distinctive "
                "pathos, violation rather than the bandit's "
                "seduction."
            ),
        ),
        ArPhase(
            id="ph_w_middle",
            role=PHASE_MIDDLE,
            scope_event_ids=("E_w_tajomaru_leaves",),
            annotation=(
                "Tajōmaru leaves. The wife is alone with her bound "
                "husband. The husband's gaze of contempt is the "
                "proximate cause of her pathos — authored in this "
                "encoding's prose rather than in the typed event "
                "model — and compels the movement toward "
                "denouement."
            ),
        ),
        ArPhase(
            id="ph_w_end",
            role=PHASE_END,
            scope_event_ids=("E_w_killing", "E_husband_dead"),
            annotation=(
                "The killing, dissociated. The wife's account does "
                "not contain a moment of recognition; her "
                "relationship to her own action is incomplete."
            ),
        ),
    ),
    complication_event_id="E_w_tajomaru_leaves",
    denouement_event_id="E_w_killing",
    peripeteia_event_id="E_intercourse",
    anagnorisis_event_id=None,
    asserts_unity_of_action=True,
    asserts_unity_of_time=False,
    asserts_unity_of_place=False,
    aims_at_catharsis=True,
    characters=(
        ArCharacter(
            id="ar_w_wife",
            name="The wife",
            character_ref_id="wife",
            hamartia_text=(
                "Aristotle's hamartia fits awkwardly: the wife's "
                "self-account is a tragedy of pathos more than error. "
                "If hamartia is present it is the dissociative "
                "refusal to own the killing — a refusal that the "
                "telling itself is a repetition of."
            ),
            is_tragic_hero=True,
        ),
    ),
)


# ============================================================================
# Mythos 3 — The samurai's account (via the medium)
# ============================================================================

AR_RASHOMON_SAMURAI = ArMythos(
    id="ar_rashomon_samurai",
    title="Rashomon — The samurai's account",
    action_summary=(
        "The samurai, speaking through a medium from beyond death: "
        "after the assault, his wife turns to Tajōmaru and begs him "
        "to kill her husband so she can follow him without shame. "
        "Tajōmaru refuses in horror; the wife flees; Tajōmaru "
        "cuts the samurai's bonds and leaves; the samurai commits "
        "ritual suicide with his wife's dagger."
    ),
    central_event_ids=(
        *_CANONICAL_FLOOR_BEGINNING_SCOPE,
        "E_h_wife_requests_killing",
        "E_h_tajomaru_refuses",
        "E_h_wife_flees",
        "E_h_frees_husband",
        "E_h_suicide",
        "E_husband_dead",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=(
        ArPhase(
            id="ph_h_beginning",
            role=PHASE_BEGINNING,
            scope_event_ids=_CANONICAL_FLOOR_BEGINNING_SCOPE,
            annotation=(
                "Canonical-floor lead-up; the shared given. The "
                "samurai's reading of E_intercourse is the worst "
                "of the four — his testimony arranges these events "
                "to see consent where his wife was violated, an "
                "ethos that shapes the mythos he moves toward."
            ),
        ),
        ArPhase(
            id="ph_h_middle",
            role=PHASE_MIDDLE,
            scope_event_ids=(
                "E_h_wife_requests_killing",
                "E_h_tajomaru_refuses",
                "E_h_wife_flees",
                "E_h_frees_husband",
            ),
            annotation=(
                "The betrayal-and-abandonment sequence. The "
                "samurai's wife asks the bandit to kill him; "
                "Tajōmaru refuses (an event unique to this "
                "testimony); the wife flees; Tajōmaru unbinds the "
                "samurai and leaves. The samurai is alone with the "
                "dagger."
            ),
        ),
        ArPhase(
            id="ph_h_end",
            role=PHASE_END,
            scope_event_ids=("E_h_suicide", "E_husband_dead"),
            annotation=(
                "Ritual self-erasure. The samurai's account is the "
                "only one in which the husband kills himself; the "
                "dagger's later theft (per the woodcutter's "
                "testimony) is what makes E_husband_dead a disputed "
                "cause-of-death across the four accounts."
            ),
        ),
    ),
    complication_event_id="E_h_wife_requests_killing",
    denouement_event_id="E_h_frees_husband",
    peripeteia_event_id="E_h_wife_requests_killing",
    anagnorisis_event_id=None,
    asserts_unity_of_action=True,
    asserts_unity_of_time=False,
    asserts_unity_of_place=False,
    aims_at_catharsis=True,
    characters=(
        ArCharacter(
            id="ar_h_samurai",
            name="The samurai",
            character_ref_id="husband",
            hamartia_text=(
                "The samurai's hamartia is ignorance of his wife's "
                "character — he bound his honor to her fidelity and "
                "cannot recover from her (claimed) request for his "
                "death. The account is structured to preserve his "
                "honor posthumously; ritual suicide is the only "
                "response his code admits."
            ),
            is_tragic_hero=True,
        ),
    ),
)


# ============================================================================
# Mythos 4 — The woodcutter's account (belated confession)
# ============================================================================

AR_RASHOMON_WOODCUTTER = ArMythos(
    id="ar_rashomon_woodcutter",
    title="Rashomon — The woodcutter's account",
    action_summary=(
        "The woodcutter's belated confession: after the assault, "
        "the wife goads both men into a messy, cowardly fight; "
        "Tajōmaru and the husband fumble at each other in a "
        "graceless struggle; the wife flees; Tajōmaru kills the "
        "husband; the woodcutter, hidden in the undergrowth, "
        "steals the husband's pearl-handled dagger from the "
        "corpse — the theft that makes his own testimony "
        "suspect."
    ),
    central_event_ids=(
        *_CANONICAL_FLOOR_BEGINNING_SCOPE,
        "E_wc_wife_goads",
        "E_wc_fight",
        "E_wc_wife_flees",
        "E_wc_theft",
        "E_husband_dead",
    ),
    plot_kind=PLOT_COMPLEX,
    phases=(
        ArPhase(
            id="ph_wc_beginning",
            role=PHASE_BEGINNING,
            scope_event_ids=_CANONICAL_FLOOR_BEGINNING_SCOPE,
            annotation=(
                "Canonical-floor lead-up. The woodcutter is the "
                "only testifier with no sexual or intimate "
                "relationship to the event (he is a hidden "
                "witness); his reading of E_intercourse is the "
                "most external of the four."
            ),
        ),
        ArPhase(
            id="ph_wc_middle",
            role=PHASE_MIDDLE,
            scope_event_ids=("E_wc_wife_goads", "E_wc_fight"),
            annotation=(
                "The wife's goading and the ensuing graceless "
                "fight. The woodcutter dwells on the "
                "cowardice — important to the account's truth-"
                "claim structure (he is the only testifier "
                "incentivized toward dishonoring all parties)."
            ),
        ),
        ArPhase(
            id="ph_wc_end",
            role=PHASE_END,
            scope_event_ids=(
                "E_wc_wife_flees", "E_wc_theft", "E_husband_dead",
            ),
            annotation=(
                "The wife's flight, the husband's death, and the "
                "woodcutter's theft of the dagger. The theft is "
                "the pivot of the woodcutter's self-incrimination "
                "— the reason his confession is late, and the "
                "reason his testimony cannot resolve into clean "
                "authority. The film's framing narrative (priest's "
                "crisis of faith) sits outside this mythos's "
                "substrate events; it is named here for context "
                "but not grounded in this record."
            ),
        ),
    ),
    complication_event_id="E_wc_wife_goads",
    denouement_event_id="E_wc_fight",
    peripeteia_event_id="E_wc_wife_goads",
    anagnorisis_event_id=None,
    asserts_unity_of_action=True,
    asserts_unity_of_time=False,
    asserts_unity_of_place=False,
    aims_at_catharsis=True,
    characters=(
        ArCharacter(
            id="ar_wc_woodcutter",
            name="The woodcutter",
            character_ref_id="woodcutter",
            hamartia_text=(
                "The woodcutter's hamartia is small complicity "
                "compounded by silence — the dagger theft is a "
                "petty act that, in being concealed, implicates "
                "the entire testimony. Aristotle would find this "
                "awkward: the woodcutter's account is a self-"
                "inclusive tragedy whose hero is the account's "
                "own narrator, a frame Aristotelian theory does "
                "not natively admit."
            ),
            is_tragic_hero=True,
        ),
    ),
)


# ============================================================================
# The tuple
# ============================================================================

AR_RASHOMON_MYTHOI: tuple = (
    AR_RASHOMON_BANDIT,
    AR_RASHOMON_WIFE,
    AR_RASHOMON_SAMURAI,
    AR_RASHOMON_WOODCUTTER,
)
