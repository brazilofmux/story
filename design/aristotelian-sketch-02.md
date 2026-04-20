# Aristotelian dialect — sketch 02 (ArMythosRelation + ArAnagnorisisChain + ArPeripeteiaAnagnorisisBinding)

**Status:** draft, active
**Date:** 2026-04-19
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [aristotelian-sketch-01](aristotelian-sketch-01.md) — commitments A1–A9 unchanged
**Frames:** [architecture-sketch-02](architecture-sketch-02.md), [aristotelian-sketch-01](aristotelian-sketch-01.md)
**Related:** [aristotelian-probe-sketch-01](aristotelian-probe-sketch-01.md) (source of the forcing functions); [save-the-cat-sketch-02](save-the-cat-sketch-02.md) (precedent for dialect-amendment-by-extension)
**Superseded by:** nothing yet

## Purpose

Close three of the five dialect-extension proposals banked from the Aristotelian probe arc. Each of the three addresses a concrete structural gap in a shipped encoding — not a hypothetical requirement. The remaining two proposals are held out with explicit rationale: one is blocked by substrate-layer absence; the other is against sketch-01's deliberate scope.

The sketch adds three new dialect-layer constructs (A10–A12) and four new self-verifier checks (A7.6–A7.9). Commitments A1–A9 from sketch-01 are unchanged.

## Why now

Aristotelian-probe-sketch-01 (2026-04-19) ran two live probes against the dialect surface. The Oedipus probe surfaced two relations_wanted entries (`ArAnagnorisisChain`, `ArPeripeteiaAnagnorisisBinding`); the Rashomon probe surfaced three (`ArMythosRelation`, `ArFrameMythos`, `ArAnagnorisisLevel`).

Sketch-01 A8 pre-flagged `ArMythosRelation` as a sketch-02 concern *if a forcing function appeared*. It appeared. The two Oedipus-surfaced proposals are not flagged in sketch-01 but emerge from a concrete shipped encoding limit (Jocasta's recognition preceding Oedipus's; the action_summary's prose claim of coincidence contradicted by the record's own fields).

Landing the three well-forced ones now clears the probe's productive output and keeps the dialect's deferrals honest. The two held-out proposals are documented (see §Deferred extensions) so the next probe cycle does not re-surface them as novel.

## Scope — what this sketch does and doesn't do

**In scope:**

- `ArMythosRelation` record expressing structural relations between two or more ArMythos records (contests / parallel / contains).
- `ArAnagnorisisStep` record + `ArMythos.anagnorisis_chain` field expressing staggered character-level recognitions within a single mythos.
- `ArMythos.peripeteia_anagnorisis_binding` field + `peripeteia_anagnorisis_adjacency_bound` field expressing the structural relation between reversal and recognition.
- Four new self-verifier checks (A7.6 – A7.9) over the new fields.
- Encoding migrations for Oedipus (A11 + A12) and Rashomon (A10).

**Out of scope:**

- `ArFrameMythos` — blocked by substrate-layer absence. Rashomon's gate / priest / commoner / rain frame has no substrate events today (state-of-play-02: "grove-only substrate scope"). Revisit when a substrate extension lands; the A10 `contains` vocabulary is pre-placed for forward-compatibility.
- `ArAnagnorisisLevel` — against sketch-01's deliberate scope. A8 placed audience response out of the dialect in the same class as catharsis; admitting a level modifier on anagnorisis reopens that decision, which is a sketch-01 amendment, not a sketch-02 extension.
- Cross-dialect Lowering (A9 unchanged).
- Changes to core records (`ArMythos.plot_kind` enum, `ArPhase.role` enum, `ArCharacter` shape, `ArObservation` severity set).
- Schema-layer landing of A10–A12 under `schema/aristotelian/`. That is a separate production-format arc; see AA11.

## Commitments

Labels A10–A12 continue sketch-01's A1–A9 numbering. A7.6–A7.9 extend A7's numbered check list.

