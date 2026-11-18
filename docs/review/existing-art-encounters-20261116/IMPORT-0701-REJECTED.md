# Attempt0701 rejected: old-schema evidence

Subsequent coordinator investigation is preserved untouched in `attempts/02-0701-old-schema/LOADED-BUNDLE-DIAGNOSIS.md`: actual0701 runner logs load an older relocated bundle, not the corrected installed executable. The underlying stale-path retention mechanism remains unproven. Actual corrected0710 is independently validated in `IMPORT-0710.md`. Historical rejection facts below remain unchanged.

At November16 07:03UTC worker ran the current `verify_capture.py` against exact coordinator paths:

```sh
python3 docs/review/existing-art-encounters-20261116/verify_capture.py \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-exports-20261116-0701 \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-20261116-0701.xcresult
```

Result: exit1 `ValueError: Wrong schema`. The native summary/test identity checks completed before this failure, but packet validation did not pass. No corrected gallery was produced.

Exact exported ledger: `6B76E82E-326A-4C0B-AB4B-3DED5D1B5BC3.json`, SHA256 `fa9b33de6b790c63930b7f170f0497734393940f0969ef6afc45bc7fc22d3407`.

It declares `existing-art-encounters-v1`, contains no `framing`, `playerX`, `renderNodes` or `crop` fields, and records first cameraX352. Its capture ticks are1,57,120,161,321,459,844,2224,3625. This cannot establish that the corrected schema v2 staged framing code executed. Current Swift SHA remains `30def02cb69cd49acf7a990ac742bd72fce525bca748999ec465df513b09a5fc` with schema v2.

All12 exported files are retained under `attempts/02-0701-old-schema/exports/` and were byte-compared against the original exact0701 export directory, all identical. Original0649 inadequate framing remains untouched. A portable regression rejects this real0701 ledger and checks every original PNG hash. No schema relaxation or invented success is permitted.

The cause of the source/result discrepancy is **unresolved**. The ledger alone cannot distinguish a stale executable, different build source/project path, export origin mismatch or another build/evidence problem. Coordinator was notified immediately with exact ledger identity. No claim is made about which cause occurred. No native rerun or Swift edits were performed by worker.

runtime#240 remains open. Corrected framing is still awaiting independently validated actual v2 evidence and coordinator visual review. Staged snapshot camera framing is not live follow. Source fidelity, owner acceptance and production admission remain blocked/not granted.
