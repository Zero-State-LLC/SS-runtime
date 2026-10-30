import Testing
@testable import SurveillanceCore

/// `hud-tutorial.md` sentence case for VoiceOver, `acceptance.md` F-013.
@Suite struct SpokenHUDTests {
    private func caption(_ text: String, _ captionClass: CaptionClass, sequence: Int) -> CaptionBoard.Entry {
        .init(text: text, cueId: "cue", captionClass: captionClass, priority: 1, tick: 0, sequence: sequence)
    }

    @Test func f013TheFirstCameraCopyIsSpokenInSentenceCase() {
        var spoken = SpokenHUD()
        #expect(spoken.announcements(tutorial: HUDLayout.firstEncounterCameraCopy, reinforcement: nil, captions: [])
            == ["Move toward a camera to shoot it. Destruction adds exposure."])
    }

    @Test func eachCopyIsAnnouncedOnceWhileItShows() {
        var spoken = SpokenHUD()
        let copy = HeatCaptionProjector.copy(count: 2, state: .hunted)
        #expect(spoken.announcements(tutorial: nil, reinforcement: copy, captions: []) == ["Reinforcements +2. Hunted."])
        #expect(spoken.announcements(tutorial: nil, reinforcement: copy, captions: []).isEmpty)
        #expect(spoken.announcements(tutorial: nil, reinforcement: nil, captions: []).isEmpty)
        #expect(spoken.announcements(tutorial: nil, reinforcement: copy, captions: []).count == 1, "a new wave is announced again")
    }

    @Test func onlySafetyCaptionsAreAnnouncedAndOnlyWhenNew() {
        var spoken = SpokenHUD()
        let shot = caption("Civic Pulse", .routine, sequence: 1)
        let cone = caption("Cone sweep: crowd control", .safety, sequence: 2)
        #expect(spoken.announcements(tutorial: nil, reinforcement: nil, captions: [shot, cone]) == ["Cone sweep: crowd control"])
        #expect(spoken.announcements(tutorial: nil, reinforcement: nil, captions: [shot, cone]).isEmpty)
        let again = caption("Cone sweep: crowd control", .safety, sequence: 3)
        #expect(spoken.announcements(tutorial: nil, reinforcement: nil, captions: [again]) == ["Cone sweep: crowd control"],
                "a repeated warning is a new warning")
    }

    @Test func theOrderIsTutorialThenReinforcementsThenCaptions() {
        var spoken = SpokenHUD()
        let lines = spoken.announcements(
            tutorial: "PATROL • STAY OUT OF THE CONES • WALK PAST OR STRIKE",
            reinforcement: HeatCaptionProjector.copy(count: 1, state: .tracked),
            captions: [caption("Player damaged", .safety, sequence: 1)]
        )
        #expect(lines == ["Patrol. Stay out of the cones. Walk past or strike.", "Reinforcements +1. Tracked.", "Player damaged"])
    }
}
