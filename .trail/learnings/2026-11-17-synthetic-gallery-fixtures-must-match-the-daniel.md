---
title: Synthetic gallery fixtures must match the native producer envelope
author: Daniel
date: 2026-11-17
branch: qa/bp001-projection-decision-20261116
id: l-17d0e3d7
scope: repo
status: active
src: agent
touches:
  - ".github/workflows/ci.yml"
  - docs/handoff/NEXT.md
---

## Decided
A passing synthetic gallery check must use the actual native producer's record and assembly shape. Compare the Swift record keys and source census before interpreting synthetic loader success as integration coverage.
## Tried and ruled out
The V9 gallery expected record.supplementalSource and invented extra ordinary source roles in its synthetic fixture. The actual Swift producer emits supplementalManifestSHA256 and leaves the ordinary source census unchanged, with supplementary geometry and images bound through assembly.supplementalBinding and assembly.supplements. Both Node suites passed the invented protocol before coordinator inspection exposed the mismatch. Issue254 records the defect.
## In the code
AppTests/BlockedBaseCurbSceneTests.swift:507-515 is the record producer. docs/review/blocked-base-curb-relief-20261116/gallery/gallery.js:152-161 and gallery/test_helpers.js:25-52 contained the divergent synthetic protocol. Repair the new gallery to the exact native envelope and add native-shaped negative tests, never rewrite native evidence to satisfy a synthetic fixture. Actual imported V9 remains a separate required test.
