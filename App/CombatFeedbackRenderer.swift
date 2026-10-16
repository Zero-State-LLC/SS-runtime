import SpriteKit
import SurveillanceCore

/// CC-008. Four persistent shapes; no per-frame node allocation, gameplay
/// mutation, random motion, or retained entity history.
@MainActor
final class CombatFeedbackRenderer {
    let root = SKNode()
    let aim = SKShapeNode()
    let discharge = SKShapeNode(circleOfRadius: 6)
    let jammer = SKShapeNode()
    let concealment = SKShapeNode()
    private var shotTick: UInt64?
    private var lastTick: UInt64?

    init() {
        root.zPosition = 19
        aim.name = "civic-pulse-aim"
        discharge.name = "civic-pulse-discharge"
        jammer.name = "signal-jammer-active"
        concealment.name = "ghost-step-concealment"
        let aimPath = CGMutablePath()
        aimPath.addLines(between: [CGPoint(x: 23, y: -5), CGPoint(x: 31, y: 0), CGPoint(x: 23, y: 5)])
        aim.path = aimPath
        let warm = SKColor(red: 1, green: 0.94, blue: 0.78, alpha: 1)
        aim.strokeColor = warm
        discharge.strokeColor = warm
        discharge.fillColor = warm.withAlphaComponent(0.65)
        jammer.path = Self.segmentedContour(radius: 27, segments: 8)
        jammer.strokeColor = SKColor(red: 0.3, green: 0.85, blue: 0.9, alpha: 1)
        // Four right-angle corners distinguish concealment from interference
        // even without colour. It is not the circular damage-immunity symbol.
        let corners = CGMutablePath()
        for (x, y) in [(1.0, 1.0), (-1.0, 1.0), (-1.0, -1.0), (1.0, -1.0)] {
            corners.move(to: CGPoint(x: x * 19, y: y * 32))
            corners.addLine(to: CGPoint(x: x * 32, y: y * 32))
            corners.addLine(to: CGPoint(x: x * 32, y: y * 19))
        }
        concealment.path = corners
        concealment.strokeColor = SKColor(white: 0.95, alpha: 1)
        for shape in [aim, discharge, jammer, concealment] {
            shape.lineWidth = 2
            shape.isHidden = true
            root.addChild(shape)
        }
    }

    func reset() {
        shotTick = nil
        lastTick = nil
        for node in root.children { node.isHidden = true; node.removeAllActions() }
    }

    func update(_ snap: PresentationSnapshot, events: [AuthoritativeEvent], settings: PresentationVFXSettings) {
        if let lastTick, snap.tick < lastTick { reset() }
        let fresh = snap.tick != lastTick
        lastTick = snap.tick
        guard !snap.outcome.isTerminal, !snap.upgradePending else {
            for node in root.children { node.isHidden = true }
            shotTick = nil
            return
        }
        let player = CGPoint(x: snap.player.x, y: snap.player.y)
        if fresh, let shot = snap.combatFeedback.shot,
           events.contains(where: { $0.tick == snap.tick && $0.type == .weaponFired && $0.primaryEntityId == shot.projectile }),
           shot.velocity != .zero {
            shotTick = snap.tick
            aim.position = player
            aim.zRotation = atan2(CGFloat(shot.velocity.y.raw), CGFloat(shot.velocity.x.raw))
            discharge.position = CGPoint(x: CGFloat(shot.origin.x.raw) / CGFloat(Q8.scale),
                                         y: CGFloat(shot.origin.y.raw) / CGFloat(Q8.scale))
        }
        let shooting = shotTick.map { snap.tick >= $0 && snap.tick - $0 < 6 } ?? false
        aim.isHidden = !shooting
        aim.position = player
        discharge.isHidden = !shooting
        // Reduced motion/flash is a static outline for the same truthful cue.
        discharge.fillColor = settings.reducedMotion || settings.reducedFlash ? .clear : aim.strokeColor.withAlphaComponent(0.65)
        jammer.isHidden = !snap.combatFeedback.jammerReducedExposure
        jammer.position = player
        jammer.zRotation = settings.reducedMotion || settings.reducedFlash ? 0 : CGFloat(snap.tick % 120) * .pi / 60
        concealment.isHidden = !snap.ghostConcealmentActive
        concealment.position = player
    }

    private static func segmentedContour(radius: CGFloat, segments: Int) -> CGPath {
        let path = CGMutablePath()
        for index in 0..<segments {
            let start = CGFloat(index) * 2 * .pi / CGFloat(segments)
            path.move(to: CGPoint(x: radius * cos(start), y: radius * sin(start)))
            path.addArc(center: .zero, radius: radius, startAngle: start,
                        endAngle: start + .pi / CGFloat(segments), clockwise: false)
        }
        return path
    }
}
