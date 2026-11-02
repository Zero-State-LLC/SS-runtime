import Testing
@testable import SurveillanceCore

@Suite(.serialized)
struct LethalWarningTests {
    @Test func contactHorizonMatchesTheScaledRemainder() {
        // 60 dps for 60 ticks is 60 unscaled points. At 50% that removes 30.
        #expect(LethalWarning.contactWouldExhaust(
            integrity: 30, remainderHundredths: 0, accumulator: 0, dps: 60, percent: 50
        ))
        #expect(!LethalWarning.contactWouldExhaust(
            integrity: 31, remainderHundredths: 0, accumulator: 0, dps: 60, percent: 50
        ))
        // Boss contact is 10. Sixty ticks are 10 points, and 10 at 50% removes 5.
        #expect(LethalWarning.contactWouldExhaust(
            integrity: 5, remainderHundredths: 0, accumulator: 0, dps: 10, percent: 50
        ))
        #expect(!LethalWarning.contactWouldExhaust(
            integrity: 6, remainderHundredths: 0, accumulator: 0, dps: 10, percent: 50
        ))
    }

    @Test func aQuietPlayerAtOneIntegrityStaysQuiet() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_setPlayerIntegrity(1)
        #expect(!LethalWarning.isOn(sim.state))
        #expect(sim.state.tutorial.copy != LethalWarning.card)
    }

    @Test func contactOnTheWorldUsesTheSameHorizon() throws {
        var sim = try Simulation.make(seed: 1)
        let id = sim.testing_spawnStandard(.autonomousInformant, at: playerPoint(sim))
        sim.testing_setEnemyCombat(id, contactDps: 60)
        sim.testing_setPlayerIntegrity(30)
        #expect(LethalWarning.isOn(sim.state))
        sim.testing_setPlayerIntegrity(31)
        #expect(!LethalWarning.isOn(sim.state))
    }

    @Test func anUnawareEnemyDoesNotCount() throws {
        var sim = try Simulation.make(seed: 1)
        let id = sim.testing_spawnStandard(
            .autonomousInformant, at: playerPoint(sim), awareness: .unaware
        )
        sim.testing_setEnemyCombat(id, contactDps: 60)
        sim.testing_setPlayerIntegrity(1)
        #expect(!LethalWarning.isOn(sim.state))
    }

    @Test func safetyRationaleWarnsOnlyWhenTheScaledConeWouldExhaust() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_setCollisionSolids([])
        sim.testing_installBoss()
        let boss = try #require(sim.state.enemies.first { $0.archetype == .algorithmicModerate })
        sim.testing_setEnemyCombat(boss.id, contactDps: 0)
        let gap = boss.radius + PlayerBody.radiusUnits + 40
        sim.testing_setPlayerPosition(VecI(
            x: boss.position.x.unitsTruncated + gap,
            y: boss.position.y.unitsTruncated
        ))
        sim.testing_beginBossTelegraph(.safetyRationale, remaining: 10)
        sim.testing_setPlayerIntegrity(9)
        #expect(LethalWarning.isOn(sim.state))
        sim.testing_setPlayerIntegrity(10)
        #expect(!LethalWarning.isOn(sim.state))
    }

    @Test func theTelegraphSetsTheCardWithoutApplyingDamageOrAdvancingTheTutorial() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_setCollisionSolids([])
        sim.testing_installBoss()
        let boss = try #require(sim.state.enemies.first { $0.archetype == .algorithmicModerate })
        sim.testing_setEnemyCombat(boss.id, contactDps: 0)
        let gap = boss.radius + PlayerBody.radiusUnits + 40
        sim.testing_setPlayerPosition(VecI(
            x: boss.position.x.unitsTruncated + gap,
            y: boss.position.y.unitsTruncated
        ))
        sim.testing_beginBossTelegraph(.safetyRationale, remaining: 10)
        sim.testing_setPlayerIntegrity(9)
        let before = sim.state.player.integrity
        let phase = sim.state.tutorial.phase
        let result = sim.step(command: nil)
        #expect(sim.state.tutorial.lethalWarningPreempts)
        #expect(sim.state.tutorial.copy == LethalWarning.card)
        #expect(sim.state.tutorial.copyIsSafetyMessage)
        #expect(sim.state.tutorial.phase == phase)
        #expect(sim.state.player.integrity == before)
        #expect(!result.events.contains { $0.type == .playerDamaged })
    }

    @Test func narrowTailoringSumsTheBoltsThatContainThePlayer() throws {
        var sim = try openBoss(attack: .narrowTailoring)
        // Standing on the boss, every bolt's first sweep already overlaps.
        sim.testing_setPlayerIntegrity(13)
        #expect(LethalWarning.isOn(sim.state))
        sim.testing_setPlayerIntegrity(14)
        #expect(!LethalWarning.isOn(sim.state))
    }

    @Test func independentReviewSumsTheFiveFiredBolts() throws {
        var sim = try openBoss(attack: .independentReview)
        sim.testing_setPlayerIntegrity(20)
        #expect(LethalWarning.isOn(sim.state))
        sim.testing_setPlayerIntegrity(21)
        #expect(!LethalWarning.isOn(sim.state))
    }

    @Test func exposureTelegraphsStayQuiet() throws {
        var fog = try Simulation.make(seed: 1)
        let fogId = fog.testing_spawnStandard(.fogAnalyticsCloud, at: farPoint(fog))
        fog.testing_setEnemyCombat(fogId, ai: .telegraph, stateTicks: 20, contactDps: 0)
        fog.testing_setPlayerIntegrity(1)
        #expect(!LethalWarning.isOn(fog.state))

        var order = try Simulation.make(seed: 1)
        order.testing_setCollisionSolids([])
        order.testing_installBoss()
        let boss = try #require(order.state.enemies.first { $0.archetype == .algorithmicModerate })
        order.testing_setEnemyCombat(boss.id, contactDps: 0)
        order.testing_setPlayerPosition(VecI(
            x: boss.position.x.unitsTruncated + 400,
            y: boss.position.y.unitsTruncated
        ))
        order.testing_beginBossTelegraph(.temporaryOrder, remaining: 10)
        order.testing_setPlayerIntegrity(1)
        #expect(!LethalWarning.isOn(order.state))
    }

    @Test func aSolidConsumesTheWitchBoltAndAMineDoesNotWarn() throws {
        let origin = playerPoint(try Simulation.make(seed: 1))
        let witchAt = VecI(x: origin.x + 200, y: origin.y)
        var blocked = try Simulation.make(seed: 1)
        blocked.testing_setPlayerPosition(origin)
        blocked.testing_setCollisionSolids([
            AABB(center: VecI(x: origin.x + 100, y: origin.y), halfSize: VecI(x: 8, y: 40))
        ])
        let blockedId = blocked.testing_spawnStandard(.sutroSignalWitch, at: witchAt)
        blocked.testing_setEnemyCombat(blockedId, ai: .telegraph, stateTicks: 10, contactDps: 0)
        blocked.testing_setPlayerIntegrity(1)
        #expect(!LethalWarning.isOn(blocked.state))

        var open = try Simulation.make(seed: 1)
        open.testing_setCollisionSolids([])
        open.testing_setPlayerPosition(origin)
        let openId = open.testing_spawnStandard(.sutroSignalWitch, at: witchAt)
        open.testing_setEnemyCombat(openId, ai: .telegraph, stateTicks: 10, contactDps: 0)
        open.testing_setPlayerIntegrity(1)
        #expect(LethalWarning.isOn(open.state))

        var mined = try Simulation.make(seed: 1)
        mined.testing_insertMine(at: playerPoint(mined), armRemaining: 0, radius: 42)
        mined.testing_setPlayerIntegrity(1)
        #expect(!LethalWarning.isOn(mined.state))
    }

    @Test func theWitchTelegraphWarnsAndTheFireTickDoesNot() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_setCollisionSolids([])
        let id = sim.testing_spawnStandard(.sutroSignalWitch, at: playerPoint(sim))
        sim.testing_setEnemyCombat(id, ai: .telegraph, stateTicks: 10, contactDps: 0)
        sim.testing_setPlayerIntegrity(5)
        #expect(LethalWarning.isOn(sim.state))
        sim.testing_setPlayerIntegrity(6)
        #expect(!LethalWarning.isOn(sim.state))
        sim.testing_setEnemyCombat(id, stateTicks: 0)
        sim.testing_setPlayerIntegrity(1)
        #expect(!LethalWarning.isOn(sim.state))
    }

    @Test func theDaemonQueryWarnsOnlyWhileItsTelegraphHolds() throws {
        var sim = try Simulation.make(seed: 1)
        let far = farPoint(sim)
        let id = EntityID(900)
        sim.testing_insertEnemy(EnemyBody(
            id: id,
            archetype: .improperSearchDaemon,
            position: far.asQ8,
            velocity: .zero,
            integrity: 120,
            radius: 28,
            speedUnitsPerSecond: 70,
            contactDps: 0,
            state: .queryTelegraph,
            stateTicks: 10,
            spawnTick: 0,
            nextSpecialTick: 0,
            lockPosition: nil,
            encounterId: "elite",
            queryMarkers: [sim.state.player.position]
        ))
        sim.testing_setPlayerIntegrity(7)
        #expect(LethalWarning.isOn(sim.state))
        sim.testing_setPlayerIntegrity(8)
        #expect(!LethalWarning.isOn(sim.state))
        sim.testing_setEnemyCombat(id, ai: .dashTelegraph)
        sim.testing_setPlayerIntegrity(1)
        #expect(!LethalWarning.isOn(sim.state))
    }

    @Test func theCardOutranksLockdownAndHidesNothingAboutProgress() {
        var tutorial = TutorialState()
        tutorial.noteDisplacement(96)
        tutorial.lockdownPreempts = true
        tutorial.extractionPreempts = .armed
        tutorial.lethalWarningPreempts = true
        #expect(tutorial.copy == LethalWarning.card)
        #expect(tutorial.copyIsSafetyMessage)
        #expect(tutorial.phase == .field)
        tutorial.lethalWarningPreempts = false
        #expect(tutorial.copy == "LOCKDOWN")
    }

    @Test func flippingTheFlagLeavesTheGameplayDigestAlone() throws {
        var sim = try Simulation.make(seed: 1)
        let before = sim.state.digest()
        sim.testing_setLethalWarning(true)
        #expect(sim.state.digest() == before)
        #expect(sim.state.tutorial.lethalWarningPreempts)
    }

    @Test func theHapticFiresOnTheRisingEdgeAndRearmsAfterSixtyClearTicks() {
        var projector = AudioProjector()
        let world = quietWorld()
        let first = projector.project(tick: 1, events: [], world: world, lethalWarning: true)
        #expect(first.cues.contains(where: isLethalHaptic))
        let held = projector.project(tick: 2, events: [], world: world, lethalWarning: true)
        #expect(!held.cues.contains(where: isLethalHaptic))
        for tick in 3..<62 {
            _ = projector.project(tick: UInt64(tick), events: [], world: world, lethalWarning: false)
        }
        let early = projector.project(tick: 62, events: [], world: world, lethalWarning: true)
        #expect(!early.cues.contains(where: isLethalHaptic))
        for tick in 63..<123 {
            _ = projector.project(tick: UInt64(tick), events: [], world: world, lethalWarning: false)
        }
        let rearmed = projector.project(tick: 123, events: [], world: world, lethalWarning: true)
        let cue = rearmed.cues.first(where: isLethalHaptic)
        #expect(cue?.haptic == .warning)
        #expect(cue?.priority == 1)
        #expect(cue?.audioId.isEmpty == true)
        #expect(cue?.consumesEffectVoice == false)
        #expect(cue?.caption.isEmpty == true)
    }

    private func isLethalHaptic(_ cue: ProjectedCue) -> Bool {
        cue.audioId.isEmpty && cue.haptic == .warning
    }

    private func quietWorld() -> AudioWorldQuery {
        AudioWorldQuery(
            playerId: EntityID(1),
            playerPosition: .zero,
            outcome: .playing,
            extractionArmed: false,
            hasAlgorithmicModerate: false,
            lockdownEntered: false,
            detectionState: .hidden,
            viewport: ViewportSpec(
                baselineWorldWidth: 1920,
                baselineWorldHeight: 1080,
                deadZoneWidth: 64,
                deadZoneHeight: 64,
                maximumLookAheadUnits: 48
            )
        )
    }

    private func playerPoint(_ sim: Simulation) -> VecI {
        VecI(
            x: sim.state.player.position.x.unitsTruncated,
            y: sim.state.player.position.y.unitsTruncated
        )
    }

    private func farPoint(_ sim: Simulation) -> VecI {
        let point = playerPoint(sim)
        return VecI(x: point.x + 400, y: point.y)
    }

    /// Boss and Player on the same point, solids cleared, contact silenced.
    private func openBoss(attack: BossAttackID) throws -> Simulation {
        var sim = try Simulation.make(seed: 1)
        sim.testing_setCollisionSolids([])
        sim.testing_installBoss()
        let boss = try #require(sim.state.enemies.first { $0.archetype == .algorithmicModerate })
        sim.testing_setPlayerPosition(VecI(
            x: boss.position.x.unitsTruncated,
            y: boss.position.y.unitsTruncated
        ))
        sim.testing_setEnemyCombat(boss.id, contactDps: 0)
        sim.testing_beginBossTelegraph(attack, remaining: 10)
        return sim
    }
}
