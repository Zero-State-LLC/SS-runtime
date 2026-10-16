# Retained rear-boot source reuse and production-route check

Status: source material refinement, not animation/art admission.

Review of BP-002 and the existing SS-painted-character-source artifact confirmed that four distinct neutral drawings already exist. The record explicitly describes them as a source study, not the editable layered master. Its north-facing image contains usable rear boot paint. The previous plain rear material was therefore unnecessary for this source comparison.

The new material recipe samples the retained north-facing source using its existing uniform registration (312/459, root 462,971 to 192,336). Back-facing boot/shaft surfaces select that source; the forward tongue and toe retain their respective front-source mappings. Rear-view contact renders were inspected and now show heel/cuff/sole detail without assigning the front lace patch there. Material placement is authored against the proposed geometry; cross-view projection and dimensions are not calibrated by the generated drawing. Side transitions between source views remain rough and require refinement.

BP-002 remains the controlling sequence: four neutral facings with one consistent editable master, south movement review against world travel, then other movement facings. The four retained drawings are reference evidence, not completion of that gate. The present south source still needs material, proportion, full-motion and actual-renderer proof. BP-003's other five movement families, BP-004 camera delivery and BP-005 environment obligations are not replaced by this Player work. No benchmark completion claim is made.

Authority: SS-specs d602775 benchmark-production.md and controlled-character-source.md were checked before this source change. They already govern retained source reuse, authored hidden surfaces, distinct facings and staged adoption; no new spec behavior or pin change is needed for this experiment. Runtime code, active art and metadata remain unchanged.

Verification: boot/material.py and assemble.py completed exit 0; 32 material poses/depth arrays and sixteen distinct whole-character source frames. The rear/front contact sheet was inspected. This does not prove all-angle seams, four-facing motion or device performance. Previous clean core run remains 773 tests / 109 suites; no new runtime test was warranted by the material-only change.

Reproduce with Python + NumPy + Pillow: boot/material.py, then assemble.py. Archive includes the original four-facing source as well as the retained front source, exact registration and material recipe, editable body source and outputs. Next source work should use the retained side boot views to resolve the side/rear material transition, while preserving the full production gates above.
