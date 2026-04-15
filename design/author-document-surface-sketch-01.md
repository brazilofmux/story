# Author document surface — sketch 01

**Status:** draft, captured (idea direction; not yet committed to)
**Date:** 2026-04-15
**Supersedes:** nothing
**Frames:** [architecture-sketch-02.md](architecture-sketch-02.md)
**Superseded by:** nothing

## Purpose

Captures an open design direction surfaced 2026-04-15: the author-facing
surface of the engine should *feel like a document*, not like a Python
file, even while the engine itself stays Python.

This is not yet a commitment. The motivation is UX: a `.py` file says
*this is code, leave it to the engineer*; a `.story` or `.md` file says
*this is yours, go ahead.* For a project whose load-bearing goal is to
force creative humans (and LLMs) to do their homework on stories, the
on-ramp matters. The current Python encoding files (`macbeth_dramatic.py`,
`macbeth_lowerings.py`, `macbeth_verification.py`) are nearly-data wearing
Python clothes; the proposal here is a thin author-facing layer on top
that parses INTO those Python records.

## Motivation

The user observed that the existing prototype stack assumes the author
will see Python code and run. For an engineer, that's fine. For a writer
who's never opened a Python file, even a syntactically clean
`Throughline(role_label="main-character", owners=("C_macbeth",), ...)`
is a friction surface: it announces *this is code*, and a writer
naturally assumes that means they shouldn't touch it.

A document-style format — Markdown with fenced declarative blocks, or a
small custom DSL — would shift the perceived ownership boundary. The
content is the author's; the engine just reads what they wrote.

The technical constraint is that the verifier and orchestrator already
work against the Python record kernel and shouldn't change. Whatever
author surface lands has to be *one-directional* (document → records);
the records stay canonical.

## Two candidate shapes

### 1. Markdown with fenced declarative blocks

Author writes a single `macbeth.md` that reads as a story bible. The
prose is the author's commentary; the fenced blocks are the structured
data the engine consumes:

````markdown
# Macbeth — encoded against the Dramatic dialect

The story is an argument that *unchecked ambition unmakes the one who
indulges it*. The MC's arc traces a moral descent in nine beats; the
relationship arc tracks the marriage's trajectory.

```argument id=A_ambition_unmakes
premise = "unchecked ambition unmakes the one who indulges it"
counter_premise = "ambition is what elevates; restraint is mediocre"
resolution_direction = AFFIRM
domain = moral-philosophical
```

```throughline id=T_mc_macbeth
role_label = main-character
owners = [C_macbeth]
subject = the MC's moral descent...
stakes_id = Stakes_macbeth_soul
contributes = [{argument: A_ambition_unmakes, side: AFFIRMS}]
```

The MC throughline lives in nine beats — see `B_mc_1` through `B_mc_9`
below. ...
````

**Pros.** Familiar (every dev who's touched a static site generator has
seen this). Diff-friendly. Comment-friendly: the prose around the blocks
*is* the author's commentary, no separate documentation needed.
Versioning is git as usual.

**Cons.** Yet another schema (the fenced block grammar). The block
grammar will need decisions about how to express tuples, nested objects,
references between records.

**Implementation cost.** Small. Markdown + fenced blocks is well-trodden.
The block contents could be TOML, a tiny key=value grammar, or even raw
JSON5. A parser stub fits in ~200 lines.

### 2. Story-flavored mini-DSL

Author writes one `.story` file per encoding using a story-flavored
indent-based grammar:

```
story "Macbeth" template=dramatica-8

argument A_ambition_unmakes:
    premise "unchecked ambition unmakes the one who indulges it"
    counter "ambition is what elevates; restraint is mediocre"
    resolves AFFIRM in moral-philosophical

throughline T_mc_macbeth role=main-character:
    owners C_macbeth
    subject "the MC's moral descent..."
    stakes Stakes_macbeth_soul
    contributes A_ambition_unmakes AFFIRMS

scene S_prophecy at 1:
    title "The Witches' first prophecy"
    advances T_overall_scotland B_op_1, T_mc_macbeth B_mc_1
    conflict_shape "the supernatural addresses the human..."
    result "Macbeth holds the prophecy..."
```

**Pros.** Cleanest read. Maximally document-feeling. Author doesn't see
braces, equals signs, or quotes around field names.

**Cons.** A custom grammar to design and maintain. `lark` or hand-rolled.
More opinions baked in (where commas go, how to express tuples,
how to do references).

**Implementation cost.** Bigger. Grammar, parser, error messages.
~500-800 lines.

## Why Markdown specifically — beyond "writers like documents"

(Added 2026-04-15 after user observation.)

Markdown has already become the universal medium between humans and AIs,
and the asymmetry is interesting: the AI sees the source text always;
the human sees rendered output (tables, equations, fenced code with
syntax highlighting, mermaid diagrams). UIs that render markdown into
visually distinct surfaces *are not changing what the AI consumes* —
they're changing what the human consumes from the same underlying text.

Fenced declarative blocks for story records are exactly that pattern,
just for a structure no AI website renders specially yet. The author
writes:

````markdown
```throughline id=T_mc_macbeth
role_label = main-character
owners = [C_macbeth]
...
```
````

The AI sees the same fenced block the human does. A UI that knows about
the `throughline` block type *could* render it as a styled card, an
interactive form, a visualization of the throughline's beats. A UI that
doesn't, falls back to displaying it as a code block — still readable,
still editable, no information lost. The AI behaves identically in
either case.

This means the author surface is **forward-compatible by default.**
We're not waiting on tooling to make the format usable; we're shipping
in a format the existing universal tooling already handles, and any
specialized rendering becomes a pure upgrade. If the project succeeds
and `throughline` blocks become a thing some renderer cares about, that
renderer is a strict win for human authors and changes nothing for AI
authors.

This also means the format ages well. ASCII / UTF-8 plain text with
markdown structure has been the lowest-common-denominator interchange
format for decades; that's unlikely to change. A custom DSL or a binary
format, however expressive, has to fight for tooling. Markdown doesn't.

## Recommendation (if/when we proceed)

Start with the Markdown-with-fenced-blocks shape. It ships a real
"document" surface fast, lets us see whether the document-feel is
actually what authors want before investing in a custom grammar, and
gives us a reversible decision path. If that surface lands well and
authors start asking *can I write this without the fenced-block
scaffolding*, then a DSL becomes the right next step rather than a
speculative one.

Either way, the architecture is the same:

```
authors/macbeth.md  -->  parser  -->  Python records  -->  verifier
                                         (canonical)
```

The Python records remain the source of truth, the test surface, and
what the verifier consumes. The parser is a single-direction
adapter — no round-trip serialization in this iteration.

## What this sketch is not

- Not a commitment. The current Python prototype stack is fine for
  research / design / experiment mode. The user explicitly chose to
  defer this work.
- Not a port. The engine stays in Python. This is purely about what the
  author *opens*.
- Not a database / persistence story. Records still live in memory,
  initialized at parse time. Multi-author / collaborative editing is
  out of scope for this iteration.
- Not a substrate-to-prose layer. That's a separate concern; the user
  has noted confidence that LLMs can do that transformation directly
  or with one simple step.

## When this would advance

Two natural triggers:
- A non-engineer author wants to try the system and bounces off the
  Python files. Concrete signal that the on-ramp is the actual blocker.
- The number of high-level dialects grows past two or three, and the
  per-dialect Python authoring overhead becomes the friction
  rather than the dialect design itself.

Until then: research / design / experiment mode in Python is the right
posture.
