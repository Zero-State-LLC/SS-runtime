# Coordinator source review, November 16 22:23 UTC

**Decision: recommended only for the isolated building comparison. Not benchmark equivalence, owner acceptance or production admission.**

The coordinator inspected `output/first-sample-comparison.png` at native200x240 and half100x120, then `output/source-full.png` at source resolution. The roof now has a legible inset and coping edge, the window/entry returns retain the independently painted material, and stair treads read as depth rather than a flat panel. The unchanged D108 basis and source envelope remain appropriate. This is a bounded improvement over the v6 flat-panel source, not a reason to change camera projection or collision.

Limitations remain: symmetric massing and repeated facade paint differ from the benchmark, fine bevel lighting/lamp/weathering are still baked, hidden faces reuse materials, and the vent is a separately registered2.5D raster. Native scene composition, context cohesion and post-change occlusion still require actual capture. No second aesthetic source pass is requested before that evidence.

Independent coordinator validation at22:22 passed all12 kiosk tests in14.720s, including isolated byte replay, geometry/UV/material mutations, independent landmarks, exported OBJ replay and source alpha. The source authoring and depth-buffered renderer were read directly. The read-only original-byte audit passed110 tracked original source/capture files against HEAD1eaa66d. See `coordinator-tests-2222.log` and `original-byte-audit.json`.

Reviewed bindings:
- Image: `output/source-full.png`, SHA256`c411e33b79e0ffc5b0eb86143cd8785a564e573b5819bc1d4c399ef5d3b60264`.
- Registration: `output/registration.json`, SHA256`9a00502006c3070dd2ae30de0299797fb983b1418437768d1ac9b09c6eabcd9f`.
- Manifest: `output/manifest.json`, SHA256`b2c8695bbf21b0bd48c7f7ddd8cdbaf0eb0240b3d45d4d5c9163e0da538d28fe`.

Root[512,640], canvas[1000,1200], source root[500,1160], uniform draw size[200,240]. All authority and motion gates remain unchanged.
