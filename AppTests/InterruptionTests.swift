import AVFoundation
import SpriteKit
import SurveillanceCore
import Testing
@testable import SSRuntime

/// `run-shell.md` § 13 (D-106), RS-025–RS-032. The scene-phase hook itself is
/// one line in `GameContainerView`; these cover what it decides and does.
@Suite(.serialized)
@MainActor
struct InterruptionTests {
    private func makeScene() -> (GameScene, SKView) {
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 844, height: 390))
        view.isPaused = true // Only the explicitly driven frames advance.
        let scene = GameScene(size: view.bounds.size)
        view.presentScene(scene)
        scene.session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        return (scene, view)
    }

    /// The container's handler, without SwiftUI: pause when the scene says so.
    private func leaveForeground(_ scene: GameScene) -> Bool {
        guard scene.pausesOnInterruption else { return false }
        scene.setPaused(true)
        return true
    }

    // RS-025, RS-026: a ticking run pauses, adds no tick, and stays paused.
    @Test func aTickingRunPausesAndStaysPaused() {
        let (scene, view) = makeScene()
        defer { view.presentScene(nil) }
        scene.update(1)
        let tick = scene.currentTick
        #expect(leaveForeground(scene))
        for frame in 2...11 { scene.update(TimeInterval(frame)) }
        #expect(scene.currentTick == tick, "no tick while interrupted, or after return until resumed")
        #expect(!scene.pausesOnInterruption)
        scene.setPaused(false)
        scene.update(12)
        #expect(scene.currentTick == tick + 1)
    }

    // RS-027: already paused, nothing changes.
    @Test func alreadyPausedIsUnchanged() {
        let (scene, view) = makeScene()
        defer { view.presentScene(nil) }
        scene.setPaused(true)
        #expect(!leaveForeground(scene))
    }

    // RS-028: the intro advances no tick, so it is left to continue.
    @Test func theIntroIsLeftAlone() throws {
        let (scene, view) = makeScene()
        defer { view.presentScene(nil) }
        scene.beginDailyRun(try DailyRun(day: DailyRun.Day(utc: Date(timeIntervalSince1970: 1_790_000_000))))
        #expect(scene.intro != nil)
        #expect(!scene.pausesOnInterruption)
    }

    // RS-029: interrupt-and-resume is invisible to the authoritative run.
    @Test func anInterruptionDoesNotChangeTheRun() {
        let (plain, plainView) = makeScene()
        let (interrupted, interruptedView) = makeScene()
        defer { plainView.presentScene(nil); interruptedView.presentScene(nil) }
        var frame: TimeInterval = 1
        for _ in 0..<60 { plain.update(frame); interrupted.update(frame); frame += 1 }
        #expect(leaveForeground(interrupted))
        for _ in 0..<30 { interrupted.update(frame); frame += 1 }
        interrupted.setPaused(false)
        for _ in 0..<60 { plain.update(frame); interrupted.update(frame); frame += 1 }
        #expect(plain.currentTick == interrupted.currentTick)
        #expect(plain.session.simulation.state.digest() == interrupted.session.simulation.state.digest())
    }

    // RS-030: an audio interruption silences until it ends.
    @Test func audioInterruptionSilencesUntilItEnds() {
        let engine = AudioEngine()
        engine.handleInterruption(.began)
        #expect(engine.interrupted)
        engine.handleInterruption(.ended)
        #expect(!engine.interrupted)
    }

    // RS-031, RS-032: Reduced Motion follows iOS until the player sets it.
    @Test func reducedMotionFollowsTheSystemUntilChosen() throws {
        let suite = "InterruptionTests.reducedMotion"
        let defaults = try #require(UserDefaults(suiteName: suite))
        defer { defaults.removePersistentDomain(forName: suite) }

        #expect(SettingsStore(defaults: defaults, systemReduceMotion: true).settings.vfx.reducedMotion)
        #expect(!SettingsStore(defaults: defaults, systemReduceMotion: false).settings.vfx.reducedMotion)

        // Another setting changing does not freeze Reduced Motion.
        let store = SettingsStore(defaults: defaults, systemReduceMotion: false)
        store.settings.captions = .all
        #expect(SettingsStore(defaults: defaults, systemReduceMotion: true).settings.vfx.reducedMotion)

        // The player's own choice wins over a later system change.
        let chooser = SettingsStore(defaults: defaults, systemReduceMotion: true)
        chooser.settings.vfx.reducedMotion = false
        #expect(!SettingsStore(defaults: defaults, systemReduceMotion: true).settings.vfx.reducedMotion)

        // Reset returns to following the system.
        chooser.resetToDefaults()
        #expect(SettingsStore(defaults: defaults, systemReduceMotion: true).settings.vfx.reducedMotion)
    }
}
