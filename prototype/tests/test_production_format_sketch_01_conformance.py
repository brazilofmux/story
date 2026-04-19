"""
test_production_format_sketch_01_conformance.py — conformance of
the Python prototype's Description AND Entity records to the
canonical specs in schema/description.json + schema/entity.json.

Specified by design/production-format-sketch-01.md PFS4 (for
Description) and design/production-format-sketch-02.md PEA2 (for
Entity). The test validates every existing encoding's ENTITIES
and DESCRIPTIONS tuples against their schemas; failures either
match a known disposition (documented in the relevant sketch) or
fail loud as new findings needing attention.

The module-name retains "sketch_01" for stability — sketches
01 + 02 share one test surface by design (PEA2 "the sketch-01 +
sketch-02 surfaces are one test surface; no reason to split").

The test is the **first consumer** of the schemas outside Python.
It proves: a JSON Schema validator written in any language can
read these schema files and produce conformance verdicts against
records the Python prototype authored. The Python prototype is
unchanged by this test.

PFS2 discipline applies: the test module reads the Python
prototype (for dump-and-validate) but the **schemas** were
authored from design sketches alone. When a conformance failure
surfaces that a schema's enum doesn't accept a value the Python
emits, the disposition is either "amend the design sketch" or
"Python over-specified" — NOT "expand the schema to fit Python".

Run:
    cd prototype
    .venv/bin/python3 -m tests.test_production_format_sketch_01_conformance
"""

from __future__ import annotations

import dataclasses
import importlib
import json
import pathlib
import sys
import traceback

try:
    import jsonschema
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError as exc:
    raise ImportError(
        "This test requires jsonschema + referencing. Install via "
        "`pip install -r prototype/requirements.txt`."
    ) from exc


# ============================================================================
# Schema loading
# ============================================================================


def _repo_root() -> pathlib.Path:
    """The project's repo root, found by walking up from this test file."""
    here = pathlib.Path(__file__).resolve()
    # tests/ → prototype/ → repo root
    return here.parent.parent.parent


def _load_description_schema() -> dict:
    schema_path = _repo_root() / "schema" / "description.json"
    with open(schema_path) as f:
        return json.load(f)


def _load_entity_schema() -> dict:
    schema_path = _repo_root() / "schema" / "entity.json"
    with open(schema_path) as f:
        return json.load(f)


def _load_prop_schema() -> dict:
    schema_path = _repo_root() / "schema" / "prop.json"
    with open(schema_path) as f:
        return json.load(f)


def _load_event_schema() -> dict:
    schema_path = _repo_root() / "schema" / "event.json"
    with open(schema_path) as f:
        return json.load(f)


def _load_held_schema() -> dict:
    schema_path = _repo_root() / "schema" / "held.json"
    with open(schema_path) as f:
        return json.load(f)


def _load_branch_schema() -> dict:
    schema_path = _repo_root() / "schema" / "branch.json"
    with open(schema_path) as f:
        return json.load(f)


def _load_aristotelian_phase_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "aristotelian" / "phase.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_aristotelian_character_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "aristotelian" / "character.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_aristotelian_mythos_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "aristotelian" / "mythos.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_save_the_cat_character_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "save_the_cat" / "character.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_save_the_cat_strand_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "save_the_cat" / "strand.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_save_the_cat_beat_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "save_the_cat" / "beat.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_save_the_cat_story_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "save_the_cat" / "story.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_lowering_annotation_review_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "lowering" / "annotation_review.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_lowering_observation_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "lowering" / "lowering_observation.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_lowering_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "lowering" / "lowering.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_verification_review_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "verification" / "verification_review.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_verification_structural_advisory_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "verification" / "structural_advisory.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_verification_answer_proposal_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "verification" / "verification_answer_proposal.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _load_verifier_commentary_schema() -> dict:
    schema_path = (
        _repo_root() / "schema" / "verification" / "verifier_commentary.json"
    )
    with open(schema_path) as f:
        return json.load(f)


def _build_schema_registry() -> Registry:
    """Build a referencing Registry mapping canonical $id URIs to the
    loaded schemas. Lets cross-file $refs resolve without fetching —
    schema/event.json $refs schema/prop.json + schema/held.json;
    schema/held.json $refs schema/prop.json; schema/description.json
    $refs schema/prop.json for its PropositionAnchor variant;
    schema/aristotelian/mythos.json $refs its sibling phase.json +
    character.json (production-format-sketch-06 PFS6-X1).

    The four save_the_cat schemas are registered for symmetry and
    $id lookup; none of them carry outbound cross-file $refs
    (production-format-sketch-07 PFS7-X1 — flat-with-id-refs
    topology; the registry is present-but-unused at the Save-the-Cat
    dialect layer).

    The lowering namespace (production-format-sketch-09 PFS9-D8)
    adds three schemas: lowering.json, annotation_review.json,
    lowering_observation.json. lowering.json's inline
    $defs/annotation.review_states uses cross-file $ref to
    annotation_review.json (PFS9-X2) — the registry is load-bearing
    here.

    Pattern introduced by production-format-sketch-03 P3A4; extended
    by production-format-sketch-04 P4A1 for held.json; extended by
    production-format-sketch-06 PFS6-D5 for the aristotelian dialect;
    extended by production-format-sketch-07 PFS7-D6 for the
    save-the-cat dialect; extended by production-format-sketch-09
    PFS9-D8 for the lowering namespace."""
    registry = Registry()
    for schema in (
        _load_prop_schema(), _load_held_schema(),
        _load_event_schema(), _load_description_schema(),
        _load_aristotelian_phase_schema(),
        _load_aristotelian_character_schema(),
        _load_aristotelian_mythos_schema(),
        _load_save_the_cat_beat_schema(),
        _load_save_the_cat_character_schema(),
        _load_save_the_cat_story_schema(),
        _load_save_the_cat_strand_schema(),
        _load_lowering_annotation_review_schema(),
        _load_lowering_observation_schema(),
        _load_lowering_schema(),
        _load_verification_review_schema(),
        _load_verification_structural_advisory_schema(),
        _load_verification_answer_proposal_schema(),
        _load_verifier_commentary_schema(),
    ):
        resource = Resource.from_contents(schema, default_specification=DRAFT202012)
        registry = registry.with_resource(uri=schema["$id"], resource=resource)
    return registry


# ============================================================================
# Known dispositions — discrepancies discovered during implementation
# ============================================================================
#
# No active Description dispositions as of 2026-04-19. Sketch-01's
# two original Description dispositions (`authoring-note` kind,
# `superseded` status) both retired under the descriptions-sketch-01
# §Amendments of 2026-04-19, which added each value to its sketch
# enumeration with structural justification; `schema/description.json`
# was updated to match. The Description corpus validates clean.
#
# Adding a new disposition requires amending production-format-
# sketch-01 §Conformance dispositions first; the test is not the
# right place to silently accept new drift.


# ============================================================================
# Encoding discovery
# ============================================================================


def _discover_encoding_records(attribute_name: str) -> list:
    """Return list of (encoding_module_name, records_list) tuples.
    Discovers encodings under prototype/story_engine/encodings/
    that define `attribute_name` (e.g., "ENTITIES" or
    "DESCRIPTIONS") at module level. Empty lists skip silently —
    an encoding can legally bootstrap with no entries."""
    encodings_dir = (
        _repo_root() / "prototype" / "story_engine" / "encodings"
    )
    out: list = []
    for py_path in sorted(encodings_dir.glob("*.py")):
        name = py_path.stem
        if name.startswith("_"):
            continue
        try:
            module = importlib.import_module(
                f"story_engine.encodings.{name}"
            )
        except Exception:
            continue
        records = getattr(module, attribute_name, None)
        if records is None:
            continue
        if not records:
            continue
        out.append((name, list(records)))
    return out


def _discover_encoding_descriptions() -> list:
    return _discover_encoding_records("DESCRIPTIONS")


def _discover_encoding_entities() -> list:
    return _discover_encoding_records("ENTITIES")


def _discover_encoding_events() -> list:
    """Events live under different attribute names across encodings:
    some use FABULA, some use EVENTS_ALL. Try both, in order."""
    from_fabula = _discover_encoding_records("FABULA")
    seen = {name for name, _ in from_fabula}
    from_events_all = [
        (name, events) for name, events
        in _discover_encoding_records("EVENTS_ALL")
        if name not in seen
    ]
    return from_fabula + from_events_all


def _discover_encoding_branches() -> list:
    """Branches are exported as `ALL_BRANCHES` (a dict mapping label
    → Branch record) by each encoding under
    prototype/story_engine/encodings/. Per production-format-
    sketch-05 PFS5-D2."""
    encodings_dir = (
        _repo_root() / "prototype" / "story_engine" / "encodings"
    )
    out: list = []
    for py_path in sorted(encodings_dir.glob("*.py")):
        name = py_path.stem
        if name.startswith("_"):
            continue
        try:
            module = importlib.import_module(
                f"story_engine.encodings.{name}"
            )
        except Exception:
            continue
        all_branches = getattr(module, "ALL_BRANCHES", None)
        if all_branches is None:
            continue
        if not all_branches:
            continue
        out.append((name, list(all_branches.values())))
    return out


def _discover_encoding_aristotelian_records():
    """Walks encoding modules for Aristotelian records. Returns a
    triple `(mythoi, phases, characters)` — three lists of
    (encoding_name, records). Per production-format-sketch-06
    PFS6-D4.

    Mythoi come from module-level `AR_*` attrs that are either an
    `ArMythos` (Oedipus's `AR_OEDIPUS_MYTHOS`) or a tuple of
    `ArMythos` (Rashomon's `AR_RASHOMON_MYTHOI`). Phases and
    characters are collected by traversing each mythos's `.phases`
    and `.characters` tuples; deduplication is by id within a
    single encoding (same-id records across encodings are a
    corpus-authoring concern, not a discovery concern)."""
    from story_engine.core.aristotelian import ArMythos
    encodings_dir = (
        _repo_root() / "prototype" / "story_engine" / "encodings"
    )
    mythoi_out: list = []
    phases_out: list = []
    chars_out: list = []
    for py_path in sorted(encodings_dir.glob("*.py")):
        name = py_path.stem
        if name.startswith("_"):
            continue
        try:
            module = importlib.import_module(
                f"story_engine.encodings.{name}"
            )
        except Exception:
            continue
        # Dedupe by id — Rashomon exports both singletons
        # (AR_RASHOMON_BANDIT, etc.) and a tuple (AR_RASHOMON_MYTHOI)
        # pointing at the same four mythoi; discovery would see them
        # twice otherwise.
        mythoi_seen: dict = {}
        for attr_name in dir(module):
            if not attr_name.startswith("AR_"):
                continue
            value = getattr(module, attr_name, None)
            if isinstance(value, ArMythos):
                mythoi_seen[value.id] = value
            elif (
                isinstance(value, tuple)
                and value
                and all(isinstance(v, ArMythos) for v in value)
            ):
                for v in value:
                    mythoi_seen[v.id] = v
        mythoi = list(mythoi_seen.values())
        if not mythoi:
            continue
        mythoi_out.append((name, mythoi))

        # Traverse each mythos's phases and characters; dedup by id
        # within the encoding. (Cross-encoding id collisions are
        # tolerable — same-id records across unrelated encodings
        # aren't a shape concern.)
        phases_seen: dict = {}
        chars_seen: dict = {}
        for mythos in mythoi:
            for phase in mythos.phases:
                phases_seen[phase.id] = phase
            for char in mythos.characters:
                chars_seen[char.id] = char
        if phases_seen:
            phases_out.append((name, list(phases_seen.values())))
        if chars_seen:
            chars_out.append((name, list(chars_seen.values())))
    return mythoi_out, phases_out, chars_out


def _discover_encoding_save_the_cat_records():
    """Walks encoding modules for Save-the-Cat records. Returns a
    quadruple `(stories, beats, strands, characters)` — four lists
    of (encoding_name, records). Per production-format-sketch-07
    PFS7-D5.

    Save-the-Cat encodings export a singleton `STORY`, a tuple
    `BEATS`, a tuple `STRANDS`, and a tuple `CHARACTERS` at module
    level. No `STC_*` prefix is used (contrast Aristotelian's
    `AR_*` prefix) — Save-the-Cat encodings are single-Story per
    module so the canonical-names convention suffices.

    Sibling `*_save_the_cat_lowerings.py` and
    `*_save_the_cat_verification.py` modules re-import STORY /
    BEATS / STRANDS from the base encoding for their own work; we
    skip them so the same records don't get validated multiple
    times. The base encoding filename ends exactly with
    `_save_the_cat.py`."""
    from story_engine.core.save_the_cat import (
        StcStory, StcBeat, StcStrand, StcCharacter,
    )
    encodings_dir = (
        _repo_root() / "prototype" / "story_engine" / "encodings"
    )
    stories_out: list = []
    beats_out: list = []
    strands_out: list = []
    chars_out: list = []
    for py_path in sorted(encodings_dir.glob("*_save_the_cat.py")):
        name = py_path.stem
        if name.startswith("_"):
            continue
        try:
            module = importlib.import_module(
                f"story_engine.encodings.{name}"
            )
        except Exception:
            continue
        story = getattr(module, "STORY", None)
        if not isinstance(story, StcStory):
            continue
        stories_out.append((name, [story]))

        beats = getattr(module, "BEATS", ())
        if beats and all(isinstance(b, StcBeat) for b in beats):
            beats_out.append((name, list(beats)))

        strands = getattr(module, "STRANDS", ())
        if strands and all(isinstance(s, StcStrand) for s in strands):
            strands_out.append((name, list(strands)))

        characters = getattr(module, "CHARACTERS", ())
        if characters and all(
            isinstance(c, StcCharacter) for c in characters
        ):
            chars_out.append((name, list(characters)))

    return stories_out, beats_out, strands_out, chars_out


