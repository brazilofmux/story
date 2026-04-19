"""
aristotelian_reader_model_client.py — live LLM probe on the
Aristotelian dialect surface. Specified by aristotelian-probe-
sketch-01.

Dialect-only probe (APS1): the LLM sees only Aristotelian records
(ArMythos, ArPhase, ArCharacter), optional ArObservations (the
self-verifier's output), and a minimal substrate summary for
grounding. No Dramatic / Dramatica-complete / Save-the-Cat records
ever appear in the prompt, even on encodings (Oedipus) that have
all four dialect layers. Aristotelian-sketch-01 A9 scopes cross-
dialect Lowering out of the dialect; the probe stays inside one
dialect in parallel.

Three output kinds (APS2):

1. **AristotelianAnnotationReview** — per-field verdict on an
   Aristotelian record's prose. Parallels
   lowering.AnnotationReview but targets a dialect record's
   prose field (ArMythos.action_summary, ArPhase.annotation,
   ArCharacter.hamartia_text) rather than a Lowering's
   annotation. Translates to ArAnnotationReview.

2. **ObservationCommentary** — verdict on one ArObservation.
   Parallels verification.VerifierCommentary. Oedipus and
   Rashomon both verify with zero observations; the empty case
   still validates the shape for future encodings that surface
   observations. Translates to ArObservationCommentary.

3. **DialectReading** — one per invocation. New surface with no
   analog in the dramatic client. Captures the probe's
   distinctive methodological signal (APS6 P4): did the LLM
   engage Aristotelian vocabulary on the dialect's terms or
   drift into Dramatica / screenplay-structural vocabulary?
   Translates to a DialectReading record.

Defaults follow reader-model-sketch-01 + dramatic_reader_model_
client.py:

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
from dataclasses import dataclass
from typing import Literal, Optional

from pydantic import BaseModel, Field

try:
    import anthropic
except ImportError as exc:
    raise ImportError(
        "The aristotelian-reader-model client requires the anthropic "
        "SDK. Install dependencies via "
        "`pip install -r prototype/requirements.txt`."
    ) from exc

from story_engine.core.aristotelian import (
    ArAnnotationReview,
    ArCharacter,
    ArMythos,
    ArObservation,
    ArObservationCommentary,
    ArPhase,
    DialectReading,
    FIELDS_BY_TARGET_KIND,
    FIELD_ACTION_SUMMARY,
    FIELD_HAMARTIA_TEXT,
    FIELD_PHASE_ANNOTATION,
    TARGET_AR_CHARACTER,
    TARGET_AR_MYTHOS,
    TARGET_AR_PHASE,
    VALID_COMMENTARY_ASSESSMENTS,
    VALID_READ_ON_TERMS,
    VALID_REVIEW_FIELDS,
    VALID_REVIEW_TARGET_KINDS,
    VALID_REVIEW_VERDICTS,
)


# ============================================================================
# Pydantic schemas — what the LLM returns (typed I/O per R1)
# ============================================================================


# Literal-constrain the enum-like fields at parse time. Invalid
# values fail Pydantic validation rather than landing as malformed
# records. Mirrors the dramatic client's AnnotationVerdict /
# CommentaryAssessment pattern.
AnnotationVerdict = Literal[
    "approved", "needs-work", "rejected", "noted",
]

ObservationAssessment = Literal[
    "endorses", "qualifies", "dissents", "noted",
]

ReviewTargetKind = Literal[
    "ArMythos", "ArPhase", "ArCharacter",
]

ReviewField = Literal[
    "action_summary",   # ArMythos only
    "annotation",       # ArPhase only
    "hamartia_text",    # ArCharacter only
]

ReadOnTerms = Literal["yes", "partial", "no"]


class AristotelianAnnotationReview(BaseModel):
    """One LLM verdict on one prose field of one Aristotelian record."""
    target_kind: ReviewTargetKind = Field(
        description=(
            "record kind of the review target: 'ArMythos', "
            "'ArPhase', or 'ArCharacter'"
        )
    )
    target_id: str = Field(
        description=(
            "id of the target record (e.g., 'ar_oedipus', "
            "'ph_beginning', 'ar_jocasta'); must match a record "
            "shown in the prompt"
        )
    )
    field: ReviewField = Field(
        description=(
            "which prose field on the target is under review. "
            "'action_summary' pairs with ArMythos only; "
            "'annotation' with ArPhase only; 'hamartia_text' with "
            "ArCharacter only"
        )
    )
    verdict: AnnotationVerdict = Field(
        description="reviewer's verdict on the named prose field"
    )
    rationale: str = Field(
        description=(
            "1-3 sentences grounded in the record under review "
            "and the substrate events it names. Stay in "
            "Aristotelian vocabulary"
        )
    )


class ObservationCommentary(BaseModel):
    """One LLM read on a single ArObservation."""
    target_observation_id: str = Field(
        description=(
            "synthetic id of the ArObservation being commented on; "
            "matches one of the ids shown in the prompt's "
            "ArObservations section (e.g., 'ao_0')"
        )
    )
    assessment: ObservationAssessment = Field(
        description=(
            "endorses (finding well-grounded), qualifies (finding "
            "stands with clarification), dissents (commenter "
            "disagrees, with grounded counter-argument), or noted "
            "(read but no position)"
        )
    )
    rationale: str = Field(
        description=(
            "2-4 sentences explaining the assessment, grounded in "
            "the ArObservation's message and the records it "
            "targets. A dissent must name what the A7 check missed "
            "or got wrong"
        )
    )
    suggested_signature: Optional[str] = Field(
        default=None,
        description=(
            "Optional. If the commentary identifies a concrete "
            "signature the A7 check might add, propose it as "
            "free-form prose. Not actionable code — inspiration "
            "for the maintainer. Omit unless the suggestion is "
            "concrete and grounded"
        ),
    )


class DialectReadingOutput(BaseModel):
    """The LLM's read on the Aristotelian surface as a whole.
    One per invocation."""
    read_on_terms: ReadOnTerms = Field(
        description=(
            "self-report on whether the review engaged Aristotelian "
            "vocabulary (peripeteia, anagnorisis, hamartia, unity, "
            "catharsis) throughout. 'yes' = clean in-dialect read; "
            "'partial' = mostly in-dialect with specific "
            "scope-limits or relation-wants that would need dialect "
            "extension; 'no' = reverted to Dramatica / screenplay "
            "vocabulary"
        )
    )
    rationale: str = Field(
        description=(
            "3-8 sentences explaining the read_on_terms verdict. "
            "Name specific Aristotelian primitives used; flag "
            "specific places where the vocabulary strained"
        )
    )
    drift_flagged: list[str] = Field(
        default_factory=list,
        description=(
            "Specific out-of-dialect phrases or record types you "
            "noticed yourself using or wanting to use (e.g., "
            "'DSP_limit', 'inciting beat', 'pressure-shape'). "
            "Empty list = clean in-dialect read"
        ),
    )
    scope_limits_observed: list[str] = Field(
        default_factory=list,
        description=(
            "Dialect-scope limits you perceived (e.g., "
            "'meta-anagnorisis: audience-level recognition that "
            "Aristotelian character-level anagnorisis can't "
            "express'). Describe the limit, don't just name it"
        ),
    )
    relations_wanted: list[str] = Field(
        default_factory=list,
        description=(
            "Structural extensions you thought would help (e.g., "
            "'ArMythosRelation to express contest between four "
            "testimony mythoi over shared canonical-floor "
            "events'). Non-empty is NOT drift — these are "
            "probe-surfaced forcing functions for future "
            "Aristotelian-sketch extensions"
        ),
    )


class AristotelianReaderOutput(BaseModel):
    """The full structured response. Empty lists are legal —
    a reviewer with nothing to propose returns empty collections,
    not prose."""
    annotation_reviews: list[AristotelianAnnotationReview] = (
        Field(default_factory=list)
    )
    observation_commentaries: list[ObservationCommentary] = (
        Field(default_factory=list)
    )
    dialect_reading: Optional[DialectReadingOutput] = Field(
        default=None,
        description=(
            "One per invocation. Required in practice; marked "
            "Optional so a refusal / malformed response doesn't "
            "fail the whole parse"
        ),
    )


# ============================================================================
# Result types — translated into dialect-native records
# ============================================================================


@dataclass(frozen=True)
class DroppedOutput:
    """A raw LLM output that failed scope or structural validation
    at translation time. `reason` is a short human-readable
    explanation; `raw` is the Pydantic record so a reviewing author
    can see exactly what was dropped.

    R5 enforcement: the prompt tells the LLM what's in scope, but
    we verify in code. A review that targets a record id not shown,
    a (target_kind, field) mismatch, or an ArObservation id that
    doesn't resolve lands here — never in the accepted lists."""
    reason: str
    raw: object


