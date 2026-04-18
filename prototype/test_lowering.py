"""
test_lowering.py — permanent tests for the Lowering record machinery
(lowering-record-sketch-01 L1-L10).

Synthetic-fixture tests pin each commitment independently. Integration
tests run against oedipus_lowerings.py to confirm the worked-examples
module produces a coherent set of bindings.

Run:  python3 test_lowering.py
"""

from __future__ import annotations

import sys
import traceback

from lowering import (
    CrossDialectRef, cross_ref,
    Annotation, AnnotationReview, PositionRange,
    Lowering, LoweringStatus, LoweringObservation,
    ATTENTION_STRUCTURAL, ATTENTION_INTERPRETIVE, ATTENTION_FLAVOR,
    VALID_ATTENTIONS,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK,
    index_by_upper, index_by_lower, by_status,
    staleness_signal,
    validate_lowerings,
    ingest_annotation_review,
    group_observations_by_severity, group_observations_by_code,
)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


def _trivial_lowering(**overrides) -> Lowering:
    base = dict(
        id="L_test",
        upper_record=cross_ref("dramatic", "X"),
        lower_records=(cross_ref("substrate", "x"),),
        annotation=Annotation(text="binding"),
        τ_a=100,
    )
    base.update(overrides)
    return Lowering(**base)


def _codes(observations: list) -> set:
    return {o.code for o in observations}


# ----------------------------------------------------------------------------
# CrossDialectRef
# ----------------------------------------------------------------------------


def test_cross_dialect_ref_repr_is_legible():
    r = cross_ref("dramatic", "C_oedipus")
    assert repr(r) == "dramatic:C_oedipus"


def test_cross_dialect_ref_equality_by_value():
    a = cross_ref("dramatic", "X")
    b = cross_ref("dramatic", "X")
    c = cross_ref("substrate", "X")
    assert a == b
    assert a != c


def test_cross_dialect_ref_is_hashable():
    """CrossDialectRef must be hashable so it can be a dict key
    (used by index_by_upper / index_by_lower)."""
    a = cross_ref("dramatic", "X")
    b = cross_ref("dramatic", "X")
    d = {a: "ok"}
    assert d[b] == "ok"


# ----------------------------------------------------------------------------
# L1 / L2 — record shape
# ----------------------------------------------------------------------------


def test_lowering_minimal_construction():
    lw = _trivial_lowering()
    assert lw.id == "L_test"
    assert lw.status == LoweringStatus.ACTIVE
    assert lw.position_range is None
    assert lw.anchor_τ_a is None
    assert lw.metadata == {}


# ----------------------------------------------------------------------------
# L8 — status invariants
# ----------------------------------------------------------------------------


def test_active_lowering_with_empty_lower_records_rejected():
    """ACTIVE Lowerings must point at ≥1 lower record; the
    constructor enforces this at __post_init__."""
    try:
        Lowering(
            id="L_bad",
            upper_record=cross_ref("dramatic", "X"),
            lower_records=(),  # empty + ACTIVE = invalid
            annotation=Annotation(text=""),
            τ_a=0,
        )
    except ValueError as e:
        assert "L_bad" in str(e)
        assert "ACTIVE" in str(e)
        return
    raise AssertionError("expected ValueError for empty ACTIVE lower_records")


def test_pending_lowering_with_empty_lower_records_admitted():
    """PENDING Lowerings may have empty lower_records — that's the
    promissory-binding case."""
    lw = Lowering(
        id="L_pending",
        upper_record=cross_ref("dramatic", "X"),
        lower_records=(),
        annotation=Annotation(text="will lower once realization exists"),
        τ_a=100,
        status=LoweringStatus.PENDING,
        metadata={"why_pending": "lower record not yet authored"},
    )
    assert lw.status == LoweringStatus.PENDING
    assert lw.lower_records == ()


