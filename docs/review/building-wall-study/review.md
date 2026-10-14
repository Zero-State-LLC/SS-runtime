# Building wall separation study

Tool: built-in image_gen, 2026-10-14. Exact prompt in prompt.txt; unmodified generated source in source.png. Input was the existing building.png benchmark asset. Runtime baseline 9501261; specification c773f960ee8f53ac429828767fcd09f4da0d7cb3.

OBSERVED: the elevated candidate removes the baked sidewalk apron, trees, fences and stairs while retaining paired teal/brick facades, cream trim and roof details. Entrances now meet its base. This isolates vertical artwork more clearly than the old scenic cutout.

FAILED: the accompanying plan contains roof-like finials and does not unambiguously map the visible door locations. It is not an editable or measured ground-plan master. Bay projections also make the footprint nonrectangular; it cannot be fitted truthfully to the existing square obstacle by scaling. Neither panel is admitted to production. No collision change or renderer substitution was made.

Next: establish an explicit authored footprint for the projection comparison, then render the wall asset against that constraint. Preserve facade materials where practical; avoid asking an image model to independently invent the technical plan and certify its own geometry. The current arena remains authoritative.

Validation: runtime spec pin reconciled to c773f960ee8f53ac429828767fcd09f4da0d7cb3. All 21 contract/fixture JSON files match that exact commit, except the documented catalog specificationCommit field. Four targeted ContractVersionsTests and AssetCatalogTests passed. No simulator or physical-device test was rerun for this documentation/pin-only adoption; no renderer behavior changed.
