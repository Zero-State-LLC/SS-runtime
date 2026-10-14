# Intent

**Author:** Codex, at the repository owner's direction
**Date:** 2026-10-13
**Status:** accepted
**Next stage:** implement the SS-specs D-102 / PC-009 correction

Owner authorization: “execute plan” on 2026-10-13, referring to the reviewed three-fix plan.

## Problem

The sole controller-to-session input transfer is inside DEBUG. Release builds never consume movement or Dodge.

## Proposed outcome

Touch movement, one-shot Dodge, pause/resume, and restart pass through the production scene in Debug and Release. Existing CI verifies both configurations.

## Affected users/systems

Players, GameScene input integration, app tests, and existing CI.

## Constraints/non-goals

Preserve input quantization, debug autopilot, and one-level scope. Gameplay Exposure changes are owned by SS-specs intent/2026-10-13-audit-corrections.md and D-102, not this runtime-only intent.

## Open questions

None for the authorized correction. Physical-device acceptance remains separate.

## Verified claims

OBSERVED: applyController's only caller is conditionally compiled under DEBUG; touch callbacks mutate the controller but not the session. Existing controller tests do not traverse that boundary.

## Assumed claims

Debug and Release simulator tests must establish the correction; source inspection alone does not establish interactive acceptance.
