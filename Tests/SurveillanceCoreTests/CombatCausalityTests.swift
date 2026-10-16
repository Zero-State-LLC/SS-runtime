import Testing
@testable import SurveillanceCore

@Suite(.serialized)
struct CombatCausalityTests {
    @Test(arguments: [false, true])
    func actualSweepOrdersTargetAndWall(wallFirst: Bool) throws {
        var sim = try Simulation.make(seed: 1)
        let p = sim.state.player.position
        let x = p.x.unitsTruncated + 100
        let y = p.y.unitsTruncated
        let targetX = x + 40
        sim.testing_spawnInformant(at: VecI(x: targetX, y: y), integrity: 100, speed: 0)
        let enemy = try #require(sim.state.enemies.last)
        let wallX = wallFirst ? x + 5 : x + 70
        sim.testing_setCollisionSolids([AABB(center: VecI(x: wallX + 1, y: y), halfSize: VecI(x: 1, y: 30))])
        sim.testing_injectMovingPulse(from: VecI(x: x, y: y).asQ8, velocity: VecI(x: 90, y: 0).asQ8)
        let result = sim.step(command: .neutral(tick: 1))
        let hits = result.events.filter { $0.type == .projectileHit && $0.secondaryEntityId == enemy.id }
        #expect(hits.count == (wallFirst ? 0 : 1))
    }

    @Test func realWallEntityTieIsBlocked() throws {
        var sim = try Simulation.make(seed: 1)
        let x = sim.state.player.position.x.unitsTruncated + 100
        let y = sim.state.player.position.y.unitsTruncated
        sim.testing_spawnInformant(at: VecI(x: x + 40, y: y), integrity: 100, speed: 0)
        let enemy = try #require(sim.state.enemies.last)
        let entry = x + 40 - enemy.radius - Targeting.projectileRadius
        sim.testing_setCollisionSolids([AABB(center: VecI(x: entry + 1, y: y), halfSize: VecI(x: 1, y: 30))])
        sim.testing_injectMovingPulse(from: VecI(x: x, y: y).asQ8, velocity: VecI(x: 90, y: 0).asQ8)
        let result = sim.step(command: .neutral(tick: 1))
        #expect(!result.events.contains { $0.type == .projectileHit && $0.secondaryEntityId == enemy.id })
    }

    @Test func stationaryAndMissedWallSweepsAreDefined() {
        let wall = AABB(center: VecI(x: 10, y: 0), halfSize: VecI(x: 2, y: 2))
        #expect(Collision.segmentEntryTime(VecI(x: 10, y: 0).asQ8, VecI(x: 10, y: 0).asQ8, box: wall) == 0)
        #expect(Collision.segmentEntryTime(.zero, .zero, box: wall) == nil)
        #expect(Collision.segmentEntryTime(.zero, VecI(x: 20, y: 0).asQ8, box: wall) == 102)
    }

    @Test func startInsideCircleHitsAtEntryNotExit() {
        #expect(Collision.sweepCircleTime(from: .zero, to: VecI(x: 20, y: 0).asQ8,
                                         radius: 4, target: .zero, targetRadius: 2) == 0)
    }

    @Test func mineEvidenceNamesHazardRatherThanOwner() throws {
        var sim = try Simulation.make(seed: 1)
        let point = VecI(x: sim.state.player.position.x.unitsTruncated + 10,
                         y: sim.state.player.position.y.unitsTruncated)
        sim.testing_insertMine(at: point, armRemaining: 0)
        let mine = try #require(sim.state.mines.last)
        let result = sim.step(command: .neutral(tick: 1))
        let hit = try #require(result.events.first { $0.type == .playerDamaged })
        #expect(hit.secondaryEntityId == mine.id)
        #expect(hit.payload["ownerEntityId"] == .string(mine.ownerId.decimalString))
        #expect(hit.payload["sourceXQ8"] == .integer(mine.position.x.raw))
        #expect(hit.payload["damageKind"] == .string("mine"))
        #expect(!sim.state.mines.contains { $0.id == mine.id })
    }

    @Test func contactEvidenceListsAllCurrentContributors() throws {
        var sim = try Simulation.make(seed: 1)
        let point = VecI(x: sim.state.player.position.x.unitsTruncated,
                         y: sim.state.player.position.y.unitsTruncated)
        for _ in 0..<3 { sim.testing_spawnInformant(at: point, integrity: 100, speed: 0) }
        let ids = sim.state.enemies.map(\.id).sorted()
        var contact: AuthoritativeEvent?
        for tick in 1...20 {
            let result = sim.step(command: .neutral(tick: UInt64(tick)))
            if let found = result.events.first(where: { $0.type == .playerDamaged && $0.payload["damageKind"] == .string("contact") }) {
                contact = found; break
            }
        }
        let hit = try #require(contact)
        #expect(hit.payload["contributors"] == .array(ids.map { .string($0.decimalString) }))
    }

    @Test func retiredProjectileRetainsIncomingPoint() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_injectHostileBolt()
        let shot = try #require(sim.state.projectiles.last)
        let result = sim.step(command: .neutral(tick: 1))
        let hit = try #require(result.events.first { $0.type == .playerDamaged })
        #expect(hit.payload["sourceXQ8"] == .integer(shot.previous.x.raw))
        #expect(hit.payload["damageKind"] == .string("projectile"))
        #expect(!sim.state.projectiles.contains { $0.id == shot.id && $0.alive })
    }
}
