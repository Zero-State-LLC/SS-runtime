# North neutral first source sample, PROPOSED

Scope: slice 3 under the owner approval at 2026-11-16 03:10:28 UTC. Contract IDs: BP-002, BP-007, BP-008, BP-012, T1045. This is not production, native, simulator, family or animation admission.

## Deliverables

- `north-neutral.png`: 384 x 416 RGBA assembly.
- `layers/`: 13 editable full-canvas layers in bottom-to-top order.
- `components/`: exact RGBA crops from detached sheet components.
- `south-north.png`: unchanged south original beside proposed north.
- `north-extension.json`: same-master extension bindings, hashes, transforms and limits.
- `index.html`: native 64 x 69.33 and large views, plus layer toggles.

## Method

`assemble.py` crops each authored extraction region from the revised sheet, records the actual alpha bounding box and saves that RGBA crop byte-for-byte. It uses no threshold cleanup, mask repainting, warping or mirroring. Each layer has only uniform per-part Lanczos resampling and translation into a 384 x 416 canvas. The left flat guide is not used.

Back view uses anatomical right on screen right. The right satchel binds to `right_hip`. The painted strap runs from screen-left shoulder to anatomical-right hip. Ground root stays at (192,336), with logical root (32,56).

## Provenance

Revised sheet: `/Users/appliedalchemylabs/.jcode/generated-images/1794798956933-ig_07cd661172aa2162016afa7548d1d087d0a302a894cfd91028.png`, copied to `source/`. Its metadata is copied too. All north back and hidden-surface paint is native-image-generation output, not original master paint. The prior attempt `1794798865937-ig_07cd661172aa2162016afa74e4f19087d089e00f6d009c0970.png` is history only.

Original read-only inputs are the south neutral frame `SS-player-bounded-neutral/frames/00.png` and `SS-player-bounded-proportions/source/body-rig.json`. JSON bindings are semantic extensions only. The south pivots are 2D annotations, so the bindings do not prove anatomical continuity.

## Owner leg preference, 03:41:04 UTC

Owner: "legs on assembled north and south are inconsistent. i like the baggy look better". The leg-width target now follows the baggy attempt 01 trouser volume across facings, PROPOSED. Attempt 02's leg slimming is superseded for legs only. Its files stay unchanged as history. The south originals and release 5/13 stay unchanged. Bag, coat and material remain separate open decisions.

`baggy-leg-landmarks.json` records attempt 01 leg alpha bounds and opaque row widths. The layers span y220-360. Root (192,336) is the canonical registration anchor, not a required bottom edge for the visible boots. The unchanged south alpha also extends to y359. Knee and cuff y are not semantically annotated.

**Current selection: attempt 01** (`north-neutral.png` SHA-256 `0a6e15bd2aa8cc486dd14521b60680bed6a2dd0833707972850e65d7991f4fbb`, identical to `attempts/01-uniform-0.4/`). This is the PROPOSED baggy reference.

## Correction attempt 02, BLOCKED HISTORY

Attempt 01 (single scale 0.4) is preserved read-only in `attempts/01-uniform-0.4/` and is active again. Attempt 02 is immutable history in `attempts/02-per-part-uniform/`. Each part has one uniform scale and a translation, chosen against original south `body-source` alpha bounds. See `attempts/02-per-part-uniform/proportion-comparison.json`. These are measurements, not pass thresholds.

The thigh, torso, upper arm and shin widths now match the south closely, and the bag is smaller. The constraints conflict, though. With the visible boot bottom wrongly treated as fixed at y336 to match the slim south boot layers, the generated thighs and shins leave a 4 to 5 px opaque gap at each knee. That constraint was false: y336 is the root anchor, not the boot end. The gap partly came from that mistake. Forearms, hood and satchel also cannot match both width and height with one uniform scale. Attempt 02 also stays blocked because the owner prefers the baggy legs. This is still a proposed generated hidden-surface extension, not original master paint.

## Verification

Run:

```sh
/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python docs/review/player-north-source-20261116/assemble.py
/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python -B docs/review/player-north-source-20261116/test_source.py
```

Nine source guards cover source and original hashes, exact component RGBA identity, layer transforms and hashes, complete unique composition, left/right asymmetry, registration, unchanged south comparison and actual-alpha gap samples. The transparent RGB glow seen by some viewers is not counted as opacity.

Visual inspection of attempt 01 found no floating part, cut gap or duplicated detached layer in the source-size assembly. Independent coordinator verification on November16 at04:10UTC loaded all17 images in actual Brave, checked both native images at64×69.328125 CSS pixels and source images at384×416, and exercised all13 layer controls. Each hid/restored only its associated layer, all were restored, and the ground-root marker remained. No failed control check was reported. All nine source guards also passed independently. This is source-gallery behavior, not native rendering or visual acceptance.

## Limits

The parts do not establish master continuity. Compared with the approved south, the north has a much larger satchel, heavier boots and leg volume, a different coat-tail shape and smoother material treatment. The elevated view is not proven. Treat this as a review sample, not a basis for north animation.

Shins and boots are single generated parts, so there is no independent boot control. Joint range, depth treatment, heel/toe contacts, native renderer, simulator, live playback, device and production fidelity are unverified. No new generation, shared-file edit or commit was made.
