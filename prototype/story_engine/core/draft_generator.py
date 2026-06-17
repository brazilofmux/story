"""
draft_generator.py — substrate → first-draft prose generator.

The first step toward the project's generation terminus (state-of-play-16
§What's next): turn a verified substrate encoding into a first-draft
prose rendering. The substrate is the SOURCE OF TRUTH; the LLM is the
prose renderer, not the author of record. This is the compiler back-end
the middle-end (substrate IR + dialect overlays + verifiers) was built
to feed.

Design:

- **The substrate drives the order.** Generation walks the SJUZHET
  (the staged narrative order, τ_d), NOT the FABULA (chronological
  order, τ_s). For Oedipus Tyrannus the two differ sharply — the play
  opens in medias res and reveals the past through interrogation — so
  the sjuzhet/fabula distinction is load-bearing for the draft.

- **A static story bible is cached.** The dramatis personae, the
  backstory world-facts, the audience's pre-play knowledge, and the
  phase / peripeteia / anagnorisis arc go in the system prompt (cached
  across scenes). Each scene is rendered from a per-scene BRIEF plus
  running continuity.

- **Each scene brief carries the structural facts the prose must
  honor:** the event's asserted world-facts, the knowledge changes
  (who comes to know/believe what — the engine of dramatic irony), the
  audience disclosures, the attached authorial descriptions (tone /
  intent), the focalization (POV), and whether the beat is the
  peripeteia or anagnorisis.

The generator is dialect-light: it takes the substrate (sjuzhet,
fabula, entities, descriptions) and an OPTIONAL ArMythos for the phase
and peripeteia/anagnorisis structure. Any encoding with a sjuzhet can
be rendered; the mythos sharpens the arc framing when present.

API key: reads `ANTHROPIC_API_KEY` from the environment (SDK default),
same as the reader-model clients.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

try:
    import anthropic
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "The draft generator requires the anthropic SDK. Install via "
        "`pip install -r prototype/requirements.txt`."
    ) from exc


# ============================================================================
# Result records
# ============================================================================


@dataclass(frozen=True)
class SceneDraft:
    """One rendered scene."""
    τ_d: int
    event_id: str
    focalizer: str            # display name or "(omniscient)"
    brief: str                # the structured brief handed to the model
    prose: str                # the rendered scene


@dataclass
class GenerationResult:
    """The full first draft plus its per-scene parts and the bible."""
    title: str
    story_bible: str
    scenes: list = field(default_factory=list)   # list[SceneDraft]

    @property
    def draft(self) -> str:
        """The assembled first draft, scenes joined in sjuzhet order."""
        return "\n\n".join(s.prose.strip() for s in self.scenes)


def result_to_payload(result) -> dict:
    """A JSON-serializable per-scene payload of a GenerationResult — the
    structured-draft artifact the convergence loop mutates and re-scores
    (a repaired scene's prose can be substituted and the draft
    reassembled). 'tau_d' uses an ASCII key for round-trip safety."""
    return {
        "title": result.title,
        "story_bible": result.story_bible,
        "scenes": [
            {"tau_d": s.τ_d, "event_id": s.event_id,
             "focalizer": s.focalizer, "prose": s.prose}
            for s in result.scenes
        ],
    }


# ============================================================================
# Substrate rendering helpers
# ============================================================================


def _name_map(entities) -> dict:
    return {e.id: e.name for e in entities}


def _nm(name_map: dict, eid: str) -> str:
    return name_map.get(eid, eid)


def _char_name(ref_id: str, mythos, name_map: dict) -> str:
    """Resolve a character reference (an ArCharacter id like 'ar_duchess',
    or a substrate-entity id) to a readable name. Prefers the ArCharacter
    record's own name, then its substrate identity hook, then the raw id.
    Keeps the generator dialect-light — works whether refs point at
    ArCharacter ids or substrate entity ids."""
    if not ref_id:
        return ref_id
    for c in getattr(mythos, "characters", ()) or ():
        if getattr(c, "id", None) == ref_id:
            return getattr(c, "name", None) or _nm(name_map, ref_id)
        if getattr(c, "character_ref_id", None) == ref_id:
            return getattr(c, "name", None) or _nm(name_map, ref_id)
    return _nm(name_map, ref_id)


def _render_prop(prop, name_map: dict) -> str:
    """Render a structural Prop as a readable predicate, entity args
    resolved to display names where known."""
    args = ", ".join(_nm(name_map, a) for a in prop.args)
    return f"{prop.predicate}({args})"


def _world_facts(event, name_map: dict) -> list:
    """The world-facts this event asserts (and retracts)."""
    out = []
    for eff in event.effects:
        prop = getattr(eff, "prop", None)
        if prop is None:
            continue
        # WorldEffect has .asserts; KnowledgeEffect routes through .held.
        if hasattr(eff, "asserts"):
            verb = "asserts" if eff.asserts else "retracts"
            out.append(f"{verb}: {_render_prop(prop, name_map)}")
    return out


def _knowledge_changes(event, name_map: dict) -> list:
    """Who comes to know / believe / lose what at this event — the
    engine of dramatic irony."""
    out = []
    for eff in event.effects:
        held = getattr(eff, "held", None)
        agent = getattr(eff, "agent_id", None)
        if held is None or agent is None:
            continue
        slot = getattr(held, "slot", None)
        slot_name = getattr(slot, "name", str(slot)).lower()
        verb = "loses belief" if getattr(eff, "remove", False) else "comes to"
        rel = "know" if slot_name == "known" else slot_name
        prop_txt = _render_prop(held.prop, name_map) if held.prop else "(unspecified)"
        out.append(f"{_nm(name_map, agent)} {verb} {rel}: {prop_txt}")
    return out


def _disclosures_text(entry, name_map: dict) -> list:
    out = []
    for d in getattr(entry, "disclosures", ()) or ():
        prop = getattr(d, "prop", None)
        if prop is not None:
            out.append(_render_prop(prop, name_map))
    return out


# ============================================================================
# Story bible (static, cached in the system prompt)
# ============================================================================


def _backstory_facts(sjuzhet, fabula, name_map: dict) -> list:
    """World-facts asserted by events that occur BEFORE the staged
    action begins — the backstory the audience holds (and that the
    play reveals). Defined as fabula events whose τ_s precedes the
    earliest non-anchor staged event's τ_s."""
    staged_ids = {e.event_id for e in sjuzhet}
    staged_τ = [
        ev.τ_s for ev in fabula
        if ev.id in staged_ids and ev.τ_s >= 0
    ]
    cutoff = min(staged_τ) if staged_τ else 0
    facts = []
    for ev in sorted(fabula, key=lambda e: e.τ_s):
        if ev.τ_s >= cutoff:
            continue
        for f in _world_facts(ev, name_map):
            if f.startswith("asserts: "):
                facts.append(f[len("asserts: "):])
    return facts


