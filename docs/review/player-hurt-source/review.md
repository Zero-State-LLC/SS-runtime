# BP-002/BP-003 hooded hurt source study

Status: CAPTURED / not admitted. Built-in image_gen produced a three-pose strip using the existing west costume reference and approved shared scene. Exact prompt is prompt.txt. Original is source.png; source hash and delivery hashes are export-records.json. This uses the user's authorized deterministic alpha cleanup and registration workflow.

OBSERVED: costume identity is more consistent than the currently bundled hurt frames: hood, strap, belt, arm patch and boots remain recognizable. The elevated view exposes the top of hood and shoulders. The middle pose bends and brings the arms inward; the final pose recovers. This is a qualitative source comparison, not renderer or benchmark acceptance.

Three 384×384 candidate exports use one uniform scale (312/706), with logical 64×64 canvas and (32,56) anchor. All are downsampled from the generated source, not enlarged from the 256px delivery. No frame is independently stretched or normalized by its alpha box. Alpha cleanup removes low-alpha haze; RGB is unchanged. Exact recipe: export.py. All three resulting alpha bounds remain within the canvas without edge clipping.

FAILED planted-foot invariance: approximate manually annotated sole centers vary by up to 5.60 export pixels (0.93 logical units) relative to pose 1 after root registration. These are diagnostic estimates, not a precise contact solve or an acceptance threshold. See landmark-drift.json. Foot spacing and costume contour still shift; registration cannot repair those anatomical changes.

OPEN: controlled editable source/pose master, consistent four-facing identity, matching live-state neutral/movement transition, real-renderer playback and normal/Reduced Motion review. The generated raster is not a rig or a complete character sheet. This study may guide a corrected source, but must not replace production frames yet. No new cadence: comparison uses the existing three-frame 20-fps hurt duration (150 ms); no authoritative damage or movement changes.

Validation is image/export inspection only. No runtime resources or code changed, so no new runtime test claim is made. Previous renderer evidence remains at runtime 987c32a. Spec authority remains 56a5a5da1d87491d23df86731cc01a5acd868d26, BP-002/BP-003/BP-007. Art improvement is partial; the benchmark remains unachieved.
