"""
demo.py — run the substrate against the encoded Oedipus Rex slice and
print a narrative report.

For a series of discourse-time milestones (τ_d), prints:
  - what the reader knows / believes / holds as open questions about the
    four central propositions of the tragedy
  - what Oedipus holds about the same
  - what Jocasta holds about the same
  - live dramatic ironies on those propositions
  - for the two anagnorisis moments, the delta in the realizing agent's state

Run:
    cd prototype && python3 -m demos.demo
"""

from __future__ import annotations

from story_engine.core.substrate import (
    Branch, BranchKind, CANONICAL, CANONICAL_LABEL,
    Slot, Confidence,
    scope, project_knowledge, project_reader, project_world,
    dramatic_ironies, sternberg_curiosity,
)
from story_engine.encodings.oedipus import (
    FABULA, SJUZHET, AGENT_IDS,
    child_of, killed, married, dead, king, adopted_by,
    gap_real_parents,
)


ALL_BRANCHES = {CANONICAL_LABEL: CANONICAL}


# ----------------------------------------------------------------------------
# Display helpers
# ----------------------------------------------------------------------------

AGENT_NAMES = {
    "oedipus": "Oedipus",
    "jocasta": "Jocasta",
    "laius":   "Laius",
    "polybus": "Polybus",
    "merope":  "Merope",
    "messenger": "Messenger",
    "shepherd": "Shepherd",
    "reader":  "Reader",
}

def name(agent_id: str) -> str:
    return AGENT_NAMES.get(agent_id, agent_id)

def format_prop(p) -> str:
    # Pretty-print propositions with entity names instead of ids.
    args_pretty = []
    for a in p.args:
        if isinstance(a, str) and a in AGENT_NAMES:
            args_pretty.append(AGENT_NAMES[a])
        else:
            args_pretty.append(str(a))
    if not args_pretty:
        return p.predicate
    return f"{p.predicate}({', '.join(args_pretty)})"

def slot_label(slot: Slot) -> str:
    return {
        Slot.KNOWN:     "known",
        Slot.BELIEVED:  "believed",
        Slot.SUSPECTED: "suspected",
        Slot.GAP:       "gap",
    }[slot]

SEP = "─" * 76


# ----------------------------------------------------------------------------
# The central propositions of the tragedy. Irony displays filter by these.
# ----------------------------------------------------------------------------

CENTRAL_PROPS = [
    killed("oedipus", "laius"),
    child_of("oedipus", "laius"),
    child_of("oedipus", "jocasta"),
    married("oedipus", "jocasta"),
]

# Agents we report state for in each milestone. (Reader reported separately.)
REPORTED_AGENTS = ["oedipus", "jocasta"]


def report_agent_state(agent_id: str, τ_s: int, banner: str) -> None:
    events_in_scope = scope(CANONICAL, FABULA, ALL_BRANCHES)
    state = project_knowledge(agent_id, events_in_scope, τ_s)
    print(f"  {banner}")
    for p in CENTRAL_PROPS:
        h = state.holds(p)
        if h is None:
            print(f"    {format_prop(p):<42}  —  (not held)")
        else:
            print(f"    {format_prop(p):<42}  —  {slot_label(h.slot)}")


def report_reader_state(reader_state, banner: str) -> None:
    print(f"  {banner}")
    for p in CENTRAL_PROPS:
        h = reader_state.holds(p)
        if h is None:
            print(f"    {format_prop(p):<42}  —  (not held)")
        else:
            print(f"    {format_prop(p):<42}  —  {slot_label(h.slot)}")


def report_ironies(reader_state, τ_s: int) -> None:
    ironies = dramatic_ironies(
        agent_ids=REPORTED_AGENTS,
        reader_state=reader_state,
        all_events=FABULA,
        branch=CANONICAL,
        all_branches=ALL_BRANCHES,
        τ_s=τ_s,
    )
    # Filter to central propositions for display.
    ironies = [i for i in ironies if i.prop in CENTRAL_PROPS]
    # Deduplicate by (informed, uninformed, prop).
    seen = set()
    unique = []
    for i in ironies:
        key = (i.informed_id, i.uninformed_id, i.prop)
        if key in seen:
            continue
        seen.add(key)
        unique.append(i)

    if not unique:
        print("  Live ironies on the central propositions:  (none)")
        return

    print("  Live ironies on the central propositions:")
    for i in unique:
        print(f"    {name(i.informed_id)} > {name(i.uninformed_id)}:  "
              f"{format_prop(i.prop)}")


