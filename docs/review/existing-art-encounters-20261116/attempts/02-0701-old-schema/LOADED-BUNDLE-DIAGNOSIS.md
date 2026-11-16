# Loaded-bundle diagnosis, November 16, 2026 07:09 UTC

The untouched 07:01 xcresult was independently exported again into a fresh directory. Its encounter ledger still reports `existing-art-encounters-v1`. This excludes contamination from the first export directory.

`runner-session.log` is the actual xcresult-exported session diagnostic. At local 23:01:49.565 (November 16 07:01:49.565 UTC), XCTest logs loading its test bundle from:

```
/Users/appliedalchemylabs/Library/Developer/CoreSimulator/Devices/84297C74-033E-408F-9622-D36BFF32F74E/data/Library/Caches/com.apple.containermanagerd/Dead/temp.2xAkmi/C472D75F-5D11-48A5-8CAF-B2D2FE8BEE79/SSRuntime.app/PlugIns/SSRuntimeTests.xctest/
```

At 07:09 UTC the executable at that exact path still existed. Read-only `shasum -a 256` returned `ae9e1477a9319fabe8a51e372f374e2565c7c99eefedca5c110ac7c91c3d1ece`. `strings` found `existing-art-encounters-v1`.

In contrast, the current derived-product executable and current `simctl get_app_container` executable both hash to `cb8a0f252bb2bb46bca16c808eba373569f31fcfe1d4640bef487016c91e5504` and contain `existing-art-encounters-v2` plus `staged snapshot Player center, not live follow`. The derived binary modification time is November 16 06:59:16 UTC, before the 07:01 run. The 06:59 traversal build log records compilation of the corrected encounter source.

Thus the runner reported loading an older, relocated bundle rather than the currently installed corrected bundle. Checking only the current installed path did not establish executed-test provenance. The mechanism that retained the old path is not proven. No production defect is inferred.

The coordinator scheduled one focused retry after shutting down and rebooting only dedicated simulator `84297C74-033E-408F-9622-D36BFF32F74E`, without erasing data or changing assertions/source. Result path ends `0710.xcresult`. Its outcome must be verified from fresh attachments and runner diagnostics, not from xcodebuild success alone. Historical 07:01 evidence remains rejected for corrected framing.
