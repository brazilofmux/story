# Aristotelian dialect — sketch 04 (compilation-surface instantiation: A15 extensions + A16 preferences)

**Status:** draft, active
**Date:** 2026-04-21
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [aristotelian-sketch-01](aristotelian-sketch-01.md), [aristotelian-sketch-02](aristotelian-sketch-02.md), [aristotelian-sketch-03](aristotelian-sketch-03.md) — A1–A14 + A7.1–A7.11 unchanged
**Frames:** [dialect-compilation-surface-sketch-01](dialect-compilation-surface-sketch-01.md) — first concrete instantiation of DCS1's two-sided surface; [compilation-sketch-01](compilation-sketch-01.md) — A15 fields flow to stages 1–3, A16 fields flow to stage 4 only
**Related:** `prototype/story_engine/encodings/hamlet_aristotelian.py` — the worked-example payload below; `state-of-play-12` for the post-sketch-03 corpus and probe surface
**Superseded by:** nothing yet

## Purpose

First concrete application of `dialect-compilation-surface-sketch-01`'s two-sided surface to the Aristotelian dialect:

- **A15** — Aristotelian's instantiation of DCS1 side 1 (hard structural extensions). Three first-member flavors: `phase_event_count_bound` (cardinality), `co_presence_required_over_phase` (locality), `audience_knowledge_constraint` (audience-knowledge timing).
- **A16** — Aristotelian's instantiation of DCS1 side 2 (soft preference annotations). Three first-member flavors: `tonal_register`, `binding_distance_preference`, `phase_pacing_preference`.
- **A7.12 / A7.13 / A7.14** — Tier-2 verifier checks for A15's three flavors. A16 fields get no verifier coverage per DCS3.

The architectural commitment is the *surface itself* (A15 and A16). The flavors are first members; each surface admits more flavors without sketch-amendment, the way A13's `kind` is canonical-plus-open.

## Why now