### A10 — ArMythosRelation expresses structural relations between mythoi

```python
@dataclass(frozen=True)
class ArMythosRelation:
    id: str
    kind: str                              # canonical-plus-open
    mythoi_ids: Tuple[str, ...]            # ≥ 2 mythos ids
    over_event_ids: Tuple[str, ...] = ()   # substrate events at stake
    annotation: str = ""
```

**Canonical kind vocabulary:**

- `"contests"` — two or more mythoi differ structurally over shared events. The Rashomon four-testimony case. `over_event_ids` names the contested events (typically the canonical-floor events that appear in every participating mythos's beginning phase).
- `"parallel"` — two mythoi run alongside without contesting each other: a single work may ship two separable arcs with overlapping casts but non-overlapping events. `over_event_ids` optional.
- `"contains"` — one mythos envelopes another (the outer mythos's `central_event_ids` is a strict superset of each inner's). Vocabulary ships for forward-compatibility with a deferred `ArFrameMythos`; no encoding uses it today.

**Canonical-plus-open discipline.** Non-canonical `kind` values are accepted but flagged at severity `noted` (not `advises-review`). This matches Save-the-Cat's role_labels vocabulary shape: authors can experiment without a dialect update, and the noted-severity finding is a nudge rather than a block.

**A10 placement.** `ArMythosRelation` records live on an encoding's module at encoding scope (parallel to how `AR_RASHOMON_MYTHOI` is a tuple at module scope today). The dialect does not add a new top-level container; authors maintain a `AR_*_RELATIONS` tuple and pass it to `verify`.

**Architectural classification: extension.** New dialect-layer record. N-ary via `mythoi_ids` tuple. Substrate-agnostic (`over_event_ids` references checked only when substrate threaded through).

### A11 — ArAnagnorisisStep + anagnorisis_chain express staggered recognitions

```python
@dataclass(frozen=True)
class ArAnagnorisisStep:
    id: str
    event_id: str                          # substrate event: the realization moment
    character_ref_id: str                  # who realizes — required; see below
    precipitates_main: bool = False        # does this step cause the mythos's main anagnorisis?
    annotation: str = ""

@dataclass(frozen=True)
class ArMythos:
    # ... existing fields unchanged ...
    anagnorisis_chain: Tuple[ArAnagnorisisStep, ...] = ()
```

Sketch-01 A4 committed `ArMythos.anagnorisis_event_id` as a singular `Optional[str]`. A11 does not modify that field; it adds a sibling tuple for additional recognitions that structurally exist within the same mythos.

**A11 invariants (A7.7 enforces):**

1. Every step's `event_id` is in the enclosing mythos's `central_event_ids`.
2. If `precipitates_main=True`, the mythos's `anagnorisis_event_id` must be non-None, and the step's τ_s must be strictly less than the main anagnorisis event's τ_s. Enforceable only when substrate events are threaded; skips otherwise (consistent with A7 check 4's existing substrate-absent behavior).
3. A step's `event_id` must not equal `anagnorisis_event_id`. The main recognition is the main recognition; steps are strictly additional moments.

**Why `character_ref_id` is required, not optional.** The probe's `relations_wanted` entry named `ArAnagnorisisChain` as "a relation linking multiple recognition events **within one mythos**". That scoping is character-level by construction (anagnorisis is character-level in Aristotelian vocabulary per A4 / A5). A step with no character ref would be audience-level — the `ArAnagnorisisLevel` case this sketch explicitly rejects. Keeping the ref required keeps A11 in sketch-02's scope.

**Backward compatibility.** `anagnorisis_chain: Tuple[...] = ()` defaults empty. All five shipped mythoi (Oedipus + 4 Rashomon) author no chain; verification behavior on them is unchanged. Only Oedipus migrates to use the field (AA9).

**Architectural classification: extension.** One new dialect record + one optional field on `ArMythos` with empty-tuple default. No modification to `anagnorisis_event_id` semantics.

