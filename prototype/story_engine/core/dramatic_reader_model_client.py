"""
dramatic_reader_model_client.py — live LLM probe at the cross-boundary
surface (Dramatic + Lowerings + verifier output).

Companion to reader_model_client.py. Where that module probes the
substrate-side ReaderView (events + descriptions on a single dialect),
this one probes the *cross-boundary surface*: the Dramatic dialect's
records, the Lowerings binding them to substrate, and the verifier's
output on those records. The LLM's role is the same — interpretive
peer per reader-model-sketch-01 — but the surfaces are different.

Two output kinds:

1. **AnnotationReview** (substrate-native, from lowering.py). The LLM
   reads a Lowering's annotation against the records on both sides
   and emits a verdict on whether the annotation is faithful. Same
   shape as a human-authored AnnotationReview — the substrate doesn't
   distinguish reviewer source beyond `reviewer_id`.

2. **VerifierCommentary** (defined in verification.py). The LLM reads
   a VerificationReview produced by the verifier and emits an
   assessment on whether the verdict is sensible. This is the
   "review of a review" surface — a third-party read on the
   verifier's verdict. The author walks these and decides whether
   to extend the check function, accept the dissent, or note and
   move on.

Architectural placement: this is **tooling**, not substrate or
verifier. The verifier produces output; the Lowerings carry
annotations; this module assembles them into a probe surface and
calls Claude. The LLM's response lands in the proposal queue (same
shape contract as the substrate-side probe).

Defaults follow reader-model-sketch-01 + claude-api skill (same
choices as the substrate-side client):

- model: claude-opus-4-6
- thinking: {"type": "adaptive"}
- output_config.effort: "high"
- max_tokens: 16_000
- cache_control: {"type": "ephemeral"} on the system block
- typed I/O via `client.messages.parse()` with Pydantic schemas

Requires: `pip install -r prototype/requirements.txt`.
API key: reads `ANTHROPIC_API_KEY` from the environment.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Literal, Optional

from pydantic import BaseModel, Field

try:
    import anthropic
except ImportError as exc:
    raise ImportError(
        "The dramatic-reader-model client requires the anthropic SDK. "
        "Install dependencies via "
        "`pip install -r prototype/requirements.txt`."
    ) from exc

from story_engine.core.lowering import (
    AnnotationReview,
    CrossDialectRef,
    Lowering,
    LoweringStatus,
    VERDICT_APPROVED, VERDICT_NEEDS_WORK,
    VERDICT_REJECTED, VERDICT_NOTED,
)
from story_engine.core.verification import (
    StructuralAdvisory,
    VerificationReview,
    VerifierCommentary,
    ASSESSMENT_ENDORSES, ASSESSMENT_QUALIFIES,
    ASSESSMENT_DISSENTS, ASSESSMENT_NOTED,
)


# ============================================================================
# Pydantic schemas — what the LLM returns (typed I/O per R1)
# ============================================================================


# Annotation-review verdicts mirror lowering.VERDICT_*. Constraining
# the Literal at parse time means a verdict outside this set fails
# validation rather than landing as a malformed record.
AnnotationVerdict = Literal[
    "approved", "needs-work", "rejected", "noted",
]

# Verifier-commentary assessments mirror verification.ASSESSMENT_*.
CommentaryAssessment = Literal[
    "endorses", "qualifies", "dissents", "noted",
]


class DramaticReaderAnnotationReview(BaseModel):
    """One LLM verdict on a single Lowering's annotation."""
    lowering_id: str = Field(
        description="id of the Lowering whose annotation is being reviewed"
    )
    verdict: AnnotationVerdict = Field(
        description="the reviewer's verdict on the annotation"
    )
    rationale: str = Field(
        description=(
            "1-3 sentences explaining the verdict, grounded in the "
            "upper record, lower record(s), and (where helpful) the "
            "substrate context provided"
        )
    )


class DramaticReaderVerifierCommentary(BaseModel):
    """One LLM read on a single VerificationReview."""
    target_review_id: str = Field(
        description=(
            "synthetic id of the verifier review being commented on; "
            "matches one of the ids shown in the prompt's verifier "
            "output section"
        )
    )
    assessment: CommentaryAssessment = Field(
        description=(
            "endorses (verdict well-grounded), qualifies (verdict "
            "stands but with a clarification), dissents (commenter "
            "disagrees, with grounded counter-argument), or noted "
            "(read but no position)"
        )
    )
    rationale: str = Field(
        description=(
            "2-4 sentences explaining the assessment. Cite specific "
            "records or signatures from the prompt content. A dissent "
            "must name what the verifier's check missed or got wrong; "
            "a qualification must name what's being added to the "
            "verdict's reading."
        )
    )
    suggested_signature: Optional[str] = Field(
        default=None,
        description=(
            "Optional. If the commentary identifies a concrete "
            "signature the verifier's check might add, propose it as "
            "free-form prose (e.g., 'consider also that the owner "
            "Entity appears as the told_by listener of utterance "
            "events advancing the throughline'). Not actionable code "
            "— this is inspiration for the author who maintains the "
            "check. Omit unless the suggestion is concrete."
        ),
    )


