import SpriteKit

/// BP-001 isolated test mapping. This is not a production projection or art approval.
struct ReferenceProjectionTrial {
    let name: String
    let degrees: CGFloat
    let yScale: CGFloat

    static let midpoint = Self(name: "midpoint", degrees: 45, yScale: 0.5)
    // Direction fit: docs/review/bp001-reference-trial-20261116/ground-fit.json.
    // Absolute world scale, translation and upright art are not recovered.
    static let reference = Self(name: "reference-fit", degrees: -29.755022433623864,
                                yScale: 1.0180179537588112)
    static let candidates = [reference, midpoint]
    static let referenceImageSHA256 = "49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb"
    static let landmarksSHA256 = "4da2792b52b2ca13b61b950f26d30b2d3cdfbd8260474d146da588c2e153a484"

    var radians: CGFloat { degrees * .pi / 180 }
    var matrix: [CGFloat] {
        [cos(radians), -sin(radians), yScale * sin(radians), yScale * cos(radians)]
    }

    func forward(_ p: CGPoint) -> CGPoint {
        let m = matrix
        return CGPoint(x: m[0] * p.x + m[1] * p.y, y: m[2] * p.x + m[3] * p.y)
    }

    func inverse(_ p: CGPoint) -> CGPoint {
        CGPoint(x: cos(radians) * p.x + sin(radians) * p.y / yScale,
                y: -sin(radians) * p.x + cos(radians) * p.y / yScale)
    }

    /// Preserve stick magnitude, not screen travel speed. No shipping input change.
    func analogWorld(_ p: CGPoint) -> CGPoint {
        let magnitude = hypot(p.x, p.y)
        guard magnitude > 0 else { return .zero }
        let world = inverse(p)
        let length = hypot(world.x, world.y)
        return CGPoint(x: world.x / length * magnitude, y: world.y / length * magnitude)
    }

    @MainActor
    func groundChain(center: CGPoint) -> (root: SKNode, coordinates: SKNode) {
        let scale = SKNode(), rotate = SKNode(), translate = SKNode()
        scale.position = center
        scale.yScale = yScale
        rotate.zRotation = radians
        translate.position = CGPoint(x: -center.x, y: -center.y)
        scale.addChild(rotate)
        rotate.addChild(translate)
        return (scale, translate)
    }
}
