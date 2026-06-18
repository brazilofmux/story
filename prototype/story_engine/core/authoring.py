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
from story_engine.core.save_the_cat import (
    StcStory, StcBeat, StcStrand, StcCharacter, StrandAdvancement, StrandKind,
    CANONICAL_BEATS, CANONICAL_BEAT_BY_SLOT, GENRE_BY_ID,
    verify as stc_verify,
)


class StoryFormatError(ValueError):
    """A human-facing authoring error — phrased for a writer, not a
    stack trace. Raised when the .story.toml is structurally unusable
    before the dialect verifier even runs (a missing field, an event id
    referenced that does not exist, an event in no phase or two)."""


@dataclass
class CompiledStory:
    """Everything an encoding module exports, produced from a
    .story.toml — ready for the generator / evaluator / verifier. The
    substrate (entities · fabula · sjuzhet · descriptions · preplay) is
    dialect-neutral; the overlay is dialect-specific — `mythos` carries the
    Aristotelian `ArMythos`, `overlay` carries the chosen dialect's overlay
    object (the same one for Aristotelian, a `CompiledStcOverlay` for
    Save-the-Cat)."""
    title: str
    logline: str
    entities: list = field(default_factory=list)
    fabula: list = field(default_factory=list)
    sjuzhet: list = field(default_factory=list)
    descriptions: list = field(default_factory=list)
    preplay_disclosures: tuple = ()
    dialect: str = "aristotelian"
    mythos: object = None        # ArMythos (Aristotelian)
    overlay: object = None       # the dialect overlay (ArMythos / CompiledStcOverlay)


@dataclass(frozen=True)
class CompiledStcOverlay:
    """The Save-the-Cat overlay a `.story.toml` compiles to: the canonical
    `StcStory` plus the authored beat / strand / character records and the
    beat→event map the generator needs. Mirrors what a `*_save_the_cat`
    encoding exports."""
    story: object                # StcStory
    beats: tuple = ()
    strands: tuple = ()
    characters: tuple = ()
    beat_event_ids: dict = field(default_factory=dict)
    action_summary: str = ""

    def verify(self) -> list:
        return stc_verify(self.story, beats=self.beats, strands=self.strands,
                          characters=self.characters)


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
# Compile — a dialect-neutral substrate build, then a per-dialect overlay
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class _Substrate:
    """The dialect-neutral core a `.story.toml` compiles to, shared by every
    overlay builder: entities · fabula · sjuzhet · descriptions · preplay,
    plus the bookkeeping (`event_id_set`, `by_when`, the raw doc lists) the
    overlays need."""
    title: str
    logline: str
    entities: list
    fabula: list
    sjuzhet: list
    descriptions: list
    preplay: tuple
    event_id_set: set
    by_when: dict
    valid_ids: set
    raw_chars: list
    raw_events: list
    raw_places: list


def _build_substrate(doc: dict) -> _Substrate:
    """Build the dialect-neutral substrate (the same Entities / Events /
    Sjuzhet / Descriptions every encoding authors, regardless of dialect)."""
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
    for c in raw_chars:
        cid = _require(c, "id", "a character")
        entities.append(Entity(id=cid, name=c.get("name", cid), kind="agent"))
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

    return _Substrate(
        title=title, logline=logline, entities=entities, fabula=fabula,
        sjuzhet=sjuzhet, descriptions=descriptions, preplay=preplay,
        event_id_set=event_id_set, by_when=by_when, valid_ids=valid_ids,
        raw_chars=raw_chars, raw_events=raw_events, raw_places=raw_places,
    )


def compile_story(doc: dict, dialect: str = "aristotelian") -> CompiledStory:
    """Compile a parsed .story.toml document into a CompiledStory.

    The substrate is dialect-neutral; the overlay is `dialect`-specific.
    Aristotelian and Save-the-Cat have live overlay compilers; the other
    dialects' overlays are interviewed but not yet compiled here."""
    sub = _build_substrate(doc)
    d = (dialect or "aristotelian").strip().lower().replace("_", "-")
    if d == "aristotelian":
        mythos = _build_aristotelian_overlay(doc, sub)
        return CompiledStory(
            title=sub.title, logline=sub.logline, entities=sub.entities,
            fabula=sub.fabula, sjuzhet=sub.sjuzhet, descriptions=sub.descriptions,
            preplay_disclosures=sub.preplay, dialect="aristotelian",
            mythos=mythos, overlay=mythos,
        )
    if d == "save-the-cat":
        overlay = _build_stc_overlay(doc, sub)
        return CompiledStory(
            title=sub.title, logline=sub.logline, entities=sub.entities,
            fabula=sub.fabula, sjuzhet=sub.sjuzhet, descriptions=sub.descriptions,
            preplay_disclosures=sub.preplay, dialect="save-the-cat",
            overlay=overlay,
        )
    raise StoryFormatError(
        f"compile_story has no overlay compiler for dialect {dialect!r} yet "
        f"(Aristotelian and Save-the-Cat are wired)")


