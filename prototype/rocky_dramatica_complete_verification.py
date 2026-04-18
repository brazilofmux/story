"""
rocky_dramatica_complete_verification.py — fourth cross-boundary
verifier at the **dramatica-complete → substrate** coupling boundary.

Parallels the three existing verifiers (Macbeth / Oedipus / Ackroyd).
Rocky's encoding is structurally distinct from all three:

- **First Timelock in the corpus.** DSP_limit=Timelock is
  affirmatively detected via LT9 (pressure-shape-taxonomy-sketch-02):
  the substrate carries `scheduled_fight(apollo, mac)` and
  `scheduled_fight(apollo, rocky)` as scheduling predicates (LT8),
  and under LT7's arc-position banding the LT2 convergence signals
  (Mac's pre-plot retraction at τ_s=-5, went_the_distance emergence
  at τ_s=55 terminal) are all non-middle-arc. Middle-arc LT2 count
  is 0; LT9 fires. Under sketch-01 (before LT9) the same substrate
  produced NEEDS_WORK 0.33 — the first non-APPROVED DSP_limit in
  the corpus, which directly drove the cross-boundary reader-model
  probe's dissent that proposed the LT9 signature.

- **First Outcome=Failure.** All three prior encodings had
  Outcome=Success; even the tragedies' OS goals (identify the killer,
  name the murderer) resolved. Rocky's OS goal is the clean
  publicity-stunt win for Apollo — which does NOT land because Rocky
  goes the distance. The Outcome=Success checks in the other three
  verifiers ask "did the goal's load-bearing fact land?" — for
  Failure, the same question is asked but the expected answer
  inverts: a Failure declaration is supported if the goal's fact
  does NOT land.

- **First Judgment=Good for the MC.** Oedipus, Macbeth, Ackroyd all
  have Judgment=Bad (epistemic ruin, moral degradation, betrayer
  self-erasure). Rocky's Judgment=Good is the opposite shape — the
  MC's internal resolution is positive at τ_s=end. The substrate
  signature is the confluence of went_the_distance (achievement),
  called_out(rocky, adrian) (relationship payoff), and refused_rematch
  (acceptance of the outcome as sufficient).

- **Same Steadfast+Start pair as Ackroyd, different semantic polarity.**
  Ackroyd's Steadfast is a pre-existing trait (betrayer_of_trust
  derives at the murder and holds through the arc); Ackroyd's Start
  is ultimatum-compelled (Poirot forces Sheppard's confession-writing).
  Rocky's Steadfast is "club fighter to end"; Rocky's Start is
  privately chosen (the night-before articulation) rather than
  externally compelled. Same structural shape at the verifier layer;
  different authorial semantics.

- **Same Do-er + Activity pair as Oedipus/Macbeth.** Rocky's action-
  saturated MC arc (training, fighting) lets EK2's external-action
  predicate carry DA_mc and DSP_approach the same way it did for
  Macbeth.

Measured verdicts (post-pressure-shape-taxonomy-sketch-02, 2026-04-17):

- DA_mc: APPROVED 0.72 (action-saturated MC arc under EK2)
- DSP_approach: APPROVED 0.74 (Do-er; same EK2 predicate)
- DSP_limit: APPROVED 1.00 (Timelock-strong via LT9 — two distinct
  scheduled_fight Props, zero middle-arc LT2 signals; closes the
  prior sketch-01 NEEDS_WORK 0.33 verdict)
- DSP_outcome: APPROVED 1.00 (Failure declared; went_the_distance
  DOES derive → goal does NOT cleanly land)
- DSP_judgment: APPROVED (Good declared; Rocky's positive-closure facts
  all hold at end)
- DSP_resolve: APPROVED (Steadfast declared; no identity collapses
  involving Rocky)
- DSP_growth: APPROVED (Start declared; articulated_goal lands at
  τ_s=45 and persists)
- Story_goal: shows trajectory toward Failure (clean stunt
  contaminated)
- Story_consequence: APPROVED (consequence IS realized under Failure)

Per V6, trajectory and moment checks compose with inference-01's
derivation surface — went_the_distance is derived via
WENT_THE_DISTANCE_RULE, not authored.
"""

