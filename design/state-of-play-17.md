# State of play — sketch 17

**Status:** active
**Date:** 2026-06-17
**Supersedes:** [state-of-play-16](state-of-play-16.md)

Single-sketch refresh marking **aristotelian-sketch-07** (`4f37cd1`) —
the landing of **OQ-MALFI-3** (pathos-hero vs arc-hero split), the
strongest finding the corpus had banked that was *both* probe-surfaced
*and* cross-encoding-confirmed with a proposed shape. The headline: the
full new-finding loop — *probe surfaces a gap with a proposed field →
the next sketch lands it end-to-end → migrate the exercising encodings →
re-probe verifies closure and moves attention to the next layer* — has
now run to completion for the **third** time (OQ-LEAR-4 → sketch-06 was
the first; OQ-MALFI-3's cross-encoding *confirmation* via the Revenger's
arc was the second; sketch-07 is the third), and the loop is now a
reliable, repeatable instrument rather than a one-off.

Since SoP-16, two commits (both research/production-blended):

- `8971084` — the substrate→first-draft generator (Oedipus); the
  compiler **back-end** opened (see SoP-16's pause-point reflection and
  `project-goal-generation-tool` memory).
- `4f37cd1` — **sketch-07**: A22/A23/A7.19, two migrations, Session-7
  re-probe closure.

## Headline — three load-bearing claims

### 1. OQ-MALFI-3 is CLOSED, verified at both sites, with zero strain

Sketch-07 landed exactly the shape the Revenger's Session-5 probe
proposed: **A22 `ArMythos.pathos_character_ref_ids`** (a tuple, not a
singular — the probe insisted on the list) + **A23
`ArCharacter.pathos_carrier: bool`** (the probe's companion flag), with
**A7.19** enforcing resolution + A22/A23 concordance. The field is
orthogonal on two axes the corpus exercises in opposite directions:

- **Revenger's** (the harder site): the pathos-centre is split off from
  *both* the recognizer and the tragic-hero set, and is borne by
  arc-less, non-agentive referents — Gloriana (a skull, dead nine years
  pre-play) + Antonio's wife. A22 admits them with no arc requirement;
  the overloaded `AR_PATHOS_CLUSTER_PARALLEL` relation that previously
  carried the claim under stretch is **retired**.
- **Malfi** (the surfacing site): the pathos-centre (the Duchess) *is*
  the tragic hero, split only from the recognizer (Ferdinand). The
  coincidence case, proving A22/A23's orthogonality to `is_tragic_hero`.

The **Session-7 re-probe** read both encodings clean: `read_on_terms=
yes`, `drift_flagged=[]`, 6/7 and 14/15 annotation reviews approved, 0
rejected. The reader called A22 load-bearing in its own words —
"expressively names them as pathos-centres **without requiring arc
machinery** … cardinality (list) and orthogonality to
`anagnorisis_character_ref_id` both **confirmed as correct**" (Revenger's);
"works here **without strain** … the field's coarseness (names who, not
how or when) **does not impede the read**" (Malfi). **No pathos field
was re-proposed at either site.** OQ-MALFI-3 is the third banked finding
closed by the design→land→re-probe loop.

### 2. The "author-predicted next-OQs falsify" rule held a fourth time

