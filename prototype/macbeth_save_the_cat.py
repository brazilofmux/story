"""
macbeth_save_the_cat.py — *Macbeth* encoded in the Save the Cat dialect.

Second encoding of Macbeth at an upper-dialect level (parallel to
macbeth_dramatic.py, which encodes the same play against the Dramatic
dialect). Follows the worked-example table sketched in
`design/save-the-cat-sketch-01.md` under "Worked example: Macbeth".

Pure dialect content. No substrate references; no Lowering records.
Connective machinery (Macbeth-at-Save-the-Cat → substrate) is out of
scope here — that's the subject of a future `lowering-sketch-03` or
companion `macbeth_save_the_cat_lowerings.py`. This file only
exercises the dialect on its own terms.

The encoding's value is twofold:

1. **Dialect validation.** Save the Cat was designed for 21st-century
   commercial screenplays; Macbeth is a 17th-century stage tragedy.
   Encoding Macbeth pressures the dialect on the widest-possible
   distance between target form and authored material. Points of
   strain are surfaced in comments below; they're features, not bugs.

2. **Cross-dialect comparison.** The same play now exists at both
   Dramatic and Save the Cat. A future exercise can run both verifiers
   against both encodings and note what each dialect captures that the
   other misses — the empirical payoff of architecture-sketch-02's
   multi-dialect commitment.

Where Macbeth strains the dialect:

- **B Story is the marriage, which is also the A Story's catalyst.**
  Snyder's B Story is a parallel arc (often a romance) that *carries
  the theme* while the A plot handles external events. Macbeth's
  marriage IS the conspiratorial engine of the A plot; there's no
  meaningful separation. The encoding honors Snyder's shape by naming
  the marriage as the B strand, but the two strands entangle far more
  tightly than the dialect typically expects. This will be visible
  in how many beats advance *both* strands.

- **Theme Stated is not dialogue from a non-protagonist.** Snyder
  conventionally places the thematic line in a non-protagonist's
  mouth early. Macbeth's "Fair is foul, and foul is fair" comes from
  the Witches, who are arguably a supernatural collective rather than
  "a character" in Snyder's sense. The encoding promotes that line to
  `theme_statement`; whether it strictly matches the convention is
  debatable.

- **Genre fit is imperfect.** None of Snyder's ten commercial genres
  fits a pre-modern tragedy cleanly. `Rites of Passage` is the
  least-bad fit — Macbeth's moral descent IS a life-stage transition
  gone wrong ("the wrong way" archetype), his conscience-vs-ambition
  struggle is internal though framed externally, and the "tomorrow"
  soliloquy is an acceptance (of meaninglessness rather than wisdom).
  But it's a stretch. Alternative readings:

    - **Whydunit**: Macbeth as detective of his own motivation;
      prophecy as the secret; descent into tyranny as the dark turn.
      The archetypes map well; the genre's typical investigator
      structure does not.
    - **Monster in the House**: Macbeth himself is the monster;
      Scotland the closed house; regicide the sin. Protagonist-as-
      monster is unusual but defensible for tragedy.
    - **Institutionalized**: the individual vs. the natural order of
      monarchy; the cost of destroying the institution. Fits the
      political dimension but misses the moral-interior center.

  The encoding picks `Rites of Passage` and leaves the alternatives
  in comments. A future encoding variant could exercise the dialect
  by re-encoding under a different genre.

- **Page positions are proportional, not literal.** Save the Cat's
  page targets assume a 110-page screenplay. Macbeth has five acts,
  ~2500 lines, and no pages in Snyder's sense. `page_actual` values
  below are chosen proportionally: they place each beat at roughly
  where Snyder's target would land if the play ran 110 pages, while
  staying strictly monotonic in slot order.

Expected verifier output (the encoding's contract):

- 0 beat_slot_unfilled        (all 15 slots filled)
- 0 multiple_beats_per_slot    (one authored beat per slot)
- 0 page_actual_non_monotonic  (pages increase with slot)
- 0 theme_statement_empty      (set to "Fair is foul, and foul is fair")
- 0 beat_id_unresolved, strand_id_unresolved, genre_unknown
- 0 advancement_strand_unresolved
- 0 multiple_a_strands, multiple_b_strands
- 1 genre_archetypes_declared  (NOTED, informational — lists the
                                 three archetypes Rites of Passage
                                 asks the encoding to exhibit)

One noted observation. Everything else clean.

Run the self-verifier:

    python3 -c 'import macbeth_save_the_cat as m; \
                from save_the_cat import verify, group_by_code; \
                obs = verify(m.STORY, beats=m.BEATS, strands=m.STRANDS); \
                print(f"observations: {len(obs)}"); \
                [print(f"  [{x.severity}] {x.code}: {x.message[:80]}") \
                 for x in obs]'
"""

