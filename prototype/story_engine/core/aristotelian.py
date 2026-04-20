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

# A10 — ArMythosRelation kind vocabulary (canonical-plus-open).
# Non-canonical kinds are admitted but flagged at SEVERITY_NOTED per
# A7.6 check 1; canonical values match the sketch-02 worked cases.

RELATION_CONTESTS = "contests"
RELATION_PARALLEL = "parallel"
RELATION_CONTAINS = "contains"

CANONICAL_RELATION_KINDS: frozenset = frozenset({
    RELATION_CONTESTS, RELATION_PARALLEL, RELATION_CONTAINS,
})

# A12 — peripeteia_anagnorisis_binding vocabulary. The None value is
# admitted at the field level (Optional default); the set below lists
# the non-None values A7.8 recognizes. A non-None value outside this
# set is flagged `peripeteia_anagnorisis_binding_invalid_value`.

BINDING_COINCIDENT = "coincident"
BINDING_ADJACENT = "adjacent"
BINDING_SEPARATED = "separated"

VALID_PERIPETEIA_ANAGNORISIS_BINDINGS: frozenset = frozenset({
    BINDING_COINCIDENT, BINDING_ADJACENT, BINDING_SEPARATED,
})

# A13 (sketch-03) — ArCharacterArcRelation kind vocabulary (canonical-
# plus-open). Non-canonical kinds are admitted but flagged at
# SEVERITY_NOTED per A7.10 check 1; canonical values match the sketch-
# 03 Hamlet worked cases.

ARC_RELATION_PARALLEL = "parallel"
ARC_RELATION_MIRROR = "mirror"
ARC_RELATION_FOIL = "foil"

CANONICAL_CHARACTER_ARC_RELATION_KINDS: frozenset = frozenset({
    ARC_RELATION_PARALLEL, ARC_RELATION_MIRROR, ARC_RELATION_FOIL,
})

# A14 (sketch-03) — ArAnagnorisisStep step_kind vocabulary. Unlike
# A10/A13's canonical-plus-open discipline, this enum is closed:
# invalid values emit SEVERITY_ADVISES_REVIEW. Empty string is
# distinct from the vocabulary — it means "derive from
# precipitates_main + character identity" (see A7.11).

STEP_KIND_PARALLEL = "parallel"
STEP_KIND_PRECIPITATING = "precipitating"
STEP_KIND_STAGING = "staging"

VALID_STEP_KINDS: frozenset = frozenset({
    STEP_KIND_PARALLEL, STEP_KIND_PRECIPITATING, STEP_KIND_STAGING,
})

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
class ArAnagnorisisStep:
    """A11 (sketch-02). One staggered character-level recognition
    within a mythos, supplementary to `ArMythos.anagnorisis_event_id`.

    `event_id` names the substrate event at which the recognition
    lands. `character_ref_id` identifies who realizes — required per
    A11, which keeps the step strictly character-level (audience-
    level recognition is sketch-01 A4 / A8 scope-out).

    `precipitates_main=True` declares that this step causes the
    mythos's main anagnorisis event. When set, A7.7 invariant 2
    enforces that the step's τ_s strictly precedes the main
    anagnorisis event's τ_s (when substrate events are threaded
    through `verify`).

    A step's `event_id` must be in the enclosing mythos's
    `central_event_ids` (A7.7 invariant 1) and must not equal
    `anagnorisis_event_id` (A7.7 invariant 3).

    `step_kind` (A14, sketch-03) splits the A11 `precipitates_main`
    binary along a second axis: same-character-as-main vs. different-
    character. Canonical values:

      - "parallel"      — different character; non-precipitating.
      - "precipitating" — different character; causally drives main.
      - "staging"       — same character as main; epistemic waypoint.

    Empty string (default) means "derive from precipitates_main +
    character identity" — A7.11's back-compat path. Pre-sketch-03
    encodings leave step_kind="" and continue to verify under A11's
    binary semantics. `precipitates_main` is soft-deprecated by A14;
    see the sketch's A14 invariants for the consistency rules the
    verifier enforces when both fields are set.
    """
    id: str
    event_id: str
    character_ref_id: str
    precipitates_main: bool = False
    step_kind: str = ""
    annotation: str = ""


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
    # A11 — staggered character-level recognitions supplementing the
    # singular `anagnorisis_event_id`. Empty by default; pre-sketch-02
    # encodings carry no chain. A7.7 enforces A11 invariants 1–3 + 5.
    anagnorisis_chain: Tuple[ArAnagnorisisStep, ...] = ()
    # A12 — typed structural relation between peripeteia and
    # anagnorisis events. None default admits pre-sketch-02 encodings
    # unchanged; non-None values are checked by A7.8 against the
    # events' actual τ_s distance using `peripeteia_anagnorisis_
    # adjacency_bound`.
    peripeteia_anagnorisis_binding: Optional[str] = None
    peripeteia_anagnorisis_adjacency_bound: int = 3
    # A14 (sketch-03) — the character whose recognition lands at
    # anagnorisis_event_id. Required for step_kind="staging" to
    # verify (A7.11 invariant 2). None default leaves pre-sketch-03
    # encodings unchanged; A7.11's back-compat derivation treats
    # None as "no staging classification available" and any empty-
    # step_kind chain step derives to "parallel" (different char)
    # or "precipitating" (from precipitates_main).
    anagnorisis_character_ref_id: Optional[str] = None


