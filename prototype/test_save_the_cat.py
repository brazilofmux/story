"""
test_save_the_cat.py — permanent tests for the Save the Cat dialect
(per save-the-cat-sketch-01 commitments S1-S8).

Synthetic-fixture tests pin the dialect's invariants — canonical beat
sheet shape, the ten genres, record construction, and self-verifier
behavior across each observation code. No integration tests yet
because no encoding has landed; those will arrive in a follow-on
when (e.g.) macbeth_save_the_cat.py exists.

Run:
    python3 test_save_the_cat.py
"""

from __future__ import annotations

import sys
import traceback

from save_the_cat import (
    CANONICAL_BEATS, CANONICAL_BEAT_BY_SLOT, CANONICAL_BEAT_NAMES,
    NUM_CANONICAL_BEATS,
    GENRES, GENRE_BY_ID,
    GENRE_MONSTER_IN_THE_HOUSE, GENRE_WHYDUNIT,
    StcStory, StcBeat, StcStrand, StcGenre,
    StcCharacter, StcArchetypeAssignment,
    CANONICAL_ROLE_LABELS, CANONICAL_ROLE_LABEL_SET,
    StrandAdvancement, StrandKind, StcObservation,
    SEVERITY_NOTED, SEVERITY_ADVISES_REVIEW,
    verify, group_by_severity, group_by_code,
    COUPLING_DECLARATIONS,
    COUPLING_REALIZATION, COUPLING_CHARACTERIZATION,
    COUPLING_CLAIM_MOMENT, COUPLING_CLAIM_TRAJECTORY,
    VALID_COUPLING_KINDS,
)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


def _full_beat_set() -> tuple:
    """A clean 15-beat tuple with strictly-monotonic page_actuals.
    Used as a baseline that the verifier should produce few or no
    observations against."""
    return tuple(
        StcBeat(
            id=f"B_{i}",
            slot=i,
            page_actual=i * 7,  # 7, 14, 21, ..., 105 — strictly monotonic
            description_of_change=f"slot {i} change",
        )
        for i in range(1, NUM_CANONICAL_BEATS + 1)
    )


def _full_story(**overrides) -> StcStory:
    """A clean StcStory referencing a 15-beat full set, with theme
    statement, a genre, and archetype_assignments covering the
    genre's three archetypes via prose notes. Used as the baseline a
    test mutates from. Clean under both sketch-01 S1–S8 and
    sketch-02 S9–S13."""
    from save_the_cat import StcArchetypeAssignment
    beats = _full_beat_set()
    base = dict(
        id="S_test", title="Test Story",
        theme_statement="ambition unmakes the ambitious",
        stc_genre_id=GENRE_MONSTER_IN_THE_HOUSE.id,
        beat_ids=tuple(b.id for b in beats),
        strand_ids=(),
        archetype_assignments=(
            StcArchetypeAssignment(
                archetype="the monster", note="test monster",
            ),
            StcArchetypeAssignment(
                archetype="the house", note="test house",
            ),
            StcArchetypeAssignment(
                archetype="the sin", note="test sin",
            ),
        ),
    )
    base.update(overrides)
    return StcStory(**base)


def _codes(observations: list) -> set:
    return {o.code for o in observations}


# ----------------------------------------------------------------------------
# Canonical beat sheet (S1)
# ----------------------------------------------------------------------------


def test_canonical_beats_has_fifteen_entries():
    assert len(CANONICAL_BEATS) == 15
    assert NUM_CANONICAL_BEATS == 15


def test_canonical_beats_slot_positions_are_1_to_15():
    slots = [b.slot for b in CANONICAL_BEATS]
    assert slots == list(range(1, 16)), (
        f"canonical beat slots should be 1..15 in order; got {slots}"
    )


def test_canonical_beat_names_match_snyder():
    """Spot-check a few beat names that should be exactly Snyder's
    terminology — these are what an author already familiar with
    Save the Cat will recognize."""
    expected = {
        1: "Opening Image",
        4: "Catalyst",
        6: "Break Into Two",
        9: "Midpoint",
        11: "All Is Lost",
        14: "Finale",
        15: "Final Image",
    }
    for slot, name in expected.items():
        assert CANONICAL_BEAT_BY_SLOT[slot].name == name, (
            f"slot {slot} should be named {name!r}; got "
            f"{CANONICAL_BEAT_BY_SLOT[slot].name!r}"
        )


def test_canonical_beat_lookup_by_slot():
    for slot in range(1, 16):
        b = CANONICAL_BEAT_BY_SLOT[slot]
        assert b.slot == slot
        assert b.name in CANONICAL_BEAT_NAMES


