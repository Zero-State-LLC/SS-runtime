# Receipt archive

Read 2026-11-04 from `ReceiptArchive` on `5d954be`. No receipt field was added.

The receipt fields stay in [run-receipt-2026-11-04.md](run-receipt-2026-11-04.md). Encoding stays in [canonical-json-2026-11-04.md](canonical-json-2026-11-04.md).

`ReceiptStore` writes under Application Support, directory `RunReceipts`. It stores only when the outcome is terminal. A serialized receipt of length 0, or a digest shorter than 12 characters, is refused.

The filename is `run-` plus a UTC stamp `yyyyMMdd'T'HHmmss'Z'` plus `-` plus the first 12 characters of the digest, and `.json`. The stamp is the device clock. The bytes are written to a hidden temporary file in that directory, the previous file of the same name is removed, and the temporary file is moved into place. A failure removes the temporary file.

The directory keeps 50 receipts. Past that, the oldest go. Age is the file creation date, and equal dates sort by filename. `GameScene` attempts the store once. A thrown write leaves the guard clear, so a later tick tries again. `beginRehearsal` sets the guard, so a rehearsal is not archived.

This does not add a receipt field.
