"""
demo_rashomon.py — run the substrate against the encoded Rashomon grove
scene and print a branch-indexed report.

Where demo.py (Oedipus) demonstrates reader-vs-character irony on a
single canonical branch, this demo exercises the `:contested` branch
machinery and the description surface: four sibling branches, each
internally consistent, mutually incompatible, with the substrate
reporting per-branch answers for structural questions and the
description API carrying the interpretive content that the fold does
not touch.

Run:
    cd prototype && python3 demo_rashomon.py
"""

from __future__ import annotations

from substrate import (
    Slot, Confidence, Attention,
    scope, project_knowledge, project_reader, project_world,
    dramatic_ironies, sternberg_curiosity,
    descriptions_for, descriptions_on_branch, by_kind, open_questions,
    anchor_event,
)
from rashomon import (
    EVENTS_ALL, SJUZHET_BY_BRANCH, AGENT_IDS, ALL_BRANCHES,
    CONTESTED_BRANCHES, DESCRIPTIONS,
    B_TAJOMARU, B_WIFE, B_HUSBAND, B_WOODCUTTER,
    killed, killed_with, stole, fled, dead,
    had_intercourse_with, bound_to, at_location,
)


# ----------------------------------------------------------------------------
# Display helpers
# ----------------------------------------------------------------------------

AGENT_NAMES = {
    "tajomaru":   "Tajomaru",
    "wife":       "the Wife",
    "husband":    "the Husband",
    "woodcutter": "the Woodcutter",
    "reader":     "Reader",
}

BRANCH_NAMES = {
    ":b-tajomaru":   "Tajomaru's account",
    ":b-wife":       "the Wife's account",
    ":b-husband":    "the Husband's account (via medium)",
    ":b-woodcutter": "the Woodcutter's confession",
    ":canonical":    "canonical (undisputed)",
}


def name(agent_id: str) -> str:
    return AGENT_NAMES.get(agent_id, agent_id)


def format_prop(p) -> str:
    args = [AGENT_NAMES.get(a, str(a)) if isinstance(a, str) else str(a)
            for a in p.args]
    return f"{p.predicate}({', '.join(args)})" if args else p.predicate


def slot_label(slot: Slot) -> str:
    return {Slot.KNOWN: "known", Slot.BELIEVED: "believed",
            Slot.SUSPECTED: "suspected", Slot.GAP: "gap"}[slot]


SEP = "─" * 76


# ----------------------------------------------------------------------------
# Propositions whose contested status is the whole point. With the
# interpretive predicates retired (duel_character, coerced,
# yielded_willingly, begged_to_kill), the contested structural surface
# is smaller — who killed, with what weapon, did someone flee or steal.
# The interpretive material is reported separately as descriptions.
# ----------------------------------------------------------------------------

CENTRAL_PROPS = [
    killed("tajomaru", "husband"),
    killed("wife",     "husband"),
    killed("husband",  "husband"),
    killed_with("tajomaru", "husband", "sword"),
    killed_with("wife",     "husband", "dagger"),
    killed_with("husband",  "husband", "dagger"),
    fled("tajomaru"),
    fled("wife"),
    stole("woodcutter", "dagger"),
]


def print_header(title: str) -> None:
    print()
    print(SEP)
    print(title)
    print(SEP)


# ----------------------------------------------------------------------------
# Section 1 — per-branch world state on the contested propositions
# ----------------------------------------------------------------------------

def world_state_matrix(τ_s: int) -> None:
    print_header(f"Per-branch world state at τ_s={τ_s}")
    print()
    header = f"  {'proposition':<48}" + "".join(
        f"{b.label:<16}" for b in CONTESTED_BRANCHES
    )
    print(header)
    print("  " + "─" * (48 + 16 * len(CONTESTED_BRANCHES)))
    world_by_branch = {}
    for b in CONTESTED_BRANCHES:
        scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
        world_by_branch[b.label] = project_world(scoped, τ_s)
    for p in CENTRAL_PROPS:
        cells = []
        for b in CONTESTED_BRANCHES:
            asserted = p in world_by_branch[b.label]
            cells.append("TRUE" if asserted else ".")
        row = f"  {format_prop(p):<48}" + "".join(f"{c:<16}" for c in cells)
        print(row)


# ----------------------------------------------------------------------------
# Section 2 — per-branch reader state at end of testimonies
# ----------------------------------------------------------------------------

