# BP-010 legal-encounter contrast diagnostic

Status: REVIEWED static encounter; production admission incomplete.

Runtime base 746ef65 plus the new test; specs c075b21e9e70828b032f7f319a712c179450b4f9. Normal seed-1 GameSession commands from DebugAutopilot run reached nearby enemies and projectiles without scenario seeding. GameScene then advanced normally and rendered its production scene/HUD/fog/fields. Only the Player texture was replaced with its registered painted neutral facing, at the same 64×64 logical size. Three paused captures compare the fine outline at 100%, 25% and 0%. This uses the current shipping projection, not the experimental shared-scene projection.

Recorded state: tick 461, Player (264,592), south; two enemies, one projectile, no telegraphs. The full no-border screenshot visibly includes both enemies, a projectile and a Camera field. The Player remains distinguishable, including the grayscale Player crop. Existing enemy dashed outlines are preserved. This is an observer judgment about this frame, not a faction-recognition user study. No dense encounter, motion, hit confirmation or final source-animation acceptance follows. The legacy environment, camera and enemy art are visibly inconsistent with the benchmark and remain unfinished.

The attachment serializes a GhostRecord with seed, identity, tick, digest and normal input commands. It is a review artifact, not a successful run saved to the user's best-run store. Decoding and replaying those commands reproduces the captured state's digest. This verifies legal provenance without overwriting authoritative state. The source scene uses normal GameScene settings; no controlled fog-density matrix was performed. Paused SpriteKit actions and a neutral Player pose are not animation evidence.

Initial iOS build failed because PlayerCommand is not Encodable. Defect #125 was filed before repair. The test now uses the existing GhostRecord format and verifies replay digest; no assertion was weakened and production code was unchanged. Initial failure is retained in work/player-contrast-encounter/capture.xcresult. Corrected result Test-SSRuntime-2026.10.14_18-16-00--0700.xcresult: succeeded, 98 executions, one existing warning; new encounter test passed in 6.668 seconds. 91 Swift Testing tests passed in 36.679 seconds, plus five XCTest cases and two extra parameter executions. Simulator iPhone 17 Pro CACB3927-A76E-43A5-9ACA-C389EB38C0C3; viewport 704×326 points, original captures 2112×978 pixels.

Core regression: 773 tests in 109 suites passed in 427.884 seconds. The app-test-only serialization correction does not change that core code. No physical-device testing occurred.

Continue with multiple encounter phases, directional movement, damage versus steady-state treatment, controlled fog, occlusion and dense-scene evidence before selecting a production border policy. Do not call this sparse still the completed BP-010 matrix or the final benchmark scene.
