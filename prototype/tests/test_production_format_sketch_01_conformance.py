"""
test_production_format_sketch_01_conformance.py — conformance of
the Python prototype's Description records to the canonical
spec in schema/description.json.

Specified by design/production-format-sketch-01.md PFS4. The test
validates every existing encoding's DESCRIPTIONS tuple against
the schema; failures either match a known disposition (documented
below) or fail loud as new findings needing attention.

The test is the **first consumer** of the schemas outside Python.
It proves: a JSON Schema validator written in any language can
read schema/description.json and produce conformance verdicts
against records the Python prototype authored. The Python
prototype is unchanged by this test.

PFS2 discipline applies: the test module reads the Python
prototype (for dump-and-validate) but the **schema** was authored
from design sketches alone. When a conformance failure surfaces
that the schema's enum doesn't accept a value the Python emits,
the disposition is either "amend the design sketch" or "Python
over-specified" — NOT "expand the schema to fit Python".

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
except ImportError as exc:
    raise ImportError(
        "This test requires jsonschema. Install via "
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


def _discover_encoding_descriptions() -> list:
    """Return list of (encoding_module_name, descriptions_list)
    tuples. Discovers encodings under
    prototype/story_engine/encodings/ that define a DESCRIPTIONS
    attribute (the naming convention across the current corpus)."""
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
        descriptions = getattr(module, "DESCRIPTIONS", None)
        if descriptions is None:
            continue
        if not descriptions:
            # An empty DESCRIPTIONS list has nothing to validate;
            # skip silently.
            continue
        out.append((name, list(descriptions)))
    return out


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


def test_schema_file_metaschema_valid():
    """The schema itself is a valid JSON Schema 2020-12 document."""
    schema = _load_description_schema()
    Draft202012Validator.check_schema(schema)


def test_schema_has_expected_shape():
    """Spot-check of schema structure — guards against accidental
    breakage of the schema during unrelated edits."""
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
    """Meta-test: each disposition this test recognizes must be
    documented in production-format-sketch-01.md. Check by
    substring presence of the disposition name in the sketch
    file."""
    sketch_path = (
        _repo_root() / "design" / "production-format-sketch-01.md"
    )
    content = sketch_path.read_text()
    # Sketch should mention each disposition by its value string
    assert "authoring-note" in content, (
        "disposition 'authoring-note' not documented in "
        "production-format-sketch-01.md"
    )
    assert "superseded" in content, (
        "disposition 'superseded' not documented in "
        "production-format-sketch-01.md"
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