# ============================================================================
# Mythos relation (A10 — sketch-02)
# ============================================================================


@dataclass(frozen=True)
class ArCharacterArcRelation:
    """A13 (sketch-03). Structural relation between two or more
    ArCharacter records *within a single ArMythos*. Hamlet's three-way
    tragic-hero parallelism (pairwise mirror Hamlet-Laertes + foil
    Hamlet-Claudius) is the canonical case.

    Distinguished from A10 `ArMythosRelation` by scope: A10 ties
    ≥2 ArMythos records (inter-mythos); A13 ties ≥2 ArCharacter ids
    within one ArMythos named by `mythos_id`.

    `kind` is canonical-plus-open. Canonical values:
      - "parallel" — umbrella; two or more arcs run within one mythos
        without a more specific structural sub-shape.
      - "mirror"   — parallelism plus structural symmetry (Hamlet-
        Laertes: both sons avenging murdered fathers with opposite
        tempers).
      - "foil"     — parallelism plus structural opposition (Hamlet-
        Claudius: will-to-act vs. will-to-retain).
    Non-canonical values are admitted at severity=NOTED (A7.10 check 1).

    `character_ref_ids` lists the participating ArCharacter ids within
    `mythos_id`'s ArCharacter tuple; ≥2 required (A7.10 check 2). All
    ids must resolve against the named mythos's `characters`.

    `over_event_ids` names substrate events where the arcs track /
    mirror — optional, substrate-check skipped when not threaded.
    """
    id: str
    kind: str
    character_ref_ids: Tuple[str, ...]
    mythos_id: str
    over_event_ids: Tuple[str, ...] = ()
    annotation: str = ""


@dataclass(frozen=True)
class ArMythosRelation:
    """A10 (sketch-02). Structural relation between two or more
    ArMythos records. The Rashomon four-testimony contest is the
    canonical case.

    `kind` is canonical-plus-open. Canonical values:
      - "contests"  — mythoi differ structurally over shared events.
      - "parallel"  — mythoi run alongside without contesting.
      - "contains"  — first mythos envelopes each subsequent one.
    Non-canonical values are admitted at severity=NOTED (A7.6 check 1).

    `mythoi_ids` lists the participating mythos ids; ≥ 2 required
    (A7.6 check 2). For `contains`, the first id is the container;
    order is otherwise unspecified.

    `over_event_ids` names substrate events at stake — typically the
    canonical-floor events that appear in every participating mythos's
    `central_event_ids` for `kind="contests"`. Optional for `parallel`.
    A7.6 check 3 / 4 + A7.9 enforce the consistency rules.
    """
    id: str
    kind: str
    mythoi_ids: Tuple[str, ...]
    over_event_ids: Tuple[str, ...] = ()
    annotation: str = ""


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
# Sketch-02 checks — A7.6 through A7.9
# ============================================================================


