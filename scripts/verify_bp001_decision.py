#!/usr/bin/env python3
"""Verify the BP-001 decision pack, optionally against exported xcresult attachments.

No renderer execution or owner acceptance is implied. Run from any directory:
  python3 scripts/verify_bp001_decision.py [--capture-root PATH] [--output PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops

import palette_conformance as palette_audit

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "docs/review/bp001-decision-20261116"
PLATES = ROOT / "docs/review/bp001-same-art-pair"
BASES = (
    "BP001-quiet-street-current", "BP001-quiet-street-midpoint",
    "BP001-encounter-current", "BP001-encounter-projected-100-same-art",
)
SOURCES = (
    "AppTests/BenchmarkCaptureTests.swift", "App/BenchmarkReviewArt.swift",
    "App/WorldRenderer.swift", "App/GameScene.swift",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(capture_root: Path | None = None) -> dict:
    provenance = json.loads((PACK / "capture-provenance.json").read_text())
    assert provenance["ownerChoice"] == "UNRECORDED"
    assert provenance["shippingMappingChanged"] is False
    for name, digest in provenance["referenceSHA256"].items():
        assert sha(PACK / name) == digest, f"concept reference changed: {name}"
    assert set(provenance["sourceSHA256"]) == set(SOURCES)
    for name, digest in provenance["sourceSHA256"].items():
        assert sha(ROOT / name) == digest, f"capture source changed: {name}"
    observed = {}
    if capture_root:
        for kind in ("quiet", "encounter"):
            folder = capture_root / f"{kind}-attachments"
            for group in json.loads((folder / "manifest.json").read_text()):
                for attachment in group["attachments"]:
                    name = attachment["suggestedHumanReadableName"].split("_0_")[0]
                    if name.startswith("BP001-") and attachment["exportedFileName"].endswith(".png"):
                        assert name not in observed, f"duplicate attachment: {name}"
                        observed[name] = folder / attachment["exportedFileName"]
    expected = set()
    for base in BASES:
        for geometry in ("", "-geometry"):
            for scale in ("", "-half", "-gray"):
                name = base + geometry + scale
                expected.add(name)
                path = PLATES / (name + ".png")
                with Image.open(path) as image:
                    expected_size = (1056, 489) if scale == "-half" else (2112, 978)
                    assert image.size == expected_size, f"wrong dimensions: {name}"
                    if scale == "-gray":
                        r, g, b = image.convert("RGB").split()
                        assert ImageChops.difference(r, g).getbbox() is None, name
                        assert ImageChops.difference(g, b).getbbox() is None, name
                assert sha(path) == provenance["plateSHA256"][name], f"plate drift: {name}"
                if capture_root:
                    assert path.read_bytes() == observed[name].read_bytes(), f"fresh capture mismatch: {name}"
    assert set(provenance["plateSHA256"]) == expected
    if capture_root:
        assert set(observed) == expected, "incomplete fresh comparison export"
    palette = json.loads((PACK / "palette-report.json").read_text())
    assert palette["method"] == "BP-011"
    assert len(palette["plates"]) == 4
    assert {Path(p["file"]).stem for p in palette["plates"]} == set(BASES)
    reference = palette_audit.measure(ROOT / palette["reference"]["file"])
    assert {k: v for k, v in reference.items() if k != "file"} == {
        k: v for k, v in palette["reference"].items() if k != "file"}
    for plate in palette["plates"]:
        actual = palette_audit.measure(ROOT / plate["file"], exclude_top=240)
        actual["file"] = plate["file"]
        actual["zone"] = None
        actual["flags"] = palette_audit.flags(actual, reference, None)
        assert actual == plate, f"palette drift: {plate['file']}"
    return {"status": "VERIFIED_STATIC_DECISION_EVIDENCE_NOT_ACCEPTANCE",
            "plates": len(expected), "sourceFiles": len(provenance["sourceSHA256"]),
            "freshExportByteMatches": len(expected) if capture_root else None,
            "checks": ["recorded source hashes", "24 plate hashes and dimensions",
                       "grayscale channels", "four natural palette measurements"],
            "ownerChoice": "UNRECORDED", "shippingMappingChanged": False}


def record_provenance(capture_root: Path) -> None:
    plates = {}
    captures = []
    for kind in ("quiet", "encounter"):
        folder = capture_root / f"{kind}-attachments"
        for group in json.loads((folder / "manifest.json").read_text()):
            for attachment in group["attachments"]:
                name = attachment["suggestedHumanReadableName"].split("_0_")[0]
                if name.startswith("BP001-") and attachment["exportedFileName"].endswith(".png"):
                    path = folder / attachment["exportedFileName"]
                    assert path.read_bytes() == (PLATES / (name + ".png")).read_bytes(), name
                    assert name not in plates, name
                    plates[name] = sha(path)
                    captures.append({"plate": name, "device": attachment["deviceName"],
                                     "unixTimestamp": attachment["timestamp"],
                                     "exportedFileName": attachment["exportedFileName"]})
    assert len(plates) == 24
    provenance = {
        "status": "STATIC_OWNER_DECISION_EVIDENCE_ONLY",
        "ownerChoice": "UNRECORDED", "shippingMappingChanged": False,
        "capture": {"xcresult": "ss-receipt-v2-20261115/app-Debug.xcresult",
                    "configuration": "Debug", "xcode": "26.5 (17F42)",
                    "os": "iOS Simulator 26.5 (23F77)",
                    "viewportPoints": [704, 326], "nativePixels": [2112, 978],
                    "halfPixels": [1056, 489], "displayScale": 3,
                    "runtimeBase": "df8473713a3d37aeca05d4e1110f979f197b9ceb",
                    "workingTree": "receipt-v2 candidate overlay, not a clean capture commit",
                    "sourceQualification": "Captured App and fixture source bytes equal runtimeBase and receipt-v2 final head dcf073c0; receipt changes do not touch these sources"},
        "quiet": {"kind": "controlled modified street fixture", "cameraIntegrity": 3,
                  "buildingRegistration": "uniform constrained building, same on both sides"},
        "encounter": {"kind": "unedited command-driven snapshot, paused presentation",
                      "seed": 1, "upgrade": "ghostStep", "tick": 4976,
                      "player": [1205, 1039], "facing": "s", "enemies": 7,
                      "projectiles": 1, "telegraphs": 0, "cameras": 8,
                      "scenarioSeeded": False, "registerServiceBuilding": False,
                      "digest": "d96494f03b4ade6a6a6dc02961ffd1dc73c5e1f2a86a029ca6dcd22d207162f5"},
        "paletteExclusions": {"topNativePixelRows": 240, "topViewportPoints": 80,
                              "referenceCrop": "none", "lowerTouchControls": "retained",
                              "zoneAllowance": "none", "geometryOverlays": "not measured"},
        "referenceOrigin": "SS-specs@08406b9 docs/review/phase4, unchanged copies",
        "referenceSHA256": {name: sha(PACK / name) for name in
                            ("street-corner-approved-concept.png", "street-corner-midpoint-concept.png")},
        "sourceSHA256": {name: sha(ROOT / name) for name in SOURCES},
        "plateSHA256": dict(sorted(plates.items())), "attachments": captures,
        "limitations": ["Shipping control is not a measured original-reference projection",
                        "No owner projection selection, live input/facing, traversal, dense-combat or physical-device acceptance",
                        "No production art admission or gameplay change"]}
    (PACK / "capture-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-root", type=Path)
    parser.add_argument("--record-provenance", action="store_true",
                        help="record fresh matching exports before verification")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.record_provenance:
        if not args.capture_root:
            parser.error("--record-provenance requires --capture-root")
        record_provenance(args.capture_root)
    result = verify(args.capture_root)
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
