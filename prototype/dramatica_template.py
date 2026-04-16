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

# ============================================================================
# Issue / Element Quad registries
# ============================================================================
#
# These registries map Concern-label → Issue Quad and Issue-label →
# Element Quad. They're populated below with shipped theory data.

# Issue Quad registry: maps Concern-label → Issue Quad.
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


# ============================================================================
# Issue Quads — Variations under each Concern (Type)
# ============================================================================
#
# Dramatica ships canonical Variation labels for each Concern (Type)
# in each Domain. 4 Domains × 4 Concerns × 4 Variations = 64 total.
#
# Source: Dramatica Table of Story Elements (Screenplay Systems,
# 1995/1999). Quad position assignments (A/B/C/D) follow the chart's
# spatial layout: A=top-left, B=top-right, C=bottom-left,
# D=bottom-right.

# -- Activity (Physics) Domain --

ISSUE_QUAD_UNDERSTANDING = Quad(
    id="issue_understanding",
    kind="issue-quad",
    element_A="instinct",
    element_B="senses",
    element_C="interpretation",
    element_D="conditioning",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_DOING = Quad(
    id="issue_doing",
    kind="issue-quad",
    element_A="wisdom",
    element_B="skill",
    element_C="enlightenment",
    element_D="experience",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_OBTAINING = Quad(
    id="issue_obtaining",
    kind="issue-quad",
    element_A="approach",
    element_B="self-interest",
    element_C="morality",
    element_D="attitude",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_LEARNING = Quad(
    id="issue_learning",
    kind="issue-quad",
    element_A="prerequisites",
    element_B="strategy",
    element_C="analysis",
    element_D="preconditions",
    authored_by="dramatica-theory",
)

# -- Situation (Universe) Domain --

ISSUE_QUAD_THE_PAST = Quad(
    id="issue_the-past",
    kind="issue-quad",
    element_A="fate",
    element_B="prediction",
    element_C="interdiction",
    element_D="destiny",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_HOW_THINGS_ARE_CHANGING = Quad(
    id="issue_how-things-are-changing",
    kind="issue-quad",
    element_A="fact",
    element_B="security",
    element_C="threat",
    element_D="fantasy",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_THE_FUTURE = Quad(
    id="issue_the-future",
    kind="issue-quad",
    element_A="openness",
    element_B="delay",
    element_C="choice",
    element_D="preconception",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_THE_PRESENT = Quad(
    id="issue_the-present",
    kind="issue-quad",
    element_A="work",
    element_B="attract",
    element_C="repel",
    element_D="attempt",
    authored_by="dramatica-theory",
)

# -- Manipulation (Psychology) Domain --

ISSUE_QUAD_DEVELOPING_A_PLAN = Quad(
    id="issue_developing-a-plan",
    kind="issue-quad",
    element_A="state-of-being",
    element_B="situation",
    element_C="circumstances",
    element_D="sense-of-self",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_PLAYING_A_ROLE = Quad(
    id="issue_playing-a-role",
    kind="issue-quad",
    element_A="knowledge",
    element_B="ability",
    element_C="desire",
    element_D="thought",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_CHANGING_ONES_NATURE = Quad(
    id="issue_changing-ones-nature",
    kind="issue-quad",
    element_A="rationalization",
    element_B="obligation",
    element_C="commitment",
    element_D="responsibility",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_CONCEIVING_AN_IDEA = Quad(
    id="issue_conceiving-an-idea",
    kind="issue-quad",
    element_A="permission",
    element_B="need",
    element_C="expediency",
    element_D="deficiency",
    authored_by="dramatica-theory",
)

# -- Fixed Attitude (Mind) Domain --

ISSUE_QUAD_MEMORIES = Quad(
    id="issue_memories",
    kind="issue-quad",
    element_A="truth",
    element_B="evidence",
    element_C="suspicion",
    element_D="falsehood",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_IMPULSIVE_RESPONSES = Quad(
    id="issue_impulsive-responses",
    kind="issue-quad",
    element_A="value",
    element_B="confidence",
    element_C="worry",
    element_D="worth",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_INNERMOST_DESIRES = Quad(
    id="issue_innermost-desires",
    kind="issue-quad",
    element_A="closure",
    element_B="hope",
    element_C="dream",
    element_D="denial",
    authored_by="dramatica-theory",
)

ISSUE_QUAD_CONTEMPLATION = Quad(
    id="issue_contemplation",
    kind="issue-quad",
    element_A="investigation",
    element_B="appraisal",
    element_C="reappraisal",
    element_D="doubt",
    authored_by="dramatica-theory",
)

# -- Register all Issue Quads --

_ALL_ISSUE_QUADS = (
    # Activity
    (CONCERN_ACTIVITY_QUAD, (
        ISSUE_QUAD_UNDERSTANDING,
        ISSUE_QUAD_DOING,
        ISSUE_QUAD_OBTAINING,
        ISSUE_QUAD_LEARNING,
    )),
    # Situation
    (CONCERN_SITUATION_QUAD, (
        ISSUE_QUAD_THE_PAST,
        ISSUE_QUAD_HOW_THINGS_ARE_CHANGING,
        ISSUE_QUAD_THE_FUTURE,
        ISSUE_QUAD_THE_PRESENT,
    )),
    # Manipulation
    (CONCERN_MANIPULATION_QUAD, (
        ISSUE_QUAD_DEVELOPING_A_PLAN,
        ISSUE_QUAD_PLAYING_A_ROLE,
        ISSUE_QUAD_CHANGING_ONES_NATURE,
        ISSUE_QUAD_CONCEIVING_AN_IDEA,
    )),
    # Fixed Attitude (A=innermost-desires, B=impulsive-responses,
    #                  C=contemplation, D=memories)
    (CONCERN_FIXED_ATTITUDE_QUAD, (
        ISSUE_QUAD_INNERMOST_DESIRES,
        ISSUE_QUAD_IMPULSIVE_RESPONSES,
        ISSUE_QUAD_CONTEMPLATION,
        ISSUE_QUAD_MEMORIES,
    )),
)

for _cq, _iquads in _ALL_ISSUE_QUADS:
    for _iq in _iquads:
        # The concern label is the element in the Concern Quad whose
        # position matches the Issue Quad's position in the list.
        _concern_label = {
            0: _cq.element_A, 1: _cq.element_B,
            2: _cq.element_C, 3: _cq.element_D,
        }[_iquads.index(_iq)]
        register_issue_quad(_concern_label, _iq)


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
# Dramatica has four character element dimensions (Motivation,
# Methodology, Evaluation, Purpose — 16 each, 64 total). Each
# archetype gets a companion pair from one quad per dimension.
# All four dimensions follow the same structural pattern.
#
# Source: Dramatica Weekend Workshop Syllabus (storymind.com),
# cross-referenced with the Lost Theory Book. The Lost Theory Book
# notes that the Methodology/Evaluation/Purpose material was "never
# fully developed" — the element labels are consistent across both
# sources, but canonical verification against the Dramatica software
# is advised.


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


# --------------------------------------------------------------------
# Methodology Elements — how characters approach problems
# --------------------------------------------------------------------

class MethodologyElement(str, Enum):
    """The 16 Methodology Elements from Dramatica theory. Arranged as
    the methodology quad of quads:

    Protagonist quad:   Proaction / Certainty
    Antagonist quad:    Reaction / Potentiality
    Reason quad:        Inaction / Probability
    Emotion quad:       Protection / Possibility
    Sidekick quad:      Deduction / Acceptance
    Skeptic quad:       Induction / Non-Acceptance
    Guardian quad:      Reduction / Evaluation
    Contagonist quad:   Production / Re-evaluation
    """
    PROACTION = "proaction"
    CERTAINTY = "certainty"
    REACTION = "reaction"
    POTENTIALITY = "potentiality"
    INACTION = "inaction"
    PROBABILITY = "probability"
    PROTECTION = "protection"
    POSSIBILITY = "possibility"
    DEDUCTION = "deduction"
    ACCEPTANCE = "acceptance"
    INDUCTION = "induction"
    NON_ACCEPTANCE = "non-acceptance"
    REDUCTION = "reduction"
    EVALUATION = "evaluation"
    PRODUCTION = "production"
    RE_EVALUATION = "re-evaluation"


ARCHETYPE_METHODOLOGY_ELEMENTS: dict = {
    "Protagonist": (MethodologyElement.PROACTION, MethodologyElement.CERTAINTY),
    "Antagonist": (MethodologyElement.REACTION, MethodologyElement.POTENTIALITY),
    "Reason": (MethodologyElement.INACTION, MethodologyElement.PROBABILITY),
    "Emotion": (MethodologyElement.PROTECTION, MethodologyElement.POSSIBILITY),
    "Sidekick": (MethodologyElement.DEDUCTION, MethodologyElement.ACCEPTANCE),
    "Skeptic": (MethodologyElement.INDUCTION, MethodologyElement.NON_ACCEPTANCE),
    "Guardian": (MethodologyElement.REDUCTION, MethodologyElement.EVALUATION),
    "Contagonist": (MethodologyElement.PRODUCTION, MethodologyElement.RE_EVALUATION),
}

METHODOLOGY_QUAD_APPROACH = Quad(
    id="methodology_quad_approach",
    kind="methodology-quad",
    element_A="proaction",       # Protagonist's initiative
    element_B="certainty",       # Protagonist's conviction
    element_C="reaction",        # Antagonist's responsiveness
    element_D="potentiality",    # Antagonist's openness
    authored_by="dramatica-theory",
)

METHODOLOGY_QUAD_ATTITUDE = Quad(
    id="methodology_quad_attitude",
    kind="methodology-quad",
    element_A="inaction",        # Reason's restraint
    element_B="probability",     # Reason's likelihood assessment
    element_C="protection",      # Emotion's defensiveness
    element_D="possibility",     # Emotion's openness to chance
    authored_by="dramatica-theory",
)

METHODOLOGY_QUAD_REASONING = Quad(
    id="methodology_quad_reasoning",
    kind="methodology-quad",
    element_A="deduction",       # Sidekick's logical derivation
    element_B="acceptance",      # Sidekick's willingness
    element_C="induction",       # Skeptic's empirical inference
    element_D="non-acceptance",  # Skeptic's refusal
    authored_by="dramatica-theory",
)

METHODOLOGY_QUAD_PROCESS = Quad(
    id="methodology_quad_process",
    kind="methodology-quad",
    element_A="reduction",       # Guardian's simplification
    element_B="evaluation",      # Guardian's assessment
    element_C="production",      # Contagonist's generation
    element_D="re-evaluation",   # Contagonist's reassessment
    authored_by="dramatica-theory",
)

ALL_METHODOLOGY_QUADS = (
    METHODOLOGY_QUAD_APPROACH,
    METHODOLOGY_QUAD_ATTITUDE,
    METHODOLOGY_QUAD_REASONING,
    METHODOLOGY_QUAD_PROCESS,
)


# --------------------------------------------------------------------
# Evaluation Elements — how characters measure progress
# --------------------------------------------------------------------

class EvaluationElement(str, Enum):
    """The 16 Evaluation (Means of Evaluation) Elements from
    Dramatica theory. Arranged as the evaluation quad of quads:

    Protagonist quad:   Effect / Proven
    Antagonist quad:    Cause / Unproven
    Reason quad:        Trust / Theory
    Emotion quad:       Test / Hunch
    Sidekick quad:      Result / Accurate
    Skeptic quad:       Process / Non-Accurate
    Guardian quad:      Ending / Expectation
    Contagonist quad:   Unending / Determination
    """
    EFFECT = "effect"
    PROVEN = "proven"
    CAUSE = "cause"
    UNPROVEN = "unproven"
    TRUST = "trust"
    THEORY = "theory"
    TEST = "test"
    HUNCH = "hunch"
    RESULT = "result"
    ACCURATE = "accurate"
    PROCESS = "process"
    NON_ACCURATE = "non-accurate"
    ENDING = "ending"
    EXPECTATION = "expectation"
    UNENDING = "unending"
    DETERMINATION = "determination"


ARCHETYPE_EVALUATION_ELEMENTS: dict = {
    "Protagonist": (EvaluationElement.EFFECT, EvaluationElement.PROVEN),
    "Antagonist": (EvaluationElement.CAUSE, EvaluationElement.UNPROVEN),
    "Reason": (EvaluationElement.TRUST, EvaluationElement.THEORY),
    "Emotion": (EvaluationElement.TEST, EvaluationElement.HUNCH),
    "Sidekick": (EvaluationElement.RESULT, EvaluationElement.ACCURATE),
    "Skeptic": (EvaluationElement.PROCESS, EvaluationElement.NON_ACCURATE),
    "Guardian": (EvaluationElement.ENDING, EvaluationElement.EXPECTATION),
    "Contagonist": (EvaluationElement.UNENDING, EvaluationElement.DETERMINATION),
}

EVALUATION_QUAD_EVIDENCE = Quad(
    id="evaluation_quad_evidence",
    kind="evaluation-quad",
    element_A="effect",          # Protagonist's impact measure
    element_B="proven",          # Protagonist's verification
    element_C="cause",           # Antagonist's origin measure
    element_D="unproven",        # Antagonist's doubt
    authored_by="dramatica-theory",
)

EVALUATION_QUAD_JUDGMENT = Quad(
    id="evaluation_quad_judgment",
    kind="evaluation-quad",
    element_A="trust",           # Reason's confidence
    element_B="theory",          # Reason's framework
    element_C="test",            # Emotion's trial
    element_D="hunch",           # Emotion's intuition
    authored_by="dramatica-theory",
)

EVALUATION_QUAD_MEASUREMENT = Quad(
    id="evaluation_quad_measurement",
    kind="evaluation-quad",
    element_A="result",          # Sidekick's outcome
    element_B="accurate",        # Sidekick's precision
    element_C="process",         # Skeptic's means
    element_D="non-accurate",    # Skeptic's imprecision
    authored_by="dramatica-theory",
)

EVALUATION_QUAD_EXPECTATION = Quad(
    id="evaluation_quad_expectation",
    kind="evaluation-quad",
    element_A="ending",          # Guardian's terminus
    element_B="expectation",     # Guardian's anticipation
    element_C="unending",        # Contagonist's perpetuation
    element_D="determination",   # Contagonist's resolve
    authored_by="dramatica-theory",
)

ALL_EVALUATION_QUADS = (
    EVALUATION_QUAD_EVIDENCE,
    EVALUATION_QUAD_JUDGMENT,
    EVALUATION_QUAD_MEASUREMENT,
    EVALUATION_QUAD_EXPECTATION,
)


# --------------------------------------------------------------------
# Purpose Elements — what characters seek to achieve
# --------------------------------------------------------------------

class PurposeElement(str, Enum):
    """The 16 Purpose Elements from Dramatica theory. Arranged as
    the purpose quad of quads:

    Protagonist quad:   Knowledge / Actuality
    Antagonist quad:    Thought / Perception
    Reason quad:        Ability / Aware
    Emotion quad:       Desire / Self-Aware
    Sidekick quad:      Order / Inertia
    Skeptic quad:       Chaos / Change
    Guardian quad:      Equity / Projection
    Contagonist quad:   Inequity / Speculation
    """
    KNOWLEDGE = "knowledge"
    ACTUALITY = "actuality"
    THOUGHT = "thought"
    PERCEPTION = "perception"
    ABILITY = "ability"
    AWARE = "aware"
    DESIRE = "desire"
    SELF_AWARE = "self-aware"
    ORDER = "order"
    INERTIA = "inertia"
    CHAOS = "chaos"
    CHANGE = "change"
    EQUITY = "equity"
    PROJECTION = "projection"
    INEQUITY = "inequity"
    SPECULATION = "speculation"


ARCHETYPE_PURPOSE_ELEMENTS: dict = {
    "Protagonist": (PurposeElement.KNOWLEDGE, PurposeElement.ACTUALITY),
    "Antagonist": (PurposeElement.THOUGHT, PurposeElement.PERCEPTION),
    "Reason": (PurposeElement.ABILITY, PurposeElement.AWARE),
    "Emotion": (PurposeElement.DESIRE, PurposeElement.SELF_AWARE),
    "Sidekick": (PurposeElement.ORDER, PurposeElement.INERTIA),
    "Skeptic": (PurposeElement.CHAOS, PurposeElement.CHANGE),
    "Guardian": (PurposeElement.EQUITY, PurposeElement.PROJECTION),
    "Contagonist": (PurposeElement.INEQUITY, PurposeElement.SPECULATION),
}

PURPOSE_QUAD_KNOWLEDGE = Quad(
    id="purpose_quad_knowledge",
    kind="purpose-quad",
    element_A="knowledge",       # Protagonist's information goal
    element_B="actuality",       # Protagonist's reality goal
    element_C="thought",         # Antagonist's contemplation goal
    element_D="perception",      # Antagonist's viewpoint goal
    authored_by="dramatica-theory",
)

PURPOSE_QUAD_ABILITY = Quad(
    id="purpose_quad_ability",
    kind="purpose-quad",
    element_A="ability",         # Reason's capability goal
    element_B="aware",           # Reason's awareness goal
    element_C="desire",          # Emotion's want
    element_D="self-aware",      # Emotion's introspection goal
    authored_by="dramatica-theory",
)

PURPOSE_QUAD_ORDER = Quad(
    id="purpose_quad_order",
    kind="purpose-quad",
    element_A="order",           # Sidekick's stability goal
    element_B="inertia",         # Sidekick's continuity goal
    element_C="chaos",           # Skeptic's disruption goal
    element_D="change",          # Skeptic's transformation goal
    authored_by="dramatica-theory",
)

PURPOSE_QUAD_EQUITY = Quad(
    id="purpose_quad_equity",
    kind="purpose-quad",
    element_A="equity",          # Guardian's fairness goal
    element_B="projection",     # Guardian's foresight goal
    element_C="inequity",       # Contagonist's imbalance goal
    element_D="speculation",    # Contagonist's conjecture goal
    authored_by="dramatica-theory",
)

ALL_PURPOSE_QUADS = (
    PURPOSE_QUAD_KNOWLEDGE,
    PURPOSE_QUAD_ABILITY,
    PURPOSE_QUAD_ORDER,
    PURPOSE_QUAD_EQUITY,
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


@dataclass(frozen=True)
class MethodologyElementAssignment:
    """Assigns a Methodology Element to a Character."""
    id: str
    character_id: str
    element: MethodologyElement
    authored_by: str = "author"


@dataclass(frozen=True)
class EvaluationElementAssignment:
    """Assigns an Evaluation Element to a Character."""
    id: str
    character_id: str
    element: EvaluationElement
    authored_by: str = "author"


@dataclass(frozen=True)
class PurposeElementAssignment:
    """Assigns a Purpose Element to a Character."""
    id: str
    character_id: str
    element: PurposeElement
    authored_by: str = "author"


def _check_element_uniqueness(
    assignments: tuple,
    dimension_name: str,
) -> list:
    """Each element within a dimension may appear on at most one
    character. Duplicates are Dramatica's hardest character-level
    rule. Works for any dimension (Motivation, Methodology,
    Evaluation, Purpose)."""
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
                    f"{dimension_name} Element {element.value!r} is "
                    f"assigned to {len(chars)} characters: "
                    f"{chars}. Dramatica requires each element on "
                    f"exactly one character."
                ),
            ))
    return out


def _check_archetype_conformance(
    assignments: tuple,
    characters: tuple,
    archetype_elements: dict,
    dimension_name: str,
) -> list:
    """If a character carries an archetype function label AND has
    element assignments, check whether the assignments match the
    archetype's canonical elements. Divergence is an observation,
    not an error (complex characters diverge intentionally).
    Works for any dimension."""
    out = []
    by_char: dict = {}
    for a in assignments:
        by_char.setdefault(a.character_id, set()).add(a.element)
    for char in characters:
        if not hasattr(char, "function_labels"):
            continue
        for fn in char.function_labels:
            if fn not in archetype_elements:
                continue
            canonical = set(archetype_elements[fn])
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
                        f"{fn!r} whose canonical {dimension_name} "
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
# Issue Quads are shipped as canonical theory data above; Element
# Quads are registered by encodings as needed (256 total — deferred
# until pressured by a third encoding).


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
    methodology_assignments: tuple = (),
    evaluation_assignments: tuple = (),
    purpose_assignments: tuple = (),
    characters: tuple = (),
) -> list:
    """Run Character Element checks across all four dimensions.
    Returns a list of DramaticaObservation records. Composes with
    verify_dramatica_complete — call both.

    The ``assignments`` parameter carries Motivation assignments
    (backward-compatible name)."""
    out: list = []
    dimensions = (
        (assignments, ARCHETYPE_MOTIVATION_ELEMENTS, "Motivation"),
        (methodology_assignments, ARCHETYPE_METHODOLOGY_ELEMENTS,
         "Methodology"),
        (evaluation_assignments, ARCHETYPE_EVALUATION_ELEMENTS,
         "Evaluation"),
        (purpose_assignments, ARCHETYPE_PURPOSE_ELEMENTS, "Purpose"),
    )
    for dim_assignments, archetype_map, dim_name in dimensions:
        if not dim_assignments:
            continue
        out.extend(_check_element_uniqueness(
            dim_assignments, dim_name,
        ))
        out.extend(_check_archetype_conformance(
            dim_assignments, characters, archetype_map, dim_name,
        ))
    return out


# ============================================================================
# Per-record-type coupling-kind declarations (verification-sketch-01 V5)
# ============================================================================
#
# Parallels dramatic.py's COUPLING_DECLARATIONS but covers the record
# types and Story-level fields the dramatica-complete Template adds.
# Imports the coupling-kind constants and CouplingDeclaration shape
# from dramatic.py so the Template extends rather than duplicates the
# dialect's declaration surface.
#
# The finding worth naming: **no Realization couplings appear at the
# Template layer.** Realization couplings (Story, Character, Throughline
# owners, Scene advances) are declared at the Dramatic dialect level.
# Template records classify or claim against substrate — they do not
# introduce new record-is-made-true-by-specific-lower-records bindings.
# This means authoring Lowerings for dramatica-complete encodings
# reduces to authoring them for the underlying Dramatic encoding
# (which *_lowerings.py already does for Oedipus and Macbeth). The
# Template's new coupling work lives entirely in the verifier surface.
#
# DynamicStoryPoint is a special case: its coupling kind depends on
# which axis the record is keyed to (Resolve, Growth, Approach, Limit,
# Outcome, Judgment). The record-level declaration below uses
# claim-trajectory as a broad-modal default (three of six axes); the
# authoritative per-axis mapping is DSP_COUPLING_KIND_BY_AXIS, and
# `dsp_coupling_kind(dsp)` dispatches correctly per record.

from dramatic import (
    CouplingDeclaration,
    COUPLING_REALIZATION,
    COUPLING_CHARACTERIZATION,
    COUPLING_CLAIM_MOMENT,
    COUPLING_CLAIM_TRAJECTORY,
    COUPLING_FLAVOR,
)


TEMPLATE_COUPLING_DECLARATIONS = (
    # Story-level Template extensions. story_goal is a claim-trajectory
    # about what the OS Throughline works toward across the narrative;
    # story_consequence is a claim-moment about substrate state at the
    # point the goal lands (or doesn't). These fields aren't on the
    # Dramatic `Story` dataclass — Template passes them to verifiers
    # as separate strings — but the coupling declaration treats them
    # as Story-conceptual extensions so a verifier asking
    # `coupling_kind_for("Story", "story_goal")` gets the right answer.
    CouplingDeclaration("Story", "story_goal", COUPLING_CLAIM_TRAJECTORY),
    CouplingDeclaration("Story", "story_consequence", COUPLING_CLAIM_MOMENT),

    # DomainAssignment — a Throughline placed in a Domain classifies
    # the substrate pattern the Throughline exhibits across its events
    # (Activity → external-action-saturated; Situation → state/setting
    # saturated; Fixed Attitude → attitude-saturated; Manipulation →
    # influence/scheme-saturated). Characterization.
    CouplingDeclaration("DomainAssignment", None,
                        COUPLING_CHARACTERIZATION),

    # DynamicStoryPoint — see DSP_COUPLING_KIND_BY_AXIS for the
    # authoritative per-axis mapping. The record-level declaration is
    # claim-trajectory as a modal default; `dsp_coupling_kind(dsp)`
    # is the correct dispatch.
    CouplingDeclaration("DynamicStoryPoint", None,
                        COUPLING_CLAIM_TRAJECTORY),

    # Signpost — at narrative position N, the Throughline is "at" a
    # Concern. The claim is that substrate events at that position
    # exhibit the named Concern's pattern. Claim-moment (scoped to a
    # specific narrative position).
    CouplingDeclaration("Signpost", None, COUPLING_CLAIM_MOMENT),

    # Character Element assignments across all four dimensions —
    # claim-trajectory: the character exhibits the element pair
    # across their arc (Protagonist pursues goals and considers
    # actions across the narrative; Antagonist avoids and reconsiders;
    # etc.). Each of the four dimensions (Motivation, Methodology,
    # Evaluation, Purpose) gets the same coupling kind.
    CouplingDeclaration("CharacterElementAssignment", None,
                        COUPLING_CLAIM_TRAJECTORY),
    CouplingDeclaration("MethodologyElementAssignment", None,
                        COUPLING_CLAIM_TRAJECTORY),
    CouplingDeclaration("EvaluationElementAssignment", None,
                        COUPLING_CLAIM_TRAJECTORY),
    CouplingDeclaration("PurposeElementAssignment", None,
                        COUPLING_CLAIM_TRAJECTORY),

    # ThematicPicks fields. concern_pick and issue_pick classify what
    # the Throughline is about (characterization). problem_pick and
    # the three derived fields (solution / symptom / response) are
    # claim-trajectory — what's driving / resolving / manifesting /
    # responding-to the trouble across the Throughline's arc.
    CouplingDeclaration("ThematicPicks", "concern_pick",
                        COUPLING_CHARACTERIZATION),
    CouplingDeclaration("ThematicPicks", "issue_pick",
                        COUPLING_CHARACTERIZATION),
    CouplingDeclaration("ThematicPicks", "problem_pick",
                        COUPLING_CLAIM_TRAJECTORY),
    CouplingDeclaration("ThematicPicks", "solution_override",
                        COUPLING_CLAIM_TRAJECTORY),
    CouplingDeclaration("ThematicPicks", "symptom_override",
                        COUPLING_CLAIM_TRAJECTORY),
    CouplingDeclaration("ThematicPicks", "response_override",
                        COUPLING_CLAIM_TRAJECTORY),

    # Quad / QuadPick — theory-data constructs. No direct substrate
    # coupling; they exist within the Template for authoring and
    # validation. Flavor.
    CouplingDeclaration("Quad", None, COUPLING_FLAVOR),
    CouplingDeclaration("QuadPick", None, COUPLING_FLAVOR),
)


# Per-axis coupling kind for DynamicStoryPoint. Authoritative over
# the record-level declaration above.
DSP_COUPLING_KIND_BY_AXIS = {
    DSPAxis.RESOLVE:   COUPLING_CLAIM_TRAJECTORY,  # MC changes vs. not across arc
    DSPAxis.GROWTH:    COUPLING_CLAIM_TRAJECTORY,  # MC adopts/stops a trait across arc
    DSPAxis.APPROACH:  COUPLING_CHARACTERIZATION,  # substrate events classify as Do-er/Be-er
    DSPAxis.LIMIT:     COUPLING_CHARACTERIZATION,  # substrate pressure shape classifies
    DSPAxis.OUTCOME:   COUPLING_CLAIM_MOMENT,      # at τ_s end: goal achieved or not
    DSPAxis.JUDGMENT:  COUPLING_CLAIM_TRAJECTORY,  # MC's internal resolution across arc
}


def dsp_coupling_kind(dsp: DynamicStoryPoint) -> str:
    """Return the authoritative coupling kind for a DSP record,
    dispatching on its axis. Prefer this over
    `template_coupling_kind_for("DynamicStoryPoint", None)` for DSPs
    because the record-level declaration is only a modal default."""
    return DSP_COUPLING_KIND_BY_AXIS[dsp.axis]


def template_coupling_kind_for(
    record_type: str,
    field: Optional[str] = None,
) -> Optional[str]:
    """Look up the coupling kind for a (record_type, field) pair among
    the Template declarations. Returns None if no Template declaration
    applies; callers that want the combined Dramatic+Template lookup
    should fall back to dramatic.coupling_kind_for after this returns
    None. Same field-level-wins-over-record-level precedence as
    dramatic.coupling_kind_for."""
    for d in TEMPLATE_COUPLING_DECLARATIONS:
        if d.record_type == record_type and d.field == field:
            return d.kind
    if field is not None:
        for d in TEMPLATE_COUPLING_DECLARATIONS:
            if d.record_type == record_type and d.field is None:
                return d.kind
    return None


def template_fields_with_coupling(
    record_type: str,
    kind: str,
) -> tuple:
    """Return the field names of `record_type` that carry coupling
    kind `kind` among the Template declarations."""
    return tuple(
        d.field for d in TEMPLATE_COUPLING_DECLARATIONS
        if d.record_type == record_type and d.kind == kind
    )
