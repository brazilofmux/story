"""
authoring.py — the human front-end: a plain-text story format that
compiles to the verified substrate + Aristotelian overlay the engine
already consumes.

The thesis the engine proved is "a verified structural substrate drives
faithful generation." Until now that substrate was authored in Python.
This module lets a writer author it in a friendly `.story.toml` file
instead — no code — and compiles it to the same objects the generator,
evaluator, repair, and convergence loops take. The substrate stays the
source of truth; only the authoring surface changes.

The format (see `samples/*.story.toml` for a worked example):

    title    = "..."
    logline  = "..."
    telling  = "chronological" | "reverse" | "explicit"   # staging order
    # for "explicit": add  staging = ["event_id", ...]
    preplay  = ["fact(arg)", ...]        # what the audience knows entering

    [[characters]]
    id = "halvard"; name = "Halvard"
    role = "tragic-hero" | "pathos-centre" | "figure"
    hamartia = "..."                     # tragic-hero only, optional

    [[places]]                           # optional
    id = "vantage_light"; name = "the Vantage Light"

    [[events]]
    id = "ship_founders"; when = 9       # when = story-time τ_s
    who = ["captain", "halvard"]         # participants (character/place ids)
    roles = ["captain", "keeper"]        # optional, parallel to `who`
    focalizer = "captain"                # optional POV; omit = omniscient
    mark = "peripeteia" | "anagnorisis"  # optional structural mark
    recognizer = "halvard"               # on the anagnorisis event, optional
    summary = "..."                      # the beat, plain prose
    note = "..."                         # optional authorial reader-frame
    establishes = ["ship_wrecked(captain)", ...]   # optional world facts

    [[anti_recognitions]]                # optional: recognition-too-late
    at = "ship_founders"; who = "captain"

    [phases]
    beginning = ["...", ...]
    middle    = ["...", ...]
    end       = ["...", ...]

`compile_story(doc)` returns a `CompiledStory` carrying the same exports
an encoding module would (ENTITIES, FABULA, SJUZHET, DESCRIPTIONS,
PREPLAY_DISCLOSURES, mythos). `verify_compiled(...)` runs the dialect
self-verifier so the author gets the same structural feedback the Python
encodings get — author, verify, fix, generate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from story_engine.core.substrate import (
    Entity, Prop, Event, Slot, Confidence, Diegetic, Narrative,
    Held, KnowledgeEffect, WorldEffect, SjuzhetEntry, Disclosure,
    Description, Attention, anchor_event,
)
from story_engine.core.aristotelian import (
    ArMythos, ArPhase, ArCharacter, ArAnagnorisisStep,
    PHASE_BEGINNING, PHASE_MIDDLE, PHASE_END,
    PLOT_SIMPLE, PLOT_COMPLEX,
    BINDING_COINCIDENT, BINDING_ADJACENT, BINDING_SEPARATED,
    QUALIFIER_ANTI,
    verify,
)


class StoryFormatError(ValueError):
    """A human-facing authoring error — phrased for a writer, not a
    stack trace. Raised when the .story.toml is structurally unusable
    before the dialect verifier even runs (a missing field, an event id
    referenced that does not exist, an event in no phase or two)."""


@dataclass
class CompiledStory:
    """Everything an encoding module exports, produced from a
    .story.toml — ready for the generator / evaluator / verifier."""
    title: str
    logline: str
    entities: list = field(default_factory=list)
    fabula: list = field(default_factory=list)
    sjuzhet: list = field(default_factory=list)
    descriptions: list = field(default_factory=list)
    preplay_disclosures: tuple = ()
    mythos: object = None


# ----------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------

def _parse_prop(s: str) -> Prop:
    """Parse a plain predicate string like 'record_unbroken(halvard)' or
    'storm_active()' into a Prop."""
    s = s.strip()
    if "(" not in s or not s.endswith(")"):
        raise StoryFormatError(
            f"fact {s!r} must look like predicate(arg, arg) or predicate()"
        )
    pred, rest = s[:-1].split("(", 1)
    args = tuple(a.strip() for a in rest.split(",") if a.strip())
    return Prop(pred.strip(), args)


def _require(doc: dict, key: str, where: str):
    if key not in doc:
        raise StoryFormatError(f"{where} is missing the required '{key}'")
    return doc[key]


def _ar_id(char_id: str) -> str:
    return f"ar_{char_id}"


# ----------------------------------------------------------------------------
# Compile
# ----------------------------------------------------------------------------

def compile_story(doc: dict) -> CompiledStory:
    """Compile a parsed .story.toml document into a CompiledStory."""
    title = _require(doc, "title", "the story")
    logline = doc.get("logline", "")

    raw_chars = doc.get("characters", [])
    raw_events = doc.get("events", [])
    raw_places = doc.get("places", [])
    if not raw_events:
        raise StoryFormatError("the story has no [[events]]")
    if not raw_chars:
        raise StoryFormatError("the story has no [[characters]]")

    # --- Entities (agents from characters, locations from places) ---
    entities = []
    char_by_id = {}
    for c in raw_chars:
        cid = _require(c, "id", "a character")
        entities.append(Entity(id=cid, name=c.get("name", cid), kind="agent"))
        char_by_id[cid] = c
    for p in raw_places:
        pid = _require(p, "id", "a place")
        entities.append(Entity(id=pid, name=p.get("name", pid), kind="location"))

    valid_ids = {e.id for e in entities}

    # --- Fabula + per-event descriptions ---
    fabula = []
    descriptions = []
    event_ids = []
    desc_seq = 1000
    for i, ev in enumerate(raw_events, start=1):
        eid = _require(ev, "id", f"event #{i}")
        if eid in event_ids:
            raise StoryFormatError(f"duplicate event id {eid!r}")
        when = ev.get("when")
        if when is None:
            raise StoryFormatError(f"event {eid!r} needs a 'when' (story-time)")
        who = ev.get("who", [])
        roles = ev.get("roles", [])
        for w in who:
            if w not in valid_ids:
                raise StoryFormatError(
                    f"event {eid!r} names participant {w!r} which is not a "
                    f"declared character or place")
        participants = {}
        for j, w in enumerate(who):
            role = roles[j] if j < len(roles) else f"participant_{j + 1}"
            participants[role] = w

        effects = []
        for fact in ev.get("establishes", []):
            effects.append(WorldEffect(prop=_parse_prop(fact), asserts=True))
        # A light knowledge anchor so the brief has a focalizer-held fact.
        foc = ev.get("focalizer")
        if foc and foc in valid_ids and ev.get("summary"):
            effects.append(KnowledgeEffect(
                agent_id=foc,
                held=Held(prop=Prop("witnesses", (eid,)), slot=Slot.KNOWN,
                          confidence=Confidence.CERTAIN,
                          via=Diegetic.OBSERVATION.value,
                          provenance=(f"focalized @ τ_s={when}",)),
            ))

        fabula.append(Event(
            id=eid, type=ev.get("mark") or ev.get("type", "beat"),
            τ_s=int(when), τ_a=i,
            participants=participants, effects=tuple(effects),
        ))
        event_ids.append(eid)

        if ev.get("summary"):
            descriptions.append(Description(
                id=f"D_{eid}_beat", attached_to=anchor_event(eid),
                kind="beat", attention=Attention.STRUCTURAL,
                text=ev["summary"], authored_by="author", τ_a=desc_seq))
            desc_seq += 1
        if ev.get("note"):
            descriptions.append(Description(
                id=f"D_{eid}_note", attached_to=anchor_event(eid),
                kind="reader-frame", attention=Attention.INTERPRETIVE,
                text=ev["note"], authored_by="author", τ_a=desc_seq))
            desc_seq += 1

    event_id_set = set(event_ids)
    by_when = {e.id: e.τ_s for e in fabula}

    # --- Preplay disclosures ---
    preplay = tuple(
        Disclosure(prop=_parse_prop(f), slot=Slot.KNOWN,
                   confidence=Confidence.CERTAIN, via=Narrative.DISCLOSURE.value)
        for f in doc.get("preplay", [])
    )

    # --- Sjuzhet (staging order) ---
    telling = doc.get("telling", "chronological").strip().lower()
    if telling == "explicit":
        order = doc.get("staging")
        if not order:
            raise StoryFormatError(
                "telling = 'explicit' requires a staging = [...] list")
    elif telling == "reverse":
        order = sorted(event_ids, key=lambda e: by_when[e], reverse=True)
    elif telling == "chronological":
        order = sorted(event_ids, key=lambda e: by_when[e])
    else:
        raise StoryFormatError(
            f"telling {telling!r} must be 'chronological', 'reverse', or "
            f"'explicit'")
    for e in order:
        if e not in event_id_set:
            raise StoryFormatError(f"staging names unknown event {e!r}")

    foc_by_event = {ev["id"]: ev.get("focalizer") for ev in raw_events}
    sjuzhet = []
    for td, eid in enumerate(order):
        sjuzhet.append(SjuzhetEntry(
            event_id=eid, τ_d=td,
            focalizer_id=foc_by_event.get(eid),
            disclosures=preplay if td == 0 else (),
        ))

    # --- Overlay: characters ---
    ar_chars = []
    pathos_ids = []
    hero_ids = []
    for c in raw_chars:
        role = c.get("role", "figure").strip().lower()
        is_hero = role == "tragic-hero"
        is_pathos = role == "pathos-centre"
        if is_hero:
            hero_ids.append(c["id"])
        if is_pathos:
            pathos_ids.append(_ar_id(c["id"]))
        ar_chars.append(ArCharacter(
            id=_ar_id(c["id"]), name=c.get("name", c["id"]),
            character_ref_id=c["id"],
            hamartia_text=c.get("hamartia"),
            is_tragic_hero=is_hero,
            pathos_carrier=is_pathos,
        ))

    # --- Overlay: phases ---
    phases_doc = _require(doc, "phases", "the story")
    phase_map = [
        (PHASE_BEGINNING, phases_doc.get("beginning", [])),
        (PHASE_MIDDLE, phases_doc.get("middle", [])),
        (PHASE_END, phases_doc.get("end", [])),
    ]
    seen = {}
    for role, ids in phase_map:
        for eid in ids:
            if eid not in event_id_set:
                raise StoryFormatError(
                    f"phase {role!r} names unknown event {eid!r}")
            if eid in seen:
                raise StoryFormatError(
                    f"event {eid!r} is in two phases ({seen[eid]} and {role})")
            seen[eid] = role
    unphased = event_id_set - set(seen)
    if unphased:
        raise StoryFormatError(
            f"these events are in no phase: {', '.join(sorted(unphased))}")
    ar_phases = tuple(
        ArPhase(id=f"ph_{role}", role=role, scope_event_ids=tuple(ids))
        for role, ids in phase_map if ids
    )

    # --- Overlay: marks (peripeteia / anagnorisis) ---
    peri = [ev["id"] for ev in raw_events if ev.get("mark") == "peripeteia"]
    anag = [ev["id"] for ev in raw_events if ev.get("mark") == "anagnorisis"]
    peripeteia_id = peri[0] if peri else None
    anagnorisis_id = anag[0] if anag else None

    recognizer = None
    for ev in raw_events:
        if ev.get("mark") == "anagnorisis" and ev.get("recognizer"):
            recognizer = _ar_id(ev["recognizer"])
    if recognizer is None and hero_ids:
        recognizer = _ar_id(hero_ids[0])

    # --- Overlay: binding (computed from τ_s distance) ---
    binding = None
    if peripeteia_id and anagnorisis_id:
        d = abs(by_when[peripeteia_id] - by_when[anagnorisis_id])
        binding = (BINDING_COINCIDENT if d == 0
                   else BINDING_ADJACENT if d <= 3
                   else BINDING_SEPARATED)

    # --- Overlay: anti-recognition chain ---
    chain = []
    for ar in doc.get("anti_recognitions", []):
        at = _require(ar, "at", "an anti_recognition")
        who = _require(ar, "who", "an anti_recognition")
        if at not in event_id_set:
            raise StoryFormatError(f"anti_recognition names unknown event {at!r}")
        chain.append(ArAnagnorisisStep(
            id=f"arstep_{who}_{at}", event_id=at, character_ref_id=_ar_id(who),
            precipitates_main=False, anagnorisis_qualifier=QUALIFIER_ANTI,
            annotation=ar.get("note", ""),
        ))

    # central events in phase order (beginning→middle→end)
    central = tuple(eid for _, ids in phase_map for eid in ids)

    plot_kind = PLOT_COMPLEX if (peripeteia_id or anagnorisis_id) else PLOT_SIMPLE

    # complication / denouement defaults: last beginning / last middle
    beginning_ids = phases_doc.get("beginning", [])
    middle_ids = phases_doc.get("middle", [])
    complication = doc.get("complication") or (
        beginning_ids[-1] if beginning_ids else None)
    denouement = doc.get("denouement") or (
        middle_ids[-1] if middle_ids else None)

    mythos = ArMythos(
        id="ar_" + title.lower().replace(" ", "_")[:24],
        title=title,
        action_summary=doc.get("action_summary", logline),
        central_event_ids=central,
        plot_kind=plot_kind,
        phases=ar_phases,
        complication_event_id=complication,
        denouement_event_id=denouement,
        peripeteia_event_id=peripeteia_id,
        anagnorisis_event_id=anagnorisis_id,
        anagnorisis_character_ref_id=recognizer,
        characters=tuple(ar_chars),
        anagnorisis_chain=tuple(chain),
        peripeteia_anagnorisis_binding=binding,
        pathos_character_ref_ids=tuple(pathos_ids),
    )

    return CompiledStory(
        title=title, logline=logline, entities=entities, fabula=fabula,
        sjuzhet=sjuzhet, descriptions=descriptions,
        preplay_disclosures=preplay, mythos=mythos,
    )


def load_story_file(path: str) -> CompiledStory:
    """Parse and compile a .story.toml file."""
    import tomllib
    with open(path, "rb") as f:
        doc = tomllib.load(f)
    return compile_story(doc)


def verify_compiled(compiled: CompiledStory) -> list:
    """Run the Aristotelian self-verifier on a compiled story — the same
    structural feedback the Python encodings get."""
    return verify(
        compiled.mythos,
        substrate_events=tuple(compiled.fabula),
        mythoi=(compiled.mythos,),
    )
