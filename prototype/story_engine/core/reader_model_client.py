"""
reader_model_client.py — live LLM integration for the reader-model surface.

First live-LLM iteration of reader-model-sketch-01's probe. Takes a
`ReaderView` (produced by `substrate.reader_view`) and a list of description
ids to review / questions to answer, and calls Claude Opus 4.6 with a typed
prompt + structured-output schema. Returns substrate-native `ReviewEntry`
records (ready for `ingest_review`) and `AnswerProposal` records (queue-
ready candidate descriptions the author can accept to commit).

Architectural placement: this is **tooling**, not substrate. The substrate
produces the view and ingests results; the LLM call, prompt templating,
and response parsing live here. Keeps the fold pure (R5 — every invocation
is explicit, declared, visible to the caller).

Defaults follow reader-model-sketch-01 and the claude-api skill:

- model: claude-opus-4-6 (user's explicit pick; best-in-class writer)
- thinking: {"type": "adaptive"} (recommended on Opus 4.6; budget_tokens is
  deprecated)
- output_config.effort: "high" — this is interpretive work where quality
  matters
- max_tokens: 16_000 (non-streaming; well under SDK timeout limits)
- cache_control: {"type": "ephemeral"} at top level — caches the largest
  stable prefix (system prompt + view), which pays off the moment the
  caller makes a second call against the same view (e.g., re-invoking with
  a different subset of descriptions to review)
- typed I/O only (R1): uses `client.messages.parse()` with a Pydantic
  schema; no free-form prose crosses the boundary

Requires: `pip install -r prototype/requirements.txt`.
API key: reads `ANTHROPIC_API_KEY` from the environment (SDK default).
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
        "The reader-model client requires the anthropic SDK. "
        "Install dependencies via "
        "`pip install -r prototype/requirements.txt`."
    ) from exc

from story_engine.core.substrate import (
    AnswerProposal,
    Attention,
    Description,
    DescStatus,
    EditProposal,
    KnowledgeEffect,
    Prop,
    ReaderView,
    ReviewEntry,
    ReviewVerdict,
    WorldEffect,
    effective_branches,
)


# ============================================================================
# Pydantic schemas — what the LLM returns (typed I/O per R1)
# ============================================================================


# Kind names track the descriptions-sketch-01 starting vocabulary. The
# Literal constrains the LLM at parse time — a kind outside this set fails
# validation rather than landing a malformed record in substrate.
AnswerKind = Literal[
    "texture",
    "motivation",
    "reader-frame",
    "trust-flag",
    "authorial-uncertainty",
    "provenance",
]

Verdict = Literal["approved", "needs-work", "rejected", "noted"]


class ReaderReview(BaseModel):
    """One reviewer verdict from the LLM on a single description."""
    description_id: str = Field(description="id of the description being reviewed")
    verdict: Verdict = Field(description="the reviewer's verdict")
    rationale: str = Field(
        description=(
            "1-3 sentences explaining the verdict, grounded in view content"
        )
    )


class ReaderAnswer(BaseModel):
    """A proposed answer to a `is_question=True` description, shaped as a
    new description the author can accept to commit."""
    question_description_id: str = Field(
        description="id of the is_question=True description being answered"
    )
    answer_kind: AnswerKind = Field(
        description=(
            "kind of the proposed answer — match the answer's content, not "
            "the question's kind"
        )
    )
    answer_text: str = Field(
        description=(
            "body of the proposed new description; 3-6 sentences, grounded "
            "in view content"
        )
    )
    rationale: str = Field(
        description=(
            "1-2 sentences explaining how the answer derives from facts + "
            "other descriptions in view"
        )
    )


class ReaderEdit(BaseModel):
    """A proposed edit to an existing description — a rewrite the
    author can accept to replace the current text with an improved
    version. Produced when a review's rationale names a specific
    revision and the improvement is concrete enough to offer as a
    drop-in. Descriptions flagged with is_question=True are NOT
    edit-eligible (use ReaderAnswer for those)."""
    source_description_id: str = Field(
        description=(
            "id of the description to be replaced. Must be in scope "
            "(edits_for) and must not be a question."
        )
    )
    new_text: str = Field(
        description=(
            "the replacement text for the description's body. Should "
            "address the specific issue the review identified, keep "
            "within the source description's kind/attention, and stay "
            "grounded in view content."
        )
    )
    new_kind: Optional[AnswerKind] = Field(
        default=None,
        description=(
            "optional override if the edit warrants re-categorization. "
            "Defaults to the source's kind (preserve) when omitted."
        ),
    )
    rationale: str = Field(
        description=(
            "1-2 sentences explaining what specifically was changed "
            "and why, grounded in facts / descriptions in view"
        )
    )


class ReaderOutput(BaseModel):
    """The full structured response. Empty lists are legal — an LLM with
    nothing to propose or review returns empty collections, not prose."""
    reviews: list[ReaderReview] = Field(default_factory=list)
    answers: list[ReaderAnswer] = Field(default_factory=list)
    edits: list[ReaderEdit] = Field(default_factory=list)


# ============================================================================
# Result types — translated into substrate-native records
# ============================================================================


@dataclass(frozen=True)
class DroppedOutput:
    """A raw LLM output record that failed scope or structural validation
    at ingest time. `reason` is a short human-readable explanation;
    `raw` is the Pydantic record (ReaderReview or ReaderAnswer) so a
    reviewing author can see exactly what was dropped and why.

    R5 enforcement: the prompt tells the LLM what's in scope, but we
    verify in code. An LLM that reviews a description outside
    reviews_for, or proposes an answer for a non-question description,
    lands here — never in reviews / proposed_answers.
    """
    reason: str
    raw: object  # ReaderReview | ReaderAnswer


@dataclass
class ReaderModelResult:
    """What invoke_reader_model returns. `review_candidates`,
    `answer_proposals`, and `edit_proposals` are substrate-native and
    scope-enforced. `dropped` captures outputs that failed validation
    (for audit and debugging). `raw_output` is the pre-translation LLM
    response, kept for callers who want the rationale strings without
    re-parsing.

    `review_candidates` pairs each translated `ReviewEntry` with its
    target description id. The pair is the authoritative artifact —
    a `ReviewEntry` alone does not identify which description it
    reviews, and zipping two parallel lists (translated vs. raw) is
    unsafe when any raw record was dropped at the validation gate.
    """
    review_candidates: list  # list[tuple[str, ReviewEntry]]
    answer_proposals: list   # list[AnswerProposal] — queue-ready
    edit_proposals: list     # list[EditProposal] — queue-ready
    dropped: list            # list[DroppedOutput]
    raw_output: ReaderOutput


# ============================================================================
# Prompt construction
# ============================================================================


# The system prompt is intentionally frozen across calls. Any per-request
# content (timestamps, ids, task-specific directives) lives in the user
# message so the system prompt can be cached per the claude-api skill's
# silent-invalidator audit. If you need to tweak behavior per call,
# adjust the task section, not this string.
SYSTEM_PROMPT = """You are a reader-model — an interpretive peer to a \
structured story-telling engine. Your role is specified by \
reader-model-sketch-01 in the project's design/ directory.

