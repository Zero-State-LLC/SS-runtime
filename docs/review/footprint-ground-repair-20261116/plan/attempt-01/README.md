# Shared footprint, ground and prop plan: first preview

Status: **first source preview only, NOT visually accepted**. Approved intent: `intent/2026-11-16-footprint-ground-consistency.md`. All work is isolated here. Historical V7 files remain read-only and are checked against `v7-immutable-sha256.json`.

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
- `ground.svg`: editable layered material geometry and actual-contact seams. It omits deterministic microtexture, which `replay.py` supplies.
- `ground.png`: full registered source.
- `material-ids.png`: road1, curb2, sidewalk3, foundation4, independently tested against layout and actual rendered PNG samples.
- `first-plan-preview.png`: annotated overhead source plan, not an actual native scene.
- `first-source-detail.png`: unannotated source detail crop.
- `test_plan.py`: independent validator with no author/replay imports.
- `tests-first.log`, `tests-final.log`: actual executions, first17 and final19 tests passed.
- `manifest.json`: source/output SHA256 hashes. `v7-immutable-sha256.json`: historical byte preservation inventory.

## Commands and checks

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/footprint-ground-repair-20261116/plan/author.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/footprint-ground-repair-20261116/plan/replay.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/footprint-ground-repair-20261116/plan/test_plan.py
```

Nineteen independent tests pass, including15 adversarial mutations: missing neighboring building, changed solid, Camera root, Camera field, stretched ground registration, foundation hole, virtual-as-actual kiosk corner, false source landmark, invented legacy contact, original interior tree root, tree on road, excess shadow, removed sidewalk, road pixel inside a blocked building, and actual rendered PNG disagreement. Normal checks include historical SHA256 preservation, all building foundation pixels, dense independently evaluated material boundaries and more than14,000 actual RGB source samples outside explicit seam/shadow exceptions.

The first renderer invocation failed before producing any preview because NumPy was unavailable. It was replaced with existing local Pillow before the first successful render. No external API or installation was used. First preview generated once; no art correction has been applied. An identical replay for byte determinism is not another art iteration. No native runs, production changes, commit, push, source admission or visual acceptance are claimed. Swift tests are left to the coordinator's shared validation lane under the explicit no-native-run ownership restriction.
