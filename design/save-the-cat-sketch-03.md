# Save the Cat dialect — sketch 03 (compilation-surface instantiation: S14 extensions + S15 preferences)

**Status:** draft, active
**Date:** 2026-04-21
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [save-the-cat-sketch-01](save-the-cat-sketch-01.md), [save-the-cat-sketch-02](save-the-cat-sketch-02.md) — S1–S13 unchanged
**Frames:** [dialect-compilation-surface-sketch-01](dialect-compilation-surface-sketch-01.md) — second concrete instantiation of DCS1's two-sided surface (first was [aristotelian-sketch-04](aristotelian-sketch-04.md)); forces DOQ2 (cross-dialect symmetry) to fire; [compilation-sketch-01](compilation-sketch-01.md) — S14 fields flow to stages 1–3, S15 fields flow to stage 4 only
**Related:** `prototype/story_engine/encodings/macbeth_save_the_cat.py` — the worked-example payload below; `aristotelian-sketch-04` — the first per-dialect DCS instantiation whose axes this sketch either mirrors or diverges from; `project_dialect_compilation_surface.md` (memory)
**Superseded by:** nothing yet

## Purpose

Second concrete application of `dialect-compilation-surface-sketch-01`'s two-sided surface. Applies DCS1's hard/soft cut to the Save the Cat dialect:

- **S14** — Save the Cat's instantiation of DCS1 side 1 (hard structural extensions). Three first-member flavors: `page_target_tolerance` (positional bound), `co_presence_required_at_slot` (locality at slot), `strand_convergence_required_at_slot` (strand-presence at slot).
- **S15** — Save the Cat's instantiation of DCS1 side 2 (soft preference annotations). Three first-member flavors: `tonal_register`, `genre_adherence_preference`, `slot_emphasis_preference`.
- **S16** — Three new verifier checks covering S14's three flavors (S16.1, S16.2, S16.3). S15 fields get no verifier coverage per DCS3.

The architectural commitment is the *surface itself* (S14 and S15). The flavors are first members; each surface admits more flavors without sketch-amendment, the way sketch-01 S10's role labels are canonical-plus-open.

This is also the **forcing-function run for DOQ2** (`dialect-compilation-surface-sketch-01` cross-dialect symmetry). The "DOQ2 judgment" section below is the explicit outcome: which axes overlap with Aristotelian's A15/A16, which don't, and what that says about globalizing any flavor vocabulary.

## Why now

`aristotelian-sketch-04` committed the first per-dialect DCS instantiation. Per DCS5, flavor taxonomies are dialect-local by default; per DOQ2, cross-dialect symmetry reopens once a second dialect grows its surface. Save the Cat is the right second target because:

1. **Schema-landed already.** Save the Cat has a Tier-1 schema directory (`schema/save_the_cat/`); Dramatic and Dramatica-template do not. Mirror `aristotelian-sketch-04`'s three-commit arc (design → Python → schema landing) cleanly without first needing to land a fresh Tier-1 schema.
2. **Structurally distinct from Aristotelian.** Beat-driven vs phase-driven; page-positioned vs τ_s-indexed; 15 fixed canonical slots vs open event sequence; A/B strand bifurcation vs unified mythos. Enough architectural distance that overlap — where it appears — is meaningful evidence, not an artifact of shared vocabulary.
3. **Middle-weight dialect.** Bigger than Aristotelian in conceptual scope (15 canonical slots, 10 genres × 3 archetypes), smaller than Dramatica-complete (the deep end). Right size to stress DOQ2 without the second instantiation becoming a project in itself.

Macbeth is the obvious worked-example payload: the only encoding that exists at both Aristotelian (`macbeth_aristotelian.py`) and Save the Cat (`macbeth_save_the_cat.py`). Cross-dialect reading of the same material lets the flavors be judged against a shared reference text. Sketch-02's character layer is already wired on the Save the Cat Macbeth encoding, so S14-SE2 and S14-SE3 have concrete ids to reference from day one.

## Scope — what this sketch does and doesn't do

**In scope:**

- Two new architectural commitments (S14 + S15) instantiating DCS1 sides 1 and 2 for Save the Cat.
- Three first-member flavors per side, each with field shape, semantics, and Macbeth worked-example values.
- Three new verifier checks (S16.1, S16.2, S16.3) covering S14's three flavors.
- Explicit **DOQ2 judgment**: per-axis overlap analysis against Aristotelian's A15/A16, with globalization recommendations.
- Optionality discipline (every flavor optional; pre-sketch-03 encodings verify identically).
- Verifier-signature check: do S14 flavors require new `verify` kwargs? Answer: no — every S14 flavor lives on existing record types (`StcStory` or `StcBeat`).

**Out of scope:**

- Implementation (Python dataclass field additions; S16.1–S16.3 functions; encoding migrations). Follows in a separate "implement" commit, mirroring `aristotelian-sketch-04` → `0ab7660`.
- Schema-layer landing (`schema/save_the_cat/*.json` amendments). Production-format-sketch follows; gated on this design.
- Migration of `ackroyd_save_the_cat.py` to use S14 + S15 fields. Pre-sketch-03 encodings stay unchanged; only Macbeth receives worked-example values. Ackroyd may opt in later if its encoding presses for it.
- Probe-client rendering of S14 + S15 fields. Save the Cat doesn't currently have a probe surface analogous to Aristotelian's; if it grows one, DOQ-STC3-4 below banks the question.
- Compile-time overlay schema (DCS6 / DOQ3). Not STC-specific; lives in compilation-sketch-02.
- Side-2 ranker consumption. Stage 4 of compilation is not implemented; S15 fields are authored-but-not-yet-consumed by design.
- Globalizing any flavor vocabulary. DOQ2 judgment may recommend future globalization; this sketch does not commit any field to a cross-dialect schema.