def _check_anagnorisis_chain(
    mythos: ArMythos,
    events_by_id: dict,
) -> list:
    """A7.7. Enforce A11 invariants 1–3 and check 5.

    1. step.event_id ∈ mythos.central_event_ids.
    2. if step.precipitates_main: main anagnorisis_event_id non-None
       AND step.τ_s < main.τ_s (substrate-threaded only).
    3. step.event_id ≠ mythos.anagnorisis_event_id.
    5. step.character_ref_id resolves to an ArCharacter in the
       mythos's characters tuple (skip if no characters authored).
    """
    out: list = []
    central_set = set(mythos.central_event_ids)
    character_ids = {c.id for c in mythos.characters}

    for step in mythos.anagnorisis_chain:
        # Invariant 1
        if step.event_id not in central_set:
            out.append(ArObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="anagnorisis_step_event_not_central",
                target_id=step.id,
                message=(f"ArAnagnorisisStep {step.id!r} names "
                         f"event_id={step.event_id!r} which is not in "
                         f"mythos {mythos.id!r}'s central_event_ids; "
                         f"A11 invariant 1 requires it."),
            ))
        # Invariant 3
        if (mythos.anagnorisis_event_id is not None
                and step.event_id == mythos.anagnorisis_event_id):
            out.append(ArObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="anagnorisis_step_equals_main",
                target_id=step.id,
                message=(f"ArAnagnorisisStep {step.id!r} names "
                         f"event_id={step.event_id!r} which equals "
                         f"mythos {mythos.id!r}'s anagnorisis_event_id; "
                         f"A11 invariant 3 reserves the main event "
                         f"for the singular anagnorisis_event_id."),
            ))
        # Invariant 2
        if step.precipitates_main:
            if mythos.anagnorisis_event_id is None:
                out.append(ArObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="anagnorisis_step_precipitates_without_main",
                    target_id=step.id,
                    message=(f"ArAnagnorisisStep {step.id!r} declares "
                             f"precipitates_main=True but mythos "
                             f"{mythos.id!r} has no "
                             f"anagnorisis_event_id; A11 invariant 2 "
                             f"requires a main recognition to "
                             f"precipitate."),
                ))
            elif events_by_id:
                step_event = events_by_id.get(step.event_id)
                main_event = events_by_id.get(mythos.anagnorisis_event_id)
                if (step_event is not None
                        and main_event is not None
                        and step_event.τ_s >= main_event.τ_s):
                    out.append(ArObservation(
                        severity=SEVERITY_ADVISES_REVIEW,
                        code="anagnorisis_step_precipitates_ordering",
                        target_id=step.id,
                        message=(f"ArAnagnorisisStep {step.id!r} "
                                 f"declares precipitates_main=True but "
                                 f"its τ_s ({step_event.τ_s}) is not "
                                 f"strictly less than main "
                                 f"anagnorisis τ_s ({main_event.τ_s}); "
                                 f"A11 invariant 2 requires strict "
                                 f"precedence."),
                    ))
        # Check 5 — character ref resolution (only if characters
        # authored on the mythos).
        if character_ids and step.character_ref_id not in character_ids:
            out.append(ArObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="anagnorisis_step_character_unresolved",
                target_id=step.id,
                message=(f"ArAnagnorisisStep {step.id!r} names "
                         f"character_ref_id={step.character_ref_id!r} "
                         f"which does not match any ArCharacter id in "
                         f"mythos {mythos.id!r}'s characters tuple."),
            ))
    return out


def _check_peripeteia_anagnorisis_binding(
    mythos: ArMythos,
    events_by_id: dict,
) -> list:
    """A7.8. Consistency check for A12's typed binding.

    Runs only when peripeteia_anagnorisis_binding is non-None.
    Requires both peripeteia_event_id and anagnorisis_event_id
    non-None, both resolving to substrate events, and the declared
    binding consistent with their τ_s distance.
    """
    binding = mythos.peripeteia_anagnorisis_binding
    if binding is None:
        return []

    if binding not in VALID_PERIPETEIA_ANAGNORISIS_BINDINGS:
        return [ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="peripeteia_anagnorisis_binding_invalid_value",
            target_id=mythos.id,
            message=(f"ArMythos {mythos.id!r} declares "
                     f"peripeteia_anagnorisis_binding={binding!r} "
                     f"which is not in "
                     f"{sorted(VALID_PERIPETEIA_ANAGNORISIS_BINDINGS)}."),
        )]

    if (mythos.peripeteia_event_id is None
            or mythos.anagnorisis_event_id is None):
        return [ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="peripeteia_anagnorisis_binding_inconsistent",
            target_id=mythos.id,
            message=(f"ArMythos {mythos.id!r} declares "
                     f"peripeteia_anagnorisis_binding={binding!r} but "
                     f"one of peripeteia_event_id / "
                     f"anagnorisis_event_id is None; A12 requires "
                     f"both when a binding is declared."),
        )]

    if not events_by_id:
        return []

    p_event = events_by_id.get(mythos.peripeteia_event_id)
    a_event = events_by_id.get(mythos.anagnorisis_event_id)
    if p_event is None or a_event is None:
        return [ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="peripeteia_anagnorisis_binding_event_unresolved",
            target_id=mythos.id,
            message=(f"ArMythos {mythos.id!r} declares "
                     f"peripeteia_anagnorisis_binding={binding!r} but "
                     f"one of peripeteia_event_id "
                     f"({mythos.peripeteia_event_id!r}) or "
                     f"anagnorisis_event_id "
                     f"({mythos.anagnorisis_event_id!r}) does not "
                     f"resolve in substrate events."),
        )]

    same_event = mythos.peripeteia_event_id == mythos.anagnorisis_event_id
    distance = abs(p_event.τ_s - a_event.τ_s)
    bound = mythos.peripeteia_anagnorisis_adjacency_bound

    if binding == BINDING_COINCIDENT:
        consistent = same_event
        expected = "peripeteia_event_id == anagnorisis_event_id"
    elif binding == BINDING_ADJACENT:
        consistent = (not same_event) and distance <= bound
        expected = (f"events distinct and |τ_s distance| ≤ "
                    f"{bound}")
    else:  # BINDING_SEPARATED
        consistent = distance > bound
        expected = f"|τ_s distance| > {bound}"

    if not consistent:
        return [ArObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="peripeteia_anagnorisis_binding_inconsistent",
            target_id=mythos.id,
            message=(f"ArMythos {mythos.id!r} declares "
                     f"peripeteia_anagnorisis_binding={binding!r} but "
                     f"the events' actual τ_s facts "
                     f"(peripeteia={p_event.τ_s}, "
                     f"anagnorisis={a_event.τ_s}, "
                     f"same_event={same_event}) do not satisfy "
                     f"{expected!r}."),
        )]
    return []


