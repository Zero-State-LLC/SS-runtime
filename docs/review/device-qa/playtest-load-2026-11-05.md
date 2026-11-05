# Playtest load

Read 2026-11-05 from `PlaytestEvidenceLoader.load` on `ef68565`. No session field was changed.

The directory those files are read from stays in [evidence-names-2026-11-05.md](evidence-names-2026-11-05.md).

`load` requires a JSON object whose `taskId` is `T903` or `T904`, and a non-empty `sessions` array of objects. A bad root, any other task id, or an empty sessions array throws `PlaytestEvidenceError.invalidJSON`. Each session requires `participantId` as a string, `completedOnboardingWithoutInstruction` as a bool, and `describedExposureCorrectly` as a bool. A session missing one of those throws `invalidJSON`. `beganVoluntaryReplay` is that bool when the value is a bool, and false when the key is absent or the value is not a bool. `competentRunDurationMinutes` is stored as the `doubleValue` of an `NSNumber`, and is absent when that cast fails.

`loadAll` lists the directory, skips hidden files, keeps names whose extension is `json`, and loads each one.

This does not close T903 or T904.
