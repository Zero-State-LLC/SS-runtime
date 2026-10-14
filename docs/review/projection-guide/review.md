# BP-007 measured ground-projection guide

Runtime baseline: 91724c8. Specification baseline: c773f960ee8f53ac429828767fcd09f4da0d7cb3. This is a reproducible analytic guide, not a SpriteKit capture, production art, selected projection or gameplay change.

## Inputs and findings

The script reads solid-03-transit-kiosk directly from civic-seam-arena-004.json: center (576,704), half-size (64,64). It records the contract hash and exact world vertices. No footprint is inferred from the generated building. The upright 110-unit wireframe height is an illustrative art-guide parameter only.

Current screen mapping is (x,-y), relative to the solid center. The PROPOSED elevated candidate is u=(x-y)/sqrt(2), v=-(x+y)/(2*sqrt(2)), with screen y downward. This is a 45-degree ground rotation followed by vertical compression, chosen as a measurable experiment, not an angle recovered from the approved concept. Upright image height is kept independent of the ground transform.

OBSERVED arithmetic: the same 128x128 obstacle has a projected bounding box about 181.02x90.51. Its projected area is half the current footprint area. At unchanged 704x326 screen framing, the inverse-projected viewport covers 459,008 world square units versus 229,504. This ignores map boundaries and occlusion; it is geometric coverage, not a claim about visible enemies. Both transforms passed 2,178 combined point round trips on a sampled world grid with error below 1e-10.

## Consequence for the next renderer comparison

Do not adopt this matrix globally as a cosmetic fix. Current visible-world dimensions and encounter readability need explicit reconciliation. A uniform zoom of sqrt(2) would restore area alone, but would not restore the old viewport shape, cardinal travel appearance or threat visibility. It is another comparison setting, not an accepted solution.

Apply any candidate consistently to ground geometry, actor roots, prop roots, projectile paths, fields, telegraphs, overlays and camera tracking. Upright art must be authored for that candidate and attached to projected roots rather than compressed with the ground plane. Directional art selection must agree with the projected travel vector. Input needs a documented inverse-direction mapping and analog-magnitude policy; do not change authoritative speed to equalize screen-space movement. The same world-space circle becomes an ellipse under this candidate, so a screen-space circular damage indicator would be false.

Keep the existing projection and gameplay untouched until a real-renderer scene demonstrates the candidate with legal encounters, traversal and contact overlays. The guide provides exact source constraints for a new building master; it does not satisfy that scene gate.

## Research and reproduction

Tiled's primary renderer implements separate forward/inverse isometric coordinate conversion and projects rectangle vertices to polygons: https://github.com/mapeditor/tiled/blob/master/src/libtiled/isometricrenderer.cpp (accessed 2026-10-14). Its object documentation separates image alignment and collision objects: https://doc.mapeditor.org/en/stable/manual/objects/ . These establish an implementation approach, not SS's preferred aesthetic angle. No Tiled code was copied.

Run build_guide.py with --arena pointing to the pinned civic-seam-arena-004.json and --out to a destination directory. It requires Pillow and the macOS Helvetica font. projection.json records exact matrices, viewport corners and verification results. comparison.png is an engineering drawing, not replacement artwork.
