# Constrained building source and renderer registration

Runtime parent095be8b; spec c773f960ee8f53ac429828767fcd09f4da0d7cb3. CAPTURED / REVIEWED_CANDIDATE, not production admission.

## Source

Built-in image_gen used geometry-guide.png as a geometric constraint and the existing benchmark building as a facade/material reference. Exact prompt in prompt.txt. It returned1254x1254 RGBA, rather than the requested1024 canvas. source.png is unmodified. building-registered.png remaps alpha only (<=32transparent, >=240opaque, linear between). No warp, rescale, repaint or collider change. registration.json records hashes, dimensions, contact annotation and deviations.

The facade retains teal paint, cream trim, brick and roof equipment. Baked sidewalk, stairs, gardens and fences are removed. Ground-floor bay detailing still deviates slightly from the requested flat plane. Lower-contour fits on sampled source columns have slopes about0.470 and-0.544 versus guide slopes+/-0.5. Maximum local fit residuals are8.45 and1.08source pixels. These are diagnostic observations, not an accepted tolerance or proof of the unseen rear boundary.

## Renderer

Candidate texture lives only in AppTests/BenchmarkAssets. The test uses the existing real WorldRenderer scene and projection comparison. The visible near corner at source(653,1152) is placed at the projected world minimum-x/minimum-y corner of the existing128x128 obstacle. A uniform draw scale maps the approximate934-pixel side-to-side span to128*sqrt(2)logical units. Upright art is not compressed with the ground plane. The old art and new art are both captured at zoom1 andsqrt(2).

OBSERVED: wall-ground contact is much closer to the magenta projected footprint, and the formerly obscured newsbox is visible. The roof and upper walls intentionally extend over ground behind their contacts. The overlay's rear edges run across the visible facade because the diagnostic overlay draws hidden geometry on top; this alone is not a wall-contact failure.

Remaining: a small source/base mismatch; hidden-rear correspondence not established by this2Dsource; apparent building/player/camera scale; continuous street/curb/rail composition; depth sorting and front/rear/corner traversal; legal projectile and camera-field contact; quiet and dense animation review. Equal-area zoom still crops the camera. No projection/framing choice is accepted. Do not replace the shipping arena assets from these stills.

## Validation

Test-SSRuntime-2026.10.14_11-39-11--0700.xcresult: Passed87tests, zero failures/skips;89executions with dynamic cases. iPhone17Pro simulatoriOS26.5. No physical device run. Geometry invariants and transform assertions pass, but the capture does not exercise traversal, animation or legal encounters. Raw captures and manifest are retained in capture/. Generated local Xcode resource references were updated for this test without changing signing settings; generated project files are not committed.
