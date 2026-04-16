"""
dramatica_template.py — the `dramatica-complete` Template for the
Dramatic dialect, per dramatica-template-sketch-01.

This module extends the Dramatic dialect's Template mechanism with
Dramatica's Grand Argument Story theory. Per Q1, Templates may
declare their own record types; this module ships the record types,
the shipped theory data (quad labels), and the self-verifier
extensions that enforce Dramatica's structural rules.

Record types added (all per dramatica-template-sketch-01):

- **Quad** — the fundamental Dramatica structural unit. Four labeled
  positions arranged in a dynamic-pair / companion-pair crosshatch.
  Shipped as theory data for Domains + Concerns; author-instanced
  for Issues and Problems (deferred — pattern extends uniformly).

- **QuadPick** — a record saying "I choose position X from Quad Y,
  attached to record Z." Normalized: the Quad exists as a record,
  and the pick references it.

- **DomainAssignment** — assigns one of four Domains (Activity,
  Situation, Manipulation, Fixed Attitude) per Throughline. Four
  total, non-duplicative — Dramatica's hardest structural rule at
  this level.

- **DynamicStoryPoint** — six binary-choice records at Story level:
  Resolve (Change/Steadfast), Growth (Start/Stop), Approach
  (Do-er/Be-er), Limit (Timelock/Optionlock), Outcome (Success/
  Failure), Judgment (Good/Bad).

- **Signpost** — four per Throughline, representing act-progression
  moments. Each names which Concern from the Throughline's Domain
  the Throughline passes through at that position.

Shipped theory data:

- The Domain Quad (4 positions).
- Four Concern Quads (one per Domain, 4 Concerns each = 16 total).
  These are Dramatica's canonical Type labels per Domain.

Internal rules ("nope, you can't do that"):

- Domain assignments must cover all 4 Domains exactly once across
  the 4 Throughlines. No duplicates.
- Six DynamicStoryPoints must be present, one per axis, each with a
  valid choice.
- Signposts: 4 per Throughline, positions 1-4 distinct, elements
  drawn from the Throughline's assigned Domain's Concern quad.
- Throughline count exactly 4, role_labels covering the four
  required labels.

The module does not yet ship Issue / Problem quad data (the 64 +
256 deeper levels); per the sketch's Q3 and OQ5, the pattern
extends uniformly and is deferred until an encoding pressures it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple


# ============================================================================
# Enums
# ============================================================================


class Domain(str, Enum):
    """Dramatica's four Domains — the broadest classification of
    a Throughline's conflict arena."""
    ACTIVITY = "activity"                # external + process
    SITUATION = "situation"              # external + state
    MANIPULATION = "manipulation"        # internal + process
    FIXED_ATTITUDE = "fixed-attitude"    # internal + state


class DSPAxis(str, Enum):
    """The six Dynamic Story Point axes."""
    RESOLVE = "resolve"
    GROWTH = "growth"
    APPROACH = "approach"
    LIMIT = "limit"
    OUTCOME = "outcome"
    JUDGMENT = "judgment"


class Resolve(str, Enum):
    CHANGE = "change"
    STEADFAST = "steadfast"


class Growth(str, Enum):
    START = "start"
    STOP = "stop"


class Approach(str, Enum):
    DO_ER = "do-er"
    BE_ER = "be-er"


class Limit(str, Enum):
    TIMELOCK = "timelock"
    OPTIONLOCK = "optionlock"


