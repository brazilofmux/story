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


def _build_schema_registry() -> Registry:
    """Build a referencing Registry mapping canonical $id URIs to the
    loaded schemas. Lets cross-file $refs resolve without fetching —
    schema/event.json $refs schema/prop.json via the canonical URI;
    schema/description.json (post production-format-sketch-03) does
    the same for its PropositionAnchor variant.

    Pattern introduced by production-format-sketch-03 P3A4; extends
    naturally to future cross-file refs (dialect records → substrate,
    Lowerings → dialect records, etc.)."""
    registry = Registry()
    for schema in (
        _load_prop_schema(), _load_event_schema(),
        _load_description_schema(),
    ):
        resource = Resource.from_contents(schema, default_specification=DRAFT202012)
        registry = registry.with_resource(uri=schema["$id"], resource=resource)
    return registry


# ============================================================================
# Known dispositions — discrepancies discovered during PFA4 implementation
# ============================================================================
#
# Each disposition names a known class of conformance failure that is
# recorded in design/production-format-sketch-01.md §Conformance
# dispositions. Records whose failure matches a known pattern are
# counted as "dispositioned" (test tolerates); records whose failure
# does NOT match cause the test to fail loudly.
#
# Adding a new disposition requires amending production-format-
# sketch-01 first; the test is not the right place to silently accept
# new drift.


# Sketch-incompleteness: `authoring-note` is used in encodings
# (rashomon.py, macbeth.py) but not enumerated in
# descriptions-sketch-01 §Kinds. Resolution path: amend
# descriptions-sketch-01 to add `authoring-note` to the kind
# vocabulary with a one-line description + typical attention +
# example (§Extension rule).
DISPOSITION_KIND_AUTHORING_NOTE = "authoring-note"

# Sketch-incompleteness: `superseded` is used on Description.status
# (representing an edited-over description) but not enumerated in
# descriptions-sketch-01 §Optional fields (which names only
# committed/provisional). Resolution path: amend descriptions-
# sketch-01 to add `superseded` as a third status value with
# semantics.
DISPOSITION_STATUS_SUPERSEDED = "superseded"


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


def _dump_knowledge_effect(effect) -> dict:
    """Map a Python KnowledgeEffect to the schema's KnowledgeEffect
    shape. Two shape divergences per production-format-sketch-03
    §Conformance dispositions (populated during implementation):

    1. Python's KnowledgeEffect wraps a full Held(prop, slot,
       confidence, via, provenance) record as `held`. The schema
       derived from substrate-effect-shape-sketch-01 ES3 has only
       (holder, prop, via) — slot/confidence/provenance are
       fold-output per ES3's scope-out. The dump extracts prop and
       via from held; discards slot, confidence, and provenance.
       This is "Python over-specified" per PFS2 — the Held fields
       are not on the effect shape the sketch committed to.

    2. Python carries a `remove: bool` retraction polarity on
       KnowledgeEffect. The sketch does not admit (ES3 "No asserts
       field"; identity-and-realization-sketch-01 explicitly argues
       against realization-removes-propositions). remove=True
       cases are dropped by the dump; a companion audit test
       (test_knowledge_effect_remove_audit) counts and reports them
       as a known disposition.
    """
    return {
        "kind": "knowledge",
        "holder": effect.agent_id,
        "prop": _dump_prop(effect.held.prop),
        "via": effect.held.via,
    }


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


# ============================================================================
# Failure classification
# ============================================================================


