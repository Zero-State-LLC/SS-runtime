# Environment filter

Read 2026-11-05 from `EnvironmentTextures.texture` on `87ab159`. No texture was replaced.

The decoration load stays in [decoration-placement-2026-11-02.md](decoration-placement-2026-11-02.md). Clip filtering stays in [clip-playback-2026-11-04.md](clip-playback-2026-11-04.md).

A texture is cached by asset id. The loaded image uses nearest filtering. Ground, fog, solids, housings, captain art, and props all use this function. A missing path, file, or image returns nil, and the caller keeps its own fallback.

This does not replace a texture.
