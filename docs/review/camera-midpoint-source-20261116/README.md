# Municipal Camera midpoint source, FIRST SAMPLE (slice 6)

## Owner rejection, November16 04:22:37UTC

Owner: “this does not match benchmark.” The latest Camera sample is rejected for fidelity. The earlier attempt02 recommendation below is withdrawn. The fixed `street-corner-approved-concept.png` remains the benchmark; selecting a midpoint ground transform did not authorize substituting the alternate midpoint concept as source authority. Preserve attempts01/02 as rejected comparison history. Only first-sample correction against the original approved benchmark may continue. No states, clips or production admission follow from the passing source tests.

## Independent technical review before owner rejection, November16 04:22UTC

Open `index.html` for actual64×96 and32×48 source previews and grayscale controls. Coordinator verified all5images loaded in Brave, exact CSS sizes, grayscale on/off and no horizontal overflow. All10 strengthened source guards pass with ResourceWarnings treated as errors. They now verify the exact full pinned contract bytes in `source/clip-metadata-001.json`, the census subset's keyed clip identities, complete attempt02 transform reconstruction and layer hashes. CI also compares the copied full contract directly to the unchanged runtime bundle.

Before the owner rejection, the coordinator recommended attempt02 for review based on its concept extraction. That recommendation is withdrawn: matching the alternate midpoint concept did not establish fidelity to the unchanged approved benchmark. Leaf-contaminated base edges, baked scene illumination, contour quality, missing hidden underpaint and concept-to-Player scale also remain unresolved. Do not expand states/clips or substitute this intact frame for missing states. No native renderer, live cadence or device evidence is claimed.

Status: `FIRST_SAMPLE_PROPOSED_NOT_ADMISSION`. Authorized by coordinator stallion at 2026-11-16 04:06 UTC under the owner's ten-slice authorization (FACTS 03:10:28 UTC) and the D-108 midpoint selection. This packet is source-only. It makes no production, runtime, catalog, shared-file or commit change.

## What it is