# ----------------------------------------------------------------------------
# Overlay: Aristotelian
# ----------------------------------------------------------------------------

def _build_aristotelian_overlay(doc: dict, sub: _Substrate) -> ArMythos:
    title = sub.title
    logline = sub.logline
    raw_chars = sub.raw_chars
    raw_events = sub.raw_events
    event_id_set = sub.event_id_set
    by_when = sub.by_when

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
    return mythos


# ----------------------------------------------------------------------------
# Overlay: Save-the-Cat
# ----------------------------------------------------------------------------

# canonical beat name → slot (case-insensitive lookup at compile)
_STC_SLOT_BY_NAME = {b.name.lower(): b.slot for b in CANONICAL_BEATS}


def _build_stc_overlay(doc: dict, sub: _Substrate) -> CompiledStcOverlay:
    """Map the authoring dict's Save-the-Cat fields onto the canonical
    `StcStory` + the beat / strand / character records the generator needs.

    The author commits a `theme_statement`, a `genre`, per-character role
    labels, and a canonical `beat` name on each event; we group events by
    beat into the fifteen slots, synthesize the A-story strand (and a
    theme-carrying B-story strand when a theme is stated), and emit the
    beat→event map. Beats are tolerated-missing — an un-beated story still
    compiles (the verifier merely notes the unfilled slots)."""
    raw_chars = sub.raw_chars
    raw_events = sub.raw_events
    char_ids = {c.get("id") for c in raw_chars if c.get("id")}

    characters = tuple(
        StcCharacter(
            id=c["id"], name=c.get("name", c["id"]),
            role_labels=((c["role"].strip().lower(),)
                         if (c.get("role") or "").strip() else ()),
        )
        for c in raw_chars
    )

    # group events into canonical slots by their authored beat name
    by_slot: dict = {}
    for ev in raw_events:
        slot = _STC_SLOT_BY_NAME.get((ev.get("beat") or "").strip().lower())
        if slot:
            by_slot.setdefault(slot, []).append(ev)

    strand_a = "a_story"
    beats = []
    beat_event_ids: dict = {}
    for slot in sorted(by_slot):
        evs = by_slot[slot]
        canon = CANONICAL_BEAT_BY_SLOT[slot]
        participant_ids = tuple(dict.fromkeys(
            w for ev in evs for w in (ev.get("who") or []) if w in char_ids))
        desc = " ".join((ev.get("summary") or "").strip()
                        for ev in evs if (ev.get("summary") or "").strip())
        beats.append(StcBeat(
            id=f"beat{slot:02d}_{canon.name.lower().replace(' ', '_')}"[:40],
            slot=slot, page_actual=canon.page_target,
            description_of_change=desc or canon.purpose,
            advances=(StrandAdvancement(strand_id=strand_a),),
            participant_ids=participant_ids,
        ))
        beat_event_ids[slot] = tuple(ev["id"] for ev in evs)

    strands = [StcStrand(id=strand_a, kind=StrandKind.A_STORY,
                         description="the external plot")]
    theme = (doc.get("theme_statement") or "").strip()
    if theme:
        strands.append(StcStrand(id="b_story", kind=StrandKind.B_STORY,
                                 description=theme))

    genre = (doc.get("genre") or "").strip().lower()
    genre_id = genre if genre in GENRE_BY_ID else None

    story = StcStory(
        id=("stc_" + sub.title.lower().replace(" ", "_"))[:28],
        title=sub.title,
        theme_statement=theme,
        stc_genre_id=genre_id,
        beat_ids=tuple(b.id for b in beats),
        strand_ids=tuple(s.id for s in strands),
        character_ids=tuple(c.id for c in characters),
    )
    return CompiledStcOverlay(
        story=story, beats=tuple(beats), strands=tuple(strands),
        characters=characters, beat_event_ids=beat_event_ids,
        action_summary=sub.logline or doc.get("action_summary", ""),
    )


def load_story_file(path: str, dialect: str = "aristotelian") -> CompiledStory:
    """Parse and compile a .story.toml file."""
    import tomllib
    with open(path, "rb") as f:
        doc = tomllib.load(f)
    return compile_story(doc, dialect)


def verify_compiled(compiled: CompiledStory) -> list:
    """Run the compiled story's dialect self-verifier — the same structural
    feedback the Python encodings get."""
    if compiled.dialect == "save-the-cat":
        return compiled.overlay.verify()
    return verify(
        compiled.mythos,
        substrate_events=tuple(compiled.fabula),
        mythoi=(compiled.mythos,),
    )
