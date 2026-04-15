# story — computational storytelling engine

A research and design notebook for a storytelling engine based on a multi-layered architectural stack. The project aims to bridge the gap between high-level narrative structure (Dramatica, Aristotelian poetics) and a formal, tri-temporal world-state "substrate."

## Project Overview

The "story" project implements a modular stack for narrative generation and analysis:

1.  **Substrate:** The base layer (sink) that tracks events, propositions, and agent knowledge across three time dimensions:
    - **τ_s (Story Time):** The sequence of events within the story world (fabula).
    - **τ_a (Author Time):** The sequence of authorial revisions and additions.
    - **τ_d (Discourse Time):** The order in which facts are disclosed to the reader (sjuzhet).
2.  **Dramatic Dialect:** An upper-layer dialect for high-level narrative structure, featuring Arguments, Throughlines (roles), Scenes, Beats, and Stakes. It is influenced by Dramatica but remains theory-agnostic.
3.  **Lowering & Verification:** A connective layer that maps high-level narrative records to concrete substrate facts (Realization) and verifies their consistency via automated checks (Characterization, Claims).
4.  **Inference Model:** A query-time derivation engine using Horn-clause rules to compute complex story predicates (e.g., "parricide", "incest") from simple, authored facts.
5.  **Reader Model:** An interpretive layer that bridges the "description surface" (unstructured text) and the formal substrate using LLMs (Anthropic Claude) or human feedback.

## Repository Structure

- `design/`: Architectural sketches (`{topic}-sketch-NN.md`). Active sketches are self-contained; old ones are preserved and marked as superseded.
- `prototype/`: Python 3.12 reference implementation. Written as an "executable specification" for maximum portability.
- `research/`: Survey notes on existing narrative theories (`theories/`) and computational systems (`systems/`).
- `AGENTS.md`: Specific guidelines for AI agents interacting with this repository.

## Building and Running

The project consists of Markdown documentation and Python prototypes.

### Prerequisites
- Python 3.12+
- (Optional) Anthropic API Key for the reader-model probe.

### Core Prototypes
Navigate to the `prototype/` directory to run the demos and tests:

```sh
cd prototype

# Demos
python3 demo.py                  # Oedipus Rex: dramatic irony and anagnorisis report
python3 demo_rashomon.py         # Rashomon: matrix of contested branches and testimonies

# Tests (Standard Library only)
python3 test_substrate.py        # Core substrate invariants
python3 test_inference.py        # Inference engine and rule derivation
python3 test_dramatic.py         # Dramatic dialect and M8 verifier
python3 test_lowering.py         # Lowering records and staleness tracking
python3 test_verification.py     # Verifier primitives (Characterization, etc.)

# Reader Model (Requires dependencies and API key)
pip install -r requirements.txt
python3 demo_reader_model.py --dry-run  # Print the reader-model prompt without calling API
python3 demo_reader_model.py --walk     # Interactive authorial walker over LLM proposals
```

## Development Conventions

- **Design First:** Major architectural changes must be drafted as a Markdown sketch in `design/` before implementation.
- **Sketch Immutability:** Never overwrite a superseded sketch; mark it as `Status: superseded` and link to its successor.
- **Plain Markdown:** Use lowercase, hyphenated filenames and follow the templates in `research/`.
- **Executable Specification:** Prototype code (`prototype/*.py`) should prioritize clarity and portability. Avoid complex Python-specific idioms (metaclasses, decorators) to ensure it can be easily ported to C#, Rust, or Go.
- **Verification Over Refactoring:** The "quality control" for research entries is editorial. Ensure links are correct and index tables in READMEs are updated.
- **No Test Frameworks:** Use plain `assert` statements and minimal test runners to keep the prototype dependency-free.

## Key Files

- `design/architecture-sketch-02.md`: The multi-dialect stack architecture.
- `design/substrate-sketch-05.md`: The current substrate specification.
- `prototype/substrate.py`: The core substrate implementation.
- `prototype/dramatic.py`: The Dramatic dialect implementation.
- `prototype/lowering.py`: The cross-dialect mapping machinery.
- `AGENTS.md`: Mandatory reading for any AI assistant working in this repo.
