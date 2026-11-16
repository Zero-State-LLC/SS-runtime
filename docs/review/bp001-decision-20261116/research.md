# BP-001 research: preserve the visual benchmark, compare renderer choices

Researched November 16, 2026. Owner instruction: **research for the decision; the visual benchmark stays.** This is a research recommendation, not a projection decision, new acceptance threshold, art admission or implementation authorization.

## Recommendation

**Do not select midpoint from the existing A/B alone. Prepare a reference-calibrated original-reference renderer trial, then compare it with midpoint against the unchanged approved concept.** Keep midpoint as the useful engineering comparator, not a replacement visual benchmark. This supersedes this packet's earlier recommendation to select midpoint as the source-work basis now.

Why: A is shipping ground mapping, not a faithful original-reference candidate. B demonstrates a more coherent relationship between the present building and paving in a still, but that does not establish fidelity to the approved image. The canonical BP-001 explicitly asks for original-reference and midpoint candidates. Neither technical documentation nor the current capture closes that missing comparison.

## What stays fixed

- The approved `street-corner-approved-concept.png`, its identity and the Civic Seam direction remain the artistic target. The separate midpoint concept is an illustration of an alternative, not a newly approved benchmark.
- Preserve the hooded Player, complete municipal Camera, architectural/material richness, muted weathered street palette, apparent scale relationships, lighting coherence and ground contact. These are visual-review criteria, not newly invented numeric pass bands.
- Preserve the actual 704×326-point gameplay viewport, HUD, authoritative geometry and existing gameplay. Capture pixels and backing scale remain separately reported.
- Preserve Player settle timing at 0.375 seconds and the breadth-first delivery order. No source detail, new facing, source repaint, arena change or production migration is authorized by this research.

Local authority: SS-specs `benchmark-production.md:39–55` (shared sample), `:108–118` (framing/registration), `:132–166` (fixed palette reference and owner gate), `:305–328` (facing/input). These are repository requirements, not conclusions attributed to external sources.

## Separate the four problems

| Problem | What must be demonstrated | What does not solve it |
|---|---|---|
| Ground projection | One forward/inverse mapping for ground geometry, fields, paths and object roots | Rotating only an overlay or adjusting collision to fit a picture |
| Upright source viewpoint | Anatomical facings, building wall contact and pole roots agree with the chosen view | Squashing or rotating the entire elevated sprite |
| Framing and visibility | Player/building/Camera proportions and threat visibility at the same viewport | Larger texture files, or zoom chosen solely to enlarge the Player |
| Fidelity | Palette, materials, architecture, lighting and readable authored detail against the approved concept | Passing a matrix test or choosing whichever current candidate is less broken |

Apple documents that parent scale and rotation propagate through drawing and coordinate conversion [S1, S2]. **Engineering inference:** projecting the whole finished scene also deforms already elevated art. Keep upright art separate and attach its contact root to the projected ground. The current comparison already does this for its named billboards. Tiled independently separates projected object geometry from image alignment [S5]. These sources support a mechanism, not a preferred SS angle.

## What the evidence actually says

**Observed in this packet:** quiet A and B use the same candidate art and differ in mapping. A shows upright elevated architecture on axis-aligned paving. B makes paving and building orientation read more consistently. Both remain visually different from the approved image in composition, materials, scale relationships and colour. That is a qualitative review observation, not a measured fidelity score.

**Measured, existing palette report:** approved reference luminance/chroma are **85.2 / 11.4**. Quiet A is **126.8 / 25.2**, quiet B **127.2 / 25.7**. Both are flagged by the existing proposed bands. Encounter A **94.4 / 12.8** and B **99.3 / 16.0** fall within them. The runtime samples omit the documented upper HUD strip, the reference is uncropped, and lower controls remain. Composition influences the result. The numbers do not isolate material colour or establish acceptance. Midpoint does not repair the quiet-scene palette drift.

