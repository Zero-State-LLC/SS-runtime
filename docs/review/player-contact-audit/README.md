# Player contact evidence audit — 2026-10-16

T1045 / BP-008. Inspection of existing continuous-renderer records; no new simulator run or production change.

## Observed

All 16 current `AppTests/BenchmarkAssets/player-source-s-*.png` files and the pose JSON match the 17 SHA256 values recorded in `../player-low-recovery/source-record.json`. Both historical shared traversal modes observed all 16 frames. The shared test uses a fixed half-second clip and an explicit front-source alias for world SW travel; it is not the separate distance-phase experiment.

Applying the authored support-toe model to recorded rendered roots yields support-segment vertical ranges of 2.614–5.013 logical units in standard motion and 2.399–4.735 in Reduced Motion. Five segments per mode are retained in contact-audit.json, with sample count, distinct frames and observations. One standard segment has only three distinct poses; the others have four. Do not erase held-frame movement or replace missing observations with interpolated proof.

Method: rendered root Y minus half the authored forward toe coordinate plus toe height. The candidate uses six source pixels per logical unit and upright art. These are model-derived contacts, not tracked sole pixels, and no pass tolerance is adopted. Records lack exact movie-frame timestamps, so video-to-telemetry identity remains approximate; do not label individual movie frames with presumed pose IDs.

The source sixteen-pose and seam plates were inspected. They retain the hood, asymmetric strap/pouch, narrow stance and opposing arm variation. Lower-leg material is still visibly less detailed than the torso at enlarged scale. Static plates cannot establish normal-speed motion quality or a smooth displayed seam. No fresh normal/quarter-speed playback judgment is claimed by this audit.

## Consequence

Player contact remains open despite complete texture coverage. Use the existing continuous renderer test for the next comparison, retaining exact source hashes and selected clip, and review normal and quarter speed separately. Establish displayed sole-to-ground behavior before changing timing or source amplitudes; compare against the existing distance-phase evidence rather than inventing a new playback policy. Preserve stance, arm swing and lower knee recovery. Complete missing authored facings/actions after the south contact/finish gate; enemy production stays deferred until Player completion.

Camera-depth/exterior videos are neutral-pose captures with paused actions and cannot substitute for this evidence. This audit changes no runtime behavior and does not require repeating the previously passing core suite.


## Decoded movie seam inspection

The existing standard-motion detail MP4 was decoded with passthrough timestamps: 125 actual video frames, without FFmpeg's default duplication to a constant-rate raw stream. A lower-body masked RGB template comparison estimates source pose and origin for each frame; source remains unmodified. The two detected wraps are near movie frames 45 and 104. `pixel-match.json` retains scores, runner-up scores, timestamps and video hash. These are estimated image matches, not authoritative pose IDs. `track_capture.py` is an offline inspection recipe using the workspace-relative source/video paths, not a runtime tool.

`live-seam-104.png` shows the second 16→1 transition in actual captured pixels. The hood, strap and body retain registration across the seam; the advancing foot changes pose without a visible detached limb in this inspected sequence. `live-seam-45.png` contains an ambiguous image at movie frame 45 with substantially higher template error; its estimated pose must not be used to claim a reversal or source defect. Investigate the original capture if that transient recurs. Neither plate establishes subjective normal-speed acceptance or proves a stationary support foot. Prior modeled-contact findings remain open.

Separate existing continuous clips remain at `outputs/SS-shared-traversal-recorded/standard-normal-detail.mp4` and `standard-quarter-detail.mp4` at workspace level. These are historical simulator motion, not the later paused Camera repair. No new animation or physical-device acceptance is claimed.
