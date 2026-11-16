# Scene QA: footprint occlusion, Player halo and finite ground overlay

Owner authorized QA/diagnose/fix at2026-11-16T20:45:59.264Z. Actual final v4 evidence at eb67469 is technically valid and exact-head CI43852421883 has five successful jobs, but its final visual verdict remains NOT MET.

## Reproduced defects

`python3 -B docs/review/scene-qa-repair-20261116/qa.py` exits1 on retained native-capture-1040. After correcting the probe to avoid applying zoom twice to already-projected root coordinates, registered Camera silhouette coverage by stone is84.5%,84.1%,84.0%; captured Player exterior pale-pixel ratios are88.4%,86.8%,90.7% across zoom1/1.25/1.4. Initial and corrected probe outputs are retained separately. Coverage is a registered silhouette diagnostic, not an independent rendered-ID pass. The halo test samples actual captured image pixels.

Three ranked hypotheses and tests:

1. Root-only order ignores solid extent: Camera[496,672] is outside the kiosk's minX512 wall plane, but its projected root sum1168 sorts behind kiosk root sum1152. A footprint separation constraint must put the building before the near-side Camera without changing either world root or source registration. Behind-wall controls must remain behind.
2. Player source replacement retains a separate `faction-outline` node. Disable only that test-only border and move the existing soft ground shadow from its default radius offset to the explicit registered foot root. Actual captured exterior pixels should lose the halo; shadow root must match Player root.
3. Candidate uses a finite576x576 ground picture at[448,384] over contrasting runtime ground. Extend the same authored corner/material into a full-world ground treatment rather than tile or stretch the entire curb motif. Preserve original world feature registration and all gameplay solids/fields.

New review-only fixture/inputs/captures will retain full authoritative24-solid geometry, all environment uprights, HUD/controls, immutable old packets, exact executable provenance and strict importer checks. No source redraw, collision/field migration, arbitrary visibility Z boost, hidden environment, production admission, merge, physical certification, animation/encounter expansion or acceptance is inferred. This is separate from #248 insertion-order correction and #241 stale binary provenance.
