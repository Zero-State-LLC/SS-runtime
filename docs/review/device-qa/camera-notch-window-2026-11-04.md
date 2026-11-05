# Camera notch window

Read 2026-11-04 from `CameraHUDProjector` on `86c05bb`. No notch was added.

The fill rule and the 90-tick constant stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). `tamperSpike` stays in [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md).

A hit is `cameraIntegrityChanged` or `cameraDestroyed`. A destroy is `cameraDestroyed`. A hit stores the tick and sets the persisted integrity to `targetIntegrity` when the query is damageable, and to 0 otherwise. A destroy stores its own tick and sets the persisted integrity to 0. When the query is still damageable, that value is then replaced with `targetIntegrity`.

The window is `tick` at or after the stored tick and fewer than `integrityNotchPersistTicks` later. Live means damageable and any of targeted, damaged, or in range. The notches show when the persisted integrity is above 0 and either the query is live or the hit window is open. The tamper label uses the destroy window. Its copy is `HUDLayout.tamperCopy`, the spike prefixed by `+` and followed by ` TAMPER`, during that window and empty outside it. `drawCameraNotches` still draws that label when the notches themselves are hidden.

This does not change the fill rule.
