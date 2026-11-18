---
title: Only the Camera-adjacent building is the reported geometry outlier
author: Daniel
date: 2026-11-17
branch: qa/bp001-projection-decision-20261116
id: l-8a383d12
scope: repo
status: active
replaces: l-cfaf62a0
src: agent
touches:
  - FACTS.md
  - docs/handoff/NEXT.md
---

## Decided
Owner clarified at 2026-11-17T01:51UTC that only the building beside the Camera post has odd geometry and spacing relative to its neighbors. Keep surrounding buildings as unchanged visual references, not redesign targets. This narrows the earlier scene-wide interpretation because the owner explicitly distinguished this one building.
## In the code:
docs/review/architectural-scale-20261117/source/build.py: the published multi-building proposal is historical evidence, not authority to carry residential/civic changes forward. FACTS.md and docs/handoff/NEXT.md record the narrower scope. Preserve published outputs. No new aesthetic attempt or native run follows from clarification alone.
