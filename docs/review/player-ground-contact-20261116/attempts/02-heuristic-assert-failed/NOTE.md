# Attempt 02: assertion heuristic failed (no evidence retained)

- **Run:** `ss-groundcontact-native-20261116-0425-looped.xcresult`. Fixed-time looping was already corrected in this run.
- **Result:** XCTest failed with 2 failures.

My added check required that frame 15 make up less than a quarter of picks. That threshold was arbitrary. It failed on `pause|distance-phase`, where a valid 15-tick pause holds frame 15 (76 picks against 75 allowed).

I replaced it with an exact pause-hold assertion: each held core tick keeps exactly one pose, and the pause has at least 15 held rows. No coverage was relaxed. The other multi-cycle checks still apply to every group:
- all 16 frames are selected;
- the cycle wraps at least once;
- every fixed-time frame equals `(offset % 30) * 32 / 60`.

The log is kept here. Attachments from this failed run were not imported.