Sketch-07 pre-banked two next-layer OQs — **S7P-OQ1** (an explicit
pathos-*split* signal) and **S7P-OQ2** (distributed-vs-concentrated
pathos typing). The Session-7 probe surfaced **neither** as a demand;
the Malfi read even gently named the S7P-OQ2 shape ("names who, not how
or when") only to say it *does not impede the read*. This is the fourth
consecutive instance of the rule first stated in SoP-16: **probe-surfaced
findings re-confirm; author-predicted next-OQs are reliably falsifiable
and usually unforced.** The instrument for choosing what to invest a
second-site encoding in is now well-calibrated: prefer a finding a probe
has surfaced unprompted (OQ-MALFI-3 qualified; it closed cleanly), not
one we forecast (S6P-OQ1/OQ2, S7P-OQ1/OQ2 — all unforced).

### 3. The probes' attention moved to a coherent next layer

With the pathos-centre closed, both Session-7 probes surfaced new
forcing functions — and they cluster around two themes the dialect has
genuinely not yet typed:

- **Three-party and dead-party relations.** The Revenger's wants a
  `memorial` / `debt` `ArCharacterArcRelation` kind (Vindice → Gloriana:
  a living agent whose whole action is owed to a dead, non-agentive
  character — who is *also* the pathos-centre, so it "would pair
  naturally with `pathos_character_ref_ids`"). Malfi wants a **ternary**
  instrumental (wielder→instrument→victim; Ferdinand→Bosola→Duchess
  exceeds the two-slot `character_ref_ids`). These are the same shape
  from two angles: the relation apparatus presupposes exactly two
  arc-bearing agents, and the corpus keeps needing a third or a
  zero-arc party.
- **The character axis of the peripeteia.** Malfi wants
  `ArMythos.peripeteia_character_ref_id` (parallel to
  `anagnorisis_character_ref_id`) for mythoi where the reversal and the
  recognition land on different characters — A12's binding is temporal
  only; the character split is currently inferred.

Both are recorded as banked S7P findings (see below). Neither is forced
*yet* — each wants its own second-site encoding.

## What is built — delta from sketch-16

### Dialect ledger — A1–A23 (was A1–A21)

- **A22** `ArMythos.pathos_character_ref_ids: Tuple[str, ...] = ()` — the
  pathos-centre. **A23** `ArCharacter.pathos_carrier: bool = False`. Both
  extension-only (prior-preserving defaults); architecture-sketch-02
  GREEN holds through A23.
- **A7.19** `_check_pathos_centre` — four checks (resolution,
  no-duplicates, named⇒flagged advises-review, flagged⇒named noted),
  wired into `verify`.

### Production surface (landed in-arc, not deferred)

- `schema/aristotelian/mythos.json` — `pathos_character_ref_ids` (AS07-2).
- `schema/aristotelian/character.json` — `pathos_carrier` (AS07-3).
- Conformance pins + the `_dump_armythos` / `_dump_archaracter` round-trip
  helpers updated (and the latent sketch-06 `secondary_peripeteia`
  dump-gap fixed in passing).
- `aristotelian_reader_model_client.py` renders both fields + a sketch-07
  system-prompt note (phrased non-leading per the Session-6 "mildly
  leading" critique — it explicitly invites the probe to say the shape
  is wrong or the gap still open).

### Encoding migrations (the de-stretch)

- `revengers_tragedy_aristotelian.py` — A22 tuple + A23 flags;
  `AR_PATHOS_CLUSTER_PARALLEL` retired; action_summary, module docstring,
  and `OQ_MALFI_3_FINDING` de-stretched / marked CLOSED. Verifies clean
  (0 observations). Now ONE arc-relation (was two).
- `malfi_aristotelian.py` — A22 `(ar_duchess,)` + A23 flag;
  `OQ_MALFI_3_FINDING` marked CLOSED. 3 pre-existing noteds, no pathos
  observation.
- `revengers_tragedy.py` (substrate) — one description de-stretched.

### Probe artifacts

- `prototype/reader_model_revengers_aristotelian_session7_output.json`
- `prototype/reader_model_malfi_aristotelian_session7_output.json`

### Test surface

- **test_aristotelian: 232** (+10 sketch-07: A7.19 clean + four violation
  paths + the noted + both migrations + the closure-note pin; one test
  renamed as the cluster relation retired). Conformance **107**. Full
  core sweep green (**1134 tests, 0 failures**).

## The banked-findings ledger after this sketch

- **OQ-MALFI-3** — pathos field. **CLOSED** (sketch-07; verified both
  sites).
- **S7P-OQ3** — `memorial` / `debt` relation kind (living agent → dead
  non-agentive pathos-centre). **NEW, probe-surfaced (Revenger's S7).**
  Strongest new finding; pairs with A22. Forcing site: any tragedy whose
  protagonist's action is owed to a specific dead character (revenge,
  mourning-plays).
- **S7P-OQ4** — `ArMythos.peripeteia_character_ref_id`. **NEW,
  probe-surfaced (Malfi S7).** For cross-character peripeteia↔anagnorisis
  splits. Adjacent to the falsified S7P-OQ1 but distinct (it types the
  peripeteia-bearer, not the pathos-split).
- **S7P-OQ5** — ternary instrumental (`target_of_instrument_ref_id`).
  **NEW, probe-surfaced (Malfi S7).** The OQ-MALFI-4 family; the
  two-slot `character_ref_ids` can't hold wielder/instrument/victim.
- **S7P-OQ6** — `catharsis_mode` / `ArCatharsis` record (audience
  affective trajectory). **NEW, probe-surfaced (Revenger's S7).** Joins
  the long-banked audience-anagnorisis family.
- **OQ-MALFI-1B** — temporal mode on concordant instrumentals. Banked;
  **re-surfaced a third time** (both S7 probes re-proposed a
  `temporal_relation` field). Ripening toward a forcing site.
- **S6P-OQ1** — main-level `anagnorisis_qualifier`. Banked UNFORCED
  (predicted thrice, falsified thrice).
- **S7P-OQ1 / S7P-OQ2** — pathos-split signal / distributed-concentrated
  typing. **Banked UNFORCED** (author-predicted by sketch-07; both
  falsified at Session 7).
- **OQ-MALFI-4, OQ-AP7** — unchanged from SoP-16.

## What's next (research AND production)

### Production track — the generation back-end (now the active swing)

The compiler back-end (`draft_generator.py`) exists and produced a
faithful Oedipus first draft (`8971084`). Per
`feedback_research_production_alternation.md`, the last several commits
are research-heavy (sketch-07); the natural counter-swing — and the move
*toward the project's actual goal* (a free generation tool, see
`project-goal-generation-tool`) — is to **generalize the generator to a
second encoding** (Malfi or Lear), proving the substrate→prose path is
not Oedipus-specific and that the richer Aristotelian apparatus (the
now-landed pathos-centre, secondary peripeteiai, anti-anagnorisis, the
arc relations) is visibly load-bearing in generation. **This is the
immediate next move.**

After that, the decompile-and-verify evaluator (terminus #2) becomes the
quality signal — same reader-model infra, text→substrate instead of
substrate→text.

### Research track

1. **A second-site encoding for the ripest banked finding.** S7P-OQ3
   (memorial/debt relation) is the strongest new probe-surfaced finding
   and pairs with the just-landed A22 — a natural sketch-08 candidate
   once a forcing site is named (a mourning- or revenge-play whose
   protagonist's action is owed to a specific dead character; the
   Revenger's already half-forces it). OQ-MALFI-1B has now surfaced
   thrice and is the other ripe candidate.
2. **S6P-OQ1 / S7P-OQ1 second-site search** — still banked unforced;
   await a clean site, do not force.

### Recommendation

**Generation (generalize the draft generator to Malfi or Lear)** is the
recommended next move: it is the production counter-swing the alternation
rule calls for, it advances the project's stated end goal directly, and
it stress-tests the dialect apparatus (including sketch-07's pathos
field) as *generation input* rather than only as analysis output. The
research loop is in a clean, well-banked state and can wait for a forcing
site to ripen (S7P-OQ3 / OQ-MALFI-1B are the front-runners).

## Context-economy discipline (cold-start continuity)

Rules unchanged from sketches-04 through -16, with the SoP-16 sharpening
reaffirmed and now four-times-confirmed:

- **Probe-surfaced findings re-confirm; author-predicted next-OQs
  usually don't.** OQ-MALFI-3 (probe-surfaced) closed cleanly; every
  author-predicted S*P-OQ to date (S6P-OQ1/OQ2, S7P-OQ1/OQ2) is
  unforced. When choosing a finding to invest a second-site encoding in,
  prefer one a probe surfaced unprompted (S7P-OQ3, OQ-MALFI-1B qualify).

### What a cold-start Claude should read first

1. `design/README.md` — active sketches per topic (the aristotelian
   index is stale past probe-sketch-03; read the sketch files).
2. This doc (`design/state-of-play-17.md`) — current state.
3. `design/aristotelian-sketch-07.md` — the latest landed dialect sketch
   (A22/A23/A7.19), incl. its Session-7 closure-result section.
4. `design/state-of-play-16.md` — supersedes-link; the Revenger's arc +
   OQ-MALFI-3 confirmation + the generation back-end's opening.
5. `prototype/story_engine/core/aristotelian.py` — the dialect, A1–A23.
6. `prototype/story_engine/core/draft_generator.py` — the back-end
   (substrate→prose); `prototype/demos/demo_generate_oedipus.py` +
   `prototype/oedipus_first_draft.md` — the first generation.
7. `prototype/reader_model_revengers_aristotelian_session7_output.json`
   + `..._malfi_..._session7_output.json` — the closure artifacts.
8. `git log --oneline 9a43c1f..HEAD` — the two commits since SoP-16.
