import Testing
@testable import SurveillanceCore

/// D-118 (bosses.md § Captain path search). Every arena vector here is a case
/// in which an earlier rule left the Captain standing still.
@Suite struct CaptainPathTests {
    private static func chase(from start: VecI, to player: VecI, solids: [AABB]? = nil, ticks: Int = 900) throws -> Int64 {
        var sim = try Simulation.make(seed: 1)
        sim.testing_completeMobAndEliteGraph()
        sim.testing_installBoss()
        if let solids { sim.testing_setCollisionSolids(solids) }
        let boss = try #require(sim.state.enemies.first { $0.archetype == .algorithmicModerate })
        sim.testing_setEnemyPosition(boss.id, start)
        var closest = Int64.max
        for _ in 0..<ticks {
            sim.testing_setPlayerPosition(player)
            sim.testing_setPlayerIntegrity(150)
            _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
            if let body = sim.state.enemies.first(where: { $0.id == boss.id }) {
                closest = min(closest, IntMath.isqrt(body.position.distanceSquared(to: player.asQ8)) / Q8.scale)
            }
        }
        return closest
    }

    /// BO-025: east of a lone block, the Player held behind its west face.
    /// Before D-116 the Captain stopped at the face.
    @Test func theCaptainRoundsALoneBlock() throws {
        let block = AABB(center: VecI(x: 1152, y: 1248), halfSize: VecI(x: 96, y: 160))
        let closest = try Self.chase(from: VecI(x: 1278, y: 1284), to: VecI(x: 980, y: 1300), solids: [block])
        #expect(closest < 90, "came within \(closest) units")
    }

    /// BO-026: the Player pressed into the far corner of `solid-06`, beyond a
    /// 52-unit gap the Captain cannot pass. D-116 held it at the gap; the path
    /// search goes the long way round.
    @Test(arguments: [
        // (start, Player): the narrow gap, then the D-117 freezes at the
        // service divider (probe seed 34) and at the top edge (seed 46).
        (VecI(x: 1278, y: 1284), VecI(x: 1036, y: 1435)),
        (VecI(x: 1336, y: 828), VecI(x: 1290, y: 1415)),
        (VecI(x: 2156, y: 427), VecI(x: 2214, y: 32)),
    ])
    func theCaptainReachesThePlayerWhereEarlierRulesFroze(start: VecI, player: VecI) throws {
        let closest = try Self.chase(from: start, to: player, ticks: 1_800)
        #expect(closest < 90, "came within \(closest) units")
    }

    #if DEBUG
    /// BO-027: the debug boss scenario, the Player standing still at the far
    /// spawn. Under D-116 as first written the Captain froze under
    /// `solid-11-court-column-a`.
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
    #endif

    /// BO-028: a leg is clear only if the body keeps its radius from every
    /// solid. 26 units under a column, a line passes and a radius-30 body
    /// does not.
    @Test func aLegMustClearTheBody() {
        let column = [AABB(center: VecI(x: 1920, y: 704), halfSize: VecI(x: 32, y: 72))]
        #expect(!CaptainPath.clear((1966, 802), (1502, 802), radius: 30, boxes: column))
        #expect(CaptainPath.clear((1966, 810), (1502, 810), radius: 30, boxes: column))
        // A body already touching the column may leave along it.
        #expect(CaptainPath.clear((1982, 704), (1982, 900), radius: 30, boxes: column))
    }

    /// The memoised graph is the graph: same inputs, same waypoint, cached or not.
    @Test func theCacheChangesNothing() throws {
        let sim = try Simulation.make(seed: 1)
        let bounds = sim.state.arena.boundsUnits.aabb
        let boxes = sim.state.liveSolids.sorted { $0.id.utf8LessThan($1.id) }.map(\.box)
        let fresh = CaptainPath.Graph(radius: 30, bounds: bounds, boxes: boxes)
        let cached = CaptainPath.Graph.cached(radius: 30, bounds: bounds, boxes: boxes)
        #expect(fresh.nodes.elementsEqual(cached.nodes) { $0 == $1 })
        let a = fresh.firstWaypoint(from: (1966, 802), to: (160, 192), radius: 30, boxes: boxes)
        let b = cached.firstWaypoint(from: (1966, 802), to: (160, 192), radius: 30, boxes: boxes)
        #expect(a.map { [$0.0, $0.1] } == b.map { [$0.0, $0.1] })
        #expect(a != nil)
    }
}