`camera-midpoint-intact.png` is an editable, complete municipal Camera (Integrity 3, intact) on the existing 256 x 384 texture, 64 x 96 logical canvas, with the ground anchor at (32,88) = pixel (128,352). `build.py` splits it into five layers that do not overlap: `base`, `pole` (finial, shaft and collars), `junction_box`, `arm` and `head`. Stacked in that order, they reproduce the source image exactly (RGBA, with transparent pixels' RGB ignored; see the equality note in `source-record.json`). The head polygon is reused verbatim from `camera-shared-source`.

## Provenance (honest label)

- Pixels: `camera-shared-source/intact.png` (sha `aa437f0e…`), copied to `source/recovered-intact.png`.
- Origin: the `camera-state-study` built-in image_gen sheet, with alpha cleanup and registration. That study was a **CAPTURED candidate and was never accepted**. Label: `GENERATED_PRIOR_CANDIDATE_RECOVERED_NOT_ORIGINAL_MASTER`. It is reused as the starting point, not treated as accepted art.
- Benchmark: the SS-specs `phase4/street-corner-approved-concept.png` and `street-corner-midpoint-concept.png` are copied unchanged, with their hashes recorded. The specs checkout is at `a54b87f`. The runtime base is `9a4b7a7`.
- No image generation, repainting, warping or resampling of the source pixels. Review plates are resized previews only.

## Review plates (`review/`)

- `benchmark-comparison.png`: approved concept crop, midpoint concept crop and this sample at matched height.
- `native-half-grayscale.png`: native 64x96 and half 32x48 (both shown at 3x), plus the grayscale of each. The ground anchor is marked.
- `layers-annotated.png`: layer polygons and the anchor at 2x.

## Measured facts (not thresholds)

- Opaque height is 313 px (rows 39-351). The last opaque base row is 351, directly above the anchor row 352.
- The widest part of the base is 82 px, over rows 296-327. The head spans 154 opaque columns, combined over rows 150-214.
- Opaque pixels per layer: base 5,591, pole 8,447, junction box 1,756, arm 5,562, head 5,812.

## Fidelity limitations (observed)

- **Viewpoint:** the sample's base ellipse and dome underside read as a slightly lower, more frontal elevation than the midpoint concept, which shows more of the top of the base and the cap. Uniform transforms cannot change this. A true midpoint view needs new or repainted source, which is a design or source gate for review.
- **Proportion:** compared with both concepts, the sample's dome and arm are larger relative to pole height, and the pole is shorter and thicker. The concepts have a longer shaft with an extra collar.
- **Material:** the sample is cleaner and smoother than the concept's worn cast metal. There is no ground contact shading and no leaf debris. Those belong to the environment, not the device.
- **Half scale:** the cyan indicator and arm still read. The junction box becomes a two-pixel blob.
- **Grayscale:** the ivory head separates from the dark pole. The indicator disappears, which is acceptable because state must not depend on colour.
- **Layers:** there is no hidden underpaint behind the arm or head, so moving a layer would expose holes. The polygons are visual boundaries, not collision, targeting or field geometry.
- **Not done:** Damaged, Critical and Destroyed states, the six clips and their 16 frame slots were not re-authored here. The Integrity 3/2/1/0 and six-clip requirements are recorded in `source-record.json` as preserved requirements. The existing `camera-clips` packet is unchanged. There is no real-renderer, native-device or encounter evidence.

## Frame-count discrepancy (reported, contract unchanged)

The ten-slice intent (`SS-specs intent/2026-11-16-grounded-motion-ten-slices.md:18`) says "existing six clips, 17 frames". The contracts say 16:

- The pinned SS-specs `b1ed874` `contracts/clip-metadata-001.json` has 6 camera clips: operational_idle 4, hit 2, critical_enter 3, destroy 4, field_off 1, destroyed_idle 2 = **16** frame IDs.
- The runtime copy at `Sources/SurveillanceCore/Resources/contracts/clip-metadata-001.json:2390-2518` has the same 16 `actor_camera_*` frame IDs. `asset-catalog-001.json` has 32 `actor_camera_` lines, which are 16 assets each matched by the "assetId" and "runtimePath" patterns.
- `Sources/SurveillanceCore/Presentation/ClipMetadata.swift:79` and `AppTests/CameraPlaybackTests.swift:100-103` enforce the same per-clip counts.
- BP-004 (`benchmark-production.md:94`) lists 4/2/3/4/1/2, which also totals 16. `camera-clips/clips.json` exports 16.

The "17" in the intent matches no contract or code. It may count the 4 settled stills plus 13 transitions, or it may be a typo. Correcting it belongs to SS-specs, so it is not changed here.

## Attempt 02: extracted from the fixed midpoint concept (proposal)

`attempts/02-midpoint-concept-extraction/`, built by `build_attempt02.py`. Attempt 01 (top-level files) is kept unchanged as the control.

- Pixels are an exact crop of `street-corner-midpoint-concept.png` at (880,60)-(1080,420). The alpha is a deterministic silhouette: dark and ivory outline walls, closed, filled, then the largest component kept. Every opaque cutout pixel equals the concept RGB, and a guard checks this.
- One uniform Lanczos scale of 0.934 makes the device the same 313 px height as attempt 01, so the world draw size is unchanged. A translation puts the base centre (concept 947,401) at pixel (128,351), just above the anchor row 352. There is no flattening, repainting or generation. Label: `EXTRACTED_FROM_APPROVED_MIDPOINT_CONCEPT_NOT_GENERATED_NOT_ORIGINAL_MASTER`.
- Result: the concept's elevation and proportions carry over. The shaft is longer and slimmer, with an extra collar. The dome is smaller, and the top of the base is visible. It has 5 non-overlapping layers.
- `review/three-way.png` shows the midpoint concept, attempt 01 and attempt 02 side by side. `review/native-half-grayscale.png` shows both attempts at native, half and grayscale.

Attempt 02 limitations:

- Lighting and worn texture are baked in from the scene.
- 81 leaf- or orange-coloured pixels remain at the base edge (y >= 300). The mask edge carries some pavement tint, and the outline is softer than attempt 01's inked contour.
- There is no underpaint, and the head and arm are smaller at half scale.
- Damaged, Critical and Destroyed states cannot be extracted, because the concept shows only the intact device. Those states will need new paint aligned to this geometry. That is the next source step after fidelity review. This conservative path did not need image generation, so nothing is blocked.

## Reproduce

```sh
PY=/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python
cd docs/review/camera-midpoint-source-20261116
"$PY" -B build.py && "$PY" -B test_source.py
```

Six guards pass (`tests.log`). They cover immutable input hashes, the honest label, registration and anchor, an exact non-overlapping layer reconstruction, all five device layers present, and the preserved six-clip and Integrity 3/2/1/0 contract.

## Review verdict (worker): WITHDRAWN at 04:22:37 UTC

~~Recommend attempt 02 as the next owner-review sample.~~ Withdrawn after the owner's rejection. **Attempt 01 is REJECTED** because it is a recovered generated candidate with the wrong proportions. **Attempt 02 is REJECTED** because it used the midpoint concept as substitute authority. Both are kept as comparison history. The notes below describe them as they were before the rejection.

## Attempt 03: from the FIXED APPROVED concept (for direct inspection, not accepted)

`attempts/03-approved-concept-extraction/`, built by `build_attempt03.py`. The only authority is `source/approved-concept.png`. The midpoint selection is a ground transform plus upright registration. It does not change the source viewpoint, proportions or materials.

- Pixels are an exact RGB crop of the approved concept at (880,20)-(1060,470), with the same deterministic contour-fill alpha used before. One uniform Lanczos scale of 0.7524 maps the device's 416 concept rows onto the target rows 39-351. Measured after resampling: rows 38-351 at alpha > 128, and 36-353 at any alpha (Lanczos edge spill). Nothing above alpha 128 lies on or below anchor row 352. The approved original is pinned in both the build and the tests at sha256 `49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb`. The base centre (concept 932,446) sits on anchor px (128,352). There is no generation, repaint or non-uniform scale.
- **Direct comparison:** `review/benchmark-same-scale.png` shows the approved concept crop put through the identical scale and placement, then the proposal, then a magenta contamination map. `review/benchmark-native-64x96-3x.png` shows the same panels at native size. `review/native-half-grayscale.png` shows native, half and grayscale views.
- Concept measurements: the pole is 37 px wide at y260, the base is 83 px wide at y420, and the device is 416 px tall. The pole is long and slim, with the finial, top, mid and lower collars and the stepped base. Head, arm and junction box ratios are the concept's own, because only one uniform scale was applied.
- **Contamination (shown, not hidden):** 4 leaf-coloured pixels and 107 pavement-grey pixels lie within 3 px of the silhouette edge in the output. The grey count may include edge metal highlights. A dark leaf fleck remains at the lower-left base edge.
- Remaining gaps:
  - The concept's lighting and wear are baked in.
  - At the 0.75x downscale the outline reads thinner than in the concept.
  - There is no underpaint and no layer split.
  - It is intact only. States and clips stay blocked.

I do not claim it matches the benchmark. It is a faithful extraction for owner inspection. 17/17 guards pass with `-W error::ResourceWarning`, both in place and from a relocated copy. The tests independently recompute the contamination counts and the measured rows. The root `source-record.json` (attempt 01) and the attempt 02 record now carry REJECTED statuses.

## Superseded notes (pre-rejection)

Open fidelity gates before any state or clip expansion:

- Leaf contamination at the base edge (81 px).
- Baked scene lighting.
- A softer contour than the inked control.
- No underpaint behind the arm and head.

Damaged, Critical and Destroyed states and the 16 clip frames stay **blocked** until fidelity review.

Tests are portable. `test_source.py` reads only files copied into `source/` and the attempt folders: the concepts, the recovered states and `camera-clip-contract.json` copied from the runtime contract. It passes 10/10 from a relocated copy with `-W error::ResourceWarning`. Only `build.py` needs the sibling inputs, and it needs them only for regeneration.
