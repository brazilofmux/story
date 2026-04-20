"""
verifier_helpers.py — shared helpers for cross-boundary verifier
modules.

Extracted once the third encoding's verifier landed (REVIEW.md
Finding 3's trigger: "duplicated cross-boundary verifier logic that
will drift"). Previously the same five helpers lived in both
oedipus_verification.py and macbeth_verification.py with identical
bodies; macbeth_save_the_cat_verification.py had a trimmed subset.
This module holds the canonical definitions; each verifier module
imports what it needs.

Design: helpers take their collections explicitly (fabula,
throughlines, entities, lowerings) rather than closing over module-
level state. Each verifier module still owns its encoding-specific
imports — this module only holds the reusable logic. Dialect-
specific helpers (throughline / character / lowering walks) continue
to live here because the "cross-boundary verifier" pattern is where
they're reused; they're not general substrate utilities and don't
belong in substrate.py.
"""

from __future__ import annotations

from story_engine.core.substrate import (
    Event, KnowledgeEffect, WorldEffect,
    IDENTITY_PREDICATE, in_scope, project_world, derive_all_world,
)
from story_engine.core.dramatic import Throughline, ABSTRACT_THROUGHLINE_OWNERS
from story_engine.core.lowering import cross_ref, LoweringStatus


# Role-name precedence for identifying an event's "primary actor" —
# the participant whose knowledge/agency the event centers. Ordered
# most-specific first; the first role present in an event's
# `participants` dict wins. Encodings that introduce new role names
# may extend this list, but the five below cover every event shape
# in the current Oedipus / Macbeth / Ackroyd encodings.
_PRIMARY_ACTOR_ROLES = ("killer", "speaker", "actor", "agent", "subject")


# LT12a constraint-predicate vocabulary (pressure-shape-taxonomy-
# sketch-03). Retractions of propositions whose predicate matches
# this set are presumed *enabling* (state removal that opens a new
# action) rather than *restricting* (option-closing convergence).
# Explicitly excludes `scheduled_*` — that prefix is LT8's domain.
# Encodings can extend this vocabulary at their verifier invocation
# via the `constraint_vocab` parameter on `classify_arc_limit_shape_
# strong` / `classify_retraction_kind`.
DEFAULT_CONSTRAINT_VOCAB: frozenset = frozenset({
    "bound_to", "tied_to",
    "imprisoned_in", "trapped_in", "locked_in",
})


# LT8 scheduling-predicate prefixes (pressure-shape-taxonomy-sketch-02
# + scheduling-act-utterance-sketch-01). Any `WorldEffect` whose prop
# predicate begins with one of these prefixes contributes to LT8's
# scheduling-signal count, and — combined with a zero middle-arc LT2
# count — fires LT9 (timelock-strong).
#
# Semantics per prefix:
#
#   - `scheduled_*` — objective external schedule; unconditional until
#     retracted (Rocky's model).
#   - `requested_*` — subjective one-party scheduling act carried by
#     an utterance; structurally force-carrying via the speech-act
#     itself, contingent on target acceptance (Rashomon's bandit /
#     samurai model).
#
# Match is case-sensitive at string position 0. Both prefixes
# contribute equally to LT9 strength in sketch-01; per-prefix
# weighting is deferred (OQ4).
SCHEDULING_PREFIXES: frozenset = frozenset({
    "scheduled_",
    "requested_",
})

# Authorial vocabulary token per scheduling-act-utterance-sketch-02
# SC6. When a Lowering's annotation text contains this substring,
# the Lowering names a narratively load-bearing driver not modeled
# in substrate. Case-sensitive substring match; hyphenated form is
# the canonical spelling per the probe's flagged text.
PROSE_CARRIED_MARKER = "prose-carried"


def _prose_carried_lowerings(lowerings: tuple) -> tuple:
    """SC6 helper. Return the subset of `lowerings` whose
    `annotation.text` contains the `PROSE_CARRIED_MARKER` substring.

    Empty input → empty output. Defensive against missing or
    non-string annotation.text (skips silently)."""
    out = []
    for lw in lowerings:
        annotation = getattr(lw, "annotation", None)
        text = getattr(annotation, "text", None)
        if isinstance(text, str) and PROSE_CARRIED_MARKER in text:
            out.append(lw)
    return tuple(out)


def find_substrate_event(event_id: str, fabula: tuple) -> Event:
    """Look up a substrate Event by id, or raise KeyError. Linear
    scan; fabulas are authored tuples and typically under 30 events,
    so no indexing overhead is warranted."""
    for e in fabula:
        if e.id == event_id:
            return e
    raise KeyError(f"no substrate event with id {event_id!r}")


def find_throughline(
    throughline_id: str, throughlines: tuple,
) -> Throughline:
    """Look up a Dramatic Throughline by id, or raise KeyError.
    Linear scan over the encoding's THROUGHLINES tuple."""
    for t in throughlines:
        if t.id == throughline_id:
            return t
    raise KeyError(f"no throughline with id {throughline_id!r}")


def is_abstract_throughline_owner(owner_id: str) -> bool:
    """True if the owner id is a Dramatic sentinel (none,
    the-situation, the-relationship) rather than a concrete
    Character id. Delegates to dramatic.ABSTRACT_THROUGHLINE_OWNERS
    as the single source of truth — previous hand-rolled copies of
    this check risked drifting from the canonical set."""
    return owner_id in ABSTRACT_THROUGHLINE_OWNERS


def event_participants_flat(event: Event) -> set:
    """Flatten an Event's participants dict into a set of entity ids.
    Substrate events sometimes use lists for participant slots (e.g.,
    'targets', 'killers'); this collapses those into a single flat
    set so callers can test entity-id membership directly."""
    out = set()
    parts = event.participants or {}
    for v in parts.values():
        if isinstance(v, str):
            out.add(v)
        elif isinstance(v, (list, tuple)):
            for e in v:
                if isinstance(e, str):
                    out.add(e)
    return out


def primary_actor_id(event: Event) -> str:
    """Return the entity id considered the event's primary actor,
    resolved via role-name precedence
    (`killer > speaker > actor > agent > subject`). Falls back to
    the first participant value if none of the privileged roles is
    present. Returns None if the event has no participants at all.

    For list-valued roles (e.g., `killers=[...]`) the first id in
    the list wins. Per EK2 in event-kind-taxonomy-sketch-01."""
    parts = event.participants or {}
    for role in _PRIMARY_ACTOR_ROLES:
        if role in parts:
            v = parts[role]
            if isinstance(v, (list, tuple)):
                return v[0] if v else None
            return v
    for v in parts.values():
        if isinstance(v, (list, tuple)):
            if v:
                return v[0]
        else:
            return v
    return None


