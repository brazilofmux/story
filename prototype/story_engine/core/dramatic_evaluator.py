"""
dramatic_evaluator.py — fidelity evaluation in the general DRAMATIC dialect's
own terms (the FOURTH dialect to reach evaluate-parity).

The peer of `draft_evaluator.py` (Aristotelian), `dramatica_evaluator.py`
(Dramatica), and `save_the_cat_evaluator.py` (Save-the-Cat). The Dramatic
dialect is the lean PARENT: a story makes one thematic ARGUMENT, carried by a
small cast playing functions (Hero, Obstacle, optional Helpers), with
something at STAKE. There are no acts, signposts, or beat sheet to count.

So the fidelity target is necessarily SOFTER than Save-the-Cat's fifteen
named beats — and the honesty discipline matters more here. Two tiers:
- CRISP, name-level: the Hero, the Obstacle, the Helper(s) — who plays each
  function in the argument.
- The ARGUMENT's resolution: does the prose AFFIRM / NEGATE / COMPLICATE /
  leave UNRESOLVED its premise? (the dialect's own four-value axis — it
  already admits a middle, so no forcing.)
- FUZZY, content-level: the argument's claim, and the stakes. Scored by
  token overlap, and LABELLED fuzzy so a soft match is not mistaken for a
  crisp one.

Two stages, same shape as the peers:
1. `decompile_dramatic(prose, …)` → `DramaticReading` (BLIND — given the FORM,
   never which character fills which function or how the argument lands).
2. `compare_to_story(reading, story)` → `DramaticFidelityReport` (pure Python).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from story_engine.core.llm import DEFAULT_MODEL

try:
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover
    raise ImportError("dramatic_evaluator requires pydantic.") from exc

from story_engine.core.reader_model_client_base import invoke_parse_helper


# ============================================================================
# Stage 1 — the blind Dramatic reading
# ============================================================================

class DramaticReading(BaseModel):
    """A blind reading of a draft in the general Dramatic dialect. The reader
    is given the FORM (a thematic argument carried by Hero/Obstacle/Helper
    functions) but never the storyform — never who fills which function or
    how the author resolved the argument."""
    hero: str = Field(
        description="The HERO / protagonist — the character who drives the "
                    "story's argument. Named as the prose names them.")
    obstacle: str = Field(
        description="The OBSTACLE / antagonist — the character or force that "
                    "most opposes the Hero. Named as the prose names them.")
    helper: str = Field(
        default="",
        description="The HELPER — a character who aids the Hero's quest. Name "
                    "them; '' if none is clear.")
    argument_claim: str = Field(
        description="In one phrase: what does this story ARGUE? Its central "
                    "thematic claim about how the world works.")
    argument_resolution: str = Field(
        description="How does the story resolve that claim by the end? "
                    "'affirm' if the prose upholds/proves it, 'negate' if it "
                    "refutes/undercuts it, 'complicate' if it both supports "
                    "and qualifies it, 'unresolved' if it leaves it open, '' "
                    "if unclear.")
    stakes: str = Field(
        default="",
        description="What is AT STAKE — what the Hero risks and stands to "
                    "gain. One phrase; '' if unclear.")
    overall_read: str = Field(
        description="Does the prose hold together as one argued story on "
                    "these terms? One or two sentences.")


_DRAMATIC_SYSTEM_PROMPT = """\
You are a structural reader trained on the general Dramatic theory of story: \
a story makes ONE thematic argument, carried by a small cast playing \
functions — a Hero who drives the argument, an Obstacle who opposes it, and \
optional Helpers who aid the Hero — with something concrete at stake.

You will be given the prose of a draft. Report the Dramatic structure you \
perceive: who is the Hero, who is the Obstacle, who (if anyone) helps; the \
single claim the story argues and whether the ending AFFIRMS, NEGATES, \
COMPLICATES, or leaves that claim UNRESOLVED; and what is at stake.

Critical discipline: report ONLY what the PROSE supports. You are NOT given \
the storyform — reconstruct it from the text alone. Name characters as the \
prose names them; leave a field empty rather than inventing.

