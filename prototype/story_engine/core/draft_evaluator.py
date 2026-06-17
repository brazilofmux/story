"""
draft_evaluator.py — decompile a generated draft back toward the
Aristotelian dialect and measure structural fidelity (terminus #2).

The generator (`draft_generator.py`) is the compiler back-end: verified
substrate → first-draft prose. This module is the **quality signal** the
generation track needs: it reads the prose BLIND (the prose only, no
substrate) and extracts the Aristotelian structure it perceives —
peripeteia, anagnorisis, the pathos-centre, staggered recognitions
(including anti-recognitions), the tragic heroes — then compares that
blind reading against the substrate the draft was generated FROM. The
diff is a fidelity score: did the structural spine survive the
substrate → prose round-trip?

This is the natural evaluator because:

- It reuses the reader-model infra (typed extraction via
  `client.messages.parse`), running it text → structure instead of
  structure → critique.
- The comparison is **name-level**, not event-id-level. Character names
  survive into the prose ("the Duchess"); substrate event ids do not.
  Comparing at the name/qualifier/cardinality level keeps the read
  honest — the decompiler is never shown the answer key (the event ids
  or the authored field values), only the prose.
- A generated draft is "structurally good" to the degree its prose still
  reads as the tragedy the substrate specified: the reversal on the
  right character, the recognition on the right one, the pity-and-fear
  where the pathos-centre put it, the anti-recognition still too-late.

Two stages:

1. `decompile_draft(draft_text, …)` → `DecompiledStructure` (a typed,
   blind reading of the prose).
2. `compare_to_mythos(decompiled, mythos)` → `FidelityReport` (pure
   Python; offline-testable; no API).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

try:
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "The draft evaluator requires pydantic. Install via "
        "`pip install -r prototype/requirements.txt`."
    ) from exc

from story_engine.core.reader_model_client_base import invoke_parse_helper


# ============================================================================
# Stage 1 — the blind decompilation (typed extraction from prose)
# ============================================================================


class RecognitionRead(BaseModel):
    """One recognition the reader perceives in the prose."""
    character: str = Field(
        description="The character who comes to knowledge, named as the "
                    "prose names them (e.g. 'the Duchess', 'Ferdinand')."
    )
    summary: str = Field(
        description="One sentence: what they recognize, and when in the "
                    "action."
    )
    qualifier: str = Field(
        description="'genuine' for an ordinary recognition; 'anti' for a "
                    "recognition that is REAL but arrives too late to alter "
                    "the outcome (recognition-without-remedy); 'partial' "
                    "for an incomplete grasp; '' if unsure."
    )


class DecompiledStructure(BaseModel):
    """A blind Aristotelian reading of a draft's prose. The reader is
    given ONLY the prose and the dialect vocabulary — never the
    substrate the draft was generated from."""
    plot_kind: str = Field(
        description="'complex' if the action turns on a peripeteia and/or "
                    "anagnorisis; 'simple' otherwise."
    )
    unity_of_action: bool = Field(
        description="True if the prose reads as ONE unified action; False "
                    "if it reads as parallel/episodic plots."
    )
    peripeteia: str = Field(
        description="The main reversal of fortune: what turns, and the beat "
                    "it turns at. Empty if none is perceptible."
    )
    peripeteia_character: str = Field(
        description="The character whose fortune the main reversal turns, "
                    "named as the prose names them. Empty if unclear."
    )
    anagnorisis: str = Field(
        description="The main recognition: the move from ignorance to "
                    "knowledge that carries the play's weight."
    )
    anagnorisis_character: str = Field(
        description="The character who comes to that knowledge, named as "
                    "the prose names them. Empty if unclear."
    )
    pathos_centre_characters: list[str] = Field(
        default_factory=list,
        description="The character(s) who carry the play's pity-and-fear — "
                    "the suffering-centre — even if they are not the ones "
                    "who act or recognize. Named as the prose names them."
    )
    tragic_hero_characters: list[str] = Field(
        default_factory=list,
        description="The character(s) the prose frames as the tragic "
                    "hero(es) — bearing a hamartia and an arc toward a fall."
    )
    staggered_recognitions: list[RecognitionRead] = Field(
        default_factory=list,
        description="Each distinct recognition the prose stages, including "
                    "anti-recognitions. Empty if there is only the one main "
                    "recognition already named above."
    )
    secondary_reversals: list[str] = Field(
        default_factory=list,
        description="Reversals of OTHER characters' fortunes beyond the "
                    "main one — other arcs falling. Each entry names the "
                    "character and the turn. Empty if the fall is single."
    )
    telling_order: str = Field(
        default="",
        description="How the PROSE is ordered relative to the story's "
                    "chronology, judged from the prose's own sequence: "
                    "'chronological' if events are narrated in the order they "
                    "happen; 'reverse' if the telling moves backward through "
                    "time (the aftermath staged first, the origin last); "
                    "'non-linear' if fractured or interleaved out of order."
    )
    overall_read: str = Field(
        description="Does the prose hold together as a tragedy on "
                    "Aristotelian terms? One or two sentences."
    )


_DECOMPILE_SYSTEM_PROMPT = """\
You are a structural reader. You will be given the prose of a draft \
play or script. Read it as a dramatist trained on Aristotle's Poetics \
and report the structure you perceive — the arrangement of the \
incidents (mythos), the reversal (peripeteia), the recognition \
(anagnorisis), the suffering that grounds pity-and-fear (pathos), the \
tragic hero and the error (hamartia) that undoes them.

