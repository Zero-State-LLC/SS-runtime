# Extraction brackets

Read 2026-11-05 from `VFXRenderer.extractionBrackets` on `c6da67e`. No zone was moved.

The zone box stays in [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md). The countdown stays in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The angle step stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md).

The brackets sit at the extraction zone's centre, on the world effect layer. Each side is that zone's full width or height. Each arm is 18. The stroke is red 0.35, green 0.85, blue 0.60, alpha 0.9, at line width 3.

Reduced motion or reduced flash adds a fill of that colour at alpha 0.15, with a clear stroke. Its horizontal scale starts at 0 and runs to 1 over the presentation lifetime.

Otherwise each of the variant's particles is a 4 by 4 square of the stroke colour. It starts at half the zone's width and height along the shake note's angle step, and it travels to the centre, fading over the lifetime.

This does not move the zone.
