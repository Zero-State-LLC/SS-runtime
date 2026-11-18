---
title: Registered corners do not establish coherent visible footprints
author: Daniel
date: 2026-11-16
branch: qa/bp001-projection-decision-20261116
id: l-32ae8bd6
scope: repo
status: active
src: agent
---

## Decided
- Distinguish authoritative blocked envelopes, actual mesh contact contours and virtual corners. Corner projection checks cannot establish visible architectural contact, setbacks, pavement relationships or prop clearance. This is an owner correction, not an optional aesthetic shortcut.
- Author building foundations, sidewalk/curb/road regions and decorative prop roots from one shared plan. Independently authored ground can put painted road under a building, while a registered prop can still sit inside it.
## Tried and ruled out
- docs/review/building-perspective-detail-20261116/scene/native.py validates registered corners, including a virtual omitted kiosk chamfer corner. Treating that algebra as coherent visible bases missed the road overlap and interior tree demonstrated by docs/review/footprint-consistency-20261116/diagnose.py.
- Another building-only sprite resize cannot repair a conflicting ground/prop layout. The owner must authorize widening a frozen presentation scope before those layers change.
## Watch out
- Source-plan semantic validation and actual native visible-contact inspection are both needed. An unobserved raster contact must remain unknown, not inferred from a canvas rectangle. A conservative crop census may prove that a canvas is outside the retained view, but does not certify its geometry.
- In the code: AppTests/BuildingPerspectiveSceneTests.swift measures registration. docs/review/footprint-ground-repair-20261116/verify_preservation.py separately checks historical bytes and conservative building crop membership. Do not rewrite old capture evidence to hide defects.