def build_story_bible(
    *,
    title: str,
    sjuzhet,
    fabula,
    entities,
    mythos=None,
    preplay_disclosures=(),
    dialect_note: str = "",
) -> str:
    name_map = _name_map(entities)
    lines = []
    lines.append(f"# STORY BIBLE — {title}")
    if dialect_note:
        lines.append(f"\nFrame: {dialect_note}")

    # Dramatis personae (agents).
    agents = [e for e in entities if getattr(e, "kind", "") == "agent"]
    lines.append("\n## Dramatis personae")
    for a in agents:
        lines.append(f"- {a.name} (id: {a.id})")

    # Backstory the audience holds entering the play.
    backstory = _backstory_facts(sjuzhet, fabula, name_map)
    if backstory:
        lines.append("\n## Backstory (true before the staged action; "
                     "the play reveals it)")
        for f in backstory:
            lines.append(f"- {f}")

    # The audience's pre-play knowledge (dramatic-irony baseline).
    pre = [
        _render_prop(d.prop, name_map)
        for d in preplay_disclosures
        if getattr(d, "prop", None) is not None
    ]
    if pre:
        lines.append("\n## What the AUDIENCE knows entering (the "
                     "characters may not — this is the irony engine)")
        for p in pre:
            lines.append(f"- {p}")

    # The arc (from the mythos if present).
    if mythos is not None:
        lines.append("\n## Dramatic arc")
        if getattr(mythos, "action_summary", ""):
            lines.append(mythos.action_summary)
        peri = getattr(mythos, "peripeteia_event_id", None)
        anag = getattr(mythos, "anagnorisis_event_id", None)
        if peri:
            lines.append(f"\n- PERIPETEIA (the reversal) lands at: {peri}")
        if anag:
            lines.append(f"- ANAGNORISIS (the recognition) lands at: {anag}")
        # A19 (sketch-06) — secondary reversals, for mythoi carrying
        # multiple tragic arcs (Malfi's four; Lear's Gloucester). Surfaced
        # only when present; single-arc plays (Oedipus) skip this.
        secondary = getattr(mythos, "secondary_peripeteia_event_ids", ()) or ()
        if secondary:
            lines.append(
                f"- SECONDARY REVERSALS (other arcs falling): "
                f"{', '.join(secondary)}"
            )
        # A11/A14/A20 (sketch-02/03/06) — the staggered recognition chain,
        # incl. anti-recognitions (real but too late to alter outcome).
        chain = getattr(mythos, "anagnorisis_chain", ()) or ()
        if chain:
            lines.append("\n## Staggered recognitions (the chain)")
            for step in chain:
                who = _char_name(getattr(step, "character_ref_id", ""),
                                 mythos, name_map)
                qual = getattr(step, "anagnorisis_qualifier", "") or ""
                tag = ""
                if qual == "anti":
                    tag = " — an ANTI-recognition: real, but arrives too " \
                          "late to change anything"
                elif qual == "partial":
                    tag = " — a PARTIAL recognition (incomplete grasp)"
                lines.append(
                    f"- {who} recognizes at {getattr(step, 'event_id', '?')}"
                    f"{tag}"
                )
        # A22 (sketch-07) — the pathos-centre: who carries the play's
        # pity-and-fear. Distinct from the recognizer when the play splits
        # them (Malfi: the Duchess suffers, Ferdinand recognizes).
        pathos = getattr(mythos, "pathos_character_ref_ids", ()) or ()
        if pathos:
            names = ", ".join(_char_name(p, mythos, name_map) for p in pathos)
            lines.append(
                f"\n## Pathos-centre (the play's pity-and-fear lives here)\n"
                f"- {names} — render their suffering as the emotional centre, "
                f"even where they are not the one who comes to knowledge"
            )
        # A5 (sketch-01) — the tragic hero(es) and their hamartia. The
        # error of judgement that drives the fall; rich generation input.
        chars = getattr(mythos, "characters", ()) or ()
        heroes = [c for c in chars if getattr(c, "is_tragic_hero", False)]
        if heroes:
            lines.append("\n## Tragic hero(es) and the error that undoes them")
            for c in heroes:
                ham = getattr(c, "hamartia_text", None)
                base = getattr(c, "name", c.id)
                if getattr(c, "pathos_carrier", False):
                    base += " (also the pathos-centre)"
                if ham:
                    lines.append(f"- {base}: {ham}")
                else:
                    lines.append(f"- {base}")
        phases = getattr(mythos, "phases", ()) or ()
        if phases:
            lines.append("\n## Phase structure")
            for ph in phases:
                role = getattr(ph, "role", "?")
                lines.append(f"- {role}: {', '.join(ph.scope_event_ids)}")
    return "\n".join(lines)


