"""
dramatica_evaluator.py — fidelity evaluation in DRAMATICA's own terms.

The peer of `draft_evaluator.py` (which scores in Aristotelian terms).
Closing asymmetry #2: a Dramatica-generated draft must be scorable
against the storyform it came from — WITHOUT forcing it through an
Aristotelian lens (no peripeteia/pathos). This reads the prose BLIND and
extracts the Dramatica structure it perceives — the four throughlines,
the story goal, the ending shape (Outcome × Judgment), the Main
Character's Resolve — then compares that to the authored storyform.

Two stages, same discipline as the Aristotelian evaluator:
1. `decompile_dramatica(draft_text, …)` → `DramaticaReading` (blind).
2. `compare_to_storyform(reading, storyform)` → `DramaticaFidelityReport`
   (pure Python, offline-testable; the reader never sees the answer key).

The load-bearing checks for a non-tragic story: did the prose land the
OUTCOME (e.g. Failure — the public goal is not won) and the JUDGMENT
(e.g. Good — the protagonist is personally fulfilled) as INDEPENDENT
axes? That pair is what makes Rocky a personal triumph rather than a
tragedy, and it is exactly what an Aristotelian evaluator cannot see.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from story_engine.core.llm import DEFAULT_MODEL

try:
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover
    raise ImportError("dramatica_evaluator requires pydantic.") from exc

from story_engine.core.reader_model_client_base import invoke_parse_helper


# ============================================================================
# Stage 1 — the blind Dramatica reading
# ============================================================================

class DramaticaReading(BaseModel):
    """A blind Dramatica reading of a draft's prose. The reader is given
    ONLY the prose — never the storyform it was generated from."""
    story_goal: str = Field(
        description="What the OVERALL story is collectively trying to "
                    "achieve — the public/objective goal, in one phrase.")
    outcome: str = Field(
        description="Is the overall-story goal achieved by the end? "
                    "'success' if achieved, 'failure' if not, '' if unclear. "
                    "Judge the OBJECTIVE result only (the scoreboard / verdict "
                    "/ who took the prize), not how anyone feels.")
    judgment: str = Field(
        description="Does the MAIN CHARACTER end personally resolved and "
                    "fulfilled, or in anguish? 'good' if fulfilled/at peace, "
                    "'bad' if unresolved/anguished, '' if unclear. This is "
                    "INDEPENDENT of outcome — a character can lose and feel "
                    "good, or win and feel bad.")
    ending_shape: str = Field(
        description="Name the ending in a phrase: e.g. 'personal triumph' "
                    "(loses but fulfilled), 'tragedy' (loses and anguished), "
                    "'success' (wins and fulfilled), 'hollow victory' (wins "
                    "but anguished).")
    main_character: str = Field(
        description="The Main Character — whose personal throughline the "
                    "story follows. Named as the prose names them.")
    mc_resolve: str = Field(
        description="Does the Main Character CHANGE their essential nature by "
                    "the end, or hold it? 'steadfast' if they hold, 'changed' "
                    "if they change, '' if unclear.")
    influence_character: str = Field(
        default="",
        description="The character who most pressures the Main Character to "
                    "change (or to hold). Named as the prose names them; '' "
                    "if none is clear.")
    relationship: str = Field(
        default="",
        description="The central relationship that grows or strains across "
                    "the story (e.g. 'Rocky and Adrian'). '' if none.")
    throughlines_present: list[str] = Field(
        default_factory=list,
        description="Which of the four Dramatica throughlines you can clearly "
                    "identify in the prose: any of 'overall', 'main "
                    "character', 'influence character', 'relationship'.")
    overall_read: str = Field(
        description="Does the prose hold together as a complete story on "
                    "these terms? One or two sentences.")


_DRAMATICA_SYSTEM_PROMPT = """\
You are a structural reader trained on the Dramatica theory of story. \
You will be given the prose of a draft. Read it and report the Dramatica \
structure you perceive — the four throughlines (the Overall Story, the \
Main Character, the Influence Character, the Relationship), the story \
goal, and the two independent outcome axes.

