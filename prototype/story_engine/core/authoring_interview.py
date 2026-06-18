"""
authoring_interview.py — the AI-interview authoring front-end.

`authoring.py` compiles a `.story.toml` (a plain dict) into the verified
substrate. This module makes producing that dict a CONVERSATION instead of a
form: an AI interviewer elicits the story and extracts the authoring dict, and
the dict's gaps — the very commitments the compiler and the chosen dialect's
overlay require — become the interview's next questions.

Two halves, by design:

- `interview_gaps(doc, dialect=...)` — the SPINE. Pure, deterministic,
  standard-library. Given the authoring dict it reports what is missing or
  under-committed, each as a human-facing question with a severity:
    * "blocking"   — `authoring.compile_story` would refuse (no title, an event
      with no `when`, an unphased beat, a participant who is not a declared
      character, …). These are the dialect-agnostic SKELETON the substrate
      (entities · fabula · sjuzhet · phases) needs regardless of overlay;
    * "structural" — the dialect's homework: the commitments its self-verifier
      wants but tolerates missing. This is now PER-DIALECT — Aristotelian
      (peripeteia, anagnorisis, hamartia, pathos), Save-the-Cat (theme, genre,
      the fifteen beats, a protagonist), Dramatica (four throughlines, four
      domains, the eight dynamics, goal/consequence), Dramatic (arguments,
      stakes, a main-character throughline). Each overlay mirrors its dialect
      verifier's vocabulary, turned around to face the author.
  This is the conceptual heart and it needs no model — it is the substrate's
  and the dialect's demands, enumerated and phrased as questions.

- `extract_story_draft(brief, dialect=..., ...)` — the LLM half (pydantic,
  imported lazily so the spine stays dependency-free): turn a natural brief +
  answers into / merge into the authoring dict, with a per-dialect schema and
  system prompt so the model fills the right overlay's fields.

The loop (see `demos/author_by_interview.py`): extract → ask the top gaps →
extract again → until no blocking gap remains → `compile_story` →
`verify_compiled` → generate.

Scope honesty: `compile_story` lands the substrate skeleton + the Aristotelian
overlay (the live TOML compiler). The other three dialects' structural homework
is now elicited and gap-checked here — matching where the rest of the stack is
(generate · evaluate · repair · converge for all four) — and their authoring
record is verified by the existing per-dialect encodings; a TOML→non-Aristotelian
compiler is the remaining, named seam.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional


# ============================================================================
# The spine — deterministic gap analysis (no API, no dependencies)
# ============================================================================

@dataclass(frozen=True)
class Gap:
    """One missing or under-committed thing in the authoring dict, phrased as
    a question. `severity` is 'blocking' (compile would refuse) or
    'structural' (dialect homework, tolerated if declined)."""
    severity: str
    code: str
    question: str
    target: str = ""        # the event/character id the gap concerns, if any


_TELLINGS = ("chronological", "reverse", "explicit")


def _label(ev: dict) -> str:
    return (ev.get("summary") or ev.get("id") or "an unnamed beat").strip()


def _valid_ids(doc: dict) -> set:
    """The declared character + place ids — the universe a `who`, an owner, or
    a recognizer may name."""
    chars = doc.get("characters") or []
    places = doc.get("places") or []
    return ({c.get("id") for c in chars if c.get("id")}
            | {p.get("id") for p in places if p.get("id")})


# ----------------------------------------------------------------------------
# The dialect-agnostic skeleton — what the substrate needs, any overlay
# ----------------------------------------------------------------------------

def _skeleton_gaps(doc: dict) -> list:
    """The gaps every dialect shares: the commitments `compile_story` needs to
    build entities · fabula · sjuzhet · phases at all, plus the two
    dialect-neutral structural nudges (a beat with no summary; a one-beat
    story). Overlay-specific homework lives in the dialect overlays."""
    gaps: list = []
    chars = doc.get("characters") or []
    events = doc.get("events") or []
    valid_ids = _valid_ids(doc)

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

    if len(events) == 1:
        gaps.append(Gap("structural", "too_few_events",
                        "A story usually turns on several beats — what happens "
                        "before and after this one?"))

    return gaps


# ============================================================================
# Dialect overlays — each dialect's structural homework, as gap rules
#
# The vocabularies below mirror the dialect verifiers (`aristotelian.verify`,
# `save_the_cat_evaluator`, `dramatica_evaluator`, `dramatic_evaluator`) and
# are kept in lockstep with them. An overlay reads the dialect-specific fields
# the author commits to and reports what its verifier would want.
# ============================================================================

# ---- Aristotelian ----------------------------------------------------------
ARISTOTELIAN_ROLES = ("tragic-hero", "pathos-centre", "figure")


def _aristotelian_overlay(doc: dict) -> list:
    gaps: list = []
    chars = doc.get("characters") or []
    events = doc.get("events") or []
    valid_ids = _valid_ids(doc)

    # recognizer referential integrity — blocking: the compiler refuses it.
    for ev in events:
        rec = (ev.get("recognizer") or "").strip()
        if rec and rec not in valid_ids:
            gaps.append(Gap("blocking", "recognizer_unknown",
                            f"The recognizer '{rec}' isn't a declared "
                            f"character — who is it?", ev.get("id", "")))

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
    return gaps


# ---- Save-the-Cat ----------------------------------------------------------
STC_CANONICAL_BEATS = (
    "Opening Image", "Theme Stated", "Set-Up", "Catalyst", "Debate",
    "Break Into Two", "B Story", "Fun and Games", "Midpoint",
    "Bad Guys Close In", "All Is Lost", "Dark Night of the Soul",
    "Break Into Three", "Finale", "Final Image",
)
# the beats that carry the structural skeleton — the ones the interview insists
# on; the atmospheric beats (Opening/Final Image, Theme Stated) are polish.
STC_LOAD_BEARING_BEATS = (
    "Catalyst", "Break Into Two", "Midpoint", "All Is Lost",
    "Break Into Three", "Finale",
)
STC_GENRES = (
    "monster-in-the-house", "golden-fleece", "out-of-the-bottle",
    "dude-with-a-problem", "rites-of-passage", "buddy-love", "whydunit",
    "fool-triumphant", "institutionalized", "superhero",
)
STC_ROLE_LABELS = (
    "protagonist", "antagonist", "love-interest", "mentor", "confidant",
    "ally", "narrator", "victim", "suspect", "threshold-guardian",
)


def _save_the_cat_overlay(doc: dict) -> list:
    gaps: list = []
    chars = doc.get("characters") or []
    events = doc.get("events") or []

    if not (doc.get("theme_statement") or "").strip():
        gaps.append(Gap("structural", "stc_no_theme",
                        "What is the theme — the one claim about life the story "
                        "argues (the 'Theme Stated' beat)?"))

    genre = (doc.get("genre") or "").strip().lower()
    if not genre:
        gaps.append(Gap("structural", "stc_no_genre",
                        "Which of the ten genres is this — monster-in-the-house, "
                        "golden-fleece, dude-with-a-problem, buddy-love, …?"))
    elif genre not in STC_GENRES:
        gaps.append(Gap("structural", "stc_unknown_genre",
                        f"'{genre}' isn't one of the ten Save-the-Cat genres."))

    roles = [(c.get("role") or "").strip().lower() for c in chars]
    if chars and "protagonist" not in roles:
        gaps.append(Gap("structural", "stc_no_protagonist",
                        "Who is the protagonist — the one whose transformation "
                        "the beats track?"))

    # beat coverage — each event may name a canonical beat via `beat`.
    assigned = {(ev.get("beat") or "").strip() for ev in events if (ev.get("beat") or "").strip()}
    for b in sorted(b for b in assigned if b not in STC_CANONICAL_BEATS):
        gaps.append(Gap("structural", "stc_unknown_beat",
                        f"'{b}' isn't one of the fifteen Save-the-Cat beats."))
    if events:
        missing = [b for b in STC_LOAD_BEARING_BEATS if b not in assigned]
        if missing:
            gaps.append(Gap("structural", "stc_unfilled_beats",
                            "These load-bearing beats aren't placed on any beat "
                            f"yet: {', '.join(missing)}. Which event is each?"))
    return gaps


# ---- Dramatica -------------------------------------------------------------
DRAMATICA_THROUGHLINES = (
    "overall-story", "main-character", "impact-character", "relationship",
)
DRAMATICA_DOMAINS = ("activity", "situation", "manipulation", "fixed-attitude")
DRAMATICA_DYNAMICS = {
    "resolve": ("change", "steadfast"),
    "growth": ("start", "stop"),
    "approach": ("do-er", "be-er"),
    "problem-solving-style": ("linear", "holistic"),
    "driver": ("action", "decision"),
    "limit": ("timelock", "optionlock"),
    "outcome": ("success", "failure"),
    "judgment": ("good", "bad"),
}


def _normalize_dynamics(raw) -> dict:
    """Accept dynamics as a dict {axis: pole} (the extraction schema's flat
    shape, with underscore or hyphen keys) or a list [{axis, choice}], and
    normalize to {axis: pole-or-tuple} keyed by the canonical hyphen axis names.
    A list/tuple choice is a genuinely-dual (ambiguous) axis — honored, not
    flattened (see `dramatica-precision-limit`): forcing a binary the story
    doesn't commit to is exactly the over-claim the substrate refuses."""
    out: dict = {}
    items = []
    if isinstance(raw, dict):
        items = list(raw.items())
    elif isinstance(raw, list):
        for d in raw:
            if isinstance(d, dict):
                items.append((d.get("axis"), d.get("choice", d.get("pole"))))
    for axis, choice in items:
        a = str(axis or "").strip().lower().replace("_", "-")
        if not a:
            continue
        if isinstance(choice, (list, tuple)):
            poles = tuple(str(c).strip().lower() for c in choice if str(c).strip())
            if poles:                       # an empty list is an unset axis
                out[a] = poles
        else:
            pole = str(choice or "").strip().lower()
            if pole:                        # an empty string is an unset axis
                out[a] = pole
    return out