def report_curiosity(reader_state) -> None:
    gaps = sternberg_curiosity(reader_state)
    if not gaps:
        print("  Reader's open curiosity gaps:  (none)")
        return
    print("  Reader's open curiosity gaps:")
    for h in gaps:
        print(f"    {format_prop(h.prop)}")


def held_diff(before, after):
    """Tuple of (removed, added, migrated) Helds between two states."""
    before_map = {h.prop: h for h in before.by_prop}
    after_map  = {h.prop: h for h in after.by_prop}
    removed  = [h for p, h in before_map.items() if p not in after_map]
    added    = [h for p, h in after_map.items()  if p not in before_map]
    migrated = [(before_map[p], after_map[p])
                for p in before_map if p in after_map
                and before_map[p].slot != after_map[p].slot]
    return removed, added, migrated


def report_anagnorisis_delta(agent_id: str, τ_s_before: int, τ_s_after: int) -> None:
    events_in_scope = scope(CANONICAL, FABULA, ALL_BRANCHES)
    before = project_knowledge(agent_id, events_in_scope, τ_s_before)
    after  = project_knowledge(agent_id, events_in_scope, τ_s_after)
    removed, added, migrated = held_diff(before, after)

    print(f"  ANAGNORISIS — {name(agent_id)}:")
    for h in removed:
        print(f"    removed  ({slot_label(h.slot)})   {format_prop(h.prop)}")
    for bh, ah in migrated:
        print(f"    migrated {slot_label(bh.slot)} → {slot_label(ah.slot)}  "
              f"{format_prop(ah.prop)}")
    for h in added:
        print(f"    added    ({slot_label(h.slot)})   {format_prop(h.prop)}")


# ----------------------------------------------------------------------------
# Milestones — (τ_d, τ_s, caption)
# ----------------------------------------------------------------------------

MILESTONES = [
    (0,  -46, "τ_d=0 — play opens; the audience enters knowing the myth"),
    (5,    5, "τ_d=5 — Jocasta mentions the crossroads; Oedipus grows uneasy"),
    (7,    7, "τ_d=7 — Messenger announces Polybus's death"),
    (8,    8, "τ_d=8 — Messenger reveals the adoption"),
    (9,    9, "τ_d=9 — Jocasta realizes"),
    (12,  12, "τ_d=12 — the Shepherd testifies"),
    (13,  13, "τ_d=13 — Oedipus's anagnorisis"),
]


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> None:
    print()
    print("Oedipus Rex — substrate prototype")
    print("Central propositions tracked:")
    for p in CENTRAL_PROPS:
        print(f"  · {format_prop(p)}")
    print()

    prior_oedipus_τ_s = None
    prior_jocasta_τ_s = None

    for (τ_d, τ_s, caption) in MILESTONES:
        print(SEP)
        print(caption)
        print(SEP)

        reader_state = project_reader(
            sjuzhet=SJUZHET,
            all_events=FABULA,
            branch=CANONICAL,
            all_branches=ALL_BRANCHES,
            up_to_τ_d=τ_d,
        )
        report_reader_state(reader_state,      banner="Reader:")
        report_agent_state("oedipus", τ_s,     banner="Oedipus:")
        report_agent_state("jocasta", τ_s,     banner="Jocasta:")
        report_ironies(reader_state, τ_s)
        report_curiosity(reader_state)

        # Anagnorisis deltas.
        if τ_d == 9 and prior_jocasta_τ_s is not None:
            print()
            report_anagnorisis_delta("jocasta", prior_jocasta_τ_s, τ_s)
        if τ_d == 13 and prior_oedipus_τ_s is not None:
            print()
            report_anagnorisis_delta("oedipus", prior_oedipus_τ_s, τ_s)

        prior_oedipus_τ_s = τ_s
        prior_jocasta_τ_s = τ_s
        print()


if __name__ == "__main__":
    main()
