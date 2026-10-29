#!/usr/bin/env python3
"""Summarize a pacing/heat probe report (JSONL from `PacingProbeTests`).

The probes write one JSON object per run. This prints what tuning decisions
need and the raw report hides: win rate and median winning time by pilot
profile, by upgrade, and by both; where failed runs die; and how much of a
winning run passes after Lockdown is entered. Sustained runs are excluded
(they never end by design); only legal runs are summarized.

    SS_HEAT_SEEDS=20 SS_HEAT_LEGAL_SEEDS=60 SS_HEAT_REPORT=$PWD/heat.jsonl \\
      swift test -c release -Xswiftc -enable-testing --filter heatD083StyleSweep
    python3 scripts/probe_summary.py heat.jsonl

These are bot pilots, not players (D-093). Use the numbers to find gaps, then
confirm them in a human playtest.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

TICKS_PER_SECOND = 60


def clock(seconds: float) -> str:
    return f"{int(seconds // 60)}:{int(seconds % 60):02d}"


def load(path: Path) -> list[dict]:
    runs = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if "error" in row:
            sys.exit(f"{path}: probe reported an error run: {row['error']}")
        runs.append(row)
    return runs


def table(title: str, runs: list[dict], key) -> None:
    groups: dict = defaultdict(list)
    for run in runs:
        groups[key(run)].append(run)
    print(f"\n{title}")
    print(f"  {'group':34} {'runs':>5} {'win':>7} {'median win':>11}  failures")
    for group in sorted(groups, key=str):
        rows = groups[group]
        wins = [r for r in rows if r["outcome"] == "success"]
        median = clock(statistics.median(r["ticks"] for r in wins) / TICKS_PER_SECOND) if wins else "-"
        failures: dict[str, int] = defaultdict(int)
        for r in rows:
            if r["outcome"] != "success":
                failures[r["failureReason"] or (f"stalled {r['stalledOn']}" if r["stalledOn"] else r["outcome"])] += 1
        label = " / ".join(group) if isinstance(group, tuple) else str(group)
        print(f"  {label:34} {len(rows):5} {100 * len(wins) / len(rows):6.1f}% {median:>11}  {dict(failures)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("report", type=Path, help="JSONL written by SS_HEAT_REPORT or SS_PACING_REPORT")
    args = parser.parse_args()

    runs = [r for r in load(args.report) if not r.get("sustained", False)]
    if not runs:
        sys.exit("no legal runs in report")
    print(f"{len(runs)} legal runs from {args.report}")

    table("By pilot profile", runs, lambda r: r["profile"])
    table("By upgrade", runs, lambda r: r["upgrade"])
    table("By profile and upgrade", runs, lambda r: (r["profile"], r["upgrade"]))

    failed = [r for r in runs if r["outcome"] != "success"]
    in_court = [r for r in failed if "bossActivated" in r["milestones"]]
    print(f"\nFailures: {len(failed)}; after the Captain activated: {len(in_court)}")
    if in_court:
        before = statistics.median(r["milestones"]["bossActivated"] for r in in_court) / TICKS_PER_SECOND
        survived = statistics.median(r["ticks"] - r["milestones"]["bossActivated"] for r in in_court) / TICKS_PER_SECOND
        print(f"  median time to reach the Court {clock(before)}; median time survived there {clock(survived)}")

    wins = [r for r in runs if r["outcome"] == "success" and "lockdownEntered" in r["milestones"]]
    if wins:
        share = sorted((r["ticks"] - r["milestones"]["lockdownEntered"]) / r["ticks"] for r in wins)
        entered = statistics.median(r["milestones"]["lockdownEntered"] for r in wins) / TICKS_PER_SECOND
        print(f"\nLockdown entered at a median {clock(entered)}; share of a winning run after it: "
              f"median {100 * statistics.median(share):.0f}% "
              f"(p10 {100 * share[len(share) // 10]:.0f}%, p90 {100 * share[9 * len(share) // 10]:.0f}%)")

    medal_wins = [r for r in runs if r["outcome"] == "success"]
    if medal_wins:
        counts: dict[str, int] = defaultdict(int)
        for r in medal_wins:
            for medal in r.get("medals", []):
                counts[medal] += 1
        earned = ", ".join(f"{m} {100 * n / len(medal_wins):.0f}%" for m, n in sorted(counts.items()))
        print(f"\nMedals per win ({len(medal_wins)} wins): {earned or 'none'}")


if __name__ == "__main__":
    main()