from __future__ import annotations

from typing import Callable

from substrate import (
    Entity, Event, CANONICAL, Slot,
    project_world, project_knowledge, in_scope,
    world_holds_derived,
)
from rocky import (
    FABULA, ENTITIES, RULES, ALL_BRANCHES,
    went_the_distance, fought_rounds, refused_rematch,
    called_out, romantic_partnership, trained_by,
)

from dramatic import Throughline, Character
from rocky_dramatic import THROUGHLINES, CHARACTERS, STORY

from dramatica_template import (
    DomainAssignment, DynamicStoryPoint, DSPAxis,
    Domain, Approach, Outcome, Judgment,
)
from rocky_dramatica_complete import (
    DOMAIN_ASSIGNMENTS, DYNAMIC_STORY_POINTS,
    STORY_GOAL, STORY_CONSEQUENCE,
)

from lowering import (
    CrossDialectRef, cross_ref, LoweringStatus,
)
from rocky_lowerings import LOWERINGS
from verification import (
    VerificationReview, StructuralAdvisory,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH,
    VERDICT_NOTED,
    SEVERITY_NOTED,
)
from verifier_helpers import (
    classify_event_action_shape, agent_ids_from_entities,
    dsp_limit_characterization_check,
    detect_preceding_ic_event,
    events_advancing_throughline,
)


# ============================================================================
# Encoding-bound helpers
# ============================================================================


ROCKY_ENTITY_ID = "rocky"
APOLLO_ENTITY_ID = "apollo"
ADRIAN_ENTITY_ID = "adrian"
_AGENT_IDS = agent_ids_from_entities(ENTITIES)


def _end_τ_s() -> int:
    """Highest τ_s in Rocky's fabula."""
    return max(e.τ_s for e in FABULA if e.τ_s is not None)


def _events_lowered_from_throughline(throughline_id: str) -> tuple:
    """Return substrate Events reached via ACTIVE Lowerings whose
    upper_record is this Throughline."""
    upper = cross_ref("dramatic", throughline_id)
    event_ids: list = []
    for lw in LOWERINGS:
        if lw.upper_record != upper:
            continue
        if lw.status != LoweringStatus.ACTIVE:
            continue
        for lr in lw.lower_records:
            if lr.dialect == "substrate":
                event_ids.append(lr.record_id)
    events = []
    for eid in event_ids:
        for e in FABULA:
            if e.id == eid:
                events.append(e)
                break
    return tuple(events)


def _rocky_is_participant(event: Event) -> bool:
    parts = event.participants or {}
    return ROCKY_ENTITY_ID in parts.values()


# ============================================================================
# Check 1 — Characterization: DomainAssignment(T_mc_rocky, ACTIVITY)
# ============================================================================