class Outcome(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class Judgment(str, Enum):
    GOOD = "good"
    BAD = "bad"


DSP_VALID_CHOICES = {
    DSPAxis.RESOLVE: {Resolve.CHANGE, Resolve.STEADFAST},
    DSPAxis.GROWTH: {Growth.START, Growth.STOP},
    DSPAxis.APPROACH: {Approach.DO_ER, Approach.BE_ER},
    DSPAxis.LIMIT: {Limit.TIMELOCK, Limit.OPTIONLOCK},
    DSPAxis.OUTCOME: {Outcome.SUCCESS, Outcome.FAILURE},
    DSPAxis.JUDGMENT: {Judgment.GOOD, Judgment.BAD},
}


class QuadPosition(str, Enum):
    """The four positions within a Quad."""
    A = "A"
    B = "B"
    C = "C"
    D = "D"


# ============================================================================
# Record types
# ============================================================================


@dataclass(frozen=True)
class Quad:
    """The fundamental Dramatica structural unit. Four labeled elements
    arranged with dynamic-pair and companion-pair internal structure:
        A ←─ dynamic ─→ C
        ↕                ↕
        companion        companion
        ↕                ↕
        B ←─ dynamic ─→ D
    Dynamic pairs: (A, C), (B, D).
    Companion pairs: (A, B), (C, D).
    Dependent pairs (derived): (A, D), (B, C).
    """
    id: str
    kind: str                     # e.g., "domain-quad", "concern-activity-quad"
    element_A: str
    element_B: str
    element_C: str
    element_D: str
    authored_by: str = "dramatica-theory"

    @property
    def dynamic_pairs(self) -> tuple:
        return (
            (self.element_A, self.element_C),
            (self.element_B, self.element_D),
        )

    @property
    def companion_pairs(self) -> tuple:
        return (
            (self.element_A, self.element_B),
            (self.element_C, self.element_D),
        )

    @property
    def dependent_pairs(self) -> tuple:
        return (
            (self.element_A, self.element_D),
            (self.element_B, self.element_C),
        )

    def element_at(self, position: QuadPosition) -> str:
        return {
            QuadPosition.A: self.element_A,
            QuadPosition.B: self.element_B,
            QuadPosition.C: self.element_C,
            QuadPosition.D: self.element_D,
        }[position]

    def dynamic_pair_of(self, position: QuadPosition) -> QuadPosition:
        """Return the position dynamically opposed to the given one."""
        return {
            QuadPosition.A: QuadPosition.C,
            QuadPosition.B: QuadPosition.D,
            QuadPosition.C: QuadPosition.A,
            QuadPosition.D: QuadPosition.B,
        }[position]


@dataclass(frozen=True)
class QuadPick:
    """A record saying 'I choose position X from Quad Y, attached to
    record Z.' The Quad is the theory data; the pick is the authorial
    choice per encoding."""
    id: str
    quad_id: str                  # references a Quad.id
    chosen_position: QuadPosition
    attached_to_kind: str         # e.g., "throughline", "story"
    attached_to_id: str           # id of the attached record
    authored_by: str = "author"


@dataclass(frozen=True)
class DomainAssignment:
    """Assigns one of four Domains to a Throughline. Dramatica requires
    all four Domains covered across the four Throughlines — no
    duplicates. This is the template's hardest structural rule at
    this level."""
    id: str
    throughline_id: str
    domain: Domain
    authored_by: str = "author"


@dataclass(frozen=True)
class DynamicStoryPoint:
    """One of six binary-choice records at Story level. Per Q5, all
    six are expected when the Template is `dramatica-complete`."""
    id: str
    axis: DSPAxis
    choice: str                   # value from the axis's valid set
    story_id: str
    authored_by: str = "author"

    def __post_init__(self):
        valid = DSP_VALID_CHOICES.get(self.axis, set())
        if self.choice not in {v.value for v in valid}:
            raise ValueError(
                f"DynamicStoryPoint {self.id!r}: choice "
                f"{self.choice!r} is not valid for axis "
                f"{self.axis.value!r}; valid choices are "
                f"{sorted(v.value for v in valid)}"
            )


@dataclass(frozen=True)
class Signpost:
    """One act-progression marker on a Throughline. Four per Throughline,
    positions 1-4. Each names a Concern (Type) from the Throughline's
    assigned Domain. The four Signposts of a Throughline use all four
    Concerns of its Domain, in a progression order the author declares.
    """
    id: str
    throughline_id: str
    signpost_position: int        # 1..4
    signpost_element: str         # a Concern label from the Domain
    authored_by: str = "author"

    def __post_init__(self):
        if not (1 <= self.signpost_position <= 4):
            raise ValueError(
                f"Signpost {self.id!r}: signpost_position "
                f"{self.signpost_position} out of range; must be 1-4"
            )


# ============================================================================
# Shipped theory data — Domain Quad + four Concern Quads
# ============================================================================
#
# Dramatica's canonical quad labels. These are theory-data, not
# authorial content — they ship with the Template.

DOMAIN_QUAD = Quad(
    id="dramatica_domain_quad",
    kind="domain-quad",
    element_A=Domain.ACTIVITY.value,
    element_B=Domain.SITUATION.value,
    element_C=Domain.MANIPULATION.value,
    element_D=Domain.FIXED_ATTITUDE.value,
)

# Concern Quads — one per Domain. Each Domain has four Types (Concerns)
# that describe the specific nature of conflict within that Domain.

CONCERN_ACTIVITY_QUAD = Quad(
    id="concern_activity_quad",
    kind="concern-quad",
    element_A="understanding",
    element_B="doing",
    element_C="obtaining",
    element_D="learning",
)

CONCERN_SITUATION_QUAD = Quad(
    id="concern_situation_quad",
    kind="concern-quad",
    element_A="the-past",
    element_B="how-things-are-changing",
    element_C="the-future",
    element_D="the-present",
)

CONCERN_MANIPULATION_QUAD = Quad(
    id="concern_manipulation_quad",
    kind="concern-quad",
    element_A="developing-a-plan",
    element_B="playing-a-role",
    element_C="changing-one's-nature",
    element_D="conceiving-an-idea",
)

CONCERN_FIXED_ATTITUDE_QUAD = Quad(
    id="concern_fixed_attitude_quad",
    kind="concern-quad",
    element_A="innermost-desires",
    element_B="impulsive-responses",
    element_C="contemplation",
    element_D="memories",
)

CONCERN_QUADS_BY_DOMAIN = {
    Domain.ACTIVITY: CONCERN_ACTIVITY_QUAD,
    Domain.SITUATION: CONCERN_SITUATION_QUAD,
    Domain.MANIPULATION: CONCERN_MANIPULATION_QUAD,
    Domain.FIXED_ATTITUDE: CONCERN_FIXED_ATTITUDE_QUAD,
}

ALL_SHIPPED_QUADS = (
    DOMAIN_QUAD,
    CONCERN_ACTIVITY_QUAD,
    CONCERN_SITUATION_QUAD,
    CONCERN_MANIPULATION_QUAD,
    CONCERN_FIXED_ATTITUDE_QUAD,
)


# ============================================================================
# Observation record — same shape as Dramatic's but template-specific
# ============================================================================


@dataclass(frozen=True)
class DramaticaObservation:
    """One self-verifier finding from the Dramatica template checks.
    Severity is 'noted' or 'advises-review'; code is a stable tag."""
    severity: str
    code: str
    target_id: str
    message: str


SEVERITY_NOTED = "noted"
SEVERITY_ADVISES_REVIEW = "advises-review"


# ============================================================================
# Self-verification — the "nope, you can't do that" rules
# ============================================================================


def _check_throughline_count(throughlines: tuple) -> list:
    """Dramatica requires exactly 4 Throughlines with the four
    canonical role_labels."""
    out = []
    if len(throughlines) != 4:
        out.append(DramaticaObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="throughline_count_wrong",
            target_id="story",
            message=(f"Dramatica requires exactly 4 Throughlines; "
                     f"got {len(throughlines)}"),
        ))
    required_roles = {
        "overall-story", "main-character",
        "impact-character", "relationship",
    }
    found_roles = {t.role_label for t in throughlines}
    missing = required_roles - found_roles
    if missing:
        out.append(DramaticaObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="throughline_role_missing",
            target_id="story",
            message=(f"Missing Throughline role_labels: "
                     f"{sorted(missing)}"),
        ))
    return out


