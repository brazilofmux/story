"""
test_aristotelian_reader_model_client.py — tests for the
Aristotelian-dialect LLM probe client.

Same shape as test_dramatic_reader_model_client.py: synthetic
Pydantic outputs run through the classify / translate pipeline
without hitting the API. Plus dry-run prompt-construction checks
against the real Oedipus and Rashomon Aristotelian encodings.

Covers:
- Eligible-target enumeration (Oedipus / Rashomon / synthetic
  fixtures with no hamartia_text).
- Prompt construction: records section, observations section
  (with + without observations), substrate grounding,
  task-section naming.
- Scope enforcement on annotation reviews: out-of-scope triple,
  unresolved target_id, (target_kind, field) mis-pairing.
- Scope enforcement on observation commentaries: unresolved id,
  out-of-scope id.
- Translation: annotation review (anchor_τ_a, reviewer_id),
  observation commentary (target_observation resolved to the
  actual object), dialect reading (list → tuple).
- Full round-trip translation through translate_raw_output with
  a mix of accepted + dropped raws.

Run:
    cd prototype
    .venv/bin/python3 -m tests.test_aristotelian_reader_model_client
"""

from __future__ import annotations

import sys
import traceback

from story_engine.core.aristotelian import (
    ArAnnotationReview, ArCharacter, ArMythos, ArObservation,
    ArObservationCommentary, ArPhase, DialectReading,
    FIELD_ACTION_SUMMARY, FIELD_ANNOTATION, FIELD_HAMARTIA_TEXT,
    FIELD_PHASE_ANNOTATION,
    PHASE_BEGINNING, PHASE_END, PHASE_MIDDLE,
    PLOT_COMPLEX, PLOT_SIMPLE,
    SEVERITY_ADVISES_REVIEW,
    TARGET_AR_ANAGNORISIS_STEP,
    TARGET_AR_CHARACTER,
    TARGET_AR_CHARACTER_ARC_RELATION,
    TARGET_AR_MYTHOS,
    TARGET_AR_PHASE,
)
from story_engine.core.aristotelian_reader_model_client import (
    AristotelianAnnotationReview,
    AristotelianReaderOutput,
    DialectReadingOutput,
    DroppedOutput,
    ObservationCommentary,
    _classify_annotation_review,
    _classify_observation_commentary,
    _eligible_targets,
    _records_by_kind_id,
    _translate_annotation_review,
    _translate_dialect_reading,
    _translate_observation_commentary,
    build_user_prompt,
    translate_raw_output,
)


# ============================================================================
# Fixtures — synthetic dialect records + real encoding imports
# ============================================================================


def _synthetic_mythos(
    id: str = "m_test",
    plot_kind: str = PLOT_SIMPLE,
    with_characters: bool = True,
    with_hamartia: bool = True,
) -> ArMythos:
    """A tiny one-mythos encoding suitable for scope / translation
    tests. Three phases, central_event_ids = e0..e2, optional
    characters."""
    phases = (
        ArPhase(id="p_b", role=PHASE_BEGINNING,
                scope_event_ids=("e0",),
                annotation="opening phase"),
        ArPhase(id="p_m", role=PHASE_MIDDLE,
                scope_event_ids=("e1",),
                annotation="middle phase"),
        ArPhase(id="p_e", role=PHASE_END,
                scope_event_ids=("e2",),
                annotation="end phase"),
    )
    characters: tuple = ()
    if with_characters:
        characters = (
            ArCharacter(
                id="c_hero", name="Hero",
                hamartia_text=(
                    "missed the mark" if with_hamartia else None
                ),
                is_tragic_hero=True,
            ),
        )
    return ArMythos(
        id=id, title="Test mythos",
        action_summary="a test",
        plot_kind=plot_kind,
        central_event_ids=("e0", "e1", "e2"),
        phases=phases,
        characters=characters,
    )


def _synthetic_observations() -> tuple:
    """Two ArObservations for commentary-surface tests. Both have
    severity="advises-review" so the commentary surface has
    something substantial to commentate on."""
    return (
        ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="phase_overlap",
            target_id="m_test",
            message="Event 'e0' appears in multiple phase scopes.",
        ),
        ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="complex_missing_peripeteia_or_anagnorisis",
            target_id="m_test",
            message=(
                "Complex plot requires peripeteia or anagnorisis."
            ),
        ),
    )


# ============================================================================
# Eligible-target enumeration
# ============================================================================


