# Native and host qualification, November 17, 2026

Classification: OBSERVED automated diagnostic evidence, not art or release acceptance.

Runtime source head for the fresh Debug build: `0aa395145de56852722256590f8b74cf7fd17118`. Pinned specs: `b1ed874e1e8eb0e61b2174b9093201e9a61e1a4b`. Xcode26.5, Swift6.3.2. Simulator: iPhone17Pro, iOS26.5 (23F77), arm64, CACB3927-A76E-43A5-9ACA-C389EB38C0C3. Neither iOS18 execution nor physical-device performance is established.

## Host partitions

`host-partitions.log` records850tests/123suites passing after521.555seconds with `swift test --skip CameraPlacementTests --skip CameraFairnessTests --parallel --num-workers 1`, then9CameraPlacement tests passing. The command was killed by the tool's600second deadline during the final fairness partition (background729709imvv, exit124). It is NOT an exit0 combined run. The850-test process compiled before the gate census correction; the separately retained25-test `gates-after.log` qualifies that correction.

A fresh separate `swift test --filter CameraFairnessTests --parallel --num-workers 1` completed exit0: one exhaustive legal-set test passed in75.778seconds. See `fairness.log`. Do not add overlapping targeted tests to claim a larger unique test census.

## Fresh Debug simulator test

`xcodegen generate`, then `xcodebuild test -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' -configuration Debug CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT`, selected suites:

- ExistingArtTraversalTests
- TouchControllerTests
- TerminalAccessibilityTests
- AudioLifecycleTests
- SceneInputIntegrationTests
- RuntimeAssetRegistryTests
- PrivacyManifestTests

Observed result:27passed,0failed,0skipped,0expected failures. `native-debug/summary.json` is the xcresulttool summary. Full local result: `$JCODE_SCRATCH_DIR/ss-production-native-20261117-0206.xcresult`; full log and exported attachments use the same prefix. Actual build used `ss-blocked-base-curb-v9-derived-20261117-0020` as derived data, but ran a fresh `xcodebuild test`, not test-without-building.

Independently ran the existing traversal validator's `attachments` and `validate_packet` functions over all exported attachments:2arms,52scene images,824post-action rows,50selected-texture images,1073delivered resource bindings verified. Each arm contains380commands, pause/collision/reversal/front-rear phases and independently replayed final digest, and both final digests match. See `native-debug/traversal-validation.json`.

This is NOT the historical strict result importer: its1-or3-test whitelist was deliberately not relaxed to accept this27-test run. The27-test result is qualified separately by the actual summary. Resource inventory is a reachable bundle superset, not proof every asset was visible.

## Fresh Release simulator test

The same build configuration and destination, switched to Release and excluding traversal, completed exit0 in325.3seconds. `native-release-summary.json` records25passed,0failed,0skipped. The actual result tree includes AudioLifecycleTests, PrivacyManifestTests, RuntimeAssetRegistryTests, SceneInputIntegrationTests and TouchControllerTests. Although TerminalAccessibilityTests was also selected, it did not appear in the Release result tree. Therefore this is not Release terminal-accessibility coverage. Full local result/log: `$JCODE_SCRATCH_DIR/ss-production-release-20261117-0211.xcresult` and `.log`. The apparent240second background stall was redirected build output; active Swift compiler processes and an advancing log established progress, so it was not cancelled.

## Encounter and presentation qualification

A fresh Debug run selected ExistingArtEncounterTests and DevicePresentationRegressionTests:16passed,0failed,0skipped, exit0 in87.3seconds. Result: `$JCODE_SCRATCH_DIR/ss-production-encounter-20261117-0217.xcresult`; `native-encounter-summary.json` retained. The existing attachment/content validator independently verified9captures and1073resource bindings, including all four Camera integrity states, Camera destruction, dense/hostile entities, mines, entity death and field occlusion. It explicitly reports player damage and telegraphs NOT_OBSERVED. See `encounter-validation.json`. Static legal-pilot rendered frames are not live playtesting, boss telegraph acceptance, or a complete journey. Historical strict single-test importer was not relaxed to accept this16-test result.

## Actual image inspection

Two unchanged actual simulator PNGs retained:

- `native-debug/front-south-shipping.png`, SHA256 `a7bff1ce83a8b8c336facb79c8b11492924b992612208a3f5654310c92d668b1`.
- `native-debug/release-shipping.png`, SHA256 `5d202b5cc7dca66fa184e242d7e7d22aa40b7b35d1c76cfbc25ba0ad377e0289`.

Coordinator inspected both2112x978images. OBSERVED: legacy prop near the top has an opaque rectangular dark background; paving is conspicuously repetitive; player/prop silhouettes and scale remain visually inconsistent. The second capture shows the countermeasure prompt. This SKView test does not host the SwiftUI choice overlay, so its absence is NOT evidence that upgrade choices are absent in the complete app. These are shipping-tree diagnostic images, not the V9 editable-source scene and not the new kiosk-only proposal. No visual acceptance, source-family admission, listening QA, complete player journey, all16poses, display scanout or physical-device certification follows from this pass.

The complete current traversal passed locally, but does not erase the historical CI35second timeout at314/290of380samples (issue259). Its cause remains unproven. Issue237's intermittent15/16pose coverage remains separate and unresolved.

## Asset audit interpretation

The existing canonical catalog remains authoritative:1530entries,1073accepted/reachable runtime assets,1030image resources,43audio/music resources. All1030decoded image dimensions matched metadata.152adapted entries and3level-matched Hexwire cues record SOURCE hashes rather than delivered-file hashes. A naive155-hash-mismatch audit was therefore an invalid comparison, not155asset-corruption defects. The actual native validator matched all1073DELIVERED resource hashes instead. Do not rewrite source provenance to conceal this distinction.

Metadata presence is not rights approval. Three Hexwire cues retain generation-date/plan evidence pending. No audio listening, physical-floor measurement, external playtest or art-owner acceptance was performed. Expansion remains NOT_COMPUTABLE.
