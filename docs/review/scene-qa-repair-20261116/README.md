# Bounded scene QA repair, November 16, 2026

Review only. No production admission, owner acceptance, merge, motion/encounter expansion or physical-device certification.

## Evidence and result

The new v5 fixture fixes three diagnosed presentation defects without changing authoritative actor roots, solid geometry or fields:

- Geometry-backed footprint ordering puts the near-side Camera in front of the kiosk. It retains behind-wall cases and fails closed on cyclic ordering constraints.
- The candidate Player no longer inherits the separate pale faction outline. Its existing shadow is registered at the Player foot root rather than the old offset.
- The authored paving/road context extends over the complete arena. Original corner pixels and world feature locations remain exact, avoiding the old finite patch material boundary.

`native-capture-v5/` is the real 21:00 UTC focused native result: one test, six captures, eighteen images. At 21:12 UTC, the coordinator independently reverified every retained file and source binding, then compared the still-current built test executable SHA256 with the captured/imported binary hash: `7a31efe5dbee7230bfe6651829289a190b22feee76609401879496f0c606502f`. This comparison occurred before any v6 rebuild. See `coordinator-retained-2112.log`.

Actual captured-pixel probes pass at zoom 1, 1.25 and 1.4: no sampled pale Player exterior pixels, zero registered Camera silhouette covered by the kiosk, and Camera core matching ratios approximately 94.5%, 90.3%, 76.3%. Those measurements are diagnostic thresholds, not proof of fidelity or unobstructed controls. The lower zoom-1.4 score helped expose the remaining visible movement-stick overlap.

**Actual image verdict: improved, overall benchmark NOT MET.** The Camera is visible, the pale Player halo is gone and the broad paving material boundary is removed. The Camera intersects the fixed movement control at the highest zoom. Building roof/crop, source fidelity, painted lighting, Player proportion/contact fidelity, pavement repetition and scene composition remain limited. The separately bounded v6 framing follow-through addresses control overlap only. It must not change actor placement, move controls or masquerade as dynamic camera-follow evidence.

## Reproduce portable checks

From the repository root with Python 3 and Pillow:

```sh
python3 -B -W error::ResourceWarning -m unittest discover -s docs/review/scene-qa-repair-20261116 -p 'test_*.py'
python3 -B -W error::ResourceWarning docs/review/scene-qa-repair-20261116/ground/test_ground.py
python3 -B docs/review/scene-qa-repair-20261116/retained.py docs/review/scene-qa-repair-20261116/native-capture-v5
python3 -B docs/review/scene-qa-repair-20261116/qa.py --capture docs/review/scene-qa-repair-20261116/native-capture-v5 --prepared docs/review/scene-qa-repair-20261116/native-inputs-v5
node docs/review/scene-qa-repair-20261116/gallery/test_evidence.js
```

With local Swift/Xcode available, the narrowly compiled depth helper has its own suite, not a full Swift package run:

```sh
python3 -B docs/review/scene-qa-repair-20261116/depth/test_depth.py
```

`coordinator-tests-2112.log` preserves 41 QA, 13 compiled depth and 9 ground checks. All 75 prior scene regressions also passed. A staged-only clean export passed all 41 QA checks. Its first retained-evidence invocation correctly rejected absent Git tracking, because environment variables alone do not establish the required `.git` or exported tracking receipt. Initializing and indexing the actual clean export fixed that setup error without changing the validator or copied inputs. Retained evidence and gallery checks then passed at 21:19 UTC. Both outputs are preserved in `clean-export-2117-missing-tracking.log` and `clean-export-2119-pass.log`.

Earlier red probes, implementation failures and all prior native packets remain intact. `retained.py` verifies preserved evidence but explicitly does not claim a new native execution or a current installed-binary comparison.

Serve `docs/review` over localhost and open `scene-qa-repair-20261116/gallery/`. Each capture version is explicit and must validate its records and all eighteen image hashes. Missing or invalid packets never fall back to a different version.