### A12 — peripeteia_anagnorisis_binding types the reversal/recognition relation

```python
@dataclass(frozen=True)
class ArMythos:
    # ... existing fields unchanged ...
    peripeteia_anagnorisis_binding: Optional[str] = None
    peripeteia_anagnorisis_adjacency_bound: int = 3
```

Replaces author prose (e.g., "reversal and recognition coincide") with a machine-checkable structural declaration. Four values:

- `None` (default) — no structural claim. The author's `action_summary` carries whatever reading applies. Pre-sketch-02 encodings start here; no migration required.
- `"coincident"` — `peripeteia_event_id == anagnorisis_event_id`. Both exactly one substrate event.
- `"adjacent"` — `peripeteia_event_id != anagnorisis_event_id` and `|τ_s(peripeteia) − τ_s(anagnorisis)| ≤ peripeteia_anagnorisis_adjacency_bound`. Two distinct substrate moments but narratively adjacent.
- `"separated"` — `|τ_s(peripeteia) − τ_s(anagnorisis)| > peripeteia_anagnorisis_adjacency_bound`. Staged as a two-beat movement.

**Why the adjacency bound is per-mythos, not global.** Dramatic pacing varies across encodings. A mythos spanning decades may treat a τ_s distance of 10 as adjacent; one compressed to a single dramatic day may treat 2 as separated. The default `3` is a placeholder for Oedipus-scale pacing; authors override when their dramatic clock demands it.

**A12 invariants (A7.8 enforces):** if `peripeteia_anagnorisis_binding` is set to a non-None value, both `peripeteia_event_id` and `anagnorisis_event_id` must be non-None, both must resolve in substrate events, and the declared value must be consistent with the τ_s facts. Disagreement is severity `advises-review` with code `peripeteia_anagnorisis_binding_inconsistent`.

**Architectural classification: extension.** Two optional fields on `ArMythos` with `None` / `3` defaults. Zero change to pre-sketch-02 behavior.

### A7.6 — ArMythosRelation structural integrity

For each `ArMythosRelation`:

1. `kind` in canonical set `{"contests", "parallel", "contains"}` — non-canonical values emit `severity=noted`.
2. `mythoi_ids` has ≥ 2 entries; all ids resolve to mythoi in the encoding (requires the `mythoi` kwarg).
3. For `kind="contests"`: every event in `over_event_ids` appears in every listed mythos's `central_event_ids`.
4. For `kind="contains"`: the first listed mythos's `central_event_ids` is a strict superset of every subsequent listed mythos's.

### A7.7 — ArAnagnorisisStep integrity

Enforces the three A11 invariants (above) plus:

5. `character_ref_id` resolves to an `ArCharacter` in the enclosing mythos's `characters` tuple, if the mythos authors any characters. Self-contained mythoi with empty `characters` skip this check (same discipline as A7 check 5 hamartia-participation).

### A7.8 — peripeteia_anagnorisis_binding consistency

Runs when `peripeteia_anagnorisis_binding` is non-None. If substrate events aren't threaded, skips (consistent with A7 check 4's substrate-absent behavior).

### A7.9 — ArMythosRelation event-reference integrity

Every event id in `over_event_ids` must resolve in substrate events when threaded. Independent of A7.6 checks 3 / 4 (which read against `central_event_ids`, not raw substrate).

### A7 orchestration — verify signature extension

```python
def verify(
    mythos: ArMythos,
    *,
    substrate_events: tuple = (),
    mythoi: Tuple[ArMythos, ...] = (),                # NEW (A7.6)
    relations: Tuple[ArMythosRelation, ...] = (),     # NEW (A7.6, A7.9)
) -> list:
    ...
```

Both new kwargs default empty. Callers not adopting A10–A12 change nothing — the dialect-local checks added by A7.6 / A7.9 skip on empty inputs. `group_by_severity` / `group_by_code` are unchanged.

## Worked case — Rashomon under A10