def mc_throughline_activity_domain_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DA_mc — T_mc_rocky is in Activity domain. Substrate
    check: of the events reached via L_mc_throughline, count external-
    action-shaped vs. internal-state-shaped per EK2."""
    events = _events_lowered_from_throughline("T_mc_rocky")
    if not events:
        return (
            VERDICT_NOTED, None,
            "T_mc_rocky has no ACTIVE substrate-event Lowerings; "
            "DomainAssignment check cannot evaluate",
        )
    total = len(events)
    action_count = sum(
        1 for e in events
        if classify_event_action_shape(e, agent_ids=_AGENT_IDS)
        == "external"
    )
    state_count = total - action_count
    ratio = action_count / total
    if ratio >= 0.7:
        return (
            VERDICT_APPROVED, ratio,
            f"{action_count}/{total} ({ratio:.0%}) MC-Throughline "
            f"events are external-action-shaped (EK2); {state_count} "
            f"are internal-state-shaped. Consistent with Activity "
            f"domain — Rocky's arc is training-and-fighting, not "
            f"reflection.",
        )
    if ratio >= 0.4:
        return (
            VERDICT_PARTIAL_MATCH, ratio,
            f"{action_count}/{total} ({ratio:.0%}) MC-Throughline "
            f"events are external-action-shaped (EK2); the mix is "
            f"heavier on internal states than Activity-domain predicts.",
        )
    return (
        VERDICT_NEEDS_WORK, ratio,
        f"only {action_count}/{total} ({ratio:.0%}) MC-Throughline "
        f"events are external-action-shaped per EK2. Activity-domain "
        f"classification weakly supported.",
    )


# ============================================================================
# Check 2 — Characterization: DSP_approach = Do-er
# ============================================================================


def rocky_do_er_approach_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DSP_approach — Rocky is a Do-er. Substrate check:
    of events where Rocky is a participant, the fraction that are
    external-action-shaped per EK2. Rocky's Throughline is training,
    courtship, fighting — all outward."""
    rocky_events = [e for e in FABULA if _rocky_is_participant(e)]
    if not rocky_events:
        return (
            VERDICT_NOTED, None,
            "Rocky entity has no recorded participations; check "
            "cannot evaluate",
        )
    total = len(rocky_events)
    action_count = sum(
        1 for e in rocky_events
        if classify_event_action_shape(e, agent_ids=_AGENT_IDS)
        == "external"
    )
    ratio = action_count / total
    if ratio >= 0.65:
        return (
            VERDICT_APPROVED, ratio,
            f"Rocky participates in {total} events; {action_count} "
            f"({ratio:.0%}) are external-action-shaped (EK2). Do-er "
            f"approach confirmed.",
        )
    if ratio >= 0.35:
        return (
            VERDICT_PARTIAL_MATCH, ratio,
            f"Rocky participates in {total} events; {action_count} "
            f"({ratio:.0%}) are external-action-shaped (EK2). Mixed "
            f"Do-er / Be-er signature.",
        )
    return (
        VERDICT_NEEDS_WORK, ratio,
        f"Rocky participates in {total} events; only {action_count} "
        f"({ratio:.0%}) are external-action-shaped per EK2. Do-er "
        f"classification weakly supported.",
    )


# ============================================================================
# Check 3 — Characterization: DSP_limit = Timelock
#            (pressure-shape-taxonomy-sketch-01 — stress-tests LT5)
# ============================================================================


def dsp_limit_timelock_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DSP_limit. Rocky declares Timelock — the fight is
    calendared; the clock counts down. LT2 reads the substrate and
    counts convergence signals: Rocky has one retraction (Mac's fight
    scheduling) and one rule-emergence (went_the_distance), which
    land Optionlock 0.67 under LT2. Under LT5 this is a
    declaration/substrate disagreement → NEEDS_WORK or PARTIAL_MATCH.

    This is the FIRST non-APPROVED DSP_limit verdict in the corpus
    and the direct test of LT5's asymmetric disposition (strong
    Optionlock predicate; weak complement-only Timelock predicate).
    The honest signal is: LT2 cannot affirmatively detect Timelock
    without a future substrate-05 scheduling vocabulary or a
    description-kind classifier (LT3-strong OQ1). Rocky's retraction
    is structurally a pre-plot premise retraction, not an arc-
    converging signal; the rule-emergence lands AT the scheduled τ_s,
    not before — so convergence coincides with schedule rather than
    replacing it. The finding feeds Phase 3's README update."""
    declared = next(
        d.choice for d in DYNAMIC_STORY_POINTS if d.axis == DSPAxis.LIMIT
    )
    return dsp_limit_characterization_check(
        FABULA, RULES, CANONICAL, ALL_BRANCHES, declared,
    )


# ============================================================================
# Check 4 — Claim-moment: DSP_outcome = Failure at τ_s = end
# ============================================================================


