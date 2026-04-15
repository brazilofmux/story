"""
ackroyd_save_the_cat.py — *The Murder of Roger Ackroyd* encoded in
the Save the Cat dialect.

Third encoding at Save the Cat (after Macbeth). Per the plan in
ackroyd-sketch-01, Ackroyd is the dialect's native genre —
Whydunit — and the encoding's value is in demonstrating that Save
the Cat's advertised native-genre fit is real. Where Macbeth's
Rites of Passage fit was the least-bad of ten genres (and the
cross-dialect comparison documented the strain), Ackroyd should
fit cleanly. If it doesn't, *that* is the finding.

Notable features of this encoding:

- **Genre: Whydunit.** Poirot as "the detective"; Sheppard's
  blackmail + murder as "the secret"; the reveal-and-aftermath as
  "the dark turn." Every archetype maps to an authored character or
  structural fact without strain.

- **A story = the investigation; B story = Flora-Ralph love.**
  Mirrors Macbeth's plot-shaped partition (A=political,
  B=marriage). The A story is the external case; the B story is
  the love arc that *motivates* the A's engagement (Flora hires
  Poirot because she loves Ralph and insists on his innocence) —
  textbook B-story-embodies-theme structure.

- **Protagonist-commit at slot 6 lines up cleanly.** Where Macbeth's
  Break Into Two was internal (the commit to kill; slot 6 PENDING
  for substrate lowering because the moment isn't a staged event),
  Ackroyd's slot 6 is Poirot accepting Flora's commission — a
  staged event (E_flora_summons_poirot) with clear participants.
  Save the Cat's structural skeleton assumes a detective-story
  protagonist commit, which Ackroyd provides.

- **Theme: 'The truth will out.'** Poirot-style rationalist
  affirmation. Same AFFIRM resolution as the Dramatic dialect's
  A_truth_recovers; two dialects naming the same claim in their
  respective vernaculars.

- **Compression pattern at the middle.** Ackroyd's substrate
  compresses the investigation into one event
  (E_poirot_investigates); four Save the Cat beats (Fun and Games,
  Midpoint, Bad Guys Close In, All Is Lost) all read different
  phases of that one event. The cross-dialect comparison will call
  this out — the compression is the opposite of Macbeth's
  (substrate-compresses-dialect-expands here vs. dialect-compresses-
  substrate-expands in Macbeth's slot 10).

- **Genre-archetype verification is informational.** Per
  save-the-cat-sketch-01 OQ1, per-genre archetype checking at
  encoding level is deferred. The self-verifier surfaces the genre
  declaration; archetype assignment to specific characters is an
  authorial claim the encoding makes in comments and the reader's
  pattern-matching, not a machine-checked fact in this iteration.

Expected verifier output: 1 NOTED observation (genre_archetypes_
declared, informational — lists whydunit's three archetypes as the
dialect's reminder to the author). Everything else clean.
"""

from __future__ import annotations

from save_the_cat import (
    StcStory, StcBeat, StcStrand, StrandAdvancement, StrandKind,
    GENRE_WHYDUNIT,
)


# ============================================================================
# Strands (S3)
# ============================================================================
#
# A story = the external case: a murder, an investigation, an
# identification of the killer, a moral terminus. This is what would
# be on the Whydunit's cover copy.
#
# B story = the Flora-Ralph love arc: a young woman's conviction
# that her fiancé is innocent, a secret marriage to a parlormaid,
# the love story whose clearing-of-accusation is the A plot's
# emotional spine. Save the Cat's B story traditionally carries the
# theme; in Ackroyd the theme is "the truth will out" — and the love
# arc carries it via the same pattern: Flora's belief in Ralph's
# truth is vindicated only when Poirot's truth-recovery on the A
# plot clears him by naming someone else.

Strand_A_case = StcStrand(
    id="Strand_A_case",
    kind=StrandKind.A_STORY,
    description=(
        "the investigation arc: a widow's suicide opens the story; a "
        "letter in motion names a blackmailer; a murder follows; a "
        "retired detective is engaged; the household's secrets are "
        "exposed one by one; the killer is identified as the "
        "narrator himself; the moral-legal order is restored at the "
        "cost of his suicide. The external plot's shape — setup, "
        "inciting crime, investigation, reveal, aftermath — is the "
        "Whydunit genre's canonical scaffold"
    ),
)