class DramaticReaderOutput(BaseModel):
    """The full structured response. Empty lists are legal — an LLM
    with nothing to propose returns empty collections, not prose."""
    annotation_reviews: list[DramaticReaderAnnotationReview] = (
        Field(default_factory=list)
    )
    verifier_commentaries: list[DramaticReaderVerifierCommentary] = (
        Field(default_factory=list)
    )


# ============================================================================
# Result types — translated into substrate/verifier-native records
# ============================================================================


@dataclass(frozen=True)
class DroppedOutput:
    """A raw LLM output record that failed scope or structural
    validation at translation time. `reason` is a short
    human-readable explanation; `raw` is the Pydantic record so a
    reviewing author can see exactly what was dropped and why.

    R5 enforcement: the prompt tells the LLM what's in scope, but
    we verify in code. An LLM that reviews a Lowering outside
    `lowerings_to_review`, or comments on a verifier review id that
    doesn't resolve, lands here — never in the accepted lists.
    """
    reason: str
    raw: object  # one of the Pydantic schemas


@dataclass
class DramaticReaderModelResult:
    """What invoke_dramatic_reader_model returns.

    `annotation_review_candidates` pairs each translated
    AnnotationReview with the lowering_id it targets — same
    pair-as-authoritative-artifact pattern as the substrate-side
    client. Zipping parallel lists is unsafe when any raw record
    was dropped at the validation gate.

    `verifier_commentaries` is a flat list of VerifierCommentary
    records; each carries `target_review` directly (the resolved
    VerificationReview) so the consumer doesn't need to re-resolve
    by id.
    """
    annotation_review_candidates: list  # list[tuple[str, AnnotationReview]]
    verifier_commentaries: list         # list[VerifierCommentary]
    dropped: list                       # list[DroppedOutput]
    raw_output: DramaticReaderOutput


# ============================================================================
# Prompt construction
# ============================================================================


SYSTEM_PROMPT = """You are a reader-model — an interpretive peer to a \
structured story-telling engine. Your role is specified by \
reader-model-sketch-01 in the project's design/ directory.

This invocation puts you on the **cross-boundary surface**: a Dramatic \
upper dialect (Throughlines, Scenes, Characters, Argument), the \
Lowerings that bind those records to a substrate (events + entities), \
and the *verifier's* output on those records. Your job is to read \
critically along that boundary.

The Dramatic dialect admits **Templates** — specific theory-shaped \
extensions that ship additional record types. When the prompt \
includes a *Template records* section (e.g., under the \
`dramatica-complete` Template: DomainAssignments, DynamicStoryPoints, \
Signposts, ThematicPicks, CharacterElementAssignments, Story_goal / \
Story_consequence), those records are part of the upper dialect — \
treat them with the same care as Throughlines and Scenes. The \
verifier may target Template records directly (a VerificationReview \
whose `target_record` is `dramatica-complete:DSP_limit` is judging \
the DynamicStoryPoint declaration against substrate evidence).

Your contract:

R1. Typed I/O only. You produce structured output matching the \
provided schema. Prose lives inside the `rationale` field; never \
outside it.

R2. The surface distinguishes three tiers structurally. Upper-dialect \
records (Argument, Throughlines, Scenes, Characters) are interpretive \
*structural assertions* about a story. Lowerings bind upper to lower \
with an `annotation` that justifies the binding. Verifier output is \
the engine's automated read on whether the bindings + claims hold. \
These are separate surfaces with different semantics — never treat one \
as a substitute for another.

R3. You propose; the author decides. Your annotation reviews are \
recommendations — the author walks them and decides whether to attach \
them to the Lowering's annotation. Your verifier commentaries are \
candidate readings of the verifier's verdicts — the author walks them \
and decides whether to extend the check function, accept the dissent, \
or note and move on. You do not assert anything into substrate or \
verifier state directly.

R4. Same record types a human reviewer would produce — just with \
`reviewer_id` / `commenter_id` = "llm:<model>". The substrate doesn't \
distinguish LLM and human reviews beyond the identifier.

## The two output kinds

### Annotation reviews

For each Lowering you are asked to review, produce one \
DramaticReaderAnnotationReview:

- `lowering_id`: the Lowering being reviewed.
- `verdict`: one of:
  - "approved" — the annotation faithfully justifies the binding. \
The upper record's claim *does* land in the lower record(s).
  - "needs-work" — the annotation has a specific problem: an \
overstatement of what the lower side carries, an unclear claim, an \
unflagged tension between upper and lower, missing context the lower \
side reveals.
  - "rejected" — the annotation should not stand. The binding is \
asserting something the lower side does not realize, or the \
annotation actively misreads one of the sides.
  - "noted" — read but no position taken (out of your competence; \
missing context).
- `rationale`: 1-3 sentences explaining the verdict. Specific, \
grounded in the upper record, lower record(s), and any substrate \
context provided.

### Verifier commentaries

For each verifier review you are asked to comment on, produce one \
DramaticReaderVerifierCommentary:

- `target_review_id`: the synthetic id of the verifier review (the \
prompt assigns these — `vr_0`, `vr_1`, …).
- `assessment`: one of:
  - "endorses" — the verifier's verdict is well-grounded. Nothing to \
add.
  - "qualifies" — the verdict stands, but a specific clarification, \
missed nuance, or alternate reading is worth recording alongside it.
  - "dissents" — you disagree with the verdict. State a specific \
counter-argument grounded in the records (not a general "I see it \
differently"). A dissent that doesn't name what the check missed or \
got wrong belongs as "noted" or "qualifies" instead.
  - "noted" — read but no position taken.
- `rationale`: 2-4 sentences explaining the assessment. Cite specific \
records or signatures.
- `suggested_signature` (optional): if the commentary identifies a \
concrete signature the check might add, propose it as free-form prose \
(e.g., "consider also checking that the owner Entity appears as the \
`told_by` listener of utterance events"). Not actionable code; just \
inspiration for the author who maintains the check. Omit unless the \
suggestion is concrete and grounded.

## Scope discipline

You see exactly what the prompt contains. Nothing exists, for your \
purposes, outside it.

- Never invent records. If the prompt contains no evidence for a \
claim, do not make that claim.
- Verifier reviews carry their own `comment` field with rationale \
from the check function. Read it before commenting — a dissent that \
ignores what the check explicitly stated is a weak dissent.
- A verdict of "partial-match" with strength=0.92 is not a failure \
mode by default; the check function explicitly chose that threshold. \
Endorsement of a partial-match is a perfectly valid assessment.
- A Lowering with `status=PENDING` carries no lower records. Reviews \
of pending annotations should focus on whether the annotation \
correctly identifies what would need to exist for the binding to flip \
to ACTIVE — not on the absence of lower records itself.
- Do not attempt to author code, propose new records the prompt did \
not ask for, or speak about records outside the supplied scope. If \
you cannot make a good-faith judgment, "noted" is correct. \
"needs-work" / "dissents" are for specific findings, not general \
uncertainty.
"""