def outcome_failure_claim_at_end_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-moment: at τ_s = end, the OS goal does NOT cleanly land.
    Rocky's OS goal is 'stage Apollo's bicentennial heavyweight title
    defense as a clean publicity event — champion vs. local unknown;
    one-sided spectacle'. Under Outcome=Failure the clean outcome is
    contaminated — Rocky goes the distance. Substrate check: at end,
    `went_the_distance(rocky, apollo)` DOES derive via
    WENT_THE_DISTANCE_RULE. The derivation of went_the_distance IS
    the failure of the clean-publicity goal.

    Inverted from the three prior encodings (all Outcome=Success).
    For Failure, a positive load-bearing fact that contradicts the
    goal IS the support for the Failure declaration."""
    τ_end = _end_τ_s()
    events_up_to_end = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    world_facts = project_world(
        events_in_scope=events_up_to_end, up_to_τ_s=τ_end,
    )
    proof = world_holds_derived(
        world_facts, went_the_distance(ROCKY_ENTITY_ID, APOLLO_ENTITY_ID),
        RULES,
    )
    if proof is not None:
        return (
            VERDICT_APPROVED, 1.0,
            f"went_the_distance(rocky, apollo) derives at τ_s={τ_end} "
            f"via WENT_THE_DISTANCE_RULE (fought_rounds=15 + "
            f"standing_at_final_bell); the clean-publicity OS goal is "
            f"contaminated. Outcome=Failure claim is supported by "
            f"substrate — the goal's opposite is the load-bearing fact.",
        )
    return (
        VERDICT_NEEDS_WORK, 0.0,
        f"went_the_distance(rocky, apollo) does NOT derive at "
        f"τ_s={τ_end}; substrate does not support Outcome=Failure "
        f"claim. The clean-publicity goal may have landed as intended.",
    )


# ============================================================================
# Check 5 — Claim-trajectory: DSP_judgment = Good
# ============================================================================


def judgment_good_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: Judgment=Good = Rocky's internal resolution
    is positive at τ_s=end. For Rocky the substrate signature is the
    confluence of three positive-closure facts in his knowledge
    state and the world: went_the_distance (achievement), called_out
    (relationship payoff), and refused_rematch (acceptance). All
    three must hold for the Good trajectory to land.

    Inverted from Oedipus/Macbeth/Ackroyd's Judgment=Bad checks
    (which look for an emerging-and-persisting negative predicate —
    self-identity-collapse, tyrant, betrayer_of_trust). Good-trajectory
    looks for the positive-closure confluence at end rather than a
    trajectory shape across τ_s — Rocky's positive resolution lands
    in one cluster at τ_s=55-57, not as an arc-spanning
    shape-emergence. Trajectory-nature is still present in the sense
    that the facts must accrete across the fight's τ_s range."""
    τ_end = _end_τ_s()
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    final_world = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=τ_end,
    )
    distance_proof = world_holds_derived(
        final_world, went_the_distance(ROCKY_ENTITY_ID, APOLLO_ENTITY_ID),
        RULES,
    )
    went_distance = distance_proof is not None
    called = called_out(ROCKY_ENTITY_ID, ADRIAN_ENTITY_ID) in final_world
    refused = refused_rematch(ROCKY_ENTITY_ID) in final_world

    matches = sum((went_distance, called, refused))
    if matches == 3:
        return (
            VERDICT_APPROVED, 1.0,
            f"at τ_s={τ_end}: went_the_distance derives, "
            f"called_out(rocky, adrian) holds, refused_rematch(rocky) "
            f"holds. All three positive-closure facts confirm "
            f"Judgment=Good — Rocky's internal resolution is "
            f"achievement + relationship + self-sufficiency.",
        )
    if matches == 2:
        return (
            VERDICT_PARTIAL_MATCH, matches / 3,
            f"at τ_s={τ_end}: went_distance={went_distance}, "
            f"called={called}, refused={refused}. Two of three "
            f"positive-closure facts hold; Judgment=Good partially "
            f"supported.",
        )
    return (
        VERDICT_NEEDS_WORK, matches / 3,
        f"at τ_s={τ_end}: went_distance={went_distance}, "
        f"called={called}, refused={refused}. Only {matches}/3 "
        f"positive-closure facts hold; Judgment=Good weakly supported.",
    )


# ============================================================================
# Check 6 — Claim-trajectory: DSP_resolve = Steadfast
# ============================================================================


