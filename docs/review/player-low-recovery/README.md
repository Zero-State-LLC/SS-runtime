# Lower-recovery renderer validation

## Verified

The new 16-frame source and matching pose metadata were reconciled into the test-only renderer fixture. See source-record.json for exact hashes. App run Test-SSRuntime-2026.10.15_17-42-31--0700 passed 111 named tests / 113 executions, zero failures or skips. Full/half/quarter input and all three Reduced Motion captures each observed all 16 textures. Prepared outline playback had no texture readbacks. This is post-action simulator evidence, not physical scanout or device acceptance.

The core runner completed 773 tests / 109 suites with all tests passed in 619.924 seconds. However, the swift test command exited 1 after sandbox-exec denied manifest evaluation (sandbox_apply: Operation not permitted). Preserve this as test-runner success with a command-level environment failure, not a clean command pass. App and core tests overlapped, so callback timing is retained as loaded-host evidence, not an isolated performance result. Stage-4 p95 ranges from 16.67 to 33.33 ms and maxima reach 43.84 ms. No sustained 60-fps claim is made.

## Contact gap

Projected authored support-toe measurements show displacement within support observations. Full-input clean review spans 2.50–2.75 logical pixels per support segment; half input spans 7.25 and quarter input spans 7.75–8.75. Other full-input runs reach 4.75. These values include frame holds, sampling phase and whole-unit presentation rounding. They are not pixel-tracked contact or an acceptance threshold. Single-sample segments report null, never zero drift.

Normal/quarter-speed visual review, contact acceptance and the interaction matrix remain open. Frame coverage alone must not close BP-008. Shared scene and production admission remain deferred.

## Researched next comparison

Apple documents action-speed scaling: https://developer.apple.com/documentation/spritekit/skaction . Unity distinguishes animation pose from root trajectory: https://docs.unity.com/en-us/engine/6000.7/manual/animation-section/animation-mecanim/avatar-creationand-setup/root-motion . These mechanisms do not prescribe an SS policy.

Proposed next experiment: compare the exact authored-cadence control against presentation phase driven by actual post-collision distance. Keep simulation authoritative and unchanged; do not use desired joystick speed when blocked. Assess fixed frame holds and stop/start/reversal separately. This proposal must be reconciled with the existing rational timing contract before runtime adoption. No phase policy or numerical slip tolerance has been inferred or applied.