def classify_event_action_shape(
    event: Event,
    *,
    agent_ids: frozenset = None,
) -> str:
    """Classify an Event as `"external"` or `"internal"` action-shaped
    per EK2 (event-kind-taxonomy-sketch-01).

    An event is **external-action-shaped** iff both hold:
      1. **Interpersonal.** Its participants include at least two
         distinct entity ids. If `agent_ids` is provided, only
         participants in that set count toward this clause — so a
         location or non-agent placeholder does not inflate the
         count. (Callers pass `agent_ids` built from their encoding's
         ENTITIES tuple; see the `agent_ids_from_entities` helper.)
      2. **Outward-effect.** Either a `WorldEffect` is present, or
         a `KnowledgeEffect` whose target agent is not the event's
         primary actor (so the event updates someone *else's*
         knowledge).

    If either clause fails, the event is **internal-state-shaped**.
    These two categories are exhaustive — EK2 defines internal-state
    as the complement of external-action.

    The classifier reads fold-visible structural features only. It
    does not branch on the event's `type` string, per EK1's
    discipline ("verifier classification reads fold-visible
    structure, not type strings"). Substrate-05 M1 routes modality
    with downstream fold consequence to effects; EK2 reads those
    effects and turns them into a yes/no answer."""
    parts = event.participants or {}
    all_ids = []
    for v in parts.values():
        if isinstance(v, (list, tuple)):
            all_ids.extend(x for x in v if isinstance(x, str))
        elif isinstance(v, str):
            all_ids.append(v)
    if agent_ids is not None:
        filtered = [i for i in all_ids if i in agent_ids]
    else:
        filtered = list(all_ids)
    interpersonal = len(set(filtered)) >= 2

    actor = primary_actor_id(event)
    has_world_effect = any(
        isinstance(ef, WorldEffect) for ef in event.effects
    )
    has_outward_knowledge = any(
        isinstance(ef, KnowledgeEffect) and ef.agent_id != actor
        for ef in event.effects
    )
    outward = has_world_effect or has_outward_knowledge

    if interpersonal and outward:
        return "external"
    return "internal"


# ----------------------------------------------------------------------------
# Arc-level limit-shape classifier — pressure-shape-taxonomy-sketch-01
# ----------------------------------------------------------------------------


def _effect_is_identity_proposition(effect) -> bool:
    """True if the effect asserts an identity/2 proposition on either
    the world or an agent's knowledge state."""
    if isinstance(effect, WorldEffect):
        return effect.prop.predicate == IDENTITY_PREDICATE
    if isinstance(effect, KnowledgeEffect):
        return effect.held.prop.predicate == IDENTITY_PREDICATE
    return False


def classify_arc_limit_shape(
    fabula,
    rules,
    canonical_branch,
    all_branches: dict,
) -> tuple:
    """Classify an arc's limit-pressure shape per LT2/LT3 in
    pressure-shape-taxonomy-sketch-01.

    Reads fold-visible fabula structure only (events, effects,
    rule-derivable world facts) — no type-string dispatch, per LT1.
    The three LT2 convergence signals are computed independently:

      1. **Retraction.** Count events with a `WorldEffect.asserts=False`
         that retracts a proposition previously asserted in the fabula.
      2. **Identity resolution.** Count events whose effects include
         at least one identity/2 proposition (either as a `WorldEffect`
         prop or as a `KnowledgeEffect.held.prop`).
      3. **Rule-derivable emergence.** Count world-facts derivable at
         the arc's end (via `derive_all_world`) whose proof kind is
         `"derived"` and which were not derivable from the empty
         initial world.

    Returns `(classification, strength, signals)` where:

      - `classification`: `"optionlock"` if ≥ 1 signal kind fires
        (LT2 disjunction); `"timelock-consistent"` if 0 signal kinds
        fire (LT3 complement-only detection).
      - `strength`: `min(1.0, signal_kinds / 3.0)`. 1 kind → 0.33,
        2 kinds → 0.67, 3 kinds → 1.0. Reports how many distinct
        convergence mechanisms the arc exhibits, not how many events
        fire each — multiplicity is reported in `signals`.
      - `signals`: tuple of `"<kind>:<count>"` tags documenting which
        mechanisms fired (e.g., `("retraction:1", "rule-emergence:4")`).
        Empty tuple for timelock-consistent arcs.

    LT3 asymmetry is deliberate: the Timelock side is weaker than the
    Optionlock side because substrate-05 has no scheduling vocabulary.
    The complement-only signal ("zero convergence") is consistent with
    Timelock but not affirmative evidence of it. Callers should apply
    LT5's disposition table (the author's DSP_limit declaration
    determines verdict polarity; the classifier only reports observed
    shape).
    """
    events = [
        e for e in fabula if in_scope(e, canonical_branch, all_branches)
    ]
    events_sorted = sorted(
        events, key=lambda e: (e.τ_s if e.τ_s is not None else 0, e.τ_a)
    )

    # Signal 1 — retractions that unwind a prior assertion.
    asserted_so_far: set = set()
    retraction_count = 0
    for e in events_sorted:
        for ef in e.effects:
            if not isinstance(ef, WorldEffect):
                continue
            if ef.asserts:
                asserted_so_far.add(ef.prop)
            else:
                if ef.prop in asserted_so_far:
                    retraction_count += 1
                    asserted_so_far.discard(ef.prop)

    # Signal 2 — identity-proposition effects (equivalence-class collapses).
    identity_resolution_count = sum(
        1 for e in events_sorted
        if any(_effect_is_identity_proposition(ef) for ef in e.effects)
    )

    # Signal 3 — rule-derivable compounds that emerge mid-arc. Strip
    # any authored fact whose predicate matches a rule head before
    # deriving, since N10 ("authored wins") hides rule firings behind
    # already-authored compounds. The substrate commitment is that rule
    # heads are dedicated compound predicates, so stripping by predicate
    # is safe here.
    rule_emergence_count = 0
    rules_tuple = tuple(rules)
    if events_sorted and rules_tuple:
        end_τ = max(e.τ_s for e in events_sorted if e.τ_s is not None)
        end_world = project_world(events_sorted, up_to_τ_s=end_τ)
        rule_head_preds = {r.head.predicate for r in rules_tuple}
        stripped_end_world = {
            p for p in end_world if p.predicate not in rule_head_preds
        }
        stripped_derivations = derive_all_world(
            stripped_end_world, rules_tuple,
        )
        rule_emergence_count = sum(
            1 for _p, proof in stripped_derivations.items()
            if proof.kind == "derived"
        )

    signals: list = []
    if retraction_count > 0:
        signals.append(f"retraction:{retraction_count}")
    if identity_resolution_count > 0:
        signals.append(f"identity-resolution:{identity_resolution_count}")
    if rule_emergence_count > 0:
        signals.append(f"rule-emergence:{rule_emergence_count}")

    kinds_firing = len(signals)
    if kinds_firing == 0:
        return ("timelock-consistent", 0.0, ())
    strength = min(1.0, kinds_firing / 3.0)
    return ("optionlock", strength, tuple(signals))


