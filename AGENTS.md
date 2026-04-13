# Repository Guidelines

## Project Structure & Module Organization

This repository is a research and design notebook for a story-telling engine. Top-level files are minimal; most work lives in:

- `research/theories/`: long-form survey notes on narrative theories such as `three-act.md` and `dramatica.md`
- `research/systems/`: survey notes on computational narrative systems such as `tale-spin.md` and `facade.md`
- `design/`: architectural sketches such as `substrate-sketch-01.md`

Use one Markdown file per theory, system, or design sketch. Cross-cutting notes belong in the relevant `README.md`, not scattered across individual entries.

## Build, Test, and Development Commands

There is no compiled build or automated test suite in this repo. The core workflow is editing and reviewing Markdown:

- `rg --files`: list repository files quickly
- `sed -n '1,160p' research/README.md`: inspect local guidance before editing
- `git diff --stat`: review scope before committing
- `git diff`: verify wording, links, and formatting changes

If you use a Markdown linter or previewer locally, keep output clean, but do not add tool-specific config unless requested.

## Coding Style & Naming Conventions

Write in plain Markdown with short sections and explicit headings. Match the existing tone: analytical, direct, and skeptical rather than promotional.

- Use lowercase, hyphenated filenames such as `campbell-monomyth.md`
- Name design sketches `{topic}-sketch-NN.md`
- Keep old sketches; mark them as superseded instead of overwriting
- Prefer primary sources and clearly label tentative claims

When adding new research entries, start from `research/theories/_template.md` or `research/systems/_template.md`.

## Testing Guidelines

Quality control here is editorial. Before submitting changes:

- confirm links and paths are correct
- check that new entries follow the relevant template sections
- verify claims against primary sources where possible
- make sure index tables in `research/theories/README.md` or `research/systems/README.md` are updated when adding entries

## Commit & Pull Request Guidelines

Recent history uses short, imperative commit subjects like `Expand survey: add Aristotle, Propp, Dramatica, MINSTREL, MEXICA`. Follow that pattern.

Pull requests should explain:

- what documents were added or revised
- whether claims are primary-source-backed or still tentative
- any new index entries, cross-references, or superseded design sketches