def _check_mythos_relations(
    relations: tuple,
    mythoi: tuple,
) -> list:
    """A7.6. Structural integrity for ArMythosRelation records.

    1. kind in CANONICAL_RELATION_KINDS — else severity=NOTED.
    2. len(mythoi_ids) ≥ 2; each id resolves against `mythoi` (if
       `mythoi` is threaded through — skip resolution when empty).
    3. kind="contests": each over_event_ids event appears in every
       participating mythos's central_event_ids.
    4. kind="contains": first mythos's central_event_ids is a strict
       superset of every subsequent participating mythos's.
    """
    out: list = []
    mythoi_by_id = {m.id: m for m in mythoi}

    for rel in relations:
        # Check 1 — canonical-plus-open
        if rel.kind not in CANONICAL_RELATION_KINDS:
            out.append(ArObservation(
                severity=SEVERITY_NOTED,
                code="mythos_relation_kind_noncanonical",
                target_id=rel.id,
                message=(f"ArMythosRelation {rel.id!r} declares "
                         f"kind={rel.kind!r} which is not in "
                         f"{sorted(CANONICAL_RELATION_KINDS)}; admitted "
                         f"under canonical-plus-open discipline."),
            ))

        # Check 2a — cardinality
        if len(rel.mythoi_ids) < 2:
            out.append(ArObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="mythos_relation_mythoi_too_few",
                target_id=rel.id,
                message=(f"ArMythosRelation {rel.id!r} lists "
                         f"{len(rel.mythoi_ids)} mythos id(s); A10 "
                         f"requires at least 2."),
            ))

        # Check 2b — resolution (only if caller threaded mythoi)
        participating: list = []
        unresolved: list = []
        for mid in rel.mythoi_ids:
            if mid in mythoi_by_id:
                participating.append(mythoi_by_id[mid])
            else:
                unresolved.append(mid)
        if mythoi and unresolved:
            out.append(ArObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="mythos_relation_mythoi_unresolved",
                target_id=rel.id,
                message=(f"ArMythosRelation {rel.id!r} references "
                         f"mythos id(s) {sorted(unresolved)!r} which do "
                         f"not resolve against the mythoi collection."),
            ))

        # Check 3 — contests: over_event_ids coverage
        if (rel.kind == RELATION_CONTESTS
                and participating
                and rel.over_event_ids):
            for eid in rel.over_event_ids:
                for m in participating:
                    if eid not in m.central_event_ids:
                        out.append(ArObservation(
                            severity=SEVERITY_ADVISES_REVIEW,
                            code="mythos_relation_contests_event_absent",
                            target_id=rel.id,
                            message=(f"ArMythosRelation {rel.id!r} "
                                     f"(kind='contests') names "
                                     f"over_event_id {eid!r} which is "
                                     f"not in mythos {m.id!r}'s "
                                     f"central_event_ids."),
                        ))

        # Check 4 — contains: first mythos strict-superset of each rest
        if rel.kind == RELATION_CONTAINS and len(participating) >= 2:
            outer = participating[0]
            outer_set = set(outer.central_event_ids)
            for inner in participating[1:]:
                inner_set = set(inner.central_event_ids)
                if not (inner_set < outer_set):
                    out.append(ArObservation(
                        severity=SEVERITY_ADVISES_REVIEW,
                        code="mythos_relation_contains_not_superset",
                        target_id=rel.id,
                        message=(f"ArMythosRelation {rel.id!r} "
                                 f"(kind='contains') expects outer "
                                 f"mythos {outer.id!r} to be a strict "
                                 f"superset of inner {inner.id!r}; "
                                 f"events in inner but not outer: "
                                 f"{sorted(inner_set - outer_set)!r}."),
                    ))
    return out


def _check_relation_event_refs(
    relations: tuple,
    events_by_id: dict,
) -> list:
    """A7.9. Every event id in a relation's over_event_ids must
    resolve in substrate events when threaded. Skips when caller
    does not pass substrate events (consistent with A7 check 4).
    """
    if not events_by_id:
        return []
    out: list = []
    for rel in relations:
        seen_missing = set()
        for eid in rel.over_event_ids:
            if eid not in events_by_id and eid not in seen_missing:
                seen_missing.add(eid)
                out.append(ArObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="mythos_relation_event_ref_unresolved",
                    target_id=rel.id,
                    message=(f"ArMythosRelation {rel.id!r} references "
                             f"over_event_id {eid!r} which is not in "
                             f"the substrate events collection."),
                ))
    return out