# ----------------------------------------------------------------------------
# Genres (S5)
# ----------------------------------------------------------------------------


def test_genres_count_is_ten():
    assert len(GENRES) == 10


def test_genre_by_id_lookup():
    assert "monster-in-the-house" in GENRE_BY_ID
    assert "buddy-love" in GENRE_BY_ID
    assert "superhero" in GENRE_BY_ID


def test_each_genre_carries_archetypes():
    """Per S5, archetypes are the genre's structural commitment. Each
    genre should ship with at least one archetype."""
    for g in GENRES:
        assert g.archetypes, f"genre {g.id!r} has no archetypes"


# ----------------------------------------------------------------------------
# StcBeat construction (S1)
# ----------------------------------------------------------------------------


def test_stc_beat_valid_slot_constructs():
    b = StcBeat(id="B_one", slot=1, page_actual=1)
    assert b.slot == 1


def test_stc_beat_slot_zero_raises():
    try:
        StcBeat(id="B_bad", slot=0, page_actual=1)
    except ValueError as e:
        assert "out of range" in str(e)
        return
    raise AssertionError("StcBeat with slot=0 should raise")


def test_stc_beat_slot_sixteen_raises():
    try:
        StcBeat(id="B_bad", slot=16, page_actual=1)
    except ValueError as e:
        assert "out of range" in str(e)
        return
    raise AssertionError("StcBeat with slot=16 should raise")


def test_stc_beat_advances_default_empty():
    b = StcBeat(id="B_one", slot=1, page_actual=1)
    assert b.advances == ()


def test_stc_beat_carries_strand_advancements():
    adv = StrandAdvancement(strand_id="A", note="shifts the A story")
    b = StcBeat(id="B_one", slot=1, page_actual=1, advances=(adv,))
    assert len(b.advances) == 1
    assert b.advances[0].strand_id == "A"


# ----------------------------------------------------------------------------
# StcStrand (S3)
# ----------------------------------------------------------------------------


def test_stc_strand_kind_enum():
    a = StcStrand(id="A", kind=StrandKind.A_STORY)
    b = StcStrand(id="B", kind=StrandKind.B_STORY)
    assert a.kind == StrandKind.A_STORY
    assert b.kind == StrandKind.B_STORY


# ----------------------------------------------------------------------------
# verify — empty story (S6)
# ----------------------------------------------------------------------------


def test_verify_empty_story_flags_all_unfilled_slots_plus_empty_theme():
    """An empty Story should surface 15 beat_slot_unfilled
    observations plus 1 theme_statement_empty observation. That's the
    homework-shape: 'here are the 16 things you have not yet
    addressed.'"""
    obs = verify(StcStory(id="S_empty", title="Empty"))
    codes = _codes(obs)
    assert "theme_statement_empty" in codes
    unfilled_count = sum(
        1 for o in obs if o.code == "beat_slot_unfilled"
    )
    assert unfilled_count == 15, (
        f"empty story should flag all 15 slots unfilled; got "
        f"{unfilled_count}"
    )


# ----------------------------------------------------------------------------
# verify — clean full story
# ----------------------------------------------------------------------------


def test_verify_full_story_with_monotonic_pages_is_minimal():
    """A Story with all 15 beats at strictly-monotonic page_actuals
    and a theme statement should produce only the informational
    `genre_archetypes_declared` notice (no advise-review observations)."""
    beats = _full_beat_set()
    story = _full_story()
    obs = verify(story, beats=beats)
    advises = [o for o in obs if o.severity == SEVERITY_ADVISES_REVIEW]
    assert advises == [], (
        f"clean full story should have no advise-review observations; "
        f"got {[o.code for o in advises]}"
    )
    # Genre informational notice should still appear.
    assert "genre_archetypes_declared" in _codes(obs)


# ----------------------------------------------------------------------------
# verify — individual codes
# ----------------------------------------------------------------------------


def test_verify_flags_theme_statement_empty():
    beats = _full_beat_set()
    story = _full_story(theme_statement="")
    obs = verify(story, beats=beats)
    assert "theme_statement_empty" in _codes(obs)


def test_verify_flags_theme_statement_whitespace_only():
    """Whitespace-only theme is treated as empty — the framework
    treats theme as load-bearing, and `   ` is not a load-bearing
    claim."""
    beats = _full_beat_set()
    story = _full_story(theme_statement="   \n  ")
    obs = verify(story, beats=beats)
    assert "theme_statement_empty" in _codes(obs)


