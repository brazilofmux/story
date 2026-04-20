# Aristotelian dialect — sketch 03 (ArCharacterArcRelation + staged-chain step_kind)

**Status:** draft, active
**Date:** 2026-04-20
**Supersedes:** nothing (amendment, not consolidation)
**Extends:** [aristotelian-sketch-01](aristotelian-sketch-01.md) — commitments A1–A9 unchanged; [aristotelian-sketch-02](aristotelian-sketch-02.md) — commitments A10–A12 + A7.6–A7.9 unchanged except A11 step-kind soft-deprecation below
**Frames:** [architecture-sketch-02](architecture-sketch-02.md), [aristotelian-sketch-01](aristotelian-sketch-01.md), [aristotelian-sketch-02](aristotelian-sketch-02.md)
**Related:** [aristotelian-probe-sketch-03](aristotelian-probe-sketch-03.md) (banked OQ-AP5 + OQ-AP6 as source of sketch-03's forcing functions); `prototype/reader_model_hamlet_aristotelian_output.json` (the Hamlet live-probe artifact that closes the banked OQs); `prototype/story_engine/encodings/hamlet_aristotelian.py` (the fourth Aristotelian encoding and the sketch-03 forcing-function payload; contains author-banked `OQ_AP5..OQ_AP8_FINDING` prose constants this sketch dispositions)
**Superseded by:** nothing yet

## Purpose

Close two of the banked Aristotelian OQs — one from aristotelian-probe-sketch-03 (`OQ-AP6`, intra-mythos parallel-character-arc) and one from the Hamlet probe run (`OQ-AP10`, protagonist-scope anagnorisis chain) — and formally retire a third (`OQ-AP5`, fate-agent at dialect scope).

The sketch adds one new dialect-layer record (A13) and one enum-valued field on `ArAnagnorisisStep` (A14), with two new self-verifier checks (A7.10, A7.11). Commitments A1–A12 from sketches 01/02 are unchanged except A11's `precipitates_main` is marked soft-deprecated in favor of the new `step_kind` field; both continue to work, with `step_kind` taking precedence when set.

## Why now

The Hamlet Aristotelian encoding (Sessions 1–4 of the multi-session research arc) and its live probe (Session 5, commit `6e5e41c`, 2026-04-20) together deliver the corpus evidence the banked OQs required.

- **OQ-AP6 forcing criterion (sketch-02 / probe-sketch-03)**: "second encoding with ≥2 tragic heroes in a single mythos." Hamlet authors **three** ArCharacter records with `is_tragic_hero=True` (AR_HAMLET, AR_CLAUDIUS, AR_LAERTES). Criterion met with a margin — three, not two.
- **OQ-AP6 probe-direct hit**: the Hamlet probe's `relations_wanted` explicitly proposes `ArMythosRelation kind='parallel'` between Hamlet's and Laertes's revenge arcs, and the same probe's `scope_limits_observed` flags that the dialect has no structural primitive for ranking three competing `is_tragic_hero=True` claims within one mythos. Two independent probe surfaces of the same gap.
- **OQ-AP10 (NEW, Hamlet probe)**: probe's `relations_wanted` asks `anagnorisis_chain` be usable for **intra-character** staggering — Hamlet's three-stage epistemic progression (Ghost claim τ_s=1 → Mousetrap verification τ_s=6 → Laertes reveal τ_s=17). A11's current shape mechanically admits this (no invariant forbids same-character steps) but carries no structural distinction between "parallel-character recognition" (Lady Macbeth, Claudius-prays) and "same-character epistemic staging." The authoring pattern is ambiguous; A14 canonicalizes it.
- **OQ-AP5 retirement criterion**: two independent negative probe signals. The Witches (Macbeth probe, 2026-04-19) stayed below dialect surface; the Ghost (Hamlet probe, 2026-04-20) stayed below dialect surface. Both encodings' authors pre-banked the forcing pressure in prose (`OQ_AP5_FINDING` in hamlet_aristotelian.py; parallel Macbeth encoding note). Both probes read the fate-agent without demanding a typed dialect record. Under the sketch-02 forcing-function discipline, "no probe surfaces the pressure across two complementary encodings" is the retirement signal for a banked OQ.

Landing A13 + A14 now clears the probe's productive output; retiring OQ-AP5 keeps the OQ ledger honest. Two other Hamlet-author-banked OQs (AP7 numerical-range, AP8 same-beat) stayed below probe pressure and remain banked with explicit dispositions below.

## Scope — what this sketch does and doesn't do

**In scope:**

- `ArCharacterArcRelation` record expressing intra-mythos structural relations between two or more ArCharacter records within a single ArMythos.
- `step_kind` enum-valued field on `ArAnagnorisisStep` distinguishing parallel / precipitating / staging; soft-deprecation of `precipitates_main`.
- Two new self-verifier checks (A7.10 for ArCharacterArcRelation integrity; A7.11 for step_kind consistency).
- Encoding migration for Hamlet (A13 + A14 use). No migration of Oedipus / Rashomon / Macbeth — their existing A11 steps map cleanly to A14's derived defaults and no intra-mythos ArCharacterArcRelation is needed (Oedipus's Jocasta step is precipitating-by-different-character; Macbeth's Lady-Macbeth step is parallel-by-different-character; neither needs A13 — Lady Macbeth's structural relation to Macbeth is carried by the non-precipitating step, sketch-02 worked-case verified).
- Formal retirement of OQ-AP5 (ArFateAgent / ArProphecyStructure) with rationale.

**Out of scope:**