Critical discipline: report ONLY what the PROSE supports. You are NOT \
given the storyform the author intended — reconstruct it from the text \
alone. Hold the two ending axes APART: OUTCOME is the objective result \
(was the public goal achieved?), JUDGMENT is the Main Character's \
personal resolution (do they end fulfilled or in anguish?). A story can \
fail its goal and still feel like a triumph, or achieve its goal and \
feel hollow — say what the PROSE actually does, do not collapse the two. \
Name characters as the prose names them; leave a field empty rather than \
inventing.

Produce the typed structure. Prose belongs only inside the fields.
"""


# Genre-only framing for the blind reader — never the specific storyform
# (which outcome, which judgment). Passing the generation note here LEADS
# the read. Names the task, not the answer.
GENRE_NOTE = (
    "The draft is a complete story (a Dramatica storyform underlies it). "
    "Reconstruct its structure — the four throughlines, the story goal, the "
    "two INDEPENDENT ending axes (Outcome: was the objective goal achieved? "
    "Judgment: does the Main Character end fulfilled or in anguish?), the MC "
    "resolve — from the PROSE ALONE. You are NOT told the storyform; work it "
    "out from the text, and do not collapse Outcome and Judgment together."
)


def decompile_dramatica(
    draft_text: str,
    *,
    title: str = "",
    dialect_note: str = GENRE_NOTE,
    model: str = DEFAULT_MODEL,
    effort: str = "high",
    max_tokens: int = 6000,
    dry_run: bool = False,
    client=None,
) -> Optional[DramaticaReading]:
    """Read the draft prose blind and return the Dramatica structure it
    supports. Returns None on dry_run.

    `dialect_note` MUST be genre-only (defaults to GENRE_NOTE). Do NOT pass
    the generation note — naming the intended outcome/judgment leads the
    read and it is no longer blind."""
    header = []
    if title:
        header.append(f"Draft title: {title}")
    if dialect_note:
        header.append(f"Frame: {dialect_note}")
    header.append("Below is the full prose of the draft. Report the "
                  "Dramatica structure you perceive, per your contract.")
    user_prompt = "\n".join(header) + "\n\n=== DRAFT PROSE ===\n\n" + draft_text
    return invoke_parse_helper(
        system_prompt=_DRAMATICA_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_format=DramaticaReading,
        model=model, max_tokens=max_tokens, effort=effort,
        dry_run=dry_run, client=client,
    )


# ============================================================================
# Stage 2 — the fidelity comparison (pure Python, offline-testable)
# ============================================================================

@dataclass(frozen=True)
class DramaticaFidelityFinding:
    dimension: str
    authored: str
    decompiled: str
    verdict: str             # "preserved" | "drifted" | "lost" | "added"
    note: str = ""


@dataclass
class DramaticaFidelityReport:
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


def _dyn_map(storyform) -> dict:
    """{axis: representative pole string}. For a dual axis this is the lean
    — a single string, so string-consuming callers (repair's directive) keep
    working. Use `_dyn_poles` when you need the honest full span."""
    out = {}
    for d in getattr(storyform, "dynamics", ()) or ():
        axis = d.axis.value if hasattr(d.axis, "value") else d.axis
        out[axis] = d.leans if hasattr(d, "leans") else d.choice
    return out


def _dyn_poles(storyform) -> dict:
    """{axis: frozenset of lowercased poles}. A single-pole axis → a 1-set;
    a dual axis → its full span. This is what makes scoring ambiguity-honest:
    a read that lands ANY spanned pole is faithful."""
    out = {}
    for d in getattr(storyform, "dynamics", ()) or ():
        axis = d.axis.value if hasattr(d.axis, "value") else d.axis
        poles = d.poles if hasattr(d, "poles") else frozenset({d.choice})
        out[axis] = frozenset(str(p).lower() for p in poles)
    return out


def _axis_label(poles: frozenset) -> str:
    """Display label for an authored axis: the single pole, or the dual span
    joined with '|' so the report SHOWS the axis was authored ambiguous."""
    return "|".join(sorted(poles))


def _perspective_of(throughline_id: str) -> str:
    t = throughline_id.lower()
    if "overall" in t or t.startswith("t_os"):
        return "overall"
    if "_mc" in t or "mc_" in t:
        return "main character"
    if "_ic" in t or "ic_" in t:
        return "influence character"
    if "_rel" in t or "rel_" in t or "_rs" in t:
        return "relationship"
    return "overall"


def _norm(s: str) -> set:
    return {t.strip(",.;:'\"").lower() for t in (s or "").split() if t}


def _matches(a: str, b: str) -> bool:
    na, nb = _norm(a), _norm(b)
    return bool(na and nb and (na & nb))


def compare_to_storyform(reading: DramaticaReading,
                         storyform) -> DramaticaFidelityReport:
    """Compare a blind Dramatica reading to the authored storyform.
    Enum/name-level, pure Python; the reader never saw the storyform."""
    report = DramaticaFidelityReport(title=getattr(storyform, "title", ""))
    dyn = _dyn_map(storyform)
    poles = _dyn_poles(storyform)

    def _score_axis(axis: str, got_raw: str, base_note: str, dimension=None):
        """Score one DSP axis by pole membership. A single-pole axis is
        strict (the binary case, unchanged). A dual axis reads `preserved`
        if the blind read lands ANY spanned pole — because for a genuinely
        dual story EITHER pole is faithful; that is honesty, not leniency.
        Ambiguity is declared by the AUTHOR — it never loosens a binary axis."""
        spanned = poles.get(axis) or frozenset()
        if not spanned:
            return
        got = (got_raw or "").lower()
        dual = len(spanned) > 1
        note = base_note
        if dual:
            note += (" — authored DUAL; either pole is faithful "
                     "(ambiguity-honest, not drift)")
        report.findings.append(DramaticaFidelityFinding(
            dimension=dimension or axis, authored=_axis_label(spanned),
            decompiled=got or "(none)",
            verdict="preserved" if got in spanned else "drifted",
            note=note))

    # 1. Outcome (objective result) — the load-bearing non-tragedy axis.
    _score_axis("outcome", reading.outcome, "the objective result the prose lands")

    # 2. Judgment (personal resolution) — independent of outcome.
    _score_axis("judgment", reading.judgment,
                "the Main Character's personal resolution")

    # 3. Ending shape: the Outcome×Judgment combination survived as a whole.
    a_end = (getattr(storyform, "canonical_ending", "") or "").replace("-", " ")
    if a_end:
        got_end = (reading.ending_shape or "").lower()
        # A dual axis makes ANY of its spanned poles a faithful read of the
        # ending's flavour — match against the full span, not one pole.
        pole_hit = any(p in got_end for p in poles.get("outcome", ()))
        pole_hit = pole_hit or any(p in got_end for p in poles.get("judgment", ()))
        ok = _matches(a_end, got_end) or pole_hit or "triumph" in got_end
        report.findings.append(DramaticaFidelityFinding(
            dimension="ending_shape", authored=a_end,
            decompiled=reading.ending_shape or "(none)",
            verdict="preserved" if ok else "drifted",
            note="the ending's character — not a tragedy if judgment is good"))

    # 4. MC Resolve (steadfast / changed).
    _score_axis("resolve", reading.mc_resolve,
                "the Main Character's resolve", dimension="mc_resolve")

    # 5. Main Character identity (the MC throughline's subject).
    mc_subject = ""
    for da in getattr(storyform, "domain_assignments", ()) or ():
        if _perspective_of(da.throughline_id) == "main character":
            parts = da.throughline_id.split("_")
            mc_subject = parts[2] if len(parts) > 2 else ""
    if mc_subject:
        report.findings.append(DramaticaFidelityFinding(
            dimension="main_character", authored=mc_subject,
            decompiled=reading.main_character or "(none)",
            verdict="preserved" if _matches(mc_subject, reading.main_character)
            else "lost"))

    # 6. Throughline coverage — how many of the four the reader identified.
    authored_persp = {
        _perspective_of(da.throughline_id)
        for da in getattr(storyform, "domain_assignments", ()) or ()
    }
    got_persp = {p.strip().lower() for p in reading.throughlines_present}
    for persp in sorted(authored_persp):
        report.findings.append(DramaticaFidelityFinding(
            dimension="throughline", authored=persp,
            decompiled=", ".join(sorted(got_persp)) or "(none)",
            verdict="preserved" if persp in got_persp else "lost",
            note=f"the {persp} throughline reads in the prose"))

    return report