@dataclass
class AristotelianReaderModelResult:
    """What invoke_aristotelian_reader_model returns.

    `annotation_reviews`, `observation_commentaries`, and
    `dialect_reading` hold the translated dialect-native records.
    `dropped` carries raw outputs that failed validation. `raw_output`
    preserves the pre-translation Pydantic structure for audit."""
    annotation_reviews: list          # list[ArAnnotationReview]
    observation_commentaries: list    # list[ArObservationCommentary]
    dialect_reading: Optional[DialectReading]
    dropped: list                     # list[DroppedOutput]
    raw_output: AristotelianReaderOutput


# ============================================================================
# System prompt — the methodological lever (APS3)
# ============================================================================


SYSTEM_PROMPT = """You are a reader-model — an interpretive peer to a \
structured story-telling engine. Your role is specified by \
reader-model-sketch-01 in the project's design/ directory. This \
invocation is specified by aristotelian-probe-sketch-01.

This invocation puts you on the **Aristotelian dialect surface**. \
The dialect encodes narrative in Aristotle's *Poetics* vocabulary: \
ArMythos (the arrangement of incidents — mythos-as-soul, Poetics \
1450a), ArPhase (beginning/middle/end — logical divisions per \
1451a), ArCharacter (including hamartia — "missing the mark," \
Poetics 1453a). Records may name a peripeteia (reversal, 1452a) \
and an anagnorisis (recognition, ibid). ArObservations are the \
dialect's self-verifier output (aristotelian-sketch-01 A7).

You are reading **one dialect only**. Even if the encoding also \
exists under Dramatica / Save-the-Cat / screenplay-structural \
frames elsewhere, those layers are not shown to you here. Your \
contract is to engage these records *on the dialect's own terms*.

## Methodological lever — the vocabulary rule

Use Aristotelian vocabulary where it applies: **mythos**, \
**peripeteia**, **anagnorisis**, **hamartia**, **unity of action \
/ time / place**, **catharsis**, **pity**, **fear**, \
**complication**, **denouement**, **complex vs. simple plot**. \
Do NOT translate these records into other dialects' vocabularies \
(DSP_limit / pressure-shape / Signpost / Domain from Dramatica; \
inciting beat / midpoint / climax from Save-the-Cat; \
protagonist / antagonist / subplot from general screenplay). If \
you find yourself wanting to reach for other-dialect terms, \
**say so explicitly** in the DialectReading's `drift_flagged` \
list rather than reaching. A probe that flags its own strain is \
more useful than one that papers over it.

Non-dialect vocabulary in `relations_wanted` is different: an \
extension the dialect *could* grow is a forcing function, not \
drift. "ArMythosRelation" is a fair thing to ask for; "DSP_limit" \
is drift.

## Your contract

R1. Typed I/O only. You produce structured output matching the \
provided schema. Prose lives inside `rationale` fields; never \
outside them.

R2. You propose; the author decides. Your reviews are \
recommendations — the author walks them and decides whether to \
update the reviewed prose, amend the encoding, or note and move \
on. You do not mutate state.

R3. Same record types a human reviewer would produce — just with \
`reviewer_id` / `commenter_id` = "llm:<model>".

## The three output kinds

### Annotation reviews (`annotation_reviews`)

For each prose field you are asked to review, produce one \
AristotelianAnnotationReview:

- `target_kind`: 'ArMythos', 'ArPhase', or 'ArCharacter'.
- `target_id`: id of the target record (must appear in the \
prompt).
- `field`: which prose field — 'action_summary' (ArMythos), \
'annotation' (ArPhase), or 'hamartia_text' (ArCharacter). Each \
target_kind has exactly one reviewable field; mis-pairings are \
dropped.
- `verdict`: one of:
  - "approved" — the prose faithfully describes the substrate \
events it names and stays inside Aristotelian vocabulary.
  - "needs-work" — the prose has a specific problem: an \
overstatement of what the substrate carries, an unclear claim, \
a tension between the prose and the record's structural fields \
(e.g., action_summary names "recognition" but \
anagnorisis_event_id is None).
  - "rejected" — the prose should not stand: misreads the \
substrate events, or makes a claim the dialect's structural \
frame actively contradicts.
  - "noted" — read but no position taken (out of competence; \
missing context).
- `rationale`: 1-3 sentences, grounded in the record and the \
substrate events it names.

### Observation commentaries (`observation_commentaries`)

For each ArObservation you are asked to comment on, produce one \
ObservationCommentary:

- `target_observation_id`: synthetic id from the ArObservations \
section (e.g., `ao_0`).
- `assessment`: endorses / qualifies / dissents / noted.
- `rationale`: 2-4 sentences. Cite the observation's message and \
the records it targets. A dissent must name what the A7 check \
missed or got wrong.
- `suggested_signature` (optional): free-form prose naming a \
concrete signature the check might add. Omit unless concrete and \
grounded.

The encoding in this prompt may have zero ArObservations. If so, \
`observation_commentaries` is an empty list — do not fabricate \
observations or comment on records as if they were observations.

### Dialect reading (`dialect_reading`)

Exactly one per invocation. Your read on the Aristotelian surface \
as a whole:

- `read_on_terms`: 'yes' (clean in-dialect read), 'partial' \
(mostly in-dialect, specific scope-limits or relation-wants \
surfaced), or 'no' (reverted to other-dialect vocabulary).
- `rationale`: 3-8 sentences explaining the verdict. Name \
specific Aristotelian primitives used; flag specific places \
where the vocabulary strained.
- `drift_flagged`: list of out-of-dialect phrases you used or \
wanted to use. Empty = clean.
- `scope_limits_observed`: list of dialect-scope limits you \
perceived. Describe the limit, don't just name it (e.g., not \
"meta-anagnorisis" but "meta-anagnorisis: audience-level \
recognition that one testimony is false — Aristotelian \
anagnorisis is character-level only").
- `relations_wanted`: list of structural extensions you thought \
would help. Non-empty is NOT drift — these are forcing functions \
for a future aristotelian-sketch-02.

## Scope discipline

You see exactly what the prompt contains. Nothing exists, for \
your purposes, outside it.

- Do not invent records. If a target_id is not in the prompt, do \
not produce a review for it.
- Observation commentaries cite the synthetic id exactly. If the \
observations section says "(no observations)", \
`observation_commentaries` is `[]`.
- "noted" is correct for uncertainty. "needs-work" / "dissents" \
are for specific findings, not general discomfort.
"""


