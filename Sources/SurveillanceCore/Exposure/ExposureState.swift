public enum DetectionState: String, Equatable, Sendable {
    case hidden
    case observed
    case tracked
    case hunted
    case lockdown

    public static func projected(_ exposure: Int) -> DetectionState {
        switch exposure {
        case 0..<200: .hidden
        case 200..<450: .observed
        case 450..<700: .tracked
        case 700..<1000: .hunted
        default: .lockdown
        }
    }
}

public enum ExposureReason: String, Equatable, Sendable {
    case cameraContact
    case recovery
    case cameraTamper
    case fogPulse
    case observationPulse
    case forcedLockdown
}

public struct ExposureState: Equatable, Sendable {
    public var exposure: Int
    public var detectionState: DetectionState
    public var noContactTicks: Int
    public var lockdownEntered: Bool
    public var peak: Int
    /// D-101 (exposure.md § Quiet approach): true until the Detection State
    /// reaches `tracked` or higher before M-C activates; latched false.
    public var quietApproach: Bool

    public init(
        exposure: Int = 0,
        detectionState: DetectionState = .hidden,
        noContactTicks: Int = 0,
        lockdownEntered: Bool = false
    ) {
        self.exposure = exposure
        self.detectionState = detectionState
        self.noContactTicks = noContactTicks
        self.lockdownEntered = lockdownEntered
        self.peak = exposure
        self.quietApproach = true
    }

    /// `exposure.md` constants: Camera Tamper Spike per destruction (D-086).
    public static let tamperSpike = 150

    /// `exposure.md` constants: Tamper floor, per Camera destroyed this run (D-084).
    public static let tamperFloorPerCamera = 150

    /// exposure.md § Court release (D-109): the Exposure assigned when the
    /// Daemon falls and the Lockdown latch is released.
    public static let courtReleaseExposure = 700

    /// § Court release, step 1: clear the latch and assign 700. The Detection
    /// State is left as it is; the next tick's resolution projects it and
    /// publishes the one `lockdown`→final change.
    public mutating func releaseForCourt() {
        lockdownEntered = false
        exposure = Self.courtReleaseExposure
    }

    /// `upgrades.md` Signal Jammer: positive contact delta reduced by 1, to a
    /// minimum of 1; Fog and Observation pulses scaled by 75/100. The combat
    /// content contract must state the same values (`CombatContent.decode`).
    public static let jammerContactReduction = 1
    public static let jammerMinimumContact = 1
    public static let jammerPulseRatio = (numerator: 75, denominator: 100)
    /// D-113: heat reinforcements removed from each M-A/M-B wave (minimum 0).
    public static let jammerHeatReinforcementReduction = 2

    public static func contactDelta(cameraCount n: Int, signalJammer: Bool) -> Int {
        guard n > 0 else { return 0 }
        var delta = min(5, 2 + n - 1)
        if signalJammer {
            delta = max(jammerMinimumContact, delta - jammerContactReduction)
        }
        return delta
    }

    public struct Change: Equatable, Sendable {
        public var before: Int
        public var after: Int
        public var reason: ExposureReason
    }

    public struct Resolution: Equatable, Sendable {
        public var changes: [Change]
        public var contactDelta: Int
        public var tamperApplied: Int
        public var before: Int
        public var after: Int
        public var stateBefore: DetectionState
        public var stateAfter: DetectionState
        public var lockdownEnteredThisTick: Bool
        public var reason: ExposureReason
    }

    /// D-102 phases 13–14: all eligible deltas, then one final state/Lockdown.
    public mutating func resolveTick(
        survivingContactCount: Int,
        tamperAmounts: [Int],
        signalJammer: Bool,
        forceLockdown: Bool = false,
        destroyedCameras: Int = 0,
        fogPulseAmounts: [Int] = [],
        observationPulseAmounts: [Int] = []
    ) -> Resolution {
        let before = exposure
        let stateBefore = detectionState
        var reason: ExposureReason = .cameraContact
        var contact = 0
        var tamper = 0

        if lockdownEntered || forceLockdown {
            if forceLockdown && !lockdownEntered {
                exposure = 1000
                reason = .forcedLockdown
            } else {
                exposure = 1000
            }
            noContactTicks = survivingContactCount > 0 ? 0 : noContactTicks + (survivingContactCount == 0 ? 1 : 0)
            if survivingContactCount > 0 { noContactTicks = 0 }
        } else if survivingContactCount > 0 {
            noContactTicks = 0
            contact = Self.contactDelta(cameraCount: survivingContactCount, signalJammer: signalJammer)
            exposure += contact
            reason = .cameraContact
        } else {
            noContactTicks += 1
            // D-084 Tamper floor: recovery stops at 150 × Cameras destroyed.
            // It only limits recovery; it never raises Exposure.
            let floor = Self.tamperFloorPerCamera * destroyedCameras
            if noContactTicks > 60, exposure > floor {
                exposure = max(floor, exposure - 2)
                reason = .recovery
            }
        }

        for amount in tamperAmounts {
            tamper += amount
            exposure += amount
            reason = .cameraTamper
        }

        if forceLockdown {
            exposure = 1000
            reason = .forcedLockdown
        }

        exposure = min(1000, max(0, exposure))
        var changes: [Change] = []
        if exposure != before {
            changes.append(Change(before: before, after: exposure, reason: reason))
        }
        // Observation amounts already carry the boss phase and Signal Jammer
        // modifiers. Fog's existing modifier applies here exactly once.
        let namedPulses = fogPulseAmounts.map {
            (signalJammer ? Int(IntMath.divHalfAway(Int64($0) * Int64(Self.jammerPulseRatio.numerator), Int64(Self.jammerPulseRatio.denominator))) : $0, ExposureReason.fogPulse)
        } + observationPulseAmounts.map { ($0, ExposureReason.observationPulse) }
        for (amount, pulseReason) in namedPulses where exposure < 1000 {
            let pulseBefore = exposure
            exposure = min(1000, max(0, exposure + amount))
            if exposure != pulseBefore {
                reason = pulseReason
                changes.append(Change(before: pulseBefore, after: exposure, reason: reason))
            }
        }
        if exposure > peak { peak = exposure }

        var lockdownThisTick = false
        if exposure >= 1000 {
            exposure = 1000
            if !lockdownEntered {
                lockdownEntered = true
                lockdownThisTick = true
            }
        }

        detectionState = lockdownEntered ? .lockdown : DetectionState.projected(exposure)
        if lockdownEntered { exposure = 1000 }

        return Resolution(
            changes: changes,
            contactDelta: contact,
            tamperApplied: tamper,
            before: before,
            after: exposure,
            stateBefore: stateBefore,
            stateAfter: detectionState,
            lockdownEnteredThisTick: lockdownThisTick,
            reason: reason
        )
    }
}