def test_eligible_targets_oedipus_count():
    """Oedipus's Aristotelian encoding — 1 ArMythos + 3 phases +
    2 characters (both with hamartia_text) + 1 ArAnagnorisisStep
    (AR_STEP_JOCASTA, sketch-02) = 7 eligible prose fields under
    sketch-04 APA4-3 (staging-step / arc-relation annotations are
    reviewable)."""
    from story_engine.encodings.oedipus_aristotelian import (
        AR_OEDIPUS_MYTHOS,
    )
    targets = _eligible_targets((AR_OEDIPUS_MYTHOS,))
    assert len(targets) == 7, (
        f"expected 7 eligible targets on Oedipus; got {len(targets)}"
    )
    kinds = sorted(set(t[0] for t in targets))
    assert kinds == [
        TARGET_AR_ANAGNORISIS_STEP,
        TARGET_AR_CHARACTER,
        TARGET_AR_MYTHOS,
        TARGET_AR_PHASE,
    ]


def test_eligible_targets_rashomon_count():
    """Rashomon — 4 ArMythos × (1 action_summary + 3 phase
    annotations + 1 hamartia_text) = 20 eligible prose fields."""
    from story_engine.encodings.rashomon_aristotelian import (
        AR_RASHOMON_MYTHOI,
    )
    targets = _eligible_targets(AR_RASHOMON_MYTHOI)
    assert len(targets) == 20, (
        f"expected 20 eligible targets on Rashomon; got {len(targets)}"
    )
    mythos_count = sum(1 for t in targets if t[0] == TARGET_AR_MYTHOS)
    phase_count = sum(1 for t in targets if t[0] == TARGET_AR_PHASE)
    char_count = sum(1 for t in targets if t[0] == TARGET_AR_CHARACTER)
    assert mythos_count == 4
    assert phase_count == 12
    assert char_count == 4


def test_eligible_targets_skips_characters_without_hamartia():
    """An ArCharacter with hamartia_text=None has nothing to
    review; _eligible_targets drops it."""
    mythos = _synthetic_mythos(with_hamartia=False)
    targets = _eligible_targets((mythos,))
    char_targets = [t for t in targets if t[0] == TARGET_AR_CHARACTER]
    assert char_targets == [], (
        f"expected no character targets when hamartia_text is None; "
        f"got {char_targets}"
    )
    # Mythos and phases still count: 1 + 3 = 4
    assert len(targets) == 4


def test_records_by_kind_id_indexes_all_records():
    """Every ArMythos / ArPhase / ArCharacter across all mythoi is
    in the index, keyed on (kind, id)."""
    m1 = _synthetic_mythos(id="m_one")
    m2 = _synthetic_mythos(id="m_two")
    index = _records_by_kind_id((m1, m2))
    assert (TARGET_AR_MYTHOS, "m_one") in index
    assert (TARGET_AR_MYTHOS, "m_two") in index
    # Phase ids overlap between mythoi; the last one wins in the
    # flat index — acceptable for this usage because the validator
    # only needs existence and scope validation also checks
    # (target_kind, target_id, field) in targets_to_review.
    assert (TARGET_AR_PHASE, "p_b") in index
    assert (TARGET_AR_CHARACTER, "c_hero") in index


# ============================================================================
# Prompt construction
# ============================================================================


def test_prompt_construction_oedipus_basic():
    """The Oedipus invocation's prompt contains the ArMythos
    records section, the 'no observations' marker, the substrate
    section, and the task section."""
    from story_engine.encodings.oedipus_aristotelian import (
        AR_OEDIPUS_MYTHOS,
    )
    from story_engine.encodings.oedipus import FABULA
    targets = _eligible_targets((AR_OEDIPUS_MYTHOS,))
    prompt, id_map = build_user_prompt(
        mythoi=(AR_OEDIPUS_MYTHOS,),
        observations=(),
        substrate_events=list(FABULA),
        targets_to_review=targets,
        observations_to_comment_on=[],
    )
    assert "# Aristotelian dialect surface" in prompt
    assert "## ArMythos records" in prompt
    assert "## ArObservations" in prompt
    assert "(no observations — encoding verifies clean)" in prompt
    assert "## Substrate context" in prompt
    assert "## Task" in prompt
    assert "ar_oedipus" in prompt
    assert "ph_oedipus_beginning" in prompt
    assert id_map == {}


def test_prompt_construction_rashomon_all_four_mythoi_appear():
    """All four Rashomon testimony mythoi render into the prompt."""
    from story_engine.encodings.rashomon_aristotelian import (
        AR_RASHOMON_MYTHOI,
    )
    from story_engine.encodings.rashomon import EVENTS_ALL
    targets = _eligible_targets(AR_RASHOMON_MYTHOI)
    prompt, _ = build_user_prompt(
        mythoi=AR_RASHOMON_MYTHOI,
        observations=(),
        substrate_events=list(EVENTS_ALL),
        targets_to_review=targets,
        observations_to_comment_on=[],
    )
    # Each Rashomon testimony mythos id contains a testifier name
    for expected in (
        "ar_rashomon_bandit", "ar_rashomon_wife",
        "ar_rashomon_samurai", "ar_rashomon_woodcutter",
    ):
        assert expected in prompt, (
            f"expected mythos id {expected!r} rendered in prompt"
        )


