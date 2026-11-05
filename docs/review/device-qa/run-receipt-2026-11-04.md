# Run receipt

Read 2026-11-04 from `RunReceipt.canonical` on `fcab4e5`. No receipt field was added.

The schema string is `run-receipt-001`. Encoding is [canonical-json-2026-11-04.md](canonical-json-2026-11-04.md). The four identity strings are [replay-identity-2026-11-04.md](replay-identity-2026-11-04.md). Outcome here is `success`, `failure`, or `invalid`. The incident-report sentences are [run-card-2026-11-04.md](run-card-2026-11-04.md). The seal events are [terminal-seal-2026-11-04.md](terminal-seal-2026-11-04.md). Presentation metadata is [presentation-settings-2026-11-04.md](presentation-settings-2026-11-04.md).

`elapsedTicks` is the terminal tick when one is stored, otherwise the current tick. `finalDigest` is the terminal digest when one is stored, otherwise `digest()`. Destructions are sorted by tick, then by camera id. Selected sockets are sorted by socket id in UTF-8 order. The elite receipt id is `improper-search-daemon`. The boss receipt id is `algorithmic-moderate`.

| Key | What it holds |
| --- | --- |
| schemaVersion | `run-receipt-001` |
| identity | ruleset, content, arena, replay schema |
| seed | the run seed |
| outcome | `success`, `failure`, or `invalid` |
| elapsedTicks | terminal tick, or the current tick |
| finalDigest | terminal digest, or `digest()` |
| player | finalIntegrity, damageTaken, integrityRestored |
| exposure | final, peak, finalState (the detection raw value), lockdownEntered |
| combat | damageDealt, defeatsByArchetype |
| objectives.combatAuthority | mob complete and required, currentNode raw value, elite id and defeated, boss id, defeated, and phasesReached, complete |
| objectives.networkBlackout | camerasDestroyed, camerasTotal the literal 8, complete |
| objectives.extractionArmed | whether extraction is armed |
| cameraDestructions | cameraId, tick, housingFamily, wasDetectingPlayer, source, exposureBefore, exposureAfter, triggeredLockdown |
| camerasDamaged | summary count |
| camerasDestroyed | summary count |
| tamperExposureApplied | summary total |
| cameraObjective | destroyed, total, complete |
| upgrade | the upgrade raw value, or null |
| boss | phasesReached, defeated |
| diagnostics | the diagnostic strings |
| presentation | `PresentationReceiptMetadata.canonical` |
| cameraPlacement | version, placementSeed, selectedSockets (socketId, cameraEntityId, housingFamily) |