Your contract:

R1. Typed I/O only. You produce structured output matching the provided \
schema. Prose lives inside the `rationale` and `answer_text` fields; \
never outside them.

R2. The view distinguishes facts from descriptions structurally. Events \
(facts) are in the `events` section. Descriptions (interpretations) are \
in the `descriptions` section. These are separate surfaces with different \
semantics — never treat a description as if it were a derived fact or \
vice versa.

R3. You propose; the author decides. Your reviews are recommendations. \
Your answers are candidate descriptions for authorial acceptance, not \
accepted facts. You do not assert anything into substrate state \
directly.

R4. Reviews are the same record type a human reviewer would produce — \
just with `reviewer_id` = "llm:<model>". The substrate does not \
distinguish LLM and human reviews beyond the identifier.

## The engine's division of labor

The engine separates structural facts (typed events with effects — who \
is where, who knows what, who killed whom) from interpretive \
descriptions (motivation, tonal texture, reader-frame commentary). The \
schema catches drift in facts; an attentive reader catches drift in \
descriptions. That attentive reader is you.

## What you will see

A ReaderView containing:

- `branch`: the narrative branch (:canonical, or a :contested branch \
such as :b-wife).
- `up_to_τ_s`: story-time bound. Events at later τ_s are out of scope.
- `up_to_τ_a`: authored-time bound.
- `events`: typed event records with effects. Canonical structural \
truth on this branch.
- `descriptions`: typed description records (kind, attention, text, \
branch scope). Interpretations attached to events or other \
descriptions.
- `open_questions`: descriptions where is_question=True. Author-posed \
questions about the story.