def _dramatica_overlay(doc: dict) -> list:
    gaps: list = []
    valid_ids = _valid_ids(doc)
    throughlines = doc.get("throughlines") or []

    roles = [(t.get("role") or "").strip().lower() for t in throughlines]
    missing_tl = [r for r in DRAMATICA_THROUGHLINES if r not in roles]
    if missing_tl:
        gaps.append(Gap("structural", "dram_missing_throughlines",
                        "Dramatica needs all four throughlines; not yet set: "
                        f"{', '.join(missing_tl)}."))

    domains_seen: list = []
    for t in throughlines:
        r = (t.get("role") or "").strip().lower()
        dom = (t.get("domain") or "").strip().lower()
        if not dom:
            gaps.append(Gap("structural", "dram_throughline_no_domain",
                            f"Which domain does the {r or 'throughline'} occupy "
                            "— activity, situation, manipulation, or "
                            "fixed-attitude?", r))
        elif dom not in DRAMATICA_DOMAINS:
            gaps.append(Gap("structural", "dram_unknown_domain",
                            f"'{dom}' isn't a Dramatica domain.", r))
        else:
            domains_seen.append(dom)
        owner = (t.get("owner") or "").strip()
        if owner and owner not in valid_ids:
            gaps.append(Gap("structural", "dram_owner_unknown",
                            f"The {r or 'throughline'} names owner '{owner}', "
                            "not a declared character.", r))
    if throughlines:
        if len(set(domains_seen)) != len(domains_seen):
            gaps.append(Gap("structural", "dram_domain_collision",
                            "Each throughline must occupy a distinct domain — "
                            "two share one."))
        elif not missing_tl:
            missing_dom = [d for d in DRAMATICA_DOMAINS if d not in domains_seen]
            if missing_dom:
                gaps.append(Gap("structural", "dram_domains_incomplete",
                                "These domains aren't assigned to any "
                                f"throughline: {', '.join(missing_dom)}."))

    dynamics = _normalize_dynamics(doc.get("dynamics"))
    missing_dyn = [a for a in DRAMATICA_DYNAMICS if a not in dynamics]
    if missing_dyn:
        gaps.append(Gap("structural", "dram_missing_dynamics",
                        "Dramatica's eight dynamics fix the storyform; not yet "
                        f"set: {', '.join(missing_dyn)}."))
    for axis, pole in dynamics.items():
        allowed = DRAMATICA_DYNAMICS.get(axis)
        if not allowed:
            continue
        poles = pole if isinstance(pole, tuple) else (pole,) if pole else ()
        bad = [p for p in poles if p not in allowed]
        if bad:
            gaps.append(Gap("structural", "dram_bad_dynamic",
                            f"The {axis} dynamic has {', '.join(bad)}, but must "
                            f"be one of {', '.join(allowed)}.", axis))

    if not (doc.get("story_goal") or "").strip():
        gaps.append(Gap("structural", "dram_no_goal",
                        "What is the story goal — what the overall story "
                        "collectively pursues?"))
    if not (doc.get("story_consequence") or "").strip():
        gaps.append(Gap("structural", "dram_no_consequence",
                        "What is the consequence if the goal is not achieved?"))
    return gaps


