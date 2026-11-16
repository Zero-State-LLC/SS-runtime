# First native build attempt, November 16 06:44 UTC

The coordinator selected all three new existing-art tests for a compilation/integration smoke run. It was not an importable one-test packet result. The build failed with Swift's ambiguous `zero` overload in `ExistingArtTraversalTests.capturePair`; `player.convert(.zero, to: scene)` could refer to CGPoint or CGRect.

The coordinator changed only that expression to `CGPoint.zero`. No assertion, fixture, runtime behavior or evidence gate was relaxed. `summary.json` reports result unknown and totalTestCount0. This attempt is failed build evidence, never a passing test. The full xcresult remains at `/Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-native-20261116-0644.xcresult`; `xcode-test.log` is retained here. The next attempts use separate direct one-test selections and fresh result paths with the same warmed derived-data directory.