After the view, a task section names which descriptions to review and \
which questions to answer.

## Reviewing descriptions

For each description you are asked to review, produce one ReaderReview:

- `description_id`: the description being reviewed.
- `verdict`: one of:
  - "approved" — consistent with the events in view and a reasonable \
interpretation.
  - "needs-work" — has a specific problem: factual tension with events, \
an unclear claim, or a reading that undermines the scene's effect.
  - "rejected" — the description should not exist; its claim is wrong \
in a way editing won't fix.
  - "noted" — you read it but decline to take a position (missing \
context, outside your expertise).
- `rationale`: 1-3 sentences explaining the verdict. Specific, grounded \
in the view's contents.

## Answering open questions

For each open question, produce one ReaderAnswer:

- `question_description_id`: the is_question description being \
answered.
- `answer_kind`: the kind for the proposed answer (texture, \
motivation, reader-frame, trust-flag, authorial-uncertainty, or \
provenance). Pick the kind whose semantics match the answer's content, \
not the question's kind.
- `answer_text`: the body of the proposed new description. A \
substantive answer, 3-6 sentences, grounded in view content.
- `rationale`: 1-2 sentences explaining how the answer follows from \
the facts and other descriptions in view.

## Proposing edits

When a review identifies a concrete revision — a specific better \
phrasing, a tightened claim, the removal of an inaccuracy the rest of \
the description otherwise gets right — you may ALSO produce a \
ReaderEdit alongside the review. Edits are a drop-in replacement for \
the description's text; accepted edits supersede the source.

One ReaderEdit per description you want to revise:

- `source_description_id`: the description being replaced. Must not be \
a question (questions take answers, not edits) and must not already \
be superseded.
- `new_text`: the replacement body. Keep the source's kind and \
attention unless you set `new_kind`. Address the specific issue the \
review identified; preserve anything that was not flagged.
- `new_kind`: optional — set only when the edit changes what kind of \
interpretation the description carries (rare).
- `rationale`: 1-2 sentences naming exactly what you changed and why, \
grounded in view content.

Edits are OPTIONAL. If your review identified no concrete revision, \
or only a vague "could be better," do NOT emit an edit. An empty \
edits list is the common case, and is preferred to a speculative \
rewrite. An approved-verdict review never needs an accompanying edit.

## Scope discipline

You see exactly what the view contains. Nothing exists, for your \
purposes, outside the view.

