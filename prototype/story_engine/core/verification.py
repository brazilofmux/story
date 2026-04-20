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

from story_engine.core.lowering import (
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


# Assessments a VerifierCommentary can carry. Distinct vocabulary
# from VERDICT_* because the question is different — a verdict
# judges a record; an assessment judges a verdict.

ASSESSMENT_ENDORSES = "endorses"
ASSESSMENT_QUALIFIES = "qualifies"
ASSESSMENT_DISSENTS = "dissents"
ASSESSMENT_NOTED = "noted"

VALID_ASSESSMENTS = frozenset({
    ASSESSMENT_ENDORSES, ASSESSMENT_QUALIFIES,
    ASSESSMENT_DISSENTS, ASSESSMENT_NOTED,
})


# Coupling-kind vocabulary, mirroring dramatic.COUPLING_*. Verification
# is dialect-agnostic so it can't import dramatic.py; the same strings
# are duplicated here. An encoding's verifier module can import either
# set — they resolve to the same string values.

COUPLING_REALIZATION = "realization"
COUPLING_CHARACTERIZATION = "characterization"
COUPLING_CLAIM_MOMENT = "claim-moment"
COUPLING_CLAIM_TRAJECTORY = "claim-trajectory"
COUPLING_FLAVOR = "flavor"

ORCHESTRATABLE_COUPLING_KINDS = frozenset({
    COUPLING_CHARACTERIZATION,
    COUPLING_CLAIM_MOMENT,
    COUPLING_CLAIM_TRAJECTORY,
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


@dataclass(frozen=True)
class VerifierCommentary:
    """A reviewer's read on a VerificationReview — does the verifier's
    verdict feel right? Is the check well-grounded? Is there a
    signature the check missed?

    Distinct from VerificationReview itself: VerificationReview is
    the verifier's verdict on a record; VerifierCommentary is a
    third-party (human reviewer or LLM probe) reading of the
    verifier's verdict. Routes through the proposal queue the same
    way — the author walks and decides whether to act on it (e.g.,
    extend the check function, accept the dissent and re-run, file
    away as noted).

    `assessment` ∈ {endorses, qualifies, dissents, noted}:
      - endorses — verdict is well-grounded; nothing to add.
      - qualifies — verdict stands but with a clarification, missed
        nuance, or alternate reading worth capturing alongside.
      - dissents — commenter disagrees with the verdict, has a
        specific counter-argument grounded in the records.
      - noted — read but no position taken.

    `suggested_signature` is an optional concrete signature the
    commenter thinks the check might add (e.g., "consider also
    checking that owner Entity appears as `told_by` listener, not
    just literal participant"). Free-form prose, intended as
    inspiration for the author who maintains the check function;
    not actionable code.
    """
    commenter_id: str
    commented_at_τ_a: int
    assessment: str       # one of ASSESSMENT_*
    target_review: VerificationReview
    comment: str
    suggested_signature: Optional[str] = None


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
# Direct upper-record review orchestrator
# ============================================================================
#
# Some verifier layers already know their exact upper-record target and
# do not route through Lowerings at all. The dramatica-complete
# verifiers are the current example: each check function takes one
# authored upper-record ref (e.g. `dramatica-complete:DSP_limit`) and
# returns a verdict tuple directly. The helper below centralizes the
# "wrap this direct check in a VerificationReview" pattern so authored
# encodings stop hand-rolling identical `_wrap_check()` helpers.


@dataclass(frozen=True)
class DirectCheckRegistration:
    """One direct upper-record check to wrap as a VerificationReview.

    `upper_dialect` + `upper_record_id` identify the authored record
    the check is judging. `check_fn` takes that CrossDialectRef and
    returns the standard `(verdict, match_strength, comment)` tuple.
    `reviewer_id` is passed through verbatim so callers can use either
    a stable verifier id or a story-scoped suffix (as Rashomon does).
    """
    upper_dialect: str
    upper_record_id: str
    check_fn: Callable
    reviewer_id: str


def run_direct_review_checks(
    registrations: tuple,
    *,
    reviewed_at_τ_a: int = 0,
    anchor_τ_a: int = 0,
) -> tuple:
    """Run a tuple of DirectCheckRegistrations and return
    VerificationReviews in registration order.

    This is the direct-check analogue to the lowering-aware
    orchestrators above: no record enumeration, no coupling-kind
    dispatch, no advisory path. Each registration names exactly one
    upper record and one check function; this helper only provides the
    common review-wrapping logic.
    """
    out: list = []
    for registration in registrations:
        upper_ref = cross_ref(
            registration.upper_dialect,
            registration.upper_record_id,
        )
        verdict, strength, comment = registration.check_fn(upper_ref)
        out.append(VerificationReview(
            reviewer_id=registration.reviewer_id,
            reviewed_at_τ_a=reviewed_at_τ_a,
            verdict=verdict,
            anchor_τ_a=anchor_τ_a,
            target_record=upper_ref,
            comment=comment,
            match_strength=strength,
        ))
    return tuple(out)


# ============================================================================
# Per-record-type orchestrator (V5 — auto-enumerate from declarations)
# ============================================================================
#
# The hand-wired pattern that oedipus_verification.py and
# macbeth_verification.py both use today is:
#
#   CHARACTERIZATION_CHECKS = (("T_mc_X", "dramatic", check_fn), ...)
#   CLAIM_TRAJECTORY_CHECKS = ...
#   CLAIM_MOMENT_CHECKS = ...
#   def run(): out = []; out.extend(run_X_checks(...)); ...
#
# Each (record_id, dialect, check_fn) triple has to be paired with the
# right primitive runner manually — the author keeps three parallel
# tuples and three parallel run_* calls in lockstep. As encodings grow
# and as more checks land on each record type, the bookkeeping
# multiplies and silent gaps become easy.
#
# The orchestrator below replaces all three of those tuples with a
# single CHECK_REGISTRY of CheckRegistrations, plus a `records_by_type`
# dict the encoding builds from its Story aggregate. Dispatch by
# coupling kind happens here; the encoding only declares which check
# fires on which records.


@dataclass(frozen=True)
class CheckRegistration:
    """Binds a check function to records the orchestrator should run
    it against.

    The orchestrator iterates records of `record_type` from the
    encoding's enumeration. For each record where `applies_to(record)`
    returns True, the check function fires through the appropriate
    verification primitive (Characterization / Claim-moment /
    Claim-trajectory) selected by `coupling_kind`.

    `field` is informational — it names the record field this check
    is grounded in (e.g., "role_label" on a Throughline, "result" on
    a Scene). It does not affect dispatch in this iteration; the
    primitive runners take a record reference and let the check
    function decide what to read. A future iteration could use
    `field` to cross-reference dramatic.COUPLING_DECLARATIONS for
    coverage reports.

    `coupling_kind` must be one of:
      - COUPLING_CHARACTERIZATION
      - COUPLING_CLAIM_MOMENT
      - COUPLING_CLAIM_TRAJECTORY
    Realization and Flavor are not orchestratable here (Realization
    has no primitive yet; Flavor has no verifier by design).

    `applies_to` is a predicate `(record) -> bool`. The orchestrator
    silent-skips records where it returns False — this is how the
    encoding restricts a check to specific records (e.g.,
    `lambda t: t.role_label == "main-character"`). A registration
    with a vacuous `applies_to=lambda r: True` fires on every record
    of its `record_type`; a check function that should run on
    multiple records but conditionalize on something specific can use
    a more restrictive `applies_to`.

    `description` is a human-readable label, surfaced in coverage
    reports and walker output.
    """
    coupling_kind: str
    record_type: str
    field: Optional[str]
    applies_to: Callable
    check_fn: Callable
    description: str = ""

    def __post_init__(self):
        if self.coupling_kind not in ORCHESTRATABLE_COUPLING_KINDS:
            raise ValueError(
                f"CheckRegistration coupling_kind {self.coupling_kind!r} "
                f"is not orchestratable; expected one of "
                f"{sorted(ORCHESTRATABLE_COUPLING_KINDS)}"
            )


def orchestrate_checks(
    *,
    records_by_type: dict,
    registry: tuple,
    lowerings: tuple,
    record_dialect: str,
    reviewed_at_τ_a: int = 0,
    reviewer_id_prefix: str = "verifier",
) -> tuple:
    """Dispatch registered checks against an encoding's records.
    Returns a tuple of (VerificationReview | StructuralAdvisory).

    For each CheckRegistration in `registry`:
      - Iterate `records_by_type[registration.record_type]`.
      - For each record where `applies_to(record)` is True, fire the
        check through the primitive matching `coupling_kind`.

    The result mix matches what the existing per-primitive runners
    produce: VerificationReviews when the check ran and a verdict
    landed; StructuralAdvisories when a Characterization or
    Claim-moment was skipped because the upper had no ACTIVE
    Lowerings (Claim-trajectory always runs, so it never produces
    a skip-advisory).

    `reviewer_id_prefix` is composed with the coupling kind to form
    the per-result reviewer_id, e.g.,
    'verifier:dramatic-substrate-characterization'. Encoding modules
    that want to override per-primitive can pass their own prefix or
    re-stamp results after the fact; the prefix here is the common
    case.
    """
    out: list = []
    for registration in registry:
        records = records_by_type.get(registration.record_type, ())
        for record in records:
            if not registration.applies_to(record):
                continue
            record_id = record.id
            kind = registration.coupling_kind

            if kind == COUPLING_CHARACTERIZATION:
                reviewer_id = (
                    f"{reviewer_id_prefix}:{record_dialect}-substrate-"
                    f"characterization"
                )
                review = verify_characterization(
                    record_id, record_dialect, lowerings,
                    registration.check_fn,
                    reviewer_id=reviewer_id,
                    reviewed_at_τ_a=reviewed_at_τ_a,
                )
                if review is None:
                    out.append(StructuralAdvisory(
                        advisor_id=reviewer_id,
                        advised_at_τ_a=reviewed_at_τ_a,
                        severity=SEVERITY_NOTED,
                        comment=(
                            f"upper record {record_dialect}:{record_id} "
                            f"has no ACTIVE Lowerings; characterization "
                            f"check {registration.description!r} skipped"
                        ),
                        scope=(cross_ref(record_dialect, record_id),),
                    ))
                else:
                    out.append(review)

            elif kind == COUPLING_CLAIM_TRAJECTORY:
                reviewer_id = (
                    f"{reviewer_id_prefix}:{record_dialect}-substrate-"
                    f"claim-trajectory"
                )
                review = verify_claim_trajectory(
                    record_id, record_dialect, lowerings,
                    registration.check_fn,
                    reviewer_id=reviewer_id,
                    reviewed_at_τ_a=reviewed_at_τ_a,
                )
                # Claim-trajectory always returns a review.
                out.append(review)

            elif kind == COUPLING_CLAIM_MOMENT:
                reviewer_id = (
                    f"{reviewer_id_prefix}:{record_dialect}-substrate-"
                    f"claim-moment"
                )
                review = verify_claim_moment(
                    record_id, record_dialect, lowerings,
                    registration.check_fn,
                    reviewer_id=reviewer_id,
                    reviewed_at_τ_a=reviewed_at_τ_a,
                )
                if review is None:
                    out.append(StructuralAdvisory(
                        advisor_id=reviewer_id,
                        advised_at_τ_a=reviewed_at_τ_a,
                        severity=SEVERITY_NOTED,
                        comment=(
                            f"upper record {record_dialect}:{record_id} "
                            f"has no ACTIVE Lowerings; claim-moment "
                            f"check {registration.description!r} skipped"
                        ),
                        scope=(cross_ref(record_dialect, record_id),),
                    ))
                else:
                    out.append(review)
            # CheckRegistration.__post_init__ rejects any other kind, so
            # no fall-through case is reachable here.

    return tuple(out)


# ============================================================================
# Coverage report — registry vs. coupling declarations
# ============================================================================
#
# orchestrate_checks dispatches the registry. coverage_report is the
# inverse audit: given the dialect's COUPLING_DECLARATIONS and the
# encoding's records, surface every (record, declaration) pair where
# *no* registered check would fire. This is the homework-forcer the
# Expert System framing wants — the gaps are visible, not silent.
#
# Coverage matches by (record_type, coupling_kind, applies_to). The
# `field` on a CheckRegistration is informational only; a registration
# on (Argument, claim-trajectory, premise) covers both the premise
# declaration AND the resolution_direction declaration on Argument
# because both share record_type + kind. The author who wants per-
# field tracking should write per-field check functions; the gap report
# would then reflect that granularity.


@dataclass(frozen=True)
class CoverageGap:
    """A field declared in coupling_declarations that no registered
    check fires on for a specific record. The expert-system meta-
    finding: 'this is where you have homework left to do.'

    Realization and Flavor declarations are skipped entirely —
    Realization has no orchestrator-dispatched primitive yet, and
    Flavor has no verifier by design — so neither generates gaps.
    """
    record_type: str
    record_id: str
    record_dialect: str
    field: Optional[str]
    coupling_kind: str
    message: str  # human-readable, suitable for advisory-style output


def _registration_covers(
    registration: "CheckRegistration",
    record_type: str,
    coupling_kind: str,
    record,
) -> bool:
    """Does this registration fire on (record_type, coupling_kind,
    record)? The matching is structural: same record_type, same
    coupling_kind, applies_to(record) is True."""
    if registration.record_type != record_type:
        return False
    if registration.coupling_kind != coupling_kind:
        return False
    try:
        return bool(registration.applies_to(record))
    except Exception:
        # A predicate that errors on a record can't be relied on to
        # cover it; treat as not-covering. The author's predicate
        # bug surfaces here rather than being swallowed silently.
        return False


def coverage_report(
    *,
    records_by_type: dict,
    registry: tuple,
    coupling_declarations: tuple,
    record_dialect: str = "dramatic",
) -> tuple:
    """Compare the orchestrator's registry against the dialect's
    coupling_declarations. Returns a tuple of CoverageGap records:
    one per (record, declaration) pair the registry doesn't cover.

    Each input declaration must have at least the attributes
    `record_type`, `field`, and `kind` — matching the
    `CouplingDeclaration` shape from dramatic.py (the verification
    module stays dialect-agnostic by reading those attributes
    directly rather than importing the dialect's class).

    Only orchestratable kinds (Characterization, Claim-moment,
    Claim-trajectory) generate gaps; Realization and Flavor
    declarations are silently skipped.
    """
    gaps: list = []
    for declaration in coupling_declarations:
        if declaration.kind not in ORCHESTRATABLE_COUPLING_KINDS:
            continue
        records = records_by_type.get(declaration.record_type, ())
        for record in records:
            covered = any(
                _registration_covers(
                    reg, declaration.record_type, declaration.kind, record,
                )
                for reg in registry
            )
            if covered:
                continue
            field_part = (
                f".{declaration.field}" if declaration.field is not None
                else " (whole-record)"
            )
            message = (
                f"{declaration.record_type}{field_part} on "
                f"{record_dialect}:{record.id} is declared as "
                f"{declaration.kind}, but no registered check fires "
                f"on this record"
            )
            gaps.append(CoverageGap(
                record_type=declaration.record_type,
                record_id=record.id,
                record_dialect=record_dialect,
                field=declaration.field,
                coupling_kind=declaration.kind,
                message=message,
            ))
    return tuple(gaps)


def group_gaps_by_record(gaps: tuple) -> dict:
    """Bucket CoverageGaps by record_id. Useful for "show me everything
    unchecked about S_some_scene" reports."""
    out: dict = {}
    for g in gaps:
        out.setdefault(g.record_id, []).append(g)
    return out


def group_gaps_by_kind(gaps: tuple) -> dict:
    """Bucket CoverageGaps by coupling_kind. Useful for "how many
    Claim-moment fields have I left unchecked" summaries."""
    out: dict = {k: [] for k in ORCHESTRATABLE_COUPLING_KINDS}
    for g in gaps:
        out.setdefault(g.coupling_kind, []).append(g)
    return out


def group_gaps_by_record_type(gaps: tuple) -> dict:
    """Bucket CoverageGaps by record_type. Useful for "what record
    types have the most unchecked declarations" reports."""
    out: dict = {}
    for g in gaps:
        out.setdefault(g.record_type, []).append(g)
    return out


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