## Commitments

Labels S14–S16 continue sketches 01–02's S1–S13 numbering. S16 opens a new family for compilation-surface verifier checks (parallel to how Aristotelian's A7.12–A7.14 extended A7).

### S14 — Side-1 hard structural extensions surface

Per DCS1, S14 commits the Save the Cat dialect to carry hard-constraint fields that flow through `compilation-sketch-01`'s stages 1–3. Three first-member flavors:

#### S14-SE1 — `page_target_tolerance` on `StcBeat` (positional tolerance)

```python
@dataclass(frozen=True)
class StcBeat:
    # ... existing fields unchanged ...
    page_tolerance_before: int = 0  # 0 = use canonical page_target strictly
    page_tolerance_after: int = 0   # 0 = use canonical page_target strictly
```

**Semantics.** Hard constraint: when both bounds are non-zero, `canonical_page_target - page_tolerance_before ≤ page_actual ≤ canonical_page_target + page_tolerance_after`. When only `page_tolerance_before > 0` and `page_tolerance_after == 0`, only the early-side tolerance binds. Symmetric for late-side-only. When both are 0 (default), the field carries no constraint and pre-sketch-03 beats verify identically.

**Relation to sketch-01 S2 / the existing `page_actual_non_monotonic` check.** S2's monotonicity check is *ordering* — beats in slot order must have increasing `page_actual`. S14-SE1 is *positional* — each beat's `page_actual` is bounded around its own canonical target. The two are orthogonal: a beat can be monotonic but outside its canonical window (signals an unusually-shaped encoding); or within its window but non-monotonic (signals a structural inversion). Both observations are worth surfacing.

**Compiler use.** Stage 1 extracts to per-beat positional constraints. Stage 2 (feasibility) folds into the overall page-budget calculation. Stage 3 (planner) treats the bounds as preconditions on beat-emission positioning — the beat cannot be placed outside its tolerance window.

**Verifier (S16.1) responsibility.** Structural consistency only: tolerances non-negative; if both set, `page_actual` falls within the tolerance window around the beat's canonical `page_target` (looked up via `CANONICAL_BEAT_BY_SLOT[slot].page_target`).

**Why dialect-specific.** Page-target tolerance is Save the Cat's own because `page_target` is STC's positional coordinate. No Aristotelian analog at the field level, though the *shape* (arithmetic bound around a canonical position) parallels A15-SE1's min/max count.

**Macbeth values (worked example):**

```python
# Macbeth's beat pages are proportional against a 110-page screenplay;
# the play is stage material. Authorial tolerance wider than Snyder's
# tight commercial-screenplay expectations.

B_01_opening = StcBeat(
    # ... existing fields ...
    page_actual=1,                       # canonical 1
    page_tolerance_before=0,             # can't go earlier than page 1
    page_tolerance_after=3,              # NEW (S14-SE1)
)
B_04_catalyst = StcBeat(
    # ... existing fields ...
    page_actual=12,                      # canonical 12
    page_tolerance_before=5,             # NEW (S14-SE1)
    page_tolerance_after=5,              # NEW (S14-SE1)
)
B_09_midpoint = StcBeat(
    # ... existing fields ...
    page_actual=55,                      # canonical 55 (exact)
    page_tolerance_before=8,             # NEW — midpoint's load-bearing
    page_tolerance_after=8,              # NEW — but some drift admissible
)
B_14_finale = StcBeat(
    # ... existing fields ...
    page_actual=95,                      # canonical 85; already outside default
    page_tolerance_before=10,            # NEW — widen to accommodate
    page_tolerance_after=5,              # NEW
)
B_15_final_image = StcBeat(
    # ... existing fields ...
    page_actual=110,                     # canonical 110
    page_tolerance_before=2,
    page_tolerance_after=0,              # can't overshoot end
)
```

Five beats receive tolerance values; the other ten stay at default 0 (no tolerance, implying author intends the canonical target for those). Macbeth's `B_14_finale` at page 95 sits outside its canonical 85 target; S14-SE1 lets the encoding declare "this is intentional drift, within ±10 pages" rather than the verifier silently accepting the discrepancy.

#### S14-SE2 — `co_presence_required_at_slot` on `StcStory` (character locality at slot)

```python
@dataclass(frozen=True)
class StcCoPresenceRequirement:
    """S14-SE2 (sketch-03). Hard constraint: the named characters must
    all appear in participant_ids of at least min_count authored beats
    whose slot equals the named slot.

    Distinct from sketch-02's S13 character-id resolution (which checks
    that references resolve) — S14-SE2 is a structural *presence claim*
    across slot positions, not a reference-integrity check."""
    id: str
    character_ref_ids: Tuple[str, ...]  # ≥ 2
    slot: int                            # 1..15
    min_count: int = 1


@dataclass(frozen=True)
class StcStory:
    # ... existing fields unchanged ...
    co_presence_requirements: Tuple[StcCoPresenceRequirement, ...] = ()
```

**Semantics.** Hard constraint: for each requirement, ≥ `min_count` authored beats with matching slot must have all named `character_ref_ids` in their `participant_ids`. The requirement is on slot-scoped *beat-level* co-presence, not on substrate locations (STC has no substrate coordinate directly; location-in-story is represented by beat participation).

**Compiler use.** Stage 1 extracts to per-beat participant preconditions. Stage 3 (planner) treats co-presence as a precondition on beat generation — the planner must emit at least `min_count` beats at that slot whose participants cover the requirement. CS6 fires if no plan simultaneously satisfies all co-presence requirements.

**Verifier (S16.2) responsibility.** Structural consistency: `len(character_ref_ids) ≥ 2`; all characters resolve in `story.character_ids` (and by extension the characters collection); `1 ≤ slot ≤ 15`; `min_count ≥ 1`. Whether the authored beats actually carry the participants is a further check — S16.2 verifies participation against current authoring as well.

