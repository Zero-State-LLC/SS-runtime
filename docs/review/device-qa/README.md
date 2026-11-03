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
| [enemy-action-facing-frame-01-2026-11-03.md](enemy-action-facing-frame-01-2026-11-03.md) | Non-idle frame 01 in north, east, and west for the five standard enemies |
| [player-action-rest-frames-2026-11-03.md](player-action-rest-frames-2026-11-03.md) | Dodge 02–04, recover 02, and complete 02–04 in north, east, and west |
| [clip-lengths-2026-11-03.md](clip-lengths-2026-11-03.md) | Every shipped actor clip has the same frame count in all four directions |
| [player-idle-rest-frames-2026-11-03.md](player-idle-rest-frames-2026-11-03.md) | Idle frames 02–04 in north, east, and west |
| [player-move-rest-frames-2026-11-03.md](player-move-rest-frames-2026-11-03.md) | Move frames 02–06 in north, east, and west |
| [enemy-idle-rest-frames-2026-11-03.md](enemy-idle-rest-frames-2026-11-03.md) | Idle frames 02–04 in north, east, and west for the five standard enemies |
| [enemy-south-move-rest-2026-11-03.md](enemy-south-move-rest-2026-11-03.md) | South move frames 02–06 for the four enemies that have a move clip |
| [enemy-move-rest-frames-2026-11-03.md](enemy-move-rest-frames-2026-11-03.md) | Move frames 02–06 in north, east, and west for those four enemies |
| [boss-south-rest-frames-2026-11-03.md](boss-south-rest-frames-2026-11-03.md) | Boss south frames after 01 |
| [boss-six-rest-frames-2026-11-03.md](boss-six-rest-frames-2026-11-03.md) | Boss frames 02–06 in north, east, and west |
| [boss-long-rest-frames-2026-11-03.md](boss-long-rest-frames-2026-11-03.md) | Boss stagger and long frames in north, east, and west |
| [elite-south-rest-frames-2026-11-03.md](elite-south-rest-frames-2026-11-03.md) | Elite south frames after 01 |
| [elite-six-rest-frames-2026-11-03.md](elite-six-rest-frames-2026-11-03.md) | Elite frames 02–06 in north, east, and west |
| [elite-short-rest-frames-2026-11-03.md](elite-short-rest-frames-2026-11-03.md) | Elite short frames in north, east, and west |
| [enemy-south-hurt-defeat-rest-2026-11-03.md](enemy-south-hurt-defeat-rest-2026-11-03.md) | Standard-enemy hurt and defeat, south, after frame 01 |
| [enemy-hurt-defeat-rest-frames-2026-11-03.md](enemy-hurt-defeat-rest-frames-2026-11-03.md) | Standard-enemy hurt and defeat in north, east, and west |
| [enemy-south-action-rest-2026-11-03.md](enemy-south-action-rest-2026-11-03.md) | South frames 02–03 of pursuit, charge, recover, pulse, cast, and throw |
| [enemy-south-commit-rest-2026-11-03.md](enemy-south-commit-rest-2026-11-03.md) | South frame 02 of the five commit clips |
| [informant-action-rest-frames-2026-11-03.md](informant-action-rest-frames-2026-11-03.md) | Informant pursuit frames 02–03 and pursuitCommit 02 in north, east, and west |
| [cable-charge-rest-frames-2026-11-03.md](cable-charge-rest-frames-2026-11-03.md) | Cable charge frames 02–03 and chargeCommit 02 in north, east, and west |
| [cable-recover-rest-frames-2026-11-03.md](cable-recover-rest-frames-2026-11-03.md) | Cable recover frames 02–03 in north, east, and west |
| [fog-pulse-rest-frames-2026-11-03.md](fog-pulse-rest-frames-2026-11-03.md) | Fog pulse frames 02–03 and pulseCommit 02 in north, east, and west |
| [witch-cast-rest-frames-2026-11-03.md](witch-cast-rest-frames-2026-11-03.md) | Witch cast frames 02–03 and castCommit 02 in north, east, and west |
| [vendor-throw-rest-frames-2026-11-03.md](vendor-throw-rest-frames-2026-11-03.md) | Vendor throw frames 02–03 and throwCommit 02 in north, east, and west |
| [player-copied-direction-rows-2026-11-03.md](player-copied-direction-rows-2026-11-03.md) | North, east, and west hurt, defeat, and extraction files, which match the south bytes |
| [shell-image-bounds-2026-11-03.md](shell-image-bounds-2026-11-03.md) | Title backdrop, wordmark, plates, launch mark, and app icon |
| [captain-housing-bounds-2026-11-03.md](captain-housing-bounds-2026-11-03.md) | The two Captain housing PNGs, idle and active |
| [audio-file-bytes-2026-11-03.md](audio-file-bytes-2026-11-03.md) | The 34 shipped m4a files |
| [world-layer-order-2026-11-03.md](world-layer-order-2026-11-03.md) | World layers 0 through 14, and the roots above that stack |
| [layer-offsets-2026-11-03.md](layer-offsets-2026-11-03.md) | Foundation, gate, ghost, and camera-badge offsets inside a layer |
| [haptic-patterns-2026-11-03.md](haptic-patterns-2026-11-03.md) | The six haptic patterns and the UIKit call each one makes |
| [player-weapon-cues-2026-11-03.md](player-weapon-cues-2026-11-03.md) | Civic Pulse, impact, player damage, and dodge cues |
| [camera-cues-2026-11-03.md](camera-cues-2026-11-03.md) | Camera hit, critical, destroy, field-off, and tamper cues |
| [run-state-cues-2026-11-03.md](run-state-cues-2026-11-03.md) | Detection, lockdown, extraction, blackout, and terminal cues |
| [boss-upgrade-cues-2026-11-03.md](boss-upgrade-cues-2026-11-03.md) | Boss telegraph and phase cues, the three upgrades, and the lethal warning |
| [effect-voice-ceiling-2026-11-03.md](effect-voice-ceiling-2026-11-03.md) | Eight effect voices, and which cue is dropped first |
| [mix-and-blackout-2026-11-03.md](mix-and-blackout-2026-11-03.md) | Mix defaults, crossfades, music beds, and the blackout drop |

Next session: follow [retest-checklist.md](retest-checklist.md) (D-105 allows device checks on any build).
