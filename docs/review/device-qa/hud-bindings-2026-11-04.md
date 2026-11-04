# HUD bindings

Read 2026-11-04 from `HUDRenderer`, `HUDLayout`, and `DetectionPresentation` on `49759ab`. No label was changed. Shapes and authored sizes stay in [hud-shapes-2026-11-03.md](hud-shapes-2026-11-03.md). Exposure bands stay in [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md).

The integrity bar is `playerIntegrity / playerMaxIntegrity`. The printed number is the integer. The fill is critical when `integrity * 4 <= maxIntegrity`. At the content maximum of 150, 37 qualifies and 38 does not.

The exposure bar is `exposure / 1000`, with notches at 200, 450, 700, and 1000. The detection label is the glyph, a space, and the uppercased state. Lockdown uses the critical colour. The others use the text colour.

| State | Glyph |
|---|---|
| `hidden` | `( )` |
| `observed` | `(-)` |
| `tracked` | `[o]` |
| `hunted` | `[#]` |
| `lockdown` | `[X]` |

The boss bar is boss integrity over its max, or 0 when the max is 0. A boss in transition uses the dim fill. The phase line is `PUBLIC SAFETY`, `CIVIL LIBERTIES`, `TEMPORARY SAFEGUARD`, or `INDEPENDENT REVIEW`.

The extraction ring is drawn only while armed. Its arc is `extractionRemaining / 300`. The number is `extractionSeconds`, which is 0 when remaining is 0 and `(remainingTicks + 59) / 60` otherwise. 300 ticks prints 5.

Objective copy is `MOB ENCOUNTER A`, `MOB ENCOUNTER B`, `MOB ENCOUNTER C`, `IMPROPER SEARCH DAEMON`, `ALGORITHMIC MODERATE`, `DEFEAT THE CURRENT AUTHORITY` while inside the locked box, or `PHOENIX STEPS OPEN` once extraction is armed. The camera line is `CAM <destroyed>/8` until all eight are destroyed, then `NETWORK BLACKOUT 8/8`. It stays hidden until a camera is damaged or destroyed. Three notches sit beside it. Index `i` is filled when `i < integrity`, so 3 fills all three, 2 fills the first two, and 1 fills the first. They persist 90 ticks after a hit.

Upgrade glyphs are `///` for Signal Jammer, `<>` for Ricochet Pulse, and `::` for Ghost Step. Terminal copy is `RUN COMPLETE`, `PLAYER DOWN`, or `RUN INVALID`.

This does not add a meter.
