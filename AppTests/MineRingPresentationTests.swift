import CoreGraphics
import SpriteKit
import Testing
@testable import SSRuntime
@testable import SurveillanceCore

/// T1060 / D-121. The Vendor mine is a stroke-only ring at the snapshot
/// radius. Arming is width 2. Armed is width 4. The fill stays clear.
@Suite(.serialized)
@MainActor
struct MineRingPresentationTests {
    /// SpriteKit stores an assigned gray `SKColor` as float components in
    /// extended sRGB. Compare at the thousandth, which is the precision of
    /// white 0.92 and alpha 0.95.
    private static func rgba(_ color: SKColor) -> (CGFloat, CGFloat, CGFloat, CGFloat) {
        let space = CGColorSpace(name: CGColorSpace.extendedSRGB)!
        let converted = color.cgColor.converted(to: space, intent: .defaultIntent, options: nil) ?? color.cgColor
        let parts = converted.components ?? []
        let thousandth = { (index: Int) -> CGFloat in
            let value = index < parts.count ? parts[index] : -1
            return (value * 1000).rounded() / 1000
        }
        return (thousandth(0), thousandth(1), thousandth(2), thousandth(3))
    }

    @Test func ringIsClearStrokeAtTheAuthoredRadius() throws {
        let state = try Simulation.make(seed: 1).state
        let mine = try #require(state.content.standardEnemies[.victorianVendor]?.mine)
        var snap = PresentationSnapshot(state)
        let arming = PresentationSnapshot.MineSprite(
            id: EntityID(7),
            x: 40,
            y: 50,
            radius: mine.radius,
            armed: false,
            armRemaining: mine.arm,
            lifeRemaining: mine.lifetime
        )
        let armed = PresentationSnapshot.MineSprite(
            id: EntityID(8),
            x: 80,
            y: 90,
            radius: mine.radius,
            armed: true,
            armRemaining: 0,
            lifeRemaining: mine.lifetime
        )
        snap.mines = [arming, armed]

        let renderer = WorldRenderer()
        renderer.render(snap)

        let armingNode = try #require(renderer.root.childNode(withName: "//mine-7") as? SKShapeNode)
        let armedNode = try #require(renderer.root.childNode(withName: "//mine-8") as? SKShapeNode)
        let authored = SKShapeNode(circleOfRadius: CGFloat(mine.radius))
        let authoredBounds = try #require(authored.path).boundingBox
        let clear = (CGFloat(0), CGFloat(0), CGFloat(0), CGFloat(0))
        let neutral = (CGFloat(0.92), CGFloat(0.92), CGFloat(0.92), CGFloat(0.95))
        #expect(Self.rgba(Palette.mineStroke) == neutral)
        for (sprite, node) in [(arming, armingNode), (armed, armedNode)] {
            #expect(Self.rgba(node.fillColor) == clear)
            #expect(Self.rgba(node.strokeColor) == neutral)
            #expect(node.path?.boundingBox == authoredBounds)
            #expect(node.position == CGPoint(x: sprite.x, y: sprite.y))
        }
        #expect(armingNode.lineWidth == 2)
        #expect(armedNode.lineWidth == 4)

        snap.mines = []
        renderer.render(snap)
        #expect(renderer.root.childNode(withName: "//mine-7") == nil)
        #expect(renderer.root.childNode(withName: "//mine-8") == nil)
    }
}
