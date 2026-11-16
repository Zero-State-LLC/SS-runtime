# Explicit v6 gallery support

This gallery retains v5 as its default and preserves the v4/v5 paths and checks. The third, explicit selection `v6` uses only `../../scene-qa-framing-20261116/native-capture-v6/` relative to this gallery. It never falls back to v5 or v4.

The contract is bound to the new `AppTests/SceneQAFramingTests.swift` record literals:

- Fixture: `source-scene-qa-006-control-framing`.
- Record schema: `source-scene-records-006`.
- Record and verification status: `NATIVE_QUIET_SOURCE_COMPARISON_NOT_ACCEPTANCE`.
- Same one-test, six-capture, eighteen-image census and static quiet scope.

The v6 option initially says **pending evidence verification**. Every v6 load resets that label. Only after fixture/schema/provenance checks, the exact record-byte hash, all eighteen PNG hashes and decoded dimensions succeed does its label say **hash-verified capture, not acceptance**. Failed loading clears all prior displayed captures, disables comparison controls and shows no alternate capture. Neither existence of the new selector nor passing synthetic tests establishes v6 native evidence.

Native/half logical sizes remain 704x326 and 352x163. Grayscale selection remains reversible, and the existing full benchmark aspect ratio and CSS rules are unchanged. No browser or native run was performed for this change.

## Focused checks

```sh
node docs/review/scene-qa-repair-20261116/gallery/test_evidence.js
node docs/review/scene-qa-repair-20261116/gallery/test_loader.js
node --check docs/review/scene-qa-repair-20261116/gallery/gallery.js
```

Default evidence checks read the actual retained v4/v5 packets: 36 PNG hashes/dimensions, 48 image/size/grayscale selections, and the original 15 rejection cases. Fifteen added in-memory v6 protocol mutations reject wrong record/verification fixture versions, wrong record schema/status, wrong capture identity, mismatched PNG/input/harness/executable hashes and unsupported acceptance, including selecting a synthetic v6 packet as v4/v5.

The loader test runs the real gallery code with a synthetic DOM/network/image decoder. It verifies missing v6, v5-at-v6-path mismatch, corrupt PNG bytes, changed record bytes, pending/verified label transitions, old object-URL release, and no fallback even when v5 is available. It also exercises 36 retained-v5 control combinations, with exact logical sizing and grayscale restoration. Synthetic v6 data exists only in memory and is explicitly reported as synthetic. It is never written into the native packet directory or published as capture evidence.

After the coordinator imports real v6 evidence, require it explicitly:

```sh
node docs/review/scene-qa-repair-20261116/gallery/test_evidence.js --require-v6
```

This mode fails if any v6 record, verification or PNG is absent or invalid. It does not silently skip unavailable v6 evidence. Success will cover three actual packet versions and 54 PNGs, while still not constituting a browser/native execution or visual acceptance.

During implementation the first loader execution encountered Node's read-only global WebCrypto getter. The harness now uses the existing getter and installs a fallback only if absent. Assertions and gallery validation were not weakened.