# ============================================================================
# Sketch-03 checks — A7.10 + A7.11
# ============================================================================


def _check_character_arc_relations(
    character_arc_relations: tuple,
    mythoi: tuple,
    events_by_id: dict,
) -> list:
    """A7.10. Structural integrity for ArCharacterArcRelation records.

    1. `kind` in CANONICAL_CHARACTER_ARC_RELATION_KINDS — non-canonical
       emits severity=NOTED.
    2. `len(character_ref_ids) ≥ 2`.
    3. `mythos_id` resolves against `mythoi`, and every id in
       `character_ref_ids` resolves to an ArCharacter within that
       mythos's `characters` tuple. Requires `mythoi` threaded;
       resolution-subchecks skip when `mythoi` is empty (consistent
       with A7.6 discipline).
    4. Every event id in `over_event_ids` resolves in substrate events
       when substrate threaded. Skips when substrate empty.
    """
    out: list = []
    mythoi_by_id = {m.id: m for m in mythoi}

    for rel in character_arc_relations:
        # Check 1 — canonical-plus-open kind
        if rel.kind not in CANONICAL_CHARACTER_ARC_RELATION_KINDS:
            out.append(ArObservation(
                severity=SEVERITY_NOTED,
                code="character_arc_relation_kind_noncanonical",
                target_id=rel.id,
                message=(f"ArCharacterArcRelation {rel.id!r} declares "
                         f"kind={rel.kind!r} which is not in "
                         f"{sorted(CANONICAL_CHARACTER_ARC_RELATION_KINDS)}"
                         f"; admitted under canonical-plus-open "
                         f"discipline."),
            ))

        # Check 2 — cardinality
        if len(rel.character_ref_ids) < 2:
            out.append(ArObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="character_arc_relation_refs_too_few",
                target_id=rel.id,
                message=(f"ArCharacterArcRelation {rel.id!r} lists "
                         f"{len(rel.character_ref_ids)} character id(s); "
                         f"A13 requires at least 2."),
            ))

        # Check 3 — mythos + character resolution (requires mythoi)
        if mythoi:
            target_mythos = mythoi_by_id.get(rel.mythos_id)
            if target_mythos is None:
                out.append(ArObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="character_arc_relation_mythos_unresolved",
                    target_id=rel.id,
                    message=(f"ArCharacterArcRelation {rel.id!r} names "
                             f"mythos_id={rel.mythos_id!r} which does "
                             f"not resolve against the mythoi "
                             f"collection."),
                ))
            else:
                char_ids = {c.id for c in target_mythos.characters}
                for cid in rel.character_ref_ids:
                    if cid not in char_ids:
                        out.append(ArObservation(
                            severity=SEVERITY_ADVISES_REVIEW,
                            code=("character_arc_relation_character"
                                  "_unresolved"),
                            target_id=rel.id,
                            message=(f"ArCharacterArcRelation {rel.id!r} "
                                     f"names character_ref_id={cid!r} "
                                     f"which does not resolve against "
                                     f"mythos {target_mythos.id!r}'s "
                                     f"characters tuple."),
                        ))

        # Check 4 — over_event_ids resolve in substrate (when threaded)
        if events_by_id:
            seen_missing: set = set()
            for eid in rel.over_event_ids:
                if eid not in events_by_id and eid not in seen_missing:
                    seen_missing.add(eid)
                    out.append(ArObservation(
                        severity=SEVERITY_ADVISES_REVIEW,
                        code=("character_arc_relation_event_ref"
                              "_unresolved"),
                        target_id=rel.id,
                        message=(f"ArCharacterArcRelation {rel.id!r} "
                                 f"references over_event_id {eid!r} "
                                 f"which is not in the substrate events "
                                 f"collection."),
                    ))
    return out


def _derived_step_kind(
    step: ArAnagnorisisStep,
    anagnorisis_character_ref_id: Optional[str],
) -> str:
    """Back-compat derivation for A14. When `step.step_kind` is
    empty, derive from `precipitates_main` + character identity.

    If `anagnorisis_character_ref_id` is None, same-character-as-main
    cannot be distinguished structurally; the conservative default is
    "parallel" (or "precipitating" when the flag is set). Authors who
    want "staging" must both set `step_kind="staging"` explicitly and
    name `anagnorisis_character_ref_id` on the mythos.
    """
    if step.step_kind:
        return step.step_kind
    if (anagnorisis_character_ref_id is not None
            and step.character_ref_id == anagnorisis_character_ref_id):
        return STEP_KIND_STAGING
    if step.precipitates_main:
        return STEP_KIND_PRECIPITATING
    return STEP_KIND_PARALLEL


