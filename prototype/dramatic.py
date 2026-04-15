"""
dramatic.py — first-pass implementation of the Dramatic dialect
(dramatic-sketch-01).

This module is deliberately self-contained. It does not import from
substrate.py, oedipus.py, macbeth.py, or any other dialect's module.
Per architecture-sketch-02 A6, dialects stand alone; cross-dialect
linkage (Lowering records, verifier-record output to the proposal
queue) lives in separate modules and is built on top.

Scope of this first pass:

- The dialect's eight core record types: Story, Argument, Throughline,
  Character, Scene, Beat, Stakes, Template.
- Helper records: ArgumentContribution, SceneAdvancement, StakesOwner,
  FunctionSlot.
- Four enums: FunctionMultiplicity, ResolutionDirection, ArgumentSide,
  StakesOwnerKind.
- Four shipped Templates: dramatica-8 (eight EXACTLY_ONE slots),
  three-actor, two-actor, ensemble.
- The M8 self-verifier: id resolution, beat / scene sequencing,
  template conformance with multiplicity, argument completeness
  (soft), stakes coverage (observation), scene purpose (observation),
  orphans.

Deferred to follow-on passes (with pointers to the relevant sketch):

- Description surface for Dramatic records (dramatic-sketch-01 M10
  + descriptions-01 pattern). The substrate's Description record
  could be reused via dialect-qualified AnchorRef, or the dialect
  could declare its own. This pass does neither.
- Cross-dialect references / Lowering record integration (architecture-
  sketch-02, lowering-record-sketch-01). The Lowering machinery lives
  in a separate module yet to be written.
- Dramatica-complete Template extensions (dramatica-template-sketch-01
  Q1-Q10). The dramatica-8 Template here ships only the eight
  function labels; Quad records, DynamicStoryPoints, Signposts, and
  the Domain/Concern/Issue/Problem hierarchy are
  dramatica-template-sketch-01 territory and require dramatic-sketch-02
  Template-extension machinery before they can land.
- Reader-model probe at the Dramatic boundary (architecture-sketch-02
  A11). A separate `demo_reader_model_dramatic_*.py` would invoke
  the existing reader_model_client against a Dramatic encoding;
  that integration is its own concern.

The dialect is intended to be encoded against. The first such encoding
(oedipus_dramatic.py) is the natural follow-on to this file.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Iterable


# ============================================================================
# Enums
# ============================================================================


class FunctionMultiplicity(str, Enum):
    """Per-function-slot cardinality declared at Template level. The
    self-verifier counts how many Characters carry each label and
    compares against the slot's declared multiplicity."""
    EXACTLY_ONE = "exactly-one"
    AT_MOST_ONE = "at-most-one"
    AT_LEAST_ONE = "at-least-one"
    ANY = "any"


class ResolutionDirection(str, Enum):
    """The Argument's stance toward its premise."""
    AFFIRM = "affirm"
    NEGATE = "negate"
    COMPLICATE = "complicate"
    UNRESOLVED = "unresolved"


class ArgumentSide(str, Enum):
    """A Throughline's stated contribution to an Argument."""
    AFFIRMS = "affirms"
    OPPOSES = "opposes"
    COMPLICATES = "complicates"


class StakesOwnerKind(str, Enum):
    """What kind of record a Stakes record is owned by."""
    THROUGHLINE = "throughline"
    STORY = "story"


# Sentinel owner identifiers a Throughline can claim instead of a
# Character id (M2 admits abstract owners).
THROUGHLINE_OWNER_NONE = "none"
THROUGHLINE_OWNER_SITUATION = "the-situation"
THROUGHLINE_OWNER_RELATIONSHIP = "the-relationship"

ABSTRACT_THROUGHLINE_OWNERS = frozenset({
    THROUGHLINE_OWNER_NONE,
    THROUGHLINE_OWNER_SITUATION,
    THROUGHLINE_OWNER_RELATIONSHIP,
})


# ============================================================================
# Templates (M5)
# ============================================================================


@dataclass(frozen=True)
class FunctionSlot:
    """One named function slot within a Template, with declared
    multiplicity."""
    label: str
    multiplicity: FunctionMultiplicity


