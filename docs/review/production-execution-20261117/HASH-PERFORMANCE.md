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

These ratios apply only to the complete isolated hash-to-hex operation, not the simulation, app CPU utilization or FPS. The observed sample is Debug, while this microbenchmark is optimized Release. No before/after native frame-rate comparison has been performed.

## Compatibility verification

`SHA256ParityTests` covers empty/abc/multi-block/million-a fixed known vectors in both paths, every input length0...257plus larger block boundaries through65536bytes, binary byte values, UTF8/non-ASCII/NUL input and exact lowercase output. Canonically equivalent Unicode strings must retain distinct UTF8 digests rather than being silently normalized.

Focused command: `swift test --filter 'SHA256ParityTests|DeterminismTests|Replay'` completed exit0:23tests in8suites passed, including the three new parity tests, live replay lockstep, unknown-version rejection, complete-run digests and replay-earned medals. Raw build/test log: `hash-parity-tests.log`. The211.658second test run included211.656seconds in the existing medal replay fixture. A no-output watchdog fired while that CPU-active fixture ran, and a process sample established the active stack before waiting for successful completion. No timeout or test assertion was changed.

The full non-camera host partition is running separately. Native integration and physical-device validation are not yet claimed for this change.

## Remaining gates

Playback237 and traversal259 remain open and unresolved. No assertion, timing envelope, accepted gate or golden digest is weakened. Native Debug/Release integration, supported physical-device matrix and frame-time acceptance remain separate requirements. This change grants no art acceptance, merge, release or deployment.
