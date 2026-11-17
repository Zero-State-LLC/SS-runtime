#!/usr/bin/env python3
"""Check the built Release product, not source-level conditional compilation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

app = Path(sys.argv[1]).resolve(strict=True)
executable = app / "SSRuntime"
raw = executable.read_bytes()
symbols = subprocess.check_output(["nm", "-j", str(executable)], text=True)
assert "KioskPlayableReview" not in symbols, "Review symbols present in Release"
for marker in [b"-SSKioskReview", b"debug-playable-kiosk-review-001"]:
    assert marker not in raw, "Review launch/schema bytes present in Release"
forbidden = {
    "c411e33b79e0ffc5b0eb86143cd8785a564e573b5819bc1d4c399ef5d3b60264",
    "5a1c7fa1cf23d7bd85bc5676b4a0e297662071404cbb3ec454c9153a7d97c931",
    "c3313e0475e6aac62f1ec66ff7db4e254ae95e4ef193c5079bf5921e1e90d63b",
}
images = sorted(app.rglob("*.png"))
assert images, "No bundled images inspected"
for image in images:
    assert hashlib.sha256(image.read_bytes()).hexdigest() not in forbidden, f"Review image bundled: {image}"
print(json.dumps({
    "status": "RELEASE_REVIEW_EXCLUSION_VERIFIED_NOT_DEVICE_QUALIFICATION",
    "executableSHA256": hashlib.sha256(raw).hexdigest(),
    "pngFilesInspected": len(images),
    "reviewSymbolAbsent": True,
    "reviewLaunchAndSchemaBytesAbsent": True,
    "reviewImageHashesAbsent": True,
}, indent=2))
