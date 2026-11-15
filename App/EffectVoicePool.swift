/// One device-level budget shared by ordinary and pitched effects.
/// Lower priority numbers are more important. Array order is admission age,
/// not projector sequence (which can restart with a new projection/session).
@MainActor
final class EffectVoicePool {
    private struct Voice {
        let priority: Int
        let isPlaying: () -> Bool
        let stop: () -> Void
    }
    private var voices: [Voice] = []
    var count: Int { voices.count }

    func admit(priority: Int, isPlaying: @escaping () -> Bool, stop: @escaping () -> Void) -> Bool {
        voices.removeAll { voice in
            guard !voice.isPlaying() else { return false }
            voice.stop()
            return true
        }
        if voices.count == 8 {
            let lowest = voices.map(\.priority).max()!
            guard priority <= lowest else { return false }
            let oldest = voices.firstIndex { $0.priority == lowest }!
            voices.remove(at: oldest).stop()
        }
        voices.append(Voice(priority: priority, isPlaying: isPlaying, stop: stop))
        return true
    }

    func stopAll() {
        for voice in voices { voice.stop() }
        voices.removeAll()
    }
}
