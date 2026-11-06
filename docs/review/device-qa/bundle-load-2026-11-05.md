# The bundled lookup

Read 2026-11-05 from `BundledResource.data` on `ef68565`. No asset was admitted. Intake stays in [asset-intake-2026-11-05.md](asset-intake-2026-11-05.md). Reachable ids stay in [bundle-filter-2026-11-05.md](bundle-filter-2026-11-05.md). Catalog refusal stays in [catalog-gate-2026-11-05.md](catalog-gate-2026-11-05.md).

`data` loads `Bundle.module` for `name` with extension `json` in `subdirectory`. When that URL is missing, the path is `#filePath` two directories up, then `Resources/<subdirectory>/<name>.json`. Either path is read with `try!`.

`RuntimeAssetBundle.url(forFile:)` looks in subdirectory `RuntimeAssets` with no extension. The fallback is `Resources/RuntimeAssets/<name>`. A fallback path that `FileManager` reports as absent returns nil.

`SpecBundle.contract` uses subdirectory `contracts`. `SpecBundle.fixture` uses subdirectory `fixtures`.

This does not admit an asset.
