# Device presentation QA — issue #117

Intent accepted 2026-10-13. Baseline main: `6e42cb47e8be10cffcc8398cbf9e2fff5fbe7dac`.
Spec: `2377b99c6b6d1654e2cb976ee1b7e07b75c77e1a`. No gameplay, content, arena, or replay identity change.

## Checks required

| Area | Automated coverage | Physical check |
|---|---|---|
| Camera follow | CameraFollowTests: turn continuity, dead zone, vertical facing, bounds/reset | Turn in place, reverse while moving, arena edge |
| Surveillance fields | DevicePresentationRegressionTests: emitter position, clockwise convention, narrow occluders, cover changes | Approach cover; compare field boundary and Exposure |
| Animation lifecycle | Removed camera sprite reappears with action attached | Movement/idle/hurt/defeat and camera damage states |
| Performance | Frame timeline streak classification; core suite | Record frame percentiles with `-SSQA`, repeat baseline opening and full run |
| Controls | Existing SceneInputIntegrationTests in Debug and Release | Movement, Dodge, pause/resume, restart |
| Visual clipping | Geometry coverage; broader visual review pending | Cameras, walls, gates, actors, HUD and safe-area edges |
| Authority | Full core/replay golden suite | No claim that visual QA substitutes for deterministic tests |

## Evidence and status

- Baseline user playtest: FAIL (immediate stutter/jumps and rendering defects).
- [Baseline profile](baseline.md): renderer and name lookup dominate; outline generation is not the primary observed cost.
- Candidate core checks: 740 tests across 104 suites passed (528.067 seconds). Debug/Release app CI still running.
- Candidate physical playtest: FAIL. User reports broken camera and character animation, jumbled/unrecognizable assets, collision problems, and suspected hit-detection problems. See candidate-findings.md.
- C-003 p95 <=16.67 ms remains unproven. The connected iPhone 17 Pro is not the baseline iPhone 12; report actual hardware rather than relabel it.

No release or full-QA pass is claimed. Further animation/clipping symptoms require reproduction on the candidate; issues remain open until verified.

## Measurement notes

Each note records one fact about bytes or draw calls already on main. None of them closes a parent task.

| Note | Fact |
|---|---|
| [solid-footprint-2026-11-01.md](solid-footprint-2026-11-01.md) | Two blocking solids: canvas, ink, and the blocking rectangle |
| [solid-footprint-twelve-2026-11-02.md](solid-footprint-twelve-2026-11-02.md) | The other twelve blocking solids, same three facts |
| [camera-frame-bounds-2026-11-02.md](camera-frame-bounds-2026-11-02.md) | Camera head frames and the five housings, at anchor (32, 88) |
| [enemy-sprite-bounds-2026-11-02.md](enemy-sprite-bounds-2026-11-02.md) | Five standard enemies, canvas 64×64, anchor (32, 56), body radii |
| [retest-checklist.md](retest-checklist.md) | Human rows, plus the device-sitting bot column |
| [decoration-placement-2026-11-02.md](decoration-placement-2026-11-02.md) | Twenty-one placed decoration canvases and their draw boxes |
| [tiled-planes-2026-11-02.md](tiled-planes-2026-11-02.md) | Six ground tiles and the two fog bands |
| [player-sprite-bounds-2026-11-03.md](player-sprite-bounds-2026-11-03.md) | Shipped player frames, canvas 64×64, anchor (32, 56), radius 18 |
| [boss-sprite-bounds-2026-11-03.md](boss-sprite-bounds-2026-11-03.md) | Shipped `algorithmicModerate` frames, canvas 96×96, anchor (48, 84), radius 30 |
| [shape-hazards-2026-11-03.md](shape-hazards-2026-11-03.md) | Projectile, mine, and telegraph shapes the renderer already draws |
| [unplaced-images-2026-11-03.md](unplaced-images-2026-11-03.md) | Motif, telegraph, and objective PNGs the draw path does not place |
| [hud-shapes-2026-11-03.md](hud-shapes-2026-11-03.md) | HUD and control PNGs, and the shapes the HUD draws instead |
| [decoration-solid-overlap-2026-11-03.md](decoration-solid-overlap-2026-11-03.md) | No placed decoration canvas shares area with a blocking rectangle |
| [player-action-frames-2026-11-03.md](player-action-frames-2026-11-03.md) | South dodge, recover, hurt, defeat, extraction, and complete frames |
| [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md) | Kerb, solid foundation, extraction, fields, cones, sockets, markers, shadow, and gate |
| [player-facing-frame-01-2026-11-03.md](player-facing-frame-01-2026-11-03.md) | Idle and move frame 01 in each direction; the other directions are not copies of south |
| [south-state-frame-01-2026-11-03.md](south-state-frame-01-2026-11-03.md) | South frame 01 of the non-idle enemy states and of the elite |
| [player-direction-copies-2026-11-03.md](player-direction-copies-2026-11-03.md) | Hurt, defeat, and extraction reuse the south bytes in every direction |
| [direction-distinct-2026-11-03.md](direction-distinct-2026-11-03.md) | Outside those three clips, no two directions share a PNG hash |
| [player-action-facing-frame-01-2026-11-03.md](player-action-facing-frame-01-2026-11-03.md) | Dodge, recover, and complete frame 01 in north, east, and west |
| [enemy-idle-frame-01-2026-11-03.md](enemy-idle-frame-01-2026-11-03.md) | Idle frame 01 in north, east, and west for the five standard enemies |
| [boss-facing-frame-01-2026-11-03.md](boss-facing-frame-01-2026-11-03.md) | Boss frame 01 in north, east, and west of the seven states |
| [elite-facing-frame-01-2026-11-03.md](elite-facing-frame-01-2026-11-03.md) | Elite frame 01 in north, east, and west of the eight states |

Next session: follow [retest-checklist.md](retest-checklist.md) (D-105 allows device checks on any build).
