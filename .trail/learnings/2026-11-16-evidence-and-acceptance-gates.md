---
title: Separate technical evidence from visual acceptance and native provenance
author: Jcode
date: 2026-11-16
branch: qa/bp001-projection-decision-20261116
id: l-evidence-gates-20261116
scope: repo
status: active
src: agent
touches:
  - "docs/review/"
  - "AppTests/"
---

## Decided
- Source editability, byte-identical replay and passing tests do not establish visual fidelity, owner acceptance or production admission. Keep these verdicts separate. Read docs/handoff/NEXT.md for the current authorized scope.
- The November 16 bounded Player, Camera and stone repairs exhausted their allowed previews and remain NOT RECOMMENDED. Do not perform a third same-method attempt, lower the benchmark, or integrate rejected art to unblock a scene. A materially different source method needs owner authorization. Motion and encounter expansion still need owner scene approval.
- Verify actual native evidence, not just XCTest success: loaded binary provenance, nonzero expected cases, screenshot orientation and content, actual interactions, and explicit limits on physical-device/VoiceOver/full-game claims.
- Keep #237, #239, #240 and #241 distinct. A corrected deterministic control does not fix the live #237 playback failure. Do not resume unfiltered local Swift runs after the two recorded 600-second failures.

## Tried and ruled out
- Upgrade interaction tests passed while app.screenshot() produced cropped/misoriented landscape screenshots. XCUIScreen.main.screenshot() corrected capture without changing production UI or interaction assertions. Preserve raw orientation metadata and both attempts (#243).
- An encounter run passed while loading an older simulator test bundle. A dedicated simulator restart yielded corrected v2 evidence with matching loaded-binary hash (#241). The underlying stale-path mechanism remains unproven.
- Technical Camera/stone source tests passed despite coordinator visual rejection. Reproducibility is not a substitute for benchmark review.

## Evidence
- docs/handoff/NEXT.md
- docs/review/upgrade-interaction-20261116/README.md
- docs/review/camera-surface-authored-20261116/COORDINATOR-REVIEW.md
- docs/review/stone-surface-authored-20261116/COORDINATOR-VERDICT.md
- docs/review/playback237-diagnosis-20261116/
