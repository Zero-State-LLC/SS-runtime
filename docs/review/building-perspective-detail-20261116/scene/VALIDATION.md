# Worker validation, 2026-11-16 22:28 UTC

Owned changes only: `AppTests/BuildingPerspectiveSceneTests.swift` and this `scene/` directory.
Prior packets, production, project files, CI, gallery and handoff files were not edited.
No commit, push, native build, simulator execution or source recommendation by this worker.

- `python3 -m unittest discover -s docs/review/building-perspective-detail-20261116/scene -p 'test_*.py' -v`: **41 passed**, 31.339 seconds. Full raw output: `portable-tests-2227.log`.
- `swiftc -frontend -parse -D DEBUG -D SS_SOURCE_SCENE_REVIEW -D SS_BUILDING_PERSPECTIVE_REVIEW AppTests/BuildingPerspectiveSceneTests.swift`: exit 0 at 22:28 UTC. Syntax only, not native typechecking/execution.
- Frozen Swift SHA256: `92cf6adf3ebee3ddd970cda799b19fcffee190c1b5fd998f02f176f4dd403e01`.
- New fixture condition: `DEBUG && SS_SOURCE_SCENE_REVIEW && SS_BUILDING_PERSPECTIVE_REVIEW`.
- Exact selected native test: `SSRuntimeTests/BuildingPerspectiveSceneTests/testQuietSouthNeutralOrdinaryScene`.
- Immutable v6 native record and its assembly/preparation transitive SHA checks pass in every positive synthetic validation.
- Thirteen original runtime building PNGs were byte-compared against committed `HEAD` before pinning their SHA256 values. No old v6 source-hash measurement is claimed.
- Four turtle context registrations were read independently, projected from their authored ground landmarks, and matched D108 with maximum absolute error `4.263256414560601e-14` logical world-draw units. This is geometry validation, not visual recommendation.

Portable tests include complete importer/retained integration using mocked xcresult
commands, temporary synthetic images and deliberately fake executable bytes. They are
not actual native evidence and leave no native capture/preparation in this packet.
Both historical v6 retained evidence and copied v6 records are rejected as v7 inputs.

## Coordination and remaining gate

Coordinator was notified of the exact guard/ID and froze Swift before its 22:27 build.
No Swift edits occurred after 22:26:52. Coordinator owns native execution and visual
review. `README.md` contains bind/prepare/import/retained commands and schemas.

Source-schema mapping for coordinator, without authoring any recommendation:

```python
registration = {key: author_row[key] for key in
                ('canvasPixels', 'rootPixelsTopLeft', 'worldPosition', 'drawSizeWorld')}
# context/registration.json, each row:
groundPixelsTopLeft = [v['sourcePixelsTopLeft'] for v in author_row['geometryLandmarks']]
# Require names footprint-0, footprint-1, footprint-2, footprint-3 in that order.
# kiosk/output/registration.json:
# Use author's explicit groundPixelsTopLeft, requested from whale, not guessed alpha bounds.
```

At this checkpoint source final recommendations are absent and no `assembly.json`,
`native-inputs-v7` or native capture was created here. Binder deliberately fails closed.
Whale was asked to provide explicit four authoritative ground-corner pixels and label
any virtual chamfer corners honestly. Turtle's current registration schema matches.

Escalated inherited coverage gap to coordinator for a defect issue: v5/v6 retained
verifier hashes but does not validate export-manifest test/attachment identities.
V7 independently rejects empty, duplicate and old-test manifests even after rehashing.
No historical verifier or packet was changed, and its valid actual manifest was not
reclassified as bad evidence.
