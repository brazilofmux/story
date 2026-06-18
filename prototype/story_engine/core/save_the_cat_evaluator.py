"""
save_the_cat_evaluator.py — fidelity evaluation in SAVE-THE-CAT's own terms.

The peer of `draft_evaluator.py` (Aristotelian) and `dramatica_evaluator.py`
(Dramatica). Brings the third dialect toward full-stack parity: an
StC-generated draft must be scorable against the beat sheet it came from —
WITHOUT forcing it through an Aristotelian or Dramatica lens.

Save-the-Cat's structure is unusually decompilable: it asserts every
commercial story hits the SAME fifteen named beats in order (Opening Image
… Final Image). That gives a crisp, nameable fidelity target — the StC
analogue of the Aristotelian named categories that proved stable (peripeteia,
anagnorisis) rather than the Dramatica dynamics that flickered.

Two stages, same discipline as the peers:
1. `decompile_stc(draft_text, …)` → `StcReading` (BLIND — the reader is given
   the FORM, the fifteen canonical beat names, never WHICH event fills each).
2. `compare_to_sheet(reading, sheet)` → `StcFidelityReport` (pure Python,
   offline-testable; the reader never sees the answer key).

The load-bearing checks: did the prose carry the fifteen beats, in canonical
ORDER, on the right protagonist, with the B story present? Beat coverage IS
the fidelity signal for this dialect — the beats are the structure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

try:
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover
    raise ImportError("save_the_cat_evaluator requires pydantic.") from exc

from story_engine.core.reader_model_client_base import invoke_parse_helper
from story_engine.core.save_the_cat import (
    CANONICAL_BEAT_BY_SLOT, CANONICAL_BEAT_NAMES, NUM_CANONICAL_BEATS,
)


# ============================================================================
# Stage 1 — the blind Save-the-Cat reading
# ============================================================================

class StcBeatRead(BaseModel):
    """One beat the reader located in the prose."""
    beat: str = Field(
        description="Which of the fifteen canonical beats this is — use the "
                    "canonical NAME exactly (e.g. 'Catalyst', 'Midpoint', "
                    "'All Is Lost', 'Final Image').")
    what_happens: str = Field(
        description="One sentence: what in the PROSE fills this beat, and "
                    "roughly where in the story it lands.")


class StcReading(BaseModel):
    """A blind Save-the-Cat reading of a draft's prose. The reader is given
    the FORM (the fifteen beat names) but never the storyform — never which
    event the author placed at each beat."""
    protagonist: str = Field(
        description="The protagonist — the character the beat sheet tracks. "
                    "Named as the prose names them.")
    beats_identified: list[StcBeatRead] = Field(
        default_factory=list,
        description="The canonical beats you can locate in the prose, IN THE "
                    "ORDER they appear in the text. Include only beats you can "
                    "actually point to; leave out ones you cannot find.")
    theme_stated: str = Field(
        default="",
        description="The story's thematic claim (the Theme Stated beat), if "
                    "you can identify it; '' if not.")
    b_story: str = Field(
        default="",
        description="The B story — the secondary thread (often a relationship) "
                    "that carries the theme. Name it in a phrase; '' if none.")
    midpoint: str = Field(
        default="",
        description="The Midpoint turn: is it a FALSE VICTORY or a FALSE "
                    "DEFEAT, and what happens? '' if unclear.")
    all_is_lost: str = Field(
        default="",
        description="The All Is Lost beat — the rock-bottom / death (literal, "
                    "professional, or symbolic). '' if unclear.")
    final_mirrors_opening: str = Field(
        default="",
        description="Does the Final Image mirror/invert the Opening Image to "
                    "register how the world changed? 'yes', 'no', or '' if "
                    "unclear.")
    overall_read: str = Field(
        description="Does the prose hold together as a complete beat sheet? "
                    "One or two sentences.")


_STC_SYSTEM_PROMPT = """\
You are a structural reader trained on Blake Snyder's Save the Cat beat \
sheet. You will be given the prose of a draft. Read it and report the \
fifteen-beat structure you perceive: which canonical beats appear, in what \
order, on which protagonist, with what B story.