Strand_B_flora_ralph = StcStrand(
    id="Strand_B_flora_ralph",
    kind=StrandKind.B_STORY,
    description=(
        "the love arc: Flora Ackroyd engaged to Ralph Paton; Ralph's "
        "disappearance after the murder makes him the prime suspect; "
        "Flora's conviction of his innocence drives her to engage "
        "Poirot; Ursula's confession reveals Ralph's secret marriage "
        "to her and his reason for going missing; Poirot's eventual "
        "identification of Sheppard clears Ralph publicly. The B "
        "arc's emotional payoff is the vindication of Flora's belief "
        "in Ralph's truth; the theme ('the truth will out') is "
        "embodied by the love's refusal to accept the easy "
        "accusation"
    ),
)

STRANDS = (Strand_A_case, Strand_B_flora_ralph)


# ============================================================================
# Beats — one per canonical slot (S1)
# ============================================================================
#
# 15 canonical slots. Ackroyd's fit against Save the Cat is clean
# enough that every slot has a clear content mapping, though several
# collapse into substrate events that carry multiple beats (the
# investigation sequence in particular).

B_01_opening = StcBeat(
    id="B_01_opening",
    slot=1,
    page_actual=1,
    description_of_change=(
        "King's Abbot, an English village after the Great War; Dr. "
        "Sheppard at home with his sister Caroline; the bell rings "
        "in the night and he is called to the Ferrars house. Village "
        "gossip about the Ferrars marriage has been building for "
        "weeks. The tone is English country domestic; the first "
        "image is of the doctor walking home through the morning "
        "fog, carrying the knowledge his work has just given him"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="establishes the village, the narrator, and the "
                 "death that opens the case",
        ),
    ),
)

B_02_theme = StcBeat(
    id="B_02_theme",
    slot=2,
    page_actual=5,
    description_of_change=(
        "Poirot's thematic claim stands over the whole novel: the "
        "truth will out. Snyder's Theme Stated slot wants a line "
        "spoken early by a non-protagonist; in Ackroyd the theme "
        "is stated by the detective's very premise of having taken "
        "the case — reason applied patiently recovers what "
        "concealment tries to hide. The ironic form is that the "
        "narrator is telling us the theme himself, unknowing of "
        "what it will cost him"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the theme frames the investigation's premise",
        ),
    ),
)

B_03_setup = StcBeat(
    id="B_03_setup",
    slot=3,
    page_actual=8,
    description_of_change=(
        "the village's status quo: Ackroyd the wealthy widower; "
        "Sheppard the trusted doctor; Flora engaged to Ralph Paton; "
        "Raymond the secretary; Parker the butler; Ursula the "
        "parlormaid. The household is introduced; its secrets are "
        "present but not yet surfaced — Ralph and Ursula's marriage; "
        "Parker's blackmail history; Flora's financial need; "
        "Sheppard's practice of blackmail against Mrs. Ferrars. The "
        "setup IS the closed circle the investigation will work "
        "through"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the closed circle of suspects established",
        ),
        StrandAdvancement(
            strand_id="Strand_B_flora_ralph",
            note="Flora-Ralph engagement in place; Ralph's "
                 "relationship to Ursula (secret) in place",
        ),
    ),
)

B_04_catalyst = StcBeat(
    id="B_04_catalyst",
    slot=4,
    page_actual=12,
    description_of_change=(
        "Mrs. Ferrars' suicide overnight. The inciting disruption: "
        "she has left a letter for Ackroyd naming her blackmailer. "
        "The letter is in motion — which means the blackmailer is "
        "minutes from being named. The world is still ordinary on "
        "the surface; the narrator knows better"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the inciting event; all subsequent case-plot "
                 "motion flows from the letter Ackroyd is about to "
                 "receive",
        ),
    ),
)

