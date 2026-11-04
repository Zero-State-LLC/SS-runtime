# Caption board

Read 2026-11-04 from `CaptionBoard` on `93f6d67`. No cue was reclassified.

Safety captions are `player_damage`, `daemon_query`, `daemon_dash`, `exposure_state_up`, `lockdown_enter`, `extraction_armed`, `extraction_reset`, and `extraction_tick`. Any cue id that starts with `boss_telegraph_` is safety as well. Every other cue is routine.

The board shows at most 3 captions. Each lasts 150 ticks from the tick it was ingested. A repeat of the same caption drops the old entry and starts the time again. Off shows nothing. Important shows safety captions. All shows safety and routine.

The three that show are ranked safety before routine, then the lower cue priority number, then the newest. They are drawn oldest first. The board counts simulation ticks, so it holds still while the run is paused or in hit-stop.
