---
title: Loop native controls explicitly and load hidden-tab images without decode
author: Daniel
date: 2026-11-16
branch: qa/bp001-projection-decision-20261116
id: l-a74f2dbc
scope: repo
status: active
src: agent
touches:
  - ".github/workflows/ci.yml"
---

## Decided
- A looped fixed-time control must wrap its tick offset by the authored cycle duration before calling ClipTiming.frameIndex. That selector clamps by design. Native evidence must independently check multi-cycle selections, not merely report that XCTest passed.
- Source gallery readiness uses image load/error events rather than awaiting decode in an unfocused tab. In actual Brave, decode remained pending after PNGs loaded and timed out the verification. A load-event preloader with generation tokens passed all38 paired selections and228 size/grayscale checks.
## Tried and ruled out
- Unwrapped frameIndex in AppTests/PlayerGroundContactNativeTests.swift froze900 of1200 fixed-time records in the first native run. Its policy comparison is invalid and is tracked separately as runtime#238, not#237.
## In the code:
- AppTests/PlayerGroundContactNativeTests.swift
- docs/review/player-ground-contact-20261116/build_native_gallery.py
- docs/review/player-ground-contact-20261116/test_native_gallery.js
