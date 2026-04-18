"""Skeleton generator — ships per design/skeleton-generator-sketch-01.md.

Writes the canonical 5-file stub for a new dramatica-complete
encoding given a work-id, title, and character list.

Usage (from `prototype/`):

    python3 -m story_engine.tools.skeleton \\
        --work-id <snake_case> \\
        --title "<human title>" \\
        --characters "id1:Name1,id2:Name2,..." \\
        [--out-dir <path>] [--force]

Outputs (into --out-dir, default story_engine/encodings/):

    <work-id>.py
    <work-id>_dramatic.py
    <work-id>_dramatica_complete.py
    <work-id>_lowerings.py
    <work-id>_dramatica_complete_verification.py

Sketch commitments honored:
- SG1: tool location, CLI form
- SG2: CLI flags (--work-id, --title, --characters, --out-dir, --force)
- SG3: 5 output files
- SG4: stubs import cleanly; verifier run() emits "skeletal" advisory
- SG5: dramatica-complete only in v1
- SG6: no content invention — characters carry only id + name
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path
from typing import Iterable

from story_engine.tools.skeleton_templates import TEMPLATES


SNAKE_CASE_RE = re.compile(r"^[a-z_][a-z0-9_]*$")
# Character ids (used as Python identifiers in substrate) — must start
# with a lowercase letter. More restrictive than work-id because they
# become module-level names inside generated encoding files.
CHARACTER_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def validate_work_id(work_id: str) -> None:
    if not SNAKE_CASE_RE.match(work_id):
        raise ValueError(
            f"--work-id must be snake_case (lowercase letters / digits / "
            f"underscore, may start with underscore for test / private "
            f"encodings). Got: {work_id!r}"
        )


def parse_characters(spec: str) -> list[tuple[str, str]]:
    """Parse --characters "id1:Name1,id2:Name2,..." into [(id, name), ...].

    Rejects empty specs, duplicate ids, and non-snake_case ids.
    """
    if not spec.strip():
        raise ValueError("--characters may not be empty — at least one required")
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for pair in spec.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if ":" not in pair:
            raise ValueError(
                f"--characters entry must be 'id:Name', got: {pair!r}"
            )
        char_id, name = pair.split(":", 1)
        char_id = char_id.strip()
        name = name.strip()
        if not CHARACTER_ID_RE.match(char_id):
            raise ValueError(
                f"Character id must be snake_case starting with a "
                f"letter, got: {char_id!r}"
            )
        if not name:
            raise ValueError(
                f"Character name may not be empty (id: {char_id!r})"
            )
        if char_id in seen:
            raise ValueError(f"Duplicate character id: {char_id!r}")
        seen.add(char_id)
        out.append((char_id, name))
    if not out:
        raise ValueError("--characters yielded zero characters after parsing")
    return out


def render_entity_constants(characters: list[tuple[str, str]]) -> str:
    """Render Entity(...) assignment lines for the substrate stub."""
    lines = []
    for char_id, name in characters:
        lines.append(
            f'{char_id} = Entity(id="{char_id}", name="{name}", kind="agent")'
        )
    return "\n".join(lines)


def render_character_defs(characters: list[tuple[str, str]]) -> str:
    """Render Character(...) assignment lines for the dramatic stub."""
    lines = []
    for char_id, name in characters:
        lines.append(
            f'C_{char_id} = Character(id="{char_id}", name="{name}")'
        )
    return "\n".join(lines)


def render_character_id_list(
    characters: list[tuple[str, str]], prefix: str = ""
) -> str:
    """Render a comma-separated id list for tuple/list literals.

    `prefix="C_"` for dramatic (references Character bindings);
    `prefix=""` for substrate (references Entity bindings).
    """
    return ", ".join(f"{prefix}{char_id}" for char_id in (c[0] for c in characters))


def render_all(
    work_id: str,
    title: str,
    characters: list[tuple[str, str]],
    date: str | None = None,
) -> dict[str, str]:
    """Render all 5 stub files. Returns {basename_with_work_id_prefix: text}."""
    if date is None:
        date = _dt.date.today().isoformat()

    context_substrate = {
        "work_id": work_id,
        "title": title,
        "date": date,
        "entity_constants": render_entity_constants(characters),
        "character_id_list": render_character_id_list(characters, prefix=""),
    }
    context_dramatic = {
        "work_id": work_id,
        "title": title,
        "date": date,
        "character_defs": render_character_defs(characters),
        "character_id_list": render_character_id_list(characters, prefix="C_"),
    }
    context_minimal = {
        "work_id": work_id,
        "title": title,
        "date": date,
    }

    rendered: dict[str, str] = {}
    for filename_tmpl, body_tmpl in TEMPLATES.items():
        filename = filename_tmpl.format(work_id=work_id)
        if filename == f"{work_id}.py":
            rendered[filename] = body_tmpl.format(**context_substrate)
        elif filename == f"{work_id}_dramatic.py":
            rendered[filename] = body_tmpl.format(**context_dramatic)
        else:
            rendered[filename] = body_tmpl.format(**context_minimal)
    return rendered


def write_files(
    files: dict[str, str], out_dir: Path, force: bool = False
) -> list[Path]:
    """Write rendered files to out_dir. Returns paths written.

    Refuses to overwrite existing files unless force=True (SG2).
    """
    if not out_dir.is_dir():
        raise FileNotFoundError(f"--out-dir does not exist: {out_dir}")
    written: list[Path] = []
    # First pass: check all conflicts before writing anything
    if not force:
        existing = [
            out_dir / name for name in files if (out_dir / name).exists()
        ]
        if existing:
            raise FileExistsError(
                "Refusing to overwrite existing files (use --force to "
                f"overwrite): {', '.join(p.name for p in existing)}"
            )
    # Second pass: write
    for name, text in files.items():
        path = out_dir / name
        path.write_text(text, encoding="utf-8")
        written.append(path)
    return written


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m story_engine.tools.skeleton",
        description=(
            "Generate a 5-file dramatica-complete encoding skeleton. "
            "See design/skeleton-generator-sketch-01.md."
        ),
    )
    parser.add_argument("--work-id", required=True, help="snake_case module prefix")
    parser.add_argument("--title", required=True, help="human-readable title")
    parser.add_argument(
        "--characters",
        required=True,
        help="comma-separated id:Name pairs, e.g. 'sherlock:Sherlock,watson:Watson'",
    )
    parser.add_argument(
        "--out-dir",
        default="story_engine/encodings",
        help="output directory (default: story_engine/encodings)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite existing files (default: refuse)",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        validate_work_id(args.work_id)
        characters = parse_characters(args.characters)
        files = render_all(args.work_id, args.title, characters)
        written = write_files(files, Path(args.out_dir), force=args.force)
    except (ValueError, FileNotFoundError, FileExistsError) as e:
        print(f"skeleton: {e}", file=sys.stderr)
        return 2

    print(f"Wrote {len(written)} files to {args.out_dir}/:")
    for path in written:
        print(f"  {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
