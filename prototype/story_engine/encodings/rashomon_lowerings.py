"""
rashomon_lowerings.py — Lowering bindings: Rashomon Dramatic ↔
substrate. First *multi-Story* encoding's lowerings file.

Structural asymmetry to note up front: the Rashomon substrate
(rashomon.py) models only the **grove scene** — the four contested
testimonies plus the undisputed canonical floor. It does not model
the **gate frame** (priest, commoner, rain, abandoned baby). The
multi-Story Dramatic encoding (rashomon_dramatic.py), by contrast,
does: S_frame carries the full Dramatica-8 structure at the gate;
the four testimony Stories (S_bandit_ver, S_wife_ver, S_samurai_ver,
S_woodcutter_ver) are skeletal.

The lowering surface therefore splits cleanly:

- **Testimony Stories → substrate.** Every Character, Scene, and
  Throughline in the four testimony Stories maps to grove-scene
  substrate records. Each testimony Story's events live on its
  branch: S_bandit_ver → B_TAJOMARU, S_wife_ver → B_WIFE,
  S_samurai_ver → B_HUSBAND, S_woodcutter_ver → B_WOODCUTTER.

- **Frame Story → PENDING.** C_priest, C_commoner, and every frame
  Scene (S_frame_at_gate, S_frame_testimonies_reported,
  S_frame_woodcutter_breaks, S_frame_abandoned_baby,
  S_frame_rain_stops) have no substrate counterpart by design. The
  substrate's scope is the grove; the gate is Dramatic-only. PENDING
  status preserves the option to lower them later if the substrate
  scope is extended.

- **Shared entities across testimony Stories.** The Character records
  C_bandit, C_wife, C_samurai, C_woodcutter each appear in multiple
  testimony Stories (each testimony's `character_ids` tuple lists
  the agents named in that account). Entity-aliasing is OQ3 in
  multi-story-sketch-01; here we take the simple pragmatic stance —
  one Lowering per Character → Entity, not one per (Character, Story)
  pair. The verifier's per-Story iteration (MS4) uses
  `LOWERINGS_BY_STORY` below to scope Lowerings appropriately.

Character → Entity identifications (dramatis-personae):
    C_bandit     → tajomaru
    C_wife       → wife
    C_samurai    → husband    (the samurai IS the husband agent)
    C_woodcutter → woodcutter

Coupling kinds: every ACTIVE Lowering is Realization (per L1).
DSP-level and Story-level couplings live in the verifier surface
(rashomon_dramatica_complete_verification.py), not here.
"""

from __future__ import annotations

from story_engine.core.substrate import Event
from story_engine.encodings.rashomon import (
    EVENTS_ALL,
    B_TAJOMARU, B_WIFE, B_HUSBAND, B_WOODCUTTER,
)

from story_engine.encodings.rashomon_dramatic import (
    S_frame, S_bandit_ver, S_wife_ver, S_samurai_ver, S_woodcutter_ver,
)

from story_engine.core.lowering import (
    Lowering, CrossDialectRef, cross_ref,
    Annotation, PositionRange,
    LoweringStatus,
    ATTENTION_STRUCTURAL, ATTENTION_INTERPRETIVE,
)


# ============================================================================
# Helpers
# ============================================================================


def _substrate_event(event_id: str) -> Event:
    for e in EVENTS_ALL:
        if e.id == event_id:
            return e
    raise KeyError(f"no substrate event with id {event_id!r}")


def _max_event_τ_a(*event_ids: str) -> int:
    return max(_substrate_event(eid).τ_a for eid in event_ids)


def _dramatic(record_id: str) -> CrossDialectRef:
    return cross_ref("dramatic", record_id)


def _substrate(record_id: str) -> CrossDialectRef:
    return cross_ref("substrate", record_id)


# ============================================================================
# Character → Entity Lowerings (ACTIVE for grove agents, PENDING for
# frame-only characters)
# ============================================================================

