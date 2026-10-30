import Testing
@testable import SurveillanceCore

/// D-114 (enemies-and-encounters.md § Corner pursuit).
@Suite struct CornerPursuitTests {
    private let box: [(id: String, box: AABB)] = [("block", AABB(center: VecI(x: 0, y: 0), halfSize: VecI(x: 100, y: 100)))]

    @Test func aClearLineSteersStraightAtTheTarget() {
        let target = VecI(x: 300, y: 300).asQ8
        #expect(CornerPursuit.waypoint(from: VecI(x: 300, y: 0).asQ8, to: target, radius: 20, solids: box) == target)
    }

    /// The target is behind the box and nearer its lower edge: the lower
    /// near corner, outside the box by radius + 4.
    @Test func aBlockedLineSteersForTheCornerOnTheShortWayRound() {
        let corner = CornerPursuit.waypoint(
            from: VecI(x: 200, y: 60).asQ8, to: VecI(x: -200, y: 80).asQ8, radius: 20, solids: box
        )
        #expect(corner == VecI(x: 124, y: 124).asQ8)
    }

    /// At that corner the target is still hidden; the next corner along,
    /// which sees it, is chosen rather than the one just reached.
    @Test func aReachedCornerHandsOnToTheNext() {
        let corner = CornerPursuit.waypoint(
            from: VecI(x: 124, y: 124).asQ8, to: VecI(x: -200, y: 80).asQ8, radius: 20, solids: box
        )
        #expect(corner == VecI(x: -124, y: 124).asQ8)
    }

    /// Exactly symmetric: the first corner in the specified order wins.
    @Test func tiesResolveInCornerOrder() {
        let corner = CornerPursuit.waypoint(
            from: VecI(x: 200, y: 0).asQ8, to: VecI(x: -200, y: 0).asQ8, radius: 20, solids: box
        )
        #expect(corner == VecI(x: 124, y: -124).asQ8)
    }

    /// Scratch trace from the intent: behind `solid-06-service-yard-a`, with
    /// the Player held still, direct pursuit stopped level with the Player at
    /// the far face. Corner pursuit arrives.
    @Test(arguments: [ArchetypeID.autonomousInformant, .cableCarCorrelator])
    func aChaserBehindTheServiceYardReachesThePlayer(archetype: ArchetypeID) throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_completeEncounter("M-A")
        sim.testing_selectUpgrade(.ghostStep)
        let player = VecI(x: 1024, y: 1380)
        sim.testing_setPlayerPosition(player)
        let id = sim.testing_spawnStandard(archetype, at: VecI(x: 1268, y: 1282))
        var closest = Int64.max
        for _ in 0..<600 {
            sim.testing_setPlayerPosition(player)
            _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
            if let enemy = sim.state.enemies.first(where: { $0.id == id }) {
                closest = min(closest, IntMath.isqrt(enemy.position.distanceSquared(to: player.asQ8)) / Q8.scale)
            }
        }
        #expect(closest < 60, "came within \(closest) units")
    }

    /// A Correlator in charge range with the block between never winds up a
    /// charge into the wall.
    @Test func noChargeWithoutAClearLine() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_completeEncounter("M-A")
        sim.testing_selectUpgrade(.ghostStep)
        let player = VecI(x: 1024, y: 1300)
        sim.testing_setPlayerPosition(player)
        let id = sim.testing_spawnStandard(.cableCarCorrelator, at: VecI(x: 1268, y: 1250))
        for _ in 0..<240 {
            sim.testing_setPlayerPosition(player)
            _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
            guard let enemy = sim.state.enemies.first(where: { $0.id == id }) else { break }
            if !Collision.lineOfFireClear(from: enemy.position, to: player.asQ8, solids: sim.state.liveSolids) {
                #expect(enemy.state != .telegraph && enemy.state != .charge)
            }
        }
    }

    @Test func theConstantsAreTheSpecifiedOnes() {
        #expect(CornerPursuit.cornerMarginUnits == 4)
        #expect(CornerPursuit.reachedUnits == 8)
    }
}