@dataclass(frozen=True)
class Template:
    """A Character Function Template names a vocabulary of function
    labels and their per-label multiplicities. Stories declare which
    Template they use; Characters carry function labels drawn from
    that Template's vocabulary.

    Per dramatic-sketch-01 M5, the Template's `function_slots` is
    authoritative for two separate things: which labels are *known*
    to the Template (an unknown label on a Character surfaces as an
    observation) and *how many* Characters the Template expects to
    carry each label (multiplicity check).
    """
    id: str
    name: str
    function_slots: tuple  # tuple[FunctionSlot, ...]

    def slot_for(self, label: str) -> Optional[FunctionSlot]:
        for s in self.function_slots:
            if s.label == label:
                return s
        return None

    def labels(self) -> tuple:
        return tuple(s.label for s in self.function_slots)


# Standard templates shipped with the dialect.

DRAMATICA_8 = Template(
    id="dramatica-8",
    name="Dramatica 8 character functions",
    function_slots=(
        FunctionSlot("Protagonist",  FunctionMultiplicity.EXACTLY_ONE),
        FunctionSlot("Antagonist",   FunctionMultiplicity.EXACTLY_ONE),
        FunctionSlot("Reason",       FunctionMultiplicity.EXACTLY_ONE),
        FunctionSlot("Emotion",      FunctionMultiplicity.EXACTLY_ONE),
        FunctionSlot("Skeptic",      FunctionMultiplicity.EXACTLY_ONE),
        FunctionSlot("Sidekick",     FunctionMultiplicity.EXACTLY_ONE),
        FunctionSlot("Guardian",     FunctionMultiplicity.EXACTLY_ONE),
        FunctionSlot("Contagonist",  FunctionMultiplicity.EXACTLY_ONE),
    ),
)

THREE_ACTOR = Template(
    id="three-actor",
    name="three-actor template",
    function_slots=(
        FunctionSlot("Hero",     FunctionMultiplicity.EXACTLY_ONE),
        FunctionSlot("Obstacle", FunctionMultiplicity.EXACTLY_ONE),
        FunctionSlot("Helper",   FunctionMultiplicity.AT_LEAST_ONE),
    ),
)

TWO_ACTOR = Template(
    id="two-actor",
    name="two-actor template",
    function_slots=(
        FunctionSlot("Protagonist", FunctionMultiplicity.EXACTLY_ONE),
        FunctionSlot("Antagonist",  FunctionMultiplicity.EXACTLY_ONE),
    ),
)

ENSEMBLE = Template(
    id="ensemble",
    name="ensemble template",
    function_slots=(
        FunctionSlot("voice", FunctionMultiplicity.AT_LEAST_ONE),
    ),
)

STANDARD_TEMPLATES = (DRAMATICA_8, THREE_ACTOR, TWO_ACTOR, ENSEMBLE)


def standard_templates_index() -> dict:
    """A dict mapping template id to Template, drawn from
    STANDARD_TEMPLATES. Authors with a custom Template build their own
    dict and pass it to `verify`."""
    return {t.id: t for t in STANDARD_TEMPLATES}


# ============================================================================
# Records
# ============================================================================


@dataclass(frozen=True)
class Argument:
    """A claim the Story interrogates. M1 — a Story may have zero or
    more. `parent_argument_id` admits nested polyphony.

    `domain` is an author-free-form classification tag (Flavor coupling
    per the four-coupling-kinds framework — no formal verifier).
    """
    id: str
    premise: str
    resolution_direction: ResolutionDirection
    counter_premise: Optional[str] = None
    domain: Optional[str] = None
    parent_argument_id: Optional[str] = None
    authored_by: str = "author"


@dataclass(frozen=True)
class ArgumentContribution:
    """A Throughline's stated contribution to a specific Argument."""
    argument_id: str
    side: ArgumentSide


@dataclass(frozen=True)
class Throughline:
    """A structural role within the Argument. M2 — roles, not
    characters. `owners` is the single authoritative source for which
    Characters fill the role (the dialect explicitly does not
    re-assert this on the Character record).

    `owners` admits Character ids and the abstract sentinels
    THROUGHLINE_OWNER_NONE / THROUGHLINE_OWNER_SITUATION /
    THROUGHLINE_OWNER_RELATIONSHIP.
    """
    id: str
    role_label: str
    owners: tuple   # tuple[str, ...]
    subject: str
    counterpoint_throughline_ids: tuple = ()
    argument_contributions: tuple = ()  # tuple[ArgumentContribution, ...]
    stakes_id: Optional[str] = None
    authored_by: str = "author"