def reader_state_matrix(up_to_τ_d: int) -> None:
    print_header(f"Per-branch reader state at τ_d={up_to_τ_d}")
    print()
    print("  The reader inhabits each branch's reality in turn. On each")
    print("  branch the reader holds that branch's disclosed structural")
    print("  facts as KNOWN; the facts of other branches are simply absent")
    print("  from this branch's reader state. The interpretive content")
    print("  (modality, character of the fight, speech-act content) is")
    print("  not in the reader state at all — it lives on the description")
    print("  surface below. Cross-branch uncertainty (meta-level) is a")
    print("  known soft spot — see rashomon.py's *Known soft spots* #2.")
    print()
    reader_by_branch = {}
    for b in CONTESTED_BRANCHES:
        reader_by_branch[b.label] = project_reader(
            sjuzhet=SJUZHET_BY_BRANCH[b.label],
            all_events=EVENTS_ALL,
            branch=b,
            all_branches=ALL_BRANCHES,
            up_to_τ_d=up_to_τ_d,
        )
    header = f"  {'proposition':<48}" + "".join(
        f"{b.label:<16}" for b in CONTESTED_BRANCHES
    )
    print(header)
    print("  " + "─" * (48 + 16 * len(CONTESTED_BRANCHES)))
    for p in CENTRAL_PROPS:
        cells = []
        for b in CONTESTED_BRANCHES:
            h = reader_by_branch[b.label].holds(p)
            cells.append(slot_label(h.slot) if h else ".")
        row = f"  {format_prop(p):<48}" + "".join(f"{c:<16}" for c in cells)
        print(row)


# ----------------------------------------------------------------------------
# Section 3 — per-branch descriptions on the intercourse event
# ----------------------------------------------------------------------------
#
# This is the surface the fold does not see. Each branch carries its
# own texture description; one reader-frame description on canonical
# is visible on every branch via canonical-is-universal.

def intercourse_descriptions() -> None:
    print_header("Per-branch descriptions on E_intercourse")
    print()
    print("  The intercourse event itself is a canonical fact (every")
    print("  branch agrees it happened). The *modality* — was it")
    print("  violation or yielding, coerced or consented — is not a")
    print("  proposition the fold dispatches on. It is a description")
    print("  attached to the event, branch-scoped where it differs.")
    print()
    anchor = anchor_event("E_intercourse")
    all_ = descriptions_for(anchor, DESCRIPTIONS)
    for b in CONTESTED_BRANCHES:
        visible = descriptions_on_branch(
            branch=b, descriptions=all_, events=EVENTS_ALL,
            all_branches=ALL_BRANCHES, up_to_τ_a=10_000,
        )
        print(f"  {BRANCH_NAMES[b.label]}  ({b.label})")
        for d in visible:
            scope_note = ""
            if d.branches is not None:
                if ":canonical" in d.branches and len(d.branches) == 1:
                    scope_note = "  [canonical — visible on every branch]"
                elif d.branches == frozenset({b.label}):
                    scope_note = f"  [branch-scoped to {b.label}]"
                else:
                    scope_note = f"  [branches={sorted(d.branches)}]"
            print(f"    · [{d.kind}/{d.attention.value}] "
                  f"{d.text}{scope_note}")
        print()


# ----------------------------------------------------------------------------
# Section 4 — per-branch dramatic-irony summary
# ----------------------------------------------------------------------------

def per_branch_irony_counts(up_to_τ_d: int, τ_s: int) -> None:
    print_header(f"Per-branch dramatic-irony counts at (τ_d={up_to_τ_d}, τ_s={τ_s})")
    print()
    print("  Reader > Character and Character > Character ironies, computed")
    print("  per branch over the branch's reader-state and character states.")
    print("  Counts are totals across ALL propositions the branch sees, not")
    print("  just the display-central ones above.")
    print()
    for b in CONTESTED_BRANCHES:
        reader_state = project_reader(
            sjuzhet=SJUZHET_BY_BRANCH[b.label],
            all_events=EVENTS_ALL,
            branch=b,
            all_branches=ALL_BRANCHES,
            up_to_τ_d=up_to_τ_d,
        )
        ironies = dramatic_ironies(
            agent_ids=AGENT_IDS,
            reader_state=reader_state,
            all_events=EVENTS_ALL,
            branch=b,
            all_branches=ALL_BRANCHES,
            τ_s=τ_s,
        )
        reader_over_char = sum(1 for i in ironies if i.informed_id == "reader")
        char_over_char   = sum(1 for i in ironies if i.informed_id != "reader")
        print(f"  {BRANCH_NAMES[b.label]}  ({b.label})")
        print(f"    Reader > Character:         {reader_over_char}")
        print(f"    Character > Character:      {char_over_char}")
        print()


