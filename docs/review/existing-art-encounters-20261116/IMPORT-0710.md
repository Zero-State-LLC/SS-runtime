# Actual corrected capture0710

## Independently verified import

At November16 07:14UTC worker independently ran the unchanged schema v2 validator against exact coordinator xcresult and exports. Exit0: `STATIC_EXISTING_ART_NOT_ACCEPTANCE`, nine captures and1073 resources. The gallery builder revalidated native identity and complete packet before rendering. No worker native execution, source edits or commits occurred.

- Result: `/Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-20261116-0710.xcresult`
- Original exports: `/Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-exports-20261116-0710`
- Retained exports: `capture-0710/exports/`, all12 files byte-compared identical to original.
- Gallery: `capture-0710/gallery.html`,20210882bytes, SHA256 `4e2616e7c70fbe77c9647d3e1e9048a51bf554a0e87f63d8cf28535bfad603d6`.
- Ledger: `A8A1760A-932F-41E1-947E-99D4EF362D4F.json`, SHA256 `ad12b9f106ba9201cb040437fbc0e89f1d36a46dc7d438574b97460ed72db69e`.
- Final/replay digest at6000: `a4cb58875ae9707408c2cd55f64e4f92c4b285f44e69abe7915a54100ca395fe`.

Dense tick459 PNG is `exports/285884EB-20CF-44E0-BB2A-8AD5A7E1B872.png`. Its actual measured included scene nodes are Player, nearby enemies10/12 and projectile27. Schema v2 independently checks their roots and accumulated bounds against the actual Player-centered crop. This is staged snapshot camera framing, NOT live follow. Node inclusion still does not independently establish unobscured pixels or artistic quality. Coordinator owns browser/image review and publication.

Observed global state tags: Camera integrity0/1/2/3, cameraDestroyed, dense, entityDied, fieldOcclusion, hostile and mines. Not observed: playerDamaged and telegraphs. Global Camera/mines tags are not a claim that every corresponding object is visible in its plate.

## Actual loaded-runner provenance

`native.log` is the exact original coordinator xcodebuild log, SHA256 `ac4756455731a0a27d2fc692fcdd2d155d8dd1499aa9983ef17b7b13b98b9803`. It records the focused native test passing71.885seconds with one test and zero failures. `native-summary.json` and `native-tests.json` were fetched directly from the exact xcresult and retained for portable identity checks.

`runner-diagnostics/` retains all four exported diagnostics files byte-identically. The actual session log line149 records loading:

```
/Users/appliedalchemylabs/Library/Developer/CoreSimulator/Devices/84297C74-033E-408F-9622-D36BFF32F74E/data/Containers/Bundle/Application/5CF8FE91-EF42-44C2-9C5B-EDB5A248CF8E/SSRuntime.app/PlugIns/SSRuntimeTests.xctest/
```

Worker independently hashed `SSRuntimeTests` at that exact loaded path at07:15UTC: `cb8a0f252bb2bb46bca16c808eba373569f31fcfe1d4640bef487016c91e5504`, matching the coordinator's compiled v2 hash. Actual session log SHA256 `4be6dba376c703984f804711dd4867e0fd53737b1477702463af956f3e1ec87a`. This binds the run to the corrected container, unlike rejected0701. See untouched coordinator `attempts/02-0701-old-schema/LOADED-BUNDLE-DIAGNOSIS.md` for older relocated-bundle evidence and its mechanism limits.

## Portable proof and limits

At07:15UTC28 offline tests passed in1.084s. Five new actual0710 regressions validate exact retained native identity/full packet, actual dense-node census, stale/hidden framing mutations, byte-exact gallery reproduction/scope disclosure and actual runner loaded-container identity. `git diff --check` passed. Swift remained SHA256 `30def02cb69cd49acf7a990ac742bd72fce525bca748999ec465df513b09a5fc`.

Both previous attempts remain untouched. runtime#240 remains open for coordinator review. Source fidelity BLOCKED, owner acceptance and production admission NOT_GRANTED. This is production-projection existing-art staged control, NOT coherent benchmark acceptance, live-follow validation or complete attack animation evidence.

```sh
python3 docs/review/existing-art-encounters-20261116/verify_capture.py \
  docs/review/existing-art-encounters-20261116/capture-0710/exports \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-encounters-20261116-0710.xcresult
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s docs/review/existing-art-encounters-20261116 -p 'test_*.py' -v
```

For reexport, use `build_gallery.py` with these same inputs and a fresh output path. Retained gallery is exclusive-created and must not be overwritten.