def _classify_failure(description, error: jsonschema.ValidationError) -> str:
    """Return a disposition name if this failure matches a known
    disposition, else 'new-finding'."""
    # Kind-enum failure: description.kind not in schema enum
    if (
        error.validator == "enum"
        and list(error.absolute_path) == ["kind"]
    ):
        return (
            DISPOSITION_KIND_AUTHORING_NOTE
            if description.kind == "authoring-note"
            else "new-finding"
        )
    # Status-enum failure
    if (
        error.validator == "enum"
        and list(error.absolute_path) == ["status"]
    ):
        status_val = (
            description.status.value
            if hasattr(description.status, "value")
            else description.status
        )
        return (
            DISPOSITION_STATUS_SUPERSEDED
            if status_val == "superseded"
            else "new-finding"
        )
    return "new-finding"


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
    # Kind enum matches descriptions-sketch-01 §Kinds
    kind_enum = set(schema["properties"]["kind"]["enum"])
    assert kind_enum == {
        "texture", "motivation", "reader-frame",
        "authorial-uncertainty", "trust-flag", "provenance",
    }
    # Status enum matches descriptions-sketch-01 §Optional fields
    status_enum = set(schema["properties"]["status"]["enum"])
    assert status_enum == {"committed", "provisional"}


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
    production-format-sketch-03 PFS3-E1 through E7."""
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
    assert defs["KnowledgeEffect"]["properties"]["kind"] == {
        "const": "knowledge"
    }
    # KnowledgeEffect via enum matches substrate-effect-shape-sketch-01
    # ES4 (11 values: 6 diegetic + 5 narrative)
    via_enum = set(
        defs["KnowledgeEffect"]["properties"]["via"]["enum"]
    )
    assert via_enum == {
        "observation", "utterance-heard", "inference",
        "deception", "forgetting", "realization",
        "disclosure", "focalization", "omission",
        "framing", "retroactive-reframing",
    }


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
    """Every Description across every encoding either validates
    against the schema or matches a known disposition. New
    findings fail loudly with the specific record id + error
    location."""
    schema = _load_description_schema()
    validator = Draft202012Validator(schema)

    encodings = _discover_encoding_descriptions()
    assert encodings, (
        "expected at least one encoding with DESCRIPTIONS; found none"
    )

    total = 0
    clean_passes = 0
    dispositioned_by_kind = {}  # disposition_name → count
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
            # Classify each error; if every error is dispositioned,
            # count as dispositioned. Mixed = treat as new-finding
            # for caution.
            error_dispositions = [
                _classify_failure(description, e) for e in errors
            ]
            if all(d != "new-finding" for d in error_dispositions):
                for d in error_dispositions:
                    dispositioned_by_kind[d] = (
                        dispositioned_by_kind.get(d, 0) + 1
                    )
            else:
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
    if dispositioned_by_kind:
        print(f"  dispositioned failures:")
        for name, count in sorted(dispositioned_by_kind.items()):
            print(f"    - {name}: {count}")
    if new_findings:
        print(f"  NEW findings (fail):        {len(new_findings)}")
        for finding in new_findings:
            print(f"    {finding['encoding']}: {finding['description_id']}")
            for err in finding["errors"]:
                print(f"      - path={err['path']} "
                      f"validator={err['validator']}: {err['message']}")

    assert not new_findings, (
        f"{len(new_findings)} new conformance finding(s) not yet "
        f"dispositioned in production-format-sketch-01; see output"
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
    """PFS2 disposition audit: Python's KnowledgeEffect carries
    a `remove: bool` retraction polarity that the schema-derived
    shape (substrate-effect-shape-sketch-01 ES3) does not admit.
    The design sketch + identity-and-realization-sketch-01 both
    argue against the 'realization removes old propositions'
    pattern this field enables.

    This test *informs*, not *blocks*. The dump-layer silently
    drops the remove field (schema doesn't admit it); this audit
    surfaces the count so a cleanup arc can be scoped.

    Baseline at production-format-sketch-03 commit (2026-04-19):
    7 KnowledgeEffects with remove=True. A future encoding-side
    refactor per identity-and-realization-sketch-01 §Prior
    encoding's workaround, and its retirement drives the count
    to 0."""
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


def test_dispositions_resolution_paths():
    """Meta-test: each Description disposition this test
    recognizes must be documented in
    production-format-sketch-01.md."""
    sketch_path = (
        _repo_root() / "design" / "production-format-sketch-01.md"
    )
    content = sketch_path.read_text()
    assert "authoring-note" in content, (
        "disposition 'authoring-note' not documented in "
        "production-format-sketch-01.md"
    )
    assert "superseded" in content, (
        "disposition 'superseded' not documented in "
        "production-format-sketch-01.md"
    )


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
