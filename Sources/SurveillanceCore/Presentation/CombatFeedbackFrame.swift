/// T1035 / CC-008: transient observations of a completed tick. Never serialized
/// into WorldState, used by rules, or substituted for authoritative events.
public struct CombatFeedbackFrame: Equatable, Sendable {
    public struct Shot: Equatable, Sendable {
        public var projectile: EntityID
        public var origin: VecQ8
        public var velocity: VecQ8
        public init(projectile: EntityID, origin: VecQ8, velocity: VecQ8) {
            self.projectile = projectile
            self.origin = origin
            self.velocity = velocity
        }
    }
    public var shot: Shot? = nil
    public var jammerReducedExposure = false
    public init() {}
}