def _discover_encoding_lowerings():
    """Walks encoding modules for Lowering records. Returns a list of
    (encoding_name, lowerings_list) tuples. Per production-format-
    sketch-09 PFS9-D7.

    Lowering encodings export `LOWERINGS` as a module-level tuple in
    files matching `*_lowerings.py` (the canonical naming). Empty
    tuples skip silently (and_then_there_were_none_lowerings.py
    scaffolded with an empty tuple for future population)."""
    from story_engine.core.lowering import Lowering
    encodings_dir = (
        _repo_root() / "prototype" / "story_engine" / "encodings"
    )
    out: list = []
    for py_path in sorted(encodings_dir.glob("*_lowerings.py")):
        name = py_path.stem
        if name.startswith("_"):
            continue
        try:
            module = importlib.import_module(
                f"story_engine.encodings.{name}"
            )
        except Exception:
            continue
        lowerings = getattr(module, "LOWERINGS", None)
        if lowerings is None:
            continue
        if not lowerings:
            continue
        if not all(isinstance(lw, Lowering) for lw in lowerings):
            continue
        out.append((name, list(lowerings)))
    return out


def _discover_encoding_verifier_output():
    """Walks encoding modules matching *_verification.py and calls
    each module's run() function. Classifies each element of the
    returned tuple by isinstance on the four verification record
    types. Returns a quadruple `(reviews, advisories, proposals,
    commentaries)` — each a list of (encoding_name, records)
    tuples. Per production-format-sketch-10 PFS10-D5."""
    from story_engine.core.verification import (
        VerificationReview, StructuralAdvisory,
        VerificationAnswerProposal, VerifierCommentary,
    )
    encodings_dir = (
        _repo_root() / "prototype" / "story_engine" / "encodings"
    )
    reviews_out: list = []
    advisories_out: list = []
    proposals_out: list = []
    commentaries_out: list = []
    for py_path in sorted(encodings_dir.glob("*_verification.py")):
        name = py_path.stem
        if name.startswith("_"):
            continue
        try:
            module = importlib.import_module(
                f"story_engine.encodings.{name}"
            )
        except Exception:
            continue
        run_fn = getattr(module, "run", None)
        if run_fn is None or not callable(run_fn):
            continue
        try:
            result = run_fn()
        except Exception:
            continue
        if result is None:
            continue
        mod_reviews: list = []
        mod_advisories: list = []
        mod_proposals: list = []
        mod_commentaries: list = []
        for item in result:
            if isinstance(item, VerificationReview):
                mod_reviews.append(item)
            elif isinstance(item, StructuralAdvisory):
                mod_advisories.append(item)
            elif isinstance(item, VerificationAnswerProposal):
                mod_proposals.append(item)
            elif isinstance(item, VerifierCommentary):
                mod_commentaries.append(item)
            # unknown-type elements ignored (defensive)
        if mod_reviews:
            reviews_out.append((name, mod_reviews))
        if mod_advisories:
            advisories_out.append((name, mod_advisories))
        if mod_proposals:
            proposals_out.append((name, mod_proposals))
        if mod_commentaries:
            commentaries_out.append((name, mod_commentaries))
    return reviews_out, advisories_out, proposals_out, commentaries_out


# ============================================================================
# Dump: Python Description → schema-conforming JSON dict
# ============================================================================


def _dump_anchor(anchor) -> dict:
    """Map Python's flat AnchorRef(kind, target_id) to the schema's
    tagged-union shape.

    The Python prototype represents all anchor kinds with the same
    (kind, target_id) pair — described in substrate.py's AnchorRef
    docstring as "Effect-anchors, proposition-anchors, and
    sjuzhet-entry-anchors are reachable from this shape without
    field additions — the prototype simply does not resolve them
    yet." The schema uses a discriminated-union per the full
    descriptions-sketch-01 §Required fields vocabulary.

    At dump time: kind='event' → {'kind': 'event', 'event_id': <id>};
    kind='description' → {'kind': 'description', 'description_id':
    <id>}. Other anchor kinds do not appear in the current corpus.
    Future encodings that use effect / proposition / sjuzhet-entry
    anchors will need the schema's richer shape exposed in Python —
    that is a prototype evolution, not a schema change."""
    field_by_kind = {
        "event": "event_id",
        "description": "description_id",
        "effect": "event_id",
        "proposition": "prop",
        "sjuzhet-entry": "sjuzhet_entry_id",
    }
    field = field_by_kind.get(anchor.kind)
    if field is None:
        raise ValueError(
            f"unknown AnchorRef kind {anchor.kind!r} — no mapping "
            f"to schema variant"
        )
    return {"kind": anchor.kind, field: anchor.target_id}


def _dump_review_entry(review) -> dict:
    """Map Python ReviewEntry to the schema's ReviewEntry shape."""
    out = {
        "reviewer_id": review.reviewer_id,
        "reviewed_at_τ_a": review.reviewed_at_τ_a,
        "verdict": (
            review.verdict.value
            if hasattr(review.verdict, "value") else review.verdict
        ),
        "anchor_τ_a": review.anchor_τ_a,
    }
    if review.comment is not None:
        out["comment"] = review.comment
    return out


def _dump_prop(prop) -> dict:
    """Map a Python Prop to a JSON-compatible dict conforming to
    schema/prop.json (per substrate-prop-literal-sketch-01 PL1–PL7).

    Python's Prop has tuple args; JSON has arrays. Items are already
    atomic primitives (string Entity-ids, int/float/bool). PL5
    forbids nested structures; the dump does not defensive-check
    because the Python Prop's frozen dataclass + tuple-of-primitives
    contract already constrains at construction time."""
    return {
        "predicate": prop.predicate,
        "args": list(prop.args),
    }


def _dump_world_effect(effect) -> dict:
    """Map a Python WorldEffect to the schema's WorldEffect shape.
    Adds the 'kind' discriminator (production-format-sketch-03
    PFS3-E5) which the Python class identity carries implicitly."""
    return {
        "kind": "world",
        "prop": _dump_prop(effect.prop),
        "asserts": effect.asserts,
    }


def _dump_held(held) -> dict:
    """Map a Python Held to the schema's Held shape per
    substrate-held-record-sketch-01 SH2 + production-format-
    sketch-04 PFS4-D2. Field-for-field isomorphic to the Python
    dataclass: prop gets recursively dumped; slot/confidence are
    str-subclass Enums whose .value yields the schema's enum string;
    via is already a plain string; provenance is a tuple converted
    to a JSON array."""
    slot_val = (
        held.slot.value if hasattr(held.slot, "value") else held.slot
    )
    confidence_val = (
        held.confidence.value if hasattr(held.confidence, "value")
        else held.confidence
    )
    return {
        "prop": _dump_prop(held.prop),
        "slot": slot_val,
        "confidence": confidence_val,
        "via": held.via,
        "provenance": list(held.provenance),
    }


def _dump_knowledge_effect(effect) -> dict:
    """Map a Python KnowledgeEffect to the schema's KnowledgeEffect
    shape per production-format-sketch-04 PFS4-E-amend-1 + PFS4-D1.

    The schema's post-sketch-04 shape is (kind, holder, held,
    remove?). The Python's (agent_id, held, remove) is
    field-for-field isomorphic under one rename (agent_id → holder)
    and one omission-when-default (remove omitted when False,
    relying on the schema's default: false).

    Sketch-03's two dispositions both retire under this amendment:
    Disposition 1 (shape translation) becomes a trivial rename;
    Disposition 2 (remove polarity) closes — remove is now a
    first-class schema field per substrate-held-record-sketch-01
    SH8."""
    out = {
        "kind": "knowledge",
        "holder": effect.agent_id,
        "held": _dump_held(effect.held),
    }
    if effect.remove:
        out["remove"] = True
    return out


def _dump_effect(effect) -> dict:
    """Dispatch on Python class identity to produce the tagged-union
    shape the schema expects."""
    # Lazy import to avoid a circular: substrate is imported via
    # the encoding modules, which import when discover runs.
    from story_engine.core.substrate import (
        KnowledgeEffect as _KnowledgeEffect,
        WorldEffect as _WorldEffect,
    )
    if isinstance(effect, _WorldEffect):
        return _dump_world_effect(effect)
    if isinstance(effect, _KnowledgeEffect):
        return _dump_knowledge_effect(effect)
    raise ValueError(
        f"unknown effect type {type(effect).__name__!r} — no "
        f"schema shape defined"
    )


def _dump_event(event) -> dict:
    """Map a Python Event to schema/event.json shape. Omits optional
    fields with default values (status='committed', branches=
    {':canonical'}) to keep the dump small and to match the
    description-dump convention (omit defaults).

    Omits `metadata` entirely — sketch-05 §The five required elements
    + §Additionally does not include metadata; Python carries the
    field (sketch-04 era) but 0/102 current-corpus events populate
    it. Per PFS2, the schema does not admit. See
    production-format-sketch-03 §Conformance dispositions."""
    out = {
        "id": event.id,
        "type": event.type,
        "τ_s": event.τ_s,
        "τ_a": event.τ_a,
        "participants": {
            role: (
                list(value) if isinstance(value, (list, tuple))
                else value
            )
            for role, value in event.participants.items()
        },
        "effects": [_dump_effect(eff) for eff in event.effects],
    }
    if event.preconditions:
        out["preconditions"] = [_dump_prop(p) for p in event.preconditions]
    status_val = (
        event.status.value if hasattr(event.status, "value")
        else event.status
    )
    if status_val != "committed":
        out["status"] = status_val
    # Python default is frozenset({':canonical'}). Omit only when
    # exactly that; include when any other branch membership.
    from story_engine.core.substrate import CANONICAL_LABEL
    if event.branches != frozenset({CANONICAL_LABEL}):
        out["branches"] = sorted(event.branches)
    return out


def _dump_entity(entity) -> dict:
    """Map a Python Entity to a JSON-compatible dict conforming
    to schema/entity.json (per substrate-entity-record-sketch-01
    SE1–SE6 + production-format-sketch-02 PFE1–PFE4).

    Trivial: three fields, all strings. No anchor mapping, no
    Enum coercion — the Python Entity already has plain str
    fields per substrate-sketch-05's translatable-Python
    discipline."""
    return {
        "id": entity.id,
        "name": entity.name,
        "kind": entity.kind,
    }


def _dump_description(description) -> dict:
    """Map a Python Description to a JSON-compatible dict
    conforming to the shape the schema expects.

    Frozen dataclass → dict is almost `dataclasses.asdict`, but
    the anchor needs discriminator mapping and Enum-valued fields
    need `.value` extraction. Optional fields with None or empty
    defaults are omitted from the dump — the schema doesn't require
    them and their inclusion would make the dump noisier."""
    out = {
        "id": description.id,
        "attached_to": _dump_anchor(description.attached_to),
        "kind": description.kind,
        "attention": (
            description.attention.value
            if hasattr(description.attention, "value")
            else description.attention
        ),
        "text": description.text,
        "authored_by": description.authored_by,
        "τ_a": description.τ_a,
    }
    # Optional fields: include only when they carry meaning
    if description.is_question:
        out["is_question"] = True
    if description.branches is not None:
        # frozenset → sorted list for determinism
        out["branches"] = sorted(description.branches)
    if description.review_states:
        out["review_states"] = [
            _dump_review_entry(r) for r in description.review_states
        ]
    if description.promoted_to is not None:
        out["promoted_to"] = description.promoted_to
    status_val = (
        description.status.value
        if hasattr(description.status, "value")
        else description.status
    )
    # Skip default-committed; include only when status differs.
    # Rationale: the sketch treats committed as the default; the
    # Python defaults to DescStatus.COMMITTED. Omitting the default
    # keeps the dump small and keeps the status field validated
    # only when it's actually distinguishing.
    if status_val != "committed":
        out["status"] = status_val
    if description.metadata:
        out["metadata"] = dict(description.metadata)
    return out


def _dump_branch(branch) -> dict:
    """Map a Python Branch to a JSON-compatible dict conforming
    to schema/branch.json (per substrate-sketch-04 §Branch
    representation + production-format-sketch-05 PFS5-B1..B6 +
    PFS5-D1).

    Field-for-field isomorphic: label (string pass-through),
    kind (enum `.value` extraction), parent (omitted when None —
    canonical case; included verbatim otherwise). Python's
    Branch dataclass lacks a `metadata` field; the schema admits
    it as optional (PFS5-B6), so the dump simply omits it."""
    out = {
        "label": branch.label,
        "kind": (
            branch.kind.value if hasattr(branch.kind, "value")
            else branch.kind
        ),
    }
    if branch.parent is not None:
        out["parent"] = branch.parent
    return out


def _dump_arphase(phase) -> dict:
    """Map a Python ArPhase to a JSON-compatible dict conforming to
    schema/aristotelian/phase.json (production-format-sketch-06
    PFS6-D2). Field-for-field isomorphic: id / role /
    scope_event_ids pass-through; annotation passes through even
    when empty (no omit-on-default; the Python record's default
    is "" not None — presence is invariant)."""
    return {
        "id": phase.id,
        "role": phase.role,
        "scope_event_ids": list(phase.scope_event_ids),
        "annotation": phase.annotation,
    }


def _dump_archaracter(character) -> dict:
    """Map a Python ArCharacter to a JSON-compatible dict conforming
    to schema/aristotelian/character.json (production-format-
    sketch-06 PFS6-D3). Field-for-field isomorphic: id / name /
    is_tragic_hero always emitted; character_ref_id and
    hamartia_text omitted when None."""
    out = {
        "id": character.id,
        "name": character.name,
        "is_tragic_hero": character.is_tragic_hero,
    }
    if character.character_ref_id is not None:
        out["character_ref_id"] = character.character_ref_id
    if character.hamartia_text is not None:
        out["hamartia_text"] = character.hamartia_text
    return out


