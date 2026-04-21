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

save-the-cat-sketch-02 amendment (StcCharacter) commitments:
- S9:  StcCharacter as a minimal optional record type.
- S10: Role labels as canonical-plus-open vocabulary.
- S11: Optional reference wiring on StcBeat / StcStrand / StcStory.
- S12: Genre archetype assignments bind archetypes to characters
       or prose notes.
- S13: Three new verifier checks — character-id resolution,
       one-protagonist advisory, archetype coverage.

save-the-cat-sketch-03 amendment (compilation-surface instantiation)
commitments:
- S14: Side-1 hard structural extensions surface; three first-member
       flavors (page_target_tolerance on StcBeat,
       co_presence_required_at_slot on StcStory,
       strand_convergence_required_at_slot on StcStory).
- S15: Side-2 soft preference annotations surface; three first-member
       flavors (tonal_register and genre_adherence_preference on
       StcStory, emphasis_preference on StcBeat).
- S16: Three new verifier checks covering S14's flavors (S16.1 page
       tolerance, S16.2 co-presence structural integrity +
       participation, S16.3 strand-convergence structural integrity
       + advancement).

Per `dialect-compilation-surface-sketch-01` DCS3, S15 fields receive
no verifier coverage by construction. Per DCS4, all new fields are
optional with empty / 0 / "" defaults; pre-sketch-03 encodings
verify identically.
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
    surfaces it as an observation, not an error).

    Per S11, `participant_ids` is an optional tuple of StcCharacter
    ids present in the beat. Empty by default — existing encodings
    that pre-date sketch-02 continue to verify cleanly without
    wiring. When set, the verifier checks that every id resolves.

    Per S14-SE1 (sketch-03), `page_tolerance_before` and
    `page_tolerance_after` express the hard constraint that
    `page_actual` may drift up to that many pages below or above the
    canonical `page_target` for this slot. Both default 0, meaning
    the field carries no constraint. Verified by S16.1.

    Per S15-SP3 (sketch-03), `emphasis_preference` is a soft per-beat
    ranker input from a canonical-plus-open vocabulary
    `{minimal, standard, expanded, centerpiece, ""}`. Empty string
    is neutral. Not verifier-covered (DCS3)."""
    id: str
    slot: int
    page_actual: int
    description_of_change: str = ""
    advances: tuple = ()              # tuple[StrandAdvancement, ...]
    participant_ids: tuple = ()       # tuple[str, ...] — StcCharacter ids
    page_tolerance_before: int = 0    # S14-SE1 (sketch-03)
    page_tolerance_after: int = 0     # S14-SE1 (sketch-03)
    emphasis_preference: str = ""     # S15-SP3 (sketch-03)
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
    encodings (especially short-form) collapse them.

    Per S11, `focal_character_id` optionally names the one character
    the strand is structurally about (often the protagonist for the
    A story and the love-interest for the B story under Snyder's
    convention). None by default."""
    id: str
    kind: StrandKind
    description: str = ""
    focal_character_id: Optional[str] = None
    authored_by: str = "author"


# ============================================================================
# StcCharacter and role labels (S9, S10)
# ============================================================================
#
# Per save-the-cat-sketch-02 S9, a minimal optional record. S10 names
# a canonical role-label set the dialect recognizes; open strings are
# admissible (per-genre archetypes and author-introduced labels live
# in the open-string tail).


# Canonical role labels. Authors may use others; these are what the
# verifier's one-protagonist advisory and the walker's grouping
# recognize. Stability of this list is OQ4 — expand cautiously.
CANONICAL_ROLE_LABELS: Tuple[str, ...] = (
    "protagonist",
    "antagonist",
    "love-interest",
    "mentor",
    "confidant",
    "ally",
    "narrator",
    "victim",
    "suspect",
    "threshold-guardian",
)

CANONICAL_ROLE_LABEL_SET = frozenset(CANONICAL_ROLE_LABELS)