Produce the typed structure. Prose belongs only inside the fields.
"""


# Genre-only framing — the FORM (argument + functions), never the answer key
# (who is the Hero, which way the argument lands).
GENRE_NOTE = (
    "The draft is a general Dramatic story: one thematic argument carried by "
    "a Hero, an Obstacle, and optional Helpers, with stakes. Reconstruct — "
    "who plays each function, what the story argues and whether it AFFIRMS / "
    "NEGATES / COMPLICATES / leaves UNRESOLVED that claim, and what is at "
    "stake — from the PROSE ALONE. You are NOT told the answer; work it out "
    "from the text."
)


def decompile_dramatic(
    draft_text: str,
    *,
    title: str = "",
    dialect_note: str = GENRE_NOTE,
    model: str = DEFAULT_MODEL,
    effort: str = "high",
    max_tokens: int = 6000,
    dry_run: bool = False,
    client=None,
) -> Optional[DramaticReading]:
    """Read the draft prose blind and return the Dramatic structure it
    supports. Returns None on dry_run.

    `dialect_note` MUST be genre-only (defaults to GENRE_NOTE). Do NOT pass
    the generation note — naming the functions/argument leads the read."""
    header = []
    if title:
        header.append(f"Draft title: {title}")
    if dialect_note:
        header.append(f"Frame: {dialect_note}")
    header.append("Below is the full prose of the draft. Report the Dramatic "
                  "structure you perceive, per your contract.")
    user_prompt = "\n".join(header) + "\n\n=== DRAFT PROSE ===\n\n" + draft_text
    return invoke_parse_helper(
        system_prompt=_DRAMATIC_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_format=DramaticReading,
        model=model, max_tokens=max_tokens, effort=effort,
        dry_run=dry_run, client=client,
    )


# ============================================================================
# Stage 2 — the fidelity comparison (pure Python, offline-testable)
# ============================================================================

@dataclass(frozen=True)
class DramaticFidelityFinding:
    dimension: str
    authored: str
    decompiled: str
    verdict: str             # "preserved" | "drifted" | "lost" | "added"
    note: str = ""


@dataclass
class DramaticFidelityReport:
    title: str
    findings: list = field(default_factory=list)

    @property
    def scored(self) -> list:
        return [f for f in self.findings if f.verdict != "added"]

    @property
    def preserved(self) -> int:
        return sum(1 for f in self.scored if f.verdict == "preserved")

    @property
    def score(self) -> float:
        s = self.scored
        return (self.preserved / len(s)) if s else 0.0


_HERO_FUNCS = {"hero", "protagonist"}
_OBSTACLE_FUNCS = {"obstacle", "antagonist"}
_HELPER_FUNCS = {"helper"}

_STOP = {"the", "of", "a", "an", "and", "to", "is", "that", "his", "her",
         "their", "by", "it", "what", "who", "they", "he", "she", "in", "as",
         "for", "be", "are", "or", "but", "not", "no", "than", "more", "most",
         "person", "man", "woman", "people", "story", "thing", "you"}


def _toks(s: str) -> set:
    raw = "".join(c if c.isalnum() else " " for c in (s or "")).split()
    return {t.lower() for t in raw if t}


def _names_for(story, funcs: set) -> list:
    """The authored character names whose function labels hit `funcs`."""
    out = []
    for c in getattr(story, "characters", ()) or ():
        labels = {str(l).lower() for l in (getattr(c, "function_labels", ()) or ())}
        if labels & funcs:
            out.append(getattr(c, "name", c.id))
    return out


def _name_matches(a: str, b: str) -> bool:
    na, nb = (_toks(a) - _STOP), (_toks(b) - _STOP)
    return bool(na and nb and (na & nb))


def _any_name_match(read: str, pool: list) -> bool:
    return any(_name_matches(read, p) for p in pool)


def _content_overlap(read: str, *authored: str) -> bool:
    """Fuzzy: do the reading's content tokens overlap the authored text(s)?"""
    r = _toks(read) - _STOP
    if not r:
        return False
    a = set()
    for t in authored:
        a |= (_toks(t) - _STOP)
    return bool(r & a)