def test_pending_lowering_with_non_empty_records_surfaces_observation():
    """A PENDING Lowering with lower_records is suspicious — the
    author probably meant ACTIVE. Construction is allowed; validator
    surfaces it."""
    lw = Lowering(
        id="L_weird",
        upper_record=cross_ref("dramatic", "X"),
        lower_records=(cross_ref("substrate", "y"),),
        annotation=Annotation(text=""),
        τ_a=100,
        status=LoweringStatus.PENDING,
    )
    obs = validate_lowerings((lw,))
    assert "pending_lowering_has_records" in _codes(obs)


# ----------------------------------------------------------------------------
# L3 — many-to-many binding
# ----------------------------------------------------------------------------


def test_one_lowering_can_have_many_lower_records():
    lw = _trivial_lowering(lower_records=(
        cross_ref("substrate", "a"),
        cross_ref("substrate", "b"),
        cross_ref("substrate", "c"),
    ))
    assert len(lw.lower_records) == 3


def test_one_lower_record_can_be_target_of_many_lowerings():
    """index_by_lower returns a list per lower CrossDialectRef so
    multiple Lowerings sharing a lower record are visible."""
    lr = cross_ref("substrate", "shared")
    lw1 = _trivial_lowering(id="L1", lower_records=(lr,))
    lw2 = _trivial_lowering(id="L2", lower_records=(lr,))
    idx = index_by_lower((lw1, lw2))
    assert len(idx[lr]) == 2
    assert {l.id for l in idx[lr]} == {"L1", "L2"}


# ----------------------------------------------------------------------------
# L4 — typed-fact and description targets uniform
# ----------------------------------------------------------------------------


def test_lower_records_can_mix_typed_and_description_targets():
    """The schema is uniform: Lowering doesn't care whether a target
    is a typed fact (e.g., substrate Event) or a description (e.g.,
    substrate Description). Both are CrossDialectRefs."""
    lw = _trivial_lowering(lower_records=(
        cross_ref("substrate", "E_some_event"),
        cross_ref("substrate", "D_some_description"),
    ))
    # Both are valid; no validation distinguishes them.
    obs = validate_lowerings((lw,))
    assert obs == []


# ----------------------------------------------------------------------------
# L5 — annotation attention
# ----------------------------------------------------------------------------


def test_annotation_default_attention_is_structural():
    a = Annotation(text="x")
    assert a.attention == ATTENTION_STRUCTURAL


def test_annotation_can_carry_review_states():
    review = AnnotationReview(
        reviewer_id="reviewer:test",
        reviewed_at_τ_a=200,
        verdict=VERDICT_APPROVED,
        anchor_τ_a=100,
        comment="reads honestly",
    )
    a = Annotation(text="x", review_states=(review,))
    assert len(a.review_states) == 1
    assert a.review_states[0].verdict == VERDICT_APPROVED


def test_annotation_with_unknown_attention_surfaces_observation():
    lw = _trivial_lowering(
        annotation=Annotation(text="x", attention="not-a-real-attention"),
    )
    obs = validate_lowerings((lw,))
    assert "annotation_attention_unknown" in _codes(obs)


def test_ingest_annotation_review_appends_and_does_not_mutate():
    """ingest_annotation_review returns a new Lowering with the review
    appended to annotation.review_states; the original is unchanged
    (frozen dataclass invariant). Mirrors substrate.ingest_review one
    tier up."""
    lw = _trivial_lowering()
    assert len(lw.annotation.review_states) == 0
    review = AnnotationReview(
        reviewer_id="llm:test",
        reviewed_at_τ_a=300,
        verdict=VERDICT_APPROVED,
        anchor_τ_a=lw.τ_a,
        comment="annotation reads honestly against the binding",
    )
    new_lw = ingest_annotation_review(lw, review)
    # Original untouched.
    assert len(lw.annotation.review_states) == 0
    # New Lowering carries the review.
    assert len(new_lw.annotation.review_states) == 1
    assert new_lw.annotation.review_states[0] is review
    # Annotation text and other fields are preserved.
    assert new_lw.annotation.text == lw.annotation.text
    assert new_lw.annotation.attention == lw.annotation.attention
    # Lowering-level fields preserved.
    assert new_lw.id == lw.id
    assert new_lw.upper_record == lw.upper_record
    assert new_lw.lower_records == lw.lower_records