@dataclass(frozen=True)
class Character:
    """A person or anthropomorphized agent. M2's ownership convention:
    Throughline ownership is per Throughline.owners only — this record
    does NOT carry an inverse `throughlines` field, because two
    authoritative-looking fields that could disagree is exactly the
    drift the schema-inclusion test rules out.

    `function_labels` are drawn from the Story's declared Template; an
    unknown label surfaces as an observation from the verifier.
    """
    id: str
    name: str
    function_labels: tuple = ()  # tuple[str, ...]
    authored_by: str = "author"


@dataclass(frozen=True)
class Beat:
    """A developmental moment within a Throughline. Optional anchor
    for Scene.advances; Stories that don't author Beats can have
    Scenes that name a Throughline directly.
    """
    id: str
    throughline_id: str
    beat_position: int
    beat_type: Optional[str] = None
    description_of_change: str = ""
    authored_by: str = "author"


@dataclass(frozen=True)
class SceneAdvancement:
    """One throughline-and-optional-beat that a Scene advances.
    `beat_id` is optional: a Scene may name a Throughline without
    pointing at a specific Beat (most useful for early-draft Stories
    where Beats are not yet authored)."""
    throughline_id: str
    beat_id: Optional[str] = None


@dataclass(frozen=True)
class Scene:
    """A unit of argumentative work. M3 — declared purpose. A Scene
    with empty `advances` is admissible (the verifier surfaces it as
    an observation, not an error)."""
    id: str
    title: str
    narrative_position: int
    advances: tuple = ()  # tuple[SceneAdvancement, ...]
    conflict_shape: str = ""
    result: str = ""
    authored_by: str = "author"


@dataclass(frozen=True)
class StakesOwner:
    """Stakes are owned by a Throughline or by the Story as a whole."""
    kind: StakesOwnerKind
    id: str


@dataclass(frozen=True)
class Stakes:
    """Risk and reward. M6 — first-class. Authored separately from the
    Throughline because Stakes are often a distinct authorial move
    (a Throughline may exist without yet-clarified Stakes); the
    temporal gap between Throughline-exists and Stakes-exists is
    diagnostic."""
    id: str
    owner: StakesOwner
    at_risk: str
    to_gain: str
    external_manifestation: str = ""
    authored_by: str = "author"


@dataclass(frozen=True)
class Story:
    """The dialect's root record. Aggregates other records by id.

    `character_function_template_id` declares which Template the Story
    uses. None means no function declarations and no template-
    conformance check is run.
    """
    id: str
    title: str
    character_function_template_id: Optional[str] = None
    argument_ids: tuple = ()
    throughline_ids: tuple = ()
    character_ids: tuple = ()
    scene_ids: tuple = ()
    beat_ids: tuple = ()
    stakes_ids: tuple = ()
    authored_by: str = "author"


# ============================================================================
# Self-verifier (M8)
# ============================================================================


@dataclass(frozen=True)
class Observation:
    """One self-verifier finding, emitted to be walked or ingested by
    higher-level tooling. Severity is a hint:

    - "noted": informational; e.g., "this Scene declares no advances"
    - "advises-review": something genuinely warrants attention; e.g.,
      a Template slot is unfilled or overfilled.

    `code` is a short stable tag the walker can group by.
    `target_id` is the record id (or label-pair like
    "label:Antagonist") the observation is about.
    """
    severity: str
    code: str
    target_id: str
    message: str


def _index(records: Iterable, attr: str = "id") -> dict:
    """Index a sequence of records by an attribute (default `id`)."""
    return {getattr(r, attr): r for r in records}


