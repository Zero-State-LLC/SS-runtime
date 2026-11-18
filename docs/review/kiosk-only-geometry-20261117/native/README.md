# Native kiosk-only geometry comparison

BP-001/007/012, T1045. Review evidence only, not accepted art, production admission, release or physical-device certification.

This new fixture substitutes the two frozen **flat** kiosk source PNGs into the retained V9 native scene. It keeps all V9 textured neighboring buildings, ground, supplements, actors, controls, fields and depth rules. Both arms use their own exact registration and ground-contact projections. No geometry source, earlier native capture, or prior preparation is overwritten. This is not a textured-kiosk integration or an interactive runtime-delivery claim.

## Scope and lineage

- `AppTests/KioskOnlyGeometrySceneTests.swift` is adapted from the exact V9 harness cited in its header. `harness-adaptation.diff` records the initial bounded adaptation.
- `native.py` prepares two sources, rejects stale dependencies, strictly imports one passed native test and verifies six captures/eighteen images. Prepared records are not native evidence.
- `test_native.py` uses explicitly synthetic records for adapter regressions. Passing these tests is not a native-capture result.
- `retained.py` reruns stored-summary, attachment, executable, source, authority, contact and pixel checks without another simulator execution.
- Across each same-zoom pair, all pixels outside the union of the two kiosk canvases plus a two-native-pixel filtering margin must match exactly. This is a conservative rectangular mask, not a claim that every inside-mask background pixel is independently proven unchanged. Source/actor identity checks separately preserve all non-kiosk content.
- Controls and Player shadow are supplied by the actual native scene. The original kiosk roof vent is intentionally absent in both flat source arms. The unchanged blocked base may still read as a stair landing. No horizontal spacing or gameplay footprint correction is claimed.

## Preparation and portable checks

```sh
python3 docs/review/kiosk-only-geometry-20261117/native/native.py check
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/kiosk-only-geometry-20261117/native/test_native.py
swift test --scratch-path docs/review/kiosk-only-geometry-20261117/.swift-build --skip-build --filter 'CameraMountSolidTests|CameraHousingArtTests|EnvironmentContractTests'
```

Fresh preparation is `native.py prepare --output NEW_EMPTY_PATH`, but the Swift fixture deliberately reads the frozen `native/prepared` path. Never replace that directory to retrofit a later source attempt.

## Serialized native execution

ADAPT `blocked-base-curb-relief-20261116/scene/RUN-NATIVE.md:1-48`. The native slot must be reserved with the coordinator. No simulator reset, erasure or external asset generation is required.

```sh
xcodegen generate
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS='SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW SS_KIOSK_ONLY_GEOMETRY_REVIEW' -derivedDataPath docs/review/kiosk-only-geometry-20261117/native/derived -only-testing:SSRuntimeTests/KioskOnlyGeometrySceneTests/testQuietSouthNeutralOrdinaryScene build-for-testing
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS='SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW SS_KIOSK_ONLY_GEOMETRY_REVIEW' -derivedDataPath docs/review/kiosk-only-geometry-20261117/native/derived -resultBundlePath NEW_EMPTY_RESULT.xcresult -only-testing:SSRuntimeTests/KioskOnlyGeometrySceneTests/testQuietSouthNeutralOrdinaryScene test-without-building
python3 docs/review/kiosk-only-geometry-20261117/native/native.py import --xcresult NEW_EMPTY_RESULT.xcresult --output NEW_EMPTY_CAPTURE --test-executable docs/review/kiosk-only-geometry-20261117/native/derived/Build/Products/Debug-iphonesimulator/SSRuntime.app/PlugIns/SSRuntimeTests.xctest/SSRuntimeTests
python3 docs/review/kiosk-only-geometry-20261117/native/retained.py NEW_EMPTY_CAPTURE --test-executable docs/review/kiosk-only-geometry-20261117/native/derived/Build/Products/Debug-iphonesimulator/SSRuntime.app/PlugIns/SSRuntimeTests.xctest/SSRuntimeTests
```

Hash the freshly built executable before native execution. Do not rebuild between capture and import. Inspect actual images at all three zooms after the strict importer succeeds. A build success, zero-test run or synthetic adapter result cannot substitute for native proof.