def _dump_armythos(mythos) -> dict:
    """Map a Python ArMythos to a JSON-compatible dict conforming to
    schema/aristotelian/mythos.json (production-format-sketch-06
    PFS6-D1). Field-for-field isomorphic with these shapes:

    - Required fields (id / title / action_summary /
      central_event_ids / plot_kind / phases) pass through; phases
      each dumped via _dump_arphase.
    - Optional event-id pointers omitted when None.
    - Three boolean asserts_* fields always emitted (dataclass
      always carries them).
    - unity_of_time_bound / unity_of_place_max_locations /
      aims_at_catharsis always emitted (dataclass defaults; PFS6
      anticipated non-finding 2).
    - characters list; empty list emits as empty array."""
    out = {
        "id": mythos.id,
        "title": mythos.title,
        "action_summary": mythos.action_summary,
        "central_event_ids": list(mythos.central_event_ids),
        "plot_kind": mythos.plot_kind,
        "phases": [_dump_arphase(p) for p in mythos.phases],
        "asserts_unity_of_action": mythos.asserts_unity_of_action,
        "asserts_unity_of_time": mythos.asserts_unity_of_time,
        "asserts_unity_of_place": mythos.asserts_unity_of_place,
        "unity_of_time_bound": mythos.unity_of_time_bound,
        "unity_of_place_max_locations": mythos.unity_of_place_max_locations,
        "aims_at_catharsis": mythos.aims_at_catharsis,
        "characters": [_dump_archaracter(c) for c in mythos.characters],
    }
    if mythos.complication_event_id is not None:
        out["complication_event_id"] = mythos.complication_event_id
    if mythos.denouement_event_id is not None:
        out["denouement_event_id"] = mythos.denouement_event_id
    if mythos.peripeteia_event_id is not None:
        out["peripeteia_event_id"] = mythos.peripeteia_event_id
    if mythos.anagnorisis_event_id is not None:
        out["anagnorisis_event_id"] = mythos.anagnorisis_event_id
    return out


def _dump_stccharacter(character) -> dict:
    """Map a Python StcCharacter to a JSON-compatible dict conforming
    to schema/save_the_cat/character.json (production-format-
    sketch-07 PFS7-D4). Field-for-field isomorphic: id / name
    always emitted; description / authored_by pass through (Python
    default empty string and 'author' respectively; no omit-on-
    default per PFS6-D2's annotation precedent). role_labels tuple
    → list (empty tuple → empty array)."""
    return {
        "id": character.id,
        "name": character.name,
        "description": character.description,
        "role_labels": list(character.role_labels),
        "authored_by": character.authored_by,
    }


def _dump_stcstrand(strand) -> dict:
    """Map a Python StcStrand to schema/save_the_cat/strand.json
    (production-format-sketch-07 PFS7-D3). Field-for-field
    isomorphic: id always; kind dumped as its str-subclass Enum
    value ('a-story' / 'b-story'); description / authored_by pass
    through; focal_character_id omitted when None."""
    kind_val = (
        strand.kind.value if hasattr(strand.kind, "value")
        else strand.kind
    )
    out = {
        "id": strand.id,
        "kind": kind_val,
        "description": strand.description,
        "authored_by": strand.authored_by,
    }
    if strand.focal_character_id is not None:
        out["focal_character_id"] = strand.focal_character_id
    return out


def _dump_strand_advancement(advance) -> dict:
    """Map a Python StrandAdvancement sub-record to the inline
    $defs shape in schema/save_the_cat/beat.json (PFS7-X2 + PFS7-
    BT4)."""
    return {
        "strand_id": advance.strand_id,
        "note": advance.note,
    }


def _dump_stcbeat(beat) -> dict:
    """Map a Python StcBeat to schema/save_the_cat/beat.json
    (production-format-sketch-07 PFS7-D2). Field-for-field
    isomorphic: id / slot / page_actual always; description_of_change
    / authored_by pass through; advances tuple walked via
    _dump_strand_advancement; participant_ids tuple → list."""
    return {
        "id": beat.id,
        "slot": beat.slot,
        "page_actual": beat.page_actual,
        "description_of_change": beat.description_of_change,
        "advances": [_dump_strand_advancement(a) for a in beat.advances],
        "participant_ids": list(beat.participant_ids),
        "authored_by": beat.authored_by,
    }


def _dump_archetype_assignment(assignment) -> dict:
    """Map a Python StcArchetypeAssignment sub-record to the inline
    $defs shape in schema/save_the_cat/story.json (PFS7-X2 + PFS7-
    ST6). archetype always emitted; character_id omitted when
    None; note emitted unconditionally (Python default empty
    string)."""
    out = {
        "archetype": assignment.archetype,
        "note": assignment.note,
    }
    if assignment.character_id is not None:
        out["character_id"] = assignment.character_id
    return out


def _dump_stcstory(story) -> dict:
    """Map a Python StcStory to schema/save_the_cat/story.json
    (production-format-sketch-07 PFS7-D1). Field-for-field
    isomorphic: id / title always; theme_statement / authored_by
    pass through; stc_genre_id omitted when None; beat_ids /
    strand_ids / character_ids tuples → lists;
    archetype_assignments tuple walked via
    _dump_archetype_assignment."""
    out = {
        "id": story.id,
        "title": story.title,
        "theme_statement": story.theme_statement,
        "beat_ids": list(story.beat_ids),
        "strand_ids": list(story.strand_ids),
        "character_ids": list(story.character_ids),
        "archetype_assignments": [
            _dump_archetype_assignment(a)
            for a in story.archetype_assignments
        ],
        "authored_by": story.authored_by,
    }
    if story.stc_genre_id is not None:
        out["stc_genre_id"] = story.stc_genre_id
    return out


def _dump_cross_dialect_ref(ref) -> dict:
    """Map a Python CrossDialectRef sub-record to the inline $defs
    shape in schema/lowering/lowering.json (PFS9-D2 + PFS9-X1).
    Field-for-field: {dialect, record_id}."""
    return {
        "dialect": ref.dialect,
        "record_id": ref.record_id,
    }


def _dump_position_range(pr) -> dict:
    """Map a Python PositionRange sub-record to the inline $defs
    shape (PFS9-D5)."""
    return {
        "coord": pr.coord,
        "min_value": pr.min_value,
        "max_value": pr.max_value,
    }


def _dump_annotation_review(review) -> dict:
    """Map a Python AnnotationReview to
    schema/lowering/annotation_review.json (PFS9-D4). Required
    fields always emit; comment omitted when None."""
    out = {
        "reviewer_id": review.reviewer_id,
        "reviewed_at_τ_a": review.reviewed_at_τ_a,
        "verdict": review.verdict,
        "anchor_τ_a": review.anchor_τ_a,
    }
    if review.comment is not None:
        out["comment"] = review.comment
    return out


def _dump_annotation(annotation) -> dict:
    """Map a Python Annotation sub-record to the inline $defs shape
    in schema/lowering/lowering.json (PFS9-D3 + PFS9-X1). text
    always emitted (required by schema); attention / authored_by
    unconditional (Python defaults — empty emission would drop
    presence-signals the PFS2 discipline wants preserved);
    review_states walked via _dump_annotation_review."""
    return {
        "text": annotation.text,
        "attention": annotation.attention,
        "authored_by": annotation.authored_by,
        "review_states": [
            _dump_annotation_review(r) for r in annotation.review_states
        ],
    }


def _dump_lowering(lowering) -> dict:
    """Map a Python Lowering to schema/lowering/lowering.json
    (PFS9-D1). Required fields (id, upper_record, lower_records,
    annotation, status) always emit. authored_by, τ_a always emit
    (Python defaults). position_range omitted when None. anchor_τ_a
    omitted when None. metadata omitted when empty dict.

    status dumps as the enum string value ('active' or 'pending')."""
    status_val = (
        lowering.status.value if hasattr(lowering.status, "value")
        else lowering.status
    )
    out = {
        "id": lowering.id,
        "upper_record": _dump_cross_dialect_ref(lowering.upper_record),
        "lower_records": [
            _dump_cross_dialect_ref(lr) for lr in lowering.lower_records
        ],
        "annotation": _dump_annotation(lowering.annotation),
        "authored_by": lowering.authored_by,
        "τ_a": lowering.τ_a,
        "status": status_val,
    }
    if lowering.position_range is not None:
        out["position_range"] = _dump_position_range(
            lowering.position_range
        )
    if lowering.anchor_τ_a is not None:
        out["anchor_τ_a"] = lowering.anchor_τ_a
    if lowering.metadata:
        out["metadata"] = dict(lowering.metadata)
    return out


def _dump_lowering_observation(obs) -> dict:
    """Map a Python LoweringObservation to schema/lowering/
    lowering_observation.json (PFS9-D6). All four fields required
    and always emitted."""
    return {
        "severity": obs.severity,
        "code": obs.code,
        "target_id": obs.target_id,
        "message": obs.message,
    }


def _dump_verification_review(review) -> dict:
    """Map a Python VerificationReview to
    schema/verification/verification_review.json (PFS10-D1).
    Required fields always emit; target_record rendered via
    shared _dump_cross_dialect_ref (PFS9-D2); comment and
    match_strength omitted when None."""
    out = {
        "reviewer_id": review.reviewer_id,
        "reviewed_at_τ_a": review.reviewed_at_τ_a,
        "verdict": review.verdict,
        "anchor_τ_a": review.anchor_τ_a,
        "target_record": _dump_cross_dialect_ref(review.target_record),
    }
    if review.comment is not None:
        out["comment"] = review.comment
    if review.match_strength is not None:
        out["match_strength"] = review.match_strength
    return out


def _dump_structural_advisory(advisory) -> dict:
    """Map a Python StructuralAdvisory to
    schema/verification/structural_advisory.json (PFS10-D2).
    Required fields always emit; scope walked via
    _dump_cross_dialect_ref; match_strength omitted when None."""
    out = {
        "advisor_id": advisory.advisor_id,
        "advised_at_τ_a": advisory.advised_at_τ_a,
        "severity": advisory.severity,
        "comment": advisory.comment,
        "scope": [
            _dump_cross_dialect_ref(ref) for ref in advisory.scope
        ],
    }
    if advisory.match_strength is not None:
        out["match_strength"] = advisory.match_strength
    return out


def _dump_verification_answer_proposal(proposal) -> dict:
    """Map a Python VerificationAnswerProposal to
    schema/verification/verification_answer_proposal.json
    (PFS10-D3). All six fields always emit (including status
    with Python default 'pending'). question_id rendered via
    _dump_cross_dialect_ref."""
    return {
        "proposer_id": proposal.proposer_id,
        "question_id": _dump_cross_dialect_ref(proposal.question_id),
        "proposed_text": proposal.proposed_text,
        "rationale": proposal.rationale,
        "proposed_at_τ_a": proposal.proposed_at_τ_a,
        "status": proposal.status,
    }


def _dump_verifier_commentary(commentary) -> dict:
    """Map a Python VerifierCommentary to
    schema/verification/verifier_commentary.json (PFS10-D4).
    Required fields always emit; target_review rendered via
    _dump_verification_review (full nested shape, matching the
    Python's by-value carrying). suggested_signature omitted
    when None."""
    out = {
        "commenter_id": commentary.commenter_id,
        "commented_at_τ_a": commentary.commented_at_τ_a,
        "assessment": commentary.assessment,
        "target_review": _dump_verification_review(
            commentary.target_review
        ),
        "comment": commentary.comment,
    }
    if commentary.suggested_signature is not None:
        out["suggested_signature"] = commentary.suggested_signature
    return out


# ============================================================================
# Tests
# ============================================================================


def test_description_schema_metaschema_valid():
    """schema/description.json is a valid JSON Schema 2020-12
    document."""
    schema = _load_description_schema()
    Draft202012Validator.check_schema(schema)


def test_entity_schema_metaschema_valid():
    """schema/entity.json is a valid JSON Schema 2020-12 document."""
    schema = _load_entity_schema()
    Draft202012Validator.check_schema(schema)


def test_prop_schema_metaschema_valid():
    """schema/prop.json is a valid JSON Schema 2020-12 document."""
    schema = _load_prop_schema()
    Draft202012Validator.check_schema(schema)


def test_event_schema_metaschema_valid():
    """schema/event.json is a valid JSON Schema 2020-12 document."""
    schema = _load_event_schema()
    Draft202012Validator.check_schema(schema)


def test_held_schema_metaschema_valid():
    """schema/held.json is a valid JSON Schema 2020-12 document
    (production-format-sketch-04 P4A1)."""
    schema = _load_held_schema()
    Draft202012Validator.check_schema(schema)


def test_branch_schema_metaschema_valid():
    """schema/branch.json is a valid JSON Schema 2020-12 document
    (production-format-sketch-05 PFS5-B1)."""
    schema = _load_branch_schema()
    Draft202012Validator.check_schema(schema)


def test_aristotelian_phase_schema_metaschema_valid():
    """schema/aristotelian/phase.json is a valid JSON Schema 2020-12
    document (production-format-sketch-06 PFS6-P1..P5)."""
    schema = _load_aristotelian_phase_schema()
    Draft202012Validator.check_schema(schema)


def test_aristotelian_character_schema_metaschema_valid():
    """schema/aristotelian/character.json is a valid JSON Schema
    2020-12 document (production-format-sketch-06 PFS6-C1..C5)."""
    schema = _load_aristotelian_character_schema()
    Draft202012Validator.check_schema(schema)