- Never invent events. If the view contains no evidence for a claim, \
do not make that claim.
- Never synthesize identities (claim that two named entities are the \
same). The substrate forbids automatic identity inference.
- Do not reason about sibling branches, earlier or later τ_s ranges, \
or other content you cannot see in this view. Comparative claims \
("the most X of the Y accounts", "X is better than Y") are licensed \
only when every item being compared appears in the view. If they do \
not, make the claim about only the content you see, or do not make \
it.
- If a description is on a contested branch (say, :b-wife), evaluate \
it within that branch's reality. Do not hold it against facts from a \
sibling :contested branch — and do not compare it to descriptions on \
sibling branches unless those descriptions are in the view.
- If you cannot make a good-faith judgment on a description, \
verdict="noted" is correct. "needs-work" is for specific flaws, not \
general uncertainty.
"""


def _format_prop(p: Prop) -> str:
    if not p.args:
        return p.predicate
    args_str = ", ".join(str(a) for a in p.args)
    return f"{p.predicate}({args_str})"


def _event_to_dict(event) -> dict:
    """Convert an Event to a JSON-dumpable dict for the prompt."""
    effects: list[dict] = []
    for e in event.effects:
        if isinstance(e, WorldEffect):
            effects.append(
                {
                    "kind": "world",
                    "prop": _format_prop(e.prop),
                    "asserts": e.asserts,
                }
            )
        elif isinstance(e, KnowledgeEffect):
            effects.append(
                {
                    "kind": "agent_knowledge",
                    "agent": e.agent_id,
                    "prop": _format_prop(e.held.prop),
                    "slot": e.held.slot.value,
                    "via": e.held.via,
                    "remove": e.remove,
                }
            )
    return {
        "id": event.id,
        "type": event.type,
        "τ_s": event.τ_s,
        "τ_a": event.τ_a,
        "branches": sorted(event.branches),
        "participants": event.participants,
        "effects": effects,
    }


def _description_to_dict(record, events, descriptions) -> dict:
    """Convert a ViewDescriptionRecord to a JSON-dumpable dict."""
    d = record.description
    anchor = d.attached_to
    anchor_repr = f"{anchor.kind}:{anchor.target_id}"
    eff_branches = effective_branches(d, events, descriptions)
    return {
        "id": d.id,
        "attached_to": anchor_repr,
        "kind": d.kind,
        "attention": d.attention.value,
        "text": d.text,
        "authored_by": d.authored_by,
        "τ_a": d.τ_a,
        "is_question": d.is_question,
        "branches_visible_on": sorted(eff_branches),
        "effectively_unreviewed": record.effectively_unreviewed,
        "anchor_in_view": record.anchor_in_view,
    }


def _serialize_view(view: ReaderView, events: list, descriptions: list) -> str:
    """Render the ReaderView as a readable prompt body. Facts and
    descriptions live in distinct top-level sections per R2's structural
    firewall — the LLM can never misread one as the other.
    """
    attention_filter_str = (
        ", ".join(sorted(a.value for a in view.attention_filter))
        if view.attention_filter
        else "all"
    )
    events_json = json.dumps(
        [_event_to_dict(r.event) for r in view.events],
        indent=2,
        ensure_ascii=False,
    )
    descriptions_json = json.dumps(
        [_description_to_dict(r, events, descriptions) for r in view.descriptions],
        indent=2,
        ensure_ascii=False,
    )
    open_questions_lines = [
        f"- {r.description.id}" for r in view.open_questions
    ] or ["(none)"]

    return "\n".join(
        [
            "# ReaderView",
            "",
            f"- branch: {view.branch_label}",
            f"- up_to_τ_s: {view.up_to_τ_s}",
            f"- up_to_τ_a: {view.up_to_τ_a}",
            f"- attention_filter: {attention_filter_str}",
            "",
            "## Events (facts)",
            "",
            events_json,
            "",
            "## Descriptions (interpretations)",
            "",
            descriptions_json,
            "",
            "## Open questions",
            "",
            *open_questions_lines,
        ]
    )


def _build_task_section(
    reviews_for: list[str],
    answers_for: list[str],
    edits_for: list[str],
) -> str:
    parts: list[str] = ["## Task", ""]
    if reviews_for:
        parts.append("Review these descriptions:")
        parts.extend(f"- {d}" for d in reviews_for)
    else:
        parts.append("(No descriptions to review.)")
    parts.append("")
    if answers_for:
        parts.append("Answer these open questions:")
        parts.extend(f"- {d}" for d in answers_for)
    else:
        parts.append("(No open questions to answer.)")
    parts.append("")
    if edits_for:
        parts.append(
            "Edits are permitted (but not required) on these descriptions:"
        )
        parts.extend(f"- {d}" for d in edits_for)
        parts.append("")
        parts.append(
            "Only propose an edit when your review identifies a specific, "
            "concrete revision — a better phrasing, a tightened claim, a "
            "removed inaccuracy. A general 'this could be better' is not "
            "enough; an empty edits list is the common case."
        )
    else:
        parts.append("(Edits are not permitted in this invocation.)")
    return "\n".join(parts)


def build_user_prompt(
    view: ReaderView,
    events: list,
    descriptions: list,
    reviews_for: list[str],
    answers_for: list[str],
    edits_for: list[str],
) -> str:
    """Public helper: assemble the full user message without calling the API.
    Used by the demo's dry-run mode and by structure tests."""
    body = _serialize_view(view, events, descriptions)
    task = _build_task_section(reviews_for, answers_for, edits_for)
    return f"{body}\n\n{task}"


# ============================================================================
# Translation: LLM output → substrate-native records
# ============================================================================


def _resolve_anchor_τ_a(anchor, events, descriptions) -> Optional[int]:
    """Latest τ_a among records matching the anchor's id. Matches the
    substrate's internal convention for review staleness tracking."""
    if anchor.kind == "event":
        best: Optional[int] = None
        for e in events:
            if e.id == anchor.target_id and (best is None or e.τ_a > best):
                best = e.τ_a
        return best
    if anchor.kind == "description":
        best = None
        for d in descriptions:
            if d.id == anchor.target_id and (best is None or d.τ_a > best):
                best = d.τ_a
        return best
    return None