# ---- Dramatic --------------------------------------------------------------
DRAMATIC_THROUGHLINES = (
    "overall-story", "main-character", "impact-character", "relationship",
)
DRAMATIC_RESOLUTIONS = ("affirm", "negate", "complicate", "unresolved")
# abstract throughline owners (no single character carries them)
DRAMATIC_OWNER_SENTINELS = ("none", "situation", "relationship")


def _dramatic_overlay(doc: dict) -> list:
    gaps: list = []
    valid_ids = _valid_ids(doc)
    arguments = doc.get("arguments") or []
    throughlines = doc.get("throughlines") or []

    if not arguments:
        gaps.append(Gap("structural", "dramatic_no_argument",
                        "What argument does the story make — the thematic "
                        "premise it puts on trial?"))
    for i, a in enumerate(arguments, start=1):
        if not (a.get("premise") or "").strip():
            gaps.append(Gap("structural", "dramatic_arg_no_premise",
                            f"Argument #{i} needs a premise — the claim it "
                            "interrogates."))
        res = (a.get("resolution") or a.get("resolution_direction") or "").strip().lower()
        if res and res not in DRAMATIC_RESOLUTIONS:
            gaps.append(Gap("structural", "dramatic_bad_resolution",
                            f"An argument resolves '{res}', but must be one of: "
                            f"{', '.join(DRAMATIC_RESOLUTIONS)}."))

    roles = [(t.get("role") or "").strip().lower() for t in throughlines]
    if "main-character" not in roles:
        gaps.append(Gap("structural", "dramatic_no_main_character",
                        "Which throughline is the main character's — whose "
                        "personal arc anchors the story?"))
    for t in throughlines:
        r = (t.get("role") or "").strip().lower()
        owner = (t.get("owner") or "").strip()
        if owner and owner not in valid_ids \
                and owner.lower() not in DRAMATIC_OWNER_SENTINELS:
            gaps.append(Gap("structural", "dramatic_owner_unknown",
                            f"The {r or 'throughline'} names owner '{owner}', "
                            "not a declared character.", r))
        stakes = t.get("stakes") or {}
        if not ((stakes.get("at_risk") or "").strip()
                or (stakes.get("to_gain") or "").strip()):
            gaps.append(Gap("structural", "dramatic_throughline_no_stakes",
                            f"What's at stake in the {r or 'throughline'} "
                            "throughline — what's risked, what's to gain?", r))
    return gaps


