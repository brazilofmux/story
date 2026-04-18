# Timelock or Optionlock? Real Stories Don't Pick One.

*What an LLM probe found when I asked it to check my narrative-structure verifier against four actual stories.*

---

## 1. The Rulebook

Dramatica is a narrative theory used mostly by screenwriters. It has a rule called DSP_limit. Every story, the theory says, is driven to its climax by one of two forces: **Optionlock** (the hero runs out of alternatives until only the true answer remains — Agatha Christie territory) or **Timelock** (the clock counts down to a scheduled event, and the hero has to be ready when the bell rings — *Rocky* territory). Pick one.

This is a theorist's love. Binary choices are computable. Four Dramatica binary choices across eleven axes locate your story in the theory's famous 16,384-storyform grid.

Writers who've encoded actual stories know a secret: most stories don't honor the binary. A murder mystery narrows options AND the victim's blood is getting cold. A heist is a deadline AND options foreclose as the guards move. *Oedipus Rex* eliminates explanations one by one (Optionlock) and the plague is killing the city (Timelock). *Macbeth* narrows Macbeth's alternatives (Optionlock) and Duncan visits on a specific night; prophecies collapse in sequence at the climax (Timelock).

This is an article about what happens when you encode four real stories in a formal verifier, ask an LLM to read your verifier's verdicts, and iterate. By the fifth pass the LLM started suggesting that real stories might not pick one — that the theory is tighter than the substrate sustains. The observation is provisional: two encodings have surfaced it; a candidate sketch to formalize compound pressure is banked as a next step. But it's the most interesting signal from six passes, and worth taking seriously.

---

## 2. What I'm Building

A story-telling engine whose structural layer is mechanical and checkable, while the affective layer — tone, texture, meaning — stays human. The schema catches structural drift (who killed whom, who knows what when, what branches exist); a human reader catches affective drift (whether a scene works emotionally). I call this the grid-snap commitment. Two surfaces, two failure modes, two kinds of verification.

The engine is a stack. At the bottom, an event-based substrate where every story is an ordered set of typed events with effects on the world and on agents' knowledge. Above that, three upper dialects — Dramatic (parameterized, role-driven), Save the Cat (prescriptive, beat-driven), and a full Dramatica-Complete template encoding Dramatica's Grand Argument Story theory as data. Machinery binds upper-dialect records to substrate facts. Verifiers run at the boundaries. The Dramatica verifier runs nine checks per encoding — domain assignments, pressure shapes, judgments, growths, goals — each producing a verdict with a match-strength score.

So far: ~600 tests, four stories fully encoded through both the substrate and the Dramatica upper dialect — *Oedipus Rex*, *Macbeth*, *The Murder of Roger Ackroyd*, *Rocky* — plus a fifth, *Rashomon*, encoded at the substrate layer for its four-contested-branches structure. The probe/verifier loop in this article runs against the four dual-encoded stories (they're the ones with both surfaces). At the dialect-layer alone the corpus is broader — seven stories including *Pride and Prejudice* and *Chinatown* — and closes the full Dramatica Outcome × Judgment matrix there. Research, not a product. I expect to spend twenty years on it.

---

## 3. The Partnership

The verifier is mechanical. For each check it reads the substrate and returns a verdict. Most of the time, the verdict is right. Sometimes it's wrong, or right-but-for-the-wrong-reason.

The probe is an LLM — Claude Opus, as it happens. I feed it the verifier's output plus the encoded story's records and ask it to *review the verifier's reviews*. It can endorse a verdict (well-grounded), qualify it (the verdict stands but needs a note), or dissent (wrong, here's why).

I didn't expect much. What would an LLM reviewing a mechanical checker's reviews actually catch?

It caught the verifier using the wrong signals, repeatedly, in ways it could specify.

Concrete example. *Rocky* is a Timelock story — the fight is scheduled, Rocky has to be ready. My DSP_limit check looked for convergence signals (world-fact retractions, identity collapses, rule-derived compounds emerging mid-arc). If it found none, it reported "consistent with Timelock but not affirmatively detected." If it found any, it reported disagreement.

Rocky's substrate had two convergence signals: a retraction (Mac's scheduled fight is cancelled when Mac breaks his hand) and a rule-derived compound (`went_the_distance` derives at the final bell from `fought_rounds = 15` plus `standing_at_final_bell`). My verifier called it NEEDS_WORK at strength 0.33 — Timelock declared, but the substrate looked Optionlock-shaped.

