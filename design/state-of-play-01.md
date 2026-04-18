# State of play — sketch 01

**Status:** superseded by [state-of-play-02](state-of-play-02.md)
**Date:** 2026-04-18

A cold-start orientation doc. Written at the Rashomon-arc close
(commit `6fa0d1d`) because we just shipped a paper milestone and
paused. The `design/` README and individual sketches describe
*what each topic commits to*; this doc describes **where the project
actually is right now** — what has been built, what the probe has
found, what's open, and what to pick up next.

Re-write this sketch (don't amend — write sketch-02) at the next
milestone. Stale state-of-play is worse than none.

---

## What is built

### The dialect stack (core machinery)

The `prototype/` package implements a three-dialect stack bound by
Lowerings:

- **substrate** (`substrate.py`) — typed facts, events, branches,
  descriptions. The "sink" dialect. Specified by substrate-sketch-05,
  descriptions-sketch-01, focalization-sketch-01, identity-and-
  realization-sketch-01, inference-model-sketch-01.
- **dramatic** (`dramatic.py`) — Throughlines, Characters, Scenes,
  Beats, Arguments, Stakes. Dialect-neutral upper surface. Extended
  in Rashomon arc with `StoryEncoding` + `StoryRelation` for multi-
  Story (multi-story-sketch-01).
- **dramatica-complete** (`dramatica_template.py`) — Dramatica's
  specific theory-shaped extension: DomainAssignments, DSPs
  (DynamicStoryPoints on 6 axes), Signposts, ThematicPicks,
  CharacterElementAssignments, Story_goal, Story_consequence.
  Specified by dramatica-template-sketch-01.
- **lowering** (`lowering.py`) — the cross-dialect binding record.
  Each Lowering has an `upper_record` CrossDialectRef, `lower_records`
  tuple of CrossDialectRefs, an `annotation` (author-authored
  justification), and `status` (ACTIVE / PENDING). Specified by
  lowering-record-sketch-01 (superseded earlier lowering-sketch-01/02).
- **verification** (`verification.py`) — VerificationReview and
  StructuralAdvisory records. Dialect-boundary checkers emit these.
  Orchestrated through encoding-specific `*_verification.py` files.

Shared verifier helpers live in `verifier_helpers.py`: action-shape
classification (EK2), DSP-limit classification (LT1-LT12), event-
agency classification (AG1-AG6), and the `classify_arc_limit_shape_
strong` function that carries LT7-LT9 per pressure-shape-taxonomy-
sketch-02.

### The encodings (five works, in order of addition)

Each encoding ships four files: `{work}.py` (substrate), `{work}_
dramatic.py` (dramatic), `{work}_dramatica_complete.py` (template),
`{work}_lowerings.py` (bindings), `{work}_dramatica_complete_
verification.py` (cross-boundary checks). Plus demos.

1. **Oedipus** — the origin encoding. First to exercise the
   reader-outruns-character dynamic via inference-model-sketch-01's
   `parricide` + `incest` rules. Tragedy arc. DSP_limit=Optionlock.
2. **Macbeth** — second encoding. First IC-via-prophecy mechanics.
   Save-the-Cat crosscheck encoding (see `macbeth_save_the_cat.py`).
   Tragedy arc. DSP_limit=Optionlock.
3. **Ackroyd** — *The Murder of Roger Ackroyd*. First betrayer-MC
   encoding. Drove identification-goal-sketch-01 (IG2), manipulation-
   taxonomy work (MN4), beat-weight-taxonomy (BW4). DSP_limit=
   Optionlock. Judgment=Bad.
4. **Rocky** — first non-tragedy. First Outcome=Failure. First
   Judgment=Good for MC. First Timelock claim — which drove LT9
   (pressure-shape-taxonomy-sketch-02) to affirmatively detect
   Timelock via scheduling predicates. DSP_limit=Timelock.
5. **Rashomon** — first multi-Story encoding (5 Stories, 10
   relations). Frame + 4 testimony Stories. Frame DSP_limit=Optionlock;
   each testimony DSP_limit=Timelock. Verification runs per-Story
   per MS4. See *open findings* below.

### The probe (cross-boundary reader-model)

`dramatic_reader_model_client.py` — Anthropic SDK client. Renders
the Dramatic + Template + Lowering + substrate + VerificationReview
records into a prompt; Pydantic-typed structured output. Three
behavioral modes empirically observed: **architectural-finding**
(LT9 proposal from Rocky-sketch-01), **implementation-refinement**
(probe qualifies a verdict), **bar-raising** (probe endorses but
proposes stricter check). Observed as probe assessments:
`endorses` / `qualifies` / `dissents` / `noted`.

V5 = V6 distribution-identical (plateau confirmed empirically in
the Ackroyd/Macbeth/Oedipus/Rocky loop before the Substack piece).

### The article

`articles/2026-04-18-timelock-or-optionlock.md`, published
2026-04-18 at
https://unlikelyemphasis.substack.com/p/timelock-or-optionlock-real-stories

10 sections. Section 8 stakes Rashomon as next stress test —
section-8 hypothesis has now been tested (see *open findings*).

---

## What the probe has revealed (not yet closed)

Findings below are open — the corpus has surfaced them; no sketch
has absorbed them yet. In priority order:

### LT2 enabling-vs-restricting retractions (Rashomon-probe, 2026-04-18)

**Finding.** LT2 treats every `asserts=False` WorldEffect as an
Optionlock convergence signal when the retracted prop had been
asserted in-scope earlier. But the substrate carries two structurally
distinct kinds of retraction:

- **Enabling retraction.** State removal that creates a new
  possibility for the immediately subsequent event. Example:
  `E_t_frees_husband` retracting `bound_to(husband, tree)` — this
  *enables* the duel rather than foreclosing alternatives.
- **Restricting retraction.** State removal that closes a
  previously available path. This is what LT2 was designed to
  detect.

Both look identical at the WorldEffect layer. The bandit and samurai
testimonies (NEEDS_WORK 0.67) are false-positives under LT2; their
substrate retractions are enabling, not restricting.

**Proposed shape.** Pressure-shape-taxonomy-sketch-03. Add an LT13
(or whatever the next lemma is) that distinguishes enabling from
restricting retractions. Candidate predicate: a retraction is
*enabling* if the immediately subsequent event on the same arc has a
precondition satisfied by the retraction; *restricting* otherwise.
Only restricting retractions fire LT2.

### LT2 foreclosure detection for effect_count=0 events (Rashomon-probe)

**Finding.** `E_h_tajomaru_refuses` has no WorldEffects — it's a
non-event (the bandit doesn't kill). But it structurally forecloses
the "bandit kills husband" narrative path. LT2 misses it because
there's no prop to retract.

**Proposed shape.** Same sketch as above or a sibling. Events with
effect_count=0 that correspond to a declined/refused affordance
should count as retractions of the *affordance prop* (even when the
substrate doesn't author a prop for the affordance).

### Substrate-asymmetry-across-siblings as a reportable signal (Rashomon)

**Finding.** Four testimonies declared uniformly Timelock. Two verify
NEEDS_WORK, two NOTED. The asymmetry is informative — it says the
substrate shapes differ even when the authorial claim is uniform.
No current verifier surface reports this as a single "sibling
asymmetry" finding; each testimony is checked independently.

**Proposed shape.** A sibling-comparison pass that runs after the
per-Story MS4 pass and emits a single StructuralAdvisory when sibling
testimonies (parallel-to StoryRelations) produce divergent verdicts.
Low priority — the per-Story verdicts already carry the information;
this is just a convenience surface.

---

## What's next (research)

In the order I'd work them:

1. **LT2 sketch-03** — close the two Rashomon probe findings.
   Smallest shippable unit; closes the arc cleanly. Re-run the four
   Rashomon testimony checks; the two NEEDS_WORK should either flip
   or stand with clearer reason.
2. **The `story_engine/core` vs `encodings/` package split.** Not
   research; mechanical. Defer until LT2 sketch-03 is in — avoids
   moving files while they're being edited.
3. **Skeleton generator** — a tool that, given Story title +
   Characters + Throughline count, stubs the four encoding files.
   Codifies only the mechanical shell; does not thwart research.
4. **Maybe-next research targets** (no commitment):
   - A sixth encoding to test a specific hypothesis the current
     five don't cover. Candidate: a mystery with multiple suspects
     (not *Ackroyd* — that's an inverted-mystery). Something like
     *And Then There Were None* if we want to stress-test the
     unreliable-frame machinery further.
   - The fourth Dramatica quad layer (Elements per Variation).
     Storage-cheap; probe-context expensive; not urgent.
   - Non-Dramatica Templates (Save-the-Cat is partly-done for
     Macbeth+Ackroyd; Freytag / Aristotelian / author-defined all
     admitted by architecture-sketch-02).

---

## Context-economy discipline (for cold-start continuity)

The conversation-context risk is real: if the active Claude hits
limits, the only recovery paths are rollback, handoff to Codex, or
wait for model upgrade. None are good. The mitigation is discipline
about *what gets written down in durable form* — so a fresh Claude
can read the design/ directory, the articles, the memory/ pointers,
and the git log, and pick up with minimal conversation-replay.

Rules I commit to (also saved to memory):

- **Sketches before implementation.** Every architectural finding
  gets a sketch *before* code, not after. Already doing this.
- **State-of-play at milestone boundaries.** This doc. Re-write (not
  amend) sketch-02 at the next natural pause.
- **Probe output JSON files are durable artifacts.** Check them in;
  reference them in articles and commits. They preserve "what the
  LLM found" across sessions.
- **Commit messages are cross-session artifacts.** Already writing
  them substantively. Keep doing that — they're often the densest
  record of a change's reasoning.
- **Prefer Grep/Read-slice over full Read** when the target is
  known. Full Read is ~hundreds of lines of context; targeted read
  is ~dozens. Reserve full Read for unfamiliar files.
- **Spawn Explore agents aggressively** for any research that will
  take 3+ queries. Agent context is separate; results come back
  compact.

### What a cold-start Claude should read first

If you're picking up this project without conversation memory:

1. `CLAUDE.md` (if exists — not sure, check)
2. `design/README.md` — active sketches per topic
3. This doc (`design/state-of-play-01.md`) — current corpus +
   open findings
4. `articles/2026-04-18-timelock-or-optionlock.md` — the paper,
   which contextualizes what the corpus is for
5. `git log --oneline -30` — recent commits
6. The most recently touched encoding's `*_verification.py`
   file — these are the densest check-logic records