@dataclass(frozen=True)
class StcCharacter:
    """One authored character. Deliberately minimal (per S9) — id,
    name, description, role_labels. The dialect does not track
    character-character relations or per-character arcs at this
    iteration; see save-the-cat-sketch-02 open questions.

    `role_labels` is a tuple (not a set) to preserve author-declared
    ordering when a character carries multiple overlapping roles —
    the Ackroyd case where Sheppard is
    ("protagonist", "antagonist", "narrator"). Labels drawn from
    `CANONICAL_ROLE_LABELS` are recognized by the verifier; open
    strings are admitted for per-genre archetypes and the long tail."""
    id: str
    name: str
    description: str = ""
    role_labels: Tuple[str, ...] = ()
    authored_by: str = "author"


@dataclass(frozen=True)
class StcArchetypeAssignment:
    """One binding between a genre archetype label and either a
    character id or a prose note (S12). Exactly one of
    `character_id` / `note` must be set; the verifier surfaces
    both-set or neither-set as advise-review."""
    archetype: str
    character_id: Optional[str] = None
    note: str = ""


# ============================================================================
# Compilation-surface sub-records (S14-SE2, S14-SE3) — sketch-03
# ============================================================================


@dataclass(frozen=True)
class StcCoPresenceRequirement:
    """S14-SE2 (sketch-03). Hard constraint: the named characters must
    all appear in `participant_ids` of at least `min_count` authored
    beats whose slot matches. The requirement is on slot-scoped
    beat-level co-presence — Save the Cat's analog to Aristotelian's
    A15-SE2 co-presence-over-phase. Field-shape parity with the
    Aristotelian form is the strongest cross-dialect symmetry signal
    observed during the DCS1 DOQ2 spike."""
    id: str
    character_ref_ids: Tuple[str, ...]  # ≥ 2 characters
    slot: int                            # 1..15
    min_count: int = 1


@dataclass(frozen=True)
class StcStrandConvergenceRequirement:
    """S14-SE3 (sketch-03). Hard constraint: at the named slot, each
    strand named in `strand_ref_ids` must be advanced (appear in at
    least one authored beat's `advances`) by at least one beat in
    that slot. Captures Snyder's 'A and B collide' convention at
    Midpoint and the 'A and B resolve together' convention at Finale.

    Dialect-specific — strands are an STC primitive with no
    Aristotelian analog."""
    id: str
    strand_ref_ids: Tuple[str, ...]  # ≥ 2 strands
    slot: int                         # 1..15


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

    Per S11, `character_ids` aggregates the Story's characters — the
    authoritative list the verifier walks for one-protagonist and
    archetype-coverage checks. Per S12, `archetype_assignments`
    binds each of the declared genre's archetypes to either a
    character or a prose note.

    Per S14-SE2 + S14-SE3 (sketch-03), `co_presence_requirements`
    and `strand_convergence_requirements` carry hard structural
    constraints the compiler reads from stages 1–3. Both default
    empty; S16.2 and S16.3 verify structural integrity and
    participation/advancement.

    Per S15-SP1 + S15-SP2 (sketch-03), `tonal_register` and
    `genre_adherence_preference` are soft ranker inputs consumed at
    compiler stage 4. Both default "". No verifier coverage per DCS3.
    """
    id: str
    title: str
    theme_statement: str = ""
    stc_genre_id: Optional[str] = None
    beat_ids: tuple = ()       # tuple[str, ...]
    strand_ids: tuple = ()     # tuple[str, ...]
    character_ids: tuple = ()  # tuple[str, ...] — S11
    archetype_assignments: tuple = ()  # tuple[StcArchetypeAssignment, ...] — S12
    co_presence_requirements: tuple = ()        # S14-SE2 (sketch-03)
    strand_convergence_requirements: tuple = () # S14-SE3 (sketch-03)
    tonal_register: str = ""                    # S15-SP1 (sketch-03)
    genre_adherence_preference: str = ""        # S15-SP2 (sketch-03)
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
    archetypes; archetype-coverage is the S13
    _check_archetype_coverage job (see below), which runs when
    sketch-02's archetype_assignments are present."""
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


# ============================================================================
# S13 — character-id resolution, one-protagonist, archetype coverage
# ============================================================================


