# Clean-silhouette renderer review — 2026-10-15

New actual Simulator/SpriteKit recording with the latest startup readiness preparation. South-facing hooded player, approved narrower stance, arm swing and restored knee-pad detail unchanged. The review-only switch hides faction-outline nodes after action synchronization. Existing outline controls and production presentation policy remain unchanged.

The clean review test passed: all 16 frames, three observed cycle wraps, zero playback texture readbacks. The full recorded app run had 112 passing executions and one failure: Reduced Motion delivered 15/16 frames. That result is retained; this is not a fully passing app run. Concurrent core testing and recording were active, so the cause is not isolated. Previous unrecorded app run passed all 112 executions before adding this review-only switch.

Normal and quarter speed are separate HTML pages, with detail and full-viewport options. Quarter speed replays the same recorded frames at 0.25x, with no interpolation. The original continuous recording is ../SS-player-startup-review/clean-silhouette-renderer.mov. Review extract starts at 361.75 seconds and spans approximately 2.15 seconds; original timestamps preserved through export. Test metadata and post-action records are alongside this report.

Review contact, knee orientation, heel/tongue ownership, coat overlap, arm motion and internal 16→1 seams. The outer movie loop is not an animation seam. Only south walk is represented; candidate idle and unseen facings remain incomplete. Shared scene and device testing remain gated on review. No shipping art or accessibility policy was changed.

Full core regression completed: 773 tests across 109 suites passed in 832.380 seconds (exit 0). This does not clear the separate recorded Reduced Motion app failure.