def _check_domain_assignments(
    assignments: tuple, throughlines: tuple,
) -> list:
    """Four DomainAssignments, one per Throughline, covering all four
    Domains without duplication."""
    out = []
    if len(assignments) != 4:
        out.append(DramaticaObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="domain_assignment_count_wrong",
            target_id="story",
            message=(f"Dramatica requires exactly 4 "
                     f"DomainAssignments; got {len(assignments)}"),
        ))

    # Check for duplicates.
    domains_used = [a.domain for a in assignments]
    domain_set = set(d.value for d in domains_used)
    if len(domain_set) < len(domains_used):
        dupes = [d.value for d in domains_used
                 if domains_used.count(d) > 1]
        out.append(DramaticaObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="domain_assignment_duplicate",
            target_id="story",
            message=(f"Duplicate Domain assignments: "
                     f"{sorted(set(dupes))}. Dramatica requires "
                     f"each Domain used exactly once."),
        ))

    # Check all four Domains covered.
    all_domains = {d.value for d in Domain}
    missing = all_domains - domain_set
    if missing:
        out.append(DramaticaObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="domain_assignment_incomplete",
            target_id="story",
            message=(f"Missing Domain assignments: "
                     f"{sorted(missing)}. Dramatica requires all "
                     f"four Domains covered."),
        ))

    # Check each assignment references a valid Throughline.
    tl_ids = {t.id for t in throughlines}
    for a in assignments:
        if a.throughline_id not in tl_ids:
            out.append(DramaticaObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="domain_assignment_throughline_unknown",
                target_id=a.id,
                message=(f"DomainAssignment {a.id!r} references "
                         f"Throughline {a.throughline_id!r} which "
                         f"is not in the encoding"),
            ))
    return out


