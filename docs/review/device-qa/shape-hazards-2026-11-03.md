# Shape hazards the renderer already draws

Read 2026-11-03 from `WorldRenderer` on `c700b82`. No color, width, or fill was changed. Runtime `#167` stays unmerged. The D-121 widths of 2 and 4 are not adopted. T1060 stays open because the mine fill is not clear.

## Projectiles

`renderProjectiles` builds an `SKShapeNode` circle whose radius is the projectile's radius. The stroke is clear. The fill is `Palette.playerProjectile` `SKColor(red: 1, green: 0.94, blue: 0.78, alpha: 1)` or `Palette.hostileProjectile` `SKColor(red: 0.95, green: 0.45, blue: 0.30, alpha: 1)`.

The trail is a line from the previous position to the current position. Its line width is the same radius. The trail colors are the same RGB at alpha 0.35 for the player and 0.30 for a hostile shot.

The player shot radius set in `Targeting.projectileRadius` is 4. The Witch shot radius in `combat-content-009` is 6. `narrowTailoring` and `independentReview` use radius 7. `safetyRationale` and `temporaryOrder` are not these filled circles.

## Mines

`renderMines` builds a filled circle of the mine's radius. The Vendor mine radius in `combat-content-009` is 42. The fill is `Palette.mineArmed` `SKColor(red: 0.85, green: 0.35, blue: 0.25, alpha: 0.35)` when armed, and `Palette.mineArming` `SKColor(white: 0.6, alpha: 0.15)` while arming. The stroke is `Palette.mineStroke` `SKColor(red: 0.9, green: 0.5, blue: 0.35, alpha: 0.8)`. The line width is 3 when armed and 1 while arming.

## Telegraphs

`renderTelegraphs` draws a cone, a lane, or an emitter field from the snapshot. It does not sample a telegraph PNG. The stroke is `Palette.telegraphStroke` `SKColor(red: 0.95, green: 0.55, blue: 0.35, alpha: 0.9)`. The line width is 4 when locked and 2 otherwise. `Palette.telegraphFill` uses alpha 0.42 when locked, and `0.10 + 0.22 * progress` otherwise.