def test_prompt_construction_substrate_section_omitted_when_empty():
    """No substrate_events → no substrate section (parallel to
    dramatic client's substrate-context pattern)."""
    mythos = _synthetic_mythos()
    prompt, _ = build_user_prompt(
        mythoi=(mythos,),
        observations=(),
        substrate_events=[],
        targets_to_review=_eligible_targets((mythos,)),
        observations_to_comment_on=[],
    )
    assert "## Substrate context" not in prompt


def test_prompt_construction_observations_section_with_observations():
    """When observations are passed, the section renders them with
    synthetic ids ao_0, ao_1, … and the id_map maps back."""
    mythos = _synthetic_mythos()
    observations = _synthetic_observations()
    prompt, id_map = build_user_prompt(
        mythoi=(mythos,),
        observations=observations,
        substrate_events=[],
        targets_to_review=_eligible_targets((mythos,)),
        observations_to_comment_on=["ao_0", "ao_1"],
    )
    assert "ao_0" in prompt
    assert "ao_1" in prompt
    assert "phase_overlap" in prompt
    assert "(no observations — encoding verifies clean)" not in prompt
    assert id_map == {"ao_0": observations[0], "ao_1": observations[1]}


def test_prompt_construction_task_section_names_targets():
    """The task section lists each (kind, id, field) triple
    explicitly."""
    mythos = _synthetic_mythos()
    targets = _eligible_targets((mythos,))
    prompt, _ = build_user_prompt(
        mythoi=(mythos,),
        observations=(),
        substrate_events=[],
        targets_to_review=targets,
        observations_to_comment_on=[],
    )
    assert "ArMythos:m_test:action_summary" in prompt
    assert "ArPhase:p_b:annotation" in prompt
    assert "ArCharacter:c_hero:hamartia_text" in prompt


def test_prompt_construction_methodological_lever_in_system_prompt():
    """The system prompt's vocabulary rule is present — the
    methodological lever APS3 hangs the probe's falsifiability on."""
    from story_engine.core.aristotelian_reader_model_client import (
        SYSTEM_PROMPT,
    )
    assert "peripeteia" in SYSTEM_PROMPT
    assert "anagnorisis" in SYSTEM_PROMPT
    assert "hamartia" in SYSTEM_PROMPT
    assert "drift_flagged" in SYSTEM_PROMPT
    # Must explicitly warn against other-dialect vocabulary
    assert "DSP_limit" in SYSTEM_PROMPT or "Dramatica" in SYSTEM_PROMPT


# ============================================================================
# Annotation-review scope enforcement (R5)
# ============================================================================


def test_annotation_review_in_scope_accepted():
    """A review targeting a rendered record via a declared triple
    is accepted."""
    mythos = _synthetic_mythos()
    records_index = _records_by_kind_id((mythos,))
    targets = _eligible_targets((mythos,))
    raw = AristotelianAnnotationReview(
        target_kind=TARGET_AR_MYTHOS, target_id="m_test",
        field=FIELD_ACTION_SUMMARY, verdict="approved",
        rationale="solid summary",
    )
    reason = _classify_annotation_review(raw, records_index, targets)
    assert reason is None, f"expected accepted; got drop: {reason}"


def test_annotation_review_outside_scope_rejected():
    """R5: a triple pointing at a rendered record but NOT in
    targets_to_review drops at ingest."""
    mythos = _synthetic_mythos()
    records_index = _records_by_kind_id((mythos,))
    # Only allow mythos-level review
    narrowed_targets = [
        (TARGET_AR_MYTHOS, "m_test", FIELD_ACTION_SUMMARY),
    ]
    # But the LLM targets a phase anyway
    raw = AristotelianAnnotationReview(
        target_kind=TARGET_AR_PHASE, target_id="p_b",
        field=FIELD_PHASE_ANNOTATION, verdict="approved",
        rationale="ok",
    )
    reason = _classify_annotation_review(
        raw, records_index, narrowed_targets,
    )
    assert reason is not None
    assert "targets_to_review" in reason


def test_annotation_review_unknown_target_id_rejected():
    """A target_id that doesn't resolve to any rendered record
    drops, even when nominally in scope."""
    mythos = _synthetic_mythos()
    records_index = _records_by_kind_id((mythos,))
    targets = [(TARGET_AR_MYTHOS, "m_ghost", FIELD_ACTION_SUMMARY)]
    raw = AristotelianAnnotationReview(
        target_kind=TARGET_AR_MYTHOS, target_id="m_ghost",
        field=FIELD_ACTION_SUMMARY, verdict="approved",
        rationale="ghost",
    )
    reason = _classify_annotation_review(raw, records_index, targets)
    assert reason is not None
    assert "does not resolve" in reason


