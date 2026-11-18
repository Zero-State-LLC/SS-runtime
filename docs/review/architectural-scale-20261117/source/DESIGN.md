# Source implementation design, fixed before initial render

BP-001/007/012, T1045. One initial proposal only. This directory is source-only and does not grant acceptance, production admission, or native execution.

## Concrete proposal

Retained Player source root-to-alpha-top is 49.5 world units, full alpha span 53.3333. These are visual reference measurements, not physical stature or collision dimensions.

- Kiosk: top 132 to 104, recessed roof 125 to 100, entry recessed span 27.116279..92.775194 to 18..80 (clearance 65.658915 to 62). Cornice/frieze zone 107.782946..132 to 94..104. Roof parapet height 7 to 4. Preserve XY chamfer39, footprint128x128 and recess8.2.
- Both residences: shell112 to150, floor pitch46 to66, glazing35 to40, coping121 to157, chimney136 to172. Existing sources have no explicit doorway, so do not invent a measured clearance.
- Civic west: shell142 to120, glazing96 to64, coping151 to127, lantern156 to134. Existing source has no explicit doorway. Keep that limitation visible.
- Civic dais: platform13 to9, rail top34 to35. Not a building with stories/windows/doors.
- Preserve every XY mesh coordinate, contact contour, authority envelope, world root, recess/plan depth, actor/prop transform, field input, framing and depth item. Reauthor Z at explicit subdivision anchors, never uniformly rescale a sprite.

## Extraction and reconstruction

Read kiosk/output/mesh.json and context/geometry.json as exact current geometry. Persist full current and proposed face/vertex representations and every Z mapping. Flat material classes expose glazing, entry, cornices and roof, with no texture sampling or new detailing. Existing geometric relief remains. The kiosk raster roof vent is not a mesh and is omitted in both untextured arms, explicitly, not misrepresented as geometry.

Reconstruct ground from V9's ground-plan image and recorded ground witness. Recompose unchanged Player/Camera/props and V9 supplements by retained registered source layers, using the exact imported depth_order oracle on the complete V9 depthItems. Require its order and constraints to equal V9. Never use a native scene capture as a compositing substrate. Unknown offscreen actor rectangles must be proven outside every crop.

Camera field geometry is reconstructed from recorded origin, heading, angle, range and solids using the existing field-path algorithm. Native field raster style, runtime shadow rendering, filtering and blend behavior cannot be byte-proven. Therefore both arms are visibly labeled SOURCE PROXY, NOT NATIVE. Field authority is retained, not tuned to fit art. Show the untouched V9 native capture separately alongside the original full uncropped benchmark and both untextured arms. The Player and Camera images/transforms are identical across arms, with image hashes and layer equality checks.

## Reuse decisions

ADAPT: kiosk/baseline_renderer.py registration and coefficients, kiosk/replay.py:100-137 triangle depth rendering, context/replay.py projection and per-face depth, App/CameraFieldGeometry.swift:22-72 field path clipping. Exact input file hashes are recorded in output/manifest.json. Import unchanged docs/review/scene-qa-repair-20261116/native.py:266-298 for authoritative world-footprint depth ordering. No legacy source is admitted to production.

No aesthetic rerender. Technical failures must remain in source logs before a corrected run. Coordinator owns gallery, publication, independent visual review and handoff.
