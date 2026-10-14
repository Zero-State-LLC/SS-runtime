import Testing
@testable import SurveillanceCore

@Suite struct WeaponUpgradeFeedbackTests {
    @Test func shotEvidenceSurvivesRetirementAndIgnoresMovementFacing() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_keepCameras([], integrity: 3)
        sim.testing_setCollisionSolids([])
        for _ in 0..<29 { sim.step(command: nil) }
        #expect(sim.combatFeedback.shot == nil)
        let p = sim.state.player.position
        sim.testing_spawnInformant(at: VecI(x: p.x.unitsTruncated - 10, y: p.y.unitsTruncated), integrity: 100, speed: 0)
        let result = sim.step(command: .init(tick: 30, moveX: 32767, moveY: 0, dodgePressed: false))
        let shot = try #require(sim.combatFeedback.shot)
        #expect(shot.velocity.x.raw < 0)
        #expect(sim.state.player.facing.x.raw > 0)
        #expect(shot.origin == sim.state.player.position)
        #expect(result.events.contains { $0.type == .weaponFired && $0.primaryEntityId == shot.projectile })
        #expect(!sim.state.projectiles.contains { $0.id == shot.projectile && $0.alive })
        sim.step(command: nil)
        #expect(sim.combatFeedback.shot == nil)
        sim.restart()
        #expect(sim.combatFeedback == CombatFeedbackFrame())
    }

    @Test func noTargetProducesNoShotEvidence() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_keepCameras([], integrity: 3)
        for _ in 0..<60 {
            let result = sim.step(command: nil)
            #expect(sim.combatFeedback.shot == nil)
            #expect(!result.events.contains { $0.type == .weaponFired })
        }
    }

    @Test(arguments: [false, true])
    func concealmentMatchesExactWindowAndNotOrdinaryDodge(ghost: Bool) throws {
        var sim = try Simulation.make(seed: 1)
        if ghost { sim.testing_selectUpgrade(.ghostStep) }
        sim.step(command: .init(tick: 1, moveX: 32767, moveY: 0, dodgePressed: true))
        for tick in 1...31 {
            #expect(PresentationSnapshot(sim.state).ghostConcealmentActive == (ghost && tick <= 30))
            if tick < 31 { sim.step(command: nil) }
        }
        sim.restart()
        #expect(!PresentationSnapshot(sim.state).ghostConcealmentActive)
    }

    @Test(arguments: [0, 999, 1000])
    func jammerContourRequiresActualUnclampedFogReduction(exposure: Int) throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_keepCameras([], integrity: 3)
        sim.testing_selectUpgrade(.signalJammer)
        sim.testing_setExposure(exposure)
        sim.testing_insertEnemy(EnemyBody(id: EntityID(999_999), archetype: .fogAnalyticsCloud,
            position: sim.state.player.position, velocity: .zero, integrity: 10_000, radius: 16,
            speedUnitsPerSecond: 0, contactDps: 0, state: .telegraph, stateTicks: 1,
            spawnTick: 0, nextSpecialTick: 0, encounterId: "feedback-fog"))
        sim.step(command: nil)
        #expect(sim.combatFeedback.jammerReducedExposure == (exposure == 0))
        sim.step(command: nil)
        #expect(!sim.combatFeedback.jammerReducedExposure)
    }

    @Test func jammerDoesNotClaimTamperOrIdleReduction() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_selectUpgrade(.signalJammer)
        sim.step(command: nil)
        #expect(!sim.combatFeedback.jammerReducedExposure)
        sim.testing_keepOnlyCamera(at: 0, integrity: 1)
        sim.testing_injectPulseHitting(camera: sim.state.cameras[0])
        let result = sim.step(command: nil)
        #expect(result.events.contains { $0.type == .cameraDestroyed })
        #expect(!sim.combatFeedback.jammerReducedExposure)
    }

    @Test func jammerTracksRealCameraContactThenClearsOutsideField() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_selectUpgrade(.signalJammer)
        sim.testing_keepOnlyCamera(at: 0, integrity: 3)
        sim.testing_setCollisionSolids([], preserveCameras: true)
        sim.testing_relocateCamera(at: 0, position: .init(x: 200, y: 200), headingMilli: MilliDeg.right)
        sim.testing_setPlayerPosition(.init(x: 300, y: 200))
        sim.step(command: nil)
        #expect(sim.state.cameras[0].wasDetecting)
        #expect(sim.state.exposure.exposure == 1)
        #expect(sim.combatFeedback.jammerReducedExposure)
        sim.testing_setPlayerPosition(.init(x: 100, y: 200))
        sim.step(command: nil)
        #expect(!sim.combatFeedback.jammerReducedExposure)
    }

    @Test func jammerTracksActualBossObservationPulse() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_selectUpgrade(.signalJammer)
        sim.testing_keepCameras([], integrity: 3)
        sim.testing_setCollisionSolids([])
        sim.testing_installBoss()
        sim.testing_activateBossField(remaining: 181)
        let emitter = try #require(sim.state.bossRuntime?.activeEmitter)
        sim.testing_setPlayerPosition(emitter.position)
        let result = sim.step(command: nil)
        #expect(result.events.contains { $0.payload["reason"] == .string("observationPulse") })
        #expect(sim.combatFeedback.jammerReducedExposure)
    }

    @Test func cardsExplainExclusionsAndExposeDistinctNonColourIcons() {
        let cards = UpgradePresentation.selectionCards()
        #expect(cards.map(\.selectionIndex) == [0, 1, 2])
        #expect(Set(cards.map(\.symbolName)).count == 3)
        #expect(cards.allSatisfy { !$0.effect.isEmpty && !$0.exclusions.isEmpty })
        #expect(cards[0].voiceOverLabel.contains("No Tamper or damage reduction"))
        #expect(cards[1].voiceOverLabel.contains("clear line of sight"))
        #expect(cards[2].voiceOverLabel.contains("Fog, Observation and Tamper still apply"))
    }
}