def classify_retraction_kind(
    retracted_prop,
    retraction_τ_s: int,
    sorted_events: list,
    constraint_vocab: frozenset = DEFAULT_CONSTRAINT_VOCAB,
    window: int = 2,
) -> tuple:
    """LT12 retraction-kind classifier (pressure-shape-taxonomy-
    sketch-03). Classifies a retraction as *enabling* (state removal
    that opens a new action) or *restricting* (option-closing
    convergence).

    A retraction of `P(X, ...)` at `retraction_τ_s` is **enabling** iff:

      - **LT12a (lexical)**: `P.predicate` matches `constraint_vocab`
        (default: `bound_to`, `tied_to`, `imprisoned_in`,
        `trapped_in`, `locked_in`). These predicates represent
        bounding constraints whose removal releases agency. OR
      - **LT12b (positional)**: the retracted prop's first argument
        `X` appears as a named participant (any role) in an event
        within the arc window `(retraction_τ_s, retraction_τ_s +
        window]`. This catches enabling retractions outside the
        lexical vocabulary when the retractee becomes active shortly
        afterwards.

    Returns `("enabling", reason)` or `("restricting", None)` where
    `reason` is `"constraint-vocabulary"` (LT12a) or
    `"subject-reactivation"` (LT12b).

    Only restricting retractions count as LT2 convergence signals per
    LT14 (sketch-03 disposition table). Enabling retractions are
    reported in the classifier's output so the verifier's comment
    can reference them, but they do not shift the verdict.
    """
    # LT12a — lexical
    if retracted_prop.predicate in constraint_vocab:
        return ("enabling", "constraint-vocabulary")

    # LT12b — positional subject-reactivation
    if retracted_prop.args:
        subject = retracted_prop.args[0]
        window_hi = retraction_τ_s + window
        for e in sorted_events:
            if e.τ_s is None or e.τ_s <= retraction_τ_s:
                continue
            if e.τ_s > window_hi:
                break
            if subject in _participant_values(e.participants):
                return ("enabling", "subject-reactivation")

    return ("restricting", None)


def _participant_values(participants) -> set:
    """Flatten an event's participants mapping into a set of entity
    ids, handling both scalar values ("a": "tajomaru") and list values
    ("targets": ["husband", "wife"]) uniformly."""
    values: set = set()
    if not participants:
        return values
    for v in participants.values():
        if isinstance(v, (list, tuple)):
            for item in v:
                values.add(item)
        else:
            values.add(v)
    return values


