"""Summarize native midpoint attachments without treating callbacks as display proof."""
import argparse
import hashlib
import json
import statistics
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("attachments", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()
rows = []
for path in sorted(args.attachments.glob("*.json")):
    data = json.loads(path.read_text())
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        continue
    first = data[0]
    if first.get("settleUnitsPerSecond") != 128:
        continue
    active = [row for row in data if not row["warmup"] and row["tick"] > 0]
    if len(active) < 2:
        raise ValueError(f"Insufficient active observations: {path}")
    gaps = [(b["wallTime"] - a["wallTime"]) * 1000 for a, b in zip(active, active[1:])]
    if min(gaps) < 0:
        raise ValueError(f"Nonmonotonic callback wall clock: {path}")
    poses = sorted({row["settleFrame"] for row in active if row["settleFrame"] >= 0})
    costs = [row["updateStageSeconds"]["total"] * 1000 for row in active]
    neutral = [row for row in active if row["settleFrame"] == 16]
    rows.append({
        "attachment": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "release": first["releaseTargetFrame"] + 1, "reducedMotion": first["reducedMotion"],
        "observedPoseIndices": poses, "unobservedPoseIndices": [] if first["reducedMotion"] else sorted(set(range(17)) - set(poses)),
        "callbackMedianMs": statistics.median(gaps), "callbackMaxMs": max(gaps),
        "updateMedianMs": statistics.median(costs), "updateMaxMs": max(costs),
        "firstActiveWallTime": active[0]["wallTime"], "lastActiveWallTime": active[-1]["wallTime"],
        "firstNeutralWallTime": neutral[0]["wallTime"] if neutral else None,
        "scope": "callback selection and CPU update measurements; not video or physical display acceptance",
    })
keys = [(row["release"], row["reducedMotion"]) for row in rows]
if len(keys) != 4 or set(keys) != {(phase, reduced) for phase in (5, 13) for reduced in (False, True)}:
    raise ValueError(f"Expected exactly four midpoint variants, found {keys}")
args.output.write_text(json.dumps(rows, indent=2) + "\n")
print(f"Summarized {len(rows)} midpoint variants")
