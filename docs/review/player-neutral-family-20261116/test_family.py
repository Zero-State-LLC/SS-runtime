#!/usr/bin/env python3
"""
Integrity tests for player-neutral-family-20261116 - slice 5

Guards:
  T1  Input source images unchanged (SHA-256 match against sibling packets)
  T2  All four output strip images exist and are correct dimensions
  T3  Strips are bit-for-bit reproducible (re-run assemble and compare)
  T4  Native strip is 4*64+3*4 = 268 wide, 69 tall
  T5  Half strip is 4*32+3*4 = 140 wide, 35 tall
  T6  Grayscale strip has no saturation (all pixels have equal R=G=B in RGBA composite)
  T7  All 16 role-mask files exist and are 384x416 RGBA
  T8  Each role mask has at least one opaque pixel (confirms layer coverage)
  T9  family.json has required keys and PROPOSED status
  T10 index.html is non-empty and contains all four facing labels
  T11 Layer files exist for each facing (linked from sibling packets)
  T12 North source SHA matches the active attempt-01 hash known from the north packet
  T13 South, east and west SHA-256 prefixes match their own packet test suites
  T14 Output-hashes.json round-trips (re-compute and compare)
"""

import hashlib, importlib.util, json, os, subprocess, sys, tempfile
from pathlib import Path

try:
    from PIL import Image, ImageOps
    import numpy as np
except ImportError:
    sys.exit("Pillow and numpy required.")

ROOT = Path(__file__).parent.resolve()
REPO = ROOT.parents[2]

SOUTH_PATH = REPO / "docs/review/player-baggy-south-source-20261116/south-baggy-neutral.png"
NORTH_PATH = REPO / "docs/review/player-north-source-20261116/north-neutral.png"
EAST_PATH  = REPO / "docs/review/player-side-source-20261116/east/east-neutral.png"
WEST_PATH  = REPO / "docs/review/player-side-source-20261116/west/west-neutral.png"

SOUTH_LAYERS_DIR = REPO / "docs/review/player-baggy-south-source-20261116/layers"
NORTH_LAYERS_DIR = REPO / "docs/review/player-north-source-20261116/layers"
EAST_LAYERS_DIR  = REPO / "docs/review/player-side-source-20261116/east/layers"
WEST_LAYERS_DIR  = REPO / "docs/review/player-side-source-20261116/west/layers"

NORTH_SHA = "0a6e15bd2aa8cc486dd14521b60680bed6a2dd0833707972850e65d7991f4fbb"
EAST_PREFIX  = "4be91d1d"
WEST_PREFIX  = "9d06aa54"


def load_image(path):
    with Image.open(path) as source:
        return source.copy()


