import SwiftUI

/// Isolated host of the unmodified production view and selection model.
/// No game simulation, native VoiceOver session or production admission claimed.
@main
struct SSUpgradeReviewApp: App {
    @StateObject private var model = UpgradeSelectionModel()
    @State private var selection = "none"
    @State private var count = 0

    private var size: DynamicTypeSize {
        let arguments = ProcessInfo.processInfo.arguments
        if arguments.contains("--accessibility5") { return .accessibility5 }
        if arguments.contains("--accessibility3") { return .accessibility3 }
        return .large
    }

    var body: some Scene {
        WindowGroup {
            UpgradeSelectionView(model: model) { index in
                guard model.submit(index) else { return }
                selection = String(index)
                count += 1
            }
            .environment(\.dynamicTypeSize, size)
            .overlay(alignment: .topTrailing) {
                Text("selected=\(selection);count=\(count)")
                    .font(.system(size: 9)).foregroundStyle(.yellow)
                    .background(.black)
                    .accessibilityIdentifier("review-selection-result")
            }
            .onAppear { model.synchronize(pending: true) }
        }
    }
}
