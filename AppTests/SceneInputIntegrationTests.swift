import SpriteKit
import Testing
@testable import SSRuntime

/// PC-009 / T301. These run in both CI configurations and enter at the same
/// point-space boundary as UITouch, then execute the real GameScene.update.
@Suite(.serialized)
@MainActor
struct SceneInputIntegrationTests {
    final class Finger {}
    private func token(_ finger: Finger) -> TouchController.TouchToken {
        .init(id: ObjectIdentifier(finger))
    }

    private func makeScene() -> (GameScene, SKView) {
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 844, height: 390))
        view.isPaused = true // Only the explicitly driven frames advance.
        let scene = GameScene(size: view.bounds.size)
        view.presentScene(scene)
        scene.session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        return (scene, view)
    }

    @Test func touchMovementAndDodgeReachTheSimulation() throws {
        let (scene, view) = makeScene()
        defer { view.presentScene(nil) }
        let layout = try #require(scene.controlLayout)
        let stick = Finger(), dodge = Finger()
        let start = scene.session.simulation.state.player.position
        scene.beginTouch(token: token(stick), atPoints: layout.stickCentre)
        scene.moveTouch(token: token(stick), toPoints: CGPoint(x: layout.stickCentre.x + layout.stickRadius, y: layout.stickCentre.y))
        scene.update(1)
        #expect(scene.session.commandLog.last?.moveX == Int16(TouchController.maximum))
        #expect(scene.session.simulation.state.player.position != start)
        scene.beginTouch(token: token(dodge), atPoints: CGPoint(x: layout.dodgeRect.midX, y: layout.dodgeRect.midY))
        scene.update(2)
        #expect(scene.session.commandLog.last?.dodgePressed == true)
        scene.update(3)
        #expect(scene.session.commandLog.last?.dodgePressed == false)
        scene.endTouch(token: token(stick))
        scene.endTouch(token: token(dodge))
        scene.update(4)
        #expect(scene.session.commandLog.last?.moveX == 0)
    }

    @Test func pauseResumeClearsHeldMovementAndBufferedDodge() throws {
        let (scene, view) = makeScene()
        defer { view.presentScene(nil) }
        let layout = try #require(scene.controlLayout)
        let stick = Finger(), dodge = Finger(), replacement = Finger()
        let edge = CGPoint(x: layout.stickCentre.x + layout.stickRadius, y: layout.stickCentre.y)
        scene.beginTouch(token: token(stick), atPoints: edge)
        scene.update(1)
        #expect(scene.session.commandLog.last?.moveX != 0)
        scene.beginTouch(token: token(dodge), atPoints: CGPoint(x: layout.dodgeRect.midX, y: layout.dodgeRect.midY))
        let tick = scene.currentTick
        scene.setPaused(true)
        scene.update(2)
        #expect(scene.currentTick == tick)
        scene.setPaused(false)
        scene.update(3)
        #expect(scene.currentTick == tick + 1)
        #expect(scene.session.commandLog.last?.moveX == 0)
        #expect(scene.session.commandLog.last?.dodgePressed == false)
        scene.beginTouch(token: token(replacement), atPoints: edge)
        scene.update(4)
        #expect(scene.session.commandLog.last?.moveX == Int16(TouchController.maximum))
    }

    @Test func restartRestoresInitialStateAndClearsInput() throws {
        let (scene, view) = makeScene()
        defer { view.presentScene(nil) }
        let layout = try #require(scene.controlLayout)
        let stick = Finger(), dodge = Finger()
        let initial = scene.session.simulation.state.digest()
        scene.beginTouch(token: token(stick), atPoints: CGPoint(x: layout.stickCentre.x + layout.stickRadius, y: layout.stickCentre.y))
        scene.update(1)
        scene.beginTouch(token: token(dodge), atPoints: CGPoint(x: layout.dodgeRect.midX, y: layout.dodgeRect.midY))
        scene.restartRun()
        #expect(scene.currentTick == 0)
        #expect(scene.session.simulation.state.digest() == initial)
        scene.update(2)
        #expect(scene.session.commandLog.last?.moveX == 0)
        #expect(scene.session.commandLog.last?.dodgePressed == false)
    }
}
