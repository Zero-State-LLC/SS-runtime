#!/usr/bin/env python3
"""
Player neutral family assembly - slice 5
Owner authorization: 2026-11-16 05:56:35 UTC (approved ten-slice plan)
Contract IDs: BP-002, BP-007, BP-012, T1045

Assembles a common editable four-facing neutral family from the four
already-accepted source packets.  Produces:
  - family.json          common parameter/equipment model
  - four-facing-source.png   all four at 384x416
  - four-facing-native.png   all four at 64×69 (SpriteKit native)
  - four-facing-half.png     all four at 32×35
  - four-facing-grayscale.png
  - role-masks/<facing>-<role>.png   per-facing role-mask overlays
  - index.html               gallery with per-facing layer toggles

No new image generation is performed.  All inputs are read-only.
"""

import hashlib, json, os, shutil, sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow required: pip install Pillow")

ROOT = Path(__file__).parent.resolve()
REPO = ROOT.parents[2]

# ---------------------------------------------------------------------------
# Input paths - all read-only
# ---------------------------------------------------------------------------

SOUTH_PATH = REPO / "docs/review/player-baggy-south-source-20261116/south-baggy-neutral.png"
NORTH_PATH = REPO / "docs/review/player-north-source-20261116/north-neutral.png"
EAST_PATH  = REPO / "docs/review/player-side-source-20261116/east/east-neutral.png"
WEST_PATH  = REPO / "docs/review/player-side-source-20261116/west/west-neutral.png"

SOUTH_LAYERS_DIR = REPO / "docs/review/player-baggy-south-source-20261116/layers"
NORTH_LAYERS_DIR = REPO / "docs/review/player-north-source-20261116/layers"
EAST_LAYERS_DIR  = REPO / "docs/review/player-side-source-20261116/east/layers"
WEST_LAYERS_DIR  = REPO / "docs/review/player-side-source-20261116/west/layers"

SOUTH_EXT = REPO / "docs/review/player-baggy-south-source-20261116/baggy-south.json"
NORTH_EXT = REPO / "docs/review/player-north-source-20261116/north-extension.json"
EAST_EXT  = REPO / "docs/review/player-side-source-20261116/east/east-extension.json"
WEST_EXT  = REPO / "docs/review/player-side-source-20261116/west/west-extension.json"