def test_annotation_review_kind_field_mismatch_rejected():
    """A (target_kind, field) mis-pair (e.g., ArMythos +
    hamartia_text) drops. FIELDS_BY_TARGET_KIND enforces the
    one-field-per-kind rule per APS2."""
    mythos = _synthetic_mythos()
    records_index = _records_by_kind_id((mythos,))
    # Scope allows the triple nominally, but the mis-pair fails
    # before the scope check
    targets = [(TARGET_AR_MYTHOS, "m_test", FIELD_HAMARTIA_TEXT)]
    raw = AristotelianAnnotationReview(
        target_kind=TARGET_AR_MYTHOS, target_id="m_test",
        field=FIELD_HAMARTIA_TEXT, verdict="approved",
        rationale="miss-paired",
    )
    reason = _classify_annotation_review(raw, records_index, targets)
    assert reason is not None
    assert "does not pair with target_kind" in reason


# ============================================================================
# Annotation-review translation
# ============================================================================


def test_translate_annotation_review_produces_ar_record():
    """An accepted raw → ArAnnotationReview with reviewer_id,
    anchor_τ_a supplied by caller, verdict, comment-from-rationale,
    and the full (target_kind, target_id, field) triple
    preserved."""
    raw = AristotelianAnnotationReview(
        target_kind=TARGET_AR_PHASE, target_id="p_m",
        field=FIELD_PHASE_ANNOTATION, verdict="needs-work",
        rationale="the annotation overstates what the middle holds",
    )
    review = _translate_annotation_review(
        raw, reviewer_id="llm:test", current_τ_a=500, anchor_τ_a=300,
    )
    assert isinstance(review, ArAnnotationReview)
    assert review.reviewer_id == "llm:test"
    assert review.reviewed_at_τ_a == 500
    assert review.anchor_τ_a == 300
    assert review.target_kind == TARGET_AR_PHASE
    assert review.target_id == "p_m"
    assert review.field == FIELD_PHASE_ANNOTATION
    assert review.verdict == "needs-work"
    assert review.comment == (
        "the annotation overstates what the middle holds"
    )


# ============================================================================
# Observation-commentary scope enforcement
# ============================================================================


def test_observation_commentary_in_scope_accepted():
    """A commentary with a resolvable synthetic id in scope is
    accepted."""
    observations = _synthetic_observations()
    id_map = {"ao_0": observations[0], "ao_1": observations[1]}
    raw = ObservationCommentary(
        target_observation_id="ao_0",
        assessment="endorses",
        rationale="the A7 check's message names the cause",
    )
    reason = _classify_observation_commentary(
        raw, id_map, observations_to_comment_on=["ao_0", "ao_1"],
    )
    assert reason is None


def test_observation_commentary_unknown_id_rejected():
    """A synthetic id not in the id_map drops."""
    observations = _synthetic_observations()
    id_map = {"ao_0": observations[0]}
    raw = ObservationCommentary(
        target_observation_id="ao_99",
        assessment="endorses",
        rationale="ghost",
    )
    reason = _classify_observation_commentary(
        raw, id_map, observations_to_comment_on=["ao_99"],
    )
    assert reason is not None
    assert "does not resolve" in reason


def test_observation_commentary_outside_scope_rejected():
    """An id in the id_map but NOT in observations_to_comment_on
    drops."""
    observations = _synthetic_observations()
    id_map = {"ao_0": observations[0], "ao_1": observations[1]}
    raw = ObservationCommentary(
        target_observation_id="ao_1",
        assessment="endorses",
        rationale="out of scope",
    )
    reason = _classify_observation_commentary(
        raw, id_map, observations_to_comment_on=["ao_0"],
    )
    assert reason is not None
    assert "observations_to_comment_on" in reason


# ============================================================================
# Observation-commentary translation
# ============================================================================


def test_translate_observation_commentary_resolves_target():
    """An accepted raw → ArObservationCommentary carrying the
    resolved ArObservation object (not a copy, not the id)."""
    observations = _synthetic_observations()
    id_map = {"ao_0": observations[0], "ao_1": observations[1]}
    raw = ObservationCommentary(
        target_observation_id="ao_1",
        assessment="qualifies",
        rationale=(
            "the check's message is accurate but could name the "
            "configured plot_kind value for clarity"
        ),
        suggested_signature=(
            "include plot_kind value in the message text"
        ),
    )
    commentary = _translate_observation_commentary(
        raw, id_map, commenter_id="llm:test", current_τ_a=500,
    )
    assert isinstance(commentary, ArObservationCommentary)
    assert commentary.commenter_id == "llm:test"
    assert commentary.commented_at_τ_a == 500
    assert commentary.assessment == "qualifies"
    assert commentary.target_observation is observations[1]
    assert commentary.target_observation.code == (
        "complex_missing_peripeteia_or_anagnorisis"
    )
    assert commentary.suggested_signature is not None


# ============================================================================
# Dialect-reading translation
# ============================================================================