def classify_arc_limit_shape_strong(
    fabula,
    rules,
    canonical_branch,
    all_branches: dict,
    constraint_vocab: frozenset = DEFAULT_CONSTRAINT_VOCAB,
    enabling_window: int = 2,
) -> dict:
    """LT7–LT12 arc-position-aware classifier per pressure-shape-
    taxonomy-sketches 02 and 03. Extends `classify_arc_limit_shape`
    with:

      1. **LT7** — each LT2 convergence signal is tagged by arc
         position: `peripheral-pre` (τ_s < 0, substrate convention
         for backstory), `terminal` (τ_s within top 10% of the
         positive-arc range), or `middle-arc` (the remainder).
      2. **LT8** — scheduling-predicate signals: any `WorldEffect`
         whose prop's predicate begins with any recognized scheduling
         prefix (`SCHEDULING_PREFIXES` — `"scheduled_"` per sketch-02,
         `"requested_"` per scheduling-act-utterance-sketch-01) is a
         positive Timelock signal, regardless of whether it
         asserts or retracts. The prefix set is verifier-local
         vocabulary per LT6.
      3. **LT9** — strong Timelock predicate: scheduling signal
         present AND middle-arc LT2 signal count is zero.
      4. **LT12** — enabling vs restricting retractions. A retraction
         in the middle-arc band is classified per
         `classify_retraction_kind`; only restricting retractions
         contribute to the LT2 convergence count. Enabling
         retractions are reported in `enabling_retractions` so the
         verifier comment can surface them. Peripheral-pre and
         terminal-band retractions are exempt from LT12 — LT7's
         banding handles them first.

    Returns a dict with the following keys:

      - `classification`: one of `"optionlock"`, `"timelock-strong"`,
        `"timelock-consistent"`, `"optionlock-peripheral"`,
        `"undetermined"`.
      - `strength`: float in [0.0, 1.0].
      - `signals`: tuple of `"<kind>:<count>"` strings, compatible
        with sketch-01's format (flat totals across all positions;
        retraction count reflects ALL retractions for back-compat,
        enabling and restricting alike).
      - `middle_arc_kinds`: count of distinct LT2 signal kinds with
        at least one **restricting** middle-arc event (LT12-aware).
      - `peripheral_pre_count`, `middle_arc_count`, `terminal_count`:
        event counts per band across all three LT2 signal kinds
        (flat, enabling-inclusive; used for diagnostics, not verdict).
      - `scheduling_signals`: tuple of predicate names that fired
        LT8 (distinct `Prop` count, not event count). Flat across
        all recognized prefixes.
      - `scheduling_count`: number of distinct `Prop`s in
        `scheduling_signals`.
      - `scheduling_prefixes`: dict mapping each matched prefix
        (e.g., `"scheduled_"`, `"requested_"`) to the tuple of Props
        carrying that prefix, sorted by predicate name. Prefixes
        with zero matches are omitted. Additive per
        scheduling-act-utterance-sketch-01 SC3 — sketch-02-only
        callers can ignore it.
      - `enabling_retractions`: tuple of
        `(predicate, τ_s, reason)` triples — one per middle-arc
        retraction classified enabling by LT12.
      - `enabling_retraction_count`: convenience integer, equals
        `len(enabling_retractions)`.
      - `arc_range`: `(min_τ_s, max_τ_s)` for diagnostics.
      - `terminal_threshold`: the τ_s cutoff used for terminal-band
        classification (computed as `max_τ_s - 0.1 × positive_span`).

    The existing `classify_arc_limit_shape` is unchanged and
    continues to serve sketch-01-only callers (LT11 back-compat).

    Per LT1, classification is a function of fold-visible substrate
    structure — events, effects, and rule derivations. Per LT11,
    `dsp_limit_characterization_check` below consumes this dict
    directly to apply the LT14 disposition table.
    """
    events = [
        e for e in fabula if in_scope(e, canonical_branch, all_branches)
    ]
    events_sorted = sorted(
        events, key=lambda e: (e.τ_s if e.τ_s is not None else 0, e.τ_a)
    )

    if not events_sorted:
        return {
            "classification": "undetermined",
            "strength": 0.0,
            "signals": (),
            "middle_arc_kinds": 0,
            "peripheral_pre_count": 0,
            "middle_arc_count": 0,
            "terminal_count": 0,
            "scheduling_signals": (),
            "scheduling_count": 0,
            "scheduling_prefixes": {},
            "enabling_retractions": (),
            "enabling_retraction_count": 0,
            "arc_range": (0, 0),
            "terminal_threshold": 0.0,
        }

    τs_values = [e.τ_s for e in events_sorted if e.τ_s is not None]
    max_τ = max(τs_values)
    min_τ = min(τs_values)
    positive_τs = [t for t in τs_values if t >= 0]
    min_positive = min(positive_τs) if positive_τs else 0
    positive_span = max(1, max_τ - min_positive)
    # Terminal band: top 10% of positive-arc range, BUT only when the
    # positive arc has enough events to cleanly separate middle from
    # terminal (> 3 positive-τ_s events). Short synthetic fabulae or
    # 1–3-event arcs treat every positive-arc event as middle-arc,
    # preserving sketch-01's flat semantics for such cases. Rocky /
    # Oedipus / Macbeth / Ackroyd all have enough events to activate
    # the band; small unit-test fixtures do not.
    if len(positive_τs) > 3:
        terminal_threshold = max_τ - 0.1 * positive_span
    else:
        terminal_threshold = float("inf")

    def _band_for(τ):
        if τ is None:
            return "middle-arc"
        if τ < 0:
            return "peripheral-pre"
        if τ > terminal_threshold:
            return "terminal"
        return "middle-arc"

    # === Retractions + scheduling-predicate scan (single pass) ===
    #
    # LT12 integration (sketch-03): retractions in the middle-arc band
    # are classified as enabling or restricting. `retraction_bands`
    # continues to carry the flat count (back-compat with sketch-01's
    # signal display); `restricting_retraction_bands` carries the
    # LT12-filtered count used for classification. Enabling middle-arc
    # retractions are collected in `enabling_retractions_list`.
    asserted_so_far: set = set()
    retraction_bands = {"peripheral-pre": 0, "middle-arc": 0, "terminal": 0}
    restricting_retraction_bands = {
        "peripheral-pre": 0, "middle-arc": 0, "terminal": 0,
    }
    enabling_retractions_list: list = []
    scheduling_props: set = set()
    for e in events_sorted:
        for ef in e.effects:
            if not isinstance(ef, WorldEffect):
                continue
            for prefix in SCHEDULING_PREFIXES:
                if ef.prop.predicate.startswith(prefix):
                    scheduling_props.add(ef.prop)
                    break
            if ef.asserts:
                asserted_so_far.add(ef.prop)
            else:
                if ef.prop in asserted_so_far:
                    band = _band_for(e.τ_s)
                    retraction_bands[band] += 1
                    # LT12 applies only within the middle-arc band.
                    # Peripheral-pre and terminal retractions pass
                    # through LT7's banding unchanged.
                    if band == "middle-arc":
                        kind, reason = classify_retraction_kind(
                            ef.prop, e.τ_s, events_sorted,
                            constraint_vocab=constraint_vocab,
                            window=enabling_window,
                        )
                        if kind == "enabling":
                            enabling_retractions_list.append(
                                (ef.prop.predicate, e.τ_s, reason)
                            )
                        else:
                            restricting_retraction_bands[band] += 1
                    else:
                        restricting_retraction_bands[band] += 1
                    asserted_so_far.discard(ef.prop)

    # === Identity resolutions (equivalence-class effects) ===
    identity_bands = {"peripheral-pre": 0, "middle-arc": 0, "terminal": 0}
    for e in events_sorted:
        if any(_effect_is_identity_proposition(ef) for ef in e.effects):
            identity_bands[_band_for(e.τ_s)] += 1

    # === Rule-derivable emergences with per-rule τ_s localization ===
    # For each derived compound at end, compute the emergence τ_s as
    # the MIN across rules whose head matches (any single rule is
    # sufficient to derive the compound), where each rule's τ_s is
    # the MAX τ_s of any event asserting a body-premise predicate
    # (approximation: we match on predicate, not ground args, which
    # is correct for the current corpus where each rule uses a
    # distinct predicate vocabulary).
    rule_emergence_bands = {
        "peripheral-pre": 0, "middle-arc": 0, "terminal": 0,
    }
    rules_tuple = tuple(rules)
    if events_sorted and rules_tuple:
        end_τ = max_τ
        end_world = project_world(events_sorted, up_to_τ_s=end_τ)
        rule_head_preds = {r.head.predicate for r in rules_tuple}
        stripped_end_world = {
            p for p in end_world if p.predicate not in rule_head_preds
        }
        stripped_derivations = derive_all_world(
            stripped_end_world, rules_tuple,
        )
        # First-assertion τ_s per predicate (earliest world-assertion).
        # Used to compute "first τ_s at which a rule's body is
        # collectively satisfied": for each body literal, take the
        # earliest τ_s the predicate is asserted anywhere; emergence
        # is the MAX across body literals (all must hold together).
        # Predicates only appearing as rule heads (never authored) get
        # the recursive earliest via their rule's emergence — but for
        # simplicity we treat head-only predicates as deriving at the
        # min τ_s of any event asserting at least one of their
        # contributing body predicates, which is conservative.
        first_assert_τ_by_pred: dict = {}
        for e in events_sorted:
            for ef in e.effects:
                if isinstance(ef, WorldEffect) and ef.asserts:
                    p = ef.prop.predicate
                    if (p not in first_assert_τ_by_pred
                            or e.τ_s < first_assert_τ_by_pred[p]):
                        first_assert_τ_by_pred[p] = e.τ_s

        for derived_prop, proof in stripped_derivations.items():
            if proof.kind != "derived":
                continue
            best_emergence_τ = None
            for rule in rules_tuple:
                if rule.head.predicate != derived_prop.predicate:
                    continue
                # For each body literal, the earliest τ_s its predicate
                # is asserted in the fabula. Emergence of this rule's
                # head = max across body literals (all must hold
                # together). If any body literal has no authored
                # assertion, fall back to the rule's min contributing
                # predicate τ_s (rule is head-only; approximate).
                body_τs: list = []
                missing_any = False
                for lit in rule.body:
                    τ = first_assert_τ_by_pred.get(lit.predicate)
                    if τ is None:
                        missing_any = True
                        break
                    body_τs.append(τ)
                if missing_any:
                    # Any body literal whose predicate is never
                    # authored is head-only; this rule's firing depends
                    # on chained derivation. Skip rigorous computation
                    # here — head-only chains currently appear only
                    # for Macbeth's `tyrant` (body: kinslayer, regicide,
                    # king), where `king` is authored so its earliest
                    # τ_s is available; the derived premises'
                    # emergences are handled when THEY derive. For the
                    # present rule, use the min of known body τ_s.
                    known = [
                        first_assert_τ_by_pred[lit.predicate]
                        for lit in rule.body
                        if lit.predicate in first_assert_τ_by_pred
                    ]
                    rule_emergence_τ = max(known) if known else None
                else:
                    rule_emergence_τ = max(body_τs)
                if rule_emergence_τ is not None:
                    if (best_emergence_τ is None
                            or rule_emergence_τ < best_emergence_τ):
                        best_emergence_τ = rule_emergence_τ
            if best_emergence_τ is not None:
                rule_emergence_bands[_band_for(best_emergence_τ)] += 1

    # Totals across bands
    peripheral_pre = (
        retraction_bands["peripheral-pre"]
        + identity_bands["peripheral-pre"]
        + rule_emergence_bands["peripheral-pre"]
    )
    middle_arc = (
        retraction_bands["middle-arc"]
        + identity_bands["middle-arc"]
        + rule_emergence_bands["middle-arc"]
    )
    terminal = (
        retraction_bands["terminal"]
        + identity_bands["terminal"]
        + rule_emergence_bands["terminal"]
    )

    # Kinds firing anywhere (sketch-01 format; flat retraction count
    # for back-compat includes both enabling and restricting).
    retraction_total = sum(retraction_bands.values())
    identity_total = sum(identity_bands.values())
    rule_emergence_total = sum(rule_emergence_bands.values())
    kinds_firing = sum(
        1 for n in (retraction_total, identity_total, rule_emergence_total)
        if n > 0
    )

    # LT12-aware kinds firing (restricting retractions only). Used by
    # classification (sketch-03 LT14): if every middle-arc retraction
    # is enabling, the substrate is LT2-clean for Timelock purposes,
    # not arc-peripheral.
    restricting_retraction_total = sum(restricting_retraction_bands.values())
    restricting_kinds_firing = sum(
        1 for n in (
            restricting_retraction_total,
            identity_total,
            rule_emergence_total,
        )
        if n > 0
    )

    # Middle-arc kinds (LT7 / LT9 / LT12) — restricting-only for the
    # retraction kind, per sketch-03 LT14. Identity and rule-emergence
    # kinds are unchanged by LT12.
    middle_arc_kinds = sum(
        1 for n in (
            restricting_retraction_bands["middle-arc"],
            identity_bands["middle-arc"],
            rule_emergence_bands["middle-arc"],
        )
        if n > 0
    )

    signal_strs: list = []
    if retraction_total > 0:
        signal_strs.append(f"retraction:{retraction_total}")
    if identity_total > 0:
        signal_strs.append(f"identity-resolution:{identity_total}")
    if rule_emergence_total > 0:
        signal_strs.append(f"rule-emergence:{rule_emergence_total}")

    scheduling_signals_tuple = tuple(
        sorted({p.predicate for p in scheduling_props})
    )
    scheduling_count = len(scheduling_props)

    # SC3 — per-prefix breakdown. One pass, two-arg match (longest
    # prefix would matter only if the set contained overlapping
    # prefixes; today it does not, so first-match order is irrelevant).
    # Empty-tuple values are omitted — the dict lists only prefixes
    # with at least one match.
    scheduling_prefixes_map: dict = {}
    for prefix in SCHEDULING_PREFIXES:
        matched = tuple(sorted(
            (p for p in scheduling_props if p.predicate.startswith(prefix)),
            key=lambda q: q.predicate,
        ))
        if matched:
            scheduling_prefixes_map[prefix] = matched

    # Classification per LT7–LT9 + LT12 (sketch-03). Uses restricting-
    # only counts throughout — enabling retractions never shift the
    # classification verdict, only the comment/diagnostics.
    if scheduling_count > 0 and middle_arc_kinds == 0:
        classification = "timelock-strong"
        strength = min(1.0, scheduling_count / 2.0)
    elif middle_arc_kinds > 0:
        classification = "optionlock"
        strength = min(1.0, restricting_kinds_firing / 3.0)
    elif restricting_kinds_firing == 0 and scheduling_count == 0:
        classification = "timelock-consistent"
        strength = 0.5
    else:
        # Restricting signals fire but only peripheral/terminal, and
        # no scheduling predicate. LT10's declared=Optionlock +
        # only-peripheral/terminal row.
        classification = "optionlock-peripheral"
        strength = 0.5 * min(1.0, restricting_kinds_firing / 3.0)

    return {
        "classification": classification,
        "strength": strength,
        "signals": tuple(signal_strs),
        "middle_arc_kinds": middle_arc_kinds,
        "peripheral_pre_count": peripheral_pre,
        "middle_arc_count": middle_arc,
        "terminal_count": terminal,
        "scheduling_signals": scheduling_signals_tuple,
        "scheduling_count": scheduling_count,
        "scheduling_prefixes": scheduling_prefixes_map,
        "enabling_retractions": tuple(enabling_retractions_list),
        "enabling_retraction_count": len(enabling_retractions_list),
        "arc_range": (min_τ, max_τ),
        "terminal_threshold": terminal_threshold,
    }