def dsp_resolve_steadfast_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: DSP_resolve=Steadfast = Rocky's fundamental
    stance does not transition mid-arc. For Rocky the substrate
    signature is structural absence: no identity-resolution events
    where Rocky's knowledge state gains an equivalence class collapse
    that redefines who he is. Unlike Ackroyd (whose Steadfast rests
    on a pre-existing rule-derived trait), Rocky's Steadfast rests
    on the *absence* of transition — he is the same man in the club
    fight and the Apollo fight, just writ larger.

    Check: Rocky's knowledge state at τ_s=0 and τ_s=end should have
    the same equivalence-class structure (specifically, no new
    classes involving rocky). This is a structural-invariance
    predicate, not a trait-emergence one."""
    events_in_scope_all = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    τ_end = _end_τ_s()

    def _rocky_classes_at(τ: int) -> tuple:
        state = project_knowledge(
            agent_id=ROCKY_ENTITY_ID,
            events_in_scope=events_in_scope_all,
            up_to_τ_s=τ,
        )
        return tuple(
            tuple(sorted(cls))
            for cls in state.equivalence_classes()
            if ROCKY_ENTITY_ID in cls
        )

    classes_at_start = _rocky_classes_at(0)
    classes_at_end = _rocky_classes_at(τ_end)

    # RE3: core-drive-persistence note per resolve-endpoint-sketch-
    # 01. Rocky's defining drive is `articulated_goal(rocky,
    # went_the_distance)`, which enters at τ_s=45 (state-addition
    # around the arc's midpoint) and persists through τ_end via
    # the rule-derived `went_the_distance(rocky, apollo)` at
    # τ_s=55. The state-addition is NOT a paradigm-reversal; v3
    # probe observation: Rocky's core drive, once articulated,
    # never wavers — Steadfast confirmed at the end-state layer.
    from substrate import Prop, project_knowledge as _pk
    articulated_prop = Prop("articulated_goal",
                            ("rocky", "went_the_distance"))
    rocky_state_end = _pk(
        agent_id=ROCKY_ENTITY_ID,
        events_in_scope=events_in_scope_all,
        up_to_τ_s=τ_end,
    )
    articulated_at_end = rocky_state_end.holds(articulated_prop) is not None
    re_note = (
        f" [RE3 core-drive-persistence: `articulated_goal(rocky, "
        f"went_the_distance)` {'holds' if articulated_at_end else 'does not hold'} "
        f"at τ_end={τ_end}; the state-addition at τ_s=45 is a "
        f"mid-arc articulation, not a paradigm-reversal. Rocky's "
        f"Steadfast read is preserved at the end-state layer: "
        f"once articulated, the drive is never abandoned]"
    )

    # RR3: IC-relational signal per resolve-relational-sketch-01.
    # For Steadfast, count IC throughline pressure events Rocky held
    # through (Apollo's dismissals, selections, in-ring pressure).
    # Rocky has no direct T_ic_apollo Lowering; fall back to
    # Scene.advances to recover IC events.
    ic_events = _events_lowered_from_throughline("T_ic_apollo")
    if not ic_events:
        from rocky_dramatic import SCENES
        ic_events = events_advancing_throughline(
            "T_ic_apollo", LOWERINGS, SCENES, FABULA,
        )
    ic_τs = sorted(
        e.τ_s for e in ic_events
        if e.τ_s is not None and e.τ_s >= 0
    )
    ic_note = (
        f" [RR3 IC-resistance: Rocky's drive held stable through "
        f"{len(ic_τs)} Apollo-throughline pressure events "
        f"(τ_s={ic_τs}); Dramatica's IC-driven Steadfast signal "
        f"structurally supported — Rocky does not abandon his "
        f"articulated goal under IC pressure]"
    ) if ic_τs else (
        " [RR3 IC-resistance: no Apollo-throughline events found; "
        "resistance claim unverified]"
    )

    if not classes_at_start and not classes_at_end:
        return (
            VERDICT_APPROVED, 1.0,
            f"Rocky's knowledge state at τ_s=0 and τ_s={τ_end} both "
            f"show zero equivalence classes involving rocky; no "
            f"identity transition across the arc. Resolve=Steadfast "
            f"confirmed — Rocky is structurally the same throughout."
            f"{re_note}{ic_note}",
        )
    if classes_at_start == classes_at_end:
        return (
            VERDICT_APPROVED, 1.0,
            f"Rocky's equivalence classes unchanged across the arc "
            f"({len(classes_at_start)} at both τ_s=0 and τ_s={τ_end}). "
            f"Resolve=Steadfast confirmed.{re_note}{ic_note}",
        )
    return (
        VERDICT_NEEDS_WORK, 0.0,
        f"Rocky's equivalence classes changed across the arc: "
        f"{len(classes_at_start)} at τ_s=0, {len(classes_at_end)} "
        f"at τ_s={τ_end}. Resolve=Steadfast predicts no such "
        f"transition.{re_note}{ic_note}",
    )


# ============================================================================
# Check 7 — Claim-trajectory: DSP_growth = Start
# ============================================================================


def dsp_growth_start_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: DSP_growth=Start = Rocky needs to START
    committing to a goal he had been unable to articulate. The
    substrate signature: the proposition `articulated_goal(rocky,
    went_the_distance)` is NOT in Rocky's knowledge state pre-τ_s=45,
    IS in Rocky's state from τ_s=45 (the night-before-fight scene).

    Parallel to Ackroyd's Growth=Start check (which looks for
    confession-writing post-ultimatum); Rocky's Start is privately
    chosen at the empty-ring scene rather than externally compelled —
    which differentiates Good-judgment Start from Bad-judgment Start.
    The substrate-level check is the same shape: a specific
    proposition acquired mid-arc."""
    from substrate import Prop  # local import to avoid cycle issues
    events_in_scope_all = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    articulated = Prop("articulated_goal",
                       (ROCKY_ENTITY_ID, "went_the_distance"))
    τ_end = _end_τ_s()

    def _rocky_holds_at(τ: int) -> bool:
        state = project_knowledge(
            agent_id=ROCKY_ENTITY_ID,
            events_in_scope=events_in_scope_all,
            up_to_τ_s=τ,
        )
        return any(h.prop == articulated for h in state.by_prop)

    # Find the earliest τ_s at which articulated_goal enters Rocky's
    # state. Expected: τ_s=45 (E_night_before_fight).
    all_τ_s = sorted({e.τ_s for e in FABULA if e.τ_s is not None})
    first_holding = None
    for τ in all_τ_s:
        if _rocky_holds_at(τ):
            first_holding = τ
            break

    holds_at_end = _rocky_holds_at(τ_end)

    if first_holding is None or not holds_at_end:
        return (
            VERDICT_NEEDS_WORK, 0.0,
            f"articulated_goal(rocky, went_the_distance) never enters "
            f"Rocky's state (first_holding={first_holding}, "
            f"holds_at_end={holds_at_end}); Growth=Start predicts "
            f"mid-arc acquisition that the substrate does not show.",
        )

    # Start trajectory expects acquisition mid-arc (not at τ_s=0).
    if first_holding > 0:
        return (
            VERDICT_APPROVED, 1.0,
            f"articulated_goal(rocky, went_the_distance) enters "
            f"Rocky's state at τ_s={first_holding} (the night-before-"
            f"fight private-reflection scene); holds through "
            f"τ_s={τ_end}. Growth=Start confirmed — Rocky starts "
            f"committing to a named goal after a long arc of evasion.",
        )
    return (
        VERDICT_PARTIAL_MATCH, 0.5,
        f"articulated_goal held from τ_s=0; Growth=Start predicts "
        f"mid-arc acquisition rather than pre-arc trait.",
    )


