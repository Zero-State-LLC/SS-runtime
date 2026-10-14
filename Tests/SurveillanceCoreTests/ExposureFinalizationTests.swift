import Testing
@testable import SurveillanceCore

/// D-102 / T410: real phase ordering, not a direct call to the Exposure helper.
struct ExposureFinalizationTests {
    private func fogCrossing() throws -> Simulation {
        var sim = try Simulation.make(seed: 1)
        sim.testing_keepCameras([], integrity: 3)
        for _ in 0..<61 { sim.step(command: nil) }
        sim.testing_setExposure(432)
        sim.testing_insertEnemy(EnemyBody(
            id: EntityID(999_999), archetype: .fogAnalyticsCloud,
            position: sim.state.player.position, velocity: .zero,
            integrity: 10_000, radius: 16, speedUnitsPerSecond: 0, contactDps: 0,
            state: .telegraph, stateTicks: 1, spawnTick: 0,
            nextSpecialTick: 0, encounterId: "audit-fog"
        ))
        return sim
    }

    @Test func fogCrossingRevokesQuietBeforeRecoveryCanEraseIt() throws {
        var sim = try fogCrossing()
        sim.step(command: nil)
        #expect(sim.state.exposure.exposure == 450)
        #expect(sim.state.exposure.detectionState == .tracked)
        #expect(!sim.state.exposure.quietApproach)
        sim.step(command: nil)
        #expect(sim.state.exposure.exposure == 448)
        #expect(sim.state.exposure.detectionState == .observed)
        #expect(!sim.state.exposure.quietApproach)
    }

    @Test func fogCrossingPublishesOneFinalDetectionEvent() throws {
        var sim = try fogCrossing()
        let result = sim.step(command: nil)
        let changes = result.events.filter { $0.type == .detectionStateChanged }
        #expect(changes.count == 1)
        #expect(changes.first?.payload["before"] == .string("observed"))
        #expect(changes.first?.payload["after"] == .string("tracked"))
    }
    @Test func fogTransitionReachesAudioAndVFX() throws {
        var sim = try fogCrossing()
        let result = sim.step(command: nil)
        var audio = AudioProjector()
        let projected = audio.project(tick: result.tick, events: result.events, world: .from(sim.state))
        #expect(projected.cues.contains { $0.audioId == "exposure_state_up" })
        #expect(projected.captions.contains("Detection tracked"))
        var vfx = VFXProjector()
        let frame = vfx.project(tick: result.tick, events: result.events, catalog: try .bundled())
        #expect(frame.presentations.filter { $0.recipeId == "exposureThreshold" }.count == 1)
    }

    @Test func signalJammerModifiesTheFogPulseExactlyOnce() throws {
        var sim = try fogCrossing()
        sim.testing_selectUpgrade(.signalJammer)
        let result = sim.step(command: nil)
        #expect(sim.state.exposure.exposure == 445)
        #expect(sim.state.exposure.quietApproach)
        #expect(!result.events.contains { $0.type == .detectionStateChanged })
    }

    @Test func lethalTickSuppressesNamedPulsesButStillResolvesRecovery() throws {
        var sim = try fogCrossing()
        sim.testing_setPlayerIntegrity(1)
        sim.testing_injectHostileBolt(damage: 100)
        let result = sim.step(command: nil)
        #expect(result.outcome == .failure)
        #expect(sim.state.exposure.exposure == 430)
        #expect(!result.events.contains { $0.payload["reason"] == .string("fogPulse") })
        let terminalTick = sim.state.tick
        let next = sim.step(command: nil)
        #expect(next.events.isEmpty)
        #expect(sim.state.tick == terminalTick)
    }

    @Test func forcedMobCLockdownWithDueFogKeepsQuiet() throws {
        var sim = try fogCrossing()
        sim.testing_completeEncounter("M-A")
        sim.testing_completeEncounter("M-B")
        let trigger = try #require(sim.state.arena.encounterTriggers.first { $0.encounterId == "M-C" })
        sim.testing_setPlayerPosition(trigger.aabb.center)
        // Add a due pulse at the actual M-C trigger, not at the old position.
        sim.testing_insertEnemy(EnemyBody(
            id: EntityID(999_998), archetype: .fogAnalyticsCloud,
            position: sim.state.player.position, velocity: .zero,
            integrity: 10_000, radius: 16, speedUnitsPerSecond: 0, contactDps: 0,
            state: .telegraph, stateTicks: 1, spawnTick: 0,
            nextSpecialTick: 0, encounterId: "audit-fog"
        ))
        let result = sim.step(command: nil)
        #expect(sim.state.encounters["M-C"]?.activated == true)
        #expect(sim.state.exposure.exposure == 1000)
        #expect(sim.state.exposure.quietApproach)
        let lockdown = result.events.filter { $0.type == .lockdownEntered }
        #expect(lockdown.count == 1)
        #expect(lockdown.first?.phase == 14)
        #expect(lockdown.first?.payload["reason"] == .string("forcedLockdown"))
    }

    @Test func allDeltasProduceOneFinalStateAndOneLockdown() {
        var state = ExposureState(exposure: 440, detectionState: .observed)
        let result = state.resolveTick(survivingContactCount: 1, tamperAmounts: [150],
                                      signalJammer: false, fogPulseAmounts: [20, 20],
                                      observationPulseAmounts: [400, 30])
        #expect(result.stateBefore == .observed)
        #expect(result.stateAfter == .lockdown)
        #expect(result.after == 1000)
        #expect(result.lockdownEnteredThisTick)
        #expect(result.reason == .observationPulse)
        #expect(result.changes.map(\.after) == [592, 612, 632, 1000])
        let next = state.resolveTick(survivingContactCount: 0, tamperAmounts: [],
                                    signalJammer: false, observationPulseAmounts: [400])
        #expect(!next.lockdownEnteredThisTick)
        #expect(next.changes.isEmpty)
    }

    @Test func multipleFogPulsesEmitOnlyTheFinalTransition() throws {
        var sim = try fogCrossing()
        sim.testing_insertEnemy(EnemyBody(
            id: EntityID(999_998), archetype: .fogAnalyticsCloud,
            position: sim.state.player.position, velocity: .zero,
            integrity: 10_000, radius: 16, speedUnitsPerSecond: 0, contactDps: 0,
            state: .telegraph, stateTicks: 1, spawnTick: 0,
            nextSpecialTick: 0, encounterId: "audit-fog"
        ))
        let result = sim.step(command: nil)
        #expect(sim.state.exposure.exposure == 470)
        #expect(result.events.filter { $0.type == .detectionStateChanged }.count == 1)
        #expect(result.events.filter { $0.payload["reason"] == .string("fogPulse") }.count == 2)
    }

    @Test func recoveryAndPulseDoNotPublishAnIntermediateState() throws {
        var sim = try fogCrossing()
        sim.testing_setExposure(450)
        let result = sim.step(command: nil)
        #expect(sim.state.exposure.exposure == 468)
        #expect(sim.state.exposure.detectionState == .tracked)
        #expect(!sim.state.exposure.quietApproach)
        #expect(!result.events.contains { $0.type == .detectionStateChanged })
    }

}
