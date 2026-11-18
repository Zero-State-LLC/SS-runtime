# Actual coordinator encounter0649 import

**SUPERSEDED: passing-but-inadequate stale-framing attempt, runtime#240. This is NOT visible encounter evidence.** Coordinator image review found tick459 shows the initial camera area without Player or nearby enemies. Global counts and native success were insufficient. All original exports and executed source are retained under `attempts/01-stale-framing/`; the text below describes the historical import, not current acceptance. Corrected schema v2 rejects this attempt.

Worker independently validated the exported native result and attachments at November16 06:53UTC. Both `verify_capture.py` and `build_gallery.py` exited0. No simulator was run by this worker and Swift remained frozen.

- Native result: `/Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-20261116-0649.xcresult`
- Exact exports: `/Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-exports-20261116-0649`
- Gallery: `/Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-gallery-20261116-0649.html`
- Gallery bytes24953931, SHA256 `bfbc352a14a8eaf3fc5dc521b0b17f7ce929499a8155eaaba984ecce0640f9bc`.
- Ledger attachment `2D44A176-F3FF-4831-9148-E1943C8A5D3C.json`, SHA256 `1f99da97c2504d1a94600187dee5fefb1768daf534622553921ba26b6c29c87d`.
- Legal commands attachment `A71855F0-4B65-4B13-AC63-5014CB3DEE3A.json`, SHA256 `6a48e2369cf58ed9154208d11c379dbb556d95519d07fe00e6a3b0cbe3905297`.
- Terminal tick6000, scenarioSeeded false, final/replay digest `a4cb58875ae9707408c2cd55f64e4f92c4b285f44e69abe7915a54100ca395fe`.
- Validator status `STATIC_EXISTING_ART_NOT_ACCEPTANCE`, nine captures and1073 resource hashes verified against source bytes.

| Actual tick | New observed tags |
| --- | --- |
| 1 | camera-integrity-3 |
| 57 | camera-integrity-2 |
| 120 | fieldOcclusion |
| 161 | entityDied |
| 321 | camera-integrity-1 |
| 459 | dense |
| 844 | camera-integrity-0, cameraDestroyed |
| 2224 | hostile |
| 3625 | mines |

All imported PNGs are1408×652 pixels. Gallery displays the actual704×326 logical scene and352×163 half logical size. No invented captures or pixel resampling files were created. Exact original PNG bytes are embedded unchanged.

Not observed: playerDamaged and telegraphs. This is the existing-art production-projection static control, NOT a coherent benchmark. Source fidelity remains BLOCKED. Owner acceptance and production admission remain NOT_GRANTED. Actual gallery visual review belongs to coordinator and is not asserted here. Complete attack animation, live cadence and sprite-ordering coverage remain unsupported.

Reproduction, preserving existing output:

```sh
python3 docs/review/existing-art-encounters-20261116/verify_capture.py \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-exports-20261116-0649 \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-20261116-0649.xcresult
# Use a fresh output path. The builder refuses to overwrite the retained gallery.
python3 docs/review/existing-art-encounters-20261116/build_gallery.py \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-exports-20261116-0649 \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-20261116-0649.xcresult \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-gallery-20261116-0649-reexport.html
```
