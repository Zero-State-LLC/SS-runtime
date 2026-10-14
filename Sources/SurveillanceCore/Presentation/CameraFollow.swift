import Foundation

/// Stateful display-only follow (animation §9 / arena-layout camera framing).
/// RulesViewport and authoritative positions never use this state.
public struct CameraFollow: Sendable {
    public private(set) var x: Double?
    public private(set) var y: Double?
    private var anchorX: Double = 0
    private var anchorY: Double = 0
    public init() {}
    public mutating func reset() { self = Self() }

    public mutating func update(player: VecI, heading: VecQ8, bounds: AABB, deltaTime: Double) {
        let px = Double(player.x), py = Double(player.y)
        if x == nil {
            anchorX = px; anchorY = py
            x = px; y = py
        }
        let halfDeadX = Double(PresentationCamera.deadZoneWidth) / 2
        let halfDeadY = Double(PresentationCamera.deadZoneHeight) / 2
        anchorX = min(max(anchorX, px - halfDeadX), px + halfDeadX)
        anchorY = min(max(anchorY, py - halfDeadY), py + halfDeadY)
        let hx = Double(heading.x.raw), hy = Double(heading.y.raw)
        let length = hypot(hx, hy)
        let look = Double(PresentationCamera.lookAhead)
        let targetX = anchorX + (length > 0 ? hx / length * look : 0)
        let targetY = anchorY + (length > 0 ? hy / length * look : 0)
        // Exponential smoothing is independent of display cadence. Cap resume
        // gaps so a stalled frame cannot turn into a sudden camera jump.
        let dt = deltaTime.isFinite ? min(max(deltaTime, 0), 1.0 / 30) : 0
        let gain = 1 - exp(-dt / 0.12)
        let halfW = Double(PresentationCamera.visibleWidth) / 2
        let halfH = Double(PresentationCamera.visibleHeight) / 2
        func clamp(_ value: Double, _ low: Double, _ high: Double) -> Double {
            low <= high ? min(max(value, low), high) : (low + high) / 2
        }
        x = clamp(x! + (targetX - x!) * gain, Double(bounds.minX) + halfW, Double(bounds.maxX) - halfW)
        y = clamp(y! + (targetY - y!) * gain, Double(bounds.minY) + halfH, Double(bounds.maxY) - halfH)
    }
}
