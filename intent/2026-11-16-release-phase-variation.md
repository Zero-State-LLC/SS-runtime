# Slight phase-dependent release motion

Owner direction received November 16, 2026 at 02:36:26 UTC: "should add slight variation in phases for more dynamic motion".

## Implementation decision

Create a separate, deterministic source candidate in `docs/review/player-release-variation-20261116/`. Vary the easing and lift arc slightly by release phase/source stance, rather than adding random jitter or stretching the same raster. Preserve the original source masters and the published baseline at commit `15be1316d3817604e751664d5167f1649db2fc6b` for synchronized before/after comparison.

- Keep 17 poses and 3/128-second holds, with neutral beginning at 0.375 seconds.
- Keep source entry and neutral pixels exact and preserve the approved phase5/13 frames and samples byte-for-byte.
- Keep planted toe contacts, limb geometry, stationary root and existing contact schedules. Small profile amplitudes are authored proposals, not visual acceptance thresholds.
- Render in bounded batches with validated checkpoints, never by relaxing source or endpoint guards.
- Provide normal and separate quarter-speed baseline/candidate review. Changes to new intermediate poses must be measurable and repeatable, with exact endpoint identity.

## Evidence boundaries

The earlier all-release native packet remains evidence only for the unchanged baseline. Do not relabel it as a native capture of this new variation. Source review is not live cadence, shared-scene, physical-device, art admission or merge approval. All four-facing/family gates and issue237 remain open. No production assets, App/Sources, input, mapping or shipping specification pin changes are authorized by this refinement. Do not retry the twice-capped local unfiltered Swift suite.