def _check_dynamic_story_points(dsps: tuple) -> list:
    """Six DynamicStoryPoints, one per axis."""
    out = []
    axes_found = {dsp.axis for dsp in dsps}
    all_axes = {a for a in DSPAxis}
    missing = all_axes - axes_found
    if missing:
        out.append(DramaticaObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="dsp_missing",
            target_id="story",
            message=(f"Missing DynamicStoryPoint axes: "
                     f"{sorted(a.value for a in missing)}. "
                     f"Dramatica expects all six."),
        ))
    # Check for duplicates.
    if len(dsps) > len(axes_found):
        out.append(DramaticaObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="dsp_duplicate",
            target_id="story",
            message=(f"Duplicate DynamicStoryPoints: {len(dsps)} "
                     f"records for {len(axes_found)} axes"),
        ))
    return out


def _check_signposts(
    signposts: tuple, throughlines: tuple,
    domain_assignments: tuple,
) -> list:
    """Four Signposts per Throughline, positions 1-4 distinct,
    elements drawn from the Throughline's Domain's Concern quad."""
    out = []
    tl_ids = {t.id for t in throughlines}
    da_by_tl = {a.throughline_id: a.domain for a in domain_assignments}

    by_tl = {}
    for sp in signposts:
        by_tl.setdefault(sp.throughline_id, []).append(sp)

    for tl in throughlines:
        tl_sps = by_tl.get(tl.id, [])
        if len(tl_sps) != 4:
            out.append(DramaticaObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="signpost_count_wrong",
                target_id=tl.id,
                message=(f"Throughline {tl.id!r} has "
                         f"{len(tl_sps)} Signposts; Dramatica "
                         f"requires exactly 4"),
            ))
            continue

        # Positions 1-4 distinct.
        positions = [sp.signpost_position for sp in tl_sps]
        if sorted(positions) != [1, 2, 3, 4]:
            out.append(DramaticaObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="signpost_positions_invalid",
                target_id=tl.id,
                message=(f"Throughline {tl.id!r} Signpost positions "
                         f"are {sorted(positions)}; must be "
                         f"[1, 2, 3, 4]"),
            ))

        # Elements from the Domain's Concern quad.
        domain = da_by_tl.get(tl.id)
        if domain is not None:
            concern_quad = CONCERN_QUADS_BY_DOMAIN.get(domain)
            if concern_quad is not None:
                valid_elements = {
                    concern_quad.element_A, concern_quad.element_B,
                    concern_quad.element_C, concern_quad.element_D,
                }
                for sp in tl_sps:
                    if sp.signpost_element not in valid_elements:
                        out.append(DramaticaObservation(
                            severity=SEVERITY_ADVISES_REVIEW,
                            code="signpost_element_invalid",
                            target_id=sp.id,
                            message=(
                                f"Signpost {sp.id!r} element "
                                f"{sp.signpost_element!r} is not "
                                f"in Domain {domain.value!r}'s "
                                f"Concern quad "
                                f"{sorted(valid_elements)}"),
                        ))

                # All four Concern elements should be used.
                used = {sp.signpost_element for sp in tl_sps}
                unused = valid_elements - used
                if unused:
                    out.append(DramaticaObservation(
                        severity=SEVERITY_NOTED,
                        code="signpost_elements_incomplete",
                        target_id=tl.id,
                        message=(
                            f"Throughline {tl.id!r} Signposts use "
                            f"only {sorted(used)} from "
                            f"{sorted(valid_elements)}; Dramatica "
                            f"expects all four Concerns used "
                            f"across the 4 Signposts"),
                    ))

    return out


def _check_story_goal_consequence(
    story_goal: str, story_consequence: str,
) -> list:
    """Story Goal and Story Consequence should be present."""
    out = []
    if not story_goal.strip():
        out.append(DramaticaObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="story_goal_empty",
            target_id="story",
            message="Story Goal is empty; Dramatica expects it set",
        ))
    if not story_consequence.strip():
        out.append(DramaticaObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="story_consequence_empty",
            target_id="story",
            message=("Story Consequence is empty; Dramatica "
                     "expects it set"),
        ))
    return out


