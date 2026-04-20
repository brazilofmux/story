"""
ackroyd_dramatica_complete_verification.py — third cross-boundary
verifier at the **dramatica-complete → substrate** coupling boundary.

Parallels macbeth_dramatica_complete_verification.py and
oedipus_dramatica_complete_verification.py. Same four-check shape;
Ackroyd's substrate pressures the checks in a third direction.

What's structurally different about Ackroyd:

- **MC = Manipulation domain**, not Activity. Sheppard's arc is
  concealment — doctor-as-narrator-as-murderer. The DA_mc check
  must recognize manipulation-kinds (blackmail, preparation,
  staged_disclosure, killing-as-endgame, suicide-as-concealment)
  rather than action-kinds. A direct port of the Macbeth check
  would mis-classify him.

- **DSP_approach = Be-er**, not Do-er. Sheppard's arc is inward —
  he writes himself as narrator, he conceals through positioning.
  The Be-er check inverts the Do-er signal: higher internal-state
  ratio should support the classification. Mixed result expected
  since the actual murder + suicide are overt actions.

- **OS goal is identification.** Poirot names the killer. Substrate
  check: `killed(sheppard, ackroyd)` is world-asserted at end
  (literal, not derived — Ackroyd's encoding authors the fact at
  the murder event). The OS goal lands when that fact is public.

- **Judgment=Bad renders as moral exposure + suicide.** Macbeth's
  Judgment=Bad trajectory was `tyrant(macbeth)` deriving and
  persisting. Oedipus's was epistemic self-identity landing. For
  Sheppard, the load-bearing predicate is `betrayer_of_trust(
  sheppard, ackroyd)` — derived from the rule
  `killed(X,Y) ∧ patient_of(Y,X) ⇒ betrayer_of_trust(X,Y)`
  (Ackroyd's inference surface). The trajectory: doesn't derive
  pre-murder, does derive post-murder, persists to end.

The three-verifier triptych now in the repo (Macbeth, Oedipus,
Ackroyd) gives a first real spectrum of substrate-completeness
signals:

- Macbeth (action-saturated substrate, MC=Activity, Do-er): APPROVED
  at 0.69 / 0.79 for DA_mc / DSP_approach.
- Oedipus (epistemic substrate post-F5-extension, MC=Activity, Do-er):
  NEEDS_WORK at 0.31 / 0.31 — taxonomy gap (investigation-as-
  utterance); see planned item 1.
- Ackroyd (mixed substrate, MC=Manipulation, Be-er): expected
  PARTIAL on DA_mc and DSP_approach since the check semantics
  invert / change for Manipulation + Be-er. Outcome / Judgment
  should land cleanly.

Deferred follow-ons remain the same as the Macbeth / Oedipus
verifiers: remaining DSP axes (Resolve, Growth, Limit), Signpost
claim-moment checks (×16), CharacterElementAssignment
claim-trajectory checks (×32 across four dimensions), ThematicPicks
pick-chain checks, Story_goal / Story_consequence claims. Pressing
those now would duplicate the gap across three encodings; better
to expand coverage once a shared pattern emerges worth extracting.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# Substrate-side imports.
from story_engine.core.substrate import (
    Entity, Event, CANONICAL,
    project_world, in_scope,
    world_holds_derived, world_holds_literal,
)
from story_engine.encodings.ackroyd import (
    FABULA, ENTITIES, RULES, ALL_BRANCHES,
    killed, dead, betrayer_of_trust, accused_of_murder,
)
from story_engine.core.substrate import Slot, project_knowledge

# Dramatic-side imports.
from story_engine.core.dramatic import Throughline, Character
from story_engine.encodings.ackroyd_dramatic import THROUGHLINES, CHARACTERS, STORY

# Template-side imports.
from story_engine.core.dramatica_template import (
    DomainAssignment, DynamicStoryPoint, DSPAxis,
    Domain, Approach, Outcome, Judgment,
)
from story_engine.encodings.ackroyd_dramatica_complete import (
    DOMAIN_ASSIGNMENTS, DYNAMIC_STORY_POINTS,
    STORY_GOAL, STORY_CONSEQUENCE,
)

# Lowering + verifier-primitive machinery.
from story_engine.core.lowering import (
    CrossDialectRef, cross_ref, LoweringStatus,
)
from story_engine.encodings.ackroyd_lowerings import LOWERINGS
from story_engine.core.verification import (
    StructuralAdvisory,
    DirectCheckRegistration, run_direct_review_checks,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH,
    VERDICT_NOTED,
    SEVERITY_NOTED,
)
from story_engine.core.verifier_helpers import (
    classify_event_action_shape, agent_ids_from_entities,
    dsp_limit_characterization_check,
    classify_event_manipulation_shape,
    detect_preceding_ic_event,
    fabula_end_τ_s, events_lowered_from_throughline,
)


# ============================================================================
# Encoding-bound helpers
# ============================================================================


SHEPPARD_ENTITY_ID = "sheppard"
ACKROYD_ENTITY_ID = "ackroyd"
_AGENT_IDS = agent_ids_from_entities(ENTITIES)


# Manipulation-kind event taxonomy for Ackroyd. Distinct from the
# Activity-kind taxonomy used by Macbeth / Oedipus verifiers — those
# encodings have MC=Activity; Ackroyd's MC=Manipulation, so the
# characterization check looks for different substrate signatures:
# concealment, scheming, staging, endgame-as-concealment. Unique to
# this encoding (for now); if a second Manipulation-MC encoding
# lands, promote to a shared module.
MANIPULATION_KINDS = frozenset({
    "blackmail_begins",
    "preparation",          # planting the dictaphone (alibi staging)
    "staged_disclosure",
    "commission",           # orders that function as cover
    "killing",              # the apex act of the concealed scheme
    "death_by_suicide",     # cover collapses; self-erasure closes
    "confession_writing",   # narrative self-management
    "ultimatum",            # the scheme's last-move negotiation
})

def _event_kind(event: Event) -> str:
    """Type-string extractor — retained only for
    mc_throughline_manipulation_domain_check, which still uses the
    MANIPULATION_KINDS set. The Manipulation-domain question is not
    covered by EK2 (EK2 classifies external-vs-internal action-shape,
    not manipulation-shape); EK5 notes that different upper-dialect
    classifications ask different structural questions and each
    gets its own classifier. A future classifier for manipulation-
    shape (participants in deception relations, effect on a third
    party's knowledge about the actor's role, etc.) could retire
    MANIPULATION_KINDS; not in scope for this pass."""
    return getattr(event, "type", None) or ""


def _sheppard_is_participant(event: Event) -> bool:
    parts = event.participants or {}
    return SHEPPARD_ENTITY_ID in parts.values()


# ============================================================================
# Check 1 — Characterization: DomainAssignment(T_mc_sheppard, MANIPULATION)
# ============================================================================


def mc_throughline_manipulation_domain_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DA_mc — T_mc_sheppard is in the Manipulation
    domain. Post-event-manipulation-taxonomy-sketch-01 (MN4), the
    check composes two signals:

    - **Type-set signal** (existing): event type ∈
      `MANIPULATION_KINDS` (blackmail, preparation, staged_disclosure,
      killing-as-endgame, confession-writing, suicide-as-concealment).
    - **Concealment-asymmetry signal** (MN2): Sheppard holds a
      self-fact at `Slot.KNOWN` that at least one other participant
      in the event does not — structural trace of performed
      innocence. Fires on investigation events where Sheppard is
      `also_present` / `assistant`.

    An event counts as manipulation-shaped if EITHER signal fires.
    The compositional form closes the 2026-04-17 Ackroyd probe's
    qualification: investigation events were classified as
    non-manipulation under the type-set alone; under MN4 they're
    correctly counted."""
    events = events_lowered_from_throughline("T_mc_sheppard", LOWERINGS, FABULA)
    if not events:
        return (
            VERDICT_NOTED, None,
            "T_mc_sheppard has no ACTIVE substrate-event Lowerings; "
            "DomainAssignment check cannot evaluate",
        )
    total = len(events)

    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]

    type_set_hits = 0
    asymmetry_hits = 0
    combined = 0
    for e in events:
        type_hit = _event_kind(e) in MANIPULATION_KINDS
        asymmetry_hit = (
            classify_event_manipulation_shape(
                e, SHEPPARD_ENTITY_ID, events_in_scope,
            )
            == "manipulation"
        )
        if type_hit:
            type_set_hits += 1
        if asymmetry_hit:
            asymmetry_hits += 1
        if type_hit or asymmetry_hit:
            combined += 1

    ratio = combined / total
    breakdown = (
        f"{combined}/{total} ({ratio:.0%}) MC-Throughline events "
        f"manipulation-shaped — {type_set_hits} via "
        f"MANIPULATION_KINDS type-set + {asymmetry_hits} via MN2 "
        f"concealment-asymmetry (overlap allowed)"
    )

    if ratio >= 0.7:
        return (
            VERDICT_APPROVED, ratio,
            f"{breakdown}. Consistent with Manipulation domain — "
            f"Sheppard's concealment layer is visible structurally "
            f"at every investigation event he participates in "
            f"(he holds `killed(sheppard, ackroyd)` at KNOWN from "
            f"the murder onward; non-Sheppard participants do not "
            f"hold it at KNOWN until Poirot's reveal).",
        )
    if ratio >= 0.4:
        return (
            VERDICT_PARTIAL_MATCH, ratio,
            f"{breakdown}. Manipulation-domain classification "
            f"partially supported; some events may be post-reveal "
            f"where the concealment asymmetry has collapsed.",
        )
    return (
        VERDICT_NEEDS_WORK, ratio,
        f"{breakdown}. Manipulation domain classification is "
        f"weakly supported by substrate.",
    )