def _check_character_references_resolve(
    story: StcStory,
    beats_by_id: dict,
    strands_by_id: dict,
    characters_by_id: dict,
) -> list:
    """S13 (1): every character id named in StcStory.character_ids,
    StcBeat.participant_ids, StcStrand.focal_character_id, and
    StcArchetypeAssignment.character_id must resolve. Unresolved
    ids advise-review."""
    out = []
    known = set(characters_by_id.keys())

    for cid in story.character_ids:
        if cid not in known:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="character_id_unresolved",
                target_id=story.id,
                message=(f"Story {story.id!r} references character_id "
                         f"{cid!r} which is not in the characters "
                         f"collection"),
            ))

    for bid in story.beat_ids:
        if bid not in beats_by_id:
            continue
        b = beats_by_id[bid]
        for cid in b.participant_ids:
            if cid not in known:
                out.append(StcObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="participant_id_unresolved",
                    target_id=b.id,
                    message=(f"Beat {b.id!r} names participant_id "
                             f"{cid!r} which is not in the characters "
                             f"collection"),
                ))

    for sid in story.strand_ids:
        if sid not in strands_by_id:
            continue
        s = strands_by_id[sid]
        if s.focal_character_id is not None and s.focal_character_id not in known:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="focal_character_id_unresolved",
                target_id=s.id,
                message=(f"Strand {s.id!r} names focal_character_id "
                         f"{s.focal_character_id!r} which is not in "
                         f"the characters collection"),
            ))

    for aa in story.archetype_assignments:
        if aa.character_id is not None and aa.character_id not in known:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="archetype_character_id_unresolved",
                target_id=story.id,
                message=(f"ArchetypeAssignment for archetype "
                         f"{aa.archetype!r} names character_id "
                         f"{aa.character_id!r} which is not in the "
                         f"characters collection"),
            ))

    return out


def _check_unreferenced_characters(
    story: StcStory,
    beats_by_id: dict,
    strands_by_id: dict,
    characters_by_id: dict,
) -> list:
    """S11: characters that aren't named in any beat's
    participant_ids, any strand's focal_character_id, or any
    archetype assignment's character_id are noted (informational —
    some encodings declare cast up front and wire in later)."""
    out = []
    referenced = set()
    for bid in story.beat_ids:
        if bid in beats_by_id:
            referenced.update(beats_by_id[bid].participant_ids)
    for sid in story.strand_ids:
        if sid in strands_by_id:
            s = strands_by_id[sid]
            if s.focal_character_id is not None:
                referenced.add(s.focal_character_id)
    for aa in story.archetype_assignments:
        if aa.character_id is not None:
            referenced.add(aa.character_id)

    for cid in story.character_ids:
        if cid not in characters_by_id:
            continue  # already surfaced by _check_character_references_resolve
        if cid not in referenced:
            out.append(StcObservation(
                severity=SEVERITY_NOTED,
                code="character_unreferenced",
                target_id=cid,
                message=(f"Character {cid!r} is declared on the Story "
                         f"but not referenced by any beat, strand, or "
                         f"archetype assignment. Admissible — some "
                         f"encodings declare cast up front"),
            ))
    return out


def _check_one_protagonist(
    story: StcStory,
    characters_by_id: dict,
) -> list:
    """S13 (2): exactly-one character carries 'protagonist' in
    role_labels is the expected shape. Multiple protagonists
    advise-review (ensemble stories exist but are unusual); zero
    protagonists is noted (informational)."""
    out = []
    protagonists = [
        characters_by_id[cid]
        for cid in story.character_ids
        if cid in characters_by_id
        and "protagonist" in characters_by_id[cid].role_labels
    ]
    if len(protagonists) > 1:
        ids = [c.id for c in protagonists]
        out.append(StcObservation(
            severity=SEVERITY_ADVISES_REVIEW,
            code="multiple_protagonists",
            target_id=story.id,
            message=(f"Story {story.id!r} has multiple characters "
                     f"carrying 'protagonist' in role_labels: {ids}. "
                     f"Snyder's framework assumes one; ensemble stories "
                     f"do exist but confirm intentional"),
        ))
    elif len(protagonists) == 0 and story.character_ids:
        out.append(StcObservation(
            severity=SEVERITY_NOTED,
            code="no_protagonist_declared",
            target_id=story.id,
            message=(f"Story {story.id!r} declares characters but none "
                     f"carries 'protagonist' in role_labels. If a "
                     f"character plays that role, label it so the "
                     f"verifier recognizes the structural claim"),
        ))
    return out


