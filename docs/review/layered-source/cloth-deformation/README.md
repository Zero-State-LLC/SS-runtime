# Anchored coat-tail deformation — BP-002 source study

The existing twenty-two source layers now use ten rigid joint controls plus two independent cloth deformation controls. Coat tails no longer rotate as rigid detached pieces. Each tail uses six authored rows with hem weights [0, 0, 0.15, 0.4, 0.7, 1]. The top two rows remain fixed while the lower rows translate horizontally. The PNG exporter samples a strip mesh; no runtime mesh engine or cloth simulation is added.

This follows the documented authoring pattern of keeping garment attachment vertices tied to the body while separate controls affect the rest of the garment, illustrated in Spine's mix-and-match example: https://esotericsoftware.com/spine-examples-mix-and-match . The particular rows, weights and diagnostic ±4-source-pixel offsets are authored study parameters, not externally validated SS settings.

## Reproduce

Requires Python 3 and Pillow. rig.json contains layer bindings and deformation rows. Put a JSON object such as {"right_coat_tail": 4, "left_coat_tail": -4} in a file, then run:

```sh
python3 render_source.py --pose 0 --deformations-file cloth.json --output pose.png
```

The cloth values are horizontal offsets in source pixels, not angles. Other joint controls retain clockwise image-space angles through --angles-file. Zero deformation returns the original image without resampling. Fixed attachment rows are copied unchanged to avoid alpha-rounding differences during export.

## Evidence and limits

Neutral is exact against the preceding source. In all eight diagnostic poses every composite pixel above source row 210 remains unchanged, including each cloth attachment. Nonzero offsets change the cloth pixels. Neutral and both extrema were visually inspected in cloth-endpoints.png. The GIF is a small cloth-control study, not accepted secondary animation or a locomotion cycle.

The torso is stationary in this comparison. Combined body movement, depth/overdraw, garment follow-through, boot overlaps, authored heel/toe contacts, full gait and other facings remain open. No production resource, active metadata or gameplay identity changed. Prior core test results do not validate artwork.
