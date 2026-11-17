# Native kiosk geometry comparison verdict

2026-11-17 02:43UTC. Implementing worker inspection, not independent coordinator acceptance. BP-001/007/012, T1045.

**Native integration verified for the two frozen flat kiosk arms. Overall benchmark NOT MET.** The next production step is a separately recorded textured candidate and actual playable-runtime integration, not accepting this diagnostic flat material as finished art. Preserve this comparison and all prior source/evidence bytes.

## Actual execution

Fresh `native/derived` build succeeded at02:40UTC. Exactly `KioskOnlyGeometrySceneTests/testQuietSouthNeutralOrdinaryScene()` passed at02:41:47UTC: one test, zero failures,14.431seconds. No skip, fallback, simulator restart, erased device or second native attempt. The simulator slot was released to the coordinator after strict import at02:42UTC.

The strict importer and subsequent retained checker both verified six captures/eighteen images, all frozen V9 source/authority metadata, non-kiosk actor records, full footprint/contact correspondence, joint depth order, control layout and framing. Same-zoom pixels outside the union of kiosk canvases plus a two-native-pixel filtering margin match exactly at all three zooms. All pairs differ within the kiosk region. The rectangular mask is conservative, so this is not an alpha-exact proof of every background pixel inside those rectangles.

| Identity | SHA256 |
|---|---|
| Fresh-built and actually loaded test executable | `45d02db24f86d132536e2bd46ff2b9b63d82bcd8817a21e9f90b77135ac8efff` |
| Harness source | `80167c20a3ab797f5790b4f516784c627ee985fdf0b3c1030100ff76a575a5c5` |
| Prepared input | `861901fd95e626f8b4b5f4784255294b2247bbb7256131641cac9567f75e4edb` |
| Actual native records | `08e462e5053b93bcc4106d42977ab17ab9428d46385939cc7263c6a90b5cebf1` |
| Verification receipt binding all retained outputs | `5927f5eb49299e12372dd34acd1ab149f520cc2ff64c7e468748caaa317b8408` |
| Full original benchmark | `d8c174a44d480ba4d67ac3b3280134dc602a12a85e41d3aa0827479f3068d7f3` |

Actual source images and their individual SHA256 values are bound by `capture-01/source-scene-records.json` and `capture-01/verification.json`. Native images are2112x978, half-size views1056x489. The original benchmark remains1672x941 and was inspected uncropped.

## Visible inspection

Opened all six actual `capture-01/source-scene-{control,candidate}-ordinary-z{100,125,140}-half.png` images directly and the original full benchmark. No synthetic sheet was substituted for native inspection. Native-resolution and grayscale variants were validated and retained, not separately visually reviewed by this worker.

- At zoom1, the proposed kiosk has a visibly thinner crown and lower silhouette against the unchanged north frontage. The Camera and Player retain their previous positions, scale and appearance. Its doorway starts lower relative to the Camera head, while the broad plan remains conspicuous.
- At zoom1.25, the same improvement is visible without any change to neighboring buildings. The rectangular facade openings, plain roof and large pale facade remain obviously diagnostic rather than benchmark-quality surfaces.
- At zoom1.4, the tall control roof extends beyond the upper image edge. The lower candidate roof fits below the top edge, while the visible HUD remains superimposed in its unchanged native positions. This is a visible framing difference caused by the intended silhouette change, not an altered camera or viewport.
- In every candidate, the lower crown reduces the tower-like reading but does not establish that the reported geometry/spacing defect is solved. Horizontal width, chamfer, adjacent northern-building contact, Camera clearance and Player distance are deliberately unchanged.
- The blocked base still reads as a small raised landing or step. The thin horizontal entry marks and plain lower mass reinforce that ambiguity. This comparison makes no additional curb/base correction.
- Relative to the full benchmark, flat material, missing roof-vent detail, simplified facade relief, clean paving repetition, reduced material wear and the stationary Player silhouette remain major deficits. Those are not accepted merely because native contact/authority checks pass.

## Validation and retained failures

- 15 adapter regressions passed at02:41UTC,39.048seconds. These include synthetic schema/authority/path negatives and are not themselves capture evidence.
- 7 retained-evidence tests passed at02:42UTC,4.085seconds, using disposable copies of the actual capture. Modified/missing/unlisted images, forged acceptance, aliased receipt and recataloged actor mutation are rejected.
- 8 focused Swift contract tests passed at02:38UTC using `--skip-build` with the earlier owned package build. This is a current execution of existing core test products, not a rebuild or proof of UIKit/SpriteKit compilation. The separate fresh Xcode build and actual native test establish that boundary.
- Production-source `git diff --exit-code -- App Sources Tests project.yml SPEC_BASELINE.md` returned0 at02:43UTC. No production renderer or package source was changed by this native lane.

No compiler, native test or importer assertion failed. The first build tool submission was refused before execution because computed log redirection targets required explicit justification, then the exact command was authorized against the three new owned log paths. A120second background watchdog fired because build output was redirected, but the build log was actively progressing and completed149seconds after launch. Existing no-throw `try`, audio converter, accessibility duplicate-class and no-drawable warnings remain in raw logs. They were not silently removed or promoted into failures or success evidence.

## Handoff

The coordinator can inspect the native pair without another simulator run using `native/retained.py`. Use the already delivered `../editable/candidate-indexed-mesh.json` as the unchanged geometry basis for a new textured packet. Do not overwrite the flat source PNGs, prepared input or capture. Any textured output needs its own source/material/registration closure and native evidence. The geometry decision remains a review candidate, not owner acceptance. No production admission, merge, release, deployment, changed collision/Camera authority or physical-device certification is claimed.
