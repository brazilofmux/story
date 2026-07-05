"""
draft_convergence.py — iterate generate → evaluate → repair to a
structural-fidelity ceiling.

The repair loop (`draft_repair.py`) fixes one beat and verifies it in
isolation. Convergence makes it a PIPELINE: splice each repaired scene
back into the draft, re-evaluate the WHOLE draft, and repeat until
fidelity stops climbing. The draft is a structured per-scene artifact so
a repaired scene can be substituted and the assembled text re-scored.

The control loop is dependency-injected — `evaluate_fn` (assembled text
→ fidelity report) and `repair_fn` (directive → new scene prose) are
passed in — so the convergence logic (stop conditions, splicing, score
trajectory) is pure and offline-testable; only the demo wires the real
API-backed functions.

Stop conditions (whichever first):
- fidelity reaches `target` (default 1.0);
- a round produces no localizable directives (nothing left to repair);
- a round does not improve the score over the previous round (a repair
  that didn't help — the round's repairs are ROLLED BACK so the returned
  scenes are the best-scoring draft, not the degraded one);
- `max_iters` reached (no repairs are applied on the way out — an
  unevaluated repair would make the final score describe prose nobody
  scored).

Invariant: the returned scenes are always the best-evaluated state, and
`final_score` is their score.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from story_engine.core.draft_repair import plan_repairs


def assemble(scenes) -> str:
    """Join per-scene prose in staged (tau_d) order — the assembled
    draft, mirroring GenerationResult.draft. `scenes` is a list of
    mutable dicts with 'tau_d' and 'prose'."""
    ordered = sorted(scenes, key=lambda s: s["tau_d"])
    return "\n\n".join((s.get("prose") or "").strip() for s in ordered)


@dataclass
class IterationRecord:
    iteration: int
    score: float
    n_directives: int
    repaired_events: list = field(default_factory=list)
    stopped: str = ""             # reason this was the last iteration, if so


@dataclass
class ConvergenceRun:
    history: list = field(default_factory=list)   # list[IterationRecord]
    scenes: list = field(default_factory=list)    # final per-scene dicts
    reports: list = field(default_factory=list)   # the per-round reports

    @property
    def initial_score(self) -> float:
        return self.history[0].score if self.history else 0.0

    @property
    def final_score(self) -> float:
        """Score of the RETURNED scenes. Because degrading rounds are
        rolled back and no repairs are applied after the last evaluation,
        the returned draft is always the best-evaluated state — so this is
        the max over the history, not necessarily the last record (the
        last record may document the degraded round that triggered the
        rollback)."""
        return max((r.score for r in self.history), default=0.0)

    @property
    def improved(self) -> float:
        return self.final_score - self.initial_score


def converge(
    *,
    scenes,
    mythos,
    evaluate_fn,
    repair_fn,
    plan_fn=plan_repairs,
    max_iters: int = 3,
    target: float = 1.0,
    on_round=None,
) -> ConvergenceRun:
    """Iterate evaluate → plan → repair → splice until convergence.

    `scenes` is mutated in place (repaired scenes' 'prose' replaced) and
    also returned on the run. `evaluate_fn(assembled_text)` returns a
    report exposing `.score` (float) and `.findings` (for plan_fn).
    `repair_fn(directive)` returns new prose for the directive's scene,
    or a falsy value to leave the scene unchanged.
    """
    run = ConvergenceRun(scenes=scenes)
    by_event = {}
    for s in scenes:
        by_event.setdefault(s["event_id"], []).append(s)

    snapshot = None   # (scene, prose) pairs from before the last repairs
    for it in range(max_iters):
        report = evaluate_fn(assemble(scenes))
        run.reports.append(report)
        score = float(getattr(report, "score", 0.0))
        directives = plan_fn(report, mythos)
        rec = IterationRecord(
            iteration=it, score=score, n_directives=len(directives),
        )
        run.history.append(rec)
        if on_round:
            on_round(rec, report, directives)

        # Stop conditions evaluated BEFORE repairing this round.
        if score >= target:
            rec.stopped = "target reached"
            break
        if it > 0 and score <= run.history[it - 1].score:
            # The previous round's repairs didn't help. Restore the prose
            # they replaced so the caller gets the best-scoring draft, not
            # the degraded one it was spliced into.
            if snapshot is not None:
                for s, prose in snapshot:
                    s["prose"] = prose
            rec.stopped = "no improvement over previous round"
            break
        if not directives:
            rec.stopped = "no localizable drift remaining"
            break
        if it == max_iters - 1:
            # Do NOT repair on the way out: an unevaluated repair would
            # leave final_score describing prose nobody scored.
            rec.stopped = "max_iters reached"
            break

        # Snapshot, then repair + splice.
        snapshot = [(s, s.get("prose")) for s in scenes]
        for d in directives:
            new_prose = repair_fn(d)
            if not new_prose:
                continue
            for s in by_event.get(d.event_id, []):
                s["prose"] = new_prose
                rec.repaired_events.append(d.event_id)

    return run
