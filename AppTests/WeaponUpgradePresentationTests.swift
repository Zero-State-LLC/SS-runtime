import SpriteKit
import SwiftUI
import Testing
@testable import SSRuntime
@testable import SurveillanceCore

@Suite(.serialized) @MainActor
struct WeaponUpgradePresentationTests {
    @Test func dischargeRequiresMatchingEventAndExpiresWithoutNodeGrowth() throws {
        var snap = PresentationSnapshot(try Simulation.make(seed: 1).state)
        snap.tick = 1
        let id = EntityID(999)
        snap.combatFeedback.shot = .init(projectile: id, origin: .init(unitsX: 40, unitsY: 50), velocity: .init(unitsX: -12, unitsY: 0))
        let renderer = CombatFeedbackRenderer()
        renderer.update(snap, events: [], settings: .standard)
        #expect(renderer.discharge.isHidden)
        snap.tick = 2
        let event = AuthoritativeEvent(tick: 2, phase: 7, type: .weaponFired, primary: id, payload: [:], insertion: 0)
        renderer.update(snap, events: [event], settings: .standard)
        #expect(!renderer.discharge.isHidden)
        #expect(renderer.discharge.position == CGPoint(x: 40, y: 50))
        #expect(abs(abs(renderer.aim.zRotation) - .pi) < 0.001)
        // Facing is deliberately east; aim is west.
        #expect(snap.playerDirection == "e")
        for tick in 3...1000 {
            snap.tick = UInt64(tick)
            snap.combatFeedback = .init()
            renderer.update(snap, events: [], settings: .standard)
            #expect(renderer.root.children.count == 4)
        }
        #expect(renderer.discharge.isHidden)
        renderer.reset()
        let allHidden = renderer.root.children.allSatisfy { $0.isHidden }
        #expect(allHidden)
    }

    @Test func upgradeContoursAreDistinctStaticUnderReductionAndClearOnRestart() throws {
        var snap = PresentationSnapshot(try Simulation.make(seed: 1).state)
        snap.tick = 20
        snap.combatFeedback.jammerReducedExposure = true
        snap.ghostConcealmentActive = true
        let renderer = CombatFeedbackRenderer()
        var reduced = PresentationVFXSettings.standard
        reduced.reducedMotion = true
        renderer.update(snap, events: [], settings: reduced)
        #expect(!renderer.jammer.isHidden && !renderer.concealment.isHidden)
        #expect(renderer.jammer.zRotation == 0)
        #expect(!renderer.jammer.hasActions() && !renderer.concealment.hasActions())
        #expect(renderer.jammer.path?.boundingBox != renderer.concealment.path?.boundingBox)
        snap.tick += 1
        snap.combatFeedback = .init()
        snap.ghostConcealmentActive = false
        renderer.update(snap, events: [], settings: reduced)
        #expect(renderer.jammer.isHidden && renderer.concealment.isHidden)
        renderer.reset()
        let allHidden = renderer.root.children.allSatisfy { $0.isHidden }
        #expect(allHidden)
    }

    @Test(arguments: [UInt8(0), 1, 2])
    func nativeChoiceBoundaryFreezesUntilChoiceAndClearsHeldInput(index: UInt8) throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_primeEncounterForCompletion("M-A")
        let session = GameSession(simulation: sim)
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 844, height: 390))
        view.isPaused = true
        let scene = GameScene(size: view.bounds.size, session: session)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        let finger = NSObject()
        let token = TouchController.TouchToken(id: ObjectIdentifier(finger))
        let layout = try #require(scene.controlLayout)
        scene.beginTouch(token: token, atPoints: CGPoint(x: layout.stickCentre.x + layout.stickRadius, y: layout.stickCentre.y))
        scene.update(1)
        #expect(scene.upgradeSelection.isPresented)
        let tick = scene.currentTick
        scene.update(2)
        #expect(scene.currentTick == tick)
        #expect(!scene.chooseUpgrade(3))
        #expect(scene.chooseUpgrade(index))
        #expect(!scene.chooseUpgrade((index + 1) % 3))
        scene.update(3)
        #expect(scene.currentTick == tick + 1)
        #expect(session.simulation.state.upgrade.selected == UpgradeID.from(index: index))
        #expect(session.commandLog.last?.moveX == 0)
        #expect(session.commandLog.last?.dodgePressed == false)
        #expect(!scene.upgradeSelection.isPresented)
        scene.update(4)
        #expect(session.commandLog.last?.moveX == 0)
        scene.restartRun()
        #expect(!scene.upgradeSelection.isPresented && !scene.upgradeSelection.submitted)
    }

    @Test func accessibilityTextUsesScrollingSingleColumnAndNativeSurfaceHosts() {
        #expect(UpgradeSelectionView.columnCount(width: 844, accessibility: false) == 3)
        #expect(UpgradeSelectionView.columnCount(width: 844, accessibility: true) == 1)
        #expect(UpgradeSelectionView.columnCount(width: 667, accessibility: false) == 1)
        let model = UpgradeSelectionModel()
        model.synchronize(pending: true)
        let host = UIHostingController(rootView: UpgradeSelectionView(model: model, onChoose: { _ in })
            .environment(\.dynamicTypeSize, .accessibility3))
        host.loadViewIfNeeded()
        host.view.frame = CGRect(x: 0, y: 0, width: 667, height: 375)
        host.view.layoutIfNeeded()
        #expect(host.view.bounds.width == 667)
        #expect(!model.submitted) // Layout/focus must not implicitly choose.
    }
}