def verify_dramatica_complete(
    *,
    throughlines: tuple,
    domain_assignments: tuple = (),
    dynamic_story_points: tuple = (),
    signposts: tuple = (),
    story_goal: str = "",
    story_consequence: str = "",
) -> list:
    """Run all Dramatica-template structural checks. Returns a list
    of DramaticaObservation records.

    Per Q9, these compose *with* the base Dramatic dialect's M8
    checks — run both. The Template's checks do not replace the
    dialect's; they extend.

    Per the sketch: all checks emit observations, never errors. An
    encoding partway through Dramatica-fication gets observations
    naming what's missing, not a rejection.
    """
    out: list = []
    out.extend(_check_throughline_count(throughlines))
    out.extend(_check_domain_assignments(
        domain_assignments, throughlines,
    ))
    out.extend(_check_dynamic_story_points(dynamic_story_points))
    out.extend(_check_signposts(
        signposts, throughlines, domain_assignments,
    ))
    out.extend(_check_story_goal_consequence(
        story_goal, story_consequence,
    ))
    return out


# ============================================================================
# Convenience: Outcome × Judgment → canonical ending
# ============================================================================


def canonical_ending(outcome: str, judgment: str) -> str:
    """Dramatica's four-way ending categorization."""
    table = {
        (Outcome.SUCCESS.value, Judgment.GOOD.value): "triumph",
        (Outcome.SUCCESS.value, Judgment.BAD.value): "personal-tragedy",
        (Outcome.FAILURE.value, Judgment.GOOD.value): "personal-triumph",
        (Outcome.FAILURE.value, Judgment.BAD.value): "tragedy",
    }
    return table.get((outcome, judgment), "unknown")


# ============================================================================
# Character Element decomposition — Motivation Elements
# ============================================================================
#
# In Dramatica, the 8 archetypes decompose into pairs of Motivation
# Elements (16 total). Each element may be assigned to exactly one
# character — this is the "nope, you can't do that" rule with the
# most authorial bite: if Pursue is on your Protagonist, no other
# character may carry Pursue. The archetype is just a preset pairing;
# complex characters can reassign elements, but uniqueness holds.
#
# Dramatica has three additional element sets (Methodology, Evaluation,
# Purpose — 16 each, 48 more). They follow the same pattern. This
# module ships the Motivation set first; the others extend uniformly.


class MotivationElement(str, Enum):
    """The 16 Motivation Elements from Dramatica theory. Arranged as
    the motivations quad of quads:

    Protagonist quad:   Pursue / Consider
    Antagonist quad:    Prevent / Reconsider
    Reason quad:        Logic / Control
    Emotion quad:       Feeling / Uncontrolled
    Sidekick quad:      Faith / Support
    Skeptic quad:       Disbelief / Oppose
    Guardian quad:      Conscience / Help
    Contagonist quad:   Temptation / Hinder
    """
    PURSUE = "pursue"
    CONSIDER = "consider"
    AVOID = "avoid"
    RECONSIDER = "reconsider"
    LOGIC = "logic"
    CONTROL = "control"
    FEELING = "feeling"
    UNCONTROLLED = "uncontrolled"
    FAITH = "faith"
    SUPPORT = "support"
    DISBELIEF = "disbelief"
    OPPOSE = "oppose"
    CONSCIENCE = "conscience"
    HELP = "help"
    TEMPTATION = "temptation"
    HINDER = "hinder"


# The canonical archetype → motivation-element mapping. Each archetype
# gets exactly two motivation elements. 8 archetypes × 2 = 16 elements.
# If the author uses archetypes as-is, these are the assignments. If
# they build complex characters, they can reassign, but uniqueness
# across the cast must hold.

ARCHETYPE_MOTIVATION_ELEMENTS: dict = {
    "Protagonist": (MotivationElement.PURSUE, MotivationElement.CONSIDER),
    "Antagonist": (MotivationElement.AVOID, MotivationElement.RECONSIDER),
    "Reason": (MotivationElement.LOGIC, MotivationElement.CONTROL),
    "Emotion": (MotivationElement.FEELING, MotivationElement.UNCONTROLLED),
    "Sidekick": (MotivationElement.FAITH, MotivationElement.SUPPORT),
    "Skeptic": (MotivationElement.DISBELIEF, MotivationElement.OPPOSE),
    "Guardian": (MotivationElement.CONSCIENCE, MotivationElement.HELP),
    "Contagonist": (MotivationElement.TEMPTATION, MotivationElement.HINDER),
}


# The 4 Motivation Quads. Each archetype takes the companion pair
# (A+B or C+D) from one of these quads. Dynamic pairs are the
# fundamental oppositions; companion pairs are the cooperative set
# an archetype bundles.