def dsp_limit_characterization_check(
    fabula,
    rules,
    canonical_branch,
    all_branches: dict,
    declared_choice: str,
    lowerings: tuple = (),
) -> tuple:
    """Shared DSP_limit characterization check for the dramatica-
    complete → substrate verifier surface. Called by each encoding's
    verifier module with its own fabula/rules/canonical scope.

    Returns `(verdict, strength, comment)` per the LT5 disposition
    table in pressure-shape-taxonomy-sketch-01:

      - Optionlock declared + Optionlock-shaped → `APPROVED`.
      - Timelock declared + timelock-consistent → `NOTED`
        (consistent-but-not-affirmed; LT3's honest asymmetry).
      - Optionlock declared + no convergence signals → `NEEDS_WORK`.
      - Timelock declared + convergence signals present →
        `PARTIAL_MATCH` or `NEEDS_WORK` by signal strength.
      - Unknown declared_choice → `NOTED` with a diagnostic.

    `declared_choice` is the DSP_limit record's `.choice` value
    (e.g., `Limit.OPTIONLOCK.value` or `Limit.TIMELOCK.value`).

    `lowerings` is an optional tuple of Lowering records scoped to
    the current Story / verification call — typically
    `LOWERINGS_BY_STORY[story_id]`. When non-empty AND the verdict
    would be NOTED at `classification == "timelock-consistent"`,
    the comment is specialized per scheduling-act-utterance-sketch-
    02 SC8: any Lowering whose `annotation.text` contains the
    `PROSE_CARRIED_MARKER` substring (SC6) surfaces a trailing
    sentence naming the Lowering id(s) and the representational
    gap. Verdict + strength are unchanged. The default empty tuple
    preserves pre-sketch-02 behavior exactly.

    Consumes `classify_arc_limit_shape_strong` for the LT7–LT9
    refinement (arc-position banding + scheduling-predicate
    recognition + strong Timelock predicate per sketch-02).
    Sketch-01's LT5 preserved — the author's declaration is never
    silently overridden; the verifier reports whether substrate
    structure supports it.
    """
    result = classify_arc_limit_shape_strong(
        fabula, rules, canonical_branch, all_branches,
    )
    classification = result["classification"]
    signals = result["signals"]
    scheduling_signals = result["scheduling_signals"]
    middle_arc_kinds = result["middle_arc_kinds"]
    peripheral_pre = result["peripheral_pre_count"]
    terminal = result["terminal_count"]
    middle_arc = result["middle_arc_count"]
    scheduling_count = result["scheduling_count"]
    scheduling_prefixes = result["scheduling_prefixes"]
    enabling_retractions = result["enabling_retractions"]
    kinds_firing = len(signals)

    declared_normalized = (declared_choice or "").lower()
    signal_text = (
        ", ".join(signals) if signals else "no LT2 convergence signals"
    )
    position_text = (
        f"positions: {middle_arc} middle-arc, {peripheral_pre} "
        f"peripheral-pre, {terminal} terminal"
    )
    scheduling_text = (
        ", ".join(scheduling_signals) if scheduling_signals
        else "no scheduling predicates"
    )
    # SC3 — when more than one scheduling prefix matched, append a
    # per-prefix breakdown so the verdict rationale shows the LT8
    # composition (e.g., "LT8 signals: 1 scheduled_, 1 requested_").
    # Single-prefix cases retain the sketch-02 comment shape.
    if len(scheduling_prefixes) >= 2:
        prefix_breakdown = ", ".join(
            f"{len(props)} {prefix}"
            for prefix, props in sorted(scheduling_prefixes.items())
        )
        scheduling_breakdown_suffix = (
            f" LT8 signals: {prefix_breakdown}."
        )
    else:
        scheduling_breakdown_suffix = ""
    # LT12: surface enabling-retractions as a comment suffix so the
    # verdict rationale explains what the classifier saw but did not
    # count toward LT2 convergence.
    if enabling_retractions:
        enabling_clauses = ", ".join(
            f"{pred}@τ_s={τ} ({reason})"
            for pred, τ, reason in enabling_retractions
        )
        enabling_suffix = (
            f" LT12 excluded {len(enabling_retractions)} "
            f"enabling retraction(s): {enabling_clauses}."
        )
    else:
        enabling_suffix = ""

    # Import verdict constants lazily to keep verifier_helpers' import
    # graph narrow (verification.py imports verifier_helpers indirectly
    # via the verifier modules; avoid a cycle).
    from story_engine.core.verification import (
        VERDICT_APPROVED, VERDICT_NEEDS_WORK,
        VERDICT_PARTIAL_MATCH, VERDICT_NOTED,
    )

    if declared_normalized == "optionlock":
        if classification == "optionlock":
            return (
                VERDICT_APPROVED, result["strength"],
                f"DSP_limit=Optionlock declared; substrate exhibits "
                f"middle-arc convergence ({signal_text}; "
                f"{position_text}). Arc ends because alternatives are "
                f"eliminated (LT2 + LT7). Strength {result['strength']:.2f} "
                f"reflects {kinds_firing}/3 signal kinds firing.",
            )
        if classification == "optionlock-peripheral":
            return (
                VERDICT_PARTIAL_MATCH, result["strength"],
                f"DSP_limit=Optionlock declared; substrate shows LT2 "
                f"signals ({signal_text}) but all are arc-peripheral "
                f"or terminal ({position_text}). Under LT7 these do "
                f"not constitute middle-arc convergence — the arc "
                f"body may not be doing the elimination work the "
                f"declaration claims.",
            )
        if classification == "timelock-strong":
            return (
                VERDICT_NEEDS_WORK, 1.0 - result["strength"],
                f"DSP_limit=Optionlock declared, but substrate shows "
                f"scheduling predicate(s) ({scheduling_text}) with no "
                f"middle-arc LT2 signals. LT9 reads this as "
                f"Timelock-shape-strong; the declaration and substrate "
                f"disagree." + scheduling_breakdown_suffix,
            )
        return (
            VERDICT_NEEDS_WORK, 0.0,
            f"DSP_limit=Optionlock declared, but substrate shows no "
            f"convergence signals (no retractions, no identity "
            f"resolutions, no rule-derivable emergences, no scheduling "
            f"predicates). Neither LT2 nor LT9 can confirm the "
            f"declared pressure shape.",
        )
    if declared_normalized == "timelock":
        if classification == "undetermined":
            # Empty fabula or no positive-τ_s events. Degenerate case;
            # report as LT3-weak since there is no substrate signal
            # either for or against the Timelock declaration.
            return (
                VERDICT_NOTED, None,
                f"DSP_limit=Timelock declared; fabula has no canonical-"
                f"scope events. Consistent with Timelock but not "
                f"affirmatively detected — LT3's honest weak-fallback "
                f"asymmetry (sketch-01).",
            )
        if classification == "timelock-strong":
            return (
                VERDICT_APPROVED, result["strength"],
                f"DSP_limit=Timelock declared; substrate shows "
                f"scheduling predicate(s) ({scheduling_text}) and "
                f"zero middle-arc LT2 convergence signals ({position_text}). "
                f"LT9 affirmatively detects Timelock shape. Strength "
                f"{result['strength']:.2f} = "
                f"min(1.0, {scheduling_count}/2)."
                + scheduling_breakdown_suffix,
            )
        if classification == "timelock-consistent":
            # SC8 — scan threaded lowerings for prose-carried drivers;
            # append a specializing suffix when any match. Verdict and
            # strength remain unchanged per sketch-02's discipline.
            prose_carried = _prose_carried_lowerings(lowerings)
            if prose_carried:
                ids = ", ".join(lw.id for lw in prose_carried)
                prose_carried_suffix = (
                    f" Lowering annotation(s) {ids} identify prose-"
                    f"carried temporal driver(s) not modeled in "
                    f"substrate — a specific representational gap "
                    f"per scheduling-act-utterance-sketch-02 "
                    f"OQ2-reshaped closure."
                )
            else:
                prose_carried_suffix = ""
            return (
                VERDICT_NOTED, None,
                f"DSP_limit=Timelock declared; substrate shows no "
                f"restricting middle-arc LT2 convergence signals AND "
                f"no scheduling predicate (LT8). Consistent with "
                f"Timelock but not affirmatively detected — LT3's "
                f"honest weak-fallback asymmetry (sketch-01). Consider "
                f"naming the scheduled endpoint with a `scheduled_*` "
                f"predicate to fire LT9."
                + enabling_suffix + prose_carried_suffix,
            )
        if classification == "optionlock-peripheral":
            # Restricting signals fire but only peripheral/terminal,
            # no scheduling. Timelock-compatible in spirit — no
            # middle-arc convergence — but LT8 did not confirm.
            return (
                VERDICT_NOTED, None,
                f"DSP_limit=Timelock declared; substrate shows "
                f"restricting LT2 signals ({signal_text}) all in "
                f"arc-peripheral or terminal bands ({position_text}) "
                f"and no scheduling predicate (LT8). Middle-arc is "
                f"clean (consistent with Timelock); LT9 does not "
                f"fire for lack of scheduling signal. Consider "
                f"naming the scheduled endpoint to lift the verdict "
                f"to APPROVED." + enabling_suffix,
            )
        # classification == "optionlock" — substrate exhibits middle-arc
        # convergence, contradicting the Timelock declaration.
        return (
            VERDICT_NEEDS_WORK, 1.0 - result["strength"],
            f"DSP_limit=Timelock declared, but substrate exhibits "
            f"middle-arc LT2 convergence ({signal_text}; "
            f"{position_text}). The arc body looks Optionlock-shaped "
            f"per LT2+LT7+LT12. Either the DSP choice needs "
            f"revisiting or the substrate's convergence is incidental "
            f"to a genuinely schedule-driven arc (LT9 does not fire: "
            f"{scheduling_count} scheduling predicate(s) present)."
            + enabling_suffix,
        )
    return (
        VERDICT_NOTED, None,
        f"DSP_limit choice {declared_choice!r} is not recognized "
        f"(expected 'optionlock' or 'timelock'); classifier observed "
        f"{classification} with {signal_text}.",
    )


