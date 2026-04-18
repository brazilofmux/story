# State of play — sketch 02

**Status:** active
**Date:** 2026-04-18
**Supersedes:** [state-of-play-01](state-of-play-01.md)

A cold-start orientation doc, rewritten (per sketch-01's own
discipline — "don't amend, write sketch-02 at the next milestone")
at the close of the Rashomon probe/sketch cycle: sketch-03 landed
(`ada7e97`), the post-LT12 Rashomon probe endorses its landing
(`25a56f4`), and the three open findings recorded in sketch-01 are
all absorbed.

Re-write this sketch (don't amend — write sketch-03) at the next
milestone. Stale state-of-play is worse than none.

---

## What is built

### The dialect stack (core machinery)

Unchanged from sketch-01 — a three-dialect stack bound by Lowerings:

- **substrate** (`substrate.py`) — typed facts, events, branches,
  descriptions. The "sink" dialect. Specified by substrate-sketch-05,
  descriptions-sketch-01, focalization-sketch-01, identity-and-
  realization-sketch-01, inference-model-sketch-01.
- **dramatic** (`dramatic.py`) — Throughlines, Characters, Scenes,
  Beats, Arguments, Stakes. Dialect-neutral upper surface. Extended
  in the Rashomon arc with `StoryEncoding` + `StoryRelation` for
  multi-Story (multi-story-sketch-01).
- **dramatica-complete** (`dramatica_template.py`) — Dramatica's
  specific theory-shaped extension: DomainAssignments, DSPs on 6
  axes, Signposts, ThematicPicks, CharacterElementAssignments,
  Story_goal, Story_consequence. Specified by dramatica-template-
  sketch-01.
- **lowering** (`lowering.py`) — the cross-dialect binding record.
  Specified by lowering-record-sketch-01.
- **verification** (`verification.py`) — VerificationReview and
  StructuralAdvisory records. Orchestrated through encoding-
  specific `*_verification.py` files.

Shared verifier helpers in `verifier_helpers.py`: EK2 (action shape),
AG1–AG6 (event agency), LT1–LT11 (DSP-limit pressure shape), **LT12
(retraction-kind classification via `classify_retraction_kind`), the
`enabling_retractions` / `restricting_retraction_bands` output fields
on `classify_arc_limit_shape_strong`, and the LT14 disposition table
landed 2026-04-18 with sketch-03.**

### The encodings (five works, same five as sketch-01)

No new encoding since sketch-01. Rashomon's verification module
(`rashomon_dramatica_complete_verification.py`) was updated to
reference LT12–LT14; no substrate or Dramatic-layer changes.

1. **Oedipus** — DSP_limit=Optionlock. Unchanged by LT12.
2. **Macbeth** — DSP_limit=Optionlock. Unchanged by LT12.
3. **Ackroyd** — DSP_limit=Optionlock. Unchanged by LT12 (LT12b
   does not fire on the `ralph_paton` retraction per sketch-03's
   worked-case prediction; OQ3 ratified by implementation).
4. **Rocky** — DSP_limit=Timelock, APPROVED 1.00. LT7 peripheral-
   pre banding handles the `scheduled_fight` retraction before LT12
   is consulted; unchanged.
5. **Rashomon** — DSP_limit=Optionlock (frame) / Timelock (×4
   testimonies). **Bandit and samurai shifted NEEDS_WORK 0.67 →
   NOTED 0.5 post-LT12; wife and woodcutter unchanged at NOTED 0.5.
   All four testimonies now carry a uniform NOTED verdict**,
   consistent with the uniform authorial Timelock claim and
   honest-but-unaffirmed per LT3's weak-fallback.

177 verification tests pass (170 pre-sketch-03 + 7 new tests pinning
LT12a/b/c behavior and the Rashomon verdict shifts).

### The probe (cross-boundary reader-model)

`dramatic_reader_model_client.py` — Anthropic SDK client with
Pydantic-typed structured output. Four behavioral modes observed so
far: **architectural-finding** (Rocky LT9 dissent; original Rashomon
LT2 qualifications), **implementation-refinement** (probe qualifies
a verdict's detail), **bar-raising** (probe endorses but proposes
stricter check), and now **bar-raising-through-endorsement** (probe
endorses a landed sketch AND proposes a sibling refinement — the
post-LT12 pattern).

Two Rashomon probe JSONs form a chain:

- `reader_model_rashomon_output.json` (original, pre-LT12) — the
  two qualifications that drove sketch-03.
- `reader_model_rashomon_post_lt12_output.json` (post-LT12) — all
  5 commentaries are endorses-or-bar-raising-qualifies; zero
  architectural-finding qualifications remaining. Sketch-03's
  landing is validated.

V5 = V6 distribution-identical on the four single-Story runs
(plateau confirmed empirically before the Substack piece).

### The article

`articles/2026-04-18-timelock-or-optionlock.md`, published
2026-04-18 at
https://unlikelyemphasis.substack.com/p/timelock-or-optionlock-real-stories

Unchanged since sketch-01 was written. Section 8's Rashomon
hypothesis has now cycled through probe → sketch → probe and
landed.

---

## What the probe has revealed (closed since sketch-01)

All three sketch-01 findings closed:

- **LT2 enabling-vs-restricting retractions** → closed by
  sketch-03's **LT12** (lexical constraint-predicate vocabulary +
  positional subject-reactivation rule; restricting-only LT2
  counting).
