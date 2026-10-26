# Reviewed settle timing acceptance — 2026-10-19

Owner response to the proposed0.375-second settle in native normal-speed clips: **“Timing feels right.”** Review page: `outputs/SS-player-settle-timing/midpoint-normal-speed.html`. This supersedes proposed timing status in older midpoint review notes. Earlier0.25s feedback remains “Too abrupt”;0.5s was too slow.

Accepted scope: duration of the reviewed phases5/13 candidate. Existing exact ClipTiming uses3/128s per source hold; neutral begins at48/128s, with first eligible60Hz sample at tick23(0.3833s). No rounding to integer FPS or gameplay speed change.

Not accepted by this timing answer: contact accuracy, lift amplitude, hidden surfaces, remaining release phases, facings, complete idle family, distance-based movement policy or production activation. The runtime's opt-in comparison already represents the accepted duration; production defaults and spec pin remain unchanged. Next work is source-backed contact/interruption coverage and remaining-phase expansion under this timing baseline.

Current complete playback regression:22 tests pass, zero failures/skips; see ../shared-distance-phase/full-suite-result.json. This pass is automated evidence, not visual approval.

Coverage inspection: `testBenchmarkSettleCancelsWithoutChangingSelectedState` uses distinct bundled textures, not the actual17-pose source sequences. It clears `benchmarkPlayerSettleSequences` before the terminal idle check. The next source-backed matrix must retain configuration to test non-resurrection, while allowing a genuinely new backed move→stop to create a new occurrence. This is a test-evidence gap, not yet an observed runtime defect.
