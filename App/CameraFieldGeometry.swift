import CoreGraphics
import Foundation
import SurveillanceCore

/// Display-only visibility polygon; never used to decide detection.
/// All occluders and the fractional emitter origin come from the snapshot.
enum CameraFieldGeometry {
    struct Key: Equatable {
        let originX: Double
        let originY: Double
        let range: Int
        let heading: Int
        let angle: Int
        let solids: [AABB]
        init(camera: PresentationSnapshot.CameraSprite, solids: [AABB]) {
            originX = camera.fieldOrigin.map { Double($0.x.raw) / Double(Q8.scale) } ?? Double(camera.x)
            originY = camera.fieldOrigin.map { Double($0.y.raw) / Double(Q8.scale) } ?? Double(camera.y)
            range = camera.range; heading = camera.headingMilli; angle = camera.fieldAngleMilli
            self.solids = solids
        }
    }

    static func path(_ key: Key) -> CGPath {
        let path = CGMutablePath()
        let origin = CGPoint(x: key.originX, y: key.originY)
        guard key.range > 0, key.angle > 0 else { return path }
        let base = -Double(key.heading) * .pi / 180_000
        let half = Double(key.angle) * .pi / 360_000
        // Sample the range arc and both sides of every obstacle corner. Uniform
        // rays alone can bridge over a narrow occluder between adjacent rays.
        let count = max(1, Int(ceil(Double(key.angle) / 1_000)))
        var angles = (0...count).map { -half + 2 * half * Double($0) / Double(count) }
        for box in key.solids {
            for x in [box.minX, box.maxX] {
                for y in [box.minY, box.maxY] {
                    let a = atan2(Double(y) - key.originY, Double(x) - key.originX) - base
                    let relative = atan2(sin(a), cos(a))
                    for offset in [-1e-7, 0, 1e-7] where abs(relative + offset) <= half {
                        angles.append(relative + offset)
                    }
                }
            }
        }
        path.move(to: origin)
        for angle in angles.sorted() {
            let dx = cos(base + angle), dy = sin(base + angle)
            var reach = Double(key.range)
            for box in key.solids {
                if let entry = entry(origin: origin, dx: dx, dy: dy, box: box) {
                    reach = min(reach, entry)
                }
            }
            path.addLine(to: CGPoint(x: key.originX + dx * reach, y: key.originY + dy * reach))
        }
        path.closeSubpath()
        return path
    }

    private static func entry(origin: CGPoint, dx: Double, dy: Double, box: AABB) -> Double? {
        var near = -Double.infinity, far = Double.infinity
        for (o, d, lo, hi) in [(Double(origin.x), dx, Double(box.minX), Double(box.maxX)),
                               (Double(origin.y), dy, Double(box.minY), Double(box.maxY))] {
            if abs(d) < 1e-12 {
                if o < lo || o > hi { return nil }
            } else {
                let a = (lo - o) / d, b = (hi - o) / d
                near = max(near, min(a, b)); far = min(far, max(a, b))
            }
        }
        guard near <= far, far >= 0 else { return nil }
        return max(0, near)
    }
}