# ============================================================================
# Helpers — render records as JSON-serializable dicts for the prompt
# ============================================================================


def _ar_phase_to_dict(phase: ArPhase) -> dict:
    return {
        "kind": "ArPhase",
        "id": phase.id,
        "role": phase.role,
        "scope_event_ids": list(phase.scope_event_ids),
        "annotation": phase.annotation,
    }


def _ar_character_to_dict(character: ArCharacter) -> dict:
    return {
        "kind": "ArCharacter",
        "id": character.id,
        "name": character.name,
        "character_ref_id": character.character_ref_id,
        "hamartia_text": character.hamartia_text,
        "is_tragic_hero": character.is_tragic_hero,
    }


def _ar_mythos_to_dict(mythos: ArMythos) -> dict:
    return {
        "kind": "ArMythos",
        "id": mythos.id,
        "title": mythos.title,
        "action_summary": mythos.action_summary,
        "plot_kind": mythos.plot_kind,
        "central_event_ids": list(mythos.central_event_ids),
        "complication_event_id": mythos.complication_event_id,
        "denouement_event_id": mythos.denouement_event_id,
        "peripeteia_event_id": mythos.peripeteia_event_id,
        "anagnorisis_event_id": mythos.anagnorisis_event_id,
        "asserts_unity_of_action": mythos.asserts_unity_of_action,
        "asserts_unity_of_time": mythos.asserts_unity_of_time,
        "asserts_unity_of_place": mythos.asserts_unity_of_place,
        "unity_of_time_bound": mythos.unity_of_time_bound,
        "unity_of_place_max_locations": mythos.unity_of_place_max_locations,
        "aims_at_catharsis": mythos.aims_at_catharsis,
        "phases": [_ar_phase_to_dict(p) for p in mythos.phases],
        "characters": [_ar_character_to_dict(c) for c in mythos.characters],
    }