The probe dissented:

> The Timelock assignment is well-supported by the narrative and substrate structure. The fight is scheduled at a fixed date; the entire training arc is explicitly deadline-driven preparation; the fight itself is fifteen rounds — a temporal limit. The 'convergence shape' the check detects (retraction:1 from Mac's injury removing him; rule-emergence:1 from WENT_THE_DISTANCE_RULE) are not Optionlock signatures — they are setup mechanics and consequence derivations, respectively. Mac's injury doesn't remove an option from Rocky; it creates the temporal setup. The rule-emergence is a post-limit evaluation, not a limit mechanism.

And in the suggested-signature field:

> Consider adding a signature for scheduled temporal endpoints: when a scheduling-type event establishes a future date and the story's progression converges toward that date with training/preparation events filling the interval, this is a positive Timelock indicator.

Three hours later I'd written a design sketch — arc-position banding for the signals (so pre-plot setup doesn't count like middle-arc convergence) plus a scheduling-predicate recognition rule. Implementation: about forty lines. Rocky's DSP_limit shifted from **NEEDS_WORK 0.33 → APPROVED 1.00**. Zero substrate changes. The probe's reading had been right; the verifier's predicate had been the problem.

This is the partnership pattern. The probe names a structural gap. I write a sketch committing the fix. The measurement shifts.

---

## 4. Seven Shifts in Two Days

After Rocky I did the obvious thing and ran the same probe against the other three encodings. Each surfaced a different structural gap. Each got a sketch.

| Story | What shifted |
|---|---|
| Rocky | DSP_limit NEEDS_WORK 0.33 → APPROVED 1.00 |
| Oedipus | DSP_growth PARTIAL 0.50 → APPROVED 1.00 |
| Oedipus | Story_goal PARTIAL 0.70 → APPROVED 1.00 |
| Ackroyd | DA_mc PARTIAL 0.54 → APPROVED 0.85 |
| Macbeth | DA_mc PARTIAL 0.69 → PARTIAL **0.65** |

Sit on that last row. *Macbeth's* number went *down*. PARTIAL 0.69 → PARTIAL 0.65. After I adopted the probe's suggestion — weight events by beat type, so inciting prophecies and midpoint ghosts count more than rising-action murders — the measurement honestly dropped. The probe had said *"the 0.69 strength may even be generous"* — and it was.

This is the second thing the partnership does. It doesn't just propose fixes that raise verdicts. Sometimes the right answer is for the number to drop, because the old number was overstating what the substrate supported.

Then a cross-corpus moment. All four stories' DSP_resolve checks got qualified on the same axis: *Dramatica's Resolve is about whether the main character changes in response to the Impact Character's influence. Your checks measure MC state in isolation. That's not the same thing.* Four independent qualifications, one architectural gap. I wrote a sketch that added a temporal-correlation check between each MC inflection moment and the nearest preceding Impact-Character throughline event. All four verdicts held at APPROVED; all four comments now carry the relational signal.

Seven sketches in two days. Four measurement shifts (three up, one honestly down). Three additive-signal enrichments.

---

## 5. The Plateau

I kept running probes. This is the part I wasn't expecting.

After the seventh sketch landed, the probe's commentary distribution stopped changing much. Six passes exist now, each covering the same four stories. Here's the aggregate:

| Pass | Annotations approved | Endorsed | Qualified | Dissented |
|---|---|---|---|---|
| v1 | 90 | 27 | 7 | **2** |
| v2 | 88 | 28 | 8 | 0 |
| v3 | 90 | 29 | 7 | 0 |
| v4 | 89 | 29 | 7 | 0 |
| v5 | 92 | 28 | 8 | 0 |
| v6 | 92 | 28 | 8 | 0 |

Two observations. First: the loop converges. V5 and V6 are distribution-identical. Dissents vanish after v1 — the probe's substantive disagreements all get captured in sketches by pass two.

Second: the loop converges *at a rate*, not at silence. The probe keeps finding things. The qualifications shift in content each pass, but the total stays in the 7–8 range (settling at 8 in v5 and v6). The partnership isn't going to fall silent because the sketches have landed. Under the current corpus and verifier it keeps producing signal at roughly this rate — until something about the stories, the probe, or the verifier fundamentally changes.

