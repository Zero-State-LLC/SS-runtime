"""Report recorded pose coverage without equating it with timing correctness."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
rows = []
for path in sorted((root / "midpoint-recording-attachments").glob("*.json")):
    data = json.loads(path.read_text())
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        continue
    first = data[0]
    if first.get("settleUnitsPerSecond") != 128:
        continue
    seen = sorted({r["settleFrame"] for r in data if r.get("settleFrame", -1) >= 0})
    reduced = first["reducedMotion"]
    rows.append({
        "attachment": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "releasePoseOneBased": first["releaseTargetFrame"] + 1,
        "reducedMotion": reduced,
        "observedPoseIndices": seen,
        "unobservedPoseIndices": [] if reduced else sorted(set(range(17)) - set(seen)),
        "coverageMeaning": "settle bypass expected" if reduced else "renderer callback observations, not physical display proof",
    })
assert len(rows) == 4, "Expected exactly two release poses by two motion modes"
assert {(r["releasePoseOneBased"], r["reducedMotion"]) for r in rows} == {(p, m) for p in (5, 13) for m in (False, True)}
(root / "midpoint-recorded-pose-coverage.json").write_text(json.dumps(rows, indent=2) + "\n")
print(json.dumps(rows, indent=2))