- OQ-AP7 (numerical-range of BINDING_SEPARATED). Author-banked in hamlet_aristotelian.py but the probe did not pressure it. Stays banked; see §Deferred.
- OQ-AP8 (same-beat staggered recognition — Laertes's deathbed recognition at τ_s=17 compressed into the same event as Hamlet's main anagnorisis). A11 invariant 3 forbids chain steps at the main event; the probe did not pressure relaxation. Stays banked; see §Deferred.
- OQ-AP9 (audience-level dramatic irony). Four surfacings across Rashomon-v1, Rashomon-v2, Macbeth, Hamlet. Still against sketch-01 A4/A8 scope (reader-response territory); would be a sketch-01 amendment, not a sketch-03 extension. Stays scope-rejected; fourth re-surfacing strengthens the rejection-as-stance by consensus across four encodings.
- OQ-AP1 (typed ArPathos / ArCatharsisLevel). Third independent signal (Macbeth scattered pathos; Hamlet scattered pathos; Hamlet polis-level catharsis inflection). Each signal is distinct; a fourth *convergent* signal is the forcing criterion. Stays banked.
- Schema-layer landing of A13 + A14 under `schema/aristotelian/`. Follow-on production-format sketch, gated on A14's step_kind → fields-on-existing-schema question; see AA15.
- Changes to core records (`ArMythos.plot_kind` enum, `ArPhase.role` enum, `ArCharacter` shape, `ArObservation` severity set). Changes to A1–A9 commitment semantics. Changes to A10 (ArMythosRelation stays inter-mythos; A13 covers intra-mythos).
- Cross-dialect Lowering (A9 unchanged).

## Commitments

Labels A13–A14 continue sketches 01/02's A1–A12 numbering. A7.10–A7.11 extend A7's numbered check list (sketch-02 committed A7.6–A7.9).

### A13 — ArCharacterArcRelation expresses intra-mythos parallel character arcs

```python
@dataclass(frozen=True)
class ArCharacterArcRelation:
    id: str
    kind: str                              # canonical-plus-open
    character_ref_ids: Tuple[str, ...]     # ≥ 2 character ids within one mythos
    mythos_id: str                         # the containing mythos
    over_event_ids: Tuple[str, ...] = ()   # substrate events where arcs track/mirror
    annotation: str = ""
```

**Canonical kind vocabulary:**

- `"parallel"` — two or more character arcs run within one mythos without precipitation between them: each arc carries its own hamartia, recognition, and fall. Umbrella kind; used when the structural parallelism is the relation's content, without a more specific sub-shape.
- `"mirror"` — two arcs structurally inverted over shared pressure: both sons avenging murdered fathers (Hamlet / Laertes); both pursuing fate-agent's commission via opposite temperaments (Macbeth / Banquo, a hypothetical — not authored in the current corpus). Implies parallelism *plus* structural symmetry.
- `"foil"` — two arcs structurally opposed over shared pressure: will-to-act vs. will-to-retain (Hamlet / Claudius); moral clarity vs. moral bankruptcy (Cordelia / Goneril, hypothetical). Implies parallelism *plus* structural opposition.