def test_aristotelian_mythos_schema_metaschema_valid():
    """schema/aristotelian/mythos.json is a valid JSON Schema
    2020-12 document (production-format-sketch-06 PFS6-M1..M11)."""
    schema = _load_aristotelian_mythos_schema()
    Draft202012Validator.check_schema(schema)


def test_cross_file_registry_resolves_prop_ref():
    """The referencing Registry resolves event.json's Prop $ref to
    schema/prop.json. Guards against build-environment breakage
    where validators can't follow the canonical $id URIs."""
    registry = _build_schema_registry()
    event_schema = _load_event_schema()
    validator = Draft202012Validator(event_schema, registry=registry)
    # An Event whose preconditions use Prop exercises the cross-file
    # ref path.
    dummy_event = {
        "id": "E_test", "type": "test",
        "τ_s": 0, "τ_a": 0,
        "participants": {},
        "effects": [],
        "preconditions": [
            {"predicate": "test_pred", "args": ["a", "b"]}
        ],
    }
    errors = list(validator.iter_errors(dummy_event))
    assert errors == [], (
        f"expected zero validation errors on the dummy event; "
        f"got: {[e.message for e in errors]}"
    )


def test_description_schema_has_expected_shape():
    """Spot-check of Description schema structure — guards
    against accidental breakage of the schema during unrelated
    edits."""
    schema = _load_description_schema()
    assert schema["$schema"] == (
        "https://json-schema.org/draft/2020-12/schema"
    )
    assert schema["title"] == "Description"
    required = set(schema["required"])
    assert required == {
        "id", "attached_to", "kind", "attention", "text",
        "authored_by", "τ_a",
    }
    assert schema["additionalProperties"] is False
    # Anchor variants
    anchor_variants = schema["properties"]["attached_to"]["oneOf"]
    variant_titles = sorted(v["title"] for v in anchor_variants)
    assert variant_titles == [
        "DescriptionAnchor", "EffectLocatorAnchor", "EventAnchor",
        "PropositionAnchor", "SjuzhetEntryAnchor",
    ]
    # Kind enum matches descriptions-sketch-01 §Kinds (the six
    # starting kinds plus `authoring-note` added 2026-04-19 under
    # §Amendments Addition 1).
    kind_enum = set(schema["properties"]["kind"]["enum"])
    assert kind_enum == {
        "texture", "motivation", "reader-frame",
        "authorial-uncertainty", "trust-flag", "provenance",
        "authoring-note",
    }
    # Status enum matches descriptions-sketch-01 §Optional fields
    # (original pair plus `superseded` added 2026-04-19 under
    # §Amendments Addition 2 — the edit-chain marker).
    status_enum = set(schema["properties"]["status"]["enum"])
    assert status_enum == {"committed", "provisional", "superseded"}


def test_prop_schema_has_expected_shape():
    """Spot-check of Prop schema structure per
    substrate-prop-literal-sketch-01 PL1–PL7 +
    production-format-sketch-03 PFS3-P1/P2/P3."""
    schema = _load_prop_schema()
    assert schema["title"] == "Prop"
    assert set(schema["required"]) == {"predicate", "args"}
    assert schema["additionalProperties"] is False
    # args items are anyOf over atomic primitives (PL4). Note:
    # anyOf not oneOf — integers validate against both 'integer'
    # and 'number', so oneOf would always fail on integer args.
    item_any_of = schema["properties"]["args"]["items"]["anyOf"]
    item_types = sorted(variant["type"] for variant in item_any_of)
    assert item_types == ["boolean", "integer", "number", "string"]
    # predicate has minLength 1 (non-empty per PL2)
    assert schema["properties"]["predicate"]["minLength"] == 1


def test_event_schema_has_expected_shape():
    """Spot-check of Event schema structure per
    substrate-sketch-05 §Event internals +
    production-format-sketch-03 PFS3-E1 through E7 +
    production-format-sketch-04 PFS4-E-amend-1 through E-amend-4
    (KnowledgeEffect shape revision)."""
    schema = _load_event_schema()
    assert schema["title"] == "Event"
    assert set(schema["required"]) == {
        "id", "type", "τ_s", "τ_a", "participants", "effects",
    }
    assert schema["additionalProperties"] is False
    # Three optional fields admitted
    all_props = set(schema["properties"].keys())
    optional = all_props - set(schema["required"])
    assert optional == {"preconditions", "status", "branches"}
    # Explicit exclusions per PFS3-E7
    assert "metadata" not in all_props
    assert "descriptions" not in all_props
    # Effects $defs: WorldEffect + KnowledgeEffect with kind
    # discriminators (PFS3-E5)
    defs = schema["$defs"]
    assert set(defs.keys()) == {"WorldEffect", "KnowledgeEffect"}
    assert defs["WorldEffect"]["properties"]["kind"] == {
        "const": "world"
    }
    # KnowledgeEffect post-sketch-04 shape: (kind, holder, held,
    # remove?). prop + via moved into the nested Held.
    ke_def = defs["KnowledgeEffect"]
    assert ke_def["properties"]["kind"] == {"const": "knowledge"}
    assert set(ke_def["required"]) == {"kind", "holder", "held"}
    assert set(ke_def["properties"].keys()) == {
        "kind", "holder", "held", "remove",
    }
    assert ke_def["properties"]["remove"]["type"] == "boolean"
    assert ke_def["properties"]["remove"]["default"] is False
    # held field $refs schema/held.json (PFS4-E-amend-1)
    assert ke_def["properties"]["held"]["$ref"] == (
        "https://brazilofmux.github.io/story/schema/held.json"
    )


def test_held_schema_has_expected_shape():
    """Spot-check of Held schema structure per
    substrate-held-record-sketch-01 SH1-SH7 +
    production-format-sketch-04 PFS4-H1 through H7."""
    schema = _load_held_schema()
    assert schema["title"] == "Held"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/held.json"
    )
    assert set(schema["required"]) == {
        "prop", "slot", "confidence", "via", "provenance",
    }
    assert schema["additionalProperties"] is False
    # prop $refs prop.json
    assert schema["properties"]["prop"]["$ref"] == (
        "https://brazilofmux.github.io/story/schema/prop.json"
    )
    # Slot closed enum — SH3
    assert set(schema["properties"]["slot"]["enum"]) == {
        "known", "believed", "suspected", "gap",
    }
    # Confidence closed enum — SH4
    assert set(schema["properties"]["confidence"]["enum"]) == {
        "certain", "believed", "suspected", "open",
    }
    # Via closed enum — 11 values (6 diegetic + 5 narrative) per
    # substrate-effect-shape-sketch-01 ES4, re-homed to Held by
    # the ES3-amendment
    assert set(schema["properties"]["via"]["enum"]) == {
        "observation", "utterance-heard", "inference",
        "deception", "forgetting", "realization",
        "disclosure", "focalization", "omission",
        "framing", "retroactive-reframing",
    }
    # provenance is array of strings, admits empty
    prov = schema["properties"]["provenance"]
    assert prov["type"] == "array"
    assert prov["items"] == {"type": "string"}


def test_held_corpus_conformance():
    """Every Held nested inside a corpus KnowledgeEffect validates
    against schema/held.json. Direct per-Held validation, parallel
    to the per-Entity conformance test but for the fold-output /
    effect-input record shape (production-format-sketch-04 P4A3)."""
    held_schema = _load_held_schema()
    registry = _build_schema_registry()
    validator = Draft202012Validator(held_schema, registry=registry)

    from story_engine.core.substrate import KnowledgeEffect

    seen_event_ids = set()
    total = 0
    clean_passes = 0
    new_findings: list = []

    encodings = _discover_encoding_events()
    assert encodings, (
        "expected at least one encoding with events; found none"
    )

    for encoding_name, events in encodings:
        for event in events:
            # Re-export inflation dedup (match the Entity / Event
            # pattern — the same event appears in multiple modules
            # via FABULA re-exports; count each unique event once).
            if event.id in seen_event_ids:
                continue
            seen_event_ids.add(event.id)
            for eff in event.effects:
                if not isinstance(eff, KnowledgeEffect):
                    continue
                total += 1
                dumped = _dump_held(eff.held)
                errors = list(validator.iter_errors(dumped))
                if not errors:
                    clean_passes += 1
                    continue
                new_findings.append({
                    "encoding": encoding_name,
                    "event_id": event.id,
                    "prop": eff.held.prop,
                    "errors": [
                        {
                            "path": list(e.absolute_path),
                            "validator": e.validator,
                            "message": e.message,
                        }
                        for e in errors
                    ],
                })

    print()
    print(
        f"test_held_corpus_conformance: {total} Held records "
        f"(unique KnowledgeEffects deduped by event id)"
    )
    print(f"  clean passes:               {clean_passes}")
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings[:10]:
            print(f"    {finding['encoding']}: {finding['event_id']}")
            print(f"      prop={finding['prop']}")
            for err in finding["errors"][:3]:
                print(f"      - path={err['path']} "
                      f"validator={err['validator']}: {err['message']}")
        if len(new_findings) > 10:
            print(f"    ... and {len(new_findings) - 10} more")

    assert not new_findings, (
        f"{len(new_findings)} Held conformance finding(s); see "
        f"output. Resolve per production-format-sketch-04's "
        f"§Conformance dispositions protocol."
    )
    assert total > 0


def test_branch_schema_has_expected_shape():
    """Spot-check of Branch schema structure per substrate-
    sketch-04 §Branch representation + production-format-
    sketch-05 PFS5-B1 through PFS5-B6."""
    schema = _load_branch_schema()
    assert schema["title"] == "Branch"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/branch.json"
    )
    # Two required fields unconditionally (PFS5-B1)
    assert set(schema["required"]) == {"label", "kind"}
    # Strict shape (PFS5-B2)
    assert schema["additionalProperties"] is False
    # All four declared properties (PFS5-B3..B6)
    assert set(schema["properties"].keys()) == {
        "label", "kind", "parent", "metadata",
    }
    # label is non-empty string (PFS5-B3)
    label = schema["properties"]["label"]
    assert label["type"] == "string"
    assert label["minLength"] == 1
    # kind closed enum at four values (PFS5-B4)
    assert set(schema["properties"]["kind"]["enum"]) == {
        "canonical", "contested", "draft", "counterfactual",
    }
    # parent is a non-empty string when present (PFS5-B5)
    parent = schema["properties"]["parent"]
    assert parent["type"] == "string"
    assert parent["minLength"] == 1
    # metadata is open object when present (PFS5-B6)
    assert schema["properties"]["metadata"]["type"] == "object"
    # Parent conditional via allOf/if-then-else (PFS5-B5)
    all_of = schema.get("allOf", [])
    assert len(all_of) == 1
    clause = all_of[0]
    assert clause["if"]["properties"]["kind"]["const"] == "canonical"
    assert clause["then"] == {"not": {"required": ["parent"]}}
    assert clause["else"] == {"required": ["parent"]}


def test_branch_corpus_conformance():
    """Every Branch across every encoding's ALL_BRANCHES validates
    against schema/branch.json. Parallel to the Entity / Held /
    Description corpus tests (production-format-sketch-05 PFS5-D2).

    Current corpus is heavily canonical-biased: 7 encodings ship
    `ALL_BRANCHES = {CANONICAL_LABEL: CANONICAL}`; Rashomon
    additionally ships 4 CONTESTED branches. No DRAFT and no
    COUNTERFACTUAL records — those two kinds are admitted by the
    schema (PFS5-B4) but unexercised in the substrate-layer
    corpus, per §Conformance dispositions Disposition 2 (non-
    finding)."""
    schema = _load_branch_schema()
    validator = Draft202012Validator(schema)

    encodings = _discover_encoding_branches()
    assert encodings, (
        "expected at least one encoding with ALL_BRANCHES; found none"
    )

    total = 0
    clean_passes = 0
    kind_counts: dict = {}  # kind string → count
    new_findings: list = []

    for encoding_name, branches in encodings:
        for branch in branches:
            total += 1
            dumped = _dump_branch(branch)
            kind_counts[dumped["kind"]] = (
                kind_counts.get(dumped["kind"], 0) + 1
            )
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "branch_label": branch.label,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(f"test_branch_corpus_conformance: {total} Branch records")
    print(f"  clean passes:               {clean_passes}")
    print(f"  by kind:                    {dict(sorted(kind_counts.items()))}")
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(f"    {finding['encoding']}: {finding['branch_label']}")
            for err in finding["errors"]:
                print(f"      - path={err['path']} "
                      f"validator={err['validator']}: {err['message']}")

    assert not new_findings, (
        f"{len(new_findings)} Branch conformance finding(s); see "
        f"output. Resolve per production-format-sketch-05's "
        f"§Conformance dispositions protocol."
    )
    assert total > 0


def test_description_schema_references_prop_by_url():
    """After production-format-sketch-03 PFS3-D1, description.json's
    PropositionAnchor variant $refs schema/prop.json instead of
    the PropPlaceholder honest-gap marker. Guards against
    regression of the PropPlaceholder resolution."""
    schema = _load_description_schema()
    # PropPlaceholder entry removed from $defs
    assert "PropPlaceholder" not in schema.get("$defs", {})
    # PropositionAnchor variant $refs prop.json
    prop_anchor = None
    for variant in schema["properties"]["attached_to"]["oneOf"]:
        if variant.get("title") == "PropositionAnchor":
            prop_anchor = variant
            break
    assert prop_anchor is not None
    assert prop_anchor["properties"]["prop"] == {
        "$ref": "https://brazilofmux.github.io/story/schema/prop.json"
    }


