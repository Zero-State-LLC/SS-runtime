# Recording-load frame miss: measured diagnosis

All 80 moving observations match the proposed distance-phase formula. Missing source frame 15 is selected only on ticks 30, 60, 90 and 120 for this full-input route. The recorded callbacks bracket each opportunity at 29→31, 59→61, 89→91 and 119→121. This establishes a display-sampling miss, not incorrect phase arithmetic or malformed source art. The initiating delay remains unproven.

Opt-in Debug stage timing is now available in GameSession. The regression compares every tick's digest and events plus final command logs with timing disabled, for both measured/control execution orders. Fresh suite: 117 named tests / 119 executions passed, zero failures. Prior recorded failure remains open.

Across 240 measured steps, stage medians were simulation 1.86–1.87 ms, HUD/captions/quiet/feel 1.31–1.35 ms, awareness snapshot/hint 1.21–1.24 ms. Awareness snapshot/hint consumed about 28% of measured session time. These are coarse, overhead-inclusive Debug simulator timings, not CPU samples or proof of the original recording bottleneck.

Next: inspect and remove unnecessary full-snapshot construction in presentation-only hint/feel paths if exact semantic parity can be demonstrated. Preserve tick/event timing, first-visible-enemy behavior, damage/AI authority, command/replay invariants and unchanged animation coverage. Use a CPU/GPU trace if reduced CPU work does not resolve delayed callbacks. Do not lengthen the test, slow playback or queue stale poses to conceal the failure.
