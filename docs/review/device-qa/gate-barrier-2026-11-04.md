# Gate barrier

Read 2026-11-04 from `GateBarrier` on `5d954be`. No gate was moved.

Which gates close stays in [forward-gates-2026-11-04.md](forward-gates-2026-11-04.md).

A closed gate is one of the solids. An open gate is not, so it draws no barrier. The viewer is the player's truncated point. The long axis is vertical when the box's y half-size is greater than its x half-size. Length and depth are twice those half-sizes. The tile count is `max(1, round(length / nominal))`, and `nominal` is `max(1, depth * max(aspect, 0.01))`. The aspect is the barricade texture's width over its height, or `128 / 48` when that texture is absent. The tiles split the length equally and fill the box.

The open face is the long side toward the viewer. An offset below 0 selects face −1. Any other offset, including a viewer on the centre line, selects +1. The warning strip is 4 units deep, inset by `face * (depth / 2 - 2)` from the centre, and it runs the full length.

Lights sit on a pitch of 16, which is length 10 plus gap 6. The count is at least 1 and otherwise `length / pitch` rounded down. The rail is white 0.10 at alpha 0.95. Each light is red 1, green 0.72, blue 0.18, and its thickness is the strip depth minus 1. Without the barricade texture, a tile is white 0.46 with a band of red 0.92, green 0.70, blue 0.16 at half the length and 0.4 of the depth. The barrier root is z 0.5 in the solids layer.

This does not change a collision box.
