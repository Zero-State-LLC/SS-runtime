# Identity defect: retained source layer versus original frame

Status: **OPEN LOCAL EVIDENCE, NOT A GREEN WAIVER.** Coordinator notified09:37UTC to open a repository defect issue under the escalation contract. This worker has not opened or linked a remote issue and does not claim one exists.

The pilot exactly reproduces the entire tracked baggy target, including its inherited composited upper layer. Exact copied-source hashes pass. A stronger original-neutral-frame identity guard fails honestly. `tests.log` retains the first failure with9passed/1failed. No assertion, fixture, source pixel, pilot pixel or CI was changed to make it green.

## Exact observation

Two coordinates are opaque in the copied upper layer, but alpha254 in the original neutral frame:

| Source x,y | Original neutral RGBA | Copied upper = tracked baggy = pilot RGBA |
| --- | --- | --- |
|125,119|52,43,32,254|53,44,33,255|
|123,124|19,17,21,254|19,17,21,255|

The first strict assertion fails on five channel values across these two pixels. It therefore does not execute the following whole-top equality assertion. The separate diagnostic evaluates that full region: **157pixels above y200 differ from the original frame**. They all already occur in the tracked baggy target, which the pilot reproduces exactly. `identity-diagnostic.json` records every differing coordinate and original/copied/pilot values, not merely the first two.

The earlier baggy source deliberately copied original-frame pixels only where BOTH its assembled upper layer and the original frame were alpha255. Those jointly opaque pixels still match exactly. This documented limitation does not establish unconditional original-frame equality at antialiased edges. The current stricter test exposes the difference without pretending that a UV change caused it.

## Why no automatic correction

Changing the copied upper pixels would violate exact copied-layer preservation and create a second pilot whose full output no longer exactly matches the tracked baggy target. Changing the strict test would conceal the original-frame discrepancy. The first preview has been submitted for coordinator review, so neither action is taken unilaterally. This is a source-authority/identity interpretation to resolve explicitly, not a reason to invent hidden garment paint or adjust knee geometry.

Potential resolution after review: make a new separately identified upper-layer derivative that restores the original-frame edge bytes, with exact provenance and a clearly delimited ownership rule. Retain pilot01 and its red log. Do not modify the original tracked baggy source, weaken the assertion or treat this proposal as already authorized.

No family, scene, animation, acceptance or production readiness follows from the nine other passing checks.
