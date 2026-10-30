import SwiftUI
import SurveillanceCore
import UIKit

/// `acceptance.md` F-007 and `visual-assets.md`: the results surface works with
/// VoiceOver. SpriteKit draws the panel; this is what SwiftUI needs to expose
/// it. Rects are in the HUD's safe-rectangle point space, which is the
/// coordinate space of a SwiftUI view laid out inside the safe area.
struct TerminalAccessibilitySurface: Equatable {
    /// The drawn copy, for the reflowed card at accessibility text sizes.
    var title: String
    var rows: [RunCard.Row]
    var summary: String
    var spokenRows: String
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
///
/// `visual-assets.md`: results support Dynamic Type up to 200% through reflow
/// or scrolling. The drawn panel has a fixed size, so at accessibility text
/// sizes a scrolling SwiftUI card in the upgrade overlay's style replaces it.
struct TerminalAccessibilityOverlay: View {
    @ObservedObject var model: TerminalAccessibilityModel
    var onRestart: () -> Void
    var onShare: () -> Void
    var onRehearse: () -> Void
    @Environment(\.dynamicTypeSize) private var typeSize

    var body: some View {
        if let surface = model.surface {
            if typeSize.isAccessibilitySize {
                reflowed(surface)
            } else {
                overDrawnPanel(surface)
            }
        }
    }

    private func reflowed(_ surface: TerminalAccessibilitySurface) -> some View {
        ZStack {
            Color(red: 0.035, green: 0.05, blue: 0.07).ignoresSafeArea()
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    Text(surface.title).font(.title2.bold())
                        .accessibilityLabel(TerminalSpeech.sentence(surface.title))
                        .accessibilityAddTraits(.isHeader)
                    VStack(alignment: .leading, spacing: 14) {
                        ForEach(Array(surface.rows.enumerated()), id: \.offset) { _, row in
                            VStack(alignment: .leading, spacing: 4) {
                                Text(row.label).font(.subheadline.bold()).opacity(0.75)
                                Text(row.value).font(.body.monospacedDigit())
                            }
                            .fixedSize(horizontal: false, vertical: true)
                        }
                    }
                    // VoiceOver reads the rows as sentences, as on the drawn panel.
                    .accessibilityElement(children: .ignore)
                    .accessibilityLabel(surface.spokenRows)
                    VStack(alignment: .leading, spacing: 12) {
                        reflowedButton("RESTART", TerminalSpeech.restart, action: onRestart)
                        if surface.share != nil {
                            reflowedButton("SHARE", TerminalSpeech.share, action: onShare)
                        }
                        if surface.rehearse != nil {
                            reflowedButton(HUDLayout.rehearseControlCopy, TerminalSpeech.rehearse, action: onRehearse)
                        }
                    }
                }
                .padding(24)
                .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
        .foregroundStyle(.white)
    }

    private func reflowedButton(_ copy: String, _ label: String, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Text(copy).font(.headline)
                .fixedSize(horizontal: false, vertical: true)
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(16)
                .background(Color.white.opacity(0.07), in: RoundedRectangle(cornerRadius: 12))
                .overlay(RoundedRectangle(cornerRadius: 12).stroke(Color.white.opacity(0.5)))
                .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
        .accessibilityLabel(label)
    }

    private func overDrawnPanel(_ surface: TerminalAccessibilitySurface) -> some View {
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
