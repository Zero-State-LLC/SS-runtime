import SpriteKit
import SurveillanceCore
import Testing
@testable import SSRuntime

#if DEBUG
/// `run-shell.md` § 14 (D-107), RS-033–RS-040. Debug only: the Court is reached
/// through the `boss` debug scenario rather than four minutes of play.
@Suite(.serialized)
@MainActor
struct CourtRehearsalTests {
    /// Steps a session with neutral input until the run is terminal.
    private func runToEnd(_ session: GameSession, cap: Int = 120_000) throws {
        for _ in 0..<cap where !session.simulation.state.outcome.isTerminal {
            if session.simulation.state.upgrade.pending { session.pendingUpgradeChoice = 0 }
            session.step()
        }
        try #require(session.simulation.state.outcome.isTerminal)
    }

    private func courtSession() throws -> GameSession {
        let session = GameSession(seed: 1)
        try #require(session.seedScenario("boss"))
        session.step()
        try #require(session.courtReached)
        return session
    }

    // RS-033 precondition and RS-035: the snapshot is the Court's first state.
    @Test func reachingTheCourtKeepsASnapshot() throws {
        let session = try courtSession()
        let snapshot = try #require(session.courtSnapshot)
        #expect(snapshot.seed == session.simulation.state.seed)
        #expect(snapshot.simulation.state.bossRuntime != nil)
        #expect(session.courtStartTick == snapshot.simulation.state.tick)
    }

    // RS-035, RS-039: a rehearsal resumes from the snapshot, and the same
    // commands from it give the same digest every time.
    @Test func rehearsalsFromTheSameSnapshotAreIdentical() throws {
        let session = try courtSession()
        let start = try #require(session.courtSnapshot).simulation.state.digest()
        try runToEnd(session)
        var digests: [String] = []
        for _ in 0..<2 {
            #expect(session.beginRehearsal())
            #expect(session.isRehearsal)
            #expect(session.simulation.state.digest() == start)
            #expect(session.commandLog == session.courtSnapshot?.commandLog)
            try runToEnd(session)
            digests.append(session.simulation.state.digest())
        }
        #expect(digests[0] == digests[1])
    }

    // RS-036: a rehearsal is never archived.
    @Test func aRehearsalIsNotArchived() throws {
        let session = try courtSession()
        try runToEnd(session)
        #expect(session.beginRehearsal())
        #expect(session.terminalReceiptStored, "the receipt guard skips a rehearsal")
    }

    // RS-038, RS-040: Restart is a real run on the same seed and keeps the
    // snapshot until a later run replaces it; another seed discards it.
    @Test func restartKeepsTheSnapshotForItsSeedOnly() throws {
        let session = try courtSession()
        let seed = session.simulation.state.seed
        session.restartRun(seed: seed)
        #expect(!session.isRehearsal)
        #expect(!session.courtReached)
        #expect(session.simulation.state.tick == 0)
        #expect(session.courtSnapshot != nil)
        session.restartRun(seed: seed &+ 1)
        #expect(session.courtSnapshot == nil)
        #expect(!session.beginRehearsal())
    }

    // RS-033, RS-034, RS-036, RS-037 through the scene: the control is offered
    // only after a Court failure, the rehearsal card has no medals or Share,
    // and a failed rehearsal offers it again.
    @Test func theSceneOffersRehearsalOnlyAfterACourtDeath() throws {
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
        try playToEnd()
        #expect(scene.rehearsalOffered)
        #expect(scene.rehearseCourt())
        #expect(!scene.rehearsalOffered)
        #expect(scene.session.isRehearsal)
        #expect(scene.intro == nil)
        try playToEnd()
        #expect(scene.rehearsalOffered, "RS-037: offered again after a failed rehearsal")
        #expect(scene.currentRunCard?.isRehearsal == true)
        #expect(scene.currentRunCard?.medals.isEmpty == true)
        scene.restartRun()
        #expect(!scene.session.isRehearsal)
        #expect(scene.currentTick == 0)
    }
}
#endif
