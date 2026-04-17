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
from typing import Callable, Optional

# Substrate-side imports.
from substrate import (
    Entity, Event, CANONICAL,
    project_world, in_scope,
    world_holds_derived, world_holds_literal,
)
from ackroyd import (
    FABULA, ENTITIES, RULES, ALL_BRANCHES,
    killed, dead, betrayer_of_trust,
)

# Dramatic-side imports.
from dramatic import Throughline, Character
from ackroyd_dramatic import THROUGHLINES, CHARACTERS, STORY

# Template-side imports.
from dramatica_template import (
    DomainAssignment, DynamicStoryPoint, DSPAxis,
    Domain, Approach, Outcome, Judgment,
)
from ackroyd_dramatica_complete import (
    DOMAIN_ASSIGNMENTS, DYNAMIC_STORY_POINTS,
)

# Lowering + verifier-primitive machinery.
from lowering import (
    CrossDialectRef, cross_ref, LoweringStatus,
)
from ackroyd_lowerings import LOWERINGS
from verification import (
    VerificationReview, StructuralAdvisory,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH,
    VERDICT_NOTED,
    SEVERITY_NOTED,
)
from verifier_helpers import (
    classify_event_action_shape, agent_ids_from_entities,
)


# ============================================================================
# Encoding-bound helpers
# ============================================================================


SHEPPARD_ENTITY_ID = "sheppard"
ACKROYD_ENTITY_ID = "ackroyd"
_AGENT_IDS = agent_ids_from_entities(ENTITIES)


def _end_τ_s() -> int:
    return max(e.τ_s for e in FABULA if e.τ_s is not None)


def _events_lowered_from_throughline(throughline_id: str) -> tuple:
    """Same helper as the Macbeth / Oedipus verifiers; encoding-
    agnostic logic with Ackroyd's LOWERINGS as source."""
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
    domain. Substrate check: of events reached via L_mc_throughline,
    count manipulation-kind (concealment, scheming, staging,
    endgame-as-concealment)."""
    events = _events_lowered_from_throughline("T_mc_sheppard")
    if not events:
        return (
            VERDICT_NOTED, None,
            "T_mc_sheppard has no ACTIVE substrate-event Lowerings; "
            "DomainAssignment check cannot evaluate",
        )
    total = len(events)
    manip_count = sum(
        1 for e in events if _event_kind(e) in MANIPULATION_KINDS
    )
    ratio = manip_count / total
    if ratio >= 0.7:
        return (
            VERDICT_APPROVED, ratio,
            f"{manip_count}/{total} ({ratio:.0%}) MC-Throughline "
            f"events are manipulation-kind (blackmail, preparation, "
            f"staged_disclosure, killing-as-endgame, "
            f"confession-writing, suicide-as-concealment). Consistent "
            f"with Manipulation domain.",
        )
    if ratio >= 0.4:
        return (
            VERDICT_PARTIAL_MATCH, ratio,
            f"{manip_count}/{total} ({ratio:.0%}) MC-Throughline "
            f"events are manipulation-kind; the remainder are "
            f"investigatory / discovery events that document the "
            f"scheme rather than enact it.",
        )
    return (
        VERDICT_NEEDS_WORK, ratio,
        f"only {manip_count}/{total} ({ratio:.0%}) MC-Throughline "
        f"events are manipulation-kind. Manipulation domain "
        f"classification is weakly supported by substrate.",
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
    τ_end = _end_τ_s()
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
    τ_end = _end_τ_s()
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
    """Run the four Template-layer verifier checks for Ackroyd."""
    return (
        _wrap_check(
            "dramatica-complete", "DA_mc",
            mc_throughline_manipulation_domain_check,
            reviewer_id="verifier:characterization:domain-assignment",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_approach",
            sheppard_be_er_approach_check,
            reviewer_id="verifier:characterization:dsp-approach",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_outcome",
            outcome_success_claim_at_end_check,
            reviewer_id="verifier:claim-moment:dsp-outcome",
        ),
        _wrap_check(
            "dramatica-complete", "DSP_judgment",
            judgment_bad_trajectory_check,
            reviewer_id="verifier:claim-trajectory:dsp-judgment",
        ),
    )


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
