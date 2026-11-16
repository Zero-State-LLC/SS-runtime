# Trail check disposition

`trail check --base HEAD` at23:30 returned one lexical conflict on the new CI step at `.github/workflows/ci.yml:138`: it matched words "test ground native" to the older learning about unwrapped `frameIndex` freezing a fixed-time Player animation. Raw output is `trail-check-2330.log`. The check was limited to the first400KB of this evidence-heavy diff, not a complete independent code review.

The new CI step invokes portable V8 semantic/source/capture-retention and gallery checks. It does not change `AppTests/PlayerGroundContactNativeTests.swift`, reintroduce its frame-index code, or change any looped playback. V8 is explicitly a stationary ordinary-scene comparison, not animation-family evidence. The existing loop-wrapping correction and its strict diagnostics remain intact. Thus this match does not identify a substantive conflict with the learning, and the change proceeds with this reason in the commit message and PR publication note. No Trail rule or learning was weakened or edited.

The initial shell used `trail check && export`, so export did not execute in that command. The separately logged export is the actual validation. The source geometry, exact oracle regression and retained native provenance remain independently checked. Keyword advisories are not visual acceptance and do not justify modifying immutable historical bytes.
