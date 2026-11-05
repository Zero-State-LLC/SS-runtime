# Camera clip states

Read 2026-11-04 from `CameraPresentation.persistentState` and `WorldRenderer.playCamera` on `006304e`. No camera clip was added.

Integrity 3 is `operational`, 2 is `damaged`, 1 is `critical`, and any other integrity is `dormant`. `operational` plays `camera_operational_idle`. `damaged` and `hit` play `camera_hit`. `critical` plays `camera_critical_enter`. `destroying` plays `camera_destroy`. `fieldOff` plays `camera_field_off`. `destroyed` and `dormant` play `camera_destroyed_idle`.

The snapshot maps each camera through `persistentState`. `fieldVisible` is integrity above 0. The stored clip is the clip for that persistent state. `CameraPresentation.project` is called from `CameraPresentationTests`.

`playCamera` settles on the persistent clip. Integrity at or below 0 uses the literal `camera_destroy` as the transition clip. Any higher integrity uses the settled clip as the transition. An unbacked transition, or a settled clip with no last texture, returns false, and the renderer draws a circle of radius 12 filled from `cameraFill` of the persistent state. The sprite box is 64 by 96. The anchor comes from the sprite library for the settled clip.

The token is `camera`, the integrity, and the reduced-motion flag. An unchanged token leaves the sprite running. Reduced motion sets the last texture of the settled clip. Otherwise the sprite starts on the first texture of the transition clip. `camera_operational_idle` and `camera_destroyed_idle` have `loop` true. `camera_hit`, `camera_critical_enter`, `camera_destroy`, and `camera_field_off` have `loop` false. `animation` repeats a looping clip and plays the others once. Integrity 3 runs the operational action. Integrity 2, 1, and 0 run a non-looping transition and then set the settled clip's last texture.

When review art is installed and the benchmark camera is incomplete, the sprite is that art's texture for the integrity, or the art's fallback camera, at 64 by 96. With review art absent, a housing family that has a texture is drawn under the head at the same box. The placed-camera record stays in [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md).