def _check_archetype_coverage(
    story: StcStory,
    genres_by_id: dict,
    characters_by_id: dict,
) -> list:
    """S13 (3): if the Story declares a genre with archetypes, every
    archetype should appear in exactly one archetype_assignment.
    Missing archetypes advise-review; duplicated archetypes
    advise-review; extraneous archetypes (not in the genre's list)
    advise-review. Each assignment must have exactly one of
    character_id / note set; neither-or-both advise-review."""
    out = []

    # Each archetype_assignment must have exactly one of the two set.
    for aa in story.archetype_assignments:
        has_char = aa.character_id is not None
        has_note = bool(aa.note.strip())
        if has_char and has_note:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="archetype_assignment_both_set",
                target_id=story.id,
                message=(f"ArchetypeAssignment for archetype "
                         f"{aa.archetype!r} has both character_id and "
                         f"note set; exactly one is expected"),
            ))
        if not has_char and not has_note:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="archetype_assignment_neither_set",
                target_id=story.id,
                message=(f"ArchetypeAssignment for archetype "
                         f"{aa.archetype!r} has neither character_id "
                         f"nor note set; exactly one is expected"),
            ))

    # Coverage against the declared genre's archetypes.
    if story.stc_genre_id is None:
        # No genre → no coverage check. But if archetype_assignments
        # are set without a genre, that's a smell worth noting.
        if story.archetype_assignments:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="archetype_assignments_without_genre",
                target_id=story.id,
                message=(f"Story {story.id!r} declares "
                         f"archetype_assignments but no stc_genre_id; "
                         f"archetypes are genre-scoped"),
            ))
        return out
    if story.stc_genre_id not in genres_by_id:
        return out  # already surfaced by _check_id_resolution
    genre = genres_by_id[story.stc_genre_id]

    archetype_seq = [aa.archetype for aa in story.archetype_assignments]
    archetype_set = set(archetype_seq)
    declared = set(genre.archetypes)

    # Missing: archetypes declared by the genre but not assigned.
    for ar in genre.archetypes:
        if ar not in archetype_set:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="archetype_missing",
                target_id=story.id,
                message=(f"Genre {genre.name!r} names archetype "
                         f"{ar!r}; the Story has no "
                         f"archetype_assignment for it. Bind it to a "
                         f"character or provide a prose note, or "
                         f"document why it's intentionally absent"),
            ))

    # Duplicated: one archetype appearing multiple times.
    seen = set()
    for ar in archetype_seq:
        if ar in seen:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="archetype_duplicated",
                target_id=story.id,
                message=(f"Archetype {ar!r} appears in multiple "
                         f"archetype_assignments; exactly one "
                         f"assignment per archetype is expected"),
            ))
        seen.add(ar)

    # Extraneous: archetypes assigned but not in the genre's list.
    for ar in archetype_seq:
        if ar not in declared:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="archetype_extraneous",
                target_id=story.id,
                message=(f"ArchetypeAssignment names archetype "
                         f"{ar!r} which is not in genre "
                         f"{genre.name!r}'s archetypes "
                         f"{list(genre.archetypes)}"),
            ))

    return out


# ============================================================================
# S16 — compilation-surface verifier checks (sketch-03)
# ============================================================================


