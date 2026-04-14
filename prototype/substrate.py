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
  draft branches     code supports shape; no encoded story uses them yet
  counterfactuals    as above
  framing, omission, retroactive reframing
  causality warrants beyond preconditions
  BLANK slot distinct from GAP (collapsed)
  inference engine   realizations are authored events, not derived
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
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

# ----------------------------------------------------------------------------
# Identity substitution helpers (identity-and-realization-sketch-01)
# ----------------------------------------------------------------------------
#
# Identity is a first-class proposition (I1). Predicate name is "identity",
# arity 2, arguments are entity ids. Substitution happens at query time
# (I3); the held set is literal. Substitution fires only on KNOWN
# identities (I7).
#
# The helpers here are module-private (underscore-prefixed) because they
# are consumed by KnowledgeState methods and by world_holds; they are not
# part of the public surface the sketch documents.

IDENTITY_PREDICATE = "identity"

_SLOT_RANK = {
    Slot.KNOWN: 3,
    Slot.BELIEVED: 2,
    Slot.SUSPECTED: 1,
    Slot.GAP: 0,
}


def _weaker_slot(a: Slot, b: Slot) -> Slot:
    """Return the weaker of two slots under
    KNOWN > BELIEVED > SUSPECTED > GAP. Used by focalization per
    focalization-sketch-01 F1 and by any other caller that needs
    the 'min' of two epistemic slots."""
    return a if _SLOT_RANK[a] <= _SLOT_RANK[b] else b


def _known_identities_from(held_list) -> list:
    """Extract the identity/2 propositions held as KNOWN. I7: only KNOWN
    identities participate in equivalence-class construction."""
    return [
        h.prop for h in held_list
        if h.slot == Slot.KNOWN
        and h.prop.predicate == IDENTITY_PREDICATE
        and len(h.prop.args) == 2
    ]