from __future__ import annotations

from save_the_cat import (
    StcStory, StcBeat, StcStrand, StrandAdvancement, StrandKind,
    GENRE_RITES_OF_PASSAGE,
)


# ============================================================================
# Strands (S3)
# ============================================================================
#
# A story = the external political plot: Macbeth's rise to the throne
# through regicide, his tyranny, his fall to Macduff, Malcolm's
# restoration. This is what would be on the trailer.
#
# B story = the marriage: a conspiracy become partnership become
# isolation become grief. Snyder's B Story typically carries the theme;
# here the marriage does carry the ambition-unmakes-the-ambitious
# claim in its most compressed form (both spouses end dead, the
# partnership itself consumed by what it undertook).

Strand_A_scotland = StcStrand(
    id="Strand_A_scotland",
    kind=StrandKind.A_STORY,
    description=(
        "the political arc: loyal thane receives prophecy, murders his "
        "king, seizes the throne, rules as tyrant, is overthrown by "
        "the rightful heir. Scotland's natural succession is broken "
        "and then repaired. The external stakes are the kingdom's "
        "moral order and its subjects' safety under a usurper"
    ),
)

Strand_B_marriage = StcStrand(
    id="Strand_B_marriage",
    kind=StrandKind.B_STORY,
    description=(
        "the marriage arc: a partnership that begins in shared "
        "ambition, unifies around the conspiracy to kill Duncan, "
        "collaborates through its aftermath, then isolates as Macbeth "
        "acts without his wife, then ends in her death and his "
        "'tomorrow' soliloquy. The marriage carries the theme: the "
        "more ambition succeeds, the less of the marriage remains"
    ),
)

STRANDS = (Strand_A_scotland, Strand_B_marriage)


# ============================================================================
# Beats — one per canonical slot (S1)
# ============================================================================
#
# Per the worked-example table in save-the-cat-sketch-01. Each beat
# declares which strand(s) it advances. Many beats advance both; see
# the docstring's note on the marriage-as-A-plot-catalyst strain.
#
# page_actual positions are proportional against Snyder's 110-page
# canonical sheet (not literal line numbers in the play).

B_01_opening = StcBeat(
    id="B_01_opening",
    slot=1,
    page_actual=1,
    description_of_change=(
        "the heath; thunder; three witches appear and disperse before "
        "any human has entered the play. The world's first register is "
        "supernatural disorder — weather, omens, ambiguity — setting "
        "the tone for everything the play's human action will be "
        "judged against"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="establishes Scotland as a world where the "
                 "supernatural intrudes on political order",
        ),
    ),
)

B_02_theme = StcBeat(
    id="B_02_theme",
    slot=2,
    page_actual=5,
    description_of_change=(
        "the Witches chant 'Fair is foul, and foul is fair' — the "
        "play's thematic claim stated in its opening minutes by "
        "non-protagonist voices. Everything that follows will enact "
        "this inversion: the loyal warrior becomes the tyrant, the "
        "gentle queen becomes the murderer's accomplice, the "
        "prophecy's protection becomes the trap"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="the thematic line names the moral register the A "
                 "plot will be measured against",
        ),
    ),
)

B_03_setup = StcBeat(
    id="B_03_setup",
    slot=3,
    page_actual=8,
    description_of_change=(
        "Macbeth is introduced as Scotland's hero — the thane who "
        "has just won Duncan's war for him. Duncan is the good king, "
        "generous to a fault. The marriage is established: Macbeth "
        "writes home immediately upon hearing the prophecy. The "
        "status quo is a capable warrior loyal to a kind king, "
        "married to an equal partner. Everything the play will break "
        "is introduced as intact"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="Scotland's political order shown intact — the "
                 "baseline the regicide will destroy",
        ),
        StrandAdvancement(
            strand_id="Strand_B_marriage",
            note="the marriage shown as a real partnership — the "
                 "baseline against which the isolation of Acts 3-5 "
                 "will be visible",
        ),
    ),
)

B_04_catalyst = StcBeat(
    id="B_04_catalyst",
    slot=4,
    page_actual=12,
    description_of_change=(
        "the Witches deliver the first prophecy: thane of Glamis, "
        "thane of Cawdor, king hereafter. Within minutes, the Cawdor "
        "half is confirmed by royal messengers — the prophecy has "
        "already partly come true. The status quo is disrupted not "
        "by an external event (a knock at the door) but by an "
        "internal event (ambition named and given a path)"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="the inciting incident of the political plot — a "
                 "claim on the throne has been introduced",
        ),
    ),
)

