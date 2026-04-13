# Design

Architectural sketches and design notes for the story-telling engine. Each sketch is numbered and dated; revisions do not overwrite predecessors. Old sketches are left in place as a record of how the design changed, so we can see our own reasoning over time.

## Convention

- Files named `{topic}-sketch-NN.md` where NN is sequential per topic.
- Every sketch has a **Status** (*draft*, *revised*, *superseded*, *abandoned*) and a **Date** at the top.
- When a sketch is superseded, its status is updated and a link to the successor is added — but the file stays.
- Sketches are not specifications. They are the design thinking in progress. Claims and commitments may be wrong. Open questions are first-class.

## Current sketches

- [Substrate — sketch 01](substrate-sketch-01.md) *(superseded by 02)* — the event-log + per-agent-knowledge-projection substrate that emerged as the convergent architectural commitment of the research survey.
- [Substrate — sketch 02](substrate-sketch-02.md) — delta revising T1 (ambiguity-tolerant fabula), K2 (same algebra, different update operators for reader vs. characters), and the library claim (prescriptive structures operate over fabula and sjuzhet both). Adds three open questions missed in sketch 01: explicit causality, event granularity, focalization/narrator layer.
