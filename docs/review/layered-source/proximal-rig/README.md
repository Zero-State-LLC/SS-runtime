# South painted-source rig scaffold — BP-002 / T1045

This source package preserves the original south neutral and adds separate hidden cloth overlaps at both shoulders, elbows, hips and knees. It contains eighteen layer PNGs, editable rig.json controls and an offline Pillow renderer. No skeletal runtime dependency is introduced.

## Reproduce a source pose

Requires Python 3 and Pillow. From the unpacked directory:

```sh
python3 render_source.py --pose 0 --output neutral.png
python3 render_source.py --pose 9 --output combined.png
```

Edit a JSON object of named angles, for example `{"right_shoulder": 6, "right_elbow": -12}`, then pass its file using `--angles-file`. Angles are clockwise in the 384×384 source image. Pivots are manually estimated; they are not anatomical measurements. rig.json holds the parent hierarchy, bindings, draw order and diagnostic poses. Each layer is transformed once by its composed parent/child matrix. The identity transform bypasses resampling to preserve neutral pixels.

## Verified and observed

The saved-source renderer reproduces the neutral exactly. Parent/child joint locations agree within floating-point precision, and the diagnostic transforms preserve segment lengths. A known quarter-turn calibration passes; unknown joint controls fail explicitly. Neutral and eight shoulder/hip extremes were visually inspected, as was the combined pose. The shoulders carry both forearms and their hidden elbow patches; hips carry shins and hidden knee patches.

Only clipped hidden cloth from built-in image generation was retained. Original visible patches, pockets, cuffs, hands, boots and kneepads were preserved; generated replacements for them were discarded. Generation prompts and hashes are included. Shoulder/hip patches are masked to the original opaque silhouette at rest. This guarantees neutral concealment, not correctness at arbitrary motion extremes.

## Still unfinished

This is a rigid-layer source scaffold, not a finished animation master or walk. It lacks weighted mesh deformation, elevated gait foreshortening, independent boot and coat controls, foot targets/contact, full pose-range garment review and the other three facing rigs. No 16-frame locomotion, SpriteKit movement or device acceptance follows. Existing active production art and timing metadata remain unchanged. Native graphics-editor or skeletal-editor import has not been verified.