B_05_debate = StcBeat(
    id="B_05_debate",
    slot=5,
    page_actual=15,
    description_of_change=(
        "Macbeth's hesitation meets Lady Macbeth's pressure. 'If it "
        "were done when 'tis done, then 'twere well it were done "
        "quickly' — the debate rendered as concrete dramatic question "
        "(should I kill the king under my own roof?), answered "
        "through his wife's iron counter-arguments. The debate is "
        "both spouses' first joint project"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="the political question hangs — will the thane act "
                 "on the prophecy?",
        ),
        StrandAdvancement(
            strand_id="Strand_B_marriage",
            note="the marriage's first test — will the partnership "
                 "override the husband's moral hesitation?",
        ),
    ),
)

B_06_break_into_two = StcBeat(
    id="B_06_break_into_two",
    slot=6,
    page_actual=25,
    description_of_change=(
        "Macbeth commits: 'I am settled, and bend up each corporal "
        "agent to this terrible feat.' The choice is crossed. "
        "Everything from here is the new world — the world in which "
        "this thane is going to murder his king"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="the threshold crossing: the political plot now has "
                 "an actor committed to regicide",
        ),
        StrandAdvancement(
            strand_id="Strand_B_marriage",
            note="the marriage fuses around the committed plan — "
                 "at this point spouses are most unified",
        ),
    ),
)

B_07_b_story = StcBeat(
    id="B_07_b_story",
    slot=7,
    page_actual=30,
    description_of_change=(
        "the marriage surfaces as the play's moral engine just after "
        "the threshold. Lady Macbeth handles logistics; Macbeth's "
        "resolve wobbles; her 'unsex me here' earlier in the act "
        "is cashed here as practical command. The B story is the "
        "marriage's full conspiratorial unity — the moment the "
        "partnership is most effectively one"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_B_marriage",
            note="the B story introduced as a distinct locus — this "
                 "marriage is its own arc, not just the A plot's "
                 "engine",
        ),
    ),
)

B_08_fun_and_games = StcBeat(
    id="B_08_fun_and_games",
    slot=8,
    page_actual=35,
    description_of_change=(
        "Duncan is murdered in his sleep; Lady Macbeth smears the "
        "grooms with blood; the sons flee; Macbeth is crowned. This "
        "is the 'promise of the premise' sequence — the prophecy's "
        "first half has literalized. Macbeth navigates the new world "
        "(kingship) without yet fully bearing its costs. But the "
        "dagger speech and 'Macbeth shall sleep no more' hint the "
        "costs are already being accrued"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="the regicide is accomplished; natural succession "
                 "is broken; the usurpation is fact",
        ),
        StrandAdvancement(
            strand_id="Strand_B_marriage",
            note="the marriage executes its first joint act; she "
                 "handles the aftermath while he unravels",
        ),
    ),
)

B_09_midpoint = StcBeat(
    id="B_09_midpoint",
    slot=9,
    page_actual=55,
    description_of_change=(
        "Macbeth crowned; the new court established; false victory. "
        "The stakes raise and the A and B stories collide: the "
        "prophecy also named Banquo's line as future kings, which "
        "means the prize Macbeth has seized is temporary. From here, "
        "every action will be to protect a throne whose loss is "
        "already foretold"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="the false stability — the kingdom has a king "
                 "again, but the king is a usurper and knows his "
                 "tenure is foretold to end",
        ),
    ),
)

B_10_bad_guys_close_in = StcBeat(
    id="B_10_bad_guys_close_in",
    slot=10,
    page_actual=60,
    description_of_change=(
        "Banquo murdered (Fleance escapes); the banquet ghost "
        "breaks Macbeth's public composure; he returns to the "
        "Witches for the second prophecy. Pressure mounts — from the "
        "supernatural (the ghost, the new prophecies), from the "
        "political (Macduff's absence becomes suspicion), from the "
        "internal (Macbeth's sleep gone, his wife's influence "
        "waning). The Macduff family is slaughtered offstage: the "
        "moral nadir"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="the bad guys (here the forces of restoration, "
                 "from Macbeth's POV) close in: Macduff flees to "
                 "England, Malcolm raises an army, Scotland bleeds",
        ),
        StrandAdvancement(
            strand_id="Strand_B_marriage",
            note="the marriage isolates: Macbeth orders Banquo's "
                 "death without telling Lady Macbeth; at the "
                 "banquet she cannot reach him through the crack",
        ),
    ),
)

