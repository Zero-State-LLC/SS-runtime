# Final coordinator binding prepared, November16 23:17UTC

Consumed the coordinator-authored `../recommendations.json`, backed by actual
`../SOURCE-REVIEW-FINAL.md` SHA256
`a633d036627b0b7da7ea09faa370b0d1a5fb00615d117f5c0760d7c4b5d2ac9e`.
This worker did not author or independently recommend source art.

Actual `native.py bind` and `native.py prepare` both exited0. Logs:
`bind-final.log`, `prepare-final.log`. A separate fresh Python import reran the real
semantic oracle and temporary deterministic replay, then verified exact equality
with `expected_input()` and all ten staged PNG SHA256 values at23:17UTC.
All thirteen generated correction outputs match the reviewed source byte-for-byte.
Replay writes only temporary output, not the reviewed source packet or another art attempt.

| Artifact | SHA256 |
| --- | --- |
| `assembly.json` | `a7053a54f0dfa57deda6ee1d11e922d9ad93c18662f596e4a8a6597353ecf11f` |
| `native-inputs-v8/native-inputs.json` | `01b8a38131be4157c3c8120cb6d378cdc21b5e31fb580673d1a46374604d5f78` |
| Frozen Swift fixture | `47264781c7059f5dd7f650c30aac6ac1c50ebe913ab2270b9757f75ce0aed3c1` |
| Immutable shared semantic plan | `3b145fc228ac73367b1d6c5d60ee48e1578ebdbc972493afa9ba5a91018d880b` |

## Exact staged source bytes

| Role | SHA256 |
| --- | --- |
| paving | `f4a3f542d8879b036c1a1979ab5fa03356b69350181fb526e190098982191dac` |
| camera | `1343507b7517cd2a4848810b14aca88644677f35266ec8299dcbbf8347ef5ab1` |
| player | `b32bfcba5ac7cee383715d5f0b918e53b2e7be56634886754ab82357431d6ed4` |
| stone | `5b5751602fb5299777a134fcb1dbedf4de1822a8e1375d86505c88056a240539` |
| kiosk | `c411e33b79e0ffc5b0eb86143cd8785a564e573b5819bc1d4c399ef5d3b60264` |
| context-01 | `edf9d79bb71337eb908ab654a11e6011e8b69354101f30dab2dffbd401073482` |
| context-02 | `d1ed85e7a64965c9063db1533672ef07d8b4e9c81588f5c11f9a711f57a75355` |
| context-04 | `26640bb8c2c92e08679643e028346f5c926a5d2fbd021f5996b03d6081a42948` |
| context-05 | `4cb22248df71f1a3ff956c52ab76bdcc3a8aac01ce598e13097db52b9615a204` |
| ground-plan | `97ae5825c57c9e21b48a3d863bfd3e93b940e3eb5c5134b9c51172cc6656b7c7` |

First nine sources/registrations remain exact V7 bytes. Only ground-plan is new.
Candidate props follow unchanged final semantic plan: prop0 `[691,639]`, tree `[858,716]`.
Full source-base clearance is separate from new baked-shadow/contact limits.

Latest owned portable run: **56 tests passed**, `tests-correction-binding.log`.
Swift remains frozen at the compiled hash. No worker native build/run, project
generation, commit, push or unfiltered Swift test. Coordinator reported build success
and binary `350e5db4e74bf86d992747953c15a03eb76b38493e9398c0333fc5adb97a550f`,
but actual loaded-binary agreement still requires the coordinator's native run/import.
No V8 native capture, pixel parity result or visual acceptance is claimed here.
