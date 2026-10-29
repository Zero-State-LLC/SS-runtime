/// audio-haptics.md § Captain and Daemon captions (D-111): the authority's
/// voice. Each attack caption names its form first, because that is the safety
/// information, then the justification. At most 40 characters each.
public enum CaptainCaptions {
    public static let maxLength = 40

    public static func telegraph(_ attack: BossAttackID) -> String {
        switch attack {
        case .safetyRationale: "Cone: for your safety"
        case .narrowTailoring: "3 bolts: narrowly tailored"
        case .temporaryOrder: "Field: temporary, indefinitely"
        case .independentReview: "Ring, 1 gap: independently reviewed"
        }
    }

    public static let daemonQuery = "Query: just a quick search"
    public static let daemonDash = "Dash: reasonable suspicion"

    public static func phase(_ phase: BossPhase) -> String {
        switch phase {
        case .publicSafety: "Public Safety: nothing to hide?"
        case .civilLiberties: "Civil Liberties: duly balanced"
        case .temporarySafeguard: "Safeguard: until further notice"
        case .independentReview: "Review: the Authority finds no fault"
        }
    }

    public static let defeated = "Authority defeated: no further questions"

    /// Every D-111 caption, for the length check.
    public static var all: [String] {
        [BossAttackID.safetyRationale, .narrowTailoring, .temporaryOrder, .independentReview].map(telegraph)
            + [daemonQuery, daemonDash]
            + [BossPhase.publicSafety, .civilLiberties, .temporarySafeguard, .independentReview].map(phase)
            + [defeated]
    }
}
