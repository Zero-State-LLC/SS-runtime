"""Compare recorded tick selection with wall-time proxies, not display evidence."""
import argparse
import hashlib
import json
from bisect import bisect_right
from pathlib import Path


def compare(path):
    data = path.read_bytes()
    records = json.loads(data)
    if not isinstance(records, list) or not records:
        return None
    rows = [r for r in records if not r.get("warmup", False)]
    if not rows or rows[0].get("reducedMotion", True):
        return None
    entry = next(i for i, r in enumerate(rows) if r["settleFrame"] == 0)
    start = rows[entry]
    units = start["settleUnitsPerSecond"]
    holds = start["settleFrameUnits"]
    boundaries = [sum(holds[:i]) for i in range(len(holds))]
    assert boundaries[-1] / units == 0.375, "Accepted neutral boundary changed"

    def index(elapsed):
        return max(0, min(len(holds) - 1, bisect_right(boundaries, elapsed * units) - 1))

    active = []
    for row in rows[entry:]:
        if row["settleFrame"] < 0:
            break
        expected = index((row["tick"] - start["tick"]) / 60)
        assert expected == row["settleFrame"], "Tick reconstruction differs from native evidence"
        active.append(row)
    observed = sorted({r["settleFrame"] for r in active})
    proxies = {}
    modes = ["post-action-wall-time", "wall-time-minus-update-duration"]
    if "clockSample" in start:
        modes += ["spritekit-update-time", "tick-plus-residual"]
    for mode in modes:
        def clock(row):
            if mode == "spritekit-update-time":
                return row["clockSample"]["spriteKitTime"]
            if mode == "tick-plus-residual":
                return row["tick"] / 60 + row["clockSample"]["accumulatorAfter"]
            offset = row["updateStageSeconds"]["total"] if mode.endswith("duration") else 0
            return row["wallTime"] - offset
        origin = clock(start)
        samples = []
        for row in rows[entry:]:
            elapsed = clock(row) - origin
            samples.append({"tick": row["tick"], "elapsed": elapsed, "frame": index(elapsed)})
            if elapsed >= boundaries[-1] / units:
                break
        assert samples[-1]["elapsed"] >= 0.375, "Capture ends before neutral"
        proxies[mode] = {
            "samples": samples,
            "missing": sorted(set(range(len(holds))) - {r["frame"] for r in samples}),
        }
    return {
        "source": str(path), "sha256": hashlib.sha256(data).hexdigest(),
        "release": start["releaseTargetFrame"] + 1,
        "tickReconstructionMatches": True,
        "observedMissing": sorted(set(range(len(holds))) - set(observed)),
        "proxies": proxies,
        "limit": "No sampled clock proves physical presentation. Wall-time proxies are not SpriteKit time. "
                 "Subtracting update duration does not remove action evaluation or scheduling delay. "
                 "These are sensitivity comparisons, not validated clock replacements.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attachments", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    results = [result for path in sorted(args.attachments.glob("*.json"))
               if path.name != "manifest.json" and (result := compare(path)) is not None]
    assert {r["release"] for r in results} == {5, 13}, "Require both Standard release phases"
    assert len(results) == 2, "Ambiguous or duplicate capture variants"
    args.output.write_text(json.dumps(results, indent=2) + "\n")
    for result in results:
        print(result["release"], "observed missing", result["observedMissing"],
              "proxy missing", {k: v["missing"] for k, v in result["proxies"].items()})
