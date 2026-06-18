"""
authoring_interview.py — the AI-interview authoring front-end.

`authoring.py` compiles a `.story.toml` (a plain dict) into the verified
substrate. This module makes producing that dict a CONVERSATION instead of a
form: an AI interviewer elicits the story and extracts the authoring dict, and
the dict's gaps — the very commitments the compiler and the Aristotelian
overlay require — become the interview's next questions.

Two halves, by design:

- `interview_gaps(doc)` — the SPINE. Pure, deterministic, standard-library.
  Given the authoring dict, it reports what is missing or under-committed, each
  as a human-facing question with a severity:
    * "blocking"   — `authoring.compile_story` would refuse (no title, an event
      with no `when`, an unphased beat, a participant who is not a declared
      character, …);
    * "structural" — the Aristotelian homework the engine wants but tolerates
      missing (no peripeteia marked, an anagnorisis with no recognizer, a
      tragic-hero with no hamartia, no pathos-centre).
  This is the conceptual heart and it needs no model — it is the substrate's
  demands, enumerated and phrased as questions.

- `extract_story_draft(...)` — the LLM half (pydantic, imported lazily so the
  spine stays dependency-free): turn a natural brief + answers into / merge
  into the authoring dict.

The loop (see `demos/author_by_interview.py`): extract → ask the top gaps →
extract again → until no blocking gaps remain → `compile_story` →
`verify_compiled` → generate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# ============================================================================
# The spine — deterministic gap analysis (no API, no dependencies)
# ============================================================================

@dataclass(frozen=True)
class Gap:
    """One missing or under-committed thing in the authoring dict, phrased as
    a question. `severity` is 'blocking' (compile would refuse) or
    'structural' (Aristotelian homework, tolerated if declined)."""
    severity: str
    code: str
    question: str
    target: str = ""        # the event/character id the gap concerns, if any


_TELLINGS = ("chronological", "reverse", "explicit")


def _label(ev: dict) -> str:
    return (ev.get("summary") or ev.get("id") or "an unnamed beat").strip()


def interview_gaps(doc: dict) -> list:
    """Enumerate the authoring dict's gaps as questions, blocking first.
    Pure — the same demands `authoring.compile_story` and the Aristotelian
    overlay enforce, turned to face the author."""
    gaps: list = []
    chars = doc.get("characters") or []
    events = doc.get("events") or []
    places = doc.get("places") or []
    valid_ids = ({c.get("id") for c in chars if c.get("id")}
                 | {p.get("id") for p in places if p.get("id")})

    # ---- blocking: compile_story would raise ----
    if not (doc.get("title") or "").strip():
        gaps.append(Gap("blocking", "no_title",
                        "What's the title of the story?"))
    if not chars:
        gaps.append(Gap("blocking", "no_characters",
                        "Who are the people in this story? Name at least one."))
    if not events:
        gaps.append(Gap("blocking", "no_events",
                        "What happens? Walk me through the key beats."))

    for c in chars:
        if not (c.get("id") or "").strip():
            gaps.append(Gap("blocking", "char_no_id",
                            f"The character \"{c.get('name', '?')}\" needs a "
                            f"short id (a one-word handle).",
                            c.get("name", "")))

    seen_ids: set = set()
    for ev in events:
        eid = (ev.get("id") or "").strip()
        if not eid:
            gaps.append(Gap("blocking", "event_no_id",
                            f"The beat \"{_label(ev)}\" needs a short id."))
            continue
        if eid in seen_ids:
            gaps.append(Gap("blocking", "event_dup_id",
                            f"Two beats share the id '{eid}'.", eid))
        seen_ids.add(eid)
        if ev.get("when") is None:
            gaps.append(Gap("blocking", "event_no_when",
                            f"When does \"{_label(ev)}\" happen, in story-time "
                            f"order relative to the others?", eid))
        for w in ev.get("who") or []:
            if w not in valid_ids:
                gaps.append(Gap("blocking", "event_unknown_who",
                                f"The beat \"{_label(ev)}\" involves '{w}', "
                                f"but no such character or place is declared — "
                                f"add them?", eid))
        if not (ev.get("summary") or "").strip():
            gaps.append(Gap("structural", "event_no_summary",
                            f"What actually happens in the beat '{eid}'?", eid))

    telling = (doc.get("telling") or "chronological").strip().lower()
    if telling not in _TELLINGS:
        gaps.append(Gap("blocking", "bad_telling",
                        f"The telling order '{telling}' must be one of: "
                        f"chronological, reverse, explicit."))
    elif telling == "explicit" and not doc.get("staging"):
        gaps.append(Gap("blocking", "explicit_no_staging",
                        "You chose an explicit telling order — in what order "
                        "does the audience experience the beats?"))

    phases = doc.get("phases") or {}
    phased: set = set()
    for key in ("beginning", "middle", "end"):
        phased.update(phases.get(key) or [])
    if not phased:
        gaps.append(Gap("blocking", "no_phases",
                        "How do the beats fall into a beginning, a middle, and "
                        "an end?"))
    else:
        unphased = seen_ids - phased
        if unphased:
            gaps.append(Gap("blocking", "unphased_events",
                            f"These beats aren't placed in a phase yet: "
                            f"{', '.join(sorted(unphased))}. Beginning, "
                            f"middle, or end?"))

    # recognizer / anti-recognition referential integrity (blocking-ish)
    for ev in events:
        rec = (ev.get("recognizer") or "").strip()
        if rec and rec not in valid_ids:
            gaps.append(Gap("blocking", "recognizer_unknown",
                            f"The recognizer '{rec}' isn't a declared "
                            f"character — who is it?", ev.get("id", "")))

    # ---- structural: the Aristotelian homework ----
    marks = [ev.get("mark") for ev in events]
    if events and "peripeteia" not in marks:
        gaps.append(Gap("structural", "no_peripeteia",
                        "Which beat is the turn — the reversal of fortune "
                        "(peripeteia)?"))
    if events and "anagnorisis" not in marks:
        gaps.append(Gap("structural", "no_anagnorisis",
                        "Is there a moment of recognition — a character coming "
                        "to a truth (often too late)? Which beat?"))
    for ev in events:
        if ev.get("mark") == "anagnorisis" and not (ev.get("recognizer") or "").strip():
            gaps.append(Gap("structural", "anag_no_recognizer",
                            f"At the recognition \"{_label(ev)}\", who comes to "
                            f"the knowledge?", ev.get("id", "")))

    roles = [(c.get("role") or "figure").strip().lower() for c in chars]
    if chars and "tragic-hero" not in roles:
        gaps.append(Gap("structural", "no_hero",
                        "Who is the tragic hero — whose fall does the story "
                        "follow?"))
    if chars and "pathos-centre" not in roles:
        gaps.append(Gap("structural", "no_pathos",
                        "Where does the story's pity centre — is the hero also "
                        "its heart, or is it someone else (a victim, a loved "
                        "one)?"))
    for c in chars:
        if (c.get("role") or "").strip().lower() == "tragic-hero" \
                and not (c.get("hamartia") or "").strip():
            gaps.append(Gap("structural", "hero_no_hamartia",
                            f"What is {c.get('name', c.get('id'))}'s tragic "
                            f"flaw (hamartia) — the trait that undoes them?",
                            c.get("id", "")))
    if len(events) == 1:
        gaps.append(Gap("structural", "too_few_events",
                        "A story usually turns on several beats — what happens "
                        "before and after this one?"))

    return gaps


def blocking_gaps(doc: dict) -> list:
    return [g for g in interview_gaps(doc) if g.severity == "blocking"]


def structural_gaps(doc: dict) -> list:
    return [g for g in interview_gaps(doc) if g.severity == "structural"]


def is_compilable(doc: dict) -> bool:
    """True when no blocking gap remains — `compile_story` should succeed."""
    return not blocking_gaps(doc)


def next_questions(doc: dict, *, n: int = 3, include_structural: bool = True):
    """The next questions to put to the author: all blocking gaps first
    (compilation is gated on them), then structural ones, capped at `n`."""
    gaps = blocking_gaps(doc)
    if include_structural:
        gaps = gaps + structural_gaps(doc)
    return [g.question for g in gaps[:n]]


# ============================================================================
# The LLM half — extract / merge the authoring dict from natural input
# ============================================================================

_SYSTEM_PROMPT = """\
You are a story-structure interviewer for a generation engine. The engine needs
a story expressed as a precise authoring record it can verify and render. Your
job is to turn the author's natural description (and their answers to follow-up
questions) into that record — committing to concrete structural facts, never
inventing content the author has not implied.

