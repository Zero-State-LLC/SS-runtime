# Standard enemy stats

Read 2026-11-04 from `combat-content-009` on `49759ab`. No stat was changed. Sprite bounds stay in the sprite notes. Speeds are units per second. `Steering.speedQ8` converts one with a half-away multiply by the Q8 scale, divided by 60.

| Archetype | HP | Radius | Speed | Contact |
|---|---|---|---|---|
| `fogAnalyticsCloud` | 30 | 18 | 84 | 4 |
| `cableCarCorrelator` | 60 | 20 | 108 | 12 |
| `sutroSignalWitch` | 45 | 18 | 72 | 6 |
| `autonomousInformant` | 30 | 16 | 144 | 8 |
| `victorianVendor` | 90 | 22 | 60 | 10 |

Fog pulse: first 120, cooldown 180, telegraph 45, range 220, exposure 20.

Cable charge: first 90, cooldown 180, telegraph 30, 24 ticks at speed 300, recover 45.

Witch range is 220 to 300. The shot is first 60, cooldown 120, telegraph 30, speed 360, radius 6, lifetime 90, damage 10.

The informant has no pulse, charge, shot, or mine.

Vendor range is 160 to 220. The mine is first 90, cooldown 180, telegraph 36, maximum 2, arm 30, lifetime 240, radius 42, damage 12. The drawn mine stays the filled disc in [shape-hazards-2026-11-03.md](shape-hazards-2026-11-03.md). Runtime `#167` stays unmerged. T1060 stays open.

The first special tick from a spawn is the same `first` value: fog 120, cable 90, witch 60, vendor 90. An informant has no special tick.

This does not add an enemy.