SYSTEM_PROMPT_TEMPLATE = """\
You are a dramatist rendering a VERIFIED story structure into a \
first-draft prose script. The structure below is the source of truth, \
produced by a story-telling engine; your job is to render it, not to \
re-author it.

Ground rules:
1. Render the beat the scene brief describes. Do NOT invent events, \
characters, deaths, or revelations that are not in the brief or bible. \
You may invent dialogue, staging, sensory texture, and connective \
tissue that SERVE the given facts.
2. Honor focalization. When a focalizer is named, write in close third \
person anchored to that character's perception; when omniscient, write \
with a dramatist's external eye (or a chorus/narrator voice if it fits \
the frame).
3. Honor the knowledge state. Characters act ONLY on what they know at \
this beat. Where the audience knows something a character does not \
(see the bible's irony baseline), let the scene carry that irony — but \
never let an ignorant character speak as if informed.
4. Honor the authorial descriptions attached to a beat — they encode \
intended tone and reading.
5. The PERIPETEIA and ANAGNORISIS beats carry the play's structural \
weight; render them with the force the arc demands.
6. Maintain continuity with the story so far.

Output ONLY the scene's prose. No headings, no meta-commentary, no \
stage directions in brackets unless they read as part of the prose.

{bible}
"""


# ============================================================================
# Scene brief
# ============================================================================


