"""
conformance.py — corpus audits for encoding referential integrity.

Factored out of
`prototype/tests/test_production_format_sketch_01_conformance.py`
per the "factor working parts" discipline. Each audit function
returns an `AuditReport` carrying structured findings + pre-
formatted report lines. Test wrappers call `audit_*()`, print the
report, and assert `report.is_clean()`. Other callers (future
tooling, walkers, pre-commit hooks) get the same surface.

Audit kinds landed (per referential-integrity-sketch-01 RI7 +
referential-integrity-sketch-02 RI9–RI14):

- `audit_branch_labels`  — every Event.branches label resolves in
  ALL_BRANCHES (plus implicit canonical). Closes PFS5 OQ3.
- `audit_aristotelian_event_refs` — every ArMythos / ArPhase
  event-id resolves in the paired substrate FABULA/EVENTS_ALL.
  Closes PFS6 OQ3.
- `audit_save_the_cat_intra_story` — every StcStory / StcBeat /
  StcStrand intra-encoding id resolves. Closes PFS7 OQ4.
- `audit_cross_dialect_refs` — every CrossDialectRef on Lowering /
  VerificationReview / StructuralAdvisory /
  VerificationAnswerProposal records resolves in the paired
  encoding's authored-id set, with §D1 dispositions. Closes
  PFS10 OQ1.
- `audit_character_ref_ids` — every ArCharacter.character_ref_id
  resolves in substrate Entity ids ∪ Dramatic Character ids per
  the multi-dialect fallback (A5). Closes PFS6 OQ4.

**Not** factored here: `test_knowledge_effect_remove_audit`, which
is operational/informational (prints a corpus count against a
documented baseline; no clean-or-findings semantic).

Discovery helpers walk `prototype/story_engine/encodings/*.py`
dynamically. Adding a new encoding is automatic. Adding a new
audit kind: follow one of the existing function shapes; return
`AuditReport`.

Per sketch-02 §Dispositions D1: `AXIS_LABEL_DISPOSITIONS` lists
two (dialect, record_id) tuples emitted by dramatica-complete
verifiers that the audit accepts without resolution. The
disposition retires when the paired records are authored (see
PFS6 OQ2).
"""

from __future__ import annotations

import importlib
import pathlib
from dataclasses import dataclass, field


# ============================================================================
# Constants — shared across audits
# ============================================================================


DIALECT_TOKEN_SUFFIX: dict = {
    "substrate": "",                  # paired substrate module is {work} itself
    "dramatic": "_dramatic",
    "save-the-cat": "_save_the_cat",
    "dramatica-complete": "_dramatica_complete",
    "aristotelian": "_aristotelian",
}


# Per referential-integrity-sketch-02 §Dispositions D1:
# dramatica-complete verifiers use these two axis-label tokens as
# target_record.record_id rather than pointers to authored records.
# Reversal path: dramatic-sketch-02 per PFS6 OQ2 may author these
# as DynamicStoryPoint records, at which point the disposition
# retires.
AXIS_LABEL_DISPOSITIONS: frozenset = frozenset({
    ("dramatica-complete", "Story_goal"),
    ("dramatica-complete", "Story_consequence"),
})


# ============================================================================
# Audit output records
# ============================================================================


@dataclass(frozen=True)
class AuditFinding:
    """One unresolved reference. `summary` is a pre-formatted
    human-readable line for printing; `detail` is the structured
    payload for downstream tooling (schema varies per audit kind)."""
    summary: str
    detail: dict = field(default_factory=dict)