def test_verify_flags_beat_id_unresolved():
    beats = _full_beat_set()
    story = _full_story(
        beat_ids=tuple(b.id for b in beats) + ("B_ghost",),
    )
    obs = verify(story, beats=beats)
    assert "beat_id_unresolved" in _codes(obs)


def test_verify_flags_strand_id_unresolved():
    beats = _full_beat_set()
    story = _full_story(strand_ids=("S_ghost",))
    obs = verify(story, beats=beats, strands=())
    assert "strand_id_unresolved" in _codes(obs)


def test_verify_flags_genre_unknown():
    beats = _full_beat_set()
    story = _full_story(stc_genre_id="not-a-real-genre")
    obs = verify(story, beats=beats)
    assert "genre_unknown" in _codes(obs)


def test_verify_flags_beat_slot_unfilled_for_specific_slots():
    """A Story missing slot 9 (Midpoint) should flag exactly that
    slot — not all 15."""
    full = _full_beat_set()
    # Drop the slot-9 beat.
    beats = tuple(b for b in full if b.slot != 9)
    story = _full_story(beat_ids=tuple(b.id for b in beats))
    obs = verify(story, beats=beats)
    unfilled = [
        o for o in obs if o.code == "beat_slot_unfilled"
    ]
    assert len(unfilled) == 1
    assert "Midpoint" in unfilled[0].message


def test_verify_flags_multiple_beats_per_slot():
    """Two beats sharing slot 8 (Fun and Games) — admissible per S1
    but surfaced as a noted observation."""
    full = list(_full_beat_set())
    extra = StcBeat(id="B_8b", slot=8, page_actual=40)
    beats = tuple(full + [extra])
    story = _full_story(beat_ids=tuple(b.id for b in beats))
    obs = verify(story, beats=beats)
    assert "multiple_beats_per_slot" in _codes(obs)
    # Severity is noted, not advises-review (per S1 admissibility).
    multi_obs = next(
        o for o in obs if o.code == "multiple_beats_per_slot"
    )
    assert multi_obs.severity == SEVERITY_NOTED


def test_verify_flags_page_actual_non_monotonic():
    """A beat with page_actual that goes backward against slot order
    surfaces."""
    full = list(_full_beat_set())
    # Replace slot 5 with a page that goes backward from slot 4's page (28).
    full[4] = StcBeat(id="B_5", slot=5, page_actual=10)
    beats = tuple(full)
    story = _full_story(beat_ids=tuple(b.id for b in beats))
    obs = verify(story, beats=beats)
    assert "page_actual_non_monotonic" in _codes(obs)


def test_verify_flags_multiple_a_strands():
    beats = _full_beat_set()
    strands = (
        StcStrand(id="A1", kind=StrandKind.A_STORY),
        StcStrand(id="A2", kind=StrandKind.A_STORY),
    )
    story = _full_story(
        beat_ids=tuple(b.id for b in beats),
        strand_ids=tuple(s.id for s in strands),
    )
    obs = verify(story, beats=beats, strands=strands)
    assert "multiple_a_strands" in _codes(obs)


def test_verify_flags_multiple_b_strands():
    beats = _full_beat_set()
    strands = (
        StcStrand(id="B1", kind=StrandKind.B_STORY),
        StcStrand(id="B2", kind=StrandKind.B_STORY),
    )
    story = _full_story(
        beat_ids=tuple(b.id for b in beats),
        strand_ids=tuple(s.id for s in strands),
    )
    obs = verify(story, beats=beats, strands=strands)
    assert "multiple_b_strands" in _codes(obs)


def test_verify_flags_advancement_strand_unresolved():
    """A beat that advances a non-existent strand surfaces."""
    full = list(_full_beat_set())
    full[7] = StcBeat(
        id="B_8", slot=8, page_actual=56,
        advances=(StrandAdvancement(strand_id="S_ghost"),),
    )
    beats = tuple(full)
    strands = (StcStrand(id="A", kind=StrandKind.A_STORY),)
    story = _full_story(
        beat_ids=tuple(b.id for b in beats),
        strand_ids=("A",),
    )
    obs = verify(story, beats=beats, strands=strands)
    assert "advancement_strand_unresolved" in _codes(obs)