def classify_event_agency_shape(event, mc_id: str):
    """Classify an event as pursuit / consequential / neutral / None
    from the perspective of the named MC, per event-agency-taxonomy-
    sketch-01 (AG1–AG6).

    Returns:
        - `None` — MC is not a participant in the event; not classified.
        - `"consequential"` — event has at least one WorldEffect whose
          prop asserts a fact whose first argument equals `mc_id`
          (AG2). Self-directed state changes, exile, consequence-
          landing events. Both asserts=True and asserts=False effects
          count — a retraction of `king(macbeth)` is also a
          consequential change.
        - `"pursuit"` — MC is participant, event is not consequential
          per AG2, and the event has at least one non-MC-only effect
          (at least one effect not exclusively about MC state per a
          loose sanity check; currently satisfied by any non-empty
          effect list). AG3. Investigation-era participation fires
          here — including `listener` utterance events where the MC
          has summoned the speaker.
        - `"neutral"` — MC participates but neither predicate fires.
          Edge case; rare.

    Per AG1, the classifier reads fold-visible structure only:
    event.participants (for MC membership) and event.effects (for
    AG2's first-arg match). Event type strings and participant role
    names are not inspected.
    """
    parts = event.participants or {}
    if mc_id not in parts.values():
        return None

    consequential = False
    has_any_effect = False
    for ef in event.effects:
        has_any_effect = True
        if isinstance(ef, WorldEffect):
            if ef.prop.args and str(ef.prop.args[0]) == mc_id:
                consequential = True

    if consequential:
        return "consequential"
    if not has_any_effect:
        return "neutral"
    return "pursuit"


