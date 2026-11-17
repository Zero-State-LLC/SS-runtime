# Coordinator Release isolation check

2026-11-17 03:15UTC. Independently inspected the actual successful Release build at `release/derived/Build/Products/Release-iphonesimulator/SSRuntime.app`, not just preprocessor source.

- Executable exists, SHA256 `04fab4f35bb7ebf66727e31cabef686ca17440aeaea34c932d41c714c9839f95`.
- `nm -j` completed successfully and contained no `KioskPlayableReview` symbol.
- Executable bytes contain neither `-SSKioskReview` nor `debug-playable-kiosk-review-001`.
- Enumerated and SHA256-hashed all1032PNG files under the actual Release app. None matches any of the three exact current/candidate/base review PNG hashes from `resources/`.

The script asserted a nonempty Release inventory, exactly three distinct review hashes, successful symbol extraction and absence of all matches. This establishes exclusion of this unaccepted review helper and its exact image bytes from this built Release bundle. It is not proof of app-store readiness, physical-device behavior, rights clearance or overall asset acceptance. No release/deployment was performed.
