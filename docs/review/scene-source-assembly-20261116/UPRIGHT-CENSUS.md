# Issue247: complete upright census, isolated review harness

Coordinator opened runtime issue247 before authorizing this repair at10:21 UTC. The1020 native test and old importer passed, but actual inspection exposed environment buildings incorrectly entering the ground projection. Technical success did not establish scene correctness. No test tolerance or gameplay assertion is weakened.

## Preserved attempt

`attempt-1020-before-upright-census/` contains byte-for-byte copies of the original Swift, native.py, assemble.py, tests, assembly, historical pending manifest, NATIVE.md, native-inputs and native-capture-1020. The originals of1020 capture and preparation remain in place for the gallery. `attempt-1020-sha256.txt` records every archive file. The archive is never repaired in place.

The retained old importer's `validate_records` still verifies historical1020 against its exact old prepared input. The new historical regression executes that entry point and compares every archived capture file with its original. The current importer rejects the same record for missing revision3 schema. The original native result and old verification are historical evidence of a real run with a known harness defect, not the corrected scene.

## Existing contracts, not new production behavior

ADAPT `AppTests/BenchmarkCaptureTests.swift:205-213`: enumerate `//environment-upright-*` in addition to actors. Classification comes from `App/EnvironmentTextures.swift:8-31`. Expected backed-solid cohort follows `App/WorldRenderer.swift:695-772`: exclude authoritative Camera mount solids, gates and the explicit review building replacement, then use existing `EnvironmentLibrary.solidAssetId` and `EnvironmentTextures.solidTexture`. No source art, production classification, collisions or fields are changed.

The harness independently inventories all existing environment sprites before extraction. Expected names must be nonempty and exactly match the backed authoritative cohort. It records every original name, world root, size, anchor, local scale, rotation, visibility and alpha. A second enumeration supplies extraction and must match that inventory exactly. All original nodes are retained, reparented for capture, then restored. No surrounding art is hidden, removed from the composition, resized or re-rooted.

Every extracted upright, including environment, records its actual projected root and two measured local-unit basis vectors in scene coordinates. Native assertions check midpoint/zoom roots and axis-aligned uniform scale. Importer requires the exact ordered census, unique names, nonempty expected cohort, matching independent inventory, original sizes/anchors/scales, axis-aligned measured bases and unchanged inventories across zooms and both arms. It checks all actors rather than merely five or at least five. The exact24-solid census, Camera field path, authority digest, HUD and controls remain asserted.

## Version boundary

- Fixture: `source-scene-continuation-003-upright-census`.
- Prepared input schema: `source-scene-native-003`.
- Records schema: `source-scene-records-003`.
- New preparation directory: `native-inputs-v3/`. Old `native-inputs/` is not overwritten.
- Still six ordinary records and18images at zooms1,1.25,1.4. No animated family claim.

Synthetic mutations exercise omitted, duplicate, empty, wrong-name and wrong-count cohorts; missing independent fields; root/size/anchor/scale drift; stale inventories across zoom/arm; hidden/rotated/transparent nodes; and ground-warped basis vectors. Synthetic images/records remain mechanics-only and never acceptance evidence.

## Validation and next action

Initial revision3 run:58portable tests passed6.458s and Swift frontend parsing passed with DEBUG+SS_SOURCE_SCENE_REVIEW. `tests-upright-census-initial.log` retains the output. Final validation at10:25 UTC: **58 tests passed in11.479s** (`tests-upright-census-final.log`), both Swift frontend parse modes passed (DEBUG with and without SS_SOURCE_SCENE_REVIEW), and fresh `native-inputs-v3` preparation succeeded. Harness source SHA256 `f8b1e61dc81ee72e6e787ae604f23b0bae20eed63e33ec10e6ee6e0488b0bf86`; prepared JSON SHA256 `514fefe24bd06cc2a6439052e7e568b93f0e96a70d0a6dece604e2ddaa00fedc`. These are source/preparation hashes, not loaded native executable evidence. `preparation-upright-v3.json` retains the receipt. Native execution and visual validation remain coordinator-owned after code review. `NATIVE.md` has the focused1026 command and import command, selecting only `testQuietSouthNeutralOrdinaryScene`. Do not rerun prepare over an existing preparation directory. No production/CI edits, commits, pushes or native runs were made by this worker.