# Canonical beat-type weight vocabulary per beat-weight-taxonomy-
# sketch-01 (BW2). Values tuned to the Dramatic dialect's common
# five-beat structure (Macbeth's vocabulary). Unknown strings default
# to 1.0 (rising-action baseline).
_BEAT_TYPE_WEIGHTS = {
    "inciting": 2.0,
    "rising": 1.0,
    "midpoint": 2.0,
    "climax": 2.0,
    "denouement": 1.5,
}


def beat_type_weight(beat_type) -> float:
    """Return the canonical weight for a beat_type string per BW2.
    Unknown / None values default to 1.0 (rising-action baseline)
    per the sketch's conservative-default discipline."""
    if not beat_type:
        return 1.0
    return _BEAT_TYPE_WEIGHTS.get(beat_type, 1.0)


def event_to_beat_type(
    event_id: str,
    throughline_id: str,
    lowerings,
    scenes,
    beats,
):
    """Resolve the beat_type for a substrate event, for a specific
    throughline, per BW3. Walks:

      substrate event_id →
      Scene-level Lowering whose lower_records contain the event →
      Scene.advances matching throughline_id →
      Beat.beat_type

    Returns the beat_type string, or None if any step fails.
    """
    # Step 1 — find Scene-level lowerings pointing at this substrate
    # event. Scene lowerings have upper_record.dialect == "dramatic"
    # and upper_record.record_id starting with "S_" by convention.
    scenes_by_id = {s.id: s for s in scenes}
    beats_by_id = {b.id: b for b in beats}
    for lw in lowerings:
        ur = lw.upper_record
        if ur.dialect != "dramatic":
            continue
        scene = scenes_by_id.get(ur.record_id)
        if scene is None:
            continue
        if not any(
            lr.dialect == "substrate" and lr.record_id == event_id
            for lr in lw.lower_records
        ):
            continue
        # Step 2 — find the Scene's advance entry for this throughline.
        for advance in scene.advances:
            if advance.throughline_id != throughline_id:
                continue
            beat = beats_by_id.get(advance.beat_id)
            if beat is None:
                continue
            return beat.beat_type
    return None


def fabula_end_τ_s(fabula) -> int:
    """Highest τ_s across a fabula's events. Skips events with
    `τ_s is None` (unanchored / pre-fabula records). Raises
    `ValueError` if no event in the fabula has a τ_s — the dramatica-
    complete verifiers rely on this as the arc endpoint, so a silent
    zero would be a semantic lie."""
    return max(e.τ_s for e in fabula if e.τ_s is not None)


def events_lowered_from_throughline(
    throughline_id: str,
    lowerings,
    fabula,
) -> tuple:
    """Return substrate Events reached via ACTIVE Lowerings whose
    `upper_record` is the named Dramatic Throughline. Complementary
    to `events_advancing_throughline` below: this helper walks direct
    `T_* → substrate-events` Lowerings; the other walks Scene-level
    Lowerings whose scene `advances` the throughline. Encodings with
    direct Throughline Lowerings (Ackroyd, Macbeth, Oedipus, Rocky)
    use this; others fall back to the Scene.advances path.

    Iterates `lowerings` in input order, collects substrate
    `lower_records`, then resolves each id to an Event via linear
    scan over `fabula`. Duplicate ids are kept (matching the prior
    per-encoding copies — the same substrate Event can appear under
    two ACTIVE Lowerings, which is a distinct authorial claim the
    caller may want to see)."""
    upper = cross_ref("dramatic", throughline_id)
    event_ids: list = []
    for lw in lowerings:
        if lw.upper_record != upper:
            continue
        if lw.status != LoweringStatus.ACTIVE:
            continue
        for lr in lw.lower_records:
            if lr.dialect == "substrate":
                event_ids.append(lr.record_id)
    events: list = []
    for eid in event_ids:
        for e in fabula:
            if e.id == eid:
                events.append(e)
                break
    return tuple(events)


def events_advancing_throughline(
    throughline_id: str,
    lowerings,
    scenes,
    fabula,
):
    """Collect substrate events realized by Scenes that advance the
    named throughline, via Scene.advances. Complementary to direct
    throughline-Lowering lookup (`events_lowered_from_throughline`
    above): some encodings have a direct T_ic_* → events Lowering
    (Ackroyd, Macbeth), others don't (Oedipus, Rocky), and the
    Scene.advances path recovers IC-throughline events for the latter.

    Walk:
      1. For each Scene-level Lowering, check if the Scene's
         `advances` tuple contains an entry with
         `throughline_id=target`.
      2. If yes, collect the Lowering's substrate lower_records.
      3. Resolve each to an Event via the fabula.

    Returns a tuple of matching Event records (order preserved as
    encountered; caller sorts by τ_s as needed).
    """
    scenes_by_id = {s.id: s for s in scenes}
    events_by_id = {e.id: e for e in fabula}
    out: list = []
    seen: set = set()
    for lw in lowerings:
        ur = lw.upper_record
        if ur.dialect != "dramatic":
            continue
        scene = scenes_by_id.get(ur.record_id)
        if scene is None:
            continue
        if not any(
            adv.throughline_id == throughline_id
            for adv in scene.advances
        ):
            continue
        if getattr(lw, "status", None) is not None and lw.status != LoweringStatus.ACTIVE:
            continue
        for lr in lw.lower_records:
            if lr.dialect != "substrate":
                continue
            if lr.record_id in seen:
                continue
            ev = events_by_id.get(lr.record_id)
            if ev is not None:
                out.append(ev)
                seen.add(lr.record_id)
    return tuple(out)


