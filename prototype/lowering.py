"""
lowering.py — first-pass implementation of lowering-record-sketch-01
(L1-L10). Dialect-agnostic.

This module implements the Lowering record and its supporting types
without importing from any specific dialect (substrate.py,
dramatic.py, etc.). Lowerings carry CrossDialectRefs (dialect string
+ record id) on both the upper and lower side; the dialect modules
are imported only by worked-examples modules that author specific
Lowerings (e.g., oedipus_lowerings.py).

Per lowering-record-sketch-01:

- L1 — Lowering records carry Realization couplings only. The other
  three coupling kinds (Characterization, Claim, Flavor) belong to
  the verifier surface (verification-sketch-01) or to nothing
  (Flavor). The shape and helpers in this module are designed for
  Realization; folding any other kind into Lowering is an
  architectural mistake the L1 commitment guards against.
- L2 — Record shape: id, upper_record, lower_records, annotation,
  position_range (optional), status, authored_by, τ_a,
  anchor_τ_a (optional), metadata.
- L3 — Many-to-many binding. One Lowering points at many lower
  records; one lower record can be the target of many Lowerings.
  No record-level deduplication enforced.
- L4 — `lower_records` admits typed-fact records and description
  records interchangeably; the Lowering schema is uniform regardless
  of target kind. The verifier may behave differently per target
  kind, but Lowering doesn't.
- L5 — `annotation` carries attention (structural / interpretive /
  flavor) and review_states. Same pattern as descriptions-01.
- L6 — Staleness via `anchor_τ_a` snapshot. Authored at construction
  time as max(lower_record.τ_a) where the lower dialect supports
  τ_a-style timestamping. Comparison happens at staleness-check
  time, performed by `staleness_signal`.
- L7 — Optional `position_range` for position correspondence between
  the upper and lower dialects when both use positional ordering.
  Author-declared.
- L8 — `status = "pending"` admits Lowerings authored against upper
  records whose lower realization doesn't yet exist. lower_records
  may be empty under "pending". ACTIVE is the default.
- L9 — Authored through the proposal queue; never synthesized.
  Supersession via metadata["supersedes"]/"superseded_by".
- L10 — Lowering records do not carry verification logic. A binding
  is just a binding; checking is verifier territory.

Deferred to follow-on passes:

- Verifier integration (verification-sketch-01). The verifier
  consumes Lowerings as input but is implemented separately.
- Reader-model proposal-queue integration. A LoweringProposal record
  parallel to AnswerProposal / EditProposal would land in the
  walker; this module's `Lowering` is the accepted form.
- Lowering descriptions (annotations-on-the-annotation, per
  descriptions-01's recursive description-on-description pattern).
  The annotation field is a single value here, not a record with its
  own description anchors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ============================================================================
# Cross-dialect references
# ============================================================================


@dataclass(frozen=True)
class CrossDialectRef:
    """A reference to a record in a specific dialect. The dialect's
    own modules are responsible for resolving the record_id to an
    actual record; this module just carries the pair.

    Examples:
        CrossDialectRef(dialect="dramatic", record_id="C_oedipus")
        CrossDialectRef(dialect="substrate", record_id="oedipus")
        CrossDialectRef(dialect="substrate", record_id="E_oedipus_anagnorisis")
    """
    dialect: str
    record_id: str

    def __repr__(self) -> str:
        return f"{self.dialect}:{self.record_id}"


def cross_ref(dialect: str, record_id: str) -> CrossDialectRef:
    """Convenience constructor — equivalent to the dataclass form
    but reads as a cleaner expression in encoding files."""
    return CrossDialectRef(dialect=dialect, record_id=record_id)


# ============================================================================
# Annotation
# ============================================================================
#
# Per L5, annotation is the binding's prose rationale. It carries
# attention and review_states, parallel to descriptions-01's
# Description record but as a value type (no id, no anchor).
#
# Attention values are strings rather than an enum to keep this module
# free of cross-module imports. The convention matches descriptions-01:
# "structural" / "interpretive" / "flavor".

ATTENTION_STRUCTURAL = "structural"
ATTENTION_INTERPRETIVE = "interpretive"
ATTENTION_FLAVOR = "flavor"

VALID_ATTENTIONS = frozenset({
    ATTENTION_STRUCTURAL,
    ATTENTION_INTERPRETIVE,
    ATTENTION_FLAVOR,
})


# Verdicts an annotation review can carry. Same vocabulary as
# substrate.ReviewVerdict but kept as strings here (cross-module
# independence).

VERDICT_APPROVED = "approved"
VERDICT_NEEDS_WORK = "needs-work"
VERDICT_REJECTED = "rejected"
VERDICT_NOTED = "noted"


@dataclass(frozen=True)
class AnnotationReview:
    """One review act on a Lowering's annotation. Mirrors
    substrate.ReviewEntry shape; kept here to preserve dialect-
    independence."""
    reviewer_id: str
    reviewed_at_τ_a: int
    verdict: str       # one of VERDICT_*
    anchor_τ_a: int    # snapshot of the Lowering's τ_a at review time
    comment: Optional[str] = None


@dataclass(frozen=True)
class Annotation:
    """Prose rationale for a Lowering binding. The annotation is
    where the author's reasoning lives — why these lower records
    realize this upper record. Reviewable, supersedable.

    `attention` is structural by default (most Lowerings are
    structural assertions about realization). Interpretive
    annotations discuss how *well* a binding reads; flavor
    annotations are author-side commentary not expected to be
    pressed."""
    text: str
    attention: str = ATTENTION_STRUCTURAL
    authored_by: str = "author"
    review_states: tuple = ()  # tuple[AnnotationReview, ...]


# ============================================================================
# Position correspondence
# ============================================================================


@dataclass(frozen=True)
class PositionRange:
    """When the upper and lower dialects both use positional
    ordering and the Lowering covers a range, this captures the
    lower-side range that realizes the upper record.

    `coord` names the lower-dialect coordinate (e.g., 'τ_d' for
    substrate sjuzhet ordering, 'narrative_position' for Dramatic
    scene order). `min_value` and `max_value` are inclusive
    integers."""
    coord: str
    min_value: int
    max_value: int


# ============================================================================
# Lowering record itself
# ============================================================================


class LoweringStatus(str, Enum):
    """Per L8. ACTIVE is the default. PENDING admits Lowerings
    authored against upper records whose lower realization doesn't
    yet exist; under PENDING, lower_records may be empty."""
    ACTIVE = "active"
    PENDING = "pending"


@dataclass(frozen=True)
class Lowering:
    """An authored binding from one upper-dialect record to one or
    more lower-dialect records, asserting that the lower records
    realize the upper one. Realization coupling only (L1).

    Constructor enforces L8: PENDING Lowerings may have empty
    `lower_records`; ACTIVE Lowerings must have at least one.
    """
    id: str
    upper_record: CrossDialectRef
    lower_records: tuple   # tuple[CrossDialectRef, ...]
    annotation: Annotation
    authored_by: str = "author"
    τ_a: int = 0
    status: LoweringStatus = LoweringStatus.ACTIVE
    position_range: Optional[PositionRange] = None
    anchor_τ_a: Optional[int] = None
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.status == LoweringStatus.ACTIVE and not self.lower_records:
            raise ValueError(
                f"Lowering {self.id!r} status=ACTIVE but lower_records "
                f"is empty; ACTIVE Lowerings must point at ≥1 lower "
                f"record (use status=PENDING for promissory bindings)"
            )


# ============================================================================
# Indexing helpers
# ============================================================================


def index_by_upper(lowerings: tuple) -> dict:
    """Group Lowerings by their upper_record. Returns dict mapping
    CrossDialectRef → list of Lowerings sharing that upper.

    Per L3, one upper record may have multiple Lowerings (most
    common case is supersession via metadata['supersedes']; an
    encoding might also have several distinct Lowerings on the same
    upper if the realization spans different boundary perspectives).
    """
    out = {}
    for lw in lowerings:
        out.setdefault(lw.upper_record, []).append(lw)
    return out


def index_by_lower(lowerings: tuple) -> dict:
    """Group Lowerings by *each* lower_record they reference. One
    lower record can be the target of many Lowerings (per L3); the
    returned dict reflects this with lists per lower CrossDialectRef.
    """
    out = {}
    for lw in lowerings:
        for lr in lw.lower_records:
            out.setdefault(lr, []).append(lw)
    return out


def by_status(lowerings: tuple, status: LoweringStatus) -> list:
    """Filter Lowerings by status. Convenience for walker / report
    code that wants to surface pending Lowerings separately."""
    return [lw for lw in lowerings if lw.status == status]


# ============================================================================
# Staleness (L6)
# ============================================================================


def staleness_signal(
    lowering: Lowering,
    current_τ_a_for: callable,
) -> Optional[int]:
    """Return the staleness signal for a Lowering, or None if the
    Lowering has no anchor_τ_a (the lower dialect doesn't support
    τ_a-style timestamping, or the author chose not to set one).

    `current_τ_a_for` is a callable mapping CrossDialectRef → current
    τ_a (or None if the ref has no current τ_a in the lower dialect).
    The caller wires this up — typically by inspecting the relevant
    dialect's record collection.

    Returns:
      - None if anchor_τ_a is None (staleness undefined).
      - 0 if no lower record's current τ_a exceeds the snapshot
        (the Lowering is fresh).
      - max(current - anchor) > 0 if any lower record has been
        edited since the Lowering was authored. The integer is how
        far the most-edited lower record has advanced past the
        anchor; bigger means more divergence.

    A non-zero positive return is the staleness flag. The caller
    decides what to do (surface as walker observation, etc.).
    """
    if lowering.anchor_τ_a is None:
        return None
    max_drift = 0
    for lr in lowering.lower_records:
        current = current_τ_a_for(lr)
        if current is None:
            continue
        drift = current - lowering.anchor_τ_a
        if drift > max_drift:
            max_drift = drift
    return max_drift


# ============================================================================
# Validation (lightweight; not the verifier)
# ============================================================================
#
# These checks are about the Lowering record itself being well-formed
# at the dialect-agnostic level: status invariants, supersession
# consistency, etc. They are NOT cross-dialect verification (does the
# binding's annotation actually hold? — that's verifier territory).


@dataclass(frozen=True)
class LoweringObservation:
    """A finding from `validate_lowerings`. Severity is "noted" or
    "advises-review"; code is a short stable tag."""
    severity: str
    code: str
    target_id: str
    message: str


def validate_lowerings(lowerings: tuple) -> list:
    """Self-consistency checks on a Lowering collection. Returns a
    list of LoweringObservation.

    Currently checks:
    - Duplicate Lowering ids.
    - PENDING Lowerings with non-empty lower_records (the
      __post_init__ check catches the inverse case; this surfaces
      the also-suspicious case of a PENDING Lowering that has
      records, since the author probably meant to flip status to
      ACTIVE).
    - Annotation attention values in VALID_ATTENTIONS.
    - Supersession metadata consistency: if metadata['supersedes']
      points at another Lowering id, that Lowering exists; and the
      superseded Lowering should have metadata['superseded_by']
      pointing back.
    """
    out = []
    by_id = {}
    for lw in lowerings:
        if lw.id in by_id:
            out.append(LoweringObservation(
                severity="advises-review",
                code="lowering_id_duplicate",
                target_id=lw.id,
                message=(f"Lowering id {lw.id!r} appears more than once "
                         f"in the collection"),
            ))
        by_id[lw.id] = lw

        if (lw.status == LoweringStatus.PENDING
                and lw.lower_records):
            out.append(LoweringObservation(
                severity="noted",
                code="pending_lowering_has_records",
                target_id=lw.id,
                message=(f"Lowering {lw.id!r} is PENDING but has "
                         f"non-empty lower_records ({len(lw.lower_records)} "
                         f"records); did you mean to flip to ACTIVE?"),
            ))

        if lw.annotation.attention not in VALID_ATTENTIONS:
            out.append(LoweringObservation(
                severity="advises-review",
                code="annotation_attention_unknown",
                target_id=lw.id,
                message=(f"Lowering {lw.id!r} annotation attention "
                         f"{lw.annotation.attention!r} not in "
                         f"{sorted(VALID_ATTENTIONS)}"),
            ))

    # Supersession consistency: pass after id-dup check so by_id is
    # populated.
    for lw in lowerings:
        supersedes_id = lw.metadata.get("supersedes")
        if supersedes_id is not None:
            if supersedes_id not in by_id:
                out.append(LoweringObservation(
                    severity="advises-review",
                    code="supersedes_unresolved",
                    target_id=lw.id,
                    message=(f"Lowering {lw.id!r} metadata['supersedes'] "
                             f"references {supersedes_id!r}, no such "
                             f"Lowering"),
                ))
            else:
                superseded = by_id[supersedes_id]
                back_ref = superseded.metadata.get("superseded_by")
                if back_ref != lw.id:
                    out.append(LoweringObservation(
                        severity="noted",
                        code="supersession_back_reference_missing",
                        target_id=supersedes_id,
                        message=(f"Lowering {supersedes_id!r} is "
                                 f"superseded by {lw.id!r} but its "
                                 f"metadata['superseded_by'] is "
                                 f"{back_ref!r}"),
                    ))

    return out


# ============================================================================
# Convenience grouping (mirrors dramatic.group_by_*)
# ============================================================================


def group_observations_by_severity(observations: list) -> dict:
    out = {"noted": [], "advises-review": []}
    for o in observations:
        out.setdefault(o.severity, []).append(o)
    return out


def group_observations_by_code(observations: list) -> dict:
    out = {}
    for o in observations:
        out.setdefault(o.code, []).append(o)
    return out
