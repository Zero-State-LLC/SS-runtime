# Share text

Read 2026-11-04 from `RunCard.shareText` on `fcab4e5`. No label was changed. The clock, the ghost row, and the three outcome sentences stay in [run-card-2026-11-04.md](run-card-2026-11-04.md).

Share joins one line per row with newlines. The first line is `Surveillance Survivor`. The second is `INCIDENT REPORT · DATE` and the date, or `INCIDENT REPORT` when the card has no date. The third is `OUTCOME:` and the incident sentence.

Every other card row is included except `DATE` and `MEDALS`. `TIME` and `CAMERAS` use the report labels already recorded on the run card. `PEAK DETECTION` and `GHOST` keep those labels. The camera value is the destruction count, a slash, and 8. When the network is blacked out it also appends `NETWORK BLACKOUT`. Peak detection is the state name in capitals. A run that has entered lockdown prints `LOCKDOWN`. Otherwise the name comes from the peak exposure: `HIDDEN`, `OBSERVED`, `TRACKED`, or `HUNTED`.

When a success earned medals, the last line is `MEDALS` and the earned names in enum order, separated by spaces: `GHOST`, `SHADOW`, `BLACKOUT`, `SURGICAL`, `SWIFT`. The card's own medal row joins those names with a middle dot and writes `NEW` after a medal earned for the first time today. The share line leaves both of those off.

This does not add a row.
