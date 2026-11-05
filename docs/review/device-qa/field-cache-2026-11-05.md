# Field cache

Read 2026-11-05 from `WorldRenderer.cameraFieldPath` on `5a71391`. No ray was changed.

The origin and the ray math stay in [camera-field-polygon-2026-11-04.md](camera-field-polygon-2026-11-04.md). Contact sampling stays in [camera-contact-2026-11-04.md](camera-contact-2026-11-04.md).

`cameraPaths` stores a geometry key and a path under the node name. `reset` clears it. The key holds the origin from that polygon note, the range, the heading, the field angle, and the solid boxes. A stored path is reused when the key already holds an equal geometry. Otherwise `CameraFieldGeometry.path` is computed and stored.

A visible camera asks for the path under `field-<id>` when the stored geometry differs or the shape has no path. The captain field asks under `captain-field` on the same rule.

This does not change the polygon.
