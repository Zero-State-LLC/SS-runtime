# Whole-scene muted paving native trial

**Status: PAVING MATERIAL TRIAL. NOT ACCEPTANCE.** See [`../visual-acceptance-20261116/CONTRACT.md`](../visual-acceptance-20261116/CONTRACT.md).

## What changed

Both arms use the exact ground composition from the whole-scene diagnostic arm:
- asphalt bounds (800, 0, 1504, 1536) and (0, 0, 800, 600), tileUnits 128;
- the same curb and rail lines.

Only `BenchmarkReviewArt.paving` differs:
- **plaza:** `env_ground_plaza`.
- **muted:** `AppTests/WholeSceneAssets/whole-scene-muted-paving.png`.

Everything else is unchanged: the constrained building, Camera, props, HUD, Camera field (with `.paired` contrast) and outlines. The view is ORDINARY only, at zoom 1, 1.25 and 1.4, as native, half-size and grayscale PNGs: 18 plates. No production, renderer constant, input, collision, building replacement, shadow, HUD or field change.

## Paving source and provenance

- **Source:** `/Users/appliedalchemylabs/.jcode/generated-images/1794806293758-ig_0a14a4739e7f6a34016afa91ec2a2487d0a32bc6c445c7818d.png`. The generation metadata is retained as `source-metadata.json`: OpenAI image edit, quality medium, with the prompt recorded.
- **Bundled copy:** byte-exact, SHA256 `c0decdab226512a790ddecf49cf703c9fc736f7943f11bc364b76b111b7c3125`, 1254×1254. The test hashes the PNG loaded from the bundle and asserts this SHA.
- **Scale:** the production `WorldRenderer.groundTileUnits` stays 128. The authored 4×4 slabs therefore come out at 32 world units per slab. The constant was not changed.
- **Seam:** the opposite-edge RGB mean absolute difference is 12.90/255 left/right and 14.28/255 top/bottom. The tile is **NOT mathematically seamless**, and seam/repetition review is **pending**. `source-repeat-preview.html` shows a 2×2 CSS repeat without changing any source pixels.

## Runs (focused, fresh result bundles)

1. **attempts/01-hud-visible-assumption:** FAILED with 2 failures. My new assertion that every HUD node is visible was wrong, because the production HUD hides 3 nodes in this state. I replaced it with a recorded hidden-node census that must be identical across both arms. The test never sets `isHidden` itself.
2. **attempts/02-zero-tests-rejected:** the xcodebuild run returned "TEST SUCCEEDED" but executed **0 tests** (`totalTestCount` 0). It is **rejected** and kept only as history; the verifier rejects that summary.
3. **Valid run:** `-only-testing:SSRuntimeTests/WholeScenePavingTests/testMutedPavingVersusPlazaOrdinaryOnly` with result bundle `<scratch>/ss-wholescene-paving-20261116-0528.xcresult`. 1 test passed with 0 failures in 7.4 s, 05:27:44 to 05:28:17 UTC. `capture/` holds the 18 plates, records, summary, test tree, attachment manifest and log.

## Verification

- `verify_capture.py --exports <scratch>/ss-wholescene-paving-20261116-0528-exports --xcresult <same>.xcresult` → `VERIFIED_PROVENANCE_TRIAL_NOT_ACCEPTANCE`. It checks:
  - exactly 1 passing test with the expected identity, and that the retained summary and test tree match the bundle;
  - the bundled and generated paving SHA;
  - that the prior `WholeSceneBenchmarkTests.swift` (`93d9d99f…`) and all 36 prior plate bytes are unchanged;
  - 18 plates plus 1 record, byte-equal to the attachments;
  - exact paving provenance and open items, and the input-hash scope;
  - ordinary-only labels, roles and suffixes, a native size of 2112×978 (704×326 points at 3×), half at 1056×489, and true grayscale;
  - an identical HUD hidden-node census and identical upright roots across both arms;
  - that the arms differ at every zoom.
- `test_capture_evidence.py` → 7 of 7 tests passed offline, with no xcrun. They include the rejected zero-test summary and mutations of provenance, scope, census, labels, roots, prior evidence, attachments, and the CSS-only preview.
- **Unbound inputs, disclosed:** `env_ground_plaza`, `env_ground_asphalt` and the Camera candidate frame family are not hashed by this capture.

## Observation (not acceptance)

The muted paving reads grey instead of beige and is closer to the benchmark's ground palette. The building is still the saturated two-storey fallback, there are still no contact shadows, and the cone and HUD are still prominent. The slab scale and repetition need owner review at normal play scale.
