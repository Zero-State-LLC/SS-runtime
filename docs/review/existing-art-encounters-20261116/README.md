# Existing-art legal encounter diagnostic, slice9

## Authority and status

Accepted runtime `intent/2026-11-16-benchmark-faithful-scene.md`, owner authorization November16 05:56:35UTC, explicitly permits slice9 legal/dense encounters with existing supported art. No new approval is required for this bounded test-only implementation. Any new art, coherent-source acceptance or detailed family expansion remains gated.

- Current evidence: actual corrected0710 v2 independently validated, nine captures and1073 resources. Gallery ready at `capture-0710/gallery.html`. Exact native/runner provenance and limits in `IMPORT-0710.md`.
- Attempt0701 remains rejected old-schema evidence; exact relocated-bundle diagnosis is preserved in coordinator `attempts/02-0701-old-schema/LOADED-BUNDLE-DIAGNOSIS.md`.
- Attempt0649: native passed but framing inadequate. NOT visible encounter evidence, tracked in runtime#240. Preserved byte-for-byte under `attempts/01-stale-framing/`.
- Coordinator visual review: rejected original0649 framing. Corrected0710 awaits coordinator browser/image review and publication.
- Source fidelity: BLOCKED. Owner acceptance and production admission: NOT GRANTED.

## What the new test does

`AppTests/ExistingArtEncounterTests.swift` uses the existing seed1 `DebugAutopilot(scenario: "run", upgrade: .ghostStep)` legal command driver from `ReferenceProjectionCaptureTests.swift:139-200`. It starts a fresh `GameSession`, makes no scenario/test-state edits, and runs at most6000 normal steps or stops at terminal. The command attachment retains upgrade choices. Final public `GhostRun.replay` verifies the final digest. A second linear command replay verifies each captured prefix digest. Capture redraw must leave both digest and complete presentation snapshot unchanged.

The corrected v2 test explicitly stages the presentation camera at the actual snapshot Player center after redraw. This direct test-only position assignment does not step simulation and is NOT live camera-follow coverage. Each capture records actual Player/enemy/projectile snapshot positions, render-node names and scene roots, accumulated presentation bounds, ancestor visibility, crop bounds and computed intersections. Every plate requires the Player node/root/bounds included. The dense selector still requires two enemies within300×130 of Player, but now also requires an actual projectile within the704×326 Player-centered crop. Dense captures additionally assert two nearby enemy nodes and a projectile node included. Global Camera/combat counts remain global state metadata, not renamed visual coverage. Render bounds are presentation checks, never authoritative collision or targeting.

The original0649 test let Session.step advance gameplay without driving the camera-follow update. Its tick459 dense plate remained at the initial camera area, without Player or nearby enemies, despite globally valid encounter counts. Native success and hash validation did not prove framing. The new validator requires schema v2 and independently recomputes crop/root/bounds inclusion, rejecting schema v1 and stale/offscreen claims. See `FRAMING-CORRECTION.md` and preserved `attempts/01-stale-framing/`.

The test samples at most12 first-occurrence images across twelve categories: Camera integrity0/1/2/3, cameraDestroyed, playerDamaged, entityDied, nearby encounter, hostile projectile, mines, telegraphs and field clipping. Categories not reached are recorded as `notObserved`, never seeded to force coverage. Failure to reach the established nearby encounter remains red.

`GameScene.redrawBenchmarkPresentation()` renders the actual snapshot/HUD using existing production art, fog, authoritative field geometry and the existing production projection. No candidate artwork, hidden HUD, field removal, quiet composition or midpoint scene substitution is installed. This is a **production-projection control**, not the requested coherent midpoint scene. Camera field nodes are required absent when the actual snapshot says field-off. Captured Camera metadata includes whether each mount root is inside the crop. Global Camera state observations are not automatically on-screen art coverage.

Field occlusion means a query against the existing `CameraFieldGeometry.path` for an unedited actual Camera and actual solids. A sample on a ray toward an actual solid is inside the unclipped cone but outside the clipped cone. Both paths are diagnostic queries only, never written into a snapshot. This is presentation field-clipping evidence, not an independent authoritative line-of-sight implementation or a sprite-ordering proof.

Actual Camera state, clip/backing, enemies/reaction requests, mine arming/lifetime, projectiles, events and counts are retained. Clip backing is not proof that every authored animation pose was displayed. The paused view does not drive actual animation actions through all frames. Only selected captures ingest VFX events, so continuous effect lifetimes and attack animation timing are explicitly not covered. This packet cannot certify live cadence, physical performance, every attack, visual sprite occlusion or complete Camera transition animation.

## Resource and attachment binding

The test hashes actual runtime-resolved bytes for the full reachable eligible input inventory, plus three bundled catalog/presentation/clip contracts. The current independent source census contains1073 eligible resources. A development `RuntimeAssetBundle` source fallback makes the native assertion fail. The inventory is a superset, not proof of which resource was sampled by every pixel. No test-source self-attestation is claimed.

