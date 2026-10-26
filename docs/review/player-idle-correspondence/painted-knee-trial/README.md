# Retained knee-paint trial — not accepted

Separately rendered neutral material comparison. The prior thigh renderer sampled retained paint and then overwrote the anterior cap with procedural shading/noise. This trial preserves sampled paint under the existing cap mask, without changing pose, geometry, UVs or root. Inspection shows recognizable source paint but an undersized/shallow visible pad; this is not a satisfactory repair and is not installed in runtime.

The trial separates material loss from the remaining cap geometry/mapping/overlap problem. The cause of the compressed visible pad is not proven. Inspect cap orientation, UV range and calf depth occlusion before another material-only iteration. Do not adopt this trial merely because it reuses original paint. Reference crop and comparison are retained.

A separate analytical neutral fit to source knee y=265 with planted toe y=0 produces equal segment length 12.3771, versus current 13.5. Existing stride targets exceed its reach (25.7923 maximum hip–ankle distance versus 24.7541 reach, before a neutral foot-depth offset). Therefore a shorter-leg substitution alone is rejected. The 2D landmark is an authored calibration target, not recovered anatomy. No source stride, registration or gameplay change was made.

Copied historical files are not evidence for this trial. Relevant outputs: frames/00.png, comparison.png, knee-source-crop.png, change-record.json and modified thigh.py. Existing movement and neutral controls are preserved in their original output directories.