def test_verify_genre_archetypes_declared_is_informational():
    """A Story declaring a genre always surfaces a noted observation
    naming the genre's archetypes — this is intentional, a pointer
    for the author to remember which archetypes they're committed to.
    Severity is noted, not advise-review."""
    beats = _full_beat_set()
    story = _full_story()
    obs = verify(story, beats=beats)
    arch_obs = [o for o in obs if o.code == "genre_archetypes_declared"]
    assert len(arch_obs) == 1
    assert arch_obs[0].severity == SEVERITY_NOTED
    assert "the monster" in arch_obs[0].message


def test_verify_no_genre_means_no_archetype_observation():
    """A Story without a declared genre should not surface the genre
    archetypes notice."""
    beats = _full_beat_set()
    story = _full_story(stc_genre_id=None)
    obs = verify(story, beats=beats)
    assert "genre_archetypes_declared" not in _codes(obs)


# ----------------------------------------------------------------------------
# Grouping helpers
# ----------------------------------------------------------------------------


def test_group_by_severity_buckets_correctly():
    obs = verify(StcStory(id="S_empty", title="Empty"))
    by_sev = group_by_severity(obs)
    assert SEVERITY_NOTED in by_sev
    assert SEVERITY_ADVISES_REVIEW in by_sev
    # Empty story has 15 advise-review (unfilled slots) + 1 noted (theme).
    assert len(by_sev[SEVERITY_ADVISES_REVIEW]) == 15
    assert len(by_sev[SEVERITY_NOTED]) == 1


def test_group_by_code_buckets_correctly():
    obs = verify(StcStory(id="S_empty", title="Empty"))
    by_code = group_by_code(obs)
    assert by_code["beat_slot_unfilled"]
    assert by_code["theme_statement_empty"]


# ----------------------------------------------------------------------------
# COUPLING_DECLARATIONS
# ----------------------------------------------------------------------------


def test_coupling_declarations_use_valid_kinds():
    for d in COUPLING_DECLARATIONS:
        assert d.kind in VALID_COUPLING_KINDS, (
            f"coupling declaration on {d.record_type}.{d.field} "
            f"has invalid kind {d.kind!r}"
        )


def test_coupling_declarations_include_each_record_type():
    """Every record type in the dialect should have at least one
    coupling declaration. Surfaces if a record type is added without
    declaring its coupling shape — the kind of drift that becomes
    silent verifier-coverage gaps later."""
    record_types = {d.record_type for d in COUPLING_DECLARATIONS}
    expected = {"StcStory", "StcBeat", "StcStrand", "StcGenre"}
    missing = expected - record_types
    assert not missing, (
        f"coupling declarations missing record types: {missing}"
    )


def test_coupling_declarations_include_realization_and_claim_kinds():
    """Save the Cat is a Claim-heavy dialect (theme_statement is
    Claim-trajectory, beat description_of_change is Claim-moment, etc.).
    Confirm the declared mix reflects that."""
    kinds = [d.kind for d in COUPLING_DECLARATIONS]
    assert COUPLING_REALIZATION in kinds
    assert COUPLING_CLAIM_TRAJECTORY in kinds
    assert COUPLING_CLAIM_MOMENT in kinds
    assert COUPLING_CHARACTERIZATION in kinds


# ----------------------------------------------------------------------------
# save-the-cat-sketch-02 (S9-S13 — StcCharacter amendment)
# ----------------------------------------------------------------------------


# S9 / S10 — StcCharacter + canonical role labels


def test_stc_character_constructs_with_minimal_fields():
    c = StcCharacter(id="C1", name="Test")
    assert c.id == "C1"
    assert c.name == "Test"
    assert c.role_labels == ()


def test_stc_character_role_labels_is_tuple_not_set():
    """S9 requires role_labels to preserve author-declared ordering;
    tuple (not frozenset) is the substrate shape."""
    c = StcCharacter(
        id="C1", name="Test",
        role_labels=("protagonist", "antagonist", "narrator"),
    )
    assert c.role_labels == ("protagonist", "antagonist", "narrator")
    # Order is preserved even when labels duplicate in other directions.
    assert c.role_labels[0] == "protagonist"
    assert c.role_labels[-1] == "narrator"


def test_canonical_role_labels_include_expected_vocabulary():
    """S10: the canonical role labels ship as a named vocabulary the
    verifier recognizes."""
    expected = {
        "protagonist", "antagonist", "love-interest", "mentor",
        "confidant", "ally", "narrator", "victim", "suspect",
        "threshold-guardian",
    }
    assert set(CANONICAL_ROLE_LABELS) == expected
    assert CANONICAL_ROLE_LABEL_SET == frozenset(expected)