@dataclass(frozen=True)
class AuditReport:
    """Result of one audit run. Tests print `report_lines` and
    assert `is_clean()`. Tooling consumers read `findings` +
    `stats` directly."""
    name: str
    findings: tuple = ()              # tuple[AuditFinding, ...]
    stats: dict = field(default_factory=dict)
    report_lines: tuple = ()          # tuple[str, ...]

    def is_clean(self) -> bool:
        return len(self.findings) == 0

    def failure_message(self) -> str:
        return (
            f"{len(self.findings)} unresolved {self.name} "
            f"reference(s); see output. Resolve per referential-"
            f"integrity-sketch-01 RI6 dispositions protocol."
        )

    def print_report(self) -> None:
        for line in self.report_lines:
            print(line)


# ============================================================================
# Encoding discovery (dynamic — walks prototype/story_engine/encodings/)
# ============================================================================


def _repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[3]


def _encodings_dir() -> pathlib.Path:
    return _repo_root() / "prototype" / "story_engine" / "encodings"


def _iter_encoding_modules(glob: str = "*.py"):
    """Yield (name, module) for each importable encoding module
    matching `glob`. Modules starting with `_` are skipped. Import
    failures are swallowed (partial corpora don't break audits)."""
    for py_path in sorted(_encodings_dir().glob(glob)):
        name = py_path.stem
        if name.startswith("_"):
            continue
        try:
            module = importlib.import_module(
                f"story_engine.encodings.{name}"
            )
        except Exception:
            continue
        yield name, module


def _discover_encoding_records(attribute_name: str) -> list:
    out: list = []
    for name, module in _iter_encoding_modules():
        records = getattr(module, attribute_name, None)
        if records is None or not records:
            continue
        out.append((name, list(records)))
    return out


def _discover_encoding_events() -> list:
    from_fabula = _discover_encoding_records("FABULA")
    seen = {name for name, _ in from_fabula}
    from_events_all = [
        (name, events) for name, events
        in _discover_encoding_records("EVENTS_ALL")
        if name not in seen
    ]
    return from_fabula + from_events_all


def _discover_encoding_aristotelian_records():
    """Returns triple `(mythoi, phases, characters)` of
    (encoding_name, list) pairs. Deduplicates by id within an
    encoding (Rashomon exports both singletons and a tuple of the
    same mythoi)."""
    from story_engine.core.aristotelian import ArMythos
    mythoi_out: list = []
    phases_out: list = []
    chars_out: list = []
    for name, module in _iter_encoding_modules():
        mythoi_seen: dict = {}
        for attr_name in dir(module):
            if not attr_name.startswith("AR_"):
                continue
            value = getattr(module, attr_name, None)
            if isinstance(value, ArMythos):
                mythoi_seen[value.id] = value
            elif (
                isinstance(value, tuple) and value
                and all(isinstance(v, ArMythos) for v in value)
            ):
                for v in value:
                    mythoi_seen[v.id] = v
        mythoi = list(mythoi_seen.values())
        if not mythoi:
            continue
        mythoi_out.append((name, mythoi))
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
    """Returns quadruple `(stories, beats, strands, characters)` of
    (encoding_name, list) pairs. Only walks `*_save_the_cat.py`
    base encodings — sibling `*_lowerings.py` / `*_verification.py`
    re-exports are skipped."""
    from story_engine.core.save_the_cat import (
        StcStory, StcBeat, StcStrand, StcCharacter,
    )
    stories_out: list = []
    beats_out: list = []
    strands_out: list = []
    chars_out: list = []
    for name, module in _iter_encoding_modules("*_save_the_cat.py"):
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


def _discover_encoding_lowerings() -> list:
    from story_engine.core.lowering import Lowering
    out: list = []
    for name, module in _iter_encoding_modules("*_lowerings.py"):
        lowerings = getattr(module, "LOWERINGS", None)
        if lowerings is None or not lowerings:
            continue
        if not all(isinstance(lw, Lowering) for lw in lowerings):
            continue
        out.append((name, list(lowerings)))
    return out