def _norm_resolution(s: str) -> str:
    """Normalize a resolution word to one of affirm/negate/complicate/
    unresolved (by stem), or '' if unrecognized."""
    t = (s or "").strip().lower()
    for canon in ("affirm", "negate", "complicate", "unresolved"):
        if t.startswith(canon[:5]) or canon in t:
            return canon
    # common synonyms the reader may use
    if any(w in t for w in ("uphold", "prove", "vindicat", "confirm")):
        return "affirm"
    if any(w in t for w in ("refute", "undercut", "deny", "disprove")):
        return "negate"
    return ""


def compare_to_story(reading: DramaticReading, story) -> DramaticFidelityReport:
    """Compare a blind Dramatic reading to the authored Dramatic story.
    Name/axis level for the crisp dimensions, token-overlap (labelled fuzzy)
    for the argument claim and the stakes. The reader never saw the story."""
    report = DramaticFidelityReport(title=getattr(story, "title", ""))

    # 1. Hero identity (crisp).
    heroes = _names_for(story, _HERO_FUNCS)
    if heroes:
        report.findings.append(DramaticFidelityFinding(
            dimension="hero", authored=", ".join(heroes),
            decompiled=reading.hero or "(none)",
            verdict="preserved" if _any_name_match(reading.hero, heroes)
            else "lost", note="who drives the argument"))

    # 2. Obstacle identity (crisp).
    obstacles = _names_for(story, _OBSTACLE_FUNCS)
    if obstacles:
        report.findings.append(DramaticFidelityFinding(
            dimension="obstacle", authored=", ".join(obstacles),
            decompiled=reading.obstacle or "(none)",
            verdict="preserved" if _any_name_match(reading.obstacle, obstacles)
            else "lost", note="who opposes the Hero"))

    # 3. Helper identity (crisp; scored only if a Helper was authored). A draft
    # with multiple Helpers preserves the dimension if the read finds ANY.
    helpers = _names_for(story, _HELPER_FUNCS)
    if helpers:
        report.findings.append(DramaticFidelityFinding(
            dimension="helper", authored=", ".join(helpers),
            decompiled=reading.helper or "(none)",
            verdict="preserved" if _any_name_match(reading.helper, helpers)
            else "lost", note="who aids the Hero (any authored helper)"))

    # 4. Argument resolution direction (the thematic outcome).
    args = getattr(story, "arguments", ()) or ()
    if args:
        arg = args[0]
        a_dir = getattr(getattr(arg, "resolution_direction", ""), "value",
                        getattr(arg, "resolution_direction", ""))
        a_dir = str(a_dir).lower()
        got = _norm_resolution(reading.argument_resolution)
        report.findings.append(DramaticFidelityFinding(
            dimension="argument_resolution", authored=a_dir,
            decompiled=got or (reading.argument_resolution or "(none)"),
            verdict="preserved" if got == a_dir else "drifted",
            note="does the prose land the argument the authored way"))

        # 5. Argument claim (FUZZY — content-token overlap with the premise).
        premise = getattr(arg, "premise", "")
        report.findings.append(DramaticFidelityFinding(
            dimension="argument_claim", authored=premise[:60],
            decompiled=(reading.argument_claim or "(none)")[:60],
            verdict="preserved" if _content_overlap(reading.argument_claim,
                                                    premise) else "drifted",
            note="FUZZY: the claim's content survived (token overlap)"))

    # 6. Stakes (FUZZY — content-token overlap with at-risk / to-gain).
    stakes = getattr(story, "stakes", ()) or ()
    if stakes:
        stk = stakes[0]
        at_risk = getattr(stk, "at_risk", "")
        to_gain = getattr(stk, "to_gain", "")
        report.findings.append(DramaticFidelityFinding(
            dimension="stakes", authored=(at_risk or to_gain)[:60],
            decompiled=(reading.stakes or "(none)")[:60],
            verdict="preserved" if _content_overlap(reading.stakes, at_risk,
                                                    to_gain) else "lost",
            note="FUZZY: what is at risk / to gain reads (token overlap)"))

    return report