def build_scene_brief(
    *,
    entry,
    fabula_by_id: dict,
    name_map: dict,
    phase_role: Optional[str],
    is_peripeteia: bool,
    is_anagnorisis: bool,
    descriptions_for_event: list,
    is_secondary_peripeteia: bool = False,
    chain_step=None,
    mythos=None,
) -> str:
    event = fabula_by_id.get(entry.event_id)
    lines = []
    lines.append(f"SCENE (τ_d={entry.τ_d}) — event {entry.event_id}")
    if phase_role:
        lines.append(f"Phase: {phase_role}")
    marks = []
    if is_peripeteia:
        marks.append("THIS IS THE PERIPETEIA (the reversal)")
    if is_anagnorisis:
        marks.append("THIS IS THE ANAGNORISIS (the recognition)")
    if is_secondary_peripeteia:
        marks.append("THIS IS A SECONDARY REVERSAL (another arc falling "
                     "here — give it weight, but not the main reversal's)")
    if chain_step is not None:
        who = _char_name(getattr(chain_step, "character_ref_id", ""),
                         mythos, name_map)
        qual = getattr(chain_step, "anagnorisis_qualifier", "") or ""
        if qual == "anti":
            marks.append(f"{who} RECOGNIZES here — but it is an "
                         f"ANTI-recognition: the truth lands too late to "
                         f"change the outcome (render the bitterness of "
                         f"recognition-without-remedy)")
        elif qual == "partial":
            marks.append(f"{who} PARTIALLY recognizes here (an incomplete "
                         f"grasp of the truth)")
        else:
            marks.append(f"{who} RECOGNIZES here (a staggered recognition "
                         f"in the chain)")
    if marks:
        lines.append("** " + "; ".join(marks) + " **")

    foc = getattr(entry, "focalizer_id", None)
    lines.append(f"Focalization: {_nm(name_map, foc) if foc else '(omniscient)'}")

    if event is not None:
        lines.append(f"Event type: {event.type}")
        if event.participants:
            parts = ", ".join(
                f"{role}={_nm(name_map, eid)}"
                for role, eid in event.participants.items()
            )
            lines.append(f"Participants: {parts}")
        facts = _world_facts(event, name_map)
        if facts:
            lines.append("What becomes true (render these as the beat's "
                         "events):")
            for f in facts:
                lines.append(f"  - {f}")
        kc = _knowledge_changes(event, name_map)
        if kc:
            lines.append("Knowledge changes (who learns/loses what):")
            for k in kc:
                lines.append(f"  - {k}")

    disc = _disclosures_text(entry, name_map)
    if disc:
        lines.append("The AUDIENCE learns this beat:")
        for d in disc:
            lines.append(f"  - {d}")

    for d in descriptions_for_event:
        lines.append(f"Authorial note ({d.kind}): {d.text}")

    return "\n".join(lines)


# ============================================================================
# Generation
# ============================================================================


def _scene_synopsis(entry, fabula_by_id: dict, name_map: dict) -> str:
    """A one-line terse beat-summary for the running 'story so far'."""
    event = fabula_by_id.get(entry.event_id)
    if event is None:
        return entry.event_id
    parts = " / ".join(
        _nm(name_map, eid) for eid in event.participants.values()
    )
    return f"{event.type}: {parts}".strip(" :/")


def _extract_text(response) -> str:
    out = []
    for block in getattr(response, "content", []) or []:
        if getattr(block, "type", None) == "text":
            out.append(block.text)
    return "".join(out).strip()


