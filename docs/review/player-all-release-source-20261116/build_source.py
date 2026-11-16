#!/usr/bin/env python3
"""Offline source-only release continuation. No runtime or original input writes.

Adaptation authority: ../player-settle-prototype/build_source.py:6-52.
Paint, meshes, material ownership and assembly come from the supplied editable
bounded source, not from generated imagery. New phases are PROPOSED.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image

NAMES = ("SS-player-bounded-proportions", "SS-player-bounded-neutral", "SS-player-settle-prototype")
PRESERVED = (5, 13)
EPS = 1e-8  # Inherited numerical tolerance, not a visual acceptance threshold.
TIMING = {"unitsPerSecond": 128, "frameUnits": [3] * 17, "neutralBoundaryUnits": 48,
          "neutralBoundarySeconds": 0.375, "totalUnitsIncludingNeutralHold": 51}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    result = {}
    for name in NAMES:
        require((root / name).is_dir(), f"Missing source input: {name}")
        for path in sorted((root / name).rglob("*")):
            require(not path.is_symlink(), f"Input symlink not allowed: {path}")
            if path.is_file():
                result[str(path.relative_to(root))] = sha(path)
    return result


def legs(pose):
    pairs = pose["legs"]
    require(len(pairs) == 2 and {q["side"] for q in pairs} == {"left", "right"}, "Expected exactly two named legs")
    return {q["side"]: q for q in pairs}


def support_side(source):
    by_side = legs(source)
    planted = [q for q in by_side.values() if q["contact"]]
    require(len(planted) <= 1, "Ambiguous double-planted release requires explicit authoring")
    if planted:
        require(abs(planted[0]["toe"][2]) <= EPS, "Planted source toe above ground")
        return planted[0]["side"]
    ordered = sorted(by_side.values(), key=lambda q: q["toe"][2])
    require(abs(ordered[0]["toe"][2] - ordered[1]["toe"][2]) > EPS, "Equal airborne toe heights require explicit authoring")
    return ordered[0]["side"]


def solve(hip, ankle):
    axis = ankle - hip
    distance = np.linalg.norm(axis)
    require(2 < distance < 27, f"Unreachable hip/ankle distance: {distance}")
    axis = axis / distance
    along = (12.5**2 - 14.5**2 + distance**2) / (2 * distance)
    height = math.sqrt(12.5**2 - along**2)
    forward = np.array([0.0, 1.0, 0.0])
    forward -= axis * np.dot(forward, axis)
    require(np.linalg.norm(forward) > EPS, "Degenerate knee bend plane")
    forward /= np.linalg.norm(forward)
    return hip + along * axis + height * forward


def foot(side, hip, toe, angle, contact, origin):
    r = math.radians(angle)
    ankle = toe + np.array([0, -7.5 * math.cos(r) + 3 * math.sin(r), 7.5 * math.sin(r) + 3 * math.cos(r)])
    heel = toe + np.array([0, -10 * math.cos(r), 10 * math.sin(r)])
    return {"side": side, "phase": 0, "contact": contact, "angle": angle,
            "hip": hip.tolist(), "knee": solve(hip, ankle).tolist(), "ankle": ankle.tolist(),
            "heel": heel.tolist(), "toe": toe.tolist(),
            "contactWorld": (toe + origin).tolist() if contact else None}


def smooth(t):
    return t * t * (3 - 2 * t)


def generate(source, neutral):
    support = support_side(source)
    neutral_legs = legs(neutral)
    # Retain the authored world contact's offset when the entry is planted.
    # For airborne entries, the stationary source-local origin is zero.
    q = legs(source)[support]
    origin = np.array(q["contactWorld"]) - np.array(q["toe"]) if q["contact"] else np.zeros(3)
    samples = []
    for k in range(17):
        if k == 0:
            p = copy.deepcopy(source)
        else:
            p = {"time": source["time"], "legs": []}
            u, v = smooth(min(1, (k - 1) / 7)), smooth(max(0, (k - 8) / 8))
            for q in source["legs"]:
                n = neutral_legs[q["side"]]
                hip = np.array(q["hip"]) * (1 - u) + np.array(n["hip"]) * u
                w = v if q["side"] == support else u
                toe = np.array(q["toe"]) * (1 - w) + np.array(n["toe"]) * w
                if q["side"] == support:
                    toe[2] = 3 * math.sin(math.pi * v) if k > 8 else 0
                    contact = k <= 8 or k == 16
                else:
                    contact = k >= 8
                p["legs"].append(foot(q["side"], hip, toe, q["angle"] * (1 - w), contact, origin))
        p["settleProgress"] = k / 16
        p["settleSeconds"] = k * 3 / 128
        samples.append(p)
    return samples


def validate(samples, source, neutral, phase):
    require(len(samples) == 17, f"phase {phase}: expected 17 poses")
    require(samples[0]["legs"] == source["legs"], f"phase {phase}: entry source changed")
    support = support_side(source)
    neutral_legs = legs(neutral)
    rows, intervals = [], []
    for k, p in enumerate(samples):
        require(p["settleProgress"] == k / 16, f"phase {phase}: sample order at {k}")
        for side, q in legs(p).items():
            h, a, knee, toe, heel = (np.array(q[key], dtype=float) for key in ("hip", "ankle", "knee", "toe", "heel"))
            require(np.isfinite(np.concatenate((h, a, knee, toe, heel))).all(), f"phase {phase} pose {k} {side}: nonfinite geometry")
            upper, lower, reach = float(np.linalg.norm(h-knee)), float(np.linalg.norm(a-knee)), float(np.linalg.norm(h-a))
            label = f"phase {phase} pose {k} {side}"
            require(abs(upper-12.5) < EPS and abs(lower-14.5) < EPS, f"{label}: segment lengths {upper}/{lower}")
            require(2 < reach < 27, f"{label}: reach {reach}")
            require(min(toe[2], heel[2]) >= -EPS, f"{label}: ground clearance {toe[2]}/{heel[2]}")
            require(knee[2] <= h[2], f"{label}: knee above hip {knee[2]}/{h[2]}")
            if k:
                expected_contact = (k <= 8 or k == 16) if side == support else k >= 8
                require(q["contact"] == expected_contact, f"{label}: contact schedule")
            if q["contact"]:
                require(abs(toe[2]) < EPS and q["contactWorld"] is not None, f"{label}: invalid contact")
            else:
                require(q["contactWorld"] is None, f"{label}: airborne contactWorld")
            if k == 16:
                for key in ("hip", "knee", "ankle", "heel", "toe"):
                    require(np.allclose(q[key], neutral_legs[side][key], rtol=0, atol=EPS), f"{label}: neutral {key}")
            rows.append({"pose": k, "side": side, "upperLength": upper, "lowerLength": lower,
                         "reach": reach, "toeHeight": float(toe[2]), "heelHeight": float(heel[2]),
                         "kneeMinusHipHeight": float(knee[2]-h[2]), "contact": q["contact"],
                         "toe": q["toe"], "contactWorld": q["contactWorld"]})
    for side in ("left", "right"):
        start = None
        for k in range(18):
            active = k < 17 and legs(samples[k])[side]["contact"]
            if active and start is None:
                start = k
            if start is not None and not active:
                baseline = legs(samples[start])[side]
                for j in range(start, k):
                    current = legs(samples[j])[side]
                    require(np.allclose(current["toe"], baseline["toe"], rtol=0, atol=EPS), f"phase {phase}: {side} contact toe drift at {j}")
                    require(np.allclose(current["contactWorld"], baseline["contactWorld"], rtol=0, atol=EPS), f"phase {phase}: {side} world contact drift at {j}")
                intervals.append({"side": side, "firstPose": start, "lastPose": k-1,
                                  "firstUnits": start*3, "endExclusiveUnits": k*3,
                                  "maximumToeDrift": max(math.dist(legs(samples[j])[side]["toe"], baseline["toe"]) for j in range(start, k))})
                start = None
    for k in range(1, 9):
        require(legs(samples[k])[support]["toe"][:2] == legs(source)[support]["toe"][:2], f"phase {phase}: support slid at {k}")
    # Consecutive poses never move both toes horizontally.
    simultaneous = []
    for k in range(1, 17):
        moved = [s for s in ("left", "right") if math.dist(legs(samples[k-1])[s]["toe"][:2], legs(samples[k])[s]["toe"][:2]) > EPS]
        if len(moved) == 2:
            simultaneous.append(k)
    require(not simultaneous, f"phase {phase}: both toes slide at {simultaneous}")
    return {"phase": phase, "status": "PRESERVED" if phase in PRESERVED else "PROPOSED",
            "supportSide": support, "selection": "authored-contact" if any(q["contact"] for q in source["legs"]) else "lower-authored-toe",
            "contactIntervals": intervals, "simultaneousHorizontalToeMoves": simultaneous, "measurements": rows}


def adapt_assembly(text):
    replacements = [("t=pose['time'];phase=math.tau*t/.5;", "t=pose['time'];phase=math.tau*t/.5;settle_weight=1-pose['settleProgress'];", 1),
                    ("4*math.sin(phase-math.pi/4)", "4*settle_weight*math.sin(phase-math.pi/4)", 2),
                    ("swing=sign*math.cos(phase)", "swing=settle_weight*sign*math.cos(phase)", 1),
                    ("(1536,1792)", "(1536,2240)", 1),
                    ("assert len(set(x['rgbaSHA256'] for x in metrics))==16", "assert len(set(x['rgbaSHA256'] for x in metrics))==len(poses)", 1)]
    for old, new, count in replacements:
        require(text.count(old) == count, f"Assembly recipe drift at {old!r}")
        text = text.replace(old, new)
    return text


def rgba(path):
    with Image.open(path) as image:
        require(image.size == (384, 416), f"Unexpected frame size: {path}")
        return image.convert("RGBA").tobytes()


def endpoint_checks(frames, source_frame, neutral_frame, phase):
    checks = []
    for index, target in ((0, source_frame), (16, neutral_frame)):
        actual, expected = rgba(frames / f"{index:02d}.png"), rgba(target)
        if actual != expected:
            a, b = np.frombuffer(actual, dtype=np.uint8).reshape(-1,4), np.frombuffer(expected, dtype=np.uint8).reshape(-1,4)
            raise ValueError(f"phase {phase} endpoint {index}: {int(np.any(a != b, axis=1).sum())} RGBA pixels differ")
        checks.append({"pose": index, "exactRGBA": True, "rgbaSHA256": hashlib.sha256(actual).hexdigest()})
    return checks


def render_phase(root, work, samples, phase):
    base = root / NAMES[0]
    dst = work / f"phase-{phase:02d}"
    dst.mkdir(parents=True)
    shutil.copytree(base / "source", dst / "source", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(base / "boot/source", dst / "boot/source", ignore=shutil.ignore_patterns("__pycache__"))
    for name in ("material.py", "source.png", "four-facing-source.png", "registration.json", "retained-body-contact.png"):
        shutil.copy2(base / "boot" / name, dst / "boot" / name)
    shutil.copy2(base / "thigh.py", dst / "thigh.py")
    save(dst / "source/samples.json", samples)
    save(dst / "boot/samples.json", samples)
    (dst / "assemble.py").write_text(adapt_assembly((base / "assemble.py").read_text()))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    for relative in ("boot/material.py", "assemble.py"):
        result = subprocess.run([sys.executable, str(dst / relative)], cwd=dst, env=env, capture_output=True, text=True)
        (dst / (Path(relative).stem + ".log")).write_text(result.stdout + result.stderr)
        require(result.returncode == 0, f"phase {phase}: {relative} failed: {result.stderr[-2000:]}")
    return dst / "frames"


def completed_work(root, dst, samples):
    """Validate a completed source-render checkpoint, never trust existence alone."""
    record_path = dst / "assembly-record.json"
    if not record_path.exists():
        return False
    base = root / NAMES[0]
    for relative in ("source/samples.json", "boot/samples.json"):
        require(json.loads((dst / relative).read_text()) == samples, f"Checkpoint source mismatch: {dst}/{relative}")
    for folder in ("source", "boot/source"):
        for original in sorted((base / folder).rglob("*")):
            if not original.is_file() or "__pycache__" in original.parts:
                continue
            relative = original.relative_to(base)
            if str(relative) == "source/samples.json":
                continue
            require(sha(original) == sha(dst / relative), f"Checkpoint master changed: {relative}")
    for relative in ("thigh.py", "boot/material.py", "boot/source.png", "boot/four-facing-source.png", "boot/registration.json", "boot/retained-body-contact.png"):
        require(sha(base / relative) == sha(dst / relative), f"Checkpoint recipe changed: {relative}")
    require((dst / "assemble.py").read_text() == adapt_assembly((base / "assemble.py").read_text()), "Checkpoint assembly changed")
    records = json.loads(record_path.read_text())["frames"]
    require([row["frame"] for row in records] == list(range(17)), "Incomplete checkpoint assembly order")
    require(len({row["rgbaSHA256"] for row in records}) == 17, "Checkpoint lacks17 distinct source poses")
    for row in records:
        actual = hashlib.sha256(rgba(dst / "frames" / f'{row["frame"]:02d}.png')).hexdigest()
        require(actual == row["rgbaSHA256"], f"Checkpoint rendered pixels changed at {dst}, pose {row['frame']}")
    return True


def build(root, output, jobs, resume=False):
    root, output = root.resolve(), output.resolve()
    require(not output.is_relative_to(root) and not root.is_relative_to(output), "Output and source roots must not overlap")
    before = inventory(root)
    if resume:
        require(output.is_dir() and not (output / "manifest.json").exists(), "Resume requires an incomplete output")
        require(json.loads((output / "input-inventory.json").read_text()) == before, "Resume inputs changed")
    else:
        require(not output.exists(), f"Output exists, use a fresh path: {output}")
        output.mkdir(parents=True)
        save(output / "input-inventory.json", before)
    try:
        sources = json.loads((root / NAMES[0] / "source/samples.json").read_text())
        neutral = json.loads((root / NAMES[1] / "source/samples.json").read_text())[0]
        require(len(sources) == 16, "Expected all16 ordered movement phases")
        all_samples, facts, rendered = {}, [], {}
        for phase, source in enumerate(sources, 1):
            if phase in PRESERVED:
                samples = json.loads((root / NAMES[2] / f"phase-{phase:02d}/source/samples.json").read_text())
            else:
                samples = generate(source, neutral)
            all_samples[phase] = samples
            facts.append(validate(samples, source, neutral, phase))
        save(output / "geometry-contact-checks.json", facts)
        work = output / ".work"
        phases = [p for p in range(1, 17) if p not in PRESERVED]
        def render(p):
            dst = work / f"phase-{p:02d}"
            if resume and dst.exists():
                if completed_work(root, dst, all_samples[p]):
                    print(f"JCODE_PROGRESS {json.dumps({'message': f'Validated source checkpoint {p}', 'current': p, 'total': 16})}", flush=True)
                    return p, dst / "frames"
                preserved = work / f"interrupted-phase-{p:02d}"
                require(not preserved.exists(), f"Already interrupted twice: {p}")
                dst.rename(preserved)
            print(f"JCODE_PROGRESS {json.dumps({'message': f'Rendering source release {p}', 'current': p, 'total': 16})}", flush=True)
            return p, render_phase(root, work, all_samples[p], p)
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            rendered.update(pool.map(render, phases))
        for phase in PRESERVED:
            rendered[phase] = root / NAMES[2] / f"phase-{phase:02d}/frames"
        endpoints = {}
        for phase in range(1, 17):
            endpoints[phase] = endpoint_checks(rendered[phase], root / NAMES[0] / f"frames/{phase-1:02d}.png", root / NAMES[1] / "frames/00.png", phase)
        # No reviewable frames are published until every geometry/contact/endpoint check passes.
        records = []
        for phase in range(1, 17):
            dst = output / f"phase-{phase:02d}"
            (dst / "frames").mkdir(parents=True)
            if phase in PRESERVED:
                shutil.copy2(root / NAMES[2] / f"phase-{phase:02d}/source/samples.json", dst / "samples.json")
            else:
                save(dst / "samples.json", all_samples[phase])
            frames = []
            for k in range(17):
                path = dst / "frames" / f"{k:02d}.png"
                shutil.copy2(rendered[phase] / path.name, path)
                frames.append({"pose": k, "path": str(path.relative_to(output)), "fileSHA256": sha(path), "rgbaSHA256": hashlib.sha256(rgba(path)).hexdigest()})
            records.append({"phase": phase, "status": "PRESERVED" if phase in PRESERVED else "PROPOSED",
                            "samplesPath": str((dst / 'samples.json').relative_to(output)), "samplesSHA256": sha(dst / "samples.json"),
                            "endpoints": endpoints[phase], "frames": frames})
        require(inventory(root) == before, "Original input inventory changed")
        save(output / "manifest.json", {"status": "PROPOSED_SOURCE_ONLY_NOT_LIVE_CADENCE", "projectionDecision": "167171d89f9dfdad550e1b3b95510fc84514d0b1",
             "timing": TIMING, "preservedPhases": list(PRESERVED), "newPhases": phases,
             "inputsUnchanged": True, "inputFileCount": len(before), "phases": records,
             "limits": ["Source-only stationary root, not native playback", "Toe contacts, not full-sole contact", "Existing 3-unit lift remains an authored proposal", "Original5/13 timing fields are historical, manifest timing is explicit", "No art admission or visual acceptance"]})
    except Exception as error:
        unchanged = inventory(root) == before
        save(output / "failure.json", {"error": str(error), "inputsUnchanged": unchanged, "reviewPublished": False})
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=2, choices=range(1,5))
    parser.add_argument("--resume", action="store_true", help="Validate completed work and regenerate only interrupted phases")
    args = parser.parse_args()
    build(args.source_root, args.output, args.jobs, args.resume)


if __name__ == "__main__":
    main()
