#!/usr/bin/env python3
"""Import a complete successful static native all-release capture, never cadence evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PHASES = [p for p in range(1, 17) if p not in (5, 13)]
EXPECTED = {(phase, pose) for phase in PHASES for pose in range(17)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def attachments(exports):
    images, records = {}, []
    manifest = json.loads((exports / "manifest.json").read_text())
    for case in manifest:
        for item in case["attachments"]:
            name = item.get("suggestedHumanReadableName", "")
            match = re.search(r"allrelease-native-(\d+)-pose-(\d+)(?:_|\.|$)", name)
            path = exports / item["exportedFileName"]
            if match:
                key = tuple(map(int, match.groups()))
                if key in images:
                    raise ValueError(f"Duplicate native pose: {key}")
                images[key] = path
            elif name.startswith("allrelease-native-pose-records"):
                records.append(path)
    if set(images) != EXPECTED or len(records) != 1:
        raise ValueError("Expected exactly238 native poses and one record attachment")
    rows = json.loads(records[0].read_text())
    validate_records(rows)
    return images, records[0], rows


def validate_records(rows):
    if len(rows) != 238 or {(r["phase"], r["pose"]) for r in rows} != EXPECTED:
        raise ValueError("Native record census differs from images")
    for row in rows:
        expected = 0 if row["pose"] == 0 else (row["pose"] * 180 + 127) // 128
        if row["tickOffset"] != expected:
            raise ValueError("Native tick sampling differs from exact3/128 holds")
        p, k = row["phase"], row["pose"]
        source = (f"player-source-s-{p-1:02d}" if k == 0 else
                  "player-source-s-neutral" if k == 16 else f"player-allrelease-{p:02d}-{k:02d}")
        if row["source"] != source:
            raise ValueError("Native record names wrong source texture")


def verify_capture(target):
    report = json.loads((target / "verification.json").read_text())
    summary = report["summary"]
    if (report["status"] != "STATIC_NATIVE_SOURCE_CHECK_NOT_ADMISSION"
            or report["poses"] != 238 or report["phases"] != PHASES
            or summary.get("passedTests") != 2 or summary.get("failedTests") != 0
            or summary.get("skippedTests") != 0):
        raise ValueError("Published native evidence has invalid census or result")
    rows = json.loads((target / "pose-records.json").read_text())
    validate_records(rows)
    expected_files = {f"phase-{p:02d}-pose-{k:02d}.png" for p, k in EXPECTED} | {"pose-records.json"}
    expected_sources = {"AppTests/AllReleaseSourceTests.swift", "project.yml"} | {
        f"AppTests/BenchmarkAssets/{row['source']}.png" for row in rows}
    for key, root, expected in [("attachmentHashes", target, expected_files),
                                ("sourceHashes", ROOT, expected_sources)]:
        if set(report[key]) != expected:
            raise ValueError(f"Published {key} census differs")
        for name, digest in report[key].items():
            if sha(root / name) != digest:
                raise ValueError(f"Published evidence drift: {name}")
    for row in rows:
        if row.get("sourceSHA256") != report["sourceHashes"][f"AppTests/BenchmarkAssets/{row['source']}.png"]:
            raise ValueError("Published native source bytes differ")
    print(json.dumps({"status": report["status"], "verifiedPoses": 238,
                      "verifiedSources": len(expected_sources)}))


def import_capture(exports, result, target):
    if target.exists():
        raise ValueError("Use a fresh output path, preserve prior evidence")
    summary = json.loads(subprocess.check_output([
        "xcrun", "xcresulttool", "get", "test-results", "summary", "--path", str(result)], text=True))
    if not (summary.get("passedTests") == 2 and summary.get("failedTests") == 0
            and summary.get("skippedTests") == 0):
        raise ValueError(f"Expected successful two-test focused native run: {summary}")
    images, records, rows = attachments(exports)
    source_files = {"AppTests/AllReleaseSourceTests.swift", "project.yml"}
    source_files.update(f"AppTests/BenchmarkAssets/{row['source']}.png" for row in rows)
    hashes = {name: sha(ROOT / name) for name in sorted(source_files)}
    for row in rows:
        if row.get("sourceSHA256") != hashes[f"AppTests/BenchmarkAssets/{row['source']}.png"]:
            raise ValueError("Actual native source bytes differ from current resource")
    target.mkdir(parents=True)
    files = {}
    for (phase, pose), path in sorted(images.items()):
        name = f"phase-{phase:02d}-pose-{pose:02d}.png"
        shutil.copy2(path, target / name)
        files[name] = sha(target / name)
    shutil.copy2(records, target / "pose-records.json")
    files["pose-records.json"] = sha(target / "pose-records.json")
    report = {"status": "STATIC_NATIVE_SOURCE_CHECK_NOT_ADMISSION", "poses": len(images),
              "phases": PHASES, "xcresult": str(result.resolve()), "summary": summary,
              "sourceHashes": hashes, "attachmentHashes": files,
              "limits": ["Static isolated crop, not full704x326 scene acceptance",
                         "Not live cadence or moving contact", "Not four-facing admission",
                         "Source art and all new releases still require visual review"]}
    (target / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    options = "".join(f'<option value="{p:02d}">Release {p}</option>' for p in PHASES)
    html = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Player remaining releases: static native evidence</title>
<style>body{font:17px/1.6 system-ui;background:#202326;color:#eee;margin:32px;max-width:1000px}a{color:#a9d8df}button,select,input{font:inherit}img{width:576px;max-width:100%;image-rendering:auto}label{display:inline-block;margin:10px}aside{border-left:4px solid #c4ac76;padding:12px;background:#292d30}</style>
<h1>Remaining south releases: native pose inspection</h1>
<aside>238 static SpriteKit poses across14 new source candidates. This is not normal-speed playback, a shared-scene projection test, four-facing completion or art admission. Exact0.375s neutral boundary is preserved.</aside>
<p>Original releases5/13 are unchanged and excluded from this new capture. Images are isolated192×144-point crops, enlarged here for inspection. Source normal/quarter-speed reviews remain separate.</p><p><a href="../player-all-release-source-20261116/artifacts/normal-speed.html">Normal-speed source review</a> · <a href="../player-all-release-source-20261116/artifacts/quarter-speed.html">Quarter-speed source review</a> · <a href="README.md">Evidence and limitations</a> · <a href="review-verdict.md">Review verdict</a></p>
<label>Release <select id="phase">OPTIONS</select></label>
<label>Pose <input id="pose" type="range" min="0" max="16" value="0"></label>
<button id="previous">Previous pose</button> <button id="next">Next pose</button>
<p id="status" role="status"></p><a id="full" target="_blank" rel="noopener"><img id="image" alt="Static native Player pose"></a>
<p><a href="verification.json">Exact native result and hashes</a> · <a href="pose-records.json">Selected source and tick records</a></p>
<script>const phase=document.querySelector('#phase'),pose=document.querySelector('#pose'),image=document.querySelector('#image');function show(){const path=`phase-${phase.value}-pose-${String(pose.value).padStart(2,'0')}.png`;image.src=path;document.querySelector('#full').href=path;document.querySelector('#status').textContent=`Release ${Number(phase.value)}, pose ${Number(pose.value)+1}/17, static native image`;image.onerror=()=>{document.querySelector('#status').textContent='Missing image: '+path}}phase.onchange=show;pose.oninput=show;document.querySelector('#previous').onclick=()=>{pose.value=Math.max(0,Number(pose.value)-1);show()};document.querySelector('#next').onclick=()=>{pose.value=Math.min(16,Number(pose.value)+1);show()};show();</script></html>'''
    (target / "index.html").write_text(html.replace("OPTIONS", options))
    print(json.dumps({"status": report["status"], "poses": len(images), "passedTests": 2}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exports", type=Path)
    parser.add_argument("--xcresult", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path, help="Recheck published capture and source bytes without Xcode")
    args = parser.parse_args()
    if args.verify:
        verify_capture(args.verify)
    elif args.exports and args.xcresult and args.output:
        import_capture(args.exports, args.xcresult, args.output)
    else:
        parser.error("Use --verify PATH or all of --exports, --xcresult, --output")
