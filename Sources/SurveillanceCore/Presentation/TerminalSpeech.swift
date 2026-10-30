/// `acceptance.md` F-007 and `visual-assets.md`: the results surface works with
/// VoiceOver. `hud-tutorial.md`: copy drawn in uppercase is spoken in sentence
/// case. SpriteKit draws the surface; this is what VoiceOver reads for it.
///
/// Presentation only: it reads the run card and the drawn copy, nothing else.
public enum TerminalSpeech {
    public static let restart = "Restart"
    public static let share = "Share run summary"
    public static let rehearse = "Rehearse Court"

    /// The outcome title, then each card row in drawn order, as sentences.
    public static func summary(title: String, card: RunCard?) -> String {
        var sentences = [sentence(title)]
        if let card {
            sentences += card.rows.map { spoken($0, card: card) }
        }
        return sentences.joined(separator: ". ") + "."
    }

    /// `PEAK DETECTION` → `Peak detection`.
    static func sentence(_ copy: String) -> String {
        let lowered = copy.lowercased()
        guard let first = lowered.first else { return lowered }
        return first.uppercased() + lowered.dropFirst()
    }

    static func spoken(_ row: RunCard.Row, card: RunCard) -> String {
        switch row.label {
        case "TIME", RunCard.rehearsalLabel:
            return sentence(row.label) + " " + duration(row.value)
        case "CAMERAS":
            // `3/8 NETWORK BLACKOUT` → `Cameras 3 of 8, network blackout`.
            var parts = row.value.split(separator: " ", maxSplits: 1).map(String.init)
            let count = parts.removeFirst().replacingOccurrences(of: "/", with: " of ")
            return (["Cameras " + count] + parts.map { $0.lowercased() }).joined(separator: ", ")
        case "GHOST":
            return "Ghost " + ghost(row.value)
        case RunCard.medalsLabel:
            let medals = card.medals.map { sentence($0.name) + (card.newMedals.contains($0) ? ", new" : "") }
            return "Medals: " + medals.joined(separator: "; ")
        default:
            return sentence(row.label) + " " + row.value.lowercased()
        }
    }

    /// `RunCard.clock` text spelled out, so `5:12` is not read as a time of day.
    static func duration(_ clock: String) -> String {
        let parts = clock.split(separator: ":").compactMap { Int($0) }
        guard parts.count == 2 else { return clock }
        func unit(_ n: Int, _ name: String) -> String { "\(n) \(name)" + (n == 1 ? "" : "s") }
        switch (parts[0], parts[1]) {
        case (0, let s): return unit(s, "second")
        case (let m, 0): return unit(m, "minute")
        case (let m, let s): return unit(m, "minute") + " " + unit(s, "second")
        }
    }

    /// `NEW BEST`, or the signed gap `RunCard` draws against the stored best.
    static func ghost(_ value: String) -> String {
        if value == "NEW BEST" { return "new best" }
        guard let sign = value.first, sign == "+" || sign == "-" else { return value.lowercased() }
        let gap = String(value.dropFirst())
        if gap == "0:00" { return "level with your best" }
        return duration(gap) + (sign == "+" ? " behind your best" : " ahead of your best")
    }
}
