# BP-001 isolated reference-ground trial

November 16, 2026. Review-only evidence under SS-specs `intent/2026-11-16-reference-projection-trial.md`. Open `index.html` locally.

## Verdict

**Owner decision, November 16 at 01:39:04 UTC: midpoint selected.** The owner said "midpoint is good. continue". The canonical record is SS-specs `decisions.md`; execution scope is `intent/2026-11-16-midpoint-source-continuation.md`. This releases the projection-choice prerequisite for existing breadth-first source work, not art admission, merge or a partial shipping transform. The approved original concept remains the visual benchmark. No final zoom or numerical source-camera elevation was selected.

**Trial finding remains: the measured ground fit is not a faithful reconstruction of the approved reference.** The trial is useful because it exposes the mismatch rather than compensating with changed artwork or collision. The original pre-decision verdict selected neither candidate. The later owner choice does not erase the limitations below.

The reference fit uses approximately -29.755 degrees rotation and 1.018 ground y-scale. Midpoint uses +45 degrees and 0.5. The four fitting segments and two held-out segments, residual disagreement, endpoint sensitivity and axis conventions are in `landmarks.json` and `ground-fit.json`. These do not recover camera elevation, absolute world scale, translation or the perspective of upright artwork.

At the same focus and magnification, the reference-ground candidate moves the quiet-scene building toward the top-left and clips its canvas at all three zooms. Midpoint contains the building canvas at 1x and 1.25x but clips it at 1.4x. The building's baked perspective remains unchanged and is not registered anew to disguise disagreement with the new ground axes. Player source-alpha height occupies approximately 15.3%, 19.1% and 21.4% of viewport height at the three zooms in either mapping. These are unoccluded source occupancy estimates, not measured visible anatomy or human readability acceptance.

All six quiet-scene plates flag both luminance and chroma against the unchanged BP-011 bands. Five legal-encounter plates have no palette flags, while midpoint at 1.4x flags mean chroma 17.6 above 17. No flags is not whole-scene visual acceptance. Palette measurements exclude the top 240 native pixel rows, retain lower touch controls, use an uncropped reference and no zone allowance.

## Evidence

- Final focused native Debug xcresult: 3 passed, 0 failed, 0 skipped on iPhone 17 Pro simulator, iOS 26.5, Xcode 26.5. `capture-manifest.json` records the local bundle and full summary.
- 72 exact native attachments: two fixtures, two mappings, three zooms, natural/authoritative overlay and native/half/grayscale. Twelve metrics attachments plus one complete world-command record are retained.
- Native plates are 2112x978 pixels at 704x326 points, backing scale 3. Half derivatives are 1056x489. Grayscale channel equality is verified.
- Existing legal Ghost Step encounter remains tick 4976 and digest `d96494f03b4ade6a6a6dc02961ffd1dc73c5e1f2a86a029ca6dcd22d207162f5`. The first attempt placed the tick assertion before the existing GameScene first update, observing 4975. The final trial asserts 4976 after that update, matching prior capture timing and digest, not a substituted encounter.
- Identical authoritative commands replay to the same digest. Actual SpriteKit forward/inverse conversions exercise eight headings and four magnitudes. Analog inverse checks preserve input magnitude. No production inverse-input mapping was installed.
- Browser gallery: all 36 control combinations loaded both correct plates at expected dimensions with no load error. The approved image loaded at 1672x941. See `browser-verification.json`.
- Five reference-fit numerical regressions, five prior decision-packet regressions and four trial-verifier regressions passed during this turn. Native and browser evidence remains static review evidence, not physical acceptance.

## CI qualification

Final trial head `c1f9fb5106759ec19da9d8d82fc542de9846b394` passed all five jobs in run43784016529, fetched November16 at01:36:50UTC. Debug completed at01:36:46UTC. This is full remote-CI success, not completion of the twice-capped local unfiltered runs, physical acceptance or resolution of #237.

Historical published run 43779430334 at `01e9317` failed existing `testSharedProjectedPlayerTraversal` at `DisplayedPlaybackTests.swift:1184`: 15 observed poses versus 16 required. All other jobs passed. This revision predates the reference trial. Defect runtime #237 records the failure. The check is unchanged. A focused local reproduction passed 1/1 on November 16 at 01:00 UTC (`playback-defect-237.xcresult`, 19.814 seconds), so the CI failure was not reproduced locally and remains unresolved. A later green run cannot erase this intermittent observation. Do not describe the entire PR as passing based only on the focused trial suite.

## Reproduce

From the runtime repository, with the existing project environment and Pillow installed:

```sh
python3 -m unittest discover -s scripts -p 'test_reference_projection_fit.py'
python3 -m unittest discover -s scripts -p 'test_bp001_decision.py'
python3 -m unittest discover -s scripts -p 'test_reference_trial.py'
python3 scripts/verify_reference_trial.py
swift test
xcodegen generate
```

Focused capture command used:

```sh
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' \
  -configuration Debug CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES \
  SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT \
  -derivedDataPath "$JCODE_SCRATCH_DIR/ss-runtime-audit-derived" \
  -only-testing:SSRuntimeTests/ReferenceProjectionCaptureTests \
  -resultBundlePath "$JCODE_SCRATCH_DIR/ss-bp001-reference-trial-20261116/trial-debug-final.xcresult" test
```

Use a fresh result-bundle path when recapturing and a locally available simulator identifier. Export its attachments with `xcresulttool`, then run `verify_reference_trial.py --exports <directory> --xcresult <bundle>` to import only a successful complete focused suite. The verifier checks source hashes, unchanged approved reference, existing fixture/art hashes, identical legal digest, geometry metadata, image bytes/dimensions/grayscale and recomputed palette reports.

The frozen capture verifier's `ownerChoice: UNRECORDED` field describes the pre-decision capture checkpoint. It is not the current decision authority; the later owner selection above is recorded in SS-specs. Re-verification after the decision update passed all72 plate hashes,12 metric records and six capture-source hashes. The five decision-packet and four trial-verifier regressions also passed. Browser smoke checks confirmed the selected-midpoint banner, unchanged1672x941 reference and correct2112x978 quiet/legal natural pairs. The prior36-combination browser result remains historical, not a new full sweep.

## Reserved gates

The packet itself authorizes no change. The later owner decision selects midpoint and permits continuation under D-108, with new source samples remaining candidates. Production transform/input migration, collision change, depth-policy change, asset admission and merge are not completed or approved by the comparison. Preserve the 0.375s Player settle. Static comparisons do not validate live facings, occlusion, dense play, actual device performance or human acceptance. BP-005/BP-008/BP-009/BP-012 remain open where applicable.
