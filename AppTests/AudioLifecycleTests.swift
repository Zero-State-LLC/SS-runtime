import Testing
@testable import SSRuntime
import SurveillanceCore

@Suite(.serialized)
@MainActor
struct AudioLifecycleTests {
    @Test func rapidResumeCannotReviveCancelledOneShots() async throws {
        let engine = AudioEngine()
        engine.playAfterDuck(.presentation(audioId: "audit_pause_stale"), delayMs: 30)
        engine.setSuspended(true)
        engine.setSuspended(false)
        engine.playAfterDuck(.presentation(audioId: "audit_interrupt_stale"), delayMs: 30)
        engine.handleInterruption(.began)
        engine.handleInterruption(.ended)
        try await Task.sleep(for: .milliseconds(150))
        #expect(engine.missingCueIds.isEmpty)
    }

    @Test func pauseAndInterruptionComposeAndDiscardDeferredCue() async throws {
        let engine = AudioEngine()
        engine.playAfterDuck(.presentation(audioId: "audit_missing_delayed"), delayMs: 30)
        engine.setSuspended(true)
        engine.handleInterruption(.began)
        engine.handleInterruption(.ended)
        engine.playPresentationCue(.presentation(audioId: "audit_missing_paused"))
        try await Task.sleep(for: .milliseconds(150))
        #expect(engine.missingCueIds.isEmpty)
        engine.setSuspended(false)
        engine.playPresentationCue(.presentation(audioId: "audit_missing_resumed"))
        #expect(engine.missingCueIds == ["audit_missing_resumed"])
    }

    @Test func resumingSceneCannotOverrideActiveInterruption() {
        let engine = AudioEngine()
        engine.handleInterruption(.began)
        engine.setSuspended(true)
        engine.setSuspended(false)
        engine.playPresentationCue(.presentation(audioId: "audit_still_interrupted"))
        #expect(engine.interrupted)
        #expect(engine.missingCueIds.isEmpty)
        engine.handleInterruption(.ended)
        engine.playPresentationCue(.presentation(audioId: "audit_interruption_ended"))
        #expect(!engine.interrupted)
        #expect(engine.missingCueIds == ["audit_interruption_ended"])
        engine.reset()
    }

    @Test func resetCancelsDeferredCue() async throws {
        let engine = AudioEngine()
        engine.playAfterDuck(.presentation(audioId: "audit_missing_reset"), delayMs: 30)
        engine.reset()
        try await Task.sleep(for: .milliseconds(150))
        #expect(engine.missingCueIds.isEmpty)
    }

    @Test func suspensionClearsBlackoutImmediatelyAndDoesNotRearmIt() async throws {
        let engine = AudioEngine()
        engine.beginBlackoutDrop()
        #expect(engine.musicDropped)
        engine.setSuspended(true)
        #expect(!engine.musicDropped)
        engine.setSuspended(false)
        try await Task.sleep(for: .milliseconds(150))
        #expect(!engine.musicDropped)
    }
}