```python
AR_RASHOMON_CONTEST = ArMythosRelation(
    id="arel_rashomon_contest",
    kind="contests",
    mythoi_ids=(
        "ar_rashomon_bandit",
        "ar_rashomon_wife",
        "ar_rashomon_samurai",
        "ar_rashomon_woodcutter",
    ),
    over_event_ids=(
        "E_travel", "E_tajomaru_sees_them", "E_lure", "E_bind",
        "E_bring_wife", "E_intercourse",
    ),
    annotation=(
        "The four testimonies of Rashomon render the same six "
        "canonical-floor events as the beginning of a distinct "
        "mythos. The contest is not over whether the events "
        "occurred — all four agree they did — but over how they "
        "are arranged toward pathos (seduction vs. assault; noble "
        "combat vs. cowardly scuffle; honorable refusal vs. "
        "coerced complicity). Aristotle's framework is mythos-"
        "singular; this relation records the dialect-level "
        "acknowledgment that the work's catharsis depends on the "
        "friction between competing arrangements of shared "
        "incidents."
    ),
)

AR_RASHOMON_RELATIONS = (AR_RASHOMON_CONTEST,)
```

Verification:

```python
for m in AR_RASHOMON_MYTHOI:
    obs = verify(
        m, substrate_events=EVENTS_ALL,
        mythoi=AR_RASHOMON_MYTHOI,
        relations=AR_RASHOMON_RELATIONS,
    )
```

All four mythoi carry the six canonical-floor events in their beginning phases. A7.6 check 3 passes: each event in `over_event_ids` appears in every listed mythos's `central_event_ids`. A7.9 passes: each event resolves in substrate.

The probe's Rashomon dialect_reading named the pre-sketch-02 limit: *"the Aristotelian dialect has no native way to express that the same substrate event carries different significance depending on whose mythos it appears in — it can only repeat the event ID across mythoi."* A10 gives the dialect the structural hook; the per-mythos phase `annotation` prose still carries the interpretive content (grid-snap, per architecture-sketch-01 A3).

## Worked case — Oedipus under A11

Oedipus's Jocasta realizes at `E_jocasta_realizes` (τ_s=9) — four substrate steps before Oedipus's own anagnorisis at `E_oedipus_anagnorisis` (τ_s=13). Sketch-01's encoding placed Jocasta's realization in the middle phase as a workaround; A11 lets it live in its actual structural role.

```python
AR_STEP_JOCASTA = ArAnagnorisisStep(
    id="arstep_jocasta_realizes",
    event_id="E_jocasta_realizes",              # τ_s=9
    character_ref_id="ar_jocasta",
    precipitates_main=True,
    annotation=(
        "Jocasta realizes before Oedipus does. Her recognition "
        "precipitates the pressure toward his — she begs him to "
        "stop the investigation; her suicide follows. In the "
        "play's fabula she leaves the stage; in the mythos's "
        "structure she has triggered the recognition Oedipus will "
        "reach four τ_s-steps later at the shepherd's testimony. "
        "The dialect's singular anagnorisis_event_id names "
        "Oedipus's as the mythos's main recognition; this step "
        "names Jocasta's as the precipitating earlier."
    ),
)

AR_OEDIPUS_MYTHOS = ArMythos(
    # ... fields unchanged ...
    anagnorisis_chain=(AR_STEP_JOCASTA,),
)
```

Verification (A7.7):

- Invariant 1: `E_jocasta_realizes` ∈ `central_event_ids`. ✓
- Invariant 2: `precipitates_main=True` → `anagnorisis_event_id='E_oedipus_anagnorisis'` non-None; τ_s(9) < τ_s(13). ✓
- Invariant 3: `event_id='E_jocasta_realizes'` ≠ `anagnorisis_event_id='E_oedipus_anagnorisis'`. ✓
- Check 5: `character_ref_id='ar_jocasta'` resolves in `AR_OEDIPUS_MYTHOS.characters`. ✓