I expected the probe to eventually agree with the verifier on everything once the sketches landed. It doesn't. Instead, it *calibrates*. As the verifier improves, the probe's standard improves in lockstep. The floor moves up.

There's a name for this kind of partnership. It's called editorial review.

---

## 6. Bar-Raising

Let me show you what I mean.

In pass four I noticed Ackroyd had a persistently-flagged annotation — `L_blunt`. Major Blunt is the retired officer in Christie's novel who becomes Poirot's informal informant. His Dramatica function is "Sidekick." My record bound him to the substrate entity. My annotation read, in full: `"C_blunt (Sidekick) → Entity 'major_blunt'."`

The probe's finding, four passes in a row, paraphrased: this is the thinnest annotation in your Ackroyd encoding. Every other function-bearing character explains how the function manifests — how Caroline's conviction drives Poirot's engagement, why Raglan's skepticism is institutional, what role Ralph's disappearance plays. L_blunt just says "Sidekick" and points at an entity. The function is structurally unjustified.

I expanded the annotation to about eighty words. Named the events Blunt participates in. Grounded the Sidekick function in his quiet support of Flora's conviction. Explained the household-credibility role.

The next probe pass endorsed L_blunt. *And then raised the bar on two other Lowerings* — `L_banquo` and `L_malcolm` in Macbeth. Both equally thin. Both previously endorsed. The probe had calibrated its standard to the new Ackroyd-L_blunt example.

I fixed those. The pass after that raised the bar to `L_duncan`, `L_lady_macduff`, `L_fleance` — Macbeth characters *without* declared functions. One-line identity bindings. My reasoning had been "characters without function labels don't need function-justification." The probe disagreed: every character Lowering should carry substrate-grounded context, not just a binding.

This is bar-raising. A third thing the partnership does, alongside architectural findings and implementation refinements. The probe's quality floor tracks the corpus's best example. Fix one thing to a high standard and the probe pulls the rest up behind it.

Useful property. I can't coast. If I want the corpus to stay at its current quality I have to keep up with the probe. If I want it to get better I improve one thing past the probe's current standard, and the floor rises.

---

## 7. The Compound Pressure

Now: the finding I promised.

Run the probe for six passes and you accumulate a lot of commentary. Most of it is story-specific. Some isn't. Some is a *pattern* across stories.

In pass five the probe said something on Oedipus that stopped me. It was qualifying the DSP_limit check — the same check that had shifted to APPROVED via Optionlock-shape detection in pass two. The qualification:

> The optionlock reading is directionally correct — Oedipus Rex narrows alternatives until only the terrible truth remains. However, the plague introduces a timelock pressure (the city is dying; urgency).

Pass six, same pattern, different story:

> The Optionlock verdict is defensible — Macbeth's options do narrow as the arc proceeds. However, there is a plausible Timelock counter-reading: the play's tension also derives from temporal pressure — Duncan's visit creating a time-window…

Two encodings. Two independent passes. Same hypothesis: *maybe the story has both pressure shapes, not one*.

Dramatica says pick one. The DSP_limit axis is binary.

The probe's suggestion, in effect: some stories may carry both pressures simultaneously.

Read Oedipus's substrate: the plague is a timer, genuinely running out. At the same time, Oedipus is narrowing options on his investigation. Both pressures are structurally detectable in the fabula; both are dramatically present on the page. If the probe's reading holds, Sophocles didn't pick one.

Macbeth is harder to see, but the probe makes the case. Options narrow (Banquo gone, Macduff defected, Lady Macbeth unraveled, prophecies collapsing, Birnam moving). And time squeezes: Duncan's specific-night visit is the window when the murder has to happen; the prophecies collapse in sequence at the climax; the fight is now.

Why does Dramatica say pick one? Because binary is computable. Four binary choices across eleven axes gives you the famous 16,384 storyforms. Allow compound pressure-shape and your storyform-space doubles at that axis, or becomes continuous (which is worse), or requires a whole new compound-axis vocabulary. The theory's elegance depends on the binary.

