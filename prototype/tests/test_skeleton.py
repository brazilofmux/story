"""test_skeleton.py — permanent tests for story_engine.tools.skeleton.

Six acceptance checks per design/skeleton-generator-sketch-01.md:

1. CLI writes all 5 files.
2. Each generated file imports cleanly.
3. Generated verifier's run() emits a 'skeletal_encoding' advisory.
4. Re-running without --force fails with a files-exist error.
5. Re-running with --force overwrites.
6. Invalid inputs (bad work-id, empty characters) fail loudly.

Because the generated stubs use absolute imports
(`from story_engine.encodings.{work_id}_dramatic import STORY`),
generation happens into the real story_engine/encodings/ directory
with an underscore-prefixed work-id (`_test_skeleton_smoke`). Each
test uses a try/finally to clean up.

Run: python3 -m tests.test_skeleton
"""
from __future__ import annotations

import importlib
import sys
import traceback
from pathlib import Path

from story_engine.tools import skeleton


# The generated test encoding lives here — underscore-prefix so it
# can't be confused with a real encoding. Name kept stable so cleanup
# can be robust across interrupted runs.
TEST_WORK_ID = "_test_skeleton_smoke"

# Resolve story_engine/encodings path relative to this test file.
_TESTS_DIR = Path(__file__).resolve().parent
_ENCODINGS_DIR = _TESTS_DIR.parent / "story_engine" / "encodings"

TEST_FILENAMES = tuple(
    f"{TEST_WORK_ID}{suffix}" for suffix in (
        ".py",
        "_dramatic.py",
        "_dramatica_complete.py",
        "_lowerings.py",
        "_dramatica_complete_verification.py",
    )
)


def _cleanup():
    """Remove all generated test files. Safe to call multiple times."""
    for name in TEST_FILENAMES:
        path = _ENCODINGS_DIR / name
        if path.exists():
            path.unlink()
    # Drop any imports from sys.modules so re-imports pick up fresh content.
    drop = [
        m for m in sys.modules
        if m.startswith(f"story_engine.encodings.{TEST_WORK_ID}")
    ]
    for m in drop:
        del sys.modules[m]


def _invoke_cli(*extra_args, work_id=TEST_WORK_ID):
    """Call skeleton.main with a minimal valid arg set plus extras."""
    argv = [
        "--work-id", work_id,
        "--title", "Test Skeleton Smoke",
        "--characters", "alice:Alice,bob:Bob",
        "--out-dir", str(_ENCODINGS_DIR),
    ]
    argv.extend(extra_args)
    return skeleton.main(argv)


# ============================================================================
# Tiny test harness (mirrors the rest of prototype/tests/).
# ============================================================================

RESULTS: list[tuple[str, bool, str | None]] = []


def _run(name, fn):
    try:
        fn()
        RESULTS.append((name, True, None))
        print(f"ok    {name}")
    except Exception:
        tb = traceback.format_exc()
        RESULTS.append((name, False, tb))
        print(f"FAIL  {name}")
        print(tb)


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


def test_cli_writes_all_five_files():
    _cleanup()
    try:
        rc = _invoke_cli()
        assert rc == 0, f"expected rc=0, got {rc}"
        for name in TEST_FILENAMES:
            path = _ENCODINGS_DIR / name
            assert path.exists(), f"missing: {path}"
            assert path.stat().st_size > 0, f"empty: {path}"
    finally:
        _cleanup()


def test_generated_files_import_cleanly():
    _cleanup()
    try:
        rc = _invoke_cli()
        assert rc == 0
        # Import each of the 5 generated modules
        mods = [
            f"story_engine.encodings.{TEST_WORK_ID}",
            f"story_engine.encodings.{TEST_WORK_ID}_dramatic",
            f"story_engine.encodings.{TEST_WORK_ID}_dramatica_complete",
            f"story_engine.encodings.{TEST_WORK_ID}_lowerings",
            f"story_engine.encodings.{TEST_WORK_ID}_dramatica_complete_verification",
        ]
        imported = {name: importlib.import_module(name) for name in mods}
        # Sanity: substrate stub exposes ENTITIES with the two characters
        substrate_mod = imported[mods[0]]
        assert [e.id for e in substrate_mod.ENTITIES] == ["alice", "bob"]
        # Dramatic stub has the Story with matching character ids
        dramatic_mod = imported[mods[1]]
        assert dramatic_mod.STORY.character_ids == ("alice", "bob")
        # Template stub has empty DomainAssignments
        template_mod = imported[mods[2]]
        assert template_mod.DOMAIN_ASSIGNMENTS == ()
        # Lowerings stub is empty
        lowerings_mod = imported[mods[3]]
        assert lowerings_mod.LOWERINGS == ()
    finally:
        _cleanup()