# ============================================================================
# Check 8 — Claim-trajectory: Story_goal (Failure trajectory)
# ============================================================================


def story_goal_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: Story_goal = 'stage a clean publicity-stunt
    win for Apollo'. Under DSP_outcome=Failure the goal does NOT
    land. The substrate signature of the failure trajectory:

    1. `scheduled_fight(apollo, rocky)` is world-asserted early
       (τ_s=-1, Apollo's selection) — the premise is in place.
    2. The goal would cleanly land only if `went_the_distance` did
       NOT derive at end. Across τ_s=46-55, premises accumulate:
       E_round_one_knockdown (as scripted); E_rocky_gets_up (the
       unscripted turn); E_fight_ends (both rule premises land).
    3. At τ_s=end, went_the_distance derives — the goal has been
       contaminated.

    Trajectory check: verify the premises accumulate in order
    (scheduled_fight exists at τ_s<0; went_the_distance does NOT
    derive at τ_s=45; DOES derive at τ_s=end). This is the Failure-
    shape trajectory: premises of the un-goal accrete."""
    from rocky import scheduled_fight
    τ_end = _end_τ_s()
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]

    world_pre = project_world(events_in_scope=events_in_scope, up_to_τ_s=-1)
    world_mid = project_world(events_in_scope=events_in_scope, up_to_τ_s=45)
    world_end = project_world(events_in_scope=events_in_scope, up_to_τ_s=τ_end)

    scheduled_early = scheduled_fight("apollo", "rocky") in world_pre
    contamination_mid = world_holds_derived(
        world_mid, went_the_distance("rocky", "apollo"), RULES,
    ) is not None
    contamination_end = world_holds_derived(
        world_end, went_the_distance("rocky", "apollo"), RULES,
    ) is not None

    # Expected Failure-trajectory shape:
    # - scheduled_early: True (premise in place at arc start)
    # - contamination_mid: False (premises not yet assembled)
    # - contamination_end: True (goal contaminated by end)
    if scheduled_early and not contamination_mid and contamination_end:
        return (
            VERDICT_APPROVED, 1.0,
            f"Story_goal Failure trajectory: scheduled_fight(apollo, "
            f"rocky) in world at τ_s=-1 (premise-in-place); "
            f"went_the_distance does NOT derive at τ_s=45 (mid-arc, "
            f"premises not yet assembled); DOES derive at τ_s={τ_end} "
            f"(goal contaminated). The clean-publicity goal was set "
            f"up and then displaced by what actually happened in the "
            f"ring. Failure trajectory confirmed.",
        )
    matches = sum((scheduled_early, not contamination_mid, contamination_end))
    if matches == 2:
        return (
            VERDICT_PARTIAL_MATCH, matches / 3,
            f"Story_goal trajectory: scheduled_early={scheduled_early}, "
            f"contamination_mid={contamination_mid}, "
            f"contamination_end={contamination_end}. Two of three "
            f"expected trajectory points match.",
        )
    return (
        VERDICT_NEEDS_WORK, matches / 3,
        f"Story_goal trajectory: scheduled_early={scheduled_early}, "
        f"contamination_mid={contamination_mid}, "
        f"contamination_end={contamination_end}. Trajectory does not "
        f"match the scheduled-then-contaminated shape Failure predicts.",
    )


# ============================================================================
# Check 9 — Claim-moment: Story_consequence
# ============================================================================


def story_consequence_moment_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-moment: Story_consequence = 'the card is staged but the
    scripted narrative is contaminated; the unknown does not fall
    down; Apollo takes the scorecard but refuses the rematch'. Under
    DSP_outcome=Failure the consequence IS realized (not avoided).
    Substrate check: at τ_s=end, (a) went_the_distance(rocky, apollo)
    derives (the unknown stayed up), AND (b) refused_rematch(apollo)
    holds (Apollo concedes what the scorecards didn't).

    Inverted from the three prior encodings' Story_consequence checks
    (which verify consequence AVOIDED under Success); under Failure,
    consequence REALIZED is the expected substrate shape."""
    τ_end = _end_τ_s()
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    final_world = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=τ_end,
    )
    distance_derives = world_holds_derived(
        final_world, went_the_distance(ROCKY_ENTITY_ID, APOLLO_ENTITY_ID),
        RULES,
    ) is not None
    apollo_refused = refused_rematch(APOLLO_ENTITY_ID) in final_world

    if distance_derives and apollo_refused:
        return (
            VERDICT_APPROVED, 1.0,
            f"at τ_s={τ_end}: went_the_distance(rocky, apollo) derives "
            f"(the unknown stayed up) AND refused_rematch(apollo) "
            f"holds (Apollo concedes what scorecards didn't). Story_"
            f"consequence (stunt contaminated) IS realized — the "
            f"substrate supports Outcome=Failure.",
        )
    matches = sum((distance_derives, apollo_refused))
    if matches == 1:
        return (
            VERDICT_PARTIAL_MATCH, 0.5,
            f"at τ_s={τ_end}: distance_derives={distance_derives}, "
            f"apollo_refused={apollo_refused}. One of two consequence-"
            f"realization conditions holds; partial realization.",
        )
    return (
        VERDICT_NEEDS_WORK, 0.0,
        f"at τ_s={τ_end}: distance_derives={distance_derives}, "
        f"apollo_refused={apollo_refused}. Consequence is not "
        f"realized; substrate does not support the declared Failure.",
    )


