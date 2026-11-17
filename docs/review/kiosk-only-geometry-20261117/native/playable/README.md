# DEBUG-only playable kiosk review

BP-001/007/012, T1045. Reversible plumbing authorized by coordinator at2026-11-17 02:54UTC. **Not production catalog admission or accepted art.**

## What this route does

`App/KioskPlayableReview.swift` is compiled only under `DEBUG`. It loads a four-file local review directory only after both explicit launch flags are present. The manifest SHA256, all three PNG SHA256 values, PNG signatures/dimensions and exact authored registrations must match compiled constants. Missing, aliased, malformed or modified input rejects the entire review and shows `KIOSK REVIEW REJECTED / DEFAULT ART`, not an accepted fallback. No launch flag means no review resource reads and unchanged ordinary rendering.

A narrow `WorldRenderer` branch replaces only the decorative texture of `solid-03-transit-kiosk`. Its existing authoritative footprint foundation remains visible. All other solids, ground, props, fog, Player/Camera families and actions, fields, controls, targeting and simulation remain on their existing routes. The broad `BenchmarkReviewArt` installer is deliberately not used because it also changes those unrelated cohorts. Installing/removing this override invalidates only static-solid presentation, not actor clips or the entire renderer. The internal test API supports current/candidate/default transitions without stepping or repositioning authority.

Both current and candidate keep the exact V9 blocked-base source. Its authored root is[525,653]. Because the delivered building PNG is an already-projected source, the base is composed inside that one source group at the existing D108 projection of local offset[13,13]:[0,13/sqrt(2)]. The base paints before the building, matching V9 depth order. No gameplay prop/root is moved. The world root of the source group remains[512,640].

**Projection limitation:** the ordinary playable scene uses its existing live world projection, whereas the V9 comparison's whole-scene midpoint projection lives in test fixtures. This route does not silently add that global projection or claim V9 scene parity. Neighbor art remains the existing playable renderer's art. A visible authoritative rectangular foundation may contrast with the isometric source silhouette. That is disclosed review evidence, not a footprint or visual-acceptance claim. The separately verified flat native comparison remains available for exact V9-context geometry comparison.

## Frozen source binding

`resources/manifest.json` SHA256 `11fd5f08aaeac28e2940005534802d2f9cf1d4366a8856ec0bf060ef59503264`.

| Role | Exact PNG SHA256 | Canvas | Root top-left | World root | Draw size |
|---|---|---|---|---|---|
| Current | `c411e33b79e0ffc5b0eb86143cd8785a564e573b5819bc1d4c399ef5d3b60264` |1000x1200|[500,1160]|[512,640]|[200,240]|
| Candidate | `5a1c7fa1cf23d7bd85bc5676b4a0e297662071404cbb3ec454c9153a7d97c931` |1000x1060|[500,1020]|[512,640]|[200,212]|
| V9 base | `c3313e0475e6aac62f1ec66ff7db4e254ae95e4ef193c5079bf5921e1e90d63b` |230x136|[115,95]|[525,653]|[57.5,34]|

`stage.py` copied exact bytes from the frozen textured source and V9 preparation. It refuses to overwrite `resources/`. No canonical texture or asset catalog is edited. The resources remain outside App/ and are not copied into Release bundles. Use an absolute canonical local directory, with no symlinks or `..` components. This is a local simulator review workflow, not a physical-device delivery claim.

## Build and selected tests

Run from repository root. Coordinate the simulator slot before the `test-without-building` or launch commands. Build-only does not launch the simulator.

```sh
xcodegen generate
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES -derivedDataPath docs/review/kiosk-only-geometry-20261117/native/playable/derived -only-testing:SSRuntimeTests/KioskPlayableReviewTests build-for-testing
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES -derivedDataPath docs/review/kiosk-only-geometry-20261117/native/playable/derived -resultBundlePath NEW_EMPTY_PLAYABLE_RESULT.xcresult -only-testing:SSRuntimeTests/KioskPlayableReviewTests test-without-building
```

The eight selected tests cover explicit/no opt-in, rejected arguments, source/manifest/registration/path corruption, current/candidate/base registration, mismatched authority, unchanged neighboring textures/transforms and actor nodes, reversible default restoration, and120actual legal session ticks with an uninjected control-session digest/snapshot comparison. Test count and execution status must come from the actual xcresult, not this description.

## Next actual playable comparison

After the selected tests pass and the coordinator grants the simulator slot:

```sh
APP=docs/review/kiosk-only-geometry-20261117/native/playable/derived/Build/Products/Debug-iphonesimulator/SSRuntime.app
RESOURCES="$PWD/docs/review/kiosk-only-geometry-20261117/native/playable/resources"
DEVICE=CACB3927-A76E-43A5-9ACA-C389EB38C0C3
xcrun simctl install "$DEVICE" "$APP"
xcrun simctl launch --terminate-running-process "$DEVICE" com.zer0state.surveillancesurvivor -SSMute -SSAutopilot run -SSKioskReview current -SSKioskReviewRoot "$RESOURCES"
# Inspect/capture current in the actual running app, then perform the candidate launch.
xcrun simctl launch --terminate-running-process "$DEVICE" com.zer0state.surveillancesurvivor -SSMute -SSAutopilot run -SSKioskReview candidate -SSKioskReviewRoot "$RESOURCES"
```

`-SSAutopilot run` is the existing legal-command pilot, not a scenario seed or a new repositioning shortcut. Omitting it retains the ordinary title/start/manual-input flow. Do not use `-SSSeed` to pretend a seeded state is a legal traversal. Capture screenshot/video at recorded ticks and show the explicit review status. Current/candidate asynchronous screenshots at different ticks are not pixel-equivalent evidence. Inspect live movement, pause/resume and retained base relationships without declaring complete gameplay qualification.

Restore ordinary behavior by relaunching without both kiosk flags. Release ignores this feature entirely because loader, fields, branches and launch handling are all inside `#if DEBUG`. Release build/symbol/string checks and native test results are recorded in the validation log files, not inferred from source inspection.