def test_entity_schema_has_expected_shape():
    """Spot-check of Entity schema structure per
    substrate-entity-record-sketch-01 SE1–SE6 +
    production-format-sketch-02 PFE1–PFE4."""
    schema = _load_entity_schema()
    assert schema["$schema"] == (
        "https://json-schema.org/draft/2020-12/schema"
    )
    assert schema["title"] == "Entity"
    assert set(schema["required"]) == {"id", "name", "kind"}
    assert schema["additionalProperties"] is False
    # Three fields only (SE2; PFE2)
    assert set(schema["properties"].keys()) == {"id", "name", "kind"}
    # Closed kind enum (SE3; PFE3)
    kind_enum = set(schema["properties"]["kind"]["enum"])
    assert kind_enum == {"agent", "object", "location", "abstract"}
    # No τ_a (SE5; PFE4) — record is timeless
    assert "τ_a" not in schema["properties"]


def test_corpus_conformance():
    """Every Description across every encoding validates against
    the schema. Dispositions 1 and 2 (authoring-note kind,
    superseded status) retired 2026-04-19 under descriptions-
    sketch-01 §Amendments; the corpus is clean on both axes.
    Any schema-validation failure is a new finding and fails
    the test loudly with the record id + error location."""
    schema = _load_description_schema()
    validator = Draft202012Validator(schema)

    encodings = _discover_encoding_descriptions()
    assert encodings, (
        "expected at least one encoding with DESCRIPTIONS; found none"
    )

    total = 0
    clean_passes = 0
    new_findings: list = []

    for encoding_name, descriptions in encodings:
        for description in descriptions:
            total += 1
            dumped = _dump_description(description)
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: e.absolute_path,
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "description_id": description.id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    # Report
    print(f"  total descriptions validated: {total}")
    print(f"  clean passes:               {clean_passes}")
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(f"    {finding['encoding']}: {finding['description_id']}")
            for err in finding["errors"]:
                print(f"      - path={err['path']} "
                      f"validator={err['validator']}: {err['message']}")

    assert not new_findings, (
        f"{len(new_findings)} new Description conformance finding(s); "
        f"see output. Resolve per production-format-sketch-01's "
        f"§Conformance dispositions protocol."
    )
    # Sanity: expect >0 total — silent-skip everything would mean
    # encoding discovery broke.
    assert total > 0


def test_event_corpus_conformance():
    """Every Event across every encoding validates against
    schema/event.json (with cross-file $ref to schema/prop.json
    resolved via the registry). Expected: all pass cleanly after
    the dump-layer handles the KnowledgeEffect shape translation
    (Python's held.prop/held.via → schema's prop/via) and effect
    kind discriminator addition.

    Python over-specifications documented in the sketch's
    §Conformance dispositions (not tested here): metadata field,
    KnowledgeEffect.held richer shape, KnowledgeEffect.remove
    retraction polarity (see test_knowledge_effect_remove_audit)."""
    registry = _build_schema_registry()
    event_schema = _load_event_schema()
    validator = Draft202012Validator(event_schema, registry=registry)

    encodings = _discover_encoding_events()
    assert encodings, (
        "expected at least one encoding with FABULA or EVENTS_ALL; "
        "found none"
    )

    total = 0
    clean_passes = 0
    new_findings: list = []

    for encoding_name, events in encodings:
        for event in events:
            total += 1
            try:
                dumped = _dump_event(event)
            except Exception as exc:
                new_findings.append({
                    "encoding": encoding_name,
                    "event_id": getattr(event, "id", "<unknown>"),
                    "errors": [{
                        "path": [],
                        "validator": "dump-failed",
                        "message": str(exc),
                    }],
                })
                continue
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "event_id": event.id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print(f"  total events validated:     {total}")
    print(f"  clean passes:               {clean_passes}")
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings[:10]:
            print(f"    {finding['encoding']}: {finding['event_id']}")
            for err in finding["errors"][:3]:
                print(f"      - path={err['path']} "
                      f"validator={err['validator']}: {err['message']}")
        if len(new_findings) > 10:
            print(f"    ... and {len(new_findings) - 10} more")

    assert not new_findings, (
        f"{len(new_findings)} Event conformance finding(s); see "
        f"output. Resolve per production-format-sketch-03's "
        f"§Conformance dispositions protocol."
    )
    assert total > 0


def test_knowledge_effect_remove_audit():
    """Operational audit: count KnowledgeEffects with remove=True
    across the corpus.

    Per substrate-held-record-sketch-01 SH8 + production-format-
    sketch-04 PFS4-E-amend-2, the `remove` polarity is a
    legitimate first-class KnowledgeEffect field supporting
    factual dislodgement (the messenger's reveal dislodging
    Oedipus's BELIEVED `child_of(oedipus, polybus)`; Jocasta's
    realization dislodging her BELIEVED `dead(the-exposed-baby)`;
    the anagnorisis closing Oedipus's GAP for his parentage).
    identity-and-realization-sketch-01 §Sternberg-stays-literal
    already endorsed the pattern.

    The count at 2026-04-19 is 7 (Oedipus 3 + Macbeth 2 + Ackroyd
    2 equivalent by deduped event-id). This is the **intended
    baseline, not a drift-to-zero cleanup target**. The audit
    remains for operational visibility — a significant jump from
    7 (to 40+) is worth noticing as either:

    - a new encoding author adopting the dislodgement idiom
      appropriately (likely fine; the pattern generalizes), or
    - a regression toward realization-removes-propositions
      (which identity-and-realization-sketch-01 explicitly
      retired in favor of identity assertions + query-time
      substitution).

    State-of-play-06 framed this test as "drives the count to 0".
    That framing was incorrect; state-of-play-07 rewrites it."""
    from story_engine.core.substrate import KnowledgeEffect
    seen_event_ids = set()
    remove_true_count = 0
    encodings = _discover_encoding_events()
    for encoding_name, events in encodings:
        for event in events:
            # Re-export inflation: the same event objects appear in
            # multiple modules (FABULA + lowerings re-exports); count
            # each event once by id to report the corpus-level figure.
            if event.id in seen_event_ids:
                continue
            seen_event_ids.add(event.id)
            for eff in event.effects:
                if (isinstance(eff, KnowledgeEffect)
                        and getattr(eff, "remove", False)):
                    remove_true_count += 1
    print(
        f"  KnowledgeEffect.remove=True count (deduped by event id):"
        f" {remove_true_count} (baseline: 7 at 2026-04-19; drift "
        f"from baseline = finding)"
    )
    # Informational; no assertion on count. The baseline is
    # documented in the sketch.


def test_entity_corpus_conformance():
    """Every Entity across every encoding validates against
    schema/entity.json. No dispositions anticipated (see
    production-format-sketch-02 §Conformance dispositions); any
    failure is a new finding that requires an amendment before
    this test can pass."""
    schema = _load_entity_schema()
    validator = Draft202012Validator(schema)

    encodings = _discover_encoding_entities()
    assert encodings, (
        "expected at least one encoding with ENTITIES; found none"
    )

    total = 0
    clean_passes = 0
    new_findings: list = []

    for encoding_name, entities in encodings:
        for entity in entities:
            total += 1
            dumped = _dump_entity(entity)
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: e.absolute_path,
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "entity_id": entity.id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print(f"  total entities validated:   {total}")
    print(f"  clean passes:               {clean_passes}")
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(f"    {finding['encoding']}: {finding['entity_id']}")
            for err in finding["errors"]:
                print(f"      - path={err['path']} "
                      f"validator={err['validator']}: {err['message']}")

    assert not new_findings, (
        f"{len(new_findings)} Entity conformance finding(s); see "
        f"output. Resolve per production-format-sketch-02's "
        f"§Conformance dispositions protocol (amend the sketch; "
        f"never silently widen the schema)."
    )
    assert total > 0


def test_anchor_dump_is_tagged_union():
    """The dump function maps Python's flat AnchorRef to the
    tagged-union shape the schema expects."""
    from story_engine.core.substrate import anchor_event, anchor_desc
    dumped_event = _dump_anchor(anchor_event("E_test"))
    assert dumped_event == {"kind": "event", "event_id": "E_test"}
    dumped_desc = _dump_anchor(anchor_desc("D_test"))
    assert dumped_desc == {
        "kind": "description", "description_id": "D_test",
    }


def test_anchor_dump_rejects_unknown_kind():
    """An anchor with an unrecognized kind fails the dump loudly
    — better than silently producing a schema-invalid record."""
    from story_engine.core.substrate import AnchorRef
    bogus = AnchorRef(kind="galaxy", target_id="milky-way")
    try:
        _dump_anchor(bogus)
    except ValueError as e:
        assert "galaxy" in str(e)
    else:
        assert False, "expected ValueError on unknown anchor kind"


def test_review_entry_dump_omits_none_comment():
    """An omitted comment shouldn't produce a `comment: null` field
    in the dump — schema's comment is optional, and null isn't a
    string."""
    from story_engine.core.substrate import ReviewEntry, ReviewVerdict
    entry = ReviewEntry(
        reviewer_id="llm:test", reviewed_at_τ_a=10,
        verdict=ReviewVerdict.APPROVED, anchor_τ_a=5,
    )
    dumped = _dump_review_entry(entry)
    assert "comment" not in dumped
    assert dumped["verdict"] == "approved"


def test_entity_sketches_exist():
    """Meta-test: the design sketches the Entity schema derives
    from exist in design/. Guards against schema-without-sketch
    drift (the inverse of the Python-as-spec drift PFS2 inverts)."""
    root = _repo_root() / "design"
    assert (root / "substrate-entity-record-sketch-01.md").exists(), (
        "schema/entity.json exists but its design-layer spec "
        "(substrate-entity-record-sketch-01.md) is missing"
    )
    assert (root / "production-format-sketch-02.md").exists(), (
        "schema/entity.json exists but its production-layer "
        "spec (production-format-sketch-02.md) is missing"
    )


def test_aristotelian_phase_schema_has_expected_shape():
    """Spot-check of ArPhase schema structure per aristotelian-
    sketch-01 A2 + production-format-sketch-06 PFS6-P1..P5."""
    schema = _load_aristotelian_phase_schema()
    assert schema["title"] == "ArPhase"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "aristotelian/phase.json"
    )
    assert set(schema["required"]) == {
        "id", "role", "scope_event_ids",
    }
    assert schema["additionalProperties"] is False
    assert set(schema["properties"].keys()) == {
        "id", "role", "scope_event_ids", "annotation",
    }
    # role closed enum at the three Aristotelian phases
    assert set(schema["properties"]["role"]["enum"]) == {
        "beginning", "middle", "end",
    }
    # scope_event_ids is array of non-empty strings
    scope = schema["properties"]["scope_event_ids"]
    assert scope["type"] == "array"
    assert scope["items"]["type"] == "string"
    assert scope["items"]["minLength"] == 1


def test_aristotelian_character_schema_has_expected_shape():
    """Spot-check of ArCharacter schema structure per aristotelian-
    sketch-01 A5 + production-format-sketch-06 PFS6-C1..C5."""
    schema = _load_aristotelian_character_schema()
    assert schema["title"] == "ArCharacter"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "aristotelian/character.json"
    )
    assert set(schema["required"]) == {"id", "name"}
    assert schema["additionalProperties"] is False
    assert set(schema["properties"].keys()) == {
        "id", "name", "character_ref_id",
        "hamartia_text", "is_tragic_hero",
    }
    # character_ref_id optional non-empty string (PFS6-C3)
    ref = schema["properties"]["character_ref_id"]
    assert ref["type"] == "string"
    assert ref["minLength"] == 1
    # is_tragic_hero optional boolean (PFS6-C5)
    assert (
        schema["properties"]["is_tragic_hero"]["type"] == "boolean"
    )


def test_aristotelian_mythos_schema_has_expected_shape():
    """Spot-check of ArMythos schema structure per aristotelian-
    sketch-01 A1 + production-format-sketch-06 PFS6-M1..M11 +
    PFS6-X1."""
    schema = _load_aristotelian_mythos_schema()
    assert schema["title"] == "ArMythos"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "aristotelian/mythos.json"
    )
    # Six required fields per PFS6-M1
    assert set(schema["required"]) == {
        "id", "title", "action_summary",
        "central_event_ids", "plot_kind", "phases",
    }
    assert schema["additionalProperties"] is False
    # All declared properties per PFS6-M1..M11
    assert set(schema["properties"].keys()) == {
        "id", "title", "action_summary",
        "central_event_ids", "plot_kind", "phases",
        "complication_event_id", "denouement_event_id",
        "peripeteia_event_id", "anagnorisis_event_id",
        "asserts_unity_of_action", "asserts_unity_of_time",
        "asserts_unity_of_place",
        "unity_of_time_bound", "unity_of_place_max_locations",
        "aims_at_catharsis", "characters",
    }
    # central_event_ids non-empty array (PFS6-M3)
    central = schema["properties"]["central_event_ids"]
    assert central["type"] == "array"
    assert central["minItems"] == 1
    # plot_kind closed enum (PFS6-M4)
    assert set(schema["properties"]["plot_kind"]["enum"]) == {
        "simple", "complex",
    }
    # phases non-empty array via cross-file $ref (PFS6-M5 + PFS6-X1)
    phases = schema["properties"]["phases"]
    assert phases["type"] == "array"
    assert phases["minItems"] == 1
    assert phases["items"]["$ref"] == (
        "https://brazilofmux.github.io/story/schema/"
        "aristotelian/phase.json"
    )
    # characters array via cross-file $ref (PFS6-M11 + PFS6-X1)
    characters = schema["properties"]["characters"]
    assert characters["type"] == "array"
    assert characters["items"]["$ref"] == (
        "https://brazilofmux.github.io/story/schema/"
        "aristotelian/character.json"
    )
    # Complex-plot conditional via allOf/if-then-else-anyOf (PFS6-M6)
    all_of = schema.get("allOf", [])
    assert len(all_of) == 1
    clause = all_of[0]
    assert clause["if"]["properties"]["plot_kind"]["const"] == "complex"
    assert "anyOf" in clause["then"]
    required_sets = [
        set(branch["required"])
        for branch in clause["then"]["anyOf"]
    ]
    assert {"peripeteia_event_id"} in required_sets
    assert {"anagnorisis_event_id"} in required_sets


