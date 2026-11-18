# Coordinator-only native v7 run command

Do not execute until exact coordinator recommendations have been generated, bound and
prepared successfully. This worker has not executed native tools. The existing
22:27 build command in `native-build-2227.log` used the following exact build setting:

```text
SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW SS_BUILDING_PERSPECTIVE_REVIEW
```

There are **no additional runtime environment variables** read by this fixture.
Inputs are read from the repository-relative path
`docs/review/building-perspective-detail-20261116/scene/native-inputs-v7/native-inputs.json`.
Do not rebuild after the executable hash is retained without updating provenance.

From the repository root, coordinator may run the already built exact one-test fixture:

```sh
set -e
PACKET=docs/review/building-perspective-detail-20261116/scene
test -f "$PACKET/native-inputs-v7/native-inputs.json"
shasum -a 256 -c "$PACKET/build-source-2227.sha256"
RESULT="/Users/appliedalchemylabs/.jcode/scratch/ss-building-perspective-v7-$(date -u +%Y%m%d-%H%M%S).xcresult"
test ! -e "$RESULT"
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS='SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW SS_BUILDING_PERSPECTIVE_REVIEW' -derivedDataPath /Users/appliedalchemylabs/.jcode/scratch/ss-releasevariation-native-derived-20261116 -resultBundlePath "$RESULT" -only-testing:SSRuntimeTests/BuildingPerspectiveSceneTests/testQuietSouthNeutralOrdinaryScene test-without-building
```

The selection must yield exactly one passed test, no failures/skips, six captures,
eighteen images and nineteen export attachments. Import with `scene/native.py import`,
passing the actual built `SSRuntimeTests.xctest/SSRuntimeTests` executable. The importer
compares its SHA256 to the executable actually loaded by the fixture. A successful
build, reading current source bytes or a zero-test result is not sufficient.
