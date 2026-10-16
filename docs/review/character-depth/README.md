# Shared lower-body source depth and calf refinement

Status: source integration candidate; not benchmark art or active runtime animation.

Both boot/calf renders now retain their per-pixel source depth. The thigh renderer returns matching world-source depth. assemble.py resolves all four images through one depth buffer, replacing average per-limb draw ordering. The recorded comparison uses the same current images with the prior average-sort composite: 168–555 pixels differ per frame across all sixteen frames. This establishes that the source depth path has an effect; it does not establish correct whole-character occlusion.

The calf tube changes from uniform radius 1.45 to an authored tapered profile: radius 1.6 at source distance 3.45 from ankle, 2.0 at 7, 2.2 at 11 and 2.0 at 13.5. These are candidate source proportions, not anatomy measurements or new specification requirements. Retained high-resolution cloth material follows longitudinal calf position. The first crop included a knee-pad fragment, duplicated on the back; boot/rejected-knee-pad-swatch.png preserves that failure. The revised crop uses registered source rectangle [158,289,180,307], excluding the visible pad.

The sixteen-pose sheet was inspected. Depth ordering and cloth coverage are improved construction mechanisms, but the knee cap/joint remains visibly exposed in recovery, the cloth patch is repetitive and the boot material does not match the upper-body quality. Torso and coat still use front-layer compositing outside the shared lower-body buffer. No art acceptance is claimed. The next source repair is a continuous knee/joint surface with correctly owned pad material, followed by full-source motion quality and existing renderer travel gates.

Verification: boot/material.py and assemble.py each completed exit 0; 32 boot/calf images and depth arrays, sixteen distinct RGBA source frames, fixed 384x416 canvas and existing 0.5-second source cycle. The GIF is deliberately slowed to 125ms/frame. Pixel depth records and assembly hashes are retained. Prior clean core result remains 773 tests in 109 suites. No runtime/device validation is newly claimed.

Authority: existing SS-specs d602775 controlled-character-source.md/BP-002/BP-008. No new product policy or active code/art/metadata changed. Reproduce with Python + NumPy + Pillow: boot/material.py, then assemble.py. Exact source geometry, material, depth and assembly recipes plus inputs and evidence are archived.