B_05_debate = StcBeat(
    id="B_05_debate",
    slot=5,
    page_actual=15,
    description_of_change=(
        "the evening at Fernly: Ackroyd announces he has the letter; "
        "Sheppard sits across from him knowing his name is in it. "
        "The Debate slot's dramatic question — what will our "
        "protagonist do? — is internally resolved on one side of "
        "the table while the external dinner conversation plays out. "
        "This is the novel's most sustained piece of performed "
        "composure"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the case's pivot point — the moment before the "
                 "murder",
        ),
    ),
)

B_06_break_into_two = StcBeat(
    id="B_06_break_into_two",
    slot=6,
    page_actual=25,
    description_of_change=(
        "Flora Ackroyd engages Poirot on the morning after the "
        "murder. The Protagonist's choice: the retired detective "
        "crosses the threshold out of his vegetable-marrow retirement "
        "into the case. Every subsequent page is the new world — "
        "the world in which Poirot is investigating. Save the Cat's "
        "Break Into Two slot lands cleanly on a Whydunit: the "
        "detective's commit is the structural pivot"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the Protagonist's commitment; the investigation "
                 "begins in earnest",
        ),
        StrandAdvancement(
            strand_id="Strand_B_flora_ralph",
            note="Flora's love for Ralph is what motivates the "
                 "commission — the B arc drives the A arc's "
                 "engagement",
        ),
    ),
)

B_07_b_story = StcBeat(
    id="B_07_b_story",
    slot=7,
    page_actual=30,
    description_of_change=(
        "the Flora-Ralph love arc surfaces as the novel's moral "
        "engine just after the threshold. Ralph is missing; public "
        "opinion accuses him; Flora refuses the accusation. Her "
        "conviction is the B story's premise — 'the one I love is "
        "telling the truth' — and it carries the novel's theme "
        "under pressure the A plot will spend chapters testing"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_B_flora_ralph",
            note="the B story proper — Flora's belief in Ralph as "
                 "the novel's load-bearing emotional claim",
        ),
    ),
)

B_08_fun_and_games = StcBeat(
    id="B_08_fun_and_games",
    slot=8,
    page_actual=35,
    description_of_change=(
        "Poirot's investigation: interviews with the household, "
        "the procedural pleasures of reason-applied-to-particulars. "
        "Each suspect's private secret surfaces one by one — Flora's "
        "theft of £40, Parker's earlier blackmail attempt, Raymond's "
        "overheard phrase, Major Blunt's reticence about his "
        "feelings for Flora, Ursula's imminent confession. The "
        "'promise of the premise' sequence that any Whydunit reader "
        "opens the book for"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the investigation's procedural middle — the "
                 "pleasures the genre promises",
        ),
        StrandAdvancement(
            strand_id="Strand_B_flora_ralph",
            note="Flora's private fact (the £40 theft) comes out; "
                 "Ursula's secret surfaces soon",
        ),
    ),
)

B_09_midpoint = StcBeat(
    id="B_09_midpoint",
    slot=9,
    page_actual=55,
    description_of_change=(
        "the dictaphone breakthrough: Poirot traces the phone call's "
        "origin, reconstructs the alibi's mechanism, and privately "
        "arrives at the solution. A false victory for Sheppard — on "
        "the surface he is still assistant-Watson; underneath, "
        "Poirot now knows. The A and B stories collide: Poirot's "
        "working-out of the alibi simultaneously clears the red-"
        "herrings (Ralph among them) and names the one person who "
        "could have staged it"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the investigator's private solution arrives; the "
                 "A story's resolution is now inevitable",
        ),
    ),
)

B_10_bad_guys_close_in = StcBeat(
    id="B_10_bad_guys_close_in",
    slot=10,
    page_actual=60,
    description_of_change=(
        "the noose tightens: Ursula confesses the marriage; Ralph's "
        "continued absence is re-read as protection-of-the-innocent "
        "rather than flight-of-the-guilty; Sheppard's unease grows "
        "as the suspect pool narrows to him. The bad guys closing "
        "in are — from Sheppard's POV — Poirot's steady advance; "
        "from the innocents' POV, the relief that the wrong-accuser "
        "crowd is dispersing"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the suspect pool narrows; the only remaining "
                 "candidate is the narrator",
        ),
        StrandAdvancement(
            strand_id="Strand_B_flora_ralph",
            note="Ralph cleared in effect, though not yet publicly; "
                 "the B story's tension drops",
        ),
    ),
)

