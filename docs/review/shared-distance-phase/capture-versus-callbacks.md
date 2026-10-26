# Capture timing versus renderer callbacks

OBSERVED from the recorded shared comparison: active post-action callbacks (tick > 0, outside warmup) have no intervals above50ms across the six Standard Motion variants. Exported movie intervals reach78–135ms. This demonstrates that the movie timeline is not equivalent to the callback timeline; it does not establish physical presentation cadence.

| Case | Callback median ms | Callback max ms | Captured max ms | Update median ms | Update max ms |
|---|---:|---:|---:|---:|---:|
| full-fixed | 17.60 | 42.60 | 135.00 | 6.72 | 32.75 |
| full-distance | 17.42 | 37.47 | 103.33 | 7.08 | 13.79 |
| half-fixed | 16.96 | 42.01 | 81.67 | 6.40 | 13.63 |
| half-distance | 16.80 | 47.08 | 78.33 | 7.55 | 20.96 |
| quarter-fixed | 16.87 | 36.80 | 85.00 | 6.54 | 17.00 |
| quarter-distance | 16.81 | 43.83 | 86.67 | 7.11 | 16.23 |

INFERRED: recorder/output sampling contributes to the visible gaps. Do not attribute all observed stutter to game update work, or assert flawless rendering from callback coverage. There are still37–47ms callback intervals and one32.75ms update. Clean native capture, actual sole/ground tracking and performance-floor device profiling remain open.50ms is a descriptive bin here, not an adopted budget or acceptance threshold. Movie gaps are measured in the final trimmed windows; callback statistics cover all active observations for each complete variant, so these are interval distributions, not one-to-one aligned events.

Inputs: recording-coverage.json, recording-attachments/, source-pts-verification.json. Derived values: recording-callback-cadence.json.

## Next capture comparison

Apple documents Simulator recording through `simctl io … recordVideo` in [Become a Simulator expert](https://developer.apple.com/videos/play/wwdc2020/10647/). This provides a supported alternative capture path, not a guarantee of frame-perfect output. A read-only local `simctl help io` check on2026-10-19 could not connect to CoreSimulatorService from the restricted shell and reported denied log access. Xcode's current native test run remains active; do not interpret the shell error as an application crash or restart the simulator during that run.

Next isolated recording should capture a single labeled variant with preparation excluded from the review interval, preserving native callback records and source PTS. Compare capture intervals and visible source poses to the same run's post-action trace before presenting normal-speed cadence as review evidence. Retain original geometry, command stream, idle tail and assertions. Use the supported Simulator UI path if direct service access remains unavailable; capture-path substitution itself must be measured, not assumed to cure gaps.
