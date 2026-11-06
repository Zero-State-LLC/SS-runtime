# The destruction totals

Read 2026-11-05 from `CameraDestructionReceiptSummary.project` on `ef68565`. No spike was added. The camera line stays in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md).

Damaged is the count of cameras whose integrity is above 0 and below 3. Destroyed is `destructions.count`. Tamper is the sum, over those records, of `max(0, exposureAfter - exposureBefore)`. Objective destroyed is that same destroyed count. Objective total is `HUDLayout.cameraObjectiveTotal`. Objective complete is `networkBlackout`.

This does not emit an event.
