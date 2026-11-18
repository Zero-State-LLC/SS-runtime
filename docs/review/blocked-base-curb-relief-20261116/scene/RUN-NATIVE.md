# Coordinator-only serialized native V9 commands

ADAPT current `footprint-ground-repair-20261116/scene/RUN-NATIVE.md:1-48`.
This file contains instructions only. Scene worker did not execute any native command.

Not executed by this worker. Do not start until final source recommendation,
`scene/native.py bind` and `prepare` have succeeded. Keep existing native jobs/results
and the immutable V8 packet untouched. A fresh derived directory avoids overwriting
V8 build products. No additional runtime environment variables are read by the fixture.

Bind ONLY `source/attempt-02/manifest.json`, pinned SHA256
`5b0943d029eadaf00d4e2d039dbeeda3e3353241c7881f28dd370c3295ab1891`.
The recommendation evidence must be outside the entire `source/` tree.
The first manifest and both source attempts remain immutable. The one bounded source
correction is consumed, so no third aesthetic attempt is authorized.

Required compile flags:
`SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW SS_BLOCKED_BASE_CURB_REVIEW`.
The existing `project.yml` discovers `AppTests/`; generation is coordinator-owned.

From repository root, after obtaining the serialized slot:

```sh
set -e
PACKET=docs/review/blocked-base-curb-relief-20261116/scene
DERIVED=/Users/appliedalchemylabs/.jcode/scratch/ss-blocked-base-curb-v9-derived-20261116
DEST='platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3'
FLAGS='SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW SS_BLOCKED_BASE_CURB_REVIEW'
test -f "$PACKET/native-inputs-v9/native-inputs.json"
xcodegen generate
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination "$DEST" CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS="$FLAGS" -derivedDataPath "$DERIVED" -only-testing:SSRuntimeTests/BlockedBaseCurbSceneTests/testQuietSouthNeutralOrdinaryScene build-for-testing
EXECUTABLE="$DERIVED/Build/Products/Debug-iphonesimulator/SSRuntime.app/PlugIns/SSRuntimeTests.xctest/SSRuntimeTests"
test -f "$EXECUTABLE"
shasum -a 256 "$EXECUTABLE" AppTests/BlockedBaseCurbSceneTests.swift "$PACKET/native-inputs-v9/native-inputs.json"
RESULT="/Users/appliedalchemylabs/.jcode/scratch/ss-blocked-base-curb-v9-$(date -u +%Y%m%d-%H%M%S).xcresult"
test ! -e "$RESULT"
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination "$DEST" CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS="$FLAGS" -derivedDataPath "$DERIVED" -resultBundlePath "$RESULT" -only-testing:SSRuntimeTests/BlockedBaseCurbSceneTests/testQuietSouthNeutralOrdinaryScene test-without-building
python3 "$PACKET/native.py" import --xcresult "$RESULT" --output "$PACKET/native-capture-v9" --test-executable "$EXECUTABLE"
python3 "$PACKET/retained.py" "$PACKET/native-capture-v9" --test-executable "$EXECUTABLE"
```

The executable path above follows the retained hosted unit-test pattern. If Xcode places
the built product elsewhere, use the actual `SSRuntimeTests.xctest/SSRuntimeTests` build
artifact and retain its exact path, not the app binary or a source SHA. Preserve build
and test logs and the pre-run binary hash. Never rebuild between capture and import.

Expected result: exactly **one passed test**, zero failures/skips/expected failures,
**six captures/eighteen images**, nineteen attachments with the exact V9 test identity,
loaded/fresh-built executable SHA agreement, nine full baseline RGBA matches, and all
semantic-plan/contact/authority checks. A zero-test result or successful build is not
capture evidence. Failed import leaves no native-capture output directory. Native and
visual failures must remain retained, not normalized away.

After import, coordinator must inspect actual images at all three zooms in both arms
and publish the bounded final scene for owner review. This worker does not recommend
source art or grant owner acceptance, production admission, merge or issue closure.