def test_stc_character_admits_open_string_role_labels():
    """S10: canonical labels are recognized, not required. Open
    strings are admissible for per-genre archetypes and the long
    tail."""
    c = StcCharacter(
        id="C_poirot", name="Poirot",
        role_labels=("the detective",),  # Whydunit archetype, open string
    )
    assert "the detective" in c.role_labels


# S11 — reference wiring


def test_stc_beat_participant_ids_defaults_empty():
    """S11: the new participant_ids field defaults to empty so
    sketch-01 encodings verify cleanly without migration."""
    b = StcBeat(id="B1", slot=1, page_actual=1)
    assert b.participant_ids == ()


def test_stc_beat_carries_participant_ids():
    b = StcBeat(
        id="B1", slot=1, page_actual=1,
        participant_ids=("C1", "C2"),
    )
    assert b.participant_ids == ("C1", "C2")


def test_stc_strand_focal_character_id_defaults_none():
    """S11: focal_character_id defaults to None; strands that don't
    declare a focal character still verify."""
    s = StcStrand(id="S1", kind=StrandKind.A_STORY)
    assert s.focal_character_id is None


def test_stc_strand_focal_character_id_carries():
    s = StcStrand(
        id="S1", kind=StrandKind.A_STORY, focal_character_id="C1",
    )
    assert s.focal_character_id == "C1"


def test_stc_story_character_and_archetype_fields_default_empty():
    """S11 / S12: new Story fields default to empty tuples so
    sketch-01 encodings are unaffected."""
    s = StcStory(id="S", title="T")
    assert s.character_ids == ()
    assert s.archetype_assignments == ()


# S13 — character-id resolution


def test_verify_flags_unresolved_story_character_id():
    chars = (StcCharacter(id="C1", name="A", role_labels=("protagonist",)),)
    story = _full_story(
        character_ids=("C1", "C_nonexistent"),
    )
    obs = verify(story, beats=_full_beat_set(), characters=chars)
    codes = _codes(obs)
    assert "character_id_unresolved" in codes


def test_verify_flags_unresolved_participant_id():
    chars = (StcCharacter(id="C1", name="A", role_labels=("protagonist",)),)
    # Rebuild the beat set so one beat references a character.
    beats = list(_full_beat_set())
    beats[0] = StcBeat(
        id=beats[0].id, slot=1, page_actual=beats[0].page_actual,
        participant_ids=("C_nonexistent",),
    )
    beats = tuple(beats)
    story = _full_story(
        beat_ids=tuple(b.id for b in beats),
        character_ids=tuple(c.id for c in chars),
    )
    obs = verify(story, beats=beats, characters=chars)
    codes = _codes(obs)
    assert "participant_id_unresolved" in codes


def test_verify_flags_unresolved_focal_character_id():
    chars = (StcCharacter(id="C1", name="A", role_labels=("protagonist",)),)
    strand = StcStrand(
        id="Str1", kind=StrandKind.A_STORY,
        focal_character_id="C_nonexistent",
    )
    story = _full_story(
        strand_ids=("Str1",),
        character_ids=tuple(c.id for c in chars),
    )
    obs = verify(
        story, beats=_full_beat_set(), strands=(strand,), characters=chars,
    )
    codes = _codes(obs)
    assert "focal_character_id_unresolved" in codes


def test_verify_flags_unresolved_archetype_character_id():
    chars = (StcCharacter(id="C1", name="A", role_labels=("protagonist",)),)
    story = _full_story(
        character_ids=tuple(c.id for c in chars),
        stc_genre_id=GENRE_MONSTER_IN_THE_HOUSE.id,
        archetype_assignments=(
            StcArchetypeAssignment(
                archetype="the monster", character_id="C_nonexistent",
            ),
            StcArchetypeAssignment(
                archetype="the house", note="the test house",
            ),
            StcArchetypeAssignment(
                archetype="the sin", note="the test sin",
            ),
        ),
    )
    obs = verify(story, beats=_full_beat_set(), characters=chars)
    codes = _codes(obs)
    assert "archetype_character_id_unresolved" in codes


def test_verify_flags_unreferenced_characters_as_noted():
    """S11: characters declared on the Story but not used anywhere
    surface as NOTED (informational). Here C1 is wired into beat
    B_1 so only C_unref fires."""
    chars = (
        StcCharacter(id="C1", name="A", role_labels=("protagonist",)),
        StcCharacter(id="C_unref", name="B"),
    )
    beats = list(_full_beat_set())
    beats[0] = StcBeat(
        id=beats[0].id, slot=1, page_actual=beats[0].page_actual,
        participant_ids=("C1",),
    )
    beats = tuple(beats)
    story = _full_story(
        beat_ids=tuple(b.id for b in beats),
        character_ids=("C1", "C_unref"),
    )
    obs = verify(story, beats=beats, characters=chars)
    unref = [o for o in obs if o.code == "character_unreferenced"]
    assert len(unref) == 1
    assert unref[0].severity == SEVERITY_NOTED
    assert unref[0].target_id == "C_unref"


