"""
Substrate — Python reference implementation of design/substrate-sketch-04.md.

This module is written as an executable specification. It prioritizes fidelity
to the sketch and mechanical portability over Pythonic idiom. No metaclasses,
no decorators beyond @dataclass, no generators where a list will do. A reader
porting this to another language should not have to guess intent.

Sketch-04 commitments implemented:
  E1   event-primary; state is a fold over the event log
  E2   typed events (partial-order not yet exploited; total order suffices)
  E3   tri-temporal fields (τ_s, τ_a present; τ_d lives in the sjuzhet)
  K1   per-agent knowledge projection via fold
  K2   reader as epistemic subject with disjoint narrative update operators
  B1   branch labels, kinds, fold-scope rule

Deliberately omitted in this first prototype:
  F1                 emotional / tension projections
  partial order      total order is enough for the encoded slice
  contested branches code supports shape; no encoded story uses them yet
  draft branches     as above; see open question 14
  counterfactuals    as above
  framing, omission, retroactive reframing
  causality warrants beyond preconditions
  BLANK slot distinct from GAP (collapsed)
  inference engine   realizations are authored events, not derived
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union


# ----------------------------------------------------------------------------
# Entities
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Entity:
    """Anything referred to by the story. Agents are entities with kind='agent'
    (see sketch 04 ontology: Agent is a subtype of Entity, but a Python
    inheritance hierarchy adds portability friction we don't need here).
    """
    id: str
    name: str
    kind: str  # "agent", "object", "location", "abstract"


# ----------------------------------------------------------------------------
# Propositions
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Prop:
    """A fact-shaped claim: predicate + tuple of arguments. Hashable so
    propositions can be keys in dicts and members of sets. Args are either
    entity ids (strings) or primitive values.
    """
    predicate: str
    args: tuple

    def __repr__(self) -> str:
        return f"{self.predicate}({', '.join(repr(a) for a in self.args)})"


# ----------------------------------------------------------------------------
# Branches (B1)
# ----------------------------------------------------------------------------

class BranchKind(str, Enum):
    CANONICAL = "canonical"
    CONTESTED = "contested"
    DRAFT = "draft"
    COUNTERFACTUAL = "counterfactual"


CANONICAL_LABEL = ":canonical"


@dataclass(frozen=True)
class Branch:
    """A branch label with kind and parent. Parent defaults per sketch 04:

      - :canonical must NOT have a parent (it is root).
      - :contested defaults to :canonical as parent if none is given.
      - :draft and :counterfactual MUST name a parent (or source, for
        counterfactuals) explicitly — they are children of something.

    These defaults and requirements are enforced in __post_init__ rather
    than left to caller discipline. For a reference implementation, the
    invariant belongs in the data type, not in documentation.
    """
    label: str
    kind: BranchKind
    parent: Optional[str] = None

    def __post_init__(self):
        if self.kind == BranchKind.CANONICAL:
            if self.parent is not None:
                raise ValueError(
                    f":canonical branch {self.label!r} must not have a parent"
                )
            return

        if self.kind == BranchKind.CONTESTED:
            if self.parent is None:
                object.__setattr__(self, "parent", CANONICAL_LABEL)
            return

        # DRAFT or COUNTERFACTUAL
        if self.parent is None:
            raise ValueError(
                f"Branch {self.label!r} of kind {self.kind.value!r} must "
                f"name a parent (counterfactuals: a source) explicitly"
            )


CANONICAL = Branch(label=CANONICAL_LABEL, kind=BranchKind.CANONICAL, parent=None)


# ----------------------------------------------------------------------------
# Epistemic slots and confidences (K1)
# ----------------------------------------------------------------------------

class Slot(str, Enum):
    KNOWN = "known"
    BELIEVED = "believed"
    SUSPECTED = "suspected"
    GAP = "gap"
    # BLANK deliberately collapsed to GAP in this prototype.


class Confidence(str, Enum):
    CERTAIN = "certain"
    BELIEVED = "believed"
    SUSPECTED = "suspected"
    OPEN = "open"  # for gaps — the agent is aware the question is open


# ----------------------------------------------------------------------------
# Update operator names (K2)
# ----------------------------------------------------------------------------

class Diegetic(str, Enum):
    OBSERVATION = "observation"
    UTTERANCE_HEARD = "utterance-heard"
    INFERENCE = "inference"
    DECEPTION = "deception"
    FORGETTING = "forgetting"
    REALIZATION = "realization"


class Narrative(str, Enum):
    DISCLOSURE = "disclosure"
    FOCALIZATION = "focalization"
    OMISSION = "omission"
    FRAMING = "framing"
    RETROACTIVE_REFRAMING = "retroactive-reframing"


# ----------------------------------------------------------------------------
# Held propositions — what an agent holds in its knowledge state
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Held:
    """One proposition held by an agent, with slot, confidence, operator, and
    a minimal provenance trail. Provenance is a tuple of short strings in this
    prototype; a production system would carry richer causality links.
    """
    prop: Prop
    slot: Slot
    confidence: Confidence
    via: str                # the name of the update operator that placed this
    provenance: tuple = ()  # ("observed @ τ=-100",) or ("heard from messenger @ τ=3",)


# ----------------------------------------------------------------------------
# Effects
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class KnowledgeEffect:
    """Effect on an agent's epistemic state.

    If remove=True the proposition is removed (used by realization/forgetting
    to migrate old beliefs out). Otherwise the Held replaces any prior Held
    for the same proposition on this agent.
    """
    agent_id: str
    held: Held
    remove: bool = False


@dataclass(frozen=True)
class WorldEffect:
    """Effect on the shared canonical world state. World state is used for
    enforcement checks (preconditions) and for the 'what is actually true'
    side of Sternberg queries.
    """
    prop: Prop
    asserts: bool = True


Effect = Union[KnowledgeEffect, WorldEffect]


# ----------------------------------------------------------------------------
# Events (E1, E2, E3)
# ----------------------------------------------------------------------------

class EventStatus(str, Enum):
    COMMITTED = "committed"
    PROVISIONAL = "provisional"


@dataclass(frozen=True)
class Event:
    id: str
    type: str                                    # story-level event type
    τ_s: int                                     # story-time
    τ_a: int                                     # authored-time (sequence number)
    participants: dict                           # role -> entity_id
    effects: tuple                               # tuple[Effect]
    preconditions: tuple = ()                    # tuple[Prop]
    status: EventStatus = EventStatus.COMMITTED
    branches: frozenset = frozenset({CANONICAL_LABEL})
    metadata: dict = field(default_factory=dict)


# ----------------------------------------------------------------------------
# Fold-scope rule (B1)
# ----------------------------------------------------------------------------

def ancestor_chain(branch: Branch, all_branches: dict) -> list:
    """Parent chain up to the root, excluding self. all_branches is a dict
    mapping label -> Branch."""
    chain = []
    current_label = branch.parent
    while current_label is not None:
        ancestor = all_branches.get(current_label)
        if ancestor is None:
            break
        chain.append(ancestor)
        current_label = ancestor.parent
    return chain


def in_scope(event: Event, branch: Branch, all_branches: dict) -> bool:
    """Whether an event is in fold-scope for branch `branch`, per sketch 04.

    Rule:
      - The event is in scope if it carries `branch.label` directly, or if it
        carries the label of any ancestor of `branch` (walking up the parent
        chain). The canonical-is-universal consequence: pre-divergence events
        labeled :canonical are picked up on every downstream branch.
      - The event is NOT in scope if it is only on a sibling :contested
        branch — sibling contested branches do not inherit from each other.

    Draft supersession (open question 14) and counterfactual removal are not
    yet implemented. When the prototype gains those, this function gains an
    exclusion check against branch-specific supersession/removal metadata.
    """
    if branch.label in event.branches:
        return True
    for ancestor in ancestor_chain(branch, all_branches):
        if ancestor.label in event.branches:
            return True
    return False


def scope(branch: Branch, events: list, all_branches: dict) -> list:
    """All events in fold-scope for `branch`, sorted by (τ_s, τ_a).

    The τ_a tiebreaker is load-bearing: two events at the same story-time
    can touch the same proposition, and the 'later effects win' fold rule
    is only well-defined if the ordering is total and deterministic.
    Story-time alone does not guarantee either. Authorial time does.
    """
    return sorted(
        (e for e in events if in_scope(e, branch, all_branches)),
        key=lambda e: (e.τ_s, e.τ_a),
    )


# ----------------------------------------------------------------------------
# Knowledge state
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class KnowledgeState:
    """An agent's epistemic state at a specific (branch, τ_s). Essentially a
    set of Held propositions, indexed by proposition for O(1) lookups.
    """
    agent_id: str
    by_prop: tuple  # tuple[Held] — effectively a set, kept as tuple for frozen-ness

    def holds(self, p: Prop) -> Optional[Held]:
        for h in self.by_prop:
            if h.prop == p:
                return h
        return None

    def slot(self, slot: Slot) -> list:
        return [h for h in self.by_prop if h.slot == slot]

    def known(self) -> list:      return self.slot(Slot.KNOWN)
    def believed(self) -> list:   return self.slot(Slot.BELIEVED)
    def suspected(self) -> list:  return self.slot(Slot.SUSPECTED)
    def gaps(self) -> list:       return self.slot(Slot.GAP)

    def holds_as(self, p: Prop, slot: Slot) -> bool:
        h = self.holds(p)
        return h is not None and h.slot == slot


# ----------------------------------------------------------------------------
# Per-agent knowledge projection (K1)
# ----------------------------------------------------------------------------

def project_knowledge(
    agent_id: str,
    events_in_scope: list,
    up_to_τ_s: int,
) -> KnowledgeState:
    """Fold knowledge-effects targeting `agent_id` up to `up_to_τ_s`.

    Fold rules:
      - A non-remove KnowledgeEffect replaces any prior Held for the same
        proposition.
      - A remove=True effect deletes the proposition from the state.
      - Later effects win over earlier ones (events are in τ_s order).
    """
    by_prop = {}  # prop -> Held

    for event in events_in_scope:
        if event.τ_s > up_to_τ_s:
            break
        for effect in event.effects:
            if not isinstance(effect, KnowledgeEffect):
                continue
            if effect.agent_id != agent_id:
                continue
            if effect.remove:
                by_prop.pop(effect.held.prop, None)
            else:
                by_prop[effect.held.prop] = effect.held

    return KnowledgeState(agent_id=agent_id, by_prop=tuple(by_prop.values()))


# ----------------------------------------------------------------------------
# World-state projection
# ----------------------------------------------------------------------------

def project_world(events_in_scope: list, up_to_τ_s: int) -> set:
    """The set of canonically-asserted world propositions at τ_s."""
    world = {}
    for event in events_in_scope:
        if event.τ_s > up_to_τ_s:
            break
        for effect in event.effects:
            if not isinstance(effect, WorldEffect):
                continue
            if effect.asserts:
                world[effect.prop] = True
            else:
                world.pop(effect.prop, None)
    return set(world.keys())


# ----------------------------------------------------------------------------
# Sjuzhet and reader projection (K2)
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Disclosure:
    """A narrative-update posit. The sjuzhet places this proposition into
    the reader's state at the stated slot/confidence via the named operator.
    """
    prop: Prop
    slot: Slot
    confidence: Confidence
    via: str  # Narrative.* value


@dataclass(frozen=True)
class SjuzhetEntry:
    """Narration of a fabula event. Carries narrative-update metadata. The
    reader's projection is folded from a sequence of these in τ_d order.
    """
    event_id: str
    τ_d: int
    focalizer_id: Optional[str] = None  # None = omniscient
    disclosures: tuple = ()             # tuple[Disclosure]
    # framing, omission, retroactive reframing deferred; see sketch 04 K2.


def _is_shipped(branch_label: str, all_branches: dict) -> bool:
    """A branch is 'shipped' if it is :canonical or :contested.
    :draft and :counterfactual branches are not part of the work.
    """
    b = all_branches.get(branch_label)
    if b is None:
        return False
    return b.kind in (BranchKind.CANONICAL, BranchKind.CONTESTED)


def project_reader(
    sjuzhet: list,              # list[SjuzhetEntry], not required to be sorted
    all_events: list,
    branch: Branch,
    all_branches: dict,
    up_to_τ_d: int,
) -> KnowledgeState:
    """Compute the reader's epistemic state at discourse-time `up_to_τ_d`.

    Validation:
      - The sjuzhet must only reference events that are in fold-scope for
        `branch` (sketch 04: sjuzhet draws only from :canonical and
        :contested branches; implementation detail: the reader branch
        itself is expected to be one of those).
      - The referenced event must carry at least one shipped-kind label.
      - An entry referencing an unknown event id is a spec error.

    All three conditions raise ValueError. A prototype is a specification;
    silently skipping malformed entries would hide bugs downstream.

    Additionally: the reader branch itself must be a shipped kind
    (:canonical or :contested). project_reader is not defined on :draft
    or :counterfactual branches — those are authoring or analytical
    constructs that readers do not experience.

    For each sjuzhet entry with τ_d ≤ up_to_τ_d, in τ_d order:
      - Focalization is recorded as metadata only. See note below.
      - Explicit disclosures are applied with their stated slot/confidence
        and operator. A later disclosure overrides any prior disclosure for
        the same proposition, which is how reveals and foreshadow-payoffs
        migrate reader state.

    Note on focalization semantics (prototype-level):

    Sketch 04 K2 defines focalization as a constraint on reader access:
    propositions the focalizer lacks become reader-gaps; propositions the
    focalizer misconstrues become reader-believed rather than reader-known.
    That is subtle to implement correctly — in particular, demotion of
    prior disclosures requires τ_d-scoped reader-state tracking we do not
    yet have. Previous drafts of this function folded the focalizer's
    entire state into the reader's state; that was wrong (it collapses
    'the scene is routed through X's perspective' into 'the narration
    dumps X's mind into the reader'). The current implementation records
    focalization as metadata only: no automatic state mutation occurs.
    Disclosures remain the only positive-update operator.

    This is weaker than sketch 04 asserts. Proper focalization semantics
    are a deliberate deferred item for a later sketch/prototype iteration.
    """
    if branch.kind not in (BranchKind.CANONICAL, BranchKind.CONTESTED):
        raise ValueError(
            f"project_reader may only be called on shipped branches "
            f"(:canonical or :contested); got branch {branch.label!r} "
            f"of kind {branch.kind.value!r}"
        )

    by_prop = {}  # prop -> Held
    event_by_id = {e.id: e for e in all_events}
    entries_sorted = sorted(sjuzhet, key=lambda s: s.τ_d)

    for entry in entries_sorted:
        if entry.τ_d > up_to_τ_d:
            break

        event = event_by_id.get(entry.event_id)
        if event is None:
            raise ValueError(
                f"Sjuzhet entry at τ_d={entry.τ_d} references unknown "
                f"event id {entry.event_id!r}"
            )

        if not in_scope(event, branch, all_branches):
            raise ValueError(
                f"Sjuzhet entry at τ_d={entry.τ_d} narrates event "
                f"{entry.event_id!r}, which is not in fold-scope for "
                f"branch {branch.label!r}"
            )

        if not any(_is_shipped(label, all_branches) for label in event.branches):
            raise ValueError(
                f"Sjuzhet entry at τ_d={entry.τ_d} narrates event "
                f"{entry.event_id!r}, which is not on any shipped branch "
                f"(branches={sorted(event.branches)!r}); sjuzhet may not "
                f"draw from :draft or :counterfactual branches"
            )

        # Focalization: metadata only; no positive state update.
        # (The focalizer_id is preserved on the entry for later inspection
        # and for a future inference/reader-model layer.)

        for d in entry.disclosures:
            by_prop[d.prop] = Held(
                prop=d.prop,
                slot=d.slot,
                confidence=d.confidence,
                via=d.via,
                provenance=(f"disclosed @ τ_d={entry.τ_d}",),
            )

    return KnowledgeState(agent_id="reader", by_prop=tuple(by_prop.values()))


# ----------------------------------------------------------------------------
# Queries
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Irony:
    """A live dramatic-irony instance at τ_s on a branch.

    A holds `prop` as known; B does not (or holds it only as suspected/gap);
    the reader is aware (holds it as known or believed).
    """
    informed_id: str
    uninformed_id: str
    prop: Prop
    τ_s: int
    branch_label: str

    def __repr__(self) -> str:
        return (f"Irony({self.informed_id} > {self.uninformed_id}, "
                f"{self.prop}, τ_s={self.τ_s}, branch={self.branch_label})")


def dramatic_ironies(
    agent_ids: list,
    reader_state: KnowledgeState,
    all_events: list,
    branch: Branch,
    all_branches: dict,
    τ_s: int,
) -> list:
    """All live dramatic-irony triples at τ_s on `branch`.

    Two classes of irony are reported:

    (1) Reader > Character. For each proposition p the reader KNOWS, and
        for each character c that does not hold p as KNOWN, an irony
        fires. This is the Oedipus Rex class of irony: the audience knows
        more than the protagonist.

    (2) Character > Character, with the reader aware. For each ordered
        pair (A, B) of distinct characters, if A holds p as KNOWN and B
        does not, and the reader also holds p (KNOWN or BELIEVED), an
        irony fires. This is the Jocasta-realizes-first class.

    Both classes return Irony records. The substrate does not distinguish
    them; the caller can filter by informed_id == "reader" if desired.
    """
    events_in_scope = scope(branch, all_events, all_branches)
    states = {aid: project_knowledge(aid, events_in_scope, τ_s) for aid in agent_ids}

    results = []

    # (1) Reader > Character ironies.
    for h in reader_state.known():
        for aid in agent_ids:
            held = states[aid].holds(h.prop)
            if held is None or held.slot != Slot.KNOWN:
                results.append(Irony(
                    informed_id="reader",
                    uninformed_id=aid,
                    prop=h.prop,
                    τ_s=τ_s,
                    branch_label=branch.label,
                ))

    # (2) Character > Character ironies (reader aware).
    for informed_id in agent_ids:
        for h in states[informed_id].known():
            if not (reader_state.holds_as(h.prop, Slot.KNOWN) or
                    reader_state.holds_as(h.prop, Slot.BELIEVED)):
                continue
            for uninformed_id in agent_ids:
                if informed_id == uninformed_id:
                    continue
                b_held = states[uninformed_id].holds(h.prop)
                if b_held is None or b_held.slot != Slot.KNOWN:
                    results.append(Irony(
                        informed_id=informed_id,
                        uninformed_id=uninformed_id,
                        prop=h.prop,
                        τ_s=τ_s,
                        branch_label=branch.label,
                    ))

    return results


def sternberg_curiosity(reader_state: KnowledgeState) -> list:
    """Reader's open curiosity gaps — propositions in the GAP slot.

    Sketch 04 distinguishes curiosity (past-facing gap) from suspense (future-
    facing gap). The prototype treats any GAP as curiosity; suspense needs a
    concept of 'outcome not yet reached' that we don't model yet. Left as an
    extension point when the prototype earns its next iteration.
    """
    return reader_state.gaps()