**Measured transform, not recovered reference camera:** `AppTests/BenchmarkCaptureTests.swift:1023–1147` applies +45° rotation and 0.5 vertical scale to ground, keeping named billboards upright. That matrix was selected as an experiment. There is no measured fit establishing that it reproduces the approved concept.

**Earlier analytic evidence, not a fresh capture:** `../projection-guide/review.md` derives a 128×128 world obstacle's projected bounding box of about **181.02×90.51**, half the ground area. At unchanged 704×326 framing the inverse viewport covers **459,008** world square units rather than **229,504**, ignoring boundaries and occlusion. This is not a count of visible threats. A √2 zoom restores area only, not shape, facing or visibility. `../resolution-budget/review.md` likewise shows the historical building alpha height rising from **63.5% to 89.8%** at √2 zoom. Those older assets and settings are not a measurement of today's painted Player.

**Unproved:** a faithful original-reference candidate, live eight-direction input/facing integration, dense legal-encounter visibility, front/rear/corner depth behavior, device performance and owner acceptance. Existing transform assertions are not a complete playable migration.

## Why no exact camera angle is prescribed

The approved concept is a raster illustration, not a supplied calibrated scene. OpenCV's camera-pose example requires planar correspondences and known camera intrinsics [S6]. **Inference for this task:** a plausible ground fit does not recover hidden wall vertices, unique camera settings, upright anatomy or artist intent. Do not invent an exact elevation from a roof edge or call the midpoint's 45° a measured reference angle.

Start with visible ground-plane directions and contact landmarks. Record the selected points, assumptions, residual disagreement and uncertainty. Fit a simple affine/orthographic-like ground model first. If consistent reference landmarks cannot fit that model, report the mismatch before proposing perspective or a larger renderer change. Do not warp the reference until it agrees with the candidate. No new package, 3D engine or Tiled/OpenCV adoption is recommended here.

## Smallest discriminating trial, proposed only

1. **Freeze inputs.** Record the approved image hash, current source hashes, viewport, fixture identity and capture settings. Keep the full reference visible at its original aspect ratio. The reference is 1672×941, while gameplay is 704×326, so never stretch one to match the other. Any diagnostic region of interest must be named, shown alongside the full reference and identical across comparisons.
2. **Calibrate the missing A-reference candidate.** Use labeled ground contacts and ground-axis landmarks, not roof bounds or arbitrary sprite rectangles. Keep wall contact, walkable apron and hidden/unknown geometry separate. Record the fitted mapping and remaining discrepancies. Use existing art and neutral diagnostic geometry where needed, without generating further family source detail. Existing art may limit the achievable fit and must be labeled as such.
3. **Compare A-reference and B-midpoint.** First use identical snapshot, art, HUD, field treatment and framing. Then show a separately labeled framing sweep for each candidate, using the already documented 1×/1.25×/1.4× settings rather than silently compensating one side. Measure occupied Player, Camera and building heights as viewport fractions, with source/output sampling. Full-reference fidelity and geometry correctness are separate verdicts.
4. **Prove playable coherence.** Traverse front, rear and corners in eight headings, including quarter/half/full analog input, stop, blocked movement, slide, reversal and reactions. Record authoritative heading, post-collision displacement, projected travel and authored facing separately. Preserve event-owned facing. Unsupported authored directions remain explicitly unsupported, not relabeled as new art.
5. **Prove visibility.** Capture quiet, the same legal encounter, and a dense legal encounter. Keep attacks, Camera fields, projectiles, shadows, occlusion, map edges and HUD exclusions. Review native, half-size and grayscale with natural and authoritative overlays. Run BP-011, retaining its existing reference and review-flag semantics. Dense/playable/device proof is required before asset admission, not claimed by this research.
6. **Present the owner decision.** Show where each candidate matches or misses the fixed benchmark and which tests remain open. Record the owner's selected projection and images only after the owner chooses. Do not convert this research into D-108 approval.