# S13 — one-protagonist check


def test_verify_flags_multiple_protagonists_advise_review():
    chars = (
        StcCharacter(id="C1", name="A", role_labels=("protagonist",)),
        StcCharacter(id="C2", name="B", role_labels=("protagonist",)),
    )
    beats = list(_full_beat_set())
    beats[0] = StcBeat(
        id=beats[0].id, slot=1, page_actual=beats[0].page_actual,
        participant_ids=("C1", "C2"),
    )
    beats = tuple(beats)
    story = _full_story(
        beat_ids=tuple(b.id for b in beats),
        character_ids=tuple(c.id for c in chars),
    )
    obs = verify(story, beats=beats, characters=chars)
    multi = [o for o in obs if o.code == "multiple_protagonists"]
    assert len(multi) == 1
    assert multi[0].severity == SEVERITY_ADVISES_REVIEW


def test_verify_flags_no_protagonist_declared_as_noted():
    chars = (StcCharacter(id="C1", name="A", role_labels=("confidant",)),)
    beats = list(_full_beat_set())
    beats[0] = StcBeat(
        id=beats[0].id, slot=1, page_actual=beats[0].page_actual,
        participant_ids=("C1",),
    )
    beats = tuple(beats)
    story = _full_story(
        beat_ids=tuple(b.id for b in beats),
        character_ids=tuple(c.id for c in chars),
    )
    obs = verify(story, beats=beats, characters=chars)
    no_prot = [o for o in obs if o.code == "no_protagonist_declared"]
    assert len(no_prot) == 1
    assert no_prot[0].severity == SEVERITY_NOTED


# S13 — archetype coverage


def test_verify_flags_archetype_missing():
    chars = (StcCharacter(id="C1", name="A", role_labels=("protagonist",)),)
    beats = list(_full_beat_set())
    beats[0] = StcBeat(
        id=beats[0].id, slot=1, page_actual=beats[0].page_actual,
        participant_ids=("C1",),
    )
    beats = tuple(beats)
    story = _full_story(
        beat_ids=tuple(b.id for b in beats),
        character_ids=tuple(c.id for c in chars),
        archetype_assignments=(
            # Only one of Monster-in-the-House's three archetypes.
            StcArchetypeAssignment(archetype="the monster", note="x"),
        ),
    )
    obs = verify(story, beats=beats, characters=chars)
    missing = [o for o in obs if o.code == "archetype_missing"]
    assert len(missing) == 2  # "the house" and "the sin" missing


def test_verify_flags_archetype_duplicated():
    story = _full_story(
        archetype_assignments=(
            StcArchetypeAssignment(archetype="the monster", note="a"),
            StcArchetypeAssignment(archetype="the monster", note="b"),
            StcArchetypeAssignment(archetype="the house", note="c"),
            StcArchetypeAssignment(archetype="the sin", note="d"),
        ),
    )
    obs = verify(story, beats=_full_beat_set())
    dup = [o for o in obs if o.code == "archetype_duplicated"]
    assert len(dup) == 1


def test_verify_flags_archetype_extraneous():
    story = _full_story(
        archetype_assignments=(
            StcArchetypeAssignment(archetype="the monster", note="a"),
            StcArchetypeAssignment(archetype="the house", note="b"),
            StcArchetypeAssignment(archetype="the sin", note="c"),
            StcArchetypeAssignment(
                archetype="not-a-real-archetype", note="d",
            ),
        ),
    )
    obs = verify(story, beats=_full_beat_set())
    extra = [o for o in obs if o.code == "archetype_extraneous"]
    assert len(extra) == 1


def test_verify_flags_archetype_assignment_both_set():
    chars = (StcCharacter(id="C1", name="A", role_labels=("protagonist",)),)
    beats = list(_full_beat_set())
    beats[0] = StcBeat(
        id=beats[0].id, slot=1, page_actual=beats[0].page_actual,
        participant_ids=("C1",),
    )
    beats = tuple(beats)
    story = _full_story(
        beat_ids=tuple(b.id for b in beats),
        character_ids=tuple(c.id for c in chars),
        archetype_assignments=(
            StcArchetypeAssignment(
                archetype="the monster", character_id="C1", note="bad",
            ),
            StcArchetypeAssignment(archetype="the house", note="h"),
            StcArchetypeAssignment(archetype="the sin", note="s"),
        ),
    )
    obs = verify(story, beats=beats, characters=chars)
    both = [o for o in obs if o.code == "archetype_assignment_both_set"]
    assert len(both) == 1


