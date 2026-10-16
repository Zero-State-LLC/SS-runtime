import SpriteKit

/// Review-only texture injection. The test target owns all candidate files.
/// It cannot alter simulation geometry or asset admission records.
@MainActor
struct BenchmarkReviewArt {
    struct GroundPatch {
        let texture: SKTexture
        let bounds: CGRect
        let tileUnits: CGFloat
    }
    struct GroundLine {
        let start: CGPoint
        let end: CGPoint
        let width: CGFloat
        let color: SKColor
    }
    struct Placement {
        let texture: SKTexture
        let size: CGSize
        let anchor: CGPoint
        let position: CGPoint
    }
    enum PlayerPresentation: Equatable {
        case staticComposition
        case selectedClip
    }
    // Environment injection must not erase action/event ownership in live reviews.
    var playerPresentation: PlayerPresentation = .staticComposition
    let player: SKTexture
    let camera: SKTexture
    let building: Placement
    let buildingID: String
    let props: [Placement]
    let paving: SKTexture
    var cameraStates: [Int: SKTexture] = [:]
    var groundPatches: [GroundPatch] = []
    var groundLines: [GroundLine] = []
    /// One proposed street arrangement shared by static and animated reviews.
    /// World-space decoration only: never changes the arena or collision data.
    mutating func configureStreetCorner(asphalt: SKTexture) {
        groundPatches = [
            .init(texture: asphalt, bounds: CGRect(x: 900, y: 0, width: 1404, height: 1536), tileUnits: 128),
            .init(texture: asphalt, bounds: CGRect(x: 0, y: 0, width: 900, height: 480), tileUnits: 128)
        ]
        func line(_ a: CGPoint, _ b: CGPoint, _ width: CGFloat, _ value: CGFloat) -> GroundLine {
            .init(start: a, end: b, width: width, color: SKColor(white: value, alpha: 1))
        }
        groundLines = []
        // Layered curb edge, with a gap aligned to the south crossing.
        for (width, shade): (CGFloat, CGFloat) in [(8, 0.22), (5, 0.57)] {
            groundLines.append(line(CGPoint(x: 896, y: 484), CGPoint(x: 896, y: 1536), width, shade))
            groundLines.append(line(CGPoint(x: 0, y: 484), CGPoint(x: 492, y: 484), width, shade))
            groundLines.append(line(CGPoint(x: 564, y: 484), CGPoint(x: 896, y: 484), width, shade))
        }
        // Rails sit inside the road; muted crossing paint does not rival cues.
        for x: CGFloat in [960, 1000] {
            groundLines.append(line(CGPoint(x: x, y: 0), CGPoint(x: x, y: 1536), 5, 0.12))
            groundLines.append(line(CGPoint(x: x, y: 0), CGPoint(x: x, y: 1536), 1.5, 0.55))
        }
        for y in stride(from: 464, through: 320, by: -24) {
            groundLines.append(line(CGPoint(x: 496, y: y), CGPoint(x: 560, y: y), 10, 0.62))
        }
    }

}

/// Geometry for the BP-007 review projection only. Not the gameplay/rules viewport.
enum BenchmarkProjectionGeometry {
    static func project(_ point: CGPoint) -> CGPoint {
        let r = CGFloat(0.5).squareRoot()
        return CGPoint(x: r * (point.x - point.y), y: r * (point.x + point.y) / 2)
    }

    static func inverse(_ point: CGPoint) -> CGPoint {
        let r = CGFloat(0.5).squareRoot()
        return CGPoint(x: (point.x + 2 * point.y) / (2 * r),
                       y: (2 * point.y - point.x) / (2 * r))
    }

