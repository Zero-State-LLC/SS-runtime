# V7 footprint consistency correction, November 16 22:52 UTC

Owner feedback at22:50:20UTC: footprints are inconsistent. This supersedes the coordinator's claim that the footprints were corrected/coherent. The V7 packet remains immutable evidence and is not accepted.

## Confirmed evidence

`diagnose.py` reads the actual v7 candidate records, bound ground source and original ground-layout parameters. It does not synthesize a new native capture. Run:

```sh
python3 docs/review/footprint-consistency-20261116/diagnose.py
python3 docs/review/footprint-consistency-20261116/test_diagnose.py
```

Four diagnostic tests pass, including analytical rectangle/half-plane area checks. `diagnosis.json` retains input hashes and exact counts. These tests confirm the defect, not a repaired scene.

| Canonical footprint | Paving | Curb | Painted road |
| --- | ---: | ---: | ---: |
| residential-west |57.8125%|1.171875%|41.015625%|
| residential-north |100%|0%|0%|
| transit-kiosk |100%|0%|0%|
| civic-west |33.3333%|3.125%|63.5417%|
| civic-dais |0%|0%|100%|

Percentages measure whole authoritative rectangles, including offcrop portions, at one-world-unit cell centers. These five shapes avoid the rounded-corner transition, so independent analytical strip areas match the sample counts exactly. Road here means the authored ground material, not gameplay walkability.

The retained tree root[858,780] is inside civic-west[736,768]..[928,1152]. Enlarging that building to fill its plot exposed this previously tolerated prop/layout conflict.

## Why passing registration did not settle this

- `building-perspective-detail-20261116/kiosk/replay.py:134-140` constructs four ground pixels from authoritative rectangle corners. One is explicitly virtual because the visible chamfer omits it. This proves a transform relation, not an actual rendered contact contour.
- `building-perspective-detail-20261116/scene/native.py:242-264` compares those declared points with projected authoritative vertices. It does not inspect whether road, sidewalk, doors, props and neighboring bases agree.
- `paving-corner-review-20261116/source.json:13-25` independently chooses curb x800/y600, radius48, width6 and road ornaments.
- `scene-qa-repair-20261116/ground/build.py:97-134` extends world coverage while preserving that corner's semantics. It explicitly does not certify streets around every other building.
- Kiosk chamfered body/stairs and context full rectangular plinths do not use one visible-contact contract. Actual mesh contact, collision envelope and visual foundation must be inspected separately.

These are concrete inconsistencies and a coverage gap. They do not establish that every perceived footprint problem has the same cause. No historical checks or capture bytes were changed.

## Recommended next bounded repair, approval required

Use one shared ground plan for visible building bases, blocked envelopes, sidewalk/curb/road and decorative prop roots. Preserve authoritative solids, Camera/Player roots and field, framing and controls. Derive contact contours from actual z0 mesh geometry, label virtual collision corners separately, and verify clearances/occlusion in plan and native scene. Do not stretch sprites, move collision, cover contradictions by arbitrary depth, or call algebraic corner equality visual consistency.

The previous authorized pass explicitly froze non-building sources and prop roots and exhausted its bounded correction. Repairing this defect requires changing presentation ground/prop layout, so it cannot honestly be completed under that same frozen scope. Proposed next work order is `intent/2026-11-16-footprint-ground-consistency.md`. No new art or native retry starts before approval.
