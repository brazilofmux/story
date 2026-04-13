"""
demo_rashomon.py — run the substrate against the encoded Rashomon grove
scene and print a branch-indexed report.

Where demo.py (Oedipus) demonstrates reader-vs-character irony on a
single canonical branch, this demo exercises the `:contested` branch
machinery: four sibling branches, each internally consistent, mutually
incompatible, with the substrate reporting per-branch answers for the
same propositions.

Run:
    cd prototype && python3 demo_rashomon.py
"""

from __future__ import annotations

from substrate import (
    Slot, Confidence,
    scope, project_knowledge, project_reader, project_world,
    dramatic_ironies, sternberg_curiosity,
)
from rashomon import (
    EVENTS_ALL, SJUZHET_BY_BRANCH, AGENT_IDS, ALL_BRANCHES,
    CONTESTED_BRANCHES,
    B_TAJOMARU, B_WIFE, B_HUSBAND, B_WOODCUTTER,
    killed, killed_with, coerced, yielded_willingly, duel_character,
    stole, begged_to_kill, fled, dead, had_intercourse_with,
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
# Propositions whose contested status is the whole point. For each, the
# demo shows the per-branch verdict side by side.
# ----------------------------------------------------------------------------

CENTRAL_PROPS = [
    killed("tajomaru", "husband"),
    killed("wife",     "husband"),
    killed("husband",  "husband"),
    killed_with("tajomaru", "husband", "sword"),
    killed_with("wife",     "husband", "dagger"),
    killed_with("husband",  "husband", "dagger"),
    coerced("tajomaru", "wife"),
    yielded_willingly("wife", "tajomaru"),
    duel_character("tajomaru", "husband", "noble"),
    duel_character("tajomaru", "husband", "cowardly"),
    begged_to_kill("wife", "tajomaru", "husband"),
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
    # Column: each contested branch. Row: each proposition.
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
    print("  branch the reader holds that branch's disclosed facts as KNOWN;")
    print("  the facts of other branches are simply absent from this branch's")
    print("  reader state. Cross-branch uncertainty (meta-level) is a known")
    print("  soft spot — see rashomon.py's *Known soft spots* #2.")
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
# Section 3 — per-branch dramatic-irony summary
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
# Section 4 — where the branches agree vs disagree on a key proposition
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
# Section 5 — sibling non-inheritance, demonstrated
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
    print("  By contrast, had_intercourse_with(Tajomaru, the Wife) is on")
    print("  :canonical, so every branch sees it:")
    print()
    p2 = had_intercourse_with("tajomaru", "wife")
    for b in CONTESTED_BRANCHES:
        scoped = scope(b, EVENTS_ALL, ALL_BRANCHES)
        w = project_world(scoped, 100)
        verdict = "TRUE" if p2 in w else "absent"
        print(f"  {b.label:<18}  {verdict}")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> None:
    print()
    print("Rashomon — substrate prototype (four contested branches)")
    print()
    print("Branches:")
    for b in CONTESTED_BRANCHES:
        print(f"  · {b.label:<18} — {BRANCH_NAMES[b.label]}")

    # τ_s=100 is well past all grove-scene events; the full testimony
    # content is folded. τ_d=100 likewise exceeds all sjuzhet entries.
    world_state_matrix(τ_s=100)
    reader_state_matrix(up_to_τ_d=100)
    per_branch_irony_counts(up_to_τ_d=100, τ_s=100)
    agreement_on_killer()
    sibling_non_inheritance()
    print()


if __name__ == "__main__":
    main()