def _ar_observation_to_dict(
    observation: ArObservation, synthetic_id: str,
) -> dict:
    return {
        "observation_id": synthetic_id,
        "kind": "ArObservation",
        "severity": observation.severity,
        "code": observation.code,
        "target_id": observation.target_id,
        "message": observation.message,
    }


def _substrate_event_summary(event) -> dict:
    """Minimal event summary for grounding prose reviews. Parallels
    dramatic_reader_model_client._substrate_event_summary but
    stripped further — no effect_count (Aristotelian prose reviews
    rarely need effect shape to judge). Enough for the LLM to check
    "the action_summary claims X; does the event with that id
    actually carry X's participants at the right τ_s?".

    Keeps the substrate section small: the Rashomon four-mythos
    invocation references 22 events; at ~40 chars / event summary
    the section stays well under a paragraph."""
    return {
        "id": event.id,
        "type": event.type,
        "τ_s": event.τ_s,
        "participants": event.participants,
    }


# ============================================================================
# Prompt construction
# ============================================================================


def _build_records_section(mythoi: tuple) -> str:
    """Render all ArMythos records (phases + characters inlined) as
    JSON. Mythos order is input order; phases / characters preserve
    their declared order."""
    payload = [_ar_mythos_to_dict(m) for m in mythoi]
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _build_observations_section(observations: tuple) -> tuple:
    """Render ArObservation records with synthetic ids. Returns
    (rendered_json_or_empty_marker, id_map).

    An empty observations tuple renders the literal "(no
    observations — encoding verifies clean)" so the prompt reads
    naturally and the LLM sees that `observation_commentaries`
    should be `[]`.
    """
    if not observations:
        return "(no observations — encoding verifies clean)", {}
    id_map: dict = {}
    rendered: list = []
    for index, obs in enumerate(observations):
        sid = f"ao_{index}"
        id_map[sid] = obs
        rendered.append(_ar_observation_to_dict(obs, sid))
    return json.dumps(rendered, indent=2, ensure_ascii=False), id_map