Apple's camera guide distinguishes camera scale from world size and keeps camera-child HUD nodes unaffected by camera zoom [S3]. Its conversion API supports conversion between node coordinate spaces [S4]. Tiled's renderer supplies a primary example of paired forward/inverse mapping and rectangle-vertex projection [S5]. These justify the comparison architecture without settling its aesthetics.

### Input and replay caveat

For the current midpoint, with `r = sqrt(0.5)` in positive-up scene coordinates:

```text
P(dx,dy) = (r*(dx-dy), r*(dx+dy)/2)
P^-1(sx,sy) = ((sx+2*sy)/(2*r), (2*sy-sx)/(2*r))
```

Screen-down projects from world south-west, not world south. For screen-relative analog input, inverse-map the desired direction and restore the original stick magnitude under the existing command rules. Do not normalize the displayed displacement to make all screen directions equally fast. The two projected diagonal screen speeds differ by a factor of two at equal world speed. This is derived from the local matrix and recorded in SS-specs `:305–328`, not an external recommendation.

Replay checks must distinguish boundaries: identical **world commands** must retain simulation identity for a presentation-only trial. Identical physical stick gestures can intentionally produce different world commands after a separately approved inverse-input migration, so do not demand the same digest for those different command streams.

## Decision rule and confidence

- **High confidence:** the visual benchmark must remain fixed, A-shipping is not A-reference, midpoint is not a calibrated reconstruction, and a partial transform is not production readiness.
- **Moderate confidence:** a reference-calibrated ground/root model with independently authored upright art is the least disruptive first trial within the existing renderer. Its final visual quality is unproved.
- **Not determined:** the winning projection, exact angle, final zoom, diagonal-facing sufficiency and performance on the floor device.

**Recommended next owner authorization:** the isolated faithful original-reference comparison trial, with no new family source detail or production mapping change. The owner projection choice remains **UNRECORDED**. This research does not implement that trial or reserve permission on the owner's behalf.

## Validation of this research-only update

On November 16, 2026, `python3 scripts/verify_bp001_decision.py` rechecked all 24 plate hashes/dimensions, four capture-source hashes, grayscale channels, concept hashes and four palette computations. Five regressions passed with `python3 scripts/test_bp001_decision.py`. Existing `swift test --filter Projection` passed 14 tests across five suites. The live browser loaded both unchanged 1672×941 concepts and four 2112×978 natural plates, displayed the revised notice and opened this complete document through its gallery link. `git diff --check` passed. No full native suite or new capture was run for this documentation-only change. Fresh-export comparisons remain the separately recorded earlier evidence, not a new claim from this turn.

## Primary sources consulted November 16, 2026

Paraphrases only. No external implementation code copied. External sources establish mechanics and limitations, not SS visual approval.

- **S1, Apple, About SpriteKit Coordinate Systems:** parent-local positions, positive-up scene coordinates and rotation conventions. `https://developer.apple.com/documentation/spritekit/about-spritekit-coordinate-systems`
- **S2, Apple, About Node Property Propagation:** scale/rotation affect descendants and coordinate conversion. `https://developer.apple.com/documentation/spritekit/about-node-property-propagation`
- **S3, Apple, Getting Started with a Camera:** inverse camera transforms and camera-child HUD behavior. `https://developer.apple.com/documentation/spritekit/getting-started-with-a-camera`
- **S4, Apple, SKNode.convert(_:from:):** conversion between node coordinate systems. `https://developer.apple.com/documentation/spritekit/sknode/convert(_:from:)`
- **S5, Tiled primary renderer and object manual:** forward/inverse conversion, rectangle-to-polygon projection, independent tile-object alignment. `https://github.com/mapeditor/tiled/blob/master/src/libtiled/isometricrenderer.cpp` and `https://doc.mapeditor.org/en/stable/manual/objects/`
- **S6, OpenCV, Basic concepts of the homography:** assumptions for planar mappings and pose estimation with known intrinsics. `https://docs.opencv.org/4.12.0/d9/dab/tutorial_homography.html`
