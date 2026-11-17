# Native validation, 2026-11-17 03:16 UTC

Focused `test-without-building` completed with exit65. Actual `tests-0314-summary.json` reports **8 total, 7 passed, 1 failed, 0 skipped**. Preserve `tests-0314.xcresult` and raw log. This is not a passing integration qualification.

The sole failure is `testLiveSceneToggleAndLegalMovementKeepSimulationParity` at the final whole-snapshot equality. All120 per-tick state-digest assertions passed. Exact failure-text comparison isolates array order in `spawnSockets`, with identical socket members. Set display order also differs but does not change Set equality.

Cause: `Sources/SurveillanceCore/Presentation/PresentationSnapshot.swift:333-338` flattens `enemySpawnSockets.values`, relying on unordered Dictionary iteration. Independently initialized sessions can therefore produce unequal presentation snapshots despite equal simulation digests. `App/WorldRenderer.swift:1152-1164` also assigns socket node IDs from enumeration indexes. No assertion, fixture or implementation has been patched to force green. Coordinator notified to open defect issue and assign bounded core repair separately.

Simulator slot released to coordinator at03:16UTC. Do not launch another test or simulator job without a new grant.

Debug final build succeeded. Release build succeeded and preceding background task confirmed review symbols/launch strings absent. Host focused `swift test` log reports8tests in3suites passed. These do not erase the native failure.

Exact current/candidate launch commands and app/resource paths are in README.md under 'Next actual playable comparison'. Framing uses the ordinary live camera and existing legal-command `-SSAutopilot run`, not V9 fixed-framing or a seeded shortcut. Capture full screen with review status, record actual tick, and disclose that independently timed screenshots are not pixel-equivalent comparisons. No actual playable screenshots yet produced by this worker.

No art acceptance, production admission, full gameplay qualification or physical-device claim.
