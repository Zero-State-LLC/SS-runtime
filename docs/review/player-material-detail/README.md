# Player material detail comparison

T1045 source polish. Proposed material-only revision of SS-player-low-recovery. Retained source contrast is less suppressed on calf, boot vamp and plain material surfaces. No new noise, geometry, UV placement, laces, poses, stance, arm swing or timing. The previous candidate is preserved.

Verification: all 16 output alpha masks match baseline exactly; all changed pixels lie inside the original calf/boot masks. Pose, rig, geometry and assembly inputs are byte-identical. See material-only-verification.json and verify_material.py. An initial diagnostic assumed rows above 260 contained no calf pixels; it failed on pose 4 because raised calf geometry reaches row 259. That assumption was discarded in favor of comparing the actual existing part masks. No production test was changed.

Inspection shows stronger calf folds and toe/sole separation. Remaining boot faceting and the lower material detail relative to the torso are not claimed solved. Coefficients are an authored comparison, not physical measurements. This reuses retained source art, with no new costume or anatomical design.

Normal and quarter videos contain the same 16 poses, repeated eight times. Each cycle lasts 0.5 and 2 seconds respectively. These are source previews, not renderer captures. No runtime resources changed. Contact, facings, action coverage, visual acceptance and production admission remain open. Other copied studies retain their historical provenance; this README and material-only-verification.json describe the new change.


## Renderer reconciliation — 2026-10-16

The 16 material-detail textures are staged in AppTests/BenchmarkAssets, with an updated source record and unchanged pose JSON. Production art and metadata remain unchanged. Previous test textures are preserved in the source workspace and Git baseline.

Xcode result Test-SSRuntime-2026.10.16_12-23-14--0700: DisplayedPlaybackTests, 15 tests passed, zero failures/skips, 196.027 seconds on iPhone 17 Pro / iOS 26.5 Simulator. The suite covers partial input, repeated Reduced Motion cycles, selected-clip and command-driven interruptions, and six projected shared traversals. All 27 exported metric attachments report 16 frames and coveragePassed=true; see coverage-summary.json and renderer-records. This was not a movie-recording-load run and supplies no new continuous video.

Built-resource verification: Xcode optimizes PNGs to CgBI, so original file hashes do not match built files. After Apple pngcrush reversal, all 16 alpha channels and opaque RGB pixels match the candidate exactly. Translucent RGB is excluded from exact equality because of premultiplication rounding. Pose JSON is byte-identical. See built-resource-verification.json. Initial byte-hash comparison failed due to this encoding transformation; it was not treated as a pass.

`swift test --disable-sandbox --filter Clip` exited 0: 66 tests in 11 suites passed. These are targeted core clip tests, not a fresh full-core or full-app run. No assertions, pose parameters or playback rules changed. Contact/seam visual acceptance, missing facings/actions, production admission and device performance remain open.