def test_verify_flags_archetype_assignment_neither_set():
    story = _full_story(
        archetype_assignments=(
            StcArchetypeAssignment(archetype="the monster"),  # neither
            StcArchetypeAssignment(archetype="the house", note="h"),
            StcArchetypeAssignment(archetype="the sin", note="s"),
        ),
    )
    obs = verify(story, beats=_full_beat_set())
    neither = [
        o for o in obs if o.code == "archetype_assignment_neither_set"
    ]
    assert len(neither) == 1


def test_verify_flags_archetype_assignments_without_genre():
    """If the Story declares archetype_assignments but no genre,
    the assignments can't be validated against any archetype set —
    surface the smell."""
    beats = _full_beat_set()
    story = StcStory(
        id="S", title="T",
        theme_statement="test theme",
        stc_genre_id=None,
        beat_ids=tuple(b.id for b in beats),
        archetype_assignments=(
            StcArchetypeAssignment(archetype="foo", note="bar"),
        ),
    )
    obs = verify(story, beats=beats)
    codes = _codes(obs)
    assert "archetype_assignments_without_genre" in codes


# Integration pins — both migrated encodings verify cleanly (1 NOTED only)


def test_ackroyd_save_the_cat_verifies_with_one_noted_observation():
    """Post-sketch-02 Ackroyd STC: same observation shape as pre-
    sketch-02 (1 NOTED `genre_archetypes_declared`); no new adverse
    observations introduced by the StcCharacter amendment."""
    from ackroyd_save_the_cat import STORY, BEATS, STRANDS, CHARACTERS
    obs = verify(
        STORY, beats=BEATS, strands=STRANDS, characters=CHARACTERS,
    )
    advises = [o for o in obs if o.severity == SEVERITY_ADVISES_REVIEW]
    assert advises == [], (
        f"Ackroyd STC should have no advise-review observations; "
        f"got {[o.code for o in advises]}"
    )
    noteds = [o for o in obs if o.severity == SEVERITY_NOTED]
    assert len(noteds) == 1
    assert noteds[0].code == "genre_archetypes_declared"


def test_macbeth_save_the_cat_verifies_with_one_noted_observation():
    """Post-sketch-02 Macbeth STC: same shape as pre-sketch-02."""
    from macbeth_save_the_cat import STORY, BEATS, STRANDS, CHARACTERS
    obs = verify(
        STORY, beats=BEATS, strands=STRANDS, characters=CHARACTERS,
    )
    advises = [o for o in obs if o.severity == SEVERITY_ADVISES_REVIEW]
    assert advises == [], (
        f"Macbeth STC should have no advise-review observations; "
        f"got {[o.code for o in advises]}"
    )
    noteds = [o for o in obs if o.severity == SEVERITY_NOTED]
    assert len(noteds) == 1
    assert noteds[0].code == "genre_archetypes_declared"


def test_sheppard_carries_three_canonical_role_labels():
    """The load-bearing structural claim of sketch-02 on Ackroyd: a
    single character carrying protagonist + antagonist + narrator
    simultaneously. This is what the amendment was written to make
    expressible."""
    from ackroyd_save_the_cat import C_sheppard
    assert "protagonist" in C_sheppard.role_labels
    assert "antagonist" in C_sheppard.role_labels
    assert "narrator" in C_sheppard.role_labels


def test_macbeth_archetype_assignments_use_prose_notes_only():
    """Rites of Passage's archetypes are internal stages, not
    characters. The Macbeth encoding binds all three via prose
    notes — the sketch-02 signal for 'genre archetypes are not
    character-shaped on this material.'"""
    from macbeth_save_the_cat import STORY
    assert len(STORY.archetype_assignments) == 3
    for aa in STORY.archetype_assignments:
        assert aa.character_id is None
        assert aa.note  # non-empty prose note


def test_ackroyd_archetype_assignments_mix_character_and_prose():
    """Whydunit's three archetypes split: one character ('the
    detective' → Poirot), two prose notes ('the secret', 'the
    dark turn'). The sketch-02 signal for 'genre archetypes split
    cleanly on this material.'"""
    from ackroyd_save_the_cat import STORY
    by_arch = {aa.archetype: aa for aa in STORY.archetype_assignments}
    assert by_arch["the detective"].character_id == "C_poirot"
    assert by_arch["the detective"].note == ""
    assert by_arch["the secret"].character_id is None
    assert by_arch["the secret"].note
    assert by_arch["the dark turn"].character_id is None
    assert by_arch["the dark turn"].note