def test_aristotelian_phase_corpus_conformance():
    """Every ArPhase reachable through encoding-level ArMythos
    records validates against schema/aristotelian/phase.json
    (production-format-sketch-06 PFS6-P1..P5)."""
    schema = _load_aristotelian_phase_schema()
    validator = Draft202012Validator(schema)

    _, phases_by_encoding, _ = (
        _discover_encoding_aristotelian_records()
    )
    assert phases_by_encoding, (
        "expected at least one encoding with Aristotelian phases; "
        "found none"
    )

    total = 0
    clean_passes = 0
    role_counts: dict = {}
    new_findings: list = []

    for encoding_name, phases in phases_by_encoding:
        for phase in phases:
            total += 1
            dumped = _dump_arphase(phase)
            role_counts[dumped["role"]] = (
                role_counts.get(dumped["role"], 0) + 1
            )
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "phase_id": phase.id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_aristotelian_phase_corpus_conformance: "
        f"{total} ArPhase records"
    )
    print(f"  clean passes:               {clean_passes}")
    print(
        f"  by role:                    "
        f"{dict(sorted(role_counts.items()))}"
    )
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: {finding['phase_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} ArPhase conformance finding(s); see "
        f"output. Resolve per production-format-sketch-06's "
        f"§Conformance dispositions protocol."
    )
    assert total > 0


def test_aristotelian_character_corpus_conformance():
    """Every ArCharacter reachable through encoding-level ArMythos
    records validates against schema/aristotelian/character.json
    (production-format-sketch-06 PFS6-C1..C5)."""
    schema = _load_aristotelian_character_schema()
    validator = Draft202012Validator(schema)

    _, _, chars_by_encoding = (
        _discover_encoding_aristotelian_records()
    )
    assert chars_by_encoding, (
        "expected at least one encoding with Aristotelian "
        "characters; found none"
    )

    total = 0
    clean_passes = 0
    tragic_hero_count = 0
    new_findings: list = []

    for encoding_name, characters in chars_by_encoding:
        for character in characters:
            total += 1
            dumped = _dump_archaracter(character)
            if dumped.get("is_tragic_hero"):
                tragic_hero_count += 1
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "character_id": character.id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_aristotelian_character_corpus_conformance: "
        f"{total} ArCharacter records"
    )
    print(f"  clean passes:               {clean_passes}")
    print(f"  is_tragic_hero=True:        {tragic_hero_count}")
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: "
                f"{finding['character_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} ArCharacter conformance finding(s); "
        f"see output. Resolve per production-format-sketch-06's "
        f"§Conformance dispositions protocol."
    )
    assert total > 0


def test_aristotelian_mythos_corpus_conformance():
    """Every ArMythos across every encoding's AR_*_MYTHOS /
    AR_*_MYTHOI exports validates against
    schema/aristotelian/mythos.json (production-format-sketch-06
    PFS6-M1..M11 + PFS6-X1). Uses the registry-bound validator
    because mythos.json $refs its sibling phase.json and
    character.json (PFS6-D5)."""
    registry = _build_schema_registry()
    mythos_schema = _load_aristotelian_mythos_schema()
    validator = Draft202012Validator(
        mythos_schema, registry=registry,
    )

    mythoi_by_encoding, _, _ = (
        _discover_encoding_aristotelian_records()
    )
    assert mythoi_by_encoding, (
        "expected at least one encoding with ArMythos records; "
        "found none"
    )

    total = 0
    clean_passes = 0
    plot_kind_counts: dict = {}
    new_findings: list = []

    for encoding_name, mythoi in mythoi_by_encoding:
        for mythos in mythoi:
            total += 1
            dumped = _dump_armythos(mythos)
            plot_kind_counts[dumped["plot_kind"]] = (
                plot_kind_counts.get(dumped["plot_kind"], 0) + 1
            )
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "mythos_id": mythos.id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_aristotelian_mythos_corpus_conformance: "
        f"{total} ArMythos records"
    )
    print(f"  clean passes:               {clean_passes}")
    print(
        f"  by plot_kind:               "
        f"{dict(sorted(plot_kind_counts.items()))}"
    )
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: {finding['mythos_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} ArMythos conformance finding(s); "
        f"see output. Resolve per production-format-sketch-06's "
        f"§Conformance dispositions protocol."
    )
    assert total > 0


# ============================================================================
# Save-the-Cat conformance — PFS7
# ============================================================================


def test_save_the_cat_character_schema_metaschema_valid():
    """schema/save_the_cat/character.json is a valid JSON Schema
    2020-12 document (production-format-sketch-07 PFS7-CH1..CH4)."""
    schema = _load_save_the_cat_character_schema()
    Draft202012Validator.check_schema(schema)


def test_save_the_cat_strand_schema_metaschema_valid():
    """schema/save_the_cat/strand.json is a valid JSON Schema
    2020-12 document (production-format-sketch-07 PFS7-SR1..SR4)."""
    schema = _load_save_the_cat_strand_schema()
    Draft202012Validator.check_schema(schema)


def test_save_the_cat_beat_schema_metaschema_valid():
    """schema/save_the_cat/beat.json is a valid JSON Schema 2020-12
    document (production-format-sketch-07 PFS7-BT1..BT5 + PFS7-X2
    inline strand_advancement $defs)."""
    schema = _load_save_the_cat_beat_schema()
    Draft202012Validator.check_schema(schema)


def test_save_the_cat_story_schema_metaschema_valid():
    """schema/save_the_cat/story.json is a valid JSON Schema 2020-12
    document (production-format-sketch-07 PFS7-ST1..ST6 + PFS7-X2
    inline archetype_assignment $defs)."""
    schema = _load_save_the_cat_story_schema()
    Draft202012Validator.check_schema(schema)


def test_save_the_cat_character_schema_has_expected_shape():
    """Spot-check of StcCharacter schema structure per save-the-cat-
    sketch-02 S9/S10 + production-format-sketch-07 PFS7-CH1..CH4."""
    schema = _load_save_the_cat_character_schema()
    assert schema["title"] == "StcCharacter"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "save_the_cat/character.json"
    )
    assert set(schema["required"]) == {"id", "name"}
    assert schema["additionalProperties"] is False
    assert set(schema["properties"].keys()) == {
        "id", "name", "description", "role_labels", "authored_by",
    }
    # role_labels is open per PFS7-CH4 — no enum, any non-empty string
    role_labels = schema["properties"]["role_labels"]
    assert role_labels["type"] == "array"
    assert role_labels["items"]["type"] == "string"
    assert role_labels["items"]["minLength"] == 1
    assert "enum" not in role_labels["items"]


def test_save_the_cat_strand_schema_has_expected_shape():
    """Spot-check of StcStrand schema structure per save-the-cat-
    sketch-01 S3 + sketch-02 S11 + production-format-sketch-07
    PFS7-SR1..SR4."""
    schema = _load_save_the_cat_strand_schema()
    assert schema["title"] == "StcStrand"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "save_the_cat/strand.json"
    )
    assert set(schema["required"]) == {"id", "kind"}
    assert schema["additionalProperties"] is False
    assert set(schema["properties"].keys()) == {
        "id", "kind", "description", "focal_character_id",
        "authored_by",
    }
    # kind closed enum at the two Save-the-Cat strand kinds (PFS7-SR2)
    assert set(schema["properties"]["kind"]["enum"]) == {
        "a-story", "b-story",
    }
    # focal_character_id optional non-empty string (PFS7-SR4)
    fci = schema["properties"]["focal_character_id"]
    assert fci["type"] == "string"
    assert fci["minLength"] == 1


def test_save_the_cat_beat_schema_has_expected_shape():
    """Spot-check of StcBeat schema structure per save-the-cat-
    sketch-01 S1/S2/S3 + sketch-02 S11 + production-format-sketch-
    07 PFS7-BT1..BT5 + PFS7-X2."""
    schema = _load_save_the_cat_beat_schema()
    assert schema["title"] == "StcBeat"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "save_the_cat/beat.json"
    )
    assert set(schema["required"]) == {"id", "slot", "page_actual"}
    assert schema["additionalProperties"] is False
    assert set(schema["properties"].keys()) == {
        "id", "slot", "page_actual", "description_of_change",
        "advances", "participant_ids", "authored_by",
    }
    # slot integer 1..15 (PFS7-BT2; matches NUM_CANONICAL_BEATS)
    slot = schema["properties"]["slot"]
    assert slot["type"] == "integer"
    assert slot["minimum"] == 1
    assert slot["maximum"] == 15
    # page_actual integer, no bound (PFS7-BT2)
    page = schema["properties"]["page_actual"]
    assert page["type"] == "integer"
    assert "minimum" not in page
    # advances via inline $defs per PFS7-X2 + PFS7-BT4
    advances = schema["properties"]["advances"]
    assert advances["type"] == "array"
    assert advances["items"]["$ref"] == "#/$defs/strand_advancement"
    sa = schema["$defs"]["strand_advancement"]
    assert set(sa["required"]) == {"strand_id"}
    assert sa["additionalProperties"] is False
    # participant_ids as plain-string array per PFS7-BT5
    pids = schema["properties"]["participant_ids"]
    assert pids["type"] == "array"
    assert pids["items"]["type"] == "string"
    assert pids["items"]["minLength"] == 1


def test_save_the_cat_story_schema_has_expected_shape():
    """Spot-check of StcStory schema structure per save-the-cat-
    sketch-01 S4/S5 + sketch-02 S11/S12 + production-format-
    sketch-07 PFS7-ST1..ST6 + PFS7-X1 + PFS7-X2."""
    schema = _load_save_the_cat_story_schema()
    assert schema["title"] == "StcStory"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "save_the_cat/story.json"
    )
    assert set(schema["required"]) == {"id", "title"}
    assert schema["additionalProperties"] is False
    assert set(schema["properties"].keys()) == {
        "id", "title", "theme_statement", "stc_genre_id",
        "beat_ids", "strand_ids", "character_ids",
        "archetype_assignments", "authored_by",
    }
    # beat_ids / strand_ids / character_ids: plain-string arrays
    # per PFS7-X1 (flat-with-id-refs). Guard against accidental
    # promotion to $ref-typed arrays.
    for field in ("beat_ids", "strand_ids", "character_ids"):
        arr = schema["properties"][field]
        assert arr["type"] == "array"
        assert arr["items"]["type"] == "string"
        assert arr["items"]["minLength"] == 1
        assert "$ref" not in arr["items"], (
            f"{field} items must be plain strings per PFS7-X1, not "
            f"$ref-typed"
        )
    # archetype_assignments via inline $defs per PFS7-X2 + PFS7-ST6
    aa_arr = schema["properties"]["archetype_assignments"]
    assert aa_arr["type"] == "array"
    assert aa_arr["items"]["$ref"] == "#/$defs/archetype_assignment"
    aa_def = schema["$defs"]["archetype_assignment"]
    assert set(aa_def["required"]) == {"archetype"}
    assert aa_def["additionalProperties"] is False
    assert set(aa_def["properties"].keys()) == {
        "archetype", "character_id", "note",
    }


def test_save_the_cat_character_corpus_conformance():
    """Every StcCharacter in every encoding's CHARACTERS tuple
    validates against schema/save_the_cat/character.json
    (production-format-sketch-07 PFS7-CH1..CH4 + PFS7-D4)."""
    schema = _load_save_the_cat_character_schema()
    validator = Draft202012Validator(schema)

    _, _, _, chars_by_encoding = (
        _discover_encoding_save_the_cat_records()
    )
    assert chars_by_encoding, (
        "expected at least one encoding with Save-the-Cat "
        "characters; found none"
    )

    total = 0
    clean_passes = 0
    role_label_total = 0
    new_findings: list = []

    for encoding_name, characters in chars_by_encoding:
        for character in characters:
            total += 1
            dumped = _dump_stccharacter(character)
            role_label_total += len(dumped["role_labels"])
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "character_id": character.id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_save_the_cat_character_corpus_conformance: "
        f"{total} StcCharacter records"
    )
    print(f"  clean passes:               {clean_passes}")
    print(f"  total role_labels emitted:  {role_label_total}")
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: "
                f"{finding['character_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} StcCharacter conformance finding(s); "
        f"see output. Resolve per production-format-sketch-07's "
        f"§Conformance dispositions protocol."
    )
    assert total > 0