- **LT2 foreclosure detection for effect_count=0 events** →
  addressed by sketch-03's **LT13** (author-opt-in `affordance_*`
  prefix protocol; automatic structural detection deferred as
  sketch-03 OQ1 pending a larger refusal-event corpus).
- **Substrate-asymmetry-across-siblings** → absorbed. Uniform
  NOTED across all four testimonies under LT14; the prior asymmetry
  was an LT2-detector artifact, not a substantive narrative
  signal. No sibling-comparison verifier pass needed.

## What the probe has revealed (open, new since sketch-01)

Findings below surfaced in the post-LT12 Rashomon probe
(`reader_model_rashomon_post_lt12_output.json`, committed at
`25a56f4`). All five commentaries endorsed sketch-03's LT12
classifications; four of them planted sibling refinements.

### Scheduling-act utterances (post-LT12, three testimonies)

**Finding.** Three testimony commentaries (bandit, wife, woodcutter)
independently propose that utterance events — requests, commands,
goadings, provocations — carry an implicit scheduling act that could
fire LT9 (strong Timelock detection), but the current substrate
doesn't surface them as `scheduled_*` predicates. Probe-proposed
candidate predicate names from the run:

- `requested_combat` on `E_t_wife_requests_killing` (bandit probe)
- `situational_forcing` on `E_w_tajomaru_leaves` (wife probe)
- `provoked_confrontation` on `E_wc_wife_goads` (woodcutter probe)

**Proposed shape.** A new sketch — candidate number LT15, or a
scheduling-act-utterance-sketch-01 under a separate topic —
distinguishing **explicit** schedulings (LT8's `scheduled_*`, which
the author asserts as a typed Prop) from **implicit** schedulings
(utterance events whose speech-act force creates a pending
commitment without a typed Prop).

