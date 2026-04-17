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

from substrate import (
    Event, KnowledgeEffect, WorldEffect,
    IDENTITY_PREDICATE, in_scope, project_world, derive_all_world,
)
from dramatic import Throughline, ABSTRACT_THROUGHLINE_OWNERS
from lowering import cross_ref, LoweringStatus


# Role-name precedence for identifying an event's "primary actor" —
# the participant whose knowledge/agency the event centers. Ordered
# most-specific first; the first role present in an event's
# `participants` dict wins. Encodings that introduce new role names
# may extend this list, but the five below cover every event shape
# in the current Oedipus / Macbeth / Ackroyd encodings.
_PRIMARY_ACTOR_ROLES = ("killer", "speaker", "actor", "agent", "subject")


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
    for v in event.participants.values():
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


def classify_arc_limit_shape_strong(
    fabula,
    rules,
    canonical_branch,
    all_branches: dict,
) -> dict:
    """LT7–LT9 arc-position-aware classifier per pressure-shape-
    taxonomy-sketch-02. Extends `classify_arc_limit_shape` with:

      1. **LT7** — each LT2 convergence signal is tagged by arc
         position: `peripheral-pre` (τ_s < 0, substrate convention
         for backstory), `terminal` (τ_s within top 10% of the
         positive-arc range), or `middle-arc` (the remainder).
      2. **LT8** — scheduling-predicate signals: any `WorldEffect`
         whose prop's predicate begins with `"scheduled_"` is a
         positive Timelock signal, regardless of whether it
         asserts or retracts. The prefix is verifier-local
         vocabulary per LT6.
      3. **LT9** — strong Timelock predicate: scheduling signal
         present AND middle-arc LT2 signal count is zero.

    Returns a dict with the following keys:

      - `classification`: one of `"optionlock"`, `"timelock-strong"`,
        `"timelock-consistent"`, `"optionlock-peripheral"`,
        `"undetermined"`.
      - `strength`: float in [0.0, 1.0].
      - `signals`: tuple of `"<kind>:<count>"` strings, compatible
        with sketch-01's format (flat totals across all positions).
      - `middle_arc_kinds`: count of distinct LT2 signal kinds with
        at least one middle-arc event.
      - `peripheral_pre_count`, `middle_arc_count`, `terminal_count`:
        event counts per band across all three LT2 signal kinds.
      - `scheduling_signals`: tuple of predicate names that fired
        LT8 (distinct `Prop` count, not event count).
      - `scheduling_count`: number of distinct `Prop`s in
        `scheduling_signals`.
      - `arc_range`: `(min_τ_s, max_τ_s)` for diagnostics.
      - `terminal_threshold`: the τ_s cutoff used for terminal-band
        classification (computed as `max_τ_s - 0.1 × positive_span`).

    The existing `classify_arc_limit_shape` is unchanged and
    continues to serve sketch-01-only callers (LT11 back-compat).

    Per LT1, classification is a function of fold-visible substrate
    structure — events, effects, and rule derivations. Per LT11,
    `dsp_limit_characterization_check` below consumes this dict
    directly to apply the LT10 disposition table.
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
    asserted_so_far: set = set()
    retraction_bands = {"peripheral-pre": 0, "middle-arc": 0, "terminal": 0}
    scheduling_props: set = set()
    for e in events_sorted:
        for ef in e.effects:
            if not isinstance(ef, WorldEffect):
                continue
            if ef.prop.predicate.startswith("scheduled_"):
                scheduling_props.add(ef.prop)
            if ef.asserts:
                asserted_so_far.add(ef.prop)
            else:
                if ef.prop in asserted_so_far:
                    retraction_bands[_band_for(e.τ_s)] += 1
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

    # Kinds firing anywhere (sketch-01 format)
    retraction_total = sum(retraction_bands.values())
    identity_total = sum(identity_bands.values())
    rule_emergence_total = sum(rule_emergence_bands.values())
    kinds_firing = sum(
        1 for n in (retraction_total, identity_total, rule_emergence_total)
        if n > 0
    )

    # Middle-arc kinds (LT7 / LT9)
    middle_arc_kinds = sum(
        1 for n in (
            retraction_bands["middle-arc"],
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

    # Classification per LT7–LT9
    if scheduling_count > 0 and middle_arc_kinds == 0:
        classification = "timelock-strong"
        strength = min(1.0, scheduling_count / 2.0)
    elif middle_arc_kinds > 0:
        classification = "optionlock"
        strength = min(1.0, kinds_firing / 3.0)
    elif kinds_firing == 0 and scheduling_count == 0:
        classification = "timelock-consistent"
        strength = 0.5
    else:
        # Signals fire but only peripheral/terminal, and no scheduling
        # predicate to support a Timelock-strong reading. LT10's
        # declared=Optionlock + only-peripheral/terminal row.
        classification = "optionlock-peripheral"
        strength = 0.5 * min(1.0, kinds_firing / 3.0)

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
        "arc_range": (min_τ, max_τ),
        "terminal_threshold": terminal_threshold,
    }


def dsp_limit_characterization_check(
    fabula,
    rules,
    canonical_branch,
    all_branches: dict,
    declared_choice: str,
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

    # Import verdict constants lazily to keep verifier_helpers' import
    # graph narrow (verification.py imports verifier_helpers indirectly
    # via the verifier modules; avoid a cycle).
    from verification import (
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
                f"disagree.",
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
                f"min(1.0, {scheduling_count}/2).",
            )
        if classification == "timelock-consistent":
            return (
                VERDICT_NOTED, None,
                f"DSP_limit=Timelock declared; substrate shows no LT2 "
                f"convergence signals AND no scheduling predicate "
                f"(LT8). Consistent with Timelock but not "
                f"affirmatively detected — LT3's honest weak-fallback "
                f"asymmetry (sketch-01). Consider naming the "
                f"scheduled endpoint with a `scheduled_*` predicate "
                f"to fire LT9.",
            )
        if classification == "optionlock-peripheral":
            # Signals fire but only peripheral/terminal, no scheduling.
            # This is Timelock-compatible in spirit — no middle-arc
            # convergence — but LT8 did not confirm.
            return (
                VERDICT_NOTED, None,
                f"DSP_limit=Timelock declared; substrate shows LT2 "
                f"signals ({signal_text}) all in arc-peripheral or "
                f"terminal bands ({position_text}) and no scheduling "
                f"predicate (LT8). Middle-arc is clean (consistent "
                f"with Timelock); LT9 does not fire for lack of "
                f"scheduling signal. Consider naming the scheduled "
                f"endpoint to lift the verdict to APPROVED.",
            )
        # classification == "optionlock" — substrate exhibits middle-arc
        # convergence, contradicting the Timelock declaration.
        return (
            VERDICT_NEEDS_WORK, 1.0 - result["strength"],
            f"DSP_limit=Timelock declared, but substrate exhibits "
            f"middle-arc LT2 convergence ({signal_text}; "
            f"{position_text}). The arc body looks Optionlock-shaped "
            f"per LT2+LT7. Either the DSP choice needs revisiting or "
            f"the substrate's convergence is incidental to a "
            f"genuinely schedule-driven arc (LT9 does not fire: "
            f"{scheduling_count} scheduling predicate(s) present).",
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
    from substrate import (
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