# Pinned SHA-256 of each source image (from their own test suites)
PINNED_SHA = {
    "south": "unverified",  # resolved at runtime from baggy-south.json
    "north": "0a6e15bd2aa8cc486dd14521b60680bed6a2dd0833707972850e65d7991f4fbb",
    "east":  "4be91d1d",    # prefix - resolved at runtime
    "west":  "9d06aa54",    # prefix - resolved at runtime
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()

def load_rgba(path):
    with Image.open(path) as source:
        return source.convert("RGBA")

def to_native(img):
    """Scale 384x416 -> 64x69 (floor) using Lanczos."""
    return img.resize((64, 69), Image.LANCZOS)

def to_half(img):
    return img.resize((32, 35), Image.LANCZOS)

def to_grayscale(img):
    return ImageOps.grayscale(img).convert("RGBA")

def hstack(images, gap=4):
    w = sum(im.width for im in images) + gap * (len(images) - 1)
    h = max(im.height for im in images)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    x = 0
    for im in images:
        out.paste(im, (x, 0))
        x += im.width + gap
    return out

def layer_files(layers_dir):
    d = Path(layers_dir)
    if not d.exists():
        return []
    return sorted(f for f in d.iterdir() if f.suffix == ".png")

# ---------------------------------------------------------------------------
# Role masks
# Roles are semantic groupings of parts present in every facing.
# ---------------------------------------------------------------------------

ROLES = {
    # Note: south packet merges hood+satchel into original_upper (no separate layer).
    # The east-facing uses far_left_*/near_right_* naming; west uses far_right_*/near_left_*.
    "lower_body":   {"left_thigh", "right_thigh", "left_shin_boot", "right_shin_boot",
                     "left_shin_kneepad", "right_shin_kneepad",
                     "original_boots",
                     # east: near=right, far=left
                     "far_left_thigh", "near_right_thigh",
                     "far_left_shin_boot", "near_right_shin_boot",
                     # west: near=left, far=right
                     "far_right_thigh", "near_left_thigh",
                     "far_right_shin_boot", "near_left_shin_boot"},
    "upper_body":   {"torso_coat_equipment", "left_upper_arm", "right_upper_arm",
                     "left_forearm_hand", "right_forearm_hand",
                     "left_coat_tail", "right_coat_tail",
                     "original_upper",
                     # east: near=right, far=left
                     "far_left_upper_arm", "near_right_upper_arm",
                     "far_left_forearm_hand", "near_right_forearm_hand",
                     "far_left_coat_tail", "near_right_coat_tail",
                     # west: near=left, far=right
                     "far_right_upper_arm", "near_left_upper_arm",
                     "far_right_forearm_hand", "near_left_forearm_hand",
                     "far_right_coat_tail", "near_left_coat_tail"},
    "equipment":    {"right_satchel"},
    "head":         {"hood"},
}

def build_role_mask(layers_dir, role_parts, canvas=(384, 416)):
    """Return an RGBA image showing only the pixels belonging to role_parts."""
    mask = Image.new("RGBA", canvas, (0, 0, 0, 0))
    for f in layer_files(layers_dir):
        if f.stem in role_parts:
            layer = load_rgba(f)
            if layer.size != canvas:
                layer = layer.resize(canvas, Image.LANCZOS)
            mask = Image.alpha_composite(mask, layer)
    return mask

# ---------------------------------------------------------------------------
# Common parameter/equipment mapping
# ---------------------------------------------------------------------------

def build_family_json(south_ext_path, north_ext_path, east_ext_path, west_ext_path,
                      out_hashes):
    with open(south_ext_path) as f:
        se = json.load(f)
    with open(north_ext_path) as f:
        ne = json.load(f)
    with open(east_ext_path) as f:
        ee = json.load(f)
    with open(west_ext_path) as f:
        we = json.load(f)

    return {
        "status": "BLOCKED_UNRECONCILED_FAMILY",
        "coherent": False,
        "ready": False,
        "accepted": False,
        "absentRoleLayers": {
            "south-equipment": "hood and satchel merged into original_upper; no separate layer; role mask is empty canvas",
            "south-head":      "hood merged into original_upper; no separate layer; role mask is empty canvas",
        },
        "kind": "PARTITIONED_RECORD_OF_INDEPENDENT_GENERATED_VIEWS_NOT_COMMON_EDITABLE_MASTER",
        "coherenceWarning": (
            "The four facings are independent image_generation outputs from separate sheets. "
            "No shared anatomical model, rig, or single editable source underpins them. "
            "Hash and dimension checks do not establish anatomical continuity, costume coherence, "
            "or consistent viewpoint. The open blockers are unresolved cross-facing discrepancies."
        ),
        "sliceRef": "slice-5 of 2026-11-16 ten-slice plan",
        "ownerAuthorization": "2026-11-16 05:56:35 UTC",
        "contractIDs": ["BP-002", "BP-007", "BP-012", "T1045"],
        "canvas": [384, 416],
        "groundRoot": [192, 336],
        "logicalCanvas": [64, 69.333333],
        "logicalRoot": [32, 56],
        "facingOrder": ["south", "east", "north", "west"],
        "anatomy": {
            "south": "anatomical right on screen left; cloth patch on anatomical-left thigh (screen right)",
            "north": "anatomical right on screen right; satchel on anatomical-right hip (screen right)",
            "east":  "screen-right facing; anatomical right near (screen right); anatomical left far",
            "west":  "screen-left facing; anatomical left near (screen left); anatomical right far",
        },
        "equipment": {
            "satchel": {
                "anatomicalBind": "right_hip",
                "facingNotes": {
                    "south": "front-right hip, visible",
                    "north": "right hip, visible at back",
                    "east":  "near right hip, partially behind torso at rear edge - BLOCKER: depth unresolved",
                    "west":  "far right hip, partially occluded - BLOCKER: depth unresolved",
                }
            },
            "clothPatch": {
                "anatomicalBind": "left_thigh",
                "facingNotes": {
                    "south": "screen right thigh, visible",
                    "north": "screen left thigh (hidden side), not visible",
                    "east":  "anatomical left = far thigh, partially visible or occluded",
                    "west":  "anatomical left = near thigh, visible",
                }
            }
        },
        "partVocabulary": {
            "note": "Parts are per-facing; names beginning far_/near_ are side-facing variants.",
            "canonical_parts": sorted(ROLES["lower_body"] | ROLES["upper_body"] |
                                      ROLES["equipment"] | ROLES["head"]),
            "roles": {role: sorted(parts) for role, parts in ROLES.items()},
        },
        "sourcePackets": {
            "south": {
                "path": "docs/review/player-baggy-south-source-20261116",
                "image": "south-baggy-neutral.png",
                "sha256": out_hashes["south"],
                "layersDir": "layers",
            },
            "north": {
                "path": "docs/review/player-north-source-20261116",
                "image": "north-neutral.png",
                "sha256": out_hashes["north"],
                "layersDir": "layers",
                "activeAttempt": "attempts/01-uniform-0.4",
            },
            "east": {
                "path": "docs/review/player-side-source-20261116/east",
                "image": "east-neutral.png",
                "sha256": out_hashes["east"],
                "layersDir": "layers",
            },
            "west": {
                "path": "docs/review/player-side-source-20261116/west",
                "image": "west-neutral.png",
                "sha256": out_hashes["west"],
                "layersDir": "layers",
            },
        },
        "openBlockers": [
            "Satchel depth placement differs between south (front-hip) and north/east/west (rear-hip). Not resolved; tests do not assert it.",
            "Coat tails generated broader and flatter on north/east/west than south. Not reconciled.",
            "Camera elevation: side views appear closer to eye level than south. Not proven.",
            "Baggy-south trouser shins 5-7 px narrower than north reference at row 295. Trade-off deferred.",
            "Shin and boot are one part on all non-south facings; no independent boot control.",
            "No joint-range, contact, heel/toe, native renderer, simulator, live-cadence or device verification.",
            "These generated facings are not original master paint. Hidden surfaces are generated proposals.",
        ],
        "limits": "PROPOSED source samples only. No production admission, animation, native-render, shipping or pin change authorized.",
    }

# ---------------------------------------------------------------------------
# HTML gallery
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Player neutral facing record - BLOCKED_UNRECONCILED_FAMILY - {date}</title>
<style>
body {{ font-family: monospace; background: #1a1a2e; color: #eee; padding: 16px; }}
h1 {{ color: #e94560; }}
.blocked {{ background: #7a0000; color: #ffc; padding: 10px 14px; border-radius: 4px; margin-bottom: 16px; font-size: 13px; line-height: 1.6; }}
.section {{ margin-bottom: 32px; }}
h2 {{ color: #aaa; background: #16213e; padding: 6px 10px; }}
.strip-container {{ overflow-x: auto; }}
img.strip {{ image-rendering: pixelated; display: block; margin: 8px 0; }}
.facing-block {{ display: inline-block; vertical-align: top; margin-right: 24px; }}
.facing-block h3 {{ margin: 4px 0; color: #e94560; }}
.layer-controls {{ margin: 4px 0; }}
.layer-controls label {{ display: block; cursor: pointer; font-size: 12px; }}
.layer-controls input {{ margin-right: 4px; }}
canvas.facing {{ image-rendering: pixelated; display: block; }}
.blocker {{ background: #2d1b00; border-left: 3px solid #f90; padding: 6px 10px; margin: 4px 0; font-size: 12px; }}
.absent-mask {{ background: #111; border: 1px solid #555; color: #888; font-size: 10px; padding: 4px 6px; display: inline-block; vertical-align: bottom; width: 96px; height: 104px; box-sizing: border-box; }}
.note {{ font-size: 11px; color: #aaa; margin: 2px 0 6px 0; }}
</style>
</head>
<body>
<h1>Player neutral facing record - BLOCKED_UNRECONCILED_FAMILY - {date}</h1>
<div class="blocked">
  <strong>STATUS: BLOCKED_UNRECONCILED_FAMILY</strong> &nbsp;|&nbsp; coherent=false &nbsp; ready=false &nbsp; accepted=false<br>
  Four independently generated views from separate sheets. No shared anatomical model, rig, or single editable source.
  Hash and dimension checks do not establish anatomical continuity, costume coherence, or consistent viewpoint.
  The intended slice-5 goal (a genuinely coherent editable family) is <strong>NOT completed</strong> by this record.
  No production admission, animation, native-render, or shipping authorized.
</div>

<div class="section">
<h2>Four-facing strip (source 384×416)</h2>
<div class="strip-container">
<img class="strip" src="four-facing-source.png" alt="four-facing source">
</div>
<p>Panels left to right: south (baggy proposal), east, north (attempt 01 baggy), west. Original south (slim legs, unchanged) not shown; see individual packets.</p>
</div>

<div class="section">
<h2>Native (64×69 px) - logical canvas 64×69.333 rounded down; not exact 50%</h2>
<p class="note">Logical canvas is 64×69.333 CSS px. PNG scaled to 64×69 (floor). Strip is 268 px wide (4×64 + 3×4 gap). Not exact 50% of source.</p>
<img class="strip" src="four-facing-native.png" alt="four-facing native" style="width:{native_w}px;height:{native_h}px;">
</div>

<div class="section">
<h2>Half (32×35 px) - 32×34.5 rounded up; not exact 50% of native</h2>
<p class="note">Half of 64×69 is 32×34.5. PNG is 32×35 (ceil). Not exact 50% of native.</p>
<img class="strip" src="four-facing-half.png" alt="four-facing half" style="width:{half_w}px;height:{half_h}px;">
</div>

<div class="section">
<h2>Grayscale (64×69 px, same rounding as native)</h2>
<img class="strip" src="four-facing-grayscale.png" alt="four-facing grayscale" style="width:{native_w}px;height:{native_h}px;">
</div>

<div class="section">
<h2>Role masks (source 384×416) - per facing</h2>
<p>South <em>equipment</em> and <em>head</em> masks are <strong>absent</strong>: those layers are merged into original_upper in the south packet and cannot be isolated without source repair. All other masks have opaque pixels.</p>
{role_mask_html}
</div>

<div class="section">
<h2>Per-facing layer toggles (source size)</h2>
{layer_toggle_html}
</div>

<div class="section">
<h2>Open blockers</h2>
{blocker_html}
</div>

<script>
{toggle_js}
</script>
</body>
</html>
"""

ABSENT_MASKS = {("south", "equipment"), ("south", "head")}

def build_html(facing_layers, role_mask_names, blockers, date):
    # Role masks section - absent masks shown as labelled placeholder, not silent empty image
    role_mask_html = ""
    for facing in ["south", "east", "north", "west"]:
        role_mask_html += f'<div class="facing-block"><h3>{facing}</h3>\n'
        for role in ROLES:
            fn = f"role-masks/{facing}-{role}.png"
            if (facing, role) in ABSENT_MASKS:
                role_mask_html += (
                    f'<div>{role}: '
                    f'<span class="absent-mask">ABSENT<br>{role}<br>merged into<br>original_upper;<br>source repair<br>required</span>'
                    f'</div>\n'
                )
            else:
                role_mask_html += f'<div>{role}: <img src="{fn}" alt="{facing} {role}" style="height:104px;image-rendering:pixelated;vertical-align:bottom;border:1px solid #333;"></div>\n'
        role_mask_html += "</div>\n"

    # Layer toggle section
    layer_toggle_html = ""
    toggle_js_parts = []

    for facing, layers in facing_layers.items():
        bid = f"facing_{facing}"
        layer_toggle_html += f'<div class="facing-block"><h3>{facing}</h3>\n'
        layer_toggle_html += f'<canvas class="facing" id="canvas_{facing}" width="384" height="416" style="width:192px;height:208px;border:1px solid #333;"></canvas>\n'
        layer_toggle_html += '<div class="layer-controls">\n'
        for lname in layers:
            cid = f"chk_{facing}_{lname}"
            label = lname.replace("_", " ")
            layer_toggle_html += f'<label><input type="checkbox" id="{cid}" checked onchange="redraw_{facing}()"> {label}</label>\n'
        layer_toggle_html += "</div></div>\n"

        # JS for this facing
        layer_paths = [f"../../{facing_layer_path(facing, lname)}" for lname in layers]
        js = f"""
var imgs_{facing} = {{}};
var loaded_{facing} = 0;
var total_{facing} = {len(layers)};
var order_{facing} = {json.dumps(layers)};
(function() {{
  var paths = {json.dumps(layer_paths)};
  var names = {json.dumps(layers)};
  for (var i = 0; i < names.length; i++) {{
    (function(n, p) {{
      var img = new Image();
      img.onload = function() {{ imgs_{facing}[n] = img; loaded_{facing}++; if (loaded_{facing} === total_{facing}) redraw_{facing}(); }};
      img.src = p;
    }})(names[i], paths[i]);
  }}
}})();
function redraw_{facing}() {{
  var canvas = document.getElementById('canvas_{facing}');
  var ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, 384, 416);
  for (var i = 0; i < order_{facing}.length; i++) {{
    var n = order_{facing}[i];
    var chk = document.getElementById('chk_{facing}_' + n);
    if (chk && chk.checked && imgs_{facing}[n]) {{
      ctx.drawImage(imgs_{facing}[n], 0, 0);
    }}
  }}
}}
"""
        toggle_js_parts.append(js)

    # Blockers
    blocker_html = "\n".join(f'<div class="blocker">{b}</div>' for b in blockers)

    # native strip dimensions: 4 facings x 64 wide + 3 gaps of 4 = 268 wide, 69 tall
    native_w = 4 * 64 + 3 * 4
    native_h = 69
    half_w = 4 * 32 + 3 * 4
    half_h = 35

    return HTML_TEMPLATE.format(
        date=date,
        native_w=native_w, native_h=native_h,
        half_w=half_w, half_h=half_h,
        role_mask_html=role_mask_html,
        layer_toggle_html=layer_toggle_html,
        toggle_js="\n".join(toggle_js_parts),
        blocker_html=blocker_html,
    )

def facing_layer_path(facing, lname):
    """Return the relative path from docs/review to the layer file."""
    dirs = {
        "south": "player-baggy-south-source-20261116/layers",
        "north": "player-north-source-20261116/layers",
        "east":  "player-side-source-20261116/east/layers",
        "west":  "player-side-source-20261116/west/layers",
    }
    return f"review/{dirs[facing]}/{lname}.png"

def layer_names_for_facing(layers_dir):
    return [f.stem for f in sorted(Path(layers_dir).glob("*.png"))]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Player neutral family assembly - slice 5 - PROPOSED")

    out = ROOT
    masks_dir = out / "role-masks"
    masks_dir.mkdir(exist_ok=True)

    # --- Load images ---
    print("Loading source images...")
    south = load_rgba(SOUTH_PATH)
    north = load_rgba(NORTH_PATH)
    east  = load_rgba(EAST_PATH)
    west  = load_rgba(WEST_PATH)

    hashes = {
        "south": sha256(SOUTH_PATH),
        "north": sha256(NORTH_PATH),
        "east":  sha256(EAST_PATH),
        "west":  sha256(WEST_PATH),
    }
    print("Input SHA-256:")
    for k, v in hashes.items():
        print(f"  {k}: {v[:16]}...")

    # --- Four-facing strips ---
    print("Building four-facing strips...")
    # Order: south, east, north, west
    order = [south, east, north, west]

    source_strip = hstack(order, gap=4)
    source_strip.save(out / "four-facing-source.png")
    print(f"  four-facing-source.png: {source_strip.size}")

    native_imgs = [to_native(im) for im in order]
    hstack(native_imgs, gap=4).save(out / "four-facing-native.png")
    print("  four-facing-native.png")

    half_imgs = [to_half(im) for im in order]
    hstack(half_imgs, gap=4).save(out / "four-facing-half.png")
    print("  four-facing-half.png")

    gray_imgs = [to_grayscale(to_native(im)) for im in order]
    hstack(gray_imgs, gap=4).save(out / "four-facing-grayscale.png")
    print("  four-facing-grayscale.png")

    # --- Role masks ---
    print("Building role masks...")
    facing_layers_dirs = {
        "south": SOUTH_LAYERS_DIR,
        "north": NORTH_LAYERS_DIR,
        "east":  EAST_LAYERS_DIR,
        "west":  WEST_LAYERS_DIR,
    }
    for facing, ldir in facing_layers_dirs.items():
        for role, parts in ROLES.items():
            mask = build_role_mask(ldir, parts)
            mask.save(masks_dir / f"{facing}-{role}.png")
            print(f"  role-masks/{facing}-{role}.png")

    # --- family.json ---
    print("Building family.json...")
    fam = build_family_json(SOUTH_EXT, NORTH_EXT, EAST_EXT, WEST_EXT, hashes)
    (out / "family.json").write_text(json.dumps(fam, indent=2))
    print("  family.json")

    # --- index.html ---
    print("Building index.html...")
    facing_layers_map = {
        facing: layer_names_for_facing(ldir)
        for facing, ldir in facing_layers_dirs.items()
    }
    html = build_html(
        facing_layers_map,
        role_mask_names=[f"{f}-{r}" for f in ["south","east","north","west"] for r in ROLES],
        blockers=fam["openBlockers"],
        date="2026-11-16",
    )
    (out / "index.html").write_text(html)
    print("  index.html")

    # --- Output hashes ---
    out_files = [
        "four-facing-source.png",
        "four-facing-native.png",
        "four-facing-half.png",
        "four-facing-grayscale.png",
        "family.json",
    ]
    out_hashes = {}
    for fn in out_files:
        h = sha256(out / fn)
        out_hashes[fn] = h
        print(f"  {fn}: {h[:16]}...")

    (out / "output-hashes.json").write_text(json.dumps(out_hashes, indent=2))
    print("Assembly complete. Run test_family.py to verify.")

if __name__ == "__main__":
    main()
