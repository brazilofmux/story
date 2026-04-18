"""
rashomon_dramatica_complete_verification.py — fifth cross-boundary
verifier at the **dramatica-complete → substrate** coupling boundary,
and the FIRST multi-Story verifier (per multi-story-sketch-01 MS4).

Prior verifiers (Macbeth, Oedipus, Ackroyd, Rocky) each ran against
a single-Story encoding. Rashomon runs per-Story across five Stories:

  - S_frame (the gate narrative — Dramatica-complete Template records
    but NO substrate lowerings; substrate scope is grove-only)
  - S_bandit_ver, S_wife_ver, S_samurai_ver, S_woodcutter_ver (the four
    contested testimonies — each skeletal with DomainAssignment +
    DSP_limit=Timelock)

Primary research question per the Substack article's section 8:
each testimony's DSP_limit is declared Timelock, staking the claim
that testimonies are "scheduled climaxes within their own narrative
arcs" (the duel, the violation, the suicide). What does LT9 (per
pressure-shape-taxonomy-sketch-02) detect against each testimony's
contested branch?

Per-Story scoping (MS4): for each testimony Story, the LT9 classifier
is run with the testimony's contested branch as the canonical scope
(B_TAJOMARU, B_WIFE, B_HUSBAND, B_WOODCUTTER). Canonical-is-universal
means the pre-divergence grove-setup events (E_lure, E_bind,
E_bring_wife, E_intercourse, E_husband_dead, E_body_found) are visible
on every testimony's scope; the testimony-specific events are only
visible on their own branch. This is exactly the scope a per-Story
verifier needs.

Frame Story verification: emitted as a single coordinating NOTED
verdict — the frame's DomainAssignments and DSPs are encoded, but no
ACTIVE Lowering binds them to substrate (the gate isn't in substrate
scope). Recorded for multi-Story completeness; no substrate signal
available.

What this verifier is built to surface, not hide:

- **DSP_limit=Timelock against a Timelock-declared testimony that
  happens to carry a substrate retraction in its middle arc.** The
  testimonies unbind the husband (retraction of `bound_to`) in three
  of four branches; the woodcutter branch does not. The retraction
  lands as an LT2 middle-arc signal against the author's Timelock
  declaration. This is exactly the sketch-01 vs sketch-02 disposition
  question: is a scheduled climax Timelock even when a mid-arc
  retraction looks Optionlock-shaped? The verifier does not decide;
  it reports the disagreement honestly.

- **Woodcutter testimony has no retraction.** Its LT2 signal count
  is zero. With no scheduling predicate either (LT8 inert), the
  verdict is NOTED (Timelock-consistent) per LT3's weak-fallback
  asymmetry. Among the four testimonies, this is the one whose
  substrate looks cleanly Timelock-shaped.

- **Two axes of asymmetry across the four testimonies.** First:
  retraction vs no-retraction (three testimonies unbind the husband;
  the woodcutter's account has the husband already dead by the time
  the fight begins, so no unbinding is needed — the structural detail
  that carries the verifier signal is also a plot detail). Second:
  event count differences activate (samurai, woodcutter: 5 and 4
  events with terminal band computed) vs do-not-activate (bandit,
  wife: 3 and 2 events, flat semantics) the LT7 terminal-band refinement.
  The verifier makes both axes visible.

Honest scope limit: this verifier does NOT test the frame Story's
declarations (DSP_limit=Optionlock, Outcome=Success, Judgment=Good)
against substrate — there is no substrate to test against. The
multi-Story extension's first real test is the testimony-side LT9
runs.
"""

from __future__ import annotations

from typing import Callable

from substrate import CANONICAL
from rashomon import (
    EVENTS_ALL, ALL_BRANCHES,
    B_TAJOMARU, B_WIFE, B_HUSBAND, B_WOODCUTTER,
)

from dramatica_template import DSPAxis, Limit
from rashomon_dramatic import (
    S_frame, S_bandit_ver, S_wife_ver, S_samurai_ver, S_woodcutter_ver,
)
from rashomon_dramatica_complete import (
    DYNAMIC_STORY_POINTS_BY_STORY,
)

from lowering import CrossDialectRef, cross_ref
from verification import (
    VerificationReview,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH,
    VERDICT_NOTED,
)
from verifier_helpers import dsp_limit_characterization_check