**Why this is the axis of strongest cross-dialect overlap.** Aristotelian's A15-SE2 carries essentially the same architectural shape: a tuple of requirements, each naming ≥2 characters and a structural position (phase for Aristotelian, slot for STC), with `min_count`. The field name mirrors exactly (`co_presence_requirements`). The record-type name differs by prefix convention only (`ArCoPresenceRequirement` vs `StcCoPresenceRequirement`). **This is the DOQ2 evidence for globalization on the co-presence axis** — see DOQ2 judgment section.

**Macbeth values (worked example):**

```python
MACBETH_STC_CO_PRESENCE = (
    StcCoPresenceRequirement(
        id="copres_macbeth_witches_catalyst",
        character_ref_ids=("C_macbeth", "C_witches"),
        slot=4,  # Catalyst — prophecy delivery requires both present
        min_count=1,
    ),
    StcCoPresenceRequirement(
        id="copres_macbeth_lady_debate",
        character_ref_ids=("C_macbeth", "C_lady_macbeth"),
        slot=5,  # Debate — the debate is structurally a two-person scene
        min_count=1,
    ),
    StcCoPresenceRequirement(
        id="copres_macbeth_macduff_finale",
        character_ref_ids=("C_macbeth", "C_macduff"),
        slot=14,  # Finale — antagonist confrontation
        min_count=1,
    ),
)
# Threaded into STORY via co_presence_requirements=MACBETH_STC_CO_PRESENCE
```

Three structurally load-bearing co-presence claims. Each maps to a scene whose structural weight in Macbeth depends on exactly those characters being present. All three are satisfiable against the existing `participant_ids` authoring in `macbeth_save_the_cat.py` (verified in implement-phase testing).

#### S14-SE3 — `strand_convergence_required_at_slot` on `StcStory` (strand-presence at slot)

```python
@dataclass(frozen=True)
class StcStrandConvergenceRequirement:
    """S14-SE3 (sketch-03). Hard constraint: at the named slot, each
    strand named in strand_ref_ids must be advanced (appear in at least
    one authored beat's `advances`) by at least one beat in that slot.

    The typical Save-the-Cat use: assert that A and B stories both
    advance at slot 9 (Midpoint) and slot 14 (Finale) — Snyder's
    'A and B collide' and 'A and B resolve together' conventions."""
    id: str
    strand_ref_ids: Tuple[str, ...]  # ≥ 2 (otherwise trivially satisfied)
    slot: int                         # 1..15


@dataclass(frozen=True)
class StcStory:
    # ... existing fields unchanged ...
    strand_convergence_requirements: Tuple[
        StcStrandConvergenceRequirement, ...
    ] = ()
```

**Semantics.** Hard constraint: for each requirement, every strand named in `strand_ref_ids` must be advanced at the named slot — i.e., at least one authored beat with matching slot has a `StrandAdvancement` for each named strand. The constraint asserts *simultaneous strand activity* at a structural position.

**Compiler use.** Stage 1 extracts to per-slot strand preconditions. Stage 3 (planner) emits beats whose `advances` collectively cover the requirement. CS6 fires if no plan can arrange simultaneous strand advancement at the required slot.

**Verifier (S16.3) responsibility.** Structural consistency: `len(strand_ref_ids) ≥ 2`; all strands resolve in `story.strand_ids`; `1 ≤ slot ≤ 15`. Whether the authored beats actually carry the advancement is also checked — S16.3 verifies advancement against current authoring.

**Why dialect-specific.** Strands are a Save-the-Cat primitive (A story / B story). Aristotelian has no strand concept at A1–A14; a mythos is unified. The *architectural shape* (arithmetic bound on multi-entity presence at a structural position) echoes A15-SE2's co-presence, but the entity type (strand vs character) is dialect-local. **DOQ2 evidence: shape-overlap without vocabulary-overlap.**

**Macbeth values (worked example):**

```python
MACBETH_STC_STRAND_CONVERGENCE = (
    StcStrandConvergenceRequirement(
        id="converge_macbeth_midpoint",
        strand_ref_ids=("Strand_A_scotland", "Strand_B_marriage"),
        slot=9,  # Midpoint — A (political) and B (marriage) collide
    ),
    StcStrandConvergenceRequirement(
        id="converge_macbeth_finale",
        strand_ref_ids=("Strand_A_scotland", "Strand_B_marriage"),
        slot=14,  # Finale — both resolve together
    ),
)
# Threaded into STORY via strand_convergence_requirements=MACBETH_STC_STRAND_CONVERGENCE
```