def test_save_the_cat_strand_corpus_conformance():
    """Every StcStrand in every encoding's STRANDS tuple validates
    against schema/save_the_cat/strand.json (production-format-
    sketch-07 PFS7-SR1..SR4 + PFS7-D3)."""
    schema = _load_save_the_cat_strand_schema()
    validator = Draft202012Validator(schema)

    _, _, strands_by_encoding, _ = (
        _discover_encoding_save_the_cat_records()
    )
    assert strands_by_encoding, (
        "expected at least one encoding with Save-the-Cat strands; "
        "found none"
    )

    total = 0
    clean_passes = 0
    kind_counts: dict = {}
    new_findings: list = []

    for encoding_name, strands in strands_by_encoding:
        for strand in strands:
            total += 1
            dumped = _dump_stcstrand(strand)
            kind_counts[dumped["kind"]] = (
                kind_counts.get(dumped["kind"], 0) + 1
            )
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "strand_id": strand.id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_save_the_cat_strand_corpus_conformance: "
        f"{total} StcStrand records"
    )
    print(f"  clean passes:               {clean_passes}")
    print(
        f"  by kind:                    "
        f"{dict(sorted(kind_counts.items()))}"
    )
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: {finding['strand_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} StcStrand conformance finding(s); "
        f"see output. Resolve per production-format-sketch-07's "
        f"§Conformance dispositions protocol."
    )
    assert total > 0


def test_save_the_cat_beat_corpus_conformance():
    """Every StcBeat in every encoding's BEATS tuple validates
    against schema/save_the_cat/beat.json (production-format-
    sketch-07 PFS7-BT1..BT5 + PFS7-D2)."""
    schema = _load_save_the_cat_beat_schema()
    validator = Draft202012Validator(schema)

    _, beats_by_encoding, _, _ = (
        _discover_encoding_save_the_cat_records()
    )
    assert beats_by_encoding, (
        "expected at least one encoding with Save-the-Cat beats; "
        "found none"
    )

    total = 0
    clean_passes = 0
    slot_counts: dict = {}
    total_advancements = 0
    new_findings: list = []

    for encoding_name, beats in beats_by_encoding:
        for beat in beats:
            total += 1
            dumped = _dump_stcbeat(beat)
            slot_counts[dumped["slot"]] = (
                slot_counts.get(dumped["slot"], 0) + 1
            )
            total_advancements += len(dumped["advances"])
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "beat_id": beat.id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_save_the_cat_beat_corpus_conformance: "
        f"{total} StcBeat records"
    )
    print(f"  clean passes:               {clean_passes}")
    print(
        f"  by slot:                    "
        f"{dict(sorted(slot_counts.items()))}"
    )
    print(f"  total StrandAdvancements:   {total_advancements}")
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: {finding['beat_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} StcBeat conformance finding(s); "
        f"see output. Resolve per production-format-sketch-07's "
        f"§Conformance dispositions protocol."
    )
    assert total > 0


def test_save_the_cat_story_corpus_conformance():
    """Every StcStory in every encoding's STORY singleton validates
    against schema/save_the_cat/story.json (production-format-
    sketch-07 PFS7-ST1..ST6 + PFS7-D1). Uses a plain validator —
    story.json has no outbound cross-file $ref per PFS7-X1."""
    schema = _load_save_the_cat_story_schema()
    validator = Draft202012Validator(schema)

    stories_by_encoding, _, _, _ = (
        _discover_encoding_save_the_cat_records()
    )
    assert stories_by_encoding, (
        "expected at least one encoding with a Save-the-Cat Story; "
        "found none"
    )

    total = 0
    clean_passes = 0
    genre_counts: dict = {}
    total_archetype_assignments = 0
    new_findings: list = []

    for encoding_name, stories in stories_by_encoding:
        for story in stories:
            total += 1
            dumped = _dump_stcstory(story)
            genre = dumped.get("stc_genre_id", "<none>")
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
            total_archetype_assignments += len(
                dumped["archetype_assignments"]
            )
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "story_id": story.id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_save_the_cat_story_corpus_conformance: "
        f"{total} StcStory records"
    )
    print(f"  clean passes:               {clean_passes}")
    print(
        f"  by genre:                   "
        f"{dict(sorted(genre_counts.items()))}"
    )
    print(
        f"  total archetype_assignments: {total_archetype_assignments}"
    )
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: {finding['story_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} StcStory conformance finding(s); "
        f"see output. Resolve per production-format-sketch-07's "
        f"§Conformance dispositions protocol."
    )
    assert total > 0


# ============================================================================
# Lowering-family conformance — PFS9
# ============================================================================


def test_lowering_annotation_review_schema_metaschema_valid():
    """schema/lowering/annotation_review.json is a valid JSON Schema
    2020-12 document (production-format-sketch-09 PFS9-AR1..AR4)."""
    schema = _load_lowering_annotation_review_schema()
    Draft202012Validator.check_schema(schema)


def test_lowering_observation_schema_metaschema_valid():
    """schema/lowering/lowering_observation.json is a valid JSON
    Schema 2020-12 document (production-format-sketch-09
    PFS9-LO1..LO4)."""
    schema = _load_lowering_observation_schema()
    Draft202012Validator.check_schema(schema)


def test_lowering_schema_metaschema_valid():
    """schema/lowering/lowering.json is a valid JSON Schema 2020-12
    document (production-format-sketch-09 PFS9-L1..L10 +
    PFS9-X1/X2/X3)."""
    schema = _load_lowering_schema()
    Draft202012Validator.check_schema(schema)


def test_lowering_annotation_review_schema_has_expected_shape():
    """Spot-check of AnnotationReview schema structure per
    lowering-record-sketch-01 L6 + PFS9-AR1..AR4."""
    schema = _load_lowering_annotation_review_schema()
    assert schema["title"] == "AnnotationReview"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "lowering/annotation_review.json"
    )
    assert set(schema["required"]) == {
        "reviewer_id", "reviewed_at_τ_a", "verdict", "anchor_τ_a",
    }
    assert schema["additionalProperties"] is False
    assert set(schema["properties"].keys()) == {
        "reviewer_id", "reviewed_at_τ_a", "verdict", "anchor_τ_a",
        "comment",
    }
    assert set(schema["properties"]["verdict"]["enum"]) == {
        "approved", "needs-work", "rejected", "noted",
    }


def test_lowering_observation_schema_has_expected_shape():
    """Spot-check of LoweringObservation schema structure per
    core/lowering.py:validate_lowerings emission pattern +
    PFS9-LO1..LO4."""
    schema = _load_lowering_observation_schema()
    assert schema["title"] == "LoweringObservation"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "lowering/lowering_observation.json"
    )
    assert set(schema["required"]) == {
        "severity", "code", "target_id", "message",
    }
    assert schema["additionalProperties"] is False
    assert set(schema["properties"].keys()) == {
        "severity", "code", "target_id", "message",
    }
    assert set(schema["properties"]["severity"]["enum"]) == {
        "noted", "advises-review",
    }
    assert "enum" not in schema["properties"]["code"]


def test_lowering_schema_has_expected_shape():
    """Spot-check of Lowering schema structure per lowering-record-
    sketch-01 L1..L10 + PFS9-L1..L10 + PFS9-X1..X4."""
    schema = _load_lowering_schema()
    assert schema["title"] == "Lowering"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/lowering/lowering.json"
    )
    assert set(schema["required"]) == {
        "id", "upper_record", "lower_records", "annotation", "status",
    }
    assert schema["additionalProperties"] is False
    assert set(schema["properties"].keys()) == {
        "id", "upper_record", "lower_records", "annotation",
        "authored_by", "τ_a", "status", "position_range",
        "anchor_τ_a", "metadata",
    }
    assert set(schema["$defs"].keys()) == {
        "cross_dialect_ref", "annotation", "position_range",
    }
    cdr = schema["$defs"]["cross_dialect_ref"]
    assert set(cdr["required"]) == {"dialect", "record_id"}
    assert cdr["additionalProperties"] is False
    assert "enum" not in cdr["properties"]["dialect"]
    assert cdr["properties"]["dialect"]["minLength"] == 1
    ann = schema["$defs"]["annotation"]
    assert set(ann["required"]) == {"text"}
    assert ann["additionalProperties"] is False
    assert set(ann["properties"]["attention"]["enum"]) == {
        "structural", "interpretive", "flavor",
    }
    rs = ann["properties"]["review_states"]
    assert rs["type"] == "array"
    assert rs["items"]["$ref"] == (
        "https://brazilofmux.github.io/story/schema/"
        "lowering/annotation_review.json"
    )
    pr = schema["$defs"]["position_range"]
    assert set(pr["required"]) == {"coord", "min_value", "max_value"}
    assert pr["additionalProperties"] is False
    assert schema["properties"]["upper_record"]["$ref"] == (
        "#/$defs/cross_dialect_ref"
    )
    assert schema["properties"]["lower_records"]["items"]["$ref"] == (
        "#/$defs/cross_dialect_ref"
    )
    assert set(schema["properties"]["status"]["enum"]) == {
        "active", "pending",
    }
    all_of = schema.get("allOf", [])
    assert len(all_of) == 1
    clause = all_of[0]
    assert clause["if"]["properties"]["status"]["const"] == "active"
    assert clause["then"]["properties"]["lower_records"]["minItems"] == 1
    assert schema["properties"]["metadata"]["type"] == "object"
    assert (
        schema["properties"]["metadata"]["additionalProperties"] is True
    )


def test_lowering_corpus_conformance():
    """Every Lowering in every encoding's LOWERINGS tuple validates
    against schema/lowering/lowering.json (PFS9-L1..L10 + PFS9-D1).
    Uses the registry-bound validator because lowering.json's inline
    $defs/annotation.review_states cross-file-refs
    annotation_review.json per PFS9-X2."""
    registry = _build_schema_registry()
    schema = _load_lowering_schema()
    validator = Draft202012Validator(schema, registry=registry)

    lowerings_by_encoding = _discover_encoding_lowerings()
    assert lowerings_by_encoding, (
        "expected at least one encoding with authored Lowerings; "
        "found none"
    )

    total = 0
    clean_passes = 0
    status_counts: dict = {}
    position_range_count = 0
    anchor_τ_a_count = 0
    metadata_count = 0
    new_findings: list = []

    for encoding_name, lowerings in lowerings_by_encoding:
        for lw in lowerings:
            total += 1
            dumped = _dump_lowering(lw)
            status_counts[dumped["status"]] = (
                status_counts.get(dumped["status"], 0) + 1
            )
            if "position_range" in dumped:
                position_range_count += 1
            if "anchor_τ_a" in dumped:
                anchor_τ_a_count += 1
            if "metadata" in dumped:
                metadata_count += 1
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "lowering_id": lw.id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_lowering_corpus_conformance: "
        f"{total} Lowering records"
    )
    print(f"  clean passes:               {clean_passes}")
    print(
        f"  by status:                  "
        f"{dict(sorted(status_counts.items()))}"
    )
    print(f"  with position_range:        {position_range_count}")
    print(f"  with anchor_τ_a:            {anchor_τ_a_count}")
    print(f"  with metadata:              {metadata_count}")
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: "
                f"{finding['lowering_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} Lowering conformance finding(s); "
        f"see output. Resolve per production-format-sketch-09's "
        f"§Conformance dispositions protocol."
    )
    assert total > 0


def test_lowering_annotation_review_corpus_conformance():
    """Every AnnotationReview reachable through encoded Lowering's
    annotation.review_states validates against
    schema/lowering/annotation_review.json (PFS9-AR1..AR4).

    Today's corpus has zero authored review_states (encodings
    don't populate reviews; those land from the reader-model
    probe output surface). Test passes with total=0 and a
    descriptive note per PFS9 §Corpus expectations."""
    schema = _load_lowering_annotation_review_schema()
    validator = Draft202012Validator(schema)

    lowerings_by_encoding = _discover_encoding_lowerings()

    total = 0
    clean_passes = 0
    verdict_counts: dict = {}
    new_findings: list = []

    for encoding_name, lowerings in lowerings_by_encoding:
        for lw in lowerings:
            for review in lw.annotation.review_states:
                total += 1
                dumped = _dump_annotation_review(review)
                verdict_counts[dumped["verdict"]] = (
                    verdict_counts.get(dumped["verdict"], 0) + 1
                )
                errors = sorted(
                    validator.iter_errors(dumped),
                    key=lambda e: list(e.absolute_path),
                )
                if not errors:
                    clean_passes += 1
                    continue
                new_findings.append({
                    "encoding": encoding_name,
                    "lowering_id": lw.id,
                    "errors": [
                        {
                            "path": list(e.absolute_path),
                            "validator": e.validator,
                            "message": e.message,
                        }
                        for e in errors
                    ],
                })

    print()
    print(
        f"test_lowering_annotation_review_corpus_conformance: "
        f"{total} AnnotationReview records"
    )
    print(f"  clean passes:               {clean_passes}")
    if verdict_counts:
        print(
            f"  by verdict:                 "
            f"{dict(sorted(verdict_counts.items()))}"
        )
    else:
        print(
            f"  note:                       "
            f"zero authored review_states today; expected per "
            f"PFS9 §Corpus expectations"
        )
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: "
                f"{finding['lowering_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} AnnotationReview conformance "
        f"finding(s); see output."
    )


def test_lowering_observation_corpus_conformance():
    """Every LoweringObservation emitted by validate_lowerings on each
    encoding's LOWERINGS tuple validates against
    schema/lowering/lowering_observation.json (PFS9-LO1..LO4). A
    clean corpus emits zero observations (otherwise the encoding
    has a self-consistency issue pre-dating PFS9)."""
    from story_engine.core.lowering import validate_lowerings

    schema = _load_lowering_observation_schema()
    validator = Draft202012Validator(schema)

    lowerings_by_encoding = _discover_encoding_lowerings()
    assert lowerings_by_encoding, (
        "expected at least one encoding with authored Lowerings; "
        "found none"
    )

    total = 0
    clean_passes = 0
    code_counts: dict = {}
    severity_counts: dict = {}
    new_findings: list = []
    observations_by_encoding: dict = {}

    for encoding_name, lowerings in lowerings_by_encoding:
        observations = validate_lowerings(tuple(lowerings))
        if observations:
            observations_by_encoding[encoding_name] = observations
        for obs in observations:
            total += 1
            dumped = _dump_lowering_observation(obs)
            code_counts[dumped["code"]] = (
                code_counts.get(dumped["code"], 0) + 1
            )
            severity_counts[dumped["severity"]] = (
                severity_counts.get(dumped["severity"], 0) + 1
            )
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "observation_code": obs.code,
                "observation_target": obs.target_id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_lowering_observation_corpus_conformance: "
        f"{total} LoweringObservation records"
    )
    print(f"  clean passes:               {clean_passes}")
    if severity_counts:
        print(
            f"  by severity:                "
            f"{dict(sorted(severity_counts.items()))}"
        )
        print(
            f"  by code:                    "
            f"{dict(sorted(code_counts.items()))}"
        )
        print(
            f"  emitting encodings:         "
            f"{sorted(observations_by_encoding.keys())}"
        )
    else:
        print(
            f"  note:                       "
            f"zero observations — corpus is self-consistent"
        )
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: "
                f"{finding['observation_code']} "
                f"@ {finding['observation_target']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} LoweringObservation conformance "
        f"finding(s); see output."
    )


