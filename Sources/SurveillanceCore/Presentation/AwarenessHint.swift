/// Presentation-only D-089 tutorial copy (`hud-tutorial.md` "First unaware
/// enemy on screen"). Derived from the snapshot; it never writes simulation
/// state and never enters the digest.
///
/// It shows once per run: the first time a snapshot has an unaware enemy
/// inside the visible viewport, for the tutorial card's maximum visual
/// duration. It is a tutorial hint, not a safety message, so the tutorial
/// setting hides it.
public struct AwarenessHintProjector: Equatable, Sendable {
    public static let copy = "UNSEEN ENEMIES HOLD • STRIKE FIRST FOR TRIPLE DAMAGE"

    /// `hud-tutorial.md`: each card's maximum visual duration.
    public static let visibleTicks: UInt64 = 300

    /// Top-left reference rectangle. The layout table does not place this
    /// copy; it takes the row under the heat caption's borrowed Boss
    /// Integrity slot, clear of the tutorial card, which it must not
    /// replace. It and the heat caption do not show together in practice:
    /// a wave has reinforcements only while `tracked` or above, and that
    /// state alerts every unaware enemy.
    public static let referenceRect = HUDRect(x: 422 - 180, y: 108, width: 360, height: 24)

    private var shownAt: UInt64?

    public init() {}

    public mutating func reset() {
        self = AwarenessHintProjector()
    }

    /// True when an unaware enemy lies inside the viewport the snapshot's
    /// presentation camera shows.
    public static func unawareEnemyOnScreen(_ snap: PresentationSnapshot) -> Bool {
        let halfWidth = PresentationCamera.visibleWidth / 2
        let halfHeight = PresentationCamera.visibleHeight / 2
        return snap.enemies.contains { enemy in
            enemy.unaware
                && abs(enemy.x - snap.camera.center.x) <= halfWidth
                && abs(enemy.y - snap.camera.center.y) <= halfHeight
        }
    }

    /// Equivalent visibility query without constructing unrelated render data.
    public static func unawareEnemyOnScreen(_ state: WorldState) -> Bool {
        let camera = PresentationCamera.follow(
            player: VecI(x: state.player.position.x.unitsTruncated, y: state.player.position.y.unitsTruncated),
            heading: state.player.facing, bounds: state.arena.boundsUnits)
        return state.enemies.contains { enemy in
            enemy.alive && enemy.isUnaware && PresentationCamera.contains(
                VecI(x: enemy.position.x.unitsTruncated, y: enemy.position.y.unitsTruncated),
                center: camera.center)
        }
    }

    /// The copy to draw for `snap`, or nil.
    public mutating func project(_ snap: PresentationSnapshot) -> String? {
        project(tick: snap.tick, visible: Self.unawareEnemyOnScreen(snap))
    }

    /// Session path: same hint semantics without full rendering projection.
    public mutating func project(_ state: WorldState) -> String? {
        project(tick: state.tick, visible: Self.unawareEnemyOnScreen(state))
    }

    private mutating func project(tick: UInt64, visible: @autoclosure () -> Bool) -> String? {
        if shownAt == nil, visible() { shownAt = tick }
        guard let shownAt, tick >= shownAt, tick - shownAt < Self.visibleTicks else { return nil }
        return Self.copy
    }
}