def _scene_structural_flags(entry, mythos):
    """Recompute the per-scene structural lookups (phase, peripeteia,
    anagnorisis, secondary peripeteia, chain step) for one sjuzhet entry
    from the mythos — the same lookups `generate_draft`'s loop computes,
    factored so a single scene can be (re-)rendered in isolation."""
    phase_role = None
    is_peri = is_anag = is_sec = False
    chain_step = None
    if mythos is not None:
        for ph in getattr(mythos, "phases", ()) or ():
            if entry.event_id in getattr(ph, "scope_event_ids", ()):
                phase_role = getattr(ph, "role", None)
        is_peri = entry.event_id == getattr(mythos, "peripeteia_event_id", None)
        is_anag = entry.event_id == getattr(mythos, "anagnorisis_event_id", None)
        is_sec = entry.event_id in (
            getattr(mythos, "secondary_peripeteia_event_ids", ()) or ()
        )
        for s in getattr(mythos, "anagnorisis_chain", ()) or ():
            if getattr(s, "event_id", None) == entry.event_id:
                chain_step = s
    return phase_role, is_peri, is_anag, is_sec, chain_step


def render_scene_prose(
    *,
    entry,
    sjuzhet,
    fabula,
    entities,
    descriptions=(),
    mythos=None,
    preplay_disclosures=(),
    title: str = "",
    dialect_note: str = "",
    story_so_far: str = "",
    extra_directive: str = "",
    model: str = "claude-opus-4-6",
    effort: str = "medium",
    max_tokens: int = 4000,
    client: Optional["anthropic.Anthropic"] = None,
) -> str:
    """Render (or RE-render) a single sjuzhet scene in isolation, with
    the full story bible for context and an optional `extra_directive`
    appended to the scene brief. This is the primitive the repair loop
    uses: given a structural drift, re-render the responsible scene with
    a corrective directive, keeping the same bible + brief the original
    generation used.

    `sjuzhet` is the FULL staged order (for the bible's backstory /
    irony baseline); `entry` is the one scene to render."""
    name_map = _name_map(entities)
    fabula_by_id = {e.id: e for e in fabula}

    phase_role, is_peri, is_anag, is_sec, chain_step = \
        _scene_structural_flags(entry, mythos)

    descs_for_event = [
        d for d in descriptions
        if getattr(getattr(d, "attached_to", None), "target_id", None)
        == entry.event_id
    ]

    brief = build_scene_brief(
        entry=entry,
        fabula_by_id=fabula_by_id,
        name_map=name_map,
        phase_role=phase_role,
        is_peripeteia=is_peri,
        is_anagnorisis=is_anag,
        is_secondary_peripeteia=is_sec,
        chain_step=chain_step,
        mythos=mythos,
        descriptions_for_event=descs_for_event,
    )
    if extra_directive:
        brief = (brief + "\n\n** REVISION DIRECTIVE (a prior draft of this "
                 "beat drifted from the structure; honor this) **\n"
                 + extra_directive)

    bible = build_story_bible(
        title=title, sjuzhet=sjuzhet, fabula=fabula, entities=entities,
        mythos=mythos, preplay_disclosures=preplay_disclosures,
        dialect_note=dialect_note,
    )
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(bible=bible)

    sof = story_so_far or "STORY SO FAR: (render this beat in isolation)"
    user_prompt = (
        f"{sof}\n\nRender the scene now, from this brief:\n\n{brief}"
    )

    if client is None:
        client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        output_config={"effort": effort},
        system=[{
            "type": "text", "text": system_prompt,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": user_prompt}],
    )
    return _extract_text(response)


def generate_draft(
    *,
    title: str,
    sjuzhet,
    fabula,
    entities,
    descriptions=(),
    mythos=None,
    preplay_disclosures=(),
    dialect_note: str = "",
    model: str = "claude-opus-4-6",
    effort: str = "medium",
    max_tokens: int = 4000,
    dry_run: bool = False,
    on_scene=None,             # optional callback(SceneDraft) for progress
    client: Optional["anthropic.Anthropic"] = None,
) -> GenerationResult:
    """Render the encoding's sjuzhet into a first-draft prose script,
    scene by scene, substrate-driven.

    `dry_run=True` builds the bible and per-scene briefs and returns
    them WITHOUT calling the API (each SceneDraft.prose is empty) — for
    inspecting exactly what the substrate hands the renderer.
    """
    name_map = _name_map(entities)
    fabula_by_id = {e.id: e for e in fabula}

    # Phase + peripeteia/anagnorisis lookup from the mythos.
    phase_of: dict = {}
    peri_id = anag_id = None
    secondary_peri: set = set()
    chain_by_event: dict = {}
    if mythos is not None:
        for ph in getattr(mythos, "phases", ()) or ():
            for eid in ph.scope_event_ids:
                phase_of[eid] = getattr(ph, "role", None)
        peri_id = getattr(mythos, "peripeteia_event_id", None)
        anag_id = getattr(mythos, "anagnorisis_event_id", None)
        secondary_peri = set(
            getattr(mythos, "secondary_peripeteia_event_ids", ()) or ()
        )
        for step in getattr(mythos, "anagnorisis_chain", ()) or ():
            eid = getattr(step, "event_id", None)
            if eid:
                chain_by_event[eid] = step

    # Descriptions grouped by anchored event id.
    descs_by_event: dict = {}
    for d in descriptions:
        anchor = getattr(d, "attached_to", None)
        target = getattr(anchor, "target_id", None)
        if target:
            descs_by_event.setdefault(target, []).append(d)

    bible = build_story_bible(
        title=title, sjuzhet=sjuzhet, fabula=fabula, entities=entities,
        mythos=mythos, preplay_disclosures=preplay_disclosures,
        dialect_note=dialect_note,
    )
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(bible=bible)

    result = GenerationResult(title=title, story_bible=bible)

    ordered = sorted(sjuzhet, key=lambda e: e.τ_d)
    synopsis_so_far: list = []

    if client is None and not dry_run:
        client = anthropic.Anthropic()

    for entry in ordered:
        brief = build_scene_brief(
            entry=entry,
            fabula_by_id=fabula_by_id,
            name_map=name_map,
            phase_role=phase_of.get(entry.event_id),
            is_peripeteia=(entry.event_id == peri_id),
            is_anagnorisis=(entry.event_id == anag_id),
            is_secondary_peripeteia=(entry.event_id in secondary_peri),
            chain_step=chain_by_event.get(entry.event_id),
            mythos=mythos,
            descriptions_for_event=descs_by_event.get(entry.event_id, []),
        )
        foc = getattr(entry, "focalizer_id", None)
        foc_name = _nm(name_map, foc) if foc else "(omniscient)"

        if dry_run:
            scene = SceneDraft(
                τ_d=entry.τ_d, event_id=entry.event_id,
                focalizer=foc_name, brief=brief, prose="",
            )
            result.scenes.append(scene)
            if on_scene:
                on_scene(scene)
            continue

        story_so_far = (
            "STORY SO FAR (beats already rendered, in order):\n"
            + "\n".join(f"  {i+1}. {s}" for i, s in enumerate(synopsis_so_far))
            if synopsis_so_far else
            "STORY SO FAR: (this is the opening beat)"
        )
        prev_prose = (
            "\n\nThe immediately preceding scene's prose (for voice + "
            "continuity):\n" + result.scenes[-1].prose
            if result.scenes else ""
        )
        user_prompt = (
            f"{story_so_far}{prev_prose}\n\n"
            f"Render the next scene now, from this brief:\n\n{brief}"
        )

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            thinking={"type": "adaptive"},
            output_config={"effort": effort},
            system=[{
                "type": "text", "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user_prompt}],
        )
        prose = _extract_text(response)
        scene = SceneDraft(
            τ_d=entry.τ_d, event_id=entry.event_id,
            focalizer=foc_name, brief=brief, prose=prose,
        )
        result.scenes.append(scene)
        synopsis_so_far.append(
            _scene_synopsis(entry, fabula_by_id, name_map)
        )
        if on_scene:
            on_scene(scene)

    return result