def _check_page_target_tolerance(
    story: StcStory, beats_by_id: dict,
) -> list:
    """S16.1 (S14-SE1). For each authored beat on the story:
    tolerances non-negative; if either is set, `page_actual` falls
    within the tolerance window around the canonical `page_target`
    for the beat's slot. Skips cleanly when both tolerances at
    default 0."""
    out = []
    for bid in story.beat_ids:
        if bid not in beats_by_id:
            continue
        b = beats_by_id[bid]
        if b.page_tolerance_before < 0:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="page_tolerance_before_negative",
                target_id=b.id,
                message=(f"Beat {b.id!r} has page_tolerance_before="
                         f"{b.page_tolerance_before}; must be ≥ 0"),
            ))
        if b.page_tolerance_after < 0:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="page_tolerance_after_negative",
                target_id=b.id,
                message=(f"Beat {b.id!r} has page_tolerance_after="
                         f"{b.page_tolerance_after}; must be ≥ 0"),
            ))
        if b.page_tolerance_before == 0 and b.page_tolerance_after == 0:
            continue  # neither bound active; default-empty tolerance window
        if b.page_tolerance_before < 0 or b.page_tolerance_after < 0:
            continue  # negative bound already surfaced; skip positional check
        canonical = CANONICAL_BEAT_BY_SLOT.get(b.slot)
        if canonical is None:
            continue  # should not happen; slot already range-checked on construction
        earliest = canonical.page_target - b.page_tolerance_before
        latest = canonical.page_target + b.page_tolerance_after
        if b.page_actual < earliest:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="page_actual_before_tolerance",
                target_id=b.id,
                message=(f"Beat {b.id!r} has page_actual={b.page_actual} "
                         f"which is earlier than tolerance window "
                         f"[{earliest}, {latest}] around canonical "
                         f"page_target={canonical.page_target} for slot "
                         f"{b.slot} ({canonical.name!r})"),
            ))
        if b.page_actual > latest:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="page_actual_after_tolerance",
                target_id=b.id,
                message=(f"Beat {b.id!r} has page_actual={b.page_actual} "
                         f"which is later than tolerance window "
                         f"[{earliest}, {latest}] around canonical "
                         f"page_target={canonical.page_target} for slot "
                         f"{b.slot} ({canonical.name!r})"),
            ))
    return out


def _check_co_presence_requirements(
    story: StcStory,
    beats_by_id: dict,
    characters_by_id: dict,
) -> list:
    """S16.2 (S14-SE2). For each co-presence requirement on the
    story: structural integrity (≥2 refs, characters resolve, slot
    in range, min_count ≥ 1) plus participation (≥min_count authored
    beats at matching slot whose participant_ids cover all named
    characters)."""
    out = []
    known_chars = set(characters_by_id.keys())
    for req in story.co_presence_requirements:
        # Structural integrity.
        if len(req.character_ref_ids) < 2:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="co_presence_refs_too_few",
                target_id=req.id,
                message=(f"CoPresenceRequirement {req.id!r} names "
                         f"{len(req.character_ref_ids)} character(s); "
                         f"co-presence requires at least 2"),
            ))
        for cid in req.character_ref_ids:
            if cid not in known_chars:
                out.append(StcObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="co_presence_character_unresolved",
                    target_id=req.id,
                    message=(f"CoPresenceRequirement {req.id!r} names "
                             f"character_ref_id {cid!r} which is not in "
                             f"the characters collection"),
                ))
        if not (1 <= req.slot <= NUM_CANONICAL_BEATS):
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="co_presence_slot_out_of_range",
                target_id=req.id,
                message=(f"CoPresenceRequirement {req.id!r} has slot="
                         f"{req.slot}; must be 1..{NUM_CANONICAL_BEATS}"),
            ))
        if req.min_count < 1:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="co_presence_min_count_zero",
                target_id=req.id,
                message=(f"CoPresenceRequirement {req.id!r} has min_count="
                         f"{req.min_count}; must be ≥ 1"),
            ))

        # Participation: count beats at matching slot whose
        # participant_ids cover all named characters. Skip if the
        # requirement is structurally broken (would produce noise).
        if (len(req.character_ref_ids) < 2
                or not (1 <= req.slot <= NUM_CANONICAL_BEATS)
                or req.min_count < 1):
            continue
        needed = set(req.character_ref_ids)
        covering_count = 0
        for bid in story.beat_ids:
            if bid not in beats_by_id:
                continue
            b = beats_by_id[bid]
            if b.slot != req.slot:
                continue
            if needed.issubset(set(b.participant_ids)):
                covering_count += 1
        if covering_count < req.min_count:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="co_presence_insufficient_participation",
                target_id=req.id,
                message=(f"CoPresenceRequirement {req.id!r} at slot "
                         f"{req.slot} requires {req.min_count} beat(s) "
                         f"with all of {list(req.character_ref_ids)} in "
                         f"participant_ids; found {covering_count}"),
            ))
    return out