def _check_id_resolution(
    story: Story,
    arguments_by_id: dict,
    throughlines_by_id: dict,
    characters_by_id: dict,
    scenes_by_id: dict,
    beats_by_id: dict,
    stakes_by_id: dict,
    templates_by_id: dict,
) -> list:
    """Every record reference resolves to an existing record.

    Catches: Story.character_function_template_id, Story.*_ids;
    Throughline.owners (Character ids only — sentinels are not
    checked); Throughline.counterpoint_throughline_ids;
    Throughline.argument_contributions[*].argument_id;
    Throughline.stakes_id; Beat.throughline_id;
    Scene.advances[*].throughline_id and beat_id; Stakes.owner.
    """
    out = []

    # Story → Template
    if story.character_function_template_id is not None:
        if story.character_function_template_id not in templates_by_id:
            out.append(Observation(
                severity="advises-review",
                code="id_unresolved",
                target_id=story.id,
                message=(f"Story.character_function_template_id "
                         f"{story.character_function_template_id!r} "
                         f"does not resolve to any known Template"),
            ))

    # Story → record sets
    for kind, ids, table in (
        ("Argument",   story.argument_ids,   arguments_by_id),
        ("Throughline", story.throughline_ids, throughlines_by_id),
        ("Character",  story.character_ids,  characters_by_id),
        ("Scene",      story.scene_ids,      scenes_by_id),
        ("Beat",       story.beat_ids,       beats_by_id),
        ("Stakes",     story.stakes_ids,     stakes_by_id),
    ):
        for ref_id in ids:
            if ref_id not in table:
                out.append(Observation(
                    severity="advises-review",
                    code="id_unresolved",
                    target_id=story.id,
                    message=(f"Story.{kind.lower()}_ids references "
                             f"{ref_id!r}, which does not resolve to "
                             f"any {kind} record"),
                ))

    # Throughline → Character ids and argument ids
    for t in throughlines_by_id.values():
        for owner in t.owners:
            if owner in ABSTRACT_THROUGHLINE_OWNERS:
                continue
            if owner not in characters_by_id:
                out.append(Observation(
                    severity="advises-review",
                    code="id_unresolved",
                    target_id=t.id,
                    message=(f"Throughline.owners references "
                             f"{owner!r}, neither a Character id nor "
                             f"a recognized abstract owner"),
                ))
        for ref_id in t.counterpoint_throughline_ids:
            if ref_id not in throughlines_by_id:
                out.append(Observation(
                    severity="advises-review",
                    code="id_unresolved",
                    target_id=t.id,
                    message=(f"Throughline.counterpoint references "
                             f"{ref_id!r}, no such Throughline"),
                ))
        for contrib in t.argument_contributions:
            if contrib.argument_id not in arguments_by_id:
                out.append(Observation(
                    severity="advises-review",
                    code="id_unresolved",
                    target_id=t.id,
                    message=(f"Throughline argument_contribution "
                             f"references Argument {contrib.argument_id!r}, "
                             f"no such Argument"),
                ))
        if t.stakes_id is not None and t.stakes_id not in stakes_by_id:
            out.append(Observation(
                severity="advises-review",
                code="id_unresolved",
                target_id=t.id,
                message=(f"Throughline.stakes_id {t.stakes_id!r} "
                         f"does not resolve to any Stakes"),
            ))

    # Beat → Throughline
    for b in beats_by_id.values():
        if b.throughline_id not in throughlines_by_id:
            out.append(Observation(
                severity="advises-review",
                code="id_unresolved",
                target_id=b.id,
                message=(f"Beat.throughline_id {b.throughline_id!r} "
                         f"does not resolve to any Throughline"),
            ))

    # Scene → Throughline / Beat (per advancement)
    for s in scenes_by_id.values():
        for adv in s.advances:
            if adv.throughline_id not in throughlines_by_id:
                out.append(Observation(
                    severity="advises-review",
                    code="id_unresolved",
                    target_id=s.id,
                    message=(f"Scene advances Throughline "
                             f"{adv.throughline_id!r}, no such "
                             f"Throughline"),
                ))
            if adv.beat_id is not None and adv.beat_id not in beats_by_id:
                out.append(Observation(
                    severity="advises-review",
                    code="id_unresolved",
                    target_id=s.id,
                    message=(f"Scene advances Beat {adv.beat_id!r}, "
                             f"no such Beat"),
                ))

    # Stakes → owner
    for st in stakes_by_id.values():
        owner_id = st.owner.id
        if st.owner.kind == StakesOwnerKind.THROUGHLINE:
            if owner_id not in throughlines_by_id:
                out.append(Observation(
                    severity="advises-review",
                    code="id_unresolved",
                    target_id=st.id,
                    message=(f"Stakes.owner names Throughline "
                             f"{owner_id!r}, no such Throughline"),
                ))
        elif st.owner.kind == StakesOwnerKind.STORY:
            if owner_id != story.id:
                out.append(Observation(
                    severity="advises-review",
                    code="id_unresolved",
                    target_id=st.id,
                    message=(f"Stakes.owner names Story {owner_id!r}, "
                             f"does not match this Story id {story.id!r}"),
                ))

    return out


