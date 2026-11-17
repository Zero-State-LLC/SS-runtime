#if DEBUG
import SpriteKit
import SurveillanceCore

/// Opt-in live presentation adapter. Authority and action coordinates stay in world space.
/// ADAPT: AppTests/DisplayedPlaybackTests.swift:514-521 (restore before authoring),
/// AppTests/ReferenceProjectionTrial.swift:24-51 (midpoint chain and magnitude-preserving inverse).
@MainActor
final class LiveWorldProjection {
    struct Upright {
        let node: SKNode
        /// Optional world-space attachment, for a screen-space badge offset from an actor root.
        var root: CGPoint? = nil
    }
    private struct Saved {
        let node: SKNode
        let parent: SKNode
        let index: Int
        let position: CGPoint
        let z: CGFloat
    }
    let ground = SKNode()
    let rotation = SKNode()
    let uprightLayer = SKNode()
    private var saved: [Saved] = []
    private var roots: [Saved] = []
    private var cameraPosition: CGPoint?
    private weak var camera: SKCameraNode?
    private(set) var applied = false

    static func requested(arguments: [String], hasReview: Bool) throws -> Bool {
        let flags = arguments.indices.filter { arguments[$0] == "-SSKioskProjection" }
        guard !flags.isEmpty else { return false }
        guard hasReview, flags.count == 1, let flag = flags.first,
              flag + 1 < arguments.count, arguments[flag + 1] == "midpoint" else {
            throw KioskPlayableReview.Invalid.arguments
        }
        return true
    }

    static func analogWorld(_ screen: CGPoint) -> CGPoint {
        let magnitude = hypot(screen.x, screen.y)
        guard magnitude > 0 else { return .zero }
        let world = BenchmarkProjectionGeometry.inverse(screen)
        let length = hypot(world.x, world.y)
        return CGPoint(x: world.x * magnitude / length, y: world.y * magnitude / length)
    }

    init(scene: SKScene, camera: SKCameraNode, worldRoots: [SKNode]) {
        self.camera = camera
        ground.name = "live-midpoint-ground"
        rotation.name = "live-midpoint-world"
        uprightLayer.name = "live-midpoint-uprights"
        ground.yScale = 0.5
        rotation.zRotation = .pi / 4
        scene.addChild(ground)
        ground.addChild(rotation)
        scene.addChild(uprightLayer)
        roots = worldRoots.compactMap { node in
            guard let parent = node.parent, let index = parent.children.firstIndex(of: node) else { return nil }
            return Saved(node: node, parent: parent, index: index, position: node.position, z: node.zPosition)
        }
        for entry in roots {
            entry.node.removeFromParent()
            rotation.addChild(entry.node)
        }
        // Keep authoring space ordinary until the first completed presentation.
        ground.yScale = 1
        rotation.zRotation = 0
    }

    func restore() {
        guard applied else { return }
        for entry in saved {
            // A deliberate removal between frames must not resurrect a stale sprite.
            guard entry.node.parent === uprightLayer else { continue }
            entry.node.removeFromParent()
            entry.node.position = entry.position
            entry.node.zPosition = entry.z
            entry.parent.insertChild(entry.node, at: min(entry.index, entry.parent.children.count))
        }
        saved.removeAll(keepingCapacity: true)
        if let cameraPosition { camera?.position = cameraPosition }
        cameraPosition = nil
        ground.yScale = 1
        rotation.zRotation = 0
        applied = false
    }

    func apply(uprights: [Upright]) {
        guard !applied else { return }
        ground.yScale = 0.5
        rotation.zRotation = .pi / 4
        // Capture indexes before any detach, preserving exact sibling order on restore.
        let entries: [(Upright, Saved)] = uprights.compactMap { item in
            guard let parent = item.node.parent,
                  let index = parent.children.firstIndex(of: item.node) else { return nil }
            return (item, Saved(node: item.node, parent: parent, index: index,
                         position: item.node.position, z: item.node.zPosition))
        }
        saved = entries.map(\.1)
        for (item, entry) in entries {
            let point: CGPoint
            if let root = item.root {
                let projected = BenchmarkProjectionGeometry.project(root)
                point = CGPoint(x: projected.x + entry.position.x - root.x,
                                y: projected.y + entry.position.y - root.y)
            } else {
                point = entry.parent.convert(entry.position, to: uprightLayer)
            }
            var depth = entry.z
            var ancestor: SKNode? = entry.parent
            while let node = ancestor, node !== uprightLayer.parent {
                depth += node.zPosition
                ancestor = node.parent
            }
            entry.node.removeFromParent()
            entry.node.position = point
            entry.node.zPosition = depth
            uprightLayer.addChild(entry.node)
        }
        cameraPosition = camera?.position
        if let cameraPosition { camera?.position = BenchmarkProjectionGeometry.project(cameraPosition) }
        applied = true
    }

    func remove() {
        restore()
        for entry in roots {
            entry.node.removeFromParent()
            entry.parent.insertChild(entry.node, at: min(entry.index, entry.parent.children.count))
        }
        roots.removeAll()
        ground.removeFromParent()
        uprightLayer.removeFromParent()
    }
}
#endif
