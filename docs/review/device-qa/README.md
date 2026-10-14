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
- Candidate automated checks: in progress.
- Candidate physical playtest: pending.
- C-003 p95 <=16.67 ms remains unproven. The connected iPhone 17 Pro is not the baseline iPhone 12; report actual hardware rather than relabel it.

No release or full-QA pass is claimed. Further animation/clipping symptoms require reproduction on the candidate; issues remain open until verified.
