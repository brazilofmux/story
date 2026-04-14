"""
proposal_walker.py — interactive walker over reader-model output.

Tooling, not substrate. The substrate produces `ReviewEntry` and
`AnswerProposal` records; this module lets an author walk through those
records one at a time and accept / decline / skip / quit, routing
accepted outputs to `substrate.ingest_review` and
`substrate.accept_answer_proposal` (or `decline_proposal`).

Reader-model-sketch-01 R3 (partner-not-fallback) says reader-model
outputs never mutate substrate state directly: accepted outputs produce
new reviews or new descriptions via authorial act. The walker *is* that
authorial act — for each record, the author explicitly decides, and the
walker invokes the substrate's ingest/accept/decline functions on the
author's behalf.

The walker is stream-based (takes `stdin` / `stdout`) so tests can drive
it with `io.StringIO` without a terminal. Default streams are
`sys.stdin` / `sys.stdout`.

Scope of this iteration:
- Walks reviews (as (target_id, ReviewEntry) candidates).
- Walks AnswerProposal queue entries.
- Does NOT walk PromotionProposal queue entries (fact-proposal
  acceptance has no concrete effect path yet; the LLM probe doesn't
  emit fact proposals so there's nothing to walk).
- No persistence. Decisions live only for the duration of the walk;
  persistence is deferred per descriptions-sketch-01 OQ3.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Optional

from substrate import (
    AnswerProposal,
    Description,
    EditProposal,
    ReviewEntry,
    accept_answer_proposal,
    accept_edit_proposal,
    decline_proposal,
    ingest_review,
)


# ----------------------------------------------------------------------------
# Decision records
# ----------------------------------------------------------------------------


@dataclass(frozen=True)
class Decision:
    """One walker decision. `kind` is "review", "answer-proposal", or
    "edit-proposal"; `target_id` identifies the record (description id
    for reviews and edits, question id for answer proposals);
    `choice` is one of "accept" / "decline" / "skip" / "quit".
    """
    kind: str
    target_id: str
    choice: str


def _prompt(stdin, stdout, prompt_text: str) -> str:
    """Read a single non-empty line from stdin, trimmed. Returns "" on
    EOF (which callers treat as quit)."""
    stdout.write(prompt_text)
    stdout.flush()
    line = stdin.readline()
    if line == "":  # EOF
        return ""
    return line.strip()


def _read_choice(stdin, stdout, prompt_text: str) -> str:
    """Prompt the author until they type a valid choice character.
    Returns one of "a" / "d" / "s" / "q". EOF is treated as "q".

    We keep re-prompting on unrecognized input rather than defaulting,
    since every decision lands in substrate state — silent defaulting
    would be a foot-gun."""
    while True:
        raw = _prompt(stdin, stdout, prompt_text)
        if raw == "":
            return "q"
        ch = raw[0].lower()
        if ch in ("a", "d", "s", "q"):
            return ch
        stdout.write(
            f"  (unrecognized input {raw!r}; "
            f"type a / d / s / q)\n"
        )


# ----------------------------------------------------------------------------
# Presentation helpers
# ----------------------------------------------------------------------------


def _rule(stdout, title: str) -> None:
    stdout.write("\n")
    stdout.write("-" * 72)
    stdout.write("\n")
    stdout.write(title)
    stdout.write("\n")
    stdout.write("-" * 72)
    stdout.write("\n")


def _indent(text: str, prefix: str = "    ") -> str:
    lines = text.splitlines() or [""]
    return "\n".join(prefix + line for line in lines)


def _render_review(
    stdout,
    target: Description,
    review: ReviewEntry,
) -> None:
    stdout.write(f"description: {target.id}\n")
    stdout.write(f"  kind:       {target.kind}\n")
    stdout.write(f"  attention:  {target.attention.value}\n")
    stdout.write(f"  text:\n")
    stdout.write(_indent(target.text) + "\n")
    stdout.write(f"\nreviewer:  {review.reviewer_id}\n")
    stdout.write(f"  verdict:   {review.verdict.value}\n")
    stdout.write(f"  anchor_τ_a: {review.anchor_τ_a}\n")
    if review.comment:
        stdout.write(f"  comment:\n")
        stdout.write(_indent(review.comment) + "\n")


def _render_edit_proposal(
    stdout,
    proposal: EditProposal,
    source: Optional[Description],
) -> None:
    stdout.write(f"edit source: {proposal.source_description_id}\n")
    d_new = proposal.proposed_description
    if source is not None:
        stdout.write(f"  current kind:       {source.kind}\n")
        stdout.write(f"  current attention:  {source.attention.value}\n")
        stdout.write(f"  current text:\n")
        stdout.write(_indent(source.text) + "\n")
    else:
        stdout.write(f"  (source description not found in current collection)\n")
    stdout.write(f"\nproposed id:     {d_new.id}\n")
    stdout.write(f"  proposed kind: {d_new.kind}")
    if source is not None and d_new.kind != source.kind:
        stdout.write(f"   (changed from {source.kind})")
    stdout.write("\n")
    stdout.write(f"  author:        {d_new.authored_by}\n")
    stdout.write(f"  new text:\n")
    stdout.write(_indent(d_new.text) + "\n")
    if proposal.rationale:
        stdout.write(f"\nrationale:\n")
        stdout.write(_indent(proposal.rationale) + "\n")


def _render_answer_proposal(
    stdout,
    proposal: AnswerProposal,
    question: Optional[Description],
) -> None:
    stdout.write(f"answers question: {proposal.question_description_id}\n")
    if question is not None:
        stdout.write(_indent(f"question text: {question.text}") + "\n")
    d = proposal.proposed_description
    stdout.write(f"\nproposed description: {d.id}\n")
    stdout.write(f"  kind:       {d.kind}\n")
    stdout.write(f"  attention:  {d.attention.value}\n")
    stdout.write(f"  attached_to: {d.attached_to.kind}:{d.attached_to.target_id}\n")
    stdout.write(f"  author:     {d.authored_by}\n")
    stdout.write(f"  status:     {d.status.value} (would flip to committed on accept)\n")
    stdout.write(f"  text:\n")
    stdout.write(_indent(d.text) + "\n")
    if proposal.rationale:
        stdout.write(f"\nrationale:\n")
        stdout.write(_indent(proposal.rationale) + "\n")


# ----------------------------------------------------------------------------
# Walkers
# ----------------------------------------------------------------------------


_CHOICE_PROMPT = "  [a]ccept  [d]ecline  [s]kip  [q]uit  > "


def walk_reviews(
    candidates: list,
    descriptions: list,
    *,
    stdin=None,
    stdout=None,
) -> tuple:
    """Walk LLM review candidates. `candidates` is a list of
    (target_description_id, ReviewEntry) pairs.

    For each pair, the author sees the target description + the LLM's
    review and chooses accept / decline / skip / quit.

    Accept calls `ingest_review` and replaces the description in
    `descriptions` by id. Decline and skip leave state unchanged.
    Quit stops the walk early.

    Returns (new_descriptions, decisions).
    """
    if stdin is None:
        stdin = sys.stdin
    if stdout is None:
        stdout = sys.stdout

    working = list(descriptions)
    decisions: list = []

    total = len(candidates)
    if total == 0:
        stdout.write("\n(no reviews to walk)\n")
        return working, decisions

    stdout.write(f"\n=== walking {total} review candidate(s) ===\n")

    for i, (target_id, review) in enumerate(candidates, start=1):
        target = next((d for d in working if d.id == target_id), None)
        if target is None:
            stdout.write(
                f"\n[review {i}/{total}] target id {target_id!r} not found "
                f"in descriptions; skipping.\n"
            )
            decisions.append(Decision("review", target_id, "skip"))
            continue

        _rule(stdout, f"[review {i}/{total}]")
        _render_review(stdout, target, review)
        choice = _read_choice(stdin, stdout, _CHOICE_PROMPT)

        if choice == "q":
            decisions.append(Decision("review", target_id, "quit"))
            stdout.write("\n(quit; remaining reviews skipped)\n")
            break
        if choice == "a":
            updated = ingest_review(target, review)
            working = [updated if d.id == target_id else d for d in working]
            decisions.append(Decision("review", target_id, "accept"))
            stdout.write(f"  accepted — review appended to {target_id}\n")
        elif choice == "d":
            decisions.append(Decision("review", target_id, "decline"))
            stdout.write(f"  declined — review dropped\n")
        else:  # "s"
            decisions.append(Decision("review", target_id, "skip"))
            stdout.write(f"  skipped\n")

    return working, decisions


def walk_edit_proposals(
    queue: list,
    descriptions: list,
    *,
    stdin=None,
    stdout=None,
) -> tuple:
    """Walk pending EditProposal entries in `queue`. Non-EditProposal
    entries (PromotionProposal, AnswerProposal) and non-pending entries
    are left untouched and not shown.

    For each pending EditProposal, the author sees the source
    description's current text + the proposed replacement text +
    rationale, and chooses accept / decline / skip / quit.

    Accept calls `accept_edit_proposal`, appending a committed new
    description and marking the source SUPERSEDED. Decline flips the
    queue entry's status to declined. Skip leaves it pending. Quit
    stops the walk early.

    Returns (new_descriptions, new_queue, decisions).
    """
    if stdin is None:
        stdin = sys.stdin
    if stdout is None:
        stdout = sys.stdout

    working_desc = list(descriptions)
    working_queue = list(queue)
    decisions: list = []

    pending_indices = [
        i for i, entry in enumerate(working_queue)
        if isinstance(entry, EditProposal) and entry.status == "pending"
    ]
    total = len(pending_indices)

    if total == 0:
        stdout.write("\n(no pending edit proposals to walk)\n")
        return working_desc, working_queue, decisions

    stdout.write(f"\n=== walking {total} pending edit proposal(s) ===\n")

    for step, idx in enumerate(pending_indices, start=1):
        entry = working_queue[idx]
        source_id = entry.source_description_id
        source = next(
            (d for d in working_desc if d.id == source_id),
            None,
        )

        _rule(stdout, f"[edit proposal {step}/{total}]")
        _render_edit_proposal(stdout, entry, source)
        choice = _read_choice(stdin, stdout, _CHOICE_PROMPT)

        if choice == "q":
            decisions.append(Decision("edit-proposal", source_id, "quit"))
            stdout.write("\n(quit; remaining proposals skipped)\n")
            break
        if choice == "a":
            working_desc, working_queue = accept_edit_proposal(
                entry, working_desc, working_queue,
            )
            decisions.append(Decision("edit-proposal", source_id, "accept"))
            new_id = entry.proposed_description.id
            stdout.write(
                f"  accepted — {source_id} superseded; {new_id} "
                f"committed (queue entry marked accepted)\n"
            )
        elif choice == "d":
            working_queue = decline_proposal(entry, working_queue)
            decisions.append(Decision("edit-proposal", source_id, "decline"))
            stdout.write(f"  declined — source description unchanged\n")
        else:  # "s"
            decisions.append(Decision("edit-proposal", source_id, "skip"))
            stdout.write(f"  skipped — queue entry left pending\n")

    return working_desc, working_queue, decisions


def walk_answer_proposals(
    queue: list,
    descriptions: list,
    *,
    stdin=None,
    stdout=None,
) -> tuple:
    """Walk pending AnswerProposal entries in `queue`. Non-AnswerProposal
    entries (e.g. PromotionProposal) and non-pending entries are left
    untouched and not shown.

    For each pending AnswerProposal, the author sees the target question
    + the proposed answer description and chooses accept / decline /
    skip / quit.

    Accept calls `accept_answer_proposal`, appending a committed copy of
    the proposed description to `descriptions` and flipping the queue
    entry's status to accepted. Decline calls `decline_proposal`,
    flipping the status to declined. Skip and quit leave state
    unchanged.

    Returns (new_descriptions, new_queue, decisions).
    """
    if stdin is None:
        stdin = sys.stdin
    if stdout is None:
        stdout = sys.stdout

    working_desc = list(descriptions)
    working_queue = list(queue)
    decisions: list = []

    # Snapshot the pending-proposal indices at walk start. accept/decline
    # replace entries at these indices in place (queue length unchanged),
    # so the indices remain stable for the duration of the walk.
    pending_indices = [
        i for i, entry in enumerate(working_queue)
        if isinstance(entry, AnswerProposal) and entry.status == "pending"
    ]
    total = len(pending_indices)

    if total == 0:
        stdout.write("\n(no pending answer proposals to walk)\n")
        return working_desc, working_queue, decisions

    stdout.write(f"\n=== walking {total} pending answer proposal(s) ===\n")

    for step, idx in enumerate(pending_indices, start=1):
        entry = working_queue[idx]
        q_id = entry.question_description_id
        question = next(
            (d for d in working_desc if d.id == q_id),
            None,
        )

        _rule(stdout, f"[answer proposal {step}/{total}]")
        _render_answer_proposal(stdout, entry, question)
        choice = _read_choice(stdin, stdout, _CHOICE_PROMPT)

        if choice == "q":
            decisions.append(Decision("answer-proposal", q_id, "quit"))
            stdout.write("\n(quit; remaining proposals skipped)\n")
            break
        if choice == "a":
            working_desc, working_queue = accept_answer_proposal(
                entry, working_desc, working_queue,
            )
            decisions.append(Decision("answer-proposal", q_id, "accept"))
            new_id = entry.proposed_description.id
            stdout.write(
                f"  accepted — {new_id} committed to descriptions "
                f"(queue entry marked accepted)\n"
            )
        elif choice == "d":
            working_queue = decline_proposal(entry, working_queue)
            decisions.append(Decision("answer-proposal", q_id, "decline"))
            stdout.write(f"  declined — queue entry marked declined\n")
        else:  # "s"
            decisions.append(Decision("answer-proposal", q_id, "skip"))
            stdout.write(f"  skipped — queue entry left pending\n")

    return working_desc, working_queue, decisions


# ----------------------------------------------------------------------------
# Convenience
# ----------------------------------------------------------------------------


def summarize_decisions(decisions: list) -> dict:
    """Group decisions by (kind, choice) and return counts."""
    counts: dict = {}
    for d in decisions:
        key = (d.kind, d.choice)
        counts[key] = counts.get(key, 0) + 1
    return counts


def print_decision_summary(decisions: list, stdout=None) -> None:
    """Human-readable summary, suitable for end-of-walk recap."""
    if stdout is None:
        stdout = sys.stdout
    counts = summarize_decisions(decisions)
    if not counts:
        stdout.write("\n(no decisions recorded)\n")
        return
    stdout.write("\n=== decision summary ===\n")
    for (kind, choice), n in sorted(counts.items()):
        stdout.write(f"  {kind:<18} {choice:<10} {n}\n")