**Canonical-plus-open discipline** (matches A10's): non-canonical `kind` values are accepted at severity `noted` (not `advises-review`). Authors can experiment without a dialect amendment.

**Forward-vocabulary note.** Only `"mirror"` has direct corpus use today (Hamlet-Laertes). `"parallel"` is umbrella; `"foil"` ships forward-compatibly (Hamlet-Claudius is the first candidate, authored below). Additional kinds (`doubled-fall` for three-way simultaneous catastrophe; `shadow` for Jungian pairing) are explicitly **not** canonical today — see OQ8 below. This matches sketch-02 A10's shipping pattern: ship only vocabulary with corpus pressure, accept experimentation via noted severity, re-canonicalize when forcing functions arrive.

**A13 placement.** `ArCharacterArcRelation` records live at encoding scope alongside any `ArMythosRelation` records (parallel to how `AR_RASHOMON_RELATIONS` is a module-scope tuple). Authors maintain an `AR_*_CHARACTER_ARC_RELATIONS` tuple and pass it to `verify`.

**Architectural classification: extension.** New dialect-layer record. N-ary via `character_ref_ids` tuple. Intra-mythos by construction (one `mythos_id`, not a mythoi tuple). Substrate-agnostic (`over_event_ids` references checked only when substrate threaded through).

**Distinguished from A10.** A10's `ArMythosRelation` ties ≥2 ArMythos records; A13's `ArCharacterArcRelation` ties ≥2 ArCharacter records *within one ArMythos*. The two records address orthogonal axes: inter-mythos structural friction (Rashomon's four testimonies contest) vs. intra-mythos character-arc parallelism (Hamlet's three tragic heroes mirror / foil). Neither can express the other's gap.

### A14 — step_kind field on ArAnagnorisisStep; soft-deprecation of precipitates_main

```python
@dataclass(frozen=True)
class ArAnagnorisisStep:
    id: str
    event_id: str                          # substrate event: the realization moment
    character_ref_id: str                  # who realizes — required (unchanged from A11)
    precipitates_main: bool = False        # SOFT-DEPRECATED — see below
    step_kind: str = ""                    # NEW — "parallel" | "precipitating" | "staging"; empty = derive
    annotation: str = ""
```

A11's `precipitates_main` binary conflates two orthogonal dimensions: (a) whether this step's recognition causes the main mythos anagnorisis, and (b) whether this step is by the same character as the main anagnorisis. The probe's OQ-AP10 pressure is exactly the dimension-(b) gap: Hamlet's three-stage epistemic progress is same-character, each step does causally contribute to the final, but the pattern is structurally distinct from Jocasta-causing-Oedipus (different character, precipitating) and from Lady-Macbeth-parallel (different character, non-precipitating).

**Canonical step_kind values:**

- `"parallel"` — different-character-from-main, non-precipitating. Lady Macbeth's sleepwalking (Macbeth); Claudius's prayer-scene (Hamlet). Derived default when `step_kind=""` and `precipitates_main=False` and step's character ≠ main-anagnorisis-character.
- `"precipitating"` — different-character-from-main, causally precipitating the main. Jocasta's realization (Oedipus). Derived default when `step_kind=""` and `precipitates_main=True`.
- `"staging"` — **NEW** — same-character-as-main, epistemic waypoint on that character's staged coming-to-know. Hamlet's Ghost-claim step; Hamlet's Mousetrap-verification step. Has no pre-sketch-03 authoring pattern; requires explicit `step_kind="staging"` to declare.

**Back-compat derivation (when `step_kind=""`):**

```python
if step_kind == "":
    if character_ref_id == main_anagnorisis_character_ref_id:
        derived = "staging"
    elif precipitates_main:
        derived = "precipitating"
    else:
        derived = "parallel"
```

This requires a way to know who the main anagnorisis character is. A14 adds a second optional field on ArMythos:

```python
@dataclass(frozen=True)
class ArMythos:
    # ... existing fields unchanged ...
    anagnorisis_character_ref_id: Optional[str] = None
```

When `anagnorisis_character_ref_id` is None, `step_kind=""` cannot distinguish "staging" from "parallel" structurally; A7.11 treats the empty case as deriving to "parallel" (conservative — forces authors to opt in to "staging" explicitly when the main character isn't named). All pre-sketch-03 encodings ship with `anagnorisis_character_ref_id=None`; their existing steps all derive to "parallel" or "precipitating" (none were same-character-as-main) and A7.7 behavior is unchanged for them.

**A14 invariants (A7.11 enforces):**

1. If `step_kind` is non-empty, it must be in `{"parallel", "precipitating", "staging"}` — invalid values emit `severity=advises-review` with code `anagnorisis_step_kind_invalid`.
2. If `step_kind == "staging"`: `anagnorisis_character_ref_id` must be non-None on the enclosing mythos; the step's `character_ref_id` must equal it. Violations: `anagnorisis_step_staging_character_mismatch` (advises-review) or `anagnorisis_step_staging_requires_main_character` (advises-review).
3. If `step_kind == "precipitating"`: `precipitates_main` must be True. Code: `anagnorisis_step_kind_precipitates_mismatch` (noted when `step_kind` set explicitly and `precipitates_main` contradicts).
4. If `step_kind == "parallel"`: `precipitates_main` must be False. Code: same.
5. If `step_kind == "staging"`: `precipitates_main` must be True. **Staging steps precipitate by definition** — they are the same character's epistemic waypoints on the path to their own main anagnorisis; each step contributes causally to the final recognition. Code: same. This invariant also preserves the pre-sketch-03 reader contract: any existing call site that reads only `step.precipitates_main` continues to see True for every staging step and thus correctly classifies it as "causes the main" (losing only the staging-vs-precipitating distinction, which is new information the old reader did not expect).
6. For all staging steps: the step's τ_s must be strictly less than the main anagnorisis event's τ_s (epistemic waypoints precede the recognition). Enforceable when substrate threaded; skips otherwise. Code: `anagnorisis_step_staging_ordering`.

**Soft-deprecation of `precipitates_main`.** Existing call sites reading `step.precipitates_main` continue to work *and stay semantically honest* under A14. Invariants 3 / 4 / 5 (above) require `precipitates_main=True` for both precipitating and staging kinds, and `False` for parallel — so any old reader classifying a step as "causes the main" iff `precipitates_main` is True gets the correct answer for every sketch-03 encoding. The information the old reader *cannot* extract is the staging-vs-precipitating distinction, which is the new dimension A14 introduces — and that is correct: the old reader was not told about it, and would not expect to see it. New encodings should set `step_kind` directly; `precipitates_main` remains as an authorial redundancy the verifier enforces consistency on. A future sketch (sketch-04 or later) may remove `precipitates_main` once the corpus has migrated; no commitment here.

**A11 invariant 3 unchanged.** "A step's `event_id` must not equal `anagnorisis_event_id`" holds under A14. Staging steps are strictly earlier than the main; they are not the main. (OQ-AP8's same-beat staggered recognition, which *would* require relaxing invariant 3, remains out of scope — see §Deferred.)

**Architectural classification: extension.** One new optional field on `ArAnagnorisisStep` (`step_kind`, empty-string default). One new optional field on `ArMythos` (`anagnorisis_character_ref_id`, None default). `precipitates_main` semantics preserved; all pre-sketch-03 encodings verify identically.

### A7.10 — ArCharacterArcRelation structural integrity

For each `ArCharacterArcRelation`:

1. `kind` in canonical set `{"parallel", "mirror", "foil"}` — non-canonical values emit `severity=noted` with code `character_arc_relation_kind_noncanonical`.
2. `character_ref_ids` has ≥ 2 entries. Violation: `character_arc_relation_refs_too_few` (advises-review).
3. All character ids resolve to `ArCharacter` records within the mythos named by `mythos_id` (requires `mythoi` kwarg to find the mythos; requires the mythos to carry non-empty `characters` tuple). Violations: `character_arc_relation_character_unresolved` (advises-review) or `character_arc_relation_mythos_unresolved` (advises-review).
4. Every event id in `over_event_ids` resolves in substrate events when substrate threaded. Code: `character_arc_relation_event_ref_unresolved`. Skips when substrate empty (consistent with A7 check 4 / A7.9 discipline).

### A7.11 — ArAnagnorisisStep step_kind consistency

Enforces the five A14 invariants (above). Skip conditions parallel A7.7 (a non-precipitating step is always verifiable; precipitating / staging steps that require substrate skip when substrate absent).

### A7 orchestration — verify signature extension

```python
def verify(
    mythos: ArMythos,
    *,
    substrate_events: tuple = (),
    mythoi: Tuple[ArMythos, ...] = (),
    relations: Tuple[ArMythosRelation, ...] = (),
    character_arc_relations: Tuple[
        ArCharacterArcRelation, ...
    ] = (),                                              # NEW (A7.10)
) -> list:
    ...
```

One new kwarg, empty-tuple default. Callers not adopting A13 change nothing; A7.10 skips on empty input. A7.11 runs on the enclosing mythos's `anagnorisis_chain` without a new kwarg (the chain is already on the mythos). `group_by_severity` / `group_by_code` unchanged.

## Worked case — Hamlet under A13

Hamlet authors three ArCharacter records, all `is_tragic_hero=True` (AR_HAMLET, AR_CLAUDIUS, AR_LAERTES). The three-way parallelism has two structural sub-relations that sketch-03 admits:

```python
AR_HAMLET_LAERTES_MIRROR = ArCharacterArcRelation(
    id="arc_hamlet_laertes_mirror",
    kind="mirror",
    character_ref_ids=("ar_hamlet", "ar_laertes"),
    mythos_id="ar_hamlet",
    over_event_ids=(
        "E_hamlet_meets_ghost",      # (Ghost's commission — Hamlet's revenge ground)
        "E_hamlet_kills_polonius",   # (Laertes's father, Hamlet's deed — the mirror's trigger)
        "E_ophelia_drowns",
        "E_laertes_returns",
        "E_duel_plotted",
        "E_duel_begins",
        "E_hamlet_laertes_wounded",
        "E_laertes_reveals_plot",
        "E_laertes_dies",
        "E_hamlet_dies",
    ),
    annotation=(
        "Hamlet and Laertes mirror each other as sons avenging "
        "murdered fathers. The structural inversion: Hamlet's "
        "revenge proceeds via delay, verification, and internal "
        "dialogue with moral scruple; Laertes's proceeds via "
        "immediate return and immediate commitment to violent "
        "action. Both fathers killed by Claudius's agency (King "
        "Hamlet directly; Polonius indirectly via the arras-stabbing "
        "Claudius provoked Hamlet toward). Both sons die at the end "
        "having accomplished the revenge; Laertes recognizes his "
        "pawn-status in the same beat that reveals the shape of "
        "Claudius's plot to Hamlet. The mirror is not decorative — "
        "it is what makes the duel-plot work dramatically, and it "
        "is what the play's catharsis depends on. Structural "
        "parallelism of this weight belongs at dialect scope; "
        "hamartia_text prose alone cannot render it to the walker."
    ),
)

AR_HAMLET_CLAUDIUS_FOIL = ArCharacterArcRelation(
    id="arc_hamlet_claudius_foil",
    kind="foil",
    character_ref_ids=("ar_hamlet", "ar_claudius"),
    mythos_id="ar_hamlet",
    over_event_ids=(
        "E_king_hamlet_poisoned",
        "E_claudius_crowned",
        "E_mousetrap_performance",
        "E_claudius_prays",
        "E_hamlet_kills_claudius",
    ),
    annotation=(
        "Hamlet and Claudius are structurally opposed tragic heroes: "
        "Hamlet's hamartia is failure-of-action (scruple, delay, "
        "'enterprise of great pith and moment / lose the name of "
        "action'); Claudius's is failure-of-renunciation (will to "
        "retain the crime's gains while knowing the moral cost — "
        "'may one be pardon'd and retain the offence?'). Each "
        "recognizes the other's failure in the moment of their own "
        "catastrophe: Claudius's prayer-scene names Hamlet as "
        "the scourge he has earned; Hamlet's final killing of "
        "Claudius is the act his hamartia delayed throughout. Foil, "
        "not mirror: the structural shape is opposition, not "
        "symmetry."
    ),
)

AR_HAMLET_CHARACTER_ARC_RELATIONS = (
    AR_HAMLET_LAERTES_MIRROR,
    AR_HAMLET_CLAUDIUS_FOIL,
)
```

Verification:

```python
verify(
    AR_HAMLET_MYTHOS,
    substrate_events=FABULA,
    mythoi=(AR_HAMLET_MYTHOS,),
    character_arc_relations=AR_HAMLET_CHARACTER_ARC_RELATIONS,
)
```

A7.10 passes on both records: `kind` canonical; two character ids per relation resolve in `AR_HAMLET_MYTHOS.characters`; `mythos_id` resolves via the `mythoi` kwarg; all `over_event_ids` resolve in FABULA.

The probe's two surfaces of OQ-AP6 — the `relations_wanted` parallel-arc proposal and the `scope_limits_observed` three-way tragic-hero flag — close cleanly under A13. Hamlet's three-way parallelism is expressed as two pairwise relations (mirror + foil), which matches the probe's language (the probe's proposal was explicitly pairwise: "between Hamlet's and Laertes's revenge paths"). A three-way single relation could be authored (`character_ref_ids=(ar_hamlet, ar_claudius, ar_laertes)`) but would lose the mirror-vs-foil distinction the probe's scope_limits named. Pairwise decomposition is the honest encoding.

## Worked case — Hamlet under A14

Hamlet's anagnorisis_chain in the current encoding (`hamlet_aristotelian.py`) authors one step: `AR_STEP_CLAUDIUS_PRAYS`, non-precipitating, Claudius. The probe's OQ-AP10 pressure asks for protagonist-scope staging — Hamlet's own three-stage epistemic progression. Under A14:

```python
# ArMythos gains one field assignment:
AR_HAMLET_MYTHOS = ArMythos(
    # ... existing fields unchanged ...
    anagnorisis_event_id="E_laertes_reveals_plot",         # unchanged
    anagnorisis_character_ref_id="ar_hamlet",              # NEW (A14)
    anagnorisis_chain=(
        AR_STEP_HAMLET_GHOST_CLAIM,                        # NEW
        AR_STEP_HAMLET_MOUSETRAP,                          # NEW
        AR_STEP_CLAUDIUS_PRAYS,                            # unchanged
    ),
)

AR_STEP_HAMLET_GHOST_CLAIM = ArAnagnorisisStep(
    id="arstep_hamlet_ghost_claim",
    event_id="E_hamlet_meets_ghost",                       # τ_s=1
    character_ref_id="ar_hamlet",
    step_kind="staging",
    precipitates_main=True,    # derivable, but set explicitly for honesty
    annotation=(
        "Hamlet's first epistemic waypoint: the Ghost's direct "
        "revelation of Claudius's guilt. Not the recognition — "
        "Hamlet holds it provisionally ('the spirit that I have "
        "seen / May be the devil'), does not yet act on it, requires "
        "corroboration via the Mousetrap. Structurally: the "
        "commission grounds the action, but the knowledge stays "
        "tentative until verified. First of three staging steps "
        "culminating in the main anagnorisis at E_laertes_reveals_plot."
    ),
)

AR_STEP_HAMLET_MOUSETRAP = ArAnagnorisisStep(
    id="arstep_hamlet_mousetrap",
    event_id="E_mousetrap_performance",                    # τ_s=6
    character_ref_id="ar_hamlet",
    step_kind="staging",
    precipitates_main=True,
    annotation=(
        "Hamlet's second epistemic waypoint: the Mousetrap "
        "performance converts the Ghost's claim from tentative-"
        "revelation to verified-certainty. 'I'll take the ghost's "
        "word for a thousand pound.' Second staging step; narrows "
        "the remaining epistemic gap to the structural shape of "
        "Claudius's response (which Hamlet does not yet understand "
        "is a counter-plot in motion). Precedes the main anagnorisis "
        "at τ_s=17 by 11 τ_s-steps."
    ),
)

AR_STEP_CLAUDIUS_PRAYS = ArAnagnorisisStep(
    id="arstep_claudius_prays",
    event_id="E_claudius_prays",                           # τ_s=7
    character_ref_id="ar_claudius",
    step_kind="parallel",       # derivable, set explicitly
    precipitates_main=False,
    annotation=(
        # unchanged from pre-sketch-03 encoding
        ...
    ),
)
```

Verification (A7.11) on the three steps:

- AR_STEP_HAMLET_GHOST_CLAIM: `step_kind="staging"` → invariant 2 (staging character-match): `anagnorisis_character_ref_id="ar_hamlet"` is non-None and equals step's `character_ref_id`. ✓ Invariant 5 (staging must precipitate): `precipitates_main=True`. ✓ Invariant 6 (staging ordering): τ_s(1) < τ_s(17). ✓
- AR_STEP_HAMLET_MOUSETRAP: same shape. τ_s(6) < τ_s(17). ✓
- AR_STEP_CLAUDIUS_PRAYS: `step_kind="parallel"`, `character_ref_id="ar_claudius"` ≠ `anagnorisis_character_ref_id="ar_hamlet"` (as expected for parallel). ✓ Invariant 4: `precipitates_main=False`. ✓

The three-step chain now structurally expresses both the Hamlet staged-coming-to-know and Claudius's parallel-character-recognition — orthogonal axes, both carried by A14's `step_kind` vocabulary. The probe's OQ-AP10 gap ("anagnorisis_chain can't express Hamlet's staged epistemic progression") closes.

**Note on authoring migration.** The sketch-03 encoding update replaces the single `AR_STEP_CLAUDIUS_PRAYS` entry with the three-step chain. `AR_STEP_CLAUDIUS_PRAYS` itself gains `step_kind="parallel"` (derivable from pre-sketch-03 `precipitates_main=False` + different character, but set for clarity). Pre-sketch-03 behavior is preserved: a Hamlet encoding frozen at sketch-02 surface would still verify cleanly — adding staging steps is additive, not replacing.

## Deferred extensions

### OQ-AP1 — typed ArPathos / ArCatharsisLevel (stays banked)

**Proposal signals (three independent):** (a) Macbeth probe-sketch-03: scattered pathos across E_macduff_family_killed + E_lady_macbeth_dies + E_macbeth_killed (absorbed cleanly, no forcing). (b) Hamlet author-note: implicit cluster pathos across duel-beat deaths. (c) Hamlet probe Session 5: polis-level catharsis inflection (Fortinbras / succession vacuum) vs. catharsis from protagonist's fall alone.

**Why deferred:** three signals, each *distinct*. A typed ArPathos addressing scatter (signal a) is a different extension from typed ArCatharsisLevel addressing audience-response-level (signal c); signal (b) overlaps (a). The three are not convergent on a single forcing function. A fourth signal that converges with one of the existing three is the forcing criterion.

**Forcing function for reopening:** a fourth Aristotelian probe-surfaced signal that (i) re-surfaces scattered pathos as structurally under-served *and* (ii) asks for a typed record, not prose. OR a cross-dialect Lowering pressure to bind Dramatica's Impact Character resolution quality to a typed ArPathos/ArCatharsis property.

### OQ-AP7 — numerical range of BINDING_SEPARATED (stays banked)

**Proposal:** distinguish near-separated (distance 4–10) from distant-separated (>10) at A12's field, or add a raw `peripeteia_anagnorisis_distance` alongside the categorical binding.

**Why deferred:** author-flagged in hamlet_aristotelian.py but the probe did not pressure the range. Hamlet's distance 9 (the widest in corpus) verified clean under A12's coarse categorical, and the probe's `scope_limits_observed` / `relations_wanted` did not surface the distinction. The forcing pressure is authorial intuition ("Hamlet's 9 is structurally heavier than Oedipus's 5") not probe-surfaced.

**Forcing function for reopening:** (a) a probe surfaces the near-vs-distant distinction on a future encoding, or (b) a walker / prose-export consumer needs to render the distinction authoritatively (currently handled by `peripeteia_anagnorisis_adjacency_bound` being per-mythos, which already lets authors scale the threshold).

### OQ-AP8 — same-beat staggered recognition (stays banked)

**Proposal:** relax A11 invariant 3 ("step's event_id must not equal anagnorisis_event_id") to admit Laertes's deathbed self-recognition at E_laertes_reveals_plot (τ_s=17, the same event as Hamlet's main anagnorisis). Author-flagged in hamlet_aristotelian.py.

**Why deferred:** the probe did not pressure relaxation. Invariant 3 carries a legitimate semantic content (the main recognition is *the* main recognition; chain steps are *additional* moments). Relaxing it to admit same-event chain steps requires a new invariant about within-event ordering by character-subject identity — workable but not corpus-pressured today.

**Forcing function for reopening:** (a) a probe on a future encoding proposes a same-event chain step structurally, or (b) a second author-banked same-event case emerges (King Lear's dying recognition coincident with Cordelia's death-revelation could be a candidate; currently no Lear encoding exists).

### OQ-AP9 — audience-level dramatic irony / meta-anagnorisis (scope-rejected, not banked)

**Proposal signals (four independent):** Rashomon-v1 relations_wanted; Rashomon-v2 probe; Macbeth probe-sketch-03 scope_limits; Hamlet probe Session 5 scope_limits. Each surfaces the same gap: Aristotelian anagnorisis is character-level; dialect has no primitive for audience epistemic position.

**Why scope-rejected (not banked):** sketch-01 A4 committed anagnorisis as character-level per Poetics 1452a; A8 committed audience response as out-of-scope in the same class as catharsis. Admitting audience-level structure reopens A4 and A8, which is a sketch-01 amendment, not a sketch-03 extension. Four re-surfacings across four independent encodings strengthens the scope-rejection stance by consensus — the dialect consistently acknowledges what it does not cover, and the acknowledgment is the feature.

**Interpretation for future sketches.** If a future arc revisits sketch-01 A4/A8 (a substantive architectural question requiring its own sketch), the four-point re-surfacing ledger is the strongest case for opening it. Not a sketch-03 concern.

## Retired — OQ-AP5 (fate-agent at dialect scope)

**Original proposal (aristotelian-probe-sketch-03 §Finding 2):** typed ArFateAgent or ArProphecyStructure record for supernatural / equivocating causal agents — Macbeth's Witches, Hamlet's Ghost, hypothetical Cassandra / Greek chorus.

**Retirement rationale:** two independent negative probe signals.

- **Macbeth probe (2026-04-19, probe-sketch-03):** the probe read the Witches structurally without proposing a typed record; the fate-agent function was carried at substrate (via observe-only `apparition_of` predicates, content predicates on held sets) and at hamartia_text prose. No dialect pressure.
- **Hamlet probe (2026-04-20, Session 5):** the probe read the Ghost structurally without proposing a typed record; the fate-agent function again carried entirely at substrate (via `apparition_of`, `ghost_claims_killed_by`, `ghost_demands_revenge`, `poisoned_in_ear` predicates) and at hamartia_text prose. No dialect pressure.

Both author-banked `OQ_AP5_FINDING` prose constants (Macbeth's parallel and Hamlet's in `hamlet_aristotelian.py` lines 489–513) claimed the pressure existed; both probes read the encodings without demanding a dialect record. The sketch-02 forcing-function discipline names "no probe surfaces the pressure across two complementary encodings" as the retirement signal — which is what has happened.

**Retirement content:** OQ-AP5 moves off the banked-OQ list. The fate-agent function is recorded as **correctly substrate-only** — an Aristotelian-dialect observation about substrate-layer causal mechanics, not a dialect extension. Future encodings with fate-agent structure (hypothetical Cassandra, Oedipus-via-Delphi, Aeschylus's trilogy) should not re-raise OQ-AP5 without new probe-surfaced pressure; the retirement is based on two-encoding probe silence, not author hesitation.

**OQ-AP5's text stays in the record.** The `OQ_AP5_FINDING` prose constants in `hamlet_aristotelian.py` and (parallel) `macbeth_aristotelian.py` are cross-session artifacts documenting the authorial pressure — they capture what the encodings surfaced even if the probes did not pressure dialect-level closure. No action on the constants beyond updating the prose to mention the sketch-03 retirement.

## Amendment to aristotelian-probe-sketch-03 predictions

Probe-sketch-03 banked two new OQs post-Macbeth-probe: OQ-AP5 (supernatural agency) and OQ-AP6 (intra-mythos parallel-character-arc).

- **OQ-AP6 forcing criterion closed by Hamlet probe.** Probe-sketch-03 named the forcing function: "second encoding with ≥2 tragic heroes in a single mythos (Hamlet, Lear)." Hamlet delivered three; the probe's own `relations_wanted` made the ask explicit. This sketch closes.
- **OQ-AP5 forcing criteria unmet.** Probe-sketch-03 named the forcing function: "(a) second encoding with fate-agent ambiguity, (b) cross-dialect Lowering pressure, or (c) verifier check for probability-vs-equivocation." Hamlet delivered (a) — the Ghost is a second fate-agent in corpus. But the Ghost's posture is *direct revelation + commission* (no equivocation), structurally different from the Witches' *equivocating prophecy*. The two fate-agents span the Aristotelian causal-agency space orthogonally rather than convergently. And the critical signal — (a)-with-probe-pressure — did not materialize: neither probe flagged fate-agent as dialect-level gap. Retirement is the honest outcome.

The Hamlet probe also surfaced two OQs probe-sketch-03 did not anticipate: OQ-AP9 (dramatic irony, treated here as fourth surfacing of the Rashomon-originated audience-level pressure) and OQ-AP10 (protagonist-scope anagnorisis chain, closed by A14).

## Architectural classification

Every commitment A13–A14 is **extension-only** on the dialect:

- A13 adds one new dialect record (`ArCharacterArcRelation`) with encoding-scope authorship.
- A14 adds one optional field on `ArAnagnorisisStep` (`step_kind`, empty-string default) and one optional field on `ArMythos` (`anagnorisis_character_ref_id`, None default). `precipitates_main` semantics unchanged for existing encodings; new encodings can rely on `step_kind` alone.

Zero modification to A1–A12 field semantics (A11 invariants 1/2/3 hold; `precipitates_main` is soft-deprecated but functional). Zero modification to substrate, Dramatic, Save-the-Cat, substrate effects, or cross-boundary records. The `verify` signature gains one optional kwarg (`character_arc_relations`) with empty default; call-sites that ignore A13 see no behavior change; A7.10 skips on empty input. A7.11 runs over existing `anagnorisis_chain` but all checks derive their decisions from the new `step_kind` field which is empty-string for pre-sketch-03 steps, producing derived values consistent with pre-sketch-03 `precipitates_main` semantics.

Sketch-01 + sketch-02's architectural verdict — *every commitment A1–A12 is extension-only; no core-record modification* — extends to A1–A14 under sketch-03. The stability signal continues; the dialect has now absorbed fourteen commitments across three sketches without modifying a single pre-existing field's semantics.

## Open questions

1. **OQ7 — Three-way character-arc relations.** A13 admits `character_ref_ids` tuples of any length ≥ 2. Hamlet's three-way parallelism is authored pairwise (mirror + foil) rather than as a single three-way relation. Is a three-way `("ar_hamlet", "ar_claudius", "ar_laertes")` relation with `kind="parallel"` equivalent to the two pairwise authorings plus an implicit Laertes-Claudius relation? Deferred until a second encoding authors a three-way relation with structurally-distinct-from-pairwise content.
2. **OQ8 — Additional canonical kind vocabulary.** `doubled-fall` (three-way catastrophe-shape) and `shadow` (Jungian pairing) are candidates but lack corpus pressure. Mirror and foil have one corpus use each (Hamlet); parallel is umbrella. If a second encoding authors a `kind` the current canonical set doesn't cover, revisit.
3. **OQ9 — Redundancy between A13 and A11 staging steps.** Hamlet-Laertes mirror (A13) and hypothetical Laertes-staging step at Laertes-recognition (A11 staging — blocked by OQ-AP8 invariant-3 bar) would be different surfaces on overlapping content. Not redundant today (A13 ships, OQ-AP8 stays banked), but if OQ-AP8 opens, coordinate the two surfaces explicitly.
4. **OQ10 — precipitates_main final deprecation.** A14 soft-deprecates; eventual removal awaits corpus migration to `step_kind`. A future sketch may remove the field once all encodings set `step_kind` directly. No sketch-03 commitment.
5. **OQ11 — Cross-encoding character-arc relations.** All A13 relations live within one mythos. Does a cross-encoding relation make sense (a corpus-level claim that Hamlet-Laertes mirrors Oedipus-no-one, i.e., the absence of a mirror is itself a structural claim)? The cross-dialect Lowering (architecture-sketch-02 A8) is the right home; A9 keeps cross-dialect out of the dialect.
6. **OQ12 — Schema-layer landing.** Deferred to a follow-on PFS arc. A13 would add `ArCharacterArcRelation` as a new schema file under `schema/aristotelian/`. A14 would extend `mythos.json` with one new optional field (`anagnorisis_character_ref_id`) and `anagnorisis_step.json` with one new optional field (`step_kind`). Not covered by AA12–AA17; see AA15.
7. **OQ13 — Same-character non-precipitating steps (the fourth cell).** A14's invariants forbid the combination `step_kind="staging"` + `precipitates_main=False` (invariant 5) and require staging steps to be same-character (invariant 2); no step_kind admits same-character + non-precipitating. The structural gap: a character's *false* recognition (a premature claim of understanding that does not contribute to their true anagnorisis) is same-character, non-precipitating, and currently unencodable under A14. No corpus pressure today. Forcing function for reopening: an encoding with a structurally load-bearing false-recognition moment (Hamlet's own closet-scene "one may smile, and smile, and be a villain" is a candidate that today is carried in prose, not as a chain step).

## Acceptance criteria

Labels AA12–AA17 continue sketches 01/02's AA1–AA11.

- **[AA12]** `prototype/story_engine/core/aristotelian.py` gains one new record (`ArCharacterArcRelation`) + one optional field on `ArAnagnorisisStep` (`step_kind`) + one optional field on `ArMythos` (`anagnorisis_character_ref_id`). No change to pre-existing fields on `ArMythos`, `ArPhase`, `ArCharacter`, `ArObservation`, `ArMythosRelation`, or to A1–A12 constant vocabularies.
- **[AA13]** `verify` signature extended with `character_arc_relations` kwarg (default empty tuple). Two new checker functions implementing A7.10–A7.11 (`_check_character_arc_relations`, `_check_anagnorisis_step_kind`). New observation codes: `character_arc_relation_kind_noncanonical`, `character_arc_relation_refs_too_few`, `character_arc_relation_character_unresolved`, `character_arc_relation_mythos_unresolved`, `character_arc_relation_event_ref_unresolved`, `anagnorisis_step_kind_invalid`, `anagnorisis_step_staging_character_mismatch`, `anagnorisis_step_staging_requires_main_character`, `anagnorisis_step_kind_precipitates_mismatch`, `anagnorisis_step_staging_ordering`.
- **[AA14]** Encoding `prototype/story_engine/encodings/hamlet_aristotelian.py` gains `AR_STEP_HAMLET_GHOST_CLAIM`, `AR_STEP_HAMLET_MOUSETRAP`, `AR_HAMLET_LAERTES_MIRROR`, `AR_HAMLET_CLAUDIUS_FOIL`, `AR_HAMLET_CHARACTER_ARC_RELATIONS` tuple. `AR_HAMLET_MYTHOS` grows `anagnorisis_character_ref_id="ar_hamlet"`, expanded `anagnorisis_chain` tuple. `AR_STEP_CLAUDIUS_PRAYS` gains `step_kind="parallel"` (derivable but explicit). Module docstring references sketch-03 extensions; `OQ_AP5_FINDING` prose constant updated to note the sketch-03 retirement.
- **[AA15]** Conformance test (`prototype/tests/test_production_format_sketch_01_conformance.py`) is NOT modified by this sketch. Schema-layer landing of A13 + A14 is a separate production-format arc (follow-on PFS sketch). That arc ships `schema/aristotelian/character_arc_relation.json` + extends `schema/aristotelian/mythos.json` and `schema/aristotelian/anagnorisis_step.json` with the two new optional fields. The Python prototype's Tier 2 conformance-test audits continue to pass unmodified.
- **[AA16]** Tests in `prototype/tests/test_aristotelian.py` cover both new checks and the Hamlet encoding migration: A7.10 structural integrity (kind vocabulary; character_ref_ids ≥ 2; mythos_id resolves; over_event_ids resolve), A7.11 invariants (step_kind vocabulary; staging character-match; staging ordering; precipitates_main consistency across all three kinds), and backward-compatibility (pre-sketch-03 encodings without step_kind / anagnorisis_character_ref_id verify identically to sketch-02 baseline). Target: +10–15 tests.
- **[AA17]** No action on `macbeth_aristotelian.py`, `oedipus_aristotelian.py`, or `rashomon_aristotelian.py` beyond optional annotation pass. Their existing `ArAnagnorisisStep` records (AR_STEP_JOCASTA precipitating-different-character; AR_STEP_LADY_MACBETH_SLEEPWALKING parallel-different-character) derive correctly under A14 without `step_kind` set. Authors *may* set `step_kind` explicitly for clarity in a cleanup pass; not required by sketch-03 acceptance.

Post-sketch test totals update state-of-play counts. Baseline at sketch open: 822 passing (production-format-sketch-13 landing).

## Summary

Two probe-surfaced Aristotelian extensions close cleanly under sketch-01 + sketch-02's extension-only discipline. `ArCharacterArcRelation` types Hamlet's three-way tragic-hero parallelism structurally (mirror + foil pairwise); `step_kind` on `ArAnagnorisisStep` + `anagnorisis_character_ref_id` on `ArMythos` close the protagonist-scope staged-recognition gap that OQ-AP10 surfaced. OQ-AP5 (fate-agent) formally retires on two-negative-probe grounds. Three OQs remain banked with explicit dispositions (OQ-AP1 pathos/catharsis; OQ-AP7 numerical-range; OQ-AP8 same-beat staggered); one pressure stays scope-rejected (OQ-AP9 audience-level irony, now four surfacings across four encodings).

Architectural verdict extends sketches 01/02's GREEN: commitments A1–A14 remain extension-only; no core-record modification; no substrate change; no new effect kind. The probe arc (four encodings, five probe runs) has produced six banked OQs plus two well-forced closures; sketch-03 lands the two well-forced ones and retires one; the banked-OQ ledger continues as the honest record of what the dialect chose not to encode today.

If implementation of AA12–AA17 surfaces an extension that cannot be had as pure addition, halt and re-open the architectural question.