def test_ingest_annotation_review_appends_to_existing_reviews():
    """A second ingest preserves the prior review and appends the new
    one in order — the review_states tuple is append-only."""
    first = AnnotationReview(
        reviewer_id="reviewer:a", reviewed_at_τ_a=300,
        verdict=VERDICT_APPROVED, anchor_τ_a=100, comment="first",
    )
    second = AnnotationReview(
        reviewer_id="reviewer:b", reviewed_at_τ_a=400,
        verdict=VERDICT_NEEDS_WORK, anchor_τ_a=100, comment="second",
    )
    lw = _trivial_lowering(
        annotation=Annotation(text="x", review_states=(first,)),
    )
    new_lw = ingest_annotation_review(lw, second)
    assert len(new_lw.annotation.review_states) == 2
    assert new_lw.annotation.review_states[0] is first
    assert new_lw.annotation.review_states[1] is second


# ----------------------------------------------------------------------------
# L6 — staleness via anchor_τ_a
# ----------------------------------------------------------------------------


def test_staleness_signal_none_when_anchor_undefined():
    lw = _trivial_lowering()  # no anchor_τ_a
    sig = staleness_signal(lw, current_τ_a_for=lambda r: 100)
    assert sig is None


def test_staleness_signal_zero_when_no_drift():
    lr = cross_ref("substrate", "x")
    lw = _trivial_lowering(
        lower_records=(lr,),
        anchor_τ_a=50,
    )
    # Current τ_a for x is also 50 — no drift.
    sig = staleness_signal(lw, current_τ_a_for=lambda r: 50)
    assert sig == 0


def test_staleness_signal_positive_when_lower_advanced():
    lr_a = cross_ref("substrate", "a")
    lr_b = cross_ref("substrate", "b")
    lw = _trivial_lowering(
        lower_records=(lr_a, lr_b),
        anchor_τ_a=50,
    )
    # `a` has advanced to 80; `b` is still 50. Max drift = 30.
    def current(r):
        return {lr_a: 80, lr_b: 50}[r]
    sig = staleness_signal(lw, current_τ_a_for=current)
    assert sig == 30


def test_staleness_signal_skips_records_with_no_current_τ_a():
    """Some lower records (e.g., substrate Entities) have no τ_a;
    the callable returns None for those, and staleness_signal skips
    them rather than failing."""
    lr_event = cross_ref("substrate", "E_x")
    lr_entity = cross_ref("substrate", "oedipus")
    lw = _trivial_lowering(
        lower_records=(lr_event, lr_entity),
        anchor_τ_a=10,
    )
    def current(r):
        if r == lr_event:
            return 15
        return None  # entity has no τ_a
    sig = staleness_signal(lw, current_τ_a_for=current)
    assert sig == 5


# ----------------------------------------------------------------------------
# L7 — position correspondence
# ----------------------------------------------------------------------------


def test_position_range_carried_intact():
    pr = PositionRange(coord="τ_d", min_value=0, max_value=8)
    lw = _trivial_lowering(position_range=pr)
    assert lw.position_range.coord == "τ_d"
    assert lw.position_range.min_value == 0
    assert lw.position_range.max_value == 8


# ----------------------------------------------------------------------------
# L9 — supersession metadata consistency
# ----------------------------------------------------------------------------


def test_supersession_with_proper_back_reference_passes():
    old = _trivial_lowering(
        id="L_old",
        metadata={"superseded_by": "L_new"},
    )
    new = _trivial_lowering(
        id="L_new",
        metadata={"supersedes": "L_old"},
    )
    obs = validate_lowerings((old, new))
    assert "supersedes_unresolved" not in _codes(obs)
    assert "supersession_back_reference_missing" not in _codes(obs)


def test_supersedes_unresolved_id_surfaces():
    new = _trivial_lowering(
        id="L_new",
        metadata={"supersedes": "L_does_not_exist"},
    )
    obs = validate_lowerings((new,))
    assert "supersedes_unresolved" in _codes(obs)