# ----------------------------------------------------------------------------
# Test runner
# ----------------------------------------------------------------------------


TESTS = [
    # Canonical beat sheet
    test_canonical_beats_has_fifteen_entries,
    test_canonical_beats_slot_positions_are_1_to_15,
    test_canonical_beat_names_match_snyder,
    test_canonical_beat_lookup_by_slot,
    # Genres
    test_genres_count_is_ten,
    test_genre_by_id_lookup,
    test_each_genre_carries_archetypes,
    # StcBeat
    test_stc_beat_valid_slot_constructs,
    test_stc_beat_slot_zero_raises,
    test_stc_beat_slot_sixteen_raises,
    test_stc_beat_advances_default_empty,
    test_stc_beat_carries_strand_advancements,
    # StcStrand
    test_stc_strand_kind_enum,
    # verify — empty
    test_verify_empty_story_flags_all_unfilled_slots_plus_empty_theme,
    # verify — full
    test_verify_full_story_with_monotonic_pages_is_minimal,
    # verify — individual codes
    test_verify_flags_theme_statement_empty,
    test_verify_flags_theme_statement_whitespace_only,
    test_verify_flags_beat_id_unresolved,
    test_verify_flags_strand_id_unresolved,
    test_verify_flags_genre_unknown,
    test_verify_flags_beat_slot_unfilled_for_specific_slots,
    test_verify_flags_multiple_beats_per_slot,
    test_verify_flags_page_actual_non_monotonic,
    test_verify_flags_multiple_a_strands,
    test_verify_flags_multiple_b_strands,
    test_verify_flags_advancement_strand_unresolved,
    test_verify_genre_archetypes_declared_is_informational,
    test_verify_no_genre_means_no_archetype_observation,
    # Grouping
    test_group_by_severity_buckets_correctly,
    test_group_by_code_buckets_correctly,
    # COUPLING_DECLARATIONS
    test_coupling_declarations_use_valid_kinds,
    test_coupling_declarations_include_each_record_type,
    test_coupling_declarations_include_realization_and_claim_kinds,
    # save-the-cat-sketch-02 S9-S13 (StcCharacter amendment)
    test_stc_character_constructs_with_minimal_fields,
    test_stc_character_role_labels_is_tuple_not_set,
    test_canonical_role_labels_include_expected_vocabulary,
    test_stc_character_admits_open_string_role_labels,
    test_stc_beat_participant_ids_defaults_empty,
    test_stc_beat_carries_participant_ids,
    test_stc_strand_focal_character_id_defaults_none,
    test_stc_strand_focal_character_id_carries,
    test_stc_story_character_and_archetype_fields_default_empty,
    test_verify_flags_unresolved_story_character_id,
    test_verify_flags_unresolved_participant_id,
    test_verify_flags_unresolved_focal_character_id,
    test_verify_flags_unresolved_archetype_character_id,
    test_verify_flags_unreferenced_characters_as_noted,
    test_verify_flags_multiple_protagonists_advise_review,
    test_verify_flags_no_protagonist_declared_as_noted,
    test_verify_flags_archetype_missing,
    test_verify_flags_archetype_duplicated,
    test_verify_flags_archetype_extraneous,
    test_verify_flags_archetype_assignment_both_set,
    test_verify_flags_archetype_assignment_neither_set,
    test_verify_flags_archetype_assignments_without_genre,
    test_ackroyd_save_the_cat_verifies_with_one_noted_observation,
    test_macbeth_save_the_cat_verifies_with_one_noted_observation,
    test_sheppard_carries_three_canonical_role_labels,
    test_macbeth_archetype_assignments_use_prose_notes_only,
    test_ackroyd_archetype_assignments_mix_character_and_prose,
]


def main() -> int:
    passed = 0
    failed = 0
    for test in TESTS:
        try:
            test()
        except AssertionError as e:
            print(f"FAIL  {test.__name__}")
            print(f"      {e}")
            failed += 1
            continue
        except Exception:
            print(f"ERROR {test.__name__}")
            traceback.print_exc()
            failed += 1
            continue
        print(f"ok    {test.__name__}")
        passed += 1

    print()
    print(f"{passed} passed, {failed} failed, {len(TESTS)} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