def _discover_encoding_verifier_output():
    """Runs each `*_verification.py` module's `run()` function and
    classifies the returned records by type into four lists.
    Returns quadruple `(reviews, advisories, proposals,
    commentaries)` of (encoding_name, records) pairs."""
    from story_engine.core.verification import (
        VerificationReview, StructuralAdvisory,
        VerificationAnswerProposal, VerifierCommentary,
    )
    reviews_out: list = []
    advisories_out: list = []
    proposals_out: list = []
    commentaries_out: list = []
    for name, module in _iter_encoding_modules("*_verification.py"):
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
# Dialect-resolution helpers (RI9, RI10, RI11)
# ============================================================================


def work_from_lowerings_module(name: str) -> str:
    """Per RI11. Strip `_lowerings` suffix; if what remains ends in
    a dialect qualifier (currently `_save_the_cat`), strip that too.
    Example: `ackroyd_save_the_cat_lowerings` → `ackroyd`."""
    if name.endswith("_lowerings"):
        name = name[: -len("_lowerings")]
    for suffix in ("_save_the_cat",):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    return name


def work_from_verification_module(name: str) -> str:
    """Per RI11 for `*_verification.py` modules. Strip suffixes
    in the fixed order: `_verification`, then one of
    `_dramatica_complete` / `_save_the_cat`."""
    if name.endswith("_verification"):
        name = name[: -len("_verification")]
    for suffix in ("_dramatica_complete", "_save_the_cat"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    return name


def collect_dialect_record_ids(work: str, dialect_token: str) -> tuple:
    """Per RI10. Returns `(expected_module_name, id_set)`; id_set is
    None if the module can't be imported (caller reports missing-
    module context).

    Id-collection walks module-level tuple/list attributes whose
    elements carry an `.id` attribute, plus module-level singletons
    with `.id`. The walk is dialect-agnostic. Known non-record
    constants (`GENRES`, `CANONICAL_BEATS`) are excluded."""
    suffix = DIALECT_TOKEN_SUFFIX.get(dialect_token)
    if suffix is None:
        return (f"<unknown-dialect-token:{dialect_token}>", None)
    module_name = work + suffix
    try:
        module = importlib.import_module(
            f"story_engine.encodings.{module_name}"
        )
    except Exception:
        return (module_name, None)

    id_set: set = set()
    for attr_name in dir(module):
        if attr_name.startswith("_"):
            continue
        if attr_name in ("GENRES", "CANONICAL_BEATS"):
            continue
        value = getattr(module, attr_name, None)
        if value is None:
            continue
        if isinstance(value, (tuple, list)) and value:
            if all(hasattr(v, "id") and isinstance(v.id, str) for v in value):
                id_set.update(v.id for v in value)
        elif hasattr(value, "id") and isinstance(
            getattr(value, "id"), str
        ):
            id_set.add(value.id)
    return (module_name, id_set)


# ============================================================================
# Audit: branch labels (RI7 #1)
# ============================================================================


def audit_branch_labels() -> AuditReport:
    """Every Event.branches label resolves in the encoding's
    ALL_BRANCHES dict (plus the implicit CANONICAL_LABEL)."""
    from story_engine.core.substrate import CANONICAL_LABEL

    events_by_encoding = _discover_encoding_events()
    total_refs = 0
    total_events = 0
    clean_events = 0
    findings: list = []
    encodings_covered: list = []

    for encoding_name, events in events_by_encoding:
        try:
            module = importlib.import_module(
                f"story_engine.encodings.{encoding_name}"
            )
        except Exception:
            continue
        all_branches = getattr(module, "ALL_BRANCHES", None)
        if all_branches is None:
            continue
        target_set = set(all_branches.keys())
        target_set.add(CANONICAL_LABEL)
        encodings_covered.append(encoding_name)

        for event in events:
            total_events += 1
            event_clean = True
            for label in event.branches:
                total_refs += 1
                if label not in target_set:
                    event_clean = False
                    findings.append(AuditFinding(
                        summary=(
                            f"{encoding_name}: Event {event.id!r} "
                            f".branches → {label!r} (not in "
                            f"ALL_BRANCHES; target-set size "
                            f"{len(target_set)})"
                        ),
                        detail={
                            "encoding": encoding_name,
                            "event_id": event.id,
                            "field": "branches",
                            "unresolved_ref": label,
                            "target_set_size": len(target_set),
                        },
                    ))
            if event_clean:
                clean_events += 1

    lines: list = [
        "",
        f"audit_branch_labels: {total_events} Events carrying "
        f"{total_refs} branch-label references",
        f"  clean events:               {clean_events}",
        f"  encodings audited:          {len(encodings_covered)}",
    ]
    if findings:
        lines.append(f"  unresolved references:      {len(findings)}")
        for f in findings:
            lines.append(f"    {f.summary}")

    return AuditReport(
        name="branch-label",
        findings=tuple(findings),
        stats={
            "total_events": total_events,
            "clean_events": clean_events,
            "total_refs": total_refs,
            "encodings_audited": len(encodings_covered),
        },
        report_lines=tuple(lines),
    )


# ============================================================================
# Audit: Aristotelian event refs (RI7 #2)
# ============================================================================


def audit_aristotelian_event_refs() -> AuditReport:
    """Every ArMythos and ArPhase event-id resolves to an Event
    id in the paired substrate encoding. Pairing:
    `{work}_aristotelian` ↔ `{work}`."""
    mythoi_by_encoding, _, _ = _discover_encoding_aristotelian_records()
    total_refs = 0
    total_records = 0
    clean_records = 0
    findings: list = []
    encodings_covered: list = []

    for encoding_name, mythoi in mythoi_by_encoding:
        if not encoding_name.endswith("_aristotelian"):
            findings.append(AuditFinding(
                summary=(
                    f"{encoding_name}: <discovery> .<naming> → "
                    f"encoding name does not end in '_aristotelian' "
                    f"— cannot derive substrate pair"
                ),
                detail={
                    "encoding": encoding_name,
                    "record_id": "<discovery>",
                    "field": "<naming>",
                },
            ))
            continue
        substrate_name = encoding_name[: -len("_aristotelian")]
        try:
            substrate_module = importlib.import_module(
                f"story_engine.encodings.{substrate_name}"
            )
        except Exception as exc:
            findings.append(AuditFinding(
                summary=(
                    f"{encoding_name}: <discovery> "
                    f".<substrate-import> → cannot import paired "
                    f"substrate {substrate_name!r}: {exc}"
                ),
                detail={
                    "encoding": encoding_name,
                    "record_id": "<discovery>",
                    "field": "<substrate-import>",
                    "reason": str(exc),
                },
            ))
            continue

        substrate_events: list = []
        fabula = getattr(substrate_module, "FABULA", None)
        if fabula is not None:
            substrate_events = list(fabula)
        else:
            events_all = getattr(substrate_module, "EVENTS_ALL", None)
            if events_all is not None:
                substrate_events = list(events_all)
        target_set = {e.id for e in substrate_events}
        encodings_covered.append(
            f"{encoding_name} → {substrate_name} "
            f"({len(target_set)} events)"
        )

        for mythos in mythoi:
            total_records += 1
            mythos_clean = True
            for ev_id in mythos.central_event_ids:
                total_refs += 1
                if ev_id not in target_set:
                    mythos_clean = False
                    findings.append(AuditFinding(
                        summary=(
                            f"{encoding_name}: {mythos.id} "
                            f".central_event_ids → {ev_id!r} (not "
                            f"in substrate target-set of size "
                            f"{len(target_set)})"
                        ),
                        detail={
                            "encoding": encoding_name,
                            "record_id": mythos.id,
                            "field": "central_event_ids",
                            "unresolved_ref": ev_id,
                            "target_set_size": len(target_set),
                        },
                    ))
            for field_name in (
                "complication_event_id", "denouement_event_id",
                "peripeteia_event_id", "anagnorisis_event_id",
            ):
                ev_id = getattr(mythos, field_name)
                if ev_id is None:
                    continue
                total_refs += 1
                if ev_id not in target_set:
                    mythos_clean = False
                    findings.append(AuditFinding(
                        summary=(
                            f"{encoding_name}: {mythos.id} "
                            f".{field_name} → {ev_id!r} (not in "
                            f"substrate target-set of size "
                            f"{len(target_set)})"
                        ),
                        detail={
                            "encoding": encoding_name,
                            "record_id": mythos.id,
                            "field": field_name,
                            "unresolved_ref": ev_id,
                            "target_set_size": len(target_set),
                        },
                    ))
            if mythos_clean:
                clean_records += 1

            for phase in mythos.phases:
                total_records += 1
                phase_clean = True
                for ev_id in phase.scope_event_ids:
                    total_refs += 1
                    if ev_id not in target_set:
                        phase_clean = False
                        findings.append(AuditFinding(
                            summary=(
                                f"{encoding_name}: "
                                f"{mythos.id}.phases[{phase.id}] "
                                f".scope_event_ids → {ev_id!r} "
                                f"(not in substrate target-set of "
                                f"size {len(target_set)})"
                            ),
                            detail={
                                "encoding": encoding_name,
                                "record_id": (
                                    f"{mythos.id}.phases[{phase.id}]"
                                ),
                                "field": "scope_event_ids",
                                "unresolved_ref": ev_id,
                                "target_set_size": len(target_set),
                            },
                        ))
                if phase_clean:
                    clean_records += 1

    lines: list = [
        "",
        f"audit_aristotelian_event_refs: {total_records} Aristotelian "
        f"records carrying {total_refs} event-id references",
        f"  clean records:              {clean_records}",
        f"  encodings audited:",
    ]
    for entry in encodings_covered:
        lines.append(f"    {entry}")
    if findings:
        lines.append(f"  unresolved references:      {len(findings)}")
        for f in findings:
            lines.append(f"    {f.summary}")

    return AuditReport(
        name="Aristotelian event-id",
        findings=tuple(findings),
        stats={
            "total_records": total_records,
            "clean_records": clean_records,
            "total_refs": total_refs,
            "encodings_audited": encodings_covered,
        },
        report_lines=tuple(lines),
    )


# ============================================================================
# Audit: Save-the-Cat intra-story (RI7 #3)
# ============================================================================


def audit_save_the_cat_intra_story() -> AuditReport:
    """Every Save-the-Cat id reference resolves to a sibling
    record in the same encoding module. Audited fields:
    StcStory.{beat_ids, strand_ids, character_ids,
    archetype_assignments[].character_id}, StcBeat.participant_ids,
    StcBeat.advances[].strand_id, StcStrand.focal_character_id."""
    stories_by_encoding, beats_by_encoding, strands_by_encoding, \
        characters_by_encoding = _discover_encoding_save_the_cat_records()

    beats_index = {
        name: {b.id for b in beats}
        for name, beats in beats_by_encoding
    }
    strands_index = {
        name: {s.id for s in strands}
        for name, strands in strands_by_encoding
    }
    characters_index = {
        name: {c.id for c in chars}
        for name, chars in characters_by_encoding
    }

    total_refs = 0
    total_records = 0
    clean_records = 0
    findings: list = []
    encodings_covered: list = []

    def _finding(encoding, record_id, field_name, ref, target_size):
        findings.append(AuditFinding(
            summary=(
                f"{encoding}: {record_id!r} .{field_name} → "
                f"{ref!r} (not in target-set of size {target_size})"
            ),
            detail={
                "encoding": encoding,
                "record_id": record_id,
                "field": field_name,
                "unresolved_ref": ref,
                "target_set_size": target_size,
            },
        ))

    for encoding_name, stories in stories_by_encoding:
        beat_ids = beats_index.get(encoding_name, set())
        strand_ids = strands_index.get(encoding_name, set())
        character_ids = characters_index.get(encoding_name, set())
        encodings_covered.append(
            f"{encoding_name} "
            f"({len(beat_ids)} beats / {len(strand_ids)} strands / "
            f"{len(character_ids)} characters)"
        )

        for story in stories:
            total_records += 1
            story_clean = True
            for bid in story.beat_ids:
                total_refs += 1
                if bid not in beat_ids:
                    story_clean = False
                    _finding(encoding_name, story.id, "beat_ids",
                             bid, len(beat_ids))
            for sid in story.strand_ids:
                total_refs += 1
                if sid not in strand_ids:
                    story_clean = False
                    _finding(encoding_name, story.id, "strand_ids",
                             sid, len(strand_ids))
            for cid in story.character_ids:
                total_refs += 1
                if cid not in character_ids:
                    story_clean = False
                    _finding(encoding_name, story.id, "character_ids",
                             cid, len(character_ids))
            for aa in story.archetype_assignments:
                if aa.character_id is None:
                    continue
                total_refs += 1
                if aa.character_id not in character_ids:
                    story_clean = False
                    _finding(
                        encoding_name, story.id,
                        (f"archetype_assignments[{aa.archetype}]"
                         f".character_id"),
                        aa.character_id, len(character_ids),
                    )
            if story_clean:
                clean_records += 1

        beats_for_encoding = dict(beats_by_encoding).get(encoding_name, [])
        for beat in beats_for_encoding:
            total_records += 1
            beat_clean = True
            for cid in beat.participant_ids:
                total_refs += 1
                if cid not in character_ids:
                    beat_clean = False
                    _finding(encoding_name, beat.id, "participant_ids",
                             cid, len(character_ids))
            for adv in beat.advances:
                total_refs += 1
                if adv.strand_id not in strand_ids:
                    beat_clean = False
                    _finding(
                        encoding_name, beat.id,
                        f"advances[{adv.strand_id}].strand_id",
                        adv.strand_id, len(strand_ids),
                    )
            if beat_clean:
                clean_records += 1

        strands_for_encoding = dict(strands_by_encoding).get(
            encoding_name, []
        )
        for strand in strands_for_encoding:
            total_records += 1
            strand_clean = True
            if strand.focal_character_id is not None:
                total_refs += 1
                if strand.focal_character_id not in character_ids:
                    strand_clean = False
                    _finding(
                        encoding_name, strand.id,
                        "focal_character_id",
                        strand.focal_character_id, len(character_ids),
                    )
            if strand_clean:
                clean_records += 1

    lines: list = [
        "",
        f"audit_save_the_cat_intra_story: {total_records} "
        f"Save-the-Cat records carrying {total_refs} id references",
        f"  clean records:              {clean_records}",
        f"  encodings audited:",
    ]
    for entry in encodings_covered:
        lines.append(f"    {entry}")
    if findings:
        lines.append(f"  unresolved references:      {len(findings)}")
        for f in findings:
            lines.append(f"    {f.summary}")

    return AuditReport(
        name="Save-the-Cat id",
        findings=tuple(findings),
        stats={
            "total_records": total_records,
            "clean_records": clean_records,
            "total_refs": total_refs,
            "encodings_audited": encodings_covered,
        },
        report_lines=tuple(lines),
    )


# ============================================================================
# Audit: CrossDialectRef resolution (RI9–RI12)
# ============================================================================


def audit_cross_dialect_refs() -> AuditReport:
    """Every CrossDialectRef on Lowering / VerificationReview /
    StructuralAdvisory / VerificationAnswerProposal records
    resolves to an existing record-id in the paired encoding.
    Per §Dispositions D1, a small fixed set of axis-label tokens
    is accepted without resolution."""
    lowerings_by_encoding = _discover_encoding_lowerings()
    reviews_by_encoding, advisories_by_encoding, \
        proposals_by_encoding, _ = _discover_encoding_verifier_output()

    cache: dict = {}

    def lookup(work: str, dialect_token: str):
        key = (work, dialect_token)
        if key not in cache:
            cache[key] = collect_dialect_record_ids(work, dialect_token)
        return cache[key]

    findings: list = []
    total_refs = 0
    resolved_refs = 0
    dispositioned_refs = 0
    sources_audited = 0

    def audit_ref(source_kind: str, source_module: str,
                  source_record_id: str, field_name: str,
                  ref, work: str):
        nonlocal total_refs, resolved_refs, dispositioned_refs
        total_refs += 1
        if (ref.dialect, ref.record_id) in AXIS_LABEL_DISPOSITIONS:
            dispositioned_refs += 1
            return
        module_name, id_set = lookup(work, ref.dialect)
        if id_set is None:
            findings.append(AuditFinding(
                summary=(
                    f"{source_kind} in {source_module}: "
                    f"{source_record_id!r} .{field_name} → "
                    f"({ref.dialect!r}, {ref.record_id!r}): paired "
                    f"module {module_name!r} cannot be loaded"
                ),
                detail={
                    "source_kind": source_kind,
                    "source_module": source_module,
                    "source_record_id": source_record_id,
                    "field": field_name,
                    "dialect": ref.dialect,
                    "record_id": ref.record_id,
                    "reason": (
                        f"paired module {module_name!r} cannot be loaded"
                    ),
                },
            ))
            return
        if ref.record_id not in id_set:
            findings.append(AuditFinding(
                summary=(
                    f"{source_kind} in {source_module}: "
                    f"{source_record_id!r} .{field_name} → "
                    f"({ref.dialect!r}, {ref.record_id!r}): not in "
                    f"{module_name!r} authored-id set "
                    f"(size {len(id_set)})"
                ),
                detail={
                    "source_kind": source_kind,
                    "source_module": source_module,
                    "source_record_id": source_record_id,
                    "field": field_name,
                    "dialect": ref.dialect,
                    "record_id": ref.record_id,
                    "reason": (
                        f"not in {module_name!r} authored-id set "
                        f"(size {len(id_set)})"
                    ),
                },
            ))
        else:
            resolved_refs += 1

    for encoding_name, lowerings in lowerings_by_encoding:
        work = work_from_lowerings_module(encoding_name)
        for lw in lowerings:
            sources_audited += 1
            audit_ref("Lowering", encoding_name, lw.id, "upper_record",
                      lw.upper_record, work)
            for i, lr in enumerate(lw.lower_records):
                audit_ref("Lowering", encoding_name, lw.id,
                          f"lower_records[{i}]", lr, work)

    for encoding_name, reviews in reviews_by_encoding:
        work = work_from_verification_module(encoding_name)
        for review in reviews:
            sources_audited += 1
            audit_ref("VerificationReview", encoding_name,
                      review.reviewer_id, "target_record",
                      review.target_record, work)

    for encoding_name, advisories in advisories_by_encoding:
        work = work_from_verification_module(encoding_name)
        for advisory in advisories:
            sources_audited += 1
            for i, ref in enumerate(advisory.scope):
                audit_ref("StructuralAdvisory", encoding_name,
                          advisory.advisor_id, f"scope[{i}]",
                          ref, work)

    for encoding_name, proposals in proposals_by_encoding:
        work = work_from_verification_module(encoding_name)
        for proposal in proposals:
            sources_audited += 1
            audit_ref("VerificationAnswerProposal", encoding_name,
                      proposal.proposer_id, "question_id",
                      proposal.question_id, work)

    lines: list = [
        "",
        f"audit_cross_dialect_refs: {sources_audited} source records "
        f"carrying {total_refs} CrossDialectRef references",
        f"  resolved references:        {resolved_refs}",
        f"  dispositioned references:   {dispositioned_refs}",
        f"  modules cached:             {len(cache)}",
    ]
    if findings:
        lines.append(f"  unresolved references:      {len(findings)}")
        for f in findings:
            lines.append(f"    {f.summary}")

    return AuditReport(
        name="CrossDialectRef",
        findings=tuple(findings),
        stats={
            "sources_audited": sources_audited,
            "total_refs": total_refs,
            "resolved_refs": resolved_refs,
            "dispositioned_refs": dispositioned_refs,
            "modules_cached": len(cache),
        },
        report_lines=tuple(lines),
    )


# ============================================================================
# Audit: ArCharacter.character_ref_id (RI13)
# ============================================================================


def audit_character_ref_ids() -> AuditReport:
    """Every ArCharacter.character_ref_id (when set) resolves to
    either a substrate Entity id OR a Dramatic Character id in the
    paired encoding. Multi-dialect fallback per aristotelian-
    sketch-01 A5."""
    _, _, chars_by_encoding = _discover_encoding_aristotelian_records()
    findings: list = []
    total_refs = 0
    resolved_refs = 0
    characters_audited = 0
    encodings_covered: list = []

    for encoding_name, characters in chars_by_encoding:
        if not encoding_name.endswith("_aristotelian"):
            continue
        work = encoding_name[: -len("_aristotelian")]

        try:
            substrate_module = importlib.import_module(
                f"story_engine.encodings.{work}"
            )
        except Exception:
            substrate_module = None
        entity_ids: set = set()
        if substrate_module is not None:
            entities = getattr(substrate_module, "ENTITIES", ())
            entity_ids = {
                e.id for e in entities if hasattr(e, "id")
            }

        try:
            dramatic_module = importlib.import_module(
                f"story_engine.encodings.{work}_dramatic"
            )
        except Exception:
            dramatic_module = None
        dramatic_character_ids: set = set()
        if dramatic_module is not None:
            drams_chars = getattr(dramatic_module, "CHARACTERS", ())
            dramatic_character_ids = {
                c.id for c in drams_chars if hasattr(c, "id")
            }

        target_set = entity_ids | dramatic_character_ids
        encodings_covered.append(
            f"{encoding_name} ({len(entity_ids)} substrate entities "
            f"+ {len(dramatic_character_ids)} dramatic characters "
            f"= {len(target_set)} union)"
        )

        for char in characters:
            characters_audited += 1
            if char.character_ref_id is None:
                continue
            total_refs += 1
            if char.character_ref_id not in target_set:
                findings.append(AuditFinding(
                    summary=(
                        f"{encoding_name}: ArCharacter {char.id!r} "
                        f"character_ref_id={char.character_ref_id!r} "
                        f"(not in substrate+dramatic union of size "
                        f"{len(entity_ids)}+"
                        f"{len(dramatic_character_ids)})"
                    ),
                    detail={
                        "encoding": encoding_name,
                        "character_id": char.id,
                        "character_ref_id": char.character_ref_id,
                        "substrate_set_size": len(entity_ids),
                        "dramatic_set_size": len(dramatic_character_ids),
                    },
                ))
            else:
                resolved_refs += 1

    lines: list = [
        "",
        f"audit_character_ref_ids: {characters_audited} ArCharacter "
        f"records ({total_refs} carrying non-None character_ref_id)",
        f"  resolved references:        {resolved_refs}",
        f"  encodings audited:",
    ]
    for entry in encodings_covered:
        lines.append(f"    {entry}")
    if findings:
        lines.append(f"  unresolved references:      {len(findings)}")
        for f in findings:
            lines.append(f"    {f.summary}")

    return AuditReport(
        name="character_ref_id",
        findings=tuple(findings),
        stats={
            "characters_audited": characters_audited,
            "total_refs": total_refs,
            "resolved_refs": resolved_refs,
            "encodings_audited": encodings_covered,
        },
        report_lines=tuple(lines),
    )
