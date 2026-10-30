import Testing
@testable import SurveillanceCore

/// D-116 (bosses.md § Pursuit, enemies-and-encounters.md § Corner pursuit).
@Suite struct CaptainCornerPursuitTests {
    private static func chase(from start: VecI, to player: VecI, solids: [AABB]?) throws -> Int64 {
        var sim = try Simulation.make(seed: 1)
        sim.testing_completeMobAndEliteGraph()
        sim.testing_installBoss()
        if let solids { sim.testing_setCollisionSolids(solids) }
        let boss = try #require(sim.state.enemies.first { $0.archetype == .algorithmicModerate })
        sim.testing_setEnemyPosition(boss.id, start)
        var closest = Int64.max
        for _ in 0..<900 {
            sim.testing_setPlayerPosition(player)
            sim.testing_setPlayerIntegrity(150)
            _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
            if let body = sim.state.enemies.first(where: { $0.id == boss.id }) {
                closest = min(closest, IntMath.isqrt(body.position.distanceSquared(to: player.asQ8)) / Q8.scale)
            }
        }
        return closest
    }

    /// BO-025: the Captain against the east face of the service-yard block,
    /// the Player behind its west face. Before D-116 it stood at the face.
    @Test func theCaptainRoundsTheServiceYardBlock() throws {
        let block = AABB(center: VecI(x: 1152, y: 1248), halfSize: VecI(x: 96, y: 160))
        let closest = try Self.chase(from: VecI(x: 1278, y: 1284), to: VecI(x: 980, y: 1300), solids: [block])
        #expect(closest < 90, "came within \(closest) units")
    }

    /// BO-026, a recorded limit: the approach point tests a line, not a body.
    /// With the Player pressed into the far corner of `solid-06` (the probe
    /// trace), the line under the block is clear but the 52-unit gap beside
    /// `mount-cam-z04-b` is narrower than the Captain, so it still holds.
    @Test func aGapNarrowerThanTheCaptainStillHoldsIt() throws {
        let closest = try Self.chase(from: VecI(x: 1278, y: 1284), to: VecI(x: 1036, y: 1435), solids: nil)
        #expect(closest > 90)
    }
}

extension CaptainCornerPursuitTests {
    /// BO-027 (D-117): the debug boss scenario with the Player standing still
    /// at the far spawn. Under D-116 as first written the Captain froze under
    /// `solid-11-court-column-a`, its line to a corner clear but its body not.
    @Test func theCaptainCrossesTheArenaToAStillPlayer() throws {
        var sim = try Simulation.make(seed: 1)
        let seeded = sim.debug_seedScenario("boss")
        #expect(seeded)
        var ticks = 0
        while !sim.isTerminal && ticks < 6_000 {
            _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
            ticks += 1
        }
        #expect(sim.state.outcome == .failure, "the Captain reached the Player within \(ticks) ticks")
    }

    /// D-117: a path counts as clear for the Captain only if its body keeps
    /// its radius from every solid.
    @Test func bodyClearanceRejectsAPathThatGrazesACorner() {
        let column: [(id: String, box: AABB)] = [("column", AABB(center: VecI(x: 1920, y: 704), halfSize: VecI(x: 32, y: 72)))]
        // 26 units under the column: a line clears it, a radius-30 body does not.
        #expect(!CornerPursuit.bodyClear(from: VecI(x: 1966, y: 802).asQ8, to: VecI(x: 1502, y: 802).asQ8, radius: 30, solids: column))
        #expect(CornerPursuit.bodyClear(from: VecI(x: 1966, y: 810).asQ8, to: VecI(x: 1502, y: 810).asQ8, radius: 30, solids: column))
        #expect(CornerPursuit.bodyReachedUnits == 2)
    }
}
