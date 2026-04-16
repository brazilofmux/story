"""
pride_and_prejudice_dramatic.py — *Pride and Prejudice* encoded in the
Dramatic dialect.

Fourth encoding at the Dramatic dialect level (after Oedipus, Macbeth,
Ackroyd). Records the novel's argumentative structure: one Argument,
four Throughlines under the dramatica-8 Template, nine Characters,
ten Scenes, four Stakes records, twenty Beats.

Pure dialect content. No substrate references; no Lowering records.
This encoding pressures the Dramatic dialect in directions neither
tragedy nor Whydunit touched — it is the corpus's first non-tragic
story and its first Triumph (Outcome=Success, Judgment=Good).

Notable features the encoding exercises:

- **Female Protagonist + MC.** Elizabeth Bennet carries both the
  Protagonist function slot and the main-character Throughline. First
  female MC in the corpus; first MC whose problem is an *attitude*
  rather than an action.

- **Prejudice as Fixed Attitude.** Elizabeth's "first impressions"
  (Austen's working title) are a fixed attitude she applies to Darcy,
  Wickham, and her sisters' suitors. The MC Throughline is about the
  slow dissolution of that attitude under accumulating evidence.

- **Comedic resolution with real stakes.** Pride and Prejudice is
  structurally a comedy (marriages at the end), but the stakes are
  genuine — the entailed estate threatens the Bennet family's
  survival, Lydia's elopement threatens the family's honor, Wickham's
  earlier conduct threatens Georgiana. The novel earns its comic
  ending through real jeopardy.

- **Ensemble quality without overwhelming cast.** Multiple courtship
  subplots (Jane/Bingley, Lydia/Wickham, Charlotte/Collins) all feed
  the central Argument. The dramatica-8 slots distribute across the
  Bennets and their orbit without requiring an abstract Throughline
  owner.

- **IC who manipulates events.** Darcy's impact on Elizabeth comes
  not just from his philosophical opposition but from his actions —
  separating Bingley from Jane (wrong), paying off Wickham (right).
  His Throughline is in the Manipulation domain.

- **No double-function characters.** Unlike Macbeth (Protagonist +
  Emotion on one character) or Ackroyd (Protagonist + IC on Poirot,
  MC + Antagonist on Sheppard), Pride and Prejudice's dramatica-8
  slots map 1:1 to characters. Darcy is Guardian + IC, which is a
  role-label + function-label pairing (not a double function_label).

Expected verifier output (the encoding's contract):

- 0 slot_unfilled / slot_overfilled (all 8 dramatica-8 slots filled).
- 0 throughline_no_stakes (all 4 Throughlines have Stakes).
- 0 id_unresolved, no orphans, no duplicate positions.
"""

from __future__ import annotations

from dramatic import (
    Story, Argument, Throughline, Character, Beat, Scene, Stakes,
    ArgumentContribution, SceneAdvancement, StakesOwner,
    ResolutionDirection, ArgumentSide, StakesOwnerKind,
    THROUGHLINE_OWNER_SITUATION, THROUGHLINE_OWNER_RELATIONSHIP,
)


# ============================================================================
# Argument
# ============================================================================

A_prejudice_dissolves = Argument(
    id="A_prejudice_dissolves",
    premise=("a fixed attitude formed on first impression can be "
             "dissolved by patient attention to the evidence, when "
             "the attitude-holder is willing to revise"),
    counter_premise=("first impressions are reliable; the heart knows "
                     "what the senses have reported; to revise is to "
                     "be manipulated. Mrs. Bennet voices a caricature "
                     "of this position (all her first impressions are "
                     "marriage-arithmetic); Lady Catherine voices the "
                     "authoritarian form; Elizabeth herself voices "
                     "the generous form that the novel respects but "
                     "systematically refutes"),
    resolution_direction=ResolutionDirection.AFFIRM,
    domain="moral-epistemic",
)

ARGUMENTS = (A_prejudice_dissolves,)


# ============================================================================
# Throughlines
# ============================================================================

