# HUD anchors

Read 2026-11-04 from `HUDAnchor` on `5d954be`. No rectangle was moved.

The reference rectangles stay in [control-rects-2026-11-04.md](control-rects-2026-11-04.md) and [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The HUD scale values stay in [presentation-settings-2026-11-04.md](presentation-settings-2026-11-04.md).

`playerIntegrity`, `combatObjective`, and `cameraObjective` are top-left. `exposureBar`, `detectionLabel`, `bossIntegrity`, `tutorialCard`, and `tamperSpike` are top-centre. `upgradeBadge` is top-right. `extractionCountdown`, the stick, the dodge, and pause are centre.

A top-left rect is already the rect `HUDLayout` maps. Top-centre subtracts `width / 2` from x. Top-right subtracts `width` from x. Centre subtracts `width / 2` from x and `height / 2` from y. The division is integer division.

The stick, the dodge, and pause are controls. `HUDRenderer` maps a control with `mappedControl`. Every other element maps with the HUD scale.

This does not move a control.
