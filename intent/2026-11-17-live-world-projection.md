# Approved live presentation-projection correction

Owner approval:2026-11-17T03:40:46.895Z, replying to the explicit request to authorize a broader presentation-projection correction after the live kiosk/foundation mismatch. Base:2baaeb1765c1df0618b79c1af826f40139d4d793, openPR236.

## Outcome

A reversible actual-playable review route in which ground geometry and registered upright roots use the same midpoint projection. It must not be merely a transformed still or an attractive replacement scene. The existing kiosk current/candidate sources, their base, and neighboring asset designs remain frozen.

## Engineering choice

Add an explicit Debug-only projection opt-in alongside the validated kiosk review flags. Keep ordinary/default and Release behavior unchanged until reviewed. Reuse the existing midpoint forward/inverse math rather than introduce a new artistic camera. Ground surfaces, foundations, fields, telegraphs, shadows and world effects use one mapping. Upright artwork keeps its local shape and projects its ground root exactly once. HUD and screen effects remain screen-space. Camera follow and manual analog input are projection-aware without modifying authoritative mechanics or the world-space autopilot.

## Acceptance checks

1. Flag absent: unchanged default behavior. Invalid/partial flags fail closed. Release executable contains no new review launch/schema/symbol markers.
2. Independent geometry tests compare ground corners, actor/Camera/kiosk roots and field points against analytic projection. Upright texture/anchor/scale and source bytes are unchanged. Retained foundation is not hidden to conceal mismatch.
3. Live callbacks restore authoring-space transforms before updates/actions and reapply after them without drift, stale parents, animation resets or duplicate projection. Cover pause/resume, redraw, new nodes, toggle/remove and restart.
4. Equal legal authoritative commands produce equal per-tick digests and complete snapshots with/without presentation mode. Manual screen input maps back to normalized world direction without changing analog magnitude, touch layout, deadzone, dodge or choice controls. Autopilot commands remain world-space.
5. Actual native tests and ordinary-start legal-pilot app captures show the selected mode and NOT ACCEPTED status. Preserve failed attempts and record exact build/source identities. Raw asynchronous app frames are not matched-tick pixel equivalence.
6. Independently inspect actual visible results. Report unresolved ground contact, occlusion, framing or source-registration deficiencies honestly rather than claiming art acceptance from geometry tests.
7. Publish verified code, tests, docs and handoff to existingPR236, preserving all old packets and unrelated untracked work.

## Boundaries

No changes to simulation, collision, arena coordinates, Camera fields/roots, Player roots, rules, content contracts or canonical asset admission. Approval permits the necessary presentation transforms across neighboring objects, not redesigning or regenerating their source art. No paid generation, issue closure, merge, release/deploy, physical certification or owner art acceptance is granted. New evidence belongs under `docs/review/live-world-projection-20261117/`.
