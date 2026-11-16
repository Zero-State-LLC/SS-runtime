# Coordinator-only serialized native V8 commands

Not executed by this worker. Do not start until final source recommendation,
`scene/native.py bind` and `prepare` have succeeded. Keep existing native jobs/results
and the immutable V7 packet untouched. A fresh derived directory avoids overwriting
V7 build products. No additional runtime environment variables are read by the fixture.

Required compile flags:
`SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW SS_FOOTPRINT_GROUND_REVIEW`.
The existing `project.yml` discovers `AppTests/`; generation is coordinator-owned.

From repository root, after obtaining the serialized slot:

```sh
set -e
PACKET=docs/review/footprint-ground-repair-20261116/scene
DERIVED=/Users/appliedalchemylabs/.jcode/scratch/ss-footprint-ground-v8-derived-20261116
DEST='platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3'
FLAGS='SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW SS_FOOTPRINT_GROUND_REVIEW'
test -f "$PACKET/native-inputs-v8/native-inputs.json"
xcodegen generate
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination "$DEST" CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS="$FLAGS" -derivedDataPath "$DERIVED" -only-testing:SSRuntimeTests/FootprintGroundSceneTests/testQuietSouthNeutralOrdinaryScene build-for-testing
EXECUTABLE="$DERIVED/Build/Products/Debug-iphonesimulator/SSRuntime.app/PlugIns/SSRuntimeTests.xctest/SSRuntimeTests"
test -f "$EXECUTABLE"
shasum -a 256 "$EXECUTABLE" AppTests/FootprintGroundSceneTests.swift "$PACKET/native-inputs-v8/native-inputs.json"
RESULT="/Users/appliedalchemylabs/.jcode/scratch/ss-footprint-ground-v8-$(date -u +%Y%m%d-%H%M%S).xcresult"
test ! -e "$RESULT"
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination "$DEST" CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS="$FLAGS" -derivedDataPath "$DERIVED" -resultBundlePath "$RESULT" -only-testing:SSRuntimeTests/FootprintGroundSceneTests/testQuietSouthNeutralOrdinaryScene test-without-building
python3 "$PACKET/native.py" import --xcresult "$RESULT" --output "$PACKET/native-capture-v8" --test-executable "$EXECUTABLE"
python3 "$PACKET/retained.py" "$PACKET/native-capture-v8" --test-executable "$EXECUTABLE"
```

The executable path above follows the retained hosted unit-test pattern. If Xcode places
the built product elsewhere, use the actual `SSRuntimeTests.xctest/SSRuntimeTests` build
artifact and retain its exact path, not the app binary or a source SHA. Preserve build
and test logs and the pre-run binary hash. Never rebuild between capture and import.

Expected result: exactly **one passed test**, zero failures/skips/expected failures,
**six captures/eighteen images**, nineteen attachments with the exact V8 test identity,
loaded/fresh-built executable SHA agreement, nine full baseline RGBA matches, and all
semantic-plan/contact/authority checks. A zero-test result or successful build is not
capture evidence. Failed import leaves no native-capture output directory. Native and
visual failures must remain retained, not normalized away.

After import, coordinator must inspect actual images at all three zooms in both arms
and publish the bounded final scene for owner review. This worker does not recommend
source art or grant owner acceptance, production admission, merge or issue closure.
