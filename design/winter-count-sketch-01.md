# winter-count-sketch-01 — the anti-marketing tragedy

**The claim this piece exists to make:** the engine can hold a story
shape that every commercial instinct — and every note a draft would
normally accumulate — pulls away from, and can *prove* it held it,
scene by scene, with the blind-reading evaluator as witness.

## The shape

THE WINTER COUNT (`encodings/winter_count.py` +
`winter_count_dramatica_complete.py` + `demos/demo_generate_winter_count.py`).
An original Vastisetr story — same town as The Price of Warmth, two
generations earlier; the Beehive alehouse stands in both.

The storyform is the Failure × Bad corner, fully committed:

| axis | choice | the note it refuses |
|---|---|---|
| Resolve | **steadfast** | "give her an arc" |
| Growth | stop | "let her learn in time" |
| Approach | do-er | — |
| Style | **linear** | a ledger mind; the tragedy is arithmetic |
| Driver | **decision** | "have the storm do it" — no; people decide |
| Limit | optionlock | ration → seed → the pass → the raid → nothing |
| Outcome | **failure** | "save the town in the third act" |
| Judgment | **bad** | "give the ending hope" |

`canonical_ending(failure, bad) = "tragedy"` — and the companion
storyform (Price of Warmth) lands `success × good` from the IDENTICAL
four-domain grid (OS=Situation, MC=Fixed-Attitude, IC=Manipulation,
RS=Activity). One town, one grid, opposite polarity. The pair — not
either story alone — is the demonstration.

## Where the substrate earns its keep

The tragedy's engine is the knowledge discipline, not any event:

- `E_rot_found` retracts `stores_enough(granary)` from the WORLD while
  exactly one mind (`halla`) learns `rot(granary)`. The town's belief —
  held CERTAIN, via utterance-heard, from the public count — is
  thereafter false, and the substrate knows it is false.
- `E_pass_vote` is the hinge: every voter reasons **correctly** from
  what they hold, and the vote closes the town's one exit. No villain,
  no idiot ball — a rational catastrophe, checkable from the Held
  records.
- The sibling knowledge-lock: after `E_shortfall`, Halla cannot expose
  Eirik's forged chit without an audit exposing her false total. Her
  lie shields his theft; his theft hostages her lie. No scene states
  this; it FOLLOWS from who knows what, when.
- One flashback (`E_ketil_fall`, τ_s=−7300, staged fifth): the reader
  learns why the lie is unthinkable in the same hour they watch her
  tell it.

## The marketing imperatives, violated on purpose

1. Save-the-cat inverted: her first significant act is refusing a
   starving family, without cruelty — which is worse.
2. No arc: the last scene is the first scene (a woman at a table,
   counting), with the town dead around it.
3. No villain: Kol is hungry, Eirik is merciful, Jorunn is careful,
   Halla is principled. The antagonist is arithmetic.
4. The child dies; the rescue vote fails rationally; the granary burns
   in a riot nobody wanted; the IC dies on the ice being the help
   nobody sent for; the thaw brings traders, not meaning.
5. Judgment stays bad: no lesson, no tear, no absolution — the count
   is perfect at last, and it counts the dead.

Why it should still work: a fifteen-scene dread runway of pure
dramatic irony (the reader carries the rot from scene three), strict
decision-driven causality after the opening freeze, an optionlock that
narrows audibly, and an ending inevitable in retrospect. The oldest
contract there is, kept to the letter.

## Status

- Encoding, storyform, demo, and structural tests
  (`tests/test_winter_count.py`) all landed; dry-run bible and briefs
  verified offline. 17 events, 17 staged scenes, acts AUTHORED (not
  positional), every scene carrying a texture note.
- Generation/convergence run pending an `ANTHROPIC_API_KEY` in the
  environment:
  `.venv/bin/python3 -m demos.demo_generate_winter_count --converge
  --save-md winter_count_first_draft.md`
- The evaluator-side fixes that make the Failure×Bad corner *checkable*
  (ending-shape cell comparison instead of word-bag overlap; resolve
  vocabulary normalization) landed alongside — before them, a draft
  that drifted from tragedy to triumph could score `preserved`.