# ----------------------------------------------------------------------------
# Section 5 — who killed the husband (per-branch verdict)
# ----------------------------------------------------------------------------

def agreement_on_killer() -> None:
    print_header("Who killed the husband? — per-branch verdict")
    print()
    print("  For every (killer, victim) pair the story names, which branches")
    print("  assert killed(killer, victim) at the end of the grove scene?")
    print()
    candidates = [
        ("tajomaru", "husband"),
        ("wife",     "husband"),
        ("husband",  "husband"),
    ]
    for killer_id, victim_id in candidates:
        prop = killed(killer_id, victim_id)
        branches_asserting = []
        for b in CONTESTED_BRANCHES:
            scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
            w = project_world(scoped, 100)
            if prop in w:
                branches_asserting.append(b.label)
        if branches_asserting:
            print(f"  {format_prop(prop)}")
            for lbl in branches_asserting:
                print(f"    · {BRANCH_NAMES[lbl]}  ({lbl})")
        else:
            print(f"  {format_prop(prop)}   (no branch asserts this)")
        print()


# ----------------------------------------------------------------------------
# Section 6 — sibling non-inheritance, demonstrated
# ----------------------------------------------------------------------------

def sibling_non_inheritance() -> None:
    print_header("Sibling non-inheritance — the substrate invariant, shown")
    print()
    print("  The woodcutter's branch asserts stole(Woodcutter, dagger).")
    print("  Per the fold-scope rule, this fact should be visible on")
    print("  :b-woodcutter and on no other branch — sibling :contested")
    print("  branches do not inherit from each other. Below, the per-branch")
    print("  world state for stole(Woodcutter, dagger):")
    print()
    p = stole("woodcutter", "dagger")
    for b in CONTESTED_BRANCHES:
        scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
        w = project_world(scoped, 100)
        verdict = "TRUE" if p in w else "absent"
        print(f"  {b.label:<18}  {verdict}")
    print()
    print("  The D4 branch-scoping rule mirrors this for descriptions.")
    print("  The wife's texture description on E_intercourse is visible on")
    print("  :b-wife only, not on sibling branches:")
    print()
    anchor = anchor_event("E_intercourse")
    for b in CONTESTED_BRANCHES:
        visible = descriptions_on_branch(
            branch=b, descriptions=descriptions_for(anchor, DESCRIPTIONS),
            events=EVENTS_ALL, all_branches=ALL_BRANCHES, up_to_τ_a=10_000,
        )
        wife_texture = any(d.id == "D_intercourse_wife_texture" for d in visible)
        verdict = "TRUE" if wife_texture else "absent"
        print(f"  {b.label:<18}  {verdict}")


# ----------------------------------------------------------------------------
# Section 7 — description surface summary
# ----------------------------------------------------------------------------

def description_surface_summary() -> None:
    print_header("Description surface — summary")
    print()
    by_kind_counts = {}
    by_attention_counts = {}
    for d in DESCRIPTIONS:
        by_kind_counts[d.kind] = by_kind_counts.get(d.kind, 0) + 1
        by_attention_counts[d.attention.value] = \
            by_attention_counts.get(d.attention.value, 0) + 1
    print("  By kind:")
    for k in sorted(by_kind_counts):
        print(f"    {k:<24} {by_kind_counts[k]}")
    print()
    print("  By attention:")
    for a in sorted(by_attention_counts):
        print(f"    {a:<24} {by_attention_counts[a]}")
    print()
    questions = open_questions(DESCRIPTIONS)
    print(f"  Open questions (is_question=True): {len(questions)}")
    for q in questions:
        print(f"    · [{q.kind}] {q.text[:72]}{'...' if len(q.text) > 72 else ''}")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> None:
    print()
    print("Rashomon — substrate prototype (four contested branches + descriptions)")
    print()
    print("Branches:")
    for b in CONTESTED_BRANCHES:
        print(f"  · {b.label:<18} — {BRANCH_NAMES[b.label]}")

    # τ_s=100 is well past all grove-scene events; the full testimony
    # content is folded. τ_d=100 likewise exceeds all sjuzhet entries.
    world_state_matrix(τ_s=100)
    reader_state_matrix(up_to_τ_d=100)
    intercourse_descriptions()
    per_branch_irony_counts(up_to_τ_d=100, τ_s=100)
    agreement_on_killer()
    sibling_non_inheritance()
    description_surface_summary()
    print()


if __name__ == "__main__":
    main()