def _build_substrate_section(substrate_events: list) -> Optional[str]:
    """Render the substrate-event summary. Returns None when empty —
    the caller omits the whole section in that case, matching the
    dramatic client's substrate-context pattern."""
    if not substrate_events:
        return None
    payload = {
        "events": [_substrate_event_summary(e) for e in substrate_events],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _build_task_section(
    targets_to_review: list,
    observations_to_comment_on: list,
    has_observations: bool,
) -> str:
    """Render the task section. `targets_to_review` is a list of
    (target_kind, target_id, field) triples (as lists, matching the
    JSON-friendly shape); `observations_to_comment_on` is a list of
    synthetic ids."""
    parts: list = ["## Task", ""]
    if targets_to_review:
        parts.append("Review the prose on these record-fields:")
        for target_kind, target_id, field in targets_to_review:
            parts.append(f"- {target_kind}:{target_id}:{field}")
    else:
        parts.append("(No prose fields to review.)")
    parts.append("")
    if observations_to_comment_on:
        parts.append("Comment on these ArObservations:")
        for sid in observations_to_comment_on:
            parts.append(f"- {sid}")
    elif has_observations:
        parts.append("(No ArObservations to comment on.)")
    else:
        parts.append(
            "(The encoding verifies with zero observations; "
            "`observation_commentaries` should be `[]`.)"
        )
    parts.append("")
    parts.append(
        "Produce exactly one DialectReading for this invocation, "
        "regardless of how many annotation reviews or observation "
        "commentaries you emit."
    )
    return "\n".join(parts)


def _eligible_targets(mythoi: tuple) -> list:
    """Return every (target_kind, target_id, field) triple the
    invocation could review. Used as the default `targets_to_review`
    when the caller doesn't specify. Order: mythos records first
    (action_summary), then phases (annotation), then characters
    (hamartia_text), preserving declared order within each."""
    out: list = []
    for m in mythoi:
        out.append((TARGET_AR_MYTHOS, m.id, FIELD_ACTION_SUMMARY))
    for m in mythoi:
        for p in m.phases:
            out.append((TARGET_AR_PHASE, p.id, FIELD_PHASE_ANNOTATION))
    for m in mythoi:
        for c in m.characters:
            # Only characters with non-None hamartia_text are
            # naturally reviewable — an empty field has nothing to
            # review. Drop characters with no hamartia text.
            if c.hamartia_text is not None:
                out.append(
                    (TARGET_AR_CHARACTER, c.id, FIELD_HAMARTIA_TEXT)
                )
    return out


def _records_by_kind_id(mythoi: tuple) -> dict:
    """Build an index (target_kind, target_id) -> record. Used by
    scope validators to confirm a review targets an actually-
    rendered record."""
    index: dict = {}
    for m in mythoi:
        index[(TARGET_AR_MYTHOS, m.id)] = m
        for p in m.phases:
            index[(TARGET_AR_PHASE, p.id)] = p
        for c in m.characters:
            index[(TARGET_AR_CHARACTER, c.id)] = c
    return index


def build_user_prompt(
    mythoi: tuple,
    observations: tuple,
    substrate_events: list,
    targets_to_review: list,
    observations_to_comment_on: list,
) -> tuple:
    """Public helper: assemble the full user message and the
    synthetic-id map for ArObservations. Returns (prompt, id_map).

    The id_map is needed at translation time to resolve the LLM's
    `target_observation_id` values back to ArObservation records.
    Empty observations produce an empty id_map."""
    records_section = _build_records_section(mythoi)
    observations_section, id_map = _build_observations_section(observations)
    substrate_section = _build_substrate_section(substrate_events)
    task = _build_task_section(
        targets_to_review, observations_to_comment_on,
        has_observations=bool(observations),
    )

    sections: list = [
        "# Aristotelian dialect surface",
        "",
        "## ArMythos records",
        "",
        ("(Each ArMythos inlines its phases and characters. "
         "Prose fields under review: `action_summary` on each "
         "ArMythos; `annotation` on each ArPhase; `hamartia_text` "
         "on each ArCharacter that carries one.)"),
        "",
        records_section,
        "",
        "## ArObservations (self-verifier output)",
        "",
        ("(Each observation carries a synthetic `observation_id` "
         "like `ao_0` — use that id when commenting. Empty section "
         "means the encoding verifies clean and "
         "`observation_commentaries` should be `[]`.)"),
        "",
        observations_section,
        "",
    ]
    if substrate_section is not None:
        sections.extend([
            "## Substrate context (grounding)",
            "",
            ("(Minimal summary of substrate events named by the "
             "ArMythos records above. For grounding prose reviews "
             "against what the named events actually carry — "
             "`id`, `type`, `τ_s`, `participants`. Not exhaustive; "
             "no effect lists.)"),
            "",
            substrate_section,
            "",
        ])
    sections.extend(["", task])
    return "\n".join(sections), id_map


# ============================================================================
# Translation: LLM output → dialect-native records
# ============================================================================


def _classify_annotation_review(
    raw: AristotelianAnnotationReview,
    records_index: dict,
    targets_to_review: list,
) -> Optional[str]:
    """Validate one raw annotation review against scope. Returns
    None if accepted, else a reason string.

    Four gates: (a) target_kind is in the vocabulary, (b) field is
    in the vocabulary and pairs correctly with target_kind,
    (c) target_id resolves to an actual record of that kind in the
    index, (d) the (target_kind, target_id, field) triple is in
    `targets_to_review`."""
    if raw.target_kind not in VALID_REVIEW_TARGET_KINDS:
        return (
            f"target_kind {raw.target_kind!r} is not one of "
            f"{sorted(VALID_REVIEW_TARGET_KINDS)}"
        )
    if raw.field not in VALID_REVIEW_FIELDS:
        return (
            f"field {raw.field!r} is not one of "
            f"{sorted(VALID_REVIEW_FIELDS)}"
        )
    valid_fields_for_kind = FIELDS_BY_TARGET_KIND[raw.target_kind]
    if raw.field not in valid_fields_for_kind:
        return (
            f"field {raw.field!r} does not pair with target_kind "
            f"{raw.target_kind!r}; valid fields for that kind are "
            f"{sorted(valid_fields_for_kind)}"
        )
    if (raw.target_kind, raw.target_id) not in records_index:
        return (
            f"target_id {raw.target_id!r} with target_kind "
            f"{raw.target_kind!r} does not resolve to any rendered "
            f"record"
        )
    triple = [raw.target_kind, raw.target_id, raw.field]
    # targets_to_review is a list of 3-tuples-as-lists; compare
    # normalized
    normalized_scope = [list(t) for t in targets_to_review]
    if triple not in normalized_scope:
        return (
            f"review target {raw.target_kind}:{raw.target_id}:"
            f"{raw.field} is outside the declared targets_to_review "
            f"scope"
        )
    # Redundant Literal-constrained by Pydantic, but belt+braces
    if raw.verdict not in VALID_REVIEW_VERDICTS:
        return (
            f"verdict {raw.verdict!r} is not one of "
            f"{sorted(VALID_REVIEW_VERDICTS)}"
        )
    return None


def _translate_annotation_review(
    raw: AristotelianAnnotationReview,
    reviewer_id: str,
    current_τ_a: int,
    anchor_τ_a: int,
) -> ArAnnotationReview:
    """One accepted AristotelianAnnotationReview → one
    ArAnnotationReview record. Caller must have already passed the
    raw through _classify_annotation_review and seen None."""
    return ArAnnotationReview(
        reviewer_id=reviewer_id,
        reviewed_at_τ_a=current_τ_a,
        target_kind=raw.target_kind,
        target_id=raw.target_id,
        field=raw.field,
        verdict=raw.verdict,
        comment=raw.rationale,
        anchor_τ_a=anchor_τ_a,
    )


def _classify_observation_commentary(
    raw: ObservationCommentary,
    id_map: dict,
    observations_to_comment_on: list,
) -> Optional[str]:
    """Validate one raw observation commentary against scope.
    Returns None if accepted, else a reason string."""
    if raw.target_observation_id not in observations_to_comment_on:
        return (
            f"target_observation_id {raw.target_observation_id!r} "
            f"is outside the declared observations_to_comment_on "
            f"scope"
        )
    if raw.target_observation_id not in id_map:
        return (
            f"target_observation_id {raw.target_observation_id!r} "
            f"does not resolve to any ArObservation in this "
            f"invocation"
        )
    if raw.assessment not in VALID_COMMENTARY_ASSESSMENTS:
        return (
            f"assessment {raw.assessment!r} is not one of "
            f"{sorted(VALID_COMMENTARY_ASSESSMENTS)}"
        )
    return None


def _translate_observation_commentary(
    raw: ObservationCommentary,
    id_map: dict,
    commenter_id: str,
    current_τ_a: int,
) -> ArObservationCommentary:
    """One accepted ObservationCommentary → one
    ArObservationCommentary carrying the resolved ArObservation."""
    target = id_map[raw.target_observation_id]
    return ArObservationCommentary(
        commenter_id=commenter_id,
        commented_at_τ_a=current_τ_a,
        assessment=raw.assessment,
        target_observation=target,
        comment=raw.rationale,
        suggested_signature=raw.suggested_signature,
    )


def _classify_dialect_reading(
    raw: DialectReadingOutput,
) -> Optional[str]:
    """Validate the dialect reading. Pydantic already constrains
    read_on_terms via Literal; the belt+braces check here guards
    against a future shape drift."""
    if raw.read_on_terms not in VALID_READ_ON_TERMS:
        return (
            f"read_on_terms {raw.read_on_terms!r} is not one of "
            f"{sorted(VALID_READ_ON_TERMS)}"
        )
    return None


def _translate_dialect_reading(
    raw: DialectReadingOutput,
    reader_id: str,
    current_τ_a: int,
) -> DialectReading:
    return DialectReading(
        reader_id=reader_id,
        read_at_τ_a=current_τ_a,
        read_on_terms=raw.read_on_terms,
        rationale=raw.rationale,
        drift_flagged=tuple(raw.drift_flagged),
        scope_limits_observed=tuple(raw.scope_limits_observed),
        relations_wanted=tuple(raw.relations_wanted),
    )


# ============================================================================
# Entry point
# ============================================================================


def invoke_aristotelian_reader_model(
    *,
    mythoi: tuple,
    current_τ_a: int,
    observations: tuple = (),
    substrate_events: Optional[list] = None,
    targets_to_review: Optional[list] = None,
    observations_to_comment_on: Optional[list] = None,
    anchor_τ_a: Optional[int] = None,
    model: str = "claude-opus-4-6",
    reviewer_id: Optional[str] = None,
    effort: str = "high",
    max_tokens: int = 16_000,
    dry_run: bool = False,
    client: Optional["anthropic.Anthropic"] = None,
) -> AristotelianReaderModelResult:
    """Invoke the Aristotelian-dialect reader-model probe.

    Args:
        mythoi: tuple of ArMythos records. Single-mythos encodings
            (Oedipus) pass `(AR_OEDIPUS_MYTHOS,)`; multi-mythos
            encodings (Rashomon) pass the whole tuple.
        current_τ_a: τ_a stamped on all produced records. Typical:
            "next τ_a after the last authoring commit".
        observations: tuple of ArObservation records (the A7
            verifier's output). Default: empty — Oedipus and
            Rashomon both verify with zero.
        substrate_events: optional list of Event records for
            grounding prose reviews. Default: None (no substrate
            section rendered). Passing a full fabula is fine; the
            renderer summarizes each event to `(id, type, τ_s,
            participants)` only.
        targets_to_review: list of (target_kind, target_id, field)
            triples to review. Default: every eligible prose field
            across the mythoi. Pass `[]` to skip annotation
            reviews.
        observations_to_comment_on: list of synthetic ids
            (`ao_0`, `ao_1`, …) to comment on. Default: every
            ArObservation's synthetic id. Pass `[]` to skip
            commentary (or leave default on a zero-observation run
            — it becomes `[]` automatically).
        anchor_τ_a: τ_a the encoding was last authored at, used as
            the ArAnnotationReview's `anchor_τ_a` for staleness.
            Default: `current_τ_a` (safe floor — reviews pin to
            their own time when caller has no better signal).
        model / reviewer_id / effort / max_tokens / dry_run /
            client: standard knobs parallel to
            invoke_dramatic_reader_model.

    Returns:
        AristotelianReaderModelResult with annotation_reviews,
        observation_commentaries, dialect_reading (or None on a
        refusal / malformed response), dropped (raw outputs that
        failed scope validation), and raw_output.
    """
    if reviewer_id is None:
        reviewer_id = f"llm:{model}"
    if substrate_events is None:
        substrate_events = []
    if anchor_τ_a is None:
        anchor_τ_a = current_τ_a

    if targets_to_review is None:
        targets_to_review = _eligible_targets(mythoi)
    if observations_to_comment_on is None:
        observations_to_comment_on = [
            f"ao_{i}" for i in range(len(observations))
        ]

    user_prompt, id_map = build_user_prompt(
        mythoi, observations, substrate_events,
        targets_to_review, observations_to_comment_on,
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
        return AristotelianReaderModelResult(
            annotation_reviews=[],
            observation_commentaries=[],
            dialect_reading=None,
            dropped=[],
            raw_output=AristotelianReaderOutput(),
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
        output_format=AristotelianReaderOutput,
    )

    raw: AristotelianReaderOutput = response.parsed_output
    return translate_raw_output(
        raw=raw,
        mythoi=mythoi,
        id_map=id_map,
        targets_to_review=targets_to_review,
        observations_to_comment_on=observations_to_comment_on,
        reviewer_id=reviewer_id,
        current_τ_a=current_τ_a,
        anchor_τ_a=anchor_τ_a,
    )


def translate_raw_output(
    *,
    raw: AristotelianReaderOutput,
    mythoi: tuple,
    id_map: dict,
    targets_to_review: list,
    observations_to_comment_on: list,
    reviewer_id: str,
    current_τ_a: int,
    anchor_τ_a: int,
) -> AristotelianReaderModelResult:
    """Translate a raw Pydantic output into a result. Public so
    tests can exercise translation without constructing an
    API-client mock; demos that cache raw JSON can also re-run
    translation without a second API call."""
    records_index = _records_by_kind_id(mythoi)

    annotation_reviews: list = []
    observation_commentaries: list = []
    dropped: list = []

    for ar in raw.annotation_reviews:
        reason = _classify_annotation_review(
            ar, records_index, targets_to_review,
        )
        if reason is not None:
            dropped.append(DroppedOutput(reason=reason, raw=ar))
            continue
        annotation_reviews.append(
            _translate_annotation_review(
                ar, reviewer_id, current_τ_a, anchor_τ_a,
            )
        )

    for oc in raw.observation_commentaries:
        reason = _classify_observation_commentary(
            oc, id_map, observations_to_comment_on,
        )
        if reason is not None:
            dropped.append(DroppedOutput(reason=reason, raw=oc))
            continue
        observation_commentaries.append(
            _translate_observation_commentary(
                oc, id_map, reviewer_id, current_τ_a,
            )
        )

    dialect_reading: Optional[DialectReading] = None
    if raw.dialect_reading is not None:
        reason = _classify_dialect_reading(raw.dialect_reading)
        if reason is not None:
            dropped.append(
                DroppedOutput(reason=reason, raw=raw.dialect_reading)
            )
        else:
            dialect_reading = _translate_dialect_reading(
                raw.dialect_reading, reviewer_id, current_τ_a,
            )

    return AristotelianReaderModelResult(
        annotation_reviews=annotation_reviews,
        observation_commentaries=observation_commentaries,
        dialect_reading=dialect_reading,
        dropped=dropped,
        raw_output=raw,
    )
