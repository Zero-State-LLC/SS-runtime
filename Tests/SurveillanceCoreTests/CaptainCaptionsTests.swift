import Testing
@testable import SurveillanceCore

/// D-111, audio-haptics.md § Captain and Daemon captions (AH-007, AH-008).
@Suite(.serialized)
struct CaptainCaptionsTests {
    @Test func ah008EveryCaptionFitsTheColumn() {
        #expect(CaptainCaptions.all.count == 11)
        for caption in CaptainCaptions.all {
            #expect(caption.count <= CaptainCaptions.maxLength, "\(caption)")
        }
    }

    @Test func ah007TelegraphsLeadWithTheirForm() {
        #expect(CaptainCaptions.telegraph(.safetyRationale).hasPrefix("Cone:"))
        #expect(CaptainCaptions.telegraph(.narrowTailoring).hasPrefix("3 bolts:"))
        #expect(CaptainCaptions.telegraph(.temporaryOrder).hasPrefix("Field:"))
        #expect(CaptainCaptions.telegraph(.independentReview).hasPrefix("Ring, 1 gap:"))
        #expect(CaptainCaptions.daemonQuery.hasPrefix("Query:"))
        #expect(CaptainCaptions.daemonDash.hasPrefix("Dash:"))
    }

    private func project(_ type: EventType, payload: [String: CanonicalJSON]) throws -> [ProjectedCue] {
        var projector = AudioProjector()
        let sim = try Simulation.make(seed: 1)
        let event = AuthoritativeEvent(tick: 5, phase: 16, type: type, primary: EntityID(9), payload: payload, insertion: 0)
        return projector.project(tick: 5, events: [event], world: AudioWorldQuery.from(sim.state)).cues
    }

    @Test(arguments: [BossAttackID.safetyRationale, .narrowTailoring, .temporaryOrder, .independentReview])
    func theProjectorCaptionsEachCaptainAttack(attack: BossAttackID) throws {
        let cues = try project(.bossAttackStarted, payload: ["attackId": .string(attack.rawValue), "phaseId": .string("publicSafety")])
        let cue = try #require(cues.first { $0.audioId == "boss_telegraph_\(attack.rawValue)" })
        #expect(cue.caption == CaptainCaptions.telegraph(attack))
    }

    @Test(arguments: [BossPhase.civilLiberties, .temporarySafeguard, .independentReview])
    func theProjectorCaptionsEachPhaseChange(phase: BossPhase) throws {
        let cues = try project(.bossPhaseChanged, payload: ["before": .string("publicSafety"), "after": .string(phase.rawValue)])
        let cue = try #require(cues.first { $0.audioId == "boss_phase_\(phase.rawValue)" })
        #expect(cue.caption == CaptainCaptions.phase(phase))
    }

    @Test func theProjectorCaptionsTheDefeat() throws {
        let cues = try project(.bossDefeated, payload: [:])
        #expect(cues.first { $0.audioId == "boss_defeated" }?.caption == CaptainCaptions.defeated)
    }
}