def _check_strand_convergence_requirements(
    story: StcStory,
    beats_by_id: dict,
    strands_by_id: dict,
) -> list:
    """S16.3 (S14-SE3). For each strand convergence requirement on
    the story: structural integrity (≥2 refs, strands resolve, slot
    in range) plus advancement (each named strand appears in at
    least one beat at the matching slot's `advances`). Emits one
    missing-advancement observation per strand that fails
    independently."""
    out = []
    known_strands = set(strands_by_id.keys())
    for req in story.strand_convergence_requirements:
        if len(req.strand_ref_ids) < 2:
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="strand_convergence_refs_too_few",
                target_id=req.id,
                message=(f"StrandConvergenceRequirement {req.id!r} names "
                         f"{len(req.strand_ref_ids)} strand(s); "
                         f"convergence requires at least 2"),
            ))
        for sid in req.strand_ref_ids:
            if sid not in known_strands:
                out.append(StcObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="strand_convergence_strand_unresolved",
                    target_id=req.id,
                    message=(f"StrandConvergenceRequirement {req.id!r} "
                             f"names strand_ref_id {sid!r} which is not "
                             f"in the strands collection"),
                ))
        if not (1 <= req.slot <= NUM_CANONICAL_BEATS):
            out.append(StcObservation(
                severity=SEVERITY_ADVISES_REVIEW,
                code="strand_convergence_slot_out_of_range",
                target_id=req.id,
                message=(f"StrandConvergenceRequirement {req.id!r} has "
                         f"slot={req.slot}; must be 1..{NUM_CANONICAL_BEATS}"),
            ))

        # Advancement: for each strand, at least one beat at the
        # matching slot must advance it. Skip if structurally broken.
        if (len(req.strand_ref_ids) < 2
                or not (1 <= req.slot <= NUM_CANONICAL_BEATS)):
            continue
        for sid in req.strand_ref_ids:
            if sid not in known_strands:
                continue  # unresolved already surfaced
            advanced = False
            for bid in story.beat_ids:
                if bid not in beats_by_id:
                    continue
                b = beats_by_id[bid]
                if b.slot != req.slot:
                    continue
                if any(adv.strand_id == sid for adv in b.advances):
                    advanced = True
                    break
            if not advanced:
                out.append(StcObservation(
                    severity=SEVERITY_ADVISES_REVIEW,
                    code="strand_convergence_missing_advancement",
                    target_id=req.id,
                    message=(f"StrandConvergenceRequirement {req.id!r} "
                             f"at slot {req.slot}: no authored beat in "
                             f"that slot advances strand {sid!r}"),
                ))
    return out


def verify(
    story: StcStory,
    *,
    beats: tuple = (),
    strands: tuple = (),
    characters: tuple = (),
    genres: tuple = GENRES,
) -> list:
    """Run all self-verification checks on a Story plus its record
    bundle. Returns a list of StcObservation records.

    Per S6, no check rejects a Story; observations are advisory and
    flow to the proposal queue (in a higher layer) for author walking.
    Verification is a partner, not a gate.

    `characters` is the tuple of StcCharacter records per S9 / S11.
    Empty by default — encodings that pre-date sketch-02 continue to
    verify without wiring characters. The S13 checks activate only
    when the Story declares character_ids or archetype_assignments.
    """
    beats_by_id = _index(beats)
    strands_by_id = _index(strands)
    characters_by_id = _index(characters)
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
    # S13 — character-layer checks (amendment, sketch-02)
    out.extend(_check_character_references_resolve(
        story, beats_by_id, strands_by_id, characters_by_id,
    ))
    out.extend(_check_unreferenced_characters(
        story, beats_by_id, strands_by_id, characters_by_id,
    ))
    out.extend(_check_one_protagonist(story, characters_by_id))
    out.extend(_check_archetype_coverage(
        story, genres_by_id, characters_by_id,
    ))
    # S16 — compilation-surface checks (sketch-03)
    out.extend(_check_page_target_tolerance(story, beats_by_id))
    out.extend(_check_co_presence_requirements(
        story, beats_by_id, characters_by_id,
    ))
    out.extend(_check_strand_convergence_requirements(
        story, beats_by_id, strands_by_id,
    ))
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
