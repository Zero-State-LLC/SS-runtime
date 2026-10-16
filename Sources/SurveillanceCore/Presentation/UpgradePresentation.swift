/// hud-tutorial-001 / upgrades-001 protected selection presentation. Presentation-only.
public enum UpgradePresentation {
    public struct Card: Equatable, Sendable {
        public var upgrade: UpgradeID
        public var selectionIndex: UInt8
        public var name: String
        public var role: String
        public var effect: String
        public var exclusions: String
        public var symbolName: String
        public var numericSummary: String
        public var voiceOverLabel: String
    }

    public static let selectionOrder: [UpgradeID] = [.signalJammer, .ricochetPulse, .ghostStep]

    public static func selectionCards() -> [Card] {
        selectionOrder.map(card(for:))
    }

    public static func voiceOverLabels() -> [String] {
        selectionCards().map(\.voiceOverLabel)
    }

    public static func card(for upgrade: UpgradeID) -> Card {
        switch upgrade {
        case .signalJammer:
            Card(
                upgrade: .signalJammer,
                selectionIndex: 0,
                name: "Signal Jammer",
                role: "Surveillance control",
                effect: "Build Exposure more slowly under surveillance.",
                exclusions: "No Tamper or damage reduction.",
                symbolName: "antenna.radiowaves.left.and.right.slash",
                numericSummary: "Camera gain −1/tick (min 1); Fog/Observation −25%",
                voiceOverLabel:
                    "Signal Jammer. Surveillance control. Reduces camera contact gain by one point per tick, minimum one. Reduces fog and boss observation pulses by twenty-five percent. No Tamper or damage reduction."
            )
        case .ricochetPulse:
            Card(
                upgrade: .ricochetPulse,
                selectionIndex: 1,
                name: "Ricochet Pulse",
                role: "Crowd control",
                effect: "A hit can continue to one nearby enemy or camera at full damage.",
                exclusions: "Requires clear line of sight. No third hit.",
                symbolName: "arrow.triangle.branch",
                numericSummary: "One continuation per hit; 160 unit range",
                voiceOverLabel:
                    "Ricochet Pulse. Crowd control. Each civic pulse hit may continue once to a second enemy or camera within one hundred sixty units, excluding the first target, at full damage with clear line of sight. No third hit."
            )
        case .ghostStep:
            Card(
                upgrade: .ghostStep,
                selectionIndex: 2,
                name: "Ghost Step",
                role: "Mobility and surveillance evasion",
                effect: "Dodge faster and briefly disappear from camera detection.",
                exclusions: "No damage immunity. Fog, Observation and Tamper still apply.",
                symbolName: "figure.run",
                numericSummary: "540 u/s for 0.2 s; 1.5 s cooldown; 0.5 s camera concealment; no damage immunity",
                voiceOverLabel:
                    "Ghost Step. Mobility and surveillance evasion. Dodge speed five hundred forty units per second for zero point two seconds, one point five second cooldown, camera concealment for thirty ticks including dodge start, zero point five seconds. No damage immunity. Fog, Observation and Tamper still apply."
            )
        }
    }
}
