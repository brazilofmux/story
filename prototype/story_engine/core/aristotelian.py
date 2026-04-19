"""
aristotelian.py — Aristotelian narrative dialect (per aristotelian-
sketch-01).

Third upper-dialect under architecture-sketch-02's stack, after
dramatic.py and save_the_cat.py. Written on the dialect's own terms;
substrate event ids are referenced but the substrate is not traversed
except via the explicit unity-of-time / unity-of-place verifier checks
(A6).

Aristotle's *Poetics* (~335 BCE) predates Dramatica by ~2400 years.
This dialect is a falsifiable stability test of architecture-sketch-02's
claim that the stack admits theoretically distinct frames by clean
extension. See aristotelian-sketch-01.md's "Architectural judgment"
and stress case for the design-phase test result.

Per aristotelian-sketch-01 commitments:
- A1: ArMythos as the primary record (mythos-as-soul per Poetics 1450a).
- A2: ArPhase with role ∈ {beginning, middle, end} — logical divisions.
- A3: simple vs complex plot; if complex, at least one of
      peripeteia / anagnorisis required.
- A4: peripeteia / anagnorisis as interpretive pointers to substrate
      event ids.
- A5: ArCharacter with optional character_ref_id cross-dialect hook.
- A6: three unities — unity of action (always checked); unity of
      time / place (opt-in, configurable bounds).
- A7: self-verifier within Aristotelian vocabulary (5 checks).
- A8: catharsis / pity / fear as authorial claims, not checks.
- A9: cross-dialect Lowering out of scope.

Running tests:
    cd prototype
    python3 -m tests.test_aristotelian
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


# ============================================================================
# Constants — role / plot-kind / severity vocabularies
# ============================================================================

PHASE_BEGINNING = "beginning"
PHASE_MIDDLE = "middle"
PHASE_END = "end"

VALID_PHASE_ROLES: frozenset = frozenset({
    PHASE_BEGINNING, PHASE_MIDDLE, PHASE_END,
})

PLOT_SIMPLE = "simple"
PLOT_COMPLEX = "complex"

VALID_PLOT_KINDS: frozenset = frozenset({PLOT_SIMPLE, PLOT_COMPLEX})

SEVERITY_NOTED = "noted"
SEVERITY_ADVISES_REVIEW = "advises-review"


# ============================================================================
# Records — A1, A2, A5
# ============================================================================

@dataclass(frozen=True)
class ArPhase:
    """A2. One of the three logical divisions of the mythos.

    Unlike Save-the-Cat beats, phases are NOT page-positioned; they
    are logical divisions connected by necessity or probability
    (Poetics 1451a). `scope_event_ids` names the substrate events
    authoring this phase; no overlap across phases within a single
    mythos (A6 unity-of-action check enforces disjoint coverage).
    """
    id: str
    role: str                                # "beginning" | "middle" | "end"
    scope_event_ids: Tuple[str, ...]
    annotation: str = ""


@dataclass(frozen=True)
class ArCharacter:
    """A5. Aristotelian character-layer record.

    `character_ref_id` is the cross-dialect identity hook: if an
    encoding also authors a substrate Entity or a Dramatic Character
    record, its id goes here. If the Aristotelian encoding stands
    alone, `character_ref_id` is None and the Aristotelian dialect
    carries the character on its own.

    `hamartia_text` is author prose — "missing the mark" per Poetics
    1453a. NOT the Bradleyan "tragic flaw" reading (moral defect);
    Aristotle's sense is closer to an error of judgment, often
    from ignorance.

    `is_tragic_hero` distinguishes the central hero from other
    characters who may also carry a hamartia (e.g., Jocasta in
    Oedipus).
    """
    id: str
    name: str
    character_ref_id: Optional[str] = None
    hamartia_text: Optional[str] = None
    is_tragic_hero: bool = False


@dataclass(frozen=True)
class ArMythos:
    """A1. The Aristotelian dialect's primary record. Mythos is the
    arrangement of the incidents — the *soul* of tragedy (Poetics
    1450a), above character, thought, diction, melody, spectacle.

    `central_event_ids` names the substrate events comprising the
    action. Order is preserved for author intent but not
    semantically required; the phase structure (A2) authorizes
    the arrangement.

    `plot_kind` is A3: "simple" or "complex". If "complex", at
    least one of `peripeteia_event_id` / `anagnorisis_event_id`
    must be non-None (A7 check 1).

    `complication_event_id` and `denouement_event_id` mark the
    Aristotelian "binding" and "unbinding" (Poetics 1455b) —
    where beginning ends and middle begins, and where middle ends
    and end begins. Optional.

    The three unity assertions default to the Aristotelian stance:
    unity of action required (A6), unity of time / place not
    asserted (neoclassical). Authors opt in to the neoclassical
    unities by flipping the booleans and (optionally) configuring
    the bounds.

    `aims_at_catharsis` is A8 — an authorial claim about the
    work's intended effect on pity and fear. The self-verifier
    cannot check catharsis (audience-response, out of scope) and
    the field's value does not affect any verification output.

    `characters` is a tuple of ArCharacter records authored at
    mythos scope. Dialect does not track character-at-encoding
    scope separately; an encoding authoring multiple mythoi can
    share characters by reusing the same ArCharacter id across
    mythoi.
    """
    id: str
    title: str
    action_summary: str
    central_event_ids: Tuple[str, ...]
    plot_kind: str
    phases: Tuple[ArPhase, ...]
    complication_event_id: Optional[str] = None
    denouement_event_id: Optional[str] = None
    peripeteia_event_id: Optional[str] = None
    anagnorisis_event_id: Optional[str] = None
    asserts_unity_of_action: bool = True
    asserts_unity_of_time: bool = False
    asserts_unity_of_place: bool = False
    unity_of_time_bound: int = 24
    unity_of_place_max_locations: int = 1
    aims_at_catharsis: bool = True
    characters: Tuple[ArCharacter, ...] = ()


# ============================================================================
# Observation record (A7)
# ============================================================================

@dataclass(frozen=True)
class ArObservation:
    """One self-verifier finding from `verify`. Mirrors StcObservation
    shape for walker-compatibility across dialects.

    Severity is "noted" (observation recorded; no review required)
    or "advises-review" (check uncovered a structural issue the
    author should see).
    """
    severity: str
    code: str
    target_id: str
    message: str


# ============================================================================
# Self-verifier — A7 checks 1-5
# ============================================================================


def _check_plot_kind(mythos: ArMythos) -> list:
    """A7 check 1 (first half). plot_kind must be valid."""
    out: list = []
    if mythos.plot_kind not in VALID_PLOT_KINDS:
        out.append(ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="plot_kind_invalid",
            target_id=mythos.id,
            message=(f"ArMythos {mythos.id!r} declares plot_kind="
                     f"{mythos.plot_kind!r} which is not in "
                     f"{sorted(VALID_PLOT_KINDS)}"),
        ))
    return out


def _check_complex_requires_peripeteia_or_anagnorisis(
    mythos: ArMythos,
) -> list:
    """A7 check 1 (second half). A3: complex plots require at least
    one of peripeteia / anagnorisis."""
    if mythos.plot_kind != PLOT_COMPLEX:
        return []
    if (mythos.peripeteia_event_id is None
            and mythos.anagnorisis_event_id is None):
        return [ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="complex_missing_peripeteia_or_anagnorisis",
            target_id=mythos.id,
            message=(f"ArMythos {mythos.id!r} declares plot_kind="
                     f"'complex' but sets neither peripeteia_event_id "
                     f"nor anagnorisis_event_id; A3 requires at least "
                     f"one."),
        )]
    return []


def _check_phase_coverage_unity_of_action(mythos: ArMythos) -> list:
    """A7 check 2 + A6 unity-of-action. Every central_event_ids event
    appears in exactly one phase's scope_event_ids; union of phase
    scopes equals central_event_ids as a set.

    Unity of action is always checked (A6) — `asserts_unity_of_action`
    is the authorial claim and defaults True; the verifier enforces
    the structural version regardless."""
    out: list = []

    # Phase-role validity + role coverage
    phase_roles = [ph.role for ph in mythos.phases]
    for ph in mythos.phases:
        if ph.role not in VALID_PHASE_ROLES:
            out.append(ArObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="phase_role_invalid",
                target_id=ph.id,
                message=(f"ArPhase {ph.id!r} declares role={ph.role!r} "
                         f"which is not in {sorted(VALID_PHASE_ROLES)}"),
            ))
    # Every role from the canonical triple is declared at least once
    for required_role in VALID_PHASE_ROLES:
        if required_role not in phase_roles:
            out.append(ArObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="phase_role_missing",
                target_id=mythos.id,
                message=(f"ArMythos {mythos.id!r} has no phase with "
                         f"role={required_role!r}; A2 requires all "
                         f"three of beginning/middle/end."),
            ))

    # Disjoint coverage + equality with central_event_ids
    central_set = set(mythos.central_event_ids)
    phase_union: set = set()
    seen_in_phase: dict = {}
    for ph in mythos.phases:
        for eid in ph.scope_event_ids:
            if eid in seen_in_phase:
                out.append(ArObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="phase_overlap",
                    target_id=mythos.id,
                    message=(f"Event {eid!r} appears in multiple phase "
                             f"scopes ({seen_in_phase[eid]!r} and "
                             f"{ph.id!r}); A6 unity of action requires "
                             f"disjoint phase coverage."),
                ))
            seen_in_phase[eid] = ph.id
            phase_union.add(eid)

    missing = central_set - phase_union
    for eid in sorted(missing):
        out.append(ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="central_event_unphased",
            target_id=mythos.id,
            message=(f"central_event_ids contains {eid!r} which is "
                     f"not in any phase's scope_event_ids; A6 unity "
                     f"of action requires phase coverage of every "
                     f"central event."),
        ))

    extra = phase_union - central_set
    for eid in sorted(extra):
        out.append(ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="phase_event_not_central",
            target_id=mythos.id,
            message=(f"Phase scope references event {eid!r} which is "
                     f"not in central_event_ids; A6 requires phase "
                     f"coverage equal to the central set."),
        ))

    return out


def _check_event_ref_integrity(
    mythos: ArMythos,
    events_by_id: dict,
) -> list:
    """A7 check 4. Every event id referenced by mythos resolves to
    a substrate event in events_by_id."""
    if not events_by_id:
        # Caller did not pass substrate events — skip the check rather
        # than flagging every event as missing. This lets the dialect
        # self-verify in isolation for tests that do not thread the
        # substrate through.
        return []

    out: list = []
    referenced: list = []
    for eid in mythos.central_event_ids:
        referenced.append(("central_event_ids", eid))
    for ph in mythos.phases:
        for eid in ph.scope_event_ids:
            referenced.append((f"phases[{ph.id}].scope_event_ids", eid))
    for field_name in (
        "complication_event_id", "denouement_event_id",
        "peripeteia_event_id", "anagnorisis_event_id",
    ):
        eid = getattr(mythos, field_name)
        if eid is not None:
            referenced.append((field_name, eid))

    seen_missing = set()
    for location, eid in referenced:
        if eid not in events_by_id and eid not in seen_missing:
            seen_missing.add(eid)
            out.append(ArObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="event_ref_unresolved",
                target_id=mythos.id,
                message=(f"ArMythos {mythos.id!r} references event "
                         f"{eid!r} (via {location}) which is not in "
                         f"the substrate events collection."),
            ))
    return out


def _check_unity_of_time(
    mythos: ArMythos,
    events_by_id: dict,
) -> list:
    """A6 unity of time. Only checked if `asserts_unity_of_time`.

    max(τ_s) - min(τ_s) over central_event_ids resolvable in
    events_by_id must be ≤ `unity_of_time_bound`.
    """
    if not mythos.asserts_unity_of_time:
        return []
    if not events_by_id:
        return []

    resolved = [
        events_by_id[eid]
        for eid in mythos.central_event_ids
        if eid in events_by_id
    ]
    if not resolved:
        return []

    τ_values = [e.τ_s for e in resolved]
    span = max(τ_values) - min(τ_values)
    if span > mythos.unity_of_time_bound:
        return [ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="unity_of_time_violated",
            target_id=mythos.id,
            message=(f"ArMythos {mythos.id!r} asserts unity of time "
                     f"with bound {mythos.unity_of_time_bound} but the "
                     f"τ_s span of its central events is {span} "
                     f"(min={min(τ_values)}, max={max(τ_values)})."),
        )]
    return []


def _locations_asserted_by_event(event) -> set:
    """Return the set of locations this event asserts via
    world(at_location(<entity>, <location>)) effects.

    Only WorldEffect.asserts=True effects count (retractions do not
    add to the location set)."""
    locs: set = set()
    for eff in event.effects:
        # Duck-type — we avoid importing WorldEffect to keep the
        # dialect module free of substrate dependency at import time.
        prop = getattr(eff, "prop", None)
        asserts = getattr(eff, "asserts", True)
        if prop is None or not asserts:
            continue
        if prop.predicate == "at_location" and len(prop.args) >= 2:
            locs.add(prop.args[1])
    return locs


def _check_unity_of_place(
    mythos: ArMythos,
    events_by_id: dict,
) -> list:
    """A6 unity of place. Only checked if `asserts_unity_of_place`.

    Collect all locations asserted (via world(at_location(...))) by
    events in central_event_ids. Flag if the distinct-location count
    exceeds `unity_of_place_max_locations`. Events without any
    at_location effect contribute nothing (not a violation).
    """
    if not mythos.asserts_unity_of_place:
        return []
    if not events_by_id:
        return []

    locations: set = set()
    for eid in mythos.central_event_ids:
        event = events_by_id.get(eid)
        if event is None:
            continue
        locations |= _locations_asserted_by_event(event)

    if len(locations) > mythos.unity_of_place_max_locations:
        return [ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="unity_of_place_violated",
            target_id=mythos.id,
            message=(f"ArMythos {mythos.id!r} asserts unity of place "
                     f"with max_locations={mythos.unity_of_place_max_locations} "
                     f"but at_location effects across its central "
                     f"events name {len(locations)} distinct "
                     f"location(s): {sorted(locations)}."),
        )]
    return []


def _check_hamartia_participation(
    mythos: ArMythos,
    events_by_id: dict,
) -> list:
    """A7 check 5. For each ArCharacter flagged `is_tragic_hero=True`
    with a non-None `hamartia_text` and a non-None `character_ref_id`,
    the referenced entity must participate in at least one event in
    `central_event_ids`.

    If `character_ref_id` is None, skip (self-contained Aristotelian
    encoding); participation cannot be checked without an entity id.
    If `is_tragic_hero` is False, skip (the check is specifically
    about the hero).
    """
    if not events_by_id:
        return []

    out: list = []
    central_events = [
        events_by_id[eid]
        for eid in mythos.central_event_ids
        if eid in events_by_id
    ]
    for character in mythos.characters:
        if not character.is_tragic_hero:
            continue
        if character.hamartia_text is None:
            continue
        if character.character_ref_id is None:
            continue
        ref = character.character_ref_id
        participates = any(
            ref in e.participants.values()
            for e in central_events
        )
        if not participates:
            out.append(ArObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="hamartia_hero_absent",
                target_id=character.id,
                message=(f"ArCharacter {character.id!r} "
                         f"(ref={character.character_ref_id!r}) is "
                         f"flagged is_tragic_hero=True with "
                         f"hamartia_text set, but does not appear as "
                         f"a participant in any central event of "
                         f"mythos {mythos.id!r}."),
            ))
    return out


# ============================================================================
# Public verify — A7 orchestrator
# ============================================================================


def verify(
    mythos: ArMythos,
    *,
    substrate_events: tuple = (),
) -> list:
    """Run A7 checks 1-5 on a single mythos.

    `substrate_events` is the encoding's Event records. Empty by
    default — event-ref integrity, unity-of-time, unity-of-place,
    and hamartia-participation checks skip when no events are
    threaded through (useful for tests that exercise the dialect
    alone). Authors running the verifier for real pass their
    encoding's FABULA or equivalent.

    Returns a list of ArObservation records. Per A7, none is an
    error — all are advisory. An encoding with no findings is
    Aristotelian-consistent per the checks this dialect runs; an
    encoding with findings is still usable, with the observations
    flowing to higher-layer walker / review machinery.

    Multi-mythos encodings call `verify` per-mythos (see
    aristotelian-sketch-01 stress case — Rashomon).
    """
    events_by_id = {e.id: e for e in substrate_events}

    out: list = []
    out.extend(_check_plot_kind(mythos))
    out.extend(_check_complex_requires_peripeteia_or_anagnorisis(mythos))
    out.extend(_check_phase_coverage_unity_of_action(mythos))
    out.extend(_check_event_ref_integrity(mythos, events_by_id))
    out.extend(_check_unity_of_time(mythos, events_by_id))
    out.extend(_check_unity_of_place(mythos, events_by_id))
    out.extend(_check_hamartia_participation(mythos, events_by_id))
    return out


# ============================================================================
# Convenience groupings
# ============================================================================


def group_by_severity(observations: list) -> dict:
    out: dict = {SEVERITY_NOTED: [], SEVERITY_ADVISES_REVIEW: []}
    for o in observations:
        out.setdefault(o.severity, []).append(o)
    return out


def group_by_code(observations: list) -> dict:
    out: dict = {}
    for o in observations:
        out.setdefault(o.code, []).append(o)
    return out