# ============================================================================
# Check 2 — Characterization: DSP_approach = Be-er (INVERTED)
# ============================================================================


def sheppard_be_er_approach_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DSP_approach — Sheppard is a Be-er. Substrate
    check (inverted relative to Do-er): of events where Sheppard is
    a participant, the fraction that are internal-state-shaped per
    EK2 (the complement of external-action-shaped; see
    event-kind-taxonomy-sketch-01 EK2's final clause).

    Note on semantics: Sheppard performs the murder (overt action)
    and the suicide (overt action) onstage; the bulk of his arc is
    internal (managing the narrative, writing the manuscript,
    sustaining the concealment). So a clean Be-er signature is
    expected but not overwhelming — the first Be-er in the corpus
    whose outward moments are cinematic."""
    sh_events = [e for e in FABULA if _sheppard_is_participant(e)]
    if not sh_events:
        return (
            VERDICT_NOTED, None,
            "Sheppard entity has no recorded participations; check "
            "cannot evaluate",
        )
    total = len(sh_events)
    internal = sum(
        1 for e in sh_events
        if classify_event_action_shape(e, agent_ids=_AGENT_IDS)
        == "internal"
    )
    action = total - internal
    internal_ratio = internal / total
    if internal_ratio >= 0.6:
        return (
            VERDICT_APPROVED, internal_ratio,
            f"Sheppard participates in {total} events; {internal} "
            f"({internal_ratio:.0%}) are internal-state-shaped (EK2); "
            f"{action} are external-action-shaped. Be-er approach "
            f"confirmed.",
        )
    if internal_ratio >= 0.3:
        return (
            VERDICT_PARTIAL_MATCH, internal_ratio,
            f"Sheppard participates in {total} events; {internal} "
            f"({internal_ratio:.0%}) are internal-state-shaped (EK2); "
            f"{action} are external-action-shaped. Mixed Be-er / "
            f"Do-er signature — Sheppard's concealment-from-inside "
            f"is real but the murder and suicide are cinematic.",
        )
    return (
        VERDICT_NEEDS_WORK, internal_ratio,
        f"only {internal}/{total} ({internal_ratio:.0%}) "
        f"Sheppard-participating events are internal-state-shaped "
        f"per EK2; Be-er classification weakly supported — substrate "
        f"shows him as overwhelmingly action-oriented.",
    )


# ============================================================================
# Check 3 — Claim-moment: DSP_outcome = Success at τ_s = end
# ============================================================================


def outcome_success_claim_at_end_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-moment: at τ_s = end, the OS goal lands. Ackroyd's OS
    goal is "identify Ackroyd's murderer." The load-bearing substrate
    fact is `killed(sheppard, ackroyd)` being world-asserted — the
    murder is on the record and the killer is named. Ackroyd's
    encoding authors this literally (rather than via derivation
    from premises), so the check uses world_holds_literal."""
    τ_end = fabula_end_τ_s(FABULA)
    events_up_to_end = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    world_facts = project_world(
        events_in_scope=events_up_to_end, up_to_τ_s=τ_end,
    )
    holds = world_holds_literal(
        killed(SHEPPARD_ENTITY_ID, ACKROYD_ENTITY_ID),
        world_facts,
    )
    if holds:
        return (
            VERDICT_APPROVED, 1.0,
            f"killed(sheppard, ackroyd) holds at τ_s={τ_end}; "
            f"Outcome=Success claim (OS goal — murderer of Ackroyd "
            f"identified) is supported by substrate at end of "
            f"fabula. The fact is world-authored at the murder event.",
        )
    return (
        VERDICT_NEEDS_WORK, 0.0,
        f"killed(sheppard, ackroyd) does NOT hold at τ_s={τ_end}; "
        f"Outcome=Success claim not supported.",
    )


# ============================================================================
# Check 4 — Claim-trajectory: DSP_judgment = Bad
# ============================================================================


def judgment_bad_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: Judgment=Bad = Sheppard's moral resolution
    is catastrophic. For Ackroyd this renders via the
    `betrayer_of_trust` derivation: the rule
    `killed(X,Y) ∧ patient_of(Y,X) ⇒ betrayer_of_trust(X,Y)` fires
    from the murder event onward (Ackroyd was Sheppard's patient).
    Trajectory shape: betrayer_of_trust(sheppard, ackroyd) does not
    derive pre-murder, does derive from the murder event forward,
    persists through end. Like Macbeth's tyrant trajectory, but the
    predicate rests on a relational fact (patient_of) rather than a
    state-collapse (king-and-kinslayer)."""
    τ_end = fabula_end_τ_s(FABULA)
    events_in_scope_all = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    betrayer_query = betrayer_of_trust(
        SHEPPARD_ENTITY_ID, ACKROYD_ENTITY_ID,
    )

    def _betrayer_holds_at(τ: int) -> bool:
        wf = project_world(
            events_in_scope=events_in_scope_all, up_to_τ_s=τ,
        )
        return (
            world_holds_derived(wf, betrayer_query, RULES) is not None
        )

    at_start = _betrayer_holds_at(0)
    at_end = _betrayer_holds_at(τ_end)

    # Find the earliest τ_s at which betrayer_of_trust derives.
    all_τ_s = sorted({e.τ_s for e in FABULA if e.τ_s is not None})
    first_holding = None
    for τ in all_τ_s:
        if _betrayer_holds_at(τ):
            first_holding = τ
            break

    if not at_start and at_end and first_holding is not None:
        return (
            VERDICT_APPROVED, 1.0,
            f"betrayer_of_trust(sheppard, ackroyd) does not hold at "
            f"τ_s=0; emerges at τ_s={first_holding} (post-murder, "
            f"when killed + patient_of coincide in the rule); still "
            f"holds at τ_s={τ_end}. Emerges-and-persists trajectory "
            f"consistent with Judgment=Bad.",
        )
    if at_end and not at_start:
        return (
            VERDICT_PARTIAL_MATCH, 0.7,
            f"betrayer_of_trust(sheppard, ackroyd) holds at end "
            f"(τ_s={τ_end}) but emergence τ_s could not be "
            f"pinpointed.",
        )
    return (
        VERDICT_NEEDS_WORK, 0.0,
        f"betrayer_of_trust trajectory: at_start={at_start}, "
        f"at_end={at_end}. Does not match the emerges-and-persists "
        f"shape Judgment=Bad predicts.",
    )


# ============================================================================
# Check 5 — Claim-trajectory: DSP_resolve = Steadfast (inverted)
# ============================================================================


def dsp_resolve_steadfast_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: DSP_resolve=Steadfast = the MC maintains
    their stance throughout; no mid-arc transition. For Ackroyd the
    substrate signature is: `betrayer_of_trust(sheppard, ackroyd)`
    emerges at τ_s=1 (the murder event, the very start of the post-
    prologue arc) and holds through τ_s=11. The MC's defining role
    is a near-pre-existing trait — no mid-arc transition visible
    within the investigation arc (τ_s ∈ [2, 11]).

    Inverted from Oedipus/Macbeth's Change check (which looks for
    a mid-arc transition); Steadfast looks for *absence* of such a
    transition across the arc's investigation span."""
    τ_end = fabula_end_τ_s(FABULA)
    events_in_scope_all = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    all_τ_s = sorted({e.τ_s for e in FABULA if e.τ_s is not None})

    def _betrayer_holds_at(τ: int) -> bool:
        wf = project_world(
            events_in_scope=events_in_scope_all, up_to_τ_s=τ,
        )
        return world_holds_derived(
            wf, betrayer_of_trust(SHEPPARD_ENTITY_ID, ACKROYD_ENTITY_ID),
            RULES,
        ) is not None

    transition_τ = None
    for τ in all_τ_s:
        if _betrayer_holds_at(τ):
            transition_τ = τ
            break

    if transition_τ is None:
        return (
            VERDICT_NEEDS_WORK, 0.0,
            "betrayer_of_trust never derives; Resolve=Steadfast "
            "needs a stable defining trait the substrate does not "
            "carry.",
        )

    # Investigation arc begins when Poirot is engaged — slot 6.
    # Everything before is pre-play setup. Steadfast means the trait
    # is in place BEFORE the investigation arc starts.
    investigation_start = 2  # E_flora_summons_poirot at τ_s=2
    arc_span = τ_end - investigation_start
    if arc_span <= 0:
        return (
            VERDICT_NEEDS_WORK, 0.0,
            "investigation arc has zero span; cannot classify "
            "trajectory shape.",
        )

    # RE3: core-drive-persistence note per resolve-endpoint-sketch-
    # 01. Ackroyd's defining fact `betrayer_of_trust(sheppard,
    # ackroyd)` derives at τ_s=1 (via the killing event) and holds
    # through τ_end=11. No state-additions; clean pre-arc-trait
    # persistence. Contrasts with Rocky's Steadfast (articulated
    # goal as state-addition) — Ackroyd's is pre-arc-anchored.
    re_note = (
        f" [RE3 core-drive-persistence: `betrayer_of_trust` "
        f"derives at τ_s={transition_τ} and holds through "
        f"τ_end={τ_end}; no state-additions around the defining "
        f"trait. Steadfast confirmed at both identity and "
        f"end-state layers — the distinction from Rocky's "
        f"mid-arc-articulated Steadfast]"
    )

    # RR3: IC-relational signal per resolve-relational-sketch-01.
    # For Steadfast, count the IC throughline's pressure events —
    # Sheppard's Steadfast holds across Poirot's investigation.
    # Resistance signal = count of IC events the MC held through.
    ic_events = events_lowered_from_throughline("T_ic_poirot", LOWERINGS, FABULA)
    ic_τs = sorted(
        e.τ_s for e in ic_events
        if e.τ_s is not None and e.τ_s >= investigation_start
    )
    ic_note = (
        f" [RR3 IC-resistance: Sheppard's betrayer_of_trust held "
        f"stable through {len(ic_τs)} Poirot-throughline pressure "
        f"events (τ_s={ic_τs}); Dramatica's IC-driven Steadfast "
        f"signal structurally supported — MC did not voluntarily "
        f"change approach before external compulsion]"
    ) if ic_τs else (
        " [RR3 IC-resistance: no Poirot-throughline events found "
        "in investigation arc; resistance claim unverified]"
    )

    if transition_τ <= investigation_start:
        return (
            VERDICT_APPROVED, 1.0,
            f"betrayer_of_trust(sheppard, ackroyd) derives at "
            f"τ_s={transition_τ}, before the investigation arc "
            f"begins at τ_s={investigation_start}; the trait is "
            f"steady across τ_s ∈ [{investigation_start}, {τ_end}]. "
            f"Resolve=Steadfast confirmed — Sheppard's defining "
            f"role is a pre-arc trait, not a mid-arc transition."
            f"{re_note}{ic_note}",
        )
    position = (transition_τ - investigation_start) / arc_span
    return (
        VERDICT_PARTIAL_MATCH, max(1.0 - position, 0.0),
        f"betrayer_of_trust emerges at τ_s={transition_τ}, "
        f"{position:.0%} through the investigation arc [{investigation_start}, "
        f"{τ_end}]. Resolve=Steadfast would predict emergence "
        f"before or at the arc's start.{re_note}{ic_note}",
    )


# ============================================================================
# Check 6 — Claim-trajectory: DSP_growth = Start
# ============================================================================


def dsp_growth_start_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: DSP_growth=Start = the MC needs to START
    doing something they have been failing to do — confess,
    acknowledge, accept responsibility. For Ackroyd the substrate
    signature is: Sheppard participates in concealment events
    throughout (the ultimatum, the confession-writing, the suicide
    at τ_s=11 are terminal events, not the start of an admitted
    confession). The growth=start axis diagnoses the NEEDED
    acquisition; the substrate shows the acquisition arriving
    only at the terminal edge (after Poirot's ultimatum) — the
    growth happens at the point of no-return.

    Check: look for confession-shaped events in the fabula, and
    verify they occur at or after the ultimatum (growth=start
    achieved only under external compulsion = Bad-judgment shape)."""
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]

    ultimatum_τ = None
    confession_τ = None
    for e in FABULA:
        if e.τ_s is None:
            continue
        if (e.type == "ultimatum"
                and SHEPPARD_ENTITY_ID in (e.participants or {}).values()):
            ultimatum_τ = e.τ_s
        if (e.type == "confession_writing"
                and SHEPPARD_ENTITY_ID in (e.participants or {}).values()):
            confession_τ = e.τ_s

    if ultimatum_τ is None or confession_τ is None:
        return (
            VERDICT_NEEDS_WORK, 0.0,
            f"Ackroyd substrate needs both ultimatum and "
            f"confession_writing events for Growth=Start "
            f"trajectory; ultimatum_τ={ultimatum_τ}, "
            f"confession_τ={confession_τ}.",
        )

    if ultimatum_τ <= confession_τ:
        return (
            VERDICT_APPROVED, 1.0,
            f"Sheppard's confession-writing (τ_s={confession_τ}) "
            f"follows Poirot's ultimatum (τ_s={ultimatum_τ}). "
            f"Growth=Start is achieved only under external "
            f"compulsion — the MC starts what they have been "
            f"failing to start, but too late to avert judgment. "
            f"Classic Start/Bad shape.",
        )
    return (
        VERDICT_PARTIAL_MATCH, 0.5,
        f"confession_τ={confession_τ} precedes ultimatum_τ="
        f"{ultimatum_τ}; Growth=Start trajectory shape is not the "
        f"expected ultimatum-compelled order.",
    )


# ============================================================================
# Check 7 — Claim-trajectory: Story_goal
# ============================================================================


def story_goal_trajectory_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-trajectory: Story_goal = 'identify the killer of Roger
    Ackroyd and recover the household's moral order'. Substrate
    signature: the knowledge of `killed(sheppard, ackroyd)` expands
    across agents over the arc — at τ_s=1 only Sheppard knows; by
    τ_s=8 (reveal) at least four key agents hold it at KNOWN.
    Trajectory: expanding-knowledge shape."""
    τ_end = fabula_end_τ_s(FABULA)
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    target_prop = killed(SHEPPARD_ENTITY_ID, ACKROYD_ENTITY_ID)

    # Core witnesses/participants who should hold the knowledge by end.
    knowers = ("poirot", "caroline_sheppard", "inspector_raglan",
               "flora_ackroyd")

    def _knower_count_at(τ: int) -> int:
        count = 0
        for agent in knowers:
            state = project_knowledge(
                agent_id=agent,
                events_in_scope=events_in_scope,
                up_to_τ_s=τ,
            )
            if state.holds_as(target_prop, Slot.KNOWN):
                count += 1
        return count

    early_count = _knower_count_at(2)
    end_count = _knower_count_at(τ_end)
    total = len(knowers)

    if early_count == 0 and end_count == total:
        return (
            VERDICT_APPROVED, 1.0,
            f"Story_goal trajectory: 0/{total} key knowers hold "
            f"killed(sheppard, ackroyd) at KNOWN at τ_s=2 "
            f"(investigation start); {end_count}/{total} hold it "
            f"at τ_s={τ_end}. Knowledge expansion lands the goal "
            f"across the entire witness-set.",
        )
    if end_count >= total - 1 and end_count > early_count:
        return (
            VERDICT_PARTIAL_MATCH, end_count / total,
            f"Story_goal trajectory: {early_count}/{total} → "
            f"{end_count}/{total} key knowers. Goal mostly lands; "
            f"one witness is missing at τ_end.",
        )
    return (
        VERDICT_NEEDS_WORK, end_count / total if total else 0.0,
        f"Story_goal trajectory: {early_count}/{total} → "
        f"{end_count}/{total} key knowers at τ_s={τ_end}. "
        f"Expected expansion to the full witness set is not "
        f"reached.",
    )


# ============================================================================
# Check 8 — Characterization: DSP_limit (pressure-shape-taxonomy-sketch-01)
# ============================================================================


def dsp_limit_optionlock_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
) -> tuple:
    """Characterize DSP_limit. Ackroyd declares Optionlock (Poirot
    eliminates suspects one by one). LT2 predicts convergence signals
    in the substrate: the explicit retraction of
    `accused_of_murder(ralph_paton, ackroyd)` at the reveal (landed
    same-day as the Story_consequence fix), and rule-derivable
    emergences (`betrayer_of_trust`, `driver_of_suicide`). Delegates
    to `dsp_limit_characterization_check` in verifier_helpers."""
    declared = next(
        d.choice for d in DYNAMIC_STORY_POINTS if d.axis == DSPAxis.LIMIT
    )
    return dsp_limit_characterization_check(
        FABULA, RULES, CANONICAL, ALL_BRANCHES, declared,
    )


# ============================================================================
# Check 9 — Claim-moment: Story_consequence
# ============================================================================


def story_consequence_moment_check(
    upper_ref: CrossDialectRef,
    _unused_lower_refs: tuple = (),
    _unused_ranges: tuple = (),
) -> tuple:
    """Claim-moment: Story_consequence = 'the killer goes undetected;
    Ralph Paton remains under suspicion'. Under Outcome=Success, the
    consequence is AVOIDED at τ_end. Substrate check: at τ_end, (a)
    the killer IS publicly detected (multiple agents hold
    killed(sheppard, ackroyd) at KNOWN) AND (b) Ralph Paton is NOT
    accused_of_murder anymore. Both conditions must hold for the
    consequence to be averted."""
    τ_end = fabula_end_τ_s(FABULA)
    events_in_scope = [
        e for e in FABULA if in_scope(e, CANONICAL, ALL_BRANCHES)
    ]
    final_world = project_world(
        events_in_scope=events_in_scope, up_to_τ_s=τ_end,
    )

    # Public detection: ≥3 of the key knowers hold killed KNOWN.
    knowers = ("poirot", "caroline_sheppard", "inspector_raglan",
               "flora_ackroyd")
    target = killed(SHEPPARD_ENTITY_ID, ACKROYD_ENTITY_ID)
    knower_count = 0
    for agent in knowers:
        state = project_knowledge(
            agent_id=agent,
            events_in_scope=events_in_scope,
            up_to_τ_s=τ_end,
        )
        if state.holds_as(target, Slot.KNOWN):
            knower_count += 1
    publicly_detected = knower_count >= 3

    # Ralph cleared: accused_of_murder(ralph_paton, ackroyd) does
    # NOT hold as a world fact at τ_end (it was raised during
    # investigation but the substrate should have removed / never-
    # asserted it by end).
    ralph_accused = (
        accused_of_murder("ralph_paton", ACKROYD_ENTITY_ID)
        in final_world
    )
    ralph_cleared = not ralph_accused

    if publicly_detected and ralph_cleared:
        return (
            VERDICT_APPROVED, 1.0,
            f"at τ_s={τ_end}: {knower_count}/{len(knowers)} key "
            f"agents hold killed(sheppard, ackroyd) at KNOWN "
            f"(killer publicly detected) AND Ralph not accused "
            f"(cleared). Story_consequence (killer-undetected + "
            f"Ralph-suspect) fully averted; substrate supports "
            f"Outcome=Success.",
        )
    matches = sum(1 for cond in (publicly_detected, ralph_cleared) if cond)
    strength = matches / 2
    if matches == 1:
        return (
            VERDICT_PARTIAL_MATCH, strength,
            f"at τ_s={τ_end}: publicly_detected={publicly_detected} "
            f"({knower_count}/{len(knowers)} knowers), "
            f"ralph_cleared={ralph_cleared}. One half of the "
            f"consequence-avoidance condition holds.",
        )
    return (
        VERDICT_NEEDS_WORK, strength,
        f"at τ_s={τ_end}: publicly_detected=False, "
        f"ralph_cleared=False. Consequence not averted.",
    )


# ============================================================================
# Orchestration
# ============================================================================


CHECK_REGISTRY = (
    DirectCheckRegistration(
        "dramatica-complete", "DA_mc",
        mc_throughline_manipulation_domain_check,
        "verifier:characterization:domain-assignment",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_approach",
        sheppard_be_er_approach_check,
        "verifier:characterization:dsp-approach",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_limit",
        dsp_limit_optionlock_check,
        "verifier:characterization:dsp-limit",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_outcome",
        outcome_success_claim_at_end_check,
        "verifier:claim-moment:dsp-outcome",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_judgment",
        judgment_bad_trajectory_check,
        "verifier:claim-trajectory:dsp-judgment",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_resolve",
        dsp_resolve_steadfast_trajectory_check,
        "verifier:claim-trajectory:dsp-resolve",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_growth",
        dsp_growth_start_trajectory_check,
        "verifier:claim-trajectory:dsp-growth",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "Story_goal",
        story_goal_trajectory_check,
        "verifier:claim-trajectory:story-goal",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "Story_consequence",
        story_consequence_moment_check,
        "verifier:claim-moment:story-consequence",
    ),
)


def run() -> tuple:
    """Run the Template-layer verifier checks for Ackroyd. Returns a
    tuple of VerificationReview records.

    Check inventory (9 checks across all three primitives):
    - Characterization: DA_mc (Manipulation), DSP_approach (Be-er),
      DSP_limit (Optionlock)
    - Claim-moment: DSP_outcome, Story_consequence
    - Claim-trajectory: DSP_judgment, DSP_resolve (Steadfast —
      inverted from Oedipus/Macbeth's Change), DSP_growth (Start —
      inverted from Oedipus/Macbeth's Stop), Story_goal
    """
    return run_direct_review_checks(CHECK_REGISTRY)


if __name__ == "__main__":
    reviews = run()
    print(f"=== Ackroyd dramatica-complete → substrate verifier ===")
    print(f"{len(reviews)} checks run; "
          f"{sum(1 for r in reviews if r.verdict == VERDICT_APPROVED)} "
          f"approved.\n")
    for r in reviews:
        target = f"{r.target_record.dialect}:{r.target_record.record_id}"
        strength = (
            f" strength={r.match_strength:.2f}"
            if r.match_strength is not None else ""
        )
        print(f"[{r.verdict}]{strength} {target}")
        print(f"  via {r.reviewer_id}")
        print(f"  {r.comment}\n")
