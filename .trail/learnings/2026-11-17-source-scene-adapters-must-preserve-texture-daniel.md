---
title: Source-scene adapters must preserve texture domains and explicit face normals
author: Daniel
date: 2026-11-17
branch: qa/bp001-projection-decision-20261116
id: l-c409d88e
scope: repo
status: active
src: agent
---

## Decided
A source-scene reconstruction must adapt the producer's explicit texture and normal conventions, not infer them from sprite bounds or vertex winding. Actual image inspection is required before declaring a comparison usable, because self-recomposition tests can faithfully reproduce the same wrong adapter.
## Tried and ruled out
Using the clipped arena node size2304x1536 as the square ground texture domain stretched paving and exposed black apron regions. The retained producer samples a2304x2304square texture and clips it to the arena. Recomputing every face normal from winding also culled context roof faces even though context geometry explicitly declares upward normals. Kiosk geometry uses winding-derived normals, so one convention cannot silently replace the other.
## In the code
AppTests/BlockedBaseCurbSceneTests.swift:308-313 defines square ground registration and tileUnits2304 over clipped arena bounds. docs/review/building-perspective-detail-20261116/context/replay.py:57-58 uses explicit face normals. docs/review/architectural-scale-20261117/source/build.py is the source-proxy adapter. REVIEW-FIRST.md and REVIEW-SECOND.md in that packet retain actual-image diagnoses, and issue255 records the independent-validation gaps. Preserve failed artifacts and keep the one geometry proposal fixed during technical renderer repairs. No aesthetic acceptance or native equivalence follows from these fixes.
