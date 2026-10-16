// BP-007 host SpriteKit diagnostic. No app or simulation acceptance is implied.
import Foundation
import SpriteKit

let scene = SKScene(size: CGSize(width: 704, height: 326))
let center = CGPoint(x: 736, y: 654)
let squash = SKNode(), rotation = SKNode(), translation = SKNode()
squash.position = center
squash.yScale = 0.5
rotation.zRotation = .pi / 4
translation.position = CGPoint(x: -center.x, y: -center.y)
scene.addChild(squash)
squash.addChild(rotation)
rotation.addChild(translation)
let r = CGFloat(0.5).squareRoot()
let directions: [(CGFloat, CGFloat)] = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
var samples = 0
var maximumError: CGFloat = 0
for (x, y) in directions {
    for magnitude: CGFloat in [0.25, 0.5, 1, 120] {
        let length = hypot(x, y)
        let dx = x / length * magnitude, dy = y / length * magnitude
        let point = CGPoint(x: center.x + dx, y: center.y + dy)
        let actual = translation.convert(point, to: scene)
        let expected = CGPoint(x: center.x + r * (dx - dy), y: center.y + r * (dx + dy) / 2)
        let recovered = scene.convert(actual, to: translation)
        let error = max(abs(actual.x - expected.x), abs(actual.y - expected.y),
                        abs(recovered.x - point.x), abs(recovered.y - point.y))
        maximumError = max(maximumError, error)
        // SpriteKit stores transforms at Float precision. Budget eight ULPs for
        // composed forward/inverse arithmetic, not a visual contact tolerance.
        let tolerance = CGFloat(Float(max(abs(point.x), abs(point.y), 1)).ulp) * 8
        precondition(error <= tolerance, "Projection/inverse mismatch: \(error), bound \(tolerance)")
        samples += 1
    }
}
let screenDownWorld = scene.convert(CGPoint(x: center.x, y: center.y - 1), to: translation)
precondition(screenDownWorld.x < center.x && screenDownWorld.y < center.y)
print("PASS: \(samples) host SpriteKit forward/inverse samples; maximum error \(maximumError) points; screen-down maps to world SW")