def test_generated_verifier_run_emits_skeletal_advisory():
    _cleanup()
    try:
        rc = _invoke_cli()
        assert rc == 0
        verif_mod = importlib.import_module(
            f"story_engine.encodings.{TEST_WORK_ID}_dramatica_complete_verification"
        )
        result = verif_mod.run()
        assert len(result) == 1, f"expected 1 advisory, got {len(result)}"
        advisory = result[0]
        assert advisory.advisor_id == f"skeleton:{TEST_WORK_ID}", \
            f"unexpected advisor_id: {advisory.advisor_id}"
        assert TEST_WORK_ID in advisory.comment
    finally:
        _cleanup()


def test_rerun_without_force_refuses_overwrite():
    _cleanup()
    try:
        rc = _invoke_cli()
        assert rc == 0
        # Second invocation should refuse
        rc2 = _invoke_cli()
        assert rc2 == 2, f"expected rc=2 (refusal), got {rc2}"
        # Files still there and unchanged
        for name in TEST_FILENAMES:
            assert (_ENCODINGS_DIR / name).exists()
    finally:
        _cleanup()


def test_rerun_with_force_overwrites():
    _cleanup()
    try:
        rc = _invoke_cli()
        assert rc == 0
        # Mark first file to detect overwrite
        first_path = _ENCODINGS_DIR / TEST_FILENAMES[0]
        original_size = first_path.stat().st_size
        first_path.write_text("# marker\n", encoding="utf-8")
        assert first_path.stat().st_size != original_size
        # Second invocation with --force should succeed and overwrite
        rc2 = _invoke_cli("--force")
        assert rc2 == 0
        assert first_path.stat().st_size == original_size, \
            "file was not overwritten back to generated content"
    finally:
        _cleanup()


def test_invalid_work_id_rejected():
    _cleanup()
    try:
        rc = _invoke_cli(work_id="BadCaseName")
        assert rc == 2, f"expected rc=2, got {rc}"
        # No files should be written
        for name in TEST_FILENAMES:
            path = _ENCODINGS_DIR / f"BadCaseName{name[len(TEST_WORK_ID):]}"
            assert not path.exists()
    finally:
        _cleanup()


def test_empty_characters_rejected():
    _cleanup()
    try:
        argv = [
            "--work-id", TEST_WORK_ID,
            "--title", "T",
            "--characters", "",
            "--out-dir", str(_ENCODINGS_DIR),
        ]
        rc = skeleton.main(argv)
        assert rc == 2, f"expected rc=2, got {rc}"
    finally:
        _cleanup()


def test_duplicate_character_id_rejected():
    _cleanup()
    try:
        argv = [
            "--work-id", TEST_WORK_ID,
            "--title", "T",
            "--characters", "alice:Alice,alice:Alicia",
            "--out-dir", str(_ENCODINGS_DIR),
        ]
        rc = skeleton.main(argv)
        assert rc == 2, f"expected rc=2, got {rc}"
    finally:
        _cleanup()


def main():
    # Safety: clean up any leftover files before starting
    _cleanup()
    _run("test_cli_writes_all_five_files",
         test_cli_writes_all_five_files)
    _run("test_generated_files_import_cleanly",
         test_generated_files_import_cleanly)
    _run("test_generated_verifier_run_emits_skeletal_advisory",
         test_generated_verifier_run_emits_skeletal_advisory)
    _run("test_rerun_without_force_refuses_overwrite",
         test_rerun_without_force_refuses_overwrite)
    _run("test_rerun_with_force_overwrites",
         test_rerun_with_force_overwrites)
    _run("test_invalid_work_id_rejected",
         test_invalid_work_id_rejected)
    _run("test_empty_characters_rejected",
         test_empty_characters_rejected)
    _run("test_duplicate_character_id_rejected",
         test_duplicate_character_id_rejected)
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    total = len(RESULTS)
    print(f"\n{passed} passed, {total - passed} failed, {total} total")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
