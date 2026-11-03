# World layer order

Read 2026-11-03 from the runtime sources on `241c167`. No z position was changed.

`GameScene` sets `ignoresSiblingOrder` on the view. Siblings draw by `zPosition`. A tie is undefined.

`WorldRenderer` makes one child of its root for each `Layer` case. The child's `zPosition` is the case's raw value.

| Layer | z |
|---|---:|
| `ground` | 0 |
| `decorations` | 1 |
| `fogLow` | 2 |
| `solids` | 3 |
| `cameraHousings` | 4 |
| `fogHigh` | 5 |
| `extraction` | 6 |
| `cameraFields` | 7 |
| `telegraphs` | 8 |
| `mines` | 9 |
| `spawnSockets` | 10 |
| `actorShadows` | 11 |
| `actors` | 12 |
| `projectiles` | 13 |
| `markers` | 14 |

The z below is each node's own `zPosition`. The parent is the node `GameScene` adds it to. The world root is a child of the scene.

| Node | Parent | z |
|---|---|---:|
| Daily grade | world root | 1.5 |
| Near-miss edges | world root | 7.5 |
| Court telegraph rings | world root | 8.5 |
| Combat feedback | world root | 19 |
| VFX world layer | scene | 20 |
| Court light | camera | 790 |
| Lockdown tint | camera | 800 |
| VFX screen layer | camera | 900 |
| Intro overlay | camera | 950 |
| HUD root | camera | 1000 |

The daily grade is `decorations + 0.5`. The near-miss edges are `cameraFields + 0.5`. The court rings are `telegraphs + 0.5`. The lockdown tint and the court light multiply. The tint is a child of the camera, above the world stack and below the HUD. This does not close T1046.