The probe's Oedipus dialect_reading named the pre-sketch-02 limit precisely: *"the Aristotelian frame has no native way to model staggered recognitions within a single mythos — anagnorisis_event_id is singular."* A11 closes the limit without retouching A4.

## Worked case — Oedipus under A12

Oedipus's peripeteia (`E_messenger_adoption_reveal`, τ_s=8) and anagnorisis (`E_oedipus_anagnorisis`, τ_s=13) are separated by five substrate steps. The probe flagged the action_summary's original claim of coincidence as prose in tension with the structural fields. An author-fix updated the prose before commit; the structural relation lives only in prose today.

```python
AR_OEDIPUS_MYTHOS = ArMythos(
    # ... fields unchanged ...
    peripeteia_anagnorisis_binding="separated",
    peripeteia_anagnorisis_adjacency_bound=3,
)
```

Verification (A7.8):

- Both event ids resolve in substrate. ✓
- `|τ_s(8) − τ_s(13)| = 5 > 3`. Consistent with `"separated"`. ✓

If an author later declares `"coincident"` while the fields still point at different events, A7.8 raises `advises-review` with code `peripeteia_anagnorisis_binding_inconsistent`.

## Worked case — Rashomon under A12 (null-case)

Each Rashomon testimony sets `peripeteia_event_id` to a testimony-specific event but `anagnorisis_event_id=None` (the probe noted *the absence of anagnorisis across all four mythoi is itself an Aristotelian finding*). A12's binding requires both to be non-None; the field stays at `None` for all four testimonies.

This is the intended behavior: A12 types the relation when both events exist; it says nothing about mythoi that decline to name recognition.

## Deferred extensions

### ArFrameMythos (Rashomon probe, deferred)

**Proposal:** encode Rashomon's frame narrative (gate, rain, priest, commoner, baby) as an outer mythos containing the four testimony mythoi, letting the frame's own beginning/middle/end and its cathartic arc find an Aristotelian home.

**Why deferred, not rejected:** the substrate has no frame events. State-of-play-02: "S_frame carries full Dramatica-8 declarations but no ACTIVE Lowerings — grove-only substrate scope." A dialect record with no substrate to bind is notation without content; the `central_event_ids` would be empty and every A7 check on it would be either vacuous or fail.

**Forcing function for reopening:** a Rashomon substrate extension adding frame events large enough to carry a beginning/middle/end scope. When that happens, A10's `"contains"` kind is pre-placed for the outer-to-inner relationship. Whether `ArFrameMythos` arrives as a specialization record (discriminator on `ArMythos`), a descriptor, or is subsumed entirely by A10's existing shape waits until the substrate work forces the choice.

### ArAnagnorisisLevel (Rashomon probe, rejected from sketch-02)

**Proposal:** a modifier distinguishing character-level recognition (Aristotle's native sense) from audience-level recognition (the spectator's realization that all testimony is self-serving).

**Why rejected from sketch-02:** aristotelian-sketch-01 A4 commits anagnorisis as **character-level** per Poetics 1452a; A8 commits audience response as **out of scope** in the same class as catharsis. The sketch acknowledged Rashomon's meta-anagnorisis as a genuine *dialect-scope limit* — *honest limits, sized by the theory itself, not by the architecture*.

Admitting `ArAnagnorisisLevel` widens the dialect's scope into reader-response territory sketch-01 deliberately closed. That is a sketch-01 amendment — revisiting A4 and A8 — not a sketch-02 extension. Any such revisit has to re-examine catharsis too (same class; same architectural stance).

The probe's `scope_limits_observed` finding for audience-level anagnorisis remains the correct dialect output: the dialect acknowledges what it does not cover. Keeping the scope-out surfaced as a limit is the feature, not the bug.

## Amendment to aristotelian-probe-sketch-01 predictions

Probe sketch-01 made five falsifiable predictions (P1–P5). P5 was exploratory: "Rashomon specifically surfaces `ArMythosRelation` as `relations_wanted`." The live probe returned `ArMythosRelation: a structural relation expressing that four mythoi share a canonical-floor beginning ...`. **P5 passed.** This sketch is the structural consequence — P5 produced its forcing function and this sketch closes it.

