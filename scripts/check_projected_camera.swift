import Foundation
import SpriteKit

@main
struct ProjectedCameraCheck {
    static func main() throws {
        let bounds = CGRect(x: 0, y: 0, width: 2304, height: 1536)
        let viewport = CGSize(width: 704, height: 326)
        var checked = 0
        for zoom: CGFloat in [0.75, 1, 1.25, 1.4] {
            for x: CGFloat in [-100, 0, 18, 1152, 2286, 2304, 2500] {
                for y: CGFloat in [-100, 0, 18, 768, 1518, 1536, 1700] {
                    let center = BenchmarkProjectionGeometry.containedCenter(
                        desired: CGPoint(x: x, y: y), bounds: bounds, viewport: viewport, magnification: zoom)!
                    // Independent SpriteKit inverse: scale, rotation, world translation.
                    let scene = SKScene(), scale = SKNode(), rotation = SKNode(), translation = SKNode()
                    scale.xScale = zoom; scale.yScale = zoom / 2
                    rotation.zRotation = .pi / 4; translation.position = CGPoint(x: -center.x, y: -center.y)
                    scene.addChild(scale); scale.addChild(rotation); rotation.addChild(translation)
                    for sx: CGFloat in [-352, 352] {
                        for sy: CGFloat in [-163, 163] {
                            let world = scene.convert(CGPoint(x: sx, y: sy), to: translation)
                            let epsilon: CGFloat = 0.002 // Float-backed SpriteKit transform precision only.
                            precondition(world.x >= bounds.minX - epsilon && world.x <= bounds.maxX + epsilon)
                            precondition(world.y >= bounds.minY - epsilon && world.y <= bounds.maxY + epsilon)
                            let independent = BenchmarkProjectionGeometry.inverse(CGPoint(x: sx / zoom, y: sy / zoom))
                            precondition(abs(world.x - center.x - independent.x) < epsilon)
                            precondition(abs(world.y - center.y - independent.y) < epsilon)
                            checked += 1
                        }
                    }
                }
            }
        }
        precondition(BenchmarkProjectionGeometry.containedCenter(desired: .zero,
            bounds: CGRect(x: 0, y: 0, width: 100, height: 100), viewport: viewport, magnification: 1) == nil)
        precondition(BenchmarkProjectionGeometry.containedCenter(desired: .zero,
            bounds: bounds, viewport: viewport, magnification: 0) == nil)
        let screen = CGRect(x: -352, y: -163, width: 704, height: 326)
        // Synthetic boundary fixtures exercise geometry; iOS captures supply real HUD bounds.
        let exclusions = [CGRect(x: -352, y: 100, width: 704, height: 63),
            CGRect(x: -352, y: -163, width: 160, height: 140),
            CGRect(x: 240, y: -163, width: 112, height: 110)]
        var hudChecks = 0
        for zoom: CGFloat in [0.75, 1, 1.25, 1.4] {
            let region = BenchmarkProjectionGeometry.unobstructedRegion(viewport: screen,
                exclusions: exclusions, minimumSize: CGSize(width: 64*zoom, height: 64*zoom))!
            precondition(screen.contains(region))
            for exclusion in exclusions {
                let overlap = region.intersection(exclusion)
                precondition(overlap.isNull || overlap.width == 0 || overlap.height == 0)
            }
            for x: CGFloat in [18, 1152, 2286] { for y: CGFloat in [18,768,1518] {
                let player = CGPoint(x: x, y: y)
                let focus = BenchmarkProjectionGeometry.playerVisibleCenter(desired: player, bounds: bounds,
                    viewport: viewport, magnification: zoom, player: player,
                    canvas: CGRect(x: -32, y: -8, width: 64, height: 64), safeRegion: region)!
                let projected = BenchmarkProjectionGeometry.project(CGPoint(x: x-focus.x, y: y-focus.y))
                let canvas = CGRect(x: (projected.x-32)*zoom, y: (projected.y-8)*zoom,
                    width: 64*zoom, height: 64*zoom)
                precondition(region.insetBy(dx: -0.000001, dy: -0.000001).contains(canvas))
                hudChecks += 1
            } }
        }
        precondition(BenchmarkProjectionGeometry.unobstructedRegion(viewport: screen,
            exclusions: [screen], minimumSize: CGSize(width: 64, height: 64)) == nil)
        precondition(BenchmarkProjectionGeometry.unobstructedRegion(viewport: screen,
            exclusions: [], minimumSize: CGSize(width: 705, height: 64)) == nil)
        precondition(BenchmarkProjectionGeometry.unobstructedRegion(viewport: screen,
            exclusions: [], minimumSize: CGSize(width: 64, height: 64)) == screen)
        var conflict: [[String: Any]] = []
        for zoom: CGFloat in [1, 1.25] {
            for player in [CGPoint(x: 18, y: 18), CGPoint(x: 2286, y: 1518), CGPoint(x: 1327, y: 1495)] {
                let focus = BenchmarkProjectionGeometry.containedCenter(desired: player, bounds: bounds,
                    viewport: viewport, magnification: zoom)!
                let p = BenchmarkProjectionGeometry.project(CGPoint(x: player.x-focus.x, y: player.y-focus.y))
                let root = CGPoint(x: p.x * zoom, y: p.y * zoom)
                let canvas = CGRect(x: root.x-32*zoom, y: root.y-8*zoom, width: 64*zoom, height: 64*zoom)
                let frame = CGRect(x: -352, y: -163, width: 704, height: 326)
                let playerCanvas = CGRect(x: -32, y: -8, width: 64, height: 64)
                let safe = BenchmarkProjectionGeometry.playerVisibleCenter(desired: player, bounds: bounds,
                    viewport: viewport, magnification: zoom, player: player, canvas: playerCanvas)!
                let safeOffset = BenchmarkProjectionGeometry.project(CGPoint(x: player.x-safe.x, y: player.y-safe.y))
                let safeRect = CGRect(x: (safeOffset.x+playerCanvas.minX)*zoom,
                    y: (safeOffset.y+playerCanvas.minY)*zoom, width: 64*zoom, height: 64*zoom)
                precondition(frame.insetBy(dx: -0.000001, dy: -0.000001).contains(safeRect))
                var overshootX: CGFloat = 0, overshootY: CGFloat = 0
                for sx: CGFloat in [-352,352] { for sy: CGFloat in [-163,163] {
                    let d = BenchmarkProjectionGeometry.inverse(CGPoint(x: sx/zoom,y: sy/zoom))
                    let world = CGPoint(x: safe.x+d.x,y: safe.y+d.y)
                    overshootX = max(overshootX,bounds.minX-world.x,world.x-bounds.maxX)
                    overshootY = max(overshootY,bounds.minY-world.y,world.y-bounds.maxY)
                } }
                conflict.append(["zoom": zoom, "player": [player.x,player.y], "focus": [focus.x,focus.y],
                    "rootVisible": frame.contains(root), "canvasVisible": frame.contains(canvas),
                    "playerVisibleFocus": [safe.x,safe.y], "playerVisibleCanvas": true,
                    "requiredBackdropOvershootXY": [overshootX,overshootY]])
            }
        }
        precondition(conflict.contains { ($0["rootVisible"] as? Bool) == false })
        let data = try JSONSerialization.data(withJSONObject: ["spriteKitCornerChecks": checked,
            "invalidInputChecks": 2, "hudSafeBoundaryChecks": hudChecks, "hudRegionEdgeCases": 3, "visibilityConflicts": conflict,
            "scope": "Host SpriteKit geometry, not iOS displayed framing or production camera admission"], options: [.prettyPrinted,.sortedKeys])
        print(String(decoding: data, as: UTF8.self))
    }
}
