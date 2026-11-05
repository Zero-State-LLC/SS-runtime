# Damage impact

Read 2026-11-04 from `VFXRenderer.impactArc` on `e4ff026`. No damage number was changed.

The same-source skip stays in [hit-stop-2026-11-04.md](hit-stop-2026-11-04.md). One world unit stays in [q8-scale-2026-11-04.md](q8-scale-2026-11-04.md). The shot mark stays in [combat-feedback-marks-2026-11-04.md](combat-feedback-marks-2026-11-04.md).

The impact point is the evidence point named `impact`, raw divided by the Q8 scale, or the player when that point is absent. The origin is the evidence point named `source`, on the same scale. An origin is dropped when the contributor list is present and its count is not 1, and when the origin equals the impact.

With no origin the path is a circle of diameter 48, and the node is named `damage-impact-ring`. With an origin the path is an arc of radius 24, from the direction toward that origin minus 0.7 to the same direction plus 0.7, and the node is named `damage-impact-direction`. The stroke is red 0.95, green 0.36, blue 0.28, line width 4, with round caps. It fades over the second half of the presentation lifetime.

Reduced motion or reduced flash draws that stroke only. Otherwise a circle of radius 18, white 0.96 at alpha 0.9, line width 3, is removed after `2 / 60` seconds. Each of the variant's particles is a 3 by 3 square of the stroke colour and travels 14 along its angle. With no origin that angle is the index times a full turn, divided by the particle count. With an origin the index is shifted so the set is centred, and the angle is the origin direction plus that shift times 0.5.

This does not change a damage number.
