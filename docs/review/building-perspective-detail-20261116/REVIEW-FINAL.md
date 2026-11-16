# Final bounded building scene review, November 16 22:41 UTC

## Verdict

**Building perspective/detail improved. Overall benchmark still NOT MET. Owner scene review required before further aesthetic, motion or encounter work.** No production admission, merge, issue closure or physical-device certification.

Open `gallery/index.html` through the local review server. V7 is the default and fails closed if evidence is absent or corrupt. It compares a fresh v6-style baseline with the building-only candidate. Earlier v6 remains selectable and immutable. The original benchmark is displayed uncropped with its aspect ratio preserved.

## Actual visual inspection

Coordinator inspected actual v7 candidate native images at zoom1 and1.4, actual baseline at zoom1, the full immutable1672x941 benchmark, and actual source native/half exports. Actual browser exercised every version/zoom/arm/size/grayscale combination.

- Context buildings now have consistent roof axes, wall depth, and explicit footprint contact instead of stretched padded sprites. The left residential facade and rear civic facade fill their authoritative plots rather than leaving dark unused foundation rectangles.
- Kiosk parapet, window returns, entry depth and stair treads are clearer. The kiosk still uses the original D108 basis, not a replacement camera transform.
- Camera remains visibly in front of the kiosk and Player remains visible with no obvious pale outline in inspected captures. Measured actor canvases are inside crop and outside all three actual visible controls at all three zooms, in both arms. The new neighboring masses occupy substantially more of the scene, including behind HUD controls, which is not a claim of ideal composition.
- Remaining deficiencies: repetitive window bays and roof wear, oversized-feeling contextual masses, simplified civic identity, flat/clean paving and roads, mixed treatment of the existing tree and props, weak contact/shadow depth, and the stationary Player silhouette differ from the benchmark. Source editability does not erase those differences. The tree appears poorly grounded against the new rear facade, an unchanged prop/layout limitation now more apparent.
- Some architectural relief and weathering remain baked, hidden surfaces reuse visible materials, and the kiosk vent remains a registered2.5D raster. This is not a complete 3D asset family or animated scene.

No third source correction or further scene aesthetic retry was made after this final comparison.

## Verified evidence

Actual native run `scene/native-run-2237.log`, result bundle `/Users/appliedalchemylabs/.jcode/scratch/building-perspective-native-2237.xcresult`: exactly one passed test, zero failures. Importer requires six captures, eighteen PNGs, nineteen unique exported attachments and exact selected test identity. Imported packet is `scene/native-capture-v7/`.

Actual loaded executable SHA256 `2ab2c18e4aa4ea18e488d242c716e67a8dd8af6655aa325248b08e0ca827024b` matches the fresh build executable, independently rehashed at22:39. Frozen Swift source hash is separately `92cf6adf3ebee3ddd970cda799b19fcffee190c1b5fd998f02f176f4dd403e01`, not binary attestation.

All nine fresh baseline images (native, half and grayscale at1/1.25/1.4) have exactly equal RGBA pixels to immutable v6 candidate images. See `verify_baseline.py` and `baseline-pixels-2241.json`. No old evidence was rewritten.

The strict binder/retained checks preserve all24solids, roots, Camera field, view center[684,724], controls, geometry-derived depths, non-building sources and18uprights. Five explicit building-source corner registrations agree with actual projected authoritative footprints. The kiosk chamfer's omitted corner is honestly labeled a virtual authoritative footprint corner, not a visible mesh vertex.

Independent coordinator checks:13kiosk tests,11context tests,41scene importer/retained regressions. Both Node suites passed with actual v7 evidence required,36retained images and53rejected metadata mutations. Actual Brave passed72control selections/96image displays, exact704x326 or352x163CSS sizing, grayscale restoration, full benchmark aspect and no page overflow. `gallery/browser-final-2239.json` distinguishes this from structural tests.

## Retained problems and boundaries

Compaction interrupted the final roof correction workflow. The first recovery test correctly failed against stale outputs. `context/coordinator-tests-2233.log` and the withdrawn premature review remain recorded. Executing the already-written bounded correction and replay, then re-inspecting the actual new images, passed all11unchanged strict checks. No acceptance threshold was weakened.

Jev's decision service returned401. Direct actions in the same actual browser tab completed verification. Initial probe had unsupported top-level await and failed before action; its corrected promise-return probe produced the recorded outcome.

Issue251 records inherited v5/v6 retained export-manifest semantic coverage. V7 checks exact attachment/test identities independently. Older evidence and validators remain unchanged, and the issue remains open. Prior issues and source/device/merge gates remain unchanged. No unfiltered Swift retry or automatic CI polling chain.
