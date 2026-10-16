import SwiftUI
import SurveillanceCore

/// The scene publishes transitions only, not a SwiftUI update every game tick.
@MainActor
final class UpgradeSelectionModel: ObservableObject {
    @Published private(set) var isPresented = false
    @Published private(set) var submitted = false

    func synchronize(pending: Bool) {
        guard pending != isPresented else { return }
        isPresented = pending
        submitted = false
    }
    func submit(_ index: UInt8) -> Bool {
        guard isPresented, !submitted, UpgradeID.from(index: index) != nil else { return false }
        submitted = true
        return true
    }
}

/// T1035: native buttons provide the same action for touch, VoiceOver and
/// Switch Control. Equal columns collapse to an ordered scrolling list at
/// accessibility text sizes; no text is truncated or given a fixed height.
struct UpgradeSelectionView: View {
    @ObservedObject var model: UpgradeSelectionModel
    var onChoose: (UInt8) -> Void
    @Environment(\.dynamicTypeSize) private var typeSize

    static func columnCount(width: CGFloat, accessibility: Bool) -> Int {
        accessibility || width < 760 ? 1 : 3
    }
    var body: some View {
        if model.isPresented {
            GeometryReader { geometry in
                ZStack {
                    Color(red: 0.035, green: 0.05, blue: 0.07).ignoresSafeArea()
                    ScrollView {
                        VStack(alignment: .leading, spacing: 20) {
                            Text("Choose one upgrade").font(.title2.bold())
                                .accessibilityAddTraits(.isHeader)
                            Text("The run is paused while you choose.").font(.body)
                            LazyVGrid(columns: Array(repeating: GridItem(.flexible(), alignment: .top),
                                count: Self.columnCount(width: geometry.size.width, accessibility: typeSize.isAccessibilitySize)),
                                alignment: .leading, spacing: 16) {
                                ForEach(UpgradePresentation.selectionCards(), id: \.selectionIndex) { card in
                                    Button { onChoose(card.selectionIndex) } label: {
                                        VStack(alignment: .leading, spacing: 12) {
                                            Label(card.name, systemImage: card.symbolName).font(.headline)
                                            Text(card.role).font(.subheadline.bold())
                                            Text(card.effect).font(.body)
                                            Text(card.numericSummary).font(.body.monospacedDigit())
                                            Text(card.exclusions).font(.body)
                                        }
                                        .fixedSize(horizontal: false, vertical: true)
                                        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
                                        .padding(18)
                                        .background(Color.white.opacity(0.07), in: RoundedRectangle(cornerRadius: 12))
                                        .overlay(RoundedRectangle(cornerRadius: 12).stroke(Color.white.opacity(0.5)))
                                        .contentShape(Rectangle())
                                    }
                                    .buttonStyle(.plain)
                                    .disabled(model.submitted)
                                    .accessibilityLabel(card.voiceOverLabel)
                                    .accessibilityHint("Choose this upgrade and resume the run")
                                    .accessibilityIdentifier("upgrade-\(card.upgrade.rawValue)")
                                }
                            }
                        }
                        .padding(24)
                    }
                }
                .foregroundStyle(.white)
            }
        }
    }
}