# ============================================================================
# The dialect registry — gap rules + extraction schema/prompt, one per dialect
# ============================================================================

@dataclass(frozen=True)
class Dialect:
    """A pluggable overlay: how the interview gap-checks and extracts a story
    in one dialect's vocabulary. `overlay_gaps` is the deterministic spine
    half; `system_prompt` / `build_schema` are the LLM extraction half.

    `constrained` selects the extraction transport. The structured-output
    grammar compiler (`messages.parse`) has a schema-complexity ceiling — the
    Aristotelian and Save-the-Cat schemas compile under it, but the larger
    Dramatica / Dramatic schemas do not (the server returns "Schema is too
    complex" / "Grammar compilation timed out"). Those dialects extract via
    plain JSON mode instead (ask for JSON, validate with pydantic in Python),
    which has no schema-size limit. See `extract_story_draft`."""
    name: str
    overlay_gaps: Callable[[dict], list]
    system_prompt: str
    build_schema: Callable[[], type]
    postprocess: Optional[Callable[[dict], dict]] = None
    constrained: bool = True


# ---- extraction: shared base + per-dialect schemas (pydantic, lazy) --------

_SHARED_RECORD = """\
The record's shared skeleton (every dialect):
- title, logline; telling ("chronological" | "reverse" | "explicit").
- characters: each a short lowercase id, a name, and a role.
- events (the beats): each a short id, a `when` integer (story-time order), the
  participant ids in `who`, a `summary` of the beat, and an optional `focalizer`.
- phases: which event ids are in the beginning, the middle, the end (every event
  in exactly one).

Commit to ids that are short lowercase handles, integer `when` values to fix
story-time order. If the author has not supplied something, leave it absent
rather than fabricating — the interview will ask for it next. Carry forward
everything already established in the prior record."""


def _aristotelian_schema():
    from pydantic import BaseModel, Field

    class CharacterDraft(BaseModel):
        id: str = Field(description="short lowercase handle")
        name: str = ""
        role: str = Field(default="figure",
                          description="tragic-hero | pathos-centre | figure")
        hamartia: str = ""

    class EventDraft(BaseModel):
        id: str = Field(description="short lowercase handle")
        when: Optional[int] = Field(default=None,
                                    description="story-time order, integer")
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

    return StoryDraft


