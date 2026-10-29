# Agent gotchas — Surveillance Survivor Runtime

Environment notes that used to bloat `AGENTS.md`. Keep secrets out.
If a gotcha is fixed, delete the row. Do not leave historical traps as current guidance.

## Local environment

| Trap | What happens | What to do |
|---|---|---|
| Commit `SSRuntime.xcodeproj` or signing data | Personal team / bundle IDs leak; project.yml is no longer the source | Generate with `xcodegen generate`. The xcodeproj is gitignored. |
| Run `swift test` on Linux with Swift 6.0/6.1 | 6.0.3 rejects a Swift Testing `#expect` in `ClipMetadataTests`; 6.1 debug overflows the test-worker stack | Use Swift 6.2+ (e.g. the `swift:6.2-noble` image). macOS CI (`macos-15`) stays the authority; Linux runs only `SurveillanceCore`, never the app. |
| Expect scenario-seeded tests in a release probe build | `debug_` hooks and the two feel tests that use them compile only in Debug | Release probes compile; those two tests run in Debug and CI. |

## CI and validators

| Trap | What happens | What to do |
|---|---|---|
| First CI job skips `CameraPlacementTests` and `CameraFairnessTests` | Looks like those suites are gone | Later jobs run them with `--filter`. Do not drop those jobs to stay green. |
| App job greps `xcodebuild` then checks `PIPESTATUS` | Grep can hide a failed build if you drop the pipe check | Keep the `PIPESTATUS` gate. A red honest build is required. |

If a check looks green-but-inert, follow `AGENTS.md` **Escalation**. Do not
patch the test to match the broken path.

## Measurement traps

| Looks like | Actually is |
|---|---|
| Sprite / node bounds as hitboxes or Camera FOV | Authoritative geometry lives in `SurveillanceCore`, not rendered nodes |
| Wall-clock elapsed time as simulation advance | Fixed 60 Hz ticks. App suspension must not advance authority by wall clock |

Record only traps that have bitten someone. A measurement trap is not a product
defect. Do not file one as a bug.

## Do not put here

- Architecture invariants (those stay in `AGENTS.md`)
- Command tables (those stay in `AGENTS.md`)
- Tokens, mailbox passwords, or live world IDs
- Deploy runbooks
- Invented gameplay
