# Final bounded V8 scene review

November 16, 2026, 23:29 UTC. BP-001/007/012, T1045.

**Ground/base/prop consistency is improved in the retained ordinary views. Overall benchmark NOT MET. This is a comparison for owner review, not acceptance or a claim that all footprints are now coherent. No further aesthetic attempt is authorized.**

## Actual evidence

The selected native retry `ss-footprint-ground-v8-2321.xcresult` passed exactly one test, zero failures, producing six captures and eighteen images. The strict importer exported nineteen attachments and passed at23:25. Independent `scene/retained.py` rehashed the actual fresh-built executable and verified all retained contracts plus nine complete baseline RGBA comparisons against immutable V7 candidate images.

Loaded and independently rehashed build SHA256: `7b4efe2e482d3707e8d08aff5bd4406d3ccdedb26467919ce7b5b2fc3545500d`. Frozen Swift: `3ab178cdbc141f51e3ee0ccfd5e30b6a2e29e6e562bf8d98ef0fe8cb797dcef5`. Prepared input: `598ec899b0171b9cf6ca32366a15053ad4666d15e8ebad7e0d792fea3c95bdbf`. See `native-run-2321.log`, `native-import-2325.log`, `retained-2325.log` and `scene/native-capture-v8/verification.json`.

Actual Brave verified72 control selections/96 image displays over V7/V8, all three zooms, baseline/candidate/paired, native/half and grayscale states. Exact logical sizes704x326 and352x163, reference grayscale restoration and no page overflow were checked. `browser-check-2328.json` retains the results and initial automation failures. Node harness checks are separately synthetic UI checks over real retained bytes, not browser evidence.

## Ordinary-view findings

Coordinator directly inspected actual baseline and candidate PNGs at1,1.25 and1.4, candidate half-size overviews, and the original uncropped benchmark.

- At1, the connected sidewalk now visibly continues around the kiosk and along the rear facade rather than leaving those buildings over the old road patch. The tree grate is on the sidewalk, separated from the rear building base rather than appearing attached to its facade. The right-hand dais has a surrounding foundation/sidewalk treatment. These are bounded improvements in this crop, not proof about offcrop buildings.
- At1.25, the tree and newsbox base regions remain on compatible paving. The larger continuous sidewalk removes the old abrupt road crossing behind Player. Actor roots for Camera and Player are preserved, so this is not a framing or visibility trick.
- At1.4, the kiosk steps, chamfer and planar foundation infill are clearly distinguishable, but the mineral patch at the front still looks like walkable paving. It does not adequately communicate that the chamfer-omitted portion of the authoritative rectangle remains blocked. Passing material coverage and registered contact tests does not settle this visual/affordance problem.
- The new curb is an angular, thin planar boundary, not the benchmark's visibly raised rounded curb. Sidewalk slabs remain conspicuously regular and weathering understated. The road and crossing are simplified and cleaner than the reference. The overall broad apron and road composition still differ substantially.
- Building masses dominate the scene, with repetitive facade/roof treatments. Player retains a stationary frontal stance and weak grounded walking silhouette compared with the benchmark. Camera remains close against the kiosk rather than the reference's open placement. These preserved limitations are not repaired by this ground pass.

## What the checks establish, and what they do not

All24 solids,18 uprights, Camera/Player roots and authoritative fields, view center[684,724], production HUD/controls, all nine old source images and five building registrations remain fixed. Only reviewed ground presentation and plan-authorized decorative prop positions differ. Baseline images match V7 exactly. Conservative prop base-region checks cover124200source samples outside solids on sidewalk. Actual contact geometry is known for the five mesh sources whose canvases can intersect the crop. Nine legacy raster contacts remain unknown/offcrop, not certified.

First flat source rejection, one permitted material correction, and native2317 failure are preserved. Issue253 corrects only an impossible Double-exact check of SpriteKit's float-backed depth storage, without tolerance weakening. The actual retry is separate evidence and does not erase that failure. See `NATIVE-ORACLE-253.md`.

Independent local suites passed59scene and10audit tests after the oracle correction. Earlier exact final plan suite passed27tests and focused Swift suite16tests. Both gallery suites subsequently passed with `--require-v8`. Tracked-export validation and publication are recorded separately, not inferred here. No new unfiltered Swift run or automated CI polling chain was performed.

## Stop and handoff

Publish this bounded final comparison and request owner scene review. Do not start another aesthetic correction, change the authoritative footprint to match art, expand motion/encounters, admit production art, merge, close issues or claim physical-device certification. Technical verification does not grant owner acceptance. The benchmark remains NOT MET.