def _save_the_cat_schema():
    from pydantic import BaseModel, Field

    class CharacterDraft(BaseModel):
        id: str = Field(description="short lowercase handle")
        name: str = ""
        role: str = Field(default="",
                          description="protagonist | antagonist | love-interest "
                                      "| mentor | … (Save-the-Cat role label)")

    class EventDraft(BaseModel):
        id: str = Field(description="short lowercase handle")
        when: Optional[int] = Field(default=None,
                                    description="story-time order, integer")
        who: list[str] = Field(default_factory=list)
        summary: str = ""
        beat: str = Field(default="",
                          description="the canonical beat this event realizes, "
                                      "e.g. 'Catalyst', 'Midpoint', 'Finale'")
        focalizer: str = ""

    class PhasesDraft(BaseModel):
        beginning: list[str] = Field(default_factory=list)
        middle: list[str] = Field(default_factory=list)
        end: list[str] = Field(default_factory=list)

    class StoryDraft(BaseModel):
        title: str = ""
        logline: str = ""
        telling: str = "chronological"
        theme_statement: str = Field(default="",
                                     description="the story's thematic claim")
        genre: str = Field(default="",
                           description="one of the ten genres, e.g. "
                                       "'dude-with-a-problem'")
        characters: list[CharacterDraft] = Field(default_factory=list)
        events: list[EventDraft] = Field(default_factory=list)
        phases: PhasesDraft = Field(default_factory=PhasesDraft)

    return StoryDraft


def _dramatica_schema():
    from pydantic import BaseModel, Field

    class CharacterDraft(BaseModel):
        id: str = Field(description="short lowercase handle")
        name: str = ""
        role: str = ""

    class EventDraft(BaseModel):
        id: str = Field(description="short lowercase handle")
        when: Optional[int] = Field(default=None)
        who: list[str] = Field(default_factory=list)
        summary: str = ""

    class ThroughlineDraft(BaseModel):
        role: str = Field(description="one of the four throughline roles")
        domain: str = Field(default="", description="one of the four domains")
        owner: str = Field(default="", description="character id, if any")

    # The eight dynamics as one flat object (each a single pole). Kept flat —
    # not a list of {axis, choice} — to stay under the structured-output schema
    # complexity ceiling. `_normalize_dynamics` maps these to the canonical
    # hyphenated axis names.
    class DynamicsDraft(BaseModel):
        resolve: str = ""
        growth: str = ""
        approach: str = ""
        problem_solving_style: str = ""
        driver: str = ""
        limit: str = ""
        outcome: str = ""
        judgment: str = ""

    class PhasesDraft(BaseModel):
        beginning: list[str] = Field(default_factory=list)
        middle: list[str] = Field(default_factory=list)
        end: list[str] = Field(default_factory=list)

    class StoryDraft(BaseModel):
        title: str = ""
        logline: str = ""
        telling: str = "chronological"
        story_goal: str = ""
        story_consequence: str = ""
        characters: list[CharacterDraft] = Field(default_factory=list)
        events: list[EventDraft] = Field(default_factory=list)
        throughlines: list[ThroughlineDraft] = Field(default_factory=list)
        dynamics: DynamicsDraft = Field(default_factory=DynamicsDraft)
        phases: PhasesDraft = Field(default_factory=PhasesDraft)

    return StoryDraft


def _dramatic_schema():
    from pydantic import BaseModel, Field

    class CharacterDraft(BaseModel):
        id: str = Field(description="short lowercase handle")
        name: str = ""
        role: str = ""

    class EventDraft(BaseModel):
        id: str = Field(description="short lowercase handle")
        when: Optional[int] = Field(default=None)
        who: list[str] = Field(default_factory=list)
        summary: str = ""
        focalizer: str = ""

    class ArgumentDraft(BaseModel):
        premise: str = Field(description="the thematic claim the story tests")
        resolution: str = Field(default="",
                                description="affirm | negate | complicate | "
                                            "unresolved")

    class StakesDraft(BaseModel):
        at_risk: str = ""
        to_gain: str = ""

    class ThroughlineDraft(BaseModel):
        role: str = Field(description="overall-story | main-character | "
                                      "impact-character | relationship")
        owner: str = Field(default="", description="character id, or none / "
                                                   "situation / relationship")
        stakes: StakesDraft = Field(default_factory=StakesDraft)

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
        arguments: list[ArgumentDraft] = Field(default_factory=list)
        throughlines: list[ThroughlineDraft] = Field(default_factory=list)
        phases: PhasesDraft = Field(default_factory=PhasesDraft)

    return StoryDraft


