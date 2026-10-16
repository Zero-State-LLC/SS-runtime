import Foundation

/// The per-tick presentation state for medals (D-095) and feel pass 2
/// (D-097, D-098), fed by the app's session after every step.
///
/// It consumes the tick's published events, the enemy list before the step,
/// and the state after it. It owns no simulation and is never read by one:
/// `FeelPassPresentationOnlyTests` runs the same commands with and without it
/// and compares the digest and the receipt.
public struct FeelPassPresenter: Equatable, Sendable {
    public private(set) var medals = MedalTracker()
    public private(set) var takedowns = TakedownTracker()
    public private(set) var tutorial = TutorialLineQueue()
    public private(set) var encounterLabels = EncounterLabelGate()
    /// This tick's takedowns (D-097), by ascending ID.
    public private(set) var lastTakedowns: [EntityID] = []
    /// Patrol members whose cone edge is lit (D-097 near miss).
    public private(set) var nearMiss: [EntityID] = []
    /// The single tutorial line to draw (D-098), or nil.
    public private(set) var tutorialLine: String?
    /// The combat objective copy to draw (D-098), or nil before its
    /// encounter activates.
    public private(set) var objectiveCopy: String?

    public init() {}

    public mutating func reset() {
        self = FeelPassPresenter()
    }

    /// Before a step: learn the patrol (for `SHADOW`).
    public mutating func willStep(_ state: WorldState) {
        medals.notePatrol(state)
    }

    /// After a step.
    public mutating func didStep(events: [AuthoritativeEvent], enemiesBefore: [EnemyBody], state: WorldState) {
        medals.ingest(events)
        lastTakedowns = takedowns.ingest(events: events, before: enemiesBefore, after: state.enemies)
        observe(state)
    }

    /// Refreshes everything derived from the current state alone (also used
    /// once a debug scenario has rewritten the state).
    public mutating func observe(_ state: WorldState) {
        let player = VecI(x: state.player.position.x.unitsTruncated, y: state.player.position.y.unitsTruncated)
        let camera = PresentationCamera.follow(player: player, heading: state.player.facing, bounds: state.arena.boundsUnits)
        let node = CombatAuthoritySnapshot.project(state).currentNode
        let copy = HUDLayout.combatObjectiveCopy(
            node: node, extractionArmed: state.extraction.armed,
            insideLockedExtraction: state.arena.extraction.aabb.contains(player) && !state.extraction.armed)
        nearMiss = PatrolNearMiss.members(state)
        objectiveCopy = encounterLabels.project(copy: copy, node: node, tick: state.tick, state: state)
        // Match PatrolConeProjection's membership exactly, including zero-facing
        // exclusion, without computing the clipped outlines just to test origins.
        let patrol = Set(state.enemies.filter {
            $0.alive && $0.isUnaware && $0.patrol.map { $0.facing != .zero } == true
        }.map(\.id))
        var patrolVisible = false
        var unawareVisible = false
        for enemy in state.enemies where enemy.alive && enemy.isUnaware {
            guard PresentationCamera.contains(
                VecI(x: enemy.position.x.unitsTruncated, y: enemy.position.y.unitsTruncated),
                center: camera.center) else { continue }
            if patrol.contains(enemy.id) { patrolVisible = true } else { unawareVisible = true }
        }
        var hints: [String] = []
        if patrolVisible { hints.append(PatrolTutorial.copy) }
        if unawareVisible { hints.append(AwarenessHintProjector.copy) }
        let safety = state.tutorial.copyIsSafetyMessage
        let card = safety || state.tutorial.copy.isEmpty ? nil : state.tutorial.copy
        let blocked = state.upgrade.pending || safety || encounterLabels.isFresh(node, tick: state.tick)
        tutorialLine = tutorial.update(card: card, hints: hints, blocked: blocked)
    }

    /// The D-089 hint is about unaware enemies in general; a patrol member's
    /// cone has its own line, so the patrol alone does not raise this one.
    static func unawareNonPatrolOnScreen(_ snap: PresentationSnapshot) -> Bool {
        let patrol = Set(snap.patrolCones.map(\.id))
        return snap.enemies.contains { enemy in
            enemy.unaware && !patrol.contains(enemy.id)
                && PresentationCamera.contains(VecI(x: enemy.x, y: enemy.y), center: snap.camera.center)
        }
    }

    /// The tick's audio with the takedown's pitch and caption (D-097).
    public func decorate(_ audio: AudioProjection) -> AudioProjection {
        StealthTexture.decorate(audio, takedowns: lastTakedowns)
    }

    /// § 8c streak copy, or nil.
    public var streakCopy: String? { takedowns.hudCopy }

    /// The medals `state` earned (§ 12), empty unless it succeeded.
    public func earnedMedals(_ state: WorldState) -> [Medal] {
        medals.medals(for: state)
    }
}
