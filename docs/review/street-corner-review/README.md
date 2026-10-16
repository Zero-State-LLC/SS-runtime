# Street-corner composition trial

Specs first: benchmark-production.md defines a researched street organization trial, with proposed fixture dimensions separated from NACTO guidance. Runtime BenchmarkReviewArt.configureStreetCorner shares road/curb/rail/crossing placement between static and live review fixtures. No collision, actor size, cadence or rules changed.

Captured by testCaptureCompleteCameraCandidatesInSharedScene (passed, 16.842 s) in Test-SSRuntime-2026.10.15_21-09-37--0700. Overall suite was deliberately stopped after Xcode retained the old full scheme; do not claim a full pass. Updated live traversal remains unverified. Swift parse and diff checks pass.

Visual inspection: road now wraps the corner and separates sidewalk from asphalt. Camera field remains visible, player retains clean review silhouette. The small player/large viewport and crossing clipped by lower edge remain below benchmark. Next: closer framing comparison with unchanged world sizes and HUD, then targeted traversal. Added SSBenchmarkReview scheme and its project.yml source for focused iteration, but UI selection has not yet been verified effective.
