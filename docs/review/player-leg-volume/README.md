# Player leg-volume candidate

Fuller calf/trouser and boot-shaft geometry, with a small transition adjustment above the knee. Existing knee-pad surface detail and geometry retained. Hood, torso layers, coat, arm motion, stance, toe trajectories, source samples, 16 frames and half-second timing are unchanged. This edits the existing native mesh source; no new raster paint was generated.

normal-speed.html and quarter-speed.html show separate source playback, with pause/step controls. detail-review.png compares previous source above with the fuller candidate below. seam-review.png shows frames 15, 16, 1, 2. Geometry parameters remain proposed.

Validation: 16 unique frames, fixed 384×416 canvas, unchanged pose sample files and arm/coat assembly; changes confined to the lower-body region (first changed row 194); all 32 projected knee centers covered by finite opaque surfaces; alpha bounds stay inside the canvas. See volume-verification.json and joint-verification.json. The preliminary upper-210-row equality check failed because the intended thigh change starts above row 210; this was investigated rather than counted as a pass. Existing torso source layers and assembly remain identical. Statistics do not replace visual review.

No runtime or production assets replaced. This revision has not yet been tested in the renderer; prior Reduced Motion test results apply to the previous candidate. Review both source speeds before renderer validation and shared-scene integration.
