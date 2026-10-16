# Right knee hidden-overlap study

Status: bounded source-authoring progress; not an admitted animation or complete rig.

Built-in image generation produced a plain fabric extension above the isolated boot. The generated boot was discarded; only a small hidden patch was retained, uniformly registered to the original source crop. The original visible limb, costume and sole remain unchanged in the neutral setup pose. The exact prompt is in prompt.txt, with generator source and registration details in manifest.json.

The overlap is a separate layer below the original thigh. Eight diagnostic poses rotate the original shin and hidden patch around an approximate source-space point by up to eight degrees. The side-by-side GIF and enlarged endpoint show the small cut opening filled. At the two endpoints the patch adds coverage to 27 and 24 pixels respectively; this is coverage evidence, not an anatomy or quality score. Both endpoints were reviewed as still images. The local browser review played the PNG sequence (observed frame counter advancing) and paused/scrubbed to frames 2 and 6. Both enlarged endpoint seams were inspected. This verifies source diagnostic playback only; it is not SpriteKit motion evidence.

Neutral reconstruction passes exact composite checks on black, white and gray. Initial assembly exposed incorrect layer ordering; after correcting that, a remaining 40 edge-pixel difference came from unnecessarily resampling the zero-angle pose. The exporter now preserves the identity transform without resampling. The assertions were retained.

Transparent part exports originally retained neighboring source artwork in invisible RGB. A tool preview displayed those hidden colors. The refined layer exporter now clears fully transparent RGB, verifies that invariant for each layer and retains the original visible composites. This is source-reference hygiene, not a claimed fix to SpriteKit rendering.

This is not locomotion: it supplies no foot planting, world displacement, elevated leg foreshortening, full rig, other joints/facings or 16-frame gait. The pivot is approximate. Remaining part ownership and joint surfaces need work. No runtime production art changed, and existing runtime tests do not prove this artwork accepted.

## Packaged editable source

The eleven-layer south-neutral-with-knee.ora retains the ten extracted layers plus a separate bottom-layer right-knee underpaint. An independent archive read resolves every stack entry, reconstructs the stored merged image exactly and checks the original composite on three backgrounds. All layer pixels with zero alpha have zero RGB. Repeated packaging produces the same archive hash. A native graphics editor has not opened the archive; mesh/bone controls remain absent. The local review provides playback and frame scrubbing, not source editing.
