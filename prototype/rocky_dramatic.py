"""
rocky_dramatic.py — *Rocky* (1976) encoded in the Dramatic dialect.

Fifth encoding at the Dramatic dialect level (after Oedipus, Macbeth,
Ackroyd, Pride and Prejudice). Records the film's argumentative
structure: one Argument, four Throughlines under the dramatica-8
Template, eight function-carrying Characters, ten Scenes, four
Stakes records, twenty Beats.

Pure dialect content. No substrate references; no Lowering records.
This encoding is the corpus's first Failure-outcome story and its
first Personal Triumph (Outcome=Failure, Judgment=Good):

- **Rocky loses the fight** (split decision to Apollo) — the OS
  goal (Apollo defends his title cleanly in a bicentennial
  publicity stunt) is **not** achieved in the expected way; the
  stunt becomes real and Apollo is shaken.
- **Rocky wins Adrian, his self-respect, and the crowd** — the
  MC's internal resolution is Good despite the external Failure.
- The film's thesis — worth is measured by whether one can go
  the distance, not by whether one wins — is exactly the
  argument that personal-triumph endings make.

Notable features:

- **First Steadfast Do-er MC.** Ackroyd was Steadfast + Be-er.
  Oedipus and Macbeth were Change + Do-er. Rocky is the
  orthogonal combination: Steadfast + Do-er. He never changes
  (he's always the same palooka) but he acts relentlessly.

- **First Timelock Limit.** All four prior encodings are
  Optionlock (options narrow until only one remains). Rocky's
  limit is a calendar date — the fight is set, the clock counts
  down to bell time. The DSP axis's other choice is finally
  exercised.

- **First Failure outcome.** All prior encodings have
  Outcome=Success (even the tragedies — the OS goal resolves,
  the MC is the casualty). Rocky's OS goal (Apollo's clean
  publicity-stunt win) fails; the failure is WHY the MC wins.

- **Small cast, all eight slots filled distinctly.** No
  double-function characters. Parallels Ackroyd and Pride and
  Prejudice in cleanness; contrasts with Macbeth and Oedipus's
  complex-character divergences.

Expected verifier output (the encoding's contract):

- 0 slot_unfilled / slot_overfilled (all 8 dramatica-8 slots
  filled by distinct characters).
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

A_distance_is_worth = Argument(
    id="A_distance_is_worth",
    premise=("a man's worth is measured by whether he can go the "
             "distance, not whether he wins; to remain standing "
             "through what was meant to break him is its own form "
             "of victory"),
    counter_premise=("victory is the only measure; everything else "
                     "is losing gracefully. Apollo speaks the "
                     "counter-premise as entertainment business "
                     "(the marketing matters; a stunt is a stunt); "
                     "the sports establishment speaks it as "
                     "competitive logic (one champion, one title). "
                     "The fifteen rounds refute both"),
    resolution_direction=ResolutionDirection.AFFIRM,
    domain="moral-athletic",
)

ARGUMENTS = (A_distance_is_worth,)


# ============================================================================
# Throughlines
# ============================================================================

T_overall_fight = Throughline(
    id="T_overall_fight",
    role_label="overall-story",
    owners=(THROUGHLINE_OWNER_SITUATION,),
    subject=("a bicentennial heavyweight title defense planned as a "
             "marketing stunt — the scheduled contender injures his "
             "hand; the champion picks a local unknown for publicity; "
             "a million-dollar gate assembles around a fight no one "
             "expects to be real. The fight itself is what the stunt "
             "becomes when the unknown refuses to fall down"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_distance_is_worth",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_title_stakes",
)

T_mc_rocky = Throughline(
    id="T_mc_rocky",
    role_label="main-character",
    owners=("C_rocky",),
    subject=("a thirty-year-old club fighter working for a loan "
             "shark in South Philly; carries turtles in a pet store; "
             "lives in a cold-water room with his dog Butkus; has "
             "never been more than a preliminary fighter. The phone "
             "call from Jergens's office is the first time his life "
             "has been asked to be something other than what it "
             "already is"),
    counterpoint_throughline_ids=("T_ic_apollo",),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_distance_is_worth",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_rocky_self",
)

T_ic_apollo = Throughline(
    id="T_ic_apollo",
    role_label="impact-character",
    owners=("C_apollo",),
    subject=("the heavyweight champion of the world, entrepreneur, "
             "showman; wears George Washington into the ring; treats "
             "the fight as a marketing inflection; whose dismissive "
             "attitude forms Rocky's opportunity and whose late-round "
             "realization (he cannot put this club fighter down) "
             "impacts the MC by confirming what the MC was already "
             "going to prove"),
    counterpoint_throughline_ids=("T_mc_rocky",),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_distance_is_worth",
            side=ArgumentSide.COMPLICATES,
        ),
    ),
    stakes_id="Stakes_apollo_reign",
)

T_rel_rocky_adrian = Throughline(
    id="T_rel_rocky_adrian",
    role_label="relationship",
    owners=(THROUGHLINE_OWNER_RELATIONSHIP,),
    subject=("a courtship between two people who have been alone too "
             "long to have practice at not being alone — a shy "
             "pet-store clerk and a club fighter nobody looks at. The "
             "relationship emerges against Paulie's resentment and "
             "inside the pressure of Rocky's training; it is the thing "
             "Rocky is fighting for by the time the bell rings"),
    argument_contributions=(
        ArgumentContribution(
            argument_id="A_distance_is_worth",
            side=ArgumentSide.AFFIRMS,
        ),
    ),
    stakes_id="Stakes_adrian_rocky",
)

THROUGHLINES = (
    T_overall_fight, T_mc_rocky, T_ic_apollo, T_rel_rocky_adrian,
)


# ============================================================================
# Characters
# ============================================================================
#
# dramatica-8 slot assignment for this encoding:
#
#   Protagonist   → C_rocky    (pursues the fight opportunity;
#                               considers going the distance)
#   Antagonist    → C_apollo   (avoids taking Rocky seriously;
#                               reconsiders mid-fight)
#   Reason        → C_duke     (Apollo's trainer — "ain't gonna be a
#                               joke"; the voice of boxing logic)
#   Emotion       → C_adrian   (her feeling draws Rocky's out of
#                               him; the film's emotional axis)
#   Sidekick      → C_gazzo    (loan shark Rocky works for; gives
#                               Rocky the $500, cuts him loose from
#                               debt-collection work; loyal in his
#                               own way)
#   Skeptic       → C_jergens  (the fight promoter; dismisses Rocky
#                               as the "Italian Stallion" publicity
#                               gimmick; never takes him seriously)
#   Guardian      → C_mickey   (the old trainer who throws Rocky out
#                               of his locker, then shows up at his
#                               apartment to manage him; protects
#                               and guides)
#   Contagonist   → C_paulie   (tempts Rocky toward bitterness and
#                               drink; hinders the Adrian
#                               relationship; a friend who is not
#                               Rocky's friend)
#
# Eight distinct characters, eight distinct function slots. No
# character carries two function_labels; the verifier's
# slot-coverage check should report all 8 slots filled exactly once.
# Rocky's MC role is Throughline ownership, not a function label —
# same convention as all prior encodings.

C_rocky = Character(
    id="C_rocky", name="Rocky Balboa",
    function_labels=("Protagonist",),
)

C_apollo = Character(
    id="C_apollo", name="Apollo Creed",
    function_labels=("Antagonist",),
)

C_mickey = Character(
    id="C_mickey", name="Mickey Goldmill",
    function_labels=("Guardian",),
)

C_paulie = Character(
    id="C_paulie", name="Paulie Pennino",
    function_labels=("Contagonist",),
)

C_adrian = Character(
    id="C_adrian", name="Adrian Pennino",
    function_labels=("Emotion",),
)

C_duke = Character(
    id="C_duke", name="Tony \"Duke\" Evers",
    function_labels=("Reason",),
)

C_gazzo = Character(
    id="C_gazzo", name="Tony Gazzo",
    function_labels=("Sidekick",),
)

C_jergens = Character(
    id="C_jergens", name="Miles Jergens",
    function_labels=("Skeptic",),
)

# Characters present but carrying no dramatica-8 function. Spider
# Rico is Rocky's opponent in the opening club fight; the bar
# owner is the one Gazzo asks Rocky to collect from; Bob is the
# dock worker Rocky refuses to hurt.

C_spider_rico = Character(
    id="C_spider_rico", name="Spider Rico",
    function_labels=(),
)

C_bob = Character(
    id="C_bob", name="Bob (the dock worker)",
    function_labels=(),
)

CHARACTERS = (
    C_rocky, C_apollo, C_mickey, C_paulie, C_adrian,
    C_duke, C_gazzo, C_jergens,
    C_spider_rico, C_bob,
)


# ============================================================================
# Beats — per Throughline, ordered by beat_position
# ============================================================================

BEATS = (
    # T_overall_fight — the bicentennial stunt becomes a real title
    # defense
    Beat(id="B_op_1", throughline_id="T_overall_fight",
         beat_position=1, beat_type="inciting",
         description_of_change=("Apollo's scheduled contender Mac "
                                "Lee Green injures his hand; the "
                                "title defense faces cancellation "
                                "three months before a million-"
                                "dollar bicentennial card")),
    Beat(id="B_op_2", throughline_id="T_overall_fight",
         beat_position=2, beat_type="rising",
         description_of_change=("Apollo proposes giving a local "
                                "unknown the shot as a marketing "
                                "stunt — 'give him a shot at the "
                                "title'; Jergens resists then agrees "
                                "for the storyline")),
    Beat(id="B_op_3", throughline_id="T_overall_fight",
         beat_position=3, beat_type="rising",
         description_of_change=("Rocky picked from the Philadelphia "
                                "rankings; contract signed on "
                                "camera; the fight is on the "
                                "calendar; training assembles on "
                                "both sides")),
    Beat(id="B_op_4", throughline_id="T_overall_fight",
         beat_position=4, beat_type="climax",
         description_of_change=("the fight goes fifteen rounds; "
                                "Apollo wins by split decision; the "
                                "stunt did not go as scripted — the "
                                "scripted winner had a harder night "
                                "than anticipated")),
    Beat(id="B_op_5", throughline_id="T_overall_fight",
         beat_position=5, beat_type="denouement",
         description_of_change=("'ain't gonna be no rematch' (Rocky) "
                                "/ 'don't want one' (Apollo); the "
                                "fight's sequel is refused by both "
                                "men, for opposite reasons")),

    # T_mc_rocky — club fighter to a man who went the distance
    Beat(id="B_mc_1", throughline_id="T_mc_rocky",
         beat_position=1, beat_type="inciting",
         description_of_change=("opening club fight against Spider "
                                "Rico; headbutt; scrappy win; "
                                "nineteen-seventy-six Rocky Balboa, "
                                "a club fighter nobody watches")),
    Beat(id="B_mc_2", throughline_id="T_mc_rocky",
         beat_position=2, beat_type="rising",
         description_of_change=("Mickey throws him out of the locker "
                                "assigned to him; his own trainer "
                                "has given up on him; 'you had the "
                                "talent'")),
    Beat(id="B_mc_3", throughline_id="T_mc_rocky",
         beat_position=3, beat_type="rising",
         description_of_change=("Jergens's office: the offer; 'me, "
                                "fight you?'; incredulity shading "
                                "into agreement before Rocky quite "
                                "knows why")),
    Beat(id="B_mc_4", throughline_id="T_mc_rocky",
         beat_position=4, beat_type="rising",
         description_of_change=("Mickey at the apartment offering to "
                                "manage; the scene turns from "
                                "rejection (the gym) to late arrival "
                                "(the home); Rocky accepts")),
    Beat(id="B_mc_5", throughline_id="T_mc_rocky",
         beat_position=5, beat_type="rising",
         description_of_change=("the training: the meat locker; the "
                                "pre-dawn runs; the stairs to the "
                                "Philadelphia Museum of Art; the "
                                "physical transformation")),
    Beat(id="B_mc_6", throughline_id="T_mc_rocky",
         beat_position=6, beat_type="midpoint",
         description_of_change=("night before the fight, alone in "
                                "the ring; 'I just want to go the "
                                "distance'; the goal articulated "
                                "smaller than winning")),
    Beat(id="B_mc_7", throughline_id="T_mc_rocky",
         beat_position=7, beat_type="climax",
         description_of_change=("round one knockdown; Rocky gets "
                                "up; fifteen rounds of not going "
                                "down; the articulated goal achieved "
                                "in real time")),
    Beat(id="B_mc_8", throughline_id="T_mc_rocky",
         beat_position=8, beat_type="denouement",
         description_of_change=("bell rings after fifteen; Rocky "
                                "calls for Adrian through the "
                                "crowd; the decision almost does "
                                "not matter")),

    # T_ic_apollo — champion shaken by what he scheduled
    Beat(id="B_ic_1", throughline_id="T_ic_apollo",
         beat_position=1, beat_type="inciting",
         description_of_change=("Apollo is interrupted in his "
                                "promotional element; the Mac Lee "
                                "Green cancellation is a scheduling "
                                "problem to be solved creatively")),
    Beat(id="B_ic_2", throughline_id="T_ic_apollo",
         beat_position=2, beat_type="rising",
         description_of_change=("proposes Rocky's name from the "
                                "rankings page; the decision is "
                                "entertainment business, not "
                                "competitive concern")),
    Beat(id="B_ic_3", throughline_id="T_ic_apollo",
         beat_position=3, beat_type="rising",
         description_of_change=("Duke warns 'ain't gonna be a joke'; "
                                "Apollo dismisses — the dismissal IS "
                                "the IC's fixed attitude at work")),
    Beat(id="B_ic_4", throughline_id="T_ic_apollo",
         beat_position=4, beat_type="midpoint",
         description_of_change=("enters the ring as George "
                                "Washington; dismissive showmanship "
                                "announced in costume; first round "
                                "goes as planned — the knockdown")),
    Beat(id="B_ic_5", throughline_id="T_ic_apollo",
         beat_position=5, beat_type="rising",
         description_of_change=("Rocky gets up; by round five "
                                "Apollo is fighting seriously; the "
                                "ribs go in the middle rounds; the "
                                "dismissive attitude collapses "
                                "under evidence")),
    Beat(id="B_ic_6", throughline_id="T_ic_apollo",
         beat_position=6, beat_type="denouement",
         description_of_change=("split decision; Apollo takes the "
                                "win; tells Rocky 'ain't gonna be no "
                                "rematch'; the IC has been changed "
                                "by the encounter, whether he "
                                "admits it or not")),

    # T_rel_rocky_adrian — the relationship emerges and becomes
    # what Rocky is fighting for
    Beat(id="B_rel_1", throughline_id="T_rel_rocky_adrian",
         beat_position=1, beat_type="inciting",
         description_of_change=("Rocky flirts with Adrian in the "
                                "pet store; the jokes, the "
                                "persistence; Adrian does not "
                                "respond visibly — the relationship "
                                "as not-yet")),
    Beat(id="B_rel_2", throughline_id="T_rel_rocky_adrian",
         beat_position=2, beat_type="rising",
         description_of_change=("Thanksgiving — Paulie throws the "
                                "turkey out into the alley; throws "
                                "Adrian at Rocky; the forced "
                                "introduction into the apartment")),
    Beat(id="B_rel_3", throughline_id="T_rel_rocky_adrian",
         beat_position=3, beat_type="rising",
         description_of_change=("ice skating — Rocky rents the rink "
                                "ten minutes; walks next to Adrian "
                                "while she skates; the conversation "
                                "that opens her")),
    Beat(id="B_rel_4", throughline_id="T_rel_rocky_adrian",
         beat_position=4, beat_type="midpoint",
         description_of_change=("his apartment; the first kiss; "
                                "'I don't like to lose'; the "
                                "relationship committed to against "
                                "her expectation")),
    Beat(id="B_rel_5", throughline_id="T_rel_rocky_adrian",
         beat_position=5, beat_type="rising",
         description_of_change=("training period — Adrian is always "
                                "there; the quiet presence in the "
                                "meat locker; the woman he is "
                                "fighting for becomes visible to "
                                "both of them")),
    Beat(id="B_rel_6", throughline_id="T_rel_rocky_adrian",
         beat_position=6, beat_type="denouement",
         description_of_change=("'Adrian!' — through the crowd, "
                                "after fifteen rounds; she reaches "
                                "him; the relationship is the film's "
                                "final image")),
)


# ============================================================================
# Scenes
# ============================================================================

S_club_fight = Scene(
    id="S_club_fight", title="Opening: Rocky vs. Spider Rico",
    narrative_position=1,
    advances=(
        SceneAdvancement(throughline_id="T_mc_rocky",
                         beat_id="B_mc_1"),
    ),
    conflict_shape=("a Philadelphia club fight; the Resurrection "
                    "A.C.; forty dollars a round; an illegal "
                    "headbutt; a scrappy win that nobody will "
                    "remember tomorrow"),
    result=("Rocky is established as he has been for years — a "
            "club fighter, a body for hire, a man whose best is "
            "not very much"),
)

S_mickey_locker = Scene(
    id="S_mickey_locker", title="Mickey takes Rocky's locker",
    narrative_position=2,
    advances=(
        SceneAdvancement(throughline_id="T_mc_rocky",
                         beat_id="B_mc_2"),
    ),
    conflict_shape=("Rocky's locker has been assigned to a younger "
                    "fighter; Mickey will not pretend Rocky is "
                    "going somewhere; 'you had the talent to become "
                    "a good fighter'"),
    result=("the establishment of boxing has told Rocky he is done; "
            "Rocky is alone with his dog and his turtles and his "
            "not-yet with Adrian"),
)

S_apollo_announces = Scene(
    id="S_apollo_announces", title="Apollo picks the unknown",
    narrative_position=3,
    advances=(
        SceneAdvancement(throughline_id="T_overall_fight",
                         beat_id="B_op_1"),
        SceneAdvancement(throughline_id="T_overall_fight",
                         beat_id="B_op_2"),
        SceneAdvancement(throughline_id="T_ic_apollo",
                         beat_id="B_ic_1"),
        SceneAdvancement(throughline_id="T_ic_apollo",
                         beat_id="B_ic_2"),
    ),
    conflict_shape=("Apollo's promotional camp faces Mac Lee Green's "
                    "injury three months out; Apollo proposes a "
                    "novelty opponent; Jergens objects then "
                    "converts; Apollo picks a name from the "
                    "Philadelphia rankings"),
    result=("a bicentennial marketing stunt is on the calendar; "
            "the scripted outcome is a one-sided display; Rocky "
            "does not yet know"),
)

S_jergens_office = Scene(
    id="S_jergens_office", title="Rocky in Jergens's office",
    narrative_position=4,
    advances=(
        SceneAdvancement(throughline_id="T_overall_fight",
                         beat_id="B_op_3"),
        SceneAdvancement(throughline_id="T_mc_rocky",
                         beat_id="B_mc_3"),
    ),
    conflict_shape=("Rocky is told the offer; 'me, fight you?'; "
                    "the explanation that this is about the "
                    "storyline, the Italian Stallion marketing, "
                    "the chance for an unknown"),
    result=("Rocky agrees before he quite understands what "
            "agreeing means; the phone call home; the opportunity "
            "against any conceivable preparation"),
)

S_thanksgiving = Scene(
    id="S_thanksgiving", title="Thanksgiving at Paulie's",
    narrative_position=5,
    advances=(
        SceneAdvancement(throughline_id="T_rel_rocky_adrian",
                         beat_id="B_rel_2"),
    ),
    conflict_shape=("Paulie is drunk; throws the cooked turkey into "
                    "the alley; demands Adrian go out with Rocky; "
                    "forces an introduction neither has prepared "
                    "for"),
    result=("Adrian at the edge of leaving the apartment with "
            "Rocky; ashamed; embarrassed; not quite refused; the "
            "relationship begins under pressure, not invitation"),
)

S_ice_skating = Scene(
    id="S_ice_skating",
    title="Ice skating (ten minutes, closed rink)",
    narrative_position=6,
    advances=(
        SceneAdvancement(throughline_id="T_rel_rocky_adrian",
                         beat_id="B_rel_3"),
    ),
    conflict_shape=("Rocky walks the ice rink's edge while Adrian "
                    "skates; the slow opening of conversation; the "
                    "story about her brother, her mother, her "
                    "failures; the jokes that let her be heard"),
    result=("Adrian is visible to Rocky; visible to herself; the "
            "shell is no longer the whole of her; she walks him "
            "back home without retreating"),
)

S_first_kiss = Scene(
    id="S_first_kiss", title="First kiss at Rocky's apartment",
    narrative_position=7,
    advances=(
        SceneAdvancement(throughline_id="T_rel_rocky_adrian",
                         beat_id="B_rel_4"),
    ),
    conflict_shape=("Adrian at Rocky's apartment; her coat not "
                    "coming off; the wall; Rocky moves to her; "
                    "'I don't like to lose, so I don't always "
                    "win' — the kiss on her terms"),
    result=("the relationship has a before and an after; Adrian "
            "has chosen; she will be present for what is coming"),
)

S_mickey_apartment = Scene(
    id="S_mickey_apartment",
    title="Mickey asks to manage Rocky",
    narrative_position=8,
    advances=(
        SceneAdvancement(throughline_id="T_mc_rocky",
                         beat_id="B_mc_4"),
    ),
    conflict_shape=("Mickey at the apartment door; the same Mickey "
                    "who threw him out of the locker; his pitch — "
                    "he has spent fifty years on palookas and he "
                    "wants one last fight with someone who might "
                    "be more than that"),
    result=("Rocky rages and then agrees; Mickey is in the corner "
            "for the fight; the trainer and the fighter both get "
            "a last chance they had stopped expecting"),
)

S_training_montage = Scene(
    id="S_training_montage",
    title="Training: meat, stairs, dawn runs",
    narrative_position=9,
    advances=(
        SceneAdvancement(throughline_id="T_mc_rocky",
                         beat_id="B_mc_5"),
        SceneAdvancement(throughline_id="T_rel_rocky_adrian",
                         beat_id="B_rel_5"),
        SceneAdvancement(throughline_id="T_ic_apollo",
                         beat_id="B_ic_3"),
    ),
    conflict_shape=("months compressed into minutes: Rocky hitting "
                    "sides of beef in Paulie's plant; running up the "
                    "Art Museum steps; Mickey watching; Adrian "
                    "present through all of it; Apollo's camp "
                    "casual, Duke warning"),
    result=("Rocky transformed physically; Adrian transformed "
            "emotionally; Apollo's lack of transformation sets up "
            "the fight's surprise"),
)

S_night_before = Scene(
    id="S_night_before", title="Rocky alone in the ring",
    narrative_position=10,
    advances=(
        SceneAdvancement(throughline_id="T_mc_rocky",
                         beat_id="B_mc_6"),
    ),
    conflict_shape=("Rocky visits the empty Spectrum the night "
                    "before; sees his face on the poster with the "
                    "shorts colored wrong; walks back to the "
                    "apartment; the quiet articulation to Adrian: "
                    "'I just want to go the distance'"),
    result=("the goal is set smaller than the crowd will measure "
            "it; the private goal is the one he will keep; "
            "Adrian holds it with him"),
)

S_fight = Scene(
    id="S_fight", title="Rocky vs. Apollo (fifteen rounds)",
    narrative_position=11,
    advances=(
        SceneAdvancement(throughline_id="T_overall_fight",
                         beat_id="B_op_4"),
        SceneAdvancement(throughline_id="T_mc_rocky",
                         beat_id="B_mc_7"),
        SceneAdvancement(throughline_id="T_ic_apollo",
                         beat_id="B_ic_4"),
        SceneAdvancement(throughline_id="T_ic_apollo",
                         beat_id="B_ic_5"),
    ),
    conflict_shape=("Apollo as George Washington; Rocky in the "
                    "American-flag trunks; round one knockdown; "
                    "Rocky gets up; the middle rounds Apollo "
                    "fighting for real; the ribs; the cut eye; "
                    "fifteen rounds neither man is meant to finish"),
    result=("Apollo wins by split decision; Rocky does not go "
            "down; the scripted outcome is contaminated by what "
            "actually happened in the ring"),
)

S_after = Scene(
    id="S_after", title="'Adrian!'",
    narrative_position=12,
    advances=(
        SceneAdvancement(throughline_id="T_overall_fight",
                         beat_id="B_op_5"),
        SceneAdvancement(throughline_id="T_mc_rocky",
                         beat_id="B_mc_8"),
        SceneAdvancement(throughline_id="T_ic_apollo",
                         beat_id="B_ic_6"),
        SceneAdvancement(throughline_id="T_rel_rocky_adrian",
                         beat_id="B_rel_6"),
    ),
    conflict_shape=("the bell has rung; the decision is announced; "
                    "Apollo takes the microphone to refuse a "
                    "rematch; Rocky is looking for Adrian through "
                    "the crowd and cannot see her until she "
                    "reaches him"),
    result=("the fight is lost; the MC's goal is kept; the "
            "relationship is the final image; the Argument is "
            "affirmed by how the scene closes, not by the "
            "scorecards"),
)

SCENES = (
    S_club_fight, S_mickey_locker, S_apollo_announces,
    S_jergens_office, S_thanksgiving, S_ice_skating,
    S_first_kiss, S_mickey_apartment, S_training_montage,
    S_night_before, S_fight, S_after,
)


# ============================================================================
# Stakes
# ============================================================================

Stakes_title_stakes = Stakes(
    id="Stakes_title_stakes",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_overall_fight"),
    at_risk=("the marketing integrity of the bicentennial card; "
             "Apollo's heavyweight title; the gate's financial "
             "return; the storyline the promoters have scripted"),
    to_gain=("the promoters' narrative confirmed (a one-sided "
             "publicity bout); Apollo's record extended cleanly; "
             "a good night of television"),
    external_manifestation=("the fight's publicity run; the press "
                            "conference posturing; the costume "
                            "choice; the scorecards that split; "
                            "Apollo's post-fight refusal of a "
                            "rematch"),
)

Stakes_rocky_self = Stakes(
    id="Stakes_rocky_self",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_mc_rocky"),
    at_risk=("whether Rocky has been a bum or has been something "
             "else all along; whether fifteen rounds under the "
             "champion's best is the proof of a life, or just "
             "another club fight at a larger scale"),
    to_gain=("the self-knowledge of going the distance; the "
             "private evidence that the not-yet-amounted-to-"
             "anything was still not nothing; a place in his own "
             "life"),
    external_manifestation=("the physical transformation under "
                            "Mickey's training; the round one "
                            "knockdown and the stand-up; the cut "
                            "eye and the ribs and the staying "
                            "upright; the final 'Adrian!'"),
)

Stakes_apollo_reign = Stakes(
    id="Stakes_apollo_reign",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_ic_apollo"),
    at_risk=("Apollo's self-construction as the champion who runs "
             "the fight rather than being run by it; the "
             "promoter-athlete synthesis Apollo has made a career "
             "of; the distance between him and the men he fights"),
    to_gain=("a clean bicentennial win; the storyline "
             "self-authored; the championship extended without "
             "incident; the self-construction confirmed"),
    external_manifestation=("the George Washington costume; the "
                            "dismissive press conference; Duke's "
                            "warnings ignored; the mid-fight "
                            "realization; the 'no rematch' "
                            "declaration that concedes more than "
                            "it refuses"),
)

Stakes_adrian_rocky = Stakes(
    id="Stakes_adrian_rocky",
    owner=StakesOwner(kind=StakesOwnerKind.THROUGHLINE,
                      id="T_rel_rocky_adrian"),
    at_risk=("whether Adrian ever steps out of the shell her "
             "brother and her pet-store refuge have together "
             "built around her; whether Rocky ever has anyone "
             "who is his, for whom the fifteen rounds are kept"),
    to_gain=("a relationship that both have stopped expecting; "
             "a woman for Rocky to call through the crowd; a "
             "man for Adrian to be visible to"),
    external_manifestation=("the pet-store flirting; the "
                            "Thanksgiving forced introduction; "
                            "the ice rink; the first kiss; the "
                            "training-period presence; the "
                            "'Adrian!' through the post-fight "
                            "crowd"),
)

STAKES = (
    Stakes_title_stakes, Stakes_rocky_self,
    Stakes_apollo_reign, Stakes_adrian_rocky,
)


# ============================================================================
# Story root
# ============================================================================

STORY = Story(
    id="S_rocky",
    title="Rocky",
    character_function_template_id="dramatica-8",
    argument_ids=tuple(a.id for a in ARGUMENTS),
    throughline_ids=tuple(t.id for t in THROUGHLINES),
    character_ids=tuple(c.id for c in CHARACTERS),
    scene_ids=tuple(s.id for s in SCENES),
    beat_ids=tuple(b.id for b in BEATS),
    stakes_ids=tuple(s.id for s in STAKES),
)