B_11_all_is_lost = StcBeat(
    id="B_11_all_is_lost",
    slot=11,
    page_actual=75,
    description_of_change=(
        "Lady Macbeth dies offstage — her sleepwalking was the last "
        "sign of the self that ambition had unmade; her death (cause "
        "unspecified, suicide implied) is the rock bottom. The B "
        "story's protagonist is gone. Macbeth is alone with what he "
        "has become"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_B_marriage",
            note="the B story's terminal event — the partner is "
                 "dead, the marriage ended not with conflict but "
                 "with the simple removal of the other person",
        ),
    ),
)

B_12_dark_night = StcBeat(
    id="B_12_dark_night",
    slot=12,
    page_actual=78,
    description_of_change=(
        "'Tomorrow, and tomorrow, and tomorrow' — Macbeth's response "
        "to news of his wife's death. Not grief, exhaustion; not "
        "despair, deflation. Life is a tale told by an idiot, full "
        "of sound and fury, signifying nothing. The despair before "
        "the insight — except the insight that arrives is not "
        "redemption but recognition of meaninglessness"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="the tyrant's interior collapses even as the "
                 "external forces arrive at his gate",
        ),
    ),
)

B_13_break_into_three = StcBeat(
    id="B_13_break_into_three",
    slot=13,
    page_actual=85,
    description_of_change=(
        "news arrives that Birnam Wood is moving toward Dunsinane — "
        "the second prophecy's first 'impossible' protection has "
        "literalized against Macbeth. He arms himself anyway. The "
        "answer is found: the prophecies were traps, not shields. "
        "He commits to the final approach — not with the lesson the "
        "story has taught, but in defiance of it ('at least we'll "
        "die with harness on our back')"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="the tyrant commits to the final confrontation; "
                 "Scotland's restoration now has a moving army at "
                 "the castle gate",
        ),
    ),
)

B_14_finale = StcBeat(
    id="B_14_finale",
    slot=14,
    page_actual=95,
    description_of_change=(
        "Macbeth faces Macduff in single combat. He boasts of the "
        "prophecy's last protection ('none of woman born shall harm "
        "Macbeth'); Macduff reveals the Caesarean birth ('from his "
        "mother's womb untimely ripped'); the last protection "
        "collapses. Macbeth fights anyway and is killed. The A and "
        "B stories resolve together — the political plot by the "
        "tyrant's death; the marriage plot by the husband joining "
        "the wife he lost"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="the tyrant killed; the political plot's climax — "
                 "usurpation answered by the rightful heir's sword",
        ),
        StrandAdvancement(
            strand_id="Strand_B_marriage",
            note="the marriage's final closure — both spouses now "
                 "dead, the partnership that opened the play ended "
                 "in matched annihilation",
        ),
    ),
)

B_15_final_image = StcBeat(
    id="B_15_final_image",
    slot=15,
    page_actual=110,
    description_of_change=(
        "Malcolm crowned at Scone. The lords gather; the rightful "
        "succession is restored; the kingdom names its new king. "
        "Mirrors and inverts the Opening Image — where Act 1 opened "
        "on supernatural disorder and an absent king, the play "
        "closes on political order and a present, acknowledged king. "
        "The world has changed by being restored"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_scotland",
            note="the political plot's denouement — natural "
                 "succession reasserted; Scotland can begin again",
        ),
    ),
)

BEATS = (
    B_01_opening, B_02_theme, B_03_setup, B_04_catalyst, B_05_debate,
    B_06_break_into_two, B_07_b_story, B_08_fun_and_games,
    B_09_midpoint, B_10_bad_guys_close_in, B_11_all_is_lost,
    B_12_dark_night, B_13_break_into_three, B_14_finale,
    B_15_final_image,
)


# ============================================================================
# Story root (S4, S5)
# ============================================================================
#
# theme_statement is the literal line the Theme Stated beat dramatizes,
# promoted to Story level per S4. For Macbeth the line is the Witches'
# "Fair is foul, and foul is fair" — an inversion claim the play's
# subsequent action will enact in detail. (The ambition-unmakes-the-
# ambitious reading, used in macbeth_dramatic.py's Argument, is a
# thematic gloss; the dialect asks for the literal line Snyder's Theme
# Stated beat conventionally carries.)
#
# Genre: Rites of Passage. Macbeth's moral descent is a life-stage
# transition taken the wrong way. See docstring for why this is the
# least-bad fit and for the alternatives considered.

STORY = StcStory(
    id="S_macbeth_stc",
    title="Macbeth",
    theme_statement="Fair is foul, and foul is fair.",
    stc_genre_id=GENRE_RITES_OF_PASSAGE.id,
    beat_ids=tuple(b.id for b in BEATS),
    strand_ids=tuple(s.id for s in STRANDS),
)