# ============================================================================
# Helpers — render records as JSON-serializable dicts for the prompt
# ============================================================================


def _ref_to_str(ref: CrossDialectRef) -> str:
    """Render a CrossDialectRef as 'dialect:record_id' for prompts."""
    return f"{ref.dialect}:{ref.record_id}"


def _argument_to_dict(arg) -> dict:
    return {
        "kind": "Argument",
        "id": arg.id,
        "premise": arg.premise,
        "counter_premise": arg.counter_premise,
        "resolution_direction": arg.resolution_direction.value,
        "domain": arg.domain,
        "parent_argument_id": arg.parent_argument_id,
    }


def _throughline_to_dict(t) -> dict:
    return {
        "kind": "Throughline",
        "id": t.id,
        "role_label": t.role_label,
        "owners": list(t.owners),
        "subject": t.subject,
        "counterpoint_throughline_ids": list(t.counterpoint_throughline_ids),
        "argument_contributions": [
            {"argument_id": ac.argument_id, "side": ac.side.value}
            for ac in t.argument_contributions
        ],
        "stakes_id": t.stakes_id,
    }


def _character_to_dict(c) -> dict:
    return {
        "kind": "Character",
        "id": c.id,
        "name": c.name,
        "function_labels": list(c.function_labels),
    }


def _scene_to_dict(s) -> dict:
    return {
        "kind": "Scene",
        "id": s.id,
        "title": s.title,
        "narrative_position": s.narrative_position,
        "advances": [
            {"throughline_id": a.throughline_id, "beat_id": a.beat_id}
            for a in s.advances
        ],
        "conflict_shape": s.conflict_shape,
        "result": s.result,
    }


def _beat_to_dict(b) -> dict:
    return {
        "kind": "Beat",
        "id": b.id,
        "throughline_id": b.throughline_id,
        "beat_position": b.beat_position,
        "beat_type": b.beat_type,
        "description_of_change": b.description_of_change,
    }


def _stakes_to_dict(s) -> dict:
    return {
        "kind": "Stakes",
        "id": s.id,
        "owner": {"kind": s.owner.kind.value, "id": s.owner.id},
        "at_risk": s.at_risk,
        "to_gain": s.to_gain,
        "external_manifestation": s.external_manifestation,
    }