_ARISTOTELIAN_PROMPT = f"""\
You are a story-structure interviewer for a generation engine. The engine needs
a story expressed as a precise authoring record it can verify and render. Your
job is to turn the author's natural description (and their answers to follow-up
questions) into that record — committing to concrete structural facts, never
inventing content the author has not implied.

This is an ARISTOTELIAN tragedy. Beyond the shared skeleton:
- characters carry a role ("tragic-hero" | "pathos-centre" | "figure") and a
  tragic-hero carries a hamartia (the flaw that undoes them).
- events may carry a `mark` ("peripeteia" the reversal | "anagnorisis" the
  recognition), and an anagnorisis carries a `recognizer` (the character id who
  comes to the knowledge).

{_SHARED_RECORD}"""

_SAVE_THE_CAT_PROMPT = f"""\
You are a story-structure interviewer for a generation engine, working in the
SAVE-THE-CAT dialect. Turn the author's natural description (and their answers)
into a precise authoring record — committing to concrete facts, never inventing
content the author has not implied.

Beyond the shared skeleton:
- theme_statement: the one claim about life the story argues.
- genre: one of the ten ("monster-in-the-house", "golden-fleece",
  "out-of-the-bottle", "dude-with-a-problem", "rites-of-passage", "buddy-love",
  "whydunit", "fool-triumphant", "institutionalized", "superhero").
- characters carry a Save-the-Cat role label ("protagonist", "antagonist",
  "love-interest", "mentor", "confidant", "ally", "narrator", "victim",
  "suspect", "threshold-guardian").
- each event may name the canonical `beat` it realizes (one of the fifteen:
  Opening Image, Theme Stated, Set-Up, Catalyst, Debate, Break Into Two,
  B Story, Fun and Games, Midpoint, Bad Guys Close In, All Is Lost, Dark Night
  of the Soul, Break Into Three, Finale, Final Image).

{_SHARED_RECORD}"""

_DRAMATICA_PROMPT = f"""\
You are a story-structure interviewer for a generation engine, working in the
DRAMATICA dialect. Turn the author's natural description (and their answers)
into a precise authoring record — committing to concrete facts, never inventing
content the author has not implied.

Beyond the shared skeleton:
- story_goal: what the overall story collectively pursues; story_consequence:
  what happens if the goal is not achieved.
- throughlines: the four ("overall-story", "main-character", "impact-character",
  "relationship"), each placed in a distinct domain ("activity", "situation",
  "manipulation", "fixed-attitude"), with an `owner` character id where one
  character carries it.
- dynamics: the eight axes, each set to one pole — resolve (change|steadfast),
  growth (start|stop), approach (do-er|be-er), problem-solving-style
  (linear|holistic), driver (action|decision), limit (timelock|optionlock),
  outcome (success|failure), judgment (good|bad). Where the story genuinely does
  not commit a binary, give the axis BOTH poles rather than forcing one.

{_SHARED_RECORD}"""

_DRAMATIC_PROMPT = f"""\
You are a story-structure interviewer for a generation engine, working in the
DRAMATIC dialect. Turn the author's natural description (and their answers) into
a precise authoring record — committing to concrete facts, never inventing
content the author has not implied.

Beyond the shared skeleton:
- arguments: the thematic claims the story puts on trial, each a `premise` and a
  `resolution` ("affirm" | "negate" | "complicate" | "unresolved").
- throughlines: the structural roles ("overall-story", "main-character",
  "impact-character", "relationship"), each with an `owner` (a character id, or
  the sentinel none / situation / relationship) and `stakes` (what's at_risk and
  what's to_gain).

{_SHARED_RECORD}"""


def _postprocess_aristotelian(doc: dict) -> dict:
    for c in doc.get("characters", []):
        if not c.get("hamartia"):
            c.pop("hamartia", None)
    for ev in doc.get("events", []):
        for k in ("mark", "recognizer", "focalizer"):
            if not ev.get(k):
                ev.pop(k, None)
    return doc


def _postprocess_save_the_cat(doc: dict) -> dict:
    for ev in doc.get("events", []):
        for k in ("beat", "focalizer"):
            if not ev.get(k):
                ev.pop(k, None)
    for k in ("theme_statement", "genre"):
        if not (doc.get(k) or "").strip():
            doc.pop(k, None)
    return doc


def _postprocess_generic(doc: dict) -> dict:
    for ev in doc.get("events", []):
        if not ev.get("focalizer"):
            ev.pop("focalizer", None)
    return doc