The record's shape:
- title, logline; telling ("chronological" | "reverse" | "explicit").
- characters: each has a short id, a name, a role ("tragic-hero" |
  "pathos-centre" | "figure"), and (for a tragic-hero) a hamartia.
- events (the beats): each has a short id, a `when` integer (story-time order),
  the participant ids in `who`, a `summary` of the beat, optionally a `mark`
  ("peripeteia" | "anagnorisis"), a `recognizer` (on an anagnorisis), and a
  `focalizer`.
- phases: which event ids are in the beginning, the middle, the end (every
  event must be placed in exactly one).

Commit to ids that are short lowercase handles. Use integer `when` values to
fix story-time order. If the author has not supplied something, leave it absent
rather than fabricating — the interview will ask for it next. Carry forward
everything already established in the prior record.
"""


def extract_story_draft(
    brief: str,
    *,
    prior: Optional[dict] = None,
    answers: Optional[str] = None,
    model: str = "claude-opus-4-6",
    effort: str = "high",
    max_tokens: int = 6000,
    dry_run: bool = False,
    client=None,
) -> Optional[dict]:
    """Turn a natural brief (plus the prior draft and the author's latest
    answers) into the authoring dict. Returns the dict, or None on dry_run.

    Pydantic is imported here, lazily, so `interview_gaps` and the rest of the
    spine stay standard-library and offline-testable."""
    from pydantic import BaseModel, Field
    from story_engine.core.reader_model_client_base import invoke_parse_helper

    class CharacterDraft(BaseModel):
        id: str = Field(description="short lowercase handle")
        name: str = ""
        role: str = Field(default="figure",
                          description="tragic-hero | pathos-centre | figure")
        hamartia: str = ""

    class EventDraft(BaseModel):
        id: str = Field(description="short lowercase handle")
        when: Optional[int] = Field(
            default=None, description="story-time order, integer")
        who: list[str] = Field(default_factory=list,
                               description="participant character/place ids")
        summary: str = ""
        mark: str = Field(default="",
                          description="'peripeteia' | 'anagnorisis' | ''")
        recognizer: str = Field(default="",
                                description="character id, on an anagnorisis")
        focalizer: str = ""

    class PhasesDraft(BaseModel):
        beginning: list[str] = Field(default_factory=list)
        middle: list[str] = Field(default_factory=list)
        end: list[str] = Field(default_factory=list)

    class StoryDraft(BaseModel):
        title: str = ""
        logline: str = ""
        telling: str = "chronological"
        characters: list[CharacterDraft] = Field(default_factory=list)
        events: list[EventDraft] = Field(default_factory=list)
        phases: PhasesDraft = Field(default_factory=PhasesDraft)

    import json
    parts = [f"Author's brief:\n{brief}"]
    if prior:
        parts.append("Record so far (carry all of this forward, refine it):\n"
                     + json.dumps(prior, indent=1))
    if answers:
        parts.append(f"Author's latest answers to your questions:\n{answers}")
    parts.append("Produce the complete, updated authoring record.")
    user_prompt = "\n\n".join(parts)

    draft = invoke_parse_helper(
        system_prompt=_SYSTEM_PROMPT, user_prompt=user_prompt,
        output_format=StoryDraft, model=model, max_tokens=max_tokens,
        effort=effort, dry_run=dry_run, client=client,
    )
    if draft is None:
        return None
    doc = draft.model_dump()
    # Drop empty optionals so the dict reads like a hand-authored .story.toml
    # (and so `interview_gaps` sees genuine absence, not empty strings).
    for c in doc.get("characters", []):
        if not c.get("hamartia"):
            c.pop("hamartia", None)
    for ev in doc.get("events", []):
        for k in ("mark", "recognizer", "focalizer"):
            if not ev.get(k):
                ev.pop(k, None)
    return doc