Critical discipline: report ONLY what the PROSE supports. You are NOT \
given the structure the author intended — you are reconstructing it \
from the text alone. If the prose makes one character the suffering \
centre while a DIFFERENT character is the one who finally understands, \
SAY SO; do not smooth the split away. If a recognition lands too late \
to change anything, mark it 'anti'. Name characters exactly as the \
prose names them. Where the text does not support a structural claim, \
leave the field empty rather than inventing one.

Report the telling order honestly: if the prose narrates the aftermath \
before the cause — moving backward through time — say 'reverse'; if it \
jumps around, 'non-linear'; if it runs in chronological sequence, \
'chronological'. Judge only from the order the PROSE presents events, \
not the order in which they happen.

Produce the typed structure. Prose belongs only inside the fields.
"""


def decompile_draft(
    draft_text: str,
    *,
    title: str = "",
    dialect_note: str = "",
    model: str = "claude-opus-4-6",
    effort: str = "high",
    max_tokens: int = 8000,
    dry_run: bool = False,
    client=None,
) -> Optional[DecompiledStructure]:
    """Read the draft prose blind and return the Aristotelian structure
    the prose supports. Returns None on dry_run (prints the prompt)."""
    header = []
    if title:
        header.append(f"Draft title: {title}")
    if dialect_note:
        header.append(f"Frame (the form it was written in): {dialect_note}")
    header.append(
        "Below is the full prose of the draft. Read it and report the "
        "structure you perceive, per your contract."
    )
    user_prompt = "\n".join(header) + "\n\n=== DRAFT PROSE ===\n\n" + draft_text

    return invoke_parse_helper(
        system_prompt=_DECOMPILE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_format=DecompiledStructure,
        model=model,
        max_tokens=max_tokens,
        effort=effort,
        dry_run=dry_run,
        client=client,
    )


# ============================================================================
# Stage 2 — the fidelity comparison (pure Python, offline-testable)
# ============================================================================


@dataclass(frozen=True)
class FidelityFinding:
    """One structural dimension's round-trip verdict."""
    dimension: str
    authored: str            # what the substrate specified
    decompiled: str          # what the blind prose reading found
    verdict: str             # "preserved" | "drifted" | "lost" | "added"
    note: str = ""


@dataclass
class FidelityReport:
    """The substrate → prose → substrate round-trip result."""
    title: str
    findings: list = field(default_factory=list)   # list[FidelityFinding]

    @property
    def scored(self) -> list:
        """Findings that count toward the score (preserved/drifted/lost —
        an 'added' element is informational, not a fidelity loss)."""
        return [f for f in self.findings if f.verdict != "added"]

    @property
    def preserved(self) -> int:
        return sum(1 for f in self.scored if f.verdict == "preserved")

    @property
    def score(self) -> float:
        s = self.scored
        return (self.preserved / len(s)) if s else 0.0


def _norm(name: str) -> set:
    """Normalize a character name to a token set for fuzzy matching —
    'the Duchess of Amalfi' and 'the Duchess' share the 'duchess' token.
    Drops articles/particles so the shared proper-noun tokens align."""
    stop = {"the", "of", "a", "an", "duke", "duchess", "lord", "sir"}
    toks = {t.strip(",.;:'\"").lower() for t in name.split()}
    core = {t for t in toks if t and t not in stop}
    # Keep a role-token fallback so 'the Duchess' still matches when the
    # only shared token IS the role word.
    return core if core else {t for t in toks if t}


def _name_matches(a: str, b: str) -> bool:
    """True if two character names plausibly denote the same character."""
    if not a or not b:
        return False
    na, nb = _norm(a), _norm(b)
    if na & nb:
        return True
    # Role-word fallback: both reduce to the same single role token.
    ra = {t.strip(",.;:'\"").lower() for t in a.split()}
    rb = {t.strip(",.;:'\"").lower() for t in b.split()}
    return bool(ra & rb & {"duchess", "duke", "cardinal", "king"})


def _any_match(name: str, pool: list) -> bool:
    return any(_name_matches(name, p) for p in pool)


def _char_name(ref_id: str, mythos) -> str:
    """ArCharacter id / substrate ref → readable name, for authored
    expectations."""
    for c in getattr(mythos, "characters", ()) or ():
        if getattr(c, "id", None) == ref_id or \
                getattr(c, "character_ref_id", None) == ref_id:
            return getattr(c, "name", ref_id)
    return ref_id