The partnership's suggestion — still provisional, two encodings in — is that the theory's elegance is a property of the theory, not of stories. The substrate, populated with actual story events, carries enough structural information to *detect* compound pressure: two mechanisms generating convergence simultaneously. The probe noticed. I hadn't. A third encoding surfacing the same pattern would make this a finding rather than a hypothesis.

The sketch on the docket — if it lands — would formalize compound pressure as a third classification alongside Optionlock and Timelock. That doesn't break the Dramatica frame; it *softens* it. A story could be 80% Optionlock with a 20% Timelock dimension, or the reverse. The verifier would report both ratios. The author's DSP_limit choice would still name which pressure the author is *centering* — but the verifier would stop pretending the other dimension isn't there.

This is one of the things the partnership does. It surfaces places where the formalization may be tighter than the substrate sustains, and hands me candidate sketches to soften them *without breaking the theory's useful frame*.

---

## 8. The Methodology

I started the project with an old assumption. If I formalize Dramatica theory in a story-verification engine, the engine will *enforce* Dramatica. Stories that don't fit will fail verification. My job is to build a sharp, rigorous formalization and let the sharpness do the work.

The probe/verifier partnership does something different.

You formalize the theory and write sketches — commitment artifacts that name what the verifier checks and why. You encode a few real stories. You run the verifier. Then you add the LLM probe, feed it the output and the story, and ask it to find disagreement.

It does. Not because the probe knows Dramatica better than you do — it doesn't. It knows Dramatica *worse*. It knows *stories* in a way the verifier doesn't. The verifier has the theory's letter; the probe has read enough narrative to feel the theory's pressure points.

You write sketches that close the probe's findings one at a time. Each takes an hour or two. Each shifts a measurement. Seven in my two days. You re-run the probe. Some findings resolve; new ones surface — refinements of earlier findings, or cross-corpus patterns that only show up once per-encoding noise has quieted. You land more sketches.

Eventually the probe converges to a plateau. It's still finding things. The rate is stable. The distribution is stable. The content shifts each pass, but the total stays at about eight non-endorsements per four-story pass — roughly 22% of the 36 commentaries generated by the 9-check verifier across all four encodings. This is not the signal running out. This is the partnership arriving at its steady state.

And then, at the plateau, something new. The probe surfaces *architectural observations about the theory itself*. Not "the verifier is wrong about Macbeth's domain assignment" but "Dramatica is tighter on DSP_limit than real stories support." The probe isn't finding verifier bugs anymore. It's finding theory pressure points.

This is not enforcement of the theory. It's calibration of the theory against the stories. The formalization becomes a dialog between the theoretical commitment and the substrate record. The sketches are the dialog's artifacts.

I think this is how structural narrative theory gets done now. Not "argue the theory." *Run* the theory against encoded stories, with an LLM partner, and let the pressure points surface.

---

## 9. Coda

Honest limits. Four stories isn't a lot. A sample that small can pattern-match but can't generalize — the compound-pressure finding is provisional until more encodings surface it. (Two already have.) The probe is non-deterministic. Across six passes the distribution is stable, but a single pass is noisy; anyone reproducing specific findings should run multiple passes. This is research, not a product. The substrate is Python-as-specification — each encoding takes a full session or two to write by hand. "Apply this to any story you want" isn't possible yet.

That said, the partnership pattern — LLM probe reviewing a rigorous formalization's output, sketches as commitment artifacts, the plateau as a convergence signal, bar-raising as an emergent quality property — feels portable. Any field where a checkable formalization is run against a stressing corpus might show a similar shape. I haven't tested that. The honest version: this is what happened in *this* project, and I'd expect the pattern to at least rhyme elsewhere.

The Oedipus/Macbeth compound-pressure finding started as a specific probe commentary on two encodings. If a third encoding surfaces the same pattern, it becomes a candidate theoretical claim: that Dramatica's DSP_limit axis is binary-because-of-computability, not binary-because-of-stories. That would be a finding. Right now it's a hypothesis, emergent from the partnership, not visible at either end alone.

The repo is public: [github.com/brazilofmux/story](https://github.com/brazilofmux/story). The reasoning-over-time is preserved — nineteen active sketches, six probe passes, every measurement shift documented in commit messages. If someone in 2030 wants to think seriously about this problem, everything's there, including the arguments I lost.

This is a ~20-year personal project. I'm in the first week.

The clock is ticking AND the options are narrowing. Compound pressure. Real life.