L_bandit = Lowering(
    id="L_bandit",
    upper_record=_dramatic("C_bandit"),
    lower_records=(_substrate("tajomaru"),),
    annotation=Annotation(
        text=("Dramatic Character C_bandit (Tajōmaru, testimony-Story "
              "MC of S_bandit_ver; also a participant in the other "
              "three testimony Stories) → substrate Entity "
              "'tajomaru'."),
    ),
    τ_a=400,
)

L_wife = Lowering(
    id="L_wife",
    upper_record=_dramatic("C_wife"),
    lower_records=(_substrate("wife"),),
    annotation=Annotation(
        text=("C_wife (MC of S_wife_ver; participant across all four "
              "testimonies) → Entity 'wife'."),
    ),
    τ_a=401,
)

L_samurai = Lowering(
    id="L_samurai",
    upper_record=_dramatic("C_samurai"),
    lower_records=(_substrate("husband"),),
    annotation=Annotation(
        text=("C_samurai (MC of S_samurai_ver, which relays the "
              "samurai's testimony via the medium) → Entity 'husband'. "
              "The substrate uses 'husband' as the entity id because "
              "the grove-scene agent is foregrounded there as the "
              "wife's husband; the Dramatic dialect names the same "
              "agent as 'samurai' foregrounding social-role identity. "
              "Same ontic agent; different naming emphasis by layer."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=402,
)

L_woodcutter = Lowering(
    id="L_woodcutter",
    upper_record=_dramatic("C_woodcutter"),
    lower_records=(_substrate("woodcutter"),),
    annotation=Annotation(
        text=("C_woodcutter (frame Story Protagonist AND MC of "
              "S_woodcutter_ver, the belated-confession testimony) → "
              "Entity 'woodcutter'. The same Character plays two "
              "Story roles under multi-Story encoding: frame MC and "
              "testimony MC. One Entity carries both."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=403,
)

L_priest_pending = Lowering(
    id="L_priest_pending",
    upper_record=_dramatic("C_priest"),
    lower_records=(),
    annotation=Annotation(
        text=("C_priest is a frame-Story character (Emotion function; "
              "witness to the testimonies at the gate). The Rashomon "
              "substrate models only the grove scene, not the gate; "
              "there is no Entity 'priest'. PENDING keeps the option "
              "open for a future substrate-scope extension."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=404,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": ("frame-only character; substrate scope "
                              "is grove-only by design (see rashomon.py "
                              "Simplifications)")},
)

L_commoner_pending = Lowering(
    id="L_commoner_pending",
    upper_record=_dramatic("C_commoner"),
    lower_records=(),
    annotation=Annotation(
        text=("C_commoner is a frame-Story character (Skeptic; IC of "
              "the frame Story). Same rationale as L_priest_pending."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=405,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": ("frame-only character; substrate scope "
                              "is grove-only by design")},
)


# ============================================================================
# Scene → Event(s) Lowerings — Frame Story (all PENDING)
# ============================================================================
#
# The frame scenes happen at the gate, which the substrate does not
# model. Each is PENDING with a note about what a substrate extension
# would need to represent.

L_frame_at_gate_pending = Lowering(
    id="L_frame_at_gate_pending",
    upper_record=_dramatic("S_frame_at_gate"),
    lower_records=(),
    annotation=Annotation(
        text=("S_frame_at_gate (the three characters take shelter at "
              "Rashomon gate; commoner presses woodcutter and priest "
              "to explain their state) has no substrate counterpart — "
              "the substrate's scope is grove-only. A future extension "
              "would need gate/shelter Entities and a fabula for the "
              "frame's own event sequence."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=420,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "frame-only scene"},
)

L_frame_testimonies_reported_pending = Lowering(
    id="L_frame_testimonies_reported_pending",
    upper_record=_dramatic("S_frame_testimonies_reported"),
    lower_records=(),
    annotation=Annotation(
        text=("S_frame_testimonies_reported (the woodcutter and priest "
              "recount the three testimonies given at court) is the "
              "Scene through which the contained Stories' content "
              "enters the frame. Its lowering would be a "
              "Story-contains-Story pointer rather than a Scene-to-"
              "Event binding. Deferred per multi-story-sketch-01's "
              "allowance — testimony-reporting is carried by the "
              "containment StoryRelation at the encoding layer."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=421,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": ("containment-via-reporting; handled at "
                              "StoryEncoding.relations layer, not "
                              "lowering layer")},
)

L_frame_woodcutter_breaks_pending = Lowering(
    id="L_frame_woodcutter_breaks_pending",
    upper_record=_dramatic("S_frame_woodcutter_breaks"),
    lower_records=(),
    annotation=Annotation(
        text=("S_frame_woodcutter_breaks (the woodcutter's belated "
              "confession at the gate) is the frame Scene through "
              "which S_woodcutter_ver's content enters. Same "
              "containment-via-reporting rationale as "
              "L_frame_testimonies_reported_pending."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=422,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "containment-via-reporting"},
)

L_frame_abandoned_baby_pending = Lowering(
    id="L_frame_abandoned_baby_pending",
    upper_record=_dramatic("S_frame_abandoned_baby"),
    lower_records=(),
    annotation=Annotation(
        text=("S_frame_abandoned_baby (the baby cries; commoner strips "
              "its clothing; woodcutter takes the baby home). The "
              "frame's argumentative climax. Frame-only; substrate "
              "does not model the gate. A substrate extension would "
              "need a 'baby' Entity and a small gate fabula."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=423,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "frame-only scene"},
)

L_frame_rain_stops_pending = Lowering(
    id="L_frame_rain_stops_pending",
    upper_record=_dramatic("S_frame_rain_stops"),
    lower_records=(),
    annotation=Annotation(
        text=("S_frame_rain_stops (rain stops; woodcutter leaves with "
              "the baby; priest watches him go). Frame-only; same "
              "rationale."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=424,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "frame-only scene"},
)


# ============================================================================
# Scene → Event(s) Lowerings — S_bandit_ver (ACTIVE, B_TAJOMARU branch)
# ============================================================================
#
# Tajōmaru's testimony runs from the seduction through the duel. The
# seduction lowers to canonical floor events (the scene's content is
# shared across all testimonies at the structural layer); the duel
# lowers to the branch-specific combat event on B_TAJOMARU.

L_bandit_seduction = Lowering(
    id="L_bandit_seduction",
    upper_record=_dramatic("S_bandit_seduction"),
    lower_records=(
        _substrate("E_lure"),
        _substrate("E_bind"),
        _substrate("E_bring_wife"),
        _substrate("E_intercourse"),
        _substrate("E_t_wife_requests_killing"),
        _substrate("E_t_frees_husband"),
    ),
    annotation=Annotation(
        text=("S_bandit_seduction (Tajōmaru lures the samurai off-"
              "road, ties him, brings the wife, and — in his telling "
              "— seduces her with her eventual willingness) realizes "
              "as six substrate events: four canonical-floor events "
              "(E_lure, E_bind, E_bring_wife, E_intercourse — "
              "undisputed structurally across all testimonies) plus "
              "two branch-scoped events on B_TAJOMARU "
              "(E_t_wife_requests_killing, E_t_frees_husband). The "
              "seduction's modality (yielding vs. violation) lives in "
              "the description surface — D_intercourse_tajomaru_"
              "texture, branch-scoped to B_TAJOMARU — not in the "
              "event facts."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=440,
    position_range=PositionRange(coord="τ_s", min_value=2, max_value=8),
    anchor_τ_a=_max_event_τ_a(
        "E_lure", "E_bind", "E_bring_wife", "E_intercourse",
        "E_t_wife_requests_killing", "E_t_frees_husband",
    ),
)

L_bandit_duel = Lowering(
    id="L_bandit_duel",
    upper_record=_dramatic("S_bandit_duel"),
    lower_records=(_substrate("E_t_duel"),),
    annotation=Annotation(
        text=("S_bandit_duel (twenty-three strokes; Tajōmaru wins; "
              "the samurai is dead) → E_t_duel on B_TAJOMARU. The "
              "'noble-duel' framing is D_t_duel_character (interpretive "
              "texture), not event content."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=441,
    anchor_τ_a=_substrate_event("E_t_duel").τ_a,
)


# ============================================================================
# Scene → Event(s) Lowerings — S_wife_ver (ACTIVE, B_WIFE branch)
# ============================================================================

L_wife_violated = Lowering(
    id="L_wife_violated",
    upper_record=_dramatic("S_wife_violated"),
    lower_records=(
        _substrate("E_intercourse"),
        _substrate("E_w_tajomaru_leaves"),
    ),
    annotation=Annotation(
        text=("S_wife_violated (the bandit violates the wife; "
              "afterward she pleads with her tied husband and meets "
              "his gaze of contempt) realizes as the canonical-floor "
              "E_intercourse plus the branch-scoped E_w_tajomaru_"
              "leaves on B_WIFE. The 'violation' framing is "
              "D_intercourse_wife_texture (branch-scoped to B_WIFE) — "
              "NOT an event predicate. The husband's gaze of contempt "
              "is not modeled as a substrate event (no world effect, "
              "no knowledge-state change typed in this encoding); it "
              "is prose-carried."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=450,
    position_range=PositionRange(coord="τ_s", min_value=5, max_value=8),
    anchor_τ_a=_max_event_τ_a("E_intercourse", "E_w_tajomaru_leaves"),
)

L_wife_killing = Lowering(
    id="L_wife_killing",
    upper_record=_dramatic("S_wife_killing"),
    lower_records=(_substrate("E_w_killing"),),
    annotation=Annotation(
        text=("S_wife_killing (the wife kills her husband with the "
              "dagger in a half-conscious act) → E_w_killing on "
              "B_WIFE. The 'half-conscious' framing is prose/testimony "
              "texture; the substrate asserts the killing as the "
              "branch's claim."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=451,
    anchor_τ_a=_substrate_event("E_w_killing").τ_a,
)


# ============================================================================
# Scene → Event(s) Lowerings — S_samurai_ver (ACTIVE, B_HUSBAND branch)
# ============================================================================

L_samurai_begging = Lowering(
    id="L_samurai_begging",
    upper_record=_dramatic("S_samurai_begging"),
    lower_records=(
        _substrate("E_h_wife_requests_killing"),
        _substrate("E_h_tajomaru_refuses"),
        _substrate("E_h_wife_flees"),
    ),
    annotation=Annotation(
        text=("S_samurai_begging (the wife begs the bandit to kill "
              "her husband; the bandit refuses; the wife flees) "
              "realizes as three branch-scoped events on B_HUSBAND. "
              "The 'disgust' framing of the refusal — 'even Tajōmaru "
              "was repulsed' — is D_h_wife_requests_killing (motivation "
              "description), not an event effect."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=460,
    position_range=PositionRange(coord="τ_s", min_value=7, max_value=9),
    anchor_τ_a=_max_event_τ_a(
        "E_h_wife_requests_killing", "E_h_tajomaru_refuses",
        "E_h_wife_flees",
    ),
)

L_samurai_suicide = Lowering(
    id="L_samurai_suicide",
    upper_record=_dramatic("S_samurai_suicide"),
    lower_records=(
        _substrate("E_h_frees_husband"),
        _substrate("E_h_suicide"),
    ),
    annotation=Annotation(
        text=("S_samurai_suicide (the husband is unbound; he takes "
              "his own life with the wife's dagger) realizes as two "
              "B_HUSBAND events. The 'humiliated' framing is "
              "D_h_suicide_texture (motivation description)."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=461,
    position_range=PositionRange(coord="τ_s", min_value=10, max_value=11),
    anchor_τ_a=_max_event_τ_a("E_h_frees_husband", "E_h_suicide"),
)


# ============================================================================
# Scene → Event(s) Lowerings — S_woodcutter_ver (ACTIVE,
# B_WOODCUTTER branch)
# ============================================================================

L_woodcutter_fight = Lowering(
    id="L_woodcutter_fight",
    upper_record=_dramatic("S_woodcutter_fight"),
    lower_records=(
        _substrate("E_wc_wife_goads"),
        _substrate("E_wc_fight"),
        _substrate("E_wc_wife_flees"),
    ),
    annotation=Annotation(
        text=("S_woodcutter_fight (the wife goads both men; Tajōmaru "
              "and the samurai fight cowardly and clumsily; the "
              "samurai dies; the wife flees) realizes as three "
              "B_WOODCUTTER events. The 'cowardly' framing is "
              "D_wc_fight_character (texture description); the "
              "goading content is D_wc_wife_goads (motivation "
              "description). Event facts carry the structural "
              "killing; descriptions carry the tonal reading."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=470,
    position_range=PositionRange(coord="τ_s", min_value=7, max_value=10),
    anchor_τ_a=_max_event_τ_a(
        "E_wc_wife_goads", "E_wc_fight", "E_wc_wife_flees",
    ),
)

L_woodcutter_theft = Lowering(
    id="L_woodcutter_theft",
    upper_record=_dramatic("S_woodcutter_theft"),
    lower_records=(_substrate("E_wc_theft"),),
    annotation=Annotation(
        text=("S_woodcutter_theft (the woodcutter returns to the "
              "scene and takes the wife's pearl-inlaid dagger — the "
              "self-incriminating detail) → E_wc_theft on "
              "B_WOODCUTTER. The trust-flag description "
              "D_woodcutter_trust sits on this event; its authorial-"
              "uncertainty child D_wc_authorial_doubt sits on the "
              "trust-flag itself (description-on-description)."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=471,
    anchor_τ_a=_substrate_event("E_wc_theft").τ_a,
)


# ============================================================================
# Throughline → many-events with position_range — testimony Stories
# ============================================================================
#
# Each testimony's MC Throughline realizes across that testimony's
# branch events. The canonical-floor events are NOT included here —
# they are shared setup across all four branches, not MC-Throughline-
# carrying beats that characterize the testifier's self-account.
# (The seduction/violation intercourse event is canonical floor; its
# per-branch reading lives in descriptions, not in the fabula, so the
# MC Throughline's arc-body is on the branch-scoped events where the
# testifier's account diverges.)

L_bandit_mc_throughline = Lowering(
    id="L_bandit_mc_throughline",
    upper_record=_dramatic("T_bandit_mc"),
    lower_records=(
        _substrate("E_t_wife_requests_killing"),
        _substrate("E_t_frees_husband"),
        _substrate("E_t_duel"),
    ),
    annotation=Annotation(
        text=("T_bandit_mc (Tajōmaru's self-account of prowess and "
              "noble contest) realizes across the three B_TAJOMARU "
              "branch events — the wife's requested killing that "
              "motivates the duel, the unbinding that makes a fair "
              "fight possible, and the twenty-three-stroke duel "
              "itself. Arc runs τ_s=7..9. Branch-scoped per "
              "throughline-lowering-scope-sketch-01 TL2: the "
              "subject-named seduction (canonical-floor events "
              "E_lure, E_bind, E_bring_wife, E_intercourse at "
              "τ_s=2..5) is shared substrate; Tajōmaru's reading of "
              "those events as a noble seduction lives in "
              "D_intercourse_tajomaru_texture (Description on "
              "E_intercourse), not in this Lowering's "
              "lower_records."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=490,
    position_range=PositionRange(coord="τ_s", min_value=7, max_value=9),
    anchor_τ_a=_max_event_τ_a(
        "E_t_wife_requests_killing", "E_t_frees_husband", "E_t_duel",
    ),
)

L_wife_mc_throughline = Lowering(
    id="L_wife_mc_throughline",
    upper_record=_dramatic("T_wife_mc"),
    lower_records=(
        _substrate("E_w_tajomaru_leaves"),
        _substrate("E_w_killing"),
    ),
    annotation=Annotation(
        text=("T_wife_mc (the wife's self-account of violation and a "
              "half-conscious killing) realizes across the two "
              "B_WIFE branch events. Arc runs τ_s=7..10. "
              "Branch-scoped per throughline-lowering-scope-sketch-"
              "01 TL2: the subject-named violation is realized by "
              "canonical-floor E_intercourse at τ_s=5; the wife's "
              "reading of that event as violation lives in "
              "D_intercourse_wife_texture (Description on "
              "E_intercourse), not in this Lowering's "
              "lower_records."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=491,
    position_range=PositionRange(coord="τ_s", min_value=7, max_value=10),
    anchor_τ_a=_max_event_τ_a("E_w_tajomaru_leaves", "E_w_killing"),
)

L_samurai_mc_throughline = Lowering(
    id="L_samurai_mc_throughline",
    upper_record=_dramatic("T_samurai_mc"),
    lower_records=(
        _substrate("E_h_wife_requests_killing"),
        _substrate("E_h_tajomaru_refuses"),
        _substrate("E_h_wife_flees"),
        _substrate("E_h_frees_husband"),
        _substrate("E_h_suicide"),
    ),
    annotation=Annotation(
        text=("T_samurai_mc (the samurai's self-account, delivered "
              "through the medium: betrayal and ritual self-erasure) "
              "realizes across five B_HUSBAND branch events. Arc runs "
              "τ_s=7..11. Longest testimony-MC arc of the four."),
        attention=ATTENTION_STRUCTURAL,
    ),
    τ_a=492,
    position_range=PositionRange(coord="τ_s", min_value=7, max_value=11),
    anchor_τ_a=_max_event_τ_a(
        "E_h_wife_requests_killing", "E_h_tajomaru_refuses",
        "E_h_wife_flees", "E_h_frees_husband", "E_h_suicide",
    ),
)

L_woodcutter_mc_throughline = Lowering(
    id="L_woodcutter_mc_throughline",
    upper_record=_dramatic("T_woodcutter_mc"),
    lower_records=(
        _substrate("E_wc_wife_goads"),
        _substrate("E_wc_fight"),
        _substrate("E_wc_wife_flees"),
        _substrate("E_wc_theft"),
    ),
    annotation=Annotation(
        text=("T_woodcutter_mc (the woodcutter's belated account: a "
              "cowardly fight, a goading wife, and the self-"
              "incriminating theft of the dagger) realizes across "
              "four B_WOODCUTTER branch events. Arc runs τ_s=7..11. "
              "The theft is the self-incriminating pivot — the "
              "Throughline arc INCLUDES it because the woodcutter's "
              "account centers on admitting his own complicity."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=493,
    position_range=PositionRange(coord="τ_s", min_value=7, max_value=11),
    anchor_τ_a=_max_event_τ_a(
        "E_wc_wife_goads", "E_wc_fight", "E_wc_wife_flees", "E_wc_theft",
    ),
)


# ============================================================================
# Throughline → PENDING — frame Throughlines
# ============================================================================

L_frame_overall_pending = Lowering(
    id="L_frame_overall_pending",
    upper_record=_dramatic("T_frame_overall"),
    lower_records=(),
    annotation=Annotation(
        text=("T_frame_overall (the interpretive crisis at the gate) "
              "has no substrate realization — frame-only. PENDING."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=495,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "frame-only throughline"},
)

L_frame_mc_pending = Lowering(
    id="L_frame_mc_pending",
    upper_record=_dramatic("T_frame_mc"),
    lower_records=(),
    annotation=Annotation(
        text=("T_frame_mc (the woodcutter's struggle at the gate — "
              "to be the kind of witness he was not in the grove, "
              "and make good on it). The woodcutter's **frame-side** "
              "arc happens at the gate, which the substrate does not "
              "model. His **testimony-side** arc is lowered via "
              "L_woodcutter_mc_throughline. Same Entity, two "
              "Throughlines across two Stories — classic multi-Story "
              "shape. PENDING on the frame side."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=496,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "frame-only throughline"},
)

L_frame_ic_pending = Lowering(
    id="L_frame_ic_pending",
    upper_record=_dramatic("T_frame_ic"),
    lower_records=(),
    annotation=Annotation(
        text=("T_frame_ic (the commoner's cynicism). Frame-only; "
              "PENDING."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=497,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "frame-only throughline"},
)

L_frame_rel_pending = Lowering(
    id="L_frame_rel_pending",
    upper_record=_dramatic("T_frame_rel"),
    lower_records=(),
    annotation=Annotation(
        text=("T_frame_rel (the priest-woodcutter relationship: "
              "crisis of faith and its restoration). Frame-only; "
              "PENDING."),
        attention=ATTENTION_INTERPRETIVE,
    ),
    τ_a=498,
    status=LoweringStatus.PENDING,
    metadata={"why_pending": "frame-only throughline"},
)


# ============================================================================
# Aggregate
# ============================================================================

LOWERINGS = (
    # Character → Entity (ACTIVE)
    L_bandit, L_wife, L_samurai, L_woodcutter,
    # Character → Entity (PENDING — frame-only)
    L_priest_pending, L_commoner_pending,
    # Scene → Event(s), frame (all PENDING)
    L_frame_at_gate_pending,
    L_frame_testimonies_reported_pending,
    L_frame_woodcutter_breaks_pending,
    L_frame_abandoned_baby_pending,
    L_frame_rain_stops_pending,
    # Scene → Event(s), testimonies (ACTIVE)
    L_bandit_seduction, L_bandit_duel,
    L_wife_violated, L_wife_killing,
    L_samurai_begging, L_samurai_suicide,
    L_woodcutter_fight, L_woodcutter_theft,
    # Throughline → many-events (ACTIVE — testimonies)
    L_bandit_mc_throughline,
    L_wife_mc_throughline,
    L_samurai_mc_throughline,
    L_woodcutter_mc_throughline,
    # Throughline → PENDING — frame
    L_frame_overall_pending,
    L_frame_mc_pending,
    L_frame_ic_pending,
    L_frame_rel_pending,
)


# ============================================================================
# Per-Story Lowerings view — for MS4 per-Story verification
# ============================================================================
#
# Each testimony Story's scope = its own Character Lowerings + Scene
# Lowerings + Throughline Lowerings. Shared Characters (e.g., C_bandit
# appears in all four testimonies) are listed under each Story that
# references them — the Character Lowering record itself is unique,
# but the Story-scoped view surfaces which Stories reach it.

LOWERINGS_BY_STORY = {
    S_frame.id: (
        # Frame sees C_woodcutter (shared with woodcutter testimony),
        # C_priest, C_commoner as characters; frame Scenes; frame
        # Throughlines. All PENDING except C_woodcutter (which has
        # an active grove-side lowering).
        L_woodcutter,
        L_priest_pending, L_commoner_pending,
        L_frame_at_gate_pending,
        L_frame_testimonies_reported_pending,
        L_frame_woodcutter_breaks_pending,
        L_frame_abandoned_baby_pending,
        L_frame_rain_stops_pending,
        L_frame_overall_pending, L_frame_mc_pending,
        L_frame_ic_pending, L_frame_rel_pending,
    ),
    S_bandit_ver.id: (
        L_bandit, L_wife, L_samurai,
        L_bandit_seduction, L_bandit_duel,
        L_bandit_mc_throughline,
    ),
    S_wife_ver.id: (
        L_wife, L_bandit, L_samurai,
        L_wife_violated, L_wife_killing,
        L_wife_mc_throughline,
    ),
    S_samurai_ver.id: (
        L_samurai, L_bandit, L_wife,
        L_samurai_begging, L_samurai_suicide,
        L_samurai_mc_throughline,
    ),
    S_woodcutter_ver.id: (
        L_woodcutter, L_bandit, L_wife, L_samurai,
        L_woodcutter_fight, L_woodcutter_theft,
        L_woodcutter_mc_throughline,
    ),
}
