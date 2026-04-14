# Focalization — sketch 01

**Status:** draft, active
**Date:** 2026-04-13
**Supersedes:** nothing (new topic; closes a specific prototype weakening)
**Frames:** [architecture-sketch-01.md](architecture-sketch-01.md), [substrate-sketch-05.md](substrate-sketch-05.md), [identity-and-realization-sketch-01.md](identity-and-realization-sketch-01.md)
**Superseded by:** nothing yet

## Purpose

Close the one explicit weakening the substrate's `project_reader`
currently admits to. The function's docstring says:

> Sketch 04 K2 defines focalization as a constraint on reader access:
> propositions the focalizer lacks become reader-gaps; propositions
> the focalizer misconstrues become reader-believed rather than
> reader-known. That is subtle to implement correctly — in particular,
> demotion of prior disclosures requires τ_d-scoped reader-state
> tracking we do not yet have. Previous drafts of this function
> folded the focalizer's entire state into the reader's state; that
> was wrong (it collapses 'the scene is routed through X's
> perspective' into 'the narration dumps X's mind into the reader').
> The current implementation records focalization as metadata only:
> no automatic state mutation occurs. Disclosures remain the only
> positive-update operator.
>
> This is weaker than sketch 04 asserts. Proper focalization
> semantics are a deliberate deferred item for a later sketch /
> prototype iteration.

This is that sketch. The fix is narrower than the docstring
anticipated:

- The "τ_d-scoped reader-state tracking" concern was about
  *demoting prior reader state* when a later scene is focalized
  through someone who knows less. This sketch side-steps that
  concern by committing: focalization constrains *new disclosures*
  as they land in the reader's state, not *prior reader state*.
  Carried-forward knowledge persists.
- The "dump the focalizer's state into the reader" failure mode is
  avoided by the same rule: focalization affects the *slot* of
  disclosures the author already wrote, not a wholesale merge.

Neither implementation shortcut is needed. The model is additive,
per-entry, and pure.

This sketch specifies:

- The slot-constraint rule (F1) with explicit ordering.
- The per-entry scope rule (F2) — no retroactive demotion.
- The reference-τ_s rule (F3) — focalizer's state at the narrated
  event's story-time.
- The omniscient default (F4).
- Interaction with identity substitution (F5).
- What is deferred (F6) — narrator intrusion, external focalization,
  suspense/immersion effects.
- Worked examples over Oedipus and Rashomon.
- Implementation notes for the `project_reader` change.

## What this sketch is *not* committing to