The fifteen canonical beats, in order: Opening Image, Theme Stated, Set-Up, \
Catalyst, Debate, Break Into Two, B Story, Fun and Games, Midpoint, Bad Guys \
Close In, All Is Lost, Dark Night of the Soul, Break Into Three, Finale, \
Final Image.

Critical discipline: report ONLY what the PROSE supports. You are NOT given \
the beat sheet the author intended — reconstruct it from the text alone. \
Label each beat you find with its canonical name exactly. List the beats in \
the ORDER they appear in the prose, not the canonical order, so the reader \
can tell whether the progression holds. Leave a beat OUT rather than \
inventing one you cannot point to. Name characters as the prose names them.

Produce the typed structure. Prose belongs only inside the fields.
"""


# Genre-only framing — the FORM (the fifteen beats), never the answer key
# (which event fills each beat). Naming the form is fair; naming the fillings
# would lead the read.
GENRE_NOTE = (
    "The draft is a Save-the-Cat beat-sheet story. Reconstruct its fifteen-"
    "beat structure — which of the canonical beats (Opening Image, Theme "
    "Stated, Set-Up, Catalyst, Debate, Break Into Two, B Story, Fun and "
    "Games, Midpoint, Bad Guys Close In, All Is Lost, Dark Night of the Soul, "
    "Break Into Three, Finale, Final Image) you can locate, in what order, on "
    "which protagonist, with what B story — from the PROSE ALONE. You are NOT "
    "told what the author placed at each beat; work it out from the text."
)


def decompile_stc(
    draft_text: str,
    *,
    title: str = "",
    dialect_note: str = GENRE_NOTE,
    model: str = "claude-opus-4-6",
    effort: str = "high",
    max_tokens: int = 6000,
    dry_run: bool = False,
    client=None,
) -> Optional[StcReading]:
    """Read the draft prose blind and return the Save-the-Cat structure it
    supports. Returns None on dry_run.

    `dialect_note` MUST be genre-only (defaults to GENRE_NOTE). Do NOT pass
    the generation note — naming which event fills each beat leads the read
    and it is no longer blind."""
    header = []
    if title:
        header.append(f"Draft title: {title}")
    if dialect_note:
        header.append(f"Frame: {dialect_note}")
    header.append("Below is the full prose of the draft. Report the "
                  "Save-the-Cat structure you perceive, per your contract.")
    user_prompt = "\n".join(header) + "\n\n=== DRAFT PROSE ===\n\n" + draft_text
    return invoke_parse_helper(
        system_prompt=_STC_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_format=StcReading,
        model=model, max_tokens=max_tokens, effort=effort,
        dry_run=dry_run, client=client,
    )


# ============================================================================
# Stage 2 — the fidelity comparison (pure Python, offline-testable)
# ============================================================================

@dataclass(frozen=True)
class StcFidelityFinding:
    dimension: str
    authored: str
    decompiled: str
    verdict: str             # "preserved" | "drifted" | "lost" | "added"
    note: str = ""


@dataclass
class StcFidelityReport:
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


def _norm_beat(name: str) -> str:
    """Normalize a beat name to lowercased alnum tokens joined by spaces."""
    toks = [t for t in
            "".join(c if c.isalnum() else " " for c in (name or "")).split()]
    return " ".join(t.lower() for t in toks)


# canonical normalized-name → slot
_CANON_BY_NORM = {_norm_beat(n): s
                  for s, n in ((b.slot, b.name)
                               for b in CANONICAL_BEAT_BY_SLOT.values())}
# token sets for fuzzy fallback
_CANON_TOKENS = {s: set(_norm_beat(CANONICAL_BEAT_BY_SLOT[s].name).split())
                 for s in CANONICAL_BEAT_BY_SLOT}


def _slot_of_read(beat_name: str) -> Optional[int]:
    """Map a reader's beat label to a canonical slot. Exact normalized match
    first; else the best token-overlap above threshold, requiring the
    distinguishing token so 'Break Into Two' and 'Break Into Three' (and
    'Opening Image' / 'Final Image') do not collide."""
    norm = _norm_beat(beat_name)
    if not norm:
        return None
    if norm in _CANON_BY_NORM:
        return _CANON_BY_NORM[norm]
    toks = set(norm.split())
    best, best_score = None, 0.0
    for slot, ctoks in _CANON_TOKENS.items():
        inter = toks & ctoks
        if not inter:
            continue
        # the distinguishing tokens that must match if present
        distinguishers = {"two", "three", "opening", "final"} & ctoks
        if distinguishers and not (distinguishers & toks):
            continue
        score = len(inter) / len(toks | ctoks)
        if score > best_score:
            best, best_score = slot, score
    return best if best_score >= 0.5 else None


def _protagonist_of(sheet) -> str:
    """The sheet's protagonist: a character with the 'protagonist' role, else
    the A strand's focal character, else the first character."""
    chars = getattr(sheet, "characters", ()) or ()
    for c in chars:
        if "protagonist" in (getattr(c, "role_labels", ()) or ()):
            return c.name
    by_id = {c.id: c for c in chars}
    for st in getattr(sheet, "strands", ()) or ():
        kind = st.kind.value if hasattr(st.kind, "value") else st.kind
        if kind == "a-story" and getattr(st, "focal_character_id", None):
            c = by_id.get(st.focal_character_id)
            if c:
                return c.name
    return chars[0].name if chars else ""