    /// Ground containment can conflict with player visibility; callers must measure both.
    static func containedCenter(desired: CGPoint, bounds: CGRect,
                                viewport: CGSize, magnification: CGFloat) -> CGPoint? {
        guard magnification.isFinite, magnification > 0,
              viewport.width.isFinite, viewport.height.isFinite,
              viewport.width > 0, viewport.height > 0,
              desired.x.isFinite, desired.y.isFinite,
              bounds.origin.x.isFinite, bounds.origin.y.isFinite,
              bounds.width.isFinite, bounds.height.isFinite,
              bounds.width > 0, bounds.height > 0 else { return nil }
        let margin = (viewport.width / 2 + viewport.height) / (CGFloat(2).squareRoot() * magnification)
        guard bounds.width >= 2 * margin, bounds.height >= 2 * margin else { return nil }
        return CGPoint(x: min(max(desired.x, bounds.minX + margin), bounds.maxX - margin),
                       y: min(max(desired.y, bounds.minY + margin), bounds.maxY - margin))
    }
    /// Candidate priority: keep the registered player canvas visible, reporting
    /// outside-arena coverage separately. No gameplay bound is changed.
    static func playerVisibleCenter(desired: CGPoint, bounds: CGRect, viewport: CGSize,
                                    magnification: CGFloat, player: CGPoint, canvas: CGRect,
                                    safeRegion: CGRect? = nil) -> CGPoint? {
        guard let contained = containedCenter(desired: desired, bounds: bounds,
                                               viewport: viewport, magnification: magnification),
              player.x.isFinite, player.y.isFinite,
              canvas.origin.x.isFinite, canvas.origin.y.isFinite,
              canvas.width.isFinite, canvas.height.isFinite,
              canvas.width > 0, canvas.height > 0,
              canvas.width * magnification <= viewport.width,
              canvas.height * magnification <= viewport.height else { return nil }
        let point = project(player), initial = project(contained)
        let viewportRect = CGRect(x: -viewport.width / 2, y: -viewport.height / 2,
                                  width: viewport.width, height: viewport.height)
        let region = safeRegion ?? viewportRect
        guard !region.isNull, !region.isInfinite,
              viewportRect.contains(region),
              region.width >= canvas.width * magnification,
              region.height >= canvas.height * magnification else { return nil }
        let minX = point.x + canvas.maxX - region.maxX / magnification
        let maxX = point.x + canvas.minX - region.minX / magnification
        let minY = point.y + canvas.maxY - region.maxY / magnification
        let maxY = point.y + canvas.minY - region.minY / magnification
        return inverse(CGPoint(x: min(max(initial.x, minX), maxX),
                               y: min(max(initial.y, minY), maxY)))
    }

    /// Static diagnostic composition, not a dynamic HUD-follow policy.
    /// Enumerating obstacle edges finds the maximal center-containing rectangle.
    static func unobstructedRegion(viewport: CGRect, exclusions: [CGRect],
                                   minimumSize: CGSize) -> CGRect? {
        guard !viewport.isNull, !viewport.isInfinite, viewport.width > 0, viewport.height > 0,
              minimumSize.width.isFinite, minimumSize.height.isFinite,
              minimumSize.width > 0, minimumSize.height > 0,
              exclusions.allSatisfy({ !$0.isNull && !$0.isInfinite }) else { return nil }
        let obstacles = exclusions.map { $0.intersection(viewport) }
            .filter { !$0.isNull && $0.width > 0 && $0.height > 0 }
        let xs = Set([viewport.minX, viewport.maxX] + obstacles.flatMap { [$0.minX, $0.maxX] }).sorted()
        let ys = Set([viewport.minY, viewport.maxY] + obstacles.flatMap { [$0.minY, $0.maxY] }).sorted()
        var best: CGRect?
        for left in xs where left <= viewport.midX {
            for right in xs where right >= viewport.midX && right-left >= minimumSize.width {
                for bottom in ys where bottom <= viewport.midY {
                    for top in ys where top >= viewport.midY && top-bottom >= minimumSize.height {
                        let candidate = CGRect(x: left, y: bottom, width: right-left, height: top-bottom)
                        guard !obstacles.contains(where: {
                            let overlap = candidate.intersection($0)
                            return !overlap.isNull && overlap.width > 0 && overlap.height > 0
                        }) else { continue }
                        if best == nil || candidate.width * candidate.height > best!.width * best!.height {
                            best = candidate
                        }
                    }
                }
            }
        }
        return best
    }

}