T_overall_bennets = Throughline(
    id="T_overall_bennets",
    role_label="overall-story",
    owners=(THROUGHLINE_OWNER_SITUATION,),
    subject=("a family of five unmarried daughters in a precarious "
             "entailed situation; the matrimonial pressure of Regency "
             "England bearing on them; the arrival of Bingley and "
             "Darcy at Netherfield setting the plot in motion; the "
             "successive resolutions of Jane-Bingley, Elizabeth-Darcy, "
             "and — catastrophically then redemptively — Lydia-Wickham"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_prejudice_dissolves",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_family_future",
)

T_mc_elizabeth = Throughline(
    id="T_mc_elizabeth",
    role_label="main-character",
    owners=("C_elizabeth",),
    subject=("a second daughter whose wit and quickness make her her "
             "father's favorite and whose fixed attitude toward Darcy "
             "is formed in the first ballroom scene and sustained "
             "through Wickham's accusations, through Darcy's first "
             "proposal, until his letter forces a re-reading of every "
             "prior piece of evidence. Her arc is the slow dissolution "
             "of a prejudice she was proud of holding"),
    counterpoint_throughline_ids=("T_ic_darcy",),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_prejudice_dissolves",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_elizabeth_judgment",
)

T_ic_darcy = Throughline(
    id="T_ic_darcy",
    role_label="impact-character",
    owners=("C_darcy",),
    subject=("a wealthy proud man whose initial rudeness ('tolerable, "
             "but not handsome enough to tempt me') forms Elizabeth's "
             "prejudice; who separates Bingley from Jane under the "
             "same prejudicial logic; whose letter after the failed "
             "first proposal is the evidence that forces Elizabeth's "
             "revision; who then manipulates events behind the scenes "
             "(the Wickham payoff, Bingley's return) to prove by "
             "action the change of attitude his letter promised"),
    counterpoint_throughline_ids=("T_mc_elizabeth",),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_prejudice_dissolves",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_darcy_honor",
)

T_rel_elizabeth_darcy = Throughline(
    id="T_rel_elizabeth_darcy",
    role_label="relationship",
    owners=(THROUGHLINE_OWNER_RELATIONSHIP,),
    subject=("a courtship that begins as mutual dismissal, passes "
             "through antagonism, reaches its lowest point at the "
             "Hunsford proposal, re-orients at Pemberley, and resolves "
             "in the second proposal walk. The relationship's activity "
             "— dances, dinners, walks, letters — IS its argument "
             "against the prejudice that would have kept both parties "
             "apart"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_prejudice_dissolves",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_union",
)

THROUGHLINES = (
    T_overall_bennets, T_mc_elizabeth, T_ic_darcy,
    T_rel_elizabeth_darcy,
)


# ============================================================================
# Characters
# ============================================================================
#
# dramatica-8 slot assignment for this encoding:
#
#   Protagonist   → C_elizabeth      (pursues understanding of Darcy;
#                                     drives toward truth)
#   Antagonist    → C_lady_catherine (opposes the match; her demand
#                                     that Elizabeth refuse Darcy is
#                                     the Antagonist's clearest act)
#   Reason        → C_jane           (her gentle optimism reads the
#                                     best in everyone; the Reason
#                                     position's generous form)
#   Emotion       → C_lydia          (impulsive, uncontrolled; her
#                                     elopement is emotion carrying
#                                     her past sense)
#   Sidekick      → C_bingley        (loyal, supportive; his faith in
#                                     Darcy's judgment about Jane is
#                                     the Sidekick form — loyal even
#                                     when wrong)
#   Skeptic       → C_mr_bennet      (doubts every pretension; his
#                                     sardonic distance is the
#                                     Skeptic's comedic form)
#   Guardian      → C_darcy          (guards those under his care —
#                                     Georgiana, Bingley, eventually
#                                     the Bennet family via the
#                                     Wickham payoff; IC role is
#                                     Throughline ownership, not
#                                     a second function label)
#   Contagonist   → C_wickham        (tempts Elizabeth into wrong
#                                     inferences about Darcy; hinders
#                                     the truth by charming into
#                                     belief)
#
# Characters who appear but carry no dramatica-8 function: Mrs.
# Bennet, Charlotte Lucas, Mr. Collins, Mrs. Gardiner. They have
# narrative weight but no slot to fill or under-fill.

C_elizabeth = Character(
    id="C_elizabeth", name="Elizabeth Bennet",
    function_labels=("Protagonist",),
    # The Main Character role is carried by T_mc_elizabeth's owner
    # edge (owners=("C_elizabeth",)); Dramatica role_labels live on
    # Throughlines, not on Character function_labels.
)

C_darcy = Character(
    id="C_darcy", name="Fitzwilliam Darcy",
    function_labels=("Guardian",),
    # The Impact Character role is carried by T_ic_darcy's owner
    # edge (owners=("C_darcy",)); Darcy's function is Guardian
    # (warns/helps those under his care — Georgiana, Bingley, the
    # Bennet family via the Wickham payoff). IC + Guardian parallels
    # Ackroyd's Poirot as Protagonist + IC.
)

C_lady_catherine = Character(
    id="C_lady_catherine", name="Lady Catherine de Bourgh",
    function_labels=("Antagonist",),
)

C_jane = Character(
    id="C_jane", name="Jane Bennet",
    function_labels=("Reason",),
)

C_lydia = Character(
    id="C_lydia", name="Lydia Bennet",
    function_labels=("Emotion",),
)

C_bingley = Character(
    id="C_bingley", name="Charles Bingley",
    function_labels=("Sidekick",),
)

C_mr_bennet = Character(
    id="C_mr_bennet", name="Mr. Bennet",
    function_labels=("Skeptic",),
)

C_wickham = Character(
    id="C_wickham", name="George Wickham",
    function_labels=("Contagonist",),
)

# Narratively important but carrying no dramatica-8 function slot.

C_mrs_bennet = Character(
    id="C_mrs_bennet", name="Mrs. Bennet",
    function_labels=(),
)

C_charlotte = Character(
    id="C_charlotte", name="Charlotte Lucas",
    function_labels=(),
)

C_collins = Character(
    id="C_collins", name="Mr. Collins",
    function_labels=(),
)

C_mrs_gardiner = Character(
    id="C_mrs_gardiner", name="Mrs. Gardiner",
    function_labels=(),
)

CHARACTERS = (
    C_elizabeth, C_darcy, C_lady_catherine, C_jane, C_lydia,
    C_bingley, C_mr_bennet, C_wickham,
    C_mrs_bennet, C_charlotte, C_collins, C_mrs_gardiner,
)


# ============================================================================
# Beats — per Throughline, ordered by beat_position
# ============================================================================

BEATS = (
    # T_overall_bennets — the Bennet family's arc from precarious to
    # three-daughters-well-married
    Beat(id="B_op_1", throughline_id="T_overall_bennets",
         beat_position=1, beat_type="inciting",
         description_of_change=("Bingley takes Netherfield; a rich "
                                "single man has arrived in want of a "
                                "wife; Mrs. Bennet's matrimonial "
                                "engine engages")),
    Beat(id="B_op_2", throughline_id="T_overall_bennets",
         beat_position=2, beat_type="rising",
         description_of_change=("the Meryton ball establishes the "
                                "field — Bingley charms Jane, Darcy "
                                "insults Elizabeth, Wickham appears "
                                "later to skew the pitch")),
    Beat(id="B_op_3", throughline_id="T_overall_bennets",
         beat_position=3, beat_type="rising",
         description_of_change=("Collins arrives to claim an heiress; "
                                "Elizabeth refuses; Charlotte accepts "
                                "him — one Bennet's future secured, "
                                "but as survival, not match")),
    Beat(id="B_op_4", throughline_id="T_overall_bennets",
         beat_position=4, beat_type="midpoint",
         description_of_change=("Lydia elopes with Wickham; the "
                                "family's entire future collapses "
                                "into scandal; none of the daughters "
                                "will marry respectably if this isn't "
                                "fixed")),
    Beat(id="B_op_5", throughline_id="T_overall_bennets",
         beat_position=5, beat_type="denouement",
         description_of_change=("three daughters well-married: Jane "
                                "to Bingley, Elizabeth to Darcy, "
                                "Lydia to Wickham (unhappily but "
                                "respectably); Pemberley opens its "
                                "gardens to the Gardiners")),

    # T_mc_elizabeth — prejudice formed and dissolved, beat by beat
    Beat(id="B_mc_1", throughline_id="T_mc_elizabeth",
         beat_position=1, beat_type="inciting",
         description_of_change=("overhears Darcy's 'tolerable, but not "
                                "handsome enough'; the fixed attitude "
                                "begins to form in the first hour of "
                                "acquaintance")),
    Beat(id="B_mc_2", throughline_id="T_mc_elizabeth",
         beat_position=2, beat_type="rising",
         description_of_change=("Wickham's account of Darcy's cruelty "
                                "crystallizes her prejudice; she "
                                "accepts the story because it "
                                "confirms the attitude she already "
                                "holds")),
    Beat(id="B_mc_3", throughline_id="T_mc_elizabeth",
         beat_position=3, beat_type="rising",
         description_of_change=("refuses Darcy's first proposal at "
                                "Hunsford — the prejudice at its "
                                "most articulate, voiced at full "
                                "scale in response to his pride")),
    Beat(id="B_mc_4", throughline_id="T_mc_elizabeth",
         beat_position=4, beat_type="midpoint",
         description_of_change=("reads Darcy's letter; forced to "
                                "reconsider Wickham, Jane, her own "
                                "first-impression method; 'till this "
                                "moment I never knew myself'")),
    Beat(id="B_mc_5", throughline_id="T_mc_elizabeth",
         beat_position=5, beat_type="climax",
         description_of_change=("stands against Lady Catherine at "
                                "Longbourn — now clear in her own "
                                "mind about Darcy, and willing to "
                                "say so; the prejudice not only "
                                "gone but inverted into advocacy")),
    Beat(id="B_mc_6", throughline_id="T_mc_elizabeth",
         beat_position=6, beat_type="denouement",
         description_of_change=("accepts Darcy's second proposal; "
                                "the attitude's dissolution is "
                                "complete; married with full "
                                "understanding of what her first "
                                "impression cost her")),

    # T_ic_darcy — pride dissolved, attitude changed
    Beat(id="B_ic_1", throughline_id="T_ic_darcy",
         beat_position=1, beat_type="inciting",
         description_of_change=("initial dismissiveness at the "
                                "Meryton ball; his pride announced "
                                "in the voice of unguarded candor")),
    Beat(id="B_ic_2", throughline_id="T_ic_darcy",
         beat_position=2, beat_type="rising",
         description_of_change=("separates Bingley from Jane on "
                                "prejudicial grounds (mother, "
                                "sisters, connections); the same "
                                "fixed attitude Elizabeth holds, "
                                "wielded as an act")),
    Beat(id="B_ic_3", throughline_id="T_ic_darcy",
         beat_position=3, beat_type="midpoint",
         description_of_change=("first proposal at Hunsford — offers "
                                "his hand while insulting her "
                                "family; rejected; for the first "
                                "time his pride is named as such "
                                "and to his face")),
    Beat(id="B_ic_4", throughline_id="T_ic_darcy",
         beat_position=4, beat_type="rising",
         description_of_change=("writes the letter that night; "
                                "gives Elizabeth the evidence she "
                                "needs without demanding revision; "
                                "the first act of the new Darcy")),
    Beat(id="B_ic_5", throughline_id="T_ic_darcy",
         beat_position=5, beat_type="rising",
         description_of_change=("pays Wickham off; saves the Bennet "
                                "family honor; does it privately; "
                                "his letter's promise proved by "
                                "action rather than words")),
    Beat(id="B_ic_6", throughline_id="T_ic_darcy",
         beat_position=6, beat_type="denouement",
         description_of_change=("second proposal walk to Oakham "
                                "Mount; the changed man proposes "
                                "again to the changed woman; the "
                                "attitude's dissolution mirrors "
                                "Elizabeth's")),

    # T_rel_elizabeth_darcy — the relationship's shape through
    # successive meetings
    Beat(id="B_rel_1", throughline_id="T_rel_elizabeth_darcy",
         beat_position=1, beat_type="inciting",
         description_of_change=("first ball; mutual dismissal; each "
                                "takes a fixed attitude toward the "
                                "other")),
    Beat(id="B_rel_2", throughline_id="T_rel_elizabeth_darcy",
         beat_position=2, beat_type="rising",
         description_of_change=("Netherfield, Rosings, the slow "
                                "accumulation of encounters; "
                                "sparring on Darcy's side shading "
                                "into attraction; Elizabeth reads "
                                "none of it")),
    Beat(id="B_rel_3", throughline_id="T_rel_elizabeth_darcy",
         beat_position=3, beat_type="midpoint",
         description_of_change=("the Hunsford proposal and refusal; "
                                "the relationship at its lowest and "
                                "most honest — both say what they "
                                "actually think")),
    Beat(id="B_rel_4", throughline_id="T_rel_elizabeth_darcy",
         beat_position=4, beat_type="rising",
         description_of_change=("Pemberley — Elizabeth sees his "
                                "estate, his servants' regard, his "
                                "sister; meets him again and is met "
                                "with civility; the relationship "
                                "re-orients in half a dozen scenes")),
    Beat(id="B_rel_5", throughline_id="T_rel_elizabeth_darcy",
         beat_position=5, beat_type="denouement",
         description_of_change=("the second proposal; engagement; "
                                "the relationship's true shape, now "
                                "on foundations neither pride nor "
                                "prejudice")),
)


# ============================================================================
# Scenes
# ============================================================================

S_meryton_ball = Scene(
    id="S_meryton_ball", title="The Meryton Assembly",
    narrative_position=1,
    advances=(
        SceneAdvancement(throughline_id="T_overall_bennets",
                         beat_id="B_op_2"),
        SceneAdvancement(throughline_id="T_mc_elizabeth",
                         beat_id="B_mc_1"),
        SceneAdvancement(throughline_id="T_ic_darcy",
                         beat_id="B_ic_1"),
        SceneAdvancement(throughline_id="T_rel_elizabeth_darcy",
                         beat_id="B_rel_1"),
    ),
    conflict_shape=("a country assembly; the new gentlemen are "
                    "inspected; one charms, the other insults; "
                    "first impressions fix themselves on both "
                    "sides"),
    result=("Bingley and Jane paired in general expectation; Darcy "
            "and Elizabeth mutually dismissed; Elizabeth carries "
            "the insult home as a story"),
)

S_netherfield_visit = Scene(
    id="S_netherfield_visit", title="Elizabeth at Netherfield",
    narrative_position=2,
    advances=(
        SceneAdvancement(throughline_id="T_rel_elizabeth_darcy",
                         beat_id="B_rel_2"),
    ),
    conflict_shape=("Jane falls ill at Netherfield; Elizabeth walks "
                    "three muddy miles to nurse her; Darcy's "
                    "attention shifts without his or her noticing; "
                    "Caroline Bingley's jealousy registers the "
                    "shift for them"),
    result=("Darcy's attitude toward Elizabeth begins to move; "
            "Elizabeth's does not; the asymmetry is the engine of "
            "the rest of the novel"),
)

S_wickham_arrives = Scene(
    id="S_wickham_arrives", title="Wickham's account of Darcy",
    narrative_position=3,
    advances=(
        SceneAdvancement(throughline_id="T_mc_elizabeth",
                         beat_id="B_mc_2"),
    ),
    conflict_shape=("the charming lieutenant tells his version of a "
                    "history Elizabeth already believes; she accepts "
                    "it because it confirms what her prejudice "
                    "expects"),
    result=("Elizabeth's prejudice crystallized; Wickham's "
            "performance has found its perfect audience"),
)

S_collins_refused = Scene(
    id="S_collins_refused", title="Collins proposes; Charlotte accepts",
    narrative_position=4,
    advances=(
        SceneAdvancement(throughline_id="T_overall_bennets",
                         beat_id="B_op_3"),
    ),
    conflict_shape=("the heir presumptive offers Elizabeth his "
                    "hand; she refuses against her mother's "
                    "hysterics; Charlotte takes him instead, on "
                    "terms of survival not affection"),
    result=("one Bennet connection secured at the cost of "
            "Charlotte's comfort; Elizabeth's refusal sets up "
            "what it means to her to refuse a man she doesn't "
            "love"),
)

S_hunsford_proposal = Scene(
    id="S_hunsford_proposal", title="Darcy's first proposal",
    narrative_position=5,
    advances=(
        SceneAdvancement(throughline_id="T_mc_elizabeth",
                         beat_id="B_mc_3"),
        SceneAdvancement(throughline_id="T_ic_darcy",
                         beat_id="B_ic_3"),
        SceneAdvancement(throughline_id="T_rel_elizabeth_darcy",
                         beat_id="B_rel_3"),
    ),
    conflict_shape=("Darcy declares his love against his own "
                    "better judgment; lists the objections to her "
                    "family while proposing; Elizabeth refuses in "
                    "terms matched to his presumption"),
    result=("the relationship's lowest point and most honest; "
            "each now knows precisely what the other thinks of "
            "them"),
)

S_darcy_letter = Scene(
    id="S_darcy_letter", title="Darcy's letter",
    narrative_position=6,
    advances=(
        SceneAdvancement(throughline_id="T_mc_elizabeth",
                         beat_id="B_mc_4"),
        SceneAdvancement(throughline_id="T_ic_darcy",
                         beat_id="B_ic_4"),
    ),
    conflict_shape=("a letter arrives in the morning; contains the "
                    "history of Wickham's conduct toward Georgiana "
                    "and a plain account of the Bingley-Jane "
                    "intervention; does not ask for revision of "
                    "sentiment, only of fact"),
    result=("Elizabeth re-reads every scene of the past year; "
            "'till this moment I never knew myself'; the "
            "prejudice dissolves as evidence accumulates on the "
            "other side"),
)

S_pemberley = Scene(
    id="S_pemberley", title="Elizabeth at Pemberley",
    narrative_position=7,
    advances=(
        SceneAdvancement(throughline_id="T_rel_elizabeth_darcy",
                         beat_id="B_rel_4"),
    ),
    conflict_shape=("Elizabeth tours Pemberley with the Gardiners "
                    "expecting Darcy absent; the housekeeper's "
                    "account of him as master is a testimonial; "
                    "he appears unexpectedly and meets her with "
                    "civility rather than triumph"),
    result=("the relationship re-enters on terms Elizabeth did "
            "not expect; Darcy's change of attitude is proved by "
            "what he does in her presence, not what he argues"),
)

S_lydia_elopes = Scene(
    id="S_lydia_elopes", title="Lydia's elopement",
    narrative_position=8,
    advances=(
        SceneAdvancement(throughline_id="T_overall_bennets",
                         beat_id="B_op_4"),
    ),
    conflict_shape=("news reaches Pemberley that Lydia has run off "
                    "with Wickham; the Bennet family's respectability "
                    "is forfeit unless marriage is produced; "
                    "Elizabeth believes at this moment she has lost "
                    "Darcy forever"),
    result=("the family crisis at its peak; Elizabeth returns home; "
            "Darcy acts offstage without telling anyone"),
)

S_wickham_payoff = Scene(
    id="S_wickham_payoff", title="Darcy's hidden intervention",
    narrative_position=9,
    advances=(
        SceneAdvancement(throughline_id="T_ic_darcy",
                         beat_id="B_ic_5"),
    ),
    conflict_shape=("Darcy finds Wickham in London; pays his debts "
                    "and buys his commission and compels the "
                    "marriage; arranges to have it appear the "
                    "Gardiners' work so the Bennets won't know he "
                    "did it"),
    result=("the family is saved; Elizabeth learns by accident "
            "(through Mrs. Gardiner's letter) that Darcy did it; "
            "the evidence of his changed attitude is now overwhelming"),
)

S_lady_catherine_visit = Scene(
    id="S_lady_catherine_visit",
    title="Lady Catherine's demand at Longbourn",
    narrative_position=10,
    advances=(
        SceneAdvancement(throughline_id="T_mc_elizabeth",
                         beat_id="B_mc_5"),
    ),
    conflict_shape=("Lady Catherine arrives in a storm to demand "
                    "Elizabeth promise not to marry Darcy; "
                    "Elizabeth refuses to promise; the Antagonist "
                    "acts openly"),
    result=("Lady Catherine reports the exchange to Darcy, hoping "
            "for confirmation; instead it tells him Elizabeth has "
            "not refused him in principle; he returns"),
)

S_second_proposal = Scene(
    id="S_second_proposal", title="The second proposal",
    narrative_position=11,
    advances=(
        SceneAdvancement(throughline_id="T_mc_elizabeth",
                         beat_id="B_mc_6"),
        SceneAdvancement(throughline_id="T_ic_darcy",
                         beat_id="B_ic_6"),
        SceneAdvancement(throughline_id="T_rel_elizabeth_darcy",
                         beat_id="B_rel_5"),
    ),
    conflict_shape=("Darcy walks with Elizabeth; she thanks him for "
                    "Lydia; he asks whether her feelings have "
                    "altered; they have; he proposes again; she "
                    "accepts"),
    result=("the engagement; the two changed people meet each other "
            "as they now are; the attitude that began in the first "
            "scene is dissolved by the last"),
)

S_three_marriages = Scene(
    id="S_three_marriages",
    title="Three daughters married",
    narrative_position=12,
    advances=(
        SceneAdvancement(throughline_id="T_overall_bennets",
                         beat_id="B_op_5"),
    ),
    conflict_shape=("Jane and Bingley settle at Netherfield; "
                    "Elizabeth and Darcy at Pemberley; Lydia and "
                    "Wickham transferred to the north; the Bennet "
                    "family's matrimonial situation is resolved "
                    "(comically and asymmetrically)"),
    result=("the novel closes on settled futures; the entailed "
            "estate's threat no longer threatens the surviving "
            "unmarried sisters, since two are at Pemberley's "
            "disposal"),
)

SCENES = (
    S_meryton_ball, S_netherfield_visit, S_wickham_arrives,
    S_collins_refused, S_hunsford_proposal, S_darcy_letter,
    S_pemberley, S_lydia_elopes, S_wickham_payoff,
    S_lady_catherine_visit, S_second_proposal, S_three_marriages,
)


# ============================================================================
# Stakes
# ============================================================================

Stakes_family_future = Stakes(
    id="Stakes_family_future",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_overall_bennets"),
    at_risk=("the Bennet family's respectability, the unmarried "
             "sisters' prospects, the roof over Mrs. Bennet's head "
             "after Mr. Bennet dies and Collins inherits"),
    to_gain=("advantageous matches for the daughters; security "
             "against the entail; preservation of the family's "
             "place in county society"),
    external_manifestation=("the entailed estate hanging over every "
                            "scene; Collins's inheritance pressing "
                            "down; Lydia's scandal briefly wiping "
                            "the prospects away; the three settled "
                            "marriages at the novel's close"),
)

Stakes_elizabeth_judgment = Stakes(
    id="Stakes_elizabeth_judgment",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_mc_elizabeth"),
    at_risk=("Elizabeth's capacity for accurate judgment — the "
             "faculty she prides herself on; her self-image as a "
             "fair reader of character; her future happiness, "
             "which depends on her reading Darcy right"),
    to_gain=("an honest account of herself; the self-knowledge "
             "that 'till this moment I never knew myself'; "
             "ultimately the marriage that proves she has revised "
             "well"),
    external_manifestation=("the refusal of Darcy's first proposal; "
                            "the letter-reading; her advocacy before "
                            "Lady Catherine; her acceptance of the "
                            "second proposal — each external act "
                            "marking an internal revision"),
)

Stakes_darcy_honor = Stakes(
    id="Stakes_darcy_honor",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_ic_darcy"),
    at_risk=("Darcy's capacity to deserve the woman he has proposed "
             "to; his standing in his own eyes after Elizabeth names "
             "his pride; the people he is responsible for "
             "(Georgiana, Bingley, Pemberley)"),
    to_gain=("the honor of having changed under correction; "
             "Elizabeth's regard on terms he can accept; a marriage "
             "that repairs rather than repeats the first proposal's "
             "error"),
    external_manifestation=("the letter written the night after "
                            "rejection; the hidden Wickham payoff; "
                            "the civility at Pemberley; the second "
                            "proposal on Elizabeth's terms"),
)

Stakes_union = Stakes(
    id="Stakes_union",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_rel_elizabeth_darcy"),
    at_risk=("whether the two can ever be in the same room as "
             "themselves rather than as the caricatures their first "
             "impressions made of each other; whether the "
             "relationship can exist at all"),
    to_gain=("a marriage founded on what each now is, after both "
             "have been corrected by the other; the rare Austen "
             "union where neither party is deceived"),
    external_manifestation=("the successive encounters across six "
                            "months: ball, Netherfield, Rosings, "
                            "Hunsford, Pemberley, Longbourn, second "
                            "proposal; each one a piece of the "
                            "relationship's accumulating shape"),
)

STAKES = (
    Stakes_family_future, Stakes_elizabeth_judgment,
    Stakes_darcy_honor, Stakes_union,
)


# ============================================================================
# Story root
# ============================================================================

STORY = Story(
    id="S_pride_and_prejudice",
    title="Pride and Prejudice",
    character_function_template_id="dramatica-8",
    argument_ids=tuple(a.id for a in ARGUMENTS),
    throughline_ids=tuple(t.id for t in THROUGHLINES),
    character_ids=tuple(c.id for c in CHARACTERS),
    scene_ids=tuple(s.id for s in SCENES),
    beat_ids=tuple(b.id for b in BEATS),
    stakes_ids=tuple(s.id for s in STAKES),
)