def _classify_review(
    raw: ReaderReview,
    descriptions: list,
    reviews_for: list,
) -> Optional[str]:
    """Validate a raw review against the declared invocation scope.
    Returns None if accepted, or a reason string if it should be
    dropped. R5 enforcement: membership in reviews_for is the
    authoritative gate, not the prompt."""
    if raw.description_id not in reviews_for:
        return (
            f"description_id {raw.description_id!r} is outside the "
            f"declared reviews_for scope"
        )
    if not any(d.id == raw.description_id for d in descriptions):
        return (
            f"description_id {raw.description_id!r} does not resolve "
            f"to any known description"
        )
    return None


def _translate_review(
    raw: ReaderReview,
    descriptions: list,
    events: list,
    reviewer_id: str,
    current_τ_a: int,
) -> ReviewEntry:
    """One accepted ReaderReview → one ReviewEntry. Caller must have
    already passed the review through _classify_review and seen None
    (accepted); this function assumes the id resolves."""
    desc = next(d for d in descriptions if d.id == raw.description_id)
    anchor_τ_a = _resolve_anchor_τ_a(desc.attached_to, events, descriptions)
    return ReviewEntry(
        reviewer_id=reviewer_id,
        reviewed_at_τ_a=current_τ_a,
        verdict=ReviewVerdict(raw.verdict),
        anchor_τ_a=anchor_τ_a if anchor_τ_a is not None else 0,
        comment=raw.rationale,
    )


def _classify_answer(
    raw: ReaderAnswer,
    descriptions: list,
    answers_for: list,
) -> Optional[str]:
    """Validate a raw answer against the declared invocation scope.
    Returns None if accepted, or a reason string if it should be
    dropped.

    Three gates:
      - `question_description_id` must be in `answers_for` (R5).
      - The target description must exist.
      - The target must have `is_question=True`. A ReaderAnswer naming
        an ordinary description is a contract violation — answers are
        for open questions only (descriptions-sketch-01 D3 + the
        reader-model sketch's answer-shape).
    """
    if raw.question_description_id not in answers_for:
        return (
            f"question_description_id {raw.question_description_id!r} is "
            f"outside the declared answers_for scope"
        )
    question = next(
        (d for d in descriptions if d.id == raw.question_description_id),
        None,
    )
    if question is None:
        return (
            f"question_description_id {raw.question_description_id!r} "
            f"does not resolve to any known description"
        )
    if not question.is_question:
        return (
            f"description {raw.question_description_id!r} is not a "
            f"question (is_question=False); answers are only valid for "
            f"is_question=True descriptions"
        )
    return None


def _classify_edit(
    raw: ReaderEdit,
    descriptions: list,
    edits_for: list,
) -> Optional[str]:
    """Validate a raw edit against the declared invocation scope.
    Returns None if accepted, or a reason string if it should be
    dropped.

    Four gates:
      - `source_description_id` must be in `edits_for` (R5).
      - The source must exist in the collection.
      - The source must not be is_question=True (answers, not edits,
        are the right response to questions).
      - The source must not already be SUPERSEDED (edits target the
        current head of a supersession chain; a stale source would
        silently produce an orphan successor).
    """
    if raw.source_description_id not in edits_for:
        return (
            f"source_description_id {raw.source_description_id!r} is "
            f"outside the declared edits_for scope"
        )
    source = next(
        (d for d in descriptions if d.id == raw.source_description_id),
        None,
    )
    if source is None:
        return (
            f"source_description_id {raw.source_description_id!r} does "
            f"not resolve to any known description"
        )
    if source.is_question:
        return (
            f"description {raw.source_description_id!r} is a question "
            f"(is_question=True); questions take answers, not edits"
        )
    if source.status == DescStatus.SUPERSEDED:
        return (
            f"description {raw.source_description_id!r} is already "
            f"SUPERSEDED; edits must target the current head"
        )
    return None


