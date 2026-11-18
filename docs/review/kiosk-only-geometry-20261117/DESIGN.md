# Kiosk-only geometry comparison design

BP-001/007/012, T1045. Owner execution directive 2026-11-17T01:55:50Z and explicit kiosk-only work order. This isolated review packet is not production artwork, acceptance, or native integration.

## Measured cause and bounded choice, before rendering

The current kiosk is 128 by 128 in plan, height132, roof deck125, parapet7. Its cornice zone107.7829457364341..132 is24.2170542635659 high, almost half the unchanged Player root-to-alpha-top reference49.5. Entry threshold27.116279069767447 is above the retained18-high blocked-base supplement by9.116279069767447. Entry head92.77519379844962 gives65.65891472868218 clearance. Neighbor shell heights112/112/142 and dais34 remain exact, not the earlier proposal's taller residences or shorter civic building.

Reuse only the existing kiosk candidate's explicit sixteen Z anchors: top104, roof100, parapet4, cornice94..104, entry18..80. This directly reduces the oversized vertical crown and aligns the visual threshold with the existing base without uniform sprite scaling or changes to XY. It is a bounded hypothesis, not proof that height explains all odd spacing. No new horizontal subdivisions, new topology, altered material classes or arbitrary second percentage are added. Existing relief/recess depths, contact contour including chamfer39, authoritative128x128 envelope and world root remain unchanged.

Camera root[496,672] is16 units west of the blocked rectangle. Player root[736,654] is96 units east. The north residence and kiosk touch at one authoritative envelope corner[512,768]. These relationships cannot be repaired by changing Z and remain explicitly unresolved. The chamfer's missing rectangle corner remains a virtual authority corner, not a visible ground vertex. Entry is a blocked visual aperture, not traversable gameplay.

## Exact reference preservation

Import hash-pinned `architectural-scale-20261117/source/build.py` for current mesh extraction, proven flat kiosk rasterization, square-ground UV mapping, field projection and registered-layer composition. Do not invoke its scene-wide proposed() or dimensions() functions. Reuse V9's four original textured neighbor PNGs and exact registrations in both comparison arms, retaining full current neighbor geometry in the editable JSON. No neighbor recoloring or rerasterization. Keep all actor/prop/supplement layers identical, full authoritative depth order/constraints, ground, center[684,724], canvas2112x978 and zooms1/1.25/1.4.

Both arms replace only the kiosk with an untextured mesh proxy to isolate geometry. Show the full original benchmark and untouched V9 native at each zoom as separate reference panes. Never composite onto a native screenshot. Explicit limitations: Pillow sampling instead of SpriteKit, native shadow/HUD/touch controls and raster kiosk roof vent omitted, field raster approximated. Geometry authority and native fidelity are separate claims.

## Validation and failure policy

Save editable original/proposed geometry, explicit Z map, measured dimension/spacing diff, source hashes, retained layer hashes and comparison PNGs. Validate all neighbor dictionaries byte-canonically, all kiosk non-Z fields, XY/contact/footprint equality, actor/ground/depth equality and full-image changed-pixel containment within the union of kiosk silhouettes. Independently reconstruct the scene from frozen inputs. Mutation checks must reject neighbor, XY, Z-map and authority changes. Preserve logs of every actual failure. Output directories fail closed rather than overwrite. Coordinator reviews actual images and decides further work. No commit, paid calls, simulator work or shared-file edits.
