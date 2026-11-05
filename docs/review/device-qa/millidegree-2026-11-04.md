# Millidegree heading

Read 2026-11-04 from `Cordic` on `fcab4e5`. No angle was changed.

Angles are clockwise from +X. `MilliDeg.circle` is 360,000 and `right` is 90,000. `normalize` is the value modulo 360,000, and a negative remainder is raised by one circle. `delta` is that clockwise gap, kept when it is at most 180,000 and otherwise reported as the shorter step the other way (`diff - circle`). `absDelta` is the absolute value of `delta`.

The Q15 unit is 32,767. `sinCos` starts x at 19,898 and y at 0, reduces the angle to one right angle, and walks this atan table, in millidegrees:

45,000, 26,565, 14,036, 7,125, 3,576, 1,790, 895, 448, 224, 112, 56, 28, 14, 7, 3, 2, 1.

The quadrant is the normalized angle divided by 90,000. Quadrant 0 keeps `(cos, sin) = (x, y)`. Quadrant 1 is `(-y, x)`. Quadrant 2 is `(-x, -y)`. The remaining quadrant is `(y, -x)`.

`headingUnit` returns `(cos, −sin)`. `atan2Milli` is `normalize(circle − atan2CCW)`. A `(0, 0)` counter-clockwise atan2 returns 0, so `atan2Milli(0, 0)` is 0.

This is the arena angle system. The shipping draw projection stays `(x, −y)`.