def _check_beat_sequencing(beats_by_id: dict) -> list:
    """Beats within a Throughline have distinct beat_position values."""
    out = []
    by_throughline = {}
    for b in beats_by_id.values():
        by_throughline.setdefault(b.throughline_id, []).append(b)
    for t_id, group in by_throughline.items():
        positions = [b.beat_position for b in group]
        if len(positions) != len(set(positions)):
            duplicates = [p for p in positions if positions.count(p) > 1]
            out.append(Observation(
                severity="advises-review",
                code="beat_position_duplicate",
                target_id=t_id,
                message=(f"Throughline {t_id!r} has Beats at "
                         f"duplicate positions: {sorted(set(duplicates))}"),
            ))
    return out


def _check_scene_sequencing(scenes_by_id: dict) -> list:
    """Scenes have distinct narrative_position values across the
    Story."""
    out = []
    positions = [s.narrative_position for s in scenes_by_id.values()]
    if len(positions) != len(set(positions)):
        duplicates = sorted({p for p in positions if positions.count(p) > 1})
        for s in scenes_by_id.values():
            if s.narrative_position in duplicates:
                out.append(Observation(
                    severity="advises-review",
                    code="scene_position_duplicate",
                    target_id=s.id,
                    message=(f"Scene {s.id!r} narrative_position "
                             f"{s.narrative_position} is shared with "
                             f"another Scene"),
                ))
    return out


def _check_template_conformance(
    story: Story,
    characters_by_id: dict,
    templates_by_id: dict,
) -> list:
    """Soft template conformance: known-label check + multiplicity
    check. Per M9, a Story declaring a Template is not required to
    populate it fully; observations indicate incompleteness."""
    out = []
    if story.character_function_template_id is None:
        return out
    template = templates_by_id.get(story.character_function_template_id)
    if template is None:
        # Already reported by id-resolution check; nothing more to do.
        return out

    known = set(template.labels())

    # Known-label check.
    for c in characters_by_id.values():
        for label in c.function_labels:
            if label not in known:
                out.append(Observation(
                    severity="advises-review",
                    code="function_label_unknown",
                    target_id=c.id,
                    message=(f"Character {c.id!r} carries function "
                             f"{label!r}, not in Template "
                             f"{template.id!r}'s vocabulary "
                             f"{sorted(known)}"),
                ))

    # Multiplicity check.
    counts = {label: 0 for label in known}
    for c in characters_by_id.values():
        for label in c.function_labels:
            if label in counts:
                counts[label] += 1
    for slot in template.function_slots:
        c = counts[slot.label]
        m = slot.multiplicity
        if m == FunctionMultiplicity.EXACTLY_ONE:
            if c == 0:
                out.append(Observation(
                    severity="advises-review",
                    code="slot_unfilled",
                    target_id=f"label:{slot.label}",
                    message=(f"Template slot {slot.label!r} "
                             f"(exactly-one) has no Character; expected 1"),
                ))
            elif c >= 2:
                out.append(Observation(
                    severity="advises-review",
                    code="slot_overfilled",
                    target_id=f"label:{slot.label}",
                    message=(f"Template slot {slot.label!r} "
                             f"(exactly-one) has {c} Characters; "
                             f"expected 1"),
                ))
        elif m == FunctionMultiplicity.AT_MOST_ONE:
            if c >= 2:
                out.append(Observation(
                    severity="advises-review",
                    code="slot_overfilled",
                    target_id=f"label:{slot.label}",
                    message=(f"Template slot {slot.label!r} "
                             f"(at-most-one) has {c} Characters; "
                             f"expected at most 1"),
                ))
        elif m == FunctionMultiplicity.AT_LEAST_ONE:
            if c == 0:
                out.append(Observation(
                    severity="advises-review",
                    code="slot_unfilled",
                    target_id=f"label:{slot.label}",
                    message=(f"Template slot {slot.label!r} "
                             f"(at-least-one) has no Character; "
                             f"expected at least 1"),
                ))
        # ANY: never triggers.
    return out