The design tension: implicit scheduling is close to a speech-act
theory of narrative time, which is philosophically rich and
technically under-constrained. Getting this wrong risks converting
every request/command event into a Timelock signal. Probably the
shape is: author-opt-in per-event via a verifier-local vocabulary
(mirroring LT12a's constraint-predicate approach), with specific
whitelist rather than structural inference. OQ: does `SpeechAct` or
similar belong at the substrate/Dramatic layer, or is it purely a
verifier-local vocabulary?

This is the deeper of the two new seeds. It affects LT9's strong
Timelock detection across the corpus — not just Rashomon.

### Enabling-retraction preservation (post-LT12, samurai)

**Finding.** Sketch-03's LT12 silently excludes enabling retractions
from the LT2 count (reports them in the classifier's
`enabling_retraction_count` output field and in the verifier comment
string, but does not convert them into any verdict-shifting signal).
The samurai probe commentary suggests they could carry a secondary
annotation — `enabling_condition_removed` vs `convergence_signal` —
to preserve the narrative information the retraction carries rather
than discarding it.

Quoted probe:

> "the bound_to retraction at τ_s=10 might merit a secondary
> annotation as 'enabling_condition_removed' distinct from
> 'convergence_signal' to preserve the information LT12 currently
> discards."

**Proposed shape.** Smaller than the scheduling-act seed. Two paths:

- Extend `classify_arc_limit_shape_strong`'s output dictionary
  further — add a typed `signal_kinds` list with `convergence` /
  `enabling_condition_removed` entries — so downstream verifiers
  can reference the enabling-retraction structure when their check
  has a use for it. Mechanical.
- Wait until a concrete downstream check has a use for enabling-
  retraction signals before standardizing their surface. The
  post-LT12 probe doesn't point at a specific check; it's a
  preservation argument rather than a use-case argument.

Lean toward the second. Add durable surface only when a forcing
function argues for it.

---

## What's next (research)

In the order I'd work them:

1. ~~**Scheduling-act utterances sketch.**~~ **Landed 2026-04-18 as
   [scheduling-act-utterance-sketch-01](scheduling-act-utterance-
   sketch-01.md)** (design only; implementation pending review).
   Extended LT8 prefix-recognition to `{"scheduled_", "requested_"}`;
   codified Rocky's scheduling-Prop pattern as general authoring
   discipline. Closes bandit + samurai probe qualifications; OQ1
   (`provoked_*`) and OQ2 (`situational_forcing`) remain open; OQ3
   banks `prophesied_*` for future Oedipus/Macbeth work.
2. **The `story_engine/core` vs `encodings/` package split** — now
   **unblocked** (sketch-01 gated this on LT2 sketch-03 landing,
   which it has). Mechanical refactor. Doing this before #3
   prevents moving files while they're being edited by a later
   research arc.
3. ~~**Skeleton generator**~~ **Landed 2026-04-18 as
   [skeleton-generator-sketch-01](skeleton-generator-sketch-01.md)
   + `prototype/story_engine/tools/skeleton.py`.** CLI tool that
   writes the canonical 5-file dramatica-complete encoding stub
   given a work-id, title, and character list. 8 tests pin the
   six sketch acceptance criteria; 573 → 581 prototype test total.
4. ~~**Enabling-retraction preservation**~~ **Banked as an explicit
   deferral sketch — [enabling-retraction-preservation-sketch-01](
   enabling-retraction-preservation-sketch-01.md)** (2026-04-18,
   first deferral sketch in the corpus). Four criteria enumerated
   for when to write sketch-02; none holds today. If no forcing
   function surfaces in two more probe cycles, the finding can be
   formally dropped per the deferral sketch's revisit-criteria.
5. **Maybe-next research targets** (no commitment):
   - A sixth encoding. Candidate: *And Then There Were None* if we
     want to stress-test the unreliable-frame machinery further, or
     a comedy/ensemble work to balance the 4-of-5 tragedies in the
     corpus.
   - The fourth Dramatica quad layer (Elements per Variation).
     Storage-cheap; probe-context expensive; not urgent.
   - Non-Dramatica Templates (Save-the-Cat is partly-done for
     Macbeth + Ackroyd; Freytag / Aristotelian / author-defined
     all admitted by architecture-sketch-02).

---

## Context-economy discipline (for cold-start continuity)

Same rules as sketch-01; the discipline has been working. Rules I
commit to (also saved to memory):

- **Sketches before implementation.** Every architectural finding
  gets a sketch *before* code, not after. Sketch-03 followed this.
- **State-of-play at milestone boundaries.** This doc. Re-write
  (not amend) sketch-03 at the next natural pause.
- **Probe output JSON files are durable artifacts.** The two
  Rashomon probe JSONs (`reader_model_rashomon_output.json` and
  `reader_model_rashomon_post_lt12_output.json`) are the
  template: one JSON before the sketch, one JSON after, both
  checked in. The pair shows the probe's behavior shift from
  architectural-finding to bar-raising-through-endorsement
  concretely.
- **Commit messages are cross-session artifacts.** `ada7e97` and
  `25a56f4` carry the dense record of sketch-03's landing and its
  probe validation. Keep writing them substantively.
- **Prefer Grep/Read-slice over full Read** when the target is
  known. Reserve full Read for unfamiliar files.
- **Spawn Explore agents aggressively** for any research that will
  take 3+ queries. Agent context is separate; results come back
  compact.

### What a cold-start Claude should read first

If you're picking up this project without conversation memory:

1. `design/README.md` — active sketches per topic.
2. This doc (`design/state-of-play-02.md`) — current corpus +
   open findings.
3. `articles/2026-04-18-timelock-or-optionlock.md` — the paper,
   which contextualizes what the corpus is for.
4. `git log --oneline -30` — recent commits.
5. The most recently touched encoding's `*_verification.py` file.
6. The latest probe JSON (`reader_model_rashomon_post_lt12_
   output.json`) — a dense record of where the probe's attention
   currently sits.
