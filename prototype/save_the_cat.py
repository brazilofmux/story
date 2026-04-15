"""
save_the_cat.py — Save the Cat narrative dialect (per save-the-cat-
sketch-01).

Second upper-dialect under architecture-sketch-02's stack, after
dramatic.py. Written on the dialect's own terms; no substrate or
Dramatic vocabulary is reached for. Connective machinery (Lowerings,
cross-boundary verifiers) is architecture-sketch-02's concern and lives
in companion modules per the existing pattern.

Save the Cat (Blake Snyder, 2005) is a beat-driven framework: every
commercial story has 15 specific beats in a specific order at specific
proportional positions. Compared to dramatic.py, this dialect is
prescriptive where Dramatic is parameterized, beat-driven where
Dramatic is role-driven, and page-positioned where Dramatic uses
abstract narrative_position.

Per save-the-cat-sketch-01 commitments:
- S1: 15 canonical beat slots, fixed names and order.
- S2: page targets are the dialect's positional coordinate.
- S3: A and B Story strands as first-class.
- S4: theme statement at Story level (the Theme Stated beat's content).
- S5: Genre as a Template-shaped record (10 genres ship as data).
- S6: Self-verifier within Save the Cat vocabulary; flags only via
      observation, never errors.
- S7: Description surface inherited (matches future Dramatic-side state).
- S8: Connective relations to other dialects out of scope here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple


# ============================================================================
# Strand kinds (S3)
# ============================================================================


class StrandKind(str, Enum):
    """Two strand kinds per Snyder. A story = external plot; B story =
    internal/relationship arc that embodies the theme."""
    A_STORY = "a-story"
    B_STORY = "b-story"


# ============================================================================
# The 15 canonical beat slots (S1, S2)
# ============================================================================
#
# Snyder's beat sheet, with target page numbers on a 110-page screenplay.
# Range-beats (Set-Up, Debate, Fun and Games, Bad Guys Close In, Dark
# Night, Finale) carry the start of the conventional range as
# `page_target`; point-beats (Catalyst, Break Into Two, Midpoint, etc.)
# carry the canonical point.
#
# `purpose` is a one-line description of what the beat does in Snyder's
# framework. It's what the encoding's authored beat is *trying to be*;
# the encoding's beat content describes how it lands.


@dataclass(frozen=True)
class StcCanonicalBeat:
    """One of the 15 fixed beats Save the Cat asserts every commercial
    story has. The dialect carries the canonical sheet as data; an
    authored encoding fills each slot with its own StcBeat record."""
    slot: int                # 1..15
    name: str
    page_target: int         # canonical page on a 110-page screenplay
    purpose: str


CANONICAL_BEATS: Tuple[StcCanonicalBeat, ...] = (
    StcCanonicalBeat(
        slot=1, name="Opening Image", page_target=1,
        purpose=("the first impression: tone, mood, the world before "
                 "the story disturbs it; mirrors the Final Image"),
    ),
    StcCanonicalBeat(
        slot=2, name="Theme Stated", page_target=5,
        purpose=("the story's thematic claim, usually spoken by a "
                 "non-protagonist character; the protagonist won't "
                 "fully understand it until the end"),
    ),
    StcCanonicalBeat(
        slot=3, name="Set-Up", page_target=1,
        purpose=("the protagonist's status quo and what's wrong with "
                 "it; introduces what needs fixing in the protagonist's "
                 "world and inner life"),
    ),
    StcCanonicalBeat(
        slot=4, name="Catalyst", page_target=12,
        purpose=("the inciting incident; the message, knock at the "
                 "door, news that disrupts the status quo"),
    ),
    StcCanonicalBeat(
        slot=5, name="Debate", page_target=12,
        purpose=("the protagonist's resistance: should I do this? "
                 "rendered as concrete dramatic question, not "
                 "internal monologue"),
    ),
    StcCanonicalBeat(
        slot=6, name="Break Into Two", page_target=25,
        purpose=("the protagonist's choice; they cross the threshold "
                 "into the new world / situation"),
    ),
    StcCanonicalBeat(
        slot=7, name="B Story", page_target=30,
        purpose=("the introduction of the B story (often the love "
                 "interest or a relationship that will carry the "
                 "theme); arrives just after the threshold crossing"),
    ),
    StcCanonicalBeat(
        slot=8, name="Fun and Games", page_target=30,
        purpose=("the promise of the premise; the sequence the trailer "
                 "is built from; the protagonist navigating the new "
                 "world without yet fully bearing its costs"),
    ),
    StcCanonicalBeat(
        slot=9, name="Midpoint", page_target=55,
        purpose=("a false victory or false defeat; the stakes raise "
                 "and the A and B stories collide; from here the "
                 "screws tighten"),
    ),
    StcCanonicalBeat(
        slot=10, name="Bad Guys Close In", page_target=55,
        purpose=("external pressure mounts as internal flaws compound; "
                 "the protagonist's allies and resources thin"),
    ),
    StcCanonicalBeat(
        slot=11, name="All Is Lost", page_target=75,
        purpose=("the rock bottom; the false defeat (after midpoint "
                 "victory) or the deeper pit (after midpoint defeat); "
                 "often a death — literal, professional, or symbolic"),
    ),
    StcCanonicalBeat(
        slot=12, name="Dark Night of the Soul", page_target=75,
        purpose=("the protagonist sits with the loss; the moment "
                 "before the answer arrives; despair before insight"),
    ),
    StcCanonicalBeat(
        slot=13, name="Break Into Three", page_target=85,
        purpose=("the answer is found; the protagonist commits to the "
                 "final approach with the lesson the story has taught"),
    ),
    StcCanonicalBeat(
        slot=14, name="Finale", page_target=85,
        purpose=("the climactic sequence: the protagonist applies the "
                 "lesson, the A and B stories resolve together, the "
                 "old world is dismantled or the new one secured"),
    ),
    StcCanonicalBeat(
        slot=15, name="Final Image", page_target=110,
        purpose=("the closing shot; mirrors and inverts the Opening "
                 "Image to register how the world has changed"),
    ),
)

NUM_CANONICAL_BEATS = len(CANONICAL_BEATS)
assert NUM_CANONICAL_BEATS == 15, (
    f"Save the Cat's canonical beat sheet must have 15 entries; "
    f"got {NUM_CANONICAL_BEATS}"
)

CANONICAL_BEAT_BY_SLOT = {b.slot: b for b in CANONICAL_BEATS}
CANONICAL_BEAT_NAMES = tuple(b.name for b in CANONICAL_BEATS)


# ============================================================================
# Authored records (S1, S3)
# ============================================================================


@dataclass(frozen=True)
class StrandAdvancement:
    """One strand a beat advances. A beat may advance the A story, the
    B story, both, or (rarely) neither. `note` is optional authorial
    commentary on what the advance accomplishes for that strand."""
    strand_id: str
    note: str = ""


@dataclass(frozen=True)
class StcBeat:
    """One authored beat. `slot` names which canonical beat (1..15)
    this fills. `page_actual` is where the author placed it; for
    non-screenplay encodings, this is interpreted proportionally
    against the encoding's own page count.

    Multiple StcBeats may share a slot (S1 admits this; the verifier
    surfaces it as an observation, not an error)."""
    id: str
    slot: int
    page_actual: int
    description_of_change: str = ""
    advances: tuple = ()              # tuple[StrandAdvancement, ...]
    authored_by: str = "author"

    def __post_init__(self):
        if not (1 <= self.slot <= NUM_CANONICAL_BEATS):
            raise ValueError(
                f"StcBeat {self.id!r} slot {self.slot} is out of range; "
                f"must be 1..{NUM_CANONICAL_BEATS}"
            )


@dataclass(frozen=True)
class StcStrand:
    """A or B story. Per S3, both are first-class records, and a Story
    may declare zero, one, or both. Snyder's framework strongly implies
    every story has both, but the dialect doesn't enforce that — some
    encodings (especially short-form) collapse them."""
    id: str
    kind: StrandKind
    description: str = ""
    authored_by: str = "author"


# ============================================================================
# Genre Template (S5)
# ============================================================================


@dataclass(frozen=True)
class StcGenre:
    """One of Snyder's ten genres, treated as a Template-shaped record
    parallel to dramatic.Template. A Story optionally declares a
    `stc_genre_id`; the self-verifier (S6) checks the encoding against
    the genre's archetypes if so.

    `archetypes` is a tuple of label strings naming what the genre
    requires (e.g., 'the monster', 'the house', 'the sin' for Monster
    in the House). Per-genre beat semantics are NOT carried in this
    iteration; deferred per save-the-cat-sketch-01 OQ1.
    """
    id: str
    name: str
    description: str
    archetypes: Tuple[str, ...] = ()


# Snyder's ten genres, sketched as data. Each carries the three
# canonical archetypes traditionally associated with the genre.

GENRE_MONSTER_IN_THE_HOUSE = StcGenre(
    id="monster-in-the-house",
    name="Monster in the House",
    description=("a monster (supernatural, criminal, or pathological), "
                 "in a closed environment (the house), unleashed by "
                 "the sin (someone's transgression that brought the "
                 "monster in)"),
    archetypes=("the monster", "the house", "the sin"),
)

GENRE_GOLDEN_FLEECE = StcGenre(
    id="golden-fleece",
    name="Golden Fleece",
    description=("a road trip story; the prize is rarely what the "
                 "protagonist actually needs; the journey transforms "
                 "the road crew"),
    archetypes=("the road", "the team", "the prize"),
)

GENRE_OUT_OF_THE_BOTTLE = StcGenre(
    id="out-of-the-bottle",
    name="Out of the Bottle",
    description=("magic, briefly: the protagonist gets a wish or an "
                 "ability they didn't earn; pays for it; learns what "
                 "actually mattered"),
    archetypes=("the wish", "the spell", "the lesson"),
)

GENRE_DUDE_WITH_A_PROBLEM = StcGenre(
    id="dude-with-a-problem",
    name="Dude with a Problem",
    description=("an ordinary person dropped into extraordinary "
                 "circumstances; survival rather than ambition drives "
                 "the plot"),
    archetypes=("the innocent hero", "the sudden event", "the life-or-death battle"),
)

GENRE_RITES_OF_PASSAGE = StcGenre(
    id="rites-of-passage",
    name="Rites of Passage",
    description=("the pain of a life-stage transition; coming-of-age, "
                 "midlife, dying; the struggle is internal even when "
                 "framed externally"),
    archetypes=("the life problem", "the wrong way", "the acceptance"),
)

GENRE_BUDDY_LOVE = StcGenre(
    id="buddy-love",
    name="Buddy Love",
    description=("two halves becoming one; love story or partnership; "
                 "the protagonists need each other to be whole"),
    archetypes=("the incomplete hero", "the counterpart", "the complication"),
)

GENRE_WHYDUNIT = StcGenre(
    id="whydunit",
    name="Whydunit",
    description=("not whodunit but why; the dark mystery of motivation; "
                 "the protagonist's pursuit transforms them"),
    archetypes=("the detective", "the secret", "the dark turn"),
)

GENRE_FOOL_TRIUMPHANT = StcGenre(
    id="fool-triumphant",
    name="Fool Triumphant",
    description=("the underdog who wins by being themselves; an "
                 "establishment underestimates the fool to its cost"),
    archetypes=("the fool", "the establishment", "the transformation"),
)

GENRE_INSTITUTIONALIZED = StcGenre(
    id="institutionalized",
    name="Institutionalized",
    description=("the individual versus the group; the cost of "
                 "joining, leaving, or destroying the institution"),
    archetypes=("the group", "the choice", "the sacrifice"),
)

GENRE_SUPERHERO = StcGenre(
    id="superhero",
    name="Superhero",
    description=("an extraordinary person in an ordinary world; the "
                 "burden of the gift; the cost of being special"),
    archetypes=("the special power", "the nemesis", "the curse"),
)

GENRES: Tuple[StcGenre, ...] = (
    GENRE_MONSTER_IN_THE_HOUSE,
    GENRE_GOLDEN_FLEECE,
    GENRE_OUT_OF_THE_BOTTLE,
    GENRE_DUDE_WITH_A_PROBLEM,
    GENRE_RITES_OF_PASSAGE,
    GENRE_BUDDY_LOVE,
    GENRE_WHYDUNIT,
    GENRE_FOOL_TRIUMPHANT,
    GENRE_INSTITUTIONALIZED,
    GENRE_SUPERHERO,
)

assert len(GENRES) == 10, f"Save the Cat ships ten genres; got {len(GENRES)}"

GENRE_BY_ID = {g.id: g for g in GENRES}


# ============================================================================
# Story root (S4)
# ============================================================================


@dataclass(frozen=True)
class StcStory:
    """The Save the Cat dialect's root record. Aggregates beats and
    strands by id; declares an optional genre (S5) and the canonical
    theme statement (S4).

    `theme_statement` is the literal claim the Theme Stated beat
    dramatizes; it is promoted to Story level so other tooling can
    reference it without parsing the beat content. Empty is admissible
    (the verifier surfaces it); some authors set the theme later.
    """
    id: str
    title: str
    theme_statement: str = ""
    stc_genre_id: Optional[str] = None
    beat_ids: tuple = ()       # tuple[str, ...]
    strand_ids: tuple = ()     # tuple[str, ...]
    authored_by: str = "author"


# ============================================================================
# Self-verifier (S6) — analogue to dramatic.verify
# ============================================================================


@dataclass(frozen=True)
class StcObservation:
    """One self-verifier finding from `verify`. Severity is "noted" or
    "advises-review"; code is a short stable tag the walker can group
    by."""
    severity: str
    code: str
    target_id: str
    message: str


SEVERITY_NOTED = "noted"
SEVERITY_ADVISES_REVIEW = "advises-review"


def _index(records: tuple) -> dict:
    """id → record. Trusts caller for uniqueness; duplicate ids
    surface as a separate observation."""
    return {r.id: r for r in records}


def _check_id_resolution(
    story: StcStory,
    beats_by_id: dict,
    strands_by_id: dict,
    genres_by_id: dict,
) -> list:
    """Story.beat_ids and strand_ids must resolve in their collections;
    stc_genre_id, if set, must resolve in genres_by_id."""
    out = []
    for bid in story.beat_ids:
        if bid not in beats_by_id:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="beat_id_unresolved",
                target_id=story.id,
                message=(f"Story {story.id!r} references beat_id "
                         f"{bid!r} which is not in the beats "
                         f"collection"),
            ))
    for sid in story.strand_ids:
        if sid not in strands_by_id:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="strand_id_unresolved",
                target_id=story.id,
                message=(f"Story {story.id!r} references strand_id "
                         f"{sid!r} which is not in the strands "
                         f"collection"),
            ))
    if (story.stc_genre_id is not None
            and story.stc_genre_id not in genres_by_id):
        out.append(StcObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="genre_unknown",
            target_id=story.id,
            message=(f"Story {story.id!r} declares stc_genre_id "
                     f"{story.stc_genre_id!r} which is not in the "
                     f"genres collection"),
        ))
    return out


def _check_theme_statement(story: StcStory) -> list:
    """S4: theme_statement should be set (advisory)."""
    if not story.theme_statement.strip():
        return [StcObservation(
            severity=SEVERITY_NOTED,
            code="theme_statement_empty",
            target_id=story.id,
            message=(f"Story {story.id!r} has no theme_statement; "
                     f"Save the Cat treats theme as load-bearing — the "
                     f"Theme Stated beat dramatizes a claim the story "
                     f"argues. Empty here means the claim isn't named "
                     f"yet."),
        )]
    return []


def _check_beat_slot_coverage(
    story: StcStory, beats_by_id: dict,
) -> list:
    """S1: each of the 15 canonical slots should have at least one
    authored beat. Unfilled slots are advise-review (encoding is
    incomplete); slots with multiple beats are noted (admissible per
    S1)."""
    out = []
    by_slot: dict = {}
    # Walk only beats this Story claims, not the global beats collection.
    for bid in story.beat_ids:
        if bid not in beats_by_id:
            continue  # already surfaced by _check_id_resolution
        b = beats_by_id[bid]
        by_slot.setdefault(b.slot, []).append(b)

    for slot in range(1, NUM_CANONICAL_BEATS + 1):
        if slot not in by_slot:
            canonical = CANONICAL_BEAT_BY_SLOT[slot]
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="beat_slot_unfilled",
                target_id=story.id,
                message=(f"Story {story.id!r} has no authored beat for "
                         f"slot {slot} ({canonical.name!r}); Save the "
                         f"Cat's framework expects all 15 slots "
                         f"populated"),
            ))

    for slot, slot_beats in by_slot.items():
        if len(slot_beats) > 1:
            ids = [b.id for b in slot_beats]
            canonical = CANONICAL_BEAT_BY_SLOT[slot]
            out.append(StcObservation(
                severity=SEVERITY_NOTED,
                code="multiple_beats_per_slot",
                target_id=story.id,
                message=(f"Story {story.id!r} has multiple beats in "
                         f"slot {slot} ({canonical.name!r}): {ids}. "
                         f"Admissible per S1; the slot lands across "
                         f"discrete moments rather than one"),
            ))

    return out


def _check_page_actual_monotonic(
    story: StcStory, beats_by_id: dict,
) -> list:
    """S2: page_actual values, walked in slot order, should be
    monotonically increasing. Out-of-order pages suggest either a
    misnamed slot or an unconventional structure worth flagging."""
    out = []
    beats = sorted(
        (beats_by_id[bid] for bid in story.beat_ids if bid in beats_by_id),
        key=lambda b: b.slot,
    )
    prev_page = None
    prev_id = None
    for b in beats:
        if prev_page is not None and b.page_actual < prev_page:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="page_actual_non_monotonic",
                target_id=b.id,
                message=(f"Beat {b.id!r} (slot {b.slot}) has "
                         f"page_actual={b.page_actual}, but the "
                         f"previous beat in slot order ({prev_id!r}) "
                         f"is at page {prev_page}. Pages should "
                         f"increase across the slot sequence"),
            ))
        prev_page = b.page_actual
        prev_id = b.id
    return out


def _check_strand_kinds(
    story: StcStory, strands_by_id: dict,
) -> list:
    """S3 advisory: at most one A strand and one B strand per Story.
    Multiple of either is admissible but unusual — surface as noted."""
    out = []
    a_strands = []
    b_strands = []
    for sid in story.strand_ids:
        if sid not in strands_by_id:
            continue
        s = strands_by_id[sid]
        if s.kind == StrandKind.A_STORY:
            a_strands.append(s.id)
        elif s.kind == StrandKind.B_STORY:
            b_strands.append(s.id)
    if len(a_strands) > 1:
        out.append(StcObservation(
            severity=SEVERITY_NOTED,
            code="multiple_a_strands",
            target_id=story.id,
            message=(f"Story {story.id!r} has multiple A-story "
                     f"strands: {a_strands}. Snyder's framework "
                     f"assumes one; verify intentional"),
        ))
    if len(b_strands) > 1:
        out.append(StcObservation(
            severity=SEVERITY_NOTED,
            code="multiple_b_strands",
            target_id=story.id,
            message=(f"Story {story.id!r} has multiple B-story "
                     f"strands: {b_strands}. Snyder's framework "
                     f"assumes one; verify intentional"),
        ))
    return out


def _check_advancement_strand_resolution(
    story: StcStory, beats_by_id: dict, strands_by_id: dict,
) -> list:
    """S3: every StrandAdvancement on every authored beat must
    reference a strand that exists. Unresolved strand_ids surface as
    advise-review."""
    out = []
    known = set(strands_by_id.keys())
    for bid in story.beat_ids:
        if bid not in beats_by_id:
            continue
        b = beats_by_id[bid]
        for adv in b.advances:
            if adv.strand_id not in known:
                out.append(StcObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="advancement_strand_unresolved",
                    target_id=b.id,
                    message=(f"Beat {b.id!r} advances strand "
                             f"{adv.strand_id!r} which is not in the "
                             f"strands collection"),
                ))
    return out


def _check_genre_archetypes(
    story: StcStory, genres_by_id: dict,
) -> list:
    """S5: if the Story declares a genre, the dialect surfaces the
    genre's required archetypes as a pointer for the author. The
    dialect does not check whether the encoding *contains* the
    archetypes (Save the Cat carries archetype-identification at the
    description / character level, which this dialect doesn't model
    yet — see save-the-cat-sketch-01 OQ1)."""
    out = []
    if story.stc_genre_id is None:
        return out
    if story.stc_genre_id not in genres_by_id:
        # Already surfaced by _check_id_resolution.
        return out
    genre = genres_by_id[story.stc_genre_id]
    if genre.archetypes:
        out.append(StcObservation(
            severity=SEVERITY_NOTED,
            code="genre_archetypes_declared",
            target_id=story.id,
            message=(f"Story {story.id!r} declares genre "
                     f"{genre.name!r}; the genre's archetypes are "
                     f"{list(genre.archetypes)}. Encoding-side "
                     f"archetype assignment is the author's "
                     f"responsibility in this iteration"),
        ))
    return out


def verify(
    story: StcStory,
    *,
    beats: tuple = (),
    strands: tuple = (),
    genres: tuple = GENRES,
) -> list:
    """Run all S6 self-verification checks on a Story plus its record
    bundle. Returns a list of StcObservation records.

    Per S6, no check rejects a Story; observations are advisory and
    flow to the proposal queue (in a higher layer) for author walking.
    Verification is a partner, not a gate.
    """
    beats_by_id = _index(beats)
    strands_by_id = _index(strands)
    genres_by_id = _index(genres)

    out: list = []
    out.extend(_check_id_resolution(
        story, beats_by_id, strands_by_id, genres_by_id,
    ))
    out.extend(_check_theme_statement(story))
    out.extend(_check_beat_slot_coverage(story, beats_by_id))
    out.extend(_check_page_actual_monotonic(story, beats_by_id))
    out.extend(_check_strand_kinds(story, strands_by_id))
    out.extend(_check_advancement_strand_resolution(
        story, beats_by_id, strands_by_id,
    ))
    out.extend(_check_genre_archetypes(story, genres_by_id))
    return out


# ============================================================================
# Convenience grouping (parallel to dramatic.group_*)
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
# Per-record-type coupling-kind declarations (parallel to
# dramatic.COUPLING_DECLARATIONS — supports verifier orchestrator
# reuse on Save the Cat encodings)
# ============================================================================
#
# Save the Cat is more prescriptive than Dramatic, which means more
# fields admit Claim-shaped coupling kinds. The same vocabulary applies:
#
# - "realization":      upper record made true by specific lower records
# - "characterization": upper record classifies a substrate pattern
# - "claim-moment":     upper record asserts substrate state at a τ_s
# - "claim-trajectory": upper record asserts substrate trajectory
# - "flavor":           free-form metadata, no formal check
#
# A future companion module would use verification.COUPLING_* and
# orchestrate_checks against these declarations.

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
    record_type: str
    field: Optional[str]
    kind: str


COUPLING_DECLARATIONS: Tuple[CouplingDeclaration, ...] = (
    # Story root realizes (the Story binds to the substrate's branch
    # the encoding sits on).
    CouplingDeclaration("StcStory", None, COUPLING_REALIZATION),

    # Theme statement is a Claim-trajectory: the substrate trajectory
    # should exhibit the theme's arc across the story.
    CouplingDeclaration(
        "StcStory", "theme_statement", COUPLING_CLAIM_TRAJECTORY,
    ),

    # Beat fields. description_of_change is Claim-moment (the substrate
    # change at this beat's moment); page_actual is structural (within-
    # dialect coordinate, no substrate analog directly).
    CouplingDeclaration(
        "StcBeat", "description_of_change", COUPLING_CLAIM_MOMENT,
    ),
    CouplingDeclaration("StcBeat", "advances", COUPLING_REALIZATION),

    # Strand description is Claim-trajectory (the strand traces an arc
    # through substrate state).
    CouplingDeclaration(
        "StcStrand", "description", COUPLING_CLAIM_TRAJECTORY,
    ),

    # Genre is a Template-shaped field; archetypes are a
    # Characterization-coupling target (the substrate should exhibit
    # the archetype patterns).
    CouplingDeclaration(
        "StcGenre", "archetypes", COUPLING_CHARACTERIZATION,
    ),
)
