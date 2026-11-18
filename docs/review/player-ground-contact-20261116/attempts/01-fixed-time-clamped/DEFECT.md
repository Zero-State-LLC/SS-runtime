# Attempt 01: fixed-time clamped (INVALID, history only)

- **Run:** `ss-groundcontact-native-20261116-0348.xcresult`, executed at 03:48 UTC.
- **Code that ran:** `PlayerGroundContactNativeTests.executed.swift`, SHA `b5b77ecd…`.

**Defect (runtime#238):** fixed-time frames came from `ClipTiming.frameIndex(atTickOffset: tick - start)`, which clamps by design. After 30 ticks every fixed-time row stayed on frame 15. That froze 900 of 1,200 fixed-time rows. The spans this run reported for fixed-time (9.128662 / 6.300262 / 3.106598) are invalid. The distance-phase rows were valid, but the active packet supersedes them.

**What is kept here:**
- `native/`: the exact captures and records from this run.
- `native-results-0348.md`: the results as reported at the time, including the later correction.
- `native-xcode-test-0348.log`: the run log.
- `verify_native-0348.py`: the verifier as it stood then, which recorded the defect.

The current `verify_native.py` rejects these records by their frame selection, not only by their counts. `testOldClampedRunRejectedBySelectionNotOnlyCount` covers that.