def _check_argument_completeness(
    arguments_by_id: dict,
    scenes_by_id: dict,
    throughlines_by_id: dict,
    beats_by_id: dict,
) -> list:
    """For each Argument with a non-UNRESOLVED resolution_direction,
    note whether any Scene or final Beat appears to resolve it.

    Deliberately weak — this is a literal text check. Genuine
    resolution is interpretive and lives in descriptions; the verifier
    only flags total absence of any plausibly-resolving Scene/Beat.

    A Scene "appears to resolve" an Argument if its `result` text is
    non-empty AND it advances a Throughline that contributes to that
    Argument. A Beat "appears to resolve" if it has the highest
    beat_position within its Throughline AND that Throughline
    contributes to the Argument.
    """
    out = []
    for arg in arguments_by_id.values():
        if arg.resolution_direction == ResolutionDirection.UNRESOLVED:
            continue

        # Find Throughlines contributing to this Argument.
        contributing = [
            t for t in throughlines_by_id.values()
            if any(c.argument_id == arg.id for c in t.argument_contributions)
        ]
        if not contributing:
            out.append(Observation(
                severity="noted",
                code="argument_no_throughline_contribution",
                target_id=arg.id,
                message=(f"Argument {arg.id!r} declares "
                         f"resolution_direction "
                         f"{arg.resolution_direction.value!r} but no "
                         f"Throughline declares contribution to it"),
            ))
            continue

        contributing_ids = {t.id for t in contributing}
        # Plausible-resolution Scene check.
        plausibly_resolving = []
        for s in scenes_by_id.values():
            if not s.result.strip():
                continue
            for adv in s.advances:
                if adv.throughline_id in contributing_ids:
                    plausibly_resolving.append(s)
                    break
        if not plausibly_resolving:
            out.append(Observation(
                severity="noted",
                code="argument_no_resolving_scene",
                target_id=arg.id,
                message=(f"Argument {arg.id!r} declares "
                         f"resolution_direction "
                         f"{arg.resolution_direction.value!r} but no "
                         f"Scene with a non-empty `result` advances any "
                         f"contributing Throughline; the resolution may "
                         f"be unrealized in scene-level work"),
            ))
    return out


def _check_stakes_coverage(
    throughlines_by_id: dict,
    stakes_by_id: dict,
) -> list:
    """Throughlines with no Stakes record surface as observations."""
    out = []
    for t in throughlines_by_id.values():
        if t.stakes_id is None:
            # Look for Stakes records that name this Throughline as owner.
            owns_us = [
                s for s in stakes_by_id.values()
                if s.owner.kind == StakesOwnerKind.THROUGHLINE
                and s.owner.id == t.id
            ]
            if not owns_us:
                out.append(Observation(
                    severity="noted",
                    code="throughline_no_stakes",
                    target_id=t.id,
                    message=(f"Throughline {t.id!r} has no declared "
                             f"Stakes (neither via stakes_id nor via "
                             f"a Stakes record naming it as owner)"),
                ))
    return out


def _check_scene_purpose(scenes_by_id: dict) -> list:
    """Scenes with empty `advances` surface as observations."""
    out = []
    for s in scenes_by_id.values():
        if not s.advances:
            out.append(Observation(
                severity="noted",
                code="scene_no_purpose",
                target_id=s.id,
                message=(f"Scene {s.id!r} declares no `advances` — no "
                         f"Throughline or Beat is named as the unit "
                         f"of argumentative work this Scene performs"),
            ))
    return out


def _check_orphans(
    story: Story,
    arguments_by_id: dict,
    throughlines_by_id: dict,
    characters_by_id: dict,
    scenes_by_id: dict,
    beats_by_id: dict,
    stakes_by_id: dict,
) -> list:
    """Records present in any of the by_id dicts but not referenced
    from Story.*_ids surface as observations."""
    out = []
    for kind, table, story_ids in (
        ("Argument",   arguments_by_id,   set(story.argument_ids)),
        ("Throughline", throughlines_by_id, set(story.throughline_ids)),
        ("Character",  characters_by_id,  set(story.character_ids)),
        ("Scene",      scenes_by_id,      set(story.scene_ids)),
        ("Beat",       beats_by_id,       set(story.beat_ids)),
        ("Stakes",     stakes_by_id,      set(story.stakes_ids)),
    ):
        for record_id in table:
            if record_id not in story_ids:
                out.append(Observation(
                    severity="noted",
                    code="record_orphan",
                    target_id=record_id,
                    message=(f"{kind} {record_id!r} is not referenced "
                             f"from Story.{kind.lower()}_ids; it is "
                             f"orphaned in the Story's record graph"),
                ))
    return out