PNG attachments are emitted as exact data and hashed in the capture ledger. `verify_capture.py` checks one passing exact native test, rejects zero/skipped/expected-failure/wrong test runs, requires unique attachment identities, safe paths, command hash and replay boundary identity, exact reachable input census/paths/hashes, contract hashes, PNG decode/dimensions/bytes, capture state preservation and truthful observed/notObserved tags. Current source-resource bytes must match runtime bytes. A mismatch stays red, not waived. Replay execution itself is asserted natively; the portable validator does not independently run Swift gameplay.

Verification structure adapts the repository's established result-tree and exported attachment conventions, specifically `docs/review/player-ground-contact-20261116/verify_native.py:39-66`, without importing its fixed-time policy or fixture data. No legacy production source is copied.

## Coordinator-only focused native command, not run here

Coordinator must serialize the simulator slot and regenerate the project if the newly added test is not present. Existing project.yml already includes AppTests by directory. The worker made no project/CI edits.

```sh
xcodegen generate
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,id=84297C74-033E-408F-9622-D36BFF32F74E' \
  -configuration Debug CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES \
  SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT \
  -derivedDataPath /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-derived-20261116 \
  -resultBundlePath /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-20261116.xcresult \
  -only-testing:SSRuntimeTests/ExistingArtEncounterTests/testLegalPilotExistingArtEncounterEvidence test
xcrun xcresulttool export attachments \
  --path /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-20261116.xcresult \
  --output-path /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-exports-20261116
python3 docs/review/existing-art-encounters-20261116/verify_capture.py \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-exports-20261116 \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-20261116.xcresult
```

The UDID above is the existing available `SS QA SE 20261115` found through read-only `simctl list`, not a simulator boot request. Coordinator may substitute its serialized destination. Result paths must be unused; preserve any failed attempts rather than overwrite them.

## Static gallery for verified exports

`build_gallery.py` first checks the exact native result, exported attachment identities and the complete existing packet validator. It then embeds only ledger-listed, hash-checked PNG bytes into a self-contained HTML file. Every capture is labeled with its actual tick/tags, actual PNG dimensions and hash. Both native logical scene dimensions and half logical dimensions are shown, with a display-only grayscale toggle. Observed and notObserved categories and the prominent production-projection existing-art NOT coherent benchmark disclaimer remain visible. The gallery does not invent additional captures or constitute visual acceptance. Output creation is exclusive, so an existing gallery cannot be overwritten.

```sh
python3 docs/review/existing-art-encounters-20261116/build_gallery.py \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-exports-20261116 \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-20261116.xcresult \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-gallery-20261116.html
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s docs/review/existing-art-encounters-20261116 -p 'test_*.py' -v
```

At November16 06:52UTC all19 offline tests passed in0.520s, including five new synthetic gallery loader/output checks. `git diff --check` passed. No gallery from native evidence had been generated at that check. Subsequently encounter0649 was validated and rendered, recorded in `IMPORT-0649.md`. Swift remained frozen during this addition, with no native execution or new dependency.

At November16 07:04UTC23 offline tests passed in0.417s, including the real0701 rejection and original PNG hash checks. `git diff --check` passed. No corrected gallery was generated from rejected0701. Its12 original export files are separately retained byte-identically under `attempts/02-0701-old-schema/exports/`.

At November16 07:15UTC28 offline tests passed in1.084s, including five actual corrected0710 packet, dense-node, mutation, exact gallery and runner-load regressions. Corrected0710 native summary and attachments validate, gallery generated, original logs/diagnostics retained in `capture-0710/`. Both earlier attempts remain untouched. No worker native or Swift changes.

## Offline checks and limits

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s docs/review/existing-art-encounters-20261116 -p test_validator.py -v
xcrun swiftc -frontend -parse -D DEBUG AppTests/ExistingArtEncounterTests.swift
```

Final offline validation at November16 06:41UTC: all14 portable tests passed in0.323s, DEBUG Swift syntax parsing passed, and `git diff --check` passed. The final combined shell command returned1 only because the trailing search found no em dashes or stale test-count prose.

The portable mutations are synthetic reader tests, not native captures or legal-play outcomes. Source syntax parsing passes. Standalone typecheck against an existing derived module was attempted twice: first lacked the XCTest search path; the second found the ObjC framework but not the Swift assertion overlay (`cannot find XCTUnwrap/XCTAssertEqual in scope`). Those auxiliary invocations are NOT successful typechecks/builds. No further attempts at that cause were made. Coordinator's subsequent actual0710 focused Xcode test passed and its exact native identity, v2 packet and runner path were independently validated, see `IMPORT-0710.md`. No native test, unfiltered Swift retry, production/shared project/CI edit or commit was performed.