def _translate_edit(
    raw: ReaderEdit,
    descriptions: list,
    reviewer_id: str,
    current_τ_a: int,
) -> EditProposal:
    """One accepted ReaderEdit → one EditProposal. Caller must have
    already passed the edit through _classify_edit and seen None;
    this function assumes the source resolves and is edit-eligible.

    The proposed new description inherits the source's anchor, branches,
    and **metadata** (an edit that changes anchoring is a different
    operation; re-anchoring is out of scope for this iteration).
    Preserving source metadata is load-bearing: if an answer description
    (carrying metadata["answers_question"]) is later edited, the
    replacement must keep the question link, or the answer becomes an
    orphan. Kind defaults to the source's kind when `new_kind` is
    omitted; attention is preserved from the source. The new record
    starts PROVISIONAL and flips to COMMITTED at accept time;
    `metadata["supersedes"]` is layered on by accept_edit_proposal.
    """
    source = next(d for d in descriptions if d.id == raw.source_description_id)
    safe_reviewer = reviewer_id.replace(":", "_")
    new_id = f"{source.id}_edit_by_{safe_reviewer}_τ_a_{current_τ_a}"
    new_kind = raw.new_kind if raw.new_kind is not None else source.kind
    new_desc = Description(
        id=new_id,
        attached_to=source.attached_to,
        kind=new_kind,
        attention=source.attention,
        text=raw.new_text,
        authored_by=reviewer_id,
        τ_a=current_τ_a,
        is_question=False,
        branches=source.branches,
        status=DescStatus.PROVISIONAL,
        # Inherit source metadata; accept_edit_proposal layers
        # `supersedes` on top. Copy the dict so mutating the new
        # description's metadata can't bleed into the source's.
        metadata=dict(source.metadata),
    )
    return EditProposal(
        source_description_id=source.id,
        proposed_description=new_desc,
        proposer_id=reviewer_id,
        rationale=raw.rationale,
        proposed_at_τ_a=current_τ_a,
    )


def _translate_answer(
    raw: ReaderAnswer,
    descriptions: list,
    reviewer_id: str,
    current_τ_a: int,
) -> AnswerProposal:
    """One accepted ReaderAnswer → one AnswerProposal. Caller must have
    already passed the answer through _classify_answer and seen None
    (accepted); this function assumes the target is a valid question."""
    question = next(d for d in descriptions if d.id == raw.question_description_id)
    safe_reviewer = reviewer_id.replace(":", "_")
    new_id = (
        f"{raw.question_description_id}_answer_"
        f"by_{safe_reviewer}_τ_a_{current_τ_a}"
    )
    new_desc = Description(
        id=new_id,
        attached_to=question.attached_to,
        kind=raw.answer_kind,
        attention=Attention.INTERPRETIVE,
        text=raw.answer_text,
        authored_by=reviewer_id,
        τ_a=current_τ_a,
        branches=question.branches,
        status=DescStatus.PROVISIONAL,
        metadata={"answers_question": raw.question_description_id},
    )
    return AnswerProposal(
        question_description_id=raw.question_description_id,
        proposed_description=new_desc,
        proposer_id=reviewer_id,
        rationale=raw.rationale,
        proposed_at_τ_a=current_τ_a,
    )


# ============================================================================
# Entry point
# ============================================================================


