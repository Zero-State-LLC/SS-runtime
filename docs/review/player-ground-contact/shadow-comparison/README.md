# Isolated shadow placement comparison

2026-10-19: build succeeded; two native Simulator tests passed, zero failures, 36.748 seconds. Twelve traversal configurations compare production-default shadow drop and review-only placement at the player ground root. All retain 16 movement frames, expected simulation trace/digest, supported held idle and zero outline readbacks. Shadow-to-ground deltas are measured after scene transforms. Source registration, size, art, timing, shadow texture/size/opacity and production default remain unchanged.

Initial compilation caught an ambiguous .zero overload; corrected to CGPoint.zero before the successful build. Specs validation and diff whitespace checks passed.

This is geometric and behavior evidence. No new visual capture was produced by these tests (capturesImages remains false); normal/quarter visual comparison is still required before selecting the candidate. Do not treat this as visual acceptance or a full-suite run.