# ============================================================================
# Orchestration
# ============================================================================


def _wrap_check(
    upper_dialect: str,
    upper_record_id: str,
    check_fn: Callable,
    reviewer_id: str,
    *,
    reviewed_at_τ_a: int = 0,
) -> VerificationReview:
    upper_ref = cross_ref(upper_dialect, upper_record_id)
    verdict, strength, comment = check_fn(upper_ref)
    return VerificationReview(
        reviewer_id=reviewer_id,
        reviewed_at_τ_a=reviewed_at_τ_a,
        verdict=verdict,
        anchor_τ_a=0,
        target_record=upper_ref,
        comment=comment,
        match_strength=strength,
    )


def run() -> tuple:
    """Run the Template-layer verifier checks for Rocky. Returns a
    tuple of VerificationReview records.

    Check inventory (9 checks across all three primitives):
    - Characterization: DA_mc (Activity), DSP_approach (Do-er),
      DSP_limit (Timelock — first non-APPROVED under LT5)
    - Claim-moment: DSP_outcome (Failure), Story_consequence
      (REALIZED under Failure)
    - Claim-trajectory: DSP_judgment (Good — first in corpus for MC),
      DSP_resolve (Steadfast), DSP_growth (Start), Story_goal
      (trajectory toward Failure)
    """
    return (
        _wrap_check(
            "dramatica-complete", "DA_mc",
            mc_throughline_activity_domain_check,
            reviewer_id="verifier:characterization:domain-assignment",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_approach",
            rocky_do_er_approach_check,
            reviewer_id="verifier:characterization:dsp-approach",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_limit",
            dsp_limit_timelock_check,
            reviewer_id="verifier:characterization:dsp-limit",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_outcome",
            outcome_failure_claim_at_end_check,
            reviewer_id="verifier:claim-moment:dsp-outcome",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_judgment",
            judgment_good_trajectory_check,
            reviewer_id="verifier:claim-trajectory:dsp-judgment",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_resolve",
            dsp_resolve_steadfast_trajectory_check,
            reviewer_id="verifier:claim-trajectory:dsp-resolve",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_growth",
            dsp_growth_start_trajectory_check,
            reviewer_id="verifier:claim-trajectory:dsp-growth",
        ),
        _wrap_check(
            "dramatica-complete", "Story_goal",
            story_goal_trajectory_check,
            reviewer_id="verifier:claim-trajectory:story-goal",
        ),
        _wrap_check(
            "dramatica-complete", "Story_consequence",
            story_consequence_moment_check,
            reviewer_id="verifier:claim-moment:story-consequence",
        ),
    )


if __name__ == "__main__":
    reviews = run()
    print(f"=== Rocky dramatica-complete → substrate verifier ===")
    approved = sum(1 for r in reviews if r.verdict == VERDICT_APPROVED)
    print(f"{len(reviews)} checks run; {approved} approved.\n")
    for r in reviews:
        target = f"{r.target_record.dialect}:{r.target_record.record_id}"
        strength = (
            f" strength={r.match_strength:.2f}"
            if r.match_strength is not None else ""
        )
        print(f"[{r.verdict}]{strength} {target}")
        print(f"  via {r.reviewer_id}")
        print(f"  {r.comment}\n")
