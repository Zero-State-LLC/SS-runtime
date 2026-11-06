# The diagnostic seal

Read 2026-11-05 from `Simulation.invalidate` on `ef68565`. No outcome was retuned.

The code names and the seal-once rule stay in [terminal-seal-2026-11-04.md](terminal-seal-2026-11-04.md).

The function returns unless the outcome is `playing` or `upgradeSelectionPending`. It then sets the outcome to `invalid`, stores the code, and seals with `state.tick`. The event is `diagnosticFailure` at phase 18. The payload key is `code`, and the value is the code's raw value.

This does not add a diagnostic code.