DIALECTS: dict = {
    "aristotelian": Dialect(
        "aristotelian", _aristotelian_overlay, _ARISTOTELIAN_PROMPT,
        _aristotelian_schema, _postprocess_aristotelian),
    "save-the-cat": Dialect(
        "save-the-cat", _save_the_cat_overlay, _SAVE_THE_CAT_PROMPT,
        _save_the_cat_schema, _postprocess_save_the_cat),
    "dramatica": Dialect(
        "dramatica", _dramatica_overlay, _DRAMATICA_PROMPT,
        _dramatica_schema, _postprocess_generic, constrained=False),
    "dramatic": Dialect(
        "dramatic", _dramatic_overlay, _DRAMATIC_PROMPT,
        _dramatic_schema, _postprocess_generic, constrained=False),
}

DEFAULT_DIALECT = "aristotelian"


def _dialect(dialect: str) -> Dialect:
    try:
        return DIALECTS[dialect]
    except KeyError:
        raise ValueError(
            f"unknown dialect {dialect!r}; one of {sorted(DIALECTS)}")


# ============================================================================
# The gap API — skeleton + the selected dialect's overlay
# ============================================================================

def interview_gaps(doc: dict, dialect: str = DEFAULT_DIALECT) -> list:
    """Enumerate the authoring dict's gaps as questions, blocking first.
    Pure — the dialect-agnostic skeleton `authoring.compile_story` enforces,
    plus the chosen dialect's structural homework, turned to face the author."""
    return _skeleton_gaps(doc) + _dialect(dialect).overlay_gaps(doc)


def blocking_gaps(doc: dict, dialect: str = DEFAULT_DIALECT) -> list:
    return [g for g in interview_gaps(doc, dialect) if g.severity == "blocking"]


def structural_gaps(doc: dict, dialect: str = DEFAULT_DIALECT) -> list:
    return [g for g in interview_gaps(doc, dialect) if g.severity == "structural"]


def is_compilable(doc: dict, dialect: str = DEFAULT_DIALECT) -> bool:
    """True when no blocking gap remains — `compile_story` should succeed."""
    return not blocking_gaps(doc, dialect)


def next_questions(doc: dict, *, n: int = 3, include_structural: bool = True,
                   dialect: str = DEFAULT_DIALECT):
    """The next questions to put to the author: all blocking gaps first
    (compilation is gated on them), then structural ones, capped at `n`."""
    gaps = blocking_gaps(doc, dialect)
    if include_structural:
        gaps = gaps + structural_gaps(doc, dialect)
    return [g.question for g in gaps[:n]]


# ============================================================================
# The loop controller — pure, with injected extract_fn / answer_fn
# ============================================================================

@dataclass
class InterviewRound:
    round: int
    n_blocking: int
    n_structural: int
    questions: list = field(default_factory=list)
    answers: str = ""
    stopped: str = ""          # reason this was the last round, if so


@dataclass
class InterviewRun:
    rounds: list = field(default_factory=list)
    final_doc: dict = field(default_factory=dict)
    dialect: str = DEFAULT_DIALECT

    @property
    def complete(self) -> bool:
        return bool(self.rounds) and self.rounds[-1].stopped == "complete"

    @property
    def compilable(self) -> bool:
        return is_compilable(self.final_doc, self.dialect)


def run_interview(
    *,
    brief: str,
    extract_fn,
    answer_fn,
    dialect: str = DEFAULT_DIALECT,
    max_rounds: int = 6,
    ask_structural: bool = True,
    on_round=None,
) -> InterviewRun:
    """Drive the interview to a well-formed authoring dict in `dialect`.

    `extract_fn(brief, prior, answers) -> dict` turns the brief + the prior
    draft + the author's latest answers into the authoring dict (the LLM half,
    or a fake in tests). `answer_fn(questions, doc) -> str` supplies the
    author's answers to the round's questions (interactive stdin, an
    AI-simulated author, a scripted list, or a fake) — an empty answer ends the
    interview.

    The loop is pure given those two; it mirrors `draft_convergence.converge`:
    extract → gaps-as-questions → answer → re-extract, stopping when no gaps
    remain ('complete'), when answers stop reducing the gap count ('stalled'),
    when the author finishes, or at `max_rounds`."""
    _dialect(dialect)  # validate early
    run = InterviewRun(dialect=dialect)
    doc = extract_fn(brief, None, None) or {}
    prev_metric = None

    for i in range(max_rounds):
        blocking = blocking_gaps(doc, dialect)
        structural = structural_gaps(doc, dialect) if ask_structural else []
        active = blocking + structural
        rec = InterviewRound(
            round=i, n_blocking=len(blocking), n_structural=len(structural),
            questions=[g.question for g in active],
        )
        run.rounds.append(rec)
        if on_round:
            on_round(rec, blocking, structural)

        if not active:
            rec.stopped = "complete"
            break
        if prev_metric is not None and len(active) >= prev_metric:
            rec.stopped = "stalled (answers stopped reducing gaps)"
            break
        if i == max_rounds - 1:
            rec.stopped = "max rounds reached"
            break

        prev_metric = len(active)
        answers = answer_fn(rec.questions, doc) or ""
        rec.answers = answers
        if not answers.strip():
            rec.stopped = "author finished"
            break
        doc = extract_fn(brief, doc, answers) or doc

    run.final_doc = doc
    return run