# ============================================================================
# Per-Story DSP_limit checks — each uses that Story's contested branch
# as the canonical scope for LT9.
# ============================================================================
#
# Rashomon's substrate has no compound rules (no `RULES` export), so
# each check passes an empty rules tuple. LT9's scheduling-predicate
# scan still runs; LT2's retraction / identity-resolution scans still
# run. Rule-derivable-emergence signals are structurally absent from
# Rashomon, which is correct — the grove scene does not carry compound
# derivations.


_NO_RULES: tuple = ()


def _run_testimony_dsp_limit_check(
    story_id: str,
    canonical_scope_branch,
) -> tuple:
    """Run the DSP_limit characterization check for a single testimony
    Story. Returns `(verdict, strength, comment)`. The testimony's
    contested branch is passed as `canonical_branch` — this is the
    per-Story MS4 scoping: the testimony's own events plus the
    canonical grove floor are in scope; the other testimonies are
    not."""
    dsp_limit = next(
        d for d in DYNAMIC_STORY_POINTS_BY_STORY[story_id]
        if d.axis == DSPAxis.LIMIT
    )
    declared = dsp_limit.choice
    return dsp_limit_characterization_check(
        EVENTS_ALL, _NO_RULES, canonical_scope_branch, ALL_BRANCHES,
        declared,
    )


def bandit_dsp_limit_check(upper_ref, _unused_lower_refs=()):
    """S_bandit_ver: DSP_limit=Timelock declared. LT9 runs against
    B_TAJOMARU scope (canonical grove events + Tajōmaru's branch events:
    wife-requests-killing, frees-husband, duel). The `frees-husband`
    event retracts `bound_to(husband, tree)` — an LT2 convergence signal.
    With 3 positive-τ_s events (flat semantics per LT7), this retraction
    lands in the middle-arc band → classification=optionlock →
    declaration/substrate disagreement."""
    return _run_testimony_dsp_limit_check(S_bandit_ver.id, B_TAJOMARU)


def wife_dsp_limit_check(upper_ref, _unused_lower_refs=()):
    """S_wife_ver: DSP_limit=Timelock declared. LT9 runs against B_WIFE
    scope. `tajomaru_leaves` retracts `at_location(tajomaru, ...)` —
    fold behavior determines whether this counts as an LT2 retraction
    (requires the prop to have been asserted prior). With 2 positive-τ_s
    events (flat semantics), this is the testimony with the smallest
    substrate surface — and the one where LT2 signal interpretation
    leans on what counts as a prior assertion."""
    return _run_testimony_dsp_limit_check(S_wife_ver.id, B_WIFE)


def samurai_dsp_limit_check(upper_ref, _unused_lower_refs=()):
    """S_samurai_ver: DSP_limit=Timelock declared. LT9 runs against
    B_HUSBAND scope. 5 positive-τ_s events (τ_s=7..11) — ENOUGH to
    activate LT7's terminal-band refinement. The `frees-husband`
    retraction at τ_s=10 lands middle-arc (terminal threshold ~10.6);
    the suicide at τ_s=11 lands terminal. Longest of the four
    testimonies; most LT7-sensitive."""
    return _run_testimony_dsp_limit_check(S_samurai_ver.id, B_HUSBAND)


def woodcutter_dsp_limit_check(upper_ref, _unused_lower_refs=()):
    """S_woodcutter_ver: DSP_limit=Timelock declared. LT9 runs against
    B_WOODCUTTER scope. The woodcutter's branch contains NO unbinding
    event — the husband's binding is not retracted on this branch
    because the fight proceeds while he's bound (or the woodcutter's
    account doesn't track it). With zero LT2 middle-arc signals AND no
    scheduling predicate (LT8 inert), LT3's honest weak-fallback fires
    → NOTED: Timelock-consistent but not affirmatively detected. Of
    the four testimonies, this is the one with the cleanest
    Timelock-compatible substrate."""
    return _run_testimony_dsp_limit_check(S_woodcutter_ver.id, B_WOODCUTTER)


# ============================================================================
# Frame Story — coordinating NOTED verdict
# ============================================================================


