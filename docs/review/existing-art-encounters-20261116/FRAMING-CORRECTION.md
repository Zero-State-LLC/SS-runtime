# runtime#240 staged framing correction

Current outcome: actual0710 schema v2 packet and exact loaded-runner provenance independently validated. See `IMPORT-0710.md` and `capture-0710/gallery.html`. Coordinator visual review/publication remains pending, #240 remains open, and this is staged follow rather than live camera-follow. The implementation and preparation chronology below is historical.

## Proven defect and retained attempt

Coordinator reviewed actual encounter0649 tick459 PNG and found the initial camera area without Player or nearby enemies. The test advanced authoritative gameplay through `session.step()` but only redrew presentation, never running the GameScene camera-follow update. That camera remained stale. The globally valid nearby/combat counts were not visible encounter proof. Original native success is retained as passing-but-inadequate, not relabeled visual success.

`attempts/01-stale-framing/` preserves the executed source, original validator/gallery builder/import notes and all12 exported files, including nine original PNGs and manifest. Worker compared every exported file byte-for-byte against the exact original exports at November16 07:00UTC: all12 identical. Executed Swift SHA256 `999fa702ca61dfa4a1523d4f8c0444a2407875763d900ac47566bf517a889a37`. Original xcresult and original gallery remain at their scratch paths in `IMPORT-0649.md`. No image bytes were rewritten.

## Narrow correction

Only the test changes. After rendering the unedited authoritative snapshot, set the existing scene camera directly to the actual snapshot Player position and unit scale. This is explicitly **staged snapshot follow, NOT live camera-follow**. There is no GameScene.update call, simulation update or production hook change. Existing shipping art, projection, inputs and replay remain unchanged.

At every capture record actual Player, enemy and projectile scene-node names, exact snapshot/root positions, accumulated presentation bounds, ancestor visibility and crop intersection results. Assert all roots agree with snapshot coordinates. Require Player included in every crop. Dense selection retains two enemies within300×130 but additionally requires a projectile inside the704×326 Player-centered crop, then asserts at least two nearby enemy nodes and a projectile node are included. Global state tags remain global, not proof that every tagged Camera/mine/effect is visible. Node inclusion is not pixel visibility or occlusion proof.

Portable schema v2 validator independently recalculates centered camera/crop, render-node census/identities/coordinates, bounds intersections and dense inclusion. It rejects stale center, offscreen crop, missing/hidden nodes and falsely reported inclusion. Old v1 actual0649 is rejected, not grandfathered.

## Validation and coordination

At November16 06:59UTC22 offline tests passed in0.443s, DEBUG Swift syntax parsing passed and `git diff --check` passed. Actual retained-attempt regression verified original PNG hashes and rejects v1. Current Swift SHA256 `30def02cb69cd49acf7a990ac742bd72fce525bca748999ec465df513b09a5fc`.

The framing patch was applied06:58:39 through06:58:51 under coordinator06:57:29 authorization, before the06:58:51 freeze message arrived. Worker immediately notified coordinator and froze further Swift edits. No simulator or native build was started by worker. Fresh native typing/integration/captures remain unverified pending coordinator execution. No commits.

Focused fresh native command for coordinator after serialized slot release:

```sh
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,id=84297C74-033E-408F-9622-D36BFF32F74E' \
  -configuration Debug CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES \
  SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT \
  -derivedDataPath /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-derived-20261116-0700 \
  -resultBundlePath /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-20261116-0700.xcresult \
  -only-testing:SSRuntimeTests/ExistingArtEncounterTests/testLegalPilotExistingArtEncounterEvidence test
```

Use unused paths and the coordinator's serialized destination. This command is prepared, NOT run. Source fidelity remains BLOCKED, acceptance/admission NOT_GRANTED regardless of framing outcome.