def test_supersession_back_reference_missing_surfaces():
    old = _trivial_lowering(id="L_old")  # no superseded_by metadata
    new = _trivial_lowering(
        id="L_new",
        metadata={"supersedes": "L_old"},
    )
    obs = validate_lowerings((old, new))
    assert "supersession_back_reference_missing" in _codes(obs)


# ----------------------------------------------------------------------------
# Indexing helpers
# ----------------------------------------------------------------------------


def test_index_by_upper_groups_by_upper_record():
    upper_a = cross_ref("dramatic", "A")
    upper_b = cross_ref("dramatic", "B")
    lw1 = _trivial_lowering(id="L1", upper_record=upper_a)
    lw2 = _trivial_lowering(id="L2", upper_record=upper_a)  # same upper
    lw3 = _trivial_lowering(id="L3", upper_record=upper_b)
    idx = index_by_upper((lw1, lw2, lw3))
    assert len(idx[upper_a]) == 2
    assert len(idx[upper_b]) == 1


def test_by_status_filters():
    lw1 = _trivial_lowering(id="L1")  # ACTIVE
    lw2 = Lowering(
        id="L2",
        upper_record=cross_ref("dramatic", "Y"),
        lower_records=(),
        annotation=Annotation(text=""),
        τ_a=0,
        status=LoweringStatus.PENDING,
    )
    active = by_status((lw1, lw2), LoweringStatus.ACTIVE)
    pending = by_status((lw1, lw2), LoweringStatus.PENDING)
    assert [l.id for l in active] == ["L1"]
    assert [l.id for l in pending] == ["L2"]


# ----------------------------------------------------------------------------
# Validator — duplicate ids
# ----------------------------------------------------------------------------


def test_duplicate_lowering_ids_surface():
    lw1 = _trivial_lowering(id="L_dup")
    lw2 = _trivial_lowering(id="L_dup")
    obs = validate_lowerings((lw1, lw2))
    assert "lowering_id_duplicate" in _codes(obs)


# ----------------------------------------------------------------------------
# Integration — oedipus_lowerings
# ----------------------------------------------------------------------------


def test_oedipus_lowerings_validates_clean():
    """The worked-examples module's Lowering set passes validation
    with no observations."""
    import oedipus_lowerings as ol
    obs = validate_lowerings(ol.LOWERINGS)
    assert obs == [], (
        f"oedipus_lowerings should validate cleanly; got "
        f"{[(o.code, o.target_id) for o in obs]}"
    )


def test_oedipus_lowerings_split_by_status():
    """After the F5 substrate extension (2026-04-16) and the
    Oedipus-hygiene pass (2026-04-17 — removed the
    L_discovery_and_crown_pending placeholder which referenced a
    non-existent Scene), 16 ACTIVE + 1 PENDING is the encoding's
    contract. Tiresias/Creon Characters are ACTIVE (Entities added).
    The remaining PENDING is the prologue (still cut from substrate);
    the discovery-and-crown placeholder was removed during hygiene."""
    import oedipus_lowerings as ol
    active = by_status(ol.LOWERINGS, LoweringStatus.ACTIVE)
    pending = by_status(ol.LOWERINGS, LoweringStatus.PENDING)
    assert len(active) == 16, f"expected 16 ACTIVE, got {len(active)}"
    assert len(pending) == 1, f"expected 1 PENDING, got {len(pending)}"


def test_oedipus_lowerings_throughline_realization_uses_position_range():
    """The MC Throughline Lowering carries a PositionRange spanning
    fabula τ_s from birth (-100) through exile (17)."""
    import oedipus_lowerings as ol
    mc = next(l for l in ol.LOWERINGS if l.id == "L_mc_throughline")
    assert mc.position_range is not None
    assert mc.position_range.coord == "τ_s"
    assert mc.position_range.min_value == -100
    assert mc.position_range.max_value == 17
    # And it spans many lower records (13 after F5 extension).
    assert len(mc.lower_records) >= 13