- Narrator intrusion (author overriding focalization to disclose
  something the focalizer doesn't know). A future sketch may add
  a `bypass_focalization` flag on `Disclosure`.
- External focalization (camera-only perspective — narrator shows
  behavior, no epistemic access). Represented conceptually by a
  non-agent focalizer; implementation deferred.
- Fixed vs. variable focalization as a typed distinction. The
  substrate's per-entry `focalizer_id` already supports both; no
  new machinery needed.
- Multiple simultaneous focalizers within one entry. If needed,
  encodings compose multiple entries at the same τ_d.
- Suspense / immersion effects where the reader "forgets" broader
  knowledge to feel with the focalizer. That's a reader-psychology
  model, not a focalization constraint. Open question.
- A new event-kind, new effect type, or new sjuzhet field. The
  existing `SjuzhetEntry.focalizer_id` is sufficient.
- Performance optimizations. A per-entry `project_knowledge` call
  for the focalizer is cheap at prototype scale.

If a question starts "how do I let the narrator break focalization"
or "how does the reader's state get re-downgraded when…" — it is
out of scope.

## What this sketch *is* committing to

1. **F1 — Focalization constrains disclosure slot.** A sjuzhet
   entry with `focalizer_id` set demotes each disclosure in that
   entry. The disclosure lands at `min(author_slot, focalizer_slot)`
   under the ordering `KNOWN > BELIEVED > SUSPECTED > GAP`. If the
   focalizer does not hold the proposition (not even under
   substitution per F5), the disclosure lands at `GAP`. The
   disclosure still enters the reader's state — just at a demoted
   slot.
2. **F2 — Focalization-driven demotion does not override stronger
   prior reader state.** When F1's demotion produces an effective
   slot weaker than the slot the reader already holds for the same
   proposition from an earlier entry, the write is skipped and
   prior reader state persists. Memory does not get downgraded just
   because the narrative perspective shifts. **Explicit author
   demotion** (e.g., an omniscient entry that discloses P at a
   weaker slot than the reader currently holds — retroactive
   reframing by unreliable-narrator reveal) is NOT focalization-
   driven and is not subject to F2; it follows the existing
   "later disclosure overrides earlier" convention. The
   distinction: F2 only protects against *incidental* weakening
   caused by perspective shift, not against *intentional*
   weakening the author authored at face value.
3. **F3 — The focalizer's reference τ_s is the narrated event's
   τ_s.** For a sjuzhet entry narrating event `E`, focalization
   uses `project_knowledge(focalizer_id, events_in_scope, E.τ_s)`
   as the constraint state. Because events' effects land at their
   own τ_s, a focalizer who is a participant in the event (e.g.,
   the killer in a killing event) sees the event's effects in
   their own state at the reference τ_s.
4. **F4 — Omniscient is the explicit default.** A sjuzhet entry
   with `focalizer_id=None` is omniscient narration; disclosures
   pass through at their author-stated slot. This preserves the
   current prototype's behavior for encodings that don't opt into
   focalization.
5. **F5 — Focalizer access is substitution-aware.** When checking
   "does the focalizer hold P?", the substrate uses `holds(P)`
   (substitution-aware per identity-and-realization-sketch-01 I3/I7),
   not `holds_literal(P)`. A focalizer who query-knows a fact via
   identity substitution is treated as knowing it for focalization
   purposes. This is the natural composition: the reader's access
   through the focalizer reflects the focalizer's full
   substitution-aware epistemic reach.
6. **F6 — No narrator intrusion; no external focalization.** All
   disclosures in a focalized entry are constrained by F1. There
   is no flag for the narrator to override focalization and
   disclose beyond the focalizer's access. Similarly, no
   "external focalizer" abstraction. Both are legitimate
   narratological phenomena; both are deferred.

F1 through F6 pass architecture-sketch-01 A3: each describes
drift the schema catches, not content an attentive reviewer could
self-police from prose. Without F1's constraint, a disclosure that
should have been a GAP (because the focalizer doesn't know the
proposition) would silently become KNOWN in the reader's state —
exactly the kind of epistemic drift an author could not reliably
catch by re-reading.

## Relation to prior sketches

- **Architecture-01 A3.** Focalization machinery passes A3. The
  constraint is structural (slot-level demotion), not interpretive.
  Whether a scene *feels* focalized through Alice is description
  territory; whether the reader's slot for a disclosure is KNOWN or
  GAP is fact territory.
- **Substrate-05 K2.** Sketch-05 carried forward substrate-04's K2
  commitment ("reader-as-subject with disjoint narrative update
  operators") and noted the focalization weakening. F1-F5 close
  that weakening; F6 explicitly defers what isn't closed.
- **Identity-and-realization-01 I3, I7.** F5 depends on
  substitution-aware `holds`. An identity the focalizer holds as
  KNOWN extends their focalization-access; an identity they hold as
  BELIEVED/SUSPECTED/GAP (per I7) does not. Focalization does not
  invent new identity semantics; it composes with the existing ones.
- **Descriptions-01.** Focalization is a constraint on facts; it
  does not touch descriptions. A description attached to a sjuzhet
  entry is fold-invisible regardless of focalization — the
  description surface doesn't have "slots" to demote. Any
  focalization-like framing *of* interpretation lives in the
  description (e.g., `kind=reader-frame` texts that say "this
  scene reads differently from Alice's angle"), not in the fact
  fold.
- **Reader-model-01.** The reader-model's `ReaderView` consumes
  the substrate-produced state. Focalization operates upstream of
  the view (in `project_reader`), so the view carries the already-
  focalized reader state without needing its own rule.

## The slot-ordering rule (F1 in detail)

### The ordering

```
KNOWN > BELIEVED > SUSPECTED > GAP
```

Matches the `_SLOT_RANK` mapping the substrate already uses for
identity-substitution multi-match resolution (KNOWN=3, BELIEVED=2,
SUSPECTED=1, GAP=0). No new ordering is introduced.

### The demotion rule

For each disclosure `d` in a sjuzhet entry with `focalizer_id = F`:

- Compute the focalizer's state: `F_state = project_knowledge(F,
  events_in_scope, entry.event.τ_s)`.
- Compute the focalizer's slot for `d.prop`:
  - If `F_state.holds(d.prop)` returns a `Held`, its slot is the
    focalizer's slot.
  - If `F_state.holds(d.prop)` returns `None`, the focalizer's
    slot is conceptually "absent" — represented as `GAP` in the
    demotion calculation (the weakest slot).
- The disclosure's effective slot = `min(d.slot, focalizer_slot)`
  under the KNOWN>BELIEVED>SUSPECTED>GAP ordering.
- The disclosure is applied to the reader's state at the effective
  slot, preserving the disclosure's confidence and via fields.
  (Confidence is orthogonal to slot; it tracks how strongly the
  slot is held, not the slot itself.)

### Worked table

Author says         | Focalizer holds           | Reader receives
--------------------|---------------------------|----------------------
`KNOWN`             | `KNOWN`                   | `KNOWN`
`KNOWN`             | `BELIEVED`                | `BELIEVED`
`KNOWN`             | `SUSPECTED`               | `SUSPECTED`
`KNOWN`             | `GAP` (authored)          | `GAP`
`KNOWN`             | *absent*                  | `GAP`
`BELIEVED`          | `KNOWN`                   | `BELIEVED` (author weaker)
`SUSPECTED`         | `KNOWN`                   | `SUSPECTED` (author weaker)
`GAP` (explicit)    | `KNOWN`                   | `GAP` (author weakest)

### Why GAP, not suppression, for focalizer-absent

When the focalizer doesn't hold a disclosed proposition, the
disclosure could either be **demoted to GAP** (land in the reader's
state as an acknowledged open question) or **suppressed**
(disappear entirely, no reader state change for that proposition).

F1 chooses GAP. Reasons:

- **Narrative usefulness.** The GAP record surfaces the open
  question in Sternberg-curiosity queries and in the reader's
  visible-gaps display. The reader experiences a question they
  don't have the answer to — classic curiosity fuel. Suppression
  would hide the question entirely.
- **Substrate-04 K2 consistency.** K2's phrasing — "propositions
  the focalizer lacks become reader-gaps" — is exactly the GAP
  treatment.
- **Auditability.** A GAP record is a visible artifact of the
  focalization act. Suppression leaves no trace; an author
  inspecting the reader state has no signal that their disclosure
  didn't land.

Suppression is the more conservative alternative and may revisit
later if the GAP behavior generates false-positive curiosity signals
in practice.

## Per-entry scope (F2 in detail)

### The rule

When F1's computation produces a disclosure-effective-slot weaker
than what the reader already holds for the same proposition
(from an earlier entry), the write is skipped. The reader's prior
stronger slot persists.

A disclosure is *focalization-demoted* when `effective_slot !=
author_slot` — i.e., the focalizer-constraint step lowered the
slot below what the author wrote. Only focalization-demoted
disclosures are subject to F2's skip-if-weaker rule.
**Non-demoted disclosures** (omniscient entries, or focalized
entries where the focalizer holds the prop at the author's slot
or stronger) follow the existing "later disclosure overrides
earlier" convention unchanged.

### The distinction — focalization-driven vs. explicit author demotion

Two scenarios produce a disclosure slot weaker than the reader's
current state:

- **Focalization-driven demotion.** Author writes `KNOWN`; the
  focalizer doesn't hold the prop; F1 lowers to `GAP`. The
  demotion is incidental — a side effect of perspective, not an
  authorial choice about the reader's conviction. F2 forbids
  writing over stronger prior state in this case.

- **Explicit author demotion.** Author writes `BELIEVED` in an
  omniscient entry (or in a focalized entry where the focalizer
  holds the prop at `BELIEVED` or weaker — the demotion is at
  the author's own slot, not further). This is retroactive
  reframing, a legitimate narrative device — the unreliable-
  narrator reveal, the "actually that wasn't true" moment. F2
  does not protect against this; later-overrides-earlier applies
  as before.

The implementation test is whether `effective_slot < author_slot`.
If yes, F2 applies; if no, existing convention applies.

### Why this matters

If focalization retroactively demoted prior reader state
*incidentally*, two problems:

1. **Memory model.** A reader who learned X in scene 1 doesn't
   "forget" X when scene 2 is focalized through someone who
   doesn't know X. That's immersion, not amnesia. Suspense and
   immersion are handled by the author's *sequencing* and *what
   they disclose*, not by retroactive state demotion.
2. **Accidental destruction.** An author who writes a focalized
   scene without thinking about what the focalizer holds could
   silently destroy the reader's prior knowledge. F2 catches
   this: the focalization demotion becomes a no-op when it would
   weaken prior state. If the author actually wants retroactive
   weakening, they use an omniscient disclosure at the weaker
   slot (explicit, visible as authored intent).

Side-effect benefit: F2 resolves the substrate-04 docstring
concern about "τ_d-scoped reader-state tracking we do not yet
have." The tracking was only needed for retroactive demotion;
F2 avoids the incidental demotion, so the tracking is unneeded.

### What suspense/immersion actually is

When a reader "feels suspense" during a scene focalized through a
less-knowledgeable character, their broader knowledge isn't
literally erased — they hold both their knowledge *and* the
character's uncertainty in tension. Modeling that is a
reader-psychology task (how an LLM or human interprets the view),
not a substrate constraint. Lives above the substrate; the
reader-model surface (reader-model-01) is where it goes.

## Reference τ_s (F3 in detail)

For a sjuzhet entry with `event_id = E` and `focalizer_id = F`:

```
focalizer_state = project_knowledge(F, events_in_scope, E.τ_s)
```

### Why the event's τ_s

The event happens at τ_s; its effects land at τ_s. A focalizer who
participates in the event (the killer in a killing event, the
speaker in an utterance) has the event's effects in their state at
τ_s. A focalizer who witnesses without participating still has
`observe()` effects at τ_s.

### What about a focalizer not present at the event?

An author can set `focalizer_id` to an agent who was not present
at the event — a narrative device like retrospective focalization
through an absent witness. That focalizer's state at τ_s will not
include the event's effects (they weren't there to observe). Any
disclosure of the event's effects through that focalizer will
demote to GAP under F1. This is correct: the reader's access
through an absent focalizer *should* be sparse.

### What about τ_s of disclosures that are unrelated to the event?

Some author disclosures in an entry may assert propositions not
produced by the event itself — foreshadowing, background
commentary. F1/F3 still apply: the focalizer's state at E.τ_s is
the constraint. If the focalizer holds the proposition at KNOWN by
τ_s, disclosure passes through. If not, demotion fires. This
naturally handles "author uses a focalized scene to remind the
reader of something the focalizer knows" vs. "author tries to
smuggle omniscient background into a focalized scene."

## Substitution-aware focalizer access (F5 in detail)

Per identity-and-realization-sketch-01, agents' `holds(p)` queries
are substitution-aware. F5 says focalization uses the same query:

```
focalizer_held = focalizer_state.holds(d.prop)  # substitution-aware
```

### What this implies

- A focalizer who holds `P(a)` and `identity(a, b)` at KNOWN
  substitution-knows `P(b)`. A disclosure of `P(b)` through this
  focalizer passes at KNOWN.
- A focalizer who holds `identity(a, b)` only as SUSPECTED does
  not substitute (per I7). A disclosure of `P(b)` (when only
  `P(a)` is literally held) demotes to GAP.
- Post-anagnorisis Jocasta's state includes
  `identity(oedipus, the-exposed-baby)` at KNOWN; substitution
  gives her `child_of(oedipus, jocasta)` even though she only
  literally holds `child_of(the-exposed-baby, jocasta)`. A
  disclosure of `child_of(oedipus, jocasta)` through Jocasta
  post-anagnorisis passes at KNOWN.

### What this does NOT imply

- The substrate does not materialize derived facts into the
  focalizer's state to make the substitution visible. The
  focalizer's `by_prop` remains literal (I3's invariant).
  Substitution is a property of *how* the substrate queries the
  state, not of the state itself.

## What's deferred (F6 details)

### Narrator intrusion

Classic novelistic device: in a mostly-focalized passage, the
narrator breaks perspective for a sentence to tell the reader
something the focalizer doesn't know. (Austen does this
constantly.)

In the substrate, this would be a `Disclosure` flagged to bypass
focalization — land at the author's slot regardless of the
focalizer's state. Sketch 01 does not include this flag. When an
encoding needs narrator intrusion, the current workaround is to
split the entry: an omniscient entry (focalizer_id=None) at
τ_d=N.1 carries the intrusion; a focalized entry at τ_d=N.2
carries the focalized disclosures. Ugly but correct.

A future sketch (probably a small amendment rather than a
separate sketch topic) adds the flag.

### External focalization

Genette's third mode: the narrator shows only external behavior —
no access to any character's epistemic state. Represented as
"camera view." In the substrate, this would be a focalizer_id set
to a non-agent entity (a "camera" or "external" placeholder) that
constrains disclosures to world-level facts only, with no agent
state to query.

Not needed for the current encodings. If later encodings want it,
the design shape is: a focalizer kind field distinguishing agent,
external, and (future) collective/multiple modes. Defer.

### Suspense and immersion effects

Already discussed under F2. The substrate faithfully represents
what the reader's literal state is; the *feel* of suspense (the
reader's broader knowledge in tension with a focalized scene's
limited perspective) is reader-psychology above the substrate.
Reader-model-01's LLM interpretation is the natural home for such
effects.

## Worked example — Oedipus

The Oedipus encoding has two focalized sjuzhet entries:

```
SjuzhetEntry(
    event_id="E_jocasta_realizes",
    τ_d=9, focalizer_id="jocasta",
    disclosures=(),
),

SjuzhetEntry(
    event_id="E_oedipus_anagnorisis",
    τ_d=13, focalizer_id="oedipus",
    disclosures=(),
),
```

Both have empty disclosures. F1 has nothing to constrain; behavior
is identical to before. The entries continue to record their
focalizer for downstream inspection (reader-model views render
"focalized through Jocasta" as a structural cue), but no state
update is affected.

This is the "backward-compatible" case: existing focalized entries
without disclosures are unaffected. Encodings that want to exercise
F1 start authoring disclosures on focalized entries.

### Hypothetical — Jocasta's realization with a disclosure

Suppose an author wanted `E_jocasta_realizes` to disclose
`child_of(oedipus, jocasta)` to the reader. Jocasta's post-event
state at τ_s=9 holds `identity(oedipus, the-exposed-baby)` KNOWN
plus `child_of(the-exposed-baby, jocasta)` KNOWN; substitution
gives her `child_of(oedipus, jocasta)` at KNOWN. F1 passes the
disclosure at KNOWN. Correct.

If the same disclosure were authored on the *earlier* entry
`E_jocasta_mentions_crossroads` focalized through Jocasta at τ_s=5
— before her anagnorisis — Jocasta's state at τ_s=5 does not have
the identity. Substitution doesn't fire. F1 demotes disclosure to
GAP. The reader would see `child_of(oedipus, jocasta)` as a GAP at
τ_d=5: a question opened through Jocasta's ignorance.

The two scenarios produce different reader states, correctly
tracking the information flow.

## Worked example — Rashomon

Rashomon has many focalized entries — one per testimony beat.
Each is focalized through the testifier (`"tajomaru"`, `"wife"`,
`"husband"`, `"woodcutter"`). Many carry disclosures.

### A representative case

```
SjuzhetEntry(
    event_id="E_t_duel",
    τ_d=13, focalizer_id="tajomaru",
    disclosures=(
        _disc(killed("tajomaru", "husband")),
        _disc(killed_with("tajomaru", "husband", "sword")),
    ),
),
```

Under F1, each disclosure is constrained by Tajomaru's state at
`E_t_duel.τ_s=9` on the `:b-tajomaru` branch.

Tajomaru's literal state at τ_s=9 on his branch must include
`killed(tajomaru, husband)` at KNOWN for the disclosure to pass
through at KNOWN. Inspection of the current encoding:

```
Event(
    id="E_t_duel",
    type="combat",
    ...
    effects=(
        world(killed("tajomaru", "husband")),
        world(killed_with("tajomaru", "husband", "sword")),
    ),
),
```

Only world effects. No `observe()` for Tajomaru. Under F1, the
disclosure demotes to GAP.

This is an **encoding bug** F1 exposes: a killer ought to know
they killed. Fix: add `observe()` effects for killers in their own
killing events. Similarly for `E_w_killing` (wife), `E_h_suicide`
(husband), `E_wc_fight` (Tajomaru in the woodcutter branch).

The probe ships this fix alongside F1. Legitimate encoding
improvement regardless — under the new model it becomes visible.

### After the encoding fix

With Tajomaru holding `killed(tajomaru, husband)` at KNOWN from
τ_s=9 on his branch, F1 passes the disclosure at KNOWN. Reader
receives KNOWN. The test
`test_reader_on_tajomaru_branch_knows_tajomaru_killed_husband`
continues to pass.

### The payoff — cross-branch focalization

More interesting: Rashomon's four branches produce four distinct
reader states. On `:b-tajomaru`, the reader receives the testimony
through Tajomaru's lens. On `:b-wife`, through the Wife's. F1's
substitution-aware access interacts with each branch's own identity
substitutions (if any). For the current encoding, no per-branch
identities exist, but the machinery is in place.

### A focalization-driven demotion on Rashomon

If an entry on `:b-wife` were focalized through the wife and
disclosed something the wife doesn't hold — e.g., the woodcutter's
later confession details — F1 demotes those disclosures to GAP on
that branch's reader state. No test currently exercises this, but
a synthetic test in the probe does.

## Implementation notes

### project_reader changes

Currently:

```python
for entry in entries_sorted:
    ...
    for d in entry.disclosures:
        by_prop[d.prop] = Held(
            prop=d.prop, slot=d.slot,
            confidence=d.confidence, via=d.via,
            provenance=(f"disclosed @ τ_d={entry.τ_d}",),
        )
```

Under F1 + F2:

```python
for entry in entries_sorted:
    ...
    focalizer_state = None
    if entry.focalizer_id is not None:
        focalizer_state = project_knowledge(
            entry.focalizer_id, events_in_scope, event.τ_s,
        )
    for d in entry.disclosures:
        effective_slot = d.slot
        focalization_demoted = False
        if focalizer_state is not None:
            focalizer_held = focalizer_state.holds(d.prop)
            focalizer_slot = focalizer_held.slot if focalizer_held else Slot.GAP
            effective_slot = _weaker_slot(d.slot, focalizer_slot)
            focalization_demoted = (effective_slot != d.slot)

        # F2: focalization-driven demotion does not override stronger
        # prior reader state. Explicit author demotion (non-focalized
        # or focalized-but-at-author's-slot) still applies.
        if focalization_demoted:
            current = by_prop.get(d.prop)
            if current is not None and \
               _SLOT_RANK[current.slot] >= _SLOT_RANK[effective_slot]:
                continue  # keep prior stronger state; skip write

        by_prop[d.prop] = Held(
            prop=d.prop, slot=effective_slot,
            confidence=d.confidence, via=d.via,
            provenance=(
                f"disclosed @ τ_d={entry.τ_d}"
                + (f", focalized through {entry.focalizer_id} at "
                   f"τ_s={event.τ_s}" if entry.focalizer_id else ""),
            ),
        )
```

With `_weaker_slot(a, b)` returning the slot with the lower
`_SLOT_RANK`.

The F2 guard is gated on `focalization_demoted` so that:

- Omniscient disclosures (no focalizer) always overwrite — existing
  reveal/reframing convention unchanged.
- Focalized disclosures where the focalizer matches or exceeds the
  author's slot always overwrite — no demotion happened, so F2 is
  inactive.
- Focalized disclosures where the focalizer lowered the slot check
  the reader's current state; only write if the demotion does not
  weaken prior state.

### Signature stability

`project_reader` keeps the same signature. Internal behavior
changes; callers unaffected. The docstring is updated to remove
the weakening note.

### Memoization

Per-entry `project_knowledge(focalizer_id, …)` is re-computed for
every entry with a focalizer, even if the same focalizer and τ_s
appear across multiple entries. A simple memo keyed by
`(focalizer_id, up_to_τ_s)` within a single `project_reader` call
is an easy optimization if profiling shows it matters. Not in
sketch 01 scope.

### The helper `_weaker_slot`

```python
def _weaker_slot(a: Slot, b: Slot) -> Slot:
    """Return whichever of a, b is weaker under
    KNOWN > BELIEVED > SUSPECTED > GAP."""
    return a if _SLOT_RANK[a] <= _SLOT_RANK[b] else b
```

Reuses the existing `_SLOT_RANK` dict.

### Backward compatibility

- Entries with `focalizer_id=None`: unchanged behavior (F4).
- Entries with `focalizer_id=<id>` and no disclosures: unchanged
  behavior (no disclosures to constrain).
- Entries with `focalizer_id=<id>` and disclosures: may change if
  the focalizer doesn't hold a disclosed proposition. Encodings
  that relied on the pre-F1 behavior (disclosure always passes at
  author-stated slot) need review. The probe ships a Rashomon
  encoding fix (killer observations) that this exposes.

## Tests the probe will add

Synthetic (in `test_substrate.py`):

- F1 slot-demotion through author>focalizer case
- F1 slot-demotion through focalizer-absent → GAP case
- F1 author-weaker-than-focalizer passes through at author slot
- F2 prior stronger reader state persists through a later focalized
  entry whose F1-demoted disclosure would weaken it
- F2 explicit-author demotion via omniscient entry still overrides
  prior stronger state (distinction from F2 protection)
- F3 focalizer's reference τ_s is the event's τ_s
- F4 omniscient entries unchanged
- F5 substitution-aware focalizer access

Story-integrated (in `test_rashomon.py` and `test_substrate.py`):

- Per-branch Rashomon testimony: reader receives each testifier's
  disclosures at KNOWN via F1 (after encoding fix for killer
  observations)
- Oedipus: existing focalized entries (empty disclosures) remain
  unaffected; the three existing Oedipus tests continue to pass

## Open questions

1. **Narrator intrusion flag.** A `Disclosure` field like
   `bypass_focalization: bool = False` would let the author
   override F1 for specific disclosures in a focalized entry. Not
   urgent (workaround is splitting entries), but Austen-style
   narrators would use this heavily. Follow-on amendment.
2. **External focalization.** Camera-only perspective. Needs a
   focalizer kind beyond agent. Not exercised by current
   encodings; defer.
3. **Suspense / immersion as reader-psychology.** F2 declines to
   retroactively demote. If the project later wants "reader feels
   suspense" as a structural signal, it lives on the reader-model
   surface (consulting descriptions + gap state), not in
   substrate focalization.
4. **Collective / multiple focalization.** A scene focalized
   through several characters simultaneously (a crowd, a jury).
   Implementation shape open: per-disclosure weakest-across-the-
   group? Strongest? Depends on the narrative intent. Defer.
5. **Focalizer-as-reader-model-source.** An LLM-focalizer reading
   a description and producing a slot constraint. Bleeds into
   reader-model-01 territory. Defer.
6. **Focalization in counterfactual branches.** `:counterfactual`
   branch scoping already applies to `project_knowledge`; F3's
   reference τ_s computation composes naturally. Not exercised;
   no special handling expected.
7. **Performance at scale.** Per-entry focalizer-state
   computation is O(entries × events). Memoization by
   `(focalizer_id, τ_s)` is simple if needed.
8. **Focalization of sjuzhet entries that introduce identity
   propositions.** An entry discloses `identity(A, B)` at KNOWN,
   focalizer holds the identity at SUSPECTED. F1 demotes to
   SUSPECTED. The reader now substitution-knows nothing via that
   identity (per I7). Intended behavior — partial realization
   yields partial reader access.

## Discipline

Process expectations for work against this sketch:

- **Focalized entries that carry disclosures are deliberate.**
  An author using `focalizer_id` commits to the disclosure
  constraint. If they want a disclosure to pass unconstrained,
  they omit focalizer_id on that entry (or wait for narrator
  intrusion in a future sketch).
- **Encodings author observations for participants.** A killer
  ought to hold `killed(…)` about their own act; a speaker ought
  to hold their own utterance's content. If focalization exposes
  an encoding gap (the focalizer doesn't know their own actions),
  fix the encoding, don't work around F1.
- **The literal reader state remains literal.** Like identity
  substitution, focalization is a constraint on *how the substrate
  builds the reader state from disclosures*. Once the state is
  built, it's literal — no secret demotion at query time.
- **Prior reader state is sacred.** F2's no-retroactive-demotion
  rule is a strict invariant. A future sketch that wants
  suspense-driven demotion opens a different mechanism; it does
  not rewrite F2.

## Summary

| | Before F1-F6 | After F1-F6 |
|---|---|---|
| `focalizer_id=None` | omniscient | unchanged (F4) |
| `focalizer_id=X`, no disclosures | metadata only | unchanged |
| `focalizer_id=X`, disclosures | pass at author slot | demoted by F1 rule |
| Prior stronger state, later focalization-demoted disclosure | overwritten | preserved (F2) |
| Prior stronger state, later explicit-author weaker disclosure | overwritten | overwritten (F2 inactive) |
| Focalizer holds via identity substitution | no effect | counts as holding (F5) |
| Focalizer absent for disclosed prop | no effect | disclosure → GAP (F1) |
| Narrator intrusion | no support | no support (F6 defers) |
| External focalization | no support | no support (F6 defers) |
| Suspense / immersion | no support | reader-model territory |
| `project_reader` signature | (sjuzhet, events, branch, all_branches, up_to_τ_d) | unchanged |
| `project_reader` docstring weakening | present | removed |
