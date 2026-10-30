import SpriteKit
import SurveillanceCore
import Testing
@testable import SSRuntime

#if DEBUG
/// `acceptance.md` F-007: results work with VoiceOver. The scene publishes the
/// drawn surface's spoken summary and control rects only while it shows.
@Suite(.serialized)
@MainActor
struct TerminalAccessibilityTests {
    @Test func theResultsSurfaceIsPublishedOnlyWhileItShows() throws {
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 844, height: 390))
        view.isPaused = true
        let scene = GameScene(size: view.bounds.size)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        scene.session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        try #require(scene.session.seedScenario("boss"))
        var frame: TimeInterval = 1
        func playToEnd() throws {
            for _ in 0..<120_000 where !scene.session.simulation.state.outcome.isTerminal {
                scene.update(frame); frame += 1.0 / 60
            }
            try #require(scene.session.simulation.state.outcome == .failure)
            scene.update(frame); frame += 1.0 / 60
        }
        #expect(scene.terminalAccessibility.surface == nil)

        try playToEnd()
        let run = try #require(scene.terminalAccessibility.surface)
        #expect(run.summary.hasPrefix("Player down. "))
        #expect(run.share != nil)
        #expect(run.rehearse != nil, "a Court death offers Rehearse Court")
        #expect(run.panel.contains(run.restart))

        #expect(scene.rehearseCourt())
        #expect(scene.terminalAccessibility.surface == nil)
        try playToEnd()
        let rehearsal = try #require(scene.terminalAccessibility.surface)
        #expect(rehearsal.summary.hasPrefix("Rehearsal down. Rehearsal "))
        #expect(rehearsal.share == nil, "run-shell.md § 14.3: a rehearsal cannot be shared")

        scene.restartRun()
        #expect(scene.terminalAccessibility.surface == nil)
    }
}
#endif