def test_translate_dialect_reading_converts_lists_to_tuples():
    """Pydantic ships list fields; the translated DialectReading
    record holds tuples for the frozen-dataclass hashability
    discipline."""
    raw = DialectReadingOutput(
        read_on_terms="partial",
        rationale=(
            "engaged peripeteia and anagnorisis cleanly; flagged "
            "scope-limits on character-level recognition"
        ),
        drift_flagged=[],
        scope_limits_observed=[
            "meta-anagnorisis: audience-level recognition",
        ],
        relations_wanted=["ArMythosRelation for contest"],
    )
    reading = _translate_dialect_reading(
        raw, reader_id="llm:test", current_τ_a=500,
    )
    assert isinstance(reading, DialectReading)
    assert reading.read_on_terms == "partial"
    assert isinstance(reading.drift_flagged, tuple)
    assert isinstance(reading.scope_limits_observed, tuple)
    assert isinstance(reading.relations_wanted, tuple)
    assert reading.scope_limits_observed[0].startswith(
        "meta-anagnorisis"
    )
    assert reading.relations_wanted == ("ArMythosRelation for contest",)


# ============================================================================
# Full-roundtrip translation
# ============================================================================


def test_translate_raw_output_full_roundtrip():
    """Raw output with one accepted annotation review, one accepted
    observation commentary, and one dialect reading translates to
    three populated result collections and no drops."""
    mythos = _synthetic_mythos()
    observations = _synthetic_observations()
    targets = _eligible_targets((mythos,))
    id_map = {"ao_0": observations[0], "ao_1": observations[1]}
    raw = AristotelianReaderOutput(
        annotation_reviews=[
            AristotelianAnnotationReview(
                target_kind=TARGET_AR_MYTHOS, target_id="m_test",
                field=FIELD_ACTION_SUMMARY, verdict="approved",
                rationale="solid",
            ),
        ],
        observation_commentaries=[
            ObservationCommentary(
                target_observation_id="ao_0",
                assessment="endorses",
                rationale="well-grounded",
            ),
        ],
        dialect_reading=DialectReadingOutput(
            read_on_terms="yes",
            rationale="engaged cleanly",
        ),
    )
    result = translate_raw_output(
        raw=raw, mythoi=(mythos,), id_map=id_map,
        targets_to_review=targets,
        observations_to_comment_on=["ao_0", "ao_1"],
        reviewer_id="llm:test", current_τ_a=500, anchor_τ_a=400,
    )
    assert len(result.annotation_reviews) == 1
    assert len(result.observation_commentaries) == 1
    assert result.dialect_reading is not None
    assert result.dropped == []
    assert result.annotation_reviews[0].comment == "solid"
    assert result.observation_commentaries[0].target_observation is (
        observations[0]
    )


def test_translate_raw_output_drops_invalid_alongside_accepted():
    """Mixed raw with one accepted review and one out-of-scope
    review — only the accepted one lands in results; the other is
    in dropped with a reason."""
    mythos = _synthetic_mythos()
    targets = [(TARGET_AR_MYTHOS, "m_test", FIELD_ACTION_SUMMARY)]
    raw = AristotelianReaderOutput(
        annotation_reviews=[
            AristotelianAnnotationReview(
                target_kind=TARGET_AR_MYTHOS, target_id="m_test",
                field=FIELD_ACTION_SUMMARY, verdict="approved",
                rationale="in scope",
            ),
            # Out of scope — phase annotation not in targets
            AristotelianAnnotationReview(
                target_kind=TARGET_AR_PHASE, target_id="p_b",
                field=FIELD_PHASE_ANNOTATION, verdict="approved",
                rationale="should drop",
            ),
        ],
        dialect_reading=DialectReadingOutput(
            read_on_terms="yes", rationale="clean",
        ),
    )
    result = translate_raw_output(
        raw=raw, mythoi=(mythos,), id_map={},
        targets_to_review=targets,
        observations_to_comment_on=[],
        reviewer_id="llm:test", current_τ_a=500, anchor_τ_a=400,
    )
    assert len(result.annotation_reviews) == 1
    assert result.annotation_reviews[0].comment == "in scope"
    assert len(result.dropped) == 1
    assert isinstance(result.dropped[0], DroppedOutput)
    assert "targets_to_review" in result.dropped[0].reason


def test_translate_raw_output_empty_dialect_reading_stays_none():
    """A Pydantic output with dialect_reading=None translates to a
    result with dialect_reading=None. Robust to refusal / malformed
    cases where the LLM didn't emit the reading."""
    mythos = _synthetic_mythos()
    raw = AristotelianReaderOutput(
        annotation_reviews=[], observation_commentaries=[],
        dialect_reading=None,
    )
    result = translate_raw_output(
        raw=raw, mythoi=(mythos,), id_map={},
        targets_to_review=[], observations_to_comment_on=[],
        reviewer_id="llm:test", current_τ_a=500, anchor_τ_a=400,
    )
    assert result.dialect_reading is None
    assert result.annotation_reviews == []
    assert result.observation_commentaries == []
    assert result.dropped == []


