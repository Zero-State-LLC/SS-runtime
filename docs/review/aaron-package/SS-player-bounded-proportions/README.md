# Bounded proportion candidate

Proposed source revision: thigh/calf 12.5/14.5 at unchanged total reach 27. Unsupported-foot clearance is scaled by 0.5941785113, lowering heel/toe/ankle together without changing pitch. This is fitted to the previous sampled maximum knee height, not an anatomical measurement. Supported targets, hips, source timing, stance width, torso and arm controls are preserved. Calf garment geometry and its UV length normalization follow the revised calf segment.

All 32 sampled leg solves are reachable, preserve both segment lengths and have nonnegative heel/toe clearance; no knee exceeds the hip. Maximum sampled knee height is unchanged at 21.0434778829. Maximum adjacent knee step drops from 5.2889 to 5.0382; right seam increases slightly (0.4031 to 0.4309), left seam decreases (4.2011 to 3.6171). No arbitrary acceptance threshold is inferred from those numbers.

Normal and quarter MP4s each contain 128 frames: eight repetitions of the same 16 source poses, 4 and 16 seconds. These are source previews, not renderer captures. The inspected comparison shows slightly shorter upper thighs and lower recovery feet; cadence, seam, contact and visual acceptance remain open. Prior copied reports describe historical candidates. Relevant outputs: proposal.json, geometry-checks.json, comparison.png, export-checks.json and these freshly generated videos.

No runtime texture or pose metadata has been replaced with this candidate. Next: match a neutral from the same source proportions and inspect transitions; only then replace the isolated renderer fixture and rerun relevant checks. Boot fidelity and other facings/actions remain open.
