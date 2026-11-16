# Playback #237: retained failure investigation

Status: UNRESOLVED. Earlier claims of an established harness-only cause and cold-test ordering are withdrawn. The later autopilot log is not evidence about this test. No fix is justified yet. No explicitStepSeconds change is proposed.

## Exact retained evidence

`evidence/github-metadata.json` retains artifact and run fields fetched through `gh api` at06:22:51UTC: artifact14198828420,724246160bytes, API digest `sha256:2b90932b5229614dd75fa682b708178f6ccdada4995f02dc4c3fdf449ff50675`, full head `9769d922cc8f3e908c0d611dd2f48df6418089cd`. The digest is GitHub metadata, not a locally recomputed archive checksum.

Fetched `gh run download 43803119616 --name app-tests-Debug -D /tmp/artifact-debug`, then moved only that owned download to the previously absent `/Users/appliedalchemylabs/.jcode/scratch/ss-playback237-ci-43803119616`. Retained source: `/Users/appliedalchemylabs/.jcode/scratch/ss-playback237-ci-43803119616/SSRuntime.xcresult`, with `xcodebuild.log`. The initial `/tmp` placement was an incorrect scratch-location practice, not the current reproduction path.

`xcrun xcresulttool get object --legacy --path /Users/appliedalchemylabs/.jcode/scratch/ss-playback237-ci-43803119616/SSRuntime.xcresult --format json` identifies one failure: `DisplayedPlaybackTests.testSharedProjectedPlayerGroundedShadowComparison()`, XCTAssertEqual 15 versus 16 at source line1184 (xcresult URL uses zero-based1183).

The testsRef is `0~ngy7oQVXGJplVebtJAOFn6bEtkWXgv5U1KoqrOaPoP-vdRrKXhANryAarSm3iCbQDiE-h84E2n1ICbWQyOHIsg==`.
The failed test summaryRef is `0~0IRy-N5ahkoXp9wBprKuxVuk-zU2afvRdu8yGaGfTJ0annSBZOtzHFB8DTM8gXhlnuoXFJVRo1V8-SeZC41rwQ==`.

Six JSON attachments were exported using `xcrun xcresulttool export --legacy --path ... --id <payloadRef> --output-path <file> --type file`. Their unmodified bytes are retained in `evidence/act0.json` through `act5.json`. Attachment name and payload references are retained in `evidence/attachments.json`.

| Index | Zoom | Tracking | Reduced | Records | Observed poses |
|---|---|---|---|---|---|
|0|1.0|false|false|91|all16|
|1|1.0|false|true|93|all16|
|2|1.25|false|false|92|all16|
|3|1.25|false|true|89|all16|
|4|1.25|true|false|63|0...14, missing15|
|5|1.25|true|true|89|all16|

This refutes the earlier guessed nontracking/Reduced case for this exact run. Historical #237 observations must not be substituted for this run.

### Failed case observations

Movement has44 records. Frame14 at tick29 / SpriteKit time1724.76666667 is followed by frame0 at tick32 / time1724.83106667, approximately64.4ms later. Frame15 is not observed anywhere in this case. The subsequent cycle includes frame9/tick49 -> frame3/tick64 across approximately315.5ms, spanning another potential frame15 visit. The remaining movement ends at frame9/tick75, then idle begins at76. Thus this is not merely one skipped cycle. All authoritative positions/digests still require their independent checks.

Measured multi-frame transitions:
- ticks29->32: frame14->0,64.4ms
- ticks35->42: frame2->5,107.8ms
- ticks42->45: frame5->7,51.3ms
- ticks45->49: frame7->9,66.8ms
- ticks49->64: frame9->3,315.5ms
- ticks64->67: frame3->5,54.7ms

## Ranked hypotheses, not conclusions

1. Callback stalls prevent pose15 from being sampled on both complete cycles. Prediction: replaying the retained timestamp schedule through the actual SKAction path reproduces absence15 while regular timestamps cover16. This would explain observed sampling, not establish stall origin.
2. Work inside the scene update causes stalls. Prediction: update-stage timings account for the gaps. Must compare entry/post-action times and stage totals before blaming rendering, shadow positioning or simulation.
3. Host scheduling or SpriteKit action evaluation contributes outside measured update stages. Prediction: substantial gap remains outside summed measured work. Native instrumented playback may distinguish this but cannot prove the historical host cause.

No source-equivalent-path argument excludes a production timing contribution. No deterministic selector may replace live playback coverage. No assertions, production assets, inputs, pin, or behavior were changed.

## Measured work versus uninstrumented interval

For ticks49->64, update-entry uptime advances316.7905ms. The preceding update total is17.4317ms, leaving299.3588ms outside that measured update. The new update takes40.2721ms. For ticks29->32, entry separation68.8028ms minus previous update3.5265ms leaves65.2763ms outside the previous update. These quantities do not attribute the remainder to host scheduling: action evaluation, rendering, driver/GPU work and uninstrumented test work may occur there. The large gap is NOT explained solely by the preceding measured update. No profiler or scheduling trace identifies the origin.

## Executable regression and honest red

```sh
python3 docs/review/playback237-diagnosis-20261116/extract_evidence.py /Users/appliedalchemylabs/.jcode/scratch/ss-playback237-ci-43803119616/SSRuntime.xcresult
python3 -m unittest discover -s docs/review/playback237-diagnosis-20261116 -p 'test_trace_probe.py' -v
python3 docs/review/playback237-diagnosis-20261116/trace_probe.py docs/review/playback237-diagnosis-20261116/evidence/act4.json --require-all-poses
```

Extraction succeeds for all six original attachments. The strict command was run and returns1 with missing `[15]`. Control act0 returns0. Seven diagnostic regression tests pass, including byte-hash provenance, five controls, exact failed-case identity, strict CLI red, removed-observation mutation and invalid/reversed input rejection. These tests validate the evidence reader, not corrected gameplay or reexecution of SpriteKit. The reader never reconstructs unseen poses from timing. No native canary was invented. Existing attachments already expose timing/pose detail, so no new simulator run or shared test edit was required for this bounded diagnosis.

## Separate #238 integration

`git merge-base --is-ancestor 3ad31ad HEAD` returned0. Exact full commit `3ad31adfb956be6389bfc263c0515b89c51b7f9c` CI run43805471684 fetched this turn is successful in all five jobs: device-sitting, app Release, swift, app Debug, spec-parity. This verifies commit ancestry and CI integration only. Independently ran `python3 -m unittest discover -s docs/review/player-ground-contact-20261116 -p 'test_native_evidence.py' -v`:14 tests passed in29.809s, including rejection of the old clamped run and missing-loop mutations. It does not fix #237 or certify live cadence. Neither issue was closed.

## Validation limits

Five existing ClipTiming tests passed via `swift test --filter ClipTiming`. An earlier invented filter selected zero tests and is NOT validation. Neither command exercises SpriteKit playback. No native execution yet. The retained trace analysis is a diagnostic replay, not a fix or full runtime reproduction. No commits or pushes.
