# Playback timing investigation

Observed from retained callback costs: median simulation cost per advanced tick is approximately 6.4–7.1 ms in these Debug simulator runs. The recorded full-input Reduced Motion distance run includes two callbacks advancing nine ticks each; the unrecorded counterpart advances at most three per callback. The recorded run's maximum measured simulation cost per individual tick is 10.09 ms, while its maximum callback interval is 152.74 ms. This supports accumulated catch-up work as a contributor after a delay, but does not identify the initial delay's cause.

Do not drop simulation ticks, change controller speed, remove authoritative actors or weaken coverage to hide the symptom. No production performance fix is justified from callback aggregates alone. The source-frame selection adds only a bounded texture lookup, but it has not been profiled as a call-tree cost.

Next: profile the same scenario with recording disabled, preserve thread-state and Time Profiler evidence, then repeat the measured condition. Apple describes using Instruments to separate running and blocked thread time in https://developer.apple.com/documentation/xcode/reducing-your-app-s-launch-time and its Release profiling workflow in https://developer.apple.com/videos/play/wwdc2025/306/ . These are tool-method references, not proof of an SS bottleneck. Keep Debug test-fixture evidence distinct from optimized shipping/device performance.

The expanded animation interruption guard is being validated separately. It does not claim to cure these timing spikes.
