# Recovery correction propagated through source cycle

Status: source geometry candidate only. No final character animation or runtime resource admitted.

Authority: SS-specs d602775 BP-002/BP-008 and controlled-character-source.md require source key and contact review before complete painted-cycle admission. This follows the authored recovery key from runtime 66cfb07. No design requirement or spec pin changes.

cycle.py applies the authored ankle correction only during swing using a smooth sin-squared envelope, normalized at the authored key. It solves a fixed-length chain with the knee lateral coordinate explicitly between hip and ankle, avoiding an uncontrolled sideways pole projection. The candidate assumes the ankle remains below the hip; it fails if this branch condition or reachability is violated. Both legs share the correction half a cycle apart.

The envelope, knee lateral rule and hidden source landmarks are authored choices for this candidate, not researched anatomical facts or production acceptance criteria. The prior research in controlled-character-source.md supports explicit IK and source-space constraints; it does not prescribe this trajectory. The original painted knee-pad annotation remains approximate.

Sixteen poses sample the existing 0.5-second duration without a duplicate closing pose. Dense inspection uses 1,001 samples. Maximum segment-length error is approximately 7.1e-15 source units, support-toe difference from the prior model approximately 1.8e-15, and the seam and authored-key differences are zero. Heel/toe landmarks stay at or above the authored ground plane. These values verify construction, not anatomical correctness or benchmark fidelity.

The slow comparison GIF uses 125ms per frame for inspection, not the shipping cadence. The sixteen-pose sheet was inspected. This remains a line/sole-volume source diagnostic; body counter-motion, cloth, hands, actual boot materials, full-character silhouette and distinct facings remain unfinished. The previous sampled-frame world-travel sliding concern remains unresolved; preserving continuous source support is not a real-renderer travel test.

Reproduce with Python 3 and Pillow: python3 cycle.py. Exact recipe, parameters, authored key, samples, verification and images are in source.zip. No active code/resources changed. Latest core validation remains the clean 773-test / 109-suite run recorded in recovery-pose-correction; this source-only change did not rerun it. Script assertions and reproduction passed.

Next: apply the owned boot volume and retained costume layers to these poses, review knee/ankle occlusion across the range, then advance through the existing full-art and renderer gates. This diagnostic does not replace those gates.
