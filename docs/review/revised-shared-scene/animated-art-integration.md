# Shared animated-art integration

Installing environment review art previously forced a static player texture and removed actions on every render. BenchmarkReviewArt now has an explicit playerPresentation mode: staticComposition remains the default; selectedClip leaves normal clip selection, occurrence facing, action timing and fallback intact.

The regression compares shared-art and normal renderers across movement, idle, dodge, event-owned hurt and an unsupported direction, with repeated render calls in both motion modes. It also verifies the static control. The new test passed; the fresh suite passed 115 named tests / 117 executions, with no failures. Specs validation passed.

This enables the next live shared traversal but is not that traversal. No production art admission, full-facing acceptance or performance acceptance is claimed.