def verify(
    story: Story,
    *,
    arguments: tuple = (),
    throughlines: tuple = (),
    characters: tuple = (),
    scenes: tuple = (),
    beats: tuple = (),
    stakes: tuple = (),
    templates: Optional[dict] = None,
) -> list:
    """Run all M8 self-verification checks on a Story plus its
    record bundle. Returns a list of Observations.

    `templates` maps template id to Template; defaults to
    STANDARD_TEMPLATES.

    Per M8, no check rejects a Story; observations are advisory and
    flow to the proposal queue (in a higher layer) for author
    walking. Verification is a partner, not a gate.
    """
    if templates is None:
        templates = standard_templates_index()

    arguments_by_id   = _index(arguments)
    throughlines_by_id = _index(throughlines)
    characters_by_id  = _index(characters)
    scenes_by_id      = _index(scenes)
    beats_by_id       = _index(beats)
    stakes_by_id      = _index(stakes)

    out = []
    out.extend(_check_id_resolution(
        story, arguments_by_id, throughlines_by_id, characters_by_id,
        scenes_by_id, beats_by_id, stakes_by_id, templates,
    ))
    out.extend(_check_beat_sequencing(beats_by_id))
    out.extend(_check_scene_sequencing(scenes_by_id))
    out.extend(_check_template_conformance(story, characters_by_id, templates))
    out.extend(_check_argument_completeness(
        arguments_by_id, scenes_by_id, throughlines_by_id, beats_by_id,
    ))
    out.extend(_check_stakes_coverage(throughlines_by_id, stakes_by_id))
    out.extend(_check_scene_purpose(scenes_by_id))
    out.extend(_check_orphans(
        story, arguments_by_id, throughlines_by_id, characters_by_id,
        scenes_by_id, beats_by_id, stakes_by_id,
    ))
    return out


# ============================================================================
# Convenience grouping for observations
# ============================================================================


def group_by_severity(observations: list) -> dict:
    """Bucket observations into {'noted': [...], 'advises-review': [...]}."""
    out = {"noted": [], "advises-review": []}
    for o in observations:
        out.setdefault(o.severity, []).append(o)
    return out


def group_by_code(observations: list) -> dict:
    """Bucket observations into a dict keyed by `code` for scan-friendly
    reporting."""
    out = {}
    for o in observations:
        out.setdefault(o.code, []).append(o)
    return out


# ============================================================================
# Per-record-type coupling-kind declarations (verification-sketch-01 V5)
# ============================================================================
#
# These declarations name, per record type and per field, which coupling
# kind from the four-coupling-kinds framework (lowering-sketch-01 F1)
# applies. Verifiers read these declarations to know which check to run
# for each record/field pair; authors read them to know what to expect.
#
# The four coupling kinds (per the framework, repeated here for clarity):
#
# - "realization":  upper record made true by specific lower records;
#                   uses Lowering machinery (lowering-record-sketch-01)
# - "characterization": upper record classifies a substrate pattern;
#                   uses verification (verification-sketch-01)
# - "claim-moment": upper record asserts substrate state at a τ_s;
#                   uses verification (Claim-moment primitive)
# - "claim-trajectory": upper record asserts substrate trajectory across
#                   τ_s range; uses verification (Claim-trajectory primitive)
# - "flavor":       free-form author metadata; no formal check
#
# A record type may admit multiple coupling kinds across different
# fields (e.g., Argument has trajectory-Claim and Flavor fields); each
# (record_type, field) pair maps to one coupling kind. field=None means
# the declaration applies to the whole record.

COUPLING_REALIZATION = "realization"
COUPLING_CHARACTERIZATION = "characterization"
COUPLING_CLAIM_MOMENT = "claim-moment"
COUPLING_CLAIM_TRAJECTORY = "claim-trajectory"
COUPLING_FLAVOR = "flavor"

VALID_COUPLING_KINDS = frozenset({
    COUPLING_REALIZATION, COUPLING_CHARACTERIZATION,
    COUPLING_CLAIM_MOMENT, COUPLING_CLAIM_TRAJECTORY,
    COUPLING_FLAVOR,
})


@dataclass(frozen=True)
class CouplingDeclaration:
    """One per-record-type-or-field coupling-kind declaration. `field`
    is the optional field name; None means the declaration applies to
    the whole record. `kind` is a coupling kind string (one of
    VALID_COUPLING_KINDS)."""
    record_type: str
    field: Optional[str]
    kind: str