def _check_anagnorisis_step_kind(
    mythos: ArMythos,
    events_by_id: dict,
) -> list:
    """A7.11. Enforce the five A14 invariants for `step_kind`.

    1. Non-empty step_kind in VALID_STEP_KINDS.
    2. step_kind="staging": anagnorisis_character_ref_id must be non-
       None and equal the step's character_ref_id.
    3. step_kind="precipitating": precipitates_main must be True.
    4. step_kind="parallel": precipitates_main must be False.
    5. step_kind="staging": precipitates_main must be True.
    6. Staging steps: step's τ_s < main anagnorisis event's τ_s (when
       substrate threaded).
    """
    out: list = []
    main_char = mythos.anagnorisis_character_ref_id

    for step in mythos.anagnorisis_chain:
        # Invariant 1 — vocabulary (only if explicitly set)
        if step.step_kind and step.step_kind not in VALID_STEP_KINDS:
            out.append(ArObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="anagnorisis_step_kind_invalid",
                target_id=step.id,
                message=(f"ArAnagnorisisStep {step.id!r} declares "
                         f"step_kind={step.step_kind!r} which is not in "
                         f"{sorted(VALID_STEP_KINDS)}."),
            ))
            # Further checks on this step would be noise; skip.
            continue

        effective_kind = _derived_step_kind(step, main_char)

        # Invariants 2, 5, 6 — staging-specific
        if effective_kind == STEP_KIND_STAGING:
            if main_char is None:
                out.append(ArObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code=("anagnorisis_step_staging_requires_main"
                          "_character"),
                    target_id=step.id,
                    message=(f"ArAnagnorisisStep {step.id!r} is "
                             f"step_kind='staging' but enclosing mythos "
                             f"{mythos.id!r} has no "
                             f"anagnorisis_character_ref_id; A14 "
                             f"invariant 2 requires it."),
                ))
            elif step.character_ref_id != main_char:
                out.append(ArObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code=("anagnorisis_step_staging_character"
                          "_mismatch"),
                    target_id=step.id,
                    message=(f"ArAnagnorisisStep {step.id!r} is "
                             f"step_kind='staging' with "
                             f"character_ref_id="
                             f"{step.character_ref_id!r}, but mythos "
                             f"{mythos.id!r} names "
                             f"anagnorisis_character_ref_id="
                             f"{main_char!r}; A14 invariant 2 requires "
                             f"them to match."),
                ))
            # Invariant 5 — staging precipitates (noted if user set
            # step_kind explicitly and precipitates_main contradicts;
            # derived staging from same-character already implies
            # precipitates_main should be True — flag if not).
            if not step.precipitates_main:
                out.append(ArObservation(
                    severity=SEVERITY_NOTED,
                    code="anagnorisis_step_kind_precipitates_mismatch",
                    target_id=step.id,
                    message=(f"ArAnagnorisisStep {step.id!r} is "
                             f"step_kind='staging' with "
                             f"precipitates_main=False; A14 invariant 5 "
                             f"requires staging steps to precipitate "
                             f"the main recognition."),
                ))
            # Invariant 6 — staging ordering (substrate-threaded only)
            if (events_by_id
                    and mythos.anagnorisis_event_id is not None):
                step_event = events_by_id.get(step.event_id)
                main_event = events_by_id.get(mythos.anagnorisis_event_id)
                if (step_event is not None
                        and main_event is not None
                        and step_event.τ_s >= main_event.τ_s):
                    out.append(ArObservation(
                        severity=SEVERITY_ADVISES_REVIEW,
                        code="anagnorisis_step_staging_ordering",
                        target_id=step.id,
                        message=(f"ArAnagnorisisStep {step.id!r} "
                                 f"(step_kind='staging') has τ_s "
                                 f"({step_event.τ_s}) not strictly less "
                                 f"than main anagnorisis τ_s "
                                 f"({main_event.τ_s}); A14 invariant 6 "
                                 f"requires strict precedence."),
                    ))

        # Invariants 3, 4 — precipitating / parallel precipitates_main
        # consistency. Only flag when step_kind is explicitly set
        # (empty-string derivation is always self-consistent by
        # construction of `_derived_step_kind`).
        if step.step_kind == STEP_KIND_PRECIPITATING:
            if not step.precipitates_main:
                out.append(ArObservation(
                    severity=SEVERITY_NOTED,
                    code="anagnorisis_step_kind_precipitates_mismatch",
                    target_id=step.id,
                    message=(f"ArAnagnorisisStep {step.id!r} is "
                             f"step_kind='precipitating' with "
                             f"precipitates_main=False; A14 invariant 3 "
                             f"requires precipitating steps to have "
                             f"precipitates_main=True."),
                ))
        elif step.step_kind == STEP_KIND_PARALLEL:
            if step.precipitates_main:
                out.append(ArObservation(
                    severity=SEVERITY_NOTED,
                    code="anagnorisis_step_kind_precipitates_mismatch",
                    target_id=step.id,
                    message=(f"ArAnagnorisisStep {step.id!r} is "
                             f"step_kind='parallel' with "
                             f"precipitates_main=True; A14 invariant 4 "
                             f"requires parallel steps to have "
                             f"precipitates_main=False."),
                ))
    return out


