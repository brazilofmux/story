"""
fidelity.py — the shared core of the four dialect evaluators
(`evaluator-shared-core-sketch-01`).

Each dialect evaluator decompiles a draft's prose blind and compares the
reading to what was authored. The record types that carry the verdicts,
the scoring, and the name/content matching policy are dialect-neutral
and live here — ONCE. The dialects keep their own vocabularies as
aliases (`StcFidelityFinding`, …) and their own Stage-2 comparison
logic; only what is actually common is shared (ESC1–ESC3).

Standard library only: the evaluators' Stage 1 (typed extraction) is
venv-backed, but the record types and scoring are pure Python and stay
importable without pydantic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ============================================================================
# The fidelity record pair (ESC1)
# ============================================================================


@dataclass(frozen=True)
class FidelityFinding:
    """One structural dimension's round-trip verdict."""
    dimension: str
    authored: str            # what the substrate/storyform specified
    decompiled: str          # what the blind prose reading found
    verdict: str             # "preserved" | "drifted" | "lost" | "added"
    note: str = ""


@dataclass
class FidelityReport:
    """The authored → prose → blind-reading round-trip result."""
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


# ============================================================================
# Name matching (ESC3) — one policy for all four dialects
# ============================================================================

ARTICLES = frozenset({"the", "a", "an", "of"})

# One honorific set for every corpus — a title word is a title word
# whether the play is Malfi (duke/duchess/cardinal) or Macbeth
# (lord/lady/thane). Growing this per new corpus is an open question in
# the sketch; do not add speculative entries.
TITLES = frozenset({
    "cardinal", "count", "countess", "duchess", "duke", "king", "lady",
    "lord", "prince", "princess", "queen", "sir", "thane",
})


def tokens(s: str) -> set:
    """Lowercased alphanumeric tokens of a string."""
    raw = "".join(c if c.isalnum() else " " for c in (s or "")).split()
    return {t.lower() for t in raw if t}


def normalize_name(name: str) -> set:
    """A character name's core tokens for matching — articles and titles
    dropped, so 'the Duchess of Amalfi' and 'Amalfi' align on the proper
    noun. A name that is ONLY a title ('the Duchess') keeps its title
    tokens, so it can still match — but never on a bare article."""
    toks = tokens(name)
    core = toks - ARTICLES - TITLES
    return core if core else toks - ARTICLES


def name_matches(a: str, b: str) -> bool:
    """True if two character names plausibly denote the same character:
    core-token overlap first; else a shared TITLE token ('the Duchess' ↔
    'Duchess of Amalfi'). Empty input never matches, and 'the Duchess'
    never matches 'the Duke' on the shared article."""
    if not (a or "").strip() or not (b or "").strip():
        return False
    na, nb = normalize_name(a), normalize_name(b)
    if na and nb and (na & nb):
        return True
    return bool(tokens(a) & tokens(b) & TITLES)


def any_name_match(name: str, pool) -> bool:
    return any(name_matches(name, p) for p in pool)


# ============================================================================
# Fuzzy content overlap (ESC3) — for claim/stakes-style dimensions
# ============================================================================

# Generic function/content words that must not carry a fuzzy match on
# their own. (This is the Dramatic evaluator's stop-set, now shared.)
CONTENT_STOP = frozenset({
    "the", "of", "a", "an", "and", "to", "is", "that", "his", "her",
    "their", "by", "it", "what", "who", "they", "he", "she", "in", "as",
    "for", "be", "are", "or", "but", "not", "no", "than", "more", "most",
    "person", "man", "woman", "people", "story", "thing", "you",
})


def content_overlap(read: str, *authored: str) -> bool:
    """Fuzzy: do the reading's content tokens overlap the authored
    text(s)? Callers must LABEL dimensions scored this way as fuzzy, so
    a soft match is never mistaken for a crisp one."""
    r = tokens(read) - CONTENT_STOP
    if not r:
        return False
    a: set = set()
    for t in authored:
        a |= (tokens(t) - CONTENT_STOP)
    return bool(r & a)


# ============================================================================
# Authored-side name lookup (ESC3)
# ============================================================================


def char_name(ref_id: str, mythos) -> str:
    """Character id / substrate ref → readable name, for authored
    expectations."""
    for c in getattr(mythos, "characters", ()) or ():
        if getattr(c, "id", None) == ref_id or \
                getattr(c, "character_ref_id", None) == ref_id:
            return getattr(c, "name", ref_id)
    return ref_id
