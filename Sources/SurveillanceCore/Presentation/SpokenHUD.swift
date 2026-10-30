/// `hud-tutorial.md` (copy is spoken in sentence case) and `acceptance.md`
/// F-013 (the first Camera encounter's copy reaches VoiceOver): what VoiceOver
/// announces during play.
///
/// Only what a player must not miss: tutorial copy, the heat reinforcement
/// caption, and safety captions. Each is announced once when it appears.
/// Routine captions stay on screen only; announcing every shot would bury the
/// warnings. Presentation only: it reads what the HUD draws and nothing else.
public struct SpokenHUD: Equatable, Sendable {
    private var tutorial: String?
    private var reinforcement: String?
    /// Sequences of safety captions already announced and still showing.
    private var announced: Set<Int> = []

    public init() {}

    public mutating func reset() {
        self = SpokenHUD()
    }

    /// The announcements for this frame, in order: tutorial, reinforcements,
    /// then new safety captions oldest first.
    public mutating func announcements(
        tutorial: String?,
        reinforcement: String?,
        captions: [CaptionBoard.Entry]
    ) -> [String] {
        var spoken: [String] = []
        if tutorial != self.tutorial {
            self.tutorial = tutorial
            if let tutorial, !tutorial.isEmpty { spoken.append(Self.sentences(tutorial)) }
        }
        if reinforcement != self.reinforcement {
            self.reinforcement = reinforcement
            if let reinforcement, !reinforcement.isEmpty { spoken.append(Self.sentences(reinforcement)) }
        }
        let safety = captions.filter { $0.captionClass == .safety }
        for caption in safety where !announced.contains(caption.sequence) {
            spoken.append(caption.text)
        }
        announced = Set(safety.map(\.sequence))
        return spoken
    }

    /// `MOVE TOWARD A CAMERA TO SHOOT IT • DESTRUCTION ADDS EXPOSURE` →
    /// `Move toward a camera to shoot it. Destruction adds exposure.`
    public static func sentences(_ copy: String) -> String {
        copy.components(separatedBy: " • ")
            .map { TerminalSpeech.sentence($0) }
            .joined(separator: ". ") + "."
    }
}