# ============================================================================
# Public verify — A7 orchestrator
# ============================================================================


def verify(
    mythos: ArMythos,
    *,
    substrate_events: tuple = (),
    mythoi: tuple = (),
    relations: tuple = (),
    character_arc_relations: tuple = (),
) -> list:
    """Run A7 checks 1-5 + A7.6-A7.9 + A7.10-A7.11 on a single mythos.

    `substrate_events` is the encoding's Event records. Empty by
    default — event-ref integrity, unity-of-time, unity-of-place,
    hamartia-participation, and A12 binding checks skip when no
    events are threaded through. Authors running the verifier for
    real pass their encoding's FABULA or equivalent.

    `mythoi` is the encoding's full ArMythos tuple (used by A7.6
    for mythos-id resolution on relations). `relations` is the
    encoding's ArMythosRelation tuple. Both default empty; sketch-01
    encodings that do not author A10 relations call `verify` with
    the sketch-01 signature unchanged and see sketch-01 behavior.

    Returns a list of ArObservation records. Per A7, none is an
    error — all are advisory. An encoding with no findings is
    Aristotelian-consistent per the checks this dialect runs; an
    encoding with findings is still usable, with the observations
    flowing to higher-layer walker / review machinery.

    Multi-mythos encodings call `verify` per-mythos. A10 relations
    are evaluated once per `verify` call — a relation-check finding
    surfaces on every call of every mythos in the relation; callers
    that want dedupe should invoke the `_check_mythos_relations` +
    `_check_relation_event_refs` helpers directly at encoding scope.

    `character_arc_relations` (A13, sketch-03) is the encoding's
    ArCharacterArcRelation tuple. A7.10 evaluates each relation's
    structural integrity; finds surface once per `verify` call
    regardless of which mythos it targets (the relation's `mythos_id`
    selects which mythos it binds to). Default empty; pre-sketch-03
    encodings change nothing.
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
    out.extend(_check_anagnorisis_chain(mythos, events_by_id))
    out.extend(_check_peripeteia_anagnorisis_binding(mythos, events_by_id))
    out.extend(_check_mythos_relations(relations, mythoi))
    out.extend(_check_relation_event_refs(relations, events_by_id))
    out.extend(_check_character_arc_relations(
        character_arc_relations, mythoi, events_by_id,
    ))
    out.extend(_check_anagnorisis_step_kind(mythos, events_by_id))
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


# ============================================================================
# Probe-surface records (aristotelian-probe-sketch-01 APA1)
# ============================================================================
#
# Three additive record types that let a reader-model probe land
# output on this dialect. The existing dialect records (ArMythos,
# ArPhase, ArCharacter, ArObservation, verify) are unmodified.
#
# ArAnnotationReview parallels lowering.AnnotationReview but targets
# a dialect record's prose field (Aristotelian has no Lowerings per
# A9). ArObservationCommentary parallels verification.VerifierCommentary
# but targets an ArObservation (Aristotelian's self-verifier emits
# ArObservations, not VerificationReviews). DialectReading has no
# analog in the existing stack — it captures the probe's distinctive
# methodological signal: did the reader engage the dialect on its
# own terms or drift into other dialects' vocabularies?


# Verdict vocabulary mirrors lowering.VERDICT_*; duplicated here to
# keep aristotelian.py import-free of lowering.py (parallels
# verification.py's duplicate VERDICT_* constants).

VERDICT_APPROVED = "approved"
VERDICT_NEEDS_WORK = "needs-work"
VERDICT_REJECTED = "rejected"
VERDICT_NOTED = "noted"

VALID_REVIEW_VERDICTS: frozenset = frozenset({
    VERDICT_APPROVED, VERDICT_NEEDS_WORK,
    VERDICT_REJECTED, VERDICT_NOTED,
})

# Assessment vocabulary mirrors verification.ASSESSMENT_*.

ASSESSMENT_ENDORSES = "endorses"
ASSESSMENT_QUALIFIES = "qualifies"
ASSESSMENT_DISSENTS = "dissents"
ASSESSMENT_NOTED = "noted"

VALID_COMMENTARY_ASSESSMENTS: frozenset = frozenset({
    ASSESSMENT_ENDORSES, ASSESSMENT_QUALIFIES,
    ASSESSMENT_DISSENTS, ASSESSMENT_NOTED,
})

# Target-kind vocabulary for ArAnnotationReview. Each Aristotelian
# record kind with a reviewable prose field appears here.

TARGET_AR_MYTHOS = "ArMythos"
TARGET_AR_PHASE = "ArPhase"
TARGET_AR_CHARACTER = "ArCharacter"

VALID_REVIEW_TARGET_KINDS: frozenset = frozenset({
    TARGET_AR_MYTHOS, TARGET_AR_PHASE, TARGET_AR_CHARACTER,
})

# Field-name vocabulary for ArAnnotationReview. Per APS2 each
# target_kind has exactly one reviewable prose field; the table
# is fixed and translation-time validators use FIELDS_BY_TARGET_KIND
# to reject mis-paired reviews.

FIELD_ACTION_SUMMARY = "action_summary"    # ArMythos only
FIELD_PHASE_ANNOTATION = "annotation"      # ArPhase only
FIELD_HAMARTIA_TEXT = "hamartia_text"      # ArCharacter only

VALID_REVIEW_FIELDS: frozenset = frozenset({
    FIELD_ACTION_SUMMARY, FIELD_PHASE_ANNOTATION, FIELD_HAMARTIA_TEXT,
})

FIELDS_BY_TARGET_KIND: dict = {
    TARGET_AR_MYTHOS: frozenset({FIELD_ACTION_SUMMARY}),
    TARGET_AR_PHASE: frozenset({FIELD_PHASE_ANNOTATION}),
    TARGET_AR_CHARACTER: frozenset({FIELD_HAMARTIA_TEXT}),
}

# DialectReading's read_on_terms vocabulary — the reader's self-
# report on whether its review used Aristotelian vocabulary or
# drifted into other dialects' vocabularies.

READ_ON_TERMS_YES = "yes"
READ_ON_TERMS_PARTIAL = "partial"
READ_ON_TERMS_NO = "no"

VALID_READ_ON_TERMS: frozenset = frozenset({
    READ_ON_TERMS_YES, READ_ON_TERMS_PARTIAL, READ_ON_TERMS_NO,
})


@dataclass(frozen=True)
class ArAnnotationReview:
    """One reviewer's verdict on one prose field of one Aristotelian
    record. Parallels lowering.AnnotationReview in shape and
    staleness semantics (reader-model-sketch-01 R6: anchor_τ_a
    snapshots the reviewed record's last-authored τ_a).

    `target_kind` + `target_id` + `field` identifies the prose
    under review — e.g., `("ArMythos", "ar_oedipus",
    "action_summary")`. `verdict` ∈ VERDICT_*.

    Aristotelian records don't carry record-level τ_a, so the
    caller supplies the encoding-level τ_a as `anchor_τ_a`.

    `id` is optional — the target triple is unique within a
    probe run; a consumer that needs external cross-reference
    can assign one.
    """
    reviewer_id: str
    reviewed_at_τ_a: int
    target_kind: str
    target_id: str
    field: str
    verdict: str
    comment: Optional[str] = None
    anchor_τ_a: int = 0
    id: Optional[str] = None


@dataclass(frozen=True)
class ArObservationCommentary:
    """A reviewer's read on an ArObservation. Parallels
    verification.VerifierCommentary — the target is this dialect's
    observation shape rather than a VerificationReview.

    `assessment` ∈ ASSESSMENT_*:
      - endorses: finding is well-grounded, nothing to add.
      - qualifies: finding stands with a clarification.
      - dissents: commenter disagrees; must name what the check
        missed or got wrong.
      - noted: read but no position taken.

    `target_observation` holds the resolved ArObservation (by
    value — ArObservation is frozen and has no id).
    `suggested_signature` is optional free-form prose naming a
    concrete signature the commenter thinks the A7 check might
    add; inspiration for the maintainer, not executable code.
    """
    commenter_id: str
    commented_at_τ_a: int
    assessment: str
    target_observation: ArObservation
    comment: Optional[str] = None
    suggested_signature: Optional[str] = None


@dataclass(frozen=True)
class DialectReading:
    """A reader-model's read on the Aristotelian surface as a whole.
    One per probe invocation; captures the methodological signal
    aristotelian-probe-sketch-01 exists to produce (APS6 P4).

    `read_on_terms` is the reader's self-report. `rationale` is
    bounded free-form (prompt caps length; record does not
    enforce).

    `drift_flagged` names specific out-of-dialect phrases or record
    types the reader noticed itself using or wanting to use (e.g.,
    "DSP_limit", "pressure-shape", "inciting beat"). Empty tuple =
    clean in-dialect read.

    `scope_limits_observed` names dialect-scope limits perceived
    (for Rashomon: meta-anagnorisis — the audience's recognition
    that no testimony is fully true, which Aristotelian's
    character-level anagnorisis cannot express).

    `relations_wanted` names structural extensions the reader
    thought would help. Non-empty is NOT drift — the canonical
    example is `ArMythosRelation`, which aristotelian-sketch-01
    A8 / stress-case already flagged as a candidate sketch-02
    extension. A non-empty `relations_wanted` is a probe-surfaced
    forcing function, not a failure.
    """
    reader_id: str
    read_at_τ_a: int
    read_on_terms: str
    rationale: str
    drift_flagged: tuple = ()               # tuple[str, ...]
    scope_limits_observed: tuple = ()       # tuple[str, ...]
    relations_wanted: tuple = ()            # tuple[str, ...]
