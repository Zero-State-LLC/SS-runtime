# BP-002 contact-pose fit

Status: SINGLE PAINTED KEY STUDY; not an admitted animation or full source master.

The prior lower-leg block was a geometry experiment, not benchmark art. This study fits hip lateral spacing and hip projection approximately to the retained painted source, separates ankle spacing from hip spacing and uses a 3D two-segment chain with a forward pole. The proposed chain was reauthored from 25.5 to 27 units after the raised hip made a landing unreachable. No solver stretch was enabled. parameters.json records these authored choices; they are not anatomical measurements inferred from the neutral raster.

Existing SS-specs 492d921 BP-002/BP-008 and controlled-character-source.md authorize source geometry and attachment alternatives while keeping world-travel, four-facing and complete-family review open. No new gameplay or art-admission policy was needed. The Animation Mentor run-cycle research cited in the preceding study motivates blocked support/flight keys, not these dimensions or projection values.

## Source and review

1. block.py and parameters.json produce the revised candidate geometry, sixteen samples and numerical diagnostics. 1,001 sampled poses remain reachable, segment residual is below 8e-15, sampled heel/toe clearance is nonnegative, and nominal continuous support contact closes. The held-frame drift finding remains 7.44 units; this is not actual renderer evidence.
2. make-guide.py places the original costume beside the contact guide. Screen annotations are approximate. The planted right leg is image-left; the recovered left leg is image-right.
3. Built-in imagegen made painted-contact-source.png from the neutral and guide using prompt.txt. The result retained the costume identity better than isolated boot variants, but the recovered ankle was visibly below its knee rather than folded behind it.
4. A single local correction, recorded in recovery-correction-prompt.txt, produced recovery-corrected-source.png. Visually, the raised boot now sits partly behind its knee/thigh and the two legs have distinct depth treatment. This is improved pose readability, not proof of a correct hidden foot model.
5. assemble.py registers the correction uniformly using two approximate hood/belt landmarks, extracts only the lower-body region and assembles it beneath the original body layers. contact-extraction.json preserves the polygon and transform. The complete original RGBA region above row199 is copied exactly; the original coat and arms also draw above the imported legs below that row. This avoids admitting generated upper-body texture changes. body-source/ and body-rig.json retain the editable original component layers. The imported leg patch is one painted key, not a fully weighted mesh or reusable locomotion rig.

## Limits and next work

The corrected pose remains shorter in its forward leg than the projected guide, and the hidden ankle/heel cannot be located reliably from visible pixels alone. Do not stretch the replacement to conceal this mismatch, label it a measured contact pose, or build sixteen independently generated images around it. Reconcile the authored model with reviewed painted proportions and explicit hidden surfaces, then build the support, push-off and opposite-step keys from that source. The current upper body is neutral; arm/torso counter-motion is not yet authored.

comparison.png shows the original neutral, registered generated correction and retained-body assembly. The assembly was visually inspected. Its lower-body fold is a useful source direction, but no full cycle, complete facing, actual world displacement, runtime visual or device acceptance follows. The 384x416 working canvas permits the forward foot; it is not a change to production canvas, logical size or anchor.

## Reproduction and provenance

Python3 + Pillow: run block.py, make-guide.py and assemble.py. The first script validates source geometry; assemble.py verifies exact original upper-region RGBA preservation. This is offline source production, not executable game code. The prior 773-test core result remains the latest; no new runtime test claim is made for this art-only study. sha256.json records files; source.zip contains the editable study and raw images. No active texture, clip, catalog, spec pin, collision, controller or gameplay changes were made.