def frame_declarations_not_substrate_bound_check(upper_ref, _unused=()):
    """Frame Story carries full Dramatica-complete declarations (DA_frame_*,
    DSP_frame_*, Story_goal, Story_consequence) but no ACTIVE
    Lowerings binding them to substrate — the frame's gate narrative
    is not in rashomon.py's scope. Per MS4, per-Story verification
    acknowledges the encoding but cannot run substrate-based checks.
    Single NOTED verdict stands in for what would be 8+ individual
    NOTED verdicts if each DSP + the goal + the consequence were
    checked separately."""
    return (
        VERDICT_NOTED, None,
        "S_frame: full Template declarations (4 DomainAssignments, 6 "
        "DSPs, Story_goal, Story_consequence) are encoded, but all "
        "frame-Story Lowerings are PENDING — the Rashomon substrate "
        "scope is grove-only and does not model the gate narrative. "
        "No substrate-based verification possible for the frame "
        "Story's declarations. Per multi-story-sketch-01 MS4, the "
        "per-Story verifier reports this gap rather than producing "
        "spurious verdicts.",
    )


# ============================================================================
# Orchestration
# ============================================================================


def _wrap_check(
    story_id: str,
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
        reviewer_id=f"{reviewer_id}:story={story_id}",
        reviewed_at_τ_a=reviewed_at_τ_a,
        verdict=verdict,
        anchor_τ_a=0,
        target_record=upper_ref,
        comment=comment,
        match_strength=strength,
    )


def run() -> tuple:
    """Run the Template-layer verifier checks across all five Rashomon
    Stories per MS4.

    Check inventory:
    - S_frame: 1 coordinating NOTED verdict (no substrate to test against)
    - S_bandit_ver: DSP_limit=Timelock against B_TAJOMARU
    - S_wife_ver: DSP_limit=Timelock against B_WIFE
    - S_samurai_ver: DSP_limit=Timelock against B_HUSBAND
    - S_woodcutter_ver: DSP_limit=Timelock against B_WOODCUTTER

    5 checks total — one per Story, matching the multi-Story encoding's
    per-Story discipline.
    """
    return (
        _wrap_check(
            S_frame.id,
            "dramatica-complete", "DSP_frame_limit",
            frame_declarations_not_substrate_bound_check,
            reviewer_id="verifier:multi-story:frame-declarations",
        ),
        _wrap_check(
            S_bandit_ver.id,
            "dramatica-complete", "DSP_bandit_limit",
            bandit_dsp_limit_check,
            reviewer_id="verifier:characterization:dsp-limit",
        ),
        _wrap_check(
            S_wife_ver.id,
            "dramatica-complete", "DSP_wife_limit",
            wife_dsp_limit_check,
            reviewer_id="verifier:characterization:dsp-limit",
        ),
        _wrap_check(
            S_samurai_ver.id,
            "dramatica-complete", "DSP_samurai_limit",
            samurai_dsp_limit_check,
            reviewer_id="verifier:characterization:dsp-limit",
        ),
        _wrap_check(
            S_woodcutter_ver.id,
            "dramatica-complete", "DSP_woodcutter_limit",
            woodcutter_dsp_limit_check,
            reviewer_id="verifier:characterization:dsp-limit",
        ),
    )


if __name__ == "__main__":
    reviews = run()
    print(f"=== Rashomon dramatica-complete → substrate verifier ===")
    print(f"    (first multi-Story verifier; per-Story MS4 scoping)")
    approved = sum(1 for r in reviews if r.verdict == VERDICT_APPROVED)
    needs_work = sum(1 for r in reviews if r.verdict == VERDICT_NEEDS_WORK)
    partial = sum(1 for r in reviews if r.verdict == VERDICT_PARTIAL_MATCH)
    noted = sum(1 for r in reviews if r.verdict == VERDICT_NOTED)
    print(f"{len(reviews)} checks run; "
          f"{approved} APPROVED, {needs_work} NEEDS_WORK, "
          f"{partial} PARTIAL_MATCH, {noted} NOTED.\n")
    for r in reviews:
        target = f"{r.target_record.dialect}:{r.target_record.record_id}"
        strength = (
            f" strength={r.match_strength:.2f}"
            if r.match_strength is not None else ""
        )
        print(f"[{r.verdict}]{strength} {target}")
        print(f"  via {r.reviewer_id}")
        print(f"  {r.comment}\n")
