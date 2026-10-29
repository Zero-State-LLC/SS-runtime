# Device retest checklist (issue #117)

Allowed on any build by D-105 (SS-specs #67). Record the build and art state; this session tests feel, performance and correctness, not art admission (D-022–D-024, E-021 stay open).

## Setup

1. Check out `main` and record the commit: `git rev-parse HEAD`.
2. `xcodegen generate`, open `SSRuntime.xcodeproj`, scheme `SSRuntime`.
3. Edit Scheme → Run → Build Configuration **Release**. Add the launch argument **`-SSQA`** and disable "Debug executable".
4. Install on the iPhone. Record model and iOS version. The 2026-10-13 sessions used an iPhone 17 Pro on iOS 26.3.1 (iPhone18,1).
5. Open Console.app, select the phone, and filter on subsystem `com.zer0state.surveillancesurvivor`, category `device-qa`.

`-SSQA` logs `QA device=… p50 p95 p99 worst` every 300 frames and one `QA_DAMAGE {…}` line per Player hit. At each run end it writes:
- `Documents/SS-damage-QA-latest.json`: the whole run's damage events and commands. Before #143 this export stopped at M-A.
- `Application Support/ReleaseEvidence/device-run-*.json`.
- After three consecutive successes: the release-candidate bundle and the expansion-gate report in the same folder. Before #143 this could never happen.

Copy them off with Xcode → Window → Devices and Simulators → the app → Download Container.

## Runs

Play from the title (Start). Three runs:

| Run | Style | Goal |
|---|---|---|
| 1 | natural | reach the Captain Court |
| 2 | sneaky (avoid Cameras and patrol cones) | finish |
| 3 | loud (shoot Cameras) | finish |

For the release-candidate bundle you need three **consecutive successes**; a failure resets the count. Keep playing until you have them, or record that you could not.

## Re-check every 2026-10-13 finding

Mark each PASS / FAIL / NOT SEEN, with a timestamp or screenshot.

| # | 10-13 finding | What to look for |
|---|---|---|
| 1 | Camera animation frames contain separated fragments | Do Cameras look like one complete device in every state (intact, hit, critical, destroyed)? Any floating pieces? |
| 2 | Solid art leaves invisible blocking space | Walk along every building edge. Are you ever blocked where nothing is drawn, or allowed into something drawn as solid? |
| 3 | Unrecognizable characters, broken animation | Can you name each enemy type at phone distance? Note which ones you can't. |
| 4 | Damage with no visible source | When Integrity drops and you can't see why, note the time. Afterwards, match it to the `QA_DAMAGE` line: `sourceEntityId`, `damageKind`, `ownerEntityId`. Probes show Vendor **mines** are ~9% of all damage, so look at the ground. |
| — | Stutter and view jumps | Note any hitch. Afterwards, copy the `p95/p99/worst` lines. C-003 target: p95 ≤ 16.67 ms. |

## Interruptions (D-106, once runtime #142 is merged)

| Vector | Action | Expected |
|---|---|---|
| RS-025 | Mid-combat, pull down Control Center | Pause surface is up on return; no ticks passed |
| RS-026 | Mid-combat, switch apps for 10 s and come back | Still paused until you press Resume |
| RS-030 | Mid-run, have someone call the phone (or trigger Siri) | Game audio stops; music returns after the call |
| RS-031 | With iOS Settings → Accessibility → Motion → Reduce Motion on, delete and reinstall the app | Reduced Motion is on in the game's Settings |

## Record

Add `docs/review/device-qa/retest-<date>.md` with:
- the commit and art state (production art; the benchmark art is test-only);
- the device;
- the table above filled in;
- the QA log excerpts.

Attach the downloaded JSON files, or summarize them if they are large. Leave #117 open unless every row passes.