def invoke_reader_model(
    view: ReaderView,
    events: list,
    descriptions: list,
    current_τ_a: int,
    *,
    reviews_for: Optional[list[str]] = None,
    answers_for: Optional[list[str]] = None,
    edits_for: Optional[list[str]] = None,
    model: str = "claude-opus-4-6",
    reviewer_id: Optional[str] = None,
    effort: str = "high",
    max_tokens: int = 16_000,
    dry_run: bool = False,
    client: Optional["anthropic.Anthropic"] = None,
) -> ReaderModelResult:
    """Invoke the reader-model on a `ReaderView`.

    Args:
        view: the ReaderView to evaluate (from `substrate.reader_view`).
        events: the full events list (needed to resolve event anchors).
        descriptions: the full descriptions list (needed for description
            anchors and for translating LLM output back into substrate
            records).
        current_τ_a: authored-time stamp placed on all produced records.
            The caller picks it; typical choice is "next τ_a after the
            last commit", whatever the authoring workflow decides.
        reviews_for: ids of descriptions to review. Default: all
            descriptions in the view. Pass `[]` to skip reviews.
        answers_for: ids of is_question descriptions to answer. Default:
            all open_questions in the view. Pass `[]` to skip answers.
        edits_for: ids of descriptions the LLM may propose edits for.
            Default: every non-question description in the view.
            Pass `[]` to forbid edits. Edits are only proposed where
            a review's rationale names a concrete revision; an empty
            `edits` list is the common case, not an error.
        model: Claude model id. Default claude-opus-4-6.
        reviewer_id: stamped on produced records. Default "llm:<model>".
        effort: "low" | "medium" | "high" | "max". Default "high" — this
            is interpretive work where quality matters.
        max_tokens: response cap. Default 16000 (non-streaming).
        dry_run: if True, return an empty result after printing the
            full prompt. No API call, no API key needed.
        client: optional pre-configured `anthropic.Anthropic` instance.
            Default: construct one from env (`ANTHROPIC_API_KEY`).

    Returns:
        A `ReaderModelResult` containing:
          - `review_candidates`: list[tuple[str, ReviewEntry]] — each
            tuple is (target_description_id, translated review). Pass
            directly to `proposal_walker.walk_reviews`, or invoke
            `substrate.ingest_review(description, review)` yourself
            against the named target.
          - `answer_proposals`: list[AnswerProposal] queue-ready via
            `substrate.ingest_question_answer`; the author accepts or
            declines via `substrate.accept_answer_proposal` /
            `substrate.decline_proposal`.
          - `edit_proposals`: list[EditProposal] queue-ready via
            `substrate.ingest_edit_proposal`; the author accepts or
            declines via `substrate.accept_edit_proposal` /
            `substrate.decline_proposal`.
          - `raw_output`: the pre-translation ReaderOutput for
            debugging.
    """
    if reviewer_id is None:
        reviewer_id = f"llm:{model}"
    if reviews_for is None:
        reviews_for = [r.description.id for r in view.descriptions]
    if answers_for is None:
        answers_for = [r.description.id for r in view.open_questions]
    if edits_for is None:
        # Default edits scope is every non-question description in the
        # view — the same population the reviews target, minus the
        # questions (which take answers rather than edits).
        edits_for = [
            r.description.id for r in view.descriptions
            if not r.description.is_question
        ]

    user_prompt = build_user_prompt(
        view, events, descriptions, reviews_for, answers_for, edits_for
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
        return ReaderModelResult(
            review_candidates=[],
            answer_proposals=[],
            edit_proposals=[],
            dropped=[],
            raw_output=ReaderOutput(),
        )

    if client is None:
        client = anthropic.Anthropic()

    # `parse()` doesn't accept top-level cache_control. Put the directive
    # on the system block itself — this caches the system prompt (the
    # frozen prefix) across calls, which is what we wanted anyway.
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
        output_format=ReaderOutput,
    )

    raw: ReaderOutput = response.parsed_output

    review_candidates: list = []
    answer_proposals: list = []
    edit_proposals: list = []
    dropped: list = []

    for rr in raw.reviews:
        reason = _classify_review(rr, descriptions, reviews_for)
        if reason is not None:
            dropped.append(DroppedOutput(reason=reason, raw=rr))
            continue
        # Keep the target_id paired with the translated record at the
        # moment of translation. Parallel-zipping raw.reviews with a
        # filtered `reviews` list misaligns when any raw record was
        # dropped at the validation gate; the pair is authoritative.
        entry = _translate_review(
            rr, descriptions, events, reviewer_id, current_τ_a
        )
        review_candidates.append((rr.description_id, entry))

    for ra in raw.answers:
        reason = _classify_answer(ra, descriptions, answers_for)
        if reason is not None:
            dropped.append(DroppedOutput(reason=reason, raw=ra))
            continue
        answer_proposals.append(
            _translate_answer(ra, descriptions, reviewer_id, current_τ_a)
        )

    for re in raw.edits:
        reason = _classify_edit(re, descriptions, edits_for)
        if reason is not None:
            dropped.append(DroppedOutput(reason=reason, raw=re))
            continue
        edit_proposals.append(
            _translate_edit(re, descriptions, reviewer_id, current_τ_a)
        )

    return ReaderModelResult(
        review_candidates=review_candidates,
        answer_proposals=answer_proposals,
        edit_proposals=edit_proposals,
        dropped=dropped,
        raw_output=raw,
    )
