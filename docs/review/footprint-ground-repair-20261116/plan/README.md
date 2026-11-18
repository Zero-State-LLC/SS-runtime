# Shared footprint, ground and prop plan: final bounded correction

Status: **one bounded material correction completed, NOT visually accepted**. The coordinator rejected first material in `../SOURCE-REVIEW-01.md`. All17 attempt01 files are preserved under `attempt-01/`; no third art pass is authorized. Approved intent: `intent/2026-11-16-footprint-ground-consistency.md`. All work is isolated here. Historical V7 files remain read-only and are checked against `v7-immutable-sha256.json`.

## Correction02

Inspect `final-source-detail.png` and `final-plan-preview.png`. `materials.json` and `material.py` now use the hash-pinned retained paving supertile, warm limestone curb joints/wear, staggered mineral foundation courses, and restrained worn crossing/lane paint plus drain/manhole details. Every road detail pixel is clipped to road material, not sidewalk, curb or foundation. `plan.json`, `material-ids.png`, all shared roots and registrations remain byte-identical to attempt01. The unchanged plan's `attempt:1` and first-preview labels identify the geometry contract origin; `materials.json`, `manifest.json` and `validation.json` carry final material attempt2 status.

The first preview was rejected, not recommended. Correction02 is delivered for coordinator review, not owner or visual acceptance. Native execution remains the separate scene lane. Ground SHA256: `97ae5825c57c9e21b48a3d863bfd3e93b940e3eb5c5134b9c51172cc6656b7c7`.

## Scene binding contract

Read `plan.json`. Bind `ground.png` as canvas **4608×4608**, source root **[0,4608]**, world root **[0,0]**, uniform draw size **2304×2304**. Clip with the retained arena [0,0,2304,1536], not by stretching the image. Keep Camera/Player roots, fields, all 24 solids, controls and framing identical to the V7 records under `protected`.

Preserve every V7 building/source sprite byte. Only move `benchmark-prop-1` (tree) from [858,780] to **[858,716]**. Keep prop0 at [691,639]. Ground already contains small contact ellipses: prop0 contact radius5/shadow radius8, tree contact radius8/shadow radius16 world units, alpha maximum0.22. Those radii describe this added treatment, not a claim about embedded pixels in historical prop art. Do not add duplicate new shadow layers. Independent tests require the entire conservative shadow disk to lie on sidewalk and outside every authoritative solid.

## Layout and mesh evidence

All **14** building envelopes receive a mineral foundation with3-unit collar, **24-unit sidewalk** and **4-unit curb**. Overlapping sidewalks merge, including a connected transit/civic apron. The remaining material is road. This is presentation material, never gameplay walkability. No road, curb or sidewalk pixels occur inside any building envelope, including offcrop portions. Thus unchanged neighboring buildings are included, not merely the five replacement sources.

Four context buildings use the actual z=0 vertices of their full rectangular plinth meshes. Kiosk contact is the actual five-corner chamfered mesh boundary, including [551,640] and [512,679]. The authoritative corner [512,640] is explicitly **virtual**, not a visible mesh contact. New ground mineral infill fills that blocked corner, with a dark seam following the actual chamfer. It contains no door, step or traversable-path marking. No building image pixels changed.

**Limitation:** the other nine retained buildings are raster sprites without actual mesh definitions in the V7 source packet. Their foundation envelopes are treated, but their actual architectural contacts are explicitly unknown, not inferred from sprite bounds. This plan does not certify those contacts or solve their inherited sprite registration. Coordinator must account for this in scene review; passing these checks is not full footprint consistency or owner acceptance.

## Files

- `plan.json`: editable shared machine-readable contract, roots, protected authority, actual and virtual landmarks.
- `author.py`: reproducible extraction from immutable actual V7 solids/meshes.
- `replay.py`: local Pillow renderer of `plan.json`; no API or production writes.
- `materials.json`, `material.py`: bounded correction source and retained-input SHA256s; no shared geometry edits.
- `material-1-tile.png` through `material-4-tile.png`: reproducible editable material tiles.
- `road-mask.png`, `road-details.png`, `road-details-mask.png`, `road-details.svg-fragment`: explicit road-only detail layers and clipping witnesses.
- `ground.svg`: editable layered geometry, textured material patterns, contact seams and clipped road-detail shapes. Tiny paint-loss pixels and fine drain lines are replayed by Python rather than individually vectorized.
- `final-plan-preview.png`, `final-source-detail.png`: final correction previews for coordinator review.
- `ground.png`: full registered corrected source.
- `material-ids.png`: road1, curb2, sidewalk3, foundation4, independently tested against layout and actual rendered PNG samples.
- `first-plan-preview.png`: annotated overhead source plan, not an actual native scene.
- `first-source-detail.png`: unannotated source detail crop.
- `test_plan.py`: independent validator with no author/replay imports.
- `tests-first.log`, `tests-final.log`: historical first-attempt executions,17 then19 tests passed.
- `tests-correction.log`, `validation-tests.log`, `validation.json`: corrected actual27-test execution and byte-identical replay evidence.
- `manifest.json`: source/output SHA256 hashes. `v7-immutable-sha256.json`: historical byte preservation inventory.

## Commands and checks

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/footprint-ground-repair-20261116/plan/author.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/footprint-ground-repair-20261116/plan/replay.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/footprint-ground-repair-20261116/plan/test_plan.py
```

Twenty-seven independent tests pass, including18 adversarial mutations. The original15 cover missing neighboring building, changed solid, Camera root, Camera field, stretched ground registration, foundation hole, virtual-as-actual kiosk corner, false source landmark, invented legacy contact, original interior tree root, tree on road, excess shadow, removed sidewalk, road pixel inside a blocked building, and actual rendered PNG disagreement. Three correction mutations reject crossing paint on a foundation, a missing crossing, and undeclared road paint. New checks pin all17 attempt01 files, preserve shared plan/material IDs, verify exact retained paving resampling, require all road details to stay in their declared road-only bounds and compare every crossing/lane paint pixel with the independently specified worn pattern. Normal checks also include209 V7 SHA256s, every building foundation pixel, dense material boundaries and15,612 actual RGB source samples outside explicit seam/shadow exceptions.

The first renderer invocation failed before producing any preview because NumPy was unavailable. It was replaced with existing local Pillow before the first successful render. No external API or installation was used. First preview followed by exactly one coordinator-directed material correction. Identical replay for byte determinism is not another art iteration. Run `PYTHONDONTWRITEBYTECODE=1 python3 docs/review/footprint-ground-repair-20261116/plan/validate.py` to execute27 tests, verify14 byte-identical replay outputs and seal the recursive manifest including attempt01. No third art pass. No native runs, production changes, commit, push, source admission or visual acceptance are claimed. Swift tests are left to the coordinator's shared validation lane under the explicit no-native-run ownership restriction.
