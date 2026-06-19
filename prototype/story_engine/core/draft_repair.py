"""
draft_repair.py — close the generate → evaluate → REPAIR loop.

The evaluator (`draft_evaluator.py`) finds where a generated draft's
prose drifted from the substrate it was generated from. This module
turns those findings into targeted scene re-renders: it maps each
localizable structural loss back to the substrate event that carries it,
builds a corrective directive, and re-renders that one scene with the
directive appended — keeping the rest of the draft intact.

The engine improving its own output against the source of truth:
generate (substrate → prose) → evaluate (prose → fidelity) → repair
(re-render the drifted beats) → re-evaluate.

`plan_repairs` is pure Python (offline-testable): a `FidelityReport`
plus the authored mythos in, a list of `RepairDirective` out. Only
*localizable* losses become directives — an anti-recognition or a
main-recognition drift maps cleanly to one substrate event; a diffuse
loss (e.g. a thinned pathos-texture spread over many scenes) does not
and is reported as unrepairable-here rather than forced onto a scene.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from story_engine.core.llm import DEFAULT_MODEL

from story_engine.core.draft_generator import (
    render_scene_prose, _scene_synopsis, _name_map,
)


@dataclass(frozen=True)
class RepairDirective:
    """A targeted corrective re-render: which scene (event), which
    structural dimension it restores, and the directive text to append
    to that scene's brief."""
    event_id: str
    dimension: str
    instruction: str
    authored: str = ""        # the authored fact being restored


def _char_name(ref_id: str, mythos) -> str:
    for c in getattr(mythos, "characters", ()) or ():
        if getattr(c, "id", None) == ref_id or \
                getattr(c, "character_ref_id", None) == ref_id:
            return getattr(c, "name", ref_id)
    return ref_id


def plan_repairs(report, mythos) -> list:
    """Map a FidelityReport's localizable losses to RepairDirectives.

    Currently repairs two cleanly-localizable dimensions:
    - `anti_recognition` lost → the chain step's event: insist the
      authored character ALSO recognizes (mutual, too-late).
    - `anagnorisis_character` lost/drifted → the main anagnorisis event:
      insist the recognition lands on the authored recognizer.

    Diffuse dimensions (pathos_centre, tragic_hero, secondary_reversals)
    are NOT forced onto a single scene — they are skipped here and remain
    visible in the report. Returns possibly-empty list."""
    out: list = []
    chain = getattr(mythos, "anagnorisis_chain", ()) or ()

    for f in getattr(report, "findings", []):
        if f.dimension == "anti_recognition" and f.verdict == "lost":
            for step in chain:
                if (getattr(step, "anagnorisis_qualifier", "") or "").lower() \
                        != "anti":
                    continue
                who = _char_name(getattr(step, "character_ref_id", ""), mythos)
                if who and who in f.authored:
                    out.append(RepairDirective(
                        event_id=getattr(step, "event_id", ""),
                        dimension="anti_recognition",
                        authored=f"{who} (anti-recognition)",
                        instruction=(
                            f"{who} must ALSO come to recognition at this "
                            f"beat — the recognition is MUTUAL and lands in "
                            f"the SAME instant as the mortal blow. Do NOT let "
                            f"{who} die unknowing or pass the recognition to "
                            f"another character. {who} must see, too late to "
                            f"change anything, the truth of who strikes and "
                            f"why — a recognition that is real but powerless "
                            f"to alter the outcome (an anti-recognition)."
                        ),
                    ))

        if f.dimension == "anagnorisis_character" and \
                f.verdict in ("lost", "drifted"):
            anag_event = getattr(mythos, "anagnorisis_event_id", None)
            if anag_event:
                out.append(RepairDirective(
                    event_id=anag_event,
                    dimension="anagnorisis_character",
                    authored=f.authored,
                    instruction=(
                        f"The main recognition at this beat belongs to "
                        f"{f.authored}. Render {f.authored}'s move from "
                        f"ignorance to knowledge as the structural weight of "
                        f"the scene; do not let another character's reaction "
                        f"displace it."
                    ),
                ))

    # De-duplicate directives that target the same event+dimension.
    seen = set()
    deduped = []
    for d in out:
        key = (d.event_id, d.dimension)
        if key not in seen:
            seen.add(key)
            deduped.append(d)
    return deduped


def build_story_so_far(sjuzhet, fabula, entities, *, up_to_τ_d: int) -> str:
    """A terse 'story so far' for an isolated re-render: the beats
    staged before the target scene, in sjuzhet order. Pure Python."""
    name_map = _name_map(entities)
    fabula_by_id = {e.id: e for e in fabula}
    prior = sorted(
        (e for e in sjuzhet if e.τ_d < up_to_τ_d), key=lambda e: e.τ_d
    )
    if not prior:
        return "STORY SO FAR: (this is the opening beat)"
    lines = [
        f"  {i+1}. {_scene_synopsis(e, fabula_by_id, name_map)}"
        for i, e in enumerate(prior)
    ]
    return "STORY SO FAR (beats already staged, in order):\n" + "\n".join(lines)


@dataclass
class RepairResult:
    """One scene's before/after repair."""
    directive: RepairDirective
    τ_d: int
    before: str = ""
    after: str = ""


def repair_scene(
    directive,
    *,
    sjuzhet,
    fabula,
    entities,
    descriptions=(),
    mythos=None,
    adapter=None,
    preplay_disclosures=(),
    title: str = "",
    dialect_note: str = "",
    before: str = "",
    model: str = DEFAULT_MODEL,
    effort: str = "medium",
    max_tokens: int = 4000,
    client=None,
) -> Optional[RepairResult]:
    """Re-render the scene a directive targets, with the corrective
    directive appended. Returns a RepairResult (before/after), or None
    if the directive's event is not in the sjuzhet. Dialect-agnostic:
    pass `mythos` (Aristotelian) OR `adapter` (any DialectFrame, e.g.
    Dramatica) — whichever the draft was generated with."""
    entry = next(
        (e for e in sjuzhet if e.event_id == directive.event_id), None
    )
    if entry is None:
        return None
    story_so_far = build_story_so_far(
        sjuzhet, fabula, entities, up_to_τ_d=entry.τ_d
    )
    after = render_scene_prose(
        entry=entry,
        sjuzhet=sjuzhet,
        fabula=fabula,
        entities=entities,
        descriptions=descriptions,
        mythos=mythos,
        adapter=adapter,
        preplay_disclosures=preplay_disclosures,
        title=title,
        dialect_note=dialect_note,
        story_so_far=story_so_far,
        extra_directive=directive.instruction,
        model=model,
        effort=effort,
        max_tokens=max_tokens,
        client=client,
    )
    return RepairResult(
        directive=directive, τ_d=entry.τ_d, before=before, after=after,
    )
