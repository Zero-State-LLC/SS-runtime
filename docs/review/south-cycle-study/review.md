# South movement study — FAILED, not admitted

Built-in image generation produced an initial 4×4 sheet and one targeted gait-order correction from the registered hooded-player south candidate. Both original PNGs and exact prompts are preserved. No shipping assets, catalog entries or animation metadata changed.

Visual review of the corrected sheet: frames 1–2 have a screen-left leading boot, frames 3–4 switch to screen-right although the requested passing transition is later; frame 8 returns to screen-left before frame 9 returns right. Similar switches recur in frames 10–12 and 13–16. Passing poses are not clearly established. Arms and coat contours change without a coherent mechanical progression. A stable-looking costume and sixteen different images do not establish sixteen usable animation poses.

The diagnostic export uses proportional 4×4 cell boundaries (the generated sheet is 1254×1254, not an exact multiple of four), one common 224×224 resampling and a fixed placement on 256×256 canvases. Individual poses were not resized to hide drift. These are diagnostic frames, not validated ground-anchor registrations. Source hashes and frame hashes are in exports.json. The quarter-speed WebP uses 125ms holds. The HTML viewer uses a 31.25ms normal frame interval (16 poses over 0.5 seconds), quarter-speed and frame stepping; it is not the runtime renderer and cannot establish foot slide against world travel.

Next production action: establish and review contact, down, passing and up key poses for both steps with explicit anatomical landmarks; construct in-betweens from those constraints. Do not repeat unconstrained 16-frame generation or promote this sheet merely because all cells differ. The timing foundation remains useful, but art fidelity is still unproven.

Tool: built-in image_gen. No CLI fallback used. Deterministic export follows the user's explicit cleanup/export authorization. Full initial and correction prompts: prompts.json.
