# Retained v5/v6 export-manifest semantic validation gap

Found during independent v7 fixture review on November 16, 2026.

`scene-qa-repair-20261116/retained.py:24-33` requires the manifest filename and verifies its bytes against the verification report, but `verify` never parses its test/attachment identities. The v6 retained adapter delegates directly to that implementation. A changed manifest with a recomputed self-reported digest can therefore bypass semantic identity checking. This is a coverage defect, not evidence that the preserved actual manifests are wrong, and not cryptographic authentication against coordinated replacement of every trust anchor.

The new isolated v7 adapter independently calls `validate_attachment_manifest`: exact one selected test, nineteen unique expected attachments, one device, expected file types, no failures. Its 41 portable tests passed independently in `scene/coordinator-tests-2235.log`, including rehashed malformed manifests. No older verifier, old evidence, assertions or thresholds were changed.

Follow-up: authorize a separately reviewed historical-verifier hardening slice, preserve historical capture bytes, add exact empty/duplicate/wrong-test/mixed-device mutation tests, and verify the old actual manifests remain accepted. Keep this issue open until integration evidence is reviewed. V7 passing does not close the inherited gap.
