# Player neutral family record - BLOCKED_UNRECONCILED_FAMILY - slice 5

Slice 5 of the owner-approved ten-slice plan (2026-11-16 05:56:35 UTC).
Contract IDs: BP-002, BP-007, BP-012, T1045.

This packet does NOT admit any facing into production, trigger animation,
permit native-render or shipping, or change any pinned spec, receipt or
replay. It is a source-only review artifact.

## What this is - and what it is not

**What it is:** a partitioned record of four independently generated views,
each with its own layer set and provenance, assembled into a comparison strip
with shared parameter/equipment annotations. No new image generation was
performed. All inputs are read-only.

**What it is not:** a common editable master that can faithfully author all
four facings from a single source. The four generated facings are independent
image_generation outputs from separate sheets. No shared anatomical model,
shared rig, or single editable file underpins them. Passing hash and dimension
checks does not establish anatomical continuity, costume coherence, or
consistent viewpoint. Do not interpret the integrity tests as evidence of a
coherent family. The open blockers (satchel depth, coat volume, camera
elevation) are unresolved cross-facing discrepancies, not minor finish items.

| Facing | Source packet |
|---|---|
| south | `docs/review/player-baggy-south-source-20261116` |
| east  | `docs/review/player-side-source-20261116/east` |
| north | `docs/review/player-north-source-20261116` (attempt 01, baggy) |
| west  | `docs/review/player-side-source-20261116/west` |

## Deliverables

- `four-facing-source.png`: all four at 384x416 (gap 4 px), panels south / east / north / west.
- `four-facing-native.png`: all four at 64x69 raster pixels, rounded from logical 64x69.333.
- `four-facing-half.png`: all four at 32x35 raster pixels, rounded from 32x34.5. Not exact 50% of the 64x69 preview.
- `four-facing-grayscale.png`: all four at 64x69, desaturated.
- `role-masks/`: 16 RGBA files (4 facings × 4 roles: lower_body, upper_body, equipment, head), 384x416 each.
- `family.json`: common parameter/equipment mapping, anatomy notes, part vocabulary, source packet hashes, open blockers.
- `output-hashes.json`: SHA-256 of each output for reproducibility.
- `index.html`: four-facing strip gallery plus per-facing layer toggles and role-mask display.
- `assemble.py`: reproducible deterministic assembly from sibling packets.
- `test_family.py`: 15 integrity groups (107 assertions passing, 2 disclosed skips).

## Reproduce

```sh
P=/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python
$P -B docs/review/player-neutral-family-20261116/assemble.py
$P -B docs/review/player-neutral-family-20261116/test_family.py
```

## Integrity tests (107 PASS, 0 FAIL, 2 SKIP)

| ID  | Guard |
|-----|-------|
| T1  | Input source images unchanged (SHA-256 match) |
| T2  | All four output strip images exist and are correct dimensions |
| T3  | Strips are bit-for-bit reproducible (re-run assemble) |
| T4  | Native strip 268x69 |
| T5  | Half strip 140x35 |
| T6  | Grayscale strip has no saturation |
| T7  | All 16 role-mask files exist and are 384x416 RGBA |
| T8  | Each role mask has opaque pixels (south-equipment + south-head SKIP: merged into original_upper) |
| T9  | family.json has required keys and BLOCKED_UNRECONCILED_FAMILY status |
| T10 | index.html non-empty and contains all four facing labels |
| T11 | Layer files exist for each facing |
| T12 | North SHA matches active attempt-01 |
| T13 | South/east/west SHA prefixes match their own packet declarations |
| T14 | output-hashes.json round-trips |
| T15 | Blocked status, false coherence/readiness/acceptance flags, and both absent south roles documented |

## Coordinator browser evidence

Coordinator stallion reported on November 16 at 06:20 UTC that all 45 layer
toggles changed and restored pixels over loopback, all 20 gallery images
loaded, and there was no page overflow. This is coordinator-reported gallery
behavior, not independent verification by this worker or evidence of a
coherent source family. The family remains BLOCKED_UNRECONCILED_FAMILY.

## Disclosed blocker: south has no separate equipment/head layers

The south baggy-neutral packet merges hood and satchel into `original_upper`.
Those roles are not separately isolatable from the south layer set. The south
role masks for `equipment` and `head` are empty canvases. This is a known
limitation of the south source structure, not an assembly error. The original
south release-5/13 frames are untouched.

## Common parameter/equipment mapping

See `family.json` for the full record. Highlights:

- Canvas: 384x416 RGBA. Ground root: (192, 336). Logical canvas: 64x69.333.
- Satchel binds to `right_hip` in all facings. South: front-right hip. North: rear-right hip. East/west: satchel depth placement is an **open blocker**.
- Cloth patch binds to `left_thigh` in all facings (south: screen-right thigh; visible in west near-thigh).
- Layer naming: south/north use left_*/right_* (anatomical). East uses far_left_*/near_right_*. West uses far_right_*/near_left_*.

## Open blockers (from family.json)

1. Satchel depth placement differs between south (front-hip) and north/east/west (rear-hip). Not resolved.
2. Coat tails generated broader and flatter on north/east/west than south. Not reconciled.
3. Camera elevation: side views appear closer to eye level than south. Not proven.
4. Baggy-south trouser shins 5-7 px narrower than north reference at row 295. Trade-off deferred.
5. Shin and boot are one part on all non-south facings; no independent boot control.
6. No joint-range, contact, heel/toe, native renderer, simulator, live-cadence or device verification.
7. Generated facings are not original master paint. Hidden surfaces are generated proposals.

## Limits

BLOCKED_UNRECONCILED_FAMILY source samples only. Original south release-5/13 unchanged. No
animation, native-render, simulator, production admission, shipping, merge or
specification-pin change authorized. Owner review required before any further
expansion.