# ============================================================================
# Sketch-04 APA4: sketch-03 rendering extensions
# ============================================================================


def test_sketch04_step_kind_renders_in_step_dict():
    """APA4-1: _ar_anagnorisis_step_to_dict includes step_kind so
    the probe reads the sketch-03 vocabulary ('staging' / 'parallel'
    / 'precipitating') the encoding authored."""
    from story_engine.core.aristotelian import (
        ArAnagnorisisStep, STEP_KIND_STAGING,
    )
    from story_engine.core.aristotelian_reader_model_client import (
        _ar_anagnorisis_step_to_dict,
    )
    step = ArAnagnorisisStep(
        id="arstep_test",
        event_id="E_reveal",
        character_ref_id="c_hero",
        step_kind=STEP_KIND_STAGING,
        precipitates_main=True,
        annotation="staged reveal",
    )
    rendered = _ar_anagnorisis_step_to_dict(step)
    assert rendered["step_kind"] == STEP_KIND_STAGING
    # Pre-sketch-03 fields still render unchanged.
    assert rendered["precipitates_main"] is True
    assert rendered["annotation"] == "staged reveal"


def test_sketch04_empty_step_kind_renders_as_empty_string():
    """A pre-sketch-03 step (step_kind="") still renders the field,
    as an empty string. The probe sees what was authored — if the
    encoding didn't declare, the probe reads the absence."""
    from story_engine.core.aristotelian import ArAnagnorisisStep
    from story_engine.core.aristotelian_reader_model_client import (
        _ar_anagnorisis_step_to_dict,
    )
    step = ArAnagnorisisStep(
        id="arstep_legacy",
        event_id="E_reveal",
        character_ref_id="c_hero",
        precipitates_main=False,
        annotation="legacy step",
    )
    rendered = _ar_anagnorisis_step_to_dict(step)
    assert rendered["step_kind"] == ""


def test_sketch04_anagnorisis_character_ref_id_renders_in_mythos_dict():
    """APA4-2: _ar_mythos_to_dict includes anagnorisis_character_ref_id
    so the probe reads which character the main anagnorisis belongs
    to. Required for the probe to evaluate staging-step closure."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_MYTHOS,
    )
    from story_engine.core.aristotelian_reader_model_client import (
        _ar_mythos_to_dict,
    )
    rendered = _ar_mythos_to_dict(AR_HAMLET_MYTHOS)
    assert rendered["anagnorisis_character_ref_id"] == "ar_hamlet"


def test_sketch04_anagnorisis_character_ref_id_none_renders_none():
    """Pre-sketch-03 encodings (Oedipus / Rashomon / Macbeth) leave
    the field at None; the rendering carries None through."""
    from story_engine.encodings.oedipus_aristotelian import (
        AR_OEDIPUS_MYTHOS,
    )
    from story_engine.core.aristotelian_reader_model_client import (
        _ar_mythos_to_dict,
    )
    rendered = _ar_mythos_to_dict(AR_OEDIPUS_MYTHOS)
    assert rendered["anagnorisis_character_ref_id"] is None


def test_sketch04_character_arc_relation_renders():
    """APA4-3: _ar_character_arc_relation_to_dict renders all six
    fields (id, kind, character_ref_ids, mythos_id, over_event_ids,
    annotation) for the probe."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_LAERTES_MIRROR,
    )
    from story_engine.core.aristotelian_reader_model_client import (
        _ar_character_arc_relation_to_dict,
    )
    rendered = _ar_character_arc_relation_to_dict(AR_HAMLET_LAERTES_MIRROR)
    assert rendered["kind"] == "ArCharacterArcRelation"
    assert rendered["id"] == "arc_hamlet_laertes_mirror"
    assert rendered["relation_kind"] == "mirror"
    assert rendered["character_ref_ids"] == ["ar_hamlet", "ar_laertes"]
    assert rendered["mythos_id"] == "ar_hamlet"
    # over_event_ids is a full list — just verify it's a list with
    # the expected shape (cardinality > 0, all strings).
    assert isinstance(rendered["over_event_ids"], list)
    assert len(rendered["over_event_ids"]) > 0
    assert all(isinstance(e, str) for e in rendered["over_event_ids"])
    assert isinstance(rendered["annotation"], str)
    assert rendered["annotation"]  # non-empty


def test_sketch04_character_arc_relations_section_omitted_when_empty():
    """_build_character_arc_relations_section returns None on empty
    input; the prompt omits the whole section. Parallels the
    ArMythosRelation / substrate-section pattern."""
    from story_engine.core.aristotelian_reader_model_client import (
        _build_character_arc_relations_section,
    )
    assert _build_character_arc_relations_section(()) is None
    assert _build_character_arc_relations_section([]) is None