`dialect-compilation-surface-sketch-01` named the two-sided shape abstractly (DCS1) and committed to *next per-dialect surface = forcing function for DOQ1 (catalog)*. Aristotelian is the obvious first target: deepest dialect (sketches 01–03 + four-encoding corpus + Hamlet's multi-session arc), most stress-tested verifier surface, most concrete probe-back-pressure history.

Hamlet specifically is the obvious worked-example payload: it is the corpus's most structurally complex encoding (32 events, 3 tragic heroes, 3-step staging chain, mirror+foil arc relations, BINDING_SEPARATED distance 9 — the widest in corpus) and the only encoding that has been re-probed under post-sketch-03 client extensions (Session 6, commit `4b30291`).

## Scope — what this sketch does and doesn't do

**In scope:**

- Two new architectural commitments (A15 + A16) instantiating DCS1 sides 1 and 2 for Aristotelian.
- Three first-member flavors per side, each with field shape, semantics, and Hamlet worked-example values.
- Three new Tier-2 verifier checks (A7.12, A7.13, A7.14) covering A15's three flavors.
- Optionality discipline (every flavor optional; pre-sketch-04 encodings verify identically).
- Verifier-signature check: do A15 flavors require new `verify` kwargs? Answer: no — every A15 flavor lives as a field on existing record types (ArMythos or ArPhase).

**Out of scope:**

- Implementation (Python dataclass field additions; A7.12–A7.14 functions; encoding migrations). Follows in a separate "implement" commit, the aristotelian-sketch-03 pattern (sketch `6918a32` design → `ac926e2` implement).
- Schema-layer landing (`schema/aristotelian/*.json` amendments). Production-format sketch follows; gated on this design.
- Probe-client rendering of A15 + A16 fields. Future probe-sketch-05 (or amendment to probe-sketch-04). DOQ7 from the surface sketch lives here in concrete form.
- Compile-time overlay schema (DCS6 / DOQ3). Not Aristotelian-specific; lives in compilation-sketch-02.
- Migration of Oedipus / Rashomon / Macbeth to use A15 + A16 fields. Pre-sketch-04 encodings stay unchanged; only Hamlet receives the worked-example values, and only as authored examples — verification continues to pass with the field defaults if the values are not authored.
- Side-2 ranker consumption. Stage 4 of compilation is not implemented; A16 fields are authored-but-not-yet-consumed by design.

## Commitments

Labels A15–A16 continue sketches 01–03's A1–A14 numbering. A7.12–A7.14 extend A7's check list (sketch-03 committed A7.10–A7.11).

### A15 — Side-1 hard structural extensions surface

Per DCS1, A15 commits the Aristotelian dialect to carry hard-constraint fields that flow through `compilation-sketch-01`'s stages 1–3. Three first-member flavors:

#### A15-SE1 — `phase_event_count_bound` on `ArPhase` (cardinality)

```python
@dataclass(frozen=True)
class ArPhase:
    # ... existing fields unchanged ...
    min_event_count: int = 0   # 0 = unbounded floor
    max_event_count: int = 0   # 0 = unbounded ceiling
```

**Semantics.** Hard constraint: when both bounds are non-zero, `min_event_count ≤ len(scope_event_ids) ≤ max_event_count`. When `min_event_count > 0` and `max_event_count == 0`, only the floor binds. Symmetric for ceiling-only. When both are 0 (default), the field carries no constraint and pre-sketch-04 phases verify identically.

**Compiler use.** Stage 1 extracts to per-phase cardinality constraints. Stage 2 (feasibility) folds into the two-level budget calculation: `Σ_phases min_event_count × W_min_per_beat ≤ word_budget`. Stage 3 (planner) treats the bounds as preconditions on event-emission per phase — cannot generate fewer than `min_event_count` events, cannot generate more than `max_event_count`.

**Verifier (A7.12) responsibility.** Structural consistency only: bounds non-negative; if both set, `min ≤ max`; current `len(scope_event_ids)` falls within bounds (when authored).

**Hamlet values (worked example):**

```python
AR_HAMLET_BEGINNING = ArPhase(
    id="ar_hamlet_beginning",
    role="beginning",
    scope_event_ids=(...,),  # 13 events
    min_event_count=10,      # NEW (A15-SE1)
    max_event_count=15,      # NEW (A15-SE1)
    annotation="...",
)
AR_HAMLET_MIDDLE = ArPhase(
    id="ar_hamlet_middle",
    role="middle",
    scope_event_ids=(...,),  # 11 events
    min_event_count=8,
    max_event_count=14,
    annotation="...",
)
AR_HAMLET_END = ArPhase(
    id="ar_hamlet_end",
    role="end",
    scope_event_ids=(...,),  # 8 events
    min_event_count=6,
    max_event_count=10,
    annotation="...",
)
```

Slack on both sides — bounds frame the structural mass without overspecifying. The current authoring (13 / 11 / 8) sits comfortably in the middle of each range; a future compilation could regenerate within the range without violating the dialect.

#### A15-SE2 — `co_presence_required_over_phase` on `ArMythos` (locality)

```python
@dataclass(frozen=True)
class ArCoPresenceRequirement:
    """A15-SE2 (sketch-04). Hard constraint: the named characters must
    co-locate at ≥ min_count substrate events whose τ_s falls within
    the named phase's scope_event_ids.

    Co-location at substrate level requires the substrate to carry
    location state per character per event — see DOQ-AR4-1 for the
    substrate-coverage gap this surface exposes.
    """
    id: str
    character_ref_ids: Tuple[str, ...]   # ≥ 2
    phase_id: str
    min_count: int = 1


@dataclass(frozen=True)
class ArMythos:
    # ... existing fields unchanged ...
    co_presence_requirements: Tuple[ArCoPresenceRequirement, ...] = ()
```

**Semantics.** Hard constraint: for each requirement, ≥ `min_count` substrate events in the named phase's scope must have all named characters co-located. Co-location requires substrate-state knowledge — see DOQ-AR4-1 for the substrate gap this exposes.

**Compiler use.** Stage 1 extracts to per-event co-presence preconditions. Stage 3 (planner) treats co-presence as STRIPS preconditions on the relevant events (CS3) — and where existing events don't satisfy the requirement, generates intermediate events (travel, meeting) to do so. CS6 fires if no plan satisfies all co-presence requirements simultaneously.

**Verifier (A7.13) responsibility.** Structural consistency only: characters resolve in mythos's `characters`; phase resolves in mythos's `phases`; `min_count ≥ 1`. Whether the substrate ACTUALLY carries the co-presence is the compiler's stage-1/3 question — see DOQ-AR4-1.

**Hamlet values (worked example):**

```python
AR_HAMLET_CO_PRESENCE = (
    ArCoPresenceRequirement(
        id="copres_hamlet_claudius_end",
        character_ref_ids=("ar_hamlet", "ar_claudius"),
        phase_id="ar_hamlet_end",
        min_count=2,   # the duel + the final killing
    ),
    ArCoPresenceRequirement(
        id="copres_hamlet_laertes_end",
        character_ref_ids=("ar_hamlet", "ar_laertes"),
        phase_id="ar_hamlet_end",
        min_count=2,   # the duel + Laertes's deathbed reveal
    ),
    ArCoPresenceRequirement(
        id="copres_hamlet_horatio_beginning",
        character_ref_ids=("ar_hamlet", "ar_horatio"),
        phase_id="ar_hamlet_beginning",
        min_count=1,   # the Ghost-scene witness
    ),
)
# Threaded into AR_HAMLET_MYTHOS via co_presence_requirements=AR_HAMLET_CO_PRESENCE
```

Three requirements, all structurally load-bearing in the play. The mirror+foil arc relations from sketch-03 named these characters as related; A15-SE2 makes the *spatial-temporal cooccurrence* of the relation a hard constraint, not just a relation-annotation.

#### A15-SE3 — `audience_knowledge_constraint` on `ArMythos` (audience-knowledge timing)

```python
@dataclass(frozen=True)
class ArAudienceKnowledgeConstraint:
    """A15-SE3 (sketch-04). Hard constraint: the audience must possess
    the named knowledge subject by τ_s ≤ latest_τ_s. When source_event_id
    is set, asserts the knowledge is delivered at that specific event.

    The 'subject' is a free-text canonical knowledge claim — the dialect
    does not constrain its vocabulary, but A15-SE3 admits authoring
    discipline via consistency across encodings (DOQ-AR4-2).

    Distinct from sketch-03 OQ-AP9 (audience-level recognition as a
    dialect record) — A15-SE3 is an authorial *constraint on knowledge
    timing*, not a dialect-level recognition record. The two are
    architecturally orthogonal; A15-SE3 may close part of OQ-AP9's
    productive surface.
    """
    id: str
    subject: str
    latest_τ_s: int
    source_event_id: Optional[str] = None


@dataclass(frozen=True)
class ArMythos:
    # ... existing fields unchanged ...
    audience_knowledge_constraints: Tuple[
        ArAudienceKnowledgeConstraint, ...
    ] = ()
```

**Semantics.** Hard constraint: by the time substrate τ_s reaches `latest_τ_s`, the audience must have access to the named knowledge subject. When `source_event_id` is set, asserts that event delivers the knowledge.

**Compiler use.** Stage 1 extracts to audience-state invariants over substrate. Stage 3 (planner) emits substrate ensuring the knowledge is conveyed by `latest_τ_s` (typically by ensuring an event at or before that τ_s actually carries the conveyance). CS6 fires if no plan can convey the knowledge in time.

**Verifier (A7.14) responsibility.** Structural consistency only: `subject` non-empty; `latest_τ_s ≥ 0`; `source_event_id` (if set) resolves to a substrate event with `τ_s ≤ latest_τ_s`. **Whether the substrate actually carries audience-projection state is out of scope** — see DOQ-AR4-1.

**Hamlet values (worked example):**

```python
AR_HAMLET_AUDIENCE_KNOWLEDGE = (
    ArAudienceKnowledgeConstraint(
        id="ak_claudius_killed_king_hamlet",
        subject="claudius_killed_king_hamlet",
        latest_τ_s=1,
        source_event_id="E_hamlet_meets_ghost",
    ),
    ArAudienceKnowledgeConstraint(
        id="ak_polonius_behind_arras",
        subject="polonius_behind_arras",
        latest_τ_s=7,
        source_event_id="E_polonius_hides_behind_arras",
    ),
    ArAudienceKnowledgeConstraint(
        id="ak_duel_swords_poisoned",
        subject="laertes_sword_unbated_and_poisoned",
        latest_τ_s=15,
        source_event_id="E_duel_plotted",
    ),
)
# Threaded into AR_HAMLET_MYTHOS via audience_knowledge_constraints=AR_HAMLET_AUDIENCE_KNOWLEDGE
```

Three load-bearing pieces of dramatic-irony knowledge. Each is a setup the play exploits at a later moment: the Ghost's revelation grounds the audience's reading of every Hamlet/Claudius scene; Polonius-behind-the-arras grounds the τ_s=8 stabbing; the poisoned-sword setup grounds the entire end-phase reading.

A15-SE3 is the most exploratory of the three flavors — it surfaces a real substrate gap (DOQ-AR4-1) that the other two also touch but less acutely. Including it in the first instantiation is deliberate: better to expose the gap now than discover it after the surface is committed.

### A16 — Side-2 soft preference annotations surface

Per DCS1, A16 commits the Aristotelian dialect to carry preference-annotation fields that flow only to `compilation-sketch-01` stage 4. No verifier coverage (DCS3). Three first-member flavors:

#### A16-SP1 — `tonal_register` on `ArMythos` (tonal preference)

```python
@dataclass(frozen=True)
class ArMythos:
    # ... existing fields unchanged ...
    tonal_register: str = ""
```

**Semantics.** Single string from a controlled-but-open vocabulary. Initial controlled set: `{tragic-pure, tragic-with-irony, elegiac, claustrophobic, classical, modern}`. Empty string (default) is neutral — ranker has no tonal preference signal.

**Ranker use.** Stage 4 ranker reads `tonal_register` as a scoring rubric input. Specific scoring algorithm is OQ4 (compilation-sketch-01); A16-SP1 commits to the *input language*, not the scoring.

**Vocabulary discipline.** Canonical-plus-open like A10 / A13 `kind`. Authors can use non-canonical values; the ranker is responsible for handling them gracefully (default-neutral when unrecognized).

**Hamlet value:** `tonal_register="tragic-with-irony"` — captures the gravedigger scene, the "to be or not to be" reflexivity, the play-within-a-play recursion, the running self-aware irony of Hamlet's commentary on his own delay.

#### A16-SP2 — `binding_distance_preference` on `ArMythos` (ranker-objective preference)

```python
@dataclass(frozen=True)
class ArMythos:
    # ... existing fields unchanged ...
    binding_distance_preference: str = ""
```

**Semantics.** Single string from `{prefer_near, prefer_separated, prefer_wide, neutral, ""}`. Empty string defaults to neutral. The preference biases the stage-4 ranker toward candidates with the matching peripeteia↔anagnorisis distance characteristic.

**Distinct from A12.** A12's `peripeteia_anagnorisis_binding` is a *typed structural assertion* (the binding IS adjacent / separated / coincident); A7.8 enforces it against actual τ_s distance. A16-SP2 is a *soft ranker preference* over admissible distances within whatever A12 binding-class is asserted. Hard structural fact; soft scoring preference. The two stack: A12 says "this is SEPARATED with adjacency_bound=N"; A16-SP2 says "within SEPARATED, prefer wider over narrower" (`prefer_wide`).

**Ranker use.** Stage 4 ranker computes the actual binding distance for each candidate and scores in the direction of the preference. Algorithm is OQ4; A16-SP2 commits the input.

**Hamlet value:** `binding_distance_preference="prefer_wide"` — Hamlet's BINDING_SEPARATED with distance 9 is the corpus's widest. The text's emotional shape relies on the long delay between peripeteia (E_hamlet_kills_polonius τ_s=8) and anagnorisis (E_laertes_reveals_plot τ_s=17) — the entire end-phase arc lives in that gap. The preference matches the encoded structure.

#### A16-SP3 — `phase_pacing_preference` on `ArPhase` (pacing preference)

```python
@dataclass(frozen=True)
class ArPhase:
    # ... existing fields unchanged ...
    pacing_preference: str = ""
```

**Semantics.** Single string from `{slow_burn, even, accelerating, rapid_escalation, decelerating, ""}`. Empty string is neutral. The preference biases stage-4 ranker toward candidates whose intra-phase event distribution matches the named pacing shape.

**Cross-phase coherence.** Authors may use different preferences per phase — typical Aristotelian shape is `even / slow_burn / rapid_escalation`. The ranker scores each phase's pacing independently; no cross-phase consistency required by A16-SP3 itself (open question: should there be? Banked as DOQ-AR4-3).

**Ranker use.** Stage 4 ranker measures candidate event-distribution within each phase and scores against the per-phase preference. Algorithm is OQ4.

**Hamlet values (worked example):**

```python
AR_HAMLET_BEGINNING = ArPhase(
    # ... existing + A15-SE1 fields ...
    pacing_preference="even",         # NEW (A16-SP3)
)
AR_HAMLET_MIDDLE = ArPhase(
    # ... existing + A15-SE1 fields ...
    pacing_preference="slow_burn",    # the soliloquies, the long delay
)
AR_HAMLET_END = ArPhase(
    # ... existing + A15-SE1 fields ...
    pacing_preference="rapid_escalation",  # poison, duel, deaths, in tight succession
)
```

Three preferences mapping the canonical Aristotelian dramatic shape onto Hamlet's specific texture. The middle-phase `slow_burn` and end-phase `rapid_escalation` together express the play's signature emotional arc — long deliberation collapsing into rapid catastrophe.

### A7.12 — `phase_event_count_bound` consistency (A15-SE1)

For each `ArPhase`:

1. `min_event_count ≥ 0`. Violation: `phase_event_count_min_negative` (advises-review).
2. `max_event_count ≥ 0`. Violation: `phase_event_count_max_negative` (advises-review).
3. If both `min_event_count > 0` and `max_event_count > 0`: `min_event_count ≤ max_event_count`. Violation: `phase_event_count_bounds_inverted` (advises-review).
4. `len(scope_event_ids)` falls within bounds when bounds active. Violations: `phase_event_count_below_min` / `phase_event_count_above_max` (advises-review). Skips when bounds at default 0.

### A7.13 — `co_presence_required_over_phase` structural integrity (A15-SE2)

For each `ArCoPresenceRequirement` on the mythos:

1. `len(character_ref_ids) ≥ 2`. Violation: `co_presence_refs_too_few` (advises-review).
2. All `character_ref_ids` resolve in `mythos.characters`. Violation: `co_presence_character_unresolved` (advises-review).
3. `phase_id` resolves in `mythos.phases`. Violation: `co_presence_phase_unresolved` (advises-review).
4. `min_count ≥ 1`. Violation: `co_presence_min_count_zero` (advises-review).

A7.13 does NOT verify that the substrate actually carries the co-presence — that is a compiler-stage-3 question. See DOQ-AR4-1 for the substrate-coverage gap.

### A7.14 — `audience_knowledge_constraint` structural integrity (A15-SE3)

For each `ArAudienceKnowledgeConstraint` on the mythos:

1. `subject` is non-empty after strip. Violation: `audience_knowledge_subject_empty` (advises-review).
2. `latest_τ_s ≥ 0`. Violation: `audience_knowledge_τ_s_negative` (advises-review).
3. If `source_event_id` is set, it resolves in `substrate_events` when threaded. Violation: `audience_knowledge_source_event_unresolved` (advises-review). Skips when substrate empty.
4. If `source_event_id` is set, the resolved event's `τ_s ≤ latest_τ_s`. Violation: `audience_knowledge_source_event_too_late` (advises-review). Skips when substrate empty.

A7.14 does NOT verify that the substrate's audience-projection state actually carries the knowledge — see DOQ-AR4-1.

### A7 orchestration — verify signature stays unchanged

All A15 fields live on existing record types (`ArPhase`, `ArMythos`); A7.12 / A7.13 / A7.14 walk the existing structures. No new `verify` kwarg. Pre-sketch-04 callers continue to work; A7.12–A7.14 skip cleanly when fields stay at defaults.

`group_by_severity` / `group_by_code` unchanged.

## Open questions — banked

### DOQ-AR4-1 — Substrate audience-projection / co-presence state coverage

A15-SE2 (`co_presence_required_over_phase`) and A15-SE3 (`audience_knowledge_constraint`) both reference substrate state the substrate may not currently carry:

- Co-presence requires per-event-per-character location state. Substrate has `Entity` records and `Held` records; whether these compose into reliable per-event location state per character is unverified.
- Audience-knowledge requires an audience-projection of substrate facts. Substrate has no audience-state record kind today.

This is the same surface as `compilation-sketch-01` OQ1 (state representation granularity). A15-SE2 + A15-SE3 force the question concretely. Two paths:

- **Substrate extension** — add a `LocationFact` or `AudienceKnowledgeFact` substrate record kind. Heavy; touches every existing encoding.
- **Compiler-internal projection** — stage 1 derives location state from `Entity` + `Held` traversal; stage 1 derives audience-projection from event-visibility metadata. Light; stays inside the compiler.

**Forcing function:** first stage-1 implementation that needs to honor an A15-SE2 or A15-SE3 constraint. The implementation either succeeds with substrate-as-is (light path), needs substrate metadata (medium path), or needs new substrate record kinds (heavy path). The path emerges; the question gets answered.

### DOQ-AR4-2 — A15-SE3 `subject` vocabulary discipline

A15-SE3's `subject` is free-text canonical knowledge claim. Cross-encoding consistency is undefined: Hamlet's `"claudius_killed_king_hamlet"` and a hypothetical Macbeth `"macbeth_killed_duncan"` follow the same {actor}_{verb}_{object} convention by accident.

Three options:
- **Free-text.** Author discipline only; no verifier check.
- **Controlled vocabulary per dialect.** Aristotelian-specific subject taxonomy; verifier-checkable.
- **Per-encoding controlled vocabulary.** Each encoding declares its own subject set; verifier checks consistency within encoding.

**Forcing function:** second encoding adopts A15-SE3. Vocabulary drift visible iff conventions diverge.

### DOQ-AR4-3 — Cross-phase pacing-preference coherence (A16-SP3)

A16-SP3 admits arbitrary per-phase combinations including incoherent ones (e.g., `decelerating / decelerating / decelerating` across all three phases — a dramatic shape that contradicts Aristotelian rising-action expectations).

Should the dialect or the ranker enforce any cross-phase coherence?

- **Dialect (verifier) enforcement.** Add a check family ranking known-incoherent combinations. Limits authorial freedom; matches expert-system posture (`project_expert_system_goal.md`).
- **Ranker enforcement.** Ranker scores incoherent combinations lower without erroring; preserves authorial freedom but loses verifier visibility.
- **Neither.** Authors are free to encode anti-canonical pacing; if it produces bad stories, the prose-level audience signals it. Most laissez-faire.

**Forcing function:** first encoding authoring an anti-canonical pacing combination. Currently no encoding does; banked.

### DOQ-AR4-4 — Probe rendering of A15 + A16 fields (DOQ7 instantiation)

Per DOQ7 from `dialect-compilation-surface-sketch-01`, the probe (reader-model client) may or may not surface A15 + A16 fields for review. Aristotelian-specific positions:

- **A15 fields read by probe.** Rendering A15-SE3 audience-knowledge constraints helps the probe interpret dramatic-irony observations. Probe could surface inconsistencies between A15-SE3 declarations and the substrate prose's actual irony deployment.
- **A16 fields read by probe.** Rendering A16-SP1 tonal-register lets the probe interpret prose against author-declared tone. Could surface `noted` observations on tone mismatch.
- **Neither rendered.** Probe stays at sketch-03 surface (5 record kinds × specific fields); A15/A16 are compiler-and-ranker-only. Cleanest separation.

**Forcing function:** first probe-sketch-05 attempt. Decision local to that sketch.

### DOQ-AR4-5 — Compile-time overlay shape for Aristotelian (DOQ3 instantiation)

Per DCS6, the compile-time `hints` input becomes a dialect-overlay. For Aristotelian, the overlay shape question becomes: can compile-time author submit a partial `ArMythos` carrying only A15/A16 field overrides?

If yes (option a from DOQ3): compile-time author can change `binding_distance_preference` per compilation without editing the canonical encoding. Useful for exploratory generation.

If side-2-only (option b): A15 fields are encoding-level only; only A16 fields admit compile-time override.

**Forcing function:** first compilation that wants a per-run preference override. Banked.

## Worked example — Hamlet under sketch-04

Hamlet is the largest, most stress-tested encoding. Under sketch-04, three new field assignments on existing records and three new module-level tuples:

```python
# In hamlet_aristotelian.py:

# A15-SE2 module-level tuple
AR_HAMLET_CO_PRESENCE = (
    ArCoPresenceRequirement(
        id="copres_hamlet_claudius_end",
        character_ref_ids=("ar_hamlet", "ar_claudius"),
        phase_id="ar_hamlet_end",
        min_count=2,
    ),
    ArCoPresenceRequirement(
        id="copres_hamlet_laertes_end",
        character_ref_ids=("ar_hamlet", "ar_laertes"),
        phase_id="ar_hamlet_end",
        min_count=2,
    ),
    ArCoPresenceRequirement(
        id="copres_hamlet_horatio_beginning",
        character_ref_ids=("ar_hamlet", "ar_horatio"),
        phase_id="ar_hamlet_beginning",
        min_count=1,
    ),
)

# A15-SE3 module-level tuple
AR_HAMLET_AUDIENCE_KNOWLEDGE = (
    ArAudienceKnowledgeConstraint(
        id="ak_claudius_killed_king_hamlet",
        subject="claudius_killed_king_hamlet",
        latest_τ_s=1,
        source_event_id="E_hamlet_meets_ghost",
    ),
    ArAudienceKnowledgeConstraint(
        id="ak_polonius_behind_arras",
        subject="polonius_behind_arras",
        latest_τ_s=7,
        source_event_id="E_polonius_hides_behind_arras",
    ),
    ArAudienceKnowledgeConstraint(
        id="ak_duel_swords_poisoned",
        subject="laertes_sword_unbated_and_poisoned",
        latest_τ_s=15,
        source_event_id="E_duel_plotted",
    ),
)

# Phases gain A15-SE1 + A16-SP3 fields
AR_HAMLET_BEGINNING = ArPhase(
    id="ar_hamlet_beginning", role="beginning",
    scope_event_ids=(...,),
    min_event_count=10, max_event_count=15,    # A15-SE1
    pacing_preference="even",                   # A16-SP3
    annotation="...",
)
AR_HAMLET_MIDDLE = ArPhase(
    id="ar_hamlet_middle", role="middle",
    scope_event_ids=(...,),
    min_event_count=8, max_event_count=14,
    pacing_preference="slow_burn",
    annotation="...",
)
AR_HAMLET_END = ArPhase(
    id="ar_hamlet_end", role="end",
    scope_event_ids=(...,),
    min_event_count=6, max_event_count=10,
    pacing_preference="rapid_escalation",
    annotation="...",
)

# Mythos gains A15-SE2/SE3 + A16-SP1/SP2 fields
AR_HAMLET_MYTHOS = ArMythos(
    # ... existing fields unchanged ...
    co_presence_requirements=AR_HAMLET_CO_PRESENCE,            # A15-SE2
    audience_knowledge_constraints=AR_HAMLET_AUDIENCE_KNOWLEDGE,  # A15-SE3
    tonal_register="tragic-with-irony",                         # A16-SP1
    binding_distance_preference="prefer_wide",                  # A16-SP2
)
```

Verification under sketch-04 (signature unchanged from sketch-03):

```python
verify(
    AR_HAMLET_MYTHOS,
    substrate_events=FABULA,
    mythoi=(AR_HAMLET_MYTHOS,),
    character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
)
```

Expected outcome: A7.12–A7.14 run cleanly. Bounds (A7.12) all satisfied — Hamlet's authored event counts (13/11/8) fall within (10..15)/(8..14)/(6..10). Co-presence (A7.13) — three records, all characters resolve, all phases resolve. Audience-knowledge (A7.14) — three records, all subjects non-empty, all source events resolve and τ_s ≤ latest_τ_s.

A16 fields (`tonal_register`, `binding_distance_preference`, `pacing_preference`) emit no observations — by DCS3 they are not verifier-coverable.

## Pre-sketch-04 corpus: Oedipus / Rashomon / Macbeth

All A15 and A16 fields default to empty / 0 / "". Pre-sketch-04 encodings stay unchanged and verify identically. Authors may opt in incrementally:

- Oedipus could grow A15-SE1 phase bounds (its three phases are tight: 8/9/6).
- Macbeth could grow A15-SE2 (Macbeth-Lady-Macbeth co-presence in act-2 phase).
- Rashomon's four-mythos contest is more naturally an A10 ArMythosRelation case; A15/A16 surfaces don't add structural pressure.

No migration is committed by sketch-04. Hamlet is the worked-example payload; other encodings remain at sketch-03 surface until probe-back-pressure or independent author motivation pushes adoption.

## Architectural classification: extension

Six new optional fields across two record types (`ArPhase`: `min_event_count`, `max_event_count`, `pacing_preference`; `ArMythos`: `co_presence_requirements`, `audience_knowledge_constraints`, `tonal_register`, `binding_distance_preference`) plus two new dataclass record types (`ArCoPresenceRequirement`, `ArAudienceKnowledgeConstraint`).

All defaults are empty / 0 / "". A1–A14 semantics unchanged. A7.1–A7.11 unchanged. Verifier signature unchanged. Pre-sketch-04 encodings verify identically.

## Relationship to prior commitments

| Prior | Refined / extended by sketch-04 | How |
|---|---|---|
| `dialect-compilation-surface-sketch-01` DCS1 | Concretized | A15 + A16 are Aristotelian's instantiations of the two-sided surface |
| `dialect-compilation-surface-sketch-01` DCS2 | Concretized | A15 fields flow to stages 1–3; A16 fields flow to stage 4 only |
| `dialect-compilation-surface-sketch-01` DCS3 | Concretized | A7.12–A7.14 cover side 1; side 2 has no checks by construction |
| `dialect-compilation-surface-sketch-01` DCS4 | Honored | All fields default-empty; pre-sketch-04 encodings unchanged |
| `dialect-compilation-surface-sketch-01` DCS5 | Honored | A15 + A16 vocabularies are Aristotelian-local (DOQ-AR4-2 admits cross-dialect symmetry as a future question) |
| `dialect-compilation-surface-sketch-01` DOQ1 | Partially closed | Per-side flavor catalog gets six concrete first members; abstraction holds |
| `dialect-compilation-surface-sketch-01` DOQ6 | Surfaces concretely as DOQ-AR4-1 | Lowering / substrate-coverage gap exposed by A15-SE2 + A15-SE3 |
| `dialect-compilation-surface-sketch-01` DOQ7 | Surfaces concretely as DOQ-AR4-4 | Probe rendering of new surface |
| `compilation-sketch-01` OQ1 | Pressured | Substrate state representation must accommodate co-presence + audience-projection (DOQ-AR4-1) |
| `compilation-sketch-01` OQ4 | Bounded above | A16's three flavors define part of the ranker's input language |
| `compilation-sketch-01` OQ5 | Refined | Hard side 1 vs soft side 2 cut becomes concrete per-flavor; per-side flavor count matters less than side-membership |
| `aristotelian-sketch-01` A2 | Extended | ArPhase grows three optional fields; A2 semantics unchanged |
| `aristotelian-sketch-01` A1 | Extended | ArMythos grows four optional fields + two new sub-record kinds |
| `aristotelian-sketch-03` A14 | Adjacent | A14's `anagnorisis_character_ref_id` is structurally on `ArMythos`; A15/A16 add adjacent fields without disturbing A14 |

## Concrete next arcs (candidates)

1. **Implement sketch-04** — Python dataclass amendments + A7.12–A7.14 functions + Hamlet encoding migration to use the worked-example values + tests. Follows aristotelian-sketch-03's pattern (design `6918a32` → implement `ac926e2`). Likely commit message: `aristotelian-sketch-04: implement A15-A16 + A7.12-A7.14`.
2. **Schema-layer landing** — production-format-sketch-N adding the new optional fields to `schema/aristotelian/mythos.json` + `phase.json`, plus two new schemas `schema/aristotelian/co_presence_requirement.json` + `audience_knowledge_constraint.json`. Follows PFS13's amendment pattern.
3. **Probe-sketch-05** — decide DOQ-AR4-4 (probe rendering of A15 + A16 fields). Likely scoped to one side or one record kind for the first iteration.
4. **Second per-dialect application** — Save-the-Cat, Dramatic, or Dramatica-template grows its own A15/A16-shaped surface. Forces DOQ2 (cross-dialect symmetry) from the surface sketch.

Per `feedback_research_production_alternation.md`: the natural sequence is implement-sketch-04 (production) → schema landing (production) → probe-sketch-05 (research-mode) → second dialect (mixed).

## What a cold-start Claude should read first

1. `dialect-compilation-surface-sketch-01.md` — the architectural commitments (DCS1–DCS6) this sketch concretizes.
2. This sketch.
3. `aristotelian-sketch-03.md` — the immediate prior Aristotelian commitments (A13, A14) this sketch builds adjacent to.
4. `compilation-sketch-01.md` — the four-stage pipeline that consumes A15 (stages 1–3) and A16 (stage 4).
5. `prototype/story_engine/encodings/hamlet_aristotelian.py` — the worked-example payload's home.
6. `state-of-play-12.md` — current corpus and post-sketch-03 dialect status.

## Honest framing

Sketch-04 is the first time the dialect grows fields *for the compiler* rather than fields the compiler will eventually consume incidentally. Every prior dialect field had a verification or interpretation home; A15/A16 fields exist to give the compiler structured input the substrate cannot provide and the existing dialect did not anticipate.

The risk: A15/A16 fields could become an undisciplined dumping ground for "things the compiler might want." DCS3's verifier-bisection and DCS5's dialect-locality are the discipline guards. Each new flavor in either bucket should be motivated by *concrete compiler-stage need* and either Tier-2-checkable (side 1) or LLM-interpretable (side 2). Three flavors per side in the first instantiation is a deliberate floor — enough to demonstrate the architecture, not so many that the surface inflates before the compiler is implemented to use it.

The opportunity: with A15/A16 in place, every subsequent compilation work has a stable dialect-side surface to bind to. The next per-stage compilation sketch (likely stage 2 feasibility or stage 1 constraint extraction) can target real Aristotelian fields, not hypothetical ones.

Per `project_solution_horizon.md`: same dual-axis framing as the surface sketch. If this engine implements the compiler, A15/A16 are the surface it binds to. If a future more-capable AI does it, the surface, the verifier coverage bisection, and the worked Hamlet example are the inputs that survive.