def test_oedipus_lowerings_anchor_τ_a_set_for_event_targets():
    """Lowerings whose lower side includes substrate events have
    anchor_τ_a set; Lowerings whose lower side is only substrate
    Entities have anchor_τ_a=None (entities have no τ_a)."""
    import oedipus_lowerings as ol
    # L_oedipus binds Character → Entity. anchor_τ_a should be None.
    char = next(l for l in ol.LOWERINGS if l.id == "L_oedipus")
    assert char.anchor_τ_a is None
    # L_anagnorisis binds Scene → Event. anchor_τ_a should be set.
    scene = next(l for l in ol.LOWERINGS if l.id == "L_anagnorisis")
    assert scene.anchor_τ_a is not None
    assert scene.anchor_τ_a > 0


def test_oedipus_lowerings_pending_carry_why_metadata():
    """Every PENDING Lowering carries metadata['why_pending']
    documenting why it can't bind yet."""
    import oedipus_lowerings as ol
    for lw in by_status(ol.LOWERINGS, LoweringStatus.PENDING):
        assert "why_pending" in lw.metadata, (
            f"PENDING Lowering {lw.id!r} has no why_pending metadata"
        )


def test_oedipus_lowerings_index_by_upper_one_per_upper():
    """In this encoding, each Dramatic upper record has exactly one
    Lowering. Index maps each upper to a singleton list."""
    import oedipus_lowerings as ol
    idx = index_by_upper(ol.LOWERINGS)
    for upper, lws in idx.items():
        assert len(lws) == 1, (
            f"upper {upper} has {len(lws)} Lowerings; expected 1 in this encoding"
        )


# ----------------------------------------------------------------------------
# Test runner
# ----------------------------------------------------------------------------


TESTS = [
    # CrossDialectRef
    test_cross_dialect_ref_repr_is_legible,
    test_cross_dialect_ref_equality_by_value,
    test_cross_dialect_ref_is_hashable,
    # L1 / L2 — shape
    test_lowering_minimal_construction,
    # L8 — status invariants
    test_active_lowering_with_empty_lower_records_rejected,
    test_pending_lowering_with_empty_lower_records_admitted,
    test_pending_lowering_with_non_empty_records_surfaces_observation,
    # L3 — many-to-many
    test_one_lowering_can_have_many_lower_records,
    test_one_lower_record_can_be_target_of_many_lowerings,
    # L4 — uniform target shape
    test_lower_records_can_mix_typed_and_description_targets,
    # L5 — annotation
    test_annotation_default_attention_is_structural,
    test_annotation_can_carry_review_states,
    test_annotation_with_unknown_attention_surfaces_observation,
    test_ingest_annotation_review_appends_and_does_not_mutate,
    test_ingest_annotation_review_appends_to_existing_reviews,
    # L6 — staleness
    test_staleness_signal_none_when_anchor_undefined,
    test_staleness_signal_zero_when_no_drift,
    test_staleness_signal_positive_when_lower_advanced,
    test_staleness_signal_skips_records_with_no_current_τ_a,
    # L7 — position correspondence
    test_position_range_carried_intact,
    # L9 — supersession metadata
    test_supersession_with_proper_back_reference_passes,
    test_supersedes_unresolved_id_surfaces,
    test_supersession_back_reference_missing_surfaces,
    # Indexing helpers
    test_index_by_upper_groups_by_upper_record,
    test_by_status_filters,
    # Validator
    test_duplicate_lowering_ids_surface,
    # Integration
    test_oedipus_lowerings_validates_clean,
    test_oedipus_lowerings_split_by_status,
    test_oedipus_lowerings_throughline_realization_uses_position_range,
    test_oedipus_lowerings_anchor_τ_a_set_for_event_targets,
    test_oedipus_lowerings_pending_carry_why_metadata,
    test_oedipus_lowerings_index_by_upper_one_per_upper,
]


def main() -> int:
    passed = 0
    failed = 0
    for test in TESTS:
        try:
            test()
        except AssertionError as e:
            print(f"FAIL  {test.__name__}")
            print(f"      {e}")
            failed += 1
            continue
        except Exception:
            print(f"ERROR {test.__name__}")
            traceback.print_exc()
            failed += 1
            continue
        print(f"ok    {test.__name__}")
        passed += 1

    print()
    print(f"{passed} passed, {failed} failed, {len(TESTS)} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