MOTIVATION_QUAD_ACTION = Quad(
    id="motivation_quad_action",
    kind="motivation-quad",
    element_A="pursue",        # Protagonist's drive
    element_B="consider",      # Protagonist's deliberation
    element_C="avoid",         # Antagonist's evasion
    element_D="reconsider",    # Antagonist's re-evaluation
    authored_by="dramatica-theory",
)

MOTIVATION_QUAD_DECISION = Quad(
    id="motivation_quad_decision",
    kind="motivation-quad",
    element_A="faith",         # Sidekick's trust
    element_B="support",       # Sidekick's loyalty
    element_C="disbelief",     # Skeptic's doubt
    element_D="oppose",        # Skeptic's resistance
    authored_by="dramatica-theory",
)

MOTIVATION_QUAD_EVALUATION = Quad(
    id="motivation_quad_evaluation",
    kind="motivation-quad",
    element_A="logic",         # Reason's analysis
    element_B="control",       # Reason's governance
    element_C="feeling",       # Emotion's intuition
    element_D="uncontrolled",  # Emotion's abandon
    authored_by="dramatica-theory",
)

MOTIVATION_QUAD_PROTECTION = Quad(
    id="motivation_quad_protection",
    kind="motivation-quad",
    element_A="conscience",    # Guardian's moral compass
    element_B="help",          # Guardian's assistance
    element_C="temptation",    # Contagonist's lure
    element_D="hinder",        # Contagonist's obstruction
    authored_by="dramatica-theory",
)

ALL_MOTIVATION_QUADS = (
    MOTIVATION_QUAD_ACTION,
    MOTIVATION_QUAD_DECISION,
    MOTIVATION_QUAD_EVALUATION,
    MOTIVATION_QUAD_PROTECTION,
)


@dataclass(frozen=True)
class CharacterElementAssignment:
    """Assigns a Motivation Element to a Character. Per Dramatica,
    each element must be assigned to exactly one character in the
    encoding. Uniqueness is enforced by the template verifier."""
    id: str
    character_id: str
    element: MotivationElement
    authored_by: str = "author"


def _check_character_element_uniqueness(
    assignments: tuple,
) -> list:
    """Each Motivation Element may appear on at most one character.
    Duplicates are Dramatica's hardest character-level rule."""
    out = []
    element_to_chars: dict = {}
    for a in assignments:
        element_to_chars.setdefault(a.element, []).append(
            a.character_id
        )
    for element, chars in element_to_chars.items():
        if len(chars) > 1:
            out.append(DramaticaObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="element_assigned_to_multiple_characters",
                target_id=element.value,
                message=(
                    f"Motivation Element {element.value!r} is "
                    f"assigned to {len(chars)} characters: "
                    f"{chars}. Dramatica requires each element on "
                    f"exactly one character."
                ),
            ))
    return out


def _check_archetype_element_conformance(
    assignments: tuple,
    characters: tuple,
) -> list:
    """If a character carries an archetype function label AND has
    element assignments, check whether the assignments match the
    archetype's canonical elements. Divergence is an observation,
    not an error (complex characters diverge intentionally)."""
    out = []
    by_char: dict = {}
    for a in assignments:
        by_char.setdefault(a.character_id, set()).add(a.element)
    for char in characters:
        if not hasattr(char, "function_labels"):
            continue
        for fn in char.function_labels:
            if fn not in ARCHETYPE_MOTIVATION_ELEMENTS:
                continue
            canonical = set(ARCHETYPE_MOTIVATION_ELEMENTS[fn])
            actual = by_char.get(char.id, set())
            if not actual:
                continue  # no assignments yet — observation elsewhere
            if actual != canonical:
                out.append(DramaticaObservation(
                    severity=SEVERITY_NOTED,
                    code="archetype_element_divergence",
                    target_id=char.id,
                    message=(
                        f"Character {char.id!r} carries function "
                        f"{fn!r} whose canonical Motivation "
                        f"Elements are "
                        f"{sorted(e.value for e in canonical)}, "
                        f"but actual assignments are "
                        f"{sorted(e.value for e in actual)}. "
                        f"Divergence from archetype is valid for "
                        f"complex characters; verify intentional."
                    ),
                ))
    return out