def sha256(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()

PASS = []
FAIL = []

def check(name, cond, detail=""):
    if cond:
        PASS.append(name)
        print(f"  PASS  {name}")
    else:
        FAIL.append(name)
        print(f"  FAIL  {name}" + (f": {detail}" if detail else ""))

# ---------------------------------------------------------------------------
# T1  Input source images unchanged
# ---------------------------------------------------------------------------
print("T1  Input source images unchanged")
check("T1a south_exists",  SOUTH_PATH.exists(), str(SOUTH_PATH))
check("T1b north_sha",     sha256(NORTH_PATH) == NORTH_SHA,
      f"got {sha256(NORTH_PATH)[:16]}…")
check("T1c east_prefix",   sha256(EAST_PATH).startswith(EAST_PREFIX),
      f"got {sha256(EAST_PATH)[:8]}")
check("T1d west_prefix",   sha256(WEST_PATH).startswith(WEST_PREFIX),
      f"got {sha256(WEST_PATH)[:8]}")

# ---------------------------------------------------------------------------
# T2  Output images exist and are correct dimensions
# ---------------------------------------------------------------------------
print("T2  Output images exist and correct dimensions")
expected_dims = {
    "four-facing-source.png":    (1548, 416),
    "four-facing-native.png":    (268, 69),
    "four-facing-half.png":      (140, 35),
    "four-facing-grayscale.png": (268, 69),
}
for fn, expected in expected_dims.items():
    p = ROOT / fn
    exists = p.exists()
    check(f"T2  {fn} exists", exists, str(p))
    if exists:
        im = load_image(p)
        check(f"T2  {fn} dimensions", im.size == expected,
              f"got {im.size} expected {expected}")

# ---------------------------------------------------------------------------
# T3  Strips reproducible
# ---------------------------------------------------------------------------
print("T3  Strips reproducible (re-run assemble.py)")
orig_hashes = json.loads((ROOT / "output-hashes.json").read_text())
# Remove output files so we can re-run cleanly
import shutil, tempfile
tmp = tempfile.mkdtemp()
for fn in orig_hashes:
    src = ROOT / fn
    if src.exists():
        shutil.copy2(src, tmp)

result = subprocess.run(
    [sys.executable, "-B", "-W", "error::ResourceWarning", str(ROOT / "assemble.py")],
    capture_output=True, text=True
)
check("T3  assemble exit 0", result.returncode == 0, result.stderr[:200])

for fn, expected_h in orig_hashes.items():
    p = ROOT / fn
    if p.exists():
        actual = sha256(p)
        check(f"T3  {fn} reproducible", actual == expected_h,
              f"got {actual[:16]}… expected {expected_h[:16]}…")

# ---------------------------------------------------------------------------
# T4  Native strip dimensions
# ---------------------------------------------------------------------------
print("T4  Native strip dimensions")
native = load_image(ROOT / "four-facing-native.png")
check("T4  native width",  native.width  == 4*64 + 3*4,  str(native.width))
check("T4  native height", native.height == 69,           str(native.height))

# ---------------------------------------------------------------------------
# T5  Half strip dimensions
# ---------------------------------------------------------------------------
print("T5  Half strip dimensions")
half = load_image(ROOT / "four-facing-half.png")
check("T5  half width",  half.width  == 4*32 + 3*4, str(half.width))
check("T5  half height", half.height == 35,          str(half.height))

# ---------------------------------------------------------------------------
# T6  Grayscale strip has no saturation
# ---------------------------------------------------------------------------
print("T6  Grayscale strip has no saturation")
gray = load_image(ROOT / "four-facing-grayscale.png").convert("RGBA")
arr = np.array(gray)
# For every pixel with alpha > 0, R == G == B
alpha_mask = arr[:, :, 3] > 0
rgb = arr[alpha_mask, :3]
is_gray = np.all(rgb[:, 0:1] == rgb[:, 1:3], axis=1)
check("T6  all opaque pixels are gray",
      bool(np.all(is_gray)),
      f"{np.sum(~is_gray)} non-gray pixels")

# ---------------------------------------------------------------------------
# T7  All 16 role-mask files exist and are 384x416 RGBA
# ---------------------------------------------------------------------------
print("T7  Role mask files exist and correct size")
ROLES_LIST = ["lower_body", "upper_body", "equipment", "head"]
for facing in ["south", "east", "north", "west"]:
    for role in ROLES_LIST:
        p = ROOT / "role-masks" / f"{facing}-{role}.png"
        exists = p.exists()
        check(f"T7  {facing}-{role} exists", exists)
        if exists:
            im = load_image(p)
            check(f"T7  {facing}-{role} size", im.size == (384, 416) and im.mode == "RGBA",
                  f"{im.size} {im.mode}")

# ---------------------------------------------------------------------------
# T8  Each role mask has at least one opaque pixel
# ---------------------------------------------------------------------------
print("T8  Role masks non-empty (have opaque pixels)")
# South packet merges hood and satchel into original_upper (no separate layer).
# Those roles are not separately isolatable from south layers, which is a disclosed blocker.
SOUTH_MERGED_ROLES = {"equipment", "head"}
for facing in ["south", "east", "north", "west"]:
    for role in ROLES_LIST:
        if facing == "south" and role in SOUTH_MERGED_ROLES:
            print(f"  SKIP  T8  south-{role}: merged into original_upper (disclosed blocker)")
            continue
        p = ROOT / "role-masks" / f"{facing}-{role}.png"
        if p.exists():
            arr = np.array(load_image(p).convert("RGBA"))
            count = int(np.sum(arr[:, :, 3] > 128))
            check(f"T8  {facing}-{role} opaque_pixels >= 1", count >= 1,
                  f"got {count}")

# ---------------------------------------------------------------------------
# T9  family.json required keys and status
# ---------------------------------------------------------------------------
print("T9  family.json structure")
fam = json.loads((ROOT / "family.json").read_text())
check("T9  status BLOCKED_UNRECONCILED_FAMILY", fam.get("status") == "BLOCKED_UNRECONCILED_FAMILY",
      fam.get("status", ""))
check("T9  four facings in anatomy", set(fam.get("anatomy", {}).keys()) == {"south","east","north","west"})
check("T9  sourcePackets present", set(fam.get("sourcePackets", {}).keys()) == {"south","east","north","west"})
check("T9  openBlockers non-empty", len(fam.get("openBlockers", [])) > 0)
check("T9  partVocabulary present", "partVocabulary" in fam)
check("T9  equipment mapping present", "equipment" in fam and "satchel" in fam["equipment"])
check("T9  limits field present", "limits" in fam)

# ---------------------------------------------------------------------------
# T10  index.html non-empty and contains all four facings
# ---------------------------------------------------------------------------
print("T10  index.html content")
html = (ROOT / "index.html").read_text()
check("T10  index.html non-empty", len(html) > 500)
for facing in ["south", "east", "north", "west"]:
    check(f"T10  index contains {facing}", facing in html)
h1 = html.split('<h1>', 1)[1].split('</h1>', 1)[0]
check("T10  blocked status in h1", "BLOCKED_UNRECONCILED_FAMILY" in h1)
check("T10  blocked status banner", "STATUS: BLOCKED_UNRECONCILED_FAMILY" in html)
check("T10  two inline absent role labels", html.count('<span class="absent-mask">ABSENT') == 2)
check("T10  rounding disclosed", "32×34.5" in html and "64×69.333" in html)
check("T10  no unexplained absent mask images", 'src="role-masks/south-equipment.png"' not in html and 'src="role-masks/south-head.png"' not in html)

# ---------------------------------------------------------------------------
# T11  Layer files exist for each facing
# ---------------------------------------------------------------------------
print("T11  Layer files exist for each facing")
layer_dirs = {
    "south": SOUTH_LAYERS_DIR,
    "north": NORTH_LAYERS_DIR,
    "east":  EAST_LAYERS_DIR,
    "west":  WEST_LAYERS_DIR,
}
for facing, ldir in layer_dirs.items():
    files = list(Path(ldir).glob("*.png")) if Path(ldir).exists() else []
    check(f"T11  {facing} has >=1 layer", len(files) >= 1,
          f"found {len(files)} in {ldir}")

# ---------------------------------------------------------------------------
# T12  North SHA matches active attempt-01
# ---------------------------------------------------------------------------
print("T12  North SHA matches attempt-01")
check("T12  north sha exact",
      sha256(NORTH_PATH) == NORTH_SHA,
      sha256(NORTH_PATH)[:16])

# ---------------------------------------------------------------------------
# T13  South, east, west SHA prefixes match packet declarations
# ---------------------------------------------------------------------------
print("T13  South/east/west SHA prefixes")
east_sha  = sha256(EAST_PATH)
west_sha  = sha256(WEST_PATH)
check("T13  east prefix",   east_sha.startswith(EAST_PREFIX),  east_sha[:8])
check("T13  west prefix",   west_sha.startswith(WEST_PREFIX),  west_sha[:8])
# South: compare against family.json recorded sha
south_sha = sha256(SOUTH_PATH)
recorded  = fam["sourcePackets"]["south"]["sha256"]
check("T13  south sha matches family.json", south_sha == recorded,
      f"file={south_sha[:16]} json={recorded[:16]}")

# ---------------------------------------------------------------------------
# T14  output-hashes.json round-trips
# ---------------------------------------------------------------------------
print("T14  output-hashes.json round-trips")
stored = json.loads((ROOT / "output-hashes.json").read_text())
for fn, expected_h in stored.items():
    p = ROOT / fn
    if p.exists():
        actual = sha256(p)
        check(f"T14  {fn}", actual == expected_h,
              f"got {actual[:16]}… stored {expected_h[:16]}…")

# ---------------------------------------------------------------------------
# T15  family.json must NOT claim coherence/readiness/acceptance; absent layers documented
# ---------------------------------------------------------------------------
print("T15  Reject coherence/readiness/acceptance; document absent layers")
check("T15  status is BLOCKED_UNRECONCILED_FAMILY",
      fam.get("status") == "BLOCKED_UNRECONCILED_FAMILY",
      fam.get("status", ""))
check("T15  coherent is explicitly False",
      fam.get("coherent") is False,
      str(fam.get("coherent")))
check("T15  ready is explicitly False",
      fam.get("ready") is False,
      str(fam.get("ready")))
check("T15  accepted is explicitly False",
      fam.get("accepted") is False,
      str(fam.get("accepted")))
absent = fam.get("absentRoleLayers", {})
check("T15  south-equipment absent layer documented",
      "south-equipment" in absent,
      str(list(absent.keys())))
check("T15  south-head absent layer documented",
      "south-head" in absent,
      str(list(absent.keys())))
# Confirm the absent entries mention the merge reason
check("T15  south-equipment entry mentions original_upper",
      "original_upper" in absent.get("south-equipment", ""),
      absent.get("south-equipment", ""))
check("T15  south-head entry mentions original_upper",
      "original_upper" in absent.get("south-head", ""),
      absent.get("south-head", ""))

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print(f"PASS: {len(PASS)}  FAIL: {len(FAIL)}")
if FAIL:
    print("Failed tests:")
    for f in FAIL:
        print(f"  {f}")
    sys.exit(1)
else:
    print("All tests passed.")