B_11_all_is_lost = StcBeat(
    id="B_11_all_is_lost",
    slot=11,
    page_actual=75,
    description_of_change=(
        "Sheppard knows he has been solved; Poirot has not yet "
        "spoken, but the evidence is all in place. The 'all is "
        "lost' beat in a Whydunit is felt from the killer's side — "
        "not the detective's. From Sheppard's narrative perspective "
        "(which the reader has been in throughout) this is the rock "
        "bottom: the performance is over; the manuscript he is "
        "writing will not be 'the case Poirot failed' — it will be "
        "a confession"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the case has been solved privately; the public "
                 "reveal is pending",
        ),
    ),
)

B_12_dark_night = StcBeat(
    id="B_12_dark_night",
    slot=12,
    page_actual=78,
    description_of_change=(
        "the quiet beat before the reveal. For Sheppard, a night of "
        "waiting — composition, calculation of what he can control "
        "in the remaining hours, the manuscript's drafting. For "
        "Poirot, the moment of deciding how to close the case — "
        "full arraignment or private mercy. The 'despair before the "
        "answer arrives' slot lands interiorly in a Whydunit; the "
        "substrate does not stage it but the narrative frame holds "
        "it"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the pause; both sides prepare for the reveal",
        ),
    ),
)

B_13_break_into_three = StcBeat(
    id="B_13_break_into_three",
    slot=13,
    page_actual=85,
    description_of_change=(
        "Poirot gathers the cast. The detective commits to the "
        "final approach: the drawing-room reconstruction, the public "
        "naming. The answer is found and the method will be deployed "
        "— 'method, order, and the little grey cells' brought "
        "together for the case's closure"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the commit to the public reveal; the Whydunit's "
                 "drawing-room scene is about to happen",
        ),
    ),
)

B_14_finale = StcBeat(
    id="B_14_finale",
    slot=14,
    page_actual=95,
    description_of_change=(
        "the drawing-room reveal. Poirot walks the cast through the "
        "reconstruction; piece by piece the alibi is disassembled; "
        "the letter, the dictaphone, the phone call, the patient-"
        "of-trust fact — each named in sequence; Sheppard is "
        "identified. The A story climaxes publicly. Ralph is "
        "cleared by the same reveal that names the killer"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the case's public close; the Whydunit genre's "
                 "signature scene",
        ),
        StrandAdvancement(
            strand_id="Strand_B_flora_ralph",
            note="Ralph's public clearing; Flora's belief vindicated "
                 "(the B story's payoff)",
        ),
    ),
)

B_15_final_image = StcBeat(
    id="B_15_final_image",
    slot=15,
    page_actual=110,
    description_of_change=(
        "Sheppard's manuscript's closing paragraph; the overdose "
        "implied; the novel ends on the narrator's own description "
        "of taking his last dose. Mirrors and inverts the Opening "
        "Image: where the novel opened with the doctor walking home "
        "in morning fog carrying knowledge his work had given him, "
        "it closes with the same doctor at the writing desk at "
        "night, having finally given knowledge back — in the form "
        "of a confession that has been the novel all along"
    ),
    advances=(
        StrandAdvancement(
            strand_id="Strand_A_case",
            note="the A story's denouement; case closed on all sides",
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
# theme_statement is the literal claim the Theme Stated beat
# dramatizes. For Ackroyd, Poirot's rationalist claim that patient
# reasoning recovers truth from concealment — the Whydunit genre's
# core thesis.
#
# Genre: Whydunit — the dialect's native fit for this material.

STORY = StcStory(
    id="S_ackroyd_stc",
    title="The Murder of Roger Ackroyd",
    theme_statement="The truth will out.",
    stc_genre_id=GENRE_WHYDUNIT.id,
    beat_ids=tuple(b.id for b in BEATS),
    strand_ids=tuple(s.id for s in STRANDS),
)
