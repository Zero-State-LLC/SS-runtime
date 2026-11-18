# Exact final source binding, 2026-11-16 22:38 UTC

Coordinator released the final-context hold at 22:35 and acknowledged the kiosk's
explicit footprint metadata at 22:36. The source PNGs, source tests, coordinator
reviews and frozen Swift fixture were not edited by this worker. No native command,
commit or push was executed.

## Delivered inputs

- Recommendations: `../recommendations.json`, SHA256 `3e2148f11a525a3ba2b073ebd124726b63210cdb935a0dfb01c033ad657190f7`.
- Native input: `native-inputs-v7/native-inputs.json`, SHA256 `c9fe0a3b85f7845b50836dc0282bbbec392a52a6384a79ee09f5d6637297ac85`.
- All nine prepared PNGs match the exact source hashes, including the unchanged four v6 candidate sources.
- Frozen fixture SHA remains `92cf6adf3ebee3ddd970cda799b19fcffee190c1b5fd998f02f176f4dd403e01` and matches coordinator's `build-source-2227.sha256`.

Exact new image bindings:

| Role | SHA256 |
| --- | --- |
| kiosk | `c411e33b79e0ffc5b0eb86143cd8785a564e573b5819bc1d4c399ef5d3b60264` |
| context-01 | `edf9d79bb71337eb908ab654a11e6011e8b69354101f30dab2dffbd401073482` |
| context-02 | `d1ed85e7a64965c9063db1533672ef07d8b4e9c81588f5c11f9a711f57a75355` |
| context-04 | `26640bb8c2c92e08679643e028346f5c926a5d2fbd021f5996b03d6081a42948` |
| context-05 | `4cb22248df71f1a3ff956c52ab76bdcc3a8aac01ce598e13097db52b9615a204` |

Kiosk has 29 bound dependency records. Each context source has 39, including every
manifest-declared input/output, `author.py`, final `replay.py`, `test_context.py`,
`repair_roof_density.py` and the retained `attempt-01/geometry.json` that the repair
reads. Both review documents are separately SHA-bound recommendation evidence.

The exact approved mapping command executed successfully at 22:37:

```sh
python3 docs/review/building-perspective-detail-20261116/build_recommendations.py --kiosk-review-sha256 5e83d9f73e42f97bde6c275ee2b0579832d3b547f148dbd6861f5d7b1c0f04c7 --kiosk-manifest-sha256 48a2728f50ba07edc674c46bdc63fb7743062063bb1177d2fa92b6e842b5883f --context-review-sha256 b3fe6119e73d07148a9dd2d97de2f6a28d5a50c6c2e03f84be72dc4fe5c9d34a --context-manifest-sha256 5ac5fd81fd591bce2fb6ae61db82b7e7a34444707266d7ed04d0621b40116468
python3 docs/review/building-perspective-detail-20261116/scene/native.py bind --recommendations docs/review/building-perspective-detail-20261116/recommendations.json
python3 docs/review/building-perspective-detail-20261116/scene/native.py prepare
```

Do not rerun into existing destinations. The script deliberately refuses overwrites.
Logs are `recommendations-2237.log`, `bind-2237.log`, and `prepare-2237.log`.
The exact coordinator native run command and build-setting string are in
`RUN-NATIVE.md`; no additional runtime environment variables are needed.

## Validation and preserved failure

First mapping attempt failed before writing output, retained as
`recommendations-2236.log`. The independent projection oracle returns a tuple, but
the recursive close-vector helper expects a list. Corrected only the adapter to
`list(a.project(...))`, preserving all geometry, .002 tolerance, sources and Swift.
No test assertion was weakened, and no source was changed to match the validator.

After correction:

- Seven read-only mapper preflight checks passed, including stale implementation,
  omitted repair dependency, first-sample manifest and wrong explicit approval hash
  rejection. See `mapping-preflight-2236.log`.
- Actual five-source validation passed all four ground corners each. Twenty individual
  +1-pixel corner mutations and five forged dependency hashes were rejected: 30
  positive/mutation checks total. See `binding-verification-2237.log`.
- Current expected preparation exactly equals retained native-inputs JSON, and all nine
  prepared image SHA256 values match their sources.
- Full existing portable suite: **41 passed in 33.445 seconds**. See
  `portable-tests-2237.log`.

These are preparation/portable checks, not a native capture or owner acceptance.
The initial context correction failure remains preserved by coordinator under context;
only the actually rebuilt and subsequently reviewed final bytes are bound here.