# ============================================================================
# Verification-family conformance — PFS10
# ============================================================================


def test_verification_review_schema_metaschema_valid():
    """schema/verification/verification_review.json is a valid JSON
    Schema 2020-12 document (production-format-sketch-10
    PFS10-VR1..VR5)."""
    schema = _load_verification_review_schema()
    Draft202012Validator.check_schema(schema)


def test_structural_advisory_schema_metaschema_valid():
    """schema/verification/structural_advisory.json is a valid JSON
    Schema 2020-12 document (production-format-sketch-10
    PFS10-SA1..SA4)."""
    schema = _load_verification_structural_advisory_schema()
    Draft202012Validator.check_schema(schema)


def test_verification_answer_proposal_schema_metaschema_valid():
    """schema/verification/verification_answer_proposal.json is a
    valid JSON Schema 2020-12 document (production-format-sketch-10
    PFS10-AP1..AP3)."""
    schema = _load_verification_answer_proposal_schema()
    Draft202012Validator.check_schema(schema)


def test_verifier_commentary_schema_metaschema_valid():
    """schema/verification/verifier_commentary.json is a valid JSON
    Schema 2020-12 document (production-format-sketch-10
    PFS10-VC1..VC4 + PFS10-X2)."""
    schema = _load_verifier_commentary_schema()
    Draft202012Validator.check_schema(schema)


def test_verification_review_schema_has_expected_shape():
    """Spot-check of VerificationReview schema structure per
    verification-sketch-01 V2 + PFS10-VR1..VR5 + PFS10-X1."""
    schema = _load_verification_review_schema()
    assert schema["title"] == "VerificationReview"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "verification/verification_review.json"
    )
    assert set(schema["required"]) == {
        "reviewer_id", "reviewed_at_τ_a", "verdict",
        "anchor_τ_a", "target_record",
    }
    assert schema["additionalProperties"] is False
    assert set(schema["properties"].keys()) == {
        "reviewer_id", "reviewed_at_τ_a", "verdict",
        "anchor_τ_a", "target_record", "comment", "match_strength",
    }
    # verdict closed enum (PFS10-VR3)
    assert set(schema["properties"]["verdict"]["enum"]) == {
        "approved", "needs-work", "partial-match", "noted",
    }
    # target_record uses inline $defs/cross_dialect_ref per PFS10-X1
    assert schema["properties"]["target_record"]["$ref"] == (
        "#/$defs/cross_dialect_ref"
    )
    assert "cross_dialect_ref" in schema["$defs"]
    cdr = schema["$defs"]["cross_dialect_ref"]
    assert set(cdr["required"]) == {"dialect", "record_id"}
    assert cdr["additionalProperties"] is False
    # match_strength bounded [0, 1] per PFS10-VR5
    ms = schema["properties"]["match_strength"]
    assert ms["type"] == "number"
    assert ms["minimum"] == 0
    assert ms["maximum"] == 1


def test_structural_advisory_schema_has_expected_shape():
    """Spot-check of StructuralAdvisory schema structure per V2 +
    PFS10-SA1..SA4 + PFS10-X1."""
    schema = _load_verification_structural_advisory_schema()
    assert schema["title"] == "StructuralAdvisory"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "verification/structural_advisory.json"
    )
    assert set(schema["required"]) == {
        "advisor_id", "advised_at_τ_a", "severity",
        "comment", "scope",
    }
    assert schema["additionalProperties"] is False
    # severity closed enum (PFS10-SA3)
    assert set(schema["properties"]["severity"]["enum"]) == {
        "noted", "suggest-review", "suggest-revise",
    }
    # scope uses inline cross_dialect_ref (PFS10-X1)
    scope = schema["properties"]["scope"]
    assert scope["type"] == "array"
    assert scope["items"]["$ref"] == "#/$defs/cross_dialect_ref"
    assert "cross_dialect_ref" in schema["$defs"]


def test_verification_answer_proposal_schema_has_expected_shape():
    """Spot-check of VerificationAnswerProposal schema structure per
    V2 + PFS10-AP1..AP3 + PFS10-X1 + PFS10-X3."""
    schema = _load_verification_answer_proposal_schema()
    assert schema["title"] == "VerificationAnswerProposal"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "verification/verification_answer_proposal.json"
    )
    assert set(schema["required"]) == {
        "proposer_id", "question_id", "proposed_text",
        "rationale", "proposed_at_τ_a", "status",
    }
    assert schema["additionalProperties"] is False
    # question_id uses inline cross_dialect_ref (PFS10-X1)
    assert schema["properties"]["question_id"]["$ref"] == (
        "#/$defs/cross_dialect_ref"
    )
    assert "cross_dialect_ref" in schema["$defs"]
    # status is open non-empty string per PFS10-AP3 / PFS10-X3
    status = schema["properties"]["status"]
    assert status["type"] == "string"
    assert status["minLength"] == 1
    assert "enum" not in status


def test_verifier_commentary_schema_has_expected_shape():
    """Spot-check of VerifierCommentary schema structure per V7 +
    PFS10-VC1..VC4 + PFS10-X2."""
    schema = _load_verifier_commentary_schema()
    assert schema["title"] == "VerifierCommentary"
    assert schema["$id"] == (
        "https://brazilofmux.github.io/story/schema/"
        "verification/verifier_commentary.json"
    )
    assert set(schema["required"]) == {
        "commenter_id", "commented_at_τ_a", "assessment",
        "target_review", "comment",
    }
    assert schema["additionalProperties"] is False
    # assessment closed enum (PFS10-VC3)
    assert set(schema["properties"]["assessment"]["enum"]) == {
        "endorses", "qualifies", "dissents", "noted",
    }
    # target_review cross-file $ref to verification_review.json per PFS10-X2
    assert schema["properties"]["target_review"]["$ref"] == (
        "https://brazilofmux.github.io/story/schema/"
        "verification/verification_review.json"
    )
    # No inline cross_dialect_ref (target_review encapsulates it)
    assert "$defs" not in schema or (
        "cross_dialect_ref" not in schema.get("$defs", {})
    )


def test_verification_review_corpus_conformance():
    """Every VerificationReview emitted by running each encoding's
    *_verification.py run() function validates against
    schema/verification/verification_review.json (PFS10-VR1..VR5 +
    PFS10-D1)."""
    schema = _load_verification_review_schema()
    validator = Draft202012Validator(schema)

    reviews_by_encoding, _, _, _ = (
        _discover_encoding_verifier_output()
    )
    assert reviews_by_encoding, (
        "expected at least one encoding emitting VerificationReview "
        "records; found none"
    )

    total = 0
    clean_passes = 0
    verdict_counts: dict = {}
    match_strength_count = 0
    comment_count = 0
    new_findings: list = []

    for encoding_name, reviews in reviews_by_encoding:
        for review in reviews:
            total += 1
            dumped = _dump_verification_review(review)
            verdict_counts[dumped["verdict"]] = (
                verdict_counts.get(dumped["verdict"], 0) + 1
            )
            if "match_strength" in dumped:
                match_strength_count += 1
            if "comment" in dumped:
                comment_count += 1
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "reviewer_id": review.reviewer_id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_verification_review_corpus_conformance: "
        f"{total} VerificationReview records"
    )
    print(f"  clean passes:               {clean_passes}")
    print(
        f"  by verdict:                 "
        f"{dict(sorted(verdict_counts.items()))}"
    )
    print(f"  with match_strength:        {match_strength_count}")
    print(f"  with comment:               {comment_count}")
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: "
                f"{finding['reviewer_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} VerificationReview conformance "
        f"finding(s); see output. Resolve per production-format-"
        f"sketch-10's §Conformance dispositions protocol."
    )
    assert total > 0


def test_structural_advisory_corpus_conformance():
    """Every StructuralAdvisory emitted by running each encoding's
    *_verification.py run() function validates against
    schema/verification/structural_advisory.json (PFS10-SA1..SA4 +
    PFS10-D2). The skeleton encoding emits at least one; most
    verifiers emit zero."""
    schema = _load_verification_structural_advisory_schema()
    validator = Draft202012Validator(schema)

    _, advisories_by_encoding, _, _ = (
        _discover_encoding_verifier_output()
    )

    total = 0
    clean_passes = 0
    severity_counts: dict = {}
    new_findings: list = []

    for encoding_name, advisories in advisories_by_encoding:
        for advisory in advisories:
            total += 1
            dumped = _dump_structural_advisory(advisory)
            severity_counts[dumped["severity"]] = (
                severity_counts.get(dumped["severity"], 0) + 1
            )
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "advisor_id": advisory.advisor_id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_structural_advisory_corpus_conformance: "
        f"{total} StructuralAdvisory records"
    )
    print(f"  clean passes:               {clean_passes}")
    if severity_counts:
        print(
            f"  by severity:                "
            f"{dict(sorted(severity_counts.items()))}"
        )
        print(
            f"  emitting encodings:         "
            f"{sorted(name for name, _ in advisories_by_encoding)}"
        )
    else:
        print(
            f"  note:                       "
            f"zero advisories; expected (only skeleton encoding "
            f"emits one)"
        )
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: "
                f"{finding['advisor_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} StructuralAdvisory conformance "
        f"finding(s); see output."
    )


def test_verification_answer_proposal_corpus_conformance():
    """Every VerificationAnswerProposal emitted by *_verification.py
    run() functions validates against
    schema/verification/verification_answer_proposal.json
    (PFS10-AP1..AP3 + PFS10-D3). Today's corpus emits zero;
    schema structure validated via metaschema + shape tests."""
    schema = _load_verification_answer_proposal_schema()
    validator = Draft202012Validator(schema)

    _, _, proposals_by_encoding, _ = (
        _discover_encoding_verifier_output()
    )

    total = 0
    clean_passes = 0
    status_counts: dict = {}
    new_findings: list = []

    for encoding_name, proposals in proposals_by_encoding:
        for proposal in proposals:
            total += 1
            dumped = _dump_verification_answer_proposal(proposal)
            status_counts[dumped["status"]] = (
                status_counts.get(dumped["status"], 0) + 1
            )
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "proposer_id": proposal.proposer_id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_verification_answer_proposal_corpus_conformance: "
        f"{total} VerificationAnswerProposal records"
    )
    print(f"  clean passes:               {clean_passes}")
    if status_counts:
        print(
            f"  by status:                  "
            f"{dict(sorted(status_counts.items()))}"
        )
    else:
        print(
            f"  note:                       "
            f"zero proposals today; expected per PFS10 §Corpus "
            f"expectations"
        )
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: "
                f"{finding['proposer_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} VerificationAnswerProposal "
        f"conformance finding(s); see output."
    )


def test_verifier_commentary_corpus_conformance():
    """Every VerifierCommentary emitted by *_verification.py run()
    functions validates against
    schema/verification/verifier_commentary.json (PFS10-VC1..VC4 +
    PFS10-D4). Uses the registry-bound validator because
    verifier_commentary.json cross-file-refs
    verification_review.json per PFS10-X2. Today's corpus emits
    zero (commentary records live in probe output JSONs, not
    verifier run() output); schema structure validated via
    metaschema + shape tests."""
    registry = _build_schema_registry()
    schema = _load_verifier_commentary_schema()
    validator = Draft202012Validator(schema, registry=registry)

    _, _, _, commentaries_by_encoding = (
        _discover_encoding_verifier_output()
    )

    total = 0
    clean_passes = 0
    assessment_counts: dict = {}
    new_findings: list = []

    for encoding_name, commentaries in commentaries_by_encoding:
        for commentary in commentaries:
            total += 1
            dumped = _dump_verifier_commentary(commentary)
            assessment_counts[dumped["assessment"]] = (
                assessment_counts.get(dumped["assessment"], 0) + 1
            )
            errors = sorted(
                validator.iter_errors(dumped),
                key=lambda e: list(e.absolute_path),
            )
            if not errors:
                clean_passes += 1
                continue
            new_findings.append({
                "encoding": encoding_name,
                "commenter_id": commentary.commenter_id,
                "errors": [
                    {
                        "path": list(e.absolute_path),
                        "validator": e.validator,
                        "message": e.message,
                    }
                    for e in errors
                ],
            })

    print()
    print(
        f"test_verifier_commentary_corpus_conformance: "
        f"{total} VerifierCommentary records"
    )
    print(f"  clean passes:               {clean_passes}")
    if assessment_counts:
        print(
            f"  by assessment:              "
            f"{dict(sorted(assessment_counts.items()))}"
        )
    else:
        print(
            f"  note:                       "
            f"zero commentaries today; expected per PFS10 §Corpus "
            f"expectations (commentary records live in probe JSONs)"
        )
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(
                f"    {finding['encoding']}: "
                f"{finding['commenter_id']}"
            )
            for err in finding["errors"]:
                print(
                    f"      - path={err['path']} "
                    f"validator={err['validator']}: {err['message']}"
                )

    assert not new_findings, (
        f"{len(new_findings)} VerifierCommentary conformance "
        f"finding(s); see output."
    )


# ============================================================================
# Test runner
# ============================================================================


def main() -> int:
    tests = [
        (name, fn) for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    ]
    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
        except Exception:
            failed += 1
            print(f"FAIL  {name}")
            traceback.print_exc()
        else:
            passed += 1
            print(f"ok    {name}")
    print()
    print(f"{passed} passed, {failed} failed, {passed + failed} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
