# Architectural proportion decision aid

**One initial proposal, awaiting owner review. Not accepted art, not native evidence.** BP-001/007/012, T1045. Owner approved the comparison on November17,2026 at01:18:40UTC.

Open `gallery/index.html` from the repository HTTP server. It shows the full original benchmark, the unchanged V9 native context, then current/proposed untextured source views at1.00,1.25 and1.40. No controls or toggles are needed to see all six views.

## What this proposal changes

These are source/world units, not measured real-world dimensions. The retained Player's root-to-alpha-top is49.5units and total alpha span53.3333units. That is a visual reference, not physical stature or collision geometry. Values below are the single design fixed before rendering, also recorded in `source/DESIGN.md`.

| Source feature | Current | Proposed | Reason to compare |
| --- | ---: | ---: | --- |
| Kiosk top |132|104|Reduce one-story facade/roof mass relative to Player |
| Kiosk recessed roof |125|100|Reduce parapet height7to4 |
| Kiosk entry recess vertical span |27.1163to92.7752|18to80|Clearance65.6589to62, about1.33to1.25Player visual heights |
| Kiosk cornice/frieze zone |107.7829to132|94to104|Reduce24.2171-unit top band to10 |
| Both residential shells |112|150|Separate two-story scale from kiosk scale |
| Residential story pitch |46|66|Current pitch is shorter than Player visual height, proposed is about1.33times it |
| Residential glazing height |35|40|Rebalance openings within taller stories |
| Residential coping / chimney top |121 /136|157 /172|Carry roof components with revised facade |
| Civic west shell |142|120|Reduce dominant tall facade |
| Civic west glazing |96|64|Reduce opening height relative to Player |
| Civic coping / lantern top |151 /156|127 /134|Rebalance roof profile |
| Civic dais platform / rail top |13 /34|9 /35|Separate platform thickness from low rail height |

All XY mesh coordinates, authoritative envelopes, plan depth and actor/prop registrations remain fixed. Kiosk footprint stays128x128, chamfer39 and recess depth8.2. This is piecewise Z reauthoring at named subdivisions, not an image-space resize or a global building scale factor. See generated source geometry and dimension evidence under `source/output/`.

## What it cannot conclude

- The context residences and civic source have no explicit doorways. Their doorway clearance cannot be measured or certified by this comparison. The dais has no story/window/door semantics.
- Current and proposed are source-scene reconstructions with the same renderer, not pixel-identical native captures. Native filtering, field raster styling, shadows and blending are not certified. Runtime controls/HUD are unchanged but are not drawn in the source proxy. Untouched V9 is shown separately to prevent that confusion.
- The kiosk's existing raster roof ventilator is not mesh geometry and is omitted in both untextured arms. That omission is not approval to remove it from final art.
- Existing footprint/contact defects, perspective/material fidelity, the retained Player silhouette and physical-device behavior are not solved by passing geometric checks.
- No aesthetic retry, texture/detail pass or new native run is authorized by this packet. Any change to footprints, Camera or Player authority needs a separate decision.

## Evidence and review

- `source/DESIGN.md`: proposal fixed before first render, including extraction and adaptation decisions.
- `source/DIMENSIONS.md` and `source/massing-measurements.json`: all feature dimensions, Player-relative ratios, complete Z maps, unchanged plan depths, roof areas and qualified cornice-volume measures.
- `source/`: reproducible geometry implementation and tests.
- `REVIEW.md`: coordinator's actual image inspection, not test-derived aesthetic acceptance.
- `VALIDATION.md`: executed commands, observed checks and remaining limits.
- `CONTRACT.md`: approval, scope, preservation and next review gate.
- `protected-files.json` / `audit.py`:11432prior tracked files protected byte-for-byte, excluding only the approved intent and live handoff.

**Next gate:** owner reviews the massing direction before any detailed materials or final textured native comparison. No production admission, merge, issue closure, motion/encounter expansion or physical-device certification.