# ============================================================================
# Pick-chain: Concern → Issue → Problem, with derivation
# ============================================================================
#
# Dramatica's nested hierarchy: each Throughline picks a Concern
# (from its Domain's Concern Quad), then an Issue (from that
# Concern's Issue Quad), then a Problem (from that Issue's Element
# Quad). Each pick constrains the next level's options.
#
# The Problem pick automatically derives:
#   Solution = dynamic pair of Problem in the Element Quad
#   Symptom = companion of Problem
#   Response = dependent of Problem
#
# These derivations are the sketch's forcing function #2. In this
# implementation, the derivation functions exist; the template
# verifier checks that any explicitly-authored Solution/Symptom/
# Response agrees with the derivation.
#
# Issue Quads (Variations under each Type/Concern): Dramatica ships
# canonical labels for each. A mapping from Concern-label → Issue
# Quad is needed for chain validation. The full 64 labels require
# canonical Dramatica reference; this module ships the mapping
# structure with selected entries and validates the chain where
# data is available.


# Issue Quad registry: maps Concern-label → Issue Quad.
# Entries are added as theory data is authored.
ISSUE_QUADS_BY_CONCERN: dict = {}


def register_issue_quad(concern_label: str, quad: Quad) -> None:
    """Register an Issue Quad for a specific Concern label. Called
    during module initialization as theory data is authored."""
    ISSUE_QUADS_BY_CONCERN[concern_label] = quad


# Element Quad registry: maps Issue-label → Element (Problem) Quad.
ELEMENT_QUADS_BY_ISSUE: dict = {}


def register_element_quad(issue_label: str, quad: Quad) -> None:
    """Register an Element Quad for a specific Issue label."""
    ELEMENT_QUADS_BY_ISSUE[issue_label] = quad


@dataclass(frozen=True)
class ThematicPicks:
    """All four levels of thematic picks for one Throughline.
    Concern, Issue, Problem are QuadPick records referencing the
    appropriate Quad at each level. Solution, Symptom, Response
    are derived from the Problem pick."""
    throughline_id: str
    concern_pick: QuadPick         # from Domain's Concern Quad
    issue_pick: QuadPick           # from chosen Concern's Issue Quad
    problem_pick: QuadPick         # from chosen Issue's Element Quad
    # Optional explicit Solution/Symptom/Response (for verification
    # against derivation).
    solution_override: Optional[str] = None
    symptom_override: Optional[str] = None
    response_override: Optional[str] = None


def derive_from_problem(problem_pick: QuadPick, quad: Quad) -> dict:
    """Given a Problem pick and its Quad, derive Solution, Symptom,
    and Response positions and labels.

    Returns a dict with keys 'solution', 'symptom', 'response',
    each containing (position, element_label)."""
    pos = problem_pick.chosen_position

    # Solution: dynamic pair
    sol_pos = quad.dynamic_pair_of(pos)

    # Symptom: companion (A↔B, C↔D)
    companion_map = {
        QuadPosition.A: QuadPosition.B,
        QuadPosition.B: QuadPosition.A,
        QuadPosition.C: QuadPosition.D,
        QuadPosition.D: QuadPosition.C,
    }
    sym_pos = companion_map[pos]

    # Response: dependent (A↔D, B↔C)
    dependent_map = {
        QuadPosition.A: QuadPosition.D,
        QuadPosition.B: QuadPosition.C,
        QuadPosition.C: QuadPosition.B,
        QuadPosition.D: QuadPosition.A,
    }
    rsp_pos = dependent_map[pos]

    return {
        "solution": (sol_pos, quad.element_at(sol_pos)),
        "symptom": (sym_pos, quad.element_at(sym_pos)),
        "response": (rsp_pos, quad.element_at(rsp_pos)),
    }