def compute_pre_post_action_ratios(
    mc_id: str,
    transition_τ,
    events_in_scope: list,
    agent_ids,
    shift_threshold: float = 0.3,
) -> dict:
    """RE2/RE5: compare MC EK2 action-shape ratio pre vs post a
    transition τ_s. Returns dict with pre/post counts, external-
    ratios, absolute shift, and shift_detected bool (shift ≥
    threshold).

    Used by Change-declared DSP_resolve checks to detect whether
    the MC's behavioral signature structurally changes across the
    transition — a positive end-state signal for Change per
    resolve-endpoint-sketch-01.

    `transition_τ` is the MC's identity / paradigm transition τ_s.
    `events_in_scope` is the canonical fabula; `agent_ids` is the
    frozenset EK2 expects.
    """
    if transition_τ is None:
        return {
            "pre_count": 0,
            "post_count": 0,
            "pre_external_ratio": 0.0,
            "post_external_ratio": 0.0,
            "shift": 0.0,
            "shift_detected": False,
        }

    pre_external = pre_total = 0
    post_external = post_total = 0
    for e in events_in_scope:
        if e.τ_s is None:
            continue
        parts = event_participants_flat(e)
        if mc_id not in parts:
            continue
        shape = classify_event_action_shape(e, agent_ids=agent_ids)
        if e.τ_s < transition_τ:
            pre_total += 1
            if shape == "external":
                pre_external += 1
        else:
            post_total += 1
            if shape == "external":
                post_external += 1

    pre_ratio = pre_external / pre_total if pre_total > 0 else 0.0
    post_ratio = post_external / post_total if post_total > 0 else 0.0
    shift = abs(pre_ratio - post_ratio)
    return {
        "pre_count": pre_total,
        "post_count": post_total,
        "pre_external_ratio": pre_ratio,
        "post_external_ratio": post_ratio,
        "shift": shift,
        "shift_detected": shift >= shift_threshold,
    }


def detect_preceding_ic_event(
    target_τ,
    ic_event_τs,
    window: int = 5,
) -> dict:
    """RR2/RR4: check whether any IC-throughline event τ_s falls in
    the window [target_τ - window, target_τ] — detecting temporal
    correlation between an IC event and a later MC critical moment.

    Returns a dict with:
      - has_correlation: bool — True if any IC τ_s is in the window.
      - nearest_preceding_ic_τ: Optional[int] — the latest IC τ_s
        in the window (closest before target_τ), or None.
      - gap: Optional[int] — target_τ - nearest_preceding_ic_τ.
      - ic_events_in_window: tuple[int] — all IC τ_s in the window,
        sorted ascending.

    `target_τ` may be None (e.g., Steadfast encodings with no MC
    transition); returns has_correlation=False and None values in
    that case. `ic_event_τs` is a list/tuple of τ_s values (ints).

    Per RR6 the frame is verifier-local; per RR1 the detection is
    purely structural (no type-string dispatch).
    """
    if target_τ is None:
        return {
            "has_correlation": False,
            "nearest_preceding_ic_τ": None,
            "gap": None,
            "ic_events_in_window": (),
        }
    lo = target_τ - window
    in_window = sorted(t for t in ic_event_τs if t is not None and lo <= t <= target_τ)
    if not in_window:
        return {
            "has_correlation": False,
            "nearest_preceding_ic_τ": None,
            "gap": None,
            "ic_events_in_window": (),
        }
    nearest = in_window[-1]
    return {
        "has_correlation": True,
        "nearest_preceding_ic_τ": nearest,
        "gap": target_τ - nearest,
        "ic_events_in_window": tuple(in_window),
    }


def classify_event_manipulation_shape(
    event,
    mc_id: str,
    events_in_scope: list,
):
    """Classify an event as manipulation-shaped / not, per
    event-manipulation-taxonomy-sketch-01 (MN1–MN5).

    Returns:
        - `None` — MC is not a participant in the event.
        - `"manipulation"` — MN2's concealment-asymmetry predicate
          fires: MC holds at least one self-fact at `Slot.KNOWN`
          (a world-proposition with `prop.args[0] == mc_id`) that
          at least one non-MC participant in this event does NOT
          hold at `Slot.KNOWN` at event.τ_s.
        - `"non-manipulation"` — MC participates but MN2 does not
          fire (no asymmetry found among this event's participants).

    Per MN1, reads fold-visible structure only — participants dict,
    world-state via `project_world`, each non-MC participant's
    `KnowledgeState` via `project_knowledge`. No event type strings,
    no participant role names.

    `events_in_scope` is the canonical-scope fabula list the verifier
    is running over — used to project world state and per-agent
    knowledge at `event.τ_s`.
    """
    # Lazy import to keep verifier_helpers' import graph narrow.
    from story_engine.core.substrate import (
        project_world as _project_world,
        project_knowledge as _project_knowledge,
        Slot as _Slot,
    )

    participant_ids = event_participants_flat(event)
    if mc_id not in participant_ids:
        return None

    τ = event.τ_s
    if τ is None:
        return "non-manipulation"

    world = _project_world(events_in_scope=events_in_scope, up_to_τ_s=τ)
    # Self-facts: world-propositions whose first argument is mc_id.
    self_facts = [
        p for p in world
        if p.args and str(p.args[0]) == mc_id
    ]
    if not self_facts:
        return "non-manipulation"

    mc_state = _project_knowledge(
        agent_id=mc_id,
        events_in_scope=events_in_scope,
        up_to_τ_s=τ,
    )
    mc_known_self_facts = [
        p for p in self_facts if mc_state.holds_as(p, _Slot.KNOWN)
    ]
    if not mc_known_self_facts:
        return "non-manipulation"

    non_mc_participants = [p for p in participant_ids if p != mc_id]
    if not non_mc_participants:
        # MC is the only participant; asymmetry needs at least one
        # other agent in the event.
        return "non-manipulation"

    # Fire on first asymmetry found: any (self-fact, other-participant)
    # pair where the other does not hold the fact at KNOWN.
    for other_id in non_mc_participants:
        other_state = _project_knowledge(
            agent_id=other_id,
            events_in_scope=events_in_scope,
            up_to_τ_s=τ,
        )
        for p in mc_known_self_facts:
            if not other_state.holds_as(p, _Slot.KNOWN):
                return "manipulation"

    return "non-manipulation"


def agent_ids_from_entities(entities: tuple) -> frozenset:
    """Build the `agent_ids` frozenset the EK2 classifier expects,
    from an encoding's `ENTITIES` tuple. Selects entities whose
    `kind == "agent"` — excluding locations, objects, and abstract
    placeholders. Used by cross-boundary verifiers; each encoding
    passes its own ENTITIES in."""
    return frozenset(e.id for e in entities if e.kind == "agent")


def entity_id_for_character(
    character_id: str,
    lowerings: tuple,
    entities: tuple,
) -> str:
    """Walk `lowerings` to find the substrate Entity id that the
    given Dramatic Character lowers to. Returns the entity id string,
    or None if no ACTIVE Lowering exists or the lowering targets
    aren't substrate Entities.

    `entities` disambiguates Entity ids from Event ids — both live in
    the 'substrate' dialect namespace, but Character Lowerings should
    target Entities. A lowering whose lower_records name substrate
    Events (not Entities) is skipped, so a misauthored Lowering
    pointing a Character at an Event doesn't silently pass.
    """
    char_ref = cross_ref("dramatic", character_id)
    for lw in lowerings:
        if lw.upper_record != char_ref:
            continue
        if lw.status != LoweringStatus.ACTIVE:
            continue
        for lr in lw.lower_records:
            if lr.dialect == "substrate":
                if any(e.id == lr.record_id for e in entities):
                    return lr.record_id
    return None