def test_sketch04_prompt_includes_character_arc_relations_section():
    """APA4-3 + APA4-4: when character_arc_relations is non-empty,
    build_user_prompt emits a dedicated section with the sketch-03
    A13 heading, and the rendered relations appear in the prompt."""
    from story_engine.encodings.hamlet import FABULA
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_CHARACTER_ARC_RELATIONS, AR_HAMLET_MYTHOS,
    )
    prompt, _ = build_user_prompt(
        mythoi=(AR_HAMLET_MYTHOS,),
        observations=(),
        substrate_events=list(FABULA),
        targets_to_review=_eligible_targets(
            (AR_HAMLET_MYTHOS,),
            character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
        ),
        observations_to_comment_on=[],
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    assert "ArCharacterArcRelation records (sketch-03 A13)" in prompt
    assert "arc_hamlet_laertes_mirror" in prompt
    assert "arc_hamlet_claudius_foil" in prompt
    # The canonical-kind vocabulary appears in the preamble.
    assert "mirror" in prompt
    assert "foil" in prompt


def test_sketch04_prompt_omits_arc_relations_section_when_empty():
    """Oedipus authors no ArCharacterArcRelation — the section is
    absent entirely (heading does not appear). Pre-sketch-04 call
    sites stay byte-identical through this path."""
    from story_engine.encodings.oedipus_aristotelian import (
        AR_OEDIPUS_MYTHOS,
    )
    prompt, _ = build_user_prompt(
        mythoi=(AR_OEDIPUS_MYTHOS,),
        observations=(),
        substrate_events=[],
        targets_to_review=_eligible_targets((AR_OEDIPUS_MYTHOS,)),
        observations_to_comment_on=[],
    )
    assert "ArCharacterArcRelation records" not in prompt


def test_sketch04_eligible_targets_includes_staging_step_annotations():
    """APA4-3: Hamlet's three-step anagnorisis_chain carries three
    non-empty annotations — all three join the eligible set as
    ArAnagnorisisStep.annotation triples."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_CHARACTER_ARC_RELATIONS, AR_HAMLET_MYTHOS,
    )
    targets = _eligible_targets(
        (AR_HAMLET_MYTHOS,),
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    step_triples = [
        t for t in targets if t[0] == TARGET_AR_ANAGNORISIS_STEP
    ]
    assert len(step_triples) == 3, (
        f"expected 3 ArAnagnorisisStep triples (Ghost-claim, "
        f"Mousetrap, Claudius-prays); got {step_triples}"
    )
    step_ids = sorted(t[1] for t in step_triples)
    assert step_ids == [
        "arstep_claudius_prays",
        "arstep_hamlet_ghost_claim",
        "arstep_hamlet_mousetrap",
    ]
    assert all(t[2] == FIELD_ANNOTATION for t in step_triples)


def test_sketch04_eligible_targets_includes_arc_relation_annotations():
    """APA4-3: Hamlet's two ArCharacterArcRelation records join the
    eligible set as ArCharacterArcRelation.annotation triples when
    character_arc_relations is threaded through."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_CHARACTER_ARC_RELATIONS, AR_HAMLET_MYTHOS,
    )
    targets = _eligible_targets(
        (AR_HAMLET_MYTHOS,),
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    arc_triples = [
        t for t in targets if t[0] == TARGET_AR_CHARACTER_ARC_RELATION
    ]
    assert len(arc_triples) == 2
    arc_ids = sorted(t[1] for t in arc_triples)
    assert arc_ids == [
        "arc_hamlet_claudius_foil",
        "arc_hamlet_laertes_mirror",
    ]
    assert all(t[2] == FIELD_ANNOTATION for t in arc_triples)


def test_sketch04_hamlet_eligible_targets_full_count():
    """Hamlet Session 6: 1 mythos action_summary + 3 phase
    annotations + 3 hamartia_texts + 3 staging/parallel step
    annotations + 2 arc-relation annotations = 12 reviewable
    prose fields. (The sketch-04 draft named 11; Hamlet authors
    3 chain steps rather than 2 staging — the mirror of Claudius's
    prayer step adds one more reviewable annotation.)"""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_CHARACTER_ARC_RELATIONS, AR_HAMLET_MYTHOS,
    )
    targets = _eligible_targets(
        (AR_HAMLET_MYTHOS,),
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    assert len(targets) == 12, (
        f"expected 12 eligible targets on Hamlet (sketch-04); "
        f"got {len(targets)}"
    )


def test_sketch04_records_by_kind_id_indexes_steps_and_arc_relations():
    """APA4-4: _records_by_kind_id indexes staging steps (from
    mythos.anagnorisis_chain) and arc relations (from the kwarg),
    so scope validation resolves target_ids to rendered records."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_CHARACTER_ARC_RELATIONS, AR_HAMLET_MYTHOS,
    )
    index = _records_by_kind_id(
        (AR_HAMLET_MYTHOS,),
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    assert (
        TARGET_AR_ANAGNORISIS_STEP,
        "arstep_hamlet_ghost_claim",
    ) in index
    assert (
        TARGET_AR_CHARACTER_ARC_RELATION,
        "arc_hamlet_laertes_mirror",
    ) in index


def test_sketch04_annotation_review_on_arc_relation_accepted():
    """Scope validation accepts a review on an
    ArCharacterArcRelation:annotation triple when the relation is
    in the kwarg and in targets_to_review."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_CHARACTER_ARC_RELATIONS, AR_HAMLET_MYTHOS,
    )
    records_index = _records_by_kind_id(
        (AR_HAMLET_MYTHOS,),
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    targets = _eligible_targets(
        (AR_HAMLET_MYTHOS,),
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    raw = AristotelianAnnotationReview(
        target_kind=TARGET_AR_CHARACTER_ARC_RELATION,
        target_id="arc_hamlet_laertes_mirror",
        field=FIELD_ANNOTATION,
        verdict="approved",
        rationale="mirror-relation prose cites the play's own line",
    )
    reason = _classify_annotation_review(raw, records_index, targets)
    assert reason is None, f"expected accepted; got drop: {reason}"


def test_sketch04_annotation_review_on_staging_step_accepted():
    """Scope validation accepts a review on an
    ArAnagnorisisStep:annotation triple for a chain step with
    authored prose."""
    from story_engine.encodings.hamlet_aristotelian import (
        AR_HAMLET_CHARACTER_ARC_RELATIONS, AR_HAMLET_MYTHOS,
    )
    records_index = _records_by_kind_id(
        (AR_HAMLET_MYTHOS,),
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    targets = _eligible_targets(
        (AR_HAMLET_MYTHOS,),
        character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
    )
    raw = AristotelianAnnotationReview(
        target_kind=TARGET_AR_ANAGNORISIS_STEP,
        target_id="arstep_hamlet_ghost_claim",
        field=FIELD_ANNOTATION,
        verdict="needs-work",
        rationale="staging-step prose overstates the epistemic claim",
    )
    reason = _classify_annotation_review(raw, records_index, targets)
    assert reason is None, f"expected accepted; got drop: {reason}"


def test_sketch04_system_prompt_carries_sketch03_paragraph():
    """APA4-5: SYSTEM_PROMPT names the sketch-03 extensions so the
    LLM knows what A13 / A14 mean when it encounters them in the
    records section."""
    from story_engine.core.aristotelian_reader_model_client import (
        SYSTEM_PROMPT,
    )
    assert "sketch-03" in SYSTEM_PROMPT
    assert "ArCharacterArcRelation" in SYSTEM_PROMPT
    assert "step_kind" in SYSTEM_PROMPT
    assert "staging" in SYSTEM_PROMPT
    assert "anagnorisis_character_ref_id" in SYSTEM_PROMPT


def test_sketch04_pre_sketch03_encodings_prompt_byte_identical():
    """Oedipus / Rashomon / Macbeth demos use default-empty
    character_arc_relations. The prompts for those encodings must
    stay byte-identical to pre-sketch-04 behavior, modulo the
    SYSTEM_PROMPT + records-section-preamble updates (which apply
    universally). This test covers the USER prompt for Rashomon —
    the heaviest pre-sketch-03 case — with and without the sketch-04
    kwargs explicitly empty."""
    from story_engine.encodings.rashomon_aristotelian import (
        AR_RASHOMON_MYTHOI, AR_RASHOMON_RELATIONS,
    )
    # Default (no sketch-04 kwarg)
    prompt_default, _ = build_user_prompt(
        mythoi=AR_RASHOMON_MYTHOI,
        observations=(),
        substrate_events=[],
        targets_to_review=_eligible_targets(AR_RASHOMON_MYTHOI),
        observations_to_comment_on=[],
        relations=AR_RASHOMON_RELATIONS,
    )
    # Explicit-empty kwarg
    prompt_explicit, _ = build_user_prompt(
        mythoi=AR_RASHOMON_MYTHOI,
        observations=(),
        substrate_events=[],
        targets_to_review=_eligible_targets(AR_RASHOMON_MYTHOI),
        observations_to_comment_on=[],
        relations=AR_RASHOMON_RELATIONS,
        character_arc_relations=(),
    )
    assert prompt_default == prompt_explicit
    # And neither emits the sketch-03 A13 section heading.
    assert "ArCharacterArcRelation records" not in prompt_default


# ============================================================================
# Test runner
# ============================================================================


def main() -> int:
    tests = [
        (name, fn) for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    ]
    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
        except Exception:
            failed += 1
            print(f"FAIL  {name}")
            traceback.print_exc()
        else:
            passed += 1
            print(f"ok    {name}")
    print()
    print(f"{passed} passed, {failed} failed, {passed + failed} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
