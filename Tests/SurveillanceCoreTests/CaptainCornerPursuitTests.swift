import Testing
@testable import SurveillanceCore

/// D-116 (bosses.md § Pursuit, enemies-and-encounters.md § Corner pursuit).
@Suite struct CaptainCornerPursuitTests {
    /// BO-013, the probe trace behind the intent: before D-116 the Captain
    /// stood against the east face of `solid-06-service-yard-a` for 2.5
    /// minutes while the Player stood below and behind it.
    @Test func theCaptainRoundsTheServiceYard() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_completeMobAndEliteGraph()
        sim.testing_installBoss()
        let boss = try #require(sim.state.enemies.first { $0.archetype == .algorithmicModerate })
        sim.testing_setEnemyPosition(boss.id, VecI(x: 1278, y: 1284))
        let player = VecI(x: 1036, y: 1435)
        var closest = Int64.max
        for _ in 0..<900 {
            sim.testing_setPlayerPosition(player)
            sim.testing_setPlayerIntegrity(150)
            _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
            if let body = sim.state.enemies.first(where: { $0.id == boss.id }) {
                closest = min(closest, IntMath.isqrt(body.position.distanceSquared(to: player.asQ8)) / Q8.scale)
            }
        }
        #expect(closest < 90, "came within \(closest) units")
    }
}