def _build_equivalence_classes(identity_props: list) -> dict:
    """Union-find over identity propositions. Returns a dict mapping each
    entity id that appears in any identity to the frozenset of all entities
    in its equivalence class. Entity ids not in any identity proposition
    are not in the returned dict — they are trivially singleton classes,
    and callers treat "not in map" as "equivalent only to self".
    """
    parents = {}

    def find(x):
        # Iterative with path compression.
        while parents[x] != x:
            parents[x] = parents[parents[x]]
            x = parents[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parents[ra] = rb

    for p in identity_props:
        # Defensive filter — callers are expected to pre-filter, but a
        # silent wrong answer from unioning non-identity props is worse
        # than a cheap predicate/arity check here.
        if p.predicate != IDENTITY_PREDICATE or len(p.args) != 2:
            continue
        a, b = p.args
        parents.setdefault(a, a)
        parents.setdefault(b, b)
        union(a, b)

    classes = {}
    for x in list(parents.keys()):
        root = find(x)
        classes.setdefault(root, set()).add(x)

    return {x: frozenset(classes[find(x)]) for x in parents}


def _equivalent(a, b, class_map: dict) -> bool:
    """Two entity references are equivalent if equal, or if both appear
    in the class_map and share a class."""
    if a == b:
        return True
    if a not in class_map or b not in class_map:
        return False
    return class_map[a] is class_map[b] or class_map[a] == class_map[b]


def _prop_matches_under_substitution(
    literal: Prop, query: Prop, class_map: dict,
) -> bool:
    """A literal Prop matches a query Prop under substitution iff the
    predicates match, the arity matches, and each positional arg is
    equivalent under the equivalence classes.
    """
    if literal.predicate != query.predicate:
        return False
    if len(literal.args) != len(query.args):
        return False
    for la, qa in zip(literal.args, query.args):
        if not _equivalent(la, qa, class_map):
            return False
    return True


@dataclass(frozen=True)
class KnowledgeState:
    """An agent's epistemic state at a specific (branch, τ_s). Essentially a
    set of Held propositions, indexed by proposition for O(1) lookups.

    Under identity-and-realization-sketch-01, query methods on this state
    are substitution-aware by default — `holds` resolves equivalence
    classes from KNOWN identity propositions the agent holds and matches
    against the literal held set. The held set itself stays literal (I3).
    """
    agent_id: str
    by_prop: tuple  # tuple[Held] — effectively a set, kept as tuple for frozen-ness

    def holds_literal(self, p: Prop) -> Optional[Held]:
        """Literal match against by_prop. No substitution. Used for
        debugging, for rendering an agent's un-realized beliefs, and for
        pinning the literal-set-preservation invariant in tests."""
        for h in self.by_prop:
            if h.prop == p:
                return h
        return None

    def holds(self, p: Prop) -> Optional[Held]:
        """Substitution-aware query per identity-and-realization-sketch-01
        I3 + I7. Returns the strongest-slot match among literal Held
        records that match `p` under the agent's KNOWN-identity
        equivalence classes. Tiebreak: the earliest record in by_prop
        (by_prop is built in τ_s, τ_a event order by project_knowledge,
        so by_prop order is a proxy for authored-time order).
        """
        matches = self.holds_all_matches(p)
        if not matches:
            return None
        return matches[0]

    def holds_all_matches(self, p: Prop) -> list:
        """All literal Held records matching `p` under substitution, in
        strongest-slot-then-earliest-by-prop-order. An empty list means
        the agent does not hold `p` even under substitution."""
        class_map = self._known_identity_classes()
        results = [
            (idx, h) for idx, h in enumerate(self.by_prop)
            if _prop_matches_under_substitution(h.prop, p, class_map)
        ]
        results.sort(key=lambda pair: (-_SLOT_RANK[pair[1].slot], pair[0]))
        return [h for _, h in results]

    def _known_identity_classes(self) -> dict:
        """The equivalence-class map induced by this agent's KNOWN
        identity propositions."""
        return _build_equivalence_classes(_known_identities_from(self.by_prop))

    def equivalence_classes(self) -> list:
        """List of non-singleton equivalence classes under the agent's
        KNOWN identities. Singletons are implicit (any entity not in any
        returned class is equivalent only to itself)."""
        class_map = self._known_identity_classes()
        seen = set()
        out = []
        for cls in class_map.values():
            key = frozenset(cls)
            if key in seen:
                continue
            seen.add(key)
            out.append(key)
        return out

    def slot(self, slot: Slot) -> list:
        """Literal slot introspection: the Held records whose literal slot
        is `slot`. Substitution does not apply — these methods report what
        the agent has committed, not what they hold under substitution."""
        return [h for h in self.by_prop if h.slot == slot]

    def known(self) -> list:      return self.slot(Slot.KNOWN)
    def believed(self) -> list:   return self.slot(Slot.BELIEVED)
    def suspected(self) -> list:  return self.slot(Slot.SUSPECTED)
    def gaps(self) -> list:       return self.slot(Slot.GAP)

    def holds_as(self, p: Prop, slot: Slot) -> bool:
        """True iff substitution-aware holds(p) returns a Held at the
        requested slot."""
        h = self.holds(p)
        return h is not None and h.slot == slot


# ----------------------------------------------------------------------------
# World-side substitution query (identity-and-realization-sketch-01 I2)
# ----------------------------------------------------------------------------
#
# project_world returns a set of Props. Substitution over the world set
# follows the same rule: build equivalence classes from any identity/2
# props in the set, match queries under the classes. The world set has
# no slot (world facts are asserted, not believed at a slot), so there
# is no "strongest match" to pick — world_holds returns a bool.


def world_holds(query: Prop, world_props: set) -> bool:
    """Substitution-aware query over a world-state set (as returned by
    project_world). Extracts identity/2 propositions from `world_props`,
    builds equivalence classes, and checks whether any prop in the set
    matches `query` under those classes.

    Note: world identities do not have a "known" slot — world-state
    props are assertions, not beliefs. All identity props in the world
    set participate in substitution.
    """
    identity_props = [
        p for p in world_props
        if p.predicate == IDENTITY_PREDICATE and len(p.args) == 2
    ]
    class_map = _build_equivalence_classes(identity_props)
    for p in world_props:
        if _prop_matches_under_substitution(p, query, class_map):
            return True
    return False


def world_holds_literal(query: Prop, world_props: set) -> bool:
    """Literal membership — equivalent to `query in world_props`, but
    provided as a named alias for symmetry with `holds_literal` on
    KnowledgeState."""
    return query in world_props


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
      - Focalization constrains disclosures per focalization-sketch-01
        F1 (see below).
      - Explicit disclosures are applied with their (possibly demoted)
        slot. A later disclosure overrides any prior disclosure for the
        same proposition, which is how reveals and foreshadow-payoffs
        migrate reader state — subject to the F2 guard on focalization-
        driven demotion.

    Focalization semantics per focalization-sketch-01:

      F1 — If the entry's focalizer_id is set, each disclosure is
           constrained to min(author_slot, focalizer_slot) under the
           ordering KNOWN > BELIEVED > SUSPECTED > GAP. If the
           focalizer does not hold the proposition (not even via
           identity substitution per F5), the effective slot is GAP.
           Focalizer access uses substitution-aware holds().

      F2 — Focalization-driven demotion (effective_slot < author_slot)
           cannot override stronger prior reader state. The write is
           skipped when the reader already holds the proposition at a
           slot equal-to-or-stronger-than the focalization-demoted
           slot. Explicit author demotion (omniscient entries, or
           focalized entries where the focalizer is already at the
           author's slot or weaker) still overrides per the usual
           later-disclosure-wins convention.

      F3 — Focalizer's reference state is projected at the narrated
           event's τ_s.

      F4 — Omniscient entries (focalizer_id=None) pass through
           unchanged.

      F5 — Focalizer's holds() is substitution-aware, so KNOWN
           identities extend the focalizer's access exactly as they
           would for any other query.

      F6 — No narrator intrusion; no external focalization in this
           sketch. All disclosures in a focalized entry are
           constrained by F1.
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

    # Events in fold-scope for this branch. Computed once; used to build
    # focalizer states per entry. Building it once (not per entry) is an
    # invariant: the branch is fixed across project_reader's lifetime.
    events_in_scope = scope(branch, all_events, all_branches)

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

        # F1 prep: if focalized, compute the focalizer's state at the
        # narrated event's τ_s (F3). This projection folds the branch-
        # scoped events up to τ_s, so the event's own effects on the
        # focalizer are visible — correct for participants like the
        # speaker of an utterance or the killer of a killing.
        focalizer_state = None
        if entry.focalizer_id is not None:
            focalizer_state = project_knowledge(
                entry.focalizer_id, events_in_scope, event.τ_s,
            )

        for d in entry.disclosures:
            effective_slot = d.slot
            focalization_demoted = False

            if focalizer_state is not None:
                # F5: substitution-aware access. holds() consults the
                # focalizer's KNOWN identities per identity-and-
                # realization-sketch-01 I7.
                focalizer_held = focalizer_state.holds(d.prop)
                focalizer_slot = (
                    focalizer_held.slot if focalizer_held is not None
                    else Slot.GAP
                )
                # F1: effective slot is the weaker of (author, focalizer).
                effective_slot = _weaker_slot(d.slot, focalizer_slot)
                focalization_demoted = (effective_slot != d.slot)

            # F2: focalization-driven demotion must not override stronger
            # prior reader state. The guard is gated on focalization_
            # demoted — explicit author demotion (omniscient weaker
            # disclosure, or focalized-but-not-further-demoted) still
            # overrides per the later-wins convention.
            if focalization_demoted:
                current = by_prop.get(d.prop)
                if current is not None and \
                   _SLOT_RANK[current.slot] >= _SLOT_RANK[effective_slot]:
                    continue

            provenance = (
                f"disclosed @ τ_d={entry.τ_d}"
                + (f", focalized through {entry.focalizer_id} at "
                   f"τ_s={event.τ_s}" if entry.focalizer_id is not None
                   else ""),
            )
            by_prop[d.prop] = Held(
                prop=d.prop,
                slot=effective_slot,
                confidence=d.confidence,
                via=d.via,
                provenance=provenance,
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


# ============================================================================
# Descriptions — the fold-invisible peer surface (descriptions-sketch-01).
# ============================================================================
#
# Facts live above; descriptions live below. The two surfaces never share a
# type in a way that would let a fold function receive a description. That
# separation is the firewall architecture-sketch-01 A2 and descriptions-01 D1
# commit to. The surfaces meet only at the rendering layer (a tool that prints
# a scene prints both) and at authorial promotion (an author turns a
# description into an event, explicitly).
#
# Descriptions are immutable records. Edits append a new description with a
# later τ_a; review history is a tuple of ReviewEntry records. Staleness is
# computed, not stored: a review is stale when its anchor_τ_a is less than
# the anchor's current τ_a.
#
# This prototype implements the event-anchor and description-anchor shapes
# (the two the Rashomon refactor exercises). Effect-anchors, proposition-
# anchors, and sjuzhet-entry-anchors are declared in descriptions-sketch-01
# and left for a later iteration; the shape of AnchorRef is built to admit
# them without a signature change.


class Attention(str, Enum):
    STRUCTURAL = "structural"
    INTERPRETIVE = "interpretive"
    FLAVOR = "flavor"


class ReviewVerdict(str, Enum):
    APPROVED = "approved"
    NEEDS_WORK = "needs-work"
    REJECTED = "rejected"
    NOTED = "noted"


class DescStatus(str, Enum):
    COMMITTED = "committed"
    PROVISIONAL = "provisional"


@dataclass(frozen=True)
class ReviewEntry:
    """One review act on one description.

    `anchor_τ_a` is the anchor's τ_a at the time of review. Staleness is the
    pair (this entry, current anchor τ_a); the entry is not mutated when the
    anchor is edited, the comparison is.
    """
    reviewer_id: str
    reviewed_at_τ_a: int
    verdict: ReviewVerdict
    anchor_τ_a: int
    comment: Optional[str] = None


@dataclass(frozen=True)
class AnchorRef:
    """A description's attachment point. `kind` names the anchor's type
    ('event', 'description'); `target_id` is the anchored record's id.
    Effect-anchors, proposition-anchors, and sjuzhet-entry-anchors are
    reachable from this shape without field additions — the prototype simply
    does not resolve them yet.
    """
    kind: str
    target_id: str


def anchor_event(event_id: str) -> AnchorRef:
    return AnchorRef(kind="event", target_id=event_id)


def anchor_desc(description_id: str) -> AnchorRef:
    return AnchorRef(kind="description", target_id=description_id)


@dataclass(frozen=True)
class Description:
    """A fold-invisible interpretive record attached to a typed anchor.

    `branches=None` means "inherit from the anchor" (the D4 default). An
    explicit `branches` set is a subset override; descriptions-sketch-01's
    subset-override invariant (must be non-empty subset of the anchor's
    branches) is a responsibility of the authoring tool / encoding, not
    enforced at record construction — a prototype would need the anchor
    resolved at construction time to enforce it, which couples this record
    to the event log in a way the data type should not require.
    """
    id: str
    attached_to: AnchorRef
    kind: str
    attention: Attention
    text: str
    authored_by: str
    τ_a: int
    is_question: bool = False
    branches: Optional[frozenset] = None
    review_states: tuple = ()
    promoted_to: Optional[str] = None
    status: DescStatus = DescStatus.COMMITTED
    metadata: dict = field(default_factory=dict)


# ----------------------------------------------------------------------------
# Description queries — the API that is NOT the fold API (D1).
# ----------------------------------------------------------------------------
#
# Fold functions (project_knowledge, project_world, project_reader,
# dramatic_ironies, sternberg_curiosity) do not accept descriptions in any
# signature. These functions live in a separate surface. Callers that want
# to display facts and descriptions side by side compose at the rendering
# layer.


def _resolve_anchor_branches(
    anchor: AnchorRef,
    events: list,
    descriptions: list,
) -> Optional[frozenset]:
    """The branch set of a description's anchor, or None if the anchor is
    an orphan (referent does not exist). Used to compute a description's
    effective branches when the description did not set its own.
    """
    if anchor.kind == "event":
        for e in events:
            if e.id == anchor.target_id:
                return e.branches
        return None
    if anchor.kind == "description":
        for d in descriptions:
            if d.id == anchor.target_id:
                return effective_branches(d, events, descriptions)
        return None
    return None


def effective_branches(
    desc: Description,
    events: list,
    descriptions: list,
) -> frozenset:
    """The branch set this description is visible on.

    If the description carries an explicit `branches` set, that is authoritative
    (subset-override per D4). Otherwise it inherits from the anchor. An orphan
    description (anchor id missing) resolves to the empty set, which means no
    branch sees it; this is a bug signal, not a feature.
    """
    if desc.branches is not None:
        return desc.branches
    anchor_branches = _resolve_anchor_branches(desc.attached_to, events, descriptions)
    if anchor_branches is None:
        return frozenset()
    return anchor_branches


def descriptions_for(
    anchor: AnchorRef,
    descriptions: list,
) -> list:
    """All descriptions attached to `anchor`, in τ_a order."""
    matches = [d for d in descriptions if d.attached_to == anchor]
    return sorted(matches, key=lambda d: d.τ_a)


def descriptions_on_branch(
    branch: Branch,
    descriptions: list,
    events: list,
    all_branches: dict,
    up_to_τ_a: int,
) -> list:
    """All descriptions visible on `branch` at `up_to_τ_a`, in τ_a order.

    Visibility follows the same inheritance rule as events: a description is
    visible on `branch` if its effective-branches set contains `branch.label`
    or the label of any ancestor. Sibling :contested branches do not inherit
    from each other — the D4 branch semantics mirror the B1 fold-scope rule.
    """
    result = []
    for d in descriptions:
        if d.τ_a > up_to_τ_a:
            continue
        eff = effective_branches(d, events, descriptions)
        if not eff:
            continue
        if branch.label in eff:
            result.append(d)
            continue
        for ancestor in ancestor_chain(branch, all_branches):
            if ancestor.label in eff:
                result.append(d)
                break
    return sorted(result, key=lambda d: d.τ_a)


def by_kind(descriptions: list, kind: str) -> list:
    """All descriptions of a given kind."""
    return [d for d in descriptions if d.kind == kind]


def open_questions(descriptions: list) -> list:
    """All descriptions flagged as questions (is_question=True)."""
    return [d for d in descriptions if d.is_question]


def is_review_stale(entry: ReviewEntry, anchor_current_τ_a: int) -> bool:
    """A review is stale if its recorded anchor_τ_a is older than the
    anchor's current τ_a (i.e., the anchor has been edited since)."""
    return entry.anchor_τ_a < anchor_current_τ_a


def is_effectively_unreviewed(
    desc: Description,
    anchor_current_τ_a: int,
) -> bool:
    """A description is effectively unreviewed if it has no approved/noted
    review whose anchor_τ_a ≥ the anchor's current τ_a. `needs-work` and
    `rejected` verdicts do not count as review for this purpose — they are
    flags, not approvals; a description with only those has been seen and
    marked for action, which is a distinct state from unreviewed.
    """
    for entry in desc.review_states:
        if entry.verdict in (ReviewVerdict.APPROVED, ReviewVerdict.NOTED):
            if entry.anchor_τ_a >= anchor_current_τ_a:
                return False
    return True


def unreviewed(
    descriptions: list,
    anchor_τ_a_by_id: dict,
    attention: Attention = Attention.STRUCTURAL,
) -> list:
    """Descriptions that are effectively unreviewed at the current anchor τ_a,
    filtered to a single attention level (structural by default — the ones
    that block).

    `anchor_τ_a_by_id` maps anchor target_id -> the anchor's current τ_a. The
    caller supplies this; computing it from scratch would couple descriptions
    to the event log in a way the API does not mandate.
    """
    result = []
    for d in descriptions:
        if d.attention != attention:
            continue
        current = anchor_τ_a_by_id.get(d.attached_to.target_id)
        if current is None:
            continue
        if is_effectively_unreviewed(d, current):
            result.append(d)
    return result


# ============================================================================
# Reader-model surface — the view and the ingest path
# (reader-model-sketch-01).
# ============================================================================
#
# The substrate exposes two things the reader-model (human or LLM) needs:
# a typed view of the fabula+descriptions scoped to an invocation, and
# an ingest path for the typed outputs the reader-model produces
# (reviews and promotion proposals).
#
# The substrate does not call the reader-model. Tooling does. The view
# is pure data; ingestion produces new immutable records (descriptions
# are append-only per descriptions-sketch-01) or adds entries to a
# proposal queue (a plain list; persistence is tooling's problem).
#
# This is the first probe (sketch-01's tiny prototype slice). Three
# commitments from the sketch exercise here: R1 (typed I/O — every
# input and output is a dataclass), R2 (facts and descriptions are
# structurally distinct in the view), and R5 (every invocation
# declares its scope — branch, τ_s bound, τ_a bound, attention filter,
# optional anchor scope). R3, R4, R6 are implicit in the surface
# shape and tested by the consumers.
#
# Question-answer ingestion and refusal/malformed record handling are
# deferred to a later probe iteration — neither is exercised by the
# current Rashomon encoding beyond one authorial-uncertainty question,
# and this probe's job is to prove the view + review plumbing without
# overbuilding.


@dataclass(frozen=True)
class ViewEventRecord:
    """An event, as the reader-model sees it. The record's presence in
    the view's `events` list (rather than its `descriptions` list) is
    the fact-vs-description label — there is no merged container the
    reader-model could accidentally read as one when it is the other.
    """
    event: Event


@dataclass(frozen=True)
class ViewDescriptionRecord:
    """A description, as the reader-model sees it, annotated with
    review-state derivatives the reader-model would otherwise have to
    recompute.

    `anchor_in_view` is True if the description's anchor (event or
    other description) is also in the view; False if the anchor is
    outside the view's scope. A description whose anchor is out-of-
    view is still legal (descriptions-sketch-01 requires the anchor
    to resolve *in the story*, not in any particular view), but the
    reader-model should be warned that context is thin.

    `effectively_unreviewed` and `stale_review_ids` are computed at
    the view's τ_a bound, using the anchor's τ_a at that same bound.
    The reader-model does not have to recompute staleness — the view
    did it already.
    """
    description: Description
    anchor_in_view: bool
    effectively_unreviewed: bool
    stale_review_ids: tuple  # tuple[int] — indices into description.review_states


@dataclass(frozen=True)
class ReaderView:
    """The typed view the reader-model consumes. Scope is declared on
    every field; two identical ReaderViews produce identical LLM
    prompts (modulo serialization format), which is reproducibility.
    """
    branch_label: str
    up_to_τ_s: int
    up_to_τ_a: int
    attention_filter: Optional[frozenset]
    anchor_scope: Optional[frozenset]
    events: tuple  # tuple[ViewEventRecord]
    descriptions: tuple  # tuple[ViewDescriptionRecord]
    open_questions: tuple  # tuple[ViewDescriptionRecord] — subset of descriptions


@dataclass(frozen=True)
class PromotionProposal:
    """A reader-model's proposal that a description warrants a fact.
    Lives in the proposal queue; an authorial act is required to
    promote (descriptions-sketch-01 D5). `proposed_fact` is an Event
    or an Effect record constructed but not added to any event log;
    status transitions pending → accepted | declined.
    """
    description_id: str
    proposed_fact: object
    proposer_id: str
    rationale: str
    proposed_at_τ_a: int
    status: str = "pending"


def _anchor_current_τ_a(
    anchor: AnchorRef,
    events: list,
    descriptions: list,
    up_to_τ_a: Optional[int] = None,
) -> Optional[int]:
    """The τ_a of the anchor referenced by `anchor`, or None if the
    anchor does not resolve.

    If `up_to_τ_a` is given, returns the latest τ_a ≤ up_to_τ_a among
    records matching the anchor id — bitemporal retrieval so a
    historical view sees the anchor as it was at invocation time, not
    as it is at present. When a caller supplies `up_to_τ_a`, staleness
    computed against the returned τ_a reflects only edits within the
    invocation's scope.

    None bound means latest-available; used when the caller does not
    care about bitemporal snapshotting.
    """
    best: Optional[int] = None
    if anchor.kind == "event":
        for e in events:
            if e.id != anchor.target_id:
                continue
            if up_to_τ_a is not None and e.τ_a > up_to_τ_a:
                continue
            if best is None or e.τ_a > best:
                best = e.τ_a
        return best
    if anchor.kind == "description":
        for d in descriptions:
            if d.id != anchor.target_id:
                continue
            if up_to_τ_a is not None and d.τ_a > up_to_τ_a:
                continue
            if best is None or d.τ_a > best:
                best = d.τ_a
        return best
    return None


def reader_view(
    branch: Branch,
    events: list,
    descriptions: list,
    all_branches: dict,
    up_to_τ_s: int,
    up_to_τ_a: int,
    attention_filter: Optional[frozenset] = None,
    anchor_scope: Optional[frozenset] = None,
) -> ReaderView:
    """Construct a reader-model view. Deterministic, pure, no side effects.

    Scope rules:
      - Events are included if they are in fold-scope for `branch` (per
        the B1 rule), have τ_s ≤ up_to_τ_s, τ_a ≤ up_to_τ_a, and — if
        `anchor_scope` is set — have an id in that set.
      - Descriptions are included if they are visible on `branch` (per
        the D4 branch-semantics rule), have τ_a ≤ up_to_τ_a, pass the
        attention_filter (if set), and — if `anchor_scope` is set —
        have id in the set OR have an attached_to target id in the set.
        (Anchor-scope on a description looks at both directions: the
        description itself, or its anchor, being in scope.)

    The attention_filter is a frozenset of Attention values; None means
    no filter. The anchor_scope is a frozenset of anchor ids (event or
    description ids); None means no filter.
    """
    scoped_events = [
        e for e in events
        if in_scope(e, branch, all_branches)
        and e.τ_s <= up_to_τ_s
        and e.τ_a <= up_to_τ_a
        and (anchor_scope is None or e.id in anchor_scope)
    ]
    scoped_events.sort(key=lambda e: (e.τ_s, e.τ_a))

    event_ids_in_view = {e.id for e in scoped_events}

    all_desc_on_branch = descriptions_on_branch(
        branch=branch, descriptions=descriptions, events=events,
        all_branches=all_branches, up_to_τ_a=up_to_τ_a,
    )

    def _passes_anchor_scope(d: Description) -> bool:
        if anchor_scope is None:
            return True
        return d.id in anchor_scope or d.attached_to.target_id in anchor_scope

    def _passes_attention(d: Description) -> bool:
        if attention_filter is None:
            return True
        return d.attention in attention_filter

    scoped_descriptions = [
        d for d in all_desc_on_branch
        if _passes_anchor_scope(d) and _passes_attention(d)
    ]
    scoped_descriptions.sort(key=lambda d: d.τ_a)
    # `anchor_in_view` answers "is the anchor also in *this view*?" — not
    # "does the anchor exist in the collection?" — so it uses the scoped
    # description set, not the full input. A structural-only view can
    # legally retain a description whose interpretive-attention anchor
    # was filtered out; that case must surface as anchor_in_view=False.
    desc_ids_in_view = {d.id for d in scoped_descriptions}

    desc_records = []
    for d in scoped_descriptions:
        anchor_id = d.attached_to.target_id
        in_view = (
            (d.attached_to.kind == "event" and anchor_id in event_ids_in_view)
            or (d.attached_to.kind == "description" and anchor_id in desc_ids_in_view)
        )
        anchor_τ_a = _anchor_current_τ_a(
            d.attached_to, events, descriptions, up_to_τ_a=up_to_τ_a,
        )
        if anchor_τ_a is None:
            eff_unreviewed = True
            stale_ids = ()
        else:
            eff_unreviewed = is_effectively_unreviewed(d, anchor_τ_a)
            stale_ids = tuple(
                i for i, entry in enumerate(d.review_states)
                if is_review_stale(entry, anchor_τ_a)
            )
        desc_records.append(ViewDescriptionRecord(
            description=d,
            anchor_in_view=in_view,
            effectively_unreviewed=eff_unreviewed,
            stale_review_ids=stale_ids,
        ))

    event_records = tuple(ViewEventRecord(event=e) for e in scoped_events)
    open_q = tuple(r for r in desc_records if r.description.is_question)

    return ReaderView(
        branch_label=branch.label,
        up_to_τ_s=up_to_τ_s,
        up_to_τ_a=up_to_τ_a,
        attention_filter=attention_filter,
        anchor_scope=anchor_scope,
        events=event_records,
        descriptions=tuple(desc_records),
        open_questions=open_q,
    )


# ----------------------------------------------------------------------------
# Ingest — how reader-model outputs land in the substrate
# ----------------------------------------------------------------------------
#
# The substrate holds descriptions and proposal queues as plain lists.
# Ingesting a review produces a new immutable Description with the
# review appended; the caller is responsible for swapping the old
# record out of its collection (the substrate does not manage the
# collection). Ingesting a proposal appends to a queue (also the
# caller's collection).


def ingest_review(
    description: Description,
    review: ReviewEntry,
) -> Description:
    """Append `review` to the description's review_states tuple.
    Returns a new immutable Description record per descriptions-01's
    record-level invariants (edits append; the record is not mutated).
    The caller replaces the old record in whatever collection holds
    the descriptions.
    """
    new_reviews = description.review_states + (review,)
    return replace(description, review_states=new_reviews)


def ingest_proposal(
    proposal: PromotionProposal,
    queue: list,
) -> list:
    """Append `proposal` to the proposal queue, returning a new list.
    The queue is kept as a list (not a set) because ordering by
    proposed_at_τ_a matters for review presentation.
    """
    return list(queue) + [proposal]