# ============================================================================
# The LLM half — extract / merge the authoring dict from natural input
# ============================================================================

def _extract_via_json(*, system_prompt, user_prompt, output_format, model,
                      effort, max_tokens, dry_run, client):
    """Extraction without the structured-output grammar compiler: ask for a
    JSON object, parse it, and validate with the pydantic schema in Python.
    Used for dialects whose schema exceeds the `messages.parse` complexity
    ceiling. Returns the validated model instance, or None on dry_run."""
    import json
    schema_hint = json.dumps(output_format.model_json_schema())
    sys_prompt = (system_prompt + "\n\nReturn your answer as a single JSON "
                  "object conforming to this JSON Schema (no prose, no code "
                  "fence):\n" + schema_hint)
    full_user = user_prompt + "\n\nReturn ONLY the JSON object."
    if dry_run:
        return None

    import anthropic
    client = client or anthropic.Anthropic()
    response = client.messages.create(
        model=model, max_tokens=max_tokens, thinking={"type": "adaptive"},
        output_config={"effort": effort},
        system=[{"type": "text", "text": sys_prompt,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": full_user}],
    )
    text = "".join(b.text for b in response.content if b.type == "text").strip()
    # tolerate a stray code fence or surrounding prose
    if "```" in text:
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end + 1]
    return output_format.model_validate(json.loads(text))


def extract_story_draft(
    brief: str,
    *,
    dialect: str = DEFAULT_DIALECT,
    prior: Optional[dict] = None,
    answers: Optional[str] = None,
    model: str = "claude-opus-4-6",
    effort: str = "high",
    max_tokens: int = 6000,
    dry_run: bool = False,
    client=None,
) -> Optional[dict]:
    """Turn a natural brief (plus the prior draft and the author's latest
    answers) into the authoring dict for `dialect`. Returns the dict, or None
    on dry_run.

    The schema and system prompt come from the dialect registry, so the model
    fills the right overlay's fields. Dialects flagged `constrained` extract
    via the structured-output grammar (`messages.parse`); the rest extract via
    plain JSON mode (`_extract_via_json`) because their schema exceeds the
    grammar compiler's complexity ceiling. Pydantic is imported in the schema
    builders, lazily, so `interview_gaps` and the rest of the spine stay
    standard-library and offline-testable."""
    d = _dialect(dialect)
    output_format = d.build_schema()

    import json
    parts = [f"Author's brief:\n{brief}"]
    if prior:
        parts.append("Record so far (carry all of this forward, refine it):\n"
                     + json.dumps(prior, indent=1))
    if answers:
        parts.append(f"Author's latest answers to your questions:\n{answers}")
    parts.append("Produce the complete, updated authoring record.")
    user_prompt = "\n\n".join(parts)

    if d.constrained:
        from story_engine.core.reader_model_client_base import invoke_parse_helper
        draft = invoke_parse_helper(
            system_prompt=d.system_prompt, user_prompt=user_prompt,
            output_format=output_format, model=model, max_tokens=max_tokens,
            effort=effort, dry_run=dry_run, client=client,
        )
    else:
        draft = _extract_via_json(
            system_prompt=d.system_prompt, user_prompt=user_prompt,
            output_format=output_format, model=model, max_tokens=max_tokens,
            effort=effort, dry_run=dry_run, client=client,
        )
    if draft is None:
        return None
    doc = draft.model_dump()
    # Drop empty optionals so the dict reads like a hand-authored .story.toml
    # (and so the gap rules see genuine absence, not empty strings).
    return d.postprocess(doc) if d.postprocess else doc