The Oedipus probe additionally surfaced two unpredicted relations_wanted entries (`ArAnagnorisisChain`, `ArPeripeteiaAnagnorisisBinding`). Sketch-01's Oedipus-side predictions (P1, P4) targeted prose-review quality and drift-avoidance; the dialect-reading's `relations_wanted` was not scoped by a specific prediction. Counting these as bonus probe-surfaced forcing functions rather than prediction-breakers.

## Architectural classification

Every commitment A10–A12 is **extension-only** on the dialect:

- A10 adds one new dialect record (`ArMythosRelation`) with encoding-scope authorship.
- A11 adds one new record (`ArAnagnorisisStep`) + one optional field on `ArMythos` (`anagnorisis_chain`), defaulting empty.
- A12 adds two optional fields on `ArMythos` (`peripeteia_anagnorisis_binding`, `peripeteia_anagnorisis_adjacency_bound`), defaulting `None` / `3`.

Zero modification to `ArPhase`, `ArCharacter`, `ArObservation`, or any A1–A9 field semantics. Zero modification to substrate, Dramatic, Save-the-Cat, substrate effects, or cross-boundary records. The `verify` signature gains two optional kwargs with empty defaults; call-sites that ignore A10–A12 see no behavior change.

Sketch-01's architectural verdict — *every commitment A1–A9 is extension-only; no core-record modification* — extends to A1–A12 under sketch-02. The sketch-01 stability signal holds.

## Open questions

1. **OQ1 — `mythoi_ids` canonical ordering.** The tuple is ordered only for `kind="contains"` (first = container). For `contests` / `parallel`, order is unspecified. Does a canonical ordering (e.g., lexicographic on mythos id) improve dedup / walker-display? Deferred until a second encoding authors a relation.
2. **OQ2 — Cross-mythos adjacency bound normalization.** A12's `peripeteia_anagnorisis_adjacency_bound` is per-mythos. If a future check reads across mythoi (e.g., "all mythoi in a contest relation should agree on binding kind"), bound aggregation rules would need defining. Not in scope here.
3. **OQ3 — Chain τ_s ordering.** `anagnorisis_chain` preserves authorial order. No invariant enforces τ_s-monotonic ordering across chain steps. Add if a future encoding suggests order matters.
4. **OQ4 — `precipitates_main` uniqueness.** A11 admits zero-or-more steps with `precipitates_main=True`. No invariant says at most one. If a forcing function surfaces — a mythos where exactly one of many realizations is cited as *the* trigger — tighten to at-most-one.
5. **OQ5 — Cross-encoding relations.** All A10 relations live within one encoding. Does a cross-encoding relation make sense (e.g., an Oedipus-vs-Ackroyd "narrator-is-the-killer" structural echo)? The cross-dialect Lowering sketch (architecture-sketch-02 A8) is the right home; A9 keeps cross-dialect out of the dialect.
6. **OQ6 — Schema-layer landing of A10–A12.** Deferred to a follow-on PFS arc. The Aristotelian schema subdir (`schema/aristotelian/`) ships three schemas today (ArMythos / ArPhase / ArCharacter). A10–A12 would add `ArMythosRelation` as a new schema file and amend `mythos.json` to admit the two new fields + the `anagnorisis_chain` array. Not covered by AA6–AA10; see AA11.

## Acceptance criteria

Labels AA6–AA11 continue sketch-01's AA1–AA5.