def compare_to_mythos(decompiled: DecompiledStructure, mythos) -> FidelityReport:
    """Compare a blind prose reading to the authored mythos it was
    generated from. Name-level, pure Python; the decompiler never saw
    the authored values, so agreement is evidence the prose carried the
    structure."""
    report = FidelityReport(title=getattr(mythos, "title", ""))
    chars = getattr(mythos, "characters", ()) or ()

    # 1. plot_kind
    authored_pk = getattr(mythos, "plot_kind", "")
    report.findings.append(FidelityFinding(
        dimension="plot_kind",
        authored=authored_pk,
        decompiled=decompiled.plot_kind,
        verdict=("preserved"
                 if decompiled.plot_kind.strip().lower() == authored_pk.lower()
                 else "drifted"),
    ))

    # 2. unity of action
    authored_uoa = bool(getattr(mythos, "asserts_unity_of_action", True))
    report.findings.append(FidelityFinding(
        dimension="unity_of_action",
        authored=str(authored_uoa),
        decompiled=str(decompiled.unity_of_action),
        verdict=("preserved"
                 if decompiled.unity_of_action == authored_uoa else "drifted"),
    ))

    # 3. anagnorisis character (the recognizer)
    anag_ref = getattr(mythos, "anagnorisis_character_ref_id", None)
    if anag_ref:
        authored_anag = _char_name(anag_ref, mythos)
        ok = _name_matches(authored_anag, decompiled.anagnorisis_character)
        report.findings.append(FidelityFinding(
            dimension="anagnorisis_character",
            authored=authored_anag,
            decompiled=decompiled.anagnorisis_character or "(none)",
            verdict="preserved" if ok else "lost",
            note=("the prose put the recognition on the right character"
                  if ok else
                  "the recognition did not land on the authored recognizer"),
        ))

    # 4. pathos-centre (A22) — each authored centre should be readable
    pathos_ids = getattr(mythos, "pathos_character_ref_ids", ()) or ()
    authored_pathos = [_char_name(p, mythos) for p in pathos_ids]
    for name in authored_pathos:
        ok = _any_match(name, decompiled.pathos_centre_characters)
        report.findings.append(FidelityFinding(
            dimension="pathos_centre",
            authored=name,
            decompiled=", ".join(decompiled.pathos_centre_characters) or "(none)",
            verdict="preserved" if ok else "lost",
            note=("the pity-and-fear still reads as centred here"
                  if ok else "the pathos-centre did not survive the prose"),
        ))
    # decompiled pathos centres not authored = added (informational)
    for got in decompiled.pathos_centre_characters:
        if authored_pathos and not _any_match(got, authored_pathos):
            report.findings.append(FidelityFinding(
                dimension="pathos_centre",
                authored="(not authored)", decompiled=got,
                verdict="added",
                note="prose reads a pathos-centre the substrate did not mark",
            ))

    # 5. tragic heroes (A5)
    authored_heroes = [getattr(c, "name", c.id) for c in chars
                       if getattr(c, "is_tragic_hero", False)]
    for name in authored_heroes:
        ok = _any_match(name, decompiled.tragic_hero_characters)
        report.findings.append(FidelityFinding(
            dimension="tragic_hero",
            authored=name,
            decompiled=", ".join(decompiled.tragic_hero_characters) or "(none)",
            verdict="preserved" if ok else "lost",
        ))

    # 6. anti-recognitions (A20) — each authored 'anti' chain step should
    #    surface as an anti-recognition in the blind read.
    chain = getattr(mythos, "anagnorisis_chain", ()) or ()
    decomp_anti = [r for r in decompiled.staggered_recognitions
                   if (r.qualifier or "").lower() == "anti"]
    for step in chain:
        if (getattr(step, "anagnorisis_qualifier", "") or "").lower() != "anti":
            continue
        who = _char_name(getattr(step, "character_ref_id", ""), mythos)
        ok = any(_name_matches(who, r.character) for r in decomp_anti)
        report.findings.append(FidelityFinding(
            dimension="anti_recognition",
            authored=f"{who} (anti)",
            decompiled=", ".join(f"{r.character} (anti)" for r in decomp_anti)
                       or "(no anti-recognition read)",
            verdict="preserved" if ok else "lost",
            note=("the recognition-too-late survived as prose"
                  if ok else
                  "the anti-recognition flattened into an ordinary one"),
        ))

    # 7. secondary reversals (A19) — cardinality survival
    authored_sec = getattr(mythos, "secondary_peripeteia_event_ids", ()) or ()
    if authored_sec:
        n_auth, n_got = len(authored_sec), len(decompiled.secondary_reversals)
        # Preserved if the prose carries at least a clear majority of the
        # secondary falls (the read is fuzzier than an exact count).
        ok = n_got >= max(1, (n_auth + 1) // 2)
        report.findings.append(FidelityFinding(
            dimension="secondary_reversals",
            authored=f"{n_auth} secondary reversal(s)",
            decompiled=f"{n_got} read",
            verdict="preserved" if ok else "drifted",
            note=("the multi-arc fall survived"
                  if ok else "the secondary arcs thinned in the prose"),
        ))

    return report