COUPLING_DECLARATIONS = (
    # Story root — the whole record realizes (Story binds to the
    # substrate's branch / fold the story is encoded against).
    CouplingDeclaration("Story", None, COUPLING_REALIZATION),

    # Argument fields. The premise and resolution_direction are
    # Claim-trajectory (the substrate trajectory should exhibit
    # the premise's resolution as authored). The domain tag is
    # Flavor (free-form classification, no verifier).
    CouplingDeclaration("Argument", "premise", COUPLING_CLAIM_TRAJECTORY),
    CouplingDeclaration("Argument", "counter_premise", COUPLING_FLAVOR),
    CouplingDeclaration("Argument", "resolution_direction", COUPLING_CLAIM_TRAJECTORY),
    CouplingDeclaration("Argument", "domain", COUPLING_FLAVOR),

    # Throughline fields. Owners realize (Characters lower to Entities;
    # the Throughline's owner-set is realized by the Entity-set the
    # owner Characters lower to). Role_label and subject are
    # Characterizations (they classify what kind of Throughline this
    # is; a verifier checks the substrate exhibits the matching
    # pattern). Argument_contributions are Claim-trajectory
    # (the throughline's contribution should be visible in the
    # substrate trajectory). Stakes_id is structural (a within-
    # dialect link; substrate doesn't see it).
    CouplingDeclaration("Throughline", "owners", COUPLING_REALIZATION),
    CouplingDeclaration("Throughline", "role_label", COUPLING_CHARACTERIZATION),
    CouplingDeclaration("Throughline", "subject", COUPLING_CHARACTERIZATION),
    CouplingDeclaration("Throughline", "argument_contributions",
                        COUPLING_CLAIM_TRAJECTORY),

    # Character — the whole record realizes (a Dramatic Character is
    # made true by a substrate Entity).
    CouplingDeclaration("Character", None, COUPLING_REALIZATION),

    # Beat fields. description_of_change is a Claim-moment about
    # what changes at this beat in the substrate.
    CouplingDeclaration("Beat", "description_of_change", COUPLING_CLAIM_MOMENT),

    # Scene fields. Advances realize via Lowering (Scene → Events).
    # Result and conflict_shape are Claim-moment (about substrate
    # state at the scene's bounds).
    CouplingDeclaration("Scene", "advances", COUPLING_REALIZATION),
    CouplingDeclaration("Scene", "conflict_shape", COUPLING_CLAIM_MOMENT),
    CouplingDeclaration("Scene", "result", COUPLING_CLAIM_MOMENT),

    # Stakes fields. at_risk and to_gain are Claim-trajectory (what
    # could be lost / gained across the trajectory). external_manifestation
    # is Claim-moment (how the stakes show up to the reader at
    # specific moments in the substrate).
    CouplingDeclaration("Stakes", "at_risk", COUPLING_CLAIM_TRAJECTORY),
    CouplingDeclaration("Stakes", "to_gain", COUPLING_CLAIM_TRAJECTORY),
    CouplingDeclaration("Stakes", "external_manifestation",
                        COUPLING_CLAIM_MOMENT),
)


def coupling_kind_for(record_type: str, field: Optional[str] = None) -> Optional[str]:
    """Look up the coupling kind for a (record_type, field) pair.
    Returns the coupling kind string, or None if no declaration
    applies. If a record-level declaration (field=None) exists for
    the record_type and the caller asks about a specific field, the
    record-level declaration falls through (record-level applies to
    every field unless overridden). Specific field declarations win
    over record-level when both exist."""
    # Specific-field match first.
    for d in COUPLING_DECLARATIONS:
        if d.record_type == record_type and d.field == field:
            return d.kind
    # Fall back to record-level (field=None).
    if field is not None:
        for d in COUPLING_DECLARATIONS:
            if d.record_type == record_type and d.field is None:
                return d.kind
    return None


def fields_with_coupling(record_type: str, kind: str) -> tuple:
    """Return the field names of `record_type` that carry coupling
    kind `kind`. Useful for verifiers that want to enumerate all
    fields of a given kind on a record type."""
    return tuple(
        d.field for d in COUPLING_DECLARATIONS
        if d.record_type == record_type and d.kind == kind
    )


def declarations_for_kind(kind: str) -> tuple:
    """All CouplingDeclarations for a given coupling kind, across all
    record types. Useful when a verifier wants to enumerate every
    record/field that needs its check run."""
    return tuple(d for d in COUPLING_DECLARATIONS if d.kind == kind)
