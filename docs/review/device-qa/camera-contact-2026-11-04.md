# Camera contact

Read 2026-11-04 from `Detection.sampleContacts` on `fcab4e5`. No field angle was changed. Exposure bands stay in [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md). The field-origin offset stays in [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md).

When the player is camera-invisible on this tick, every camera clears `wasDetecting` and the sample is empty. A camera that is not damageable clears `wasDetecting` and is skipped.

A damageable camera detects when the player is inside its cone and the segment from the field origin to the player meets no live solid. The cone uses half the field angle, in integer milli-degrees. A squared distance greater than the range squared is outside, so the range boundary is inside. The heading test passes when the absolute milli-degree difference is at most that half angle.

The live solids are the permanent solids, every camera mount, and each gate that is still closed. A destroyed camera keeps its mount square. The sample does not remove the detecting camera's own mount from that list. Detecting ids are returned in ascending entity id.

This does not add a camera.