- **[AA6]** `prototype/story_engine/core/aristotelian.py` gains three additions: `ArMythosRelation` record, `ArAnagnorisisStep` record, and three new fields on `ArMythos` (`anagnorisis_chain`, `peripeteia_anagnorisis_binding`, `peripeteia_anagnorisis_adjacency_bound`). No change to pre-existing fields on `ArMythos`, `ArPhase`, `ArCharacter`, `ArObservation`, or to constant vocabularies.
- **[AA7]** `verify` signature extended with `mythoi` + `relations` kwargs (both default empty). Four new checker functions implementing A7.6–A7.9 (`_check_mythos_relations`, `_check_anagnorisis_chain`, `_check_peripeteia_anagnorisis_binding`, `_check_relation_event_refs`). New observation codes: `mythos_relation_kind_noncanonical`, `mythos_relation_mythoi_unresolved`, `mythos_relation_mythoi_too_few`, `mythos_relation_contests_event_absent`, `mythos_relation_contains_not_superset`, `mythos_relation_event_ref_unresolved`, `anagnorisis_step_event_not_central`, `anagnorisis_step_equals_main`, `anagnorisis_step_precipitates_without_main`, `anagnorisis_step_precipitates_ordering`, `anagnorisis_step_character_unresolved`, `peripeteia_anagnorisis_binding_invalid_value`, `peripeteia_anagnorisis_binding_inconsistent`, `peripeteia_anagnorisis_binding_event_unresolved`.
- **[AA8]** Encoding `prototype/story_engine/encodings/rashomon_aristotelian.py` gains `AR_RASHOMON_CONTEST` + `AR_RASHOMON_RELATIONS` tuple. Module docstring's current note flagging the relation as sketch-02-deferred is updated to point at the authored relation. No change to existing mythoi or the `AR_RASHOMON_MYTHOI` tuple shape.
- **[AA9]** Encoding `prototype/story_engine/encodings/oedipus_aristotelian.py` gains `AR_STEP_JOCASTA`; `AR_OEDIPUS_MYTHOS` grows `anagnorisis_chain=(AR_STEP_JOCASTA,)` and `peripeteia_anagnorisis_binding="separated"`. The module docstring notes the two sketch-02 extensions authored.
- **[AA10]** Tests in `prototype/tests/test_aristotelian.py` cover all four new checks and both encoding migrations: A7.6 structural integrity (kind vocabulary; mythoi_ids ≥ 2; event refs resolve; contests all-mythoi coverage; contains superset), A7.7 invariants 1–5, A7.8 consistency across all four enum values including inconsistent detection, A7.9 event-ref resolution, and backward-compatibility (encodings without A10–A12 verify identically to pre-sketch-02). Target: +12–18 tests.
- **[AA11]** Conformance test (`prototype/tests/test_production_format_sketch_01_conformance.py`) is NOT modified by this sketch. Schema-layer landing of A10–A12 is a separate production-format arc (follow-on PFS sketch), gated on a schema-layer decision about whether `ArMythosRelation` ships as its own schema file under `schema/aristotelian/` or is inlined into an extended `mythos.json`. That arc also adds the two new `ArMythos` fields to `mythos.json` and an `anagnorisis_chain` array schema. The Python prototype's Tier 2 conformance-test audits (branch-label audit, referential-integrity audits) continue to pass unmodified.

Post-sketch test totals update state-of-play counts. Baseline at sketch open: 755 passing.

## Summary

Three probe-surfaced dialect extensions close cleanly under sketch-01's extension-only discipline. `ArMythosRelation` types the Rashomon four-testimony contest structurally; `ArAnagnorisisStep` + `anagnorisis_chain` closes the Oedipus staggered-recognition limit; `peripeteia_anagnorisis_binding` makes the reversal/recognition relation machine-checkable. Two probe-surfaced candidates are held out with reasons — `ArFrameMythos` blocked by substrate absence; `ArAnagnorisisLevel` against sketch-01's scope.

Architectural verdict extends sketch-01's GREEN: commitments A1–A12 remain extension-only; no core-record modification; no substrate change; no new effect kind. The probe produced its forcing functions, this sketch closes the three well-forced ones, and the dialect grows without touching A1–A9.

If implementation of AA6–AA11 surfaces an extension that cannot be had as pure addition, halt and re-open the architectural question.
