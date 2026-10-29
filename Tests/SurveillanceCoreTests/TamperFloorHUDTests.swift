import Testing
@testable import SurveillanceCore

/// D-110, hud-tutorial.md § Exposure presentation (UI-012–UI-014): where the
/// Tamper floor marker sits on the Exposure bar.
@Suite struct TamperFloorHUDTests {
    @Test func noMarkerBeforeAnyCameraIsDestroyed() {
        #expect(HUDLayout.tamperFloor(camerasDestroyed: 0) == nil)
    }

    @Test func markerFollowsTheRule() {
        #expect(HUDLayout.tamperFloor(camerasDestroyed: 1) == 150)
        #expect(HUDLayout.tamperFloor(camerasDestroyed: 3) == 450)
        #expect(HUDLayout.tamperFloor(camerasDestroyed: 6) == 900)
    }

    @Test func markerStopsAtTheEndOfTheBar() {
        #expect(HUDLayout.tamperFloor(camerasDestroyed: 7) == 1000)
        #expect(HUDLayout.tamperFloor(camerasDestroyed: 8) == 1000)
    }

    /// The marker and the recovery floor are the same number.
    @Test func markerMatchesTheExposureFloor() {
        for destroyed in 1...8 {
            #expect(HUDLayout.tamperFloor(camerasDestroyed: destroyed)
                == min(1000, ExposureState.tamperFloorPerCamera * destroyed))
        }
    }
}
