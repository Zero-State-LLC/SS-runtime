# Canonical hashing cost, November 17, 2026

## Measured cause and bounded change

The actual Debug simulator process sample collected at02:39UTC is retained as `hash-profile-before.txt`. Its3074main-thread samples include1338under GameScene.update and215under CanonicalJSON.sha256Hex, of which188enter the portable SHA256 algorithm. This is a sampled call-stack observation, not a causal explanation of intermittent playback237 or traversal259. It is not a physical-device frame-time result.

The change uses CryptoKit SHA256 on platforms that provide it and retains the existing portable implementation on other platforms. The portable body is unchanged and remains directly exercised on Apple hosts. Lowercase hexadecimal formatting now maps nibbles to ASCII rather than invoking Foundation formatting once per byte. Serialization, hash inputs, empty digest, API return types and simulation tick behavior are unchanged. No digest caching, sampling, omitted ticks or disabled hashing is introduced.

## Reproducible isolated measurement

```sh
swiftc -O Sources/SurveillanceCore/Determinism/SHA256.swift \
  docs/review/production-execution-20261117/HashBenchmark.swift \
  -o "$JCODE_SCRATCH_DIR/ss-hash-benchmark-20261117"
"$JCODE_SCRATCH_DIR/ss-hash-benchmark-20261117"
```

Observed exit0 at02:54UTC. Raw five-round measurements: `hash-benchmark-release.json`. Each size uses16deterministic binary payloads, prechecks exact equality, warms both paths and alternates measurement order. The baseline is the retained original hash plus original Foundation formatter. The checksum consumes every output. This is a host macOS optimized executable, not the app or an iPhone benchmark. Other qualification work was active, so results are not controlled thermal/performance certification.

| Payload bytes | Iterations per round | Median old/new cost ratio |
|---|---:|---:|
| 0 | 1000 | 25.48x |
| 64 | 1000 | 37.61x |
| 1024 | 1000 | 25.49x |
| 4096 | 1000 | 20.74x |
| 65536 | 100 | 14.38x |

A second execution with `-Onone` completed exit0 at02:59UTC. Its exact same harness and workload are retained in `hash-benchmark-debug.json`. Debug median old/new ratios were9.52x,12.29x,60.33x,150.89x and988.01x for the same ascending payload sizes. Large Debug ratios compare the deliberately unoptimized Swift fallback against the platform implementation. They do not predict whole-app acceleration.

These ratios apply only to the complete isolated hash-to-hex operation, not the simulation, app CPU utilization or FPS. Both host build configurations were measured, but no before/after native frame-rate comparison has been performed.

## Compatibility verification

`SHA256ParityTests` covers empty/abc/multi-block/million-a fixed known vectors in both paths, every input length0...257plus larger block boundaries through65536bytes, binary byte values, UTF8/non-ASCII/NUL input and exact lowercase output. Canonically equivalent Unicode strings must retain distinct UTF8 digests rather than being silently normalized.

Focused command: `swift test --filter 'SHA256ParityTests|DeterminismTests|Replay'` completed exit0:23tests in8suites passed, including the three new parity tests, live replay lockstep, unknown-version rejection, complete-run digests and replay-earned medals. Raw build/test log: `hash-parity-tests.log`. The211.658second test run included211.656seconds in the existing medal replay fixture. A no-output watchdog fired while that CPU-active fixture ran, and a process sample established the active stack before waiting for successful completion. No timeout or test assertion was changed.

Two aggregate attempts exceeded the tool's600second execution deadline and exited124. Their unmodified output is retained as `hash-core-timeout.log` and `hash-chained-timeout.log`, with the latter task status JSON. The second tool request specified1800seconds but was still terminated at600seconds. This is not a passing aggregate command. Its feel/medal and pacing subprocesses completed, then the camera/game-feel/transit stage ran out of the aggregate budget. No assertions, fixture sizes or application timing requirements were weakened.

Separate bounded commands completed exit0 against the post-hash, pre-socket-order-fix host binary:

| Partition | Swift Testing reported result | Raw log |
|---|---|---|
| Broad, excluding eight long suites |781tests/119suites | `hash-core-fast.log` |
| FeelPassPresentationOnlyTests and MedalTests |20tests/2suites | `hash-feel-medal.log` |
| PacingSegmentsTests and PacingProbeTests |9tests/2suites, two existing optional probes skipped | `hash-pacing.log` |
| GameFeelTests, TransitPatrolTests, CameraPlacementTests, CameraFairnessTests |57tests/4suites | `hash-final-partition.log` |

Do not add the overlapping focused23-test run to these partition counts. The broad log also contains a separately reported XCTest case. Final socket-ordering change fed8a3d is covered by21independently rerun socket/hash/reinforcement tests, the unchanged8native review tests and fresh native traversal. It is not silently attributed to the earlier host binary.

Final native existing-art traversal passed, and the unchanged strict importer verified2arms,52scene images,824post-action rows,50texture images and1073delivered resource bindings. Final Release rebuild passed, with review code/launch strings/image hashes absent from the actual product. See `../kiosk-only-geometry-20261117/native/playable/ACTUAL-PLAYABLE-REVIEW.md`. These checks are integration evidence, not frame-rate or physical-device certification.

## Remaining gates

Playback237 and traversal259 remain open and unresolved. No assertion, timing envelope, accepted gate or golden digest is weakened. Supported physical-device matrix and frame-time acceptance remain separate requirements. This change grants no art acceptance, merge, release or deployment.
