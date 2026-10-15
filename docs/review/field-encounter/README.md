# BP-001/BP-010 replayable field encounter comparison

Specification: d859658, researched field-contrast comparison. This capture adds an unedited encounter to the quiet-scene comparison. It does not select or admit a production field style.

## Reproducible encounter

GameSession seed 1 advances with normal DebugAutopilot run commands until nearby enemies, a nearby projectile and a live nearby Camera field coexist. No scenario seeding or snapshot coordinate edits. The presented capture is tick 461: two enemies, one projectile, zero telegraphs. Exact commands, identity, seed, tick and digest are attached in BP010-field-encounter-commands-seed-1.json. GhostRun replay matches digest 3ef4396ad640181e63f716d717d117d262fd60d88480aa2f19e24f83d31d3a13.

GameScene renders the production ground/fog/HUD/geometry; the Player is a painted neutral and standard Cameras use the complete candidate family. Each control/dark/paired image uses the same authoritative snapshot/digest. Normal and Reduced Motion settings are compared while paused; this is a settings/state comparison, not temporal motion or interruption evidence. Candidate art remains test-only.

## Validation

Xcode Test-SSRuntime-2026.10.14_22-37-59--0700.xcresult: 106 executions, zero failures. Existing nonthrowing-try warning remains. Three focused core CameraPresentationTests passed with exit 0. The prior full core run remains 773/109, exit 0; no core source changed this turn. Each PNG is 2112×978 for 704×326 logical points at 3×. Native, half-size and grayscale comparison sheets derive from these captures.

## Observations

The original fill is difficult to locate in grayscale against the busy paving. Dark-only is visible but loses clarity against darker patches. Paired outlines remain clearer through the fog/busy ground, with the projectile and enemies still visible in this snapshot. The long high-contrast edges are visually prominent and may compete with attack cues; one still cannot resolve that tradeoff. The nearby enemy overlaps part of the field boundary. These are observed review judgments, not accessibility compliance or user-test findings.

The complete camera, its marker and ground field are present, but the camera is cropped near the top HUD and the field apex is visually separated from the pole base/overlapped by an enemy. Emitter-to-art registration should be explicitly inspected before acceptance rather than inferred from this picture. Legacy buildings retain opaque backgrounds, disparate scale and perspective; the white Player outline remains. This QA scene is not the approved street-corner benchmark.

## Still required

Dense encounter, Captain field visuals, detecting-state distinction, overlapping fields, explicit clipped-wall/corner views, intended dark asphalt/shadow backdrops, moving traversal and temporal Reduced Motion, user readability review and performance. Existing geometry/lifecycle tests support correctness but do not close those visual gates. Full character animation/environment production and physical-device acceptance remain open.
