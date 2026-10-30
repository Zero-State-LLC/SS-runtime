import SwiftUI
import SurveillanceCore
import UIKit

/// `acceptance.md` F-007 and `visual-assets.md`: the results surface works with
/// VoiceOver. SpriteKit draws the panel; this is what SwiftUI needs to expose
/// it. Rects are in the HUD's safe-rectangle point space, which is the
/// coordinate space of a SwiftUI view laid out inside the safe area.
struct TerminalAccessibilitySurface: Equatable {
    var summary: String
    var panel: CGRect
    var restart: CGRect
    var share: CGRect?
    var rehearse: CGRect?
}

/// The scene publishes transitions only, not a SwiftUI update every frame.
@MainActor
final class TerminalAccessibilityModel: ObservableObject {
    @Published private(set) var surface: TerminalAccessibilitySurface?

    func synchronize(_ surface: TerminalAccessibilitySurface?) {
        guard surface != self.surface else { return }
        let appeared = self.surface == nil && surface != nil
        self.surface = surface
        // Move VoiceOver to the results, as a new screen would.
        if appeared { UIAccessibility.post(notification: .screenChanged, argument: nil) }
    }
}

/// Native buttons over the drawn controls: the same action for touch,
/// VoiceOver and Switch Control, and nothing drawn, so the Civic Seam panel is
/// unchanged. The summary element reads the outcome and every card row.
struct TerminalAccessibilityOverlay: View {
    @ObservedObject var model: TerminalAccessibilityModel
    var onRestart: () -> Void
    var onShare: () -> Void
    var onRehearse: () -> Void

    var body: some View {
        if let surface = model.surface {
            ZStack(alignment: .topLeading) {
                Color.clear
                    .frame(width: surface.panel.width, height: surface.panel.height)
                    .position(x: surface.panel.midX, y: surface.panel.midY)
                    .allowsHitTesting(false)
                    .accessibilityElement()
                    .accessibilityLabel(surface.summary)
                    .accessibilityAddTraits(.isHeader)
                    .accessibilitySortPriority(4)
                control(surface.restart, TerminalSpeech.restart, priority: 3, action: onRestart)
                if let share = surface.share {
                    control(share, TerminalSpeech.share, priority: 2, action: onShare)
                }
                if let rehearse = surface.rehearse {
                    control(rehearse, TerminalSpeech.rehearse, priority: 1, action: onRehearse)
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
            .accessibilityElement(children: .contain)
        }
    }

    private func control(_ rect: CGRect, _ label: String, priority: Double, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Color.clear.contentShape(Rectangle())
        }
        .buttonStyle(.plain)
        .frame(width: rect.width, height: rect.height)
        .position(x: rect.midX, y: rect.midY)
        .accessibilityLabel(label)
        .accessibilitySortPriority(priority)
    }
}