Only two requirements. Both represent Snyder's canonical "A+B convergence" beats — the structural claims where the two strands are supposed to be simultaneously active. Each is satisfiable in the current Macbeth STC encoding (`B_09_midpoint` advances only A, but `B_14_finale` advances both A and B). Implementing sketch-03 will *surface* that Macbeth's slot-9 encoding advances only A — an S16.3 observation that may prompt re-authoring or affirmative acceptance (Macbeth's midpoint stress is in the A plot; B-strand advancement at slot 9 is encoded implicitly but not authored as a `StrandAdvancement`). This is a valuable probe into the encoding's structural precision.

### S15 — Side-2 soft preference annotations surface

Per DCS1, S15 commits the Save the Cat dialect to carry preference-annotation fields that flow only to `compilation-sketch-01` stage 4. No verifier coverage (DCS3). Three first-member flavors:

#### S15-SP1 — `tonal_register` on `StcStory` (tonal preference)

```python
@dataclass(frozen=True)
class StcStory:
    # ... existing fields unchanged ...
    tonal_register: str = ""
```

**Semantics.** Single string from a controlled-but-open vocabulary. Initial controlled set: `{tragic, comedic, thriller, elevated, grounded, hybrid}`. Empty string (default) is neutral — ranker has no tonal preference signal.

**Ranker use.** Stage 4 ranker reads `tonal_register` as a scoring rubric input. Specific scoring algorithm is OQ4 (compilation-sketch-01); S15-SP1 commits to the *input language*, not the scoring.

**Vocabulary discipline.** Canonical-plus-open like sketch-02's S10 role labels.

**Field-name choice is deliberate.** Aristotelian's A16-SP1 is also named `tonal_register`. Using the same field name (with different vocabulary per dialect) is the clearest DOQ2 signal: **tonal register is an axis on which cross-dialect symmetry is plausible**. The vocabularies overlap on `tragic` / `tragic-pure` / `tragic-with-irony`; diverge on `comedic` (absent from Aristotelian) and `elegiac` (absent from STC); `elevated` and `classical` overlap in spirit. See DOQ2 judgment.

**Macbeth value:** `tonal_register="tragic"` — captures the play's unified-tragic register without the Hamlet-specific "tragic-with-irony" note. Macbeth's tragedy is relentless rather than reflexively ironic; the vocabulary choice is load-bearing.

#### S15-SP2 — `genre_adherence_preference` on `StcStory` (ranker-objective preference)

```python
@dataclass(frozen=True)
class StcStory:
    # ... existing fields unchanged ...
    genre_adherence_preference: str = ""
```

**Semantics.** Single string from `{strict, loose, inventive, genre-bending, ""}`. Empty string is neutral. The preference biases stage-4 ranker toward candidates that hew tightly to the declared genre's archetypes (`strict`) vs those that stretch them (`inventive`, `genre-bending`).

**Ranker use.** Stage 4 ranker computes per-candidate conformance to the declared genre's `archetypes` (from sketch-01 S5 / sketch-02 S12). Algorithm is OQ4.

**Why STC-specific.** Genre is a Save-the-Cat primitive (S5). Aristotelian has no genre layer; its A16-SP2 (`binding_distance_preference`) is about peripeteia↔anagnorisis distance — a structural feature of Aristotelian's dramatic shape that has no STC analog. **DOQ2 evidence: ranker-objective preferences are structurally dialect-local; field names and vocabularies diverge.**

**Macbeth value:** `genre_adherence_preference="loose"` — Macbeth's Rites-of-Passage framing is honest but imperfect (see `macbeth_save_the_cat.py` docstring). `loose` declares "the encoding knows the genre fit is a stretch; rank accordingly." An `inventive` or `genre-bending` reading would be defensible too; `loose` is the middle choice.

#### S15-SP3 — `slot_emphasis_preference` on `StcBeat` (emphasis/pacing preference)

```python
@dataclass(frozen=True)
class StcBeat:
    # ... existing fields unchanged ...
    emphasis_preference: str = ""
```

**Semantics.** Single string from `{minimal, standard, expanded, centerpiece, ""}`. Empty string is neutral. The preference biases stage-4 ranker toward allocating more (`expanded`, `centerpiece`) or less (`minimal`) prose real-estate to this beat relative to its canonical weight.

**Ranker use.** Stage 4 ranker consumes `emphasis_preference` as a per-beat scaling factor when allocating the overall word budget across beats. Algorithm is OQ4.

**Relation to Aristotelian's A16-SP3.** Aristotelian's `pacing_preference` is per-phase; STC's `emphasis_preference` is per-beat. Both are **per-structural-unit pacing/emphasis preferences** — shape-overlap with different granularity. Field names differ (`pacing_preference` vs `emphasis_preference`); vocabularies differ (Aristotelian's `{slow_burn, even, accelerating, rapid_escalation, decelerating}` vs STC's `{minimal, standard, expanded, centerpiece}`). Aristotelian's vocabulary is about *temporal distribution*; STC's is about *emphasis weight*. Different semantic frames pointing at related ranker concerns.

**Macbeth values (worked example):**

```python
B_02_theme.emphasis_preference          = ""          # neutral — short beat
B_08_fun_and_games.emphasis_preference  = "expanded"  # the regicide is load-bearing
B_09_midpoint.emphasis_preference       = "centerpiece"  # structural pivot
B_11_all_is_lost.emphasis_preference    = "standard"  # Lady Macbeth's death is offstage
B_12_dark_night.emphasis_preference     = "centerpiece"  # 'tomorrow' soliloquy
B_14_finale.emphasis_preference         = "expanded"  # duel + reveal + death
```

Six beats receive emphasis values; the other nine stay at default neutral. The two `centerpiece` annotations mark Macbeth's structural high points — midpoint collision and dark-night soliloquy — as places where the ranker should allocate disproportionate prose real-estate.

### S16 — New verifier check family for S14 flavors

S16 opens a new check family for compilation-surface hard extensions. Three checks, all severity `advises-review` (following sketch-01 S6's observations-never-errors discipline):

#### S16.1 — `page_target_tolerance` consistency (S14-SE1)

For each `StcBeat`:

1. `page_tolerance_before ≥ 0`. Violation: `page_tolerance_before_negative` (advises-review).
2. `page_tolerance_after ≥ 0`. Violation: `page_tolerance_after_negative` (advises-review).
3. If either tolerance > 0: look up canonical `page_target` from `CANONICAL_BEAT_BY_SLOT[slot]`; check `page_target - page_tolerance_before ≤ page_actual ≤ page_target + page_tolerance_after`. Violations: `page_actual_before_tolerance` / `page_actual_after_tolerance` (advises-review). Skips when both tolerances at default 0.

#### S16.2 — `co_presence_required_at_slot` structural integrity (S14-SE2)

For each `StcCoPresenceRequirement` on the story:

1. `len(character_ref_ids) ≥ 2`. Violation: `co_presence_refs_too_few` (advises-review).
2. All `character_ref_ids` resolve in `story.character_ids` (and via that, the characters collection). Violation: `co_presence_character_unresolved` (advises-review).
3. `1 ≤ slot ≤ 15`. Violation: `co_presence_slot_out_of_range` (advises-review).
4. `min_count ≥ 1`. Violation: `co_presence_min_count_zero` (advises-review).
5. **Participation check:** number of authored beats with matching slot whose `participant_ids` contain ALL `character_ref_ids` must be ≥ `min_count`. Violation: `co_presence_insufficient_participation` (advises-review).

Check 5 is the S14-SE2-specific contribution (analog to A7.13 stopping at structural-integrity, but STC beats already have `participant_ids` authored, so we can check participation directly without a compiler-stage gap).

#### S16.3 — `strand_convergence_required_at_slot` structural integrity (S14-SE3)

For each `StcStrandConvergenceRequirement` on the story:

1. `len(strand_ref_ids) ≥ 2`. Violation: `strand_convergence_refs_too_few` (advises-review).
2. All `strand_ref_ids` resolve in `story.strand_ids`. Violation: `strand_convergence_strand_unresolved` (advises-review).
3. `1 ≤ slot ≤ 15`. Violation: `strand_convergence_slot_out_of_range` (advises-review).
4. **Advancement check:** for each strand in `strand_ref_ids`, at least one authored beat with matching slot must have a `StrandAdvancement` with that `strand_id`. Violation: `strand_convergence_missing_advancement` (advises-review; emitted per missing strand).

### Verifier orchestration — verify signature stays unchanged

All S14 fields live on existing record types (`StcStory` or `StcBeat`); S16.1/2/3 walk the existing structures. No new `verify` kwarg. Pre-sketch-03 callers continue to work; S16 checks skip cleanly when fields stay at defaults (empty tuples; tolerances at 0).

`group_by_severity` / `group_by_code` unchanged.

## DOQ2 judgment — cross-dialect symmetry evidence

This is the forcing-function run for `dialect-compilation-surface-sketch-01` DOQ2. With both Aristotelian (A15/A16) and Save-the-Cat (S14/S15) surfaces in hand, we can answer per-axis whether the flavor vocabularies overlap enough to globalize.

### Per-axis comparison

| Axis | Aristotelian | Save-the-Cat | Overlap | Globalization? |
|---|---|---|---|---|
| Character co-presence at structural position | A15-SE2 `co_presence_requirements` on `ArMythos`; record `ArCoPresenceRequirement` with `character_ref_ids`, `phase_id`, `min_count` | S14-SE2 `co_presence_requirements` on `StcStory`; record `StcCoPresenceRequirement` with `character_ref_ids`, `slot`, `min_count` | **Strong.** Same field name; parallel record shape; only positional-reference field differs (`phase_id` vs `slot`) | **Recommend: globalize the record-shape pattern, keep positional-reference dialect-local.** See below. |
| Tonal register | A16-SP1 `tonal_register` on `ArMythos`; `{tragic-pure, tragic-with-irony, elegiac, claustrophobic, classical, modern}` | S15-SP1 `tonal_register` on `StcStory`; `{tragic, comedic, thriller, elevated, grounded, hybrid}` | **Medium-strong.** Same field name, overlapping-but-distinct vocabularies | **Recommend: globalize the field name and open vocabulary; keep canonical sets dialect-local.** See below. |
| Structural positional bound (arithmetic) | A15-SE1 `min_event_count` / `max_event_count` on `ArPhase` (count-based) | S14-SE1 `page_tolerance_before` / `page_tolerance_after` on `StcBeat` (position-based) | **Shape-only.** Both are two-int arithmetic bounds around a structural coordinate; neither positional unit (event-count vs page) nor target (phase's event list vs beat's canonical page) is shared | **Do not globalize.** Pattern is reusable (two-int arithmetic bound around a dialect-local coordinate); shared field names would mislead. |
| Multi-entity presence at structural position | A15-SE2 covers character-presence only | S14-SE3 `strand_convergence_requirements` is strand-presence — an STC-local second member of the multi-entity family | **Shape-only (via S14-SE2).** Aristotelian lacks strands. | **Do not globalize the strand record.** Do note the meta-pattern: "multi-entity-of-kind-K present-at-structural-position-P" is a recurring DCS1 shape. |
| Ranker-objective preference | A16-SP2 `binding_distance_preference` (peripeteia↔anagnorisis distance) | S15-SP2 `genre_adherence_preference` (conformance to genre archetypes) | **None.** Different fields target different dialect-specific structural features | **Do not globalize.** Dialect-local remains correct default. |
| Per-unit pacing/emphasis | A16-SP3 `pacing_preference` on `ArPhase` (temporal distribution) | S15-SP3 `emphasis_preference` on `StcBeat` (word-budget weight) | **Weak.** Both are per-structural-unit preferences feeding ranker; different semantic frames (distribution vs weight) | **Do not globalize.** Too-different semantic frames; might merge later if a stage-4 implementation unifies them. |
| Audience-knowledge timing | A15-SE3 `audience_knowledge_constraints` | *No S14 analog.* STC is not fundamentally about dramatic-irony timing | **None.** | **Dialect-local stays correct.** |

### Globalization recommendations

DOQ2 was a conservative-default: dialect-local unless evidence emerges. The evidence from this spike:

1. **Globalize the co-presence record shape.** Both dialects independently arrived at a tuple of records, each with `character_ref_ids` (tuple of ≥2), a positional-reference field, and `min_count`. The positional-reference differs (`phase_id` vs `slot`), but the rest is identical. **Recommendation:** extract a `CoPresenceRequirement` abstract shape into a shared schema-agnostic module (or document convention); each dialect's concrete record inherits shape but names its positional field per its own coordinate. Field name `co_presence_requirements` on the dialect's root record stays consistent across dialects.

   This is the first globalization candidate DOQ2 admits.

2. **Globalize the `tonal_register` field name and vocabulary convention.** Both dialects named the field identically. The canonical-plus-open vocabulary discipline is the same. Vocabularies differ in specific tokens but share spirit (both include `tragic`; both name a range-of-register scale). **Recommendation:** `tonal_register` is admissible as a cross-dialect field name. Each dialect's canonical vocabulary stays local; authors who move between dialects use the same cognitive field. A future third dialect (Dramatic, Dramatica-template) SHOULD use `tonal_register` if it wants this axis, not a new name.

3. **Do not globalize the positional-bound pattern beyond the two-int shape convention.** Both dialects use two-int arithmetic bounds around a dialect-local structural coordinate (count or page). Field names are dialect-specific and SHOULD be (Aristotelian's `min_event_count/max_event_count` doesn't map onto STC's `page_tolerance_before/after` without losing clarity). **Recommendation:** document the **shape convention** — "two-int arithmetic bound around a dialect-local coordinate" — as a DCS-shape guideline. Don't commit to any field name.

4. **Do not globalize anything else.** The other axes either don't overlap (audience-knowledge, strand-convergence, ranker-objective) or overlap too weakly (per-unit pacing) to make shared names useful.

### What DOQ2 becomes after this judgment

DCS5 stands: dialect-local is the conservative default for the *flavor vocabulary*. DOQ2's open question is answered by *partial globalization on two specific axes* (co-presence record shape; tonal-register field name) with shape conventions for the rest. Neither axis globalization is committed by sketch-03 itself — both are recommendations for a future `dialect-compilation-surface-sketch-02` (or amendment to -01) that formalizes the cross-dialect globalized surfaces.

**Forcing function for any globalization:** a third dialect (Dramatic, Dramatica-template) growing its own DCS surface. If it ALSO independently arrives at co-presence requirements and `tonal_register`, the globalization case goes from 2-of-2 to 3-of-3 and formalization becomes pressing. If it diverges on both, the recommendation relaxes.

## Open questions — banked

### DOQ-STC3-1 — S14-SE3 strand-convergence vs existing multi_a_strands observation

Sketch-01's S6 already surfaces `multiple_a_strands` / `multiple_b_strands` when a story has multiple strands of the same kind. S14-SE3 admits a requirement like `("Strand_A_1", "Strand_A_2")` — convergence between two A strands. Is that admissible? Probably yes (ensemble stories with parallel A plots that converge at the climax), but the interaction with sketch-01's noted observation isn't specified.

**Forcing function:** first encoding with multiple A-kind strands that authors a convergence requirement. Currently no encoding has multiple A-kind strands; banked.

### DOQ-STC3-2 — `emphasis_preference` vs strand emphasis

S15-SP3 is per-beat. An authorial desire like "emphasize the B strand throughout the middle act" isn't directly expressible — it would require marking every middle-act beat that advances B with `emphasis_preference="expanded"`. A strand-level emphasis field (`strand_emphasis_preference` on `StcStrand`) would be a natural extension.

**Forcing function:** first encoding whose authored emphasis pattern is predominantly strand-shaped rather than beat-shaped. Banked.

### DOQ-STC3-3 — Archetype-adherence granularity

S15-SP2 is story-level. An authorial desire like "adhere tightly to the Whydunit 'the detective' archetype but loosely to 'the dark turn'" isn't expressible. Per-archetype-assignment preference would be a natural extension.

**Forcing function:** first encoding whose genre-conformance pattern is sharply uneven across archetypes. Banked.

### DOQ-STC3-4 — Probe rendering of S14 + S15 fields

Save the Cat doesn't currently have a probe client (analogous to Aristotelian's probe-sketch-04). If one is written, it will face the DOQ7 decision concretely — which S14/S15 fields to surface for review. Aristotelian's DOQ-AR4-4 banks the same question for its dialect; STC's decision can be independent.

**Forcing function:** first STC probe client. Banked.

### DOQ-STC3-5 — Compile-time overlay shape for Save the Cat (DOQ3 instantiation)

Per DCS6, the compile-time `hints` input becomes a dialect-overlay. For Save the Cat, the overlay would be a partial `StcStory` carrying S14/S15 overrides. Is the per-beat `emphasis_preference` the natural granularity, or does compile-time override happen at the `StcBeat` level directly (which would require the overlay to carry sub-records)?

**Forcing function:** first compilation with a per-run preference override. Banked.

### DOQ-STC3-6 — Interaction between S14-SE1 tolerance and sketch-01 S2 monotonicity

If S14-SE1 tolerances are loose enough, they could admit `page_actual` sequences that violate S2's monotonicity. Current S2 is independent (checks ordering) and S16.1 is independent (checks positional). But the two together could produce orthogonally-reported conflicts. Is that a feature (two independent signals) or a bug (should they be reconciled into a single combined check)?

**Forcing function:** first authoring where S14-SE1 tolerances admit a monotonicity violation. Banked.

## Worked example — Macbeth under sketch-03

Summary of the fields Macbeth adds under sketch-03:

```python
# In macbeth_save_the_cat.py:

# S14-SE2 module-level tuple
MACBETH_STC_CO_PRESENCE = (
    StcCoPresenceRequirement(
        id="copres_macbeth_witches_catalyst",
        character_ref_ids=("C_macbeth", "C_witches"),
        slot=4,
        min_count=1,
    ),
    StcCoPresenceRequirement(
        id="copres_macbeth_lady_debate",
        character_ref_ids=("C_macbeth", "C_lady_macbeth"),
        slot=5,
        min_count=1,
    ),
    StcCoPresenceRequirement(
        id="copres_macbeth_macduff_finale",
        character_ref_ids=("C_macbeth", "C_macduff"),
        slot=14,
        min_count=1,
    ),
)

# S14-SE3 module-level tuple
MACBETH_STC_STRAND_CONVERGENCE = (
    StcStrandConvergenceRequirement(
        id="converge_macbeth_midpoint",
        strand_ref_ids=("Strand_A_scotland", "Strand_B_marriage"),
        slot=9,
    ),
    StcStrandConvergenceRequirement(
        id="converge_macbeth_finale",
        strand_ref_ids=("Strand_A_scotland", "Strand_B_marriage"),
        slot=14,
    ),
)

# StcBeats gain S14-SE1 tolerances + S15-SP3 emphasis on selected beats
# (see S14-SE1 and S15-SP3 sections for specific values).

# STORY gains S14-SE2/SE3 + S15-SP1/SP2 fields
STORY = StcStory(
    # ... existing fields unchanged ...
    co_presence_requirements=MACBETH_STC_CO_PRESENCE,             # S14-SE2
    strand_convergence_requirements=MACBETH_STC_STRAND_CONVERGENCE,  # S14-SE3
    tonal_register="tragic",                                      # S15-SP1
    genre_adherence_preference="loose",                           # S15-SP2
)
```

Verification under sketch-03 (signature unchanged from sketch-02):

```python
verify(
    STORY,
    beats=BEATS,
    strands=STRANDS,
    characters=CHARACTERS,
)
```

Expected outcome under sketch-03:

- **S16.1** (page-tolerance): five beats have tolerances; all `page_actual` values within their tolerance windows. Clean.
- **S16.2** (co-presence): three requirements.
  - `copres_macbeth_witches_catalyst` — slot 4, `B_04_catalyst` has `participant_ids=("C_witches", "C_macbeth", "C_banquo")` — both witches and Macbeth present. Clean.
  - `copres_macbeth_lady_debate` — slot 5, `B_05_debate` has `participant_ids=("C_macbeth", "C_lady_macbeth")` — both present. Clean.
  - `copres_macbeth_macduff_finale` — slot 14, `B_14_finale` has `participant_ids=("C_macbeth", "C_macduff")` — both present. Clean.
- **S16.3** (strand convergence): two requirements.
  - `converge_macbeth_midpoint` — slot 9, `B_09_midpoint` advances only `Strand_A_scotland`, not `Strand_B_marriage`. **Emits** `strand_convergence_missing_advancement` for `Strand_B_marriage`. **This is the expected observation** — it's the sketch-03 surface surfacing a real structural gap in the existing encoding that the author may want to address (the B strand IS active at the midpoint but not authored as a `StrandAdvancement` — a precision gap).
  - `converge_macbeth_finale` — slot 14, `B_14_finale` advances both strands. Clean.

Expected total S16 observations: **1** (the strand_convergence_missing_advancement for Strand_B_marriage at slot 9).

S15 fields (`tonal_register`, `genre_adherence_preference`, `emphasis_preference`) emit no observations — by DCS3 they are not verifier-coverable.

**Sketch-03's single S16 observation is a feature, not a bug.** It demonstrates that the new surface does real work: it surfaces a structural claim about the encoding (B-strand advancement at midpoint) that was not visible under sketch-02. The author can either re-author `B_09_midpoint` to include a `StrandAdvancement(strand_id="Strand_B_marriage", ...)` (closing the observation) or accept it as an intentional encoding choice (the B strand is PRESENT at midpoint but not structurally ADVANCED — a defensible reading).

## Pre-sketch-03 corpus: Ackroyd

All S14 and S15 fields default to empty / 0 / "". The Ackroyd STC encoding stays unchanged and verifies identically. Authors may opt in incrementally:

- Ackroyd could grow S14-SE2 (Poirot+Sheppard co-presence at slot 14 reveal).
- Ackroyd could grow S15-SP1 (`tonal_register="elevated"` or similar for the Christie-prose register).
- Ackroyd's Whydunit archetypes (`the detective`, `the secret`, `the dark turn`) make S15-SP2 a natural fit — conceivably `genre_adherence_preference="strict"` since Ackroyd IS the archetypal Whydunit.

No migration is committed by sketch-03. Macbeth is the worked-example payload; Ackroyd remains at sketch-02 surface until independent author motivation or probe-back-pressure pushes adoption.

## Architectural classification: extension

New on `StcStory`: four optional fields (`co_presence_requirements`, `strand_convergence_requirements`, `tonal_register`, `genre_adherence_preference`) plus two new dataclass record types (`StcCoPresenceRequirement`, `StcStrandConvergenceRequirement`).

New on `StcBeat`: three optional fields (`page_tolerance_before`, `page_tolerance_after`, `emphasis_preference`).

All defaults are empty / 0 / "". S1–S13 semantics unchanged. The S6 verifier surface grows by three checks (S16.1, S16.2, S16.3); its observations-never-errors discipline is preserved. Verifier signature unchanged. Pre-sketch-03 encodings verify identically.

## Relationship to prior commitments

| Prior | Refined / extended by sketch-03 | How |
|---|---|---|
| `dialect-compilation-surface-sketch-01` DCS1 | Concretized (second time) | S14 + S15 are Save-the-Cat's instantiations of the two-sided surface |
| `dialect-compilation-surface-sketch-01` DCS2 | Concretized | S14 fields flow to stages 1–3; S15 fields flow to stage 4 only |
| `dialect-compilation-surface-sketch-01` DCS3 | Concretized | S16.1–3 cover side 1; side 2 has no checks by construction |
| `dialect-compilation-surface-sketch-01` DCS4 | Honored | All fields default-empty; pre-sketch-03 encodings unchanged |
| `dialect-compilation-surface-sketch-01` DCS5 | Mostly honored | S14 + S15 vocabularies are dialect-local. DOQ2 judgment recommends partial globalization for co-presence-shape and `tonal_register` field-name |
| `dialect-compilation-surface-sketch-01` DOQ1 | Further instantiated | Per-side flavor catalog gets six more concrete members (three per side) |
| `dialect-compilation-surface-sketch-01` DOQ2 | **Partially answered** | Two axes admit globalization (co-presence shape, `tonal_register` name); the rest stay dialect-local. See DOQ2 judgment section |
| `dialect-compilation-surface-sketch-01` DOQ6 | Surfaces again | S14-SE2 (character presence) and S14-SE3 (strand presence) interact with Lowering only if a future Lowering exercise binds participant_ids / advances to substrate |
| `dialect-compilation-surface-sketch-01` DOQ7 | Surfaces concretely as DOQ-STC3-4 | Probe rendering of new surface (STC-specific instantiation) |
| `compilation-sketch-01` OQ4 | Bounded above | S15's three flavors define part of the ranker's input language for Save-the-Cat |
| `compilation-sketch-01` OQ5 | Refined | Hard side 1 vs soft side 2 cut stays concrete per-flavor; sketch-03 adds six more sort decisions, all consistent with DCS1 |
| `aristotelian-sketch-04` (A15 / A16) | Parallel reference | A15-SE2 and S14-SE2 converge on the `co_presence_requirements` field name and record shape — the strongest cross-dialect symmetry signal |
| `save-the-cat-sketch-01` S1–S8 | Extended | `StcStory` grows four optional fields; `StcBeat` grows three optional fields |
| `save-the-cat-sketch-02` S9–S13 | Adjacent | Sketch-02's character layer provides the ids S14-SE2 references; no modification of S9–S13 |

## Concrete next arcs (candidates)

1. **Implement sketch-03** — Python dataclass amendments + S16.1–S16.3 functions + Macbeth encoding migration to use the worked-example values + tests. Mirror `aristotelian-sketch-04` → `0ab7660`. Likely commit message: `save-the-cat-sketch-03: implement S14-S15 + S16.1-S16.3`.
2. **Schema-layer landing** — production-format-sketch-N adding the new optional fields to `schema/save_the_cat/story.json` + `beat.json`, plus two new schemas `schema/save_the_cat/co_presence_requirement.json` + `strand_convergence_requirement.json`. Follows PFS13/PFS14's amendment pattern.
3. **`dialect-compilation-surface-sketch-02`** — formalize the two DOQ2 globalizations from this sketch (co-presence record shape; `tonal_register` field name), or explicitly re-defer them pending a third dialect.
4. **Third per-dialect application** — Dramatic or Dramatica-template grows its own DCS surface. Would require a Tier-1 schema landing as prerequisite since neither currently has one. Forces DOQ2 from 2-of-2 to 3-of-3 evidence.

Per `feedback_research_production_alternation.md`: the natural sequence from sketch-03 is implement (production) → schema landing (production) → then a research-mode return to `dialect-compilation-surface-sketch-02` to formalize (or re-defer) the DOQ2 globalizations.

## What a cold-start Claude should read first

1. `dialect-compilation-surface-sketch-01.md` — the architectural commitments (DCS1–DCS6) this sketch concretizes.
2. `aristotelian-sketch-04.md` — the first per-dialect DCS instantiation whose axes this sketch compares against in the DOQ2 judgment.
3. This sketch.
4. `save-the-cat-sketch-01.md` and `save-the-cat-sketch-02.md` — prior STC commitments (S1–S13) this sketch builds adjacent to.
5. `compilation-sketch-01.md` — the four-stage pipeline that consumes S14 (stages 1–3) and S15 (stage 4).
6. `prototype/story_engine/encodings/macbeth_save_the_cat.py` — the worked-example payload's home.
7. `project_dialect_compilation_surface.md` (memory) — the surface-arc milestone this sketch extends.

## Honest framing

Sketch-03 is the second dialect's turn through DCS1. Its payoff is threefold:

1. **The architecture holds.** DCS1's two-sided cut mapped onto Save-the-Cat without distortion, just as it mapped onto Aristotelian. Three side-1 flavors and three side-2 flavors fell out of the dialect's existing primitives (beats, strands, genres, characters) without adding new primitives to the dialect — DCS1 is behaving as an extension surface, not a forcing ontology.
2. **DOQ2 gets partial closure.** Not "no globalization" (too conservative given the co-presence evidence) and not "full globalization" (too aggressive given the divergent axes). The partial answer is the honest one: two axes admit shared names; the rest stay local. A future sketch can formalize; a third dialect would pressure-test the answer.
3. **Macbeth under sketch-03 surfaces a real structural observation.** The strand-convergence check at slot 9 flags that Macbeth's midpoint beat doesn't author B-strand advancement. That's not a bug in sketch-03's design; it's sketch-03's design doing work — surfacing a structural claim the existing encoding was implicit about. The author can address it either way (re-author or accept); the new surface made the choice visible.

The risk: S14/S15 could become a dumping ground for "things the compiler might want." DCS3's verifier-bisection and DCS5's dialect-locality are the discipline guards, and this sketch is additionally disciplined by the DOQ2 judgment — three-plus axes that looked superficially shareable (positional bound, ranker objective, per-unit pacing) were rejected as too-divergent for globalization. That discipline should continue on the next dialect.

Per `project_solution_horizon.md`: same dual-axis framing. If this engine implements the compiler, S14/S15 are the surface it binds to for Save-the-Cat compilations. If a future more-capable AI does it, the surface, the verifier coverage bisection, the worked Macbeth example, AND the two-dialect DOQ2 judgment are the inputs that survive — the second instantiation demonstrates the pattern replicates, which is stronger evidence than a single instance could give.
