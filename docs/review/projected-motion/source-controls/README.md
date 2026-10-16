# Foot and cloth control preparation — BP-002 / BP-008

Twenty-two editable PNG layers and twelve source controls retain the original neutral exactly. Boot/toe regions are split from the shin/boot layers at source row 309; coat tails are split below row 205 from the torso/coat layer. The original art was neither repainted nor mirrored. Isolated source parts were visually inspected. Extraction polygons and approximate pivots are saved in extraction.json.

These are source cuts, not anatomical definitions. The ankle pivots and visible sole edges do not identify hidden heels or establish contact. New cut edges have no authored overlap yet. Coat roots require deformation/attachment review before motion. Do not use this source as a completed gait or claim world-space contact from it.

The independent renderer reads rig.json and source PNGs. Run `python3 render_source.py --pose 0 --output neutral.png` with Python and Pillow. Unknown named controls fail. Existing diagnostic poses are inherited from the previous scaffold; they do not exercise or approve the new foot/cloth controls. The new source has only been checked in neutral.

Research driving the next step: Spine's mix-and-match example documents weighted depth/garment controls and hidden surfaces (https://esotericsoftware.com/spine-examples-mix-and-match); its IK guide describes endpoint constraints and stretch/compress limits (https://esotericsoftware.com/spine-ik-constraints). These mechanisms do not select SS gait or contact phases. Specs 492d921 separates source/anatomical measures from projected lengths and requires authored foot contacts before gait claims.

No runtime production asset or timing metadata changed. Full key poses, depth treatment, contact tests, four facings and device evidence remain open.
