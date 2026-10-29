import Testing
@testable import SurveillanceCore

/// D-109: exposure.md § Court release (EX-021–EX-024) and bosses.md § Court
/// Lockdown (BO-010–BO-012).
@Suite(.serialized)
struct CourtReleaseTests {
    /// M-A and M-B complete, M-C activated (forced Lockdown) and completed,
    /// every Camera switched off, then the Daemon defeated.
    private static func released(destroyCameras: Int = 0) throws -> Simulation {
        var sim = try Simulation.make(seed: 1)
        sim.testing_completeEncounter("M-A")
        sim.testing_completeEncounter("M-B")
        for index in 0..<destroyCameras { sim.testing_destroyCameraAtIndex(index) }
        let trigger = try #require(sim.state.arena.encounterTriggers.first { $0.encounterId == "M-C" })
        sim.testing_setPlayerPosition(trigger.aabb.center)
        _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
        #expect(sim.state.exposure.lockdownEntered)
        // No M-C waves (Fog pulses would move Exposure), no Camera contact,
        // and enough Integrity that no test ends in a terminal failure.
        sim.testing_completeEncounter("M-C")
        sim.testing_keepCameras([], integrity: 0)
        sim.testing_setPlayerIntegrity(100_000)
        sim.testing_defeatElite()
        return sim
    }

    @Test func ex021TheDaemonReleasesTheLatchAndTheNextTickResolvesHunted() throws {
        var sim = try Self.released()
        #expect(sim.state.eliteDefeated)
        #expect(!sim.state.exposure.lockdownEntered)
        #expect(sim.state.exposure.exposure == 700)
        #expect(sim.state.exposure.detectionState == .lockdown, "unchanged until the next resolution")
        let result = sim.step(command: .neutral(tick: sim.state.tick + 1))
        let changes = result.events.filter { $0.type == .detectionStateChanged }
        #expect(changes.count == 1)
        #expect(changes.first?.payload["before"] == .string("lockdown"))
        #expect(changes.first?.payload["after"] == .string("hunted"))
        #expect(!result.events.contains { $0.type == .lockdownEntered })
        #expect(sim.state.exposure.detectionState == .hunted)
    }

    @Test func ex022LockdownInTheCourtLatchesForTheRestOfTheRun() throws {
        var sim = try Self.released()
        _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
        sim.testing_setExposure(1000)
        let entered = sim.step(command: .neutral(tick: sim.state.tick + 1))
        #expect(entered.events.filter { $0.type == .lockdownEntered }.count == 1)
        for _ in 0..<120 { _ = sim.step(command: .neutral(tick: sim.state.tick + 1)) }
        #expect(sim.state.exposure.lockdownEntered)
        #expect(sim.state.exposure.exposure == 1000)
        #expect(sim.state.exposure.detectionState == .lockdown)
    }

    @Test func ex023ExposureRecoversInTheCourt() throws {
        var sim = try Self.released()
        for _ in 0..<62 { _ = sim.step(command: .neutral(tick: sim.state.tick + 1)) }
        #expect(sim.state.exposure.exposure < 700)
        #expect(sim.state.exposure.detectionState == .tracked)
    }

    @Test func ex024TheFloorNeitherRaisesTheReleaseNorLetsItRecover() throws {
        var sim = try Self.released(destroyCameras: 6)
        #expect(sim.state.destructions.count == 6)
        #expect(sim.state.exposure.exposure == 700)
        for _ in 0..<62 { _ = sim.step(command: .neutral(tick: sim.state.tick + 1)) }
        #expect(sim.state.exposure.exposure == 700)
    }

    /// Ticks until the Captain's next telegraph starts, from `cooldown`.
    private static func ticksToNextTelegraph(cooldown: Int, courtLockdown: Bool) throws -> Int {
        var sim = try Self.released()
        _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
        if courtLockdown {
            sim.testing_setExposure(1000)
            _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
            #expect(sim.state.exposure.lockdownEntered)
        }
        sim.testing_installBoss()
        sim.testing_setBossCooldown(cooldown)
        for elapsed in 1...1000 {
            _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
            if (sim.state.bossRuntime?.telegraphRemaining ?? 0) > 0 { return elapsed }
        }
        Issue.record("no telegraph within 1000 ticks")
        return -1
    }

    @Test func bo010CourtLockdownHalvesTheCooldown() throws {
        let normal = try Self.ticksToNextTelegraph(cooldown: 90, courtLockdown: false)
        let pressed = try Self.ticksToNextTelegraph(cooldown: 90, courtLockdown: true)
        #expect(normal == 91, "90 cooldown ticks, then the telegraph starts")
        #expect(pressed == 46, "45 cooldown ticks at 2 per tick, then the telegraph starts")
    }

    @Test func bo011TelegraphLengthIsUnchanged() throws {
        var sim = try Self.released()
        _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
        sim.testing_setExposure(1000)
        _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
        sim.testing_installBoss()
        sim.testing_beginBossTelegraph(.safetyRationale, remaining: 45)
        var elapsed = 0
        while (sim.state.bossRuntime?.telegraphRemaining ?? 0) > 0, elapsed < 100 {
            _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
            elapsed += 1
        }
        #expect(elapsed == 45)
    }

    @Test func bo012WithoutCourtLockdownTheCooldownIsUnchanged() throws {
        #expect(try Self.ticksToNextTelegraph(cooldown: 120, courtLockdown: false) == 121)
    }

    @Test func theStepIsTwo() {
        #expect(BossSystem.courtLockdownCooldownStep == 2)
        #expect(ExposureState.courtReleaseExposure == 700)
    }
}
