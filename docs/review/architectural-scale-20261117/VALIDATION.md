# Validation and evidence limits

Status at November17,2026 01:40UTC: **local review-packet validation complete, owner review required**. This is not aesthetic acceptance, native evidence or a remote-CI receipt.

## Executed checks

- `python3 docs/review/architectural-scale-20261117/test_audit.py`:8tests passed, raw `audit-tests-0121.log`.
- `python3 docs/review/architectural-scale-20261117/audit.py check`:11432prior tracked files verified byte-for-byte at initial checkpoint.
- `swift test --filter 'CameraMountSolidTests|CameraHousingArtTests|EnvironmentContractTests'`:8Swift Testing tests in3suites passed, raw `swift-focused-0124.log`. The XCTest preamble reports0because these suites use Swift Testing. No unfiltered suite or native simulator run was performed.
- Initial source tests passed12checks but failed to catch ground-UV and explicit-normal adapter defects found through actual image inspection. Issue255 remains open. `REVIEW-FIRST.md` and `REVIEW-SECOND.md` document the observations and narrow repairs. Passing that initial suite is not final validation.

## Final observed validation

- Coordinator independently ran18source tests successfully in `coordinator-source-tests-0137.log`, including unchanged XY/contact geometry, nonuniform Z maps, all71depth items, identical Player/Camera layers, independent square-ground UV witnesses, explicit normals for every context face, actual roof-interior pixels across all five meshes, exact source-layer recomposition, preserved failed artifacts and independent dimension/massing formulas.
- `gallery-tests-0133.log`:7tests passed for all8image references, all4document links, exact six-view census,2112x978scene frames, full original benchmark, and explicit source-proxy notices.
- `tracked-export-0138.log`: fresh staged-only export11618files, all5commands passed. These include33portable tests (8audit+18source+7gallery),11432prior protected-file hashes, and a complete renderer replay. **All47replayed files, including the manifest, are byte-identical**. Export excludes unpublished sibling packets. Only publication/validation documentation was subsequently updated, not the validated renderer, geometry, images, gallery or tests.
- Final source manifest SHA256: `cfa00dd646449a95a20153626c453e005e43de4c2db548c6a1ae6f7066f5a629`. Coordinator inspected all3actual comparison sheets, exact hashes in `REVIEW.md`.
- Actual Brave at01:35:34UTC loaded all8images, fetched all6source images matching final manifest hashes, served all4document links withHTTP200, and had no horizontal overflow. All source scenes displayed at542x250.9765625CSS with exact2112x978natural dimensions, original benchmark1672x941withcontain. See `browser-check-0135.json`. Actual screenshot was inspected through the browser tool but its temporary image path was not available for filesystem retention. No saved screenshot file is claimed.
- Jev401 required direct browser fallback. A no-return eval yieldedundefined. Async image decode stalled while the tab was hidden, then a completed-image/no-store-fetch check succeeded after selecting the tab. These are browser verification limitations, not changed visual evidence.
- The first final-normal roof probe incorrectly sampled a pixel occluded by the proposed dais rail. Its red test/log are retained in `source/probe-failure/` and `source/tests-final.log`. Analytic ray-plane intersection confirms the old pixel must remain cornice. The corrected test checks both that occluded pixel and an independently clear roof pixel. No renderer or image bytes changed to force green. `source/TECHNICAL-CORRECTION.md` gives the derivation; issue255 remains open.
- `trail-build-0138.log`, `trail-check-final.log` and `TRAIL-CHECK.md` record graph refresh and scoped lexical review. Final check reported0conflicts/20warnings but only inspected first400KB. Raw failure logs remain unedited.

The export job's no-output watchdog fired because all progress was redirected to its retained log. Inspection showed active98%CPU renderer and advancing output. It completed successfully after91.5seconds, without cancellation or retry.

## Unchanged gates

This remains one aesthetic proposal with technical renderer repairs, not multiple aesthetic alternatives. Current/proposed source geometry and dimension records must remain identical across preserved technical attempts. Native rendering, material fidelity, owner acceptance, production admission, merge, issue closure, motion/encounter and physical-device certification are not established by these checks. Remote CI is not inferred passing from local tests.
