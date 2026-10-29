#!/usr/bin/env python3
"""BP-011 palette conformance report (SS-specs benchmark-production.md, D-108).

Compares review plates with the approved Civic Seam concept on three values:
mean luminance, mean chroma and the share of pixels nearest each
civic-seam-visual-direction.md section 10 colour. A plate outside the band is
flagged for owner review; it is never rejected by this script.

    python3 scripts/palette_conformance.py PLATE.png [PLATE.png ...] \\
        --reference path/to/street-corner-approved-concept.png \\
        [--exclude-top 130] [--zone civicPlaza] [--json report.json]

The exact method is BP-011's: 8-bit sRGB, HUD rows excluded, box-filter
downsample to 300 px wide, Rec. 709 luminance weights on the 8-bit values
without linearising, chroma as max(R,G,B) - min(R,G,B), and nearest palette
colour by squared RGB distance.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

# civic-seam-visual-direction.md section 10.
PALETTE = {
    "fogLight": "CBD1CF",
    "civicLimestone": "BDB39F",
    "weatheredStucco": "A79C8B",
    "asphaltBlueGray": "343D43",
    "brickShadow": "594541",
    "bayWindowTeal": "406C6A",
    "transitRed": "A83D39",
    "agedBrass": "A68449",
    "phoenixGold": "D29A37",
    "surveillanceCyan": "39C8D8",
    "detectionRed": "EF4B47",
}
PALETTE_RGB = {name: tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) for name, value in PALETTE.items()}

# BP-011 PROPOSED band, relative to the reference; the owner may change it.
LUMINANCE_TOLERANCE = 0.25
CHROMA_CEILING_RATIO = 1.5
# A Civic Plaza plate may sit this much lighter (limestone massing).
ZONE_LUMINANCE_ALLOWANCE = {"civicPlaza": 0.15}
WIDTH = 300


def measure(path: Path, exclude_top: int = 0) -> dict:
    image = Image.open(path).convert("RGB")
    if exclude_top:
        image = image.crop((0, exclude_top, image.width, image.height))
    height = max(1, round(WIDTH * image.height / image.width))
    image = image.resize((WIDTH, height), Image.Resampling.BOX)
    pixels = image.tobytes()
    count = len(pixels) // 3
    luminance = chroma = 0.0
    shares = {name: 0 for name in PALETTE}
    for i in range(0, len(pixels), 3):
        r, g, b = pixels[i], pixels[i + 1], pixels[i + 2]
        luminance += 0.2126 * r + 0.7152 * g + 0.0722 * b
        chroma += max(r, g, b) - min(r, g, b)
        nearest = min(PALETTE_RGB, key=lambda n: (r - PALETTE_RGB[n][0]) ** 2
                      + (g - PALETTE_RGB[n][1]) ** 2 + (b - PALETTE_RGB[n][2]) ** 2)
        shares[nearest] += 1
    return {
        "file": str(path),
        "meanLuminance": round(luminance / count, 1),
        "meanChroma": round(chroma / count, 1),
        "paletteShares": {n: round(100 * c / count, 1) for n, c in sorted(shares.items(), key=lambda x: -x[1]) if c},
    }


def flags(plate: dict, reference: dict, zone: str | None) -> list[str]:
    allowance = ZONE_LUMINANCE_ALLOWANCE.get(zone or "", 0.0)
    low = reference["meanLuminance"] * (1 - LUMINANCE_TOLERANCE)
    high = reference["meanLuminance"] * (1 + LUMINANCE_TOLERANCE + allowance)
    ceiling = reference["meanChroma"] * CHROMA_CEILING_RATIO
    found = []
    if not low <= plate["meanLuminance"] <= high:
        found.append(f"meanLuminance {plate['meanLuminance']} outside {low:.0f}-{high:.0f}")
    if plate["meanChroma"] > ceiling:
        found.append(f"meanChroma {plate['meanChroma']} above {ceiling:.0f}")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="BP-011 palette conformance report")
    parser.add_argument("plates", nargs="+", type=Path)
    parser.add_argument("--reference", type=Path, required=True,
                        help="the approved concept (SS-specs docs/review/phase4/street-corner-approved-concept.png)")
    parser.add_argument("--exclude-top", type=int, default=0, help="HUD rows to exclude, in source pixels")
    parser.add_argument("--zone", help="the zone the plate mainly shows, e.g. civicPlaza")
    parser.add_argument("--json", type=Path, help="also write the report as JSON")
    args = parser.parse_args()

    reference = measure(args.reference)
    report = {"method": "BP-011", "reference": reference, "plates": []}
    print(f"reference  L={reference['meanLuminance']:5.1f}  C={reference['meanChroma']:4.1f}  "
          + ", ".join(f"{n} {v}%" for n, v in list(reference["paletteShares"].items())[:3]))
    for path in args.plates:
        plate = measure(path, args.exclude_top)
        plate["zone"] = args.zone
        plate["flags"] = flags(plate, reference, args.zone)
        report["plates"].append(plate)
        status = "FLAG: " + "; ".join(plate["flags"]) if plate["flags"] else "within band"
        print(f"{path.name}  L={plate['meanLuminance']:5.1f}  C={plate['meanChroma']:4.1f}  "
              + ", ".join(f"{n} {v}%" for n, v in list(plate["paletteShares"].items())[:3]) + f"  [{status}]")
    if args.json:
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
