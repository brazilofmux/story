"""
verification.py — first verifier primitive (Characterization) per
verification-sketch-01 (V1-V8).

Dialect-agnostic. Imports from `lowering` (for CrossDialectRef and
LoweringStatus) but does not import from any specific dialect module
(substrate.py, dramatic.py). Encoding-specific verifier code lives
in modules like `oedipus_verification.py` that import from both
dialects plus this module.

Scope of this first pass:

- Verifier output records: VerificationReview, StructuralAdvisory,
  VerificationAnswerProposal. All three flow through the existing
  proposal queue (per V2). The walker integration is deferred — for
  now they are records consumers can collect and print.
- One primitive: **Characterization** (V3). Given an upper record
  id + dialect, the upper record's ACTIVE Lowerings, and a
  caller-supplied check function, run the check and return a
  VerificationReview. The check function receives the upper-record
  reference and the union of all lower records across the upper's
  Lowerings; it returns (verdict, match_strength, comment).
- Convenience: a `run_characterization_checks` orchestrator that
  takes a list of (upper_ref, check_fn) pairs and runs them all,
  returning a list of VerificationReviews.

Deferred to follow-on passes:

- Claim-moment and Claim-trajectory primitives (V3 says three
  primitives total; this sketch ships one).
- Inference-01 composition (V6) — characterization checks may
  consult substrate state derived via the rule engine; the check
  function does this through the substrate-side context it receives,
  not via this module.
- Walker integration (extending proposal_walker.py to handle the
  three new entry kinds). For now, the verifier just returns lists.
- VerificationAnswerProposal acceptance flow (parallel to
  AnswerProposal acceptance in the substrate's reader-model surface).
- Per-record-type / per-field iteration (per V5). Right now the
  caller picks which records to verify; a future orchestrator can
  enumerate based on dramatic.COUPLING_DECLARATIONS.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Callable

from lowering import (
    CrossDialectRef, cross_ref,
    Lowering, LoweringStatus,
)


# ============================================================================
# Verdict and severity vocabularies
# ============================================================================
#
# Same vocabulary as descriptions-01's ReviewVerdict, kept as strings
# for cross-module independence.

VERDICT_APPROVED = "approved"
VERDICT_NEEDS_WORK = "needs-work"
VERDICT_PARTIAL_MATCH = "partial-match"
VERDICT_NOTED = "noted"

VALID_VERDICTS = frozenset({
    VERDICT_APPROVED, VERDICT_NEEDS_WORK,
    VERDICT_PARTIAL_MATCH, VERDICT_NOTED,
})

SEVERITY_NOTED = "noted"
SEVERITY_SUGGEST_REVIEW = "suggest-review"
SEVERITY_SUGGEST_REVISE = "suggest-revise"

VALID_SEVERITIES = frozenset({
    SEVERITY_NOTED, SEVERITY_SUGGEST_REVIEW, SEVERITY_SUGGEST_REVISE,
})


# ============================================================================
# Output records (V2)
# ============================================================================


@dataclass(frozen=True)
class VerificationReview:
    """A review attached to a specific record (upper, Lowering, or
    Template). Same shape as descriptions-01's ReviewEntry plus a
    target_record reference and an optional match_strength.

    `match_strength` is in [0, 1] and is meaningful for partial-match
    verdicts (a Characterization that holds 70% of the time). Other
    verdicts may set it for transparency or leave it None."""
    reviewer_id: str
    reviewed_at_τ_a: int
    verdict: str
    anchor_τ_a: int
    target_record: CrossDialectRef
    comment: Optional[str] = None
    match_strength: Optional[float] = None


@dataclass(frozen=True)
class StructuralAdvisory:
    """An observation that spans multiple records or names a pattern
    rather than attaching to a specific record. Used when the
    verifier finding is not naturally a review."""
    advisor_id: str
    advised_at_τ_a: int
    severity: str
    comment: str
    scope: tuple   # tuple[CrossDialectRef]
    match_strength: Optional[float] = None


@dataclass(frozen=True)
class VerificationAnswerProposal:
    """A verifier-sourced proposal answering an upper-dialect open
    question (a Description with is_question=True, in
    descriptions-01 terms). Parallels AnswerProposal from
    reader-model-01 but the proposer is a verifier, not a
    reader-model partner."""
    proposer_id: str
    question_id: CrossDialectRef
    proposed_text: str
    rationale: str
    proposed_at_τ_a: int
    status: str = "pending"


# ============================================================================
# Characterization primitive (V3, V4, V7)
# ============================================================================


# A check function takes the upper record's CrossDialectRef and the
# union of lower records across all the upper's ACTIVE Lowerings
# (tuple[CrossDialectRef]); it returns
# (verdict, match_strength, comment).
CharacterizationCheck = Callable[
    [CrossDialectRef, tuple],
    tuple,  # (verdict_str, Optional[float], comment_str)
]


def verify_characterization(
    upper_record_id: str,
    upper_dialect: str,
    lowerings: tuple,
    check: CharacterizationCheck,
    *,
    reviewer_id: str = "verifier:characterization",
    reviewed_at_τ_a: int = 0,
) -> Optional[VerificationReview]:
    """Run a Characterization check on an upper record's ACTIVE
    Lowerings. Returns a VerificationReview, or None if the upper
    record has no ACTIVE Lowerings (no substrate realization to
    check against).

    The check function is caller-supplied and contains the
    encoding-specific logic: given the upper reference and the
    union of lower records across the upper's ACTIVE Lowerings, it
    returns (verdict, match_strength, comment). Per V7,
    partial-match verdicts are first-class — the check returns
    `match_strength` in [0, 1] alongside the verdict.

    Per V4, the check function speaks the upper dialect's vocabulary
    and consults the lower dialect's queries through whatever
    substrate context it captures in its closure; this module is
    dialect-agnostic.
    """
    upper_ref = cross_ref(upper_dialect, upper_record_id)
    upper_lowerings = [
        lw for lw in lowerings
        if lw.upper_record == upper_ref
        and lw.status == LoweringStatus.ACTIVE
    ]
    if not upper_lowerings:
        return None

    all_lower = tuple(
        lr for lw in upper_lowerings for lr in lw.lower_records
    )
    verdict, strength, comment = check(upper_ref, all_lower)

    if verdict not in VALID_VERDICTS:
        # Defensive: the encoding's check function returned an
        # unrecognized verdict. Surface as 'noted' with a comment
        # so the verifier doesn't drop the result silently.
        comment = (
            f"check returned non-standard verdict {verdict!r}; "
            f"recording as 'noted'. Original comment: {comment}"
        )
        verdict = VERDICT_NOTED

    anchor_τ_a = max(
        (lw.anchor_τ_a for lw in upper_lowerings if lw.anchor_τ_a is not None),
        default=0,
    )

    return VerificationReview(
        reviewer_id=reviewer_id,
        reviewed_at_τ_a=reviewed_at_τ_a,
        verdict=verdict,
        anchor_τ_a=anchor_τ_a,
        target_record=upper_ref,
        comment=comment,
        match_strength=strength,
    )


def run_characterization_checks(
    checks: tuple,
    lowerings: tuple,
    *,
    reviewer_id: str = "verifier:characterization",
    reviewed_at_τ_a: int = 0,
) -> tuple:
    """Run a list of (upper_record_id, upper_dialect, check_fn)
    triples through verify_characterization. Returns a tuple of
    (VerificationReview | StructuralAdvisory) — VerificationReview
    when the check ran (the upper record had ACTIVE Lowerings);
    StructuralAdvisory("noted", "no_active_lowerings", ...) when
    the check was skipped because the upper had no ACTIVE Lowerings.
    """
    out = []
    for (upper_id, upper_dialect, check) in checks:
        review = verify_characterization(
            upper_id, upper_dialect, lowerings, check,
            reviewer_id=reviewer_id,
            reviewed_at_τ_a=reviewed_at_τ_a,
        )
        if review is None:
            out.append(StructuralAdvisory(
                advisor_id=reviewer_id,
                advised_at_τ_a=reviewed_at_τ_a,
                severity=SEVERITY_NOTED,
                comment=(f"upper record {upper_dialect}:{upper_id} has no "
                         f"ACTIVE Lowerings; characterization check "
                         f"skipped"),
                scope=(cross_ref(upper_dialect, upper_id),),
            ))
        else:
            out.append(review)
    return tuple(out)


# ============================================================================
# Convenience grouping
# ============================================================================


# ============================================================================
# Claim-trajectory primitive (V3, V6)
# ============================================================================


# A trajectory check function takes the upper record's CrossDialectRef,
# the union of lower records across the upper's ACTIVE Lowerings (which
# may be empty — see below), and a tuple of PositionRanges authored on
# those Lowerings (also possibly empty). It returns
# (verdict_str, Optional[match_strength], comment_str).
#
# The check captures substrate context in its closure: events, rules,
# fold-projection callables. This module stays dialect-agnostic.
#
# Per V6, trajectory checks naturally compose with inference-01's
# derivation surface — the substrate state the check inspects may
# include facts derived via the rule engine (parricide, regicide, etc.).
ClaimTrajectoryCheck = Callable[
    [CrossDialectRef, tuple, tuple],
    tuple,  # (verdict_str, Optional[float], comment_str)
]


def verify_claim_trajectory(
    upper_record_id: str,
    upper_dialect: str,
    lowerings: tuple,
    check: ClaimTrajectoryCheck,
    *,
    reviewer_id: str = "verifier:claim-trajectory",
    reviewed_at_τ_a: int = 0,
) -> VerificationReview:
    """Run a Claim-trajectory check on an upper record.

    Unlike Characterization, this primitive does NOT short-circuit
    when the upper has no ACTIVE Lowerings. The Argument's claim
    (e.g., resolution_direction=AFFIRM) is about the substrate
    trajectory, which exists regardless of whether any Lowering
    binds the Argument to specific lower records — Lowering is for
    Realization, and Argument doesn't realize (lowering-sketch-01
    F6). The check function supplies its own trajectory scope from
    its closure.

    When ACTIVE Lowerings DO exist, this primitive collects their
    lower_records and position_ranges and passes them to the check
    as additional context. The check decides whether to use them.

    Per V6, the check function may consult substrate state that
    includes derived facts via the inference engine; the substrate
    context it captures should expose `world_holds_derived` /
    `holds_derived` if it wants to.
    """
    upper_ref = cross_ref(upper_dialect, upper_record_id)
    upper_lowerings = [
        lw for lw in lowerings
        if lw.upper_record == upper_ref
        and lw.status == LoweringStatus.ACTIVE
    ]

    all_lower = tuple(
        lr for lw in upper_lowerings for lr in lw.lower_records
    )
    position_ranges = tuple(
        lw.position_range for lw in upper_lowerings
        if lw.position_range is not None
    )

    verdict, strength, comment = check(upper_ref, all_lower, position_ranges)

    if verdict not in VALID_VERDICTS:
        comment = (
            f"check returned non-standard verdict {verdict!r}; "
            f"recording as 'noted'. Original comment: {comment}"
        )
        verdict = VERDICT_NOTED

    anchor_τ_a = max(
        (lw.anchor_τ_a for lw in upper_lowerings if lw.anchor_τ_a is not None),
        default=0,
    )

    return VerificationReview(
        reviewer_id=reviewer_id,
        reviewed_at_τ_a=reviewed_at_τ_a,
        verdict=verdict,
        anchor_τ_a=anchor_τ_a,
        target_record=upper_ref,
        comment=comment,
        match_strength=strength,
    )


def run_claim_trajectory_checks(
    checks: tuple,
    lowerings: tuple,
    *,
    reviewer_id: str = "verifier:claim-trajectory",
    reviewed_at_τ_a: int = 0,
) -> tuple:
    """Run a list of (upper_record_id, upper_dialect, check_fn)
    triples through verify_claim_trajectory. Returns a tuple of
    VerificationReviews — every check produces a review, including
    when no Lowerings exist for the upper record (the trajectory
    check runs against the substrate scope the check function
    captures)."""
    out = []
    for (upper_id, upper_dialect, check) in checks:
        review = verify_claim_trajectory(
            upper_id, upper_dialect, lowerings, check,
            reviewer_id=reviewer_id,
            reviewed_at_τ_a=reviewed_at_τ_a,
        )
        out.append(review)
    return tuple(out)


# ============================================================================
# Claim-moment primitive (V3, V6)
# ============================================================================


# A moment check function takes the upper record's CrossDialectRef,
# the union of lower records across the upper's ACTIVE Lowerings,
# and a tuple of PositionRanges authored on those Lowerings. It
# returns (verdict_str, Optional[match_strength], comment_str).
#
# Operationally identical to ClaimTrajectoryCheck in signature; the
# semantic difference is what the check does — Claim-moment checks
# query substrate state at a specific moment (typically derived
# from the lower records' τ_s or the position_range), while
# Claim-trajectory checks iterate substrate state across a range.
#
# The framework keeps the two as separate primitives (per V3) so
# verifier-id provenance and check-shape expectations stay
# distinct, even though the orchestration code is structurally
# parallel.
ClaimMomentCheck = Callable[
    [CrossDialectRef, tuple, tuple],
    tuple,  # (verdict_str, Optional[float], comment_str)
]


def verify_claim_moment(
    upper_record_id: str,
    upper_dialect: str,
    lowerings: tuple,
    check: ClaimMomentCheck,
    *,
    reviewer_id: str = "verifier:claim-moment",
    reviewed_at_τ_a: int = 0,
) -> Optional[VerificationReview]:
    """Run a Claim-moment check on an upper record.

    Returns None when the upper has no ACTIVE Lowerings — the
    moment-pattern claim depends on knowing *which* lower records
    locate the moment. Without Lowerings the check has no anchor.
    This differs from `verify_claim_trajectory` (which always runs
    because trajectory claims have substrate-wide scope) and
    matches `verify_characterization` (which also short-circuits
    on no-Lowerings since pattern-classification needs records to
    classify).

    The check function receives the upper ref, the union of lower
    records across ACTIVE Lowerings, and the tuple of
    PositionRanges authored on those Lowerings. Most moment checks
    derive a τ_s from the lower records (e.g., the max τ_s of the
    lowered substrate events) and query substrate state at that
    moment.

    Per V6, moment checks may consume substrate state derived via
    the inference engine (`world_holds_derived`,
    `holds_derived`); this module is dialect-agnostic and the
    check captures whatever substrate context it needs in its
    closure.
    """
    upper_ref = cross_ref(upper_dialect, upper_record_id)
    upper_lowerings = [
        lw for lw in lowerings
        if lw.upper_record == upper_ref
        and lw.status == LoweringStatus.ACTIVE
    ]
    if not upper_lowerings:
        return None

    all_lower = tuple(
        lr for lw in upper_lowerings for lr in lw.lower_records
    )
    position_ranges = tuple(
        lw.position_range for lw in upper_lowerings
        if lw.position_range is not None
    )

    verdict, strength, comment = check(upper_ref, all_lower, position_ranges)

    if verdict not in VALID_VERDICTS:
        comment = (
            f"check returned non-standard verdict {verdict!r}; "
            f"recording as 'noted'. Original comment: {comment}"
        )
        verdict = VERDICT_NOTED

    anchor_τ_a = max(
        (lw.anchor_τ_a for lw in upper_lowerings if lw.anchor_τ_a is not None),
        default=0,
    )

    return VerificationReview(
        reviewer_id=reviewer_id,
        reviewed_at_τ_a=reviewed_at_τ_a,
        verdict=verdict,
        anchor_τ_a=anchor_τ_a,
        target_record=upper_ref,
        comment=comment,
        match_strength=strength,
    )


def run_claim_moment_checks(
    checks: tuple,
    lowerings: tuple,
    *,
    reviewer_id: str = "verifier:claim-moment",
    reviewed_at_τ_a: int = 0,
) -> tuple:
    """Run a list of (upper_record_id, upper_dialect, check_fn)
    triples through verify_claim_moment. Returns a tuple of
    (VerificationReview | StructuralAdvisory) — Reviews when the
    check ran (the upper had ACTIVE Lowerings); Advisories with
    code='no_active_lowerings' when the check was skipped.

    Same orchestration shape as run_characterization_checks; the
    two share the no-Lowerings-skipped semantics.
    """
    out = []
    for (upper_id, upper_dialect, check) in checks:
        review = verify_claim_moment(
            upper_id, upper_dialect, lowerings, check,
            reviewer_id=reviewer_id,
            reviewed_at_τ_a=reviewed_at_τ_a,
        )
        if review is None:
            out.append(StructuralAdvisory(
                advisor_id=reviewer_id,
                advised_at_τ_a=reviewed_at_τ_a,
                severity=SEVERITY_NOTED,
                comment=(f"upper record {upper_dialect}:{upper_id} has no "
                         f"ACTIVE Lowerings; claim-moment check skipped"),
                scope=(cross_ref(upper_dialect, upper_id),),
            ))
        else:
            out.append(review)
    return tuple(out)


# ============================================================================
# Convenience grouping
# ============================================================================


def reviews_only(results: tuple) -> tuple:
    """Filter a verifier result tuple to just VerificationReviews."""
    return tuple(r for r in results if isinstance(r, VerificationReview))


def advisories_only(results: tuple) -> tuple:
    """Filter to just StructuralAdvisories."""
    return tuple(r for r in results if isinstance(r, StructuralAdvisory))


def group_by_verdict(reviews: tuple) -> dict:
    """Bucket VerificationReviews by verdict for scan-friendly output."""
    out = {v: [] for v in VALID_VERDICTS}
    for r in reviews:
        out.setdefault(r.verdict, []).append(r)
    return out
