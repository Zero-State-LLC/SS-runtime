# South contact key — lead-leg repair

Status: REVISED SOURCE KEY, not an admitted sprite or completed gait.

Authority: SS-specs d602775, controlled-character-source.md BP-002/BP-008. Those requirements already cover constrained pose correction, hidden surfaces, original costume preservation and source-space versus world-contact evidence. No new gameplay or design policy was required. Runtime parent 0cc0793.

## What changed

Built-in image_gen edited the previous retained-body contact key using the existing authored pose guide. The exact prompt is in prompt.txt; source.png is the unmodified output. The forward anatomical right leg (image left) previously ended above the proposed contact point. The correction extends the lower chain and revises its painted folds/boot while keeping the same costume direction. It does not generate sixteen independent poses.

assemble.py applies one uniform registration using approximate hood-tip/belt landmarks, extracts the lead-leg polygon, retains the previous opposite leg and redraws original body/coat/arm layers over it. The complete original RGBA region above row 199 is copied exactly and checked byte-for-byte. No nonuniform stretch or alpha cleanup is used. registration.json records source/target points, transform, extraction polygon and approximate visible landmarks. baseline/ contains all inputs required to reproduce the assembly without another folder or image-generation call.

## Review

The lead knee and toe extend lower than in the previous key and better approach the existing pose guide. Approximate registered knee is (173.99,275.72) versus guide (172.31,280.24); toe is (169.17,378.62) versus guide (162,381). These are manual visible-feature annotations, not measured hidden anatomy, solver residuals, or an acceptance tolerance. The outline and boot material still require consistency review with other keys.

The recovery ankle/heel remain concealed. This key cannot establish their shape or contact model, and does not prove a coherent full-body gait. Upper body remains neutral; arm/torso counter-motion is not authored. Next: author the concealed recovery surfaces and validate their attachment before support/push-off/opposite-step keys. Do not expand this patch into sixteen duplicated or independently generated poses. Retain actual world-travel, four-facing, full-source, renderer and device gates.

## Reproduction and verification

Python 3 + Pillow: `python3 assemble.py`. It writes registered source, isolated lead leg, assembled lower body, retained-body key, comparison and verification.json. Source hashes are recorded in sha256.json. The source archive contains editable masks/parameters and original component PNGs; this is still a partial painted source, not a complete rig.

Verification passed: deterministic assembly and exact original upper-region preservation. No runtime code, active textures, metadata, spec pins or gameplay changed in this turn. The preceding simulator/core results are not art validation and are not claimed as newly run here. Physical-device testing remains deferred.