def _check_pick_chain(
    picks_list: tuple,
    domain_assignments: tuple,
) -> list:
    """Validate Concern → Issue → Problem chain integrity for each
    ThematicPicks record.

    Rules:
    - Concern pick's quad_id must match the Domain's Concern Quad
    - Issue pick's quad_id must match the chosen Concern's Issue Quad
      (if registered)
    - Problem pick's quad_id must match the chosen Issue's Element
      Quad (if registered)
    - If solution/symptom/response overrides are present, they must
      agree with derivation from the Problem pick
    """
    out = []
    da_by_tl = {a.throughline_id: a.domain for a in domain_assignments}

    for tp in picks_list:
        tl_id = tp.throughline_id
        domain = da_by_tl.get(tl_id)

        # Check Concern pick's quad matches the Domain's Concern Quad.
        if domain is not None:
            expected_concern_quad = CONCERN_QUADS_BY_DOMAIN.get(domain)
            if (expected_concern_quad is not None
                    and tp.concern_pick.quad_id
                    != expected_concern_quad.id):
                out.append(DramaticaObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="concern_pick_wrong_quad",
                    target_id=tp.concern_pick.id,
                    message=(
                        f"Concern pick {tp.concern_pick.id!r} "
                        f"references quad {tp.concern_pick.quad_id!r}"
                        f" but Throughline {tl_id!r}'s Domain "
                        f"{domain.value!r} expects Concern Quad "
                        f"{expected_concern_quad.id!r}"
                    ),
                ))

        # Check Issue pick's quad matches chosen Concern's Issue Quad.
        concern_label = None
        if domain is not None:
            cq = CONCERN_QUADS_BY_DOMAIN.get(domain)
            if cq is not None:
                concern_label = cq.element_at(
                    tp.concern_pick.chosen_position,
                )
        if concern_label is not None:
            expected_issue_quad = ISSUE_QUADS_BY_CONCERN.get(
                concern_label,
            )
            if (expected_issue_quad is not None
                    and tp.issue_pick.quad_id
                    != expected_issue_quad.id):
                out.append(DramaticaObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="issue_pick_wrong_quad",
                    target_id=tp.issue_pick.id,
                    message=(
                        f"Issue pick {tp.issue_pick.id!r} references "
                        f"quad {tp.issue_pick.quad_id!r} but Concern "
                        f"{concern_label!r} expects Issue Quad "
                        f"{expected_issue_quad.id!r}"
                    ),
                ))

        # Check Problem pick's quad matches chosen Issue's Element Quad.
        issue_label = None
        if concern_label is not None:
            iq = ISSUE_QUADS_BY_CONCERN.get(concern_label)
            if iq is not None:
                issue_label = iq.element_at(
                    tp.issue_pick.chosen_position,
                )
        if issue_label is not None:
            expected_element_quad = ELEMENT_QUADS_BY_ISSUE.get(
                issue_label,
            )
            if (expected_element_quad is not None
                    and tp.problem_pick.quad_id
                    != expected_element_quad.id):
                out.append(DramaticaObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="problem_pick_wrong_quad",
                    target_id=tp.problem_pick.id,
                    message=(
                        f"Problem pick {tp.problem_pick.id!r} "
                        f"references quad "
                        f"{tp.problem_pick.quad_id!r} but Issue "
                        f"{issue_label!r} expects Element Quad "
                        f"{expected_element_quad.id!r}"
                    ),
                ))

        # Check derivation overrides agree.
        problem_quad_id = tp.problem_pick.quad_id
        # Find the quad in shipped data or registries.
        problem_quad = None
        for q in ALL_SHIPPED_QUADS:
            if q.id == problem_quad_id:
                problem_quad = q
                break
        if problem_quad is None:
            for q in ELEMENT_QUADS_BY_ISSUE.values():
                if q.id == problem_quad_id:
                    problem_quad = q
                    break

        if problem_quad is not None:
            derived = derive_from_problem(tp.problem_pick, problem_quad)
            for field_name, override in [
                ("solution", tp.solution_override),
                ("symptom", tp.symptom_override),
                ("response", tp.response_override),
            ]:
                if override is not None:
                    _, derived_label = derived[field_name]
                    if override != derived_label:
                        out.append(DramaticaObservation(
                            severity=SEVERITY_ADVISES_REVIEW,
                            code=f"{field_name}_override_mismatch",
                            target_id=tp.problem_pick.id,
                            message=(
                                f"Explicit {field_name} "
                                f"{override!r} does not match "
                                f"derived {field_name} "
                                f"{derived_label!r} from Problem "
                                f"pick at position "
                                f"{tp.problem_pick.chosen_position.value}"
                                f" in quad "
                                f"{problem_quad_id!r}"
                            ),
                        ))
    return out


def verify_thematic_picks(
    picks_list: tuple = (),
    domain_assignments: tuple = (),
) -> list:
    """Run pick-chain and derivation checks. Composes with
    verify_dramatica_complete and verify_character_elements —
    call all three."""
    return _check_pick_chain(picks_list, domain_assignments)


def verify_character_elements(
    assignments: tuple = (),
    characters: tuple = (),
) -> list:
    """Run Character Element checks. Returns a list of
    DramaticaObservation records. Composes with
    verify_dramatica_complete — call both."""
    out: list = []
    out.extend(_check_character_element_uniqueness(assignments))
    out.extend(_check_archetype_element_conformance(
        assignments, characters,
    ))
    return out
