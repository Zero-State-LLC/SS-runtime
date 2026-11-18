# Issue253 exact storage repair and retry preparation

Coordinator reported native2317 failed one test at the ground patch equality guard,
before capture. Actual coordinator SpriteKit probe is
`../ground-property-probe-2318.log`: assigning zPosition0.1 reads back
`0.10000000149011612`, exactly `CGFloat(Float(0.1))`, not `CGFloat(0.1)`.
Issue253 was filed before this oracle correction. No art defect is inferred.

Coordinator authorized only one Swift assertion-line repair: compare to the exact
Float-backed stored value and include observed size, anchor, zPosition, expected
stored Z, hidden and alpha in the failure diagnostic. No tolerance was added or
widened, no other condition changed, and no source/art/authority bytes changed.

## Current retry inputs

- Frozen Swift SHA256: `3ab178cdbc141f51e3ee0ccfd5e30b6a2e29e6e562bf8d98ef0fe8cb797dcef5`.
- Stable `native-inputs-v8/native-inputs.json` SHA256: `598ec899b0171b9cf6ca32366a15053ad4666d15e8ebad7e0d792fea3c95bdbf`.
- Assembly remains `a7053a54f0dfa57deda6ee1d11e922d9ad93c18662f596e4a8a6597353ecf11f`.
- All ten staged source PNGs retain the exact hashes listed in `BINDING.md`.
- Actual fresh preparation exited0, `prepare-retry-issue253.log`.

## Preserved failed attempt

`attempt-01-native2317/` retains the old input directory intact, copied original
assembly/bind/prepare logs and binding/freeze documentation. Its archived Swift source
was reconstructed by reversing the sole changed assertion line, then independently
verified against exact original SHA `47264781c7059f5dd7f650c30aac6ac1c50ebe913ab2270b9757f75ce0aed3c1`.
The old input manifest remains exact SHA
`01b8a38131be4157c3c8120cb6d378cdc21b5e31fb580673d1a46374604d5f78`.
Every one of17 archived files passed `shasum -a 256 -c ../attempt-01-native2317.sha256`
at23:21UTC. Original native2317 logs/xcresult remain coordinator-owned and untouched.
No failed result is rewritten into passing evidence.

## Validation and gate

Swift frontend parse passed23:19UTC. Three new source-only regression guards verify
exact IEEE754 Float storage, exactly one changed assertion line with all other
conditions retained, diagnostic completeness and old preparation/source hashes.
The complete owned suite passed **59 tests** at23:21UTC (`tests-issue253-retry.log`).
These guards do not pretend to execute SpriteKit. Native storage evidence comes from
the coordinator's actual probe, not this worker's Python arithmetic.

The coordinator owns rebuild and one retry with the new frozen Swift and fresh input
hash. No worker native build/run/project generation occurred. If the same failure
recurs, stop rather than weakening the check or running a third attempt.
