# Municipal camera shared source — BP-004

This source repair addresses the previously measured changing pole/base across four settled-state images. It implements the existing BP-004 fixed-mount requirement at SS-specs 521aec30cbb926938591d1ffb22233b24102732c; no new design or gameplay policy is introduced.

The original intact image supplies one permanent mount, pole and base. An explicitly authored polygon separates the changing dome. Four independently editable dome layers compose over that shared structure. No image generation, warping, new material or inferred collision geometry was used. Original input PNGs are retained under source/; build.py reproduces all layers and exports with Python 3 and Pillow.

Verification: every RGBA pixel outside the dome mask matches the intact original in every state (zero differing pixels). The reconstructed intact image matches the original byte-for-byte in decoded RGBA. All four images retain the 256×384 texture canvas, 64×96 logical canvas and (32,88) logical ground anchor. source-record.json records mask vertices, input/output hashes and bounds. The polygon is an authored visual layer boundary, not an anatomical measurement or simulation geometry.

Visual review: comparison.png shows all four states at source size and 64×96 logical size. The permanent structure remains stable and destroyed dome remains dark; dome damage remains separate from the permanent suspension arm. The damage notches remain runtime overlays and are intentionally not baked into these sources.

Scope: review source only. The active assets and test-bundle assets are unchanged. These four settled states are not the required six animation clips or sixteen delivery slots. Operational, hit, critical-entry, destruction, field-off and destroyed-idle timing, interruption, Reduced Motion and legal encounter captures remain required. No runtime or device acceptance is claimed. Character animation, environment projection and player outline work remain open.

Run `python3 build.py` from any directory to reproduce. No new app/core test result is claimed for this offline art-only change; the preceding full app run passed 100 simulator test executions.
