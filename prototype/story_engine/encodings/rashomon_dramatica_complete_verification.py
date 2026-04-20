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
contested branch — and, under LT12 (pressure-shape-taxonomy-
sketch-03), how are the bandit/samurai `bound_to` retractions
classified?

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
  happens to carry a substrate retraction in its middle arc.**
  The bandit and samurai testimonies retract `bound_to(husband,
  tree)` in the middle arc (`E_t_frees_husband`, `E_h_frees_
  husband`). Under sketch-02 these fired LT2 and produced
  NEEDS_WORK 0.67 verdicts — the first non-APPROVED verdict
  surfaced by the Rashomon probe. Under sketch-03 LT12a classifies
  both as *enabling* retractions (the `bound_to` predicate matches
  the constraint vocabulary); they no longer count toward LT2
  convergence, and the verdicts become NOTED 0.5. The shift
  closes the probe's first qualification.

- **Bandit + samurai shift NOTED → APPROVED under scheduling-act-
  utterance-sketch-01 (SC2 + SC4).** Both testimonies' `E_*_wife_
  requests_killing` utterance events now carry a `requested_killing
  (tajomaru, husband)` world effect (SC4). LT8 recognizes the
  `requested_` prefix per the extended `SCHEDULING_PREFIXES` set
  (SC2); combined with zero middle-arc LT2 signals (LT12 excludes
  the `bound_to` retraction as enabling), LT9 fires → timelock-
  strong, APPROVED strength `min(1.0, 1/2.0) = 0.5`. Substrate
  polarity shifts from consistent-with to substrate-confirms;
  numerical strength 0.5 is unchanged.

- **Wife + woodcutter stay NOTED 0.5.** The wife testimony's
  τ_s=7 event is an action (`E_w_tajomaru_leaves`, OQ2 in
  sketch-01's deferred list); the woodcutter testimony's event
  is a dual-party goading (`E_wc_wife_goads`, OQ1). Neither falls
  under `requested_*`'s one-way-request shape; both stay on LT3's
  honest weak-fallback verdict. The resulting across-sibling
  asymmetry is substantive — two testimonies surface explicit
  speech-act scheduling force; two do not.

Honest scope limit: this verifier does NOT test the frame Story's
declarations (DSP_limit=Optionlock, Outcome=Success, Judgment=Good)
against substrate — there is no substrate to test against. The
multi-Story extension's first real test is the testimony-side LT9
runs.
"""

from __future__ import annotations

from story_engine.core.substrate import CANONICAL
from story_engine.encodings.rashomon import (
    EVENTS_ALL, ALL_BRANCHES,
    B_TAJOMARU, B_WIFE, B_HUSBAND, B_WOODCUTTER,
)

from story_engine.core.dramatica_template import DSPAxis, Limit
from story_engine.encodings.rashomon_dramatic import (
    S_frame, S_bandit_ver, S_wife_ver, S_samurai_ver, S_woodcutter_ver,
)
from story_engine.encodings.rashomon_dramatica_complete import (
    DYNAMIC_STORY_POINTS_BY_STORY,
)
from story_engine.encodings.rashomon_lowerings import LOWERINGS_BY_STORY

from story_engine.core.lowering import CrossDialectRef, cross_ref
from story_engine.core.verification import (
    DirectCheckRegistration, run_direct_review_checks,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK, VERDICT_PARTIAL_MATCH,
    VERDICT_NOTED,
)
from story_engine.core.verifier_helpers import dsp_limit_characterization_check


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
    not.

    Per scheduling-act-utterance-sketch-02 SC9, the Story's
    scope-relevant Lowerings (`LOWERINGS_BY_STORY[story_id]`) are
    threaded through to surface the prose-carried driver signal on
    testimonies whose verdict would otherwise be NOTED with no
    specialization. Only S_wife_ver exercises the signal in the
    current corpus (L_wife_violated's annotation names the
    husband's gaze of contempt as prose-carried)."""
    dsp_limit = next(
        d for d in DYNAMIC_STORY_POINTS_BY_STORY[story_id]
        if d.axis == DSPAxis.LIMIT
    )
    declared = dsp_limit.choice
    return dsp_limit_characterization_check(
        EVENTS_ALL, _NO_RULES, canonical_scope_branch, ALL_BRANCHES,
        declared,
        lowerings=LOWERINGS_BY_STORY[story_id],
    )


def bandit_dsp_limit_check(upper_ref, _unused_lower_refs=()):
    """S_bandit_ver: DSP_limit=Timelock declared. LT9 runs against
    B_TAJOMARU scope (canonical grove events + Tajōmaru's branch
    events: wife-requests-killing, frees-husband, duel). The
    `frees-husband` event retracts `bound_to(husband, tree)`; under
    LT12a (sketch-03) `bound_to` is in the constraint-predicate
    vocabulary → the retraction is enabling (unbinding enables the
    duel, not foreclosing an option). Restricting retraction count:
    0. With no scheduling predicate either, classification is
    timelock-consistent → NOTED 0.5."""
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
    B_HUSBAND scope. 5 positive-τ_s events (τ_s=7..11). Under
    LT12a (sketch-03) `E_h_frees_husband`'s retraction of
    `bound_to(husband, tree)` is enabling (the husband is unbound
    so he can commit suicide; not an option-closing move).
    Restricting retraction count: 0. Classification:
    timelock-consistent → NOTED 0.5. Parallels S_bandit_ver's
    verdict under sketch-03; both were NEEDS_WORK 0.67 under
    sketch-02."""
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


CHECK_REGISTRY = (
    DirectCheckRegistration(
        "dramatica-complete", "DSP_frame_limit",
        frame_declarations_not_substrate_bound_check,
        f"verifier:multi-story:frame-declarations:story={S_frame.id}",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_bandit_limit",
        bandit_dsp_limit_check,
        f"verifier:characterization:dsp-limit:story={S_bandit_ver.id}",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_wife_limit",
        wife_dsp_limit_check,
        f"verifier:characterization:dsp-limit:story={S_wife_ver.id}",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_samurai_limit",
        samurai_dsp_limit_check,
        f"verifier:characterization:dsp-limit:story={S_samurai_ver.id}",
    ),
    DirectCheckRegistration(
        "dramatica-complete", "DSP_woodcutter_limit",
        woodcutter_dsp_limit_check,
        f"verifier:characterization:dsp-limit:story={S_woodcutter_ver.id}",
    ),
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
    return run_direct_review_checks(CHECK_REGISTRY)


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