def _name_matches(a: str, b: str) -> bool:
    na = {t for t in _norm_beat(a).split()}
    nb = {t for t in _norm_beat(b).split()}
    stop = {"the", "of", "a", "an", "lord", "lady", "king", "thane"}
    na, nb = (na - stop), (nb - stop)
    return bool(na and nb and (na & nb))


def compare_to_sheet(reading: StcReading, sheet) -> StcFidelityReport:
    """Compare a blind Save-the-Cat reading to the authored beat sheet.
    Beat-name / order level, pure Python; the reader never saw the sheet."""
    report = StcFidelityReport(title=getattr(sheet, "title", ""))

    authored_slots = sorted({b.slot for b in getattr(sheet, "beats", ()) or ()})
    read_slots = [_slot_of_read(b.beat) for b in reading.beats_identified]
    read_slots_found = [s for s in read_slots if s is not None]
    read_set = set(read_slots_found)

    # 1. Beat coverage — one finding per authored slot. The beats ARE the
    # structure; coverage is the core fidelity signal for this dialect.
    for slot in authored_slots:
        name = CANONICAL_BEAT_BY_SLOT[slot].name
        report.findings.append(StcFidelityFinding(
            dimension=f"beat[{slot:02d}]", authored=name,
            decompiled=name if slot in read_set else "(not found)",
            verdict="preserved" if slot in read_set else "lost",
            note=CANONICAL_BEAT_BY_SLOT[slot].purpose.split(";")[0]))

    # 2. Beat ORDER — did the identified beats appear in canonical order?
    nondecreasing = all(a <= b for a, b in
                        zip(read_slots_found, read_slots_found[1:]))
    report.findings.append(StcFidelityFinding(
        dimension="beat_order", authored="1→15 canonical",
        decompiled="→".join(str(s) for s in read_slots_found) or "(none)",
        verdict="preserved" if nondecreasing and read_slots_found else "drifted",
        note="the fifteen-beat progression survived in sequence"))

    # 3. Protagonist identity.
    prot = _protagonist_of(sheet)
    if prot:
        report.findings.append(StcFidelityFinding(
            dimension="protagonist", authored=prot,
            decompiled=reading.protagonist or "(none)",
            verdict="preserved" if _name_matches(prot, reading.protagonist)
            else "lost", note="the beat sheet tracks this character"))

    # 4. B story present (only scored if the sheet authored a B strand).
    has_b = any((st.kind.value if hasattr(st.kind, "value") else st.kind)
                == "b-story" for st in getattr(sheet, "strands", ()) or ())
    if has_b:
        report.findings.append(StcFidelityFinding(
            dimension="b_story", authored="present",
            decompiled=reading.b_story or "(none)",
            verdict="preserved" if reading.b_story.strip() else "lost",
            note="the B story (theme-carrying secondary thread) reads"))

    return report