def _domain_assignment_to_dict(da) -> dict:
    return {
        "kind": "DomainAssignment",
        "id": da.id,
        "throughline_id": da.throughline_id,
        "domain": da.domain.value if hasattr(da.domain, "value") else da.domain,
    }


def _dynamic_story_point_to_dict(dsp) -> dict:
    return {
        "kind": "DynamicStoryPoint",
        "id": dsp.id,
        "axis": dsp.axis.value if hasattr(dsp.axis, "value") else dsp.axis,
        "choice": dsp.choice,
        "story_id": dsp.story_id,
    }


def _signpost_to_dict(sp) -> dict:
    return {
        "kind": "Signpost",
        "id": sp.id,
        "throughline_id": sp.throughline_id,
        "signpost_position": sp.signpost_position,
        "signpost_element": sp.signpost_element,
    }


def _quad_pick_to_dict(qp) -> dict:
    return {
        "id": qp.id,
        "quad_id": qp.quad_id,
        "chosen_position": (
            qp.chosen_position.value
            if hasattr(qp.chosen_position, "value") else qp.chosen_position
        ),
        "attached_to_kind": qp.attached_to_kind,
        "attached_to_id": qp.attached_to_id,
    }


def _thematic_picks_to_dict(tp) -> dict:
    return {
        "kind": "ThematicPicks",
        "throughline_id": tp.throughline_id,
        "concern_pick": _quad_pick_to_dict(tp.concern_pick),
        "issue_pick": _quad_pick_to_dict(tp.issue_pick),
        "problem_pick": _quad_pick_to_dict(tp.problem_pick),
        "solution_override": tp.solution_override,
        "symptom_override": tp.symptom_override,
        "response_override": tp.response_override,
    }


def _element_assignment_to_dict(ea, dimension: str) -> dict:
    """Render one {Character,Methodology,Evaluation,Purpose}ElementAssignment
    as a dict. `dimension` is the authorial dimension string (Motivation /
    Methodology / Evaluation / Purpose) the element lives in — the element
    label alone doesn't disambiguate, since the four dimensions share some
    surface vocabulary."""
    return {
        "kind": "ElementAssignment",
        "dimension": dimension,
        "id": ea.id,
        "character_id": ea.character_id,
        "element": (
            ea.element.value if hasattr(ea.element, "value") else ea.element
        ),
    }


def _lowering_to_dict(lw: Lowering) -> dict:
    """Render a Lowering with annotation, status, position_range,
    and resolved upper/lower references. The annotation is the
    review target; surface it prominently so the LLM grades the
    annotation against the binding it sits on top of."""
    pr = lw.position_range
    return {
        "id": lw.id,
        "status": lw.status.value,
        "upper_record": _ref_to_str(lw.upper_record),
        "lower_records": [_ref_to_str(lr) for lr in lw.lower_records],
        "position_range": (
            {"coord": pr.coord, "min_value": pr.min_value,
             "max_value": pr.max_value}
            if pr is not None else None
        ),
        "annotation": {
            "text": lw.annotation.text,
            "attention": lw.annotation.attention,
            "authored_by": lw.annotation.authored_by,
            "review_count": len(lw.annotation.review_states),
        },
        "τ_a": lw.τ_a,
        "anchor_τ_a": lw.anchor_τ_a,
        "metadata": dict(lw.metadata),
    }


def _verification_review_to_dict(
    vr: VerificationReview, synthetic_id: str,
) -> dict:
    """Render a VerificationReview with a synthetic id the LLM uses
    to reference it in commentaries. The reviewer's own comment is
    surfaced verbatim — a useful commentary engages with what the
    check explicitly said, not just the verdict label."""
    return {
        "review_id": synthetic_id,
        "kind": "VerificationReview",
        "reviewer_id": vr.reviewer_id,
        "target_record": _ref_to_str(vr.target_record),
        "verdict": vr.verdict,
        "match_strength": vr.match_strength,
        "anchor_τ_a": vr.anchor_τ_a,
        "comment": vr.comment,
    }


def _structural_advisory_to_dict(adv: StructuralAdvisory) -> dict:
    """Render a StructuralAdvisory. These are not individually
    commentable in this iteration — they appear as context only.
    A future iteration could add an AdvisoryCommentary surface."""
    return {
        "kind": "StructuralAdvisory",
        "advisor_id": adv.advisor_id,
        "severity": adv.severity,
        "scope": [_ref_to_str(r) for r in adv.scope],
        "comment": adv.comment,
        "match_strength": adv.match_strength,
    }


def _substrate_event_summary(event) -> dict:
    """Lightweight substrate-event summary for prompt context.
    Uses fewer fields than reader_model_client._event_to_dict — the
    Dramatic-side LLM doesn't need full effect lists, just enough to
    judge whether a Lowering's annotation matches what the lower
    record(s) carry."""
    return {
        "id": event.id,
        "type": event.type,
        "τ_s": event.τ_s,
        "τ_a": event.τ_a,
        "participants": event.participants,
        "effect_count": len(event.effects),
    }


