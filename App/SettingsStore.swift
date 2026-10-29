import SurveillanceCore
import SwiftUI
import UIKit

/// Local persistence for `PresentationSettings`.
///
/// `plan.md` lists persistence as "settings-and-local-run-receipts", and
/// `audio-haptics-001` says settings are "local, independent, and excluded from
/// replay authority". So this never touches the simulation and never travels
/// with a replay — it is a per-device preference file and nothing more.
@MainActor
final class SettingsStore: ObservableObject {
    private static let key = "com.zer0state.surveillancesurvivor.presentationSettings"
    /// `run-shell.md` § 13.3 (D-106): set once the player changes Reduced
    /// Motion in Settings. Until then it follows iOS Reduce Motion.
    static let reducedMotionChosenKey = "com.zer0state.surveillancesurvivor.reducedMotionChosen"

    @Published var settings: PresentationSettings {
        didSet {
            if !resetting, oldValue.vfx.reducedMotion != settings.vfx.reducedMotion {
                defaults.set(true, forKey: Self.reducedMotionChosenKey)
            }
            persist()
        }
    }

    private let defaults: UserDefaults
    /// iOS Reduce Motion, read once at launch (§ 13.3).
    private let systemReduceMotion: Bool
    private var resetting = false

    init(defaults: UserDefaults = .standard,
         systemReduceMotion: Bool = UIAccessibility.isReduceMotionEnabled) {
        self.defaults = defaults
        self.systemReduceMotion = systemReduceMotion
        // A stored file is untrusted input: a decode failure falls back to the
        // contract defaults rather than refusing to start.
        var loaded = PresentationSettings.defaults
        if let data = defaults.data(forKey: Self.key),
           let decoded = try? JSONDecoder().decode(PresentationSettings.self, from: data)
        {
            loaded = decoded
        }
        if !defaults.bool(forKey: Self.reducedMotionChosenKey) {
            loaded.vfx.reducedMotion = systemReduceMotion
        }
        settings = loaded
    }

    private func persist() {
        guard let data = try? JSONEncoder().encode(settings) else { return }
        defaults.set(data, forKey: Self.key)
    }

    /// Back to the contract defaults, with Reduced Motion following iOS again.
    func resetToDefaults() {
        defaults.removeObject(forKey: Self.reducedMotionChosenKey)
        var reset = PresentationSettings.defaults
        reset.vfx.reducedMotion = systemReduceMotion
        resetting = true
        settings = reset
        resetting = false
    }
}
