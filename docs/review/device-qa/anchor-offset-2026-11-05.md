# The camera offset

Read 2026-11-05 from `CameraPlacement.fieldOrigin` and `targetAnchor` on `ef68565`. No socket was moved. The offset numbers stay in [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md). The heading unit and `q15` stay in [millidegree-2026-11-04.md](millidegree-2026-11-04.md). Half-away division stays in [q8-scale-2026-11-04.md](q8-scale-2026-11-04.md).

`fieldOrigin` offsets the socket by `fieldOriginOffset`. `targetAnchor` offsets it by `targetAnchorOffset`. Both use the socket heading.

The local x is to the right of the heading. The local y is forward along it. The heading unit is `(fx, fy)`. The right vector is `(fy, -fx)`. Each world component starts at the socket coordinate times `Q8.scale`, then adds `mulDivHalfAway` of the right component times the local x times that scale, over `q15`, and the same product for the forward component and the local y.

This does not move a socket.