def _substrate_entity_summary(entity) -> dict:
    return {
        "id": entity.id,
        "kind": entity.kind,
    }


def _build_dramatic_section(
    arguments: tuple, throughlines: tuple, characters: tuple,
    scenes: tuple, beats: tuple, stakes: tuple,
) -> str:
    payload = {
        "arguments": [_argument_to_dict(a) for a in arguments],
        "throughlines": [_throughline_to_dict(t) for t in throughlines],
        "characters": [_character_to_dict(c) for c in characters],
        "scenes": [_scene_to_dict(s) for s in scenes],
        "beats": [_beat_to_dict(b) for b in beats],
        "stakes": [_stakes_to_dict(s) for s in stakes],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _build_template_section(
    domain_assignments: tuple,
    dynamic_story_points: tuple,
    signposts: tuple,
    thematic_picks: tuple,
    character_element_assignments: tuple,
    methodology_element_assignments: tuple,
    evaluation_element_assignments: tuple,
    purpose_element_assignments: tuple,
    story_goal: Optional[str],
    story_consequence: Optional[str],
) -> Optional[str]:
    """Render the Template-records section. Returns None when every
    argument is empty — callers using the probe on a Dramatic-only
    surface should see no Template section at all, preserving the
    Dramatic-only prompt shape.

    The Story-level fields (goal / consequence) appear as dict entries
    keyed by the record_id the verifier uses to target them
    (`Story_goal` / `Story_consequence`), matching the
    `dramatica-complete:Story_goal` pattern a VerificationReview
    target_record carries."""
    if not any((
        domain_assignments, dynamic_story_points, signposts,
        thematic_picks,
        character_element_assignments, methodology_element_assignments,
        evaluation_element_assignments, purpose_element_assignments,
        story_goal, story_consequence,
    )):
        return None
    payload: dict = {}
    if domain_assignments:
        payload["domain_assignments"] = [
            _domain_assignment_to_dict(da) for da in domain_assignments
        ]
    if dynamic_story_points:
        payload["dynamic_story_points"] = [
            _dynamic_story_point_to_dict(dsp) for dsp in dynamic_story_points
        ]
    if signposts:
        payload["signposts"] = [
            _signpost_to_dict(sp) for sp in signposts
        ]
    if thematic_picks:
        payload["thematic_picks"] = [
            _thematic_picks_to_dict(tp) for tp in thematic_picks
        ]
    if character_element_assignments:
        payload["character_element_assignments_motivation"] = [
            _element_assignment_to_dict(ea, "Motivation")
            for ea in character_element_assignments
        ]
    if methodology_element_assignments:
        payload["character_element_assignments_methodology"] = [
            _element_assignment_to_dict(ea, "Methodology")
            for ea in methodology_element_assignments
        ]
    if evaluation_element_assignments:
        payload["character_element_assignments_evaluation"] = [
            _element_assignment_to_dict(ea, "Evaluation")
            for ea in evaluation_element_assignments
        ]
    if purpose_element_assignments:
        payload["character_element_assignments_purpose"] = [
            _element_assignment_to_dict(ea, "Purpose")
            for ea in purpose_element_assignments
        ]
    story_level: dict = {}
    if story_goal:
        story_level["Story_goal"] = story_goal
    if story_consequence:
        story_level["Story_consequence"] = story_consequence
    if story_level:
        payload["story_level_fields"] = story_level
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _build_lowerings_section(lowerings: tuple) -> str:
    return json.dumps(
        [_lowering_to_dict(lw) for lw in lowerings],
        indent=2, ensure_ascii=False,
    )


def _build_verifier_section(
    verifier_results: tuple,
) -> tuple:
    """Render verifier output and return (rendered_json, id_map).
    `id_map` maps synthetic ids ('vr_0', 'vr_1', ...) → the original
    VerificationReview objects, for translation back at result time.
    StructuralAdvisories appear in the rendered output but get no id
    (they are context, not commentable in this iteration)."""
    id_map: dict = {}
    rendered: list = []
    review_index = 0
    for r in verifier_results:
        if isinstance(r, VerificationReview):
            sid = f"vr_{review_index}"
            review_index += 1
            id_map[sid] = r
            rendered.append(_verification_review_to_dict(r, sid))
        elif isinstance(r, StructuralAdvisory):
            rendered.append(_structural_advisory_to_dict(r))
        else:
            # Unknown shape — render its repr so the LLM can at least
            # see something. Shouldn't happen with current verifier
            # primitives, but the union may grow.
            rendered.append({"kind": "Unknown", "repr": repr(r)})
    return json.dumps(rendered, indent=2, ensure_ascii=False), id_map


def _build_substrate_section(
    substrate_events: list, substrate_entities: list,
) -> Optional[str]:
    """Optional substrate context — empty section if both lists are
    empty. The LLM is told that this section is *for grounding
    Lowering annotations against actual lower-side content*."""
    if not substrate_events and not substrate_entities:
        return None
    payload = {
        "events": [_substrate_event_summary(e) for e in substrate_events],
        "entities": [_substrate_entity_summary(e) for e in substrate_entities],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _build_task_section(
    lowerings_to_review: list[str],
    reviews_to_comment_on: list[str],
) -> str:
    parts: list[str] = ["## Task", ""]
    if lowerings_to_review:
        parts.append("Review the annotations on these Lowerings:")
        parts.extend(f"- {lid}" for lid in lowerings_to_review)
    else:
        parts.append("(No Lowering annotations to review.)")
    parts.append("")
    if reviews_to_comment_on:
        parts.append("Comment on these verifier reviews:")
        parts.extend(f"- {sid}" for sid in reviews_to_comment_on)
    else:
        parts.append("(No verifier reviews to comment on.)")
    return "\n".join(parts)


def build_user_prompt(
    arguments: tuple, throughlines: tuple, characters: tuple,
    scenes: tuple, beats: tuple, stakes: tuple,
    lowerings: tuple,
    verifier_results: tuple,
    substrate_events: list,
    substrate_entities: list,
    lowerings_to_review: list[str],
    reviews_to_comment_on: list[str],
    *,
    domain_assignments: tuple = (),
    dynamic_story_points: tuple = (),
    signposts: tuple = (),
    thematic_picks: tuple = (),
    character_element_assignments: tuple = (),
    methodology_element_assignments: tuple = (),
    evaluation_element_assignments: tuple = (),
    purpose_element_assignments: tuple = (),
    story_goal: Optional[str] = None,
    story_consequence: Optional[str] = None,
) -> tuple:
    """Public helper: assemble the full user message and the
    review-id-map without calling the API. The id_map is needed at
    translation time to resolve the LLM's `target_review_id`s back
    to VerificationReview objects.

    Template-record kwargs are optional. When every Template input is
    empty, no Template section is rendered — the Dramatic-only prompt
    shape is preserved. When any Template input is populated, a
    `Template records (dramatica-complete)` section appears right
    after the Dramatic section, so the LLM can read the Template
    declarations alongside the underlying Dramatic records the
    verifier is judging them against."""
    dramatic_section = _build_dramatic_section(
        arguments, throughlines, characters, scenes, beats, stakes,
    )
    template_section = _build_template_section(
        domain_assignments, dynamic_story_points, signposts,
        thematic_picks,
        character_element_assignments, methodology_element_assignments,
        evaluation_element_assignments, purpose_element_assignments,
        story_goal, story_consequence,
    )
    lowerings_section = _build_lowerings_section(lowerings)
    verifier_section, id_map = _build_verifier_section(verifier_results)
    substrate_section = _build_substrate_section(
        substrate_events, substrate_entities,
    )
    task = _build_task_section(lowerings_to_review, reviews_to_comment_on)

    sections = [
        "# Cross-boundary surface",
        "",
        "## Dramatic records (upper dialect)",
        "",
        dramatic_section,
        "",
    ]
    if template_section is not None:
        sections.extend([
            "## Template records (dramatica-complete)",
            "",
            ("(Template records extend the Dramatic dialect with "
             "theory-specific types. The verifier may target these "
             "directly — a VerificationReview on "
             "`dramatica-complete:DSP_limit` is judging the matching "
             "DynamicStoryPoint declaration, so read these alongside "
             "the Dramatic records when commenting on such reviews.)"),
            "",
            template_section,
            "",
        ])
    sections.extend([
        "## Lowerings (cross-dialect bindings)",
        "",
        lowerings_section,
        "",
        "## Verifier output",
        "",
        ("(Reviews carry synthetic `review_id` values like `vr_0`. "
         "Use those ids when commenting. Advisories have no id and "
         "are context only.)"),
        "",
        verifier_section,
        "",
    ])
    if substrate_section is not None:
        sections.extend([
            "## Substrate context (lower-side records, summarized)",
            "",
            ("(For grounding Lowering annotations against the actual "
             "content of the lower records they bind to. Not exhaustive "
             "— event effects are summarized as counts.)"),
            "",
            substrate_section,
            "",
        ])
    sections.extend(["", task])
    return "\n".join(sections), id_map


# ============================================================================
# Translation: LLM output → substrate/verifier-native records
# ============================================================================


def _classify_annotation_review(
    raw: DramaticReaderAnnotationReview,
    lowerings: tuple,
    lowerings_to_review: list[str],
) -> Optional[str]:
    """Validate one raw annotation review against scope.
    Returns None if accepted, else a reason string."""
    if raw.lowering_id not in lowerings_to_review:
        return (
            f"lowering_id {raw.lowering_id!r} is outside the declared "
            f"lowerings_to_review scope"
        )
    if not any(lw.id == raw.lowering_id for lw in lowerings):
        return (
            f"lowering_id {raw.lowering_id!r} does not resolve to any "
            f"known Lowering"
        )
    return None


def _translate_annotation_review(
    raw: DramaticReaderAnnotationReview,
    lowerings: tuple,
    reviewer_id: str,
    current_τ_a: int,
) -> AnnotationReview:
    """One accepted DramaticReaderAnnotationReview → one
    AnnotationReview record. Caller must have already passed the raw
    through _classify_annotation_review and seen None."""
    lw = next(lw for lw in lowerings if lw.id == raw.lowering_id)
    return AnnotationReview(
        reviewer_id=reviewer_id,
        reviewed_at_τ_a=current_τ_a,
        verdict=raw.verdict,
        anchor_τ_a=lw.τ_a,
        comment=raw.rationale,
    )


def _classify_verifier_commentary(
    raw: DramaticReaderVerifierCommentary,
    id_map: dict,
    reviews_to_comment_on: list[str],
) -> Optional[str]:
    """Validate one raw verifier commentary against scope.
    Returns None if accepted, else a reason string."""
    if raw.target_review_id not in reviews_to_comment_on:
        return (
            f"target_review_id {raw.target_review_id!r} is outside the "
            f"declared reviews_to_comment_on scope"
        )
    if raw.target_review_id not in id_map:
        return (
            f"target_review_id {raw.target_review_id!r} does not "
            f"resolve to any verifier review in this invocation"
        )
    return None


def _translate_verifier_commentary(
    raw: DramaticReaderVerifierCommentary,
    id_map: dict,
    commenter_id: str,
    current_τ_a: int,
) -> VerifierCommentary:
    """One accepted DramaticReaderVerifierCommentary → one
    VerifierCommentary record. Caller must have already passed the
    raw through _classify_verifier_commentary and seen None."""
    target = id_map[raw.target_review_id]
    return VerifierCommentary(
        commenter_id=commenter_id,
        commented_at_τ_a=current_τ_a,
        assessment=raw.assessment,
        target_review=target,
        comment=raw.rationale,
        suggested_signature=raw.suggested_signature,
    )


# ============================================================================
# Entry point
# ============================================================================


def invoke_dramatic_reader_model(
    *,
    arguments: tuple,
    throughlines: tuple,
    characters: tuple,
    scenes: tuple,
    beats: tuple,
    stakes: tuple,
    lowerings: tuple,
    verifier_results: tuple,
    current_τ_a: int,
    substrate_events: Optional[list] = None,
    substrate_entities: Optional[list] = None,
    lowerings_to_review: Optional[list[str]] = None,
    reviews_to_comment_on: Optional[list[str]] = None,
    domain_assignments: tuple = (),
    dynamic_story_points: tuple = (),
    signposts: tuple = (),
    thematic_picks: tuple = (),
    character_element_assignments: tuple = (),
    methodology_element_assignments: tuple = (),
    evaluation_element_assignments: tuple = (),
    purpose_element_assignments: tuple = (),
    story_goal: Optional[str] = None,
    story_consequence: Optional[str] = None,
    model: str = "claude-opus-4-6",
    reviewer_id: Optional[str] = None,
    effort: str = "high",
    max_tokens: int = 16_000,
    dry_run: bool = False,
    client: Optional["anthropic.Anthropic"] = None,
) -> DramaticReaderModelResult:
    """Invoke the cross-boundary reader-model probe.

    Args:
        arguments / throughlines / characters / scenes / beats /
            stakes: the Dramatic records the probe should see. Pass
            the encoding's full tuple for each (e.g.,
            macbeth_dramatic.ARGUMENTS, .THROUGHLINES, etc.).
        lowerings: the Lowering records the probe should see.
        verifier_results: the verifier's output tuple — a mix of
            VerificationReview and StructuralAdvisory. Each
            VerificationReview gets a synthetic id ('vr_0', 'vr_1',
            ...) the LLM uses to reference it.
        current_τ_a: τ_a stamped on all produced records. Caller's
            choice; typical: "next τ_a after the last commit".
        substrate_events / substrate_entities: optional. When
            provided, surface as a substrate-context section so the
            LLM can ground its annotation reviews against actual
            lower-side content. Default: None (no substrate section
            rendered).
        lowerings_to_review: ids of Lowerings whose annotations the
            LLM should review. Default: every Lowering id in the
            input. Pass `[]` to skip annotation reviews.
        reviews_to_comment_on: synthetic ids of verifier reviews the
            LLM should comment on. Default: every VerificationReview
            in `verifier_results` (assigned ids in input order). Pass
            `[]` to skip commentary.
        domain_assignments / dynamic_story_points / signposts /
            thematic_picks / character_element_assignments /
            methodology_element_assignments /
            evaluation_element_assignments /
            purpose_element_assignments: optional Template records
            under a dialect Template (e.g., `dramatica-complete`).
            When any are provided, the prompt renders a Template-
            records section so the LLM can read them alongside the
            base Dramatic records. Each defaults to `()` — the
            Dramatic-only caller passes nothing and gets the
            original prompt shape.
        story_goal / story_consequence: optional Story-level Template
            strings. Surfaced as `Story_goal` / `Story_consequence`
            to match the record_id convention the verifier uses when
            targeting them.
        model / reviewer_id / effort / max_tokens / dry_run / client:
            standard knobs, parallel to invoke_reader_model.

    Returns:
        DramaticReaderModelResult containing:
          - annotation_review_candidates: list[tuple[str,
            AnnotationReview]] — each tuple is (lowering_id, review).
            The author walks these and decides whether to attach to
            the Lowering's annotation.
          - verifier_commentaries: list[VerifierCommentary] — each
            carries `target_review` directly. The author walks these
            and decides whether to extend the check, accept the
            dissent, or note and move on.
          - dropped: list[DroppedOutput] — raw outputs that failed
            scope validation (audit + debug).
          - raw_output: pre-translation DramaticReaderOutput.
    """
    if reviewer_id is None:
        reviewer_id = f"llm:{model}"
    if substrate_events is None:
        substrate_events = []
    if substrate_entities is None:
        substrate_entities = []
    if lowerings_to_review is None:
        lowerings_to_review = [lw.id for lw in lowerings]
    if reviews_to_comment_on is None:
        reviews_to_comment_on = _extract_review_ids(verifier_results)

    # Build prompt + synthetic-id map. The id_map is needed at
    # translation time to resolve the LLM's `target_review_id`s back
    # to VerificationReview objects.
    user_prompt, id_map = build_user_prompt(
        arguments, throughlines, characters, scenes, beats, stakes,
        lowerings, verifier_results,
        substrate_events, substrate_entities,
        lowerings_to_review, reviews_to_comment_on,
        domain_assignments=domain_assignments,
        dynamic_story_points=dynamic_story_points,
        signposts=signposts,
        thematic_picks=thematic_picks,
        character_element_assignments=character_element_assignments,
        methodology_element_assignments=methodology_element_assignments,
        evaluation_element_assignments=evaluation_element_assignments,
        purpose_element_assignments=purpose_element_assignments,
        story_goal=story_goal,
        story_consequence=story_consequence,
    )

    if dry_run:
        print("=" * 76)
        print("SYSTEM PROMPT")
        print("=" * 76)
        print(SYSTEM_PROMPT)
        print()
        print("=" * 76)
        print("USER PROMPT")
        print("=" * 76)
        print(user_prompt)
        return DramaticReaderModelResult(
            annotation_review_candidates=[],
            verifier_commentaries=[],
            dropped=[],
            raw_output=DramaticReaderOutput(),
        )

    if client is None:
        client = anthropic.Anthropic()

    response = client.messages.parse(
        model=model,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        output_config={"effort": effort},
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_prompt}],
        output_format=DramaticReaderOutput,
    )

    raw: DramaticReaderOutput = response.parsed_output

    annotation_review_candidates: list = []
    verifier_commentaries: list = []
    dropped: list = []

    for ar in raw.annotation_reviews:
        reason = _classify_annotation_review(
            ar, lowerings, lowerings_to_review,
        )
        if reason is not None:
            dropped.append(DroppedOutput(reason=reason, raw=ar))
            continue
        review = _translate_annotation_review(
            ar, lowerings, reviewer_id, current_τ_a,
        )
        annotation_review_candidates.append((ar.lowering_id, review))

    for vc in raw.verifier_commentaries:
        reason = _classify_verifier_commentary(
            vc, id_map, reviews_to_comment_on,
        )
        if reason is not None:
            dropped.append(DroppedOutput(reason=reason, raw=vc))
            continue
        commentary = _translate_verifier_commentary(
            vc, id_map, reviewer_id, current_τ_a,
        )
        verifier_commentaries.append(commentary)

    return DramaticReaderModelResult(
        annotation_review_candidates=annotation_review_candidates,
        verifier_commentaries=verifier_commentaries,
        dropped=dropped,
        raw_output=raw,
    )


def _extract_review_ids(verifier_results: tuple) -> list:
    """Return the synthetic ids that would be assigned to the
    VerificationReviews in `verifier_results`, in the same order
    `_build_verifier_section` would assign them. Used as the default
    `reviews_to_comment_on` when the caller doesn't specify one."""
    out: list = []
    review_index = 0
    for r in verifier_results:
        if isinstance(r, VerificationReview):
            out.append(f"vr_{review_index}")
            review_index += 1
    return out
