---
title: Review architectural proportions before adding more facade detail
author: Daniel
date: 2026-11-17
branch: qa/bp001-projection-decision-20261116
id: l-cfaf62a0
scope: repo
status: active
src: agent
touches:
  - FACTS.md
  - docs/handoff/NEXT.md
---

## Decided
Owner flagged the Camera-fronted V9 building as awkwardly sized, as an example. Treat that as a scale/proportion concern across visible frontage, not another curb-material problem. Propose a simple untextured massing comparison against unchanged Player and Camera references before detail work. Owner did not prescribe a uniform resize direction or percentage.
## Tried and ruled out
The V9 base/curb pass preserved the architectural sources and therefore could not establish coherent doorway, story, facade and roof proportions. Its successful correspondence checks are not architectural-scale acceptance. Uniformly scaling the current kiosk image would invalidate its fixed ground registration.
## In the code
FACTS.md records the November17 correction. intent/2026-11-17-architectural-scale-review.md is a draft awaiting approval, not execution authority. docs/review/building-perspective-detail-20261116/kiosk/baseline_renderer.py:17-26 fixes the kiosk128x128 footprint and projection. docs/review/building-perspective-detail-20261116/scene/native.py:100-132 checks ground correspondence, not believable architectural proportions. Preserve Camera/Player and collision authority unless separately approved.
